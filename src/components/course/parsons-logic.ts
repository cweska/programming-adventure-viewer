/**
 * Pure helpers for <ParsonsBoard> ("put the lines in order") and the exercise player's "Assemble it".
 * Client-safe, no React. Blocks are plain strings and may repeat, so everything works by position.
 */

/** A small, fast, seeded random number generator (mulberry32). Returns numbers in [0, 1). */
function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** A stable 32-bit hash of a string (FNV-1a). */
export function hashSeed(text: string): number {
  let hash = 0x811c9dc5;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

function sameOrder<T>(a: readonly T[], b: readonly T[]): boolean {
  return a.length === b.length && a.every((value, index) => value === b[index]);
}

/**
 * Shuffle `items` the same way every time for the same `seed` (so a page reload shows the same pieces).
 * When there are at least two different items, the result is never in the original order: a student
 * should never be handed the answer already assembled.
 */
export function seededShuffle<T>(items: readonly T[], seed: string): T[] {
  const out = [...items];
  const random = mulberry32(hashSeed(seed));
  for (let index = out.length - 1; index > 0; index -= 1) {
    const pick = Math.floor(random() * (index + 1));
    [out[index], out[pick]] = [out[pick], out[index]];
  }
  if (out.length >= 2 && sameOrder(out, items) && new Set(items).size > 1) {
    // Rotate by one: still deterministic, and now different from the original order.
    out.push(out.shift() as T);
  }
  return out;
}

/**
 * Which of `blocks` are still in the Pieces list, as indexes into `blocks`. Each line already in
 * `value` uses up the first unused block with the same text (blocks can repeat).
 */
export function remainingPieces(blocks: readonly string[], value: readonly string[]): number[] {
  const used = new Set<number>();
  for (const line of value) {
    const at = blocks.findIndex((block, index) => block === line && !used.has(index));
    if (at >= 0) used.add(at);
  }
  return blocks.map((_, index) => index).filter((index) => !used.has(index));
}

/** Add a piece to the end of the program. */
export function addLine(value: readonly string[], line: string): string[] {
  return [...value, line];
}

/** Take line `index` out of the program (it goes back to the pieces). */
export function removeLine(value: readonly string[], index: number): string[] {
  if (index < 0 || index >= value.length) return [...value];
  return value.filter((_, at) => at !== index);
}

/** Move line `from` to position `to` (clamped). Returns a new array. */
export function moveLine(value: readonly string[], from: number, to: number): string[] {
  const out = [...value];
  if (from < 0 || from >= out.length) return out;
  const target = Math.max(0, Math.min(out.length - 1, to));
  if (target === from) return out;
  const [line] = out.splice(from, 1);
  out.splice(target, 0, line);
  return out;
}

/** How a line reads to a screen reader: indentation said out loud, so order and nesting are clear. */
export function spokenLine(line: string): string {
  const indent = line.length - line.trimStart().length;
  const text = line.trim() || "blank line";
  if (indent === 0) return text;
  const levels = Math.max(1, Math.round(indent / 4));
  return `${text} (indented ${levels === 1 ? "once" : `${levels} times`})`;
}
