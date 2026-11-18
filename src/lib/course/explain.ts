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
 * comma inside `[ ]`, and `.remove()` handed a value the list does not hold. Unit 5 (dictionaries) adds the sheet's
 * own slips, from the program's sheets (the setup's too): `=` inside a sheet (never "take the quotes off"), a key with
 * no quotes (`{name: "Lucky"}`, `lucky[name]`), text with no quotes as a value (`"name": Gearshift`, never "capital
 * letters"), bare words in `{ }` or `[ ]` (and the variable that holds them), a missing colon after a key, a missing
 * comma Python reports on the next line, a dot or round brackets where a sheet needs square ones, a name where a list
 * needs a position (with the position, from the list's sheets), a KeyError's real cause (a skipped level, the keys
 * the other way round, one level too deep, a near miss, a position, two keys in one `[ ]`, a variable's name in
 * quotes, `==` where one `=` stores, a key read to test whether it is there, a key no line makes), a position past
 * the end of a list of sheets (counted by its sheets), a variable's name in quotes in math, a whole sheet as a key
 * or in a comparison, math with `None`, and `str()` shown on the line's own read. Unit 6 (loops) adds the loop's own
 * slips, read from the program's `for` lines: a list asked for a key inside a loop over it (`roster["name"]`: read the
 * sheet through the loop variable), a whole sheet used as a position (`roster[member]`), a `for` loop over one number
 * (`for i in len(wall):`), a whole sheet or a whole list added to a number (`total + member`, `total + values`), a
 * list's name in quotes in a `for` line (`for gap in "chalk_wall":`, whatever crash it causes later), a recipe's
 * ingredient name used outside the recipe (`mana_bar(hero)` in the loop: hand over the loop variable), a
 * one-ingredient recipe handed its pieces with a comma (`show_on_ley_board(member["name"], member["mana"])`), and a loop
 * over a dictionary given `.items` with no `( )` or two names for one key a pass. Some of
 * these rows say the slip in a sentence of their own when the explainer is lean (`lean`), still never the fix.
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
  | "one-box-per-line"
  | "names-side-by-side"
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
  | "list-tool-without-dot"
  | "items-after-brackets"
  | "tool-after-dot"
  | "not-on-the-list"
  | "read-from-none"
  | "row-not-item"
  // dictionaries (Unit 5)
  | "equals-in-sheet"
  | "key-outside-sheet"
  | "unquoted-key"
  | "dot-on-a-sheet"
  | "name-as-position"
  | "whole-sheet-as-key"
  | "whole-card-compared"
  | "math-with-none"
  // loops (Unit 6)
  | "loop-over-number"
  | "item-as-position"
  | "one-past-the-end"
  | "no-starting-value"
  | "tag-as-name"
  | "list-to-recipe"
  | "break-outside-loop"
  | "colon-in-one-line-loop"
  | "choice-needs-else"
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
  | "outside-print"
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
  /**
   * The lean name of this slip when its kind's general name does not fit it: a dictionary read with round brackets
   * is the list kind's slip (`list-needs-square-brackets`), but its lean name says "a dictionary".
   */
  slip?: string;
  /** The line the slip is on, when Python names the line after it (a sheet's missing comma): the lean explainer says this one. */
  slipLine?: number;
  /**
   * What the lean explainer says in place of "The mistake is on line N: <the slip's name>." when the row has words of its
   * own for the slip and the evidence (Unit 6: "Line 8 asks a list for a tag (key), like `roster["name"]`. A list has
   * positions, not tags."). Never the fix.
   */
  lean?: string;
  /**
   * The fix goes on a line above the one Python stopped at, but the explainer can't say which (a box no line makes
   * yet): the crash banner says "the mistake is on line 5 or a line above it", never only "Fix line 5".
   */
  fixAbove?: boolean;
};

/** The line a debugging exercise shows when a run gets further than the one before (ExercisePlayer). */
export const GOT_FURTHER_LINE = "Python got further: you fixed that mistake.";

/** The prefix an ordinary exercise's explanation gets when a run gets further than the one before. */
export const ONE_FIXED_PREFIX = "One fixed! Python found the next mistake.";

/** Unit 3 ("First Recipes") teaches `def`: before it, the explainer never says "make it with def". */
export const FUNCTIONS_UNIT_ORDER = 3;

/** Unit 2 ("Control Flow") teaches `random.randint`. */
export const RANDOM_UNIT_ORDER = 2;

/**
 * Unit 4 ("Lists") teaches lists: square brackets for a position, `.append()`, `+` between two lists, slices, and
 * the list tools (`sorted`, `max`, `.remove()`, `in`). Its rows name them; before it the older advice is unchanged.
 */
export const LISTS_UNIT_ORDER = 4;

/**
 * Unit 5 ("Dictionaries") teaches sheets: a key in quotes, a colon, then its value; square brackets to read and store
 * by key; values inside values (`caster["abilities"]["magical_affinity"]`); a list of sheets (`roster[2]["name"]`);
 * and `in` on a sheet's keys. Its rows name them; before it the older advice is unchanged.
 */
export const DICTS_UNIT_ORDER = 5;

/**
 * Unit 6 ("Loops") teaches `for` (over a list, a list of sheets and `range(...)`), the loop variable, a running total,
 * `while` and `break`. Its rows name the loop's own words (the loop variable, a pass, `range(...)`); before it the older
 * advice is unchanged.
 */
export const LOOPS_UNIT_ORDER = 6;

/** What the player knows about the exercise. Every field is optional; more context gives more exact help. */
export type ExplainContext = {
  /** The worked example's code: a name copied from it gets "this name is from the example". */
  example?: string;
  /** The names the task asks for (the exercise's "Names to use"). */
  names?: readonly string[];
  /**
   * The previous run's traceback, when that run crashed too. A later error after it (or a line that now
   * parses) reads "One fixed! Python found the next mistake." (Python stops at the first error, so fixes come
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
   * and the list tools; from Unit 5 (DICTS_UNIT_ORDER) the sheet rows name keys in quotes, the colon, square brackets
   * for a key, the level a key sits on and a list of sheets; from Unit 6 (LOOPS_UNIT_ORDER) the loop rows name the loop
   * variable, `range(...)` and a pass (and nothing a later unit teaches: no f-strings, no `None` written in code).
   * Without a unit, those rows stay closed and the older advice is unchanged.
   */
  unitOrder?: number;
  /**
   * A debugging exercise (a Broken spell: "Fix line 3 ...", or the older "Mend line 3 ..."). A run that got further is marked `gotFurther`
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
  /**
   * The exercise's hidden `setup` code, run before the student's (the game's `caster`, as in the campaign). From Unit 5
   * on, its sheets count as the program's own, so a KeyError can name the level a key sits on.
   */
  setup?: string;
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

/** Names as code, joined for a sentence: "`a`", "`a` and `b`", "`a`, `b` and `c`". */
function codeList(names: readonly string[]): string {
  const shown = names.map((name) => `\`${name}\``);
  return shown.length <= 1 ? (shown[0] ?? "") : `${shown.slice(0, -1).join(", ")} and ${shown.at(-1)}`;
}

/** How each comparison sign is said out loud, so a sign typed backwards can be typed the way it is said. */
const SAID_ALOUD: Record<string, string> = { ">=": "greater than or equal to", "<=": "less than or equal to", "!=": "not equal to" };

/** What each kind of opening mark is called (the plain-language guide's words). */
const PAIR_NAMES: Record<string, string> = { "(": "parentheses", "[": "square brackets", "{": "curly braces" };

/** Math signs from a book or a word processor that Python can't read, with the key Python uses instead. */
const TYPED_SIGNS: Record<string, [string, string]> = {
  "×": ["*", "times"],
  "÷": ["/", "divided by"],
  "−": ["-", "minus"],
  "–": ["-", "minus"],
  "—": ["-", "minus"],
};

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
    ? "To Python those are two different names: capitals count, like in a password."
    : "To Python those are two different names.";
  const here = line ? `line ${line}` : "this line";
  if (task.includes(name) && !task.includes(close)) {
    const madeText = codePart(sourceLine(code, made.line)).trim();
    const renamed = madeText.replace(new RegExp(`^${escapeRegExp(close)}(?![\\w])`), name);
    const fix = renamed !== madeText ? `Change line ${made.line} to \`${renamed}\`` : `Rename it to \`${name}\` on line ${made.line}.`;
    return explain(kind, title, `Line ${made.line} makes \`${close}\`, but your step's box is \`${name}\`. ${differ} ${fix}`, raw);
  }
  if (task.includes(close) && !task.includes(name)) {
    return explain(
      kind,
      title,
      `${here[0].toUpperCase()}${here.slice(1)} uses \`${name}\`, but your step's box is \`${close}\`. ${differ} On ${here}, write \`${close}\`, letter for letter.`,
      raw,
    );
  }
  if (!sameLetters) return null;
  return explain(
    kind,
    title,
    `Line ${made.line} makes \`${close}\`, but ${here} uses \`${name}\`. ${differ} Make both lines match, letter for letter.`,
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
  const from = `\`${name}\` is a name from the Example, not from your task.`;
  if (use.length === 1) return `${from} Your task's name is \`${use[0]}\`: write \`${use[0]}\` here.`;
  if (use.length > 1) return `${from} Your task's names are ${codeList(use)}.`;
  return `${from} First make your own box, with the name your step asks for.`;
}

/* ---------------------------------------------------------------------------------------------- */
/* The slips                                                                                       */
/* ---------------------------------------------------------------------------------------------- */

function explain(kind: CourseErrorKind, title: string, hint: string, raw: string): CourseExplanation {
  return { title, hint, raw, kind };
}

/**
 * Python's last line guesses `==` ("Maybe you meant '==' instead of '='?") on slips that have nothing to do with a
 * question (`74 = 47`, `"name" = "Lucky"` in a sheet, two boxes on one line). The reading routine says Python's last
 * line says the same thing in Python's words, so a literal reader would type `==`: the box says the guess is wrong,
 * right after what happened (the fixed line stays last). "" when Python made no such guess.
 */
function wrongGuess(message: string): string {
  return /maybe you meant '=='/i.test(message) ? " Python's last line guesses `==`, but that guess is wrong here." : "";
}

const COUNT_WORDS = ["", "one", "two", "three", "four", "five", "six", "seven"];

/**
 * `hour_2 = 48, hour_3 = 47`: two boxes made on one line, with a comma between them. Python reads it as a question
 * ("Maybe you meant '=='"), and the `==` advice would write nonsense (`hour_2 = 48, hour_3 == 47`): one box per line.
 */
function explainBoxesOnOneLine(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/invalid syntax|cannot assign/i.test(message)) return null;
  const body = codePart(text);
  const mask = maskStrings(body);
  const parts: string[] = [];
  let depth = 0;
  let from = 0;
  for (let at = 0; at < mask.length; at += 1) {
    const char = mask[at];
    if ("([{".includes(char)) depth += 1;
    else if (")]}".includes(char)) depth -= 1;
    else if (char === "," && depth === 0) {
      parts.push(body.slice(from, at));
      from = at + 1;
    }
  }
  parts.push(body.slice(from));
  if (parts.length < 2) return null;
  const made = parts.map((part) => part.trim().match(/^([A-Za-z_]\w*)\s*=(?!=)\s*(\S.*)$/));
  if (made.some((found) => !found || KEYWORDS.has(found[1]))) return null;
  const lines = made.map((found) => `${found?.[1]} = ${found?.[2].trim()}`);
  const fix = lines.length === 2
    ? `put \`${lines[1]}\` on a new line of its own, under \`${lines[0]}\``
    : `put each one on a line of its own: ${codeList(lines)}`;
  return explain(
    "one-box-per-line",
    "One box per line",
    `${lineWord(line)} makes ${COUNT_WORDS[lines.length] ?? lines.length} boxes on one line.${wrongGuess(message)} Python makes one box per line: ${fix}.`,
    raw,
  );
}

/**
 * The list the code makes above `line` (one line, `chalk_wall = [48, 48, 74, ...]`) that holds the number `item`, and
 * its position there, or null. The last such list wins: it is the one the line is about.
 */
