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
import { exerciseSchema, playablesOf, type Checkpoint, type Playable } from "../../lib/course/schema";
import { CompareView } from "./CompareView";
import { applyRun, assembledCode, helpRungs, helpState, isBlankOrStarter, runOutcome } from "./exercise-logic";
import { ExercisePlayer } from "./ExercisePlayer";
import { HelpStack } from "./HelpStack";
import { LessonPlayer } from "./LessonPlayer";
import { NamesChips } from "./NamesChips";
import { ParsonsBoard } from "./ParsonsBoard";
import { PredictStep } from "./PredictStep";
import { SymbolTray } from "./SymbolTray";

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
  // As the player does it: the side quest's checks are graded from their own slice, by position.
  const mainCount = flattenChecks(exercise.checkpoints).length;
  const bonusGrade =
    bonus.length > 0 && !grade.crashed
      ? gradeCheckpoints(bonus, { ...result, checks: (result.checks ?? []).slice(mainCount) }, code)
      : null;
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
      it(`${where}: the side quest counts after the exercise is done`, () => {
        const early = press(exercise, exercise.bonus!.solution, fresh());
        expect(early.bonusGrade?.allPassed).toBe(true);
        const main = press(exercise, exercise.solution, fresh());
        expect(main.next.done).toBe(true);
        const side = press(exercise, exercise.bonus!.solution, main.next);
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
        expect(html).not.toContain('data-testid="help"');
        expect(html).not.toContain('data-testid="help-button"');
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

  it("renders one Help control (not per-step hint lists) on a full-support lesson", () => {
    const entry = items.find(({ item }) => item.kind === "lesson");
    if (!entry) return;
    const html = renderToString(createElement(LessonPlayer, itemPageProps(entry.unit.id, entry.item.id)!));
    expect(html.match(/data-testid="help-button"/g)?.length).toBe(1);
    // The first rung is Start me off when the step's last hint has a line to start from, else Where to look.
    expect(html).toMatch(/Help: (Start me off|Where to look)/);
    expect(html).not.toMatch(/data-testid="hint-button-\d/);
  });

  const unitOneStyle = exerciseSchema.parse({
    id: "label-a-box",
    title: "A box with a label",
    martu: "A box has a label and something inside.\nRead `=` as gets.",
    example: { code: 'snack = "glug"\nprint(snack)\n', output: "glug\n" },
    starter: 'companion = "Gearshift"\nprint(companion)\n',
    solution: 'companion = "Bomb Shell"\nprint(companion)\n',
    names: ["companion"],
    pick: "Bomb Shell",
    pairTalk: "Pair talk: tell your partner what line 2 shows.",
    solo: true,
    predict: { q: "What will this print?", choices: ["Gearshift", "companion"], answer: 0, explain: "No quotes: look inside the box." },
    checkpoints: [
      {
        id: "another-hero",
        text: "Change the hero.",
        dictated: false,
        hints: ["Line 1.", "The value goes in quotes.", "`snack = \"glug\"` makes a box."],
        checks: [{ name: "c", code: "assert companion != 'Gearshift', 'Pick another hero.'" }],
      },
    ],
  });

  it("renders Predict, Names to use, Mar'tu's pick, Pair talk, Solo and the symbol tray", () => {
    const html = renderToString(
      createElement(ExercisePlayer, {
        unitId: "u",
        itemId: "i",
        exerciseKey: "u/i/label-a-box",
        exercise: unitOneStyle,
        glossary: [],
        settings: { solutionAfterMinutes: 5, solutionAfterFailedRuns: 4 },
        mode: "lesson",
      }),
    );
    expect(html).toContain('data-testid="predict"');
    expect(html).toContain('data-testid="predict-skip"');
    expect(html).toContain('data-testid="name-chip-companion"');
    expect(html).toContain('aria-label="Put companion in your code"');
    expect(html).toContain('data-testid="pick-use"');
    expect(html).toContain("Bomb Shell");
    expect(html).toContain('data-testid="pair-talk"');
    expect(html).toContain('data-testid="pair-talk-dismiss"');
    expect(html).toContain('data-testid="solo"');
    expect(html).toContain('data-testid="symbol-tray"');
    // Non-dictated step: the names are shown prominently.
    expect(html).toContain("ex-extras is-prominent");
    // SOLO: Help starts at Where to look.
    expect(html).toContain("Help: Where to look");
    expect(html).not.toContain("Start me off");
    // Mar'tu's version is never shown before it is asked for.
    expect(html).not.toContain('data-testid="compare"');
    expect(html).not.toContain("Bomb Shell\nprint");
  });

  it("renders the Help stack's open rungs, a highlighted offer, and a locked Show me", () => {
    const checkpoint = unitOneStyle.checkpoints[0];
    const rungs = helpRungs(checkpoint, { anotherWayCount: 0, hasAssemble: false, solo: false });
    // Every rung open but the last: Compare with Mar'tu's version is next, and still locked.
    expect(rungs.map((rung) => rung.kind)).toEqual(["start", "point", "teach", "how", "show"]);
    const state = helpState(rungs, rungs.length - 1, false);
    const html = renderToString(
      createElement(HelpStack, {
        noun: "Step",
        stepNumber: 1,
        checkpoint,
        state,
        anotherWay: [],
        glossary: [],
        offer: "misses",
        compareOpen: false,
        showUnlocked: false,
        runNumber: 3,
        onReveal: () => "opened" as const,
        onDismissOffer: () => undefined,
        onOpenAssemble: () => undefined,
        onOpenCompare: () => undefined,
        onInsertStart: () => undefined,
      }),
    );
    expect(html).toContain('data-testid="help-rung-1"');
    expect(html).toContain('data-testid="help-start-code"');
    expect(html).toContain("<code>snack =</code>");
    expect(html).toContain('data-kind="how"');
    expect(html).toContain('data-testid="help-rung-3"');
    expect(html).toContain('data-kind="teach"');
    expect(html).toContain('data-testid="help-offer"');
    expect(html).toContain("Read the last line first");
    expect(html).toContain('data-testid="help-show-locked"');
    expect(html).toContain('aria-disabled="true"');
    expect(html).toContain("ex-help is-offered");
  });

  it("renders Compare with Mar'tu's version side by side without touching the code", () => {
    const html = renderToString(
      createElement(CompareView, {
        code: 'companion = Bomb Shell\nprint(companion)\n',
        solution: 'companion = "Bomb Shell"\nprint(companion)\n',
        retyping: false,
        onRetype: () => undefined,
        onLookAgain: () => undefined,
        onCopy: () => undefined,
        onClose: () => undefined,
      }),
    );
    expect(html).toContain('data-testid="compare-mine"');
    expect(html).toContain('data-testid="compare-theirs"');
    expect(html).toContain('data-testid="compare-retype"');
    expect(html).toContain('data-testid="compare-copy"');
    expect(html).not.toContain('data-testid="compare-copy-yes"');
    expect(html.match(/data-changed="true"/g)?.length).toBe(2);
    expect(html).toContain("(different)");
  });

  it("renders the small pieces on their own", () => {
    const predict = renderToString(
      createElement(PredictStep, {
        predict: unitOneStyle.predict!,
        editorCode: "print(1)\n",
        starter: unitOneStyle.starter,
        glossary: [],
        saved: undefined,
        onAnswer: () => undefined,
        onClose: () => undefined,
      }),
    );
    expect(predict).toContain('data-testid="predict-code"');
    expect(predict).toContain('data-testid="predict-choice-1"');
    const answeredEarlier = renderToString(
      createElement(PredictStep, {
        predict: unitOneStyle.predict!,
        editorCode: unitOneStyle.starter,
        starter: unitOneStyle.starter,
        glossary: [],
        saved: -1,
        onAnswer: () => undefined,
        onClose: () => undefined,
      }),
    );
    expect(answeredEarlier).toBe("");
    const chips = renderToString(
      createElement(NamesChips, { names: [], pick: "Zelda", prominent: false, onInsertName: () => undefined, onPick: () => undefined }),
    );
    expect(chips).toContain("Mar&#x27;tu&#x27;s pick");
    const tray = renderToString(createElement(SymbolTray, { onInsert: () => undefined, names: ["hero"] }));
    expect(tray).toContain('aria-label="Type double quote"');
    expect(tray).toContain('data-testid="tray-name-hero"');
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
