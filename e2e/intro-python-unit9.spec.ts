/**
 * Unit 9 ("Strings: Runes and Ribbons") in a real browser: what the teacher's ruling on Unit 9 asked of the site. The
 * explainer's strings rows (site request 1), each in the student's own names with one fix: text changed in place, a list
 * asked to join itself, a method with no `()` (the crash banner names the line that stored it), a list used like text,
 * `.append()` on text, a comma where a slice takes a colon, a curly brace with no partner in an f-string, a quote mark
 * inside text with no backslash, `.Upper()`; a text's own letters and positions in the IndexError (site request 2); the
 * same slip full in a lesson and lean in the SOLO and the Quick Check; a lean Quick Check check message; and the Quick
 * Check's question gate (4 of 5). Unit 9's Quick Check is an ordinary one (no required test-out), so the unit page and the
 * Quick Check behave as in Units 3-7, never as the Readiness Check.
 *
 * Every code below is one of the unit's own wrong answers, read from the harness sidecar, so the browser runs exactly
 * what python3 proved. Browser parity for every exercise, quiz and Quick Check (Unit 9's included: it reads every
 * published unit) is in intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "strings";
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

test.describe("Intro to Python, Unit 9: Strings", () => {
  test("the unit is on the map after Functions II, and its page offers an ordinary Quick Check: three tasks and 4 of 5 questions", async ({ page }) => {
    expect(unit.published).toBe(true);
    expect(unit.order).toBe(9);
    // An ordinary Quick Check: no required test-out, so this is never a Readiness Check.
    expect(unit.items.filter((item) => item.kind === "testout").every((item) => item.optional !== false)).toBe(true);
    await page.goto("/intro-python");
    await expect(page.getByTestId(`unit-card-${UNIT_ID}`)).toBeVisible();
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Strings");
    await expect(page.getByTestId("item-row-strings-are-rows-of-letters")).not.toContainText("Optional");
    await expect(page.getByTestId("item-row-words-that-change-shape")).not.toContainText("Optional");
    await expect(page.getByTestId("item-row-words-quiz")).not.toContainText("Optional");
    // The projects and the challenge never block anyone.
    await expect(page.getByTestId("item-row-the-water-stained-log")).toContainText("Optional");
    await expect(page.getByTestId("item-row-tag-from-blank")).toContainText("Optional");
    await expect(page.getByTestId("readiness-result")).toHaveCount(0);
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get 4 of the 5 Quick Check questions right.");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 3 tasks and get 4 of the 5 questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 3");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Quick Check 9");
  });

  test("Lesson 8A's slips: text changed in place, .append() on text, a comma in a slice, a quote mark inside text, a text's own positions", async ({ page }) => {
    const hint = page.getByTestId("explainer-hint");

    await open(page, "strings-are-rows-of-letters", "letters-cant-change");
    // The starter itself changes one letter in place.
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "text-changed-in-place");
    await expect(hint).toContainText("Line 4 tries to change one letter of word, but text can't change one letter. Build a new one and put it back: word = \"G\" + word[1:]");
    await expect(hint).not.toContainText("mixes kinds");

    await open(page, "strings-are-rows-of-letters", "letters-have-places");
    const comma = await runWrong(page, "strings-are-rows-of-letters/letters-have-places", "a comma for the colon (TypeError)", 1);
    await expect(comma).toHaveAttribute("data-kind", "comma-in-brackets");
    await expect(hint).toContainText("Inside [ ], a slice takes a colon: word = sign[0:9]. A comma asks for two positions at once.");
    const append = await runWrong(page, "strings-are-rows-of-letters/letters-have-places", "a list method on text: initials.append(name[0])", 2);
    await expect(append).toHaveAttribute("data-kind", "append-on-text");
    await expect(hint).toContainText("initials holds text, and text has no .append(). Glue it on with +: initials = initials + name[0]");

    await open(page, "strings-are-rows-of-letters", "escape-marks");
    const quote = await runWrong(page, "strings-are-rows-of-letters/escape-marks", "inner quotes with no backslash (SyntaxError)", 1);
    await expect(quote).toHaveAttribute("data-kind", "quote-inside-text");
    await expect(hint).toContainText('Put a backslash in front of each " inside: print("Mar\'tu: \\"NOT a compass.\\"")');
    // Never Python's "Perhaps you forgot a comma?" as the help: the box says the guess is wrong.
    await expect(hint).toContainText("Python's last line guesses a comma, but that guess is wrong here.");
    await expect(hint).not.toContainText("Put a comma");
    // One backslash put in and one missed (Mar'tu's own text invites it), with line 8's `print("")` still there: a quote
    // mark inside the text, never "Enter inside text" with the notes and line 8 glued onto line 3.
    const missed = await runWrong(page, "strings-are-rows-of-letters/escape-marks", "one backslash missed: a bare quote mark left inside (SyntaxError)", 2);
    await expect(missed).toHaveAttribute("data-kind", "quote-inside-text");
    await expect(hint).toContainText('Line 3 has a " inside the text with no backslash in front, so it ends the text early.');
    await expect(hint).not.toContainText("Enter");

    // Site request 2: a text's own letters and positions (the strings lessons' word), never "3 items".
    await open(page, "extra-letter-by-letter", "broken-spell-8a");
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "nothing-at-position");
    await expect(hint).toContainText("Line 2 asks tag for position 5, but tag has 5 letters, at positions 0 to 4. Positions start at 0, like a ruler. Write: last = tag[-1]");
    await expect(hint).not.toContainText("items");
  });

  test("Lesson 8B's slips: a method with no () (the banner names the line that stored it), a list asked to join, an f-string brace, .Upper()", async ({ page }) => {
    const hint = page.getByTestId("explainer-hint");
    const task = page.getByTestId("task-line");

    // The Broken spell's first bug: `note = note.lower` on line 3, and Python stops on line 4.
    await open(page, "words-that-change-shape", "broken-spell-8b");
    await runAndWait(page, 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "method-without-brackets");
    await expect(hint).toContainText("Line 3 wrote .lower with no (), so the method never ran: note holds the method itself, not text. Python runs a method only with (). Add () on line 3: note = note.lower()");
    await expect(hint).not.toContainText("builtin_function_or_method");
    await expect(task).toContainText("line 3");
    // Bug 1 fixed: the join the wrong way round, with the line's own glue and list.
    const join = await runWrong(page, "words-that-change-shape/broken-spell-8b", "bug 1 mended, the join still the wrong way round", 2);
    await expect(join).toHaveAttribute("data-kind", "join-on-list");
    await expect(hint).toContainText('Line 9 asks the list words to join itself, but a list can\'t join. Ask the glue instead: print(" ".join(words))');

    await open(page, "words-that-change-shape", "f-strings");
    const brace = await runWrong(page, "words-that-change-shape/f-strings", "a closing brace missing (SyntaxError)", 1);
    await expect(brace).toHaveAttribute("data-kind", "f-string-brace");
    await expect(hint).toContainText('Each { in an f-string needs its }: line = f"{name}: {mana}"');
    await expect(hint).not.toContainText("missing parenthesis");

    await open(page, "words-that-change-shape", "loud-and-quiet");
    const capital = await runWrong(page, "words-that-change-shape/loud-and-quiet", "a capital U (AttributeError)", 1);
    await expect(capital).toHaveAttribute("data-kind", "method-capital");
    await expect(hint).toContainText("Method names are all small letters: line = line.upper()");

    // A method used like a function, nested: the text first, then each method in order (never "write it with def").
    await open(page, "words-that-change-shape", "chain-the-spells");
    const nested = await runWrong(page, "words-that-change-shape/chain-the-spells", "lower(raw) as if it were a function (NameError)", 1);
    await expect(nested).toHaveAttribute("data-kind", "method-as-function");
    await expect(hint).toContainText("Write: return raw.lower().capitalize()");
    await expect(hint).not.toContainText("def");
    // Mar'tu's two steps copied as they are, the calls kept: the student's own Run stops on `said`, a name from his
    // example; the box names `raw`, never "hand it over as a parameter".
    const copied = await runWrong(page, "words-that-change-shape/chain-the-spells", "Mar'tu's two steps copied, the calls kept", 2);
    await expect(copied).toHaveAttribute("data-kind", "variable-in-function");
    await expect(hint).toContainText("said comes from Mar'tu's example, and tidy_line's parameter is raw. Write raw where it says said: raw = raw.lower()");
    await expect(hint).not.toContainText("Hand it over");
  });

  test("the same slip is full in a lesson and lean in the SOLO and the Quick Check: the slip and its line, never the fix", async ({ page }) => {
    const hint = page.getByTestId("explainer-hint");
    // A lesson: the join the wrong way round, with the fixed line.
    await open(page, "words-that-change-shape", "split-the-clipped");
    const full = await runWrong(page, "words-that-change-shape/split-the-clipped", "join called the wrong way round (AttributeError)", 1);
    await expect(full).toHaveAttribute("data-explainer", "full");
    await expect(full).toHaveAttribute("data-kind", "join-on-list");
    await expect(hint).toContainText('joined = " ".join(words)');

    // The SOLO: the same slip, lean.
    await open(page, "words-that-change-shape", "solo-8b");
    await expect(page.getByTestId("solo")).toBeVisible();
    const solo = await runWrong(page, "words-that-change-shape/solo-8b", "seat B's slip shape: join called the wrong way round (AttributeError)", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "join-on-list");
    await expect(hint).toContainText("Line 3 asks a list, words, to .join(). Python's last line, below, says what it found.");
    await expect(hint).not.toContainText('" ".join(words)');

    // The Quick Check: lean, no Help.
    await open(page, "qc8-a", "clip-the-log");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const qc = await runWrong(page, "qc8-a/clip-the-log", "join called the wrong way round, on the slice (spec: crash)", 1);
    await expect(qc).toHaveAttribute("data-explainer", "lean");
    await expect(hint).toContainText("Line 9 asks a list, words[:3], to .join().");
    await expect(hint).not.toContainText('" ".join(words[:3])');

    // A Quick Check check message names the slip and the evidence, never the fix (C2 step 2: the slice kept as a list).
    await setCode(page, wrongAnswer("qc8-a/clip-the-log", "the slice kept as a list"));
    await runAndWait(page, 2);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText("holds a list, not text");
    await expect(message).not.toContainText(".join(words");
  });

  test("a Quick Check form needs 4 of its 5 questions: 3 right does not pass, 4 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc8-a");
    const quiz = unit.items.find((item) => item.id === "qc8-a-questions");
    expect(form?.questionsToPass).toBe(4);
    expect(form?.exercises).toHaveLength(3);
    expect(quiz?.questions).toHaveLength(5);
    // The three tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc8-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await startWith(page, { preset: "more" }, exercises);
    await page.goto(`/intro-python/${UNIT_ID}/qc8-a`);
    await expect(page.getByTestId("testout-questions")).toContainText("Get 4 of the 5 right");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);

    const answer = async (rightCount: number) => {
      for (const [at, question] of (quiz?.questions ?? []).entries()) {
        await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of 5`);
        const right = typeof question.answer === "number" ? question.answer : (question.choices ?? []).indexOf(String(question.answer));
        expect(right, `${question.id}: the keyed answer is a choice`).toBeGreaterThanOrEqual(0);
        const choice = at < rightCount ? right : right === 0 ? 1 : 0;
        await page.getByTestId(`quiz-choice-${question.id}-${choice}`).click();
        await page.getByTestId("quiz-check").click();
        await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", at < rightCount ? "true" : "false");
        await page.getByTestId("quiz-next").click();
      }
    };
    await page.goto(`/intro-python/${UNIT_ID}/qc8-a-questions`);
    await answer(3);
    await expect(page.getByTestId("quiz-score")).toHaveText("3 of 5 right (60%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "false");
    await expect(page.getByTestId("quiz-quick-check")).toContainText("The Quick Check needs 4 of these 5 right.");

    await page.getByTestId("quiz-retake").click();
    await answer(4);
    await expect(page.getByTestId("quiz-score")).toHaveText("4 of 5 right (80%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "true");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
  });
});
