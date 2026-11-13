/**
 * Unit 1 ("Hello World: Words by the Fire") in a real browser.
 *
 * The browser-parity tests read the exported unit JSON and, for EVERY exercise, put Mar'tu's solution in the
 * editor and press Run: every step must pass, exactly as docs/intro-to-python/prototypes/harness.py proved with
 * python3. The starter must not pass (unless the exercise is "run this and read it"). This is the proof that
 * Pyodide, course_helpers.py, the grading and the player agree with the harness.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { buildParsons, checkpoint, PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "hello-world";

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
};
type RawUnit = { id: string; title: string; published: boolean; items: RawItem[] };

const unit = JSON.parse(
  readFileSync(path.join(process.cwd(), "content/courses/intro-python/units", `${UNIT_ID}.json`), "utf8"),
) as RawUnit;

/** A code field as the site reads it (schema.ts codeSchema): an array of lines is joined and ends in "\n". */
const codeText = (value: Code | undefined) => (Array.isArray(value) ? `${value.join("\n")}\n` : (value ?? ""));

const itemPath = (itemId: string) => `/intro-python/${UNIT_ID}/${itemId}`;

/** `optional` as schema.ts fills it in: challenges, cheatsheets and Quick Checks default to optional. */
const isOptional = (item: RawItem) => item.optional ?? ["challenge", "cheatsheet", "testout"].includes(item.kind);

/** Every played item (lesson, project, challenge, Quick Check, article try-it) with its exercises. */
const playable = unit.items.flatMap((item) => {
  if (item.kind === "project" || item.kind === "challenge") return [{ item, exercises: [item], single: true }];
  if (["lesson", "testout", "article"].includes(item.kind) && (item.exercises?.length ?? 0) > 0) {
    return [{ item, exercises: item.exercises ?? [], single: false }];
  }
  return [];
});
const quizzes = unit.items.filter((item) => item.kind === "quiz");

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
  else await expect(player.getByTestId("exercise-title")).toHaveText(exercise.title);
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
    const states = await Promise.all(
      Array.from({ length: steps }, (_, at) => checkpoint(page, at + 1).getAttribute("data-state")),
    );
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
async function answerQuiz(page: Page, quiz: RawItem) {
  await page.goto(itemPath(quiz.id));
  const questions = quiz.questions ?? [];
  const feedback = page.getByTestId("quiz-feedback");
  for (const [at, question] of questions.entries()) {
    const id = question.id ?? `q-${at + 1}`;
    const where = `${quiz.id}/${id}`;
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
        await expect
          .poll(() => page.locator('[data-testid="editor"] .cm-line').allTextContents())
          .toEqual(editorLines(fix));
        await page.getByTestId("quiz-bug-run").click();
        const firstLine = (question.expectedOutput ?? "").split("\n")[0];
        await expect(page.getByTestId("quiz-bug-output")).toContainText(firstLine, { timeout: 120_000 });
        break;
      }
    }
    await page.getByTestId("quiz-check").click();
    await expect(feedback, `${where}: the keyed answer is marked right`).toHaveAttribute("data-correct", "true", {
      timeout: 60_000,
    });
    await page.getByTestId("quiz-next").click();
  }
  await expect(page.getByTestId("quiz-results")).toBeVisible();
  await expect(page.getByTestId("quiz-score")).toHaveText(`${questions.length} of ${questions.length} right (100%)`);
  await expect
    .poll(() =>
      page.evaluate(
        ([key, quizKey]) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.quizzes?.[quizKey]?.best ?? null,
        [PROGRESS_KEY, `${UNIT_ID}/${quiz.id}`] as const,
      ),
    )
    .toBe(100);
}

