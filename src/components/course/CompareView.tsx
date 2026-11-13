"use client";

import { useEffect, useId, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { compareLines, type CompareLine } from "./exercise-logic";

function CodeColumn({ title, lines, testId }: { title: string; lines: CompareLine[]; testId: string }) {
  const changed = lines.filter((line) => line.changed).length;
  return (
    <figure className="ex-compare-col" data-testid={testId}>
      <figcaption className="ex-compare-title">
        {title}
        <span className="ex-muted"> · {changed === 0 ? "no different lines" : `${changed} different line${changed === 1 ? "" : "s"}`}</span>
      </figcaption>
      {lines.length === 0 ? (
        <p className="ex-muted ex-compare-empty">(empty)</p>
      ) : (
        <ol className="ex-compare-lines">
          {lines.map((line, index) => (
            <li key={index} className={`ex-compare-line${line.changed ? " is-changed" : ""}`} data-changed={line.changed}>
              <span className="ex-compare-number" aria-hidden="true">
                {index + 1}
              </span>
              <span className="ex-compare-mark" aria-hidden="true">
                {line.changed ? "≠" : ""}
              </span>
              <code>{line.text || " "}</code>
              {line.changed ? <span className="ex-sr-only"> (different)</span> : null}
            </li>
          ))}
        </ol>
      )}
    </figure>
  );
}

/**
 * "Compare with Mar'tu's version" (the Show me rung): the student's code and Mar'tu's side by side,
 * read-only, with the different lines marked. It never changes the student's code. "Now type it yourself"
 * folds Mar'tu's version away; "Copy into my editor" is an escape hatch behind a second confirm.
 *
 * testids: compare, compare-heading, compare-mine, compare-theirs, compare-retype, compare-look-again,
 * compare-copy, compare-copy-confirm, compare-copy-yes, compare-copy-no, compare-close.
 */
export function CompareView({
  code,
  solution,
  retyping,
  onRetype,
  onLookAgain,
  onCopy,
  onClose,
}: {
  code: string;
  solution: string;
  retyping: boolean;
  onRetype: () => void;
  onLookAgain: () => void;
  onCopy: () => void;
  onClose: () => void;
}) {
  const [confirmCopy, setConfirmCopy] = useState(false);
  const headingId = useId();
  const headingRef = useRef<HTMLHeadingElement>(null);
  const confirmRef = useRef<HTMLDivElement>(null);
  const diff = useMemo(() => compareLines(code, solution), [code, solution]);

  // Opening the panel moves the keyboard to it (the button that opened it may be gone).
  useEffect(() => {
    headingRef.current?.focus();
  }, []);

  const copyRef = useRef<HTMLButtonElement>(null);
  const backToCopy = useRef(false);

  useEffect(() => {
    if (confirmCopy) confirmRef.current?.querySelector<HTMLButtonElement>('[data-testid="compare-copy-no"]')?.focus();
    else if (backToCopy.current) {
      // "No, I'll type it" (or Esc) removed the button that had the keyboard: give it to "Copy into my editor".
      backToCopy.current = false;
      copyRef.current?.focus();
    }
  }, [confirmCopy]);

  function cancelCopy() {
    backToCopy.current = true;
    setConfirmCopy(false);
  }

  function onConfirmKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      event.preventDefault();
      cancelCopy();
    }
  }

  return (
    <section className={`ex-compare${retyping ? " is-retyping" : ""}`} data-testid="compare" aria-labelledby={headingId}>
      <h3 className="ex-section-title" id={headingId} ref={headingRef} tabIndex={-1} data-testid="compare-heading">
        Compare with Mar&apos;tu&apos;s version
      </h3>
      {retyping ? (
        <p className="ex-compare-note" data-testid="compare-retype-note">
          Now type it yourself in the editor, then press Run. You can look again any time.
        </p>
      ) : (
        <>
          <p className="ex-compare-note">
            Lines marked <span aria-hidden="true">≠</span>
            <span className="ex-sr-only">as different</span> are not the same in both. Your code is not changed.
          </p>
          <div className="ex-compare-cols">
            <CodeColumn title="Your code" lines={diff.mine} testId="compare-mine" />
            <CodeColumn title="Mar'tu's version" lines={diff.theirs} testId="compare-theirs" />
          </div>
        </>
      )}

      {confirmCopy ? (
        <div
          className="reset-confirm ex-confirm"
          data-testid="compare-copy-confirm"
          ref={confirmRef}
          role="group"
          aria-label="Copy Mar'tu's version into your editor?"
          onKeyDown={onConfirmKeyDown}
        >
          <p>Copy Mar&apos;tu&apos;s version over your code? You learn more by typing it yourself.</p>
          <button
            type="button"
            data-testid="compare-copy-yes"
            onClick={() => {
              setConfirmCopy(false);
              onCopy();
            }}
          >
            Yes, copy it
          </button>
          <button type="button" className="reset-cancel" data-testid="compare-copy-no" onClick={cancelCopy}>
            No, I&apos;ll type it
          </button>
        </div>
      ) : null}

      <div className="ex-compare-actions">
        {retyping ? (
          <button type="button" className="ex-quiet" data-testid="compare-look-again" onClick={onLookAgain}>
            Look again
          </button>
        ) : (
          <button type="button" className="ex-next" data-testid="compare-retype" onClick={onRetype}>
            Now type it yourself
          </button>
        )}
        {confirmCopy ? null : (
          <button
            ref={copyRef}
            type="button"
            className="ex-quiet"
            data-testid="compare-copy"
            aria-expanded={confirmCopy}
            onClick={() => setConfirmCopy(true)}
          >
            Copy into my editor
          </button>
        )}
        <button type="button" className="ex-quiet" data-testid="compare-close" onClick={onClose}>
          Close
        </button>
      </div>
    </section>
  );
}
