import { describe, expect, it } from "vitest";
import { campaignData } from "../campaign/registry";
import { activeCombatant, runEnemyTurns, startCombat } from "./combat";
import { roomBoard, testData } from "./fixtures";
import { gameReducer, playActions } from "./reducer";
import { rollDie, seedRng } from "./rng";
import { damageTotal, heroStats, modifier, resolveAttack } from "./rules";
import type { Direction } from "./schema";
import { createGame } from "./state";
import type { GameState } from "./types";
import { actorById, aliveEnemies, distance } from "./world";

function sparBoard(seed = 7) {
  return roomBoard({
    features: ["movement", "melee"],
    actors: [
      { id: "bot-1", kind: "enemy", ref: "sparring-bot", x: 7, y: 1 },
      { id: "bot-2", kind: "enemy", ref: "sparring-bot", x: 7, y: 4 },
    ],
    goal: { type: "defeat" },
    seed,
  });
}

function withTurn(state: GameState, order: string[]): GameState {
  const first = actorById(state, order[0]);
  if (!state.combat || !first) throw new Error("combat should have started");
  return { ...state, combat: { ...state.combat, order, turn: 0, movesLeft: first.speed, attacked: false } };
}

function towardNearestEnemy(state: GameState, heroId: string): Direction {
  const hero = actorById(state, heroId);
  if (!hero) throw new Error("missing hero");
  const target = aliveEnemies(state).reduce((best, enemy) => (distance(hero, enemy) < distance(hero, best) ? enemy : best));
  const options: [Direction, number, number][] = [
    ["right", 1, 0],
    ["left", -1, 0],
    ["down", 0, 1],
    ["up", 0, -1],
  ];
  const ranked = options
    .map(([direction, dx, dy]) => ({ direction, score: distance({ x: hero.x + dx, y: hero.y + dy }, target) }))
    .sort((a, b) => a.score - b.score);
  return ranked[0].direction;
}

function fight(state: GameState, limit = 400): GameState {
  let current = state;
  for (let count = 0; count < limit && current.mode === "combat"; count += 1) {
    const active = activeCombatant(current);
    if (!active) break;
    if (active.kind === "enemy") {
      current = runEnemyTurns(current);
      continue;
    }
    const before = current;
    current = gameReducer(current, { type: "move", direction: towardNearestEnemy(current, active.id) });
    if (current.combat && current.combat === before.combat && activeCombatant(current)?.id === active.id) {
      current = gameReducer(current, { type: "endTurn" });
    }
  }
  return current;
}

describe("rules", () => {
  it("turns ability scores into modifiers", () => {
    expect([1, 8, 9, 10, 11, 12, 13, 14, 17, 20].map(modifier)).toEqual([-5, -1, -1, 0, 0, 1, 1, 2, 3, 5]);
  });

  it("derives combat stats from the character sheets", () => {
    const { characters, classes } = campaignData;
    expect(heroStats(characters.gearshift, classes.warrior)).toEqual({
      maxHp: 15,
      defense: 14,
      attackBonus: 5,
      damageBonus: 3,
      speed: 5,
      initiativeBonus: 1,
    });
    expect(heroStats(characters.oogrish, classes.general)).toEqual({
      maxHp: 12,
      defense: 14,
      attackBonus: 3,
      damageBonus: 1,
      speed: 4,
      initiativeBonus: 2,
    });
  });

  it("hits on total at least defense, always hits on 20, and always misses on 1", () => {
    expect(resolveAttack(10, 5, 15)).toMatchObject({ total: 15, hit: true, critical: false });
    expect(resolveAttack(9, 5, 15)).toMatchObject({ total: 14, hit: false });
    expect(resolveAttack(20, -5, 30)).toMatchObject({ hit: true, critical: true });
    expect(resolveAttack(1, 40, 2)).toMatchObject({ hit: false, critical: false });
  });

  it("never deals less than 1 damage", () => {
    expect(damageTotal([1], -3)).toBe(1);
    expect(damageTotal([4, 6], 3)).toBe(13);
  });

  it("rolls the same dice for the same seed and stays in range", () => {
    let left = seedRng(42);
    let right = seedRng(42);
    for (let count = 0; count < 200; count += 1) {
      const a = rollDie(left, 20);
      const b = rollDie(right, 20);
      expect(a.value).toBe(b.value);
      expect(a.value).toBeGreaterThanOrEqual(1);
      expect(a.value).toBeLessThanOrEqual(20);
      left = a.rng;
      right = b.rng;
    }
  });
});

