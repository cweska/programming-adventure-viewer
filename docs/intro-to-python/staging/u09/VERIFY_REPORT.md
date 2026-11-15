## Unit 9 "Strings" final verification

All three checks pass. Unit 9 ends with 0 errors and 0 warnings in the harness, a clean export and a clean content-rules check.

**Final harness summary line** (`u09`, run with `concept_map.json` moved aside and then put back):
`3 units, 25 exercises/projects/challenges, 58 checkpoints, 588 wrong answers, 28 quiz questions — 0 errors, 0 warnings`

- **Each part, with the map in place:**
  - u09a: 13 exercises, 27 checkpoints, 217 wrong answers, 12 questions, 0 errors, 0 warnings.
  - u09b: 6 exercises, 21 checkpoints, 171 wrong answers, 6 questions, 0 errors, 0 warnings.
  - u09c: 6 exercises, 10 checkpoints, 200 wrong answers, 10 questions, 0 errors, 0 warnings.
- **Concept-not-introduced errors:** none. Nothing needed a u08 prefix.

### Export and content rules
- **Export:** `export_prototypes.py --src <staging> --out /tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u09-staging-export` exported 8 units with no errors, no warnings and no unknown fields.
- **Rules:** I ran the repo's content-test rules against the exported JSON. `content.test.ts` reads only the committed folder, so I rebuilt its rules in a script. I included the sample unit so glossary clashes would show. Result: 0 problems.
  - Every unit parses with the schema.
  - All ids are unique.
  - Every `[[term]]` resolves, and no glossary term or alias repeats across units.
  - Prose marks and fences are correct, and every fenced line is 36 characters or less.
  - Each unit's `.verify.json` points at real exercises.
- **Pre-existing warnings, not from Unit 9:** the sample unit's glossary terms `string`, `variable`, `input` and `comment` repeat Unit 1's.
- **Against the shipped Units 1–4:** staging's u04 files are older than the repo's published Unit 4 (the repo version has the hint-ladder fixes). I copied the repo's u01–u04 and staging's u05–u09 into a temporary folder and re-ran everything. The harness, export and rules all came out clean, so Unit 9 holds against what is actually shipped.

### What I fixed (only in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u09-staging/u09b_strings_practice.py`)
Curriculum 2.12 rule 2 says an optional item may use an earlier optional-only token only if it names the item that teaches it. Two places broke that:
1. **8P1 intro:** the project uses `sum()`, which is optional only (3C-03). The intro now ends: "…, and Biggest and smallest in More List Tools (`sum()`). A loop that adds works too." I updated the designer notes to match. I tested that a loop total passes.
2. **8P1 side quest, second hint:** it uses `continue`, which is optional only (5C). The hint now ends "(You met `continue` in Skip the empty, in Loops in One Line.)".

I re-ran the harness, the export and the rules check after both edits. Nothing in the repo or in earlier units' files was touched, and `git status` is clean.

### Consistency
- **UNIT dict:** identical in all three parts: `strings`, order 9, "Strings" / "Runes and Ribbons", published True. Unit campaign links are `leylines-awaken` and `friends-in-low-places`.
- **Campaign link targets:** every exercise link points to a real beat in `content/modules/*/module.json`: mana-bars, program-dialogue-options, program-dialogue-prompt, red-clock, chalk-wall and ley-clock.
- **Glossary:** only new terms. u09a adds method, immutable, escape mark, `.upper()`, `.title()`, chain, `.split()`, `.join()`, `.strip()`, `.replace()`, `.find()` and f-string. u09b adds cipher. u09c adds none.
- **House rules:**
  - Mar'tu's voice is consistent throughout.
  - No student names, no worksheet names, no "Tester" and no engine names as variables.
  - `engine` is off everywhere, and the checks use no randomness.
  - Both SOLO items and all six Quick Check exercises use `explainer="lean"`, and their messages name the slip and the evidence but never the fix.
  - `questions_to_pass=4` of 5, the same "all but one" ratio as Unit 2's QC2 (3 of 4).
  - There are no trace tasks, so no `paste_stop` guard is needed.
- **The class's slips:** each one has a wrong answer that fails where it should. The list includes `int("seven")` and `int("48 hrs")`. `int("7 ")` is correctly *not* treated as a slip, because Python ignores spaces at the ends; the cheatsheet shows `int(" 12 ")` working.
- **Alternative answers:** I tried 57 other ways a student might answer, and 56 behaved as they should. Valid alternatives pass: one-line versions, f-string versions, `+=`, the student's own creative values, `.find(...) != -1`, `not in`, and a decode written as its own loop. Typed answers, `.count()` and stripping before replacing fail with clear messages.

