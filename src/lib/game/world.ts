import { isWalkable } from "./rules";
import type { Direction, Feature, Position, Tile } from "./schema";
import type { Actor, GameState, NoticeKind } from "./types";

const LOG_LIMIT = 60;

const NOTICES: Record<Exclude<NoticeKind, "nothing-to-say">, string> = {
  "movement-locked": "Your party can't move yet. Movement hasn't been programmed.",
  "dialogue-locked": "Talking hasn't been programmed yet.",
  "melee-locked": "Fighting hasn't been programmed yet.",
  "no-moves": "No steps left this turn. Walk into an enemy to attack, or press Space to end your turn.",
  "not-your-turn": "Wait for your turn.",
};

export function delta(direction: Direction): Position {
  switch (direction) {
    case "left":
      return { x: -1, y: 0 };
    case "right":
      return { x: 1, y: 0 };
    case "up":
      return { x: 0, y: -1 };
    case "down":
      return { x: 0, y: 1 };
  }
}

export function tileAt(state: GameState, x: number, y: number): Tile | undefined {
  return state.map.tiles[y]?.[x];
}

export function actorById(state: GameState, id: string): Actor | undefined {
  return state.actors.find((actor) => actor.id === id);
}

export function actorAt(state: GameState, x: number, y: number): Actor | undefined {
  return state.actors.find((actor) => !actor.down && !actor.hidden && actor.x === x && actor.y === y);
}

export function isOpen(state: GameState, x: number, y: number): boolean {
  return isWalkable(tileAt(state, x, y)) && !actorAt(state, x, y);
}

export function distance(a: Position, b: Position): number {
  return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}

export function hasFeature(state: GameState, feature: Feature): boolean {
  return state.features.includes(feature);
}

export function aliveHeroes(state: GameState): Actor[] {
  return state.party.flatMap((id) => {
    const actor = actorById(state, id);
    return actor && !actor.down ? [actor] : [];
  });
}

export function aliveEnemies(state: GameState): Actor[] {
  return state.actors.filter((actor) => actor.kind === "enemy" && !actor.down);
}

export function updateActor(state: GameState, id: string, patch: Partial<Actor>): GameState {
  return {
    ...state,
    actors: state.actors.map((actor) => (actor.id === id ? { ...actor, ...patch } : actor)),
  };
}

export function moveActor(state: GameState, id: string, to: Position): GameState {
  const actor = actorById(state, id);
  if (!actor) return state;
  const facing = to.x < actor.x ? "left" : to.x > actor.x ? "right" : actor.facing;
  return updateActor(state, id, { x: to.x, y: to.y, facing });
}

export function notify(state: GameState, kind: NoticeKind, text?: string): GameState {
  const message = text ?? (kind === "nothing-to-say" ? "" : NOTICES[kind]);
  return { ...state, notice: { kind, text: message, id: state.tick } };
}

export function addLog(state: GameState, ...lines: string[]): GameState {
  return { ...state, log: [...state.log, ...lines].slice(-LOG_LIMIT) };
}

export function firstStepToward(
  state: GameState,
  from: Position,
  isGoal: (position: Position) => boolean,
  passable: (position: Position) => boolean,
): Position | null {
  const key = (position: Position) => `${position.x},${position.y}`;
  const seen = new Set([key(from)]);
  const queue: { position: Position; first: Position | null }[] = [{ position: from, first: null }];
  const directions: Direction[] = ["up", "left", "right", "down"];
  while (queue.length > 0) {
    const current = queue.shift();
    if (!current) break;
    if (current.first && isGoal(current.position)) return current.first;
    for (const direction of directions) {
      const step = delta(direction);
      const next = { x: current.position.x + step.x, y: current.position.y + step.y };
      if (seen.has(key(next))) continue;
      seen.add(key(next));
      if (!passable(next)) continue;
      queue.push({ position: next, first: current.first ?? next });
    }
  }
  return null;
}