describe("melee combat", () => {
  it("starts when the party comes within an enemy's range and rolls a repeatable turn order", () => {
    const start = createGame(sparBoard(), testData);
    expect(start.mode).toBe("explore");
    const near = playActions(start, [
      { type: "move", direction: "right" },
      { type: "move", direction: "right" },
    ]);
    expect(near.mode).toBe("combat");
    expect(near.combat?.order).toHaveLength(4);
    expect([...(near.combat?.order ?? [])].sort()).toEqual(["bot-1", "bot-2", "gearshift", "oogrish"]);
    const again = playActions(createGame(sparBoard(), testData), [
      { type: "move", direction: "right" },
      { type: "move", direction: "right" },
    ]);
    expect(again.combat?.order).toEqual(near.combat?.order);
    expect(near.log.some((line) => line.startsWith("Turn order:"))).toBe(true);
  });

  it("does not fight until melee is unlocked", () => {
    const board = roomBoard({ actors: [{ id: "bot", kind: "enemy", ref: "sparring-bot", x: 4, y: 3 }] });
    const state = playActions(createGame(board, testData), [{ type: "move", direction: "right" }]);
    expect(state.mode).toBe("explore");
    expect(state.notice?.kind).toBe("melee-locked");
  });

  it("limits each hero to their speed", () => {
    const board = roomBoard({
      features: ["movement", "melee"],
      actors: [{ id: "bot", kind: "enemy", ref: "sparring-bot", x: 7, y: 1 }],
    });
    let state = withTurn(startCombat(createGame(board, testData)), ["gearshift", "oogrish", "bot"]);
    expect(state.combat?.movesLeft).toBe(5);
    for (const direction of ["down", "right", "right", "right", "up"] as const) {
      state = gameReducer(state, { type: "move", direction });
    }
    expect(actorById(state, "gearshift")).toMatchObject({ x: 6, y: 3 });
    expect(state.combat?.movesLeft).toBe(0);
    const stuck = gameReducer(state, { type: "move", direction: "left" });
    expect(stuck.notice?.kind).toBe("no-moves");
    expect(actorById(stuck, "gearshift")).toMatchObject({ x: 6, y: 3 });
    expect(activeCombatant(stuck)?.id).toBe("gearshift");
    const passed = gameReducer(stuck, { type: "endTurn" });
    expect(activeCombatant(passed)?.id).toBe("oogrish");
    expect(passed.combat?.movesLeft).toBe(4);
  });

  it("rolls an attack when a hero walks into an enemy, then ends that hero's turn", () => {
    const board = roomBoard({
      features: ["movement", "melee"],
      actors: [
        { id: "near", kind: "enemy", ref: "sparring-bot", x: 4, y: 3 },
        { id: "far", kind: "enemy", ref: "sparring-bot", x: 7, y: 1 },
      ],
    });
    const state = withTurn(startCombat(createGame(board, testData)), ["gearshift", "near", "far", "oogrish"]);
    const after = gameReducer(state, { type: "move", direction: "right" });
    expect(actorById(after, "gearshift")).toMatchObject({ x: 3, y: 3 });
    const lines = after.log.slice(state.log.length);
    expect(lines[0]).toMatch(
      /^Gearshift swings his longsword: rolls \d+ \+ 5 = \d+ vs Defense 11\. (Miss!|Hit! \d+ damage\.|Critical hit! \d+ damage\.|A natural 1 always misses\.)$/,
    );
    const near = actorById(after, "near");
    const dealt = Number(lines[0].match(/(\d+) damage/)?.[1] ?? 0);
    expect(near?.hp).toBe(Math.max(0, 9 - dealt));
    expect(near?.down).toBe(near?.hp === 0);
    expect(activeCombatant(after)?.id).toBe(near?.down ? "far" : "near");
  });

  it("rolls the same attack for the same seed", () => {
    const board = roomBoard({
      features: ["movement", "melee"],
      actors: [{ id: "near", kind: "enemy", ref: "sparring-bot", x: 4, y: 3 }],
      seed: 11,
    });
    const play = () =>
      gameReducer(withTurn(startCombat(createGame(board, testData)), ["gearshift", "near", "oogrish"]), {
        type: "move",
        direction: "right",
      }).log;
    expect(play()).toEqual(play());
  });

  it("moves enemies toward the party and attacks when they are next to a hero", () => {
    const board = roomBoard({
      features: ["movement", "melee"],
      actors: [{ id: "bot", kind: "enemy", ref: "sparring-bot", x: 7, y: 3 }],
    });
    const state = withTurn(startCombat(createGame(board, testData)), ["bot", "gearshift", "oogrish"]);
    const after = runEnemyTurns(state);
    const bot = actorById(after, "bot");
    expect(bot).toMatchObject({ x: 4, y: 3 });
    expect(after.log.some((line) => line.startsWith("Sparring Bot jabs with its piston arm"))).toBe(true);
    expect(activeCombatant(after)?.id).toBe("gearshift");
  });

  it("plays a whole sparring match to victory and meets the defeat goal", () => {
    const won = fight(startCombat(createGame(sparBoard(), testData)));
    expect(won.combatResult).toBe("victory");
    expect(won.mode).toBe("explore");
    expect(won.goalMet).toBe(true);
    expect(aliveEnemies(won)).toHaveLength(0);
    expect(won.log.filter((line) => line.endsWith("powers down."))).toHaveLength(2);
    expect(won.actors.filter((actor) => actor.kind === "hero").every((hero) => !hero.down && hero.hp >= 1)).toBe(true);
  });

  it("ends in defeat when every hero is knocked out", () => {
    const board = roomBoard({
      features: ["movement", "melee"],
      actors: [{ id: "brute", kind: "enemy", ref: "brute", x: 6, y: 3 }],
    });
    const lost = fight(startCombat(createGame(board, testData)));
    expect(lost.mode).toBe("defeat");
    expect(lost.combatResult).toBe("defeat");
    expect(lost.goalMet).toBe(false);
    expect(lost.log.at(-1)).toBe("The party is knocked out.");
  });
});
