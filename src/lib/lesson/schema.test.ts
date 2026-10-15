import { describe, expect, it } from "vitest";
import { makeValidModule } from "./fixtures";
import { moduleSchema } from "./schema";

describe("lesson schema", () => {
  it("accepts a valid module", () => {
    const parsed = moduleSchema.safeParse(makeValidModule());
    expect(parsed.success).toBe(true);
  });

  it("accepts optional scene media", () => {
    const module = makeValidModule();
    module.lessons[0].beats[0].scene.video = "/scenes/gate.mp4";
    module.lessons[0].beats[0].scene.narration = "/audio/narration.mp3";
    module.lessons[0].beats[0].scene.music = "/audio/music.mp3";
    expect(moduleSchema.safeParse(module).success).toBe(true);
  });

  it("rejects missing fields", () => {
    const missingTitle = makeValidModule();
    delete (missingTitle as { title?: string }).title;
    expect(moduleSchema.safeParse(missingTitle).success).toBe(false);

    const missingLessons = makeValidModule();
    delete (missingLessons as { lessons?: unknown }).lessons;
    expect(moduleSchema.safeParse(missingLessons).success).toBe(false);

    const missingScene = makeValidModule();
    delete (missingScene.lessons[0].beats[0] as { scene?: unknown }).scene;
    expect(moduleSchema.safeParse(missingScene).success).toBe(false);

    const missingKind = makeValidModule();
    const activity = missingKind.lessons[0].beats[1].activity;
    if (!activity) throw new Error("fixture should include an activity");
    delete (activity as { kind?: string }).kind;
    expect(moduleSchema.safeParse(missingKind).success).toBe(false);
  });

  it("rejects a bad activity kind", () => {
    const module = makeValidModule();
    const activity = module.lessons[0].beats[1].activity;
    if (!activity) throw new Error("fixture should include an activity");
    (activity as { kind: string }).kind = "quiz";
    const parsed = moduleSchema.safeParse(module);
    expect(parsed.success).toBe(false);
    if (!parsed.success) {
      expect(parsed.error.issues.some((issue) => issue.path.includes("kind"))).toBe(true);
    }
  });

  it("rejects a language other than python", () => {
    const module = makeValidModule();
    (module as { language: string }).language = "javascript";
    const parsed = moduleSchema.safeParse(module);
    expect(parsed.success).toBe(false);
    if (!parsed.success) {
      expect(parsed.error.issues.some((issue) => issue.path.includes("language"))).toBe(true);
    }
  });
});
