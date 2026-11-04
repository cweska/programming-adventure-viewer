import { z } from "zod";
import type { KeyValueStorage } from "../classroom/local-store";
import { navigationFromSave, type PartNavigation } from "./navigation";
import { starterFor } from "./progression";
import type { Lesson } from "./schema";

const SAVE_PREFIX = "emberkeep-autosave:";

// Parts and lessons are saved by id, not position, so a save still opens after a lesson is edited.
const playSaveSchema = z.object({
  version: z.literal(1),
  moduleId: z.string().min(1),
  lessonId: z.string().min(1),
  beatId: z.string().min(1),
  reachedBeatId: z.string().min(1),
  frontierBeatId: z.string().min(1),
  completed: z.boolean(),
  passed: z.array(z.string()),
  code: z.record(z.string()),
  savedAt: z.string(),
});

export type PlaySave = z.infer<typeof playSaveSchema>;

export type PlayPosition = {
  lessonId: string;
  beatId: string;
  status?: "in_progress" | "completed";
  completed?: boolean;
};

export type RestoredPlay = {
  lessonIndex: number;
  nav: PartNavigation;
  completed: boolean;
  frontier: number;
};

export function saveKey(moduleId: string): string {
  return `${SAVE_PREFIX}${moduleId}`;
}

function clampIndex(index: number, count: number): number {
  return Math.min(Math.max(index, 0), Math.max(count - 1, 0));
}

export function saveFrom(input: {
  moduleId: string;
  lesson: Lesson;
  nav: PartNavigation;
  completed: boolean;
  frontier: number;
  savedAt?: string;
}): PlaySave {
  const { lesson, nav } = input;
  const beats = lesson.beats;
  const idAt = (index: number) => beats[clampIndex(index, beats.length)]?.id ?? "";
  const code: Record<string, string> = {};
  beats.forEach((beat, index) => {
    const source = nav.code[index];
    // Untouched parts are left out, so a fixed starter in the lesson still reaches the student.
    if (typeof source === "string" && source !== starterFor(beat)) code[beat.id] = source;
  });
  return {
    version: 1,
    moduleId: input.moduleId,
    lessonId: lesson.id,
    beatId: idAt(nav.index),
    reachedBeatId: idAt(Math.max(nav.unlocked, nav.index)),
    frontierBeatId: idAt(input.frontier),
    completed: input.completed,
    passed: beats.filter((_, index) => nav.passed[index] === true).map((beat) => beat.id),
    code,
    savedAt: input.savedAt ?? new Date().toISOString(),
  };
}

export function restoreSave(save: PlaySave, lessons: Lesson[]): RestoredPlay | null {
  const lessonIndex = lessons.findIndex((lesson) => lesson.id === save.lessonId);
  if (lessonIndex < 0) return null;
  const beats = lessons[lessonIndex].beats;
  const find = (id: string) => beats.findIndex((beat) => beat.id === id);
  const reachedIndex = find(save.reachedBeatId);
  let index = find(save.beatId);
  if (index < 0) index = reachedIndex;
  if (index < 0) return null;
  const frontierIndex = find(save.frontierBeatId);
  const nav = navigationFromSave(beats, {
    index,
    reached: Math.max(reachedIndex, index),
    passed: beats.map((beat) => save.passed.includes(beat.id)),
    code: beats.map((beat) => save.code[beat.id]),
  });
  return {
    lessonIndex,
    nav,
    completed: save.completed,
    frontier: frontierIndex >= 0 ? frontierIndex : index,
  };
}

export function parseSave(raw: string | null, moduleId: string): PlaySave | null {
  if (!raw) return null;
  try {
    const parsed = playSaveSchema.safeParse(JSON.parse(raw));
    if (!parsed.success || parsed.data.moduleId !== moduleId) return null;
    return parsed.data;
  } catch {
    return null;
  }
}

export function readSave(storage: KeyValueStorage, moduleId: string): PlaySave | null {
  try {
    return parseSave(storage.getItem(saveKey(moduleId)), moduleId);
  } catch {
    return null;
  }
}

export function writeSave(storage: KeyValueStorage, save: PlaySave): boolean {
  try {
    storage.setItem(saveKey(save.moduleId), JSON.stringify(save));
    return true;
  } catch {
    return false;
  }
}

export function browserStorage(): KeyValueStorage | null {
  try {
    return typeof window === "undefined" ? null : window.localStorage;
  } catch {
    return null;
  }
}

function rank(position: PlayPosition, lessons: Lesson[]): [number, number, number] | null {
  const lessonIndex = lessons.findIndex((lesson) => lesson.id === position.lessonId);
  if (lessonIndex < 0) return null;
  const beatIndex = lessons[lessonIndex].beats.findIndex((beat) => beat.id === position.beatId);
  if (beatIndex < 0) return null;
  const completed = position.completed === true || position.status === "completed";
  return [lessonIndex, beatIndex, completed ? 1 : 0];
}

// True when `ahead` is further through the module than `behind`. A position that is no longer in the
// module is never ahead, and anything that is still in the module is ahead of one that is not.
export function isAhead(ahead: PlayPosition, behind: PlayPosition, lessons: Lesson[]): boolean {
  const left = rank(ahead, lessons);
  if (!left) return false;
  const right = rank(behind, lessons);
  if (!right) return true;
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) return left[index] > right[index];
  }
  return false;
}
