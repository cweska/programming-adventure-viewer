import { expect, test, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";
import {
  MOVEMENT_SOLUTION,
  OPTIONS_SOLUTION,
  REPLIES,
  TO_THE_DOOR,
  boardSnapshot,
  expectAt,
  focusBoard,
  openLeylinePart,
  openPracticePart,
  position,
  press,
  promptSolution,
  type BoardActor,
} from "./game";

const STEPS: [string, number, number][] = [
  ["ArrowRight", 1, 0],
  ["ArrowDown", 0, 1],
  ["ArrowLeft", -1, 0],
  ["ArrowUp", 0, -1],
  ["d", 1, 0],
  ["s", 0, 1],
  ["a", -1, 0],
  ["w", 0, -1],
];

test.describe("module picker", () => {
  test("lists the campaign module and the warm-up, but not the practice yard", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("module-card-leylines-awaken")).toContainText("Module 1");
    await expect(page.getByTestId("module-card-leylines-awaken")).toContainText("Leylines Awaken");
    await expect(page.getByTestId("module-card-emberkeep")).toBeVisible();
    await expect(page.getByTestId("module-card-training-grounds")).toHaveCount(0);
    await page.getByTestId("begin-leylines-awaken").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 8");
    await expect(page.getByTestId("caption")).toContainText("This night was a peaceful one.");
  });

  test("keeps the practice yard out of student view unless a teacher previews it", async ({ page }) => {
    await page.goto("/play/training-grounds");
    await expect(page.getByText("This module has no published lesson yet.")).toBeVisible();
    await page.goto("/classroom");
    await page.getByTestId("open-practice-yard").click();
    await expect(page.getByTestId("preview-banner")).toBeVisible();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 3");
  });
});

