/**
 * Intro to Python progress, saved in this browser under localStorage "intro-python:v1"
 * (shape: CourseProgress in contracts.ts). Client-safe and SSR-safe: nothing touches `window` at import.
 *
 *  - Reading tolerates a missing, corrupt or blocked store: bad fields are dropped one by one, and when
 *    storage cannot be used at all the progress lives in memory for this visit.
 *  - Writes go to listeners at once and to storage after a short debounce (code autosaves on every
 *    keystroke), and are flushed when the tab is hidden or closed.
 *  - useCourseProgress() reads the store with useSyncExternalStore. The server render (and the first
 *    client render while hydrating) sees empty progress, so pages never mismatch.
 *  - Everything is keyed by id, so editing content never breaks a save. Status is derived, never stored.
 */
import { useSyncExternalStore } from "react";
import type {
  CourseProgress,
  CourseSettings,
  ExerciseProgress,
  ItemStatus,
  QuizProgress,
} from "./contracts";
import type { Item } from "./schema";

export const PROGRESS_KEY = "intro-python:v1";

/** How long writes wait before going to localStorage (ms). */
export const SAVE_DEBOUNCE_MS = 300;

/* ------------------------------------------------------------------------------------------------ */
/* Outline types: what progress maths needs to know about items (full Items fit these too)           */
/* ------------------------------------------------------------------------------------------------ */

export type ProgressItem = {
  id: string;
  kind: Item["kind"];
  optional: boolean;
  title?: string;
  summary?: string;
  minutes?: number;
  /** Lessons, test-outs and articles: their exercise ids. Projects and challenges have none. */
  exercises?: readonly { id: string }[];
};

export type ProgressUnit = {
  id: string;
  order: number;
  title: string;
  subtitle?: string;
  published: boolean;
  items: ProgressItem[];
};

/* ------------------------------------------------------------------------------------------------ */
/* Shape and repair                                                                                  */
/* ------------------------------------------------------------------------------------------------ */

export function emptyProgress(): CourseProgress {
  return { version: 1, exercises: {}, quizzes: {}, read: {}, testedOut: {}, settings: {} };
}

