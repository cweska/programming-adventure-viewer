import { describe, expect, it, vi } from "vitest";
import type { CourseProgress } from "./contracts";
import {
  PROGRESS_KEY,
  createProgressStore,
  emptyProgress,
  itemStatus,
  loadProgress,
  nextUpItem,
  normalizeProgress,
  parseProgress,
  saveProgress,
  unitProgress,
  withExercise,
  withQuiz,
  withRead,
  withSettings,
  withTestedOut,
  type ProgressStorage,
  type ProgressUnit,
} from "./progress";

function memoryStorage(initial: Record<string, string> = {}): ProgressStorage & { data: Record<string, string> } {
  const data = { ...initial };
  return {
    data,
    getItem: (key) => (key in data ? data[key] : null),
    setItem: (key, value) => {
      data[key] = value;
    },
  };
}

const blocked: ProgressStorage = {
  getItem: () => {
    throw new Error("SecurityError");
  },
  setItem: () => {
    throw new Error("QuotaExceededError");
  },
};

const unit: ProgressUnit = {
  id: "hello",
  order: 1,
  title: "Hello",
  published: true,
  items: [
    { id: "lesson", kind: "lesson", optional: false, exercises: [{ id: "a" }, { id: "b" }] },
    { id: "quiz", kind: "quiz", optional: false },
    { id: "project", kind: "project", optional: false },
    { id: "challenge", kind: "challenge", optional: true },
    { id: "article", kind: "article", optional: true, exercises: [{ id: "try-it" }] },
    { id: "notes", kind: "cheatsheet", optional: true },
    { id: "quick-check", kind: "testout", optional: true, exercises: [{ id: "t1" }] },
  ],
};

function apply(progress: CourseProgress, ...updates: ((p: CourseProgress) => CourseProgress)[]): CourseProgress {
  return updates.reduce((current, update) => update(current), progress);
}

const done = (previous: Parameters<Parameters<typeof withExercise>[1]>[0]) => ({ ...previous, done: true, passed: ["s"] });

describe("reading saved progress", () => {
  it("starts empty when nothing, junk or another version is saved", () => {
    expect(parseProgress(null)).toEqual(emptyProgress());
    expect(parseProgress("{not json")).toEqual(emptyProgress());
    expect(parseProgress(JSON.stringify({ version: 2, exercises: {} }))).toEqual(emptyProgress());
    expect(parseProgress("[]")).toEqual(emptyProgress());
  });

  it("keeps the good parts of a damaged save", () => {
    const progress = normalizeProgress({
      version: 1,
      exercises: {
        "u/i/e": { code: "print(1)", passed: ["a", 3, "a"], done: true, hintsUsed: { a: 2, b: "x" }, failedRuns: -2, extra: 7 },
        "u/i/bad": "nope",
      },
      quizzes: { "u/q": { best: 140, attempts: 2, lastAnswers: { q1: "1", q2: 5 } }, "u/broken": { best: "x" } },
      read: { "u/a": true, "u/b": "yes" },
      testedOut: "all",
      settings: { light: true, readAloud: "on" },
    });
    expect(progress.exercises["u/i/e"]).toMatchObject({
      code: "print(1)",
      passed: ["a"],
      done: true,
      hintsUsed: { a: 2 },
      failedRuns: 0,
      extra: 7,
    });
    expect(progress.exercises["u/i/bad"]).toBeUndefined();
    expect(progress.quizzes).toEqual({ "u/q": { best: 100, attempts: 2, lastAnswers: { q1: "1" } } });
    expect(progress.read).toEqual({ "u/a": true });
    expect(progress.testedOut).toEqual({});
    expect(progress.settings).toEqual({ light: true });
  });

  it("survives storage that throws", () => {
    expect(loadProgress(blocked)).toEqual(emptyProgress());
    expect(saveProgress(blocked, emptyProgress())).toBe(false);
    expect(loadProgress(null)).toEqual(emptyProgress());
    expect(saveProgress(null, emptyProgress())).toBe(false);
  });

  it("round-trips through storage", () => {
    const storage = memoryStorage();
    const progress = withRead("u/a")(emptyProgress());
    expect(saveProgress(storage, progress)).toBe(true);
    expect(JSON.parse(storage.data[PROGRESS_KEY])).toEqual(progress);
    expect(loadProgress(storage)).toEqual(progress);
  });
});

