import { describe, expect, it } from "vitest";
import { emberkeepModule } from "./emberkeep";
import { findModule } from "./modules";
import {
  canGoForward,
  createPartNavigation,
  goBack,
  goForward,
  navigationFromProgress,
  partLabel,
  recordPass,
  setPartCode,
} from "./navigation";

const parts = emberkeepModule.lessons[0].beats;

describe("part navigation", () => {
  it("labels parts for the student", () => {
    expect(partLabel(0, parts.length)).toBe("Part 1 of 15");
    expect(partLabel(14, parts.length)).toBe("Part 15 of 15");
  });

  it("keeps Forward locked on the first coding part until it passes", () => {
    const start = createPartNavigation(parts);
    expect(start.index).toBe(0);
    expect(start.unlocked).toBe(0);
    expect(canGoForward(start, parts.length)).toBe(false);
    expect(start.code[0]).toContain('print("ember")');
    expect(goForward(start, parts)).toBe(start);
  });

  it("unlocks the next part only after a coding part passes", () => {
    let state = recordPass(createPartNavigation(parts), parts);
    expect(state.passed[0]).toBe(true);
    expect(state.unlocked).toBe(1);
    state = goForward(state, parts);
    expect(state.index).toBe(1);
    expect(canGoForward(state, parts.length)).toBe(false);
    expect(goForward(state, parts).index).toBe(1);
  });

  it("lets a story part unlock the next part and stops Forward on the following coding part", () => {
    let state = createPartNavigation(parts);
    for (let index = 0; index < 4; index += 1) {
      state = recordPass(state, parts);
      state = goForward(state, parts);
    }
    expect(state.index).toBe(4);
    expect(parts[4]?.activity).toBeUndefined();
    expect(state.code[4]).toContain("Listen to the scene");
    expect(canGoForward(state, parts.length)).toBe(true);

    state = goForward(state, parts);
    expect(state.index).toBe(5);
    expect(canGoForward(state, parts.length)).toBe(false);
    expect(goForward(state, parts)).toBe(state);
  });

  it("restores the previous part's code and does not erase a later pass", () => {
    let state = recordPass(createPartNavigation(parts), parts);
    state = goForward(state, parts);
    state = setPartCode(state, 1, 'print("draft")\n');
    state = recordPass(state, parts);
    const returned = goBack(state);

    expect(returned.index).toBe(0);
    expect(returned.code[0]).toContain('print("ember")');
    expect(returned.passed[1]).toBe(true);
    expect(returned.unlocked).toBe(2);

    const again = goForward(returned, parts);
    expect(again.index).toBe(1);
    expect(again.code[1]).toBe('print("draft")\n');
    expect(goForward(again, parts).index).toBe(2);
  });

  it("keeps earlier passes when resuming a later part", () => {
    const resumed = navigationFromProgress(parts, 6, 'word = "keep"\n', false);
    expect(resumed.index).toBe(6);
    expect(resumed.passed[1]).toBe(true);
    expect(resumed.unlocked).toBe(6);
    expect(goBack(resumed).passed[1]).toBe(true);
    expect(canGoForward(resumed, parts.length)).toBe(false);
  });

  it("opens story parts at once but holds a part with a board goal until it is passed", () => {
    const leyline = findModule("leylines-awaken")?.lessons[0].beats ?? [];
    const start = createPartNavigation(leyline);
    expect(start.unlocked).toBe(3);
    const atDoor = navigationFromProgress(leyline, 3, "", false);
    expect(leyline[3]?.board?.goal?.type).toBe("reach");
    expect(canGoForward(atDoor, leyline.length)).toBe(false);
    const passed = recordPass(atDoor, leyline);
    expect(passed.passed[3]).toBe(true);
    expect(passed.unlocked).toBe(5);
  });
});
