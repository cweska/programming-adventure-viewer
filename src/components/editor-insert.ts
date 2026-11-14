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
 * on a new line at the end, and a note goes at the very top. A "line" with a `target` (the step's own hint says where
 * its line goes: "in place of `pass`", "on the line after `total = affinity * 2`") goes there instead, so Start me off
 * never leaves the step's line outside the recipe it belongs in.
 */
export type InsertWhere = "cursor" | "code" | "line" | "note";

/**
 * Where the step's line goes when there is no cursor yet: `replace` the line that reads `line` (`pass`, keeping its
 * indent), go on a new line `after` it (after a `#` note's whole block, when the note goes on over several lines), or
 * on a new line `before` it, with its indent ("above `print(caster["mana"])`"). `near`: names that pick which one when
 * several lines match (the recipe the step names: the `pass` under `def step_west():`).
 */
export type InsertTarget = { line: string; how: "replace" | "after" | "before"; near?: readonly string[] };

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

/**
 * The line `target` names, in `doc`, and how the text goes there: the first match inside a recipe named in
 * `target.near`, else the first match. When several lines match and the recipe the step names is there but holds none
 * of them (its `pass` already rewritten), a new line under that recipe's last line instead: the step's line stays in
 * its own recipe, never in another recipe's `pass`.
 */
function findTarget(doc: string, target: InsertTarget): { line: Line; how: InsertTarget["how"] } | null {
  const want = target.line.trim();
  const lines: Line[] = [];
  let from = 0;
  for (const text of doc.split("\n")) {
    lines.push({ from, to: from + text.length, text });
    from += text.length + 1;
  }
  const codeOf = (text: string) => {
    const hash = noteStart(text);
    return (want.startsWith("#") || hash < 0 ? text : text.slice(0, hash)).trim();
  };
  const matches = lines
    .map((line, index) => ({ line, index }))
    .filter(({ line }) => (want.startsWith("#") ? codeOf(line.text).startsWith(want) : codeOf(line.text) === want));
  if (matches.length === 0) return null;
  // The recipe a line sits in: the nearest `def` above it with less indent.
  const recipeOf = (index: number) => {
    const indent = indentOf(lines[index].text).length;
    for (let at = index - 1; at >= 0; at -= 1) {
      const header = lines[at].text.match(/^(\s*)def\s+([A-Za-z_]\w*)/);
      if (header && header[1].length < indent) return header[2];
    }
    return null;
  };
  const near = target.near ?? [];
  const named = matches.find(({ index }) => {
    const recipe = recipeOf(index);
    return recipe !== null && near.includes(recipe);
  });
  if (named) return { line: named.line, how: target.how };
  // Exactly one recipe in the code is one the step names, and it holds no match: the line belongs in it.
  const headers = lines
    .map((line, index) => ({ name: line.text.match(/^\s*def\s+([A-Za-z_]\w*)/)?.[1], index }))
    .filter(({ name }) => name !== undefined && near.includes(name));
  const header = headers.length === 1 && matches.every(({ index }) => recipeOf(index) !== null) ? headers[0].index : -1;
  if (header >= 0) {
    let last = header;
    for (let at = header + 1; at < lines.length; at += 1) {
      if (lines[at].text.trim() === "") continue;
      if (indentOf(lines[at].text).length <= indentOf(lines[header].text).length) break;
      last = at;
    }
    return { line: lines[last], how: "after" };
  }
  return { line: matches[0].line, how: target.how };
}

export function planInsert(
  doc: string,
  selection: { from: number; to: number },
  placed: boolean,
  text: InsertText,
  where: InsertWhere = "cursor",
  target?: InsertTarget,
): InsertPlan {
  const value = (lineBefore: string, lineAfter = "") => (typeof text === "function" ? text(lineBefore, lineAfter) : text);
  const end = doc.length;

  if (!placed) {
    const found = where === "line" && target ? findTarget(doc, target) : null;
    let at = found?.line ?? null;
    let how = found?.how;
    // `after` a line whose next line is the same box with a placeholder value (`road_roll =` under `# 2.`, above
    // `road_roll = 0`): rewrite that line, never a second `road_roll =` above it. Only a placeholder: a line of the
    // student's own is never replaced.
    if (at && how === "after" && at.to < end) {
      const next = lineAt(doc, at.to + 1);
      const start = value(indentOf(next.text)).replace(/\s+/g, "");
      const rest = next.text.replace(/\s+/g, "").slice(start.length);
      const placeholder = /^(-?\d+|""|''|"_+"|_+|None|False|True)$/.test(rest);
      if (start.endsWith("=") && next.text.replace(/\s+/g, "").startsWith(start) && placeholder) {
        at = next;
        how = "replace";
      }
    }
    if (at && how === "replace") {
      const indent = indentOf(at.text);
      const insert = value(indent);
      return { from: at.from + indent.length, to: at.to, insert, anchor: at.from + indent.length + insert.length };
    }
    if (at && how === "before") {
      const indent = indentOf(at.text);
      const body = value(indent);
      const insert = `${indent}${body}\n`;
      return { from: at.from, to: at.from, insert, anchor: at.from + indent.length + body.length };
    }
    // `under `# 5.`` when the note goes on (`#    and Oogrish's intelligence,`): the line goes under the whole note.
    if (at && how === "after" && target?.line.trim().startsWith("#")) {
      while (at.to < end) {
        const next = lineAt(doc, at.to + 1);
        if (!/^\s*#\s{2,}\S/.test(next.text) || indentOf(next.text) !== indentOf(at.text)) break;
        at = next;
      }
    }
    if (at) {
      const indent = indentAfter(at.text);
      const body = value(indent);
      const insert = `\n${indent}${body}`;
      return { from: at.to, to: at.to, insert, anchor: at.to + insert.length };
    }
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
