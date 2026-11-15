## Unit 10 final verification: 0 errors

**Final harness line** (whole unit, with concept_map.json moved aside and then put back):
`3 units, 34 exercises/projects/challenges, 67 checkpoints, 644 wrong answers, 41 quiz questions — 0 errors, 3 warnings`

- **The 3 warnings are intended.** They are the deliberately broken starters of the mend tasks: u10a mend-the-choice, u10b mend-the-reply and u10c mend-the-reply.
- **Each part with the concept map in place:** u10a, u10b and u10c each give 0 errors and 1 warning.

**READY path (no Strings tokens): confirmed three ways.**
- The gate ran with the map aside, so it was built only from the real u01–u07 files plus u10. Nothing in the staging folder is a u08 or u09 file.
- I scanned every visible code field with the harness's own tokenizer: starters, solutions, examples, partials, question code and wrong answers. No u09a/u09b token appears (`const:escape`, `attr:upper/title/split/join/strip/replace/find`, `node:FString`). No student-facing text has string methods or f-strings, and Unit 10 has no `introduces` or `preview` lists.
- Control test: I injected `"a".upper()` into a throwaway copy. The gate rejected it ("uses concepts not introduced yet: attr:upper"), so the gate is live.
- String methods appear only inside hidden check code, which students never see.

**Export.** `export_prototypes.py --src <staging> --out <staging>-export` gave: "Exported 8 unit(s) … 18 file(s) written", with no errors or warnings. I bundled the repo's `schema.ts` with esbuild and re-ran `content.test.ts`'s rules on the export. Result: "NO PROBLEMS".
- Every unit parses with `unitSchema`.
- Ids are unique and unit orders are distinct.
- Every glossary link resolves, and no glossary term or alias repeats. Unit 10 adds only `campaign mode`; its other links (`dictionary`, `nested dictionary`, `for loop`, `loop variable`, `function as a value`, `randint`, `traceback`) are defined in Units 2–7.
- Backticks are balanced, fences closed, and no checkpoint text starts with a number. No prose marks problems.
- No fenced prose line is over 36 characters.
- The repo is untouched (`git status` is clean).

**Consistency**
- **UNIT dict:** identical in all three files (id readiness-check, order 10, published True, links leylines-awaken and friends-in-low-places).
- **Ids:** the 14 item ids are unique.
- **Campaign links:** all real. The unit's module ids exist, and every exercise link (friends-in-low-places / hold-the-barrier) matches a real part id in `content/modules/*/module.json`.
- **Review routes:** all 13 rc-review routes point to real lessons and exercises, with matching titles. Where a route promises a worked example, Assemble it or the tracer, the target exercise has it. u10c's copy of ROUTES is identical to u10a's.
- **Part 1:** every item lists its skill tags and the campaign part it prepares (§5.3).
- **Names in checks:** no "Tester", no worksheet-written names and no sheet ids in the student-facing JSON. One sheet id is cited in a `why` in the hidden test data file, which is allowed.
- **Voice:** Mar'tu's dry, kind tone with ", yes?" holds throughout.

