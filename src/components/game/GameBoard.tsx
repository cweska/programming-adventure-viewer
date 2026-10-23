"use client";

import { useEffect, useMemo, useReducer, useRef, useState, type KeyboardEvent } from "react";
import { campaignData } from "../../lib/campaign/registry";
import { activeCombatant } from "../../lib/game/combat";
import { currentNode } from "../../lib/game/dialogue";
import { commandForKey } from "../../lib/game/input";
import { gameReducer } from "../../lib/game/reducer";
import type { Board, Direction, Feature } from "../../lib/game/schema";
import { createGame } from "../../lib/game/state";
import type { Actor, GameState } from "../../lib/game/types";
import { actorById } from "../../lib/game/world";
import { publicPath } from "../../lib/site";
import { useReducedMotion } from "../useReducedMotion";
import { MapTiles, TILE } from "./TileArt";

const STEP_MS = 260;

export type BoardScript = { token: number; moves: Direction[] };

type BoardProps = {
  board: Board;
  features: Feature[];
  script: BoardScript | null;
  autoFocus: boolean;
  compact: boolean;
  lockedHint: { features: Feature[]; text: string } | null;
  onGoal: () => void;
};

export function GameBoard(props: BoardProps) {
  const [session, setSession] = useState({ key: 0, moves: [] as Direction[] });
  const lastToken = useRef<number | null>(null);

  useEffect(() => {
    if (!props.script || props.script.token === lastToken.current) return;
    lastToken.current = props.script.token;
    const moves = props.script.moves;
    setSession((current) => ({ key: current.key + 1, moves }));
  }, [props.script]);

  return (
    <BoardSession
      key={session.key}
      {...props}
      pendingMoves={session.moves}
      autoFocus={props.autoFocus || session.key > 0}
      onRetry={() => setSession((current) => ({ key: current.key + 1, moves: [] }))}
    />
  );
}

function goalText(state: GameState): string {
  const goal = state.goal;
  if (!goal) return "";
  if (goal.type === "reach") return `You made it to ${goal.label}!`;
  if (goal.type === "talk") return `You finished talking with ${actorById(state, goal.actor)?.name ?? "them"}.`;
  return "Every enemy is down.";
}

