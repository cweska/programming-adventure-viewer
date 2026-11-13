import { describe, expect, it } from "vitest";
import type { GlossaryEntry } from "../../lib/course/schema";
import {
  findGlossaryEntry,
  glossaryRefs,
  inlineParts,
  lightBlocks,
  plainText,
  proseBlocks,
  speakableText,
} from "./prose-format";

const glossary: GlossaryEntry[] = [
  { term: "string", aliases: ["strings", "text"], plain: "Text inside quotes." },
  { term: "concatenate", aliases: ["glue"], plain: "Join strings with `+`." },
  { term: "input", aliases: ["input()"], plain: "Something typed in." },
];

describe("inline parts", () => {
  it("splits code spans and glossary links", () => {
    expect(inlineParts("Use `print()` to show a [[string]].")).toEqual([
      { kind: "text", text: "Use " },
      { kind: "code", text: "print()" },
      { kind: "text", text: " to show a " },
      { kind: "term", term: "string", text: "string" },
      { kind: "text", text: "." },
    ]);
  });

  it("shows the text after | for [[term|text]]", () => {
    expect(inlineParts("Glue [[string|strings]] together.")).toEqual([
      { kind: "text", text: "Glue " },
      { kind: "term", term: "string", text: "strings" },
      { kind: "text", text: " together." },
    ]);
  });

  it("keeps an unmatched backtick as text and does not link inside code", () => {
    expect(inlineParts("a ` b")).toEqual([{ kind: "text", text: "a ` b" }]);
    expect(inlineParts("`grid = [[0]]`")).toEqual([{ kind: "code", text: "grid = [[0]]" }]);
  });

  it("reads *words in stars* as emphasis, but never a times sign or a star in code", () => {
    expect(inlineParts("`>=` means *at least*: exactly enough counts.")).toEqual([
      { kind: "code", text: ">=" },
      { kind: "text", text: " means " },
      { kind: "em", text: "at least" },
      { kind: "text", text: ": exactly enough counts." },
    ]);
    expect(inlineParts("Read *Python's last line* first, see [[string]].")).toEqual([
      { kind: "text", text: "Read " },
      { kind: "em", text: "Python's last line" },
      { kind: "text", text: " first, see " },
      { kind: "term", term: "string", text: "string" },
      { kind: "text", text: "." },
    ]);
    for (const text of ["2 * 3 * 4 is 24", "a*b*c", "** not this **", "`x * y`"]) {
      expect(inlineParts(text).some((part) => part.kind === "em"), text).toBe(false);
    }
    expect(plainText("It asks *at most*.")).toBe("It asks at most.");
  });
});

describe("prose blocks", () => {
  it("makes one paragraph per line and skips blank lines", () => {
    const blocks = proseBlocks("First line.\n\nSecond line.");
    expect(blocks.map((block) => block.kind)).toEqual(["paragraph", "paragraph"]);
  });

  it("groups numbered lines into one list and keeps the start number", () => {
    const blocks = proseBlocks("Steps:\n1. Type it.\n2. Run it.\nDone.\n3. Later.");
    expect(blocks.map((block) => block.kind)).toEqual(["paragraph", "list", "paragraph", "list"]);
    const list = blocks[1];
    expect(list.kind === "list" && list.items.length).toBe(2);
    const later = blocks[3];
    expect(later.kind === "list" && later.start).toBe(3);
  });

  it("supports bullet lines", () => {
    const blocks = proseBlocks("- one\n- two");
    expect(blocks).toHaveLength(1);
    expect(blocks[0].kind === "list" && !blocks[0].ordered && blocks[0].items.length).toBe(2);
  });

  it("keeps fenced python code exactly, including indentation", () => {
    const blocks = proseBlocks("Look:\n```python\nif x:\n    print(\"hi\")\n```\nNice.");
    expect(blocks).toEqual([
      { kind: "paragraph", parts: [{ kind: "text", text: "Look:" }] },
      { kind: "code", language: "python", code: 'if x:\n    print("hi")' },
      { kind: "paragraph", parts: [{ kind: "text", text: "Nice." }] },
    ]);
  });

  it("treats an unclosed fence as code to the end", () => {
    const blocks = proseBlocks("```\nprint(1)\nprint(2)");
    expect(blocks).toEqual([{ kind: "code", language: "python", code: "print(1)\nprint(2)" }]);
  });

  it("does not read glossary links or lists inside code blocks", () => {
    expect(glossaryRefs("```python\n1. [[string]]\n```")).toEqual([]);
  });
});

describe("glossary", () => {
  it("lists each referenced term once", () => {
    expect(glossaryRefs("A [[string]], some [[String|strings]], and [[concatenate|glue]].")).toEqual([
      "string",
      "concatenate",
    ]);
  });

  it("finds entries by term or alias, ignoring case", () => {
    expect(findGlossaryEntry(glossary, "STRING")?.term).toBe("string");
    expect(findGlossaryEntry(glossary, "glue")?.term).toBe("concatenate");
    expect(findGlossaryEntry(glossary, "input()")?.term).toBe("input");
    expect(findGlossaryEntry(glossary, "loop")).toBeUndefined();
    expect(findGlossaryEntry(glossary, " ")).toBeUndefined();
  });
});

describe("plain and spoken text", () => {
  const text = "Use `print()` with a [[string|strings]].\n1. Type it.\n```python\nprint(1)\n```";

  it("drops markup for plain text", () => {
    expect(plainText(text)).toBe("Use print() with a strings.\n1. Type it.\nprint(1)");
  });

  it("replaces code blocks with a spoken note", () => {
    expect(speakableText(text)).toBe("Use print() with a strings. 1. Type it. Here is some code to look at.");
  });
});

describe("fewer words", () => {
  it("drops story lines and keeps the teaching lines", () => {
    const blocks = proseBlocks(
      [
        "Before we cast anything, we read, yes?",
        "`print()` shows words on the screen.",
        "Numbers do not need quotes.",
        "Lucky asked what is in it for him. Existing.",
        "1. Press Run.",
      ].join("\n"),
    );
    expect(plainText(lightBlocks(blocks).map(blockText).join("\n"))).toBe(
      "print() shows words on the screen.\nNumbers do not need quotes.\nPress Run.",
    );
  });

  it("keeps everything when every line is story", () => {
    const blocks = proseBlocks("Hi. It is me, Mar'tu.\nCome, yes?");
    expect(lightBlocks(blocks)).toEqual(blocks);
  });
});

function blockText(block: ReturnType<typeof proseBlocks>[number]): string {
  if (block.kind === "code") return block.code;
  if (block.kind === "list") return block.items.map((item) => item.map((part) => part.text).join("")).join("\n");
  return block.parts.map((part) => (part.kind === "code" ? `\`${part.text}\`` : part.text)).join("");
}
