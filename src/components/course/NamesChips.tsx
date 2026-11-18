"use client";

import { useId } from "react";

/**
 * "Names to use" chips and Mar'tu's pick (curriculum §2.2, §2.7). Each chip is a button that puts the
 * name in the editor at the cursor; the pick button puts Mar'tu's value there (in quotes where needed).
 * Any other value still passes: the pick is only for when a student can't decide. Python's own tools (`str`,
 * `print`, `len`: splitNames()) get a row of their own, "Tools to use", so they never look like one more box.
 */
export function NamesChips({
  names,
  tools = [],
  pick,
  prominent,
  onInsertName,
  onPick,
}: {
  names: readonly string[];
  /** Python's tools among the step's names, shown apart from the boxes. */
  tools?: readonly string[];
  pick?: string;
  /** The active step gives only the goal and the names (not dictated): show the chips larger. */
  prominent: boolean;
  onInsertName: (name: string) => void;
  onPick: (pick: string) => void;
}) {
  const labelId = useId();
  const toolsLabelId = useId();
  if (names.length === 0 && tools.length === 0 && !pick) return null;
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
      {tools.length > 0 ? (
        <div className="ex-names ex-tools" data-testid="tools" role="group" aria-labelledby={toolsLabelId}>
          <span className="ex-names-label" id={toolsLabelId}>
            Tools to use:
          </span>
          {tools.map((tool) => (
            <button
              key={tool}
              type="button"
              className="ex-name-chip is-tool"
              data-testid={`name-chip-${tool}`}
              data-tool="true"
              aria-label={`Put the tool ${tool} in your code`}
              title="Put this tool in your code"
              onClick={() => onInsertName(tool)}
            >
              <code>{tool}</code>
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
