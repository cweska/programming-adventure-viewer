/**
 * The exercise player's run loop, end to end on real course content, in CPython with the browser
 * worker's exact course-run semantics: flattenChecks -> run -> gradeCheckpoints -> runOutcome -> applyRun.
 * Also renders every played item on the server (the static export pre-renders these pages).
 */
import { createElement } from "react";
import { renderToString } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { ExerciseProgress } from "../../lib/course/contracts";
import { flattenChecks, gradeCheckpoints } from "../../lib/course/grading";
import { allUnits, itemPageProps } from "../../lib/course/registry";
import { runCourseChecks } from "../../lib/course/run-course";
import { playablesOf, type Checkpoint, type Playable } from "../../lib/course/schema";
import { applyRun, assembledCode, isBlankOrStarter, runOutcome } from "./exercise-logic";
import { LessonPlayer } from "./LessonPlayer";
import { ParsonsBoard } from "./ParsonsBoard";

const PLAYED = new Set(["lesson", "project", "challenge", "testout"]);

const playables: { where: string; exercise: Playable }[] = allUnits.flatMap((unit) =>
  unit.items.flatMap((item) =>
    playablesOf(item).map(({ key, exercise }) => ({ where: `${unit.id}/${item.id}${key ? `/${key}` : ""}`, exercise })),
  ),
);

function bonusCheckpoint(exercise: Playable): Checkpoint[] {
  return exercise.bonus ? [{ id: "__bonus", text: exercise.bonus.text, hints: exercise.bonus.hints, checks: exercise.bonus.checks }] : [];
}

/** One Run press, exactly as ExercisePlayer does it (bonus checks ride along). */
function press(exercise: Playable, code: string, progress: ExerciseProgress) {
  const bonus = bonusCheckpoint(exercise);
  const result = runCourseChecks(code, [...flattenChecks(exercise.checkpoints), ...flattenChecks(bonus)], {
    setup: exercise.setup,
    stdin: exercise.stdin,
    engine: exercise.engine,
  });
  const grade = gradeCheckpoints(exercise.checkpoints, result, code);
  const bonusGrade = bonus.length > 0 && !grade.crashed ? gradeCheckpoints(bonus, result, code) : null;
  const outcome = runOutcome(grade, progress.passed);
  return { grade, bonusGrade, next: applyRun(progress, outcome, { code, bonusPassed: bonusGrade?.allPassed }) };
}

const fresh = (): ExerciseProgress => ({ passed: [], done: false, hintsUsed: {}, failedRuns: 0 });

describe("the run loop on course content", () => {
  it("has content to test", () => {
    expect(playables.length).toBeGreaterThan(0);
  });

  for (const { where, exercise } of playables) {
    it(`${where}: starter and solution behave`, () => {
      const starter = press(exercise, exercise.starter, fresh());
      if (exercise.starterPasses) {
        expect(starter.grade.allPassed).toBe(true);
        expect(starter.next.done).toBe(true);
      } else {
        expect(starter.grade.allPassed).toBe(false);
        expect(starter.next.done).toBe(false);
      }

      const solved = press(exercise, exercise.solution, starter.next);
      expect(solved.grade.allPassed, JSON.stringify(solved.grade)).toBe(true);
      expect(solved.next.done).toBe(true);
      expect(solved.next.passed.sort()).toEqual(exercise.checkpoints.map((checkpoint) => checkpoint.id).sort());
      expect(solved.next.code).toBe(exercise.solution);
    });

    if (exercise.bonus) {
      it(`${where}: the side quest passes with its solution and not with the main one`, () => {
        const main = press(exercise, exercise.solution, fresh());
        expect(main.bonusGrade?.allPassed).toBe(false);
        expect(main.next.bonusDone).toBeUndefined();
        const side = press(exercise, exercise.bonus!.solution, main.next);
        expect(side.grade.allPassed).toBe(true);
        expect(side.bonusGrade?.allPassed).toBe(true);
        expect(side.next.bonusDone).toBe(true);
      });
    }

    if (exercise.assemble) {
      it(`${where}: "Assemble it" with the right lines passes`, () => {
        expect(isBlankOrStarter(exercise.starter, exercise.starter)).toBe(true);
        const code = assembledCode(exercise.assemble!.lines);
        expect(press(exercise, code, fresh()).grade.allPassed).toBe(true);
      });
    }
  }

  it("a crash fails every checkpoint and counts as a failed run", () => {
    const { where, exercise } = playables.find((entry) => !entry.exercise.starterPasses)!;
    const { grade, next } = press(exercise, "print(\n", fresh());
    expect(grade.crashed, where).toBe(true);
    expect(next.failedRuns).toBe(1);
    expect(next.passed).toEqual([]);
  });
});

describe("server render", () => {
  const items = allUnits.flatMap((unit) => unit.items.filter((item) => PLAYED.has(item.kind)).map((item) => ({ unit, item })));

  for (const { unit, item } of items) {
    it(`renders ${unit.id}/${item.id} (${item.kind})`, () => {
      const props = itemPageProps(unit.id, item.id);
      expect(props).toBeDefined();
      const html = renderToString(createElement(LessonPlayer, props!));
      expect(html).toContain('data-testid="lesson-player"');
      expect(html).toContain('data-testid="exercise-player"');
      expect(html).toContain('data-testid="run"');
      expect(html).toContain('data-testid="checkpoint-1"');
      expect(html).toContain('data-testid="item-continue"');
      if (item.kind === "lesson" || item.kind === "testout") expect(html).toContain('data-testid="exercise-rail"');
      if (item.kind === "testout") {
        expect(html).toContain('data-testid="testout-intro"');
        expect(html).not.toContain('data-testid="hint-button-1"');
        expect(html).not.toContain('data-testid="another-way"');
      }
    });
  }

  it("renders an article's try-it exercises without a Continue of its own", () => {
    const unit = allUnits.find((candidate) => candidate.items.some((item) => item.kind === "article" && item.exercises.length > 0));
    if (!unit) return;
    const article = unit.items.find((item) => item.kind === "article" && item.exercises.length > 0)!;
    if (article.kind !== "article") return;
    const props = itemPageProps(unit.id, article.id)!;
    const html = renderToString(
      createElement(LessonPlayer, {
        ...props,
        item: { kind: "lesson", id: article.id, title: article.title, optional: true, exercises: article.exercises },
      }),
    );
    expect(html).toContain('data-kind="try-it"');
    expect(html).not.toContain('data-testid="item-continue"');
  });

  it("renders the Parsons board with every piece reachable by button", () => {
    const html = renderToString(
      createElement(ParsonsBoard, { blocks: ["a = 1", "print(a)"], value: ["print(a)"], onChange: () => undefined, idPrefix: "pz" }),
    );
    expect(html).toContain('data-testid="pz-piece-0"');
    expect(html).not.toContain('data-testid="pz-piece-1"');
    expect(html).toContain('data-testid="pz-line-0"');
    expect(html).toContain('aria-label="Move line 1 up"');
  });
});
