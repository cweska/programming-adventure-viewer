import { describe, expect, it } from "vitest";
import {
  angleLabel,
  answersFromBox,
  codeHasStart,
  compareLines,
  countInputCalls,
  countsAsAttempt,
  crashTarget,
  firstParagraph,
  helpOffer,
  helpOfferLine,
  helpRungs,
  helpState,
  insideString,
  isDebugExercise,
  namesALine,
  NUDGE_AFTER_MISSES,
  NUDGE_IDLE_MS,
  NUDGE_NO_PROGRESS_MS,
  pickInsertion,
  pickIsNote,
  revealNextRung,
  RUNG_PACE_MS,
  rungInStack,
  rungPaced,
  soloPassLine,
  soloUnaided,
  solutionUnlocked,
  startOfLine,
} from "./exercise-logic";
import { coursePreset as presetOf } from "../../lib/course/progress";

const threeHints = { hints: ["start", "look", "teach"] };

describe("presets", () => {
  it("defaults to Show me more and reads the legacy light switch as Keep it short", () => {
    expect(presetOf(undefined)).toBe("more");
    expect(presetOf({})).toBe("more");
    expect(presetOf({ light: true })).toBe("short");
    expect(presetOf({ light: false })).toBe("more");
    expect(presetOf({ preset: "short" })).toBe("short");
    // An explicit preset wins over the legacy switch.
    expect(presetOf({ preset: "more", light: true })).toBe("more");
  });
});

