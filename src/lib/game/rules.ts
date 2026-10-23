import type { Character, CharacterClass, Tile } from "./schema";

const WALKABLE: ReadonlySet<Tile> = new Set<Tile>(["grass", "flowers", "path", "floor", "sand", "door"]);

export const PROFICIENCY = 2;

export function isWalkable(tile: Tile | undefined): boolean {
  return tile !== undefined && WALKABLE.has(tile);
}

export function modifier(score: number): number {
  return Math.floor((score - 10) / 2);
}

export function formatModifier(value: number): string {
  return value >= 0 ? `+${value}` : `${value}`;
}

export type HeroStats = {
  maxHp: number;
  defense: number;
  attackBonus: number;
  damageBonus: number;
  speed: number;
  initiativeBonus: number;
};

export function heroStats(character: Character, characterClass: CharacterClass): HeroStats {
  const { strength, constitution, athletics, dexterity } = character.abilities;
  return {
    maxHp: characterClass.baseHp + modifier(constitution),
    defense: 10 + modifier(dexterity) + character.armor.bonus,
    attackBonus: modifier(strength) + PROFICIENCY,
    damageBonus: modifier(strength),
    speed: Math.max(2, 4 + Math.floor(modifier(athletics) / 2)),
    initiativeBonus: modifier(dexterity),
  };
}

export type AttackOutcome = {
  natural: number;
  total: number;
  hit: boolean;
  critical: boolean;
};

export function resolveAttack(natural: number, attackBonus: number, defense: number): AttackOutcome {
  const total = natural + attackBonus;
  if (natural === 20) return { natural, total, hit: true, critical: true };
  if (natural === 1) return { natural, total, hit: false, critical: false };
  return { natural, total, hit: total >= defense, critical: false };
}

export function damageTotal(dice: number[], bonus: number): number {
  return Math.max(1, dice.reduce((sum, die) => sum + die, 0) + bonus);
}
