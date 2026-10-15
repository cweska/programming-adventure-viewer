import type { Explanation } from "../lib/languages/types";
import type { FailedCheck } from "../lib/lesson/progression";

export function ConsolePanel({
  output,
  explainer,
  feedback,
  failedChecks,
}: {
  output: string;
  explainer: Explanation | null;
  feedback: string | null;
  failedChecks: FailedCheck[];
}) {
  return (
    <section className="console" data-testid="console" aria-live="polite">
      <h2>Console</h2>
      <pre className="program-output" data-testid="stdout">
        {output || "Program output will appear here."}
      </pre>
      {explainer ? (
        <div className="explainer" data-testid="explainer">
          <h3>{explainer.title}</h3>
          <p data-testid="explainer-hint">{explainer.hint}</p>
          {explainer.raw ? (
            <details>
              <summary>Traceback</summary>
              <pre data-testid="traceback">{explainer.raw}</pre>
            </details>
          ) : null}
        </div>
      ) : null}
      {feedback ? (
        <p className="feedback" data-testid="feedback">
          {feedback}
        </p>
      ) : null}
      {failedChecks.map((check) => (
        <p key={check.name} className="failed-check" data-testid="failed-check">
          <strong>{check.name}.</strong> {check.message}
        </p>
      ))}
    </section>
  );
}
