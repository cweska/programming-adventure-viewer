# Teacher directives: curriculum v1 → v2

**From:** the teacher agent (classroom lead for this campaign), acting on the real teacher's stance.
**To:** the curriculum designer (and the engineers building the course shell).
**Inputs processed:** `design/curriculum-v1.md` (all of it), the four reviews in `reviews/curriculum-*.md`,
`personas/personas.md`, `research/zpd-principles.md`, `research/codecademy-mechanics.md`, `design/architecture.md`,
`context/brief.md`, `context/campaign-python-inventory.md`, and the harness docstring.
**Spot-checked in CPython 3.13.18:** the error messages behind every "must" that depends on Python's wording
(multi-word unquoted text, space in a name, mixed quotes, `5P`, empty `def` body, parameter near-miss, keyword
"Did you mean", `error_type = NameError`). All the reps' claims held, with one correction: a missing comma inside
a multi-line dict is reported on **either** the line missing the comma (int value: "Perhaps you forgot a comma?")
**or** the next line (string value: plain "invalid syntax"). The explainer row must name both lines (§4.1).

**Markers.** **[OWNER]** marks a decision the real teacher must confirm before it ships. Everything else is decided
here, and the designer should apply it in v2 without asking again.

---

## 0. The ten directives that matter most

1. **Time is a hard constraint.** The core is about 18.5 periods. The lean core becomes the core. Every core
   addition is paid for with a cut, or appears only when a student's behavior calls for it. Publish a time ledger
   and a campaign-critical path that a student working at 1.4× can finish inside the class's window (T1).
2. **Recipes early (new deviation D11) [OWNER].** Lesson 6A and Quiz 6A move to right after Control Flow, for the
   whole class. Units 3–5 carry recipe-shaped practice. Functions are the cliff for 11 of 11 students, and this
   gives them three weeks of spacing instead of one (T2).
3. **One help stack.** After a failed run, the student sees one message and one Help control. Every new support the
   reps asked for (Start me off, another angle, More structure, Assemble it, proactive offers) lives inside that
   control, never as a separate panel (T3, §4.3).
4. **Silence is a signal.** Add the 90-second "editor unchanged, no Run" trigger, make the Point rung always
   available, and put a "hasn't run code" flag on the teacher's page. Group 3 produces silence, not failed runs.
5. **Build an explainer precedence tree.** Today the "put it in quotes" NameError advice misfires on four of the
   class's exact slips. Every row ships with a harness wrong answer that proves it fires (§4.1).
6. **Checks must see meaning, not shape.** No OUT-only check on a computed value. Add BARE, SWAP, NEWBOX, PNM, fuzzy
   RNM, PAR-CONST and RET-PARAM. PAR argument sets must not collide with the task's calls. Never fail a student's
   own creative value (§4.2).
7. **Honest test-outs.** Every skill a Quick Check claims must have an item that can fail on the documented error.
   Each QC has two forms. A pass *converts* lessons into capstones and Trial-mode projects instead of deleting them.
   "Tested out" stays provisional until a typed spaced re-check confirms it (§4.5).
8. **Fade to campaign parity.** The final stretch and the Readiness mini-boss run with only the campaign's supports,
   in the campaign's vocabulary, with the same explainer the campaign uses. Port the explainer to the campaign (T4).
9. **Mastery evidence is typed, unassisted and partly solo.** Dictated, assembled or revealed passes never make a
   skill "solid". Each lesson has one checkpoint whose code isn't dictated and one short solo item. Together and solo
   are recorded separately (T5).
10. **A teacher can run it.** The classroom page shows "Needs you now", "Ready for more" and campaign readiness by
    skill. A one-page run-kit covers sync points, whole-class "Mar'tu moments" at the cliffs, structured pairing,
    and what early finishers do (T7, T8).

---

## 1. Big-picture directives the reps did not cover (or covered only for their own group)

### T1. Time budget and the time-neutral rule
- **Planning assumption until Q3 is answered [OWNER]:** 45–50 minute periods with about 40 working minutes each.
  Core ≤ 18.5 periods (≈ 740 min), including the Readiness Check.
  - **The draft's "lean core" becomes the core.** The nine trims in §6 of v1 move into an **"Extra practice"
    pool**. They are not deleted: the pool feeds twins, the spaced queue, and early finishers.
- **Time-neutral rule.** A change may add core minutes for *everyone* only if the v2 doc names the cut that pays for
  it. Otherwise it must be **contingent**: shown only on a signal (failure, stall, preset, first exposure under
  "Show me more"). Most rep asks are already contingent. Keep them that way.
- **Time ledger (new §6 table).** For each unit, list: core minutes, contingent minutes (an expected-use estimate),
  optional minutes, the G1 estimate (×1.4, with deferrals), and the G4 estimate (QC plus capstones). Re-estimate from
  real logs after the first class runs Unit 1 (T13).
- **Campaign-critical path.** Tag every core item `campaign-critical` or `syllabus-core`.
  - The critical path is the campaign-critical items plus the Readiness Check. It must fit in core ÷ 1.4 (≈ 530
    min), so a G1 student can finish it inside the class's window.
  - If it doesn't fit, report what pushes it over. Propose trims *inside projects* (task groups), never removal of a
    campaign-critical skill.
- **Immediate moves to optional, for everyone:** 1A-07 (triple quotes) and 1C-05 (`+=`). Later checks must accept
  `+=` and the long form. 1-A1 becomes a one-minute card (G1 R2).
- **Make Unit 8 (Strings) independent of the Readiness Check.** Under D11, `chain-methods` is first taught in
  Recipes I (6A-08), and the bar skills are spaced through 5A-07 and 6B-07. That lets the teacher run Strings before
  Module 2 or alongside it, which is the main pacing lever if periods are short.
- **No week calendar shown to students.** The course map shows milestones only. The teacher sets the class pace and
  holds sync points (T8).

### T2. D11 "Recipes early" [OWNER, recommended]
- **Order:** Unit 1 → Unit 2 → **Recipes I** (6A + Quiz 6A) → Lists → Dictionaries → Loops → **Recipes II** (6B, 6C,
  Quiz 6B, 6P) → Trials (optional) → Strings → Readiness. Renumber however reads best. Keep the item ids stable.
- **Fold `.lower().capitalize()` reading into 6A-08's starter.** `get_greeting()` returns an uppercase line, then
  tidies it in two lines, exactly as `get_dialogue_prompt_string()` does in Module 1. Add one Predict. This introduces
  `attr:capitalize` in Recipes I.
  - With that change, Units 1, 2 and Recipes I cover every line of Module 1. The separate 8B-02 hop disappears.
  - 8B-02 stays in Strings as revisit and spacing.
- **Spaced recipe practice in Units 3–5, by conversion, not addition.** In each unit, convert one or two existing
  exercises or project tasks into recipe-shaped versions (e.g. 3P1 `last_score(log)`, 4P `max_mana_for(affinity)`
  reused, 5P `average(values)`). Put def/return items into "Mar'tu remembers" and into each unit's quiz. The Control
  Flow Trials unlock in function form after Recipes I.
- **Routes M1 and M2 are a class-level setting** (teacher settings, §4.4), never per student.
  - **M1:** Units 1, 2 and Recipes I, then campaign Module 1, then the rest, then Module 2. M1 adds a 10-minute
    **"Before the cabin door"** check: Readiness items 2, 3 and 5 plus one chain-method predict. It is the teacher's
    signal for sending the class into Module 1.
  - **M2:** the whole core runs before Module 2's coding parts.
- **Why:** functions are the class-wide cliff, and spaced retrieval is the highest-utility technique. The draft
  already verified 6A as portable. This gives G4's "recipe track" benefit to everyone, without splitting the class
  timeline.
- **If the owner declines D11:** keep the v1 order, keep the fast lane as a class option, and still decline
  per-student tracks.

