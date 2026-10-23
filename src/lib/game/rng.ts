export type Roll = { value: number; rng: number };

export function seedRng(seed: number): number {
  return seed >>> 0 || 1;
}

export function nextFloat(rng: number): { value: number; rng: number } {
  const next = (rng + 0x6d2b79f5) >>> 0;
  let t = next;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  const value = ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  return { value, rng: next };
}

export function rollDie(rng: number, sides: number): Roll {
  const { value, rng: next } = nextFloat(rng);
  return { value: Math.floor(value * sides) + 1, rng: next };
}
