import { describe, expect, it } from "vitest";
import {
  angleLabel,
  answersFromBox,
  compareLines,
  countInputCalls,
  countsAsAttempt,
  firstParagraph,
  helpOffer,
  helpOfferLine,
  helpRungs,
  helpState,
  insideString,
  NUDGE_AFTER_MISSES,
  NUDGE_IDLE_MS,
  NUDGE_NO_PROGRESS_MS,
  pickInsertion,
  RUNG_PACE_MS,
  rungPaced,
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

  it("paces rungs: a Run or a few seconds opens the next one", () => {
    expect(rungPaced(null, false, 1_000)).toBe(false);
    expect(rungPaced(1_000, false, 1_000 + RUNG_PACE_MS - 1)).toBe(true);
    expect(rungPaced(1_000, false, 1_000 + RUNG_PACE_MS)).toBe(false);
    expect(rungPaced(1_000, true, 1_001)).toBe(false);
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
    idleSinceMissMs: null,
  };

  it("offers after 3 misses on a step, 4 minutes without progress, or 90 seconds idle after a miss", () => {
    expect(helpOffer(quiet)).toBeNull();
    expect(helpOffer({ ...quiet, missesInARow: NUDGE_AFTER_MISSES - 1 })).toBeNull();
    expect(helpOffer({ ...quiet, missesInARow: NUDGE_AFTER_MISSES })).toBe("misses");
    expect(helpOffer({ ...quiet, msSinceProgress: NUDGE_NO_PROGRESS_MS })).toBe("time");
    expect(helpOffer({ ...quiet, idleSinceMissMs: NUDGE_IDLE_MS - 1 })).toBeNull();
    expect(helpOffer({ ...quiet, idleSinceMissMs: NUDGE_IDLE_MS })).toBe("idle");
    expect(NUDGE_AFTER_MISSES).toBe(3);
    expect(NUDGE_NO_PROGRESS_MS).toBe(240_000);
    expect(NUDGE_IDLE_MS).toBe(90_000);
  });

  it("under Keep it short, offers only after repeated misses (curriculum §2.3)", () => {
    expect(helpOffer({ ...quiet, preset: "short", missesInARow: NUDGE_AFTER_MISSES })).toBe("misses");
    expect(helpOffer({ ...quiet, preset: "short", msSinceProgress: NUDGE_NO_PROGRESS_MS })).toBeNull();
    expect(helpOffer({ ...quiet, preset: "short", idleSinceMissMs: NUDGE_IDLE_MS })).toBeNull();
  });

  it("stays quiet without Help, when done, dismissed, or with nothing left", () => {
    const ready = { ...quiet, missesInARow: 5 };
    expect(helpOffer({ ...ready, helpAvailable: false })).toBeNull();
    expect(helpOffer({ ...ready, done: true })).toBeNull();
    expect(helpOffer({ ...ready, dismissed: true })).toBeNull();
    expect(helpOffer({ ...ready, rungsLeft: 0 })).toBeNull();
  });

  it("says one kind line", () => {
    expect(helpOfferLine("misses")).toContain("Read the last line first");
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
