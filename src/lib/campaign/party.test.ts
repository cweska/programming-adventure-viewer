import { describe, expect, it } from "vitest";
import { runPythonChecks } from "../lesson/run-checks";
import { maxManaFor } from "../game/barrier";
import { characterIdByName, partyMembers, partySetupCode } from "./party";

describe("party members for Python", () => {
  it("builds character-sheet dictionaries with mana and an empty spell book", () => {
    const [oogrish, gearshift] = partyMembers(["oogrish", "gearshift"], { oogrish: 18, gearshift: 15 });
    expect(oogrish).toMatchObject({
      character_name: "Master Oogrish",
      race: "Turtle",
      mana: 18,
      max_mana: 18,
      spell_book: {},
    });
    expect(oogrish.abilities.magical_affinity).toBe(9);
    expect(gearshift).toMatchObject({ character_name: "Gearshift", mana: 15, max_mana: 20 });
    expect(maxManaFor(13)).toBe(26);
    expect(partyMembers(["oogrish"], { oogrish: 99 })[0].mana).toBe(18);
    expect(characterIdByName("Master Oogrish")).toBe("oogrish");
    expect(characterIdByName("Nobody")).toBeUndefined();
  });

  it("gives Python a party.members list it can read and change", () => {
    const setup = partySetupCode(["oogrish", "gearshift"], { oogrish: 18, gearshift: 15 });
    const result = runPythonChecks(
      "names = [member['character_name'] for member in party.members]\n",
      [
        { name: "names", code: "assert names == ['Master Oogrish', 'Gearshift']" },
        { name: "mana", code: "assert party.members[1]['mana'] == 15 and party.members[1]['max_mana'] == 20" },
      ],
      { setup },
    );
    expect(result.ok, result.error).toBe(true);
    expect(result.checks.every((check) => check.passed)).toBe(true);
  });

  it("keeps changes between calls in one live session", () => {
    const setup = partySetupCode(["oogrish"], { oogrish: 18 });
    const result = runPythonChecks(
      "def spend(member):\n    member['mana'] = member['mana'] - 10\n    print_mana(member, str(member['mana']))\n",
      [],
      { setup, calls: ["spend(party.members[0])", "spend(party.members[0])"] },
    );
    expect(result.calls.map((call) => call.events)).toEqual([
      [{ type: "mana", name: "Master Oogrish", bar: "8", mana: 8, max: 18 }],
      [{ type: "mana", name: "Master Oogrish", bar: "-2", mana: -2, max: 18 }],
    ]);
  });
});
