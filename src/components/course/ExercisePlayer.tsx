"use client";

import Link from "next/link";
import { useEffect, useId, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import type { ExerciseProgress, GradeResult } from "../../lib/course/contracts";
import { explainCourseError } from "../../lib/course/explain";
import { flattenChecks, gradeCheckpoints } from "../../lib/course/grading";
import { getCourseProgress, progressIsSaving, updateExercise, useCourseProgress } from "../../lib/course/progress";
import type { Bonus, Checkpoint, GlossaryEntry, Playable } from "../../lib/course/schema";
import { runCourse, whenPythonReady } from "../../lib/languages/python/run";
import type { Explanation } from "../../lib/languages/types";
import { publicPath } from "../../lib/site";
import type { StageEvent } from "../../lib/stage/bridge";
import { PythonEditor, type PythonEditorHandle } from "../PythonEditor";
import { CompareView } from "./CompareView";
import {
  angleLabel,
  answersFromBox,
  anotherWayOpen,
  applyRun,
  assembledCode,
  checkpointHeading,
  countsAsAttempt,
  effectiveSupport,
  firstParagraph,
  helpOffer,
  helpRungs,
  helpState,
  hintButtonLabel,
  hintsOpen,
  isBlankOrStarter,
  isSolutionCode,
  nextFailStreak,
  pickInsertion,
  presetOf,
  revealNextRung,
  rungPaced,
  rungsShown,
  runOutcome,
  solutionUnlocked,
  stdinBoxText,
  stepNoun,
  stuckCheckpointId,
  titleFromId,
  usesInput,
  type FailStreak,
  type PlayerExtras,
  type PlayerMode,
  type Support,
} from "./exercise-logic";
import { HelpLocked, HelpStack, type RevealResult } from "./HelpStack";
import { MarTu } from "./MarTu";
import { NamesChips } from "./NamesChips";
import { ParsonsBoard } from "./ParsonsBoard";
import { seededShuffle } from "./parsons-logic";
import { PredictStep } from "./PredictStep";
import { Prose } from "./Prose";
import { ReadAloud } from "./ReadAloud";
import { SymbolTray } from "./SymbolTray";
import { PYTHON_STATUS_TEXT, type PythonStatus } from "./usePythonStatus";

/** The console shows at most this much output (a print loop can make 200,000 characters). */
const MAX_SHOWN_OUTPUT = 20_000;

function shownOutput(stdout: string): string {
  const text = stdout.replace(/\n$/, "");
  if (text.length <= MAX_SHOWN_OUTPUT) return text;
  return `${text.slice(0, MAX_SHOWN_OUTPUT)}\n… (Your program printed a lot more. Only the start is shown.)`;
}

/** Where the bonus side quest's hint count is kept in hintsUsed. */
const BONUS_ID = "__bonus";
/** How long typing waits before the code is saved. */
const CODE_SAVE_MS = 400;
/** How often visible time is counted, and saved. */
const TICK_MS = 5_000;
const SAVE_TIME_EVERY_MS = 15_000;

const CAMEO_NAMES: Record<Bonus["by"], string> = {
  "mar-tu": "Mar'tu",
  oogrish: "Oogrish",
  gearshift: "Gearshift",
  "bomb-shell": "Bomb Shell",
  lucky: "Lucky",
};

export type ExerciseNext = { label: string; onClick?: () => void; href?: string };

export type ExercisePlayerProps = {
  unitId: string;
  itemId: string;
  /** exerciseKey(unitId, itemId, exerciseId?) from schema.ts: where progress is saved. */
  exerciseKey: string;
  exercise: Playable;
  glossary: GlossaryEntry[];
  settings: { solutionAfterMinutes: number; solutionAfterFailedRuns: number; quizReadyPercent?: number };
  mode: PlayerMode;
  /** The "Next" button shown once the exercise is done (LessonPlayer passes it). */
  next?: ExerciseNext;
  /** Called once when a run passes every checkpoint. */
  onDone?: () => void;
};

type RunView = {
  stdout: string;
  grade: GradeResult | null;
  bonus: GradeResult | null;
  explanation: Explanation | null;
  /** Python itself could not run the code. */
  failure?: string;
  stage: StageEvent[];
  allPassed: boolean;
  /** The exercise was already done before this run (so the side quest is what the student is working on). */
  wasDone: boolean;
  /** Bumps every run so the live region re-announces the same words. */
  runNumber: number;
  /** This crash is the same as the last run's (so the student can tell the run happened). */
  sameError?: boolean;
  /** The same step failed with the same message as last run. */
  sameMessage?: boolean;
  /** Steps that passed for the first time in this run (the step list says "Done!" on them). */
  newlyPassed: string[];
  /** This run passed with Mar'tu's version, copied in with "Copy into my editor". */
  revealPass?: boolean;
};

/** The student's line in a course traceback (the last `File "main.py", line N`). */
function crashLine(traceback: string): number | null {
  const frames = [...traceback.matchAll(/File "main\.py", line (\d+)/g)];
  const last = frames.at(-1);
  return last ? Number(last[1]) : null;
}

function bonusCheckpoint(bonus: Bonus): Checkpoint {
  return { id: BONUS_ID, text: bonus.text, hints: bonus.hints, checks: bonus.checks };
}

function sameAnswers(a: readonly string[], b: readonly string[]): boolean {
  return a.length === b.length && a.every((answer, index) => answer === b[index]);
}

function stageLines(events: StageEvent[]): string[] {
  const lines: string[] = [];
  for (const event of events) {
    if (event.type === "prompt" || event.type === "say") lines.push(event.text);
    else if (event.type === "options") lines.push(...event.options.map((option, index) => `${index + 1}) ${option}`));
    else if (event.type === "speak") lines.push(`You say: ${event.option}`);
  }
  return lines.filter((line) => line.trim().length > 0);
}

/* ---------------------------------------------------------------------------------------------- */
/* Visible time on this exercise (for Mar'tu's version and Help offers)                            */
/* ---------------------------------------------------------------------------------------------- */

/** Visible time on the exercise: `total` across visits, `session` in this visit. */
function useActiveTime(key: string): { total: number; session: number } {
  const [sessionMs, setSessionMs] = useState(0);
  const [storedMs, setStoredMs] = useState(0);
  const unsaved = useRef(0);

  useEffect(() => {
    const saved = getCourseProgress().exercises[key];
    setStoredMs(saved?.activeMs ?? 0);
    setSessionMs(0);
    unsaved.current = 0;
    if (!saved?.firstSeenAt) updateExercise(key, (previous) => ({ ...previous, firstSeenAt: previous.firstSeenAt ?? Date.now() }));

    let last = Date.now();
    let session = 0;
    let sinceSave = 0;
    const save = () => {
      const add = unsaved.current;
      if (add <= 0) return;
      unsaved.current = 0;
      sinceSave = 0;
      updateExercise(key, (previous) => ({ ...previous, activeMs: (previous.activeMs ?? 0) + add }));
    };
    const tick = () => {
      const now = Date.now();
      // Cap each step so a sleeping laptop does not count as hours of work.
      const step = Math.min(now - last, TICK_MS * 2);
      last = now;
      if (document.visibilityState !== "visible" || step <= 0) return;
      session += step;
      sinceSave += step;
      unsaved.current += step;
      setSessionMs(session);
      if (sinceSave >= SAVE_TIME_EVERY_MS) save();
    };
    const onVisibility = () => {
      if (document.visibilityState === "hidden") {
        tick();
        save();
      } else {
        last = Date.now();
      }
    };
    const timer = window.setInterval(tick, TICK_MS);
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("pagehide", save);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("pagehide", save);
      tick();
      save();
    };
  }, [key]);

  return { total: storedMs + sessionMs, session: sessionMs };
}

