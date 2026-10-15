import { expect, test } from "@playwright/test";

test("a teacher sees a student after they join and advance", async ({ page }) => {
  const code = `GATE${Date.now()}`;
  await page.goto("/classroom");
  await page.getByLabel("Classroom name").fill("Period 2");
  await page.getByLabel("Report email").fill("teacher@example.com");
  await page.getByLabel("Join code").fill(code);
  await page.getByRole("button", { name: "Create classroom" }).click();
  await expect(page.getByTestId("created-code")).toHaveText(code);
  await expect(page.getByTestId("report-empty")).toBeVisible();

  await page.goto("/");
  await page.getByLabel("Display name").fill("Mira");
  await page.getByLabel("Join code").fill(code);
  await page.getByRole("button", { name: "Join class" }).click();
  await expect(page.getByTestId("join-status")).toContainText("Mira");
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("instructions")).toContainText("light_torch");

  await page.goto(`/classroom?code=${code}`);
  const row = page.getByTestId("report-row");
  await expect(row).toContainText("Mira");
  await expect(row).toContainText("gate");
  await expect(row).toContainText("courtyard");
  await expect(row).toContainText("In progress");
});