test.describe("Leylines Awaken", () => {
  test.use({ reducedMotion: "reduce" });

  test("tells the story with the editor hidden", async ({ page }) => {
    await page.goto("/play/leylines-awaken");
    const captions = [
      "This night was a peaceful one.",
      "His medallion started humming again.",
      "as they heard Mar'tu calling in their thick accent",
    ];
    for (const [index, caption] of captions.entries()) {
      await expect(page.getByTestId("part-label")).toHaveText(`Part ${index + 1} of 8`);
      await expect(page.getByTestId("caption")).toContainText(caption);
      await expect(page.getByTestId("editor")).toHaveCount(0);
      await expect(page.getByTestId("run")).toHaveCount(0);
      await page.getByTestId("continue").click();
    }
    await expect(page.getByTestId("part-label")).toHaveText("Part 4 of 8");
    await expect(page.getByTestId("editor")).toBeVisible();
    await expect(page.getByTestId("board")).toBeVisible();
  });

  test("programs movement, walks Oogrish's party into the cabin, and closes the door", async ({ page }) => {
    await openLeylinePart(page, 4);
    await expect(page.getByTestId("editor")).toContainText("def move_left():");
    await expect(page.getByTestId("party-member-oogrish")).toHaveAttribute("data-active", "true");
    await expectAt(page, "oogrish", 3, 5);
    await focusBoard(page);
    await press(page, "ArrowRight");
    await expect(page.getByTestId("game-notice")).toContainText("can't move yet");
    await expect(page.getByTestId("game-notice")).toContainText("Finish the code below and press Run.");
    await expectAt(page, "oogrish", 3, 5);

    await pythonReady(page);
    await replaceEditor(page, MOVEMENT_SOLUTION.replace('party.move("right")', 'party.move("left")'));
    await page.getByTestId("run").click();
    await expect(page.getByTestId("failed-check").first()).toContainText('move_right() should call party.move("right").');

    await replaceEditor(page, MOVEMENT_SOLUTION);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("feedback")).toContainText("Click the map and walk to the cabin door.");
    await expectAt(page, "oogrish", 3, 5);
    await expectAt(page, "gearshift", 3, 4);
    await expect(page.getByTestId("continue")).toHaveCount(0);

    await focusBoard(page);
    await press(page, ...TO_THE_DOOR);
    await expectAt(page, "oogrish", 11, 3);
    for (const id of ["oogrish", "gearshift", "mar-tu"]) {
      await expect(page.getByTestId(`actor-${id}`)).toHaveAttribute("data-hidden", "true");
    }
    await expect(page.getByTestId("door-closed")).toBeVisible();
    await expect(page.getByTestId("game")).toHaveAttribute("data-mode", "cutscene");
    await expect(page.getByTestId("goal-met")).toHaveText("You made it to the cabin door!");
    await press(page, "ArrowDown");
    await expectAt(page, "oogrish", 11, 3);
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("Mar'tu cannot talk until talking is programmed", async ({ page }) => {
    await openLeylinePart(page, 4);
    await pythonReady(page);
    await replaceEditor(page, MOVEMENT_SOLUTION);
    await page.getByTestId("run").click();
    await expectAt(page, "gearshift", 3, 4);
    await focusBoard(page);
    await press(page, ...Array<string>(8).fill("ArrowRight"), "ArrowUp", "ArrowRight");
    await expectAt(page, "oogrish", 11, 4);
    await expect(page.getByTestId("game-notice")).toHaveText("Talking hasn't been programmed yet.");
    await expect(page.getByTestId("dialogue-box")).toHaveCount(0);
  });

  test("shows Mar'tu's prompt in the dialogue box without wrapping long lines", async ({ page }) => {
    await openLeylinePart(page, 5);
    await expect(page.getByTestId("caption")).toContainText("It seems like the decay is accelerating.");
    await expect(page.getByTestId("editor")).toHaveCount(0);
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 6 of 8");

    await expect(page.getByTestId("conversation-speaker")).toHaveText("Mar'tu");
    await expect(page.getByTestId("conversation-prompt")).toHaveText("");
    await expect(page.getByTestId("conversation-option-1")).toHaveCount(0);

    await pythonReady(page);
    const direct = promptSolution("WILL YOU HELP US?").replace(
      "    dialogue = get_dialogue_prompt_string()\n    print_prompt(dialogue)",
      "    print_prompt(get_dialogue_prompt_string())",
    );
    await replaceEditor(page, direct);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("failed-check").first()).toContainText("in a variable first");

    const long =
      "WHAT DO YOU TWO REMEMBER ABOUT THE GREENROOM, AND WHY DOES THE MEDALLION HUM WHENEVER A FLASHOVER ROLLS IN?";
    await replaceEditor(page, promptSolution(long));
    await page.getByTestId("run").click();
    await expect(page.getByTestId("feedback")).toHaveText("Dialogue prompt implemented, well done!");
    await expect(page.getByTestId("conversation-prompt")).toHaveText(
      "What do you two remember about the greenroom, and why does the medallion hum whenever a flashover rolls in?",
    );
    const overflow = await page.evaluate(() => {
      const prompt = document.querySelector('[data-testid="conversation-prompt"]');
      const box = document.querySelector('[data-testid="conversation-box"]');
      if (!prompt || !box) return null;
      const range = document.createRange();
      range.selectNodeContents(prompt);
      const text = range.getBoundingClientRect();
      return {
        wrap: getComputedStyle(prompt).whiteSpace,
        oneLine: text.height < 2 * parseFloat(getComputedStyle(prompt).lineHeight),
        pastTheBox: text.right > box.getBoundingClientRect().right,
      };
    });
    expect(overflow).toEqual({ wrap: "nowrap", oneLine: true, pastTheBox: true });
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("builds the dialogue options with if and elif and highlights the clicked one", async ({ page }) => {
    await openLeylinePart(page, 7);
    await expect(page.getByTestId("conversation-prompt")).toHaveText("Will you help us?");
    await expect(page.getByTestId("editor")).toContainText("(user.clicked() == <option>):");
    for (const number of [1, 2, 3, 4]) {
      await expect(page.getByTestId(`conversation-option-${number}`)).toHaveText(String(number));
    }
    await page.getByTestId("conversation-option-1").click();
    await expect(page.getByTestId("conversation-notice")).toContainText("hasn't been programmed yet");

    await pythonReady(page);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("explainer")).toContainText("Syntax error");
    await expect(page.getByTestId("continue")).toHaveCount(0);

    await replaceEditor(page, OPTIONS_SOLUTION);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("feedback")).toHaveText("Dialogue fully implemented, well done!");
    for (const [index, reply] of REPLIES.entries()) {
      await expect(page.getByTestId(`conversation-option-${index + 1}`)).toContainText(reply);
    }
    await expect(page.getByTestId("conversation-option-4")).toHaveAttribute("data-selected", "true");
    await expect(page.getByTestId("conversation-reply")).toHaveText("Master Oogrish: We need to rest first.");

    await page.getByTestId("conversation-option-2").click();
    await expect(page.getByTestId("conversation-option-2")).toHaveAttribute("data-selected", "true");
    await expect(page.getByTestId("conversation-option-4")).toHaveAttribute("data-selected", "false");
    await expect(page.getByTestId("conversation-reply")).toHaveText("Master Oogrish: What is the decay?");
    await expect(page.getByTestId("conversation-notice")).toHaveCount(0);

    await page.getByTestId("continue").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 8 of 8");
    await expect(page.getByTestId("caption")).toHaveText(
      'Mar\'tu took a long exaggerated sigh and looked out the window. "We need help."',
    );
    await expect(page.getByTestId("editor")).toHaveCount(0);
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("lesson-complete")).toBeVisible();
  });
});

