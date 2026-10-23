import { campaignData } from "../campaign/registry";
import { boardSchema, enemySchema, mapSchema, type Board } from "./schema";
import type { CampaignData } from "./types";

export const testData: CampaignData = {
  ...campaignData,
  maps: {
    ...campaignData.maps,
    room: mapSchema.parse({
      id: "room",
      name: "Test room",
      sky: "day",
      rows: ["#########", "#.......#", "#...T...#", "#.......#", "#.......#", "#########"],
      legend: { "#": "wall", ".": "floor", T: "tree" },
    }),
  },
  enemies: {
    ...campaignData.enemies,
    brute: enemySchema.parse({
      id: "brute",
      name: "Test Brute",
      description: "Hits very hard.",
      hp: 200,
      defense: 30,
      attackBonus: 40,
      damageDie: 12,
      damageBonus: 40,
      speed: 6,
      dexterity: 30,
      aggroRange: 8,
      attackName: "Slam",
      verb: "slams",
      downText: "powers down",
      sprite: "/sprites/sparring-bot.svg",
    }),
  },
};

export function roomBoard(overrides: Partial<Board> = {}): Board {
  return boardSchema.parse({
    map: "room",
    party: ["gearshift", "oogrish"],
    partyStart: [
      { x: 3, y: 3 },
      { x: 2, y: 3 },
    ],
    features: ["movement"],
    ...overrides,
  });
}
