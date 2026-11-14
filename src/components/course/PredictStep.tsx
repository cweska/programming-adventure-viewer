"use client";

import { useId, useMemo, useState } from "react";
import type { GlossaryEntry, Playable } from "../../lib/course/schema";
import { useStudentSeed } from "../../lib/course/student-seed";
import { Prose } from "./Prose";
import { choiceOrder, choiceSeed } from "./quiz-grading";

/**
 * Two choices that are the same once spaces are taken out: the spaces are the whole question (`burst: 37` or
 * `burst:37`). Then every space is drawn as a faint dot, so a line break can never hide one.
 */
export function spacesMatter(choices: readonly string[]): boolean {
  const squashed = choices.map((choice) => choice.replace(/[ \t]+/g, ""));
  return squashed.some((value, index) => squashed.indexOf(value) !== index);
}

/** A choice's text with each space as a visible dot (a real space for copying and screen readers). */
function ChoiceText({ text, showSpaces }: { text: string; showSpaces: boolean }) {
  if (!showSpaces) return <span className="ex-predict-text">{text}</span>;
  const parts = text.split(" ");
  return (
    <span className="ex-predict-text is-spaced">
      {parts.map((part, index) => (
        <span key={index}>
          {index > 0 ? <span className="ex-vis-space"> </span> : null}
          {part}
        </span>
      ))}
    </span>
  );
}

/**
 * Predict before Run (curriculum §2.1 step 2): a one-click guess, free, and never in the way of Run.
 * `saved` is the remembered answer: a choice index, -1 for skipped, undefined for not asked yet.
 * A guess or skip from an earlier visit keeps the card closed. The choices show in a shuffled order (choiceOrder,
 * seeded by the student and `orderKey`, the exercise), but every index here is the AUTHORED one: `answer`, the saved
 * guess, the ✓ and ✗ marks and `data-testid="predict-choice-<index>"`.
 */
export function PredictStep({
  predict,
  editorCode,
  starter,
  glossary,
  saved,
  orderKey,
  onAnswer,
  onClose,
}: {
  predict: NonNullable<Playable["predict"]>;
  editorCode: string;
  starter: string;
  glossary: GlossaryEntry[];
  saved: number | undefined;
  /** Where the choices are (the exercise's progress key): with the student, it seeds the display order. */
  orderKey: string;
  /** A choice index, or -1 for "Skip". */
  onAnswer: (choice: number) => void;
  /** The card is gone (skipped or "Got it"): put the keyboard somewhere useful. */
  onClose: () => void;
}) {
  const [guess, setGuess] = useState<number | null>(null);
  const [closed, setClosed] = useState(false);
  const titleId = useId();
  const student = useStudentSeed();
  const order = useMemo(
    () => choiceOrder(predict.choices.length, choiceSeed(student ?? "", `${orderKey}:predict`)),
    [predict.choices.length, student, orderKey],
  );

  if (closed || (guess === null && saved !== undefined)) return null;

  // The code being predicted: shown in the card unless it is exactly what the editor shows.
  const target = predict.code ?? starter;
  const showCode = target.trim() !== editorCode.trim();
  const right = guess !== null && guess === predict.answer;
  const showSpaces = spacesMatter(predict.choices);

  function choose(index: number) {
    setGuess(index);
    onAnswer(index);
  }

  function close() {
    setClosed(true);
    onClose();
  }

  return (
    <section className="ex-predict" data-testid="predict" aria-labelledby={titleId}>
      <p className="ex-predict-title" id={titleId}>
        <span className="ex-predict-tag">Predict first</span> <Prose text={predict.q} glossary={glossary} inline />
      </p>
      {showCode ? (
        <pre className="ex-predict-code" aria-label="Code to predict" data-testid="predict-code">
          <code>{target.replace(/\n$/, "")}</code>
        </pre>
      ) : (
        <p className="ex-muted ex-predict-note">Read the code in the editor. Pick your guess, then press Run to see.</p>
      )}
      {/* Hidden until the student seed is known (after hydration), so the order never jumps. */}
      <div
        className="ex-predict-choices"
        role="group"
        aria-labelledby={titleId}
        data-ready={student !== null}
        style={student === null ? { visibility: "hidden" } : undefined}
      >
        {order.map((index) => {
          const choice = predict.choices[index] ?? "";
          const chosen = guess === index;
          const isAnswer = guess !== null && index === predict.answer;
          const mark = guess === null ? "" : isAnswer ? "✓" : chosen ? "✗" : "";
          return (
            <button
              key={index}
              type="button"
              className={`ex-predict-choice${chosen ? " is-chosen" : ""}${isAnswer ? " is-answer" : ""}`}
              data-testid={`predict-choice-${index}`}
              aria-pressed={chosen}
              onClick={() => choose(index)}
            >
              <span className="ex-predict-mark" aria-hidden="true">
                {mark}
              </span>
              <ChoiceText text={choice} showSpaces={showSpaces} />
              {isAnswer ? <span className="ex-sr-only"> (the right answer)</span> : null}
            </button>
          );
        })}
      </div>
      {showSpaces ? (
        <p className="ex-muted ex-predict-space-note" data-testid="predict-space-note">
          Look closely at the spaces: each <span className="ex-vis-space ex-vis-space-key"> </span> dot is one space.
        </p>
      ) : null}
      <div aria-live="polite">
        {guess !== null ? (
          <div className={`ex-predict-result${right ? " is-right" : ""}`} data-testid="predict-result" data-correct={right}>
            <p className="ex-predict-verdict">
              <span aria-hidden="true">{right ? "✓ " : "↻ "}</span>
              {right ? "Yes, good guess." : "Not this time. Guesses are free: now see what really happens."}
            </p>
            <Prose text={predict.explain} glossary={glossary} />
          </div>
        ) : null}
      </div>
      <div className="ex-predict-actions">
        {guess === null ? (
          <button type="button" className="ex-link-button" data-testid="predict-skip" onClick={() => {
            onAnswer(-1);
            close();
          }}>
            Skip, just let me run it
          </button>
        ) : (
          <button type="button" className="ex-quiet" data-testid="predict-close" onClick={close}>
            Got it
          </button>
        )}
      </div>
    </section>
  );
}
