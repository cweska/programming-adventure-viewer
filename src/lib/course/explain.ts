/**
 * Friendly error explanations for the Intro to Python course (contracts.ts ExplainCourseError).
 *
 * Wraps the campaign's explainPython() and adds plain-language help for the slips this class really
 * makes (docs/intro-to-python/research/student-groups.md, "Class-wide patterns", and the "starting from
 * zero" review, docs/intro-to-python/design/reviews/curriculum-starting-from-zero.md §4.1): unquoted text,
 * unclosed or mismatched quotes, `def` used to make a variable, a dash instead of `=`, `5P + 2S`, a name
 * alone on a line, capital-letter and spelling mismatches, names copied from the worked example,
 * indentation, joining text and numbers, and more.
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
  | "name-starts-with-number"
  | "number-stuck-to-name"
  // names
  | "lone-name"
  | "example-name"
  | "capital-letters"
  | "spelling"
  | "make-it-first"
  | "used-too-early"
  | "unknown-function"
  | "unknown-name"
  | "missing-import"
  // brackets, commas, colons and indents
  | "never-closed"
  | "extra-bracket"
  | "brackets-dont-match"
  | "missing-comma"
  | "missing-comma-in-list"
  | "print-needs-brackets"
  | "compare-with-double-equals"
  | "def-needs-brackets"
  | "missing-colon"
  | "indent"
  | "cant-read-line"
  // values
  | "input-is-text"
  | "text-plus-number"
  | "number-plus-text"
  | "math-with-text"
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

export type CourseExplanation = Explanation & { kind: CourseErrorKind };

/** What the player knows about the exercise. Every field is optional; more context gives more exact help. */
export type ExplainContext = {
  /** The worked example's code: a name copied from it gets "this name is from the example". */
  example?: string;
  /** The names the task asks for (the exercise's "Names to use"). */
  names?: readonly string[];
  /**
   * The previous run's traceback, when that run crashed too. A different error after it reads
   * "One fixed. Python found the next one." (Python stops at the first error, so fixes come one at a time.)
   */
  previous?: string;
};

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

/** Names the code makes before `line` (all of them when the line is unknown). */
function namesBefore(code: string, line: number | null): string[] {
  const names = definedNames(code)
    .filter((entry) => line === null || entry.line < line)
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith("_"));
  return [...new Set(names)];
}

