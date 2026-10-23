import { describe, expect, it } from "vitest";
import { roomBoard, testData } from "./fixtures";
import { playActions } from "./reducer";
import type { Direction } from "./schema";
import { createGame } from "./state";
import type { GameAction, GameState } from "./types";
import { actorById } from "./world";

function where(state: GameState, id: string) {
  const actor = actorById(state, id);
  return actor ? { x: actor.x, y: actor.y } : null;
}

function moves(...directions: Direction[]): GameAction[] {
  return directions.map((direction) => ({ type: "move", direction }));
}

describe("party movement", () => {
  it("steps the leader one tile in each direction", () => {
    const start = createGame(roomBoard(), testData);
    expect(where(start, "gearshift")).toEqual({ x: 3, y: 3 });
    expect(where(playActions(start, moves("right")), "gearshift")).toEqual({ x: 4, y: 3 });
    expect(where(playActions(start, moves("up")), "gearshift")).toEqual({ x: 3, y: 2 });
    expect(where(playActions(start, moves("down")), "gearshift")).toEqual({ x: 3, y: 4 });
    expect(where(playActions(start, moves("left")), "gearshift")).toEqual({ x: 2, y: 3 });
  });

  it("has the follower step into the tile the leader left", () => {
    const state = playActions(createGame(roomBoard(), testData), moves("right", "right", "down"));
    expect(where(state, "gearshift")).toEqual({ x: 5, y: 4 });
    expect(where(state, "oogrish")).toEqual({ x: 5, y: 3 });
  });

  it("swaps places when the leader walks back into the follower", () => {
    const state = playActions(createGame(roomBoard(), testData), moves("left"));
    expect(where(state, "gearshift")).toEqual({ x: 2, y: 3 });
    expect(where(state, "oogrish")).toEqual({ x: 3, y: 3 });
  });

  it("stops at walls, trees, and the edge of the map", () => {
    const start = createGame(roomBoard(), testData);
    expect(where(playActions(start, moves("up", "up", "up", "up")), "gearshift")).toEqual({ x: 3, y: 1 });
    expect(where(playActions(start, moves("right", "up")), "gearshift")).toEqual({ x: 4, y: 3 });
    const corner = createGame(roomBoard({ partyStart: [{ x: 0, y: 0 }, { x: 1, y: 1 }] }), testData);
    expect(where(playActions(corner, moves("left", "up")), "gearshift")).toEqual({ x: 0, y: 0 });
  });

  it("treats a person as a wall and opens their dialogue when talking is unlocked", () => {
    const board = roomBoard({
      actors: [{ id: "keeper", kind: "npc", ref: "arena-keeper", x: 4, y: 3, dialogue: "arena-keeper-welcome" }],
    });
    const locked = playActions(createGame(board, testData), moves("right"));
    expect(where(locked, "gearshift")).toEqual({ x: 3, y: 3 });
    expect(locked.notice?.kind).toBe("dialogue-locked");
    expect(locked.mode).toBe("explore");

    const open = playActions(createGame(board, testData, ["dialogue"]), moves("right"));
    expect(where(open, "gearshift")).toEqual({ x: 3, y: 3 });
    expect(open.mode).toBe("dialogue");
  });

  it("switches the leader with Tab so the other hero walks in front", () => {
    const state = playActions(createGame(roomBoard(), testData), [{ type: "swapLeader" }, ...moves("down")]);
    expect(state.leader).toBe("oogrish");
    expect(where(state, "oogrish")).toEqual({ x: 2, y: 4 });
    expect(where(state, "gearshift")).toEqual({ x: 2, y: 3 });
  });

  it("refuses to move until movement is unlocked, but lets Python's scripted steps through", () => {
    const start = createGame(roomBoard({ features: [] }), testData);
    const locked = playActions(start, moves("right"));
    expect(where(locked, "gearshift")).toEqual({ x: 3, y: 3 });
    expect(locked.notice?.kind).toBe("movement-locked");

    const scripted = playActions(start, [
      { type: "scriptedMove", direction: "right" },
      { type: "scriptedMove", direction: "down" },
    ]);
    expect(where(scripted, "gearshift")).toEqual({ x: 4, y: 4 });

    const unlocked = playActions(start, [{ type: "setFeatures", features: ["movement"] }, ...moves("right")]);
    expect(where(unlocked, "gearshift")).toEqual({ x: 4, y: 3 });
    expect(unlocked.notice).toBeNull();
  });

  it("meets a reach goal when the leader steps on it", () => {
    const board = roomBoard({ goal: { type: "reach", x: 5, y: 3, label: "the spot" } });
    const halfway = playActions(createGame(board, testData), moves("right"));
    expect(halfway.goalMet).toBe(false);
    const there = playActions(halfway, moves("right"));
    expect(there.goalMet).toBe(true);
    expect(playActions(there, moves("right")).goalMet).toBe(true);
  });
});
