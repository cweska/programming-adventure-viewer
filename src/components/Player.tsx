"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { mergeFeatures } from "../lib/game/state";
import {
  browserStorage,
  isAhead,
  readSave,
  restoreSave,
  saveFrom,
  writeSave,
  type PlayPosition,
  type PlaySave,
} from "../lib/lesson/autosave";
import { emberkeepModule } from "../lib/lesson/emberkeep";
import { findModule } from "../lib/lesson/modules";
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
  starterFor,
  type FailedCheck,
} from "../lib/lesson/progression";
import {
  moduleSchema,
  passesOnGoal,
  requiresPass,
  showsEditor,
  type Beat,
  type Module,
  type SkillCheck,
} from "../lib/lesson/schema";
import { activitySetup, castCode, skillRollCode } from "../lib/lesson/setup";
import { formatForTrigger, type FormatTrigger } from "../lib/languages/python/format-policy";
import {
  joinClassroomInBrowser,
  saveProgressInBrowser,
} from "../lib/classroom/local-store";
import { pythonAdapter, PythonTimeoutError, whenPythonReady } from "../lib/languages/python";
import type { Explanation, LiveSession, RunResult } from "../lib/languages/types";
import { isStaticExport } from "../lib/site";
import { conversationEvents, gameEvents, stageMoves, type StageEvent, type TheaterState } from "../lib/stage/bridge";
import { ConsolePanel } from "./ConsolePanel";
import { ConversationScene, type ConversationScript } from "./ConversationScene";
import { GameBoard, type BoardScript } from "./game/GameBoard";
import { PartyPanelScene, type ManaEvent, type ManaScript } from "./PartyPanelScene";
import { PythonEditor } from "./PythonEditor";
import { SkillCheckScene, type RollOutcome } from "./SkillCheckScene";
import { SpellBookScene } from "./SpellBookScene";
import { Theater } from "./Theater";

const PREVIEW_STORAGE_KEY = "emberkeep-preview";
const STUDENT_STORAGE_KEY = "emberkeep-student";
const PROMPTS_STORAGE_PREFIX = "emberkeep-prompts:";
const PASSED_STORAGE_PREFIX = "emberkeep-passed:";
const AUTOSAVE_DELAY_MS = 400;
const CODE_SYNC_DELAY_MS = 3000;

type SaveStatus = "idle" | "saved" | "failed";

type PendingCode = {
  key: string;
  index: number;
  signature: string;
  body: { studentId: string; moduleId: string; lessonId: string; beatId: string; code: string };
};

function codeSignature(studentId: string, lessonId: string, beatId: string, code: string): string {
  return [studentId, lessonId, beatId, code].join("\u0000");
}

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

