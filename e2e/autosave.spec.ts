import { expect, test, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";
import { openLeylinePart } from "./game";

const SAVE_KEY = "emberkeep-autosave:emberkeep";
const editor = (page: Page) => page.locator('[data-testid="editor"] .cm-content');

async function reachPartTwo(page: Page) {
  await pythonReady(page);
  await page.getByTestId("run").click();
  await expect(page.getByTestId("continue")).toBeVisible();
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");
}

async function createClassroom(page: Page): Promise<string> {
  const code = `SAVE${Date.now()}`;
  await page.goto("/classroom");
  await page.getByLabel("Classroom name").fill("Period 3");
  await page.getByLabel("Report email").fill("teacher@example.com");
  await page.getByLabel("Join code").fill(code);
  await page.getByRole("button", { name: "Create classroom" }).click();
  await expect(page.getByTestId("created-code")).toHaveText(code);
  return code;
}

async function joinClass(page: Page, name: string, code: string) {
  await page.getByLabel("Display name").fill(name);
  await page.getByLabel("Join code").fill(code);
  await page.getByRole("button", { name: "Join class" }).click();
  await expect(page.getByTestId("join-status")).toContainText(name);
}

test.describe("autosave", () => {
  test("brings a student back to the part and code they left, even code they never ran", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await expect(page.getByTestId("autosave-status")).toBeVisible();
    await expect(page.getByTestId("resumed")).toHaveCount(0);
    await reachPartTwo(page);
    await replaceEditor(page, 'print("draft")\n');

    // Close the page straight after typing: the save is written as the page goes away.
    await page.reload();
    await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");
    await expect(page.getByTestId("resumed")).toBeVisible();
    await expect(editor(page)).toContainText('print("draft")');
    await expect(page.getByTestId("autosave-status")).toHaveText("Progress saved on this computer.");

    await page.getByTestId("back").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("resumed")).toHaveCount(0);
    await expect(editor(page)).toContainText('print("ember")');
    await page.getByTestId("forward").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");
    await expect(editor(page)).toContainText('print("draft")');
    await expect(page.getByTestId("forward")).toBeDisabled();
  });

  test("keeps every part's code when the student went Back before leaving", async ({ page }) => {
    await page.goto("/play/emberkeep");
    await reachPartTwo(page);
    await replaceEditor(page, 'print("second")\n');
    await page.getByTestId("back").click();
    await replaceEditor(page, 'print("first")\n');
    await expect.poll(() => page.evaluate((key) => localStorage.getItem(key) ?? "", SAVE_KEY)).toContain("first");

    await page.reload();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(editor(page)).toContainText('print("first")');
    await expect(page.getByTestId("forward")).toBeEnabled();
    await page.getByTestId("forward").click();
    await expect(editor(page)).toContainText('print("second")');
  });

  test("remembers a board part the party already walked through", async ({ page }) => {
    await openLeylinePart(page, 5);
    await page.reload();
    await expect(page.getByTestId("part-label")).toHaveText("Part 5 of 8");
    await expect(page.getByTestId("resumed")).toBeVisible();

    await page.getByTestId("back").click();
    await expect(page.getByTestId("part-label")).toHaveText("Part 4 of 8");
    await expect(page.getByTestId("editor")).toContainText('party.move("down")');
    await expect(page.getByTestId("continue")).toBeVisible();
    await expect(page.getByTestId("forward")).toBeEnabled();
  });

  test("does not save a teacher's preview pass", async ({ page }) => {
    await page.goto("/play/emberkeep?preview=1");
    await expect(page.getByTestId("preview-banner")).toBeVisible();
    await expect(page.getByTestId("autosave-status")).toHaveCount(0);
    await reachPartTwo(page);
    await page.reload();
    await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 15");
    await expect(page.getByTestId("resumed")).toHaveCount(0);
    expect(await page.evaluate((key) => localStorage.getItem(key), SAVE_KEY)).toBeNull();
  });

  test("tells the class how far a student got before they joined", async ({ page }) => {
    const code = await createClassroom(page);
    await page.goto("/play/emberkeep");
    await reachPartTwo(page);

    const reported = page.waitForResponse((response) => response.url().endsWith("/api/progress"));
    await joinClass(page, "Tamsin", code);
    await reported;
    await expect(page.getByTestId("part-label")).toHaveText("Part 2 of 15");

    await page.goto(`/classroom?code=${code}`);
    const row = page.getByTestId("report-row");
    await expect(row).toContainText("Tamsin");
    await expect(row).toContainText("say-shut");
  });

  test("a joined student finds their unrun code on another computer", async ({ page, browser }) => {
    const code = await createClassroom(page);
    await page.goto("/play/emberkeep");
    await joinClass(page, "Oren", code);
    await reachPartTwo(page);
    const synced = page.waitForRequest(
      (request) => request.url().endsWith("/api/progress/code") && (request.postData() ?? "").includes("unrun"),
    );
    await replaceEditor(page, 'print("unrun")\n');
    await synced;

    const other = await browser.newContext();
    try {
      const second = await other.newPage();
      await second.goto("/play/emberkeep");
      await expect(second.getByTestId("part-label")).toHaveText("Part 1 of 15");
      await joinClass(second, "Oren", code);
      await expect(second.getByTestId("part-label")).toHaveText("Part 2 of 15");
      await expect(editor(second)).toContainText('print("unrun")');
      await expect(second.getByTestId("resumed")).toBeVisible();
    } finally {
      await other.close();
    }
  });
});
