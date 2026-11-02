import type {
  Character,
  CharacterClass,
  Dialogue,
  Direction,
  Enemy,
  Feature,
  GameMap,
  Goal,
  Npc,
  Tile,
} from "./schema";

export type CampaignData = {
  characters: Record<string, Character>;
  classes: Record<string, CharacterClass>;
  npcs: Record<string, Npc>;
  enemies: Record<string, Enemy>;
  maps: Record<string, GameMap>;
  dialogues: Record<string, Dialogue>;
};

export type ActorKind = "hero" | "npc" | "enemy";

export type Actor = {
  id: string;
  kind: ActorKind;
  ref: string;
  name: string;
  sprite: string;
  x: number;
  y: number;
  facing: "left" | "right";
  hp: number;
  maxHp: number;
  defense: number;
  attackBonus: number;
  damageDie: number;
  damageBonus: number;
  speed: number;
  dexterity: number;
  attackText: string;
  downText: string;
  aggroRange: number;
  dialogue: string | null;
  down: boolean;
  hidden: boolean;
};

export type DialogueState = {
  actorId: string;
  treeId: string;
  nodeId: string;
};

export type CombatState = {
  order: string[];
  turn: number;
  round: number;
  movesLeft: number;
  attacked: boolean;
};

export type NoticeKind =
  | "movement-locked"
  | "dialogue-locked"
  | "melee-locked"
  | "nothing-to-say"
  | "no-moves"
  | "not-your-turn"
  | "magic-locked"
  | "cast-hint"
  | "cast-run";

export type Notice = { kind: NoticeKind; text: string; id: number };

export type GameMode = "explore" | "dialogue" | "combat" | "defeat" | "cutscene";

export type CutsceneState = {
  door: { x: number; y: number };
  queue: string[];
  doorClosed: boolean;
};

export type BarrierState = {
  x0: number;
  x1: number;
  y0: number;
  y1: number;
  level: number;
  casters: string[];
  locked: boolean;
  wave: number;
  done: boolean;
};

export type ManaState = { mana: number; max: number };

export type GameState = {
  map: { id: string; name: string; sky: "night" | "day"; width: number; height: number; tiles: Tile[][] };
  actors: Actor[];
  party: string[];
  leader: string;
  features: Feature[];
  mode: GameMode;
  dialogue: DialogueState | null;
  dialogues: Record<string, Dialogue>;
  combat: CombatState | null;
  cutscene: CutsceneState | null;
  barrier: BarrierState | null;
  mana: Record<string, ManaState>;
  castLines: Record<string, string>;
  speech: { actorId: string; text: string; id: number } | null;
  castFx: { actorId: string; id: number } | null;
  manaDrop: { actorId: string; amount: number; id: number } | null;
  prompt: { text: string; id: number } | null;
  combatResult: "victory" | "defeat" | null;
  goal: Goal | null;
  goalMet: boolean;
  talkedTo: string[];
  rng: number;
  log: string[];
  notice: Notice | null;
  tick: number;
};

export type GameAction =
  | { type: "move"; direction: Direction }
  | { type: "scriptedMove"; direction: Direction }
  | { type: "swapLeader" }
  | { type: "choose"; index: number }
  | { type: "advanceDialogue" }
  | { type: "endTurn" }
  | { type: "enemyStep" }
  | { type: "cutsceneStep" }
  | { type: "cast"; actorId: string }
  | { type: "manaChanged"; actorId: string; mana: number; max: number }
  | { type: "prompt"; text: string }
  | { type: "waveStep" }
  | { type: "notice"; kind: NoticeKind }
  | { type: "setFeatures"; features: Feature[] }
  | { type: "clearNotice" };
