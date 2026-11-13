import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import {
  allUnits,
  courseMeta,
  findItem,
  findUnit,
  glossary,
  glossaryFor,
  glossaryForTexts,
  glossaryForUnit,
  itemHref,
  itemPageProps,
  nextHref,
  parseUnits,
  publishedUnits,
  unitHref,
  unitOutline,
  unitSummary,
} from "./registry";
import { unitSchema, type GlossaryEntry, type Item, type Unit } from "./schema";

function lesson(id: string, extra: Partial<Item> = {}): unknown {
  return {
    kind: "lesson",
    id,
    title: `Lesson ${id}`,
    exercises: [
      {
        id: "ex-1",
        title: "Ex",
        martu: "Use a [[variable]].",
        starter: "",
        checkpoints: [
          {
            id: "step-1",
            text: "Do it.",
            hints: ["Hint with [[String|strings]].", "Second hint."],
            checks: [{ name: "c", code: "assert True" }],
          },
        ],
        solution: "x = 1",
      },
    ],
    ...extra,
  };
}

function rawUnit(id: string, order: number, items: unknown[], published = true): unknown {
  return { id, order, title: `Unit ${id}`, published, martuIntro: "Hi.", goals: ["Learn"], items };
}

const entries: GlossaryEntry[] = [
  { term: "variable", aliases: ["variables"], plain: "A name for a value." },
  { term: "string", aliases: ["strings"], plain: "Text in quotes." },
  { term: "loop", aliases: [], plain: "Repeat." },
];

describe("the bundled course", () => {
  it("parses the course, glossary and every unit, in order", () => {
    expect(courseMeta.id).toBe("intro-python");
    expect(courseMeta.settings.quizReadyPercent).toBeGreaterThan(0);
    expect(glossary.length).toBeGreaterThan(0);
    expect(allUnits.length).toBeGreaterThan(0);
    const orders = allUnits.map((unit) => unit.order);
    expect(orders).toEqual([...orders].sort((left, right) => left - right));
  });

  it("registers every unit JSON file", () => {
    const dir = path.join(process.cwd(), "content/courses/intro-python/units");
    const files = readdirSync(dir).filter((file) => file.endsWith(".json") && !file.endsWith(".verify.json"));
    expect(allUnits.map((unit) => unit.id).sort()).toEqual(files.map((file) => file.replace(/\.json$/, "")).sort());
  });

  it("builds page props for every item with only the glossary entries it uses", () => {
    for (const unit of allUnits) {
      for (const item of unit.items) {
        const props = itemPageProps(unit.id, item.id);
        expect(props, `${unit.id}/${item.id}`).toBeDefined();
        expect(props?.item).toBe(item);
        expect(props?.unit.items.map((entry) => entry.id)).toEqual(unit.items.map((entry) => entry.id));
        expect(props?.nextHref.startsWith("/intro-python/")).toBe(true);
        for (const entry of props?.glossary ?? []) expect(glossary).toContain(entry);
      }
    }
    expect(itemPageProps("nope", "nope")).toBeUndefined();
  });

  it("finds the glossary words the sample lesson links to", () => {
    const sample = findItem("sample", "first-words");
    if (!sample) return; // the sample unit may be removed later
    const terms = glossaryFor(sample.item).map((entry) => entry.term);
    // [[concatenate|glue]] resolves through an alias to the one shared "glue" entry (Unit 1 defines it too).
    expect(terms).toEqual(expect.arrayContaining(["string", "output", "variable", "glue"]));
  });
});

describe("parseUnits", () => {
  it("sorts by order", () => {
    const units = parseUnits([rawUnit("b", 2, [lesson("x")]), rawUnit("a", 1, [lesson("y")])]);
    expect(units.map((unit) => unit.id)).toEqual(["a", "b"]);
  });

  it("names the unit that fails to parse", () => {
    expect(() => parseUnits([{ id: "broken", order: 1 }])).toThrow(/unit "broken"/);
  });

  it("rejects duplicate unit ids, orders and item ids", () => {
    expect(() => parseUnits([rawUnit("a", 1, [lesson("x")]), rawUnit("a", 2, [lesson("x")])])).toThrow(/two units/);
    expect(() => parseUnits([rawUnit("a", 1, [lesson("x")]), rawUnit("b", 1, [lesson("x")])])).toThrow(/both have order/);
    expect(() => parseUnits([rawUnit("a", 1, [lesson("x"), lesson("x")])])).toThrow(/two items/);
  });
});