### T3. One help stack with layered defaults
The reps asked for about a dozen help features. Each is reasonable alone, but stacked on one screen they would
recreate the "wall of text at our worst moment" G1 described. The screen contract is in §4.3. It is binding on the
ExercisePlayer being built now: do not build separate floating offers, cameo-plus-offer stacks, or a second Parsons
button.

### T4. Fade to campaign parity (the ZPD target is *the campaign's* support, not ours)
- **Campaign mode.** 6C-04, 6C-05, 6P and Readiness Part 2 run with only what the campaign gives:
  - numbered comments, check messages, the explainer, and Compare after 5 minutes;
  - hints capped at rung 2, with no Assemble-it, no tracer and no auto-offered angles.
  
  Under "Show me more", 6C-05 keeps its More-structure ladder (G3 R15), but its pass is then recorded "with
  structure", and the mini-boss is campaign mode for everyone.
- **Vocabulary converges on the campaign's words.** See the terminology contract (§4.7). Rehearsal checkpoints copy
  the campaign's own phrasing: "Replace each `pass` with…", "replace each placeholder with the matching parameter",
  "Store the result of `…` in a variable", "Pass that variable to `…`".
- **Port the explainer.** The improved explainer rows and the None notice go into the campaign's `explain.ts` in a
  separate PR, with campaign tests updated. Otherwise students learn to read messages the campaign never shows them.
  Until that PR lands, the Readiness review screen says plainly that campaign messages are shorter.
- (Out of scope, recommended later: the campaign's instructions-light toggle for students "in the blue", research
  §4.2.)

### T5. Mastery evidence must be honest
- **One non-dictated checkpoint per lesson.** Each lesson has at least one checkpoint that gives the goal and "Names
  to use" but no code. Only these can make a skill **solid**, along with SOLO items, QC items and spaced items.
  Checkpoints whose text dictates the line carry `dictates: true`, and the harness enforces at least one
  non-dictated checkpoint per lesson.
- **Passes "with structure" are recorded as such.** These are passes after Parsons, Start me off, More structure or
  a reveal. An Assemble-it pass is followed by a 1–2 line typed twin (G3 R17). A reveal is followed by an immediate
  twin (G2 R20, modified).
- **Together and solo are separate positive ticks** (G3 R16). Neither is a failure.
- **Every typed QC and Readiness item is behavior-checked** (CMB, PAR, BND, CALL), never OUT alone.

### T6. Verification discipline (extends rule 2.7 #8)
- Every new explainer row and check pattern ships with:
  - a harness `wrong_answers` entry reproducing the documented slip, cited by sheet ID in `notes` only;
  - an `explain.test.ts` case;
  - for NameError, a precedence test that the right row wins.
- **New harness lints:**
  - (a) No OUT-only check on a computed value. The hard-coded literal must be a wrong answer that fails (G2 R3).
  - (b) PAR collision: no fresh argument set may give the same result as a call written in the task (G3 R14).
  - (c) `starterLevel`: the first exposure of a construct is at S3 or above, and consecutive steps drop by at most
    one level (G3 R8).
  - (d) QC coverage: each claimed skill has an item with an evidence-based wrong answer (G4 R1).
  - (e) Creative value: no check downstream of a creative prompt compares against a fixed creative value (G2 R4).
  - (f) Unit 1 word cap: ≤ 60 words of Learn text before the first action.
  - (g) At least one non-dictated checkpoint per lesson (T5).

### T7. Teacher visibility
The spec is in §4.4. One structural question decides how much of it can exist: **[OWNER] Does the class use server
mode during class?** On the static GitHub Pages export, the classroom page sees only that browser's data, so "Needs
you now" can't be live. Recommend server mode for class periods, and static for home practice.

### T8. A teacher run-kit (new one-page doc, `docs/intro-to-python/teacher-guide.md`)
- **The shape of a period:** a 3-minute warm-up ("Mar'tu remembers" projected), self-paced work, then a 2-minute
  close (the pulse).
- **Sync points.** The class regroups at each unit's quiz/project day.
  - Early finishers go to Trials, side quests or the Extra practice pool, **never to helper duty by default**.
  - Students behind work the critical path, with the teacher's deferral switch.
- **Whole-class "Mar'tu moments" at the cliffs** (5 minutes, teacher-led, projected; the MKO is also the teacher):
  - 6A-01 box versus recipe;
  - 6A-06b be-the-ledger, traced on the board together;
  - 4B-01 boxes in boxes;
  - 6C-01 "the box holds the recipe";
  - 5A-05 the decay reveal, as a class discussion.
  
  These keep a spread-out class meeting at the hardest ideas.
- **A structured pairing protocol.** The driver/navigator roles rotate every exercise, and each lesson has one solo
  item. After Unit 1, review the solo-versus-together evidence and re-pair if a pair isn't producing solo passes.
  The sheets show unstructured collaboration (A-03/A-04, and the B section) lifted no one above the scaffolding.
- **Provisional starting presets:**
  - "Show me more" for G1, G2 and G3, **including B-02 and B-03, whose paper totals are inflated by templates and
    shared hands**;
  - QC1 first for G4.
  
  These are defaults to confirm in-app, never labels.
- **How to read the dashboard**, and what to do with a "Review first" Readiness result (pair them in the campaign,
  and pre-teach the flagged skill).
- **Privacy reminders** (T10).

### T9. The story serves the learning
- **Fun budget:**
  - At most one flavor line per screen, outside instruction and check text.
  - Cameo pass lines: at most one per checkpoint pass.
  - Mar'tu echoes typed values only at designated spots (§3, G1 R27).
- **World-as-data payoffs are protected.** 4A-01, 5A-05, 5B-04 and 2P1 are the best kind of fun, because the story
  *is* the data. A tested-out student gets them in "Mar'tu's notes" or a 2-minute "Mar'tu wants to show you
  something" item, never skipped silently (G4).
- **Side quests combine ideas instead of repeating them** (G4 R16). This is time-neutral, since they replace "one more
  of the same".
- Calm mode is an independent toggle, off by default, and not tied to presets (G4, Q13).
- No lore in checkpoints, check messages or quiz logic (v1 rule; keep it).

### T10. Privacy and classroom safety
- **Never put a student's written value into content.** This covers joke names, the fast-food strings and anything
  that could be a first name: not in check messages, not in "Not this" contrast galleries, not in Parsons
  distractors. Use invented values (`"Zelda"`, `"Kratos"` are fine as fictional). Sheet IDs appear only in design
  notes and harness `notes`, never in client bundles.
- **Echo, hero persistence and the sandbox are local only.** They pass a blocklist with a generic fallback, and a
  **class-level teacher switch turns them off**. Nothing a student types goes to the classroom API (architecture
  §5.2 already forbids code and free text; keep the privacy test).
- No visible preset badge. Hint use stays private to the student and the teacher.

### T11. Release gating
Not every feature blocks Unit 1. The tiers and gates are in §6. The live tracer does **not** block Unit 1, because
static step tables stand in for it until it ships. The trace-table item type **does** block Recipes I.

### T12. Shared-code safety
Course changes to `explain.ts`, `ConsolePanel` and the worker are additive behind a course flag (prelude
`"course"`), and campaign tests stay green. Porting to the campaign is its own PR (T4).

### T13. Measure after the first class
- **Log:**
  - which help rung or angle came right before a pass;
  - silent-stall offers accepted versus dismissed;
  - each QC pass against the same skill's later Readiness item;
  - predict accuracy per skill;
  - real minutes per item.
- **After Unit 1:** the designer and the teacher compare the time ledger with the logs and recalibrate the
  thresholds (3 failed runs, 4 min, 90 s, the 10 s rung spacing).

---

## 2. Conflicts between groups, resolved