/* ---------------------------------------------------------------------------------------------- */
/* Pieces of the Learn pane                                                                        */
/* ---------------------------------------------------------------------------------------------- */

function WorkedExample({ example }: { example: NonNullable<Playable["example"]> }) {
  return (
    <figure className="ex-example" data-testid="worked-example">
      <figcaption className="ex-example-label">
        <span className="ex-example-tag">Example</span> not your task
      </figcaption>
      <p className="ex-example-note">Read it and see what it prints. Your task is in the steps below.</p>
      <pre className="ex-example-code" aria-label="Example code" data-testid="example-code">
        <code>{example.code.replace(/\n$/, "")}</code>
      </pre>
      {example.stdin && example.stdin.length > 0 ? (
        <p className="ex-example-stdin">
          When it asks, the answer{example.stdin.length > 1 ? "s are" : " is"}:{" "}
          {example.stdin.map((answer, at) => (
            <span key={at}>
              {at > 0 ? ", " : null}
              <code className="inline-code">{answer}</code>
            </span>
          ))}
        </p>
      ) : null}
      <p className="ex-example-prints">It prints:</p>
      <pre className="ex-example-output" aria-label="What the example prints" data-testid="example-output">
        {example.output.replace(/\n$/, "") || "(nothing)"}
      </pre>
    </figure>
  );
}

function AnotherWay({ exercise, glossary }: { exercise: Playable; glossary: GlossaryEntry[] }) {
  const angles = exercise.anotherWay;
  const [index, setIndex] = useState(-1);
  const shown = index >= 0 ? angles[index] : null;
  const nextIndex = (index + 1) % angles.length;
  const showNext = index < 0 || angles.length > 1;

  return (
    <div className="ex-another" data-testid="another-way-box">
      <div className="ex-another-buttons">
        {showNext ? (
          <button type="button" className="ex-quiet" data-testid="another-way" onClick={() => setIndex(nextIndex)}>
            {index < 0 ? "Explain it another way" : "Another way"}: {angleLabel(angles[nextIndex])}
          </button>
        ) : null}
        {shown ? (
          <button type="button" className="ex-quiet" data-testid="another-way-hide" onClick={() => setIndex(-1)}>
            Hide it
          </button>
        ) : null}
      </div>
      <div aria-live="polite">
      {shown ? (
        <div className="ex-another-text" data-testid="another-way-text">
          <p className="ex-another-title">
            {angleLabel(shown)}
            {angles.length > 1 ? (
              <span className="ex-muted">
                {" "}
                ({index + 1} of {angles.length})
              </span>
            ) : null}
          </p>
          <Prose text={shown.text} glossary={glossary} />
          <ReadAloud text={shown.text} testId="read-aloud-another-way" />
        </div>
      ) : null}
      </div>
    </div>
  );
}

function CampaignLink({ link, glossary }: { link: NonNullable<Playable["campaignLink"]>; glossary: GlossaryEntry[] }) {
  return (
    <details className="ex-campaign" data-testid="campaign-link">
      <summary>
        <img className="ex-cameo" src={publicPath("/sprites/lucky.svg")} alt="" aria-hidden="true" />
        <span>
          <span className="ex-cameo-name">Lucky:</span> &ldquo;What&apos;s in it for me?&rdquo;
        </span>
      </summary>
      <div className="ex-campaign-body">
        <Prose text={link.why} glossary={glossary} />
        {link.snippet ? (
          <pre className="ex-campaign-code" aria-label="Code from the campaign">
            <code>{link.snippet.replace(/\n$/, "")}</code>
          </pre>
        ) : null}
        <p className="ex-muted">
          In the campaign: {titleFromId(link.module)}, {titleFromId(link.part)}.
        </p>
      </div>
    </details>
  );
}

