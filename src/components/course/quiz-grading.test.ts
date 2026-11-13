import { describe, expect, it } from "vitest";
import { questionSchema, type Question } from "../../lib/course/schema";
import {
  emptyResponse,
  fillCorrect,
  gradeWithoutPython,
  hasAnswer,
  normalizeOutput,
  outputMatches,
  parsonsBlocks,
  parsonsCode,
  predictCorrect,
  quizPercent,
  responseText,
  seededShuffle,
} from "./quiz-grading";

function question<T extends Question["type"]>(raw: Record<string, unknown> & { type: T }): Extract<Question, { type: T }> {
  return questionSchema.parse({ id: "q", q: "Question?", explain: "Because.", ...raw }) as Extract<Question, { type: T }>;
}

const mc = question({ type: "mc", choices: ["a", "b", "c"], answer: 1 });
const predictTyped = question({ type: "predict", code: "print('hi')\nprint('there')", answer: "hi\nthere" });
const predictChoices = question({
  type: "predict",
  code: "print(1)",
  answer: "Next burst in 37 hours",
  choices: ["Next burst in 37 hours", "Next burst in hours hours"],
});
const predictError = question({ type: "predict", code: "print(x)", answer: "ERROR: NameError: name 'x' is not defined" });
const fill = question({ type: "fill", code: 'print("a" + ___ + "b")', answer: '" "', accept: ["' '"], expectedOutput: "a b" });
const parsons = question({ type: "parsons", lines: ["print(1)", "print(2)", "print(3)"], distractors: ["print(4)"], expectedOutput: "1\n2\n3" });
const bug = question({ type: "bug", code: 'print("x)', fix: 'print("x")', expectedOutput: "x" });

describe("output comparison", () => {
  it("ignores trailing spaces and outer blank lines, like the harness", () => {
    expect(normalizeOutput("\n a  \r\nb \n\n")).toBe("a\nb");
    expect(outputMatches("Shield up.\n", "Shield up.")).toBe(true);
    expect(outputMatches("Shield up", "Shield up.")).toBe(false);
  });
});

describe("mc", () => {
  it("grades the chosen index", () => {
    expect(gradeWithoutPython(mc, { type: "mc", choice: 1 })).toBe(true);
    expect(gradeWithoutPython(mc, { type: "mc", choice: 0 })).toBe(false);
    expect(gradeWithoutPython(mc, { type: "mc", choice: null })).toBe(false);
  });
});

describe("predict", () => {
  it("compares typed answers line by line, trimmed", () => {
    expect(predictCorrect(predictTyped, { choice: null, text: "  hi \n there\n\n" })).toBe(true);
    expect(predictCorrect(predictTyped, { choice: null, text: "hi there" })).toBe(false);
    expect(predictCorrect(predictTyped, { choice: null, text: "   " })).toBe(false);
  });

  it("grades a chosen choice", () => {
    expect(predictCorrect(predictChoices, { choice: 0, text: "" })).toBe(true);
    expect(predictCorrect(predictChoices, { choice: 1, text: "" })).toBe(false);
    expect(predictCorrect(predictChoices, { choice: null, text: "Next burst in 37 hours" })).toBe(false);
  });

  it("accepts the error's name or the word error for ERROR answers", () => {
    expect(predictCorrect(predictError, { choice: null, text: "NameError" })).toBe(true);
    expect(predictCorrect(predictError, { choice: null, text: "error" })).toBe(true);
    expect(predictCorrect(predictError, { choice: null, text: "TypeError" })).toBe(false);
    expect(predictCorrect(predictError, { choice: null, text: "x" })).toBe(false);
  });
});

describe("fill", () => {
  it("accepts the answer or an accepted spelling, trimmed", () => {
    expect(fillCorrect(fill, ' " " ')).toBe(true);
    expect(fillCorrect(fill, "' '")).toBe(true);
    expect(fillCorrect(fill, '""')).toBe(false);
    expect(fillCorrect(fill, "")).toBe(false);
  });
});

describe("parsons and bug", () => {
  it("passes the authored order without Python and asks for a run otherwise", () => {
    expect(gradeWithoutPython(parsons, { type: "parsons", order: ["print(1)", "print(2)", "print(3)"] })).toBe(true);
    expect(gradeWithoutPython(parsons, { type: "parsons", order: ["print(2)", "print(1)", "print(3)"] })).toBeNull();
    expect(gradeWithoutPython(parsons, { type: "parsons", order: [] })).toBe(false);
    expect(gradeWithoutPython(bug, { type: "bug", code: 'print("x")' })).toBeNull();
    expect(parsonsCode(["a", "b"])).toBe("a\nb\n");
    expect(parsonsCode([])).toBe("");
  });

  it("offers every line and distractor, shuffled the same way for the same attempt", () => {
    const first = parsonsBlocks(parsons, 0);
    expect([...first].sort()).toEqual([...parsons.lines, ...parsons.distractors].sort());
    expect(parsonsBlocks(parsons, 0)).toEqual(first);
  });
});

describe("seeded shuffle", () => {
  it("is deterministic and never leaves a movable list in order", () => {
    const items = ["a", "b", "c", "d"];
    for (let seed = 0; seed < 50; seed += 1) {
      const shuffled = seededShuffle(items, `s${seed}`);
      expect(shuffled).toEqual(seededShuffle(items, `s${seed}`));
      expect([...shuffled].sort()).toEqual(items);
      expect(shuffled).not.toEqual(items);
    }
    expect(seededShuffle(["x", "x"], "s")).toEqual(["x", "x"]);
    expect(seededShuffle([], "s")).toEqual([]);
  });
});

describe("responses", () => {
  it("starts empty (bug starts with the buggy code) and knows when there is an answer", () => {
    expect(hasAnswer(emptyResponse(mc))).toBe(false);
    expect(hasAnswer(emptyResponse(predictTyped))).toBe(false);
    expect(hasAnswer(emptyResponse(fill))).toBe(false);
    expect(hasAnswer(emptyResponse(parsons))).toBe(false);
    expect(emptyResponse(bug)).toEqual({ type: "bug", code: bug.code });
    expect(hasAnswer({ type: "predict", choice: null, text: "hi" })).toBe(true);
    expect(hasAnswer(undefined)).toBe(false);
  });

  it("turns answers into short text for the save", () => {
    expect(responseText(mc, { type: "mc", choice: 2 })).toBe("2");
    expect(responseText(predictChoices, { type: "predict", choice: 1, text: "" })).toBe("Next burst in hours hours");
    expect(responseText(parsons, { type: "parsons", order: ["a", "b"] })).toBe("a\nb");
  });

  it("scores as a whole percent", () => {
    expect(quizPercent(5, 6)).toBe(83);
    expect(quizPercent(0, 0)).toBe(0);
    expect(quizPercent(9, 6)).toBe(100);
  });
});