describe("the Help rungs", () => {
  const full = { anotherWayCount: 3, hasAssemble: true, solo: false };

  it("climbs Start me off, Where to look, Another way, Teach me, More structure, Show me how, Compare", () => {
    const rungs = helpRungs({ hints: ["point", "teach", "teach more", "Write `caster = \"Gearshift\"`."] }, full);
    expect(rungs.map((rung) => rung.kind)).toEqual(["start", "point", "another", "teach", "teach", "structure", "how", "show"]);
    expect(rungs.map((rung) => rung.label)).toEqual([
      "Start me off",
      "Where to look",
      "Another way",
      "Teach me",
      "Teach me more",
      "More structure",
      "Show me how",
      "Compare with Mar'tu's version",
    ]);
    expect(rungs[0].start).toBe("caster =");
    // Authored hints are point -> teach -> show: the nearly-the-answer hint comes after every gentler rung.
    expect(rungs.filter((rung) => rung.hint !== undefined).map((rung) => rung.hint)).toEqual([0, 1, 2, 3]);
  });

  it("skips what the exercise does not have", () => {
    const rungs = helpRungs({ hints: ["a", "b"] }, { anotherWayCount: 0, hasAssemble: false, solo: false });
    expect(rungs.map((rung) => rung.kind)).toEqual(["point", "how", "show"]);
    const twoHints = helpRungs({ hints: ["Numbers need no quotes.", "Write `mana = 20` on its own line."] }, full);
    expect(twoHints.map((rung) => rung.kind)).toEqual(["start", "point", "another", "structure", "how", "show"]);
  });

  it("starts a SOLO exercise at Where to look", () => {
    const rungs = helpRungs({ hints: ["a", "b", "Try `print(name)`."] }, { ...full, solo: true });
    expect(rungs[0].kind).toBe("point");
    expect(rungs.some((rung) => rung.kind === "start")).toBe(false);
    expect(rungs.at(-1)?.kind).toBe("show");
  });

  it("Start me off gives only the first tokens of the step's line, never the whole answer", () => {
    expect(startOfLine(["a", "Write `caster = \"Gearshift\"` on the first line."])).toBe("caster =");
    expect(startOfLine(["a", "b", 'Try `print("Welcome to the cabin, " + name)`.'])).toBe("print(");
    expect(startOfLine(["a", "Then `print(leader + \" has \" + str(max_mana) + \" mana.\")`."])).toBe("print(");
    expect(startOfLine(["a", "Add `total += 5`."])).toBe("total +=");
    expect(startOfLine(["a", "Use `name = input(\"Who? \")`."])).toBe("name =");
    // Nothing safe to give: no code, no ( or =, a comparison, or only one hint.
    expect(startOfLine(["a", "Just press Run and look at the console."])).toBeNull();
    expect(startOfLine(["a", "Use `mana`."])).toBeNull();
    expect(startOfLine(["a", "Check `mana == 20`."])).toBeNull();
    expect(startOfLine(["a", "Check `mana >= 20`."])).toBeNull();
    expect(startOfLine(["a", "Write `(1 + 2)`."])).toBeNull();
    expect(startOfLine(["Write `mana = 20`."])).toBeNull();
    expect(startOfLine(undefined)).toBeNull();
    // A hint that shows an example with other names gives no start: Mar'tu's version must use it.
    expect(startOfLine(["a", "`snack = \"glug\"` makes a box."], 'companion = "Bomb Shell"\n')).toBeNull();
    expect(startOfLine(["a", "Write `mana = 20`."], "caster = 'G'\nmana=20\n")).toBe("mana =");
    // Lists: a bare `print(` that reads a list runs on to its bracket, and a `(` inside [ ] cuts at the bracket.
    const wall = "chalk_wall = [48, 37]\nprint(chalk_wall[len(chalk_wall) - 1])\n";
    expect(startOfLine(["a", "Write `print(chalk_wall[len(chalk_wall) - 1])` under the `# 1.` note."], wall)).toBe("print(chalk_wall[");
    expect(startOfLine(["a", "Write `return wall[len(wall) - 1]` in place of `return 0`."], "    return wall[-1]\n")).toBe("return wall[");
    // Not in Mar'tu's version: the plain start, as before. Other lines keep their start.
    expect(startOfLine(["a", "Write `print(colors[1])`."], "print(chalk_wall[0])\n")).toBe("print(");
    expect(startOfLine(["a", "Write `log[0][1] = log[0][1] + 2` under task 3."], "log[0][1] = log[0][1] + 2\n")).toBe("log[0][1] =");
    expect(startOfLine(["a", "Write `print(len(chalk_wall))`."], "print(len(chalk_wall))\n")).toBe("print(");
  });

  it("knows what is open and what comes next", () => {
    const rungs = helpRungs(threeHints, full);
    let state = helpState(rungs, 0, false);
    expect(state.open).toEqual([]);
    expect(state.next?.kind).toBe("point");
    expect(state.nextLocked).toBe(false);
    expect(state.left).toBe(rungs.length - 1);

    state = helpState(rungs, rungs.length - 1, false);
    expect(state.next?.kind).toBe("show");
    expect(state.nextLocked).toBe(true);
    expect(state.left).toBe(0);

    state = helpState(rungs, rungs.length - 1, true);
    expect(state.nextLocked).toBe(false);
    expect(state.left).toBe(1);

    state = helpState(rungs, 99, true);
    expect(state.open).toHaveLength(rungs.length);
    expect(state.next).toBeNull();
    expect(state.left).toBe(0);
    expect(helpState(rungs, -3, true).open).toEqual([]);
  });

  it("Keep it short climbs Where to look, Teach me, Show me how and Compare; the rest wait under More options", () => {
    const rungs = helpRungs({ hints: ["point", "teach", "Write `caster = \"Gearshift\"`."] }, full);
    expect(rungs.map((rung) => rung.kind)).toEqual(["start", "point", "another", "teach", "structure", "how", "show"]);
    let state = helpState(rungs, 0, false, { preset: "short" });
    expect(state.next?.kind).toBe("point");
    expect(state.nextIndex).toBe(1);
    expect(state.extras.map((rung) => rung.kind)).toEqual(["start", "another", "structure"]);
    expect(state.left).toBe(3);
    // Opening Where to look saves 2 (Start me off is stepped over); the next press opens Teach me.
    state = helpState(rungs, 2, false, { preset: "short" });
    expect(state.open.map((rung) => rung.kind)).toEqual(["point"]);
    expect(state.opened).toBe(2);
    expect(state.next?.kind).toBe("teach");
    state = helpState(rungs, 4, false, { preset: "short" });
    expect(state.next?.kind).toBe("how");
    state = helpState(rungs, 6, false, { preset: "short" });
    expect(state.next?.kind).toBe("show");
    expect(state.nextLocked).toBe(true);
    // Show me more keeps every rung in the stack and nothing under More options.
    expect(helpState(rungs, 0, false).extras).toEqual([]);
    expect(rungInStack("start", "more")).toBe(true);
    expect(rungInStack("start", "short")).toBe(false);
    expect(rungInStack("how", "short")).toBe(true);
    // The saved count runs over the whole list: switching presets never opens Mar'tu's version early.
    expect(helpState(rungs, 5, true, { preset: "short" }).open.map((rung) => rung.kind)).toEqual(["point", "teach"]);
  });

  it("steps over Start me off when it has nothing to give (the line is there, or right after a crash)", () => {
    const rungs = helpRungs({ hints: ["point", "teach", "Write `caster = \"Gearshift\"`."] }, full);
    const skipStart = (rung: { kind: string }) => rung.kind === "start";
    const state = helpState(rungs, 0, false, { skip: skipStart });
    expect(state.next?.kind).toBe("point");
    expect(state.nextIndex).toBe(1);
    expect(state.left).toBe(rungs.length - 2);
    expect(revealNextRung({}, "make-caster", rungs.length, state.nextIndex + 1)).toEqual({ "make-caster": 2 });
    // Never closes rungs, never past the top.
    expect(revealNextRung({ a: 4 }, "a", 7, 2)).toEqual({ a: 4 });
    expect(revealNextRung({ a: 4 }, "a", 7, 99)).toEqual({ a: 7 });
    expect(revealNextRung({ a: 4 }, "a", 7)).toEqual({ a: 5 });
    expect(codeHasStart('# 1. Make caster\ncaster="Gearshift"\n', "caster =")).toBe(true);
    expect(codeHasStart("# caster = here\n", "caster =")).toBe(false);
    expect(codeHasStart('print("Welcome to the cabin, Lucky")\n', "print(")).toBe(true);
    expect(codeHasStart('name = input("Who? ")\n', "print(")).toBe(false);
    expect(codeHasStart("anything\n", "")).toBe(false);
    // Mar'tu's other finished lines (the starter's, an earlier step's) are not this step's line begun.
    const step = { solution: "w = [1, 2]\nprint(len(w))\nprint(w[0])\nprint(w[-1])\n", line: "print(w[-1])" };
    expect(codeHasStart("w = [1, 2]\nprint(len(w))\n", "print(", step)).toBe(false);
    expect(codeHasStart("w = [1, 2]\nprint(len(w))\nprint(w[0])\n", "print(w[", step)).toBe(false);
    expect(codeHasStart("w = [1, 2]\nprint(w[0])\nprint(w[\n", "print(w[", step)).toBe(true);
    expect(codeHasStart("w = [1, 2]\nprint(w[0])\nprint(w[-1])\n", "print(w[", step)).toBe(true);
    // A Broken spell's line is not in Mar'tu's version: it is still the line to mend.
    expect(codeHasStart("print(Steady)\n", "print(", { solution: 'print("Steady")\n', line: 'print("Steady")' })).toBe(true);
  });

  it("paces rungs: a Run or a few seconds opens the next one", () => {
    expect(rungPaced(null, false, 1_000)).toBe(false);
    expect(rungPaced(1_000, false, 1_000 + RUNG_PACE_MS - 1)).toBe(true);
    expect(rungPaced(1_000, false, 1_000 + RUNG_PACE_MS)).toBe(false);
    expect(rungPaced(1_000, true, 1_001)).toBe(false);
  });
});