describe("lookups and links", () => {
  const units: Unit[] = parseUnits([
    rawUnit("hello", 1, [
      lesson("first"),
      { kind: "quiz", id: "quiz", title: "Quiz", questions: [{ type: "mc", id: "q", q: "Q?", explain: "E.", choices: ["a", "b"], answer: 0 }] },
      { kind: "testout", id: "quick-check", title: "Quick Check", exercises: (lesson("t") as { exercises: unknown[] }).exercises },
    ]),
    rawUnit("later", 2, [lesson("one")], false),
  ]);
  const [hello] = units;

  it("finds units and items", () => {
    expect(findUnit("hello", units)?.id).toBe("hello");
    expect(findUnit("missing", units)).toBeUndefined();
    expect(findItem("hello", "quiz", units)?.item.kind).toBe("quiz");
    expect(findItem("hello", "missing", units)).toBeUndefined();
    expect(publishedUnits(units).map((unit) => unit.id)).toEqual(["hello"]);
  });

  it("builds app paths without the base path or a trailing slash", () => {
    expect(unitHref("hello")).toBe("/intro-python/hello");
    expect(itemHref("hello", "first")).toBe("/intro-python/hello/first");
  });

  it("goes to the next item, skips the Quick Check, and returns to the unit at the end", () => {
    expect(nextHref(hello, hello.items[0])).toBe("/intro-python/hello/quiz");
    expect(nextHref(hello, hello.items[1])).toBe("/intro-python/hello");
    expect(nextHref(hello, hello.items[2])).toBe("/intro-python/hello");
    expect(nextHref(hello, { id: "missing" })).toBe("/intro-python/hello");
  });

  it("summarizes a unit without content", () => {
    const summary = unitSummary(hello);
    expect(summary).toEqual({
      id: "hello",
      order: 1,
      title: "Unit hello",
      items: [
        { id: "first", kind: "lesson", title: "Lesson first", optional: false },
        // A quiz's size and a Quick Check's tasks: what a Quick Check pass needs (progress.ts quickCheckPassed).
        { id: "quiz", kind: "quiz", title: "Quiz", optional: false, questionCount: 1 },
        { id: "quick-check", kind: "testout", title: "Quick Check", optional: true, exercises: [{ id: "ex-1" }] },
      ],
    });
    expect(JSON.stringify(summary)).not.toContain("assert");
  });

  it("outlines a unit with exercise ids for progress maths", () => {
    const outline = unitOutline(hello);
    expect(outline.published).toBe(true);
    expect(outline.items[0].exercises).toEqual([{ id: "ex-1" }]);
    expect(outline.items[1].exercises).toEqual([]);
    expect(JSON.stringify(outline)).not.toContain("assert");
  });

  it("collects glossary entries from prose and hints, by term or alias, ignoring case", () => {
    const item = hello.items[0];
    expect(glossaryFor(item, entries).map((entry) => entry.term)).toEqual(["variable", "string"]);
    expect(glossaryForTexts(["[[VARIABLES]] and [[nothing]]"], entries).map((entry) => entry.term)).toEqual([
      "variable",
    ]);
  });

  it("does not read glossary links out of code fields", () => {
    const item = unitSchema.parse(
      rawUnit("u", 1, [
        lesson("x", {
          exercises: [
            {
              id: "e",
              title: "E",
              martu: "Plain.",
              starter: "grid = [[loop]]",
              checkpoints: [{ id: "s", text: "Go.", hints: ["a", "b"], checks: [{ name: "c", code: "assert [[loop]]" }] }],
              solution: "[[loop]]",
            },
          ],
        } as Partial<Item>),
      ]),
    ).items[0];
    expect(glossaryFor(item, entries)).toEqual([]);
  });

  it("collects a unit page's glossary from the intro and goals", () => {
    const unit = unitSchema.parse({
      ...(rawUnit("u", 1, [lesson("x")]) as object),
      martuIntro: "A [[loop]].",
      goals: ["Store a [[variable]]"],
    });
    expect(glossaryForUnit(unit, entries).map((entry) => entry.term)).toEqual(["loop", "variable"]);
  });
});

describe("bundle guard", () => {
  it("no client component imports the registry (it would ship the whole course)", () => {
    const dir = path.join(process.cwd(), "src/components/course");
    const offenders = readdirSync(dir)
      .filter((file) => /\.(ts|tsx)$/.test(file) && !file.endsWith(".test.ts"))
      .filter((file) => /from\s+["'][^"']*lib\/course\/registry["']/.test(readFileSync(path.join(dir, file), "utf8")));
    expect(offenders).toEqual([]);
  });
});
