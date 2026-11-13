"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { ItemPageProps } from "../../lib/course/contracts";
import { getCourseProgress, markTestedOut, useCourseProgress } from "../../lib/course/progress";
import {
  exerciseKey,
  type ChallengeItem,
  type Exercise,
  type Item,
  type LessonItem,
  type ProjectItem,
  type TestoutItem,
} from "../../lib/course/schema";
import { KindBadge } from "./CourseBits";
import { unitHref } from "./course-links";
import { exerciseIndexFromHash, hashForExercise, type PlayerMode } from "./exercise-logic";
import { ExercisePlayer, type ExerciseNext } from "./ExercisePlayer";
import { Prose } from "./Prose";

type PlayedItem = LessonItem | ProjectItem | ChallengeItem | TestoutItem;

function isPlayed(item: Item): item is PlayedItem {
  return item.kind === "lesson" || item.kind === "project" || item.kind === "challenge" || item.kind === "testout";
}

/* ---------------------------------------------------------------------------------------------- */
/* Lessons and Quick Checks: a row of exercises                                                    */
/* ---------------------------------------------------------------------------------------------- */

/**
 * Read the current exercise from the URL hash (#<exerciseId>), keep it there with replaceState, and follow
 * hash changes. With no hash, open the first exercise not done yet (`fallback`).
 */
