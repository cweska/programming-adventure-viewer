"use client";

import { useEffect, useRef, useState } from "react";
import { characterIdByName } from "../lib/campaign/party";
import { campaignData } from "../lib/campaign/registry";
import type { PartyPanel, SceneImage } from "../lib/lesson/schema";
import { publicPath } from "../lib/site";
import type { GameEvent } from "../lib/stage/bridge";
import { useReducedMotion } from "./useReducedMotion";

const STEP_MS = 350;

export type ManaEvent = Extract<GameEvent, { type: "mana" }>;
export type ManaScript = { token: number; events: ManaEvent[] };

type Row = { bar: string; mana: number; max: number };

/** The party panel: one row per member, with each mana bar the student's code draws. */
export function PartyPanelScene({
  image,
  panel,
  script,
  passed,
}: {
  image: SceneImage | undefined;
  panel: PartyPanel;
  script: ManaScript | null;
  passed: boolean;
}) {
  const [rows, setRows] = useState<Record<string, Row>>({});
  const reducedMotion = useReducedMotion();
  const timers = useRef<number[]>([]);

  useEffect(() => {
    if (!script) return;
    setRows({});
    timers.current = script.events.map((event, index) =>
      window.setTimeout(
        () => {
          const id = characterIdByName(event.name);
          if (!id) return;
          setRows((current) => ({ ...current, [id]: { bar: event.bar, mana: event.mana, max: event.max } }));
        },
        reducedMotion ? 0 : STEP_MS * (index + 1),
      ),
    );
    return () => timers.current.forEach((timer) => window.clearTimeout(timer));
  }, [script, reducedMotion]);

  return (
    <div className="party-scene" data-testid="party-scene">
      <div className="conversation-scene">
        {image ? <img className="conversation-image" src={publicPath(image.src)} alt={image.alt} /> : null}
        <ol className="mana-panel" aria-label="Party mana">
          {panel.members.map((id) => {
            const character = campaignData.characters[id];
            const row = rows[id];
            return (
              <li key={id} className="mana-row" data-testid={`mana-row-${id}`} data-filled={row ? "true" : "false"}>
                {character ? <img src={publicPath(character.portrait)} alt="" /> : null}
                <span className="mana-name">{character?.name ?? id}</span>
                <span className="mana-slot" data-testid={`mana-text-${id}`}>
                  {row ? row.bar : "Mana bar not drawn yet"}
                </span>
              </li>
            );
          })}
        </ol>
      </div>
      {passed ? (
        <p className="scene-success" data-testid="party-success" role="status">
          {panel.success}
        </p>
      ) : null}
    </div>
  );
}
