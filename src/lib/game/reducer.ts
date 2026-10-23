import { activeCombatant, combatMove, endTurn, enemyStep } from "./combat";
import { cutsceneStep } from "./cutscene";
import { advanceDialogue, chooseOption } from "./dialogue";
import { stepParty, swapLeader } from "./movement";
import { mergeFeatures } from "./state";
import type { GameAction, GameState } from "./types";

function apply(state: GameState, action: GameAction): GameState {
  switch (action.type) {
    case "move":
      if (state.mode === "combat") return combatMove(state, action.direction);
      return stepParty(state, action.direction);
    case "scriptedMove":
      return stepParty(state, action.direction, true);
    case "swapLeader":
      return swapLeader(state);
    case "choose":
      return chooseOption(state, action.index);
    case "advanceDialogue":
      return advanceDialogue(state);
    case "endTurn":
      return activeCombatant(state)?.kind === "hero" ? endTurn(state) : state;
    case "enemyStep":
      return enemyStep(state);
    case "cutsceneStep":
      return cutsceneStep(state);
    case "setFeatures":
      return { ...state, features: mergeFeatures(action.features) };
    case "clearNotice":
      return { ...state, notice: null };
  }
}

export function gameReducer(state: GameState, action: GameAction): GameState {
  const next = apply(state, action);
  return next === state ? state : { ...next, tick: state.tick + 1 };
}

export function playActions(state: GameState, actions: readonly GameAction[]): GameState {
  return actions.reduce(gameReducer, state);
}
