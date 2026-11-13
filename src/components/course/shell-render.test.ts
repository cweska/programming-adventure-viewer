/**
 * Server-render smoke tests for the course shell (no DOM needed): what each page shows before
 * hydration, with empty progress, matches what students should see first.
 */
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { itemPageProps, unitOutline } from "../../lib/course/registry";
import { questionSchema, unitSchema, type GlossaryEntry, type QuizItem } from "../../lib/course/schema";
import { CheatsheetView } from "./CheatsheetView";
import { CourseMap, unitStatusText, type MapUnit } from "./CourseMap";
import { Prose } from "./Prose";
import { QuizPlayer } from "./QuizPlayer";
import { UnitPage } from "./UnitPage";

const glossary: GlossaryEntry[] = [{ term: "string", aliases: ["strings"], plain: "Text in `quotes`.", example: '"hi"' }];

function unit(id: string, order: number, published: boolean) {
  return unitSchema.parse({
    id,
    order,
    title: `Unit ${id}`,
    published,
    martuIntro: "Hi. It is me, Mar'tu.\nWe learn [[string|strings]] today.",
    goals: ["Print a [[string]]"],
    items: [
      {
        kind: "lesson",
        id: "first",
        title: "First steps",
        summary: "Print words.",
        minutes: 10,
        exercises: [
          {
            id: "e",
            title: "E",
            martu: "Go.",
            starter: "",
            checkpoints: [{ id: "s", text: "Go.", hints: ["a", "b"], checks: [{ name: "c", code: "assert True" }] }],
            solution: "print(1)",
          },
        ],
      },
      { kind: "cheatsheet", id: "notes", title: "Notes", entries: [{ concept: "Print", code: ["print(1)"], output: "1" }] },
      {
        kind: "testout",
        id: "quick-check",
        title: "Quick Check",
        exercises: [
          {
            id: "t",
            title: "T",
            martu: "Go.",
            starter: "",
            checkpoints: [{ id: "s", text: "Go.", hints: ["a", "b"], checks: [{ name: "c", code: "assert True" }] }],
            solution: "print(1)",
          },
        ],
      },
    ],
  });
}

function mapUnit(id: string, order: number, published: boolean): MapUnit {
  const parsed = unit(id, order, published);
  return { ...unitOutline(parsed), goals: parsed.goals };
}

describe("Prose", () => {
  it("renders lines, lists, code and glossary buttons", () => {
    const html = renderToStaticMarkup(
      createElement(Prose, {
        text: "Use `print()` with a [[string|strings]] and a [[loop]].\n1. Type it.\n```python\nprint(\"hi\")\n```",
        glossary,
      }),
    );
    expect(html).toContain('<code class="inline-code">print()</code>');
    expect(html).toContain('data-testid="glossary-term"');
    expect(html).toContain('aria-expanded="false"');
    expect(html).toContain(">strings</button>");
    expect(html).toContain("<span> and a </span><span>loop</span>"); // unknown terms are plain text
    expect(html).toContain('<ol class="prose-list"><li>');
    expect(html).toContain('<pre class="prose-code" aria-label="Python code"><code>print(&quot;hi&quot;)</code></pre>');
  });

  it("hides story lines in Fewer words mode and offers them back", () => {
    const html = renderToStaticMarkup(
      createElement(Prose, { text: "Hi. It is me, Mar'tu.\n`print()` shows words.", light: true }),
    );
    expect(html).not.toContain("It is me");
    expect(html).toContain("Show all the words");
  });
});

