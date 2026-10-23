import { existsSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { createGame } from "../game/state";
import { isWalkable } from "../game/rules";
import type { Board, Feature } from "../game/schema";
import { actorAt, firstStepToward, tileAt } from "../game/world";
import { bundledModules, studentModules } from "../lesson/modules";
import { campaignData } from "./registry";

const boards = bundledModules.flatMap((module) =>
  module.lessons.flatMap((lesson) =>
    lesson.beats.flatMap((beat) => (beat.board ? [{ module, beat, board: beat.board as Board }] : [])),
  ),
);

function publicFile(src: string): boolean {
  return existsSync(path.join("public", src.replace(/^\//, "")));
}

describe("campaign content", () => {
  it("bundles the warm-up, Module 1, and the teacher practice yard", () => {
    expect(bundledModules.map((module) => module.id)).toEqual(["emberkeep", "leylines-awaken", "training-grounds"]);
    expect(studentModules().map((module) => module.id)).toEqual(["leylines-awaken", "emberkeep"]);
  });

  it("points every character, NPC, and enemy at art that exists", () => {
    const art = [
      ...Object.values(campaignData.characters).flatMap((character) => [character.sprite, character.portrait]),
      ...Object.values(campaignData.npcs).flatMap((npc) => [npc.sprite, npc.portrait]),
      ...Object.values(campaignData.enemies).map((enemy) => enemy.sprite),
      ...bundledModules.flatMap((module) =>
        module.lessons.flatMap((lesson) => lesson.beats.flatMap((beat) => beat.scene.images.map((image) => image.src))),
      ),
    ];
    for (const src of art) expect(publicFile(src), src).toBe(true);
  });

  it("gives every character a known class", () => {
    for (const character of Object.values(campaignData.characters)) {
      expect(campaignData.classes[character.classId], character.id).toBeTruthy();
    }
  });

  it("only lets dialogue speakers be known people", () => {
    for (const tree of Object.values(campaignData.dialogues)) {
      for (const node of Object.values(tree.nodes)) {
        const known = node.speaker in campaignData.npcs || node.speaker in campaignData.characters;
        expect(known, `${tree.id}: ${node.speaker}`).toBe(true);
      }
    }
  });

  it("builds every board and keeps everyone on open ground", () => {
    expect(boards.length).toBeGreaterThan(0);
    for (const { beat, board } of boards) {
      const state = createGame(board, campaignData);
      const spots = new Set<string>();
      for (const actor of state.actors) {
        expect(isWalkable(tileAt(state, actor.x, actor.y)), `${beat.id}: ${actor.id}`).toBe(true);
        const key = `${actor.x},${actor.y}`;
        expect(spots.has(key), `${beat.id}: two actors on ${key}`).toBe(false);
        spots.add(key);
      }
    }
  });

  it("makes every goal reachable", () => {
    for (const { beat, board } of boards) {
      const state = createGame(board, campaignData);
      const leader = state.actors[0];
      const goal = board.goal;
      if (!goal) continue;
      if (goal.type === "reach") {
        expect(isWalkable(tileAt(state, goal.x, goal.y)), beat.id).toBe(true);
        expect(actorAt(state, goal.x, goal.y), beat.id).toBeUndefined();
        const step = firstStepToward(
          state,
          leader,
          (position) => position.x === goal.x && position.y === goal.y,
          (position) => isWalkable(tileAt(state, position.x, position.y)) && !actorAt(state, position.x, position.y),
        );
        expect(step, `${beat.id} goal is reachable`).not.toBeNull();
      }
      if (goal.type === "talk") {
        const target = board.actors.find((actor) => actor.id === goal.actor);
        expect(target?.kind, beat.id).toBe("npc");
        expect(target?.dialogue, beat.id).toBeTruthy();
        expect(board.features, beat.id).toContain("dialogue");
      }
      if (goal.type === "defeat") {
        expect(board.actors.some((actor) => actor.kind === "enemy"), beat.id).toBe(true);
        expect(board.features, beat.id).toContain("melee");
      }
    }
  });

  it("only lets students use a feature after a coding part has built it", () => {
    const built = new Set<Feature>();
    for (const module of studentModules().filter((item) => item.campaign)) {
      for (const lesson of module.lessons.filter((item) => item.published)) {
        for (const beat of lesson.beats) {
          for (const feature of beat.board?.features ?? []) {
            expect(built.has(feature), `${module.id}/${beat.id} uses ${feature} before it is programmed`).toBe(true);
          }
          for (const feature of beat.activity?.unlocks ?? []) built.add(feature);
        }
      }
    }
    expect(built.has("movement")).toBe(true);
  });

  it("hides the editor on campaign story and gameplay parts", () => {
    const module = bundledModules.find((item) => item.id === "leylines-awaken");
    for (const beat of module?.lessons[0].beats ?? []) {
      expect(beat.editor === "hidden", beat.id).toBe(!beat.activity);
    }
  });
});
