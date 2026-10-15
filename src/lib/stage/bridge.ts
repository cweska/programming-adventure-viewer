export type StageEvent =
  | { type: "say"; text: string }
  | { type: "flare" }
  | { type: "focus"; imageId: string };

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

export function applyStageEvents(state: TheaterState, events: readonly unknown[]): TheaterState {
  return events.reduce<TheaterState>((current, event) => applyStageMessage(current, event), state);
}
