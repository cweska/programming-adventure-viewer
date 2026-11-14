/**
 * Unit 3 ("Functions I: First Recipes") in a real browser: what the teacher's ruling on the Unit 3 reviews asked
 * of the site. The explainer's recipe rows (a recipe written like math, an ingredient in quotes, the wrong number
 * of values for a recipe's ingredients, `randint` the wrong way round, a recipe called before its `def`, a call's
 * unquoted words split on its commas), full in a lesson and lean in the SOLO and the Quick Check, lean Quick Check
 * check messages, the Quick Check's question gate, and the optional challenge.
 *
 * Every code below is one of the unit's own wrong answers, read from the harness sidecar, so the browser runs
 * exactly what python3 proved. Browser parity for every exercise, quiz and Quick Check is in
 * intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "first-recipes";
const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");

type Code = string | string[];
type Question = { id: string; type: string; answer: number | string; choices?: string[] };
type RawItem = {
  id: string;
  kind: string;
  questionsToPass?: number;
  exercises?: { id: string; checkpoints: { id: string }[] }[];
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

async function open(page: Page, itemId: string, exerciseId: string) {
  await page.goto(`/intro-python/${UNIT_ID}/${itemId}#${exerciseId}`);
  await expect(page.getByTestId("exercise-player")).toBeVisible();
  await pythonReady(page);
}

/** Run one of the unit's wrong answers and return the explainer. */
async function runWrong(page: Page, key: string, why: string, run: number) {
  await setCode(page, wrongAnswer(key, why));
  await runAndWait(page, run);
  return page.getByTestId("explainer");
}

