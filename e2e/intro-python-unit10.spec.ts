/**
 * Unit 10 ("Campaign Readiness Check: Before We Continue") in a real browser: what the teacher's ruling on Unit 10
 * asked of the site (src/lib/course/readiness.ts).
 *
 *  - Site request 1, the MUST: a unit that holds a required test-out has no Quick Check offer; its forms are rows in
 *    ITEMS order, Part 1 A and its questions core; passing a form never tests the unit out, so the mini-boss and
 *    rc-explain stay the student's, and Ready needs the mini-boss; forms B and C are locked rows until Part 1 A was tried
 *    and Mar'tu's notes were opened; the re-check is hidden until it is due (or the teacher opens it); Continue after
 *    Part 1 A goes to the notes only after a miss.
 *  - Site request 2: a failed questions quiz's retake draws the next form's questions, which count for Part 1, and a
 *    question's answer shows once.
 *  - Site requests 3 and 4: the Readiness result, twins counting; a mini-boss pass after Compare is "with Mar'tu's
 *    version" and names Mini-boss B; Compare opens after 5 minutes only.
 *  - Site request 5: campaign mode's last rung is "Last hint".
 *  - Site requests 6-9: the explainer's lean kinds for the unit's own slips, and Unit 3's full words for the same code.
 *
 * Every code below is one of the unit's own solutions or wrong answers, read from the exported JSON and the harness
 * sidecar, so the browser runs exactly what python3 proved. Browser parity for every exercise and quiz of the unit is
 * in intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "readiness-check";
const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");

type Code = string | string[];
type Question = { id: string; type: string; answer: number | string; choices?: string[] };
type RawItem = {
  id: string;
  kind: string;
  title: string;
  optional?: boolean;
  questionsToPass?: number;
  solution?: Code;
  exercises?: { id: string; checkpoints: { id: string }[]; solution: Code }[];
  questions?: Question[];
};

const unit = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.json`), "utf8")) as { order: number; published: boolean; items: RawItem[] };
const sidecar = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.verify.json`), "utf8")) as {
  exercises: Record<string, { wrongAnswers?: { why: string; code: Code }[] }>;
};

const codeText = (value: Code | undefined) => (Array.isArray(value) ? `${value.join("\n")}\n` : (value ?? ""));
const item = (id: string): RawItem => {
  const found = unit.items.find((entry) => entry.id === id);
  if (!found) throw new Error(`no item ${id}`);
  return found;
};
const tasks = (form: string) => item(form).exercises ?? [];

/** The unit's own wrong answer for `key` ("<item>/<exercise>") whose `why` contains `why` (a whole `why` wins). */
function wrongAnswer(key: string, why: string): string {
  const near = (sidecar.exercises[key]?.wrongAnswers ?? []).filter((entry) => entry.why.includes(why));
  const exact = near.filter((entry) => entry.why === why);
  const found = exact.length === 1 ? exact : near;
  expect(found, `${key}: one wrong answer about "${why}"`).toHaveLength(1);
  return codeText(found[0].code);
}

