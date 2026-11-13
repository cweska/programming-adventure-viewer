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
import { checkpoint } from "./course";
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

    test("a Broken spell shows one \"Python got further\" line when the error moves on (no \"One fixed!\" too)", async ({ page }) => {
      await page.goto(`${itemPath("words-in-quotes")}#broken-spell-1a`);
      await expect(page.getByTestId("exercise-title")).toHaveText("Broken spell: three slips");
      await pythonReady(page);
      await setCode(page, 'print("Shield up.)\nPrint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 1);
      await expect(page.getByTestId("got-further")).toHaveCount(0);
      await setCode(page, 'print("Shield up.")\nPrint("Barrier\'s holding.")\nprint(Steady)\n');
      await runAndWait(page, 2);
      await expect(page.getByTestId("got-further")).toHaveText(/Python got further: that slip is mended\./);
      await expect(page.getByTestId("explainer-hint")).not.toContainText("One fixed");
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
});
