# Intro to Python: curriculum v2 ("Mar'tu's Lessons")

**Status:** v2. It applies every accepted or modified directive in `design/teacher-directives-curriculum.md`.
Items marked **[OWNER]** still need the real teacher's yes (listed in §8). Nothing in the course content has been
built yet. This document is the build spec for the prototype files.

**Read with:** `context/brief.md`, `context/campaign-python-inventory.md`, `personas/personas.md`,
`research/zpd-principles.md`, `research/codecademy-mechanics.md`, `design/architecture.md`, and
`docs/intro-to-python/prototypes/harness.py` + `FORMAT.md` (the prototype format and verifier).

**Verified for v2 (CPython 3.13.18):**
- `design/curriculum_v2_gate.py` holds representative code for all 260 planned items, in course order (each Quick Check form and each Readiness
  form counted once). It
  runs the harness's own tokenizer on six paths and reports **0 violations on each**:
  - **CORE:** core items only.
  - **CRIT:** the campaign-critical path only.
  - **FULL:** every item.
  - **M1:** Units 1–3 plus "Before the cabin door".
  - **READY:** the Readiness Check with no Strings items.
  - **TRIALS:** each Trials set against the unit where it unlocks.

  The script also passes lints (c), (f) and (g). It computes the time ledger (core 733 min; critical path 435 min
  against a 524-minute limit), and it wrote `docs/intro-to-python/prototypes/concept_map.json`. Its output is in
  `design/gate-v2-output.txt`.
- `design/v2check/probe.py` and `probe2.py` executed every error message and output this plan quotes. One v1 claim
  was wrong: `choice == option 2` raises **SyntaxError: invalid syntax**, not a NameError. The explainer row is
  fixed (§2.6).
- **Not verified yet:** checkpoint wording, hints and art are design intent. The prototype files must prove them
  with `harness.py`.

**IP rule.** Codecademy's "Learn Python 3" supplies only the learning goals and the item mix. Every premise, name,
value, line of text and question is original and set in Tor.

**Privacy.** Persona evidence is cited by anonymous sheet ID (A-01 to A-08, B-01 to B-03), in this document and
in harness `notes` only, never in anything a student sees. No student's written value appears in content, check
messages, contrast galleries or Parsons distractors (§2.11).

---

## Contents
0. Changes from v1 and why (directive → change)
1. Course overview (purpose, story frame, unit order, deviations, routes, the code/file map)
2. Site experience (exercise loop, help stack, presets, item kinds, checks, explainer, accommodations, mastery,
   terminology, campaign mode, privacy, authoring rules and lints, teacher page and run-kit, legend)
3. Units 1–10, item by item (the per-exercise spec)
4. Concept introduction map (token → first exercise; skill gates without tokens)
5. Campaign Readiness Check ("arriving in the ZPD", operationalized)
6. Time ledger, campaign-critical path, release gates
7. Prototype work packages
8. Open [OWNER] questions

---

# 0. Changes from v1 and why

Each directive ID from the teacher's file maps to what changed in v2, and where. "→ §x" points to the section
that now carries it. **A** = accepted, **AM** = accepted as modified, **D** = declined (kept declined).

## 0.1 Structure and time (the headline directives, T1–T13)

| Directive | What changed in v2 |
|---|---|
| **Top-10 #1 / T1** time is a hard constraint | The v1 lean core is now the core: **733 min ≈ 18.3 periods**, including the Readiness Check and five Mar'tu moments (§6.1). The nine v1 trims, plus 1A-07 and 1C-05, moved to an **Extra practice pool**. Pool items are optional and keep their ids, and they feed twins, the spaced queue and early finishers. Project task groups that left the core became each project's Lucky side quest. A time ledger (§6.1) gives core, contingent, pool, optional, G1 and G4 minutes per unit. Every item is tagged **CC** (campaign-critical) or **SC** (syllabus-core). The critical path is **435 min**, against a limit of core ÷ 1.4 = 524 (§6.2). No week calendar is shown to students; the map shows milestones only (§2.13). |
| T1 immediate moves | 1A-07 (triple quotes) and 1C-05 (`+=`) are pool items. Later checks accept `+=` and the long form, and no core code shows `+=`. 1-A1 is a one-minute card (§3, Unit 1). |
| T1 Strings independent | The Readiness Check uses no token Strings introduces (the READY gate path proves it). `chain-methods` is taught in 6A-08, and the bar skills are spaced through 5A-07 and 6B-07. Strings can run before, alongside or after Module 2 (§1.5). |
| **#2 / T2 / D11** Recipes early **[OWNER]** | New order: Hello World → Control Flow → **Functions I: First Recipes** (6A, Quiz 6A) → Lists → Dictionaries → Loops → **Functions II: Spell Recipes** (6B, 6C, Quiz 6B, 6P) → Trials (optional) → Strings → Readiness (§1.3). 6A-08's starter now tidies its line with `.lower()` then `.capitalize()`, with one Predict, so `attr:capitalize` enters at 6A-08 and Units 1–3 cover every line of Module 1. Recipe-shaped practice in Units 4–6 is by conversion: 3A-06 `newest_mark(wall)`, 4P `max_mana_for` reused, 5A-07 `mana_bar(hero)`, 5P `average(values)`, and 3P1 `last_score(log)` (pool). Every warm-up from Lists on carries a def/return item, and so does each unit quiz. The Control Flow Trials unlock in function form after Unit 3. |
| T2 routes M1/M2 | A class-level teacher setting (§1.5, §2.13). M1 adds the 10-minute **"Before the cabin door"** check (u03b). |
| **#3 / T3** one help stack | Binding screen contract in §2.2: after a failed run there is one message and one **Help** control. Start me off, Another way, More structure and Assemble it all live inside it. |
| **#4** silence is a signal | 90-second "editor unchanged, no Run" trigger. The Point rung is always available. "Hasn't run code" shows on the teacher page (§2.2, §2.13). |
| **#5** explainer precedence tree | §2.6, with the harness wrong answer that proves each row fires. |
| **#6** checks see meaning | §2.5 adds BARE, SWAP/LINE-TOTAL, NEWBOX, PNM, fuzzy RNM, LEFT, PAR-CONST, RET-PARAM, STREXACT, OUT diff, extended NAME and CMB. There are no OUT-only checks on computed values (lint a). PAR sets never collide with the task's calls (lint b). A student's creative value never fails a check (lint e). |
| **#7** honest test-outs | Every QC has a coverage table (skill → item → evidence wrong answer), **two forms**, and a "not yet" result for any untestable skill. A pass converts items instead of deleting them (§2.4). "Tested out" stays provisional until a typed spaced item confirms it. |
| **#8 / T4** fade to campaign parity | **Campaign mode** (§2.10) for 6C-04, 6C-05, 6P and Readiness Part 2. Vocabulary converges on the campaign's words (§2.9). Porting the explainer to `explain.ts` is a separate PR (§6.3), and until it lands the Readiness review screen says campaign messages are shorter. |
| **#9 / T5** mastery evidence | Each lesson has at least one **non-dictated** checkpoint (`dictates: false`, lint g) and one **SOLO** item. "With structure" passes are recorded as such, and an Assemble pass or a reveal triggers a typed twin. Together and solo are separate ticks (§2.8). Every typed QC and Readiness item is behavior-checked. |
| **#10 / T7 / T8** a teacher can run it | §2.13: the classroom page (Needs you now, Ready for more, campaign readiness by skill), teacher settings, the summary schema additions, and an outline of the one-page run-kit (`docs/intro-to-python/teacher-guide.md`) with the sync points and Mar'tu moments. |
| T6 verification discipline | Every new explainer row and check pattern names its proving `wrong_answers` entry (§2.5, §2.6). Lints (a)–(g) are in §2.12. The gate script already checks (c), (f) and (g) at design time. |
| T9 fun budget | At most one flavor line per screen, one cameo line per checkpoint pass, and echo only at designated spots. The world-as-data payoffs (2P1, 4A-01, 5A-05, 5B-04) are protected and shown to tested-out students as "Mar'tu wants to show you something". At least one combining side quest per lesson. Calm mode is independent and off by default (§1.2, §2.7). |
| T10 privacy | §2.11 covers the no-student-values rule, the blocklist with a generic fallback, the class switch, and the absence of a visible preset badge. |
| T11 release gating | §6.3: the tiers, each with its gate. Static step tables stand in for the tracer in Unit 1. The trace-table item type blocks Unit 3. |
| T12 shared-code safety | Course changes to `explain.ts`, ConsolePanel and the worker are additive behind the `"course"` prelude flag (§2.12 rule 12). |
| T13 measure | §6.4 lists the log fields and the after-Unit-1 recalibration. |

## 0.2 Conflicts resolved (C1–C15)

| ID | Ruling applied |
|---|---|
| C1 placement and fading | The preset question appears on the first map visit. No answer, "never" or "a little" gives "Show me more". "Yes" offers QC1, never an automatic "Keep it short". Self-report and the pulse can only **add** support. Support fades only on performance: a hint-free streak of 5 checkpoints, a QC pass, or predict accuracy of at least 80% over a lesson. A QC1 pass sets "Keep it short" (§2.3). |
| C2 4B-04 names | 4B-04 keeps **different** names. Its comment reads "Replace each 0 with the variable that holds that value". "Matching" means an exact name from 6B-03 on, and the "same word, two jobs" Investigate sits in 6B-03 (§3). |
| C3 different-from-example checks | 1A-02 and 1B-01 keep the check. Its failure message offers **Mar'tu's pick inline**, and the pick counts as the student's own. |
| C4 assemble or type first | The default view follows the preset: Assemble-first on A-stage exercises under "Show me more", a typed starter under "Keep it short". Assemble it is always a More-structure level, and an Assemble pass is followed by a typed twin. |
| C5 pairs | The teacher assigns pairs. The course never auto-pairs, and pair mode is off by default. |
| C6 solo size | One SOLO item per lesson, ≤ 2 min: a make-twin in writing lessons (1B, 1C, 6A, 6B, 6C), one bug elsewhere. Values differ per seat. It is recorded, never blocking, and never shown to the partner. On a pass: "You did that alone. I saw." |
| C7 fast lane / recipe track | D11 is class-wide. There is no per-student order. Module 1 timing is the teacher's call, informed by "Before the cabin door". |
| C8 offer volume | An offer is a highlight on the Help control plus one line, never a pop-up. One dismiss silences offers for that exercise. Offers turn off after a hint-free streak. Under "Keep it short", only the 3-failed-runs trigger is active. |
| C9 price-first | Only the **second** word problem (1C-02 CP2, ropes) and the 1C-03 twin put the price first. The `# how many?` / `# how much is one?` comments stay. |
| C10 echo and persistence | Echo appears only at designated spots, on the student's own screen, through the blocklist and the class switch. Persistence is Tier 3. |
| C11 meaning prompts | "Names to use" chips are always on. Point-at-it questions and example-name heads-ups are hidden under "Keep it short" and instructions-light. |
| C12 two-call starters | 6A-04 and 6A-05 start with two calls plus "add a third call for your own hero". 6A-06 CP3 is goal-only for everyone. "Start from blank" is offered on hint-free streaks. |
| C13 `print(two words)` | One message. If either word is a defined name, it leads with the space-in-name reading; otherwise it leads with the quotes reading. Each version names the other in one clause (§2.6). |
| C14 capstone-first | Offered only after a hint-free streak or a QC pass, never on self-report. Every skipped skill gets a one-minute spaced item plus the Readiness re-check. |
| C15 1-A1 | A ≤ 60-word card with three pictures and G3's two sentences, then just-in-time coach marks. |

## 0.3 Group 1, "Starting from zero" (G1)

| ID | Decision → change |
|---|---|
| R1 | AM → §2.3: the preset question on the first map visit, defaulting to "Show me more", fading on performance only. |
| R2 | A → 1-A1 card (≤ 60 words, three pictures) plus coach marks (§2.2). |
| R3 | AM → §2.6 rows: `invalid decimal literal`, the bare-name line, `'(' was never closed`, the any-bad-`def` row, the dict-comma row naming **this line and the line above**, plain titles, and "One fixed. Python found the next one:". |
| R4 | A → BARE check (§2.5) in 1B-02, 1B-03, 1B-06 and QC1 #2. Messages use invented values. |
| R5 | AM → new core **6A-06b `be-the-ledger`** on the trace-table item type, with a matching predict in Quiz 6A and Readiness item 4b. |
| R6 | A → the reconciliation card at 4A-02, worded with the quotes principle. |
| R7 | AM → at least 3 genuinely different angles for Unit 1 concepts and CC skills, at least 2 elsewhere. The next unseen angle is served inside Help (§2.2). Angles are listed per exercise in §3. |
| R8 | A → **blocks Unit 1**: starters pre-type `full = "█"` / `empty = "░"` (and `▮ ▯`, `▓`), and the editor toolbar has a symbol tray. |
| R9 | A → the help-stack contract (§2.2). |
| R10 | A → read-aloud and the picture angles say `=` as "gets" and `==` as "is the same as" (§2.9). |
| R11 | A → 2A-02 first exposure is `clock_is_red = (clock_color == "red")`. 2A-03 drops the parentheses. |
| R12 | A → OUT (diff) check (§2.5). |
| R13 | A → 1C-07 has three checkpoints and pre-typed left sides, and checks the student's own hero. |
| R14 | A → the wild-count message in 1C-02. The 1000-ropes step is the 1C-03 Investigate for everyone, using Try other numbers. |
| R15 | A → 1B-06 adds `def companion = "Gearshift"`. 2C-06 stays as review. |
| R16 | A → 1A-03 teaches "quotes and brackets come in pairs" with `print("Shield up."`. |
| R17 | AM → task-group headers in every project starter. Placeholders and the full ladder appear under "Show me more". 4P pre-builds two sheets under "Show me more". |
| R18 | AM → one SOLO item per lesson (C6). |
| R19 | AM → CC/SC tags (§6.2). Deferral is a teacher-controlled per-student switch that the dashboard suggests. The freed time goes to the 1B-T, 1C-T and 6A-T twins. |
| R20 | A → the PAR-CONST message with a call table (§2.5), in 6A-04, 6A-05 and 6A-06. |
| R21 | A → glossary entries: defined / not defined, syntax, run, call, value, assign, indent, method (§2.7). |
| R22 | A → terminology contract (§2.9). |
| R23 | A → no "box" in 1A. The 1A explainer uses G1's wording (§2.6 rule 9). |
| R24 | A → a neutral, non-red "fizzle" panel in the course. Proposed for the campaign in the port PR. |
| R25 | A → glossary and read-aloud stay on in QCs and the Readiness Check. |
| R26 | A → quiz review for everyone: what you got right, then "worth another look", then the score. |
| R27 | AM → echo spots only: 1A-02, 1B-02, the 1P1 watch-keeper, 2P1's tiers, 8B-08 (§2.11). |
| R28 | A → ≤ 60 words of Learn text before the first action in 1A–1C for every preset (lint f; drafts in §3). The labeled-box picture is shown by default in 1B. |
| R29 | A → 3A-01 pre-types `hour_1 = 48`. |
| R30 | A → 1W-04 points out `-`, `_` and `=` side by side. |
| R31 | A → a missed recall item shows the answer and a one-line why, with no red X (§2.1). |
| unnumbered | A: 1B-02 CP2 message ("That prints the word *character*…"). A: 1B-02 distractors (a lone `"Zelda"`, `character - "Zelda"`). A: 1C-08 stamp angle plus the glue-versus-stamp sentence. A: 2A-04 "the dot means ask this text to do something". A: the two-step "read the error" footer from 1W-02 on, with the full routine in 2C-07. A: 5A-05 stays predict-heavy with a static trace table. A: 1A-07 and 1C-05 deferred. AM: Q1 is superseded by D11. |

## 0.4 Group 2, "Right shape, wrong meaning" (G2)

| ID | Decision → change |
|---|---|
| R1 | A → price-first in 1C-02 CP2 and in the 1C-T twin. |
| R2 | A → the multi-word row (§2.6), plus a multi-word case in 1A-04, **extended to `==`** after the probe showed `choice == option 2` is a SyntaxError. |
| R3 | A → lint (a). It fixes 3A-06 (now PAR), 3A-08 (merged into 3A-05, CMB), 3B-01 (CMB + range), 3B-04 (pool, CMB), 8A-02 (merged into 8A-01, CMB), 8B-03 (CMB) and QC3 #2 (CMB). |
| R4 | A → 1C-07 checks the student's own hero (CMB rerun with `"Tester"`), generalized as lint (e). |
| R5 | AM → merged into 6A-06b. The handed-back `7` (raw inputs) message is kept. RET-PARAM is added (§2.5). |
| R6 | A → 6A-04 and 6A-05 starters have two calls with `# should show …` comments. CP2 is "add a third call for your hero". |
| R7 | A → SWAP plus LINE-TOTAL in 1C-02, 1C-03, 4B-04, 6B-03 and 6C-04. |
| R8 | AM → "Names to use" chips everywhere. LEFT uses an authored `foreign_names` list. The heads-up never blocks and is muted under "Keep it short". |
| R9 | AM → one-click point-at-it questions on 1C-08, 2A-03, 4A-05, 4B-04, 5A-07 and 6A-06, and on every `dictates: true` checkpoint. They count as "explains" evidence and are hidden under "Keep it short" and instructions-light. Unit 1 has them if the inline mc ships by then; otherwise they are retrofitted at the Unit 2 release. |
| R10 | A → the rerun table inside CMB failures (Unit 1). The Try other numbers button comes by Unit 2, introduced at 1C-01. 1C-09 is the payoff. |
| R11 | A → one quotes sentence, word for word everywhere (§2.9), plus the 6-card sort as 4A-07's Investigate. |
| R12 | A → "show your working" in Unit 1. "Recipe" is reserved for `def`, with a 1C callback in 6A-05. |
| R13 | A → wall values are "gaps" and differences are "shrink". 5A-05 is "How much each gap shrank". §1.2 and T-Lo-2 are fixed. |
| R14 | A → the `error_type = NameError` special case (2C-01) and the "Did you mean" reframe (§2.6 rule 5). |
| R15 | AM → fade on performance only (C1). Predict calibration shows topics at lesson end, with no running percentage. |
| R16 | A → when the tracer ships. Until then, a wrong predict on a return value or reassignment opens the static trace table. |
| R17 | A → Readiness item 12 is typed with a CMB rerun. Every typed item is behavior-checked. |
| R18 | A → letter-diff highlighting on near-miss names, sharing one helper with the OUT diff. |
| R19 | A → the distractor rule (§2.12 rule 8). Distractors use invented values. |
| R20 | AM → an immediate, required twin after a reveal, using the student's own values where there is a creative slot. The spaced twin stays. |
| R21 | AM → Tier 3 (§6.3). |
| R22 | AM → designated echo spots (§2.11). |
| R23 | A → STREXACT (§2.5), merged with G3 R24. |
| R24 | A → 5A-02's Learn says the naming rule aloud. |
| R25 | D → coach marks instead of a tour. |
| unnumbered | A: every exercise has its own starter, with no carry-over unless designed. A: 1B-04's campaign reason. A: hint names `a`/`b` go in `foreign_names`. A: 4B-04 keeps different names. |

## 0.5 Group 3, "Steady with a template" (G3)

| ID | Decision → change |
|---|---|
| R1 | A → explainer rule 4 (a bare value plus the required name) outranks the quotes row (§2.6). |
| R2 | A → 1B-01 Investigate "delete `companion =`, Run, what happened?", with a static "made, not kept" picture. |
| R3 | A → 6A-05a `fill-the-ingredients` is contingent (first exposure under "Show me more", or after an assisted or failed 6A-04), plus the `___` row. |
| R4 | A → 6A-06 Investigate "delete `return total`", plus the console None notice (§2.6). |
| R5 | AM → Start me off (rung 0) and More structure live inside Help. More-structure levels are hand-authored for rehearsals and projects and auto-derived elsewhere. A step down is logged, and the next exercise starts back at its default. |
| R6 | A → the silent-stall trigger (§2.2). |
| R7 | A → under instructions-light, the Point rung is always available and project starters keep their task-group headers. |
| R8 | A → a `starter_level` field (S4–S0) on every exercise in §3, enforced by lint (c). |
| R9 | AM → teacher-set pairs. Prompts name seats, solo twins use different values per seat, and solo results are hidden from the partner. Two seats on one device only if devices are shared **[OWNER]**. |
| R10 | A → the run-kit says B-02/B-03 start on "Show me more". The 6A-S solo twin informs placement. |
| R11 | A → NEWBOX (§2.5), with a 1C-03 wrong answer. |
| R12 | A → `_near_names` covers plurals and case-plus-plural. Python's "Did you mean" is passed through for user-defined names (§2.6 rule 6). |
| R13 | A → the empty-body IndentationError row, proven in 6A-02. |
| R14 | A → lint (b). 6A-05's PAR sets are (6, 5) and (20, 1). |
| R15 | A → the 6C-05 four-level ladder (L1 default for everyone). A pass below L1 is recorded "with structure". |
| R16 | AM → mastery map v1 (with structure / from comments / from blank, plus tested out (provisional), plus together and solo ticks), by the Unit 4 release (§2.8, §6.3). |
| R17 | A → a 1–2 line typed twin after an Assemble pass. |
| R18 | A → Readiness items 2, 3 and 8 get campaign-style starters (`def roll_die(die_size): return 1`). |
| R19 | A → 1C-07 left sides. 2B-08 and 5A-02 get skeletons at first exposure. |
| R20 | A → Investigate prompts are one-click choices, with free text optional. |
| R21 | A → the two-apostrophes row (proven in 1A-03). |
| R22 | A → suppress keyword and builtin suggestions, listing the parameter names instead (PNM). |
| R23 | A → "You did that alone. I saw." on SOLO passes. |
| R24 | A → merged into STREXACT. |
| R25 | A → the "When does a recipe need `return`?" card in 6B-02, paid off by 6B-07. |
| unnumbered | A: G3's two sentences on 1-A1. A: the 1C-03 Teach rung ("a 0 in the starter is a placeholder"). A: rehearsal comment numbers map one-to-one onto checkpoints. A: 6A-04's "from what you know" angle and the `hero_name` predict. AM: pair mode is the teacher's choice. |

## 0.6 Group 4, "Ready to stretch" (G4)

| ID | Decision → change |
|---|---|
| R1 | A → every QC's coverage table. A skill with no failable item shows "not yet" (§2.4 and each QC in §3). |
| R2 | AM → the conversion table (§2.4). Exercise-level routing by the Unit 2 release; Unit 1 may ship lesson-level plus capstone conversion. |
| R3 | A → PNM takes precedence inside a function body (§2.6 rule 2). |
| R4 | A → fuzzy RNM using `foreign_names` (§2.6 rule 3). |
| R5 | A → the space-in-name rows (both forms) and the mixed-quotes row. |
| R6 | AM → see C2. |
| R7 | A → instructions-light always shows "Names to use" and the signature, never trims rehearsal starters, and keeps the explainer on in QCs, Trials and light mode. |
| R8 | A → **for everyone**: the spaced re-check includes typed items on `combine-values`, `exact-names`, `param-use` and `return-right-name` (§5.4). |
| R9 | A → §6.1: "most of Unit 1 by QC1; Units 2–7 at about 0.7–0.8× through capstone-first and light mode". |
| R10 | A → 6A-06 CP3 (`max_fuel_for(cells)`, goal only) is the lesson's non-dictated checkpoint, plus PAR-CONST. |
| R11 | A → capstone-first from the Unit 2 release, on a hint-free streak or a QC pass only. |
| R12 | D → no per-student order (C7). |
| R13 | A → type-first under "Keep it short", with Assemble as the fallback (C4). |
| R14 | AM → Mar'tu's slate is Tier 3: local only, explainer on, `# expect:` checks, and the teacher's class switch. |
| R15 | AM → **"Mar'tu's seal"** (asserts) is optional article 2-A2 at the end of Unit 2, re-offered as a side quest in 6A-09 and T-Own. `node:Assert` is optional-only. |
| R16 | A → at least one combining side quest per lesson (§3 BQ lines). |
| R17 | AM → **"The Hard-Coded Ledger"** Trial (T-HCL) is in v2. "Four copies, one loop" and "One bar recipe" are Tier 3. |
| R18 | A → two forms per QC. |
| R19 | A → Mar'tu's pick inline (C3), a "use Mar'tu's picks" button in projects, and DF available in QCs. |
| R20 | AM → the opt-in apprentice protocol is in the run-kit, never the default. |
| R21 | AM → one required recall item (< 1 min) per lesson, for tested-out skills only. A miss reverts the skill to "practicing" and queues its capstone. |
| R22 | A → "Why does this work?" sidebars in 6A-05 ("Why the recipe can't know the numbers yet") and 6A-07 ("Whose kitchen is `result` in?"). |
| R23 | AM → a one-click "what was different?" after Compare. |
| R24 | AM → "Explain a line you wrote" in the Readiness Check for everyone. Hard mode is Tier 3. |
| R25 | A → QC-R1 opens with "Nobody in this cabin has written a recipe yet. This shows Mar'tu where to start." |
| R26 | A → QC1 #1 is multiple choice, plus the symbol tray. |
| unnumbered | A: story reveals are never skipped silently (T9). A: cameos stay under "Keep it short", and Calm mode is independent. A: QC1 sets the preset (C1). A: 6C-05 L1 for everyone. |

## 0.7 Specs, answers and the action list

