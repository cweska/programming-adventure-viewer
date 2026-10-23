import type { DialogueNode } from "./schema";
import type { Actor, GameState } from "./types";
import { hasFeature, notify } from "./world";

export function startDialogue(state: GameState, actor: Actor): GameState {
  if (!hasFeature(state, "dialogue")) return notify(state, "dialogue-locked");
  const tree = actor.dialogue ? state.dialogues[actor.dialogue] : undefined;
  if (!tree) return notify(state, "nothing-to-say", `${actor.name} has nothing to say right now.`);
  return {
    ...state,
    mode: "dialogue",
    notice: null,
    dialogue: { actorId: actor.id, treeId: tree.id, nodeId: tree.start },
  };
}

export function currentNode(state: GameState): DialogueNode | null {
  if (!state.dialogue) return null;
  return state.dialogues[state.dialogue.treeId]?.nodes[state.dialogue.nodeId] ?? null;
}

function goTo(state: GameState, next: string | null | undefined): GameState {
  const conversation = state.dialogue;
  if (!conversation) return state;
  if (next) return { ...state, dialogue: { ...conversation, nodeId: next } };
  const talkedTo = state.talkedTo.includes(conversation.actorId)
    ? state.talkedTo
    : [...state.talkedTo, conversation.actorId];
  const finishesGoal = state.goal?.type === "talk" && state.goal.actor === conversation.actorId;
  return {
    ...state,
    mode: "explore",
    dialogue: null,
    talkedTo,
    goalMet: state.goalMet || finishesGoal,
  };
}

export function chooseOption(state: GameState, index: number): GameState {
  if (state.mode !== "dialogue") return state;
  const option = currentNode(state)?.options?.[index];
  if (!option) return state;
  return goTo(state, option.next);
}

export function advanceDialogue(state: GameState): GameState {
  if (state.mode !== "dialogue") return state;
  const node = currentNode(state);
  if (!node || node.options) return state;
  return goTo(state, node.next);
}
