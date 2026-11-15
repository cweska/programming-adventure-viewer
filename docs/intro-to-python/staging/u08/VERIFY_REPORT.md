## Unit 8 final verification: "Code Challenges" / "Trials of the Yard"

**Result: Unit 8 passes. The only open items depend on Unit 7.** I worked only in the staging dir. The repo and the earlier units' files are untouched, and `git status` is clean.

### 1. Harness
- **With `concept_map.json` (the normal run), `harness.py u08`:** `3 units, 33 exercises/projects/challenges, 86 checkpoints, 546 wrong answers, 0 quiz questions — 0 errors, 0 warnings`
- **All real files, map moved aside:** 9 errors, 0 warnings. I restored the map afterwards.
  - Every error is "concept not introduced yet" for `node:DefaultArg` and `node:KeywordArg`. These are u07c tokens, from card 6B-08.
  - They sit in `make-bar` (starter, solution, predict, assemble) and `make-bar-clamped` (starter, solution, partials 1-2, assemble).
  - No other errors.
- **Cross-check with the real Unit 7:** I built a separate folder of symlinks (`.../scratchpad/u08verify/combined`): u01–u06 and u08 from the staging dir, u07a–c from `.../intro-python/u07-staging`. With no map: `0 errors, 0 warnings`. So the two u07 tokens resolve once Unit 7 ships.
- **Unlock ceilings:** my own script checked each set against the tokens that the real u01–u06 files introduce (u07 from the map). It covered starter, solution, example, partials, predict, assemble lines and distractors, and bonus solutions, with and without setup exemptions. **0 violations in any set:**

  | Set | Items | Ceiling |
  |---|---|---|
  | T-HCL | `hard-coded-ledger` | Unit 1 |
  | Control Flow | `can-cast`, `clock-color`, `passes-with-luck` and their twins | Units 1–3 |
  | Lists | `newest-gap`, `last-three`, `add-guess` and their twins | Units 1–4 |
  | Dictionaries | `spell-cost`, `affinity-of`, `meets`, `rename-spell`, `rename-safely` | Units 1–5 |
  | Dictionaries T-D-1a and Loops | `cheapest-spell`; the Loops set | Units 1–6 |
  | Functions and T-Own | u08c items, plus 6B-08 and 2-A2 | Units 1–7 |

  - One exception outside the sets: the intro article `trials-of-the-yard` has an example, `def double(n)`, that uses Unit 3 tokens (`node:FunctionDef`, `node:Return`). It passes the course-order gate, and its notes justify it.
  - `concept_map.json` disagrees with the real files in three places: it puts `op:In` in u04b (the files teach it in u05a), and `node:Tuple` and `call:zip` in u04b (the files teach `node:Tuple` in u06b and `call:zip` nowhere). No Lists or Dictionaries trial uses any of them, so the ceilings hold either way.

### 2. Export and content rules
- The exporter (`--src u08-staging --out u08-staging-export`) wrote 7 units and 16 files with no errors and no unknown fields.
- I ran the repo's own `content.test.ts` checks against the export in a scratch copy of the repo layout. They cover schema parsing, unique ids, unique glossary terms and aliases, `[[link]]` resolution, prose rules and fences ≤ 36 characters.
  - **Staging export plus the sample unit:** 18 passed, 1 failed. `make-bar`'s Learn text links `[[default value]]` and `[[keyword argument]]`, which are Unit 7 (u07c) glossary terms, so they do not resolve without Unit 7.
  - **Same export plus the real Unit 7 (and Unit 9):** 19 of 19 passed.
