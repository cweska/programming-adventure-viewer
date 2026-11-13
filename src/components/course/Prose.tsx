"use client";

import { useEffect, useId, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";
import type { GlossaryEntry } from "../../lib/course/schema";
import { findGlossaryEntry, inlineParts, lightBlocks, proseBlocks, type InlinePart, type ProseBlock } from "./prose-format";

/* Server renders run useEffect never; use it there so React does not warn about useLayoutEffect. */
const useIsoLayoutEffect = typeof window === "undefined" ? useEffect : useLayoutEffect;

/** Short inline code (`mana = mana - cost`) stays on one line, so it never reads as two pieces of code. */
function inlineCodeClass(code: string): string {
  return code.length <= 24 ? "inline-code is-short" : "inline-code";
}

/** Inline code and plain text only (used inside the glossary popover, where terms do not nest). */
function SimpleInline({ text }: { text: string }) {
  return (
    <>
      {inlineParts(text).map((part, index) =>
        part.kind === "code" ? (
          <code key={index} className={inlineCodeClass(part.text)}>
            {part.text}
          </code>
        ) : (
          <span key={index}>{part.text}</span>
        ),
      )}
    </>
  );
}

/** A glossary word: a button that opens a small box with the plain meaning and an example. */
export function GlossaryTerm({ entry, children }: { entry: GlossaryEntry; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const [shift, setShift] = useState(0);
  const [above, setAbove] = useState(false);
  const wrapRef = useRef<HTMLSpanElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const popoverRef = useRef<HTMLSpanElement>(null);
  const id = useId();

  useEffect(() => {
    if (!open) return;
    const onPointer = (event: PointerEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(event.target as Node)) setOpen(false);
    };
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("pointerdown", onPointer);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onPointer);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  // Keep the box on screen at phone width: slide it left if it would run off the right edge, and open it
  // above the word when there is no room below (a term near the bottom of a phone screen).
  useIsoLayoutEffect(() => {
    if (!open) {
      setShift(0);
      setAbove(false);
      return;
    }
    const box = popoverRef.current;
    if (!box) return;
    const term = buttonRef.current?.getBoundingClientRect();
    // On a phone the box is a sheet fixed to the screen (course.css), so it can never run off the edge:
    // it goes to the top of the screen when the word is in the lower half, so it never covers the word.
    if (getComputedStyle(box).position === "fixed") {
      setShift(0);
      setAbove(term ? term.top + term.height / 2 > window.innerHeight / 2 : false);
      return;
    }
    const rect = box.getBoundingClientRect();
    const overflow = rect.right - (window.innerWidth - 12);
    setShift(overflow > 0 ? Math.max(0, Math.min(overflow, rect.left - 12)) : 0);
    if (rect.bottom <= window.innerHeight - 8) return;
    if (term && term.top - rect.height - 6 >= 8) {
      setAbove(true);
      return;
    }
    // No room above either (a very short window): scroll just enough to show it.
    try {
      box.scrollIntoView({ block: "nearest" });
    } catch {
      // Old browsers: the box is still there, one scroll away.
    }
  }, [open]);

  return (
    <span className="glossary-wrap" ref={wrapRef}>
      <button
        ref={buttonRef}
        type="button"
        className="glossary-term"
        aria-expanded={open}
        aria-controls={open ? id : undefined}
        data-testid="glossary-term"
        onClick={() => setOpen((value) => !value)}
      >
        {children}
      </button>
      {open ? (
        <span
          ref={popoverRef}
          id={id}
          role="note"
          className={`glossary-popover${above ? " is-above" : ""}`}
          data-testid="glossary-popover"
          style={shift ? { transform: `translateX(-${shift}px)` } : undefined}
        >
          <span className="glossary-popover-term">{entry.term}</span>
          <span className="glossary-popover-plain">
            <SimpleInline text={entry.plain} />
          </span>
          {entry.example ? (
            <span className="glossary-popover-example">
              <span className="glossary-popover-label">Example:</span> <code className="inline-code">{entry.example}</code>
            </span>
          ) : null}
          <button
            type="button"
            className="glossary-close"
            onClick={() => {
              setOpen(false);
              buttonRef.current?.focus();
            }}
          >
            Close
          </button>
        </span>
      ) : null}
    </span>
  );
}

function Inline({ parts, glossary }: { parts: InlinePart[]; glossary: readonly GlossaryEntry[] }) {
  return (
    <>
      {parts.map((part, index) => {
        if (part.kind === "code") {
          return (
            <code key={index} className={inlineCodeClass(part.text)}>
              {part.text}
            </code>
          );
        }
        if (part.kind === "term") {
          const entry = findGlossaryEntry(glossary, part.term);
          return entry ? (
            <GlossaryTerm key={index} entry={entry}>
              {part.text}
            </GlossaryTerm>
          ) : (
            <span key={index}>{part.text}</span>
          );
        }
        return <span key={index}>{part.text}</span>;
      })}
    </>
  );
}

function Block({ block, glossary }: { block: ProseBlock; glossary: readonly GlossaryEntry[] }) {
  if (block.kind === "code") {
    return (
      <pre className="prose-code" aria-label="Python code">
        <code>{block.code}</code>
      </pre>
    );
  }
  if (block.kind === "list") {
    const items = block.items.map((item, index) => (
      <li key={index}>
        <Inline parts={item} glossary={glossary} />
      </li>
    ));
    return block.ordered ? (
      <ol className="prose-list" start={block.start === 1 ? undefined : block.start}>
        {items}
      </ol>
    ) : (
      <ul className="prose-list">{items}</ul>
    );
  }
  return (
    <p>
      <Inline parts={block.parts} glossary={glossary} />
    </p>
  );
}

/**
 * Course prose (see the format at the top of src/lib/course/schema.ts): one paragraph per line, numbered
 * lists, `inline code`, fenced python code, and [[glossary]] words that open a plain-language box.
 *
 * `light` ("Fewer words") hides the story lines and shows a button to bring them back.
 * `inline` renders a single line with no wrapping <p> (for titles, list items and buttons).
 */
export function Prose({
  text,
  glossary = [],
  light = false,
  inline = false,
  className,
  testId,
}: {
  text: string;
  glossary?: readonly GlossaryEntry[];
  light?: boolean;
  inline?: boolean;
  className?: string;
  testId?: string;
}) {
  const [showAll, setShowAll] = useState(false);
  const blocks = useMemo(() => proseBlocks(text), [text]);
  const shown = useMemo(() => (light && !showAll ? lightBlocks(blocks) : blocks), [blocks, light, showAll]);
  const hidden = blocks.length - shown.length;

  if (inline) {
    return (
      <span className={className} data-testid={testId}>
        <Inline parts={inlineParts(text.replace(/\s*\n\s*/g, " "))} glossary={glossary} />
      </span>
    );
  }

  return (
    <div className={["prose", className].filter(Boolean).join(" ")} data-testid={testId}>
      {shown.map((block, index) => (
        <Block key={index} block={block} glossary={glossary} />
      ))}
      {light && (hidden > 0 || showAll) ? (
        <button type="button" className="prose-more" onClick={() => setShowAll((value) => !value)} aria-expanded={showAll}>
          {showAll ? "Fewer words" : "Show all the words"}
        </button>
      ) : null}
    </div>
  );
}
