import type { Direction } from "./schema";

export type Command =
  | { type: "move"; direction: Direction }
  | { type: "swap" }
  | { type: "confirm" }
  | { type: "option"; index: number }
  | { type: "release" };

const MOVES: Record<string, Direction> = {
  ArrowLeft: "left",
  ArrowRight: "right",
  ArrowUp: "up",
  ArrowDown: "down",
  a: "left",
  d: "right",
  w: "up",
  s: "down",
};

export function commandForKey(key: string): Command | null {
  const direction = MOVES[key] ?? MOVES[key.toLowerCase()];
  if (direction && (key.length === 1 || key.startsWith("Arrow"))) return { type: "move", direction };
  if (key === "Tab") return { type: "swap" };
  if (key === " " || key === "Enter" || key === "Spacebar") return { type: "confirm" };
  if (key === "Escape") return { type: "release" };
  if (/^[1-9]$/.test(key)) return { type: "option", index: Number(key) - 1 };
  return null;
}
