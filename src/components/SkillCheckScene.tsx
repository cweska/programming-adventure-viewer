"use client";

import { useEffect, useRef, useState } from "react";
import { campaignData } from "../lib/campaign/registry";
import type { SceneImage, SkillCheck } from "../lib/lesson/schema";
import { publicPath } from "../lib/site";
import { useReducedMotion } from "./useReducedMotion";

export type RollEvent = { roll: number; success: boolean; required: number };
export type RollOutcome = { kind: "roll"; roll: RollEvent } | { kind: "no-session" } | { kind: "error" };

type Phase = "idle" | "rolling" | "result" | "helper" | "open";

const TUMBLE_MS = 1100;
const RESULT_MS = 2500;
const HELPER_MS = 2200;

export function SkillCheckScene({
  image,
  skillCheck,
  canRoll,
  opened,
  onRoll,
  onOpened,
}: {
  image: SceneImage | undefined;
  skillCheck: SkillCheck;
  canRoll: boolean;
  opened: boolean;
  onRoll: (option: SkillCheck["options"][number]) => Promise<RollOutcome>;
  onOpened: () => void;
}) {
  const [phase, setPhase] = useState<Phase>(opened ? "open" : "idle");
  const [chosen, setChosen] = useState<string | null>(null);
  const [face, setFace] = useState(20);
  const [roll, setRoll] = useState<RollEvent | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const reducedMotion = useReducedMotion();
  const timers = useRef<number[]>([]);
  const onOpenedRef = useRef(onOpened);
  useEffect(() => {
    onOpenedRef.current = onOpened;
  });

  useEffect(() => () => timers.current.forEach((timer) => window.clearTimeout(timer)), []);

  function later(ms: number, action: () => void) {
    timers.current.push(window.setTimeout(action, reducedMotion ? 0 : ms));
  }

  function open() {
    setPhase("open");
    onOpenedRef.current();
  }

  async function choose(option: SkillCheck["options"][number]) {
    if (phase !== "idle") return;
    if (!canRoll) {
      setNotice("Skill checks haven't been programmed yet. Finish the code below and press Run.");
      return;
    }
    setNotice(null);
    setChosen(option.id);
    setPhase("rolling");
    const outcome = await onRoll(option);
    if (outcome.kind !== "roll") {
      setPhase("idle");
      setChosen(null);
      setNotice(
        outcome.kind === "no-session"
          ? "Press Run to roll with your own code."
          : "Your code stopped during the roll. Read the message in the console.",
      );
      return;
    }
    const result = outcome.roll;
    if (!reducedMotion) {
      const spin = window.setInterval(() => setFace(1 + Math.floor(Math.random() * 20)), 70);
      timers.current.push(window.setTimeout(() => window.clearInterval(spin), TUMBLE_MS));
    }
    later(TUMBLE_MS, () => {
      setFace(result.roll);
      setRoll(result);
      setPhase("result");
      later(RESULT_MS, () => {
        if (result.success) {
          open();
          return;
        }
        setPhase("helper");
        later(HELPER_MS, open);
      });
    });
  }

  const helper = campaignData.npcs[skillCheck.helper.npc];
  const shown = phase === "open" ? skillCheck.openImage : image;
  const option = skillCheck.options.find((item) => item.id === chosen);
  const narration = roll && option && phase !== "rolling" ? (roll.success ? option.successText : option.failureText) : null;
  return (
    <div className="skill-check" data-testid="skill-check" data-phase={phase}>
      <div className="skill-scene">
        {shown ? <img className="conversation-image" src={publicPath(shown.src)} alt={shown.alt} /> : null}
        {phase === "helper" && helper ? (
          <div className="skill-helper" data-testid="skill-helper">
            <img className="skill-helper-sprite" src={publicPath(helper.sprite)} alt={helper.name} />
            <p className="skill-helper-line">
              <strong>{helper.name}:</strong> {skillCheck.helper.line}
            </p>
          </div>
        ) : null}
        {phase === "rolling" || phase === "result" || phase === "helper" || (phase === "open" && roll) ? (
          <div className="skill-roll" data-testid="skill-roll" data-roll={roll?.roll ?? ""}>
            <div className={phase === "rolling" ? "die is-tumbling" : "die"} aria-hidden="true">
              <svg viewBox="0 0 100 100">
                <polygon points="50,4 92,28 92,72 50,96 8,72 8,28" />
                <polygon points="50,22 80,72 20,72" fill="none" />
                <path d="M50 4 L50 22 M8 28 L50 22 L92 28 M8 28 L20 72 M92 28 L80 72 M8 72 L20 72 M92 72 L80 72 M20 72 L50 96 L80 72" fill="none" />
                <text x="50" y="62" textAnchor="middle">
                  {face}
                </text>
              </svg>
            </div>
            <p className="skill-roll-text" role="status" data-testid="skill-result">
              {phase === "rolling"
                ? `Rolling for ${option?.label.toLowerCase() ?? "the check"}…`
                : roll
                  ? `Rolled ${roll.roll}, needed ${roll.required}. ${roll.success ? "Success!" : "Not this time."}`
                  : ""}
            </p>
          </div>
        ) : null}
        {phase === "open" ? (
          <p className="scene-success" data-testid="skill-success" role="status">
            {skillCheck.success}
          </p>
        ) : null}
      </div>
      {narration ? (
        <p
          className="skill-narration"
          data-testid="skill-narration"
          data-outcome={roll?.success ? "success" : "failure"}
          role="status"
        >
          {narration}
        </p>
      ) : null}
      {phase !== "open" ? (
        <ol className="skill-options">
          {skillCheck.options.map((item, index) => (
            <li key={item.id}>
              <button
                type="button"
                className={chosen === item.id ? "conversation-option is-selected" : "conversation-option"}
                data-testid={`skill-option-${item.id}`}
                disabled={phase !== "idle"}
                onClick={() => void choose(item)}
              >
                <span className="option-key">{index + 1}</span> {item.label}
              </button>
            </li>
          ))}
        </ol>
      ) : null}
      {notice ? (
        <p className="game-notice" data-testid="skill-notice" role="status">
          {notice}
        </p>
      ) : null}
    </div>
  );
}