describe("CourseMap", () => {
  it("shows published units only (preview is read in the browser)", () => {
    const html = renderToStaticMarkup(
      createElement(CourseMap, {
        title: "Intro to Python",
        intro: "Hi. It is me, Mar'tu.",
        units: [mapUnit("hello", 1, true), mapUnit("draft", 2, false)],
        glossary,
      }),
    );
    expect(html).toContain('data-testid="course-map"');
    expect(html).toContain('data-testid="martu-says"');
    expect(html).toContain('data-testid="unit-card-hello"');
    expect(html).not.toContain("unit-card-draft");
    expect(html).toContain('data-testid="unit-status-hello">Not started<');
    expect(html).toContain('href="/intro-python/hello"');
    expect(html).toContain("Next up");
  });

  it("says so when no unit is published yet", () => {
    const html = renderToStaticMarkup(
      createElement(CourseMap, { title: "Intro", intro: "Hi.", units: [mapUnit("draft", 1, false)], glossary }),
    );
    expect(html).toContain('data-testid="course-empty"');
  });

  it("words unit status plainly", () => {
    const base = { done: 0, total: 3, percent: 0, testedOut: false, started: false, complete: false };
    expect(unitStatusText(base)).toBe("Not started");
    expect(unitStatusText({ ...base, started: true, done: 1 })).toBe("1 of 3 done");
    expect(unitStatusText({ ...base, started: true, done: 3, complete: true })).toBe("Complete");
    expect(unitStatusText({ ...base, testedOut: true, complete: true })).toBe("Tested out");
  });
});

describe("UnitPage", () => {
  it("lists items with kind badges and status, and offers the Quick Check up front", () => {
    const parsed = unit("hello", 1, false);
    const html = renderToStaticMarkup(
      createElement(UnitPage, {
        unit: { ...unitOutline(parsed), martuIntro: parsed.martuIntro, goals: parsed.goals },
        campaign: [{ id: "leylines-awaken", title: "Leylines Awaken" }],
        glossary,
      }),
    );
    expect(html).toContain('data-testid="unit-page"');
    expect(html).toContain('data-testid="unpublished-banner"');
    expect(html).toContain('data-testid="item-link-first"');
    expect(html).toContain('href="/intro-python/hello/first"');
    expect(html).toContain('data-testid="item-status-first"');
    expect(html).toContain(">Lesson<");
    expect(html).toContain(">Cheatsheet<");
    expect(html).toContain("Optional");
    expect(html).toContain("Already know this?");
    expect(html).toContain('href="/intro-python/hello/quick-check"');
    expect(html).not.toContain('data-testid="item-link-quick-check"');
    expect(html).toContain('href="/play/leylines-awaken"');
  });
});

describe("item views", () => {
  const settings = { solutionAfterMinutes: 5, solutionAfterFailedRuns: 4, quizReadyPercent: 70 };
  const summary = { id: "hello", order: 1, title: "Hello", items: [] };

  it("renders a quiz's first question with a Check button", () => {
    const item: QuizItem = {
      kind: "quiz",
      id: "quiz",
      title: "Chalk Quiz",
      optional: false,
      questions: [
        questionSchema.parse({ type: "mc", id: "q1", q: "Which one?", explain: "E.", choices: ["mana = 20", "A string"], answer: 0 }),
        questionSchema.parse({ type: "fill", id: "q2", q: "Fill it.", explain: "E.", code: "print(___)", answer: "1", expectedOutput: "1" }),
      ],
    };
    const html = renderToStaticMarkup(
      createElement(QuizPlayer, { unit: summary, item, glossary, nextHref: "/intro-python/hello", settings }),
    );
    expect(html).toContain('data-testid="quiz-question-q1"');
    expect(html).toContain("Question 1 of 2");
    expect(html).toContain('data-testid="quiz-choice-q1-0"');
    expect(html).toContain('<code class="quiz-choice-code">mana = 20</code>');
    expect(html).toContain('data-testid="quiz-check"');
    expect(html).not.toContain("quiz-question-q2");
  });

  it("renders a cheat sheet with a print button", () => {
    const parsed = unit("hello", 1, true);
    const item = parsed.items[1];
    if (item.kind !== "cheatsheet") throw new Error("expected a cheatsheet");
    const html = renderToStaticMarkup(
      createElement(CheatsheetView, { unit: summary, item, glossary, nextHref: "/intro-python/hello", settings }),
    );
    expect(html).toContain('data-testid="cheatsheet"');
    expect(html).toContain('data-testid="cheatsheet-print"');
    expect(html).toContain("print(1)");
  });

  it("renders every bundled quiz without crashing", () => {
    for (const props of [itemPageProps("sample", "chalk-quiz")]) {
      if (!props || props.item.kind !== "quiz") continue;
      const html = renderToStaticMarkup(createElement(QuizPlayer, { ...props, item: props.item }));
      expect(html).toContain('data-testid="quiz-check"');
    }
  });
});
