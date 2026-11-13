import { describe, expect, it } from "vitest";
import type { ExerciseProgress, GradeResult } from "../../lib/course/contracts";
import type { Checkpoint } from "../../lib/course/schema";
import {
  angleLabel,
  anotherWayOpen,
  applyRun,
  assembledCode,
  checkpointHeading,
  effectiveSupport,
  exerciseIndexFromHash,
  hashForExercise,
  hintButtonLabel,
  hintsOpen,
  isBlankOrStarter,
  nextFailStreak,
  parseStdinBox,
  revealNextRung,
  rungsShown,
  runOutcome,
  solutionUnlocked,
  stdinBoxText,
  stepNoun,
  stripComment,
  stuckCheckpointId,
  titleFromId,
  usesInput,
} from "./exercise-logic";

const empty = (): ExerciseProgress => ({ passed: [], done: false, hintsUsed: {}, failedRuns: 0 });

function checkpoint(id: string): Checkpoint {
  return { id, text: `Do ${id}.`, hints: ["one", "two"], checks: [{ name: "c", code: "assert True" }] };
}

const checkpoints = [checkpoint("a"), checkpoint("b"), checkpoint("c")];

function grade(passed: boolean[], crashed = false): GradeResult {
  const grades = checkpoints.map((cp, index) => ({ id: cp.id, passed: !crashed && passed[index], message: "msg" }));
  const firstFailing = grades.findIndex((g) => !g.passed);
  return {
    crashed,
    checkpoints: grades,
    firstFailing: firstFailing < 0 ? null : firstFailing,
    allPassed: firstFailing < 0,
  };
}

describe("stepper hash", () => {
  const ids = ["read-the-chalk", "ask-the-traveler", "barrier-report"];

  it("finds the exercise in the hash", () => {
    expect(exerciseIndexFromHash("#ask-the-traveler", ids)).toBe(1);
    expect(exerciseIndexFromHash("barrier-report", ids)).toBe(2);
    expect(exerciseIndexFromHash(" #barrier-report ", ids)).toBe(2);
  });

  it("falls back to the first exercise", () => {
    expect(exerciseIndexFromHash("", ids)).toBe(0);
    expect(exerciseIndexFromHash("#nope", ids)).toBe(0);
    expect(exerciseIndexFromHash("#%E0%A4%A", ids)).toBe(0);
  });

  it("round-trips through hashForExercise", () => {
    for (const [index, id] of ids.entries()) expect(exerciseIndexFromHash(hashForExercise(id), ids)).toBe(index);
    expect(hashForExercise("x")).toBe("#x");
  });
});

describe("support levels", () => {
  it("Quick Checks never give help", () => {
    expect(effectiveSupport("testout", "full")).toBe("none");
    expect(effectiveSupport("lesson", "light")).toBe("light");
    expect(effectiveSupport("lesson", undefined)).toBe("full");
  });

  it("opens hints by support", () => {
    expect(hintsOpen("full", false)).toBe(true);
    expect(hintsOpen("light", false)).toBe(false);
    expect(hintsOpen("light", true)).toBe(true);
    expect(hintsOpen("none", true)).toBe(false);
  });

  it("offers another way only with full support", () => {
    const angles = [{ angle: "analogy", text: "x" }];
    expect(anotherWayOpen("full", angles)).toBe(true);
    expect(anotherWayOpen("full", [])).toBe(false);
    expect(anotherWayOpen("light", angles)).toBe(false);
    expect(anotherWayOpen("none", angles)).toBe(false);
  });
});

describe("solution gating", () => {
  const gate = { support: "full" as const, activeMs: 0, failedRuns: 0, solutionAfterMinutes: 5, solutionAfterFailedRuns: 4 };

  it("stays locked at first", () => {
    expect(solutionUnlocked(gate)).toBe(false);
    expect(solutionUnlocked({ ...gate, activeMs: 4 * 60_000 + 59_000, failedRuns: 3 })).toBe(false);
  });

  it("opens after the minutes of active time", () => {
    expect(solutionUnlocked({ ...gate, activeMs: 5 * 60_000 })).toBe(true);
  });

  it("opens after the failed runs", () => {
    expect(solutionUnlocked({ ...gate, failedRuns: 4 })).toBe(true);
  });

  it("works for light support but never for none", () => {
    expect(solutionUnlocked({ ...gate, support: "light", failedRuns: 9 })).toBe(true);
    expect(solutionUnlocked({ ...gate, support: "none", failedRuns: 99, activeMs: 1e9 })).toBe(false);
  });
});