export function Player({ moduleId, draft = false }: { moduleId?: string; draft?: boolean }) {
  const startModule = (moduleId ? findModule(moduleId) : undefined) ?? emberkeepModule;
  const initialLesson = startModule.lessons[0];
  const initialNav = createPartNavigation(initialLesson.beats);
  const [preview, setPreview] = useState(draft);
  const [lessonModule, setLessonModule] = useState<Module>(startModule);
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
  const [confirmingReset, setConfirmingReset] = useState(false);
  const [student, setStudent] = useState<StudentSession | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [joinError, setJoinError] = useState("");
  const [joining, setJoining] = useState(false);
  const [script, setScript] = useState<BoardScript | null>(null);
  const [conversationScript, setConversationScript] = useState<ConversationScript | null>(null);
  const [checksPassed, setChecksPassed] = useState<Record<string, boolean>>({});
  const [prompts, setPrompts] = useState<Record<string, string>>({});
  const [manaScript, setManaScript] = useState<ManaScript | null>(null);
  const [autosaveReady, setAutosaveReady] = useState(false);
  const [saveStatus, setSaveStatus] = useState<SaveStatus>("idle");
  const [resumed, setResumed] = useState(false);

  const navRef = useRef(nav);
  const completedRef = useRef(false);
  const restoredFromSaveRef = useRef(false);
  const pendingSaveRef = useRef<PlaySave | null>(null);
  const pendingCodeRef = useRef<PendingCode | null>(null);
  const lastCodeSyncRef = useRef("");
  const typedRef = useRef(false);
  const indexRef = useRef(0);
  const codeRef = useRef(initialNav.code[0] ?? "");
  const lessonIdRef = useRef(initialLesson.id);
  const frontierRef = useRef(0);
  const previewRef = useRef(draft);
  const studentRef = useRef<StudentSession | null>(null);
  const moduleRef = useRef(lessonModule);
  const passedCodeRef = useRef<Record<string, string>>({});
  const liveRef = useRef<{ key: string; session: LiveSession } | null>(null);

  const lessons = useMemo(() => lessonsFor(lessonModule, preview), [lessonModule, preview]);
  const lesson = lessons[lessonIndex];
  const beat = lesson?.beats[nav.index];
  const atEnd = Boolean(lesson) && nav.index >= lesson.beats.length - 1;
  const partPassed = nav.passed[nav.index] === true;
  const continueUnlocked = Boolean(beat) && !(lessonCompleted && atEnd) && (!requiresPass(beat) || partPassed);
  const partKey = lesson && beat ? `${lesson.id}/${beat.id}` : "";
  const unlocked = partPassed || checksPassed[partKey] === true;
  const partFeatures = beat
    ? mergeFeatures(beat.board?.features ?? [], unlocked ? (beat.activity?.unlocks ?? []) : [])
    : [];

  function writeNavigation(next: PartNavigation) {
    navRef.current = next;
    setNav(next);
  }

  function writeCompleted(value: boolean) {
    completedRef.current = value;
    setLessonCompleted(value);
  }

  function openIndex(next: PartNavigation, beats: Beat[], lessonId: string) {
    const part = beats[next.index];
    if (!part) return;
    setResumed(false);
    typedRef.current = false;
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
    setScript(null);
    setConversationScript(null);
    setManaScript(null);
    setConfirmingReset(false);
    endLiveSession();
    void formatPart("load", next.index, source, lessonId);
  }

  function endLiveSession() {
    liveRef.current?.session.end();
    liveRef.current = null;
  }

  function rememberPassedCode(beatId: string, source: string) {
    passedCodeRef.current = { ...passedCodeRef.current, [beatId]: source };
    try {
      localStorage.setItem(`${PASSED_STORAGE_PREFIX}${moduleRef.current.id}`, JSON.stringify(passedCodeRef.current));
    } catch {
      // Without storage, later parts fall back to the answer key that ships with them.
    }
  }

  function explainFailure(error: unknown) {
    if (error instanceof PythonTimeoutError) {
      liveRef.current = null;
      setExplainer({
        title: "Time limit",
        hint: "The program ran too long and was stopped. Check for an infinite loop.",
        raw: "",
      });
      setPythonReady(false);
      whenPythonReady()
        .then(() => setPythonReady(true))
        .catch(() => setPythonReady(false));
      return;
    }
    setExplainer({
      title: "Python could not start",
      hint: "The player could not run this program. Try again in a moment.",
      raw: error instanceof Error ? error.message : String(error),
    });
  }

  async function startLiveSession(key: string, setup: string, source: string) {
    try {
      const { session, result } = await pythonAdapter.startSession({ setup, code: source });
      const currentLesson = lessons[lessonIndex];
      const currentPart = currentLesson?.beats[navRef.current.index];
      const stillHere = currentLesson && currentPart && `${currentLesson.id}/${currentPart.id}` === key;
      if (!result.ok || !stillHere) {
        session.end();
        return;
      }
      liveRef.current?.session.end();
      liveRef.current = { key, session };
    } catch (error) {
      explainFailure(error);
    }
  }

  async function callLive(code: string): Promise<RunResult | "no-session" | "error"> {
    const live = liveRef.current;
    if (!live || live.key !== partKey) return "no-session";
    try {
      const result = await live.session.call(code);
      const printed = [result.stdout, result.stderr].filter((chunk) => chunk.trim().length > 0).join("");
      if (printed) setOutput((previous) => previous + printed);
      if (!result.ok) {
        setExplainer(pythonAdapter.explain(result.traceback));
        return "error";
      }
      return result;
    } catch (error) {
      explainFailure(error);
      return "error";
    }
  }

  async function rollSkill(option: SkillCheck["options"][number]): Promise<RollOutcome> {
    const result = await callLive(skillRollCode(option));
    if (result === "no-session") return { kind: "no-session" };
    if (result === "error") return { kind: "error" };
    const roll = result.stageEvents.find((event) => event.type === "roll");
    return roll?.type === "roll"
      ? { kind: "roll", roll: { roll: roll.roll, success: roll.success, required: roll.required } }
      : { kind: "error" };
  }

  async function castFor(index: number, spell: string): Promise<StageEvent[] | null> {
    const result = await callLive(castCode(index, spell));
    if (result === "no-session") return null;
    if (result === "error") return [];
    return result.stageEvents;
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
    // The part's code changed while formatting (for example, a saved lesson was restored), so keep the newer code.
    if (navRef.current.code[index] !== snapshot) return formatted;
    writeNavigation(setPartCode(navRef.current, index, formatted));
    if (indexRef.current === index) {
      codeRef.current = formatted;
      setCode(formatted);
    }
    return formatted;
  }

  function onCodeChange(value: string) {
    typedRef.current = true;
    codeRef.current = value;
    setCode(value);
    writeNavigation(setPartCode(navRef.current, indexRef.current, value));
  }

  function resetCode() {
    const currentLesson = lessons[lessonIndex];
    const index = navRef.current.index;
    const part = currentLesson?.beats[index];
    setConfirmingReset(false);
    if (!currentLesson || !part || running) return;
    const starter = starterFor(part);
    onCodeChange(starter);
    setOutput("");
    setExplainer(null);
    setFeedback(null);
    setFailedChecks([]);
    void formatPart("load", index, starter, currentLesson.id);
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
    try {
      const saved = localStorage.getItem(`${PROMPTS_STORAGE_PREFIX}${moduleRef.current.id}`);
      if (saved) setPrompts(JSON.parse(saved) as Record<string, string>);
    } catch {
      // Remembered prompts are a convenience; the scene works without them.
    }
    try {
      const passed = localStorage.getItem(`${PASSED_STORAGE_PREFIX}${moduleRef.current.id}`);
      if (passed) passedCodeRef.current = JSON.parse(passed) as Record<string, string>;
    } catch {
      passedCodeRef.current = {};
    }
    return () => {
      liveRef.current?.session.end();
      liveRef.current = null;
    };
  }, []);

  function rememberPrompt(beatId: string, text: string) {
    setPrompts((previous) => {
      const next = { ...previous, [beatId]: text };
      try {
        localStorage.setItem(`${PROMPTS_STORAGE_PREFIX}${moduleRef.current.id}`, JSON.stringify(next));
      } catch {
        // Storage can be unavailable; the prompt still shows for this visit.
      }
      return next;
    });
  }

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const isPreview = draft || params.get("preview") === "1";
    previewRef.current = isPreview;
    if (isPreview) {
      setPreview(true);
      if (!draft) return;
      const raw = sessionStorage.getItem(PREVIEW_STORAGE_KEY);
      if (!raw) return;
      try {
        const parsed = moduleSchema.safeParse(JSON.parse(raw));
        if (!parsed.success || !parsed.data.lessons[0]) return;
        const beats = parsed.data.lessons[0].beats;
        setLessonModule(parsed.data);
        moduleRef.current = parsed.data;
        setLessonIndex(0);
        writeCompleted(false);
        frontierRef.current = 0;
        openIndex(createPartNavigation(beats), beats, parsed.data.lessons[0].id);
      } catch {
        setJoinError("The preview draft could not be read.");
      }
      return;
    }

    restoreLocalSave(moduleRef.current);
    // Saving starts only after the restore, so the fresh first render never overwrites a save.
    setAutosaveReady(true);

    const saved = localStorage.getItem(STUDENT_STORAGE_KEY);
    if (!saved) return;
    try {
      const record = JSON.parse(saved) as { displayName?: string; joinCode?: string };
      if (record.displayName && record.joinCode) {
        void joinClass(record.displayName, record.joinCode, moduleRef.current, false);
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
    writeCompleted(completed);
    frontierRef.current = nextIndex;
    openIndex(next, beats, visible[nextLesson].id);
    setResumed(true);
  }

  function restoreLocalSave(module: Module) {
    const storage = browserStorage();
    const save = storage ? readSave(storage, module.id) : null;
    if (!save) return;
    const visible = lessonsFor(module, false);
    const restored = restoreSave(save, visible);
    if (!restored) return;
    const restoredLesson = visible[restored.lessonIndex];
    setLessonIndex(restored.lessonIndex);
    writeCompleted(restored.completed);
    frontierRef.current = restored.frontier;
    openIndex(restored.nav, restoredLesson.beats, restoredLesson.id);
    restoredFromSaveRef.current = true;
    const pastStart =
      restored.lessonIndex > 0 || restored.nav.index > 0 || restored.completed || save.passed.length > 0;
    if (pastStart) setResumed(true);
  }

  // The furthest part this student reached in the lesson on screen.
  function frontierPart(module: Module, isPreview: boolean) {
    const current = lessonsFor(module, isPreview).find((item) => item.id === lessonIdRef.current);
    if (!current || current.beats.length === 0) return null;
    const index = Math.min(Math.max(navRef.current.index, frontierRef.current), current.beats.length - 1);
    return { lesson: current, index, part: current.beats[index] };
  }

  function localPosition(module: Module, isPreview: boolean): PlayPosition | null {
    const reached = frontierPart(module, isPreview);
    if (!reached) return null;
    return { lessonId: reached.lesson.id, beatId: reached.part.id, completed: completedRef.current };
  }

  // Tells the class how far this browser got, for play saved here before the student joined.
  function reportLocalProgress(module: Module, isPreview: boolean) {
    const reached = frontierPart(module, isPreview);
    if (!reached) return;
    void persist({
      status: completedRef.current ? "completed" : "in_progress",
      lessonId: reached.lesson.id,
      beatId: reached.part.id,
      latestCode: navRef.current.code[reached.index] ?? "",
      index: reached.index,
    });
  }

  async function joinClass(name: string, codeValue: string, module: Module, isPreview: boolean) {
    setJoining(true);
    setJoinError("");
    try {
      const body = isStaticExport
        ? joinClassroomInBrowser(name, codeValue, module.id)
        : await (async () => {
            const response = await fetch("/api/classroom/join", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ displayName: name, joinCode: codeValue, moduleId: module.id }),
            });
            const payload = (await response.json()) as {
              error?: string;
              student?: { id: string; displayName: string; classroomId: string };
              progress?: StoredProgress | null;
            };
            if (!response.ok) {
              return { error: payload.error ?? "Could not join that classroom." };
            }
            return payload;
          })();
      if (!body.student) {
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
      const progress = body.progress ?? null;
      const visible = lessonsFor(module, isPreview);
      const local = localPosition(module, isPreview);
      const start = visible[0]?.beats[0] ? { lessonId: visible[0].id, beatId: visible[0].beats[0].id } : null;
      // A save restored in this browser wins a tie: it has the code for every part, not just one.
      const keepLocal = restoredFromSaveRef.current;
      if (
        progress &&
        (!local || isAhead(progress, local, visible) || (!keepLocal && !isAhead(local, progress, visible)))
      ) {
        applyProgress(progress, module, isPreview);
      } else if (local) {
        // Played here before joining: bring the class report up to where the student is.
        const known = progress ?? start;
        if (!known || isAhead(local, known, visible)) reportLocalProgress(module, isPreview);
      }
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
    if (args.status !== "completed" && args.index < frontierRef.current) return;
    // The frontier moves for guests too, so it is in their save if they join a class later.
    frontierRef.current = Math.max(frontierRef.current, args.index);
    const currentStudent = studentRef.current;
    if (!currentStudent) return;
    const signature = codeSignature(currentStudent.id, args.lessonId, args.beatId, args.latestCode);
    const committed = await commitProgress(previewRef.current, async () => {
      if (isStaticExport) {
        saveProgressInBrowser({
          studentId: currentStudent.id,
          moduleId: moduleRef.current.id,
          lessonId: args.lessonId,
          beatId: args.beatId,
          status: args.status,
          latestCode: args.latestCode,
        });
        return;
      }
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
    if (committed) lastCodeSyncRef.current = signature;
  }

  function flushSave() {
    const save = pendingSaveRef.current;
    if (!save) return;
    pendingSaveRef.current = null;
    const storage = browserStorage();
    setSaveStatus(storage && writeSave(storage, save) ? "saved" : "failed");
  }

  function flushCode() {
    const pending = pendingCodeRef.current;
    if (!pending) return;
    pendingCodeRef.current = null;
    // The class keeps code for one part per lesson: the furthest. Code from a part left behind would move it back.
    if (pending.index < frontierRef.current) return;
    lastCodeSyncRef.current = pending.signature;
    fetch("/api/progress/code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(pending.body),
      keepalive: true,
    }).catch(() => {
      if (lastCodeSyncRef.current === pending.signature) lastCodeSyncRef.current = "";
    });
  }

  useEffect(() => {
    if (!autosaveReady || preview || !lesson) return;
    pendingSaveRef.current = saveFrom({
      moduleId: lessonModule.id,
      lesson,
      nav,
      completed: lessonCompleted,
      frontier: frontierRef.current,
    });
    const timer = window.setTimeout(flushSave, AUTOSAVE_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, [autosaveReady, preview, lessonModule, lesson, nav, lessonCompleted]);

  useEffect(() => {
    const key = lesson && beat ? `${lesson.id}/${beat.id}` : "";
    if (pendingCodeRef.current && pendingCodeRef.current.key !== key) flushCode();
    if (isStaticExport || preview || !student || !lesson || !beat) return;
    // Only the student's own edits are sent; the class already has the part's starting code.
    if (!typedRef.current || nav.index < frontierRef.current) return;
    const signature = codeSignature(student.id, lesson.id, beat.id, code);
    if (signature === lastCodeSyncRef.current) {
      pendingCodeRef.current = null;
      return;
    }
    pendingCodeRef.current = {
      key,
      index: nav.index,
      signature,
      body: { studentId: student.id, moduleId: lessonModule.id, lessonId: lesson.id, beatId: beat.id, code },
    };
    const timer = window.setTimeout(flushCode, CODE_SYNC_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, [preview, student, lessonModule, lesson, beat, nav.index, code]);

  useEffect(() => {
    // Write anything still waiting when the tab closes, the student switches away, or the player unmounts.
    function flushAll() {
      flushSave();
      flushCode();
    }
    function onVisibility() {
      if (document.visibilityState === "hidden") flushAll();
    }
    window.addEventListener("pagehide", flushAll);
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      window.removeEventListener("pagehide", flushAll);
      document.removeEventListener("visibilitychange", onVisibility);
      flushAll();
    };
  }, []);

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
    endLiveSession();
    const setup = activitySetup(part.activity, passedCodeRef.current);
    try {
      const result = await pythonAdapter.run({
        code: source,
        checks: part.activity?.checks ?? [],
        setup,
      });
      const printed = [result.stdout, result.stderr].filter((chunk) => chunk.trim().length > 0).join("");
      setOutput(printed);
      if (!result.ok) setExplainer(pythonAdapter.explain(result.traceback));
      const grade = gradeRun(part, result);
      setFeedback(grade.feedback);
      setFailedChecks(grade.failedChecks);
      const key = `${currentLesson.id}/${part.id}`;
      if (part.activity && grade.canContinue) {
        rememberPassedCode(part.id, source);
        if (passesOnGoal(part)) {
          setChecksPassed((previous) => ({ ...previous, [key]: true }));
        } else {
          writeNavigation(recordPass(navRef.current, currentLesson.beats));
        }
        if (part.skillCheck || part.board?.casting) await startLiveSession(key, setup, source);
        if (part.board?.casting) {
          // A fresh session starts everyone at full starting mana, so the board starts over too.
          setScript((previous) => ({ token: (previous?.token ?? 0) + 1, moves: [] }));
        }
      }
      if (part.partyPanel) {
        const mana = gameEvents(result.stageEvents).filter((event): event is ManaEvent => event.type === "mana");
        setManaScript((previous) => ({ token: (previous?.token ?? 0) + 1, events: mana }));
      }
      setTheater((previous) => {
        const next = nextTheaterState(part, result.stageEvents);
        return { ...next, flareToken: previous.flareToken + next.flareToken };
      });
      const moves = stageMoves(result.stageEvents);
      if (part.board && moves.length > 0) {
        setScript((previous) => ({ token: (previous?.token ?? 0) + 1, moves }));
      }
      const spoken = conversationEvents(result.stageEvents);
      if (part.conversation && spoken.length > 0) {
        setConversationScript((previous) => ({ token: (previous?.token ?? 0) + 1, events: spoken }));
        const lastPrompt = spoken.filter((event) => event.type === "prompt").at(-1);
        if (lastPrompt?.type === "prompt") rememberPrompt(part.id, lastPrompt.text);
      }
      await persist({
        status: "in_progress",
        lessonId: currentLesson.id,
        beatId: part.id,
        latestCode: source,
        index: current.index,
      });
    } catch (error) {
      explainFailure(error);
    } finally {
      setRunning(false);
    }
  }

  function onPartGoal() {
    const currentLesson = lessons[lessonIndex];
    const current = navRef.current;
    const part = currentLesson?.beats[current.index];
    if (!currentLesson || !part || !passesOnGoal(part) || current.passed[current.index]) return;
    writeNavigation(recordPass(current, currentLesson.beats));
    void persist({
      status: "in_progress",
      lessonId: currentLesson.id,
      beatId: part.id,
      latestCode: codeRef.current,
      index: current.index,
    });
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
    if (requiresPass(beat) && navRef.current.passed[navRef.current.index] !== true) return;
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
    writeCompleted(true);
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
      writeCompleted(false);
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
      {resumed && !preview ? (
        <p className="banner" data-testid="resumed">
          Welcome back! You are right where you left off.
        </p>
      ) : null}
      <section className="join-bar" aria-label="Classroom">
        {isStaticExport ? (
          <p className="local-note">This class stays in this browser. It does not sync to other computers.</p>
        ) : null}
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
        {preview ? null : (
          <p className="local-note autosave-status" data-testid="autosave-status" role="status">
            {saveStatus === "failed"
              ? "This browser would not save your progress. Keep this tab open until you finish."
              : saveStatus === "saved"
                ? "Progress saved on this computer."
                : "Your progress saves automatically."}
          </p>
        )}
      </section>

      <Theater
        scene={beat.scene}
        caption={theater.caption}
        flareToken={theater.flareToken}
        focusedImageId={theater.focusedImageId}
        stage={
          beat.board ? (
            <GameBoard
              key={`${lesson.id}/${beat.id}`}
              board={beat.board}
              features={partFeatures}
              script={script}
              autoFocus={!showsEditor(beat)}
              compact={showsEditor(beat)}
              lockedHint={
                beat.activity?.unlocks
                  ? { features: beat.activity.unlocks, text: "Finish the code below and press Run." }
                  : null
              }
              onGoal={onPartGoal}
              onCast={
                beat.board.casting
                  ? (index) => castFor(index, beat.board?.casting?.spell ?? "")
                  : undefined
              }
            />
          ) : beat.conversation ? (
            <ConversationScene
              key={`${lesson.id}/${beat.id}`}
              images={beat.scene.images}
              conversation={beat.conversation}
              prompt={prompts[beat.conversation.promptFrom ?? beat.id] ?? ""}
              script={conversationScript}
              canChoose={partFeatures.includes("dialogue")}
            />
          ) : beat.skillCheck ? (
            <SkillCheckScene
              key={`${lesson.id}/${beat.id}`}
              image={beat.scene.images[0]}
              skillCheck={beat.skillCheck}
              canRoll={unlocked}
              opened={partPassed}
              onRoll={rollSkill}
              onOpened={onPartGoal}
            />
          ) : beat.spellBook ? (
            <SpellBookScene
              key={`${lesson.id}/${beat.id}`}
              image={beat.scene.images[0]}
              spellBook={beat.spellBook}
              inked={partPassed}
            />
          ) : beat.partyPanel ? (
            <PartyPanelScene
              key={`${lesson.id}/${beat.id}`}
              image={beat.scene.images[0]}
              panel={beat.partyPanel}
              script={manaScript}
              passed={partPassed}
            />
          ) : undefined
        }
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

      {showsEditor(beat) ? (
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
            <button
              type="button"
              className="reset-code"
              data-testid="reset-code"
              onClick={() => setConfirmingReset(true)}
              disabled={running}
            >
              Reset code
            </button>
          </div>
          {confirmingReset ? (
            <div className="reset-confirm" role="alertdialog" aria-label="Reset code">
              <p>Replace your code with this part&apos;s starting code?</p>
              <button type="button" data-testid="reset-confirm" onClick={resetCode}>
                Yes, reset
              </button>
              <button
                type="button"
                className="reset-cancel"
                data-testid="reset-cancel"
                onClick={() => setConfirmingReset(false)}
              >
                Cancel
              </button>
            </div>
          ) : null}
          <PythonEditor code={code} onChange={onCodeChange} onBlur={onEditorBlur} />
          <ConsolePanel
            output={output}
            explainer={explainer}
            feedback={feedback}
            failedChecks={failedChecks}
          />
        </section>
      ) : null}

      {continueUnlocked ? (
        <button type="button" className="continue" data-testid="continue" onClick={() => void onContinue()}>
          Continue
        </button>
      ) : null}
    </main>
  );
}