test.describe("practice yard", () => {
  test("moves exactly one tile per arrow key or WASD press, in every direction", async ({ page }) => {
    await openPracticePart(page, 1);
    await focusBoard(page);
    await expectAt(page, "gearshift", 2, 4);
    for (const [key, dx, dy] of STEPS) {
      const before = await position(page, "gearshift");
      await press(page, key);
      await expectAt(page, "gearshift", before.x + dx, before.y + dy);
    }
  });

  test("stops at the fence, trails the follower, and switches the leader with Tab", async ({ page }) => {
    await openPracticePart(page, 1);
    await focusBoard(page);
    await press(page, "ArrowUp", "ArrowUp", "ArrowUp", "ArrowUp", "ArrowUp");
    await expectAt(page, "gearshift", 2, 1);
    await expectAt(page, "oogrish", 2, 2);

    await press(page, "Tab");
    await expect(page.getByTestId("party-member-oogrish")).toHaveAttribute("data-active", "true");
    await expect(page.getByTestId("party-member-gearshift")).toHaveAttribute("data-active", "false");
    await press(page, "ArrowDown");
    await expectAt(page, "oogrish", 2, 3);
    await expectAt(page, "gearshift", 2, 2);

    await page.keyboard.press("Escape");
    await expect(page.getByTestId("focus-hint")).toBeVisible();
    await page.keyboard.press("ArrowDown");
    await expectAt(page, "oogrish", 2, 3);
  });

  test("talks with the Arena Keeper by clicking and by number keys", async ({ page }) => {
    await openPracticePart(page, 2);
    await focusBoard(page);
    await press(page, ...Array<string>(7).fill("ArrowRight"));
    await expectAt(page, "gearshift", 9, 4);
    await expect(page.getByTestId("dialogue-box")).toHaveCount(0);
    await press(page, "ArrowRight");
    await expectAt(page, "gearshift", 9, 4);
    await expect(page.getByTestId("dialogue-speaker")).toHaveText("Arena Keeper");
    await expect(page.getByTestId("dialogue-text")).toContainText("Welcome to the practice yard!");

    await page.getByTestId("dialogue-option-1").click();
    await expect(page.getByTestId("dialogue-text")).toContainText("Walk into someone to talk with them.");
    await page.keyboard.press("ArrowLeft");
    await expectAt(page, "gearshift", 9, 4);

    await press(page, "2");
    await expect(page.getByTestId("dialogue-text")).toContainText("Good luck out there.");
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await press(page, "Enter");
    await expect(page.getByTestId("dialogue-box")).toHaveCount(0);
    await expect(page.getByTestId("goal-met")).toHaveText("You finished talking with Arena Keeper.");
    await expect(page.getByTestId("continue")).toBeVisible();
  });
});

