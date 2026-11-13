import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

type Listener = (event: { data: unknown }) => void;

/** A stand-in for the Pyodide module worker: answers "ready", then each message with `respond`. */
class FakeWorker {
  static instances: FakeWorker[] = [];
  static respond: (message: Record<string, unknown>) => Record<string, unknown> | null = () => null;
  readonly url: string;
  readonly options: unknown;
  readonly posted: Record<string, unknown>[] = [];
  terminated = false;
  private listeners = new Map<string, Set<Listener>>();

  constructor(url: string, options: unknown) {
    this.url = url;
    this.options = options;
    FakeWorker.instances.push(this);
    queueMicrotask(() => this.emit("message", { type: "ready" }));
  }

  addEventListener(type: string, listener: Listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, new Set());
    this.listeners.get(type)?.add(listener);
  }

  removeEventListener(type: string, listener: Listener) {
    this.listeners.get(type)?.delete(listener);
  }

  postMessage(message: Record<string, unknown>) {
    this.posted.push(message);
    const reply = FakeWorker.respond(message);
    if (reply) queueMicrotask(() => this.emit("message", { type: "result", requestId: message.requestId, ...reply }));
  }

  terminate() {
    this.terminated = true;
  }

  private emit(type: string, data: unknown) {
    for (const listener of [...(this.listeners.get(type) ?? [])]) listener({ data });
  }
}

beforeEach(() => {
  vi.resetModules();
  FakeWorker.instances = [];
  vi.stubGlobal("Worker", FakeWorker);
  vi.stubGlobal("window", globalThis);
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("runCourse", () => {
  it("posts a course-run message and resolves with the run result", async () => {
    FakeWorker.respond = (message) =>
      message.type === "course-run"
        ? {
            ok: true,
            stdout: "Name? Lucky\nHi Lucky\n",
            stderr: "",
            traceback: "",
            checks: [{ name: "greet::prints", passed: true, message: "" }],
            stageEvents: [{ type: "move", direction: "left" }, { type: "bogus" }],
          }
        : null;
    const { runCourse } = await import("./run");
    const result = await runCourse({
      code: "name = input('Name? ')\nprint('Hi ' + name)\n",
      checks: [{ name: "greet::prints", code: "assert True" }],
      stdin: ["Lucky"],
      engine: true,
    });
    expect(result).toEqual({
      ok: true,
      stdout: "Name? Lucky\nHi Lucky\n",
      stderr: "",
      traceback: "",
      checks: [{ name: "greet::prints", passed: true, message: "" }],
      stageEvents: [{ type: "move", direction: "left" }],
    });
    const worker = FakeWorker.instances[0];
    expect(worker?.url).toMatch(/\/workers\/python-worker\.js$/);
    expect(worker?.options).toEqual({ type: "module" });
    expect(worker?.posted[0]).toEqual({
      type: "course-run",
      code: "name = input('Name? ')\nprint('Hi ' + name)\n",
      checks: [{ name: "greet::prints", code: "assert True" }],
      setup: "",
      stdin: ["Lucky"],
      engine: true,
      requestId: 1,
    });
  });

  it("defaults setup, stdin and engine", async () => {
    FakeWorker.respond = () => ({ ok: true, stdout: "", stderr: "", traceback: "", checks: [], stageEvents: [] });
    const { runCourse } = await import("./run");
    await runCourse({ code: "print(1)\n", checks: [] });
    expect(FakeWorker.instances[0]?.posted[0]).toMatchObject({ setup: "", stdin: [], engine: false });
  });

  it("turns the time limit into a timedOut result and restarts the worker", async () => {
    vi.useFakeTimers();
    FakeWorker.respond = (message) =>
      message.code === "print(2)\n" ? { ok: true, stdout: "2\n", stderr: "", traceback: "", checks: [], stageEvents: [] } : null;
    const { runCourse } = await import("./run");
    const pending = runCourse({ code: "while True:\n    pass\n", checks: [{ name: "c", code: "assert True" }] });
    await vi.advanceTimersByTimeAsync(5001);
    expect(await pending).toEqual({
      ok: false,
      stdout: "",
      stderr: "",
      traceback: "TimeoutError: The program ran too long and was stopped.",
      checks: [],
      stageEvents: [],
      timedOut: true,
    });
    expect(FakeWorker.instances[0]?.terminated).toBe(true);

    const next = await runCourse({ code: "print(2)\n", checks: [] });
    expect(next.stdout).toBe("2\n");
    expect(FakeWorker.instances).toHaveLength(2);
  });
});
