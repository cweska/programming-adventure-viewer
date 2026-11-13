"use client";

import { useEffect, useId, useRef, useState } from "react";
import type { AnotherWay, Checkpoint, GlossaryEntry } from "../../lib/course/schema";
import { angleLabel, helpOfferLine, type HelpOffer, type HelpState, type Rung } from "./exercise-logic";
import { Prose } from "./Prose";
import { ReadAloud } from "./ReadAloud";

export type RevealResult = "opened" | "paced" | "locked" | "none";

/**
 * The Help stack (curriculum §2.2): ONE climbing Help control for the current step. Each press opens the
 * next rung (Start me off, Where to look, Another way, Teach me, More structure, Show me). Rungs stay
 * open so they can be read again; using them never costs anything.
 *
 * testids: help, help-button, help-rung-<n> (n from 1, in order), help-offer, help-offer-dismiss,
 * help-paced, help-show-locked, help-another-next, assemble-open, compare-open, help-locked.
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
  onReveal,
  onDismissOffer,
  onOpenAssemble,
  onOpenCompare,
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
  onReveal: () => RevealResult;
  onDismissOffer: () => void;
  onOpenAssemble: () => void;
  onOpenCompare: () => void;
}) {
  const baseId = useId();
  const [note, setNote] = useState<"paced" | null>(null);
  const [angle, setAngle] = useState(0);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const lastRungRef = useRef<HTMLLIElement>(null);
  const focusLast = useRef(false);
  const stepLabel = `${noun.toLowerCase()} ${stepNumber}`;

  useEffect(() => setNote(null), [runNumber, state.open.length, checkpoint.id]);

  // The Help control goes away once every rung is open: keep the keyboard on the newest rung.
  useEffect(() => {
    if (!focusLast.current) return;
    focusLast.current = false;
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

  const buttonText = next
    ? `${state.open.length === 0 ? "Help" : "More help"}: ${next.label}${state.nextLocked ? " (opens soon)" : ""}`
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
            {helpOfferLine(offer)}
          </p>
          <button type="button" className="ex-link-button" data-testid="help-offer-dismiss" onClick={onDismissOffer}>
            No thanks
          </button>
        </div>
      ) : null}

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
            aria-label={`${buttonText}, for ${stepLabel}`}
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
      {state.open.length === 0 && !offer ? (
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
