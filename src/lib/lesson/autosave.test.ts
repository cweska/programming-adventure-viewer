import { describe, expect, it } from "vitest";
import type { KeyValueStorage } from "../classroom/local-store";
import {
  isAhead,
  parseSave,
  readSave,
  restoreSave,
  saveFrom,
  saveKey,
  writeSave,
  type PlaySave,
} from "./autosave";
import { emberkeepModule } from "./emberkeep";
import { makeValidModule } from "./fixtures";
import { findModule } from "./modules";
import { canGoForward, createPartNavigation, goBack, goForward, recordPass, setPartCode } from "./navigation";
import { visibleLessons } from "./progression";

const lessons = visibleLessons(emberkeepModule);
const lesson = lessons[0];
const parts = lesson.beats;

function memoryStorage(): KeyValueStorage & { values: Map<string, string> } {
  const values = new Map<string, string>();
  return {
    values,
    getItem(key) {
      return values.get(key) ?? null;
    },
    setItem(key, value) {
      values.set(key, value);
    },
  };
}

function playToPartThree() {
  let state = createPartNavigation(parts);
  state = setPartCode(state, 0, 'print("mine")\n');
  state = recordPass(state, parts);
  state = goForward(state, parts);
  state = setPartCode(state, 1, 'print("The gate is shut.")\n');
  state = recordPass(state, parts);
  state = goForward(state, parts);
  return setPartCode(state, 2, "# half written\n");
}

