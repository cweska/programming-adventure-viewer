import { describe, expect, it } from "vitest";
import { bundledModules } from "./modules";
import { runPythonChecks } from "./run-checks";
import { activitySetup } from "./setup";

const codingParts = bundledModules.flatMap((module) =>
  module.lessons.flatMap((lesson) =>
    lesson.beats.flatMap((beat) => (beat.activity ? [{ module: module.id, beat, activity: beat.activity }] : [])),
  ),
);

describe("Show solution", () => {
  it("has a finished solution for every coding part in every module", () => {
    expect(codingParts.length).toBe(19);
    for (const { module, beat, activity } of codingParts) {
      expect(activity.solution, `${module}/${beat.id}`).toBeTruthy();
    }
  });

  it("passes every check with each part's solution", () => {
    for (const { module, beat, activity } of codingParts) {
      const result = runPythonChecks(activity.solution ?? "", activity.checks, { setup: activitySetup(activity) });
      expect(result.ok, `${module}/${beat.id}: ${result.error}`).toBe(true);
      expect(
        result.checks.filter((check) => !check.passed).map((check) => `${module}/${beat.id} ${check.name}: ${check.message}`),
      ).toEqual([]);
    }
  });
});
