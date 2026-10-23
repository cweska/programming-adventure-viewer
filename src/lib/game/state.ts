import { seedRng } from "./rng";
import { heroStats } from "./rules";
import type { Board, Dialogue, Feature } from "./schema";
import type { Actor, CampaignData, GameState } from "./types";

function lookup<T>(table: Record<string, T>, id: string, kind: string): T {
  const value = table[id];
  if (!value) throw new Error(`Unknown ${kind} "${id}".`);
  return value;
}

export function mergeFeatures(...lists: readonly (readonly Feature[])[]): Feature[] {
  return [...new Set(lists.flat())];
}

export function createGame(board: Board, data: CampaignData, extraFeatures: readonly Feature[] = []): GameState {
  const map = lookup(data.maps, board.map, "map");
  const tiles = map.rows.map((row) => [...row].map((symbol) => lookup(map.legend, symbol, "tile")));

  const heroes: Actor[] = board.party.map((id, index) => {
    const character = lookup(data.characters, id, "character");
    const characterClass = lookup(data.classes, character.classId, "class");
    const stats = heroStats(character, characterClass);
    const start = board.partyStart[index] ?? board.partyStart[0];
    return {
      id,
      kind: "hero",
      ref: id,
      name: character.name,
      sprite: character.sprite,
      x: start.x,
      y: start.y,
      facing: "right",
      hp: stats.maxHp,
      maxHp: stats.maxHp,
      defense: stats.defense,
      attackBonus: stats.attackBonus,
      damageDie: character.weapon.damageDie,
      damageBonus: stats.damageBonus,
      speed: stats.speed,
      dexterity: character.abilities.dexterity,
      attackText: character.weapon.verb,
      downText: "is knocked out",
      aggroRange: 0,
      dialogue: null,
      down: false,
    };
  });

  const refCounts = new Map<string, number>();
  for (const actor of board.actors) refCounts.set(actor.ref, (refCounts.get(actor.ref) ?? 0) + 1);
  const seen = new Map<string, number>();

  const others: Actor[] = board.actors.map((placed) => {
    const number = (seen.get(placed.ref) ?? 0) + 1;
    seen.set(placed.ref, number);
    const suffix = (refCounts.get(placed.ref) ?? 0) > 1 ? ` ${number}` : "";
    if (placed.kind === "npc") {
      const npc = lookup(data.npcs, placed.ref, "NPC");
      return {
        id: placed.id,
        kind: "npc",
        ref: placed.ref,
        name: `${npc.name}${suffix}`,
        sprite: npc.sprite,
        x: placed.x,
        y: placed.y,
        facing: "left",
        hp: 1,
        maxHp: 1,
        defense: 10,
        attackBonus: 0,
        damageDie: 4,
        damageBonus: 0,
        speed: 0,
        dexterity: 10,
        attackText: "",
        downText: "",
        aggroRange: 0,
        dialogue: placed.dialogue ?? null,
        down: false,
      };
    }
    const enemy = lookup(data.enemies, placed.ref, "enemy");
    return {
      id: placed.id,
      kind: "enemy",
      ref: placed.ref,
      name: `${enemy.name}${suffix}`,
      sprite: enemy.sprite,
      x: placed.x,
      y: placed.y,
      facing: "left",
      hp: enemy.hp,
      maxHp: enemy.hp,
      defense: enemy.defense,
      attackBonus: enemy.attackBonus,
      damageDie: enemy.damageDie,
      damageBonus: enemy.damageBonus,
      speed: enemy.speed,
      dexterity: enemy.dexterity,
      attackText: enemy.verb,
      downText: enemy.downText,
      aggroRange: enemy.aggroRange,
      dialogue: placed.dialogue ?? null,
      down: false,
    };
  });

  const dialogues: Record<string, Dialogue> = {};
  for (const actor of others) {
    if (actor.dialogue) dialogues[actor.dialogue] = lookup(data.dialogues, actor.dialogue, "dialogue");
  }

  return {
    map: {
      id: map.id,
      name: map.name,
      sky: map.sky,
      width: tiles[0]?.length ?? 0,
      height: tiles.length,
      tiles,
    },
    actors: [...heroes, ...others],
    party: [...board.party],
    leader: board.party[0],
    features: mergeFeatures(board.features, extraFeatures),
    mode: "explore",
    dialogue: null,
    dialogues,
    combat: null,
    combatResult: null,
    goal: board.goal ?? null,
    goalMet: false,
    talkedTo: [],
    rng: seedRng(board.seed),
    log: [],
    notice: null,
    tick: 0,
  };
}
