# Curriculum v1 review: group 4, "Ready to stretch" (A-01, A-06)

**Reviewer role:** student representative for group 4 (`ready-to-stretch`).
**Read:** personas.md (group 4, help caveats, class-wide patterns), A-verified.json (A-01, A-06), brief.md,
campaign-python-inventory.md, research/zpd-principles.md §5, curriculum-v1.md end to end, and the two reviews
already filed (groups 1 and 2), so this one doesn't repeat them.
**Verified:** every Python message quoted below came from running our sheets' exact lines in CPython 3.13.18.

---

## 0. Who I speak for, and the evidence I'm holding the draft to

We were the most comfortable sheets in the class and worked on our own (help suspicion: none for A-01, low for
A-06). That's relative. **Neither of us has written a working function, and neither of us let the code combine
the 68.** Our sheets also cover only Unit 1 skills plus one function and one trace. There is **zero evidence**
that we know `if`, lists, `randint`, dictionaries or loops.

| What we wrote | Sheet | What Python 3.13 does with it | Does the draft catch it with the right message? |
|---|---|---|---|
| `total_cost = 68` (worked out by hand: `4·12=48 / 2·10=20 / 68`) | both | No error. Only a rerun check can catch it | **Yes.** CMB in 1C-03, 1C-09 and QC1 #3 |
| `character= "Zelda"`, plus the margin note "not my favorite I just can't think of a character" | A-01 | Fine | **Mostly.** The DF button exists, but 1A-02 CP1 and 1B-01 CP1 *fail* a copied example value without offering it |
| `power_up = "Fireball'` (opens with `"`, closes with `'`) | A-01 | `SyntaxError: unterminated string literal` | **No.** The explainer says "a quote opened … but never closed", and A-01 *did* close it |
| `total = attack * bonus` (parameters are `base_attack`, `bonus_multiplier`) | A-01 | `NameError: name 'attack' is not defined`, with **no** "Did you mean" | **No, and it's worse.** See below |
| `return reslt` (from the example's `result`; this function's box is `total`) | A-01 | `NameError: name 'reslt' is not defined`, no suggestion | **No.** RNM matches the example's name exactly, so `reslt` slips past it |
| `player_name = "<a first name>"` (the example's name, not `character`) | A-06 | Fine, but the check needs `character` | **Yes in lessons** (NAME). **No in QC1**, which has no example to copy from |
| `total = 10 * 5` / `return 50` (test values, no parameters) | A-06 | No error | **Yes** (PAR), but the message doesn't name the symptom (see R10) |
| Self-started program: `Pizza = 4` / `soda - 10` / `total pizzaparty = pizza + soda` / `print(pizza party)  # 68` | A-06 | `soda - 10` gives NameError. `pizza` gives `NameError … Did you mean: 'Pizza'?`. `total pizzaparty =` gives plain `SyntaxError: invalid syntax`. `print(pizza party)` gives **`invalid syntax. Perhaps you forgot a comma?`** | **Partly.** `-` vs `=` and case are covered. There's **no explainer row for a space in a name**, though 1B-04 relies on one, and Python's own "forgot a comma?" points A-06 the wrong way |
| `silver_value = 10` (4 × 5), with the right final 60 | A-06 | (paper) | Fine. A one-off slip |

**The `attack` case is a real bug in the plan.** 6A-05 promises the explanation "this recipe's ingredients are
`base_damage` and `bonus`; Python matches names letter for letter". But no check code in §2.3 implements it:
- NAME's near-miss list covers only the example's name, case variants and "typos one edit away". `attack` is
  five edits from `base_attack`.
- The §2.4 row "`NameError` … on a line with `=` or `print(`" **does** match A-01's line `total = attack * bonus`
  and 6A-05's `print(damage + bonus)`.

So as written, the explainer tells A-01: *"If you meant the words, put them in quotes: `"attack"`."* That sends A-01
toward `"attack" * bonus`, which is exactly the wrong lesson, at the exact spot our sheets fell off the cliff.

---

## 1. Verdict: would it work for us?

**Yes, with honest and granular test-outs and with the saved time spent on functions and real stretch. As
written, the test-outs are both too coarse and too leaky.**

What's right: a per-skill Quick Check on the first screen, "QC6: G4 must not skip this unit untested",
instructions-light mode, collapsible examples, the DF button, Trials with advanced variants (including a refactor
and write-your-own asserts), the "Why does this work?" sidebars, and a Readiness Check that's typed, has no reveal
and re-verifies test-outs. These are what we asked for.

Where it breaks for us:
1. **The Quick Checks claim skills they don't test, including our two sheet errors.**
   - QC1 lists `exact-names`, but its only item ("make `character`") has no example to copy. It never tests case
     or spaces. A-06 would pass it and skip 1B-04, the lesson aimed at A-06's own `Pizza`/`pizza` and
     `pizza party`.
   - QC6 says "all of the Unit 6 skills" but has no item for `return-right-name` (A-01's `return reslt`),
     `early-return` or `read-helper`. The last two are campaign-critical.
   - QC4 has no item for `list-of-dicts` (campaign-critical). QC5 has none for `loop-with-if` or `break`. QC1 omits
     `numbers-vs-text` and `reassign`, and QC2 omits `and-or-not`. Yet a passed unit counts as tested out.
   - The safety net doesn't cover the gap either. Readiness Part 1 has no typed item for `combine-values` or
     `return-right-name`, the two errors on both our sheets.
2. **Test-out deletes instead of converting.** Routing is per lesson ("skip only those lessons"). If A-01 misses
   only `repeat-string` on QC1, A-01 redoes all of 1C (9 exercises, 38 min) for one exercise (1C-08). If we pass,
   the draft doesn't say what happens to Quiz 1 or Project 1P1. Our sheets argue we should still *produce* code on
   every skill, just without the scaffolding.
3. **The explainer misfires on our exact slips** (`attack`, `reslt`, `"Fireball'`, `pizza party`).
4. **4B-04 trains A-01's misconception.** "Replace each 0 with the matching variable" matches `cost` to
   `"mana_cost"` and `needed` to `"required_affinity"`, an *approximate* match by meaning. Two lessons later, 6B-03
   and the campaign use the same words for an *exact* match (`"mana_cost": mana_cost`).
5. **The pacing in §6 overpromises.** "G4 … can test out of Units 1–3 in about 30 minutes" has no evidence behind
   it, because we've never seen `if` or lists. A-06 also sits at the edge of group 3. What we'll really do in
   Units 2–5 is go *faster through* new material, not skip it. The draft has no tool for that besides
   instructions-light.
6. **Functions, our actual gap, arrive in week 4.** The time we save in Unit 1 goes to optional breadth (Clock
   Math, tuples, `zip`) rather than to the cliff. The fast lane already shows 6A can run right after Unit 2.
7. **No sandbox, and no protection from becoming helpers.** A-06 wrote code unprompted. The draft has nowhere to
   do that. The research's opt-in peer-mentor role never made it into the curriculum, so "finish early, go help"
   becomes the default by omission.

---

## 2. Walking through it as us

### Course map and Unit 1
- The `[ Where should I start? (Quick Checks) ]` button on the first screen is the best thing in the draft for
  us. We'd click it first.
- 1A asks "Have you typed code before? (never / a little / yes)". We'd honestly answer "never" or "a little",
  because nobody here has prior Python. Our strength comes from the worksheet, not from typing. So that answer
  would suggest "Show me more" to the two students the draft wants on "Keep it short". Let QC1 set the preset when
  a student takes it (group 1 flagged the same ordering problem from the other side).
- **1A-02 CP1** ("prints a line different from the example's") and **1B-01 CP1** (`companion` ≠
  `"Gearshift"`) fail A-01 for a creative block, not a misunderstanding. A-01 copies example *values* when stuck
  and wrote down exactly that. The fail message should hand over Mar'tu's pick ("That's the example's line. Want
  Mar'tu's pick? [Use it]"), not just say "different".
- **1B-04 `exact-names`** is the lesson A-06 most needs (`pizza party`, `Pizza`/`pizza`). Its explainer promise
  ("SyntaxError: a space in the name") has no row in §2.4. Python says only "invalid syntax", or "Perhaps you
  forgot a comma?" inside `print(...)`.
- **1C-03 and 1C-09** are perfect for our 68. The rerun message ("When I changed `lantern_count` to 7,
  `total_cost` stayed 22") is the sentence we needed on paper. 1C-09 shows that the checks change inputs. A-01 will
  love finding out *how* the grader works.
- **Project 1P1** dictates every value and every step ("Make `mana_per_hour` (2) …"). For us that's
  transcription. As a Trial (premise + required output + check list + blank editor) it would be a 15-minute test
  of whether "let the code combine it" stuck.
- **QC1 #1** asks us to predict `Mana [███░░] 3/5`. We've never seen `"█" * 3`, so we'd probably miss this, which
  is fine. But a "type what it prints" answer with `█` can't be typed on a Chromebook. Make it multiple choice or
  give a symbol palette.

### Unit 2 (new to us)
- We have no evidence on any of this, so we can't honestly test out. We need the same content faster:
  examples collapsed, the capstone first (2B-08 `roll-and-decide` and the 2B-09 SOLO), and the teaching exercises
  only where we fail.
- **2B-05 `four-answers`** starts with Assemble ("A→M"). Parsons is slow for us, and mastery needs typing anyway.
  Under "Keep it short" it should open as the typed campaign-style starter, with Assemble as the fallback button.
- **2C-01** (record the traceback in three variables) is clever, and A-01 will like it.
- **Delight:** 2A-03 boundaries plus BND checks that read `needed` from our own code, so any difficulty we pick
  still passes.

### Units 3–5 (new to us)
- **3A-01 and 4A-01** (productive failure): keep them. A-06 experiments by nature, and three minutes ungraded is
  fine.
- **4B-04 `spell-book-of-spells`** is the one exercise that actively hurts A-01 (see verdict item 4 and spec 5.3).
- **4B-05 `can-they-cast`** (A→M) is the first real composition, and it starts as a Parsons puzzle. We should type
  it.
- **5A-05 (the gaps)** and **5B-04 (forecast)** are the best moments in the course: we find the decay ourselves.
  Under test-out or light mode, these story reveals must never be skipped silently.
- **Side quests** here mostly repeat ("also count them", "a fifth color"). We want ones that combine. One example:
  5A-05's gaps are 0, 1, 1, 2, 3, 4, and their own differences are 1, 0, 1, 1, 1. "Is the decay itself speeding
  up?" is a real question in Tor that needs only `range(len(...))`.

### Unit 6 (our cliff)
- **6A-05** targets our sheets exactly (A-06's `4 + 3` caught by PAR; A-01's `damage + bonus`). The A-01 branch
  needs the new check described in spec 5.2, or the explainer gives the wrong advice.
- **6A-06** dictates the body ("with `total = affinity * 2` and `return total`"). A-01 "reads the actual task",
  so A-01 will copy it, pass, and never face the moment the worksheet tested: choosing the right name to return
  with no one telling you. 6A-07 is a *debug* of someone else's `return result`, and spotting it there is easier
  than avoiding it yourself. We need one checkpoint with a goal and no dictated code.
- **PAR messages** should name A-06's symptom: "`max_mana_for(9)` and `max_mana_for(12)` both gave back 26. Your
  recipe gives the same answer whatever you hand it." That's the misconception in one sentence.
- **6B-02, 6B-04 and 6B-09** (mutation through a parameter, rebinding that doesn't reach the caller, scope) are the
  "why does this work?" material A-01 wants. Keep them.
- **6C-05** is the campaign's hardest part rehearsed. For us it should be typed from the numbered comments only,
  with no Parsons first and no starter trimming, because that's exactly the Readiness mini-boss and
  `hold-the-barrier`.
- **QC6** needs an example to copy from, so it can catch `return result`, plus a guard item and a read-helper
  item (spec 5.1).

### Unit 7 Trials, Unit 8, Readiness
- **T-F-3** (refactor an `elif` into a dict lookup, then a dict of recipes) and **T-Own** (write the asserts) are
  exactly what we asked for. T-Own is A-06's `# 68` comment made into real Python. Offer it much earlier than Unit
  7.
- Unit 8 is fine for us at speed. 8B-07's "read both, write either" for f-strings is the right weight.
- **Readiness:** keep it typed with no reveal. We'd also like an optional "hard mode" mini-boss (no comments, a
  signature only) and an "explain a line you wrote" item.

---

## 3. The principle we're asking for: test-out converts, it doesn't delete

Our sheets show solid basics *and* the exact slips that would let us skip too early. So a pass shouldn't make
material disappear. It should shrink it to the part where we produce code with no scaffolding:

| On a QC pass, this item… | …becomes |
|---|---|
| A lesson whose skills all passed | its capstone: the last Make exercise plus the SOLO broken spell, in instructions-light mode with "Start from blank" |
| A lesson where some skills failed | only the exercises tagged with the failed skills (exercise-level routing), plus the SOLO lines for those skills |
| The unit project | Trial mode: premise, required output and check table, with a blank editor |
| The unit quiz | optional (the QC was stricter and typed) |
| A campaign-rehearsal exercise (2B-05, 6A-03, 6A-08, 6A-09, 6A-10, 6B-07, 6C-04, 6C-05) | its "Start from blank" version, keeping the campaign-style comments |
| A story beat inside a skipped exercise (e.g., 5A-05's decay line) | a line in "Mar'tu's notes", or a 2-minute "Mar'tu wants to show you something" item |

At our speed a converted Unit 1 takes about 40 minutes (QC1 10 + capstones about 10 + 1C-08 if missed 4 + 1P1 as
a Trial 15), against 146 × 0.6 ≈ 88. We still write code for every skill, so the teacher sees real evidence and
not a skip.

---

## 4. Requested changes (prioritized)

| # | Where | Change | Why (our evidence) | Priority |
|---|---|---|---|---|
| R1 | QC1–QC8, §2.2 | Every skill a QC marks as tested out must have an item that can fail on our actual error. Fix QC1, QC4, QC5 and QC6 as in spec 5.1. Otherwise show the untested skills as "not yet", not "tested out". | QC1 `exact-names` can't fail on A-06's `player_name`/`pizza party`/`Pizza`. QC6 can't fail on A-01's `return reslt`. `list-of-dicts`, `early-return` and `read-helper` are campaign-critical with no QC item. | must |
| R2 | §2.2 Quick Check row, §2.5 | Exercise-level routing (skill tag → exercise ids, data the checkpoints already carry), plus the conversion table in §3: capstone, Trial-mode project, optional quiz, from-blank rehearsals. | All-or-nothing frustration (persona). A one-skill miss on QC1 currently costs all of 1C. | must |
| R3 | §2.3, §2.4, 6A-05 | Add a **PNM** (parameter near-miss) check and explainer row that **takes precedence over** the "put them in quotes" row whenever the NameError comes from inside a function body (spec 5.2). | A-01 `attack * bonus`. Python gives no suggestion, and the current row tells A-01 to quote it. | must |
| R4 | §2.3 RNM | Match the missing name against the example's identifiers with `_near_names` (one edit away), not exact equality. | A-01 `return reslt` (a typo of `result`) slips past RNM as written. | must |
| R5 | §2.4, 1B-04 | Add explainer rows for a space in a name (both forms) and for mismatched quote types (spec 5.2). | A-06 `total pizzaparty =`, `print(pizza party)` ("Perhaps you forgot a comma?" misleads). A-01 `"Fireball'`. 1B-04 relies on a row that doesn't exist. | must |
| R6 | 4B-04, Quiz 4 parsons, QC4 #3 | Rename the variables `mana_cost` and `required_affinity` so "matching" means exact, as in 6B-03 and the campaign. Add an Investigate step: rename one everywhere and see that it still runs (spec 5.3). | A-01 treats parameter names as approximate labels. 4B-04 currently rewards matching by meaning just before the campaign's "replace each placeholder with the matching parameter". | must |
| R7 | §2.5 instructions-light | Always show a "names to use" line (every required variable and function name, and the signature). Never trim starters on the campaign-rehearsal exercises. Keep the error explainer on in QCs, Trials and light mode. | Exact names are our weak spot (both sheets). A light mode that hides them would fail us for the wrong reason. A-06's from-blank code is full of explainer-worthy slips. | must |
| R8 | Readiness §5.1, §5.3 spaced re-check | For anyone who tested out, the spaced re-check must include typed items on `combine-values`, `exact-names`, `param-use` and `return-right-name`. | These are our sheet errors. Right now nothing after a QC pass re-tests the first and last of them. | must |
| R9 | §6 pacing | Replace "G4 … can test out of Units 1–3 in about 30 minutes" with: "most of Unit 1 by QC1. Units 2–6 are new to G4: plan about 0.7–0.8× through capstone-first and light mode, not test-out." | No evidence on `if`, lists or `randint`. A-06 is at the edge of group 3. | should |
| R10 | 6A-06, PAR messages | Add 6A-06 CP3: "Write `max_fuel_for(cells)`. Gearshift gets 5 fuel per cell." Give the goal only, no dictated code [PAR, RET, RNM]. Add a PAR message for "same answer for every call". | A-01 would transcribe the dictated body. A-06's `return 50` misconception needs to be named, not just shown as expected vs got. | should |
| R11 | §2.1, all lessons | **Capstone-first** offer after a hint-free streak or a QC pass: "Try the last one first?" Pass it hint-free and the teaching exercises are marked "passed by capstone", except for skills the capstone doesn't check. Fail it and you drop to exercise 1 with no penalty. | Going fast through *new* content (Units 2–6), where test-out is dishonest for us. | should |
| R12 | §1.5, §6 | A per-student **recipe track** (teacher-enabled, off by default): 6A right after Unit 2, as the fast lane already allows (gate-checked), then Units 3–5, 6B and 6C as usual. Recipe-track students get the Control Flow Trials in function form. | Functions are our gap. This gives them about 3 extra weeks of spacing and spends saved time on the cliff instead of breadth. | should |
| R13 | 2B-05, 4B-05, 6C-04, 6C-05 | Under "Keep it short", A-stage exercises open as the typed campaign-style starter, with Assemble as the fallback. | Parsons is slow for us. Mastery and the Readiness Check need typing anyway. | should |
| R14 | site feature | **Mar'tu's slate**: a sandbox reachable from any lesson, with the explainer on and the tokens taught so far. Typing `# expect: 68` above Run checks the prediction. Saved locally only, never sent to the classroom API. | A-06's unprompted mini-program, which ended with a predicted output (`# 68`) that was wrong. The slate would have shown that. | should |
| R15 | Unit 2 optional, T-Own | Offer **"Mar'tu's seal"** (write `assert` lines that prove your code) as a side quest right after 2A. It's an optional-only token, so the core gate is unaffected. | A-06's `# 68` instinct. T-Own is currently locked until after Unit 6. | should |
| R16 | Lucky's side quests | At least one side quest per lesson that combines ideas rather than repeating them. Examples: 1C-08 "bar always 10 blocks wide" (`//`, with the 1-A2 prerequisite card); 5A-05 "gaps between the gaps" (1, 0, 1, 1, 1); 5B-04 "smallest `shrink` that runs out of nights in 3 steps"; 4B-05 "say how much mana is missing"; 6C-02 `cast_twice(effect, hero)`; 6P "swap `run_array` for a dict of dials". | "Real stretch" means deepen, not race (research §5.5). Most current side quests are "one more of the same". | should |
| R17 | Unit 7 | Add refactor Trials: **"The Hard-Coded Ledger"** (a working script full of 68-style literals that fails the rerun table until each one is an expression), "Four copies, one loop", "One bar recipe". | Our shared 68 habit turned into a challenge. The persona fights for refactoring Trials, and T-F-3 is the only one. | should |
| R18 | QC1–QC8, §7 Q7 | At least 2 parallel forms per QC. A retake draws the other form. | With unlimited retakes on identical items, we'd memorize the QC. That's dishonest gating. | should |
| R19 | 1A-02, 1B-01, projects 1P1, 2P1, 4P, QCs | When a "different from the example" check fails, offer Mar'tu's pick inline. Give projects one "use Mar'tu's picks for all creative blanks" button. Keep DF available in QCs (it isn't a hint). | A-01: "not my favorite I just can't think of a character". 2P1 has five free-text tiers. | should |
| R20 | site feature, teacher guide | Add an opt-in **apprentice role**: volunteer only, never the default, never in place of the student's own Trials, with "ask, don't tell" prompts. Pair mode never pairs by placement without consent. | The persona's top frustration list includes "being turned into unpaid helpers". The research names the role, but the curriculum doesn't have it. | should |
| R21 | §2.1 "Mar'tu remembers…" | For tested-out skills, one recall item per lesson is not skippable (under 1 min), framed as "Mar'tu checks your notes". | "Re-checked later" is our own honesty ask. Skippable warm-ups don't re-verify anything. | should |
| R22 | 6A-05, 6A-07 | Add "Why does this work?" sidebars: "Why the recipe can't know the numbers yet" (they arrive at the call) and "Whose kitchen is `result` in?" (a scope preview pointing to 6B-09). | A-06's `10 * 5`; A-01's `return reslt` explained by its cause, not just its fix. | nice |
| R23 | §2.1 reveal | After "Compare with Mar'tu's version", an optional one-line "What was different, and why does theirs work?" | A-01 copies the nearest pattern under time pressure "and never learns why it works". | nice |
| R24 | Unit 9 | Optional "hard mode" mini-boss (a signature only, no comments, plus one extra branch) and an "explain a line you wrote" item. | Delight, and the research's "signals in the blue" case. | nice |
| R25 | QC6 intro | Frame it as "Nobody in this cabin has written a recipe yet. This shows Mar'tu where to start." | Overconfidence risk. A failed QC6 after an aced QC1 should feel expected, not embarrassing. | nice |
| R26 | QC1 #1 | Make it multiple choice, or provide a `█ ░` symbol palette. | Block characters can't be typed on a Chromebook. | nice |

---

## 5. Exact specs for the musts

### 5.1 Quick Check items that can actually fail on our sheets

- **QC1 #2 (rewritten):** show `Example: companion = "Gearshift"` beside the task "Make a variable named
  `character` that holds your hero, then print it." [NAME with example detection, TEXT, DF available].
  Catches A-06 `player_name`.
- **QC1 #6 (new, bug):** `Max_Mana = 18` / `print(max_mana)` and `magical affinity = 9`. Fix both [NAME].
  Catches A-06 `Pizza`/`pizza` and `pizza party`.
- **QC1 skills:** add `numbers-vs-text` and `reassign` (both already exercised by #5's `mana = mana - "3"`).
- **QC4 #6 (new):** from `roster` (a list of 3 sheets), print `roster[1]["name"]`, then spend 4 mana with
  `hero["mana"] = hero["mana"] - cost` [CMB].
- **QC5:** add one item for `loop-with-if` (print names under 10 mana [CMB]) and one for `break` (predict).
- **QC6 #1 (rewritten):** show the Example `def triple(n): result = n * 3; return result`. Task, goal only:
  "Write `armor_total(base_armor, bonus_armor)` that gives back the two added together." No body given.
  [PAR (2 fresh argument sets), RET, RNM, PNM]. This is the worksheet's Part 3 trap, rebuilt honestly. It
  catches A-01 `attack * bonus` / `return reslt` and A-06 `10 * 5` / `return 50`.
- **QC6 #7 (new):** add an early-`return` guard to a given recipe [CALL].
- **QC6 #8 (new):** a visible "already finished" helper. Call it correctly without changing it [KEEP, CALL].

### 5.2 New check and explainer rows (messages verified against CPython 3.13.18)

| Raw message | Trigger (our sheets) | Rule | What the explainer says |
|---|---|---|---|
| `NameError: name 'attack' is not defined`, raised inside a function | A-01 `total = attack * bonus` (parameters `base_attack`, `bonus_multiplier`); 6A-05 `damage` for `base_damage` | **PNM:** the missing name is a substring of a parameter, or shares a `_`-separated word with one. **Takes precedence** over the unquoted-text row. | "This recipe's ingredients are `base_attack` and `bonus_multiplier`. You wrote `attack`. Python matches names letter for letter, so use the full name from the `def` line." |
| `NameError: name 'reslt' is not defined`, inside a function | A-01 `return reslt` | **RNM, fuzzy:** the missing name is within one edit of an identifier in the lesson's Example | "You returned `reslt`, which looks like the example's `result`. This recipe's box is called `total`." |
| `SyntaxError: invalid syntax` with two bare names before `=` | A-06 `total pizzaparty = …`; 1B-04 `magical affinity = 9` | The assignment target is two words separated by a space | "A name can't have a space in it. Join the words with `_`: `magical_affinity`." |
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` with two bare names inside `( )` | A-06 `print(pizza party)` | Two adjacent names inside a call | "If `pizza party` is one name, write `pizza_party`. Names can't have spaces. (If you meant two separate things, then yes, a comma goes between them.)" |
| `SyntaxError: unterminated string literal`, where the line also has the *other* quote type after the opening one | A-01 `"Fireball'` | Mixed quote types | "You opened with `"` and closed with `'`. Python needs the same kind of quote on both ends." |

The harness `wrong_answers` for 6A-05, 6A-07 and 1B-04 should include these exact lines, so rule 2.7 #8 proves
each message fires.

### 5.3 4B-04 rewritten

- **Starter:** `spell_name = "Lantern Ward"`, `mana_cost = 6`, `required_affinity = 9`, and
  `spell = {"mana_cost": 0, "required_affinity": 0}` with the comment
  `# Replace each 0 with the matching variable: mana_cost, required_affinity`.
- **CP1:** the values come from the variables [CMB: rerun with 5 and 7].
- **CP2:** stored under its name, and Glow is kept [KEY].
- **Investigate (optional, WT "Same word, two jobs"):** "`"mana_cost"` in quotes is the label on the sheet.
  `mana_cost` without quotes is the box holding 6. Rename the box to `cost` on both lines and run. Does it still
  work? Why does the campaign keep the names the same?"
- **Catches:** `"mana_cost": "mana_cost"` (the 6B-03 message, moved earlier); literals left in place.

---

## 6. Accommodation requests (switch these on for our group)

- Offer QC1 on the first screen, and let its result (not the self-report) set the preset. "Keep it short" for
  anyone who passes.
- Instructions-light suggested after a QC pass, **with the "names to use" line always visible**.
- Worked examples and flavor collapsed, but "Why does this work?" sidebars shown as a one-line title (not hidden)
  so we notice them.
- Capstone-first and "Start from blank" offered from Unit 2 on.
- Type-first on A-stage exercises, with Assemble as the fallback.
- The DF button everywhere, including QCs, check-failure messages and projects.
- Mar'tu's slate (sandbox) with `# expect:` checks.
- Trials unlocked at each unit for hint-free or tested-out students, and the recipe track if the teacher enables
  it.
- Mentoring off unless we opt in.
- Readiness hard mode as an option.
- Required (short) spaced re-checks on anything we tested out of.

---

## 7. Keep these (don't cut in revision)

- The `[ Where should I start? (Quick Checks) ]` button. "A failed attempt costs nothing." "QC6: G4 must not skip
  this unit untested."
- CMB rerun checks and their message, plus 1C-09 showing that the checks change inputs.
- PAR with fresh values (`"Tester"`, 7, 11), RNM, and BND that reads `needed` from our code.
- 6A-07 `return-the-right-box`, which is A-01's sheet as a debugging exercise.
- 6B-02, 6B-04 and 6B-09 (mutation, rebinding, scope), plus their WT sidebars.
- The Trials format with advanced variants, T-F-3 (refactor to a dict of recipes) and T-Own (asserts).
- 5A-05's decay reveal and 5B-04's forecast. 2C-01's traceback-into-variables.
- Project 6P's composition (`hit_strength` uses `average_damage`) and dial swapping (`run_array(roster, dial)`).
- "A reveal never counts toward mastery." "Solid = passed unaided twice, including one spaced item."
- A typed Readiness Check with no reveal, and "signals in the blue → offer instructions-light in the campaign".
- No timers, leaderboards or public scores. Mar'tu's deadpan voice, kept out of the instruction lines.

---

## 8. Answers to the teacher's open questions (from our side)

- **Q1 (fast lane):** yes, and please let individual students take it (R12) even if the class doesn't.
- **Q6 (pair mode):** never pair us with others by placement without asking. If the teacher wants helpers, make
  it the opt-in apprentice role (R20).
- **Q7 (Quick Check rules):** the pass rule "every code task plus 80% of questions" is right. Show "tested out
  (provisional)" separately from "completed" in the report until the spaced re-check confirms it. Retakes can be
  unlimited only with parallel forms (R18).
- **Q8 (productive failure):** keep both hooks.
- **Q9 (Readiness stakes):** practice only, agreed. Add hard mode (R24).
- **Q12 (f-strings):** "read both, write either" is right. We'll see f-strings everywhere outside this course.
- **Q13 (Calm mode):** leave cameos on even under "Keep it short". They're one line and don't block. What we
  can't stand is click-through text, not jokes.

---

## 9. Where our asks could hurt other groups, and how to avoid it

- **Exercise-level test-out and capstone-first (R2, R11)** could let group 2's pattern-copiers skip on a lucky
  pass. Mitigation: they're offered only after a QC pass or a hint-free streak. Capstones use behavior checks (CMB,
  PAR, BND) that copying can't pass. Every skipped skill gets a required spaced item (R21) and the Readiness
  re-check (R8).
- **The recipe track (R12)** splits the class timeline: pair partners drift apart and story beats arrive in a
  different order. Mitigation: it's per student, teacher-enabled and off by default. 6A's content has no
  spoilers. The gate already verifies the fast-lane order. Side quests that use `def` in Units 3–5 appear only
  after 6A is done, which needs a small "later prerequisite" extension to rule 2.7 #2.
- **4B-04's identical names (R6)** put `"mana_cost"` and `mana_cost` side by side, which is harder for group 1,
  whose rule was "the name never goes in quotes". Mitigation: the "same word, two jobs" card is the same
  reconciliation group 1 asked for at 4A-02. 6B-03 already has the message. The campaign uses this exact shape, so
  meeting it first with support is kinder than meeting it in `spell-book`.
- **New QC items (R1)** make QCs about 3–5 minutes longer for anyone who takes one, including confident novices.
  That's the point: they make test-out honest for everyone.
- **The PNM precedence rule (R3)** must not hide the unquoted-text advice group 1 and group 2 need. It fires only
  inside a function body with a parameter that contains the missing name. Everywhere else the current row stands.
- **The sandbox (R14)** is a classroom-safety risk (joke names, real first names on our sheets). Keep it local
  only, with no sharing, no dashboard and the same PG filter as typed hero names.
- **Type-first and instructions-light defaults (R7, R13)** apply only under "Keep it short" or after a pass. The
  defaults for groups 1–3 don't change.
- **Required spaced items (R21)** cost about 1 minute per lesson, and only for students who tested out.
- **Engineering cost:** PNM, fuzzy RNM, three explainer rows, QC parallel forms and the slate. Each explainer row
  ships with harness `wrong_answers` that prove it fires (rule 2.7 #8). The explainer rows (R5) help every group.

---

## 10. In our voice

> The Quick Check button on the first screen? I'm clicking that before I read anything. I already know
> `health = 100`. But I read what it actually checks, and I could pass it by copying the word `character` off the
> question. Then I'd skip the lesson about names matching exactly, which is literally what I got wrong: I wrote
> `attack` when it was `base_attack`, and `return result` because that's what the example said. And if I make
> that mistake in Unit 6, the error box tells me to put `attack` in quotes? No. So test me, but test me on the
> thing I actually mess up.
>
> If I pass, don't just make stuff vanish. Give me the last hard one from a blank file, and the project with just
> the goal. That's more fun anyway. Let me start recipes earlier, because that's the part I actually don't get yet.
> Give me a box where I can write my own thing and put `# expect: 68` and have it tell me I was wrong (I would've
> been). And please, a button for "just pick a character for me", and don't make me the helper just because I
> finished first.