test.describe("melee combat", () => {
  test.use({ reducedMotion: "reduce" });

  function stepToward(me: BoardActor, actors: BoardActor[]): string[] {
    const enemies = actors.filter((actor) => actor.kind === "enemy" && !actor.down);
    const target = enemies.reduce((best, enemy) =>
      Math.abs(enemy.x - me.x) + Math.abs(enemy.y - me.y) < Math.abs(best.x - me.x) + Math.abs(best.y - me.y)
        ? enemy
        : best,
    );
    const horizontal = target.x > me.x ? "ArrowRight" : "ArrowLeft";
    const vertical = target.y > me.y ? "ArrowDown" : "ArrowUp";
    const keys: string[] = [];
    if (target.x !== me.x) keys.push(horizontal);
    if (target.y !== me.y) keys.push(vertical);
    return Math.abs(target.x - me.x) >= Math.abs(target.y - me.y) ? keys : keys.reverse();
  }

  async function fight(page: Page): Promise<string> {
    let seen = "";
    for (let round = 0; round < 300; round += 1) {
      const board = await boardSnapshot(page);
      seen += `\n${board.log}`;
      if (board.result) return seen;
      if (board.mode === "explore") {
        await press(page, "ArrowRight");
        continue;
      }
      if (board.mode !== "combat" || board.activeKind !== "hero" || !board.active) {
        await page.waitForTimeout(40);
        continue;
      }
      const me = board.actors.find((actor) => actor.id === board.active);
      if (!me) throw new Error("the active hero should be on the board");
      let acted = false;
      for (const key of stepToward(me, board.actors)) {
        await press(page, key);
        const after = await boardSnapshot(page);
        const moved = after.actors.find((actor) => actor.id === me.id);
        if (after.active !== me.id || moved?.x !== me.x || moved?.y !== me.y || after.log !== board.log) {
          acted = true;
          break;
        }
      }
      if (!acted) await press(page, " ");
    }
    throw new Error("the sparring match did not finish");
  }

  test("starts a turn-based fight, rolls attacks, runs enemy turns, and ends in victory", async ({ page }) => {
    await openPracticePart(page, 3);
    await focusBoard(page);
    await expect(page.getByTestId("turn-indicator")).toHaveCount(0);
    await press(page, ...Array<string>(6).fill("ArrowRight"));
    await expect(page.getByTestId("game")).toHaveAttribute("data-mode", "explore");
    await press(page, "ArrowRight");
    await expect(page.getByTestId("game")).toHaveAttribute("data-mode", "combat");
    await expect(page.getByTestId("combat-log")).toContainText("Turn order:");

    const seen = await fight(page);
    expect(seen).toContain("jabs with its piston arm");
    expect(seen).toMatch(/(swings his longsword|strikes with the Staff of Wisdom): rolls \d+ \+ \d+ = \d+ vs Defense 11\./);
    expect(seen).toContain("powers down.");
    await expect(page.getByTestId("combat-result")).toHaveText("Victory!");
    await expect(page.getByTestId("goal-met")).toHaveText("Every enemy is down.");
    await expect(page.getByTestId("actor-bot-1")).toHaveAttribute("data-down", "true");
    await expect(page.getByTestId("actor-bot-2")).toHaveAttribute("data-down", "true");
    await expect(page.getByTestId("continue")).toBeVisible();
  });
});
