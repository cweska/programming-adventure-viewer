import type { Explanation } from "../lib/languages/types";
import type { FailedCheck } from "../lib/lesson/progression";

const EMPTY_OUTPUT = "Program output will appear here.";

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
  const hasStdout = output.length > 0;
  const hasExplainer = explainer !== null;
  const hasFlavor = Boolean(feedback);
  const hasPython = hasStdout || hasExplainer;
  const showDivider = hasPython && hasFlavor;
  const showPlaceholder = !hasPython && !hasFlavor && failedChecks.length === 0;

  return (
    <section className="console" data-testid="console" aria-live="polite">
      <h2>Console</h2>
      {showPlaceholder ? (
        <pre className="program-output" data-testid="stdout">
          {EMPTY_OUTPUT}
        </pre>
      ) : null}
      {hasStdout ? (
        <pre className="program-output" data-testid="stdout">
          {output}
        </pre>
      ) : null}
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
      {showDivider ? <hr className="console-divider" data-testid="console-divider" /> : null}
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