describe("Help after a crash", () => {
  const brokenSpell = [
    { text: "Mend line 1 so it shows `Shield up.`" },
    { text: "Mend line 2 so it shows `Barrier's holding.`" },
    { text: "Mend line 3 so it shows `Steady`." },
  ];

  it("aims at the step that names the crash line, never at step 1 under \"Mend line 3 first.\"", () => {
    expect(crashTarget(brokenSpell, 3)).toBe(2);
    expect(crashTarget(brokenSpell, 1)).toBe(0);
    expect(crashTarget(brokenSpell, 5)).toBe(-1);
    expect(crashTarget(brokenSpell, null)).toBe(-1);
    // "line 1" is not "line 12".
    expect(crashTarget([{ text: "Mend line 12." }, { text: "Mend line 1." }], 1)).toBe(1);
    expect(namesALine("Line 2 is Lucky's secret.")).toBe(true);
    expect(namesALine("Print a line that has `_`, `-` and `=` in it.")).toBe(false);
  });

  it("knows a debugging exercise by its \"Mend ...\" steps (it gets the \"Python got further\" line)", () => {
    expect(isDebugExercise({ checkpoints: brokenSpell })).toBe(true);
    expect(isDebugExercise({ checkpoints: [{ text: "Make `hero` a box." }, { text: "Mend the `if` line." }] })).toBe(true);
    expect(isDebugExercise({ checkpoints: [{ text: "Make `hero` a box that holds `\"Lucky\"`." }] })).toBe(false);
    // "amend" or "mended" in other words is not the debugging verb.
    expect(isDebugExercise({ checkpoints: [{ text: "Print the amended total." }] })).toBe(false);
  });
});

