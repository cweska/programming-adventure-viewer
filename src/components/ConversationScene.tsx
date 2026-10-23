"use client";

import { useEffect, useRef, useState } from "react";
import { campaignData } from "../lib/campaign/registry";
import type { Conversation, SceneImage } from "../lib/lesson/schema";
import { publicPath } from "../lib/site";
import type { ConversationEvent } from "../lib/stage/bridge";
import { useReducedMotion } from "./useReducedMotion";

const STEP_MS = 420;
const SLOTS = 4;

export type ConversationScript = { token: number; events: ConversationEvent[] };

type View = {
  prompt: string;
  options: string[];
  selected: string | null;
  reply: string | null;
};

function personName(id: string): string {
  return campaignData.npcs[id]?.name ?? campaignData.characters[id]?.name ?? id;
}

function personPortrait(id: string): string | null {
  return campaignData.npcs[id]?.portrait ?? campaignData.characters[id]?.portrait ?? null;
}

function optionText(view: View, option: string): string {
  const match = /^option (\d)$/.exec(option.trim());
  const index = match ? Number(match[1]) - 1 : -1;
  return view.options[index] ?? option;
}

function applyEvent(view: View, event: ConversationEvent): View {
  switch (event.type) {
    case "prompt":
      return { ...view, prompt: event.text };
    case "options":
      return { ...view, options: event.options.slice(0, SLOTS), selected: null, reply: null };
    case "highlight":
      return { ...view, selected: event.option };
    case "speak":
      return { ...view, reply: optionText(view, event.option) };
  }
}

export function ConversationScene({
  images,
  conversation,
  prompt,
  script,
  canChoose,
}: {
  images: SceneImage[];
  conversation: Conversation;
  prompt: string;
  script: ConversationScript | null;
  canChoose: boolean;
}) {
  const [view, setView] = useState<View>({ prompt, options: [], selected: null, reply: null });
  const [notice, setNotice] = useState<string | null>(null);
  const reducedMotion = useReducedMotion();
  const played = useRef(false);
  const timers = useRef<number[]>([]);

  useEffect(() => {
    if (!played.current) setView((current) => ({ ...current, prompt }));
  }, [prompt]);

  useEffect(() => {
    if (!script) return;
    played.current = true;
    setNotice(null);
    setView({ prompt, options: [], selected: null, reply: null });
    timers.current = script.events.map((event, index) =>
      window.setTimeout(
        () => setView((current) => applyEvent(current, event)),
        reducedMotion ? 0 : STEP_MS * index,
      ),
    );
    return () => timers.current.forEach((timer) => window.clearTimeout(timer));
  }, [script, reducedMotion]);

  function choose(index: number) {
    if (!conversation.showOptions) return;
    if (!canChoose) {
      setNotice("Choosing an answer hasn't been programmed yet. Finish the code below and press Run.");
      return;
    }
    const text = view.options[index];
    if (!text) return;
    timers.current.forEach((timer) => window.clearTimeout(timer));
    setNotice(null);
    setView((current) => ({ ...current, selected: `option ${index + 1}`, reply: text }));
  }

  const portrait = personPortrait(conversation.speaker);
  const image = images[0];
  return (
    <div className="conversation" data-testid="conversation">
      <div className="conversation-scene">
        {image ? <img className="conversation-image" src={publicPath(image.src)} alt={image.alt} /> : null}
        <div className="conversation-panel">
          <div className="conversation-box" data-testid="conversation-box">
            {portrait ? <img className="conversation-portrait" src={publicPath(portrait)} alt="" /> : null}
            <div className="conversation-lines">
              <p className="conversation-speaker" data-testid="conversation-speaker">
                {personName(conversation.speaker)}
              </p>
              <p className="conversation-prompt" data-testid="conversation-prompt">
                {view.prompt}
              </p>
              {view.reply ? (
                <p className="conversation-reply" data-testid="conversation-reply">
                  <strong>{personName(conversation.responder)}:</strong> {view.reply}
                </p>
              ) : null}
            </div>
          </div>
          <ol
            className={conversation.showOptions ? "conversation-options" : "conversation-options is-reserved"}
            aria-hidden={conversation.showOptions ? undefined : true}
          >
            {Array.from({ length: SLOTS }, (_, index) => {
              const key = `option ${index + 1}`;
              const selected = view.selected === key;
              return (
                <li key={key}>
                  {conversation.showOptions ? (
                    <button
                      type="button"
                      className={selected ? "conversation-option is-selected" : "conversation-option"}
                      data-testid={`conversation-option-${index + 1}`}
                      data-selected={selected ? "true" : "false"}
                      onClick={() => choose(index)}
                    >
                      <span className="option-key">{index + 1}</span> {view.options[index] ?? ""}
                    </button>
                  ) : (
                    <span className="conversation-option is-empty" />
                  )}
                </li>
              );
            })}
          </ol>
        </div>
      </div>
      {notice ? (
        <p className="game-notice" data-testid="conversation-notice" role="status">
          {notice}
        </p>
      ) : null}
    </div>
  );
}
