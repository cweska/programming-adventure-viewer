import type { Beat, Module } from "./schema";
import { applyStageEvents, type StageEvent, type TheaterState } from "../stage/bridge";
import type { RunResult } from "../languages/types";

export type FailedCheck = {
  name: string;
  message: string;
};

export type Grade = {
  passed: boolean;
  canContinue: boolean;
  feedback: string | null;
  failedChecks: FailedCheck[];
};

export function visibleLessons(module: Module): Module["lessons"] {
  return module.lessons.filter((lesson) => lesson.published);
}

export function canContinueImmediately(beat: Beat): boolean {
  return !beat.activity;
}

export function initialTheater(beat: Beat): TheaterState {
  return {
    caption: beat.scene.caption,
    flareToken: 0,
    focusedImageId: null,
  };
}

export function nextTheaterState(beat: Beat, events: readonly StageEvent[]): TheaterState {
  return applyStageEvents(initialTheater(beat), events);
}

export function gradeRun(beat: Beat, result: RunResult): Grade {
  if (!beat.activity) {
    return { passed: true, canContinue: true, feedback: null, failedChecks: [] };
  }
  if (!result.ok || result.timedOut) {
    return { passed: false, canContinue: false, feedback: null, failedChecks: [] };
  }
  const failedChecks = result.checks
    .filter((check) => !check.passed)
    .map((check) => ({ name: check.name, message: check.message }));
  if (failedChecks.length === 0) {
    return {
      passed: true,
      canContinue: true,
      feedback: beat.activity.passFeedback,
      failedChecks: [],
    };
  }
  return {
    passed: false,
    canContinue: false,
    feedback: beat.activity.failFeedback,
    failedChecks,
  };
}

export async function commitProgress(
  preview: boolean,
  write: () => Promise<void> | void,
): Promise<boolean> {
  if (preview) return false;
  await write();
  return true;
}

export function starterFor(beat: Beat): string {
  if (beat.activity) return beat.activity.starterCode;
  return "# Listen to the scene, then continue.\n";
}
