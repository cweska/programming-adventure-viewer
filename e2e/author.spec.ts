import { expect, test } from "@playwright/test";

test("author page shows a validation error without calling a model", async ({ page }) => {
  let authorCalls = 0;
  await page.route("**/api/author", async (route) => {
    authorCalls += 1;
    await route.abort();
  });

  await page.goto("/author");
  await expect(page.getByRole("heading", { name: "Author a lesson" })).toBeVisible();
  const prompt = "A locked gate, a torch challenge, and a gatekeeper who must be answered.";
  await page.getByLabel("Lesson prompt").fill(prompt);
  await page.getByLabel("Model output").fill("{not json");
  await page.getByRole("button", { name: "Check draft" }).click();
  await expect(page.getByTestId("validation-error")).toContainText("not valid JSON");
  await expect(page.getByLabel("Lesson prompt")).toHaveValue(prompt);
  expect(authorCalls).toBe(0);
});
