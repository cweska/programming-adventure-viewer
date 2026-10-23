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

function activityOf(id: string): Activity {
  const activity = part(id).activity;
  if (!activity) throw new Error(`${id} should be a coding part`);
  return activity;
}

function movementActivity(): Activity {
  return activityOf("program-movement");
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

const PROMPT_SOLUTION = [
  "def get_dialogue_prompt_string():",
  '    dialogue_input = "WHAT DO YOU REMEMBER ABOUT THE GREENROOM?"',
  "    dialogue_input = dialogue_input.lower()",
  "    dialogue_input = dialogue_input.capitalize()",
  "    return dialogue_input",
  "",
  "",
  "def present_dialogue_option():",
  "    dialogue = get_dialogue_prompt_string()",
  "    print_prompt(dialogue)",
  "",
].join("\n");

function optionsSolution(): string {
  return activityOf("program-dialogue-options")
    .starterCode.replace('"Write option 1 here"', '"We will help you."')
    .replace('"Write option 2 here"', '"What is the decay?"')
    .replace('"Write option 3 here"', '"Tell us about the clock."')
    .replace('"Write option 4 here"', '"We need to rest first."')
    .replace(/<option>/, '"option 1"')
    .replace(/<option>/, '"option 2"')
    .replace(/<option>/, '"option 3"')
    .replace(/<option>/, '"option 4"')
    .replace(/(speak_dialogue\("option \d"\))/g, "$1\n        make_option_green()");
}

describe("Campaign Module 1: Leylines Awaken", () => {
  it("follows the outline: story, movement and the cabin door, the cabin, the dialogue system, and Mar'tu", () => {
    expect(module?.title).toBe("Leylines Awaken");
    expect(lesson?.title).toBe("Campaign Module 1: Leylines Awaken");
    expect(module?.campaign).toEqual({ order: 1, label: "Module 1" });
    expect(lesson?.published).toBe(true);
    expect(lesson?.beats.map((beat) => beat.id)).toEqual([
      "peaceful-night",
      "humming-medallion",
      "flashover-warning",
      "program-movement",
      "cabin-interior",
      "program-dialogue-prompt",
      "program-dialogue-options",
      "mar-tu-needs-help",
    ]);
    for (const id of ["peaceful-night", "humming-medallion", "flashover-warning", "cabin-interior", "mar-tu-needs-help"]) {
      expect(part(id).editor).toBe("hidden");
      expect(part(id).activity).toBeUndefined();
      expect(part(id).board).toBeUndefined();
    }
    const board = part("program-movement").board;
    expect(board?.party).toEqual(["oogrish", "gearshift"]);
    expect(board?.features).toEqual([]);
    expect(board?.goal).toEqual({
      type: "reach",
      x: 11,
      y: 3,
      label: "the cabin door",
      enter: { after: ["mar-tu"] },
    });
    expect(movementActivity().unlocks).toEqual(["movement"]);
    expect(part("program-dialogue-prompt").conversation).toMatchObject({ speaker: "mar-tu", showOptions: false });
    expect(part("program-dialogue-options").conversation).toMatchObject({
      speaker: "mar-tu",
      responder: "oogrish",
      showOptions: true,
      promptFrom: "program-dialogue-prompt",
    });
    expect(activityOf("program-dialogue-prompt").passFeedback).toBe("Dialogue prompt implemented, well done!");
    expect(activityOf("program-dialogue-options").passFeedback).toBe("Dialogue fully implemented, well done!");
    expect(activityOf("program-dialogue-options").unlocks).toEqual(["dialogue"]);
  });

  it("keeps the outline's description text", () => {
    expect(part("peaceful-night").scene.caption).toContain("This night was a peaceful one.");
    expect(part("humming-medallion").scene.caption).toContain("It had been two weeks since he appeared in the greenroom");
    expect(part("flashover-warning").scene.caption).toContain("as they heard Mar'tu calling in their thick accent");
    expect(part("flashover-warning").scene.caption).toContain("Boys, there is another flashover coming, get inside.");
    expect(part("program-movement").scene.caption).toContain("receive input from the arrow keys");
    expect(part("cabin-interior").scene.caption).toContain("It seems like the decay is accelerating.");
    expect(part("program-dialogue-prompt").scene.caption).toContain("We'll start with the dialogue prompt.");
    expect(part("program-dialogue-options").scene.caption).toContain("dialogue response options");
    expect(part("mar-tu-needs-help").scene.caption).toBe(
      'Mar\'tu took a long exaggerated sigh and looked out the window. "We need help."',
    );
    for (const beat of lesson?.beats ?? []) {
      expect(JSON.stringify(beat)).not.toContain("Mar'Tu");
    }
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

  it("asks for Mar'tu's line, stores it in a variable, and shows it with print_prompt", () => {
    const activity = activityOf("program-dialogue-prompt");
    expect(activity.starterCode).toContain("def present_dialogue_option():\n    pass\n");
    const starter = runPythonChecks(activity.starterCode, activity.checks);
    expect(starter.checks.every((check) => !check.passed)).toBe(true);

    const result = runPythonChecks(PROMPT_SOLUTION, activity.checks);
    expect(result.ok, result.error).toBe(true);
    expect(result.checks.map((check) => check.passed)).toEqual([true, true, true]);
    expect(result.events).toEqual([{ type: "prompt", text: "What do you remember about the greenroom?" }]);

    const direct = PROMPT_SOLUTION.replace(
      "    dialogue = get_dialogue_prompt_string()\n    print_prompt(dialogue)",
      "    print_prompt(get_dialogue_prompt_string())",
    );
    const noVariable = runPythonChecks(direct, activity.checks);
    expect(noVariable.checks.map((check) => check.passed)).toEqual([true, true, false]);
    expect(noVariable.checks[2].message).toContain("in a variable first");

    const twice = runPythonChecks(PROMPT_SOLUTION.replace("    print_prompt(dialogue)", "    print_prompt(dialogue)\n    print_prompt(dialogue)"), activity.checks);
    expect(twice.checks[1].passed).toBe(false);
  });

  it("starts the response options as a syntax error until every <option> is replaced", () => {
    const activity = activityOf("program-dialogue-options");
    expect(activity.starterCode.match(/\(user\.clicked\(\) == <option>\):/g)).toHaveLength(4);
    expect(activity.starterCode).toContain("\n    if (user.clicked() == <option>):\n");
    expect(activity.starterCode.split("\n    elif ")).toHaveLength(4);
    const starter = runPythonChecks(activity.starterCode, activity.checks);
    expect(starter.ok).toBe(false);
    expect(starter.error).toMatch(/^SyntaxError/);
  });

  it("passes the response options solution and highlights each clicked option", () => {
    const activity = activityOf("program-dialogue-options");
    const result = runPythonChecks(optionsSolution(), activity.checks);
    expect(result.ok, result.error).toBe(true);
    expect(result.checks.map((check) => check.passed)).toEqual([true, true, true, true, true]);
    expect(result.events[0]).toEqual({
      type: "options",
      options: ["We will help you.", "What is the decay?", "Tell us about the clock.", "We need to rest first."],
    });
    expect(result.events.slice(1)).toEqual(
      [1, 2, 3, 4].flatMap((number) => [
        { type: "speak", option: `option ${number}` },
        { type: "highlight", option: `option ${number}` },
      ]),
    );
  });

  it("catches unchanged options, swapped conditions, and a missing or doubled make_option_green()", () => {
    const activity = activityOf("program-dialogue-options");
    const solution = optionsSolution();

    const placeholders = runPythonChecks(
      solution.replace('"We will help you."', '"Write option 1 here"'),
      activity.checks,
    );
    expect(placeholders.checks[0].passed).toBe(false);
    expect(placeholders.checks[0].message).toContain("Change option_1");

    const swapped = runPythonChecks(
      solution.replace('== "option 1"', '== "option X"').replace('== "option 2"', '== "option 1"').replace('== "option X"', '== "option 2"'),
      activity.checks,
    );
    expect(swapped.checks.map((check) => check.passed)).toEqual([true, false, false, true, true]);

    const noGreen = runPythonChecks(solution.replaceAll("\n        make_option_green()", ""), activity.checks);
    expect(noGreen.checks.slice(1).every((check) => !check.passed)).toBe(true);
    expect(noGreen.checks[1].message).toContain("make_option_green()");

    const doubled = runPythonChecks(
      solution.replace('speak_dialogue("option 3")', 'speak_dialogue("option 3")\n        make_option_green()'),
      activity.checks,
    );
    expect(doubled.checks.map((check) => check.passed)).toEqual([true, true, true, false, true]);
  });

  it("speaks to students in parts with one-sentence fail feedback", () => {
    for (const beat of lesson?.beats ?? []) {
      expect(beat.instructions.toLowerCase()).not.toMatch(/\bbeat\b/);
      expect(beat.scene.caption.toLowerCase()).not.toMatch(/\bbeat\b/);
      if (!beat.activity) continue;
      const fail = beat.activity.failFeedback.replace(/"[^"]*"/g, "");
      expect(fail.match(/[.!?]/g), beat.id).toHaveLength(1);
    }
  });
});
