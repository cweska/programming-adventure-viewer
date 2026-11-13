import { expect, type Locator, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

/** The sample unit (scripts/course/sample/u00_sample.py): unpublished, so the map lists it only with ?preview=1. */
export const SAMPLE = "sample";
export const PROGRESS_KEY = "intro-python:v1";

export const itemUrl = (itemId: string, exerciseId?: string) =>
  `/intro-python/${SAMPLE}/${itemId}${exerciseId ? `#${exerciseId}` : ""}`;

/** Open an exercise in the sample lesson and wait until Python can run. */
export async function openExercise(page: Page, itemId: string, exerciseId?: string) {
  await page.goto(itemUrl(itemId, exerciseId));
  await expect(page.getByTestId("exercise-player")).toBeVisible();
  await pythonReady(page);
}

/** Type code into the exercise editor and press Run. */
export async function runCode(page: Page, code: string) {
  await replaceEditor(page, code);
  await page.getByTestId("run").click();
  await expect(page.getByTestId("run")).toBeEnabled({ timeout: 30_000 });
}

export function checkpoint(page: Page, n: number): Locator {
  return page.getByTestId(`checkpoint-${n}`);
}

/** Wait until the saved progress for `key` satisfies `predicate` (writes reach storage after ~300 ms). */
export async function expectSaved(page: Page, key: string, predicate: (entry: Record<string, unknown>) => boolean) {
  await expect
    .poll(async () => {
      const raw = await page.evaluate((storageKey) => window.localStorage.getItem(storageKey), PROGRESS_KEY);
      if (!raw) return false;
      const entry = (JSON.parse(raw) as { exercises?: Record<string, Record<string, unknown>> }).exercises?.[key];
      return entry ? predicate(entry) : false;
    })
    .toBe(true);
}

/** Click the parsons pieces whose code is exactly each of `lines`, in order. */
export async function buildParsons(board: Locator, lines: string[]) {
  for (const line of lines) {
    await board
      .locator("button.parsons-piece")
      .filter({ has: board.page().getByText(line, { exact: true }) })
      .click();
  }
}
