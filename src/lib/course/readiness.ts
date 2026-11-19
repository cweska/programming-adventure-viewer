/**
 * The Campaign Readiness Check (curriculum §5, Unit 10): a unit that holds a REQUIRED test-out (`kind: "testout"`
 * with `optional: false`; today only `rc-part1-a`). Client-safe, pure: every function reads saved progress and the
 * unit's outline, and returns what the unit page, the players and "Next up" show.
 *
 * Such a unit is not a Quick Check unit (teacher site request 1, the MUST of every rep):
 *  - no Quick Check offer: its forms and their `-questions` quizzes are listed with the other items, in ITEMS order,
 *    and the required form and its questions are core rows;
 *  - nothing ever tests the unit out: the mini-boss and the explain question must be done by the student;
 *  - the optional parallel forms (B, C) and their questions are locked rows until Part 1 A was tried (every task run
 *    once and the questions answered once) and Mar'tu's notes (the review article) were opened;
 *  - the spaced re-check (the other optional test-outs) stays hidden until the core is done and about a week has
 *    passed, or the teacher opens it (`?recheck=open` on the unit page);
 *  - "Next up" follows the core in order: the intro, the questions, the tasks, the mini-boss, the explain question,
 *    with Mar'tu's notes after Part 1 when something was missed.
 *
 * Everything is derived from the item list, so no content field is needed. The per-skill grouping of Part 1 (the 13
 * items of curriculum §5.3) and their review routes are READINESS_ITEMS below; content.test.ts proves they match the
 * unit's own notes and that every route is a real exercise.
 */
import type { CourseProgress, ExerciseProgress, ItemStatus } from "./contracts";
import type { ProgressItem } from "./progress";

/** About a week after the core is done, the spaced re-check opens (curriculum §5.6). */
export const RECHECK_AFTER_MS = 7 * 24 * 60 * 60 * 1000;

/** The words on a locked form's row (the teacher's wording). */
export const LOCKED_FORM_TEXT = "Opens after Part 1 A and Mar'tu's notes";

/** Which items of a readiness unit play which part, derived from the item list (ITEMS order). */
export type ReadinessPlan = {
  /** The required form (`rc-part1-a`). */
  required: string;
  /** Every parallel form, in ITEMS order, the required one first: the same number of tasks as the required form. */
  forms: string[];
  /** A form's questions quiz (`<form>-questions`), when it has one. */
  questions: Record<string, string | undefined>;
  /** The other optional test-outs: the spaced re-check. */
  rechecks: string[];
  /** Mar'tu's notes: the first article after the required form. */
  review?: string;
  /** The core mini-boss (the first project that is not optional). */
  miniBoss?: string;
  /** The optional second mini-boss, for after Mar'tu's version helped (the first optional project after it). */
  twinBoss?: string;
  /** The core quiz that is no form's questions: "Explain a line you wrote". */
  explain?: string;
  /** The intro article (the first core article). */
  intro?: string;
};

/** A unit holds a required test-out: it is a readiness unit, never a Quick Check unit. */
export function isReadinessUnit(items: readonly Pick<ProgressItem, "kind" | "optional">[]): boolean {
  return items.some((item) => item.kind === "testout" && !item.optional);
}

