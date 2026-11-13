import { publicPath } from "../../site";
import type { CourseRunInput } from "../../course/contracts";
import type { LiveSession, RunInput, RunResult } from "../types";
import { parseStageMessage, type StageEvent } from "../../stage/bridge";

const TIMEOUT_MS = 5000;

type WorkerResult = {
  type: "result";
  requestId: number;
  ok: boolean;
  stdout: string;
  stderr: string;
  traceback: string;
  checks: { name: string; passed: boolean; message: string }[];
  stageEvents: unknown[];
};

type ReadyMessage = { type: "ready" };
type FailedMessage = { type: "failed"; message: string };

let worker: Worker | null = null;
let ready: Promise<void> | null = null;
let failReason: string | null = null;
let nextRequest = 1;
let nextSession = 1;
let generation = 0;
let queue: Promise<unknown> = Promise.resolve();

function boot(): Promise<void> {
  if (ready && worker) return ready;
  failReason = null;
  worker = new Worker(publicPath("/workers/python-worker.js"), { type: "module" });
  const currentWorker = worker;
  ready = new Promise((resolve, reject) => {
    if (!currentWorker) {
      reject(new Error("Python worker did not start."));
      return;
    }
    const fail = (message: string) => {
      failReason = message;
      worker = null;
      ready = null;
      reject(new Error(message));
    };
    const onMessage = (event: MessageEvent<ReadyMessage | FailedMessage>) => {
      if (event.data?.type === "ready") {
        currentWorker.removeEventListener("message", onMessage);
        resolve();
      } else if (event.data?.type === "failed") {
        currentWorker.removeEventListener("message", onMessage);
        fail(event.data.message);
      }
    };
    currentWorker.addEventListener("message", onMessage);
    currentWorker.addEventListener("error", () => {
      fail("Python failed to load in the browser.");
    });
  });
  return ready;
}

export function whenPythonReady(): Promise<void> {
  if (typeof window === "undefined") {
    return Promise.reject(new Error("Python runs in the browser."));
  }
  return boot();
}

function toStageEvents(events: unknown[]): StageEvent[] {
  return events.flatMap((event) => {
    const parsed = parseStageMessage(event);
    return parsed ? [parsed] : [];
  });
}

export class PythonTimeoutError extends Error {
  readonly timedOut = true;
  constructor() {
    super("The program ran too long and was stopped.");
    this.name = "PythonTimeoutError";
  }
}

function send(message: Record<string, unknown>): Promise<RunResult> {
  const job = queue.then(async () => {
    if (typeof window === "undefined") {
      throw new Error("Python runs in the browser.");
    }
    await boot();
    const current = worker;
    if (!current) throw new Error(failReason ?? "Python is not available.");
    const requestId = nextRequest++;

    return new Promise<RunResult>((resolve, reject) => {
      const timer = window.setTimeout(() => {
        current.removeEventListener("message", onMessage);
        current.terminate();
        worker = null;
        ready = null;
        generation += 1;
        reject(new PythonTimeoutError());
      }, TIMEOUT_MS);

      const onMessage = (event: MessageEvent<WorkerResult | ReadyMessage | FailedMessage>) => {
        if (event.data?.type !== "result" || event.data.requestId !== requestId) return;
        window.clearTimeout(timer);
        current.removeEventListener("message", onMessage);
        const data = event.data;
        resolve({
          ok: data.ok,
          stdout: data.stdout,
          stderr: data.stderr,
          traceback: data.traceback,
          checks: data.checks ?? [],
          stageEvents: toStageEvents(data.stageEvents ?? []),
        });
      };

      current.addEventListener("message", onMessage);
      current.postMessage({ ...message, requestId });
    });
  });
  queue = job.catch(() => undefined);
  return job;
}

export function runPython(input: RunInput): Promise<RunResult> {
  return send({ type: "run", code: input.code, checks: input.checks, setup: input.setup ?? "" });
}

/** The traceback a course run reports when it hits the time limit (explainCourseError knows it). */
export const COURSE_TIMEOUT_TRACEBACK = "TimeoutError: The program ran too long and was stopped.";

/**
 * One Intro to Python course run (contracts.ts RunCourse): fresh globals, the course helpers, the campaign
 * engine only when `engine` is true, scripted input() answers, setup, the code, then the checks.
 * A run that hits the time limit resolves with `timedOut: true` (the worker is restarted); it only
 * rejects when Python itself cannot load.
 */
export async function runCourse(input: CourseRunInput): Promise<RunResult> {
  try {
    return await send({
      type: "course-run",
      code: input.code,
      checks: input.checks.map((check) => ({ name: check.name, code: check.code })),
      setup: input.setup ?? "",
      stdin: input.stdin ?? [],
      engine: input.engine === true,
    });
  } catch (error) {
    if (error instanceof PythonTimeoutError) {
      return {
        ok: false,
        stdout: "",
        stderr: "",
        traceback: COURSE_TIMEOUT_TRACEBACK,
        checks: [],
        stageEvents: [],
        timedOut: true,
      };
    }
    throw error;
  }
}

export async function startPythonSession(input: {
  setup?: string;
  code: string;
}): Promise<{ session: LiveSession; result: RunResult }> {
  const id = `session-${nextSession++}`;
  const result = await send({ type: "session-start", id, code: input.code, setup: input.setup ?? "" });
  const owner = generation;
  let ended = false;
  const session: LiveSession = {
    call(code: string) {
      if (ended || owner !== generation) {
        return Promise.resolve({
          ok: false,
          stdout: "",
          stderr: "",
          traceback: "RuntimeError: The game session has ended. Press Run to start it again.",
          checks: [],
          stageEvents: [],
        });
      }
      return send({ type: "session-call", id, code });
    },
    end() {
      if (ended) return;
      ended = true;
      if (worker && owner === generation) worker.postMessage({ type: "session-end", id });
    },
  };
  return { session, result };
}
