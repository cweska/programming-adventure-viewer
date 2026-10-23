import gearshift from "../../../content/campaign/characters/gearshift.json";
import oogrish from "../../../content/campaign/characters/oogrish.json";
import general from "../../../content/campaign/classes/general.json";
import warrior from "../../../content/campaign/classes/warrior.json";
import arenaKeeperWelcome from "../../../content/campaign/dialogue/arena-keeper-welcome.json";
import sparringBot from "../../../content/campaign/enemies/sparring-bot.json";
import moonlitHills from "../../../content/campaign/maps/moonlit-hills.json";
import trainingYard from "../../../content/campaign/maps/training-yard.json";
import arenaKeeper from "../../../content/campaign/npcs/arena-keeper.json";
import marTu from "../../../content/campaign/npcs/mar-tu.json";
import type { z } from "zod";
import {
  characterSchema,
  classSchema,
  dialogueSchema,
  enemySchema,
  mapSchema,
  npcSchema,
} from "../game/schema";
import type { CampaignData } from "../game/types";

function byId<T extends { id: string }>(schema: z.ZodType<T, z.ZodTypeDef, unknown>, raws: unknown[]): Record<string, T> {
  const entries: Record<string, T> = {};
  for (const raw of raws) {
    const parsed = schema.parse(raw);
    if (entries[parsed.id]) throw new Error(`Duplicate campaign id "${parsed.id}".`);
    entries[parsed.id] = parsed;
  }
  return entries;
}

export const campaignData: CampaignData = {
  characters: byId(characterSchema, [gearshift, oogrish]),
  classes: byId(classSchema, [warrior, general]),
  npcs: byId(npcSchema, [marTu, arenaKeeper]),
  enemies: byId(enemySchema, [sparringBot]),
  maps: byId(mapSchema, [moonlitHills, trainingYard]),
  dialogues: byId(dialogueSchema, [arenaKeeperWelcome]),
};
