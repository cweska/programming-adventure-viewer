/**
 * Every PUBLISHED Intro to Python unit, in a real browser. The units are read from
 * content/courses/intro-python/units/*.json, so a unit is covered here the moment its `published` flag is on.
 *
 * The browser-parity tests put Mar'tu's solution in the editor for EVERY exercise and press Run: every step
 * must pass, exactly as docs/intro-to-python/prototypes/harness.py proved with python3. The starter must not pass
 * (unless the exercise is "run this and read it"). This is the proof that Pyodide, course_helpers.py, the grading
 * and the player agree with the harness. Every quiz is answered with its keyed answers (100%), and each unit's
 * Quick Check is passed to test out of the unit. A readiness unit (one that holds a required test-out: Unit 10's
 * Readiness Check, src/lib/course/readiness.ts) has no Quick Check: its required form is a core row, passing it tests
 * nothing out, and its other forms are locked or hidden rows. Its own behaviour is in intro-python-unit10.spec.ts.
 *
 * The tests are independent pages: playwright.config.ts runs this file in its own project, several at a time.
 */
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { plainText } from "../src/components/course/prose-format";
import { questionsNeeded } from "../src/components/course/quiz-grading";
import type { ProgressItem } from "../src/lib/course/progress";
import { readinessPlan } from "../src/lib/course/readiness";
import { buildParsons, checkpoint, PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");

type Code = string | string[];
type RawExercise = {
  id: string;
  title: string;
  starter: Code;
  solution: Code;
  starterPasses?: boolean;
  stdin?: string[];
  checkpoints: { id?: string }[];
};
type RawQuestion = {
  id?: string;
  type: "mc" | "predict" | "fill" | "parsons" | "bug";
  answer?: number | string;
  choices?: string[];
  fix?: Code;
  lines?: string[];
  expectedOutput?: string;
};
type RawItem = RawExercise & {
  kind: string;
  id: string;
  title: string;
  optional?: boolean;
  exercises?: RawExercise[];
  questions?: RawQuestion[];
  /** A Quick Check form that needs this many of its questions (the quiz `<id>-questions`) right too. */
  questionsToPass?: number;
};
type RawUnit = { id: string; order: number; title: string; published: boolean; items: RawItem[] };

const allUnits = readdirSync(UNITS_DIR)
  .filter((name) => name.endsWith(".json") && !name.endsWith(".verify.json"))
  .map((name) => JSON.parse(readFileSync(path.join(UNITS_DIR, name), "utf8")) as RawUnit)
  .sort((a, b) => a.order - b.order);
const units = allUnits.filter((unit) => unit.published);

/** A code field as the site reads it (schema.ts codeSchema): an array of lines is joined and ends in "\n". */
const codeText = (value: Code | undefined) => (Array.isArray(value) ? `${value.join("\n")}\n` : (value ?? ""));

/** `optional` as schema.ts fills it in: challenges, cheatsheets and Quick Checks default to optional. */
const isOptional = (item: RawItem) => item.optional ?? ["challenge", "cheatsheet", "testout"].includes(item.kind);

/** The unit's readiness plan (a required test-out), or null for a Quick Check unit. */
const planOf = (unit: RawUnit) =>
  readinessPlan(unit.items.map((item) => ({ ...item, kind: item.kind as ProgressItem["kind"], optional: isOptional(item) })));

/** Every played item (lesson, project, challenge, Quick Check, article try-it) with its exercises. */
function playablesOf(unit: RawUnit) {
  return unit.items.flatMap((item) => {
    if (item.kind === "project" || item.kind === "challenge") return [{ item, exercises: [item], single: true }];
    if (["lesson", "testout", "article"].includes(item.kind) && (item.exercises?.length ?? 0) > 0) {
      return [{ item, exercises: item.exercises ?? [], single: false }];
    }
    return [];
  });
}

/** The lines CodeMirror shows for `code`: one per "\n"-separated piece, so a final "\n" shows an empty last line. */
const editorLines = (code: string) => code.split("\n");

/** The editor holds exactly `code` (no auto-closed brackets or auto-indent crept in). */
async function setCode(page: Page, code: string) {
  await replaceEditor(page, code);
  const expected = editorLines(code);
  await expect
    .poll(() => page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line').allTextContents())
    .toEqual(expected);
}

/** Press Run and wait for this run's result (Run stays enabled while it runs, so count the runs). */
async function runAndWait(page: Page, runNumber: number) {
  await page.getByTestId("run").click();
  await expect(page.getByTestId("run-count")).toHaveText(new RegExp(`Run ${runNumber} finished`), { timeout: 60_000 });
}

/** The visible step messages and crash text, so a parity failure says why. */
async function whyNot(page: Page): Promise<string> {
  const parts = await page
    .locator('[data-testid="checkpoint-message"], [data-testid="explainer"], [data-testid="run-failure"], [data-testid="stdout"]')
    .allInnerTexts();
  return parts.join(" | ").slice(0, 600);
}

async function playExercise(page: Page, exercise: RawExercise, where: string, single: boolean) {
  const player = page.getByTestId("exercise-player");
  // A project or challenge is its own page: its title is the page heading, not the exercise's.
  if (single) await expect(page.getByRole("heading", { level: 1 })).toHaveText(exercise.title);
  // A title's `code` shows as code (no backticks): "`sorted` or `.sort`".
  else await expect(player.getByTestId("exercise-title")).toHaveText(plainText(exercise.title));
  await pythonReady(page);
  if (exercise.stdin) {
    const box = page.getByTestId("stdin-box");
    await box.fill(exercise.stdin.join("\n"));
    await expect(page.getByTestId("stdin-note")).toHaveCount(0);
  }
  const steps = exercise.checkpoints.length;
  let runs = 0;

  // The starter first, on a fresh exercise (passed steps are remembered between runs).
  await setCode(page, codeText(exercise.starter));
  await runAndWait(page, ++runs);
  if (exercise.starterPasses) {
    await expect(page.getByTestId("all-passed"), `${where}: the starter should pass. ${await whyNot(page)}`).toBeVisible();
  } else {
    await expect(page.getByTestId("all-passed"), `${where}: the starter should NOT pass every step`).toHaveCount(0);
    const states = await Promise.all(Array.from({ length: steps }, (_, at) => checkpoint(page, at + 1).getAttribute("data-state")));
    expect(states.some((state) => state !== "passed"), `${where}: the starter left every step ${states.join(",")}`).toBe(true);
  }

  // Then Mar'tu's solution: every step passes.
  await setCode(page, codeText(exercise.solution));
  await runAndWait(page, ++runs);
  await expect(page.getByTestId("all-passed"), `${where}: the solution should pass. ${await whyNot(page)}`).toBeVisible();
  for (let n = 1; n <= steps; n += 1) {
    await expect(checkpoint(page, n), `${where}: step ${n}`).toHaveAttribute("data-state", "passed");
  }
  await expect(player).toHaveAttribute("data-done", "true");
}

/** Answer every question with its keyed answer and expect 100%. */
async function answerQuiz(page: Page, unit: RawUnit, quiz: RawItem) {
  await page.goto(`/intro-python/${unit.id}/${quiz.id}`);
  const questions = quiz.questions ?? [];
  const feedback = page.getByTestId("quiz-feedback");
  for (const [at, question] of questions.entries()) {
    const id = question.id ?? `q-${at + 1}`;
    const where = `${unit.id}/${quiz.id}/${id}`;
    await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of ${questions.length}`);
    await expect(page.getByTestId(`quiz-question-${id}`)).toHaveAttribute("data-type", question.type);
    switch (question.type) {
      case "mc":
        await page.getByTestId(`quiz-choice-${id}-${question.answer as number}`).click();
        break;
      case "predict":
        if (question.choices?.length) {
          const choice = question.choices.indexOf(String(question.answer));
          expect(choice, `${where}: the answer is one of the choices`).toBeGreaterThanOrEqual(0);
          await page.getByTestId(`quiz-choice-${id}-${choice}`).click();
        } else {
          await page.getByTestId("quiz-answer-input").fill(String(question.answer));
        }
        break;
      case "fill":
        await page.getByTestId("quiz-fill-input").fill(String(question.answer));
        break;
      case "parsons":
        await buildParsons(page.getByTestId(`quiz-${id}-0`), question.lines ?? []);
        break;
      case "bug": {
        await expect(page.getByTestId("quiz-bug-run")).toBeEnabled({ timeout: 120_000 });
        const fix = codeText(question.fix);
        await replaceEditor(page, fix);
        await expect.poll(() => page.locator('[data-testid="editor"] .cm-line').allTextContents()).toEqual(editorLines(fix));
        await page.getByTestId("quiz-bug-run").click();
        const firstLine = (question.expectedOutput ?? "").split("\n")[0];
        await expect(page.getByTestId("quiz-bug-output")).toContainText(firstLine, { timeout: 120_000 });
        break;
      }
    }
    await page.getByTestId("quiz-check").click();
    await expect(feedback, `${where}: the keyed answer is marked right`).toHaveAttribute("data-correct", "true", { timeout: 60_000 });
    await page.getByTestId("quiz-next").click();
  }
  await expect(page.getByTestId("quiz-results")).toBeVisible();
  await expect(page.getByTestId("quiz-score")).toHaveText(`${questions.length} of ${questions.length} right (100%)`);
  await expect
    .poll(() =>
      page.evaluate(
        ([key, quizKey]) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.quizzes?.[quizKey]?.best ?? null,
        [PROGRESS_KEY, `${unit.id}/${quiz.id}`] as const,
      ),
    )
    .toBe(100);
}

test("the course map lists every published unit, in order, and no unpublished one", async ({ page }) => {
  expect(units.length, "at least one unit is published").toBeGreaterThan(0);
  await page.goto("/intro-python");
  await expect(page.getByTestId("course-map")).toBeVisible();
  await expect(page.getByTestId("preview-banner")).toHaveCount(0);
  const cards = page.locator('[data-testid^="unit-card-"]');
  await expect(cards).toHaveCount(units.length);
  expect(await cards.evaluateAll((els) => els.map((el) => el.getAttribute("data-testid")))).toEqual(
    units.map((unit) => `unit-card-${unit.id}`),
  );
  for (const hidden of allUnits.filter((unit) => !unit.published)) {
    await expect(page.getByTestId(`unit-card-${hidden.id}`)).toHaveCount(0);
  }
});

for (const unit of units) {
  const itemPath = (itemId: string) => `/intro-python/${unit.id}/${itemId}`;

  test.describe(`Intro to Python, Unit ${unit.order}: ${unit.title}`, () => {
    const readiness = planOf(unit);
    const listTitle = readiness
      ? "the map shows it without ?preview=1, and its page lists its items, its forms among them, with no Quick Check offer"
      : "the map shows it without ?preview=1, and its page lists its items and offers its Quick Check";
    test(listTitle, async ({ page }) => {
      await page.goto("/intro-python");
      await expect(page.getByTestId(`unit-card-${unit.id}`)).toBeVisible();
      await expect(page.getByTestId(`unit-card-${unit.id}`)).toContainText(unit.title);
      await expect(page.getByTestId(`unit-status-${unit.id}`)).toContainText("Not started");

      await page.getByTestId(`unit-link-${unit.id}`).click();
      await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", unit.id);
      await expect(page.getByTestId("unpublished-banner")).toHaveCount(0);
      await expect(page.getByRole("heading", { level: 1 })).toHaveText(unit.title);

      // Every item but the Quick Check (its forms and their question quizzes) is listed, in order. A readiness unit
      // lists its forms too, in ITEMS order: the parallel forms as locked rows, the re-check not at all (not due yet).
      const testouts = unit.items.filter((item) => item.kind === "testout");
      const quickCheckIds = new Set(testouts.flatMap((form) => [form.id, `${form.id}-questions`]));
      const hidden = new Set(readiness ? readiness.rechecks.flatMap((id) => [id, `${id}-questions`]) : []);
      const locked = new Set(readiness ? readiness.forms.slice(1).flatMap((id) => [id, `${id}-questions`]) : []);
      const listed = unit.items.filter((item) => (readiness ? !hidden.has(item.id) : !quickCheckIds.has(item.id)));
      const rows = page.locator('[data-testid^="item-row-"]');
      await expect(rows).toHaveCount(listed.length);
      expect(await rows.evaluateAll((els) => els.map((el) => el.getAttribute("data-testid")))).toEqual(
        listed.map((item) => `item-row-${item.id}`),
      );
      for (const item of listed) {
        if (locked.has(item.id)) await expect(page.getByTestId(`item-locked-${item.id}`)).toBeVisible();
        else await expect(page.getByTestId(`item-link-${item.id}`)).toHaveText(item.title);
      }

      if (readiness) {
        await expect(page.getByTestId("quick-check-offer")).toHaveCount(0);
      } else if (testouts.length > 0) {
        await expect(page.getByTestId("quick-check-offer")).toBeVisible();
        await expect(page.getByTestId("testout-start")).toHaveAttribute("href", new RegExp(`/${unit.id}/${testouts[0]?.id}/?$`));
        const offered = [...quickCheckIds].filter((id) => id !== testouts[0]?.id && unit.items.some((item) => item.id === id));
        for (const id of offered) {
          await expect(page.getByTestId(`quick-check-link-${id}`)).toHaveAttribute("href", new RegExp(`/${unit.id}/${id}/?$`));
        }
      }

      // The first lesson opens in the player, and the breadcrumbs lead back to the unit.
      const lesson = unit.items.find((item) => item.kind === "lesson");
      if (lesson) {
        await page.getByTestId(`item-link-${lesson.id}`).click();
        await expect(page.getByTestId("lesson-player")).toBeVisible();
        await expect(page.getByTestId("exercise-label")).toHaveText(/^Exercise 1 of \d+$/);
        await page.getByTestId("course-breadcrumbs").getByRole("link", { name: new RegExp(unit.title) }).click();
        await expect(page.getByTestId("unit-page")).toBeVisible();
      }
    });

    test.describe("browser parity: every solution passes and every starter does not", () => {
      for (const { item, exercises, single } of playablesOf(unit)) {
        test(`${item.kind} ${item.id} (${exercises.length} exercise${exercises.length === 1 ? "" : "s"})`, async ({ page }) => {
          test.setTimeout(60_000 + exercises.length * 45_000);
          for (const [at, exercise] of exercises.entries()) {
            const where = single ? `${unit.id}/${item.id}` : `${unit.id}/${item.id}/${exercise.id}`;
            if (single || item.kind === "article") {
              if (at === 0) await page.goto(itemPath(item.id));
            } else {
              // The player reads the exercise from the URL hash, and follows it without a reload.
              await page.goto(`${itemPath(item.id)}#${exercise.id}`);
              await expect(page.getByTestId("exercise-label")).toHaveText(new RegExp(`^(Exercise|Task) ${at + 1} of ${exercises.length}$`));
            }
            await playExercise(page, exercise, where, single);
          }
        });
      }
    });

    test.describe("every quiz scores 100% with its keyed answers", () => {
      for (const quiz of unit.items.filter((item) => item.kind === "quiz")) {
        test(`quiz ${quiz.id} (${quiz.questions?.length ?? 0} questions)`, async ({ page }) => {
          await answerQuiz(page, unit, quiz);
        });
      }
    });

    const quickCheck = unit.items.find((item) => item.kind === "testout");
    if (readiness) {
      const form = unit.items.find((item) => item.id === readiness.required);
      test(`passing the required form ${readiness.required} tests nothing out: the core stays the student's to do`, async ({ page }) => {
        const tasks = form?.exercises ?? [];
        test.setTimeout(60_000 + tasks.length * 45_000);
        await page.goto(`/intro-python/${unit.id}/${readiness.required}`);
        await expect(page.getByTestId("testout-intro")).toHaveAttribute("data-readiness", "true");
        for (const [at, task] of tasks.entries()) {
          await page.goto(`/intro-python/${unit.id}/${readiness.required}#${task.id}`);
          await expect(page.getByTestId("exercise-label")).toHaveText(`Task ${at + 1} of ${tasks.length}`);
          await pythonReady(page);
          await expect(page.getByTestId("help-button")).toHaveCount(0);
          await setCode(page, codeText(task.solution));
          await runAndWait(page, 1);
          await expect(page.getByTestId("all-passed"), `${unit.id}/${readiness.required}/${task.id}: ${await whyNot(page)}`).toBeVisible();
        }
        const quiz = unit.items.find((entry) => entry.id === readiness.questions[readiness.required]);
        if (quiz) await answerQuiz(page, unit, quiz);
        await expect
          .poll(() =>
            page.evaluate(([key, unitId]) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.testedOut?.[unitId] ?? false, [
              PROGRESS_KEY,
              unit.id,
            ] as const),
          )
          .toBe(false);
        await page.goto(`/intro-python/${unit.id}`);
        await expect(page.getByTestId(`unit-status-${unit.id}`)).not.toContainText("Tested out");
        await expect(page.getByTestId(`item-status-${readiness.required}`)).toHaveAttribute("data-status", "done");
        for (const id of [readiness.miniBoss, readiness.explain].filter((entry): entry is string => Boolean(entry))) {
          await expect(page.getByTestId(`item-status-${id}`), id).toHaveAttribute("data-status", "not-started");
        }
      });
    } else if (quickCheck) {
      test(`passing Quick Check ${quickCheck.id} marks the unit as tested out`, async ({ page }) => {
        const tasks = quickCheck.exercises ?? [];
        test.setTimeout(60_000 + tasks.length * 45_000);
        await page.goto(`/intro-python/${unit.id}`);
        await page.getByTestId("testout-start").click();
        await expect(page.getByTestId("testout-intro")).toBeVisible();
        await pythonReady(page);
        await expect(page.getByTestId("testout-pending")).toBeVisible();

        for (const [at, task] of tasks.entries()) {
          await expect(page.getByTestId("exercise-label")).toHaveText(`Task ${at + 1} of ${tasks.length}`);
          await pythonReady(page);
          // No help in a Quick Check.
          await expect(page.getByTestId("help-button")).toHaveCount(0);
          await setCode(page, codeText(task.solution));
          await runAndWait(page, 1);
          await expect(page.getByTestId("all-passed"), `${unit.id}/${quickCheck.id}/${task.id}: ${await whyNot(page)}`).toBeVisible();
          if (at < tasks.length - 1) await page.getByTestId("celebrate-next").click();
        }

        if (quickCheck.questionsToPass) {
          // The tasks alone do not pass this form: its questions count too, and the page says so.
          const quiz = unit.items.find((entry) => entry.kind === "quiz" && entry.id === `${quickCheck.id}-questions`);
          expect(quiz, `${quickCheck.id}-questions exists`).toBeTruthy();
          const needed = questionsNeeded(quickCheck.questionsToPass, quiz?.questions?.length ?? 0);
          await expect(page.getByTestId("testout-questions")).toContainText(`Get ${needed} right`);
          await expect(page.getByTestId("testout-result")).toHaveCount(0);
          await page.goto(`/intro-python/${unit.id}`);
          await expect(page.getByTestId(`unit-status-${unit.id}`)).not.toContainText("Tested out");
          await expect(page.getByTestId("quick-check-more")).toContainText(`To pass, finish the tasks, then get ${needed}`);
          await answerQuiz(page, unit, quiz as RawItem);
          await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "true");
        } else {
          await expect(page.getByTestId("testout-result")).toBeVisible();
        }
        await expect
          .poll(() =>
            page.evaluate(([key, unitId]) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.testedOut?.[unitId] ?? false, [
              PROGRESS_KEY,
              unit.id,
            ] as const),
          )
          .toBe(true);

        await page.goto(`/intro-python/${unit.id}`);
        await expect(page.getByTestId("quick-check-offer")).toContainText("You passed the Quick Check");
        await expect(page.getByTestId(`unit-status-${unit.id}`)).toContainText("Tested out");
        for (const item of unit.items.filter((entry) => !isOptional(entry))) {
          await expect(page.getByTestId(`item-status-${item.id}`), item.id).toHaveAttribute("data-status", "tested-out");
        }
        await page.goto("/intro-python");
        await expect(page.getByTestId(`unit-status-${unit.id}`)).toContainText("Tested out");
      });
    }
  });
}