/** The readiness plan of a unit, or null when it holds no required test-out. */
export function readinessPlan(items: readonly ProgressItem[]): ReadinessPlan | null {
  const at = items.findIndex((item) => item.kind === "testout" && !item.optional);
  if (at < 0) return null;
  const required = items[at];
  const size = required.exercises?.length ?? 0;
  const testouts = items.filter((item) => item.kind === "testout");
  const forms = [required, ...testouts.filter((item) => item !== required && (item.exercises?.length ?? 0) === size)].map((item) => item.id);
  const quizIds = new Set(items.filter((item) => item.kind === "quiz").map((item) => item.id));
  const questions: Record<string, string | undefined> = {};
  for (const form of testouts) questions[form.id] = quizIds.has(`${form.id}-questions`) ? `${form.id}-questions` : undefined;
  const formQuizzes = new Set(Object.values(questions).filter((id): id is string => Boolean(id)));
  const miniBossAt = items.findIndex((item) => item.kind === "project" && !item.optional);
  return {
    required: required.id,
    forms,
    questions,
    rechecks: testouts.filter((item) => !forms.includes(item.id)).map((item) => item.id),
    review: items.slice(at + 1).find((item) => item.kind === "article")?.id,
    miniBoss: miniBossAt >= 0 ? items[miniBossAt].id : undefined,
    twinBoss: miniBossAt >= 0 ? items.slice(miniBossAt + 1).find((item) => item.kind === "project" && item.optional)?.id : undefined,
    explain: items.find((item) => item.kind === "quiz" && !item.optional && !formQuizzes.has(item.id))?.id,
    intro: items.find((item) => item.kind === "article" && !item.optional)?.id,
  };
}

/* ------------------------------------------------------------------------------------------------ */
/* Part 1's skills (curriculum §5.3): which question and task positions make each of the 13 items     */
/* ------------------------------------------------------------------------------------------------ */

/** A review route: an earlier exercise, by unit id, lesson item id and exercise id (rc-review's "Start here"). */
export type ReviewRoute = { unit: string; item: string; exercise?: string };

export type ReadinessSkill = {
  /** The item's number in curriculum §5.3 (1 to 13). */
  n: number;
  /** What the item checks, in rc-review's words. */
  skill: string;
  /** Positions (0-based) in each form's questions quiz. */
  questions?: number[];
  /** Positions (0-based) in each form's tasks. */
  tasks?: number[];
  /** A task whose steps are parts of the item (item 6: three reads and writes, and the `in` question). */
  taskParts?: number;
  /** Ready needs this item (curriculum §5.5: item 6 at 3 of 4 parts, item 13 passed). */
  required?: boolean;
  /** rc-review's "Start here": the first lesson to open again. */
  start: ReviewRoute;
};

/**
 * Unit 10's Part 1, item by item (curriculum §5.3, the unit's notes: `Item 3a`, `rc_item=3`, and rc-review's ROUTES).
 * The forms are parallel: question k and task k of form B or C are the twins of form A's (content.test.ts checks it).
 */
export const READINESS_ITEMS: Record<string, readonly ReadinessSkill[]> = {
  "readiness-check": [
    { n: 1, skill: "glue text with `+` and `str()`", questions: [0], start: { unit: "hello-world", item: "math-and-glue", exercise: "glue-words" } },
    { n: 2, skill: "replace `pass`", tasks: [0], start: { unit: "first-recipes", item: "recipes-with-names", exercise: "replace-pass" } },
    { n: 3, skill: "tidy a line, store it, then pass it on", questions: [1], tasks: [1], start: { unit: "first-recipes", item: "recipes-with-names", exercise: "store-then-pass" } },
    { n: 4, skill: "exactly enough, and tracing a call", questions: [2, 3], start: { unit: "control-flow", item: "true-or-false-yes", exercise: "enough-to-pass" } },
    { n: 5, skill: "which branch runs, and text in quotes", questions: [4], tasks: [2], start: { unit: "control-flow", item: "if-the-clock-turns-red", exercise: "clock-colors" } },
    {
      n: 6,
      skill: "read and write a stat sheet",
      questions: [5],
      tasks: [3],
      taskParts: 3,
      required: true,
      start: { unit: "dictionaries", item: "stat-sheets", exercise: "read-by-key" },
    },
    { n: 7, skill: "a bar of blocks", questions: [6], tasks: [4], start: { unit: "hello-world", item: "math-and-glue", exercise: "repeat-a-mark" } },
    { n: 8, skill: "roll a die", questions: [7], tasks: [5], start: { unit: "control-flow", item: "if-the-clock-turns-red", exercise: "roll-a-die" } },
    { n: 9, skill: "a function stored in a dictionary", questions: [8, 9], start: { unit: "spell-recipes", item: "spells-you-can-hand-over", exercise: "name-without-parentheses" } },
    { n: 10, skill: "a loop over a list of sheets", questions: [10, 11], start: { unit: "loops", item: "for-each-yes", exercise: "predict-the-loop" } },
    { n: 11, skill: "read the error box, then fix the line", tasks: [6], start: { unit: "control-flow", item: "when-spells-fizzle", exercise: "debug-routine" } },
    { n: 12, skill: "spend mana from a sheet", tasks: [7], start: { unit: "hello-world", item: "math-and-glue", exercise: "spend-mana" } },
    { n: 13, skill: "write a function from its goal", tasks: [8], required: true, start: { unit: "first-recipes", item: "recipes-with-names", exercise: "use-the-ingredients" } },
  ],
};

