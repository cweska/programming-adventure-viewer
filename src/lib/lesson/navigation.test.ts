import { describe, expect, it } from "vitest";
import { emberkeepModule } from "./emberkeep";
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
    expect(partLabel(0, 3)).toBe("Part 1 of 3");
    expect(partLabel(1, 3)).toBe("Part 2 of 3");
  });

  it("lets a story part unlock the next part and stops Forward there", () => {
    const start = createPartNavigation(parts);
    expect(start.index).toBe(0);
    expect(start.unlocked).toBe(1);
    expect(canGoForward(start, parts.length)).toBe(true);

    const courtyard = goForward(start, parts);
    expect(courtyard.index).toBe(1);
    expect(courtyard.unlocked).toBe(1);
    expect(canGoForward(courtyard, parts.length)).toBe(false);
    expect(goForward(courtyard, parts)).toBe(courtyard);
  });

  it("unlocks the part after a challenge only when that challenge passes", () => {
    let state = goForward(createPartNavigation(parts), parts);
    expect(goForward(state, parts).index).toBe(1);

    state = recordPass(state, parts);
    expect(state.passed[1]).toBe(true);
    expect(state.unlocked).toBe(2);
    state = goForward(state, parts);
    expect(state.index).toBe(2);
    expect(canGoForward(state, parts.length)).toBe(false);
  });

  it("restores the previous part's code and does not erase a later pass", () => {
    let state = goForward(createPartNavigation(parts), parts);
    state = setPartCode(state, 1, "draft = \"courtyard\"\n");
    state = recordPass(state, parts);
    const returned = goBack(state);

    expect(returned.index).toBe(0);
    expect(returned.code[0]).toContain("Listen to the scene");
    expect(returned.passed[1]).toBe(true);
    expect(returned.unlocked).toBe(2);

    const again = goForward(returned, parts);
    expect(again.index).toBe(1);
    expect(again.code[1]).toBe("draft = \"courtyard\"\n");
    expect(goForward(again, parts).index).toBe(2);
  });

  it("keeps earlier passes when resuming a later part", () => {
    const resumed = navigationFromProgress(parts, 2, "stage.say('hello')\n", false);
    expect(resumed.index).toBe(2);
    expect(resumed.passed[1]).toBe(true);
    expect(resumed.unlocked).toBe(2);
    expect(goBack(resumed).passed[1]).toBe(true);
  });
});
