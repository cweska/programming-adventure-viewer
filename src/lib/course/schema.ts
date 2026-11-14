import { z } from "zod";

/**
 * Content schema for the "Intro to Python" course (Mar'tu's lessons).
 *
 * Authored source: docs/intro-to-python/prototypes/uNN*_*.py (verified by harness.py), exported to
 * content/courses/intro-python/units/<unit-id>.json by scripts/course/export_prototypes.py.
 *
 * Code fields accept a string or an array of lines (joined with "\n", with a trailing newline).
 *
 * Prose fields (Mar'tu's explanations, checkpoint text, hints, article bodies) use a tiny format:
 *   - one paragraph per line ("\n" separates lines)
 *   - lines starting "1. ", "2. " ... render as a numbered list
 *   - `backticks` render as inline code
 *   - ```python fenced blocks``` render as code blocks
 *   - [[term]] or [[term|shown text]] link to the glossary
 *   - *words in stars* are emphasis (a star with a space after it stays a star: `5 * 3`)
 */

const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "ids are lower-case words joined by dashes");

export const codeSchema = z
  .union([z.string(), z.array(z.string())])
  .transform((value) => (Array.isArray(value) ? `${value.join("\n")}\n` : value));

const prose = z.string().min(1);

/** A concept token from the prototype harness (e.g. node:Assign, call:print, attr:append). */
const token = z.string().regex(/^(node|op|const|call|attr|import):[A-Za-z_]+$/);

export const courseCheckSchema = z.object({ name: z.string().min(1), code: codeSchema }).strict();

export const checkpointSchema = z
  .object({
    id: slug,
    /** One action. The UI numbers checkpoints, so no leading "1. ". */
    text: prose,
    /** The hint ladder: point -> teach -> show (2 to 5 rungs). Help shows them as Where to look, Teach me, Show me how. */
    hints: z.array(prose).min(2).max(5),
    checks: z.array(courseCheckSchema).min(1),
    /** A short in-world line shown when the checkpoint turns green. */
    passLine: z.string().optional(),
    /** True when the text spells out the code to type; false for "goal and names only" steps. */
    dictated: z.boolean().optional(),
  })
  .strict();

/**
 * A one-click card sort on an Another way angle (the quotes sort): each card goes in one of 2 or 3 groups, then
 * "Check my sort" marks each card and shows `explain`.
 */
export const cardSortSchema = z
  .object({
    groups: z.array(z.string().min(1)).min(2).max(3),
    cards: z.array(z.object({ text: z.string().min(1), group: z.number().int().min(0) }).strict()).min(2),
    explain: prose,
  })
  .strict()
  .refine((value) => value.cards.every((card) => card.group < value.groups.length), { message: "a card's group is not one of the groups" });

export const anotherWaySchema = z
  .object({
    angle: z.string().min(1),
    label: z.string().optional(),
    text: prose,
    sort: cardSortSchema.optional(),
  })
  .strict();

export const cameoSchema = z.enum(["mar-tu", "oogrish", "gearshift", "bomb-shell", "lucky"]);

export const bonusSchema = z
  .object({
    by: cameoSchema.default("lucky"),
    title: z.string().default("Side quest"),
    text: prose,
    hints: z.array(prose).default([]),
    checks: z.array(courseCheckSchema).min(1),
    solution: codeSchema,
  })
  .strict();

/** "Assemble it": a Parsons version of the exercise for anyone facing a blank editor. */
export const assembleSchema = z
  .object({
    lines: z.array(z.string()).min(2),
    distractors: z.array(z.string()).default([]),
    /**
     * Mar'tu's version after each step but the last (the harness's partials, exported with Assemble it). With them,
     * More structure on step k shuffles only the lines step k adds and keeps the rest of the program in place.
     */
    steps: z.array(codeSchema).optional(),
  })
  .strict();

export const exampleSchema = z
  .object({
    code: codeSchema,
    output: z.string(),
    stdin: z.array(z.string()).optional(),
  })
  .strict();

export const supportSchema = z.enum(["full", "light", "none"]);

/** Predict before Run: a one-click guess at what the code prints. Free, never blocks Run. */
export const exercisePredictSchema = z
  .object({
    q: prose,
    /** The code to predict (the harness runs it to prove the answer). Absent: the starter. */
    code: codeSchema.optional(),
    choices: z.array(z.string()).min(2),
    /** Index of the right choice. */
    answer: z.number().int().min(0),
    /** Shown after the guess, right or wrong. */
    explain: prose,
  })
  .strict()
  .refine((value) => value.answer < value.choices.length, { message: "predict answer is not one of the choices" });