/* ------------------------------------------------------------------------------------------------ */
/* Reading progress                                                                                  */
/* ------------------------------------------------------------------------------------------------ */

function key(unitId: string, ...ids: string[]): string {
  return [unitId, ...ids].join("/");
}

function find(items: readonly ProgressItem[], id: string | undefined): ProgressItem | undefined {
  return id === undefined ? undefined : items.find((item) => item.id === id);
}

/** A task was tried: run at least once with the student's own code (a pass, a step, or a counted miss). */
export function taskAttempted(entry: ExerciseProgress | undefined): boolean {
  return Boolean(entry && (entry.done || entry.passed.length > 0 || entry.failedRuns > 0));
}

function exerciseEntry(unitId: string, form: ProgressItem | undefined, at: number, progress: CourseProgress): ExerciseProgress | undefined {
  const exercise = form?.exercises?.[at];
  return form && exercise ? progress.exercises[key(unitId, form.id, exercise.id)] : undefined;
}

/** The quiz's questions this student got right, at least once, in any attempt. */
function rightIds(unitId: string, quizId: string | undefined, progress: CourseProgress): string[] {
  return quizId ? (progress.quizzes[key(unitId, quizId)]?.right ?? []) : [];
}

/** Task `at` passed in any parallel form (its twins count: curriculum §5.5, teacher site request 3). */
export function taskPassedAt(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, at: number, progress: CourseProgress): boolean {
  return plan.forms.some((id) => exerciseEntry(unitId, find(items, id), at, progress)?.done === true);
}

/** Question `at` answered right, once, in any parallel form's questions. */
export function questionRightAt(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, at: number, progress: CourseProgress): boolean {
  return plan.forms.some((id) => {
    const quiz = find(items, plan.questions[id]);
    const question = quiz?.questionIds?.[at];
    return question !== undefined && rightIds(unitId, quiz?.id, progress).includes(question);
  });
}

/** Part 1 A's questions were answered once (a finished attempt), or the required form has none. */
export function part1Answered(unitId: string, plan: ReadinessPlan, progress: CourseProgress): boolean {
  const quiz = plan.questions[plan.required];
  return quiz === undefined || (progress.quizzes[key(unitId, quiz)]?.attempts ?? 0) > 0;
}

/**
 * Part 1 A's tasks not tried yet (positions, 0-based): never run with the student's own code. A task skipped without a
 * Run stays here, so the site can name it ("Stuck? Skip it" is the course's own advice: the student is told what is
 * still missing, never left at a lock with no reason).
 */
export function untriedTasks(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): number[] {
  const form = find(items, plan.required);
  return (form?.exercises ?? []).map((_, at) => at).filter((at) => !taskAttempted(exerciseEntry(unitId, form, at, progress)));
}

/** Part 1 A was tried: every task of the required form run once, and its questions answered once. */
export function part1Tried(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): boolean {
  const tasks = find(items, plan.required)?.exercises ?? [];
  return tasks.length > 0 && untriedTasks(unitId, items, plan, progress).length === 0 && part1Answered(unitId, plan, progress);
}

