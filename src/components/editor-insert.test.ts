import { describe, expect, it } from "vitest";
import { noteStart, planInsert, type InsertTarget, type InsertText, type InsertWhere } from "./editor-insert";

/** Apply a plan to a document; `|` in the input marks the cursor (a placed cursor). */
function apply(withCursor: string, text: InsertText, where: InsertWhere, placed = true, target?: InsertTarget): string {
  const at = withCursor.indexOf("|");
  const doc = withCursor.replace("|", "");
  const plan = planInsert(doc, { from: at, to: at }, placed, text, where, target);
  const out = doc.slice(0, plan.from) + plan.insert + doc.slice(plan.to);
  return `${out.slice(0, plan.anchor)}|${out.slice(plan.anchor)}`;
}

const STARTER = "# Gearshift's barrier report\n# 1. Make caster\n# 2. Make mana\n";

describe("where buttons put text in the editor", () => {
  it("Start me off never lands inside a note or after code: it starts a line of its own", () => {
    // The reviewer's case: the cursor at the end of "# 1. Make caster".
    expect(apply("# Gearshift's barrier report\n# 1. Make caster|\n# 2. Make mana\n", "caster = ", "line")).toBe(
      "# Gearshift's barrier report\n# 1. Make caster\ncaster = |\n# 2. Make mana\n",
    );
    // At the start of a note line, too.
    expect(apply("|# 1. Make caster\n", "caster = ", "line")).toBe("# 1. Make caster\ncaster = |\n");
    // After a full line of code: a new line under it, not `...Lucky") print(`.
    expect(apply('print("Welcome to the cabin, Lucky")|\n', "print(", "line")).toBe('print("Welcome to the cabin, Lucky")\nprint(|\n');
    // A blank line is used as it is.
    expect(apply("# 1. Make caster\n|\n# 2. Make mana\n", "caster = ", "line")).toBe("# 1. Make caster\ncaster = |\n# 2. Make mana\n");
    // Under a line that ends with ":", the new line is indented.
    expect(apply("def greet(name):|\n", "print(", "line")).toBe("def greet(name):\n    print(|\n");
    expect(apply("    # 2. Return it|\n", "return ", "line")).toBe("    # 2. Return it\n    return |\n");
  });

  it("names and picks go at the cursor, except inside a note", () => {
    expect(apply("print(|)\n", "name", "code")).toBe("print(name|)\n");
    expect(apply('print("Welcome to the cabin, " + |\n', "name", "code")).toBe('print("Welcome to the cabin, " + name|\n');
    expect(apply("# 1. Make caster|\n", "caster", "code")).toBe("# 1. Make caster\ncaster|\n");
    expect(apply("|# 1. Make caster\n", "caster", "code")).toBe("# 1. Make caster\ncaster|\n");
    expect(apply("mana = 20  # full|\n", "mana", "code")).toBe("mana = 20  # full\nmana|\n");
    // A # inside quotes is not a note.
    expect(apply('print("#1 |\n', "caster", "code")).toBe('print("#1 caster|\n');
    // The text can depend on what is before it on its (final) line.
    const quoted: InsertText = (before) => (before.endsWith('"') ? "Zelda" : '"Zelda"');
    expect(apply('hero = "|\n', quoted, "code")).toBe('hero = "Zelda|\n');
    expect(apply("# hero here|\n", quoted, "code")).toBe('# hero here\n"Zelda"|\n');
  });

  it("tells the text what is after the cursor on its line (\"\" when it gets a line of its own)", () => {
    const seen: string[] = [];
    const text: InsertText = (before, after) => {
      seen.push(`${before}|${after}`);
      return "x";
    };
    apply('print("|")\n', text, "code");
    apply("# Print the symbols|\n", text, "code");
    apply("# note\n|\n", text, "code");
    expect(seen).toEqual(['print("|")', "|", "|"]);
  });

  it("a # note goes on a line of its own, above the line with the cursor", () => {
    expect(apply('print("Steady, now.")|\n', "# Night watch.", "note")).toBe('# Night watch.|\nprint("Steady, now.")\n');
    expect(apply('print("a")\n|\nprint("b")\n', "# Night watch.", "note")).toBe('print("a")\n# Night watch.|\nprint("b")\n');
  });

  it("before the student clicks into the code, text goes at the end (a note at the top)", () => {
    expect(apply(`${STARTER}|`, "caster = ", "line", false)).toBe(`${STARTER}caster = |`);
    expect(apply("|print(1)", "name", "code", false)).toBe("print(1)\nname|");
    expect(apply("|", "name", "cursor", false)).toBe("name|");
    expect(apply('|print("Steady, now.")\n', "# Night watch.", "note", false)).toBe('# Night watch.|\nprint("Steady, now.")\n');
  });

  it("before a click, Start me off goes where the step's hint says: in place of `pass`, or under a line", () => {
    // Unit 3's Ingredients: the step's line replaces the recipe's `pass`, never lands at the bottom outside it.
    const warn = 'def warn(hero_name):\n    # print the hero\n    pass\n\nwarn("Lucky")\n|';
    expect(apply(warn, "print(", "line", false, { line: "pass", how: "replace" })).toBe(
      'def warn(hero_name):\n    # print the hero\n    print(|\n\nwarn("Lucky")\n',
    );
    // Several recipes with `pass`: the one in the recipe the step names.
    const four = "def step_north():\n    pass\n\ndef step_west():\n    pass\n|";
    expect(apply(four, 'scout.step(', "line", false, { line: "pass", how: "replace", near: ["step_west"] })).toBe(
      "def step_north():\n    pass\n\ndef step_west():\n    scout.step(|\n",
    );
    expect(apply(four, 'scout.step(', "line", false, { line: "pass", how: "replace" })).toBe(
      "def step_north():\n    scout.step(|\n\ndef step_west():\n    pass\n",
    );
    // "on the line after `total = affinity * 2`": a new line under it, with its indent.
    const mana = "def max_mana_for(affinity):\n    total = affinity * 2\n    # 1. hand back total\n|";
    expect(apply(mana, "return ", "line", false, { line: "total = affinity * 2", how: "after" })).toBe(
      "def max_mana_for(affinity):\n    total = affinity * 2\n    return |\n    # 1. hand back total\n",
    );
    // "under the `# passed:` note" (Unit 2): a note line matches by its start.
    expect(apply("roll = 12\n# passed: True when roll is enough\n|", "passed = ", "line", false, { line: "# passed:", how: "after" })).toBe(
      "roll = 12\n# passed: True when roll is enough\npassed = |\n",
    );
    // The named recipe's `pass` already rewritten: a new line at the end of that recipe, never another recipe's `pass`.
    const westDone = 'def step_north():\n    pass\n\ndef step_west():\n    scout.step(West)\n\nstep_west()\n|';
    expect(apply(westDone, "scout.step(", "line", false, { line: "pass", how: "replace", near: ["step_west"] })).toBe(
      'def step_north():\n    pass\n\ndef step_west():\n    scout.step(West)\n    scout.step(|\n\nstep_west()\n',
    );
    // "under `# 2.`" with the starter's placeholder right under it (Unit 2's `road_roll = 0`): that line is rewritten,
    // never a second `road_roll =` above it. A real line of the student's own under the note is never replaced.
    expect(apply("# 2. Roll road_roll.\nroad_roll = 0\n\nprint(road_roll)\n|", "road_roll = ", "line", false, { line: "# 2.", how: "after" })).toBe(
      "# 2. Roll road_roll.\nroad_roll = |\n\nprint(road_roll)\n",
    );
    expect(apply("# 4. Print it\nprint(road_roll)\n|", "print(", "line", false, { line: "# 4.", how: "after" })).toBe(
      "# 4. Print it\nprint(|\nprint(road_roll)\n",
    );
    expect(apply("# 2.\nroad_roll = random.randint(1, 6)\n|", "road_roll = ", "line", false, { line: "# 2.", how: "after" })).toBe(
      "# 2.\nroad_roll = |\nroad_roll = random.randint(1, 6)\n",
    );
    // Unit 5: "above `print(caster["mana"])`": a new line over it, with its indent (inside the `else`).
    const cast = 'else:\n    # 3. Subtract the cost first.\n    print(caster["mana"])\n|';
    expect(apply(cast, 'caster["mana"] = ', "line", false, { line: 'print(caster["mana"])', how: "before" })).toBe(
      'else:\n    # 3. Subtract the cost first.\n    caster["mana"] = |\n    print(caster["mana"])\n',
    );
    // Unit 5: "under `# 5.`" when the note goes on over `#    ...` lines: under the whole note, never inside it.
    const ledger = "# 5. Print Bomb Shell's dexterity\n#    and Oogrish's intelligence,\n#    through roster.\n\n# 6. Fire Bolt\n|";
    expect(apply(ledger, "print(roster[", "line", false, { line: "# 5.", how: "after" })).toBe(
      "# 5. Print Bomb Shell's dexterity\n#    and Oogrish's intelligence,\n#    through roster.\nprint(roster[|\n\n# 6. Fire Bolt\n",
    );
    // A next note that starts a new task (`# 6.`) is not part of the one above.
    expect(apply("# 4. roster = [...]\n# 5. Print\n|", "roster = ", "line", false, { line: "# 4.", how: "after" })).toBe(
      "# 4. roster = [...]\nroster = |\n# 5. Print\n",
    );
    // No such line: the end of the code, as before. A placed cursor keeps its own place.
    expect(apply(`${STARTER}|`, "caster = ", "line", false, { line: "pass", how: "replace" })).toBe(`${STARTER}caster = |`);
    expect(apply("def warn(x):\n    pass\n\nwarn(1)|\n", "print(", "line", true, { line: "pass", how: "replace" })).toBe(
      "def warn(x):\n    pass\n\nwarn(1)\nprint(|\n",
    );
  });

  it("the symbol tray still types exactly at the cursor, even in a note", () => {
    expect(apply("# a note |\n", '"', "cursor")).toBe('# a note "|\n');
  });

  it("finds where a note starts", () => {
    expect(noteStart("x = 1  # one")).toBe(7);
    expect(noteStart('print("#")')).toBe(-1);
    expect(noteStart("print('it\\'s # fine')  # yes")).toBe(23);
    expect(noteStart("")).toBe(-1);
  });
});