function BoardSession({
  board,
  features,
  pendingMoves,
  autoFocus,
  compact,
  lockedHint,
  onGoal,
  onRetry,
}: Omit<BoardProps, "script"> & { pendingMoves: Direction[]; onRetry: () => void }) {
  const [state, dispatch] = useReducer(gameReducer, undefined, () => createGame(board, campaignData, features));
  const [focused, setFocused] = useState(false);
  const surface = useRef<HTMLDivElement>(null);
  const reducedMotion = useReducedMotion();
  const onGoalRef = useRef(onGoal);
  useEffect(() => {
    onGoalRef.current = onGoal;
  });

  const featureKey = features.join(",");
  useEffect(() => {
    dispatch({ type: "setFeatures", features: featureKey ? (featureKey.split(",") as Feature[]) : [] });
  }, [featureKey]);

  useEffect(() => {
    if (autoFocus) surface.current?.focus({ preventScroll: true });
  }, [autoFocus]);

  useEffect(() => {
    if (pendingMoves.length === 0) return;
    const timers = pendingMoves.map((direction, index) =>
      window.setTimeout(() => dispatch({ type: "scriptedMove", direction }), STEP_MS * (index + 1)),
    );
    return () => timers.forEach((timer) => window.clearTimeout(timer));
  }, [pendingMoves]);

  useEffect(() => {
    if (state.goalMet) onGoalRef.current();
  }, [state.goalMet]);

  const active = activeCombatant(state);
  const enemyTurn = state.mode === "combat" && active?.kind === "enemy";
  useEffect(() => {
    if (!enemyTurn) return;
    const timer = window.setTimeout(() => dispatch({ type: "enemyStep" }), reducedMotion ? 30 : STEP_MS);
    return () => window.clearTimeout(timer);
  }, [enemyTurn, state.tick, reducedMotion]);

  const cutscenePlaying = state.mode === "cutscene" && !state.cutscene?.doorClosed;
  useEffect(() => {
    if (!cutscenePlaying) return;
    const timer = window.setTimeout(() => dispatch({ type: "cutsceneStep" }), reducedMotion ? 30 : STEP_MS * 1.5);
    return () => window.clearTimeout(timer);
  }, [cutscenePlaying, state.tick, reducedMotion]);

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const command = commandForKey(event.key);
    if (!command) return;
    if (command.type === "release") {
      surface.current?.blur();
      return;
    }
    event.preventDefault();
    switch (command.type) {
      case "move":
        dispatch({ type: "move", direction: command.direction });
        return;
      case "swap":
        dispatch({ type: "swapLeader" });
        return;
      case "confirm":
        if (state.mode === "dialogue") dispatch({ type: "advanceDialogue" });
        else if (state.mode === "combat") dispatch({ type: "endTurn" });
        return;
      case "option":
        dispatch({ type: "choose", index: command.index });
        return;
    }
  }

  const heroes = state.party.flatMap((id) => {
    const actor = actorById(state, id);
    return actor ? [actor] : [];
  });
  const width = state.map.width * TILE;
  const height = state.map.height * TILE;
  const node = currentNode(state);
  const speaker = state.dialogue ? speakerFor(node?.speaker ?? "", actorById(state, state.dialogue.actorId)) : null;
  const notice = state.notice
    ? `${state.notice.text}${
        lockedHint?.features.some((feature) => state.notice?.kind === `${feature}-locked`) ? ` ${lockedHint.text}` : ""
      }`
    : null;

  return (
    <div className={compact ? "game is-compact" : "game"} data-testid="game" data-mode={state.mode} data-tick={state.tick}>
      <div
        ref={surface}
        className={focused ? "game-surface is-focused" : "game-surface"}
        tabIndex={0}
        role="application"
        aria-label={`${state.map.name}. Arrow keys or W A S D move. Tab switches the leader. Escape leaves the map.`}
        data-testid="board"
        onKeyDown={onKeyDown}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        onMouseDown={() => surface.current?.focus({ preventScroll: true })}
      >
        <svg viewBox={`0 0 ${width} ${height}`} className="game-map" aria-hidden="true">
          <MapTiles tiles={state.map.tiles} sky={state.map.sky} />
          {state.goal?.type === "reach" && !state.goalMet && state.mode !== "cutscene" ? (
            <g transform={`translate(${state.goal.x * TILE} ${state.goal.y * TILE})`} data-testid="goal-marker">
              <rect className="goal-marker" x={3} y={3} width={TILE - 6} height={TILE - 6} rx={6} />
            </g>
          ) : null}
          {state.cutscene?.doorClosed ? (
            <g
              transform={`translate(${state.cutscene.door.x * TILE} ${state.cutscene.door.y * TILE})`}
              data-testid="door-closed"
            >
              <rect x={8} y={0} width={32} height={48} fill="#6b4528" stroke="#2a190d" strokeWidth={4} />
              <path d="M8 16 H40 M8 32 H40" stroke="#4a2f1a" strokeWidth={3} />
              <circle cx={34} cy={26} r={2.5} fill="#c9a24a" />
            </g>
          ) : null}
          {state.actors.map((actor) => (
            <ActorToken key={actor.id} actor={actor} state={state} />
          ))}
          {state.map.sky === "night" ? <Fireflies width={width} height={height} /> : null}
        </svg>
        {state.mode === "dialogue" && node ? (
          <div
            className="dialogue-box"
            data-testid="dialogue-box"
            role="dialog"
            aria-label={`Talking with ${speaker?.name ?? "someone"}`}
          >
            {speaker?.portrait ? <img className="dialogue-portrait" src={publicPath(speaker.portrait)} alt="" /> : null}
            <div className="dialogue-body">
              <p className="dialogue-speaker" data-testid="dialogue-speaker">
                {speaker?.name}
              </p>
              <p className="dialogue-text" data-testid="dialogue-text">
                {node.text}
              </p>
              {node.options ? (
                <ol className="dialogue-options">
                  {node.options.map((option, index) => (
                    <li key={option.text}>
                      <button
                        type="button"
                        data-testid={`dialogue-option-${index + 1}`}
                        onClick={() => {
                          dispatch({ type: "choose", index });
                          surface.current?.focus({ preventScroll: true });
                        }}
                      >
                        <span className="option-key">{index + 1}</span> {option.text}
                      </button>
                    </li>
                  ))}
                </ol>
              ) : (
                <button
                  type="button"
                  data-testid="dialogue-continue"
                  onClick={() => {
                    dispatch({ type: "advanceDialogue" });
                    surface.current?.focus({ preventScroll: true });
                  }}
                >
                  Continue (Enter)
                </button>
              )}
            </div>
          </div>
        ) : null}
        {!focused ? (
          <p className="focus-hint" data-testid="focus-hint">
            Click the map to play
          </p>
        ) : null}
      </div>

      <div className="touch-pad" aria-label="Touch controls">
        {(["up", "left", "down", "right"] as const).map((direction) => (
          <button
            key={direction}
            type="button"
            className={`pad-${direction}`}
            aria-label={`Move ${direction}`}
            onClick={() => dispatch({ type: "move", direction })}
          >
            {{ up: "↑", left: "←", down: "↓", right: "→" }[direction]}
          </button>
        ))}
        <button type="button" className="pad-swap" onClick={() => dispatch({ type: "swapLeader" })}>
          Switch leader
        </button>
      </div>

      <div className="game-hud">
        <ul className="party-panel" aria-label="Party">
          {heroes.map((hero) => {
            const isActive = state.mode === "combat" ? active?.id === hero.id : state.leader === hero.id;
            return (
              <li
                key={hero.id}
                className={isActive ? "party-member is-active" : "party-member"}
                data-testid={`party-member-${hero.id}`}
                data-active={isActive ? "true" : "false"}
              >
                <img src={publicPath(hero.sprite)} alt="" />
                <div>
                  <p className="party-name">
                    {hero.name}
                    {state.mode !== "combat" && state.leader === hero.id ? <span className="badge">Leader</span> : null}
                  </p>
                  <HealthBar actor={hero} />
                </div>
              </li>
            );
          })}
        </ul>
        <div className="game-status">
          {state.mode === "combat" && state.combat && active ? (
            <div className="turn-row">
              <p
                className="turn-indicator"
                data-testid="turn-indicator"
                data-active={active.id}
                data-kind={active.kind}
              >
                Round {state.combat.round}: <strong>{active.name}</strong>
                {active.kind === "hero" ? `'s turn, ${state.combat.movesLeft} steps left` : " is acting"}
              </p>
              <button
                type="button"
                data-testid="end-turn"
                disabled={active.kind !== "hero"}
                onClick={() => {
                  dispatch({ type: "endTurn" });
                  surface.current?.focus({ preventScroll: true });
                }}
              >
                End turn (Space)
              </button>
            </div>
          ) : null}
          {state.combatResult === "victory" ? (
            <p className="combat-result" data-testid="combat-result">
              Victory!
            </p>
          ) : null}
          {state.mode === "defeat" ? (
            <div className="turn-row">
              <p className="combat-result is-defeat" data-testid="combat-result">
                Your party was knocked out.
              </p>
              <button type="button" data-testid="retry" onClick={onRetry}>
                Try again
              </button>
            </div>
          ) : null}
          {state.goalMet ? (
            <p className="goal-met" data-testid="goal-met">
              {goalText(state)}
            </p>
          ) : null}
          {notice ? (
            <p className="game-notice" data-testid="game-notice" role="status">
              {notice}
            </p>
          ) : null}
          {state.log.length > 0 ? (
            <ol className="combat-log" data-testid="combat-log" aria-live="polite">
              {state.log.slice(-6).map((line, index) => (
                <li key={`${state.log.length - 6 + index}`}>{line}</li>
              ))}
            </ol>
          ) : null}
        </div>
      </div>
    </div>
  );
}