**Minutes:**
- Core is 62: Lesson 8A 22, Lesson 8B 32, Quiz 8B 8. With the two optional warm-ups it is 66. The curriculum core is about 60 (20 + 32 + 8).
- Pool is 18 (12 + 6), the same as the spec.
- Each Quick Check form is 16 + 5 = 21 minutes, against the spec's ~10. That matches earlier units: QC2 is 19, QC6 is 18 and Unit 7's is 20.

### Items (kind, id, title, minutes, optional?, exercises)
| Kind | Id | Title | Min | Optional? | Exercises |
|---|---|---|---|---|---|
| quiz | 8a-remembers | Mar'tu remembers… | 2 | yes | 2 questions |
| lesson | strings-are-rows-of-letters | Strings Are Rows of Letters | 22 | core | 5 (9 checkpoints; SOLO solo-8a) |
| quiz | 8b-remembers | Mar'tu remembers… | 2 | yes | 2 questions |
| lesson | words-that-change-shape | Words That Change Shape | 32 | core | 8 (18 checkpoints; SOLO solo-8b) |
| quiz | words-quiz | Quiz: Words That Change Shape | 8 | core | 8 questions |
| lesson | extra-letter-by-letter | Extra practice: Letter by Letter | 12 | yes (pool) | 3 |
| quiz | rows-of-letters-quiz | Quiz: Rows of Letters | 6 | yes (pool) | 6 questions |
| project | the-water-stained-log | The Water-Stained Log | 40 | yes (recommended) | 1 (7 tasks) |
| project | the-institute-cipher | The Institute Cipher | 60 | yes (browser-only) | 1 (5 tasks) |
| challenge | tag-from-blank | Name Tags, From Blank | 10 | yes | 1 (2 checkpoints) |
| testout | qc8-a | Quick Check 9 · Form A | 16 | yes | 3 |
| quiz | qc8-a-questions | Quick Check 9 · Form A questions | 5 | yes | 5 questions |
| testout | qc8-b | Quick Check 9 · Form B | 16 | yes | 3 |
| quiz | qc8-b-questions | Quick Check 9 · Form B questions | 5 | yes | 5 questions |
| cheatsheet | chalk-notes | Mar'tu's Chalk Notes: Strings | — | reference | 24 entries |

### Remaining concerns
1. **Spec changes the authors made on purpose** (each explained in its notes; I left them alone):
   - The first warm-up drops the spec's `spells["glow"]` vs `spells["glow"](hero)` question. The notes cite a teacher ruling, which is not in `teacher-decisions.md`.
   - Quiz 8B Q7 asks for `.title()` where the spec has `capitalize`.
   - Quiz 8B Q8 is a missing `return`, not the spec's "forgotten reassignment". Questions 1 and 6 only use reassignment in their wrong choices.
   - 8B-03 steps 3 and 4 are goal-only; the spec marks them dictated.
   - 8A-07 is split into three checkpoints.
   - `tag-from-blank` is an extra item the spec does not list.
   - Each Quick Check has 5 questions where the spec has 2.
2. **Lesson 8B is dense:** 8 exercises and 18 checkpoints in 32 minutes. For this class it may run long.
3. **Wide lines in the editor:** a few code lines are longer than 36 characters, mostly the spec's own 62-character messy log line in 8P1, the cipher lines in 8P2, and the 43-character `.replace` line in 8B-05. Only fenced prose is checked, and earlier units have far more such lines.
4. **Form B gauge symbols:** the Quick Check Form B gauge uses ▮ and ▯. They are pre-typed in the starter, but someone should check they look right on student devices.
5. **Pell line in Form A:** in Quick Check Form A, putting `shield_bar(1, 4)` in a variable and printing `{pell}` fails step 2. The step asks for the call itself inside the f-string, and the lean message says the call is missing. That fits the task, but a student could reasonably try it.
6. **Open items:** 8B-08's echo spot has no schema field yet (it is recorded in the notes). 8P2 stays browser-only until the teacher confirms IDLE.
7. **Old Unit 4 copies in staging:** the staging u04 files are not the published version. Whatever packages this unit should use the repo's Unit 4, which I confirmed works with Unit 9.

Files are in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u09-staging`:
- u09a_strings_rows_and_shapes.py
- u09b_strings_practice.py
- u09c_strings_checks.py

The export is in `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u09-staging-export`.