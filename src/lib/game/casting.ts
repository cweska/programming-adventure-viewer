import type { StageEvent } from "../stage/bridge";
import type { GameAction } from "./types";

/**
 * Turns what the student's cast_spell() did into game actions: a landed
 * spell, a new mana total, or the message the student printed instead.
 * Events about someone who is not on the board are skipped.
 */
export function castActions(
  events: readonly StageEvent[],
  idByName: (name: string) => string | undefined,
): GameAction[] {
  return events.flatMap((event): GameAction[] => {
    if (event.type === "cast") {
      const actorId = idByName(event.name);
      return actorId ? [{ type: "cast", actorId }] : [];
    }
    if (event.type === "mana") {
      const actorId = idByName(event.name);
      return actorId ? [{ type: "manaChanged", actorId, mana: event.mana, max: event.max }] : [];
    }
    if (event.type === "prompt") return [{ type: "prompt", text: event.text }];
    return [];
  });
}
