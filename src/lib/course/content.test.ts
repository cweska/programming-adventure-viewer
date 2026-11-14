import { spawn, spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import courseJson from "../../../content/courses/intro-python/course.json";
import glossaryJson from "../../../content/courses/intro-python/glossary.json";
import { courseMetaSchema, glossaryEntrySchema, playablesOf, unitSchema, type Item, type Unit } from "./schema";
import { rawUnits } from "./units.generated";

/**
 * The Intro to Python content pipeline: prototypes (Python) -> harness -> exporter -> units/*.json.
 * Python is the authored source; these tests prove the exported JSON is fresh, valid and linked up.
 */

const ROOT = process.cwd();
const HARNESS = path.join(ROOT, "docs/intro-to-python/prototypes/harness.py");
const PROTOTYPES = path.join(ROOT, "docs/intro-to-python/prototypes");
const SAMPLE_DIR = path.join(ROOT, "scripts/course/sample");
const EXPORTER = path.join(ROOT, "scripts/course/export_prototypes.py");
const CONTENT = path.join(ROOT, "content/courses/intro-python");
const UNITS_DIR = path.join(CONTENT, "units");
const GENERATED_TS = path.join(ROOT, "src/lib/course/units.generated.ts");
const PROTOTYPE_FILE = /^u[0-9][0-9].*_.*\.py$/;
const SLOW = 600_000;

const scratch: string[] = [];
function tempDir(): string {
  const dir = mkdtempSync(path.join(os.tmpdir(), "intro-python-content-"));
  scratch.push(dir);
  return dir;
}
afterAll(() => {
  for (const dir of scratch) rmSync(dir, { recursive: true, force: true });
});

function python(args: string[], env: Record<string, string> = {}) {
  const child = spawnSync("python3", args, {
    cwd: ROOT,
    env: { ...process.env, ...env },
    encoding: "utf8",
    timeout: SLOW - 10_000,
    maxBuffer: 64 * 1024 * 1024,
  });
  return { status: child.status, output: `${child.stdout ?? ""}${child.stderr ?? ""}`, error: child.error };
}

/**
 * python3 without blocking: the harness takes over a minute, and a blocked test worker misses vitest's
 * heartbeat ("Timeout calling onTaskUpdate"), which fails the whole run even when every test passes.
 */
function pythonAsync(args: string[], env: Record<string, string> = {}): Promise<{ status: number | null; output: string }> {
  return new Promise((resolve) => {
    const child = spawn("python3", args, { cwd: ROOT, env: { ...process.env, ...env } });
    let output = "";
    const keep = (chunk: Buffer) => {
      output = `${output}${chunk.toString("utf8")}`.slice(-64 * 1024);
    };
    child.stdout.on("data", keep);
    child.stderr.on("data", keep);
    const timer = setTimeout(() => child.kill("SIGKILL"), SLOW - 10_000);
    child.on("error", (error) => {
      clearTimeout(timer);
      resolve({ status: null, output: `${output}${String(error)}` });
    });
    child.on("close", (status) => {
      clearTimeout(timer);
      resolve({ status, output });
    });
  });
}

type HarnessReport = { errors: string[]; stats?: { units?: unknown[] } };

async function runHarness(dir: string): Promise<{ status: number | null; errors: string[]; units: number | null; output: string }> {
  const reportPath = path.join(tempDir(), "report.json");
  const result = await pythonAsync([HARNESS, "--json", reportPath], { PROTOTYPE_DIR: dir });
  const report: HarnessReport | null = existsSync(reportPath) ? JSON.parse(readFileSync(reportPath, "utf8")) : null;
  return {
    status: result.status,
    errors: report?.errors ?? [],
    units: report?.stats?.units?.length ?? null,
    output: result.output.slice(-4000),
  };
}

const unitFiles = existsSync(UNITS_DIR)
  ? readdirSync(UNITS_DIR)
      .filter((name) => name.endsWith(".json") && !name.endsWith(".verify.json"))
      .sort()
  : [];

function readJson(file: string): unknown {
  return JSON.parse(readFileSync(file, "utf8"));
}

function parsedUnits(): Unit[] {
  return unitFiles.map((name) => unitSchema.parse(readJson(path.join(UNITS_DIR, name))));
}

/* ------------------------------------------------------------------------------------------------ */
/* Prose helpers                                                                                     */
/* ------------------------------------------------------------------------------------------------ */

/** Keys whose string values are prose (the tiny format: paragraphs, lists, `code`, [[glossary]]). */
const PROSE_KEYS = new Set([
  "martuIntro",
  "goals",
  "summary",
  "intro",
  "martu",
  "text",
  "label",
  "hints",
  "passLine",
  "why",
  "takeaway",
  "q",
  "explain",
  "whyWrong",
  "body",
  "note",
]);

/** Every prose string in a raw unit, with a path for error messages. Code fields are skipped. */
function proseStrings(value: unknown, where = ""): { where: string; text: string }[] {
  if (Array.isArray(value)) return value.flatMap((entry, i) => proseStrings(entry, `${where}[${i}]`));
  if (!value || typeof value !== "object") return [];
  return Object.entries(value as Record<string, unknown>).flatMap(([key, child]) => {
    const at = where ? `${where}.${key}` : key;
    if (!PROSE_KEYS.has(key)) return proseStrings(child, at);
    if (typeof child === "string") return [{ where: at, text: child }];
    const strings = Array.isArray(child) ? child : child && typeof child === "object" ? Object.values(child) : [];
    return strings.filter((s): s is string => typeof s === "string").map((text, i) => ({ where: `${at}[${i}]`, text }));
  });
}

/** Prose without fenced code blocks (whose code may legitimately contain [[ or backticks). */
function withoutFences(text: string): string {
  return text.replace(/```[\s\S]*?```/g, " ");
}

/** Marks prose-format.ts would show as they are (see the prose rules test). */
function proseMarkProblems(text: string): string[] {
  const plain = withoutFences(text);
  const problems: string[] = [];
  for (const span of plain.matchAll(/`([^`\n]*)`/g)) {
    if (/\[\[[A-Za-z][^\]|]*(?:\|[^\]]*)?\]\]/.test(span[1])) problems.push(`a [[glossary link]] inside \`${span[1]}\``);
  }
  // A link's shown text may be plain words or one whole code span ([[len()|`len(wall)`]]); anything else with a
  // backtick shows its [[ | ]] marks.
  for (const link of plain.matchAll(/\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]/g)) {
    const [whole, term, label] = link;
    if (term.includes("`") || (label?.includes("`") && !/^`[^`\n\]]+`$/.test(label))) {
      problems.push(`a [[glossary link]] that mixes code and words: ${whole} (show plain words, or one code span)`);
    }
  }
  const words = plain.replace(/`[^`\n]*`/g, "CODE");
  if (/\*\*/.test(words)) problems.push("** (bold is not rendered: use *one star*)");
  for (const emphasis of words.matchAll(/(?<![\w*])\*(?=[^\s*])([^*\n]*?[^\s*])\*(?![\w*])/g)) {
    if (emphasis[1].includes("CODE")) problems.push(`*stars* around a code span: ${emphasis[0]}`);
  }
  return problems;
}

