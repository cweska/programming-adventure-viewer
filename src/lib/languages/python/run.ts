import { publicPath } from "../../site";
import type { RunInput, RunResult } from "../types";
import { parseStageMessage, type StageEvent } from "../../stage/bridge";

const TIMEOUT_MS = 5000;

type WorkerResult = {
  type: "result";
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

export async function runPython(input: RunInput): Promise<RunResult> {
  if (typeof window === "undefined") {
    throw new Error("Python runs in the browser.");
  }
  await boot();
  const current = worker;
  if (!current) throw new Error(failReason ?? "Python is not available.");

  return new Promise((resolve, reject) => {
    const timer = window.setTimeout(() => {
      current.removeEventListener("message", onMessage);
      current.terminate();
      worker = null;
      ready = null;
      reject(new PythonTimeoutError());
    }, TIMEOUT_MS);

    const onMessage = (event: MessageEvent<WorkerResult | ReadyMessage | FailedMessage>) => {
      if (event.data?.type !== "result") return;
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
    current.postMessage({
      type: "run",
      code: input.code,
      checks: input.checks,
    });
  });
}
