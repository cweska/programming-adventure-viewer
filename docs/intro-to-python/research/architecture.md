# Intro to Python: architecture proposal

Status: proposal only. Nothing in the repo has changed. Read with `context/brief.md`,
`research/codecademy-mechanics.md`, `docs/campaign/README.md`, and the prototype verifier at
`docs/intro-to-python/prototypes/harness.py`, which already defines the prototype unit format.

The approach in one paragraph. "Intro to Python" is a **separate course** that lives beside the campaign
and does not extend it. The course has its own zod schema (`src/lib/course/`), its own JSON content
(`content/courses/intro-python/`), its own routes (`/intro-python/...`), and its own client player
(`src/components/course/`). It reuses the parts of the campaign stack that already work:
- the Pyodide worker and its per-check results,
- `run-checks.ts` for CPython unit tests,
- `ConsolePanel`, `PythonEditor`, `Instructions` and `explainPython`,
- the autosave principles (save by id, debounce, flush on pagehide),
- the classroom store and its two backends (SQLite, and browser `localStorage` for the GitHub Pages export).

Campaign modules, `Player.tsx`, `bundledModules`, and every existing test stay as they are. Every worker
change is additive and off by default.

---

## 0. What exists today and what it constrains

| Fact in the repo | Consequence for the course |
| --- | --- |
| `next.config.ts` builds a static export for GitHub Pages (`output: "export"`, `basePath`, `trailingSlash`). With `pageExtensions: ["tsx","jsx","mdx"]`, every `route.ts` drops out of that export. | Every course page must be a `page.tsx` with `generateStaticParams` and `dynamicParams = false`. Any API route works only in server mode, so classroom code needs an `isStaticExport` branch, like the classroom code that exists today. |
| `Player.tsx` (1,100 lines) imports `findModule`, so every module's JSON ships in the client bundle. | The course should **not** copy this. Pages are server components that pick one item from the course and pass only that item to the client player. |
| Worker: `runProgram` runs `GUARD`, then `setup`, then the code, then each check in the same globals. It returns `checks[]` in order, each with `{name, passed, message}`. `message` is the last traceback line, for example `AssertionError: Did you…?`. | Checkpoint grading needs **no worker change**. The client flattens checkpoints into one `checks[]` list and regroups the results by index. The `AssertionError: ` prefix has to be stripped for display. |
| `GUARD` is a JS template literal, and `run-checks.ts` refuses it if it contains `${` or `\`. | New Python that runs in the browser (check helpers, tracer, input shim) should live in **`.py` files next to the worker**. The worker fetches them before it disables the network. Tests and the harness then read the same files. This removes the escaping problem: the concept tokenizer needs backslashes in its regexes. |
| `GUARD` defines `party`, `user`, `stage`, `print_prompt`, and other names globally. | In a NameError lesson, `print(user)` would *not* fail. Course runs need a **plain prelude** (import guard plus course helpers). Only rehearsal exercises opt into the engine objects with `"engine": true`. |
| `TIMEOUT_MS = 5000` terminates and restarts the worker. | That restart is a bad loop-lesson experience: Pyodide reloads and the student gets no line number. Course runs add a **step budget** so an infinite loop becomes a friendly error on the loop's line. The 5-second kill stays as the backstop. |
| Ruff auto-formats on load, blur and run with `quote-style: "double"`. | This **breaks Strings lessons**. `'It\'s'` becomes `"It's"`, so an escape-character checkpoint fails, and single-quote examples get rewritten. The course should default to no auto-format, or at least use `quote-style: "preserve"` (see §4.7). |
| `run-checks.ts` spawns `python3` per call. CI uses `ubuntu-latest`, where `python3` is 3.12. Pyodide 0.28 runs CPython 3.13. | Pin CI to Python 3.13 (`actions/setup-python`). Add a batch runner so about 1,000 course verifications don't cost 1,000 process spawns. |
| The classroom `progress` table has primary key `(student_id, module_id, lesson_id)` and holds one frontier `beat_id`. The report page has no module column. | Course progress gets its own small summary table and its own report section. Putting it in `progress` would mix unit rows into the campaign report. |
| The prototype harness format (`UNIT`, `ITEMS`, exercises with `checkpoints`, `hints`, `wrong_answers`, `partials`, `another_way`, `bonus`, `tracer`, `stdin`, quiz types mc/predict/fill/parsons/bug, test-out, article, cheatsheet) is already designed and verified. | The production schema is a **camelCase JSON image of the harness format**. A one-time exporter converts the prototypes. Every rule the harness enforces becomes a vitest test. |

---

## 1. Content format and schema

### 1.1 Where files live

```
content/courses/intro-python/
  course.json                     # title, unit order, milestones, settings (solution gating, quiz "ready" %)
  glossary.json                   # [{ term, aliases, plain, example?, firstUnit }]
  units/
    hello-world.json              # one unit: meta + ordered items (lessons, quizzes, projects, ...)
    hello-world.verify.json       # TEST-ONLY: partials, wrongAnswers, designer notes (never imported by pages)
    control-flow.json
    control-flow.verify.json
    ...
src/lib/course/
  schema.ts                       # zod schemas + types (client-safe)
  registry.ts                     # imports + parses the JSON (server/test only, see 1.4)
  outline.ts                      # tiny id/kind/count outline for client progress maths
public/workers/
  course_helpers.py               # _lines, _uses, _count, _assigned_from_expression, _inputs_used,
                                  # _concept_tokens, input shim, step budget, _eq for challenges
  tracer.py                       # sys.settrace driver for the step-through tracer
```

Why one JSON file per unit, rather than per item:
- It matches the "one `module.json` per module" precedent.
- It keeps the import list at about 9 lines.
- A unit stays reviewable as one diff.

Test-only data lives in the `.verify.json` sidecar: staged partials, known wrong answers, and designer
notes. That keeps it out of page payloads while it stays next to the content it tests.

**Code fields take a string or an array of lines.** An array is joined with `\n`, with a final newline
added. The exporter writes arrays, so JSON diffs of starter and solution code read line by line. This is
the pattern `e2e/friends.ts` already uses for solutions.

### 1.2 Zod sketch (`src/lib/course/schema.ts`)

```ts
import { z } from "zod";
import { imageSchema } from "../lesson/schema";

const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
/** Code may be a string or an array of lines (joined with "\n", trailing newline added). */
export const code = z.union([z.string(), z.array(z.string())])
  .transform((v) => (Array.isArray(v) ? `${v.join("\n")}\n` : v));
/** Mar'tu prose: same tiny format as campaign instructions (one line each, `code`, "1. " steps),
 *  plus ```python fenced blocks``` and [[glossary term]] / [[term|shown text]] links. */
const prose = z.string().min(1);
const token = z.string().regex(/^(node|op|const|call|attr|import):[A-Za-z_]+$/); // harness concept tokens

export const checkSchema = z.object({ name: z.string().min(1), code }).strict();

export const checkpointSchema = z.object({
  id: slug,                                   // progress is saved by id, never by position
  text: prose,                                // ONE action; no leading "1. " (the UI numbers checkpoints)
  hints: z.array(prose).min(2).max(5),        // ladder: nudge -> concept + tiny unrelated example -> partial -> near-answer
  checks: z.array(checkSchema).min(1),
  passLine: z.string().optional(),            // short in-world line when it turns green ("Bomb Shell: Works.")
}).strict();

const anotherWaySchema = z.object({
  angle: z.enum(["analogy", "step-by-step", "in-tor", "shorter", "picture", "from-the-campaign"]),
  label: z.string().optional(),               // button text override, e.g. "Picture it"
  text: prose,
}).strict();

const cameo = z.enum(["mar-tu", "oogrish", "gearshift", "bomb-shell", "lucky"]); // ids in content/campaign