describe("updates", () => {
  it("changes one exercise without touching the old object", () => {
    const before = emptyProgress();
    const after = withExercise("u/i/e", (previous) => ({ ...previous, code: "x = 1", failedRuns: previous.failedRuns + 1 }))(
      before,
    );
    expect(before.exercises).toEqual({});
    expect(after.exercises["u/i/e"]).toEqual({ code: "x = 1", passed: [], done: false, hintsUsed: {}, failedRuns: 1 });
  });

  it("keeps the best quiz score and counts attempts", () => {
    const progress = apply(emptyProgress(), withQuiz("u/q", 50, { a: "1" }), withQuiz("u/q", 83.4), withQuiz("u/q", 20));
    expect(progress.quizzes["u/q"]).toEqual({ best: 83, attempts: 3, lastAnswers: { a: "1" } });
    expect(withQuiz("u/q", Number.NaN)(emptyProgress()).quizzes["u/q"].best).toBe(0);
    expect(withQuiz("u/q", 250)(emptyProgress()).quizzes["u/q"].best).toBe(100);
  });

  it("marks read, tested out and settings, and can undo them", () => {
    let progress = apply(emptyProgress(), withRead("u/a"), withTestedOut("u"), withSettings({ light: true }));
    expect(progress.read).toEqual({ "u/a": true });
    expect(progress.testedOut).toEqual({ u: true });
    expect(progress.settings).toEqual({ light: true });
    progress = apply(progress, withRead("u/a", false), withTestedOut("u", false), withSettings({ readAloud: true }));
    expect(progress.read).toEqual({});
    expect(progress.testedOut).toEqual({});
    expect(progress.settings).toEqual({ light: true, readAloud: true });
  });
});

describe("the store", () => {
  it("loads lazily, notifies listeners and saves", () => {
    const storage = memoryStorage({ [PROGRESS_KEY]: JSON.stringify(withRead("u/x")(emptyProgress())) });
    const store = createProgressStore(() => storage, { debounceMs: 0 });
    const listener = vi.fn();
    store.subscribe(listener);
    expect(store.get().read).toEqual({ "u/x": true });
    const first = store.get();
    expect(store.get()).toBe(first); // stable snapshot
    store.update(withRead("u/y"));
    expect(listener).toHaveBeenCalledTimes(1);
    expect(store.get()).not.toBe(first);
    expect(JSON.parse(storage.data[PROGRESS_KEY]).read).toEqual({ "u/x": true, "u/y": true });
    expect(store.saving()).toBe(true);
  });

  it("debounces writes and flushes on demand", () => {
    vi.useFakeTimers();
    try {
      const storage = memoryStorage();
      const store = createProgressStore(() => storage, { debounceMs: 300 });
      store.update(withRead("u/a"));
      store.update(withRead("u/b"));
      expect(storage.data[PROGRESS_KEY]).toBeUndefined();
      vi.advanceTimersByTime(300);
      expect(JSON.parse(storage.data[PROGRESS_KEY]).read).toEqual({ "u/a": true, "u/b": true });
      store.update(withRead("u/c"));
      store.flush();
      expect(JSON.parse(storage.data[PROGRESS_KEY]).read).toEqual({ "u/a": true, "u/b": true, "u/c": true });
    } finally {
      vi.useRealTimers();
    }
  });

  it("keeps working in memory when storage is blocked or missing", () => {
    for (const storage of [blocked, null]) {
      const store = createProgressStore(() => storage, { debounceMs: 0 });
      store.update(withTestedOut("u"));
      expect(store.get().testedOut).toEqual({ u: true });
      expect(store.saving()).toBe(false);
    }
  });

  it("ignores an update that throws", () => {
    const store = createProgressStore(() => memoryStorage(), { debounceMs: 0 });
    const spy = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const before = store.get();
    store.update(() => {
      throw new Error("bad");
    });
    expect(store.get()).toBe(before);
    spy.mockRestore();
  });

  it("reloads what another tab saved", () => {
    const storage = memoryStorage();
    const store = createProgressStore(() => storage, { debounceMs: 0 });
    store.get();
    storage.setItem(PROGRESS_KEY, JSON.stringify(withRead("u/other")(emptyProgress())));
    store.reload();
    expect(store.get().read).toEqual({ "u/other": true });
  });
});

