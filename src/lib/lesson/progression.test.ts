import { describe, expect, it } from "vitest";
import type { RunResult } from "../languages/types";
import { makeValidModule } from "./fixtures";
import {
  canContinueImmediately,
  commitProgress,
  gradeRun,
  nextTheaterState,
  visibleLessons,
} from "./progression";

function runResult(overrides: Partial<RunResult> = {}): RunResult {
  return {
    ok: true,
    stdout: "",
    stderr: "",
    traceback: "",
    checks: [],
    stageEvents: [],
    ...overrides,
  };
}

describe("progression", () => {
  const module = makeValidModule();
  const story = module.lessons[0].beats[0];
  const challenge = module.lessons[0].beats[1];
  const interactive = module.lessons[1].beats[0];

  it("lets a story beat continue immediately", () => {
    expect(canContinueImmediately(story)).toBe(true);
    expect(canContinueImmediately(challenge)).toBe(false);
    const grade = gradeRun(story, runResult({ ok: false, traceback: "NameError: name 'x' is not defined" }));
    expect(grade.canContinue).toBe(true);
  });

  it("unlocks continue when a challenge passes", () => {
    const grade = gradeRun(
      challenge,
      runResult({
        checks: [{ name: "oil lights the torch", passed: true, message: "" }],
      }),
    );
    expect(grade.passed).toBe(true);
    expect(grade.canContinue).toBe(true);
    expect(grade.feedback).toBe("The torches catch.");
    expect(grade.failedChecks).toEqual([]);
  });

  it("stays on the beat and surfaces fail feedback plus the failed check", () => {
    const grade = gradeRun(
      challenge,
      runResult({
        checks: [{ name: "oil lights the torch", passed: false, message: "Passing oil should return lit" }],
      }),
    );
    expect(grade.passed).toBe(false);
    expect(grade.canContinue).toBe(false);
    expect(grade.feedback).toBe("The sconces stay cold.");
    expect(grade.failedChecks).toEqual([
      { name: "oil lights the torch", message: "Passing oil should return lit" },
    ]);
  });

  it("updates theater state from interactive stage events", () => {
    const theater = nextTheaterState(interactive, [
      { type: "say", text: "I seek entry." },
      { type: "flare" },
      { type: "focus", imageId: "keeper" },
    ]);
    expect(theater.caption).toBe("I seek entry.");
    expect(theater.flareToken).toBe(1);
    expect(theater.focusedImageId).toBe("keeper");
  });

  it("does not write classroom progress in preview mode", async () => {
    const writes: string[] = [];
    await expect(
      commitProgress(true, () => {
        writes.push("preview");
      }),
    ).resolves.toBe(false);
    expect(writes).toEqual([]);

    await expect(
      commitProgress(false, () => {
        writes.push("saved");
      }),
    ).resolves.toBe(true);
    expect(writes).toEqual(["saved"]);
  });

  it("shows published lessons in order", () => {
    expect(visibleLessons(module).map((lesson) => lesson.id)).toEqual(["gate"]);
  });
});
