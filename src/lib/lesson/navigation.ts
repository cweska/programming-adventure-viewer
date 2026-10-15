import type { Beat } from "./schema";
import { starterFor } from "./progression";

export type PartNavigation = {
  index: number;
  unlocked: number;
  passed: boolean[];
  code: string[];
};

export function partLabel(index: number, count: number): string {
  return `Part ${index + 1} of ${count}`;
}

export function canGoBack(state: PartNavigation): boolean {
  return state.index > 0;
}

export function canGoForward(state: PartNavigation, partCount: number): boolean {
  return state.index < state.unlocked && state.index < partCount - 1;
}

function refreshUnlock(state: PartNavigation, parts: Beat[]): PartNavigation {
  let unlocked = Math.max(state.unlocked, state.index);
  for (let index = 0; index < parts.length; index += 1) {
    const story = !parts[index]?.activity;
    const passed = state.passed[index] === true;
    if ((story || passed) && index <= unlocked && index + 1 < parts.length) {
      unlocked = Math.max(unlocked, index + 1);
    }
  }
  return { ...state, unlocked };
}

export function createPartNavigation(parts: Beat[]): PartNavigation {
  return refreshUnlock(
    {
      index: 0,
      unlocked: 0,
      passed: parts.map(() => false),
      code: parts.map((part) => starterFor(part)),
    },
    parts,
  );
}

export function navigationFromProgress(
  parts: Beat[],
  index: number,
  latestCode: string,
  completed: boolean,
): PartNavigation {
  const safeIndex = Math.min(Math.max(index, 0), Math.max(parts.length - 1, 0));
  const passed = parts.map((_, partIndex) => completed || partIndex < safeIndex);
  const code = parts.map((part, partIndex) =>
    partIndex === safeIndex && latestCode ? latestCode : starterFor(part),
  );
  return refreshUnlock(
    {
      index: safeIndex,
      unlocked: completed ? Math.max(parts.length - 1, 0) : safeIndex,
      passed,
      code,
    },
    parts,
  );
}

export function setPartCode(state: PartNavigation, index: number, code: string): PartNavigation {
  if (index < 0 || index >= state.code.length) return state;
  const nextCode = state.code.slice();
  nextCode[index] = code;
  return { ...state, code: nextCode };
}

export function recordPass(state: PartNavigation, parts: Beat[]): PartNavigation {
  const passed = state.passed.slice();
  passed[state.index] = true;
  return refreshUnlock({ ...state, passed }, parts);
}

export function goBack(state: PartNavigation): PartNavigation {
  if (!canGoBack(state)) return state;
  return { ...state, index: state.index - 1 };
}

export function goForward(state: PartNavigation, parts: Beat[]): PartNavigation {
  if (!canGoForward(state, parts.length)) return state;
  return refreshUnlock({ ...state, index: state.index + 1 }, parts);
}
