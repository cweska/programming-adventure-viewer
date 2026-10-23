import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { createCatalog } from "./catalog";
import { makeValidModule } from "./fixtures";

const dirs: string[] = [];

afterEach(() => {
  for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

describe("lesson catalog", () => {
  it("saves a draft and publishes one lesson at a time", () => {
    const root = mkdtempSync(path.join(tmpdir(), "catalog-"));
    dirs.push(root);
    mkdirSync(path.join(root, "content", "modules", "sample"), { recursive: true });
    writeFileSync(
      path.join(root, "content", "modules", "sample", "module.json"),
      JSON.stringify(makeValidModule()),
    );
    const catalog = createCatalog(root);
    expect(catalog.forStudents().map((module) => module.lessons.map((lesson) => lesson.id))).toEqual([["gate"]]);

    const published = catalog.publishLesson("emberkeep", "hall");
    expect(published.lessons.find((lesson) => lesson.id === "hall")?.published).toBe(true);
    expect(catalog.forStudents()[0]?.lessons.map((lesson) => lesson.id)).toEqual(["gate", "hall"]);
  });
});
