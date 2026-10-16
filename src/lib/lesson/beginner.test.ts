import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { emberkeepModule } from "./emberkeep";
import { runPythonChecks } from "./run-checks";
import { moduleSchema, type Activity } from "./schema";

const solutions: Record<string, string> = {
  "run-ember": 'print("ember")\n',
  "say-shut": 'print("The gate is shut.")\n',
  "say-keeper": 'print("A keeper waits.")\n',
  "two-lines": 'print("The left torch is dark.")\nprint("The right torch is dark.")\n',
  "remember-ember": 'word = "ember"\n',
  "change-word": 'word = "keep"\n',
  "say-name": 'name = "Rowan"\nprint(name)\n',
  "say-place": 'place = "Emberkeep"\nprint(place)\n',
  "torch-counts": "left = 2\nright = 3\n",
  "say-counts": "left = 2\nright = 3\nprint(left)\nprint(right)\n",
  "say-sum": "left = 2\nright = 3\nprint(left + right)\n",
  "gate-answers": "left = 4\nright = 1\nprint(left + right)\n",
};

const assignment = /(^|\n)\s*[A-Za-z_][A-Za-z0-9_]*\s*=/;

function failSentences(text: string): number {
  const withoutQuotes = text.replace(/"[^"]*"/g, "");
  return withoutQuotes.match(/[.!?]/g)?.length ?? 0;
}

function requireActivity(activity: Activity | undefined, id: string): Activity {
  if (!activity) throw new Error(`${id} should be a coding part`);
  return activity;
}

describe("beginner sample module", () => {
  const lesson = emberkeepModule.lessons[0];

  it("is one published python lesson with 15 parts", () => {
    expect(moduleSchema.safeParse(emberkeepModule).success).toBe(true);
    expect(emberkeepModule.language).toBe("python");
    expect(emberkeepModule.lessons).toHaveLength(1);
    expect(lesson.published).toBe(true);
    expect(lesson.beats).toHaveLength(15);
    expect(lesson.beats.map((part) => part.id)).toEqual([
      "run-ember",
      "say-shut",
      "say-keeper",
      "two-lines",
      "wall-remembers",
      "remember-ember",
      "change-word",
      "not-the-same",
      "say-name",
      "say-place",
      "two-torches",
      "torch-counts",
      "say-counts",
      "say-sum",
      "gate-answers",
    ]);
  });

  it("reuses scene art and speaks in parts", () => {
    const spoken = [
      emberkeepModule.title,
      lesson.title,
      ...lesson.beats.flatMap((part) => [
        part.instructions,
        part.scene.caption,
        ...part.scene.images.map((image) => image.alt),
        part.activity?.passFeedback ?? "",
        part.activity?.failFeedback ?? "",
        ...(part.activity?.checks.map((check) => check.name) ?? []),
      ]),
    ];
    for (const text of spoken) {
      expect(text.toLowerCase()).not.toMatch(/\bbeat\b/);
    }
    for (const part of lesson.beats) {
      if (part.activity) expect(failSentences(part.activity.failFeedback)).toBe(1);
      for (const image of part.scene.images) {
        const relative = image.src.replace(/^\//, "");
        expect(existsSync(path.join("public", relative))).toBe(true);
      }
    }
    expect(lesson.beats.filter((part) => !part.activity).map((part) => part.id)).toEqual([
      "wall-remembers",
      "not-the-same",
      "two-torches",
    ]);
  });

  it("passes every coding part with a reference solution", () => {
    for (const part of lesson.beats) {
      if (!part.activity) continue;
      const solution = solutions[part.id];
      expect(solution, part.id).toBeTruthy();
      const result = runPythonChecks(solution, part.activity.checks);
      expect(result.ok, `${part.id} ${result.error}`).toBe(true);
      expect(
        result.checks.map((check) => check.passed),
        result.checks.map((check) => check.message).join("\n"),
      ).toEqual(part.activity.checks.map(() => true));
    }
  });

  it("does not require a variable before part 6", () => {
    for (const part of lesson.beats.slice(0, 5)) {
      if (!part.activity) continue;
      const solution = solutions[part.id];
      expect(part.activity.starterCode).not.toMatch(assignment);
      expect(solution).not.toMatch(assignment);
      const result = runPythonChecks(solution, part.activity.checks);
      expect(result.checks.every((check) => check.passed), part.id).toBe(true);
    }

    const sentence = requireActivity(lesson.beats[1]?.activity, "say-shut");
    const rememberedOnly = runPythonChecks('sentence = "The gate is shut."\n', sentence.checks);
    expect(rememberedOnly.ok).toBe(true);
    expect(rememberedOnly.checks.some((check) => !check.passed)).toBe(true);

    const firstVariable = requireActivity(lesson.beats[5]?.activity, "remember-ember");
    expect(solutions["remember-ember"]).not.toContain("print");
    expect(runPythonChecks(solutions["remember-ember"], firstVariable.checks).checks.every((check) => check.passed)).toBe(
      true,
    );
  });

  it("rejects quoted names and numbers stuck together as text", () => {
    const sayName = requireActivity(lesson.beats[8]?.activity, "say-name");
    const quoted = runPythonChecks('name = "Rowan"\nprint("name")\n', sayName.checks);
    expect(quoted.ok).toBe(true);
    expect(quoted.checks.some((check) => !check.passed)).toBe(true);

    const saySum = requireActivity(lesson.beats[13]?.activity, "say-sum");
    const stuck = runPythonChecks('left = 2\nright = 3\nprint(str(left) + str(right))\n', saySum.checks);
    expect(stuck.ok).toBe(true);
    expect(stuck.checks.some((check) => !check.passed)).toBe(true);

    const summed = runPythonChecks(solutions["say-sum"], saySum.checks);
    expect(summed.stdout.trim()).toBe("5");
    expect(summed.stdout.trim()).not.toBe("23");
  });

  it("lets browser checks read printed text", () => {
    const worker = readFileSync("public/workers/python-worker.js", "utf8");
    expect(worker).toContain('globals.set("_captured_stdout"');
  });
});
