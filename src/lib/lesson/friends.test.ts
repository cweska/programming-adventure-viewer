import { describe, expect, it } from "vitest";
import { findModule } from "./modules";
import { runPythonChecks } from "./run-checks";
import type { Activity, Beat } from "./schema";
import { activitySetup, castCode, skillRollCode } from "./setup";

const module = findModule("friends-in-low-places");
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

function run(id: string, code: string, calls: string[] = []) {
  const activity = activityOf(id);
  return runPythonChecks(code, activity.checks, { setup: activitySetup(activity), calls });
}

function passes(result: ReturnType<typeof run>): boolean[] {
  return result.checks.map((check) => check.passed);
}

const STORY = [
  "three-knocks",
  "trap-door",
  "bomb-shell-arrives",
  "the-resonance-array",
  "ley-clock",
  "map-of-tor",
  "the-burst",
  "chalk-wall",
  "greenroom",
  "red-clock",
  "raise-the-barrier",
  "thirty-two-hours",
];

const SKILL_SOLUTION = [
  "import random",
  "",
  "",
  "def perform_roll(die_size):",
  "    return random.randint(1, die_size)",
  "",
  "",
  "def strength_check(roll):",
  "    required_roll = 12",
  "    return roll >= required_roll",
  "",
  "",
  "def dexterity_check(roll):",
  "    required_roll = 15",
  "    return roll >= required_roll",
  "",
  "",
  "def investigation_check(roll):",
  "    required_roll = 9",
  "    return roll >= required_roll",
  "",
].join("\n");

