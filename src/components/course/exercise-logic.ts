/**
 * Pure logic for the Intro to Python exercise player (ExercisePlayer.tsx / LessonPlayer.tsx).
 * Client-safe, no React, no Python: everything here is unit tested in exercise-logic.test.ts.
 */
import type { ExerciseProgress, GradeResult } from "../../lib/course/contracts";
import type { AnotherWay, Checkpoint } from "../../lib/course/schema";
import type { InsertTarget } from "../editor-insert";

export type Support = "full" | "light" | "none";
export type PlayerMode = "lesson" | "project" | "challenge" | "testout" | "try-it";
/** curriculum §2.3: "Show me more" (the default) or "Keep it short". Read it with coursePreset() (progress.ts). */
export type Preset = "more" | "short";

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
 * Whether Help is available. full: always. light: after the student's first run that did not finish
 * (this visit or saved). none (Quick Checks): never.
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
  /** Counted failed runs only (see countsAsAttempt). */
  failedRuns: number;
  solutionAfterMinutes: number;
  solutionAfterFailedRuns: number;
};

/**
 * "Compare with Mar'tu's version" opens after N minutes of visible time on the exercise, OR N counted
 * failed runs (full and light support only; never in a Quick Check).
 */
export function solutionUnlocked(gate: SolutionGate): boolean {
  if (gate.support === "none") return false;
  const minutes = Math.max(0, gate.solutionAfterMinutes);
  const runs = Math.max(0, gate.solutionAfterFailedRuns);
  return gate.activeMs >= minutes * 60_000 || gate.failedRuns >= runs;
}

/**
 * Whether a missed run counts toward Mar'tu's version: only when the code CHANGED since the last run (the
 * starter counts as the "last run" before the first one), or a Help rung was opened since then. Pressing
 * Run four times on untouched starter code is not four tries; a blank editor is never a try.
 */
export function countsAsAttempt(
  source: string,
  starter: string,
  lastRunSource: string | null,
  usedHelpSinceLastRun = false,
): boolean {
  if (meaningfulLines(source).length === 0) return false;
  if (usedHelpSinceLastRun) return true;
  return normalize(source) !== normalize(lastRunSource ?? starter);
}

/** The code is Mar'tu's answer as it was put in the editor (maybe with spacing changes). */
export function isSolutionCode(code: string, solution: string): boolean {
  const squash = (text: string) => meaningfulLines(text).map((line) => line.trim()).join("\n");
  return squash(code) === squash(solution);
}

/* ------------------------------------------------------------------------------------------------ */
/* Hint ladder                                                                                       */
/* ------------------------------------------------------------------------------------------------ */

/** How many rungs are open, clamped to the ladder. */
export function rungsShown(hintsUsed: Record<string, number> | undefined, checkpointId: string, total: number): number {
  const used = hintsUsed?.[checkpointId] ?? 0;
  return Math.max(0, Math.min(total, Math.floor(used)));
}

/**
 * Open one more rung (never past the top), or, given `upTo`, every rung up to and including that many (Help
 * steps over rungs it skips, see helpState). Never closes rungs. Returns a new hintsUsed record.
 */
export function revealNextRung(
  hintsUsed: Record<string, number> | undefined,
  checkpointId: string,
  total: number,
  upTo?: number,
): Record<string, number> {
  const shown = rungsShown(hintsUsed, checkpointId, total);
  const next = upTo === undefined ? shown + 1 : Math.max(shown, Math.floor(upTo));
  return { ...(hintsUsed ?? {}), [checkpointId]: Math.min(total, next) };
}

/**
 * A SOLO pass counts as "alone" (curriculum §2.1 step 7) when no Help went past Where to look for any step
 * (the first rung of a SOLO exercise), and Mar'tu's version was never opened.
 */
