/**
 * Checkpoint grading for the Intro to Python course (contracts.ts FlattenChecks / GradeCheckpoints).
 *
 * The client sends every checkpoint's checks as one flat list named `${checkpointId}::${checkName}`
 * (flattenChecks), runs it with runCourse, and regroups the per-check results here. Pure and tested.
 */
import type { CheckResult, RunResult } from "../languages/types";
import type { CheckpointGrade, GradeResult } from "./contracts";
import { explainCourseError } from "./explain";
import type { Checkpoint, CourseCheck } from "./schema";

export const CHECK_SEPARATOR = "::";

const TIMEOUT_TRACEBACK = "TimeoutError: The program ran too long and was stopped.";

/** Shown for a bare `assert ...` with no message. */
export const NOT_DONE_MESSAGE = "This step is not done yet. Read it again, or open a hint.";

/** Shown when a check result is missing (should not happen; the run was cut short). */
export const NOT_CHECKED_MESSAGE = "This step was not checked. Press Run again.";

export function flatCheckName(checkpointId: string, checkName: string): string {
  return `${checkpointId}${CHECK_SEPARATOR}${checkName}`;
}

/** Every checkpoint's checks, in order, as one list for runCourse. */
export function flattenChecks(checkpoints: Checkpoint[]): CourseCheck[] {
  return checkpoints.flatMap((checkpoint) =>
    checkpoint.checks.map((check) => ({ name: flatCheckName(checkpoint.id, check.name), code: check.code })),
  );
}

/**
 * Turn a failing check's raw message into what the student reads.
 *   "AssertionError: Print Hello."         -> "Print Hello."
 *   "AssertionError"                       -> NOT_DONE_MESSAGE
 *   "NameError: name 'x' is not defined"   -> "Can't find `x`. ..."
 *   "TypeError: ..."                       -> "Checking this step hit a problem: ..."
 */
export function checkMessage(raw: string): string {
  const text = (raw ?? "").trim();
  if (!text) return NOT_DONE_MESSAGE;
  const assertion = text.match(/^AssertionError(?::\s*([\s\S]*))?$/);
  if (assertion) {
    const message = (assertion[1] ?? "").trim();
    return message || NOT_DONE_MESSAGE;
  }
  const missing = text.match(/^NameError: name '([^']+)' is not defined/);
  if (missing) {
    return `Can't find \`${missing[1]}\`. Make sure your code makes \`${missing[1]}\`, spelled exactly like that.`;
  }
  if (/^[A-Za-z_][\w.]*(Error|Exception):/.test(text)) {
    return `Checking this step hit a problem: ${text}. Look at the values your code makes.`;
  }
  return text;
}

function resultFor(results: CheckResult[], index: number, name: string): CheckResult | undefined {
  const atIndex = results[index];
  if (atIndex && atIndex.name === name) return atIndex;
  return results.find((result) => result.name === name);
}

/**
 * Regroup a course run's results by checkpoint. A crash (or a timeout) fails every checkpoint with the
 * friendly explanation of the error; otherwise a checkpoint passes when all of its checks pass, and its
 * message is the first failing check's message. `code` (optional) improves the crash explanation.
 */
export function gradeCheckpoints(checkpoints: Checkpoint[], result: RunResult, code = ""): GradeResult {
  const crashed = result.timedOut === true || !result.ok;
  if (crashed) {
    const traceback = result.traceback || (result.timedOut ? TIMEOUT_TRACEBACK : "");
    const message = explainCourseError(traceback, code).hint;
    return {
      crashed: true,
      checkpoints: checkpoints.map((checkpoint) => ({ id: checkpoint.id, passed: false, message })),
      firstFailing: checkpoints.length > 0 ? 0 : null,
      allPassed: false,
    };
  }

  const results = result.checks ?? [];
  let flatIndex = 0;
  const grades: CheckpointGrade[] = checkpoints.map((checkpoint) => {
    let message = "";
    let passed = true;
    for (const check of checkpoint.checks) {
      const found = resultFor(results, flatIndex, flatCheckName(checkpoint.id, check.name));
      flatIndex += 1;
      if (found?.passed) continue;
      if (passed) message = found ? checkMessage(found.message) : NOT_CHECKED_MESSAGE;
      passed = false;
    }
    return { id: checkpoint.id, passed, message };
  });
  const firstFailing = grades.findIndex((grade) => !grade.passed);
  return {
    crashed: false,
    checkpoints: grades,
    firstFailing: firstFailing === -1 ? null : firstFailing,
    allPassed: grades.length > 0 && firstFailing === -1,
  };
}
