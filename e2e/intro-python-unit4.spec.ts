/**
 * Unit 4 ("Lists: The Chalk Wall") in a real browser: what the teacher's ruling on the Unit 4 reviews asked of the
 * site. The explainer's list rows (round brackets where a list needs square ones, square brackets after a tool you
 * call, a comma between two positions, one item joined with `+`, `sorted` after a dot, unquoted words in a list,
 * `.remove()` of a value the list does not hold), full in a lesson and lean in the SOLO and the Quick Check; lean
 * check messages; the Quick Check's question gate (both questions); the hint ladders' Start me off; and the
 * course-wide choice shuffle (the display order changes, the authored index, the grading and the test ids do not).
 *
 * Every code below is one of the unit's own wrong answers, read from the harness sidecar, so the browser runs
 * exactly what python3 proved. Browser parity for every exercise, quiz and Quick Check is in
 * intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { choiceOrder, choiceSeed } from "../src/components/course/quiz-grading";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "lists";
const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");
const SEED_KEY = "intro-python:seed";

type Code = string | string[];
type Question = { id: string; type: string; answer: number | string; choices?: string[] };
type RawItem = {
  id: string;
  kind: string;
  questionsToPass?: number;
  exercises?: { id: string; checkpoints: { id: string }[]; predict?: { choices: string[]; answer: number } }[];
  questions?: Question[];
};

const unit = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.json`), "utf8")) as { items: RawItem[] };
const sidecar = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.verify.json`), "utf8")) as {
  exercises: Record<string, { wrongAnswers?: { why: string; code: Code }[] }>;
};

const codeText = (value: Code) => (Array.isArray(value) ? `${value.join("\n")}\n` : value);

/** The unit's own wrong answer for `key` ("<item>/<exercise>") whose `why` contains `why`. */
function wrongAnswer(key: string, why: string): string {
  const found = (sidecar.exercises[key]?.wrongAnswers ?? []).filter((entry) => entry.why.includes(why));
  expect(found, `${key}: one wrong answer about "${why}"`).toHaveLength(1);
  return codeText(found[0].code);
}