export function soloUnaided(saved: Pick<ExerciseProgress, "hintsUsed" | "solutionShown"> | undefined): boolean {
  if (!saved) return true;
  if (saved.solutionShown) return false;
  return Object.entries(saved.hintsUsed ?? {}).every(([id, count]) => id.startsWith("__") || count <= 1);
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

/** Offer Help after this long without typing or running (the silent stall, also before the first Run). */
export const NUDGE_IDLE_MS = 90_000;
/** Offer Help after this many failed runs in a row on one step. */
export const NUDGE_AFTER_MISSES = 3;
/** Offer Help after this much visible time on the exercise without a new step passing. */
export const NUDGE_NO_PROGRESS_MS = 4 * 60_000;

export type HelpOffer = "misses" | "time" | "idle";

/**
 * Proactive Help offers (curriculum §2.2): a highlighted Help control with one line, never a popup.
 * Only while Help is available and has something left to give; under "Keep it short" only after repeated
 * misses; and one dismiss silences offers for the exercise.
 */
export function helpOffer(input: {
  preset: Preset;
  helpAvailable: boolean;
  done: boolean;
  dismissed: boolean;
  /** Help rungs the student could still open now (a locked "Show me" does not count). */
  rungsLeft: number;
  /** Failed runs in a row on the current step. */
  missesInARow: number;
  /** Visible ms on this exercise since the last new step passed (or since opening it). */
  msSinceProgress: number;
  /**
   * Visible ms since the student last typed, ran or opened Help (or since the exercise opened): the silent
   * stall, which also counts before the first Run (curriculum §2.2, G3). Null when not measured.
   */
  idleMs: number | null;
}): HelpOffer | null {
  if (!input.helpAvailable || input.done || input.dismissed || input.rungsLeft <= 0) return null;
  if (input.missesInARow >= NUDGE_AFTER_MISSES) return "misses";
  // Under "Keep it short" only the failed-runs trigger is active (curriculum §2.3).
  if (input.preset !== "more") return null;
  if (input.msSinceProgress >= NUDGE_NO_PROGRESS_MS) return "time";
  if (input.idleMs !== null && input.idleMs >= NUDGE_IDLE_MS) return "idle";
  return null;
}

/**
 * The one line that highlights Help (Oogrish's line after repeated misses, §2.2). "Read the last line first"
 * is about Python's error message, so it is said only when the last run crashed.
 */
export function helpOfferLine(offer: HelpOffer, crashed = false): string {
  if (offer === "misses") {
    return crashed
      ? "Oogrish: \u201cSteady, now. Read the last line first. Want a nudge?\u201d"
      : "Oogrish: \u201cSteady, now. Want a nudge?\u201d";
  }
  if (offer === "time") return "This one is taking a while. That is normal. Want a nudge?";
  return "Still thinking? A nudge is one click away.";
}

/* ------------------------------------------------------------------------------------------------ */
/* The Help stack (curriculum §2.2): one climbing Help control per exercise                          */
/* ------------------------------------------------------------------------------------------------ */

export type RungKind = "start" | "point" | "another" | "teach" | "how" | "structure" | "show";

export type Rung = {
  kind: RungKind;
  /** What the Help control says before this rung opens, and the rung's title once open. */
  label: string;
  /** For point / teach / how: the checkpoint hint this rung shows. */
  hint?: number;
  /** For start: the first tokens of the step's line (e.g. `caster =` or `print(`). */
  start?: string;
};

/** Each rung waits for a Run or this long after the last one, so each one gets read. */
export const RUNG_PACE_MS = 10_000;

/**
 * "Start me off" (curriculum §2.2 rung 0): the first tokens of the step's line, up to and including its
 * first `(` or `=` (`caster =`, `print(`). Taken from the first code span of the step's last hint (the
 * "show" rung of the authored point -> teach -> show ladder). Null when there is nothing safe to give:
 * no code span, a line with no `(` or `=` (it would be the whole answer), or (given `solution`) a start that
 * Mar'tu's version does not use.
 */
export function startOfLine(hints: readonly string[] | undefined, solution?: string): string | null {
  const last = hints && hints.length >= 2 ? hints[hints.length - 1] : undefined;
  const span = last?.match(/`([^`\n]+)`/)?.[1]?.trim();
  if (!span) return null;
  // The first "(" or a lone "=" (also +=, -= ...), never ==, <=, >= or !=.
  const cut = span.match(/^(.*?)(\(|[+\-*/]?=(?!=))/);
  if (!cut || /[=!<>]$/.test(cut[1])) return null;
  const start = `${cut[1]}${cut[2]}`.trim();
  if (!start || start === "(" || start.length >= span.length) return null;
  // A hint may show an example with other names: only give a start that Mar'tu's version really uses.
  const squash = (text: string) => text.replace(/\s+/g, "");
  if (solution !== undefined && !squash(solution).includes(squash(start))) return null;
  return start;
}

/**
 * Where Start me off puts the step's line when the student has not clicked into the code yet, read from the step's
 * last hint (its own line, in Mar'tu's words): "Write `scout.step("west")` in place of `pass`" replaces that `pass`
 * (in the recipe the step names, `step_west`), "Write `return total` on the line after `total = affinity * 2`" and
 * "under the `# passed:` note" go on a new line under that one. Null when the hint names no line (the end of the
 * code, as before).
 */