function speakerFor(id: string, fallback: Actor | undefined): { name: string; portrait: string | null } {
  const npc = campaignData.npcs[id];
  if (npc) return { name: npc.name, portrait: npc.portrait };
  const character = campaignData.characters[id];
  if (character) return { name: character.name, portrait: character.portrait };
  return { name: fallback?.name ?? id, portrait: fallback?.sprite ?? null };
}

function HealthBar({ actor }: { actor: Actor }) {
  const percent = Math.round((actor.hp / actor.maxHp) * 100);
  return (
    <div className="health" aria-label={`${actor.name} health ${actor.hp} of ${actor.maxHp}`}>
      <div className="health-track">
        <div className="health-fill" style={{ width: `${percent}%` }} />
      </div>
      <span className="health-text">
        HP {actor.hp}/{actor.maxHp}
      </span>
    </div>
  );
}

function ActorToken({ actor, state }: { actor: Actor; state: GameState }) {
  const active = activeCombatant(state);
  const highlighted =
    state.mode === "combat" ? active?.id === actor.id : actor.kind === "hero" && state.leader === actor.id;
  const showHealth = actor.kind !== "npc" && (state.mode === "combat" || actor.hp < actor.maxHp);
  const flip = actor.facing === "left" ? `translate(${TILE} 0) scale(-1 1)` : undefined;
  const classes = ["actor", `actor-${actor.kind}`];
  if (actor.down) classes.push("is-down");
  if (actor.hidden) classes.push("is-hidden");
  return (
    <g
      className={classes.join(" ")}
      style={{ transform: `translate(${actor.x * TILE}px, ${actor.y * TILE}px)` }}
      data-testid={`actor-${actor.id}`}
      data-kind={actor.kind}
      data-x={actor.x}
      data-y={actor.y}
      data-hp={actor.hp}
      data-down={actor.down ? "true" : "false"}
      data-hidden={actor.hidden ? "true" : "false"}
      data-facing={actor.facing}
    >
      {highlighted ? <ellipse cx={TILE / 2} cy={TILE - 6} rx={20} ry={7} className="actor-ring" /> : null}
      <ellipse cx={TILE / 2} cy={TILE - 5} rx={14} ry={4} fill="#000000" opacity={0.3} />
      <g transform={flip}>
        <image href={publicPath(actor.sprite)} x={2} y={0} width={TILE - 4} height={TILE - 4} />
      </g>
      {showHealth ? (
        <g transform="translate(6 -2)">
          <rect width={TILE - 12} height={5} rx={2} fill="#1b1b1b" />
          <rect
            width={Math.max(0, ((TILE - 12) * actor.hp) / actor.maxHp)}
            height={5}
            rx={2}
            fill={actor.kind === "enemy" ? "#e0533d" : "#5fd16b"}
          />
        </g>
      ) : null}
    </g>
  );
}

function Fireflies({ width, height }: { width: number; height: number }) {
  const spots = useMemo(
    () =>
      Array.from({ length: 9 }, (_, index) => ({
        x: ((index * 97) % 100) / 100,
        y: ((index * 53 + 17) % 100) / 100,
        delay: (index % 5) * -1.1,
      })),
    [],
  );
  return (
    <g aria-hidden="true">
      {spots.map((spot, index) => (
        <circle
          key={index}
          className="firefly"
          cx={spot.x * width}
          cy={spot.y * height}
          r={3}
          style={{ animationDelay: `${spot.delay}s` }}
        />
      ))}
    </g>
  );
}
