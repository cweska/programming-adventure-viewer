/**
 * Server-render tests for Help options and the first-visit question (no DOM needed). The preset logic
 * itself (migration, answers, when to ask) is tested in src/lib/course/progress.test.ts.
 */
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { CourseSettings, PlacementQuestion } from "./CourseSettings";

describe("CourseSettings", () => {
  const html = renderToStaticMarkup(createElement(CourseSettings));
  const input = (testId: string) => html.match(new RegExp(`<input[^>]*data-testid="${testId}"[^>]*>`))?.[0] ?? "";

  it("offers Show me more (the default) and Keep it short as one radio group, plus Read aloud", () => {
    expect(html).toContain('data-testid="setting-preset"');
    expect(html).toContain("<legend>How much should Mar&#x27;tu explain?</legend>");
    expect(input("setting-preset-more")).toContain('type="radio"');
    expect(input("setting-preset-more")).toContain('checked=""');
    expect(input("setting-preset-short")).toContain('type="radio"');
    expect(input("setting-preset-short")).not.toContain("checked");
    // One group: both radios share a name.
    const name = input("setting-preset-more").match(/\sname="([^"]+)"/)?.[1];
    expect(name).toBeTruthy();
    expect(input("setting-preset-short")).toContain(`name="${name}"`);
    expect(html).toContain("Show me more.");
    expect(html).toContain("Keep it short.");
    expect(html).toContain('data-testid="setting-read-aloud"');
    // The old "Fewer words" switch is gone.
    expect(html).not.toContain("Fewer words");
    expect(html).not.toContain("setting-light");
  });

  it("labels every input", () => {
    for (const match of html.matchAll(/<input[^>]*\sid="([^"]+)"/g)) {
      expect(html).toContain(`for="${match[1]}"`);
    }
  });
});

describe("PlacementQuestion", () => {
  it("is not in the server render (it waits for the saved progress, so returning students never see it flash)", () => {
    expect(renderToStaticMarkup(createElement(PlacementQuestion))).toBe("");
  });
});
