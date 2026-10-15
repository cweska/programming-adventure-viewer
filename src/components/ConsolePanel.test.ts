import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { Explanation } from "../lib/languages/types";
import type { FailedCheck } from "../lib/lesson/progression";
import { ConsolePanel } from "./ConsolePanel";

const explainer: Explanation = {
  title: "Syntax error",
  hint: "Look for a missing parenthesis.",
  raw: "SyntaxError: unexpected EOF while parsing",
};

function markup(props: {
  output?: string;
  explainer?: Explanation | null;
  feedback?: string | null;
  failedChecks?: FailedCheck[];
}) {
  return renderToStaticMarkup(
    createElement(ConsolePanel, {
      output: props.output ?? "",
      explainer: props.explainer ?? null,
      feedback: props.feedback ?? null,
      failedChecks: props.failedChecks ?? [],
    }),
  );
}

function indexOf(html: string, needle: string) {
  const index = html.indexOf(needle);
  expect(index, needle).toBeGreaterThanOrEqual(0);
  return index;
}

describe("console panel", () => {
  it("shows only the empty line before a program runs", () => {
    const html = markup({});
    expect(html).toContain("Program output will appear here.");
    expect(html).not.toContain('data-testid="console-divider"');
    expect(html).not.toContain('data-testid="feedback"');
  });

  it("draws a line between python output and story feedback", () => {
    const html = markup({
      output: "ember\n",
      feedback: "The wall shows ember.",
    });
    expect(html).not.toContain("Program output will appear here.");
    const stdout = indexOf(html, 'data-testid="stdout"');
    const divider = indexOf(html, 'data-testid="console-divider"');
    const story = indexOf(html, "The wall shows ember.");
    expect(stdout).toBeLessThan(divider);
    expect(divider).toBeLessThan(story);
  });

  it("hides the line when only one side is present", () => {
    expect(markup({ output: "ember\n" })).not.toContain('data-testid="console-divider"');
    const storyOnly = markup({ feedback: "The wall shows ember." });
    expect(storyOnly).not.toContain('data-testid="console-divider"');
    expect(storyOnly).not.toContain("Program output will appear here.");
    const errorOnly = markup({ explainer });
    expect(errorOnly).not.toContain('data-testid="console-divider"');
    expect(errorOnly).not.toContain("Program output will appear here.");
  });

  it("keeps the explainer and traceback on the python side of the line", () => {
    const html = markup({
      output: "ember\n",
      explainer,
      feedback: "The wall stays shut.",
      failedChecks: [{ name: "spoken word", message: "Say ember." }],
    });
    expect(html).not.toContain("Program output will appear here.");
    const stdout = indexOf(html, 'data-testid="stdout"');
    const title = indexOf(html, "Syntax error");
    const traceback = indexOf(html, "SyntaxError: unexpected EOF while parsing");
    const divider = indexOf(html, 'data-testid="console-divider"');
    const story = indexOf(html, "The wall stays shut.");
    const check = indexOf(html, "Say ember.");
    expect(stdout).toBeLessThan(title);
    expect(title).toBeLessThan(traceback);
    expect(traceback).toBeLessThan(divider);
    expect(divider).toBeLessThan(story);
    expect(story).toBeLessThan(check);
  });
});
