"use client";

import { useEffect, useId, useRef, useState } from "react";
import type { AnotherWay, Checkpoint, GlossaryEntry } from "../../lib/course/schema";
import { angleLabel, helpOfferLine, type HelpOffer, type HelpState, type Rung } from "./exercise-logic";
import { Prose } from "./Prose";
import { ReadAloud } from "./ReadAloud";

export type RevealResult = "opened" | "paced" | "locked" | "none";

/**
 * The Help stack (curriculum §2.2): ONE climbing Help control for the current step. Each press opens the
 * next rung (Start me off, Where to look, Another way, Teach me, More structure, Show me how, Compare with
 * Mar'tu's version). Rungs stay open so they can be read again; using them never costs anything.
 *
 * Under "Keep it short" the control climbs Where to look, Teach me, Show me how and Mar'tu's version; Start me
 * off, Another way and More structure sit under "More options" (curriculum §2.3). Right after a crash, Help
 * first says which line to mend (a crash checks no step), and Start me off waits. The player aims Help at the
 * step that names the crash line; when no step does but the steps name other lines, `crashOnly` holds every
 * rung back until the code runs, so Help never contradicts "Mend line 3 first."
 *
 * testids: help, help-button, help-rung-<n> (n from 1, in order), help-offer, help-offer-dismiss,
 * help-paced, help-show-locked, help-another-next, help-start-code, help-start-insert, help-start-done,
 * help-crash, help-more-options, help-extra-<kind>, assemble-open, compare-open, help-locked.
 */