| # | Conflict | Ruling |
|---|---|---|
| C1 | **Placement and fading.** G1 R1 and G3 R10 want "Show me more" by default. G4 says the self-report misplaces them. G2 R15 says self-report and pulse inflate. | Ask the question on the first map visit. Unanswered, "never" or "a little" → "Show me more". "Yes" → offer QC1 (never auto "Keep it short"). **Self-report and the pulse can only add support. Support fades only on performance:** a hint-free streak, a QC pass, predict accuracy. A QC1 pass sets "Keep it short". The teacher may pre-set provisionally (T8). |
| C2 | **4B-04's variable names.** G2 wants names different from the keys (forces meaning). G4 R6 wants identical names (exact matching, as in the campaign). G1 worries about quotes flipping. | Keep **different** names in 4B-04, and change its comment to "Replace each 0 with the variable that holds that value". **"Matching" means an exact name from 6B-03 on, and only there.** G4's "same word, two jobs" Investigate moves to 6B-03, where identical names first appear. The quotes principle and the 4A-02 reconciliation card prepare it (C2 also answers G1 R6). |
| C3 | **"Different from the example" checks** (1A-02, 1B-01). They are G2's copy trap, but A-01 copies values only when creatively stuck. | Keep the check. Its failure message offers **Mar'tu's pick inline** ("That's the example's line. Want Mar'tu's pick? [Use it]"), and the pick counts as the student's own. |
| C4 | **Assemble-first or type-first.** G1, G2 and G3 want Parsons offered. G4 R13 wants typing first. | The default view follows the preset: Assemble-first under "Show me more" on A-stage exercises, typed starter under "Keep it short". Assemble-it is a More-structure level for everyone. An Assemble pass is followed by a typed twin. Mastery is typed. |
| C5 | **Pair defaults.** G1 wants pair mode on for A-03/A-04, G3 for B-02/B-03. G4 says never pair by placement without asking. | **The teacher assigns pairs, and the course never auto-pairs.** Pair mode is off by default. Cross-placement mentoring needs both students' consent. Review the solo evidence after Unit 1 (T8). |
| C6 | **Solo size.** G1 R18 wants one short item. G3 R9 wants a make-twin per seat. | One item, ≤ 2 minutes. In writing lessons (1B, 1C, Recipes I, 6B, 6C) it is a **make-twin**; elsewhere it is **one bug**. Values differ per seat. It is recorded, never blocking, and never shown to the partner. Mar'tu acknowledges it ("You did that alone. I saw."). |
| C7 | **Fast lane or recipe track.** G1 says no fast lane by default. G4 R12 wants a per-student recipe track. | D11 is class-wide (T2). No per-student course order. When the class goes into Module 1 is the teacher's call, informed by "Before the cabin door". |
| C8 | **Proactive help volume.** G1 and G3 want more offers. G4 calls it nagging. | An offer is a **highlight on the Help control with one line, never a pop-up.** One dismiss silences it for that exercise. It turns off after a hint-free streak. Under "Keep it short", only the 3-failed-runs trigger is active. |
| C9 | **Price-first wording (G2 R1) versus reading load (G1).** | Price-first appears only in the *second* word problem. The `# how many?` / `# how much is one?` comments stay, and read-aloud is on. The swap message is phrased as teaching. |
| C10 | **Personal echo and persistence (G1 R27, G2 R21/R22) versus classroom safety.** | Designated spots only, on the student's own screen, with a blocklist, a generic fallback and the teacher's class switch (T10). Persistence is Tier 3. |
| C11 | **Meaning prompts and heads-ups (G2 R8, R9) versus noise for G4.** | The "Names to use" chips are **always on** (G4 R7 wants them too). Point-at-it questions and example-name heads-ups are hidden under "Keep it short" and instructions-light. G4 gets non-dictated checkpoints instead (T5). |
| C12 | **Two-call starters (G2 R6) versus "give us less dictated code" (G4).** | Two-call starters in 6A-04/05, plus "add a third call for your own hero". The non-dictated 6A-06 CP3 (G4 R10) is for everyone. "Start from blank" is offered on hint-free streaks. |
| C13 | **`print(two words)`.** G2 R2 reads it as unquoted multi-word text, G4 R5 as a space in a name. Python gives the same error ("Perhaps you forgot a comma?"). | One message. If either word is a defined name, lead with "a name can't have a space; use `_`". Otherwise lead with "these look like words; put them all inside one pair of quotes". Each version mentions the other reading in one clause. |
| C14 | **Capstone-first and exercise-level skipping (G4 R2, R11) versus false confidence (G2).** | Offered only after a hint-free streak or a QC pass, never on self-report. Capstones are behavior-checked. Every skipped skill gets a required one-minute spaced item (G4 R21, modified) and the Readiness re-check. |
| C15 | **1-A1.** G1 R2 wants coach marks, G3 wants two explicit sentences, G2 R25 wants a clickable tour. | A ≤ 60-word card with three pictures and G3's two sentences, then just-in-time coach marks. No separate tour. |

---

## 3. Decisions on every requested change

Legend: **A** accept · **AM** accept-modified · **D** decline. "→" points to the merged directive or spec.

### 3.1 Group 1, "Starting from zero" (A-02, A-03, A-04)

| ID | Decision | Reason |
|---|---|---|
| R1 | **AM** | The preset question moves to the first map visit, with "Show me more" as the default. Fading only on performance; QC1 sets "Keep it short" (C1). |
| R2 | **A** | Coach marks plus a ≤ 60-word card, which also carries G3's two sentences (C15). |
| R3 | **AM** | All rows go into the precedence tree (§4.1). The dict-comma row names this line *and* the line above (verified). |
| R4 | **A** | The BARE pattern is a must, since a lone value raises no error. Fix the citations in the design doc; messages use invented values (T10). |
| R5 | **AM** | Merged with G2 R5 into one core trace item, 6A-06b, built on the new trace-table item type. It also appears in Quiz 6A and the Readiness Check. |
| R6 | **A** | The reconciliation card at 4A-02, worded with the single quotes principle (§4.7). |
| R7 | **AM** | ≥ 3 genuinely different angles for Unit 1 concepts and campaign-critical skills, ≥ 2 elsewhere. The next unseen angle is served inside the help stack, not auto-popped. |
| R8 | **A** | **Blocks Unit 1.** Starters pre-type `full = "█"` / `empty = "░"`, and the editor toolbar gets a symbol tray for answers. |
| R9 | **A** | This is the help-stack contract for everyone (T3, §4.3). |
| R10 | **A** | Read `=` as "gets" and `==` as "is the same as" in `say` text, the glossary and the picture angles. Cheap, and it fixes the algebra reading. |
| R11 | **A** | `clock_is_red = (clock_color == "red")` at first exposure; drop the parentheses in 2A-03. |
| R12 | **A** | Diff-style output mismatch with the first difference marked. Helps every group, cheap. |
| R13 | **A** | 1C-07 becomes three checkpoints, merged with G2 R4 and G3 R19. |
| R14 | **A** | The wild-count message in 1C-02. The 1000-ropes step becomes **the 1C-03 Investigate for everyone**, done with the Try-other-numbers mechanic (G2 R10). |
| R15 | **A** | Add `def companion = "Gearshift"` to 1B-06 (DEF row). 2C-06 stays as review. |
| R16 | **A** | "Quotes and brackets come in pairs", with `print("Shield up."` in 1A-03 or 1A-08. |
| R17 | **AM** | Task-group headers in every project starter, for everyone. Placeholders and the full ladder under "Show me more". 4P pre-builds two sheets under "Show me more". |
| R18 | **AM** | One item, ≤ 2 minutes: a make-twin in writing lessons, one bug elsewhere (C6). |
| R19 | **AM** | Tag every core item (T1). Deferral is a **teacher-controlled** per-student switch, suggested by the dashboard. The freed time goes to twins. |
| R20 | **A** | Merged with G4 R10 into the PAR-CONST message with a call table (§4.2). |
| R21 | **A** | Glossary additions: defined/not defined, syntax, run, call, value, assign, indent, method. |
| R22 | **A** | The terminology contract (§4.7). |
| R23 | **A** | No "box" before 1B; use G1's wording. |
| R24 | **A** | Neutral, non-red "fizzle" panel in the course. Proposed for the campaign in the port PR. |
| R25 | **A** | Glossary and read-aloud stay on in QCs and the Readiness Check. They are accessibility, not hints. |
| R26 | **A** | For everyone: what you got right, then "worth another look", then the score. No preset branch needed. |
| R27 | **AM** | Echo only at designated spots: 1A-02, 1B-02, the 1P1 watch-keeper, 2P1's tiers, 8B-08. Own screen only, with a blocklist and the teacher's switch (T10). A wider pool is Tier 3. |
| R28 | **A** | ≤ 60 words before the first action in 1A–1C **for every preset**. The labeled-box picture is shown by default in 1B. "Show me more" means more pictures and steps, not more words. |
| R29 | **A** | Pre-type `hour_1 = 48` in 3A-01. |
| R30 | **A** | Point out `-`, `_` and `=` side by side in 1W-04. |
| R31 | **A** | A missed recall item shows the answer and a one-line why, with no red X. |
| (unnumbered) 1B-02 CP2 `print("character")` message | **A** | "That prints the word *character*. Take the quotes off so Python opens the box." |
| (unnumbered) 1B-02 distractors | **A** | Add a lone `"Zelda"` and `character - "Zelda"`, with invented values (distractor rule, §4.2). |
| (unnumbered) 1C-08 why `*` works with text | **A** | Add the stamp angle and the glue-versus-stamp sentence. |
| (unnumbered) 2A-04 "the dot means ask this text to do something" | **A** | A one-line Learn addition. |
| (unnumbered) two-step "read the error" routine from day 1 | **A** | It goes in the explainer panel's footer from 1W-02 on. The full routine stays in 2C-07. |
| (unnumbered) 5A-05 heavy on Predict and Investigate | **A** | Keep the tracer, or a static trace table until it ships. |
| (unnumbered) defer 1A-07 and 1C-05 | **A** | For everyone (T1). |
| (unnumbered) Q1 "no fast lane for us" | **AM** | Superseded by D11. Module 1 timing is the teacher's class decision (C7). |

