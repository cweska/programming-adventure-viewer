import { describe, expect, it } from "vitest";
import { campaignData } from "../campaign/registry";
import { insideBarrier } from "./barrier";
import { playActions } from "./reducer";
import { boardSchema } from "./schema";
import { createGame } from "./state";
import type { GameState } from "./types";

const PARTY = ["oogrish", "gearshift", "bomb-shell", "lucky"];

function barrierBoard() {
  return boardSchema.parse({
    map: "moonlit-hills",
    party: PARTY,
    partyStart: [
      { x: 9, y: 5 },
      { x: 10, y: 5 },
      { x: 12, y: 5 },
      { x: 13, y: 5 },
    ],
    actors: [{ id: "mar-tu", kind: "npc", ref: "mar-tu", x: 11, y: 4 }],
    features: [],
    goal: { type: "barrier" },
    casting: {
      spell: "Strengthen Magic",
      mana: { oogrish: 18, gearshift: 15, "bomb-shell": 14, lucky: 19 },
      lines: { oogrish: "Steady, now.", gearshift: "Barrier's holding.", "bomb-shell": "Shield up.", lucky: "Don't try to mog while I'm shieldmaxxing." },
    },
    barrier: { x0: 7, x1: 15, y0: 0, y1: 6 },
  });
}

function castAll(state: GameState): GameState {
  return playActions(
    state,
    PARTY.map((actorId) => ({ type: "cast", actorId })),
  );
}

describe("holding the barrier", () => {
  it("starts with each hero's mana from the outline and an empty barrier", () => {
    const state = createGame(barrierBoard(), campaignData);
    expect(state.mana).toEqual({
      oogrish: { mana: 18, max: 18 },
      gearshift: { mana: 15, max: 20 },
      "bomb-shell": { mana: 14, max: 24 },
      lucky: { mana: 19, max: 26 },
    });
    expect(state.barrier).toMatchObject({ level: 0, casters: [], locked: false, wave: 0, done: false });
    expect(insideBarrier(state, 9, 5)).toBe(true);
    expect(insideBarrier(state, 2, 5)).toBe(false);
  });

  it("thickens once per new caster, says their line, and locks after all four", () => {
    let state = createGame(barrierBoard(), campaignData);
    state = playActions(state, [{ type: "cast", actorId: "oogrish" }]);
    expect(state.barrier?.level).toBe(1);
    expect(state.speech?.text).toBe("Steady, now.");
    state = playActions(state, [{ type: "cast", actorId: "oogrish" }]);
    expect(state.barrier?.level).toBe(1);
    expect(state.barrier?.locked).toBe(false);
    state = castAll(state);
    expect(state.barrier).toMatchObject({ level: 4, locked: true });
    expect(state.speech?.text).toBe("Don't try to mog while I'm shieldmaxxing.");
  });

  it("records mana changes and how much a cast spent", () => {
    const state = playActions(createGame(barrierBoard(), campaignData), [
      { type: "manaChanged", actorId: "lucky", mana: 9, max: 26 },
    ]);
    expect(state.mana.lucky).toEqual({ mana: 9, max: 26 });
    expect(state.manaDrop).toMatchObject({ actorId: "lucky", amount: 10 });
  });

  it("shows the student's own message for a failed cast", () => {
    const state = playActions(createGame(barrierBoard(), campaignData), [
      { type: "prompt", text: "Lucky doesn't have enough mana to cast Strengthen Magic." },
    ]);
    expect(state.prompt?.text).toBe("Lucky doesn't have enough mana to cast Strengthen Magic.");
  });

  it("only rolls the wave after the barrier locks, then meets the goal when it leaves the map", () => {
    let state = createGame(barrierBoard(), campaignData);
    expect(playActions(state, [{ type: "waveStep" }]).barrier?.wave).toBe(0);
    state = castAll(state);
    for (let step = 0; step < state.map.width + 1; step += 1) {
      state = playActions(state, [{ type: "waveStep" }]);
      expect(state.goalMet).toBe(false);
    }
    state = playActions(state, [{ type: "waveStep" }]);
    expect(state.barrier?.done).toBe(true);
    expect(state.goalMet).toBe(true);
    expect(playActions(state, [{ type: "waveStep" }]).barrier?.wave).toBe(state.barrier?.wave);
  });

  it("keeps the party from walking out of the barrier", () => {
    const state = playActions(createGame(barrierBoard(), campaignData), [{ type: "move", direction: "down" }]);
    expect(state.actors.find((actor) => actor.id === "oogrish")).toMatchObject({ x: 9, y: 5 });
  });
});
