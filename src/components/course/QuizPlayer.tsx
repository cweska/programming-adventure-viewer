"use client";

import Link from "next/link";
import { useEffect, useId, useMemo, useRef, useState } from "react";
import type { ItemPageProps } from "../../lib/course/contracts";
import { itemKey, markTestedOut, quickCheckPassed, quickCheckQuestions, recordQuiz, useCourseProgress } from "../../lib/course/progress";
import type { GlossaryEntry, Question, QuizItem } from "../../lib/course/schema";
import { runCourse } from "../../lib/languages/python/run";
import { PythonEditor } from "../PythonEditor";
import { KindBadge } from "./CourseBits";
import { itemHref } from "./course-links";
import { ParsonsBoard } from "./ParsonsBoard";
import { Prose } from "./Prose";
import {
  emptyResponse,
  gradeWithoutPython,
  hasAnswer,
  outputMatches,
  parsonsBlocks,
  parsonsCode,
  quizPercent,
  responseText,
  type QuizResponse,
} from "./quiz-grading";
import { PYTHON_FAILED, RunOutput, runView, type RunView } from "./RunnableExample";
import { PYTHON_STATUS_TEXT, usePythonStatus } from "./usePythonStatus";

type Checked = {
  correct: boolean;
  /** Output of a parsons/bug run. */
  view?: RunView;
  note?: string;
};

const TYPE_HINT: Record<Question["type"], string> = {
  mc: "Pick one answer.",
  predict: "What will this code print?",
  fill: "Fill in the blank.",
  parsons: "Put the lines in order.",
  bug: "Fix the code, then check it.",
};

