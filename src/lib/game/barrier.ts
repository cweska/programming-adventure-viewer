import type { GameState } from "./types";
import { aliveHeroes, notify } from "./world";

export const BARRIER_LEVELS = 4;

export function maxManaFor(magicalAffinity: number): number {
  return magicalAffinity * 2;
}

export function changeMana(state: GameState, actorId: string, mana: number, max: number): GameState {
  const before = state.mana[actorId];
  const spent = before ? before.mana - mana : 0;
  return {
    ...state,
    mana: { ...state.mana, [actorId]: { mana, max } },
    manaDrop: spent > 0 ? { actorId, amount: spent, id: state.tick } : state.manaDrop,
  };
}

export function castLanded(state: GameState, actorId: string): GameState {
  const barrier = state.barrier;
  if (!barrier || barrier.locked) return state;
  const casters = barrier.casters.includes(actorId) ? barrier.casters : [...barrier.casters, actorId];
  const everyone = aliveHeroes(state).every((hero) => casters.includes(hero.id));
  const line = state.castLines[actorId];
  return {
    ...state,
    notice: null,
    prompt: null,
    castFx: { actorId, id: state.tick },
    speech: line ? { actorId, text: line, id: state.tick } : state.speech,
    barrier: {
      ...barrier,
      casters,
      level: Math.min(BARRIER_LEVELS, casters.length),
      locked: everyone,
    },
  };
}

export function showPrompt(state: GameState, text: string): GameState {
  return { ...state, prompt: { text, id: state.tick } };
}

export function waveStep(state: GameState): GameState {
  const barrier = state.barrier;
  if (!barrier || !barrier.locked || barrier.done) return state;
  const wave = barrier.wave + 1;
  const done = wave > state.map.width + 1;
  return {
    ...state,
    barrier: { ...barrier, wave, done },
    goalMet: state.goalMet || (done && state.goal?.type === "barrier"),
  };
}

export function insideBarrier(state: GameState, x: number, y: number): boolean {
  const barrier = state.barrier;
  return Boolean(barrier && x >= barrier.x0 && x <= barrier.x1 && y >= barrier.y0 && y <= barrier.y1);
}

export function castNotice(state: GameState, unlocked: boolean): GameState {
  return notify(state, unlocked ? "cast-hint" : "magic-locked");
}
