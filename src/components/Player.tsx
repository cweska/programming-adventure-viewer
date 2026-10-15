"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { emberkeepModule } from "../lib/lesson/emberkeep";
import {
  canGoBack,
  canGoForward,
  createPartNavigation,
  goBack,
  goForward,
  navigationFromProgress,
  partLabel,
  recordPass,
  setPartCode,
  type PartNavigation,
} from "../lib/lesson/navigation";
import {
  commitProgress,
  gradeRun,
  initialTheater,
  nextTheaterState,
  type FailedCheck,
} from "../lib/lesson/progression";
import { moduleSchema, type Beat, type Module } from "../lib/lesson/schema";
import { formatForTrigger, type FormatTrigger } from "../lib/languages/python/format-policy";
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
  return preview ? module.lessons : module.lessons.filter((lesson) => lesson.published);
}

export function Player() {
  const initialLesson = emberkeepModule.lessons[0];
  const initialNav = createPartNavigation(initialLesson.beats);
  const [preview, setPreview] = useState(false);
  const [lessonModule, setLessonModule] = useState<Module>(emberkeepModule);
  const [lessonIndex, setLessonIndex] = useState(0);
  const [nav, setNav] = useState<PartNavigation>(initialNav);
  const [code, setCode] = useState(initialNav.code[0] ?? "");
  const [theater, setTheater] = useState<TheaterState>(initialTheater(initialLesson.beats[0]));
  const [output, setOutput] = useState("");
  const [explainer, setExplainer] = useState<Explanation | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [failedChecks, setFailedChecks] = useState<FailedCheck[]>([]);
  const [lessonCompleted, setLessonCompleted] = useState(false);
  const [pythonReady, setPythonReady] = useState(false);
  const [running, setRunning] = useState(false);
  const [student, setStudent] = useState<StudentSession | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [joinError, setJoinError] = useState("");
  const [joining, setJoining] = useState(false);

  const navRef = useRef(nav);
  const indexRef = useRef(0);
  const codeRef = useRef(initialNav.code[0] ?? "");
  const lessonIdRef = useRef(initialLesson.id);
  const frontierRef = useRef(0);
  const previewRef = useRef(false);
  const studentRef = useRef<StudentSession | null>(null);
  const moduleRef = useRef(lessonModule);

  const lessons = useMemo(() => lessonsFor(lessonModule, preview), [lessonModule, preview]);
  const lesson = lessons[lessonIndex];
  const beat = lesson?.beats[nav.index];
  const atEnd = Boolean(lesson) && nav.index >= lesson.beats.length - 1;
  const continueUnlocked = Boolean(beat) && !(lessonCompleted && atEnd) && (!beat.activity || nav.passed[nav.index] === true);

  function writeNavigation(next: PartNavigation) {
    navRef.current = next;
    setNav(next);
  }

  function openIndex(next: PartNavigation, beats: Beat[], lessonId: string) {
    const part = beats[next.index];
    if (!part) return;
    lessonIdRef.current = lessonId;
    indexRef.current = next.index;
    const source = next.code[next.index] ?? "";
    codeRef.current = source;
    writeNavigation(next);
    setCode(source);
    setTheater(initialTheater(part));
    setOutput("");
    setExplainer(null);
    setFeedback(null);
    setFailedChecks([]);
    void formatPart("load", next.index, source, lessonId);
  }

  async function formatPart(trigger: FormatTrigger, index: number, source: string, lessonId: string): Promise<string> {
    const snapshot = source;
    let formatted = source;
    try {
      formatted = await formatForTrigger(trigger, source, (value) => pythonAdapter.format(value));
    } catch {
      formatted = source;
    }
    if (lessonIdRef.current !== lessonId) return formatted;
    if (indexRef.current === index && codeRef.current !== snapshot) return codeRef.current;
    writeNavigation(setPartCode(navRef.current, index, formatted));
    if (indexRef.current === index) {
      codeRef.current = formatted;
      setCode(formatted);
    }
    return formatted;
  }

  function onCodeChange(value: string) {
    codeRef.current = value;
    setCode(value);
    writeNavigation(setPartCode(navRef.current, indexRef.current, value));
  }

  function onEditorBlur() {
    void formatPart("blur", indexRef.current, codeRef.current, lessonIdRef.current);
  }

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
    void formatPart("load", 0, codeRef.current, lessonIdRef.current);
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const isPreview = params.get("preview") === "1";
    previewRef.current = isPreview;
    if (isPreview) {
      setPreview(true);
      const raw = sessionStorage.getItem(PREVIEW_STORAGE_KEY);
      if (!raw) return;
      try {
        const parsed = moduleSchema.safeParse(JSON.parse(raw));
        if (!parsed.success || !parsed.data.lessons[0]) return;
        const beats = parsed.data.lessons[0].beats;
        setLessonModule(parsed.data);
        moduleRef.current = parsed.data;
        setLessonIndex(0);
        setLessonCompleted(false);
        frontierRef.current = 0;
        openIndex(createPartNavigation(beats), beats, parsed.data.lessons[0].id);
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

  function applyProgress(progress: StoredProgress, module: Module, isPreview: boolean) {
    if (progress.moduleId !== module.id) return;
    const visible = lessonsFor(module, isPreview);
    const nextLesson = visible.findIndex((item) => item.id === progress.lessonId);
    if (nextLesson < 0) return;
    const beats = visible[nextLesson].beats;
    const nextIndex = beats.findIndex((item) => item.id === progress.beatId);
    if (nextIndex < 0) return;
    const completed = progress.status === "completed";
    const next = navigationFromProgress(beats, nextIndex, progress.latestCode, completed);
    setLessonIndex(nextLesson);
    setLessonCompleted(completed);
    frontierRef.current = nextIndex;
    openIndex(next, beats, visible[nextLesson].id);
  }

  async function joinClass(name: string, codeValue: string, module: Module, isPreview: boolean) {
    setJoining(true);
    setJoinError("");
    try {
      const response = await fetch("/api/classroom/join", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ displayName: name, joinCode: codeValue }),
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
        joinCode: codeValue.trim(),
      };
      studentRef.current = session;
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
    index: number;
  }) {
    const currentStudent = studentRef.current;
    if (!currentStudent) return;
    if (args.status !== "completed" && args.index < frontierRef.current) return;
    frontierRef.current = Math.max(frontierRef.current, args.index);
    await commitProgress(previewRef.current, async () => {
      await fetch("/api/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          studentId: currentStudent.id,
          moduleId: moduleRef.current.id,
          lessonId: args.lessonId,
          beatId: args.beatId,
          status: args.status,
          latestCode: args.latestCode,
          preview: previewRef.current,
        }),
      });
    });
  }

  async function onRun() {
    const currentLesson = lessons[lessonIndex];
    const current = navRef.current;
    const part = currentLesson?.beats[current.index];
    if (!currentLesson || !part || running) return;
    setRunning(true);
    setExplainer(null);
    setFeedback(null);
    setFailedChecks([]);
    const source = await formatPart("run", current.index, codeRef.current, currentLesson.id);
    try {
      const result = await pythonAdapter.run({
        code: source,
        checks: part.activity?.checks ?? [],
      });
      const printed = [result.stdout, result.stderr].filter((chunk) => chunk.trim().length > 0).join("");
      setOutput(printed);
      if (!result.ok) setExplainer(pythonAdapter.explain(result.traceback));
      const grade = gradeRun(part, result);
      setFeedback(grade.feedback);
      setFailedChecks(grade.failedChecks);
      if (part.activity && grade.canContinue) {
        writeNavigation(recordPass(navRef.current, currentLesson.beats));
      }
      setTheater((previous) => {
        const next = nextTheaterState(part, result.stageEvents);
        return { ...next, flareToken: previous.flareToken + next.flareToken };
      });
      await persist({
        status: "in_progress",
        lessonId: currentLesson.id,
        beatId: part.id,
        latestCode: source,
        index: current.index,
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

  function onBack() {
    if (!lesson) return;
    const next = goBack(navRef.current);
    if (next === navRef.current) return;
    openIndex(next, lesson.beats, lesson.id);
  }

  function onForward() {
    if (!lesson) return;
    const next = goForward(navRef.current, lesson.beats);
    if (next === navRef.current) return;
    openIndex(next, lesson.beats, lesson.id);
  }

  async function onContinue() {
    if (!lesson || !beat) return;
    if (beat.activity && navRef.current.passed[navRef.current.index] !== true) return;
    const nextIndex = navRef.current.index + 1;
    if (nextIndex < lesson.beats.length) {
      const next = goForward(navRef.current, lesson.beats);
      const latestCode = next.code[next.index] ?? "";
      await persist({
        status: "in_progress",
        lessonId: lesson.id,
        beatId: lesson.beats[next.index].id,
        latestCode,
        index: next.index,
      });
      openIndex(next, lesson.beats, lesson.id);
      return;
    }
    setLessonCompleted(true);
    await persist({
      status: "completed",
      lessonId: lesson.id,
      beatId: beat.id,
      latestCode: codeRef.current,
      index: navRef.current.index,
    });
    const nextLessonIndex = lessonIndex + 1;
    if (nextLessonIndex < lessons.length) {
      const nextLesson = lessons[nextLessonIndex];
      setLessonIndex(nextLessonIndex);
      setLessonCompleted(false);
      frontierRef.current = 0;
      openIndex(createPartNavigation(nextLesson.beats), nextLesson.beats, nextLesson.id);
      await persist({
        status: "in_progress",
        lessonId: nextLesson.id,
        beatId: nextLesson.beats[0].id,
        latestCode: navRef.current.code[0] ?? "",
        index: 0,
      });
    }
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
      {lessonCompleted && atEnd ? (
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
              previewRef.current = preview;
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
        <div className="part-nav">
          <button type="button" data-testid="back" onClick={onBack} disabled={!canGoBack(nav)}>
            Back
          </button>
          <p className="part-count" data-testid="part-label">
            {partLabel(nav.index, lesson.beats.length)}
          </p>
          <button
            type="button"
            data-testid="forward"
            onClick={onForward}
            disabled={!canGoForward(nav, lesson.beats.length)}
          >
            Forward
          </button>
        </div>
        <p>{beat.instructions}</p>
      </section>

      <section className="code-panel">
        <div className="toolbar">
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
        <PythonEditor code={code} onChange={onCodeChange} onBlur={onEditorBlur} />
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
