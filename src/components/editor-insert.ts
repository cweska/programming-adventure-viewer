/**
 * Where a button puts text in the editor (Names to use chips, Mar'tu's pick, Help's "Start me off").
 * Pure: no CodeMirror, so it is unit tested in editor-insert.test.ts.
 *
 *  - "cursor":  at the cursor (replacing a selection). The symbol tray uses this.
 *  - "code":    at the cursor, unless the cursor is in a `#` note (or on a line that is only a note): then on
 *               a new line under it, so a name never ends up inside a note.
 *  - "line":    on a line of its own. A blank cursor line is used as it is; otherwise a new line goes under the
 *               cursor's line ("Start me off" starts a line, so it never lands in the middle of one).
 *  - "note":    a `#` note on a line of its own, above the cursor's line (notes sit above the code they explain).
 *
 * Before the student has ever clicked into the editor (`placed` false) there is no cursor to honour: text goes
 * on a new line at the end, and a note goes at the very top.
 */
export type InsertWhere = "cursor" | "code" | "line" | "note";

export type InsertPlan = { from: number; to: number; insert: string; anchor: number };

/**
 * The text that goes in may depend on what is before it on its line (e.g. Mar'tu's pick inside a string), and
 * on what is after it ("" when it goes on a line of its own).
 */
export type InsertText = string | ((lineBefore: string, lineAfter: string) => string);

type Line = { from: number; to: number; text: string };

function lineAt(doc: string, pos: number): Line {
  const from = doc.lastIndexOf("\n", pos - 1) + 1;
  const end = doc.indexOf("\n", pos);
  const to = end < 0 ? doc.length : end;
  return { from, to, text: doc.slice(from, to) };
}

/** Where a `#` note starts on a line (a `#` outside quotes), or -1. */
export function noteStart(lineText: string): number {
  let quote: string | null = null;
  for (let index = 0; index < lineText.length; index += 1) {
    const char = lineText[index];
    if (quote) {
      if (char === "\\") index += 1;
      else if (char === quote) quote = null;
    } else if (char === '"' || char === "'") {
      quote = char;
    } else if (char === "#") {
      return index;
    }
  }
  return -1;
}

function indentOf(text: string): string {
  return text.match(/^[ \t]*/)?.[0] ?? "";
}

/** The indent for a new line under `line`: the same, plus 4 spaces after a line that ends with `:`. */
function indentAfter(line: string): string {
  const hash = noteStart(line);
  const code = hash >= 0 ? line.slice(0, hash) : line;
  return code.trimEnd().endsWith(":") ? `${indentOf(line)}    ` : indentOf(line);
}

export function planInsert(
  doc: string,
  selection: { from: number; to: number },
  placed: boolean,
  text: InsertText,
  where: InsertWhere = "cursor",
): InsertPlan {
  const value = (lineBefore: string, lineAfter = "") => (typeof text === "function" ? text(lineBefore, lineAfter) : text);
  const end = doc.length;

  if (!placed) {
    if (where === "note") {
      const insert = `${value("")}\n`;
      return { from: 0, to: 0, insert, anchor: insert.length - 1 };
    }
    const needsBreak = end > 0 && doc[end - 1] !== "\n";
    const insert = `${needsBreak ? "\n" : ""}${value("")}`;
    return { from: end, to: end, insert, anchor: end + insert.length };
  }

  const from = Math.max(0, Math.min(selection.from, end));
  const to = Math.max(from, Math.min(selection.to, end));
  const line = lineAt(doc, from);
  const blank = line.text.trim() === "";
  const hash = noteStart(line.text);
  // In a note: after its `#`, or anywhere on a line that is only a note.
  const cursorInNote = hash >= 0 && (hash < from - line.from || line.text.slice(0, hash).trim() === "");

  const ownLine = where === "line" || where === "note" || (where === "code" && cursorInNote);
  if (!ownLine) {
    const insert = value(doc.slice(line.from, from), doc.slice(to, line.to));
    return { from, to, insert, anchor: from + insert.length };
  }

  if (blank) {
    // Use the empty line as it is, keeping its indent.
    const insert = value(line.text);
    return { from: line.to, to: line.to, insert, anchor: line.to + insert.length };
  }
  if (where === "note") {
    const indent = indentOf(line.text);
    const body = value(indent);
    const insert = `${indent}${body}\n`;
    return { from: line.from, to: line.from, insert, anchor: line.from + indent.length + body.length };
  }
  const indent = indentAfter(line.text);
  const body = value(indent);
  const insert = `\n${indent}${body}`;
  return { from: line.to, to: line.to, insert, anchor: line.to + insert.length };
}