function useHashIndex(ids: string[], fallback: () => number): [number, (index: number) => void] {
  const [index, setIndex] = useState(0);
  const idsKey = ids.join("|");
  const fallbackRef = useRef(fallback);
  fallbackRef.current = fallback;

  useEffect(() => {
    const list = idsKey.split("|");
    const read = () => {
      const hash = window.location.hash.replace(/^#/, "");
      setIndex(hash ? exerciseIndexFromHash(hash, list) : Math.max(0, Math.min(list.length - 1, fallbackRef.current())));
    };
    read();
    window.addEventListener("hashchange", read);
    return () => window.removeEventListener("hashchange", read);
  }, [idsKey]);

  const go = (next: number) => {
    const clamped = Math.max(0, Math.min(ids.length - 1, next));
    setIndex(clamped);
    try {
      window.history.replaceState(window.history.state, "", hashForExercise(ids[clamped]));
    } catch {
      // Some embedded browsers block history changes; the exercise still changes.
    }
  };
  return [index, go];
}

function ExerciseRow({
  props,
  exercises,
  mode,
  embedded,
}: {
  props: ItemPageProps;
  exercises: Exercise[];
  mode: PlayerMode;
  /** Inside another page (an article's try-it): no "Continue" of our own. */
  embedded: boolean;
}) {
  const { unit, item, glossary, settings, nextHref } = props;
  const progress = useCourseProgress();
  const ids = exercises.map((exercise) => exercise.id);
  const keys = exercises.map((exercise) => exerciseKey(unit.id, item.id, exercise.id));
  const [index, go] = useHashIndex(ids, () => {
    const saved = getCourseProgress().exercises;
    const open = keys.findIndex((key) => saved[key]?.done !== true);
    return open < 0 ? 0 : open;
  });
  const topRef = useRef<HTMLParagraphElement>(null);
  const moved = useRef(false);
  const doneFlags = keys.map((key) => progress.exercises[key]?.done === true);
  const allDone = doneFlags.every(Boolean);
  const current = exercises[index] ?? exercises[0];
  const currentDone = doneFlags[index] === true;
  const last = index === exercises.length - 1;
  const testedOut = progress.testedOut[unit.id] === true;

  // A Quick Check passed in full marks the unit as tested out.
  useEffect(() => {
    if (mode === "testout" && allDone && !testedOut) markTestedOut(unit.id);
  }, [mode, allDone, testedOut, unit.id]);

  // After Back / Next / a dot, bring the top of the exercise into view and give it focus.
  useEffect(() => {
    if (!moved.current) return;
    moved.current = false;
    const top = topRef.current;
    if (!top) return;
    top.focus({ preventScroll: true });
    top.scrollIntoView({ block: "start" });
  }, [index]);

  const goTo = (next: number) => {
    moved.current = true;
    go(next);
  };

  const firstOpen = doneFlags.findIndex((flag) => !flag);
  let next: ExerciseNext | undefined;
  if (!last) next = { label: `Next ${mode === "testout" ? "task" : "exercise"}`, onClick: () => goTo(index + 1) };
  else if (firstOpen >= 0 && firstOpen !== index) next = { label: `Go to ${mode === "testout" ? "task" : "exercise"} ${firstOpen + 1}`, onClick: () => goTo(firstOpen) };
  else if (!embedded) next = { label: "Continue", href: nextHref };
  const noun = mode === "testout" ? "Task" : "Exercise";

  return (
    <div className="ex-row" data-testid="exercise-row">
      <nav className="ex-stepper" aria-label={`${noun}s in ${item.title}`} data-testid="exercise-rail">
        <p className="ex-stepper-label" data-testid="exercise-label" ref={topRef} tabIndex={-1}>
          {noun} {index + 1} of {exercises.length}
        </p>
        <ol className="ex-dots">
          {exercises.map((exercise, at) => {
            const isCurrent = at === index;
            const isDone = doneFlags[at];
            return (
              <li key={exercise.id}>
                <a
                  href={hashForExercise(exercise.id)}
                  className={`ex-dot${isCurrent ? " is-current" : ""}${isDone ? " is-done" : ""}`}
                  data-testid={`exercise-dot-${at + 1}`}
                  aria-current={isCurrent ? "step" : undefined}
                  aria-label={`${noun} ${at + 1}: ${exercise.title}${isDone ? ", done" : ""}`}
                  title={exercise.title}
                  onClick={(event) => {
                    event.preventDefault();
                    goTo(at);
                  }}
                >
                  <span aria-hidden="true">{isDone ? "✓" : at + 1}</span>
                </a>
              </li>
            );
          })}
        </ol>
      </nav>

      <ExercisePlayer
        key={keys[index]}
        unitId={unit.id}
        itemId={item.id}
        exerciseKey={keys[index]}
        exercise={current}
        glossary={glossary}
        settings={settings}
        mode={mode}
        next={next}
      />

      <div className="ex-nav" data-testid="exercise-nav">
        <button
          type="button"
          className="ex-quiet"
          data-testid="exercise-back"
          onClick={() => goTo(index - 1)}
          disabled={index === 0}
        >
          <span aria-hidden="true">←</span> Back
        </button>
        {!last ? (
          <div className="ex-nav-next">
            <button type="button" data-testid="exercise-next" onClick={() => goTo(index + 1)} disabled={!currentDone}>
              Next <span aria-hidden="true">→</span>
            </button>
            {!currentDone ? (
              <p className="ex-muted ex-nav-note">Next opens when every step is done. You can also jump with the numbers above.</p>
            ) : null}
          </div>
        ) : null}
      </div>

      {!embedded ? (
        <ItemFinish
          complete={mode === "testout" ? allDone || testedOut : allDone}
          mode={mode}
          nextHref={nextHref}
          unitHrefValue={unitHref(unit.id)}
        />
      ) : null}
    </div>
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* The end of an item                                                                              */
/* ---------------------------------------------------------------------------------------------- */

function ItemFinish({
  complete,
  mode,
  nextHref,
  unitHrefValue,
}: {
  complete: boolean;
  mode: PlayerMode;
  nextHref: string;
  unitHrefValue: string;
}) {
  if (mode === "testout") {
    return (
      <div className="item-footer ex-finish" id="item-finish" tabIndex={-1} data-testid="item-finish">
        {complete ? (
          <p className="ex-finish-text" data-testid="testout-result" role="status">
            <span aria-hidden="true">✓</span> <strong>You showed Mar&apos;tu.</strong> This unit now counts as done. You can still
            try any lesson or side quest you like.
          </p>
        ) : (
          <p className="ex-muted" data-testid="testout-pending">
            Pass every task to test out. Stuck? That is fine. The lessons teach all of it.
          </p>
        )}
        <Link className={complete ? "course-button" : "ex-quiet-link"} href={complete ? nextHref : unitHrefValue} data-testid="item-continue">
          {complete ? "Continue" : "Back to the unit"}
        </Link>
      </div>
    );
  }
  const what = mode === "lesson" ? "lesson" : mode;
  return (
    <div className="item-footer ex-finish" id="item-finish" tabIndex={-1} data-testid="item-finish">
      {complete ? (
        <p className="ex-finish-text" data-testid="item-complete" role="status">
          <span aria-hidden="true">✓</span> <strong>You finished this {what}.</strong> Mar&apos;tu adds a chalk tally to the wall.
        </p>
      ) : (
        <p className="ex-muted">You can come back to this {what} any time. Your code is saved.</p>
      )}
      <Link className={complete ? "course-button" : "ex-quiet-link"} href={nextHref} data-testid="item-continue">
        {complete ? "Continue" : "Skip ahead for now"}
      </Link>
    </div>
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* Projects and challenges: one exercise                                                           */
/* ---------------------------------------------------------------------------------------------- */

function SinglePlayable({ props, item }: { props: ItemPageProps; item: ProjectItem | ChallengeItem }) {
  const { unit, glossary, settings, nextHref } = props;
  const progress = useCourseProgress();
  const key = exerciseKey(unit.id, item.id);
  const done = progress.exercises[key]?.done === true;
  const mode: PlayerMode = item.kind;
  return (
    <div className="ex-single">
      {item.kind === "project" && item.intro ? (
        <div className="ex-intro" data-testid="project-intro">
          <Prose text={item.intro} glossary={glossary} />
        </div>
      ) : null}
      <ExercisePlayer
        key={key}
        unitId={unit.id}
        itemId={item.id}
        exerciseKey={key}
        exercise={item}
        glossary={glossary}
        settings={settings}
        mode={mode}
        next={{ label: "Continue", href: nextHref }}
      />
      <ItemFinish complete={done} mode={mode} nextHref={nextHref} unitHrefValue={unitHref(unit.id)} />
    </div>
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* The item page body for lessons, projects, challenges and Quick Checks                           */
/* ---------------------------------------------------------------------------------------------- */

export function LessonPlayer(props: ItemPageProps) {
  const { unit, item } = props;
  if (!isPlayed(item)) {
    return <p className="course-empty">This page is not ready yet.</p>;
  }

  // An article's try-it exercises arrive as a lesson with the article's id: play them inline.
  const host = unit.items.find((entry) => entry.id === item.id);
  const embedded = item.kind === "lesson" && host !== undefined && host.kind !== "lesson";
  if (embedded) {
    return (
      <div className="lesson-player is-embedded" data-testid="lesson-player" data-kind="try-it">
        <ExerciseRow props={props} exercises={item.exercises} mode="try-it" embedded />
      </div>
    );
  }

  const variant =
    item.kind === "challenge" && item.variantOf ? unit.items.find((entry) => entry.id === item.variantOf) : undefined;

  return (
    <div className={`lesson-player kind-${item.kind}`} data-testid="lesson-player" data-kind={item.kind}>
      <header className="item-header">
        <KindBadge kind={item.kind} />
        {item.kind === "challenge" && item.level === "advanced" ? <span className="optional-tag ex-level">Advanced</span> : null}
        {item.optional && item.kind !== "testout" ? <span className="optional-tag">Optional</span> : null}
        <h1>{item.title}</h1>
        {item.summary ? <p className="item-summary">{item.summary}</p> : null}
        {item.minutes ? <p className="item-meta">About {item.minutes} min</p> : null}
        {variant ? (
          <p className="item-meta">
            A harder version of <Link href={`${unitHref(unit.id)}/${variant.id}`}>{variant.title}</Link>.
          </p>
        ) : null}
      </header>

      {item.kind === "testout" ? (
        <div className="ex-intro ex-quick-intro" data-testid="testout-intro">
          <p>
            Already know this? Show Mar&apos;tu. No pressure: if something&apos;s new,{" "}
            <Link href={unitHref(unit.id)}>the lessons are right here</Link>.
          </p>
          <p className="ex-muted">No hints in a Quick Check. Pass every task and the whole unit counts as done.</p>
        </div>
      ) : null}

      {item.kind === "lesson" ? <ExerciseRow props={props} exercises={item.exercises} mode="lesson" embedded={false} /> : null}
      {item.kind === "testout" ? <ExerciseRow props={props} exercises={item.exercises} mode="testout" embedded={false} /> : null}
      {item.kind === "project" || item.kind === "challenge" ? <SinglePlayable props={props} item={item} /> : null}
    </div>
  );
}