function glossaryLinks(text: string): string[] {
  const plain = withoutFences(text).replace(/`[^`\n]*`/g, " ");
  return [...plain.matchAll(/\[\[([^\]|]+)(?:\|[^\]]*)?\]\]/g)].map((match) => match[1].trim());
}

function itemsWithExercises(unit: Unit): { item: Item; checkpoints: number; key: string }[] {
  return unit.items.flatMap((item) =>
    playablesOf(item).map(({ key, exercise }) => ({
      item,
      checkpoints: exercise.checkpoints.length,
      key: key ? `${item.id}/${key}` : item.id,
    })),
  );
}

/* ------------------------------------------------------------------------------------------------ */
/* 1. The harness passes                                                                             */
/* ------------------------------------------------------------------------------------------------ */

describe("prototype harness", () => {
  it(
    "verifies every course unit in docs/intro-to-python/prototypes",
    async () => {
      const files = readdirSync(PROTOTYPES).filter((name) => PROTOTYPE_FILE.test(name));
      if (files.length === 0) return; // no units written yet: nothing to verify
      const result = await runHarness(PROTOTYPES);
      expect(result.errors, result.output).toEqual([]);
      expect(result.status, result.output).toBe(0);
    },
    SLOW,
  );

  it(
    "verifies the sample unit in scripts/course/sample",
    async () => {
      const result = await runHarness(SAMPLE_DIR);
      expect(result.errors, result.output).toEqual([]);
      expect(result.status, result.output).toBe(0);
      if (result.units !== null) expect(result.units, "the harness should find the sample unit").toBe(1);
    },
    SLOW,
  );
});

/* ------------------------------------------------------------------------------------------------ */
/* 2. The committed JSON is what the exporter makes                                                  */
/* ------------------------------------------------------------------------------------------------ */

describe("exporter", () => {
  it(
    "export --check passes (the JSON matches the prototypes)",
    () => {
      const result = python([EXPORTER, "--check"]);
      expect(result.status, result.output).toBe(0);
    },
    SLOW,
  );

  it(
    "--sample-only refuses to write over the committed course without --out",
    () => {
      const result = python([EXPORTER, "--sample-only"]);
      expect(result.status).toBe(2);
      expect(result.output).toContain("--out");
    },
    SLOW,
  );

  it(
    "--sample-only --out writes the same sample unit as the committed one",
    () => {
      const out = tempDir();
      const result = python([EXPORTER, "--sample-only", "--out", out]);
      expect(result.status, result.output).toBe(0);
      for (const name of ["sample.json", "sample.verify.json"]) {
        expect(readFileSync(path.join(out, "units", name), "utf8")).toBe(readFileSync(path.join(UNITS_DIR, name), "utf8"));
      }
      const ts = readFileSync(path.join(out, "units.generated.ts"), "utf8");
      expect(ts).toContain('import unit_sample from "./units/sample.json";');
    },
    SLOW,
  );

  it(
    "--check fails with a clear message when the JSON is stale, missing or extra",
    () => {
      const root = tempDir();
      mkdirSync(path.join(root, "scripts/course/sample"), { recursive: true });
      copyFileSync(path.join(SAMPLE_DIR, "u00_sample.py"), path.join(root, "scripts/course/sample/u00_sample.py"));
      expect(python([EXPORTER, "--root", root]).status).toBe(0);
      expect(python([EXPORTER, "--root", root, "--check"]).status).toBe(0);

      const unitPath = path.join(root, "content/courses/intro-python/units/sample.json");
      writeFileSync(unitPath, readFileSync(unitPath, "utf8").replace("Read the chalk", "Read the chalk!"));
      writeFileSync(path.join(root, "content/courses/intro-python/units/old-unit.json"), "{}\n");
      const stale = python([EXPORTER, "--root", root, "--check"]);
      expect(stale.status).toBe(1);
      expect(stale.output).toContain("changed: content/courses/intro-python/units/sample.json");
      expect(stale.output).toContain("not exported by any prototype: content/courses/intro-python/units/old-unit.json");
      expect(stale.output).toContain("npm run course:export");

      // A plain export repairs it and removes the stale file.
      expect(python([EXPORTER, "--root", root]).status).toBe(0);
      expect(existsSync(path.join(root, "content/courses/intro-python/units/old-unit.json"))).toBe(false);
      expect(python([EXPORTER, "--root", root, "--check"]).status).toBe(0);
    },
    SLOW,
  );

  it(
    "maps the prototype format to the schema: split units, defaults, numbering, sidecar, glossary merge",
    () => {
      const src = tempDir();
      const out = tempDir();
      const unitHead = `UNIT = dict(id="split-unit", order=5, title="Split", martu_intro="Hi, yes?", goals=["One"], campaign_links=[])\n`;
      writeFileSync(
        path.join(src, "u05a_split.py"),
        `${unitHead}GLOSSARY = [dict(term="string", plain="Text in quotes.", aliases=["strings"])]
ITEMS = [dict(kind="lesson", id="first", title="First", notes="item note", exercises=[dict(
    id="say-hi", title="Say hi", martu="Print it, yes?", example="print('hi')\\n", example_output="hi",
    another_way=[dict(angle="shorter", text="Just print.")], stdin=["Lucky"], starter="",
    checkpoints=[
        dict(text="1. Print hi.", hints=["a", "b"], checks=[("prints hi", "assert 'hi' in _lines(), 'Print hi.'")]),
        dict(id="twice", text="2. Print it again.", hints=["a", "b"], checks=[("two", "assert _lines().count('hi') == 2, 'Twice.'")]),
    ],
    solution="print('hi')\\nprint('hi')\\n", starter_passes=False, partials=["print('hi')\\n"],
    wrong_answers=[dict(why="once", code="print('hi')\\n", fails_at=2, message_contains="Twice")],
)])]
`,
      );
      writeFileSync(
        path.join(src, "u05b_split.py"),
        `${unitHead}GLOSSARY = [dict(term="String", plain="Text in quotes.", aliases=["strings"]), dict(term="output", plain="What prints.")]
ITEMS = [dict(kind="quiz", id="check", title="Check", questions=[
    dict(type="mc", q="Pick", choices=["a", "b"], answer=1, why_wrong={0: "No."}, explain="B."),
    dict(type="fill", q="Fill", code="print(___)\\n", answer="1", accept=[1], expected_output="1", explain="One."),
])]
`,
      );
      const result = python([EXPORTER, "--src", src, "--out", out]);
      expect(result.status, result.output).toBe(0);
      const unit = unitSchema.parse(readJson(path.join(out, "units/split-unit.json")));
      expect(unit.published).toBe(false);
      expect(unit.items.map((item) => item.id)).toEqual(["first", "check"]);
      const lesson = unit.items[0];
      if (lesson.kind !== "lesson") throw new Error("expected a lesson");
      const exercise = lesson.exercises[0];
      expect(exercise.checkpoints.map((cp) => cp.id)).toEqual(["step-1", "twice"]);
      expect(exercise.checkpoints.map((cp) => cp.text)).toEqual(["Print hi.", "Print it again."]);
      expect(exercise.checkpoints[0].checks[0]).toEqual({ name: "prints hi", code: "assert 'hi' in _lines(), 'Print hi.'" });
      expect(exercise.example).toEqual({ code: "print('hi')\n", output: "hi" });
      expect(exercise.anotherWay).toEqual([{ angle: "shorter", text: "Just print." }]);
      expect(exercise.solution).toBe("print('hi')\nprint('hi')\n");
      const raw = readJson(path.join(out, "units/split-unit.json")) as { items: { exercises?: { solution: unknown }[] }[] };
      expect(raw.items[0].exercises?.[0].solution).toEqual(["print('hi')", "print('hi')"]);
      const quiz = unit.items[1];
      if (quiz.kind !== "quiz") throw new Error("expected a quiz");
      expect(quiz.questions.map((q) => q.id)).toEqual(["q-1", "q-2"]);
      const [mc, fill] = quiz.questions;
      expect(mc.type === "mc" && mc.whyWrong).toEqual({ "0": "No." });
      expect(fill.type === "fill" && fill.accept).toEqual(["1"]);

      expect(readJson(path.join(out, "units/split-unit.verify.json"))).toEqual({
        unit: "split-unit",
        items: { first: { notes: "item note" } },
        exercises: {
          "first/say-hi": {
            partials: [["print('hi')"]],
            wrongAnswers: [{ why: "once", code: ["print('hi')"], failsAt: 2, messageContains: "Twice" }],
          },
        },
        questions: {},
      });
      const glossary = (readJson(path.join(out, "glossary.json")) as { term: string }[]).map((entry) => entry.term);
      expect(glossary).toEqual(["output", "string"]);
      const text = readFileSync(path.join(out, "units/split-unit.json"), "utf8");
      expect(text.endsWith("}\n")).toBe(true);
      expect(text).toContain('\n  "id": "split-unit",\n');
    },
    SLOW,
  );

  it(
    "rejects unknown fields, bad ids and duplicate ids with the file named",
    () => {
      const src = tempDir();
      writeFileSync(
        path.join(src, "u07_broken.py"),
        `UNIT = dict(id="Broken Unit", order=7, title="Broken", martu_intro="Hi.", goals=["x"], campaign_links=[])
ITEMS = [
    dict(kind="lesson", id="a", title="A", exercises=[dict(id="e", title="E", martu="M", starter="", solution="",
         checkpoints=[dict(text="Do it.", hints=["a", "b"], checks=[("c", "assert True")])], typo_field=1)]),
    dict(kind="cheatsheet", id="a", title="Dup", entries=[dict(concept="x", code="print(1)\\n", setup="")]),
]
`,
      );
      const result = python([EXPORTER, "--src", src, "--out", tempDir()]);
      expect(result.status).toBe(1);
      expect(result.output).toContain("u07_broken.py");
      expect(result.output).toContain("'Broken Unit' must be lower-case words joined by dashes");
      expect(result.output).toContain("unknown field 'typo_field'");
      expect(result.output).toContain("unknown field 'setup'");
      expect(result.output).toContain("duplicate id 'a'");
      expect(result.output).toContain("nothing was written");
    },
    SLOW,
  );
});

/* ------------------------------------------------------------------------------------------------ */
/* 3. The exported content is valid and linked up                                                    */
/* ------------------------------------------------------------------------------------------------ */

describe("exported course content", () => {
  it("has at least the sample unit", () => {
    expect(unitFiles).toContain("sample.json");
  });

  it("parses every units/*.json with unitSchema", () => {
    for (const name of unitFiles) {
      const result = unitSchema.safeParse(readJson(path.join(UNITS_DIR, name)));
      const issues = result.success
        ? ""
        : result.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`).join("\n");
      expect(result.success, `${name}\n${issues}`).toBe(true);
    }
  });

  it("names each unit file after its unit id", () => {
    for (const name of unitFiles) {
      expect((readJson(path.join(UNITS_DIR, name)) as { id: string }).id).toBe(name.replace(/\.json$/, ""));
    }
  });

  it("keeps ids unique within their parents, and clear of course routes", () => {
    const units = parsedUnits();
    const unitIds = units.map((unit) => unit.id);
    expect(new Set(unitIds).size, "unit ids").toBe(unitIds.length);
    for (const reserved of ["glossary", "placement", "cheatsheets", "preview"]) expect(unitIds).not.toContain(reserved);
    const orders = units.map((unit) => unit.order);
    expect(new Set(orders).size, "unit order numbers").toBe(orders.length);
    for (const unit of units) {
      const itemIds = unit.items.map((item) => item.id);
      expect(new Set(itemIds).size, `${unit.id} item ids`).toBe(itemIds.length);
      for (const item of unit.items) {
        const exercises = playablesOf(item).map(({ exercise }) => exercise);
        if (item.kind === "lesson" || item.kind === "testout" || item.kind === "article") {
          const ids = exercises.map((exercise) => exercise.id);
          expect(new Set(ids).size, `${unit.id}/${item.id} exercise ids`).toBe(ids.length);
        }
        for (const exercise of exercises) {
          const ids = exercise.checkpoints.map((cp) => cp.id);
          expect(new Set(ids).size, `${unit.id}/${item.id}/${exercise.id} checkpoint ids`).toBe(ids.length);
        }
        if (item.kind === "quiz") {
          const ids = item.questions.map((q) => q.id);
          expect(new Set(ids).size, `${unit.id}/${item.id} question ids`).toBe(ids.length);
        }
      }
    }
  });

  it("parses glossary.json, with unique terms and aliases", () => {
    const glossary = glossaryEntrySchema.array().parse(glossaryJson);
    const names = glossary.flatMap((entry) => [entry.term, ...entry.aliases].map((name) => name.toLowerCase()));
    const dupes = names.filter((name, i) => names.indexOf(name) !== i);
    expect(dupes, "glossary terms and aliases must not repeat").toEqual([]);
  });

  it("resolves every [[glossary]] link in prose to glossary.json", () => {
    const glossary = glossaryEntrySchema.array().parse(glossaryJson);
    const known = new Set(glossary.flatMap((entry) => [entry.term, ...entry.aliases].map((name) => name.toLowerCase())));
    const missing: string[] = [];
    for (const term of glossaryLinks(courseMetaSchema.parse(courseJson).intro)) {
      if (!known.has(term.toLowerCase())) missing.push(`course.json intro: [[${term}]]`);
    }
    for (const name of unitFiles) {
      for (const { where, text } of proseStrings(readJson(path.join(UNITS_DIR, name)))) {
        for (const term of glossaryLinks(text)) {
          if (!known.has(term.toLowerCase())) missing.push(`${name} ${where}: [[${term}]]`);
        }
      }
    }
    expect(missing, "add these terms to a prototype's GLOSSARY (or fix the link)").toEqual([]);
  });

  it("follows the prose rules: balanced backticks, closed fences, no leading numbers on checkpoints", () => {
    const problems: string[] = [];
    for (const name of unitFiles) {
      for (const { where, text } of proseStrings(readJson(path.join(UNITS_DIR, name)))) {
        if ((text.match(/```/g) ?? []).length % 2 !== 0) problems.push(`${name} ${where}: unclosed \`\`\` fence`);
        if ((withoutFences(text).match(/`/g) ?? []).length % 2 !== 0) problems.push(`${name} ${where}: unbalanced backticks`);
      }
    }
    for (const unit of parsedUnits()) {
      for (const item of unit.items) {
        for (const { exercise } of playablesOf(item)) {
          for (const cp of exercise.checkpoints) {
            if (/^\s*\d+[.)]\s/.test(cp.text)) problems.push(`${unit.id}/${item.id}/${exercise.id}/${cp.id}: leading number`);
          }
        }
      }
    }
    expect(problems).toEqual([]);
  });

  it("uses only the marks prose-format.ts renders: no [[link]] inside `code`, no **bold**, no *stars* around `code`", () => {
    // `random.[[randint]](1, 6)` showed the brackets as code, and **both ends** showed the stars: students copy
    // what they see. A glossary link goes outside the code span; emphasis is single stars, around words only.
    const problems: string[] = [];
    for (const name of unitFiles) {
      for (const { where, text } of proseStrings(readJson(path.join(UNITS_DIR, name)))) {
        for (const problem of proseMarkProblems(text)) problems.push(`${name} ${where}: ${problem}`);
      }
    }
    expect(problems).toEqual([]);
  });

  it("keeps the pictures and tables in prose narrow enough for a phone (36 characters a line)", () => {
    // A fenced block in prose scrolls sideways on a 390px screen past about 36 characters, hiding the labels
    // that explain the picture. Put each label on its own line under the code, or make a table a numbered list.
    const wide: string[] = [];
    for (const name of unitFiles.filter((file) => file !== "sample.json")) {
      for (const { where, text } of proseStrings(readJson(path.join(UNITS_DIR, name)))) {
        let inFence = false;
        for (const line of text.split("\n")) {
          if (/^```/.test(line.trim())) inFence = !inFence;
          else if (inFence && line.length > 36) wide.push(`${name} ${where}: ${line.length} characters: ${line}`);
        }
      }
    }
    expect(wide).toEqual([]);
  });

  it("lists every units/*.json in units.generated.ts, in course order", () => {
    const ts = readFileSync(GENERATED_TS, "utf8");
    for (const name of unitFiles) {
      expect(ts, `${name} is not imported by units.generated.ts`).toContain(
        `from "../../../content/courses/intro-python/units/${name}";`,
      );
    }
    expect(ts).not.toMatch(/\.verify\.json/);
    const ids = rawUnits.map((raw) => (raw as { id: string }).id);
    expect([...ids].sort()).toEqual(unitFiles.map((name) => name.replace(/\.json$/, "")).sort());
    const orders = rawUnits.map((raw) => (raw as { order: number }).order);
    expect(orders).toEqual([...orders].sort((a, b) => a - b));
  });

  it("keeps a .verify.json sidecar beside every unit that points at real exercises", () => {
    for (const unit of parsedUnits()) {
      const file = path.join(UNITS_DIR, `${unit.id}.verify.json`);
      expect(existsSync(file), `${unit.id}.verify.json`).toBe(true);
      const sidecar = readJson(file) as {
        unit: string;
        items: Record<string, unknown>;
        exercises: Record<string, { partials?: unknown[]; wrongAnswers?: { failsAt?: number }[] }>;
      };
      expect(sidecar.unit).toBe(unit.id);
      const playables = new Map(itemsWithExercises(unit).map((entry) => [entry.key, entry.checkpoints]));
      for (const [key, data] of Object.entries(sidecar.exercises)) {
        expect(playables.has(key), `${unit.id}.verify.json names unknown exercise ${key}`).toBe(true);
        const checkpoints = playables.get(key) ?? 0;
        expect((data.partials ?? []).length, `${unit.id}/${key} partials`).toBeLessThan(Math.max(checkpoints, 1));
        for (const wrong of data.wrongAnswers ?? []) expect(wrong.failsAt ?? 0).toBeLessThanOrEqual(checkpoints);
      }
      const itemIds = new Set(unit.items.map((item) => item.id));
      for (const key of Object.keys(sidecar.items)) expect(itemIds.has(key), `${unit.id}.verify.json item ${key}`).toBe(true);
    }
  });

  it("parses course.json, opening with Mar'tu's line", () => {
    const course = courseMetaSchema.parse(courseJson);
    expect(course.title).toBe("Intro to Python");
    expect(course.intro.startsWith(
      "Hi. It is me, Mar'tu. Before we continue on our adventure you must learn some of the language we call, Python.",
    )).toBe(true);
  });
});

/* ------------------------------------------------------------------------------------------------ */
/* The sample unit is the teacher's tour and the e2e fixture: it must keep covering everything       */
/* ------------------------------------------------------------------------------------------------ */

describe("sample unit coverage", () => {
  const sample = unitSchema.parse(readJson(path.join(UNITS_DIR, "sample.json")));
  const playables = sample.items.flatMap((item) => playablesOf(item).map(({ exercise }) => exercise));

  it("is the unpublished teacher preview, ordered last", () => {
    expect(sample.published).toBe(false);
    expect(sample.order).toBe(99);
    expect(sample.title).toBe("Sample Unit (teacher preview)");
  });

  it("has every item kind and question type", () => {
    expect(new Set(sample.items.map((item) => item.kind))).toEqual(
      new Set(["lesson", "quiz", "project", "challenge", "article", "cheatsheet", "testout"]),
    );
    const types = sample.items.flatMap((item) => (item.kind === "quiz" ? item.questions.map((q) => q.type) : []));
    expect(new Set(types)).toEqual(new Set(["mc", "predict", "fill", "parsons", "bug"]));
  });

  it("starts with a three-exercise lesson: run-and-read, input(), and a full-featured exercise", () => {
    const lesson = sample.items[0];
    if (lesson.kind !== "lesson") throw new Error("the sample starts with a lesson");
    expect(lesson.exercises).toHaveLength(3);
    const [read, ask, full] = lesson.exercises;
    expect(read.starterPasses).toBe(true);
    expect(read.example?.output).toBeTruthy();
    expect(ask.stdin?.length).toBeGreaterThan(0);
    expect(ask.example?.stdin).toEqual(ask.stdin);
    expect(full.checkpoints.length).toBeGreaterThanOrEqual(2);
    expect(full.checkpoints.every((cp) => cp.hints.length >= 2)).toBe(true);
    expect(full.anotherWay.length).toBeGreaterThan(0);
    expect(full.bonus).toBeDefined();
    expect(full.assemble).toBeDefined();
    expect(full.campaignLink).toBeDefined();
    expect(full.tracer).toBe(true);
  });

  it("uses the engine, hidden setup, an advanced variant, article examples with a try-it, and no-support test-outs", () => {
    expect(playables.some((exercise) => exercise.engine)).toBe(true);
    expect(playables.some((exercise) => exercise.setup)).toBe(true);
    const challenges = sample.items.filter((item) => item.kind === "challenge");
    expect(challenges.some((item) => item.kind === "challenge" && item.level === "advanced" && item.variantOf)).toBe(true);
    const article = sample.items.find((item) => item.kind === "article");
    expect(article?.kind === "article" && article.examples.length > 0 && article.exercises.length > 0).toBe(true);
    const testout = sample.items.find((item) => item.kind === "testout");
    expect(testout?.kind === "testout" && testout.exercises.every((exercise) => exercise.support === "none")).toBe(true);
  });

  it("uses every newer exercise field: predict, names, pick, pair talk, solo, the lean explainer, and dictated true and false", () => {
    const predict = playables.find((exercise) => exercise.predict)?.predict;
    expect(predict?.choices.length).toBeGreaterThanOrEqual(2);
    expect(predict?.choices[predict.answer]).toBeTruthy();
    expect(playables.some((exercise) => exercise.names.length > 0)).toBe(true);
    expect(playables.some((exercise) => exercise.pick)).toBe(true);
    expect(playables.some((exercise) => exercise.pairTalk)).toBe(true);
    expect(playables.some((exercise) => exercise.solo)).toBe(true);
    expect(playables.some((exercise) => exercise.explainer === "lean")).toBe(true);
    const dictated = playables.flatMap((exercise) => exercise.checkpoints.map((cp) => cp.dictated));
    expect(dictated).toContain(true);
    expect(dictated).toContain(false);
  });

  it("keeps the worked example visibly different from the task (other names, not the task with new values)", () => {
    for (const exercise of playables) {
      if (!exercise.example) continue;
      const exampleNames = new Set([...exercise.example.code.matchAll(/^([A-Za-z_]\w*)\s*=/gm)].map((match) => match[1]));
      const taskNames = [...exercise.solution.matchAll(/^([A-Za-z_]\w*)\s*=/gm)].map((match) => match[1]);
      expect(taskNames.filter((name) => exampleNames.has(name)), exercise.id).toEqual([]);
    }
  });

  it("links prose to the glossary", () => {
    const links = proseStrings(readJson(path.join(UNITS_DIR, "sample.json"))).flatMap(({ text }) => glossaryLinks(text));
    expect(links.length).toBeGreaterThan(3);
  });
});
