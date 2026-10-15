import { expect, type Page } from "@playwright/test";

export async function replaceEditor(page: Page, code: string) {
  const content = page.locator('[data-testid="editor"] .cm-content');
  await content.click();
  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.press("Backspace");
  await page.keyboard.insertText(code);
  await expect(content).toContainText(code.split("\n")[0] ?? code);
}

export async function pythonReady(page: Page) {
  await expect(page.getByTestId("run")).toBeEnabled({ timeout: 120_000 });
}
