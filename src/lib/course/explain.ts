/**
 * Friendly error explanations for the Intro to Python course (contracts.ts ExplainCourseError).
 *
 * Wraps the campaign's explainPython() and adds plain-language help for the slips this class really
 * makes (the class diagnostic's "Class-wide patterns", kept out of the repo, and the "starting from
 * zero" review, docs/intro-to-python/design/reviews/curriculum-starting-from-zero.md §4.1): unquoted text,
 * unclosed or mismatched quotes, `def` used to make a variable, a dash instead of `=`, `5P + 2S`, a name
 * alone on a line, capital-letter and spelling mismatches, names copied from the worked example,
 * indentation, joining text and numbers, and more. Unit 2 (control flow) adds its own slips: a sign typed
 * backwards (`=>`), a `___` blank left in, a question alone on a line, unquoted options, `elif` / `else` out of
 * place, a number compared with text, one `=` inside print, `lower(answer)`, `randint` without `random.`, and
 * the student's own `assert` coming out False. Unit 3 (recipes) adds a recipe written the way math writes it
 * (`max_fuel_for(cells) = cells * 5`), an ingredient name in quotes (`def max_fuel_for("cells"):`), the wrong number
 * of values handed to a recipe (read from the student's own `def` line), `random.randint` with its numbers the wrong
 * way round, a recipe that calls itself, a store written backwards (`get_greeting = greeting`), a `return` of a name
 * the recipe never makes (`return result`, even when it is the example's name), a box from another recipe's kitchen,
 * one of the task's recipes made like a box (`max_fuel_for = cells * 5`, `def max_fuel_for = ...`, a box called with
 * `( )`, `def max_fuel_for(cells) = cells * 5`, `def ("say_steady"):`), a name like one of the recipe's ingredients
 * (`hero` for `hero_name`), a recipe with no step yet, a name copied from a hint's Teach me example (`get_note`), and,
 * for every unit, unquoted words inside a call that takes several values (`heal(Moth Queen, 5)`: only the bare run of
 * words is quoted). Unit 4 (lists) adds round brackets where a list needs square ones (`chalk_wall(2) = 47`,
 * `wall(0)`), square brackets after a tool that is called (`chalk_wall.append[33]`, `max[chalk_wall]`,
 * `range[1, 9]`), a comma between two positions (`roster[2, 0]`), one item joined to a list with `+`
 * (`chalk_wall + 33`), `sorted` (or `max`, `min`, `sum`, `len`) written after a dot, unquoted words and a missing
 * comma inside `[ ]`, and `.remove()` handed a value the list does not hold.
 *
 * ExplainContext sets how much it says: `unitOrder` keeps advice to what the class has met (no "make it with
 * def" before the Functions unit, no list tools before the Lists unit), `explainer: "lean"` names the kind of slip and the line but never the fix,
 * and `debugging` leaves the "One fixed!" prefix to the player's own progress line.
 *
 * Every explanation has a stable `kind` (for tests, logging and the player), and says what happened and
 * what to try, in short sentences, with the line number when Python gives one. When it can, it shows the
 * student's own line, fixed. `code` is the student's code (used to find the line and close names); it
 * never leaves the browser.
 *
 * explainQuietSlip() covers the slips that raise NO error at all (a lone "text" line, a name alone on a
 * line, `mana - 20`): grading.ts uses it when a run passes Python but fails a checkpoint.
 */
import { explainPython } from "../languages/python/explain";
import type { Explanation } from "../languages/types";

/** What an explanation is about. Stable ids: tests, logging and the player may rely on them. */
export type CourseErrorKind =
  // quotes and text
  | "missing-quote"
  | "quotes-dont-match"
  | "apostrophe"
  | "unclosed-triple-quote"
  | "curly-quote"
  | "hidden-character"
  | "odd-character"
  | "unquoted-words"
  | "unquoted-word"
  // making a variable
  | "def-for-variable"
  | "dash-for-equals"
  | "dash-and-quote"
  | "colon-for-equals"
  | "name-goes-first"
  | "quoted-name"
  | "name-starts-with-number"
  | "number-stuck-to-name"
  | "space-in-name"
  | "dash-in-name"
  // names
  | "lone-name"
  | "example-name"
  | "capital-letters"
  | "spelling"
  | "make-it-first"
  | "not-made-yet"
  | "used-too-early"
  | "unknown-function"
  | "unknown-name"
  | "missing-import"
  // brackets, commas, colons and indents
  | "never-closed"
  | "extra-bracket"
  | "brackets-dont-match"
  | "missing-comma"
  | "two-single-quotes"
  | "missing-comma-in-list"
  | "print-needs-brackets"
  | "compare-with-double-equals"
  | "def-needs-brackets"
  | "missing-colon"
  | "indent"
  | "cant-read-line"
  // questions and choices (Unit 2)
  | "sign-backwards"
  | "blank-left"
  | "comparison-alone"
  | "unquoted-option"
  | "else-not-last"
  | "elif-without-if"
  | "else-not-lined-up"
  | "elif-spelling"
  | "else-has-question"
  | "no-question"
  | "keyword-capital"
  | "compare-number-text"
  | "equals-in-print"
  | "method-as-function"
  | "randint-needs-random"
  | "assert-failed"
  // recipes (Unit 3)
  | "recipe-like-math"
  | "quoted-ingredient"
  | "randint-backwards"
  | "recipe-not-made-yet"
  | "recipe-called-too-early"
  | "made-inside-recipe"
  | "not-in-recipe"
  | "store-backwards"
  | "quoted-recipe-name"
  // lists (Unit 4)
  | "list-needs-square-brackets"
  | "call-needs-round-brackets"
  | "comma-in-brackets"
  | "list-plus-item"
  | "tool-after-dot"
  | "not-on-the-list"
  | "read-from-none"
  | "row-not-item"
  // values
  | "input-is-text"
  | "text-plus-number"
  | "number-plus-text"
  | "math-with-text"
  | "number-in-quotes"
  | "bar-needs-brackets"
  | "name-taken"
  | "use-star-to-multiply"
  | "not-a-function"
  | "wrong-number-of-values"
  | "wrong-kind-of-value"
  | "divide-by-zero"
  | "out-of-answers"
  | "not-a-number"
  | "nothing-at-position"
  | "missing-key"
  | "attribute-spelling"
  | "no-such-module"
  | "never-ending-calls"
  | "variable-in-function"
  // runs that never finish
  | "timeout"
  | "too-much-output"
  // code that runs without an error but does nothing (explainQuietSlip)
  | "bare-value"
  | "bare-name"
  | "dash-no-effect"
  | "print-without-brackets"
  // anything else
  | "player-message"
  | "other";

export type CourseExplanation = Explanation & {
  kind: CourseErrorKind;
  /**
   * This run got further than the previous one (`ExplainContext.previous`): the error moved to a later line, or
   * the line it stopped on before now reads (or now fails another way). One slip was mended.
   */
  gotFurther?: boolean;
  /** "lean" when the fix was left out on purpose (ExplainContext.explainer). */
  explainer?: "full" | "lean";
};

/** The line a debugging exercise shows when a run gets further than the one before (ExercisePlayer). */
export const GOT_FURTHER_LINE = "Python got further: that slip is mended.";

/** The prefix an ordinary exercise's explanation gets when a run gets further than the one before. */
export const ONE_FIXED_PREFIX = "One fixed! Python found the next one.";

/** Unit 3 ("First Recipes") teaches `def`: before it, the explainer never says "make it with def". */
export const FUNCTIONS_UNIT_ORDER = 3;

/** Unit 2 ("Control Flow") teaches `random.randint`. */
export const RANDOM_UNIT_ORDER = 2;

/**
 * Unit 4 ("Lists") teaches lists: square brackets for a position, `.append()`, `+` between two lists, slices, and
 * the list tools (`sorted`, `max`, `.remove()`, `in`). Its rows name them; before it the older advice is unchanged.
 */
export const LISTS_UNIT_ORDER = 4;

/** What the player knows about the exercise. Every field is optional; more context gives more exact help. */
export type ExplainContext = {
  /** The worked example's code: a name copied from it gets "this name is from the example". */
  example?: string;
  /** The names the task asks for (the exercise's "Names to use"). */
  names?: readonly string[];
  /**
   * The previous run's traceback, when that run crashed too. A later error after it (or a line that now
   * parses) reads "One fixed! Python found the next one." (Python stops at the first error, so fixes come
   * one at a time.)
   */
  previous?: string;
  /**
   * Mar'tu's version of the exercise. A task whose version makes no variable and only prints is a
   * print-only task (Lesson 1A, before boxes are taught): there `def`, a dash and a bare value get "use
   * print" advice, never "make a variable". It also says whether `mana - 3` should be `mana = mana - 3`.
   */
  solution?: string;
  /**
   * The unit's `order` on the course map. Before the Functions unit (FUNCTIONS_UNIT_ORDER) no advice says
   * "make it with def"; in Unit 1 (before comparisons) `print(x = 1)` gets box advice, not `==`. From Unit 2
   * (RANDOM_UNIT_ORDER) `randint` the wrong way round is named; from Unit 3 the recipe rows speak the unit's words
   * (recipe, ingredient, hand over); from Unit 4 (LISTS_UNIT_ORDER) the list rows name square brackets, `.append()`
   * and the list tools. Without a unit, those rows stay closed and the older advice is unchanged.
   */
  unitOrder?: number;
  /**
   * A debugging exercise (a Broken spell: "Mend line 3 ..."). A run that got further is marked `gotFurther`
   * with no "One fixed!" prefix in the hint: the player shows its own line, GOT_FURTHER_LINE, instead.
   */
  debugging?: boolean;
  /**
   * The exercise's `explainer` field. "lean" (Unit 2's SOLO items and Quick Check 2, by the teacher's ruling):
   * the explanation names the kind of slip and the line, and leaves out the fix. Python's own last line stays
   * on screen (the player shows it under every explanation).
   */
  explainer?: "full" | "lean";
  /**
   * Names from Mar'tu's Teach me examples in the exercise's hints (`note = get_note()`), that the task itself never
   * uses (foreignNames() works them out). From Unit 3 on, a name copied from one gets the worked example's row.
   */
  foreign?: readonly string[];
};

/**
 * The class has met what unit `order` teaches: the context names that unit or a later one. The rows a unit adds
 * (Unit 3's recipes, Unit 2's random) need it; without a unit (an old caller) the advice is unchanged.
 */
function unitAtLeast(context: ExplainContext | undefined, order: number): boolean {
  return context?.unitOrder !== undefined && context.unitOrder >= order;
}

/** The task only shows words: Mar'tu's version prints and makes no variable (nothing about boxes yet). */
export function isPrintOnlyTask(context: ExplainContext | undefined): boolean {
  return printOnlyTask(context);
}

function printOnlyTask(context: ExplainContext | undefined): boolean {
  const solution = context?.solution;
  if (solution === undefined || !/(^|[^\w.])print\s*\(/.test(solution)) return false;
  if ((context?.names ?? []).some((name) => name !== "print")) return false;
  return definedNames(solution).length === 0;
}

/** `print("words")` for a print-only task: the student's own text when the line has some, else "your words". */
function printFix(text: string): string {
  const literal = codePart(text).match(/(["'])((?:(?!\1)[^\\]|\\.)*)\1/);
  if (literal && literal[2].trim()) return `print(${literal[0]})`;
  return 'print("your words")';
}

type Parsed = { type: string; message: string };

const EXCEPTION_LINE = /^([A-Za-z_][A-Za-z0-9_.]*)(?::\s?(.*))?$/;

/** The last "Type: message" line of a traceback. */
function lastException(raw: string): Parsed | null {
  const lines = raw
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.trim().length > 0);
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    const line = lines[index];
    if (/^\s/.test(line) || line.startsWith("Traceback (most recent call last)")) continue;
    const match = line.match(EXCEPTION_LINE);
    if (!match) continue;
    const type = match[1].split(".").pop() ?? match[1];
    if (!/(Error|Exception|Exit|Interrupt|Warning|Output|Iteration)$/.test(type) && match[2] === undefined) continue;
    return { type, message: (match[2] ?? "").trim() };
  }
  return null;
}

/**
 * The student's line number: the last `File "main.py", line N`. Only when there is none, the last `<exec>`
 * frame (in a Pyodide course run `<exec>` is the course helpers, not the student), then any non-library file.
 */
function errorLine(raw: string): number | null {
  const frames = [...raw.matchAll(/File "([^"]+)", line (\d+)/g)];
  if (frames.length === 0) return null;
  const main = frames.filter((frame) => frame[1] === "main.py");
  const exec = frames.filter((frame) => frame[1] === "<exec>");
  const pick = (main.length > 0 ? main : exec.length > 0 ? exec : frames.filter((frame) => !frame[1].startsWith("/"))).at(-1);
  return pick ? Number(pick[2]) : null;
}

function sourceLine(code: string, line: number | null): string {
  if (!line) return "";
  return (code ?? "").split("\n")[line - 1] ?? "";
}

function onLine(line: number | null): string {
  return line ? ` on line ${line}` : "";
}

function lineWord(line: number | null): string {
  return line ? `Line ${line}` : "This line";
}

function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* ---------------------------------------------------------------------------------------------- */
/* Reading one line: strings, comments and brackets                                               */
/* ---------------------------------------------------------------------------------------------- */

const CLOSER: Record<string, string> = { "(": ")", "[": "]", "{": "}" };
const OPENER: Record<string, string> = { ")": "(", "]": "[", "}": "{" };

type LineScan = {
  /** A string that starts on this line and never ends on it. */
  unterminated: { start: number; quote: string } | null;
  /** Brackets still open at the end of the line (outside strings), outermost first. */
  open: string[];
  /** Where a # comment starts (outside strings), or -1. */
  comment: number;
};

/** Walk one line the way Python reads it: strings (with escapes and triple quotes), comments, brackets. */
function scanLine(text: string, startOpen: readonly string[] = []): LineScan {
  const open = [...startOpen];
  let index = 0;
  while (index < text.length) {
    const char = text[index];
    if (char === "#") return { unterminated: null, open, comment: index };
    if (char === '"' || char === "'") {
      const quote = text.startsWith(char.repeat(3), index) ? char.repeat(3) : char;
      let at = index + quote.length;
      let closed = -1;
      while (at < text.length) {
        if (text[at] === "\\") {
          at += 2;
          continue;
        }
        if (text.startsWith(quote, at)) {
          closed = at;
          break;
        }
        at += 1;
      }
      if (closed < 0) return { unterminated: { start: index, quote }, open, comment: -1 };
      index = closed + quote.length;
      continue;
    }
    if (char in CLOSER) open.push(char);
    else if (char in OPENER && open.length > 0 && open[open.length - 1] === OPENER[char]) open.pop();
    index += 1;
  }
  return { unterminated: null, open, comment: -1 };
}

/** The line without its # comment and trailing spaces. */
function codePart(text: string): string {
  const scan = scanLine(text);
  return (scan.comment >= 0 ? text.slice(0, scan.comment) : text).trimEnd();
}

/**
 * The line with the inside of every string turned to spaces and any # comment cut off, so a sign or a word
 * inside text is never read as code. Every character keeps its place: a match in the mask is at the same
 * index in the line.
 */
function maskStrings(text: string): string {
  let out = "";
  let index = 0;
  while (index < text.length) {
    const char = text[index];
    if (char === "#") break;
    if (char === '"' || char === "'") {
      const quote = text.startsWith(char.repeat(3), index) ? char.repeat(3) : char;
      let at = index + quote.length;
      let closed = -1;
      while (at < text.length) {
        if (text[at] === "\\") {
          at += 2;
          continue;
        }
        if (text.startsWith(quote, at)) {
          closed = at;
          break;
        }
        at += 1;
      }
      const end = closed < 0 ? text.length : closed + quote.length;
      const inside = Math.max(0, (closed < 0 ? text.length : closed) - index - quote.length);
      out += quote + " ".repeat(inside) + (closed < 0 ? "" : quote);
      index = end;
      continue;
    }
    out += char;
    index += 1;
  }
  return out.trimEnd();
}

/** Indices in `mask` of `=` signs that are a single `=` (not `==`, `<=`, `>=`, `!=`, `+=` ...), outside brackets. */
function singleEquals(mask: string): number[] {
  const found: number[] = [];
  let depth = 0;
  for (let index = 0; index < mask.length; index += 1) {
    const char = mask[index];
    if (char in CLOSER) depth += 1;
    else if (char in OPENER) depth = Math.max(0, depth - 1);
    else if (char === "=" && depth === 0) {
      const before = mask[index - 1] ?? "";
      const after = mask[index + 1] ?? "";
      if (after === "=" || /[=<>!+\-*/%:]/.test(before)) {
        if (after === "=") index += 1;
        continue;
      }
      found.push(index);
    }
  }
  return found;
}

/** The leading spaces of a line, as a count (a tab counts as 4, the way the editor shows it). */
function indentOf(text: string): number {
  const lead = text.match(/^[ \t]*/)?.[0] ?? "";
  return lead.replace(/\t/g, "    ").length;
}

/** Brackets still open after lines 1 .. line-1 (a list or dictionary that goes on over several lines). */
function openBefore(code: string, line: number | null): string[] {
  if (!line) return [];
  let open: string[] = [];
  for (const text of (code ?? "").split("\n").slice(0, line - 1)) {
    const scan = scanLine(text, open);
    if (scan.unterminated) return [];
    open = scan.open;
  }
  return open;
}

function closersFor(open: readonly string[]): string {
  return [...open].reverse().map((bracket) => CLOSER[bracket]).join("");
}

/**
 * Close a string that never ends: `print("Hi)` -> `print("Hi")`. The brackets the student typed at the
 * end belong after the quote; brackets that were never typed are added after them.
 */
function closeQuoteLine(text: string, start: number, quote: string): { fixed: string; added: string } {
  const before = text.slice(0, start);
  const open = scanLine(before).open;
  let tail = text.slice(start + quote.length).replace(/\s+$/, "");
  const run = tail.match(/[)\]}\s]*$/)?.[0] ?? "";
  const typed = run.replace(/\s+/g, "");
  let kept = 0;
  for (let count = Math.min(typed.length, open.length); count > 0; count -= 1) {
    const candidate = typed.slice(typed.length - count);
    const fits = [...candidate].every((closer, index) => CLOSER[open[open.length - 1 - index]] === closer);
    if (fits) {
      kept = count;
      break;
    }
  }
  let closers = "";
  if (kept > 0) {
    closers = typed.slice(typed.length - kept);
    let removed = 0;
    let cut = tail.length;
    while (removed < kept && cut > 0) {
      cut -= 1;
      if (!/\s/.test(tail[cut])) removed += 1;
    }
    tail = tail.slice(0, cut).replace(/\s+$/, "");
  }
  const added = closersFor(open.slice(0, open.length - kept));
  return { fixed: `${before}${quote}${tail}${quote}${closers}${added}`, added };
}

/* ---------------------------------------------------------------------------------------------- */
/* Names in the student's code                                                                     */
/* ---------------------------------------------------------------------------------------------- */

const COMMON_BUILTINS = [
  "print", "input", "len", "str", "int", "float", "bool", "range", "list", "dict", "tuple", "set", "type",
  "round", "sum", "min", "max", "abs", "sorted", "reversed", "enumerate", "zip", "map", "filter", "True",
  "False", "None", "random", "math",
];

const KEYWORDS = new Set([
  "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del",
  "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
  "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
]);

type Definition = { name: string; line: number };

/** Names the code makes (variables, functions, parameters, loop variables, imports), with their line. */
export function definedNames(code: string): Definition[] {
  const found: Definition[] = [];
  const add = (names: string, line: number) => {
    for (const piece of names.split(",")) {
      const name = piece.trim().split(/[\s:=]/)[0]?.replace(/^\*+/, "");
      if (name && /^[A-Za-z_]\w*$/.test(name)) found.push({ name, line });
    }
  };
  (code ?? "").split("\n").forEach((text, index) => {
    const line = index + 1;
    let match = text.match(/^\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*(?:\+|-|\*|\/|\/\/|%|\*\*)?=(?!=)/);
    if (match) add(match[1], line);
    match = text.match(/^\s*def\s+([A-Za-z_]\w*)\s*\(([^)]*)\)?/);
    if (match) {
      add(match[1], line);
      add(match[2] ?? "", line);
    }
    match = text.match(/^\s*class\s+([A-Za-z_]\w*)/);
    if (match) add(match[1], line);
    match = text.match(/^\s*for\s+(.+?)\s+in\b/);
    if (match) add(match[1].replace(/[()]/g, ""), line);
    match = text.match(/^\s*import\s+(.+)$/);
    if (match) {
      for (const part of match[1].split(",")) {
        const alias = part.match(/\bas\s+(\w+)/);
        add(alias ? alias[1] : (part.trim().split(".")[0] ?? ""), line);
      }
    }
    match = text.match(/^\s*from\s+[\w.]+\s+import\s+(.+)$/);
    if (match) add(match[1].replace(/[()]/g, "").replace(/\b\w+\s+as\s+/g, ""), line);
    for (const as of text.matchAll(/\bas\s+([A-Za-z_]\w*)/g)) {
      if (/^\s*(with|except)\b/.test(text)) add(as[1], line);
    }
  });
  return found;
}

function editDistance(a: string, b: string): number {
  const row = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let i = 1; i <= a.length; i += 1) {
    let previous = row[0];
    row[0] = i;
    for (let j = 1; j <= b.length; j += 1) {
      const saved = row[j];
      row[j] = Math.min(row[j] + 1, row[j - 1] + 1, previous + (a[i - 1] === b[j - 1] ? 0 : 1));
      previous = saved;
    }
  }
  return row[b.length];
}

/**
 * The closest name the student probably meant: the same letters in a different case first, then a close
 * spelling (up to 2 letters off for longer names; pass `limit` to be stricter).
 */
export function closeName(wrong: string, candidates: string[], limit = wrong.length >= 5 ? 2 : 1): string | null {
  const unique = [...new Set(candidates)].filter((name) => name !== wrong && !name.startsWith("_"));
  const sameLetters = unique.find((name) => name.toLowerCase() === wrong.toLowerCase());
  if (sameLetters) return sameLetters;
  let best: string | null = null;
  let bestDistance = limit + 1;
  for (const name of unique) {
    if (Math.abs(name.length - wrong.length) > limit) continue;
    const distance = editDistance(wrong.toLowerCase(), name.toLowerCase());
    if (distance < bestDistance) {
      best = name;
      bestDistance = distance;
    }
  }
  return best;
}

/** Modules: a near name never suggests one (`moth` is not `math`); an import makes it a name the code made. */
const MODULES = new Set(["random", "math"]);

/**
 * Python's own names a "Did you mean" may offer: `print`, and the others this student has met here (in the
 * task's names, the example, Mar'tu's version or their own code). Without context, the common ones.
 */
function suggestableBuiltins(code: string, context?: ExplainContext): string[] {
  const all = COMMON_BUILTINS.filter((name) => !MODULES.has(name));
  if (!context) return all;
  const seen = [code ?? "", context.example ?? "", context.solution ?? ""].join("\n");
  return all.filter(
    (name) =>
      name === "print" ||
      (context.names ?? []).includes(name) ||
      new RegExp(/^[A-Z]/.test(name) ? `\\b${name}\\b` : `(^|[^\\w.])${name}\\s*\\(`).test(seen),
  );
}

/**
 * `Character = "Kratos"` then `print(character)`, in a task whose box is `character`: the line to change is
 * the one that MADE the box, not the one that uses it. Says which spelling is the task's, so the advice never
 * sends the student to the name the step check rejects. Null when the task's names do not settle it.
 */
function nameAgainstTask(
  name: string,
  close: string,
  code: string,
  line: number | null,
  defined: Definition[],
  context: ExplainContext | undefined,
  raw: string,
): CourseExplanation | null {
  const task = context?.names ?? [];
  const made = defined.find((entry) => entry.name === close);
  if (task.length === 0 || !made) return null;
  const sameLetters = close.toLowerCase() === name.toLowerCase();
  const kind = sameLetters ? "capital-letters" : "spelling";
  const title = sameLetters ? "Capital letters matter" : "Check the spelling";
  const differ = sameLetters
    ? "Python sees them as two different names, because the capital letters differ."
    : "Python sees them as two different names.";
  const here = line ? `line ${line}` : "this line";
  if (task.includes(name) && !task.includes(close)) {
    const madeText = codePart(sourceLine(code, made.line)).trim();
    const renamed = madeText.replace(new RegExp(`^${escapeRegExp(close)}(?![\\w])`), name);
    const fix = renamed !== madeText ? `Rename it on line ${made.line}: \`${renamed}\`` : `Rename it to \`${name}\` on line ${made.line}.`;
    return explain(kind, title, `Line ${made.line} makes \`${close}\`, but this task's box is \`${name}\`. ${differ} ${fix}`, raw);
  }
  if (task.includes(close) && !task.includes(name)) {
    return explain(
      kind,
      title,
      `${here[0].toUpperCase()}${here.slice(1)} uses \`${name}\`, but this task's box is \`${close}\`. ${differ} Write \`${close}\` on ${here}, spelled exactly the same.`,
      raw,
    );
  }
  if (!sameLetters) return null;
  return explain(
    kind,
    title,
    `Line ${made.line} makes \`${close}\` and ${here} uses \`${name}\`. Python sees them as two different names. Make both lines match, with the same capital letters every time.`,
    raw,
  );
}

