/**
 * Part instructions use a tiny format so they are easy to read:
 * - every line of the text is its own line on screen,
 * - a run of lines that start with "1. ", "2. ", ... becomes a numbered list,
 * - text inside `backticks` is shown as code.
 */
export type InlinePart = { code: boolean; text: string };

export type InstructionBlock =
  | { kind: "line"; parts: InlinePart[] }
  | { kind: "steps"; items: InlinePart[][] };

const STEP = /^\d+\.\s+/;

export function inlineParts(text: string): InlinePart[] {
  const pieces = text.split("`");
  // An odd number of backticks leaves the last one unmatched: keep it as plain text.
  if (pieces.length % 2 === 0) {
    const last = pieces.pop() ?? "";
    pieces[pieces.length - 1] += `\`${last}`;
  }
  return pieces.flatMap((piece, index) => (piece ? [{ code: index % 2 === 1, text: piece }] : []));
}

export function instructionBlocks(text: string): InstructionBlock[] {
  const blocks: InstructionBlock[] = [];
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (!line) continue;
    if (STEP.test(line)) {
      const item = inlineParts(line.replace(STEP, ""));
      const last = blocks.at(-1);
      if (last?.kind === "steps") last.items.push(item);
      else blocks.push({ kind: "steps", items: [item] });
      continue;
    }
    blocks.push({ kind: "line", parts: inlineParts(line) });
  }
  return blocks;
}

/** The instructions as plain text, without the backticks. */
export function instructionText(text: string): string {
  return instructionBlocks(text)
    .flatMap((block) => (block.kind === "line" ? [block.parts] : block.items))
    .map((parts) => parts.map((part) => part.text).join(""))
    .join("\n");
}
