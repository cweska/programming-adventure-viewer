import { checkAggro, startCombat } from "./combat";
import { startEnterCutscene } from "./cutscene";
import { startDialogue } from "./dialogue";
import { isWalkable } from "./rules";
import type { Direction, Position } from "./schema";
import type { GameState } from "./types";
import {
  actorAt,
  actorById,
  aliveHeroes,
  delta,
  distance,
  firstStepToward,
  hasFeature,
  isOpen,
  moveActor,
  notify,
  tileAt,
  updateActor,
} from "./world";

function followLeader(state: GameState, leaderFrom: Position): GameState {
  let next = state;
  let trail = leaderFrom;
  for (const hero of aliveHeroes(state)) {
    if (hero.id === state.leader) continue;
    const from = { x: hero.x, y: hero.y };
    if (distance(from, trail) === 1 && !actorAt(next, trail.x, trail.y)) {
      next = moveActor(next, hero.id, trail);
    } else if (distance(from, trail) > 1) {
      const step = firstStepToward(
        next,
        from,
        (position) => position.x === trail.x && position.y === trail.y,
        (position) => isOpen(next, position.x, position.y),
      );
      if (step) next = moveActor(next, hero.id, step);
    }
    trail = from;
  }
  return next;
}

function checkReach(state: GameState): GameState {
  const goal = state.goal;
  if (state.goalMet || goal?.type !== "reach" || !hasFeature(state, "movement")) return state;
  const leader = actorById(state, state.leader);
  if (!leader || leader.x !== goal.x || leader.y !== goal.y) return state;
  if (goal.enter) return startEnterCutscene(state, goal, goal.enter.after);
  return { ...state, goalMet: true };
}

export function stepParty(state: GameState, direction: Direction, scripted = false): GameState {
  if (state.mode !== "explore") return state;
  if (!scripted && !hasFeature(state, "movement")) return notify(state, "movement-locked");
  const leader = actorById(state, state.leader);
  if (!leader) return state;
  const step = delta(direction);
  const target = { x: leader.x + step.x, y: leader.y + step.y };
  const turned =
    direction === "left" || direction === "right" ? updateActor(state, leader.id, { facing: direction }) : state;
  if (!isWalkable(tileAt(state, target.x, target.y))) return turned;

  const occupant = actorAt(state, target.x, target.y);
  if (occupant?.kind === "hero") {
    const swapped = moveActor(moveActor(turned, leader.id, target), occupant.id, { x: leader.x, y: leader.y });
    return checkReach({ ...swapped, notice: null });
  }
  if (occupant) {
    if (scripted) return turned;
    if (occupant.kind === "npc") return startDialogue(turned, occupant);
    if (!hasFeature(state, "melee")) return notify(turned, "melee-locked");
    return startCombat(turned);
  }

  const moved = followLeader(moveActor(turned, leader.id, target), { x: leader.x, y: leader.y });
  const reached = checkReach({ ...moved, notice: null });
  return scripted || reached.mode !== "explore" ? reached : checkAggro(reached);
}

export function swapLeader(state: GameState): GameState {
  if (state.mode !== "explore") return state;
  const heroes = aliveHeroes(state);
  if (heroes.length < 2) return state;
  const index = heroes.findIndex((hero) => hero.id === state.leader);
  const next = heroes[(index + 1) % heroes.length];
  return { ...state, leader: next.id, notice: null };
}
