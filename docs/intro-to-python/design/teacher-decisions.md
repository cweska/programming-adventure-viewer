# Decisions from the teacher (Nov 12, 2026)

These override anything in curriculum.md that conflicts.

1. **D11 approved.** Functions I ("First Recipes") comes right after Control Flow, for the whole class.

2. **The class has already played every campaign module that exists (Modules 1 and 2), and struggled a lot.**
   Intro to Python is there to **re-ground them and rebuild confidence**, not to prepare them for a first look.
   - Use **Route M2** (whole core, then on to the next campaign module). Route M1 and the "Before the cabin door"
     check are not needed for this class, so build them last, if at all.
   - Campaign links are **"you've seen this — now you'll get it"** moments, not previews. Point back to the parts they
     already played: `move_left()` and `party.move("left")` at the cabin door, Mar'tu's dialogue line with
     `.lower().capitalize()`, the four dialogue options with `if`/`elif`, the trap-door skill checks with
     `random.randint` and `return roll >= required_roll`, the spell book `add_spell(...)`, the mana bars
     `"█" * caster["mana"]`, and `cast_spell` holding the barrier.
   - Tone: confidence first. Early, certain wins. Name the struggle kindly once ("A lot of that campaign code felt like
     a wall, yes? We will take the wall apart, one stone at a time."), then show progress. Errors are normal and
     expected; never imply they should already know this.
   - Rehearsal exercises (campaign mode) double as review of what they already saw.

3. **Every student has their own device.** Pair work is welcome where it truly helps an exercise (for example a
   "Pair talk: explain this line to your partner" prompt, predict-and-compare, or swapping broken spells to fix), but
   every checkpoint is completed solo on each student's own device. No shared-device features.

4. **Open a pull request to `main` as soon as Unit 1 passes everything**, so it can be merged before 12:00pm MST on
   Fri Nov 13 (GitHub Pages deploys only from `main`). Then keep building units in order on the branch.

Timeline: students first use the section Fri Nov 13 around 12:00pm MST. Unit 1 must be complete and solid; later
units ship as they are finished.