- No Unit 8 glossary term or alias duplicates one in any other unit (u01–u07, u09, the sample, or the repo's `glossary.json`). Unit 8 adds 13 new terms, and every one is linked: test table, hidden test, edge case, hard-coded, refactor, rerun table, ZeroDivisionError, tie, average, early exit, clamp, lookup, AssertionError.

### 3. Consistency
- The `UNIT` dict is identical in all three parts: `code-challenges`, order 8, published, campaign_links `leylines-awaken` and `friends-in-low-places`.
- Item ids are unique.
- **Campaign links:** every module and part id is a real beat in `content/modules/*/module.json`. The spec's links are all present:
  - T-CF-1a goes to `hold-the-barrier`.
  - T-CF-3 goes to `skill-checks`.
  - T-D goes to `spell-book` and `hold-the-barrier` (nested reads).
  - T-F-3a (`act-lookup`) goes to `hold-the-barrier` and quotes `spell["spell_function"](caster)`.
  - T-Own goes to `hold-the-barrier`, reading check messages.
- Every item is optional, every trial is `support="light"`, `engine` is off, and nothing uses randomness.
- **Help ladder:** 3 or more hints per checkpoint, 3–4 another_way angles, and an assemble block on every trial. The harness raised no "Start like this" or Start me off warnings.
- No student names, no worksheet-derived names and no "Tester" anywhere.
- **Wrong answers:** every slip the class makes has at least one wrong_answers entry that the harness proved fails, with a specific message:
  - a typed visible answer such as `return 44`, caught by hidden labeled tests;
  - `<` versus `<=` at the exact boundary;
  - the empty case, including the IndexError on `wall[-1]` and the ZeroDivisionError in the average;
  - `"True"` in quotes, or `"0"`;
  - printing instead of returning;
  - changing the list passed in, and the reverse;
  - a KeyError for an unknown spell or choice;
  - the wrong tie-break;
  - `effect()` written with brackets, or never called;
  - weak seals in both seal trials;
  - reading the test table backwards.
- I also ran 52 new wrong answers of my own against the checks. Every real bug failed with a kind, specific message. The 6 that passed were all correct versions written another way, such as `.get` with a default, or `<=` in the core lowest-mana trial, which has no tie rule.
- **Minutes:** core 0, as the curriculum says. Optional total 259 (u08a 96, u08b 94, u08c 69), against about 335 in the curriculum's time ledger.

### Edits I made (backups in `.../intro-python/backups/u08-final-verify/`)
1. **Mar'tu's voice.** Two Learn texts in u08a called Mar'tu by name, which no earlier unit does in the Learn pane. I made them first person:
   - `newest-gap-empty-wall`: "I wiped the wall clean once."
   - `add-guess-new-list`: "I want the old wall kept as it was…"
2. **Summaries.** In u08b and u08c, I changed "Advanced variant of X:" to "The advanced twin of X:" in 10 summaries. This matches u08a and the article's own word, "twin".
3. **Article accuracy.** "Each trial gives you a `def` line" became "Most trials give you a `def` line…", because the Hard-Coded Ledger has no `def`. "Its hidden tests" became "A table's hidden tests".

After these edits I re-ran the harness (0 errors, 0 warnings with the map, and 0 errors, 0 warnings with real Unit 7), the export, and the content checks.

### Items (kind, id, title, minutes, optional, exercise count)

`level` and `variant_of` are real FORMAT fields, so no fields were invented. Each challenge is one exercise; its checkpoints are in brackets.

| Kind | Id | Title | Min | Optional | Exercises |
|---|---|---|---|---|---|
| article | trials-of-the-yard | Trials of the Yard | 3 | yes | 0 (1 example) |
| challenge | hard-coded-ledger | The Hard-Coded Ledger | 11 | yes | 1 [6] |
| challenge | can-cast | Can I Cast? | 6 | yes | 1 [2] |
| challenge (adv, variant_of can-cast) | can-cast-skill-first | Can I Cast? Skill First | 8 | yes | 1 [2] |
| challenge | clock-color | The Clock's Color | 6 | yes | 1 [2] |
| challenge (adv) | clock-color-flashing | The Clock's Color: Flashing | 8 | yes | 1 [2] |
| challenge | passes-with-luck | Dumb Luck | 8 | yes | 1 [2] |
| challenge (adv) | which-roll | Dumb Luck: Which Roll? | 8 | yes | 1 [2] |
| challenge | newest-gap | The Newest Gap | 5 | yes | 1 [2] |
| challenge (adv) | newest-gap-empty-wall | The Newest Gap: An Empty Wall | 6 | yes | 1 [2] |
| challenge | last-three | The Last Three Gaps | 6 | yes | 1 [2] |
| challenge (adv) | total-drop | The Total Drop | 7 | yes | 1 [2] |
| challenge | add-guess | Bomb Shell's Guess | 7 | yes | 1 [2] |
| challenge (adv) | add-guess-new-list | Bomb Shell's Guess: A New List | 7 | yes | 1 [2] |
| challenge | spell-cost | The Price of a Spell | 6 | yes | 1 [2] |
| challenge (adv) | cheapest-spell | The Cheapest Spell | 10 | yes | 1 [3] |
| challenge | affinity-of | Read the Affinity | 5 | yes | 1 [2] |
| challenge (adv) | meets | Can They Cast It? | 10 | yes | 1 [3] |
| challenge | rename-spell | Rename a Spell | 6 | yes | 1 [2] |
| challenge (adv) | rename-safely | Rename, Safely | 10 | yes | 1 [3] |
| challenge | total-mana | The Party's Mana | 6 | yes | 1 [2] |
| challenge (adv) | average-mana | Average Mana | 8 | yes | 1 [3] |
| challenge | count-below | Count the Short Gaps | 6 | yes | 1 [2] |
| challenge (adv) | first-shrink-over | The First Big Shrink | 10 | yes | 1 [3] |
| challenge | lowest-mana-name | Who Needs Glug First? | 7 | yes | 1 [2] |
| challenge (adv) | lowest-with-ties | Glug, With Ties | 10 | yes | 1 [3] |
| challenge | make-bar | A Bar for Any Gauge | 7 | yes | 1 [2] |
| challenge (adv) | make-bar-clamped | A Bar That Fits Its Box | 9 | yes | 1 [4] |
| challenge | apply-to-all | One Spell for Everyone | 8 | yes | 1 [3] |
| challenge (adv) | apply-if-it-worked | Only the Ones It Worked On | 9 | yes | 1 [3] |
| challenge | reply-lookup | Four Branches, One Lookup | 8 | yes | 1 [4] |
| challenge (adv) | act-lookup | A Book of Actions | 10 | yes | 1 [4] |
| challenge | seal-can-cast | Write Your Own Checks | 8 | yes | 1 [3] |
| challenge (adv) | seal-cast-ok | Seal the Barrier | 10 | yes | 1 [3] |
| cheatsheet | read-a-test-table | How to Read a Test Table | — | yes | 0 (11 entries) |

### Remaining concerns
1. **Unit 7 dependencies, to cross-check when Unit 7 ships.**
   - Tokens `node:DefaultArg` and `node:KeywordArg` are used in `make-bar` and `make-bar-clamped`.
   - Glossary links `[[default value]]` and `[[keyword argument]]` are in `make-bar`'s Learn text.
   - Both resolve against the current `u07-staging` Unit 7.
   - Unit 8 must not be exported to the repo before Unit 7, or CI's link check fails.
2. **The intro article's `def double(n)` example uses Unit 3 tokens.** A student who opens the Hard-Coded Ledger early (after Unit 1) would see it. This is accepted as the unit card; the alternative is a Unit-1-only example.
3. **`concept_map.json` is off for u04b.** It lists `op:In` and `node:Tuple` (which the real files teach in u05a and u06b) and `call:zip` (which no file teaches). This does not affect Unit 8, but the map is stale for any partial run that relies on it.
4. **Partials.** No 2-checkpoint core in u08b or `make-bar` has a partial; u08a's cores each have one. `cheapest-spell` (3 checkpoints) has none, and its notes explain why: a strict `<` already handles the tie. Every other trial with 3 or more checkpoints has partials.
5. **Long code lines.** Some signatures in editor code are over 36 characters, e.g. `def passes_with_luck(first_roll, second_roll, needed, has_luck):` (64) and `make_bar`'s `def` line (52). These are the spec's signatures. Earlier units have many editor lines over 36 too, and the phone rule only binds prose fences, which all pass.
6. **Small style differences.** u08a names checks "hidden test: …" and u08b/u08c name them "hidden: …" and "row N: …". The player does not show check names, so students only see the messages, which are consistent. Pair-talk prompts in u08a start with "Pair talk:"; the site strips that prefix, as in earlier units.
7. **Site support that would make this unit nicer** (none of it is in FORMAT, so I did not invent fields):
   - a first-class test-table field that renders the visible rows and the hidden-test labels. Today the visible rows sit in the starter's print/comment lines and a fenced `text` table in each Learn text, and the hidden tests are labeled checks;
   - per-set unlock gating (T-HCL after Unit 1, Control Flow after Unit 3, and so on);
   - "Ready for more" suggestions on the teacher page;
   - showing a challenge's twin (`variantOf`) next to its core;
   - showing passed and failed hidden-test labels from the check names.

The verification scripts are in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u08verify/`.

Files are in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/`:
- `u08-staging/u08a_trials_early.py`
- `u08-staging/u08b_trials_data.py`
- `u08-staging/u08c_trials_functions.py`
- `u08-staging-export/` (the export)
