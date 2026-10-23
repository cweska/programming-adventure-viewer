import { rollDie } from "./rng";
import { damageTotal, formatModifier, isWalkable, modifier, resolveAttack } from "./rules";
import type { Direction, Position } from "./schema";
import type { Actor, GameState } from "./types";
import {
  actorAt,
  actorById,
  addLog,
  aliveEnemies,
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

export function activeCombatant(state: GameState): Actor | undefined {
  if (!state.combat) return undefined;
  return actorById(state, state.combat.order[state.combat.turn] ?? "");
}

export function startCombat(state: GameState): GameState {
  if (state.mode === "combat") return state;
  const combatants = [...aliveHeroes(state), ...aliveEnemies(state)];
  let rng = state.rng;
  const rolls = combatants.map((actor, index) => {
    const roll = rollDie(rng, 20);
    rng = roll.rng;
    return { actor, index, total: roll.value + modifier(actor.dexterity) };
  });
  rolls.sort(
    (left, right) =>
      right.total - left.total || right.actor.dexterity - left.actor.dexterity || left.index - right.index,
  );
  const order = rolls.map((roll) => roll.actor.id);
  const first = actorById(state, order[0] ?? "");
  const next: GameState = {
    ...state,
    rng,
    mode: "combat",
    notice: null,
    combatResult: null,
    combat: { order, turn: 0, round: 1, movesLeft: first?.speed ?? 0, attacked: false },
  };
  return addLog(
    next,
    "Combat! Everyone rolls for turn order.",
    `Turn order: ${rolls.map((roll) => `${roll.actor.name} (${roll.total})`).join(", ")}.`,
  );
}

export function checkAggro(state: GameState): GameState {
  if (state.mode !== "explore" || !hasFeature(state, "melee")) return state;
  const heroes = aliveHeroes(state);
  const alert = aliveEnemies(state).some(
    (enemy) => enemy.aggroRange > 0 && heroes.some((hero) => distance(hero, enemy) <= enemy.aggroRange),
  );
  return alert ? startCombat(state) : state;
}

function finishIfOver(state: GameState): GameState {
  if (state.mode !== "combat") return state;
  if (aliveEnemies(state).length === 0) {
    const revived = state.actors.map((actor) =>
      actor.kind === "hero" && actor.down ? { ...actor, down: false, hp: 1 } : actor,
    );
    return addLog(
      {
        ...state,
        actors: revived,
        mode: "explore",
        combat: null,
        combatResult: "victory",
        goalMet: state.goalMet || state.goal?.type === "defeat",
      },
      "Victory! The fight is over.",
    );
  }
  if (aliveHeroes(state).length === 0) {
    return addLog({ ...state, mode: "defeat", combat: null, combatResult: "defeat" }, "The party is knocked out.");
  }
  return state;
}

export function attack(state: GameState, attackerId: string, targetId: string): GameState {
  const attacker = actorById(state, attackerId);
  const target = actorById(state, targetId);
  if (!attacker || !target || target.down) return state;
  const toHit = rollDie(state.rng, 20);
  let rng = toHit.rng;
  const outcome = resolveAttack(toHit.value, attacker.attackBonus, target.defense);
  const facing = target.x < attacker.x ? "left" : target.x > attacker.x ? "right" : attacker.facing;
  let next = updateActor({ ...state, rng }, attacker.id, { facing });
  const rollText = `${attacker.name} ${attacker.attackText}: rolls ${outcome.natural} ${formatModifier(attacker.attackBonus).replace(/^([+-])/, "$1 ")} = ${outcome.total} vs Defense ${target.defense}.`;
  if (!outcome.hit) {
    const why = outcome.natural === 1 ? "A natural 1 always misses." : "Miss!";
    return { ...addLog(next, `${rollText} ${why}`), combat: next.combat ? { ...next.combat, attacked: true } : null };
  }
  const dice: number[] = [];
  for (let count = 0; count < (outcome.critical ? 2 : 1); count += 1) {
    const roll = rollDie(rng, attacker.damageDie);
    rng = roll.rng;
    dice.push(roll.value);
  }
  const damage = damageTotal(dice, attacker.damageBonus);
  const hp = Math.max(0, target.hp - damage);
  next = updateActor({ ...next, rng }, target.id, { hp, down: hp === 0 });
  const hitText = outcome.critical ? "Critical hit!" : "Hit!";
  const lines = [`${rollText} ${hitText} ${damage} damage.`];
  if (hp === 0) lines.push(`${target.name} ${target.downText}.`);
  next = addLog(next, ...lines);
  next = { ...next, combat: next.combat ? { ...next.combat, attacked: true } : null };
  return finishIfOver(next);
}

export function endTurn(state: GameState): GameState {
  const combat = state.combat;
  if (state.mode !== "combat" || !combat) return state;
  const checked = finishIfOver(state);
  if (checked.mode !== "combat") return checked;
  const count = combat.order.length;
  let turn = combat.turn;
  let round = combat.round;
  for (let step = 0; step < count; step += 1) {
    turn += 1;
    if (turn >= count) {
      turn = 0;
      round += 1;
    }
    const actor = actorById(state, combat.order[turn] ?? "");
    if (actor && !actor.down) {
      return {
        ...state,
        notice: null,
        combat: { ...combat, turn, round, movesLeft: actor.speed, attacked: false },
      };
    }
  }
  return state;
}

export function combatMove(state: GameState, direction: Direction): GameState {
  const active = activeCombatant(state);
  const combat = state.combat;
  if (!active || !combat) return state;
  if (active.kind !== "hero") return notify(state, "not-your-turn");
  if (!hasFeature(state, "movement")) return notify(state, "movement-locked");
  const step = delta(direction);
  const target = { x: active.x + step.x, y: active.y + step.y };
  const occupant = actorAt(state, target.x, target.y);
  if (occupant?.kind === "enemy") {
    if (combat.attacked) return state;
    return endTurn(attack(state, active.id, occupant.id));
  }
  if (occupant || !isWalkable(tileAt(state, target.x, target.y))) {
    return direction === "left" || direction === "right"
      ? updateActor(state, active.id, { facing: direction })
      : state;
  }
  if (combat.movesLeft <= 0) return notify(state, "no-moves");
  const moved = moveActor(state, active.id, target);
  return { ...moved, notice: null, combat: { ...combat, movesLeft: combat.movesLeft - 1 } };
}

function adjacentToHero(state: GameState, position: Position): boolean {
  return aliveHeroes(state).some((hero) => distance(hero, position) === 1);
}

export function enemyStep(state: GameState): GameState {
  const active = activeCombatant(state);
  const combat = state.combat;
  if (state.mode !== "combat" || !active || !combat || active.kind !== "enemy") return state;
  const adjacent = aliveHeroes(state).filter((hero) => distance(hero, active) === 1);
  if (adjacent.length > 0) {
    const target = adjacent.reduce((weakest, hero) => (hero.hp < weakest.hp ? hero : weakest));
    return endTurn(attack(state, active.id, target.id));
  }
  if (combat.movesLeft > 0) {
    const step = firstStepToward(
      state,
      active,
      (position) => adjacentToHero(state, position),
      (position) => isOpen(state, position.x, position.y),
    );
    if (step) {
      const moved = moveActor(state, active.id, step);
      return { ...moved, combat: { ...combat, movesLeft: combat.movesLeft - 1 } };
    }
  }
  return endTurn(state);
}

export function runEnemyTurns(state: GameState, limit = 200): GameState {
  let current = state;
  for (let count = 0; count < limit; count += 1) {
    const active = activeCombatant(current);
    if (current.mode !== "combat" || !active || active.kind !== "enemy") return current;
    current = enemyStep(current);
  }
  return current;
}
