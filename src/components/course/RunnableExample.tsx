"use client";

import { useState } from "react";
import { explainCourseError } from "../../lib/course/explain";
import { runCourse } from "../../lib/languages/python/run";
import type { Explanation, RunResult } from "../../lib/languages/types";
import { PYTHON_STATUS_TEXT, usePythonStatus } from "./usePythonStatus";

export type RunView = {
  stdout: string;
  explanation: Explanation | null;
  /** Set when Python itself could not run the code. */
  failure?: string;
};

export function runView(code: string, result: RunResult): RunView {
  if (result.ok) return { stdout: result.stdout, explanation: null };
  return { stdout: result.stdout, explanation: explainCourseError(result.traceback || result.stderr, code) };
}

export const PYTHON_FAILED = "Python could not run this. Check the internet, then press Run again.";

/** Program output and, when it crashed, the plain-language explanation. Announced politely. */
export function RunOutput({ view, testId, label = "Output" }: { view: RunView | null; testId?: string; label?: string }) {
  return (
    <div className="run-output" aria-live="polite" data-testid={testId}>
      {view ? (
        <>
          <p className="run-output-label">{label}</p>
          {view.failure ? <p className="run-output-failure">{view.failure}</p> : null}
          {view.failure ? null : view.stdout.length > 0 ? (
            <pre className="run-output-text">{view.stdout}</pre>
          ) : view.explanation ? null : (
            <pre className="run-output-text">(nothing printed)</pre>
          )}
          {view.explanation ? (
            <div className="run-output-error">
              <p className="run-output-error-title">{view.explanation.title}</p>
              <p>{view.explanation.hint}</p>
              {view.explanation.raw ? (
                <details>
                  <summary>Python&apos;s message</summary>
                  <pre>{view.explanation.raw}</pre>
                </details>
              ) : null}
            </div>
          ) : null}
        </>
      ) : null}
    </div>
  );
}

/**
 * A worked example: read-only code with a Run button that shows what it prints. Example code runs with
 * no checks; `stdin` answers its input() calls.
 */
export function RunnableExample({
  code,
  stdin,
  index,
  testPrefix = "example",
  title,
}: {
  code: string;
  stdin?: string[];
  /** 1-based number for labels and test ids (`${testPrefix}-run-${index}`). */
  index: number;
  testPrefix?: string;
  title?: string;
}) {
  const [view, setView] = useState<RunView | null>(null);
  const [running, setRunning] = useState(false);
  const [wanted, setWanted] = useState(false);
  const status = usePythonStatus(wanted);

  const run = async () => {
    setWanted(true);
    setRunning(true);
    try {
      const result = await runCourse({ code, checks: [], stdin });
      setView(runView(code, result));
    } catch {
      setView({ stdout: "", explanation: null, failure: PYTHON_FAILED });
    } finally {
      setRunning(false);
    }
  };

  return (
    <figure className="runnable-example" data-testid={`${testPrefix}-${index}`}>
      <figcaption>{title ?? `Example ${index}`}</figcaption>
      <pre className="example-code" aria-label={`Example ${index} code`}>
        <code>{code.replace(/\n$/, "")}</code>
      </pre>
      {stdin && stdin.length > 0 ? (
        <p className="example-stdin">
          When it asks, the answer{stdin.length > 1 ? "s are" : " is"}:{" "}
          {stdin.map((answer, at) => (
            <span key={at}>
              {at > 0 ? ", " : null}
              <code className="inline-code">{answer}</code>
            </span>
          ))}
        </p>
      ) : null}
      <div className="example-toolbar">
        <button type="button" onClick={run} disabled={running} data-testid={`${testPrefix}-run-${index}`}>
          {running ? "Running…" : "Run"}
        </button>
        {running && status === "loading" ? <span className="python-status">{PYTHON_STATUS_TEXT.loading}</span> : null}
      </div>
      <RunOutput view={view} testId={`${testPrefix}-output-${index}`} />
    </figure>
  );
}
