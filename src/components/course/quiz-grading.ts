/**
 * Quiz grading for the Intro to Python course. Pure and client-safe.
 *
 *  - mc:       the chosen index equals `answer`.
 *  - predict:  a chosen choice, or typed text, matches `answer` line by line (each line trimmed, blank
 *              lines at the start and end ignored). An answer that starts "ERROR" accepts "error" or
 *              the error's name.
 *  - fill:     the typed blank, trimmed, equals `answer` or one of `accept`.
 *  - parsons:  the lines in the right order pass at once; any other order is run and passes when it
 *              prints `expectedOutput` (see outputMatches).
 *  - bug:      the edited code is run and passes when it prints `expectedOutput`.
 */
import type { Question } from "../../lib/course/schema";

export type QuizResponse =
  | { type: "mc"; choice: number | null }
  | { type: "predict"; choice: number | null; text: string }
  | { type: "fill"; text: string }
  | { type: "parsons"; order: string[] }
  | { type: "bug"; code: string };

/** Output compared like the prototype harness: trailing spaces and outer blank lines do not count. */
export function normalizeOutput(text: string): string {
  return String(text ?? "")
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.trimEnd())
    .join("\n")
    .trim();
}

/** Typed answers are kinder: every line is trimmed on both sides. */
export function normalizeTyped(text: string): string {
  return String(text ?? "")
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.trim())
    .join("\n")
    .trim();
}

/** Does a program's stdout match the expected output? */
export function outputMatches(stdout: string, expected: string): boolean {
  return normalizeOutput(stdout) === normalizeOutput(expected);
}

function errorAnswerMatches(answer: string, typed: string): boolean {
  const wanted = answer.match(/([A-Za-z]+Error)/)?.[1]?.toLowerCase();
  const said = typed.toLowerCase().replace(/\s+/g, "");
  if (!said.includes("error")) return false;
  return !wanted || said === "error" || said.includes(wanted);
}

export function predictCorrect(
  question: Extract<Question, { type: "predict" }>,
  response: { choice: number | null; text: string },
): boolean {
  if (question.choices && question.choices.length > 0) {
    if (response.choice === null) return false;
    const chosen = question.choices[response.choice];
    return chosen !== undefined && normalizeOutput(chosen) === normalizeOutput(question.answer);
  }
  const typed = normalizeTyped(response.text);
  if (!typed) return false;
  if (/^ERROR\b/i.test(question.answer.trim())) return errorAnswerMatches(question.answer, typed);
  return typed === normalizeTyped(question.answer);
}

export function fillCorrect(question: Extract<Question, { type: "fill" }>, text: string): boolean {
  const typed = text.trim();
  if (!typed) return false;
  return [question.answer, ...question.accept].some((answer) => answer.trim() === typed);
}

/** The parsons lines in exactly the authored order (no Python needed). */
export function parsonsInOrder(question: Extract<Question, { type: "parsons" }>, order: readonly string[]): boolean {
  return order.length === question.lines.length && order.every((line, index) => line === question.lines[index]);
}

/** The code a parsons answer runs. */
export function parsonsCode(order: readonly string[]): string {
  return order.length ? `${order.join("\n")}\n` : "";
}

/** Grade without running Python. Returns null for parsons/bug answers that need a run. */
export function gradeWithoutPython(question: Question, response: QuizResponse): boolean | null {
  switch (question.type) {
    case "mc":
      return response.type === "mc" && response.choice === question.answer;
    case "predict":
      return response.type === "predict" && predictCorrect(question, response);
    case "fill":
      return response.type === "fill" && fillCorrect(question, response.text);
    case "parsons":
      if (response.type !== "parsons" || response.order.length === 0) return false;
      return parsonsInOrder(question, response.order) ? true : null;
    case "bug":
      return null;
    default:
      return false;
  }
}

/** True when the student has given something to check. */
export function hasAnswer(response: QuizResponse | undefined): boolean {
  if (!response) return false;
  switch (response.type) {
    case "mc":
      return response.choice !== null;
    case "predict":
      return response.choice !== null || response.text.trim().length > 0;
    case "fill":
      return response.text.trim().length > 0;
    case "parsons":
      return response.order.length > 0;
    case "bug":
      return response.code.trim().length > 0;
    default:
      return false;
  }
}

