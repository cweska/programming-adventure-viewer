/**
 * Unit 5 ("Dictionaries: Stat Sheets and Spell Books") in a real browser: what the teacher's ruling on the Unit 5
 * reviews asked of the site. The explainer's sheet rows (`=` inside a sheet, a key or a text value with no quotes, a
 * dot or round brackets where a sheet needs square ones, a name where a list needs a position, a KeyError's real
 * cause from the program's own sheets, the game's hidden `caster` included), full in a lesson and lean in the SOLO
 * and the Quick Check; lean Quick Check messages; the Quick Check's question gate (2 of 3); More structure on one
 * task of the project (only that task's lines are pieces); the one-click quotes sort; and Start me off landing where
 * its hint says.
 *
 * Every code below is one of the unit's own wrong answers (or a partial), read from the harness sidecar, so the
 * browser runs exactly what python3 proved. Browser parity for every exercise, quiz and Quick Check is in
 * intro-python-units.spec.ts.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";
import { PROGRESS_KEY } from "./course";
import { pythonReady, replaceEditor } from "./editor";

const UNIT_ID = "dictionaries";
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

/** Start with saved settings (and, optionally, exercises already passed). */
async function startWith(page: Page, settings: Record<string, unknown>, exercises: Record<string, unknown> = {}) {
  await page.goto("/intro-python");
  await page.evaluate(
    ([key, value]) => window.localStorage.setItem(key, value),
    [PROGRESS_KEY, JSON.stringify({ version: 1, exercises, quizzes: {}, read: {}, testedOut: {}, settings })] as const,
  );
}

