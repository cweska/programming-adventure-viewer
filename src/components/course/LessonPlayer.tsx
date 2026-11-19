"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { ItemPageProps } from "../../lib/course/contracts";
import type { CourseProgress } from "../../lib/course/contracts";
import { getCourseProgress, markTestedOut, quickCheckQuestions, useCourseProgress } from "../../lib/course/progress";
import {
  afterPart1,
  part1Answered,
  part1Missed,
  part1Missing,
  part1Tried,
  readinessPlan,
  readinessQuestions,
  requiredTasksDone,
  taskAttempted,
  untriedTasks,
  type ReadinessPlan,
} from "../../lib/course/readiness";
import {
  exerciseKey,
  type ChallengeItem,
  type Exercise,
  type Item,
  type LessonItem,
  type ProjectItem,
  type TestoutItem,
} from "../../lib/course/schema";
import { KindBadge, READINESS_TESTOUT_LABEL } from "./CourseBits";
import { itemHref, unitHref } from "./course-links";
import { exerciseIndexFromHash, hashForExercise, soloUnaided, type PlayerMode } from "./exercise-logic";
import { ExercisePlayer, type ExerciseNext } from "./ExercisePlayer";
import { plainText } from "./prose-format";
import { Prose } from "./Prose";
import { questionsNeeded } from "./quiz-grading";

type PlayedItem = LessonItem | ProjectItem | ChallengeItem | TestoutItem;

function isPlayed(item: Item): item is PlayedItem {
  return item.kind === "lesson" || item.kind === "project" || item.kind === "challenge" || item.kind === "testout";
}

/**
 * A Quick Check form's rule, counted: "Pass all 5 tasks and get 3 of the 4 questions right, and the whole unit counts
 * as done." The questions part only when the form needs them (questionsToPass).
 */
function quickCheckRule(
  tasks: number,
  form: ItemPageProps["unit"]["items"][number] | undefined,
  items: ItemPageProps["unit"]["items"],
): string {
  const quiz = form?.questionsToPass ? items.find((entry) => entry.kind === "quiz" && entry.id === `${form.id}-questions`) : undefined;
  const all = tasks === 1 ? "the task" : `all ${tasks} tasks`;
  const questions =
    form?.questionsToPass && quiz?.questionCount ? ` and get ${questionsNeeded(form.questionsToPass, quiz.questionCount)} questions right,` : "";
  return `Pass ${all}${questions} and the whole unit counts as done.`;
}

/** The questions quiz of a form, as the unit summary lists it. */
function questionsOf(unit: ItemPageProps["unit"], formId: string) {
  return unit.items.find((entry) => entry.kind === "quiz" && entry.id === `${formId}-questions`);
}

/**
 * A readiness unit's form (curriculum §5, readiness.ts): what its page says above the tasks. Part 1 has no hints and
 * never ends the unit by itself; a retake form's task counts for the same task in form A; the re-check is practice.
 */
function readinessRule(unit: ItemPageProps["unit"], plan: ReadinessPlan, formId: string): string {
  const form = unit.items.find((entry) => entry.id === formId);
  const tasks = form?.exercises?.length ?? 0;
  const quiz = questionsOf(unit, formId);
  const all = tasks === 1 ? "the task" : `all ${tasks} tasks`;
  const questions = form?.questionsToPass && quiz?.questionCount ? `, and get ${questionsNeeded(form.questionsToPass, quiz.questionCount)} questions right` : "";
  if (formId === plan.required) {
    return `To pass Part 1: pass ${all}${questions}. Stuck on a task? Type your best try, press Run once, then skip it and come back later. Tasks you pass stay ✓ done.`;
  }
  if (plan.forms.includes(formId)) return "Each task you pass here counts for the matching task in Form A. Tasks you pass stay ✓ done.";
  return `This re-check is practice. Pass ${all}${questions}. It does not change your Readiness result.`;
}