export function emptyResponse(question: Question): QuizResponse {
  switch (question.type) {
    case "mc":
      return { type: "mc", choice: null };
    case "predict":
      return { type: "predict", choice: null, text: "" };
    case "fill":
      return { type: "fill", text: "" };
    case "parsons":
      return { type: "parsons", order: [] };
    case "bug":
      return { type: "bug", code: question.code };
  }
}

/** A short text version of an answer, for progress.lastAnswers. */
export function responseText(question: Question, response: QuizResponse): string {
  switch (response.type) {
    case "mc":
      return response.choice === null ? "" : String(response.choice);
    case "predict":
      if (response.choice !== null && question.type === "predict" && question.choices) {
        return question.choices[response.choice] ?? "";
      }
      return response.text;
    case "fill":
      return response.text;
    case "parsons":
      return response.order.join("\n");
    case "bug":
      return response.code;
    default:
      return "";
  }
}

export function quizPercent(correct: number, total: number): number {
  if (total <= 0) return 0;
  return Math.round((Math.max(0, Math.min(correct, total)) / total) * 100);
}

/* ------------------------------------------------------------------------------------------------ */
/* Deterministic shuffling (same seed, same order: server and client agree, retakes reshuffle)       */
/* ------------------------------------------------------------------------------------------------ */

function hashSeed(seed: string): number {
  let hash = 2166136261;
  for (let index = 0; index < seed.length; index += 1) {
    hash ^= seed.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function mulberry32(seed: number): () => number {
  let state = seed;
  return () => {
    state = (state + 0x6d2b79f5) | 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value = (value + Math.imul(value ^ (value >>> 7), 61 | value)) ^ value;
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Shuffle a copy of `items` with a seed. When the shuffle would leave the items in their original order
 * (and they can move), the copy is rotated by one so a puzzle never starts solved. `mayKeepOrder` drops that
 * rotation (a list of choices is no puzzle: every order, the authored one too, is equally likely).
 */
export function seededShuffle<T>(items: readonly T[], seed: string, options: { mayKeepOrder?: boolean } = {}): T[] {
  const copy = items.slice();
  const random = mulberry32(hashSeed(seed));
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(random() * (index + 1));
    [copy[index], copy[swap]] = [copy[swap], copy[index]];
  }
  const unchanged = copy.every((item, index) => item === items[index]);
  const canMove = new Set(items).size > 1;
  if (unchanged && canMove && !options.mayKeepOrder) copy.push(copy.shift() as T);
  return copy;
}

/**
 * The order to SHOW `count` choices in (course-wide, the teacher's ruling on the Unit 4 reviews: the right answer
 * was usually authored first). A seeded shuffle of the AUTHORED indices: grading, `answer`, why_wrong, the ✓ and ✗
 * marks and every `data-testid` keep the authored index; only the display order (and so the screen-reader order)
 * follows this. `seed` names the student, the unit, item and question, and the attempt (choiceSeed), so the order
 * holds steady within an attempt and changes on a retake.
 */
export function choiceOrder(count: number, seed: string): number[] {
  return seededShuffle(
    Array.from({ length: Math.max(0, count) }, (_, index) => index),
    seed,
    { mayKeepOrder: true },
  );
}

/**
 * How many of a Quick Check form's questions must be right, in words: "3 of the 4", or, when it is every one of them,
 * "both" (2) and "all 3". `of` is "of the" in a sentence about the questions ("get 3 of the 4 right"), "of these" in
 * one about the questions on screen.
 */
export function questionsNeeded(needed: number, total: number, of = "of the"): string {
  if (needed >= total && total === 2) return "both";
  if (needed >= total && total > 2) return `all ${total}`;
  return `${needed} ${of} ${total}`;
}

/** The seed for choiceOrder: this student (studentSeed), then where the choices are, then the attempt. */
export function choiceSeed(student: string, where: string, attempt = 0): string {
  return `${student}:${where}:${attempt}`;
}

/** The blocks a parsons question offers: its lines and distractors, shuffled for this attempt. */
export function parsonsBlocks(question: Extract<Question, { type: "parsons" }>, attempt: number): string[] {
  return seededShuffle([...question.lines, ...question.distractors], `${question.id}:${attempt}`);
}