export function emptyExercise(): ExerciseProgress {
  return { passed: [], done: false, hintsUsed: {}, failedRuns: 0 };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function finiteNumber(value: unknown): number | undefined {
  return typeof value === "number" && Number.isFinite(value) ? value : undefined;
}

function cleanExercise(value: unknown): ExerciseProgress | null {
  if (!isRecord(value)) return null;
  // Keep fields this file does not know about (a newer player may add some).
  const out: ExerciseProgress & Record<string, unknown> = { ...value, ...emptyExercise() };
  if (typeof value.code === "string") out.code = value.code;
  else delete out.code;
  out.passed = Array.isArray(value.passed)
    ? [...new Set(value.passed.filter((id): id is string => typeof id === "string"))]
    : [];
  out.done = value.done === true;
  out.hintsUsed = {};
  if (isRecord(value.hintsUsed)) {
    for (const [id, rungs] of Object.entries(value.hintsUsed)) {
      const count = finiteNumber(rungs);
      if (count !== undefined && count >= 0) out.hintsUsed[id] = Math.floor(count);
    }
  }
  out.failedRuns = Math.max(0, Math.floor(finiteNumber(value.failedRuns) ?? 0));
  for (const field of ["firstSeenAt", "activeMs"] as const) {
    const number = finiteNumber(value[field]);
    if (number !== undefined && number >= 0) out[field] = number;
    else delete out[field];
  }
  for (const field of ["solutionShown", "bonusDone"] as const) {
    if (typeof value[field] === "boolean") out[field] = value[field] as boolean;
    else delete out[field];
  }
  return out;
}

function cleanQuiz(value: unknown): QuizProgress | null {
  if (!isRecord(value)) return null;
  const best = finiteNumber(value.best);
  const attempts = finiteNumber(value.attempts);
  if (best === undefined || attempts === undefined) return null;
  const out: QuizProgress = {
    best: Math.min(100, Math.max(0, best)),
    attempts: Math.max(0, Math.floor(attempts)),
  };
  if (isRecord(value.lastAnswers)) {
    const answers: Record<string, string> = {};
    for (const [id, answer] of Object.entries(value.lastAnswers)) {
      if (typeof answer === "string") answers[id] = answer;
    }
    out.lastAnswers = answers;
  }
  return out;
}

function cleanFlags(value: unknown): Record<string, true> {
  const out: Record<string, true> = {};
  if (isRecord(value)) {
    for (const [key, flag] of Object.entries(value)) if (flag === true) out[key] = true;
  }
  return out;
}

function cleanSettings(value: unknown): CourseSettings {
  const out: CourseSettings = {};
  if (isRecord(value)) {
    if (typeof value.light === "boolean") out.light = value.light;
    if (typeof value.readAloud === "boolean") out.readAloud = value.readAloud;
  }
  return out;
}

/** Repair any value into a valid CourseProgress, keeping every part that is still good. */
export function normalizeProgress(value: unknown): CourseProgress {
  if (!isRecord(value) || value.version !== 1) return emptyProgress();
  const progress = emptyProgress();
  if (isRecord(value.exercises)) {
    for (const [key, entry] of Object.entries(value.exercises)) {
      const exercise = cleanExercise(entry);
      if (exercise) progress.exercises[key] = exercise;
    }
  }
  if (isRecord(value.quizzes)) {
    for (const [key, entry] of Object.entries(value.quizzes)) {
      const quiz = cleanQuiz(entry);
      if (quiz) progress.quizzes[key] = quiz;
    }
  }
  progress.read = cleanFlags(value.read);
  progress.testedOut = cleanFlags(value.testedOut);
  progress.settings = cleanSettings(value.settings);
  return progress;
}

/** Parse saved text. Missing or corrupt text gives empty progress; it never throws. */
export function parseProgress(text: string | null | undefined): CourseProgress {
  if (!text) return emptyProgress();
  try {
    return normalizeProgress(JSON.parse(text));
  } catch {
    return emptyProgress();
  }
}

/* ------------------------------------------------------------------------------------------------ */
/* Storage                                                                                           */
/* ------------------------------------------------------------------------------------------------ */

export type ProgressStorage = Pick<Storage, "getItem" | "setItem">;

/** window.localStorage, or null when there is none or the browser blocks it. Never throws. */
export function browserProgressStorage(): ProgressStorage | null {
  try {
    if (typeof window === "undefined") return null;
    const storage = window.localStorage;
    if (!storage) return null;
    const probe = `${PROGRESS_KEY}:probe`;
    storage.setItem(probe, "1");
    storage.removeItem(probe);
    return storage;
  } catch {
    return null;
  }
}

export function loadProgress(storage: ProgressStorage | null): CourseProgress {
  if (!storage) return emptyProgress();
  try {
    return parseProgress(storage.getItem(PROGRESS_KEY));
  } catch {
    return emptyProgress();
  }
}

/** Write progress. Returns false when the browser would not save it (blocked or full storage). */
export function saveProgress(storage: ProgressStorage | null, progress: CourseProgress): boolean {
  if (!storage) return false;
  try {
    storage.setItem(PROGRESS_KEY, JSON.stringify(progress));
    return true;
  } catch {
    return false;
  }
}

/* ------------------------------------------------------------------------------------------------ */
/* Pure updates (each returns new objects, so React sees the change)                                 */
/* ------------------------------------------------------------------------------------------------ */

export type ProgressUpdate = (progress: CourseProgress) => CourseProgress;

export function withExercise(key: string, fn: (previous: ExerciseProgress) => ExerciseProgress): ProgressUpdate {
  return (progress) => {
    const previous = progress.exercises[key] ?? emptyExercise();
    const next = fn({ ...previous, passed: [...previous.passed], hintsUsed: { ...previous.hintsUsed } });
    return { ...progress, exercises: { ...progress.exercises, [key]: next } };
  };
}

/** Count one finished attempt; keep the best percent (0 to 100). */
export function withQuiz(key: string, percent: number, lastAnswers?: Record<string, string>): ProgressUpdate {
  return (progress) => {
    const previous = progress.quizzes[key];
    const score = Math.min(100, Math.max(0, Math.round(Number.isFinite(percent) ? percent : 0)));
    const next: QuizProgress = {
      best: Math.max(previous?.best ?? 0, score),
      attempts: (previous?.attempts ?? 0) + 1,
      ...(lastAnswers ? { lastAnswers: { ...lastAnswers } } : previous?.lastAnswers ? { lastAnswers: previous.lastAnswers } : {}),
    };
    return { ...progress, quizzes: { ...progress.quizzes, [key]: next } };
  };
}

export function withRead(key: string, read = true): ProgressUpdate {
  return (progress) => {
    const next = { ...progress.read };
    if (read) next[key] = true;
    else delete next[key];
    return { ...progress, read: next };
  };
}

export function withTestedOut(unitId: string, testedOut = true): ProgressUpdate {
  return (progress) => {
    const next = { ...progress.testedOut };
    if (testedOut) next[unitId] = true;
    else delete next[unitId];
    return { ...progress, testedOut: next };
  };
}

export function withSettings(patch: Partial<CourseSettings>): ProgressUpdate {
  return (progress) => ({ ...progress, settings: { ...progress.settings, ...patch } });
}

/* ------------------------------------------------------------------------------------------------ */
/* The store                                                                                         */
/* ------------------------------------------------------------------------------------------------ */

export type ProgressStore = {
  get(): CourseProgress;
  update(fn: ProgressUpdate): CourseProgress;
  replace(progress: CourseProgress): void;
  subscribe(listener: () => void): () => void;
  /** Write any pending change to storage now. */
  flush(): void;
  /** False when this browser is not saving progress (it still works for this visit). */
  saving(): boolean;
  /** Re-read storage (another tab saved). */
  reload(): void;
};

export function createProgressStore(
  getStorage: () => ProgressStorage | null,
  options: { debounceMs?: number } = {},
): ProgressStore {
  const debounceMs = options.debounceMs ?? SAVE_DEBOUNCE_MS;
  let storage: ProgressStorage | null = null;
  let current: CourseProgress | null = null;
  let saveWorks = true;
  let timer: ReturnType<typeof setTimeout> | null = null;
  let dirty = false;
  /** This tab's updates since its last write. Replayed on top of another tab's save, so neither is lost. */
  let pending: ProgressUpdate[] = [];
  /** The stored text this tab last read or wrote (anything else there came from another tab). */
  let synced: string | null = null;
  const listeners = new Set<() => void>();

  /** The stored text, or undefined when it cannot be read. */
  function readText(): string | null | undefined {
    if (!storage) return undefined;
    try {
      return storage.getItem(PROGRESS_KEY);
    } catch {
      return undefined;
    }
  }

  function ensure(): CourseProgress {
    if (current === null) {
      storage = getStorage();
      saveWorks = storage !== null;
      const text = readText();
      current = parseProgress(text ?? null);
      synced = text ?? null;
    }
    return current;
  }

  function emit() {
    for (const listener of [...listeners]) listener();
  }

  /**
   * If another tab saved since this tab last synced, rebuild this tab's progress as that save plus this
   * tab's unsaved updates (in order). Returns true when the progress changed.
   */
  function rebase(): boolean {
    const text = readText();
    if (text === undefined || text === null || text === synced) return false;
    let parsed: unknown;
    try {
      parsed = JSON.parse(text);
    } catch {
      return false; // never build on a broken save; this tab's copy is written over it
    }
    if (!isRecord(parsed) || parsed.version !== 1) return false;
    let merged = normalizeProgress(parsed);
    for (const fn of pending) {
      try {
        merged = fn(merged);
      } catch (error) {
        console.error("Could not replay a course progress update.", error);
      }
    }
    current = merged;
    synced = text;
    return true;
  }

  function flush() {
    if (timer !== null) {
      clearTimeout(timer);
      timer = null;
    }
    if (!dirty || current === null) return;
    dirty = false;
    const changed = rebase();
    pending = [];
    if (storage) {
      try {
        const text = JSON.stringify(current);
        storage.setItem(PROGRESS_KEY, text);
        synced = text;
        saveWorks = true;
      } catch {
        saveWorks = false;
      }
    } else {
      saveWorks = false;
    }
    if (changed) emit();
  }

  function schedule() {
    dirty = true;
    if (debounceMs <= 0) {
      flush();
      return;
    }
    if (timer !== null) clearTimeout(timer);
    timer = setTimeout(flush, debounceMs);
  }

  return {
    get: ensure,
    update(fn) {
      const before = ensure();
      let next: CourseProgress;
      try {
        next = fn(before);
      } catch (error) {
        console.error("Could not update course progress.", error);
        return before;
      }
      if (next === before) return before;
      current = next;
      pending.push(fn);
      schedule();
      emit();
      return next;
    },
    replace(progress) {
      ensure();
      const replacement = normalizeProgress(progress);
      current = replacement;
      pending = [() => replacement];
      schedule();
      emit();
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    },
    flush,
    saving() {
      ensure();
      return saveWorks;
    },
    reload() {
      ensure();
      if (dirty) {
        // Keep this tab's unsaved changes, on top of what the other tab saved; they are written next.
        if (rebase()) emit();
        return;
      }
      const text = readText();
      if (text === undefined || text === synced) return;
      current = parseProgress(text);
      synced = text;
      emit();
    },
  };
}

/* ------------------------------------------------------------------------------------------------ */
/* The browser's store and its hooks                                                                 */
/* ------------------------------------------------------------------------------------------------ */

const store = createProgressStore(browserProgressStorage);
const SERVER_SNAPSHOT: CourseProgress = Object.freeze(emptyProgress()) as CourseProgress;
let windowListeners = false;

function attachWindowListeners() {
  if (windowListeners || typeof window === "undefined") return;
  windowListeners = true;
  try {
    window.addEventListener("pagehide", () => store.flush());
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") store.flush();
    });
    window.addEventListener("storage", (event) => {
      if (event.key === PROGRESS_KEY) store.reload();
    });
  } catch {
    // No window events: writes still happen after the debounce.
  }
}