/** "Task 9, *Write a function from its goal*" for each untried position (the form's own task titles). */
export function untriedTaskNames(items: readonly ProgressItem[], plan: ReadinessPlan, untried: readonly number[]): string[] {
  const form = find(items, plan.required);
  return untried.map((at) => {
    const title = form?.exercises?.[at]?.title;
    return title ? `Task ${at + 1}, *${title}*` : `Task ${at + 1}`;
  });
}

/** "A", "A and B", "A, B and C". */
export function joinAnd(parts: readonly string[]): string {
  if (parts.length <= 1) return parts.join("");
  return `${parts.slice(0, -1).join(", ")} and ${parts[parts.length - 1]}`;
}

/**
 * What Part 1 A still needs before it counts as tried, in words a student can act on: the tasks not run yet (named
 * when there are three or fewer, once Part 1 A was begun) and the questions. Null when nothing is missing, or when the
 * list would only be "almost everything" (a fresh start needs no list).
 */
export function part1Missing(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): string | null {
  const untried = untriedTasks(unitId, items, plan, progress);
  const size = find(items, plan.required)?.exercises?.length ?? 0;
  const answered = part1Answered(unitId, plan, progress);
  if (untried.length > 3 || untried.length === size) return null;
  const parts: string[] = [];
  if (untried.length > 0) {
    parts.push(
      `Not tried yet: ${joinAnd(untriedTaskNames(items, plan, untried))}. Type your best try, even if it is not finished, and press Run once. That counts as tried.`,
    );
  }
  if (!answered) parts.push(untried.length > 0 ? "Answer Part 1 A's questions once, too." : "Answer Part 1 A's questions once.");
  return parts.length > 0 ? parts.join(" ") : null;
}

/** Why forms B and C are still locked (part1Missing), or null when only the notes are missing, or nothing is. */
export function lockReason(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): string | null {
  if (formsUnlocked(unitId, items, plan, progress)) return null;
  return part1Missing(unitId, items, plan, progress);
}

/** Every task position of Part 1 passed, in form A or a twin. */
export function requiredTasksDone(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): boolean {
  const size = find(items, plan.required)?.exercises?.length ?? 0;
  return size > 0 && Array.from({ length: size }, (_, at) => at).every((at) => taskPassedAt(unitId, items, plan, at, progress));
}

/**
 * Part 1's questions: how many positions are right in any form (a retake draws the next form's questions, and its
 * score counts toward the required form's `questionsToPass`: teacher site request 2), how many are needed, and of how
 * many. Null when the required form needs no questions.
 */
export function readinessQuestions(
  unitId: string,
  items: readonly ProgressItem[],
  plan: ReadinessPlan,
  progress: CourseProgress,
): { right: number; needed: number; total: number; met: boolean } | null {
  const form = find(items, plan.required);
  const quiz = find(items, plan.questions[plan.required]);
  if (!form?.questionsToPass || !quiz) return null;
  const total = quiz.questionCount ?? quiz.questionIds?.length ?? 0;
  const right = Array.from({ length: total }, (_, at) => at).filter((at) => questionRightAt(unitId, items, plan, at, progress)).length;
  return { right, needed: form.questionsToPass, total, met: total > 0 && right >= form.questionsToPass };
}

/** Something in Part 1 is still missed: a task not passed (twins count), or too few questions right. */
export function part1Missed(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): boolean {
  const questions = readinessQuestions(unitId, items, plan, progress);
  return !requiredTasksDone(unitId, items, plan, progress) || (questions !== null && !questions.met);
}

/** The parallel forms open once Part 1 A was tried and Mar'tu's notes were opened. */
export function formsUnlocked(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): boolean {
  const notes = plan.review === undefined || progress.read[key(unitId, plan.review)] === true;
  return notes && part1Tried(unitId, items, plan, progress);
}