test.describe("Intro to Python, Unit 3: Functions I: First Recipes", () => {
  test("the unit page lists the challenge as optional, and the Quick Check counts its five tasks and its questions", async ({ page }) => {
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByTestId("item-row-supply-run")).toContainText("Optional");
    await expect(page.getByTestId("item-row-recipes-with-names")).not.toContainText("Optional");
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get 3 of the 4");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 5 tasks and get 3 of the 4 questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 5");

    await page.goto(`/intro-python/${UNIT_ID}/supply-run`);
    const header = page.locator(".item-header");
    await expect(header).toContainText("Advanced");
    await expect(header).toContainText("Optional");
  });

  test("a lesson exercise gets the full recipe explainer: f(x) = 5x and an ingredient in quotes", async ({ page }) => {
    await open(page, "recipes-with-names", "send-it-back");
    const math = await runWrong(page, "recipes-with-names/send-it-back", "written like maths", 1);
    await expect(math).toHaveAttribute("data-explainer", "full");
    await expect(math).toHaveAttribute("data-kind", "recipe-like-math");
    await expect(page.getByTestId("explainer-hint")).toContainText("Line 8 is math's way to write it.");
    await expect(page.getByTestId("explainer-hint")).toContainText("def max_fuel_for(cells):");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("two equals");
    await expect(page.getByTestId("python-last-line")).toContainText("cannot assign to function call");

    const quoted = await runWrong(page, "recipes-with-names/send-it-back", "ingredient name in quotes", 2);
    await expect(quoted).toHaveAttribute("data-kind", "quoted-ingredient");
    await expect(page.getByTestId("explainer-hint")).toContainText("Ingredient names have no quotes: def max_fuel_for(cells):");
    await expect(page.getByTestId("explainer-hint")).not.toContainText('max_fuel_for = "cells"');

    const early = await runWrong(page, "recipes-with-names/send-it-back", "try line uncommented", 3);
    await expect(early).toHaveAttribute("data-kind", "recipe-not-made-yet");
    await expect(page.getByTestId("explainer-hint")).toContainText("max_fuel_for is one of this task's recipes");
  });

  test("the wrong number of values names the recipe's own ingredients, and randint's numbers are swapped back", async ({ page }) => {
    await open(page, "recipes-with-names", "use-the-ingredients");
    const count = await runWrong(page, "recipes-with-names/use-the-ingredients", "third call hands over one number", 1);
    await expect(count).toHaveAttribute("data-kind", "wrong-number-of-values");
    await expect(page.getByTestId("explainer-hint")).toHaveText(
      /show_hit has 2 ingredients \(base_damage, bonus\)\. The call on line 6 hands over 1\. Hand over one value per ingredient\./,
    );
    await expect(page.getByTestId("explainer-hint")).not.toContainText("positional");
    await expect(page.getByTestId("python-last-line")).toContainText("missing 1 required positional argument");

    await open(page, "recipes-with-names", "roll-recipe");
    const roll = await runWrong(page, "recipes-with-names/roll-recipe", "randint(die_size, 1)", 1);
    await expect(roll).toHaveAttribute("data-kind", "randint-backwards");
    await expect(page.getByTestId("explainer-hint")).toContainText("Smallest number first: random.randint(1, die_size)");
    await expect(page.getByTestId("python-last-line")).toContainText("empty range in randrange(20, 2)");

    await open(page, "recipes-with-names", "box-or-recipe");
    const order = await runWrong(page, "recipes-with-names/box-or-recipe", "called before it is defined", 1);
    await expect(order).toHaveAttribute("data-kind", "recipe-called-too-early");
    await expect(page.getByTestId("explainer-hint")).toContainText("Line 1 calls say_steady, but its def is only on line 6.");
  });

  test("a name the recipe never makes and a store written backwards get the recipe's own names, never quotes", async ({ page }) => {
    await open(page, "recipes-with-names", "return-the-right-box");
    const box = await runWrong(page, "recipes-with-names/return-the-right-box", "the starter: `return result`", 1);
    await expect(box).toHaveAttribute("data-explainer", "full");
    await expect(box).toHaveAttribute("data-kind", "not-in-recipe");
    await expect(page.getByTestId("explainer-hint")).toContainText(
      "Line 3 hands back result, but no line in armor_total makes a box by that name. This recipe's box is total: hand that back.",
    );
    await expect(page.getByTestId("explainer-hint")).not.toContainText("quotes");

    await open(page, "recipes-with-names", "store-then-pass");
    const store = await runWrong(page, "recipes-with-names/store-then-pass", "store reversed", 1);
    await expect(store).toHaveAttribute("data-kind", "store-backwards");
    await expect(page.getByTestId("explainer-hint")).toContainText("greeting = get_greeting()");

    // Lean in the SOLO: the kind of slip and its line, never the recipe's box.
    await open(page, "recipes-with-names", "solo-6a");
    const solo = await runWrong(page, "recipes-with-names/solo-6a", "a name the recipe never makes", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "not-in-recipe");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 9: a name this recipe never makes.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("ingredient");
    await expect(page.getByTestId("python-last-line")).toContainText("name 'new_health' is not defined");
  });

  test("a call's unquoted words are split on its commas: full in the side quest, lean in the SOLO", async ({ page }) => {
    await open(page, "extra-recipe-twins", "cheer-on");
    const cheer = await runWrong(page, "extra-recipe-twins/cheer-on", "split-on-commas", 1);
    await expect(cheer).toHaveAttribute("data-explainer", "full");
    await expect(cheer).toHaveAttribute("data-kind", "unquoted-words");
    await expect(page.getByTestId("explainer-hint")).toContainText('cheer_on("Captain Glug", "Go now")');

    await open(page, "recipes-with-names", "solo-6a");
    const solo = await runWrong(page, "recipes-with-names/solo-6a", "two words with no quotes", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "unquoted-words");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 6: words with no quotes.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("Moth Queen");
    await expect(page.getByTestId("python-last-line")).toContainText("Perhaps you forgot a comma?");
  });

  test("a Quick Check task is lean: the explainer and the check messages name the slip, never the fix", async ({ page }) => {
    await open(page, "qc-r1-a", "write-a-recipe");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const math = await runWrong(page, "qc-r1-a/write-a-recipe", "= used to make a recipe (a call on the left)", 1);
    await expect(math).toHaveAttribute("data-explainer", "lean");
    await expect(math).toHaveAttribute("data-kind", "recipe-like-math");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 1: a recipe written like math.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("def armor_total");

    await open(page, "qc-r1-a", "a-check-of-your-own");
    await setCode(page, wrongAnswer("qc-r1-a/a-check-of-your-own", "> instead of >= (exactly enough fails)"));
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveCount(0);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText("Exactly enough does not pass.");
    await expect(message).toContainText("(Mar'tu's check called latch_check(12), only inside the check");
    await expect(message).not.toContainText(">=");
    await expect(message).not.toContainText("Which sign");
  });

  test("a pasted program is stopped before it runs: the console never shows the traced number", async ({ page }) => {
    // Quick Check Form A, Trace the call: the program from Mar'tu's block, pasted above the rows and run.
    await open(page, "qc-r1-a", "trace-the-call");
    await setCode(page, wrongAnswer("qc-r1-a/trace-the-call", "the program pasted in and run"));
    await runAndWait(page, 1);
    await expect(page.getByTestId("stdout")).toHaveText("(Nothing was printed.)");
    await expect(page.getByTestId("stdout")).not.toContainText("55");
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("The editor holds more than the two row lines");
    // Rows only: they run (and print nothing), and the guard stays out of the way.
    await setCode(page, "# The ledger for ward_strength(2, 5)\nhanded_back_row = 45\nprinted_row = 55\n");
    await runAndWait(page, 2);
    await expect(page.getByTestId("checkpoint-2")).toHaveAttribute("data-state", "passed");

    // The lesson's ledger: the same guard, and no Assemble it (its pieces were the finished rows).
    await open(page, "recipes-with-names", "be-the-ledger");
    await setCode(page, wrongAnswer("recipes-with-names/be-the-ledger", "the program pasted in above the rows"));
    await runAndWait(page, 1);
    await expect(page.getByTestId("stdout")).toHaveText("(Nothing was printed.)");
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("The ledger holds only your rows.");
    await setCode(page, wrongAnswer("recipes-with-names/be-the-ledger", "a row worked out with a print() line"));
    await runAndWait(page, 2);
    await expect(page.getByTestId("stdout")).toHaveText("(Nothing was printed.)");
  });

  test("Send it back with the try line on: def and = mix-ups and a borrowed box get the recipe's own def and box", async ({ page }) => {
    await open(page, "recipes-with-names", "send-it-back");
    const key = "recipes-with-names/send-it-back";
    const borrowed = await runWrong(page, key, "with the try line on (the crash path", 1);
    await expect(borrowed).toHaveAttribute("data-kind", "not-in-recipe");
    await expect(page.getByTestId("explainer-hint")).toContainText("result comes from Mar'tu's example. This recipe's box is fuel: hand that back.");
    const kitchen = await runWrong(page, key, "kitchen, with the try line on", 2);
    await expect(kitchen).toHaveAttribute("data-kind", "made-inside-recipe");
    await expect(page.getByTestId("explainer-hint")).toContainText("Inside max_fuel_for, hand back its own box, fuel.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("Out here");

    for (const [why, run] of [
      ["worked out from its ingredient (`max_fuel_for", 3],
      ["is made, with the try line on (the box called)", 4],
      ["def mixed with =", 5],
      ["and a colon at the end", 6],
    ] as const) {
      const mixed = await runWrong(page, key, why, run);
      await expect(mixed).toHaveAttribute("data-kind", "recipe-like-math");
      await expect(page.getByTestId("explainer-hint")).toContainText("def max_fuel_for(cells):");
      await expect(page.getByTestId("explainer-hint")).not.toContainText("max_fuel_for = cells");
      await expect(page.getByTestId("explainer-hint")).not.toContainText("cells =");
    }
  });

  test("Start me off before a click goes in place of the recipe's pass, and Another way labels show their code", async ({ page }) => {
    await open(page, "recipes-with-names", "ingredients");
    await page.getByTestId("run").click();
    await expect(page.getByTestId("run-count")).toHaveText(/Run 1 finished/, { timeout: 60_000 });
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-start-code")).toHaveText("print(");
    await page.getByTestId("help-start-insert").click();
    const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
    await expect(lines.nth(2)).toHaveText("    print(");
    await expect(lines.last()).not.toHaveText("print(");
    await expect(page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-content')).not.toContainText("pass");

    // An angle label with a code span shows it as code, never as backticks.
    await open(page, "recipes-with-names", "return-the-right-box");
    const another = page.getByTestId("another-way").first();
    await expect(another).toContainText("Whose kitchen is result in?");
    await expect(another).not.toContainText("`");
    await expect(another.locator("code")).toHaveText("result");
  });

  test("a Quick Check form needs 3 of its 4 questions: 2 right does not pass, 3 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc-r1-a");
    const quiz = unit.items.find((item) => item.id === "qc-r1-a-questions");
    expect(form?.questionsToPass).toBe(3);
    expect(quiz?.questions).toHaveLength(4);
    // The five tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc-r1-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await page.goto("/intro-python");
    await page.evaluate(
      ([key, value]) => window.localStorage.setItem(key, value),
      [PROGRESS_KEY, JSON.stringify({ version: 1, exercises, quizzes: {}, read: {}, testedOut: {}, settings: { preset: "more" } })] as const,
    );
    await page.goto(`/intro-python/${UNIT_ID}/qc-r1-a`);
    await expect(page.getByTestId("testout-questions")).toContainText("Get 3 of the 4 right");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);

    const answer = async (rightCount: number) => {
      for (const [at, question] of (quiz?.questions ?? []).entries()) {
        await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of 4`);
        const right = question.type === "mc" ? Number(question.answer) : (question.choices ?? []).indexOf(String(question.answer));
        const choice = at < rightCount ? right : right === 0 ? 1 : 0;
        await page.getByTestId(`quiz-choice-${question.id}-${choice}`).click();
        await page.getByTestId("quiz-check").click();
        await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", at < rightCount ? "true" : "false");
        await page.getByTestId("quiz-next").click();
      }
    };
    await page.goto(`/intro-python/${UNIT_ID}/qc-r1-a-questions`);
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
