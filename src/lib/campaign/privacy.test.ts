import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { characterSchema } from "../game/schema";
import { campaignData } from "./registry";

const TEXT_FILES = /\.(json|svg|md|txt)$/;
const SHEET_LABELS = [/creator\s*\/\s*student/i, /student\s*name\s*:/i, /\bcreator\s*:/i];

function walk(dir: string): string[] {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).flatMap((entry) => {
    const full = path.join(dir, entry);
    if (statSync(full).isDirectory()) return walk(full);
    return TEXT_FILES.test(entry) ? [full] : [];
  });
}

describe("student privacy", () => {
  it("has no place to store who made a character", () => {
    const sample = structuredClone(Object.values(campaignData.characters)[0]);
    expect(characterSchema.safeParse({ ...sample, creator: "Someone" }).success).toBe(false);
    expect(characterSchema.safeParse({ ...sample, student: "Someone" }).success).toBe(false);
  });

  it("keeps character-sheet name lines out of everything the site and repo ship", () => {
    const files = [...walk("content"), ...walk("public/scenes"), ...walk("public/sprites"), ...walk("docs")];
    expect(files.length).toBeGreaterThan(0);
    for (const file of files) {
      const text = readFileSync(file, "utf8");
      for (const label of SHEET_LABELS) {
        expect(label.test(text), `${file} contains ${label}`).toBe(false);
      }
    }
  });

  it("never commits the original character sheets", () => {
    const ignore = readFileSync(".gitignore", "utf8");
    expect(ignore).toMatch(/^\*\.docx$/m);
    expect(ignore).toMatch(/^character-sheets\/$/m);
  });
});