describe("hint ladder", () => {
  it("opens one rung at a time and stops at the top", () => {
    let used: Record<string, number> = {};
    expect(rungsShown(used, "a", 3)).toBe(0);
    used = revealNextRung(used, "a", 3);
    expect(rungsShown(used, "a", 3)).toBe(1);
    used = revealNextRung(revealNextRung(revealNextRung(used, "a", 3), "a", 3), "a", 3);
    expect(used.a).toBe(3);
    expect(rungsShown(used, "b", 3)).toBe(0);
  });

  it("keeps other checkpoints' counts and clamps saved values", () => {
    const used = revealNextRung({ b: 2 }, "a", 2);
    expect(used).toEqual({ a: 1, b: 2 });
    expect(rungsShown({ a: 9 }, "a", 2)).toBe(2);
    expect(rungsShown(undefined, "a", 2)).toBe(0);
  });

  it("labels the button with the rung count", () => {
    expect(hintButtonLabel(0, 3)).toBe("Hint (1 of 3)");
    expect(hintButtonLabel(1, 3)).toBe("Next hint (2 of 3)");
    expect(hintButtonLabel(3, 3)).toBe("All 3 hints shown");
  });
});

describe("runs and progress", () => {
  it("unions passed ids across runs and marks done only when all pass in one run", () => {
    let progress = empty();
    let outcome = runOutcome(grade([true, false, false]), progress.passed);
    expect(outcome).toMatchObject({ passedNow: ["a"], newlyPassed: ["a"], allPassed: false, failed: false });
    progress = applyRun(progress, outcome, { code: "x" });
    expect(progress).toMatchObject({ passed: ["a"], done: false, failedRuns: 0, code: "x" });

    // Breaks a, passes b and c: progress, but not done.
    outcome = runOutcome(grade([false, true, true]), progress.passed);
    progress = applyRun(progress, outcome);
    expect(progress.passed).toEqual(["a", "b", "c"]);
    expect(progress.done).toBe(false);
    expect(progress.code).toBe("x");

    outcome = runOutcome(grade([true, true, true]), progress.passed);
    expect(outcome.failed).toBe(false);
    progress = applyRun(progress, outcome);
    expect(progress.done).toBe(true);
  });

  it("counts a run with no new progress as failed (crashes too)", () => {
    let progress = applyRun(empty(), runOutcome(grade([true, false, false]), []));
    const again = runOutcome(grade([true, false, false]), progress.passed);
    expect(again.failed).toBe(true);
    progress = applyRun(progress, again);
    progress = applyRun(progress, runOutcome(grade([], true), progress.passed));
    expect(progress.failedRuns).toBe(2);
  });

  it("stays done once done", () => {
    const done = { ...empty(), done: true, passed: ["a", "b", "c"] };
    expect(applyRun(done, runOutcome(grade([false, false, false]), done.passed)).done).toBe(true);
  });

  it("records the side quest only once the exercise is done", () => {
    const all = runOutcome(grade([true, true, true]), []);
    expect(applyRun(empty(), all, { bonusPassed: true }).bonusDone).toBe(true);
    const partial = runOutcome(grade([true, false, true]), []);
    expect(applyRun(empty(), partial, { bonusPassed: true }).bonusDone).toBeUndefined();
    const doneBefore = { ...empty(), done: true, passed: ["a", "b", "c"] };
    expect(applyRun(doneBefore, partial, { bonusPassed: true }).bonusDone).toBe(true);
    expect(applyRun(doneBefore, partial, { bonusPassed: false }).bonusDone).toBeUndefined();
  });

  it("finds the checkpoint the student is stuck on", () => {
    expect(stuckCheckpointId(checkpoints, grade([true, false, false]), [])).toBe("b");
    expect(stuckCheckpointId(checkpoints, grade([true, true, true]), [])).toBeNull();
    expect(stuckCheckpointId(checkpoints, grade([], true), ["a"])).toBe("b");
    expect(stuckCheckpointId(checkpoints, grade([], true), ["a", "b", "c"])).toBe("a");
  });
});