export const bonusSchema = z.object({          // "side quest": optional, never required for completion
  by: cameo, title: z.string(), text: prose,
  hints: z.array(prose).default([]),
  checks: z.array(checkSchema).min(1), solution: code,
}).strict();

const support = z.enum(["full", "light", "none"]);
// full: hints + another-way + tracer + solution after gating (lessons)
// light: hints after the first failed run, solution after gating (projects, challenges)
// none: no hints/solution/another-way (test-outs)

export const exerciseSchema = z.object({
  id: slug, title: z.string().min(1),
  martu: prose,                               // the Learn pane, in Mar'tu's voice (≤ ~230 words, grade ≤ 9: harness thresholds)
  example: z.object({ code, output: z.string(), stdin: z.array(z.string()).optional() }).strict().optional(),
  anotherWay: z.array(anotherWaySchema).default([]),
  introduces: z.array(token).default([]),     // concept gate (harness ConceptGate)
  preview: z.array(token).default([]),        // shown before taught, justified in verify notes
  engine: z.boolean().default(false),         // load party/print_prompt/... (campaign rehearsal only)
  setup: code.optional(),                     // hidden code run before the student's
  stdin: z.array(z.string()).optional(),      // scripted answers for input(), in order
  starter: code,
  checkpoints: z.array(checkpointSchema).min(1).max(6),
  solution: code,
  starterPasses: z.boolean().default(false),  // e.g. "Run this and read the output" exercises
  tracer: z.boolean().default(false),         // offer "Step through" on example + student code
  support: support.default("full"),
  bonus: bonusSchema.optional(),
  campaignLink: z.object({                    // Lucky's "What's in it for me?" box
    module: z.string(), part: z.string(), snippet: code, why: prose,
  }).strict().optional(),
  takeaway: z.object({ concept: z.string(), code, note: z.string().optional() }).strict().optional(),
  faq: z.array(z.object({ q: z.string(), a: prose }).strict()).default([]),
}).strict();

const choiceExplain = z.record(z.string(), z.string()); // choice index -> why that choice is wrong
const qBase = { id: slug, q: prose, explain: prose, teaches: z.string().optional() /* "lessonId/exerciseId" */ };
export const questionSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("mc"), ...qBase, code: code.optional(), choices: z.array(z.string()).min(2),
             answer: z.number().int().min(0), whyWrong: choiceExplain.default({}) }).strict(),
  z.object({ type: z.literal("predict"), ...qBase, code, answer: z.string(), accept: z.array(z.string()).default([]),
             choices: z.array(z.string()).optional(), setup: code.optional(), stdin: z.array(z.string()).optional() }).strict(),
  z.object({ type: z.literal("fill"), ...qBase, code /* contains ___ */, answer: z.string(),
             accept: z.array(z.string()).default([]), chips: z.array(z.string()).optional(), expectedOutput: z.string() }).strict(),
  z.object({ type: z.literal("parsons"), ...qBase, lines: z.array(z.string()).min(2), distractors: z.array(z.string()).default([]),
             indent: z.boolean().default(false), expectedOutput: z.string() }).strict(),
  z.object({ type: z.literal("bug"), ...qBase, code, fix: code, expectedOutput: z.string(),
             checks: z.array(checkSchema).default([]) }).strict(),
]);

const itemBase = { id: slug, title: z.string().min(1), optional: z.boolean().default(false) };
export const itemSchema = z.discriminatedUnion("kind", [
  z.object({ kind: z.literal("lesson"), ...itemBase, summary: z.string().optional(), exercises: z.array(exerciseSchema).min(1) }).strict(),
  z.object({ kind: z.literal("quiz"), ...itemBase, readyPercent: z.number().min(0).max(100).optional(),
             questions: z.array(questionSchema).min(3) }).strict(),
  // A project is one exercise whose checkpoints are the task checklist, grouped under small headings.
  z.object({ kind: z.literal("project"), ...itemBase, ...exerciseSchema.omit({ id: true, title: true }).shape,
             support: support.default("light"),
             taskGroups: z.array(z.object({ title: z.string(), from: slug }).strict()).default([]),
             stretch: z.array(z.object({ text: prose, checks: z.array(checkSchema).default([]) }).strict()).default([]) }).strict(),
  // A challenge either lists checkpoints, or `tests` that compile to checks (see 4.4).
  z.object({ kind: z.literal("challenge"), ...itemBase, optional: z.boolean().default(true),
             level: z.enum(["core", "advanced"]), variantOf: slug.optional(),
             ...exerciseSchema.omit({ id: true, title: true, checkpoints: true }).shape,
             support: support.default("light"),
             checkpoints: z.array(checkpointSchema).optional(),
             tests: z.array(z.object({ call: z.string(), expect: z.string(), visible: z.boolean(), label: z.string() }).strict()).optional() }).strict(),
  z.object({ kind: z.literal("article"), ...itemBase, body: prose,
             examples: z.array(z.object({ code, output: z.string(), stdin: z.array(z.string()).optional() }).strict()).default([]),
             exercises: z.array(exerciseSchema).default([]) /* optional "try it" */ }).strict(),
  z.object({ kind: z.literal("cheatsheet"), ...itemBase, optional: z.boolean().default(true),
             entries: z.array(z.object({ concept: z.string(), code, output: z.string().optional(), note: z.string().optional() }).strict()).min(1) }).strict(),
  z.object({ kind: z.literal("testout"), ...itemBase, optional: z.boolean().default(true),
             quiz: z.array(questionSchema).default([]), quizPassPercent: z.number().default(80),
             exercises: z.array(exerciseSchema.extend({ covers: z.array(slug).min(1) /* lesson ids */,
                                                     support: z.literal("none").default("none") })).min(1) }).strict(),
]);

export const unitSchema = z.object({
  id: slug, order: z.number().int().min(1), title: z.string().min(1), short: z.string().min(1),
  published: z.boolean(),                       // same rule as campaign lessons: unpublished = ?preview=1 only
  martuIntro: prose, banner: imageSchema,       // reuse public/scenes/*.svg
  goals: z.array(z.string()).min(1),            // "Student can ..." lines from the curriculum plan
  campaignLinks: z.array(z.object({ module: z.string(), part: z.string(), why: z.string() }).strict()),
  items: z.array(itemSchema).min(1),
}).strict();

export const courseSchema = z.object({
  id: z.literal("intro-python"), title: z.literal("Intro to Python"),
  units: z.array(unitSchema).min(1),
  milestones: z.array(z.object({ id: slug, label: z.string(), campaignModule: z.string(),
                                 requiresUnits: z.array(slug) }).strict()), // "Ready for Module 2"
  settings: z.object({
    solutionAfter: z.object({ minutes: z.number().default(5), failedRuns: z.number().int().default(4),
                              hintsExhausted: z.boolean().default(true) }).strict(),
    quizReadyPercent: z.number().default(70),
    stepBudget: z.number().int().default(200_000),
  }).strict(),
}).strict();

