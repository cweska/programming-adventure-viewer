import { z } from "zod";

export const featureSchema = z.enum(["movement", "dialogue", "melee"]);

export const directionSchema = z.enum(["left", "right", "up", "down"]);

export const tileSchema = z.enum([
  "grass",
  "flowers",
  "path",
  "floor",
  "sand",
  "door",
  "tree",
  "rock",
  "fence",
  "water",
  "wall",
  "roof",
  "window",
]);

const score = z.number().int().min(1).max(30);

export const abilitiesSchema = z
  .object({
    strength: score,
    constitution: score,
    athletics: score,
    dexterity: score,
    personality: score,
    perception: score,
    intelligence: score,
    wisdom: score,
    magical_affinity: score,
  })
  .strict();

const dieSchema = z.union([z.literal(4), z.literal(6), z.literal(8), z.literal(10), z.literal(12)]);

export const weaponSchema = z
  .object({
    name: z.string().min(1),
    damageDie: dieSchema,
    verb: z.string().min(1),
  })
  .strict();

export const itemSchema = z
  .object({
    name: z.string().min(1),
    kind: z.enum(["weapon", "armor", "relic", "supply"]),
    note: z.string().min(1).optional(),
  })
  .strict();

export const characterSchema = z
  .object({
    id: z.string().min(1),
    name: z.string().min(1),
    species: z.string().min(1),
    classId: z.string().min(1),
    alignment: z.string().min(1),
    size: z.string().min(1),
    appearance: z.string().min(1),
    personality: z.string().min(1),
    abilities: abilitiesSchema,
    skills: z
      .object({
        innate: z.array(z.string().min(1)),
        martial: z.array(z.string().min(1)),
        magical: z.array(z.string().min(1)),
      })
      .strict(),
    weakness: z.string().min(1),
    weapon: weaponSchema,
    armor: z.object({ name: z.string().min(1), bonus: z.number().int().min(0).max(6) }).strict(),
    inventory: z.array(itemSchema),
    faction: z.string().min(1),
    backstory: z.string().min(1),
    pastLife: z.string().min(1),
    sprite: z.string().startsWith("/"),
    portrait: z.string().startsWith("/"),
  })
  .strict();

export const classSchema = z
  .object({
    id: z.string().min(1),
    name: z.string().min(1),
    role: z.string().min(1),
    description: z.string().min(1),
    baseHp: z.number().int().min(1),
  })
  .strict();

export const npcSchema = z
  .object({
    id: z.string().min(1),
    name: z.string().min(1),
    pronouns: z.string().min(1),
    description: z.string().min(1),
    sprite: z.string().startsWith("/"),
    portrait: z.string().startsWith("/"),
  })
  .strict();

export const enemySchema = z
  .object({
    id: z.string().min(1),
    name: z.string().min(1),
    description: z.string().min(1),
    hp: z.number().int().min(1),
    defense: z.number().int().min(1),
    attackBonus: z.number().int(),
    damageDie: dieSchema,
    damageBonus: z.number().int(),
    speed: z.number().int().min(1),
    dexterity: score,
    aggroRange: z.number().int().min(0),
    attackName: z.string().min(1),
    verb: z.string().min(1),
    downText: z.string().min(1),
    sprite: z.string().startsWith("/"),
  })
  .strict();

export const mapSchema = z
  .object({
    id: z.string().min(1),
    name: z.string().min(1),
    sky: z.enum(["night", "day"]),
    rows: z.array(z.string().min(1)).min(1),
    legend: z.record(z.string().length(1), tileSchema),
  })
  .strict()
  .superRefine((map, ctx) => {
    const width = map.rows[0]?.length ?? 0;
    map.rows.forEach((row, y) => {
      if (row.length !== width) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["rows", y], message: `Row ${y} should be ${width} tiles wide.` });
      }
      for (const symbol of row) {
        if (!(symbol in map.legend)) {
          ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["rows", y], message: `"${symbol}" is not in the legend.` });
        }
      }
    });
  });

const dialogueOptionSchema = z
  .object({
    text: z.string().min(1),
    next: z.string().min(1).nullable(),
  })
  .strict();

export const dialogueNodeSchema = z
  .object({
    speaker: z.string().min(1),
    text: z.string().min(1),
    options: z.array(dialogueOptionSchema).min(1).max(9).optional(),
    next: z.string().min(1).nullable().optional(),
  })
  .strict();

export const dialogueSchema = z
  .object({
    id: z.string().min(1),
    start: z.string().min(1),
    nodes: z.record(z.string().min(1), dialogueNodeSchema),
  })
  .strict()
  .superRefine((tree, ctx) => {
    if (!(tree.start in tree.nodes)) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["start"], message: `Unknown start node "${tree.start}".` });
    }
    for (const [id, node] of Object.entries(tree.nodes)) {
      const targets = [node.next, ...(node.options ?? []).map((option) => option.next)];
      for (const target of targets) {
        if (target && !(target in tree.nodes)) {
          ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["nodes", id], message: `Unknown node "${target}".` });
        }
      }
    }
  });

export const positionSchema = z
  .object({
    x: z.number().int().min(0),
    y: z.number().int().min(0),
  })
  .strict();

export const boardActorSchema = z
  .object({
    id: z.string().min(1),
    kind: z.enum(["npc", "enemy"]),
    ref: z.string().min(1),
    x: z.number().int().min(0),
    y: z.number().int().min(0),
    dialogue: z.string().min(1).optional(),
  })
  .strict();

export const goalSchema = z.discriminatedUnion("type", [
  z
    .object({
      type: z.literal("reach"),
      x: z.number().int().min(0),
      y: z.number().int().min(0),
      label: z.string().min(1),
      enter: z.object({ after: z.array(z.string().min(1)) }).strict().optional(),
    })
    .strict(),
  z.object({ type: z.literal("talk"), actor: z.string().min(1) }).strict(),
  z.object({ type: z.literal("defeat") }).strict(),
]);

export const boardSchema = z
  .object({
    map: z.string().min(1),
    party: z.array(z.string().min(1)).min(1),
    partyStart: z.array(positionSchema).min(1),
    actors: z.array(boardActorSchema).default([]),
    features: z.array(featureSchema).default([]),
    goal: goalSchema.optional(),
    seed: z.number().int().default(1),
  })
  .strict()
  .refine((board) => board.party.length === board.partyStart.length, {
    message: "Every party member needs a start position.",
    path: ["partyStart"],
  });

export type Feature = z.infer<typeof featureSchema>;
export type Direction = z.infer<typeof directionSchema>;
export type Tile = z.infer<typeof tileSchema>;
export type Abilities = z.infer<typeof abilitiesSchema>;
export type Character = z.infer<typeof characterSchema>;
export type CharacterClass = z.infer<typeof classSchema>;
export type Npc = z.infer<typeof npcSchema>;
export type Enemy = z.infer<typeof enemySchema>;
export type GameMap = z.infer<typeof mapSchema>;
export type DialogueNode = z.infer<typeof dialogueNodeSchema>;
export type Dialogue = z.infer<typeof dialogueSchema>;
export type Position = z.infer<typeof positionSchema>;
export type BoardActor = z.infer<typeof boardActorSchema>;
export type Goal = z.infer<typeof goalSchema>;
export type Board = z.infer<typeof boardSchema>;
