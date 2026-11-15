/**
 * Unit 6 ("Loops: Every Member of the Party") in a real browser: what the teacher's ruling on the Unit 6 reviews asked
 * of the site. The explainer's loop rows (a list asked for a key inside a loop over it, the loop variable used as a
 * position, a `for` loop over one number, a whole sheet or list added to a number, a list's name in quotes in the `for`
 * line, a recipe's own ingredient name handed over in the loop, the ley board handed its pieces with a comma), full in
 * a lesson and lean in the SOLO and the Quick Check (in the teacher's own words where the ruling gives them); a loop
 * that never ends, stopped with a readable message whether it prints or not, after which Python comes back; lean Quick
 * Check messages; the Quick Check's question gate (3 of 4); and Start me off landing where its hint says.
 *
 * Every code below is one of the unit's own wrong answers (or a partial), read from the harness sidecar, so the
 * browser runs exactly what python3 proved; the one exception is the silent endless loop, which the harness never
 * runs (it would wait out its 6-second limit on every pass). Browser parity for every exercise, quiz and Quick Check is
 * in intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "loops";
const UNITS_DIR = path.join(process.cwd(), "content/courses/intro-python/units");

type Code = string | string[];
type Question = { id: string; type: string; answer: number | string; choices?: string[] };
type RawItem = {
  id: string;
  kind: string;
  questionsToPass?: number;
  exercises?: { id: string; checkpoints: { id: string }[]; solution: Code; predict?: unknown }[];
  questions?: Question[];
};

const unit = JSON.parse(readFileSync(path.join(UNITS_DIR, `${UNIT_ID}.json`), "utf8")) as { items: RawItem[] };
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

/** Mar'tu's version after step `n` of `key` (the harness's partial n). */
function partial(key: string, n: number): string {
  const found = sidecar.exercises[key]?.partials?.[n - 1];
  expect(found, `${key}: partial ${n}`).toBeTruthy();
  return codeText(found as Code);
}

