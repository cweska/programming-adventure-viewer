/**
 * Pure logic for the Intro to Python exercise player (ExercisePlayer.tsx / LessonPlayer.tsx).
 * Client-safe, no React, no Python: everything here is unit tested in exercise-logic.test.ts.
 */
import type { ExerciseProgress, GradeResult } from "../../lib/course/contracts";
import type { AnotherWay, Checkpoint } from "../../lib/course/schema";

export type Support = "full" | "light" | "none";
export type PlayerMode = "lesson" | "project" | "challenge" | "testout" | "try-it";

/* ------------------------------------------------------------------------------------------------ */
/* Stepper: the current exercise lives in the URL hash (#<exerciseId>)                              */
/* ------------------------------------------------------------------------------------------------ */

/** The exercise index a URL hash points to ("#ask-the-traveler"). Unknown or empty hashes give 0. */
export function exerciseIndexFromHash(hash: string, ids: readonly string[]): number {
  let wanted = (hash ?? "").trim().replace(/^#/, "").trim();
  try {
    wanted = decodeURIComponent(wanted);
  } catch {
    // A malformed escape: use the text as it is.
  }
  const at = ids.indexOf(wanted);
  return at >= 0 ? at : 0;
}

/** The hash for an exercise id. */
export function hashForExercise(id: string): string {
  return `#${encodeURIComponent(id)}`;
}

/* ------------------------------------------------------------------------------------------------ */
/* Support levels                                                                                    */
/* ------------------------------------------------------------------------------------------------ */

/** Quick Checks never give help, whatever the content says. */
export function effectiveSupport(mode: PlayerMode, support: Support | undefined): Support {
  if (mode === "testout") return "none";
  return support ?? "full";
}

/**
 * Whether the hint ladder is open. full: always. light: after the student's first run that did not
 * finish (this visit or saved). none: never.
 */
export function hintsOpen(support: Support, triedAndMissed: boolean): boolean {
  if (support === "full") return true;
  if (support === "light") return triedAndMissed;
  return false;
}

/** "Explain it another way" is a full-support extra. */
export function anotherWayOpen(support: Support, angles: readonly AnotherWay[]): boolean {
  return support === "full" && angles.length > 0;
}

/* ------------------------------------------------------------------------------------------------ */
/* Solution gating                                                                                   */
/* ------------------------------------------------------------------------------------------------ */

export type SolutionGate = {
  support: Support;
  activeMs: number;
  failedRuns: number;
  solutionAfterMinutes: number;
  solutionAfterFailedRuns: number;
};

/** "Show solution" appears after N minutes of active time OR N failed runs (full and light support only). */
export function solutionUnlocked(gate: SolutionGate): boolean {
  if (gate.support === "none") return false;
  const minutes = Math.max(0, gate.solutionAfterMinutes);
  const runs = Math.max(0, gate.solutionAfterFailedRuns);
  return gate.activeMs >= minutes * 60_000 || gate.failedRuns >= runs;
}

/* ------------------------------------------------------------------------------------------------ */
/* Hint ladder                                                                                       */
/* ------------------------------------------------------------------------------------------------ */

/** How many rungs are open, clamped to the ladder. */
export function rungsShown(hintsUsed: Record<string, number> | undefined, checkpointId: string, total: number): number {
  const used = hintsUsed?.[checkpointId] ?? 0;
  return Math.max(0, Math.min(total, Math.floor(used)));
}

/** Open one more rung (never past the top). Returns a new hintsUsed record. */
export function revealNextRung(
  hintsUsed: Record<string, number> | undefined,
  checkpointId: string,
  total: number,
): Record<string, number> {
  const shown = rungsShown(hintsUsed, checkpointId, total);
  return { ...(hintsUsed ?? {}), [checkpointId]: Math.min(total, shown + 1) };
}

/** The hint button's words: "Hint (1 of 3)" before opening, "Another hint (2 of 3)" after, then done. */
export function hintButtonLabel(shown: number, total: number): string {
  if (total <= 0) return "No hints";
  if (shown >= total) return `All ${total} hints shown`;
  return shown === 0 ? `Hint (1 of ${total})` : `Next hint (${shown + 1} of ${total})`;
}

/* ------------------------------------------------------------------------------------------------ */
/* Runs and progress                                                                                 */
/* ------------------------------------------------------------------------------------------------ */

/** The checkpoint a run got stuck on: the first failing one (on a crash, the first not passed yet). */
export function stuckCheckpointId(
  checkpoints: readonly Checkpoint[],
  grade: GradeResult,
  passedBefore: readonly string[],
): string | null {
  if (grade.allPassed) return null;
  if (grade.crashed) {
    const first = checkpoints.find((checkpoint) => !passedBefore.includes(checkpoint.id));
    return (first ?? checkpoints[0])?.id ?? null;
  }
  if (grade.firstFailing === null) return null;
  return checkpoints[grade.firstFailing]?.id ?? null;
}

export type RunOutcome = {
  /** Checkpoint ids that passed in this run. */
  passedNow: string[];
  /** Ids that passed for the first time in this run. */
  newlyPassed: string[];
  /** Every checkpoint passed in this run. */
  allPassed: boolean;
  /**
   * A run that did not finish and did not pass any new checkpoint (a crash counts). Running after each
   * step of a long task is progress, not failure, so it never counts toward "Show solution".
   */
  failed: boolean;
};

export function runOutcome(grade: GradeResult, passedBefore: readonly string[]): RunOutcome {
  const passedNow = grade.checkpoints.filter((checkpoint) => checkpoint.passed).map((checkpoint) => checkpoint.id);
  const newlyPassed = passedNow.filter((id) => !passedBefore.includes(id));
  const allPassed = grade.allPassed;
  return { passedNow, newlyPassed, allPassed, failed: !allPassed && newlyPassed.length === 0 };
}

/** Fold one graded run into the saved progress (passed ids are a union across runs). */
export function applyRun(
  previous: ExerciseProgress,
  outcome: RunOutcome,
  extra: { code?: string; bonusPassed?: boolean } = {},
): ExerciseProgress {
  const passed = [...previous.passed];
  for (const id of outcome.passedNow) if (!passed.includes(id)) passed.push(id);
  const next: ExerciseProgress = {
    ...previous,
    passed,
    done: previous.done || outcome.allPassed,
    failedRuns: previous.failedRuns + (outcome.failed ? 1 : 0),
  };
  if (extra.code !== undefined) next.code = extra.code;
  // The side quest counts once the exercise itself is done (now or earlier).
  if (extra.bonusPassed && next.done) next.bonusDone = true;
  return next;
}

/** Consecutive misses on one checkpoint, for the "Want a hint?" nudge. */
export type FailStreak = { checkpointId: string | null; count: number };

export function nextFailStreak(previous: FailStreak, stuckOn: string | null): FailStreak {
  if (!stuckOn) return { checkpointId: null, count: 0 };
  if (previous.checkpointId === stuckOn) return { checkpointId: stuckOn, count: previous.count + 1 };
  return { checkpointId: stuckOn, count: 1 };
}

/** Wait this long without typing after a miss before offering a hint. */
export const NUDGE_IDLE_MS = 90_000;
/** Offer a hint after this many misses in a row on one checkpoint. */
export const NUDGE_AFTER_MISSES = 2;

/** The gentle "Want a hint?" offer: full support only, and only when a hint is left to give. */
export function shouldNudge(input: {
  support: Support;
  streak: FailStreak;
  /** ms since the last keystroke, counted from the last miss (null when the last run did not miss). */
  idleSinceMissMs: number | null;
  hintsLeft: number;
  dismissed: boolean;
}): boolean {
  if (input.support !== "full" || input.dismissed || input.hintsLeft <= 0) return false;
  if (!input.streak.checkpointId) return false;
  if (input.streak.count >= NUDGE_AFTER_MISSES) return true;
  return input.idleSinceMissMs !== null && input.idleSinceMissMs >= NUDGE_IDLE_MS;
}

/* ------------------------------------------------------------------------------------------------ */
/* Code helpers                                                                                      */
/* ------------------------------------------------------------------------------------------------ */

/** The code with comments and blank lines removed, lines trimmed at the end (rough but string-aware). */
function meaningfulLines(code: string): string[] {
  return (code ?? "")
    .replace(/\r/g, "")
    .split("\n")
    .map((line) => stripComment(line).trimEnd())
    .filter((line) => line.trim().length > 0);
}

/** Drop a trailing `# comment`, leaving any `#` inside quotes alone. */
export function stripComment(line: string): string {
  let quote: string | null = null;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (quote) {
      if (char === "\\") index += 1;
      else if (char === quote) quote = null;
    } else if (char === '"' || char === "'") {
      quote = char;
    } else if (char === "#") {
      return line.slice(0, index);
    }
  }
  return line;
}

