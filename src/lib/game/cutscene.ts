import type { GameState } from "./types";
import { actorById, aliveHeroes, firstStepToward, isOpen, moveActor, updateActor } from "./world";

export function startEnterCutscene(state: GameState, door: { x: number; y: number }, after: readonly string[]): GameState {
  const queue = [...aliveHeroes(state).map((hero) => hero.id), ...after.filter((id) => actorById(state, id))];
  const leaderFirst = [state.leader, ...queue.filter((id) => id !== state.leader)];
  return {
    ...state,
    mode: "cutscene",
    notice: null,
    cutscene: { door: { ...door }, queue: leaderFirst, doorClosed: false },
  };
}

export function cutsceneStep(state: GameState): GameState {
  const cutscene = state.cutscene;
  if (state.mode !== "cutscene" || !cutscene || cutscene.doorClosed) return state;
  const [head, ...rest] = cutscene.queue;
  if (!head) {
    return { ...state, goalMet: true, cutscene: { ...cutscene, doorClosed: true } };
  }
  const actor = actorById(state, head);
  const door = cutscene.door;
  if (!actor || actor.hidden || (actor.x === door.x && actor.y === door.y)) {
    const hidden = actor ? updateActor(state, actor.id, { hidden: true }) : state;
    return { ...hidden, cutscene: { ...cutscene, queue: rest } };
  }
  const step = firstStepToward(
    state,
    actor,
    (position) => position.x === door.x && position.y === door.y,
    (position) => isOpen(state, position.x, position.y),
  );
  if (!step) {
    return { ...updateActor(state, actor.id, { hidden: true }), cutscene: { ...cutscene, queue: rest } };
  }
  return moveActor(state, actor.id, step);
}

export function runCutscene(state: GameState, limit = 200): GameState {
  let current = state;
  for (let count = 0; count < limit && current.mode === "cutscene" && !current.cutscene?.doorClosed; count += 1) {
    current = cutsceneStep(current);
  }
  return current;
}
