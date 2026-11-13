/**
 * Checkpoint grading for the Intro to Python course (contracts.ts FlattenChecks / GradeCheckpoints).
 *
 * The client sends every checkpoint's checks as one flat list named `${checkpointId}::${checkName}`
 * (flattenChecks), runs it with runCourse, and regroups the per-check results here. Pure and tested.
 */
import type { CheckResult, RunResult } from "../languages/types";
import type { CheckpointGrade, GradeResult } from "./contracts";
import { closeName, definedNames, explainCourseError, explainQuietSlip, type ExplainContext } from "./explain";
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
 *   "NameError: name 'x' is not defined"   -> "Can't find `x`. ..." (and, given the code, what it made instead)
 *   "TypeError: ..."                       -> "Checking this step hit a problem: ..."
 */
export function checkMessage(raw: string, code = "", context?: ExplainContext): string {
  const text = (raw ?? "").trim();
  if (!text) return NOT_DONE_MESSAGE;
  const assertion = text.match(/^AssertionError(?::\s*([\s\S]*))?$/);
  if (assertion) {
    const message = (assertion[1] ?? "").trim();
    return message || NOT_DONE_MESSAGE;
  }
  const missing = text.match(/^NameError: name '([^']+)' is not defined/);
  if (missing) {
    try {
      return cantFind(missing[1], code, context);
    } catch {
      return cantFind(missing[1], "");
    }
  }
  if (/^[A-Za-z_][\w.]*(Error|Exception):/.test(text)) {
    return `Checking this step hit a problem: ${text}. Look at the values your code makes.`;
  }
  return text;
}

/** "Can't find `health`." plus the name the code made instead, when there is a likely one. */
function cantFind(name: string, code: string, context?: ExplainContext): string {
  const plain = `Can't find \`${name}\`. Make sure your code makes \`${name}\`, spelled exactly like that.`;
  if (!code) return plain;
  const made = [...new Set(definedNames(code).map((entry) => entry.name))].filter((other) => !other.startsWith("_"));
  // `traveler = input(...)` copied from the example, in a task whose variable is `name`.
  const fromExample = context?.example ? new Set(definedNames(context.example).map((entry) => entry.name)) : new Set<string>();
  const copied = made.find((other) => fromExample.has(other) && !(context?.names ?? []).includes(other));
  if (copied) {
    return `Can't find \`${name}\`. Your code made \`${copied}\`, the name from the example. This task uses \`${name}\`.`;
  }
  const close = closeName(name, made);
  if (close && close.toLowerCase() === name.toLowerCase()) {
    return `Can't find \`${name}\`. Your code made \`${close}\`, but capital letters matter: use \`${name}\`.`;
  }
  if (close) return `Can't find \`${name}\`. Your code made \`${close}\`. Check the spelling: the task asks for \`${name}\`.`;
  return plain;
}

function resultFor(results: CheckResult[], index: number, name: string): CheckResult | undefined {
  const atIndex = results[index];
  if (atIndex && atIndex.name === name) return atIndex;
  return results.find((result) => result.name === name);
}

/**
 * Regroup a course run's results by checkpoint. A crash (or a timeout) fails every checkpoint with the
 * friendly explanation of the error; otherwise a checkpoint passes when all of its checks pass, and its
 * message is the first failing check's message. `code` (optional) improves the messages; `context`
 * (optional: the worked example, the task's names, the previous run's traceback) makes them more exact.
 *
 * One exception to "the check's message": a line that runs with no error but does nothing (a lone
 * `"text"` line, `mana - 20`; see explainQuietSlip) is named instead, when it explains the first failing
 * check: the check could not find a variable, the run printed nothing, or the check is about the dashed name.
 */
export function gradeCheckpoints(checkpoints: Checkpoint[], result: RunResult, code = "", context?: ExplainContext): GradeResult {
  const crashed = result.timedOut === true || !result.ok;
  if (crashed) {
    const traceback = result.traceback || (result.timedOut ? TIMEOUT_TRACEBACK : "");
    const message = explainCourseError(traceback, code, context).hint;
    return {
      crashed: true,
      checkpoints: checkpoints.map((checkpoint) => ({ id: checkpoint.id, passed: false, message })),
      firstFailing: checkpoints.length > 0 ? 0 : null,
      allPassed: false,
    };
  }

  const results = result.checks ?? [];
  let flatIndex = 0;
  const rawMessages: string[] = [];
  const grades: CheckpointGrade[] = checkpoints.map((checkpoint) => {
    let message = "";
    let raw = "";
    let passed = true;
    for (const check of checkpoint.checks) {
      const found = resultFor(results, flatIndex, flatCheckName(checkpoint.id, check.name));
      flatIndex += 1;
      if (found?.passed) continue;
      if (passed) {
        message = found ? checkMessage(found.message, code, context) : NOT_CHECKED_MESSAGE;
        raw = found?.message ?? "";
      }
      passed = false;
    }
    rawMessages.push(raw);
    return { id: checkpoint.id, passed, message };
  });
  const firstFailing = grades.findIndex((grade) => !grade.passed);
  if (firstFailing !== -1 && code) {
    const slip = quietSlipFor(code, rawMessages[firstFailing] ?? "", result.stdout ?? "", context);
    if (slip) grades[firstFailing] = { ...grades[firstFailing], message: slip };
  }
  return {
    crashed: false,
    checkpoints: grades,
    firstFailing: firstFailing === -1 ? null : firstFailing,
    allPassed: grades.length > 0 && firstFailing === -1,
  };
}

/** The quiet-slip message for a failing check, or null when the slip does not explain this failure. */
function quietSlipFor(code: string, raw: string, stdout: string, context?: ExplainContext): string | null {
  const missingName = raw.trim().match(/^NameError: name '([^']+)' is not defined/)?.[1];
  const slip = explainQuietSlip(code, { missingName, context });
  if (!slip) return null;
  const printedNothing = stdout.trim() === "";
  switch (slip.kind) {
    case "bare-value":
      return missingName || printedNothing ? slip.hint : null;
    case "bare-name":
    case "print-without-brackets":
      return printedNothing ? slip.hint : null;
    case "dash-no-effect":
      return slip.name && (missingName === slip.name || new RegExp(`\\b${slip.name}\\b`).test(raw)) ? slip.hint : null;
    default:
      return null;
  }
}
