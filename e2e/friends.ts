import { expect, type Page } from "@playwright/test";
import { pythonReady, replaceEditor } from "./editor";

export function skillSolution(seed: number | null = null): string {
  return [
    "import random",
    ...(seed === null ? [] : [`random.seed(${seed})`]),
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
}

export const SPELL_SOLUTION = [
  "def strengthen_magic(caster):",
  "    reinforce_barrier(caster)",
  "",
  "",
  "def add_spell(spell_book, spell_name, mana_cost, required_affinity, spell_function):",
  "    spell = {",
  '        "mana_cost": mana_cost,',
  '        "required_affinity": required_affinity,',
  '        "spell_function": spell_function,',
  "    }",
  "    spell_book[spell_name] = spell",
  "",
  "",
  "for member in party.members:",
  '    add_spell(member["spell_book"], "Strengthen Magic", 10, 8, strengthen_magic)',
  "",
].join("\n");

export const MANA_SOLUTION = [
  "def get_mana_bar(caster):",
  '    filled = "█" * caster["mana"]',
  '    empty = "░" * (caster["max_mana"] - caster["mana"])',
  '    return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])',
  "",
  "",
  "def show_mana(caster):",
  "    mana_bar = get_mana_bar(caster)",
  "    print_mana(caster, mana_bar)",
  "",
  "",
  "for member in party.members:",
  "    show_mana(member)",
  "",
].join("\n");

export const CAST_SOLUTION = [
  "def cast_spell(caster, spell_name):",
  '    if spell_name not in caster["spell_book"]:',
  '        print_prompt(caster["character_name"] + " doesn\'t know " + spell_name + ".")',
  "        return",
  '    spell = caster["spell_book"][spell_name]',
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
].join("\n");

export function bar(mana: number, max: number): string {
  return `Mana [${"█".repeat(mana)}${"░".repeat(max - mana)}] ${mana}/${max}`;
}

export async function solveFriends(page: Page, code: string, feedback: string) {
  await pythonReady(page);
  await replaceEditor(page, code);
  await page.getByTestId("run").click();
  await expect(page.getByTestId("feedback")).toContainText(feedback);
}

export async function openFriendsPart(page: Page, part: 1 | 3 | 13 | 14 | 15 | 16) {
  await page.goto("/play/friends-in-low-places");
  await expect(page.getByTestId("part-label")).toHaveText("Part 1 of 16");
  if (part === 1) return;
  await page.getByTestId("continue").click();
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 3 of 16");
  if (part === 3) return;
  await solveFriends(page, skillSolution(), "Your skill checks work.");
  await page.getByTestId("skill-option-strength").click();
  await expect(page.getByTestId("skill-success")).toHaveText("Door opened!");
  for (let count = 0; count < 10; count += 1) await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 13 of 16");
  if (part === 13) return;
  await solveFriends(page, SPELL_SOLUTION, "Spell book ready, well done!");
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 14 of 16");
  if (part === 14) return;
  await solveFriends(page, MANA_SOLUTION, "Mana bars working, well done!");
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 15 of 16");
  if (part === 15) return;
  await solveFriends(page, CAST_SOLUTION, "Casting works!");
  for (const id of ["oogrish", "gearshift", "bomb-shell", "lucky"]) await page.getByTestId(`cast-${id}`).click();
  await expect(page.getByTestId("goal-met")).toHaveText("The barrier held!");
  await page.getByTestId("continue").click();
  await expect(page.getByTestId("part-label")).toHaveText("Part 16 of 16");
}
