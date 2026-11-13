/**
 * Node-side course runs for vitest and tools. Spawns `python3` and runs a job with EXACTLY the browser
 * worker's "course-run" semantics: a fresh namespace, public/workers/course_helpers.py (import guard,
 * check helpers, input() shim, runner), the campaign GUARD only when `engine` is true, then
 * `_course_run(code, setup, checks, stdin)`. Server/test only (it uses child_process).
 */
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import type { RunResult } from "../languages/types";
import { parseStageMessage, type StageEvent } from "../stage/bridge";
import { workerPrelude } from "../lesson/run-checks";
import type { CourseCheck } from "./schema";

/** Same text as COURSE_TIMEOUT_TRACEBACK in src/lib/languages/python/run.ts. */
export const NODE_COURSE_TIMEOUT_TRACEBACK = "TimeoutError: The program ran too long and was stopped.";

/** The browser stops a run after 5 seconds; give a cold python3 a little more. */
const DEFAULT_TIMEOUT_MS = 8000;

const MARKER = "\n@@course-run-result@@\n";

export type CourseRunOptions = {
  setup?: string;
  stdin?: string[];
  engine?: boolean;
  /** Kill the run after this long and report `timedOut: true` (default 8000 ms). */
  timeoutMs?: number;
};

export type NodeCourseRunResult = RunResult & {
  /** The last line of the traceback ("NameError: name 'x' is not defined"), or "" when ok. */
  error: string;
};

export function courseHelpersPath(): string {
  return path.join(process.cwd(), "public/workers/course_helpers.py");
}

export function courseHelpersSource(): string {
  return readFileSync(courseHelpersPath(), "utf8");
}

export function pythonExecutable(): string {
  return process.env.COURSE_PYTHON || "python3";
}

// Mirrors createGlobals() in python-worker.js (only installed when the engine is on, like the worker).
const RUNNER = `
import json
import sys

payload = json.loads(sys.stdin.read())
ns = {"__name__": "__main__"}
events = []
if payload["engine"]:
    ns["_stage_say"] = lambda text: events.append({"type": "say", "text": str(text)})
    ns["_stage_flare"] = lambda: events.append({"type": "flare"})
    ns["_stage_focus"] = lambda image_id: events.append({"type": "focus", "imageId": str(image_id)})
    ns["_stage_move"] = lambda direction: events.append({"type": "move", "direction": str(direction)})
    ns["_stage_prompt"] = lambda text: events.append({"type": "prompt", "text": str(text)})
    ns["_stage_options"] = lambda count: events.append({"type": "options", "options": [""] * int(count)})
    ns["_stage_option"] = lambda index, text: events[-1]["options"].__setitem__(int(index), str(text))
    ns["_stage_speak"] = lambda option: events.append({"type": "speak", "option": str(option)})
    ns["_stage_highlight"] = lambda option: events.append({"type": "highlight", "option": str(option)})
    ns["_stage_cast"] = lambda name: events.append({"type": "cast", "name": str(name)})
    ns["_stage_mana"] = lambda name, bar, mana, maximum: events.append(
        {"type": "mana", "name": str(name), "bar": str(bar), "mana": int(mana), "max": int(maximum)}
    )
    ns["_stage_roll"] = lambda skill, roll, success, required: events.append(
        {"type": "roll", "skill": str(skill), "roll": int(roll), "success": bool(success), "required": int(required)}
    )
exec(compile(payload["helpers"], "course_helpers.py", "exec"), ns)
if payload["engine"]:
    exec(compile(payload["guard"], "<guard>", "exec"), ns)
result = ns["_course_run"](payload["code"], payload["setup"], payload["checks"], payload["stdin"])
result["stageEvents"] = events
sys.__stdout__.write(payload["marker"] + json.dumps(result))
sys.__stdout__.flush()
`;

type RawResult = {
  ok: boolean;
  stdout: string;
  stderr: string;
  traceback: string;
  error: string;
  checks: { name: string; passed: boolean; message: string }[];
  stageEvents: unknown[];
};

function toStageEvents(events: unknown[]): StageEvent[] {
  return events.flatMap((event) => {
    const parsed = parseStageMessage(event);
    return parsed ? [parsed] : [];
  });
}

/**
 * Run `code` with `checks` exactly like a browser course run. Returns the ordinary RunResult
 * (checks in the order sent) plus the one-line `error`. Throws only when python3 itself fails.
 */
export function runCourseChecks(
  code: string,
  checks: CourseCheck[],
  options: CourseRunOptions = {},
): NodeCourseRunResult {
  const engine = options.engine === true;
  const payload = {
    helpers: courseHelpersSource(),
    guard: engine ? workerPrelude() : "",
    engine,
    code,
    setup: options.setup ?? "",
    checks: checks.map((check) => ({ name: check.name, code: check.code })),
    stdin: options.stdin ?? [],
    marker: MARKER,
  };
  const child = spawnSync(pythonExecutable(), ["-I", "-c", RUNNER], {
    input: JSON.stringify(payload),
    encoding: "utf8",
    timeout: options.timeoutMs ?? DEFAULT_TIMEOUT_MS,
    killSignal: "SIGKILL",
    maxBuffer: 64 * 1024 * 1024,
  });
  const timedOut =
    (child.error as NodeJS.ErrnoException | undefined)?.code === "ETIMEDOUT" ||
    (child.signal === "SIGKILL" && child.status === null);
  if (timedOut) {
    return {
      ok: false,
      stdout: "",
      stderr: "",
      traceback: NODE_COURSE_TIMEOUT_TRACEBACK,
      error: NODE_COURSE_TIMEOUT_TRACEBACK,
      checks: [],
      stageEvents: [],
      timedOut: true,
    };
  }
  if (child.error) throw child.error;
  const out = child.stdout ?? "";
  const at = out.lastIndexOf(MARKER);
  if (child.status !== 0 || at < 0) {
    throw new Error(`python3 failed to run the course job: ${(child.stderr || out).trim().slice(-2000)}`);
  }
  const raw = JSON.parse(out.slice(at + MARKER.length)) as RawResult;
  return {
    ok: raw.ok,
    stdout: raw.stdout,
    stderr: raw.stderr,
    traceback: raw.traceback,
    error: raw.error,
    checks: raw.checks,
    stageEvents: toStageEvents(raw.stageEvents ?? []),
  };
}
