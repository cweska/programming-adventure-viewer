import { expect, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

export type BoardActor = { id: string; kind: string; x: number; y: number; down: boolean };

export type BoardSnapshot = {
  mode: string;
  tick: number;
  active: string | null;
  activeKind: string | null;
  actors: BoardActor[];
  log: string;
  result: string | null;
};

export const MOVEMENT_SOLUTION = [
  "def move_left():",
  '    party.move("left")',
  "",
  "",
  "def move_right():",
  '    party.move("right")',
  "",
  "",
  "def move_up():",
  '    party.move("up")',
  "",
  "",
  "def move_down():",
  '    party.move("down")',
  "",
].join("\n");

export async function expectAt(page: Page, id: string, x: number, y: number) {
  const actor = page.getByTestId(`actor-${id}`);
  await expect(actor).toHaveAttribute("data-x", String(x));
  await expect(actor).toHaveAttribute("data-y", String(y));
}

export async function position(page: Page, id: string): Promise<{ x: number; y: number }> {
  const actor = page.getByTestId(`actor-${id}`);
  return {
    x: Number(await actor.getAttribute("data-x")),
    y: Number(await actor.getAttribute("data-y")),
  };
}

export async function focusBoard(page: Page) {
  await page.getByTestId("board").focus();
  await expect(page.getByTestId("focus-hint")).toHaveCount(0);
}

export async function press(page: Page, ...keys: string[]) {
  for (const key of keys) {
    const before = await page.getByTestId("game").getAttribute("data-tick");
    await page.keyboard.press(key);
    await expect
      .poll(async () => page.getByTestId("game").getAttribute("data-tick"), { timeout: 1_000 })
      .not.toBe(before)
      .catch(() => undefined);
  }
}

export async function boardSnapshot(page: Page): Promise<BoardSnapshot> {
  return page.evaluate(() => {
    const game = document.querySelector('[data-testid="game"]');
    const turn = document.querySelector('[data-testid="turn-indicator"]');
    const actors = Array.from(document.querySelectorAll('[data-testid^="actor-"]')).map((element) => ({
      id: (element.getAttribute("data-testid") ?? "").slice("actor-".length),
      kind: element.getAttribute("data-kind") ?? "",
      x: Number(element.getAttribute("data-x")),
      y: Number(element.getAttribute("data-y")),
      down: element.getAttribute("data-down") === "true",
    }));
    return {
      mode: game?.getAttribute("data-mode") ?? "",
      tick: Number(game?.getAttribute("data-tick") ?? 0),
      active: turn?.getAttribute("data-active") ?? null,
      activeKind: turn?.getAttribute("data-kind") ?? null,
      actors,
      log: document.querySelector('[data-testid="combat-log"]')?.textContent ?? "",
      result: document.querySelector('[data-testid="combat-result"]')?.textContent ?? null,
    };
  });
}

export async function openLeylinePart(page: Page, part: 4 | 5) {
  await page.goto("/play/leylines-awaken");
  await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 5");
  for (let count = 0; count < 3; count += 1) await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 4 of 5");
  if (part === 4) return;
  await pythonReady(page);
  await replaceEditor(page, MOVEMENT_SOLUTION);
  await page.getByTestId("run").click();
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 5 of 5");
}

export async function openPracticePart(page: Page, part: 1 | 2 | 3) {
  await page.goto("/play/training-grounds?preview=1");
  await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 3");
  if (part === 1) return;
  await focusBoard(page);
  await press(page, ...Array<string>(10).fill("ArrowRight"));
  await expect(page.getByTestId("goal-met")).toBeVisible();
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 3");
  if (part === 2) return;
  await focusBoard(page);
  await press(page, ...Array<string>(8).fill("ArrowRight"), "3", "Enter");
  await expect(page.getByTestId("goal-met")).toBeVisible();
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 3 of 3");
}
