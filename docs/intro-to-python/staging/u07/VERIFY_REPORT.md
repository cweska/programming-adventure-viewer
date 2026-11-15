UNIT 7 FINAL VERIFICATION (spell-recipes, "Functions II", order 7)

Unit 7 now passes the harness and the export with no errors. I fixed two problems, both described below. Nothing in the repo was touched (`git status` is clean), no earlier unit's files were edited, and `concept_map.json` is back in place.

FINAL HARNESS SUMMARY LINE (with concept_map.json, staging dir):
3 units, 31 exercises/projects/challenges, 82 checkpoints, 664 wrong answers, 20 quiz questions — 0 errors, 0 warnings

With concept_map.json moved aside, the same run gives 32 errors, all of them "concept not introduced yet: node:For", which is a u06a token. No other token comes up. Unit 7 uses no `while`, `break`, `continue`, list comprehensions, conditional expressions or `.items()`/`.keys()`/`.values()`. Every loop is a `for` over a list or a list of dicts (the roster), plus `for x in [18, 20, 24, 26]` in the map() article example.
The places to cross-check when Unit 6 ships:
- u07a: 6b-remembers/q2; recipes-read-sheets/bar-then-draw (6 errors)
- u07b: spell-recipes-quiz/q2; broken-spell-6c (6); hand-it-over (5); write-the-spell-book (3); the-resonance-array (2)
- u07c: the lambda article (1) and its try-it a-dial-in-one-line (4); the map article (1); qc-r2-a-questions/q1; qc-r2-b-questions/q1

FIXES MADE (staging only)
1. `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u07-staging/u07a_recipes_read_sheets.py`, guard-at-the-door predict. This was the only harness error. The right choice was "Lucky casts Glow.\nERROR: KeyError: 'Star Glow'", but the harness needs a right choice that starts with "ERROR" when the code crashes. The question now says Glow's line shows first and asks what happens next, with Star Glow. The choices are "Lucky casts Star Glow.\n22" / "24" / "ERROR: KeyError: 'Star Glow'", answer 2, and the explanation is rewritten to match.
2. `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u07-staging/u07b_spells_hand_over.py`, BREW_TWIN (the "worked twin" another_way angle in cast-from-the-book). The harness passed this, but it broke the repo's phone-width rule: the fenced line `        cook["herb"] = cook["herb"] - pot["cost"]` is 49 characters. The fence now ends with `# then pay: the line below`, and the long line follows the fence as an inline code span. It keeps the long form rather than `-=`, as the designer intended, and the exercise's notes say why.

EXPORT CHECK
The exporter wrote 6 units to `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/intro-python/u07-staging-export` with no errors or warnings, so there are no unknown fields.
I also ran the content rules from content.test.ts against that output with a scratch script, `/tmp/claude-0/-home-user-programming-adventure-viewer/649b9b27-c022-5e00-b0e0-a22a84b07233/scratchpad/u07tools/content_rules.ts`. Result: 0 problems.
- Every unit parses with `unitSchema`, and unit orders are unique.
- Item, exercise, checkpoint and question ids are unique, and no checkpoint text starts with a number.
- Every `[[term]]` link resolves.
- No glossary term or alias repeats, checked across the staging units and the repo's glossary.json, which includes the sample unit.
- Backticks and fences are balanced, there is no bold and no stars around code.
- Every fenced line in prose is 36 characters or fewer.
Lines over 36 characters in editor code (starters and solutions) are not covered by the rule; Units 2 and 5 have them too.