/** Choices that look like code show in the code font. */
function looksLikeCode(text: string): boolean {
  return !text.includes("`") && /[=()[\]{}"'+*#]|^\s*\d+\s*$/.test(text);
}

function stripNewline(code: string): string {
  return code.replace(/\n$/, "");
}

function CodeBlock({ code, label = "Python code" }: { code: string; label?: string }) {
  return (
    <pre className="quiz-code" aria-label={label}>
      <code>{stripNewline(code)}</code>
    </pre>
  );
}

function ChoiceList({
  question,
  choices,
  chosen,
  locked,
  output,
  onChoose,
}: {
  question: Question;
  choices: string[];
  chosen: number | null;
  locked: boolean;
  output: boolean;
  onChoose: (index: number) => void;
}) {
  const name = useId();
  return (
    <div className="quiz-choices" role="radiogroup" aria-label="Answers">
      {choices.map((choice, index) => {
        const id = `${name}-${index}`;
        return (
          <label
            key={index}
            htmlFor={id}
            className={`quiz-choice${chosen === index ? " is-chosen" : ""}`}
            data-testid={`quiz-choice-${question.id}-${index}`}
          >
            <input
              id={id}
              type="radio"
              name={name}
              checked={chosen === index}
              disabled={locked}
              onChange={() => onChoose(index)}
            />
            {output ? (
              <pre className="quiz-choice-output">{choice}</pre>
            ) : looksLikeCode(choice) ? (
              <code className="quiz-choice-code">{choice}</code>
            ) : (
              <Prose text={choice} inline className="quiz-choice-text" />
            )}
          </label>
        );
      })}
    </div>
  );
}

function FillCode({
  question,
  text,
  locked,
  onChange,
}: {
  question: Extract<Question, { type: "fill" }>;
  text: string;
  locked: boolean;
  onChange: (text: string) => void;
}) {
  const parts = stripNewline(question.code).split("___");
  if (parts.length < 2) {
    return (
      <>
        <CodeBlock code={question.code} />
        <label className="quiz-typed">
          <span>Your answer</span>
          <input value={text} readOnly={locked} onChange={(event) => onChange(event.target.value)} data-testid="quiz-fill-input" />
        </label>
      </>
    );
  }
  return (
    <pre className="quiz-code quiz-fill" aria-label="Python code with a blank">
      <code>
        {parts.map((part, index) => (
          <span key={index}>
            {part}
            {index < parts.length - 1 ? (
              <input
                className="quiz-blank"
                aria-label="The blank"
                value={text}
                size={Math.max(4, text.length + 1)}
                readOnly={locked}
                autoComplete="off"
                autoCapitalize="off"
                spellCheck={false}
                onChange={(event) => onChange(event.target.value)}
                data-testid="quiz-fill-input"
              />
            ) : null}
          </span>
        ))}
      </code>
    </pre>
  );
}

function CorrectAnswer({ question }: { question: Question }) {
  switch (question.type) {
    case "mc":
      return (
        <p>
          The answer:{" "}
          {looksLikeCode(question.choices[question.answer] ?? "") ? (
            <code className="inline-code">{question.choices[question.answer]}</code>
          ) : (
            <Prose text={question.choices[question.answer] ?? ""} inline />
          )}
        </p>
      );
    case "predict":
      return (
        <>
          <p>It prints:</p>
          <pre className="quiz-answer-output">{question.answer}</pre>
        </>
      );
    case "fill":
      return (
        <p>
          The blank is <code className="inline-code">{question.answer}</code>
        </p>
      );
    case "parsons":
      return (
        <>
          <p>One order that works:</p>
          <CodeBlock code={parsonsCode(question.lines)} />
        </>
      );
    case "bug":
      return (
        <>
          <p>One way to fix it:</p>
          <CodeBlock code={question.fix} />
        </>
      );
    default:
      return null;
  }
}

function Feedback({
  question,
  response,
  checked,
  glossary,
}: {
  question: Question;
  response: QuizResponse | undefined;
  checked: Checked;
  glossary: readonly GlossaryEntry[];
}) {
  const whyWrong =
    question.type === "mc" && response?.type === "mc" && response.choice !== null && !checked.correct
      ? question.whyWrong[String(response.choice)]
      : undefined;
  return (
    <div className={`quiz-feedback ${checked.correct ? "is-right" : "is-wrong"}`} data-testid="quiz-feedback" data-correct={checked.correct}>
      <p className="quiz-verdict">
        <span aria-hidden="true">{checked.correct ? "✓" : "✗"}</span> {checked.correct ? "Right!" : "Not quite."}
      </p>
      {checked.note ? <p className="quiz-note">{checked.note}</p> : null}
      {whyWrong ? <Prose text={whyWrong} glossary={glossary} className="quiz-why-wrong" /> : null}
      {!checked.correct ? <CorrectAnswer question={question} /> : null}
      <Prose text={question.explain} glossary={glossary} className="quiz-explain" />
    </div>
  );
}

/**
 * A quiz: one question at a time, "Check" shows right or wrong with the explanation, and the score at the
 * end. The best score is saved. "Ready" at settings.quizReadyPercent never blocks anything. No timers,
 * unlimited retakes.
 */
function QuizRun({ unit, item, glossary, nextHref, settings }: ItemPageProps<QuizItem>) {
  const progress = useCourseProgress();
  const key = itemKey(unit.id, item.id);
  const saved = progress.quizzes[key];
  const questions = item.questions;
  const total = questions.length;

  const [attempt, setAttempt] = useState(0);
  const [index, setIndex] = useState(0);
  const [responses, setResponses] = useState<Record<string, QuizResponse>>({});
  const [checked, setChecked] = useState<Record<string, Checked>>({});
  const [checking, setChecking] = useState(false);
  const [running, setRunning] = useState(false);
  const [runViews, setRunViews] = useState<Record<string, RunView>>({});
  const [finished, setFinished] = useState<{ correct: number; percent: number } | null>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const feedbackRef = useRef<HTMLDivElement>(null);
  const resultRef = useRef<HTMLHeadingElement>(null);
  const moved = useRef(false);

  // A Quick Check form's questions (the quiz `<form>-questions`, when the form needs them): a pass here can
  // finish the Quick Check.
  const form = unit.items.find((entry) => entry.kind === "testout" && `${entry.id}-questions` === item.id && entry.questionsToPass);
  const gate = form ? quickCheckQuestions(unit.id, form, unit.items, progress) : null;
  const formPassed = form ? quickCheckPassed(unit.id, form, unit.items, progress) : false;
  const testedOut = progress.testedOut[unit.id] === true;
  useEffect(() => {
    if (formPassed && !testedOut) markTestedOut(unit.id);
  }, [formPassed, testedOut, unit.id]);

  const needsPython = questions.some((question) => question.type === "bug" || question.type === "parsons");
  const pythonStatus = usePythonStatus(needsPython);

  const question = questions[Math.min(index, total - 1)];
  const response = responses[question.id] ?? emptyResponse(question);
  const result = checked[question.id];
  const locked = result !== undefined;
  const blocks = useMemo(
    () => (question.type === "parsons" ? parsonsBlocks(question, attempt) : []),
    [question, attempt],
  );

  useEffect(() => {
    if (!moved.current) return;
    moved.current = false;
    (finished ? resultRef.current : headingRef.current)?.focus();
  }, [index, finished, attempt]);

  const setResponse = (next: QuizResponse) => {
    if (locked) return;
    setResponses((all) => ({ ...all, [question.id]: next }));
  };

  const finish = (allChecked: Record<string, Checked>) => {
    const correct = questions.filter((entry) => allChecked[entry.id]?.correct).length;
    const percent = quizPercent(correct, total);
    const answers: Record<string, string> = {};
    for (const entry of questions) answers[entry.id] = responseText(entry, responses[entry.id] ?? emptyResponse(entry));
    recordQuiz(key, percent, answers);
    moved.current = true;
    setFinished({ correct, percent });
  };

  const runCode = async (code: string): Promise<RunView> => {
    try {
      const run = await runCourse({ code, checks: [] });
      return runView(code, run, { unitOrder: unit.order });
    } catch {
      return { stdout: "", explanation: null, failure: PYTHON_FAILED };
    }
  };

  const check = async () => {
    if (locked || checking || !hasAnswer(response)) return;
    setChecking(true);
    try {
      let outcome: Checked;
      const quick = gradeWithoutPython(question, response);
      if (quick !== null) {
        outcome = { correct: quick };
      } else if (question.type === "parsons" && response.type === "parsons") {
        const view = await runCode(parsonsCode(response.order));
        outcome = view.failure
          ? { correct: false, note: "Python could not run, so only the exact order counted." }
          : { correct: !view.explanation && outputMatches(view.stdout, question.expectedOutput), view };
      } else if (question.type === "bug" && response.type === "bug") {
        const view = await runCode(response.code);
        if (view.failure) {
          setRunViews((all) => ({ ...all, [question.id]: view }));
          return; // not graded: let them try again once Python loads
        }
        const correct = !view.explanation && outputMatches(view.stdout, question.expectedOutput);
        setRunViews((all) => ({ ...all, [question.id]: view }));
        outcome = {
          correct,
          view,
          note: correct ? undefined : view.explanation ? "The code still stops with an error." : "It runs, but it does not print the right thing yet.",
        };
      } else {
        outcome = { correct: false };
      }
      setChecked((all) => ({ ...all, [question.id]: outcome }));
      window.setTimeout(() => feedbackRef.current?.focus(), 0);
    } finally {
      setChecking(false);
    }
  };

  const runBug = async () => {
    if (response.type !== "bug" || running) return;
    setRunning(true);
    try {
      const view = await runCode(response.code);
      setRunViews((all) => ({ ...all, [question.id]: view }));
    } finally {
      setRunning(false);
    }
  };

  const goNext = () => {
    if (index < total - 1) {
      moved.current = true;
      setIndex(index + 1);
    } else {
      finish(checked);
    }
  };

  const retake = () => {
    moved.current = true;
    setAttempt((value) => value + 1);
    setIndex(0);
    setResponses({});
    setChecked({});
    setRunViews({});
    setFinished(null);
  };

  const ready = settings.quizReadyPercent;

  if (finished) {
    const best = Math.max(saved?.best ?? 0, finished.percent);
    return (
      <section className="quiz quiz-results" data-testid="quiz-results">
        <h2 ref={resultRef} tabIndex={-1}>
          Your score
        </h2>
        <p className="quiz-score" data-testid="quiz-score" aria-live="polite">
          {finished.correct} of {total} right ({finished.percent}%)
        </p>
        {finished.percent >= ready ? (
          <p className="quiz-ready" data-testid="quiz-ready">
            <span aria-hidden="true">★</span> Ready! You know this well enough to move on.
          </p>
        ) : (
          <p className="quiz-not-ready">
            {ready}% or more earns the Ready badge. Look at the ones you missed, then try again if you like. You can
            also move on.
          </p>
        )}
        <p className="quiz-best" data-testid="quiz-best">
          Your best: {best}%
        </p>
        {form && gate ? (
          <p className="quiz-quick-check" data-testid="quiz-quick-check" data-passed={formPassed || testedOut ? "true" : "false"}>
            {formPassed || testedOut ? (
              <>
                <span aria-hidden="true">✓</span> <strong>You passed the Quick Check.</strong> This unit now counts as done.
              </>
            ) : gate.met ? (
              <>
                That is enough for the Quick Check. Finish{" "}
                <Link href={itemHref(unit.id, form.id)} data-testid="quiz-quick-check-tasks">
                  its tasks
                </Link>{" "}
                too, and this unit counts as done.
              </>
            ) : (
              `The Quick Check needs ${gate.needed} of these ${gate.total} right. Look at the ones you missed, then try again.`
            )}
          </p>
        ) : null}
        <ol className="quiz-review" data-testid="quiz-review">
          {questions.map((entry, at) => {
            const right = checked[entry.id]?.correct === true;
            return (
              <li key={entry.id} className={right ? "is-right" : "is-wrong"}>
                <span aria-hidden="true">{right ? "✓" : "✗"}</span>{" "}
                <span className="sr-only">{right ? "Right:" : "Missed:"}</span> Question {at + 1}.{" "}
                <Prose text={entry.q} glossary={glossary} inline />
              </li>
            );
          })}
        </ol>
        <div className="quiz-actions">
          <button type="button" onClick={retake} data-testid="quiz-retake">
            Try the quiz again
          </button>
          <Link className="course-button" href={nextHref} data-testid="quiz-next-item">
            Next
          </Link>
        </div>
      </section>
    );
  }

  const choices =
    question.type === "mc" ? question.choices : question.type === "predict" && question.choices?.length ? question.choices : null;

  return (
    <section className="quiz" data-testid="quiz">
      <div className="quiz-top">
        <p className="quiz-count" data-testid="quiz-count">
          Question {index + 1} of {total}
        </p>
        {saved && saved.attempts > 0 ? (
          <p className="quiz-best-small">
            Your best: {saved.best}%{saved.best >= ready ? " · Ready" : ""}
          </p>
        ) : null}
      </div>
      <ol className="quiz-dots" aria-label="Questions">
        {questions.map((entry, at) => {
          const state = checked[entry.id] ? (checked[entry.id].correct ? "right" : "wrong") : at === index ? "current" : "todo";
          return (
            <li key={entry.id} className={`quiz-dot is-${state}`} data-state={state}>
              {/* A mark as well as a colour, for students who can't tell green from pink. */}
              <span className="quiz-dot-mark" aria-hidden="true">
                {state === "right" ? "✓" : state === "wrong" ? "✗" : state === "current" ? "•" : ""}
              </span>
              <span className="sr-only">
                Question {at + 1}: {state === "right" ? "right" : state === "wrong" ? "missed" : state === "current" ? "now" : "not done"}
              </span>
            </li>
          );
        })}
      </ol>

      <article className="quiz-card" data-testid={`quiz-question-${question.id}`} data-type={question.type}>
        <p className="quiz-type">{TYPE_HINT[question.type]}</p>
        <h2 ref={headingRef} tabIndex={-1} className="quiz-question">
          <Prose text={question.q} glossary={glossary} inline />
        </h2>

        {question.type === "mc" && question.code ? <CodeBlock code={question.code} /> : null}
        {question.type === "predict" ? <CodeBlock code={question.code} /> : null}

        {choices ? (
          <ChoiceList
            question={question}
            choices={choices}
            chosen={response.type === "mc" || response.type === "predict" ? response.choice : null}
            locked={locked}
            output={question.type === "predict"}
            onChoose={(choice) =>
              setResponse(response.type === "predict" ? { ...response, choice } : { type: "mc", choice })
            }
          />
        ) : null}

        {question.type === "predict" && !choices && response.type === "predict" ? (
          <label className="quiz-typed">
            <span>Type what it prints, one line per line:</span>
            <textarea
              value={response.text}
              readOnly={locked}
              rows={Math.max(2, question.answer.split("\n").length + 1)}
              spellCheck={false}
              autoCapitalize="off"
              onChange={(event) => setResponse({ ...response, text: event.target.value })}
              data-testid="quiz-answer-input"
            />
          </label>
        ) : null}

        {question.type === "fill" && response.type === "fill" ? (
          <FillCode question={question} text={response.text} locked={locked} onChange={(text) => setResponse({ type: "fill", text })} />
        ) : null}

        {question.type === "parsons" && response.type === "parsons" ? (
          locked ? (
            <CodeBlock code={parsonsCode(response.order)} label="Your order" />
          ) : (
            <ParsonsBoard
              key={`${question.id}-${attempt}`}
              blocks={blocks}
              value={response.order}
              onChange={(order) => setResponse({ type: "parsons", order })}
              idPrefix={`quiz-${question.id}-${attempt}`}
            />
          )
        ) : null}

        {question.type === "bug" && response.type === "bug" ? (
          <div className="quiz-bug">
            {locked ? (
              <CodeBlock code={response.code} label="Your code" />
            ) : (
              <>
                <PythonEditor
                  key={`${question.id}-${attempt}`}
                  code={response.code}
                  onChange={(code) => setResponse({ type: "bug", code })}
                />
                <div className="quiz-bug-toolbar">
                  <button type="button" onClick={runBug} disabled={running || checking} data-testid="quiz-bug-run">
                    {running ? "Running…" : "Run"}
                  </button>
                  <button
                    type="button"
                    className="quiet-button"
                    onClick={() => setResponse({ type: "bug", code: question.code })}
                    data-testid="quiz-bug-reset"
                  >
                    Start over
                  </button>
                  {pythonStatus === "loading" || pythonStatus === "failed" ? (
                    <span className="python-status" data-testid="python-status">
                      {PYTHON_STATUS_TEXT[pythonStatus]}
                    </span>
                  ) : null}
                </div>
              </>
            )}
            <RunOutput view={runViews[question.id] ?? null} testId="quiz-bug-output" />
          </div>
        ) : null}

        <div ref={feedbackRef} tabIndex={-1} className="quiz-feedback-wrap" aria-live="polite">
          {result ? (
            <>
              <Feedback question={question} response={response} checked={result} glossary={glossary} />
              {question.type === "parsons" && result.view && !result.correct ? (
                <RunOutput view={result.view} label="Your order printed" />
              ) : null}
            </>
          ) : null}
        </div>

        <div className="quiz-actions">
          {index > 0 ? (
            <button
              type="button"
              className="quiet-button"
              onClick={() => {
                moved.current = true;
                setIndex(index - 1);
              }}
              data-testid="quiz-back"
            >
              Back
            </button>
          ) : null}
          {locked ? (
            <button type="button" onClick={goNext} data-testid="quiz-next">
              {index < total - 1 ? "Next question" : "See my score"}
            </button>
          ) : (
            <button
              type="button"
              onClick={check}
              disabled={checking || !hasAnswer(response)}
              data-testid="quiz-check"
            >
              {checking ? "Checking…" : "Check"}
            </button>
          )}
        </div>
      </article>
    </section>
  );
}

/** The quiz page: heading, then one question at a time. */
export function QuizPlayer(props: ItemPageProps<QuizItem>) {
  const { item } = props;
  return (
    <div className="course-reading">
      <header className="item-header">
        <KindBadge kind="quiz" />
        <h1>{item.title}</h1>
        {item.summary ? <Prose text={item.summary} glossary={props.glossary} className="item-summary" /> : null}
        <p className="item-meta">
          {item.questions.length} questions{item.minutes ? ` · about ${item.minutes} min` : ""} · No timer. Retake it as
          often as you like.
        </p>
      </header>
      <QuizRun {...props} />
    </div>
  );
}