/** The spaced re-check is open: the teacher opened it, or the core was done about a week ago. */
export function recheckOpen(unitId: string, progress: CourseProgress, now: number): boolean {
  const saved = progress.readiness?.[unitId];
  if (saved?.recheckOpen) return true;
  return saved?.coreDoneAt !== undefined && now - saved.coreDoneAt >= RECHECK_AFTER_MS;
}

export type RowState = "open" | "locked" | "hidden";

/** How the unit page shows an item: a normal row, a locked row (no link), or no row at all. */
export function readinessRowState(
  unitId: string,
  items: readonly ProgressItem[],
  plan: ReadinessPlan,
  item: Pick<ProgressItem, "id">,
  progress: CourseProgress,
  now: number,
  teacher = false,
): RowState {
  const recheckIds = plan.rechecks.flatMap((id) => [id, plan.questions[id]]).filter(Boolean);
  if (recheckIds.includes(item.id)) return teacher || recheckOpen(unitId, progress, now) ? "open" : "hidden";
  const parallel = plan.forms.filter((id) => id !== plan.required).flatMap((id) => [id, plan.questions[id]]).filter(Boolean);
  if (parallel.includes(item.id)) return teacher || formsUnlocked(unitId, items, plan, progress) ? "open" : "locked";
  return "open";
}

/* ------------------------------------------------------------------------------------------------ */
/* Status, Next up and Continue                                                                      */
/* ------------------------------------------------------------------------------------------------ */

/**
 * An item's status in a readiness unit: never "tested-out". The required form is done when every task position passed,
 * in form A or a twin; every other item follows its own progress (`ownStatus`, progress.ts's rawStatus).
 */
export function readinessStatus(
  unitId: string,
  items: readonly ProgressItem[],
  plan: ReadinessPlan,
  item: ProgressItem,
  progress: CourseProgress,
  ownStatus: ItemStatus,
): ItemStatus {
  if (item.id !== plan.required) return ownStatus === "tested-out" ? "not-started" : ownStatus;
  if (requiredTasksDone(unitId, items, plan, progress)) return "done";
  const started = ownStatus !== "not-started" || plan.forms.some((id) => (find(items, id)?.exercises ?? []).some((_, at) => taskAttempted(exerciseEntry(unitId, find(items, id), at, progress))));
  return started ? "in-progress" : "not-started";
}

/**
 * "Next up" in a readiness unit (teacher site request 1.5): the intro, the questions, the tasks, Mar'tu's notes when
 * something was missed, the mini-boss, the explain question. `statusOf` is the item's readiness status.
 */
export function readinessNextUp<T extends ProgressItem>(
  unitId: string,
  items: readonly T[],
  plan: ReadinessPlan,
  progress: CourseProgress,
  statusOf: (item: T) => ItemStatus,
): T | undefined {
  const item = (id: string | undefined) => (id === undefined ? undefined : items.find((entry) => entry.id === id));
  const open = (id: string | undefined) => {
    const found = item(id);
    return found && statusOf(found) !== "done" ? found : undefined;
  };
  const intro = open(plan.intro);
  if (intro) return intro;
  const questions = item(plan.questions[plan.required]);
  if (questions && (progress.quizzes[key(unitId, questions.id)]?.attempts ?? 0) === 0) return questions;
  if (!part1Tried(unitId, items, plan, progress)) return item(plan.required);
  const missed = part1Missed(unitId, items, plan, progress);
  if (missed && plan.review && progress.read[key(unitId, plan.review)] !== true) return item(plan.review);
  const boss = open(plan.miniBoss);
  if (boss) return boss;
  const explain = open(plan.explain);
  if (explain) return explain;
  return missed ? (item(plan.review) ?? item(plan.required)) : undefined;
}

/** Where Continue goes after Part 1 A: Mar'tu's notes when something was missed, otherwise the mini-boss. */
export function afterPart1(unitId: string, items: readonly ProgressItem[], plan: ReadinessPlan, progress: CourseProgress): string | undefined {
  return part1Missed(unitId, items, plan, progress) ? (plan.review ?? plan.miniBoss) : (plan.miniBoss ?? plan.review);
}

