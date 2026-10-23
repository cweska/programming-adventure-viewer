import { describe, expect, it } from "vitest";
import { currentNode } from "./dialogue";
import { roomBoard, testData } from "./fixtures";
import { playActions } from "./reducer";
import { createGame } from "./state";

function talkingBoard() {
  return roomBoard({
    features: ["movement", "dialogue"],
    actors: [{ id: "keeper", kind: "npc", ref: "arena-keeper", x: 4, y: 3, dialogue: "arena-keeper-welcome" }],
    goal: { type: "talk", actor: "keeper" },
  });
}

describe("dialogue", () => {
  it("starts when the leader walks into a person", () => {
    const state = playActions(createGame(talkingBoard(), testData), [{ type: "move", direction: "right" }]);
    expect(state.mode).toBe("dialogue");
    expect(state.dialogue).toEqual({ actorId: "keeper", treeId: "arena-keeper-welcome", nodeId: "hello" });
    expect(currentNode(state)?.options).toHaveLength(3);
  });

  it("follows the chosen option and ignores options that do not exist", () => {
    const talking = playActions(createGame(talkingBoard(), testData), [
      { type: "move", direction: "right" },
      { type: "choose", index: 0 },
    ]);
    expect(talking.dialogue?.nodeId).toBe("talking");
    expect(playActions(talking, [{ type: "choose", index: 5 }]).dialogue?.nodeId).toBe("talking");
    expect(playActions(talking, [{ type: "advanceDialogue" }]).dialogue?.nodeId).toBe("talking");
    expect(playActions(talking, [{ type: "move", direction: "down" }]).dialogue?.nodeId).toBe("talking");
  });

  it("ends on a closing line and meets the talk goal", () => {
    const end = playActions(createGame(talkingBoard(), testData), [
      { type: "move", direction: "right" },
      { type: "choose", index: 0 },
      { type: "choose", index: 1 },
    ]);
    expect(end.dialogue?.nodeId).toBe("bye");
    expect(end.goalMet).toBe(false);
    const done = playActions(end, [{ type: "advanceDialogue" }]);
    expect(done.mode).toBe("explore");
    expect(done.dialogue).toBeNull();
    expect(done.talkedTo).toEqual(["keeper"]);
    expect(done.goalMet).toBe(true);
  });

  it("says when someone has nothing to say", () => {
    const board = roomBoard({
      features: ["movement", "dialogue"],
      actors: [{ id: "mar-tu", kind: "npc", ref: "mar-tu", x: 4, y: 3 }],
    });
    const state = playActions(createGame(board, testData), [{ type: "move", direction: "right" }]);
    expect(state.mode).toBe("explore");
    expect(state.notice).toMatchObject({ kind: "nothing-to-say", text: "Mar'Tu has nothing to say right now." });
  });
});