test.describe("Intro to Python, Unit 5: Dictionaries", () => {
  test("the unit page offers the Quick Check, which needs its five tasks and 2 of its 3 questions", async ({ page }) => {
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId("unit-page")).toHaveAttribute("data-unit", UNIT_ID);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Dictionaries");
    await expect(page.getByTestId("item-row-stat-sheets")).not.toContainText("Optional");
    await expect(page.getByTestId("item-row-barrier-from-blank")).toContainText("Optional");
    await expect(page.getByTestId("quick-check-more")).toContainText("To pass, finish the tasks, then get 2 of the 3 Quick Check questions right.");

    await page.getByTestId("testout-start").click();
    await expect(page.getByTestId("testout-intro")).toBeVisible();
    await expect(page.getByTestId("testout-rule")).toHaveText(
      "No hints in a Quick Check. Pass all 5 tasks and get 2 of the 3 questions right, and the whole unit counts as done.",
    );
    await expect(page.getByTestId("exercise-label")).toHaveText("Task 1 of 5");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Quick Check 5");
  });

  test("a lesson gets the full sheet rows: a colon in a sheet, quotes on a key and on text, the key the sheet spells", async ({ page }) => {
    await open(page, "stat-sheets", "make-a-sheet");
    const equals = await runWrong(page, "stat-sheets/make-a-sheet", "= for : inside the sheet (the box habit)", 1);
    await expect(equals).toHaveAttribute("data-explainer", "full");
    await expect(equals).toHaveAttribute("data-kind", "equals-in-sheet");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText('Inside a dictionary { }, a colon goes between a key and its value: "name": "Gearshift",. The key keeps its quotes.');
    // Never the box advice that sent students the wrong way ("Take the quotes off name").
    await expect(hint).not.toContainText("Take the quotes off");
    await expect(page.getByTestId("python-last-line")).toContainText("cannot assign to literal");

    const value = await runWrong(page, "stat-sheets/make-a-sheet", "the name with no quotes (A-05/A-08 unquoted text)", 2);
    await expect(value).toHaveAttribute("data-kind", "unquoted-word");
    await expect(hint).toContainText('Gearshift has no quotes, so Python looks for a variable called that. Text in a sheet needs quotes: "name": "Gearshift",');
    await expect(hint).not.toContainText("Capital letters");

    const key = await runWrong(page, "stat-sheets/make-a-sheet", "a key with no quotes (G1 R6", 3);
    await expect(key).toHaveAttribute("data-kind", "unquoted-key");
    await expect(hint).toContainText('A key is text, so it needs quotes: "name". Without quotes, Python looks for a variable called name.');

    await open(page, "stat-sheets", "key-errors");
    const spelled = await runWrong(page, "stat-sheets/key-errors", "starter: capitals in the key", 1);
    await expect(spelled).toHaveAttribute("data-kind", "missing-key");
    await expect(hint).toContainText('The sheet spells it "max_mana". Keys match letter for letter.');
    await expect(page.getByTestId("python-last-line")).toContainText("KeyError: 'Max_Mana'");

    // `==` where one `=` stores a new key: a question, never "use a key that is already there".
    await open(page, "stat-sheets", "write-by-key");
    const asked = await runWrong(page, "stat-sheets/write-by-key", "== for = (reads a key that is not there yet)", 1);
    await expect(asked).toHaveAttribute("data-kind", "comparison-alone");
    await expect(hint).toContainText('One = stores it: gearshift["fuel"] = "starlode"');
    await expect(hint).not.toContainText("already there");
  });

  test("a KeyError names the level a key sits on, the game's hidden caster included; a list takes a position", async ({ page }) => {
    await open(page, "sheets-inside-sheets", "abilities-inside");
    await page.getByTestId("predict-skip").click();
    const skipped = await runWrong(page, "sheets-inside-sheets/abilities-inside", 'a skipped level: bomb_shell["wisdom"]', 1);
    await expect(skipped).toHaveAttribute("data-kind", "missing-key");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText('"wisdom" is inside "abilities": read the outer key first: bomb_shell["abilities"]["wisdom"]');

    // can-they-cast: `caster` comes from the game (the exercise's setup), not the student's code.
    await open(page, "sheets-inside-sheets", "can-they-cast");
    const cast = await runWrong(page, "sheets-inside-sheets/can-they-cast", 'a skipped level: caster["magical_affinity"]', 1);
    await expect(cast).toHaveAttribute("data-kind", "missing-key");
    await expect(hint).toContainText('"magical_affinity" is inside "abilities": read the outer key first: caster["abilities"]["magical_affinity"]');

    await open(page, "sheets-inside-sheets", "the-roster");
    const position = await runWrong(page, "sheets-inside-sheets/the-roster", 'a name as the position: roster["Lucky"]', 1);
    await expect(position).toHaveAttribute("data-kind", "name-as-position");
    await expect(hint).toContainText('roster is a list: it takes a position number in [ ], not a name. Lucky is at position 3: roster[3]["name"].');
    await expect(page.getByTestId("python-last-line")).toContainText("list indices must be integers or slices, not str");

    await open(page, "sheets-inside-sheets", "spell-book-of-spells");
    const stored = await runWrong(page, "sheets-inside-sheets/spell-book-of-spells", "CP2 round brackets", 1);
    await expect(stored).toHaveAttribute("data-kind", "list-needs-square-brackets");
    await expect(hint).toContainText("Store in a dictionary with square brackets: spell_book[spell_name] = spell");
    // Never Unit 3's "a recipe starts with def" or the == row.
    await expect(hint).not.toContainText("def");
    await expect(hint).not.toContainText("==");
  });

  test("lean in the SOLO and the Quick Check: the kind of slip and its line, never the fix", async ({ page }) => {
    await open(page, "stat-sheets", "solo-4a");
    const solo = await runWrong(page, "stat-sheets/solo-4a", "seat B's slip, dot access", 1);
    await expect(solo).toHaveAttribute("data-explainer", "lean");
    await expect(solo).toHaveAttribute("data-kind", "dot-on-a-sheet");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText("The slip is on line 9: a dot where a sheet needs square brackets.");
    await expect(hint).not.toContainText('oogrish["mana"]');
    await expect(page.getByTestId("python-last-line")).toContainText("'dict' object has no attribute 'mana'");

    await open(page, "qc4-a", "make-the-sheet");
    await expect(page.getByTestId("help-button")).toHaveCount(0);
    const equals = await runWrong(page, "qc4-a/make-the-sheet", "= for : inside the sheet (the box habit)", 1);
    await expect(equals).toHaveAttribute("data-explainer", "lean");
    await expect(equals).toHaveAttribute("data-kind", "equals-in-sheet");
    await expect(hint).toContainText("The slip is on line 4: an = inside a sheet.");
    await expect(hint).not.toContainText('"name": "Lucky"');
    // A check message in the Quick Check names the slip and the evidence, never the fix.
    await setCode(page, wrongAnswer("qc4-a/make-the-sheet", "values only, in curly brackets"));
    await runAndWait(page, 2);
    const message = page.getByTestId("checkpoint-message");
    await expect(message).toContainText("Your sheet has values but no keys.");
    await expect(message).not.toContainText("needs its key in front");

    await open(page, "qc4-a", "mend-the-read");
    await setCode(page, partial("qc4-a/mend-the-read", 1));
    await runAndWait(page, 1);
    // `False` left: the slip and the evidence; the evidence names the caster tried, never the read to write.
    await expect(page.getByTestId("checkpoint-message")).toContainText("is still there, so every caster gets the same answer.");
    await expect(page.getByTestId("checkpoint-message")).toContainText("a caster with 3 mana");
    await expect(page.getByTestId("checkpoint-message")).not.toContainText('caster["mana"]');
  });

  test("the same slip is full in a lesson and lean in the Quick Check (a key one level too deep, a whole card)", async ({ page }) => {
    await open(page, "qc4-a", "mend-the-read");
    await runWrong(page, "qc4-a/mend-the-read", "only the outer key: a whole card compared with <", 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "lean");
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "whole-card-compared");
    // The card was read on line 12 (`skill = caster["abilities"]`): the slip is there, not on the comparison Python stopped on.
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 12: a whole card read where one value is meant.");
    await expect(page.getByTestId("task-line")).toContainText("First, mend line 12. Python stopped on line 13, so it could not check your steps yet.");
    await expect(page.getByTestId("explainer-hint")).not.toContainText("magical_affinity");

    await open(page, "sheets-inside-sheets", "solo-4b");
    await runWrong(page, "sheets-inside-sheets/solo-4b", "both keys, inner first", 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "lean");
    await expect(page.getByTestId("explainer-hint")).toContainText("The slip is on line 8: the keys the other way round.");

    await open(page, "sheets-inside-sheets", "abilities-inside");
    await page.getByTestId("predict-skip").click();
    await runWrong(page, "sheets-inside-sheets/abilities-inside", "both keys in one bracket", 1);
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-explainer", "full");
    await expect(page.getByTestId("explainer")).toHaveAttribute("data-kind", "comma-in-brackets");
    await expect(page.getByTestId("explainer-hint")).toContainText('One key per pair of brackets: bomb_shell["abilities"]["wisdom"]');
  });

  test("the play-through's slips: = on a later key, the spell's own reads, <= caught on its own step, the card in Keep it short", async ({ page }) => {
    // `=` on line 3 (Python 3.13 says "':' expected" there): still a colon in a sheet, never a colon put before the `=`.
    await open(page, "stat-sheets", "make-a-sheet");
    const later = await runWrong(page, "stat-sheets/make-a-sheet", "= for : on a later line of the sheet", 1);
    await expect(later).toHaveAttribute("data-kind", "equals-in-sheet");
    const hint = page.getByTestId("explainer-hint");
    await expect(hint).toContainText('Line 3 has = inside a sheet. Inside a dictionary { }, a colon goes between a key and its value: "magical_affinity": 10,');
    await expect(hint).not.toContainText(": =");
    const quote = await runWrong(page, "stat-sheets/make-a-sheet", "the key's closing quote left off", 2);
    await expect(quote).toHaveAttribute("data-kind", "missing-quote");
    await expect(hint).toContainText('A key keeps both quotes, and the closing quote goes before the colon: "name": "Gearshift",');

    // can-they-cast: `spell` holds the Lantern Ward page, so the mended line keeps `spell["mana_cost"]` as it is.
    await open(page, "sheets-inside-sheets", "can-they-cast");
    const dot = await runWrong(page, "sheets-inside-sheets/can-they-cast", "dot access in the mana test", 1);
    await expect(dot).toHaveAttribute("data-kind", "dot-on-a-sheet");
    await expect(hint).toContainText('elif caster["mana"] < spell["mana_cost"]:');
    await expect(hint).not.toContainText("Lantern Ward");
    // `<=` in the affinity test stops step 1, and Help aims at step 1, whose Teach rung says `<`, not `<=`.
    await setCode(page, wrongAnswer("sheets-inside-sheets/can-they-cast", "<= in the affinity test"));
    await runAndWait(page, 2);
    await expect(page.getByTestId("checkpoint-message-1")).toContainText("Exactly enough affinity still casts");
    await expect(page.getByTestId("checkpoint-pass-1")).toHaveCount(0);
    await expect(page.getByTestId("help-button")).toHaveAttribute("aria-label", /for step 1/i);

    // The Quick Check's first task, under Keep it short: the story line, and the card it introduces.
    await startWith(page, { preset: "short" });
    await open(page, "qc4-a", "make-the-sheet");
    const bubble = page.getByTestId("exercise-player").getByTestId("martu-says").first();
    await expect(page.getByTestId("show-explanation")).toBeVisible();
    await expect(bubble).toContainText("Mar'tu's notes so far");
    await expect(bubble).toContainText(/magical_affinity\s+13/);

    // The article's `.get()` glossary link shows as code, never as [[ | ]] marks.
    await open(page, "keys-and-get");
    await expect(page.getByTestId("article")).not.toContainText("[[");
    await expect(page.getByTestId("article-try")).not.toContainText("[[");
  });

  test("More structure on a project task builds that task alone, with the rest of the ledger in place", async ({ page }) => {
    await startWith(page, { preset: "short" });
    await open(page, "martus-ledger-of-heroes");
    // Task 1 done (Mar'tu's partial 1), so Help is on task 2: write max_mana_for.
    await setCode(page, partial("martus-ledger-of-heroes", 1));
    await runAndWait(page, 1);
    await expect(page.getByTestId("checkpoint-pass-1")).toBeVisible();
    await page.getByTestId("help-more-options").locator("summary").click();
    await page.getByTestId("help-extra-structure").getByTestId("assemble-open").click();
    const board = page.getByTestId("assemble-board");
    await expect(board).toBeVisible();
    await expect(page.getByTestId("assemble-step-note")).toContainText("Build task 2 from pieces. The rest of Mar’tu’s program stays where it is.");
    await expect(page.getByTestId("assemble-context")).toContainText("# 2. Write max_mana_for(affinity).");
    await expect(page.getByTestId("assemble-gap")).toHaveCount(2);
    // Only task 2's two lines are pieces, never the 50-line program.
    const pieces = board.locator('[data-testid^="assemble-piece-"]');
    await expect(pieces).toHaveCount(2);
    await pieces.filter({ hasText: "def max_mana_for(affinity):" }).click();
    await pieces.filter({ hasText: "return affinity * 2" }).click();
    await page.getByTestId("assemble-insert").click();
    const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
    await expect(lines.filter({ hasText: 'gearshift = {' })).toHaveCount(1);
    await runAndWait(page, 2);
    await expect(page.getByTestId("checkpoint-pass-2")).toBeVisible();
    await expect(page.getByTestId("checkpoint-3")).toHaveAttribute("data-state", "active");
  });

  test("the quotes sort is one click a card: Check my sort marks each card, then shows the answers", async ({ page }) => {
    await open(page, "stat-sheets", "key-from-a-box");
    // The sort is the angle "The quotes sort" in the Learn pane's Another way.
    const another = page.getByTestId("another-way");
    for (let at = 0; at < 6; at += 1) {
      if ((await page.getByTestId("another-way-text").count()) > 0 && (await page.getByTestId("card-sort").count()) > 0) break;
      await another.click();
    }
    const sort = page.getByTestId("card-sort");
    await expect(sort).toBeVisible();
    await expect(page.getByTestId("card-sort-check")).toBeDisabled();
    // Cards: mana = 26 (box), {"mana": 26} (letters), hero["mana"] (letters), hero[mana] (box), print("mana"), print(mana).
    const picks = [1, 0, 0, 1, 0, 0];
    for (const [card, group] of picks.entries()) await page.getByTestId(`card-sort-pick-${card}-${group}`).click();
    await expect(page.getByTestId("card-sort-pick-0-1")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("card-sort-check").click();
    await expect(page.getByTestId("card-sort-result")).toContainText("5 of 6 right.");
    await expect(page.getByTestId("card-sort-mark-5")).toHaveAttribute("data-right", "false");
    await expect(page.getByTestId("card-sort-mark-0")).toHaveAttribute("data-right", "true");
    await expect(page.getByTestId("card-sort-explain")).toContainText("Cards 2, 3 and 5 have quotes, so they mean these exact letters.");
    await page.getByTestId("card-sort-pick-5-1").click();
    await page.getByTestId("card-sort-check").click();
    await expect(page.getByTestId("card-sort-result")).toContainText("6 of 6 right.");
  });

  test("Start me off lands where its hint says: in place of the line to change, and under the note the task names", async ({ page }) => {
    await open(page, "stat-sheets", "read-by-key");
    await page.getByTestId("predict-skip").click();
    await runAndWait(page, 1);
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-rung-1")).toHaveAttribute("data-kind", "start");
    await expect(page.getByTestId("help-start-code")).toHaveText("print(gearshift[");
    await page.getByTestId("help-start-insert").click();
    const lines = page.locator('[data-testid="exercise-player"] [data-testid="editor"] .cm-line');
    // "in place of `print("Gearshift: 20 mana")`": that line becomes the start, and the typed line is gone.
    await expect(lines.nth(8)).toHaveText("print(gearshift[");
    await expect(lines.filter({ hasText: 'print("Gearshift: 20 mana")' })).toHaveCount(0);
    await expect(lines.nth(5)).toHaveText('print(gearshift["mana"])');

    // which-number-is-which: the code already starts the line (`print(lucky[2])`), so Help opens at Where to look.
    await open(page, "stat-sheets", "which-number-is-which");
    await page.getByTestId("predict-skip").click();
    await runAndWait(page, 1);
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-rung-1")).toHaveAttribute("data-kind", "point");
    await expect(page.getByTestId("help-start-code")).toHaveCount(0);

    // write-by-key: "under `# 1.`", above the print that shows the new mana.
    await open(page, "stat-sheets", "write-by-key");
    await runAndWait(page, 1);
    await page.getByTestId("help-button").click();
    await expect(page.getByTestId("help-start-code")).toHaveText('gearshift["mana"] =');
    await page.getByTestId("help-start-insert").click();
    await expect(lines.nth(6)).toHaveText("# 1. Gearshift casts Fire Bolt:");
    await expect(lines.nth(7)).toHaveText('gearshift["mana"] = ');
    await expect(lines.nth(9)).toHaveText('print(gearshift["mana"])');
  });

  test("a Quick Check form needs 2 of its 3 questions: 1 right does not pass, 2 right does", async ({ page }) => {
    const form = unit.items.find((item) => item.id === "qc4-a");
    const quiz = unit.items.find((item) => item.id === "qc4-a-questions");
    expect(form?.questionsToPass).toBe(2);
    expect(quiz?.questions).toHaveLength(3);
    // The five tasks are marked passed in the saved progress (the parity spec plays them for real), so only the
    // questions are left.
    const exercises = Object.fromEntries(
      (form?.exercises ?? []).map((exercise) => [
        `${UNIT_ID}/qc4-a/${exercise.id}`,
        { passed: exercise.checkpoints.map((cp) => cp.id), done: true, hintsUsed: {}, failedRuns: 0 },
      ]),
    );
    await startWith(page, { preset: "more" }, exercises);
    await page.goto(`/intro-python/${UNIT_ID}/qc4-a`);
    await expect(page.getByTestId("testout-questions")).toContainText("Get 2 of the 3 right");
    await expect(page.getByTestId("testout-result")).toHaveCount(0);

    const answer = async (rightCount: number) => {
      for (const [at, question] of (quiz?.questions ?? []).entries()) {
        await expect(page.getByTestId("quiz-count")).toHaveText(`Question ${at + 1} of 3`);
        const right = typeof question.answer === "number" ? question.answer : (question.choices ?? []).indexOf(String(question.answer));
        const choice = at < rightCount ? right : right === 0 ? 1 : 0;
        await page.getByTestId(`quiz-choice-${question.id}-${choice}`).click();
        await page.getByTestId("quiz-check").click();
        await expect(page.getByTestId("quiz-feedback")).toHaveAttribute("data-correct", at < rightCount ? "true" : "false");
        await page.getByTestId("quiz-next").click();
      }
    };
    await page.goto(`/intro-python/${UNIT_ID}/qc4-a-questions`);
    await answer(1);
    await expect(page.getByTestId("quiz-score")).toHaveText("1 of 3 right (33%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "false");
    await expect(page.getByTestId("quiz-quick-check")).toContainText("The Quick Check needs 2 of these 3 right.");

    await page.getByTestId("quiz-retake").click();
    await answer(2);
    await expect(page.getByTestId("quiz-score")).toHaveText("2 of 3 right (67%)");
    await expect(page.getByTestId("quiz-quick-check")).toHaveAttribute("data-passed", "true");
    await page.goto(`/intro-python/${UNIT_ID}`);
    await expect(page.getByTestId(`unit-status-${UNIT_ID}`)).toContainText("Tested out");
  });
});