/** The questions a retake draws: the next parallel form's (A, then B, then C, then A again). */
export function nextQuestionsForm(plan: ReadinessPlan, quizId: string): string | undefined {
  const withQuestions = plan.forms.filter((id) => plan.questions[id]);
  const at = withQuestions.findIndex((id) => plan.questions[id] === quizId);
  if (at < 0 || withQuestions.length < 2) return undefined;
  return plan.questions[withQuestions[(at + 1) % withQuestions.length]];
}

/** The form a questions quiz belongs to, when it is a parallel form's. */
export function formOfQuestions(plan: ReadinessPlan, quizId: string): string | undefined {
  return plan.forms.find((id) => plan.questions[id] === quizId);
}

/** "Form B" from "Readiness Check · Part 1 · Form B questions" (the words after the last ·, up to "questions"). */
export function formName(title: string | undefined): string {
  const part = (title ?? "").split("·").pop()?.trim() ?? "";
  return part.replace(/\s+questions$/i, "") || "another form";
}

/* ------------------------------------------------------------------------------------------------ */
/* The result (curriculum §5.5, teacher site requests 3 and 4)                                       */
/* ------------------------------------------------------------------------------------------------ */

export type ReadinessVerdict = "ready" | "review-list" | "review-first";

/** How the mini-boss went: not done yet, done on the student's own, or done after Mar'tu's version was opened. */
export type MiniBossResult = "not-done" | "on-your-own" | "with-compare";

export type SkillResult = {
  skill: ReadinessSkill;
  passed: boolean;
  /** Parts passed, of `parts` (item 6: three reads and writes and one question). */
  partsPassed: number;
  parts: number;
  /** The first parallel form (not the required one) whose twin of this item is not tried yet: the one to try next. */
  twinForm?: string;
};

export type ReadinessResult = {
  /** Part 1 A was tried: the score means something. */
  tried: boolean;
  /** Part 1 A's tasks not tried yet (positions): each one counts as a missed skill once the result is in. */
  untried: number[];
  /**
   * The unit page shows the result: Part 1 A was tried, or its questions were answered and every task was opened or a
   * mini-boss is done (a task skipped without a Run then counts as missed, and the result says so).
   */
  visible: boolean;
  skills: SkillResult[];
  score: number;
  total: number;
  miniBoss: MiniBossResult;
  /** Null until a mini-boss is done, and Part 1 was tried (or its questions answered: an untried task counts as missed). */
  verdict: ReadinessVerdict | null;
  /** After a pass with Mar'tu's version: the second mini-boss, when it is not done yet. */
  nextBoss?: string;
};

/**
 * The verdict's words. Ready allows one or two skills short (curriculum §5.5), so "every skill" only when the score is
 * full; and "on your own" only when the mini-boss that counts used no Help past Where to look (`unaided`, as its pass
 * line and footer say): Ready itself only asks that Mar'tu's version was not opened.
 */
export function readinessVerdictText(verdict: ReadinessVerdict, score: number, total: number, unaided: boolean): string {
  if (verdict === "review-list") return "Ready, with a review list. You can go on with the campaign. Look again at the skills on this list, too.";
  if (verdict === "review-first") {
    return "Review first. Look again at the skills on this list, then try each one's twin in another form. After two rounds of review, we go on anyway.";
  }
  const what = score === total ? "every skill the next campaign part needs" : "what the next campaign part needs";
  return `Ready. You showed Mar'tu ${what}${unaided ? ", on your own" : ""}.`;
}

function bossResult(entry: ExerciseProgress | undefined): MiniBossResult {
  if (!entry?.done) return "not-done";
  return entry.doneWithCompare ? "with-compare" : "on-your-own";
}