| Directive | Where |
|---|---|
| §4.1 explainer tree | §2.6 (every row, its order, and its proving wrong answer) |
| §4.2 check library and lints | §2.5, §2.12 |
| §4.3 help stack | §2.2 |
| §4.4 classroom page and settings | §2.13 |
| §4.5 Quick Checks | §2.4 (rules, conversion) and each unit's QC entry (coverage tables, forms) |
| §4.6 Readiness changes | §5 (item 12 typed, starters for 2, 3 and 8, new item 13, explain-a-line, campaign mode, independent of Strings) |
| §4.7 terminology | §2.9 |
| §5 Q1–Q14 | Q1 → D11 plus routes (§1.5). Q2 → D1–D10 approved, D7 extended, D11 [OWNER] (§1.4). Q3 → planned to 18.3 periods (§6). Q4 → spoiler rules kept (§1.2). Q5 → FK ≤ 6 target, ≤ 60/≤ 120-word caps (§2.12). Q6 → pairs (§2.7). Q7 → QC rules (§2.4). Q8 → PF hooks kept, with a pre-typed first line (3A-01, 4A-01). Q9 → Readiness is practice only (§5). Q10 → names [OWNER]. Q11 → helpers and pseudo-tokens approved (§4.2). Q12 → f-strings: read both, write either (8B-07). Q13 → Calm mode off by default. Q14 → 8P2 browser-only until IDLE is confirmed. |
| §6 tiers | §6.3 |
| §7 action list | Phase A, steps 1–9, are this document (step 9's hand-off is §6.3). |
| §8 bring-back | This doc; the ledger (§6); the gate output (`design/gate-v2-output.txt`); Unit 1 coverage evidence is due at the Unit 1 gate (§6.3); the [OWNER] list (§8). |

---

# 1. Course overview

## 1.1 Purpose

Intro to Python gets every student into the **zone of proximal development (ZPD)** for the Python in campaign
Modules 1 and 2 (research §4.1). A student is there when they can:
- **read and explain** every line of a campaign part's starter code,
- **write the one-line edits unaided**, and
- **finish each part with only the campaign's own support**: numbered instructions, check messages, the error
  explainer, Show solution after five minutes, and an occasional hint.

The hardest parts (`spell-book`, `mana-bars`, `hold-the-barrier`) should feel like a real stretch that the
student can still win. The Campaign Readiness Check (§5) measures this.

The course follows the sample syllabus's learning goals and item mix: lessons, quizzes, projects, articles,
optional code challenges with advanced variants, and cheatsheets. It also closes the campaign gap the syllabus
leaves open:
- dictionaries: literals, reads, nested reads, writes by key, `in` / `not in`, and lists of dicts;
- functions as values: assigned, passed without `()`, stored in a dict, then called from it;
- `random.randint`;
- `"█" * n`, including `"░" * (max - mana)`;
- returning comparisons;
- early `return`;
- reading engine-helper code the student did not write.

It is built for this class's four evidence groups (personas.md):

| Group | Sheets | In one line |
|---|---|---|
| **G1** "Starting from zero" | A-02, A-03, A-04 | no working model of a variable yet |
| **G2** "Right shape, wrong meaning" | A-05, A-07, A-08, B-01 | eager; copies shapes, not meanings |
| **G3** "Steady with a template" | B-02, B-03 | solid on templates, stalls at a blank |
| **G4** "Ready to stretch" | A-01, A-06 | solid basics, one step from functions |

Three class-wide findings drive the design:
1. **Functions are the cliff.** 0 of 11 wrote a working function. So the recipes start early (D11) and come back
   in every unit after.
2. **Nobody let the code combine values.** Everyone who reached 68 typed it by hand. So CMB checks rerun the
   program with other numbers, and students can watch that happen.
3. **Students copy example names and write the value instead of `name = value`.** Only 1 of 11 wrote
   `character = ...`. So examples use visibly different names, checks name the copied identifier, and "Names to
   use" chips are always on.

## 1.2 Story frame

Mar'tu, a former Institute teacher, pulls "you" (the adventurer) aside in the cabin by the cherrywood mantle.
The Ley Clock ticks above them. Each unit opens with one Mar'tu scene line and ends with a short story beat
("Mar'tu's notes"). Lore stays out of instruction blocks. Instructions are plain English, numbered, with code in
backticks, in the same style as the campaign's.

**Opening (course map, first visit):**

> *Mar'tu draws you aside, away from the fire. Only their tired yellow eyes show under the purple shroud.*
>
> **Mar'tu:** "Hi. It is me, Mar'tu. Before we continue on our adventure you must learn some of the language we call, Python."
>
> "The ley-lines do not listen to shouting. They listen to instructions. Every barrier I raise is a few lines of Python."
>
> "One question first. Have you typed code before?"  **[ never ]  [ a little ]  [ yes ]**
>
> *(After the answer.)* "Good. We start small. When you are stuck, I will offer help. When you are not, I will leave you alone. Both are allowed."
>
> **Lucky** *(from across the room)*: "What's in it for me?"
>
> **Mar'tu:** "Existing."
>
> [ Begin ]   [ Where should I start? (Quick Checks) ]

The answer only sets the starting preset (§2.3). It is never scored or shown to anyone else. The teacher can
pre-set it provisionally.

**Mar'tu's voice rules (all text):**
- Short sentences. Dry, grim but caring, deadpan.
- At most one ", yes?" per screen.
- The accent shows in rhythm and word order, never in misspellings, so read-aloud and English learners are not
  penalized.
- **Mar'tu's voice appears only in** the first and last line of the Learn pane, pass lines, the Help control's
  label, and story beats.
- Checkpoint text, check messages, explainer text, glossary entries and quiz logic are plain standard English.
  No lore appears in them.
- Mar'tu never says "Wrong" or "You're a natural". The wise-feedback pattern is: *"Your spell fizzled. Good. Now
  we can see why, yes? I would not give you this if I thought you could not mend it."*

**Fun budget (T9).**
- At most one flavor line per screen, outside instruction and check text.
- At most one cameo line per checkpoint pass.
- Mar'tu echoes a typed value only at the designated spots (§2.11).
- **Calm mode** hides cameos. It is an independent toggle, off by default, and not tied to any preset.
- **World-as-data payoffs are protected:** 2P1 (the encounter table), 4A-01 (which number is which?), 5A-05 (the
  decay reveal) and 5B-04 (the forecast). There, the story *is* the data. A student who tests out or is deferred
  past one gets it as a "Mar'tu's notes" line or a 2-minute "Mar'tu wants to show you something" item. It is
  never skipped silently.

**Party cameos** (one line each, on passes or in side quests, never inside instructions):
- **Oogrish:** "Steady, now." He labels the Help control after 3 failed runs: "Steady, now. Read the last line
  first. Want a nudge?"
- **Gearshift:** "Math checks out." (pass line on combine and arithmetic checkpoints)
- **Bomb Shell:** clipped pass lines ("Works." "Shield up.") and the Broken-spell exercises ("That latch hates
  me.").
- **Lucky:** owns the side quests ("What's in it for me?") and the campaign-link box ("What's in it for me? This
  shows up in the campaign as…").

**World data used throughout** (real values from `content/campaign/characters/*.json` and the brief):
- **Chalk wall.** The **gaps** (hours between bursts) are `[48, 48, 47, 46, 44, 41, 37]`. Each gap's **shrink**
  from the one before is 0, 1, 1, 2, 3, 4, so "the decay is accelerating". The words "gaps" and "shrink" are
  fixed (G2 R13).
- **Party table:**

  | Hero | INT | WIS | DEX | STR | magical_affinity | max_mana (= 2 × affinity) | Weapon | Armor |
  |---|---|---|---|---|---|---|---|---|
  | Master Oogrish | 17 | 17 | 14 | 13 | 9 | 18 | Staff of Wisdom d6 | +2 |
  | Gearshift | 14 | 15 | 13 | 17 | 10 | 20 | Longsword d8 | +3 |
  | Bomb Shell | 14 | 8 | 6 | 15 | 12 | 24 | Arm cannon d8 | +3 |
  | Lucky | 13 | 12 | 15 | 17 | 13 | 26 | Telegun d6 | +3 |
- **Other recurring details:**
  - d20 skill checks against a required roll from 2 to 20, and Lucky's once-a-day Dumb Luck reroll.
  - The Ley Clock: one hand, a blue arc, and once a red flash. "It is NOT a compass."
  - Starlode ore (Gearshift) and Velocite ore (Bomb Shell, about a week left).
  - Lucky's canteen of glug.
  - Spell colors: gold, fire orange, teal, silver, and violet for Mar'tu.
  - The resonance array from the Institute.
- **Near-transfer rule.** The course rehearses the campaign's *shapes* with different names. It uses
  `learn_spell`, `cast`, `lantern_ward`, `show_on_ley_board`, `scout.step` and `roster`. It never uses
  `add_spell`, `cast_spell`, `strengthen_magic`, `print_prompt`, `party` or any other campaign name, so the
  campaign parts are not spoiled (architecture Q7).
- **Spoilers (Q4 [OWNER]).** By default, Bomb Shell and Lucky stay (the brief's opening uses Lucky's line). The
  course never shows `Strengthen Magic`, the red-clock event, or campaign function names.

## 1.3 Units in order, with rationale

D11 (Recipes early) is applied. Units are numbered in course order. **Exercise codes keep their v1 letters**
(6A, 3A, 4B …), so every directive, review and design note stays traceable. A code's digit is therefore not
always its unit number; §1.6 maps codes to units and files.

| # | Unit (in-world title) | Codes | Syllabus source | Why it sits here |
|---|---|---|---|---|
| 1 | **Hello World: "Words by the Fire"** | 1-A, 1W, 1A, 1B, 1C | Hello World | Syllabus order. Three short lessons so G1 gets a win in the first two minutes and Run feedback after every step. `"█" * n` enters early (D4). |
| 2 | **Control Flow: "The Ley Clock Decides"** | 2A, 2B, 2C | Control Flow (+ Errors lesson) | Syllabus order. `random.randint` lives here, as in the random-answer project. The Errors lesson stays at the end. |
| 3 | **Functions I: "First Recipes"** | 6A | Functions (first half) | **Moved up (D11).** Functions are the cliff for 11 of 11. Starting them after Unit 2 gives three units of spaced recipe practice before Functions II. 6A uses only Unit 1–2 ideas, and it covers every remaining line of Module 1. |
| 4 | **Lists: "The Chalk Wall"** | 3A, 3B | Lists | Syllabus order relative to Loops. Trimmed to what later units need (D7). Carries recipe-shaped practice. |
| 5 | **Dictionaries: "Stat Sheets and Spell Books"** | 4A, 4B | *new* (campaign gap) | **Inserted (D1).** Right after Lists, so "a list remembers order, a dictionary remembers meaning" is fresh, and Loops can walk a list of dicts the way the campaign walks `party.members`. |
| 6 | **Loops: "Every Member of the Party"** | 5A, 5B | Loops | Syllabus order. Loops walk the roster of hero sheets. |
| 7 | **Functions II: "Spells You Can Hand Over"** | 6B, 6C | Functions (second half) | Recipes that take sheets, build dicts, guard with early `return`, and get handed over as values. These are the campaign rehearsals. |
| 8 | **Code Challenges (optional): "Trials of the Yard"** | T- | Code Challenges | Syllabus order (after Functions). Sets unlock earlier in function form (§3, Unit 8). |
| 9 | **Strings: "Runes and Ribbons"** | 8A, 8B | Strings | Syllabus order (last). **Independent of the Readiness Check** (T1), so it is the pacing lever. |
| 10 | **Campaign Readiness Check: "Before We Continue"** | RC | *new* | **Added (D9).** Operationalizes "arriving in the ZPD" (§5). The teacher may run it before Strings. |

## 1.4 Deviations from the syllabus

D1–D10 are approved as drafted (directive §5 Q2). D7's list is extended. **D11 is new [OWNER].**

| ID | Change | Reason |
|---|---|---|
| **D1** | Insert **Dictionaries** (Unit 5) between Lists and Loops. | The campaign leans on dicts in every Module 2 part, and the syllabus has none. Right after Lists: (a) the list → dict contrast is fresh; (b) Loops walks a **list of dicts**; (c) Functions II takes a hero dict; (d) dicts return in four later units. |
| **D2** | Functions II gets **6C "Spells You Can Hand Over"** (functions as values, a dict holding a function, passing a function without `()`) plus two campaign-shaped rehearsals. lambda and `map()` stay as optional articles. | The campaign needs `add_spell(..., strengthen_magic)` and `spell["spell_function"](caster)`. The syllabus covers functions as values only through lambda and `map()`, which the campaign never uses. |
| **D3** | One string method, `.lower()`, enters in Control Flow (2A-04) for case-safe comparisons. | A control-flow use. It previews Module 1's `.lower().capitalize()`. |
| **D4** | `"█" * n` appears in Unit 1 (1C-08) and returns in Units 6, 7 and 9. | `*` is taught there. `mana-bars` depends on it, including the `(max - mana)` parentheses. |
| **D5** | A debugging strand starts in Unit 1: every lesson has a Broken spell exercise. The full Errors lesson stays at the end of Unit 2. | Unclosed and missing quotes on 6 sheets; `def` versus `=` (A-02). Research P11. |
| **D6** | Unit 1's single lesson becomes three short lessons (1A, 1B, 1C). | Small steps and early wins for G1. |
| **D7** | Some syllabus items are **optional** but kept. v2 moves the v1 trims into the **Extra practice pool** (optional items that keep their ids). | Class time (§6). None of them is campaign-critical. |
| **D8** | Code Challenges gets a Dictionaries set. | The same gap as D1. |
| **D9** | Add the Campaign Readiness Check, with a spaced re-check before Module 2. | The operational ZPD definition (research §4.5). |
| **D10** | The `input()` article is interactive (the replay shim, architecture §4.2). | Fixes Codecademy's known weakness. |
| **D11 [OWNER]** | **Functions I (6A + Quiz 6A) moves to right after Control Flow, for the whole class.** Lists, Dictionaries and Loops carry recipe-shaped practice. Functions II (6B, 6C, Quiz 6B, 6P) stays after Loops. | Functions are the cliff for 11 of 11 students. This gives three units of spacing instead of one. Spaced retrieval is the highest-utility technique (research P13). 6A was already verified portable. If declined: keep the v1 order and the fast lane as a class option, still with no per-student tracks. |

**Items that are optional or in the Extra practice pool:**

| Unit | Optional (always offered) | Extra practice pool (moved out of core in v2; keeps its id) |
|---|---|---|
| 1 | 1P2 Ward Sign, 1-A2 Clock Math, 1-A3 `input()`, QC1 | 1A-07 triple quotes, 1C-05 `+=`, twins 1B-T and 1C-T, 1P1's old task group C (Lucky's side quest) |
| 2 | 2-A1 `match`, 2-A2 Mar'tu's Seal, 2P2 Three Roads, QC2 | 2C-02, 2C-03, 2C-04, 2P1's old group D (side quest) |
| 3 | QC-R1 | twins 6A-T1, 6A-T2, 6A-T3 |
| 4 | 3C More List Tools, Quiz 3B, 3-A1 tuples, 3-A2 `zip()`, 3P2, QC3 | 3B-04 `.count`, 3B-05, 3P1 Training Log |
| 5 | 4-A1 `.get()`, QC4 | twins 4A-T and 4B-T, 4P's old groups D–E (side quest) |
| 6 | 5C comprehensions and `continue`, 5-A1 `.items()`, QC5 | 5B-05, 5P's old group D (side quest) |
| 7 | 6-A1 lambda, 6-A2 `map()`, 6-A3 two things back, QC-R2 | 6B-08 defaults and keywords, 6B-09 scope, 6P's old group D (side quest) |
| 8 | the whole unit | — |
| 9 | 8P1 Water-Stained Log (recommended), 8P2 Cipher, QC8 | 8A-04, 8A-05, 8A-08, Quiz 8A |

Syllabus goals that are now optional or pool only are default and keyword arguments (6B-08) and scope (6B-09).
6A-07's "Whose kitchen is `result` in?" sidebar covers scope at reading level for everyone.

## 1.5 Milestones and routes

- **Ready for Module 2.** All core items plus the Campaign Readiness Check (§5). This is the default goal.
- **Routes are a class-level teacher setting, never per student** (T2):
  - **Route M1** (recommended if the class has not played Module 1's coding parts [OWNER]): Units 1–3, then the
    10-minute **"Before the cabin door"** check (u03b), then campaign Module 1, then Units 4–10, then Module 2.
    Units 1–3 cover every line of Module 1, including `.lower().capitalize()` in 6A-08 (the M1 gate path proves
    it). The check is the teacher's signal for sending the class into Module 1, never a lock.
  - **Route M2:** the whole core runs before Module 2's coding parts. The rehearsals then serve as review.
- **Strings is the pacing lever.** If periods are short, the teacher runs Strings after Module 2 starts, or
  alongside it. The Readiness Check never depends on it.
- **No week calendar is shown to students.** The course map shows milestones (Unit badges, "Before the cabin
  door", "Ready for Module 2"). The teacher sets the class pace and holds sync points (§2.13).

## 1.6 Code, unit and file map

The prototype files run in file-name order, which is course order, and the concept gate follows that order.
Package detail is in §7.

| Unit | id (slug) | order | Codes inside | Prototype files |
|---|---|---|---|---|
| 1 Hello World | `hello-world` | 1 | 1-A1–1-A3, 1W, 1A, 1B, 1C, 1X-AB, 1X-C pools, Quiz 1, 1P1, 1P2, QC1 | `u01a`–`u01d` |
| 2 Control Flow | `control-flow` | 2 | 2A, 2B, 2C, 2X pool, 2-A1, 2-A2, Quiz 2, 2P1, 2P2, QC2 | `u02a`–`u02c` |
| 3 Functions I | `first-recipes` | 3 | 6A, 3X pool, Quiz 6A, Before the cabin door, QC-R1 | `u03a`–`u03b` |
| 4 Lists | `lists` | 4 | 3A, 3B, Quiz 3, 4X pool, 3C, Quiz 3B, 3-A1, 3-A2, 3P1, 3P2, QC3 | `u04a`–`u04b` |
| 5 Dictionaries | `dictionaries` | 5 | 4A, 4-A1, 4B, Quiz 4, 4P, 5X pool, QC4 | `u05a`–`u05c` |
| 6 Loops | `loops` | 6 | 5A, 5B, Quiz 5, 5P, 6X pool, 5C, 5-A1, QC5 | `u06a`–`u06b` |
| 7 Functions II | `spell-recipes` | 7 | 6B, 6C, Quiz 6B, 6P, 7X pool, 6-A1–6-A3, QC-R2 | `u07a`–`u07c` |
| 8 Trials | `code-challenges` | 8 | T-HCL, T-CF, T-L, T-D, T-Lo, T-F, T-Own | `u08a`–`u08c` |
| 9 Strings | `strings` | 9 | 8A, 8B, Quiz 8B, 9X pool, Quiz 8A, 8P1, 8P2, QC8 | `u09a`–`u09b` |
| 10 Readiness | `readiness-check` | 10 | RC Part 1 (forms A, B, C), Part 2 mini-boss (A, B), explain-a-line, spaced re-check | `u10a`–`u10c` |

Pool lessons are named by the unit they serve (1X, 2X, 3X …). The exercises inside keep their v1 ids (1A-07,
2C-02 …). Exercises merged in v2 keep their slug as a checkpoint id inside the exercise that absorbed them:
3A-04 → 3A-03, 3A-08 → 3A-05, 8A-02 → 8A-01, 8B-04 → 8B-03, 8B-06 → 8B-05.

---

# 2. Site experience

## 2.1 The exercise loop (how every lesson feels)

Every lesson has the same PRIMM / Use-Modify-Create shape (research P2, P3), so the routine itself becomes
familiar.

| Step | What the student sees | Rules |
|---|---|---|
| 0. **Mar'tu remembers…** | 1–2 recall items from at least two lessons back. From Unit 4 on, one is always a def/return item. Dictionaries and recipes come back in every later unit. | Authored as a small `quiz` item, `<lesson>-remembers`, rendered inline before the lesson. Unscored and skippable, **except** the one item tagged with a tested-out skill (under 1 minute, "Mar'tu checks your notes", G4 R21). A miss shows the answer and a one-line why, with no red X (G1 R31). Misses feed the spaced queue. |
| 1. **Learn pane** | Mar'tu's explanation, then a labeled **Example** with Run (and Step through, once the tracer ships). | ≤ 60 words before the first action in Unit 1 (lint f), ≤ 120 elsewhere. Example names and values are visibly different from the task, and listed in `foreign_names`. The Example is collapsible. The "Explain it another way" link lives here. |
| 2. **Predict** | A one-click choice or "type what it prints" **before** Run. | Free; a thinking prompt, not a test. A wrong predict about a return value or a reassignment opens the static trace table (or the tracer, once it ships). Accuracy feeds the fading rule and the lesson-end calibration line ("2 surprises, both about what a recipe hands back"). |
| 3. **Run and compare** | "Were you right? Which line surprised you?" (one click) | |
| 4. **Investigate** | 1–3 "change X and run" or "which line does Y?" prompts. | One-click choices, with free text optional (G3 R20). |
| 5. **Modify / Make** | Numbered checkpoints, one action each, checked in order. | **At least one checkpoint per lesson is non-dictated** (`dictates: false`): it gives the goal and "Names to use", never the code (T5, lint g). Checkpoints that spell out the line carry `dictates: true`. |
| 6. **Broken spell** | A debugging exercise with 2–4 bugs, one checkpoint per bug. | Can be done in pairs. |
| 7. **SOLO** | One item, ≤ 2 minutes: a **make-twin** in writing lessons (1B, 1C, 6A, 6B, 6C), **one bug** elsewhere (C6). | Values differ per seat. Recorded, never blocking, never shown to the partner. On a pass, Mar'tu says: "You did that alone. I saw." |
| 8. **Wrap** | The pulse: *too easy / just right / too hard*, plus the calibration line. | The pulse can only *add* support (C1). |

**On the exercise screen (architecture §3.1):** checkpoints show as ✓ passed, ● active and ○ locked. Each Run
re-checks every checkpoint, so a regression is caught. Only the active checkpoint's message is shown (§2.2).

**Point-at-it questions (G2 R9, AM).** After a pass on 1C-08, 2A-03, 4A-05, 4B-04, 5A-07 or 6A-06, or on any
`dictates: true` checkpoint, there is one unscored click: "Which part of your line is the *price of one*?" It
counts as "explains" evidence. It is hidden under "Keep it short" and instructions-light.

**How scaffolds fade across the course** (the function strand; each step drops at most one starter level,
lint c):

| Exercise | Starter level |
|---|---|
| 6A-02 | S3 skeleton |
| 6A-03 | S4 (`pass` placeholders) |
| 6A-04, 6A-05 | S3, two pre-written calls |
| 6A-06 | S3, with CP3 goal-only |
| 6A-08, 6A-09 | S3 / S2 numbered comments |
| 3A-06 | S2 |
| 6B-01 | S1 signature |
| 6B-03, 6B-07 | S4 (campaign placeholders) |
| 6C-05 | S2 (L1 numbered comments) |
| Readiness item 13 | goal plus an Example |
| Trials | signature only |

After a hint-free pass, the next similar exercise offers "Start from blank". After a failure, More structure is
one click inside Help (§2.2).

## 2.2 The help stack (binding contract for ExercisePlayer; T3, directive §4.3)

**After a failed run, the student sees exactly one message:**
- the explainer, if the program crashed (§2.6),
- otherwise the first failing check's message (§2.5).

Under the active checkpoint there is one **Help** control, and nothing else. There are no separate floating
offers, no cameo-plus-offer stacks, and no second Parsons button. Cameo lines appear only on a pass. After 3
failed runs, Oogrish's line becomes the Help control's label: "Steady, now. Read the last line first. Want a
nudge?"

**The Help control steps through these rungs.** Each step needs a Run or about 10 seconds:

| Order | Rung | Under "Show me more" | Under "Keep it short" |
|---|---|---|---|
| 0 | **Start me off**: inserts the line's left side or first tokens (authored `start`, or the solution's first line up to `=` or `(`) | in the stack | under "More options" |
| 1 | **Point**: where to look. Always available, even in light mode (G3 R7). | in the stack | in the stack |
| 1a | **Another way**: the next unseen angle, in the order picture → everyday → step-by-step → in Tor → shorter → from the campaign | in the stack | under "More options" |
| 2 | **Teach**: the concept, with a tiny example that is *not* the answer (its names go in `foreign_names`) | in the stack | in the stack |
| 2a | **More structure**: the next `starter_level` down (skeleton → blanks → Assemble it → worked twin). Hand-authored for campaign rehearsals and projects, auto-derived elsewhere. A step down is logged, and the next exercise starts back at its default. | in the stack | under "More options" |
| 3 | **Show**: the bottom-out line, then an **immediate, required typed twin** (§2.8) | in the stack | in the stack |

- **The Learn pane keeps its own "Explain it another way" link**, for before any failure. It serves the same
  angle bank.
- **Proactive offers highlight the Help control with one line. There is no modal.**
  - Triggers: 3 failed runs on one checkpoint, 4 minutes without progress, or **90 seconds with the editor
    unchanged and no Run** (the silent stall; G3 R6). Group 3 produces silence, not failed runs.
  - Under "Keep it short", only the failed-runs trigger is active.
  - One dismiss silences offers for that exercise. Offers turn off after a hint-free streak of 5 checkpoints.
- **Compare with Mar'tu's version** unlocks after 5 minutes, 4 failed runs, or when the ladder is used up.
  - "Retype it" is the default.
  - An immediate twin is required before the checkpoint stops counting as assisted. The spaced twin is still
    queued.
  - An optional one-click "what was different?" follows (G4 R23).
- **"Names to use" chips** show every exact name the active checkpoint requires (variables, functions,
  parameters), in every mode (C11, G4 R7).
- **The symbol tray** (`█ ░ ▮ ▯ ▓`, plus `"` and `_`) lives in the editor toolbar (G1 R8). Every bar starter
  also pre-types its blocks.
- **Coach marks, just in time** (C15): the Help control is explained on the first failed check, Another way on
  the first offer, Assemble it on the first More structure, and Try other numbers on the first CMB failure.
- **Explainer footer** from 1W-02 on: "Read the last line first. Then look at the line it names." The full
  four-step routine is taught in 2C-07.
- Hint use, offers and step-downs are private to the student, and logged for the teacher.

## 2.3 Presets and layered defaults (C1, C4, C8, C11)

**Placement.** The first-visit question sets the starting preset:
- no answer, "never" or "a little" → **"Show me more"**;
- "yes" → "Show me more", with QC1 offered first (never an automatic "Keep it short").

The teacher may pre-set either preset provisionally. **Self-report and the pulse can only add support.**
Support fades only on performance:
- a hint-free streak of 5 checkpoints offers the next lighter layer;
- a QC pass sets "Keep it short" for that unit;
- predict accuracy ≥ 80% over a lesson collapses the Example by default.

The student can switch presets at any time. There is no visible preset badge.

| Layer | "Show me more" (default) | "Keep it short" | Instructions-light (opt-in on a streak or QC pass) |
|---|---|---|---|
| Learn pane | open; more pictures and steps, **not more words** (G1 R28) | Example and flavor collapsed | goal sentence + Names to use + signature only |
| Labeled-box picture (1B), static step tables | shown by default | one click | one click |
| Warm-ups 1W | on | off | off |
| A-stage exercises (2B-05, 4B-05, 6C-04, 6C-05, 6A-03) | Assemble-first view (C4) | typed campaign-style starter, Assemble as a fallback inside Help | typed starter; **rehearsal starters are never trimmed** |
| Help rungs | full stack | rungs 1, 2 and 3; the rest under "More options" | same as "Keep it short"; Point always available |
| Proactive offers | all three triggers | failed-runs trigger only | failed-runs trigger only |
| Point-at-it questions, example-name heads-up | on | hidden | hidden |
| Names to use chips, explainer, glossary, read-aloud | on | on | on |
| Project starters | task-group headers + placeholders + full ladder | task-group headers | task-group headers |
| Quick Check offered first | no | yes | yes |
| Capstone-first offer | after a hint-free streak | after a streak or a QC pass | after a streak or a QC pass |
| Calm mode | independent, off by default | independent, off by default | independent, off by default |

## 2.4 Item kinds

| Kind (format `kind`) | Shape | Grading | Support |
|---|---|---|---|
| **Lesson** (`lesson`) | Warm-up item, then 5–14 exercises in PRIMM order, ending with Broken spell and SOLO. | Auto-checked checkpoints. | The full help stack. |
| **Mar'tu remembers** (`quiz`, 1–2 questions) | Inline warm-up before a lesson. | Unscored. One item required when it carries a tested-out skill. | None needed. |
| **Quiz** (`quiz`) | 6–8 questions: mc, predict, fill, parsons, bug. One per card. **Every unit quiz has at least one def/return item from Unit 4 on.** | Review order for everyone: what you got right, then "worth another look" with "Review this" links, then the score (G1 R26). Unlimited retakes with reshuffled choices. A "Ready" badge at 70%, which never blocks. | No hints. "Show choices" turns a predict into mc. |
| **Trace table** (new item type, Unit 3 gate) | A program plus a ledger with one row per box. The student fills each row before Run. Each row is checked as typed, with targeted messages for documented wrong values. | Per row. | Tracer to check afterward (once it ships). |
| **Project** (`project`) | Premise, task groups (headers always in the starter), and one editor. The dropped v1 task group is the project's Lucky side quest. | Every task is auto-checked, behavior-based. "Use Mar'tu's picks" fills all creative blanks (G4 R19). | Light by default; the full ladder under "Show me more". Trial mode after a QC pass: premise, required output and check table, from blank. |
| **Challenge** (`challenge`) | A signature plus a test table (visible tests, then hidden labeled ones). Core and advanced variants. | Test table. A hidden test names its label ("an empty wall"), not its values. | Light. Explainer always on. |
| **Article** (`article`) | Readable page, runnable examples, and an optional try-it. | "Mark as read". | Full on the try-it. |
| **Cheatsheet** (`cheatsheet`) | "Mar'tu's chalk notes": a concept, a snippet, its output, and a note linking back to its exercise. Printable. | — | — |
| **Extra practice** (`lesson`, `optional=True`) | The pool: deferred v1 items and twins. | As a lesson. | Full. Fed into twins, the spaced queue and early finishers. |
| **Quick Check** (two `testout` forms + two `quiz` forms) | `qcN-a` / `qcN-b` hold the code tasks (`support="none"`). `qcN-a-questions` / `qcN-b-questions` hold the predicts and mc. About 10–12 minutes. | Pass = every code task plus 80% of the questions. A retake draws the other form. | No hints, tracer or compare. Glossary, read-aloud, DF and the explainer stay on. |
| **Readiness Check** | Part 1 (13 items, three forms), Part 2 mini-boss (two forms, campaign mode), explain-a-line, spaced re-check (§5). | Per-skill routing. | §5. |

**Quick Check rules (directive §4.5).**
- **Coverage.** Every skill a QC claims has an item that can fail on the documented error. The coverage table is
  in each QC's §3 entry, and lint (d) enforces it. A skill without one shows **"not yet"**, never "tested out".
- **"Tested out (provisional)"** is shown apart from "Complete" until a typed spaced item or the Readiness
  re-check confirms it. Each tested-out skill gets the required one-minute recall item in later warm-ups.
- **Conversion on a pass** (G4 §3; exercise-level routing lands by the Unit 2 release):

  | Item | On a QC pass it becomes |
  |---|---|
  | a lesson whose skills all passed | its capstone (the last Make checkpoint plus SOLO) in light mode, with "Start from blank" |
  | a lesson with failed skills | only the exercises tagged with those skills, plus their SOLO lines |
  | the unit project | Trial mode: premise, required output and check table, from blank |
  | the unit quiz | optional |
  | a campaign rehearsal (2B-05, 6A-03, 6A-08, 6A-09, 6A-10, 6B-07, 6C-04, 6C-05) | its Start-from-blank version, keeping the campaign-style comments |
  | a story beat (2P1, 4A-01, 5A-05, 5B-04) | a "Mar'tu's notes" line or a 2-minute "Mar'tu wants to show you something" item |

## 2.5 Check library (every checkpoint in §3 cites these codes)

Checks test **behavior**, not text:
- They call the student's functions with fresh values.
- They rerun the program with changed inputs.
- They accept any quoted text the student picks, so silly, personal and in-world values all pass.

Messages are one sentence. Each says what the code did, what was expected, and the next step. They use plain
words, the terminology contract (§2.9), and **invented values only** (§2.11).

| Code | Rule | Example message | Catches (evidence) |
|---|---|---|---|
| **NAME** (extended) | Exact required name. Near misses are recognized: names in `foreign_names`, case, plural, case-plus-plural, and 1–2 edits. Shown with a letter-diff (`hea`**`l`**`th`). | "Python matches names letter for letter: you wrote `Max_Mana`, the task needs `max_mana`." | A-05/A-06/A-07/A-08 `player_name`; A-08 `heath`; B-02/B-03 `Pizza`/`pizzas` |
| **LEFT** | An identifier that appears only in `foreign_names` (the example, Teach-rung examples, the previous exercise's required names). Non-blocking heads-up when behavior passes; blocking when it breaks behavior. | "`total_frait` comes from the example. This task's box is `total_cost`." | A-08 `total_frait`; hint names `a`/`b` |
| **TEXT** | The value is a non-empty `str`. Any text is accepted. | "`character` holds `7`. This step wants text in quotes." | unquoted text (A-05, A-08, B-01) |
| **NUM** | The value is an `int`, not `"3"`. | "`armor_bonus` holds the text `"3"`. Numbers don't need quotes." | quoting numbers |
| **BARE** | A top-level statement that is only a string or number. It raises no error, so a check must catch it. | "Line 1 is a value with no box, so Python made it and forgot it. Put `character = ` in front of it." | A-04, B-02, B-03 lone values (G1 R4, G3 R1) |
| **CMB** (extended) | `_rerun(values={...})` re-executes with changed inputs and expects the result to follow. The failure message includes a **rerun table** (input / your result / expected). The same mechanism drives the **Try other numbers** button. | "When `lantern_count` became 7, `total_cost` stayed 22. Build it from the boxes." (table follows) | everyone's 68 |
| **SWAP / LINE-TOTAL** | A slot holds another input's value; or a multiplier slot holds a line total. | "You swapped them: 3 is how many lanterns, 4 is the price of one." / "12 is already the cost of all 3 lanterns. This box wants the price of one." | A-05/A-07/A-08 pizza error; placeholder swaps |
| **NEWBOX** | A new name holds the expected value while the starter's box keeps its placeholder. | "Your new box `my_total` holds 22, but `total_cost` still holds 0. Put it in `total_cost`." | G3 side-work habit |
| **OUT** (diff) | Exact-output checks show the expected and actual lines aligned, with the first difference marked. **Never the only check on a computed value** (lint a). | "Expected `Lucky has 26 mana.` · You printed `Lucky has26 mana.` (a space is missing here ^)" | `Lucky has26mana.` |
| **STREXACT** | A comparison literal differs from the expected text only by case or spaces. | "`"Option 1"` and `"option 1"` are different text to Python: every letter, space and capital counts." | A-07 `"Fire ball"`; B-03 `fireball` |
| **PAR** | Calls the student's function with **two fresh argument sets** the task never uses. **No fresh set may give the same result as a call written in the task** (lint b). | "`warn("Tester")` printed `Lucky, get inside!`. Use the parameter `hero_name`." | A-06/A-07/B-02 `10 * 5`; A-08 `25 * 2` |
| **PAR-CONST** | Two fresh calls return or print the same thing. The message includes a **call table**. | "`max_mana_for(9)` and `max_mana_for(12)` both gave back 26. A recipe gets its numbers when it is called: use `affinity`." | A-06 `return 50`; A-02/A-03/A-04 unrelated literals |
| **PNM** | A NameError inside a student function names a near-miss of a parameter (substring, a shared `_` word, ≤ 2 edits). Explainer rule 2. | "This recipe's ingredients are `base_damage` and `bonus`. You wrote `damage`. Python matches names letter for letter." | A-01 `attack` |
| **RET** | The function **returns** the value. Detects `None` and print-instead-of-return. | "`max_mana_for(9)` printed 18 but handed back `None`. Use `return total`." | B-02 blank `return`; A-07 |
| **RET-PARAM** | The function returned one of its own parameters. | "`armor_total(10, 3)` handed back 10, which is `base` as it came in. Hand back the box you computed." | A-07 raw inputs |
| **RNM** (fuzzy) | A NameError inside a function names something ≤ 2 edits from a `foreign_names` id. Explainer rule 3. | "`reslt` looks like `result` from the example. This recipe's box is `total`." | A-01 `return reslt` |
| **DEF** | `def` used to make a box. The explainer handles the SyntaxError. | "`def` makes a recipe. To make a box, write `name = value`." | A-02 `def ("character")` |
| **BND** | Boundary test at `needed - 1`, `needed`, `needed + 1` and "exactly enough". `needed` is read from the student's own code, so any chosen difficulty passes. | "With a roll of 12 and `needed = 12`, your check said fail. Exactly enough should pass: use `>=`." | campaign `<` versus `<=` |
| **RND** | `_rerun(rolls=[...])` scripts `random.randint` and records its arguments. | "`roll_die(6)` rolled `random.randint(1, 20)`. Use the parameter: `random.randint(1, die_size)`." | literal sizes; the exclusive-range belief |
| **CALL** | Setup helpers record every call; checks read the record. | "`step_south()` moved the scout north. Use the direction in the recipe's name." | copy-paste branches |
| **STO** | Inside the named function, a call's result is assigned to a variable, and that variable is passed on. | "Store what `get_greeting()` returns in a variable first, then pass that variable to `show_on_ley_board()`." | the campaign's stored-variable check |
| **NOP** | A function is handed over as a value. Detects `None` where a recipe was expected. | "You ran `warm_hands(lucky)` and handed over what it gave back (`None`). Hand over the recipe itself: `warm_hands`, no parentheses." | `strengthen_magic` without `()` |
| **LOOP** | Reruns with a roster or list of another length. The output must follow. | "With 5 heroes in `roster`, only 4 lines appeared. Use a `for` loop." | hard-coded repetition |
| **KEEP** | Code marked "already finished" is unchanged (AST compare). | "`draw_bar` changed. It is already finished, so leave it as it is." | P19 reading discipline |
| **KEY** | Dict keys are exactly as specified. | "`gearshift` has a key `"Max_Mana"`. The sheet uses `"max_mana"`." | exact-name evidence |

**Helpers** (approved, directive Q11): `_rerun(values=None, rolls=None, stdin=None)` returns
`(namespace, printed_lines, randint_calls)`. Also `_calls(helper)`, `_func_ast(name)`, and `_near_names(name)`
with plural and case-plus-plural support. `foreign_names` is read from the exercise.

**Authoring rule (kept):** checks must stay true as later checkpoints are completed. Use `'48' in _lines()`, not
`_lines() == ['48']`.

## 2.6 Explainer precedence tree (course `explain` mode; directive §4.1)

**Titles.** Each message leads with a plain title and puts the error name second, in parentheses ("Python
couldn't read line 3 (SyntaxError)", "Python found a name it doesn't know (NameError)"). When the previous run's
error is fixed and a new one appears, the message is prefixed with "One fixed. Python found the next one:". The
panel style is neutral and non-red (G1 R24).

**NameError: name 'X' is not defined.** The first matching rule wins. Each row's **proving wrong answer** is a
`wrong_answers` entry in the exercise named.

| # | Rule | Message | Proven by |
|---|---|---|---|
| 1 | X is `___` (only underscores) | "Fill in the blank `___` on line N." | 6A-05a WA "blank left" |
| 2 | Raised inside a function body, and X is a near-miss of that function's parameter | **PNM**: "This recipe's ingredients are `base_damage` and `bonus`. You wrote `damage`. Python matches names letter for letter." Python's suggestion is dropped if it is a keyword or builtin. | 6A-05 WA `print(damage + bonus)`; QC-R1 C1 WA `base + bonus` |
| 3 | X is ≤ 2 edits from a `foreign_names` id | "`reslt` looks like `result` from the example. This task's box is `total`." / "`a` comes from Mar'tu's hint example…" | 6A-07 starter (`return result`); 6A-07 WA `return reslt` |
| 4 | X is the checkpoint's required name, and the source has a bare value statement | "Line N has `"Zelda"` on its own. Python made the words and forgot them, because they're in no box. Write `character = "Zelda"`." (quotes the student's own line) | 1B-02 WA lone `"Zelda"` |
| 5 | Python says "Did you mean: 'Y'?", Y is user-defined, and X is the task's required name | "Python found two names that almost match: `max_mana` and `Max_Mana`. Use the spelling the task asks for (`max_mana`) in both places." | 1B-04 starter (verified: "Did you mean: 'Max_Mana'?") |
| 6 | "Did you mean: 'Y'?" with Y user-defined | Pass it through in plain words, adding "capitals and plurals count". If Y is a keyword or builtin (`Print` → `print`), say so plainly: "Python's commands are lower case: `print`." | 2C-03 WA `mama` → `mana` (pool); 1A-08 `Print(` |
| 6b | "Did you forget to import 'random'?" | "Add `import random` as the first line." | 2B-09 starter |
| 7 | The whole line is just X | "This line is just a name by itself, so Python looked for a box called `Zelda` and found none. To make a box: `name = value`. To show words: `print("words")`." | 1B-06 WA bare `Zelda` line |
| 8 | `X - value` where `=` was meant | "To put a value in a box, use `=`. The `-` sign subtracts." | 1B-02 WA `character - "Zelda"` |
| 9 | Otherwise | **In 1A** (no "box" yet, G1 R23): "Python thought `Fireball` was the name of something saved earlier (you'll make those next lesson) and found nothing. Words you want to show need quotes." **From 1B on:** "If you meant the words, put them in quotes: `"Fireball"`. If you meant a box (variable), make it first with `Fireball = …`." | 1A-04 starter; 1B-02 WA `character = Kratos` |

**SyntaxError and IndentationError.** The first match wins.

| Trigger (all verified in 3.13.18) | Message | Proven by |
|---|---|---|
| `unterminated string literal` and the line has the *other* quote type after the opening quote | "You opened with `"` and closed with `'`. Use the same mark at both ends." | 1A-03 WA `print("It is not a compass')` |
| `unterminated string literal` (otherwise) | "A quote opened on line N but never closed. Quotes come in pairs: one before the words, one after." | 1A-03 starter |
| source has `''word''` (two apostrophes as a quote; Python says "Perhaps you forgot a comma?") | "Two `'` marks are not one `"`. Use the `"` key." | 1A-03 WA `print(''Shield up'')` |
| `'(' was never closed` | "A `(` opened on line N and never closed. Brackets come in pairs too: add `)` at the end." | 1A-03 Investigate `print("Shield up."` |
| `invalid decimal literal` (a digit followed by a letter) | "Python doesn't read `3L` as '3 times L'. Put `*` between a number and a box, or better, use the boxes you made." | 1C-03 WA `total_cost = 3L + 5R` |
| a line starting `def` that isn't `def name(...):` (Python: `expected '('` or `invalid syntax`) | "`def` makes a recipe (a function). To make a box (a variable), write `name = value`, with no `def`." | 1B-06 starter `def companion = "Gearshift"`; 2C-06 starter |
| `cannot assign to literal` with a quoted name on the left | "The name of a box never goes in quotes. Write `weapon = "Telegun"`." (Python's own `==` hint is dropped.) | 1B-06 starter |
| `invalid syntax` with two bare words before `=` | "A name can't have a space in it. Join the words with `_`: `magical_affinity`." | 1B-04 starter `magical affinity = 9` |
| `invalid syntax` with two or more bare words after `=` **or `==`** | "These look like words. Put all of them inside one pair of quotes: `"option 2"`." | 1B-02 WA `character = Captain Glug`; 2B-05 WA `elif choice == option 2:` |
| `Perhaps you forgot a comma?` with two adjacent bare names inside `( )` (C13) | If either word is a defined name: "A name can't have a space in it; use `_`. (If you meant words, put them in quotes.)" Otherwise: "These look like words; put them all inside one pair of quotes. (If you meant one name, join it with `_`.)" | 1A-04 Investigate `print(Get inside)` |
| `invalid syntax` or `forgot a comma?` on a line inside `{ … }` | "Inside a dictionary, items are separated by commas. Check the end of line N **and** the line above it." | 4A-02 WAs (int value: reported on the line itself; string value: reported on the next line; both verified) |
| `invalid syntax. Maybe you meant '==' …` on an `if` line with `=` | "`=` puts a value in a box. To ask 'is it the same?', use `==`." | 2B-09 starter `if roll = 20:` |
| `expected ':'` | "A line that starts `if`, `elif`, `else`, `for`, `while` or `def` ends with `:`." | 2B-02 starter |
| `IndentationError: expected an indented block after 'if' statement` | "The lines that belong to this `if` must be indented under it (4 spaces)." | 2B-02 starter |
| `IndentationError: expected an indented block after function definition` | "A recipe needs at least one line inside it, indented. Write `pass` for now." | 6A-02 WA empty body |
| `invalid syntax` on an `elif` that follows `else` | "`elif` must come before `else`. `else` is always last." | 2B-09 starter |

**TypeError, KeyError, AttributeError, IndexError** (v1 rows, kept):

| Raw message | Explainer |
|---|---|
| `can only concatenate str (not "int") to str` | "You glued text to a number. Wrap the number in `str()` first." |
| `unsupported operand type(s) for -: 'str' and 'int'` | "Python did `"░" * a` first, then tried to subtract from text. Put the subtraction in parentheses: `"░" * (a - b)`." |
| `unsupported operand type(s) for -: 'int' and 'str'` | "One side is a number and the other is text. Remove the quotes from the number." |
| `'>=' not supported between instances of 'int' and 'str'` | the same, for comparisons |
| `KeyError: 'dexterity'` | "The dictionary has no key spelled exactly `'dexterity'`. Check spelling, capitals and quotes, and whether it lives one level deeper (`["abilities"]["dexterity"]`)." |
| `'dict' object has no attribute 'mana'` | "Read a dictionary with square brackets: `hero["mana"]`." |
| `'list' object has no attribute 'join'` | "`join` belongs to the separator: `" ".join(words)`." |
| `'NoneType' object is not callable` | "This box holds `None`, not a recipe. Did you run the function (with `()`) when you meant to hand it over (no `()`)?" |
| `can only concatenate str (not "NoneType") to str` | "A function gave back `None`. That usually means it has no `return` line." |
| `'NoneType' object is not subscriptable` | "`.sort()` changes the list and gives back `None`. Use `sorted(wall)` for a new list." |
| `list indices must be integers or slices, not str` | "`roster` is a list, so use a position number like `roster[3]`. Names work as keys in dictionaries." |
| `can only concatenate list (not "int") to list` | "`+` joins two lists. To add one item, use `.append(33)` or `+ [33]`." |
| `'str' object does not support item assignment` | "Strings can't be changed in place. Build a new one: `"C" + word[1:]`." |
| `IndexError: list index out of range` | "This list has 7 items, at positions 0 to 6. Position 7 doesn't exist." |
| step-limit / too much output | "Line N ran 200,000 times. Does something inside the loop ever make the condition False?" |

**Silent-but-wrong notices** (no error at all):
- **BARE**: delivered as a check message (§2.5).
- **None notice**: if a printed line is exactly `None` and the program defines a function with no `return`, one
  line appears under the output: "`None` means a recipe handed nothing back. Does it have a `return`?" Proven by
  the 6A-06 Investigate.
- **`error_type = NameError`**: it runs silently (verified). A TEXT special case in 2C-01: "`NameError` without
  quotes is Python's own name for that error. Write the words in quotes: `"NameError"`."
- **NEWBOX**: delivered as a check message.

Every row is a table-driven case in `explain.test.ts`, and every NameError rule has a precedence test proving the
right row wins (T6).

## 2.7 Accommodations: opt-in layers, each removable (expertise reversal)

| Feature | What it does | Who it serves (evidence) | How it avoids hurting others / how it fades |
|---|---|---|---|
| **Explain it another way** | ≥ 3 genuinely different angles for Unit 1 concepts and CC skills, ≥ 2 elsewhere. Angle types: picture, everyday, step-by-step, in Tor, shorter, from the campaign, contrast gallery ("Not this", invented values), sentence frame. | G1 "the same idea from another angle, not louder"; G2 meaning over shape | Collapsed. Served inside Help as the next unseen angle, never auto-popped. Usage logged so weak angles can be retired. |
| **Glossary** | Hover or tap on `[[term]]`, plain definition first. Adds *defined / not defined, syntax, run, call, value, assign, indent, method* (G1 R21) to *string, variable, parameter, argument, return, key, index, concatenate, None*. | G1 | Inline, dismissible, on in QCs and the Readiness Check (G1 R25). |
| **Static step tables → step-through tracer** | Unit 1 ships static step tables (1B-05, 1C-04). The trace-table item type (6A-06b, retrofits in 5A-04, Quiz 6A, Readiness) blocks Unit 3. The live tracer (nested boxes, call/return arrow) comes by the Dictionaries gate. | G1 traced by adding constants; G2 "return = 3 + 4" | Open by default only under "Show me more". Hidden in QCs and Readiness Part 1. |
| **Read aloud** | Web Speech reads Mar'tu's text and the instructions. An authored `say` text reads code naturally: `=` is "gets", `==` is "is the same as" (G1 R10). | G1, English learners | A button. Hidden if the device has no voices. |
| **Assemble it (Parsons)** | A More-structure level on any exercise. Adaptive: after 2 failed checks it removes a distractor or merges two blocks. Indentation is part of the puzzle. | G2 erased functions; G3 stalls at a blank | Assemble-first only on A-stage exercises under "Show me more". **An Assemble pass is followed by a 1–2 line typed twin**, and mastery needs typing. |
| **Start me off / More structure** | Rung 0 and rung 2a of Help (§2.2). | G3 | Logged. The next exercise starts back at its default level. |
| **Proactive offers** | Highlight Help with one line on 3 failed runs, 4 minutes, or a 90-second silent stall. | G1 won't ask; G3 goes silent | One dismiss silences them. Off after a streak. Only the failed-runs trigger under "Keep it short". |
| **Try other numbers** | Reruns the student's program with other inputs and shows the table. Introduced at 1C-01. | G2 "catching my own mistake" | Optional button, by the Unit 2 release. The table appears inside CMB failures from Unit 1. |
| **Pair mode with solo items** | The teacher assigns pairs (anonymous seat ids). Prompts name seats: "Seat A predicts, Seat B runs", "Swap seats", "Explain to your partner why this passed". Each lesson's SOLO item is per seat, with different values, and hidden from the partner. | A-03/A-04, the B section | Off by default. The course never auto-pairs (C5). Two seats on one device only if devices are shared **[OWNER]**. |
| **Instructions-light mode** | Goal sentence + Names to use + signature. Never trims rehearsal starters. Explainer stays on. Point is always available. | G4 "redoing variables I already know" | Offered after a hint-free streak or a QC pass. One click to turn off. |
| **Collapsible examples and flavor; Calm mode** | Collapse Examples and story lines. Calm mode hides cameos. | G4 | Independent toggles. Story beats stay one tap away. |
| **Mar'tu's pick (DF)** | "Can't decide? Use Mar'tu's pick" on every open prompt, inline on example-copy failures (C3), "use Mar'tu's picks" in projects, and available in QCs. | A-01 "can't think of a character" | Optional. Every quoted value is still accepted. |
| **Quick Check test-outs** | §2.4. Two forms, coverage tables, conversion, provisional status. | G4, and anyone who feels ready | A failed attempt costs nothing. Every pass is re-verified. |
| **Capstone-first** | "Try the last one first?" Pass it hint-free, and the teaching exercises are marked "passed by capstone" (except skills it doesn't check). Fail it, and the student drops to exercise 1 with no penalty. | G4 R11 | Offered only after a hint-free streak or a QC pass (C14). From the Unit 2 release. |
| **Lucky's side quests and the Trials** | At least one **combining** side quest per lesson (G4 R16): it mixes two ideas instead of repeating one. Plus the Trials unit, "Mar'tu's seal" and The Hard-Coded Ledger. | G4; anyone on a fast streak | Never required. Framed as side quests, not "advanced". |
| **"Why does this work?" sidebars** | Precedence, mutation through a parameter, unique keys, `.sort()` returning `None`, "Why the recipe can't know the numbers yet", "Whose kitchen is `result` in?". | G4 | Collapsed. |
| **Mastery map** | §2.8. | G3 "a checklist of what I've mastered" | Private to the student and the teacher. No comparison view. |
| **Warm-ups 1W** | What an error looks like (with the explainer footer), and where `"`, `(`, `)`, `_`, `-`, `=` and `#` are. | G1 | Contingent: on under "Show me more". |
| **No timers, leaderboards or public scores** | Nothing is timed, ranked or public. | G1 | Everyone. |

## 2.8 Mastery evidence and the skills map (T5)

**Evidence levels.** Each skill on the map ("Mar'tu's chalk wall of skills") shows one of these levels:

| Level | Earned by |
|---|---|
| **not yet** | no evidence, or a QC skill with no failable item |
| **with structure** | passes after Assemble it, Start me off, More structure or a reveal, or at starter level S4 |
| **from comments** | unassisted typed passes at S2–S3 |
| **from blank** | unassisted typed passes at S0–S1, or on a non-dictated checkpoint |
| **solid** | from comments or from blank **twice**, at least once on a SOLO, QC, spaced or Readiness item. Dictated, assembled or revealed passes never make a skill solid. |
| **tested out (provisional)** | a QC pass, until a typed spaced item or the Readiness re-check confirms it |

- **Together and solo are separate positive ticks** (G3 R16). Neither is a failure.
- **After a reveal**, an immediate typed twin is required before the checkpoint stops counting as assisted. The
  twin uses the student's own values where there is a creative slot. A spaced twin is also queued.
- **After an Assemble pass**, a 1–2 line typed twin follows.
- Every typed QC and Readiness item is behavior-checked (CMB, PAR, BND, CALL), never OUT alone.
- **Mastery map v1** is due by the Lists release (Unit 4).

**Skills** (each checkpoint in §3 lists its skill tags; **CC** marks campaign-critical skills):

| Unit | Skills |
|---|---|
| 1 | `print-text`, `quote-text` **CC**, `make-variable` **CC**, `exact-names` **CC**, `numbers-vs-text`, `reassign` **CC**, `combine-values` **CC**, `concat-str` **CC**, `repeat-string` **CC** |
| 2 | `compare` **CC**, `boundary` **CC**, `if-else` **CC**, `elif-chain` **CC**, `and-or-not`, `randint` **CC**, `read-traceback` **CC** |
| 3 | `def-call` **CC**, `replace-pass` **CC**, `param-use` **CC**, `return-value` **CC**, `return-right-name` **CC**, `trace-call` **CC**, `store-then-pass` **CC**, `return-comparison` **CC**, `randint-param` **CC**, `chain-methods` **CC** |
| 4 | `list-make` **CC**, `list-index` **CC**, `list-append-len`, `list-nested`, `range-slice-sort` |
| 5 | `dict-make` **CC**, `dict-read` **CC**, `dict-write` **CC**, `dict-in` **CC**, `dict-key-from-variable` **CC**, `dict-nested` **CC**, `list-of-dicts` **CC** |
| 6 | `for-each` **CC**, `accumulate`, `loop-with-if`, `while-loop`, `break` |
| 7 | `func-takes-dict` **CC**, `dict-from-params` **CC**, `store-by-name` **CC**, `early-return` **CC**, `read-helper` **CC**, `func-as-value` **CC**, `call-stored-func` **CC**, `none-return` |
| 9 | `string-index-slice`, `string-methods`, `split-join`, `fstring-read` |

## 2.9 Terminology contract (all student-facing text, glossary and read-aloud)

| Idea | First units | From Unit 4 / Functions II on (the campaign's words) | Read aloud |
|---|---|---|---|
| variable | "box (variable)" in Units 1–2; **no "box" in 1A** | "variable" (Mar'tu may still say "box") | `=` is "gets" |
| `==` | "is the same as" | same | "is the same as" |
| function | "recipe (function)" in Unit 3. **"Recipe" is never used for anything but `def`.** Unit 1 says "show your working". | "function" by Unit 7 | — |
| parameter / argument | "ingredient (parameter)" / "what you hand over (argument)" | "parameter" / "argument" | — |
| dictionary key | "label (key)" | "key" | — |
| return | "hands back (returns)" | "returns" | — |
| quotes | **"Quotes mean these exact letters. No quotes means look inside the box with this label."** Word for word, every time. | same | — |
| combining values | "show your working" | "build it from the variables" | — |
| chalk-wall values / differences | "gaps" / "shrink" | same | — |
| "matching" (placeholders) | used only for an **exact** name, from 6B-03 on | same | — |
| rehearsal phrasing | — | the campaign's own: "Replace each `pass` with…", "replace each placeholder with the matching parameter", "Store the result of `…` in a variable", "Pass that variable to `…`" | — |

## 2.10 Campaign mode (T4)

**Where it applies:** 6C-04, 6C-05, 6P and Readiness Part 2 (the mini-boss).

**What the student gets** (exactly what the campaign gives):
- numbered comments and numbered instructions in the campaign's phrasing;
- check messages and the explainer;
- Compare with Mar'tu's version after 5 minutes;
- hints capped at rung 2.

There is no Assemble it, no tracer, no auto-offered angles and no Start me off.

**The 6C-05 exception.** Under "Show me more", 6C-05 keeps its four-level More-structure ladder (L1 is the
default for everyone). A pass below L1 is recorded "with structure". The mini-boss is campaign mode for everyone.

**Explainer parity.** Until the campaign's `explain.ts` gets the improved rows (a separate PR, §6.3), the
Readiness review screen says plainly: "The campaign's error messages are shorter than Mar'tu's. Read the last
line first, the same way."

## 2.11 Privacy and classroom safety (T10)

- **No student's written value appears in content.** That covers joke names, food strings and anything that
  could be a first name. It applies to check messages, "Not this" galleries, Parsons distractors and quiz
  choices. Use invented values: `"Zelda"`, `"Kratos"` (fictional), `"Captain Glug"`, `"a grumpy moth"`,
  `"Tester"`. Sheet IDs appear only in this document and in harness `notes`, never in client bundles.
- **Echo spots** are the only places Mar'tu repeats a typed value: 1A-02, 1B-02, the 1P1 watch-keeper, 2P1's
  encounter tiers, and 8B-08. The echo shows only on the student's own screen. It goes through a blocklist with
  a generic fallback ("Hm. Noted."), and a **class-level teacher switch** turns it off.
- Echo, hero persistence (Tier 3) and the sandbox (Tier 3) are local only. Nothing a student types goes to the
  classroom API. Architecture §5.2 already forbids code and free text, and the privacy test is extended to the
  new summary fields.
- There is no visible preset badge. Hint use is private to the student and the teacher.

## 2.12 Authoring rules and lints (verifiable)

1. **Concept gate.** Code a student sees (starter, example, solution, partials, quiz code, cheatsheet, side-quest
   solution) uses only tokens introduced earlier in course order, or in the same exercise (`preview` with a
   justification otherwise).
2. **Core-only rule.** Core items rely only on tokens first introduced in core items. Pool and optional items
   may use earlier optional tokens only if they name the prerequisite item, which the UI shows as a recap card.
   The v2 gate script checks the CORE, CRIT, M1, READY and TRIALS paths.
3. **Setup gotcha.** The tokenizer exempts attributes on names that hidden `setup` defines. Data whose methods a
   lesson teaches must be built in the **visible starter**. Only engine-like helpers (`scout`, `ley_board`,
   `show_on_ley_board`, `mar_tu_says`, `light_up_box`, `draw_bar`, `light_lantern`, `lantern_ward`, `show_mana`,
   `get_warning`) and prebuilt rosters live in setup. Found again in v2: `lucky.get(...)` on a setup-made
   `lucky` hid `attr:get`, so 4-A1 builds its own `hero`.
4. **Engine names are off-limits** as student variables (`party`, `user`, `stage`, `print_prompt` …). The course
   uses `roster`.
5. **Examples use different names and values** from their task, are labeled "Example", and their identifiers go
   in `foreign_names`, along with Teach-rung example names and the previous exercise's required names.
6. **Checkpoint text:** one action, ≤ 2 sentences, numbered by the UI, code in backticks. The target is FK grade
   ≤ 6 (the harness warns above 9). Learn text before the first action: ≤ 60 words in Unit 1, ≤ 120 elsewhere.
7. No lore in checkpoints, check messages or quiz answer logic.
8. **Hints and wrong answers.** Every checkpoint has ≥ 2 hints (target 3: point, teach, show) and at least one
   `wrong_answers` entry from the evidence. Each entry cites the sheet ID in `notes` only. **Distractors**
   (Parsons and mc) come from documented slips across all four groups, at most 3 per puzzle, with invented
   values.
9. Never print a function object or a random value in an `example_output`.
10. Formatting is off for the course (architecture §4.7).
11. **Every exercise has its own starter.** Nothing carries over from the previous exercise unless designed.
12. **Shared-code safety.** Course changes to `explain.ts`, ConsolePanel and the worker are additive behind the
    `"course"` prelude flag, and campaign tests stay green (T12).
13. **Rehearsal exercises** (2B-05, 6A-03, 6A-08, 6A-10, 6B-07, 6C-04, 6C-05, Readiness Part 2): numbered
    comments map one-to-one onto checkpoints, and the checkpoint text copies the campaign's phrasing.
14. **New fields** (schema and exporter work, §6.3). Until the exporter accepts them, write them as the first
    line of the exercise's `notes`, in this form:
    `meta: starter_level=S3; path=CC; skills=make-variable,exact-names; solo=false; dictates=2; foreign_names=companion,player_name; par=("Tester",),("Moth",)`.
    - `starter_level` (S4 blanks or placeholders · S3 left sides or a skeleton · S2 numbered comments ·
      S1 signature · S0 blank)
    - `path` (CC / SC / pool / optional)
    - `skills`
    - `solo`
    - `dictates` (the list of dictating checkpoint numbers)
    - `foreign_names`
    - `par` (the fresh argument sets)
    - `twin` (a dict like `bonus`: text, starter, checks, solution)
    - checkpoint `start` (Start me off text, when not derivable)

15. **Assemble it blocks** (the `assemble` field, which the harness now verifies). The right lines, placed in
    the editor on their own (starter comments are dropped), must pass **every** checkpoint, so they form a
    complete program. Where a checkpoint is creative, they use Mar'tu's pick. No distractor may also be one of
    the right lines. The §3 "PA" lines list the blocks and their distractors on that basis.

**Lints** (harness work, T6; the gate script already runs c, f and g on the plan):

| Lint | Rule |
|---|---|
| (a) | No OUT-only check on a computed value. The hard-coded literal is a `wrong_answers` entry and must fail. |
| (b) | PAR collision: no fresh argument set gives the same result as a call written in the task. |
| (c) | `starter_level`: a construct's first writing step is S3 or above, and consecutive steps of a strand drop by at most one level. |
| (d) | QC coverage: each claimed skill has an item with an evidence-based wrong answer that fails. |
| (e) | Creative value: no check downstream of a creative prompt compares against a fixed creative value. A wrong answer using another creative value must pass. |
| (f) | Unit 1: ≤ 60 words of Learn text before the first action. |
| (g) | At least one non-dictated checkpoint per lesson, and exactly one SOLO item. |

## 2.13 Teacher page, settings and the run-kit (T7, T8, directive §4.4)

**Classroom page** (server mode; **[OWNER]** does the class use server mode in class?):
1. **Needs you now.** Refreshes about every 30 s. Each row gives the display name, the exercise, a neutral reason
   and the minutes. Reasons:
   - a silent stall of 6 minutes or more ("hasn't run code");
   - the same error 3 times in a row, or 8 or more failed runs on one checkpoint;
   - a reveal used before any run;
   - "too hard" together with red signals;
   - a Readiness "Review first" after two cycles.

   A row clears when the student makes progress.
2. **Ready for more.** A hint-free streak of 5 or more checkpoints, a QC pass, or "too easy" with green signals.
   Each row comes with a suggested Trial or side quest.
3. **Unit grid** (architecture §5.2). "Tested out (provisional)" is shown apart from "Complete".
4. **Campaign readiness.** Rows are the CC skills plus the campaign parts at Band A/B (§5.5). Each row counts
   students at solid / practicing / not yet, marks solo-verified students, and drills down to individuals.
5. **Teacher settings** (persist per classroom):
   - Route M1 or M2;
   - a provisional preset per student;
   - the per-student deferral switch (defers SC items; the dashboard suggests it);
   - pairs;
   - echo, persistence and sandbox on or off;
   - Show-solution timing.

- **Summary schema additions** (`.strict()`, with the privacy test extended): `lastRunAt`, `unchangedSince`,
  `sameErrorStreak`, `skills: {tag: {level, solo}}`, `testedOutProvisional`, and pulse counts. There is still no
  code, no free text, no typed values and no hero names.
- **Static export:** panels 1 and 2 are unavailable, and the page says so.

**Run-kit outline** (`docs/intro-to-python/teacher-guide.md`, one page):
- **The shape of a period:** a 3-minute warm-up ("Mar'tu remembers", projected), self-paced work, then a
  2-minute close (the pulse).
- **Sync points.** The class regroups at each unit's quiz or project day.
  - Early finishers go to the Trials, side quests or the Extra practice pool, **never to helper duty by
    default**. The opt-in apprentice protocol uses "ask, don't tell" prompts.
  - Students who are behind work the critical path, with the teacher's deferral switch.
- **Mar'tu moments** (5 minutes, teacher-led, projected; the MKO is also the teacher), at the cliffs:
  - 6A-01 box versus recipe;
  - 6A-06b be-the-ledger, traced on the board together;
  - 4B-01 boxes in boxes;
  - 6C-01 "the box holds the recipe";
  - 5A-05 the decay reveal, as a class discussion.
- **Structured pairing.** Driver and navigator rotate every exercise, and each lesson has one solo item. After
  Unit 1, review the solo-versus-together evidence and re-pair if a pair isn't producing solo passes.
- **Provisional starting presets:**
  - "Show me more" for G1, G2 and G3, **including B-02 and B-03, whose paper totals are inflated by templates and
    shared hands**;
  - QC1 first for G4.

  These are defaults to confirm in-app, never labels.
- **How to read the dashboard**, and what to do with a "Review first" Readiness result: pair the student in the
  campaign, and pre-teach the flagged skill.
- **Routes M1 and M2**, and when to send the class into Module 1 ("Before the cabin door").
- **Privacy reminders:** the echo switch, no names in content, and the static-export limits.

## 2.14 Legend for section 3

- **Flags:** **CC** core and campaign-critical · **SC** core, syllabus only (deferrable by the teacher's switch)
  · **K** contingent (shown only on a signal) · **pool** Extra practice · **O** optional.
- **Stages:** **P** predict · **R** run · **I** investigate · **M** modify · **Mk** make · **A** assemble (Parsons)
  · **D** debug · **PF** productive-failure hook (≤ 3 min, ungraded, skipped on frustration signals) ·
  **TT** trace table.
- **S-level:** starter level, S4–S0 (§2.12 rule 14).
- **Checkpoints:** **[ND]** non-dictated (goal + names only) · **[D]** dictates the code. "Names:" lists the
  chips.
- **Hooks:**
  - **AW** another-way angles · **TR** static trace table / tracer · **PA** Assemble it (blocks; distractors)
  - **BQ** Lucky's side quest (combining) · **DF** Mar'tu's pick · **PR** pair prompt · **echo** echo spot
  - **WT** "Why does this work?" sidebar · **moment** Mar'tu moment · **camp** campaign mode
  - **twin** the post-reveal or post-Assemble typed twin
- **Hints:** P point → T teach → S show (the bottom-out line). Every hint's example names go in `foreign_names`.
- **WA:** harness `wrong_answers` entries. Each gives the slip, the checkpoint it fails at, and the message
  keyword. The sheet ID goes in `notes` only.
- **intro:** the exact harness tokens the item introduces. "—" means none new.
- **Min:** typical-student minutes. G1 takes about 1.4×; G4 about 0.6–0.8× (§6).

---

# 3. Units

Each exercise entry gives:
- its code, slug and title; intro tokens; PRIMM stages; starter level; CC/SC; skills;
- the Learn text (verbatim drafts in Unit 1, where lint f applies; intent elsewhere);
- the Example, with its `foreign_names`;
- the starter;
- the checkpoints ([ND]/[D], Names to use, check codes and key messages);
- the misconceptions it catches (slip → how the check or explainer catches it);
- the hint-ladder intent (P / T / S);
- the another-way angles;
- the side quest (BQ), the twin, the flags;
- the harness wrong answers (WA).

All checks are behavior-based (§2.5). All messages use invented values (§2.11).

## Unit 1 · Hello World: "Words by the Fire" (`hello-world`, files u01a–u01d)

**Mar'tu's framing.** "Every spell begins as words. Python is fussy about words. More fussy than Lucky is about
glug, yes? Tonight: how to say something, how to keep something in a box, and how to let Python do the sums."

**RPG tie-in.** Mar'tu's chalk wall, the party's stat sheets and the night's supplies become printed lines and
labeled boxes. Mana bars appear here for the first time.

**Learning objectives (syllabus-aligned). Student can…**
1. Use `print()` with text in matching quotes, print lines in order, and print a blank line.
2. Write `#` comments, and use them to switch a line off.
3. Create a variable with `name = value`, naming it **exactly** as asked, quoting text and not numbers, and tell
   `name` apart from `"name"`.
4. Reassign a variable, including `mana = mana - cost`.
5. Use `+ - * /` (and know that `/` gives a decimal).
6. Turn a word problem into labeled variables ("how many?" / "how much is one?") and **let the code combine
   them**.
7. Join text with `+`, converting numbers with `str()`.
8. Repeat a string with `*` to draw a bar, with parentheses for `(max - mana)`.
9. Recognize and fix a missing quote or bracket, unquoted text, a space or wrong case in a name, `def` used for a
   box, and text plus a number.

Optional or pool: triple quotes, `+=` / `-=`, `** % //`, `input()`.

**Campaign links.**
- Obj 1, 3, 9 → `program-movement` and `program-dialogue-options` (`"left"`, `"option 1"`).
- Obj 4, 6 → `hold-the-barrier` (`caster["mana"] = caster["mana"] - spell["mana_cost"]`) and `mana-bars`
  (`caster["max_mana"] - caster["mana"]`).
- Obj 7 → the `mana-bars` return line.
- Obj 8 → `"█" * caster["mana"]`.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | 1-A1 card "How Mar'tu Teaches" | CC | 1 | u01a |
| 2 | 1W "Before the First Spell" (warm-ups) | K ("Show me more") | 4 | u01a |
| 3 | Lesson 1A "Words in Quotes" | CC (1A-06 SC) | 19 | u01a |
| 4 | Lesson 1B "Boxes With Labels" (with 1B-remembers) | CC | 25 | u01b |
| 5 | 1X-AB Extra practice: words and boxes (1A-07, 1B-T) | pool | 6 | u01b |
| 6 | Lesson 1C "Math and Glue" (with 1C-remembers) | CC (1C-09 SC) | 38 | u01c |
| 7 | 1X-C Extra practice: math (1C-05, 1C-T) | pool | 6 | u01c |
| 8 | Quiz 1 "Chalk Quiz" | SC | 8 | u01c |
| 9 | Project 1P1 "The Night Watch Ledger" | SC | 18 | u01c |
| 10 | Project 1P2 "The Ward Sign" | O | 25 | u01d |
| 11 | Article 1-A2 "Clock Math" | O | 12 | u01d |
| 12 | Article 1-A3 "Asking the Traveler: `input()`" | O | 15 | u01d |
| 13 | Quick Check 1 (forms A, B) | O (test-out) | 10–12 | u01d |
| 14 | Cheatsheet 1 | ref | — | u01d |

### 1-A1 "How Mar'tu Teaches" [card, CC, 1 min] (`article`, no exercises)

A ≤ 60-word card with three pictures: the Run button pointing to the console; the Help control under a
checkpoint; the ✓ ● ○ checkpoint list. Draft text (49 words):

> "Write a line. Press Run. Python answers below. **Pressing Run on unfinished code is allowed and costs nothing.
> A message from Python is information, not a mark.** Stuck? Press Help. **You can always ask for a starting line
> or more structure.** Nothing here is timed. Your hints are private."

Every other feature is introduced by just-in-time coach marks (§2.2). The card ends with two buttons: [Start 1A]
and [Take Quick Check 1].

### Lesson 1W "Before the First Spell" [K: on under "Show me more", 2 × 2 min] (u01a)

- **1W-02 `what-an-error-looks-like` · What an error looks like** · intro `call:print` `const:str` (full path) · D
  · S4 · K
  - Starter: `print("Shield up.)`.
  - Learn: "Run it. Python's message is not a mark against you. It says what Python could not read."
  - CP1 [D]: "Add the missing `"` and run again." Check: `"Shield up." in _lines()`.
  - Teaches the **explainer footer**: "Read the last line first. Then look at the line it names."
  - Hints: P "Look at the end of the words." T "Quotes come in pairs." S `print("Shield up.")`.
  - AW: picture (a fizzle panel with arrows to the last line and the line number) · shorter.
  - WA: unchanged starter → crash, "unterminated".
- **1W-04 `keyboard-symbols` · Where the symbols live** · intro — · M · S2 · K
  - Learn: a keyboard picture. "`-`, `_` and `=` sit side by side. They mean different things. `-` subtracts,
    `_` joins words in a name, `=` puts a value in a box." (G1 R30)
  - Starter: `# Print a line that has _ and - and = and # in it.`
  - CP1 [ND]: "Print a line that has `_`, `-` and `=` in it." Check: one printed line contains all three.
  - Hints: P "Put the symbols inside quotes." T `print("( )")` shows `( )`. S `print("( ) # _ - =")`.
  - AW: picture (the keyboard with the three keys circled) · step-by-step (where Shift is).
  - WA: `print(_ - =)` → crash.

### Lesson 1A "Words in Quotes" [CC, 19 min] (u01a)

No warm-up (first lesson). The preset question already happened on the course map.

- **1A-01 `press-run` · Press Run** · intro `call:print` `const:str` · P→R · S4 · *starter passes* · CC ·
  `print-text`
  - Learn (22 w): "Python reads your instructions and does them. `print` shows words on the screen. Guess what
    the console will show, then press Run."
  - Starter: `print("Hi. It is me, Mar'tu.")`
  - Predict: the words / the words with quotes / an error.
  - CP1 [D] "Press Run." Check: `"Hi. It is me, Mar'tu." in _lines()`.
  - Hints: P "Run is the button above the editor." T "Run sends your lines to Python. What `print` holds appears
    below." S "Press Run."
  - AW: in Tor ("`print` is my chalk. What is inside the quotes goes on the wall.") · picture (editor → arrow →
    console) · shorter.
  - WA: empty editor → CP1, "Run".
- **1A-02 `your-own-words` · Your own words** · intro — · M · S4 · CC · `print-text`, `quote-text` · **echo**
  - Learn (19 w): "The words inside the quotes are yours. Python shows them exactly. Change them to something
    Oogrish might say."
  - Example: `print("Shield up.")` → `Shield up.` (foreign: none)
  - Starter: `print("Write Oogrish's words here")`
  - CP1 [ND] "Change the words to a line Oogrish might say to calm the party." Checks:
    - TEXT: one printed line that is not the placeholder.
    - C3: if it equals the Example's line, the message is "That's the example's line. Want Mar'tu's pick?
      [Use it]", and the pick counts as the student's own.
  - Echo: Mar'tu repeats the line deadpan ("*<line>.* Hm. He would say that.") through the filter (§2.11).
  - Hints: P "Change only the words between the quotes." T `print("Fine.")` shows `Fine.` S
    `print("Steady, now. We go together.")`.
  - AW: in Tor · picture · shorter.
  - DF: "Steady, now."
  - BQ (Lucky, combining print + order): "Print Lucky's reply on the next line, so the two read like a
    conversation."
  - Twin: a line Gearshift might say.
  - WA: the placeholder unchanged → CP1, "Change"; the Example's line → CP1, "example".
- **1A-03 `close-the-quote` · Quotes and brackets come in pairs** · intro — · D→I · S4 · CC · `quote-text`
  - Learn (27 w): "Quotes come in pairs: one before the words, one after. Brackets come in pairs too. This line
    is missing one. Run it, read the message, then mend it."
  - Starter: line 1 `print("It is not a compass)` and line 2 `print("Shield up."`. Mending line 1 shows the
    "One fixed. Python found the next one:" prefix on line 2's `'(' was never closed`.
  - CP1 [D] "Mend line 1 so it runs." Check: a line equal to `It is not a compass` (a final period is optional).
  - CP2 [ND] "Line 2 is missing something too. Mend it." Check: `"Shield up." in _lines()`.
  - Explainer rows proven: unterminated; mixed quotes; two apostrophes; `'(' was never closed` (§2.6).
  - Hints: P "Count the quote marks on line 1, then the brackets on line 2." T "Every opening mark needs a
    closing mark: `print("Hi")` has two quotes and two brackets." S line 1 `print("It is not a compass")`; line 2
    `print("Shield up.")`.
  - AW: picture (bookends) · everyday (shoes come in pairs) · step-by-step ("Python reads from the first quote
    and looks for the next one. It never comes.") · shorter.
  - BQ (combining quotes + apostrophes): "Print `Barrier's holding.` exactly. Why does the `'` inside the `"`
    quotes not break anything?"
  - WA: `print("It is not a compass')` → crash, "unterminated"; `print(''Shield up'')` → crash, "comma";
    `print("Shield up."` left → crash, "never closed".
- **1A-04 `words-need-quotes` · Words need quotes** · intro — · D→I · S4 · CC · `quote-text`
  - Learn (22 w): "Words you want to show need quotes. Without quotes, Python thinks you mean the name of something
    saved earlier, and it finds nothing."
  - Starter: line 1 `print(Fireball)`, line 2 `print(Get inside)`.
  - CP1 [D] "Make line 1 show the word Fireball." Check: `"Fireball" in _lines()`. Explainer rule 9, 1A
    wording, with no "box".
  - Investigate (one click): "Why does Python say *not defined*?" (It looked for a saved name / It can't spell /
    The word is too long.)
  - CP2 [ND] "Line 2 has two words without quotes. Mend it." Check: `"Get inside" in _lines()`. The C13 message
    fires ("These look like words; put them all inside one pair of quotes…").
  - Single quotes pass (not a wrong answer).
  - Hints: P "Which words do you want to see on the screen?" T "Words you want to show need quotes. Without
    quotes, Python looks for something saved earlier with that name." (G1 R23 wording. The quotes sentence itself
    starts in 1B-01, once "box" exists, and is word for word from then on.) S `print("Fireball")`.
  - AW: step-by-step (what Python tries first) · everyday ("Say Lucky" versus "say 'Lucky'") · contrast gallery
    (`print(Fireball)` / `print("Fireball")`) · shorter.
  - WT: "Names versus words".
  - BQ (combining multi-word + apostrophe): "Announce Lucky's spell exactly: `Lucky's Fire Ball!`"
  - WA: `print(Fire ball)` → crash, "comma"; `print(Fireball")` → crash, "unterminated".
- **1A-05 `top-to-bottom` · Top to bottom** · intro — · P→R→M · S4 · CC · `print-text`
  - Learn (18 w): "Python runs your lines from top to bottom, one at a time. An empty `print()` shows a blank
    line."
  - Starter: `print("Get inside, yes?")`, `print("Mar'tu checks the clock.")`, `print("The hand is near the arc.")`.
  - Predict: the order of the three lines.
  - CP1 [D] "Move the line `Get inside, yes?` so it prints last." Check: its index in `_lines()` is last.
  - CP2 [D] "Add `print()` just before it, for a blank line." Check: the raw stdout has a blank line right before
    the warning.
  - Hints: P "Which line runs first?" T "Line 1 runs, then line 2, then line 3." S the three lines with
    `print()` before the last.
  - AW: picture (a ladder read top to bottom) · step-by-step (static step table: line → what appears) · shorter.
  - TR: static step table.
  - PR: "Seat A predicts the order, Seat B runs."
  - BQ (combining order + blank lines): "Add Lucky's reply after the warning, with a blank line between."
  - WA: the warning still first → CP1; no blank line → CP2.
- **1A-06 `notes-for-humans` · Notes for humans** · intro — (comments have no token) · I→M · S4 · SC
  - Learn (25 w): "A line that starts with `#` is a note for humans. Python skips it. Put `#` in front of a line
    to switch it off."
  - Starter: three prints, one of them `print("I am keeping the glug.")`.
  - CP1 [D] "Put `#` in front of the line Lucky shouldn't say out loud." Checks: the line is not printed, and
    `'keeping the glug' in _source` ("Keep the line; switch it off with `#`").
  - CP2 [ND] "Add a note of your own above the code." Check: the source has a `#` line the starter didn't.
  - Hints: P "Which line would Lucky regret?" T "`# print("Hi")` is skipped." S `# print("I am keeping the glug.")`.
  - AW: everyday (stage directions in a play script) · picture (a sticky note on the code) · from the campaign
    ("`# Replace pass with…` is a note for you") · shorter.
  - BQ (combining comments + order): "Above each line, write a note that says which hero speaks it."
  - WA: deleting the line → CP1, "switch it off".
- **1A-08 `broken-spell-1A` · Broken spell: three slips** · intro — · D · CC · `quote-text`, `read-traceback`
  - Learn (14 w): "Three lines. Three small slips. Run, read the message, mend one line, run again."
  - Starter: `Print("Barrier's holding.")`, `print("Shield up.)`, `print(Steady)`.
  - CP1–CP3 [D], one per line, each with its own green tick. Rows that fire: rule 6 for the builtin ("Python's
    commands are lower case: `print`"), unterminated, rule 9.
  - Hints per CP: P names the line. T the row's idea. S the mended line.
  - AW: step-by-step (the two-step "read the last line first" footer) · shorter.
  - Bomb Shell's pass line: "Works."
  - WA: `print(steady)` → CP3; `print("Steady)` → crash.
- **1A-S `solo-1A` · Show Mar'tu** · SOLO, one bug · S4 · CC
  - Learn (10 w): "One line, one slip. This one is yours alone."
  - Starter by seat: A `print("The lantern is lit.)`; B `print(The lantern is lit)`; solo → A.
  - CP1 [ND] "Mend the line so it shows `The lantern is lit.`"
  - Hints: two (schema). Using one records the pass "with structure".
  - Pass line: "You did that alone. I saw."

### Lesson 1B "Boxes With Labels" [CC, 25 min] (u01b)

*Mar'tu remembers… (`1b-remembers`)*
1. "Which line shows the word glug: `print(glug)` or `print("glug")`?" (1A)
2. "What does Python do with a line that starts with `#`?" (1A)

- **1B-01 `label-a-box` · A box with a label** · intro `node:Assign` · P→R→I→M · S4 · CC · `make-variable`
  - Learn (31 w): "A box (variable) has a label and something inside. `companion = "Gearshift"` makes a box
    labeled `companion` and puts the text inside. Read `=` as gets: companion gets Gearshift." The labeled-box
    picture is shown by default.
  - Starter (the code to study): `companion = "Gearshift"`, `print(companion)`, `print("companion")`.
  - Predict both lines.
  - Investigate:
    - (1) one click: which line has quotes, and what did each print?
    - (2) G3 R2: "Delete `companion = ` from line 1, leaving `"Gearshift"`. Run. What happened?" Explainer rule 4
      fires, with the static "made, not kept" picture.
  - CP1 [D] "Put `companion = ` back, and change the value to another hero." Checks: TEXT; and
    `companion != "Gearshift"`, which on failure offers Mar'tu's pick inline (C3).
  - Hints: P "The label is left of `=`." T "Read it as: companion gets Gearshift." S `companion = "Bomb Shell"`.
  - AW: picture (labeled box) · everyday (phone contacts: tap the name, the phone uses what's saved) · in Tor ("a
    jar on my shelf with a chalk label") · contrast gallery · sentence frame `____ = ____`.
  - TR: static step table.
  - BQ (combining box + order): "On a later line, give `companion` a new hero. Print it before and after the
    change."
  - Twin: `rival = "<any>"`, then print it.
  - WA: value left as `"Gearshift"` → CP1, "example"; the bare `"Gearshift"` left → crash (NameError, rule 4).
- **1B-02 `name-and-value` · Name AND value** · intro — · M · S3 · CC · `make-variable`, `exact-names`,
  `quote-text` · **echo**
  - Learn (24 w): "To make a box, write the name, then `=`, then the value. The name has no quotes. The value is
    your hero, in quotes."
  - Example: `companion = "Gearshift"` / `print(companion)` → `Gearshift`. foreign: `companion`, `player_name`,
    `hero`.
  - Starter (its own; no carry-over): `# Your box goes here:` / (blank line) / `# Print it here:`
  - CP1 [ND] "Make a box named `character` that holds your hero's name, in quotes." Names: `character`. Checks:
    - NAME (near: `companion`, `Character`, `charcter`, `player_name`);
    - TEXT;
    - BARE ("Line 1 is a value with no box, so Python made it and forgot it. Put `character = ` in front of it.").
  - CP2 [D] "Print `character`, with no quotes around the name." Checks: the AST `print` argument is
    `Name('character')`; the output equals its value. Message for `print("character")`: "That prints the word
    *character*. Take the quotes off so Python opens the box."
  - Catches (each maps to a check or an explainer row):

    | Slip (evidence) | Caught by |
    |---|---|
    | a lone `"Zelda"` then `print("Zelda")` (B-02, B-03, A-04) | BARE |
    | a lone `"Zelda"` then `print(character)` | explainer rule 4 |
    | `def ("character")` (A-02) | DEF row |
    | `character - "Zelda"` (A-04) | rule 8 |
    | `player_name = "Zelda"` (A-05–A-08) | NAME/LEFT |
    | `character = Kratos` (A-08 shape) | rule 9 |
    | `character = Captain Glug` (G2 R2) | the multi-word row |
    | `print("character")` | CP2 message |
  - Hints:
    - CP1: P "Find the word `character` in step 1. That is the box's label." T "A box is `name = value`, like
      `companion = "Gearshift"`." S `character = "Zelda"` (then use your own hero).
    - CP2: P "Look at the Example's second line." T the quotes sentence. S `print(character)`.
  - AW: picture (default open) · everyday (contacts) · sentence frame ("name, no quotes, gets value") · contrast
    gallery "Not this" (`def ("character")`, `"character" = "Zelda"`, `character - "Zelda"`, a lone `"Zelda"`) ·
    shorter.
  - PA: blocks `character = "Zelda"` / `print(character)`. Distractors (≤ 3): a lone `"Zelda"`,
    `character - "Zelda"`, `print("character")`.
  - DF: "a very tired adventurer".
  - Echo: "*<value>.* Hm. Welcome to the cabin."
  - PR: Seat A writes line 1, Seat B line 2, then swap.
  - BQ (combining boxes + comments): "Make `weapon` too, and write a `#` note above each box saying what it holds."
  - Twin: `familiar = "<any>"`, then print it.
  - WA: each row of the table above (lone value → CP1 "no box"; `player_name` → CP1 "character"; dash → crash
    "not defined"; `print("character")` → CP2 "word").
- **1B-03 `numbers-stand-alone` · Numbers stand alone** · intro `const:int` · P→I→M · S3 · CC ·
  `numbers-vs-text`, `make-variable`
  - Learn (25 w): "Numbers stand alone, with no quotes. `"3"` is text that looks like a number. `3` is a number
    Python can do math with."
  - Example: `max_mana = 26` / `print(max_mana)` / `print("max_mana")` → `26` / `max_mana`. foreign: `max_mana`.
  - Predict both lines.
  - Starter: `# Lucky's armor bonus (a number):` / `# Any weapon name (text):`
  - CP1 [ND] "Make `armor_bonus` holding Lucky's armor bonus, 3, as a number." Checks: NUM, NAME, BARE.
  - CP2 [ND] "Make `weapon` holding any weapon name, as text." Checks: TEXT, NAME.
  - Hints: P "Does a number need quotes?" T "`dice = 2` is a number box. `dice = "2"` is text." S
    `armor_bonus = 3`.
  - AW: picture (number box versus text box) · everyday (a price tag reading "3" versus three coins) ·
    step-by-step ("Python sees `3` and makes a number; it sees `"3"` and makes text") · shorter.
  - WT: "Why `"3"` isn't 3".
  - BQ (combining number box + reassign + order): "Gearshift polishes Lucky's armor. On a new line make
    `armor_bonus` hold 4, and print it before and after."
  - Twin: `dice_count = 2`.
  - WA: `armor_bonus = "3"` → CP1, "quotes"; a lone `3` → CP1, "no box".
- **1B-04 `exact-names` · Exact names** · intro — · D · S4 · CC · `exact-names`
  - Learn (30 w): "Python matches names letter for letter. `Max_Mana` and `max_mana` are two different names. A
    name cannot have a space in it; use `_` instead." Plus one line: "In the campaign, the game looks for
    `move_left` exactly. It can't find `Move_left`."
  - Starter: `Max_Mana = 18`, `print(max_mana)`, `magical affinity = 9`, `print(magical_affinity)`.
    Python reports line 3's SyntaxError first (the space-in-name row); then line 2's NameError, where rule 5
    fires ("two names almost match").
  - CP1 [D] "Line 3: a name can't have a space. Make it `magical_affinity`." Check: `magical_affinity == 9`.
  - CP2 [ND] "Make line 2 print 18, using the name the task gives: `max_mana`." Checks: `max_mana == 18`;
    NAME if `print(Max_Mana)` was used instead ("The task's name is `max_mana`; rename the box on line 1.").
  - Catches: A-06 space in a name; A-08 `heath`; A-05 `Powrup`; B-01 `power_UP`; B-02/B-03 `Pizza`/`pizzas`.
  - Hints: P "Compare the names on lines 1 and 2, letter by letter." T "A name is like a password: every letter
    and capital counts." S `max_mana = 18`.
  - AW: step-by-step (a key in a lock) · picture (letter-diff) · everyday (a password) · from the campaign
    (`move_left`).
  - BQ (combining names + numbers): "Gearshift's sheet says `MAX MANA: 20`. Make a box for it with a name Python
    accepts, and print it."
  - Twin: `Armor_Bonus` versus `armor_bonus`.
  - WA: `print(Max_Mana)` → CP2, "max_mana"; `magicalaffinity = 9` → CP1, "magical_affinity".
- **1B-05 `change-the-box` · A box can change** · intro — · P→R→I→M · S4 · CC · `reassign`
  - Learn (18 w): "A box holds one value at a time. Put a new value in, and the old one is gone."
  - Starter: `mana = 26`, `mana = 21`, `print(mana)`.
  - Predict: 26 / 21 / both. A wrong predict opens the static step table (G2 R16).
  - CP1 [D] "Add a line that puts 14 in `mana`, above the `print`." Checks: `mana == 14`; `'14' in _lines()`;
    `'26' not in _lines()`.
  - Catches: "both values stay"; "print shows everything computed earlier" (A-03, A-04).
  - Hints: P "Which value is in the box when `print` runs?" T the step table. S `mana = 14` above the `print`.
  - AW: picture (the old value crossed out) · everyday (a whiteboard: write, wipe, write) · step-by-step (table)
    · shorter.
  - TR: static step table, open by default.
  - BQ (combining reassign + order): "Lucky's glug goes 5 → 3 → 1. Print `glug_sips` after each change."
  - WA: the new line placed below the `print` → CP1, "14".
- **1B-06 `broken-spell-1B` · Broken spell** · intro — · D · CC · `make-variable`, `read-traceback`
  - Learn (13 w): "Four lines, four slips you have seen before. Mend them one at a time."
  - Starter: `"weapon" = "Telegun"` / `def companion = "Gearshift"` / `"Lucky"` / `glug_sips - 3` /
    `print(hero)` / `print(weapon)`. Rows in order: quoted-name, DEF (G1 R15), then at runtime rule 8 (dash), then
    rule 4 (`hero` required, with the bare `"Lucky"` on line 3).
  - CP1 [D] line 1 `weapon = "Telegun"`. CP2 [D] line 2 `companion = "Gearshift"`. CP3 [ND] "Line 3 should make a
    box named `hero`." CP4 [D] line 4 `glug_sips = 3`.
  - Hints: P names the line. T the row's idea. S the line.
  - AW: step-by-step (the read-the-error footer) · shorter.
  - BQ (combining): "Write one line that would get the 'a name can't have a space' message, then mend it."
  - WA: line 3 written as a bare `Lucky` → crash, rule 7 (proves rule 7); `def companion() = "Gearshift"` → crash.
- **1B-S `solo-1B` · Show Mar'tu** · SOLO make-twin · S2 · CC
  - Learn (14 w): "Make one box of your own and show what is inside. Nobody helps on this one."
  - Starter by seat: A `# 1. Make a box named familiar that holds any creature, in quotes.` / `# 2. Print
    familiar.` B uses `lantern_name`. Solo → A.
  - CP1 [ND], CP2 [ND]. Checks: NAME, TEXT, BARE, AST `print(Name)`.
  - Pass line: "You did that alone. I saw."

### Extra practice 1X-AB "Words and boxes" [pool] (u01b)
- **1A-07 `many-lines-at-once`** (kept id) · intro `const:multiline_str` · P→R→M
  - Example: a two-line `"""` note about the glug canteen.
  - Task: print a 3-line chalk note with one `print("""…""")`.
  - CP1: at least 3 lines from a single `print` call (`_count('call:print') == 1`).
  - BQ: a tiny box drawn with `|` and `-`. It is the prerequisite card for 1P2.
- **1B-T `name-and-value-again`** · twin for deferral time
  - Task: make `satchel` (text) and `coins` (a number), then print both.
  - CP1 [ND] the boxes. CP2 [D] the prints. Checks: NAME, TEXT, NUM, BARE.

### Lesson 1C "Math and Glue" [CC, 38 min] (u01c)

*Mar'tu remembers… (`1c-remembers`)*
1. "Which line makes a box: `"hero" = "Lucky"` or `hero = "Lucky"`?" (1B)
2. "Mend: `print("Shield up.)`" (1A)

- **1C-01 `chalk-math` · Mar'tu's chalk math** · intro `op:Add` `op:Sub` `op:Mult` `op:Div` · P→R→I→M · S4 · CC ·
  `combine-values`
  - Learn (13 w): "Python does math with `+`, `-`, `*` and `/`. Guess each answer, then run."
  - Predict: `46 + 44`, `48 - 37`, `9 * 2`, `48 / 2`. Investigate (one click): why is it `24.0`?
  - Starter: `first_gap = 48` / `last_gap = 37` / `# Replace 0 with how much the gap shrank, using the two boxes.`
    / `print(0)`
  - CP1 [D] "Replace 0 so it prints the shrink, using `first_gap` and `last_gap`." Checks: `'11' in _lines()`,
    plus CMB (rerun `last_gap = 41` → 7) with the rerun table.
  - **Try other numbers** is introduced here: its coach mark appears on the first CMB failure.
  - Catches: typing 11 (everyone's 68) → CMB; `print(48 - 37)` → CMB.
  - Hints: P "Which two boxes hold the gaps?" T "Python can subtract boxes: `a - b`." S
    `print(first_gap - last_gap)`.
  - AW: in Tor (the chalk wall) · picture (two jars and a minus sign) · everyday (a calculator that remembers) ·
    shorter.
  - Gearshift's pass line: "Math checks out."
  - BQ (combining parentheses + division): "Print the average of the first and last gap."
  - WA: `print(11)` → CP1, "41"; `print(48 - 37)` → CP1, "41".
- **1C-02 `what-each-number-means` · What does each number mean?** · intro — · I→M · S4 · CC · `combine-values`
  - Learn (27 w): "Before any math, ask two questions about each number: how many? how much is one? Put each
    number in the box that means that."
  - Story (task text): "Mar'tu needs 3 lanterns that cost 4 coins each. Rope costs 2 coins a coil, and Mar'tu
    needs 5 coils." The **second** problem gives the price first (C9).
  - Starter: `lantern_count = 0  # how many?` / `lantern_price = 0  # how much is one?` / `rope_count = 0  # how
    many?` / `rope_price = 0  # how much is one?` (the boxes are count-first).
  - CP1 [D] "Fill in the two lantern boxes from the story." Checks: values 3 and 4. SWAP: "You swapped them: 3 is
    how many lanterns, 4 is the price of one." Wild count: "Lucky would like 1000 lanterns. The story says 3. Use
    the story's numbers here. You get your 1000 next." LINE-TOTAL: "12 is already the cost of all 3 lanterns. This
    box wants the price of one."
  - CP2 [ND] "Fill in the two rope boxes. This story gives the price first." Checks: 5 and 2, with SWAP and the
    wild-count message.
  - Hints: P "Ask each number: how many? or how much is one?" T "In '2 maps at 6 coins', 2 is how many and 6 is
    the price of one. **A 0 in the starter is a placeholder: replace it.**" (G3) S `rope_count = 5` /
    `rope_price = 2`.
  - AW: in Tor ("How many jars? How much for one jar?") · picture (a price tag versus tally marks) · everyday (a
    shopping list) · step-by-step (underline each number, ask the question).
  - BQ (combining comments + modeling): "Write your own small shopping story in a `#` note, then fill boxes for it."
  - WA: lanterns (4, 3) → CP1, "swapped"; rope in reading order (2, 5) → CP2, "swapped"; `rope_count = 1000` →
    CP2, "story"; `lantern_price = 12` → CP1, "all 3".
- **1C-03 `let-the-code-combine` · Let the code combine it** · intro — · M→Mk · S4 · CC · `combine-values`
  - Learn (25 w): "Do not work the total out yourself. Let Python combine the boxes. Then the total stays right
    when a number changes."
  - Example: "Oogrish buys 2 maps at 6 coins." `map_count = 2` / `map_price = 6` /
    `map_cost = map_count * map_price` / `print(map_cost)` → `12`. foreign: `map_count`, `map_price`, `map_cost`.
  - Starter: the four filled boxes (3, 4, 5, 2), then `lantern_cost = 0`, `rope_cost = 0`, `total_cost = 0`,
    `print(total_cost)`.
  - CP1 [D] "Replace the 0 in `lantern_cost` so Python multiplies the lantern boxes." Check: CMB
    (`lantern_count = 7` → 28).
  - CP2 [ND] "Do the same for `rope_cost`." Check: CMB.
  - CP3 [ND] "Make `total_cost` the sum of the two costs." Checks: `total_cost == 22`; CMB (`lantern_count = 7` →
    38) with the rerun table; NEWBOX.
  - **Investigate (everyone, using Try other numbers):** "Set `rope_count = 1000`. Run. Watch `total_cost`
    follow." It shows 2012. This is G1's 1000-ropes joke turned into the lesson.
  - Catches:

    | Slip | Caught by |
    |---|---|
    | `total_cost = 22` (everyone's 68) | CMB with the table |
    | `total_cost = 12 + 10` | CMB |
    | `lantern_cost = lantern_count * 4` | CMB (rerun with a new price) |
    | `my_total = lantern_cost + rope_cost` | NEWBOX |
    | `total_cost = 3L + 5R` (A-02 `5P`) | the decimal-literal row |
    | `total_cost = lantern_count + rope_count` → 8 | "You added how many, not costs." |
  - Hints (CP3): P "Look at `total_cost = 0`. Which two costs make the total?" T "Python can add boxes. If `a = 2`
    and `b = 5`, then `c = a + b` puts 7 in `c`, and it stays right when `a` changes." S
    `total_cost = lantern_cost + rope_cost`.
  - AW: everyday (an online cart: change the quantity and the total follows) · "show your working" (G2 R12) ·
    picture (arrows from boxes into the total) · from the campaign (`caster["max_mana"] - caster["mana"]`) ·
    shorter.
  - PA: three blocks. Distractors: `total_cost = 22`, `lantern_cost = 12`,
    `total_cost = lantern_count + rope_count`.
  - PR: "Seat B explains why typing 22 is a trap."
  - BQ (combining subtraction + combined values): "Mar'tu has 30 coins. Print how many are left after shopping."
  - Twin (price-first, C9): "Candles cost 1 coin each and Mar'tu needs 3; maps cost 6 and he needs 2. Make
    `candle_cost`, `map_cost` and `supply_total`."
  - WA: `total_cost = 22` → CP3, "38"; `total_cost = 12 + 10` → CP3, "38"; `my_total = lantern_cost + rope_cost` →
    CP3, "still holds 0"; `3L + 5R` → crash, "decimal".
- **1C-04 `spend-mana` · Spend some mana** · intro — · P→R→M · S4 · CC · `reassign`
  - Learn (25 w): "`mana = mana - spell_cost` means: take what is in `mana` now, subtract the cost, and put the
    answer back in `mana`."
  - Starter: `mana = 26` / `spell_cost = 3` / `mana = mana - spell_cost` (twice) / `print(mana)`.
  - Predict: `mana` after two casts (20). A wrong predict opens the step table.
  - CP1 [D] "Make it three casts." Checks: `mana == 17`; CMB (`spell_cost = 5` → 11).
  - Catches: tracing by adding the constants (A-03/A-04); `mana = 17` typed → CMB; `mana - spell_cost` with no
    assignment → "`mana` didn't change: put the answer back with `mana = …`".
  - Hints: P "Which line spends mana?" T "Right side first, using what's in the box *now*." S a third copy of the
    line.
  - AW: picture (coins out of a jar, subtract, put back) · step-by-step (static table) · read aloud ("mana gets
    mana minus spell cost") · from the campaign (`caster["mana"] = caster["mana"] - spell["mana_cost"]`).
  - TR: static step table, open by default.
  - BQ (combining + and −): "Lucky drinks glug: +2 mana after the casts. Print the mana."
  - WA: `mana = 17` → CP1, "5"; `mana - spell_cost` → CP1, "didn't change".
- **1C-06 `glue-words` · Glue words together** · intro `call:str` · P→R→I→M · S3 · CC · `concat-str`
  - Learn (21 w): "`+` glues text to text. A number must become text first: `str(26)` gives `"26"`. Spaces are
    text too."
  - Investigate: `"Mana: " + 26` (TypeError, explainer) · `"Lucky" + "is"` (missing space).
  - Starter: `name = "Lucky"` / `mana = 26` / `# Print: Lucky has 26 mana.  Build it from the boxes.`
  - CP1 [ND] "Print `Lucky has 26 mana.`, built from `name` and `mana`." Checks: OUT diff; CMB (`name =
    "Tester"`, `mana = 4` → `Tester has 4 mana.`).
  - Catches: the whole line typed → CMB; `"mana"` in quotes → OUT diff shows the word; missing spaces → OUT diff
    (`Lucky has26 mana.`); `+ mana` without `str` → TypeError row.
  - Hints: P "Which parts come from boxes, and which are fixed words?" T "`"Hi " + name` glues two texts.
    `str(26)` makes 26 into text." S `print(name + " has " + str(mana) + " mana.")`.
  - AW: picture (beads on a string; numbers need `str()` to become beads) · everyday (gluing labels) ·
    step-by-step (build piece by piece) · from the campaign (the mana-bar return line).
  - BQ (combining concat + a second box): "Make it `Lucky has 26 of 26 mana.` with a `max_mana` box."
  - WA: the typed line → CP1, "Tester"; `name + " has " + mana` → crash, "concatenate".
- **1C-07 `status-line` · A status line** · intro — · Mk · S3 (left sides) · CC · `combine-values`,
  `concat-str`, `reassign`
  - Learn (14 w): "Build Oogrish's status line from boxes. Max mana is twice the magical affinity."
  - Starter: `hero_name = "Oogrish"` / `magical_affinity = 9` / `max_mana = 0  # twice the affinity` /
    `mana = 0  # starts full` / `# Print: Oogrish: 18/18 mana`
  - CP1 [ND] "Make `max_mana` twice the magical affinity." Check: CMB (affinity 13 → 26).
  - CP2 [D] "Make `mana` start full: `mana = max_mana`." Check: CMB.
  - CP3 [ND] "Print the status line for your hero: `<name>: <mana>/<max_mana> mana`." Checks: OUT diff against
    the student's **own** `hero_name`; CMB (`hero_name = "Tester"`, affinity 13 → `Tester: 26/26 mana`). Lint (e):
    any hero passes.
  - Under "Show me more", More structure gives `print(hero_name + ": " + ___ + "/" + ___ + " mana")` (G1 R13).
  - Hints: P "Which boxes go between the fixed words?" T the bead picture for this line. S the full `print`.
  - AW: step-by-step · picture (a status bar) · in Tor (Mar'tu's ledger line) · shorter.
  - DF: Oogrish.
  - BQ (combining status + reassign): "Do Lucky's line too (affinity 13), then spend 3 mana and print it again."
  - WA: `max_mana = 18` → CP1, "13"; the status line typed → CP3, "Tester"; `+ mana +` → crash.
- **1C-08 `repeat-a-mark` · Repeat a mark** · intro — (`op:Mult` on text; skill gate `pattern:StrRepeat`) ·
  P→R→I→M→Mk · S4 · CC · `repeat-string`
  - Learn (27 w): "`*` also stamps text: `"█" * 3` stamps three blocks. A mana bar is full blocks for the mana you
    have, then light blocks for the mana used." Plus the glue-versus-stamp sentence: "`+` glues two texts. `*`
    stamps one text a number of times."
  - Predict: `print("█" * 3)` → `███` / `█3` / an error. Investigate: `"█" * 0` and `"█" * 1`.
  - Starter (blocks pre-typed, G1 R8): `full = "█"` / `empty = "░"` / `mana = 3` / `max_mana = 5` /
    `bar = full * 0 + empty * 0` / `print("[" + bar + "]")`
  - CP1 [D] "Replace the first 0 with `mana`." Check: CMB (mana 0, 3, 5 → the full part follows).
  - CP2 [D] "Replace the second 0 with the mana used: `(max_mana - mana)`, in parentheses." Check: CMB (mana 0 →
    `[░░░░░]`, 3 → `[███░░]`, 5 → `[█████]`).
  - CP3 [ND] "Change the boxes to show Gearshift's full bar, 20 of 20." Check: `bar == full * 20`.
  - Point-at-it (G2 R9): "Which part of your line is the mana *used*?"
  - Catches: `empty * max_mana - mana` → the precedence TypeError row; `empty * 2` → CMB; `"█" + 3` → TypeError.
  - Hints (CP2): P "How many light blocks are there when mana is 3 of 5?" T "Python does `*` before `-`, so wrap
    the subtraction: `(a - b)`." S `bar = full * mana + empty * (max_mana - mana)`.
  - AW: everyday (a stamp) · picture (a fuel gauge) · step-by-step (what Python does first) · from the campaign
    (`get_mana_bar`) · shorter.
  - WT: "Why parentheses?"
  - PA: blocks, with the distractor `bar = full * mana + empty * max_mana - mana`.
  - BQ (combining bar + concat):
    - Default: "Add ` 3/5` after the bar with `str()`."
    - If the student has read 1-A2: "Make the bar always 10 blocks wide, whatever the max" (`//`).
  - Twin: a glug bar with `▓`.
  - WA: no parentheses → crash, "operand"; `empty * 2` → CP2, "mana".
- **1C-09 `broken-spell-1C` · Broken spell** · intro — · D · SC
  - Learn (18 w): "Four bugs. One of them prints the right thing and is still wrong. Mar'tu's checks try other
    numbers."
  - Bugs, one checkpoint each:
    - `print("Mana: " + mana)` (TypeError);
    - `rope_cost = 10` typed by hand (the output is right, but CMB fails: the payoff of Try other numbers);
    - `rope_count = 2` / `rope_price = 5` swapped against the story comment (the same product, so SWAP catches
      it: right answer, wrong meaning);
    - a bar with no parentheses.
  - Hints per CP.
  - BQ (combining): "Print `Total: 22 coins`, built from the boxes."
  - WA: each bug left alone fails its own CP.
- **1C-S `solo-1C` · Show Mar'tu** · SOLO make-twin · S3 · CC
  - Learn (10 w): "A short problem, just for you. Let the code combine it."
  - By seat: A "Mar'tu needs 4 candles that cost 2 coins each" (`candle_count`, `candle_price`, `candle_cost`);
    B "Arrows cost 3 coins each, and Lucky wants 6" (price-first; `arrow_count`, `arrow_price`, `arrow_cost`).
    Left sides are given.
  - CP1 [ND] the boxes (SWAP). CP2 [ND] the cost built from the boxes (CMB).

### Extra practice 1X-C "Math" [pool] (u01c)
- **1C-05 `the-short-way`** (kept id) · intro `node:AugAssign` · P→M
  - Predict `hours_waited += 6` and `mana -= 3`, then rewrite two long reassignments.
  - CP1: the values are right. CP2: `_uses('node:AugAssign')`.
  - Every later check accepts both forms. No core code shows `+=`.
- **1C-T `combine-again`** · twin (price-first)
  - "Maps cost 6 coins each and Oogrish wants 2; oil costs 3 a flask and he needs 4. Make `supply_total`."
  - Checks: CMB and SWAP.

### Quiz 1 "Chalk Quiz" [SC, 8 questions] (u01c)

Types: 3 mc · 3 predict · 1 fill · 1 bug. Review order: right answers first (G1 R26).
1. **mc.** "Which line makes a box named `hero` that holds the text Lucky?" Choices: `def ("hero")` /
   `"hero" = "Lucky"` / `hero = "Lucky"` / `hero - "Lucky"`. **Answer:** the 3rd. `why_wrong`: `def` makes a
   recipe, not a box; a box's name never goes in quotes; `-` subtracts, so use `=`.
2. **predict.** `mana = 18` / `mana = mana - 5` / `mana = mana - 5` / `print(mana)` → `8`. Why not 13: the box
   keeps only its latest value.
3. **bug.** `print("It is not a compass)` → add the closing quote.
4. **predict.** `print("█" * 2 + "░" * 3)` → `██░░░`.
5. **fill.** `print("Mana: " + ___(7))` → `str`.
6. **mc.** "Mar'tu changes `lantern_count` to 5. Which `total` line stays right?" (only the one built from the
   boxes)
7. **mc.** "`Health = 100`, then `print(health)`. What happens?" (NameError: names are exact)
8. **predict.** `rope_count = 5` / `rope_price = 2` / `print(rope_count * rope_price + 2)` → `12`.

### Project 1P1 "The Night Watch Ledger" [SC, 18 min] (u01c)

**Premise.** The barrier must hold until the next burst, 37 hours away. Mar'tu keeps a ledger of what the night
will cost: mana for the barrier and flasks of lantern oil.

**Starter** (S2): the task-group headers are always there (`# A. What we know`, `# B. Let the code combine it`,
`# C. Write the ledger`). Under "Show me more", the placeholders (`= 0`) and the full ladder are added.

**Tasks** (one checkpoint each):
- **A. What we know**
  1. `hours_until_burst = 37`.
  2. `mana_per_hour = 2`, `oil_per_hour = 1`, `oil_price = 3`.
- **B. Let the code combine it**
  3. `mana_needed` from the hours and the mana per hour. [ND]
  4. `oil_needed` and `oil_cost`. [ND]
- **C. Write the ledger**
  5. Print `Mana for the barrier: 74`, built from the boxes.
  6. Print the oil line (flasks and coins).
  7. Make `watch_keeper` hold any hero, in quotes, and print `First watch: <hero>`. **Echo** spot.

**Checks:**
- CMB: a rerun with `hours_until_burst = 32` updates every line.
- The watch-keeper accepts any text (lint e).
- "Use Mar'tu's picks" fills the creative blanks.

**Lucky's side quest (the old task group, pool, ~15 min):**
- Lucky's glug fee (`glug_sips * glug_price`, with the price his choice);
- a divider made with `"~" * 24`;
- `total_coins`;
- a reserve mana bar (1C-08).

**Trial mode** (after a QC1 pass): the premise, the required output and the check table, from blank.

**WA:** `mana_needed = 74` → task 3, "32"; a ledger line typed → task 5, "32"; `print("~~~~…")` typed in the side
quest → its check, "repetition".

### Project 1P2 "The Ward Sign" [O, 25 min] (u01d)

**Premise.** Mar'tu wants a ward sign painted on the barrier post, in big block letters (the default word is
`TOR`).

**Tasks:**
1. Draw each letter five rows tall with `print` and `ink * n`.
2. A border made with repetition.
3. `ink = "█"` (pre-typed), so one change repaints the whole sign.
4. One letter as a triple-quoted string (prerequisite card: 1A-07).

**Checks:** at least 5 rows; CMB with `ink = "#"`.

**Side quest:** sign the post in your hero's spell color (a word under the sign).

### Article 1-A2 "Clock Math" [O, 12 min] (u01d)

`**`, `%` and `//`, and order of operations. Ley Clock example: "The hand moves one mark an hour around 12 marks.
50 hours from mark 9, where is it?" `(9 + 50) % 12` → 11. Also `2 + 3 * 4` → 14 versus `(2 + 3) * 4` → 20,
`2 ** 3` → 8, `50 // 12` → 4. Intro `op:Pow` `op:Mod` `op:FloorDiv`.

- **Try-it 1-A2a `where-is-the-hand`:** `hand = (start + hours) % 12` [CMB].
- It is the prerequisite card for 8P2 and for 1C-08's 10-wide side quest.

### Article 1-A3 "Asking the Traveler: `input()`" [O, 15 min] (u01d)

`input()` always returns text, so convert with `int()` for math. The replay shim lets students answer in the
console. Intro `call:input` `call:int`.

- **Try-it 1-A3a `who-goes-there`:** greet the traveler, then double their sips of glug. `stdin=["Lucky", "3"]`.
  Checks: `_inputs_used() == 2`, plus CMB through stdin.
- Campaign link: `user.clicked()` also hands back text, which is compared with `==`.

### Quick Check 1 [O, test-out, ~12 min] (u01d: `qc1-a`, `qc1-b`, `qc1-a-questions`, `qc1-b-questions`)

Five code tasks plus three questions per form. Form B changes every name and value (`familiar`, candles,
Bomb Shell's 12 → 24, `▓`).

| # | Form A item | Type | Skills | Fails on (evidence wrong answer) |
|---|---|---|---|---|
| Q1 | "What does `print("Mana [" + "█" * 3 + "░" * 2 + "] " + str(3) + "/" + str(5))` show?" (G4 R26) | mc | `repeat-string`, `concat-str` (reading) | choosing `Mana [███░░] 3/5` without the space, or `█3░2` |
| Q2 | `x = 5` / `x = x - 2` / `print(x)` | predict | `reassign` | `5 2`, `7` |
| Q3 | "Which line is a box whose name Python accepts?" `magical affinity = 9` / `magical_affinity = 9` / `"magical_affinity" = 9` | mc | `exact-names` | the space or the quotes |
| C1 | `Example: companion = "Gearshift"` is shown beside the task "Make a variable named `character` that holds any hero, then print it." DF is available. | code | `make-variable`, `exact-names`, `quote-text` | `companion = "Zelda"` (copying the example's name; A-05–A-08) → NAME/LEFT; a lone `"Zelda"` → BARE; `character = Zelda` → crash |
| C2 | "Rope costs 2 coins a coil; Mar'tu needs 5. Lanterns: 3 at 4 coins. Make `total_cost`." | code | `combine-values` | `total_cost = 22` → CMB; swapped rope → SWAP |
| C3 | Status line from `hero_name` and `magical_affinity`, with `max_mana` computed | code | `combine-values`, `concat-str`, `reassign` | the line typed → CMB (`"Tester"`); `str` missing → crash |
| C4 | Build `bar` for any `mana` and `max_mana` (blocks pre-typed) | code | `repeat-string` | no parentheses → crash; `empty * 2` → CMB |
| C5 | Mend three lines: `print("Shield up.)`, `mana = mana - "3"`, and `Max_Mana = 18` / `print(max_mana)` (G4 R1 #6) | code (3 CPs) | `quote-text`, `numbers-vs-text`, `exact-names`, `read-traceback` | leaving `Max_Mana` → CP3, "max_mana"; `mana - "3"` → crash |

Every claimed skill has a failable item (lint d). A pass sets "Keep it short" for Unit 1 and converts the
lessons per §2.4. `numbers-vs-text` and `reassign` are claimed through C3, C5 and Q2.

### Cheatsheet 1 "Mar'tu's Chalk Notes: First Words" (u01d)

- `print("text")`; quotes and brackets come in pairs; `# note`.
- `name = value`: **a box's name never has quotes**; numbers have no quotes. The quotes sentence.
- `mana = mana - cost` (read: mana gets mana minus cost); `+ - * /` (`/` gives a decimal).
- How many × how much is one, and let the code combine it.
- `"Mana: " + str(7)`; `"█" * 3 + "░" * 2` → `███░░`; `"░" * (a - b)` needs parentheses.
- Error quick reference: unclosed quote or bracket, a name it doesn't know, a space in a name, text plus a number.
- *(extra)* `"""many lines"""`, `+=` / `-=`.

---

## Unit 2 · Control Flow: "The Ley Clock Decides" (`control-flow`, files u02a–u02c)

**Mar'tu's framing.** "The Ley Clock does not panic. It checks. If the hand is near the arc, it warns. Otherwise,
it waits. Today you teach Python to check the same way. And you learn to roll dice, because the world is not
fair, yes?"

**RPG tie-in.** Skill checks (a d20 roll against a required roll), the clock's color by the hours left, Lucky's
Dumb Luck reroll, and a four-answer dialogue chain.

**Learning objectives. Student can…**
1. Evaluate comparisons (`== != < > <= >=`) to `True` / `False`, and store one in a variable.
2. Tell `=` ("gets") from `==` ("is the same as").
3. Predict boundary results and choose `<` versus `<=` on purpose ("exactly enough mana still casts").
4. Compare text exactly (every letter, space and capital), and case-safely with `.lower()`.
5. Write `if`, `if/else` and `if/elif/else` with colons and indentation, knowing the first true branch wins.
6. Combine conditions with `and`, `or` and `not` (SC).
7. Use `import random` and `random.randint(a, b)`, knowing both ends are included.
8. Read a traceback (the last line, the line number, the type) and fix SyntaxError, IndentationError, NameError
   and TypeError. Debug a wrong answer by printing values.

**Campaign links.**
- Obj 1–3 → `skill-checks` (`return roll >= required_roll`) and `hold-the-barrier` (`<`, not `<=`).
- Obj 4–5 → `program-dialogue-options` (the four-branch chain on `"option 1"`) and `.lower().capitalize()`.
- Obj 7 → `perform_roll(die_size)`.
- Obj 8 → every part.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 2A "True or False, Yes?" (with 2A-remembers) | CC (2A-05 SC) | 20 | u02a |
| 2 | Lesson 2B "If the Clock Turns Red" (with 2B-remembers) | CC (2B-06, 2B-09 SC) | 41 | u02b |
| 3 | Article 2-A1 "Match: Another Way to Choose" | O | 12 | u02b |
| 4 | Quiz 2 | SC | 8 | u02b |
| 5 | Project 2P1 "Road Encounter Table" | SC (protected story beat) | 18 | u02b |
| 6 | Project 2P2 "Three Roads to the Institute" | O | 35 | u02c |
| 7 | Lesson 2C "When Spells Fizzle: Reading Errors" (with 2C-remembers) | CC (2C-05 SC) | 18 | u02c |
| 8 | 2X Extra practice: more fizzles (2C-02, 2C-03, 2C-04) | pool | 11 | u02c |
| 9 | Article 2-A2 "Mar'tu's Seal" (asserts) | O | 10 | u02c |
| 10 | Quick Check 2 (forms A, B) | O | 10 | u02c |
| 11 | Cheatsheet 2 | ref | — | u02c |

### Lesson 2A "True or False, Yes?" [CC, 20 min] (u02a)

*Mar'tu remembers… (`2a-remembers`)*
1. Predict `"█" * 2 + "░" * 3`. (1C)
2. "In `rope_count * rope_price`, which one is 'how many'?" (1C)

- **2A-01 `true-or-false` · True or False** · intro `const:bool` `op:Gt` `op:Lt` · P→R→M · S4 · CC · `compare`
  - Learn: "A comparison is a yes/no question. Python answers `True` or `False`, with no quotes."
  - Predict: `print(18 > 12)` and `print(6 > 15)` (Bomb Shell's DEX is 6; the latch needs 15).
  - Starter: `dex = 6` / `needed = 15` / `print(dex > needed)` / `barrier_up = 0`.
  - CP1 [D] "Change the `print` to show whether `dex` is **less than** `needed`." Checks: `'True' in _lines()`;
    CMB (`dex = 16` → `False`).
  - CP2 [D] "Make `barrier_up` hold `True`, with no quotes, and print it." Checks: `barrier_up is True`; with
    quotes, the message is "`"True"` is text. `True` with no quotes is Python's yes."
  - Hints: P "Which sign means *less than*?" T "`3 < 5` is True; `5 < 3` is False." S `print(dex < needed)`.
  - AW: everyday (a yes/no question) · picture (a light switch) · step-by-step (Python works out the comparison,
    then prints the answer) · shorter.
  - WT: "`True` has no quotes."
  - BQ (combining arithmetic + comparison): "Gearshift steadies Bomb Shell's hands (+10). Print whether
    `dex + 10` beats the latch."
  - WA: `print(True)` → CP1, "16"; `barrier_up = "True"` → CP2, "text".
- **2A-02 `ask-with-double-equals` · Asking with `==`** · intro `op:Eq` `op:NotEq` · P→I→M · S4 · CC ·
  `compare`
  - Learn: "`=` puts a value in a box: read it as *gets*. `==` asks a question: read it as *is the same as*."
  - Starter: `clock_color = "blue"` / `clock_is_red = (clock_color == "red")` / `print(clock_is_red)` /
    `hero = "Bomb Shell"`. The first exposure keeps the parentheses (G1 R11).
  - Predict → `False`.
  - Investigate: set `clock_color = "red"` (→ True), then `"Red"` (→ False), with the STREXACT note.
  - CP1 [D] "Add a line that prints whether `clock_color` is **not** `"red"`, using `!=`." Check: CMB
    (`"red"` → False).
  - CP2 [ND] "Make `is_lucky` hold whether `hero` is the same as `"Lucky"`." Names: `is_lucky`. Checks: a bool;
    CMB (`hero = "Lucky"` → True).
  - Catches:
    - `is_lucky = "Lucky"` → "That puts the text in the box. Ask with `==`."
    - `is_lucky = hero = "Lucky"` → "not a bool".
    - `!= "Red"` → CMB fails at `"red"`, with STREXACT.
  - Hints (CP2): P "This line has a *gets* and an *is the same as*." T `same = (a == b)`. S
    `is_lucky = (hero == "Lucky")`.
  - AW: shorter ("`=` puts; `==` asks") · picture (filling a box versus a `?` between two boxes) · everyday
    (writing your name tag versus asking "are you Lucky?") · step-by-step (the right side first).
  - PA: distractor `is_lucky = hero = "Lucky"`.
  - BQ (combining two boxes + `==`): "Make `same_color`: is Mar'tu's spell color the same as Lucky's?"
  - WA: `is_lucky = "Lucky"` → CP2, "==".
- **2A-03 `enough-to-pass` · Enough to pass** · intro `op:GtE` `op:LtE` · P→I→M · S4 · CC · `boundary` ·
  point-at-it
  - Learn: "`>=` means *at least*. A roll of exactly the number needed still passes."
  - Predict: `roll >= needed` for rolls 14, 15 and 16, against `needed = 15`.
  - Starter: `roll = 15` / `needed = 15` / `# passed: does roll reach needed?` / `mana = 6` / `cost = 6` /
    `# can_cast: does mana cover cost?`. No parentheses from here on.
  - CP1 [ND] "Make `passed` say whether `roll` reaches `needed`. Exactly enough counts." Check: BND (14/15/16).
  - CP2 [ND] "Make `can_cast` say whether `mana` covers `cost`. Exactly enough mana still casts." Check: BND.
  - Point-at-it: "Which sign makes 'exactly enough' pass?"
  - Hints: P "Should a 15 pass when 15 is needed?" T "`>` leaves out the boundary; `>=` includes it." S
    `passed = roll >= needed`.
  - AW: in Tor ("a 15 opens a latch that needs 15") · from the campaign ("use `<` and not `<=`, because a caster
    with exactly enough mana can still cast") · picture (a number line with a filled dot) · step-by-step (try
    14, 15, 16).
  - TR: static table.
  - BQ (combining `==` + `>=`): "Make `close_call`, True only when the roll is exactly `needed`, and print both."
  - WA: `passed = roll > needed` → CP1, "exactly"; `can_cast = True` → CP2, BND.
- **2A-04 `any-case-answer` · Any case, same answer** · intro `attr:lower` · P→I→M · S4 · CC · `compare`,
  (prereq for) `chain-methods`
  - Learn: "`"YES" == "yes"` is False: every letter, space and capital counts. **The dot means: ask this text to do
    something.** `answer.lower()` gives a lower-case copy." (G1 unnumbered)
  - Starter: `answer = "YES"` / `said_yes = answer == "yes"` / `print(said_yes)`.
  - CP1 [D] "Make `said_yes` True for any capitals: use `answer.lower()`." Check: CMB (four reruns: `"YES"`,
    `"yes"`, `"YeS"` → True; `"no"` → False).
  - Catches: `answer.lower == "yes"` → "`.lower` without `()` doesn't run. Add `()`."; `== "YES"` → STREXACT.
  - Hints: P "Which part changes the capitals?" T `"HI".lower()` gives `"hi"`. S
    `said_yes = answer.lower() == "yes"`.
  - AW: picture (a text copied in small letters) · everyday (a librarian who ignores capitals) · from the campaign
    (Module 1 tidies lines with `.lower()`) · shorter.
  - BQ (combining two method calls + `==`): "Make `same`: do two answers match, whatever their capitals?"
  - WA: `answer.lower == "yes"` → CP1; `said_yes = True` → CP1, CMB.
- **2A-05 `broken-spell-2A` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - `passed = roll => needed` (SyntaxError);
    - `needed = "15"` (TypeError in `>=`);
    - `clock_is_red = "red"` (it assigns instead of asking; no error, so the check is "not a bool").
  - Hints per bug.
  - WA: each bug left fails its own CP.
- **2A-S `solo-2A` · Show Mar'tu** · SOLO, one bug · CC
  - By seat: A `can_cast = mana > cost` with `mana = cost = 9` (a boundary bug); B `can_cast = mana >= "9"`
    (TypeError).
  - CP1 [ND] "Make `can_cast` right. Exactly enough mana still casts."

### Lesson 2B "If the Clock Turns Red" [CC, 41 min] (u02b)

*Mar'tu remembers… (`2b-remembers`)*
1. "`=` or `==`: which one asks?" (2A)
2. Predict `"Mana: " + str(4 + 3)`. (1C)

- **2B-01 `first-if` · If** · intro `node:If` · P→R→I→M · S4 · CC · `if-else`
  - Learn: "`if` asks a question. When the answer is True, Python runs the indented lines under it. When it is
    False, Python skips them."
  - Starter: `hours_left = 2` / `if hours_left < 3:` / `    print("Get inside!")`.
  - Investigate: change `hours_left` to 10, and nothing prints. Why? (one click)
  - CP1 [D] "Add a second indented line under the `if` that prints `Shield up.`" Check: CMB (2 → both lines; 10 →
    neither).
  - Hints: P "Indented lines belong to the `if`." T a two-line `if` example with different words. S the
    indented print.
  - AW: picture (a fork in the road) · everyday (if it rains, take the umbrella) · step-by-step · in Tor ("the
    barrier door opens only if…").
  - TR: static table.
  - BQ (combining `if` + concat): "Put the hours left inside the warning, with `str()`."
  - WA: the second print not indented → CP1, "10".
- **2B-02 `colon-and-indent` · Colon and indent** · intro — · D · CC · `if-else`, `read-traceback`
  - Bugs, one checkpoint each, each with its explainer row:
    - a missing colon (`expected ':'`);
    - a body with no indent (IndentationError);
    - a line that should always run, indented by mistake (behavior only: CMB).
  - AW: step-by-step ("the colon says *here comes the block*; the indent says *this belongs to it*") · picture
    (indentation as a shelf).
  - WA: each bug left fails its CP.
- **2B-03 `otherwise` · Otherwise** · intro — (`else` has no token) · M · S3 · CC · `if-else`, `boundary`
  - Example: Oogrish's perception check, `spot_roll = 13`, `spot_needed = 11`, if/else with "Oogrish spots the
    tracks." / "Nothing but mud." → `Oogrish spots the tracks.`. foreign: `spot_roll`, `spot_needed`.
  - Starter (skeleton): `strength_roll = 14` / `strength_needed = 12` / `if ___:` / `    # success line` /
    `else:` / `    # failure line`
  - CP1 [ND] "Bomb Shell pries the latch. Print a success line when `strength_roll` reaches `strength_needed`, and
    a failure line otherwise." Check: BND over 3 reruns. Any two different lines pass.
  - Catches: the Example's names → NameError, explainer rule 3 ("`spot_roll` comes from the example…"); `>` →
    BND.
  - Hints: P "What question decides which line runs?" T "`else:` has no question; it runs when the `if` didn't."
    S `if strength_roll >= strength_needed:`.
  - AW: picture (two doors) · everyday (rain → coat, otherwise → sunglasses) · step-by-step · shorter.
  - PA: distractors `if strength_roll > strength_needed:`, `else strength_roll < strength_needed:`.
  - DF: "The latch pops open." / "That latch hates me."
  - BQ (combining if/else + concat): "Show the roll in both lines."
  - Twin: a Gearshift lift check.
  - WA: `if spot_roll >= spot_needed:` → crash, "spot_roll"; `>` → CP1, "exactly".
- **2B-04 `clock-colors` · Clock colors** · intro — (`elif`) · P→I→M · S4 · CC · `elif-chain`
  - Learn: "`elif` means *else, if*. Python checks the branches from the top and takes the **first** true one."
  - Starter: the chain in the wrong order: `<= 12` → `"bright blue"` first, then `<= 2` → `"red"`, else `"calm blue"`.
  - Investigate: which hours get the wrong color? (2 gives bright blue.)
  - CP1 [D] "Put the branches in an order where 2 hours gives `"red"`." Check: CMB for 1, 2, 3, 12, 13, 40.
  - Hints: P "Which branch does hour 2 reach first?" T "First true wins: put the narrowest test first." S the
    reordered chain.
  - AW: everyday (a line of doors; you take the first one that opens) · picture · step-by-step trace · shorter.
  - TR: static table.
  - BQ (combining chain + concat): "Print `Clock: <color> (<hours>h)`."
  - WA: the order unchanged → CP1, "2".
- **2B-05 `four-answers` · Four answers** · intro — · A→M · S4 · CC · `elif-chain`, `quote-text` · rehearsal
  (`program-dialogue-options`)
  - Setup: `mar_tu_says(text)` and `light_up_box()` (CALL recorders); `choice` is set per rerun.
  - Starter (Assemble-first under "Show me more", typed under "Keep it short"): numbered comments (1:1 with the
    checkpoints), then the chain with `___` in place of each option:
    - `# 1. Replace each ___ with "option 1", "option 2", "option 3" or "option 4" (keep the quotes), in order.`
    - `# 2. Add light_up_box() under each mar_tu_says line.`
  - CP1 [D] "Replace each `___` with `"option 1"`, `"option 2"`, `"option 3"` or `"option 4"`, keeping the quotes,
    in order." Check: CALL (four reruns; each choice says its own line).
  - CP2 [D] "Add `light_up_box()` under each `mar_tu_says` line." Check: CALL (the box lights once per choice).
  - Catches:
    - `elif choice == option 2:` → **SyntaxError** (verified), the multi-word row: "put them in quotes".
    - `elif choice = "option 3":` → the `=`-in-`if` row.
    - `"Option 1"` → STREXACT.
    - `light_up_box()` under only one branch → CALL ("When choice was "option 3", no box lit.").
  - Hints: P "Which part must keep its quotes?" T the quotes sentence. S the first two branches.
  - AW: from the campaign (Module 1's dialogue boxes, described without spoilers) · step-by-step · picture (four
    boxes on a board).
  - PA: distractors `elif choice == option 2:`, `elif choice = "option 3":`, an unindented `light_up_box()`.
  - BQ (combining chain + `else`): "Add an `else:` that says `Hm.` for any other choice."
  - WA: unquoted → crash, "invalid syntax"; only one helper → CP2, "option 3"; `"Option 1"` → CP1, "capital".
- **2B-06 `and-or-not` · And, or, not** · intro `op:And` `op:Or` `op:Not` · P→I→M · S4 · SC · `and-or-not`
  - Three checkpoints [D, D, ND], each with CMB:
    - `can_cast = mana >= cost and affinity >= required` (Oogrish's affinity 9; Lantern Ward needs 9);
    - `lucky_passes = first_roll >= needed or second_roll >= needed`;
    - `not barrier_up`.
  - AW: step-by-step (a truth table using the real stats) · everyday (`and` = both keys, `or` = either key) ·
    picture · shorter.
  - WT: "`and` needs both; `or` needs one."
  - BQ (combining `or` + `and`): "Lucky passes on the first roll, or on the second if he still has Dumb Luck."
  - WA: `or` used for `can_cast` → CP1, CMB.
- **2B-07 `roll-a-die` · Roll a die** · intro `node:Import` `import:random` `attr:randint` · P→R→I→M · S4 · CC
  · `randint`
  - Learn: "`import random` lends you Python's dice. `random.randint(1, 6)` gives a whole number from 1 to 6,
    **both ends included**."
  - Predict: can it give 6? 0? Run it several times.
  - Starter: `import random` / `staff_roll = random.randint(1, 1)  # the Staff of Wisdom is a d6` /
    `sword_roll = 0  # the longsword is a d8` / two prints.
  - CP1 [D] "Make `staff_roll` a d6 roll: `random.randint(1, 6)`." Check: RND.
  - CP2 [ND] "Make `sword_roll` a d8 roll." Check: RND.
  - Catches: `randint(0, 6)` and `randint(1, 5)` (the top-excluded belief) → "A d6 has faces 1 to 6, and
    `randint` includes both ends."
  - Hints: P "How many faces does a d8 have?" T `random.randint(1, 4)` gives 1, 2, 3 or 4. S
    `sword_roll = random.randint(1, 8)`.
  - AW: picture (the die's faces) · everyday (drawing a numbered card) · contrast ("`range` stops before the end;
    `randint` includes both ends", revisited in 3B) · step-by-step.
  - BQ (combining two rolls + concat): "Roll both and print their total."
  - WA: `randint(1, 5)` → CP1; `randint(0, 8)` → CP2.
- **2B-08 `roll-and-decide` · Roll and decide** · intro — · Mk · S3 (skeleton, G3 R19) · CC · `randint`,
  `boundary`, `if-else`
  - Starter: `import random` / `action = "pry the trap door open"` / `needed = 12` / `roll = ___` /
    `if ___:` / `    # success line with the roll` / `else:` / `    # failure line with the roll`
  - CP1 [D] "Roll a d20 into `roll`." Check: RND.
  - CP2 [ND] "Print a success line when `roll` reaches `needed`, a failure line otherwise." Check: BND + RND
    (scripted `needed - 1`, `needed`, `needed + 1`).
  - CP3 [ND] "Put the roll in the line you print." Check: the printed line contains `str(roll)` under scripted
    rolls.
  - DF: the action and `needed` (any action text; any needed from 2 to 20).
  - Hints: P per CP. T `str()` for the roll. S the success line.
  - AW: step-by-step · from the campaign (skill checks, described) · picture (d20 against a target).
  - PA: yes.
  - BQ "Dumb Luck" (combining randint + a nested `if`): "If the first roll fails, roll once more."
  - WA: `roll > needed` → CP2; `random.randint(1, 19)` → CP1.
- **2B-09 `broken-spell-2B` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - `random.randint` with no `import random` ("Did you forget to import 'random'?" → rule 6b);
    - `if roll = 20:`;
    - an `elif` after `else`;
    - `elif choice == option 1:` (SyntaxError).
  - WA: each bug left fails its CP.
- **2B-S `solo-2B` · Show Mar'tu** · SOLO, one bug · CC
  - By seat: A has a missing colon on `if hours_left <= 2`; B has an unindented body.
  - CP1 [ND] "Make it print `Inside, now.` when 2 hours or fewer are left." Check: CMB.

### Article 2-A1 "Match: Another Way to Choose" [O, 12 min] (u02b)

Rewrite the four-answers chain with `match choice:` / `case "option 1":` / `case _:`. Intro `node:Match`.
- Try-it: the five-option version [CALL].
- Note: the campaign uses `elif`, so learn to read both.

### Quiz 2 [SC, 8 questions] (u02b)

Types: 2 mc · 4 predict · 1 parsons · 1 bug.
1. **predict.** `roll = 12` / `needed = 12` / `print(roll >= needed)` / `print(roll > needed)` → `True`, then
   `False`.
2. **predict.** The three-branch clock chain with `hours_left = 2` → `red`.
3. **mc.** "Which values can `random.randint(1, 6)` give?" Choices: 0–5 / 1–5 / 1–6 / 0–6. **Answer:** 1–6.
4. **predict.** `mana >= cost and affinity >= required` with affinity 8 and required 9 → `False`.
5. **parsons.** A four-option chain with indentation. Distractor: `elif choice == option 2:`.
6. **bug.** `if roll = 20:`.
7. **mc.** `=` versus `==`: "Which line asks whether `hero` is Lucky?"
8. **predict.** An order-matters chain (a wide test first).

### Project 2P1 "Road Encounter Table" [SC, 18 min, protected story beat] (u02b)

**Premise.** The road to the old Institute is long. Oogrish insists on an encounter table: roll a d20 and see
what the road throws at you. You write the encounters.

**Starter:** the task-group headers (A, B, C). Under "Show me more", the tier skeleton.

**Tasks:**
- **A. Roll**
  1. `import random`.
  2. Roll `road_roll` with a d20.
- **B. Table**
  3. `if/elif/else` with these tiers, storing any text per tier in `encounter`:
     - 1: Lucky fires the Telegun (hedge);
     - 2–6: a ley-line hums under the road;
     - 7–15: a quiet road;
     - 16–19: a brass-cart peddler;
     - 20: a starlode vein for Gearshift.

     **Echo**: Mar'tu reacts to one tier's text.
- **C. Tell it**
  4. Print `"Rolled " + str(road_roll) + ": " + encounter`.

**Checks:**
- RND + BND with scripted rolls 1, 2, 6, 7, 15, 16, 19 and 20.
- Same-tier rolls give the same `encounter`, and neighboring tiers give different ones.
- The printed line includes the roll.
- Any encounter text passes (lint e). "Use Mar'tu's picks" fills the tiers.

**Lucky's side quest (old group D, pool):**
- a perception check with `and not night_time`;
- Dumb Luck: reroll a 1, once.

**WA:** `if road_roll < 6` for tier 2–6 → task 3, "6"; the tiers out of order → task 3; `randint(1, 19)` → task 2.

### Project 2P2 "Three Roads to the Institute" [O, 35 min] (u02c)

Three ways to travel:
- **Gearshift's jeep form:** 2 starlode a mile, plus 5 to start.
- **On foot:** glug rations by distance tier.
- **Lucky's Telegun:** free, but a roll under 15 lands you in a hedge.

**Tasks:** the ration cost with `elif` tiers; the jeep formula; pick the cheapest with comparisons and `and`;
print the choice and its cost.

**Checks:** CMB reruns at distances 5, 30 and 80 pick the right road.

### Lesson 2C "When Spells Fizzle: Reading Errors" [CC, 18 min] (u02c)

The syllabus's Errors lesson, kept at the end of the unit. The full four-step routine lives here. The two-step
footer has been on since 1W-02.

*Mar'tu remembers… (`2c-remembers`)*
1. "Can `random.randint(1, 6)` give 6?" (2B)
2. A two-branch trace. (2B)

- **2C-01 `anatomy-of-a-fizzle` · Anatomy of a fizzle** · intro — · I · S3 · CC · `read-traceback`
  - Run a five-line program that fails on line 4 (a NameError on `mana_cost`).
  - Record what the traceback says in three boxes. These practice boxes, too.
  - CP1 [ND] "Make `bad_line` hold the line number." Check: NUM.
  - CP2 [ND] "Make `error_type` hold the error's name, as text." Check: TEXT, with the special case:
    `error_type = NameError` (unquoted) runs silently, so "`NameError` without quotes is Python's own name for
    that error. Write the words in quotes: `"NameError"`." (G2 R14)
  - CP3 [ND] "Make `missing_name` hold the name Python couldn't find." Check: TEXT.
  - Hints: P "Read the last line first." T the annotated-traceback picture. S the three lines.
  - AW: picture (annotated traceback) · step-by-step (the footer) · everyday (a note Python leaves you) ·
    shorter.
  - BQ (combining boxes + concat): "Print `Line 4: NameError (mana_cost)` built from your three boxes."
  - WA: `error_type = NameError` → CP2, "quotes"; `bad_line = "4"` → CP1, "number".
- **2C-05 `no-error-wrong-answer` · No error, wrong answer** · intro — · D/I · SC · `boundary`
  - A caster with exactly enough mana doesn't cast.
  - Add `print(mana)` and `print(cost)` above the `if`, then fix the comparison.
  - CP1: exactly enough now casts [BND].
  - WT: "Print-debugging is a real technique."
- **2C-06 `equals-is-not-def` · `=` is not `def`** · intro — · D · CC · `make-variable`
  - Starter: `def hero = "Lucky"` (unparseable on purpose; the harness allows it with a warning).
  - Mar'tu: "`def` is for making recipes. We start those next unit. A box needs only `=`."
  - CP1 [D] "Make `hero` a box that holds `"Lucky"`." Checks: NAME, TEXT.
  - Inoculates against the next unit's `def`-heavy starters reactivating A-02's belief.
- **2C-07 `debug-routine` · The four-step routine** · intro — · D · CC · `read-traceback`
  - The routine:
    1. Read the last line.
    2. Go to the line it names.
    3. Check the line above.
    4. Print the values.
  - A 12-line encounter script with three bugs, one checkpoint each:
    - a typo, `encounterr` (rule 6: "Did you mean");
    - `"Rolled: " + roll` (TypeError);
    - a `>` that should be `>=` (no error, so step 4 finds it).
  - Oogrish's Help label: "Steady, now. Read the last line first."
- **2C-S `solo-2C` · Show Mar'tu** · SOLO, one bug · CC
  - By seat: A `print("Mana: " + mana)`; B `print("Roll: " + roll)`.
  - CP1 [ND] "Make the line print." Checks: CMB, `str`.

### Extra practice 2X "More fizzles" [pool] (u02c)
- **2C-02 `syntax-fizzles`:** a missing `)`, a missing `:`, an unclosed quote. Investigate: why does Python
  report only one at a time?
- **2C-03 `name-fizzles`:** a typo (`mama`, rule 6), a variable used before it is made, unquoted text, and a case
  slip (rule 5: "health / heath"). These prove explainer rules 5 and 6.
- **2C-04 `type-fizzles`:** text plus a number; a number compared with quoted text.

### Article 2-A2 "Mar'tu's Seal" [O, 10 min] (u02c) (G4 R15)

"At the Institute we sealed our work: a line that says what *must* be true. If it isn't, Python stops and tells
you." Intro `node:Assert`.

- Example: `assert passed == True`.
- **Try-it `seal-the-check`:** for `passed = roll >= needed`, write three asserts at the boundary (one below,
  exactly, one above). Check: `_count('node:Assert') >= 3`, and the asserts pass against the correct line and
  fail against a `>` version (the check reruns them against both).
- Re-offered as a side quest in 6A-09 and in T-Own. `node:Assert` is optional-only, so the core gate is
  unaffected.

### Quick Check 2 [O, ~10 min] (u02c: `qc2-a`, `qc2-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| Q1 | Booleans at the boundary (rolls 11, 12, 13 against 12) | predict | `compare`, `boundary` | `>` thinking (12 → False) |
| Q2 | Trace a three-branch `elif` for three values | predict | `elif-chain` | not knowing that the first true branch wins |
| Q3 | Values `randint(1, 8)` can give | mc | `randint` | 0–8, 1–7 |
| Q4 | `not (mana >= cost and affinity >= required)` with real stats | predict | `and-or-not` | treating `and` as `or` |
| C1 | Roll a d20 against your own `needed` with if/else | code | `randint`, `boundary`, `if-else` | `>` → BND; `randint(1, 19)` → RND |
| C2 | Mend `if choice = "option 1":` and `elif choice == option 2:` | code (2 CPs) | `read-traceback`, `elif-chain`, `quote-text` | either line left → crash |

Form B uses `hours_left` tiers, a d12, and `option 3` / `option 4`.

### Cheatsheet 2

- `True` / `False` (no quotes); `==` asks, `=` puts; `< <= > >= !=`.
- Exactly enough: `>=`.
- `if x:` plus indent, `else:`, `elif` (the first true branch wins).
- `and` / `or` / `not`; `text.lower() == "yes"`.
- `import random`, then `random.randint(1, 20)` includes both 1 and 20.
- The four-step error routine.
- *(extra)* `match`, `assert`.

---

## Unit 3 · Functions I: "First Recipes" (`first-recipes`, files u03a–u03b) — D11

**Mar'tu's framing.** "At the Institute we called these *recipes*. You write the steps once and give them a name.
When you need them, you call the name. Some recipes need ingredients. Some hand something back. Nobody in this
cabin has written one yet. That is fine. That is why we start now, yes?"

**Why here.** This is the class's cliff: 0 of 11 students wrote a working function. The unit uses **only Unit 1–2
ideas** plus `def`, `pass`, `return` and `.capitalize()` (the M1 gate path proves it). Recipes then come back in
every later unit: in warm-ups, in each quiz, and in converted exercises (3A-06, 4P, 5A-07, 5P).

**Learning objectives. Student can…**
1. Tell `=` (a box) from `def` (a recipe). Know that defining doesn't run anything. Call with `()`.
2. Replace `pass` with a call, correctly indented.
3. Define parameters, pass arguments, and **use the parameters in the body**, never one call's numbers. Every
   function is shown with at least two calls.
4. `return` a value, store a call's result, explain `None`, and return the right name.
5. Trace a call with constants inside, carrying the returned value into the next box.
6. Store what a helper returns, then pass it on. Read `.lower()` then `.capitalize()`.
7. Return a comparison (`return roll >= needed`).
8. Use `random.randint(1, die_size)` with a parameter.

**Campaign links.**
- Obj 2 → `program-movement`.
- Obj 6 → `program-dialogue-prompt` (store, pass, `.lower()` / `.capitalize()`).
- Obj 7–8 → `skill-checks`.
- Together, Units 1–3 cover every line of Module 1.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 6A "Recipes With Names" (with 6A-remembers) | CC (6A-11 SC; 6A-05a K) | 60 (+3 K) | u03a |
| 2 | Quiz 6A | CC (retrieval for the cliff) | 8 | u03a |
| 3 | 3X Extra practice: recipe twins (6A-T1–T3) | pool | 9 | u03b |
| 4 | "Before the cabin door" (Route M1 only) | M1 | 10 | u03b |
| 5 | Quick Check Recipes I (forms A, B) | O | 12 | u03b |
| 6 | Cheatsheet 3 | ref | — | u03b |

### Lesson 6A "Recipes With Names" [CC, 60 min] (u03a)

*Mar'tu remembers… (`6a-remembers`)* (Units 1–2 only, so the lesson stays portable)
1. "`=` or `==`: which one asks?" (2A)
2. "What does `mana = mana - 3` do?" (1C)

- **6A-01 `box-or-recipe` · A box or a recipe?** · intro `node:FunctionDef` · P→R→I→M · S4 · CC · `def-call` ·
  **moment** (teacher-led, 5 min)
  - Learn: "A box holds a value. A recipe (function) holds steps. `def` makes a recipe. Making it does not run it.
    Calling its name with `()` runs it."
  - Starter: `steadying_words = "Steady, now."` (a box) above `def say_steady():` / `    print("Steady, now.")`
    (a recipe).
  - Predict: what does Run print? (nothing / `Steady, now.` / it twice / an error) → nothing.
  - CP1 [D] "Call the recipe: add `say_steady()` at the bottom." Check: the line prints once.
  - CP2 [D] "Make it say it twice, using two calls, not two `print`s." Checks: `_count('call:print') == 1`, and two
    lines are printed.
  - Catches: A-02 `def ("character")` (shown in the box-versus-recipe contrast panel); `say_steady` without `()`
    → "No `()` means it isn't called."
  - Hints: P "Where does anything get *called*?" T "A name with `()` after it runs that recipe." S `say_steady()`.
  - AW: everyday (a jar holds a thing; a recipe card holds steps) · picture (box and card side by side) ·
    step-by-step (the `def` line is read and remembered; nothing runs until the call) · from the campaign ("Each
    `def` line makes a function: a named set of steps.") · in Tor.
  - TR: a static step table showing the `def` being skipped until the call.
  - BQ (combining recipes inside recipes): "Write `say_ready()` that prints a line and then calls `say_steady()`."
  - WA: `say_steady` with no `()` → CP1; two `print`s → CP2, "calls".
- **6A-02 `call-it` · Call it** · intro — · M→I · S3 · CC · `def-call`
  - Starter: `def barrier_report():` / `    print("Barrier's holding.")` / `    # add a second line here` /
    `# call barrier_report here`
  - CP1 [ND] "Add a second line inside the recipe, then call it." Checks: two lines, from one call.
  - Investigate: `barrier_report` with no `()` does nothing (one click).
  - Catches: the second `print` unindented, so it runs even without a call → "That line ran without the recipe:
    indent it under `def`"; an empty body → the IndentationError row ("A recipe needs at least one line inside
    it…").
  - AW: step-by-step (the indent means *belongs to the recipe*) · picture · shorter.
  - BQ (combining recipe + concat): "Make the report print the hours left from a box, with `str()`."
  - WA: empty body → crash, "indented block"; the second line unindented → CP1.
- **6A-03 `replace-pass` · Replace pass** · intro `node:Pass` · M · S4 · CC · `replace-pass` · rehearsal
  (`program-movement`)
  - Learn (campaign wording): "Each `def` line makes a recipe: a named set of steps. `pass` means do nothing. The
    scout moves with `scout.step("north")`."
  - Setup: `scout.step(direction)` (a recorder).
  - Starter: four recipes, `def step_north():` … `def step_west():`, each with `pass`, and one numbered comment
    above each (1:1 with the checkpoints): `# 1. Replace pass with a command that moves the scout north, like
    scout.step("north").`
  - CP1–CP4 [D] "Replace `pass` in `step_<dir>` with `scout.step("<dir>")`." Check: CALL (each recipe, when called,
    moves its own direction).
  - Catches: `scout.step(north)` → NameError rule 9 ("put it in quotes"); all four `"north"` → CALL
    ("`step_south()` moved the scout north. Use the direction in the recipe's name."); an unindented body →
    IndentationError.
  - Hints: P "Which word in the recipe's name says where to go?" T "`pass` is a blank recipe card: replace it with
    one indented line." S `scout.step("north")`.
  - AW: in Tor ("`pass` is a blank recipe card") · from the campaign (Lucky's box: "This shows up in Module 1 as
    `party.move("left")`") · step-by-step · picture (a map with four arrows).
  - PA: per recipe. Distractors: `scout.step(north)`, `scout.step("north")` inside `step_south`.
  - BQ (combining calls inside a recipe): "Add `step_twice_north()` that calls `step_north()` twice."
  - Twin: `turn_left()` / `turn_right()` with `scout.turn("left")`.
  - WA: unquoted → crash; all `"north"` → CP2, "north".
- **6A-04 `ingredients` · Ingredients** · intro — · P→R→M · S3 · CC · `param-use`
  - Learn: "Some recipes need an ingredient (parameter). The card says `hero_name`. When you call it, you hand over
    a real name (argument)."
  - Example: `def cheer(name):` / `    print(name + " is ready.")` / `cheer("Oogrish")` / `cheer("Gearshift")`.
    foreign: `cheer`, `name`.
  - Starter (two calls, C12): `def warn(hero_name):` / `    # print: <hero_name>, get inside!` /
    `warn("Lucky")       # should show: Lucky, get inside!` / `warn("Bomb Shell")  # should show: Bomb Shell, get inside!`
  - Predict (G3, from what you know): "`hero_name` is a box. In the first call, what's inside it?" (Lucky /
    hero_name / nothing)
  - CP1 [ND] "Finish `warn` so both calls show their own hero." Names: `hero_name`. Checks: PAR (`"Tester"`,
    `"Moth"`, which never collide with the task's calls); PAR-CONST with a call table.
  - CP2 [ND] "Add a third call for your own hero." Check: three calls; any text (lint e).
  - Catches:
    - `print("Lucky, get inside!")` typed → PAR-CONST ("`warn("Tester")` and `warn("Moth")` both printed
      `Lucky, get inside!`…").
    - `print("hero_name, get inside!")` → PAR ("printed the word *hero_name*: take the quotes off").
    - `print(name + …)` → rule 3 (`name` is from the example).
  - Hints: P "What did the call hand over?" T "Inside the recipe, the ingredient's name holds what was handed
    over." S `print(hero_name + ", get inside!")`.
  - Glossary: *parameter* (the ingredient's name on the card), *argument* (what you hand over).
  - AW: everyday (a Mad Libs card) · picture (the call table: parameter → value per call, open under "Show me
    more") · from what you know ("`hero_name` is a box filled at the call") · step-by-step · in Tor.
  - TR: static call table.
  - BQ (combining two parameters + concat): "Add a second ingredient, `hours`, and print
    `<hero>, get inside! <hours> hours left.`"
  - Twin: `def greet(guest):`.
  - WA: the line typed → CP1, "Tester"; `"hero_name"` quoted → CP1, "word"; `name` → crash, "example".
- **6A-05a `fill-the-ingredients` · Fill the ingredients** · intro — · M · S4 · **K** (contingent: first
  exposure under "Show me more", or after an assisted or failed 6A-04)
  - Starter: `def show_hit(base_damage, bonus):` / `    print(___ + ___)` / `show_hit(4, 3)  # should show: 7`
  - CP1 [D] "Fill each `___` with an ingredient's name." Check: PAR.
  - Proves explainer rule 1 (the `___` row).
  - WA: a `___` left → crash, "blank"; `print(4 + 3)` → CP1, PAR.
- **6A-05 `use-the-ingredients` · Use the ingredients** · intro — · M · S3 · CC · `param-use` · WT "Why the recipe
  can't know the numbers yet"
  - This is the worksheet's Part 3 cliff, reframed.
  - Learn: "Inside the recipe, use the ingredient names, never the numbers from one call. The numbers arrive when
    the recipe is called. Remember 1C: show your working with boxes, not the answer. Same here." (G2 R12)
  - Starter (two calls): `def show_hit(base_damage, bonus):` / `    # print the total hit` /
    `show_hit(4, 3)  # should show: 7` / `show_hit(8, 2)  # should show: 10`
  - CP1 [ND] "Finish `show_hit` so both calls show the right total." Checks: PAR with **(6, 5) → 11** and
    **(20, 1) → 21** (no collision with 7 or 10, lint b); PAR-CONST with a call table.
  - CP2 [ND] "Add a third call with your own numbers." Check: three calls.
  - Catches:

    | Slip (evidence) | Caught by |
    |---|---|
    | `print(4 + 3)` (A-06, A-07, B-02 test values) | PAR-CONST: "`show_hit(6, 5)` and `show_hit(20, 1)` both printed 7. A recipe gets its numbers when it is called: use `base_damage` and `bonus`." plus the call table |
    | `print(damage + bonus)` (A-01) | **PNM**: "This recipe's ingredients are `base_damage` and `bonus`. You wrote `damage`. Python matches names letter for letter." |
    | `print(7)` (A-08) | PAR-CONST |
    | `print(100 * 5)` (A-02, A-03, A-04 unrelated literals) | PAR-CONST |
    | `print(a + b)` (the hint's names) | rule 3: "`a` comes from Mar'tu's hint example. This recipe's ingredients are…" |
  - Hints: P "Which names are written inside the brackets on the `def` line?" T "If `def add(a, b):`, then `a + b`
    works for any call." (`add`, `a`, `b` go in `foreign_names`.) S `print(base_damage + bonus)`.
  - AW: step-by-step (a call table) · everyday (Mad Libs) · picture (ingredients arriving at the call) · from what
    you know (1C's "show your working") · in Tor.
  - TR: static call table.
  - PR: "Seat A explains why `4 + 3` inside the recipe breaks the second call."
  - PA: distractors `print(4 + 3)`, `print(damage + bonus)`, `print(7)` (G2 R19).
  - BQ (combining parameters + a comparison): "Also print whether the hit reaches Lucky's armor of 13."
  - Twin: `def show_heal(base_heal, extra):`.
  - WA: `print(4 + 3)` → CP1, "both printed 7"; `print(damage + bonus)` → crash, "damage"; `print(7)` → CP1;
    `print(a + b)` → crash, "a".
- **6A-06 `send-it-back` · Send it back** · intro `node:Return` · P→R→I→M · S3 · CC · `return-value`,
  `param-use` · point-at-it
  - Learn: "`print` says the answer out loud to the room. `return` writes it on a note and hands it back. Put the
    note in a box, or it's gone." (G1 everyday angle)
  - Example: `def triple(n):` / `    result = n * 3` / `    return result` / `print(triple(4))` → `12`. foreign:
    `triple`, `n`, `result`.
  - Starter: `def max_mana_for(affinity):` / `    total = affinity * 2` / `    # hand back total` /
    `# lucky_max = ...`
  - CP1 [D] "Hand back `total` with `return total`." Checks: RET (`max_mana_for(9) == 18`, `(12) == 24`);
    PAR-CONST.
  - CP2 [D] "Store `max_mana_for(13)` in `lucky_max`, then print `lucky_max`." Checks: STO (assigned from a call);
    `'26' in _lines()`.
  - **Investigate (G3 R4):** "Delete `return total`. Run. What does `lucky_max` hold?" → `None`, and the console's
    None notice fires. Then put it back.
  - CP3 [ND] (G4 R10; the lesson's capstone non-dictated checkpoint) "Write `max_fuel_for(cells)`. Gearshift gets
    5 fuel per cell." Names: `max_fuel_for`, `cells`. Checks: PAR (3 → 15, 7 → 35); RET; RNM; PNM; PAR-CONST;
    RET-PARAM.
  - Catches:
    - printing instead of returning → RET ("printed 18 but handed back `None`");
    - B-02's blank `return` → RET;
    - A-07's raw inputs → RET-PARAM;
    - A-06's `return 50` → PAR-CONST;
    - `return result` (the Example's name) → rule 3;
    - `return reslt` → fuzzy RNM.
  - Point-at-it: "Which box catches what the recipe hands back?"
  - TR: a static step table with the return arrow landing in `lucky_max` (A-03 and A-04 lost the return value).
    A wrong predict opens it.
  - Hints: CP3: P "How much fuel for one cell? For `cells` cells?" T `def double(n): return n * 2`. S
    `fuel = cells * 5` / `return fuel`.
  - AW: everyday (the note handed back) · picture (the return arrow) · step-by-step · from the campaign ("a recipe
    hands back a roll", described) · in Tor.
  - BQ (combining return + concat): "Print Lucky's status line with `max_mana_for(13)` inside it, using `str()`."
  - Twin: `def double_cost(price):`.
  - WA:
    - `print(total)` instead of `return` → CP1, "None";
    - `return affinity` → CP1, "as it came in";
    - `return 26` → CP1, "both gave back";
    - `lucky_max = 26` → CP2, "store";
    - CP3 `return 15` → CP3, "both";
    - CP3 `return cells * 2` → CP3, "5 fuel per cell".
- **6A-06b `be-the-ledger` · Be the ledger** · intro — · P→TT→R · S4 · CC · `trace-call` · **trace-table item
  type** · **moment** (traced on the board together)
  - The program (shown in the Learn pane as a code block, not run yet):
    ```python
    def ward_strength(lanterns, runes):
        light = lanterns * 10
        glow = runes * 5
        return light + glow

    barrier = ward_strength(3, 4) + 10
    print(barrier)
    ```
    (Verified: it prints `60`.)
  - The ledger has one row per box, checked as typed: `lanterns` (3), `runes` (4), `light` (30), `glow` (20),
    *handed back* (50), `barrier` (60), *printed* (60).
  - Targeted messages:
    - handed back = 15 → "15 is 10 + 5, the numbers written in the recipe. On this line the boxes hold 30 and 20.
      Add what is *in* the boxes." (A-03, A-04)
    - handed back = 7 → "7 is 3 + 4, the ingredients as they came in. The recipe hands back `light + glow`." (A-07)
    - `barrier` = 40 or 30 → "The `barrier` line starts from what the recipe handed back (50), not from `light` or
      `glow`."
    - printed = 55, 45 or any sum of earlier rows → "`print(barrier)` shows only what's in `barrier`. It doesn't
      add up the earlier lines."
  - Then Run and compare.
  - **Prototype representation** until the item type exists: an exercise whose starter holds ledger boxes
    `lanterns_row = 0` … `printed_row = 0`. Each checkpoint checks one row with the messages above. The program
    is the Example, run after the last row passes.
  - AW: picture (the return arrow landing in `barrier`) · step-by-step · everyday (a shop till: the receipt shows
    what is in each line, not the price list).
  - Twin after any reveal: `ward_strength(4, 1) + 10` (→ 40 + 5 = 45, then 55; new numbers per seat).
  - The same shape returns in Quiz 6A #3 and Readiness item 4b.
  - WA: handed_back 15 → row 5, "10 + 5"; 7 → row 5, "came in"; barrier 40 → row 6; printed 55 → row 7.
- **6A-07 `return-the-right-box` · Return the right box** · intro — · D→M · S4 · CC · `return-right-name`,
  `return-value` · WT "Whose kitchen is `result` in?"
  - Starter:
    - `def armor_total(base, bonus):` / `    total = base + bonus` / `    return result` (copied from 6A-06's
      Example);
    - `def shield_total(base, bonus):` / `    total = base + bonus` (no `return`);
    - `print("Lucky: " + str(armor_total(10, 3)))` / `print("Shield: " + str(shield_total(2, 1)))`.
  - CP1 [D] "Fix `armor_total` so it hands back the box it computed." Checks: rule 3 ("`result` looks like
    `result` from the example. This recipe's box is `total`."); RET; PAR.
  - CP2 [ND] "`Shield:` shows `None`. Make `shield_total` hand back its total." Checks: RET; `Shield: 3`. Message:
    "`shield_total(2, 1)` handed back `None`: it has no `return` line."
  - WT: "Whose kitchen is `result` in?" `result` lives only inside `triple`'s kitchen (a scope preview; the full
    version is pool item 6B-09).
  - AW: everyday (handing back the wrong bowl) · picture (two kitchens) · step-by-step · shorter.
  - BQ (combining return + comparison): "Print whether Lucky's armor total beats 12."
  - WA: `return reslt` → crash, "reslt"; `return base` → CP1, "as it came in"; `print(total)` in `shield_total` →
    CP2, "None".
- **6A-08 `store-then-pass` · Store, then pass it on** · intro `attr:capitalize` · P→I→M · S3 · CC ·
  `store-then-pass`, `chain-methods` · rehearsal (`program-dialogue-prompt`)
  - Learn: "`get_greeting()` hands back a line. Look at how it tidies the line: `.lower()` makes every letter
    small, then `.capitalize()` makes the first letter big. `present_greeting()` must store that line in a
    variable, then pass the variable on."
  - Setup: `show_on_ley_board(text)` (a recorder).
  - Starter (campaign-shaped; comments 1:1 with the checkpoints):
    ```python
    # 1. Change the words inside the quotes to a greeting Mar'tu gives Lucky.
    def get_greeting():
        line = "WELCOME TO THE CABIN."
        line = line.lower()
        line = line.capitalize()
        return line


    # 2. Finish present_greeting(): store the result of get_greeting() in a variable.
    # 3. Pass that variable to show_on_ley_board().
    def present_greeting():
        pass
    ```
  - **Predict (T2):** "What does `get_greeting()` hand back?" (`WELCOME TO THE CABIN.` / `welcome to the cabin.` /
    `Welcome to the cabin.` / `Welcome To The Cabin.`) → the 3rd (verified).
  - CP1 [ND] "Change the words inside the quotes to a greeting Mar'tu gives Lucky." Check: TEXT that differs from
    the starter; any text (lint e).
  - CP2 [D] "Finish `present_greeting()`: store the result of `get_greeting()` in a variable." Check: STO.
  - CP3 [D] "Pass that variable to `show_on_ley_board()`." Checks:
    - CALL: one call, with the tidied greeting;
    - CMB: the check redefines `get_greeting` to hand back another line, calls `present_greeting()`, and the board
      must show it.
  - Catches:
    - `show_on_ley_board("Welcome to the cabin.")` typed → CMB;
    - `show_on_ley_board(get_greeting)` with no `()` → CALL ("the board showed `<function …>`: add `()` to call
      it");
    - `show_on_ley_board(get_greeting())` → STO ("store it in a variable first, as the campaign asks").
  - Subgoal labels: *Call the helper → Store what it hands back → Pass it on.*
  - Hints: P "Which recipe hands back the line?" T "`note = get_note()` catches what `get_note` hands back." S
    `greeting = get_greeting()` / `show_on_ley_board(greeting)`.
  - AW: from the campaign (Module 1 "stores the line, then passes it on", described) · step-by-step (the subgoal
    labels) · picture (a note passed from one recipe to another) · everyday (collect a parcel, then hand it on).
  - PA: blocks `greeting = get_greeting()` / `show_on_ley_board(greeting)`. Distractors:
    `show_on_ley_board(get_greeting)`, `get_greeting = greeting`.
  - BQ (combining two helpers + order): "Add `get_farewell()` with its own tidied line, and show both lines in
    order."
  - Twin: `get_warning()` / `present_warning()`.
  - WA: the typed line → CP3, "another line"; no `()` → CP3, "function"; no store → CP2, "variable".
- **6A-09 `return-a-comparison` · Return a comparison** · intro — · P→I→M · S2 · CC · `return-comparison`,
  `boundary` · rehearsal (`skill-checks`)
  - Example: `def spot_check(roll):` / `    target = 14` / an if/else that returns `True` or `False`; then its
    one-line form `return roll >= target`. foreign: `spot_check`, `target`.
  - Starter (numbered comments): `def strength_check(roll):` / `    # Bomb Shell pries the trap door.` /
    `    # 1. Set needed to how hard this is, a number from 2 to 20.` / `    needed = 0` /
    `    # 2. Replace return False with: return roll >= needed` / `    return False`
  - CP1 [D] "Set `needed` to how hard prying the door should be, from 2 to 20." Check: an int from 2 to 20.
  - CP2 [D] "Replace `return False` with `return roll >= needed`." Checks: BND (`needed` is read from the code;
    rolls `needed - 1`, `needed`, `needed + 1`, 1, 20); RET (a bool). The if/else form passes too.
  - Catches: `return True` → BND; `>` → BND ("exactly"); `print(roll >= needed)` → RET (`None`).
  - Hints: P "What should a roll of exactly `needed` give?" T the two forms of the Example. S the line.
  - AW: from the campaign (the skill-checks shape, described) · step-by-step (the two forms are equal) · picture ·
    shorter.
  - PA: yes.
  - BQ (combining):
    - "Write `dexterity_check(roll)` with its own `needed`, and print both checks for a roll of 12."
    - Seal version (prerequisite card 2-A2): "Seal it with three `assert` lines at the boundary."
  - WA: `return True` → CP2; `return roll > needed` → CP2, "exactly"; `needed = 25` → CP1.
- **6A-10 `roll-recipe` · A rolling recipe** · intro — · M · S4 · CC · `randint-param` · rehearsal
  (`perform_roll`)
  - Starter: `import random` / `def roll_die(die_size):` / `    # 1. Replace return 1 with a random whole number
    from 1 to die_size.` / `    return 1`
  - CP1 [ND] "Replace `return 1` with a random whole number from 1 to `die_size`." Check: RND (`roll_die(6)` calls
    `randint(1, 6)`; `roll_die(20)` calls `randint(1, 20)`).
  - Catches: `random.randint(1, 20)` (A-06 test values) → RND ("`roll_die(6)` rolled `randint(1, 20)`. Use the
    parameter."); a missing `import` → rule 6b; `randint(0, die_size)` → RND.
  - Hints: P "Which ingredient says how many faces?" T `random.randint(1, 6)` from 2B-07. S
    `return random.randint(1, die_size)`.
  - AW: from the campaign (described) · step-by-step · picture (a die with `die_size` faces).
  - BQ (combining recipes): "Write `attack_roll(die_size, bonus)`, which hands back `roll_die(die_size) + bonus`."
  - WA: `randint(1, 20)` → CP1; `randint(1, 6)` → CP1.
- **6A-11 `broken-spell-6A` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - a missing colon after `def`;
    - `def max_mana = 18` (the DEF row);
    - a call made before its `def` (NameError: order matters);
    - a returned wrong name (rule 3).
- **6A-S `solo-6A` · Show Mar'tu** · SOLO make-twin · S3 · CC
  - By seat: A `heal(hero_name, amount)` prints `<hero> heals <amount>.`; B `rest_line(hero_name, hours)` prints
    `<hero> rests <hours> hours.`
  - Starter: the `def` line, `# print the line`, and two calls.
  - CP1 [ND] Check: PAR. CP2 [ND] "Add a call for your own hero."
  - The first Recipes I solo informs placement (run-kit, G3 R10).

### Quiz 6A [CC, 8 questions] (u03a)

Types: 5 predict · 1 mc · 1 parsons · 1 fill.
1. **predict.** A program that only defines `say_steady()` and never calls it → *(nothing)*.
2. **predict.** `def max_mana_for(affinity): print(affinity * 2)`, then `lucky_max = max_mana_for(13)` and
   `print(lucky_max)` → `26` then `None`.
3. **predict (the ledger shape).** `ward_strength(1, 6) + 10` → `50`. Choices: 25 (the constants), 17 (the raw
   inputs), 50, 90 (adding the rows 10 + 30 + 50). `why_wrong` reuses the 6A-06b messages.
4. **predict.** `latch_check` with `needed = 11`, called on 10, 11 and 12 → `False` `True` `True`.
5. **mc.** "In `warn("Lucky")`, which is the argument?"
6. **parsons.** Store-then-pass. Distractor: `show_on_ley_board(get_greeting)`.
7. **fill.** `return roll ___ needed` → `>=`.
8. **predict.** `y = double(4)` / `print(y + 1)` → `9`.

### Extra practice 3X "Recipe twins" [pool, 9 min] (u03b)

Each twin is [ND]. These are where G1's deferred time goes (G1 R19).
- **6A-T1 `cheer-on`:** `cheer_on(hero_name, cheer)` prints `<hero>: <cheer>` [PAR].
- **6A-T2 `double-cost`:** `double_cost(price)` returns twice the price [RET, PAR-CONST].
- **6A-T3 `glug-left`:** `glug_left(sips_now, sips_drunk)` returns what's left; store it, then print it [RET,
  STO].

### "Before the cabin door" [Route M1 only, 10 min] (u03b)

**Format:** `cabin-door` (a `lesson`, `optional=True`, shown when the class route is M1; `support="none"` with the
explainer on) plus `cabin-door-questions` (a `quiz`).

Mar'tu: "Before we go through the cabin door, show me four things."

| # | Item | Readiness analog | Check |
|---|---|---|---|
| C1 | Replace `pass` in `def step_west():` with a scout step | item 2 | CALL |
| C2 | Finish `present_warning()`: store `get_warning()`, then pass it to `show_on_ley_board()` | item 3 | STO, CALL |
| Q1 | Trace a three-branch `elif` on `choice == "option 2"`; which line runs? | item 5a | predict |
| Q2 | Mend `elif choice == option 3:` | item 5b | bug |
| Q3 | Predict `"WHO GOES THERE?".lower().capitalize()` → `Who goes there?` | chain-methods | predict |

The teacher sees per-item results. The signal reads "ready for Module 1" when C1 and C2 pass typed and at least 2
of 3 questions are right. It is a signal, never a lock.

### Quick Check Recipes I [O, ~12 min] (u03b: `qc-r1-a`, `qc-r1-b`, plus question forms)

Framing (G4 R25): "Nobody in this cabin has written a recipe yet. This shows Mar'tu where to start."

| # | Form A item | Type | Skills | Fails on (evidence) |
|---|---|---|---|---|
| C1 | Goal only: "Write `armor_total(base_armor, bonus_armor)` that hands back the total." An Example using `result` is on screen. | code | `param-use`, `return-value`, `return-right-name` | `return result` → RNM (A-01); `base + bonus` → PNM (A-01); `return 13` → PAR-CONST (A-06); `print` instead of `return` → RET (B-02) |
| C2 | Replace `pass` in `step_west`; then finish `present_warning()` (2 CPs) | code | `replace-pass`, `def-call`, `store-then-pass` | `scout.step(west)` → crash; a typed line → CMB; no store → STO |
| C3 | `latch_check(roll)` with your own `needed`, returning a comparison | code | `return-comparison`, `boundary` | `>` → BND; `return True` → BND |
| C4 | `roll_die(die_size)` | code | `randint-param` | `randint(1, 6)` → RND (A-06 test values) |
| Q1 | "Which line makes a box?" `def hero = "Lucky"` / `hero = "Lucky"` / `def hero():` | mc | `=` versus `def` | A-02 |
| Q2 | A recipe with no `return`, printed → `None` | predict | `return-value` | `26` |
| Q3 | The ledger shape with new numbers | predict | `trace-call` | 15-type and 7-type answers |
| Q4 | `.lower().capitalize()` on a shouted line | predict | `chain-methods` | `WHO GOES THERE?` |

Form B uses `shield_total(base_shield, bonus_shield)`, `step_east`, `get_farewell`, `dodge_check` and
`roll_die`'s d12 test.

### Cheatsheet 3 "Recipes"

- `def name():` plus an indent; defining isn't calling; `name()` calls it.
- `pass`.
- Parameter (on the card) versus argument (handed over).
- `return value`; `x = f()` catches it; no `return` → `None`.
- `return roll >= needed`; `random.randint(1, die_size)`.
- Store, then pass.
- `.lower()` then `.capitalize()`.

---

## Unit 4 · Lists: "The Chalk Wall" (`lists`, files u04a–u04b)

**Mar'tu's framing.** "Seven numbers on my wall. I could give each one its own box. I could also lose my mind. A
list keeps them together, in order, yes?"

**RPG tie-in.** The chalk wall `[48, 48, 47, 46, 44, 41, 37]` is the unit's data. Students find the shrinking for
themselves in Unit 6. Other lists: the hero roster as name-and-mana pairs, and Oogrish's training log.

**Learning objectives. Student can…**
1. Create a list with `[ ]` and commas.
2. Read an item by zero-based index, including negative indexes, and recognize an IndexError.
3. Change an item by index.
4. Grow a list with `.append()`, and join two lists with `+`.
5. Use `len()`, and know the last index is `len - 1`. **Write a small recipe that takes a list** (`newest_mark`).
6. Read a nested list, `roster[3][1]` (the stepping stone to nested dicts).
7. Make `range(...)` (the stop value is excluded), slice with `[a:b]` and `[-3:]`, and use `sorted()` versus
   `.sort()` (which returns `None`).

Optional or pool: `.count`, `.insert`, `.pop`, `.remove`, `in`, `max` / `min` / `sum`, tuples, `zip()`.

**Campaign links.**
- Obj 1–2, 6 → `party.members` is a list, and `caster["abilities"]["magical_affinity"]` is a nested read.
- Obj 7 → `.sort()` returning `None` echoes Unit 3's missing `return`.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 3A "Many Values, One Name" (with 3A-remembers) | CC: 3A-R, 3A-02, 3A-03, 3A-06, 3A-S; the rest SC | 32 | u04a |
| 2 | Lesson 3B "Reading the Wall Closely" (with 3B-remembers) | SC | 13 | u04a |
| 3 | Quiz 3 | SC | 6 | u04a |
| 4 | 4X Extra practice (3B-04, 3B-05) | pool | 6 | u04b |
| 5 | Project 3P1 "Oogrish's Training Log" | pool | 25 | u04b |
| 6 | Lesson 3C "More List Tools" | O | 15 | u04b |
| 7 | Quiz 3B | O | 8 | u04b |
| 8 | Articles 3-A1 Tuples, 3-A2 `zip()` | O | 10 + 10 | u04b |
| 9 | Project 3P2 "The Basement Inventory" | O | 35 | u04b |
| 10 | Quick Check 3 (forms A, B) | O | 10 | u04b |
| 11 | Cheatsheet: Lists | ref | — | u04b |

### Lesson 3A "Many Values, One Name" [32 min] (u04a)

*Mar'tu remembers… (`3a-remembers`)*
1. Predict `double(9)` with `def double(n): return n * 2`. (Unit 3, the def/return item)
2. Trace `mana = 18` / `mana = mana - 5`. (1C)

- **3A-01 `how-would-you-store-it` · How would you store it?** · intro — · PF · *starter passes* · SC
  - Starter: `hour_1 = 48` is pre-typed (G1 R29).
  - "Store the seven gaps from my wall so you can ask about them later." Students try for up to 3 minutes.
  - Mar'tu then sets their attempt beside a list.
  - Skipped on frustration signals. CP1: run any attempt.
- **3A-02 `make-the-wall` · Make the wall** · intro `node:List` · M · S3 · CC · `list-make`
  - Example: `party_colors = ["gold", "fire orange"]`. foreign: `party_colors`.
  - Starter: `chalk_wall = []  # put the seven gaps in, in order`. The Learn pane shows the chalk-wall picture.
  - CP1 [ND] "Make `chalk_wall` hold the seven gaps, in order." Checks: the list equals the wall; NAME.
  - Catches:
    - `[48 48 47 …]` → "Perhaps you forgot a comma?", and the comma row extended to `[ ]` ("Inside a list, items
      are separated by commas");
    - quoted numbers → "These are text. Gaps are numbers: no quotes."
  - Hints: P "What goes between two items?" T the Example. S the full list.
  - AW: everyday (a shelf of jars) · picture (the wall with positions) · in Tor · shorter.
  - BQ (combining list + concat): `print("Gaps: " + str(chalk_wall))`.
  - WA: no commas → crash; quoted numbers → CP1, "numbers".
- **3A-03 `first-is-zero` · The first is zero** (absorbs 3A-04 `count-from-the-end`) · intro `node:Subscript`
  `op:USub` · P→R→I→M · S4 · CC · `list-index`
  - Predict `chalk_wall[1]` and `chalk_wall[6]`, then run `chalk_wall[7]` and read the IndexError.
  - CP1 [D] "Print the oldest gap using a position." Checks: `_uses('node:Subscript')`; CMB (another wall).
  - CP2 `count-from-the-end` [D] "Print the newest gap with `[-1]`, then the one before it with `[-2]`." Check: CMB.
  - Hints: P "Positions start at 0." T `colors[0]` is the first color. S `print(chalk_wall[0])`.
  - AW: picture (jars numbered from 0) · everyday (floors that start at 0) · step-by-step · in Tor.
  - TR: static table.
  - BQ (combining index + subtraction): "Print how much the newest gap shrank from the one before."
  - WA: `print(48)` → CP1, CMB; `chalk_wall[1]` → CP1.
- **3A-05 `new-chalk-mark` · A new chalk mark** (absorbs 3A-08 `join-two-walls`) · intro `attr:append` ·
  P→R→I→M · S4 · SC · `list-append-len`
  - CP1 [ND] "Append your own guess for the next gap: a number below 37." Checks: 8 items; the last is an int
    below 37. Any guess passes (lint e).
  - Investigate: `chalk_wall + [33]` versus `chalk_wall + 33` (TypeError row: "`+` joins two lists").
  - CP2 `join-two-walls` [D] "Join `old_marks` and `new_marks` into `wall` with `+`." Check: CMB (other marks).
    This fixes the v1 OUT-only check.
  - DF: 33.
  - AW: picture (a jar added at the end) · step-by-step · everyday.
  - BQ (combining append + index + arithmetic): "Append two more guesses, each 4 less than the newest:
    `chalk_wall.append(chalk_wall[-1] - 4)`."
  - WA: `.append("33")` → CP1, "number"; `chalk_wall + 33` → crash; a typed `wall` list → CP2, CMB.
- **3A-06 `how-long` · How long is the wall?** (recipe-shaped, D11) · intro `call:len` · P→I→M · S2 · CC ·
  `list-append-len`, `param-use`, `return-value`
  - Learn: "`len(wall)` counts the items. The last position is `len(wall) - 1`, because positions start at 0."
  - Starter: `def newest_mark(wall):` / `    # 1. Hand back the last item, using len(wall).` / `    return 0` /
    `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` / `print(len(chalk_wall))` /
    `print(newest_mark(chalk_wall))  # should show: 37`
  - CP1 [ND] "Make `newest_mark(wall)` hand back the last item of any wall, using `len`." Checks: PAR (`[9, 8, 7]`
    → 7, `[5]` → 5); `_uses('call:len')`; RET. This fixes the v1 OUT-only check.
  - Catches:
    - `return 37` → PAR-CONST;
    - `return wall[len(wall)]` → IndexError;
    - `return chalk_wall[len(chalk_wall) - 1]` → PAR ("Use the ingredient `wall`, not `chalk_wall`.").
  - WT: why the last index is the length minus one.
  - AW: picture · step-by-step · everyday (7 jars; the last is jar 6) · callback to Unit 3.
  - BQ (combining two recipes): "Write `oldest_mark(wall)` too, and print the shrink between oldest and newest."
  - WA: `return 37` → CP1; `return wall[len(wall)]` → crash; `chalk_wall` used inside → CP1, "wall".
- **3A-07 `fix-a-mark` · Fix a mark** · intro — · M · S4 · SC
  - The starter wall has `74` where `47` belongs (Lucky's handwriting).
  - CP1 [D] "Fix it by position. Don't retype the list." Checks: the wall is right; an `Assign` to a `Subscript`.
  - WA: retyping the list → CP1, "position".
- **3A-09 `lists-inside-lists` · Lists inside lists** · intro — · P→I→M · S4 · SC · `list-nested`
  - Code: `roster = [["Oogrish", 18], ["Gearshift", 20], ["Bomb Shell", 24], ["Lucky", 26]]`. Predict
    `roster[3][1]`.
  - CP1 [D] "Print Bomb Shell's name." CP2 [ND] "Print Oogrish's mana." Checks: CMB.
  - TR: boxes in boxes (static).
  - AW: picture (a shelf of small shelves) · step-by-step ("outer number first, then inner") · in Tor ("a box of
    boxes", which prepares nested dicts).
  - BQ (combining nested reads + addition): "Print the party's total mana from `roster`."
  - WA: `roster[2]` alone → CP1; `roster[1][2]` → crash.
- **3A-10 `broken-spell-3A` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - `chalk_wall[7]`;
    - `chalk_wall(0)` (new row: "'list' object is not callable" → "Read a list with square brackets:
      `chalk_wall[0]`");
    - `[48 48]`.
- **3A-S `solo-3A`** · SOLO, one bug · CC
  - By seat: A `print(chalk_wall[7])` for the newest; B `chalk_wall.append("33")`.
  - CP1 [ND].

### Lesson 3B "Reading the Wall Closely" [SC, 13 min] (u04a)

*Mar'tu remembers… (`3b-remembers`)*
1. Predict `"█" * 0 + "!"`. (1C)

- **3B-01 `range-of-marks` · Ranges** · intro `call:range` `call:list` · P→I→M · S4 · SC · `range-slice-sort`
  - Predict `list(range(5))` and `list(range(1, 7))`. A d6's faces are `range(1, 7)`, but you roll them with
    `randint(1, 6)`.
  - CP1 [D] "Make `d8_faces` with `range`." Checks: the list equals `[1 … 8]` and `_uses('call:range')`. A typed
    list gets "Use `range` to make it."
  - AW: picture (a ruler: the stop mark isn't included) · contrast with `randint` (2B-07).
  - WA: a typed list → CP1, "range"; `range(1, 8)` → CP1.
- **3B-02 `slice-the-wall` · Slice the wall** · intro `node:Slice` · P→M · S4 · SC
  - CP1 [ND] "Make `last_three`: the three newest gaps." Check: CMB (another wall).
  - CP2 [D] `first_two = chalk_wall[0:2]`. Check: CMB.
  - WT: "A slice is a new list."
  - WA: `[44, 41, 37]` typed → CP1, CMB; `[-3:-1]` → CP1.
- **3B-03 `sorted-or-sort` · `sorted` or `.sort`** · intro `call:sorted` `attr:sort` · P→I→M · S4 · SC
  - Investigate: `result = chalk_wall.sort()`, then `print(result)` → `None`. "None means nothing handed back,
    like a recipe with no `return`."
  - CP1 [D] "Make `shortest_first` with `sorted()`, leaving `chalk_wall` unchanged." Checks: both values.
  - WA: `shortest_first = chalk_wall.sort()` → CP1, "None".
- **3B-S `solo-3B`** · SOLO, one bug
  - By seat: A has a slice off by one; B has `x = wall.sort()` used as a list.
  - CP1 [ND].

### Quiz 3 [SC, 6 questions] (u04a)

1. **predict.** `chalk_wall[-1]` and `len(chalk_wall)` → `37`, `7`.
2. **predict.** `roster[2][0]` → `Bomb Shell`.
3. **bug.** `chalk_wall[7]` should read the newest gap.
4. **predict.** `chalk_wall[-3:]` → `[44, 41, 37]`.
5. **mc.** What `x = wall.sort()` holds.
6. **predict (def/return item).** `def first_mark(wall): return wall[0]`, then `print(first_mark([9, 8]))` → `9`.

### Extra practice 4X [pool] and the optional items (u04b)

- **3B-04 `how-many-times`** (pool) · intro `attr:count`. Count the 48s. CMB (another wall), which fixes OUT-only.
- **3B-05 `broken-spell-3B`** (pool). `chalk_wall.sort()[0]` (TypeError on `None`); a slice one off.
- **3P1 "Oogrish's Training Log"** (pool project, 25 min). Oogrish logs each yard drill and its score. Tasks:
  1. `log` as a list of `[drill, score]` pairs (any drills).
  2. Append a drill.
  3. Fix a score by nested index.
  4. **`last_score(log)` returns the newest score** (recipe-shaped; PAR with fresh logs).
  5. Print the last drill and its score with `[-1]` and `str()`.
  6. `len`.

  Checks: CMB reruns. Side quest: did the last score beat the first (`if`)?
- **3C "More List Tools"** (O): 3C-01 `insert-and-pop` (`attr:insert` `attr:pop`), 3C-02 `remove-and-in`
  (`attr:remove` `op:In`), 3C-03 `biggest-and-smallest` (`call:max` `call:min` `call:sum`).
- **Quiz 3B** (O, 8 questions): `range`, `sort` → `None`, slices.
- **3-A1 Tuples** (O, `node:Tuple`) and **3-A2 `zip()`** (O, `call:zip`), one try-it each.
- **3P2 "The Basement Inventory"** (O, 35 min): the resonance-array parts in parallel lists; insert, pop, sort and
  slice the top 3, count, `zip`. Prerequisites: 3C, 3-A2.

### Quick Check 3 [O, ~10 min] (u04b: `qc3-a`, `qc3-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| Q1 | `chalk_wall[-2]`, `len(chalk_wall)`, `roster[1][0]` | predict | `list-index`, `list-nested` | off-by-one; `[1][0]` read as Lucky |
| C1 | Make `marks` holding 46, 44 and 41, append a guess, then print the last item **through the list** | code | `list-make`, `list-append-len`, `list-index` | `print(33)` → CMB; quoted numbers |
| Q2 | What does `x = wall.sort()` hold? | mc | `range-slice-sort` | "the sorted list" |
| C2 | `last_three` from any wall | code | `range-slice-sort` | a typed list → CMB |

Form B uses `velocite_used` and `drills`.

### Cheatsheet: Lists

`[48, 47]` · `wall[0]` first · `wall[-1]` last · `wall[i] = x` · `.append(x)` · `a + b` · `len(wall)` · the last
index is `len - 1` · `roster[3][1]` · `range(1, 7)` stops before 7 · `wall[-3:]` · `sorted(wall)` versus
`wall.sort()` → `None` · an IndexError means "no such position".

---

## Unit 5 · Dictionaries: "Stat Sheets and Spell Books" (`dictionaries`, files u05a–u05c) — D1

**Mar'tu's framing.** "A list remembers order. It does not remember *meaning*. Which number is Lucky's armor?
Which is his mana? A dictionary keeps a label on every value. At the Institute, every student had a record like
this. Mine said 'talks too little'."

**RPG tie-in.** Hero stat sheets use the real values from the party table. Abilities nest inside each sheet. The
spell book is a dict of spells, and the roster is a list of sheets. This is the campaign's data model, rehearsed
with near-transfer names.

**Learning objectives. Student can…**
1. Write a dict literal with quoted string keys, `:` and commas. Explain why keys have quotes when box names don't
   (the reconciliation card).
2. Read a value by key, and fix a KeyError caused by spelling, case or nesting.
3. Change a value and add a key by assignment, including `hero["mana"] = hero["mana"] - cost`.
4. Test membership with `in` / `not in` (on keys).
5. Use a key stored in a variable: `book[spell_name]` versus `book["spell_name"]`.
6. Read and write nested values: `hero["abilities"]["magical_affinity"]`.
7. Read from a list of dicts: `roster[2]["name"]`.
8. Build a dict from variables and store it by key: `spell_book[spell_name] = spell`.
9. Combine nested reads with `if/elif/else`: get it, compare, act.

**Campaign links.**
- Obj 1, 8 → `spell-book`.
- Obj 2–3 → `mana-bars` and `hold-the-barrier` (the mana subtraction).
- Obj 4 → `if spell_name not in caster["spell_book"]:`.
- Obj 6 → `caster["abilities"]["magical_affinity"]`.
- Obj 7 → `party.members`.
- Obj 9 → the body of `hold-the-barrier`.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 4A "Stat Sheets" (with 4A-remembers) | CC (4A-01, 4A-08 SC) | 32 | u05a |
| 2 | Article 4-A1 "Why Does This Work? Keys and `.get()`" | O | 8 | u05a |
| 3 | Lesson 4B "Sheets Inside Sheets" (with 4B-remembers) | CC (4B-02, 4B-06 SC) | 30 | u05b |
| 4 | Quiz 4 | SC | 8 | u05b |
| 5 | Project 4P "Mar'tu's Ledger of Heroes" | SC | 20 | u05b |
| 6 | 5X Extra practice (4A-T, 4B-T) | pool | 7 | u05b |
| 7 | Quick Check 4 (forms A, B) | O | 12 | u05c |
| 8 | Cheatsheet: Dictionaries | ref | — | u05c |

### Lesson 4A "Stat Sheets" [32 min] (u05a)

*Mar'tu remembers… (`4a-remembers`)*
1. `roster[1][1]` from the nested list. (Unit 4)
2. Predict `max_mana_for(9)`. (Unit 3, def/return)

- **4A-01 `which-number-is-which` · Which number is which?** · intro — · P (hook) · SC · **protected story beat**
  - Code: `lucky = ["Lucky", 13, 26, 3]`. "Print Lucky's armor bonus. Which index is it?" Students guess, then
    check.
  - CP1: prints 3.
  - Mar'tu: "You had to remember that position 3 means armor. Python can remember for you."
- **4A-02 `make-a-sheet` · Make a sheet** · intro `node:Dict` · M · S3 · CC · `dict-make`
  - **Reconciliation card (G1 R6):** "Wait, quotes on names? A **box's name** (a variable) never has quotes:
    `mana = 26`. A **label inside a dictionary** (a key) is a piece of text, so it does: `{"mana": 26}`. Quotes mean
    these exact letters. No quotes means look inside the box with this label." Predict: `hero = {"mana": 26}`,
    then `print(hero["mana"])` versus `print(hero[mana])`.
  - Example: `bomb_shell = {"name": "Bomb Shell", "dexterity": 6}`. foreign: `bomb_shell`, `dexterity`.
  - Starter: `gearshift = {` / `    # "name", "magical_affinity", "max_mana", "armor_bonus"` / `}`
  - CP1 [ND] "Make `gearshift` with the keys `"name"`, `"magical_affinity"`, `"max_mana"` and `"armor_bonus"`."
    Check: KEY.
  - CP2 [ND] "Fill in his values from the sheet." Checks: 10, 20, 3; NUM, TEXT.
  - Catches:
    - `{name: "Gearshift"}` → NameError, rule 9 ("keys are text, so they need quotes");
    - `{"name" = …}` → a new row: "Use `:` between a key and its value";
    - a missing comma → the dict-comma row (int value: reported on that line; string value: reported on the next
      line; both verified);
    - `"Max_Mana"` → KEY.
  - AW: everyday (a stat sheet with labeled lines) · picture (labeled boxes inside one big box) · from the campaign
    (the `spell` dict, described) · in Tor · the reconciliation card.
  - PA: yes.
  - BQ (combining dict + recipe): "Set `"max_mana"` with `max_mana_for(10)` inside the dict." (`max_mana_for` is
    defined in the starter's side-quest block.)
  - WA: an unquoted key → crash; `=` for `:` → crash; a missing comma after `"Gearshift"` → crash on the next
    line; a missing comma after `20` → crash on that line; `"Max_Mana"` → CP1, KEY.
- **4A-03 `read-by-key` · Read by key** · intro — · P→R→M · S4 · CC · `dict-read`
  - CP1 [ND] "Print `Gearshift: 20 mana`, built from the dict." Checks: OUT diff; CMB (changed sheet values).
  - Spaced practice of `+ str()`.
  - WA: the line typed → CP1, CMB.
- **4A-04 `key-errors` · Key errors** · intro — · D · CC · `dict-read`
  - Mend `gearshift["Max_Mana"]` and `gearshift["max mana"]` (the KeyError row). One checkpoint each.
- **4A-05 `write-by-key` · Write by key** · intro — · P→R→M · S4 · CC · `dict-write` · point-at-it
  - CP1 [D] "Gearshift casts Fire Bolt: `gearshift["mana"] = gearshift["mana"] - fire_bolt_cost`." Check: CMB
    (cost 4).
  - CP2 [D] "Add a new key: `gearshift["fuel"] = "starlode"`." Check: KEY.
  - Point-at-it: "Which part reads the old mana?"
  - Catches: subtracting a typed 6 → CMB.
  - TR. From the campaign: `caster["mana"] = caster["mana"] - spell["mana_cost"]`.
  - BQ (combining write + bar): "Print Gearshift's mana bar after the cast (blocks pre-typed)."
- **4A-06 `is-it-in` · Is it in the book?** · intro `op:In` `op:NotIn` · P→I→M · S4 · CC · `dict-in`
  - Code: `spell_book = {"Glow": 2, "Warm Hands": 3}`. Predict `"Glow" in spell_book` → True and
    `2 in spell_book` → False (`in` looks at keys).
  - CP1 [ND] "If `"Fire Bolt"` is not in `spell_book`, print a message." Check: CMB (Fire Bolt added → no message).
  - WT: "`in` checks keys."
- **4A-07 `key-from-a-box` · A key from a box** · intro — · P→I→M · S4 · CC · `dict-key-from-variable`
  - Code: `spell_name = "Warm Hands"`. Predict `spell_book[spell_name]` versus `spell_book["spell_name"]` (KeyError:
    `'spell_name'`).
  - **Investigate: the 6-card quotes sort (G2 R11).** One click per card: `mana = 26`, `{"mana": 26}`,
    `hero["mana"]`, `hero[mana]`, `print("mana")`, `print(mana)` each go into "these exact letters" or "look
    inside the box".
  - CP1 [ND] "Print the cost of whichever spell `spell_name` names." Check: CMB (`spell_name = "Glow"`).
  - Catches: A-02's name-in-quotes habit, in a new form.
  - AW: step-by-step (what Python looks up in each case) · the quotes sentence · picture.
  - PA: yes.
- **4A-08 `broken-spell-4A` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each: `{"name" = "Lucky"}`, `lucky[name]`, `lucky["Mana"]`, and `lucky.mana` (the
    AttributeError row).
- **4A-S `solo-4A`** · SOLO, one bug · CC
  - By seat: A `oogrish["Mana"]`; B `oogrish.mana`.
  - CP1 [ND].

### Article 4-A1 "Why Does This Work? Keys and `.get()`" [O] (u05a)

- Keys are unique, so a second assignment overwrites.
- `.get("glug", 0)` gives a default instead of a KeyError. Intro `attr:get`. The example builds its own `hero`
  (the setup gotcha, §2.12 rule 3).
- Why `in` is fast.

### Lesson 4B "Sheets Inside Sheets" [30 min] (u05b)

*Mar'tu remembers… (`4b-remembers`)*
1. A nested list read. (Unit 4)
2. Predict `latch_check(11)` with `return roll >= 11`. (Unit 3)

- **4B-01 `abilities-inside` · Abilities inside** · intro — (skill gate `pattern:NestedSubscript`) · P→R→I · S4 ·
  CC · `dict-nested` · **moment** (boxes in boxes)
  - Code: `bomb_shell = {"name": "Bomb Shell", "mana": 24, "abilities": {"dexterity": 6, "wisdom": 8,
    "magical_affinity": 12}}`.
  - Subgoal label: *Get it out of the dictionary: outer key, then inner key.*
  - CP1 [ND] "Print Bomb Shell's wisdom." Checks: reads through both keys; CMB.
  - Catches: `bomb_shell["wisdom"]` (KeyError: "wisdom lives inside abilities"); `bomb_shell["abilities"]` alone
    prints the whole inner dict.
  - TR: boxes in boxes (static until the live tracer).
  - AW: picture (a sheet with an inner card) · step-by-step · from the campaign
    (`caster["abilities"]["magical_affinity"]`) · in Tor.
  - BQ (combining nested read + comparison): "Print whether Bomb Shell is wise enough for a spell needing
    wisdom 10."
- **4B-02 `change-inside` · Change inside** · intro — · M · SC
  - CP1: Gearshift tunes Bomb Shell's hands, +2 dexterity, as a nested read-modify-write [CMB]. Lucky: "That
    latch might stop hating you."
- **4B-03 `the-roster` · The roster** · intro — · P→M · S4 · CC · `list-of-dicts`
  - The four sheets (real stats) are built in the starter, and `roster = [oogrish, gearshift, bomb_shell, lucky]`.
  - CP1 [D] `roster[2]["name"]`. CP2 [ND] "Print Oogrish's intelligence through `roster`." Checks: CMB.
  - Lucky's box: "In the campaign, this list is called `party.members`."
- **4B-04 `spell-book-of-spells` · A spell book of spells** · intro — · P→I→M · S4 · CC · `dict-make`,
  `dict-write`, `dict-key-from-variable` · point-at-it
  - Code: `spell_book = {"Glow": {"mana_cost": 2, "required_affinity": 3}}`. Predict
    `spell_book["Glow"]["mana_cost"]`.
  - Starter: `spell_name = "Lantern Ward"`, `cost = 6`, `needed = 9`,
    `spell = {"mana_cost": 0, "required_affinity": 0}`, with the comment **"Replace each 0 with the variable that
    holds that value"** (C2: the names differ from the keys on purpose; "matching" waits for 6B-03).
  - CP1 [D] "Replace each 0." Checks: CMB (cost 5, needed 7); SWAP ("`mana_cost` holds 9, which is `needed`; the
    cost is in `cost`.").
  - CP2 [D] "Store the spell: `spell_book[spell_name] = spell`." Checks: KEY; CMB; Glow is kept.
  - Point-at-it: "Which variable holds the spell's name?"
  - Catches: literals left in the blanks (A-08 `25 * 2`; the campaign's "replace each placeholder" step);
    `spell_book["spell_name"] = spell`.
  - PA: yes.
  - BQ (combining store + `in`): "Then print whether `"Lantern Ward" in spell_book`."
  - WA: `"mana_cost": 6` → CP1, CMB; swapped → CP1, "swapped"; `spell_book["spell_name"]` → CP2.
- **4B-05 `can-they-cast` · Can they cast?** · intro — · A→M · S3 · CC · `dict-nested`, `boundary`,
  `elif-chain`
  - Given `caster` and `spell = spell_book["Lantern Ward"]`, write an `if/elif/else`:
    - if the affinity (a nested read) is too low → "isn't skilled enough";
    - else if the mana is too low → "needs more mana";
    - else subtract the cost and print the mana left.
  - Subgoal labels: *Get it → Compare → Act.*
  - CP1 [ND] the low-affinity case. CP2 [ND] the low-mana case. CP3 [ND] the casting case, including exactly enough
    mana. Checks: BND reruns with 4 caster setups.
  - Catches: `<=` instead of `<`; `caster["magical_affinity"]` (a skipped level).
  - PA: distractors `<=` and the flat key.
  - AW: step-by-step · from the campaign (the `hold-the-barrier` comments, described) · picture.
  - PR: "The navigator reads each condition aloud in plain English."
  - BQ (G4 R16, combining): "Say how much mana is missing: `needs 3 more mana`."
  - WA: `<=` → CP3, "exactly"; the flat key → crash, KeyError.
- **4B-06 `broken-spell-4B` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each: `bomb_shell["dexterity"]`, `roster["Lucky"]` (TypeError row), `spell_book[Glow]`.
- **4B-S `solo-4B`** · SOLO, one bug · CC
  - By seat: A `lucky["magical_affinity"]`; B `roster["Lucky"]["mana"]`.
  - CP1 [ND].

### Quiz 4 [SC, 8 questions] (u05b)

1. **predict.** `print("Glow" in spell_book)` / `print(2 in spell_book)` → `True`, `False`.
2. **mc.** `spell_name = "Glow"`. Which line prints Glow's cost: `spell_book["spell_name"]` /
   `spell_book[spell_name]` / `spell_book.spell_name`? → the 2nd.
3. **parsons.** Build a `spell` from `cost` and `needed`, then store it by `spell_name`. Distractor:
   `spell_book["spell_name"] = spell`.
4. **predict.** A nested read → 8.
5. **fill.** `hero["mana"] = hero["mana"] ___ cost` → `-`.
6. **bug.** A KeyError from the wrong nesting level.
7. **predict.** A list-of-dicts read.
8. **predict (def/return item).** `def cost_of(book, name): return book[name]`, then
   `print(cost_of(spell_book, "Glow"))` → `2`.

### Project 4P "Mar'tu's Ledger of Heroes" [SC, 20 min] (u05b)

**Premise.** Mar'tu copies each hero's record into the cabin ledger, Institute-style.

**Starter:** the task-group headers. Under "Show me more", two of the four sheets are pre-built (G1 R17).

**Tasks:**
- **A. Sheets**
  1. Four sheets with `"name"`, an `"abilities"` dict (`magical_affinity` plus two real abilities of the student's
     choice), and an empty `"spell_book"`.
- **B. Let the code combine it (recipe reuse, D11)**
  2. Write `max_mana_for(affinity)` again (it returns twice the affinity).
  3. Set each sheet's `["max_mana"]` with it, and `["mana"]` to the max.
- **C. Roster**
  4. `roster = [...]`.
  5. Print Bomb Shell's dexterity and Oogrish's intelligence through `roster`.
  6. Gearshift casts Fire Bolt (6).

**Checks:**
- The values match the table.
- PAR on `max_mana_for`.
- CMB: `max_mana` follows the affinity.
- The nested reads are right.
- KEY.

**Lucky's side quest (old groups D–E, pool):** Lucky drinks glug (+2, never over max, with an `if`); add `"Glow"`
to Oogrish's book with `spell_book[spell_name] = spell`; print `in` / `not in` for each hero; and Lucky's mana as
a bar.

### Extra practice 5X [pool] (u05b)

- **4A-T `write-by-key-again`:** spend mana by key [CMB].
- **4B-T `store-by-name-again`:** `book[spell_name] = spell`, then `in` [KEY].

### Quick Check 4 [O, ~12 min] (u05c: `qc4-a`, `qc4-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| C1 | Make a sheet with given keys | code | `dict-make` | `"Max_Mana"` → KEY; `{name: …}` → crash |
| C2 | Read `["abilities"]["wisdom"]` | code | `dict-nested`, `dict-read` | `hero["wisdom"]` → crash |
| C3 | `book[spell_name] = spell`, built from variables | code | `dict-write`, `dict-key-from-variable` | `book["spell_name"]` → KEY; literals → CMB |
| Q1 | `in` / `not in` on keys and on a value | predict | `dict-in` | `2 in book` → True |
| C4 | Mend a KeyError from a skipped nesting level | code | `dict-nested` | left unmended |
| C5 | (G4 R1) `roster[1]["name"]`, then spend that hero's mana by a cost variable | code (2 CPs) | `list-of-dicts`, `dict-write` | a typed number → CMB; `roster["Gearshift"]` → crash |

Form B uses Oogrish's sheet, a `wards` book and `roster[3]`.

### Cheatsheet: Dictionaries

`{"name": "Lucky", "mana": 26}` · **box names have no quotes; keys are text, so they do** · `hero["mana"]` ·
`hero["mana"] = hero["mana"] - 3` · `hero["glug"] = 2` (a new key) · `"Glow" in book` / `not in` (keys) ·
`book[spell_name]` (a variable) versus `book["spell_name"]` (the text) · `hero["abilities"]["wisdom"]` ·
`roster[2]["name"]` · `book[name] = spell` · a KeyError means "no key spelled exactly like that".

---

## Unit 6 · Loops: "Every Member of the Party" (`loops`, files u06a–u06b)

**Mar'tu's framing.** "Four heroes. Four bars to draw. Write it four times? No. Write it once, and let Python walk
down the line, yes?"

**RPG tie-in.** The roster loop is the campaign's `for member in party.members:`. The chalk wall's shrink reveals
that "the decay is accelerating". A countdown to the burst. Bomb Shell's Velocite watch.

**Learning objectives. Student can…**
1. Explain why loops exist, and write `for item in items:` with an indented body.
2. Loop over a list of dicts, read keys from each item, and call a helper or a recipe for each one.
3. Accumulate a total or a count, with the reset *before* the loop (SC).
4. Put an `if` inside a loop to filter (SC).
5. Loop with `range(len(...))` to compare neighbors (SC; the decay reveal).
6. Write a `while` loop with an update, recognize and stop an infinite loop, and use `break` (SC).

Optional: `continue`, nested loops, comprehensions, `a if c else b`, `.items()`.

**Campaign links.**
- Obj 1–2 → the bottom loops of `spell-book` and `mana-bars`.
- Obj 3 → the `hold-the-barrier` arithmetic, spaced.
- Obj 6 (`break`) → a bridge to Unit 7's early `return`.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 5A "For Each, Yes?" (with 5A-remembers) | CC: 5A-R, 5A-01, 5A-02, 5A-03, 5A-07, 5A-S; the rest SC | 37 | u06a |
| 2 | Lesson 5B "While the Clock Ticks" (with 5B-remembers) | SC | 14 | u06a |
| 3 | Quiz 5 | SC | 8 | u06a |
| 4 | Project 5P "The Velocite Watch" | SC | 20 | u06b |
| 5 | 6X Extra practice (5B-05) | pool | 3 | u06b |
| 6 | Lesson 5C "Loops in One Line" | O | 20 | u06b |
| 7 | Article 5-A1 "Looping Over a Dictionary" | O | 10 | u06b |
| 8 | Quick Check 5 (forms A, B) | O | 12 | u06b |
| 9 | Cheatsheet: Loops | ref | — | u06b |

### Lesson 5A "For Each, Yes?" [37 min] (u06a)

*Mar'tu remembers… (`5a-remembers`)*
1. `bomb_shell["abilities"]["wisdom"]`. (Unit 5)
2. Predict `strength_check(12)` with `return roll >= 12`. (Unit 3)

- **5A-01 `predict-the-loop` · Predict the loop** · intro `node:For` · P→R→I→M · S4 · CC · `for-each`
  - Predict how many lines `for color in ["gold", "fire orange", "teal", "silver"]: print(color)` prints.
  - CP1 [D] "Add a fifth color, `"violet"`, for Mar'tu." Check: five lines.
  - TR: a static loop table (`color` on each pass), open by default.
  - AW: everyday ("Mar'tu walks down the line and taps each hero") · picture (a finger moving along a shelf) ·
    step-by-step (the table) · shorter.
  - BQ (combining loop + concat): "Print `<color> light` for each."
- **5A-02 `each-mark` · Each mark on the wall** · intro — · M · S3 (skeleton, G3 R19) · CC · `for-each`
  - Learn: the naming rule (G2 R24): "**A name you invent is yours. A name the task gives you is a promise.**"
    The loop variable is yours.
  - Example: a loop over spell colors. foreign: `color`.
  - Starter: `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` / `for ___ in chalk_wall:` /
    `    # print it as "48 hours"`
  - CP1 [ND] "Print every gap on the wall as `<gap> hours`." Check: LOOP (a rerun with a 3-item wall).
  - Catches: seven separate `print` lines → LOOP. Using the Example's loop variable is fine.
  - BQ (combining loop + `if`): "Mark the gaps under 45 with `!`."
  - WA: seven prints → CP1, "3 gaps".
- **5A-03 `each-member` · Each member of the party** · intro — · M · S3 · CC · `for-each`, `list-of-dicts`
  - Setup: `roster` (4 hero dicts) and `show_on_ley_board(text)`.
  - CP1 [ND] "For each `member`, show `<name>: <mana>` on the ley board." Checks: CALL (4 lines, in order); LOOP
    (5 heroes).
  - Catches: `print(roster["name"])` (TypeError row); `roster` written where `member` belongs.
  - Lucky's box: `for member in party.members: show_mana(member)`.
  - AW: step-by-step (a trace table of `member` on each pass) · picture · from the campaign.
  - PA: yes.
  - BQ (combining loop + nested read): "Show each hero's magical affinity too."
- **5A-04 `running-total` · Running total** · intro — · P→M · S3 · SC · `accumulate`
  - CP1 [ND] "Add up the party's mana into `total`." Checks: 88 for the real party; CMB; LOOP.
  - Catches: `total = 0` inside the loop → "Your total restarts every pass. Move `total = 0` above the loop."
  - TR: the static trace table, retrofitted to the trace-table item type at the Unit 3 gate.
  - The long form is shown; `+=` is accepted.
  - AW: picture (a tally jar) · step-by-step · everyday.
  - BQ (combining accumulate + division): "Print the average mana."
- **5A-05 `how-much-each-gap-shrank` · How much each gap shrank** (renamed, G2 R13) · intro — · P→I→M · S4 · SC ·
  **protected story beat** · **moment** (the decay reveal, as a class discussion)
  - Predict-heavy, with the static trace table.
  - Starter: `for i in range(1, len(chalk_wall)):` / `    shrink = 0` / `    print(shrink)`.
  - CP1 [D] "Make `shrink` the gap before minus this gap: `chalk_wall[i - 1] - chalk_wall[i]`." Checks: OUT
    `0 1 1 2 3 4`; LOOP (another wall).
  - Mar'tu, after it passes: "The decay is accelerating. Now you have seen it yourself."
  - AW: picture (neighbors on the wall) · step-by-step.
  - BQ (G4 R16, combining): "Gaps between the gaps: print how much each shrink grew (1, 0, 1, 1, 1)."
- **5A-06 `loop-with-a-check` · A check inside the loop** · intro — · M · S2 · SC · `loop-with-if`
  - CP1 [ND] "Print the names of heroes with less than 10 mana: `needs rest`." Check: CMB (altered mana).
  - BQ (combining filter + count): "Count them too."
- **5A-07 `bars-for-everyone` · Bars for everyone** (recipe-shaped, D11) · intro — · Mk · S3 · CC ·
  `repeat-string`, `func-takes-dict`, `for-each` · point-at-it
  - Starter: `def mana_bar(hero):` / `    full = "█"` / `    empty = "░"` /
    `    # hand back full blocks for mana, empty blocks for the mana used` / `    return ""` /
    `for member in roster:` / `    # print the name and the bar`
  - CP1 [ND] "Make `mana_bar(hero)` hand back the bar for any hero." Checks: PAR (test dicts, mana 0 and full);
    RET.
  - CP2 [ND] "Print each member's name and bar." Check: LOOP.
  - Point-at-it: "Which part is the mana *used*?"
  - Catches: missing parentheses (the TypeError row).
  - Lucky's box: `get_mana_bar`.
  - PA: yes.
  - BQ (combining bar + concat): "Add ` <mana>/<max_mana>` after each bar."
- **5A-08 `broken-spell-5A` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each: a body that isn't indented; `total = 0` inside the loop;
    `print(roster["name"])`; a loop over `roster` that prints `roster`.
- **5A-S `solo-5A`** · SOLO, one bug · CC
  - By seat: A `print(roster["name"])` inside the loop; B an unindented body.
  - CP1 [ND].

### Lesson 5B "While the Clock Ticks" [SC, 14 min] (u06a)

*Mar'tu remembers… (`5b-remembers`)*
1. `"Glow" in spell_book`. (Unit 5)

- **5B-01 `countdown` · Countdown** · intro `node:While` · P→R→I · S3 · SC · `while-loop`
  - Count `hours_left` from 5 down to 1, then print "Burst!".
  - CP1: OUT; CMB (start at 3).
  - TR.
- **5B-02 `the-loop-that-never-ends` · The loop that never ends** · intro — · D · SC
  - The glug loop forgets `glug = glug - 1`. Run it, read the step-limit row, and fix it.
  - WT: "What the step limit is."
- **5B-03 `stop-at-the-first` · Stop at the first** · intro `node:Break` · M · S2 · SC · `break`
  - CP1 [ND] "Find the first gap under 45, print it, and stop." Checks: exactly one line; LOOP.
  - WT: "`break` leaves a loop. In Unit 7, `return` leaves a whole recipe."
- **5B-04 `forecast` · Mar'tu wants to show you something** · intro — · P→R · SC · 2 min · **protected story beat**
  - Pre-written: `gap = 37`, `shrink = 5`; `while gap > 24`: subtract `shrink`, add 1 to `shrink`, print `gap` →
    32, 26, 19 (verified).
  - Predict, then Run. Then change `shrink` and Run again.
  - Mar'tu, grim: "If this is right, we run out of nights."
  - BQ (G4 R16): "Find the smallest `shrink` that runs out of nights in 3 steps."
- **5B-S `solo-5B`** · SOLO, one bug
  - By seat: A a `while` update that moves the wrong way; B a countdown that is off by one.
  - CP1 [ND].

### Quiz 5 [SC, 8 questions] (u06a)

1. **predict.** An accumulator over `[18, 20, 24, 26]` → `88`.
2. **bug.** `total = 0` inside the loop prints `26`; fix it to print `88`.
3. **predict.** `while hours_left > 0` from 3 → `3` `2` `1`.
4. **predict.** The shrink loop → `0 1 1 2 3 4`.
5. **mc.** How many times does a loop body run?
6. **predict (loop-with-if, QC5 fix).** Names with mana under 10.
7. **predict.** `break` output.
8. **predict (def/return item).** `double(total)` after the loop.

### Project 5P "The Velocite Watch" [SC, 20 min] (u06b)

**Premise.** Bomb Shell has about a week of Velocite ore left. Gearshift wants numbers, not guesses: "Run the
math."

**Tasks:**
- **A. Use log (recipe-shaped, D11)**
  1. `velocite_used` holds the daily amounts (given).
  2. **`average(values)`** returns the total divided by the count, using a loop. [PAR, RET]
- **B. Days left**
  3. A `while` loop counts the days until `ore_left` drops below one day's average use.
- **C. Party check**
  4. For each member, print the name and a mana bar (reuse 5A-07's `mana_bar`).
  5. Flag anyone under 10 mana.

**Checks:** CMB and LOOP reruns with other logs and rosters; PAR on `average`.

**Lucky's side quest (old group D, pool):** `break` at the first day over 4, and print it.

### Extra practice 6X [pool] (u06b)

- **5B-05 `broken-spell-5B`:** a `while` whose update moves the wrong way; a countdown off by one.

### Lesson 5C "Loops in One Line" [O] and Article 5-A1 [O] (u06b)

- **5C-01 `skip-the-empty`:** intro `node:Continue`. Skip heroes with 0 mana.
- **5C-02 `loops-in-loops`:** print every entry of the 2D training log.
- **5C-03 `one-line-loops`:** intro `node:ListComp`. `[h for h in chalk_wall if h < 45]`.
- **5C-04 `choose-in-one-line`:** intro `node:IfExp`. `"ready" if mana >= 3 else "resting"`.
- **5-A1 "Looping Over a Dictionary":** `for name, cost in spell_book.items():`, plus `.keys()` and `.values()`.
  Intro `attr:items` `attr:keys` `attr:values` `node:Tuple`. It recaps tuples on the page.

### Quick Check 5 [O, ~12 min] (u06b: `qc5-a`, `qc5-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| C1 | Call a helper for each roster member | code | `for-each`, `list-of-dicts` | four typed calls → LOOP |
| C2 | Total the party's mana, and print the names under 10 mana (2 CPs) | code | `accumulate`, `loop-with-if` | the total typed → CMB; the reset inside the loop |
| Q1 | A `while` countdown | predict | `while-loop` | off-by-one |
| Q2 | `break` at the first match | predict | `break` | prints every match |
| C3 | Mend an accumulator that resets inside the loop | code | `accumulate` | left unmended |

### Cheatsheet: Loops

`for item in items:` plus an indent · `for member in roster: member["name"]` · `total = 0` **before** the loop ·
`for i in range(1, len(wall)):` · `while x > 0:` plus an update · the step limit means an infinite loop · `break`.

---

## Unit 7 · Functions II: "Spells You Can Hand Over" (`spell-recipes`, files u07a–u07c) — D2

**Mar'tu's framing.** "You know recipes. Now they read stat sheets, write spell books, and guard the door. And one
more thing, the strange one: a recipe can sit in a box, like any value. You can hand it to someone without
cooking it."

**Terminology** (§2.9): "function" from here on, with Mar'tu still saying "recipe". "Matching" means an exact name
from 6B-03 on.

**Learning objectives. Student can…**
1. Write functions that take a hero dict and return a value from it.
2. Change a dict passed in, and know the caller sees the change. Know when a function needs `return` (the card).
3. Build a dict from parameters with **exact matching names**, and store it by key.
4. Guard with an early `return`.
5. Read a helper they didn't write, call it correctly, and leave it unchanged.
6. Wire two functions together: build the bar, then pass it on.
7. Use a function as a value: assign it, pass it without `()`, store it in a dict, and call it from there with
   `book[name]["effect"](hero)`.

Optional or pool: default and keyword arguments (6B-08), scope (6B-09), lambda, `map()`, two return values.

**Campaign links.**
- Obj 1, 6 → `mana-bars` (`get_mana_bar`, `show_mana`).
- Obj 3 → `spell-book` (`add_spell`).
- Obj 4 → the opening of `hold-the-barrier`.
- Obj 5 → `print_mana` and `reinforce_barrier`.
- Obj 7 → `strengthen_magic` without `()`, and `spell["spell_function"](caster)`.

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 6B "Recipes That Read Stat Sheets" (with 6B-remembers) | CC (6B-10 SC) | 40 | u07a |
| 2 | Lesson 6C "Spells You Can Hand Over" (with 6C-remembers) | CC (6C-06 SC) | 37 | u07b |
| 3 | Quiz 6B | CC (retrieval) | 8 | u07b |
| 4 | Project 6P "The Resonance Array" | SC · **camp** | 20 | u07b |
| 5 | 7X Extra practice (6B-08, 6B-09) | pool | 10 | u07c |
| 6 | Articles 6-A1 lambda, 6-A2 `map()`, 6-A3 "Two Things Back" | O | 10 each | u07c |
| 7 | Quick Check Recipes II (forms A, B) | O | 12 | u07c |
| 8 | Cheatsheet: Spell Recipes | ref | — | u07c |

### Lesson 6B "Recipes That Read Stat Sheets" [CC, 40 min] (u07a)

*Mar'tu remembers… (`6b-remembers`)*
1. A nested dict write. (Unit 5)
2. A for-each over the roster. (Unit 6)

- **6B-01 `hand-over-a-sheet` · Hand over a sheet** · intro — · M · S1 · CC · `func-takes-dict`
  - Starter: the signature `def mana_line(hero):` only, plus two calls with `# should show` comments.
  - CP1 [ND] "Make `mana_line(hero)` hand back `<name>: <mana>/<max_mana>`." Checks: PAR (a `"Tester"` sheet);
    RET.
  - AW: from the campaign (`get_mana_bar(caster)`, described) · step-by-step · picture.
  - BQ (combining function + loop): "Print a line for every member of `roster`."
  - WA: a typed line for Lucky → CP1, "Tester"; `print` instead of `return` → CP1, "None".
- **6B-02 `recipes-change-sheets` · Recipes change sheets** · intro — · P→I→M · S2 · CC · `func-takes-dict`
  - Investigate: after `rest(lucky)`, the caller's `lucky` has full mana.
  - CP1 [ND] "Write `spend(hero, cost)`, which subtracts the cost from `hero["mana"]`. No `return` is needed."
    Check: PAR with a test dict; the caller's dict changes.
  - **Card (G3 R25): "When does a recipe need `return`?"** "When the caller needs a value back (`mana_line`). A
    recipe that only changes a sheet in place (`spend`) doesn't." Paid off by 6B-07.
  - WT: "Same sheet, two labels."
  - TR: yes.
- **6B-03 `many-ingredients` · Many ingredients** · intro — · M · S4 · CC · `dict-from-params`
  - Starter (campaign phrasing):
    - `def make_spell(mana_cost, required_affinity, color):`
    - `    # 1. Replace each placeholder with the matching parameter.`
    - `    spell = {"mana_cost": 0, "required_affinity": 0, "color": ""}`
    - `    # 2. Hand back the spell.`
  - CP1 [D] "Replace each placeholder with the matching parameter." Checks: PAR (`make_spell(5, 2, "teal")` and
    `(9, 7, "gold")`); SWAP.
  - CP2 [D] "Hand back `spell`." Check: RET.
  - **Investigate, "same word, two jobs" (C2 / G4 R6):** rename the parameter `mana_cost` to `cost` everywhere it
    is a parameter, and Run: it still works. Then rename the *key*, and see the spell change shape.
    "`"mana_cost"` with quotes is a label; `mana_cost` without quotes is the box handed in."
  - Catches:
    - literals left in place (A-08) → PAR;
    - `"mana_cost": "mana_cost"` (A-02's quoted-name habit) → "`mana_cost` holds the text `'mana_cost'`. Use the
      parameter without quotes.";
    - swapped parameters → SWAP.
  - PA: yes.
  - Campaign `spell-book`, step 1.
  - BQ (combining dict + function): "Add `"strength": mana_cost * 2` to the spell."
  - WA: `0` left → CP1, PAR; quoted → CP1, "text"; swapped → CP1, "swapped".
- **6B-04 `store-by-name` · Store by name** · intro — · M · S2 · CC · `store-by-name`
  - CP1 [ND] "Write `add_to_book(book, spell_name, spell)`, which stores the spell under its name." Check: KEY.
  - CP2 [ND] "Make sure a second spell keeps the first." Check: CMB.
  - Catches: `book["spell_name"] = spell`; `book = {spell_name: spell}` ("the book outside didn't change").
  - WT: "Why `book = {...}` doesn't reach the caller."
- **6B-05 `guard-at-the-door` · Guard at the door** · intro — (skill gate `pattern:EarlyReturn`) · P→I→M · S3 ·
  CC · `early-return`
  - CP1 [ND] "Add a guard to `cast_glow(hero, spell_name)`: if the spell is not in `hero["spell_book"]`, show
    `<name> doesn't know <spell>.` and `return`." Checks: CALL (one message); mana unchanged.
  - CP2 [ND] "A known spell still goes ahead." Check: the mana is spent.
  - AW: everyday ("a guard checks your name at the door before anything else happens") · step-by-step · from the
    campaign (the opening of `hold-the-barrier`).
  - WT: "The early `return` is `break` for a whole recipe."
  - BQ (combining guard + comparison): "Add a second guard for not enough mana."
- **6B-06 `read-the-helper` · Read the helper** · intro — · I→R · S4 · CC · `read-helper`
  - Starter: a visible `draw_bar(hero, bar)` with the comments "# This function is already finished. Leave it as
    it is." and "# It draws bar in this hero's row."
  - Questions (one click):
    - "Which lines should you change?" (none in `draw_bar`)
    - "What two things does it need?"
  - CP1 [D] "Call it for Lucky with any bar text." Checks: KEEP; CALL with `(lucky, <str>)`.
  - Lucky's box: `print_mana(caster, mana_bar)`. P19 practice.
- **6B-07 `bar-then-draw` · Build the bar, then draw it** · intro — · Mk · S4 · CC · `repeat-string`,
  `store-then-pass`, `read-helper` · rehearsal (`mana-bars`)
  - Gearshift's starlode gauge.
  - Starter:
    - `get_fuel_bar(robot)` has `"▮" * 0` and `"▯" * 0`, with comments naming `robot["fuel"]` and
      `robot["max_fuel"] - robot["fuel"]`;
    - `show_fuel(robot)` has store-then-pass comments;
    - the bottom loop over `robots` is already written.
    - The numbered comments map 1:1 onto the checkpoints, and the blocks are pre-typed.
  - CP1 [D] 3 of 5 → `Fuel [▮▮▮▯▯] 3/5`.
  - CP2 [D] empty and full gauges.
  - CP3 [D] `show_fuel` draws once [CALL].
  - CP4 [D] the bar is stored in a variable [STO].
  - These mirror the campaign's four checks.
  - Catches: `"▯" * robot["max_fuel"] - robot["fuel"]` (precedence); `draw_bar(robot, get_fuel_bar)`.
  - PA: per function.
  - TR: yes.
  - BQ (combining): "A glug gauge for Lucky with `▓`."
- **6B-10 `broken-spell-6B` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - a missing `return` in `mana_line` (`"Status: " + mana_line(lucky)` raises the NoneType TypeError);
    - `book["spell_name"]`;
    - `"░" * a - b`;
    - a literal instead of a parameter.
- **6B-S `solo-6B`** · SOLO make-twin · S2 · CC
  - By seat: A `rest(hero)` sets the mana to max; B `drink_glug(hero, sips)` adds sips to the mana.
  - CP1 [ND] Check: PAR, with the caller's dict changing.

### Lesson 6C "Spells You Can Hand Over" [CC, 37 min] (u07b)

*Mar'tu remembers… (`6c-remembers`)*
1. Store-then-pass. (Unit 3)
2. `spell_book[spell_name] = spell`. (Unit 5)

- **6C-01 `name-without-parentheses` · A name without parentheses** · intro — (skill gate `pattern:FuncValue`) ·
  P→I→M · S4 · CC · `func-as-value` · **moment** ("the box holds the recipe")
  - `warm_hands(hero)` shows a message.
  - Predict what `chosen_spell = warm_hands` does: nothing visible, because the box now holds the *recipe*.
  - CP1 [D] `chosen_spell = warm_hands`. Check: NOP (it holds the function).
  - CP2 [D] `chosen_spell(lucky)`. Check: CALL (one call happened).
  - Catches: `chosen_spell = warm_hands(lucky)` stores `None`, and the later call raises "NoneType not callable"
    (the explainer row).
  - AW: picture (a box holding a recipe card) · everyday ("handing someone the card versus cooking the meal and
    handing them the empty pot") · step-by-step.
  - WT, TR.
- **6C-02 `hand-it-over` · Hand it over** · intro — · M→Mk · S2 · CC · `func-as-value`
  - Given: `cast_on_everyone(heroes, effect)` loops and calls `effect(hero)`.
  - CP1 [D] "Call it with `warm_hands`, no parentheses." Check: CALL × 4.
  - CP2 [ND] "Write your own `cool_down(hero)` and hand it over too." Checks: CALL; NOP.
  - Catches: `cast_on_everyone(roster, warm_hands(lucky))` → NOP.
  - Lucky's box: `add_spell(..., strengthen_magic)`.
  - BQ (G4 R16, combining): "Write `cast_twice(effect, hero)`."
- **6C-03 `recipe-in-a-box` · A recipe in a box** · intro — (skill gate `pattern:CallOnSubscript`) · P→M · S4 · CC
  · `call-stored-func`
  - Code: `glow = {"mana_cost": 2, "required_affinity": 3, "effect": light_lantern}`.
  - Predict: `glow["effect"]` alone does nothing; `glow["effect"](lucky)` runs it.
  - CP1 [D] "Cast Glow on Lucky from the dict." Check: CALL.
  - Catches: a missing `(lucky)`.
  - AW: picture · from the campaign (`spell["spell_function"](caster)`, with "the parentheses on the end are what
    call it").
- **6C-04 `write-the-spell-book` · Write the spell book** · intro `const:None` · A→M · S4 · CC ·
  `dict-from-params`, `store-by-name`, `func-as-value` · rehearsal (`spell-book`) · **camp**
  - The starter's placeholders are `0, 0, None`, exactly like the campaign's `"spell_function": None`. That is
    why this exercise introduces the literal `None`.
  - Starter: `learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect)` builds the placeholder
    dict, followed by "# Store the spell in spell_book, using spell_name as the key". The bottom loop gives every
    hero Lantern Ward (6, 9, `lantern_ward`) and is already written.
  - CP1 [D] "Replace each placeholder with the matching parameter." Checks: PAR; SWAP.
  - CP2 [D] "Store the spell in `spell_book`, using `spell_name` as the key." Check: KEY.
  - CP3 a second spell keeps the first.
  - CP4 every hero knows Lantern Ward.
  - These mirror the campaign's checks.
  - Catches: literals left in place; `lantern_ward(hero)` in the bottom loop (NOP).
  - **Campaign mode:** numbered comments, check messages, the explainer, Compare after 5 min, hints capped at rung
    2, and no Assemble it (the "Show me more" Assemble-first view is off here).
- **6C-05 `cast-from-the-book` · Cast from the book** · intro — · A→Mk · S2 (L1) · CC · `dict-nested`,
  `elif-chain`, `boundary`, `call-stored-func`, `dict-write` · rehearsal (`hold-the-barrier`) · **camp**
  - Starter: `cast(hero, spell_name)` with the guard and `spell = hero["spell_book"][spell_name]` given, then
    three numbered comments.
  - The student writes the `if/elif/else`:
    - nested affinity `<` required → a message;
    - `elif` mana `<` cost → a message;
    - `else` → call `spell["effect"](hero)`, subtract the cost, and call `show_mana(hero)`.
  - CP1 a skilled caster with enough mana casts. CP2 the mana bar updates. CP3 too little affinity doesn't cast.
    CP4 too little mana doesn't cast. CP5 exactly enough mana still casts. CP6 the spell's own cost is used.
    These mirror the campaign's six checks.
  - Catches: `<=`; `spell["effect"]` with no `(hero)`; `hero["magical_affinity"]`; a typed number;
    `hero["mana"] - cost` without assigning it back.
  - **More-structure ladder (G3 R15).** L1 is the default for everyone. Under "Show me more" the student can step
    down; a pass below L1 is recorded "with structure":

    | Level | What the editor shows |
    |---|---|
    | L1 | numbered comments, campaign style |
    | L2 | `if ___ < ___:` / `elif ___ < ___:` / `else:`, each body still a comment |
    | L3 | adaptive Parsons (the distractors above) |
    | L4 | a worked twin with a different spell, then retype |
  - **Campaign mode** otherwise: hints capped at rung 2; this is the most important exercise for offers.
  - Subgoal labels: *Get it → Compare → Act.*
- **6C-06 `broken-spell-6C` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each: `spell["effect"]` not called; `learn_spell(..., lantern_ward(hero))`; `<=`; a
    subtraction that is never stored.
- **6C-S `solo-6C`** · SOLO make-twin · S2 · CC
  - By seat: A stores a `shout` recipe in a dict and calls it from there; B hands `shout` to `cast_on_everyone`.
  - CP1 [ND] Checks: CALL, NOP.

### Quiz 6B [CC, 8 questions] (u07b)

1. **predict.** `spells = {"glow": glow}` / `print(spells["glow"]("Lucky"))` → `Lucky glows.`
2. **mc.** "Which line hands over the recipe without running it?" `cast_on_everyone(roster, warm_hands)` /
   `…(roster, warm_hands())` / `…(roster, "warm_hands")` → the 1st.
3. **predict.** `spend(hero, 3)` changes the caller's dict → `23`.
4. **parsons.** The `cast` body with indentation. Distractors: `<=`, `spell["effect"]`.
5. **parsons.** `learn_spell`.
6. **bug.** `"░" * a - b`.
7. **mc.** What does `return` with nothing after it do?
8. **predict.** The guard clause's output.

### Project 6P "The Resonance Array" [SC, 20 min, **camp**] (u07b)

**Premise.** The brass resonance array Mar'tu hauled from the Institute has dials, and each dial needs a formula.
Mar'tu: "At the Institute we wrote every dial as a recipe. Then nobody argued about the arithmetic."

**Tasks** (campaign mode):
- **A. Dials**
  1. `max_mana_for(affinity)`.
  2. `average_damage(die_size)` returns `(1 + die_size) / 2`.
  3. `next_gap(last_gap, shrink)`.
- **B. Calibrate**
  4. `calibrate(hero)` returns a dict of readings, built by calling the dial functions on the hero's sheet.
- **C. Run the array**
  5. `run_array(heroes, dial)` takes a function as a value and prints `dial(hero)` for each hero.

**Checks:** PAR and RET with fresh values for every dial; CALL and NOP for C.

**Lucky's side quest (old group D, G4 R16):** swap `run_array` for a **dict of dials**:
`dials["mana"](hero)`.

### Extra practice 7X [pool] and the optional articles (u07c)

- **6B-08 `defaults-and-names`** (pool) · intro `node:DefaultArg` `node:KeywordArg`. `roll_die(die_size=20)`;
  `roll_die()` rolls a d20, and `roll_die(die_size=6)` a d6 [RND]. It is the prerequisite card for T-F-1.
- **6B-09 `inside-stays-inside`** (pool). Predict: printing `restored` outside `rest()` gives a NameError, because
  parameters and inner boxes live only inside the recipe. Then return `restored` and print it [RET].
- **6-A1 lambda** (O, `node:Lambda`) · **6-A2 `map()`** (O, `call:map`) · **6-A3 "Two Things Back"** (O; recap
  card for `node:Tuple` if 3-A1 was skipped).

### Quick Check Recipes II [O, ~12 min] (u07c: `qc-r2-a`, `qc-r2-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| C1 | `learn_ward(wards, ward_name, mana_cost, effect)`: a dict from parameters, stored by name | code | `dict-from-params`, `store-by-name` | literals left → PAR; `wards["ward_name"]` → KEY |
| C2 | An early-`return` guard in `use_ward(hero, ward_name)` | code | `early-return` | no `return` → it carries on (CALL) |
| C3 | Call a finished helper correctly without changing it | code | `read-helper` | an edited helper → KEEP; the arguments swapped → CALL |
| C4 | Call a stored function: `wards[name]["effect"](hero)` | code | `call-stored-func` | `(hero)` missing → CALL |
| Q1 | Handing over versus calling | mc | `func-as-value` | `warm_hands()` |
| Q2 | A missing `return`, printed | predict | `none-return` | a value instead of `None` |
| Q3 | A function that changes a passed-in sheet | predict | `func-takes-dict` | "the caller's sheet is unchanged" |

### Cheatsheet: Spell Recipes

A function that takes a sheet · changes to a dict reach the caller · when you need `return` (the card) · the
matching parameter, exactly · `book[name] = spell` · the early-`return` guard · leave finished helpers alone ·
store, then pass · `f` (the recipe) versus `f()` (the result) · `book[name]["effect"](hero)` ·
*(extra)* `def f(x=20)` / `f(x=6)`.

---

## Unit 8 · Code Challenges (optional): "Trials of the Yard" (`code-challenges`, files u08a–u08c)

**Framing.**
- **Mar'tu:** "Oogrish says a weapon is learned in the yard, not in the book. These are his trials. They are
  optional."
- **Lucky:** "What's in it for me?"
- **Mar'tu:** "Practice. And Oogrish stops lecturing you."

**Format** (`challenge`, `support="light"`, explainer always on):
- A signature, a short in-world prompt, and a test table (2–3 visible tests plus hidden labeled tests).
- Every core challenge has an **advanced variant** (`variant_of`): edge cases, a stricter spec, or a refactor.
- Each set opens to anyone on a hint-free streak, a QC pass, or when "Ready for more" lists it. The whole unit
  opens after Unit 7, as in the syllabus.
- **Unlock ceilings** (the TRIALS gate path proves each set uses only tokens taught by its unlock point):

  | Set | Opens after | Token ceiling |
  |---|---|---|
  | T-HCL | Unit 1 | Unit 1 |
  | Control Flow (in function form) | Unit 3 | Units 1–3 |
  | Lists | Unit 4 | Units 1–4 |
  | Dictionaries | Unit 5 | Units 1–5 (T-D-1a, which loops, opens after Unit 6) |
  | Loops | Unit 6 | Units 1–6 |
  | Functions and T-Own | Unit 7 | Units 1–7, plus the 6B-08 and 2-A2 cards |
- "Ready for more" on the teacher page suggests the next open set.

**Objectives:** apply what you know to unseen problems from a signature, handle boundary and empty cases, and read
test tables (the debugging habit).

**Campaign links:**
- T-CF-1a → the `hold-the-barrier` logic.
- T-CF-3 → skill checks with Dumb Luck.
- T-D → `spell-book` and nested reads.
- T-F-3a → `spell["spell_function"](caster)`.
- T-Own → reading check messages.

| File | Set | Core challenge | Advanced variant |
|---|---|---|---|
| u08a | **Refactor (G4 R17)** | **T-HCL "The Hard-Coded Ledger".** A working Unit 1 script full of 68-style literals (`lantern_cost = 12`, `total = 22`, a typed status line). It prints the right thing but fails the **rerun table** until every literal that should be an expression becomes one. Checks: CMB per line; a hidden test reruns with new counts. | — ("Four copies, one loop" and "One bar recipe" are Tier 3.) |
| u08a | **Control Flow** | **T-CF-1** `can_cast(mana, cost)` → True when the mana covers the cost (exactly enough counts). | `can_cast(mana, cost, affinity, required)` → `"ok"`, `"skill"` or `"mana"`, checking skill first. |
| | | **T-CF-2** `clock_color(hours_left)` → `"red"` (≤ 2), `"bright blue"` (≤ 12), else `"calm blue"`. | Negative hours → `"broken"`. Adds a second parameter `flashing`: when True, always `"red"`. (A default value waits for the 6B-08 card.) |
| | | **T-CF-3** `passes_with_luck(first_roll, second_roll, needed, has_luck)` | Returns `"first"`, `"reroll"` or `"none"`. |
| u08a | **Lists** | **T-L-1** `newest_gap(wall)` → the last item. | An empty wall → `-1`. |
| | | **T-L-2** `last_three(wall)` → the slice. | `total_drop(wall)` = first − last, and 0 with fewer than 2 items. |
| | | **T-L-3** `add_guess(wall, guess)` → appends only if `guess` is below the newest gap, and returns the wall. | Returns a **new** list and leaves the original unchanged (`wall[:] + [guess]`). |
| u08b | **Dictionaries** (D8) | **T-D-1** `spell_cost(book, name)` → the cost, or 0 if unknown. | `cheapest_spell(book)` → the name of the cheapest spell (a loop; opens after Unit 6). |
| | | **T-D-2** `affinity_of(hero)` → the nested read. | `meets(hero, spell)` → both checks, nested, with `<` versus `<=` exact. |
| | | **T-D-3** `rename_spell(book, old, new)` | Refuses (returns False) when `new` already exists or `old` is missing. |
| u08b | **Loops** | **T-Lo-1** `total_mana(heroes)` | `average_mana(heroes)`, with an empty roster → 0. |
| | | **T-Lo-2** `count_below(wall, limit)` | `first_shrink_over(wall, amount)` → the index of the first gap whose **shrink** is larger than `amount`, else −1 (an early exit). |
| | | **T-Lo-3** `lowest_mana_name(heroes)` | On a tie, the alphabetically first name. |
| u08c | **Functions** | **T-F-1** `make_bar(current, maximum, full="█", empty="░")` (prerequisite card 6B-08) | Clamp `current` into 0..maximum. |
| | | **T-F-2** `apply_to_all(heroes, effect)` → a list of the names affected. | Include a name only when `effect(hero)` returns True. |
| | | **T-F-3** **Refactor:** replace a four-branch `elif` that maps options to lines with a dict lookup `lines[choice]`, with a default. | A dict of *functions*: `actions[choice](hero)`. An unknown choice → False. |
| u08c | **Write your own checks** | **T-Own** Write 4 `assert` lines that would catch a wrong `can_cast` ("Mar'tu's seal", prerequisite 2-A2). | Write asserts that catch the `<=` bug in a given `cast_ok` *and* pass the correct one. |

**Cheatsheet:** "How to read a test table."

---

## Unit 9 · Strings: "Runes and Ribbons" (`strings`, files u09a–u09b)

**Independent of the Readiness Check (T1).** Nothing in Unit 10 needs a Strings token (the READY gate path proves
it). The teacher can run this unit before Module 2, alongside it, or after it.

**Mar'tu's framing.** "Runes are only letters in a row. Python sees words the same way. Today we cut them,
stretch them, and make them behave. Lucky, your notes are next."

**RPG tie-in:**
- Bomb Shell's clipped sentences (`.split()`).
- Lucky's "What's in it for me?" (methods).
- The greenroom sign ("Greenroom, Interior" / "EXIT"; slicing).
- "It is NOT a compass" (`.replace`).
- Mar'tu's lines tidied with `.lower().capitalize()` (revisited from 6A-08).
- The bars, one more time.

**Learning objectives. Student can…**
1. Index and slice strings, and use `len()`.
2. Explain that strings can't be changed in place, and build new ones instead.
3. Use escape characters `\" \n`.
4. Call methods (`.lower() .upper() .title() .capitalize() .strip() .replace() .find()`), knowing they *return
   new strings*, so reassign (`line = line.lower()`). Chain them.
5. Use `.split()` and `" ".join(...)`, and convert digits with `int()`.
6. Read and write f-strings, **and** read `+ str()` lines fluently (the campaign uses the latter).
7. Build a status bar for any values.

Pool: `in` on strings, looping over characters (8A-04, 8A-05).

| # | Item | Flag | Min | File |
|---|---|---|---|---|
| 1 | Lesson 8A "Strings Are Rows of Letters" (with 8A-remembers) | SC | 20 | u09a |
| 2 | Lesson 8B "Words That Change Shape" (with 8B-remembers) | SC | 32 | u09a |
| 3 | Quiz 8B | SC | 8 | u09a |
| 4 | 9X Extra practice (8A-04, 8A-05, 8A-08, Quiz 8A) | pool | 18 | u09b |
| 5 | Project 8P1 "The Water-Stained Log" | O (recommended) | 40 | u09b |
| 6 | Project 8P2 "The Institute Cipher" | O (browser-only until IDLE is confirmed [OWNER]) | 60 | u09b |
| 7 | Quick Check 8 (forms A, B) | O | 10 | u09b |
| 8 | Cheatsheet: Strings | ref | — | u09b |

### Lesson 8A "Strings Are Rows of Letters" [SC, 20 min] (u09a)

*Mar'tu remembers… (`8a-remembers`)*
1. `spells["glow"]` versus `spells["glow"](hero)`. (Unit 7)
2. Why does `"░" * (10 - 3)` need parentheses? (1C, 6B)

- **8A-01 `letters-have-places` · Letters have places** (absorbs 8A-02 `slice-a-word`) · intro — · P→R→M · S3 · SC
  · `string-index-slice`
  - Predict `"Telegun"[0]`, `[-1]` and `len`.
  - CP1 [ND] "Build `initials` from the roster's names with a loop." Checks: LOOP; CMB.
  - CP2 `slice-a-word` [ND] "From `sign`, slice out the word before the comma." Check: CMB (another sign). This
    fixes the v1 OUT-only check.
  - AW: picture (letters on numbered tiles, like the chalk wall) · step-by-step.
- **8A-03 `letters-cant-change` · Letters can't change** · intro — · D→M · SC
  - `word[0] = "C"` raises a TypeError (the explainer row). CP1: build `"C" + word[1:]` instead.
  - WT: immutability.
- **8A-06 `escape-marks` · Escape marks** · intro `const:escape` · P→I→M · SC
  - CP1 [D] Print `Mar'tu said, "It is not a compass."` with `\"`.
  - CP2 [ND] Print the chalk wall, one gap per line, with `\n`.
  - Note: formatting is off, so quotes stay as typed.
- **8A-07 `bars-one-more-time` · Bars one more time** · intro — · Mk · S3 · SC · `repeat-string` (spaced)
  - Starter: `def make_bar(current, maximum):` with `full = "▓"` and `empty = "░"` pre-typed.
  - CP1 [ND] "Hand back `Glug [▓▓░] 2/3` for any values." Checks: PAR; RET.
  - CP2 empty and full. Check: PAR.
  - Lucky's box: the `mana-bars` return line.
  - PA: yes.
- **8A-S `solo-8A`** · SOLO, one bug
  - By seat: A `"░" * 10 - 3` (this carries the old 8A-08's precedence bug); B `word[0] = "X"`.
  - CP1 [ND].

### Lesson 8B "Words That Change Shape" [SC, 32 min] (u09a)

*Mar'tu remembers… (`8b-remembers`)* (absorbs Quiz 8A's core questions)
1. `"Telegun"[-1]`.
2. `"Greenroom"[:5]`.

- **8B-01 `loud-and-quiet` · Loud and quiet** · intro `attr:upper` `attr:title` (`.capitalize()` revisited) ·
  P→R→I · SC · `string-methods`
  - Investigate: `line.upper()` alone doesn't change `line`, so reassign it.
  - CP1: `line` is now upper case.
  - AW: everyday ("a method hands you a new copy; catch it").
- **8B-02 `chain-the-spells` · Chain the spells** (revisit of 6A-08) · intro — · P→I→M · SC · `chain-methods`
  - CP1 [D] `tidy_line(raw)` in two steps, then chained as `raw.lower().capitalize()`. Checks: PAR; RET
    (`"WHAT IS THE DECAY?"` → `"What is the decay?"`, verified). Both forms pass.
  - Lucky's box: `option_1.lower().capitalize()`.
- **8B-03 `split-the-clipped` · Split and join** (absorbs 8B-04 `join-them-back`) · intro `attr:split` `call:int`
  `attr:join` · P→M · SC · `split-join`
  - CP1 [D] Split Bomb Shell's report on `". "`. Check: CMB (another report).
  - CP2 [ND] Count its words with `len(report.split())`. Check: CMB. This fixes the v1 OUT-only check.
  - CP3 [D] `int("48")` plus one.
  - CP4 `join-them-back` [D] `" ".join(words)`, called on the separator. Catches: `words.join(" ")` (the
    AttributeError row).
- **8B-05 `strip-and-replace` · Clean-up tools** (absorbs 8B-06 `find-a-rune`) · intro `attr:strip`
  `attr:replace` `attr:find` · P→M · SC
  - CP1 Strip Lucky's note `"  It's a compass.  "`.
  - CP2 Replace `compass` with `Ley Clock`. Mar'tu: "Thank you."
  - CP3 `find-a-rune`: `.find` gives an index, or −1 when the text isn't there.
- **8B-07 `f-strings` · f-strings** · intro `node:FString` · P→I→M · SC · `fstring-read`
  - Read both forms: `name + ": " + str(mana) + " mana"` and `f"{name}: {mana} mana"`.
  - CP1: rewrite a `+ str()` line as an f-string (`_uses('node:FString')`; identical output).
  - CP2: translate an f-string back to `+ str()`.
  - WT: "The campaign uses `+` and `str()`, so read both" (Q12: read both, write either).
- **8B-08 `whats-in-it-for-me` · What's in it for me?** · intro — · Mk · S1 · SC · **echo**
  - CP1 [ND] `lucky_reply(request)` hands back the stripped, capitalized request plus `" What's in it for me?"`.
  - CP2 [ND] `clip(sentence)` hands back Bomb Shell's version: the first three words, then a period.
  - Checks: PAR; RET. Any text passes (lint e).
  - Echo: Mar'tu reads Lucky's reply aloud, deadpan (filtered).
  - DF: yes.
  - BQ (combining two functions): `martu_reply` adds ", yes?" to a clipped sentence.
- **8B-09 `broken-spell-8B` · Broken spell** · intro — · D · SC
  - Bugs, one checkpoint each:
    - `line.lower` with no `()`;
    - `line.lower()` that is never stored;
    - `words.join(" ")`;
    - an index past the end of a `split` result.
- **8B-S `solo-8B`** · SOLO, one bug
  - By seat: A `line.lower()` never stored; B `words.join(" ")`.
  - CP1 [ND].

### Quiz 8B [SC, 8 questions] (u09a)

1. **predict.** `"WHAT IS THE DECAY?".lower().capitalize()` → `What is the decay?`
2. **predict.** `" ".join(["Shield", "up."])` and `"gold,teal".split(",")` → `Shield up.` and `['gold', 'teal']`.
3. **predict.** `"EXIT".find("Z")` → `-1`.
4. **bug.** `words.join(" ")`.
5. **mc.** An f-string versus its `+ str()` twin.
6. **predict.** Strip and replace.
7. **fill.** `.___()` → `capitalize`.
8. **bug.** A forgotten reassignment.

### Extra practice 9X [pool] and the projects (u09b)

- **8A-04 `is-it-in-there`** (pool): `clock_warning(report)` returns whether `"red"` is in `report.lower()` [PAR,
  RET].
- **8A-05 `letter-by-letter`** (pool): `count_full(bar)` counts the `"█"` blocks with a loop [PAR, RET].
- **8A-08 `broken-spell-8A`** (pool): an index past the end, `word[0] = "X"`, `len(26)`.
- **Quiz 8A** (pool, 6 questions).
- **8P1 "The Water-Stained Log"** (O, recommended, 40 min). Lucky copied the chalk wall in the rain:
  `" 48 hrs| 48 hrs |47 hrs|46hrs | 44 hrs|41 hrs | 37hrs "`. Tasks:
  1. `split("|")`.
  2. `strip` and `replace("hrs", "")`, then `int()`.
  3. Build a list.
  4. The total and the shrinks.
  5. `join` a clean line.
  6. An f-string summary.

  Checks: CMB with other messy strings. Side quest: skip a smudged `"4?"`.
- **8P2 "The Institute Cipher"** (O, 60 min). "Ley shift" encoding with `alphabet.find` and `% 26`. Prerequisite
  card 1-A2. Browser-only until IDLE is confirmed **[OWNER]**.

### Quick Check 8 [O, ~10 min] (u09b: `qc8-a`, `qc8-b`, plus question forms)

| # | Form A item | Type | Skills | Fails on |
|---|---|---|---|---|
| C1 | `tidy_line` chained | code | `chain-methods`, `string-methods` | `.lower` with no `()` → PAR |
| C2 | Split, then join | code | `split-join` | `words.join(" ")` → crash |
| C3 | `make_bar` with `(max - cur)` and `str()` | code | `repeat-string` | no parentheses → crash |
| Q1 | An index and a slice | predict | `string-index-slice` | off-by-one |
| Q2 | Read an f-string | predict | `fstring-read` | — |

### Cheatsheet: Strings

`s[0]`, `s[-1]`, `s[2:5]`, `len(s)` · strings can't change in place: `"C" + s[1:]` · `\" \n` · methods return a
new string, so `s = s.lower()` · `.lower().capitalize()` · `.split()` / `" ".join(list)` · `.strip()`,
`.replace(a, b)`, `.find(x)` → −1 · `int("48")` · `f"{name}: {mana}"` equals `name + ": " + str(mana)`.

---

## Unit 10 · Campaign Readiness Check: "Before We Continue" (`readiness-check`, files u10a–u10c)

**Mar'tu:** "You have learned enough to help, yes? Show me without the hints. Then we continue."

The full specification is in §5. Files:
- **u10a:** the intro, Part 1 form A, mini-boss A, and explain-a-line.
- **u10b:** Part 1 form B and mini-boss B.
- **u10c:** Part 1 form C and the spaced re-check items.

---

# 4. Concept introduction map

Generated by `design/curriculum_v2_gate.py`, which runs the harness tokenizer over representative code for all
260 planned items in course order.

| Path | Violations |
|---|---|
| CORE | 0 |
| CRIT (the campaign-critical path) | 0 |
| FULL | 0 |
| M1 (Units 1–3 plus "Before the cabin door") | 0 |
| READY (the Readiness Check with no Strings items) | 0 |
| TRIALS (each set against its unlock ceiling) | 0 |

`docs/intro-to-python/prototypes/concept_map.json` has one entry per package prefix (§7), so `harness.py u05b` can
gate a package before the earlier ones exist. It uses **harness tokens only**. Each entry lists every token first
taught by any item in that package, including optional and pool items, because the harness gate walks every item.
The core-only rule (§2.12 rule 2) is checked by the gate script, not by the harness.

**Changes from v1:**
- `attr:capitalize` moves to **6A-08** (Unit 3).
- `node:FunctionDef`, `node:Pass` and `node:Return` move to Unit 3, before lists.
- `op:USub` moves to 3A-03 (3A-04 was merged into it).
- `node:AugAssign`, `const:multiline_str`, `attr:count`, `node:DefaultArg` and `node:KeywordArg` are now
  pool-only.
- `node:Assert` enters at 2-A2 (optional).

| Token | First on the core path | First on the critical path | First on the full path (if earlier) | Concept |
|---|---|---|---|---|
| `call:print` `const:str` | 1A-01 | 1A-01 | 1W-02 (K) | print, text |
| `node:Assign` | 1B-01 | 1B-01 | | `name = value` |
| `const:int` | 1B-03 | 1B-03 | | whole numbers |
| `op:Add` `op:Sub` `op:Mult` `op:Div` | 1C-01 | 1C-01 | | arithmetic; `op:Mult` on text at 1C-08 |
| `call:str` | 1C-06 | 1C-06 | | `str()` before `+` |
| `const:multiline_str` | *pool only* | — | 1A-07 (pool) | `"""…"""` |
| `node:AugAssign` | *pool only* | — | 1C-05 (pool) | `+=` (checks accept it everywhere) |
| `op:Pow` `op:Mod` `op:FloorDiv` | *optional only* | — | 1-A2 | Clock Math |
| `call:input` | *optional only* | — | 1-A3 | `input()` |
| `call:int` | 8B-03 | — | 1-A3 | `int("48")` |
| `const:bool` `op:Gt` `op:Lt` | 2A-01 | 2A-01 | | True / False |
| `op:Eq` `op:NotEq` | 2A-02 | 2A-02 | | `==` `!=` |
| `op:GtE` `op:LtE` | 2A-03 | 2A-03 | | boundaries |
| `attr:lower` | 2A-04 | 2A-04 | | case-safe compare (D3) |
| `node:If` | 2B-01 | 2B-01 | | if / elif / else |
| `op:And` `op:Or` `op:Not` | 2B-06 | *(SC, not on the critical path)* | | logic |
| `node:Import` `import:random` `attr:randint` | 2B-07 | 2B-07 | | dice |
| `node:Match` | *optional only* | — | 2-A1 | match / case |
| `node:Assert` | *optional only* | — | 2-A2 | Mar'tu's seal |
| `node:FunctionDef` | 6A-01 | 6A-01 | | def |
| `node:Pass` | 6A-03 | 6A-03 | | pass |
| `node:Return` | 6A-06 | 6A-06 | | return |
| `attr:capitalize` | 6A-08 | 6A-08 | | `.lower()` then `.capitalize()` |
| `node:List` | 3A-02 | 3A-02 | | lists |
| `node:Subscript` `op:USub` | 3A-03 | 3A-03 | | `x[0]`, `x[-1]`, later `d["k"]` |
| `attr:append` | 3A-05 | — | | `.append` |
| `call:len` | 3A-06 | 3A-06 | | `len` |
| `call:range` `call:list` | 3B-01 | — | | ranges |
| `node:Slice` | 3B-02 | — | | slices |
| `call:sorted` `attr:sort` | 3B-03 | — | | sorting, `None` |
| `attr:count` | *pool only* | — | 3B-04 (pool) | `.count` |
| `attr:insert` `attr:pop` `attr:remove` | *optional only* | — | 3C | |
| `op:In` | 4A-06 | 4A-06 | 3C-02 (O) | membership |
| `call:max` `call:min` `call:sum` | *optional only* | — | 3C-03 | |
| `node:Tuple` | *optional only* | — | 3-A1 (also 5-A1, 6-A3) | tuples |
| `call:zip` | *optional only* | — | 3-A2 | |
| `node:Dict` | 4A-02 | 4A-02 | | dictionaries |
| `op:NotIn` | 4A-06 | 4A-06 | | `not in` |
| `attr:get` | *optional only* | — | 4-A1 | `.get` |
| `node:For` | 5A-01 | 5A-01 | | for loops |
| `node:While` | 5B-01 | — | | while |
| `node:Break` | 5B-03 | — | | break |
| `node:Continue` `node:ListComp` `node:IfExp` | *optional only* | — | 5C | |
| `attr:items` `attr:keys` `attr:values` | *optional only* | — | 5-A1 | |
| `const:None` | 6C-04 | 6C-04 | | the literal `None` (the campaign's placeholder) |
| `node:DefaultArg` `node:KeywordArg` | *pool only* | — | 6B-08 (pool) | defaults and keywords |
| `node:Lambda` / `call:map` | *optional only* | — | 6-A1 / 6-A2 | |
| `const:escape` | 8A-06 | — | | `\" \n` |
| `attr:upper` `attr:title` | 8B-01 | — | | case methods |
| `attr:split` `attr:join` | 8B-03 | — | | split, join |
| `attr:strip` `attr:replace` `attr:find` | 8B-05 | — | | clean-up |
| `node:FString` | 8B-07 | — | | f-strings |

**Never introduced** (out of scope; the gate keeps them out): `node:Set`, `node:DictComp`, `node:Try`,
`node:Global`, `node:Starred`, `node:With`, `node:Class`, `op:Is`, `op:IsNot`.

## 4.2 Skill gates with no harness token

The tokenizer can't see these campaign idioms, so they are gated by lesson order and skill tags. Directive Q11
approves three pseudo-tokens now. They go into `concept_map.json` only once the harness emits them; until then
they stay out, because the file must use harness tokens only.

| Idiom (skill tag) | First taught | Pseudo-token | Status |
|---|---|---|---|
| `"█" * n` (`repeat-string`) | 1C-08 | `pattern:StrRepeat` | approved |
| `a["x"]["y"]` / `a[3][1]` (`dict-nested`, `list-nested`) | 3A-09 (list), 4B-01 (dict) | `pattern:NestedSubscript` | approved |
| a function name used as a value, outside a call (`func-as-value`) | 6C-01 | `pattern:FuncValue` | approved |
| list of dicts (`list-of-dicts`) | 4B-03 | — | — |
| store-then-pass | 6A-06 / 6A-08 | — | — |
| return a comparison | 6A-09 | `pattern:ReturnCompare` | later |
| early `return` | 6B-05 | `pattern:EarlyReturn` | later |
| `d["k"](x)` (`call-stored-func`) | 6C-03 | `pattern:CallOnSubscript` | later |

---

# 5. Campaign Readiness Check (operationalizing "arriving in the ZPD")

## 5.1 What it measures

A student is ready when they can (research §4.1):
- **read and explain every line** of a campaign part's starter code,
- **write the one-line edits unaided**, and
- **complete a whole part using only the campaign's built-in support**,

with the multi-concept composition in `hold-the-barrier` as a real but winnable stretch.

**Independent of Strings (T1).** No item uses a token that Unit 9 introduces; the READY gate path proves it. Chain
methods are covered with 6A-08's `.lower()` / `.capitalize()`. The check is practice only, never a grade (Q9).

## 5.2 Format

| Part | Time | Support | Representation (format) |
|---|---|---|---|
| **Part 1**: 13 items, unaided | ~28 min | No hints, tracer, Another way or Assemble it. **Glossary, read-aloud and the explainer stay on** (G1 R25). Code answers are typed. **Every typed item is behavior-checked** (CMB, PAR, BND, CALL), never OUT alone (T5). | `rc-part1-<form>` (`testout`, the 9 code items, `support="none"`) + `rc-part1-<form>-questions` (`quiz`, the 9 predict / mc / explain items) |
| **Part 2**: the mini-boss | ~15 min | **Campaign mode for everyone** (§2.10): numbered comments, check messages, the explainer, Compare after 5 min, hints capped at rung 2. No Assemble it, tracer or Start me off. | `rc-miniboss-<form>` (`project`, `support="light"`, campaign-mode flag) |
| **Explain a line you wrote** | 1 min | One click (G4 R24, for everyone) | `rc-explain` (`quiz`). The prototype asks about the reference line `ward["effect"](hero)`; picking a line from the student's own code is UI work. |
| **Review routing** | ~15 min (contingent) | Per missed skill, in a different representation | links into the unit items |
| **Spaced re-check** | ~12 min, before Module 2 or about a week later | Unaided | `rc-recheck` (`testout`) |

There are **three parallel forms** of Part 1 (A, B, C) and **two of the mini-boss** (A, B), so a retake never
repeats an item. Each form changes names and values, never the skill.

**Explainer parity.** Until the explainer port lands in the campaign, the review screen says: "The campaign's
error messages are shorter than Mar'tu's. Read the last line first, the same way."

## 5.3 Part 1 items (form A; our world, never the campaign's exact code)

| # | Item | Type | Skill tags | Prepares | Fails on (evidence) |
|---|---|---|---|---|---|
| 1 | Predict `print("Mana: " + str(7) + "/" + str(10))` → `Mana: 7/10` | predict | `concat-str` | `mana-bars` return line | `Mana:7/10`, `Mana: 7 / 10` |
| 2 | **Campaign-style starter** (G3 R18): `def step_west():` / `    pass`. "Replace `pass` with a command that moves the scout west." | code | `replace-pass` | `program-movement` | `scout.step(west)` → crash; `"east"` → CALL |
| 3 | `get_warning()` tidies its line with `.lower()` then `.capitalize()`. (a) One click: what will the board show? (b) Finish `present_warning()`: store the result of `get_warning()` in a variable, then pass that variable to `show_on_ley_board()`. Campaign-style `pass` starter. | predict + code | `chain-methods`, `store-then-pass` | `program-dialogue-prompt`, `show_mana` | a typed line → CMB; no store → STO; no `()` → CALL |
| 4 | (a) `latch_check(roll)` with `needed = 11` and `return roll >= needed`: True or False for 10, 11 and 12. (b) The ledger shape (`ward_strength`-style) with new numbers. | predict ×2 | `boundary`, `return-comparison`, `trace-call` | `skill-checks` | 11 → False; the 15-type and 7-type values |
| 5 | (a) Trace a three-branch `if/elif/else` on `choice == "option 2"`: which line runs? (b) Mend `elif choice == option 3:`. | predict + code | `elif-chain`, `quote-text` | `program-dialogue-options` | first branch; left unquoted → crash |
| 6 | Given a hero sheet: (a) read `hero["mana"]`; (b) read `hero["abilities"]["wisdom"]`; (c) write `book[spell_name] = spell`; (d) True or False for `"Glow" in book`. | code (a–c, CMB/KEY) + predict (d) | `dict-read`, `dict-nested`, `dict-write`, `dict-in`, `dict-key-from-variable` | `spell-book`, `hold-the-barrier` | `hero["wisdom"]`; `book["spell_name"]`; `2 in book` → True |
| 7 | (a) Predict `"█" * 3 + "░" * 2`. (b) Mend `"░" * 10 - 3` (blocks pre-typed). | predict + code | `repeat-string` | `mana-bars` | `█3░2`; no parentheses |
| 8 | (a) Which values can `random.randint(1, 6)` return? (b) **Campaign-style starter:** `def roll_die(die_size):` / `    return 1`. Replace `return 1` with a random number from 1 to `die_size`. | mc + code | `randint`, `randint-param` | `skill-checks` | 1–5; `randint(1, 6)` → RND |
| 9 | **Explain:** the difference between `spells["glow"]` and `spells["glow"](hero)`. Choose the right plain-English sentence, then predict the output. | explain + predict | `func-as-value`, `call-stored-func` | `spell-book`, `hold-the-barrier` | "both run the spell" |
| 10 | Trace `for hero in roster: show_status(hero)` over 3 hero dicts: how many calls, and with what? Then explain what the loop does (one click). | trace + explain | `list-of-dicts`, `for-each` | the bottom loops of `spell-book` and `mana-bars` | "one call with the whole roster" |
| 11 | Read three tracebacks (`KeyError: 'dexterity'`; `TypeError: can only concatenate str (not "int") to str`; `NameError: name 'mana_cots' is not defined`) and mend each one-line bug. | code (3 CPs) | `read-traceback` | every part | each left |
| 12 | **Typed** (G2 R17): "Spend `cost` from `hero["mana"]`." The check reruns with another cost and another starting mana (CMB). | code | `dict-write`, `reassign`, `combine-values` | `hold-the-barrier` | `hero["mana"] = 17` → CMB; `hero["mana"] - cost` with no store |
| 13 | **New (directive §4.6):** "Write `glug_cost(sips, price_per_sip)`, which hands back the total." An Example `def triple(n): result = n * 3; return result` is on screen. | code | `param-use`, `return-right-name`, `exact-names` | every part with parameters | `return result` → RNM; `return sips * 2` → PAR; `price * sips` → PNM; a literal → PAR-CONST |

Forms B and C reuse the skills with new names and data:
- Form B: `step_east`, `get_farewell`, `dodge_check` (needed 14), `option 3`, a d8, `shield_cost(...)`, and so on.
- Form C: Gearshift's fuel sheet, `option 4`, and so on.

## 5.4 Part 2: the mini-boss

**Form A, "Hold the Lantern Ward":** `cast_ward(hero, ward_name)`. This is the near-transfer of
`hold-the-barrier`, with different names and data. **Form B, "Hold the Glow Ward":** `use_ward(caster, ward)` with
other heroes and costs.

**Given:**
- the guard clause (`if ward_name not in hero["wards"]: …; return`);
- `ward = hero["wards"][ward_name]`;
- a finished `show_mana(hero)` helper;
- numbered comments in the campaign's phrasing, 1:1 with the checkpoints.

**The student writes the `if/elif/else`:**
- the nested affinity check;
- the `<` mana check;
- the stored-effect call `ward["effect"](hero)`;
- the subtraction;
- the redraw.

**Six checks, mirroring the campaign's:**
1. skilled, with enough mana, casts;
2. the bar updates;
3. low affinity doesn't cast;
4. low mana doesn't cast;
5. exactly enough mana still casts;
6. the ward's own cost is used.

**Campaign mode for everyone** (T4). The 6C-05 More-structure ladder is not offered here. "Hard mode" (a
signature only, plus an extra branch) is Tier 3.

## 5.5 Pass heuristic (tunable, research §4.5)

| Result (neutral names) | Rule | What happens |
|---|---|---|
| **Ready** | Part 1 ≥ 11/13, with item 6 at ≥ 3 of 4 parts and item 13 passed, **and** the mini-boss passes all 6 checks in campaign mode without Compare | The "Ready for Module 2" milestone. Each skill is shown solid on the map. |
| **Ready, with a review list** | Part 1 9–10/13, **or** the mini-boss passed only after Compare (and its immediate twin) | Go on to the campaign with "Mar'tu's notes": the missed skills, each linked to its review exercise and one parallel item. The teacher sees the flags. |
| **Review first** | Part 1 ≤ 8/13, **or** the mini-boss not passed | Targeted review for each missed skill in a **different representation** (Assemble it, the trace table, a worked example), then parallel items from another form. After two review cycles the student continues anyway, with a teacher flag ("Needs you now"). The story never blocks. |

**Per-part readiness** (research §4.4). The "Prepares" column gives the teacher a per-campaign-part view:
- **Band A (unaided):** `program-movement`, `program-dialogue-prompt`, `skill-checks`.
- **Band B (with built-in support):** `spell-book`, `mana-bars`, `hold-the-barrier`.

## 5.6 Spaced re-check (before Module 2)

The re-check holds:
- **for everyone** (G4 R8): typed items on `combine-values`, `exact-names`, `param-use` and `return-right-name`,
  the class-wide sheet errors (u10c `rc-recheck`);
- parallel items for 4, 6 and 9;
- each student's misses.

Tested-out skills are re-verified here too, so a Quick Check pass never stands unverified. A miss reverts the
skill to "practicing".

## 5.7 Confirmed in the campaign itself

The ZPD target is met when campaign telemetry shows, per part:
- 2–6 runs, with different errors and recovery;
- mostly rung 1–2 hints;
- at most one Show solution per module;
- the student can explain a line they wrote.

**Signals in the red** (8 or more runs; the same error 3 or more times; reveals on most parts) mean the course
under-prepared that skill. **Signals in the blue** (1 run on every part; no hints ever) mean the campaign sits
below the zone, so offer the instructions-light toggle (research §4.2; a later campaign change).

---

# 6. Time ledger, campaign-critical path, release gates

Planning assumption **[OWNER Q3]:** 45–50 minute periods, with about **40 working minutes** each.

## 6.1 Time ledger (minutes, from `design/curriculum_v2_gate.py`)

| Unit | Core | of which CC | Contingent (expected use) | Pool | Optional | G1 estimate | G4 estimate |
|---|---|---|---|---|---|---|---|
| 1 Hello World | 109 | 77 | 4 (1W, ~80% → 3) | 27 | 62 | 108 critical + 3 + twins | ~34 (QC1 12 + capstones 10 + 1P1 Trial 12) |
| 2 Control Flow | 105 | 64 | — | 26 | 67 | 90 critical + twins | ~79 (0.75×) |
| 3 Functions I | 68 | 64 | 3 (6A-05a, ~60% → 2) + **10 (M1 cabin door)** | 9 | 12 | 90 critical + 2 + 6A-T twins | ~54 (0.8×; QC-R1 is honest, so few skip) |
| 4 Lists | 51 | 15 | — | 31 | 88 | 21 critical | ~36 (0.7×) |
| 5 Dictionaries | 90 | 51 | — | 27 | 20 | 71 critical | ~68 (0.75×) |
| 6 Loops | 79 | 21 | — | 18 | 42 | 29 critical | ~55 (0.7×) |
| 7 Functions II | 105 | 77 | — | 25 | 42 | 108 critical | ~84 (0.8×) |
| 8 Trials | — | — | — | — | 335 | — | early-finisher time |
| 9 Strings | 60 | 0 | — | 18 | 110 | (deferred) | ~42 (0.7×) |
| 10 Readiness | 56 | 56 | 15 (review routing, ~50% → 8) | — | — | 78 critical + 8 | ~45 (0.8×) |
| Mar'tu moments (5 × 2) | 10 | 10 | | | | 10 | 10 |
| **Total** | **733 ≈ 18.3 periods** | **435** | **≈ 13 expected (+10 under M1)** | 181 | 443 | **≈ 609 critical + ≈ 50 contingent and twins ≈ 660 ≈ 16.5 periods** | **≈ 507 ≈ 12.7 periods** |

- **Core ≤ 740** ✓ (733, including the Readiness Check and the Mar'tu moments).
- **G1 (×1.4).** The critical path takes ≈ 609 min. With contingent help, twins and More structure (estimated at
  about 8% of the critical path, ≈ 35 min, plus 1W, 6A-05a and review routing), G1 reaches the Readiness Check
  in ≈ 660 min ≈ 16.5 periods. That leaves ≈ 80 min of the window, about 57 typical minutes of syllabus-core items
  at 1.4×: the unit quizzes and the first projects.
  - G1 students **defer** most of Strings, 3B, 5B and the later projects, using the teacher's switch. Strings can
    be done after Module 2 starts.
  - This is honest: G1 reaches campaign readiness on time, and not the whole syllabus.
- **G4** (G4 R9 wording): "most of Unit 1 by QC1; Units 2–7 at about 0.7–0.8× through capstone-first and light
  mode." That is ≈ 12.7 periods, leaving ≈ 6 periods for the Trials, side quests and the Extra practice pool.
- **If fewer periods are available** (Q3): use Route M1 and run Strings after Module 2 starts. The core without
  Strings is 673 min ≈ 16.8 periods.
- **Item mix compared with the syllabus** (14 lessons, 14 projects, 13 quizzes):

  | | Lessons | Projects | Quizzes | Articles | Other |
  |---|---|---|---|---|---|
  | v2 core | 17 | 5 | 8 (+ the warm-up recall items) | 1 card | 1 Readiness Check |
  | v2 optional and pool | 3 (1W, 3C, 5C) + 9 Extra practice | 6 | 2 (+ the QC question forms) | 11 | 8 Quick Checks × 2 forms, 33 challenges, 9 cheatsheets |

- **Recalibrate after Unit 1** (T13): compare these minutes with the real logs, then retune the thresholds (3
  failed runs, 4 min, 90 s, 10 s rung spacing) and the 8% contingent estimate.

## 6.2 The campaign-critical path

The **critical path** is every CC item plus the Readiness Check, in course order. It is the path a deferred
student walks. The CRIT gate path proves that it is self-contained: no CC item uses a token that only SC items
teach. (One fix was needed: the 4B warm-up had used `and`, which is SC, and now uses a return-comparison item.)

| Unit | CC items (ids) | Min |
|---|---|---|
| 1 | 1-A1; 1A-01, 1A-02, 1A-03, 1A-04, 1A-05, 1A-08, 1A-S; 1B (all, with remembers); 1C-R, 1C-01, 1C-02, 1C-03, 1C-04, 1C-06, 1C-07, 1C-08, 1C-S | 77 |
| 2 | 2A-R, 2A-01–2A-04, 2A-S; 2B-R, 2B-01–2B-05, 2B-07, 2B-08, 2B-S; 2C-R, 2C-01, 2C-06, 2C-07, 2C-S | 64 |
| 3 | 6A (all but 6A-11), Quiz 6A | 64 |
| 4 | 3A-R, 3A-02, 3A-03, 3A-06, 3A-S | 15 |
| 5 | 4A-R, 4A-02–4A-07, 4A-S; 4B-R, 4B-01, 4B-03, 4B-04, 4B-05, 4B-S | 51 |
| 6 | 5A-R, 5A-01, 5A-02, 5A-03, 5A-07, 5A-S | 21 |
| 7 | 6B (all but 6B-10), 6C (all but 6C-06), Quiz 6B | 77 |
| 10 | Part 1, Part 2, explain-a-line, spaced re-check | 56 |
| — | the five Mar'tu moments | 10 |
| **Total** | | **435 ≤ core ÷ 1.4 = 524 ✓** |

Nothing pushes the path over. **If periods are cut further, trim inside projects (task groups) first:**
- 1P1 group C down to its echo task;
- 2P1 to tiers plus "Tell it";
- 4P group C;
- 6P group B;
- 5P group B.

That saves about 25 min, and no CC skill is removed.

## 6.3 Release gates (directive §6, mapped to v2 unit numbers)

Gates: **U1** = Unit 1 · **U2** = Unit 2 · **R-I** = Unit 3 · **L** = Unit 4 (Lists) · **D** = Unit 5 ·
**R-II** = Unit 7 · **RC** = Unit 10 · **T3** = later.

| Feature | Cost | Gate |
|---|---|---|
| Explainer precedence tree with the Unit 1 rows, plain titles, "One fixed" (§2.6) | S–M | **U1** |
| BARE, SWAP / LINE-TOTAL, NEWBOX, OUT diff, NAME extended, CMB rerun table, `foreign_names` / LEFT | M | **U1** |
| Lints (a), (c), (e), (f), (g); QC coverage lint (d) for QC1 | S | **U1** |
| Help stack: rung 0, Point always, highlight offers, silent stall, immediate twin, rung spacing | M | **U1** |
| "Names to use" chips; the symbol tray and pre-typed blocks | S | **U1** |
| Preset logic (the first-visit question, fading on performance only) | S | **U1** |
| QC1 rewrite with 2 forms, "not yet" for untested skills, lesson-level capstone conversion | M | **U1** |
| Neutral error panel; quiz review with right answers first; echo spots with the teacher switch | S | **U1** |
| Static step tables in place of the tracer (1B-05, 1C-04) | S (content) | **U1** |
| New exercise fields (`starter_level`, `path`, `skills`, `solo`, `dictates`, `foreign_names`, `par`, `twin`, checkpoint `start`) in the schema and exporter; until then the `meta:` line in `notes` | S–M | **U1** |
| Exercise-level QC routing; Trial-mode projects | M | U2 |
| Try other numbers button; point-at-it inline mc (retrofit 1C-08) | S–M | U2 |
| Capstone-first | M | U2 |
| Auto-derived More-structure levels | M | U2 |
| Classroom: Needs you now and the unit grid (server mode) | M | U2 |
| Trace-table item type (6A-06b; retrofits 1C-04, 5A-04, Quiz 6A, Readiness) | M | **R-I** |
| PNM, fuzzy RNM, PAR-CONST, RET-PARAM, the None notice, PAR-collision lint (b) | S–M | **R-I** |
| "Before the cabin door" (Route M1) and the Route M1/M2 teacher setting | S | **R-I** |
| Mastery map v1 (3 levels, together and solo); predict-calibration topics | M | **L** |
| Live tracer (nested boxes, call/return arrow), auto-open on a wrong predict | L | **D** (static tables until then) |
| 6C-05 hand-authored ladder; campaign mode | S–M | **R-II** |
| Campaign-readiness panel; spaced re-check | M | **RC** |
| Port the explainer and the None notice to the campaign (separate PR, campaign tests updated) | M | before Module 2 |
| Two seats on one device | M–L | only if devices are shared [OWNER] |
| Mar'tu's slate; hero persistence; the reaction pool; hard mode; extra refactor Trials | M | T3 |
| Per-student recipe track; apprentice role in software; clickable tour | — | **declined** |

**Engineering hand-off for the U1 gate** (directive §7 step 9):
1. The explainer rows in §2.6 with Unit 1 proofs, plus `explain.test.ts` precedence tests.
2. The check helpers in `course_helpers.py` (`_rerun`, `_near_names` with plurals, BARE, SWAP, NEWBOX, OUT diff),
   plus harness lints (a), (c), (e), (f), (g) and (d) for QC1.
3. The help stack in ExercisePlayer.
4. Chips, the symbol tray, and the preset logic.
5. QC1 forms and conversion.
6. The neutral panel and the quiz review order.

Every new row and pattern is proven by a harness wrong answer from §3, Unit 1.

## 6.4 Measure after the first class (T13)

Log these:
- the help rung or angle that came right before a pass;
- silent-stall offers accepted versus dismissed;
- each QC pass against the same skill's later Readiness item;
- predict accuracy per skill;
- real minutes per item.

After Unit 1, the designer and the teacher compare §6.1 with the logs and recalibrate.

---

# 7. Prototype work packages

One prototype file per package, in course order. File order is the concept-gate order, and each package's
`introduces` is in `concept_map.json`. "Ex." counts exercises, projects, challenges and Quick Check code tasks
(both forms), with quizzes listed separately. Every package repeats its unit's `UNIT` dict
(`id`, `order`, `title`, `subtitle`, `martu_intro`, `goals`, `campaign_links`).

| Prefix | File | Unit (`id`, order) | Items, in order | Ex. | Introduces |
|---|---|---|---|---|---|
| u01a | `u01a_hello_world_quotes.py` | `hello-world`, 1 | 1-A1 card; 1W (1W-02, 1W-04); 1A (1A-01–06, 1A-08, 1A-S) | 10 | `call:print` `const:str` |
| u01b | `u01b_hello_world_boxes.py` | `hello-world` | 1b-remembers; 1B (1B-01–06, 1B-S); 1X-AB (1A-07, 1B-T) | 9 | `node:Assign` `const:int` `const:multiline_str` |
| u01c | `u01c_hello_world_math_glue.py` | `hello-world` | 1c-remembers; 1C (1C-01–04, 1C-06–09, 1C-S); 1X-C (1C-05, 1C-T); Quiz 1; 1P1 | 12 + quiz | `op:Add` `op:Sub` `op:Mult` `op:Div` `call:str` `node:AugAssign` |
| u01d | `u01d_hello_world_extras.py` | `hello-world` | 1P2; 1-A2 (try-it); 1-A3 (try-it); QC1 forms A, B (+ question quizzes); Cheatsheet 1 | 13 + 2 quizzes | `op:Pow` `op:Mod` `op:FloorDiv` `call:input` `call:int` |
| u02a | `u02a_control_flow_booleans.py` | `control-flow`, 2 | 2a-remembers; 2A (2A-01–05, 2A-S) | 6 | `const:bool` `op:Gt` `op:Lt` `op:Eq` `op:NotEq` `op:GtE` `op:LtE` `attr:lower` |
| u02b | `u02b_control_flow_if.py` | `control-flow` | 2b-remembers; 2B (2B-01–09, 2B-S); 2-A1 (try-it); Quiz 2; 2P1 | 12 + quiz | `node:If` `op:And` `op:Or` `op:Not` `node:Import` `import:random` `attr:randint` `node:Match` |
| u02c | `u02c_control_flow_errors.py` | `control-flow` | 2P2; 2c-remembers; 2C (2C-01, 05, 06, 07, 2C-S); 2X (2C-02, 03, 04); 2-A2 (try-it); QC2 A, B (+ questions); Cheatsheet 2 | 14 + 2 quizzes | `node:Assert` |
| u03a | `u03a_first_recipes.py` | `first-recipes`, 3 | 6a-remembers; 6A (6A-01–05, 6A-05a, 6A-06, 6A-06b, 6A-07–11, 6A-S); Quiz 6A | 14 + quiz | `node:FunctionDef` `node:Pass` `node:Return` `attr:capitalize` |
| u03b | `u03b_first_recipes_checks.py` | `first-recipes` | 3X (6A-T1–T3); cabin-door (2) + cabin-door-questions; QC-R1 A, B (+ questions); Cheatsheet 3 | 13 + 3 quizzes | — |
| u04a | `u04a_lists.py` | `lists`, 4 | 3a-remembers; 3A (3A-01, 02, 03, 05, 06, 07, 09, 10, 3A-S); 3b-remembers; 3B (3B-01–03, 3B-S); Quiz 3 | 13 + quiz | `node:List` `node:Subscript` `op:USub` `attr:append` `call:len` `call:range` `call:list` `node:Slice` `call:sorted` `attr:sort` |
| u04b | `u04b_lists_extras.py` | `lists` | 4X (3B-04, 3B-05); 3P1; 3C (3C-01–03); Quiz 3B; 3-A1; 3-A2; 3P2; QC3 A, B (+ questions); Cheatsheet | 13 + 2 quizzes | `attr:count` `attr:insert` `attr:pop` `attr:remove` `op:In` `call:max` `call:min` `call:sum` `node:Tuple` `call:zip` |
| u05a | `u05a_dictionaries_sheets.py` | `dictionaries`, 5 | 4a-remembers; 4A (4A-01–08, 4A-S); 4-A1 (try-it) | 10 | `node:Dict` `op:NotIn` `attr:get` |
| u05b | `u05b_dictionaries_nested.py` | `dictionaries` | 4b-remembers; 4B (4B-01–06, 4B-S); Quiz 4; 4P; 5X (4A-T, 4B-T) | 10 + quiz | — |
| u05c | `u05c_dictionaries_quick_check.py` | `dictionaries` | QC4 A, B (5 code tasks each, + questions); Cheatsheet | 10 + 2 quizzes | — |
| u06a | `u06a_loops.py` | `loops`, 6 | 5a-remembers; 5A (5A-01–08, 5A-S); 5b-remembers; 5B (5B-01–04, 5B-S); Quiz 5 | 14 + quiz | `node:For` `node:While` `node:Break` |
| u06b | `u06b_loops_project.py` | `loops` | 5P; 6X (5B-05); 5C (5C-01–04); 5-A1 (try-it); QC5 A, B (+ questions); Cheatsheet | 13 + 2 quizzes | `node:Continue` `node:ListComp` `node:IfExp` `attr:items` `attr:keys` `attr:values` |
| u07a | `u07a_spell_recipes_sheets.py` | `spell-recipes`, 7 | 6b-remembers; 6B (6B-01–07, 6B-10, 6B-S) | 9 | — |
| u07b | `u07b_spell_recipes_hand_over.py` | `spell-recipes` | 6c-remembers; 6C (6C-01–06, 6C-S); Quiz 6B; 6P | 8 + quiz | `const:None` |
| u07c | `u07c_spell_recipes_extras.py` | `spell-recipes` | 7X (6B-08, 6B-09); 6-A1, 6-A2, 6-A3 (try-its); QC-R2 A, B (+ questions); Cheatsheet | 13 + 2 quizzes | `node:DefaultArg` `node:KeywordArg` `node:Lambda` `call:map` |
| u08a | `u08a_trials_control_lists.py` | `code-challenges`, 8 | T-HCL; T-CF-1/1a/2/2a/3/3a; T-L-1/1a/2/2a/3/3a | 13 | — |
| u08b | `u08b_trials_dicts_loops.py` | `code-challenges` | T-D-1/1a/2/2a/3/3a; T-Lo-1/1a/2/2a/3/3a | 12 | — |
| u08c | `u08c_trials_functions.py` | `code-challenges` | T-F-1/1a/2/2a/3/3a; T-Own, T-Own-a; Cheatsheet "How to read a test table" | 8 | — |
| u09a | `u09a_strings.py` | `strings`, 9 | 8a-remembers; 8A (8A-01, 03, 06, 07, 8A-S); 8b-remembers; 8B (8B-01, 02, 03, 05, 07, 08, 09, 8B-S); Quiz 8B | 13 + quiz | `const:escape` `attr:upper` `attr:title` `attr:split` `call:int`* `attr:join` `attr:strip` `attr:replace` `attr:find` `node:FString` |
| u09b | `u09b_strings_projects.py` | `strings` | 9X (8A-04, 8A-05, 8A-08) + Quiz 8A; 8P1; 8P2; QC8 A, B (+ questions); Cheatsheet | 11 + 3 quizzes | — |
| u10a | `u10a_readiness_form_a.py` | `readiness-check`, 10 | intro card; Part 1 form A (9 code + questions); mini-boss A; explain-a-line | 10 + 2 quizzes | — |
| u10b | `u10b_readiness_form_b.py` | `readiness-check` | Part 1 form B (9 code + questions); mini-boss B | 10 + quiz | — |
| u10c | `u10c_readiness_form_c.py` | `readiness-check` | Part 1 form C (9 code + questions); the spaced re-check (4 typed items) | 13 + quiz | — |

\* `call:int` is first used on the core path in 8B-03, which must list it in `introduces`. `concept_map.json`
records it under u01d, where the optional 1-A3 introduces it first on the full path.

**Notes for prototypers:**
- Each package names its `concept_map.json` predecessors. Run `harness.py <prefix>` until it reports 0 errors.
- Every exercise needs the `meta:` line (§2.12 rule 14) until the schema has the new fields.
- `wrong_answers` cite sheet IDs in `notes` only.
- Quick Check forms are separate `testout` items (`qcN-a`, `qcN-b`) with `support="none"`. Their questions are
  separate `quiz` items.
- Pool lessons set `optional=True`.
- Contingent items (1W, 6A-05a) are core lessons or exercises whose display is gated by the preset or signal. In
  the prototype they are ordinary items, with the trigger recorded in `meta:`.
- u02a is short (6 exercises): 2A is a 20-minute lesson, adding 2B (10) would pass 14, and a lesson can't be
  split across files.

---

# 8. Open questions for the real teacher [OWNER]

1. **D11, Recipes early.** Approve moving Functions I (6A + Quiz 6A) to right after Control Flow for the whole
   class? If not: the v1 order, with the fast lane as a class option and still no per-student tracks.
2. **Module 1 status and route.** Has the class played Module 1's coding parts? If not, we recommend **Route M1**
   (Units 1–3, "Before the cabin door", Module 1, then the rest). If yes, **Route M2**, and the rehearsals serve as
   review.
3. **Periods available.** The core is planned at ≈ 18.3 periods (40 working minutes each). If fewer: use Route M1
   and run Strings after Module 2 starts (≈ 16.8 periods).
4. **Spoilers.** Default: Bomb Shell and Lucky stay. The course never shows `Strengthen Magic`, the red-clock
   event, or campaign function names. The 5B-04 forecast shows 32 hours (Module 2's last line). Keep it?
5. **Server mode in class.** Does the class run the site in server mode during periods? It is needed for "Needs
   you now" and "Ready for more". Static export covers home practice only.
6. **Devices.** One device per student, or shared devices? Only shared devices need two seats on one device.
7. **IDLE.** Is a local Python available for 8P2? Until we know, it stays browser-only.
8. **Names.** Are the project and unit names (Night Watch Ledger, Road Encounter Table, Ledger of Heroes, Velocite
   Watch, Resonance Array, Water-Stained Log, Institute Cipher, Trials of the Yard, The Hard-Coded Ledger, Before
   the cabin door, Mar'tu's Seal) acceptable in your world? Can Mar'tu reference their Institute past this
   freely?