describe("proactive Help offers", () => {
  const quiet = {
    preset: "more" as const,
    helpAvailable: true,
    done: false,
    dismissed: false,
    rungsLeft: 3,
    missesInARow: 0,
    msSinceProgress: 0,
    idleMs: null,
  };

  it("offers after 3 misses on a step, 4 minutes without progress, or 90 seconds idle (also before any Run)", () => {
    expect(helpOffer(quiet)).toBeNull();
    expect(helpOffer({ ...quiet, missesInARow: NUDGE_AFTER_MISSES - 1 })).toBeNull();
    expect(helpOffer({ ...quiet, missesInARow: NUDGE_AFTER_MISSES })).toBe("misses");
    expect(helpOffer({ ...quiet, msSinceProgress: NUDGE_NO_PROGRESS_MS })).toBe("time");
    expect(helpOffer({ ...quiet, idleMs: NUDGE_IDLE_MS - 1 })).toBeNull();
    expect(helpOffer({ ...quiet, idleMs: NUDGE_IDLE_MS })).toBe("idle");
    expect(NUDGE_AFTER_MISSES).toBe(3);
    expect(NUDGE_NO_PROGRESS_MS).toBe(240_000);
    expect(NUDGE_IDLE_MS).toBe(90_000);
  });

  it("under Keep it short, offers only after repeated misses (curriculum §2.3)", () => {
    expect(helpOffer({ ...quiet, preset: "short", missesInARow: NUDGE_AFTER_MISSES })).toBe("misses");
    expect(helpOffer({ ...quiet, preset: "short", msSinceProgress: NUDGE_NO_PROGRESS_MS })).toBeNull();
    expect(helpOffer({ ...quiet, preset: "short", idleMs: NUDGE_IDLE_MS })).toBeNull();
  });

  it("stays quiet without Help, when done, dismissed, or with nothing left", () => {
    const ready = { ...quiet, missesInARow: 5 };
    expect(helpOffer({ ...ready, helpAvailable: false })).toBeNull();
    expect(helpOffer({ ...ready, done: true })).toBeNull();
    expect(helpOffer({ ...ready, dismissed: true })).toBeNull();
    expect(helpOffer({ ...ready, rungsLeft: 0 })).toBeNull();
  });

  it("says one kind line, and \"read the last line\" only after a crash (there is an error message to read)", () => {
    expect(helpOfferLine("misses", true)).toContain("Read the last line first");
    expect(helpOfferLine("misses")).not.toContain("last line");
    expect(helpOfferLine("misses")).toContain("Steady, now. Want a nudge?");
    expect(helpOfferLine("time")).toMatch(/nudge/);
    expect(helpOfferLine("idle")).toMatch(/nudge/);
  });
});

