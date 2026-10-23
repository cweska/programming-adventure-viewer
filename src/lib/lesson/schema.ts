import { z } from "zod";
import { boardSchema, featureSchema } from "../game/schema";

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
});

export const beatSchema = z
  .object({
    id: z.string().min(1),
    scene: sceneSchema,
    instructions: z.string().min(1),
    editor: z.enum(["hidden", "visible"]).optional(),
    board: boardSchema.optional(),
    activity: activitySchema.optional(),
  })
  .refine((beat) => beat.scene.images.length > 0 || Boolean(beat.board), {
    message: "A part needs at least one scene image or a game board.",
    path: ["scene", "images"],
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
export type Beat = z.infer<typeof beatSchema>;
export type Lesson = z.infer<typeof lessonSchema>;
export type Module = z.infer<typeof moduleSchema>;

export function requiresPass(beat: Beat): boolean {
  return Boolean(beat.activity) || Boolean(beat.board?.goal);
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