describe("item status", () => {
  const [lesson, quiz, project, challenge, article, notes, quickCheck] = unit.items;

  it("is not started with no progress", () => {
    for (const item of unit.items) expect(itemStatus("hello", item, emptyProgress())).toBe("not-started");
  });

  it("counts an opened exercise as started", () => {
    const progress = withExercise("hello/lesson/a", (previous) => ({ ...previous, firstSeenAt: 1 }))(emptyProgress());
    expect(itemStatus("hello", lesson, progress)).toBe("in-progress");
  });

  it("follows a lesson's exercises", () => {
    let progress = withExercise("hello/lesson/a", (previous) => ({ ...previous, code: "x" }))(emptyProgress());
    expect(itemStatus("hello", lesson, progress)).toBe("in-progress");
    progress = withExercise("hello/lesson/a", done)(progress);
    expect(itemStatus("hello", lesson, progress)).toBe("in-progress");
    progress = withExercise("hello/lesson/b", done)(progress);
    expect(itemStatus("hello", lesson, progress)).toBe("done");
  });

  it("uses the item key for projects and challenges, attempts for quizzes, read for articles", () => {
    const progress = apply(
      emptyProgress(),
      withExercise("hello/project", (previous) => ({ ...previous, failedRuns: 1 })),
      withExercise("hello/challenge", done),
      withQuiz("hello/quiz", 40),
      withExercise("hello/article/try-it", (previous) => ({ ...previous, code: "x" })),
      withRead("hello/notes"),
    );
    expect(itemStatus("hello", project, progress)).toBe("in-progress");
    expect(itemStatus("hello", challenge, progress)).toBe("done");
    expect(itemStatus("hello", quiz, progress)).toBe("done");
    expect(itemStatus("hello", article, progress)).toBe("in-progress");
    expect(itemStatus("hello", article, withRead("hello/article")(progress))).toBe("done");
    expect(itemStatus("hello", notes, progress)).toBe("done");
  });

  it("marks core items tested out after a Quick Check pass, but keeps real done", () => {
    const progress = apply(emptyProgress(), withTestedOut("hello"), withQuiz("hello/quiz", 100));
    expect(itemStatus("hello", lesson, progress)).toBe("tested-out");
    expect(itemStatus("hello", quiz, progress)).toBe("done");
    expect(itemStatus("hello", challenge, progress)).toBe("not-started");
    expect(itemStatus("hello", quickCheck, progress)).toBe("done");
  });

  it("counts a Quick Check done when all its exercises pass", () => {
    const progress = withExercise("hello/quick-check/t1", done)(emptyProgress());
    expect(itemStatus("hello", quickCheck, progress)).toBe("done");
  });
});

describe("unit progress", () => {
  it("counts core items only", () => {
    expect(unitProgress(unit, emptyProgress())).toEqual({
      done: 0,
      total: 3,
      percent: 0,
      testedOut: false,
      started: false,
      complete: false,
    });
    const progress = apply(
      emptyProgress(),
      withQuiz("hello/quiz", 90),
      withExercise("hello/challenge", done),
      withRead("hello/notes"),
    );
    expect(unitProgress(unit, progress)).toMatchObject({ done: 1, total: 3, percent: 33, started: true, complete: false });
  });

  it("is complete when every core item is done", () => {
    const progress = apply(
      emptyProgress(),
      withExercise("hello/lesson/a", done),
      withExercise("hello/lesson/b", done),
      withQuiz("hello/quiz", 10),
      withExercise("hello/project", done),
    );
    expect(unitProgress(unit, progress)).toMatchObject({ done: 3, total: 3, percent: 100, complete: true });
  });

  it("counts every core item done after a Quick Check pass", () => {
    expect(unitProgress(unit, withTestedOut("hello")(emptyProgress()))).toEqual({
      done: 3,
      total: 3,
      percent: 100,
      testedOut: true,
      started: true,
      complete: true,
    });
  });

  it("points Next up at the first core item not done", () => {
    expect(nextUpItem("hello", unit.items, emptyProgress())?.id).toBe("lesson");
    const progress = apply(emptyProgress(), withExercise("hello/lesson/a", done), withExercise("hello/lesson/b", done));
    expect(nextUpItem("hello", unit.items, progress)?.id).toBe("quiz");
    expect(nextUpItem("hello", unit.items, withTestedOut("hello")(emptyProgress()))).toBeUndefined();
  });
});
