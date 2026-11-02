import { partySetupCode } from "../campaign/party";
import type { Activity, SkillCheck } from "./schema";

export type PassedCode = Readonly<Record<string, string>>;

/**
 * Code that runs before a part's own code: the party for Python to read, then
 * each earlier part this one builds on. An earlier part uses the student's own
 * passing code when there is some, or the answer key that ships with the part.
 */
export function activitySetup(activity: Activity | undefined, passed: PassedCode = {}): string {
  if (!activity) return "";
  const pieces: string[] = [];
  if (activity.party) pieces.push(partySetupCode(activity.party.members, activity.party.mana));
  for (const piece of activity.background ?? []) pieces.push(passed[piece.from] ?? piece.fallback);
  return pieces.map((piece) => (piece.endsWith("\n") ? piece : `${piece}\n`)).join("\n");
}

export function skillRollCode(option: SkillCheck["options"][number]): string {
  return [
    "_roll = perform_roll(20)",
    `show_roll(${JSON.stringify(option.id)}, _roll, ${option.check}(_roll), _required_roll(${option.check}))`,
    "",
  ].join("\n");
}

export function castCode(index: number, spell: string): string {
  return `cast_spell(party.members[${Math.trunc(index)}], ${JSON.stringify(spell)})\n`;
}
