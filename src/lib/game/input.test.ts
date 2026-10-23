import { describe, expect, it } from "vitest";
import { commandForKey } from "./input";

describe("keyboard input", () => {
  it("maps arrow keys and WASD in either case to the four directions", () => {
    const cases: [string, string][] = [
      ["ArrowLeft", "left"],
      ["ArrowRight", "right"],
      ["ArrowUp", "up"],
      ["ArrowDown", "down"],
      ["a", "left"],
      ["d", "right"],
      ["w", "up"],
      ["s", "down"],
      ["A", "left"],
      ["D", "right"],
      ["W", "up"],
      ["S", "down"],
    ];
    for (const [key, direction] of cases) {
      expect(commandForKey(key), key).toEqual({ type: "move", direction });
    }
  });

  it("maps Tab, Space, Enter, Escape, and number keys", () => {
    expect(commandForKey("Tab")).toEqual({ type: "swap" });
    expect(commandForKey(" ")).toEqual({ type: "confirm" });
    expect(commandForKey("Enter")).toEqual({ type: "confirm" });
    expect(commandForKey("Escape")).toEqual({ type: "release" });
    expect(commandForKey("1")).toEqual({ type: "option", index: 0 });
    expect(commandForKey("9")).toEqual({ type: "option", index: 8 });
  });

  it("ignores other keys", () => {
    for (const key of ["q", "0", "Shift", "Alt", "F5", "Arrow", "aa"]) {
      expect(commandForKey(key), key).toBeNull();
    }
  });
});
