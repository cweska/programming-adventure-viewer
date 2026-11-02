import { describe, expect, it } from "vitest";
import { campaignData } from "../campaign/registry";
import { characterIdByName } from "../campaign/party";
import { findModule } from "../lesson/modules";
import { runPythonChecks } from "../lesson/run-checks";
import { activitySetup, castCode } from "../lesson/setup";
import type { Board } from "./schema";
import { castActions } from "./casting";
import { playActions } from "./reducer";
import { createGame } from "./state";
import type { GameState } from "./types";
import { parseStageMessage, type StageEvent } from "../stage/bridge";

const part = findModule("friends-in-low-places")?.lessons[0].beats.find((beat) => beat.id === "hold-the-barrier");

const CAST_ANSWER = (part?.activity?.starterCode ?? "").replace(
  /\n {4}# 1\.[\s\S]*\n {4}pass\n$/,
  [
    "",
    '    if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:',
    '        print_prompt(caster["character_name"] + " isn\'t skilled enough to cast " + spell_name + ".")',
    '    elif caster["mana"] < spell["mana_cost"]:',
    '        print_prompt(caster["character_name"] + " doesn\'t have enough mana to cast " + spell_name + ".")',
    "    else:",
    '        spell["spell_function"](caster)',
    '        caster["mana"] = caster["mana"] - spell["mana_cost"]',
    "        show_mana(caster)",
    "",
  ].join("\n"),
);

function clickEvents(indexes: number[]): StageEvent[][] {
  const activity = part?.activity;
  if (!activity) throw new Error("missing Part 15");
  const result = runPythonChecks(CAST_ANSWER, activity.checks, {
    setup: activitySetup(activity),
    calls: indexes.map((index) => castCode(index, "Strengthen Magic")),
  });
  expect(result.ok, result.error).toBe(true);
  return result.calls.map((call) => call.events.flatMap((event) => parseStageMessage(event) ?? []));
}

function play(state: GameState, events: StageEvent[]): GameState {
  return playActions(state, castActions(events, (name) => characterIdByName(name)));
}

describe("casting on the barrier board", () => {
  it("maps cast, mana, and prompt events to game actions and skips strangers", () => {
    const idByName = (name: string) => characterIdByName(name);
    expect(
      castActions(
        [
          { type: "cast", name: "Lucky" },
          { type: "mana", name: "Lucky", bar: "", mana: 9, max: 26 },
          { type: "prompt", text: "Nope." },
          { type: "cast", name: "Nobody" },
          { type: "move", direction: "left" },
        ],
        idByName,
      ),
    ).toEqual([
      { type: "cast", actorId: "lucky" },
      { type: "manaChanged", actorId: "lucky", mana: 9, max: 26 },
      { type: "prompt", text: "Nope." },
    ]);
  });

  it("plays the student's own casts until the barrier locks, then the wave passes", () => {
    const board = part?.board as Board;
    let state = createGame(board, campaignData, ["magic"]);
    expect(state.mana).toMatchObject({ oogrish: { mana: 18, max: 18 }, lucky: { mana: 19, max: 26 } });
    const clicks = clickEvents([0, 1, 1, 2, 3]);

    state = play(state, clicks[0]);
    expect(state.barrier?.level).toBe(1);
    expect(state.mana.oogrish).toEqual({ mana: 8, max: 18 });
    expect(state.manaDrop).toMatchObject({ actorId: "oogrish", amount: 10 });
    expect(state.speech).toMatchObject({ actorId: "oogrish", text: "Steady, now." });

    state = play(state, clicks[1]);
    state = play(state, clicks[2]);
    expect(state.prompt?.text).toBe("Gearshift doesn't have enough mana to cast Strengthen Magic.");
    expect(state.mana.gearshift).toEqual({ mana: 5, max: 20 });
    expect(state.barrier?.level).toBe(2);

    state = play(state, clicks[3]);
    state = play(state, clicks[4]);
    expect(state.barrier).toMatchObject({ level: 4, locked: true });
    expect(state.goalMet).toBe(false);

    for (let step = 0; step < 40 && !state.goalMet; step += 1) state = playActions(state, [{ type: "waveStep" }]);
    expect(state.barrier?.done).toBe(true);
    expect(state.goalMet).toBe(true);
  });
});
