"use client";

import { useId } from "react";

/**
 * "Names to use" chips and Mar'tu's pick (curriculum §2.2, §2.7). Each chip is a button that puts the
 * name in the editor at the cursor; the pick button puts Mar'tu's value there (in quotes where needed).
 * Any other value still passes: the pick is only for when a student can't decide.
 */
export function NamesChips({
  names,
  pick,
  prominent,
  onInsertName,
  onPick,
}: {
  names: readonly string[];
  pick?: string;
  /** The active step gives only the goal and the names (not dictated): show the chips larger. */
  prominent: boolean;
  onInsertName: (name: string) => void;
  onPick: (pick: string) => void;
}) {
  const labelId = useId();
  if (names.length === 0 && !pick) return null;
  const multiLine = Boolean(pick && pick.includes("\n"));
  return (
    <div className={`ex-extras${prominent ? " is-prominent" : ""}`} data-testid="step-extras">
      {names.length > 0 ? (
        <div className="ex-names" data-testid="names" role="group" aria-labelledby={labelId}>
          <span className="ex-names-label" id={labelId}>
            Names to use:
          </span>
          {names.map((name) => (
            <button
              key={name}
              type="button"
              className="ex-name-chip"
              data-testid={`name-chip-${name}`}
              aria-label={`Put ${name} in your code`}
              title="Put this name in your code"
              onClick={() => onInsertName(name)}
            >
              <code>{name}</code>
            </button>
          ))}
        </div>
      ) : null}
      {pick ? (
        <div className="ex-pick" data-testid="pick">
          {multiLine ? (
            <>
              <span className="ex-pick-label">Can&apos;t decide? Mar&apos;tu&apos;s pick:</span>
              <pre className="ex-pick-text">{pick}</pre>
              <button type="button" className="ex-quiet" data-testid="pick-use" onClick={() => onPick(pick)}>
                Put Mar&apos;tu&apos;s pick in my code
              </button>
            </>
          ) : (
            <button
              type="button"
              className="ex-pick-button"
              data-testid="pick-use"
              aria-label={`Can't decide? Use Mar'tu's pick: ${pick}`}
              onClick={() => onPick(pick)}
            >
              Can&apos;t decide? Mar&apos;tu&apos;s pick: <code>{pick}</code>
            </button>
          )}
        </div>
      ) : null}
    </div>
  );
}