describe("misses in a row", () => {
  it("counts misses in a row on the same checkpoint", () => {
    let streak = nextFailStreak({ checkpointId: null, count: 0 }, "b");
    expect(streak).toEqual({ checkpointId: "b", count: 1 });
    streak = nextFailStreak(streak, "b");
    expect(streak.count).toBe(2);
    expect(nextFailStreak(streak, "c")).toEqual({ checkpointId: "c", count: 1 });
    expect(nextFailStreak(streak, null)).toEqual({ checkpointId: null, count: 0 });
  });
});

describe("code helpers", () => {
  it("strips comments but not # inside strings", () => {
    expect(stripComment("x = 1  # set x")).toBe("x = 1  ");
    expect(stripComment('print("# not a comment")')).toBe('print("# not a comment")');
    expect(stripComment("print('it\\'s # here') # gone")).toBe("print('it\\'s # here') ");
  });

  it("spots input() calls outside comments", () => {
    expect(usesInput('name = input("Who? ")')).toBe(true);
    expect(usesInput("x = input ()")).toBe(true);
    expect(usesInput("# input() later")).toBe(false);
    expect(usesInput('print("no")')).toBe(false);
    expect(usesInput("my_input(3)")).toBe(false);
    expect(usesInput("self.input(3)")).toBe(false);
  });

  it("knows a blank or untouched editor", () => {
    const starter = "# 1. Make caster\n# 2. Print it\n";
    expect(isBlankOrStarter("", starter)).toBe(true);
    expect(isBlankOrStarter("   \n\n", starter)).toBe(true);
    expect(isBlankOrStarter("# my own note\n", starter)).toBe(true);
    expect(isBlankOrStarter(starter, starter)).toBe(true);
    expect(isBlankOrStarter('name = input("Who? ")\n# greet', 'name = input("Who? ")\n# greet\n')).toBe(true);
    expect(isBlankOrStarter('caster = "Gearshift"\n', starter)).toBe(false);
  });

  it("assembles exactly the chosen lines", () => {
    const lines = ['caster = "Gearshift"', "print(caster)"];
    expect(assembledCode(lines)).toBe('caster = "Gearshift"\nprint(caster)\n');
    expect(assembledCode([])).toBe("");
  });

  it("reads the input box one answer per line", () => {
    expect(parseStdinBox("Lucky\n")).toEqual(["Lucky"]);
    expect(parseStdinBox("a\r\n\nb\n\n")).toEqual(["a", "", "b"]);
    expect(parseStdinBox("")).toEqual([]);
    expect(stdinBoxText(["a", "b"])).toBe("a\nb");
    expect(stdinBoxText(undefined)).toBe("");
    expect(parseStdinBox(stdinBoxText(["x", "y"]))).toEqual(["x", "y"]);
  });

  it("never drops an empty answer the program needs (Press Enter)", () => {
    expect(parseStdinBox("", 1)).toEqual([""]);
    expect(parseStdinBox("Mira\n", 2)).toEqual(["Mira", ""]);
    expect(parseStdinBox("Mira", 2)).toEqual(["Mira", ""]);
    expect(parseStdinBox("Mira\n\n\n", 1)).toEqual(["Mira"]);
  });
});

describe("words", () => {
  it("labels another-way angles", () => {
    expect(angleLabel({ angle: "analogy", label: "Think of jars" })).toBe("Think of jars");
    expect(angleLabel({ angle: "step by step" })).toBe("Step by step");
    expect(angleLabel({ angle: "analogy" })).toBe("Compare it to something");
    expect(angleLabel({ angle: "cooking" })).toBe("Cooking");
  });

  it("names steps and headings by item kind", () => {
    expect(stepNoun("lesson")).toBe("Step");
    expect(stepNoun("project")).toBe("Task");
    expect(stepNoun("challenge")).toBe("Task");
    expect(checkpointHeading("lesson", true)).toBe("Run it and read the output");
    expect(checkpointHeading("lesson", false)).toBe("Your steps");
    expect(checkpointHeading("project", false)).toBe("Your tasks");
  });

  it("turns ids into titles", () => {
    expect(titleFromId("leylines-awaken")).toBe("Leylines Awaken");
    expect(titleFromId("program-dialogue-prompt")).toBe("Program Dialogue Prompt");
  });
});
