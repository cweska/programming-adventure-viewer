import { maxManaFor } from "../game/barrier";
import type { CampaignData } from "../game/types";
import { campaignData } from "./registry";

export type PartyMember = {
  character_name: string;
  race: string;
  alignment: string;
  abilities: Record<string, number>;
  skills: string[];
  inventory: string[];
  mana: number;
  max_mana: number;
  spell_book: Record<string, never>;
};

export function partyMembers(
  ids: readonly string[],
  mana: Readonly<Record<string, number>>,
  data: CampaignData = campaignData,
): PartyMember[] {
  return ids.map((id) => {
    const character = data.characters[id];
    if (!character) throw new Error(`Unknown character "${id}".`);
    const max = maxManaFor(character.abilities.magical_affinity);
    return {
      character_name: character.name,
      race: character.species,
      alignment: character.alignment,
      abilities: { ...character.abilities },
      skills: [...character.skills.innate, ...character.skills.martial, ...character.skills.magical],
      inventory: character.inventory.map((item) => item.name),
      mana: Math.min(mana[id] ?? max, max),
      max_mana: max,
      spell_book: {},
    };
  });
}

export function partySetupCode(ids: readonly string[], mana: Readonly<Record<string, number>>): string {
  const json = JSON.stringify(partyMembers(ids, mana));
  return `import json as _json\nparty.members = _json.loads(${JSON.stringify(json)})\n`;
}

export function characterIdByName(name: string, data: CampaignData = campaignData): string | undefined {
  return Object.values(data.characters).find((character) => character.name === name)?.id;
}
