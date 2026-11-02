import { expect, test } from "@playwright/test";
import {
  CAST_SOLUTION,
  MANA_SOLUTION,
  SPELL_SOLUTION,
  bar,
  openFriendsPart,
  skillSolution,
  solveFriends,
} from "./friends";
import { focusBoard, press } from "./game";

test.describe("Friends In Low Places", () => {
  test.use({ reducedMotion: "reduce" });

  test("comes after Module 1 in the picker and tells its story with the editor hidden", async ({ page }) => {
    await page.goto("/");
    const cards = page.locator('[data-testid^="module-card-"]');
    await expect(cards.nth(0)).toHaveAttribute("data-testid", "module-card-leylines-awaken");
    await expect(cards.nth(1)).toHaveAttribute("data-testid", "module-card-friends-in-low-places");
    await expect(page.getByTestId("module-card-friends-in-low-places")).toContainText("Module 2");
    await page.getByTestId("begin-friends-in-low-places").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 16");
    await expect(page.getByTestId("caption")).toHaveText(
      "A knocking from underneath their feet jarred Mar'tu and the others.",
    );
    await expect(page.getByTestId("editor")).toHaveCount(0);
    await expect(page.getByTestId("continue")).toBeVisible();
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("caption")).toContainText("Looks like the latch is sticking again.");
    await expect(page.getByTestId("editor")).toHaveCount(0);
  });

  test("locks the skill checks until they pass, then a good roll opens the trap door", async ({ page }) => {
    await openFriendsPart(page, 3);
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await page.getByTestId("skill-option-strength").click();
    await expect(page.getByTestId("skill-notice")).toContainText("Skill checks haven't been programmed yet.");

    await solveFriends(page, skillSolution(5), "Your skill checks work.");
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await page.getByTestId("skill-option-strength").click();
    await expect(page.getByTestId("skill-result")).toHaveText("Rolled 20, needed 12. Success!");
    await expect(page.getByTestId("skill-helper")).toHaveCount(0);
    await expect(page.getByTestId("skill-success")).toHaveText("Door opened!");
    await expect(page.locator('[data-testid="skill-check"] img')).toHaveAttribute("src", /fil-trapdoor-open\.svg$/);
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("lets Mar'tu open the trap door after a failed roll", async ({ page }) => {
    await openFriendsPart(page, 3);
    await solveFriends(page, skillSolution(2), "Your skill checks work.");
    await page.getByTestId("skill-option-dexterity").click();
    await expect(page.getByTestId("skill-success")).toHaveText("Door opened!");
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("shows the failed roll and Mar'tu's line before the door opens", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await openFriendsPart(page, 3);
    await solveFriends(page, skillSolution(2), "Your skill checks work.");
    await page.getByTestId("skill-option-intelligence").click();
    await expect(page.getByTestId("skill-result")).toHaveText("Rolled 2, needed 9. Not this time.");
    await expect(page.getByTestId("skill-helper")).toContainText("Oh just let me do it.");
    await expect(page.getByTestId("skill-success")).toHaveText("Door opened!");
  });

  test("inks the spell book and draws every mana bar with the student's code", async ({ page }) => {
    await openFriendsPart(page, 13);
    await expect(page.getByTestId("spell-book")).toHaveAttribute("data-inked", "false");
    await solveFriends(page, SPELL_SOLUTION, "Spell book ready, well done!");
    await expect(page.getByTestId("spell-book")).toHaveAttribute("data-inked", "true");
    await expect(page.getByTestId("spell-book-ink")).toContainText("Strengthen Magic");
    await expect(page.getByTestId("spell-book-ink")).toContainText("Mana cost: 10");
    await expect(page.getByTestId("spell-book-ink")).toContainText("Required affinity: 8");
    await expect(page.getByTestId("spell-book-success")).toHaveText("Spell book ready, well done!");
    await page.getByTestId("continue").click();

    await expect(page.getByTestId("mana-text-oogrish")).toHaveText("Mana bar not drawn yet");
    await solveFriends(page, MANA_SOLUTION, "Mana bars working, well done!");
    await expect(page.getByTestId("mana-text-oogrish")).toHaveText(bar(18, 18));
    await expect(page.getByTestId("mana-text-gearshift")).toHaveText(bar(15, 20));
    await expect(page.getByTestId("mana-text-bomb-shell")).toHaveText(bar(14, 24));
    await expect(page.getByTestId("mana-text-lucky")).toHaveText(bar(19, 26));
    await expect(page.getByTestId("party-success")).toHaveText("Mana bars working, well done!");
  });

  test("casts with the student's cast_spell until the barrier holds", async ({ page }) => {
    await openFriendsPart(page, 15);
    await expect(page.getByTestId("game")).toHaveAttribute("data-barrier-level", "0");
    await focusBoard(page);
    await press(page, "1");
    await expect(page.getByTestId("game-notice")).toContainText("Casting hasn't been programmed yet.");
    await expect(page.getByTestId("mana-oogrish")).toHaveText("Mana 18/18");

    await solveFriends(page, CAST_SOLUTION, "Casting works!");
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await focusBoard(page);
    await press(page, "ArrowLeft");
    await expect(page.getByTestId("game-notice")).toContainText("The party stays inside the barrier.");
    await press(page, "1");
    await expect(page.getByTestId("mana-oogrish")).toHaveText("Mana 8/18");
    await expect(page.getByTestId("mana-drop")).toHaveText("-10 mana");
    await expect(page.getByTestId("speech-bubble")).toHaveText("Steady, now.");
    await expect(page.getByTestId("game")).toHaveAttribute("data-barrier-level", "1");

    await page.getByTestId("cast-gearshift").click();
    await expect(page.getByTestId("mana-gearshift")).toHaveText("Mana 5/20");
    await expect(page.getByTestId("speech-bubble")).toHaveText("Barrier's holding.");
    await page.getByTestId("cast-gearshift").click();
    await expect(page.getByTestId("cast-prompt")).toHaveText(
      "Gearshift doesn't have enough mana to cast Strengthen Magic.",
    );
    await expect(page.getByTestId("mana-gearshift")).toHaveText("Mana 5/20");
    await expect(page.getByTestId("game")).toHaveAttribute("data-barrier-level", "2");

    await page.getByTestId("actor-bomb-shell").click();
    await expect(page.getByTestId("speech-bubble")).toHaveText("Shield up.");
    await page.getByTestId("cast-lucky").click();
    await expect(page.getByTestId("speech-bubble")).toHaveText("Fine. But I'm keeping track.");
    await expect(page.getByTestId("mana-lucky")).toHaveText("Mana 9/26");
    await expect(page.getByTestId("game")).toHaveAttribute("data-barrier-locked", "true");
    await expect(page.getByTestId("goal-met")).toHaveText("The barrier held!");
    await expect(page.getByTestId("game")).toHaveAttribute("data-barrier-done", "true");
    await expect(page.locator('[data-testid="barrier-firefly"][data-out="true"]').first()).toBeAttached();
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("finishes the module after the barrier holds", async ({ page }) => {
    await openFriendsPart(page, 16);
    await expect(page.getByTestId("caption")).toContainText('"Thirty-two hours," he said.');
    await expect(page.getByTestId("editor")).toHaveCount(0);
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("lesson-complete")).toBeVisible();
  });
});
