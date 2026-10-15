import { z } from "zod";

export const imageSchema = z.object({
  id: z.string().min(1).optional(),
  src: z.string().min(1),
  alt: z.string().min(1),
});

export const sceneSchema = z.object({
  images: z.array(imageSchema).min(1),
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
});

export const beatSchema = z.object({
  id: z.string().min(1),
  scene: sceneSchema,
  instructions: z.string().min(1),
  activity: activitySchema.optional(),
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

export function formatSchemaError(error: z.ZodError): string {
  return error.issues
    .map((issue) => {
      const path = issue.path.length > 0 ? issue.path.join(".") : "module";
      return `${path}: ${issue.message}`;
    })
    .join("\n");
}
