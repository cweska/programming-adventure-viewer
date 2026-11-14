/**
 * A random id for this browser's student, used only to seed the display order of choices (choiceOrder in
 * quiz-grading.ts), so two students side by side see the right answer in different places. Every student has
 * their own device (teacher decision 3). It is saved under its own localStorage key, apart from the progress: it is
 * not progress, and it never leaves the browser. Client-safe and SSR-safe: nothing touches `window` at import.
 * When storage is blocked it lives in memory for this visit.
 */
import { useSyncExternalStore } from "react";

export const STUDENT_SEED_KEY = "intro-python:seed";

let cached: string | null = null;

function freshSeed(): string {
  try {
    const bytes = new Uint32Array(2);
    globalThis.crypto.getRandomValues(bytes);
    return Array.from(bytes, (value) => value.toString(36)).join("");
  } catch {
    return `${Date.now().toString(36)}${Math.floor(Math.random() * 1e9).toString(36)}`;
  }
}

/** This browser's student seed (made and saved the first time it is asked for). Never throws. */
export function studentSeed(): string {
  if (cached !== null) return cached;
  let seed: string | null = null;
  try {
    seed = window.localStorage.getItem(STUDENT_SEED_KEY);
  } catch {
    seed = null;
  }
  if (!seed || !/^[0-9a-z]{4,40}$/.test(seed)) {
    seed = freshSeed();
    try {
      window.localStorage.setItem(STUDENT_SEED_KEY, seed);
    } catch {
      // Storage blocked: the seed lives in memory for this visit.
    }
  }
  cached = seed;
  return seed;
}

function noopSubscribe(): () => void {
  return () => undefined;
}

/**
 * The student seed, live: null during the server render and hydration (so pages never mismatch), then the seed.
 * Choice lists wait for it (they stay hidden until then), so the order never jumps after the page loads.
 */
export function useStudentSeed(): string | null {
  return useSyncExternalStore(noopSubscribe, studentSeed, () => null);
}