/** Names the code makes before `line` (all of them when the line is unknown). */
function namesBefore(code: string, line: number | null): string[] {
  const names = definedNames(code)
    .filter((entry) => line === null || entry.line < line)
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith("_"));
  return [...new Set(names)];
}

/**
 * Names the worked example makes, that the task does not use. From Unit 3 on, also the names from the hints' Teach me
 * examples (`context.foreign`): a student who copies `get_note` from a hint gets the same help as one who copies
 * the example's `result`.
 */
function exampleOnlyNames(context: ExplainContext | undefined): string[] {
  const task = new Set(context?.names ?? []);
  const made = context?.example ? definedNames(context.example).map((entry) => entry.name) : [];
  const taught = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? (context?.foreign ?? []) : [];
  return [...new Set([...made, ...taught])].filter((name) => !task.has(name));
}

/** Every name a piece of code reads, makes or calls (not Python's words, not the text inside quotes). */
function identifiersIn(code: string): string[] {
  const names = new Set<string>();
  for (const row of (code ?? "").split("\n")) {
    for (const match of maskStrings(row).matchAll(/(?<![\w.])([A-Za-z_]\w*)/g)) {
      if (!KEYWORDS.has(match[1])) names.add(match[1]);
    }
  }
  return [...names];
}

/**
 * The names Mar'tu's Teach me examples use (the code spans of the hints: `note = get_note()`, `mix(2, 9)`) that the
 * task itself never does: not in its names, Mar'tu's version or the starter, and not one of Python's own. The player
 * passes them as ExplainContext.foreign.
 */
export function foreignNames(exercise: {
  hints: readonly string[];
  solution?: string;
  starter?: string;
  names?: readonly string[];
}): string[] {
  const own = new Set([
    ...identifiersIn(exercise.solution ?? ""),
    ...identifiersIn(exercise.starter ?? ""),
    ...(exercise.names ?? []),
    ...COMMON_BUILTINS,
  ]);
  const found = new Set<string>();
  for (const hint of exercise.hints) {
    const plain = hint.replace(/```[\s\S]*?```/g, " ");
    for (const span of plain.matchAll(/`([^`\n]+)`/g)) {
      // Only a span that is code (`note = get_note()`, `cups * 10`, `line.lower()`): a lone word or a few words
      // (`Steady`, `Sit down, lucky.`) may be words to show.
      const mask = maskStrings(span[1]);
      if (!/[(=*+/\-[]|\.[A-Za-z_]/.test(mask)) continue;
      const words = [...mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)\s+(?=([A-Za-z_]\w*))/g)];
      if (words.some((pair) => !KEYWORDS.has(pair[1]) && !KEYWORDS.has(pair[2]))) continue;
      for (const name of identifiersIn(span[1])) if (!own.has(name) && !name.startsWith("_")) found.add(name);
    }
  }
  return [...found];
}

/** The names to offer instead of an example's name: the task's names, else the ones the code made. */
function taskNamesInstead(code: string, line: number | null, context: ExplainContext | undefined, skip: string[] = []): string[] {
  const fromExample = new Set(exampleOnlyNames(context));
  const task = (context?.names ?? []).filter((name) => !fromExample.has(name) && !skip.includes(name));
  if (task.length > 0) return [...new Set(task)];
  return namesBefore(code, line).filter((name) => !fromExample.has(name) && !skip.includes(name));
}

/** "`traveler` is the name from the example. This task uses `name` ..." */
function exampleNameHint(name: string, use: string[]): string {
  if (use.length === 1) return `${name} is the name from the example. This task uses ${use[0]}, so write ${use[0]} here.`;
  if (use.length > 1) return `${name} is the name from the example. This task uses its own names: ${use.join(", ")}.`;
  return `${name} is the name from the example. Make your own variable first, with the name the task asks for.`;
}

/* ---------------------------------------------------------------------------------------------- */
/* The slips                                                                                       */
/* ---------------------------------------------------------------------------------------------- */

function explain(kind: CourseErrorKind, title: string, hint: string, raw: string): CourseExplanation {
  return { title, hint, raw, kind };
}

/** `name - "value"` (a dash where `=` belongs): returns `name = "value"`. */
function dashFix(text: string, name?: string): string | null {
  const who = name ? escapeRegExp(name) : "[A-Za-z_]\\w*";
  const match = codePart(text).match(new RegExp(`^\\s*(${who})\\s*-(?!=)\\s*(.+?)\\s*$`));
  if (!match || /=/.test(match[2])) return null;
  return `${match[1]} = ${match[2]}`;
}

/**
 * `magical affinity = 9` or `magical-affinity = 9`: a name with a space or a dash, on the left of `=`.
 * Python says "invalid syntax" or "Maybe you meant '=='", neither of which helps a beginner.
 */
function explainNameShape(text: string, line: number | null, raw: string): CourseExplanation | null {
  const match = codePart(text).match(/^(\s*)([A-Za-z_]\w*(?:(?:\s+|\s*-\s*)[A-Za-z_]\w*)+)\s*=(?!=)\s*(.+?)\s*$/);
  if (!match) return null;
  const words = match[2].split(/\s*-\s*|\s+/);
  // `if mana = 5:` or `def x = 1` are other slips with their own advice.
  if (words.some((word) => KEYWORDS.has(word) || word === "print") || /:\s*$/.test(match[3])) return null;
  const fixed = `${words.join("_")} = ${match[3]}`;
  if (match[2].includes("-")) {
    return explain(
      "dash-in-name",
      "No dashes in names",
      `A name can't have a dash -${onLine(line)}. Python reads - as minus. Join the words with _ instead: ${fixed}`,
      raw,
    );
  }
  return explain(
    "space-in-name",
    "No spaces in names",
    `A name can't have spaces${onLine(line)}. Python reads ${words.join(" and ")} as separate names. Join the words with _ instead: ${fixed}`,
    raw,
  );
}

/**
 * `bar = full * mana + empty * max_mana - mana`: Python does `*` before `-`, so the text is stamped first and
 * the subtraction then hits text. Returns the line with brackets around the subtraction, or null.
 */
function barBrackets(text: string): string | null {
  const body = codePart(text).trim();
  const operand = String.raw`(?:[A-Za-z_]\w*|\d+)`;
  const textFirst = new RegExp(String.raw`((?:"[^"]*"|'[^']*'|[A-Za-z_]\w*)\s*\*\s*)(${operand}\s*-\s*${operand})(?![\w(])`);
  if (textFirst.test(body)) return body.replace(textFirst, "$1($2)");
  const countFirst = new RegExp(String.raw`(?<![\w)])(${operand}\s*-\s*${operand})(\s*\*\s*(?:"[^"]*"|'[^']*'|[A-Za-z_]\w*))`);
  if (countFirst.test(body)) return body.replace(countFirst, "($1)$2");
  return null;
}

const JOIN_CALLS = /^(str|int|float|len|round|input|abs|max|min|sum)\s*\(/;

/**
 * `print("Welcome, + name)`: text whose closing quote was forgotten before a `+` (or a `,`) that joins it to a
 * variable. Returns the line with the quote put back, `print("Welcome, " + name)`, or null.
 */
function closeTextBeforeJoin(text: string, names: string[]): string | null {
  let from = 0;
  while (from < text.length) {
    const open = text.slice(from).search(/["']/);
    if (open < 0) return null;
    const start = from + open;
    const quote = text[start];
    const close = text.indexOf(quote, start + 1);
    for (let at = start + 1; at < text.length; at += 1) {
      if (close >= 0 && at > close) break;
      const mark = text[at];
      if (mark !== "+" && mark !== ",") continue;
      const after = text.slice(at + 1).trimStart();
      const next = after.match(/^[A-Za-z_]\w*/)?.[0];
      if (!next) continue;
      const joins = names.includes(next) || (mark === "+" && JOIN_CALLS.test(after));
      if (!joins) continue;
      const words = text.slice(start + 1, at);
      if (!words.trim()) return null;
      const glue = mark === "+" ? " + " : ", ";
      return `${text.slice(0, start + 1)}${mark === "," ? words.trimEnd() : words}${quote}${glue}${after}`.trim();
    }
    if (close < 0) return null;
    from = close + 1;
  }
  return null;
}

function quotesProblem(text: string, line: number | null, raw: string, code = "", context?: ExplainContext): CourseExplanation {
  const joined = closeTextBeforeJoin(text, namesBefore(code, line));
  if (joined) {
    return explain(
      "missing-quote",
      "Missing quote",
      `The text${onLine(line)} is missing its closing quote, so Python reads the rest of the line as text too. Close the text before you join it: ${joined}`,
      raw,
    );
  }
  const bad = text ? scanLine(text).unterminated : null;
  if (bad && bad.quote.length === 1) {
    const { start, quote } = bad;
    const other = quote === '"' ? "'" : '"';
    const tail = text.slice(start + 1);
    // `print('It's fun')`: the apostrophe ended the text early, and the last quote opened a new one.
    if (quote === "'" && /[A-Za-z]'[A-Za-z]/.test(text)) {
      const first = text.indexOf("'");
      const words = text.slice(first + 1, text.lastIndexOf("'")).trim();
      return explain(
        "apostrophe",
        "Apostrophe in text",
        `The ' inside your text${onLine(line)} ends the text too early. Put double quotes around text that has an apostrophe, like "${words || "It's fun"}".`,
        raw,
      );
    }
    // `print("fireball')`: one kind of quote at the start, the other kind at the end. The other kind only
    // ENDS the text when no word follows it: in `print("Hi. It is me, Mar'tu.)` or `"the guards' post)` it is
    // an apostrophe, and the slip is the missing closing quote (below), not a mismatch.
    const lastOther = tail.lastIndexOf(other);
    const endsText = lastOther >= 0 && !/^\s*\w/.test(tail.slice(lastOther + 1));
    if (!tail.includes(quote) && endsText) {
      const words = tail.slice(0, lastOther);
      return explain(
        "quotes-dont-match",
        "Quotes don't match",
        `The text${onLine(line)} starts with ${quote} but ends with ${other}. Use the same kind of quote at both ends, like ${quote}${words}${quote}.`,
        raw,
      );
    }
    // `print(Fireball")`: the quote that is there closes the words, so the OPENING quote is the missing one.
    const unopened = text.slice(0, start).match(/^(.*[(=,+]\s*)([A-Za-z][^"'()=+,]*)$/);
    if (unopened && tail.replace(/[)\]}\s]/g, "").length === 0) {
      const fixed = `${unopened[1]}${quote}${unopened[2]}${quote}${tail.trim()}`;
      return explain(
        "missing-quote",
        "Missing quote",
        `The text${onLine(line)} is missing its opening quote. Text needs a quote at the start and at the end, like this: ${fixed}`,
        raw,
      );
    }
    if (tail.replace(/[)\]}\s]/g, "").length > 0) {
      const { fixed, added } = closeQuoteLine(text, start, quote);
      const defFix = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) && RECIPE_HEADER.test(codePart(fixed)) ? null : defForVariable(fixed);
      if (defFix && printOnlyTask(context)) return defInPrintTask(fixed, raw, true);
      if (defFix && unitAtLeast(context, FUNCTIONS_UNIT_ORDER)) {
        return explain(
          "def-for-variable",
          "def makes recipes",
          `\`def\` makes recipes (functions), not boxes. To make a box, write the name, an equals sign, then the value, with no \`def\`. Text needs a quote at both ends too: \`${defFix}\``,
          raw,
        );
      }
      if (defFix) {
        return explain(
          "def-for-variable",
          "def makes functions",
          `def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value, with no def. Text needs a quote at both ends too: ${defFix}`,
          raw,
        );
      }
      const dash = dashFix(fixed);
      if (dash && printOnlyTask(context)) return dashInPrintTask(fixed, line, raw, "dash-and-quote", true);
      if (dash) {
        return explain(
          "dash-and-quote",
          "Two fixes on one line",
          `${lineWord(line)} needs two fixes: the text needs its closing quote, and the dash - should be an equals sign =. Write: ${dash}`,
          raw,
        );
      }
      if (added) {
        return explain(
          "missing-quote",
          "Missing quote",
          `The text${onLine(line)} is missing its closing quote, and the line is missing its closing ${added}. Quotes and brackets come in pairs. Write: ${fixed}`,
          raw,
        );
      }
      return explain(
        "missing-quote",
        "Missing quote",
        `The text${onLine(line)} is missing its closing quote. Text needs a quote at the start and at the end, like this: ${fixed}`,
        raw,
      );
    }
  }
  return explain(
    "missing-quote",
    "Missing quote",
    `Some text${onLine(line)} is missing its closing quote. Text needs a quote at the start and at the end, like "Hello".`,
    raw,
  );
}

/** A value written after `def`'s name, unwrapped: `("Fire Ball")` -> `"Fire Ball"`. */
function unwrapValue(value: string): string {
  const inner = value.trim().match(/^\(\s*(["'][^"']*["']|\d+(?:\.\d+)?)\s*\)$/);
  return inner ? inner[1] : value.trim();
}