describe("autosave", () => {
  it("brings back the part, every part's code, and the passes", () => {
    const nav = playToPartThree();
    const save = saveFrom({ moduleId: emberkeepModule.id, lesson, nav, completed: false, frontier: 2 });
    expect(save.beatId).toBe(parts[2].id);
    expect(save.passed).toEqual([parts[0].id, parts[1].id]);

    const restored = restoreSave(save, lessons);
    expect(restored).not.toBeNull();
    expect(restored?.lessonIndex).toBe(0);
    expect(restored?.completed).toBe(false);
    expect(restored?.frontier).toBe(2);
    expect(restored?.nav.index).toBe(2);
    expect(restored?.nav.code[0]).toBe('print("mine")\n');
    expect(restored?.nav.code[1]).toBe('print("The gate is shut.")\n');
    expect(restored?.nav.code[2]).toBe("# half written\n");
    expect(restored?.nav.passed.slice(0, 3)).toEqual([true, true, false]);
    expect(restored?.nav.unlocked).toBe(nav.unlocked);
  });

  it("keeps Forward open to the furthest part after going Back", () => {
    const nav = goBack(goBack(playToPartThree()));
    const save = saveFrom({ moduleId: emberkeepModule.id, lesson, nav, completed: false, frontier: 2 });
    const restored = restoreSave(save, lessons);
    expect(restored?.nav.index).toBe(0);
    expect(restored?.nav.unlocked).toBe(2);
    expect(restored && canGoForward(restored.nav, parts.length)).toBe(true);
    expect(restored?.frontier).toBe(2);
  });

  it("leaves untouched parts out so they open with the lesson's own starter", () => {
    const save = saveFrom({
      moduleId: emberkeepModule.id,
      lesson,
      nav: createPartNavigation(parts),
      completed: false,
      frontier: 0,
    });
    expect(save.code).toEqual({});
    expect(restoreSave(save, lessons)?.nav.code).toEqual(createPartNavigation(parts).code);
  });

  it("restores a finished lesson", () => {
    let nav = createPartNavigation(parts);
    for (let index = 0; index < parts.length - 1; index += 1) {
      nav = goForward(recordPass(nav, parts), parts);
    }
    const save = saveFrom({ moduleId: emberkeepModule.id, lesson, nav, completed: true, frontier: parts.length - 1 });
    const restored = restoreSave(save, lessons);
    expect(restored?.completed).toBe(true);
    expect(restored?.nav.index).toBe(parts.length - 1);
  });

  it("skips parts that were removed from the lesson and keeps the rest", () => {
    const save = saveFrom({
      moduleId: emberkeepModule.id,
      lesson,
      nav: playToPartThree(),
      completed: false,
      frontier: 2,
    });
    const edited = { ...lesson, beats: parts.filter((_, index) => index !== 1) };
    const restored = restoreSave(save, [edited]);
    expect(restored?.nav.index).toBe(1);
    expect(restored?.nav.code[0]).toBe('print("mine")\n');
    expect(restored?.nav.code[1]).toBe("# half written\n");
  });

  it("falls back to the furthest part when the open part is gone", () => {
    const nav = goBack(playToPartThree());
    const save = saveFrom({ moduleId: emberkeepModule.id, lesson, nav, completed: false, frontier: 2 });
    const edited = { ...lesson, beats: parts.filter((_, index) => index !== 1) };
    expect(restoreSave(save, [edited])?.nav.index).toBe(1);
  });

  it("starts over when the saved lesson is gone or unpublished", () => {
    const module = makeValidModule();
    const draft = module.lessons[1];
    const save = saveFrom({
      moduleId: module.id,
      lesson: draft,
      nav: createPartNavigation(draft.beats),
      completed: false,
      frontier: 0,
    });
    expect(restoreSave(save, visibleLessons(module))).toBeNull();
    expect(restoreSave(save, module.lessons)?.lessonIndex).toBe(1);
  });

  it("reads back what it wrote and ignores broken or foreign saves", () => {
    const storage = memoryStorage();
    const save = saveFrom({
      moduleId: emberkeepModule.id,
      lesson,
      nav: playToPartThree(),
      completed: false,
      frontier: 2,
      savedAt: "2026-11-02T10:00:00.000Z",
    });
    expect(writeSave(storage, save)).toBe(true);
    expect(readSave(storage, emberkeepModule.id)).toEqual(save);
    expect(readSave(storage, "leylines-awaken")).toBeNull();

    storage.setItem(saveKey(emberkeepModule.id), "{not json");
    expect(readSave(storage, emberkeepModule.id)).toBeNull();
    expect(parseSave(JSON.stringify({ ...save, version: 2 }), emberkeepModule.id)).toBeNull();
    expect(parseSave(JSON.stringify({ ...save, moduleId: "other" }), emberkeepModule.id)).toBeNull();
    expect(parseSave(null, emberkeepModule.id)).toBeNull();
  });

  it("reports a failed write instead of throwing", () => {
    const full: KeyValueStorage = {
      getItem: () => null,
      setItem: () => {
        throw new Error("QuotaExceededError");
      },
    };
    const save = saveFrom({
      moduleId: emberkeepModule.id,
      lesson,
      nav: createPartNavigation(parts),
      completed: false,
      frontier: 0,
    });
    expect(writeSave(full, save)).toBe(false);
    const broken: KeyValueStorage = {
      getItem: () => {
        throw new Error("SecurityError");
      },
      setItem: () => undefined,
    };
    expect(readSave(broken, emberkeepModule.id)).toBeNull();
  });

  it("orders positions by lesson, then part, then completion", () => {
    const module = findModule("friends-in-low-places");
    const twoLessons = [lesson, ...(module ? visibleLessons(module) : [])];
    const first = { lessonId: lesson.id, beatId: parts[1].id };
    const later = { lessonId: lesson.id, beatId: parts[4].id };
    expect(isAhead(later, first, lessons)).toBe(true);
    expect(isAhead(first, later, lessons)).toBe(false);
    expect(isAhead(first, first, lessons)).toBe(false);
    expect(isAhead({ ...first, status: "completed" }, first, lessons)).toBe(true);
    expect(isAhead({ ...first, completed: true }, { ...first, status: "in_progress" }, lessons)).toBe(true);

    const nextLesson = twoLessons[1];
    if (nextLesson) {
      const start = { lessonId: nextLesson.id, beatId: nextLesson.beats[0].id };
      expect(isAhead(start, later, twoLessons)).toBe(true);
    }

    const gone = { lessonId: "gone", beatId: "gone" };
    expect(isAhead(gone, first, lessons)).toBe(false);
    expect(isAhead(first, gone, lessons)).toBe(true);
  });

  it("only accepts saves shaped like a save", () => {
    const save: PlaySave = saveFrom({
      moduleId: emberkeepModule.id,
      lesson,
      nav: createPartNavigation(parts),
      completed: false,
      frontier: 0,
    });
    expect(parseSave(JSON.stringify({ ...save, code: { a: 1 } }), emberkeepModule.id)).toBeNull();
    expect(parseSave(JSON.stringify({ ...save, passed: "all" }), emberkeepModule.id)).toBeNull();
  });
});