function subscribeStore(listener: () => void): () => void {
  attachWindowListeners();
  return store.subscribe(listener);
}

function clientSnapshot(): CourseProgress {
  return store.get();
}

function serverSnapshot(): CourseProgress {
  return SERVER_SNAPSHOT;
}

/** The student's course progress. Empty during the server render and hydration, then the saved progress. */
export function useCourseProgress(): CourseProgress {
  return useSyncExternalStore(subscribeStore, clientSnapshot, serverSnapshot);
}

function noopSubscribe(): () => void {
  return () => undefined;
}

/** True once the page has hydrated and useCourseProgress() shows the real save (false on the server). */
export function useProgressReady(): boolean {
  return useSyncExternalStore(
    noopSubscribe,
    () => true,
    () => false,
  );
}

/** The current progress outside React (e.g. in an event handler). */
export function getCourseProgress(): CourseProgress {
  return store.get();
}

/** Whether this browser is saving progress (false in private modes that block storage). */
export function progressIsSaving(): boolean {
  return store.saving();
}

export function flushCourseProgress(): void {
  store.flush();
}

/** Change one exercise's progress (key = exerciseKey(...) from schema.ts). */
export function updateExercise(key: string, fn: (previous: ExerciseProgress) => ExerciseProgress): CourseProgress {
  return store.update(withExercise(key, fn));
}