/** `def character = "Kratos"`, `def ("character")`, `def: Power_up= ("Fire Ball")`: returns `name = value`. */
function defForVariable(text: string): string | null {
  const trimmed = codePart(text).trim();
  if (!/^def\b/.test(trimmed)) return null;
  // A real function header (maybe missing its colon) is not this slip: def greet(name="Lucky")
  const header = trimmed.match(/^def\s+[A-Za-z_]\w*\s*\(([^)]*)\)?\s*:?\s*$/);
  if (header && !/^\s*["']/.test(header[1] ?? "")) return null;
  if (/^def\s+[A-Za-z_]\w*\s*:\s*$/.test(trimmed)) return null;
  const quoted = trimmed.match(/^def\s*\(\s*["']([^"']*)["']/);
  const named = trimmed.match(/^def\s+([A-Za-z_]\w*)/) ?? trimmed.match(/^def\s*:\s*([A-Za-z_]\w*)/);
  const afterColon = trimmed.match(/^def\s+[A-Za-z_]\w*\s*:\s*(.+)$/)?.[1];
  const value =
    trimmed.match(/=(?!=)\s*(.+)$/)?.[1]?.trim() ?? afterColon ?? trimmed.match(/\(\s*(["'][^"']*["'])\s*\)/)?.[1];
  const looksLikeVariable =
    Boolean(quoted) ||
    /^def\s*[(:]/.test(trimmed) ||
    /=(?!=)/.test(trimmed) ||
    /\(\s*["']/.test(trimmed) ||
    afterColon !== undefined;
  if (!looksLikeVariable) return null;
  const name = quoted?.[1] && /^[A-Za-z_]\w*$/.test(quoted[1]) ? quoted[1] : named?.[1];
  if (name && value && !quoted) return `${name} = ${unwrapValue(value)}`;
  if (name) return `${name} = "your value"`;
  return `character = "Kratos"`;
}

/**
 * `def ("Steady now")` in a task that only prints (Lesson 1A): boxes are not taught yet, so the fix is print,
 * with the student's own words. `closed` says the line's closing quote was missing too.
 */
function defInPrintTask(text: string, raw: string, closed = false): CourseExplanation {
  const quote = closed ? " The words need a quote at both ends too." : "";
  return explain(
    "def-for-variable",
    "No def needed",
    `\`def\` is not needed here: this task only shows words.${quote} To show them, write \`${printFix(text)}\``,
    raw,
  );
}

/** `oogrish - "Steady now"` in a task that only prints: the fix is print, not a box. */
function dashInPrintTask(
  text: string,
  line: number | null,
  raw: string,
  kind: "dash-for-equals" | "dash-and-quote" | "dash-no-effect",
  closed = false,
): CourseExplanation {
  const quote = closed ? " The words need a quote at both ends too." : "";
  return explain(
    kind,
    "Show it with print",
    `${lineWord(line)} has a name and a dash -, but this task only shows words.${quote} To show them, write \`${printFix(text)}\``,
    raw,
  );
}

/** A word of text typed without quotes: letters or digits, maybe with punctuation stuck to it. */
const BARE_WORD = /^[A-Za-z0-9][A-Za-z0-9,!?.:;'-]*$/;

/** Split an expression at the commas and plus signs that are not inside quotes or brackets. */
function splitTopLevel(expr: string): { parts: string[]; marks: string[] } | null {
  const parts: string[] = [];
  const marks: string[] = [];
  let depth = 0;
  let from = 0;
  let index = 0;
  while (index < expr.length) {
    const char = expr[index];
    if (char === '"' || char === "'") {
      const close = expr.indexOf(char, index + 1);
      if (close < 0) return null;
      index = close + 1;
      continue;
    }
    if (char in CLOSER) depth += 1;
    else if (char in OPENER) depth -= 1;
    else if (depth === 0 && (char === "," || char === "+")) {
      parts.push(expr.slice(from, index).trim());
      marks.push(char);
      from = index + 1;
    }
    index += 1;
  }
  parts.push(expr.slice(from).trim());
  return depth === 0 ? { parts, marks } : null;
}

/** `print("Name:", spartan rage)` -> `print("Name:", "spartan rage")`: quote the runs of plain words. */
function quoteWordRuns(expr: string, names: string[]): string | null {
  const split = splitTopLevel(expr);
  if (!split) return null;
  let changed = false;
  const parts: string[] = [];
  for (const part of split.parts) {
    const words = part.split(/\s+/).filter(Boolean);
    const plain = words.length > 0 && words.every((word) => BARE_WORD.test(word)) && words.some((word) => /[A-Za-z]/.test(word));
    const sentence = words.length >= 2 || /[.!?]$/.test(part);
    if (plain && sentence) {
      if (words.some((word) => names.includes(word))) return null;
      parts.push(`"${words.length === 1 ? part.replace(/[.!?]+$/, "") : words.join(" ")}"`);
      changed = true;
    } else {
      parts.push(part);
    }
  }
  if (!changed) return null;
  return parts.reduce((out, part, index) => (index === 0 ? part : `${out}${split.marks[index - 1] === "+" ? " + " : ", "}${part}`), "");
}

/**
 * Text typed without quotes: `caster = Gear shift`, `caster = Gearshift.`, `print(Gearshift has 20 mana.)`,
 * `print("Name:", spartan rage)`. Returns the student's own line with the quotes put in, or null when the
 * line is not that slip.
 */
function unquotedWords(text: string, names: string[]): { fixed: string; comma: boolean } | null {
  const body = codePart(text);
  // A call that takes several values (`heal(Moth Queen, 5)`, `cheer_on("Captain Glug", Go now)`): split the
  // brackets on their top-level commas and quote ONLY the bare run of words. Numbers, the program's own names and
  // quoted values stay as they are. (print keeps its own rows below: a comma there is often part of the sentence.)
  const several = body.match(/^(\s*(?:[A-Za-z_]\w*\s*=(?!=)\s*)?([A-Za-z_][\w.]*)\s*\()(.*)\)\s*$/);
  if (several && several[2] !== "print" && splitTopLevel(several[3])?.marks.includes(",")) {
    const fixed = quoteWordRuns(several[3].trim(), names);
    return fixed ? { fixed: `${several[1].trim()}${fixed})`, comma: false } : null;
  }
  const assign = body.match(/^(\s*[A-Za-z_]\w*\s*=)(?!=)\s*(.+?)\s*$/);
  const call = body.match(/^(\s*print\s*\()\s*(.*?)\s*\)\s*$/);
  if (/["']/.test(body)) {
    // Some text already has quotes: quote the runs of plain words between the commas and plus signs.
    if (assign) {
      const fixed = quoteWordRuns(assign[2], names);
      return fixed ? { fixed: `${assign[1].trim()} ${fixed}`, comma: false } : null;
    }
    if (call) {
      const fixed = quoteWordRuns(call[2], names);
      return fixed ? { fixed: `print(${fixed})`, comma: false } : null;
    }
    return null;
  }
  if (assign) {
    const words = assign[2].split(/\s+/);
    if (!words.every((word) => BARE_WORD.test(word)) || !words.some((word) => /[A-Za-z]/.test(word))) return null;
    if (words.length === 1 && !/[.!?]$/.test(words[0])) return null;
    // One word with a full stop after it ("Gearshift.") is a sentence's end, not part of the name.
    const value = words.length === 1 ? words[0].replace(/[.!?]+$/, "") : words.join(" ");
    return { fixed: `${assign[1].trim()} "${value}"`, comma: false };
  }
  if (call && !/[()]/.test(call[2])) {
    const words = call[2].split(/\s+/);
    if (words.length < 2 || !words.every((word) => BARE_WORD.test(word))) return null;
    if (!words.some((word) => /[A-Za-z]/.test(word))) return null;
    // Keep the student's variables outside the quotes, and quote the runs of words between them.
    const parts: string[] = [];
    let run: string[] = [];
    const flush = () => {
      if (run.length) parts.push(`"${run.join(" ")}"`);
      run = [];
    };
    for (const word of words) {
      if (names.includes(word)) {
        flush();
        parts.push(word);
      } else {
        run.push(word);
      }
    }
    flush();
    return { fixed: `print(${parts.join(", ")})`, comma: parts.every((part) => !part.startsWith('"')) };
  }
  return null;
}

function explainUnquoted(text: string, code: string, line: number | null, raw: string): CourseExplanation | null {
  const found = unquotedWords(text, namesBefore(code, line));
  if (!found) return null;
  if (found.comma) {
    return explain(
      "missing-comma",
      "Missing comma",
      `${lineWord(line)} has values side by side with nothing between them. Put a comma between them, like this: ${found.fixed}`,
      raw,
    );
  }
  return explain(
    "unquoted-words",
    "Missing quotes",
    `${lineWord(line)} has words with no quotes around them, so Python tries to read them as code. Text needs quotes at the start and the end, like this: ${found.fixed}`,
    raw,
  );
}

const ORDINALS: Record<string, string> = {
  "1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth", "5th": "fifth",
  "6th": "sixth", "7th": "seventh", "8th": "eighth", "9th": "ninth", "10th": "tenth",
};

/** `5P + 2S`, `x = 5x`, `1st_place = "Lucky"`: a number with letters stuck to it. */
function explainStuckNumber(text: string, code: string, line: number | null, raw: string): CourseExplanation {
  const body = codePart(text);
  let match: RegExpExecArray | null = null;
  // The first number-with-letters outside a string.
  const pattern = /(^|[^\w.])(\d+(?:\.\d+)?)([A-Za-z_]\w*)/g;
  for (let found = pattern.exec(body); found; found = pattern.exec(body)) {
    const at = found.index + found[1].length;
    if (!scanLine(body.slice(0, at)).unterminated) {
      match = found;
      break;
    }
  }
  if (!match) {
    return explain(
      "number-stuck-to-name",
      "Number stuck to letters",
      `${lineWord(line)} has a number with letters stuck to it. A name can't start with a number, and to multiply you write 5 * x, not 5x.`,
      raw,
    );
  }
  const [, , number, word] = match;
  const token = `${number}${word}`;
  if (new RegExp(`^\\s*${escapeRegExp(token)}\\s*=(?!=)`).test(body)) {
    const better = ORDINALS[`${number}${word.slice(0, 2)}`] && /^(st|nd|rd|th)/.test(word)
      ? `${ORDINALS[`${number}${word.slice(0, 2)}`]}${word.slice(2)}`
      : `${word.replace(/^_+/, "")}${number}`;
    return explain(
      "name-starts-with-number",
      "Name starts with a number",
      `A variable name can't start with a number. Start it with a letter instead, like ${better}.`,
      raw,
    );
  }
  const known = namesBefore(code, line).filter((name) => name !== body.match(/^\s*([A-Za-z_]\w*)\s*=/)?.[1]);
  const times = `${number} * ${word}`;
  const ownNames = known.length >= 2 ? ` If you already made variables for these numbers, use them instead, like ${known.slice(-2).join(" and ")}.` : "";
  return explain(
    "number-stuck-to-name",
    "Number stuck to letters",
    known.includes(word)
      ? `Python can't read ${token}: a number can't have letters stuck to it. To multiply, put * between them: ${times}`
      : `Python can't read ${token}: a number can't have letters stuck to it, and ${token} doesn't mean "${number} times ${word}". To multiply, put * between a number and a variable, like ${times} (${word} must be a variable you made).${ownNames}`,
    raw,
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* Questions and choices (Unit 2): comparisons, if / elif / else, random, assert                   */
/* ---------------------------------------------------------------------------------------------- */

const BACKWARDS: Record<string, string> = { "=>": ">=", "=<": "<=", "=!": "!=" };

/** Text methods the course uses: written after a dot (`answer.lower()`), never `lower(answer)`. */
const STRING_METHODS = new Set(["lower", "upper", "capitalize", "title", "strip"]);

/** `if ___:` or `roll = ___`: the starter's blank, still in the code. */
function blankLeft(blank: string, line: number | null, raw: string): CourseExplanation {
  return explain(
    "blank-left",
    "Fill in the blank",
    `${lineWord(line)} still has the blank \`${blank}\` from the starter. Python reads it as a name and finds nothing. Replace the \`${blank}\` with your own code: the step says what goes there.`,
    raw,
  );
}

/** `passed = roll => needed`, `if x =< 3:`, `print(a =! b)`: a two-mark sign typed the wrong way round. */
function explainBackwardsSign(text: string, line: number | null, raw: string): CourseExplanation | null {
  const mask = maskStrings(text);
  const signs = [...mask.matchAll(/(?<![=<>!])=([<>!])(?!=)/g)].map((match) => ({ at: match.index ?? 0, typed: match[0] }));
  if (signs.length === 0) return null;
  let fixed = text;
  for (const { at, typed } of [...signs].reverse()) fixed = `${fixed.slice(0, at)}${BACKWARDS[typed]}${fixed.slice(at + 2)}`;
  const typed = [...new Set(signs.map((sign) => sign.typed))];
  return explain(
    "sign-backwards",
    "Sign typed backwards",
    `${lineWord(line)} has ${typed.map((sign) => `\`${sign}\``).join(" and ")}, a sign typed backwards. In Python the \`=\` always comes second: ${typed.map((sign) => `\`${BACKWARDS[sign]}\``).join(" and ")}. Write: \`${codePart(fixed).trim()}\``,
    raw,
  );
}

const STATEMENT_WORDS =
  /^(if|elif|else|while|for|assert|return|import|from|def|class|with|try|except|finally|raise|del|pass|break|continue|global|nonlocal|lambda|yield|not|await|async|match|case|print)\b/;

type Comparison = { left: string; op: string; right: string };

/**
 * A line that is only a comparison (`hero == "Lucky"`, `roll >= needed`): it asks a question and keeps
 * nothing. Null for anything else (`passed = roll >= needed`, `print(a == b)`, `if a == b:`).
 */
function comparisonAlone(text: string): Comparison | null {
  const mask = maskStrings(text);
  const body = mask.trim();
  if (!body || STATEMENT_WORDS.test(body) || body.endsWith(":") || singleEquals(mask).length > 0) return null;
  // `passed: roll >= needed` is a note about a box's type (Python allows it and does nothing), not a question.
  if (/:/.test(mask.replace(/\[[^\]]*\]|\([^)]*\)|\{[^}]*\}/g, ""))) return null;
  let depth = 0;
  for (let index = 0; index < mask.length; index += 1) {
    const char = mask[index];
    if (char in CLOSER) depth += 1;
    else if (char in OPENER) depth = Math.max(0, depth - 1);
    else if (depth === 0) {
      // `<<` and `>>` shift numbers: they are not questions.
      if (/[<>]/.test(char) && mask[index + 1] === char) {
        index += 1;
        continue;
      }
      const op = mask.slice(index, index + 2).match(/^(==|!=|>=|<=)/)?.[1] ?? (/[<>]/.test(char) ? char : null);
      if (!op) continue;
      const left = text.slice(0, index).trim();
      const right = codePart(text.slice(index + op.length)).trim();
      if (!left || !right) return null;
      return { left, op, right };
    }
  }
  return null;
}

/** Any comparison sign in a piece of code (strings masked first). */
const COMPARE_ANYWHERE = /==|!=|>=|<=|(?<![<>])[<>](?![<>])/;

const OPTION_STOP = new Set(["and", "or", "not", "is", "in", "if", "else"]);

/**
 * `elif choice == option 2:`: two or more plain words after `==` or `!=`, with no quotes. Returns the line
 * with the quotes put in, or null.
 */
function quoteOptionWords(text: string): { fixed: string; words: string } | null {
  const mask = maskStrings(text);
  const edits: { from: number; to: number; words: string }[] = [];
  for (const match of mask.matchAll(/(==|!=)[ \t]*/g)) {
    const from = (match.index ?? 0) + match[0].length;
    const run = mask.slice(from).match(/^[A-Za-z0-9_]+(?:[ \t]+[A-Za-z0-9_]+)*/)?.[0] ?? "";
    const words: string[] = [];
    for (const word of run.split(/[ \t]+/).filter(Boolean)) {
      if (OPTION_STOP.has(word)) break;
      words.push(word);
    }
    if (words.length < 2 || !words.some((word) => /[A-Za-z]/.test(word))) continue;
    const length = mask.slice(from).match(new RegExp(`^${words.map(escapeRegExp).join("[ \\t]+")}`))?.[0].length ?? 0;
    if (length > 0) edits.push({ from, to: from + length, words: words.join(" ") });
  }
  if (edits.length === 0) return null;
  let fixed = text;
  for (const { from, to, words } of [...edits].reverse()) fixed = `${fixed.slice(0, from)}"${words}"${fixed.slice(to)}`;
  return { fixed: codePart(fixed).trim(), words: edits[0].words };
}

function explainUnquotedOption(text: string, line: number | null, raw: string): CourseExplanation | null {
  const quoted = quoteOptionWords(text);
  if (!quoted) return null;
  return explain(
    "unquoted-option",
    "Text needs quotes",
    `${lineWord(line)} compares with ${quoted.words}, words with no quotes, so Python tries to read them as code. Text in a comparison needs quotes too, like this: \`${quoted.fixed}\``,
    raw,
  );
}

type ChainHeader = { word: string; line: number };

/**
 * An `elif` or `else` Python could not fit into a chain (a SyntaxError on its line): one after the chain's
 * `else`, one with no `if` above it, or one indented into the block above.
 */
function explainChain(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const word = codePart(text).trim().match(/^(elif|else)\b/)?.[1];
  if (!word || !line) return null;
  const lines = (code ?? "").split("\n");
  const indent = indentOf(text);
  let before: ChainHeader | null = null;
  for (let at = line - 2; at >= 0; at -= 1) {
    const body = codePart(lines[at] ?? "").trim();
    if (!body) continue;
    const own = indentOf(lines[at] ?? "");
    if (own > indent) continue;
    if (own === indent) before = { word: body.match(/^(if|elif|else|for|while|try|except|finally|with|def|class|match|case)\b/)?.[1] ?? "", line: at + 1 };
    break;
  }
  if (before && (before.word === "if" || before.word === "elif")) return null;
  if (before && word === "else" && ["for", "while", "try", "except"].includes(before.word)) return null;
  if (before?.word === "else") {
    return explain(
      "else-not-last",
      "else comes last",
      word === "elif"
        ? `Line ${line} has \`elif\` after the \`else\` on line ${before.line}. In a chain, \`else\` always comes last: it catches whatever is left. Move the \`elif\` and its lines up, above the \`else\`.`
        : `Line ${line} is a second \`else\`, after the one on line ${before.line}. A chain has only one \`else\`, and it comes last. Make the first one an \`elif\` with a question, or take one away.`,
      raw,
    );
  }
  const ifAbove = lines
    .slice(0, line - 1)
    .map((row, at) => ({ row, at: at + 1 }))
    .reverse()
    .find(({ row }) => /^\s*(if|elif)\b/.test(codePart(row)) && indentOf(row) < indent);
  if (ifAbove) {
    return explain(
      "else-not-lined-up",
      "Line it up with its if",
      `Line ${line}'s \`${word}\` has more spaces in front than its \`if\` on line ${ifAbove.at}, so Python reads it as part of the block above, where an \`${word}\` can't go. Give line ${line} exactly the same spaces in front as line ${ifAbove.at}.`,
      raw,
    );
  }
  return explain(
    "elif-without-if",
    `${word} needs an if`,
    `Line ${line} starts with \`${word}\`, but no \`if\` comes just before it at the same indent, so Python can't tell which question it belongs to. Every chain starts with \`if\`: put this line straight after the \`if\` and its indented lines, lined up with the \`if\`${word === "elif" ? ", or make it an `if`" : ""}.`,
    raw,
  );
}

/** The names a line uses (outside its strings). */
function namesOnLine(text: string): string[] {
  return [...new Set([...maskStrings(text).matchAll(/(?<![\w.])[A-Za-z_]\w*/g)].map((match) => match[0]))].filter(
    (name) => !KEYWORDS.has(name),
  );
}

/** `roll >= "12"`, `needed = "15"` then `roll >= needed`, an input() answer: a number compared with text. */
function explainNumberAndText(op: string, code: string, text: string, line: number | null, raw: string): CourseExplanation {
  const title = "Number or text?";
  const body = codePart(text);
  const quoted = body.match(/(["'])(\d+(?:\.\d+)?)\1/);
  if (quoted && !scanLine(body.slice(0, quoted.index ?? 0)).unterminated) {
    const fixed = `${body.slice(0, quoted.index)}${quoted[2]}${body.slice((quoted.index ?? 0) + quoted[0].length)}`.trim();
    return explain(
      "compare-number-text",
      title,
      `${lineWord(line)} compares a number with text: \`${quoted[0]}\` has quotes, so it is text, and Python can't say which is bigger. Numbers have no quotes: \`${fixed}\``,
      raw,
    );
  }
  const used = namesOnLine(text);
  const fromInput = inputNames(code).find((name) => used.includes(name));
  if (fromInput) {
    return explain(
      "compare-number-text",
      title,
      `${fromInput} came from input(), and input() always gives back text, so ${lineWord(line).toLowerCase()} compares text with a number. Turn it into a number first: int(${fromInput})`,
      raw,
    );
  }
  const lines = (code ?? "").split("\n");
  for (const name of used) {
    const at = lines.findIndex(
      (row, index) => (line === null || index + 1 < line) && new RegExp(`^\\s*${escapeRegExp(name)}\\s*=\\s*(["'])\\d+(?:\\.\\d+)?\\1\\s*$`).test(codePart(row)),
    );
    if (at < 0) continue;
    const made = codePart(lines[at]).trim();
    return explain(
      "compare-number-text",
      title,
      `Line ${at + 1} makes \`${name}\` with quotes: \`${made}\`. Quotes make text, even when it looks like a number, so ${lineWord(line).toLowerCase()} can't compare it with a number. Take the quotes off on line ${at + 1}: \`${made.replace(/(["'])(\d+(?:\.\d+)?)\1/, "$2")}\``,
      raw,
    );
  }
  return explain(
    "compare-number-text",
    title,
    `${lineWord(line)} compares a number with text using \`${op}\`. Text is not a number, even "15", so Python can't say which is bigger. Make both sides numbers: take the quotes off the number, or turn the text into a number with int().`,
    raw,
  );
}

/** The comparison signs Mar'tu's version uses right after `name` inside a print( ) (`print(clock_color != "red")`). */
function solutionPrintSigns(solution: string | undefined, name: string): string[] {
  if (!solution) return [];
  const signs = new Set<string>();
  const at = escapeRegExp(name);
  for (const row of solution.split("\n")) {
    const mask = maskStrings(codePart(row));
    if (!/(^|[^\w.])print\s*\(/.test(mask)) continue;
    for (const match of mask.matchAll(new RegExp(`(?<![\\w.])${at}\\s*(==|!=|>=|<=|<|>)`, "g"))) signs.add(match[1]);
  }
  return [...signs];
}

/** `print(clock_color = "red")`: one `=` inside print, where `==` (a question) belongs. */
function explainEqualsInPrint(name: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation {
  const body = codePart(text);
  const sign = maskStrings(body).match(new RegExp(`(?<![\\w.])${escapeRegExp(name)}\\s*(=)(?!=)`));
  const at = sign ? (sign.index ?? 0) + sign[0].length - 1 : -1;
  const value = at >= 0 ? (body.slice(at + 1).match(/^\s*((?:"[^"]*"|'[^']*'|[^,)])+)/)?.[1] ?? "").trim() : "";
  // Unit 1 has no questions yet: print shows a box, made on the line above.
  if (context?.unitOrder !== undefined && context.unitOrder < 2) {
    return explain(
      "equals-in-print",
      "= makes a box, print shows it",
      `${lineWord(line)} has an \`=\` inside print( ). print only shows things: it can't make a box. Make the box on its own line first${value ? `, \`${name} = ${value}\`` : ""}, then show it: \`print(${name})\``,
      raw,
    );
  }
  const fixed = at >= 0 ? `${body.slice(0, at)}==${body.slice(at + 1)}`.trim() : "";
  // Mar'tu's version prints this box with another sign (`print(clock_color != "red")`): writing the `==` line
  // would send the student the wrong way, so name the kind of sign instead.
  const signs = solutionPrintSigns(context?.solution, name);
  if (signs.length > 0 && !signs.includes("==")) {
    return explain(
      "equals-in-print",
      "= makes a box",
      `${lineWord(line)} has one \`=\` inside print( ). One \`=\` puts a value in a box, and print can't do that. To show the answer to a question, use a comparison sign, such as \`==\` (is the same as) or \`!=\` (is not the same as).`,
      raw,
    );
  }
  return explain(
    "equals-in-print",
    "Use == to ask",
    `${lineWord(line)} has one \`=\` inside print( ). One \`=\` puts a value in a box, and print can't do that. To show whether they are the same, use \`==\`${fixed ? `: \`${fixed}\`` : "."}`,
    raw,
  );
}

/** `assert roll >= needed` that comes out False: the student's own seal, doing its job. */
function explainAssert(message: string, text: string, line: number | null, raw: string): CourseExplanation {
  const asked = codePart(text).trim().match(/^assert\s+(.+?)(?:\s*,\s*(["']).*)?$/)?.[1];
  const what = asked ? `\`${asked}\`` : "its question";
  return explain(
    "assert-failed",
    "Your assert caught something",
    `The \`assert\` on ${line ? `line ${line}` : "this line"} asked ${what} and got False, so Python stopped there.${message ? ` Its note says: ${/[.!?]$/.test(message) ? message : `${message}.`}` : ""} That is the seal doing its job: the code above it does not do what the assert expects. Print the values it checks to see why, then mend the code (or the assert, if it asks the wrong question).`,
    raw,
  );
}

/** A line that starts an indented block (`if ...`, `else`, `for ...`): what the colon goes after. */
const BLOCK_HEADER = /^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\b/;

/** The next line after `line` that has code, or "". */
function nextCodeLine(code: string, line: number): string {
  return (code ?? "").split("\n").slice(line).find((row) => codePart(row).trim().length > 0) ?? "";
}

/**
 * `if roll > 3` (no colon) or `if roll > 3;` (a semicolon): the header with its colon, when the block under it
 * is indented (so the line really ends there). Null otherwise.
 */
function headerWithColon(code: string, text: string, line: number | null): string | null {
  const header = codePart(text);
  if (!line || !BLOCK_HEADER.test(header) || header.endsWith(":")) return null;
  if (indentOf(nextCodeLine(code, line)) <= indentOf(text)) return null;
  return `${header.trim().replace(/\s*;$/, "")}:`;
}

/** `else roll < needed:`: `else` has no question of its own (the Otherwise distractor, QC2's "else with a condition"). */
function elseWithQuestion(text: string, line: number | null, raw: string): CourseExplanation {
  const question = codePart(text).trim().replace(/^else\b\s*/, "").replace(/:\s*$/, "").trim();
  return explain(
    "else-has-question",
    "else asks nothing",
    `${lineWord(line)} gives \`else\` a question${question ? `, \`${question}\`` : ""}. \`else\` has no question of its own: it runs when every question above it was False. Write just \`else:\`. (A new question goes after \`elif\` instead.)`,
    raw,
  );
}

/**
 * Python's own words that a student might type with a capital (`If`, `Else:`, `Import random`), each with the
 * shape of the line that really uses it, so words typed without quotes (`If you dare, enter`) are not read as one.
 */
const CAPITAL_KEYWORD_SHAPES: Record<string, RegExp> = {
  if: /^If\b.*(?::\s*$|[=!<>]=|[<>])/,
  elif: /^Elif\b.*(?::\s*$|[=!<>]=|[<>])/,
  while: /^While\b.*(?::\s*$|[=!<>]=|[<>])/,
  else: /^Else\s*:?\s*$/,
  for: /^For\s+[A-Za-z_]\w*\s+in\b/,
  def: /^Def\s+[A-Za-z_]\w*\s*\(/,
  import: /^Import\s+[A-Za-z_][\w.]*\s*$/,
};

/**
 * `If hours_left < 3:`, `Else:`, `Import random`: one of Python's words with a capital letter, which Python reads
 * as an unknown name and then can't read the line. Also `elif:` / `if:` with no question. Null otherwise.
 */
function explainKeywordShape(text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text).trim();
  const first = body.match(/^([A-Za-z]+)\b/)?.[1] ?? "";
  const small = first.toLowerCase();
  if (first && first !== small && CAPITAL_KEYWORD_SHAPES[small]?.test(maskStrings(body))) {
    const fixed = `${small}${body.slice(first.length)}`;
    return explain(
      "keyword-capital",
      "Small letters",
      `${lineWord(line)} starts with \`${first}\`. Python's own words are all small letters: \`${small}\`, not \`${first}\`. Write: \`${fixed}\``,
      raw,
    );
  }
  const bare = body.match(/^(if|elif)\s*:$/)?.[1];
  if (bare) {
    return explain(
      "no-question",
      `${bare} needs a question`,
      `${lineWord(line)} has \`${bare}:\` with no question. \`${bare}\` asks a question, so the question goes between \`${bare}\` and the colon. If this branch should run when nothing above it was True, write \`else:\` instead.`,
      raw,
    );
  }
  return null;
}

function explainMissingColon(code: string, text: string, line: number | null, raw: string): CourseExplanation {
  const elseIf = codePart(text).match(/^\s*else\s+if\b(.*)$/);
  if (elseIf) {
    const rest = elseIf[1].trim().replace(/:?$/, ":");
    return explain(
      "elif-spelling",
      "Python spells it elif",
      `${lineWord(line)} says \`else if\`. Python joins the two words into one: \`elif\`. Write: \`elif ${rest}\``,
      raw,
    );
  }
  // `else roll < needed:`: else never asks. Python says "expected ':'", but the colon is not what is missing.
  if (/^\s*else\b(?!\s*:)\s*\S/.test(codePart(text))) return elseWithQuestion(text, line, raw);
  const fixed = headerWithColon(code, text, line);
  const word = codePart(text).trim().match(BLOCK_HEADER)?.[1];
  if (fixed && word) {
    const semicolon = /;\s*$/.test(codePart(text));
    return explain(
      "missing-colon",
      "Missing colon",
      `${lineWord(line)} starts with \`${word}\`, so it ends with a colon \`:\`${semicolon ? ", not a semicolon `;`" : ""}. The colon says "the indented lines below belong to me". Write: \`${fixed}\``,
      raw,
    );
  }
  return explain(
    "missing-colon",
    "Missing colon",
    `${lineWord(line)} needs a colon : at the end. Lines that start with if, elif, else, for, while or def always end with :`,
    raw,
  );
}

/**
 * `if roll = 20:`, `said_yes = answer.lower() = "yes"`, `assert passed = False`: one `=` where a question
 * (`==`) belongs. Returns the line with `==`, or null.
 */
function doubleEqualsFix(text: string): string | null {
  const mask = maskStrings(text);
  const equals = singleEquals(mask);
  const question = /^\s*(if|elif|while|assert)\b/.test(mask);
  // In a question line every single = is the slip; in `box = a = b` the first one makes the box.
  const wrong = question ? equals : equals.length >= 2 ? equals.slice(1) : [];
  if (wrong.length === 0) return null;
  let fixed = text;
  for (const at of [...wrong].reverse()) fixed = `${fixed.slice(0, at)}==${fixed.slice(at + 1)}`;
  return codePart(fixed).trim();
}

/* ---------------------------------------------------------------------------------------------- */
/* Recipes (Unit 3): def, ingredients, the values a call hands over, randint, a recipe that calls  */
/* itself. The words are the unit's own (curriculum §2.9): "recipe (function)", "ingredient",      */
/* "hand over", "hand back".                                                                       */
/* ---------------------------------------------------------------------------------------------- */

/** A `def name(` line: from Unit 3 on, the student is writing a recipe there, never making a box. */
const RECIPE_HEADER = /^\s*def\s+[A-Za-z_]\w*\s*\(/;

/** The values inside a call's brackets, split on the commas outside strings and brackets (null if unbalanced). */
function splitArguments(inside: string): string[] | null {
  const parts: string[] = [];
  let depth = 0;
  let from = 0;
  for (let index = 0; index < inside.length; index += 1) {
    const char = inside[index];
    if (char === '"' || char === "'") {
      const close = inside.indexOf(char, index + 1);
      if (close < 0) return null;
      index = close;
      continue;
    }
    if (char in CLOSER) depth += 1;
    else if (char in OPENER) depth -= 1;
    else if (char === "," && depth === 0) {
      parts.push(inside.slice(from, index).trim());
      from = index + 1;
    }
  }
  if (depth !== 0) return null;
  const last = inside.slice(from).trim();
  return last || parts.length > 0 ? [...parts, last] : [];
}

/** The ingredients on the code's (last) `def name(...)` line, or null when the code makes no recipe by that name. */
function recipeIngredients(code: string, name: string): string[] | null {
  let found: string[] | null = null;
  for (const row of (code ?? "").split("\n")) {
    const header = codePart(row).match(new RegExp(`^\\s*def\\s+${escapeRegExp(name)}\\s*\\(([^)]*)\\)`));
    if (!header) continue;
    found = (splitArguments(header[1]) ?? [])
      .map((part) => part.split(/[\s:=]/)[0]?.replace(/^\*+/, "") ?? "")
      .filter((part) => /^[A-Za-z_]\w*$/.test(part));
  }
  return found;
}

type TaskRecipe = { name: string; ingredients: string[]; returns: boolean };

/**
 * `name` is one of the task's recipes (Unit 3 on): Mar'tu's version makes it with `def`, and the task names it (its
 * "Names to use") or the student's code calls it. Null for anything else, so a box of the student's own never gets
 * recipe advice.
 */
function taskRecipe(name: string, code: string, context?: ExplainContext): TaskRecipe | null {
  if (!unitAtLeast(context, FUNCTIONS_UNIT_ORDER) || !context?.solution || KEYWORDS.has(name)) return null;
  const ingredients = recipeIngredients(context.solution, name);
  if (!ingredients) return null;
  const call = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`);
  const called = (code ?? "").split("\n").some((row) => call.test(maskStrings(row)));
  if (!(context.names ?? []).includes(name) && !called) return null;
  const block = recipeBlocks(context.solution).find((entry) => entry.recipe === name);
  const body = block ? context.solution.split("\n").slice(block.start, block.end) : [];
  return { name, ingredients, returns: body.some((row) => /^\s*return\b/.test(codePart(row))) };
}

/**
 * "`max_fuel_for` is a recipe in this task: `def max_fuel_for(cells):`, then an indented `return cells * 5`." Built
 * from the task's ingredients and the student's own right side (`value`), when there is one.
 */
function recipeShape(recipe: TaskRecipe, value?: string): string {
  const header = `\`def ${recipe.name}(${recipe.ingredients.join(", ")}):\``;
  const right = value?.trim();
  const steps = !recipe.returns ? "then its steps, indented under it" : right ? `then an indented \`return ${right}\`` : "then an indented `return` with the answer";
  return `\`${recipe.name}\` is a recipe in this task: ${header}, ${steps}.`;
}

/**
 * `max_fuel_for(cells) = cells * 5`: a recipe written the way math writes f(x) = 5x. Python says "cannot assign to
 * function call ... Maybe you meant '=='", which sends the student the wrong way. Built from the student's own name,
 * ingredients and right side. Null for anything else (a builtin on the left, values in the brackets).
 */
function explainRecipeLikeMath(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text);
  // `double_cost = (price):`: a recipe made with `=`, the way a box is made (Python says only "invalid syntax").
  const boxLike = /^invalid syntax/i.test(message)
    ? body.match(/^\s*([A-Za-z_]\w*)\s*=\s*\(\s*((?:[A-Za-z_]\w*\s*,\s*)*[A-Za-z_]\w*)?\s*\)\s*:\s*$/)
    : null;
  if (boxLike && !KEYWORDS.has(boxLike[1]) && !COMMON_BUILTINS.includes(boxLike[1])) {
    const ingredients = (boxLike[2] ?? "").split(",").map((part) => part.trim()).filter(Boolean);
    return explain(
      "recipe-like-math",
      "A recipe starts with def",
      `${lineWord(line)} makes the recipe with \`=\`, the way a box is made. In Python a recipe (function) starts with \`def\`: \`def ${boxLike[1]}(${ingredients.join(", ")}):\`, then its steps, indented.`,
      raw,
    );
  }
  if (!/cannot assign to function call/i.test(message)) return null;
  const at = singleEquals(maskStrings(body))[0];
  if (at === undefined) return null;
  const call = body.slice(0, at).trim().match(/^([A-Za-z_]\w*)\s*\(\s*((?:[A-Za-z_]\w*\s*,\s*)*[A-Za-z_]\w*)?\s*\)$/);
  if (!call || COMMON_BUILTINS.includes(call[1]) || KEYWORDS.has(call[1])) return null;
  const ingredients = (call[2] ?? "").split(",").map((part) => part.trim()).filter(Boolean);
  if (ingredients.some((name) => KEYWORDS.has(name))) return null;
  const right = body.slice(at + 1).trim();
  const back = right ? `\`return ${right}\`` : "`return` with the answer";
  return explain(
    "recipe-like-math",
    "A recipe starts with def",
    `${lineWord(line)} is math's way to write it. In Python a recipe (function) starts with \`def\`: \`def ${call[1]}(${ingredients.join(", ")}):\`, then an indented ${back}.`,
    raw,
  );
}

/**
 * `def max_fuel_for("cells"):` or `def show_hit(4, 3):`: a value where an ingredient's name goes (Python says only
 * "invalid syntax"). The def line comes back with names in its brackets: the quotes taken off a name, else Mar'tu's
 * own ingredient in that place, else a plain `value`.
 */
function explainQuotedIngredient(text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const header = codePart(text).match(/^\s*def\s+([A-Za-z_]\w*)\s*\((.*)\)\s*:?\s*$/);
  const parts = header ? splitArguments(header[2]) : null;
  if (!header || !parts) return null;
  const quoted = (part: string) => /^(["'])[^"']*\1$/.test(part);
  const number = (part: string) => /^-?\d+(?:\.\d+)?$/.test(part);
  const isName = (part: string) => /^[A-Za-z_]\w*$/.test(part) && !KEYWORDS.has(part);
  if (!parts.some((part) => quoted(part) || number(part))) return null;
  if (!parts.every((part) => quoted(part) || number(part) || isName(part))) return null;
  const own = context?.solution ? recipeIngredients(context.solution, header[1]) : null;
  const used = new Set<string>();
  const names = parts.map((part, index) => {
    const inner = quoted(part) ? part.slice(1, -1).trim() : part;
    let name = isName(inner) ? inner : (own?.[index] ?? "");
    if (!isName(name) || used.has(name)) name = parts.length === 1 ? "value" : `value${index + 1}`;
    used.add(name);
    return name;
  });
  const fixed = `def ${header[1]}(${names.join(", ")}):`;
  if (parts.some(quoted)) {
    return explain(
      "quoted-ingredient",
      "No quotes on an ingredient",
      `${lineWord(line)} has an ingredient in quotes. Ingredient names have no quotes: \`${fixed}\``,
      raw,
    );
  }
  return explain(
    "quoted-ingredient",
    "An ingredient is a name",
    `${lineWord(line)} has a number where an ingredient's name goes. An ingredient is a name: \`${fixed}\`. The numbers go in the call.`,
    raw,
  );
}

/**
 * `def max_fuel_for(cells) = cells * 5`: math's f(x) = 5x with a `def` in front. Python says "expected ':'", and a
 * colon added at the end only gets the same error again: the colon goes right after the brackets, the steps below.
 */
function explainDefLikeMath(text: string, line: number | null, raw: string): CourseExplanation | null {
  const header = codePart(text).match(/^\s*def\s+([A-Za-z_]\w*)\s*\(([^()]*)\)\s*=(?!=)\s*(.+?)\s*:?\s*$/);
  const ingredients = header ? splitArguments(header[2]) : null;
  if (!header || !ingredients || !ingredients.every((part) => /^[A-Za-z_]\w*$/.test(part) && !KEYWORDS.has(part))) return null;
  return explain(
    "recipe-like-math",
    "Steps go below the def line",
    `${lineWord(line)} puts \`=\` after the brackets, the way math writes it. In Python the colon goes right after the brackets, and the steps go below: \`def ${header[1]}(${ingredients.join(", ")}):\`, then an indented \`return ${header[3]}\`.`,
    raw,
  );
}

/**
 * One of the task's recipes written half like a box: `def max_fuel_for = cells * 5`, or its name in quotes,
 * `def ("say_steady"):`. def-for-variable would answer "make a box", which turns the recipe into a box. A quoted name
 * with an indented step under it is a recipe too, whatever the task. Null for anything else.
 */
function explainRecipeMadeAsBox(
  text: string,
  code: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation | null {
  const body = codePart(text).trim();
  const valued = body.match(/^def\s+([A-Za-z_]\w*)\s*=(?!=)\s*(.+)$/);
  const valuedRecipe = valued ? taskRecipe(valued[1], code, context) : null;
  if (valued && valuedRecipe) {
    return explain(
      "recipe-like-math",
      "A recipe needs ( ) and a colon",
      `${lineWord(line)} mixes \`def\` with \`=\`. ${recipeShape(valuedRecipe, valued[2])}`,
      raw,
    );
  }
  const quoted = body.match(/^def\s*\(?\s*(["'])([A-Za-z_]\w*)\1\s*\)?\s*:?\s*$/);
  if (!quoted || KEYWORDS.has(quoted[2])) return null;
  const recipe = taskRecipe(quoted[2], code, context);
  const stepBelow = line !== null && indentOf(nextCodeLine(code, line)) > indentOf(text);
  if (!recipe && !stepBelow) return null;
  const header = `\`def ${quoted[2]}(${recipe ? recipe.ingredients.join(", ") : ""}):\``;
  return explain(
    "quoted-recipe-name",
    "No quotes on a recipe's name",
    `${lineWord(line)} has the recipe's name in quotes. A recipe's name has no quotes: it goes right after \`def\`, then ( ) and a colon: ${header}, with its steps indented under it.`,
    raw,
  );
}

/**
 * "missing 1 required positional argument" / "takes 1 positional argument but 2 were given". From Unit 3 on, when
 * the code makes the recipe, its ingredients come from its own `def` line; `random.randint` takes two values.
 * Python's "positional argument" words are never the explanation (its last line still shows below).
 */
function explainValueCount(message: string, code: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation {
  const count = message.match(/^([\w.]+)\(\) (?:takes (\d+) positional arguments? but (\d+) (?:were|was) given|missing (\d+) required positional arguments?)/);
  const name = count?.[1] ?? "";
  const call = line ? `The call on line ${line}` : "This call";
  const handedText = (handed: number) => (handed === 0 ? "nothing" : String(handed));
  const ingredients = count && /^[A-Za-z_]\w*$/.test(name) && unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? recipeIngredients(code, name) : null;
  if (count && ingredients) {
    const handed = count[2] !== undefined ? Number(count[3]) : ingredients.length - Number(count[4]);
    if (handed >= 0 && handed !== ingredients.length) {
      if (ingredients.length === 0) {
        return explain(
          "wrong-number-of-values",
          "Wrong number of values",
          `\`${name}\` has no ingredients, but ${call.charAt(0).toLowerCase()}${call.slice(1)} hands over ${handedText(handed)}.`,
          raw,
        );
      }
      const listed = ingredients.map((ingredient) => `\`${ingredient}\``).join(", ");
      const has = ingredients.length === 1 ? "1 ingredient" : `${ingredients.length} ingredients`;
      return explain(
        "wrong-number-of-values",
        "Wrong number of values",
        `\`${name}\` has ${has} (${listed}). ${call} hands over ${handedText(handed)}. Hand over one value per ingredient.`,
        raw,
      );
    }
  }
  // `random.randint(die_size)`: the method's own count includes Python's hidden first value.
  if (count && /^(Random\.)?randint$/.test(name) && unitAtLeast(context, RANDOM_UNIT_ORDER)) {
    const handed = count[2] !== undefined ? Number(count[3]) - 1 : 2 - Number(count[4]);
    if (handed >= 0 && handed !== 2) {
      return explain(
        "wrong-number-of-values",
        "Wrong number of values",
        `\`random.randint\` takes 2 values: the smallest number, then the biggest. ${call} hands over ${handedText(handed)}.`,
        raw,
      );
    }
  }
  return explain(
    "wrong-number-of-values",
    "Wrong number of values",
    `The function call${onLine(line)} has the wrong number of values inside its ( ).`,
    raw,
  );
}

/**
 * `random.randint(die_size, 1)`: "empty range in randrange(20, 2)". The student's own two numbers, swapped. Null when
 * the line has no `randint(` with two values, or its first value is already 1 or less (another slip emptied it).
 */
function explainRandintBackwards(text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text);
  const start = maskStrings(body).search(/(?<![\w])(?:random\s*\.\s*)?randint\s*\(/);
  if (start < 0) return null;
  const open = body.indexOf("(", start);
  let depth = 0;
  let close = -1;
  const mask = maskStrings(body);
  for (let index = open; index < mask.length; index += 1) {
    if (mask[index] in CLOSER) depth += 1;
    else if (mask[index] in OPENER && --depth === 0) {
      close = index;
      break;
    }
  }
  const values = close > open ? splitArguments(body.slice(open + 1, close)) : null;
  if (!values || values.length !== 2 || values.some((value) => !value)) return null;
  if (/^-?\d+(?:\.\d+)?$/.test(values[0]) && Number(values[0]) <= 1) return null;
  const fixed = `${body.slice(start, open).replace(/\s+/g, "")}(${values[1]}, ${values[0]})`;
  return explain(
    "randint-backwards",
    "Smallest number first",
    `${lineWord(line)} rolls with the numbers the wrong way round. Smallest number first: \`${fixed}\``,
    raw,
  );
}

/**
 * RecursionError: a recipe that calls itself (`def say_steady():` with `say_steady()` indented under it). Says which
 * line, and that the call belongs below the recipe; any other endless calling keeps the plain words.
 */
function explainRecursion(code: string, raw: string): CourseExplanation {
  const lines = (code ?? "").split("\n");
  for (const block of recipeBlocks(code)) {
    const self = new RegExp(`(^|[^\\w.])${escapeRegExp(block.recipe)}\\s*\\(`);
    for (let at = block.start; at < block.end; at += 1) {
      if (!self.test(maskStrings(codePart(lines[at] ?? "")))) continue;
      return explain(
        "never-ending-calls",
        "A recipe that calls itself",
        `Line ${at + 1} calls \`${block.recipe}\` inside \`${block.recipe}\` itself, so it starts again and again and never stops. To call it, write the call below the recipe, with no spaces in front.`,
        raw,
      );
    }
  }
  return explain(
    "never-ending-calls",
    "Never-ending calls",
    "A function keeps calling itself and never stops. Make sure it has a way to finish with a return that does not call it again.",
    raw,
  );
}

/** The recipes in the code: each `def` line and the lines its indented body spans (1-based, inclusive). */
function recipeBlocks(code: string): { recipe: string; start: number; end: number }[] {
  const lines = (code ?? "").split("\n");
  const blocks: { recipe: string; start: number; end: number }[] = [];
  lines.forEach((row, index) => {
    const recipe = codePart(row).match(/^\s*def\s+([A-Za-z_]\w*)\s*\(/)?.[1];
    if (!recipe) return;
    const indent = indentOf(row);
    let end = index + 1;
    for (let at = index + 1; at < lines.length; at += 1) {
      if (!codePart(lines[at] ?? "").trim()) continue;
      if (indentOf(lines[at] ?? "") <= indent) break;
      end = at + 1;
    }
    blocks.push({ recipe, start: index + 1, end });
  });
  return blocks;
}

/**
 * Unit 3's names, read where they do not exist (a NameError): a recipe called above its `def`, one of the task's
 * recipes that no `def` makes yet, and an ingredient or a box that only lives inside a recipe (its "kitchen"), used
 * outside it. Null for anything else.
 */
function explainRecipeName(
  name: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation | null {
  const blocks = recipeBlocks(code);
  const called = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`).test(maskStrings(codePart(text)));
  const own = blocks.find((block) => block.recipe === name);
  if (called && own && line !== null && own.start > line) {
    return explain(
      "recipe-called-too-early",
      "Called too early",
      `Line ${line} calls \`${name}\`, but its \`def\` is only on line ${own.start}. Python runs from top to bottom, so move the recipe above the line that calls it.`,
      raw,
    );
  }
  if (called && !own && (context?.names ?? []).includes(name)) {
    return explain(
      "recipe-not-made-yet",
      "Recipe not made yet",
      `\`${name}\` is one of this task's recipes, but no \`def\` line makes it yet. Write it with \`def\`${line ? ` above line ${line}, the line that calls it` : ""}.`,
      raw,
    );
  }
  const defined = definedNames(code);
  const made = defined.filter((entry) => entry.name === name);
  const body = codePart(text).trim();
  const list = (names: string[]) => names.map((entry) => `\`${entry}\``).join(names.length === 2 ? " and " : ", ");
  // `max_fuel_for = cells * 5`: one of the task's recipes made with `=`, the way a box is made, so Python reads its
  // right side now and finds no `cells`. Making `cells` first would only turn the recipe into a box.
  const boxed = body.match(/^([A-Za-z_]\w*)\s*=(?!=)\s*(.+)$/);
  const asBox = boxed && !blocks.some((block) => block.recipe === boxed[1]) ? taskRecipe(boxed[1], code, context) : null;
  if (asBox && boxed) {
    return explain(
      "recipe-like-math",
      "A recipe starts with def",
      `${lineWord(line)} makes \`${boxed[1]}\` with \`=\`, the way a box is made. ${recipeShape(asBox, boxed[2])}`,
      raw,
    );
  }
  const fromExample = exampleOnlyNames(context).includes(name);
  // No line makes `name` at all.
  if (made.length === 0 && line !== null) {
    // `get_greeting = greeting`: the store written the wrong way round, a recipe's name on the left of `=`.
    const reversed = body.match(/^([A-Za-z_]\w*)\s*=(?!=)\s*([A-Za-z_]\w*)$/);
    if (!fromExample && reversed && reversed[2] === name && blocks.some((block) => block.recipe === reversed[1])) {
      const needs = recipeIngredients(code, reversed[1]) ?? [];
      return explain(
        "store-backwards",
        "Store it the other way",
        `${lineWord(line)} puts \`${name}\` into \`${reversed[1]}\`, the wrong way round, so Python looks for a box \`${name}\` that no line makes. The new box goes on the left of \`=\`, the call on the right: ${needs.length === 0 ? `\`${name} = ${reversed[1]}()\`` : `\`${name} = ${reversed[1]}(...)\`, with one value per ingredient`}`,
        raw,
      );
    }
    // `return result` inside a recipe whose own box is `total` (RNM): never "put quotes around it". A name copied from
    // the example (or a hint's Teach me example) gets this row too, so `return result` after `fuel = ...` points at
    // `fuel`, wherever the crash shows up (the check's call, or the try line's).
    const inside = blocks.filter((block) => line > block.start && line <= block.end).at(-1);
    const read = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}(?![\\w(])`);
    if (inside && /^return\b/.test(body) && read.test(maskStrings(body))) {
      const ingredients = recipeIngredients(code, inside.recipe) ?? [];
      const boxes = [
        ...new Set(defined.filter((entry) => entry.line > inside.start && entry.line < line).map((entry) => entry.name)),
      ].filter((box) => !ingredients.includes(box));
      // One or two letters off one of the recipe's own names: a spelling slip, which keeps its own row.
      if (!fromExample && closeName(name, [...boxes, ...ingredients])) return null;
      const lead = fromExample
        ? `\`${name}\` comes from Mar'tu's example.`
        : `${lineWord(line)} hands back \`${name}\`, but no line in \`${inside.recipe}\` makes a box by that name.`;
      if (boxes.length > 0) {
        return explain(
          "not-in-recipe",
          "Not a box in this recipe",
          `${lead} ${boxes.length === 1 ? `This recipe's box is ${list(boxes)}: hand that back.` : `This recipe's boxes are ${list(boxes)}: hand back the one that holds the answer.`}`,
          raw,
        );
      }
      if (ingredients.length > 0) {
        return explain(
          "not-in-recipe",
          "Not a name in this recipe",
          `${fromExample ? `${lead} \`${inside.recipe}\` has no box by that name.` : `${lineWord(line)} hands back \`${name}\`, but \`${inside.recipe}\` has no box or ingredient by that name.`} ${ingredients.length === 1 ? `Its ingredient is ${list(ingredients)}` : `Its ingredients are ${list(ingredients)}`}: work the answer out from ${ingredients.length === 1 ? "that" : "those"}.`,
          raw,
        );
      }
    }
  }
  // Every line that makes `name` is inside one recipe (or is its `def` line, as an ingredient), and this line is not.
  const home = made.length > 0 ? blocks.find((block) => made[0].line >= block.start && made[0].line <= block.end) : undefined;
  if (!home || line === null || (line >= home.start && line <= home.end) || home.recipe === name) return null;
  if (!made.every((entry) => entry.line >= home.start && entry.line <= home.end)) return null;
  const ingredient = made.some((entry) => entry.line === home.start);
  // The line sits inside ANOTHER recipe (`return total` in `max_fuel_for`, when `total` is `max_mana_for`'s box): the
  // advice is that recipe's own names, never "out here, catch what it hands back".
  const here = blocks.filter((block) => line > block.start && line <= block.end).at(-1);
  if (here && here.recipe !== home.recipe) {
    const hereIngredients = recipeIngredients(code, here.recipe) ?? [];
    const hereBoxes = [
      ...new Set(defined.filter((entry) => entry.line > here.start && entry.line < line).map((entry) => entry.name)),
    ].filter((box) => !hereIngredients.includes(box));
    const belongs = `\`${name}\` belongs to \`${home.recipe}\`${ingredient ? " (it is one of its ingredients)" : ""}, so only that recipe can use it.`;
    const instead = /^return\b/.test(body) && hereBoxes.length > 0
      ? `Inside \`${here.recipe}\`, hand back its own box, \`${hereBoxes.at(-1)}\`.`
      : hereIngredients.length > 0
        ? `Inside \`${here.recipe}\`, use its own ${hereIngredients.length === 1 ? "ingredient" : "ingredients"}, ${list(hereIngredients)}${hereBoxes.length > 0 ? `, and its own ${hereBoxes.length === 1 ? "box" : "boxes"}, ${list(hereBoxes)}` : ""}.`
        : `Inside \`${here.recipe}\`, make what it needs there, or hand it over as an ingredient.`;
    return explain("made-inside-recipe", "Another recipe's name", `${belongs} ${instead}`, raw);
  }
  if (ingredient) {
    const lead = `\`${name}\` is an ingredient of \`${home.recipe}\`, so it only exists inside the recipe while a call runs it. Line ${line} is outside the recipe`;
    // `warn(hero_name)`: the call itself hands the ingredient over, so the call needs a value of its own.
    if (new RegExp(`(^|[^\\w.])${escapeRegExp(home.recipe)}\\s*\\(`).test(maskStrings(body))) {
      return explain("made-inside-recipe", "Only inside the recipe", `${lead}. Out here, hand over a value itself in the call.`, raw);
    }
    // `print(hero_name + ", get inside!")` at the bottom, while `pass` still sits in `warn`: the line belongs inside.
    const steps = (code ?? "").split("\n").slice(home.start, home.end).map((row) => codePart(row).trim()).filter(Boolean);
    const where = steps.length === 1 && steps[0] === "pass" ? ", in place of `pass`, four spaces in" : ", four spaces in";
    return explain("made-inside-recipe", "Only inside the recipe", `${lead}: move this line inside \`${home.recipe}\`${where}.`, raw);
  }
  return explain(
    "made-inside-recipe",
    "Only inside the recipe",
    `\`${name}\` is made inside \`${home.recipe}\`, so it only exists inside that recipe. Line ${line} is outside it. Out here, catch what the recipe hands back in a box of your own: the call goes on the right of \`=\`.`,
    raw,
  );
}

/** `return` with no spaces in front, under a recipe: it fell out of the recipe (Python: "'return' outside function"). */
function explainReturnOutside(code: string, line: number | null, raw: string): CourseExplanation {
  const above = line ? recipeBlocks((code ?? "").split("\n").slice(0, line - 1).join("\n")).at(-1) : undefined;
  if (above && line && above.end === line - 1) {
    return explain(
      "indent",
      "Indent the return",
      `Line ${line}'s \`return\` has no spaces in front, so it is outside the recipe \`${above.recipe}\`. Give it the same spaces as the lines above it.`,
      raw,
    );
  }
  return explain(
    "indent",
    "return goes in a recipe",
    `${lineWord(line)} has \`return\` outside any recipe. \`return\` only works inside a recipe (function), indented under its \`def\` line, to hand a value back.`,
    raw,
  );
}

function explainSyntax(
  message: string,
  type: string,
  text: string,
  line: number | null,
  raw: string,
  code = "",
  context?: ExplainContext,
): CourseExplanation {
  const lower = message.toLowerCase();

  if (/unterminated triple-quoted string/.test(lower)) {
    return explain(
      "unclosed-triple-quote",
      "Missing quotes",
      `A block of text that starts with three quotes${onLine(line)} never ends. Add the same three quotes where the text should stop.`,
      raw,
    );
  }
  if (/unterminated string literal|eol while scanning string literal/.test(lower)) {
    return quotesProblem(text, line, raw, code, context);
  }
  const curly = message.match(/invalid character '([“”‘’])'/);
  if (curly) {
    return explain(
      "curly-quote",
      "Curly quotes",
      `${lineWord(line)} has a curly quote ${curly[1]} that Python can't read. Python only understands straight quotes: " or '. Delete it and type the quote again in the editor.`,
      raw,
    );
  }
  if (/invalid non-printable character/.test(lower)) {
    return explain(
      "hidden-character",
      "Hidden character",
      `${lineWord(line)} has a hidden character Python can't read, often from copy and paste. Delete the spaces on that line and type them again.`,
      raw,
    );
  }
  const odd = message.match(/invalid character '(.)'/);
  if (odd) {
    return explain(
      "odd-character",
      "Odd character",
      `${lineWord(line)} has a character Python can't read: ${odd[1]}. If you copied this code, type that part again yourself.`,
      raw,
    );
  }

  const backwards = explainBackwardsSign(text, line, raw);
  if (backwards) return backwards;

  // From Unit 3 on, a `def name(` line is a recipe being written: never "make a variable" advice there.
  const recipeHeader = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) && RECIPE_HEADER.test(codePart(text));
  if (recipeHeader && /^invalid syntax/.test(lower)) {
    const ingredient = explainQuotedIngredient(text, line, raw, context);
    if (ingredient) return ingredient;
  }
  // `max_fuel_for(cells) = cells * 5`: before `compare-with-double-equals`, which would say "use ==".
  if (unitAtLeast(context, FUNCTIONS_UNIT_ORDER)) {
    const math = explainRecipeLikeMath(message, text, line, raw);
    if (math) return math;
    if (/'return' outside function/.test(lower)) return explainReturnOutside(code, line, raw);
    // `def max_fuel_for(cells) = cells * 5`, `def max_fuel_for = cells * 5`, `def ("say_steady"):`: a recipe, written
    // half like a box. Never "make a box" advice, and never "add a colon" again and again.
    const recipe = explainDefLikeMath(text, line, raw) ?? explainRecipeMadeAsBox(text, code, line, raw, context);
    if (recipe) return recipe;
  }

  const defFix = recipeHeader ? null : defForVariable(text);
  if (defFix && printOnlyTask(context)) return defInPrintTask(text, raw);
  // Unit 3 on, in the unit's words: def makes recipes, = makes boxes.
  if (defFix && unitAtLeast(context, FUNCTIONS_UNIT_ORDER)) {
    return explain(
      "def-for-variable",
      "def makes recipes",
      `\`def\` makes recipes (functions), not boxes. To make a box, write the name, an equals sign, then the value, with no \`def\`: \`${defFix}\``,
      raw,
    );
  }
  if (defFix) {
    return explain(
      "def-for-variable",
      "def makes functions",
      `def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value, with no def: ${defFix}`,
      raw,
    );
  }

  if (/^invalid syntax/.test(lower)) {
    const keyword = explainKeywordShape(text, line, raw);
    if (keyword) return keyword;
  }

  const shape = explainNameShape(text, line, raw);
  if (shape) return shape;

  if (/^invalid syntax/.test(lower)) {
    const chain = explainChain(code, text, line, raw);
    if (chain) return chain;
  }

  // Unit 4: `chalk_wall(2) = 47`, round brackets after a list's name (before the `==` row's "use two equals signs").
  if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
    const list = explainListAssignedWithCall(message, code, text, line, raw);
    if (list) return list;
  }

  // `said_yes = answer.lower() = "yes"`, `assert passed = False`: one `=` where a question needs `==`.
  if (/^invalid syntax|cannot assign to (function call|expression|comparison|attribute)/.test(lower) && !/forgot a comma/.test(lower)) {
    const asked = /maybe you meant '=='/.test(lower) || /^\s*(if|elif|while|assert)\b/.test(text) || /cannot assign/.test(lower)
      ? doubleEqualsFix(text)
      : null;
    if (asked) {
      return explain(
        "compare-with-double-equals",
        "Use == to compare",
        `${lineWord(line)} has one \`=\` where a question needs two. One \`=\` puts a value in a box; \`==\` asks "is it the same?". Write: \`${asked}\``,
        raw,
      );
    }
  }

  if (/cannot assign to literal/.test(lower)) {
    // `"weapon" = "Telegun"`: the name is first already, but in quotes (a box's name never has quotes).
    const quotedName = codePart(text).trim().match(/^(["'])([A-Za-z_]\w*)\1\s*=(?!=)\s*(.+)$/);
    const right = quotedName?.[3]?.trim() ?? "";
    if (quotedName && !KEYWORDS.has(quotedName[2]) && !(/^[A-Za-z_]\w*$/.test(right) && !KEYWORDS.has(right))) {
      return explain(
        "quoted-name",
        "No quotes on a name",
        `A box's name has no quotes${onLine(line)}. Take the quotes off ${quotedName[2]}: \`${quotedName[2]} = ${right}\``,
        raw,
      );
    }
    const swap = text.match(/^\s*(.+?)\s*=(?!=)\s*([A-Za-z_]\w*)\s*$/);
    const taskName = (context?.names ?? []).find((name) => !COMMON_BUILTINS.includes(name)) ?? "name";
    const example = swap ? `${swap[2]} = ${swap[1]}` : `${taskName} = "value"`;
    return explain(
      "name-goes-first",
      "Name goes first",
      `The name goes on the left of = and the value goes on the right, like this: ${example}`,
      raw,
    );
  }
  if (/missing parentheses in call to 'print'/.test(lower)) {
    const inside = codePart(text).trim().match(/^print\s+(.+)$/)?.[1];
    return explain(
      "print-needs-brackets",
      "print needs ( )",
      `print needs brackets ( ) around what it shows${onLine(line)}, like this: print(${inside ?? '"Hello"'})`,
      raw,
    );
  }
  if (/maybe you meant '==' or ':=' instead of '='|maybe you meant '==' instead of '='/.test(lower)) {
    const fixed = doubleEqualsFix(text);
    return explain(
      "compare-with-double-equals",
      "Use == to compare",
      fixed
        ? `To check if two things are equal${onLine(line)}, use two equals signs: ==. One = is only for making a variable. Write: \`${fixed}\``
        : `To check if two things are equal${onLine(line)}, use two equals signs: ==. One = is only for making a variable.`,
      raw,
    );
  }
  if (/''[A-Za-z]/.test(codePart(text))) {
    // `print(''Shield up'')`: two apostrophes typed for one double quote.
    return explain(
      "two-single-quotes",
      "Two ' are not one \"",
      `${lineWord(line)} has two ' marks side by side. Python reads '' as empty text, not as a " mark. Use one " at each end of the text: ${codePart(text).replace(/''/g, '"').trim()}`,
      raw,
    );
  }
  if (/perhaps you forgot a comma/.test(lower)) {
    // Unit 4: bare words inside [ ] (`[storm kick, 7]`, or an item of a list over several lines), before the
    // missing-comma rows: they are words to quote, not two items.
    if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
      const words = explainUnquotedInList(code, text, line, raw);
      if (words) return words;
    }
    // A list or dictionary over several lines: the comma at the end of this line is missing.
    const open = openBefore(code, line);
    const body = codePart(text);
    if (open.length > 0 && body.trim() && !/[,([{]$/.test(body)) {
      const what = { "{": "a dictionary { }", "[": "a list [ ]", "(": "( )" }[open[open.length - 1]] ?? "( )";
      return explain(
        "missing-comma-in-list",
        "Missing comma",
        `Inside ${what}, every item except the last needs a comma after it. Add a comma at the end of line ${line}: ${body.trim()},`,
        raw,
      );
    }
    const option = explainUnquotedOption(text, line, raw);
    if (option) return option;
    const unquoted = explainUnquoted(text, code, line, raw);
    if (unquoted) return unquoted;
    // Unit 4: `chalk_wall = [48 48, 47]`, numbers side by side in a list (never "or + to join text").
    if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
      const comma = explainListMissingComma(text, line, raw);
      if (comma) return comma;
    }
    const inside = text.match(/\(([^()"']*)\)/)?.[1]?.trim();
    // In a call that takes several values (not print), the commas split the values: never quote them together.
    const callee = codePart(text).trim().match(/^(?:[A-Za-z_]\w*\s*=(?!=)\s*)?([A-Za-z_][\w.]*)\s*\(/)?.[1];
    const several = callee !== undefined && callee !== "print" && (inside ?? "").includes(",");
    if (inside && !several && /^[A-Za-z0-9][A-Za-z0-9 ,!?.']*[A-Za-z0-9!?.]$/.test(inside) && /[A-Za-z]/.test(inside) && inside.includes(" ")) {
      return explain("unquoted-words", "Missing quotes?", `If ${inside} is text, put quotes around it: "${inside}". Text needs quotes.`, raw);
    }
    return explain(
      "missing-comma",
      "Missing comma or +",
      `${lineWord(line)} has two values side by side with nothing between them. Put a comma between them, or + to join text.`,
      raw,
    );
  }
  const neverClosed = message.match(/'([([{])' was never closed/);
  if (neverClosed) {
    const opener = neverClosed[1];
    const closing = CLOSER[opener] ?? ")";
    const scan = scanLine(text);
    const body = codePart(text);
    // `print("Shield up!)"`: the ) went inside the quotes, so it is part of the text.
    const inside = body.match(/^(.*)([)\]}])(["'])\s*$/);
    if (inside && !scan.unterminated && scan.open.length === 1 && CLOSER[scan.open[0]] === inside[2]) {
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `The ${inside[2]}${onLine(line)} is inside the quotes, so Python reads it as part of the text. Move it after the closing quote: ${inside[1]}${inside[3]}${inside[2]}`.trim(),
        raw,
      );
    }
    if (body && !scan.unterminated && scan.open.length > 0 && !/[([{]$/.test(body)) {
      const fixed = `${body}${closersFor(scan.open)}`;
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `A ${opener}${onLine(line)} opens but never closes. Brackets come in pairs, like quotes. Add ${closing} at the end of the line: ${fixed.trim()}`,
        raw,
      );
    }
    if (/[([{]$/.test(body)) {
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `The ${opener}${onLine(line)} opens, but its ${closing} never comes. Add ${closing} on its own line after the last item.`,
        raw,
      );
    }
    return explain(
      "never-closed",
      `Missing ${closing}`,
      `A ${opener}${onLine(line)} never gets its closing ${closing}. Brackets come in pairs: add ${closing} where it should end.`,
      raw,
    );
  }
  const unmatched = message.match(/unmatched '([)\]}])'/);
  if (unmatched) {
    return explain(
      "extra-bracket",
      `Extra ${unmatched[1]}`,
      `${lineWord(line)} has an extra ${unmatched[1]}. Remove it, or add the opening bracket it belongs to.`,
      raw,
    );
  }
  if (/closing parenthesis '.' does not match opening parenthesis/.test(lower)) {
    return explain(
      "brackets-dont-match",
      "Brackets don't match",
      `The brackets${onLine(line)} don't match. ( closes with ), [ closes with ], and { closes with }.`,
      raw,
    );
  }
  if (/expected '\('/.test(lower) && /^\s*def\b/.test(text)) {
    const recipe = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? codePart(text).match(/^\s*def\s+([A-Za-z_]\w*)\s*:?\s*$/)?.[1] : undefined;
    if (recipe) {
      return explain("def-needs-brackets", "def needs ( )", `A \`def\` line needs ( ) after the recipe's name, then a colon: \`def ${recipe}():\``, raw);
    }
    return explain("def-needs-brackets", "def needs ( )", `A def line needs ( ) after the function's name, then a colon, like this: def greet():`, raw);
  }
  if (/expected ':'/.test(lower)) {
    return explainMissingColon(code, text, line, raw);
  }
  if (/invalid decimal literal|invalid imaginary literal/.test(lower)) {
    return explainStuckNumber(text, code, line, raw);
  }
  if (/expected an indented block|unexpected indent|unindent does not match/.test(lower) || type === "IndentationError") {
    return explainIndent(message, line, raw, unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? code : "");
  }
  if (/^invalid syntax/.test(lower)) {
    // Unit 4: the wall's row copied as it looks (`hours = 48 48 47`), and `chalk_wall.pop[]`.
    if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
      const list = explainNumbersSideBySide(text, line, raw) ?? explainEmptySquareCall(code, text, line, raw);
      if (list) return list;
    }
    // `if hours_left < 3;`: a semicolon typed for the colon.
    if (/;\s*$/.test(codePart(text)) && headerWithColon(code, text, line)) return explainMissingColon(code, text, line, raw);
    const option = explainUnquotedOption(text, line, raw);
    if (option) return option;
    const unquoted = explainUnquoted(text, code, line, raw);
    if (unquoted) return unquoted;
    const body = codePart(text).trim();
    // `Night watch`: plain words on a line, meant as a note or as words to show.
    if (/^[A-Za-z][A-Za-z0-9 ,.!?;:-]*$/.test(body) && /\s/.test(body) && !KEYWORDS.has(body.split(/\s+/)[0] ?? "")) {
      return explain(
        "unquoted-words",
        "Words with no quotes",
        `${lineWord(line)} is plain words, so Python tries to read them as code. To make it a note, start the line with #: \`# ${body}\`. To show the words, put them in quotes inside print( ): \`print("${body}")\``,
        raw,
      );
    }
    // `print(_ - =)`: symbols to show, with no quotes around them.
    const inside = body.match(/^print\s*\(\s*([^"'()]+?)\s*\)$/)?.[1];
    if (inside) {
      return explain(
        "unquoted-words",
        "Missing quotes?",
        `${lineWord(line)} has no quotes inside print( ), so Python tries to read ${inside} as code. To show it as it is, put it in quotes: \`print("${inside}")\``,
        raw,
      );
    }
  }
  // A colon is only worth naming once the code has a line that needs one (if, for, while, def ...).
  const colons = /^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\b/m.test(code ?? "");
  return explain(
    "cant-read-line",
    "Python can't read this",
    `Python could not read line ${line ?? "?"}. Look for a missing quote${colons ? ", a missing bracket ( ), or a missing colon :." : " or a missing bracket ( )."}`,
    raw,
  );
}

/** `code` only from Unit 3 on (recipes): it reads a recipe with no step yet. Without it, the older rows. */
function explainIndent(message: string, line: number | null, raw: string, code = ""): CourseExplanation {
  const after = message.match(/expected an indented block after (.+?) on line (\d+)/);
  // A recipe with no step under its def line (its `pass` deleted, or only a note left): indenting the next line
  // (a blank, a note, or the next `def`) would not mend it, so the rule is what to say.
  const header = after && after[1] === "function definition" ? Number(after[2]) : null;
  const between = header !== null && line !== null ? (code ?? "").split("\n").slice(header, line - 1) : [];
  const recipe = header !== null ? codePart(sourceLine(code, header)).match(/^\s*def\s+([A-Za-z_]\w*)/)?.[1] : undefined;
  if (recipe && between.length > 0 && between.every((row) => codePart(row).trim() === "")) {
    // A note indented under the def line is the recipe's only "step" (a note above the next def is not).
    const indent = indentOf(sourceLine(code, header ?? 0));
    const note = between.some((row) => row.trim().startsWith("#") && indentOf(row) > indent) ? ": a note with # doesn't count" : "";
    return explain(
      "indent",
      "A recipe needs a step",
      `\`${recipe}\` has no steps yet, and a recipe needs at least one step inside${note}. Write its step under the def line, four spaces in (or put \`pass\` back while you think).`,
      raw,
    );
  }
  if (after) {
    const what = after[1]
      .replace(/^'(\w+)' statement$/, "the $1")
      .replace(/^function definition$/, "the def")
      .replace(/^class definition$/, "the class");
    return explain("indent", "Indent this line", `The line after line ${after[2]} belongs inside ${what}, so it needs 4 spaces at the start.`, raw);
  }
  if (/expected an indented block/.test(message)) {
    return explain("indent", "Indent this line", `${lineWord(line)} needs 4 spaces at the start, because it belongs inside the block above it.`, raw);
  }
  if (/unexpected indent/.test(message)) {
    return explain(
      "indent",
      "Extra spaces",
      line === 1
        ? "Line 1 starts with spaces it should not have. Delete the spaces so it starts at the left edge."
        : `${lineWord(line)} starts with spaces it should not have. Move it back so it lines up with the line above.`,
      raw,
    );
  }
  if (/unindent does not match/.test(message)) {
    return explain(
      "indent",
      "Spaces don't line up",
      `${lineWord(line)} is indented a different amount than the lines around it. Line it up exactly with its block, using 4 spaces per level.`,
      raw,
    );
  }
  if (/tabs and spaces/.test(message)) {
    return explain("indent", "Tabs and spaces", `${lineWord(line)} mixes tabs and spaces. Delete the indent and use 4 spaces instead.`, raw);
  }
  return explain("indent", "Spaces at the start", `The spaces at the start of line ${line ?? "?"} don't fit. Use 4 spaces for each level inside a block.`, raw);
}

function explainName(
  message: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation {
  const name = message.match(/name '([^']+)' is not defined/)?.[1];
  if (!name) {
    return explain("unknown-name", "Unknown name", "Python does not know one of the names on this line. Make it first, or check the spelling.", raw);
  }

  // `if ___:`: the starter's blank, still there. Python reads it as a name.
  if (/^_{2,}$/.test(name)) return blankLeft(name, line, raw);

  const forgotImport = message.match(/Did you forget to import '([^']+)'/)?.[1];
  if (forgotImport) {
    return explain("missing-import", "Missing import", `To use ${forgotImport}, add this line at the top of your code: import ${forgotImport}`, raw);
  }

  // `roll = randint(1, 6)`: randint lives inside random.
  if (name === "randint" && new RegExp(`(^|[^\\w.])randint\\s*\\(`).test(text)) {
    const fixed = codePart(text).trim().replace(/(^|[^\w.])randint\s*\(/g, "$1random.randint(");
    const imported = definedNames(code).some((entry) => entry.name === "random");
    return explain(
      "randint-needs-random",
      "randint lives in random",
      imported
        ? `${lineWord(line)} calls \`randint\` on its own, but it lives inside \`random\`. Put \`random.\` in front of it: \`${fixed}\``
        : `${lineWord(line)} calls \`randint\` on its own, but it lives inside \`random\`, and this code never brings \`random\` in. Add \`import random\` as the first line, then write: \`${fixed}\``,
      raw,
    );
  }

  // `lower(answer)`: lower belongs to the text, after a dot.
  const method = STRING_METHODS.has(name) ? codePart(text).trim().match(new RegExp(`(^|[^\\w.])${name}\\s*\\(\\s*([^()]+?)\\s*\\)`)) : null;
  if (method) {
    const owner = /^[A-Za-z_]\w*$|^["'][^"']*["']$/.test(method[2]) ? method[2] : `(${method[2]})`;
    const body = codePart(text).trim();
    const at = (method.index ?? 0) + method[1].length;
    const fixed = `${body.slice(0, at)}${owner}.${name}()${body.slice((method.index ?? 0) + method[0].length)}`.trim();
    return explain(
      "method-as-function",
      `${name} goes after a dot`,
      `${lineWord(line)} uses \`${name}\` like a function on its own, but it belongs to the text, after a dot: the text first, then \`.${name}()\`. Write: \`${fixed}\``,
      raw,
    );
  }

  // `hero == "Lucky"` on a line of its own: `==` only asks, so `hero` was never made.
  const alone = comparisonAlone(text);
  if (alone && alone.op === "==" && alone.left === name) {
    return explain(
      "comparison-alone",
      "== asks, = makes",
      `${lineWord(line)} uses \`==\`, which only asks "is it the same?". It makes nothing, so \`${name}\` was never made. To put a value in a box, use one \`=\`: \`${name} = ${alone.right}\``,
      raw,
    );
  }

  const dash = dashFix(text, name);
  if (dash && printOnlyTask(context)) return dashInPrintTask(text, line, raw, "dash-for-equals");
  if (dash) {
    return explain(
      "dash-for-equals",
      "Dash or equals?",
      `${lineWord(line)} uses a dash - where Python needs an equals sign =. To make a variable, write: ${dash}`,
      raw,
    );
  }

  const colonLine = (code ?? "")
    .split("\n")
    .find((row) => new RegExp(`^${escapeRegExp(name)}\\s*:\\s*\\S`).test(row));
  if (colonLine) {
    const value = colonLine.replace(new RegExp(`^${escapeRegExp(name)}\\s*:\\s*`), "").trim();
    return explain(
      "colon-for-equals",
      "Colon or equals?",
      `It looks like you made ${name} with a colon. Use an equals sign to make a variable: ${name} = ${value}`,
      raw,
    );
  }

  // Unit 3 on: a recipe called above its `def` or not made yet, or a name that only lives inside a recipe.
  if (unitAtLeast(context, FUNCTIONS_UNIT_ORDER)) {
    const recipe = explainRecipeName(name, code, text, line, raw, context);
    if (recipe) return recipe;
  }

  const defined = definedNames(code);
  const builtins = suggestableBuiltins(code, context);
  const known = [...defined.map((entry) => entry.name), ...builtins];
  // Trust Python's own "Did you mean" only for names this student has met (not ord, iter, map, any ...).
  const suggested = message.match(/Did you mean: '([^']+)'/)?.[1];
  const trusted =
    suggested && !suggested.startsWith("_") && (known.includes(suggested) || suggested.toLowerCase() === name.toLowerCase())
      ? suggested
      : null;
  // Names the student made can be 2 letters off; Python's own names only 1 (so count is not "round").
  const close = trusted ?? closeName(name, defined.map((entry) => entry.name)) ?? closeName(name, builtins, 1);

  // `canes_women` alone on a line: no `=`, no print( ). Python looked it up and found nothing.
  if (codePart(text).trim() === name) {
    if (close === "print") {
      return explain(
        "lone-name",
        "A name on its own",
        `${lineWord(line)} is only the word ${name}. Did you mean print? To show words, write print("your words").`,
        raw,
      );
    }
    if (close && !COMMON_BUILTINS.includes(close)) {
      return explain(
        "lone-name",
        "A name on its own",
        `${lineWord(line)} is only a name on its own: ${name}. Did you mean ${close}? To show what ${close} holds, write print(${close}).`,
        raw,
      );
    }
    if (printOnlyTask(context)) {
      return explain(
        "lone-name",
        "Words with no quotes",
        `${lineWord(line)} is only the word ${name}, with no quotes and no print, so Python reads it as a name it does not know. To show it, write \`print("${name}")\``,
        raw,
      );
    }
    return explain(
      "lone-name",
      "A name on its own",
      `${lineWord(line)} is only a name on its own, so Python looked for a variable called ${name} and found none. To make one, write ${name} = and then a value. To show words, write print("your words").`,
      raw,
    );
  }

  // `print("Hello, " + traveler)` in a task whose variable is `name`: copied from the worked example.
  if (exampleOnlyNames(context).includes(name) && !defined.some((entry) => entry.name === name)) {
    const assignedHere = text.match(/^\s*([A-Za-z_]\w*)\s*=(?!=)/)?.[1];
    // `note = get_note()`, copied from a Teach me hint: a recipe called by the example's name. Point at the task's own
    // recipe that shares a word with it (`get_greeting`), when there is one.
    const calledHere = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`).test(maskStrings(codePart(text)));
    const recipes = calledHere && unitAtLeast(context, FUNCTIONS_UNIT_ORDER)
      ? (context?.names ?? []).filter((task) => task !== name && taskRecipe(task, code, context))
      : [];
    const theirs = similarBox(name, recipes.map((task) => ({ name: task, line: 0 })), [name]);
    if (theirs) {
      return explain(
        "example-name",
        "Name from the example",
        `\`${name}\` comes from Mar'tu's example. This task's recipe is \`${theirs.name}\`: call that one, letter for letter.`,
        raw,
      );
    }
    return explain(
      "example-name",
      "Name from the example",
      exampleNameHint(name, taskNamesInstead(code, line, context, [name, ...(assignedHere ? [assignedHere] : [])])),
      raw,
    );
  }

  if (close) {
    const taskWay = nameAgainstTask(name, close, code, line, defined, context, raw);
    if (taskWay) return taskWay;
  }
  if (close && close.toLowerCase() === name.toLowerCase()) {
    return explain(
      "capital-letters",
      "Capital letters matter",
      `Python sees ${name} and ${close} as different names. Use ${close}, with the same capital letters every time.`,
      raw,
    );
  }
  if (close) {
    return explain("spelling", "Check the spelling", `Python doesn't know ${name}. Did you mean ${close}? A name must be spelled the same way every time.`, raw);
  }

  const grow = text.match(new RegExp(`^\\s*${escapeRegExp(name)}\\s*([-+*/%]|//|\\*\\*)=`));
  if (grow) {
    return explain(
      "make-it-first",
      "Make it first",
      `${lineWord(line)} changes ${name}, but ${name} has no value yet. Give it a starting value first, like ${name} = 0`,
      raw,
    );
  }

  const later = defined.find((entry) => entry.name === name && line !== null && entry.line > line);
  if (later) {
    return explain(
      "used-too-early",
      "Used too early",
      `Line ${line} uses ${name}, but ${name} is only made on line ${later.line}. Python runs from top to bottom, so make ${name} first.`,
      raw,
    );
  }

  // `print(hero)` when no line makes `hero` yet, and `hero` is one of the task's own boxes: make it, above.
  if ((context?.names ?? []).includes(name) && !defined.some((entry) => entry.name === name)) {
    const bare = line !== null ? explainQuietSlip((code ?? "").split("\n").slice(0, line - 1).join("\n")) : null;
    if (bare && bare.kind === "bare-value") {
      const value = codePart(sourceLine(code, bare.line)).trim();
      return explain(
        "not-made-yet",
        "Not made yet",
        `${name} is one of this task's boxes, but no line makes it yet. Line ${bare.line} has the value ${value} on its own: put \`${name} = \` in front of it, \`${name} = ${value}\``,
        raw,
      );
    }
    return explain(
      "not-made-yet",
      "Not made yet",
      `${name} is one of this task's boxes, but no line makes it yet. Make it ${line ? `above line ${line}` : "first"}, starting the line with \`${name} = \``,
      raw,
    );
  }

  // `if choice == yes:`: one word with no quotes after `==`, and no box by that name anywhere.
  const compared = maskStrings(text).match(new RegExp(`(==|!=)\\s*${escapeRegExp(name)}(?![\\w.(\\[])`));
  if (compared && !defined.some((entry) => entry.name === name) && !COMMON_BUILTINS.includes(name)) {
    const at = (compared.index ?? 0) + compared[0].length - name.length;
    const fixed = codePart(`${text.slice(0, at)}"${name}"${text.slice(at + name.length)}`).trim();
    return explain(
      "unquoted-option",
      "Text needs quotes",
      `${lineWord(line)} compares with \`${name}\`, a word with no quotes, so Python looked for a box called \`${name}\` and found none. If you meant the word, put it in quotes: \`${fixed}\``,
      raw,
    );
  }

  const called = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`).test(text);
  if (called) {
    // `def` is taught in the Functions unit: before it, never send a student to make a function.
    const beforeFunctions = context?.unitOrder !== undefined && context.unitOrder < FUNCTIONS_UNIT_ORDER;
    return explain(
      "unknown-function",
      "Unknown function",
      beforeFunctions
        ? `Python doesn't know a function called ${name}. Check the spelling against the task, letter for letter: Python's own functions, like print(), are all small letters.`
        : unitAtLeast(context, FUNCTIONS_UNIT_ORDER)
          ? `Python doesn't know a recipe (function) called ${name}. Check the spelling, or make it with def before you use it.`
          : `Python doesn't know a function called ${name}. Check the spelling, or make it with def before you use it.`,
      raw,
    );
  }
  // A lowercase word in code that already made variables is often a name copied from somewhere else
  // (the example, a friend's screen), so offer both fixes, the task's variables first.
  const assignedHere = text.match(/^\s*([A-Za-z_]\w*)\s*=(?!=)/)?.[1];
  // Unit 3 on, inside a recipe: a name like one of its ingredients (`hero` for `hero_name`, `damage` for
  // `base_damage`). Quotes would print the word itself on every call, so the fix is the ingredient, letter for letter.
  const kitchen = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) && line !== null
    ? recipeBlocks(code).filter((block) => line > block.start && line <= block.end).at(-1)
    : undefined;
  const ingredients = kitchen ? (recipeIngredients(code, kitchen.recipe) ?? []) : [];
  const likeIngredient = kitchen
    ? similarBox(name, ingredients.map((entry) => ({ name: entry, line: kitchen.start })), [name])?.name
    : undefined;
  if (kitchen && likeIngredient) {
    const its = ingredients.length === 1
      ? `Its ingredient is \`${likeIngredient}\`: use it letter for letter.`
      : `Its ingredients are ${ingredients.map((entry) => `\`${entry}\``).join(ingredients.length === 2 ? " and " : ", ")}: use \`${likeIngredient}\`, letter for letter.`;
    return explain("unknown-name", "Not an ingredient", `\`${name}\` is not an ingredient of \`${kitchen.recipe}\`. ${its}`, raw);
  }
  const earlier = taskNamesInstead(code, line, context, [name, ...(assignedHere ? [assignedHere] : [])]);
  if (/^[a-z][a-z0-9_]*$/.test(name) && earlier.length > 0) {
    // `mana - mana_cost`: a number is wanted there, so quotes (text) would only lead to the next crash.
    const quotes = inMath(text, name) ? "" : ` If it's text, put quotes around it: "${name}"`;
    // Only names a letter or two away are worth offering as "use this one": a list of unrelated task names
    // (bad_line, error_type ...) sends the student after the wrong thing.
    const nearTask = (context?.names ?? []).filter((task) => task !== name && editDistance(task.toLowerCase(), name.toLowerCase()) <= 2);
    if (nearTask.length > 0) {
      return explain(
        "unknown-name",
        "Unknown name",
        `Python doesn't know ${name}. If it's a variable, use this task's name: ${nearTask.slice(0, 2).join(" or ")} (spelled exactly).${quotes}`,
        raw,
      );
    }
    const similar = similarBox(name, defined, [name, ...(assignedHere ? [assignedHere] : [])]);
    // `scout.step(north)`: a lone word inside a call's brackets. A recipe's name (`step_north`) is never the box it
    // meant: lead with the quotes, then a box of the code's own, if one is like it.
    const recipeNames = new Set(recipeBlocks(code).map((block) => block.recipe));
    if (similar && recipeNames.has(similar.name) && loneArgument(text, name)) {
      const box = similarBox(name, defined.filter((entry) => !recipeNames.has(entry.name)), [name, ...(assignedHere ? [assignedHere] : [])]);
      const fixed = quoteLoneArgument(text, name);
      return explain(
        "unquoted-word",
        "Missing quotes?",
        `Python doesn't know \`${name}\`: no line in your code makes it. If it's text, put quotes around it: \`${fixed}\`${box ? ` If you meant a box, line ${box.line} makes \`${box.name}\`.` : ""}`,
        raw,
      );
    }
    if (similar) {
      return explain(
        "unknown-name",
        "Unknown name",
        `Python doesn't know ${name}: no line in your code makes it. Line ${similar.line} makes \`${similar.name}\`, which has a similar name.${quotes}`,
        raw,
      );
    }
    const shown = earlier.slice(-3).join(", ");
    const whose = context?.names?.length ? "this task's names" : "one your code made";
    return explain(
      "unknown-name",
      "Unknown name",
      `Python doesn't know ${name}. If it's a variable, use ${whose}: ${shown} (spelled exactly).${quotes}`,
      raw,
    );
  }
  if (/^[A-Za-z]+$/.test(name)) {
    return explain(
      "unquoted-word",
      "Missing quotes?",
      `Python doesn't know the name ${name}. Did you mean to put quotes around it? Text needs quotes: "${name}"`,
      raw,
    );
  }
  return explain("unknown-name", "Unknown name", `Python doesn't know ${name} yet${onLine(line)}. Make it first (${name} = ...), or check the spelling.`, raw);
}

/** `name` is one whole value inside a call's brackets on this line: `scout.step(north)`, `heal(hero, 5)`. */
function loneArgument(text: string, name: string): boolean {
  const mask = maskStrings(codePart(text));
  return new RegExp(`[(,]\\s*${escapeRegExp(name)}\\s*[,)]`).test(mask);
}

/** The line with that lone word in quotes: `scout.step("north")`. */
function quoteLoneArgument(text: string, name: string): string {
  const body = codePart(text).trim();
  const mask = maskStrings(body);
  const at = mask.search(new RegExp(`(?<=[(,]\\s*)${escapeRegExp(name)}(?=\\s*[,)])`));
  return at < 0 ? body : `${body.slice(0, at)}"${name}"${body.slice(at + name.length)}`;
}

/** `name` is a number in math on this line (`mana - mana_cost`, `cost * 2`, `3 + bonus`): text can't go there. */
function inMath(text: string, name: string): boolean {
  const mask = maskStrings(codePart(text));
  const at = escapeRegExp(name);
  if (new RegExp(`(?:[-*/%]\\s*${at}(?![\\w.(])|(?<![\\w.])${at}\\s*[-*/%])`).test(mask)) return true;
  return new RegExp(`(?:\\d\\s*\\+\\s*${at}(?![\\w.(])|(?<![\\w.])${at}\\s*\\+\\s*\\d)`).test(mask);
}

/**
 * A box the code makes whose name shares a word with `name` (`spell_cost` for `mana_cost`): the same ending
 * first, then the same start, the nearest line first. Null when no box shares a word.
 */
function similarBox(name: string, defined: Definition[], skip: string[]): Definition | null {
  const parts = name.toLowerCase().split("_").filter((part) => part.length >= 3);
  if (parts.length === 0) return null;
  const last = parts[parts.length - 1];
  const first = parts[0];
  const boxes = defined.filter((entry) => !skip.includes(entry.name) && !entry.name.startsWith("_"));
  const words = (entry: Definition) => entry.name.toLowerCase().split("_");
  const ending = boxes.find((entry) => words(entry).length > 1 && words(entry)[words(entry).length - 1] === last);
  if (ending) return ending;
  return boxes.find((entry) => words(entry).includes(first) || words(entry).includes(last)) ?? null;
}

/**
 * A name called on this line (`max_fuel_for(4)`) that the code only ever makes with `=` above it (a box, not a
 * recipe): the last line that makes it, and that line's right side. Null when no such name is called.
 */
function calledBox(code: string, text: string, line: number | null): { name: string; line: number; value: string } | null {
  const rows = (code ?? "").split("\n");
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  for (const call of maskStrings(codePart(text)).matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\(/g)) {
    const name = call[1];
    if (recipes.has(name) || KEYWORDS.has(name)) continue;
    const box = new RegExp(`^\\s*${escapeRegExp(name)}\\s*=(?!=)\\s*(.+)$`);
    let found: { name: string; line: number; value: string } | null = null;
    rows.forEach((row, index) => {
      const made = codePart(row).match(box);
      if (made && (line === null || index + 1 < line)) found = { name, line: index + 1, value: made[1].trim() };
    });
    if (found) return found;
  }
  return null;
}

function inputNames(code: string): string[] {
  return [...(code ?? "").matchAll(/^\s*([A-Za-z_]\w*)\s*=\s*input\s*\(/gm)].map((match) => match[1]);
}

/**
 * `def hero(): "Lucky"` (the student followed Python's "expected '('"), then `print(hero + " is ready.")`: a
 * TypeError about a 'function'. The slip is the def line, so it gets the def-for-variable advice.
 */
function explainRecipeUsedAsBox(message: string, code: string, text: string, raw: string): CourseExplanation | null {
  if (!/'function'/.test(message)) return null;
  const used = namesOnLine(text);
  const lines = (code ?? "").split("\n");
  for (let at = 0; at < lines.length; at += 1) {
    const header = codePart(lines[at] ?? "").trim().match(/^def\s+([A-Za-z_]\w*)\s*\(\s*\)\s*:\s*(.*)$/);
    if (!header || !used.includes(header[1])) continue;
    const value = header[2].trim() || lines.slice(at + 1).map((row) => codePart(row).trim()).find(Boolean) || "";
    const shown = value.replace(/^return\s+/, "");
    const fix = shown && !/^(pass|print\b)/.test(shown) ? `${header[1]} = ${shown}` : `${header[1]} = "your value"`;
    return explain(
      "def-for-variable",
      "def makes recipes",
      `Line ${at + 1} uses \`def\`, so \`${header[1]}\` is a recipe, not a box, and line ${errorLine(raw) ?? "?"} can't use it as a value. \`def\` makes recipes, not boxes. A box needs only a name, \`=\` and a value, with no \`def\` and no brackets: \`${fix}\``,
      raw,
    );
  }
  return null;
}

/* ---------------------------------------------------------------------------------------------- */
/* Lists (Unit 4): brackets, + and the list tools                                                  */
/* ---------------------------------------------------------------------------------------------- */

/** The tools a student calls (Python's own and the list and text methods): `name[...]` after one is a call slip. */
const CALLED_TOOLS = new Set([
  ...COMMON_BUILTINS.filter((name) => !["True", "False", "None", "random", "math"].includes(name)),
  "append", "count", "remove", "insert", "pop", "sort", "index", "extend", "copy", "clear", "reverse",
  "lower", "upper", "capitalize", "title", "strip", "randint",
]);

/**
 * Where the bracket that opens at `open` in `mask` closes (strings already masked), or -1. `open` is the index of
 * a `(` or `[`.
 */
function matchingBracket(mask: string, open: number): number {
  const opener = mask[open];
  const closer = CLOSER[opener];
  let depth = 0;
  for (let index = open; index < mask.length; index += 1) {
    if (mask[index] === opener) depth += 1;
    else if (mask[index] === closer) {
      depth -= 1;
      if (depth === 0) return index;
    }
  }
  return -1;
}

/**
 * The names the code makes as lists (`chalk_wall = [48, ...]`, also over several lines, `d8 = list(range(1, 9))`,
 * `pairs = sorted(...)`, `both = a + [b]`), with a flag for a list of lists (its first item is itself a `[ ]`).
 */
function listsMade(code: string): Map<string, { nested: boolean }> {
  const found = new Map<string, { nested: boolean }>();
  const rows = (code ?? "").split("\n");
  rows.forEach((row, index) => {
    const made = codePart(row).match(/^\s*([A-Za-z_]\w*)\s*=(?!=)\s*(\[|list\s*\(|sorted\s*\(|[A-Za-z_]\w*\s*\+\s*\[|[A-Za-z_]\w*\s*\[[^\]]*:)/);
    if (!made) return;
    // A list of lists: the first thing after its `[` (on this line or the next ones) is another `[`.
    const after = [codePart(row).slice((made.index ?? 0) + made[0].length), ...rows.slice(index + 1, index + 3)].join(" ");
    found.set(made[1], { nested: made[2] === "[" && /^\s*\[/.test(after) });
  });
  return found;
}

/**
 * `name(...)` in `text` with its round brackets made square: `chalk_wall(0)` -> `chalk_wall[0]`. Two values
 * (`chalk_wall(0, 2)`) become a run of items, `[0:2]`, or row then item, `[2][0]`, for a list of lists (`nested`).
 */
function squareBracketed(text: string, name: string, nested = false): { call: string; fixed: string; line: string } | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const at = mask.search(new RegExp(`(?<![\\w.])${escapeRegExp(name)}\\s*\\(`));
  if (at < 0) return null;
  const open = mask.indexOf("(", at);
  const close = matchingBracket(mask, open);
  if (close < 0) return null;
  const inside = body.slice(open + 1, close);
  const parts = splitTopLevel(inside);
  const two = parts && parts.parts.length === 2 && parts.marks[0] === "," ? parts.parts : null;
  const read = two ? (nested ? `${name}[${two[0]}][${two[1]}]` : `${name}[${two[0]}:${two[1]}]`) : `${name}[${inside}]`;
  return {
    call: body.slice(at, close + 1),
    fixed: read,
    line: `${body.slice(0, at)}${read}${body.slice(close + 1)}`.trim(),
  };
}

/**
 * `chalk_wall(2) = 47` ("cannot assign to function call"): round brackets after a list's name, on the left of `=`.
 * Only for a name the code makes as a list, never a recipe or one of Python's tools (Unit 3's recipe-like-math row
 * keeps `max_fuel_for(cells) = ...`). Before the `==` row, whose "use two equals signs" is wrong advice here.
 */
function explainListAssignedWithCall(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/cannot assign to function call/i.test(message)) return null;
  const body = codePart(text);
  const at = singleEquals(maskStrings(body))[0];
  const left = at === undefined ? "" : body.slice(0, at).trim();
  const name = left.match(/^([A-Za-z_]\w*)\s*\(/)?.[1];
  const list = name ? listsMade(code).get(name) : undefined;
  if (!name || !list) return null;
  const swapped = squareBracketed(text, name, list.nested);
  if (!swapped || swapped.call.trim() !== left) return null;
  return explain(
    "list-needs-square-brackets",
    "Square brackets for a list",
    `${lineWord(line)} puts ( ) after \`${name}\`. To change one item, use square brackets: \`${swapped.line}\``,
    raw,
  );
}

/**
 * "'list' object is not callable" (`chalk_wall(0)`, `wall(-1)` inside a recipe): the list read with round brackets.
 * The name is the one called on the line that is not a recipe or one of Python's tools.
 */
function explainListCalled(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  const lists = listsMade(code);
  const called = [...maskStrings(codePart(text)).matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\(/g)]
    .map((match) => match[1])
    .filter((name) => !recipes.has(name) && !CALLED_TOOLS.has(name) && !KEYWORDS.has(name));
  const name = called.find((entry) => lists.has(entry)) ?? called[0];
  const swapped = name ? squareBracketed(text, name, lists.get(name)?.nested ?? false) : null;
  if (!name || !swapped) return null;
  return explain(
    "list-needs-square-brackets",
    "Square brackets for a list",
    `${lineWord(line)} puts ( ) after \`${name}\`, so Python tries to call it like a recipe (function). \`${name}\` is a list. Read a list with square brackets: \`${swapped.fixed}\``,
    raw,
  );
}

/**
 * "... is not subscriptable" on something that is called, never read (`chalk_wall.append[33]`, `sorted[...]`,
 * `max[chalk_wall]`, `range[1, 9]`, a recipe): square brackets where the call needs round ones. `None` (from
 * `x = wall.sort()`) keeps the older words.
 */
function explainToolWithSquareBrackets(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/^('(builtin_function_or_method|function|method)' object|type '\w+') is not subscriptable/.test(message)) return null;
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  const body = codePart(text);
  const mask = maskStrings(body);
  for (const found of mask.matchAll(/(?<![\w.])((?:[A-Za-z_]\w*\.)*([A-Za-z_]\w*))\s*\[/g)) {
    const tool = found[2];
    if (!CALLED_TOOLS.has(tool) && !recipes.has(tool)) continue;
    const open = (found.index ?? 0) + found[0].length - 1;
    const close = matchingBracket(mask, open);
    if (close < 0) continue;
    const fixed = `${found[1]}(${body.slice(open + 1, close)})`;
    return explain(
      "call-needs-round-brackets",
      "Round brackets for a call",
      `${lineWord(line)} puts square brackets after \`${tool}\`, but \`${tool}\` is a tool you call, like \`print\`. Call it with round brackets: \`${fixed}\``,
      raw,
    );
  }
  return null;
}

/**
 * "list indices must be integers or slices, not tuple" (`roster[2, 0]`, `chalk_wall[0, 2]`): a comma inside `[ ]`
 * asks for two positions at once. The half that fits comes first: row then item for a list of lists, a colon for a
 * run of items otherwise.
 */
function explainCommaInBrackets(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/indices must be integers or slices, not tuple/.test(message)) return null;
  const body = codePart(text);
  const mask = maskStrings(body);
  for (const found of mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\[/g)) {
    const open = (found.index ?? 0) + found[0].length - 1;
    const close = matchingBracket(mask, open);
    const parts = close < 0 ? null : splitTopLevel(body.slice(open + 1, close));
    if (!parts || parts.parts.length !== 2 || parts.marks[0] !== ",") continue;
    const [first, second] = parts.parts;
    const name = found[1];
    const rows = `\`${name}[${first}][${second}]\``;
    const run = `\`${name}[${first}:${second}]\``;
    const nested = listsMade(code).get(name)?.nested ?? false;
    const start = "Inside [ ], a comma asks for two positions at once.";
    return explain(
      "comma-in-brackets",
      "One position per [ ]",
      nested
        ? `${start} Row then item takes two pairs of brackets: ${rows}. A run of items takes a colon: \`[0:2]\`.`
        : `${start} A run of items takes a colon: ${run}. In a list of lists, row then item takes two pairs of brackets, like \`[2][0]\`.`,
      raw,
    );
  }
  return null;
}

/**
 * 'can only concatenate list (not "int") to list' (`chalk_wall = chalk_wall + 33`): `+` joins two lists. A row of a
 * list of lists on the left (`log[0] = log[0] + 2`) is a whole pair, not its score: the inner position is missing,
 * and `.append()` would be the wrong advice.
 */
function explainListPlusItem(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const kind = message.match(/can only concatenate list \(not "(\w+)"\) to list/)?.[1];
  if (!kind) return null;
  const body = codePart(text).trim();
  const row = explainRowPlusItem(code, body, line, raw);
  if (row) return row;
  const same = body.match(/^([A-Za-z_]\w*)\s*=(?!=)\s*\1\s*\+\s*(.+)$/) ?? body.match(/^([A-Za-z_]\w*)\s*\+\s*(.+)$/);
  const item = same?.[2]?.trim();
  const fix = same && item && !/^\[/.test(item) ? `: \`${same[1]}.append(${item})\`` : "";
  return explain(
    "list-plus-item",
    "+ joins two lists",
    `${lineWord(line)} joins a list and one ${kind === "str" ? "piece of text" : "number"} with \`+\`. \`+\` joins two lists. To add one item, use \`.append()\`${fix}`,
    raw,
  );
}

/**
 * "list.append() takes exactly one argument (2 given)" (`log.append("roll and rise", 6)`): one item at a time, so a
 * pair goes in its own square brackets. "(0 given)" (`chalk_wall.count()`): the tool needs its value.
 */
function explainListToolValues(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const tool = message.match(/^list\.(\w+)\(\) takes exactly one argument \((\d+) given\)/);
  if (!tool) return null;
  const [, name, given] = tool;
  if (given === "0") {
    return explain(
      "wrong-number-of-values",
      "One value inside ( )",
      `\`.${name}()\`${onLine(line)} needs one value inside its round brackets: the value to ${name === "count" ? "count" : "use"}.`,
      raw,
    );
  }
  const body = codePart(text);
  const mask = maskStrings(body);
  const at = mask.search(new RegExp(`\\.\\s*${name}\\s*\\(`));
  const open = at < 0 ? -1 : mask.indexOf("(", at);
  const close = open < 0 ? -1 : matchingBracket(mask, open);
  // `log.append(["roll and rise"], 6)`: a one-item list beside the rest is rebuilt as one pair, never `[["roll and rise"], 6]`.
  const values = close < 0 ? null : splitTopLevel(body.slice(open + 1, close));
  const items =
    values && values.marks.every((mark) => mark === ",")
      ? values.parts.map((part) => {
          const inner = /^\[[\s\S]*\]$/.test(part) && matchingBracket(maskStrings(part), 0) === part.length - 1 ? splitTopLevel(part.slice(1, -1)) : null;
          return inner && inner.parts.length === 1 && inner.parts[0] ? inner.parts[0] : part;
        })
      : null;
  const inside = items ? items.join(", ") : close < 0 ? "" : body.slice(open + 1, close).trim();
  const fix = close < 0 ? "" : `: \`${body.slice(0, open + 1).trim()}[${inside}]${body.slice(close).trim()}\``;
  return explain(
    "wrong-number-of-values",
    "One item at a time",
    `\`.${name}()\` adds one item, and line ${line ?? "?"} hands it ${given}. To add them as one item, put them in their own square brackets${fix}`,
    raw,
  );
}

/** "not enough / too many values to unpack (expected 3, got 2)" (`across, down, up = cabin`): one name per item. */
function explainUnpackCount(message: string, line: number | null, raw: string): CourseExplanation | null {
  const counts = message.match(/(?:not enough|too many) values to unpack \(expected (\d+), got (\d+)\)/);
  if (!counts) return null;
  return explain(
    "wrong-number-of-values",
    "One name per item",
    `${lineWord(line)} has ${counts[1]} names on the left of \`=\`, but the right side holds ${counts[2]} items. Use one name per item: ${counts[2]} names.`,
    raw,
  );
}

/** "argument of type 'int' is not iterable" (`has_32 = chalk_wall in 32`): the value goes first, then `in`, then the list. */
function explainInBackwards(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/argument of type '(int|float|bool)' is not iterable/.test(message)) return null;
  const swapped = codePart(text).match(/^(\s*(?:[A-Za-z_]\w*\s*=(?!=)\s*)?)([A-Za-z_]\w*)\s+in\s+(-?\d+(?:\.\d+)?)\s*$/);
  const fix = swapped ? `: \`${`${swapped[1]}${swapped[3]} in ${swapped[2]}`.trim()}\`` : ".";
  return explain(
    "wrong-kind-of-value",
    "The value goes first",
    `\`in\` asks whether a value is in a list, so the value goes first and the list after it${onLine(line)}${fix}`,
    raw,
  );
}

/** What each tool that goes in front of a list hands back (`sorted(chalk_wall)`, `max(chalk_wall)`). */
const IN_FRONT: Record<string, string> = {
  sorted: "It hands back a sorted copy.",
  max: "It hands back the biggest item.",
  min: "It hands back the smallest item.",
  sum: "It hands back every item added up.",
  len: "It hands back how many items there are.",
};

/**
 * "'list' object has no attribute 'sorted'. Did you mean: 'sort'?" (`chalk_wall.sorted()`), and the same for `max`,
 * `min`, `sum` and `len`: these tools go in front of the list, not after a dot. Python's "Did you mean 'sort'" would
 * sort the wall itself, so it is not the advice.
 */
function explainToolAfterDot(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const tool = message.match(/^'list' object has no attribute '(sorted|max|min|sum|len)'/)?.[1];
  if (!tool) return null;
  const owner = maskStrings(codePart(text)).match(new RegExp(`([A-Za-z_]\\w*(?:\\[[^\\]]*\\])*)\\s*\\.\\s*${tool}\\s*\\(\\s*\\)`))?.[1];
  const fix = owner ? `${tool}(${owner})` : `${tool}(chalk_wall)`;
  return explain(
    "tool-after-dot",
    `${tool} goes in front`,
    `${lineWord(line)} writes \`${tool}\` after a dot. \`${tool}\` goes in front: \`${fix}\`. ${IN_FRONT[tool]}`,
    raw,
  );
}

/** "list.remove(x): x not in list" (`chalk_wall.remove(3)` for a position, or `.remove("99")` with quotes). */
function explainRemoveMissing(text: string, line: number | null, raw: string): CourseExplanation {
  const body = codePart(text);
  const mask = maskStrings(body);
  const at = mask.search(/\.\s*remove\s*\(/);
  const open = at < 0 ? -1 : mask.indexOf("(", at);
  const close = open < 0 ? -1 : matchingBracket(mask, open);
  const value = close < 0 ? "" : body.slice(open + 1, close).trim();
  const quoted = value.match(/^(["'])(-?\d+)\1$/);
  const there = value ? `There is no ${value} on the list` : "That value is not on the list";
  return explain(
    "not-on-the-list",
    "Not on the list",
    quoted
      ? `\`.remove()\`${onLine(line)} looks for that exact value. ${there}: in quotes it is text, and the list holds numbers. Ask first with \`in\`.`
      : `\`.remove()\`${onLine(line)} looks for a value, not a position. ${there}. Ask first with \`in\`.`,
    raw,
  );
}

/**
 * Bare words side by side inside `[ ]` ("Perhaps you forgot a comma?"): `log = [[storm kick, 7]]`, or one item of
 * a list over several lines (`    brass lens,`). The same row as the words inside `( )`, for a list.
 */
function explainUnquotedInList(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const pieces: string[] = [];
  // Each [ ] on the line, and the line itself when it sits inside a list that opened above it.
  for (let index = 0; index < mask.length; index += 1) {
    if (mask[index] !== "[") continue;
    const close = matchingBracket(mask, index);
    if (close > index) pieces.push(body.slice(index + 1, close));
  }
  if (openBefore(code, line).at(-1) === "[") pieces.push(body.replace(/,\s*$/, ""));
  const names = namesBefore(code, line);
  for (const piece of pieces) {
    for (const part of splitTopLevel(piece)?.parts ?? []) {
      const words = part.replace(/^\[|\]$/g, "").trim().split(/\s+/).filter(Boolean);
      if (words.length < 2 || !words.every((word) => /^[A-Za-z][A-Za-z'-]*$/.test(word))) continue;
      if (words.some((word) => KEYWORDS.has(word) || names.includes(word))) continue;
      const phrase = words.join(" ");
      return explain("unquoted-words", "Missing quotes?", `If ${phrase} is text, put quotes around it: "${phrase}". Text needs quotes.`, raw);
    }
  }
  return null;
}

/** `chalk_wall = [48 48, 47]` ("Perhaps you forgot a comma?"): two numbers side by side inside `[ ]`. */
function explainListMissingComma(text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const open = mask.indexOf("[");
  const close = open < 0 ? -1 : matchingBracket(mask, open);
  if (close < 0 || !/-?\d\s+-?\d/.test(mask.slice(open, close))) return null;
  const fixed = `${body.slice(0, open)}${body.slice(open, close + 1).replace(/(\d)\s+(?=-?\d)/g, "$1, ")}${body.slice(close + 1)}`.trim();
  return explain(
    "missing-comma-in-list",
    "Missing comma",
    `Inside a list, a comma goes between each two items. ${lineWord(line)} has numbers side by side with no comma between them: \`${fixed}\``,
    raw,
  );
}

/** The code's lines with comments cut off and strings masked, joined again, keeping every index (for multi-line lists). */
function maskedCode(code: string): { text: string; mask: string } {
  const rows = (code ?? "").split("\n").map((row) => codePart(row));
  return { text: rows.join("\n"), mask: rows.map((row) => maskStrings(row).padEnd(row.length)).join("\n") };
}

/**
 * The position of the first number in the first row of the list of lists `name` (`log = [["cane parry", 7], ...]`
 * gives 1), or null when the code does not write it out.
 */
function firstRowNumberAt(code: string, name: string): number | null {
  const { text, mask } = maskedCode(code);
  const made = new RegExp(`(^|\\n)[ \\t]*${escapeRegExp(name)}\\s*=(?!=)\\s*\\[`).exec(mask);
  if (!made) return null;
  const outer = made.index + made[0].length - 1;
  const first = mask.slice(outer + 1).search(/\S/);
  const open = first < 0 ? -1 : outer + 1 + first;
  if (open < 0 || mask[open] !== "[") return null;
  const close = matchingBracket(mask, open);
  const parts = close < 0 ? null : splitTopLevel(text.slice(open + 1, close));
  if (!parts || parts.marks.some((mark) => mark !== ",")) return null;
  const at = parts.parts.findIndex((part) => /^-?\d+(\.\d+)?$/.test(part));
  return at < 0 ? null : at;
}

/**
 * `log[0] = log[0] + 2` in a list of lists ('can only concatenate list (not "int") to list'): `log[0]` is a whole row
 * (a pair), so the number needs the row's inner position too: `log[0][1] = log[0][1] + 2`.
 */
function explainRowPlusItem(code: string, body: string, line: number | null, raw: string): CourseExplanation | null {
  const mask = maskStrings(body);
  const left = mask.match(/(?<![\w.\]])([A-Za-z_]\w*)\s*\[([^[\]]+)\]\s*\+/);
  if (!left || !listsMade(code).get(left[1])?.nested) return null;
  const name = left[1];
  const index = body.slice((left.index ?? 0) + left[0].indexOf("[") + 1, (left.index ?? 0) + left[0].lastIndexOf("]")).trim();
  const read = `${name}[${index}]`;
  const inner = firstRowNumberAt(code, name);
  const pattern = new RegExp(`(?<![\\w.])${escapeRegExp(name)}\\s*\\[\\s*${escapeRegExp(index)}\\s*\\](?!\\s*\\[)`, "g");
  const fixed = inner === null ? null : body.replace(pattern, `${read}[${inner}]`);
  return explain(
    "row-not-item",
    "A whole row",
    `${lineWord(line)} adds to \`${read}\`, but \`${read}\` is a whole row of \`${name}\`: a list, not a number. ` +
      (fixed
        ? `Add the inner position of the number in it too: \`${fixed}\``
        : "Add the inner position of the number in it too: row first, then the item in that row."),
    raw,
  );
}

/** The list tools that change the list itself and hand back nothing (`None`). */
const IN_PLACE: Record<string, string> = {
  sort: "sorts the list itself",
  append: "adds to the list itself",
  insert: "adds to the list itself",
  extend: "adds to the list itself",
  remove: "takes from the list itself",
  reverse: "turns the list itself around",
  clear: "empties the list itself",
};

/**
 * "'NoneType' object is not subscriptable" (`shortest = chalk_wall.sort()[0]`, or `x = wall.sort()` then `x[0]`):
 * a position read from `None`. In the unit's words, `None` is "nothing came back": `.sort()` sorts the list itself
 * and hands back nothing, and `sorted(wall)` hands back a sorted copy.
 */
function explainNoneRead(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/^'NoneType' object is not subscriptable/.test(message)) return null;
  const tools = Object.keys(IN_PLACE).join("|");
  const body = codePart(text);
  const mask = maskStrings(body);
  let found: { list: string; tool: string; holder?: string; at?: number } | null = null;
  const direct = new RegExp(`(?<![\\w.])([A-Za-z_]\\w*(?:\\[[^\\]]*\\])*)\\s*\\.\\s*(${tools})\\s*\\(`).exec(mask);
  if (direct) {
    const close = matchingBracket(mask, direct.index + direct[0].length - 1);
    if (close > 0 && /^\s*\[/.test(mask.slice(close + 1))) found = { list: body.slice(direct.index, direct.index + direct[1].length), tool: direct[2] };
  }
  if (!found && line) {
    // A box read with [ ] that holds None: its nearest `name = x.sort()` above this line decides.
    const rows = (code ?? "").split("\n").slice(0, line - 1);
    for (const read of mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\[/g)) {
      const holder = read[1];
      for (let at = rows.length - 1; at >= 0; at -= 1) {
        const row = codePart(rows[at] ?? "");
        const made = new RegExp(`^\\s*${escapeRegExp(holder)}\\s*=(?!=)\\s*([A-Za-z_]\\w*(?:\\[[^\\]]*\\])*)\\s*\\.\\s*(${tools})\\s*\\(`).exec(maskStrings(row));
        if (made) {
          const from = made[0].indexOf(made[1], made[0].indexOf("=") + 1);
          found = { list: row.slice(from, from + made[1].length).trim(), tool: made[2], holder, at: at + 1 };
        }
        if (made || new RegExp(`^\\s*${escapeRegExp(holder)}\\s*=(?!=)`).test(row)) break;
      }
      if (found) break;
    }
  }
  const nothing = "`None`: nothing came back";
  if (!found) {
    return explain(
      "read-from-none",
      "Nothing came back",
      `${lineWord(line)} reads a position from ${nothing}, so there is nothing to read. A tool that changes a list, like \`.sort()\`, hands back nothing, and so does a recipe with no \`return\`.`,
      raw,
    );
  }
  const what = `\`.${found.tool}()\`${found.at ? ` on line ${found.at}` : ""} ${IN_PLACE[found.tool]} and hands back nothing.`;
  const instead = found.tool === "sort" ? ` \`sorted(${found.list})\` hands back a sorted copy.` : ` Read the list itself, \`${found.list}\`, after it has changed.`;
  return explain(
    "read-from-none",
    "Nothing came back",
    found.holder
      ? `${lineWord(line)} reads a position from \`${found.holder}\`, and \`${found.holder}\` holds ${nothing}. ${what}${instead}`
      : `${lineWord(line)} reads a position from ${nothing}. ${what}${instead}`,
    raw,
  );
}

/**
 * "list indices must be integers or slices, not tuple" from two lists side by side with no comma between them:
 * `[["cane parry", 7] ["shield wall", 5]]` on one line, or a row of a list over several lines with no comma at its
 * end. Python reads the second list as a position in the first (never "a comma inside [ ]").
 */
function explainRowsWithoutComma(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/indices must be integers or slices, not tuple/.test(message)) return null;
  const body = codePart(text);
  const mask = maskStrings(body);
  const side = /(^|[=,([]\s*)(\[[^[\]]*\])\s*\[/.exec(mask);
  if (side) {
    const at = side.index + side[1].length;
    const row = body.slice(at, at + side[2].length).trim();
    return explain(
      "missing-comma-in-list",
      "Missing comma",
      `${lineWord(line)} has two lists side by side with no comma between them, so Python reads the second one as a position in the first. Put a comma after each one: \`${row},\``,
      raw,
    );
  }
  const row = body.trim();
  if (!line || !/^\[[^[\]]*\]$/.test(maskStrings(row)) || openBefore(code, line).at(-1) !== "[") return null;
  const next = (code ?? "").split("\n").slice(line).map((entry) => codePart(entry).trim()).find(Boolean) ?? "";
  if (!next.startsWith("[")) return null;
  return explain(
    "missing-comma-in-list",
    "Missing comma",
    `${lineWord(line)} ends a list with no comma, and the next line starts another, so Python reads the second one as a position in the first. Put a comma after each one: \`${row},\``,
    raw,
  );
}

/** The ingredients of the recipe whose body holds `line` (1-based), or []. */
function recipeParamsAt(code: string, line: number | null): string[] {
  if (!line) return [];
  const block = recipeBlocks(code).find((entry) => line > entry.start && line <= entry.end);
  if (!block) return [];
  const header = codePart((code ?? "").split("\n")[block.start - 1] ?? "").match(/^\s*def\s+[A-Za-z_]\w*\s*\(([^)]*)\)/);
  return (header?.[1] ?? "").split(",").map((part) => part.split("=")[0].trim()).filter(Boolean);
}

/**
 * How many items `name` holds, when the code makes it once with its items written out on one line
 * (`chalk_wall = [48, 48, 47]`, `cabin = (12, 5)`) and nothing could change how many (`.append()`, `.pop()`, `+=`, a
 * recipe that changes a list, ...). Null when that can't be read for sure.
 */
function readableLength(code: string, name: string): number | null {
  const { mask } = maskedCode(code);
  const rows = (code ?? "").split("\n").map((row) => codePart(row));
  const who = escapeRegExp(name);
  if (new RegExp(`\\.\\s*(append|insert|pop|remove|extend|clear)\\s*\\(`).test(mask) && /^\s*def\b/m.test(mask)) return null;
  if (new RegExp(`(?<![\\w.])${who}\\s*(\\.\\s*(append|insert|pop|remove|extend|clear)\\s*\\(|[-+*]=)|\\bdel\\s+${who}\\b|\\bfor\\s+${who}\\b|(?<![\\w.])${who}\\s*,[^\\n=]*=(?!=)|,\\s*${who}\\s*=(?!=)`).test(mask)) {
    return null;
  }
  const made = rows.map((row) => maskStrings(row)).filter((row) => new RegExp(`^\\s*${who}\\s*=(?!=)`).test(row));
  if (made.length !== 1) return null;
  const row = rows.find((entry) => new RegExp(`^\\s*${who}\\s*=(?!=)`).test(maskStrings(entry))) ?? "";
  const value = row.slice(row.indexOf("=") + 1).trim();
  const valueMask = maskStrings(value);
  if (!/^[[(]/.test(valueMask) || matchingBracket(valueMask, 0) !== valueMask.length - 1 || /[[(]/.test(valueMask.slice(1, -1))) return null;
  const inside = value.slice(1, -1).trim();
  if (!inside) return valueMask.startsWith("(") ? null : 0;
  const parts = splitTopLevel(inside);
  if (!parts || parts.marks.some((mark) => mark !== ",")) return null;
  const items = parts.parts.filter((part, index) => part || index < parts.parts.length - 1);
  if (valueMask.startsWith("(") && items.length < 2) return null;
  return items.every(Boolean) ? items.length : null;
}

/**
 * Unit 4: "list index out of range" in the unit's words. The class's slip, `chalk_wall[len(chalk_wall)]`, gets its own
 * row: `len()` counts the items, so it is one past the last position. Otherwise the list's own count when it can be
 * read ("`chalk_wall` holds 7 items, so its positions are 0 to 6"), and never Unit 1's "3 items" example.
 */
function explainOutOfRange(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (/string/.test(message)) return null;
  const what = /tuple/.test(message) ? "tuple" : "list";
  const mask = maskStrings(codePart(text));
  const counted = mask.match(/(?<![\w.])([A-Za-z_]\w*)\s*(?:\[|\.\s*pop\s*\()\s*len\s*\(\s*\1\s*\)\s*[\])]/);
  if (counted) {
    const name = counted[1];
    return explain(
      "nothing-at-position",
      "One past the end",
      `${lineWord(line)} uses \`len(${name})\` as a position. \`len(${name})\` counts the items, so it is one past the last position. Use \`len(${name}) - 1\`, or \`[-1]\`.`,
      raw,
    );
  }
  const reads = [...mask.matchAll(/(?<![\w.\]])([A-Za-z_]\w*)\s*\[/g)].map((match) => match[1]).filter((name) => !KEYWORDS.has(name));
  const name = reads[0];
  const last = "Positions start at 0, so the last position is one less than the number of items. `[-1]` is always the last one.";
  if (name && recipeParamsAt(code, line).includes(name)) {
    return explain(
      "nothing-at-position",
      "Nothing at that position",
      `${lineWord(line)} asks for a position \`${name}\` doesn't have. Inside the recipe, \`${name}\` is whatever ${what} the call hands over, and it may be shorter. ${last}`,
      raw,
    );
  }
  if (name && new RegExp(`(?<![\\w.])${escapeRegExp(name)}\\s*\\[[^\\]]*\\]\\s*\\[`).test(mask)) {
    return explain(
      "nothing-at-position",
      "Nothing at that position",
      `${lineWord(line)} asks for a position \`${name}\` doesn't have. In a list of lists, check both numbers: the row first, then the item in that row. ${last}`,
      raw,
    );
  }
  const count = name && reads.filter((entry) => entry === name).length === 1 ? readableLength(code, name) : null;
  if (name && count !== null) {
    return explain(
      "nothing-at-position",
      "Nothing at that position",
      count === 0
        ? `${lineWord(line)} asks for a position in \`${name}\`, but \`${name}\` is empty, so it has no positions yet.`
        : `${lineWord(line)} asks for a position \`${name}\` doesn't have. \`${name}\` holds ${count} item${count === 1 ? "" : "s"}, so its positions are 0 to ${count - 1}. From the end, \`[-1]\` is the last one.`,
      raw,
    );
  }
  return explain("nothing-at-position", "Nothing at that position", `${lineWord(line)} asks for a position the ${what} doesn't have. ${last}`, raw);
}

/**
 * Unit 4: numbers side by side with nothing between them, outside any brackets (`hours = 48 48 47 46`: the wall's
 * row copied as it looks). They need commas, inside square brackets, or one box each (never "a missing quote").
 */
function explainNumbersSideBySide(text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text).trim();
  const mask = maskStrings(body);
  let depth = 0;
  let outside = "";
  for (const char of mask) {
    if (char in CLOSER) depth += 1;
    else if (char in OPENER) depth = Math.max(0, depth - 1);
    outside += depth === 0 ? char : " ";
  }
  if (!/(^|[^\w.])-?\d+(\.\d+)?\s+-?\d/.test(outside)) return null;
  const made = body.match(/^([A-Za-z_]\w*)\s*=(?!=)\s*(-?\d+(?:\.\d+)?(?:[ \t]+-?\d+(?:\.\d+)?)+)$/);
  const fix = made ? `\`${made[1]} = [${made[2].trim().split(/\s+/).join(", ")}]\`` : "`[48, 48, 47]`";
  return explain(
    "missing-comma",
    "Numbers side by side",
    `${lineWord(line)} has numbers side by side with nothing between them. Numbers side by side need commas, inside square brackets: ${fix}. Or give each number a box of its own.`,
    raw,
  );
}

/** Unit 4: `newest = chalk_wall.pop[]`, `sorted[]`: empty square brackets after a tool that is called (a SyntaxError). */
function explainEmptySquareCall(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  const mask = maskStrings(codePart(text));
  for (const found of mask.matchAll(/(?<![\w.])((?:[A-Za-z_]\w*\.)*([A-Za-z_]\w*))\s*\[\s*\]/g)) {
    const tool = found[2];
    if (!CALLED_TOOLS.has(tool) && !recipes.has(tool)) continue;
    if (!found[1].includes(".") && !recipes.has(tool) && !COMMON_BUILTINS.includes(tool)) continue;
    return explain(
      "call-needs-round-brackets",
      "Round brackets for a call",
      `${lineWord(line)} puts square brackets after \`${tool}\`, but \`${tool}\` is a tool you call, like \`print\`. Call it with round brackets: \`${found[1]}()\``,
      raw,
    );
  }
  return null;
}

function explainType(
  message: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation {
  const fromInput = inputNames(code).find((name) => new RegExp(`\\b${escapeRegExp(name)}\\b`).test(text));
  const joinText = /can only concatenate str \(not "(int|float)"\) to str/.test(message);
  const addToNumber = /unsupported operand type\(s\) for \+: '(int|float)' and 'str'/.test(message);
  if ((joinText || addToNumber) && fromInput) {
    return explain(
      "input-is-text",
      "input() gives text",
      `${fromInput} came from input(), and input() always gives back text. To do math with it, turn it into a number first: int(${fromInput})`,
      raw,
    );
  }
  if (joinText) {
    const number = text.match(/\+\s*([A-Za-z_]\w*)\b(?!\s*\()/)?.[1] ?? text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    const example = number ? `str(${number})` : "str(score)";
    return explain(
      "text-plus-number",
      "Text + number",
      `${lineWord(line)} joins text and a number with +. Turn the number into text first with str(), like ${example}.`,
      raw,
    );
  }
  if (addToNumber) {
    const number = text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    const example = number && number !== "print" ? `str(${number})` : "str()";
    return explain(
      "number-plus-text",
      "Number + text",
      `${lineWord(line)} adds a number and text. To join them as text, turn the number into text first, like ${example}.`,
      raw,
    );
  }
  // `def hero(): "Lucky"` then `hero + " is ready."`: Python's own hint led to a recipe, not a box.
  const recipe = explainRecipeUsedAsBox(message, code, text, raw);
  if (recipe) return recipe;
  // Unit 4: one item joined to a list with `+`, square brackets after a tool, a comma between two positions.
  if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
    const list =
      explainListPlusItem(message, code, text, line, raw) ??
      explainNoneRead(message, code, text, line, raw) ??
      explainRowsWithoutComma(message, code, text, line, raw) ??
      explainToolWithSquareBrackets(message, code, text, line, raw) ??
      explainCommaInBrackets(message, code, text, line, raw) ??
      explainListToolValues(message, text, line, raw) ??
      explainInBackwards(message, text, line, raw);
    if (list) return list;
  }
  const dash = /unsupported operand type\(s\) for -/.test(message) ? dashFix(text) : null;
  if (dash && printOnlyTask(context)) return dashInPrintTask(text, line, raw, "dash-for-equals");
  if (dash) {
    return explain(
      "dash-for-equals",
      "Dash or equals?",
      `${lineWord(line)} uses a dash - where Python needs an equals sign =. To make a variable, write: ${dash}`,
      raw,
    );
  }
  const bar = /unsupported operand type\(s\) for -: '(str|int)' and '(int|str)'/.test(message) ? barBrackets(text) : null;
  if (bar) {
    return explain(
      "bar-needs-brackets",
      "Brackets for the gap",
      `Python does * before -${onLine(line)}. So it stamps the text first, then tries to take a number away from text. Put brackets around the subtraction so it happens first: ${bar}`,
      raw,
    );
  }
  const quoted = /unsupported operand type\(s\) for [-*/%+]+: '\w+' and '\w+'/.test(message)
    ? codePart(text).match(/[-*/%+]\s*(["'])(\d+(?:\.\d+)?)\1|(["'])(\d+(?:\.\d+)?)\3\s*[-*/%+]/)
    : null;
  if (quoted) {
    const digits = quoted[2] ?? quoted[4];
    const quote = quoted[1] ?? quoted[3];
    return explain(
      "number-in-quotes",
      "Math with text",
      `${quote}${digits}${quote}${onLine(line)} has quotes, so Python treats it as text, not a number. Numbers have no quotes: write ${digits}.`,
      raw,
    );
  }
  if (
    /unsupported operand type\(s\) for [-*/%]+: 'str' and '(int|float)'|unsupported operand type\(s\) for [-/%]+: '\w+' and 'str'|can't multiply sequence by non-int/.test(
      message,
    )
  ) {
    return explain(
      "math-with-text",
      "Math with text",
      `${lineWord(line)} does math with text. Text in quotes is not a number, even "5". Use int() to turn text into a number.`,
      raw,
    );
  }
  // `roll < "12"`, or `needed = "15"` then `roll >= needed`: a number and text, compared.
  const compared = message.match(/'(<|>|<=|>=)' not supported between instances of '(\w+)' and '(\w+)'/);
  if (compared && [compared[2], compared[3]].includes("str") && [compared[2], compared[3]].some((kind) => kind === "int" || kind === "float")) {
    return explainNumberAndText(compared[1], code, text, line, raw);
  }
  // `print(clock_color = "red")`: one `=` inside print.
  const keyword = message.match(/print\(\) got an unexpected keyword argument '(\w+)'/)?.[1];
  if (keyword) return explainEqualsInPrint(keyword, text, line, raw, context);

  const notCallable = message.match(/'(\w+)' object is not callable/);
  if (notCallable) {
    const shadowed = definedNames(code).find((entry) => ["print", "input", "len", "str", "int", "range", "list", "sum"].includes(entry.name));
    if (shadowed) {
      return explain(
        "name-taken",
        "Name already taken",
        `Line ${shadowed.line} uses ${shadowed.name} as a variable name, so ${shadowed.name}() stops working. Pick a different name for your variable.`,
        raw,
      );
    }
    // Unit 4: `chalk_wall(0)`, `wall(-1)`: a list read with round brackets.
    if (notCallable[1] === "list" && unitAtLeast(context, LISTS_UNIT_ORDER)) {
      const list = explainListCalled(code, text, line, raw);
      if (list) return list;
    }
    // Unit 3 on: `max_fuel_for = cells * 5`, then `max_fuel_for(4)`. The name called is a box made with `=`.
    const boxCalled = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? calledBox(code, text, line) : null;
    if (boxCalled) {
      const recipe = taskRecipe(boxCalled.name, code, context);
      const made = `line ${boxCalled.line} makes \`${boxCalled.name}\` with \`=\`, so it is a box, not a recipe (function)`;
      if (recipe) {
        return explain(
          "recipe-like-math",
          "A recipe starts with def",
          `${lineWord(line)} calls \`${boxCalled.name}\`, but ${made}. ${recipeShape(recipe, boxCalled.value)}`,
          raw,
        );
      }
      return explain(
        "not-a-function",
        "A box, not a recipe",
        `${lineWord(line)} calls \`${boxCalled.name}\` with ( ), but ${made}. Only a recipe made with \`def\` can be called.${notCallable[1] === "int" || notCallable[1] === "float" ? " To multiply by it, write * between them." : ""}`,
        raw,
      );
    }
    if (notCallable[1] === "int" || notCallable[1] === "float") {
      return explain(
        "use-star-to-multiply",
        "Use * to multiply",
        `${lineWord(line)} puts ( ) right after a number. To multiply, write * between them, like 2 * (3 + 4).`,
        raw,
      );
    }
    return explain(
      "not-a-function",
      "Not a function",
      `${lineWord(line)} puts ( ) after something that is not a function. Only functions like print() can be called with ( ).`,
      raw,
    );
  }
  if (/takes \d+ positional arguments? but \d+ (were|was) given|missing \d+ required positional argument/.test(message)) {
    return explainValueCount(message, code, line, raw, context);
  }
  return explain("wrong-kind-of-value", "Wrong kind of value", `${lineWord(line)} mixes kinds of values that don't go together: ${message}.`, raw);
}

const BLOCKED_MODULES = new Set([
  "js", "pyodide", "micropip", "urllib", "http", "socket", "ssl", "ftplib", "smtplib", "xmlrpc", "webbrowser",
  "requests", "httpx", "aiohttp",
]);

function explainParsed(parsed: Parsed, raw: string, code: string, context?: ExplainContext): CourseExplanation {
  const { type, message } = parsed;
  const line = errorLine(raw);
  const text = sourceLine(code, line) || shownLine(raw);

  switch (type) {
    case "SyntaxError":
      return explainSyntax(message, type, text, line, raw, code, context);
    case "IndentationError":
    case "TabError":
      return explainIndent(message, line, raw, unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? code : "");
    case "NameError":
      return explainName(message, code, text, line, raw, context);
    case "TypeError":
      return explainType(message, code, text, line, raw, context);
    case "ZeroDivisionError":
      return explain(
        "divide-by-zero",
        "Divided by zero",
        `${lineWord(line)} divides by zero, and no one can do that, not even Mar'tu. Check the number after the /.`,
        raw,
      );
    case "EOFError":
      return explain(
        "out-of-answers",
        "Too many questions",
        "Your code asked for input() more times than this exercise has answers for. Check that you only ask the questions the task asks for.",
        raw,
      );
    case "TimeoutError":
      return explainTimeout(code, raw);
    case "TooMuchOutput":
      return explain(
        "too-much-output",
        "Printing forever?",
        "Your code printed a huge amount, so it was stopped. A loop may be running forever: make sure it has a way to end.",
        raw,
      );
    case "ValueError": {
      const notNumber = message.match(/invalid literal for int\(\) with base 10: (.+)$|could not convert string to float: (.+)$/);
      if (notNumber) {
        const got = notNumber[1] ?? notNumber[2];
        return explain(
          "not-a-number",
          "Not a number",
          `int() and float() can only turn text made of digits, like "12", into a number. This got ${got}.`,
          raw,
        );
      }
      // Unit 4: `chalk_wall.remove(3)` (a position) or `.remove("99")` (text): a value the list does not hold.
      if (/remove\(x\): x not in list/.test(message) && unitAtLeast(context, LISTS_UNIT_ORDER)) {
        return explainRemoveMissing(text, line, raw);
      }
      // Unit 4 (tuples): `across, down, up = cabin`, one name per item.
      const unpack = unitAtLeast(context, LISTS_UNIT_ORDER) ? explainUnpackCount(message, line, raw) : null;
      if (unpack) return unpack;
      // `random.randint(die_size, 1)`: "empty range in randrange(20, 2)" (Python 3.13).
      if (/empty range (in|for) randrange/.test(message) && unitAtLeast(context, RANDOM_UNIT_ORDER)) {
        const swapped = explainRandintBackwards(text, line, raw);
        if (swapped) return swapped;
      }
      break;
    }
    case "IndexError":
      if (/out of range/.test(message)) {
        // Unit 4: in the unit's words (`len(wall)` as a position, the list's own count), never "3 items".
        const list = unitAtLeast(context, LISTS_UNIT_ORDER) ? explainOutOfRange(message, code, text, line, raw) : null;
        if (list) return list;
        const what = /string/.test(message) ? "text" : "list";
        return explain(
          "nothing-at-position",
          "Nothing at that position",
          `${lineWord(line)} asks for a position the ${what} doesn't have. Positions start at 0, so 3 items have positions 0, 1 and 2.`,
          raw,
        );
      }
      break;
    case "AssertionError":
      return explainAssert(message, text, line, raw);
    case "AttributeError": {
      const meant = message.match(/Did you mean: '([^']+)'/)?.[1];
      const attribute = message.match(/attribute '([^']+)'/)?.[1];
      if (attribute && /^_{2,}$/.test(attribute)) return blankLeft(attribute, line, raw);
      // Unit 4: `chalk_wall.sorted()` ("Did you mean 'sort'" would sort the wall itself), `chalk_wall.max()`.
      if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
        const front = explainToolAfterDot(message, text, line, raw);
        if (front) return front;
      }
      if (meant && attribute) {
        return explain("attribute-spelling", "Check the spelling", `There is no ${attribute} here. Did you mean ${meant}?`, raw);
      }
      break;
    }
    case "ModuleNotFoundError": {
      const moduleName = message.match(/No module named '([^']+)'/)?.[1];
      if (moduleName && !BLOCKED_MODULES.has(moduleName.split(".")[0] ?? "")) {
        return explain(
          "no-such-module",
          "No module with that name",
          `Python has no module called ${moduleName}. Check the spelling, like import random or import math.`,
          raw,
        );
      }
      break;
    }
    case "RecursionError":
      return explainRecursion(code, raw);
    case "UnboundLocalError": {
      // Only a recipe (Unit 3 on) can raise this, so the words are the unit's: ingredient, hand back.
      const variable = message.match(/variable '([^']+)'/)?.[1] ?? "a variable";
      return explain(
        "variable-in-function",
        "A box inside a recipe",
        `Inside a recipe (function), ${variable} is changed before it has a value there. Hand it over as an ingredient, or hand the new value back with return.`,
        raw,
      );
    }
    default:
      break;
  }

  const base = explainPython(raw);
  if (base.hint === "The theater does not have a specific hint for this error.") {
    return explain(
      "other",
      base.title,
      `Python stopped with ${type}${onLine(line)}. Read the last line of the error: it says what went wrong.`,
      raw,
    );
  }
  return explain(type === "KeyError" ? "missing-key" : "other", base.title, base.hint, raw);
}

/**
 * Explain a course run's traceback for an 11-15 year old: what happened, and what to try.
 * `context` (optional) makes it more exact: the worked example's code, the task's names, and the previous
 * run's traceback.
 */
export function explainCourseError(traceback: string, code: string, context?: ExplainContext): CourseExplanation {
  const raw = traceback ?? "";
  const parsed = lastException(raw);
  if (!parsed) {
    if (/ran too long/i.test(raw)) return explainTimeout(code, raw);
    // A one-line message from the player itself (for example "Python could not load ... Reload the page.").
    const single = raw.trim();
    if (single && !single.includes("\n")) return explain("player-message", "Python had a problem", single, raw);
    return explain(
      "other",
      "Python error",
      "Read the last line of the error: it names the problem, and the line number shows where to look.",
      raw,
    );
  }
  try {
    const full = explainParsed(parsed, raw, code ?? "", context);
    const result = context?.explainer === "lean" ? leanExplanation(full, raw) : full;
    return nextErrorAfterFix(result, parsed, raw, context);
  } catch (error) {
    // Never let a surprise in the explainer hide the student's error: fall back to Python's own words.
    console.error("Could not explain this error.", error);
    const line = errorLine(raw);
    return explain(
      "other",
      "Python stopped",
      `Python stopped with ${parsed.type}${onLine(line)}${parsed.message ? `: ${parsed.message}` : ""}. Read the last line of the error: it says what went wrong.`,
      raw,
    );
  }
}

const PARSE_ERRORS = new Set(["SyntaxError", "IndentationError", "TabError"]);

/** Kinds that mean "still no quotes": a line that now parses but has the same slip is not a fix. */
const STILL_UNQUOTED = new Set<CourseErrorKind>(["unquoted-word", "unquoted-words", "missing-quote", "unknown-name", "lone-name"]);

/**
 * "One fixed! Python found the next one.": only when something really was fixed. The error moved to a later
 * line, or the same line now parses (a SyntaxError became a run-time error) and the new error is not the same
 * slip again (`companion = Bomb Shell` -> `companion = kratos` still has no quotes), or the same line now fails
 * another way at run time (a NameError mended, and now a TypeError). Never for a new error on the same line that
 * is still unreadable (`print("Shield up!')` -> `print("Shield up!)"`).
 *
 * In a debugging exercise (`context.debugging`) the hint keeps no prefix: the player shows GOT_FURTHER_LINE on a
 * line of its own, so there is one clear progress line, not two.
 */
function nextErrorAfterFix(result: CourseExplanation, parsed: Parsed, raw: string, context?: ExplainContext): CourseExplanation {
  const previousRaw = context?.previous ?? "";
  if (!previousRaw || result.kind === "timeout" || result.kind === "too-much-output") return result;
  const previous = lastException(previousRaw);
  if (!previous || previous.type === "TimeoutError" || /ran too long/i.test(previousRaw)) return result;
  const line = errorLine(raw);
  const previousLine = errorLine(previousRaw);
  if (line === null || previousLine === null) return result;
  const later = line > previousLine;
  // The code could not be read before and now it can: that slip is mended, wherever the next error is (an
  // `import` missing on line 1 after a SyntaxError on line 16). On the same line, the same unquoted slip again
  // (`companion = Bomb Shell` -> `companion = kratos`) is not a fix.
  const nowParses =
    PARSE_ERRORS.has(previous.type) &&
    !PARSE_ERRORS.has(parsed.type) &&
    (line !== previousLine || !STILL_UNQUOTED.has(result.kind));
  const otherRunTimeSlip =
    line === previousLine && !PARSE_ERRORS.has(previous.type) && !PARSE_ERRORS.has(parsed.type) && previous.type !== parsed.type;
  // `def hero = "Lucky"` -> `def hero(): "Lucky"`: it reads now, but the box is still a recipe (no "One fixed!").
  if (result.kind === "def-for-variable" && /^\s*def\b/.test(shownLine(previousRaw))) return result;
  if (!later && !nowParses && !otherRunTimeSlip) return result;
  if (context?.debugging) return { ...result, gotFurther: true };
  return { ...result, gotFurther: true, hint: `${ONE_FIXED_PREFIX} ${result.hint}` };
}

/**
 * What each kind of slip is called when the fix is left out (`explainer: "lean"`). Every kind has a name, so a
 * new kind cannot ship without one.
 */
const SLIP_NAMES: Record<CourseErrorKind, string> = {
  "missing-quote": "a missing quote",
  "quotes-dont-match": "quotes that don't match",
  apostrophe: "an apostrophe inside quotes",
  "unclosed-triple-quote": "three quotes that never close",
  "curly-quote": "a curly quote",
  "hidden-character": "a hidden character",
  "odd-character": "a character Python can't read",
  "unquoted-words": "words with no quotes",
  "unquoted-word": "a word with no quotes",
  "def-for-variable": "`def` used to make a box",
  "dash-for-equals": "a dash where a box is made",
  "dash-and-quote": "a dash and a missing quote",
  "colon-for-equals": "a colon where a box is made",
  "name-goes-first": "a box's name on the wrong side",
  "quoted-name": "quotes around a box's name",
  "name-starts-with-number": "a name that starts with a number",
  "number-stuck-to-name": "a number stuck to letters",
  "space-in-name": "a space in a name",
  "dash-in-name": "a dash in a name",
  "lone-name": "a name on its own",
  "example-name": "a name from the example",
  "capital-letters": "capital letters that don't match",
  spelling: "a name spelled two ways",
  "make-it-first": "a box changed before it is made",
  "not-made-yet": "a box that is not made yet",
  "used-too-early": "a box used before it is made",
  "unknown-function": "a function Python doesn't know",
  "unknown-name": "a name Python doesn't know",
  "missing-import": "a missing import",
  "never-closed": "a bracket that never closes",
  "extra-bracket": "an extra bracket",
  "brackets-dont-match": "brackets that don't match",
  "missing-comma": "two values side by side",
  "two-single-quotes": "two ' marks used as a quote",
  "missing-comma-in-list": "a missing comma in a list",
  "print-needs-brackets": "print without brackets",
  "compare-with-double-equals": "one `=` where a question needs two",
  "def-needs-brackets": "a def line without ( )",
  "missing-colon": "a missing colon",
  indent: "spaces at the start of a line",
  "cant-read-line": "a line Python can't read",
  "sign-backwards": "a sign typed backwards",
  "blank-left": "a blank `___` left in",
  "comparison-alone": "a question on its own line",
  "unquoted-option": "text with no quotes in a comparison",
  "else-not-last": "an `else` that is not last",
  "elif-without-if": "an `elif` or `else` with no `if` above it",
  "else-not-lined-up": "an `elif` or `else` not lined up with its `if`",
  "elif-spelling": "`else if` written as two words",
  "else-has-question": "a question after `else`",
  "no-question": "an `if` or `elif` with no question",
  "keyword-capital": "a capital letter in one of Python's words",
  "compare-number-text": "a number compared with text",
  "equals-in-print": "one `=` inside print",
  "method-as-function": "a text method used without a dot",
  "randint-needs-random": "`randint` used on its own",
  "assert-failed": "an assert that came out False",
  "recipe-like-math": "a recipe written like math",
  "quoted-ingredient": "an ingredient name in quotes",
  "randint-backwards": "the numbers in the wrong order",
  "recipe-not-made-yet": "a recipe that is not made yet",
  "recipe-called-too-early": "a recipe called before its `def`",
  "made-inside-recipe": "a name that only lives inside a recipe",
  "not-in-recipe": "a name this recipe never makes",
  "store-backwards": "a store the wrong way round",
  "quoted-recipe-name": "quotes around a recipe's name",
  "list-needs-square-brackets": "round brackets where a list needs square ones",
  "call-needs-round-brackets": "square brackets where a call needs round ones",
  "comma-in-brackets": "a comma inside [ ] where one position goes",
  "list-plus-item": "one item joined to a list with `+`",
  "tool-after-dot": "a tool written after a dot",
  "not-on-the-list": "a value the list does not hold",
  "read-from-none": "a position read from `None`",
  "row-not-item": "a whole row where one of its items is meant",
  "input-is-text": "an input() answer used as a number",
  "text-plus-number": "text joined to a number",
  "number-plus-text": "a number added to text",
  "math-with-text": "math with text",
  "number-in-quotes": "a number in quotes",
  "bar-needs-brackets": "math in the wrong order",
  "name-taken": "a name Python already uses",
  "use-star-to-multiply": "brackets right after a number",
  "not-a-function": "( ) after something that is not a function",
  "wrong-number-of-values": "the wrong number of values handed over",
  "wrong-kind-of-value": "values of kinds that don't go together",
  "divide-by-zero": "a divide by zero",
  "out-of-answers": "more questions than answers",
  "not-a-number": "text that is not a number",
  "nothing-at-position": "a position that isn't there",
  "missing-key": "a missing key",
  "attribute-spelling": "a misspelled name after a dot",
  "no-such-module": "a module name Python doesn't know",
  "never-ending-calls": "a function that never stops calling itself",
  "variable-in-function": "a box changed inside a function",
  timeout: "a program that ran too long",
  "too-much-output": "a program that printed too much",
  "bare-value": "a value on its own",
  "bare-name": "a name on its own",
  "dash-no-effect": "a dash that keeps nothing",
  "print-without-brackets": "print without brackets",
  "player-message": "a problem loading Python",
  other: "an error Python names in its last line",
};

/** Kinds that are not a slip in the code (nothing to leave out): they stay as they are in a lean explainer. */
const ALWAYS_FULL = new Set<CourseErrorKind>(["timeout", "too-much-output", "player-message"]);

/** The plain name of a kind of slip, as the lean explainer says it ("a sign typed backwards"). */
export function slipName(kind: CourseErrorKind): string {
  return SLIP_NAMES[kind];
}

/**
 * The lean explainer (Unit 2's SOLO items and Quick Check 2): the kind of slip and the line, never the fix.
 * Python's own last line stays on screen under it, so the student reads Python first.
 */
export function leanExplanation(full: CourseExplanation, raw = full.raw): CourseExplanation {
  if (ALWAYS_FULL.has(full.kind)) return full;
  const name = SLIP_NAMES[full.kind];
  const line = errorLine(raw);
  // Titles are plain text (no code marks). A name that starts with a code word keeps its small letters.
  const plain = name.replace(/`/g, "").replace(/^(a|an|the) /, "");
  const title = /^(def|else|elif|if|print|randint|input)\b/.test(plain)
    ? `Slip: ${name.replace(/`/g, "")}`
    : `${plain.charAt(0).toUpperCase()}${plain.slice(1)}`;
  return {
    ...full,
    explainer: "lean",
    title,
    hint: `The slip is ${line ? `on line ${line}` : "in your code"}: ${name}. Python's last line, below, says what it found. Mend it yourself, then Run again.`,
  };
}

function explainTimeout(code: string, raw: string): CourseExplanation {
  const loop = /^\s*while\b/m.test(code ?? "")
    ? "A while loop may never end: make sure its condition can become False."
    : "Look for a loop that never ends.";
  return explain("timeout", "Ran too long", `Your code ran for more than 5 seconds, so it was stopped. ${loop}`, raw);
}

/** The source line Python printed under `File "...", line N` (when the code is not at hand). */
function shownLine(raw: string): string {
  const lines = raw.split("\n");
  for (let index = lines.length - 1; index > 0; index -= 1) {
    if (/^\s*File "[^"]+", line \d+/.test(lines[index - 1])) return lines[index] ?? "";
  }
  return "";
}

/* ---------------------------------------------------------------------------------------------- */
/* Slips with no error at all                                                                      */
/* ---------------------------------------------------------------------------------------------- */

export type QuietSlip = CourseExplanation & {
  kind: "bare-value" | "bare-name" | "dash-no-effect" | "print-without-brackets" | "comparison-alone";
  /** The line the slip is on (1-based). */
  line: number;
  /** For "bare-name" and "dash-no-effect": the name on that line. */
  name?: string;
};

const STRING_LITERAL = /^[rRbBuUfF]{0,2}(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')$/;
const NUMBER_LITERAL = /^-?\d+(?:\.\d+)?$/;

/**
 * A line that runs without an error and does nothing, because nothing keeps or shows its value:
 * `"chick-fa-le_women"` alone, `20` alone, `caster` alone (caster exists), `print` with no brackets,
 * `mana - 20` (a dash where = belongs). Only top-level lines are looked at, outside lists and strings.
 *
 * `missingName` is a name a check looked for and could not find ("put `character = ` in front of it").
 */
export function explainQuietSlip(code: string, options: { missingName?: string; context?: ExplainContext } = {}): QuietSlip | null {
  try {
    return findQuietSlip(code, options);
  } catch (error) {
    console.error("Could not look for quiet slips.", error);
    return null;
  }
}

function findQuietSlip(code: string, options: { missingName?: string; context?: ExplainContext }): QuietSlip | null {
  const lines = (code ?? "").split("\n");
  const defined = new Set(definedNames(code).map((entry) => entry.name));
  const printOnly = printOnlyTask(options.context);
  const solution = options.context?.solution ?? "";
  const taskName = (options.context?.names ?? []).find((name) => !COMMON_BUILTINS.includes(name));
  let open: string[] = [];
  let inTriple = false;
  for (let index = 0; index < lines.length; index += 1) {
    const text = lines[index];
    const startOpen = open;
    const scan = scanLine(text, open);
    if (inTriple) {
      if (/"""|'''/.test(text)) inTriple = false;
      continue;
    }
    if (scan.unterminated) {
      if (scan.unterminated.quote.length === 3) inTriple = true;
      open = [];
      continue;
    }
    open = scan.open;
    if (startOpen.length > 0 || /^\s/.test(text)) continue;
    const previous = index > 0 ? codePart(lines[index - 1]) : "";
    if (previous.endsWith("\\")) continue;
    const body = codePart(text).trim();
    if (!body) continue;
    const line = index + 1;
    const where = `Line ${line}`;
    const missing = options.missingName && /^[A-Za-z_]\w*$/.test(options.missingName) ? options.missingName : null;
    const raw = "";

    if (STRING_LITERAL.test(body) || NUMBER_LITERAL.test(body) || body === "True" || body === "False") {
      const keep = missing ?? taskName ?? (STRING_LITERAL.test(body) ? "character" : "number");
      // A print-only task (Lesson 1A): boxes are not taught yet, so the only fix is print.
      const hint = missing
        ? `${where} is a value on its own: ${body}. Python reads it, then forgets it, because no variable keeps it. To keep it, put ${keep} = in front of it: ${keep} = ${body}`
        : printOnly
          ? `${where} is ${STRING_LITERAL.test(body) ? "words in quotes" : "a value"} with no print, so Python reads it, then forgets it. To show it, write \`print(${body})\``
          : `${where} is a value on its own: ${body}. Python reads it, then forgets it. To show it, put it inside print( ): print(${body}). To keep it, put a name and = in front, like ${keep} = ${body}`;
      return {
        ...explain("bare-value", "A value with no name", hint, raw),
        kind: "bare-value",
        line,
      };
    }
    if (body === "print") {
      return {
        ...explain(
          "print-without-brackets",
          "print needs ( )",
          `${where} says print with no brackets, so nothing is shown. Put what to show inside brackets: print("your words")`,
          raw,
        ),
        kind: "print-without-brackets",
        line,
      };
    }
    if (/^[A-Za-z_]\w*$/.test(body) && defined.has(body) && !KEYWORDS.has(body)) {
      // Unit 3 on: a recipe's name with no `()` is a call that never happens (printing it would show the recipe).
      const recipe = unitAtLeast(options.context, FUNCTIONS_UNIT_ORDER) && new RegExp(`^\\s*def\\s+${escapeRegExp(body)}\\s*\\(`, "m").test(code ?? "");
      return {
        ...explain(
          "bare-name",
          "A name on its own",
          recipe
            ? `${where} is only the name \`${body}\`, with no \`()\`, so the recipe never runs. To call it, write \`${body}()\``
            : `${where} is only the name ${body}, so Python looks inside it and does nothing else. To show what ${body} holds, write print(${body}).`,
          raw,
        ),
        kind: "bare-name",
        line,
        name: body,
      };
    }
    const dash = body.match(/^([A-Za-z_]\w*)\s*-(?!=)\s*(.+)$/);
    if (dash && !/=/.test(dash[2]) && (STRING_LITERAL.test(dash[2].trim()) || NUMBER_LITERAL.test(dash[2].trim()) || /^[A-Za-z_]\w*$/.test(dash[2].trim()))) {
      const [, left] = dash;
      const right = dash[2].trim();
      // `mana - spell_cost`: the subtraction is right, only `mana =` is missing (the unit's `mana = mana - cost`).
      // `mana - 14` in a task that puts a new number in the box is a dash typed for =.
      const spendsBox = /^[A-Za-z_]\w*$/.test(right) && defined.has(right) && !KEYWORDS.has(right);
      const spendsInSolution = new RegExp(`^\\s*${escapeRegExp(left)}\\s*(=\\s*${escapeRegExp(left)}\\s*-|-=)`, "m").test(solution);
      const keepAnswer = defined.has(left) && !STRING_LITERAL.test(right) && (spendsBox || spendsInSolution);
      const hint = keepAnswer
        ? `${where} works out ${left} - ${right}, but nothing keeps the answer, so ${left} does not change. To keep it, put \`${left} =\` in front: \`${left} = ${left} - ${right}\``
        : printOnly
          ? `${where} has a name and a dash -, but this task only shows words. To show them, write \`${printFix(right)}\``
          : `${where} uses a dash - where = belongs, so nothing is kept. To store the value, write: ${left} = ${right}`;
      return {
        ...explain("dash-no-effect", "Dash or equals?", hint, raw),
        kind: "dash-no-effect",
        line,
        name: dash[1],
      };
    }
    // `hero == "Lucky"` or `roll >= needed` alone: Python works out True or False, then forgets it.
    const asked = comparisonAlone(text);
    if (asked) {
      const left = /^[A-Za-z_]\w*$/.test(asked.left) && !KEYWORDS.has(asked.left) ? asked.left : undefined;
      const question = `${asked.left} ${asked.op} ${asked.right}`;
      let hint: string;
      if (asked.op === "==" && left) {
        const box = `${left} = ${asked.right}`;
        // `passed == roll >= needed` is a box being made with the wrong sign: showing it makes no sense.
        const show = COMPARE_ANYWHERE.test(maskStrings(asked.right)) ? "" : ` To show the answer, put it inside print( ): \`print(${question})\``;
        hint = `${where} uses \`==\`, which only asks "is it the same?". Python works out True or False, then forgets it, so nothing changes and nothing shows. To put a new value in the box, use one \`=\`: \`${box}\`.${show}`;
      } else {
        const notMade = (options.context?.names ?? []).find((name) => !defined.has(name) && !COMMON_BUILTINS.includes(name));
        const keep = missing ?? notMade ?? "answer";
        hint = `${where} asks \`${question}\` and gets True or False, but nothing keeps or shows the answer. To keep it, put a box name and \`=\` in front: \`${keep} = ${question}\`. To show it, put it inside print( ).`;
      }
      return {
        ...explain("comparison-alone", "A question on its own", hint, raw),
        kind: "comparison-alone",
        line,
        name: left,
      };
    }
  }
  return null;
}
