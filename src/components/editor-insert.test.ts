import { describe, expect, it } from "vitest";
import { noteStart, planInsert, type InsertText, type InsertWhere } from "./editor-insert";

/** Apply a plan to a document; `|` in the input marks the cursor (a placed cursor). */
function apply(withCursor: string, text: InsertText, where: InsertWhere, placed = true): string {
  const at = withCursor.indexOf("|");
  const doc = withCursor.replace("|", "");
  const plan = planInsert(doc, { from: at, to: at }, placed, text, where);
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
