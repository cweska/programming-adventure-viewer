import { describe, expect, it } from "vitest";
import type { ExerciseProgress, GradeResult } from "../../lib/course/contracts";
import type { Checkpoint } from "../../lib/course/schema";
import {
  angleLabel,
  anotherWayOpen,
  applyRun,
  assembledCode,
  assemblesBySteps,
  checkpointHeading,
  crashAim,
  crashLineSwitchedOff,
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
  startTarget,
  stepAssemble,
  stdinBoxText,
  stepNoun,
  stripComment,
  stuckCheckpointId,
  titleFromId,
  usesInput,
} from "./exercise-logic";
import { cardSortMarks } from "./card-sort";

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
    // A SOLO item: the angles stay a Help rung (counted as Help), never a free Learn-pane button.
    expect(anotherWayOpen("full", angles, true)).toBe(false);
    expect(anotherWayOpen("full", angles, false)).toBe(true);
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

describe("crashAim: Help in a Broken spell moves past the slips already mended", () => {
  // Broken spell 2A: two steps name line 3 (the sign, then the text "15"), then a quiet bug.
  const spell2a = [
    { text: "Mend the sign on line 3 so `passed` asks whether `roll` is at least `needed`.", hints: ["a", "b"] },
    { text: "Line 3 compares a number with text. Mend the line that makes `needed`, so it holds a number.", hints: ["a", "b"] },
    { text: "`clock_is_red` prints `red`, not a yes/no answer.", hints: ["Line 6 has one `=`.", "b"] },
  ];
  // Broken spell 2B: no step names a line; the hints of the first one do.
  const spell2b = [
    { text: "Mend the line that asks whether `roll` is 20.", hints: ["Python's message names line 2.", "b"] },
    { text: "Mend the line that checks the first option.", hints: ["a", "b"] },
    { text: "Mend the clock chain.", hints: ["a", "b"] },
    { text: "Mend the roll so Python knows where `random` comes from.", hints: ["a", "b"] },
  ];

  it("aims at the next step that names the crash line after a run that got further", () => {
    const first = crashAim({ checkpoints: spell2a, crashLine: 3, signature: "3:SyntaxError", seen: [], previous: null, gotFurther: false, firstOpen: 0 });
    expect(first).toBe(0);
    const seen = [{ signature: "3:SyntaxError", step: first }];
    const next = crashAim({ checkpoints: spell2a, crashLine: 3, signature: "3:TypeError", seen, previous: seen[0], gotFurther: true, firstOpen: 0 });
    expect(next).toBe(1);
    // The sign broken again: back to step 1's Help.
    const all = [...seen, { signature: "3:TypeError", step: 1 }];
    expect(crashAim({ checkpoints: spell2a, crashLine: 3, signature: "3:SyntaxError", seen: all, previous: all[1], gotFurther: false, firstOpen: 0 })).toBe(0);
  });

  it("steps on one at a time when no step names a line, and holds still for the same slip typed another way", () => {
    let previous = { signature: "2:SyntaxError: a", step: crashAim({ checkpoints: spell2b, crashLine: 2, signature: "2:SyntaxError: a", seen: [], previous: null, gotFurther: false, firstOpen: 0 }) };
    expect(previous.step).toBe(0);
    const seen = [previous];
    for (const [line, want] of [
      [6, 1],
      [16, 2],
      [1, 3],
    ] as const) {
      const step = crashAim({ checkpoints: spell2b, crashLine: line, signature: `${line}:x`, seen, previous, gotFurther: true, firstOpen: 0 });
      expect(step).toBe(want);
      previous = { signature: `${line}:x`, step };
      seen.push(previous);
    }
    // A new message that is not further keeps the step.
    expect(crashAim({ checkpoints: spell2b, crashLine: 1, signature: "1:other", seen, previous, gotFurther: false, firstOpen: 0 })).toBe(3);
  });

  it("says only which line to mend when the steps name other lines, and keeps the old aim for a first crash", () => {
    const named = [{ text: "Mend line 3 so it shows `Steady`.", hints: ["a", "b"] }, { text: "Mend line 5 so it adds.", hints: ["a", "b"] }];
    const previous = { signature: "3:SyntaxError", step: 0 };
    expect(crashAim({ checkpoints: named, crashLine: 4, signature: "4:NameError", seen: [previous], previous, gotFurther: true, firstOpen: 0 })).toBeNull();
    expect(crashAim({ checkpoints: named, crashLine: 5, signature: "5:TypeError", seen: [previous], previous, gotFurther: true, firstOpen: 0 })).toBe(1);
    expect(crashAim({ checkpoints: named, crashLine: 4, signature: "4:x", seen: [], previous: null, gotFurther: false, firstOpen: 0 })).toBeNull();
    expect(crashAim({ checkpoints: spell2b, crashLine: 2, signature: "2:x", seen: [], previous: null, gotFurther: false, firstOpen: 2 })).toBe(2);
  });

  it("prefers the step whose Help names Python's error when several steps name the crash line", () => {
    // `=>` mended to a lone `=` (it runs), then to `>=`: the TypeError comes with no crash just before it.
    const withHints = [
      { text: spell2a[0].text, hints: ["Read Python's last line: `SyntaxError: invalid syntax`.", "b"] },
      { text: spell2a[1].text, hints: ["Read Python's last line: a `TypeError`.", "b"] },
      spell2a[2],
    ];
    const typeError = "TypeError: '>=' not supported between instances of 'int' and 'str'";
    expect(crashAim({ checkpoints: withHints, crashLine: 3, signature: `3:${typeError}`, seen: [], previous: null, gotFurther: false, firstOpen: 0, error: typeError })).toBe(1);
    expect(crashAim({ checkpoints: withHints, crashLine: 3, signature: "3:SyntaxError: invalid syntax", seen: [], previous: null, gotFurther: false, firstOpen: 0, error: "SyntaxError: invalid syntax" })).toBe(0);
    // No step's Help names the error: the first step that names the line, as before.
    expect(crashAim({ checkpoints: spell2a, crashLine: 3, signature: `3:${typeError}`, seen: [], previous: null, gotFurther: false, firstOpen: 0, error: typeError })).toBe(0);
  });
});

