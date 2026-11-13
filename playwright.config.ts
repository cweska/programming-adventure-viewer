import { defineConfig, devices } from "@playwright/test";

/** The course parity spec: one independent page per test, so it runs several at a time. */
const COURSE_PARITY = /intro-python-units\.spec\.ts$/;

export default defineConfig({
  testDir: "e2e",
  timeout: 180_000,
  expect: { timeout: 20_000 },
  fullyParallel: false,
  // The total. The "site" project keeps to one worker (its specs share the server's classroom and module
  // stores); the course parity project uses the rest.
  workers: 4,
  forbidOnly: true,
  retries: 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "retain-on-failure",
    ...devices["Desktop Chrome"],
    // Local runs on a machine whose preinstalled Chromium does not match this Playwright version can point
    // at it with PLAYWRIGHT_CHROMIUM_PATH. CI installs the matching browser and leaves this unset.
    launchOptions: process.env.PLAYWRIGHT_CHROMIUM_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_PATH } : {},
  },
  projects: [
    { name: "site", testIgnore: COURSE_PARITY, workers: 1 },
    // Every published unit's exercises, quizzes and Quick Check (only localStorage, no server state).
    { name: "course-parity", testMatch: COURSE_PARITY, fullyParallel: true, workers: 3 },
  ],
  webServer: {
    command: "npm run start",
    url: "http://127.0.0.1:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