function HintLadder({
  hints,
  shown,
  open,
  lockedNote,
  glossary,
  onReveal,
  testPrefix,
  label,
}: {
  hints: string[];
  shown: number;
  open: boolean;
  lockedNote: string | null;
  glossary: GlossaryEntry[];
  onReveal: () => void;
  /** e.g. "1" gives hint-button-1 and hint-1-1, hint-1-2 ... */
  testPrefix: string;
  label: string;
}) {
  if (hints.length === 0) return null;
  const allShown = shown >= hints.length;
  if (!open) return lockedNote ? <p className="ex-hint-locked ex-muted">{lockedNote}</p> : null;
  return (
    <div className="ex-hints">
      <ol className="ex-hint-list" aria-label={`Hints for ${label}`} aria-live="polite">
        {hints.slice(0, shown).map((hint, index) => (
          <li key={index} className="ex-hint" data-testid={`hint-${testPrefix}-${index + 1}`}>
            <span className="ex-hint-label">
              Hint {index + 1} of {hints.length}
            </span>
            <Prose text={hint} glossary={glossary} />
          </li>
        ))}
      </ol>
      <button
        type="button"
        className="ex-hint-button"
        data-testid={`hint-button-${testPrefix}`}
        onClick={allShown ? undefined : onReveal}
        aria-disabled={allShown}
        aria-label={`${hintButtonLabel(shown, hints.length)} for ${label}`}
      >
        <span aria-hidden="true">💡</span> {hintButtonLabel(shown, hints.length)}
      </button>
    </div>
  );
}

type CheckpointState = "passed" | "active" | "pending";

const STATE_MARK: Record<CheckpointState, { icon: string; words: string }> = {
  passed: { icon: "✓", words: "Done" },
  active: { icon: "●", words: "Up next" },
  pending: { icon: "○", words: "Not done yet" },
};

/* ---------------------------------------------------------------------------------------------- */
/* The player                                                                                      */
/* ---------------------------------------------------------------------------------------------- */

