"use client";

import { useEffect, useMemo, useReducer, useRef, useState, type KeyboardEvent } from "react";
import { characterIdByName } from "../../lib/campaign/party";
import { campaignData } from "../../lib/campaign/registry";
import { insideBarrier } from "../../lib/game/barrier";
import { castActions } from "../../lib/game/casting";
import { activeCombatant } from "../../lib/game/combat";
import { currentNode } from "../../lib/game/dialogue";
import { commandForKey } from "../../lib/game/input";
import { gameReducer } from "../../lib/game/reducer";
import type { Board, Direction, Feature } from "../../lib/game/schema";
import { createGame } from "../../lib/game/state";
import type { Actor, GameState } from "../../lib/game/types";
import { actorById } from "../../lib/game/world";
import { publicPath } from "../../lib/site";
import type { StageEvent } from "../../lib/stage/bridge";
import { useReducedMotion } from "../useReducedMotion";
import { MapTiles, TILE } from "./TileArt";

const STEP_MS = 260;
const WAVE_MS = 170;
const WAVE_PAUSE_MS = 900;

export type BoardScript = { token: number; moves: Direction[] };

type BoardProps = {
  board: Board;
  features: Feature[];
  script: BoardScript | null;
  autoFocus: boolean;
  compact: boolean;
  lockedHint: { features: Feature[]; text: string } | null;
  onGoal: () => void;
  /** Runs the student's cast_spell() for party member `index`. Resolves to null when there is no live code yet. */
  onCast?: (index: number) => Promise<StageEvent[] | null>;
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
  if (goal.type === "barrier") return "The barrier held!";
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
  onCast,
  onRetry,
}: Omit<BoardProps, "script"> & { pendingMoves: Direction[]; onRetry: () => void }) {
  const [state, dispatch] = useReducer(gameReducer, undefined, () => createGame(board, campaignData, features));
  const [focused, setFocused] = useState(false);
  const surface = useRef<HTMLDivElement>(null);
  const reducedMotion = useReducedMotion();
  const onGoalRef = useRef(onGoal);
  const onCastRef = useRef(onCast);
  useEffect(() => {
    onGoalRef.current = onGoal;
    onCastRef.current = onCast;
  });
  const alive = useRef(true);
  const castBusy = useRef(false);
  useEffect(() => {
    alive.current = true;
    return () => {
      alive.current = false;
    };
  }, []);

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

  const barrier = state.barrier;
  const magicOn = state.features.includes("magic");
  const waving = Boolean(barrier?.locked && !barrier.done);
  useEffect(() => {
    if (!waving) return;
    const delay = reducedMotion ? 30 : barrier?.wave === 0 ? WAVE_PAUSE_MS : WAVE_MS;
    const timer = window.setTimeout(() => dispatch({ type: "waveStep" }), delay);
    return () => window.clearTimeout(timer);
  }, [waving, state.tick, reducedMotion, barrier?.wave]);

  async function cast(index: number) {
    if (!barrier || barrier.locked || castBusy.current) return;
    const id = board.party[index];
    if (!id) return;
    if (!magicOn) {
      dispatch({ type: "notice", kind: "magic-locked" });
      return;
    }
    castBusy.current = true;
    try {
      const events = (await onCastRef.current?.(index)) ?? null;
      if (!alive.current) return;
      if (events === null) {
        dispatch({ type: "notice", kind: "cast-run" });
        return;
      }
      for (const action of castActions(events, (name) => characterIdByName(name))) dispatch(action);
    } finally {
      castBusy.current = false;
    }
  }

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const command = commandForKey(event.key);
    if (!command) return;
    if (command.type === "release") {
      surface.current?.blur();
      return;
    }
    event.preventDefault();
    if (barrier) {
      if (command.type === "move") dispatch({ type: "notice", kind: magicOn ? "cast-hint" : "magic-locked" });
      if (command.type === "option") void cast(command.index);
      return;
    }
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

  const castingNow = Boolean(barrier);
  const label = castingNow
    ? `${state.map.name}. Click a party member or press 1 to 4 to cast. Escape leaves the map.`
    : `${state.map.name}. Arrow keys or W A S D move. Tab switches the leader. Escape leaves the map.`;

  return (
    <div
      className={compact ? "game is-compact" : "game"}
      data-testid="game"
      data-mode={state.mode}
      data-tick={state.tick}
      data-barrier-level={barrier ? barrier.level : undefined}
      data-barrier-locked={barrier ? String(barrier.locked) : undefined}
      data-barrier-done={barrier ? String(barrier.done) : undefined}
    >
      <div
        ref={surface}
        className={focused ? "game-surface is-focused" : "game-surface"}
        tabIndex={0}
        role="application"
        aria-label={label}
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
          {barrier ? <SkyAlert width={width} height={height} calm={barrier.done} /> : null}
          {barrier ? <BarrierDome state={state} /> : null}
          {state.actors.map((actor) => (
            <ActorToken
              key={actor.id}
              actor={actor}
              state={state}
              onClick={
                castingNow && board.party.includes(actor.id)
                  ? () => {
                      surface.current?.focus({ preventScroll: true });
                      void cast(board.party.indexOf(actor.id));
                    }
                  : undefined
              }
            />
          ))}
          {barrier ? <CastEffects state={state} /> : null}
          {barrier ? (
            <BarrierFireflies state={state} width={width} height={height} />
          ) : state.map.sky === "night" ? (
            <Fireflies width={width} height={height} />
          ) : null}
          {barrier ? <LightWall state={state} width={width} height={height} /> : null}
        </svg>
        {state.prompt ? (
          <div className="dialogue-box cast-prompt" data-testid="cast-prompt" role="status" key={state.prompt.id}>
            <div className="dialogue-body">
              <p>{state.prompt.text}</p>
            </div>
          </div>
        ) : null}
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

      {castingNow ? null : (
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
      )}

      <div className="game-hud">
        <ul className="party-panel" aria-label="Party">
          {castingNow
            ? heroes.map((hero, index) => (
                <li key={hero.id} className="party-member is-caster" data-testid={`party-member-${hero.id}`}>
                  <button
                    type="button"
                    className="cast-button"
                    data-testid={`cast-${hero.id}`}
                    disabled={Boolean(barrier?.locked)}
                    onClick={() => {
                      surface.current?.focus({ preventScroll: true });
                      void cast(board.party.indexOf(hero.id));
                    }}
                  >
                    <span className="option-key">{index + 1}</span>
                    <img src={publicPath(hero.sprite)} alt="" />
                    <span className="cast-body">
                      <span className="party-name">{hero.name}</span>
                      <ManaBar actor={hero} state={state} />
                    </span>
                  </button>
                </li>
              ))
            : heroes.map((hero) => {
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

function ActorToken({ actor, state, onClick }: { actor: Actor; state: GameState; onClick?: () => void }) {
  const active = activeCombatant(state);
  const highlighted =
    state.mode === "combat" ? active?.id === actor.id : actor.kind === "hero" && state.leader === actor.id;
  const mana = state.mana[actor.id];
  const showHealth = !mana && actor.kind !== "npc" && (state.mode === "combat" || actor.hp < actor.maxHp);
  const casting = state.castFx?.actorId === actor.id ? state.castFx : null;
  const color = campaignData.characters[actor.ref]?.spellColor ?? "#c89bff";
  const flip = actor.facing === "left" ? `translate(${TILE} 0) scale(-1 1)` : undefined;
  const classes = ["actor", `actor-${actor.kind}`];
  if (actor.down) classes.push("is-down");
  if (actor.hidden) classes.push("is-hidden");
  if (onClick) classes.push("is-clickable");
  return (
    <g
      className={classes.join(" ")}
      onClick={onClick}
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
      {casting ? (
        <ellipse key={`glow-${casting.id}`} className="cast-glow" cx={TILE / 2} cy={TILE / 2} rx={26} ry={28} fill={color} />
      ) : null}
      <g key={casting ? `lift-${casting.id}` : "still"} className={casting ? "cast-lift" : undefined}>
        <g transform={flip}>
          <image href={publicPath(actor.sprite)} x={2} y={0} width={TILE - 4} height={TILE - 4} />
        </g>
      </g>
      {mana ? (
        <g transform="translate(6 -4)" data-testid={`mana-over-${actor.id}`} data-mana={mana.mana} data-max={mana.max}>
          <rect width={TILE - 12} height={5} rx={2} fill="#1b1b1b" />
          <rect width={Math.max(0, ((TILE - 12) * mana.mana) / Math.max(1, mana.max))} height={5} rx={2} fill="#9b6cff" />
        </g>
      ) : null}
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

function ManaBar({ actor, state }: { actor: Actor; state: GameState }) {
  const mana = state.mana[actor.id];
  if (!mana) return null;
  const percent = Math.round((Math.max(0, mana.mana) / Math.max(1, mana.max)) * 100);
  return (
    <span className="health mana" aria-label={`${actor.name} mana ${mana.mana} of ${mana.max}`}>
      <span className="health-track">
        <span className="health-fill mana-fill" style={{ width: `${percent}%` }} />
      </span>
      <span className="health-text" data-testid={`mana-${actor.id}`}>
        Mana {mana.mana}/{mana.max}
      </span>
    </span>
  );
}

function SkyAlert({ width, height, calm }: { width: number; height: number; calm: boolean }) {
  return (
    <rect
      className={calm ? "sky-alert is-calm" : "sky-alert"}
      data-testid="sky-alert"
      width={width}
      height={height}
      pointerEvents="none"
    />
  );
}

function barrierBox(state: GameState) {
  const barrier = state.barrier;
  if (!barrier) return null;
  return {
    x: barrier.x0 * TILE,
    y: barrier.y0 * TILE,
    width: (barrier.x1 - barrier.x0 + 1) * TILE,
    height: (barrier.y1 - barrier.y0 + 1) * TILE,
  };
}

function waveX(state: GameState): number {
  const barrier = state.barrier;
  if (!barrier || !barrier.locked) return -TILE * 0.5;
  return (barrier.wave - 1) * TILE;
}

function BarrierDome({ state }: { state: GameState }) {
  const barrier = state.barrier;
  const box = barrierBox(state);
  if (!barrier || !box) return null;
  const front = waveX(state);
  const flaring = barrier.locked && !barrier.done && front + TILE >= box.x && front <= box.x + box.width;
  const classes = ["barrier"];
  if (barrier.locked) classes.push("is-locked");
  if (flaring) classes.push("is-flaring");
  return (
    <rect
      className={classes.join(" ")}
      data-testid="barrier"
      data-level={barrier.level}
      x={box.x + 3}
      y={box.y + 3}
      width={box.width - 6}
      height={box.height - 6}
      rx={28}
      style={{ fillOpacity: 0.05 + barrier.level * 0.05, strokeWidth: 2 + barrier.level * 1.5 }}
      pointerEvents="none"
    />
  );
}

function LightWall({ state, width, height }: { state: GameState; width: number; height: number }) {
  const barrier = state.barrier;
  const box = barrierBox(state);
  if (!barrier || !box || barrier.done) return null;
  const x = waveX(state);
  const outside = `M0 0 H${width} V${height} H0 Z M${box.x} ${box.y} V${box.y + box.height} H${box.x + box.width} V${box.y} Z`;
  return (
    <g pointerEvents="none" data-testid="light-wall" data-x={barrier.locked ? barrier.wave - 1 : -1}>
      <clipPath id="outside-barrier">
        <path d={outside} clipRule="evenodd" />
      </clipPath>
      <g clipPath="url(#outside-barrier)">
        <rect className="light-wall-glow" x={x - TILE * 0.6} y={0} width={TILE * 1.6} height={height} />
        <rect className={barrier.locked ? "light-wall is-rolling" : "light-wall"} x={x} y={0} width={TILE * 0.5} height={height} />
      </g>
    </g>
  );
}

const BARRIER_FLIES = [
  { x: 0.6, y: 1.4 },
  { x: 2.3, y: 4.5 },
  { x: 4.2, y: 2.4 },
  { x: 5.5, y: 6.6 },
  { x: 1.4, y: 8.2 },
  { x: 3.6, y: 7.6 },
  { x: 6.4, y: 9.1 },
  { x: 9.5, y: 8.4 },
  { x: 12.3, y: 9.2 },
  { x: 14.6, y: 7.7 },
  { x: 10.4, y: 0.6 },
  { x: 13.2, y: 4.8 },
];

function BarrierFireflies({ state, width, height }: { state: GameState; width: number; height: number }) {
  const front = waveX(state) + TILE * 0.5;
  return (
    <g aria-hidden="true" pointerEvents="none">
      {BARRIER_FLIES.map((spot, index) => {
        const cx = Math.min(width - 4, spot.x * TILE);
        const cy = Math.min(height - 4, spot.y * TILE);
        const safe = insideBarrier(state, Math.floor(spot.x), Math.floor(spot.y));
        const out = Boolean(state.barrier?.locked) && !safe && cx <= front;
        return (
          <circle
            key={index}
            className={out ? "firefly is-out" : "firefly"}
            data-testid="barrier-firefly"
            data-out={out ? "true" : "false"}
            cx={cx}
            cy={cy}
            r={3}
            style={{ animationDelay: `${(index % 5) * -1.1}s` }}
          />
        );
      })}
    </g>
  );
}

function CastEffects({ state }: { state: GameState }) {
  const box = barrierBox(state);
  const fx = state.castFx;
  const caster = fx ? actorById(state, fx.actorId) : undefined;
  const drop = state.manaDrop;
  const dropActor = drop ? actorById(state, drop.actorId) : undefined;
  const speech = state.speech;
  const speaker = speech ? actorById(state, speech.actorId) : undefined;
  const width = state.map.width * TILE;
  return (
    <g pointerEvents="none">
      {fx && caster && box ? (
        <path
          key={`arc-${fx.id}`}
          className="spark-arc"
          data-testid="spark-arc"
          d={`M${caster.x * TILE + TILE / 2} ${caster.y * TILE + 8} Q ${caster.x * TILE + TILE * 1.4} ${box.y - TILE * 0.6}, ${
            caster.x * TILE + TILE / 2
          } ${box.y + 6}`}
          stroke={campaignData.characters[caster.ref]?.spellColor ?? "#c89bff"}
        />
      ) : null}
      {drop && dropActor ? (
        <text
          key={`drop-${drop.id}`}
          className="mana-drop"
          data-testid="mana-drop"
          x={dropActor.x * TILE + TILE / 2}
          y={dropActor.y * TILE - 8}
          textAnchor="middle"
        >
          -{drop.amount} mana
        </text>
      ) : null}
      {speech && speaker ? (
        <SpeechBubble key={`speech-${speech.id}`} text={speech.text} x={speaker.x * TILE + TILE / 2} y={speaker.y * TILE - 22} width={width} />
      ) : null}
    </g>
  );
}

function SpeechBubble({ text, x, y, width }: { text: string; x: number; y: number; width: number }) {
  const bubbleWidth = Math.min(width - 8, text.length * 6.6 + 18);
  const left = Math.max(4, Math.min(width - bubbleWidth - 4, x - bubbleWidth / 2));
  const top = Math.max(4, y - 26);
  return (
    <g className="speech" data-testid="speech-bubble">
      <rect x={left} y={top} width={bubbleWidth} height={24} rx={8} />
      <path d={`M${x - 6} ${top + 24} L ${x} ${top + 32} L ${x + 6} ${top + 24} Z`} />
      <text x={left + bubbleWidth / 2} y={top + 16} textAnchor="middle">
        {text}
      </text>
    </g>
  );
}
