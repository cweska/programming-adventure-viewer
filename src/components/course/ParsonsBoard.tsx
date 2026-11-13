"use client";

import { useEffect, useRef, useState } from "react";
import { addLine, moveLine, remainingPieces, removeLine, spokenLine } from "./parsons-logic";

/**
 * "Put the lines in order": an accessible Parsons board. Every action is a button (click, Enter or
 * Space), so nothing needs dragging. Pieces show in the order given in `blocks` (shuffle them first with
 * seededShuffle from ./parsons-logic). `value` is the student's program, top to bottom.
 *
 * data-testids (all start with `idPrefix`): -pieces, -piece-<i>, -program, -line-<i>, -up-<i>,
 * -down-<i>, -remove-<i>, -clear, -status.
 */
export function ParsonsBoard({
  blocks,
  value,
  onChange,
  idPrefix,
}: {
  blocks: string[];
  value: string[];
  onChange: (next: string[]) => void;
  idPrefix: string;
}) {
  const [announcement, setAnnouncement] = useState("");
  const [focusTarget, setFocusTarget] = useState<string | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const remaining = remainingPieces(blocks, value);

  useEffect(() => {
    if (!focusTarget) return;
    const root = rootRef.current;
    const target = root?.querySelector<HTMLElement>(`[data-focus-id="${focusTarget}"]`);
    if (target && !(target as HTMLButtonElement).disabled) target.focus();
    else root?.querySelector<HTMLElement>(`[data-focus-id="${idPrefix}-fallback"]`)?.focus();
    setFocusTarget(null);
  }, [focusTarget, idPrefix, value]);

  function add(pieceIndex: number, position: number) {
    const line = blocks[pieceIndex];
    onChange(addLine(value, line));
    setAnnouncement(`Added line ${value.length + 1}: ${spokenLine(line)}.`);
    // Keep the keyboard in the Pieces list: the next piece takes this one's place.
    const nextPiece = remaining[position + 1] ?? remaining[position - 1];
    setFocusTarget(nextPiece !== undefined ? `${idPrefix}-piece-${nextPiece}` : `${idPrefix}-line-${value.length}-up`);
  }

  function move(index: number, by: -1 | 1) {
    const to = index + by;
    if (to < 0 || to >= value.length) return;
    onChange(moveLine(value, index, to));
    setAnnouncement(`Moved ${spokenLine(value[index])} to line ${to + 1}.`);
    const direction = by < 0 ? "up" : "down";
    const edge = (by < 0 && to === 0) || (by > 0 && to === value.length - 1);
    setFocusTarget(`${idPrefix}-line-${to}-${edge ? (by < 0 ? "down" : "up") : direction}`);
  }

  function remove(index: number) {
    const line = value[index];
    onChange(removeLine(value, index));
    setAnnouncement(`Took out ${spokenLine(line)}. It is back in the pieces.`);
    const after = value.length - 1;
    setFocusTarget(after > 0 ? `${idPrefix}-line-${Math.min(index, after - 1)}-remove` : `${idPrefix}-fallback`);
  }

  function clear() {
    if (value.length === 0) return;
    onChange([]);
    setAnnouncement("Every line is back in the pieces.");
    setFocusTarget(`${idPrefix}-fallback`);
  }

  return (
    <div className="parsons" ref={rootRef} data-testid={idPrefix}>
      <p className="parsons-help" id={`${idPrefix}-help`}>
        Press a piece to add it to your program. Use the arrow buttons to change the order. Some pieces
        might not belong.
      </p>
      <div className="parsons-columns">
        <section className="parsons-pieces" aria-labelledby={`${idPrefix}-pieces-title`}>
          <h4 id={`${idPrefix}-pieces-title`} tabIndex={-1} data-focus-id={`${idPrefix}-fallback`}>
            Pieces
          </h4>
          {remaining.length === 0 ? (
            <p className="parsons-empty">Every piece is in your program.</p>
          ) : (
            <ul data-testid={`${idPrefix}-pieces`} aria-describedby={`${idPrefix}-help`}>
              {remaining.map((pieceIndex, position) => (
                <li key={pieceIndex}>
                  <button
                    type="button"
                    className="parsons-piece"
                    data-testid={`${idPrefix}-piece-${pieceIndex}`}
                    data-focus-id={`${idPrefix}-piece-${pieceIndex}`}
                    aria-label={`Add ${spokenLine(blocks[pieceIndex])}`}
                    onClick={() => add(pieceIndex, position)}
                  >
                    <span aria-hidden="true" className="parsons-plus">
                      +
                    </span>
                    <code>{blocks[pieceIndex]}</code>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
        <section className="parsons-program" aria-labelledby={`${idPrefix}-program-title`}>
          <h4 id={`${idPrefix}-program-title`}>Your program</h4>
          {value.length === 0 ? (
            <p className="parsons-empty" data-testid={`${idPrefix}-program`}>
              Nothing here yet. Press a piece to add it.
            </p>
          ) : (
            <ol data-testid={`${idPrefix}-program`}>
              {value.map((line, index) => (
                <li key={`${index}-${line}`} className="parsons-line" data-testid={`${idPrefix}-line-${index}`}>
                  <span className="parsons-number" aria-hidden="true">
                    {index + 1}
                  </span>
                  <code>{line}</code>
                  <span className="parsons-actions">
                    <button
                      type="button"
                      data-testid={`${idPrefix}-up-${index}`}
                      data-focus-id={`${idPrefix}-line-${index}-up`}
                      aria-label={`Move line ${index + 1} up`}
                      disabled={index === 0}
                      onClick={() => move(index, -1)}
                    >
                      <span aria-hidden="true">↑</span>
                    </button>
                    <button
                      type="button"
                      data-testid={`${idPrefix}-down-${index}`}
                      data-focus-id={`${idPrefix}-line-${index}-down`}
                      aria-label={`Move line ${index + 1} down`}
                      disabled={index === value.length - 1}
                      onClick={() => move(index, 1)}
                    >
                      <span aria-hidden="true">↓</span>
                    </button>
                    <button
                      type="button"
                      data-testid={`${idPrefix}-remove-${index}`}
                      data-focus-id={`${idPrefix}-line-${index}-remove`}
                      aria-label={`Take line ${index + 1} out`}
                      onClick={() => remove(index)}
                    >
                      <span aria-hidden="true">✕</span>
                    </button>
                  </span>
                </li>
              ))}
            </ol>
          )}
          {value.length > 0 ? (
            <button type="button" className="parsons-clear" data-testid={`${idPrefix}-clear`} onClick={clear}>
              Start over
            </button>
          ) : null}
        </section>
      </div>
      <p className="ex-sr-only" role="status" aria-live="polite" data-testid={`${idPrefix}-status`}>
        {announcement}
      </p>
    </div>
  );
}