async function setCode(page: Page, code: string) {
  await replaceEditor(page, code);
  await expect
    .poll(() => page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line').allTextContents())
    .toEqual(code.split("\n"));
}

async function runAndWait(page: Page, runNumber: number) {
  await page.getByTestId("run").click();
  await expect(page.getByTestId("run-count")).toHaveText(new RegExp(`Run ${runNumber} finished`), { timeout: 60_000 });
}

async function open(page: Page, itemId: string, exerciseId?: string) {
  await page.goto(`/intro-python/${UNIT_ID}/${itemId}${exerciseId ? `#${exerciseId}` : ""}`);
  await expect(page.getByTestId("exercise-player")).toBeVisible();
  await pythonReady(page);
}

type Saved = {
  exercises?: Record<string, unknown>;
  quizzes?: Record<string, unknown>;
  read?: Record<string, true>;
  readiness?: Record<string, unknown>;
};

/** Start with this saved progress ("Show me more"), on the course map. */
async function startWith(page: Page, saved: Saved = {}) {
  await page.goto("/intro-python");
  await page.evaluate(
    ([key, value]) => window.localStorage.setItem(key, value),
    [
      PROGRESS_KEY,
      JSON.stringify({ version: 1, exercises: {}, quizzes: {}, read: {}, testedOut: {}, settings: { preset: "more" }, ...saved }),
    ] as const,
  );
}

async function saved(page: Page): Promise<Record<string, Record<string, unknown>>> {
  return page.evaluate((key) => JSON.parse(window.localStorage.getItem(key) ?? "{}"), PROGRESS_KEY);
}

/** Form A's tasks as saved progress: every task done but those in `missed` (tried once, not passed). */
function formTasks(form: string, missed: number[] = []): Record<string, unknown> {
  return Object.fromEntries(
    tasks(form).map((task, at) => [
      `${UNIT_ID}/${form}/${task.id}`,
      missed.includes(at)
        ? { passed: [], done: false, hintsUsed: {}, failedRuns: 1 }
        : { passed: task.checkpoints.map((checkpoint) => checkpoint.id), done: true, hintsUsed: {}, failedRuns: 0 },
    ]),
  );
}

/** A questions quiz as saved progress: one attempt, these positions right. */
function quizRight(quiz: string, right: number[]): Record<string, unknown> {
  const ids = (item(quiz).questions ?? []).map((question) => question.id);
  return { [`${UNIT_ID}/${quiz}`]: { best: Math.round((100 * right.length) / ids.length), attempts: 1, right: right.map((at) => ids[at]) } };
}
const all12 = Array.from({ length: 12 }, (_, at) => at);

/** Answer a quiz on its page: the keyed answer, except at `wrongAt`, where a wrong one. Ends on the results. */
async function answerQuiz(page: Page, quiz: string, wrongAt: number[] = []) {
  await page.goto(`/intro-python/${UNIT_ID}/${quiz}`);
  const questions = item(quiz).questions ?? [];
  for (const [at, question] of questions.entries()) {
    await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of ${questions.length}`);
    const wrong = wrongAt.includes(at);
    if (question.type === "mc") {
      const answer = question.answer as number;
      await page.getByTestId(`quiz-choice-${question.id}-${wrong ? (answer + 1) % (question.choices?.length ?? 2) : answer}`).click();
    } else if (question.choices?.length) {
      const right = question.choices.indexOf(String(question.answer));
      await page.getByTestId(`quiz-choice-${question.id}-${wrong ? (right + 1) % question.choices.length : right}`).click();
    } else {
      await page.getByTestId("quiz-answer-input").fill(wrong ? "not this" : String(question.answer));
    }
    await page.getByTestId("quiz-check").click();
    await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", wrong ? "false" : "true");
    await page.getByTestId("quiz-next").click();
  }
  await expect(page.getByTestId("quiz-results")).toBeVisible();
}

test.describe("Intro to Python, Unit 10: the Readiness Check", () => {
  test("the unit page: no Quick Check offer, Part 1 as core rows in ITEMS order, forms B and C locked, the re-check hidden", async ({ page }) => {
    expect(unit.published).toBe(true);
    expect(unit.order).toBe(10);
    await startWith(page);
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Campaign Readiness Check");
    await expect(page.getByTestId("quick-check-offer")).toHaveCount(0);
    await expect(page.getByTestId("testout-start")).toHaveCount(0);
    const rows = page.locator('[data-testid^="item-row-"]');
    const shown = unit.items.filter((entry) => !["rc-recheck", "rc-recheck-questions"].includes(entry.id)).map((entry) => `item-row-${entry.id}`);
    expect(await rows.evaluateAll((els) => els.map((el) => el.getAttribute("data-testid")))).toEqual(shown);
    // Part 1 A and its questions are core rows, with links; the kind says Tasks, never Quick Check.
    for (const id of ["rc-part1-a-questions", "rc-part1-a"]) {
      await expect(page.getByTestId(`item-row-${id}`)).not.toContainText("Optional");
      await expect(page.getByTestId(`item-link-${id}`)).toBeVisible();
    }
    await expect(page.getByTestId("item-row-rc-part1-a")).toContainText("Tasks");
    await expect(page.getByTestId("unit-page")).not.toContainText("Quick Check");
    // Forms B and C and their questions: locked, in the teacher's words.
    for (const id of ["rc-part1-b-questions", "rc-part1-b", "rc-part1-c-questions", "rc-part1-c"]) {
      await expect(page.getByTestId(`item-locked-${id}`)).toHaveText("🔒 Opens after Part 1 A and Mar'tu's notes");
      await expect(page.getByTestId(`item-link-${id}`)).toHaveCount(0);
    }
    // Next up: the intro. Nothing is "Tested out", and there is no result before Part 1.
    await expect(page.getByTestId("item-row-before-we-continue")).toContainText("Next up");
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Not started");
    await expect(page.getByTestId("readiness-result")).toHaveCount(0);

    // The teacher opens the re-check with a link; it stays open for this student.
    await page.goto(`/intro-python/${UNIT_ID}?recheck=open`);
    await expect(page.getByTestId("item-row-rc-recheck")).toBeVisible();
    await expect(page.getByTestId("item-row-rc-recheck-questions")).toBeVisible();
    await expect.poll(async () => (await saved(page)).readiness?.[UNIT_ID]).toEqual({ recheckOpen: true });
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-row-rc-recheck")).toBeVisible();
    // The teacher's preview shows every row open.
    await startWith(page);
    await page.goto(`/intro-python/${UNIT_ID}?preview=1`);
    await expect(page.getByTestId("item-link-rc-part1-b")).toBeVisible();
    await expect(page.getByTestId("item-row-rc-recheck")).toBeVisible();
  });

  test("passing form A in full marks neither the mini-boss nor rc-explain, and Ready needs the mini-boss", async ({ page }) => {
    test.setTimeout(480_000);
    await startWith(page, { read: { [`${UNIT_ID}/before-we-continue`]: true } });
    // The questions first, as the unit page lists them.
    await answerQuiz(page, "rc-part1-a-questions");
    await expect(page.getByTestId("quiz-readiness")).toHaveAttribute("data-met", "true");
    await expect(page.getByTestId("quiz-quick-check")).toHaveCount(0);
    await expect(page.getByTestId("quiz-next-item")).toHaveAttribute("href", /\/readiness-check\/rc-part1-a\/?$/);
    // Then the nine tasks, each with Mar'tu's version, in the browser.
    await open(page, "rc-part1-a");
    await expect(page.getByTestId("testout-intro")).toHaveAttribute("data-readiness", "true");
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "To pass Part 1: pass all 9 tasks, and get 10 of the 12 questions right. Stuck on a task? Type your best try, press Run once, then skip it and come back later. Tasks you pass stay ✓ done.",
    );
    for (const [at, task] of tasks("rc-part1-a").entries()) {
      await page.goto(`/intro-python/${UNIT_ID}/rc-part1-a#${task.id}`);
      await expect(page.getByTestId("exercise-label")).toHaveText(`Task ${at + 1} of 9`);
      await pythonReady(page);
      await setCode(page, codeText(task.solution));
      await runAndWait(page, 1);
      await expect(page.getByTestId("all-passed"), task.id).toBeVisible();
    }
    // Part 1 done: never "this unit counts as done"; Continue goes to the mini-boss (nothing was missed).
    await expect(page.getByTestId("readiness-finish")).toHaveText("✓ Part 1 is done. Next: the mini-boss.");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);
    await expect(page.getByTestId("item-continue")).toHaveAttribute("href", /\/readiness-check\/rc-miniboss-a\/?$/);
    await expect.poll(async () => (await saved(page)).testedOut?.[UNIT_ID] ?? false).toBe(false);

    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-status-rc-part1-a")).toHaveAttribute("data-status", "done");
    await expect(page.getByTestId("item-status-rc-miniboss-a")).toHaveAttribute("data-status", "not-started");
    await expect(page.getByTestId("item-status-rc-explain")).toHaveAttribute("data-status", "not-started");
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toHaveText("3 of 5 done");
    await expect(page.getByTestId("item-row-rc-miniboss-a")).toContainText("Next up");
    // The result waits for the mini-boss: no verdict without it.
    await expect(page.getByTestId("readiness-result")).toHaveAttribute("data-verdict", "waiting");
    await expect(page.getByTestId("readiness-score")).toHaveText("Part 1: you passed all 13 skills.");
    await expect(page.getByTestId("readiness-waiting")).toContainText("Next: Mini-boss: Hold the Lantern Ward. Then Mar'tu tells you the result.");

    // The mini-boss, on the student's own: then the result is Ready.
    await open(page, "rc-miniboss-a");
    await setCode(page, codeText(item("rc-miniboss-a").solution));
    await runAndWait(page, 1);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("campaign-result")).toHaveAttribute("data-with-compare", "false");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("readiness-result")).toHaveAttribute("data-verdict", "ready");
    await expect(page.getByTestId("readiness-verdict")).toContainText("Ready. You showed Mar'tu every skill the next campaign part needs, on your own.");
    await expect(page.getByTestId("item-status-rc-explain")).toHaveAttribute("data-status", "not-started");
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toHaveText("4 of 5 done");

    // rc-explain: the student's own words first (ungraded, kept), then the one click; then the core is done.
    await page.goto(`/intro-python/${UNIT_ID}/rc-explain`);
    await page.getByTestId("quiz-own-words").fill("It takes the ward's cost off the hero's mana and keeps it.");
    await expect.poll(async () => (await saved(page)).quizzes?.[`${UNIT_ID}/rc-explain`]).toMatchObject({ attempts: 0 });
    const explain = item("rc-explain").questions?.[0];
    await page.getByTestId(`quiz-choice-${explain?.id}-${explain?.answer}`).click();
    await page.getByTestId("quiz-check").click();
    await page.getByTestId("quiz-next").click();
    await expect(page.getByTestId("quiz-results")).toBeVisible();
    await expect(page.getByTestId("quiz-ready")).toHaveCount(0);
    await page.reload();
    await expect(page.getByTestId("quiz-own-words")).toHaveValue("It takes the ward's cost off the hero's mana and keeps it.");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toHaveText("Complete");
    await expect.poll(async () => typeof ((await saved(page)).readiness?.[UNIT_ID] as { coreDoneAt?: number } | undefined)?.coreDoneAt).toBe("number");
    await expect(page.getByTestId("item-row-rc-recheck")).toHaveCount(0);
  });

  test("after a miss: no retake link before the notes, Continue goes to Mar'tu's notes, the notes open forms B and C, and a twin question counts alone", async ({ page }) => {
    test.setTimeout(240_000);
    // Part 1 A's tasks tried, the last one missed; the questions not answered yet.
    await startWith(page, { read: { [`${UNIT_ID}/before-we-continue`]: true }, exercises: formTasks("rc-part1-a", [8]) });
    // Three questions wrong: 9 of 12 is not enough. Forms B and C are still locked, so no link pulls the student there.
    await answerQuiz(page, "rc-part1-a-questions", [0, 1, 2]);
    await expect(page.getByTestId("quiz-score")).toHaveText("9 of 12 right (75%)");
    await expect(page.getByTestId("quiz-readiness")).toHaveAttribute("data-met", "false");
    await expect(page.getByTestId("quiz-readiness")).toContainText("Part 1 needs 10 of the 12 questions right. 9 are right so far.");
    await expect(page.getByTestId("quiz-readiness")).toContainText("Form B opens after Part 1 A and Mar'tu's notes.");
    await expect(page.getByTestId("quiz-retake")).toHaveCount(0);
    await expect(page.getByTestId("quiz-retake-next-form")).toHaveCount(0);

    // A retake of form A's questions: an answer shown once is never shown again, and a remembered answer never counts.
    const quizA = `${UNIT_ID}/rc-part1-a-questions`;
    await page.goto(`/intro-python/${UNIT_ID}/rc-part1-a-questions`);
    const first = item("rc-part1-a-questions").questions?.[0];
    await page.getByTestId(`quiz-choice-${first?.id}-${first?.choices?.indexOf(String(first.answer)) ?? 0}`).click();
    await page.getByTestId("quiz-check").click();
    await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-seen-before", "true");
    await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", "true");
    await expect(page.getByTestId("quiz-seen-before")).toHaveText("You met this question before, so its answer stays hidden this time.");
    await expect(page.getByTestId("quiz-feedback").locator(".quiz-explain")).toHaveCount(0);
    await expect(page.getByTestId("quiz-feedback")).not.toContainText("It prints:");
    expect(((await saved(page)).quizzes?.[quizA] as { right?: string[] }).right ?? []).not.toContain(first?.id);

    // The missed task: Continue goes to Mar'tu's notes, not the mini-boss.
    await open(page, "rc-part1-a", tasks("rc-part1-a")[8].id);
    await expect(page.getByTestId("readiness-finish")).toContainText("You tried all of Part 1. Some of it is not ✓ yet.");
    await expect(page.getByTestId("item-continue")).toHaveAttribute("href", /\/readiness-check\/rc-review\/?$/);
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-row-rc-review")).toContainText("Next up");
    await expect(page.getByTestId("item-locked-rc-part1-b")).toBeVisible();
    // Before the notes, the result names the twin without a link to the locked form.
    await expect(page.getByTestId("readiness-twin-13")).toHaveCount(0);
    await expect(page.getByTestId("readiness-twin-locked-13")).toContainText("try its twin in Form B");
    // Opening the notes opens the other forms. The notes point to this page's own list.
    await page.getByTestId("item-link-rc-review").click();
    await expect(page.getByTestId("article-read")).toBeVisible();
    await expect(page.getByTestId("article-body")).toContainText("the unit page shows Your Readiness Check");
    await expect(page.getByTestId("article-body")).not.toContainText("tracer");
    await page.goto(`/intro-python/${UNIT_ID}`);
    for (const id of ["rc-part1-b", "rc-part1-b-questions", "rc-part1-c", "rc-part1-c-questions"]) await expect(page.getByTestId(`item-link-${id}`)).toBeVisible();
    await expect(page.getByTestId("item-row-rc-miniboss-a")).toContainText("Next up");
    // The result lists the missed skill with its lesson and its twin in Form B.
    await expect(page.getByTestId("readiness-score")).toHaveText("Part 1: you passed 9 of the 13 skills.");
    await expect(page.getByTestId("readiness-missed-13")).toContainText("Write a function from its goal");
    await expect(page.getByTestId("readiness-start-13")).toHaveText("Unit 3 · Recipes With Names · Use the ingredients");
    await expect(page.getByTestId("readiness-twin-13")).toHaveAttribute("href", /\/readiness-check\/rc-part1-b\/?#shield-cost$/);

    // Form B's questions: the twins of the three missed questions, answered and checked, then the student leaves
    // before "See my score". Each right answer counts at once.
    await page.getByTestId("item-link-rc-part1-b-questions").click();
    const quizB = item("rc-part1-b-questions").questions ?? [];
    for (const [at, question] of quizB.slice(0, 3).entries()) {
      await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of ${quizB.length}`);
      if (question.type === "mc") await page.getByTestId(`quiz-choice-${question.id}-${question.answer}`).click();
      else if (question.choices?.length) await page.getByTestId(`quiz-choice-${question.id}-${question.choices.indexOf(String(question.answer))}`).click();
      else await page.getByTestId("quiz-answer-input").fill(String(question.answer));
      await page.getByTestId("quiz-check").click();
      await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", "true");
      await page.getByTestId("quiz-next").click();
    }
    await expect
      .poll(async () => (await saved(page)).quizzes?.[`${UNIT_ID}/rc-part1-b-questions`])
      .toMatchObject({ attempts: 0, right: quizB.slice(0, 3).map((question) => question.id) });
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("readiness-score")).toHaveText("Part 1: you passed 12 of the 13 skills.");

    // The twin passed in form B: the item counts, and form A's row is done.
    await page.getByTestId("readiness-twin-13").click();
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 9 of 9");
    await pythonReady(page);
    await expect(page.getByTestId("testout-rule")).toHaveText("Each task you pass here counts for the matching task in Form A. Tasks you pass stay ✓ done.");
    await setCode(page, codeText(tasks("rc-part1-b")[8].solution));
    await runAndWait(page, 1);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-status-rc-part1-a")).toHaveAttribute("data-status", "done");
    await expect(page.getByTestId("readiness-score")).toHaveText("Part 1: you passed all 13 skills.");
    await expect(page.getByTestId("readiness-missed")).toHaveCount(0);
    // Now the forms are open, a finished questions quiz offers the next form's questions.
    await answerQuiz(page, "rc-part1-a-questions");
    await expect(page.getByTestId("quiz-retake-next-form")).toHaveText("Try new questions: Form B");
  });

  test("a task skipped without a Run is named: Form A opens on it, and one Run of the student's own try opens forms B and C", async ({ page }) => {
    test.setTimeout(180_000);
    const skipped = tasks("rc-part1-a")[8];
    // 8 of 12 questions right; tasks 1-6 and 8 passed, task 7 run and missed, task 9 opened and skipped (no Run).
    await startWith(page, {
      read: { [`${UNIT_ID}/before-we-continue`]: true, [`${UNIT_ID}/rc-review`]: true },
      exercises: {
        ...formTasks("rc-part1-a", [6]),
        [`${UNIT_ID}/rc-part1-a/${skipped.id}`]: { passed: [], done: false, hintsUsed: {}, failedRuns: 0, firstSeenAt: 1 },
      },
      quizzes: quizRight("rc-part1-a-questions", [0, 1, 2, 3, 4, 5, 6, 7]),
    });
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-locked-rc-part1-b")).toBeVisible();
    await expect(page.getByTestId("readiness-lock-why")).toContainText(
      "Not tried yet: Task 9, Write a function from its goal. Type your best try, even if it is not finished, and press Run once.",
    );
    await expect(page.getByTestId("readiness-untried")).toContainText("Not tried yet in Part 1 A: Task 9, Write a function from its goal.");
    // Next up sends the student to Form A, which opens on the task not tried yet.
    await page.getByTestId("item-link-rc-part1-a").click();
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 9 of 9");
    await pythonReady(page);
    await expect(page.getByTestId("readiness-finish")).toContainText("Not tried yet: Task 9, Write a function from its goal.");
    // One Run of the student's own unfinished try: Part 1 counts as tried, and forms B and C open.
    await setCode(page, wrongAnswer("rc-part1-a/glug-cost", "price * sips (spec: PNM), with the call"));
    await runAndWait(page, 1);
    await expect(page.getByTestId("readiness-finish")).toContainText("You tried all of Part 1.");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("item-link-rc-part1-b")).toBeVisible();
    await expect(page.getByTestId("readiness-lock-why")).toHaveCount(0);
  });

  test("the mini-boss in campaign mode: Last hint, Compare after 5 minutes only, and a pass after Compare names Mini-boss B", async ({ page }) => {
    test.setTimeout(180_000);
    const boss = `${UNIT_ID}/rc-miniboss-a`;
    const part1 = { exercises: formTasks("rc-part1-a"), quizzes: quizRight("rc-part1-a-questions", all12) };
    // Nine counted misses, every rung of step 1 open: Compare still waits (no count of runs opens it here).
    await startWith(page, {
      ...part1,
      exercises: { ...part1.exercises, [boss]: { passed: [], done: false, hintsUsed: { "skilled-hero-casts": 4 }, failedRuns: 9, activeMs: 60_000 } },
    });
    await open(page, "rc-miniboss-a");
    await runAndWait(page, 1);
    await expect(page.getByTestId("help-rung-1")).toContainText("Where to look");
    await expect(page.getByTestId("help-rung-2")).toContainText("Another way");
    await expect(page.getByTestId("help-rung-3")).toContainText("Teach me");
    await expect(page.getByTestId("help-rung-4")).toContainText("Last hint");
    await expect(page.getByTestId("help")).not.toContainText("Show me how");
    await expect(page.getByTestId("help-button")).toContainText("Compare with Mar'tu's version (opens soon)");
    // The note under it tells the campaign-mode rule: time only, never "each change you run counts".
    await expect(page.getByTestId("help-show-locked")).toHaveText(
      "Mar'tu's version opens after 5 minutes on this page. Pressing Run more does not open it sooner.",
    );
    // Five minutes on the exercise open it.
    await startWith(page, {
      ...part1,
      exercises: { ...part1.exercises, [boss]: { passed: [], done: false, hintsUsed: { "skilled-hero-casts": 4 }, failedRuns: 1, activeMs: 5 * 60_000 } },
    });
    await open(page, "rc-miniboss-a");
    await runAndWait(page, 1);
    await expect(page.getByTestId("help-button")).toContainText("Compare with Mar'tu's version");
    await expect(page.getByTestId("help-button")).not.toContainText("opens soon");
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("compare")).toBeVisible();
    await expect.poll(async () => ((await saved(page)).exercises?.[boss] as { solutionShown?: boolean })?.solutionShown).toBe(true);

    // A pass after Compare: "with Mar'tu's version", Mini-boss B next, and the result keeps a review list.
    await page.reload();
    await pythonReady(page);
    await setCode(page, codeText(item("rc-miniboss-a").solution));
    await runAndWait(page, 1);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("campaign-result")).toHaveAttribute("data-with-compare", "true");
    await expect(page.getByTestId("campaign-result")).toContainText("You finished it with Mar'tu's version. That counts, with a review list. Next: Mini-boss B: Hold the Glow Ward, on your own.");
    await expect(page.getByTestId("campaign-next-boss")).toHaveAttribute("href", /\/readiness-check\/rc-miniboss-b\/?$/);
    await expect.poll(async () => ((await saved(page)).exercises?.[boss] as { doneWithCompare?: boolean })?.doneWithCompare).toBe(true);
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("readiness-result")).toHaveAttribute("data-verdict", "review-list");
    await expect(page.getByTestId("readiness-mini-boss")).toHaveText("Mini-boss: done with Mar'tu's version.");
    await expect(page.getByTestId("readiness-next-boss")).toContainText("Next: Mini-boss B: Hold the Glow Ward, on your own.");
  });

  test("Mar'tu's version of mini-boss A, then mini-boss B passed: with Mar'tu's version, never Ready", async ({ page }) => {
    test.setTimeout(120_000);
    const part1 = { exercises: formTasks("rc-part1-a"), quizzes: quizRight("rc-part1-a-questions", all12) };
    // Compare opened on A, A left unfinished: B's answer is A's with other names.
    await startWith(page, {
      ...part1,
      exercises: {
        ...part1.exercises,
        [`${UNIT_ID}/rc-miniboss-a`]: { passed: [], done: false, hintsUsed: {}, failedRuns: 1, activeMs: 5 * 60_000, solutionShown: true },
      },
    });
    await open(page, "rc-miniboss-b");
    await setCode(page, codeText(item("rc-miniboss-b").solution));
    await runAndWait(page, 1);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("campaign-result")).toHaveAttribute("data-with-compare", "true");
    await expect(page.getByTestId("campaign-result")).toHaveText("✓ You finished it with Mar'tu's version. That counts, with a review list.");
    await expect(page.getByTestId("campaign-next-boss")).toHaveCount(0);
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("readiness-result")).toHaveAttribute("data-verdict", "review-list");
    await expect(page.getByTestId("readiness-mini-boss")).toHaveText("Mini-boss: done with Mar'tu's version.");
  });

  test("the explainer names the unit's own slips, lean: text read like a sheet, a name from the campaign, a key with no quotes, a name in quotes", async ({ page }) => {
    test.setTimeout(180_000);
    await startWith(page);
    const explainer = page.getByTestId("explainer");
    const hint = page.getByTestId("explainer-hint");
    const last = page.getByTestId("python-last-line");

    await open(page, "rc-miniboss-a");
    await setCode(page, wrongAnswer("rc-miniboss-a", "the ward's name read as if it were the page"));
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "text-as-sheet");
    await expect(explainer).toHaveAttribute("data-explainer", "lean");
    await expect(explainer.locator(".ex-explainer-title")).toHaveText("Text read like a sheet");
    await expect(hint).toHaveText("Line 37 reads ward_name like a sheet: ward_name holds text, not a sheet. Python's last line, below, says what it found. Fix it yourself, then press Run again.");
    // The campaign's `caster`: this function's own names are the evidence, and Python's 'aiter' guess is left off.
    await setCode(page, wrongAnswer("rc-miniboss-a", "the campaign's name caster copied"));
    await runAndWait(page, 2);
    await expect(explainer).toHaveAttribute("data-kind", "borrowed-name");
    await expect(explainer.locator(".ex-explainer-title")).toHaveText("Name from the campaign, not this program");
    await expect(hint).toContainText("Line 32 uses caster, a name from the campaign, not from this program. cast_ward has hero, ward_name and ward.");
    await expect(last).toHaveText("Python's last line: NameError: name 'caster' is not defined.");
    await expect(page.getByTestId("traceback")).toContainText("Did you mean: 'aiter'?");

    await open(page, "rc-part1-a", "read-the-sheet");
    await setCode(page, wrongAnswer("rc-part1-a/read-the-sheet", "(a) the key unquoted (a variable, not text)"));
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "unquoted-key");
    await expect(hint).toContainText("The mistake is on line 15: a key with no quotes.");

    await page.goto(`/intro-python/${UNIT_ID}/rc-part1-a#roll-the-die`);
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 6 of 9");
    await pythonReady(page);
    await setCode(page, wrongAnswer("rc-part1-a/roll-the-die", "the parameter's name in quotes"));
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "quoted-name");
    await expect(explainer.locator(".ex-explainer-title")).toHaveText("Parameter's name in quotes");
    await expect(hint).toContainText('Line 7 hands random.randint the text "die_size": with quotes, it is text, not the parameter die_size.');
    await expect(hint).not.toContainText("random.py");
    await expect(hint).not.toContainText("Take the quotes off");

    // The same slip in Unit 3's lesson (full, and before Unit 10's rows): Unit 3's older words, with the fix.
    await page.goto("/intro-python/first-recipes/recipes-with-names#roll-recipe");
    await expect(page.getByTestId("exercise-player")).toBeVisible();
    await pythonReady(page);
    const skip = page.getByTestId("exercise-player").getByTestId("predict-skip");
    if ((await skip.count()) > 0) await skip.first().click();
    await setCode(page, 'import random\n\ndef roll_die(die_size):\n    return random.randint(1, "die_size")\n\nprint(roll_die(20))\n');
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-explainer", "full");
    await expect(explainer).not.toHaveAttribute("data-kind", "quoted-name");
  });
});