/** The Readiness result: Part 1 item by item (twins count), the mini-boss, and the verdict. */
export function readinessResult(
  unitId: string,
  items: readonly ProgressItem[],
  plan: ReadinessPlan,
  skills: readonly ReadinessSkill[],
  progress: CourseProgress,
): ReadinessResult {
  const results: SkillResult[] = skills.map((skill) => {
    const tasks = skill.tasks ?? [];
    const questions = skill.questions ?? [];
    const taskParts = (at: number) => {
      if (taskPassedAt(unitId, items, plan, at, progress)) return skill.taskParts ?? 1;
      if (!skill.taskParts) return 0;
      const steps = plan.forms.map((id) => exerciseEntry(unitId, find(items, id), at, progress)?.passed.length ?? 0);
      return Math.min(skill.taskParts, Math.max(0, ...steps));
    };
    const parts = tasks.reduce((sum) => sum + (skill.taskParts ?? 1), 0) + questions.length;
    const partsPassed =
      tasks.reduce((sum, at) => sum + taskParts(at), 0) + questions.filter((at) => questionRightAt(unitId, items, plan, at, progress)).length;
    // An item with parts passes one part short (item 6 at 3 of 4); every other item needs all of it.
    const passed = skill.taskParts ? partsPassed >= parts - 1 : partsPassed === parts;
    const twinForm = passed
      ? undefined
      : plan.forms
          .filter((id) => id !== plan.required)
          .find((id) => {
            const form = find(items, id);
            const quiz = find(items, plan.questions[id]);
            const tried = tasks.every((at) => taskAttempted(exerciseEntry(unitId, form, at, progress)));
            const answered = questions.length === 0 || (quiz !== undefined && (progress.quizzes[key(unitId, quiz.id)]?.attempts ?? 0) > 0);
            return !(tried && answered);
          });
    return { skill, passed, partsPassed, parts, ...(twinForm ? { twinForm } : {}) };
  });
  const score = results.filter((result) => result.passed).length;
  const tried = part1Tried(unitId, items, plan, progress);
  const untried = untriedTasks(unitId, items, plan, progress);
  const answered = part1Answered(unitId, plan, progress);
  const firstEntry = plan.miniBoss ? progress.exercises[key(unitId, plan.miniBoss)] : undefined;
  const secondEntry = plan.twinBoss ? progress.exercises[key(unitId, plan.twinBoss)] : undefined;
  const first = bossResult(firstEntry);
  const second = bossResult(secondEntry);
  // The first mini-boss counts; after a pass with Mar'tu's version its twin is the follow-up, and the result stays
  // "with a review list" (curriculum §5.5). The twin alone counts only when the first one is not done. Mar'tu's version
  // of either one, opened before the pass that counts, makes it "with Mar'tu's version" (the two answers are the same
  // program with other names: ExercisePlayer records it at the pass, `compareFrom`).
  const miniBoss: MiniBossResult = first !== "not-done" ? first : second;
  const form = find(items, plan.required);
  const opened = (form?.exercises ?? []).every((_, at) => exerciseEntry(unitId, form, at, progress) !== undefined);
  const counted = tried || (answered && miniBoss !== "not-done");
  const visible = tried || (answered && (opened || miniBoss !== "not-done"));
  let verdict: ReadinessVerdict | null = null;
  if (counted && miniBoss !== "not-done") {
    const requiredPassed = results.every((result) => !result.skill.required || result.passed);
    if (score <= Math.max(0, skills.length - 5)) verdict = "review-first";
    else if (score >= skills.length - 2 && requiredPassed && miniBoss === "on-your-own") verdict = "ready";
    else verdict = "review-list";
  }
  // The second mini-boss "on your own" only when its own answer was never shown.
  const nextBoss =
    miniBoss === "with-compare" && plan.twinBoss && second === "not-done" && secondEntry?.solutionShown !== true ? plan.twinBoss : undefined;
  return { tried, untried, visible, skills: results, score, total: skills.length, miniBoss, verdict, ...(nextBoss ? { nextBoss } : {}) };
}