const SPELL_ANSWER = activityOf("mana-bars").background?.[0].fallback ?? "";
const MANA_ANSWER = activityOf("hold-the-barrier").background?.[1].fallback ?? "";
const CAST_ANSWER = activityOf("hold-the-barrier")
  .starterCode.replace(
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

describe("Campaign Module 2: Friends In Low Places", () => {
  it("follows the outline: sixteen parts, four of them coding parts", () => {
    expect(module?.title).toBe("Friends In Low Places");
    expect(lesson?.title).toBe("Campaign Module 2: Friends In Low Places");
    expect(module?.campaign).toEqual({ order: 2, label: "Module 2" });
    expect(lesson?.published).toBe(true);
    expect(lesson?.beats.map((beat) => beat.id)).toEqual([
      "three-knocks",
      "trap-door",
      "skill-checks",
      "bomb-shell-arrives",
      "the-resonance-array",
      "ley-clock",
      "map-of-tor",
      "the-burst",
      "chalk-wall",
      "greenroom",
      "red-clock",
      "raise-the-barrier",
      "spell-book",
      "mana-bars",
      "hold-the-barrier",
      "thirty-two-hours",
    ]);
    for (const id of STORY) {
      expect(part(id).editor, id).toBe("hidden");
      expect(part(id).activity, id).toBeUndefined();
      expect(part(id).board, id).toBeUndefined();
    }
    expect(part("skill-checks").skillCheck?.options.map((option) => option.label)).toEqual([
      "Force it open",
      "Finesse the latch with a shim",
      "Find an easier way",
    ]);
    expect(part("skill-checks").skillCheck?.helper).toEqual({ npc: "mar-tu", line: "Oh just let me do it." });
    for (const option of part("skill-checks").skillCheck?.options ?? []) {
      expect(option.successText.length, option.id).toBeGreaterThan(20);
      expect(option.failureText.length, option.id).toBeGreaterThan(20);
      expect(option.successText, option.id).not.toBe(option.failureText);
    }
    expect(part("skill-checks").skillCheck?.options[0]).toMatchObject({
      id: "strength",
      successText:
        "You slipped your fingers in the gap and used all your strength pulling up on the hatch. You heard a pop as it flung open.",
      failureText: "You slipped your fingers in the gap and used all your strength pulling up on the hatch. It won't budge.",
    });
    expect(part("skill-checks").skillCheck?.options[2]).toMatchObject({
      id: "intelligence",
      failureText: "You investigate the surface of the trap door but don't notice anything useful.",
    });
    expect(part("spell-book").spellBook).toMatchObject({ spell: "Strengthen Magic", manaCost: 10, requiredAffinity: 8 });
    expect(part("mana-bars").partyPanel?.members).toEqual(["oogrish", "gearshift", "bomb-shell", "lucky"]);
    const board = part("hold-the-barrier").board;
    expect(board?.party).toEqual(["oogrish", "gearshift", "bomb-shell", "lucky"]);
    expect(board?.goal).toEqual({ type: "barrier" });
    expect(board?.casting?.mana).toEqual({ oogrish: 18, gearshift: 15, "bomb-shell": 14, lucky: 19 });
    expect(activityOf("hold-the-barrier").unlocks).toEqual(["magic"]);
    expect(activityOf("spell-book").passFeedback).toBe("Spell book ready, well done!");
    expect(activityOf("mana-bars").passFeedback).toBe("Mana bars working, well done!");
  });

  it("keeps the outline's description text", () => {
    expect(part("three-knocks").scene.caption).toBe(
      "A knocking from underneath their feet jarred Mar'tu and the others.",
    );
    expect(part("trap-door").scene.caption).toContain("Looks like the latch is sticking again.");
    expect(part("skill-checks").scene.caption).toContain("In RPGs, a skill check is something our character needs to do");
    expect(part("ley-clock").scene.caption).toContain("It is a Ley Clock.");
    expect(part("chalk-wall").scene.caption).toContain("The decay is accelerating.");
    expect(part("greenroom").scene.caption).toContain('"Greenroom, Interior,"');
    expect(part("raise-the-barrier").scene.caption).toContain('Mar\'tu didn\'t even turn around. "Existing."');
    expect(part("thirty-two-hours").scene.caption).toContain('"Thirty-two hours," he said.');
    expect(part("trap-door").scene.caption).toContain("Could one of you get it open for me?");
    expect(part("bomb-shell-arrives").scene.caption).toContain("the scent of ozone and humidity");
    expect(part("bomb-shell-arrives").scene.caption).toContain('"The feeling is mutual."');
    expect(part("the-resonance-array").scene.caption).toContain("has been spiking for over an hour");
    expect(part("ley-clock").scene.caption).toContain("Once again, it is not a compass.");
    expect(part("ley-clock").scene.caption).toContain("It does not show direction.");
    expect(part("map-of-tor").scene.caption).toContain("like fault lines in volcanic planets");
    expect(part("greenroom").scene.caption).toContain("relatively normal days on their home planets");
    expect(part("greenroom").scene.images[0].alt).toContain("white room");
    expect(part("red-clock").scene.caption).toContain("The clock usually turned yellow during a burst.");
    expect(part("raise-the-barrier").scene.caption).toContain("will not hold another large burst using my strength alone");
    for (const beat of lesson?.beats ?? []) {
      const text = JSON.stringify(beat);
      expect(text).not.toContain("Mar'Tu");
      expect(text).not.toContain("RPG's");
      expect(text).not.toMatch(/wookie/i);
    }
  });

  describe("Part 3: skill checks", () => {
    const activity = () => activityOf("skill-checks");

    it("starts with every check failing", () => {
      const result = run("skill-checks", activity().starterCode);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([false, false, false, false]);
      expect(result.checks[0].message).toContain("random.randint(1, die_size)");
    });

    it("passes a solution with the student's own required rolls", () => {
      const result = run("skill-checks", SKILL_SOLUTION);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([true, true, true, true]);
    });

    it("catches a fixed roll, a required roll left at 0, a backwards comparison, and one that never succeeds", () => {
      const fixed = run("skill-checks", SKILL_SOLUTION.replace("return random.randint(1, die_size)", "return 7"));
      expect(passes(fixed)).toEqual([false, true, true, true]);

      const zero = run("skill-checks", SKILL_SOLUTION.replace("required_roll = 12", "required_roll = 0"));
      expect(passes(zero)).toEqual([true, false, true, true]);
      expect(zero.checks[1].message).toContain("from 2 to 20");

      const backwards = run("skill-checks", SKILL_SOLUTION.replace("return roll >= required_roll", "return roll <= required_roll"));
      expect(passes(backwards)).toEqual([true, false, true, true]);
      expect(backwards.checks[1].message).toContain("fail on low rolls and succeed on high rolls");

      const never = run("skill-checks", SKILL_SOLUTION.replace("required_roll = 15", "required_roll = 25"));
      expect(passes(never)).toEqual([true, true, false, true]);
      expect(never.checks[2].message).toContain("never succeeds");
    });

    it("rolls a d20 through the student's own check when an option is clicked", () => {
      const options = part("skill-checks").skillCheck?.options ?? [];
      const result = run("skill-checks", SKILL_SOLUTION, options.map((option) => skillRollCode(option)));
      expect(result.calls).toHaveLength(3);
      result.calls.forEach((call, index) => {
        expect(call.ok, call.error).toBe(true);
        expect(call.events).toHaveLength(1);
        const [roll] = call.events;
        expect(roll).toMatchObject({ type: "roll", skill: options[index].id, required: [12, 15, 9][index] });
        expect(roll.roll).toBeGreaterThanOrEqual(1);
        expect(roll.roll).toBeLessThanOrEqual(20);
        expect(roll.success).toBe((roll.roll as number) >= (roll.required as number));
      });
    });
  });

  describe("Part 13: the spell book", () => {
    it("starts with the outline's code and fails every check", () => {
      const activity = activityOf("spell-book");
      expect(activity.starterCode).toContain('        "spell_function": None,\n');
      expect(activity.starterCode).toContain("    # Store the spell in spell_book, using spell_name as the key\n");
      expect(activity.party?.members).toEqual(["oogrish", "gearshift", "bomb-shell", "lucky"]);
      const result = run("spell-book", activity.starterCode);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([false, false, false, false]);
    });

    it("passes the answer key", () => {
      const result = run("spell-book", SPELL_ANSWER);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([true, true, true, true]);
    });

    it("catches a placeholder left in, a hard-coded value, and a spell book that is wiped", () => {
      const placeholder = run("spell-book", SPELL_ANSWER.replace('"spell_function": spell_function', '"spell_function": None'));
      expect(passes(placeholder)).toEqual([true, false, true, false]);

      const hardCoded = run("spell-book", SPELL_ANSWER.replace('"mana_cost": mana_cost', '"mana_cost": 10'));
      expect(passes(hardCoded)).toEqual([true, false, true, true]);
      expect(hardCoded.checks[1].message).toContain("Use the mana_cost parameter");

      const wiped = run(
        "spell-book",
        SPELL_ANSWER.replace("    spell_book[spell_name] = spell", "    spell_book.clear()\n    spell_book[spell_name] = spell"),
      );
      expect(passes(wiped)).toEqual([true, true, false, true]);
    });
  });

  describe("Part 14: mana bars", () => {
    it("builds on the spell book and starts with every check failing", () => {
      const activity = activityOf("mana-bars");
      expect(activity.background?.map((piece) => piece.from)).toEqual(["spell-book"]);
      const result = run("mana-bars", activity.starterCode);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([false, false, false, false]);
    });

    it("passes the answer key and draws every party member's bar", () => {
      const result = run("mana-bars", MANA_ANSWER);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([true, true, true, true]);
      expect(result.events.filter((event) => event.type === "mana").slice(0, 4)).toEqual([
        { type: "mana", name: "Master Oogrish", bar: `Mana [${"█".repeat(18)}] 18/18`, mana: 18, max: 18 },
        { type: "mana", name: "Gearshift", bar: `Mana [${"█".repeat(15)}${"░".repeat(5)}] 15/20`, mana: 15, max: 20 },
        { type: "mana", name: "Bomb Shell", bar: `Mana [${"█".repeat(14)}${"░".repeat(10)}] 14/24`, mana: 14, max: 24 },
        { type: "mana", name: "Lucky", bar: `Mana [${"█".repeat(19)}${"░".repeat(7)}] 19/26`, mana: 19, max: 26 },
      ]);
    });

    it("shows print_mana() already finished and a hint above every line to change", () => {
      const starter = activityOf("mana-bars").starterCode;
      expect(starter.startsWith("def print_mana(caster, mana_bar):\n")).toBe(true);
      expect(starter).toContain("    party.show_mana_bar(caster, mana_bar)\n");
      expect(starter).toContain("already finished");
      const lines = starter.split("\n");
      for (const target of ['    filled = "█" * 0', '    empty = "░" * 0', "    pass"]) {
        const index = lines.indexOf(target);
        expect(index, target).toBeGreaterThan(0);
        expect(lines[index - 1].trim().startsWith("#"), target).toBe(true);
      }
      expect(lines[lines.indexOf('    filled = "█" * 0') - 1]).toContain('caster["mana"]');
      expect(lines[lines.indexOf('    empty = "░" * 0') - 1]).toContain('caster["max_mana"] - caster["mana"]');
      expect(lines[lines.indexOf("    pass") - 1]).toContain("Replace pass");
      expect(MANA_ANSWER.startsWith("def print_mana(caster, mana_bar):\n")).toBe(true);
    });

    it("passes when the student fills in the starter's lines and keeps the comments", () => {
      const edited = activityOf("mana-bars")
        .starterCode.replace('"█" * 0', '"█" * caster["mana"]')
        .replace('"░" * 0', '"░" * (caster["max_mana"] - caster["mana"])')
        .replace("    pass\n", "    mana_bar = get_mana_bar(caster)\n    print_mana(caster, mana_bar)\n");
      const result = run("mana-bars", edited);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([true, true, true, true]);
    });

    it("still draws the bars if the student deletes the finished print_mana()", () => {
      const withoutHelper = MANA_ANSWER.replace(/^def print_mana[\s\S]*?\n\n\n/, "");
      expect(withoutHelper).not.toContain("def print_mana");
      const result = run("mana-bars", withoutHelper);
      expect(passes(result)).toEqual([true, true, true, true]);
      expect(
        result.events
          .filter((event) => event.type === "mana")
          .slice(0, 4)
          .map((event) => event.name),
      ).toEqual(["Master Oogrish", "Gearshift", "Bomb Shell", "Lucky"]);
    });

    it("catches a wrong bar and a bar that skips the variable", () => {
      const wrong = run("mana-bars", MANA_ANSWER.replace('(caster["max_mana"] - caster["mana"])', 'caster["max_mana"]'));
      expect(passes(wrong)).toEqual([false, false, true, true]);

      const direct = run(
        "mana-bars",
        MANA_ANSWER.replace("    mana_bar = get_mana_bar(caster)\n    print_mana(caster, mana_bar)", "    print_mana(caster, get_mana_bar(caster))"),
      );
      expect(passes(direct)).toEqual([true, true, true, false]);
      expect(direct.checks[3].message).toContain("in a variable first");
    });
  });

  describe("Part 15: hold the barrier", () => {
    it("builds on the spell book and mana bars and starts with every check failing", () => {
      const activity = activityOf("hold-the-barrier");
      expect(activity.background?.map((piece) => piece.from)).toEqual(["spell-book", "mana-bars"]);
      expect(activity.starterCode).toContain('spell = caster["spell_book"][spell_name]\n');
      expect(CAST_ANSWER).not.toContain("    pass\n");
      const result = run("hold-the-barrier", activity.starterCode);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([false, false, false, false, false, false]);
    });

    it("passes the answer key", () => {
      const result = run("hold-the-barrier", CAST_ANSWER);
      expect(result.ok, result.error).toBe(true);
      expect(passes(result)).toEqual([true, true, true, true, true, true]);
    });

    it("catches <= in place of <, a hard-coded cost, and a forgotten show_mana()", () => {
      const lessOrEqual = run("hold-the-barrier", CAST_ANSWER.replace('caster["mana"] < spell["mana_cost"]', 'caster["mana"] <= spell["mana_cost"]'));
      expect(passes(lessOrEqual)).toEqual([true, true, true, true, false, true]);

      const hardCoded = run("hold-the-barrier", CAST_ANSWER.replace('caster["mana"] - spell["mana_cost"]', 'caster["mana"] - 10'));
      expect(passes(hardCoded)).toEqual([false, true, true, true, false, false]);

      const noBar = run("hold-the-barrier", CAST_ANSWER.replace("        show_mana(caster)\n", ""));
      expect(passes(noBar)).toEqual([true, false, true, true, true, true]);
    });

    it("casts once per party member, then gives the student's own not-enough-mana message", () => {
      const calls = [0, 1, 2, 3, 1].map((index) => castCode(index, "Strengthen Magic"));
      const result = run("hold-the-barrier", CAST_ANSWER, calls);
      expect(result.ok, result.error).toBe(true);
      const names = ["Master Oogrish", "Gearshift", "Bomb Shell", "Lucky"];
      const left = [8, 5, 4, 9];
      result.calls.slice(0, 4).forEach((call, index) => {
        expect(call.ok, call.error).toBe(true);
        expect(call.events).toEqual([
          { type: "cast", name: names[index] },
          expect.objectContaining({ type: "mana", name: names[index], mana: left[index] }),
        ]);
      });
      expect(result.calls[4].events).toEqual([
        { type: "prompt", text: "Gearshift doesn't have enough mana to cast Strengthen Magic." },
      ]);
    });

    it("uses the student's own earlier code when there is some", () => {
      const activity = activityOf("hold-the-barrier");
      const ownBar = MANA_ANSWER.replace('"Mana ["', '"MP ["');
      const setup = activitySetup(activity, { "mana-bars": ownBar });
      expect(setup).toContain('"MP ["');
      expect(setup).toContain(SPELL_ANSWER);
      const result = runPythonChecks(CAST_ANSWER, activity.checks, { setup, calls: [castCode(0, "Strengthen Magic")] });
      expect(result.calls[0].events[1]).toMatchObject({ type: "mana", bar: `MP [${"█".repeat(8)}${"░".repeat(10)}] 8/18` });
    });
  });
});