/** Where a readiness form's Continue goes, and what its end says (the required form: Mar'tu's notes after a miss). */
function readinessFinish(
  unit: ItemPageProps["unit"],
  plan: ReadinessPlan,
  formId: string,
  progress: CourseProgress,
  allDone: boolean,
): { complete: boolean; text: string; href: string; label: string; questionsHref?: string } {
  const unitPage = unitHref(unit.id);
  if (formId !== plan.required) {
    const form = unit.items.find((entry) => entry.id === formId);
    const questions = form ? quickCheckQuestions(unit.id, form, unit.items, progress) : null;
    const complete = allDone && (questions === null || questions.met);
    if (plan.forms.includes(formId)) {
      return {
        complete,
        text: complete ? "Every task here is done. They count for Form A too." : "A task you pass here counts for the matching task in Form A.",
        href: unitPage,
        label: "Back to the unit",
      };
    }
    return {
      complete,
      text: complete ? "You finished the re-check. Mar'tu: Still solid, yes?" : "Pass every task, and its questions, to finish the re-check.",
      href: unitPage,
      label: "Back to the unit",
    };
  }
  const next = afterPart1(unit.id, unit.items, plan, progress);
  const href = next ? itemHref(unit.id, next) : unitPage;
  const questions = readinessQuestions(unit.id, unit.items, plan, progress);
  const quizId = plan.questions[plan.required];
  const answered = part1Answered(unit.id, plan, progress);
  if (!part1Missed(unit.id, unit.items, plan, progress)) {
    return { complete: true, text: "Part 1 is done. Next: the mini-boss.", href, label: "Continue" };
  }
  if (requiredTasksDone(unit.id, unit.items, plan, progress) && !answered && quizId) {
    return {
      complete: false,
      text: "Every task is done. Part 1 also has its questions: answer them once.",
      href: itemHref(unit.id, quizId),
      label: "Answer the questions",
      questionsHref: itemHref(unit.id, quizId),
    };
  }
  if (part1Tried(unit.id, unit.items, plan, progress)) {
    const short = questions && !questions.met ? ` Part 1 needs ${questionsNeeded(questions.needed, questions.total)} questions right, and ${questions.right} are right so far.` : "";
    return {
      complete: false,
      text: `You tried all of Part 1. Some of it is not ✓ yet.${short} Mar'tu's notes show where to look again.`,
      href,
      label: "Continue",
    };
  }
  // Part 1 A is not tried yet: say what is missing (a task skipped without a Run, or the questions), never only "skip it".
  const missing = part1Missing(unit.id, unit.items, plan, progress);
  if (missing) {
    const onlyQuestions = !answered && quizId !== undefined && untriedTasks(unit.id, unit.items, plan, progress).length === 0;
    return {
      complete: false,
      text: missing,
      href: onlyQuestions ? itemHref(unit.id, quizId) : unitPage,
      label: onlyQuestions ? "Answer the questions" : "Back to the unit",
    };
  }
  return {
    complete: false,
    text: allDone
      ? "Every task is done."
      : "Stuck on a task? Type your best try, press Run once, then skip it and come back to it later. Tasks you pass stay ✓ done.",
    href: unitPage,
    label: "Back to the unit",
  };
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
  // Part 1 A of a readiness unit opens at the first task not tried yet (a task skipped without a Run), then at the first
  // one not done: Next up sends the student back here for exactly that task.
  const requiredForm = mode === "testout" && readinessPlan(unit.items)?.required === item.id;
  const [index, go] = useHashIndex(ids, () => {
    const saved = getCourseProgress().exercises;
    const untried = requiredForm ? keys.findIndex((key) => !taskAttempted(saved[key])) : -1;
    if (untried >= 0 && keys.some((key) => taskAttempted(saved[key]))) return untried;
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
  // A readiness unit (a required test-out, readiness.ts): its forms never test the unit out.
  const plan = readinessPlan(unit.items);
  const testedOut = plan === null && progress.testedOut[unit.id] === true;
  // A form that needs its questions too (questionsToPass): the tasks alone do not pass it.
  const form = mode === "testout" ? unit.items.find((entry) => entry.id === item.id) : undefined;
  const questions = form ? quickCheckQuestions(unit.id, form, unit.items, progress) : null;
  const passed = allDone && (questions === null || questions.met);
  const readiness = plan && mode === "testout" ? readinessFinish(unit, plan, item.id, progress, allDone) : null;

  // A Quick Check passed in full marks the unit as tested out (never in a readiness unit).
  useEffect(() => {
    if (mode === "testout" && plan === null && passed && !testedOut) markTestedOut(unit.id);
  }, [mode, plan, passed, testedOut, unit.id]);

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

  const firstUntried = requiredForm ? keys.findIndex((key) => !taskAttempted(progress.exercises[key])) : -1;
  const firstOpen = firstUntried >= 0 && firstUntried !== index ? firstUntried : doneFlags.findIndex((flag) => !flag);
  let next: ExerciseNext | undefined;
  if (!last) next = { label: `Next ${mode === "testout" ? "task" : "exercise"}`, onClick: () => goTo(index + 1) };
  else if (firstOpen >= 0 && firstOpen !== index) next = { label: `Go to ${mode === "testout" ? "task" : "exercise"} ${firstOpen + 1}`, onClick: () => goTo(firstOpen) };
  else if (readiness) next = { label: readiness.label, href: readiness.href };
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
                  aria-label={`${noun} ${at + 1}: ${plainText(exercise.title)}${isDone ? ", done" : ""}`}
                  title={plainText(exercise.title)}
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
        unitOrder={unit.order}
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

      {readiness ? (
        <ReadinessFinish {...readiness} />
      ) : !embedded ? (
        <ItemFinish
          complete={mode === "testout" ? passed || testedOut : allDone}
          mode={mode}
          nextHref={nextHref}
          unitHrefValue={unitHref(unit.id)}
          tasksDone={allDone}
          questions={questions ? { ...questions, href: itemHref(unit.id, questions.quizId) } : null}
        />
      ) : null}
    </div>
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* The end of an item                                                                              */
/* ---------------------------------------------------------------------------------------------- */

/** The end of a readiness unit's form: never "this unit counts as done" (readinessFinish). */
function ReadinessFinish({ complete, text, href, label }: { complete: boolean; text: string; href: string; label: string }) {
  return (
    <div className="item-footer ex-finish" id="item-finish" tabIndex={-1} data-testid="item-finish" data-readiness="true">
      <p className={complete ? "ex-finish-text" : "ex-muted"} data-testid="readiness-finish" role={complete ? "status" : undefined}>
        {complete ? <span aria-hidden="true">✓ </span> : null}
        {complete ? <strong>{text}</strong> : <Prose text={text} inline />}
      </p>
      <Link className={label === "Back to the unit" ? "ex-quiet-link" : "course-button"} href={href} data-testid="item-continue">
        {label}
      </Link>
    </div>
  );
}

function ItemFinish({
  complete,
  mode,
  nextHref,
  unitHrefValue,
  tasksDone = false,
  questions = null,
}: {
  complete: boolean;
  mode: PlayerMode;
  nextHref: string;
  unitHrefValue: string;
  /** A Quick Check: every task passed. */
  tasksDone?: boolean;
  /** A Quick Check form that needs its questions too: how many, and where they are. */
  questions?: { needed: number; total: number; met: boolean; href: string } | null;
}) {
  if (mode === "testout" && !complete && tasksDone && questions) {
    return (
      <div className="item-footer ex-finish" id="item-finish" tabIndex={-1} data-testid="item-finish">
        <p className="ex-finish-text" data-testid="testout-questions" role="status">
          <span aria-hidden="true">✓</span> <strong>Every task done.</strong> Last part: the questions. Get{" "}
          {questionsNeeded(questions.needed, questions.total)} right, and this unit counts as done.
        </p>
        <Link className="course-button" href={questions.href} data-testid="testout-questions-link">
          Answer the questions
        </Link>
      </div>
    );
  }
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
            {questions
              ? `Pass every task, then get ${questionsNeeded(questions.needed, questions.total)} questions right, to test out.`
              : "Pass every task to test out."}{" "}
            Stuck? That&apos;s fine. The lessons teach all of it.
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

/**
 * A readiness unit's mini-boss or trial (solo, light support: campaign mode, curriculum §2.10): Mar'tu's version opens
 * after 5 minutes on the exercise only, as the intro promises, never after a count of failed runs (teacher site request
 * 4).
 */
export function campaignModeSettings(settings: ItemPageProps["settings"], campaign: boolean): ItemPageProps["settings"] {
  return campaign ? { ...settings, solutionAfterFailedRuns: Number.POSITIVE_INFINITY } : settings;
}

function SinglePlayable({ props, item }: { props: ItemPageProps; item: ProjectItem | ChallengeItem }) {
  const { unit, glossary, nextHref } = props;
  const progress = useCourseProgress();
  const key = exerciseKey(unit.id, item.id);
  const entry = progress.exercises[key];
  const done = entry?.done === true;
  const mode: PlayerMode = item.kind;
  const plan = readinessPlan(unit.items);
  const campaign = plan !== null && item.solo && item.support === "light";
  const settings = campaignModeSettings(props.settings, campaign);
  // The two mini-bosses are one program with other names: Mar'tu's version of either one, opened before this pass,
  // makes it "with Mar'tu's version" (readiness.ts readinessResult).
  const bosses = plan ? [plan.miniBoss, plan.twinBoss].filter((id): id is string => Boolean(id)) : [];
  const isBoss = campaign && bosses.includes(item.id);
  const compareFrom = isBoss ? bosses.filter((id) => id !== item.id).map((id) => exerciseKey(unit.id, id)) : undefined;
  const withCompare = campaign && done && entry?.doneWithCompare === true;
  // Only the mini-boss that decides the result "counts, with a review list": the first one, or the second while the
  // first is not done. The trial is extra: it never changes the result.
  const firstDone = plan?.miniBoss ? progress.exercises[exerciseKey(unit.id, plan.miniBoss)]?.done === true : false;
  const decides = isBoss && (item.id === plan?.miniBoss || !firstDone);
  // After a pass with Mar'tu's version of the first mini-boss: the second one is next, on the student's own (only while
  // its own answer was never shown).
  const twin =
    item.id === plan?.miniBoss && plan.twinBoss ? unit.items.find((candidate) => candidate.id === plan.twinBoss) : undefined;
  const twinEntry = twin ? progress.exercises[exerciseKey(unit.id, twin.id)] : undefined;
  const offerTwin = twin !== undefined && twinEntry?.done !== true && twinEntry?.solutionShown !== true;
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
        unitOrder={unit.order}
        itemId={item.id}
        exerciseKey={key}
        exercise={item}
        glossary={glossary}
        settings={settings}
        mode={mode}
        next={{ label: "Continue", href: nextHref }}
        compareFrom={compareFrom}
      />
      {campaign && done ? (
        <div className="item-footer ex-finish" id="item-finish" tabIndex={-1} data-testid="item-finish" data-readiness="true">
          <p className="ex-finish-text" data-testid="campaign-result" data-with-compare={withCompare ? "true" : "false"} role="status">
            <span aria-hidden="true">✓</span>{" "}
            {withCompare ? (
              <>
                <strong>You finished it with Mar&apos;tu&apos;s version.</strong>
                {decides ? " That counts, with a review list." : null}
                {decides && offerTwin && twin ? (
                  <>
                    {" "}
                    Next: <Link href={itemHref(unit.id, twin.id)} data-testid="campaign-next-boss">{twin.title}</Link>, on your own.
                  </>
                ) : null}
              </>
            ) : soloUnaided(entry) ? (
              <strong>You finished it on your own.</strong>
            ) : (
              // Help went past Where to look: the pass line says "with some help this time", so never "on your own" here.
              <strong>You finished it without Mar&apos;tu&apos;s version.</strong>
            )}
          </p>
          <Link className="course-button" href={nextHref} data-testid="item-continue">
            Continue
          </Link>
        </div>
      ) : (
        <ItemFinish complete={done} mode={mode} nextHref={nextHref} unitHrefValue={unitHref(unit.id)} />
      )}
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
  const plan = readinessPlan(unit.items);

  return (
    <div className={`lesson-player ex-kind-${item.kind}`} data-testid="lesson-player" data-kind={item.kind}>
      <header className="item-header">
        <KindBadge kind={item.kind} label={plan && item.kind === "testout" ? READINESS_TESTOUT_LABEL : undefined} />
        {item.kind === "challenge" && item.level === "advanced" ? <span className="optional-tag ex-level">Advanced</span> : null}
        {item.optional && item.kind !== "testout" ? <span className="optional-tag">Optional</span> : null}
        <h1>{item.title}</h1>
        {item.summary ? <Prose text={item.summary} glossary={props.glossary} className="item-summary" /> : null}
        {item.minutes ? <p className="item-meta">About {item.minutes} min</p> : null}
        {variant ? (
          <p className="item-meta">
            A harder version of <Link href={itemHref(unit.id, variant.id)}>{variant.title}</Link>.
          </p>
        ) : null}
      </header>

      {item.kind === "testout" && plan ? (
        <div className="ex-intro ex-quick-intro" data-testid="testout-intro" data-readiness="true">
          <p>
            {plan.forms.includes(item.id) ? "Part 1 of the Readiness Check" : "The Readiness Re-check"}: no hints. The glossary,
            read-aloud and the error box in the Console still work.
          </p>
          <p className="ex-muted" data-testid="testout-rule">
            {readinessRule(unit, plan, item.id)}
          </p>
        </div>
      ) : item.kind === "testout" ? (
        <div className="ex-intro ex-quick-intro" data-testid="testout-intro">
          <p>
            Already know this? Show Mar&apos;tu. No pressure: if something&apos;s new,{" "}
            <Link href={unitHref(unit.id)}>the lessons are right here</Link>.
          </p>
          <p className="ex-muted" data-testid="testout-rule">
            No hints in a Quick Check. {quickCheckRule(item.exercises.length, unit.items.find((entry) => entry.id === item.id), unit.items)}
          </p>
        </div>
      ) : null}

      {item.kind === "lesson" ? <ExerciseRow props={props} exercises={item.exercises} mode="lesson" embedded={false} /> : null}
      {item.kind === "testout" ? <ExerciseRow props={props} exercises={item.exercises} mode="testout" embedded={false} /> : null}
      {item.kind === "project" || item.kind === "challenge" ? <SinglePlayable props={props} item={item} /> : null}
    </div>
  );
}