/** Record a finished quiz attempt (key = `${unitId}/${itemId}`, percent 0 to 100). */
export function recordQuiz(key: string, percent: number, lastAnswers?: Record<string, string>): CourseProgress {
  return store.update(withQuiz(key, percent, lastAnswers));
}

/** Mark an article or cheatsheet as read (key = `${unitId}/${itemId}`). */
export function markRead(key: string, read = true): CourseProgress {
  return store.update(withRead(key, read));
}

/** The student passed this unit's Quick Check. */
export function markTestedOut(unitId: string, testedOut = true): CourseProgress {
  return store.update(withTestedOut(unitId, testedOut));
}

export function setSettings(patch: Partial<CourseSettings>): CourseProgress {
  return store.update(withSettings(patch));
}

/* ------------------------------------------------------------------------------------------------ */
/* Derived status                                                                                    */
/* ------------------------------------------------------------------------------------------------ */

export function itemKey(unitId: string, itemId: string): string {
  return `${unitId}/${itemId}`;
}

function exerciseStarted(entry: ExerciseProgress | undefined): boolean {
  if (!entry) return false;
  return (
    entry.done ||
    entry.passed.length > 0 ||
    entry.failedRuns > 0 ||
    entry.code !== undefined ||
    entry.firstSeenAt !== undefined ||
    Object.keys(entry.hintsUsed).length > 0
  );
}

