/**
 * Unit 1 ("Hello World: Words by the Fire") in a real browser: the site's way in (the nav link, the breadcrumbs)
 * and the play-through fixes that are Unit 1's own.
 *
 * Browser parity for every exercise, every quiz and the Quick Check runs for EVERY published unit (Unit 1
 * included) in intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { checkpoint, PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "hello-world";

type RawUnit = { id: string; title: string; published: boolean };

const unit = JSON.parse(
  readFileSync(path.join(process.cwd(), "content/courses/intro-python/units", `${UNIT_ID}.json`), "utf8"),
) as RawUnit;

const itemPath = (itemId: string) => `/intro-python/${UNIT_ID}/${itemId}`;

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

test.describe("Intro to Python, Unit 1: Hello World", () => {
  test("the site nav leads to the course map; Unit 1 shows without ?preview=1; breadcrumbs lead back", async ({ page }) => {
    expect(unit.published, "Unit 1 is published").toBe(true);
    await page.goto("/");
    await page.getByRole("navigation", { name: "Site" }).getByRole("link", { name: "Intro to Python" }).click();
    await expect(page.getByTestId("course-map")).toBeVisible();
    await expect(page).toHaveURL(/\/intro-python\/?$/);
    await expect(page.getByTestId("preview-banner")).toHaveCount(0);
    await expect(page.getByTestId(`unit-card-${UNIT_ID}`)).toContainText(unit.title);
    await expect(page.getByTestId("unit-card-sample")).toHaveCount(0);

    await page.getByTestId(`unit-link-${UNIT_ID}`).click();
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    // Form A, its questions, and Form B with its questions for a fresh try.
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

  test.describe("play-through fixes", () => {
    test("the first lesson's planned error does step 2: it is ticked, and stays ticked while step 3 puts the quote back", async ({ page }) => {
      await page.goto(`${itemPath("before-the-first-spell")}#what-an-error-looks-like`);
      await expect(page.getByTestId("exercise-title")).toHaveText("What an error looks like");
      await pythonReady(page);
      await runAndWait(page, 1);
      await expect(page.getByTestId("checkpoint-1")).toHaveAttribute("data-state", "passed");
      await expect(page.getByTestId("checkpoint-message-2")).toContainText("Step 2 is next");
      // Break the line on purpose: Python stops at line 1, as planned, and step 2 is done.
      await setCode(page, 'print("Shield up.)');
      await runAndWait(page, 2);
      await expect(page.getByTestId("checkpoint-2")).toHaveAttribute("data-state", "passed");
      await expect(page.getByTestId("task-line")).toHaveAttribute("data-planned", "true");
      await expect(page.getByTestId("task-line")).toContainText("Python stopped at line 1, as planned. Step 2 is done.");
      // Put the quote back but keep the dot: step 2 stays done (no ↺), and step 3 says what is left.
      await setCode(page, 'print("Shield up.")');
      await runAndWait(page, 3);
      await expect(page.getByTestId("checkpoint-2")).toHaveAttribute("data-state", "passed");
      await expect(page.getByTestId("checkpoint-2")).not.toHaveAttribute("data-slipped", "true");
      await expect(page.getByTestId("checkpoint-message-3")).toContainText("Change the `.` to `!`".replace(/`/g, ""));
      await setCode(page, 'print("Shield up!")');
      await runAndWait(page, 4);
      await expect(page.getByTestId("all-passed")).toBeVisible();
    });

    test("after a crash, Help aims at the line Python stopped on, and Python's last line is on screen", async ({ page }) => {
      await page.goto(`${itemPath("words-in-quotes")}#broken-spell-1a`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell: three mistakes");
      await pythonReady(page);
      await setCode(page, 'print("Shield up.")\nprint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("help-crash")).toContainText("Python stopped at line 3, so it couldn't finish your code. Fix line 3, then press Run again.");
      await expect(page.getByTestId("help-crash")).not.toContainText("its last line");
      // Help is for step 3 (the step that names line 3), not step 1, whose line is already right.
      await expect(page.getByTestId("help")).toHaveAttribute("data-step", "mend-line-3");
      await expect(page.getByTestId("help-button")).toContainText("step 3");
      await expect(page.getByTestId("python-last-line")).toContainText("NameError: name 'Steady' is not defined");
      await expect(page.getByTestId("traceback")).toBeHidden();
    });

    test("a Broken spell shows one \"Python got further\" line when the error moves on (no \"One fixed!\" too)", async ({ page }) => {
      await page.goto(`${itemPath("words-in-quotes")}#broken-spell-1a`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell: three mistakes");
      await pythonReady(page);
      await setCode(page, 'print("Shield up.)\nPrint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("got-further")).toHaveCount(0);
      await setCode(page, 'print("Shield up.")\nPrint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 2);
      await expect(page.getByTestId("got-further")).toHaveText(/Python got further: you fixed that mistake\./);
      await expect(page.getByTestId("explainer-hint")).not.toContainText("One fixed");
    });

    test("Keep it short has no Start me off on a step that edits a line already there, and tools sit apart from boxes", async ({ page }) => {
      await page.goto(`${itemPath("math-and-glue")}#spend-mana`);
      await page.evaluate((key) => {
        window.localStorage.setItem(
          key,
          JSON.stringify({ version: 1, exercises: {}, quizzes: {}, read: {}, testedOut: {}, settings: { preset: "short" } }),
        );
      }, PROGRESS_KEY);
      await page.reload();
      // The step's names (never reworded) say which exercise is open.
      await expect(page.getByTestId("names").getByTestId("name-chip-spell_cost")).toBeVisible();
      await expect(page.getByTestId("exercise-player")).toHaveAttribute("data-preset", "short");
      // Step 1 adds one more `mana = mana - spell_cost` line: the code already starts it, so Start me off is not
      // listed under More options (it would only say "Your code already starts this line").
      await expect(page.getByTestId("help-button")).toContainText("Help: Where to look");
      await expect(page.getByTestId("help-extra-another")).toHaveCount(1);
      await expect(page.getByTestId("help-extra-start")).toHaveCount(0);
      // Names to use holds the boxes; Python's tools have a row of their own.
      await expect(page.getByTestId("names")).toContainText("Names to use:");
      await expect(page.getByTestId("tools")).toHaveCount(0);

      await page.goto(`${itemPath("math-and-glue")}#glue-words`);
      await expect(page.getByTestId("names").getByTestId("name-chip-name")).toBeVisible();
      await expect(page.getByTestId("names").getByTestId("name-chip-mana")).toBeVisible();
      await expect(page.getByTestId("names").getByTestId("name-chip-str")).toHaveCount(0);
      await expect(page.getByTestId("tools")).toContainText("Tools to use:");
      await expect(page.getByTestId("tools").getByTestId("name-chip-str")).toBeVisible();

      // Lesson 1A's only name is `print`: a tool, and no "Names to use" before boxes are taught.
      await page.goto(`${itemPath("words-in-quotes")}#words-need-quotes`);
      await expect(page).toHaveURL(/#words-need-quotes$/);
      await expect(page.getByTestId("tools").getByTestId("name-chip-print")).toBeVisible();
      await expect(page.getByTestId("names")).toHaveCount(0);
    });

    test("a crash on a line no step names holds the steps' Help back; on the line step 4 names, Help is step 4's and names the box to make", async ({ page }) => {
      await page.goto(`${itemPath("boxes-with-labels")}#broken-spell-1b`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell");
      await pythonReady(page);
      // Line 6 (`print(weapn)`, a typo) is a line no step names: Help waits until the code runs.
      await setCode(page, 'weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapn)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("help-crash")).toContainText("Python stopped at line 6, so it couldn't finish your code. Fix line 6, then press Run again.");
      await expect(page.getByTestId("help")).toHaveAttribute("data-crash-only", "true");
      await expect(page.getByTestId("help-button")).toHaveCount(0);
      // Step 4 says "Fix line 4: ... so line 5 can't find `hero`": the crash on line 5 gets step 4's Help.
      await setCode(page, 'weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\n"Lucky"\nprint(hero)\nprint(weapon)\n');
      await runAndWait(page, 2);
      // The fix is on line 4 (the value with no name), not on line 5 where Python stopped: the banner says so.
      await expect(page.getByTestId("help-crash")).toContainText(
        "Python stopped at line 5, so it couldn't finish your code. The mistake is on line 4. Fix line 4, then press Run again.",
      );
      await expect(page.getByTestId("task-line")).toContainText("The mistake is on line 4. Fix line 4, then press Run again.");
      await expect(page.getByTestId("help")).toHaveAttribute("data-step", "line-4");
      await expect(page.getByTestId("help")).not.toHaveAttribute("data-crash-only", "true");
      await expect(page.getByTestId("help-button")).toContainText("step 4");
      await expect(page.getByTestId("explainer-hint")).toContainText("hero is one of your step's boxes");
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

    test("a run that prints too much with no loop names Python's line, never 'your loop' (Units 1-5 teach no loop)", async ({ page }) => {
      await page.goto(itemPath("ward-sign"));
      await expect(page.getByTestId("exercise-player")).toBeVisible();
      await pythonReady(page);
      await setCode(page, 'ink = "#"\nprint(ink * 300000)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "too-much-output");
      const task = page.getByTestId("task-line");
      await expect(task).not.toHaveAttribute("data-endless", "true");
      await expect(task).toContainText("Python stopped at line 2, so it couldn't finish your code. Fix line 2, then press Run again.");
      await expect(task).not.toContainText("loop");
      await page.getByTestId("run").click();
      await expect(page.getByTestId("run-count")).toHaveText(/Run 2 finished/, { timeout: 60_000 });
      await expect(page.getByTestId("same-error")).toHaveText("Same error as last time. Look closely at line 2.");
    });

    test("in a print-only exercise, Mar'tu's pick on an empty line goes in as a print line", async ({ page }) => {
      await page.goto(`${itemPath("boxes-with-labels")}#keyboard-symbols`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Where the symbols live");
      await pythonReady(page);
      await setCode(page, "# Your line goes here:\n");
      const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
      await lines.nth(1).click();
      await page.getByTestId("pick-use").first().click();
      await expect(lines.nth(1)).toHaveText('print("_ - = are side by side.")');
      await runAndWait(page, 1);
      await expect(page.getByTestId("all-passed")).toBeVisible();
    });
  });
});