export function startTarget(checkpoint: Pick<Checkpoint, "hints" | "text">): InsertTarget | null {
  const hints = checkpoint.hints ?? [];
  const last = hints.length >= 2 ? hints[hints.length - 1] : undefined;
  const place = last?.match(/\b(in place of|on the line after|under)\s+(?:the\s+)?`([^`\n]+)`/);
  if (!place) return null;
  const spans = [checkpoint.text, ...hints].flatMap((text) => [...(text ?? "").matchAll(/`([^`\n]+)`/g)].map((span) => span[1]));
  const near = [...new Set(spans.flatMap((span) => [...span.matchAll(/[A-Za-z_]\w*/g)].map((name) => name[0])))];
  return { line: place[2].trim(), how: place[1] === "in place of" ? "replace" : "after", near };
}

/**
 * The Help rungs for one step, in the curriculum's order (§2.2): Start me off (derived, see startOfLine),
 * Where to look (hints[0]), Another way (the exercise's angles), Teach me (the middle hints), More structure
 * (Assemble it), Show me how (the last hint: the step's own line), and Compare with Mar'tu's version (the
 * whole program side by side, unlocked by time or tries). Authored hints are point -> teach -> show (FORMAT.md),
 * so the nearly-the-answer hint always comes after the gentler rungs. Missing pieces are skipped. A SOLO
 * exercise starts at Where to look.
 */
export function helpRungs(
  checkpoint: Pick<Checkpoint, "hints">,
  exercise: { anotherWayCount: number; hasAssemble: boolean; solo: boolean; solution?: string },
): Rung[] {
  const hints = checkpoint.hints ?? [];
  const rungs: Rung[] = [];
  const start = exercise.solo ? null : startOfLine(hints, exercise.solution);
  if (start) rungs.push({ kind: "start", label: "Start me off", start });
  if (hints.length > 0) rungs.push({ kind: "point", label: "Where to look", hint: 0 });
  if (exercise.anotherWayCount > 0) rungs.push({ kind: "another", label: "Another way" });
  for (let index = 1; index < hints.length - 1; index += 1) {
    rungs.push({ kind: "teach", label: index === 1 ? "Teach me" : "Teach me more", hint: index });
  }
  if (exercise.hasAssemble) rungs.push({ kind: "structure", label: "More structure" });
  if (hints.length > 1) rungs.push({ kind: "how", label: "Show me how", hint: hints.length - 1 });
  rungs.push({ kind: "show", label: "Compare with Mar'tu's version" });
  return rungs;
}

/**
 * Which rungs the Help control climbs (curriculum §2.2, §2.3). "Show me more": all of them. "Keep it short":
 * Where to look, Teach me, Show me how and Mar'tu's version; Start me off, Another way and More structure wait
 * under "More options".
 */