/** Names the worked example makes, that the task does not use. */
function exampleOnlyNames(context: ExplainContext | undefined): string[] {
  if (!context?.example) return [];
  const task = new Set(context.names ?? []);
  return [...new Set(definedNames(context.example).map((entry) => entry.name))].filter((name) => !task.has(name));
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

function quotesProblem(text: string, line: number | null, raw: string, code = ""): CourseExplanation {
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
    // `print("fireball')`: one kind of quote at the start, the other kind at the end.
    if (!tail.includes(quote) && tail.includes(other)) {
      const words = tail.slice(0, tail.lastIndexOf(other));
      return explain(
        "quotes-dont-match",
        "Quotes don't match",
        `The text${onLine(line)} starts with ${quote} but ends with ${other}. Use the same kind of quote at both ends, like ${quote}${words}${quote}.`,
        raw,
      );
    }
    if (tail.replace(/[)\]}\s]/g, "").length > 0) {
      const { fixed, added } = closeQuoteLine(text, start, quote);
      const defFix = defForVariable(fixed);
      if (defFix) {
        return explain(
          "def-for-variable",
          "def makes functions",
          `def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value, with no def. Text needs a quote at both ends too: ${defFix}`,
          raw,
        );
      }
      const dash = dashFix(fixed);
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

function explainSyntax(
  message: string,
  type: string,
  text: string,
  line: number | null,
  raw: string,
  code = "",
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
    return quotesProblem(text, line, raw, code);
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

  const defFix = defForVariable(text);
  if (defFix) {
    return explain(
      "def-for-variable",
      "def makes functions",
      `def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value, with no def: ${defFix}`,
      raw,
    );
  }

  if (/cannot assign to literal/.test(lower)) {
    const swap = text.match(/^\s*(.+?)\s*=(?!=)\s*([A-Za-z_]\w*)\s*$/);
    const example = swap ? `${swap[2]} = ${swap[1]}` : `character = "Kratos"`;
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
    return explain(
      "compare-with-double-equals",
      "Use == to compare",
      `To check if two things are equal${onLine(line)}, use two equals signs: ==. One = is only for making a variable.`,
      raw,
    );
  }
  if (/perhaps you forgot a comma/.test(lower)) {
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
    const unquoted = explainUnquoted(text, code, line, raw);
    if (unquoted) return unquoted;
    const inside = text.match(/\(([^()"']*)\)/)?.[1]?.trim();
    if (inside && /^[A-Za-z0-9][A-Za-z0-9 ,!?.']*[A-Za-z0-9!?.]$/.test(inside) && /[A-Za-z]/.test(inside) && inside.includes(" ")) {
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
    return explain("def-needs-brackets", "def needs ( )", `A def line needs ( ) after the function's name, then a colon, like this: def greet():`, raw);
  }
  if (/expected ':'/.test(lower)) {
    return explain(
      "missing-colon",
      "Missing colon",
      `${lineWord(line)} needs a colon : at the end. Lines that start with if, elif, else, for, while or def always end with :`,
      raw,
    );
  }
  if (/invalid decimal literal|invalid imaginary literal/.test(lower)) {
    return explainStuckNumber(text, code, line, raw);
  }
  if (/expected an indented block|unexpected indent|unindent does not match/.test(lower) || type === "IndentationError") {
    return explainIndent(message, line, raw);
  }
  if (/^invalid syntax/.test(lower)) {
    const unquoted = explainUnquoted(text, code, line, raw);
    if (unquoted) return unquoted;
  }
  return explain(
    "cant-read-line",
    "Python can't read this",
    `Python could not read line ${line ?? "?"}. Look for a missing quote, a missing bracket ( ), or a missing colon :.`,
    raw,
  );
}

function explainIndent(message: string, line: number | null, raw: string): CourseExplanation {
  const after = message.match(/expected an indented block after (.+?) on line (\d+)/);
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

  const forgotImport = message.match(/Did you forget to import '([^']+)'/)?.[1];
  if (forgotImport) {
    return explain("missing-import", "Missing import", `To use ${forgotImport}, add this line at the top of your code: import ${forgotImport}`, raw);
  }

  const dash = dashFix(text, name);
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

  const defined = definedNames(code);
  const known = [...defined.map((entry) => entry.name), ...COMMON_BUILTINS];
  // Trust Python's own "Did you mean" only for names a beginner would know (not ord, iter, ...).
  const suggested = message.match(/Did you mean: '([^']+)'/)?.[1];
  const trusted =
    suggested && !suggested.startsWith("_") && (known.includes(suggested) || suggested.toLowerCase() === name.toLowerCase())
      ? suggested
      : null;
  // Names the student made can be 2 letters off; Python's own names only 1 (so count is not "round").
  const close = trusted ?? closeName(name, defined.map((entry) => entry.name)) ?? closeName(name, COMMON_BUILTINS, 1);

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
    return explain(
      "example-name",
      "Name from the example",
      exampleNameHint(name, taskNamesInstead(code, line, context, [name, ...(assignedHere ? [assignedHere] : [])])),
      raw,
    );
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

  const called = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`).test(text);
  if (called) {
    return explain(
      "unknown-function",
      "Unknown function",
      `Python doesn't know a function called ${name}. Check the spelling, or make it with def before you use it.`,
      raw,
    );
  }
  // A lowercase word in code that already made variables is often a name copied from somewhere else
  // (the example, a friend's screen), so offer both fixes, the task's variables first.
  const assignedHere = text.match(/^\s*([A-Za-z_]\w*)\s*=(?!=)/)?.[1];
  const earlier = taskNamesInstead(code, line, context, [name, ...(assignedHere ? [assignedHere] : [])]);
  if (/^[a-z][a-z0-9_]*$/.test(name) && earlier.length > 0) {
    const shown = earlier.slice(-3).join(", ");
    const whose = context?.names?.length ? "this task's names" : "one your code made";
    return explain(
      "unknown-name",
      "Unknown name",
      `Python doesn't know ${name}. If it's a variable, use ${whose}: ${shown} (spelled exactly). If it's text, put quotes around it: "${name}"`,
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

function inputNames(code: string): string[] {
  return [...(code ?? "").matchAll(/^\s*([A-Za-z_]\w*)\s*=\s*input\s*\(/gm)].map((match) => match[1]);
}

function explainType(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation {
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
  const dash = /unsupported operand type\(s\) for -/.test(message) ? dashFix(text) : null;
  if (dash) {
    return explain(
      "dash-for-equals",
      "Dash or equals?",
      `${lineWord(line)} uses a dash - where Python needs an equals sign =. To make a variable, write: ${dash}`,
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
    return explain(
      "wrong-number-of-values",
      "Wrong number of values",
      `The function call${onLine(line)} has the wrong number of values inside its ( ). Python says: ${message}.`,
      raw,
    );
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
      return explainSyntax(message, type, text, line, raw, code);
    case "IndentationError":
    case "TabError":
      return explainIndent(message, line, raw);
    case "NameError":
      return explainName(message, code, text, line, raw, context);
    case "TypeError":
      return explainType(message, code, text, line, raw);
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
      break;
    }
    case "IndexError":
      if (/out of range/.test(message)) {
        const what = /string/.test(message) ? "text" : "list";
        return explain(
          "nothing-at-position",
          "Nothing at that position",
          `${lineWord(line)} asks for a position the ${what} doesn't have. Positions start at 0, so 3 items have positions 0, 1 and 2.`,
          raw,
        );
      }
      break;
    case "AttributeError": {
      const meant = message.match(/Did you mean: '([^']+)'/)?.[1];
      const attribute = message.match(/attribute '([^']+)'/)?.[1];
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
      return explain(
        "never-ending-calls",
        "Never-ending calls",
        "A function keeps calling itself and never stops. Make sure it has a way to finish with a return that does not call it again.",
        raw,
      );
    case "UnboundLocalError": {
      const variable = message.match(/variable '([^']+)'/)?.[1] ?? "a variable";
      return explain(
        "variable-in-function",
        "Variable inside a function",
        `Inside a function, ${variable} is changed before it has a value there. Pass it in as a parameter, or return the new value instead.`,
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
  const result = explainParsed(parsed, raw, code ?? "", context);
  return nextErrorAfterFix(result, parsed, raw, context);
}

/** "One fixed. Python found the next one.": a different error, at or after the previous one's line. */
function nextErrorAfterFix(result: CourseExplanation, parsed: Parsed, raw: string, context?: ExplainContext): CourseExplanation {
  const previousRaw = context?.previous ?? "";
  if (!previousRaw || result.kind === "timeout" || result.kind === "too-much-output") return result;
  const previous = lastException(previousRaw);
  if (!previous || previous.type === "TimeoutError" || /ran too long/i.test(previousRaw)) return result;
  const line = errorLine(raw);
  const previousLine = errorLine(previousRaw);
  const same = previous.type === parsed.type && previous.message === parsed.message && previousLine === line;
  const later = line === null || previousLine === null || line >= previousLine;
  if (same || !later) return result;
  return { ...result, hint: `One fixed! Python found the next one. ${result.hint}` };
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
  kind: "bare-value" | "bare-name" | "dash-no-effect" | "print-without-brackets";
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
export function explainQuietSlip(code: string, options: { missingName?: string } = {}): QuietSlip | null {
  const lines = (code ?? "").split("\n");
  const defined = new Set(definedNames(code).map((entry) => entry.name));
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
      const keep = missing ?? (STRING_LITERAL.test(body) ? "character" : "number");
      return {
        ...explain(
          "bare-value",
          "A value with no name",
          missing
            ? `${where} is a value on its own: ${body}. Python reads it, then forgets it, because no variable keeps it. To keep it, put ${keep} = in front of it: ${keep} = ${body}`
            : `${where} is a value on its own: ${body}. Python reads it, then forgets it. To show it, put it inside print( ): print(${body}). To keep it, put a name and = in front, like ${keep} = ${body}`,
          raw,
        ),
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
      return {
        ...explain(
          "bare-name",
          "A name on its own",
          `${where} is only the name ${body}, so Python looks inside it and does nothing else. To show what ${body} holds, write print(${body}).`,
          raw,
        ),
        kind: "bare-name",
        line,
        name: body,
      };
    }
    const dash = body.match(/^([A-Za-z_]\w*)\s*-(?!=)\s*(.+)$/);
    if (dash && !/=/.test(dash[2]) && (STRING_LITERAL.test(dash[2].trim()) || NUMBER_LITERAL.test(dash[2].trim()) || /^[A-Za-z_]\w*$/.test(dash[2].trim()))) {
      return {
        ...explain(
          "dash-no-effect",
          "Dash or equals?",
          `${where} uses a dash - where = belongs, so nothing is kept. To store the value, write: ${dash[1]} = ${dash[2].trim()}`,
          raw,
        ),
        kind: "dash-no-effect",
        line,
        name: dash[1],
      };
    }
  }
  return null;
}