test.describe("Intro to Python, Unit 1: Hello World", () => {
  test("the course map shows Unit 1 (not the sample) without ?preview=1, and the unit page lists its items", async ({ page }) => {
    expect(unit.published, "Unit 1 is published").toBe(true);
    await page.goto("/");
    await page.getByRole("navigation", { name: "Site" }).getByRole("link", { name: "Intro to Python" }).click();
    await expect(page.getByTestId("course-map")).toBeVisible();
    await expect(page).toHaveURL(/\/intro-python\/?$/);
    await expect(page.getByTestId("preview-banner")).toHaveCount(0);
    await expect(page.getByTestId(`unit-card-${UNIT_ID}`)).toBeVisible();
    await expect(page.getByTestId(`unit-card-${UNIT_ID}`)).toContainText(unit.title);
    await expect(page.getByTestId("unit-card-sample")).toHaveCount(0);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Not started");

    await page.getByTestId(`unit-link-${UNIT_ID}`).click();
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByTestId("unpublished-banner")).toHaveCount(0);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(unit.title);

    // Every item but the Quick Check (its forms and their question quizzes) is listed, in order.
    const testouts = unit.items.filter((item) => item.kind === "testout");
    const quickCheckIds = new Set(testouts.flatMap((form) => [form.id, `${form.id}-questions`]));
    const listed = unit.items.filter((item) => !quickCheckIds.has(item.id));
    const rows = page.locator('[data-testid^="item-row-"]');
    await expect(rows).toHaveCount(listed.length);
    expect(await rows.evaluateAll((els) => els.map((el) => el.getAttribute("data-testid")))).toEqual(
      listed.map((item) => `item-row-${item.id}`),
    );
    for (const item of listed) await expect(page.getByTestId(`item-link-${item.id}`)).toHaveText(item.title);

    // The Quick Check is offered up front: Form A, its questions, and Form B with its questions for a fresh try.
    await expect(page.getByTestId("quick-check-offer")).toBeVisible();
    await expect(page.getByTestId("testout-start")).toHaveAttribute("href", new RegExp(`/${UNIT_ID}/${testouts[0]?.id}/?$`));
    const offered = [...quickCheckIds].filter((id) => id !== testouts[0]?.id && unit.items.some((item) => item.id === id));
    expect(offered.length, "Form A's questions, Form B and Form B's questions").toBe(3);
    for (const id of offered) {
      await expect(page.getByTestId(`quick-check-link-${id}`)).toHaveAttribute("href", new RegExp(`/${UNIT_ID}/${id}/?$`));
    }
    await expect(page.getByTestId("quick-check-more")).toContainText("Want different tasks? Try Form B and its questions.");

    // An item link opens the player; the breadcrumbs lead back to the unit and the map.
    await page.getByTestId("item-link-words-in-quotes").click();
    await expect(page.getByTestId("lesson-player")).toBeVisible();
    await expect(page.getByTestId("exercise-label")).toHaveText(/^Exercise 1 of \d+$/);
    const crumbs = page.getByTestId("course-breadcrumbs");
    await crumbs.getByRole("link", { name: new RegExp(unit.title) }).click();
    await expect(page.getByTestId("unit-page")).toBeVisible();
    await page.getByTestId("back-to-course").click();
    await expect(page.getByTestId("course-map")).toBeVisible();
  });

  test.describe("browser parity: every solution passes and every starter does not", () => {
    // Independent pages: with more than one worker (npx playwright test --workers 4) they run side by side.
    test.describe.configure({ mode: "parallel" });
    for (const { item, exercises, single } of playable) {
      test(`${item.kind} ${item.id} (${exercises.length} exercise${exercises.length === 1 ? "" : "s"})`, async ({ page }) => {
        test.setTimeout(60_000 + exercises.length * 45_000);
        for (const [at, exercise] of exercises.entries()) {
          const where = single ? item.id : `${item.id}/${exercise.id}`;
          if (single || item.kind === "article") {
            if (at === 0) await page.goto(itemPath(item.id));
          } else {
            // The player reads the exercise from the URL hash, and follows it without a reload.
            await page.goto(`${itemPath(item.id)}#${exercise.id}`);
            await expect(page.getByTestId("exercise-label")).toHaveText(
              new RegExp(`^(Exercise|Task) ${at + 1} of ${exercises.length}$`),
            );
          }
          await playExercise(page, exercise, where, single);
        }
      });
    }
  });

  test.describe("every quiz scores 100% with its keyed answers", () => {
    test.describe.configure({ mode: "parallel" });
    for (const quiz of quizzes) {
      test(`quiz ${quiz.id} (${quiz.questions?.length ?? 0} questions)`, async ({ page }) => {
        await answerQuiz(page, quiz);
      });
    }
  });

  test.describe("play-through fixes", () => {
    test("after a crash, Help aims at the line Python stopped on, and Python's last line is on screen", async ({ page }) => {
      await page.goto(`${itemPath("words-in-quotes")}#broken-spell-1a`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell: three slips");
      await pythonReady(page);
      await setCode(page, 'print("Shield up.")\nprint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("help-crash")).toContainText("Mend line 3 first.");
      await expect(page.getByTestId("help-crash")).not.toContainText("its last line");
      // Help is for step 3 ("Mend line 3 ..."), not step 1, whose line is already right.
      await expect(page.getByTestId("help")).toHaveAttribute("data-step", "mend-line-3");
      await expect(page.getByTestId("help-button")).toContainText("step 3");
      await expect(page.getByTestId("python-last-line")).toContainText("NameError: name 'Steady' is not defined");
      await expect(page.getByTestId("traceback")).toBeHidden();
    });

    test("a crash on a line no step names holds the steps' Help back, and names the box to make", async ({ page }) => {
      await page.goto(`${itemPath("boxes-with-labels")}#broken-spell-1b`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell");
      await pythonReady(page);
      await setCode(page, 'weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\n"Lucky"\nprint(hero)\nprint(weapon)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("help-crash")).toContainText("Mend line 5 first.");
      await expect(page.getByTestId("help")).toHaveAttribute("data-crash-only", "true");
      await expect(page.getByTestId("help-button")).toHaveCount(0);
      await expect(page.getByTestId("explainer-hint")).toContainText("hero is one of this task's boxes");
      await expect(page.getByTestId("explainer-hint")).toContainText('hero = "Lucky"');
    });

    test("a step that passed, then broke, is marked to check again, and the done panel does not celebrate", async ({ page }) => {
      await page.goto(`${itemPath("math-and-glue")}#solo-1c`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Show Mar'tu");
      await pythonReady(page);
      await setCode(page, "# Mar'tu needs 4 candles that cost 2 coins each.\ncandle_count = 4\ncandle_price = 2\ncandle_cost = candle_count * candle_price\nprint(candle_cost)\n");
      await runAndWait(page, 1);
      await expect(page.getByTestId("all-passed")).toBeVisible();
      await setCode(page, "# Mar'tu needs 4 candles that cost 2 coins each.\ncandle_count = 2\ncandle_price = 4\ncandle_cost = 8\nprint(candle_cost)\n");
      await runAndWait(page, 2);
      await expect(checkpoint(page, 1)).toHaveAttribute("data-state", "passed");
      await expect(checkpoint(page, 1)).toHaveAttribute("data-slipped", "true");
      await expect(page.getByTestId("checkpoint-slipped-1")).toContainText("check it again");
      await expect(page.getByTestId("exercise-done")).toHaveAttribute("data-slipped", "true");
      await expect(page.getByTestId("exercise-done-martu")).not.toContainText("You did that alone");
      await expect(page.getByTestId("exercise-done-martu")).toContainText("still done");
    });

    test("in a print-only warm-up, Mar'tu's pick on an empty line goes in as a print line", async ({ page }) => {
      await page.goto(`${itemPath("before-the-first-spell")}#keyboard-symbols`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Where the symbols live");
      await pythonReady(page);
      await setCode(page, "# Print a line that has _ and - and = in it.\n");
      const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
      await lines.nth(1).click();
      await page.getByTestId("pick-use").first().click();
      await expect(lines.nth(1)).toHaveText('print("_ - = are side by side.")');
      await runAndWait(page, 1);
      await expect(page.getByTestId("all-passed")).toBeVisible();
    });
  });

  test("passing the Quick Check marks Unit 1 as tested out", async ({ page }) => {
    const quickCheck = unit.items.find((item) => item.kind === "testout");
    expect(quickCheck).toBeDefined();
    const tasks = quickCheck?.exercises ?? [];
    await page.goto(`/intro-python/${UNIT_ID}`);
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
      await expect(page.getByTestId("all-passed"), `${quickCheck?.id}/${task.id}: ${await whyNot(page)}`).toBeVisible();
      if (at < tasks.length - 1) await page.getByTestId("celebrate-next").click();
    }

    await expect(page.getByTestId("testout-result")).toBeVisible();
    await expect
      .poll(() =>
        page.evaluate(([key, unitId]) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.testedOut?.[unitId] ?? false, [
          PROGRESS_KEY,
          UNIT_ID,
        ] as const),
      )
      .toBe(true);

    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("quick-check-offer")).toContainText("You passed the Quick Check");
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
    for (const item of unit.items.filter((entry) => !isOptional(entry))) {
      await expect(page.getByTestId(`item-status-${item.id}`), item.id).toHaveAttribute("data-status", "tested-out");
    }
    await page.goto("/intro-python");
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
  });
});
