import { describe, expect, it } from "vitest";
import { campaignData } from "../campaign/registry";
import { runCutscene } from "./cutscene";
import { playActions } from "./reducer";
import { boardSchema, type Direction, type Feature } from "./schema";
import { createGame } from "./state";
import type { GameAction, GameState } from "./types";
import { actorById } from "./world";

function cabinBoard(features: Feature[]) {
  return boardSchema.parse({
    map: "moonlit-hills",
    party: ["oogrish", "gearshift"],
    partyStart: [
      { x: 3, y: 5 },
      { x: 2, y: 5 },
    ],
    actors: [{ id: "mar-tu", kind: "npc", ref: "mar-tu", x: 12, y: 4 }],
    features,
    goal: { type: "reach", x: 11, y: 3, label: "the cabin door", enter: { after: ["mar-tu"] } },
  });
}

const TO_DOOR: Direction[] = ["right", "right", "right", "right", "right", "right", "right", "right", "up", "up"];

function walk(state: GameState, directions: Direction[], type: "move" | "scriptedMove" = "move"): GameState {
  return playActions(
    state,
    directions.map((direction): GameAction => ({ type, direction })),
  );
}

describe("entering a door", () => {
  it("hands control to a cutscene when the leader reaches the door", () => {
    const state = walk(createGame(cabinBoard(["movement"]), campaignData), TO_DOOR);
    expect(actorById(state, "oogrish")).toMatchObject({ x: 11, y: 3 });
    expect(state.mode).toBe("cutscene");
    expect(state.goalMet).toBe(false);
    expect(state.cutscene?.queue).toEqual(["oogrish", "gearshift", "mar-tu"]);

    const ignored = walk(state, ["down", "left"]);
    expect(actorById(ignored, "oogrish")).toMatchObject({ x: 11, y: 3 });
    expect(playActions(state, [{ type: "swapLeader" }]).leader).toBe("oogrish");
  });

  it("walks the party and then Mar'tu through the door before closing it", () => {
    let state = walk(createGame(cabinBoard(["movement"]), campaignData), TO_DOOR);
    const hiddenOrder: string[] = [];
    for (let step = 0; step < 50 && !state.cutscene?.doorClosed; step += 1) {
      state = playActions(state, [{ type: "cutsceneStep" }]);
      for (const actor of state.actors) {
        if (actor.hidden && !hiddenOrder.includes(actor.id)) hiddenOrder.push(actor.id);
      }
      if (!state.cutscene?.doorClosed) expect(state.goalMet).toBe(false);
    }
    expect(hiddenOrder).toEqual(["oogrish", "gearshift", "mar-tu"]);
    expect(state.cutscene?.doorClosed).toBe(true);
    expect(state.goalMet).toBe(true);
    expect(state.actors.every((actor) => actor.hidden)).toBe(true);
  });

  it("does not count the door until movement has been programmed", () => {
    const scripted = walk(createGame(cabinBoard([]), campaignData), TO_DOOR, "scriptedMove");
    expect(actorById(scripted, "oogrish")).toMatchObject({ x: 11, y: 3 });
    expect(scripted.mode).toBe("explore");
    expect(scripted.goalMet).toBe(false);

    const unlocked = walk(createGame(cabinBoard(["movement"]), campaignData), TO_DOOR, "scriptedMove");
    expect(runCutscene(unlocked).goalMet).toBe(true);
  });
});