export function rungInStack(kind: RungKind, preset: Preset = "more"): boolean {
  if (preset === "more") return true;
  return kind === "point" || kind === "teach" || kind === "how" || kind === "show";
}

export type HelpState = {
  /** The rungs open now (from hintsUsed) that the stack shows, in order. */
  open: Rung[];
  /** How many rungs of helpRungs() are open or stepped over (the saved count). */
  opened: number;
  /** The rung the Help control opens next, or null when every rung is open. */
  next: Rung | null;
  /** next's index in helpRungs() (-1 when there is none): opening it saves `nextIndex + 1`. */
  nextIndex: number;
  /** The next rung is Show me, but Mar'tu's version is not unlocked yet. */
  nextLocked: boolean;
  /** Rungs the student could still open now (a locked Show me does not count). */
  left: number;
  /** "Keep it short": the rungs under "More options" (open any time, in any order). Empty otherwise. */
  extras: Rung[];
};

/**
 * The Help control's state. The saved count always runs over the whole helpRungs() list, whatever the preset,
 * so switching presets never opens Mar'tu's version early. The control steps over rungs that are not in this
 * preset's stack, and over rungs `skip` says have nothing to give right now (Start me off when the line is
 * already there, or right after a crash).
 */
export function helpState(
  rungs: readonly Rung[],
  used: number,
  showUnlocked: boolean,
  options: { preset?: Preset; skip?: (rung: Rung) => boolean } = {},
): HelpState {
  const preset = options.preset ?? "more";
  const skip = options.skip ?? (() => false);
  const count = Math.max(0, Math.min(rungs.length, Math.floor(used)));
  const open = rungs.slice(0, count).filter((rung) => rungInStack(rung.kind, preset));
  const climbable = (rung: Rung) => rungInStack(rung.kind, preset) && !skip(rung);
  let nextIndex = -1;
  for (let index = count; index < rungs.length; index += 1) {
    if (climbable(rungs[index])) {
      nextIndex = index;
      break;
    }
  }
  const next = nextIndex >= 0 ? rungs[nextIndex] : null;
  const left = rungs.slice(count).filter((rung) => climbable(rung) && (rung.kind !== "show" || showUnlocked)).length;
  const extras = preset === "more" ? [] : rungs.filter((rung) => !rungInStack(rung.kind, preset));
  return { open, opened: count, next, nextIndex, nextLocked: next?.kind === "show" && !showUnlocked, left, extras };
}

/**
 * The code already starts the step's line (Start me off has nothing to add): a line outside notes that begins
 * with `start`, ignoring spaces (`caster =` matches `caster="Gearshift"`).
 */
export function codeHasStart(code: string, start: string): boolean {
  const squash = (text: string) => text.replace(/\s+/g, "");
  const wanted = squash(start);
  if (!wanted) return false;
  return meaningfulLines(code).some((line) => squash(line).startsWith(wanted));
}

/** The step's text names a line of the code ("Mend line 3 so ...", "Line 2 is Lucky's secret."). */
export function namesALine(text: string, line?: number): boolean {
  return new RegExp(`\\bline ${line === undefined ? "\\d+" : line}\\b`, "i").test(text ?? "");
}

/**
 * A debugging exercise (curriculum §2.1 step 6, the Broken spell; also the Quick Check "mend" tasks): one of its
 * steps says "Mend ..." ("Mend line 3 so it shows `Steady`."). There a run that gets further than the last one
 * shows "Python got further: that slip is mended." on a line of its own (FORMAT.md, checkpoint `text`).
 */
export function isDebugExercise(exercise: { checkpoints: readonly Pick<Checkpoint, "text">[] }): boolean {
  return exercise.checkpoints.some((checkpoint) => /\bmend\b/i.test(checkpoint.text ?? ""));
}

/**
 * After a crash on `crashLine`: the step whose text names that line (broken spells: "Mend line 3 ..."), or -1.
 * Help aims there, so it never talks about line 1 under "Mend line 3 first."
 */
