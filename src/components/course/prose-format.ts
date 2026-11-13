/**
 * The course's tiny prose format (documented at the top of src/lib/course/schema.ts), as plain data.
 * Pure and client-safe: <Prose> renders these blocks, the registry uses glossaryRefs() to pick the
 * glossary entries a page needs, and <ReadAloud> uses speakableText().
 *
 *   - one paragraph per line ("\n" separates lines; blank lines are skipped)
 *   - lines starting "1. ", "2. " ... become a numbered list ("- " lines become a bullet list)
 *   - `backticks` become inline code
 *   - ```python fenced blocks``` become code blocks (kept exactly as written)
 *   - [[term]] or [[term|shown text]] link to the glossary
 */
import type { GlossaryEntry } from "../../lib/course/schema";

export type InlinePart =
  | { kind: "text"; text: string }
  | { kind: "code"; text: string }
  | { kind: "term"; term: string; text: string };

export type ProseBlock =
  | { kind: "paragraph"; parts: InlinePart[] }
  | { kind: "list"; ordered: boolean; start: number; items: InlinePart[][] }
  | { kind: "code"; language: string; code: string };

const NUMBERED = /^(\d+)\.\s+/;
const BULLET = /^[-*]\s+/;
const FENCE = /^```\s*([A-Za-z0-9_+-]*)\s*$/;
const TERM = /\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]/g;

/** Plain text with [[term]] / [[term|text]] links. */
function termParts(text: string): InlinePart[] {
  const parts: InlinePart[] = [];
  let last = 0;
  for (const match of text.matchAll(TERM)) {
    const at = match.index ?? 0;
    if (at > last) parts.push({ kind: "text", text: text.slice(last, at) });
    const term = match[1].trim();
    const shown = (match[2] ?? match[1]).trim();
    parts.push({ kind: "term", term, text: shown });
    last = at + match[0].length;
  }
  if (last < text.length) parts.push({ kind: "text", text: text.slice(last) });
  return parts;
}

/** One line of prose: `code` spans first, then glossary links in the plain text between them. */
export function inlineParts(text: string): InlinePart[] {
  const pieces = text.split("`");
  // An odd number of backticks leaves the last one unmatched: keep it as plain text.
  if (pieces.length % 2 === 0) {
    const tail = pieces.pop() ?? "";
    pieces[pieces.length - 1] += `\`${tail}`;
  }
  const parts: InlinePart[] = [];
  pieces.forEach((piece, index) => {
    if (!piece) return;
    if (index % 2 === 1) parts.push({ kind: "code", text: piece });
    else parts.push(...termParts(piece));
  });
  return parts;
}

export function proseBlocks(text: string): ProseBlock[] {
  const blocks: ProseBlock[] = [];
  const lines = (text ?? "").replace(/\r\n?/g, "\n").split("\n");
  for (let index = 0; index < lines.length; index += 1) {
    const raw = lines[index];
    const line = raw.trim();
    const fence = line.match(FENCE);
    if (fence) {
      const code: string[] = [];
      index += 1;
      while (index < lines.length && !/^```\s*$/.test(lines[index].trim())) {
        code.push(lines[index]);
        index += 1;
      }
      blocks.push({ kind: "code", language: fence[1] || "python", code: code.join("\n") });
      continue;
    }
    if (!line) continue;
    const numbered = line.match(NUMBERED);
    const bullet = numbered ? null : line.match(BULLET);
    if (numbered || bullet) {
      const ordered = Boolean(numbered);
      const item = inlineParts(line.replace(ordered ? NUMBERED : BULLET, ""));
      const last = blocks.at(-1);
      if (last?.kind === "list" && last.ordered === ordered) last.items.push(item);
      else blocks.push({ kind: "list", ordered, start: numbered ? Number(numbered[1]) : 1, items: [item] });
      continue;
    }
    blocks.push({ kind: "paragraph", parts: inlineParts(line) });
  }
  return blocks;
}

/** Every glossary term a piece of prose links to (the part before "|"), in order, without repeats. */
export function glossaryRefs(text: string): string[] {
  const seen = new Set<string>();
  const refs: string[] = [];
  for (const block of proseBlocks(text)) {
    const lines = block.kind === "paragraph" ? [block.parts] : block.kind === "list" ? block.items : [];
    for (const parts of lines) {
      for (const part of parts) {
        if (part.kind !== "term") continue;
        const key = part.term.toLowerCase();
        if (seen.has(key)) continue;
        seen.add(key);
        refs.push(part.term);
      }
    }
  }
  return refs;
}

/** The glossary entry for a [[term]]: its term or any alias, ignoring case and outer spaces. */
export function findGlossaryEntry(glossary: readonly GlossaryEntry[], term: string): GlossaryEntry | undefined {
  const wanted = term.trim().toLowerCase();
  if (!wanted) return undefined;
  return (
    glossary.find((entry) => entry.term.trim().toLowerCase() === wanted) ??
    glossary.find((entry) => entry.aliases.some((alias) => alias.trim().toLowerCase() === wanted))
  );
}

function partsText(parts: InlinePart[]): string {
  return parts.map((part) => part.text).join("");
}

/** The prose as plain text, without backticks or glossary brackets. Code blocks are kept as written. */
export function plainText(text: string): string {
  return proseBlocks(text)
    .map((block) => {
      if (block.kind === "paragraph") return partsText(block.parts);
      if (block.kind === "code") return block.code;
      return block.items
        .map((item, index) => (block.ordered ? `${block.start + index}. ${partsText(item)}` : partsText(item)))
        .join("\n");
    })
    .join("\n");
}

/** What the read-aloud button says: the words, with code blocks replaced by a short spoken note. */
export function speakableText(text: string): string {
  return proseBlocks(text)
    .map((block) => {
      if (block.kind === "paragraph") return partsText(block.parts);
      if (block.kind === "code") return "Here is some code to look at.";
      return block.items.map((item, index) => (block.ordered ? `${block.start + index}. ` : "") + partsText(item)).join(" ");
    })
    .map((line) => line.trim())
    .filter(Boolean)
    .join(" ");
}

/** Story lines: they talk about the party, or are Mar'tu's ", yes?" asides. */
const STORY = /\b(Mar'tu|Lucky|Oogrish|Gearshift|Bomb Shell)\b|,\s*yes\?/i;

/**
 * True when a block carries something to do or learn: code, a glossary word, a list, a code block,
 * or a plain line that is not one of the story lines.
 */
function isEssential(block: ProseBlock): boolean {
  if (block.kind !== "paragraph") return true;
  if (block.parts.some((part) => part.kind === "code" || part.kind === "term")) return true;
  return !STORY.test(partsText(block.parts));
}

/**
 * "Fewer words" mode: keep the lines that teach (code, glossary words, steps, code blocks, plain facts)
 * and drop the story lines around them. Returns every block when nothing would be left.
 */
export function lightBlocks(blocks: ProseBlock[]): ProseBlock[] {
  const kept = blocks.filter(isEssential);
  return kept.length === 0 ? blocks : kept;
}
