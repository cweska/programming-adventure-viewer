import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { applyRun, helpRungs, isCampaignMode, LAST_HINT_LABEL, solutionUnlocked } from "../../components/course/exercise-logic";
import { campaignModeSettings } from "../../components/course/LessonPlayer";
import type { CourseProgress, ExerciseProgress } from "./contracts";
import {
  emptyExercise,
  emptyProgress,
  itemStatus,
  nextUpItem,
  normalizeProgress,
  unitProgress,
  withExercise,
  withOwnWords,
  withQuiz,
  withQuizExplained,
  withQuizRight,
  withRead,
  withReadiness,
  type ProgressItem,
  type ProgressUnit,
} from "./progress";
import {
  afterPart1,
  formName,
  formsUnlocked,
  isReadinessUnit,
  LOCKED_FORM_TEXT,
  lockReason,
  nextQuestionsForm,
  part1Missed,
  part1Missing,
  part1Tried,
  READINESS_ITEMS,
  readinessPlan,
  readinessQuestions,
  readinessResult,
  readinessRowState,
  readinessVerdictText,
  RECHECK_AFTER_MS,
  recheckOpen,
  untriedTasks,
} from "./readiness";
import { allUnits, itemSettings, nextHref, readinessRoutes, unitOutline, unitSummary } from "./registry";

/** Unit 10 as the unit page gets it (registry.ts unitOutline): the real item list, in ITEMS order. */
const real = allUnits.find((unit) => unit.id === "readiness-check");
if (!real) throw new Error("Unit 10 (readiness-check) is not exported");
const unit: ProgressUnit = unitOutline(real);
const items = unit.items;
const plan = readinessPlan(items)!;
const U = unit.id;
const skills = READINESS_ITEMS[U];

const item = (id: string): ProgressItem => {
  const found = items.find((entry) => entry.id === id);
  if (!found) throw new Error(`no item ${id}`);
  return found;
};
const tasksOf = (form: string) => (item(form).exercises ?? []).map((exercise) => exercise.id);
const questionsOf = (quiz: string) => [...(item(quiz).questionIds ?? [])];

type Update = (progress: CourseProgress) => CourseProgress;
const apply = (progress: CourseProgress, ...updates: Update[]) => updates.reduce((current, update) => update(current), progress);
const exercise = (key: string, entry: Partial<ExerciseProgress>): Update => withExercise(key, (previous) => ({ ...previous, ...entry }));
const passTask = (form: string, at: number): Update => exercise(`${U}/${form}/${tasksOf(form)[at]}`, { done: true, passed: ["step-1"] });
const missTask = (form: string, at: number): Update => exercise(`${U}/${form}/${tasksOf(form)[at]}`, { failedRuns: 1 });
const passAll = (form: string, except: number[] = []): Update[] =>
  tasksOf(form).map((_, at) => (except.includes(at) ? missTask(form, at) : passTask(form, at)));
/** A finished questions attempt: these positions right, the rest wrong (best is the percent right). */
const answer = (quiz: string, right: number[]): Update => {
  const ids = questionsOf(quiz);
  return withQuiz(`${U}/${quiz}`, Math.round((100 * right.length) / ids.length), {}, right.map((at) => ids[at]));
};
const allQuestions = (quiz: string, except: number[] = []) => answer(quiz, questionsOf(quiz).map((_, at) => at).filter((at) => !except.includes(at)));
const read = (id: string): Update => withRead(`${U}/${id}`);
const boss = (id: string, withCompare = false): Update => exercise(`${U}/${id}`, { done: true, passed: ["a"], ...(withCompare ? { solutionShown: true, doneWithCompare: true } : {}) });
const status = (progress: CourseProgress, id: string) => itemStatus(U, item(id), progress, items);

