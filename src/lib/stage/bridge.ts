import type { Direction } from "../game/schema";

const DIRECTIONS: readonly string[] = ["left", "right", "up", "down"];

export type StageEvent =
  | { type: "say"; text: string }
  | { type: "flare" }
  | { type: "focus"; imageId: string }
  | { type: "move"; direction: Direction }
  | ConversationEvent;

export type ConversationEvent =
  | { type: "prompt"; text: string }
  | { type: "options"; options: string[] }
  | { type: "speak"; option: string }
  | { type: "highlight"; option: string };

export type TheaterState = {
  caption: string;
  flareToken: number;
  focusedImageId: string | null;
};

export function parseStageMessage(message: unknown): StageEvent | null {
  if (!message || typeof message !== "object") return null;
  const record = message as Record<string, unknown>;
  if (record.type === "say" && typeof record.text === "string") {
    return { type: "say", text: record.text };
  }
  if (record.type === "flare") {
    return { type: "flare" };
  }
  if (record.type === "focus" && typeof record.imageId === "string" && record.imageId.length > 0) {
    return { type: "focus", imageId: record.imageId };
  }
  if (record.type === "move" && typeof record.direction === "string" && DIRECTIONS.includes(record.direction)) {
    return { type: "move", direction: record.direction as Direction };
  }
  if (record.type === "prompt" && typeof record.text === "string") {
    return { type: "prompt", text: record.text };
  }
  if (
    record.type === "options" &&
    Array.isArray(record.options) &&
    record.options.length <= 4 &&
    record.options.every((option) => typeof option === "string")
  ) {
    return { type: "options", options: [...(record.options as string[])] };
  }
  if ((record.type === "speak" || record.type === "highlight") && typeof record.option === "string") {
    return { type: record.type, option: record.option };
  }
  return null;
}

export function applyStageMessage(state: TheaterState, message: unknown): TheaterState {
  const event = parseStageMessage(message);
  if (!event) return state;
  switch (event.type) {
    case "say":
      return { ...state, caption: event.text };
    case "flare":
      return { ...state, flareToken: state.flareToken + 1 };
    case "focus":
      return { ...state, focusedImageId: event.imageId };
    default:
      return state;
  }
}

export function stageMoves(events: readonly StageEvent[]): Direction[] {
  return events.flatMap((event) => (event.type === "move" ? [event.direction] : []));
}

export function conversationEvents(events: readonly StageEvent[]): ConversationEvent[] {
  return events.filter(
    (event): event is ConversationEvent =>
      event.type === "prompt" || event.type === "options" || event.type === "speak" || event.type === "highlight",
  );
}

export function applyStageEvents(state: TheaterState, events: readonly unknown[]): TheaterState {
  return events.reduce<TheaterState>((current, event) => applyStageMessage(current, event), state);
}