/** True when the code calls input() somewhere outside a comment. */
export function usesInput(code: string): boolean {
  return meaningfulLines(code).some((line) => /(^|[^\w.])input\s*\(/.test(line));
}

function normalize(code: string): string {
  return (code ?? "").replace(/\r/g, "").trim();
}

/** The editor holds nothing of the student's yet: blank, only comments, or the untouched starter. */
export function isBlankOrStarter(code: string, starter: string): boolean {
  if (meaningfulLines(code).length === 0) return true;
  return normalize(code) === normalize(starter);
}

/**
 * The editor text after "Assemble it": exactly the assembled lines. Mar'tu's starter comments are not kept,
 * because checks that read `_source` (for example "type the name once") would count words in them.
 */
export function assembledCode(lines: readonly string[]): string {
  return lines.length > 0 ? `${lines.join("\n")}\n` : "";
}

/** The "Input for your program" box: one answer per line; trailing empty lines are ignored. */
export function parseStdinBox(text: string): string[] {
  const lines = (text ?? "").replace(/\r/g, "").split("\n");
  while (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines;
}

export function stdinBoxText(answers: readonly string[] | undefined): string {
  return (answers ?? []).join("\n");
}

/* ------------------------------------------------------------------------------------------------ */
/* Words on the screen                                                                               */
/* ------------------------------------------------------------------------------------------------ */

const ANGLE_LABELS: Record<string, string> = {
  analogy: "Compare it to something",
  "step by step": "Step by step",
  "step-by-step": "Step by step",
  steps: "Step by step",
  visual: "Picture it",
  picture: "Picture it",
  story: "Tell it as a story",
  example: "Show another example",
  "another example": "Show another example",
  "plain words": "In plain words",
  plain: "In plain words",
  mistake: "A common mistake",
  "common mistake": "A common mistake",
  campaign: "Where the campaign uses it",
};

/** What the "Explain it another way" button says for an angle. */
export function angleLabel(way: Pick<AnotherWay, "angle" | "label">): string {
  if (way.label && way.label.trim()) return way.label.trim();
  const angle = way.angle.trim();
  const known = ANGLE_LABELS[angle.toLowerCase()];
  if (known) return known;
  return angle ? angle.charAt(0).toUpperCase() + angle.slice(1) : "Another way";
}

/** "leylines-awaken" -> "Leylines Awaken" (campaign link boxes only know ids). */
export function titleFromId(id: string): string {
  return id
    .split(/[-_]/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

/** What a checkpoint is called in this kind of item. */
export function stepNoun(mode: PlayerMode): "Step" | "Task" {
  return mode === "project" || mode === "challenge" ? "Task" : "Step";
}

/** The checkpoint list's heading. */
export function checkpointHeading(mode: PlayerMode, starterPasses: boolean): string {
  if (starterPasses) return "Run it and read the output";
  return mode === "project" || mode === "challenge" ? "Your tasks" : "Your steps";
}