/** The editor holds exactly `code` (no auto-closed brackets or auto-indent crept in). */
async function setCode(page: Page, code: string) {
  await replaceEditor(page, code);
  await expect
    .poll(() => page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line').allTextContents())
    .toEqual(code.split("\n"));
}

/** Press Run and wait for this run's result (Run stays enabled while it runs, so count the runs). */
async function runAndWait(page: Page, runNumber: number) {
  await page.getByTestId("run").click();
  await expect(page.getByTestId("run-count")).toHaveText(new RegExp(`Run ${runNumber} finished`), { timeout: 60_000 });
}

async function open(page: Page, itemId: string, exerciseId?: string) {
  await page.goto(`/intro-python/${UNIT_ID}/${itemId}${exerciseId ? `#${exerciseId}` : ""}`);
  await expect(page.getByTestId("exercise-player")).toBeVisible();
  await pythonReady(page);
}

/** Run one of the unit's wrong answers and return the explainer. */
async function runWrong(page: Page, key: string, why: string, run: number) {
  await setCode(page, wrongAnswer(key, why));
  await runAndWait(page, run);
  return page.getByTestId("explainer");
}

/** The authored indices of the choices `prefix` matches, in the order the page shows them. */
async function shownOrder(page: Page, prefix: string): Promise<number[]> {
  const ids = await page.locator(`[data-testid^="${prefix}"]`).evaluateAll((els) => els.map((el) => el.getAttribute("data-testid") ?? ""));
  return ids.map((id) => Number(id.slice(prefix.length)));
}

/** A student seed whose order for `where` differs between attempt 0 and 1, with the right answer not shown first. */
function seedFor(count: number, where: string, answer: number): string {
  for (let at = 0; at < 500; at += 1) {
    const seed = `pell${at}`;
    const first = choiceOrder(count, choiceSeed(seed, where, 0));
    const again = choiceOrder(count, choiceSeed(seed, where, 1));
    if (first[0] !== answer && first.join() !== again.join()) return seed;
  }
  throw new Error("no seed");
}

test.describe("Intro to Python, Unit 4: Lists", () => {
  test("the unit page offers the Quick Check, which needs its three tasks and both questions", async ({ page }) => {
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Lists");
    await expect(page.getByTestId("item-row-one-list-same-answer")).toContainText("Optional");
    await expect(page.getByTestId("item-row-many-values-one-name")).not.toContainText("Optional");
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get both Quick Check questions right.");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 3 tasks and get both questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 3");
  });

  test("a lesson gets the full list rows: square brackets for a list, round ones for a call, + joins two lists", async ({ page }) => {
    await open(page, "many-values-one-name", "fix-a-mark");
    const assigned = await runWrong(page, "many-values-one-name/fix-a-mark", "round brackets: assigning to a call", 1);
    await expect(assigned).toHaveAttribute("data-explainer", "full");
    await expect(assigned).toHaveAttribute("data-kind", "list-needs-square-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText("Line 5 puts ( ) after chalk_wall. To change one item, use square brackets: chalk_wall[2] = 47");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("==");
    await expect(page.getByTestId("python-last-line")).toContainText("cannot assign to function call");

    await open(page, "many-values-one-name", "new-chalk-mark");
    const plus = await runWrong(page, "many-values-one-name/new-chalk-mark", "a number joined with +", 1);
    await expect(plus).toHaveAttribute("data-kind", "list-plus-item");
    await expect(page.getByTestId("explainer-hint")).toContainText("+ joins two lists. To add one item, use .append(): chalk_wall.append(33)");
    const square = await runWrong(page, "many-values-one-name/new-chalk-mark", "square brackets for append's round ones", 2);
    await expect(square).toHaveAttribute("data-kind", "call-needs-round-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText("Call it with round brackets: chalk_wall.append(33)");
    await expect(page.getByTestId("python-last-line")).toContainText("is not subscriptable");

    await open(page, "many-values-one-name", "lists-inside-lists");
    const comma = await runWrong(page, "many-values-one-name/lists-inside-lists", "a comma between the positions", 1);
    await expect(comma).toHaveAttribute("data-kind", "comma-in-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText("Row then item takes two pairs of brackets: roster[2][0].");
  });

  test("sorted after a dot, .remove() of a missing value and unquoted words in a list get the unit's words", async ({ page }) => {
    await open(page, "reading-the-wall-closely", "sorted-or-sort");
    const dot = await runWrong(page, "reading-the-wall-closely/sorted-or-sort", "sorted used as a list method", 1);
    await expect(dot).toHaveAttribute("data-kind", "tool-after-dot");
    await expect(page.getByTestId("explainer-hint")).toContainText("sorted goes in front: sorted(chalk_wall). It hands back a sorted copy.");
    await expect(page.getByTestId("python-last-line")).toContainText("Did you mean: 'sort'?");

    await open(page, "more-list-tools", "remove-and-in");
    const missing = await runWrong(page, "more-list-tools/remove-and-in", "remove by position (3), not value", 1);
    await expect(missing).toHaveAttribute("data-kind", "not-on-the-list");
    await expect(page.getByTestId("explainer-hint")).toContainText("looks for a value, not a position. There is no 3 on the list. Ask first with in.");

    await open(page, "oogrishs-training-log");
    const words = await runWrong(page, "oogrishs-training-log", "a drill with no quotes, on one line", 1);
    await expect(words).toHaveAttribute("data-kind", "unquoted-words");
    await expect(page.getByTestId("explainer-hint")).toContainText('If storm kick is text, put quotes around it: "storm kick".');
    await expect(page.getByTestId("python-last-line")).toContainText("Perhaps you forgot a comma?");
  });

  test("lean in the SOLO and the Quick Check: the kind of slip and its line, never the fix", async ({ page }) => {
    await open(page, "many-values-one-name", "solo-3a");
    const solo = await runWrong(page, "many-values-one-name/solo-3a", "round brackets: the list called like a recipe", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "list-needs-square-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 3: round brackets where a list needs square ones.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("wall[-1]");
    await expect(page.getByTestId("python-last-line")).toContainText("'list' object is not callable");

    // The SOLO's check messages are lean too: the slip and the evidence, never the tool to write.
    await open(page, "more-list-tools", "solo-3c");
    await setCode(page, wrongAnswer("more-list-tools/solo-3c", "the first gap read instead"));
    await runAndWait(page, 1);
    const soloMessage = page.getByTestId("checkpoint-message");
    await expect(soloMessage).toContainText("Your line reads the first gap, and the longest gap is not always the first.");
    await expect(soloMessage).toContainText("(Mar'tu's check tried");
    await expect(soloMessage).not.toContainText("max(");

    await open(page, "qc3-a", "make-append-read");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const plus = await runWrong(page, "qc3-a/make-append-read", "+ a number, not a list", 1);
    await expect(plus).toHaveAttribute("data-explainer", "lean");
    await expect(plus).toHaveAttribute("data-kind", "list-plus-item");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 4: one item joined to a list with +.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("marks.append(33)");
    // A check message in the Quick Check names the slip and the evidence, never the line to type.
    await setCode(page, wrongAnswer("qc3-a/make-append-read", "the fix appended"));
    await runAndWait(page, 2);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText(".append() adds 43 at the end, so the 44 is still there.");
    await expect(message).not.toContainText("marks[1]");
  });

  test("the same slip is full in a lesson and lean in the Quick Check (square brackets after append)", async ({ page }) => {
    await open(page, "many-values-one-name", "new-chalk-mark");
    await runWrong(page, "many-values-one-name/new-chalk-mark", "square brackets for append's round ones", 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "full");
    await expect(page.getByTestId("explainer-hint")).toContainText("chalk_wall.append(33)");

    await open(page, "qc3-b", "make-append-read");
    await runWrong(page, "qc3-b/make-append-read", "square brackets for append's round ones", 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "lean");
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "call-needs-round-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 6: square brackets where a call needs round ones.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("ore_used.append(9)");
  });

  test("the hint ladder ends on the step's own line: Start me off goes under its note, and a worked-out position has none", async ({ page }) => {
    await open(page, "many-values-one-name", "first-is-zero");
    await page.getByTestId("predict-skip").click();
    await runAndWait(page, 1);
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-rung-1")).toHaveAttribute("data-kind", "start");
    // The start runs on to the list's bracket: `print(` alone would match every print line.
    await expect(page.getByTestId("help-start-code")).toHaveText("print(chalk_wall[");
    await page.getByTestId("help-start-insert").click();
    const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
    await expect(lines.nth(1)).toHaveText("# 1. Print the oldest gap.");
    await expect(lines.nth(2)).toHaveText("print(chalk_wall[");

    // Fix a mark: the position is what the step asks for, so Help starts at Where to look, with no Start me off.
    await open(page, "many-values-one-name", "fix-a-mark");
    await runAndWait(page, 1);
    await expect(page.getByTestId("help-button")).toContainText("Where to look");
    await expect(page.getByTestId("help-button")).not.toContainText("Start me off");
  });

  test("a tool's glossary word and a title's code show as code, and a SOLO's Learn pane has no free Another way", async ({ page }) => {
    // [[len()|`len(wall)`]]: a code chip that opens the glossary, never raw [[ | ]] marks.
    await open(page, "many-values-one-name", "how-long");
    const learn = page.getByTestId("learn-pane");
    await expect(learn).not.toContainText("[[");
    await expect(learn).not.toContainText("]]");
    const term = learn.getByTestId("glossary-term").filter({ hasText: "len(wall)" }).first();
    await expect(term.locator("code")).toHaveText("len(wall)");
    await term.click();
    await expect(page.getByTestId("glossary-popover")).toBeVisible();

    await open(page, "reading-the-wall-closely", "sorted-or-sort");
    await expect(page.getByTestId("exercise-title")).toHaveText("sorted or .sort");
    await expect(page.getByTestId("exercise-title").locator("code")).toHaveCount(2);

    // The SOLO's angles are a Help rung only, which counts as Help: no "Explain it another way" for free.
    await open(page, "reading-the-wall-closely", "solo-3b");
    await expect(page.getByTestId("exercise-title")).toHaveText("Show Mar'tu");
    await expect(page.getByTestId("another-way-box")).toHaveCount(0);
  });

  test("choices show in a shuffled order that holds within an attempt; grading and test ids keep the authored index", async ({ page }) => {
    // A quiz: the order follows the student seed, the question and the attempt.
    const quiz = unit.items.find((item) => item.id === "3a-remembers");
    const first = quiz?.questions?.[0] as Question;
    const right = (first.choices ?? []).indexOf(String(first.answer));
    const where = `${UNIT_ID}/3a-remembers/${first.id}`;
    const seed = seedFor(first.choices?.length ?? 0, where, right);
    await page.goto("/intro-python");
    await page.evaluate(([key, value]) => window.localStorage.setItem(key, value), [SEED_KEY, seed] as const);

    await page.goto(`/intro-python/${UNIT_ID}/3a-remembers`);
    const prefix = `quiz-choice-${first.id}-`;
    await expect(page.locator('[data-testid="quiz"] .quiz-choices')).toHaveAttribute("data-ready", "true");
    const attempt0 = choiceOrder(first.choices?.length ?? 0, choiceSeed(seed, where, 0));
    expect(attempt0[0], "this seed shows the right answer somewhere other than first").not.toBe(right);
    await expect.poll(() => shownOrder(page, prefix)).toEqual(attempt0);
    // The screen-reader order is the shown order: the radio buttons sit in the same order as the labels.
    await page.reload();
    await expect.poll(() => shownOrder(page, prefix)).toEqual(attempt0);
    // The authored right answer is graded right, wherever it shows.
    await page.getByTestId(`${prefix}${right}`).click();
    await page.getByTestId("quiz-check").click();
    await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();
    const second = quiz?.questions?.[1] as Question;
    const wrong = (second.choices ?? []).findIndex((choice) => choice !== String(second.answer));
    await page.getByTestId(`quiz-choice-${second.id}-${wrong}`).click();
    await page.getByTestId("quiz-check").click();
    await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", "false");
    await page.getByTestId("quiz-next").click();
    await expect(page.getByTestId("quiz-score")).toHaveText("1 of 2 right (50%)");
    // A retake is a new attempt: a new order.
    await page.getByTestId("quiz-retake").click();
    await expect.poll(() => shownOrder(page, prefix)).toEqual(choiceOrder(first.choices?.length ?? 0, choiceSeed(seed, where, 1)));

    // An exercise's Predict first: the same seed, its own order, and the ✓ on the authored answer.
    const lesson = unit.items.find((item) => item.id === "many-values-one-name");
    const predict = lesson?.exercises?.find((exercise) => exercise.id === "first-is-zero")?.predict;
    expect(predict).toBeTruthy();
    await open(page, "many-values-one-name", "first-is-zero");
    const expected = choiceOrder(predict?.choices.length ?? 0, choiceSeed(seed, `${UNIT_ID}/many-values-one-name/first-is-zero:predict`));
    await expect(page.locator('[data-testid="predict"] .ex-predict-choices')).toHaveAttribute("data-ready", "true");
    await expect.poll(() => shownOrder(page, "predict-choice-")).toEqual(expected);
    const miss = expected.find((index) => index !== predict?.answer) ?? 0;
    await page.getByTestId(`predict-choice-${miss}`).click();
    await expect(page.getByTestId("predict-result")).toHaveAttribute("data-correct", "false");
    await expect(page.getByTestId(`predict-choice-${predict?.answer}`)).toContainText("✓");
    await expect(page.getByTestId(`predict-choice-${miss}`)).toContainText("✗");
  });

  test("a Quick Check form needs both of its questions: 1 right does not pass, 2 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc3-a");
    const quiz = unit.items.find((item) => item.id === "qc3-a-questions");
    expect(form?.questionsToPass).toBe(2);
    expect(quiz?.questions).toHaveLength(2);
    // The three tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc3-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await page.goto("/intro-python");
    await page.evaluate(
      ([key, value]) => window.localStorage.setItem(key, value),
      [PROGRESS_KEY, JSON.stringify({ version: 1, exercises, quizzes: {}, read: {}, testedOut: {}, settings: { preset: "more" } })] as const,
    );
    await page.goto(`/intro-python/${UNIT_ID}/qc3-a`);
    await expect(page.getByTestId("testout-questions")).toContainText("Get both right");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);

    const answer = async (rightCount: number) => {
      for (const [at, question] of (quiz?.questions ?? []).entries()) {
        await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of 2`);
        const right = (question.choices ?? []).indexOf(String(question.answer));
        const choice = at < rightCount ? right : right === 0 ? 1 : 0;
        await page.getByTestId(`quiz-choice-${question.id}-${choice}`).click();
        await page.getByTestId("quiz-check").click();
        await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", at < rightCount ? "true" : "false");
        await page.getByTestId("quiz-next").click();
      }
    };
    await page.goto(`/intro-python/${UNIT_ID}/qc3-a-questions`);
    await answer(1);
    await expect(page.getByTestId("quiz-score")).toHaveText("1 of 2 right (50%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "false");
    await expect(page.getByTestId("quiz-quick-check")).toContainText("The Quick Check needs both of these right.");

    await page.getByTestId("quiz-retake").click();
    await answer(2);
    await expect(page.getByTestId("quiz-score")).toHaveText("2 of 2 right (100%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "true");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
  });
});
