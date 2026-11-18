/**
 * Unit 7 ("Functions II: Spells You Can Hand Over") in a real browser: what the teacher's ruling on Unit 7 asked of the
 * site. The explainer's Unit 7 rows, which trace a value to the call that handed it over (a function handed over with
 * `()`, its name in quotes, two values in the wrong order, text where a sheet goes, a guard that lets a key through), in
 * the unit's own words ("function", "parameter", never Unit 3's "recipe"); no "One fixed!" when the same KeyError comes
 * back on the same line of code, moved down by the guard's lines; the crash banner naming the line the fix goes on; the
 * same slip full in a lesson and lean in the SOLO and the Quick Check; lean Quick Check messages; and the Quick Check's
 * question gate (3 of 4).
 *
 * Every code below is one of the unit's own wrong answers (or a partial), read from the harness sidecar, so the
 * browser runs exactly what python3 proved. Browser parity for every exercise, quiz and Quick Check (Unit 7's
 * included: it reads every published unit) is in intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "spell-recipes";
const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");

type Code = string | string[];
type Question = { id: string; type: string; answer: number | string; choices?: string[] };
type RawItem = {
  id: string;
  kind: string;
  optional?: boolean;
  questionsToPass?: number;
  exercises?: { id: string; checkpoints: { id: string }[]; solution: Code }[];
  questions?: Question[];
};

const unit = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.json`), "utf8")) as { order: number; published: boolean; items: RawItem[] };
const sidecar = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.verify.json`), "utf8")) as {
  exercises: Record<string, { partials?: Code[]; wrongAnswers?: { why: string; code: Code }[] }>;
};

const codeText = (value: Code) => (Array.isArray(value) ? `${value.join("\n")}\n` : value);

/** The unit's own wrong answer for `key` ("<item>/<exercise>") whose `why` contains `why` (a whole `why` wins). */
function wrongAnswer(key: string, why: string): string {
  const near = (sidecar.exercises[key]?.wrongAnswers ?? []).filter((entry) => entry.why.includes(why));
  const exact = near.filter((entry) => entry.why === why);
  const found = exact.length === 1 ? exact : near;
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

/** Open an exercise (skipping its predict, which never blocks Run) and wait until Python can run. */
async function open(page: Page, itemId: string, exerciseId?: string) {
  await page.goto(`/intro-python/${UNIT_ID}/${itemId}${exerciseId ? `#${exerciseId}` : ""}`);
  await expect(page.getByTestId("exercise-player")).toBeVisible();
  await pythonReady(page);
  const skip = page.getByTestId("exercise-player").getByTestId("predict-skip");
  if ((await skip.count()) > 0) await skip.first().click();
}

/** Run one of the unit's wrong answers and return the explainer. */
async function runWrong(page: Page, key: string, why: string, run: number) {
  await setCode(page, wrongAnswer(key, why));
  await runAndWait(page, run);
  return page.getByTestId("explainer");
}

/** Start with saved settings (and, optionally, exercises already passed). */
async function startWith(page: Page, settings: Record<string, unknown>, exercises: Record<string, unknown> = {}) {
  await page.goto("/intro-python");
  await page.evaluate(
    ([key, value]) => window.localStorage.setItem(key, value),
    [PROGRESS_KEY, JSON.stringify({ version: 1, exercises, quizzes: {}, read: {}, testedOut: {}, settings })] as const,
  );
}

test.describe("Intro to Python, Unit 7: Functions II", () => {
  test("the unit is on the map after Loops, and its page offers the Quick Check: four tasks and 3 of 4 questions", async ({ page }) => {
    expect(unit.published).toBe(true);
    expect(unit.order).toBe(7);
    await page.goto("/intro-python");
    await expect(page.getByTestId(`unit-card-${UNIT_ID}`)).toBeVisible();
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Functions II");
    await expect(page.getByTestId("item-row-recipes-read-sheets")).not.toContainText("Optional");
    await expect(page.getByTestId("item-row-the-resonance-array")).not.toContainText("Optional");
    // The stretch group's challenge, from blank, never blocks anyone.
    await expect(page.getByTestId("item-row-spell-book-from-blank")).toContainText("Optional");
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get 3 of the 4 Quick Check questions right.");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 4 tasks and get 3 of the 4 questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 4");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Quick Check Recipes II");
  });

  test("a guard that lets the key through: the box names the real slip, and the same KeyError lower down is no 'One fixed!'", async ({ page }) => {
    await open(page, "recipes-read-sheets", "guard-at-the-door");
    const explainer = page.getByTestId("explainer");
    const hint = page.getByTestId("explainer-hint");
    // The starter: no guard yet. The test call stays, so never "Use a key that is already there".
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "missing-key");
    await expect(hint).toContainText('The call that hands over "Star Glow" is the test: keep it. Add your guard above line 5, so cast_glow asks first.');
    await expect(hint).not.toContainText("Use a key that is already there");
    // The fix goes above line 5: the crash banner says so.
    await expect(page.getByTestId("task-line")).toContainText("The mistake is on line 5 or a line above it.");

    // A guard with no `return`: the same KeyError on the same line of code, two lines lower. Nothing was fixed yet.
    await setCode(page, wrongAnswer("recipes-read-sheets/guard-at-the-door", "a guard with no return: shows the line, then carries on to the spell"));
    await runAndWait(page, 2);
    await expect(hint).toContainText('Your guard lets "Star Glow" through to line 7. Its if shows the line, but nothing stops the function');
    await expect(hint).toContainText("Put return on a new line under line 6, with the same spaces in front.");
    await expect(hint).not.toContainText("One fixed!");
    await expect(page.getByTestId("got-further")).toHaveCount(0);
    await expect(page.getByTestId("task-line")).toContainText("The mistake is on line 7 or a line above it.");

    // `in` for `not in`: the student's own guard line, with `not in`.
    await setCode(page, wrongAnswer("recipes-read-sheets/guard-at-the-door", "`in` for `not in`"));
    await runAndWait(page, 3);
    await expect(hint).toContainText('Ask not in: if spell_name not in hero["spell_book"]:');
    await expect(hint).not.toContainText("One fixed!");
  });

  test("a lesson traces the value to the call that handed it over, in the unit's words, and names that line", async ({ page }) => {
    const hint = page.getByTestId("explainer-hint");
    const task = page.getByTestId("task-line");

    // A function handed over WITH `()`: its `None` is called inside cast_on_everyone. The fix is the call on line 13.
    await open(page, "spells-you-can-hand-over", "hand-it-over");
    const handed = await runWrong(page, "spells-you-can-hand-over/hand-it-over", "handed over the result of a call: warm_hands(lucky) hands over None", 1);
    await expect(handed).toHaveAttribute("data-explainer", "full");
    await expect(handed).toHaveAttribute("data-kind", "not-a-function");
    await expect(hint).toContainText("Line 7 calls effect, and it holds None, Python's word for nothing. The call on line 13 hands over warm_hands(lucky)");
    await expect(hint).toContainText("Hand the function over by its name, with no (): cast_on_everyone(roster, warm_hands)");
    await expect(hint).not.toContainText("NoneType");
    await expect(hint).not.toContainText("recipe");
    await expect(task).toContainText("Python stopped at line 7, so it couldn't finish your code. The mistake is on line 13. Fix line 13, then press Run again.");
    await expect(page.getByTestId("python-last-line")).toContainText("'NoneType' object is not callable");

    // An empty `()`: never "hand over one value per parameter", which only gives warm_hands(lucky).
    const empty = await runWrong(page, "spells-you-can-hand-over/hand-it-over", "handed over WITH () (missing argument)", 2);
    await expect(empty).toHaveAttribute("data-kind", "wrong-number-of-values");
    await expect(hint).toContainText("Line 13 hands warm_hands() to cast_on_everyone. The () runs warm_hands right there");
    await expect(hint).not.toContainText("one value per");

    // The finished helper's values in the wrong order: the call's line, never "mixes kinds of values".
    await open(page, "recipes-read-sheets", "read-the-helper");
    const swapped = await runWrong(page, "recipes-read-sheets/read-the-helper", "the values in the wrong order", 1);
    await expect(swapped).toHaveAttribute("data-kind", "swapped-values");
    await expect(hint).toContainText("draw_bar takes the sheet as hero, and the call puts lucky where bar goes, so line 5 reads text as a sheet. Swap the two values on line 15.");
    await expect(task).toContainText("The mistake is on line 15. Fix line 15, then press Run again.");
    // Unit 7's words: parameter, never ingredient.
    const count = await runWrong(page, "recipes-read-sheets/read-the-helper", "one value only", 2);
    await expect(count).toHaveAttribute("data-kind", "wrong-number-of-values");
    await expect(hint).toContainText("draw_bar has 2 parameters, hero and bar, but the call on line 15 hands over 1. Hand over one value per parameter");
    await expect(hint).not.toContainText("ingredient");

    // The bar's parentheses around the stamp: the bar row, never "use int()".
    await open(page, "recipes-read-sheets", "broken-spell-6b");
    const bar = await runWrong(page, "recipes-read-sheets/broken-spell-6b", "brackets in the wrong place: still text minus a number", 1);
    await expect(bar).toHaveAttribute("data-kind", "bar-needs-brackets");
    await expect(hint).toContainText('Put the parentheses around the subtraction instead: empty = "░" * (hero["max_mana"] - hero["mana"])');
    await expect(hint).not.toContainText("int()");
  });

  test("the same slip is full in a lesson and lean in the SOLO and the Quick Check: the slip and its line, never the fix", async ({ page }) => {
    const hint = page.getByTestId("explainer-hint");
    // The SOLO: the call kept in the dictionary, so None is called. Lean names the slip, never `{"effect": shout}`.
    await open(page, "spells-you-can-hand-over", "solo-6c");
    await expect(page.getByTestId("solo")).toBeVisible();
    const solo = await runWrong(page, "spells-you-can-hand-over/solo-6c", "stored the call: shout(lucky) puts None in the dict", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "not-a-function");
    await expect(hint).toContainText("Line 14 puts shout(lucky) in roar[\"effect\"], with (lucky), so line 15 calls None, Python's word for nothing. Python's last line, below, says what it found.");
    await expect(hint).not.toContainText('{"effect": shout}');
    await expect(hint).not.toContainText("Hand the function over");

    // The Quick Check: a function handed over with an empty (), in the bottom call. Lean, no Help.
    await open(page, "qc-r2-a", "learn-a-ward");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const qc = await runWrong(page, "qc-r2-a/learn-a-ward", "CP3 the function handed over WITH () (it runs now, with no hero)", 1);
    await expect(qc).toHaveAttribute("data-explainer", "lean");
    await expect(hint).toContainText("Line 22 hands ash_ward() to learn_ward, with (), so ash_ward ran there with nothing in its parentheses.");
    await expect(hint).not.toContainText('learn_ward(wards, "Ash Ward", 4, ash_ward)');
    // The same slip in a lesson is full: the fixed call.
    await open(page, "spells-you-can-hand-over", "hand-it-over");
    const full = await runWrong(page, "spells-you-can-hand-over/hand-it-over", "handed over WITH () (missing argument)", 1);
    await expect(full).toHaveAttribute("data-explainer", "full");
    await expect(hint).toContainText("cast_on_everyone(roster, warm_hands)");

    // A Quick Check check message names the slip and the evidence, never the fix (C1, step 3: the 0 left in).
    await open(page, "qc-r2-a", "learn-a-ward");
    await setCode(page, codeText(sidecar.exercises["qc-r2-a/learn-a-ward"]?.partials?.[1] as Code));
    await runAndWait(page, 1);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText("The effect handed in is still 0.");
    await expect(message).not.toContainText("ash_ward");
  });

  test("a Quick Check form needs 3 of its 4 questions: 2 right does not pass, 3 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc-r2-a");
    const quiz = unit.items.find((item) => item.id === "qc-r2-a-questions");
    expect(form?.questionsToPass).toBe(3);
    expect(form?.exercises).toHaveLength(4);
    expect(quiz?.questions).toHaveLength(4);
    // The four tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc-r2-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await startWith(page, { preset: "more" }, exercises);
    await page.goto(`/intro-python/${UNIT_ID}/qc-r2-a`);
    await expect(page.getByTestId("testout-questions")).toContainText("Get 3 of the 4 right");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);

    const answer = async (rightCount: number) => {
      for (const [at, question] of (quiz?.questions ?? []).entries()) {
        await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of 4`);
        const right = typeof question.answer === "number" ? question.answer : (question.choices ?? []).indexOf(String(question.answer));
        expect(right, `${question.id}: the keyed answer is a choice`).toBeGreaterThanOrEqual(0);
        const choice = at < rightCount ? right : right === 0 ? 1 : 0;
        await page.getByTestId(`quiz-choice-${question.id}-${choice}`).click();
        await page.getByTestId("quiz-check").click();
        await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", at < rightCount ? "true" : "false");
        await page.getByTestId("quiz-next").click();
      }
    };
    await page.goto(`/intro-python/${UNIT_ID}/qc-r2-a-questions`);
    await answer(2);
    await expect(page.getByTestId("quiz-score")).toHaveText("2 of 4 right (50%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "false");
    await expect(page.getByTestId("quiz-quick-check")).toContainText("The Quick Check needs 3 of these 4 right.");

    await page.getByTestId("quiz-retake").click();
    await answer(3);
    await expect(page.getByTestId("quiz-score")).toHaveText("3 of 4 right (75%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "true");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
  });
});
