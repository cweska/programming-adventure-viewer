import { describe, expect, it } from "vitest";
import { addLine, hashSeed, moveLine, remainingPieces, removeLine, seededShuffle, spokenLine } from "./parsons-logic";

describe("seededShuffle", () => {
  const lines = ["a = 1", "b = 2", "print(a + b)", "print(a)", "c = 3"];

  it("gives the same order for the same seed", () => {
    expect(seededShuffle(lines, "unit/item/ex")).toEqual(seededShuffle(lines, "unit/item/ex"));
  });

  it("keeps every item exactly once", () => {
    const shuffled = seededShuffle(lines, "anything");
    expect([...shuffled].sort()).toEqual([...lines].sort());
  });

  it("never hands back the original order", () => {
    for (let seed = 0; seed < 200; seed += 1) {
      expect(seededShuffle(["x", "y"], `seed-${seed}`)).toEqual(["y", "x"]);
      expect(seededShuffle(lines, `seed-${seed}`)).not.toEqual(lines);
    }
  });

  it("does not change the input and copes with tiny lists", () => {
    const input = ["one", "two", "three"];
    seededShuffle(input, "s");
    expect(input).toEqual(["one", "two", "three"]);
    expect(seededShuffle([], "s")).toEqual([]);
    expect(seededShuffle(["solo"], "s")).toEqual(["solo"]);
    expect(seededShuffle(["same", "same"], "s")).toEqual(["same", "same"]);
  });

  it("depends on the seed", () => {
    const many = Array.from({ length: 12 }, (_, index) => `line ${index}`);
    const orders = new Set(["a", "b", "c", "d", "e"].map((seed) => seededShuffle(many, seed).join("|")));
    expect(orders.size).toBeGreaterThan(1);
    expect(hashSeed("a")).not.toBe(hashSeed("b"));
  });
});

describe("remainingPieces", () => {
  it("removes the pieces already used, by position", () => {
    const blocks = ["a", "b", "c"];
    expect(remainingPieces(blocks, [])).toEqual([0, 1, 2]);
    expect(remainingPieces(blocks, ["b"])).toEqual([0, 2]);
    expect(remainingPieces(blocks, ["c", "a", "b"])).toEqual([]);
  });

  it("handles repeated lines one at a time", () => {
    const blocks = ['print("hi")', "x = 1", 'print("hi")'];
    expect(remainingPieces(blocks, ['print("hi")'])).toEqual([1, 2]);
    expect(remainingPieces(blocks, ['print("hi")', 'print("hi")'])).toEqual([1]);
  });

  it("ignores lines that are not pieces", () => {
    expect(remainingPieces(["a"], ["zzz"])).toEqual([0]);
  });
});

describe("program edits", () => {
  it("adds, removes and moves lines without changing the input", () => {
    const value = ["a", "b", "c"];
    expect(addLine(value, "d")).toEqual(["a", "b", "c", "d"]);
    expect(removeLine(value, 1)).toEqual(["a", "c"]);
    expect(removeLine(value, 9)).toEqual(["a", "b", "c"]);
    expect(moveLine(value, 0, 1)).toEqual(["b", "a", "c"]);
    expect(moveLine(value, 2, 0)).toEqual(["c", "a", "b"]);
    expect(moveLine(value, 2, 5)).toEqual(["a", "b", "c"]);
    expect(moveLine(value, 0, -3)).toEqual(["a", "b", "c"]);
    expect(moveLine(value, 7, 0)).toEqual(["a", "b", "c"]);
    expect(value).toEqual(["a", "b", "c"]);
  });
});

describe("spokenLine", () => {
  it("says the indentation out loud", () => {
    expect(spokenLine("print(x)")).toBe("print(x)");
    expect(spokenLine("    print(x)")).toBe("print(x) (indented once)");
    expect(spokenLine("        print(x)")).toBe("print(x) (indented 2 times)");
    expect(spokenLine("   ")).toBe("blank line (indented once)");
  });
});