const exerciseShape = {
  id: slug,
  title: z.string().min(1),
  /** Mar'tu's explanation: the Learn pane. */
  martu: prose,
  example: exampleSchema.optional(),
  anotherWay: z.array(anotherWaySchema).default([]),
  introduces: z.array(token).default([]),
  preview: z.array(token).default([]),
  /** Load the campaign engine helpers (party, print_prompt, ...). Off for ordinary exercises. */
  engine: z.boolean().default(false),
  /** Hidden code run before the student's code. */
  setup: codeSchema.optional(),
  /** Scripted answers for input(), in order. */
  stdin: z.array(z.string()).optional(),
  starter: codeSchema,
  checkpoints: z.array(checkpointSchema).min(1).max(12),
  solution: codeSchema,
  /** True for "run this and read it" exercises whose starter already passes. */
  starterPasses: z.boolean().default(false),
  /** Offer the step-through tracer. */
  tracer: z.boolean().default(false),
  /** full: hints, another way, solution after gating. light: hints after the first failed run. none: test-outs. */
  support: supportSchema.default("full"),
  bonus: bonusSchema.optional(),
  assemble: assembleSchema.optional(),
  /** Lucky's "What's in it for me?" box: where this shows up in the campaign. */
  campaignLink: z
    .object({ module: z.string(), part: z.string(), snippet: codeSchema.optional(), why: prose })
    .strict()
    .optional(),
  /** One line for the unit cheatsheet / skill map. */
  takeaway: z.string().optional(),
  /** Predict before Run (shown above the editor until the student guesses). */
  predict: exercisePredictSchema.optional(),
  /** "Names to use" chips: the names the steps ask for. */
  names: z.array(z.string().min(1)).default([]),
  /**
   * Mar'tu's pick: a value to use when the student can't decide (every other value is still accepted). The UI
   * puts it in quotes where needed; a pick that starts with `#` is a note and goes in as it is, on its own line.
   */
  pick: z.string().optional(),
  /** An optional "Pair talk" prompt. Each student still does every step on their own device. */
  pairTalk: prose.optional(),
  /** The lesson's SOLO item: done alone. */
  solo: z.boolean().default(false),
  /**
   * How much the crash explainer says. full: what happened and what to try (the fixed line when it can).
   * lean: the kind of slip and the line, never the fix (Unit 2's SOLO items and Quick Check 2, by the
   * teacher's ruling). Python's own last line stays on screen either way.
   */
  explainer: z.enum(["full", "lean"]).default("full"),
};

export const exerciseSchema = z.object(exerciseShape).strict();

const qBase = {
  id: slug,
  q: prose,
  /** Shown after answering, whether right or wrong. */
  explain: prose,
};

export const questionSchema = z.discriminatedUnion("type", [
  z
    .object({
      type: z.literal("mc"),
      ...qBase,
      code: codeSchema.optional(),
      choices: z.array(z.string()).min(2),
      answer: z.number().int().min(0),
      /** choice index (as a string) -> why that choice is wrong */
      whyWrong: z.record(z.string(), z.string()).default({}),
    })
    .strict(),
  z
    .object({
      type: z.literal("predict"),
      ...qBase,
      code: codeSchema,
      /** The exact output (verified by running the code). */
      answer: z.string(),
      choices: z.array(z.string()).optional(),
      setup: codeSchema.optional(),
      stdin: z.array(z.string()).optional(),
    })
    .strict(),
  z
    .object({
      type: z.literal("fill"),
      ...qBase,
      /** Contains ___ where the answer goes. */
      code: codeSchema,
      answer: z.string(),
      accept: z.array(z.string()).default([]),
      expectedOutput: z.string(),
    })
    .strict(),
  z
    .object({
      type: z.literal("parsons"),
      ...qBase,
      /** The lines in the correct order (the UI shuffles them). */
      lines: z.array(z.string()).min(2),
      distractors: z.array(z.string()).default([]),
      expectedOutput: z.string(),
    })
    .strict(),
  z
    .object({
      type: z.literal("bug"),
      ...qBase,
      code: codeSchema,
      fix: codeSchema,
      expectedOutput: z.string(),
    })
    .strict(),
]);

const itemBase = {
  id: slug,
  title: z.string().min(1),
  /** Optional items never block progress. */
  optional: z.boolean().default(false),
  /** Rough minutes for a typical student. */
  minutes: z.number().int().positive().optional(),
  summary: z.string().optional(),
};

export const lessonItemSchema = z
  .object({ kind: z.literal("lesson"), ...itemBase, exercises: z.array(exerciseSchema).min(1) })
  .strict();

export const quizItemSchema = z
  .object({ kind: z.literal("quiz"), ...itemBase, questions: z.array(questionSchema).min(1) })
  .strict();

/** A project is one exercise whose checkpoints are its task list. */
export const projectItemSchema = z
  .object({
    kind: z.literal("project"),
    ...itemBase,
    ...exerciseShape,
    intro: prose.optional(),
    support: supportSchema.default("light"),
  })
  .strict();

export const challengeItemSchema = z
  .object({
    kind: z.literal("challenge"),
    ...itemBase,
    ...exerciseShape,
    optional: z.boolean().default(true),
    level: z.enum(["core", "advanced"]).default("core"),
    variantOf: slug.optional(),
    support: supportSchema.default("light"),
  })
  .strict();

