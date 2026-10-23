import { describe, expect, it } from "vitest";
import {
  applyStageMessage,
  conversationEvents,
  parseStageMessage,
  stageMoves,
  type StageEvent,
  type TheaterState,
} from "./bridge";

const initial: TheaterState = {
  caption: "The gate is shut.",
  flareToken: 0,
  focusedImageId: null,
};

describe("stage bridge", () => {
  it("applies say, flare, and focus", () => {
    const said = applyStageMessage(initial, { type: "say", text: "We seek entry." });
    expect(said.caption).toBe("We seek entry.");

    const flared = applyStageMessage(said, { type: "flare" });
    expect(flared.flareToken).toBe(1);

    const focused = applyStageMessage(flared, { type: "focus", imageId: "arch" });
    expect(focused.focusedImageId).toBe("arch");
  });

  it("ignores unknown messages", () => {
    expect(applyStageMessage(initial, { type: "dance" })).toBe(initial);
    expect(applyStageMessage(initial, { type: "say", text: 4 })).toBe(initial);
    expect(applyStageMessage(initial, { type: "focus" })).toBe(initial);
    expect(applyStageMessage(initial, null)).toBe(initial);
    expect(applyStageMessage(initial, "nope")).toBe(initial);
  });

  it("reads party moves from Python and leaves the caption alone", () => {
    expect(parseStageMessage({ type: "move", direction: "up" })).toEqual({ type: "move", direction: "up" });
    expect(parseStageMessage({ type: "move", direction: "sideways" })).toBeNull();
    expect(parseStageMessage({ type: "move" })).toBeNull();
    expect(applyStageMessage(initial, { type: "move", direction: "left" })).toBe(initial);
    const events: StageEvent[] = [
      { type: "say", text: "Go." },
      { type: "move", direction: "left" },
      { type: "flare" },
      { type: "move", direction: "down" },
    ];
    expect(stageMoves(events)).toEqual(["left", "down"]);
  });

  it("reads dialogue prompts, options, spoken replies, and highlights from Python", () => {
    expect(parseStageMessage({ type: "prompt", text: "Will you help us?" })).toEqual({
      type: "prompt",
      text: "Will you help us?",
    });
    expect(parseStageMessage({ type: "options", options: ["Yes", "No"] })).toEqual({
      type: "options",
      options: ["Yes", "No"],
    });
    expect(parseStageMessage({ type: "options", options: ["a", "b", "c", "d", "e"] })).toBeNull();
    expect(parseStageMessage({ type: "options", options: [1] })).toBeNull();
    expect(parseStageMessage({ type: "speak", option: "option 2" })).toEqual({ type: "speak", option: "option 2" });
    expect(parseStageMessage({ type: "highlight", option: "option 2" })).toEqual({
      type: "highlight",
      option: "option 2",
    });
    expect(parseStageMessage({ type: "prompt" })).toBeNull();
    expect(applyStageMessage(initial, { type: "prompt", text: "Hi" })).toBe(initial);
    const events: StageEvent[] = [
      { type: "move", direction: "up" },
      { type: "prompt", text: "Hi" },
      { type: "speak", option: "option 1" },
    ];
    expect(conversationEvents(events)).toEqual([
      { type: "prompt", text: "Hi" },
      { type: "speak", option: "option 1" },
    ]);
  });
});