describe("Mar'tu's version: what counts as a try", () => {
  const starter = "# 1. Make caster\n";

  it("does not count untouched starter code or the same code again", () => {
    expect(countsAsAttempt(starter, starter, null)).toBe(false);
    expect(countsAsAttempt(starter, starter, starter)).toBe(false);
    expect(countsAsAttempt("caster = x\n", starter, null)).toBe(true);
    expect(countsAsAttempt("caster = x\n", starter, "caster = x\n")).toBe(false);
    expect(countsAsAttempt("caster = y\n", starter, "caster = x\n")).toBe(true);
    expect(countsAsAttempt("", starter, "caster = x\n")).toBe(false);
  });

  it("counts a rerun after a Help rung was opened", () => {
    expect(countsAsAttempt("caster = x\n", starter, "caster = x\n", true)).toBe(true);
    expect(countsAsAttempt('print("hi")\n', 'print("hi")\n', null, true)).toBe(true);
    // A blank editor is never a try.
    expect(countsAsAttempt("  \n", starter, null, true)).toBe(false);
  });

  it("four untouched runs never open Mar'tu's version", () => {
    let failedRuns = 0;
    let last: string | null = null;
    for (let run = 0; run < 4; run += 1) {
      if (countsAsAttempt(starter, starter, last)) failedRuns += 1;
      last = starter;
    }
    const gate = { support: "full" as const, activeMs: 0, failedRuns, solutionAfterMinutes: 5, solutionAfterFailedRuns: 4 };
    expect(solutionUnlocked(gate)).toBe(false);
  });
});

describe("compare lines", () => {
  it("marks the lines that differ on each side", () => {
    const mine = 'caster = Gearshift\nmana = 20\nprint(caster)\n';
    const theirs = 'caster = "Gearshift"\nmana = 20\nprint(caster + " has " + str(mana) + " mana.")\n';
    const diff = compareLines(mine, theirs);
    expect(diff.mine.map((line) => line.changed)).toEqual([true, false, true]);
    expect(diff.theirs.map((line) => line.changed)).toEqual([true, false, true]);
    expect(diff.theirs[0].text).toBe('caster = "Gearshift"');
  });

  it("handles missing and extra lines, trailing spaces and empty code", () => {
    const diff = compareLines("a = 1   \n\n\n", "a = 1\nb = 2\n");
    expect(diff.mine).toEqual([{ text: "a = 1", changed: false }]);
    expect(diff.theirs).toEqual([
      { text: "a = 1", changed: false },
      { text: "b = 2", changed: true },
    ]);
    const empty = compareLines("", "x = 1\n");
    expect(empty.mine).toEqual([]);
    expect(empty.theirs[0].changed).toBe(true);
    expect(compareLines("x\ny\n", "x\ny\n").theirs.every((line) => !line.changed)).toBe(true);
  });
});

describe("Mar'tu's pick", () => {
  it("adds quotes unless the cursor is inside a string", () => {
    expect(pickInsertion("Zelda", "hero = ")).toBe('"Zelda"');
    expect(pickInsertion("Zelda", 'hero = "')).toBe("Zelda");
    expect(pickInsertion("Zelda", "hero = 'Ze")).toBe("Zelda");
    expect(pickInsertion("Zelda", 'print("a" + ')).toBe('"Zelda"');
    expect(pickInsertion("Zelda", "# a note with a \" quote ")).toBe('"Zelda"');
  });

  it("keeps numbers, quotes and multi-line picks usable", () => {
    expect(pickInsertion("18", "mana = ")).toBe("18");
    expect(pickInsertion('the "Brave"', "x = ")).toBe("'the \"Brave\"'");
    expect(pickInsertion("a\nb", "")).toBe("a\nb");
  });

  it("in a task that only prints, puts a pick on a line of its own as a print line", () => {
    const printOnly = { printOnly: true, lineAfter: "" };
    // keyboard-symbols: the empty line under the note.
    expect(pickInsertion("_ - = are side by side.", "", printOnly)).toBe('print("_ - = are side by side.")');
    // your-own-words: the cursor at the end of the starter line gets a print line under it.
    expect(pickInsertion("Steady, now.", 'print("Write Oogrish\'s words here")', printOnly)).toBe('\nprint("Steady, now.")');
    // Between the quotes it is still just the words; with code after the cursor it is the quoted words.
    expect(pickInsertion("Steady, now.", 'print("', { printOnly: true, lineAfter: '")' })).toBe("Steady, now.");
    expect(pickInsertion("Steady, now.", "", { printOnly: true, lineAfter: "print()" })).toBe('"Steady, now."');
    // Tasks that make boxes keep the plain value.
    expect(pickInsertion("Zelda", "", { lineAfter: "" })).toBe('"Zelda"');
  });

  it("puts a pick that is a # note in as it is, never in quotes", () => {
    expect(pickIsNote("# Night watch at the cabin.")).toBe(true);
    expect(pickIsNote("Steady, now.")).toBe(false);
    expect(pickInsertion("# Night watch at the cabin.", "")).toBe("# Night watch at the cabin.");
    expect(pickInsertion("  # Night watch at the cabin.", 'print("')).toBe("# Night watch at the cabin.");
  });

  it("uses a pick written as a quoted literal as it is", () => {
    expect(pickInsertion('"Welcome to the cabin, "', "print(")).toBe('"Welcome to the cabin, "');
    expect(pickInsertion('"Welcome to the cabin, "', 'print("')).toBe("Welcome to the cabin, ");
    expect(pickInsertion("'Zelda'", "hero = ")).toBe("'Zelda'");
  });

  it("reads open strings on a line", () => {
    expect(insideString('x = "abc')).toBe(true);
    expect(insideString('x = "abc"')).toBe(false);
    expect(insideString('x = "it\\"s')).toBe(true);
    expect(insideString("")).toBe(false);
  });
});

