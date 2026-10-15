"use client";

import { useEffect, useMemo, useState } from "react";
import { emberkeepModule } from "../lib/lesson/emberkeep";
import {
  commitProgress,
  gradeRun,
  initialTheater,
  nextTheaterState,
  starterFor,
  visibleLessons,
  type FailedCheck,
} from "../lib/lesson/progression";
import { moduleSchema, type Module } from "../lib/lesson/schema";
import { pythonAdapter, PythonTimeoutError, whenPythonReady } from "../lib/languages/python";
import type { Explanation } from "../lib/languages/types";
import type { TheaterState } from "../lib/stage/bridge";
import { ConsolePanel } from "./ConsolePanel";
import { PythonEditor } from "./PythonEditor";
import { Theater } from "./Theater";

const PREVIEW_STORAGE_KEY = "emberkeep-preview";
const STUDENT_STORAGE_KEY = "emberkeep-student";

type StudentSession = {
  id: string;
  displayName: string;
  joinCode: string;
  classroomId: string;
};

type StoredProgress = {
  moduleId: string;
  lessonId: string;
  beatId: string;
  latestCode: string;
  status: "in_progress" | "completed";
};

function lessonsFor(module: Module, preview: boolean) {
  return preview ? module.lessons : visibleLessons(module);
}

