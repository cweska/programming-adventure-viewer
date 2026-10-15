import { expect, test } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

test.describe("emberkeep player", () => {
  test("shows the theater, torches, caption, instructions, editor, and console", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("theater-frame")).toBeVisible();
    await expect(page.getByTestId("torch-left")).toBeVisible();
    await expect(page.getByTestId("torch-right")).toBeVisible();
    await expect(page.getByTestId("caption")).toContainText("Emberkeep");
    await expect(page.getByTestId("instructions")).toContainText("outer gate");
    await expect(page.getByTestId("editor")).toBeVisible();
    await expect(page.locator(".cm-lineNumbers")).toBeVisible();
    await expect(page.getByTestId("console")).toBeVisible();

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
    await page.goto("/");
    await pythonReady(page);
    await replaceEditor(page, "print(");
    await page.getByTestId("run").click();
    const explainer = page.getByTestId("explainer");
    await expect(explainer).toBeVisible();
    await expect(explainer).toContainText("Syntax error");
    await expect(page.getByTestId("explainer-hint")).toContainText("parenthesis");
    await expect(page.getByTestId("traceback")).toBeHidden();
  });

  test("a correct light_torch solution reveals Continue", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("continue")).toBeVisible();
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("instructions")).toContainText("light_torch");
    await expect(page.getByTestId("continue")).toHaveCount(0);
    await pythonReady(page);
    await replaceEditor(
      page,
      ["def light_torch(oil):", "    if oil:", '        return "lit"', '    return "dark"', ""].join("\n"),
    );
    await page.getByTestId("run").click();
    await expect(page.getByTestId("feedback")).toContainText("The torches catch");
    await expect(page.getByTestId("continue")).toBeVisible();
  });

  test("stage.say changes the theater caption", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("continue").click();
    await pythonReady(page);
    await replaceEditor(
      page,
      ["def light_torch(oil):", "    if oil:", '        return "lit"', '    return "dark"', ""].join("\n"),
    );
    await page.getByTestId("run").click();
    await expect(page.getByTestId("continue")).toBeVisible();
    await page.getByTestId("continue").click();
    await expect(page.getByTestId("instructions")).toContainText("stage.say");
    await replaceEditor(page, 'stage.say("The gate knows my name.")\n');
    await page.getByTestId("run").click();
    await expect(page.getByTestId("caption")).toHaveText("The gate knows my name.");
  });
});