export const articleItemSchema = z
  .object({
    kind: z.literal("article"),
    ...itemBase,
    body: prose,
    examples: z.array(exampleSchema).default([]),
    exercises: z.array(exerciseSchema).default([]),
  })
  .strict();

export const cheatsheetItemSchema = z
  .object({
    kind: z.literal("cheatsheet"),
    ...itemBase,
    optional: z.boolean().default(true),
    entries: z
      .array(
        z
          .object({ concept: z.string(), code: codeSchema, output: z.string().optional(), note: z.string().optional() })
          .strict(),
      )
      .min(1),
  })
  .strict();

/**
 * Quick Check: pass every exercise (no hints) to test out of the unit's core items. With `questionsToPass`, the
 * form's questions (the quiz `<id>-questions`) count too: that many of them right, as well as every task.
 */
export const testoutItemSchema = z
  .object({
    kind: z.literal("testout"),
    ...itemBase,
    optional: z.boolean().default(true),
    exercises: z.array(exerciseSchema).min(1),
    questionsToPass: z.number().int().min(1).optional(),
  })
  .strict();

export const itemSchema = z.discriminatedUnion("kind", [
  lessonItemSchema,
  quizItemSchema,
  projectItemSchema,
  challengeItemSchema,
  articleItemSchema,
  cheatsheetItemSchema,
  testoutItemSchema,
]);

export const unitSchema = z
  .object({
    id: slug,
    order: z.number().int().min(1),
    title: z.string().min(1),
    /** In-world subtitle, e.g. "Words by the Fire". */
    subtitle: z.string().optional(),
    /** Unpublished units only show with ?preview=1. */
    published: z.boolean(),
    martuIntro: prose,
    goals: z.array(z.string()).min(1),
    campaignLinks: z.array(z.string()).default([]),
    items: z.array(itemSchema).min(1),
  })
  .strict();

export const glossaryEntrySchema = z
  .object({
    term: z.string().min(1),
    aliases: z.array(z.string()).default([]),
    plain: z.string().min(1),
    example: z.string().optional(),
  })
  .strict();

export const courseMetaSchema = z
  .object({
    id: z.literal("intro-python"),
    title: z.string().min(1),
    /** Mar'tu's opening on the course map. */
    intro: prose,
    settings: z
      .object({
        /** "Compare with Mar'tu's version" unlocks after this many minutes on an exercise... */
        solutionAfterMinutes: z.number().default(5),
        /** ...or this many counted failed runs (changed code, or Help opened since), whichever comes first. */
        solutionAfterFailedRuns: z.number().int().default(4),
        /** Quiz score that earns the "Ready" badge (never blocks anything). */
        quizReadyPercent: z.number().default(70),
      })
      .strict()
      .default({}),
  })
  .strict();

export type CourseCheck = z.infer<typeof courseCheckSchema>;
export type Checkpoint = z.infer<typeof checkpointSchema>;
export type AnotherWay = z.infer<typeof anotherWaySchema>;
export type Bonus = z.infer<typeof bonusSchema>;
export type Example = z.infer<typeof exampleSchema>;
export type Exercise = z.infer<typeof exerciseSchema>;
export type Question = z.infer<typeof questionSchema>;
export type LessonItem = z.infer<typeof lessonItemSchema>;
export type QuizItem = z.infer<typeof quizItemSchema>;
export type ProjectItem = z.infer<typeof projectItemSchema>;
export type ChallengeItem = z.infer<typeof challengeItemSchema>;
export type ArticleItem = z.infer<typeof articleItemSchema>;
export type CheatsheetItem = z.infer<typeof cheatsheetItemSchema>;
export type TestoutItem = z.infer<typeof testoutItemSchema>;
export type Item = z.infer<typeof itemSchema>;
export type Unit = z.infer<typeof unitSchema>;
export type GlossaryEntry = z.infer<typeof glossaryEntrySchema>;
export type CourseMeta = z.infer<typeof courseMetaSchema>;

/** Anything played in the exercise player: a lesson exercise, a project, a challenge, a test-out exercise. */
export type Playable = Exercise | ProjectItem | ChallengeItem;

/** The progress key for an exercise: "<unit>/<item>/<exercise>" (projects/challenges: "<unit>/<item>"). */
export function exerciseKey(unitId: string, itemId: string, exerciseId?: string): string {
  return exerciseId ? `${unitId}/${itemId}/${exerciseId}` : `${unitId}/${itemId}`;
}

/** The exercises an item contains, in order (projects and challenges are one exercise each). */
export function playablesOf(item: Item): { key: string | undefined; exercise: Playable }[] {
  switch (item.kind) {
    case "lesson":
    case "testout":
      return item.exercises.map((exercise) => ({ key: exercise.id, exercise }));
    case "article":
      return item.exercises.map((exercise) => ({ key: exercise.id, exercise }));
    case "project":
    case "challenge":
      return [{ key: undefined, exercise: item }];
    default:
      return [];
  }
}
