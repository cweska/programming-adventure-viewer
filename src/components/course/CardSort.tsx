"use client";

import { useState } from "react";
import type { GlossaryEntry } from "../../lib/course/schema";
import { cardSortMarks, type CardSortData } from "./card-sort";
import { Prose } from "./Prose";

/**
 * A one-click card sort on an Another way angle (the teacher's Unit 5 request: the quotes sort). Each card gets one
 * click, the group it belongs to; "Check my sort" marks each card right or not yet and shows the angle's explanation.
 * Free, never graded, never saved: a thinking tool, like Predict before Run.
 *
 * testids: card-sort, card-sort-card-<i>, card-sort-pick-<i>-<g> (aria-pressed), card-sort-check, card-sort-mark-<i>
 * (data-right), card-sort-result, card-sort-explain, card-sort-again.
 */
export function CardSort({ sort, glossary, idPrefix }: { sort: CardSortData; glossary?: GlossaryEntry[]; idPrefix: string }) {
  const [picks, setPicks] = useState<(number | null)[]>(() => sort.cards.map(() => null));
  const [checked, setChecked] = useState(false);
  const marks = checked ? cardSortMarks(sort, picks) : null;
  const sorted = picks.every((pick) => pick !== null);

  function pick(card: number, group: number) {
    setChecked(false);
    setPicks((previous) => previous.map((value, index) => (index === card ? group : value)));
  }

  return (
    <div className="card-sort" data-testid="card-sort">
      <ol className="card-sort-cards">
        {sort.cards.map((card, index) => (
          <li key={`${idPrefix}-${index}`} className="card-sort-card" data-testid={`card-sort-card-${index}`}>
            {/* The number the angle's explanation uses ("Cards 2, 3 and 5 have quotes"). */}
            <span className="card-sort-number" aria-hidden="true">
              {index + 1}
            </span>
            <code className="inline-code card-sort-text">{card.text}</code>
            <span className="card-sort-picks" role="group" aria-label={`Card ${index + 1}: which group?`}>
              {sort.groups.map((group, g) => (
                <button
                  key={g}
                  type="button"
                  className="card-sort-pick"
                  aria-pressed={picks[index] === g}
                  data-testid={`card-sort-pick-${index}-${g}`}
                  onClick={() => pick(index, g)}
                >
                  {group}
                </button>
              ))}
            </span>
            {marks ? (
              <span className={marks[index] ? "card-sort-mark right" : "card-sort-mark"} data-testid={`card-sort-mark-${index}`} data-right={marks[index]}>
                {marks[index] ? "✓ Right" : "Not yet"}
              </span>
            ) : null}
          </li>
        ))}
      </ol>
      <div className="card-sort-actions">
        <button type="button" data-testid="card-sort-check" disabled={!sorted} onClick={() => setChecked(true)}>
          Check my sort
        </button>
        {checked ? (
          <button
            type="button"
            className="ex-quiet"
            data-testid="card-sort-again"
            onClick={() => {
              setPicks(sort.cards.map(() => null));
              setChecked(false);
            }}
          >
            Sort again
          </button>
        ) : null}
        {!sorted ? <span className="ex-muted">Pick a group for every card first.</span> : null}
      </div>
      <div aria-live="polite">
        {marks ? (
          <div className="card-sort-result" data-testid="card-sort-result">
            <p>
              {marks.filter(Boolean).length} of {marks.length} right.
            </p>
            <div data-testid="card-sort-explain">
              <Prose text={sort.explain} glossary={glossary} />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