export function Player() {
  const [preview, setPreview] = useState(false);
  const [lessonModule, setLessonModule] = useState<Module>(emberkeepModule);
  const [lessonIndex, setLessonIndex] = useState(0);
  const [beatIndex, setBeatIndex] = useState(0);
  const [code, setCode] = useState(starterFor(emberkeepModule.lessons[0].beats[0]));
  const [theater, setTheater] = useState<TheaterState>(initialTheater(emberkeepModule.lessons[0].beats[0]));
  const [output, setOutput] = useState("");
  const [explainer, setExplainer] = useState<Explanation | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [failedChecks, setFailedChecks] = useState<FailedCheck[]>([]);
  const [passed, setPassed] = useState(false);
  const [finished, setFinished] = useState(false);
  const [pythonReady, setPythonReady] = useState(false);
  const [running, setRunning] = useState(false);
  const [student, setStudent] = useState<StudentSession | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [joinError, setJoinError] = useState("");
  const [joining, setJoining] = useState(false);

  const lessons = useMemo(() => lessonsFor(lessonModule, preview), [lessonModule, preview]);
  const lesson = lessons[lessonIndex];
  const beat = lesson?.beats[beatIndex];
  const continueUnlocked = Boolean(beat) && !finished && (!beat.activity || passed);

  useEffect(() => {
    let cancelled = false;
    whenPythonReady()
      .then(() => {
        if (!cancelled) setPythonReady(true);
      })
      .catch(() => {
        if (!cancelled) {
          setExplainer({
            title: "Python could not start",
            hint: "The player could not load Python in this browser. Refresh the page and try again.",
            raw: "",
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const isPreview = params.get("preview") === "1";
    if (isPreview) {
      setPreview(true);
      const raw = sessionStorage.getItem(PREVIEW_STORAGE_KEY);
      if (!raw) return;
      try {
        const parsed = moduleSchema.safeParse(JSON.parse(raw));
        if (!parsed.success) return;
        const first = parsed.data.lessons[0]?.beats[0];
        setLessonModule(parsed.data);
        setLessonIndex(0);
        setBeatIndex(0);
        setFinished(false);
        setPassed(false);
        if (first) {
          setCode(starterFor(first));
          setTheater(initialTheater(first));
        }
      } catch {
        setJoinError("The preview draft could not be read.");
      }
      return;
    }

    const saved = localStorage.getItem(STUDENT_STORAGE_KEY);
    if (!saved) return;
    try {
      const record = JSON.parse(saved) as { displayName?: string; joinCode?: string };
      if (record.displayName && record.joinCode) {
        void joinClass(record.displayName, record.joinCode, emberkeepModule, false);
      }
    } catch {
      localStorage.removeItem(STUDENT_STORAGE_KEY);
    }
  }, []);

  function resetRunState() {
    setOutput("");
    setExplainer(null);
    setFeedback(null);
    setFailedChecks([]);
    setPassed(false);
  }

  function applyProgress(progress: StoredProgress, module: Module, isPreview: boolean) {
    if (progress.moduleId !== module.id) return;
    const visible = lessonsFor(module, isPreview);
    const nextLesson = visible.findIndex((item) => item.id === progress.lessonId);
    if (nextLesson < 0) return;
    const nextBeat = visible[nextLesson].beats.findIndex((item) => item.id === progress.beatId);
    if (nextBeat < 0) return;
    const beatToShow = visible[nextLesson].beats[nextBeat];
    setLessonIndex(nextLesson);
    setBeatIndex(nextBeat);
    setCode(progress.latestCode || starterFor(beatToShow));
    setTheater(initialTheater(beatToShow));
    setFinished(progress.status === "completed");
    resetRunState();
  }

  async function joinClass(name: string, code: string, module: Module, isPreview: boolean) {
    setJoining(true);
    setJoinError("");
    try {
      const response = await fetch("/api/classroom/join", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ displayName: name, joinCode: code }),
      });
      const body = (await response.json()) as {
        error?: string;
        student?: { id: string; displayName: string; classroomId: string };
        progress?: StoredProgress | null;
      };
      if (!response.ok || !body.student) {
        setJoinError(body.error ?? "Could not join that classroom.");
        return;
      }
      const session = {
        id: body.student.id,
        displayName: body.student.displayName,
        classroomId: body.student.classroomId,
        joinCode: code.trim(),
      };
      setStudent(session);
      localStorage.setItem(
        STUDENT_STORAGE_KEY,
        JSON.stringify({ displayName: session.displayName, joinCode: session.joinCode }),
      );
      if (body.progress) applyProgress(body.progress, module, isPreview);
    } catch {
      setJoinError("Could not join that classroom.");
    } finally {
      setJoining(false);
    }
  }

  async function persist(args: {
    status: "in_progress" | "completed";
    lessonId: string;
    beatId: string;
    latestCode: string;
  }) {
    if (!student) return;
    await commitProgress(preview, async () => {
      await fetch("/api/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          studentId: student.id,
          moduleId: lessonModule.id,
          lessonId: args.lessonId,
          beatId: args.beatId,
          status: args.status,
          latestCode: args.latestCode,
          preview,
        }),
      });
    });
  }

  async function onFormat() {
    try {
      const formatted = await pythonAdapter.format(code);
      setCode(formatted);
      setExplainer(null);
    } catch (error) {
      setExplainer({
        title: "Could not format",
        hint: "Ruff could not format this yet. Fix any syntax error, then try again.",
        raw: error instanceof Error ? error.message : String(error),
      });
    }
  }

  async function onRun() {
    if (!beat || running) return;
    setRunning(true);
    setExplainer(null);
    setFeedback(null);
    setFailedChecks([]);
    setPassed(false);
    let source = code;
    try {
      const formatted = await pythonAdapter.format(code);
      source = formatted;
      if (formatted !== code) setCode(formatted);
    } catch {
      source = code;
    }
    try {
      const result = await pythonAdapter.run({
        code: source,
        checks: beat.activity?.checks ?? [],
      });
      const printed = [result.stdout, result.stderr].filter((part) => part.trim().length > 0).join("");
      setOutput(printed);
      if (!result.ok) setExplainer(pythonAdapter.explain(result.traceback));
      const grade = gradeRun(beat, result);
      setFeedback(grade.feedback);
      setFailedChecks(grade.failedChecks);
      setPassed(Boolean(beat.activity) && grade.canContinue);
      setTheater((current) => {
        const next = nextTheaterState(beat, result.stageEvents);
        return { ...next, flareToken: current.flareToken + next.flareToken };
      });
      await persist({
        status: "in_progress",
        lessonId: lesson.id,
        beatId: beat.id,
        latestCode: source,
      });
    } catch (error) {
      if (error instanceof PythonTimeoutError) {
        setExplainer({
          title: "Time limit",
          hint: "The program ran too long and was stopped. Check for an infinite loop.",
          raw: "",
        });
        setPythonReady(false);
        whenPythonReady()
          .then(() => setPythonReady(true))
          .catch(() => setPythonReady(false));
      } else {
        setExplainer({
          title: "Python could not start",
          hint: "The player could not run this program. Try again in a moment.",
          raw: error instanceof Error ? error.message : String(error),
        });
      }
    } finally {
      setRunning(false);
    }
  }

  async function onContinue() {
    if (!lesson || !beat) return;
    const nextBeatIndex = beatIndex + 1;
    if (nextBeatIndex < lesson.beats.length) {
      const nextBeat = lesson.beats[nextBeatIndex];
      await persist({
        status: "in_progress",
        lessonId: lesson.id,
        beatId: nextBeat.id,
        latestCode: starterFor(nextBeat),
      });
      setBeatIndex(nextBeatIndex);
      setCode(starterFor(nextBeat));
      setTheater(initialTheater(nextBeat));
      setFinished(false);
      resetRunState();
      return;
    }
    await persist({
      status: "completed",
      lessonId: lesson.id,
      beatId: beat.id,
      latestCode: code,
    });
    const nextLessonIndex = lessonIndex + 1;
    if (nextLessonIndex < lessons.length) {
      const nextLesson = lessons[nextLessonIndex];
      const nextBeat = nextLesson.beats[0];
      setLessonIndex(nextLessonIndex);
      setBeatIndex(0);
      setCode(starterFor(nextBeat));
      setTheater(initialTheater(nextBeat));
      resetRunState();
      await persist({
        status: "in_progress",
        lessonId: nextLesson.id,
        beatId: nextBeat.id,
        latestCode: starterFor(nextBeat),
      });
      return;
    }
    setFinished(true);
    setPassed(false);
  }

  if (!lesson || !beat) {
    return (
      <main className="column">
        <p>This module has no published lesson yet.</p>
      </main>
    );
  }

  return (
    <main className="column">
      {preview ? (
        <p className="banner" data-testid="preview-banner">
          Preview. This pass is not saved to a classroom.
        </p>
      ) : null}
      {finished ? (
        <p className="banner" data-testid="lesson-complete">
          The lesson is complete.
        </p>
      ) : null}
      <section className="join-bar" aria-label="Classroom">
        {student ? (
          <p data-testid="join-status">Joined as {student.displayName}</p>
        ) : (
          <form
            data-testid="join-form"
            onSubmit={(event) => {
              event.preventDefault();
              void joinClass(displayName, joinCode, lessonModule, preview);
            }}
          >
            <label>
              Display name
              <input
                aria-label="Display name"
                value={displayName}
                onChange={(event) => setDisplayName(event.target.value)}
              />
            </label>
            <label>
              Join code
              <input
                aria-label="Join code"
                value={joinCode}
                onChange={(event) => setJoinCode(event.target.value)}
              />
            </label>
            <button type="submit" disabled={joining}>
              {joining ? "Joining…" : "Join class"}
            </button>
          </form>
        )}
        {joinError ? (
          <p className="join-error" data-testid="join-error" role="alert">
            {joinError}
          </p>
        ) : null}
      </section>

      <Theater
        scene={beat.scene}
        caption={theater.caption}
        flareToken={theater.flareToken}
        focusedImageId={theater.focusedImageId}
      />

      <section className="instructions" data-testid="instructions">
        <h1>{lesson.title}</h1>
        <p className="beat-count">
          Beat {beatIndex + 1} of {lesson.beats.length}
        </p>
        <p>{beat.instructions}</p>
      </section>

      <section className="code-panel">
        <div className="toolbar">
          <button type="button" data-testid="format" onClick={() => void onFormat()} disabled={running}>
            Format
          </button>
          <button
            type="button"
            data-testid="run"
            onClick={() => void onRun()}
            disabled={!pythonReady || running}
          >
            {running ? "Running…" : pythonReady ? "Run" : "Loading Python…"}
          </button>
          <span data-testid="python-status" className="python-status">
            {pythonReady ? "Python is ready" : "Python is loading"}
          </span>
        </div>
        <PythonEditor code={code} onChange={setCode} />
        <ConsolePanel
          output={output}
          explainer={explainer}
          feedback={feedback}
          failedChecks={failedChecks}
        />
      </section>

      {continueUnlocked ? (
        <button type="button" className="continue" data-testid="continue" onClick={() => void onContinue()}>
          Continue
        </button>
      ) : null}
    </main>
  );
}