describe("the readiness plan, from Unit 10's own item list (no content field)", () => {
  it("finds the required form, its parallel forms, the notes, the mini-bosses, the explain question and the re-check", () => {
    expect(isReadinessUnit(items)).toBe(true);
    expect(plan).toEqual({
      required: "rc-part1-a",
      forms: ["rc-part1-a", "rc-part1-b", "rc-part1-c"],
      questions: {
        "rc-part1-a": "rc-part1-a-questions",
        "rc-part1-b": "rc-part1-b-questions",
        "rc-part1-c": "rc-part1-c-questions",
        "rc-recheck": "rc-recheck-questions",
      },
      rechecks: ["rc-recheck"],
      review: "rc-review",
      miniBoss: "rc-miniboss-a",
      twinBoss: "rc-miniboss-b",
      explain: "rc-explain",
      intro: "before-we-continue",
    });
  });

  it("leaves every other unit a Quick Check unit (its test-outs are all optional)", () => {
    for (const other of allUnits.filter((entry) => entry.id !== U)) {
      expect(isReadinessUnit(unitOutline(other).items), other.id).toBe(false);
      expect(readinessPlan(unitOutline(other).items), other.id).toBeNull();
    }
  });

  it("pairs twins by position: every parallel form has as many tasks and questions as form A", () => {
    for (const form of plan.forms) {
      expect(tasksOf(form).length, form).toBe(tasksOf(plan.required).length);
      expect(questionsOf(plan.questions[form]!).length, form).toBe(questionsOf(plan.questions[plan.required]!).length);
    }
  });

  it("groups Part 1 into curriculum §5.3's 13 items, exactly as the unit's own notes number them", () => {
    const side = JSON.parse(readFileSync(path.join(process.cwd(), "content/courses/intro-python/units/readiness-check.verify.json"), "utf8")) as {
      questions: Record<string, { notes?: string }>;
      exercises: Record<string, { notes?: string }>;
    };
    expect(skills.map((skill) => skill.n)).toEqual(Array.from({ length: 13 }, (_, at) => at + 1));
    // Every question and task position belongs to exactly one item.
    const questionAt = new Map<number, number>();
    const taskAt = new Map<number, number>();
    for (const skill of skills) {
      for (const at of skill.questions ?? []) questionAt.set(at, skill.n);
      for (const at of skill.tasks ?? []) taskAt.set(at, skill.n);
    }
    expect([...questionAt.keys()].sort((a, b) => a - b)).toEqual(questionsOf("rc-part1-a-questions").map((_, at) => at));
    expect([...taskAt.keys()].sort((a, b) => a - b)).toEqual(tasksOf("rc-part1-a").map((_, at) => at));
    // Form A's notes say "Item 3a." (questions) and "item=3b" (tasks); forms B and C say "rc_item=3".
    const itemNumber = (notes = "") => Number(notes.match(/^Item (\d+)/)?.[1] ?? notes.match(/\b(?:rc_)?item=(\d+)/)?.[1]);
    for (const form of plan.forms) {
      questionsOf(plan.questions[form]!).forEach((id, at) => {
        expect(itemNumber(side.questions[`${plan.questions[form]}/${id}`]?.notes), `${form} question ${at + 1}`).toBe(questionAt.get(at));
      });
      tasksOf(form).forEach((id, at) => {
        expect(itemNumber(side.exercises[`${form}/${id}`]?.notes), `${form} task ${at + 1}`).toBe(taskAt.get(at));
      });
    }
  });

  it("sends every missed skill to a real lesson exercise, the one rc-review marks Start here", () => {
    const routes = readinessRoutes(U);
    expect(routes.map((route) => route.n)).toEqual(skills.map((skill) => skill.n));
    const notes = real.items.find((entry) => entry.id === "rc-review");
    const body = notes && notes.kind === "article" ? notes.body : "";
    for (const route of routes) {
      expect(route.href, `item ${route.n}`).toMatch(/^\/intro-python\/[a-z-]+\/[a-z-]+#[a-z0-9-]+$/);
      // rc-review's "Start here: Unit 3 · Recipes With Names · *Replace pass*" for the same item.
      const [unitLabel, lesson, title] = route.label.split(" · ");
      expect(body, `item ${route.n}`).toContain(`Start here: ${unitLabel} · ${lesson} · *${title}*`);
      expect(route.seen, `item ${route.n}`).toMatch(/^(Questions? \d+( and \d+)?|\*[^*]+\*)( and \*[^*]+\*)?$/);
    }
    expect(routes.find((route) => route.n === 3)?.seen).toBe("Question 2 and *Store, then pass it on*");
  });
});

describe("site request 1: a required test-out is a core item, and nothing tests the unit out", () => {
  it("lists the forms in ITEMS order, the required form and its questions as core items", () => {
    expect(item("rc-part1-a").optional).toBe(false);
    expect(item("rc-part1-a-questions").optional).toBe(false);
    const stats = unitProgress(unit, emptyProgress());
    expect(stats.total).toBe(items.filter((entry) => !entry.optional).length);
    expect(items.filter((entry) => !entry.optional).map((entry) => entry.id)).toEqual([
      "before-we-continue",
      "rc-part1-a-questions",
      "rc-part1-a",
      "rc-miniboss-a",
      "rc-explain",
    ]);
  });

  it("never reads tested-out, even with an old testedOut flag, and passing every form marks neither the mini-boss nor rc-explain", () => {
    const progress = apply(
      emptyProgress(),
      ...plan.forms.flatMap((form) => passAll(form)),
      ...plan.forms.map((form) => allQuestions(plan.questions[form]!)),
      ...passAll("rc-recheck"),
      allQuestions("rc-recheck-questions"),
      (current) => ({ ...current, testedOut: { [U]: true } }),
    );
    expect(status(progress, "rc-part1-a")).toBe("done");
    expect(status(progress, "rc-miniboss-a")).toBe("not-started");
    expect(status(progress, "rc-explain")).toBe("not-started");
    for (const entry of items) expect(status(progress, entry.id), entry.id).not.toBe("tested-out");
    const stats = unitProgress(unit, progress);
    expect(stats.testedOut).toBe(false);
    expect(stats.complete).toBe(false);
    // Ready needs the mini-boss: with every form passed and no mini-boss, there is no verdict yet.
    const result = readinessResult(U, items, plan, skills, progress);
    expect(result.score).toBe(13);
    expect(result.miniBoss).toBe("not-done");
    expect(result.verdict).toBeNull();
    expect(readinessResult(U, items, plan, skills, apply(progress, boss("rc-miniboss-a"))).verdict).toBe("ready");
  });

  it("is complete only when the student did the core: the intro, Part 1, the mini-boss and rc-explain", () => {
    const core = apply(
      emptyProgress(),
      read("before-we-continue"),
      allQuestions("rc-part1-a-questions"),
      ...passAll("rc-part1-a"),
      boss("rc-miniboss-a"),
    );
    expect(unitProgress(unit, core)).toMatchObject({ done: 4, total: 5, complete: false, testedOut: false });
    const done = apply(core, answer("rc-explain", [0]));
    expect(unitProgress(unit, done)).toMatchObject({ done: 5, total: 5, complete: true, percent: 100 });
  });

  it("counts form A done when every task passed, in form A or its twin (a student redoes one task, not a form)", () => {
    const mostly = apply(emptyProgress(), ...passAll("rc-part1-a", [4]));
    expect(status(mostly, "rc-part1-a")).toBe("in-progress");
    expect(status(apply(mostly, passTask("rc-part1-c", 4)), "rc-part1-a")).toBe("done");
    expect(status(emptyProgress(), "rc-part1-a")).toBe("not-started");
    // A twin tried in form B starts form A's row.
    expect(status(apply(emptyProgress(), missTask("rc-part1-b", 0)), "rc-part1-a")).toBe("in-progress");
  });

  // [what the student did, Next up]
  const nextUp: [string, Update[], string | undefined][] = [
    ["nothing yet", [], "before-we-continue"],
    ["read the intro", [read("before-we-continue")], "rc-part1-a-questions"],
    ["answered the questions", [read("before-we-continue"), allQuestions("rc-part1-a-questions")], "rc-part1-a"],
    ["tried 8 of the 9 tasks", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a").slice(0, 8)], "rc-part1-a"],
    ["passed everything in Part 1", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a")], "rc-miniboss-a"],
    ["missed a task", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a", [2])], "rc-review"],
    ["missed 3 questions", [read("before-we-continue"), allQuestions("rc-part1-a-questions", [0, 1, 2]), ...passAll("rc-part1-a")], "rc-review"],
    ["missed a task, read the notes", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a", [2]), read("rc-review")], "rc-miniboss-a"],
    ["did the mini-boss", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a"), boss("rc-miniboss-a")], "rc-explain"],
    ["did the core", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a"), boss("rc-miniboss-a"), answer("rc-explain", [0])], undefined],
    ["did the core with a task missed", [read("before-we-continue"), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a", [2]), read("rc-review"), boss("rc-miniboss-a"), answer("rc-explain", [0])], "rc-review"],
  ];
  it.each(nextUp)("Next up follows the intro, the questions, the tasks, the notes after a miss, the mini-boss, the explain: %s", (_, updates, want) => {
    expect(nextUpItem(U, items, apply(emptyProgress(), ...updates))?.id).toBe(want);
  });

  it("sends Continue after Part 1 A to Mar'tu's notes only when something was missed, otherwise to the mini-boss", () => {
    const clean = apply(emptyProgress(), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a"));
    expect(part1Missed(U, items, plan, clean)).toBe(false);
    expect(afterPart1(U, items, plan, clean)).toBe("rc-miniboss-a");
    const missed = apply(emptyProgress(), allQuestions("rc-part1-a-questions"), ...passAll("rc-part1-a", [8]));
    expect(afterPart1(U, items, plan, missed)).toBe("rc-review");
    const fewQuestions = apply(emptyProgress(), allQuestions("rc-part1-a-questions", [0, 5, 9]), ...passAll("rc-part1-a"));
    expect(afterPart1(U, items, plan, fewQuestions)).toBe("rc-review");
  });

  it("goes Next from item to item along the core, a form's questions to its tasks (registry nextHref)", () => {
    const href = (id: string) => nextHref(real, { id });
    expect(href("before-we-continue")).toBe("/intro-python/readiness-check/rc-part1-a-questions");
    expect(href("rc-part1-a-questions")).toBe("/intro-python/readiness-check/rc-part1-a");
    expect(href("rc-part1-a")).toBe("/intro-python/readiness-check/rc-miniboss-a");
    expect(href("rc-review")).toBe("/intro-python/readiness-check/rc-miniboss-a");
    expect(href("rc-miniboss-a")).toBe("/intro-python/readiness-check/rc-explain");
    expect(href("rc-explain")).toBe("/intro-python/readiness-check");
    expect(href("rc-part1-b-questions")).toBe("/intro-python/readiness-check/rc-part1-b");
    expect(href("rc-part1-b")).toBe("/intro-python/readiness-check");
    expect(href("rc-recheck-questions")).toBe("/intro-python/readiness-check/rc-recheck");
    // Every other unit: as before (the Quick Check is skipped).
    const lists = allUnits.find((entry) => entry.id === "lists")!;
    const last = lists.items.filter((entry) => entry.kind !== "testout").at(-2)!;
    expect(nextHref(lists, last)).not.toContain("qc");
  });
});

describe("site request 1: the parallel forms lock until Part 1 A and Mar'tu's notes; the re-check waits a week", () => {
  const rowsOf = (progress: CourseProgress, now = 0, teacher = false) =>
    Object.fromEntries(items.map((entry) => [entry.id, readinessRowState(U, items, plan, entry, progress, now, teacher)]));

  // [what the student did, the B and C rows]
  const locks: [string, Update[], "locked" | "open"][] = [
    ["nothing", [], "locked"],
    ["tried every task, no questions yet", [...passAll("rc-part1-a", [3])], "locked"],
    ["tried Part 1 A, not the notes", [allQuestions("rc-part1-a-questions", [1]), ...passAll("rc-part1-a", [3])], "locked"],
    ["opened the notes, Part 1 A not tried", [read("rc-review"), allQuestions("rc-part1-a-questions")], "locked"],
    ["tried Part 1 A and opened the notes", [allQuestions("rc-part1-a-questions", [1]), ...passAll("rc-part1-a", [3]), read("rc-review")], "open"],
  ];
  it.each(locks)("rows for forms B and C and their questions: %s", (_, updates, want) => {
    const progress = apply(emptyProgress(), ...updates);
    const rows = rowsOf(progress);
    for (const id of ["rc-part1-b", "rc-part1-b-questions", "rc-part1-c", "rc-part1-c-questions"]) expect(rows[id], id).toBe(want);
    for (const id of ["before-we-continue", "rc-part1-a-questions", "rc-part1-a", "rc-review", "rc-miniboss-a", "rc-explain", "rc-miniboss-b", "rc-trial-ember-ward"]) {
      expect(rows[id], id).toBe("open");
    }
    expect(formsUnlocked(U, items, plan, progress)).toBe(want === "open");
    // The teacher's preview sees every row open.
    expect(rowsOf(progress, 0, true)["rc-part1-b"]).toBe("open");
  });

  it("names the lock in the teacher's words", () => {
    expect(LOCKED_FORM_TEXT).toBe("Opens after Part 1 A and Mar'tu's notes");
  });

  it("counts a task tried only once it was run with the student's own code", () => {
    const opened = apply(emptyProgress(), ...tasksOf("rc-part1-a").map((id) => exercise(`${U}/rc-part1-a/${id}`, { firstSeenAt: 1 })), allQuestions("rc-part1-a-questions"));
    expect(part1Tried(U, items, plan, opened)).toBe(false);
    expect(part1Tried(U, items, plan, apply(opened, ...passAll("rc-part1-a", [0, 1, 2, 3, 4, 5, 6, 7, 8])))).toBe(true);
  });

  it("hides the re-check until the core was done about a week ago, or the teacher opened it", () => {
    const day = 24 * 60 * 60 * 1000;
    const hidden = (progress: CourseProgress, now: number) => [rowsOf(progress, now)["rc-recheck"], rowsOf(progress, now)["rc-recheck-questions"]];
    expect(hidden(emptyProgress(), 30 * day)).toEqual(["hidden", "hidden"]);
    const done = apply(emptyProgress(), withReadiness(U, { coreDoneAt: 10 * day }));
    expect(hidden(done, 16 * day)).toEqual(["hidden", "hidden"]);
    expect(hidden(done, 10 * day + RECHECK_AFTER_MS)).toEqual(["open", "open"]);
    const teacher = apply(emptyProgress(), withReadiness(U, { recheckOpen: true }));
    expect(recheckOpen(U, teacher, 0)).toBe(true);
    expect(hidden(teacher, 0)).toEqual(["open", "open"]);
    expect(rowsOf(emptyProgress(), 0, true)["rc-recheck"]).toBe("open");
  });

  it("keeps the readiness dates through a save, and drops a broken one", () => {
    const saved = normalizeProgress(JSON.parse(JSON.stringify(apply(emptyProgress(), withReadiness(U, { coreDoneAt: 5, recheckOpen: true })))));
    expect(saved.readiness?.[U]).toEqual({ coreDoneAt: 5, recheckOpen: true });
    expect(normalizeProgress({ ...emptyProgress(), readiness: { [U]: { coreDoneAt: "soon", recheckOpen: "yes" } } }).readiness?.[U]).toEqual({});
    expect(normalizeProgress(emptyProgress()).readiness).toBeUndefined();
    // Setting the same value twice changes nothing.
    const once = apply(emptyProgress(), withReadiness(U, { recheckOpen: true }));
    expect(withReadiness(U, { recheckOpen: true })(once)).toBe(once);
  });
});

describe("site request 2: a retake draws the next form's questions, and its score counts for Part 1", () => {
  it("cycles A, then B, then C, then A again, for the parallel forms only", () => {
    expect(nextQuestionsForm(plan, "rc-part1-a-questions")).toBe("rc-part1-b-questions");
    expect(nextQuestionsForm(plan, "rc-part1-b-questions")).toBe("rc-part1-c-questions");
    expect(nextQuestionsForm(plan, "rc-part1-c-questions")).toBe("rc-part1-a-questions");
    expect(nextQuestionsForm(plan, "rc-recheck-questions")).toBeUndefined();
    expect(nextQuestionsForm(plan, "rc-explain")).toBeUndefined();
    expect(formName(item("rc-part1-b-questions").title)).toBe("Form B");
  });

  // [the attempts, right positions in each form, how many Part 1 positions count as right]
  const scores: [string, Record<string, number[]>, number, boolean][] = [
    ["form A, 9 of 12", { "rc-part1-a-questions": [0, 1, 2, 3, 4, 5, 6, 7, 8] }, 9, false],
    ["form A 9, then form B gets the other 3", { "rc-part1-a-questions": [0, 1, 2, 3, 4, 5, 6, 7, 8], "rc-part1-b-questions": [9, 10, 11] }, 12, true],
    ["form A 8, form B the same 8 again", { "rc-part1-a-questions": [0, 1, 2, 3, 4, 5, 6, 7], "rc-part1-b-questions": [0, 1, 2, 3, 4, 5, 6, 7] }, 8, false],
    ["form A 8, form C two more", { "rc-part1-a-questions": [0, 1, 2, 3, 4, 5, 6, 7], "rc-part1-c-questions": [8, 9] }, 10, true],
    ["the re-check does not count", { "rc-part1-a-questions": [0, 1, 2, 3, 4, 5, 6, 7, 8], "rc-recheck-questions": [0, 1, 2, 3] }, 9, false],
  ];
  it.each(scores)("counts a question right in any form: %s", (_, right, count, met) => {
    const progress = apply(emptyProgress(), ...Object.entries(right).map(([quiz, ats]) => answer(quiz, ats)));
    expect(readinessQuestions(U, items, plan, progress)).toEqual({ right: count, needed: 10, total: 12, met });
  });

  it("saves a right answer as soon as it is checked, with no attempt counted (a twin can be answered alone)", () => {
    const key = `${U}/rc-part1-b-questions`;
    const progress = apply(emptyProgress(), withQuizRight(key, questionsOf("rc-part1-b-questions")[0]));
    expect(progress.quizzes[key]).toEqual({ best: 0, attempts: 0, right: [questionsOf("rc-part1-b-questions")[0]] });
    expect(apply(progress, withQuizRight(key, questionsOf("rc-part1-b-questions")[0]))).toBe(progress);
    // Form A's question 1 missed, its twin in form B right: Part 1 counts it.
    const counted = apply(progress, answer("rc-part1-a-questions", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]));
    expect(readinessQuestions(U, items, plan, counted)?.right).toBe(12);
    expect(normalizeProgress(JSON.parse(JSON.stringify(progress))).quizzes[key]).toEqual(progress.quizzes[key]);
  });

  it("keeps the questions right in any attempt, and the explained ones, through a save", () => {
    const key = `${U}/rc-part1-a-questions`;
    const first = apply(emptyProgress(), withQuiz(key, 50, {}, ["a", "b"]));
    const second = apply(first, withQuiz(key, 25, {}, ["c"]));
    expect(second.quizzes[key]).toMatchObject({ best: 50, attempts: 2, right: ["a", "b", "c"] });
    const explained = apply(emptyProgress(), withQuizExplained(key, "a"), withQuizExplained(key, "b"), withQuizExplained(key, "a"));
    expect(explained.quizzes[key]).toEqual({ best: 0, attempts: 0, explained: ["a", "b"] });
    // An explained question before any finished attempt is not an attempt: the quiz is still not started.
    expect(status(explained, "rc-part1-a-questions")).toBe("not-started");
    const saved = normalizeProgress(JSON.parse(JSON.stringify(apply(second, withQuizExplained(key, "z")))));
    expect(saved.quizzes[key]).toMatchObject({ right: ["a", "b", "c"], explained: ["z"] });
    // An older save's quiz, with no right or explained ids, reads as before.
    expect(normalizeProgress({ ...emptyProgress(), quizzes: { [key]: { best: 50, attempts: 1 } } }).quizzes[key]).toEqual({ best: 50, attempts: 1 });
    // Every other quiz is recorded exactly as before (no right ids passed).
    expect(apply(emptyProgress(), withQuiz("lists/quiz", 80, { q: "1" })).quizzes["lists/quiz"]).toEqual({ best: 80, attempts: 1, lastAnswers: { q: "1" } });
  });
});

describe("site requests 3 and 4: per-item Readiness scoring with twins, and a pass after Compare", () => {
  const part1 = (missedTasks: number[], missedQuestions: number[]): Update[] => [
    allQuestions("rc-part1-a-questions", missedQuestions),
    ...passAll("rc-part1-a", missedTasks),
  ];

  // [what happened, Part 1 score of 13, verdict]
  const verdicts: [string, Update[], number, string | null][] = [
    ["every item, the mini-boss on your own", [...part1([], []), boss("rc-miniboss-a")], 13, "ready"],
    ["two items missed, the mini-boss on your own", [...part1([0, 8], []), boss("rc-miniboss-a")], 11, "review-list"],
    ["item 1 and item 2 missed", [...part1([0], [0]), boss("rc-miniboss-a")], 11, "ready"],
    ["item 6 at 3 of 4 parts (the `in` question missed): it still counts", [...part1([], [5]), boss("rc-miniboss-a")], 13, "ready"],
    [
      "item 6 at 2 of 4 parts (one sheet step and the `in` question missed)",
      [...part1([3], [5]), exercise(`${U}/rc-part1-a/read-the-sheet`, { passed: ["a", "b"], failedRuns: 1 }), boss("rc-miniboss-a")],
      12,
      "review-list",
    ],
    [
      "item 6 at 3 of 4 parts (one sheet step missed)",
      [...part1([3], []), exercise(`${U}/rc-part1-a/read-the-sheet`, { passed: ["a", "b"], failedRuns: 1 }), boss("rc-miniboss-a")],
      13,
      "ready",
    ],
    ["item 13 missed (required)", [...part1([8], []), boss("rc-miniboss-a")], 12, "review-list"],
    ["four items missed", [...part1([0, 6, 7], [0]), boss("rc-miniboss-a")], 9, "review-list"],
    ["five items missed", [...part1([0, 6, 7, 8], [0]), boss("rc-miniboss-a")], 8, "review-first"],
    ["every item, the mini-boss with Mar'tu's version", [...part1([], []), boss("rc-miniboss-a", true)], 13, "review-list"],
    ["every item, A with Mar'tu's version, then B on your own", [...part1([], []), boss("rc-miniboss-a", true), boss("rc-miniboss-b")], 13, "review-list"],
    ["every item, no mini-boss yet", [...part1([], [])], 13, null],
    ["a missed task's twin passed in form B", [...part1([8], []), passTask("rc-part1-b", 8), boss("rc-miniboss-a")], 13, "ready"],
    ["a missed question's twin right in form C", [...part1([], [0]), answer("rc-part1-c-questions", [0]), boss("rc-miniboss-a")], 13, "ready"],
  ];
  it.each(verdicts)("%s", (_, updates, score, verdict) => {
    const result = readinessResult(U, items, plan, skills, apply(emptyProgress(), ...updates));
    expect(result.tried).toBe(true);
    expect(result.score).toBe(score);
    expect(result.verdict).toBe(verdict);
  });

  it("has no result before Part 1 A was tried", () => {
    const result = readinessResult(U, items, plan, skills, apply(emptyProgress(), boss("rc-miniboss-a")));
    expect(result.tried).toBe(false);
    expect(result.visible).toBe(false);
    expect(result.verdict).toBeNull();
  });

  it("names a task skipped without a Run, opens nothing on a visit alone, and still gives a result once a mini-boss is done", () => {
    // 8 of 12 questions right, tasks 1-6 and 8 passed, task 7 run and missed, task 9 opened and skipped (no Run).
    const skipped = exercise(`${U}/rc-part1-a/${tasksOf("rc-part1-a")[8]}`, { firstSeenAt: 1, failedRuns: 0 });
    const start = apply(emptyProgress(), answer("rc-part1-a-questions", [0, 1, 2, 3, 4, 5, 6, 7]), ...passAll("rc-part1-a", [6, 8]), skipped);
    expect(untriedTasks(U, items, plan, start)).toEqual([8]);
    expect(part1Tried(U, items, plan, start)).toBe(false);
    // The form's end and the lock say exactly what is missing: Run task 9 once, even unfinished.
    expect(part1Missing(U, items, plan, start)).toBe(
      "Not tried yet: Task 9, *Write a function from its goal*. Type your best try, even if it is not finished, and press Run once. That counts as tried.",
    );
    const afterNotes = apply(start, read("rc-review"));
    expect(formsUnlocked(U, items, plan, afterNotes)).toBe(false);
    expect(lockReason(U, items, plan, afterNotes)).toContain("Task 9, *Write a function from its goal*");
    expect(readinessRowState(U, items, plan, item("rc-part1-b"), afterNotes, 0)).toBe("locked");
    // Every task was opened and the questions answered: the result shows, waiting for the mini-boss.
    expect(readinessResult(U, items, plan, skills, afterNotes)).toMatchObject({ visible: true, tried: false, untried: [8], verdict: null });
    // The mini-boss on the student's own: the result is in, with the untried task counted as missed (never Ready).
    const result = readinessResult(U, items, plan, skills, apply(afterNotes, boss("rc-miniboss-a")));
    expect(result).toMatchObject({ visible: true, tried: false, untried: [8], miniBoss: "on-your-own", verdict: "review-list" });
    expect(result.skills.find((entry) => entry.skill.n === 13)?.passed).toBe(false);
    // One Run of the student's own try: the task counts as tried, the forms open, and nothing is left to name.
    const ran = apply(afterNotes, missTask("rc-part1-a", 8));
    expect(part1Tried(U, items, plan, ran)).toBe(true);
    expect(formsUnlocked(U, items, plan, ran)).toBe(true);
    expect(lockReason(U, items, plan, ran)).toBeNull();
    // A fresh start names nothing (the lock's own words are enough), and neither does a long list.
    expect(part1Missing(U, items, plan, emptyProgress())).toBeNull();
    expect(part1Missing(U, items, plan, apply(emptyProgress(), passTask("rc-part1-a", 0)))).toBeNull();
    // Every task run, the questions not answered: only the questions are named.
    expect(part1Missing(U, items, plan, apply(emptyProgress(), ...passAll("rc-part1-a")))).toBe("Answer Part 1 A's questions once.");
  });

  it("carries form A's task titles in the outline, for the names above", () => {
    expect(item("rc-part1-a").exercises?.[8]).toEqual({ id: tasksOf("rc-part1-a")[8], title: "Write a function from its goal" });
    const lists = allUnits.find((entry) => entry.id === "lists")!;
    for (const entry of unitOutline(lists).items) for (const task of entry.exercises ?? []) expect(task.title, entry.id).toBeUndefined();
  });

  it("counts Mar'tu's version of either mini-boss, opened before the pass that counts (the two are one program)", () => {
    const pass = { passedNow: ["a"], newlyPassed: ["a"], allPassed: true, failed: false };
    // Compare on A, A left unfinished, then B passed: B's pass is recorded with Mar'tu's version.
    const bPass = applyRun(emptyExercise(), pass, { compareElsewhere: true });
    expect(bPass.doneWithCompare).toBe(true);
    const progress = apply(
      emptyProgress(),
      ...part1([], []),
      exercise(`${U}/rc-miniboss-a`, { solutionShown: true }),
      exercise(`${U}/rc-miniboss-b`, bPass),
    );
    const result = readinessResult(U, items, plan, skills, progress);
    expect(result).toMatchObject({ miniBoss: "with-compare", verdict: "review-list" });
    expect(result.nextBoss).toBeUndefined();
    // Compare on B, B left unfinished, then A passed: the same, and B is not offered "on your own" (its answer was shown).
    const aPass = applyRun(emptyExercise(), pass, { compareElsewhere: true });
    const reverse = readinessResult(
      U,
      items,
      plan,
      skills,
      apply(emptyProgress(), ...part1([], []), exercise(`${U}/rc-miniboss-b`, { solutionShown: true }), exercise(`${U}/rc-miniboss-a`, aPass)),
    );
    expect(reverse).toMatchObject({ miniBoss: "with-compare", verdict: "review-list" });
    expect(reverse.nextBoss).toBeUndefined();
    // Compare on B opened only after A was passed on the student's own: still Ready.
    expect(applyRun({ ...emptyExercise(), done: true, passed: ["a"] }, { ...pass, newlyPassed: [] }, { compareElsewhere: true }).doneWithCompare).toBeUndefined();
    const later = apply(emptyProgress(), ...part1([], []), boss("rc-miniboss-a"), exercise(`${U}/rc-miniboss-b`, { solutionShown: true }));
    expect(readinessResult(U, items, plan, skills, later).verdict).toBe("ready");
  });

  it("says every skill only with a full score, and on your own only when the mini-boss used no Help past Where to look", () => {
    expect(readinessVerdictText("ready", 13, 13, true)).toBe("Ready. You showed Mar'tu every skill the next campaign part needs, on your own.");
    expect(readinessVerdictText("ready", 12, 13, true)).toBe("Ready. You showed Mar'tu what the next campaign part needs, on your own.");
    expect(readinessVerdictText("ready", 12, 13, false)).toBe("Ready. You showed Mar'tu what the next campaign part needs.");
    expect(readinessVerdictText("ready", 13, 13, false)).not.toContain("on your own");
    expect(readinessVerdictText("review-list", 10, 13, true)).toMatch(/^Ready, with a review list\./);
    expect(readinessVerdictText("review-first", 6, 13, true)).toMatch(/^Review first\./);
  });

  it("names the missed items, the parts they passed, and the twin form to try next", () => {
    const progress = apply(emptyProgress(), ...part1([3, 8], [5]), boss("rc-miniboss-a"));
    const result = readinessResult(U, items, plan, skills, progress);
    const six = result.skills.find((entry) => entry.skill.n === 6)!;
    expect(six).toMatchObject({ passed: false, partsPassed: 0, parts: 4, twinForm: "rc-part1-b" });
    const thirteen = result.skills.find((entry) => entry.skill.n === 13)!;
    expect(thirteen).toMatchObject({ passed: false, twinForm: "rc-part1-b" });
    // Tried in B and missed again: C is next.
    const again = readinessResult(U, items, plan, skills, apply(progress, missTask("rc-part1-b", 8)));
    expect(again.skills.find((entry) => entry.skill.n === 13)?.twinForm).toBe("rc-part1-c");
  });

  it("records a pass after Compare as with Mar'tu's version, names Mini-boss B next, and opens Compare after 5 minutes only", () => {
    const opened: ExerciseProgress = { ...emptyExercise(), solutionShown: true, failedRuns: 9 };
    expect(applyRun(opened, { passedNow: ["a"], newlyPassed: ["a"], allPassed: true, failed: false }).doneWithCompare).toBe(true);
    expect(applyRun(emptyExercise(), { passedNow: ["a"], newlyPassed: ["a"], allPassed: true, failed: false }).doneWithCompare).toBeUndefined();
    // Compare opened after the pass is not "with Mar'tu's version".
    const passed = applyRun(emptyExercise(), { passedNow: ["a"], newlyPassed: ["a"], allPassed: true, failed: false });
    expect(applyRun({ ...passed, solutionShown: true }, { passedNow: ["a"], newlyPassed: [], allPassed: true, failed: false }).doneWithCompare).toBeUndefined();
    const result = readinessResult(U, items, plan, skills, apply(emptyProgress(), ...part1([], []), boss("rc-miniboss-a", true)));
    expect(result.miniBoss).toBe("with-compare");
    expect(result.nextBoss).toBe("rc-miniboss-b");
    // Campaign mode: 5 minutes on the exercise, never a count of failed runs.
    const settings = campaignModeSettings(itemSettings(), true);
    const gate = (activeMs: number, failedRuns: number) => solutionUnlocked({ support: "light", activeMs, failedRuns, ...settings });
    expect(gate(60_000, 50)).toBe(false);
    expect(gate(5 * 60_000, 0)).toBe(true);
    // Everywhere else: as before (4 failed runs open it).
    const usual = campaignModeSettings(itemSettings(), false);
    expect(solutionUnlocked({ support: "light", activeMs: 0, failedRuns: 4, ...usual })).toBe(true);
  });
});

describe("site request 5: campaign mode labels the last rung Last hint", () => {
  const checkpoint = { hints: ["Look at comment 1.", "A function in a dictionary runs ...", "Read the effect from `ward`."] };
  it("labels the last rung Last hint in a solo project or challenge with light support, and Show me how everywhere else", () => {
    const campaign = helpRungs(checkpoint, { anotherWayCount: 0, hasAssemble: false, solo: true, campaignMode: true });
    expect(campaign.map((rung) => rung.label)).toEqual(["Where to look", "Teach me", LAST_HINT_LABEL, "Compare with Mar'tu's version"]);
    const usual = helpRungs(checkpoint, { anotherWayCount: 0, hasAssemble: false, solo: true });
    expect(usual.find((rung) => rung.kind === "how")?.label).toBe("Show me how");
    expect(isCampaignMode({ solo: true }, "light", "project")).toBe(true);
    expect(isCampaignMode({ solo: true }, "light", "challenge")).toBe(true);
    expect(isCampaignMode({ solo: true }, "light", "lesson")).toBe(false);
    expect(isCampaignMode({ solo: false }, "light", "project")).toBe(false);
    expect(isCampaignMode({ solo: true }, "full", "project")).toBe(false);
  });

  it("matches exactly Unit 10's mini-bosses and trial: no earlier unit has a solo project or challenge", () => {
    const campaign = allUnits.flatMap((entry) =>
      entry.items.filter((candidate) => (candidate.kind === "project" || candidate.kind === "challenge") && isCampaignMode(candidate, candidate.support, candidate.kind)).map((candidate) => `${entry.id}/${candidate.id}`),
    );
    expect(campaign).toEqual(["readiness-check/rc-miniboss-a", "readiness-check/rc-miniboss-b", "readiness-check/rc-trial-ember-ward"]);
  });
});

describe("site request 10 (optional): rc-explain's own words first, ungraded and saved per student", () => {
  it("keeps the words through a save and a finished attempt, and never counts them as an attempt", () => {
    const key = `${U}/rc-explain`;
    const typed = apply(emptyProgress(), withOwnWords(key, "explain-the-pay-line", "It takes the cost off the hero's mana."));
    expect(status(typed, "rc-explain")).toBe("not-started");
    const finished = apply(typed, answer("rc-explain", [0]));
    expect(finished.quizzes[key]?.ownWords).toEqual({ "explain-the-pay-line": "It takes the cost off the hero's mana." });
    expect(normalizeProgress(JSON.parse(JSON.stringify(finished))).quizzes[key]?.ownWords).toEqual({ "explain-the-pay-line": "It takes the cost off the hero's mana." });
    expect(normalizeProgress({ ...emptyProgress(), quizzes: { [key]: { best: 0, attempts: 0, ownWords: { a: 3 } } } }).quizzes[key]?.ownWords).toEqual({});
    expect(plan.explain).toBe("rc-explain");
  });
});

describe("the page props a readiness unit's items get", () => {
  it("gives quizzes their question ids only in a readiness unit", () => {
    expect(unitSummary(real).items.find((entry) => entry.id === "rc-part1-a-questions")?.questionIds).toHaveLength(12);
    const lists = allUnits.find((entry) => entry.id === "lists")!;
    for (const entry of unitSummary(lists).items) expect(entry.questionIds, entry.id).toBeUndefined();
    for (const entry of unitOutline(lists).items) expect(entry.questionIds, entry.id).toBeUndefined();
  });
});