### 3.2 Group 2, "Right shape, wrong meaning" (A-05, A-07, A-08, B-01)

| ID | Decision | Reason |
|---|---|---|
| R1 | **A** | Price-first in the second problem and in the 1C-03 your-turn variant, so grabbing numbers in reading order fails (C9). |
| R2 | **A** | Verified: multi-word unquoted values raise SyntaxError, not NameError. Add the row and a multi-word case to 1A-04 (C13). |
| R3 | **A** | The OUT-only ban becomes harness lint (a). It fixes 3A-06, 3A-08, 3B-01, 3B-04, 8A-02, 8B-03 and QC3-2. |
| R4 | **A** | 1C-07 checks the student's own hero, generalized as lint (e). |
| R5 | **AM** | Merged with G1 R5 into 6A-06b (the `7` / raw-inputs message is kept). The RET-PARAM message is added as asked. |
| R6 | **A** | Two pre-written calls with `# should show …` comments. CP2 becomes "add a third call for your hero" (C12). |
| R7 | **A** | SWAP plus the line-total message ("12 is already the cost of all 3"), in 1C-02/03, 4B-04, 6B-03 and 6C-04. |
| R8 | **AM** | "Names to use" chips always (C11). LEFT checks against an authored `foreign_names` list (the example, the hint examples, the previous exercise's required names), not live hint tracking. The heads-up never blocks and is muted under "Keep it short". |
| R9 | **AM** | One click, unscored, on the six listed exercises and any `dictates: true` checkpoint. It counts as "explains" evidence and is hidden under "Keep it short" and instructions-light. In Unit 1 if the inline mc exists by then, otherwise retrofitted at the Unit 2 release. |
| R10 | **A** | The rerun table inside CMB failures ships with Unit 1. The voluntary button comes by Unit 2. Introduced at 1C-01; 1C-09 becomes the payoff. |
| R11 | **A** | One quotes sentence, word for word everywhere (§4.7), plus the 6-card sort as a 4A-07 recall item. |
| R12 | **A** | "Show your working" in Unit 1. "Recipe" is reserved for `def`, with a callback in 6A-05. |
| R13 | **A** | Wall values are "gaps", differences are "shrink". 5A-05 is renamed "How much each gap shrank". Fix §1.2 and T-Lo-2. |
| R14 | **A** | Special-case `error_type = NameError` (verified: it runs silently), and reframe "Did you mean" when the defined name is the typo (§4.1). |
| R15 | **AM** | The fade-only-on-performance rule is adopted (C1). Predict calibration shows the *topics* that surprised the student ("2 surprises, both about what a recipe hands back") at lesson end, with no running percentage. |
| R16 | **A** | When the tracer ships. Until then, a wrong predict on a return value or reassignment opens the static trace table. |
| R17 | **A** | Readiness item 12 becomes typed with a CMB rerun. Every typed item is behavior-checked (T5). |
| R18 | **A** | Letter-diff highlighting on near-miss names. It shares one helper with R12's output diff. |
| R19 | **A** | Distractor rule: drawn from all four groups' documented slips, at most 3 per puzzle, removed adaptively (§4.2). |
| R20 | **AM** | The post-reveal twin is **immediate and required** before the checkpoint stops being "assisted". Where there is a creative slot, it uses the student's own values. The later spaced twin stays. |
| R21 | **AM** | Tier 3, after the Readiness Check ships. Local only, filtered, with the teacher's switch (C10). |
| R22 | **AM** | Merged with G1 R27: designated spots, quoting the student's value through the filter. |
| R23 | **A** | The STREXACT message for text comparisons ("every letter, space and capital"), merged with G3 R24. |
| R24 | **A** | Say the naming rule aloud in 5A-02: "A name you invent is yours. A name the task gives you is a promise." |
| R25 | **D** | Just-in-time coach marks (G1 R2) teach each control when it's first needed, so a separate tour would only add reading. |
| (unnumbered) 1B-02 editor without 1B-01's code | **A** | Rule: every exercise has its own starter. No carry-over unless designed. |
| (unnumbered) 1B-04 campaign reason ("the game can't find `Move_left`") | **A** | One line in Learn, gives a reason instead of a rule. |
| (unnumbered) recognize hint names `a`/`b` | **A** | Via `foreign_names` (§4.1 rule 3). |
| (unnumbered) 4B-04 keep different names | **A** | Kept, with the C2 wording fix. |

### 3.3 Group 3, "Steady with a template" (B-02, B-03)

| ID | Decision | Reason |
|---|---|---|
| R1 | **A** | A must. A bare string plus the requested name now outranks the "put it in quotes" row (§4.1 rule 4). The draft's explainer would otherwise walk them deeper into the misconception. |
| R2 | **A** | The 1B-01 Investigate "delete `companion =`, Run, what happened?". A static "made, not kept" picture until the tracer ships. |
| R3 | **A** | 6A-05a `fill-the-ingredients` is contingent (first exposure under "Show me more", or after an assisted or failed 6A-04), so G4 never pays for it. Plus the `___` explainer row. |
| R4 | **A** | The 6A-06 Investigate "delete `return total`", plus the console None notice in all course runs (§4.1). |
| R5 | **AM** | Start me off (rung 0) and More structure live inside the help stack. More-structure levels are hand-authored for campaign rehearsals and projects, and auto-derived elsewhere (comment skeleton → faded blanks → Parsons). A step down is logged, and the next similar exercise starts back at its default level. |
| R6 | **A** | The silent-stall trigger: 90 s with the editor unchanged and no Run. It highlights Help and feeds the teacher's "Needs you now" (C8). |
| R7 | **A** | Under `light`, the Point rung is always available, and every project starter carries its task-group headers. |
| R8 | **A** | A `starterLevel` field (S4 blanks, S3 left sides or skeleton, S2 numbered comments, S1 signature, S0 blank), enforced by lint (c). |
| R9 | **AM** | The teacher sets the pairs (C5). Prompts name seats. Solo twins use different values per seat, and solo results are hidden from the partner. Seat tracking on one device is needed only if devices are shared [OWNER]. |
| R10 | **A** | The teacher guide says B-02/B-03 start on "Show me more" despite their totals. The first Recipes I solo twin informs placement. |
| R11 | **A** | The NEWBOX pattern for a new box holding the expected value while the starter's box is untouched. |
| R12 | **A** | `_near_names` covers plural and case-plus-plural. Python's "Did you mean" is passed through when it names a user-defined name. |
| R13 | **A** | Empty-body `IndentationError` row: "A recipe needs at least one line inside it… write `pass` for now." |
| R14 | **A** | PAR collision lint (b). 6A-05 uses (6, 5) and (20, 1). |
| R15 | **A** | 6C-05's four-level ladder, with L1 as the default for everyone. Its pass is recorded "with structure" below L1 (T4). |
| R16 | **AM** | Mastery map v1 shows three levels (with structure / from comments / from blank) plus "tested out (provisional)", with together and solo as two positive ticks. Due by the Unit 3 release. |
| R17 | **A** | A 1–2 line typed twin after an Assemble pass. |
| R18 | **A** | Readiness items 2, 3 and 8 get campaign-style starters (`def roll_die(die_size): return 1`). Faithful to the campaign. |
| R19 | **A** | 1C-07 gives the left sides. 2B-08 and 5A-02 get skeletons at first exposure, enforced by lint (c). |
| R20 | **A** | Investigate prompts are one-click choices, with free text optional. |
| R21 | **A** | The two-apostrophes row. Cheap. |
| R22 | **A** | Suppress Python's "Did you mean" when it names a keyword or builtin, and list the ingredient names instead (PNM). |
| R23 | **A** | "You did that alone. I saw." on a solo pass. One line, earns trust. |
| R24 | **A** | Merged into STREXACT (G2 R23). |
| R25 | **A** | The "When does a recipe need `return`?" card in 6B-02, paid off by 6B-07. |
| (unnumbered) the two sentences for 1-A1 | **A** | They go on the 1-A1 card (C15). |
| (unnumbered) 1C-03 Teach rung "a 0 in the starter is a placeholder" | **A** | It matches the campaign's 0 placeholders. |
| (unnumbered) 6B-07 comment numbers map one-to-one onto checkpoints | **A** | Rule for all rehearsal exercises, as in the campaign. |
| (unnumbered) 6A-04 "from what you know" angle and the `hero_name` predict | **A** | Builds on the one idea they own (`name = value`). |
| (unnumbered) pair mode on by default for B-02/B-03 | **AM** | The teacher's choice per pair (C5). |

### 3.4 Group 4, "Ready to stretch" (A-01, A-06)

| ID | Decision | Reason |
|---|---|---|
| R1 | **A** | A must. A skill with no failable item shows "not yet", never "tested out". Apply the §4.5 fixes to every QC. |
| R2 | **AM** | The conversion table is adopted (§4.5). Exercise-level routing lands by the Unit 2 release; Unit 1 may ship with lesson-level routing plus capstone conversion. |
| R3 | **A** | PNM takes precedence inside a function body (verified: `attack` gets no suggestion, and the current row says "quote it"). |
| R4 | **A** | Fuzzy RNM: the missing name is within one or two edits of a `foreign_names` identifier. |
| R5 | **A** | The space-in-name rows (both forms) and the mixed-quotes row. Verified, and 1B-04 depends on them. |
| R6 | **AM** | 4B-04 keeps different names with the "holds that value" wording. "Same word, two jobs" moves to 6B-03 (C2). |
| R7 | **A** | Instructions-light always shows "Names to use" and the signature, never trims rehearsal starters, and keeps the explainer on in QCs, Trials and light mode. |
| R8 | **A** | **For everyone, not only test-outs:** the spaced re-check includes typed items on `combine-values`, `exact-names`, `param-use` and `return-right-name`, the class-wide sheet errors. |
| R9 | **A** | Fix the §6 claim: "most of Unit 1 by QC1; Units 2–6 at about 0.7–0.8× through capstone-first and light mode." |
| R10 | **A** | 6A-06 CP3, goal only (`max_fuel_for(cells)`), is the lesson's non-dictated checkpoint (T5). Plus PAR-CONST. |
| R11 | **A** | Capstone-first from the Unit 2 release, offered only on a hint-free streak or a QC pass (C14). |
| R12 | **D** | A per-student order splits pairs and story beats and doubles the gating paths. D11 gives everyone the benefit (T2). |
| R13 | **A** | Type-first under "Keep it short", with Assemble as the fallback (C4). |
| R14 | **AM** | Tier 3. Local only, explainer on, `# expect:` checks, and a teacher class switch (T10). |
| R15 | **AM** | "Mar'tu's seal" (asserts) as an optional side quest from the end of Unit 2. The token is optional-only, so the core gate is unaffected. Content only, no new feature. |
| R16 | **A** | Content rule: at least one *combining* side quest per lesson, replacing "one more of the same" (time-neutral). |
| R17 | **AM** | "The Hard-Coded Ledger" Trial in v2, because it targets the class-wide 68. "Four copies, one loop" and "One bar recipe" are Tier 3. |
| R18 | **A** | At least two forms per QC, with predict values parametrized where checks are behavioral. Unlimited retakes are honest only with forms. |
| R19 | **A** | Mar'tu's pick offered inline on example-copy failures (C3), a "use Mar'tu's picks" button in projects, and DF in QCs (it isn't a hint). |
| R20 | **AM** | An opt-in apprentice protocol in the teacher guide, with "ask, don't tell" prompts. No software role in v2. Never the default for early finishers (T8). |
| R21 | **AM** | One required recall item (< 1 min) per lesson, for tested-out skills only. A miss reverts the skill to "practicing" and queues its capstone. It never blocks. |
| R22 | **A** | WT sidebars "Why the recipe can't know the numbers yet" (6A-05) and "Whose kitchen is `result` in?" (6A-07). |
| R23 | **AM** | An optional one-click "what was different?" after Compare (G3 R20 format), not free text. |
| R24 | **AM** | "Explain a line you wrote" (one click) goes into the Readiness Check **for everyone**, because it is in the ZPD definition. Hard mode is Tier 3 and optional. |
| R25 | **A** | Frame the Recipes QC: "Nobody in this cabin has written a recipe yet. This shows Mar'tu where to start." |
| R26 | **A** | QC1 #1 becomes multiple choice, and the symbol tray exists anyway (G1 R8). |
| (unnumbered) story reveals never skipped silently | **A** | → T9. |
| (unnumbered) cameos stay on under "Keep it short" | **A** | Calm mode is independent and off by default (T9). |
| (unnumbered) let QC1 set the preset | **A** | → C1. |
| (unnumbered) 6C-05 typed from numbered comments for G4 | **A** | L1 is the default for everyone, and the mini-boss is campaign mode (T4). |

---

## 4. Specs the designer needs

### 4.1 Explainer precedence tree (course `explain` mode; ported to the campaign later)

**Titles.** Lead with a plain title ("Python couldn't read line 3", "Python found a name it doesn't know") and put
the error name second, in parentheses. When the previous run's error is fixed and a new one appears, prefix the
message with "One fixed. Python found the next one:".

**NameError: name 'X' is not defined.** The first matching rule wins:
1. X is `___` (only underscores) → "Fill in the blank `___` on line N." (G3 R3)
2. The error is raised inside a function body, and X is a near-miss of a parameter of that function (a substring, a
   shared `_`-separated word, or ≤ 2 edits) → **PNM**: "This recipe's ingredients are `base_attack` and
   `bonus_multiplier`. You wrote `attack`. Python matches names letter for letter…" Drop any Python suggestion that is
   a keyword or builtin. (G4 R3, G3 R22)
3. X is within 2 edits of an exercise `foreign_names` identifier → "`reslt` looks like `result` from the example /
   `a` from Mar'tu's hint. This task's box is `total`." (G4 R4, G2 LEFT and `a`/`b`)
4. X is the checkpoint's required name, and the source has a bare value statement → "Line N has `"Spiderman"` on its
   own. Python made the words and forgot them, because they're in no box. Write `character = "Spiderman"`." (G3 R1)
5. Python says "Did you mean: 'Y'?", Y is user-defined, and X is the task's required name (so the student's own name
   is the typo) → "Python found two names that almost match, `health` and `heath`. Use the spelling the task asks
   for in both places." (G2 R14)
6. Python says "Did you mean: 'Y'?" with Y user-defined → pass it through in plain words, adding "capitals and
   plurals count". If Y is a keyword or builtin, drop it. (G3 R12)
7. The whole line is just X → the bare-name row (G1).
8. `X - value` where an `=` was clearly meant → the dash row (v1).
9. Otherwise → "If you meant the words, put them in quotes: `"X"`. If you meant a box (variable), make it first
   with `X = …`." In 1A, use G1 R23's wording with no "box".

**SyntaxError and IndentationError.** The first match wins:
- `unterminated string literal` and the line has the *other* quote type after the opening quote → "You opened with
  `"` and closed with `'`…" (G4 R5). Otherwise → "A quote opened on line N but never closed…" (v1)
- `''word''` (two apostrophes) → "Two `'` marks are not one `"`. Use the `"` key." (G3 R21)
- `'(' was never closed` → "Brackets come in pairs too: add `)`." (G1)
- `invalid decimal literal` with a digit followed by a letter → the `5P` row (G1)
- a line starting with `def` that isn't `def name(...):` → the def-is-for-recipes row (G1, extends v1)
- `cannot assign to literal` with a quoted name on the left → the name-in-quotes row (v1)
- `invalid syntax` with two bare words before `=` → "A name can't have a space in it. Join the words with `_`."
  (G4 R5)
- `invalid syntax` on `=` with two or more bare words on the right → "These look like words. Put all of them inside
  one pair of quotes." (G2 R2)
- `Perhaps you forgot a comma?` with two adjacent bare names inside `( )` → the C13 combined message.
- `invalid syntax` or `forgot a comma?` on a line inside `{ … }` → "Inside a dictionary, items are separated by
  commas. Check the end of line N **and** the line above it." (G1, corrected per verification)
- `IndentationError: expected an indented block after function definition` → the empty-body row (G3 R13)
- the missing colon, missing indent and `elif`-after-`else` rows (v1 2B/2C)

**Silent-but-wrong notices (no error at all):**
- **BARE:** a top-level statement that is only a value. Delivered as a check message (G1 R4).
- **None notice:** a printed line is exactly `None` and the program defines a function with no `return` that has a
  value → one line under the output (G3 R4b).
- **`error_type = NameError`:** a TEXT special case (G2 R14).
- **NEWBOX:** a check message (G3 R11).

Every row is a table-driven case in `explain.test.ts`, and every row has a harness wrong answer from the evidence
(T6).

### 4.2 Check library additions, message rules and lints

| Code | Rule | Catches |
|---|---|---|
| **BARE** | A top-level statement that is only a string or number. | Lone value lines (A-04; B-02, B-03). |
| **SWAP** | A slot's value equals another input's value, so name which one went where. Includes **LINE-TOTAL**: a multiplier equals a line total ("12 is already the cost of all 3"). | A-05, A-07, A-08 pizza error; placeholder swaps in 4B-04, 6B-03, 6C-04. |
| **NEWBOX** | A new name holds the expected value while the starter's box keeps its placeholder. | G3 side-work habit. |
| **PNM** | §4.1 rule 2, also run as a check after a NameError inside a student function. | A-01 `attack`; 6A-05 `damage`. |
| **RNM (fuzzy)** | Uses `foreign_names` with ≤ 2 edits (replaces exact match). | A-01 `reslt`. |
| **LEFT** | An identifier appears only in `foreign_names` (example, hint examples, previous exercise). | A-08 `total_frait`; `a`/`b` from hints. |
| **PAR-CONST** | Two fresh calls return or print the same thing: "`max_mana_for(9)` and `max_mana_for(12)` both gave back 26. A recipe gets its numbers when it's called…", with a call table. | A-06 `return 50`; A-02, A-03, A-04 unrelated literals. |
| **RET-PARAM** | The function returned one of its own parameters. | A-07 raw inputs. |
| **STREXACT** | A comparison literal differs from the expected text only by case or space. | `"Option 1"` / `"option1"`; B-03 `fireball`. |
| **OUT (diff)** | Exact-output checks show expected and actual lines aligned, with the first difference marked. | `Lucky has26mana.` |
| **NAME (extended)** | Plural and case-plus-plural near misses, with a letter-diff display. | B-02/B-03 `Pizza` versus `pizzas`; A-08 `heath`. |
| **CMB (extended)** | The failure message includes the rerun table (input / your result / expected). The same mechanism drives the Try-other-numbers button. | Everyone's 68. |

**Authoring rules added to §2.7:**
- Lints (a) to (g) from T6.
- `foreign_names` is required on every exercise with an example or a Teach-rung example.
- Distractors come from documented slips across all groups, at most 3 per puzzle, using invented values.
- Investigate prompts are one-click.
- In rehearsal exercises, numbered comments map one-to-one onto checkpoints.
- Every checkpoint's `start` text (for Start me off) is authored, or derived from the solution's first line up to
  `=` or `(`.

### 4.3 The help stack and layered defaults (binding UI contract)

- **After a failed run, show exactly one message:** the explainer if the program crashed, otherwise the first failing
  check's message. Show one **Help** control under the active checkpoint, and nothing else. Cameo lines appear only on
  a pass. Oogrish's 3-fail line becomes the Help control's label ("Steady, now. Read the last line first. Want a
  nudge?").
- **The Help control steps through rungs.** Each step needs a Run or about 10 seconds:

  | Order | Rung | "Show me more" | "Keep it short" |
  |---|---|---|---|
  | 0 | **Start me off** (inserts the line's left side or first tokens) | in the stack | under "More options" |
  | 1 | **Point** | in the stack | in the stack |
  | 1a | **Another way** (the next unseen angle; picture → everyday → step-by-step → in Tor → shorter → from the campaign) | in the stack | under "More options" |
  | 2 | **Teach** | in the stack | in the stack |
  | 2a | **More structure** (next `starterLevel` down: skeleton → blanks → Assemble it → worked twin) | in the stack | under "More options" |
  | 3 | **Show**, then an immediate required twin | in the stack | in the stack |

- **The Learn pane keeps its own "Explain it another way" link** for before any failure. It is concept-level, and
  served from the same angle bank.
- **Proactive offers highlight the Help control with one line; no modal.**
  - **Triggers:** 3 failed runs on a checkpoint, 4 minutes without progress, or 90 seconds with the editor unchanged
    and no Run (silent stall).
  - "Keep it short" uses only the failed-runs trigger.
  - One dismiss silences offers for that exercise, and they turn off after a hint-free streak.
- **Compare with Mar'tu's version** keeps v1's unlock rules (5 min, 4 failed runs, or the ladder used up).
  - "Retype it" is the default.
  - An immediate twin is required before the checkpoint stops counting as assisted.
  - The spaced twin is still queued.
- **"Names to use" chips** show on every checkpoint that requires exact names, in every mode.
- **The symbol tray** (`█ ░ ▮ ▯ ▓`, plus `"` and `_`) lives in the editor toolbar.
- Hint use, offers and step-downs are private to the student and logged for the teacher.

### 4.4 Classroom page and teacher settings (server mode; architecture §5.2 extended)

1. **Needs you now.** Refreshes about every 30 s. Each row gives the display name entered at runtime, the exercise,
   the reason in neutral words, and minutes. The reasons:
   - a silent stall of 6 minutes or more;
   - wheel-spinning: the same error 3 times in a row, or 8 or more failed runs on one checkpoint;
   - a reveal used before any run;
   - a "too hard" pulse together with red signals;
   - a Readiness "Review first" after two cycles.
   
   A row clears when the student makes progress.
2. **Ready for more.** A hint-free streak of 5 or more checkpoints, a QC pass, or "too easy" with green signals. Each
   row comes with a suggested Trial or side quest.
3. **Unit grid** (architecture §5.2), with **"Tested out (provisional)"** distinct from **"Complete"**.
4. **Campaign readiness.** Rows are the campaign-critical skills plus the campaign parts at Band A/B. Each row counts
   students at solid / practicing / not yet, marks solo-verified, and drills down to students.
5. **Teacher settings:**
   - Route M1 or M2 (T2);
   - a provisional preset per student;
   - the per-student deferral switch (G1 R19);
   - pairs;
   - echo, persistence and sandbox on or off (T10);
   - Show-solution timing.
   
   These persist per classroom.
- **Summary schema additions** (`.strict()`, privacy test extended): `lastRunAt`, `unchangedSince`,
  `sameErrorStreak`, `skills: {tag: level, solo}`, `testedOutProvisional`, pulse counts. Still no code, no free text,
  no typed values, no hero names.
- **Static export:** panels 1 and 2 are unavailable, so show a note saying so ([OWNER] question in T7).

### 4.5 Quick Checks: coverage, forms, conversion

- **Coverage table per QC:** skill tag → item → the evidence wrong answer it fails on. A skill without a failable
  item is reported "not yet". Minimum fixes:
  - **QC1:**
    - #1 becomes multiple choice.
    - #2 shows `Example: companion = "Gearshift"` beside the `character` task, with DF available.
    - New #6: the `Max_Mana` / `magical affinity` bug.
    - Add `numbers-vs-text` and `reassign` to its skills (#5 already exercises them).
  - **QC2:** add an `and`/`or`/`not` item.
  - **QC3:** #2 reads the last item through the list (CMB).
  - **QC4:** new #6: `roster[1]["name"]`, then spend mana with a CMB rerun.
  - **QC5:** add a `loop-with-if` item (CMB) and a `break` predict.
  - **QC6 splits into "QC Recipes I" and "QC Recipes II".**
    - Recipes I: the goal-only `armor_total(base_armor, bonus_armor)` with an Example using `result` on screen (PAR,
      RET, RNM, PNM); store-then-pass; return a comparison (BND); `roll_die` with a parameter (RND); `=` versus `def`.
    - Recipes II: a dict from parameters stored by name; an early-`return` guard; a read-helper item (KEEP, CALL);
      handing over versus calling; calling a stored function; a missing `return` → `None`.
- **Two forms per QC**, with predict values parametrized. Unlimited retakes; a retake draws the other form.
- **Pass rule:** every code task plus 80% of the questions.
- **Conversion on a pass** (from G4 §3):

  | Item | Becomes |
  |---|---|
  | a lesson whose skills all passed | its capstone (the last Make checkpoint plus SOLO) in light mode |
  | a lesson with failed skills | only the exercises tagged with those skills |
  | the unit project | Trial mode: premise, required output and check table, from blank |
  | the unit quiz | optional |
  | a campaign rehearsal exercise | its Start-from-blank version, keeping the campaign-style comments |
  | a story beat | a "Mar'tu's notes" line or a 2-minute show item |

- **Tested-out skills** get the required one-minute recall item (G4 R21, modified) and the Readiness re-check. The
  map shows "tested out (provisional)" until one of them confirms it.

### 4.6 Readiness Check changes
- Item 12 is typed with a CMB rerun (G2 R17).
- Items 2, 3 and 8 get campaign-style starters (G3 R18).
- **Add item 13:** "Write a recipe from a goal, with an Example on screen" (`param-use`, `return-right-name`,
  `exact-names`). About +3 minutes. It covers G4 R8 for everyone.
- After the mini-boss, add a one-click "Explain a line you wrote" (G4 R24, modified).
- Glossary and read-aloud stay on (G1 R25). The explainer stays on.
- The mini-boss runs in campaign mode (T4). It does not depend on Unit 8 (T1).
- The spaced re-check includes typed items on `combine-values`, `exact-names`, `param-use` and `return-right-name` for
  everyone, plus each student's misses.
- Hard mode is Tier 3.

### 4.7 Terminology contract (all student-facing text, glossary and read-aloud)

| Idea | First units | From Unit 3 / Recipes II on (the campaign's words) | Read aloud |
|---|---|---|---|
| variable | "box (variable)" in Units 1–2 | "variable" (Mar'tu may still say "box") | `=` is "gets" |
| `==` | "is the same as" | same | "is the same as" |
| function | "recipe (function)" in Recipes I; "recipe" is **never** used for anything but `def` | "function" by Recipes II | — |
| parameter / argument | "ingredient (parameter)" / "what you hand over (argument)" | "parameter" / "argument" | — |
| dictionary key | "label (key)" | "key" | — |
| return | "hands back (returns)" | "returns" | — |
| quotes | **"Quotes mean these exact letters. No quotes means look inside the box with this label."** (word for word, every time) | same | — |
| combining values (Unit 1) | "show your working" | "build it from the variables" | — |
| chalk-wall values / their differences | "gaps" / "shrink" | same | — |
| "matching" (placeholders) | used only for an **exact** name, from 6B-03 on | same | — |

---

## 5. Answers to the draft's open questions

| Q | Answer |
|---|---|
| Q1 position in the campaign | D11, plus a class-level Route M1/M2 (T2). **[OWNER]** Has the class played Module 1's coding parts? If not, recommend M1. If yes, M2, and the rehearsals serve as review. |
| Q2 deviations | D1–D10 approved as drafted, with D7's list extended by 1A-07 and 1C-05. **D11 added [OWNER]**. D3 (`.lower()` in Control Flow) and D4 (`"█" * n` in Unit 1) are good. |
| Q3 periods available | **[OWNER].** Plan to ≈ 18.5 core periods (T1). If fewer are available, use M1 and move Strings after Module 2 starts. |
| Q4 spoilers | **[OWNER].** Default: keep Bomb Shell and Lucky, since the brief's own opening uses Lucky's line. Never show `Strengthen Magic`, the red-clock event, or campaign function names (v1 rule). |
| Q5 reading level | Checkpoint text targets FK grade ≤ 6. The cap is ≤ 60 words before the first action in Unit 1 and ≤ 120 after. The accent rules are good. Length and jargon matter more than grade (G1). |
| Q6 pair mode | Teacher-chosen per pair, off by default. Solos are recorded, never required (C5, C6). **[OWNER]** Is it one device per student, or shared devices? Only shared devices need two seats on one device. |
| Q7 Quick Check rules | All code tasks plus 80%. "Tested out (provisional)" is reported separately from "complete" until confirmed. Unlimited retakes with ≥ 2 forms. The teacher may pre-set presets provisionally (§4.5, C1). |
| Q8 productive-failure hooks | Keep both, with a pre-typed first line, skipped on frustration signals. |
| Q9 Readiness stakes | Practice only, never a grade. The §5.3 heuristic is approved, with the §4.6 changes. |
| Q10 names | **[OWNER].** No objection from the classroom side. |
| Q11 engineering approvals | Approved: `_rerun`, `_calls`, `_func_ast`, `_near_names` (extended), the core-only gate rule, `roster` instead of `party`, and the §4.2 patterns. Pseudo-tokens: approve `pattern:StrRepeat`, `pattern:NestedSubscript` and `pattern:FuncValue` now (they gate the cliff idioms); the rest can wait. |
| Q12 f-strings | Read both, write either (8B-07). The campaign uses `+` and `str()`. |
| Q13 Calm mode | Off by default for everyone, an independent toggle, not tied to presets. |
| Q14 cipher | **[OWNER]** Is IDLE available? Until we know, 8P2 is browser-only. |
| New | **[OWNER]** Server mode during class (T7)? |

---

## 6. Feature tiers: cost, value and release gate

Cost: S under a day, M a few days, L a week or more. Gates: **U1** blocks the Unit 1 release · **U2** Unit 2 ·
**R-I** Recipes I · **D** Dictionaries · **R-II** Recipes II · **RC** Readiness Check · **T3** later.

| Feature | Serves | Cost | Value | Gate |
|---|---|---|---|---|
| Explainer precedence tree with the Unit 1 rows, plain titles, "One fixed" | all | S–M | High | **U1** |
| Check patterns BARE, SWAP/LINE-TOTAL, NEWBOX, OUT diff, NAME extended, CMB rerun table, `foreign_names`/LEFT | G1–G4 | M | High | **U1** |
| Lints (a), (c), (e), (f), (g); QC coverage lint (d) for QC1 | all | S | High | **U1** |
| Help stack: rung 0, Point always, highlight offers, silent stall, immediate twin, rung spacing | G1, G2, G3 | M | High | **U1** |
| "Names to use" chips; symbol tray and pre-typed blocks | G2, G4, all | S | High | **U1** |
| Preset logic (first-visit question, fading on performance only) | all | S | High | **U1** |
| QC1 rewrite, 2 forms, "not yet" for untested skills, lesson-level capstone conversion | G4 | M | High | **U1** |
| Neutral error panel; quiz review with right answers first; reaction lines at designated spots plus the teacher switch | G1, G2 | S | Med | **U1** |
| Static step tables in place of the live tracer (1B-05, 1C-04) | G1, G2 | S (content) | Med | **U1** |
| Exercise-level QC routing; Trial-mode projects | G4 | M | Med | U2 |
| Try-other-numbers button; point-at-it inline mc (retrofit to 1C-08) | G2, all | S–M | Med | U2 |
| Capstone-first | G4 | M | Med | U2 |
| Auto-derived More-structure levels | G3 | M | High | U2 |
| Classroom: Needs you now and the unit grid (server mode) | teacher | M | High | U2 |
| Mastery map v1 (3 levels, together and solo); predict calibration topics | G3, G2 | M | Med | Unit 3 |
| Trace-table item type (6A-06b, 1C-04 and 5A-04 retrofits, quizzes, Readiness) | G1, G2 | M | High | **R-I** |
| PNM, fuzzy RNM, PAR-CONST, RET-PARAM, None notice, PAR-collision lint (b) | G1–G4 | S–M | High | **R-I** |
| Live tracer (nested boxes, call/return arrow), auto-open on a wrong predict | G1, G2 | L | High | D (static tables until then) |
| 6C-05 hand-authored ladder; campaign mode | G3, all | S–M | High | R-II |
| Campaign-readiness panel; spaced re-check | teacher, all | M | High | RC |
| Port the explainer and None notice to the campaign (separate PR) | all | M | High | before Module 2 |
| Two seats on one device | G1, G3 | M–L | Med | only if devices are shared [OWNER] |
| Mar'tu's slate; hero persistence; reaction pool; hard mode; extra refactor Trials | G4, G2 | M | Low–Med | T3 |
| Per-student recipe track; apprentice role in software; clickable tour | — | — | — | **declined** |

---

## 7. Ordered action list for the designer

**Phase A: curriculum v2 (this document becomes the doc's changelog; do this before more content is authored)**
1. **Structure.** Apply D11 (T2) and make the lean core the core (T1). Move 1A-07, 1C-05 and the trimmed items into
   the Extra practice pool. Tag every item `campaign-critical` or `syllabus-core`. Make Strings independent of the
   Readiness Check.
   - Re-run `curriculum_v1_gate.py` on the core-only and full paths, and regenerate `concept_map.json`.
     `attr:capitalize` now enters at 6A-08.
2. **The time ledger and the critical path** (T1). Show that the critical path fits in core ÷ 1.4. If it doesn't,
   list the over-run and propose trims inside projects.
3. **Rewrite §2 (site experience).** The help-stack contract (§4.3); the layered-defaults table updated with C1, C4,
   C8 and C11; the terminology contract (§4.7); the check library (§4.2); the explainer precedence tree (§4.1); the
   authoring rules and lints (T6); mastery-evidence rules (T5); campaign mode (T4); privacy rules (T10).
4. **Rewrite Unit 1:**
   - 1-A1 card (C15); preset question on the first visit (C1).
   - 1A-03 paired quotes and brackets; 1A-04 multi-word case, with no "box".
   - 1B-01 delete-`companion` Investigate and the anatomy picture; 1B-02 messages, distractors and a fresh starter.
   - 1B-04 the campaign reason plus the space-in-name rows; 1B-06 `def` bug.
   - 1C-02 price-first second problem and the wild-count message.
   - 1C-03 the 1000-ropes Investigate, the LINE-TOTAL and SWAP messages, "show your working", and the placeholder
     Teach rung.
   - 1C-04 new angles and the static trace table; 1C-06 diff; 1C-07 three checkpoints, left sides, own hero.
   - 1C-08 pre-typed blocks and the stamp angle.
   - QC1 per §4.5; Quiz 1 review order; 1P1 headers, Point rung and Trial mode.
   - SOLO items per C6; ≤ 60 words; `starterLevel` on every exercise; at least one non-dictated checkpoint per
     lesson.
5. **Rewrite every Quick Check** per §4.5, with coverage tables and two forms. Split QC6.
6. **Recipes I (6A):**
   - 6A-04/05 two-call starters and PAR sets (6, 5) / (20, 1); 6A-05a (contingent); the 6A-04 angle and predict.
   - 6A-06 delete-`return` Investigate plus the goal-only CP3; the new 6A-06b trace item.
   - 6A-08 tidy-line starter.
   - PAR-CONST and RET-PARAM messages; WT sidebars; make-twin SOLO; the "Before the cabin door" check (Route M1).
7. **Units 2–5, Recipes II, Strings, Trials, Readiness:**
   - 2A-02 parentheses; 2B-05 STREXACT; 2B-08 skeleton; 2C-01 / 2C-03 special cases.
   - OUT-only fixes in Unit 3; 3A-01 pre-typed first line.
   - 4A-02 reconciliation card; 4A-07 quotes sort; 4B-04 wording (C2); 4P pre-built sheets under "Show me more".
   - 5A-02 skeleton and naming rule; 5A-05 rename; recipe-shaped conversions in Units 3–5.
   - 6B-02 return card; 6B-03 "same word, two jobs"; 6C-05 ladder; campaign mode.
   - Combining side quests; the Hard-Coded Ledger Trial; "Mar'tu's seal" side quest.
   - Readiness per §4.6.
8. **Classroom page and teacher settings spec** (§4.4), and the summary schema fields. Outline the teacher run-kit
   (T8).
9. **Engineering hand-off for the Unit 1 gate** (§6, U1 rows): explainer tree plus tests; check helpers in
   `course_helpers.py` plus harness lints; help stack in ExercisePlayer; chips; symbol tray; preset logic; QC1
   routing and conversion; neutral panel; quiz review order. Prove every new row and pattern with harness wrong
   answers.

**Phase B: later gates, in order.** U2 → Unit 3 → R-I → D → R-II → RC → port the explainer to the campaign → T3. Each
gate lists exactly the §6 rows due at that gate.

---

## 8. What to bring back to the teacher

1. **curriculum-v2.md** with a changelog keyed to the IDs above (G1-R1 … G4-R26, C1–C15, T1–T13), so every decision
   can be traced.
2. **The time ledger and the critical-path check** (T1), including the G1 and G4 estimates.
3. **The gate-script output** for both paths after D11, plus the lint results (a)–(g).
4. **Unit 1 coverage evidence:**
   - the explainer and check rows with their wrong answers, all passing;
   - QC1's coverage table;
   - a screenshot or mock of the exercise screen showing the single help stack after a failed run.
5. **A short list of the [OWNER] questions:** D11 approval, the Module 1 status / route, the periods available, the
   spoilers, server mode, the device ratio, IDLE, and the names.