describe("crashLineSwitchedOff: a crash that is part of the task", () => {
  const solution = 'hero = "Bomb Shell"\n# print("Mana left: " + str(mana - mana_cost))\nbad_line = 4\n';
  it("is true when Mar'tu's version keeps the crash line switched off with #", () => {
    expect(crashLineSwitchedOff('hero = "Bomb Shell"\nprint("Mana left: " + str(mana - mana_cost))\n', 2, solution)).toBe(true);
    expect(crashLineSwitchedOff('hero = "Bomb Shell"\n  print("Mana left: " + str(mana - mana_cost))  \n', 2, solution)).toBe(true);
  });
  it("is false for any other line, an empty line, or no solution", () => {
    expect(crashLineSwitchedOff('hero = "Bomb Shell"\nprint(mana_cost)\n', 2, solution)).toBe(false);
    expect(crashLineSwitchedOff("\n\n", 2, solution)).toBe(false);
    expect(crashLineSwitchedOff('print("Mana left: " + str(mana - mana_cost))\n', 1, undefined)).toBe(false);
    expect(crashLineSwitchedOff('print("Mana left: " + str(mana - mana_cost))\n', null, solution)).toBe(false);
  });
});

describe("where Start me off goes before a click (startTarget)", () => {
  it("reads the place from the step's last hint, and the recipe from the step's own names", () => {
    expect(
      startTarget({
        text: "Now `step_west`, on your own.",
        hints: ["Look under `def step_west():`.", 'Write `scout.step("west")` in place of `pass`, four spaces in.'],
      }),
    ).toEqual({ line: "pass", how: "replace", near: ["step_west", "def", "scout", "step", "west", "pass"] });
    expect(
      startTarget({ text: "Hand back `total`.", hints: ["Look.", "Write `return total` on the line after `total = affinity * 2`, four spaces in."] }),
    ).toMatchObject({ line: "total = affinity * 2", how: "after" });
    expect(startTarget({ text: "x", hints: ["Look.", "Write `passed = roll >= needed` under the `# passed:` note."] })).toMatchObject({
      line: "# passed:",
      how: "after",
    });
    // Unit 5: "above `X`" puts the line over X; the first place the hint names wins.
    expect(
      startTarget({ text: "x", hints: ["Look.", 'Write `caster["mana"] = caster["mana"] - spell["mana_cost"]` in the `else`, above `print(caster["mana"])`.'] }),
    ).toMatchObject({ line: 'print(caster["mana"])', how: "before" });
    expect(startTarget({ text: "x", hints: ["Look.", "Write `print(lucky[3])` in place of `print(lucky[2])`."] })).toMatchObject({
      line: "print(lucky[2])",
      how: "replace",
    });
    // A hint that names no line (or a single hint): no place, so the end of the code, as before.
    expect(startTarget({ text: "x", hints: ["Look.", "Write `say_steady()` on a new line at the bottom."] })).toBeNull();
    expect(startTarget({ text: "x", hints: ["Write `x = 1` in place of `x = 0`."] })).toBeNull();
  });
});

