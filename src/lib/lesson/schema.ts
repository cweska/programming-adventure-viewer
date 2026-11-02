import { z } from "zod";
import { boardSchema, featureSchema, manaTableSchema } from "../game/schema";

export const imageSchema = z.object({
  id: z.string().min(1).optional(),
  src: z.string().min(1),
  alt: z.string().min(1),
});

export const sceneSchema = z.object({
  images: z.array(imageSchema),
  video: z.string().min(1).optional(),
  narration: z.string().min(1).optional(),
  music: z.string().min(1).optional(),
  caption: z.string().min(1),
});

export const checkSchema = z.object({
  name: z.string().min(1),
  code: z.string().min(1),
});

export const activitySchema = z.object({
  kind: z.enum(["challenge", "interactive"]),
  starterCode: z.string(),
  passFeedback: z.string().min(1),
  failFeedback: z.string().min(1),
  checks: z.array(checkSchema).min(1),
  unlocks: z.array(featureSchema).optional(),
  party: z
    .object({ members: z.array(z.string().min(1)).min(1), mana: manaTableSchema })
    .strict()
    .optional(),
  background: z
    .array(z.object({ from: z.string().min(1), fallback: z.string().min(1) }).strict())
    .optional(),
});

export const conversationSchema = z
  .object({
    speaker: z.string().min(1),
    responder: z.string().min(1),
    showOptions: z.boolean(),
    promptFrom: z.string().min(1).optional(),
  })
  .strict();

export const skillCheckSchema = z
  .object({
    openImage: imageSchema,
    options: z
      .array(
        z
          .object({
            id: z.string().min(1),
            label: z.string().min(1),
            check: z.string().regex(/^[A-Za-z_][A-Za-z0-9_]*$/),
          })
          .strict(),
      )
      .min(1)
      .max(4),
    helper: z.object({ npc: z.string().min(1), line: z.string().min(1) }).strict(),
    success: z.string().min(1),
  })
  .strict();

export const spellBookSchema = z
  .object({
    spell: z.string().min(1),
    manaCost: z.number().int().min(0),
    requiredAffinity: z.number().int().min(0),
    success: z.string().min(1),
  })
  .strict();

export const partyPanelSchema = z
  .object({
    members: z.array(z.string().min(1)).min(1),
    success: z.string().min(1),
  })
  .strict();

export const beatSchema = z
  .object({
    id: z.string().min(1),
    scene: sceneSchema,
    instructions: z.string().min(1),
    editor: z.enum(["hidden", "visible"]).optional(),
    board: boardSchema.optional(),
    conversation: conversationSchema.optional(),
    skillCheck: skillCheckSchema.optional(),
    spellBook: spellBookSchema.optional(),
    partyPanel: partyPanelSchema.optional(),
    activity: activitySchema.optional(),
  })
  .refine((beat) => beat.scene.images.length > 0 || Boolean(beat.board), {
    message: "A part needs at least one scene image or a game board.",
    path: ["scene", "images"],
  })
  .refine(
    (beat) =>
      [beat.board, beat.conversation, beat.skillCheck, beat.spellBook, beat.partyPanel].filter(Boolean).length <= 1,
    {
      message: "A part shows at most one of: a game board, a conversation, a skill check, a spell book, a party panel.",
      path: ["scene"],
    },
  )
  .refine((beat) => !beat.skillCheck || Boolean(beat.activity), {
    message: "A skill check part needs code to run.",
    path: ["skillCheck"],
  });

export const lessonSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  published: z.boolean(),
  beats: z.array(beatSchema).min(1),
});

export const moduleSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  summary: z.string().min(1).optional(),
  campaign: z.object({ order: z.number().int(), label: z.string().min(1) }).optional(),
  language: z.literal("python"),
  lessons: z.array(lessonSchema).min(1),
});

export type SceneImage = z.infer<typeof imageSchema>;
export type Scene = z.infer<typeof sceneSchema>;
export type Check = z.infer<typeof checkSchema>;
export type Activity = z.infer<typeof activitySchema>;
export type Conversation = z.infer<typeof conversationSchema>;
export type SkillCheck = z.infer<typeof skillCheckSchema>;
export type SpellBook = z.infer<typeof spellBookSchema>;
export type PartyPanel = z.infer<typeof partyPanelSchema>;
export type Beat = z.infer<typeof beatSchema>;
export type Lesson = z.infer<typeof lessonSchema>;
export type Module = z.infer<typeof moduleSchema>;

export function requiresPass(beat: Beat): boolean {
  return Boolean(beat.activity) || Boolean(beat.board?.goal);
}

export function passesOnGoal(beat: Beat): boolean {
  return Boolean(beat.board?.goal) || Boolean(beat.skillCheck);
}

export function showsEditor(beat: Beat): boolean {
  return beat.editor !== "hidden";
}

export function formatSchemaError(error: z.ZodError): string {
  return error.issues
    .map((issue) => {
      const path = issue.path.length > 0 ? issue.path.join(".") : "module";
      return `${path}: ${issue.message}`;
    })
    .join("\n");
}
