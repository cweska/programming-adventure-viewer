import { describe, expect, it } from "vitest";
import { findModule } from "./modules";
import { runPythonChecks } from "./run-checks";
import type { Activity, Beat } from "./schema";

const module = findModule("leylines-awaken");
const lesson = module?.lessons[0];

function part(id: string): Beat {
  const beat = lesson?.beats.find((item) => item.id === id);
  if (!beat) throw new Error(`missing part ${id}`);
  return beat;
}

function movementActivity(): Activity {
  const activity = part("program-movement").activity;
  if (!activity) throw new Error("program-movement should be a coding part");
  return activity;
}

const SOLUTION = [
  "def move_left():",
  '    party.move("left")',
  "",
  "",
  "def move_right():",
  '    party.move("right")',
  "",
  "",
  "def move_up():",
  '    party.move("up")',
  "",
  "",
  "def move_down():",
  '    party.move("down")',
  "",
].join("\n");

describe("Campaign Module 1: Leyline's Awaken", () => {
  it("follows the outline: three story parts, the movement program, then the walk to the cabin", () => {
    expect(module?.campaign).toEqual({ order: 1, label: "Module 1" });
    expect(lesson?.published).toBe(true);
    expect(lesson?.beats.map((beat) => beat.id)).toEqual([
      "peaceful-night",
      "humming-medallion",
      "flashover-warning",
      "program-movement",
      "beat-the-flashover",
    ]);
    for (const id of ["peaceful-night", "humming-medallion", "flashover-warning"]) {
      expect(part(id).editor).toBe("hidden");
      expect(part(id).activity).toBeUndefined();
      expect(part(id).board).toBeUndefined();
    }
    expect(part("program-movement").board?.party).toEqual(["gearshift", "oogrish"]);
    expect(part("program-movement").board?.features).toEqual([]);
    expect(movementActivity().unlocks).toEqual(["movement"]);
    expect(part("beat-the-flashover").board?.goal).toMatchObject({ type: "reach" });
  });

  it("keeps the outline's description text", () => {
    expect(part("peaceful-night").scene.caption).toContain("This night was a peaceful one.");
    expect(part("humming-medallion").scene.caption).toContain("It had been two weeks since he appeared in the greenroom");
    expect(part("flashover-warning").scene.caption).toContain("Boys, there is another flashover coming, get inside.");
    expect(part("program-movement").scene.caption).toContain("receive input from the arrow keys");
  });

  it("starts with four empty move functions that fail every check", () => {
    const activity = movementActivity();
    for (const name of ["move_left", "move_right", "move_up", "move_down"]) {
      expect(activity.starterCode).toContain(`def ${name}():\n    pass\n`);
    }
    const result = runPythonChecks(activity.starterCode, activity.checks);
    expect(result.ok).toBe(true);
    expect(result.checks.every((check) => !check.passed)).toBe(true);
    expect(result.checks[0].message).toContain('move_left() should call party.move("left").');
  });

  it("passes the reference solution and sends one step in each direction to the game screen", () => {
    const activity = movementActivity();
    const result = runPythonChecks(SOLUTION, activity.checks);
    expect(result.ok, result.error).toBe(true);
    expect(result.checks.map((check) => check.passed)).toEqual([true, true, true, true]);
    expect(result.events).toEqual([
      { type: "move", direction: "left" },
      { type: "move", direction: "right" },
      { type: "move", direction: "up" },
      { type: "move", direction: "down" },
    ]);
  });

  it("catches a swapped direction and a misspelled one", () => {
    const activity = movementActivity();
    const swapped = runPythonChecks(SOLUTION.replace('party.move("right")', 'party.move("left")'), activity.checks);
    expect(swapped.checks.map((check) => check.passed)).toEqual([true, false, true, true]);
    expect(swapped.checks[1].message).toContain('move_right() should call party.move("right").');

    const typo = runPythonChecks(SOLUTION.replace('party.move("up")', 'party.move("upp")'), activity.checks);
    expect(typo.checks[2].passed).toBe(false);
    expect(typo.checks[2].message).toContain("The party cannot move 'upp'.");
  });

  it("speaks to students in parts with one-sentence fail feedback", () => {
    for (const beat of lesson?.beats ?? []) {
      expect(beat.instructions.toLowerCase()).not.toMatch(/\bbeat\b/);
      expect(beat.scene.caption.toLowerCase()).not.toMatch(/\bbeat\b/);
    }
    const fail = movementActivity().failFeedback.replace(/"[^"]*"/g, "");
    expect(fail.match(/[.!?]/g)).toHaveLength(1);
  });
});
