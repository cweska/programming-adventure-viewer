import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { createElement } from "react";
import { renderToString } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { questionSchema, type Question } from "../../lib/course/schema";
import { PredictStep } from "./PredictStep";
import {
  choiceOrder,
  choiceSeed,
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

describe("choice order (course-wide: the display order is shuffled, the authored index is kept)", () => {
  it("is a steady shuffle of the authored indices: the same within an attempt, new on a retake", () => {
    for (let seed = 0; seed < 50; seed += 1) {
      const order = choiceOrder(4, choiceSeed(`student-${seed}`, "lists/lists-quiz/last-and-length", 0));
      expect([...order].sort()).toEqual([0, 1, 2, 3]);
      expect(order).toEqual(choiceOrder(4, choiceSeed(`student-${seed}`, "lists/lists-quiz/last-and-length", 0)));
    }
    const retakes = new Set([0, 1, 2, 3, 4, 5].map((attempt) => choiceOrder(4, choiceSeed("pell", "u/q/q-1", attempt)).join("")));
    expect(retakes.size).toBeGreaterThan(1);
    const students = new Set(["a", "b", "c", "d", "e", "f"].map((student) => choiceOrder(4, choiceSeed(student, "u/q/q-1")).join("")));
    expect(students.size).toBeGreaterThan(1);
    expect(choiceOrder(0, "s")).toEqual([]);
    expect(choiceOrder(1, "s")).toEqual([0]);
  });

  it("does not always show the right answer first, in any unit (Units 1 to 3 authored it first most of the time)", () => {
    const dir = path.join(process.cwd(), "content/courses/intro-python/units");
    type Raw = { kind: string; id: string; questions?: { id?: string; type: string; choices?: string[]; answer: unknown }[];
      exercises?: { id: string; predict?: { choices: string[]; answer: number } }[] };
    const STUDENTS = Array.from({ length: 16 }, (_, at) => `student-${at}`);
    let questions = 0;
    let firstAuthored = 0;
    let firstShown = 0;
    for (const file of readdirSync(dir).filter((name) => name.endsWith(".json") && !name.endsWith(".verify.json"))) {
      const unit = JSON.parse(readFileSync(path.join(dir, file), "utf8")) as { id: string; items: Raw[] };
      for (const item of unit.items) {
        const asked = [
          ...(item.questions ?? []).flatMap((question, at) => {
            const choices = question.choices ?? [];
            const answer = question.type === "mc" ? (question.answer as number) : choices.indexOf(String(question.answer));
            return choices.length >= 2 && answer >= 0 ? [{ where: `${unit.id}/${item.id}/${question.id ?? `q-${at + 1}`}`, count: choices.length, answer }] : [];
          }),
          ...(item.exercises ?? []).flatMap((exercise) =>
            exercise.predict ? [{ where: `${unit.id}/${item.id}/${exercise.id}:predict`, count: exercise.predict.choices.length, answer: exercise.predict.answer }] : [],
          ),
        ];
        for (const { where, count, answer } of asked) {
          questions += 1;
          if (answer === 0) firstAuthored += 1;
          const orders = STUDENTS.map((student) => choiceOrder(count, choiceSeed(student, where)));
          // For every question, some student sees the right answer somewhere other than first.
          expect(orders.some((order) => order[0] !== answer), where).toBe(true);
          firstShown += orders.filter((order) => order[0] === answer).length;
        }
      }
    }
    expect(questions).toBeGreaterThan(50);
    // Authored, the right answer comes first in a large share of the choice questions; shown, about 1 in 3 or fewer.
    expect(firstAuthored / questions).toBeGreaterThan(0.3);
    expect(firstShown / (questions * STUDENTS.length)).toBeLessThan(0.45);
  });

  it("keeps the authored index on every predict choice: the test ids, the saved guess and the right answer", () => {
    const html = renderToString(
      createElement(PredictStep, {
        predict: { q: "What prints?", choices: ["37", "36", "48"], answer: 0, explain: "The last gap." },
        editorCode: "",
        starter: "print(37)\n",
        glossary: [],
        saved: undefined,
        orderKey: "lists/many-values-one-name/first-is-zero",
        onAnswer: () => undefined,
        onClose: () => undefined,
      }),
    );
    // On the server (no student seed yet) the choices wait, hidden, so the order never jumps after loading.
    expect(html).toContain('data-ready="false"');
    for (const index of [0, 1, 2]) expect(html).toContain(`data-testid="predict-choice-${index}"`);
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
