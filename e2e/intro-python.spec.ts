import { expect, test } from "@playwright/test";
import { buildParsons, checkpoint, expectSaved, itemUrl, openExercise, PROGRESS_KEY, runCode, SAMPLE } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const BARRIER_SOLUTION = 'caster = "Gearshift"\nmana = 20\nprint(caster + " has " + str(mana) + " mana.")\n';

test.describe("Intro to Python", () => {
  test("the site nav leads to the course map, and ?preview=1 lists the sample unit and its items", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("intro-python-callout")).toBeVisible();
    const navLink = page.getByRole("navigation", { name: "Site" }).getByRole("link", { name: "Intro to Python" });
    await expect(navLink).toBeVisible();
    await navLink.click();
    await expect(page.getByTestId("course-map")).toBeVisible();
    // The sample unit is unpublished: students never see it on the map.
    await expect(page.getByTestId(`unit-card-${SAMPLE}`)).toHaveCount(0);

    await page.goto("/intro-python?preview=1");
    await expect(page.getByTestId("preview-banner")).toBeVisible();
    await expect(page.getByTestId(`unit-card-${SAMPLE}`)).toBeVisible();
    await expect(page.getByTestId(`unit-status-${SAMPLE}`)).toContainText("Not started");

    await page.getByTestId(`unit-link-${SAMPLE}`).click();
    await expect(page.getByTestId("unit-page")).toBeVisible();
    await expect(page.getByTestId("unpublished-banner")).toBeVisible();
    await expect(page.getByTestId("quick-check-offer")).toBeVisible();
    for (const id of ["first-words", "chalk-quiz", "night-watch-sign", "mar-tu-speaks", "asking-the-traveler", "chalk-notes"]) {
      await expect(page.getByTestId(`item-row-${id}`)).toBeVisible();
    }
    // The Quick Check is offered up front, not listed with the lessons.
    await expect(page.getByTestId("item-row-quick-check")).toHaveCount(0);

    await page.getByTestId("item-link-first-words").click();
    await expect(page.getByTestId("lesson-player")).toBeVisible();
    await expect(page.getByTestId("exercise-label")).toHaveText("Exercise 1 of 3");
    await expect(page.getByTestId("course-breadcrumbs")).toContainText("Intro to Python");
  });

  test("a lesson exercise: the starter misses a step, Help climbs rung by rung, the solution passes and stays done", async ({ page }) => {
    await openExercise(page, "first-words", "barrier-report");
    await expect(page.getByTestId("exercise-label")).toHaveText("Exercise 3 of 3");
    await expect(checkpoint(page, 1)).toHaveAttribute("data-state", "active");
    // Full support: ONE Help control from the start, but no rung is shown until asked for.
    const help = page.getByTestId("help-button");
    await expect(help).toHaveCount(1);
    await expect(help).toContainText("Help: Start me off");
    await expect(page.getByTestId("help-rung-1")).toHaveCount(0);
    await expect(page.locator('[data-testid^="hint-button-"]')).toHaveCount(0);

    // The starter is only comments: step 1 fails with its friendly message (one message, nothing else).
    await page.getByTestId("run").click();
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("Can't find caster");
    await expect(page.getByTestId("checkpoint-message")).toHaveCount(1);
    await expect(page.getByTestId("stdout")).toHaveText("(Nothing was printed.)");
    await expect(checkpoint(page, 1)).toHaveAttribute("data-state", "active");

    // Help opens one rung per press, in order. Pressing again straight away asks to read it first;
    // a Run lets the next rung open.
    await help.click();
    await expect(page.getByTestId("help-rung-1")).toHaveAttribute("data-kind", "start");
    await expect(help).toContainText("More help: Where to look");
    await help.click();
    await expect(page.getByTestId("help-paced")).toBeVisible();
    await expect(page.getByTestId("help-rung-2")).toHaveCount(0);
    await runCode(page, "# thinking\n");
    await help.click();
    await expect(page.getByTestId("help-rung-2")).toHaveAttribute("data-kind", "point");
    await page.getByTestId("run").click();
    await expect(page.getByTestId("run")).toBeEnabled({ timeout: 30_000 });
    await help.click();
    await expect(page.getByTestId("help-rung-3")).toHaveAttribute("data-kind", "another");
    await expect(page.getByTestId("help-another-next")).toBeVisible();
    await expectSaved(page, `${SAMPLE}/first-words/barrier-report`, (entry) => {
      const hints = entry.hintsUsed as Record<string, number> | undefined;
      return hints?.["make-caster"] === 3;
    });

    // A crash is explained in plain words, with Python's own message folded away.
    await runCode(page, "caster = Gearshift\n");
    await expect(page.getByTestId("explainer")).toBeVisible();
    await expect(page.getByTestId("explainer-hint")).toContainText("quotes");
    await expect(page.getByTestId("traceback")).toBeHidden();

    // Two steps done, one still to go: the step list marks them, the console says only what is next.
    await runCode(page, 'caster = "Gearshift"\nmana = 20\n');
    await expect(page.getByTestId("checkpoint-pass-1")).toBeVisible();
    await expect(page.getByTestId("checkpoint-pass-2")).toBeVisible();
    await expect(page.getByTestId("checkpoint-message-3")).toContainText("Gearshift has 20 mana.");
    await expect(checkpoint(page, 3)).toHaveAttribute("data-state", "active");
    // Help moved on to step 3 and starts again at its first rung.
    await expect(page.getByTestId("help")).toHaveAttribute("data-step", "print-report");
    await expect(page.getByTestId("help-rung-1")).toHaveCount(0);

    await runCode(page, BARRIER_SOLUTION);
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("stdout")).toHaveText("Gearshift has 20 mana.");
    for (const n of [1, 2, 3]) await expect(checkpoint(page, n)).toHaveAttribute("data-state", "passed");
    await expect(page.getByTestId("exercise-player")).toHaveAttribute("data-done", "true");
    await expect(page.getByTestId("exercise-done")).toBeVisible();
    await expectSaved(page, `${SAMPLE}/first-words/barrier-report`, (entry) => entry.done === true);

    // Progress and code survive a reload.
    await page.reload();
    await expect(page.getByTestId("exercise-player")).toHaveAttribute("data-done", "true");
    await expect(checkpoint(page, 3)).toHaveAttribute("data-state", "passed");
    await expect(page.getByTestId("resumed")).toBeVisible();
    await expect(page.locator('[data-testid="editor"] .cm-content')).toContainText("mana = 20");
    await expect(page.getByTestId("exercise-dot-3")).toHaveAttribute("aria-label", /, done$/);

    // The unit page shows the lesson as started.
    await page.goto(`/intro-python/${SAMPLE}`);
    await expect(page.getByTestId("item-status-first-words")).toHaveAttribute("data-status", "in-progress");
  });

  test("an input() exercise reads its answers from the Input box", async ({ page }) => {
    await openExercise(page, "first-words", "ask-the-traveler");
    const box = page.getByTestId("stdin-box");
    await expect(box).toHaveValue("Lucky");

    await runCode(page, 'name = input("Who goes there? ")\nprint("Welcome to the cabin, " + name)\n');
    const stdout = page.getByTestId("stdout");
    await expect(stdout).toContainText("Who goes there? Lucky");
    await expect(stdout).toContainText("Welcome to the cabin, Lucky");
    await expect(page.getByTestId("all-passed")).toBeVisible();

    // A different answer runs too, but the steps are checked with Mar'tu's answers.
    await box.fill("Oogrish");
    await expect(page.getByTestId("stdin-note")).toBeVisible();
    await page.getByTestId("run").click();
    await expect(stdout).toContainText("Welcome to the cabin, Oogrish");
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("includes the name");
    await page.getByTestId("stdin-reset").click();
    await expect(box).toHaveValue("Lucky");
    await expect(page.getByTestId("stdin-note")).toHaveCount(0);

    // An empty box answers like pressing Enter: the program runs, it does not crash.
    await box.fill("");
    await page.getByTestId("run").click();
    await expect(stdout).toContainText("Welcome to the cabin,");
    await expect(page.getByTestId("explainer")).toHaveCount(0);
  });

  test("Compare with Mar'tu's version opens after real tries, side by side, and never overwrites the code", async ({ page }) => {
    await openExercise(page, "first-words", "barrier-report");
    // Untouched starter code is not a try: four Runs of it do not open Mar'tu's version.
    for (let run = 0; run < 4; run += 1) {
      await page.getByTestId("run").click();
      await expect(page.getByTestId("run")).toBeEnabled({ timeout: 30_000 });
    }
    await expect(page.getByTestId("compare-open")).toHaveCount(0);

    // Four changed tries do.
    for (const value of ["1", "2", "3", "4"]) await runCode(page, `cast = ${value}\n`);
    const open = page.getByTestId("compare-open");
    await expect(open).toBeVisible();
    await open.click();
    await expect(page.getByTestId("compare")).toBeVisible();
    await expect(page.getByTestId("compare-heading")).toBeFocused();
    await expect(page.getByTestId("compare-theirs")).toContainText('caster = "Gearshift"');
    await expect(page.getByTestId("compare-mine")).toContainText("cast = 4");
    await expect(page.locator('[data-testid="editor"] .cm-content')).toContainText("cast = 4");
    await expectSaved(page, `${SAMPLE}/first-words/barrier-report`, (entry) => entry.solutionShown === true);

    // "Now type it yourself" folds Mar'tu's version away and hands the keyboard to the editor.
    await page.getByTestId("compare-retype").click();
    await expect(page.getByTestId("compare-theirs")).toHaveCount(0);
    await expect(page.locator('[data-testid="editor"] .cm-content')).toBeFocused();
    await page.getByTestId("compare-look-again").click();
    await expect(page.getByTestId("compare-theirs")).toBeVisible();

    // Copying is an escape hatch behind a second confirm, starting on the safe choice.
    await page.getByTestId("compare-copy").click();
    await expect(page.getByTestId("compare-copy-no")).toBeFocused();
    await page.getByTestId("compare-copy-no").click();
    await expect(page.locator('[data-testid="editor"] .cm-content')).toContainText("cast = 4");
    await page.getByTestId("compare-copy").click();
    await page.getByTestId("compare-copy-yes").click();
    await expect(page.locator('[data-testid="editor"] .cm-content')).toContainText("mana = 20");
    await page.getByTestId("run").click();
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("write-it-myself")).toBeVisible();
  });

  test("the keyboard is never lost: Run keeps focus, and Esc then Tab leaves the editor", async ({ page }) => {
    await openExercise(page, "first-words", "barrier-report");
    await expect(page.getByTestId("editor-keys")).toContainText("Esc, then Tab");
    const run = page.getByTestId("run");
    await run.focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("checkpoint-message-1")).toBeVisible();
    await expect(run).toBeFocused();
    // The same result again is still announced (the live region's words change every run).
    await expect(page.getByTestId("run-count")).toContainText("Run 1");
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("run-count")).toContainText("Run 2");

    const content = page.locator('[data-testid="editor"] .cm-content');
    await content.click();
    await page.keyboard.press("Tab");
    await expect(content).toBeFocused();
    await page.keyboard.press("Escape");
    await page.keyboard.press("Tab");
    await expect(content).not.toBeFocused();
  });

  test("an engine challenge shows print_prompt() on the game screen", async ({ page }) => {
    await openExercise(page, "mar-tu-speaks");
    await runCode(page, 'line = "The decay is accelerating."\nprint_prompt(line)\nprint(line)\n');
    await expect(page.getByTestId("game-screen")).toContainText("The decay is accelerating.");
    await expect(page.getByTestId("all-passed")).toBeVisible();
  });

  test("a quiz with every question type can be answered and scored", async ({ page }) => {
    await page.goto(itemUrl("chalk-quiz"));
    await expect(page.getByTestId("quiz-count")).toHaveText("Question 1 of 6");
    const feedback = page.getByTestId("quiz-feedback");

    // mc
    await expect(page.getByTestId("quiz-question-store-mana")).toHaveAttribute("data-type", "mc");
    await page.getByTestId("quiz-choice-store-mana-1").click();
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();

    // mc with code, answered wrong on purpose
    await expect(page.getByTestId("quiz-question-q-2")).toBeVisible();
    await page.getByTestId("quiz-choice-q-2-1").click();
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "false");
    await page.getByTestId("quiz-next").click();

    // predict
    await expect(page.getByTestId("quiz-question-q-3")).toHaveAttribute("data-type", "predict");
    await page.getByTestId("quiz-choice-q-3-0").click();
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();

    // fill
    await expect(page.getByTestId("quiz-question-q-4")).toHaveAttribute("data-type", "fill");
    await page.getByTestId("quiz-fill-input").fill('" "');
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();

    // parsons
    await expect(page.getByTestId("quiz-question-q-5")).toHaveAttribute("data-type", "parsons");
    await buildParsons(page.getByTestId("quiz-q-5-0"), [
      'print("The clock turns red.")',
      'print("Everyone inside the barrier!")',
      'print("Shield up.")',
    ]);
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();

    // bug: run the fixed code, then check it
    await expect(page.getByTestId("quiz-question-q-6")).toHaveAttribute("data-type", "bug");
    await expect(page.getByTestId("quiz-bug-run")).toBeEnabled();
    await replaceEditor(page, 'print("Barrier is holding.")\n');
    await page.getByTestId("quiz-bug-run").click();
    await expect(page.getByTestId("quiz-bug-output")).toContainText("Barrier is holding.", { timeout: 120_000 });
    await page.getByTestId("quiz-check").click();
    await expect(feedback).toHaveAttribute("data-correct", "true");
    await page.getByTestId("quiz-next").click();

    await expect(page.getByTestId("quiz-results")).toBeVisible();
    await expect(page.getByTestId("quiz-score")).toHaveText("5 of 6 right (83%)");
    await expect(page.getByTestId("quiz-ready")).toBeVisible();
    await expect(page.getByTestId("quiz-review").locator("li")).toHaveCount(6);
    await expect
      .poll(() =>
        page.evaluate((key) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.quizzes?.["sample/chalk-quiz"]?.best ?? null, PROGRESS_KEY),
      )
      .toBe(83);

    await page.goto(`/intro-python/${SAMPLE}`);
    await expect(page.getByTestId("item-status-chalk-quiz")).toHaveAttribute("data-status", "done");
  });

  test("an article example runs with its input, the glossary opens, and the article can be marked read", async ({ page }) => {
    await page.goto(itemUrl("asking-the-traveler"));
    await expect(page.getByTestId("article-body")).toBeVisible();

    await page.getByTestId("article-example-run-1").click();
    const output = page.getByTestId("article-example-output-1");
    await expect(output).toContainText("Your name? Gearshift", { timeout: 120_000 });
    await expect(output).toContainText("Hello, Gearshift");

    const term = page.getByTestId("glossary-term").first();
    await term.click();
    await expect(page.getByTestId("glossary-popover")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("glossary-popover")).toHaveCount(0);
    await expect(term).toBeFocused();

    await page.getByTestId("mark-read").click();
    await expect(page.getByTestId("article-read")).toBeVisible();
  });

  test("passing the Quick Check marks the unit as tested out", async ({ page }) => {
    await page.goto(`/intro-python/${SAMPLE}`);
    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await pythonReady(page);
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 2");

    // No help in a Quick Check, even after a miss.
    await page.getByTestId("run").click();
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("Can't find leader");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    await expect(page.locator('[data-testid^="hint-button-"]')).toHaveCount(0);
    await expect(page.getByTestId("compare-open")).toHaveCount(0);

    await runCode(page, 'leader = "Oogrish"\nprint(leader)\n');
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await page.getByTestId("celebrate-next").click();
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 2 of 2");
    await pythonReady(page);
    await runCode(page, 'max_mana = 18\nprint(leader + " has " + str(max_mana) + " mana.")\n');
    await expect(page.getByTestId("all-passed")).toBeVisible();
    await expect(page.getByTestId("testout-result")).toBeVisible();
    await expect
      .poll(() => page.evaluate((key) => JSON.parse(window.localStorage.getItem(key) ?? "{}")?.testedOut?.sample ?? false, PROGRESS_KEY))
      .toBe(true);

    await page.goto(`/intro-python/${SAMPLE}`);
    await expect(page.getByTestId("quick-check-offer")).toContainText("You passed the Quick Check");
    await expect(page.getByTestId("item-status-first-words")).toHaveAttribute("data-status", "tested-out");
    await page.goto("/intro-python?preview=1");
    await expect(page.getByTestId(`unit-status-${SAMPLE}`)).toContainText("Tested out");
  });
});