export function ExercisePlayer({
  exerciseKey: key,
  exercise,
  glossary,
  settings,
  mode,
  next,
  onDone,
}: ExercisePlayerProps) {
  const progress = useCourseProgress();
  const saved: ExerciseProgress | undefined = progress.exercises[key];
  const passed = useMemo(() => saved?.passed ?? [], [saved]);
  const done = saved?.done === true;
  const support: Support = effectiveSupport(mode, exercise.support);
  const light = progress.settings.light === true;
  const noun = stepNoun(mode);
  const bonus = mode === "testout" ? undefined : exercise.bonus;
  const inputId = useId();

  const [code, setCode] = useState(exercise.starter);
  const codeRef = useRef(exercise.starter);
  const pendingSave = useRef<string | null>(null);
  const saveTimer = useRef<number | null>(null);
  const [resumed, setResumed] = useState(false);
  const [saving, setSaving] = useState(true);

  const [python, setPython] = useState<PythonStatus>("loading");
  /** Python has been ready once: from then on Run never gets `disabled` (that would drop keyboard focus). */
  const [everReady, setEverReady] = useState(false);
  const [running, setRunning] = useState(false);
  const lastRunSource = useRef<string | null>(null);
  const [view, setView] = useState<RunView | null>(null);
  const [justFinished, setJustFinished] = useState(false);
  const [missedThisVisit, setMissedThisVisit] = useState(false);
  const [streak, setStreak] = useState<FailStreak>({ checkpointId: null, count: 0 });
  const streakRef = useRef<FailStreak>({ checkpointId: null, count: 0 });
  const [nudgeDismissed, setNudgeDismissed] = useState(false);
  const [nudgeHint, setNudgeHint] = useState<{ checkpointId: string; rung: number } | null>(null);
  const missAt = useRef<number | null>(null);
  const typedAt = useRef<number>(0);
  const [now, setNow] = useState(0);

  const [confirm, setConfirm] = useState<"reset" | "solution" | null>(null);
  const [solutionNote, setSolutionNote] = useState(false);
  const [assembling, setAssembling] = useState(false);
  const [assembled, setAssembled] = useState<string[]>([]);
  const [stdinText, setStdinText] = useState(stdinBoxText(exercise.stdin));

  const activeMs = useActiveTime(key);
  const runButton = useRef<HTMLButtonElement>(null);
  const assembleHeading = useRef<HTMLHeadingElement>(null);
  const nudgeThanks = useRef<HTMLButtonElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const confirmRef = useRef<HTMLDivElement>(null);
  const toolbarRef = useRef<HTMLDivElement>(null);

  /* Load: Python, the saved code, whether this browser saves. */
  useEffect(() => {
    let alive = true;
    whenPythonReady().then(
      () => alive && setPython("ready"),
      () => alive && setPython("failed"),
    );
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    if (python === "ready") setEverReady(true);
  }, [python]);

  useEffect(() => {
    const savedCode = getCourseProgress().exercises[key]?.code;
    if (savedCode !== undefined && savedCode !== codeRef.current) {
      codeRef.current = savedCode;
      setCode(savedCode);
      setResumed(savedCode.trim() !== exercise.starter.trim());
    }
    setSaving(progressIsSaving());
    // Restore once per exercise (exercise.starter belongs to the same key); later changes come from here.
  }, [key]);

  /* Save typing after a short pause, and before the page goes away. */
  const saveCodeNow = useRef(() => {});
  saveCodeNow.current = () => {
    if (saveTimer.current !== null) {
      window.clearTimeout(saveTimer.current);
      saveTimer.current = null;
    }
    const pending = pendingSave.current;
    if (pending === null) return;
    pendingSave.current = null;
    updateExercise(key, (previous) => ({ ...previous, code: pending }));
  };

  useEffect(() => {
    const flush = () => saveCodeNow.current();
    const onVisibility = () => {
      if (document.visibilityState === "hidden") flush();
    };
    window.addEventListener("pagehide", flush);
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      window.removeEventListener("pagehide", flush);
      document.removeEventListener("visibilitychange", onVisibility);
      flush();
    };
  }, []);

  /* A slow clock for the "Want a hint?" nudge after a quiet minute and a half. */
  useEffect(() => {
    if (support !== "full") return;
    const timer = window.setInterval(() => setNow(Date.now()), TICK_MS);
    return () => window.clearInterval(timer);
  }, [support]);

  /* After each run, bring the result into view (on a phone the console is below the editor). */
  const runNumber = view?.runNumber ?? 0;
  useEffect(() => {
    if (runNumber === 0) return;
    const root = rootRef.current;
    const target =
      root?.querySelector<HTMLElement>('[data-testid="exercise-done"].is-fresh') ??
      root?.querySelector<HTMLElement>('[data-testid="console"]');
    try {
      target?.scrollIntoView({ block: "nearest" });
    } catch {
      // Old browsers without scrollIntoView options: the result is still there, just not scrolled to.
    }
  }, [runNumber]);

  useEffect(() => {
    // Start on the safe choice ("Keep my code" / "Not yet").
    if (confirm) confirmRef.current?.querySelector<HTMLButtonElement>(".reset-cancel")?.focus();
  }, [confirm]);

  // "Assemble it" removes its own button: move the keyboard to the board instead of losing it.
  useEffect(() => {
    if (assembling) assembleHeading.current?.focus();
  }, [assembling]);

  function changeCode(value: string) {
    codeRef.current = value;
    setCode(value);
    typedAt.current = Date.now();
    pendingSave.current = value;
    if (saveTimer.current !== null) window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(() => saveCodeNow.current(), CODE_SAVE_MS);
  }

  function replaceCode(value: string) {
    changeCode(value);
    saveCodeNow.current();
  }

  /* What is on screen. */
  const showInputBox = exercise.stdin !== undefined || usesInput(code);
  const stdinAnswers = answersFromBox(stdinText, exercise.stdin);
  const answersChanged = exercise.stdin !== undefined && !sameAnswers(stdinAnswers, exercise.stdin);
  const triedAndMissed = missedThisVisit || (saved?.failedRuns ?? 0) > 0 || passed.length > 0 || done;
  const hintsAreOpen = hintsOpen(support, triedAndMissed);
  const firstOpen = exercise.checkpoints.findIndex((checkpoint) => !passed.includes(checkpoint.id));
  const activeCheckpoint = firstOpen >= 0 ? exercise.checkpoints[firstOpen] : null;
  const canShowSolution =
    support !== "none" &&
    solutionUnlocked({
      support,
      activeMs,
      failedRuns: saved?.failedRuns ?? 0,
      solutionAfterMinutes: settings.solutionAfterMinutes,
      solutionAfterFailedRuns: settings.solutionAfterFailedRuns,
      hintsUsedUp:
        activeCheckpoint !== null &&
        activeCheckpoint.hints.length > 0 &&
        rungsShown(saved?.hintsUsed, activeCheckpoint.id, activeCheckpoint.hints.length) >= activeCheckpoint.hints.length,
    });
  const canAssemble = Boolean(exercise.assemble) && support !== "none" && isBlankOrStarter(code, exercise.starter);
  const pieces = useMemo(
    () => (exercise.assemble ? seededShuffle([...exercise.assemble.lines, ...exercise.assemble.distractors], key) : []),
    [exercise.assemble, key],
  );

  const stuckIndex = streak.checkpointId
    ? exercise.checkpoints.findIndex((checkpoint) => checkpoint.id === streak.checkpointId)
    : -1;
  const stuck = stuckIndex >= 0 ? exercise.checkpoints[stuckIndex] : null;
  const stuckShown = stuck ? rungsShown(saved?.hintsUsed, stuck.id, stuck.hints.length) : 0;
  const idleSinceMiss =
    missAt.current !== null && now > 0 ? now - Math.max(missAt.current, typedAt.current) : null;
  const nudging =
    !done &&
    Boolean(stuck) &&
    shouldNudge({
      support,
      streak,
      idleSinceMissMs: idleSinceMiss,
      hintsLeft: stuck ? stuck.hints.length - stuckShown : 0,
      dismissed: nudgeDismissed,
    });

  function revealHint(checkpointId: string, total: number) {
    updateExercise(key, (previous) => ({ ...previous, hintsUsed: revealNextRung(previous.hintsUsed, checkpointId, total) }));
  }

  async function run() {
    if (running) return;
    saveCodeNow.current();
    const source = codeRef.current;
    setRunning(true);
    setConfirm(null);
    setSolutionNote(false);
    try {
      if (python !== "ready") {
        setPython("loading");
        await whenPythonReady();
        setPython("ready");
      }
      const bonusCp = bonus ? bonusCheckpoint(bonus) : null;
      const mainChecks = flattenChecks(exercise.checkpoints);
      const checks = [...mainChecks, ...(bonusCp ? flattenChecks([bonusCp]) : [])];
      const answers = showInputBox ? stdinAnswers : (exercise.stdin ?? []);
      const result = await runCourse({
        code: source,
        checks,
        setup: exercise.setup,
        stdin: answers,
        engine: exercise.engine,
      });
      const grade = gradeCheckpoints(exercise.checkpoints, result, source);
      // The side quest's checks come after the main ones: grade them from their own slice, by position.
      const bonusGrade =
        bonusCp && !grade.crashed
          ? gradeCheckpoints([bonusCp], { ...result, checks: (result.checks ?? []).slice(mainChecks.length) }, source)
          : null;
      const savedBefore = getCourseProgress().exercises[key];
      const before = savedBefore?.passed ?? [];
      const wasDone = savedBefore?.done === true;
      const graded = runOutcome(grade, before);
      // Only real tries count toward "Show solution": not the untouched starter, not the same code again.
      const outcome = { ...graded, failed: graded.failed && countsAsAttempt(source, exercise.starter, lastRunSource.current) };
      lastRunSource.current = source;
      updateExercise(key, (previous) => applyRun(previous, outcome, { code: source, bonusPassed: bonusGrade?.allPassed }));

      const stuckOn = stuckCheckpointId(exercise.checkpoints, grade, [...before, ...outcome.passedNow]);
      const nextStreak = nextFailStreak(streakRef.current, stuckOn);
      if (nextStreak.checkpointId !== streakRef.current.checkpointId) {
        setNudgeDismissed(false);
        setNudgeHint(null);
      }
      streakRef.current = nextStreak;
      setStreak(nextStreak);
      missAt.current = grade.allPassed ? null : Date.now();
      if (!grade.allPassed) setMissedThisVisit(true);
      const crashText = result.traceback || result.stderr || "";
      const explanation = grade.crashed ? explainCourseError(crashText, source) : null;
      const revealPass = grade.allPassed && savedBefore?.solutionShown === true && isSolutionCode(source, exercise.solution);
      setView((previous) => ({
        stdout: result.ok ? result.stdout + (result.stderr ?? "") : result.stdout,
        grade,
        bonus: bonusGrade,
        explanation,
        stage: result.stageEvents ?? [],
        allPassed: grade.allPassed,
        wasDone,
        runNumber: (previous?.runNumber ?? 0) + 1,
        sameError:
          explanation !== null &&
          previous?.explanation != null &&
          previous.explanation.raw === explanation.raw &&
          previous.explanation.title === explanation.title,
        revealPass,
      }));
      if (grade.allPassed) {
        setJustFinished(true);
        onDone?.();
      }
      if (result.timedOut) {
        // The worker was stopped and restarts; Run comes back once Python is ready again.
        setPython("loading");
        whenPythonReady().then(
          () => setPython("ready"),
          () => setPython("failed"),
        );
      }
    } catch {
      setPython("failed");
      setView((previous) => ({
        stdout: "",
        grade: null,
        bonus: null,
        explanation: null,
        failure: "Python could not run your code. Check the internet, then press Run again.",
        stage: [],
        allPassed: false,
        wasDone: false,
        runNumber: (previous?.runNumber ?? 0) + 1,
      }));
    } finally {
      setRunning(false);
    }
  }

  function onEditorKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      event.stopPropagation();
      void run();
    }
  }

  /** Put the keyboard back on Run (or, while Python loads, on the button that opened a panel). */
  function focusRun(fallback?: string) {
    const run = runButton.current;
    if (run && !run.disabled) {
      run.focus();
      return;
    }
    const other = fallback ? toolbarRef.current?.querySelector<HTMLElement>(`[data-testid="${fallback}"]`) : null;
    (other ?? toolbarRef.current?.querySelector<HTMLElement>('[data-testid="reset-code"]'))?.focus();
  }

  function onConfirmKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      event.preventDefault();
      const opener = confirm === "solution" ? "show-solution" : "reset-code";
      setConfirm(null);
      focusRun(opener);
    }
  }

  function doReset() {
    replaceCode(exercise.starter);
    setStdinText(stdinBoxText(exercise.stdin));
    setConfirm(null);
    setResumed(false);
    setSolutionNote(false);
    focusRun();
  }

  function doShowSolution() {
    replaceCode(exercise.solution);
    updateExercise(key, (previous) => ({ ...previous, solutionShown: true }));
    setConfirm(null);
    setSolutionNote(true);
    setResumed(false);
    focusRun();
  }

  function openAssemble() {
    setAssembled([]);
    setAssembling(true);
  }

  /** After a revealed answer passes: start again from the starter and write it yourself. */
  function writeItMyself() {
    doReset();
    setJustFinished(false);
    setView(null);
  }

  function insertAssembled() {
    replaceCode(assembledCode(assembled));
    setAssembling(false);
    setAssembled([]);
    focusRun();
  }

  const runLabel = running ? "Running…" : "Run";
  const pythonText = python === "ready" ? PYTHON_STATUS_TEXT.ready : python === "failed" ? PYTHON_STATUS_TEXT.failed : PYTHON_STATUS_TEXT.loading;

  /* ------------------------------------------------------------------------------------------ */

  const learnMartu = <MarTu text={exercise.martu} glossary={glossary} />;

  const checkpointList = (
    <section className="ex-checkpoints" aria-labelledby={`${inputId}-steps`}>
      <h3 id={`${inputId}-steps`} className="ex-section-title">
        {checkpointHeading(mode, exercise.starterPasses)}
      </h3>
      <ol className="ex-checkpoint-list" data-testid="checkpoints">
        {exercise.checkpoints.map((checkpoint, index) => {
          const n = index + 1;
          const state: CheckpointState = passed.includes(checkpoint.id) ? "passed" : index === firstOpen ? "active" : "pending";
          const shown = rungsShown(saved?.hintsUsed, checkpoint.id, checkpoint.hints.length);
          return (
            <li
              key={checkpoint.id}
              className={`ex-checkpoint is-${state}`}
              data-testid={`checkpoint-${n}`}
              data-state={state}
            >
              <div className="ex-checkpoint-head">
                <span className="ex-checkpoint-mark" aria-hidden="true">
                  {STATE_MARK[state].icon}
                </span>
                <span className="ex-checkpoint-number">
                  {noun} {n}
                  <span className="ex-sr-only">: {STATE_MARK[state].words}.</span>
                </span>
              </div>
              <Prose text={checkpoint.text} glossary={glossary} className="ex-checkpoint-text" />
              <ReadAloud text={checkpoint.text} label={`Read ${noun.toLowerCase()} ${n} aloud`} testId={`read-aloud-step-${n}`} />
              <HintLadder
                hints={checkpoint.hints}
                shown={shown}
                open={hintsAreOpen && state !== "passed"}
                lockedNote={
                  support === "light" && state !== "passed" && index === firstOpen ? "Hints open after you press Run once." : null
                }
                glossary={glossary}
                onReveal={() => revealHint(checkpoint.id, checkpoint.hints.length)}
                testPrefix={String(n)}
                label={`${noun.toLowerCase()} ${n}`}
              />
            </li>
          );
        })}
      </ol>
    </section>
  );

  return (
    <div ref={rootRef} className={`ex-player${done ? " is-done" : ""}`} data-testid="exercise-player" data-mode={mode} data-done={done}>
      <div className="ex-grid">
        <section className="ex-learn" aria-label="Learn" data-testid="learn-pane">
          {mode === "lesson" || mode === "testout" || mode === "try-it" ? (
            <h2 className="ex-title" data-testid="exercise-title">
              {exercise.title}
            </h2>
          ) : null}
          {activeCheckpoint && !done ? (
            // The task first, so a student who skims sees it before Mar'tu's words and the example.
            <p className="ex-task-line" data-testid="task-line">
              <span className="ex-task-label">
                Your task ({noun.toLowerCase()} {firstOpen + 1} of {exercise.checkpoints.length}):
              </span>{" "}
              <Prose text={activeCheckpoint.text} glossary={glossary} inline />
            </p>
          ) : null}
          {light ? (
            <details className="ex-light-explain" data-testid="show-explanation">
              <summary>Show explanation</summary>
              {learnMartu}
            </details>
          ) : (
            learnMartu
          )}
          {exercise.example ? <WorkedExample example={exercise.example} /> : null}
          {anotherWayOpen(support, exercise.anotherWay) ? <AnotherWay exercise={exercise} glossary={glossary} /> : null}
          {exercise.solo ? (
            <p className="ex-solo" data-testid="solo">
              <span className="ex-solo-tag">Solo</span> This one is yours alone. No partner, no hints from a friend.
            </p>
          ) : null}
          {mode === "testout" ? null : <StepExtras exercise={exercise} glossary={glossary} />}
          {checkpointList}
          {exercise.campaignLink && mode !== "testout" ? <CampaignLink link={exercise.campaignLink} glossary={glossary} /> : null}
        </section>

        <section className="ex-work" aria-label="Your code" data-testid="work-pane">
          {exercise.predict && mode !== "testout" ? (
            <PredictCard predict={exercise.predict} starter={exercise.starter} glossary={glossary} />
          ) : null}
          <div className="toolbar ex-toolbar" ref={toolbarRef}>
            <button
              ref={runButton}
              type="button"
              className="ex-run"
              data-testid="run"
              data-running={running ? "true" : "false"}
              onClick={() => void run()}
              // Only before Python first loads is Run truly disabled. While it runs (or Python restarts
              // after a timeout) it stays focusable, so the keyboard and screen readers keep their place.
              disabled={!everReady && python === "loading"}
              aria-disabled={running || python === "loading" ? true : undefined}
            >
              <span aria-hidden="true">▶</span> {runLabel}
            </button>
            <span className="python-status" data-testid="python-status" role="status">
              {pythonText}
            </span>
            <span className="ex-toolbar-end">
              {canAssemble && !assembling ? (
                <button type="button" className="ex-quiet" data-testid="assemble-open" onClick={openAssemble}>
                  Assemble it
                </button>
              ) : null}
              {canShowSolution ? (
                <button
                  type="button"
                  className="ex-quiet"
                  data-testid="show-solution"
                  onClick={() => setConfirm("solution")}
                  aria-expanded={confirm === "solution"}
                >
                  Show solution
                </button>
              ) : null}
              <button
                type="button"
                className="ex-quiet"
                data-testid="reset-code"
                onClick={() => setConfirm("reset")}
                aria-expanded={confirm === "reset"}
              >
                Reset code
              </button>
            </span>
          </div>

          {confirm === "reset" ? (
            <div className="reset-confirm ex-confirm" data-testid="reset-confirm" ref={confirmRef} role="group" aria-label="Reset code?" onKeyDown={onConfirmKeyDown}>
              <p>Start this exercise&apos;s code over? Your steps stay done.</p>
              <button type="button" data-testid="reset-yes" onClick={doReset}>
                Yes, reset
              </button>
              <button type="button" className="reset-cancel" data-testid="reset-cancel" onClick={() => setConfirm(null)}>
                Keep my code
              </button>
            </div>
          ) : null}

          {confirm === "solution" ? (
            <div className="reset-confirm ex-confirm" data-testid="solution-confirm" ref={confirmRef} role="group" aria-label="Show solution?" onKeyDown={onConfirmKeyDown}>
              <p>Put Mar&apos;tu&apos;s answer in the editor? It replaces your code. That is okay: read it, then run it.</p>
              <button type="button" data-testid="solution-yes" onClick={doShowSolution}>
                Show it
              </button>
              <button type="button" className="reset-cancel" data-testid="solution-cancel" onClick={() => setConfirm(null)}>
                Not yet
              </button>
            </div>
          ) : null}

          {solutionNote ? (
            <p className="ex-note" data-testid="solution-note" role="status">
              This is Mar&apos;tu&apos;s answer. Read each line, then press Run to see it work.
            </p>
          ) : null}

          {resumed ? (
            <p className="ex-note" data-testid="resumed">
              Welcome back. Your code was saved, so you can pick up where you left off.
            </p>
          ) : null}

          {assembling && exercise.assemble ? (
            <section className="ex-assemble" data-testid="assemble-board" aria-label="Assemble it">
              <h3 className="ex-section-title" ref={assembleHeading} tabIndex={-1} data-testid="assemble-heading">
                Assemble it
              </h3>
              <p className="ex-muted">Build the program from pieces. Then press &ldquo;Put it in the editor&rdquo; and Run it.</p>
              <ParsonsBoard blocks={pieces} value={assembled} onChange={setAssembled} idPrefix="assemble" />
              <div className="ex-assemble-actions">
                <button type="button" data-testid="assemble-insert" onClick={insertAssembled} disabled={assembled.length === 0}>
                  Put it in the editor
                </button>
                <button
                  type="button"
                  className="ex-quiet"
                  data-testid="assemble-cancel"
                  onClick={() => {
                    setAssembling(false);
                    focusRun();
                  }}
                >
                  Cancel
                </button>
              </div>
            </section>
          ) : null}

          <div className="ex-editor" onKeyDownCapture={onEditorKeyDown}>
            <PythonEditor
              code={code}
              onChange={changeCode}
              onBlur={() => saveCodeNow.current()}
              describedBy={`${inputId}-editor-keys`}
              wrapLines
            />
          </div>
          <p className="ex-editor-foot ex-muted">
            <span data-testid="autosave-status">
              {saving ? "Your code saves in this browser." : "This browser is not saving. Copy your code before you close the page."}
            </span>{" "}
            <span className="ex-shortcut">Tip: Ctrl+Enter runs your code.</span>
            <span className="ex-editor-keys" id={`${inputId}-editor-keys`} data-testid="editor-keys">
              In the editor, Tab adds spaces. To leave the editor, press Esc, then Tab.
            </span>
          </p>

          {showInputBox ? (
            <div className="ex-stdin">
              <label htmlFor={`${inputId}-stdin`}>Input for your program</label>
              <p className="ex-muted" id={`${inputId}-stdin-help`}>
                One answer per line. Each <code className="inline-code">input()</code> takes the next answer.
              </p>
              <textarea
                id={`${inputId}-stdin`}
                data-testid="stdin-box"
                rows={Math.min(5, Math.max(2, stdinAnswers.length + 1))}
                value={stdinText}
                spellCheck={false}
                autoCapitalize="off"
                aria-describedby={`${inputId}-stdin-help`}
                onChange={(event) => setStdinText(event.target.value)}
              />
              {answersChanged ? (
                <p className="ex-stdin-note" data-testid="stdin-note">
                  The steps are checked with Mar&apos;tu&apos;s answers ({exercise.stdin?.join(", ") || "none"}). Put them back to pass.{" "}
                  <button type="button" className="ex-quiet" data-testid="stdin-reset" onClick={() => setStdinText(stdinBoxText(exercise.stdin))}>
                    Use Mar&apos;tu&apos;s answers
                  </button>
                </p>
              ) : null}
            </div>
          ) : null}

          <ExerciseConsole view={view} exercise={exercise} noun={noun} bonus={bonus} done={done} />

          {nudging && stuck ? (
            <div className="ex-nudge" data-testid="hint-nudge" role="status">
              {nudgeHint && nudgeHint.checkpointId === stuck.id ? (
                <>
                  <p className="ex-nudge-title">
                    Hint {nudgeHint.rung} of {stuck.hints.length} for {noun.toLowerCase()} {stuckIndex + 1}:
                  </p>
                  <Prose text={stuck.hints[nudgeHint.rung - 1]} glossary={glossary} />
                  <button
                    type="button"
                    className="ex-quiet"
                    data-testid="hint-nudge-no"
                    ref={nudgeThanks}
                    onClick={() => {
                      setNudgeDismissed(true);
                      focusRun();
                    }}
                  >
                    Thanks
                  </button>
                </>
              ) : (
                <>
                  <p className="ex-nudge-title">
                    Want a hint for {noun.toLowerCase()} {stuckIndex + 1}? Hints never cost you anything.
                  </p>
                  <button
                    type="button"
                    data-testid="hint-nudge-yes"
                    onClick={() => {
                      revealHint(stuck.id, stuck.hints.length);
                      setNudgeHint({ checkpointId: stuck.id, rung: Math.min(stuck.hints.length, stuckShown + 1) });
                      // This button is replaced by the hint: keep the keyboard in the nudge.
                      window.setTimeout(() => nudgeThanks.current?.focus(), 0);
                    }}
                  >
                    Yes, show a hint
                  </button>
                  <button
                    type="button"
                    className="ex-quiet"
                    data-testid="hint-nudge-no"
                    onClick={() => {
                      setNudgeDismissed(true);
                      focusRun();
                    }}
                  >
                    No thanks
                  </button>
                </>
              )}
            </div>
          ) : null}

          {done ? (
            <div className={`ex-done${justFinished ? " is-fresh" : ""}`} data-testid="exercise-done" data-reveal={view?.revealPass ? "true" : undefined}>
              <MarTu
                text={
                  justFinished && view?.revealPass
                    ? "That was my answer, so it works, yes? Now make it yours: press Write it myself and type it again without looking."
                    : justFinished && exercise.solo
                      ? "You did that alone. I saw."
                      : justFinished
                        ? "Good. Very good, yes?"
                        : "You finished this one. Run it again any time, yes?"
                }
                size="small"
                testId="exercise-done-martu"
              >
                {justFinished && view?.revealPass ? (
                  <button type="button" className="ex-next" data-testid="write-it-myself" onClick={writeItMyself}>
                    Write it myself
                  </button>
                ) : null}
                {next ? (
                  next.href ? (
                    <Link className="course-button ex-next" href={next.href} data-testid="celebrate-next">
                      {next.label} <span aria-hidden="true">→</span>
                    </Link>
                  ) : (
                    <button type="button" className="ex-next" data-testid="celebrate-next" onClick={next.onClick}>
                      {next.label} <span aria-hidden="true">→</span>
                    </button>
                  )
                ) : null}
              </MarTu>
              {exercise.takeaway ? (
                <p className="ex-takeaway" data-testid="takeaway">
                  <span className="ex-takeaway-label">Remember:</span> <Prose text={exercise.takeaway} glossary={glossary} inline />
                </p>
              ) : null}
            </div>
          ) : null}

          {done && bonus ? (
            <SideQuest
              bonus={bonus}
              doneBefore={saved?.bonusDone === true}
              shown={rungsShown(saved?.hintsUsed, BONUS_ID, bonus.hints.length)}
              glossary={glossary}
              support={support}
              onReveal={() => revealHint(BONUS_ID, bonus.hints.length)}
            />
          ) : null}
        </section>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------------------------------------- */
/* Console and side quest                                                                          */
/* ---------------------------------------------------------------------------------------------- */

function ExerciseConsole({
  view,
  exercise,
  noun,
  bonus,
  done,
}: {
  view: RunView | null;
  exercise: Playable;
  noun: string;
  bonus: Bonus | undefined;
  done: boolean;
}) {
  const grade = view?.grade ?? null;
  const stage = view ? stageLines(view.stage) : [];
  return (
    <section className="console ex-console" data-testid="console" aria-label="Console">
      <h3>Console</h3>
      {view === null ? (
        <pre className="program-output ex-placeholder" data-testid="stdout">
          Press Run to see what your code prints.
        </pre>
      ) : view.failure ? null : (
        <pre className="program-output" data-testid="stdout">
          {view.stdout.length > 0 ? shownOutput(view.stdout) : "(Nothing was printed.)"}
        </pre>
      )}
      {stage.length > 0 ? (
        <div className="ex-stage" data-testid="game-screen">
          <p className="ex-stage-label">On the game screen:</p>
          <pre>{stage.join("\n")}</pre>
        </div>
      ) : null}
      <div className="ex-results" role="status" aria-live="polite" data-testid="checkpoint-results">
        {view?.failure ? (
          <p className="ex-result is-error" data-testid="run-failure">
            {view.failure}
          </p>
        ) : null}
        {view?.explanation ? (
          <div className="explainer ex-explainer" data-testid="explainer" key={view.runNumber}>
            {view.sameError ? (
              <p className="ex-same-error" data-testid="same-error">
                Same error as last time.{" "}
                {crashLine(view.explanation.raw) ? `Look closely at line ${crashLine(view.explanation.raw)}.` : "Look closely at the line it names."}
              </p>
            ) : null}
            <p className="ex-explainer-title">{view.explanation.title}</p>
            <Prose text={view.explanation.hint} className="ex-explainer-hint" testId="explainer-hint" />
            {view.explanation.raw ? (
              <details>
                <summary>Show Python&apos;s full message</summary>
                <pre data-testid="traceback">{view.explanation.raw}</pre>
              </details>
            ) : null}
          </div>
        ) : null}
        {grade && !grade.crashed ? (
          <ul className="ex-result-list" key={view?.runNumber}>
            {grade.checkpoints.map((result, index) => {
              const checkpoint = exercise.checkpoints[index];
              if (result.passed) {
                return (
                  <li key={result.id} className="ex-result is-pass" data-testid={`checkpoint-pass-${index + 1}`}>
                    <span aria-hidden="true">✓</span>{" "}
                    <strong>
                      {noun} {index + 1} done!
                    </strong>
                    {checkpoint?.passLine ? <span className="ex-pass-line"> {checkpoint.passLine}</span> : null}
                  </li>
                );
              }
              if (index !== grade.firstFailing) return null;
              return (
                <li key={result.id} className="ex-result is-miss" data-testid="checkpoint-message">
                  <span aria-hidden="true">→</span>{" "}
                  <strong>
                    {noun} {index + 1}, not yet:
                  </strong>{" "}
                  <Prose text={result.message} inline testId={`checkpoint-message-${index + 1}`} />
                </li>
              );
            })}
          </ul>
        ) : null}
        {grade?.allPassed ? (
          <p className="ex-result is-all" data-testid="all-passed">
            <span aria-hidden="true">★</span> Every {noun.toLowerCase()} is done!
          </p>
        ) : null}
        {done && bonus && view?.bonus ? (
          view.bonus.allPassed ? (
            <p className="ex-result is-pass" data-testid="side-quest-pass">
              <span aria-hidden="true">✓</span> <strong>Side quest done!</strong> {CAMEO_NAMES[bonus.by]} is impressed.
            </p>
          ) : view.wasDone && view.bonus.firstFailing !== null ? (
            <p className="ex-result is-side" data-testid="side-quest-message">
              <span aria-hidden="true">→</span> <strong>Side quest, not yet:</strong>{" "}
              <Prose text={view.bonus.checkpoints[view.bonus.firstFailing]?.message ?? ""} inline />
            </p>
          ) : null
        ) : null}
      </div>
    </section>
  );
}

function SideQuest({
  bonus,
  doneBefore,
  shown,
  glossary,
  support,
  onReveal,
}: {
  bonus: Bonus;
  doneBefore: boolean;
  shown: number;
  glossary: GlossaryEntry[];
  support: Support;
  onReveal: () => void;
}) {
  const who = CAMEO_NAMES[bonus.by];
  return (
    <section className={`ex-side-quest${doneBefore ? " is-done" : ""}`} data-testid="side-quest" aria-label={`Side quest from ${who}`}>
      <img className="ex-cameo" src={publicPath(`/sprites/${bonus.by}.svg`)} alt="" aria-hidden="true" />
      <div className="ex-side-body">
        <p className="ex-side-title">
          <span className="ex-side-tag">Side quest (optional)</span> {bonus.title}
        </p>
        <p className="ex-muted">From {who}. It runs on the same code, so keep your steps working.</p>
        <Prose text={bonus.text} glossary={glossary} />
        <p className="ex-side-status" data-testid="side-quest-status">
          {doneBefore ? (
            <>
              <span aria-hidden="true">✓</span> Done! {who} owes you one.
            </>
          ) : (
            <>
              <span aria-hidden="true">○</span> Not done yet. Add it to your code and press Run.
            </>
          )}
        </p>
        <HintLadder
          hints={bonus.hints}
          shown={shown}
          open={support !== "none" && !doneBefore}
          lockedNote={null}
          glossary={glossary}
          onReveal={onReveal}
          testPrefix="bonus"
          label="the side quest"
        />
      </div>
    </section>
  );
}
