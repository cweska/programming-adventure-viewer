/**
 * Friendly error explanations for the Intro to Python course (contracts.ts ExplainCourseError).
 *
 * Wraps the campaign's explainPython() and adds plain-language help for the slips this class really
 * makes (docs/intro-to-python/research/student-groups.md, "Class-wide patterns"): unquoted text,
 * unclosed or mismatched quotes, `def` used to make a variable, a dash instead of `=`, capital-letter and
 * spelling mismatches, indentation, joining text and numbers, and more.
 *
 * Every explanation says what happened and what to try, in short sentences, with the line number when
 * Python gives one. `code` is the student's code (used to find the line and close names); it never
 * leaves the browser.
 */
import { explainPython } from "../languages/python/explain";
import type { Explanation } from "../languages/types";

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

/** The student's line number: the last `File "main.py", line N` (or `<exec>`, or any non-library file). */
function errorLine(raw: string): number | null {
  const frames = [...raw.matchAll(/File "([^"]+)", line (\d+)/g)];
  if (frames.length === 0) return null;
  const student = frames.filter((frame) => frame[1] === "main.py" || frame[1] === "<exec>");
  const pick = (student.length > 0 ? student : frames.filter((frame) => !frame[1].startsWith("/")))?.at(-1);
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
/* Names in the student's code                                                                     */
/* ---------------------------------------------------------------------------------------------- */

const COMMON_BUILTINS = [
  "print", "input", "len", "str", "int", "float", "bool", "range", "list", "dict", "tuple", "set", "type",
  "round", "sum", "min", "max", "abs", "sorted", "reversed", "enumerate", "zip", "map", "filter", "True",
  "False", "None", "random", "math",
];

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

/* ---------------------------------------------------------------------------------------------- */
/* The slips                                                                                       */
/* ---------------------------------------------------------------------------------------------- */

function explain(title: string, hint: string, raw: string): Explanation {
  return { title, hint, raw };
}

/** `name - "value"` (a dash where `=` belongs): returns `name = "value"`. */
function dashFix(text: string, name?: string): string | null {
  const who = name ? escapeRegExp(name) : "[A-Za-z_]\\w*";
  const match = text.match(new RegExp(`^\\s*(${who})\\s*-(?!=)\\s*(.+?)\\s*$`));
  if (!match || /=/.test(match[2])) return null;
  return `${match[1]} = ${match[2]}`;
}

function quotesProblem(text: string, line: number | null, raw: string): Explanation {
  const open = text.search(/["']/);
  if (open >= 0) {
    const quote = text[open];
    const other = quote === '"' ? "'" : '"';
    const rest = text.slice(open + 1);
    if (!rest.includes(quote) && rest.includes(other)) {
      const words = rest.slice(0, rest.indexOf(other));
      return explain(
        "Quotes don't match",
        `The text${onLine(line)} starts with ${quote} but ends with ${other}. Use the same kind of quote at both ends, like ${quote}${words}${quote}.`,
        raw,
      );
    }
    const words = rest.replace(/["']?\)*\s*$/, "").trim();
    if (quote === "'" && rest.includes("'")) {
      return explain(
        "Apostrophe in text",
        `The ' inside your text${onLine(line)} ends the text too early. Put double quotes around text that has an apostrophe, like "${words || "It's fun"}".`,
        raw,
      );
    }
    const example = words && words.length <= 40 ? `${quote}${words}${quote}` : `${quote}Hello${quote}`;
    return explain(
      "Missing quote",
      `The text${onLine(line)} is missing its closing quote. Text needs a quote at the start and at the end, like ${example}.`,
      raw,
    );
  }
  return explain(
    "Missing quote",
    `Some text${onLine(line)} is missing its closing quote. Text needs a quote at the start and at the end, like "Hello".`,
    raw,
  );
}

function defForVariable(text: string): string | null {
  const trimmed = text.trim();
  if (!/^def\b/.test(trimmed)) return null;
  // A real function header (maybe missing its colon) is not this slip: def greet(name="Lucky")
  const header = trimmed.match(/^def\s+[A-Za-z_]\w*\s*\(([^)]*)\)?\s*:?\s*$/);
  if (header && !/^\s*["']/.test(header[1] ?? "")) return null;
  if (/^def\s+[A-Za-z_]\w*\s*:\s*$/.test(trimmed)) return null;
  const quoted = trimmed.match(/^def\s*\(\s*["']([^"']*)["']/);
  const named = trimmed.match(/^def\s+([A-Za-z_]\w*)/);
  const value = trimmed.match(/=(?!=)\s*(.+)$/)?.[1]?.trim() ?? trimmed.match(/\(\s*(["'][^"']*["'])\s*\)/)?.[1];
  const looksLikeVariable = Boolean(quoted) || /^def\s*\(/.test(trimmed) || /=(?!=)/.test(trimmed) || /\(\s*["']/.test(trimmed);
  if (!looksLikeVariable) return null;
  const name = quoted?.[1] && /^[A-Za-z_]\w*$/.test(quoted[1]) ? quoted[1] : named?.[1];
  if (name && value && !quoted) return `${name} = ${value}`;
  if (name) return `${name} = "your value"`;
  return `character = "Kratos"`;
}

function explainSyntax(message: string, type: string, text: string, line: number | null, raw: string): Explanation {
  const lower = message.toLowerCase();

  if (/unterminated triple-quoted string/.test(lower)) {
    return explain(
      "Missing quotes",
      `A block of text that starts with three quotes${onLine(line)} never ends. Add the same three quotes where the text should stop.`,
      raw,
    );
  }
  if (/unterminated string literal|eol while scanning string literal/.test(lower)) {
    return quotesProblem(text, line, raw);
  }
  const curly = message.match(/invalid character '([“”‘’])'/);
  if (curly) {
    return explain(
      "Curly quotes",
      `${lineWord(line)} has a curly quote ${curly[1]} that Python can't read. Python only understands straight quotes: " or '. Delete it and type the quote again in the editor.`,
      raw,
    );
  }
  if (/invalid non-printable character/.test(lower)) {
    return explain(
      "Hidden character",
      `${lineWord(line)} has a hidden character Python can't read, often from copy and paste. Delete the spaces on that line and type them again.`,
      raw,
    );
  }
  const odd = message.match(/invalid character '(.)'/);
  if (odd) {
    return explain(
      "Odd character",
      `${lineWord(line)} has a character Python can't read: ${odd[1]}. If you copied this code, type that part again yourself.`,
      raw,
    );
  }

  const defFix = defForVariable(text);
  if (defFix) {
    return explain(
      "def makes functions",
      `def is for making functions, not variables. To make a variable, write the name, an equals sign, then the value: ${defFix}`,
      raw,
    );
  }

  if (/cannot assign to literal/.test(lower)) {
    const swap = text.match(/^\s*(.+?)\s*=(?!=)\s*([A-Za-z_]\w*)\s*$/);
    const example = swap ? `${swap[2]} = ${swap[1]}` : `character = "Kratos"`;
    return explain(
      "Name goes first",
      `The name goes on the left of = and the value goes on the right, like this: ${example}`,
      raw,
    );
  }
  if (/missing parentheses in call to 'print'/.test(lower)) {
    const inside = text.trim().match(/^print\s+(.+)$/)?.[1];
    return explain(
      "print needs ( )",
      `print needs parentheses around what it shows${onLine(line)}, like this: print(${inside ?? '"Hello"'})`,
      raw,
    );
  }
  if (/maybe you meant '==' or ':=' instead of '='|maybe you meant '==' instead of '='/.test(lower)) {
    return explain(
      "Use == to compare",
      `To check if two things are equal${onLine(line)}, use two equals signs: ==. One = is only for making a variable.`,
      raw,
    );
  }
  if (/perhaps you forgot a comma/.test(lower)) {
    const inside = text.match(/\(([^()"']*)\)/)?.[1]?.trim();
    if (inside && /^[A-Za-z][A-Za-z ,!?.']*[A-Za-z!?.]$/.test(inside) && inside.includes(" ")) {
      return explain(
        "Missing quotes?",
        `If ${inside} is text, put quotes around it: "${inside}". Text needs quotes.`,
        raw,
      );
    }
    return explain(
      "Missing comma or +",
      `${lineWord(line)} has two values side by side with nothing between them. Put a comma between them, or + to join text.`,
      raw,
    );
  }
  const neverClosed = message.match(/'([([{])' was never closed/);
  if (neverClosed) {
    const closing = { "(": ")", "[": "]", "{": "}" }[neverClosed[1]] ?? ")";
    return explain(
      `Missing ${closing}`,
      `A ${neverClosed[1]}${onLine(line)} never gets its closing ${closing}. Add ${closing} where it should end.`,
      raw,
    );
  }
  const unmatched = message.match(/unmatched '([)\]}])'/);
  if (unmatched) {
    return explain(
      `Extra ${unmatched[1]}`,
      `${lineWord(line)} has an extra ${unmatched[1]}. Remove it, or add the opening bracket it belongs to.`,
      raw,
    );
  }
  if (/closing parenthesis '.' does not match opening parenthesis/.test(lower)) {
    return explain(
      "Brackets don't match",
      `The brackets${onLine(line)} don't match. ( closes with ), [ closes with ], and { closes with }.`,
      raw,
    );
  }
  if (/expected '\('/.test(lower) && /^\s*def\b/.test(text)) {
    return explain(
      "def needs ( )",
      `A def line needs ( ) after the function's name, then a colon, like this: def greet():`,
      raw,
    );
  }
  if (/expected ':'/.test(lower)) {
    return explain(
      "Missing colon",
      `${lineWord(line)} needs a colon : at the end. Lines that start with if, elif, else, for, while or def always end with :`,
      raw,
    );
  }
  if (/invalid decimal literal|invalid imaginary literal/.test(lower)) {
    return explain(
      "Number stuck to letters",
      `${lineWord(line)} has a number with letters stuck to it. A name can't start with a number, and to multiply you write 5 * x, not 5x.`,
      raw,
    );
  }
  if (/expected an indented block|unexpected indent|unindent does not match/.test(lower) || type === "IndentationError") {
    return explainIndent(message, line, raw);
  }
  return explain(
    "Python can't read this",
    `Python could not read line ${line ?? "?"}. Look for a missing quote, a missing bracket ( ), or a missing colon :.`,
    raw,
  );
}

function explainIndent(message: string, line: number | null, raw: string): Explanation {
  const after = message.match(/expected an indented block after (.+?) on line (\d+)/);
  if (after) {
    const what = after[1]
      .replace(/^'(\w+)' statement$/, "the $1")
      .replace(/^function definition$/, "the def")
      .replace(/^class definition$/, "the class");
    return explain(
      "Indent this line",
      `The line after line ${after[2]} belongs inside ${what}, so it needs 4 spaces at the start.`,
      raw,
    );
  }
  if (/expected an indented block/.test(message)) {
    return explain("Indent this line", `${lineWord(line)} needs 4 spaces at the start, because it belongs inside the block above it.`, raw);
  }
  if (/unexpected indent/.test(message)) {
    return explain(
      "Extra spaces",
      `${lineWord(line)} starts with spaces it should not have. Move it back so it lines up with the line above.`,
      raw,
    );
  }
  if (/unindent does not match/.test(message)) {
    return explain(
      "Spaces don't line up",
      `${lineWord(line)} is indented a different amount than the lines around it. Line it up exactly with its block, using 4 spaces per level.`,
      raw,
    );
  }
  if (/tabs and spaces/.test(message)) {
    return explain("Tabs and spaces", `${lineWord(line)} mixes tabs and spaces. Delete the indent and use 4 spaces instead.`, raw);
  }
  return explain("Spaces at the start", `The spaces at the start of line ${line ?? "?"} don't fit. Use 4 spaces for each level inside a block.`, raw);
}

function explainName(message: string, code: string, text: string, line: number | null, raw: string): Explanation {
  const name = message.match(/name '([^']+)' is not defined/)?.[1];
  if (!name) return explain("Unknown name", "Python does not know one of the names on this line. Make it first, or check the spelling.", raw);

  const forgotImport = message.match(/Did you forget to import '([^']+)'/)?.[1];
  if (forgotImport) {
    return explain("Missing import", `To use ${forgotImport}, add this line at the top of your code: import ${forgotImport}`, raw);
  }

  const dash = dashFix(text, name);
  if (dash) {
    return explain(
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
  const close =
    trusted ??
    closeName(name, defined.map((entry) => entry.name)) ??
    closeName(name, COMMON_BUILTINS, 1);
  if (close && close.toLowerCase() === name.toLowerCase()) {
    return explain(
      "Capital letters matter",
      `Python sees ${name} and ${close} as different names. Use ${close}, with the same capital letters every time.`,
      raw,
    );
  }
  if (close) {
    return explain(
      "Check the spelling",
      `Python doesn't know ${name}. Did you mean ${close}? A name must be spelled the same way every time.`,
      raw,
    );
  }

  const grow = text.match(new RegExp(`^\\s*${escapeRegExp(name)}\\s*([-+*/%]|//|\\*\\*)=`));
  if (grow) {
    return explain(
      "Make it first",
      `${lineWord(line)} changes ${name}, but ${name} has no value yet. Give it a starting value first, like ${name} = 0`,
      raw,
    );
  }

  const later = defined.find((entry) => entry.name === name && line !== null && entry.line > line);
  if (later) {
    return explain(
      "Used too early",
      `Line ${line} uses ${name}, but ${name} is only made on line ${later.line}. Python runs from top to bottom, so make ${name} first.`,
      raw,
    );
  }

  const called = new RegExp(`(^|[^\\w.])${escapeRegExp(name)}\\s*\\(`).test(text);
  if (called) {
    return explain(
      "Unknown function",
      `Python doesn't know a function called ${name}. Check the spelling, or make it with def before you use it.`,
      raw,
    );
  }
  if (/^[A-Za-z]+$/.test(name)) {
    return explain(
      "Missing quotes?",
      `Python doesn't know the name ${name}. Did you mean to put quotes around it? Text needs quotes: "${name}"`,
      raw,
    );
  }
  return explain(
    "Unknown name",
    `Python doesn't know ${name} yet${onLine(line)}. Make it first (${name} = ...), or check the spelling.`,
    raw,
  );
}

function inputNames(code: string): string[] {
  return [...(code ?? "").matchAll(/^\s*([A-Za-z_]\w*)\s*=\s*input\s*\(/gm)].map((match) => match[1]);
}

function explainType(message: string, code: string, text: string, line: number | null, raw: string): Explanation {
  const fromInput = inputNames(code).find((name) => new RegExp(`\\b${escapeRegExp(name)}\\b`).test(text));
  const joinText = /can only concatenate str \(not "(int|float)"\) to str/.test(message);
  const addToNumber = /unsupported operand type\(s\) for \+: '(int|float)' and 'str'/.test(message);
  if ((joinText || addToNumber) && fromInput) {
    return explain(
      "input() gives text",
      `${fromInput} came from input(), and input() always gives back text. To do math with it, turn it into a number first: int(${fromInput})`,
      raw,
    );
  }
  if (joinText) {
    const number = text.match(/\+\s*([A-Za-z_]\w*)\b(?!\s*\()/)?.[1] ?? text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    const example = number ? `str(${number})` : "str(score)";
    return explain(
      "Text + number",
      `${lineWord(line)} joins text and a number with +. Turn the number into text first with str(), like ${example}.`,
      raw,
    );
  }
  if (addToNumber) {
    const number = text.match(/\b([A-Za-z_]\w*)\s*\+/)?.[1];
    const example = number && number !== "print" ? `str(${number})` : "str()";
    return explain(
      "Number + text",
      `${lineWord(line)} adds a number and text. To join them as text, turn the number into text first, like ${example}.`,
      raw,
    );
  }
  const dash = /unsupported operand type\(s\) for -/.test(message) ? dashFix(text) : null;
  if (dash) {
    return explain(
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
        "Name already taken",
        `Line ${shadowed.line} uses ${shadowed.name} as a variable name, so ${shadowed.name}() stops working. Pick a different name for your variable.`,
        raw,
      );
    }
    if (notCallable[1] === "int" || notCallable[1] === "float") {
      return explain(
        "Use * to multiply",
        `${lineWord(line)} puts ( ) right after a number. To multiply, write * between them, like 2 * (3 + 4).`,
        raw,
      );
    }
    return explain(
      "Not a function",
      `${lineWord(line)} puts ( ) after something that is not a function. Only functions like print() can be called with ( ).`,
      raw,
    );
  }
  if (/takes \d+ positional arguments? but \d+ (were|was) given|missing \d+ required positional argument/.test(message)) {
    return explain(
      "Wrong number of values",
      `The function call${onLine(line)} has the wrong number of values inside its ( ). Python says: ${message}.`,
      raw,
    );
  }
  return explain("Wrong kind of value", `${lineWord(line)} mixes kinds of values that don't go together: ${message}.`, raw);
}

const BLOCKED_MODULES = new Set([
  "js", "pyodide", "micropip", "urllib", "http", "socket", "ssl", "ftplib", "smtplib", "xmlrpc", "webbrowser",
  "requests", "httpx", "aiohttp",
]);

/** Explain a course run's traceback for an 11-15 year old: what happened, and what to try. */
export function explainCourseError(traceback: string, code: string): Explanation {
  const raw = traceback ?? "";
  const parsed = lastException(raw);
  if (!parsed) {
    if (/ran too long/i.test(raw)) return explainTimeout(code, raw);
    // A one-line message from the player itself (for example "Python could not load ... Reload the page.").
    const single = raw.trim();
    if (single && !single.includes("\n")) return explain("Python had a problem", single, raw);
    return explain("Python error", "Read the last line of the error: it names the problem, and the line number shows where to look.", raw);
  }
  const { type, message } = parsed;
  const line = errorLine(raw);
  const text = sourceLine(code, line) || shownLine(raw);

  switch (type) {
    case "SyntaxError":
      return explainSyntax(message, type, text, line, raw);
    case "IndentationError":
    case "TabError":
      return explainIndent(message, line, raw);
    case "NameError":
      return explainName(message, code, text, line, raw);
    case "TypeError":
      return explainType(message, code, text, line, raw);
    case "ZeroDivisionError":
      return explain(
        "Divided by zero",
        `${lineWord(line)} divides by zero, and no one can do that, not even Mar'tu. Check the number after the /.`,
        raw,
      );
    case "EOFError":
      return explain(
        "Too many questions",
        "Your code asked for input() more times than this exercise has answers for. Check that you only ask the questions the task asks for.",
        raw,
      );
    case "TimeoutError":
      return explainTimeout(code, raw);
    case "TooMuchOutput":
      return explain(
        "Printing forever?",
        "Your code printed a huge amount, so it was stopped. A loop may be running forever: make sure it has a way to end.",
        raw,
      );
    case "ValueError": {
      const notNumber = message.match(/invalid literal for int\(\) with base 10: (.+)$|could not convert string to float: (.+)$/);
      if (notNumber) {
        const got = notNumber[1] ?? notNumber[2];
        return explain(
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
        return explain("Check the spelling", `There is no ${attribute} here. Did you mean ${meant}?`, raw);
      }
      break;
    }
    case "ModuleNotFoundError": {
      const moduleName = message.match(/No module named '([^']+)'/)?.[1];
      if (moduleName && !BLOCKED_MODULES.has(moduleName.split(".")[0] ?? "")) {
        return explain(
          "No module with that name",
          `Python has no module called ${moduleName}. Check the spelling, like import random or import math.`,
          raw,
        );
      }
      break;
    }
    case "RecursionError":
      return explain(
        "Never-ending calls",
        "A function keeps calling itself and never stops. Make sure it has a way to finish with a return that does not call it again.",
        raw,
      );
    case "UnboundLocalError": {
      const variable = message.match(/variable '([^']+)'/)?.[1] ?? "a variable";
      return explain(
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
      base.title,
      `Python stopped with ${type}${onLine(line)}. Read the last line of the error: it says what went wrong.`,
      raw,
    );
  }
  return base;
}

function explainTimeout(code: string, raw: string): Explanation {
  const loop = /^\s*while\b/m.test(code ?? "")
    ? "A while loop may never end: make sure its condition can become False."
    : "Look for a loop that never ends.";
  return explain("Ran too long", `Your code ran for more than 5 seconds, so it was stopped. ${loop}`, raw);
}

/** The source line Python printed under `File "...", line N` (when the code is not at hand). */
function shownLine(raw: string): string {
  const lines = raw.split("\n");
  for (let index = lines.length - 1; index > 0; index -= 1) {
    if (/^\s*File "[^"]+", line \d+/.test(lines[index - 1])) return lines[index] ?? "";
  }
  return "";
}
