import { describe, expect, it } from "vitest";
import { applyStageMessage, type TheaterState } from "./bridge";

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
});