function listHolding(code: string, line: number | null, item: string): { list: string; position: number } | null {
  let found: { list: string; position: number } | null = null;
  (code ?? "").split("\n").forEach((text, index) => {
    if (line !== null && index + 1 >= line) return;
    const made = codePart(text).match(/^\s*([A-Za-z_]\w*)\s*=\s*\[([^\][]*)\]\s*$/);
    if (!made) return;
    const position = made[2].split(",").map((piece) => piece.trim()).indexOf(item);
    if (position >= 0) found = { list: made[1], position };
  });
  return found;
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
      `${lineWord(line)} has a dash \`-\` in a name. Python reads \`-\` as minus, like in math. Join the words with an underscore \`_\` instead: \`${fixed}\``,
      raw,
    );
  }
  return explain(
    "space-in-name",
    "No spaces in names",
    `${lineWord(line)} has a space in a name, so Python reads ${codeList(words)} as separate names. A name can't have spaces, like a username. Join the words with an underscore \`_\`: \`${fixed}\``,
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
      `The text${onLine(line)} is missing its closing quote, so Python reads the rest of the line as text too. Close the quote where the words end, before you glue on the next part: \`${joined}\``,
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
        `The apostrophe ' in your text${onLine(line)} ends the text too early, because Python reads it as the closing quote. Put double quotes around text that has an apostrophe: \`"${words || "It's fun"}"\``,
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
        `The text${onLine(line)} starts with \`${quote}\` but ends with \`${other}\`. Quotes come in matching pairs: use the same kind at both ends, like \`${quote}${words}${quote}\`.`,
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
        `The text${onLine(line)} is missing its opening quote. Like quotation marks in English, text needs a quote at the start and at the end: \`${fixed}\``,
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
          `\`def\` makes recipes (functions), not boxes. A box is its name, then \`=\`, then the value, with no \`def\`. The text needs a quote at both ends too: \`${defFix}\``,
          raw,
        );
      }
      if (defFix) {
        return explain(
          "def-for-variable",
          "No def for a box",
          `A box doesn't need \`def\`. A box is its name, then \`=\`, then the value. The text needs a quote at both ends too: \`${defFix}\``,
          raw,
        );
      }
      const dash = dashFix(fixed);
      if (dash && printOnlyTask(context)) return dashInPrintTask(fixed, line, raw, "dash-and-quote", true);
      if (dash) {
        return explain(
          "dash-and-quote",
          "Two fixes on one line",
          `${lineWord(line)} needs two fixes: the text needs its closing quote, and the dash \`-\` should be \`=\`. Write: \`${dash}\``,
          raw,
        );
      }
      if (added) {
        return explain(
          "missing-quote",
          "Missing quote",
          `The text${onLine(line)} is missing its closing quote, and the line is missing its closing \`${added}\`. Quotes and parentheses come in pairs. Write: \`${fixed}\``,
          raw,
        );
      }
      return explain(
        "missing-quote",
        "Missing quote",
        `The text${onLine(line)} is missing its closing quote. Like quotation marks in English, text needs a quote at the start and at the end: \`${fixed}\``,
        raw,
      );
    }
  }
  return explain(
    "missing-quote",
    "Missing quote",
    `Some text${onLine(line)} is missing its closing quote. Like quotation marks in English, text needs a quote at the start and at the end: \`"Hello"\`.`,
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
    `This step only shows words, so it doesn't need \`def\`.${quote} To show words in the Console, write \`${printFix(text)}\``,
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
    `${lineWord(line)} has a word and a dash \`-\`, but this step only shows words.${quote} To show words in the Console, write \`${printFix(text)}\``,
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
      `${lineWord(line)} has values side by side with nothing between them. Put a comma between them: \`${found.fixed}\``,
      raw,
    );
  }
  return explain(
    "unquoted-words",
    "Missing quotes",
    `${lineWord(line)} has words with no quotes around them, so Python tries to read them as code. Put quotes around the words, the way you quote someone's exact words in English: \`${found.fixed}\``,
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
      `${lineWord(line)} has a number with letters stuck to it. A name can't start with a number. To multiply, Python needs the \`*\` sign for times: \`5 * x\`, not \`5x\` like in algebra.`,
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
      `A box's name can't start with a number. Start it with a letter instead, like \`${better}\`.`,
      raw,
    );
  }
  const target = body.match(/^\s*([A-Za-z_]\w*)\s*=/)?.[1];
  const known = namesBefore(code, line).filter((name) => name !== target);
  // The boxes this line is about: `lantern_cost = 3L` wants `lantern_count` and `lantern_price`, never the rope boxes
  // made just above it. Same first word as the box being made, else the letter typed, else the last two made.
  const head = (name: string) => name.split("_")[0]?.toLowerCase() ?? "";
  const sameWord = target ? known.filter((name) => head(name) === head(target) && head(name) !== "") : [];
  const sameLetter = known.filter((name) => name.toLowerCase().startsWith(word.charAt(0).toLowerCase()));
  const these = sameWord.length >= 2 ? sameWord.slice(0, 2) : sameLetter.length === 2 ? sameLetter : known.slice(-2);
  const times = `${number} * ${word}`;
  const algebra = `Python can't read \`${token}\`. In algebra, ${token} means ${number} times ${word}, but Python needs the \`*\` sign for times`;
  return explain(
    "number-stuck-to-name",
    "Number stuck to letters",
    known.includes(word)
      ? `${algebra}: \`${times}\``
      : known.length >= 2
        ? `${algebra}, and only names of boxes you made. Use the boxes for these numbers: ${codeList(these)}.`
        : `${algebra}: \`${times}\`. \`${word}\` must also be a box you made first.`,
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
    `${lineWord(line)} still has the blank \`${blank}\`, like a blank left on a worksheet. Python reads it as a name and finds nothing. Replace \`${blank}\` with your own code: your step says what goes there.`,
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
  const said = SAID_ALOUD[BACKWARDS[typed[0]]];
  return explain(
    "sign-backwards",
    "Sign typed backwards",
    `${lineWord(line)} has ${typed.map((sign) => `\`${sign}\``).join(" and ")}, a sign typed backwards. Type it in the order you say it, "${said}": the \`=\` comes second, ${typed.map((sign) => `\`${BACKWARDS[sign]}\``).join(" and ")}. Write: \`${codePart(fixed).trim()}\``,
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
    `${lineWord(line)} compares with \`${quoted.words}\`, words with no quotes, so Python tries to read them as code. Words you compare need quotes too: \`${quoted.fixed}\``,
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
        ? `Line ${line} has \`elif\` after the \`else\` on line ${before.line}. \`else\` means "otherwise", so it always comes last and catches whatever is left. Move the \`elif\` and its indented lines up, above the \`else\`.`
        : `Line ${line} is a second \`else\`, after the one on line ${before.line}. An \`if\` with its \`elif\`s gets only one \`else\`, and it comes last. Make the first one an \`elif\` with a question.`,
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
      `Line ${line}'s \`${word}\` has more spaces in front than its \`if\` on line ${ifAbove.at}, so Python reads it as one of the indented lines above, where an \`${word}\` can't go. Give line ${line} exactly the same spaces in front as line ${ifAbove.at}.`,
      raw,
    );
  }
  return explain(
    "elif-without-if",
    `${word} needs an if`,
    `Line ${line} starts with \`${word}\`, but no \`if\` comes right before it, lined up the same, so Python can't tell which question it belongs to. Put this line right after the \`if\` and its indented lines, lined up with the \`if\`${word === "elif" ? ", or make it an `if`" : ""}.`,
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
      `${lineWord(line)} compares a number with text: \`${quoted[0]}\` has quotes, so it is text, and Python can't say which is bigger. A number you compare gets no quotes: \`${fixed}\``,
      raw,
    );
  }
  const used = namesOnLine(text);
  const fromInput = inputNames(code).find((name) => used.includes(name));
  if (fromInput) {
    return explain(
      "compare-number-text",
      title,
      `\`${fromInput}\` came from \`input()\`, and \`input()\` always hands back text, like writing on a paper form. So ${lineWord(line).toLowerCase()} compares text with a number. Turn it into a number first: \`int(${fromInput})\``,
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
    `${lineWord(line)} compares a number with text using \`${op}\`. Text is not a number, even \`"15"\`, so Python can't say which is bigger. Make both sides numbers: a number gets no quotes, and \`int()\` turns text into a number.`,
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
      `${lineWord(line)} has an \`=\` inside \`print( )\`. \`print\` only shows things in the Console: it can't make a box. Make the box on its own line first${value ? `, \`${name} = ${value}\`` : ""}, then show it: \`print(${name})\``,
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
      `${lineWord(line)} has one \`=\` inside \`print( )\`. One \`=\` puts a value in a box, and \`print\` can't do that. To show the answer to a question, use a comparison sign, like \`==\` for "is the same as" or \`!=\` for "is not the same as".`,
      raw,
    );
  }
  return explain(
    "equals-in-print",
    "Use == to ask",
    `${lineWord(line)} has one \`=\` inside \`print( )\`. One \`=\` puts a value in a box, and \`print\` can't do that. To ask "is it the same as?", use \`==\`${fixed ? `: \`${fixed}\`` : "."}`,
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
    `The \`assert\` on ${line ? `line ${line}` : "this line"} asked ${what} and got False, so Python stopped there.${message ? ` Its note says: ${/[.!?]$/.test(message) ? message : `${message}.`}` : ""} That's the seal doing its job: the code above it doesn't do what the \`assert\` expects. Print the values it checks to see why, then fix that code.`,
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
    `${lineWord(line)} gives \`else\` a question${question ? `, \`${question}\`` : ""}. \`else\` has no question of its own: it runs when every question above it was False. Write \`else:\` with nothing between \`else\` and the colon. A new question goes after \`elif\` instead.`,
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
      `${lineWord(line)} starts with \`${first}\`. Python's own words, like \`print\` and \`${small}\`, are all small letters, even at the start of a line. Write: \`${fixed}\``,
      raw,
    );
  }
  const bare = body.match(/^(if|elif)\s*:$/)?.[1];
  if (bare) {
    return explain(
      "no-question",
      `${bare} needs a question`,
      `${lineWord(line)} has \`${bare}:\` with no question. \`${bare}\` asks a question, so the question goes between \`${bare}\` and the colon. If the lines under it should run when every question above was False, write \`else:\` instead.`,
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
      `${lineWord(line)} starts with \`${word}\`, so it ends with a colon \`:\`${semicolon ? ", not a semicolon `;`" : ""}. Like a colon before a list in English, it says "here come my steps": the indented lines below. Write: \`${fixed}\``,
      raw,
    );
  }
  return explain(
    "missing-colon",
    "Missing colon",
    `${lineWord(line)} needs a colon \`:\` at the end. A line that starts with a word like \`if\`, \`else\` or \`def\` always ends with \`:\`, like a colon before a list in English.`,
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
  return `\`${recipe.name}\` is a recipe in your task: ${header}, ${steps}.`;
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
    `${lineWord(line)} writes the recipe the way math writes f(x) = 2x. In Python a recipe (function) starts with \`def\`: \`def ${call[1]}(${ingredients.join(", ")}):\`, then an indented ${back}.`,
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
    `${lineWord(line)} puts \`=\` after the parentheses, the way math writes f(x) = 2x. In Python the colon goes right after the parentheses, and the steps go below: \`def ${header[1]}(${ingredients.join(", ")}):\`, then an indented \`return ${header[3]}\`.`,
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
    `${lineWord(line)} has the recipe's name in quotes. A recipe's name has no quotes: it goes right after \`def\`, then parentheses ( ) and a colon: ${header}, with its steps indented under it.`,
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
  // From Unit 6, a recipe the setup makes counts too (the ley board's `show_on_ley_board(text)`).
  const recipes = unitAtLeast(context, LOOPS_UNIT_ORDER) && context?.setup ? `${context.setup}\n${code}` : code;
  const ingredients = count && /^[A-Za-z_]\w*$/.test(name) && unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? recipeIngredients(recipes, name) : null;
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
      const listed = codeList(ingredients);
      const has = ingredients.length === 1 ? "1 ingredient" : `${ingredients.length} ingredients`;
      // Unit 6: one piece of text handed over in parts, with commas, as print takes them (the ley board).
      const called = line ? sourceLine(code, line) : "";
      const textual = /^(text|line|message|words|note|label)$/.test(ingredients[0] ?? "") ||
        new RegExp(`${escapeRegExp(name)}\\s*\\([^)]*["']`).test(codePart(called));
      if (unitAtLeast(context, LOOPS_UNIT_ORDER) && ingredients.length === 1 && handed >= 2 && textual) {
        return explain(
          "wrong-number-of-values",
          "Wrong number of values",
          `\`${name}\` has ${has}, ${listed}, but ${call.charAt(0).toLowerCase()}${call.slice(1)} hands over ${handedText(handed)}. \`${name}\` takes one piece of text: glue the parts into one with \`+\`, and put \`str()\` around a number.`,
          raw,
        );
      }
      return explain(
        "wrong-number-of-values",
        "Wrong number of values",
        `\`${name}\` has ${has}, ${listed}, but ${call.charAt(0).toLowerCase()}${call.slice(1)} hands over ${handedText(handed)}. Hand over one value per ingredient, the way each blank in a Mad Lib gets one word.`,
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
    name ? `\`${name}( )\`${onLine(line)} got the wrong number of values inside its parentheses.` : `Something${onLine(line)} got the wrong number of values inside its parentheses ( ).`,
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
    `${lineWord(line)} rolls with the numbers the wrong way around. Like a die that goes from 1 to 6, the smallest number goes first: \`${fixed}\``,
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
    "A recipe (function) keeps calling itself and never stops. Make sure it can finish with a `return` that doesn't call it again.",
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
      `Line ${line} calls \`${name}\`, but its \`def\` is only on line ${own.start}. Python reads your code like a page, from top to bottom, so move the recipe above the line that calls it.`,
      raw,
    );
  }
  if (called && !own && (context?.names ?? []).includes(name)) {
    return explain(
      "recipe-not-made-yet",
      "Recipe not made yet",
      `\`${name}\` is one of your task's recipes, but no \`def\` line makes it yet. Write it with \`def\`${line ? ` above line ${line}, the line that calls it` : ""}.`,
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
        `${lineWord(line)} puts \`${name}\` into \`${reversed[1]}\`, the wrong way around, so Python looks for a box \`${name}\` that no line makes. The new box goes on the left of \`=\`, the call on the right: ${needs.length === 0 ? `\`${name} = ${reversed[1]}()\`` : `\`${name} = ${reversed[1]}(...)\`, with one value per ingredient`}`,
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
        ? `\`${name}\` comes from the Example, not from your task.`
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
    const belongs = `\`${name}\` belongs to \`${home.recipe}\`${ingredient ? " as one of its ingredients" : ""}, so only that recipe can use it.`;
    const instead = /^return\b/.test(body) && hereBoxes.length > 0
      ? `Inside \`${here.recipe}\`, hand back its own box, \`${hereBoxes.at(-1)}\`.`
      : hereIngredients.length > 0
        ? `Inside \`${here.recipe}\`, use its own ${hereIngredients.length === 1 ? "ingredient" : "ingredients"}, ${list(hereIngredients)}${hereBoxes.length > 0 ? `, and its own ${hereBoxes.length === 1 ? "box" : "boxes"}, ${list(hereBoxes)}` : ""}.`
        : `Inside \`${here.recipe}\`, make what it needs there, or hand it over as an ingredient.`;
    return explain("made-inside-recipe", "Another recipe's name", `${belongs} ${instead}`, raw);
  }
  // Unit 6: the recipe's own ingredient name, used outside it: in a loop, the loop variable goes there.
  if (ingredient && unitAtLeast(context, LOOPS_UNIT_ORDER)) return ingredientOutside(name, home.recipe, code, text, line, raw, context);
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
      `Text over many lines that starts with three quotes${onLine(line)} never ends. Like a poem's opening and closing marks, it needs the same three quotes where the text should stop.`,
      raw,
    );
  }
  if (/unterminated string literal|eol while scanning string literal/.test(lower)) {
    // Unit 5: a sheet's line (`"name: "Gearshift",`, `"name": "Gearshift,`): the quote closes before the colon or
    // the comma, never at the end of the line, where the line would still be broken.
    const sheet = unitAtLeast(context, DICTS_UNIT_ORDER) ? explainSheetQuote(code, text, line, raw) : null;
    if (sheet) return sheet;
    return quotesProblem(text, line, raw, code, context);
  }
  const curly = message.match(/invalid character '([“”‘’])'/);
  if (curly) {
    return explain(
      "curly-quote",
      "Curly quotes",
      `${lineWord(line)} has a curly quote ${curly[1]}, the kind Google Docs and phones make. Python only reads straight quotes, \`"\` or \`'\`. Delete it and type the quote again in your code.`,
      raw,
    );
  }
  if (/invalid non-printable character/.test(lower)) {
    return explain(
      "hidden-character",
      "Hidden character",
      `${lineWord(line)} has a hidden mark Python can't read, often from copy and paste. Delete the spaces on that line and type them again.`,
      raw,
    );
  }
  const odd = message.match(/invalid character '(.)'/);
  if (odd) {
    const sign = TYPED_SIGNS[odd[1]];
    // `ink = █`: the mark is text, so the fix is quotes around it, on the student's own line when the line has no
    // other quotes to get in the way (`print(█ * 5)` -> `print("█" * 5)`).
    const plain = codePart(text).trim();
    const quoted = !/["']/.test(plain) && plain.includes(odd[1]) ? plain.replace(new RegExp(`${escapeRegExp(odd[1])}+`), (run) => `"${run}"`) : null;
    return explain(
      "odd-character",
      "Odd character",
      sign
        ? `${lineWord(line)} has ${odd[1]}, which Python can't read. The keyboard has no ${odd[1]} key, so for ${sign[1]} Python uses \`${sign[0]}\`.`
        : `${lineWord(line)} has ${odd[1]} outside of quotes, where Python can't read it. A mark like ${odd[1]} is text, so it goes inside quotes: \`${quoted ?? `"${odd[1]}"`}\``,
      raw,
    );
  }

  const backwards = explainBackwardsSign(text, line, raw);
  if (backwards) return backwards;

  // Unit 6: `break` outside the loop, a colon inside a one-line loop, a one-line choice with no `else`.
  if (unitAtLeast(context, LOOPS_UNIT_ORDER)) {
    const loop = explainLoopSyntax(message, code, text, line, raw, context);
    if (loop) return loop;
  }

  // Unit 5: a sheet's own slips (`"name" = "Lucky",`, `spell_book(spell_name) = spell`, a missing colon or comma inside
  // `{ }`, bare words as a key or a value), before the box, recipe and `==` rows that would answer them wrongly.
  if (unitAtLeast(context, DICTS_UNIT_ORDER)) {
    const sheet = explainSheetSyntax(message, code, text, line, raw, context);
    if (sheet) return sheet;
  }

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
      `\`def\` makes recipes (functions), not boxes. A box is its name, then \`=\`, then the value, with no \`def\`: \`${defFix}\``,
      raw,
    );
  }
  if (defFix) {
    return explain(
      "def-for-variable",
      "No def for a box",
      `A box doesn't need \`def\`. A box is its name, then \`=\`, then the value: \`${defFix}\``,
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

  // `hour_2 = 48, hour_3 = 47`: two boxes made on one line (never "use ==": nothing asks a question here).
  const boxes = explainBoxesOnOneLine(message, text, line, raw);
  if (boxes) return boxes;

  // `said_yes = answer.lower() = "yes"`, `assert passed = False`: one `=` where a question needs `==`.
  if (/^invalid syntax|cannot assign to (function call|expression|comparison|attribute)/.test(lower) && !/forgot a comma/.test(lower)) {
    const asked = /maybe you meant '=='/.test(lower) || /^\s*(if|elif|while|assert)\b/.test(text) || /cannot assign/.test(lower)
      ? doubleEqualsFix(text)
      : null;
    if (asked) {
      return explain(
        "compare-with-double-equals",
        "Use == to compare",
        `${lineWord(line)} has one \`=\` where a question needs two. One \`=\` puts a value in a box: read it as "gets". Two, \`==\`, ask "is it the same as?". Write: \`${asked}\``,
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
        `${lineWord(line)} has quotes around a box's name.${wrongGuess(message)} Quotes mean these exact letters, so a name never gets them. Take the quotes off \`${quotedName[2]}\`: \`${quotedName[2]} = ${right}\``,
        raw,
      );
    }
    const swap = text.match(/^\s*(.+?)\s*=(?!=)\s*([A-Za-z_]\w*)\s*$/);
    if (swap) {
      return explain(
        "name-goes-first",
        "Name goes first",
        `In Python, \`=\` works one way: the box's name goes on the left, and the value goes on the right.${wrongGuess(message)} Unlike math, you can't flip the sides: \`${swap[2]} = ${swap[1]}\``,
        raw,
      );
    }
    // Unit 4: `74 = 47`, a list's item on the left: the list's name and the item's position say where 47 goes.
    // Never `chalk_wall = "value"`: copied as it reads, that would replace the whole list.
    const left = codePart(text).trim().match(/^(-?\d+(?:\.\d+)?)\s*=(?!=)\s*(.+)$/);
    const item = left && unitAtLeast(context, LISTS_UNIT_ORDER) ? listHolding(code, line, left[1]) : null;
    if (left && item) {
      return explain(
        "name-goes-first",
        "Name goes first",
        `${lineWord(line)} has the number ${left[1]} on the left of \`=\`, but the left side says where the value goes.${wrongGuess(message)} The ${left[1]} is at position ${item.position} in \`${item.list}\` (count from 0), so write: \`${item.list}[${item.position}] = ${left[2].trim()}\``,
        raw,
      );
    }
    const shown = codePart(text).trim().match(/^(.+?)\s*=(?!=)/)?.[1]?.trim();
    return explain(
      "name-goes-first",
      "Name goes first",
      `${shown ? `${lineWord(line)} has \`${shown}\` on the left of \`=\`.${wrongGuess(message)} ` : ""}In Python, \`=\` works one way: the left side is the box's name, where the value goes, and the value goes on the right. Unlike math, you can't flip the sides.${shown ? "" : wrongGuess(message)}`,
      raw,
    );
  }
  if (/missing parentheses in call to 'print'/.test(lower)) {
    const inside = codePart(text).trim().match(/^print\s+(.+)$/)?.[1];
    return explain(
      "print-needs-brackets",
      "print needs ( )",
      `\`print\` needs parentheses ( ) around what it shows${onLine(line)}, the same marks you use in math class: \`print(${inside ?? '"Hello"'})\``,
      raw,
    );
  }
  if (/maybe you meant '==' or ':=' instead of '='|maybe you meant '==' instead of '='/.test(lower)) {
    const fixed = doubleEqualsFix(text);
    return explain(
      "compare-with-double-equals",
      "Use == to compare",
      fixed
        ? `To ask whether two things are the same${onLine(line)}, use two \`=\` signs: \`==\`. One \`=\` only puts a value in a box. Write: \`${fixed}\``
        : `To ask whether two things are the same${onLine(line)}, use two \`=\` signs: \`==\`. One \`=\` only puts a value in a box.`,
      raw,
    );
  }
  if (/''[A-Za-z]/.test(codePart(text))) {
    // `print(''Shield up'')`: two apostrophes typed for one double quote.
    return explain(
      "two-single-quotes",
      "Two ' are not one \"",
      `${lineWord(line)} has two ' marks side by side. Python reads \`''\` as empty text, not as one \`"\` mark. Use one \`"\` at each end of the text: \`${codePart(text).replace(/''/g, '"').trim()}\``,
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
      const what = { "{": "a dictionary { }", "[": "a list [ ]", "(": "parentheses ( )" }[open[open.length - 1]] ?? "parentheses ( )";
      return explain(
        "missing-comma-in-list",
        "Missing comma",
        `Inside ${what}, every item except the last needs a comma after it, like items in a list in English. Add a comma at the end of line ${line}: \`${body.trim()},\``,
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
      return explain("unquoted-words", "Missing quotes?", `If \`${inside}\` is words, put quotes around them, the way you quote someone's exact words: \`"${inside}"\`.`, raw);
    }
    return explain(
      "missing-comma",
      "Missing comma",
      `${lineWord(line)} has two values side by side with nothing between them. Put a comma between them.`,
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
        `The \`${inside[2]}\`${onLine(line)} is inside the quotes, so Python reads it as part of the text. Move it after the closing quote: \`${`${inside[1]}${inside[3]}${inside[2]}`.trim()}\``,
        raw,
      );
    }
    if (body && !scan.unterminated && scan.open.length > 0 && !/[([{]$/.test(body)) {
      const fixed = `${body}${closersFor(scan.open)}`;
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `A \`${opener}\`${onLine(line)} opens but never closes. Like quotes, ${PAIR_NAMES[opener]} come in pairs. Add \`${closing}\` at the end of the line: \`${fixed.trim()}\``,
        raw,
      );
    }
    // `print(#"I am keeping the glug.")`: a `#` inside the parentheses makes the rest of the line a note, `)` too.
    if (scan.comment >= 0 && !scan.unterminated && scan.open.length > 0) {
      const unswitched = `${text.slice(0, scan.comment)}${text.slice(scan.comment + 1)}`.trim();
      const switchOff = (context?.solution ?? "").split("\n").some((row) => row.trim().replace(/^#\s*/, "# ") === `# ${unswitched}`);
      const where = line ? `line ${line}` : "the line";
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `The \`#\`${onLine(line)} is inside the parentheses, so Python skips the rest of the line, \`${closing}\` too. ${
          switchOff
            ? `Put \`#\` at the very start of ${where}, before \`${unswitched.match(/^[A-Za-z_]\w*/)?.[0] ?? unswitched}\`: \`# ${unswitched}\``
            : `Take the \`#\` out of the parentheses: \`${unswitched}\``
        }`,
        raw,
      );
    }
    if (/[([{]$/.test(body)) {
      return explain(
        "never-closed",
        `Missing ${closing}`,
        `The \`${opener}\`${onLine(line)} opens, but its \`${closing}\` never comes. Add \`${closing}\` on its own line after the last item.`,
        raw,
      );
    }
    return explain(
      "never-closed",
      `Missing ${closing}`,
      `A \`${opener}\`${onLine(line)} never gets its closing \`${closing}\`. Like quotes, ${PAIR_NAMES[opener]} come in pairs: add \`${closing}\` where it should end.`,
      raw,
    );
  }
  const unmatched = message.match(/unmatched '([)\]}])'/);
  if (unmatched) {
    return explain(
      "extra-bracket",
      `Extra ${unmatched[1]}`,
      `${lineWord(line)} has an extra \`${unmatched[1]}\` with no \`${OPENER[unmatched[1]]}\` to match it. Delete the extra one.`,
      raw,
    );
  }
  if (/closing parenthesis '.' does not match opening parenthesis/.test(lower)) {
    return explain(
      "brackets-dont-match",
      "Marks don't match",
      `The marks${onLine(line)} don't pair up. Each kind closes with its own partner: \`(\` with \`)\`, \`[\` with \`]\`, and \`{\` with \`}\`.`,
      raw,
    );
  }
  if (/expected '\('/.test(lower) && /^\s*def\b/.test(text)) {
    const recipe = unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? codePart(text).match(/^\s*def\s+([A-Za-z_]\w*)\s*:?\s*$/)?.[1] : undefined;
    if (recipe) {
      return explain("def-needs-brackets", "def needs ( )", `A \`def\` line needs parentheses ( ) after the recipe's name, then a colon: \`def ${recipe}():\``, raw);
    }
    return explain("def-needs-brackets", "def needs ( )", `A \`def\` line needs parentheses ( ) after the name, then a colon: \`def greet():\``, raw);
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
    // Unit 4: the wall's row copied as it looks (`hours = 48 48 47`), `chalk_wall.pop[]`, and the items typed after
    // the starter's empty brackets (`chalk_wall = [] 48, 48, 47`).
    if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
      const list = explainNumbersSideBySide(text, line, raw) ?? explainEmptySquareCall(code, text, line, raw) ?? explainItemsAfterBrackets(text, line, raw);
      if (list) return list;
    }
    // `lantern_cost = lantern_count lantern_price`: two of the code's names side by side, the algebra habit (5P).
    const sideBySide = explainNamesSideBySide(code, text, line, raw, context);
    if (sideBySide) return sideBySide;
    // `if hours_left < 3;`: a semicolon typed for the colon.
    if (/;\s*$/.test(codePart(text)) && headerWithColon(code, text, line)) return explainMissingColon(code, text, line, raw);
    const option = explainUnquotedOption(text, line, raw);
    if (option) return option;
    const unquoted = explainUnquoted(text, code, line, raw);
    if (unquoted) return unquoted;
    const body = codePart(text).trim();
    // `Night watch`: plain words on a line. One fix, from Mar'tu's version: a note where his line is a note (the
    // note step), else words to show (a step that shows words). Both only when there is no version to read.
    if (/^[A-Za-z][A-Za-z0-9 ,.!?;:-]*$/.test(body) && /\s/.test(body) && !KEYWORDS.has(body.split(/\s+/)[0] ?? "")) {
      const solution = context?.solution;
      const asNote = solution !== undefined && line !== null && /^\s*#/.test(solution.split("\n")[line - 1] ?? "");
      const asShown = solution !== undefined && !asNote && /(^|[^\w.])print\s*\(/.test(solution);
      const note = `A note for people starts with \`#\`, like a stage direction: \`# ${body}\``;
      const shown = `Words to show go in quotes inside \`print( )\`: \`print("${body}")\``;
      return explain(
        "unquoted-words",
        "Words with no quotes",
        `${lineWord(line)} is plain words, so Python tries to read them as code. ${asNote ? note : asShown ? shown : `${note}. ${shown}`}`,
        raw,
      );
    }
    // `_ - =`: marks on a line with no `print` and no quotes.
    if (/^[^A-Za-z0-9"'()[\]{}#\s]+(?:\s+[^A-Za-z0-9"'()[\]{}#\s]+)*$/.test(body)) {
      return explain(
        "unquoted-words",
        "Missing quotes?",
        `${lineWord(line)} has marks with no \`print\` and no quotes, so Python tries to read them as code. To show marks, put them in quotes inside \`print( )\`: \`print("${body}")\``,
        raw,
      );
    }
    // `print(_ - =)`: symbols to show, with no quotes around them.
    const inside = body.match(/^print\s*\(\s*([^"'()]+?)\s*\)$/)?.[1];
    if (inside) {
      return explain(
        "unquoted-words",
        "Missing quotes?",
        `${lineWord(line)} has no quotes inside \`print( )\`, so Python tries to read ${inside} as code. Quotes mean these exact marks: \`print("${inside}")\``,
        raw,
      );
    }
  }
  // A colon is only worth naming once the code has a line that needs one (if, for, while, def ...).
  const colons = /^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\b/m.test(code ?? "");
  return explain(
    "cant-read-line",
    "Python can't read this",
    `Python could not read line ${line ?? "?"}, like a sentence with a missing word. Look for a missing quote${colons ? ", a missing parenthesis ( ), or a missing colon :." : " or a missing parenthesis ( )."}`,
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
    const note = between.some((row) => row.trim().startsWith("#") && indentOf(row) > indent) ? " A note with `#` doesn't count." : "";
    return explain(
      "indent",
      "A recipe needs a step",
      `\`${recipe}\` has no steps yet, and a recipe needs at least one step inside it.${note} Write its step under the \`def\` line, four spaces in. While you think, \`pass\` can hold the spot, like a blank recipe card.`,
      raw,
    );
  }
  if (after) {
    const what = after[1]
      .replace(/^'(\w+)' statement$/, "the `$1`")
      .replace(/^function definition$/, "the `def`")
      .replace(/^class definition$/, "the `class`");
    return explain("indent", "Indent this line", `The line after line ${after[2]} belongs inside ${what}, so it needs 4 spaces at the start, like a sub-point in an outline.`, raw);
  }
  if (/expected an indented block/.test(message)) {
    return explain("indent", "Indent this line", `${lineWord(line)} needs 4 spaces at the start, because it belongs to the line above it that ends with \`:\`.`, raw);
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
      `${lineWord(line)} has a different number of spaces in front than the lines around it. Line it up exactly with the lines it belongs with, using 4 spaces for each level, like an outline.`,
      raw,
    );
  }
  if (/tabs and spaces/.test(message)) {
    return explain("indent", "Tabs and spaces", `${lineWord(line)} mixes tabs and spaces. Delete the indent and use 4 spaces instead.`, raw);
  }
  return explain("indent", "Spaces at the start", `The spaces at the start of line ${line ?? "?"} don't fit. Use 4 spaces for each level, like the sub-points in an outline.`, raw);
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
    return explain("unknown-name", "Unknown name", "Python doesn't know one of the names on this line. Check its spelling, letter for letter, and check that a line above makes it.", raw);
  }

  // `if ___:`: the starter's blank, still there. Python reads it as a name.
  if (/^_{2,}$/.test(name)) return blankLeft(name, line, raw);

  const forgotImport = message.match(/Did you forget to import '([^']+)'/)?.[1];
  if (forgotImport) {
    return explain("missing-import", "Missing import", `To use \`${forgotImport}\`, Python has to bring it in first, once, at the top. Add this line at the top of your code: \`import ${forgotImport}\``, raw);
  }

  // Unit 5: a key or a text value with no quotes, in a sheet (before the capital-letter and near-name rows).
  if (unitAtLeast(context, DICTS_UNIT_ORDER)) {
    const sheet = explainSheetName(name, code, text, line, raw, context);
    if (sheet) return sheet;
  }

  // `roll = randint(1, 6)`: randint lives inside random.
  if (name === "randint" && new RegExp(`(^|[^\\w.])randint\\s*\\(`).test(text)) {
    const fixed = codePart(text).trim().replace(/(^|[^\w.])randint\s*\(/g, "$1random.randint(");
    const imported = definedNames(code).some((entry) => entry.name === "random");
    return explain(
      "randint-needs-random",
      "randint lives in random",
      imported
        ? `${lineWord(line)} uses \`randint\` on its own, but it lives inside \`random\`. Put \`random.\` in front of it: \`${fixed}\``
        : `${lineWord(line)} uses \`randint\` on its own, but it lives inside \`random\`, and this code never brings \`random\` in. Add \`import random\` as the first line, then write: \`${fixed}\``,
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
      `${lineWord(line)} puts the text inside \`${name}( )\`, but \`${name}\` goes after the text, with a dot: the text first, then \`.${name}()\`. Write: \`${fixed}\``,
      raw,
    );
  }

  // Unit 4: `append(33)`: a list tool with no list's name and dot in front (never "write the recipe with def").
  const toolLine = codePart(text).trim();
  const listTool = LIST_TOOLS.has(name) && unitAtLeast(context, LISTS_UNIT_ORDER)
    ? toolLine.match(new RegExp(`(^|[^\\w.])${name}\\s*\\(`))
    : null;
  const toolList = listTool ? listAbove(code, line, context) : null;
  if (listTool && toolList) {
    const at = (listTool.index ?? 0) + listTool[1].length;
    const fixed = `${toolLine.slice(0, at)}${toolList}.${toolLine.slice(at)}`;
    return explain(
      "list-tool-without-dot",
      `${name} goes after a dot`,
      `\`.${name}()\` needs the list's name and a dot in front of it, so Python knows which list to ${name === "append" ? "add to" : "use"}: \`${fixed}\``,
      raw,
    );
  }

  // `hero == "Lucky"` on a line of its own: `==` only asks, so `hero` was never made.
  const alone = comparisonAlone(text);
  if (alone && alone.op === "==" && alone.left === name) {
    return explain(
      "comparison-alone",
      "== asks, = makes",
      `${lineWord(line)} uses \`==\`, which only asks "is it the same as?". It makes nothing, so \`${name}\` was never made. To put a value in a box, use one \`=\`: \`${name} = ${alone.right}\``,
      raw,
    );
  }

  const dash = dashFix(text, name);
  if (dash && printOnlyTask(context)) return dashInPrintTask(text, line, raw, "dash-for-equals");
  if (dash) {
    return explain(
      "dash-for-equals",
      "Dash or equals?",
      `${lineWord(line)} has a dash \`-\` where Python needs \`=\`. A dash means minus. To make a box, write: \`${dash}\``,
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
      `It looks like you made \`${name}\` with a colon \`:\`. A box is made with \`=\`: \`${name} = ${value}\``,
      raw,
    );
  }

  // Unit 3 on: a recipe called above its `def` or not made yet, or a name that only lives inside a recipe.
  if (unitAtLeast(context, FUNCTIONS_UNIT_ORDER)) {
    const recipe = explainRecipeName(name, code, text, line, raw, context);
    if (recipe) return recipe;
  }
  // Unit 6: a name that is only ever a recipe's ingredient (two recipes may share it): never "put quotes around it".
  if (unitAtLeast(context, LOOPS_UNIT_ORDER)) {
    const rows = (code ?? "").split("\n");
    const makes = definedNames(code).filter((entry) => entry.name === name);
    const onlyIngredient = makes.every((entry) => /^\s*def\b/.test(rows[entry.line - 1] ?? ""));
    const home = onlyIngredient ? ingredientHome(name, code, line, context?.setup ?? "") : null;
    if (home) return ingredientOutside(name, home, code, text, line, raw, context);
    // A running total with no start before the loop, or a tag (key) of the loop's sheets used as a name.
    const loop = explainNoStartingValue(name, code, text, line, raw, context) ?? explainTagAsName(name, code, text, line, raw, context);
    if (loop) return loop;
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
        `${lineWord(line)} is only the word \`${name}\`. Did you mean \`print\`? To show words in the Console, write \`print("your words")\`.`,
        raw,
      );
    }
    if (close && !COMMON_BUILTINS.includes(close)) {
      return explain(
        "lone-name",
        "A name on its own",
        `${lineWord(line)} is only the name \`${name}\`. Did you mean \`${close}\`? To show what \`${close}\` holds, write \`print(${close})\`.`,
        raw,
      );
    }
    if (printOnlyTask(context)) {
      return explain(
        "lone-name",
        "Words with no quotes",
        `${lineWord(line)} is only the word \`${name}\`, with no quotes and no \`print\`, so Python looks for a name it should already know, and finds none. To show it, write \`print("${name}")\``,
        raw,
      );
    }
    // `Lucky` alone on line 4, and a later line uses the step's box `hero` that no line makes: the word is that box's
    // value (Broken spell 1B), so the fix is quotes and the step's own box, never a box named `Lucky`.
    const box = line !== null ? boxStillToMake(code, line, context) : null;
    if (box) {
      return explain(
        "lone-name",
        "A name on its own",
        `${lineWord(line)} is only the word \`${name}\`. With no quotes, Python looks for a box named \`${name}\`, and no line makes one. \`${name}\` is text, so it needs quotes, and your step's box \`${box}\` needs a line that makes it. Write: \`${box} = "${name}"\``,
        raw,
      );
    }
    return explain(
      "lone-name",
      "A name on its own",
      `${lineWord(line)} is only the word \`${name}\`. With no quotes, Python looks for a box named \`${name}\`, and no line makes one. If \`${name}\` is text, it needs quotes: \`"${name}"\``,
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
        `\`${name}\` comes from the Example, not from your task. Your task's recipe is \`${theirs.name}\`: call that one, letter for letter.`,
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
      `To Python, \`${name}\` and \`${close}\` are different names: capitals count, like in a password. Use \`${close}\`, with the same capital letters every time.`,
      raw,
    );
  }
  if (close) {
    return explain("spelling", "Check the spelling", `Python doesn't know \`${name}\`. Did you mean \`${close}\`? Python never guesses a close name, so spell it the same way every time.`, raw);
  }

  const grow = text.match(new RegExp(`^\\s*${escapeRegExp(name)}\\s*([-+*/%]|//|\\*\\*)=`));
  if (grow) {
    return {
      ...explain(
        "make-it-first",
        "Make it first",
        `${lineWord(line)} changes \`${name}\`, but \`${name}\` has no value yet. Give it a starting value on a line above, like \`${name} = 0\``,
        raw,
      ),
      fixAbove: true,
    };
  }

  const later = defined.find((entry) => entry.name === name && line !== null && entry.line > line);
  if (later) {
    return explain(
      "used-too-early",
      "Used too early",
      `Line ${line} uses \`${name}\`, but \`${name}\` is only made on line ${later.line}. Python reads your code like a page, from top to bottom, so make \`${name}\` above line ${line}.`,
      raw,
    );
  }

  // `print(hero)` when no line makes `hero` yet, and `hero` is one of the task's own boxes: make it, above.
  if ((context?.names ?? []).includes(name) && !defined.some((entry) => entry.name === name)) {
    const bare = line !== null ? explainQuietSlip((code ?? "").split("\n").slice(0, line - 1).join("\n")) : null;
    if (bare && bare.kind === "bare-value") {
      const value = codePart(sourceLine(code, bare.line)).trim();
      return {
        ...explain(
          "not-made-yet",
          "Not made yet",
          `\`${name}\` is one of your step's boxes, but no line makes it yet. Line ${bare.line} has the value \`${value}\` on its own: put \`${name} = \` in front of it, so it reads \`${name} = ${value}\``,
          raw,
        ),
        // The fix is on the value's line, not the line Python stopped at: the crash banner says so.
        slipLine: bare.line,
      };
    }
    return {
      ...explain(
        "not-made-yet",
        "Not made yet",
        `\`${name}\` is one of your step's boxes, but no line makes it yet. Make it ${line ? `above line ${line}` : "first"}, on a line that starts with \`${name} = \``,
        raw,
      ),
      fixAbove: true,
    };
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
      beforeFunctions ? "Check the spelling" : "Unknown function",
      beforeFunctions
        ? `Python doesn't know \`${name}\`. Check the spelling against your step, letter for letter: Python's own words, like \`print\`, are all small letters.`
        : unitAtLeast(context, FUNCTIONS_UNIT_ORDER)
          ? `Python doesn't know a recipe (function) called \`${name}\`. Check the spelling, or write the recipe with \`def\` above the line that calls it.`
          : `Python doesn't know a function called \`${name}\`. Check the spelling, or make it with \`def\` before you use it.`,
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
  // `weapon = sword`: the whole value is one bare word, and Mar'tu's version keeps text in that box. One fix, the
  // quotes: never "use one of your step's names" (`weapon = armor_bonus`, another step's box).
  const wholeValue = assignedHere !== undefined && new RegExp(`^\\s*${escapeRegExp(assignedHere)}\\s*=(?!=)\\s*${escapeRegExp(name)}\\s*$`).test(codePart(text));
  if (wholeValue && new RegExp(`^\\s*${escapeRegExp(assignedHere ?? "")}\\s*=(?!=)\\s*["']`, "m").test(context?.solution ?? "")) {
    return explain(
      "unquoted-word",
      "Missing quotes?",
      `\`${name}\` has no quotes, so Python looks for a box named \`${name}\` and finds none. \`${assignedHere}\` holds words, and words need quotes: \`${assignedHere} = "${name}"\``,
      raw,
    );
  }
  const earlier = taskNamesInstead(code, line, context, [name, ...(assignedHere ? [assignedHere] : [])]);
  if (/^[a-z][a-z0-9_]*$/.test(name) && earlier.length > 0) {
    // `mana - mana_cost`: a number is wanted there, so quotes (text) would only lead to the next crash.
    const quotes = inMath(text, name) ? "" : ` If it's text, put quotes around it: \`"${name}"\``;
    // Only names a letter or two away are worth offering as "use this one": a list of unrelated task names
    // (bad_line, error_type ...) sends the student after the wrong thing.
    const nearTask = (context?.names ?? []).filter((task) => task !== name && editDistance(task.toLowerCase(), name.toLowerCase()) <= 2);
    if (nearTask.length > 0) {
      return explain(
        "unknown-name",
        "Unknown name",
        `Python doesn't know \`${name}\`. If it's a box, use your step's name, letter for letter: ${nearTask.slice(0, 2).map((task) => `\`${task}\``).join(" or ")}.${quotes}`,
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
        `Python doesn't know \`${name}\`: no line in your code makes it. Line ${similar.line} makes \`${similar.name}\`, which has a similar name.${quotes}`,
        raw,
      );
    }
    const shown = earlier.slice(-3).map((entry) => `\`${entry}\``).join(" or ");
    const whose = context?.names?.length ? "one of your step's names" : "one of the boxes your code made";
    // A task that only shows words (Lesson 1A) has no boxes: its only name is `print`, so the fix is the quotes.
    if (printOnlyTask(context)) {
      return explain(
        "unknown-name",
        "Unknown name",
        `\`${name}\` has no quotes, so Python looks for a name it should already know, and finds none. Words to show need quotes: \`${loneArgument(text, name) ? quoteLoneArgument(text, name) : `"${name}"`}\``,
        raw,
      );
    }
    return explain(
      "unknown-name",
      "Unknown name",
      `Python doesn't know \`${name}\`. If it's a box, use ${whose}, letter for letter: ${shown}.${quotes}`,
      raw,
    );
  }
  if (/^[A-Za-z]+$/.test(name)) {
    return explain(
      "unquoted-word",
      "Missing quotes?",
      `\`${name}\` has no quotes, so Python looks for a name it should already know, and finds none. Words need quotes, the way you quote someone's exact words: \`"${name}"\``,
      raw,
    );
  }
  return explain("unknown-name", "Unknown name", `Python doesn't know \`${name}\` yet${onLine(line)}. Check the spelling, or make it on a line above with \`${name} = \`.`, raw);
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
 * The one box of the step's names (not one of Python's tools) that no line makes, but a line below `line` uses: the
 * box a lone value on `line` was meant for (`Lucky` alone on line 4, `print(hero)` on line 5). Null when there is
 * not exactly one.
 */
function boxStillToMake(code: string, line: number, context?: ExplainContext): string | null {
  const defined = new Set(definedNames(code).map((entry) => entry.name));
  const below = (code ?? "")
    .split("\n")
    .slice(line)
    .map((row) => maskStrings(codePart(row)));
  const boxes = (context?.names ?? []).filter(
    (name) =>
      /^[A-Za-z_]\w*$/.test(name) &&
      !COMMON_BUILTINS.includes(name) &&
      !CALLED_TOOLS.has(name) &&
      !defined.has(name) &&
      below.some((row) => new RegExp(`(^|[^\\w.])${name}\\b`).test(row)),
  );
  return boxes.length === 1 ? boxes[0] : null;
}

/**
 * `def hero(): "Lucky"` (the student followed Python's "expected '('"), then `print(hero + " is ready.")`: a
 * TypeError about a 'function'. The slip is the def line, so it gets the def-for-variable advice.
 */
function explainRecipeUsedAsBox(message: string, code: string, text: string, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/'function'/.test(message)) return null;
  const used = namesOnLine(text);
  const lines = (code ?? "").split("\n");
  for (let at = 0; at < lines.length; at += 1) {
    const header = codePart(lines[at] ?? "").trim().match(/^def\s+([A-Za-z_]\w*)\s*\(\s*\)\s*:\s*(.*)$/);
    if (!header || !used.includes(header[1])) continue;
    const value = header[2].trim() || lines.slice(at + 1).map((row) => codePart(row).trim()).find(Boolean) || "";
    const shown = value.replace(/^return\s+/, "");
    const fix = shown && !/^(pass|print\b)/.test(shown) ? `${header[1]} = ${shown}` : `${header[1]} = "your value"`;
    // Before Unit 3 the class has not met recipes: the words say only what a box needs.
    if (!unitAtLeast(context, FUNCTIONS_UNIT_ORDER) && context?.unitOrder !== undefined) {
      return explain(
        "def-for-variable",
        "No def for a box",
        `Line ${at + 1} uses \`def\`, so \`${header[1]}\` is not a box, and line ${errorLine(raw) ?? "?"} can't use it as a value. A box needs only its name, \`=\` and a value, with no \`def\` and no parentheses: \`${fix}\``,
        raw,
      );
    }
    return explain(
      "def-for-variable",
      "def makes recipes",
      `Line ${at + 1} uses \`def\`, so \`${header[1]}\` is a recipe, not a box, and line ${errorLine(raw) ?? "?"} can't use it as a value. \`def\` makes recipes, not boxes. A box needs only its name, \`=\` and a value, with no \`def\` and no parentheses: \`${fix}\``,
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

/** The list tools a student calls after a list's name and a dot (`chalk_wall.append(33)`). */
const LIST_TOOLS: ReadonlySet<string> = new Set(["append", "insert", "pop", "remove", "sort", "extend", "index", "count", "clear", "reverse"]);

/**
 * The list a line is about: of the lists made above `line` (`chalk_wall = [...]`), a task name first, then the nearest
 * one above. Null when no line above makes a list.
 */
function listAbove(code: string, line: number | null, context?: ExplainContext): string | null {
  const lists: string[] = [];
  (code ?? "").split("\n").forEach((text, index) => {
    if (line !== null && index + 1 >= line) return;
    const made = codePart(text).match(/^\s*([A-Za-z_]\w*)\s*=(?!=)\s*\[/)?.[1];
    if (made) lists.push(made);
  });
  const task = new Set(context?.names ?? []);
  return [...lists].reverse().find((name) => task.has(name)) ?? lists.at(-1) ?? null;
}

/** Unit 5: a sheet's own tools, called with round brackets (`lucky.get("glug", 0)`). */
const SHEET_TOOLS: ReadonlySet<string> = new Set(["get", "keys", "values", "items"]);

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
    `${lineWord(line)} puts parentheses ( ) after \`${name}\`. To change one item of a list, use square brackets [ ]: \`${swapped.line}\``,
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
    `${lineWord(line)} puts parentheses ( ) after \`${name}\`, so Python tries to run it like a recipe (function). \`${name}\` is a list. Read a list with square brackets [ ]: \`${swapped.fixed}\``,
    raw,
  );
}

/**
 * "... is not subscriptable" on something that is called, never read (`chalk_wall.append[33]`, `sorted[...]`,
 * `max[chalk_wall]`, `range[1, 9]`, a recipe): square brackets where the call needs round ones. `None` (from
 * `x = wall.sort()`) keeps the older words.
 */
function explainToolWithSquareBrackets(
  message: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  extra: ReadonlySet<string> = new Set(),
): CourseExplanation | null {
  if (!/^('(builtin_function_or_method|function|method)' object|type '\w+') is not subscriptable/.test(message)) return null;
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  const body = codePart(text);
  const mask = maskStrings(body);
  for (const found of mask.matchAll(/(?<![\w.])((?:[A-Za-z_]\w*\.)*([A-Za-z_]\w*))\s*\[/g)) {
    const tool = found[2];
    if (!CALLED_TOOLS.has(tool) && !recipes.has(tool) && !extra.has(tool)) continue;
    const open = (found.index ?? 0) + found[0].length - 1;
    const close = matchingBracket(mask, open);
    if (close < 0) continue;
    const fixed = `${found[1]}(${body.slice(open + 1, close)})`;
    return explain(
      "call-needs-round-brackets",
      "Parentheses for a call",
      `${lineWord(line)} puts square brackets [ ] after \`${tool}\`, but \`${tool}\` is a tool you call, like \`print\`. Call it with parentheses ( ): \`${fixed}\``,
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
        ? `${start} For row then item, use two pairs of square brackets, like the row and seat on a theater ticket: ${rows}. A run of items takes a colon: \`[0:2]\`.`
        : `${start} A run of items takes a colon: ${run}. In a list of lists, row then item takes two pairs of square brackets, like \`[2][0]\`.`,
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
      `\`.${name}()\`${onLine(line)} needs one value inside its parentheses: the value to ${name === "count" ? "count" : "use"}.`,
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
      return explain("unquoted-words", "Missing quotes?", `If \`${phrase}\` is words, put quotes around them, the way you quote someone's exact words: \`"${phrase}"\`.`, raw);
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
      `${lineWord(line)} uses \`len(${name})\` as a position. \`len(${name})\` counts the items, but positions start at 0, like a ruler, so the count is one past the last position. Use \`len(${name}) - 1\`, or \`[-1]\`.`,
      raw,
    );
  }
  const reads = [...mask.matchAll(/(?<![\w.\]])([A-Za-z_]\w*)\s*\[/g)].map((match) => match[1]).filter((name) => !KEYWORDS.has(name));
  const name = reads[0];
  const last = "Positions start at 0, like a ruler, so the last position is one less than the number of items. `[-1]` is always the last one.";
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
    `${lineWord(line)} has numbers side by side with nothing between them. To keep many numbers under one name, make a list: commas between the numbers, inside square brackets, ${fix}.`,
    raw,
  );
}

/**
 * Unit 4: `chalk_wall = [] 48, 48, 47`: the items typed after the starter's empty brackets, outside the list. They go
 * between the square brackets.
 */
function explainItemsAfterBrackets(text: string, line: number | null, raw: string): CourseExplanation | null {
  const made = codePart(text).trim().match(/^([A-Za-z_]\w*)\s*=(?!=)\s*\[\s*\]\s*,?\s*([^\s,].*)$/);
  if (!made) return null;
  const items = made[2].replace(/,\s*$/, "").trim();
  const numbers = /^-?\d+(?:\.\d+)?(?:\s*,?\s*-?\d+(?:\.\d+)?)*$/.test(items);
  const listed = numbers ? items.split(/\s*,\s*|\s+/).join(", ") : items;
  return explain(
    "items-after-brackets",
    "Inside the brackets",
    `${lineWord(line)} has ${numbers ? "numbers" : "items"} after the \`]\`, outside the list. The ${numbers ? "numbers" : "items"} go between the square brackets: \`${made[1]} = [${listed}]\``,
    raw,
  );
}

/**
 * `lantern_cost = lantern_count lantern_price`: two names the code made, side by side with no sign. In algebra LP means
 * L times P, but Python needs a sign. The sign comes from Mar'tu's version when it joins the same two names.
 */
function explainNamesSideBySide(code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const known = new Set(namesBefore(code, line));
  for (const found of mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)[ \t]+([A-Za-z_]\w*)(?![\w.([])/g)) {
    const [pair, first, second] = found;
    if (KEYWORDS.has(first) || KEYWORDS.has(second) || !known.has(first) || !known.has(second)) continue;
    const between = (context?.solution ?? "").match(new RegExp(`(?<![\\w.])${escapeRegExp(first)}\\s*(\\*\\*|//|[-+*/%])\\s*${escapeRegExp(second)}(?![\\w.])`))?.[1];
    const at = found.index ?? 0;
    const fixed = between ? `${body.slice(0, at)}${first} ${between} ${second}${body.slice(at + pair.length)}`.trim() : "";
    const sign = between === "*" ? "the `*` sign for times" : between ? `a sign between them, \`${between}\`` : "a math sign between them, like `*` for times";
    return explain(
      "names-side-by-side",
      "Missing math sign",
      `${lineWord(line)} has two names side by side, \`${first}\` and \`${second}\`, with nothing between them. In algebra, LP means L times P, but Python needs ${sign}${fixed ? `: \`${fixed}\`` : "."}`,
      raw,
    );
  }
  return null;
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
      "Parentheses for a call",
      `${lineWord(line)} puts square brackets [ ] after \`${tool}\`, but \`${tool}\` is a tool you call, like \`print\`. Call it with parentheses ( ): \`${found[1]}()\``,
      raw,
    );
  }
  return null;
}

/* ---------------------------------------------------------------------------------------------- */
/* Unit 5 ("Dictionaries"): the program's sheets, and the slips the unit's own wrong answers make   */
/* ---------------------------------------------------------------------------------------------- */

type Token = { type: "str" | "num" | "name" | "op"; value: string; line: number };

/** Python's tokens, roughly: strings (with their text), numbers, names and signs. Comments are skipped. */
function pythonTokens(source: string): Token[] {
  const out: Token[] = [];
  let index = 0;
  let line = 1;
  while (index < source.length) {
    const char = source[index];
    if (char === "\n") {
      line += 1;
      index += 1;
      continue;
    }
    if (char === "#") {
      while (index < source.length && source[index] !== "\n") index += 1;
      continue;
    }
    if (/\s/.test(char)) {
      index += 1;
      continue;
    }
    const prefix = source.slice(index, index + 3).match(/^[rRbBuUfF]{1,2}(?=["'])/)?.[0] ?? "";
    const quoteAt = index + prefix.length;
    if (source[quoteAt] === '"' || source[quoteAt] === "'") {
      const mark = source[quoteAt];
      const quote = source.startsWith(mark.repeat(3), quoteAt) ? mark.repeat(3) : mark;
      let at = quoteAt + quote.length;
      let value = "";
      let closed = false;
      while (at < source.length) {
        if (source[at] === "\\" && at + 1 < source.length) {
          value += source[at + 1];
          at += 2;
          continue;
        }
        if (source.startsWith(quote, at)) {
          closed = true;
          break;
        }
        if (source[at] === "\n") {
          if (quote.length === 1) break;
          line += 1;
        }
        value += source[at];
        at += 1;
      }
      if (!closed) return out;
      out.push({ type: "str", value, line });
      index = at + quote.length;
      continue;
    }
    const word = source.slice(index).match(/^[A-Za-z_]\w*/)?.[0];
    if (word) {
      out.push({ type: "name", value: word, line });
      index += word.length;
      continue;
    }
    const number = source.slice(index).match(/^\d[\d_]*(?:\.\d+)?/)?.[0];
    if (number) {
      out.push({ type: "num", value: number, line });
      index += number.length;
      continue;
    }
    const sign = source.slice(index).match(/^(==|!=|<=|>=|\*\*|\/\/|[-+*/%]=|.)/)?.[0] ?? char;
    out.push({ type: "op", value: sign, line });
    index += sign.length;
  }
  return out;
}

type SheetValue = "number" | "text" | "sheet" | "list" | "name" | "other";

/**
 * One key of one sheet: `owner` is the variable the outermost sheet is kept in, `path` the keys above this one.
 * `stored`: the line of a key stored by a line of its own (`gearshift["fuel"] = ...`), in the program as sheetsOf()
 * reads it, so a KeyError can leave out the stores that never ran (the line that crashed, and the ones after it).
 */
type SheetEntry = {
  owner: string | null;
  path: string[];
  key: string;
  kind: SheetValue;
  value: string;
  stored?: number;
  /** A key of a variable that holds a card the program has (`spell = spell_book["Lantern Ward"]`): where it lives. */
  from?: { owner: string | null; path: string[] };
};

type Sheets = {
  entries: SheetEntry[];
  /** The variables that hold a sheet made with `{ }` (even an empty one), or a card of one (`spell = book["Glow"]`). */
  names: Set<string>;
  /** The lists made with `[ ]`: for each item, the variable it names, or the text of a sheet's `"name"` key. */
  lists: Map<string, { ref?: string; name?: string }[]>;
};

function valueKind(token: Token | undefined, after: Token | undefined): { kind: SheetValue; value: string } {
  if (!token) return { kind: "other", value: "" };
  if (token.type === "op" && token.value === "{") return { kind: "sheet", value: "" };
  if (token.type === "op" && token.value === "[") return { kind: "list", value: "" };
  if (token.type === "str") return { kind: "text", value: token.value };
  if (token.type === "num") return { kind: "number", value: token.value };
  if (token.type === "op" && token.value === "-" && after?.type === "num") return { kind: "number", value: `-${after.value}` };
  if (token.type === "name") return { kind: "name", value: token.value };
  return { kind: "other", value: "" };
}

/**
 * The program's sheets: every key written in a `{ }` (inner cards too, with the keys above them) and every key
 * stored with `sheet["key"] = ...`, and the lists, so a slip can be named from the student's own sheets.
 */
function programSheets(source: string): Sheets {
  const tokens = pythonTokens(source ?? "");
  const entries: SheetEntry[] = [];
  const names = new Set<string>();
  const lists = new Map<string, { ref?: string; name?: string }[]>();
  type Frame = { bracket: string; path: string[]; owner: string | null; key: string | null; item?: { ref?: string; name?: string } };
  const stack: Frame[] = [];
  for (let at = 0; at < tokens.length; at += 1) {
    const token = tokens[at];
    const frame = stack.at(-1);
    if (token.type === "op" && (token.value === "{" || token.value === "[" || token.value === "(")) {
      let owner = frame?.owner ?? null;
      let path = frame ? (frame.bracket === "{" && frame.key !== null ? [...frame.path, frame.key] : frame.path) : [];
      if (!frame) {
        // `name = {`, or `book["Glow"] = {`: the sheet is kept in `name`, under those keys.
        const before = tokens.slice(Math.max(0, at - 12), at);
        if (before.at(-1)?.value === "=" && before.at(-1)?.type === "op") {
          let back = before.length - 2;
          const keys: string[] = [];
          while (back >= 2 && before[back].value === "]" && before[back - 1].type === "str" && before[back - 2].value === "[") {
            keys.unshift(before[back - 1].value);
            back -= 3;
          }
          if (before[back]?.type === "name") {
            owner = before[back].value;
            path = keys;
            if (token.value === "{" && keys.length === 0) names.add(owner);
            if (token.value === "[" && keys.length === 0) lists.set(owner, []);
          }
        }
      }
      const next: Frame = { bracket: token.value, path, owner, key: null };
      // A sheet written straight into a list: its `"name"` key tells which item it is.
      if (token.value === "{" && frame?.bracket === "[" && frame.owner && lists.has(frame.owner) && stack.length === 1) {
        next.item = {};
        lists.get(frame.owner)?.push(next.item);
      }
      stack.push(next);
      continue;
    }
    if (token.type === "op" && (token.value === "}" || token.value === "]" || token.value === ")")) {
      stack.pop();
      continue;
    }
    if (!frame) continue;
    if (frame.bracket === "[" && stack.length === 1 && frame.owner && lists.has(frame.owner) && token.type === "name") {
      const previous = tokens[at - 1];
      if (previous?.value === "[" || previous?.value === ",") lists.get(frame.owner)?.push({ ref: token.value });
      continue;
    }
    if (frame.bracket !== "{") continue;
    if (token.type === "op" && token.value === ",") {
      frame.key = null;
      continue;
    }
    if (frame.key === null && token.type === "str" && tokens[at + 1]?.value === ":") {
      frame.key = token.value;
      const { kind, value } = valueKind(tokens[at + 2], tokens[at + 3]);
      entries.push({ owner: frame.owner, path: frame.path, key: token.value, kind, value });
      if (token.value === "name" && kind === "text" && frame.item && frame.path.length === 0) frame.item.name = value;
    }
  }
  // `gearshift["fuel"] = "starlode"`, `hero["abilities"]["wisdom"] = 9`: keys stored by a line of their own.
  for (let at = 0; at < tokens.length; at += 1) {
    if (tokens[at].type !== "name" || (at > 0 && tokens[at - 1].line === tokens[at].line)) continue;
    const keys: string[] = [];
    let next = at + 1;
    while (tokens[next]?.value === "[" && tokens[next + 1]?.type === "str" && tokens[next + 2]?.value === "]") {
      keys.push(tokens[next + 1].value);
      next += 3;
    }
    if (keys.length > 0 && tokens[next]?.value === "=" && tokens[next]?.type === "op") {
      const { kind, value } = valueKind(tokens[next + 1], tokens[next + 2]);
      entries.push({ owner: tokens[at].value, path: keys.slice(0, -1), key: keys[keys.length - 1], kind, value, stored: tokens[at].line });
    }
  }
  // `spell = spell_book["Lantern Ward"]`, `hero = roster[1]`: a variable that holds a card the program has gets that
  // card's keys, so a read of `spell` is checked against the Lantern Ward page (never "add the page's name").
  for (let at = 0; at < tokens.length; at += 1) {
    const made = tokens[at];
    if (made.type !== "name" || (at > 0 && tokens[at - 1].line === made.line)) continue;
    if (tokens[at + 1]?.value !== "=" || tokens[at + 1]?.type !== "op" || tokens[at + 2]?.type !== "name") continue;
    let owner: string | null = tokens[at + 2].value;
    let next = at + 3;
    const items = lists.get(owner);
    if (items && tokens[next]?.value === "[" && tokens[next + 1]?.type === "num" && tokens[next + 2]?.value === "]") {
      owner = items[Number(tokens[next + 1].value)]?.ref ?? null;
      next += 3;
    } else if (items) {
      continue;
    }
    const keys: string[] = [];
    while (tokens[next]?.value === "[" && tokens[next + 1]?.type === "str" && tokens[next + 2]?.value === "]") {
      keys.push(tokens[next + 1].value);
      next += 3;
    }
    if (!owner || owner === made.value || (keys.length === 0 && !items) || tokens[next]?.line === made.line) continue;
    const card = entries.filter(
      (entry) => entry.owner === owner && !entry.from && entry.path.length >= keys.length && keys.every((key, index) => entry.path[index] === key),
    );
    if (card.length === 0) continue;
    names.add(made.value);
    for (const entry of card) entries.push({ ...entry, owner: made.value, path: entry.path.slice(keys.length), from: { owner, path: entry.path } });
  }
  return { entries, names, lists };
}

/**
 * The setup's sheets and the student's, as one program (the game hands `caster` over before the code runs). With
 * `ranBefore` (the line Python stopped on, in the student's code), a key stored on that line or later is left out:
 * that store never ran (`bomb_shell["dexterity"] = bomb_shell["dexterity"] + 2` stops on its own right side).
 */
function sheetsOf(code: string, context?: ExplainContext, ranBefore?: number | null): Sheets {
  const setup = context?.setup ?? "";
  const sheets = programSheets(`${setup}\n${code ?? ""}`);
  if (!ranBefore) return sheets;
  const offset = setup.split("\n").length;
  return { ...sheets, entries: sheets.entries.filter((entry) => entry.stored === undefined || entry.stored - offset < ranBefore) };
}

type Read = { text: string; at: number; key?: string; position?: number; name?: string };

/** `base[...][...]` on the line: the base name, and what each pair of square brackets holds. */
type Chain = { base: string; start: number; end: number; reads: Read[] };

function readChains(text: string): Chain[] {
  const body = codePart(text);
  const mask = maskStrings(body);
  const chains: Chain[] = [];
  for (const found of mask.matchAll(/(?<![\w.\]])([A-Za-z_]\w*)\s*\[/g)) {
    if (KEYWORDS.has(found[1])) continue;
    const reads: Read[] = [];
    let open = (found.index ?? 0) + found[0].length - 1;
    let end = open;
    while (mask[open] === "[") {
      const close = matchingBracket(mask, open);
      if (close < 0) break;
      const inside = body.slice(open + 1, close).trim();
      const quoted = inside.match(/^(["'])((?:(?!\1)[^\\]|\\.)*)\1$/);
      const read: Read = { text: inside, at: open };
      if (quoted) read.key = quoted[2];
      else if (/^-?\d+$/.test(inside)) read.position = Number(inside);
      else if (/^[A-Za-z_]\w*$/.test(inside)) read.name = inside;
      reads.push(read);
      end = close + 1;
      open = end;
      while (mask[open] === " ") open += 1;
    }
    if (reads.length > 0) chains.push({ base: found[1], start: found.index ?? 0, end, reads });
  }
  return chains;
}

/** A chain written back as code: `caster["abilities"]["magical_affinity"]`. */
function chainCode(base: string, keys: readonly (string | number)[]): string {
  return `${base}${keys.map((key) => (typeof key === "number" ? `[${key}]` : `["${key}"]`)).join("")}`;
}

/** The keys a chain walks before read `upTo` (positions in a list of sheets are skipped). */
function keysBefore(chain: Chain, upTo: number): string[] {
  return chain.reads.slice(0, upTo).flatMap((read) => (read.key !== undefined ? [read.key] : []));
}

/** The entries of the sheet `chain` reads (its base's own, when the base is a sheet the program makes). */
function entriesFor(sheets: Sheets, base: string): SheetEntry[] {
  const own = sheets.entries.filter((entry) => entry.owner === base);
  if (own.length > 0) return own;
  // A list of sheets (`roster[1]["mana"]`): the keys of the sheets it holds.
  const items = sheets.lists.get(base);
  if (items) {
    const refs = new Set(items.map((item) => item.ref).filter((ref): ref is string => Boolean(ref)));
    const held = sheets.entries.filter((entry) => entry.owner !== null && refs.has(entry.owner));
    if (held.length > 0) return held;
  }
  return sheets.entries;
}

const samePath = (a: readonly string[], b: readonly string[]) => a.length === b.length && a.every((key, index) => key === b[index]);

/** A key spelled nearly like `key` (capitals, a space or `_`, a letter or two): the sheet's own spelling. */
function nearKey(key: string, keys: readonly string[]): string | null {
  const squash = (text: string) => text.toLowerCase().replace(/[\s_-]/g, "");
  const exact = keys.find((entry) => entry !== key && (entry.toLowerCase() === key.toLowerCase() || squash(entry) === squash(key)));
  if (exact) return exact;
  const limit = key.length >= 5 ? 2 : 1;
  return keys.find((entry) => entry !== key && editDistance(entry.toLowerCase(), key.toLowerCase()) <= limit) ?? null;
}

/** Whether the last line above `line` that fills `name` fills it with a number (`fire_bolt_cost = 6`). */
function variableHoldsNumber(code: string, name: string, line: number | null): boolean {
  const rows = (code ?? "").split("\n").slice(0, line ? line - 1 : undefined);
  for (const row of rows.reverse()) {
    const made = codePart(row).match(new RegExp(`^\\s*${escapeRegExp(name)}\\s*=(?!=)\\s*(.+)$`));
    if (made) return /^-?\d+(?:\.\d+)?$/.test(made[1].trim());
  }
  return false;
}

/** The variable the code fills with exactly this text (`spell_name = "Warm Hands"`), if one does. */
function variableHolding(code: string, text: string): string | null {
  for (const row of (code ?? "").split("\n")) {
    const made = codePart(row).match(/^\s*([A-Za-z_]\w*)\s*=(?!=)\s*(["'])(.*)\2\s*$/);
    if (made && made[3] === text) return made[1];
  }
  return null;
}

/** The sheets the code makes with `{ }`, in the setup or the student's code. */
function sheetNames(code: string, context?: ExplainContext): Set<string> {
  return sheetsOf(code, context).names;
}

/**
 * The bracket each character of `body` sits in, outermost first, starting with the brackets still open from the lines
 * above (`open`). Strings are masked, so a bracket inside text is never counted.
 */
function bracketsAt(body: string, open: readonly string[], position: number): { bracket: string; at: number }[] {
  const mask = maskStrings(body);
  const stack: { bracket: string; at: number }[] = open.map((bracket) => ({ bracket, at: -1 }));
  for (let index = 0; index < Math.min(position, mask.length); index += 1) {
    const char = mask[index];
    if (char in CLOSER) stack.push({ bracket: char, at: index });
    else if (char in OPENER && stack.length > 0 && stack[stack.length - 1].bracket === OPENER[char]) stack.pop();
  }
  return stack;
}

/**
 * NameError for a word that belongs in quotes in a sheet (Unit 5): a key with no quotes (`{name: "Lucky"}`,
 * `lucky[name]`, `lucky.get(glug, 0)`), or a value with no quotes (`"name": Gearshift,`,
 * `gearshift["fuel"] = starlode`). Before the capital-letter and near-name rows, which would say `gearshift`. A
 * name one letter off a variable of the code's own (a typo) keeps the spelling rows.
 */
function explainSheetName(name: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const defined = definedNames(code).map((entry) => entry.name);
  if (defined.includes(name) || (context?.names ?? []).includes(name) || COMMON_BUILTINS.includes(name)) return null;
  // A name copied from the worked example or a Teach me hint keeps the example's row.
  if (exampleOnlyNames(context).includes(name)) return null;
  const close = closeName(name, defined);
  const typo = close !== null && close.toLowerCase() !== name.toLowerCase();
  const sheets = sheetNames(code, context);
  // Unit 6: `member` in `for member in roster:` holds one sheet, so `member[name]` is a key with no quotes too.
  if (unitAtLeast(context, LOOPS_UNIT_ORDER)) for (const held of loopSheetNames(code, context)) sheets.add(held);
  const open = line === null ? [] : openBefore(code, line);
  const quote = (from: number) => `${body.slice(0, from)}"${name}"${body.slice(from + name.length)}`.trim();
  for (const found of mask.matchAll(new RegExp(`(?<![\\w.])${escapeRegExp(name)}(?![\\w(])`, "g"))) {
    const at = found.index ?? 0;
    const inside = bracketsAt(body, open, at).at(-1);
    const before = mask.slice(0, at).trimEnd();
    const after = mask.slice(at + name.length).trimStart();
    const keyRule = `A key is text, so it needs quotes: \`"${name}"\`. Without quotes, Python looks for a variable called \`${name}\`.`;
    // `{name: "Lucky"}`: a key, before its colon.
    if (inside?.bracket === "{" && after.startsWith(":") && !typo) {
      return explain("unquoted-key", "Keys need quotes", `${keyRule} ${lineWord(line)}, with the quotes put in: \`${quote(at)}\``, raw);
    }
    // `lucky[name]`, `roster[1][name]`: a key inside a sheet's square brackets.
    if (inside?.bracket === "[" && inside.at > 0 && !typo) {
      const reader = mask.slice(0, inside.at).trimEnd();
      const base = reader.match(/([A-Za-z_]\w*)$/)?.[1];
      if (/\]$/.test(reader) || (base !== undefined && sheets.has(base))) {
        // Every bare key in the line's reads gets its quotes (`gearshift[name] + str(gearshift[mana])`).
        let fixed = body;
        for (const chain of readChains(body).reverse()) {
          for (const read of [...chain.reads].reverse()) {
            if (!read.name || defined.includes(read.name) || (!sheets.has(chain.base) && read === chain.reads[0])) continue;
            const close = matchingBracket(maskStrings(fixed), read.at);
            if (close > read.at) fixed = `${fixed.slice(0, read.at)}["${read.name}"]${fixed.slice(close + 1)}`;
          }
        }
        return explain("unquoted-key", "Keys need quotes", `${keyRule} ${lineWord(line)}, with the quotes put in: \`${fixed.trim()}\``, raw);
      }
    }
    // `lucky.get(glug, 0)`: the key `.get()` looks for.
    if (inside?.bracket === "(" && inside.at > 0 && /\.\s*get\s*$/.test(mask.slice(0, inside.at)) && !typo) {
      return explain("unquoted-key", "Keys need quotes", `${keyRule} ${lineWord(line)}, with the quotes put in: \`${quote(at)}\``, raw);
    }
    // `"name": Gearshift,` inside a sheet, or `gearshift["fuel"] = starlode`: text with no quotes, as a value.
    const value = (inside?.bracket === "{" && before.endsWith(":")) ||
      (/^[A-Za-z_]\w*(\s*\[[^\]]+\])+\s*=$/.test(before) && sheets.has(before.match(/^[A-Za-z_]\w*/)?.[0] ?? ""));
    if (value && !typo && (/^[A-Z]/.test(name) || close === null)) {
      return explain(
        "unquoted-word",
        "Text needs quotes",
        `\`${name}\` has no quotes, so Python looks for a variable called that. Text in a sheet needs quotes: \`${quote(at)}\``,
        raw,
      );
    }
  }
  return null;
}

/** Bare words side by side inside `{ }` or `[ ]`: `"name": Bomb Shell`, `spell_book[Warm Hands]` (Unit 5's words). */
function explainSheetWords(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const pieces: { text: string; square: boolean }[] = [];
  for (let index = 0; index < mask.length; index += 1) {
    if (mask[index] !== "[" && mask[index] !== "{") continue;
    const close = matchingBracket(mask, index);
    if (close > index) pieces.push({ text: body.slice(index + 1, close), square: mask[index] === "[" });
  }
  const above = openBefore(code, line).at(-1);
  if (above === "{" || above === "[") pieces.push({ text: body.replace(/,\s*$/, ""), square: above === "[" });
  const names = namesBefore(code, line);
  for (const piece of pieces) {
    for (const part of splitTopLevel(piece.text)?.parts ?? []) {
      const colon = maskStrings(part).indexOf(":");
      for (const side of colon < 0 ? [part] : [part.slice(0, colon), part.slice(colon + 1)]) {
        const words = side.replace(/^[[{]|[\]}]$/g, "").trim().split(/\s+/).filter(Boolean);
        if (words.length < 2 || !words.every((word) => /^[A-Za-z][A-Za-z'-]*$/.test(word))) continue;
        if (words.some((word) => KEYWORDS.has(word) || names.includes(word))) continue;
        const phrase = words.join(" ");
        const holder = piece.square ? variableHolding(code, phrase) : null;
        return explain(
          "unquoted-words",
          "Missing quotes?",
          `If \`${phrase}\` is text, put quotes around it: \`"${phrase}"\`.${holder ? ` Or use the variable that holds it: \`${holder}\`.` : ""}`,
          raw,
        );
      }
    }
  }
  return null;
}

/**
 * A quote missing on one line of a sheet written over several lines (Unit 5): the line is a key, a colon and a value,
 * so the line is built again from its pieces, each quote where it belongs. A key keeps both quotes; text keeps both;
 * a number or a variable has none. Only a plain `key: value,` line, inside a `{ }` that the lines above opened.
 */
function explainSheetQuote(code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (line === null || openBefore(code, line).at(-1) !== "{") return null;
  const body = codePart(text);
  const lead = body.match(/^\s*/)?.[0] ?? "";
  const plain = body.trim();
  if (!/^["']?[A-Za-z_][\w ]*["']?\s*:/.test(plain) || /[()[\]#]/.test(plain)) return null;
  const colon = plain.indexOf(":");
  const keyText = plain.slice(0, colon);
  const valueText = plain.slice(colon + 1).trim().replace(/,\s*$/, "").trim();
  // A quote inside the words (`"Mar'tu's`) is not a missing one: only a quote at either end is moved.
  const ends = (piece: string) => piece.trim().replace(/^["']/, "").replace(/["']$/, "");
  if (/["']/.test(ends(keyText)) || /["']/.test(ends(valueText))) return null;
  const key = ends(keyText).trim();
  const bare = ends(valueText).trim();
  if (!/^[A-Za-z_][\w ]*$/.test(key) || !bare || /:/.test(bare)) return null;
  const defined = new Set(definedNames(code).map((entry) => entry.name));
  const number = /^-?\d+(?:\.\d+)?$/.test(bare);
  const variable = !number && /^[A-Za-z_]\w*$/.test(bare) && defined.has(bare);
  const value = bare === "{" || number || variable ? bare : `"${bare}"`;
  const fixed = `${lead}"${key}": ${value}${value === "{" ? "" : ","}`.trim();
  // Which quote went missing: the key's (it has no pair of quotes right before the colon), or the value's. Two kinds
  // of quote, one at each end (`'name": ...`), do not match.
  const keyClosed = /^(["'])[^"']*\1\s*$/.test(keyText);
  const opens = (piece: string) => /^\s*["']/.test(piece);
  const mixed = (piece: string) => /^\s*(["'])[^"']*(?!\1)["']\s*$/.test(piece);
  let why: string;
  if (mixed(keyText) || (keyClosed && mixed(valueText))) {
    return explain(
      "quotes-dont-match",
      "Quotes don't match",
      `${lineWord(line)} starts some text with one kind of quote and ends it with the other. Use the same kind of quote at both ends: \`${fixed}\``,
      raw,
    );
  } else if (!keyClosed) {
    why = `The key${onLine(line)} is missing a quote. A key keeps both quotes, ${opens(keyText) ? "and the closing quote goes before the colon" : "one at the start too"}`;
  } else if (number) {
    why = `${lineWord(line)} has a stray quote by the number. A number has no quotes`;
  } else if (variable) {
    why = `${lineWord(line)} has a stray quote by \`${bare}\`, a variable. A variable's name has no quotes`;
  } else {
    why = `The text${onLine(line)} is missing a quote. Text keeps both quotes, ${opens(valueText) ? "and the closing quote goes before the comma" : "one at the start too"}`;
  }
  return explain("missing-quote", "Missing quote", `${why}: \`${fixed}\``, raw);
}

/** The strings on a line, by where they start and end (`[start, end)`), from the mask (their insides are blank). */
function stringSpans(body: string): { start: number; end: number }[] {
  const mask = maskStrings(body);
  return [...mask.matchAll(/(["'])( *)\1/g)].map((found) => ({ start: found.index ?? 0, end: (found.index ?? 0) + found[0].length }));
}

/**
 * `"magical_affinity" 10,`, `{"name": "Gearshift", "max_mana" 20}`: the line with a colon after the key that has
 * none (a string where a key goes, inside `{ }`, with a value after it and no colon), or null.
 */
function colonAfterKey(body: string, open: readonly string[]): string | null {
  const mask = maskStrings(body);
  for (const { start, end } of stringSpans(body)) {
    if (bracketsAt(body, open, start).at(-1)?.bracket !== "{") continue;
    const before = mask.slice(0, start).trimEnd();
    const keyPlace = before === "" ? open.at(-1) === "{" : /[{,]$/.test(before);
    const after = mask.slice(end).trimStart();
    if (!keyPlace || !after || /^[:,}]/.test(after)) continue;
    return `${body.slice(0, end)}: ${body.slice(end).trimStart()}`.trim();
  }
  return null;
}

/** `{"name": "Gearshift" "max_mana": 20}`: the line with a comma between a value and the next key, or null. */
function commaBetweenPairs(body: string, open: readonly string[]): string | null {
  const mask = maskStrings(body);
  // A value (text, a number, a name, or an inner card's closing bracket), spaces, then a key and its colon.
  for (const found of mask.matchAll(/((["']) *\2|-?\d+(?:\.\d+)?|[A-Za-z_]\w*|[}\]])(\s+)(["']) *\4\s*:/g)) {
    const at = found.index ?? 0;
    if (bracketsAt(body, open, at).at(-1)?.bracket !== "{") continue;
    if (!/^[}\]]/.test(found[1]) && !/:$/.test(mask.slice(0, at).trimEnd())) continue;
    const end = at + found[1].length;
    return `${body.slice(0, end)}, ${body.slice(end).trimStart()}`.trim();
  }
  return null;
}

/**
 * `"fuel" = "starlode"` on a line of its own: the quoted word is a key of a sheet the program has, or one Mar'tu's
 * version stores (`gearshift["fuel"] = ...`). The line with the key back inside its sheet, or null (a box's name in
 * quotes keeps the quoted-name row).
 */
function keyOutsideSheet(body: string, code: string, context?: ExplainContext): { key: string; fixed: string } | null {
  const quoted = body.trim().match(/^(["'])([^"'\\]+)\1\s*=(?!=)\s*(.+)$/);
  if (!quoted) return null;
  const [, , key, right] = quoted;
  // Mar'tu's version makes a box of that name: the quoted-name row ("take the quotes off") is right.
  if (new RegExp(`^\\s*${escapeRegExp(key)}\\s*=(?!=)`, "m").test(context?.solution ?? "")) return null;
  const stored = [...(context?.solution ?? "").matchAll(new RegExp(`(?<![\\w.])([A-Za-z_]\\w*(?:\\s*\\[[^\\]]+\\])*)\\s*\\[\\s*(["'])${escapeRegExp(key)}\\2\\s*\\]\\s*=(?!=)`, "g"))];
  const sheets = sheetsOf(code, context);
  const owners = sheets.entries.filter((entry) => entry.key === key && entry.owner !== null && !entry.from);
  const holder = stored[0]?.[1]?.replace(/\s+/g, "") ??
    (new Set(owners.map((entry) => chainCode(entry.owner as string, entry.path))).size === 1 ? chainCode(owners[0].owner as string, owners[0].path) : null);
  if (!holder) return null;
  return { key, fixed: `${holder}["${key}"] = ${right.trim()}` };
}

/**
 * The SyntaxErrors a sheet's own lines give (Unit 5), before the box, recipe and `==` rows that would answer them
 * wrongly: `"name" = "Lucky",` inside `{ }` ("cannot assign to literal": never "take the quotes off"), a sheet called
 * on the left of `=` (`spell_book(spell_name) = spell`: never "a recipe starts with def" or "use =="), a missing colon
 * after a key, a missing comma that Python reports on the next line, and bare words inside the brackets.
 */
function explainSheetSyntax(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const lower = message.toLowerCase();
  const body = codePart(text);
  const open = line === null ? [] : openBefore(code, line);
  const inSheet = (position: number) => bracketsAt(body, open, position).at(-1)?.bracket === "{";
  // `"name" = "Lucky",` (or `name = "Lucky",`, the quotes taken off as the box advice said): `=` inside a sheet. On
  // the sheet's first key Python says "cannot assign to literal"; on a later key it says "':' expected after
  // dictionary key", and the row is the same: a colon, never "a missing colon" with the `=` left in.
  const eq = [...maskStrings(body).matchAll(/(?<![=!<>+\-*/%:])=(?!=)/g)].map((found) => found.index ?? 0).find(inSheet);
  const eqFrom = (at: number) => Math.max((bracketsAt(body, open, at).at(-1)?.at ?? -1) + 1, maskStrings(body).lastIndexOf(",", at) + 1, 0);
  const eqKey = eq === undefined ? "" : body.slice(eqFrom(eq), eq).trim();
  const afterKey = /':' expected after dictionary key/.test(lower) && /^(["'])[^"']*\1$/.test(eqKey);
  if (eq !== undefined && (/cannot assign to literal|maybe you meant '=='/.test(lower) || afterKey)) {
    const from = eqFrom(eq);
    const lead = body.slice(from, eq).match(/^\s*/)?.[0] ?? "";
    const key = /^[A-Za-z_]\w*$/.test(eqKey) ? `"${eqKey}"` : eqKey;
    const fixed = `${body.slice(0, from)}${lead}${key}: ${body.slice(eq + 1).trimStart()}`.trim();
    return explain(
      "equals-in-sheet",
      "A colon in a sheet",
      `${lineWord(line)} has \`=\` inside a sheet.${wrongGuess(message)} Inside a dictionary \`{ }\`, a colon goes between a key and its value, like a word and its meaning in a glossary: \`${fixed}\`. The key keeps its quotes.`,
      raw,
    );
  }
  // `"fuel" = "starlode"`: a key of the sheet (or one Mar'tu's version stores), written with no sheet before it.
  // Never "take the quotes off": the key keeps its quotes, and lives inside its sheet.
  if (/cannot assign to literal/.test(lower) && eq === undefined) {
    const outside = keyOutsideSheet(body, code, context);
    if (outside) {
      return explain(
        "key-outside-sheet",
        "A key lives in its sheet",
        `${lineWord(line)} writes the key \`"${outside.key}"\` with no sheet before it, so Python reads it as text, and text can't store a value.${wrongGuess(message)} A key lives inside its sheet: \`${outside.fixed}\`. The key keeps its quotes.`,
        raw,
      );
    }
  }
  if (/cannot assign to function call/.test(lower)) {
    const at = singleEquals(maskStrings(body))[0];
    const left = at === undefined ? "" : body.slice(0, at).trim();
    const name = left.match(/^([A-Za-z_]\w*)\s*\(/)?.[1];
    if (name && sheetNames(code, context).has(name)) {
      const swapped = squareBracketed(text, name, true);
      if (swapped && swapped.call.trim() === left) {
        // Every `gearshift("mana")` on the line, the right side too: the line shown is the whole mend.
        let mended = swapped.line;
        for (let guard = 0; guard < 8; guard += 1) {
          const next = squareBracketed(mended, name, true);
          if (!next) break;
          mended = next.line;
        }
        return {
          ...explain(
            "list-needs-square-brackets",
            "Square brackets for a sheet",
            `${lineWord(line)} puts parentheses ( ) after \`${name}\`, a dictionary. Store in a dictionary with square brackets [ ]: \`${mended}\``,
            raw,
          ),
          slip: "parentheses where a sheet needs square brackets",
        };
      }
    }
  }
  if (/':' expected after dictionary key/.test(lower)) {
    const fixed = colonAfterKey(body, open);
    return explain(
      "missing-colon",
      "A key needs a colon",
      fixed
        ? `${lineWord(line)} has a key with no colon after it. A key needs a colon before its value: \`${fixed}\``
        : `${lineWord(line)} has a key with no colon after it. A key needs a colon before its value, like \`"name": "Lucky"\`.`,
      raw,
    );
  }
  if (/^invalid syntax/.test(lower)) {
    const words = explainSheetWords(code, text, line, raw);
    if (words) return words;
    // `{"name": "Gearshift" "max_mana": 20}`: two pairs side by side on one line, with no comma between them.
    const comma = commaBetweenPairs(body, open);
    if (comma) {
      return explain(
        "missing-comma-in-list",
        "Missing comma",
        `${lineWord(line)} has two pairs side by side with no comma between them. Inside a dictionary { }, a comma goes between the pairs: \`${comma}\``,
        raw,
      );
    }
  }
  // Inside a sheet over several lines, Python names the line AFTER the slip: a value with no comma after it, or a
  // key and its value side by side with no colon (`"name" "Gearshift",`, the first key's slip).
  if (/^invalid syntax$/.test(lower.trim()) && line !== null && open.at(-1) === "{" && /^\s*["']/.test(body)) {
    const rows = (code ?? "").split("\n");
    let above = line - 2;
    while (above >= 0 && !codePart(rows[above]).trim()) above -= 1;
    const prev = above >= 0 ? codePart(rows[above]).trim() : "";
    const sideBySide = prev.match(/^(["'][^"']*["'])\s+(["'][^"']*["']|-?\d+(?:\.\d+)?|[A-Za-z_]\w*),?$/);
    if (sideBySide) {
      return {
        ...explain(
          "missing-colon",
          "A key needs a colon",
          `Line ${above + 1} has a key and its value side by side with no colon, so Python could not read on. A key needs a colon before its value: \`${sideBySide[1]}: ${sideBySide[2]},\``,
          raw,
        ),
        slipLine: above + 1,
      };
    }
    if (/^["'][^"']*["']\s*:\s*\S/.test(prev) && !/[,{[(]$/.test(prev)) {
      return {
        ...explain(
          "missing-comma-in-list",
          "Missing comma",
          `Line ${above + 1} ends with no comma, so Python read on into line ${line}. Inside a dictionary { }, every item except the last needs a comma after it: \`${prev},\``,
          raw,
        ),
        slipLine: above + 1,
      };
    }
  }
  return null;
}

/**
 * "'dict' object has no attribute 'mana'" (`lucky.mana`, `gearshift.fuel = "starlode"`): a dot where a sheet needs
 * square brackets and the key in quotes. A sheet's own tools (`.get()`) and list tools after a dot keep older rows.
 */
function explainSheetDot(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const body = codePart(text);
  const sheets = sheetsOf(code, context);
  // `roster.lucky`: a list read with a dot and a name. A list takes a position.
  const listed = message.match(/^'list' object has no attribute '([A-Za-z_]\w*)'/);
  if (listed) {
    const read = maskStrings(body).match(new RegExp(`(?<![\\w.])([A-Za-z_]\\w*)\\s*\\.\\s*${escapeRegExp(listed[1])}(?![\\w(])`));
    const items = read ? sheets.lists.get(read[1]) : undefined;
    if (!read || !items) return null;
    const position = items.findIndex((item) => item.ref === listed[1]);
    return explain(
      "name-as-position",
      "A list takes a position",
      `\`${read[1]}\` is a list: a dot and a name can't read it. Read a list by its position, in square brackets${position >= 0 ? `: \`${listed[1]}\` is at position ${position}, \`${read[1]}[${position}]\`` : `, like \`${read[1]}[0]\``}. Positions count from 0.`,
      raw,
    );
  }
  const found = message.match(/^'dict' object has no attribute '([A-Za-z_]\w*)'/);
  if (!found) return null;
  const key = found[1];
  // A key kept in a variable (`spell_book.spell_name`) goes in the brackets with no quotes.
  const variables = new Set(definedNames(code).map((entry) => entry.name).filter((name) => !sheets.entries.some((entry) => entry.key === name)));
  // Every key read with a dot on the line (`gearshift.name + ... + gearshift.mana`), never a call (`lucky.get(...)`).
  const dotted = /(?<=[\w\]])\s*\.\s*([A-Za-z_]\w*)(?![\w(])/g;
  const mask = maskStrings(body);
  if (![...mask.matchAll(dotted)].some((entry) => entry[1] === key)) return null;
  let fixed = "";
  let from = 0;
  for (const entry of mask.matchAll(dotted)) {
    const owner = mask.slice(0, entry.index ?? 0).match(/([A-Za-z_]\w*)\s*$/)?.[1];
    if (owner && MODULES.has(owner)) continue;
    fixed += `${body.slice(from, entry.index ?? 0)}[${variables.has(entry[1]) ? entry[1] : `"${entry[1]}"`}]`;
    from = (entry.index ?? 0) + entry[0].length;
  }
  fixed = mendLevels(`${fixed}${body.slice(from)}`.trim(), sheets);
  const store = /no __dict__ for setting/.test(message);
  return explain(
    "dot-on-a-sheet",
    "Square brackets for a key",
    store
      ? `${lineWord(line)} stores \`${key}\` with a dot. Store in a dictionary with square brackets${variables.has(key) ? "" : ", the key in quotes"}: \`${fixed}\``
      : `${lineWord(line)} reads \`${key}\` with a dot. Read a dictionary with square brackets, not a dot: \`${fixed}\``,
    raw,
  );
}

/** The line with each read that skips a card mended (`gearshift["wisdom"]` -> `gearshift["abilities"]["wisdom"]`). */
function mendLevels(body: string, sheets: Sheets): string {
  let out = body;
  for (const chain of readChains(body).reverse()) {
    const keys = keysBefore(chain, chain.reads.length);
    if (keys.length === 0 || chain.reads.some((read) => read.key === undefined && read.position === undefined)) continue;
    // Only a sheet the program makes (or a card of one, or a list of sheets): never another sheet's keys for a
    // variable the explainer cannot see, which would "mend" a right read into a wrong one.
    if (!sheets.entries.some((entry) => entry.owner === chain.base) && !sheets.lists.has(chain.base)) continue;
    const own = entriesFor(sheets, chain.base);
    const last = keys[keys.length - 1];
    if (own.some((entry) => entry.key === last && samePath(entry.path, keys.slice(0, -1)))) continue;
    const deeper = own.find((entry) => entry.key === last && entry.path.length > keys.length - 1 && samePath(entry.path.slice(0, keys.length - 1), keys.slice(0, -1)));
    if (!deeper) continue;
    const positions = chain.reads.filter((read) => read.key === undefined).map((read) => read.text);
    out = `${out.slice(0, chain.start)}${chainCode(`${chain.base}${positions.map((position) => `[${position}]`).join("")}`, [...deeper.path, last])}${out.slice(chain.end)}`;
  }
  return out;
}

/** "'dict' object is not callable" (`gearshift("mana")`): a sheet read with round brackets. */
function explainSheetCalled(code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const recipes = new Set(recipeBlocks(code).map((block) => block.recipe));
  const sheets = sheetNames(code, context);
  const called = [...maskStrings(codePart(text)).matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\(/g)]
    .map((match) => match[1])
    .filter((name) => !recipes.has(name) && !CALLED_TOOLS.has(name) && !KEYWORDS.has(name));
  const name = called.find((entry) => sheets.has(entry)) ?? called[0];
  const swapped = name ? squareBracketed(text, name, true) : null;
  if (!name || !swapped) return null;
  return {
    ...explain(
      "list-needs-square-brackets",
      "Square brackets for a sheet",
      `${lineWord(line)} puts parentheses ( ) after \`${name}\`, so Python tries to run it like a recipe. \`${name}\` is a dictionary. Read a dictionary with square brackets [ ], not parentheses: \`${swapped.fixed}\``,
      raw,
    ),
    slip: "parentheses where a sheet needs square brackets",
  };
}

/**
 * "list indices must be integers or slices, not str" (`roster["Lucky"]`): a list takes a position, not a name. When
 * the list's sheets say where that name is, the hint gives its position.
 */
function explainNameAsPosition(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/indices must be integers or slices, not str/.test(message)) return null;
  const sheets = sheetsOf(code, context);
  const chain = readChains(text).find((entry) => entry.reads[0]?.key !== undefined && !sheets.names.has(entry.base)) ??
    readChains(text).find((entry) => entry.reads[0]?.key !== undefined);
  if (!chain) return null;
  const word = chain.reads[0].key as string;
  const items = sheets.lists.get(chain.base) ?? [];
  const nameOf = (item: { ref?: string; name?: string }) =>
    item.name ?? sheets.entries.find((entry) => entry.owner === item.ref && entry.path.length === 0 && entry.key === "name" && entry.kind === "text")?.value;
  const position = items.findIndex((item) => (nameOf(item) ?? item.ref ?? "").toLowerCase() === word.toLowerCase());
  const rest = chain.reads.slice(1).map((read) => `[${read.text}]`).join("");
  if (position >= 0) {
    return explain(
      "name-as-position",
      "A list takes a position",
      `\`${chain.base}\` is a list: it takes a position number in \`[ ]\`, not a name. ${word} is at position ${position}: \`${chain.base}[${position}]${rest}\`. Positions count from 0.`,
      raw,
    );
  }
  return explain(
    "name-as-position",
    "A list takes a position",
    `\`${chain.base}\` is a list: it takes a position number in \`[ ]\`, not a name, like \`${chain.base}[0]\`. Positions count from 0.`,
    raw,
  );
}

/**
 * "list indices must be integers or slices, not dict" (`roster[lucky]["name"]`): a whole sheet where the list takes a
 * position. The sheet's own position comes from the list.
 */
function explainSheetAsPosition(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/indices must be integers or slices, not dict/.test(message)) return null;
  const sheets = sheetsOf(code, context);
  for (const chain of readChains(text)) {
    const first = chain.reads[0];
    const items = sheets.lists.get(chain.base);
    if (!first?.name || !items || !sheets.names.has(first.name)) continue;
    const position = items.findIndex((item) => item.ref === first.name);
    const rest = chain.reads.slice(1).map((read) => `[${read.text}]`).join("");
    const name = sheets.entries.find((entry) => entry.owner === first.name && entry.path.length === 0 && entry.key === "name" && entry.kind === "text")?.value;
    return {
      ...explain(
        "name-as-position",
        "A list takes a position",
        position >= 0
          ? `\`${first.name}\` is a whole sheet. A list takes its position: ${name ?? `\`${first.name}\``} is at position ${position}, \`${chain.base}[${position}]${rest}\`. Positions count from 0.`
          : `\`${first.name}\` is a whole sheet. A list takes a position number in \`[ ]\`, like \`${chain.base}[0]${rest}\`. Positions count from 0.`,
        raw,
      ),
      slip: "a whole sheet where a list needs a position",
    };
  }
  return null;
}

/**
 * "list indices must be integers or slices, not tuple" on a list of sheets (`roster[3, "name"]`): the position and the
 * key in one pair of brackets. Each goes in its own, position first (never Unit 4's run of items, `[3:"name"]`).
 */
function explainPositionAndKey(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/indices must be integers or slices, not tuple/.test(message)) return null;
  const sheets = sheetsOf(code, context);
  const body = codePart(text);
  const mask = maskStrings(body);
  for (const found of mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)\s*\[/g)) {
    const name = found[1];
    const items = sheets.lists.get(name);
    const open = (found.index ?? 0) + found[0].length - 1;
    const close = matchingBracket(mask, open);
    const parts = close < 0 ? null : splitTopLevel(body.slice(open + 1, close));
    if (!items || !parts || parts.parts.length < 2 || parts.marks.some((mark) => mark !== ",")) continue;
    const [first, ...keys] = parts.parts;
    if (!/^-?\d+$|^[A-Za-z_]\w*$/.test(first) || !keys.every((key) => /^(["']).*\1$/.test(key))) continue;
    const read = `${name}[${first}]${keys.map((key) => `[${key}]`).join("")}`;
    const fixed = `${body.slice(0, found.index ?? 0)}${read}${body.slice(close + 1)}`.trim();
    return {
      ...explain(
        "comma-in-brackets",
        "Position, then key",
        `\`${name}\` is a list of sheets. Position first, then the key, each in its own square brackets: \`${fixed}\``,
        raw,
      ),
      slip: "a position and a key in one [ ]",
    };
  }
  return null;
}

/** "unhashable type: 'dict'" (`spell in book`, `book[spell] = spell_name`): a whole sheet where its name goes. */
function explainWholeSheetKey(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/unhashable type: 'dict'/.test(message)) return null;
  const body = codePart(text);
  const mask = maskStrings(body);
  const asked = mask.match(/(?<![\w.])([A-Za-z_]\w*)\s+(not\s+in|in)\s+([A-Za-z_]\w*(?:\s*\[[^\]]*\])*)/);
  const texts = (code ?? "").split("\n").map((row) => codePart(row).match(/^\s*([A-Za-z_]\w*)\s*=(?!=)\s*["']/)?.[1]).filter((name): name is string => Boolean(name));
  if (asked) {
    const [, whole, op] = asked;
    const from = (asked.index ?? 0) + asked[0].lastIndexOf(asked[3]);
    const book = body.slice(from, from + asked[3].length).trim();
    const name = texts.find((entry) => entry.includes(whole) && /name/.test(entry)) ?? texts.find((entry) => /name/.test(entry));
    return explain(
      "whole-sheet-as-key",
      "in asks about a key",
      `\`${op.replace(/\s+/, " ")}\` asks about a key, like the spell's name. \`${whole}\` is a whole dictionary${name ? `: ask \`${name} ${op.replace(/\s+/, " ")} ${book}\`` : ", so ask about its name instead"}.`,
      raw,
    );
  }
  const stored = body.match(/^\s*([A-Za-z_]\w*)\s*\[\s*([A-Za-z_]\w*)\s*\]\s*=(?!=)\s*([A-Za-z_]\w*)\s*$/);
  if (stored) {
    const [, book, whole, other] = stored;
    return explain(
      "whole-sheet-as-key",
      "A key is a name",
      `${lineWord(line)} uses \`${whole}\`, a whole dictionary, as the key. A key is text, like a name. Swap them: \`${book}[${other}] = ${whole}\``,
      raw,
    );
  }
  const read = readChains(text).flatMap((chain) => chain.reads).find((entry) => entry.name);
  return explain(
    "whole-sheet-as-key",
    "A key is a name",
    `${lineWord(line)} uses a whole dictionary${read?.name ? `, \`${read.name}\`,` : ""} as a key. A key is text, like a name.`,
    raw,
  );
}

/**
 * A sheet named whole on the crash line (`caster`, `spell`), not read with a key, and right where it was made (the
 * setup's sheet, a sheet the code writes with `{ }`, or a card read by a line Mar'tu's version has too), with the read
 * that fits: the one Mar'tu's version has in the same place, else a number key that shares a word with the line.
 */
function wholeSheetOnLine(sheets: Sheets, code: string, text: string, line: number | null, context?: ExplainContext): { name: string; read: string } | null {
  const body = codePart(text);
  const mask = maskStrings(body);
  const rows = (code ?? "").split("\n");
  const solution = (context?.solution ?? "").split("\n").map((row) => codePart(row).trim());
  for (const found of mask.matchAll(/(?<![\w.])([A-Za-z_]\w*)(?![\w(])(?!\s*[[.(])/g)) {
    const name = found[1];
    if (KEYWORDS.has(name) || !sheets.names.has(name)) continue;
    // The line that made it, in the student's code: a card read there that Mar'tu's version does not have is the
    // slip (`skill = caster["abilities"]`), and the older row names that line.
    let made: string | null = null;
    for (let at = (line ?? 1) - 2; at >= 0; at -= 1) {
      const row = codePart(rows[at]).match(new RegExp(`^\\s*${escapeRegExp(name)}\\s*=(?!=)\\s*(.+)$`));
      if (row) {
        made = codePart(rows[at]).trim();
        break;
      }
    }
    if (made !== null && /\[/.test(made) && !solution.includes(made)) continue;
    const at = found.index ?? 0;
    // Mar'tu's version of this line: the same line with a read of `name` where the student has the bare name.
    let read: string | null = null;
    for (const row of solution) {
      for (const chain of readChains(row).filter((entry) => entry.base === name)) {
        if (`${row.slice(0, chain.start)}${name}${row.slice(chain.end)}` === body.trim()) read = row.slice(chain.start, chain.end);
      }
      if (read) break;
    }
    if (!read) {
      const numbers = entriesFor(sheets, name).filter((entry) => entry.kind === "number" && entry.owner === name);
      const words = (value: string) => value.toLowerCase().split(/[^a-z]+/).filter((part) => part.length > 3);
      const others = words(`${body.slice(0, at)} ${body.slice(at + name.length)}`);
      const pick = numbers.find((entry) => words(entry.key).some((part) => others.some((word) => word.includes(part) || part.includes(word)))) ??
        numbers.find((entry) => entry.path.length === 0) ?? numbers[0];
      if (!pick) continue;
      read = chainCode(name, [...pick.path, pick.key]);
    }
    return { name, read };
  }
  return null;
}

/**
 * "'<' not supported between instances of 'dict' and 'int'" (`skill = caster["abilities"]`, then `skill < needed`):
 * a whole card compared with a number. The inner key that fits the comparison comes from the program's own card.
 */
function explainWholeCardCompared(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const kinds = message.match(/'(?:<|>|<=|>=)' not supported between instances of '(\w+)' and '(\w+)'/);
  if (!kinds || !kinds.slice(1).includes("dict") || !kinds.slice(1).some((kind) => kind === "int" || kind === "float")) return null;
  const sheets = sheetsOf(code, context);
  const rows = (code ?? "").split("\n");
  // A whole sheet named on this line with no key (`caster < spell["mana_cost"]`): the key goes here, not on a line
  // above that is right as it is (the game's `caster`, or `spell = spell_book["Lantern Ward"]` from Mar'tu's version).
  const bare = wholeSheetOnLine(sheets, code, text, line, context);
  if (bare) {
    return explain(
      "whole-card-compared",
      "A whole card",
      `That compares a whole card with a number. \`${bare.name}\` is the whole sheet. Add the key, like \`${bare.read}\`.`,
      raw,
    );
  }
  // The card: a read on this line, or a variable this line compares that an earlier line filled with a read.
  const cards: { chain: Chain; row: number }[] = readChains(text).map((chain) => ({ chain, row: line ?? 0 }));
  for (const word of maskStrings(codePart(text)).match(/[A-Za-z_]\w*/g) ?? []) {
    for (let at = (line ?? 1) - 2; at >= 0; at -= 1) {
      const made = codePart(rows[at]).match(new RegExp(`^\\s*${escapeRegExp(word)}\\s*=(?!=)\\s*(.+)$`));
      if (!made) continue;
      const chain = readChains(made[1])[0];
      if (chain) cards.push({ chain, row: at + 1 });
      break;
    }
  }
  const words = (value: string) => value.toLowerCase().split(/[^a-z]+/).filter((part) => part.length > 3);
  const other = words(codePart(text));
  for (const { chain, row } of cards) {
    const keys = keysBefore(chain, chain.reads.length);
    const inner = entriesFor(sheets, chain.base).filter((entry) => samePath(entry.path, keys)).map((entry) => entry.key);
    if (keys.length === 0 || inner.length === 0) continue;
    const read = chainCode(chain.base, keys);
    // Mar'tu's version reads the card with one more key: that key, else one that shares a word with the comparison.
    const solved = readChains(context?.solution ?? "").find((entry) => entry.base === chain.base && samePath(keysBefore(entry, keys.length), keys) && entry.reads[keys.length]?.key !== undefined);
    const pick = solved?.reads[keys.length]?.key ??
      inner.find((key) => words(key).some((part) => other.some((word) => word.includes(part) || part.includes(word)))) ?? inner[0];
    const where = row !== line ? ` Line ${row} reads \`${read}\`, the whole card.` : "";
    const found = explain(
      "whole-card-compared",
      "A whole card",
      `That compares a whole card with a number.${where} Add the inner key, like \`${read}["${pick}"]\`.`,
      raw,
    );
    // The card was read on a line above (`skill = caster["abilities"]`): that line is the slip, not the comparison.
    return row !== line ? { ...found, slip: "a whole card read where one value is meant", slipLine: row } : found;
  }
  return explain(
    "whole-card-compared",
    "A whole card",
    "That compares a whole card (a dictionary) with a number. Read one value from it first, with its key in square brackets.",
    raw,
  );
}

/** "unsupported operand type(s) for -: 'NoneType' and 'int'": math with `None`, often from a recipe with no `return`. */
function explainNoneMath(message: string, code: string, raw: string): CourseExplanation | null {
  if (!/unsupported operand type\(s\) for [^:]+: ('NoneType' and '\w+'|'\w+' and 'NoneType')/.test(message)) return null;
  const silent = recipeBlocks(code).filter((block) => {
    const steps = (code ?? "").split("\n").slice(block.start, block.end).map((row) => codePart(row).trim());
    return !steps.some((step) => /^return\b/.test(step));
  });
  return explain(
    "math-with-none",
    "Math with None",
    silent.length === 1
      ? `Something handed back \`None\`: nothing came back. \`${silent[0].recipe}\`, made on line ${silent[0].start}, has no \`return\`, so it hands back \`None\`. Give it a \`return\` with its answer.`
      : "Something handed back `None`: nothing came back. Does your recipe have a `return`?",
    raw,
  );
}

/**
 * The one other card that has `key` (`spell_book["Lantern Ward"]` for `"mana_cost"`), read through the shortest way
 * the program has to it (`spell`, when `spell = spell_book["Lantern Ward"]`), or null when no card or several do.
 */
function keyOnAnotherCard(chain: Chain, key: string, sheets: Sheets): { holder: string; read: string } | null {
  const own = new Set(entriesFor(sheets, chain.base));
  const found = sheets.entries.filter((entry) => entry.key === key && entry.owner !== null && entry.owner !== chain.base && !own.has(entry));
  const cards = new Set(found.map((entry) => JSON.stringify(entry.from ?? { owner: entry.owner, path: entry.path })));
  if (cards.size !== 1) return null;
  const best = [...found].sort((a, b) => a.path.length - b.path.length)[0];
  const holder = chainCode(best.owner as string, best.path);
  return { holder, read: chainCode(holder, [key]) };
}

/**
 * KeyError for a key the sheet does not have at all (no level, no near spelling), from the program's own sheet:
 * `gearshift["fuel"] == "starlode"` on a line of its own (a question, where one `=` stores the key), a key read to
 * test whether it is there (`if spell_book["Fire Bolt"]:`, where `in` asks), and a key no line makes (the sheet's
 * own keys, and `.get()` when Mar'tu's version reads it gently). A sheet the explainer cannot see keeps the older words.
 */
function explainKeyNotThere(
  chain: Chain,
  index: number,
  key: string,
  level: readonly string[],
  sheets: Sheets,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation | null {
  const known = sheets.entries.some((entry) => entry.owner === chain.base) || sheets.names.has(chain.base) || sheets.lists.has(chain.base);
  if (!known || level.length === 0) return null;
  const body = codePart(text);
  const statement = body.trim();
  const read = body.slice(chain.start, chain.end).trim();
  const positions = chain.reads.slice(0, index).filter((entry) => entry.key === undefined).map((entry) => entry.text);
  const holder = chainCode(`${chain.base}${positions.map((position) => `[${position}]`).join("")}`, keysBefore(chain, index));
  // (g) `gearshift["fuel"] == "starlode"` alone on its line: `==` asks, and the asking reads a key that is not there.
  const asked = statement.match(/^(.+?)\s*==\s*(.+)$/);
  if (asked && asked[1].trim() === read && !/^(if|elif|while|print|return|assert)\b/.test(statement)) {
    const value = asked[2].trim();
    return {
      ...explain(
        "comparison-alone",
        "One = stores",
        `${lineWord(line)} asks a question with \`==\`: is \`${read}\` the same as \`${value}\`? The sheet has no key \`"${key}"\` yet, so asking stops the program. One \`=\` stores it: \`${read} = ${value}\``,
        raw,
      ),
      slip: "`==` where one `=` stores a key",
    };
  }
  // The key is on another card the program has, and only one (`caster["mana_cost"]`, where the cost is on the
  // spell's page): read it there. Before (h), which would turn the cost test into a test of whether a key is there.
  const elsewhere = keyOnAnotherCard(chain, key, sheets);
  if (elsewhere) {
    return {
      ...explain(
        "missing-key",
        "Another sheet's key",
        `\`${holder}\` has no key \`"${key}"\`. That key is on \`${elsewhere.holder}\`: \`${elsewhere.read}\``,
        raw,
      ),
      slip: "a key read from the wrong sheet",
    };
  }
  // (h) `if spell_book["Fire Bolt"]:` reads the key to test it: `in` asks whether a key is there, with no read. Only
  // when Mar'tu's version asks about that key with `in` or `not in`: a cost or a level read in a test is a value.
  const test = statement.match(/^(if|elif|while)\s+(.+?)\s*:?$/);
  const asks = new RegExp(`(["'])${escapeRegExp(key)}\\1\\s+(not\\s+)?in\\b`).test(context?.solution ?? "");
  if (test && test[2].includes(read) && asks) {
    const quote = new RegExp(`(["'])${escapeRegExp(key)}\\1\\s+not\\s+in\\b`).test(context?.solution ?? "") ? "not in" : "in";
    return {
      ...explain(
        "missing-key",
        "Ask with in",
        `${lineWord(line)} reads the key \`"${key}"\` to test it, and \`${holder}\` has no key spelled that, so the read stops the program. To ask whether a key is there, use \`${quote}\`: \`"${key}" ${quote} ${holder}\``,
        raw,
      ),
      slip: "a key read to test whether it is there",
    };
  }
  // (i) a key no line makes: the sheet's own keys, and `.get()` when Mar'tu's version reads this key gently.
  const shown = level.length <= 5 ? level.map((entry) => `\`"${entry}"\``) : null;
  const keys = shown ? (shown.length === 1 ? shown[0] : `${shown.slice(0, -1).join(", ")} and ${shown.at(-1)}`) : null;
  const has = keys ? `\`${holder}\` has the key${shown && shown.length > 1 ? "s" : ""} ${keys}, and no \`"${key}"\`` : `\`${holder}\` has no key \`"${key}"\``;
  const gentle = (context?.solution ?? "").match(new RegExp(`${escapeRegExp(holder)}\\.get\\(\\s*(["'])${escapeRegExp(key)}\\1[^)]*\\)`))?.[0];
  return {
    ...explain(
      "missing-key",
      "A key the sheet does not have",
      gentle
        ? `${has}, so the read stops the program. To read a key that may be missing, use \`.get()\`: \`${gentle}\``
        : `${has}, so the read stops the program. Read a key the sheet has, or store this one first.`,
      raw,
    ),
    slip: "a key the sheet does not have",
  };
}

/**
 * KeyError, in the unit's words (Unit 5), from the program's own sheets: a skipped level (`caster["magical_affinity"]`
 * when it sits inside `"abilities"`), the keys the other way round, one level too deep (`caster["abilities"]["mana"]`),
 * a near miss on capitals or a space (`"Max_Mana"`), a position on a sheet (`KeyError: 0`), and two keys in one pair
 * of brackets (`["abilities", "wisdom"]`). Anything else keeps the older words.
 */
function explainKeyError(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const sheets = sheetsOf(code, context, line);
  const shown = message.trim();
  const chains = readChains(text);
  const quoted = shown.match(/^(['"])(.*)\1$/);
  // (e) `bomb_shell["abilities", "wisdom"]` or `lucky["glug", 0]`: a comma inside one pair of square brackets.
  if (/^\(.*,.*\)$/.test(shown)) {
    for (const chain of chains) {
      const read = chain.reads.find((entry) => splitTopLevel(entry.text)?.marks.includes(","));
      if (!read) continue;
      const parts = splitTopLevel(read.text)?.parts ?? [];
      const prefix = codePart(text).slice(chain.start, read.at).trim();
      const slip = "a comma inside [ ] where one key goes";
      if (parts.length === 2 && !/^["']/.test(parts[1])) {
        return {
          ...explain("comma-in-brackets", "One key per [ ]", `Inside [ ], a comma asks for two keys at once. To give back ${parts[1]} when the key is missing, use \`.get()\`: \`${prefix}.get(${parts[0]}, ${parts[1]})\``, raw),
          slip,
        };
      }
      return {
        ...explain("comma-in-brackets", "One key per [ ]", `Inside [ ], a comma asks for two keys at once. One key per pair of square brackets: \`${prefix}${parts.map((part) => `[${part}]`).join("")}\``, raw),
        slip,
      };
    }
    return null;
  }
  // (d) `KeyError: 0`: a sheet read by position.
  if (/^-?\d+$/.test(shown)) {
    const chain = chains.find((entry) => entry.reads.some((read) => read.position === Number(shown)));
    const index = chain ? chain.reads.findIndex((read) => read.position === Number(shown)) : -1;
    const keys = chain ? entriesFor(sheets, chain.base).filter((entry) => samePath(entry.path, keysBefore(chain, index))).map((entry) => entry.key) : [];
    const like = keys.includes("name") ? "name" : (keys[0] ?? "name");
    return {
      ...explain("missing-key", "Keys, not positions", `${lineWord(line)} reads position ${shown} of a dictionary. A dictionary has keys, not positions: use a key like \`"${like}"\`.`, raw),
      slip: "a position where a sheet needs a key",
    };
  }
  if (!quoted) return null;
  const key = quoted[2];
  for (const chain of chains) {
    const index = chain.reads.findIndex((read) => read.key === key);
    if (index < 0) continue;
    const own = entriesFor(sheets, chain.base);
    const walked = keysBefore(chain, index);
    const positions = chain.reads.slice(0, index).filter((read) => read.key === undefined).map((read) => read.text);
    const head = `${chain.base}${positions.map((position) => `[${position}]`).join("")}`;
    const here = own.filter((entry) => entry.key === key);
    // A read of this key that is right where the sheet keeps it is not the slip: another read on the line is.
    if (here.some((entry) => samePath(entry.path, walked))) continue;
    // `spell["Lantern Ward"]["mana_cost"]`, where `spell = spell_book["Lantern Ward"]`: the variable already holds that
    // page, so the page's own key goes.
    const page = own.find((entry) => entry.from && entry.path.length === 0)?.from?.path;
    if (page && page.at(-1) === key && walked.length === 0 && index === 0 && chain.reads.length > 1) {
      const body = codePart(text);
      const rest = chain.reads.slice(1).map((read) => `[${read.text}]`).join("");
      const fixed = `${body.slice(0, chain.start)}${chain.base}${rest}${body.slice(chain.end)}`.trim();
      return {
        ...explain(
          "missing-key",
          "One key too many",
          `\`${chain.base}\` already holds the \`"${key}"\` page, so it has no key \`"${key}"\` of its own. Read the page's key straight from \`${chain.base}\`: \`${fixed}\``,
          raw,
        ),
        slip: "a key the variable already stands for",
      };
    }
    // (a) the key sits deeper, inside a card the read skipped (or the keys are the other way round).
    const deeper = here.find((entry) => entry.path.length > walked.length && samePath(entry.path.slice(0, walked.length), walked));
    if (deeper) {
      const skipped = deeper.path.slice(walked.length);
      const nextKey = chain.reads[index + 1]?.key;
      if (nextKey !== undefined && skipped.length === 1 && nextKey === skipped[0]) {
        return {
          ...explain("missing-key", "Outer key first", `\`"${key}"\` is inside \`"${skipped[0]}"\`: the outer key comes first: \`${chainCode(head, [...walked, skipped[0], key])}\``, raw),
          slip: "the keys the wrong way around",
        };
      }
      return {
        ...explain("missing-key", "A level skipped", `\`"${key}"\` is inside \`"${skipped.join('"]["')}"\`: read the outer key first: \`${chainCode(head, [...deeper.path, key])}\``, raw),
        slip: "a skipped level",
      };
    }
    // (b) one level too deep: the key is on a sheet above the card the read went into.
    const higher = here.find((entry) => entry.path.length < walked.length && samePath(walked.slice(0, entry.path.length), entry.path));
    if (higher) {
      const into = walked[walked.length - 1];
      return {
        ...explain(
          "missing-key",
          "One level too deep",
          `\`"${key}"\` is on the ${higher.path.length === 0 ? "big sheet" : `\`"${higher.path.at(-1)}"\` card`}, not inside \`"${into}"\`: \`${chainCode(head, [...higher.path, key])}\``,
          raw,
        ),
        slip: "a read one level too deep",
      };
    }
    // (c) a near miss: the sheet spells it another way.
    const level = own.filter((entry) => samePath(entry.path, walked)).map((entry) => entry.key);
    const near = nearKey(key, level.length > 0 ? level : own.map((entry) => entry.key));
    if (near) {
      return {
        ...explain("missing-key", "Spell the key exactly", `${lineWord(line)} reads the key \`"${key}"\`. The sheet spells it \`"${near}"\`. Keys match letter for letter.`, raw),
        slip: "a key spelled another way",
      };
    }
    // (f) `spell_book["spell_name"]`: a variable's name in quotes is only those letters (the unit's quotes rule).
    if (/^[A-Za-z_]\w*$/.test(key) && definedNames(code).some((entry) => entry.name === key)) {
      const written = codePart(text).slice(chain.start, chain.end);
      const read = chain.reads[index];
      // `gearshift["fire_bolt_cost"]`, where `fire_bolt_cost = 6`: the variable holds a number, never a key, so the
      // read goes and the variable stands on its own (`gearshift[fire_bolt_cost]` would read key 6).
      if (index === chain.reads.length - 1 && variableHoldsNumber(code, key, line)) {
        const body = codePart(text);
        const fixed = `${body.slice(0, chain.start)}${key}${body.slice(chain.end)}`.trim();
        return {
          ...explain(
            "missing-key",
            "Its own variable",
            `\`"${key}"\` in quotes is a key, and the sheet has no key spelled that. \`${key}\` is its own variable, not a key on the sheet: \`${fixed}\``,
            raw,
          ),
          slip: "a variable read as a key of the sheet",
        };
      }
      const fixed = written.replace(`[${read.text}]`, `[${key}]`);
      return explain(
        "quoted-name",
        "Quotes mean these letters",
        `\`"${key}"\` in quotes means those exact letters, and the sheet has no key spelled that. Without quotes, Python looks inside the box \`${key}\`: \`${fixed}\``,
        raw,
      );
    }
    const missing = explainKeyNotThere(chain, index, key, [...new Set(level)], sheets, text, line, raw, context);
    if (missing) return missing;
    return null;
  }
  // A key kept in a variable (`spell_book[spell_name]`): the variable's text, against the sheet's own keys.
  const near = nearKey(key, sheets.entries.map((entry) => entry.key));
  if (near) {
    return {
      ...explain("missing-key", "Spell the key exactly", `${lineWord(line)} looks for the key \`"${key}"\`. The sheet spells it \`"${near}"\`. Keys match letter for letter.`, raw),
      slip: "a key spelled another way",
    };
  }
  return null;
}

/**
 * Math with a variable's name in quotes (Unit 5): `oogrish["mana"] - "ward_cost"` takes text away from a number. The
 * quotes rule, in the unit's words: quotes mean these exact letters; without them Python looks inside the box.
 */
function explainQuotedBoxInMath(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/unsupported operand type\(s\) for [-*/%]+: '\w+' and 'str'|unsupported operand type\(s\) for [-*/%]+: 'str' and '\w+'/.test(message)) return null;
  const body = codePart(text);
  const defined = new Set(definedNames(code).map((entry) => entry.name));
  for (const found of body.matchAll(/(["'])([A-Za-z_]\w*)\1/g)) {
    const name = found[2];
    if (!defined.has(name)) continue;
    const before = body.slice(0, found.index ?? 0).trimEnd();
    const after = body.slice((found.index ?? 0) + found[0].length).trimStart();
    if (!/[-*/%+]$/.test(before) && !/^[-*/%+]/.test(after)) continue;
    const fixed = `${body.slice(0, found.index ?? 0)}${name}${body.slice((found.index ?? 0) + found[0].length)}`.trim();
    return explain(
      "quoted-name",
      "Quotes mean these letters",
      `\`${found[0]}\` in quotes means those exact letters: text, not the number in \`${name}\`. Without quotes, Python looks inside the box: \`${fixed}\``,
      raw,
    );
  }
  return null;
}

/**
 * IndexError on a list of sheets (Unit 5): `roster[4]["name"]` when the roster holds 4 sheets. The list's own count
 * and its last sheet, by name, never Unit 4's "list of lists" words (the key after the position is not a second one).
 * A list the program changes later (`.append()`, `.pop()`) keeps the count out.
 */
function explainSheetsOutOfRange(code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const sheets = sheetsOf(code, context);
  const program = maskStrings(`${context?.setup ?? ""}\n${code ?? ""}`);
  for (const chain of readChains(text)) {
    const first = chain.reads[0];
    if (first?.position === undefined) continue;
    const items = sheets.lists.get(chain.base) ?? [];
    const nameOf = (item: { ref?: string; name?: string }) =>
      item.name ?? sheets.entries.find((entry) => entry.owner === item.ref && entry.path.length === 0 && entry.key === "name" && entry.kind === "text")?.value;
    const ofSheets = items.length > 0 && items.every((item) => item.name !== undefined || (item.ref !== undefined && sheets.names.has(item.ref)));
    if (!ofSheets && chain.reads[1]?.key === undefined) continue;
    const changed = new RegExp(`(?<![\\w.])${escapeRegExp(chain.base)}\\s*\\.\\s*(append|insert|pop|remove|extend)\\s*\\(`).test(program);
    if (!ofSheets || changed) {
      return explain(
        "nothing-at-position",
        "Nothing at that position",
        `${lineWord(line)} asks for a position \`${chain.base}\` doesn't have. \`${chain.base}\` is a list of sheets: positions count from 0, so the last one is one less than the number of sheets. \`[-1]\` is always the last one.`,
        raw,
      );
    }
    const last = nameOf(items[items.length - 1]);
    return explain(
      "nothing-at-position",
      "Nothing at that position",
      `${lineWord(line)} asks for position ${first.position} of \`${chain.base}\`, and \`${chain.base}\` holds ${items.length} sheet${items.length === 1 ? "" : "s"}. Positions count from 0, so its positions are ${items.length === 1 ? "only 0" : items.length === 2 ? "0 and 1" : `0 to ${items.length - 1}`}.${last ? ` The last one, ${last}, is \`${chain.base}[${items.length - 1}]\`.` : ""}`,
      raw,
    );
  }
  return null;
}

/** `str()` for a number read from a sheet: the line's own read (`str(gearshift["mana"])`), never `str(gearshift)`. */
function sheetNumberRead(code: string, text: string, context?: ExplainContext): string | null {
  const sheets = sheetsOf(code, context);
  const body = codePart(text);
  const chains = readChains(text).filter((chain) => !/str\s*\(\s*$/.test(maskStrings(body).slice(0, chain.start)));
  const number = chains.find((chain) => {
    const keys = keysBefore(chain, chain.reads.length);
    const last = keys.at(-1);
    return last !== undefined && entriesFor(sheets, chain.base).some((entry) => entry.key === last && samePath(entry.path, keys.slice(0, -1)) && entry.kind === "number");
  });
  const pick = number ?? chains.find((chain) => /\+\s*$/.test(maskStrings(body).slice(0, chain.start)));
  return pick ? body.slice(pick.start, pick.end) : null;
}

/* ---------------------------------------------------------------------------------------------- */
/* Loops (Unit 6)                                                                                  */
/* ---------------------------------------------------------------------------------------------- */

/** One `for` line of the program: its loop variable (or names, `name, cost`), what it walks, and its line. */
type ForLoop = { variable: string; iterable: string; line: number; indent: number };

const FOR_HEADER = /^(\s*)for\s+([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s+in\s+(.+?)\s*:\s*$/;

/** The `for` lines whose body holds `line`, innermost first (by indent, as Python reads a block). */
function enclosingLoops(code: string, line: number | null): ForLoop[] {
  if (line === null) return [];
  const rows = (code ?? "").split("\n");
  const here = rows[line - 1];
  if (here === undefined) return [];
  let indent = codePart(here).trim() ? indentOf(here) : Number.POSITIVE_INFINITY;
  const loops: ForLoop[] = [];
  for (let at = line - 2; at >= 0 && indent > 0; at -= 1) {
    const row = codePart(rows[at] ?? "");
    if (!row.trim() || indentOf(row) >= indent) continue;
    indent = indentOf(row);
    const header = row.match(FOR_HEADER);
    if (header) loops.push({ variable: header[2].replace(/\s+/g, ""), iterable: header[3].trim(), line: at + 1, indent });
  }
  return loops;
}

/** The loop whose body holds `line` and walks the list `name` (`for member in roster:`), innermost first. */
function loopOver(code: string, line: number | null, name: string): ForLoop | null {
  return enclosingLoops(code, line).find((loop) => loop.iterable === name && /^[A-Za-z_]\w*$/.test(loop.variable)) ?? null;
}

/**
 * Unit 6: `for gap in "chalk_wall":` with a variable `chalk_wall` in the program (the setup's too). The loop walks the
 * letters of that text, so the crash comes later, on a line that is right (`'<' not supported between instances of
 * 'str' and 'int'`, `string indices must be integers`). The quotes are the slip: the quotes rule, and the `for` line
 * without them. Only when the line Python stopped on is that `for` line or inside its body.
 */
function explainQuotedLoop(code: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (line === null) return null;
  const rows = (code ?? "").split("\n");
  const program = `${context?.setup ?? ""}\n${code ?? ""}`;
  const made = new Set(definedNames(program).map((entry) => entry.name));
  const loops = [{ variable: "", iterable: "", line, indent: 0 }, ...enclosingLoops(code, line)]
    .map((loop) => ({ loop, header: codePart(rows[loop.line - 1] ?? "").match(FOR_HEADER) }))
    .filter(({ header }) => header !== null);
  for (const { loop, header } of loops) {
    const quoted = header?.[3].trim().match(/^(["'])([A-Za-z_]\w*)\1$/);
    if (!header || !quoted || !made.has(quoted[2])) continue;
    const name = quoted[2];
    const shape = new RegExp(`^\\s*${escapeRegExp(name)}\\s*=(?!=)\\s*([[{])`, "m").exec(program)?.[1];
    const inside = shape === "[" ? "inside the list" : shape === "{" ? "inside the dictionary" : "inside the box with this label";
    const fixed = codePart(rows[loop.line - 1] ?? "").trim().replace(quoted[0], name);
    return {
      ...explain(
        "quoted-name",
        "Quotes around a list's name",
        `Line ${loop.line} has \`${name}\` in quotes, so the loop walks its letters, one at a time. Take the quotes off \`${name}\`: no quotes means look ${inside}. Line ${loop.line} with no quotes: \`${fixed}\``,
        raw,
      ),
      slip: "a list's name in quotes in a `for` line",
      slipLine: loop.line,
    };
  }
  return null;
}

/**
 * Unit 6: "list indices must be integers or slices, not str" inside a loop over that list (`roster["name"]` under
 * `for member in roster:`): the list asked for a key. Its sheets are read through the loop variable.
 */
function explainLoopListKey(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/indices must be integers or slices, not str/.test(message)) return null;
  for (const chain of readChains(text)) {
    const first = chain.reads[0];
    const loop = first?.key !== undefined ? loopOver(code, line, chain.base) : null;
    if (!loop) continue;
    const read = codePart(text).slice(chain.start, chain.end);
    const lean = `${lineWord(line)} asks a list for a tag (key), like \`${read}\`. A list has positions, not tags.`;
    return {
      ...explain(
        "name-as-position",
        "A list has no tags (keys)",
        `${lean} Read one sheet through the loop variable: \`${chainCode(loop.variable, keysBefore(chain, chain.reads.length))}\`.`,
        raw,
      ),
      slip: "a tag (key) asked of a whole list",
      lean,
    };
  }
  return null;
}

/**
 * Unit 6: "list indices must be integers or slices, not dict" with the loop variable as the position (`roster[member]`
 * under `for member in roster:`): `member` already holds one sheet, so it is read directly.
 */
function explainLoopSheetAsPosition(message: string, code: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/indices must be integers or slices, not dict/.test(message)) return null;
  for (const chain of readChains(text)) {
    const first = chain.reads[0];
    const loop = first?.name !== undefined ? loopOver(code, line, chain.base) : null;
    if (!loop || loop.variable !== first.name) continue;
    const lean = `${lineWord(line)} uses a whole sheet as a position, like \`${chain.base}[${first.name}]\`.`;
    const direct = `${first.name}${chain.reads.slice(1).map((read) => `[${read.text}]`).join("")}`;
    return {
      ...explain(
        "name-as-position",
        "A sheet, not a position",
        `${lean} A list's positions are numbers, and \`${first.name}\` already holds one sheet, so use it on its own: \`${direct}\`.`,
        raw,
      ),
      slip: "a whole sheet used as a position",
      lean,
    };
  }
  return null;
}

/** Unit 6: "'int' object is not iterable" on a `for` line (`for i in len(wall):`, `for i in 6:`): one number to walk. */
function explainLoopOverNumber(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/^'(int|float)' object is not iterable/.test(message)) return null;
  if (!/(^|[^\w.])for\s+[A-Za-z_][\w\s,]*\s+in\s/.test(maskStrings(codePart(text)))) return null;
  const words = `${lineWord(line)} gives a \`for\` loop one number to walk. A \`for\` loop needs a list or \`range(...)\`: one number has no items to walk through.`;
  return { ...explain("loop-over-number", "A loop over one number", words, raw), lean: words };
}

/**
 * Unit 6: "'builtin_function_or_method' object is not iterable" on a `for` line (`for name, cost in spell_book.items:`):
 * the tool named without its parentheses, so the loop gets the tool itself, not what it hands back.
 */
function explainLoopToolNotCalled(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/^'(builtin_function_or_method|method)' object is not iterable/.test(message)) return null;
  const header = codePart(text).match(FOR_HEADER);
  const tool = header?.[3].trim().match(/^([A-Za-z_]\w*)\s*\.\s*([A-Za-z_]\w*)$/);
  if (!header || !tool) return null;
  const fixed = codePart(text).trim().replace(header[3].trim(), `${tool[1]}.${tool[2]}()`);
  return {
    ...explain(
      "call-needs-round-brackets",
      "Parentheses for a call",
      `${lineWord(line)} hands the loop \`${tool[1]}.${tool[2]}\` with no parentheses ( ), so the loop gets the tool itself, not what it hands back. Add the parentheses to call it: \`${fixed}\``,
      raw,
    ),
    slip: "a tool named without its parentheses",
  };
}

/**
 * Unit 6: "too many values to unpack (expected 2)" on `for name, cost in spell_book:`: a loop over a dictionary hands over
 * one key a pass, so two names cannot share it. Each key with its value comes from `.items()`.
 */
function explainLoopNamesOverKeys(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/(too many|not enough) values to unpack/.test(message)) return null;
  const header = codePart(text).match(FOR_HEADER);
  const names = header?.[2].split(",").map((name) => name.trim()) ?? [];
  const book = header?.[3].trim();
  if (!header || names.length < 2 || !book || !/^[A-Za-z_]\w*$/.test(book) || !sheetsOf(code, context).names.has(book)) return null;
  const fixed = codePart(text).trim().replace(new RegExp(`\\bin\\s+${escapeRegExp(book)}\\s*:`), `in ${book}.items():`);
  return {
    ...explain(
      "wrong-number-of-values",
      "One tag each pass",
      `${lineWord(line)} gives the loop ${names.length} names, but a loop over \`${book}\` hands over one tag (key) each pass. To get each tag with its value, loop over \`${book}.items()\`: \`${fixed}\``,
      raw,
    ),
    slip: "two names for a loop that hands over one tag",
  };
}

/**
 * Unit 6: "unsupported operand type(s) for +: 'int' and 'dict'" (`total = total + member`): a whole sheet added, so one
 * value is read from it by its key (the one Mar'tu's version reads, else a number key of its sheets). And "... 'int'
 * and 'list'" (`total = total + values` inside `for value in values:`): the whole list added, so the loop variable goes
 * there. Null when the line's right-hand name cannot be read (the older words stay).
 */
function explainWholeAdded(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const glued = /unsupported operand type\(s\) for \+: 'dict' and 'str'/.test(message);
  const kinds = glued ? [message, "dict"] : message.match(/unsupported operand type\(s\) for \+=?: '(?:int|float)' and '(dict|list)'/);
  if (!kinds) return null;
  const mask = maskStrings(codePart(text));
  const name = glued
    ? mask.match(/(?<![\w.\]])([A-Za-z_]\w*)\s*\+/)?.[1]
    : mask.match(/\+=?\s*([A-Za-z_]\w*)\b(?!\s*[[(.])/)?.[1];
  if (!name || KEYWORDS.has(name)) return null;
  if (kinds[1] === "list") {
    const loop = loopOver(code, line, name);
    return {
      ...explain(
        "row-not-item",
        "A whole list",
        `\`${name}\` is the whole list, and a whole list can't be added to a number. ${loop ? `Add the loop variable, \`${loop.variable}\`, instead.` : "Add one item from it instead."}`,
        raw,
      ),
      slip: "a whole list added where one item is meant",
    };
  }
  // The sheet's number keys: from the list the loop walks, else from the sheet itself.
  const sheets = sheetsOf(code, context);
  const walked = enclosingLoops(code, line).find((loop) => loop.variable === name)?.iterable;
  const owner = walked && /^[A-Za-z_]\w*$/.test(walked) ? walked : name;
  const wanted = glued ? "text" : "number";
  const values = entriesFor(sheets, owner).filter((entry) => entry.kind === wanted && entry.path.length === 0 && (entry.owner === owner || sheets.lists.has(owner)));
  const solved = readChains(context?.solution ?? "").find((chain) => chain.base === name && chain.reads.length === 1 && chain.reads[0].key !== undefined && values.some((entry) => entry.key === chain.reads[0].key));
  const key = solved?.reads[0].key ?? values[0]?.key;
  const like = key ? `, like \`${name}["${key}"]\`` : "";
  if (!sheets.names.has(name) && !walked) return null;
  return {
    ...explain(
      "whole-card-compared",
      "A whole sheet",
      glued
        ? `\`${name}\` is a whole sheet, not text, so it can't be glued to text. Glue on one value from it by its tag (key)${like}.`
        : `\`${name}\` is a whole sheet, and a whole sheet can't be added to a number. Add one value from it by its tag (key)${like}.`,
      raw,
    ),
    slip: glued ? "a whole sheet glued to text" : "a whole sheet added where one value is meant",
  };
}

/** One loop a line sits in: a `for` or `while` line of the program, with its line and indent. */
type LoopHeader = { keyword: "for" | "while"; line: number; indent: number };

/** The `for` and `while` lines whose body holds `line`, innermost first (by indent, as Python reads a block). */
function enclosingLoopHeaders(code: string, line: number | null): LoopHeader[] {
  if (line === null) return [];
  const rows = (code ?? "").split("\n");
  const here = rows[line - 1];
  if (here === undefined) return [];
  let indent = codePart(here).trim() ? indentOf(here) : Number.POSITIVE_INFINITY;
  const loops: LoopHeader[] = [];
  for (let at = line - 2; at >= 0 && indent > 0; at -= 1) {
    const row = codePart(rows[at] ?? "");
    if (!row.trim() || indentOf(row) >= indent) continue;
    indent = indentOf(row);
    const keyword = row.match(/^\s*(for|while)\b/)?.[1] as "for" | "while" | undefined;
    if (keyword) loops.push({ keyword, line: at + 1, indent });
  }
  return loops;
}

/** The loops written on the line itself, in a one-line loop (`[h for h in chalk_wall if h < 45]`). */
function inlineLoops(text: string, line: number): ForLoop[] {
  const mask = maskStrings(codePart(text));
  const loops: ForLoop[] = [];
  for (const found of mask.matchAll(/(?<![\w.])for\s+([A-Za-z_]\w*)\s+in\s+/g)) {
    const from = (found.index ?? 0) + found[0].length;
    // What it walks: up to an `if`, another `for`, or the bracket that closes the one-line loop.
    let depth = 0;
    let end = from;
    for (; end < mask.length; end += 1) {
      const char = mask[end];
      if (char in CLOSER) depth += 1;
      else if (char in OPENER) {
        if (depth === 0) break;
        depth -= 1;
      } else if (depth === 0 && /^\s(if|for)\s/.test(mask.slice(end, end + 5))) break;
    }
    loops.push({ variable: found[1], iterable: codePart(text).slice(from, end).trim(), line, indent: indentOf(text) });
  }
  return loops;
}

/** The code with its strings masked line by line, after each line's `#` note is cut (an apostrophe in a note is not a quote). */
function maskedLines(code: string): string {
  return (code ?? "").split("\n").map((row) => maskStrings(codePart(row))).join("\n");
}

/** The first item of a list the code writes out on one line (`chalk_wall = [48, 48, 47]` gives `48`), else null. */
function firstItemOf(code: string, name: string): string | null {
  if (readableLength(code, name) === null) return null;
  const row = (code ?? "").split("\n").map((entry) => codePart(entry)).find((entry) => new RegExp(`^\\s*${escapeRegExp(name)}\\s*=(?!=)\\s*\\[`).test(maskStrings(entry)));
  const value = row?.slice(row.indexOf("[") + 1, row.lastIndexOf("]")) ?? "";
  const first = splitTopLevel(value.trim())?.parts[0]?.trim();
  return first && /^-?\d+(\.\d+)?$/.test(first) ? first : null;
}

/** `range(1, len(chalk_wall))`: the start (a number, 0 when left out) and the list whose `len()` is the end. */
function rangeOverLength(iterable: string): { start: number; list: string } | null {
  const found = iterable.trim().match(/^range\s*\(\s*(?:(-?\d+)\s*,\s*)?len\s*\(\s*([A-Za-z_]\w*)\s*\)\s*\)$/);
  return found ? { start: Number(found[1] ?? 0), list: found[2] } : null;
}

/** A position written as the loop variable plus or minus a number (`gap`, `gap - 1`, `i + 1`): the number, else null. */
function offsetFrom(read: string, variable: string): number | null {
  const found = read.trim().match(new RegExp(`^${escapeRegExp(variable)}(?:\\s*([-+])\\s*(\\d+))?$`));
  if (!found) return null;
  return found[1] ? Number(found[2]) * (found[1] === "-" ? -1 : 1) : 0;
}

/** `[i]`, `[i - 1]`, `[i + 2]`: a position written from the loop variable and a number. */
function offsetCode(variable: string, offset: number): string {
  return offset === 0 ? variable : `${variable} ${offset < 0 ? "-" : "+"} ${Math.abs(offset)}`;
}

/**
 * Unit 6: "list index out of range" inside a loop, the unit's own two slips.
 * (a) The loop variable of `for gap in chalk_wall:` used as a position in that list (`chalk_wall[gap]`,
 * `chalk_wall[gap - 1]`, `row[score]`): it already holds an item, not a position. When Mar'tu's version walks the
 * list itself, the item is used on its own; when it walks positions (`range(1, len(chalk_wall))`), the loop does too.
 * (b) `chalk_wall[i + 1]` inside `for i in range(...len(chalk_wall))` (or a one-line loop's): on the last pass `i` is
 * the last position, so `i + 1` is one past the end. Mar'tu's version looks back (`[i - 1]`, from 1), or stops one
 * early when it looks ahead. Null otherwise: Unit 4's words stay.
 */
function explainLoopIndex(code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (line === null) return null;
  const inline = inlineLoops(text, line);
  const loops = [...inline, ...enclosingLoops(code, line)].filter((loop) => /^[A-Za-z_]\w*$/.test(loop.variable));
  const body = codePart(text).trim();
  const solution = context?.solution ?? "";
  for (const chain of readChains(text)) {
    const read = chain.reads[0];
    if (!read) continue;
    // (a) The item used as a position: the loop walks this very list.
    const walker = loops.find((loop) => loop.iterable === chain.base && offsetFrom(read.text, loop.variable) !== null);
    if (walker) {
      const item = walker.variable;
      const shift = offsetFrom(read.text, item) ?? 0;
      const first = firstItemOf(code, chain.base);
      const lean = `${lineWord(line)} uses \`${item}\`, an item from \`${chain.base}\`, as a position.`;
      const holds = `${lineWord(line)} uses \`${item}\` as a position in \`${chain.base}\`. But \`${item}\` already holds an item, not a position${first ? `: on the first pass, it holds ${first}` : ""}.`;
      // Mar'tu's version walks positions of this list (`for i in range(1, len(chalk_wall)):`): so does the fix.
      const byPosition = solution
        .split("\n")
        .map((row) => codePart(row).trim())
        .find((row) => {
          const header = row.match(FOR_HEADER);
          return header !== null && rangeOverLength(header[3])?.list === chain.base;
        });
      const readsItself = !byPosition && (solution ? new RegExp(`(?<![\\w.])for\\s+[A-Za-z_]\\w*\\s+in\\s+${escapeRegExp(chain.base)}\\b`).test(maskedLines(solution)) : shift === 0);
      if (readsItself) {
        // `chalk_wall[gap]` becomes `gap` (a read after it, `[0]`, stays).
        const full = codePart(text);
        const firstEnd = matchingBracket(maskStrings(full), read.at) + 1;
        const fixed = `${full.slice(0, chain.start)}${item}${full.slice(firstEnd)}`.trim();
        return { ...explain("item-as-position", "An item, not a position", `${holds} Use \`${item}\` itself: \`${fixed}\``, raw), lean };
      }
      const header = byPosition ?? `for i in range(len(${chain.base})):`;
      return {
        ...explain("item-as-position", "An item, not a position", `${holds} To use positions, loop over them instead: \`${header}\``, raw),
        lean,
      };
    }
    // (b) One past the end: `[i + 1]` in a loop over `range(...len(list))`.
    const counter = loops.find((loop) => rangeOverLength(loop.iterable)?.list === chain.base && (offsetFrom(read.text, loop.variable) ?? 0) > 0);
    if (!counter) continue;
    const index = counter.variable;
    const ahead = offsetFrom(read.text, index) ?? 1;
    const range = rangeOverLength(counter.iterable) as { start: number; list: string };
    const count = readableLength(code, chain.base);
    const last = count !== null && count > 0 ? `${index}\` is ${count - 1}, so \`[${read.text}]\` asks for position ${count - 1 + ahead}, past the end.` : `${index}\` is the last position, so \`[${read.text}]\` is past the end.`;
    const lead = `${lineWord(line)} reads \`${chain.base}[${read.text}]\`, ${ahead === 1 ? "one position" : `${ahead} positions`} after \`${index}\`. On the last pass, \`${last}`;
    const lean = `${lineWord(line)} reads \`${chain.base}[${read.text}]\`: on the last pass, that is past the end.`;
    const masked = maskedLines(solution);
    const looksAhead = new RegExp(`${escapeRegExp(chain.base)}\\s*\\[\\s*[A-Za-z_]\\w*\\s*\\+\\s*\\d+\\s*\\]`).test(masked);
    if (looksAhead) {
      const stop = `range(${range.start ? `${range.start}, ` : ""}len(${chain.base}) - ${ahead})`;
      return { ...explain("one-past-the-end", "One past the end", `${lead} Stop the loop ${ahead === 1 ? "one" : ahead} early: \`${stop}\``, raw), lean };
    }
    // Look back: every read of this list on the line moves back one (`[i] - [i + 1]` becomes `[i - 1] - [i]`).
    let shifted = body;
    for (const each of readChains(body).filter((entry) => entry.base === chain.base).reverse()) {
      const by = offsetFrom(each.reads[0]?.text ?? "", index);
      if (by === null || each.reads.length !== 1) continue;
      shifted = `${shifted.slice(0, each.start)}${chain.base}[${offsetCode(index, by - 1)}]${shifted.slice(each.end)}`;
    }
    const sameLine = inline.includes(counter);
    if (range.start >= 1) {
      return { ...explain("one-past-the-end", "One past the end", `${lead} Look back one instead, with \`[${index} - 1]\`: \`${shifted}\``, raw), lean };
    }
    const from = `range(1, len(${chain.base}))`;
    if (sameLine) {
      const fixed = shifted.replace(counter.iterable, from);
      return { ...explain("one-past-the-end", "One past the end", `${lead} Look back with \`[${index} - 1]\` instead, and start the range at 1: \`${fixed}\``, raw), lean };
    }
    return {
      ...explain(
        "one-past-the-end",
        "One past the end",
        `${lead} Look back with \`[${index} - 1]\` instead, and start the range at 1: \`for ${index} in ${from}:\``,
        raw,
      ),
      lean,
    };
  }
  return null;
}

/**
 * Unit 6: a NameError for a name the loop changes from itself (`total = total + member["mana"]`, `days += 1`) when
 * nothing before the loop gave it a value: a running total needs its start above the loop (`total = 0`), never quotes.
 */
function explainNoStartingValue(name: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const body = maskStrings(codePart(text));
  const who = escapeRegExp(name);
  const grows = body.match(new RegExp(`^\\s*${who}\\s*([-+*/]|//)=`)) ?? body.match(new RegExp(`^\\s*${who}\\s*=(?!=)\\s*${who}\\s*([-+*/])`));
  const fromItself = grows ?? (new RegExp(`^\\s*${who}\\s*=(?!=)(.*)(?<![\\w.])${who}(?![\\w(])`).test(body) ? ["", ""] : null);
  if (!fromItself) return null;
  // A name a letter or two from one the code makes (`totl` for `total`) is a spelling slip, not a missing start.
  if (closeName(name, definedNames(code).map((entry) => entry.name).filter((entry) => entry !== name))) return null;
  const loops = enclosingLoopHeaders(code, line);
  if (loops.length === 0) return null;
  // Mar'tu's version gives it its start (`total = 0`) at the indent of the loop it goes above.
  const start = (context?.solution ?? "")
    .split("\n")
    .map((row) => codePart(row))
    .map((row) => row.match(new RegExp(`^(\\s*)${who}\\s*=(?!=)\\s*(.+?)\\s*$`)))
    .find((found): found is RegExpMatchArray => found !== null && !new RegExp(`(?<![\\w.])${who}(?![\\w])`).test(maskStrings(found[2])));
  const loop = (start ? loops.find((entry) => entry.indent === start[1].length) : undefined) ?? loops[0];
  const value = start && /^(-?\d+(\.\d+)?|""|''|\[\])$/.test(start[2]) ? start[2] : "0";
  const sign = fromItself[1];
  const verb = sign === "+" ? "adds to" : sign === "-" ? "takes away from" : "changes";
  const lean = `${lineWord(line)} ${verb} \`${name}\`, but \`${name}\` has no starting value before the loop.`;
  return {
    ...explain(
      "no-starting-value",
      "No starting value",
      `${lineWord(line)} ${verb} \`${name}\` on every pass, but nothing gives \`${name}\` a starting value before the loop. Above line ${loop.line}, where the loop starts, put \`${name} = ${value}\``,
      raw,
    ),
    lean,
    // The fix is a new line above the loop, not the line Python stopped at: the crash banner says "line 9 or a line
    // above it" (crashFixLine), as for a box no line makes yet.
    fixAbove: true,
  };
}

/**
 * Unit 6: a NameError for a tag (key) of the sheets the loop walks (`if mana < 10:` under `for member in roster:`):
 * the value is on each sheet, so it is read through the loop variable, `member["mana"]`. Never quotes.
 */
function explainTagAsName(name: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (closeName(name, definedNames(code).map((entry) => entry.name).filter((entry) => entry !== name))) return null;
  const sheets = sheetsOf(code, context);
  const loop = enclosingLoops(code, line).find((entry) => {
    if (!/^[A-Za-z_]\w*$/.test(entry.variable) || !sheets.lists.has(entry.iterable)) return false;
    return entriesFor(sheets, entry.iterable).some((key) => key.key === name && key.path.length === 0);
  });
  if (!loop) return null;
  const body = codePart(text).trim();
  const mask = maskStrings(body);
  const read = `${loop.variable}["${name}"]`;
  let fixed = body;
  for (const found of [...mask.matchAll(new RegExp(`(?<![\\w.\\[])${escapeRegExp(name)}(?![\\w(])(?!\\s*=(?!=))`, "g"))].reverse()) {
    const at = found.index ?? 0;
    fixed = `${fixed.slice(0, at)}${read}${fixed.slice(at + name.length)}`;
  }
  const lean = `${lineWord(line)} uses \`${name}\` as a name, but \`${name}\` is a tag (key) on each sheet.`;
  return {
    ...explain(
      "tag-as-name",
      "A tag on the sheet",
      `\`${name}\` is a tag (key) on each sheet in \`${loop.iterable}\`, not a name of its own. Read it through the loop variable, \`${read}\`: \`${fixed}\``,
      raw,
    ),
    lean,
  };
}

/**
 * Unit 6: a crash inside a recipe whose ingredient was handed the list the loop walks (`mana_bar(roster)` under
 * `for member in roster:`): the slip is on the call line, which hands over this pass's item, the loop variable.
 */
function explainListToRecipe(message: string, code: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  if (!/indices must be integers or slices, not|'list' object (is not|has no)|for [-+*/]: 'list'|'list' and '|can't multiply sequence by non-int of type 'list'/.test(message)) return null;
  if (line === null) return null;
  const block = recipeBlocks(code).find((entry) => line > entry.start && line <= entry.end);
  if (!block) return null;
  const frames = [...raw.matchAll(/File "main\.py", line (\d+)/g)].map((frame) => Number(frame[1]));
  const callLine = frames.length >= 2 ? frames[frames.length - 2] : null;
  if (callLine === null) return null;
  const callText = codePart(sourceLine(code, callLine));
  const ingredients = recipeIngredients(code, block.recipe) ?? [];
  const mask = maskStrings(callText);
  for (const call of mask.matchAll(new RegExp(`(?<![\\w.])${escapeRegExp(block.recipe)}\\s*\\(`, "g"))) {
    const open = (call.index ?? 0) + call[0].length - 1;
    const close = matchingBracket(mask, open);
    if (close < 0) continue;
    const handed = splitArguments(callText.slice(open + 1, close)) ?? [];
    for (const [at, value] of handed.entries()) {
      const loop = loopOver(code, callLine, value.trim());
      if (!loop || !ingredients[at]) continue;
      const sheets = loopSheetNames(code, context).includes(loop.variable);
      const fixed = `${block.recipe}(${handed.map((part, index) => (index === at ? loop.variable : part.trim())).join(", ")})`;
      const lean = `Line ${callLine} hands \`${block.recipe}\` the whole \`${loop.iterable}\`, not one ${sheets ? "sheet" : "item"}.`;
      return {
        ...explain(
          "list-to-recipe",
          "The whole list handed over",
          `Line ${callLine} hands \`${block.recipe}\` the whole \`${loop.iterable}\`, so \`${ingredients[at]}\` is a list inside the recipe. Hand it this pass's ${sheets ? "sheet" : "item"}, the loop variable: \`${fixed}\``,
          raw,
        ),
        slip: "a whole list handed to a recipe",
        slipLine: callLine,
        lean,
      };
    }
  }
  return null;
}

/**
 * Unit 6: "'<' not supported between instances of 'dict' and 'int'" with the loop variable compared (`if member < 10:`
 * under `for member in roster:`): one value from the sheet, by its tag (key), is compared.
 */
function explainLoopSheetCompared(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const kinds = message.match(/'(?:<|>|<=|>=)' not supported between instances of '(\w+)' and '(\w+)'/);
  if (!kinds || !kinds.slice(1).includes("dict") || !kinds.slice(1).some((kind) => kind === "int" || kind === "float")) return null;
  const body = codePart(text).trim();
  const mask = maskStrings(body);
  const sheets = sheetsOf(code, context);
  for (const loop of enclosingLoops(code, line)) {
    if (!/^[A-Za-z_]\w*$/.test(loop.variable) || !loopSheetNames(code, context).includes(loop.variable)) continue;
    const who = escapeRegExp(loop.variable);
    const compared = mask.match(new RegExp(`(?<![\\w.])${who}(?![\\w(\\[.])\\s*(<=|>=|<|>)\\s*([^:]+?)\\s*(?::|$|\\band\\b|\\bor\\b)`)) ??
      mask.match(new RegExp(`([^\\s(]+)\\s*(<=|>=|<|>)\\s*${who}(?![\\w(\\[.])`));
    if (!compared) continue;
    const numbers = entriesFor(sheets, loop.iterable).filter((entry) => entry.kind === "number" && entry.path.length === 0);
    const solved = readChains(context?.solution ?? "").find((chain) => chain.base === loop.variable && chain.reads.length === 1 && chain.reads[0].key !== undefined && numbers.some((entry) => entry.key === chain.reads[0].key));
    const key = solved?.reads[0].key ?? numbers[0]?.key;
    if (!key) continue;
    const read = `${loop.variable}["${key}"]`;
    const at = compared.index ?? 0;
    const shown = body.slice(at, at + compared[0].length).replace(/\s*(:|\band\b|\bor\b)\s*$/, "").trim();
    const example = shown.replace(new RegExp(`(?<![\\w.])${who}(?![\\w(\\[.])`), read);
    const lean = `${lineWord(line)} compares \`${loop.variable}\`, a whole sheet, with a number.`;
    return {
      ...explain(
        "whole-card-compared",
        "A whole sheet",
        `${lean} Compare one value from it by its tag (key), like \`${example}\`.`,
        raw,
      ),
      slip: "a whole sheet compared with a number",
      lean,
    };
  }
  return null;
}

/**
 * Unit 6's SyntaxErrors: `break` (or `continue`) at the left edge, outside the loop; a colon inside a one-line loop
 * (`[h for h in chalk_wall: if h < 45]`, the `for` line's habit); a one-line choice with no `else`
 * (`status = "ready" if mana >= 3`). Null for anything else.
 */
function explainLoopSyntax(message: string, code: string, text: string, line: number | null, raw: string, context?: ExplainContext): CourseExplanation | null {
  const word = message.match(/'(break|continue)' (?:outside loop|not properly in loop)/)?.[1];
  if (word) {
    const rows = (code ?? "").split("\n");
    // The line above it, inside a loop: `break` lines up with it (under the `if`, inside the loop).
    let above: number | null = null;
    for (let at = (line ?? 1) - 2; at >= 0; at -= 1) {
      if (codePart(rows[at] ?? "").trim()) {
        above = at + 1;
        break;
      }
    }
    const aboveText = above ? codePart(rows[above - 1] ?? "").trim() : "";
    const header = /:$/.test(aboveText);
    const inLoop = above !== null && (enclosingLoopHeaders(code, above).length > 0 || /^(for|while)\b/.test(aboveText));
    // Under the `if` when the line above sits in one (or is one), else just inside the loop.
    const rowsAbove = above !== null ? rows.slice(0, above) : [];
    let underIf = header && /^(if|elif|else)\b/.test(aboveText);
    if (above !== null && !header) {
      for (let at = above - 2, indent = indentOf(rows[above - 1] ?? ""); at >= 0 && indent > 0; at -= 1) {
        const row = codePart(rowsAbove[at] ?? "");
        if (!row.trim() || indentOf(row) >= indent) continue;
        underIf = /^\s*(if|elif|else)\b/.test(row);
        break;
      }
    }
    const sits = underIf ? "under the `if`, inside the loop" : "inside the loop";
    const lean = `${lineWord(line)} has \`${word}\` outside the loop.`;
    const what = `\`${word}\` only works inside a loop, but ${line ? `line ${line}` : "this line"} is outside every \`for\` and \`while\` loop.`;
    const hint = inLoop && !header
      ? `${what} Indent it to line up with \`${aboveText}\` on line ${above}, so it sits ${sits}.`
      : inLoop
        ? `${what} Indent it under line ${above}, \`${aboveText}\`, so it sits ${sits}.`
        : `${what} Use it only in the indented lines under a \`for\` or \`while\` line.`;
    return { ...explain("break-outside-loop", `${word} outside the loop`, hint, raw), slip: `\`${word}\` outside a loop`, lean };
  }
  if (/expected 'else' after 'if' expression/.test(message)) {
    const body = codePart(text).trim();
    const left = body.match(/^([A-Za-z_]\w*)\s*=(?!=)/)?.[1];
    // Mar'tu's version of the line: the same box, made with both values.
    const solved = left
      ? (context?.solution ?? "").split("\n").map((row) => codePart(row).trim()).find((row) => new RegExp(`^${escapeRegExp(left)}\\s*=(?!=).*\\bif\\b.*\\belse\\b`).test(maskStrings(row)))
      : undefined;
    const lean = `${lineWord(line)} has a one-line choice with no \`else\`.`;
    return {
      ...explain(
        "choice-needs-else",
        "A choice needs else",
        solved
          ? `${lean} A one-line choice needs both values, with \`else\` before the second: \`${solved}\``
          : `${lean} A one-line choice needs both values: after the question, add \`else\` and the value to use when the answer is False.`,
        raw,
      ),
      lean,
    };
  }
  if (/^invalid syntax/.test(message)) {
    const body = codePart(text);
    const mask = maskStrings(body);
    // A colon at the top level of square brackets that hold a `for ... in`: a one-line loop has no colon.
    for (let open = mask.indexOf("["); open >= 0; open = mask.indexOf("[", open + 1)) {
      const close = matchingBracket(mask, open);
      const end = close < 0 ? mask.length : close;
      const inside = mask.slice(open + 1, end);
      if (!/(?<![\w.])for\s+[A-Za-z_][\w\s,]*\s+in\s/.test(inside)) continue;
      const colons: number[] = [];
      let depth = 0;
      for (let at = open + 1; at < end; at += 1) {
        const char = mask[at];
        if (char in CLOSER) depth += 1;
        else if (char in OPENER) depth -= 1;
        else if (char === ":" && depth === 0) colons.push(at);
      }
      // `[h for h in wall if h > 45]:` puts the colon after the brackets: the same habit.
      const after = close >= 0 ? mask.slice(close + 1).match(/^\s*:/) : null;
      if (colons.length === 0 && !after) continue;
      let fixed = body;
      const marks = after && close >= 0 ? [...colons, close + 1 + (after[0].length - 1)] : colons;
      for (const at of [...marks].reverse()) fixed = `${fixed.slice(0, at)}${fixed.slice(at + 1)}`;
      fixed = fixed.trim().replace(/ {2,}/g, " ").replace(/\s+\]/g, "]");
      const lean = `${lineWord(line)} has a colon \`:\` in a one-line loop.`;
      return {
        ...explain(
          "colon-in-one-line-loop",
          "No colon in a one-line loop",
          `${lean} A one-line loop has no colon, unlike a \`for\` line. Take out the \`:\`: \`${fixed}\``,
          raw,
        ),
        lean,
      };
    }
  }
  return null;
}

/**
 * Unit 6: the recipe's own ingredient name used outside it (`mana_bar(hero)` in the loop): it only exists inside the
 * recipe, so the call hands over a value of its own, the loop variable when the line is inside a loop.
 */
function ingredientOutside(
  name: string,
  recipe: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation {
  const loop = enclosingLoops(code, line).find((entry) => /^[A-Za-z_]\w*$/.test(entry.variable) && entry.variable !== name);
  const called = new RegExp(`(^|[^\\w.])${escapeRegExp(recipe)}\\s*\\(`).test(maskStrings(codePart(text)));
  const lead = `\`${name}\` is the name of \`${recipe}\`'s ingredient, so it only exists inside the recipe.`;
  // The call Mar'tu's version makes in its loop, when it hands over the loop variable (`light_lantern(member["name"])`).
  const solved = loop
    ? (context?.solution ?? "").match(new RegExp(`(?<![\\w.])${escapeRegExp(recipe)}\\(\\s*${escapeRegExp(loop.variable)}\\b[^()]*\\)`))?.[0]
    : undefined;
  const instead = called
    ? loop
      ? `Out here, in the loop, hand over the loop variable instead, like \`${solved ?? `${recipe}(${loop.variable})`}\`.`
      : "Out here, hand over a value of your own in the call."
    : loop
      ? `Out here, in the loop, use the loop variable, \`${loop.variable}\`.`
      : `Out here, use a value of your own, or move this line inside \`${recipe}\`.`;
  return explain("made-inside-recipe", "Only inside the recipe", `${lead} ${instead}`, raw);
}

/** Unit 6: a recipe (in the code or the setup) whose `def` line takes `name`, when `line` is outside that recipe. */
function ingredientHome(name: string, code: string, line: number | null, setup = ""): string | null {
  if (line === null) return null;
  for (const block of recipeBlocks(code)) {
    if (line >= block.start && line <= block.end) continue;
    if ((recipeIngredients(code, block.recipe) ?? []).includes(name)) return block.recipe;
  }
  // The setup's recipes (`def light_lantern(name):`) run before the code: every line of the code is outside them.
  for (const block of recipeBlocks(setup)) {
    if (!block.recipe.startsWith("_") && (recipeIngredients(setup, block.recipe) ?? []).includes(name)) return block.recipe;
  }
  return null;
}

/** Unit 6: the loop variables that walk a list of sheets (`member` in `for member in roster:`): each holds one sheet. */
function loopSheetNames(code: string, context?: ExplainContext): string[] {
  const sheets = sheetsOf(code, context);
  return (code ?? "").split("\n").flatMap((row) => {
    const header = codePart(row).match(FOR_HEADER);
    const items = header ? sheets.lists.get(header[3].trim()) : undefined;
    const ofSheets = items && items.length > 0 && items.every((item) => item.name !== undefined || (item.ref !== undefined && sheets.names.has(item.ref)));
    return header && ofSheets && /^[A-Za-z_]\w*$/.test(header[2]) ? [header[2]] : [];
  });
}

/**
 * "unsupported operand type(s) for +: 'NoneType' and 'str'" on `print(name + " has ") + str(mana)`: the `)` that closes
 * `print( )` came too early, so the rest is outside it. Move that `)` to the very end of the line.
 */
function explainOutsidePrint(message: string, text: string, line: number | null, raw: string): CourseExplanation | null {
  if (!/unsupported operand type\(s\) for [^:]+: 'NoneType' and/.test(message)) return null;
  const body = codePart(text).trim();
  const mask = maskStrings(body);
  const open = mask.match(/^print\s*\(/);
  if (!open) return null;
  let depth = 0;
  let close = -1;
  for (let at = open[0].length - 1; at < mask.length; at += 1) {
    if (mask[at] === "(") depth += 1;
    else if (mask[at] === ")") {
      depth -= 1;
      if (depth === 0) {
        close = at;
        break;
      }
    }
  }
  if (close < 0 || !/^\s*[-+*/%]/.test(mask.slice(close + 1))) return null;
  const fixed = `${body.slice(0, close).trimEnd()}${body.slice(close + 1).replace(/^\s*/, " ").trimEnd()})`;
  return explain(
    "outside-print",
    "Outside print( )",
    `${lineWord(line)} adds more pieces after the \`)\` that closes \`print( )\`, so they are outside it. Everything to show goes inside print's parentheses. Move that \`)\` to the very end of the line: \`${fixed}\``,
    raw,
  );
}

function explainType(
  message: string,
  code: string,
  text: string,
  line: number | null,
  raw: string,
  context?: ExplainContext,
): CourseExplanation {
  // `print(name + " has ") + str(mana) + " mana."`: the pieces after the `)` that closes print are outside it, and
  // print hands back `None`. Never "values of kinds that don't go together" with Python's 'NoneType'.
  const outside = explainOutsidePrint(message, text, line, raw);
  if (outside) return outside;
  const fromInput = inputNames(code).find((name) => new RegExp(`\\b${escapeRegExp(name)}\\b`).test(text));
  const joinText = /can only concatenate str \(not "(int|float)"\) to str/.test(message);
  const addToNumber = /unsupported operand type\(s\) for \+: '(int|float)' and 'str'/.test(message);
  if ((joinText || addToNumber) && fromInput) {
    return explain(
      "input-is-text",
      "input() gives text",
      `\`${fromInput}\` came from \`input()\`, and \`input()\` always hands back text, like the writing on a paper form. To do math with it, turn it into a number first: \`int(${fromInput})\``,
      raw,
    );
  }
  if (joinText) {
    const number = text.match(/\+\s*([A-Za-z_]\w*)\b(?!\s*\()/)?.[1] ?? text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    // Unit 5: a number read from a sheet is shown whole, `str(gearshift["mana"])`, never `str(gearshift)`.
    const read = unitAtLeast(context, DICTS_UNIT_ORDER) ? sheetNumberRead(code, text, context) : null;
    const example = read ? `str(${read})` : number ? `str(${number})` : "str(score)";
    return explain(
      "text-plus-number",
      "Text + number",
      `${lineWord(line)} glues text to a number with \`+\`, but \`+\` only glues text to text. Turn the number into text first with \`str()\`: \`${example}\``,
      raw,
    );
  }
  if (addToNumber) {
    const number = text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    const example = number && number !== "print" ? `str(${number})` : "str()";
    return explain(
      "number-plus-text",
      "Number + text",
      `${lineWord(line)} puts \`+\` between a number and text, and Python can't add those. To glue them as text, turn the number into text first: \`${example}\``,
      raw,
    );
  }
  // `def hero(): "Lucky"` then `hero + " is ready."`: Python's own hint led to a recipe, not a box.
  const recipe = explainRecipeUsedAsBox(message, code, text, raw, context);
  if (recipe) return recipe;
  // Unit 6: inside a loop over a list of sheets, a key asked of the list or a sheet used as a position; a `for` loop over
  // one number; a whole sheet or a whole list added to a number. Before the Unit 5 rows, which do not know the loop.
  if (unitAtLeast(context, LOOPS_UNIT_ORDER)) {
    const loop =
      explainListToRecipe(message, code, line, raw, context) ??
      explainLoopListKey(message, code, text, line, raw) ??
      explainLoopSheetAsPosition(message, code, text, line, raw) ??
      explainLoopOverNumber(message, text, line, raw) ??
      explainLoopToolNotCalled(message, text, line, raw) ??
      explainWholeAdded(message, code, text, line, raw, context) ??
      explainLoopSheetCompared(message, code, text, line, raw, context);
    if (loop) return loop;
  }
  // Unit 5: a name where a list needs a position, a whole sheet as a key or in a comparison, math with `None`.
  if (unitAtLeast(context, DICTS_UNIT_ORDER)) {
    const sheet =
      explainNameAsPosition(message, code, text, line, raw, context) ??
      explainSheetAsPosition(message, code, text, line, raw, context) ??
      explainPositionAndKey(message, code, text, line, raw, context) ??
      explainWholeSheetKey(message, code, text, line, raw) ??
      explainWholeCardCompared(message, code, text, line, raw, context) ??
      explainNoneMath(message, code, raw);
    if (sheet) return sheet;
  }
  // Unit 4: one item joined to a list with `+`, square brackets after a tool, a comma between two positions.
  if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
    const list =
      explainListPlusItem(message, code, text, line, raw) ??
      explainNoneRead(message, code, text, line, raw) ??
      explainRowsWithoutComma(message, code, text, line, raw) ??
      explainToolWithSquareBrackets(message, code, text, line, raw, unitAtLeast(context, DICTS_UNIT_ORDER) ? SHEET_TOOLS : undefined) ??
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
      `${lineWord(line)} has a dash \`-\` where Python needs \`=\`. A dash means minus. To make a box, write: \`${dash}\``,
      raw,
    );
  }
  const bar = /unsupported operand type\(s\) for -: '(str|int)' and '(int|str)'/.test(message) ? barBrackets(text) : null;
  if (bar) {
    return explain(
      "bar-needs-brackets",
      "Parentheses for the gap",
      `Python does \`*\` before \`-\`${onLine(line)}, like PEMDAS in math. So it stamps the text first, then tries to take a number away from text. Put parentheses around the subtraction so it happens first: \`${bar}\``,
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
      `\`${quote}${digits}${quote}\`${onLine(line)} has quotes, so Python treats it as text, like the number on a jersey, not a number you can do math with. A number gets no quotes: write \`${digits}\`.`,
      raw,
    );
  }
  // Unit 5: `oogrish["mana"] - "ward_cost"`: a variable's name in quotes is only those letters (the unit's quotes rule).
  const quotedBox = unitAtLeast(context, DICTS_UNIT_ORDER) ? explainQuotedBoxInMath(message, code, text, line, raw) : null;
  if (quotedBox) return quotedBox;
  if (
    /unsupported operand type\(s\) for [-*/%]+: 'str' and '(int|float)'|unsupported operand type\(s\) for [-/%]+: '\w+' and 'str'|can't multiply sequence by non-int/.test(
      message,
    )
  ) {
    return explain(
      "math-with-text",
      "Math with text",
      `${lineWord(line)} does math with text. Text in quotes is not a number, even \`"5"\`. To turn text into a number, use \`int()\`.`,
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
        `Line ${shadowed.line} uses \`${shadowed.name}\` as a box's name, so \`${shadowed.name}()\` stops working. Pick a different name for your box.`,
        raw,
      );
    }
    // Unit 5: `gearshift("mana")`: a sheet read with round brackets (before the box-called-like-a-recipe row).
    if (notCallable[1] === "dict" && unitAtLeast(context, DICTS_UNIT_ORDER)) {
      const sheet = explainSheetCalled(code, text, line, raw, context);
      if (sheet) return sheet;
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
        `${lineWord(line)} calls \`${boxCalled.name}\` with parentheses ( ), but ${made}. Only a recipe made with \`def\` can be called.${notCallable[1] === "int" || notCallable[1] === "float" ? " To multiply by it, write `*` between them." : ""}`,
        raw,
      );
    }
    if (notCallable[1] === "int" || notCallable[1] === "float") {
      return explain(
        "use-star-to-multiply",
        "Use * to multiply",
        `${lineWord(line)} puts parentheses right after a number. In math, 2(3 + 4) means times, but Python needs the \`*\` sign: \`2 * (3 + 4)\`.`,
        raw,
      );
    }
    return explain(
      "not-a-function",
      "Can't use ( ) here",
      `${lineWord(line)} puts parentheses ( ) after a value, as if it were \`print\`. Only tools like \`print\`${unitAtLeast(context, FUNCTIONS_UNIT_ORDER) ? ", and recipes made with `def`," : ""} take parentheses after their name.`,
      raw,
    );
  }
  if (/takes \d+ positional arguments? but \d+ (were|was) given|missing \d+ required positional argument/.test(message)) {
    return explainValueCount(message, code, line, raw, context);
  }
  return explain("wrong-kind-of-value", "Wrong kind of value", `${lineWord(line)} mixes kinds of values that don't go together, like adding 5 meters to 3 seconds. Python's last line names the two kinds it found.`, raw);
}

const BLOCKED_MODULES = new Set([
  "js", "pyodide", "micropip", "urllib", "http", "socket", "ssl", "ftplib", "smtplib", "xmlrpc", "webbrowser",
  "requests", "httpx", "aiohttp",
]);

function explainParsed(parsed: Parsed, raw: string, code: string, context?: ExplainContext): CourseExplanation {
  const { type, message } = parsed;
  const line = errorLine(raw);
  const text = sourceLine(code, line) || shownLine(raw);

  // Unit 6: `for gap in "chalk_wall":` walks letters, so a right line crashes later: the quotes are the slip.
  if (unitAtLeast(context, LOOPS_UNIT_ORDER) && /^(TypeError|IndexError|KeyError|AttributeError|ValueError)$/.test(type)) {
    const quoted = explainQuotedLoop(code, line, raw, context);
    if (quoted) return quoted;
  }

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
        `${lineWord(line)} divides by zero, and no one can do that, not even Mar'tu. Check the number after the \`/\`.`,
        raw,
      );
    case "EOFError":
      return explain(
        "out-of-answers",
        "Too many questions",
        "Your code asks with `input()` more times than this exercise has answers for. Ask only the questions your step asks for.",
        raw,
      );
    case "TimeoutError":
      return explainTimeout(code, raw);
    case "TooMuchOutput":
      return explain(
        "too-much-output",
        "Printing forever?",
        "Your code printed so much that it was stopped. Look for a part of your code that repeats and never ends.",
        raw,
      );
    case "ValueError": {
      const notNumber = message.match(/invalid literal for int\(\) with base 10: (.+)$|could not convert string to float: (.+)$/);
      if (notNumber) {
        const got = notNumber[1] ?? notNumber[2];
        return explain(
          "not-a-number",
          "Not a number",
          `\`int()\` and \`float()\` can only turn text made of digits, like \`"12"\`, into a number. This one got ${got}.`,
          raw,
        );
      }
      // Unit 4: `chalk_wall.remove(3)` (a position) or `.remove("99")` (text): a value the list does not hold.
      if (/remove\(x\): x not in list/.test(message) && unitAtLeast(context, LISTS_UNIT_ORDER)) {
        return explainRemoveMissing(text, line, raw);
      }
      // Unit 6: two names in a `for` over a dictionary's keys: each key with its value comes from `.items()`.
      const keys = unitAtLeast(context, LOOPS_UNIT_ORDER) ? explainLoopNamesOverKeys(message, code, text, line, raw, context) : null;
      if (keys) return keys;
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
        // Unit 6: in a loop, the item used as a position (`chalk_wall[gap]`), or `[i + 1]` one past the end.
        const loop = unitAtLeast(context, LOOPS_UNIT_ORDER) && /list/.test(message) ? explainLoopIndex(code, text, line, raw, context) : null;
        if (loop) return loop;
        // Unit 5: a list of sheets (`roster[4]["name"]`): its own count and its last sheet, never "a list of lists".
        const sheetList = unitAtLeast(context, DICTS_UNIT_ORDER) && /list/.test(message) ? explainSheetsOutOfRange(code, text, line, raw, context) : null;
        if (sheetList) return sheetList;
        // Unit 4: in the unit's words (`len(wall)` as a position, the list's own count), never "3 items".
        const list = unitAtLeast(context, LISTS_UNIT_ORDER) ? explainOutOfRange(message, code, text, line, raw) : null;
        if (list) return list;
        const what = /string/.test(message) ? "text" : "list";
        return explain(
          "nothing-at-position",
          "Nothing at that position",
          `${lineWord(line)} asks for a position the ${what} doesn't have. Positions start at 0, like a ruler, so 3 items have positions 0, 1 and 2.`,
          raw,
        );
      }
      break;
    case "AssertionError":
      return explainAssert(message, text, line, raw);
    case "KeyError": {
      // Unit 5: a skipped level, one level too deep, a near miss, a position, two keys in one [ ].
      const key = unitAtLeast(context, DICTS_UNIT_ORDER) ? explainKeyError(message, code, text, line, raw, context) : null;
      if (key) return key;
      break;
    }
    case "AttributeError": {
      const meant = message.match(/Did you mean: '([^']+)'/)?.[1];
      const attribute = message.match(/attribute '([^']+)'/)?.[1];
      if (attribute && /^_{2,}$/.test(attribute)) return blankLeft(attribute, line, raw);
      // Unit 5: `lucky.mana`, `gearshift.fuel = "starlode"`: a dot where a sheet needs square brackets.
      if (unitAtLeast(context, DICTS_UNIT_ORDER)) {
        const dot = explainSheetDot(message, code, text, line, raw, context);
        if (dot) return dot;
      }
      // Unit 4: `chalk_wall.sorted()` ("Did you mean 'sort'" would sort the wall itself), `chalk_wall.max()`.
      if (unitAtLeast(context, LISTS_UNIT_ORDER)) {
        const front = explainToolAfterDot(message, text, line, raw);
        if (front) return front;
      }
      if (meant && attribute) {
        return explain("attribute-spelling", "Check the spelling", `There is no \`${attribute}\` here. Did you mean \`${meant}\`? Python never guesses a close name.`, raw);
      }
      // The campaign's words here ("no attribute ... the object before the dot") are programmer words: the same kind, plain words.
      if (attribute) {
        return explain(
          "other",
          "Nothing by that name after the dot",
          `${lineWord(line)} asks for \`${attribute}\` after a dot, but the value before the dot has nothing called \`${attribute}\`. Check the spelling after the dot, and check the name before it.`,
          raw,
        );
      }
      break;
    }
    case "ModuleNotFoundError": {
      const moduleName = message.match(/No module named '([^']+)'/)?.[1];
      if (moduleName && !BLOCKED_MODULES.has(moduleName.split(".")[0] ?? "")) {
        return explain(
          "no-such-module",
          "No module with that name",
          `Python has no module called \`${moduleName}\`. Check the spelling, like \`import random\`.`,
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
      // Unit 6: a running total in the recipe's loop with no start (`total = 0` left out): the start goes above it.
      const start = unitAtLeast(context, LOOPS_UNIT_ORDER) ? explainNoStartingValue(variable, code, text, line, raw, context) : null;
      if (start) return start;
      return explain(
        "variable-in-function",
        "A box inside a recipe",
        `Inside a recipe (function), \`${variable}\` is changed before it has a value there. Hand it over as an ingredient, or hand the new value back with \`return\`.`,
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
      `Python stopped with ${/^[AEIOU]/.test(type) ? "an" : "a"} ${type}${onLine(line)}. Python's last line, in the box, says what went wrong. Fix that line, then press Run again.`,
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
      "Python's last line, in the box, names the problem, and its line number shows where to look. Fix that line, then press Run again.",
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
      `Python stopped with ${/^[AEIOU]/.test(parsed.type) ? "an" : "a"} ${parsed.type}${onLine(line)}. Python's last line, in the box, says what went wrong. Fix that line, then press Run again.`,
      raw,
    );
  }
}

const PARSE_ERRORS = new Set(["SyntaxError", "IndentationError", "TabError"]);

/** Kinds that mean "still no quotes": a line that now parses but has the same slip is not a fix. */
const STILL_UNQUOTED = new Set<CourseErrorKind>(["unquoted-word", "unquoted-words", "missing-quote", "unknown-name", "lone-name"]);

/**
 * "One fixed! Python found the next mistake.": only when something really was fixed. The error moved to a later
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
  "unknown-function": "a tool Python doesn't know",
  "unknown-name": "a name Python doesn't know",
  "missing-import": "a missing import",
  "never-closed": "a ( or [ that never closes",
  "extra-bracket": "an extra closing mark",
  "brackets-dont-match": "marks that don't pair up",
  "missing-comma": "two values side by side",
  "two-single-quotes": "two ' marks used as a quote",
  "missing-comma-in-list": "a missing comma in a list",
  "print-needs-brackets": "print without parentheses",
  "compare-with-double-equals": "one `=` where a question needs two",
  "one-box-per-line": "two boxes made on one line",
  "names-side-by-side": "two names with no math sign between them",
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
  "method-as-function": "a text tool used without a dot",
  "randint-needs-random": "`randint` used on its own",
  "assert-failed": "an assert that came out False",
  "recipe-like-math": "a recipe written like math",
  "quoted-ingredient": "an ingredient name in quotes",
  "randint-backwards": "the numbers in the wrong order",
  "recipe-not-made-yet": "a recipe that is not made yet",
  "recipe-called-too-early": "a recipe called before its `def`",
  "made-inside-recipe": "a name that only lives inside a recipe",
  "not-in-recipe": "a name this recipe never makes",
  "store-backwards": "a box filled the wrong way around",
  "quoted-recipe-name": "quotes around a recipe's name",
  "list-needs-square-brackets": "parentheses where a list needs square brackets",
  "call-needs-round-brackets": "square brackets where a call needs parentheses",
  "comma-in-brackets": "a comma inside [ ] where one position goes",
  "list-plus-item": "one item joined to a list with `+`",
  "list-tool-without-dot": "a list tool used without the list's name and a dot",
  "items-after-brackets": "items outside the list's square brackets",
  "tool-after-dot": "a tool written after a dot",
  "not-on-the-list": "a value the list does not hold",
  "read-from-none": "a position read from `None`",
  "row-not-item": "a whole row where one of its items is meant",
  "equals-in-sheet": "an `=` inside a sheet",
  "key-outside-sheet": "a key with no sheet before it",
  "unquoted-key": "a key with no quotes",
  "dot-on-a-sheet": "a dot where a sheet needs square brackets",
  "name-as-position": "a name where a list needs a position",
  "whole-sheet-as-key": "a whole sheet used as a key",
  "whole-card-compared": "a whole card compared with a number",
  "math-with-none": "math with `None`",
  "loop-over-number": "a `for` loop over one number",
  "item-as-position": "an item used as a position",
  "one-past-the-end": "a position one past the end",
  "no-starting-value": "a running total with no starting value",
  "tag-as-name": "a tag (key) used as a name",
  "list-to-recipe": "a whole list handed to a recipe",
  "break-outside-loop": "`break` outside a loop",
  "colon-in-one-line-loop": "a colon inside a one-line loop",
  "choice-needs-else": "a one-line choice with no `else`",
  "input-is-text": "an input() answer used as a number",
  "text-plus-number": "text joined to a number",
  "number-plus-text": "a number added to text",
  "math-with-text": "math with text",
  "number-in-quotes": "a number in quotes",
  "bar-needs-brackets": "math in the wrong order",
  "name-taken": "a name Python already uses",
  "use-star-to-multiply": "parentheses right after a number",
  "not-a-function": "parentheses after something that can't use them",
  "wrong-number-of-values": "the wrong number of values handed over",
  "wrong-kind-of-value": "values of kinds that don't go together",
  "outside-print": "pieces outside `print( )`",
  "divide-by-zero": "a divide by zero",
  "out-of-answers": "more questions than answers",
  "not-a-number": "text that is not a number",
  "nothing-at-position": "a position that isn't there",
  "missing-key": "a missing key",
  "attribute-spelling": "a misspelled name after a dot",
  "no-such-module": "a module name Python doesn't know",
  "never-ending-calls": "a recipe that never stops calling itself",
  "variable-in-function": "a box changed inside a recipe",
  timeout: "a program that ran too long",
  "too-much-output": "a program that printed too much",
  "bare-value": "a value on its own",
  "bare-name": "a name on its own",
  "dash-no-effect": "a dash that keeps nothing",
  "print-without-brackets": "print without parentheses",
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
  const name = full.slip ?? SLIP_NAMES[full.kind];
  const line = full.slipLine ?? errorLine(raw);
  // Titles are plain text (no code marks). A name that starts with a code word (or a sign, `=`) keeps its small letters.
  const plain = name.replace(/`/g, "").replace(/^(a|an|the) /, "");
  const title = /^(def|else|elif|if|print|randint|input|for|while|break)\b|^[^A-Za-z]/.test(plain)
    ? `Mistake: ${name.replace(/`/g, "")}`
    : `${plain.charAt(0).toUpperCase()}${plain.slice(1)}`;
  const mistake = full.lean ?? `The mistake is ${line ? `on line ${line}` : "in your code"}: ${name}.`;
  return {
    ...full,
    explainer: "lean",
    title,
    hint: `${mistake} Python's last line, below, says what it found. Fix it yourself, then press Run again.`,
  };
}

function explainTimeout(code: string, raw: string): CourseExplanation {
  const loop = /^\s*while\b/m.test(code ?? "")
    ? "A `while` loop may never end: make sure its question can become False."
    : "Look for a part of your code that repeats and never ends.";
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
      // The box to name: the one a check looked for, else the box Mar'tu's version fills with this same value, else the
      // only one of the task's boxes the code has not made yet (or the task's only box). With none of those, no box is
      // named (never another step's box).
      const sameValue = solution
        .split("\n")
        .map((row) => codePart(row).match(/^\s*([A-Za-z_]\w*)\s*=(?!=)\s*(.+?)\s*$/))
        .find((made) => made !== null && made[2] === body)?.[1];
      const boxes = (options.context?.names ?? []).filter((name) => !COMMON_BUILTINS.includes(name));
      const unmade = boxes.filter((name) => !defined.has(name));
      const keep = missing ?? sameValue ?? (unmade.length === 1 ? unmade[0] : boxes.length === 1 ? boxes[0] : undefined) ?? (taskName ? undefined : null);
      const lost = `${where} is a value with no name in front: \`${body}\`. Python reads it and throws it away, like a phone number saved with no contact name.`;
      // A print-only task (Lesson 1A): boxes are not taught yet, so the only fix is print.
      const hint = missing
        ? `${lost} Put \`${keep} = \` in front of it: \`${keep} = ${body}\``
        : printOnly
          ? `${where} is ${STRING_LITERAL.test(body) ? "words in quotes" : NUMBER_LITERAL.test(body) ? "a number" : "a word"} with no \`print\`, so Python reads it and throws it away. To show it in the Console, write \`print(${body})\``
          : keep
            ? `${lost} Put \`${keep} = \` in front of it: \`${keep} = ${body}\``
            : keep === undefined
              ? `${lost} To keep it, put the box's name from your step and \`=\` in front of it.`
              : `${lost} To keep it, put a box's name and \`=\` in front of it. To show it instead, put it inside \`print( )\`: \`print(${body})\``;
      // Lesson 1A has not met boxes, values or names yet: its title says what is missing there, `print`.
      return {
        ...explain("bare-value", printOnly && !missing ? "Missing print" : "A value with no name", hint, raw),
        kind: "bare-value",
        line,
      };
    }
    if (body === "print") {
      return {
        ...explain(
          "print-without-brackets",
          "print needs ( )",
          `${where} says \`print\` with no parentheses, so nothing shows in the Console. Put what to show inside parentheses: \`print("your words")\``,
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
            : `${where} is only the name \`${body}\`, so Python looks inside the box and does nothing else. To show what \`${body}\` holds, write \`print(${body})\`.`,
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
        ? `${where} works out \`${left} - ${right}\`, but nothing keeps the answer, so \`${left}\` doesn't change. Put \`${left} =\` in front, so the answer goes back in the box: \`${left} = ${left} - ${right}\``
        : printOnly
          ? `${where} has a word and a dash \`-\`, but this step only shows words. To show words in the Console, write \`${printFix(right)}\``
          : `${where} has a dash \`-\` where \`=\` belongs, so nothing goes in the box. A dash means minus. To put the value in the box, write: \`${left} = ${right}\``;
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
        const show = COMPARE_ANYWHERE.test(maskStrings(asked.right)) ? "" : ` To show the answer instead, write \`print(${question})\``;
        hint = `${where} uses \`==\`, which only asks "is it the same as?". Python works out True or False, then throws the answer away, so nothing changes and nothing shows. To put a new value in the box, use one \`=\`: \`${box}\`.${show}`;
      } else {
        // A tool's name in the task's names (`append`) is never a box to keep the answer in.
        const notMade = (options.context?.names ?? []).find((name) => !defined.has(name) && !COMMON_BUILTINS.includes(name) && !CALLED_TOOLS.has(name));
        const keep = missing ?? notMade ?? "answer";
        hint = `${where} asks \`${question}\` and gets True or False, but nothing keeps or shows the answer. To keep it, put a box's name and \`=\` in front: \`${keep} = ${question}\`. To show it instead, put it inside \`print( )\`.`;
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