describe("More structure for one step (stepAssemble)", () => {
  const exercise = {
    starter: "# 1. Make the list\n\n# 2. Print the last\n",
    solution: "# 1. Make the list\nwall = [1, 2]\n\n# 2. Print the last\nprint(wall[-1])\n",
    checkpoints: [{ id: "make" }, { id: "print" }],
    assemble: {
      lines: ["wall = [1, 2]", "print(wall[-1])"],
      distractors: ["wall = (1, 2)", "print(wall[2])", "wall.append(3)"],
      steps: ["# 1. Make the list\nwall = [1, 2]\n\n# 2. Print the last\n"],
    },
  };

  it("shuffles only the lines the step adds, with the distractors that start the same way", () => {
    const first = stepAssemble(exercise, 0);
    expect(first?.lines).toEqual(["wall = [1, 2]"]);
    expect(first?.distractors).toEqual(["wall = (1, 2)"]);
    const second = stepAssemble(exercise, 1);
    expect(second?.lines).toEqual(["print(wall[-1])"]);
    expect(second?.distractors).toEqual(["print(wall[2])"]);
  });

  it("keeps the rest of the program in place: the right pieces in the gaps give Mar'tu's version after the step", () => {
    const second = stepAssemble(exercise, 1)!;
    expect(second.fill(second.lines)).toBe(exercise.solution);
    expect(second.context.some((line) => line.kind === "gap")).toBe(true);
    // The lines around the gap stay in place, read-only; lines further off fold into "…".
    expect(second.context.map((line) => (line.kind === "fixed" ? line.text : line.kind))).toEqual(["more", "", "# 2. Print the last", "gap"]);
    // Too few pieces leave the gap out; extra pieces go after the last gap.
    expect(second.fill([])).toBe("# 1. Make the list\nwall = [1, 2]\n\n# 2. Print the last\n");
    expect(second.fill(["print(wall[-1])", "print(wall)"])).toBe(`${exercise.solution}print(wall)\n`);
  });

  it("is only for projects, challenges and long boards, never for a SOLO or an exercise with no partials", () => {
    expect(assemblesBySteps("project", exercise.assemble)).toBe(true);
    expect(assemblesBySteps("challenge", exercise.assemble)).toBe(true);
    expect(assemblesBySteps("lesson", exercise.assemble)).toBe(false);
    expect(assemblesBySteps("lesson", { ...exercise.assemble, lines: Array.from({ length: 13 }, (_, i) => `x${i} = ${i}`) })).toBe(true);
    expect(assemblesBySteps("project", { lines: exercise.assemble.lines, distractors: [] })).toBe(false);
    expect(stepAssemble({ ...exercise, solo: true }, 1)).toBeNull();
    expect(stepAssemble({ ...exercise, assemble: { ...exercise.assemble, steps: undefined } }, 1)).toBeNull();
  });
});

describe("the card sort (cardSortMarks)", () => {
  const sort = { groups: ["these exact letters", "look inside the box"], cards: [{ text: "mana = 26", group: 1 }, { text: '"mana"', group: 0 }], explain: "x" };
  it("marks each card right only when it is in its own group", () => {
    expect(cardSortMarks(sort, [1, 0])).toEqual([true, true]);
    expect(cardSortMarks(sort, [0, 0])).toEqual([false, true]);
    expect(cardSortMarks(sort, [null, null])).toEqual([false, false]);
  });
});
