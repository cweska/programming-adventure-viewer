import { describe, expect, it } from "vitest";
import { inlineParts, instructionBlocks, instructionText } from "./instructions";

describe("part instructions", () => {
  it("marks text in backticks as code", () => {
    expect(inlineParts('Type `print("hi")` and press Run.')).toEqual([
      { code: false, text: "Type " },
      { code: true, text: 'print("hi")' },
      { code: false, text: " and press Run." },
    ]);
    expect(inlineParts("`left = 2`")).toEqual([{ code: true, text: "left = 2" }]);
  });

  it("keeps an unmatched backtick as plain text", () => {
    expect(inlineParts("one `two` three ` four")).toEqual([
      { code: false, text: "one " },
      { code: true, text: "two" },
      { code: false, text: " three ` four" },
    ]);
  });

  it("puts each line on its own and groups numbered lines into steps", () => {
    const blocks = instructionBlocks(
      "Finish `add_spell()`.\n1. Fill in `mana_cost`.\n2. Store the spell.\n\nThen press Run.",
    );
    expect(blocks).toEqual([
      {
        kind: "line",
        parts: [
          { code: false, text: "Finish " },
          { code: true, text: "add_spell()" },
          { code: false, text: "." },
        ],
      },
      {
        kind: "steps",
        items: [
          [
            { code: false, text: "Fill in " },
            { code: true, text: "mana_cost" },
            { code: false, text: "." },
          ],
          [{ code: false, text: "Store the spell." }],
        ],
      },
      { kind: "line", parts: [{ code: false, text: "Then press Run." }] },
    ]);
  });

  it("reads back as plain text", () => {
    expect(instructionText("Type `x = 1`.\n1. Press `Run`.")).toBe("Type x = 1.\nPress Run.");
  });
});
