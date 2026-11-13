"use client";

import Link from "next/link";
import { useEffect } from "react";
import type { ItemPageProps } from "../../lib/course/contracts";
import { itemKey, markRead, useProgressReady } from "../../lib/course/progress";
import type { CheatsheetItem } from "../../lib/course/schema";
import { KindBadge } from "./CourseBits";
import { Prose } from "./Prose";

/** A unit's cheat sheet: concept, code, output and a note per entry. Prints cleanly on paper. */
export function CheatsheetView({ unit, item, glossary, nextHref }: ItemPageProps<CheatsheetItem>) {
  const ready = useProgressReady();
  const key = itemKey(unit.id, item.id);

  // Opening the cheat sheet is all it takes to "finish" it.
  useEffect(() => {
    if (ready) markRead(key);
  }, [ready, key]);

  return (
    <div className="course-reading cheatsheet" data-testid="cheatsheet">
      <header className="item-header">
        <KindBadge kind="cheatsheet" />
        <h1>{item.title}</h1>
        <p className="item-meta print-only">
          Intro to Python · Unit {unit.order}: {unit.title}
        </p>
        {item.summary ? <Prose text={item.summary} glossary={glossary} className="item-summary" /> : null}
        <div className="no-print item-tools">
          <button type="button" onClick={() => window.print()} data-testid="cheatsheet-print">
            Print this page
          </button>
        </div>
      </header>
      <ol className="cheatsheet-entries">
        {item.entries.map((entry, index) => (
          <li key={`${entry.concept}-${index}`} className="cheatsheet-entry" data-testid={`cheatsheet-entry-${index + 1}`}>
            <h2>
              <Prose text={entry.concept} glossary={glossary} inline />
            </h2>
            <pre className="cheatsheet-code" aria-label={`${entry.concept}: code`}>
              <code>{entry.code.replace(/\n$/, "")}</code>
            </pre>
            {entry.output !== undefined ? (
              <div className="cheatsheet-output">
                <p className="cheatsheet-label">Prints</p>
                <pre>{entry.output}</pre>
              </div>
            ) : null}
            {entry.note ? <Prose text={entry.note} glossary={glossary} className="cheatsheet-note" /> : null}
          </li>
        ))}
      </ol>
      <div className="item-footer no-print">
        <Link className="course-button" href={nextHref} data-testid="item-next">
          Next
        </Link>
      </div>
    </div>
  );
}
