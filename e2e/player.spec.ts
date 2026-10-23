import { expect, test } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

test.describe("emberkeep player", () => {
  test("shows the theater, torches, caption, instructions, editor, and console", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await expect(page.getByTestId("theater-frame")).toBeVisible();
    await expect(page.getByTestId("torch-left")).toBeVisible();
    await expect(page.getByTestId("torch-right")).toBeVisible();
    await expect(page.getByTestId("caption")).toContainText("Rain peppers on the muddy road");
    await expect(page.getByTestId("instructions")).toContainText("Press Run");
    await expect(page.getByTestId("editor")).toBeVisible();
    await expect(page.locator(".cm-lineNumbers")).toBeVisible();
    await expect(page.getByTestId("console")).toBeVisible();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("editor")).toContainText('print("ember")');
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await expect(page.getByTestId("format")).toHaveCount(0);
    await expect(page.getByRole("button", { name: "Format" })).toHaveCount(0);
    await expect(page.getByTestId("back")).toBeVisible();
    await expect(page.getByTestId("forward")).toBeVisible();

    const duration = await page.evaluate(() => {
      for (const sheet of Array.from(document.styleSheets)) {
        let rules: CSSRuleList;
        try {
          rules = sheet.cssRules;
        } catch {
          continue;
        }
        for (const rule of Array.from(rules)) {
          if (rule instanceof CSSStyleRule && rule.selectorText === ".flame") {
            return rule.style.animationDuration;
          }
        }
      }
      return "";
    });
    expect(Number.parseFloat(duration)).toBeGreaterThanOrEqual(2);

    const computed = await page
      .getByTestId("torch-left")
      .locator(".flame")
      .evaluate((element) => getComputedStyle(element).animationDuration);
    if (computed !== "0s" && computed !== "none") {
      expect(Number.parseFloat(computed)).toBeGreaterThanOrEqual(2);
    }
  });

  test("explains broken Python in plain language", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await pythonReady(page);
    await replaceEditor(page, "print(");
    await page.getByTestId("run").click();
    const explainer = page.getByTestId("explainer");
    await expect(explainer).toBeVisible();
    await expect(explainer).toContainText("Syntax error");
    await expect(page.getByTestId("explainer-hint")).toContainText("parenthesis");
    await expect(page.getByTestId("traceback")).toBeHidden();
  });

  test("Run on the prefilled print shows the word in the console", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("editor")).toContainText('print("ember")');
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await pythonReady(page);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("stdout")).toContainText("ember");
    await expect(page.getByTestId("stdout")).not.toContainText("Program output will appear here.");
    await expect(page.getByTestId("feedback")).toContainText("The wall hears ember and answers through the old magic");
    const divider = page.getByTestId("console-divider");
    await expect(divider).toBeVisible();
    const between = await page.evaluate(() => {
      const stdout = document.querySelector('[data-testid="stdout"]');
      const line = document.querySelector('[data-testid="console-divider"]');
      const story = document.querySelector('[data-testid="feedback"]');
      if (!stdout || !line || !story) return false;
      const stdoutBox = stdout.getBoundingClientRect();
      const lineBox = line.getBoundingClientRect();
      const storyBox = story.getBoundingClientRect();
      return stdoutBox.bottom <= lineBox.top && lineBox.bottom <= storyBox.top && lineBox.height > 0;
    });
    expect(between).toBe(true);
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("formats on blur and not on each keystroke", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await replaceEditor(page, "value=1\n");
    const editor = page.locator('[data-testid="editor"] .cm-content');
    await expect(editor).toContainText("value=1");
    await expect(editor).not.toContainText("value = 1");
    await page.getByTestId("instructions").click();
    await expect(editor).toContainText("value = 1");
  });

  test("Back restores the previous part and Forward stops at the furthest unlocked part", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("back")).toBeDisabled();
    await expect(page.getByTestId("forward")).toBeDisabled();

    await pythonReady(page);
    await page.getByTestId("run").click();
    await expect(page.getByTestId("stdout")).toContainText("ember");
    await expect(page.getByTestId("continue")).toBeVisible();
    await expect(page.getByTestId("forward")).toBeEnabled();

    await page.getByTestId("forward").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");
    await expect(page.getByTestId("instructions")).toContainText('print("The gate is shut.")');
    await expect(page.getByTestId("forward")).toBeDisabled();

    await replaceEditor(page, 'print("draft")\n');
    await page.getByTestId("back").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("editor")).toContainText('print("ember")');

    await page.getByTestId("forward").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");
    await expect(page.getByTestId("editor")).toContainText('print("draft")');
    await expect(page.getByTestId("forward")).toBeDisabled();
    await expect(page.getByTestId("back")).toBeEnabled();
  });
});