export function HelpStack({
  noun,
  stepNumber,
  checkpoint,
  state,
  anotherWay,
  glossary,
  offer,
  compareOpen,
  showUnlocked,
  runNumber,
  crashed = false,
  crashLine = null,
  crashOnly = false,
  startInCode = () => false,
  onReveal,
  onDismissOffer,
  onOpenAssemble,
  onOpenCompare,
  onInsertStart,
}: {
  noun: string;
  stepNumber: number;
  checkpoint: Checkpoint;
  state: HelpState;
  anotherWay: readonly AnotherWay[];
  glossary: GlossaryEntry[];
  offer: HelpOffer | null;
  compareOpen: boolean;
  showUnlocked: boolean;
  /** Bumps on every Run (clears the "read that one first" note). */
  runNumber: number;
  /** The last run crashed, at this line of the student's code (null when Python did not name one). */
  crashed?: boolean;
  crashLine?: number | null;
  /**
   * The crash is on a line no step names, while the steps name other lines (a broken spell): this step's
   * rungs would talk about a different line, so they wait until the code runs. Only the crash note shows.
   */
  crashOnly?: boolean;
  /** Whether the code already starts the step's line (Start me off then has nothing to add). */
  startInCode?: (start: string) => boolean;
  onReveal: () => RevealResult;
  onDismissOffer: () => void;
  onOpenAssemble: () => void;
  onOpenCompare: () => void;
  /** "Start me off": put the first tokens of the line in the editor. */
  onInsertStart: (text: string) => void;
}) {
  const baseId = useId();
  const [note, setNote] = useState<"paced" | null>(null);
  const [angle, setAngle] = useState(0);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const lastRungRef = useRef<HTMLLIElement>(null);
  const focusLast = useRef(false);
  const stepLabel = `${noun.toLowerCase()} ${stepNumber}`;

  useEffect(() => setNote(null), [runNumber, state.open.length, checkpoint.id]);

  // A rung just opened: bring it (and the Help control under it) into view, since the code pane can be
  // its own scroll box. The Help control goes away once every rung is open: keep the keyboard on the newest
  // rung then.
  useEffect(() => {
    if (!focusLast.current) return;
    focusLast.current = false;
    try {
      buttonRef.current?.scrollIntoView({ block: "nearest" });
      lastRungRef.current?.scrollIntoView({ block: "nearest" });
    } catch {
      // Old browsers without scrollIntoView options: the rung is still there, just not scrolled to.
    }
    if (!buttonRef.current) lastRungRef.current?.focus();
  }, [state.open.length]);

  const next = state.next;
  const offerId = `${baseId}-offer`;

  function press() {
    if (!next || state.nextLocked) return;
    const result = onReveal();
    if (result === "paced") setNote("paced");
    else if (result === "opened") {
      setNote(null);
      // Show me and More structure open their own panel, which takes the keyboard.
      focusLast.current = next.kind !== "show" && next.kind !== "structure";
    }
  }

  function rungBody(rung: Rung) {
    if (rung.kind === "another") {
      if (anotherWay.length === 0) return null;
      const shown = anotherWay[angle % anotherWay.length];
      return (
        <div className="ex-help-another">
          <p className="ex-help-angle">
            {angleLabel(shown)}
            {anotherWay.length > 1 ? (
              <span className="ex-muted">
                {" "}
                ({(angle % anotherWay.length) + 1} of {anotherWay.length})
              </span>
            ) : null}
          </p>
          <Prose text={shown.text} glossary={glossary} />
          <ReadAloud text={shown.text} testId="read-aloud-help-another" />
          {anotherWay.length > 1 ? (
            <button
              type="button"
              className="ex-quiet"
              data-testid="help-another-next"
              onClick={() => setAngle((value) => value + 1)}
            >
              Try another angle: {angleLabel(anotherWay[(angle + 1) % anotherWay.length])}
            </button>
          ) : null}
        </div>
      );
    }
    if (rung.kind === "start" && rung.start) {
      if (startInCode(rung.start)) {
        return (
          <div className="ex-help-start">
            <p data-testid="help-start-done">
              Your code already starts this line (<code className="inline-code">{rung.start}</code>). Finish it yourself.
            </p>
          </div>
        );
      }
      return (
        <div className="ex-help-start">
          <p>Start your line like this, then finish it yourself:</p>
          <pre className="ex-help-start-code" data-testid="help-start-code">
            <code>{rung.start}</code>
          </pre>
          <button type="button" className="ex-quiet" data-testid="help-start-insert" onClick={() => onInsertStart(rung.start ?? "")}>
            Put it in my code
          </button>
          <p className="ex-muted ex-help-start-note">It goes on a new line of its own.</p>
        </div>
      );
    }
    if (rung.kind === "structure") {
      return (
        <div>
          <p>Build it from pieces instead of typing it all. Put the lines in order, then put them in the editor.</p>
          <button type="button" className="ex-quiet" data-testid="assemble-open" onClick={onOpenAssemble}>
            Assemble it
          </button>
        </div>
      );
    }
    if (rung.kind === "show") {
      return (
        <div>
          <p>Mar&apos;tu&apos;s version is next to your code, with the different lines marked. Then type it yourself.</p>
          {compareOpen ? null : (
            <button type="button" className="ex-quiet" data-testid="compare-open" onClick={onOpenCompare}>
              Compare with Mar&apos;tu&apos;s version again
            </button>
          )}
        </div>
      );
    }
    const hint = rung.hint !== undefined ? checkpoint.hints[rung.hint] : undefined;
    return hint ? (
      <>
        <Prose text={hint} glossary={glossary} />
        <ReadAloud text={hint} testId={`read-aloud-help-${rung.hint}`} />
      </>
    ) : null;
  }

  const crashNote = crashed ? (
    <p className="ex-help-crash" data-testid="help-crash">
      <strong>{`Mend ${crashLine ? `line ${crashLine}` : "the error"} first.`}</strong> Python stopped there, so it could
      not check your steps yet. Read the message under your code.
    </p>
  ) : null;

  if (crashOnly) {
    return (
      <section
        className="ex-help"
        data-testid="help"
        data-step={checkpoint.id}
        data-crash-only="true"
        aria-label={`Help for ${crashLine ? `line ${crashLine}` : "the error"}`}
      >
        {crashNote}
        <p className="ex-help-note ex-muted" data-testid="help-crash-wait">
          Help for the {noun.toLowerCase()}s comes back once your code runs.
        </p>
      </section>
    );
  }

  const buttonText = next
    ? `${state.opened === 0 ? "Help" : "More help"}${crashed ? ` with ${stepLabel}` : ""}: ${next.label}${state.nextLocked ? " (opens soon)" : ""}`
    : "";

  return (
    <section
      className={`ex-help${offer ? " is-offered" : ""}`}
      data-testid="help"
      data-step={checkpoint.id}
      aria-label={`Help for ${stepLabel}`}
    >
      {offer ? (
        <div className="ex-help-offer" data-testid="help-offer" data-offer={offer}>
          <p id={offerId} role="status">
            {helpOfferLine(offer, crashed)}
          </p>
          <button type="button" className="ex-link-button" data-testid="help-offer-dismiss" onClick={onDismissOffer}>
            No thanks
          </button>
        </div>
      ) : null}

      {crashNote}

      {state.open.length > 0 ? (
        <ol className="ex-help-rungs" aria-live="polite" data-testid="help-rungs">
          {state.open.map((rung, index) => {
            const newest = index === state.open.length - 1;
            return (
              <li
                key={`${checkpoint.id}-${index}`}
                ref={newest ? lastRungRef : undefined}
                tabIndex={newest ? -1 : undefined}
                className={`ex-help-rung is-${rung.kind}${newest ? " is-newest" : ""}`}
                data-testid={`help-rung-${index + 1}`}
                data-kind={rung.kind}
              >
                <p className="ex-help-rung-label">
                  {rung.label}
                  <span className="ex-sr-only"> (help for {stepLabel})</span>
                </p>
                {rungBody(rung)}
              </li>
            );
          })}
        </ol>
      ) : null}

      <div className="ex-help-actions">
        {next ? (
          <button
            ref={buttonRef}
            type="button"
            className={`ex-help-button${offer ? " is-offered" : ""}`}
            data-testid="help-button"
            data-next={next.kind}
            aria-disabled={state.nextLocked ? true : undefined}
            aria-describedby={offer ? offerId : undefined}
            aria-label={crashed ? buttonText : `${buttonText}, for ${stepLabel}`}
            onClick={press}
          >
            <span aria-hidden="true">💡</span> {buttonText}
          </button>
        ) : null}
        {showUnlocked && !compareOpen && next !== null && next.kind !== "show" ? (
          <button type="button" className="ex-quiet" data-testid="compare-open" onClick={onOpenCompare}>
            Compare with Mar&apos;tu&apos;s version
          </button>
        ) : null}
      </div>

      {state.extras.length > 0 ? (
        <details className="ex-help-more" data-testid="help-more-options">
          <summary>More options</summary>
          <ul className="ex-help-rungs ex-help-extras">
            {state.extras.map((rung) => (
              <li key={rung.kind} className={`ex-help-rung is-${rung.kind}`} data-testid={`help-extra-${rung.kind}`} data-kind={rung.kind}>
                <p className="ex-help-rung-label">
                  {rung.label}
                  <span className="ex-sr-only"> (help for {stepLabel})</span>
                </p>
                {rungBody(rung)}
              </li>
            ))}
          </ul>
        </details>
      ) : null}

      <div aria-live="polite">
        {note === "paced" ? (
          <p className="ex-help-note" data-testid="help-paced">
            Read that one and try it first. More help opens in a few seconds, or after you press Run.
          </p>
        ) : null}
      </div>
      {state.nextLocked ? (
        <p className="ex-help-note ex-muted" data-testid="help-show-locked">
          Mar&apos;tu&apos;s version opens after a few more tries, or a few more minutes. Each change you run counts.
        </p>
      ) : null}
      {state.opened === 0 && !offer && !crashed ? (
        <p className="ex-help-note ex-muted">Help never costs you anything.</p>
      ) : null}
    </section>
  );
}

/** Shown instead of Help under "light" support until the first run that does not finish. */
export function HelpLocked() {
  return (
    <p className="ex-help-note ex-muted" data-testid="help-locked">
      Help opens after you press Run once.
    </p>
  );
}