export function crashTarget(checkpoints: readonly Pick<Checkpoint, "text">[], crashLine: number | null): number {
  if (crashLine === null) return -1;
  return checkpoints.findIndex((checkpoint) => namesALine(checkpoint.text, crashLine));
}

/**
 * The crash is part of the task: Mar'tu's version keeps the line Python stopped on, switched off with `#`
 * (Anatomy of a fizzle: read the message, write it down, then switch line 4 off). "First, mend line 4" would
 * contradict the task there, so the player says to read the message first. False for an empty line or no solution.
 */
export function crashLineSwitchedOff(code: string, crashLine: number | null, solution: string | undefined): boolean {
  if (crashLine === null || !solution) return false;
  const text = (code ?? "").split("\n")[crashLine - 1]?.trim() ?? "";
  if (!text || text.startsWith("#")) return false;
  return solution.split("\n").some((row) => /^\s*#/.test(row) && row.trim().replace(/^#\s*/, "") === text);
}

/** A crash Help has aimed at this visit: its signature (line and Python's last line) and the step it got. */
export type CrashAim = { signature: string; step: number | null };

/**
 * Where Help aims while a crash stands in a debugging exercise with several slips (a Broken spell). A crash checks
 * no step, so the first open step stays at step 1 while the student mends slip after slip; Help must move on with
 * them, or it talks about the line they just mended. Returns the step index, or null for "only say which line to
 * mend" (the steps name other lines).
 *
 * - A crash seen before this visit gets the step it had (a slip mended and then broken again).
 * - A crash that got further than the last one (`gotFurther`) aims past the last crash's step: the next step that
 *   names the crash line in its text, else (when steps name lines) none, else the next step that names it in a
 *   hint, else simply the next step.
 * - Another new crash right after one (the same slip, typed another way) keeps the last crash's step.
 * - Otherwise: the step that names the crash line, else the first open step (as before).
 *
 * When several steps name the crash line (Broken spell 2A: the sign and the text "15" are both on line 3), the one
 * whose Help names Python's error (`TypeError`, from `error`, Python's last line) wins: a student who mends `=>`
 * by way of a quiet `=` reaches the TypeError with no crash just before it, and step 1's rungs say SyntaxError.
 */
export function crashAim(input: {
  checkpoints: readonly Pick<Checkpoint, "text" | "hints">[];
  crashLine: number | null;
  signature: string;
  /** Crashes Help aimed at earlier in this visit. */
  seen: readonly CrashAim[];
  /** The last run's crash, when the last run crashed too. */
  previous: CrashAim | null;
  gotFurther: boolean;
  firstOpen: number;
  /** Python's last line (`TypeError: '>=' not supported ...`): its error's name breaks a tie between steps. */
  error?: string;
}): number | null {
  const { checkpoints, crashLine, signature, seen, previous, gotFurther, firstOpen } = input;
  const known = seen.find((aim) => aim.signature === signature);
  if (known) return known.step;
  const linesNamed = checkpoints.some((checkpoint) => namesALine(checkpoint.text));
  const indexed = checkpoints.map((checkpoint, index) => ({ checkpoint, index }));
  const errorName = input.error?.trim().match(/^([A-Z][A-Za-z]*(?:Error|Exception))\b/)?.[1];
  const namesError = ({ checkpoint }: { checkpoint: Pick<Checkpoint, "hints"> }) =>
    errorName !== undefined && (checkpoint.hints ?? []).some((hint) => new RegExp(`\\b${errorName}\\b`).test(hint));
  /** Of the steps that name the crash line, the first whose Help names this error, else simply the first. */
  const pick = (rows: typeof indexed) => {
    const naming = rows.filter(({ checkpoint }) => crashLine !== null && namesALine(checkpoint.text, crashLine));
    return (naming.find(namesError) ?? naming[0])?.index;
  };
  if (previous && previous.step !== null && crashLine !== null) {
    if (!gotFurther) return previous.step;
    const after = indexed.slice(previous.step + 1);
    const byText = pick(after);
    if (byText !== undefined) return byText;
    if (linesNamed) return null;
    const byHint = after.find(({ checkpoint }) => (checkpoint.hints ?? []).some((hint) => namesALine(hint, crashLine)));
    if (byHint) return byHint.index;
    return Math.min(previous.step + 1, checkpoints.length - 1);
  }
  const named = pick(indexed);
  if (named !== undefined) return named;
  if (linesNamed && crashLine !== null) return null;
  return firstOpen;
}

/** Whether the next rung must wait (a Run since the last rung, or RUNG_PACE_MS, lets it open). */
export function rungPaced(lastRungAt: number | null, ranSinceRung: boolean, now: number): boolean {
  if (lastRungAt === null || ranSinceRung) return false;
  return now - lastRungAt < RUNG_PACE_MS;
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

/**
 * The "Input for your program" box: one answer per line. Trailing empty lines are dropped, but never below
 * `minAnswers`; missing answers are empty, like pressing Enter (`input("Press Enter to open the door")`).
 */
export function parseStdinBox(text: string, minAnswers = 0): string[] {
  const lines = (text ?? "").replace(/\r/g, "").split("\n");
  while (lines.length > minAnswers && lines[lines.length - 1] === "") lines.pop();
  while (lines.length < minAnswers) lines.push("");
  return lines;
}

/** How many input( calls the code has outside comments (a rough count of the answers it needs). */
export function countInputCalls(code: string): number {
  let count = 0;
  for (const line of meaningfulLines(code)) count += [...line.matchAll(/(^|[^\w.])input\s*\(/g)].length;
  return count;
}

export function stdinBoxText(answers: readonly string[] | undefined): string {
  return (answers ?? []).join("\n");
}

/**
 * The answers a run gets. While the box still shows Mar'tu's answers it sends them exactly. Otherwise each
 * line is an answer, and there are at least as many as Mar'tu's answers or the code's input() calls, so an
 * empty answer ("Press Enter to open the door") is never lost.
 */
export function answersFromBox(text: string, scripted: readonly string[] | undefined, code = ""): string[] {
  if (scripted && text === stdinBoxText(scripted)) return [...scripted];
  return parseStdinBox(text, Math.max(scripted?.length ?? 0, countInputCalls(code)));
}

/* ------------------------------------------------------------------------------------------------ */
/* Compare with Mar'tu's version                                                                     */
/* ------------------------------------------------------------------------------------------------ */

export type CompareLine = { text: string; changed: boolean };

/**
 * Line-by-line differences between the student's code and Mar'tu's version (a longest-common-subsequence
 * diff on lines, ignoring trailing spaces and blank lines at the end). Each side keeps its own lines;
 * `changed` marks a line the other side does not have in the same order.
 */
export function compareLines(mine: string, theirs: string): { mine: CompareLine[]; theirs: CompareLine[] } {
  const split = (code: string) => {
    const lines = (code ?? "").replace(/\r/g, "").split("\n").map((line) => line.replace(/\s+$/, ""));
    while (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
    return lines;
  };
  const a = split(mine);
  const b = split(theirs);
  // lcs[i][j] = longest common subsequence of a[i:] and b[j:]
  const lcs: number[][] = Array.from({ length: a.length + 1 }, () => new Array<number>(b.length + 1).fill(0));
  for (let i = a.length - 1; i >= 0; i -= 1) {
    for (let j = b.length - 1; j >= 0; j -= 1) {
      lcs[i][j] = a[i] === b[j] ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
    }
  }
  const sameA = new Array<boolean>(a.length).fill(false);
  const sameB = new Array<boolean>(b.length).fill(false);
  let i = 0;
  let j = 0;
  while (i < a.length && j < b.length) {
    if (a[i] === b[j]) {
      sameA[i] = true;
      sameB[j] = true;
      i += 1;
      j += 1;
    } else if (lcs[i + 1][j] >= lcs[i][j + 1]) {
      i += 1;
    } else {
      j += 1;
    }
  }
  return {
    mine: a.map((text, index) => ({ text, changed: !sameA[index] })),
    theirs: b.map((text, index) => ({ text, changed: !sameB[index] })),
  };
}

/* ------------------------------------------------------------------------------------------------ */
/* Inserting into the editor: Names to use, Mar'tu's pick                                            */
/* ------------------------------------------------------------------------------------------------ */

/** True when the text before the cursor (on its line) leaves a string open. */
export function insideString(lineBefore: string): boolean {
  let quote: string | null = null;
  for (let index = 0; index < lineBefore.length; index += 1) {
    const char = lineBefore[index];
    if (quote) {
      if (char === "\\") index += 1;
      else if (char === quote) quote = null;
    } else if (char === "#") {
      return false;
    } else if (char === '"' || char === "'") {
      quote = char;
    }
  }
  return quote !== null;
}

/** Mar'tu's pick is a `#` note (it goes in as it is, on a line of its own). */
export function pickIsNote(pick: string): boolean {
  return (pick ?? "").trimStart().startsWith("#");
}

/**
 * What Mar'tu's pick puts in the editor: a `#` note as it is; the value itself for a number or a multi-line
 * pick; inside an open string, the bare words; otherwise the words in quotes. A pick authored as a quoted
 * literal (`"Welcome, "`) is used as it is (or without its quotes inside an open string). In a task that only
 * prints (`printOnly`), words that land on a line of their own go in as `print("...")`, so the line does
 * something (`lineAfter` is the rest of the cursor's line: "" for a line of its own).
 */
export function pickInsertion(pick: string, lineBefore: string, options: { printOnly?: boolean; lineAfter?: string } = {}): string {
  const value = pick ?? "";
  if (pickIsNote(value)) return value.trim();
  const literal = value.trim().match(/^(["'])([\s\S]*)\1$/);
  let quoted: string;
  if (literal && value.trim().length >= 2) {
    if (insideString(lineBefore)) return literal[2];
    quoted = value.trim();
  } else {
    if (value.includes("\n") || /^-?\d+(\.\d+)?$/.test(value.trim()) || insideString(lineBefore)) return value;
    quoted = value.includes('"') && !value.includes("'") ? `'${value}'` : `"${value.replace(/"/g, '\\"')}"`;
  }
  if (!options.printOnly || value.includes("\n") || (options.lineAfter ?? "").trim() !== "") return quoted;
  // A task that only prints, and the pick lands on a line of its own: words alone would do nothing there.
  if (lineBefore.trim() === "") return `print(${quoted})`;
  // Right after a finished line (`print("...")|`): a print line of its own under it, not words stuck on the end.
  if (/\)\s*$/.test(lineBefore)) return `\n${lineBefore.match(/^[ \t]*/)?.[0] ?? ""}print(${quoted})`;
  return quoted;
}

/* ------------------------------------------------------------------------------------------------ */
/* Keep it short: Mar'tu's first paragraph                                                           */
/* ------------------------------------------------------------------------------------------------ */

/**
 * The first paragraph of course prose (one paragraph per line; a fenced code block counts as one), and
 * whether there is more after it.
 */
export function firstParagraph(text: string): { first: string; more: boolean } {
  const lines = (text ?? "").replace(/\r\n?/g, "\n").split("\n");
  let start = 0;
  while (start < lines.length && lines[start].trim() === "") start += 1;
  if (start >= lines.length) return { first: "", more: false };
  let end = start + 1;
  if (/^```/.test(lines[start].trim())) {
    while (end < lines.length && !/^```\s*$/.test(lines[end].trim())) end += 1;
    end = Math.min(lines.length, end + 1);
  }
  const first = lines.slice(start, end).join("\n");
  const more = lines.slice(end).some((line) => line.trim() !== "");
  return { first, more };
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
  "from the campaign": "From the campaign",
  everyday: "In everyday life",
  "in tor": "In Tor",
  shorter: "Shorter",
  contrast: "Not this",
  "sentence frame": "Fill the frame",
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
