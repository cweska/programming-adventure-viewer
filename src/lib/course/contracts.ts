/**
 * Shared contracts between the pieces of the Intro to Python course.
 *
 *  - Running code:      src/lib/languages/python/run.ts      runCourse(input)          (engine)
 *  - Grading:           src/lib/course/grading.ts            gradeCheckpoints(...)     (engine)
 *  - Friendly errors:   src/lib/course/explain.ts            explainCourseError(...)   (engine)
 *  - Progress:          src/lib/course/progress.ts           useCourseProgress() ...   (shell)
 *  - Prose rendering:   src/components/course/Prose.tsx      <Prose text glossary />   (shell)
 *  - Content registry:  src/lib/course/registry.ts           (server/test only)        (shell)
 *  - Exercise player:   src/components/course/LessonPlayer.tsx <LessonPlayer ... />    (exercise)
 *
 * Keep these types stable. If one must change, change it here first.
 */
import type { Checkpoint, CourseCheck, GlossaryEntry, Item } from "./schema";
import type { Explanation, RunResult } from "../languages/types";

/* ------------------------------------------------------------------------------------------------ */
/* Running code                                                                                      */
/* ------------------------------------------------------------------------------------------------ */

/**
 * One course run. The worker runs, in order: the import guard, the course helpers
 * (public/workers/course_helpers.py), the campaign engine objects only when `engine` is true,
 * the input() shim fed with `stdin`, `setup`, then `code` (with `_source` = code). If that ran without
 * an exception it sets `_captured_stdout` and runs each check in the same namespace.
 * Returns the ordinary RunResult (checks in the same order as sent).
 */
export type CourseRunInput = {
  code: string;
  checks: CourseCheck[];
  setup?: string;
  stdin?: string[];
  engine?: boolean;
};

export type RunCourse = (input: CourseRunInput) => Promise<RunResult>;

/* ------------------------------------------------------------------------------------------------ */
/* Grading                                                                                           */
/* ------------------------------------------------------------------------------------------------ */

/** Checks are flattened as `${checkpointId}::${checkName}` so results can be regrouped. */
export type CheckpointGrade = {
  id: string;
  passed: boolean;
  /** The first failing check's student-facing message (AssertionError: prefix stripped). */
  message: string;
};

export type GradeResult = {
  /** The student's code raised before checks ran (or timed out). */
  crashed: boolean;
  checkpoints: CheckpointGrade[];
  /** Index of the first checkpoint that is not passed, or null when all pass. */
  firstFailing: number | null;
  allPassed: boolean;
};

export type GradeCheckpoints = (checkpoints: Checkpoint[], result: RunResult) => GradeResult;
export type FlattenChecks = (checkpoints: Checkpoint[]) => CourseCheck[];

/** Friendly explanation that also knows the class's common slips (missing quotes, def vs =, ...). */
export type ExplainCourseError = (traceback: string, code: string) => Explanation;

/* ------------------------------------------------------------------------------------------------ */
/* Progress (localStorage key "intro-python:v1")                                                     */
/* ------------------------------------------------------------------------------------------------ */

export type ExerciseProgress = {
  /** The student's latest code (autosaved). */
  code?: string;
  /** Checkpoint ids passed at least once. */
  passed: string[];
  /** Every checkpoint passed in one run. */
  done: boolean;
  /** Hint rungs revealed per checkpoint id. */
  hintsUsed: Record<string, number>;
  failedRuns: number;
  /** ms since epoch when first opened (for solution gating). */
  firstSeenAt?: number;
  /** Minutes actually spent (visible tab), accumulated. */
  activeMs?: number;
  solutionShown?: boolean;
  bonusDone?: boolean;
};

export type QuizProgress = { best: number; attempts: number; lastAnswers?: Record<string, string> };

export type CourseSettings = {
  /**
   * Support preset (curriculum §2.3). "more" = "Show me more" (the default): Mar'tu's full explanation, the
   * example open, help offered proactively. "short" = "Keep it short": explanation collapsed to the essentials,
   * example collapsed, help only when asked. Students can always open anything; presets never hide steps.
   */
  preset?: "more" | "short";
  /** Legacy alias for preset "short" (kept so saved progress still loads). */
  light?: boolean;
  /** Show the read-aloud buttons. */
  readAloud?: boolean;
};

export type CourseProgress = {
  version: 1;
  /** key = exerciseKey(unitId, itemId, exerciseId?) */
  exercises: Record<string, ExerciseProgress>;
  /** key = `${unitId}/${itemId}` */
  quizzes: Record<string, QuizProgress>;
  /** key = `${unitId}/${itemId}` */
  read: Record<string, true>;
  /** unitId -> passed the unit's Quick Check */
  testedOut: Record<string, true>;
  settings: CourseSettings;
};

export type ItemStatus = "not-started" | "in-progress" | "done" | "tested-out";

/* ------------------------------------------------------------------------------------------------ */
/* Component props                                                                                   */
/* ------------------------------------------------------------------------------------------------ */

/** What an item page knows about its unit (no other units' content is shipped to the client). */
export type UnitSummary = {
  id: string;
  order: number;
  title: string;
  subtitle?: string;
  items: { id: string; kind: Item["kind"]; title: string; optional: boolean }[];
};

export type ItemPageProps<I extends Item = Item> = {
  unit: UnitSummary;
  item: I;
  /** Only the glossary entries this item's prose references. */
  glossary: GlossaryEntry[];
  /** href of the next item in the unit (or the unit page when last). */
  nextHref: string;
  settings: { solutionAfterMinutes: number; solutionAfterFailedRuns: number; quizReadyPercent: number };
};
