/**
 * Unit 2 ("Control Flow: The Ley Clock Decides") in a real browser: what the teacher's ruling on the Unit 2
 * reviews asked of the site. The lean explainer in SOLO items and Quick Check 2, "Python got further" in a
 * debugging exercise, and the explainer's Unit 2 slips.
 *
 * Browser parity for every exercise, every quiz and the Quick Check is in intro-python-units.spec.ts.
 */
import { expect, test, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "control-flow";

const itemPath = (itemId: string, exerciseId: string) => `/intro-python/${UNIT_ID}/${itemId}#${exerciseId}`;

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

async function open(page: Page, itemId: string, exerciseId: string, title: string) {
  await page.goto(itemPath(itemId, exerciseId));
  await expect(page.getByTestId("exercise-title")).toHaveText(title);
  await pythonReady(page);
}

test.describe("Intro to Python, Unit 2: Control Flow", () => {
  test("a SOLO item's lean explainer names the slip and the line, never the fix, and Python's last line stays", async ({ page }) => {
    await open(page, "true-or-false-yes", "solo-2a", "Show Mar'tu");
    await setCode(page, "mana = 9\ncost = 9\ncan_cast = mana => cost\nprint(can_cast)\n");
    await runAndWait(page, 1);
    const explainer = page.getByTestId("explainer");
    await expect(explainer).toHaveAttribute("data-explainer", "lean");
    await expect(explainer).toHaveAttribute("data-kind", "sign-backwards");
    await expect(explainer.locator(".ex-explainer-title")).toHaveText("Sign typed backwards");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 3: a sign typed backwards.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText(">=");
    await expect(page.getByTestId("python-last-line")).toContainText("SyntaxError: invalid syntax");
  });

  test("a lesson exercise keeps the full explainer, with the line written right", async ({ page }) => {
    await open(page, "true-or-false-yes", "enough-to-pass", "Enough to pass");
    const code = "roll = 14\nneeded = 15\npassed = roll => needed\nprint(passed)\n";
    await setCode(page, code);
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "full");
    await expect(page.getByTestId("explainer-hint")).toContainText("Write: passed = roll >= needed");
  });

  test("a Broken spell says \"Python got further\" each time a run gets past the last slip, in one line", async ({ page }) => {
    await open(page, "true-or-false-yes", "broken-spell-2a", "Broken spell");
    const starter = 'roll = 17\nneeded = "15"\npassed = roll => needed\nprint(passed)\nclock_color = "blue"\nclock_is_red = "red"\nprint(clock_is_red)\n';
    await setCode(page, starter);
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "sign-backwards");
    await expect(page.getByTestId("got-further")).toHaveCount(0);

    // Line 3 mended: Python now stops on the same line for another reason (the text "15").
    await setCode(page, starter.replace("roll => needed", "roll >= needed"));
    await runAndWait(page, 2);
    await expect(page.getByTestId("got-further")).toHaveText(/Python got further: that slip is mended\./);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "compare-number-text");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("One fixed");
    // Help moves on with the student: step 2's rungs (the text "15"), not step 1's (the sign just mended).
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help")).toHaveAttribute("data-step", "mend-needed");
    await expect(page.getByTestId("help-rung-1")).toContainText("TypeError");
    await expect(page.getByTestId("help-rung-1")).not.toContainText("SyntaxError");

    // The same slip again is not progress.
    await runAndWait(page, 3);
    await expect(page.getByTestId("got-further")).toHaveCount(0);
    await expect(page.getByTestId("same-error")).toBeVisible();

    // Line 2 mended: the code runs, and the quiet slip is next.
    await setCode(page, starter.replace("roll => needed", "roll >= needed").replace('needed = "15"', "needed = 15"));
    await runAndWait(page, 4);
    await expect(page.getByTestId("got-further")).toBeVisible();
    await expect(page.getByTestId("explainer")).toHaveCount(0);
    await expect(page.getByTestId("checkpoint-message")).toBeVisible();
  });

  test("Unit 2's slips get their own words: randint without random., and no \"make it with def\" before Unit 3", async ({ page }) => {
    await open(page, "if-the-clock-turns-red", "roll-a-die", "Roll a die");
    await setCode(page, "import random\nstaff_roll = randint(1, 6)\nsword_roll = 0\nprint(staff_roll)\nprint(sword_roll)\n");
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "randint-needs-random");
    await expect(page.getByTestId("explainer-hint")).toContainText("staff_roll = random.randint(1, 6)");

    await setCode(page, "import random\nstaff_roll = roll_die(6)\nsword_roll = 0\nprint(staff_roll)\nprint(sword_roll)\n");
    await runAndWait(page, 2);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "unknown-function");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("def");
  });
});