/** Mar'tu's version of an exercise in a lesson. */
function solutionOf(itemId: string, exerciseId: string): string {
  const exercise = unit.items.find((item) => item.id === itemId)?.exercises?.find((entry) => entry.id === exerciseId);
  expect(exercise, `${itemId}/${exerciseId}`).toBeTruthy();
  return codeText(exercise?.solution as Code);
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

test.describe("Intro to Python, Unit 6: Loops", () => {
  test("the unit page offers the Quick Check, which needs its three tasks and 3 of its 4 questions", async ({ page }) => {
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Loops");
    await expect(page.getByTestId("item-row-for-each-yes")).not.toContainText("Optional");
    await expect(page.getByTestId("item-row-gearshifts-forecast")).toContainText("Optional");
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get 3 of the 4 Quick Check questions right.");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 3 tasks and get 3 of the 4 questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 3");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Quick Check 6");
  });

  test("a lesson gets the full loop rows: the loop variable for a key, a sheet for a position, the ley board's one text, the quotes", async ({ page }) => {
    await open(page, "for-each-yes", "each-member");
    const key = await runWrong(page, "for-each-yes/each-member", 'roster["name"] for member["name"] (TypeError)', 1);
    await expect(key).toHaveAttribute("data-explainer", "full");
    await expect(key).toHaveAttribute("data-kind", "name-as-position");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText('Line 7 asks a list for a key, like roster["name"]. A list has positions, not keys. Read one sheet through the loop variable: member["name"].');
    // Never Unit 5's "a position number", which sent students to roster[0] inside the loop.
    await expect(hint).not.toContainText("roster[0]");
    await expect(page.getByTestId("python-last-line")).toContainText("list indices must be integers or slices, not str");

    const sheet = await runWrong(page, "for-each-yes/each-member", "the item used as an index (roster[hero])", 2);
    await expect(sheet).toHaveAttribute("data-kind", "name-as-position");
    await expect(hint).toContainText("A list's positions are numbers, and member already holds one sheet: read it directly, member[\"name\"].");

    const board = await runWrong(page, "for-each-yes/each-member", "a comma, as in print: the ley board takes one text (TypeError)", 3);
    await expect(board).toHaveAttribute("data-kind", "wrong-number-of-values");
    await expect(hint).toContainText("show_on_ley_board takes one piece of text. Glue the parts into one with +, with str() around a number.");

    const quoted = await runWrong(page, "for-each-yes/each-member", "the list's name in quotes: the loop walks the letters of the text roster", 4);
    await expect(quoted).toHaveAttribute("data-kind", "quoted-name");
    await expect(hint).toContainText("Take the quotes off roster. With quotes, the loop walks its letters. No quotes means look inside the list.");
    await expect(page.getByTestId("python-last-line")).toContainText("string indices must be integers");

    await open(page, "for-each-yes", "how-much-each-gap-shrank");
    const number = await runWrong(page, "for-each-yes/how-much-each-gap-shrank", "for i in len(...) ('int' object is not iterable)", 1);
    await expect(number).toHaveAttribute("data-kind", "loop-over-number");
    await expect(hint).toContainText("Line 2 asks a for loop to walk one number. A for loop needs a list or range(...), not one number.");

    await open(page, "for-each-yes", "running-total");
    const whole = await runWrong(page, "for-each-yes/running-total", "the whole sheet added (TypeError)", 1);
    await expect(whole).toHaveAttribute("data-kind", "whole-card-compared");
    await expect(hint).toContainText('member is a whole sheet. Add one value from it by its key, like member["mana"].');

    // The recipe's own ingredient name handed over in the loop: the loop variable goes there, never "put quotes around it".
    await open(page, "for-each-yes", "bars-for-everyone");
    const hero = await runWrong(page, "for-each-yes/bars-for-everyone", "the recipe's ingredient name used in the loop's call, with the name (NameError)", 1);
    await expect(hero).toHaveAttribute("data-kind", "made-inside-recipe");
    await expect(hint).toContainText("hero is mana_bar's own ingredient name. It only exists inside the recipe. Out here, hand over a value of your own: inside a loop, its loop variable, like mana_bar(member).");
    await expect(hint).not.toContainText("quotes");

    // 5B-03: the quoted wall crashes on the `if` line; the quotes on line 2 are the slip.
    await open(page, "while-the-clock-ticks", "stop-at-the-first");
    const wall = await runWrong(page, "while-the-clock-ticks/stop-at-the-first", "the quoted list name: the loop walks the letters of the text chalk_wall", 1);
    await expect(wall).toHaveAttribute("data-kind", "quoted-name");
    await expect(hint).toContainText("Line 2 with no quotes: for gap in chalk_wall:");
    await expect(hint).not.toContainText("int()");
  });

  test("the same slip is full in a lesson and lean in the SOLO and the Quick Check, in the teacher's words", async ({ page }) => {
    await open(page, "for-each-yes", "solo-5a");
    await expect(page.getByTestId("solo")).toBeVisible();
    const solo = page.getByTestId("explainer");
    // The SOLO's own starter: roster[member], the loop variable used as a position.
    await runAndWait(page, 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "name-as-position");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText("Line 8 uses a whole sheet as a position, like roster[member]. Python's last line, below, says what it found.");
    await expect(hint).not.toContainText("directly");
    await expect(hint).not.toContainText('member["name"]');
    await expect(page.getByTestId("python-last-line")).toContainText("list indices must be integers or slices, not dict");

    await runWrong(page, "for-each-yes/solo-5a", 'roster["name"] for member["name"] (TypeError)', 2);
    await expect(hint).toContainText('Line 8 asks a list for a key, like roster["name"]. A list has positions, not keys. Python\'s last line');
    await expect(hint).not.toContainText("loop variable");

    await open(page, "qc5-a", "a-helper-for-each");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const number = await runWrong(page, "qc5-a/a-helper-for-each", "a loop over a number: for i in 4", 1);
    await expect(number).toHaveAttribute("data-explainer", "lean");
    await expect(number).toHaveAttribute("data-kind", "loop-over-number");
    await expect(hint).toContainText("Line 7 asks a for loop to walk one number. A for loop needs a list or range(...), not one number.");
    const promise = await runWrong(page, "qc5-a/a-helper-for-each", "the helper's own word read as a promise: light_lantern(name)", 2);
    await expect(promise).toHaveAttribute("data-kind", "made-inside-recipe");
    await expect(hint).toContainText("The slip is on line 8: a name that only lives inside a recipe.");
    await expect(hint).not.toContainText('member["name"]');
    await expect(hint).not.toContainText("put quotes around it");

    // A Quick Check message names the slip and the evidence, never the fix.
    await setCode(page, wrongAnswer("qc5-a/a-helper-for-each", "four typed calls"));
    await runAndWait(page, 3);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText("typed in the code");
    await expect(message).not.toContainText("for member in roster");
  });

  test("a loop that never ends stops with a readable message, printing or silent, and Python comes back", async ({ page }) => {
    await open(page, "while-the-clock-ticks", "the-loop-that-never-ends");
    // The starter prints on every pass: the output limit stops it in a moment.
    await runAndWait(page, 1);
    const explainer = page.getByTestId("explainer");
    await expect(explainer).toHaveAttribute("data-kind", "too-much-output");
    await expect(page.getByTestId("explainer").locator(".ex-explainer-title")).toHaveText("Printing forever?");
    await expect(page.getByTestId("explainer-hint")).toContainText("A loop may be running forever: make sure it has a way to end.");
    await expect(page.getByTestId("python-last-line")).toContainText("TooMuchOutput: This program printed more than 200,000 characters, so it was stopped.");
    // The line it was stopped on (the print) is right: no "First, mend line 3", and Help stays on the step.
    const task = page.getByTestId("task-line");
    await expect(task).toHaveAttribute("data-endless", "true");
    await expect(task).toContainText("First, make the loop end. Python stopped your program before it could check your steps.");
    await expect(task).not.toContainText("line 3");
    await expect(page.getByTestId("help-button")).toBeVisible();
    await expect(page.getByTestId("help-crash-wait")).toHaveCount(0);

    // A loop with no update that prints nothing: the 5-second limit stops it, and says why.
    await setCode(page, 'glug = 3\nwhile glug > 0:\n    glug + 1\nprint("The canteen is empty.")\n');
    await runAndWait(page, 2);
    await expect(explainer).toHaveAttribute("data-kind", "timeout");
    await expect(page.getByTestId("explainer").locator(".ex-explainer-title")).toHaveText("Ran too long");
    await expect(page.getByTestId("explainer-hint")).toHaveText(
      "Your code ran for more than 5 seconds, so it was stopped. A while loop may never end: make sure its condition can become False.",
    );
    await expect(page.getByTestId("python-last-line")).toContainText("The program ran too long and was stopped.");

    // Python restarts on its own; the mended loop then runs and passes.
    await pythonReady(page);
    await setCode(page, solutionOf("while-the-clock-ticks", "the-loop-that-never-ends"));
    await runAndWait(page, 3);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("stdout")).toContainText("The canteen is empty.");

    // The SOLO's wrong-way update: always the full "Printing forever?", even in a lean exercise.
    await open(page, "while-the-clock-ticks", "solo-5b");
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "too-much-output");
    await expect(page.getByTestId("explainer").locator(".ex-explainer-title")).toHaveText("Printing forever?");

    // A broken spell whose steps name lines ("Mend line 5 ..."): Help is there for the step, never "wait until it runs".
    await open(page, "extra-loops-that-end", "broken-spell-5b");
    await runAndWait(page, 1);
    await expect(explainer).toHaveAttribute("data-kind", "too-much-output");
    await expect(page.getByTestId("task-line")).toContainText("First, make the loop end.");
    await expect(page.getByTestId("help-button")).toBeVisible();
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help")).toHaveAttribute("data-step", "count-down");
  });

  test("Start me off lands where its hint says: under the note, and above the line it goes before", async ({ page }) => {
    const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
    // countdown: "under `# After the loop: print Burst!`", at the left edge, outside the loop.
    await open(page, "while-the-clock-ticks", "countdown");
    await runAndWait(page, 1);
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-rung-1")).toHaveAttribute("data-kind", "start");
    await expect(page.getByTestId("help-start-code")).toHaveText("print(");
    await page.getByTestId("help-start-insert").click();
    await expect(lines.nth(4)).toHaveText("# After the loop: print Burst!");
    await expect(lines.nth(5)).toHaveText("print(");
    await expect(lines.nth(3)).toHaveText("    hours_left = hours_left - 1");

    // bars-for-everyone, step 2: "above `return full * hero["mana"]`", inside the recipe, four spaces in.
    await open(page, "for-each-yes", "bars-for-everyone");
    await setCode(page, partial("for-each-yes/bars-for-everyone", 1));
    await runAndWait(page, 1);
    await expect(page.getByTestId("checkpoint-pass-1")).toBeVisible();
    // Back to the page with step 1 done and its code saved, before any click in the editor (Start me off then goes
    // where its hint says; after a click it goes at the cursor).
    await page.reload();
    await pythonReady(page);
    const skip = page.getByTestId("exercise-player").getByTestId("predict-skip");
    if ((await skip.count()) > 0) await skip.first().click();
    await runAndWait(page, 1);
    await expect(page.getByTestId("checkpoint-2")).toHaveAttribute("data-state", "active");
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-start-code")).toHaveText("used =");
    await page.getByTestId("help-start-insert").click();
    const used = lines.filter({ hasText: "used =" });
    await expect(used).toHaveCount(1);
    await expect(used).toHaveText("    used = ");
    // On a new line of its own, right above the return line (with its indent), which stays as it was.
    const all = (await lines.allTextContents()).map((text) => text.replace(/\u00a0/g, " "));
    const at = all.findIndex((text) => text.trim() === "used =");
    expect(at).toBeGreaterThan(0);
    expect(all[at].startsWith("    used =")).toBe(true);
    expect(all[at + 1].trim()).toBe('return full * hero["mana"]');
  });

  test("a Quick Check form needs 3 of its 4 questions: 2 right does not pass, 3 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc5-a");
    const quiz = unit.items.find((item) => item.id === "qc5-a-questions");
    expect(form?.questionsToPass).toBe(3);
    expect(quiz?.questions).toHaveLength(4);
    // The three tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc5-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await startWith(page, { preset: "more" }, exercises);
    await page.goto(`/intro-python/${UNIT_ID}/qc5-a`);
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
    await page.goto(`/intro-python/${UNIT_ID}/qc5-a-questions`);
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

  test("the article's glossary links with a code label show as code, never as [[ | ]] marks", async ({ page }) => {
    await page.goto(`/intro-python/${UNIT_ID}/looping-over-a-dictionary`);
    const article = page.getByTestId("article");
    await expect(article).toBeVisible();
    await expect(article).not.toContainText("[[");
    await expect(article).not.toContainText("|");
    await expect(article.locator("code", { hasText: ".items()" }).first()).toBeVisible();
  });
});