describe("Keep it short: the first paragraph", () => {
  it("returns the first line and whether more follows", () => {
    expect(firstParagraph("One.\nTwo.")).toEqual({ first: "One.", more: true });
    expect(firstParagraph("\n\nOnly.\n\n")).toEqual({ first: "Only.", more: false });
    expect(firstParagraph("")).toEqual({ first: "", more: false });
  });

  it("keeps a leading code block whole", () => {
    const text = "```\n  companion\n+---+\n```\nAfter.";
    expect(firstParagraph(text)).toEqual({ first: "```\n  companion\n+---+\n```", more: true });
  });
});

describe("the input box", () => {
  it("counts input() calls", () => {
    expect(countInputCalls('name = input("Who? ")\ninput("Press Enter")\n# input()\n')).toBe(2);
    expect(countInputCalls('print("no")')).toBe(0);
  });

  it("sends Mar'tu's answers exactly, and pads changed answers like pressing Enter", () => {
    expect(answersFromBox("Zelda\n", ["Zelda", ""])).toEqual(["Zelda", ""]);
    expect(answersFromBox("Mira", ["Zelda", ""])).toEqual(["Mira", ""]);
    expect(answersFromBox("", undefined, 'input("Press Enter to open the door")')).toEqual([""]);
    expect(answersFromBox("Ada\n\n", undefined, 'name = input()\n')).toEqual(["Ada"]);
    expect(answersFromBox("Lucky", ["Lucky"])).toEqual(["Lucky"]);
  });
});

describe("angle labels", () => {
  it("names the curriculum's angles", () => {
    expect(angleLabel({ angle: "everyday" })).toBe("In everyday life");
    expect(angleLabel({ angle: "in Tor" })).toBe("In Tor");
    expect(angleLabel({ angle: "contrast" })).toBe("Not this");
    expect(angleLabel({ angle: "sentence frame" })).toBe("Fill the frame");
  });
});

describe("the SOLO line", () => {
  it("says \"You did that alone\" only when no Help went past Where to look and Mar'tu's version stayed closed", () => {
    expect(soloUnaided(undefined)).toBe(true);
    expect(soloUnaided({ hintsUsed: {} })).toBe(true);
    expect(soloUnaided({ hintsUsed: { "step-1": 1 } })).toBe(true);
    expect(soloUnaided({ hintsUsed: { "step-1": 2 } })).toBe(false);
    // The pass line agrees with the bubble: "on your own" only when it is true.
    const line = "Mar'tu: You did that on your own. On your map: ✓ slices.";
    expect(soloPassLine(line, true, true)).toBe(line);
    expect(soloPassLine(line, true, false)).toBe("Mar'tu: You did that with some help this time. On your map: ✓ slices.");
    expect(soloPassLine(line, false, false)).toBe(line);
    expect(soloPassLine("Bomb Shell: Shield up.", true, false)).toBe("Bomb Shell: Shield up.");
    expect(soloUnaided({ hintsUsed: { "step-1": 1, __bonus: 3 } })).toBe(true);
    expect(soloUnaided({ hintsUsed: {}, solutionShown: true })).toBe(false);
  });
});