CONSISTENCY
- The UNIT dict is identical in all three parts: id spell-recipes, order 7, title "Functions II", subtitle "Spells You Can Hand Over", published True, campaign_links ["friends-in-low-places"].
- No duplicate item ids.
- Campaign links point to real beats in `content/modules/friends-in-low-places/module.json`: mana-bars, spell-book, hold-the-barrier and skill-checks.
- All 70 hero dicts match the party table (affinity 9/10/12/13, max_mana 18/20/24/26).
- Check data uses invented Tor names only (Brakka, Pell, Moth, Moss, Bellows) plus the party. There is no "Tester", no worksheet name and no student name. `base_attack` appears once, only in a sidecar `why`.
- Glossary: 11 new terms, each linked somewhere in Unit 7 and none defined in earlier units. u07a has guard, helper, matching parameter, same sheet. u07b has function as a value. u07c has default value, keyword argument, scope, lambda, map(), unpacking.
- Every one of the class's real slips listed in the brief has `wrong_answers` entries. That includes the caster-versus-target (wrong-sheet) slip, which shows up in this unit as `lucky` versus `hero` and as the hero's sheet versus the spell's page.
- Mar'tu's voice and the terminology match the brief. Student-facing "recipe" appears only in Mar'tu's lines, titles and the recipe-card analogies.
- Every SOLO item and Quick Check exercise has explainer="lean". Both Quick Check forms have questions_to_pass=3 with 4 questions, like Unit 2's QC2.
- Campaign-mode items (6C-04, 6C-05, 6P) have no tracer. 6C-04 and 6P have no Assemble it; 6C-05 keeps its L1–L4 ladder. engine=False everywhere.

ITEM LIST (kind · id · title · minutes · optional · exercise count)
u07a
- quiz · 6b-remembers · Mar'tu remembers… · 2 · optional · 2 questions
- lesson · recipes-read-sheets · Recipes That Read Stat Sheets · 40 · core · 9 exercises: hand-over-a-sheet, recipes-change-sheets, many-ingredients, store-by-name, guard-at-the-door, read-the-helper, bar-then-draw, broken-spell-6b, solo-6b
u07b
- quiz · 6c-remembers · Mar'tu remembers… · 2 · optional · 2 questions
- lesson · spells-you-can-hand-over · Spells You Can Hand Over · 38 · core · 7 exercises: name-without-parentheses, hand-it-over, recipe-in-a-box, write-the-spell-book, cast-from-the-book, broken-spell-6c, solo-6c
- quiz · spell-recipes-quiz · Spell Recipes Quiz · 8 · core · 8 questions (the spec's types and order)
- project · the-resonance-array · The Resonance Array · 20 · core · 1 (6 checkpoints, Lucky's side quest)
- challenge · spell-book-from-blank · The Spell Book, From Blank · 12 · optional · 1 (8 checkpoints)
u07c
- lesson · extra-defaults-and-scope · Extra practice: Defaults and Scope · 10 · optional · 2 exercises (defaults-and-names, inside-stays-inside)
- article · lambda · lambda: A Function in One Line · 10 · optional · 1 try-it
- article · map · map(): One Function, Every Item · 10 · optional · 1 try-it
- article · two-things-back · Two Things Back · 10 · optional · 1 try-it
- testout · qc-r2-a · Quick Check Recipes II · Form A · 16 · optional · 4 exercises
- quiz · qc-r2-a-questions · Form A questions · 4 · optional · 4 questions
- testout · qc-r2-b · Quick Check Recipes II · Form B · 16 · optional · 4 exercises
- quiz · qc-r2-b-questions · Form B questions · 4 · optional · 4 questions
- cheatsheet · chalk-notes · Mar'tu's Chalk Notes: Spell Recipes · — · optional · 21 entries

MINUTES
- The two lessons and the quiz come to 86 (40 + 38 + 8), against the ~85 in the brief.
- Adding the project, all non-optional time is 106. The curriculum's time ledger gives 105 core.
- Optional time is 96, against the ledger's 67 (pool 25 + optional 42). The whole unit is 202.

REMAINING CONCERNS
1. Lesson 6C is 38 minutes; the spec says 37.
2. Each Quick Check form is 16 minutes plus 4 for its questions, about 20 per form; the spec says ~12. Each form also has 4 questions where the spec lists 3, so the 3-of-4 gate can work as in Unit 2.
3. spell-book-from-blank (an optional 12-minute challenge) is not in the Unit 7 spec. It is the main reason optional time is over the ledger.
4. Campaign mode is not in the schema; it lives only as a `camp=true` note. The site will show 6C-04, 6C-05 and 6P with the full help ladder. Nothing in the data stops that: the rung-2 hint cap, the missing Start me off and Compare after 5 minutes are not enforced. The same goes for the skill gates on 6B-05, 6C-01 and 6C-03. This needs site work.
5. broken-spell-6b has no partials, on purpose: its slips crash in a chain, so a partial cannot turn one checkpoint green at a time. Its notes say so.
6. The `node:For` cross-check listed above is still to do once Unit 6 lands.