**Fix I made** (in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u10-staging/u10b_readiness_form_b.py`): form B's 9 Part 1 meta lines said `path="CC"`; they now say `path="READY"`, like forms A and C. This is in designer notes only, and I re-verified afterwards. No other edits; earlier units' files were not touched.

**Times**
- **Part 1:** 28 minutes (quiz 10 + tasks 18), on target (~28).
- **Mini-boss A:** 15 minutes, on target (~15).
- **Required core:** 46 minutes (intro 2 + Part 1 28 + mini-boss 15 + explain 1).
- **With the spaced re-check:** 58 minutes (re-check 12, optional and a week later), against a curriculum core of 56 (~60).
- **Review routing:** 15 minutes, optional, only after a miss (curriculum: 15).

**Items** (kind · id · title · minutes · optional · exercises)

u10a:
1. article · before-we-continue · Before We Continue · 2 · no · 0
2. quiz · rc-part1-a-questions · Readiness Check · Part 1 · Form A questions · 10 · no · 12 questions
3. testout · rc-part1-a · Readiness Check · Part 1 · Form A · 18 · no · 9 exercises (13 checkpoints), questions_to_pass=10
4. article · rc-review · Mar'tu's Notes: Where to Look Again · 15 · yes · 0
5. project · rc-miniboss-a · Mini-boss: Hold the Lantern Ward · 15 · no · 1 (6 checkpoints, 5 partials, 43 wrong answers)
6. quiz · rc-explain · Explain a line you wrote · 1 · no · 1 question

u10b:
7. quiz · rc-part1-b-questions · Readiness Check · Part 1 · Form B questions · 8 · yes · 12 questions
8. testout · rc-part1-b · Readiness Check · Part 1 · Form B · 20 · yes · 9 exercises (14 checkpoints), questions_to_pass=10
9. project · rc-miniboss-b · Mini-boss B: Hold the Glow Ward · 15 · yes · 1 (6 checkpoints)
10. challenge (advanced) · rc-trial-ember-ward · Trial: Hold the Ember Ward from its goals · 15 · yes · 1 (6 checkpoints)

u10c:
11. quiz · rc-part1-c-questions · Readiness Check · Part 1 · Form C questions · 8 · yes · 12 questions
12. testout · rc-part1-c · Readiness Check · Part 1 · Form C · 20 · yes · 9 exercises (14 checkpoints), questions_to_pass=10
13. quiz · rc-recheck-questions · Readiness Re-check questions · 3 · yes · 4 questions
14. testout · rc-recheck · Readiness Re-check · 9 · yes · 4 exercises (8 checkpoints), questions_to_pass=3

**Part 1 and mini-boss setup:**
- **Part 1 exercises:** `support="none"` and `explainer="lean"`, with no Another way, Assemble it or tracer.
- **Mini-bosses and trial:** `support="light"`, `solo=True`, `explainer="lean"`, with no Assemble it or tracer. Being solo turns off Start me off.
- **Hint cap:** every mini-boss ladder is Where to look plus two Teach rungs, with no finished line.
- **Every class slip listed in the task** is proven by a failing wrong answer. Messages are lean: they name the slip and the evidence, never the fix.

**Missing site support**
1. **Blocking: Part 1 counts as a Quick Check.**
   - Passing any testout (`rc-part1-a/b/c`, or even `rc-recheck`) calls `markTestedOut`. Unit 10 then shows as complete, and the mini-boss and explain item read "tested-out", which contradicts the Ready rule.
   - `UnitPage` moves every testout and its `-questions` quiz into the "Already know this? Pass it and this unit counts as done" box.
   - `nextUpItem` and `nextHref` skip testouts. So "Next" after the 12 questions jumps to rc-review and skips the 9 tasks, and "Next up" goes from the intro straight to the mini-boss.
   - Unit 10 needs a readiness mode: list Part 1 as core and never test the unit out with it.
2. **No hint-cap field.** The cap is written into the hints, but the last rung is still labelled "Show me how".
3. **Compare timer.** It is course-wide: 5 minutes or 4 failed runs. The spec wants 5 minutes only, and there is no per-exercise setting.
4. **No campaign-mode flag.** It is marked `camp=true` in the notes, and "no Start me off" comes only from solo.
5. **No skill-tag routing.** There is no per-skill map, no per-part Band A/B view and no teacher flags. Skills, prepared parts and review routes live only in notes meta and the rc-review article.
6. **Ready rule only approximated.** `questions_to_pass=10` plus every task stands in for "≥11/13". Item 6 at ≥3/4, item 13 required, and "mini-boss without Compare" are not enforced.
7. **Retakes.** Nothing draws form B or C, or opens only the one task Mar'tu's notes name. Quizzes keep the best score and show the answer after an attempt (e.g. 58 for i4b), so a retake of the same form can be passed from memory.
8. **Spaced re-check.** Nothing schedules it a week later, and a miss does not set the skill back to practicing. rc-recheck is optional.
9. **Explain a line.** Picking a line from the student's own code is UI work; the prototype asks about a reference line.
10. **Explainer parity.** The "messages are shorter" line sits in the mini-boss intros and rc-review, because there is no Readiness review screen.

**Content concerns** (minor, not changed)
- Mini-boss A writes its evidence as "Mar'tu's test, only inside the check: …". Mini-boss B and the trial put it in brackets: "(Mar'tu's check cast …)". u10b's notes claim the messages are the same.
- Form A splits its 28 minutes as quiz 10 + tasks 18; forms B and C use 8 + 20.
- The notes' meta lines differ in shape between parts: A has `item=`, B and C have `rc_item=`, and only C has `review=`.
- Editor code lines over 36 characters:
  - the campaign's guard lines in the mini-boss starters (up to 54);
  - rc-explain's code (47);
  - several Part 1 and re-check solutions (37–48).
  These are documented exceptions, and earlier units are wider.
- Form B's "Store, then pass it on" shares its title with the Unit 3 lesson that rc-review points to.
- Form B's traceback task uses `total_cost`, the worksheet template's name. It is not a student-written value, and Units 1 and 3 use it too.
- Mini-boss B is `use_ward(caster, ward_name)` rather than the spec's `use_ward(caster, ward)`, per the teacher's review (documented in the file).
- The "wall" struggle is named again in the intro card and the unit intro; the teacher's decision says once.

Files are in /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python:
- u10-staging/u10a_readiness_form_a.py
- u10-staging/u10b_readiness_form_b.py
- u10-staging/u10c_readiness_recheck.py
- u10-staging-export/units/readiness-check.json
- u10-staging-export/units/readiness-check.verify.json