// TEST-ONLY sidecar (units/<unit>.verify.json)
export const verifySchema = z.object({
  unit: slug,
  exercises: z.record(z.string() /* "itemId/exerciseId" or "itemId" for projects/challenges */, z.object({
    partials: z.array(code).default([]),      // partial k passes checkpoints 1..k and fails k+1
    wrongAnswers: z.array(z.object({ why: z.string(), code, failsAt: z.number().int().min(0),
                                     messageContains: z.string().optional() }).strict()).default([]),
    notes: z.string().optional(),
  }).strict()),
}).strict();
```

Glossary links use `[[term]]` and are checked by tests (see §6). Ids must be unique within their parent.
Progress keys are paths such as `lists/intro-to-lists/read-the-wall/print-first`. A test also blocks unit
ids that would collide with static routes (`glossary`, `placement`).

### 1.3 Example exercise (JSON, abbreviated)

```json
{
  "id": "read-the-wall",
  "title": "Read the chalk wall",
  "martu": "My chalk wall keeps the hours between bursts, yes?\nA [[list]] keeps many values under one name. Square brackets hold them. Commas go between.\nEvery value has a position, its [[index]]. The first index is `0`, not `1`. Strange, but you will get used to it.",
  "example": { "code": ["hours = [48, 48, 47]", "print(hours[0])"], "output": "48" },
  "anotherWay": [
    { "angle": "analogy", "text": "Picture a shelf of jars. The jar nearest your hand is jar `0`." },
    { "angle": "shorter", "text": "`[ ]` makes a list. `name[0]` reads the first item." }
  ],
  "introduces": ["node:List", "node:Subscript"],
  "starter": ["# The chalk wall, oldest burst first", ""],
  "checkpoints": [
    { "id": "make-wall",
      "text": "Make a list called `chalk_wall` that holds `48, 48, 47, 46, 44, 41, 37`.",
      "hints": ["Square brackets make a list. Put commas between the numbers.", "Start with `chalk_wall = [48, 48, ...]`."],
      "checks": [{ "name": "chalk_wall holds the hours",
                   "code": "assert chalk_wall == [48, 48, 47, 46, 44, 41, 37], 'Did you put all seven hours in chalk_wall, in order?'" }] },
    { "id": "print-first",
      "text": "Print the first hour on the wall.",
      "hints": ["The first index is `0`.", "Put `chalk_wall[0]` inside `print()`."],
      "checks": [{ "name": "prints 48", "code": "assert '48' in _lines(), 'Print the first hour on the wall.'" },
                 { "name": "reads it from the list", "code": "assert _uses('node:Subscript'), 'Read it from the list with chalk_wall[0], not by typing 48.'" }],
      "passLine": "Gearshift: Math checks out." }
  ],
  "solution": ["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "print(chalk_wall[0])"],
  "tracer": true,
  "bonus": { "by": "lucky", "title": "What's in it for me?",
             "text": "Print the newest hour without counting how long the list is.",
             "checks": [{ "name": "prints 37 by index", "code": "assert '37' in _lines() and _uses('op:USub'), 'Try a negative index.'" }],
             "solution": ["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "print(chalk_wall[0])", "print(chalk_wall[-1])"] }
}
```

Authoring rule from the harness partial test: **checks must stay true as later checkpoints are finished.**
For example, use `'48' in _lines()` rather than `_lines() == ['48']`, because the final solution has to pass
every checkpoint.

### 1.4 Bundling for static export

- `src/lib/course/registry.ts` statically imports `course.json`, `glossary.json` and each `units/*.json`,
  following the `modules.ts` pattern. It runs `courseSchema.parse` at import time. A bad file fails
  `npm test` first, and `next build` second.
- **Only server components and tests import the registry.** Each page picks out what it needs and passes
  plain props to a `"use client"` player:
  - the map page gets the course outline,
  - a unit page gets that unit's metadata and item list,
  - an item page gets that one item, the glossary entries it references, and the outline.
  
  Next serializes these props into each page's RSC payload, so an item page ships about 10–30 KB of its
  own content instead of the whole course.
- Guard: `src/lib/course/bundle.test.ts` scans every `"use client"` file under `src/components/course/`
  and fails if it imports `lib/course/registry`. This avoids a dependency; the optional alternative is the
  `server-only` package.
- `*.verify.json` is imported only by tests.
- Coexistence:
  - Course data never goes into `bundledModules`, the `ModulePicker` list, the authoring catalog
    (`content/modules` only), or `solutions.test.ts`, which still asserts exactly 19 coding parts.
  - `checkSchema` has the same shape as the campaign's, so `runPythonChecks` takes course checks unchanged.
  - The README rule "new JSON must be imported in the registry" carries over. A test lists
    `content/courses/intro-python/units/*.json` and asserts that the registry has every file.

### 1.5 From prototypes to JSON

`scripts/course/export_prototypes.py` (run once per unit, by hand) does the following:
- Loads `docs/intro-to-python/prototypes/uNN_*.py`.
- Converts snake_case to camelCase.
- Turns check tuples into `{name, code}`.
- Strips the leading `"N. "` from checkpoint text.
- Writes code as line arrays.
- Splits `partials`, `wrong_answers` and `notes` into `.verify.json`.

After export, **the JSON is canonical** and vitest is the CI gate. The harness stays a designer tool. It is
changed to read `course_helpers.py`, so it uses the same tokenizer as the site. Open question Q11 asks
whether to keep Python as the authored source instead.

---

## 2. Routes and navigation

| Route (static) | File | What it shows |
| --- | --- | --- |
| `/intro-python/` | `src/app/intro-python/page.tsx` | **Course map**: Mar'tu's opening ("Hi. It is me, Mar'tu. Before we continue on our adventure you must learn some of the language we call, Python."), then a trail of unit waypoints with status, the milestones ("Ready for Module 1/2"), and links to "Where should I start?" (placement), the glossary and the cheatsheets. |
| `/intro-python/[unitId]/` | `src/app/intro-python/[unitId]/page.tsx` | **Unit page**: banner scene + Mar'tu's unit intro (`Theater`), goals, item list (kind icon, status, "optional" tag), "Already know this? Test out", cheatsheet link, side quests / challenges. |
| `/intro-python/[unitId]/[itemId]/` | `src/app/intro-python/[unitId]/[itemId]/page.tsx` | **Item player** for any kind. Within a lesson, the current exercise is the URL hash (`#read-the-wall`), kept up to date with `history.replaceState`. This keeps about 70 static pages instead of about 200, and the Pyodide worker survives client-side navigation because `run.ts` holds it at module level. |
| `/intro-python/glossary/` | `src/app/intro-python/glossary/page.tsx` | Every term, its plain definition, a tiny example, and where it is first taught. |
| `/intro-python/placement/` (Phase 5) | `src/app/intro-python/placement/page.tsx` | Runs unit test-outs in order and stops at the first one not passed. Ends with "Start at Unit N". |
| `/intro-python/layout.tsx` | | Breadcrumb (`Intro to Python › Lists › Intro to Lists`), the `CourseSettingsProvider` (help options), and the join bar. |

```ts
// src/app/intro-python/[unitId]/[itemId]/page.tsx
export const dynamicParams = false;
export function generateStaticParams() {
  return introPython.units.flatMap((unit) => unit.items.map((item) => ({ unitId: unit.id, itemId: item.id })));
}
export default async function ItemPage({ params }: { params: Promise<{ unitId: string; itemId: string }> }) {
  const { unitId, itemId } = await params;
  const { unit, item, glossary } = pickItem(unitId, itemId);   // registry, server side
  return <ItemPlayer unit={unitMeta(unit)} item={item} glossary={glossary} outline={courseOutline} settings={introPython.settings} />;
}
```

Navigation changes:
- `layout.tsx` gets `<Link href="/intro-python">Intro to Python</Link>` between Play and Author. Next
  `Link` adds `basePath` itself. e2e finds it by role and name, like the existing nav links.
- The home page gets a small callout above the module list: "New to Python? Learn it with Mar'tu first."
  It links to the course and carries `data-testid="intro-python-callout"`. Existing `module-list` tests
  don't change.
- Unpublished units show only with `?preview=1`, mirroring `lessonsFor(module, preview)`. The flag is read
  client-side, because static pages can't vary by query string. The page always exists, and the client
  hides unpublished content unless preview is on.
- **Locking (recommendation).** Units and items stay open, with a highlighted "Next up". Exercises inside
  a lesson open in order: Next unlocks on pass, and any exercise already reached can be revisited from the
  exercise rail. Test-out is the sanctioned way to skip. See Q1.

---

## 3. UI layout and components

### 3.1 Exercise screen (lesson, project, challenge, article try-it)

Two columns from 1100px wide, because a Chromebook at 1366px fits both. Below that, one column in the
order Learn, Editor, Console. It uses a wider container than `.column`'s 1040px: `.course-column`,
`min(1400px, 100% - 32px)`.

```
Intro to Python › Lists › Intro to Lists                Exercise 3 of 9   [Help options]
┌ LEARN (scrolls on its own) ───────────────┐ ┌ EDITOR (PythonEditor) ────────────────────┐
│ [Mar'tu 96px] "A list keeps many values…" │ │                                           │
│   (🔊 Read aloud) (Explain it another way)│ │                                           │
│ Worked example ─ [Run example] [Step thru]│ │                                           │
│   hours = [48, 48, 47]   →  48            │ ├───────────────────────────────────────────┤
│ INSTRUCTIONS                              │ │ [Run] [Reset] [Step through my code]      │
│ ✓ 1. Make a list called `chalk_wall` …    │ │                [Compare with Mar'tu's…]   │
│ ● 2. Print the first hour.                │ ├ CONSOLE (ConsolePanel) ───────────────────┤
│     ✗ Read it from the list with …        │ │ output / plain-language explainer         │
│     [Get a hint (1 of 3)]                 │ │ pass line ("Gearshift: Math checks out.") │
│ ○ 3. …                                    │ └───────────────────────────────────────────┘
│ ▸ Lucky's side quest (optional)           │
│ ▸ What's in it for me? (campaign link)    │
│ [Back]                         [Next ▶]   │
└───────────────────────────────────────────┘
```

- **Checkpoint states** use icons and text, not colour alone: ✓ passed, ● active, ○ locked. Each has
  `data-state`, and results are announced through `aria-live`.
- The failing check's message shows under the active checkpoint, the way Codecademy does it. The console
  keeps stdout, the explainer and the pass line. The course calls `ConsolePanel` with
  `failedChecks={[]}`, so messages don't show twice.
- **Hint ladder.** One rung opens per click, with copy such as "Mar'tu leans closer…". The depth is
  recorded in the save. Under `support: "light"`, the ladder unlocks after the first failed Run.
- **Solution gating.** "Compare with Mar'tu's version" appears after *any* of these:
  - `settings.solutionAfter.minutes` on the exercise (default 5, counted the same way as the campaign's
    5-minute timer),
  - N failed runs,
  - the active checkpoint's hint ladder used up.
  
  It opens a read-only side-by-side line diff (a small LCS in `src/lib/course/diff.ts`; no dependency).
  The student can then **Retype it** (recommended) or **Replace my code**. Either way the checkpoints
  passed afterwards are marked `assisted`.
- **Encouragement as scaffolding.** After 3 failed runs on one checkpoint, Oogrish adds one line: "Steady,
  now. Read the last line of the error first." It points to the explainer; it isn't decoration.
- **Fun, bounded.** Cameos are one line each, with a 64×64 sprite from `public/sprites/`:
  - pass lines: Bomb Shell "Works.", Gearshift "Math checks out.", Oogrish "Steady hands.",
  - Lucky's "What's in it for me?" box, which holds the campaign link,
  - side quests, credited to a party member.
  
  Calm mode in Help options hides cameos. Course-map progress is drawn as **chalk tallies on Mar'tu's
  wall**, one per finished lesson, which fits the lore.

### 3.2 Other item screens

| Kind | Layout |
| --- | --- |
| Quiz | One question per card. The student moves forward and back, then presses Submit, which **delays feedback** (research §1.3). The score shows next, then a review that gives `explain` and `whyWrong[choice]` for each question and links "Review this" back to `teaches`. Retakes are unlimited, and choice order is shuffled with a seed. A score of at least `readyPercent` shows a "Ready" badge and never blocks anything. mc, predict and fill grade with no Python, so the quiz works while Pyodide loads. Parsons and bug questions run in the worker. |
| Project | The same `ExercisePlayer`, with checkpoints rendered as a **task checklist** under `taskGroups` headings. Every task is auto-checked. Stretch goals are optional and self-ticked when they have no checks. Default `support: "light"`. |
| Challenge | Shows the signature and a test table: each visible test with call, expected and got, then "3 of 5 hidden tests pass". A failed hidden test names its `label` ("an empty list") rather than its values. Core and advanced variants are linked. |
| Article | `RichText` body plus runnable examples (`WorkedExample`). Optional try-it exercises use `ExercisePlayer`. "Mark as read" completes it. |
| Cheatsheet | Concept, a code snippet, its output, and a note, styled as a parchment page. `@media print` hides the header, nav and join bar. Each entry links back to the exercise that taught it. |
| Test-out | A short quiz, then 1–3 code tasks with `support: "none"`: no hints, no another-way, no tracer, no solution. The result shows which lessons each task `covers`. A pass marks the unit **Tested out** and suggests side quests. A fail lists the lessons to visit. |

### 3.3 Reuse and new components

| Reuse as is | Small additive change | New (`src/components/course/`) |
| --- | --- | --- |
| `ConsolePanel` | `PythonEditor`: optional `readOnly`, `highlightLine` and `minHeight` props for the tracer and compare views | `CourseMap`, `UnitOverview`, `ItemPlayer` (kind switch) |
| `Theater` (unit intro banner) | `Instructions` / `instructions.ts`: `richBlocks()` adds fenced code blocks and `[[term]]` inline parts. Existing behaviour and tests are unchanged. | `ExercisePlayer`, `ExerciseRail`, `CheckpointList`, `HintLadder`, `WorkedExample`, `SolutionReveal` |
| `explainPython` | `explain.ts`: new cases for the course's step-limit error, `EOFError` (asked for more `input()` than provided), `UnboundLocalError`, `RecursionError`, and the `can only concatenate str (not "int")` message (hint: `str()`). The 3.13 "Did you mean" is surfaced. | `MartuSays` (portrait + speech box, reusing `.dialogue-box` / `.dialogue-portrait` CSS), `RichText`, `GlossaryTerm` |
| `pythonAdapter`, `whenPythonReady`, `PythonTimeoutError` | `languages/types.ts`: `RunInput` gains optional `stdin`, `prelude: "campaign" \| "course" \| "course+engine"`, `stepBudget`, `seed`, `interactiveInput` | `QuizPlayer` + `questions/{MultipleChoice,Predict,FillIn,Parsons,FixBug}` |
| `useReducedMotion`, `publicPath`, `pagePath` | Move `SOLUTION_DELAY_MS` into `src/lib/lesson/timing.ts`. Importing it from `Player.tsx` would pull the whole Player into course bundles. | `ChallengeTests`, `ArticleView`, `Cheatsheet`, `TestOutPlayer` |
| `.dialogue-*`, `.inline-code`, `.toolbar`, `.reset-confirm` CSS | `ModulePicker`: the callout | `CodeTracer`, `ReadAloudButton`, `HelpOptions`, `JoinBar` (+ `src/lib/classroom/session.ts`, which takes the join and fetch-or-local logic out of `Player`. Player can adopt it later in its own PR.) |

`JoinBar` reuses the `emberkeep-student` localStorage key. A student who already joined for the campaign
is joined in the course automatically.

### 3.4 data-testids (kebab-case, matching `module-card-${id}` and `begin-${id}`)

- **Course map and unit pages:**
  - `course-map`, `unit-card-<unitId>`, `unit-status-<unitId>` (text: Not started / 3 of 7 / Complete /
    Tested out), `milestone-<id>`, `item-link-<itemId>`, `item-status-<itemId>`
  - `testout-start`, `cheatsheet-link`, `intro-python-callout`
- **Exercise screen:**
  - `exercise-label` ("Exercise 3 of 9"), `exercise-rail`, `martu-says`, `read-aloud`
  - `another-way`, `another-way-text`, `worked-example`, `example-run`, `example-output`
  - `checkpoint-<n>` (with `data-state`), `checkpoint-message-<n>`, `hint-button-<n>`, `hint-<n>-<k>`
  - `solution-offer`, `solution-compare`, `solution-retype`, `solution-replace`
  - `exercise-next`, `exercise-back`, `side-quest`, `campaign-link`
- **Other item screens:**
  - quiz: `quiz-question-<n>`, `quiz-choice-<n>-<k>`, `quiz-submit`, `quiz-score`, `quiz-review`,
    `quiz-retake`
  - project, challenge, cheatsheet: `project-task-<n>`, `challenge-tests`, `challenge-hidden-summary`,
    `cheatsheet`
  - test-out: `testout-result`
- **Accommodations:**
  - `tracer-open`, `tracer-next`, `tracer-prev`, `tracer-step-label`, `tracer-line`, `tracer-vars`,
    `tracer-output`
  - `glossary-term`, `glossary-popover`, `help-options`, `stdin-prompt`, `stdin-answer`
- **Reused with the same meaning:** `run`, `editor`, `console`, `stdout`, `explainer`, `explainer-hint`,
  `traceback`, `reset-code`, `reset-confirm`, `python-status`, `autosave-status`, `resumed`, `join-form`,
  `join-status`, `feedback`.

---

## 4. Running and grading code

### 4.1 Checkpoint grading on the existing worker

- **Request.** The client flattens the checkpoints into one list:

  ```ts
  checks: exercise.checkpoints.flatMap((cp) => cp.checks)
  ```

  and keeps a parallel `groupOf[]` index. The worker already runs every check in order in the same
  namespace and returns one result per check, so grouping needs **no worker change**.
- **`gradeCheckpoints(exercise, result, earned)`** in `src/lib/course/grading.ts` is pure and unit-tested.
  It returns:

  ```ts
  { states: ("passed" | "active" | "locked")[]; activeIndex: number | null; message: string | null;
    allPassed: boolean; regressed: string[] }
  ```

- **Grading rules:**
  - Results are grouped by checkpoint. The first group with a failure is `active`. Groups before it are
    `passed`, and groups after it are `locked`, even if they would pass. This is Codecademy's in-order rule.
  - If `result.ok` is false (the student's code crashed), nothing is graded. The first checkpoint not yet
    earned becomes active, with the message "Your code stopped with an error before Mar'tu could check it.
    Read the console." The explainer handles the traceback.
  - Message cleanup (`checkpointMessage(raw)`):
    - strip a leading `AssertionError: `,
    - turn a `NameError` raised *inside a check* into "I looked for `chalk_wall` but could not find it.
      Did you name it exactly `chalk_wall`?",
    - show other exception types as "While checking, Python hit TypeError: …".
  - Every Run re-checks every checkpoint. A checkpoint earned before that now fails is listed in
    `regressed` ("Checkpoint 1 passed before, but your last change broke it"). The exercise is
    **complete** only when a single Run passes every checkpoint, so the saved solution is a working one.
- Checks run after the code finished cleanly, exactly as now. `_captured_stdout` is set before the checks,
  same as the campaign and the harness.

### 4.2 Course prelude, helpers, `input()`, and the step budget

- **Worker changes.** The worker fetches `course_helpers.py` and `tracer.py` (via
  `new URL("./…", import.meta.url)`) inside `boot()`, *before* it replaces `globalThis.fetch`. It caches
  their text. A run message's `prelude` field picks what goes into the fresh globals:
  - `"campaign"` (the default, and what happens today): `GUARD`.
  - `"course"`: the import-guard part of GUARD, then `course_helpers.py`. To make this split possible,
    take the 13-line `_guard` block out into its own constant `IMPORT_GUARD`. GUARD then becomes
    IMPORT_GUARD plus the engine objects. Both stay plain text, so the `run-checks.ts` rule still holds.
  - `"course+engine"`: GUARD, then `course_helpers.py`. Rehearsal exercises use this, so they call
    `party.move`, `print_prompt` and `print_mana`, and checks read `_prompts`, `party._moves` and
    `_mana_prints`, exactly like the campaign.
- **`course_helpers.py`** defines:
  - `_lines()`, `_uses(token)`, `_count(token)`, `_assigned_from_expression(name)`, `_inputs_used()` and
    `_concept_tokens(code)`, all taken from the harness so a check behaves the same in all three places,
  - `_eq(a, b)` for challenge tests (float tolerance; type-aware messages),
  - `_source`, which the worker sets to the code about to run.
- **Scripted `input()`.** `_set_stdin(list)` installs the harness's `_fake_input`, which echoes the prompt
  and the answer so the console reads like a terminal. When the answers run out it raises
  `EOFError("The program asked for more input than this exercise provides.")`, the same text the harness
  uses.
- **Interactive `input()`** (the input() article, free play, the Hello World input lesson):
  - Use a **replay** design. It needs no SharedArrayBuffer, so it works on GitHub Pages, where we can't
    set COOP/COEP headers.
  - When the answer queue is empty and `interactiveInput` is on, the shim raises `_NeedInput(prompt)`.
    The worker returns `{ok: false, needsInput: {prompt}}`.
  - The console shows the prompt and an answer box (`stdin-prompt`, `stdin-answer`). On Enter, the client
    re-runs the whole program with the answers so far.
  - Each Run uses one fixed `seed` for `random.seed(...)` across its replays, so a random program behaves
    the same at every step.
  - Checks run only on the final, complete replay.
- **Step budget** (course runs only):
  - `course_helpers.py` installs a counter before the student code and removes it before the checks. Each
    check is wrapped separately in `_limited(…)` with its own smaller budget.
  - Preferred mechanism: `sys.monitoring` (3.12+, which Pyodide 0.28 has), counting `JUMP` events
    (backward jumps, which are loop iterations). That costs much less than per-line tracing.
  - Fallback: `sys.settrace` counting `line` events.
  - When the budget runs out, it raises `TooManySteps("Line 4 ran 200,000 times. Is this loop's condition
    ever False?")` with the line of the hottest jump. `explain.ts` turns that into a plain explanation.
  - The 5-second kill-and-restart stays as the backstop, for C-level hangs and huge strings.
  - Phase 0 spike: measure the overhead on a Chromebook-class machine and choose the default budget.

### 4.3 Step-through code tracer (Python Tutor-style)

- **Message.** `{type: "trace", code, setup, stdin, seed, prelude, maxSteps: 400}` runs `tracer.py`
  (fetched like the helpers).
- **What `tracer.py` does:**
  - Compiles the code with `compile(src, "<student>", "exec")`.
  - Swaps `sys.stdout` for a `StringIO`.
  - Installs `sys.settrace`. The global trace function returns the local tracer only for frames whose
    `f_code.co_filename == "<student>"`, so prelude, helpers and engine calls are never shown.
  - On each `line`, `call`, `return` and `exception` event it records:

    ```ts
    { event, line, stack: ["<module>", "cast_spell"], frames: [{ name, vars: { x: VarView } }], stdoutLen }
    ```

  - Module-level variables are the globals minus a baseline snapshot taken before the exec, minus names
    starting with `_`, minus functions and modules (those show as `function cast_spell(caster, spell_name)`).
  - `VarView = { type, repr }` with repr cut at 60 characters. Lists, tuples and dicts go 2 levels deep,
    at most 12 items, so they can be drawn as "memory boxes".
  - It stops at `maxSteps` and sets `truncated: true`. A final exception step records the error, which
    makes it useful for the Errors lesson.
  - It returns `{steps, stdout, truncated, error}`.
- **UI (`CodeTracer`):**
  - A read-only `PythonEditor` with `highlightLine`, plus Prev, Next and a scrubber ("Step 12 of 57").
  - A variables panel showing new and changed values with a marker (not colour alone), and a call stack.
  - Output up to this step (`stdout.slice(0, step.stdoutLen)`).
- **Entry points:** "Step through" on worked examples where `tracer: true`, and "Step through my code"
  (the student's current code). Both are hidden under `support: "none"`.
- **Risks and mitigations:**
  - (a) Overhead: fine at 400 steps, so cap it there.
  - (b) Infinite loops are cut off by `maxSteps`, and a note says so.
  - (c) `random` and `input()`: seed and stdin are passed, with a note that "a traced run may roll
    different numbers than your last Run" when the seed differs.
  - (d) Comprehensions are inlined since 3.12 (PEP 709), so they show as repeated steps on one line.
    Fine, and it should be said in the Loops unit.
  - (e) Aliasing, two names pointing at one list, is not drawn in v1. Show `id`-based "same list as
    `party`" labels later if students need it.
  - (f) In 3.13, `f_locals` is a write-through proxy (PEP 667). The tracer only reads it, and copies every
    value through `_view`, so later mutation can't change past steps.
  - (g) The tracer never runs checks, so it can't leak hidden challenge tests.
  - (h) Line numbers: the tracer shows the exact code it ran, so it can't drift from formatting.

### 4.4 Challenges with hidden tests

`challengeChecks(tests)` in `src/lib/course/challenge.ts` compiles each test into a check. Runtime,
vitest and the exporter all share this one function.

```python
_got = _limited(lambda: <call>, 20000)
assert _eq(_got, <expect>), "<label>: <call> should return <expect>, but it returned " + repr(_got)
```

- Hidden tests use the message `"<label>: not yet"`. The UI shows only the label.
- A per-test budget turns an infinite loop into "test 3 ran too long" without killing the worker.
- The test table's "got" column comes from the check message. Visible tests return structured
  `{expected, got}` JSON in the message so the UI can parse it.

### 4.5 Quiz grading (client-side, `src/lib/course/quiz.ts`)

| Type | How it's graded |
| --- | --- |
| mc | `response === answer`. |
| predict | Compare `normalizeOutput(response)` with `normalizeOutput(answer)` and `accept`, where `normalizeOutput` trims trailing spaces on each line and outer blank lines, mirroring the harness `_norm`. A parity test checks fixtures against Python. If `choices` exist, the "Show choices" accommodation turns free text into multiple choice. |
| fill | Trimmed match against `answer` or `accept`. With `chips`, the student taps tokens instead of typing. |
| parsons | Assemble the chosen lines, with indentation when `indent: true`, run them in the worker (`prelude: "course"`, no checks), and compare normalized stdout to `expectedOutput`. Any order that produces the output is accepted, and a distractor that changes the output fails. |
| bug | The student edits in a small `PythonEditor`. It is graded by running: output must equal `expectedOutput`, and the optional `checks` (for example, "didn't just print the answer") must pass. |

- The score is `correct / total`.
- The best score and the last answers go into the save.
- Answers ship in the page payload. That is acceptable for ungraded practice (Q5).
- For test-out quizzes, mc, predict and fill can store `answerHash` (SHA-256 of the normalized answer)
  instead of `answer`, which stops casual "view source". Test-out explanations are shown only after
  submitting.

### 4.6 Worked examples and article examples

"Run example" sends `{type: "run", code: example.code, checks: [], prelude: "course", stdin}` and shows
the result in `example-output`, separate from the main console. Tests prove that `example.output` is
exactly what it prints.

### 4.7 Formatting policy

- The course passes `formatPolicy: "off"` by default. A "Tidy my code" button stays available.
- If the teacher wants auto-format (Q9), it has to use `quote-style: "preserve"` and must stay off for the
  Strings unit and the Errors lesson. Today's double-quote setting rewrites `'It\'s'` to `"It's"`, which
  breaks escape checkpoints and confuses novices.
- The campaign keeps its current policy.

---

## 5. Progress, autosave, and classroom

### 5.1 Local save (`src/lib/course/progress.ts`, pure, tested like `autosave.ts`)

- One key, `intro-python:v1`.
- One zod-validated record, with everything keyed **by id**, so content edits never break a save. This is
  the same principle as `autosave.ts`.

```ts
{
  version: 1, savedAt,
  items: { "<unitId>/<itemId>": {
      status: "not_started" | "in_progress" | "completed",
      exercises: { "<exerciseId>": {                 // projects/challenges use exerciseId "main"
          code?: string,                              // omitted while equal to the starter (as autosave does)
          earned: string[],                           // checkpoint ids ever passed
          completed: boolean, assisted: string[],     // checkpoints passed after a solution reveal
          hints: Record<string, number>,              // ladder depth per checkpoint
          failedRuns: number, solutionRevealed: boolean, msSpent: number,
          bonusDone?: boolean } },
      lastExercise?: string,
      quiz?: { best: number, attempts: number, last: Record<string, unknown> },
      read?: boolean } },
  units: { "<unitId>": { testOut?: { attempts: number, passed: boolean, bestPercent: number, passedAt?: string } } },
}
```

- **Derived state.** Pure functions compute it from the outline, never store it:
  - `exerciseDone`, `itemDone` (required items only),
  - `unitStatus`: `tested_out` if the test-out passed, otherwise `completed`, `in_progress` or
    `not_started`,
  - `milestoneReady`.
  
  Content added later then counts correctly.
- **Writes.** Debounced to 400 ms, flushed on `pagehide` and `visibilitychange`, and failures show in
  `autosave-status`. These are the same constants and patterns as `Player`, factored into a
  `useCourseProgress()` hook.
- **Reading on the map.** The map and unit pages read the save after mount. The server render shows
  neutral states, which avoids hydration mismatches.
- **Help-option settings** go in their own key, `intro-python:settings`, and are never sent to the
  classroom.
- **"Welcome back! You are right where you left off."** reuses the `resumed` testid when an item reopens
  with saved code.

### 5.2 Classroom integration (teacher sees course progress and test-out status)

- **Data.** A new table in `store.ts`. It does not touch the campaign's `progress` table or report.

  ```sql
  CREATE TABLE IF NOT EXISTS course_progress (
    student_id TEXT NOT NULL, classroom_id TEXT NOT NULL,
    course_id TEXT NOT NULL, unit_id TEXT NOT NULL,
    summary TEXT NOT NULL,            -- JSON validated by unitSummarySchema (.strict)
    updated_at TEXT NOT NULL,
    PRIMARY KEY (student_id, course_id, unit_id),
    FOREIGN KEY (student_id) REFERENCES students(id)
  );
  ```

- **`unitSummarySchema`** (`.strict()`). The privacy test asserts it rejects `name`, `displayName` and
  `student`.

  ```ts
  {
    status: "not_started" | "in_progress" | "completed" | "tested_out",
    itemsDone, itemsRequired, exercisesDone, exercisesTotal,
    frontier: { itemId, exerciseId } | null,
    testOut: { attempts, passed, bestPercent } | null,
    quizzes: Record<string, number>,
    hintsShown, solutionsRevealed, assistedCheckpoints, bonusDone,
    stuck: [{ itemId, exerciseId, checkpointId, failedRuns, hints }]   // at most 3
  }
  ```

  **No code and no free text is sent.**
- **API (server mode):**
  - `POST /api/course-progress` with `{studentId, courseId, unitId, summary, preview}`. `preview` is
    ignored, as `/api/progress` does today.
  - `GET /api/classroom/course-report?code=&course=intro-python`.
  - Both are `route.ts` files, so the static export drops them automatically.
- **Static export.** `local-store.ts` gains `courseProgress: []` in its database, plus
  `saveCourseSummaryInBrowser` and `courseReportInBrowser`. This is the same-browser behaviour the
  classroom page already explains.
- **When the summary is sent:**
  - when an exercise completes, a quiz is submitted, a test-out finishes, or a unit's status changes,
  - debounced, and only for the unit that changed,
  - never on keystrokes.
  
  Joining sends a summary for every unit that has local progress, the same idea as
  `reportLocalProgress`.
- **Classroom page.** A new "Intro to Python" section (`data-testid="course-report"`):
  - one row per student (`course-report-row`) and one column per unit (`course-cell-<unitId>`),
  - each cell reads "Tested out", "Complete", "5 of 9" or "—", and its `title` gives detail (quiz bests,
    hints, reveals),
  - an optional "Where the class is stuck" list, built from the `stuck` entries.
  
  The report shows hints and reveals neutrally. Wording such as "hints used" rather than "cheated" is a
  Q10 conversation.
- **Email.** No course emails by default, because 8 units × 30 students would be noise. An opt-in "email
  me when a student tests out or finishes a unit" is Q10.
- **Cross-device resume** (Phase 6, optional). Add a `course_saves(student_id, course_id, save_json)` table
  and restore it on join in server mode. Static mode gets "Download / load my progress file" instead
  (Q4).

---

## 6. Testing strategy (mirrors the repo: vitest + CPython, Playwright, CI)

### 6.1 Runner extensions (`src/lib/lesson/run-checks.ts`)

- `runPythonChecks(code, checks, { setup, calls, stdin, prelude: "campaign" | "course" | "course+engine", stepBudget })`.
  The RUNNER builds the same prelude as the worker by reading `IMPORT_GUARD`, `GUARD`,
  `course_helpers.py` and `tracer.py` from `public/workers/`.
- `runPythonBatch(jobs[])` runs many jobs in **one** `python3` process. It isolates each job in a fresh
  namespace and gives each a timeout through `signal.alarm`. This keeps about 1,000 course runs to a few
  seconds.
- CI: add `actions/setup-python@v5` with `python-version: "3.13"` before `npm test`, to match Pyodide
  0.28's CPython.

### 6.2 Unit tests (new files under `src/lib/course/`)

| File | What it proves |
| --- | --- |
| `schema.test.ts` | Every unit parses, and the registry imports every `units/*.json` file. Ids are unique, with no route collisions. Banner and sprite art exist (`public/…`). Every `[[term]]` resolves and every glossary term is used. Every exercise has a solution, and every checkpoint has at least 2 hints. **Writing rules** from `docs/campaign/README.md`: backticks balanced, checkpoint text has no leading `N. ` (the UI numbers checkpoints), one action per checkpoint (at most 2 sentences), check messages are one sentence (the `failSentences` idea from `beginner.test.ts`). Reading load stays under hard ceilings: Mar'tu text ≤ 300 words, Flesch-Kincaid grade ≤ 10. The harness's softer warnings stay warnings. |
| `solutions.test.ts` | The port of `verify_exercise`, for every exercise, project, challenge, test-out task and article try-it. (a) The **solution passes every checkpoint**. (b) The **starter fails at least one**, unless `starterPasses`. (c) Partial k passes checkpoints 1..k and fails k+1. (d) **Every known wrong answer fails at its `failsAt` checkpoint, with a message containing `messageContains`.** (e) The example prints exactly `example.output`. (f) The bonus solution passes the bonus checks, and the plain solution does not. (g) Challenge `tests` compile, and an infinite-loop wrong answer is reported as "ran too long", not as a hang. |
| `quiz-keys.test.ts` | Executes every predict, fill (answer + accept), parsons (ordered lines) and bug (fix passes; buggy code doesn't produce `expectedOutput`) item. Article examples and cheatsheet entries print their stated output. |
| `concepts.test.ts` | Port of `ConceptGate`. In course order, no code a student *sees* uses a concept token that hasn't been introduced: starter, solution, example, partials, quiz code, cheatsheet. `preview` lists the exceptions. |
| `grading.test.ts` | `gradeCheckpoints` covers the in-order rule, the crash case, regressions, and message cleanup (`AssertionError:` stripped; NameError inside a check made friendly). |
| `quiz.test.ts` | The pure grading functions, seeded shuffle stability, and `normalizeOutput` parity with Python `_norm` on fixtures. |
| `progress.test.ts` | Save and restore by id, behaviour after content edits (removed exercise, renamed checkpoint), completion rules, test-out → `tested_out`, assisted marking, summary building, size bound (< 300 KB for a full course of code). |
| `tracer.test.ts` | Runs `tracer.py` in CPython: the steps for a 3-iteration loop, function call and return frames, `maxSteps` truncation, an exception step, prelude frames hidden. |
| `input.test.ts` | The scripted-stdin echo, the EOFError text, the `_NeedInput` replay protocol, and the same seed giving identical replays. |
| `bundle.test.ts` | No client course component imports the registry, and no client file imports `*.verify.json`. |
| `diff.test.ts` | The line diff used by Compare. |
| Changes to existing tests | `instructions.test.ts`: `richBlocks` (code fences, `[[term|text]]`), with old cases unchanged. `explain.test.ts`: the new error cases. `store.test.ts` / `local-store.test.ts`: course summaries and report. `privacy.test.ts`: the summary schema rejects name fields, and the walk already covers `content/`. |

### 6.3 e2e (`e2e/intro-python.spec.ts`, with helpers in `e2e/course.ts`; reuses `pythonReady` and `replaceEditor`)

1. The nav link "Intro to Python" leads to the course map. Mar'tu's opening line shows, and `unit-card-hello-world` is visible.
2. The exercise loop:
   - Run the starter, and `checkpoint-1` reaches `data-state="active"` with its message.
   - `hint-button-1` opens `hint-1-1`, then `hint-1-2`.
   - Type the solution, Run, and every checkpoint is `passed`.
   - `exercise-next` reaches exercise 2.
3. Autosave: reload, and the code and checkpoint states come back with `resumed` visible.
4. Quiz: answer, submit, and `quiz-score` and `quiz-review` show the explanation. Retake reshuffles.
5. Test-out: pass Unit 1's test-out, and the map's `unit-status-hello-world` reads "Tested out".
6. Tracer: on an exercise with `tracer`, Next steps until `tracer-vars` shows `chalk_wall`.
7. `input()`: interactive replay. `stdin-prompt` appears, the student answers, and the output shows the echo.
8. An infinite `while` loop shows the friendly step-limit explainer with a line number, and `run` stays
   enabled with no worker reload.
9. Classroom: create a class, join from the course, finish an exercise, and `/classroom?code=…` shows
   `course-cell-hello-world` with progress.

Static export smoke, after the existing `npm run build:pages`: a CI step asserts that
`out/intro-python/index.html` and one item page exist, and that each item page's HTML contains no other
unit's solution text (a cheap check on bundle hygiene).

---

## 7. Phased implementation plan

Rough sizes are lines of code including tests and excluding course content. Each phase is one PR, green in
CI, and leaves the site shippable. Unpublished units stay hidden until the teacher flips `published`.

| Phase | Scope | Files (new unless marked ±) | Size |
| --- | --- | --- | --- |
| **0. Spikes** (1–2 days, no product code) | Loop-budget overhead in Pyodide (`sys.monitoring` vs `settrace`) on a Chromebook-class machine. Input replay. Tracer at 400 steps. Ruff `quote-style: "preserve"`. RSC payload size per item page. | `docs/intro-to-python/spikes.md` (findings only) | — |
| **1. Content core and grading** | Schema, registry, outline, exporter, course helpers, worker prelude modes, scripted stdin, step budget, test runner batch, verification tests. Unit 1 exported. | `src/lib/course/{schema,registry,outline,grading,challenge}.ts` · `public/workers/course_helpers.py` · ± `public/workers/python-worker.js` (+~110) · ± `src/lib/languages/{types,python/run}.ts` (+~30) · ± `src/lib/lesson/run-checks.ts` (+~90) · `scripts/course/export_prototypes.py` · ± `docs/intro-to-python/prototypes/harness.py` (reads helpers) · `content/courses/intro-python/{course,glossary}.json`, `units/hello-world{,.verify}.json` · tests: `schema`, `solutions`, `quiz-keys`, `concepts`, `grading`, `bundle` · ± `.github/workflows/ci.yml` (setup-python 3.13) | ~1,700 |
| **2. Routes and the exercise loop** | Nav link, course map, unit page, item page (lessons), Learn pane, checkpoints, hint ladder, another-way, worked example, solution compare, autosave, join bar, callout, CSS. | `src/app/intro-python/{layout,page}.tsx`, `[unitId]/page.tsx`, `[unitId]/[itemId]/page.tsx` · ± `src/app/layout.tsx` · `src/components/course/{CourseMap,UnitOverview,ItemPlayer,ExercisePlayer,ExerciseRail,MartuSays,RichText,CheckpointList,HintLadder,WorkedExample,SolutionReveal,JoinBar}.tsx` · `src/components/course/useCourseProgress.ts` · `src/lib/course/{progress,diff}.ts` · `src/lib/classroom/session.ts` · `src/lib/lesson/timing.ts` · ± `src/lib/lesson/instructions.ts` · ± `src/components/{ModulePicker,PythonEditor}.tsx` · ± `src/app/globals.css` (+~400) · `e2e/intro-python.spec.ts`, `e2e/course.ts` | ~2,300 |
| **3. The other item kinds** | Quiz (5 types, delayed review), project checklist and stretch goals, challenge test table, article, cheatsheet (print), interactive `input()` replay. | `src/components/course/{QuizPlayer,ChallengeTests,ArticleView,Cheatsheet,StdinPrompt}.tsx`, `questions/*.tsx` · `src/lib/course/quiz.ts` · ± worker (`needsInput`) · ± `explain.ts` · tests: `quiz`, `input`, `explain` · e2e additions | ~1,700 |
| **4. Classroom** | Course summaries in both stores, API routes, report section, summary builder. | ± `src/lib/classroom/{store,local-store}.ts` (+~170) · `src/app/api/course-progress/route.ts` · `src/app/api/classroom/course-report/route.ts` · ± `src/app/classroom/page.tsx` (+~110) · `src/lib/course/summary.ts` · tests (store, local-store, privacy) · e2e classroom case | ~800 |
| **5. Accommodations** | Tracer, glossary popovers and page, read-aloud (Web Speech API), Help options drawer (read-aloud, bigger text, easy-read font such as Atkinson Hyperlegible through `next/font`, fast lane, calm mode, show choices), test-out player, placement page, side-quest UI. | `public/workers/tracer.py` · ± worker (`trace`) · `src/components/course/{CodeTracer,GlossaryTerm,ReadAloudButton,HelpOptions,TestOutPlayer,SideQuest}.tsx` · `src/app/intro-python/{glossary,placement}/page.tsx` · `src/lib/course/settings.ts` · tests: `tracer`, more `progress` · e2e test-out and tracer | ~1,900 |
| **6. Content rollout and docs** | Export and review the remaining units, teacher review passes, optional cross-device resume, authoring guide. | `content/courses/intro-python/units/*.json` (+ verify) · `docs/intro-to-python/README.md` (authoring rules in the campaign README style) · ± `docs/campaign/README.md` (link) | content-bound |

Order note: the accommodations most tied to the core loop ship in Phase 2, because they are cheap and
central: the hint ladder, "explain it another way", and solution gating. Phase 4 can come before Phase 3
if the teacher wants visibility first.

Content volume, for scale: about 8 units, about 14 lessons, about 120–150 exercises, about 400 checkpoints,
about 13 quizzes, about 10 projects, and optional challenges. At roughly 6 Python runs per exercise for
verification, `runPythonBatch` is what keeps `npm test` fast.

---

## 8. Risks and open questions for the teacher

**Decisions needed (with my recommendation):**
1. **Locking.** Should units be open with a recommended path, or locked in order? *Recommend open units
   and items, exercises in order within a lesson, and test-out as the way to skip.*
2. **Solution reveal timing.** 5 minutes (as in the campaign), *or* 4 failed runs, *or* hints used up,
   whichever comes first? Should the teacher see reveal counts? *Recommend yes, shown neutrally, with
   "Retype it" as the default way to use a reveal.*
3. **Test-out rules.** Pass mark (all code tasks + 80% quiz?), retakes (unlimited, or one per day?),
   whether "tested out" counts as complete for reports, and whether students who tested out still get
   side quests. *Recommend unlimited retakes, a pass counted as complete, and side quests suggested.*
4. **Progress on shared Chromebooks.** On GitHub Pages, progress lives only in that browser, and guest
   mode wipes it. Is a "download / load my progress file" button acceptable, or is server mode
   (cross-device resume) needed?
5. **Answers in the page.** Quiz keys, checks and hidden tests are readable in page source on a static
   site. That is fine for ungraded practice, but test-out results should not be used as grades. You
   mentioned some students may get help, so treat test-out as a self-placement signal, not an assessment.
6. **Reading level target.** The harness warns above grade 9. Middle-school readers may need a target of
   grade 6–7 for Mar'tu's text. The accent ("…, yes?") has to stay light enough for read-aloud and
   English learners.
7. **Rehearsal versus spoilers.** How close may campaign-rehearsal exercises get to the real campaign
   tasks (`perform_roll`, `add_spell`, `cast_spell`) before they spoil the campaign? *Recommend
   near-transfer: the same helpers and shapes, with different names and data.*
8. **Placement entry.** Should the course map offer "Where should I start?" placement to everyone on the
   first visit, or only when the teacher enables it?
9. **Auto-format.** The campaign tidies code on Run. The course should not, or should only with
   `quote-style: "preserve"` (see §4.7). Is that acceptable?
10. **Teacher report detail and email.** Is a per-unit summary plus "where the class is stuck" enough?
    Should completion or test-out emails be sent (default off)?
11. **Authored source format.** Should JSON be canonical (recommended: matches campaign modules and needs
    no build step), or should the Python prototype files stay canonical, with generated JSON and a sync
    test? Python is easier to hand-edit for code-heavy content.

**Technical risks:**
- **Infinite loops and performance.** The step-budget overhead on low-end Chromebooks is unmeasured
  (Phase 0). The fallback is today's 5-second kill-and-reload.
- **Python version drift.** CI uses 3.12 by default and Pyodide uses 3.13, so error wording and features
  differ. Pinning CI to 3.13 removes most of it.
- **Read-aloud.** Web Speech voices vary by device and some may be missing offline. Detect the feature and
  hide the button when it's unavailable. Code read aloud punctuation by punctuation is clumsy, so consider
  an authored `say` text for key lines.
- **Engine names hide NameErrors.** `party`, `user` and `stage` would shadow NameError lessons. This is
  why the course uses its own prelude and `engine: true` is opt-in.
- **CodeMirror Tab.** `@uiw/react-codemirror` uses `indentWithTab`, so keyboard users need "Esc, then
  Tab" to leave the editor. Document this in Help options.
- **Content scale.** About 400 checkpoints, each needing at least 2 hints and behaviour-based,
  cumulative-safe checks, is the real cost. Tests catch broken keys, not unclear teaching, so plan
  teacher and student-rep review time per unit.
- **Privacy.**
  - The assessment PDFs and persona notes contain or are derived from real students. Keep them out of the
    repo; suggest a git-ignored `student-work/` folder.
  - `.verify.json` notes must never quote students.
  - Classroom summaries carry no names, code or free text. Display names stay where they are today,
    entered at runtime.
- **Original content only.** Codecademy is used for learning goals and structure only, never for text,
  values, project premises or quiz items. This needs review discipline, because no test can enforce it.