function exercisesStatus(
  unitId: string,
  item: ProgressItem,
  progress: CourseProgress,
): { done: boolean; started: boolean } {
  const exercises = item.exercises ?? [];
  const entries = exercises.map((exercise) => progress.exercises[`${unitId}/${item.id}/${exercise.id}`]);
  return {
    done: exercises.length > 0 && entries.every((entry) => entry?.done === true),
    started: entries.some(exerciseStarted),
  };
}

function rawStatus(unitId: string, item: ProgressItem, progress: CourseProgress): ItemStatus {
  const key = itemKey(unitId, item.id);
  switch (item.kind) {
    case "lesson": {
      const { done, started } = exercisesStatus(unitId, item, progress);
      return done ? "done" : started ? "in-progress" : "not-started";
    }
    case "testout": {
      if (progress.testedOut[unitId]) return "done";
      const { done, started } = exercisesStatus(unitId, item, progress);
      return done ? "done" : started ? "in-progress" : "not-started";
    }
    case "project":
    case "challenge": {
      const entry = progress.exercises[key];
      return entry?.done ? "done" : exerciseStarted(entry) ? "in-progress" : "not-started";
    }
    case "quiz": {
      const quiz = progress.quizzes[key];
      return quiz && quiz.attempts > 0 ? "done" : "not-started";
    }
    case "article": {
      if (progress.read[key]) return "done";
      return exercisesStatus(unitId, item, progress).started ? "in-progress" : "not-started";
    }
    case "cheatsheet":
      return progress.read[key] ? "done" : "not-started";
    default:
      return "not-started";
  }
}

/**
 * An item's status. A core item in a unit the student tested out of reads "tested-out" (unless they did it
 * anyway, then "done").
 */
export function itemStatus(unitId: string, item: ProgressItem, progress: CourseProgress): ItemStatus {
  const status = rawStatus(unitId, item, progress);
  if (status !== "done" && progress.testedOut[unitId] && !item.optional && item.kind !== "testout") return "tested-out";
  return status;
}

export type UnitProgress = {
  /** Core (not optional) items done, or all of them after a Quick Check pass. */
  done: number;
  total: number;
  /** 0 to 100. */
  percent: number;
  testedOut: boolean;
  /** Any item touched. */
  started: boolean;
  complete: boolean;
};

export function unitProgress(unit: Pick<ProgressUnit, "id" | "items">, progress: CourseProgress): UnitProgress {
  const core = unit.items.filter((item) => !item.optional && item.kind !== "testout");
  const testedOut = progress.testedOut[unit.id] === true;
  const statuses = unit.items.map((item) => ({ item, status: itemStatus(unit.id, item, progress) }));
  const doneCore = statuses.filter(
    ({ item, status }) => !item.optional && item.kind !== "testout" && (status === "done" || status === "tested-out"),
  ).length;
  const done = testedOut ? core.length : doneCore;
  const total = core.length;
  return {
    done,
    total,
    percent: total === 0 ? (testedOut ? 100 : 0) : Math.round((done / total) * 100),
    testedOut,
    started: testedOut || statuses.some(({ status }) => status !== "not-started"),
    complete: testedOut || (total > 0 && done === total),
  };
}

/** The first core item not done yet: the "Next up" marker. Undefined when the unit is complete. */
export function nextUpItem<T extends ProgressItem>(unitId: string, items: readonly T[], progress: CourseProgress): T | undefined {
  if (progress.testedOut[unitId]) return undefined;
  return items.find(
    (item) => !item.optional && item.kind !== "testout" && itemStatus(unitId, item, progress) !== "done",
  );
}
