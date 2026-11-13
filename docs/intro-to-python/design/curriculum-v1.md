# Intro to Python: curriculum draft v1 ("Mar'tu's Lessons")

**Status:** draft for the teacher's review. Nothing in the repo has changed.
**Read with:** `context/brief.md`, `context/campaign-python-inventory.md`, `personas/personas.md`,
`research/zpd-principles.md`, `research/codecademy-mechanics.md`, `design/architecture.md`, and the prototype
verifier `docs/intro-to-python/prototypes/harness.py`.
**Verified so far:** every planned exercise has a representative solution in
`design/curriculum_v1_gate.py`. That script runs the harness tokenizer over all 166 coded items (138 core, 28
optional) in course order. It found **no gate violations on the core-only path or the full path**, and it
produced the concept map in section 4. The sample quiz keys and the error messages quoted in this plan were
executed in CPython 3.13 (`design/qcheck/q.py`). Everything else here (checkpoint wording, hints, art) is
design intent. The prototype phase still has to build and verify it.

**IP rule.** Codecademy's "Learn Python 3" supplies only the learning goals and the item mix. Every premise,
name, value, line of text, and question below is original and set in Tor.

**Student privacy.** Persona evidence is cited only by anonymous sheet IDs (A-01 to A-08, B-01 to B-03). No
student names appear here, and none may appear in content or in check messages.

---

## Contents
1. Course overview (purpose, story frame, unit order, deviations, milestones)
2. Site experience (exercise loop, item kinds, checks, error explainer, accommodations, mastery map, authoring rules)
3. Units 1 to 9, item by item
4. Concept introduction map (token → first exercise)
5. Campaign Readiness Check
6. Pacing (core vs optional, periods)
7. Open questions for the teacher

---

# 1. Course overview

## 1.1 Purpose

Intro to Python gets every student into the **zone of proximal development (ZPD)** for the Python in campaign
Modules 1 and 2. A student is there when they can:
- read and explain every line of a campaign part's starter code,
- write the one-line edits without help, and
- finish each part with only the campaign's own support: numbered instructions, check messages, the error
  explainer, and an occasional hint.

The hardest parts (`spell-book`, `mana-bars`, `hold-the-barrier`) should feel like a real stretch that the
student can still win.

The course follows the sample syllabus's learning goals and item mix: lessons, quizzes, projects, articles,
optional code challenges with advanced variants, and cheatsheets. It also closes the campaign gap the syllabus
leaves open:
- dictionaries: literals, reads, nested reads, writes by key, `in` and `not in`, and lists of dicts,
- functions as values, including a dictionary that holds a function,
- `random.randint`,
- `"█" * n`,
- returning comparisons,
- early `return`,
- reading engine-helper code the student did not write.

It is built for this class's four evidence groups (personas.md):
- **G1, "Starting from zero"** (A-02, A-03, A-04): no working model of a variable yet.
- **G2, "Right shape, wrong meaning"** (A-05, A-07, A-08, B-01): eager, copy shapes rather than meanings.
- **G3, "Steady with a template"** (B-02, B-03): solid on templates, stall at a blank.
- **G4, "Ready to stretch"** (A-01, A-06): solid basics, one step from functions.

Three class-wide findings drive the design:
1. **Functions are the cliff.** Nobody wrote a working function.
2. **Nobody let the code combine values.** Everyone who reached 68 typed it in by hand.
3. **Students copy example names and write the value instead of `name = value`.** Only 1 of 11 wrote the
   requested `character = ...`.

## 1.2 Story frame

Mar'tu, a former Institute teacher, pulls "you" (the adventurer) aside in the cabin by the cherrywood mantle.
The Ley Clock ticks on the mantle above them. Each unit opens with one Mar'tu scene line and ends with a short
story beat ("Mar'tu's notes"). Lore stays out of instruction blocks. Instructions are plain English, numbered,
with code in backticks, in the same style as the campaign's.

**Sample opening (course map, first visit):**

> *Mar'tu draws you aside, away from the fire. Only their tired yellow eyes show under the purple shroud.*
>
> **Mar'tu:** "Hi. It is me, Mar'tu. Before we continue on our adventure you must learn some of the language we call, Python."
>
> "The ley-lines do not listen to shouting. They listen to instructions. Every barrier I raise is a few lines of Python. Every spell in your book will be too."
>
> "I taught at the Institute for many years. Most of my students were not from another world. You will still do fine, yes?"
>
> "We start small. One line, then two. When you are stuck, I will offer help. When you are not stuck, I will leave you alone. Both are allowed."
>
> **Lucky** *(from across the room)*: "What's in it for me?"
>
> **Mar'tu:** "Existing."
>
> [ Begin Unit 1 ]   [ Where should I start? (Quick Checks) ]   [ Help options ]

**Mar'tu's voice rules (all text):**
- Short sentences. Dry, grim but caring, deadpan.
- At most one ", yes?" per screen (a heuristic).
- The accent shows in rhythm and word order, never in misspellings, so read-aloud and English learners are not
  penalized.
- **Mar'tu's voice appears only in the Learn pane's first and last line, pass lines, hint openers ("Mar'tu
  leans closer…"), and story beats.**
- Checkpoint text, check messages, and glossary entries are plain standard English.
- Mar'tu never says "Wrong" or "You're a natural". Wise feedback looks like this: *"Your spell fizzled. Good.
  Now we can see why, yes? I would not give you this if I thought you could not mend it."*

**Party cameos.** Each cameo is one line, outside instructions, and can be hidden with Calm mode.
- **Oogrish:** "Steady, now." He also delivers the encouragement line after 3 failed runs: "Steady, now. Read
  the last line of the error first."
- **Gearshift:** "Math checks out." (pass line)
- **Bomb Shell:** clipped pass lines ("Works." "Shield up.") and the debugging exercises. "That latch hates
  me."
- **Lucky:** owns the side quests ("What's in it for me?") and the campaign-link box ("What's in it for me?
  This shows up in the campaign as…").

**World data used throughout** (real values from `content/campaign/characters/*.json` and the brief):
- **Chalk wall** (hours between bursts): `[48, 48, 47, 46, 44, 41, 37]`. The gaps between them are 0, 1, 1, 2,
  3, 4, so "the decay is accelerating".
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
- **Near-transfer rule:** the course rehearses the campaign's shapes with different names. For example, it uses
  `learn_spell`, `cast`, `lantern_ward` and `show_on_ley_board`, never `add_spell`, `cast_spell`,
  `strengthen_magic` or `print_prompt`. That way the campaign parts are not spoiled (architecture Q7).

## 1.3 Units in order, with rationale

| # | Unit (in-world title) | Syllabus source | Why it sits here |
|---|---|---|---|
| 1 | **Hello World: "Words by the Fire"** | Hello World | Syllabus order. Split into three short lessons so G1 gets a win in the first two minutes and Run feedback after every step. Introduces `"█" * n` early (deviation D4). |
| 2 | **Control Flow: "The Ley Clock Decides"** | Control Flow (+ Errors lesson) | Syllabus order. `random.randint` lives here, as in the syllabus's random-answer project. The Errors lesson stays at the end of the unit, as in the syllabus. |
| 3 | **Lists: "The Chalk Wall"** | Lists | Syllabus order. Trimmed to what the campaign and later units need. The rest is optional (D7). |
| 4 | **Dictionaries: "Stat Sheets and Spell Books"** | *new* (campaign gap) | **Inserted (D1).** Dictionaries are the campaign's main data structure. Placed right after Lists, they come back in Loops, Functions and Strings (spaced practice), and Loops can walk a list of dicts the way the campaign walks `party.members`. |
| 5 | **Loops: "Every Member of the Party"** | Loops | Syllabus order. Loops walk the roster of hero dicts. |
| 6 | **Functions: "Mar'tu's Recipes"** | Functions | Syllabus order. Expanded to three lessons because functions are the class's cliff. Lesson 6C covers functions as values and a dict holding a function (D2). |
| 7 | **Code Challenges (optional): "Trials of the Yard"** | Code Challenges | Syllabus order (after Functions, because every challenge is "write this function"). Adds a Dictionaries set (D8). |
| 8 | **Strings: "Runes and Ribbons"** | Strings | Syllabus order (last). It recycles dicts and functions, and revisits `"█" * n` and `.lower().capitalize()` chaining. |
| 9 | **Campaign Readiness Check: "Before We Continue"** | *new* | **Added (D9).** Operationalizes "arriving in the ZPD" (section 5). |

## 1.4 Deviations from the syllabus (each needs the teacher's approval)

| ID | Change | Reason |
|---|---|---|
| **D1** | Insert **Unit 4 Dictionaries** between Lists and Loops. | The campaign leans on dicts in every Module 2 part, and the syllabus has none. ZPD P1 asks for a dict unit "before Functions finishes". Putting it right after Lists means: (a) the list → dict contrast is fresh ("a list remembers order, a dict remembers meaning"); (b) Loops can walk a **list of dicts** (`for member in party.members:`); (c) Functions can take a hero dict (`get_mana_bar(caster)`); (d) dicts come back in 4 later units (spacing, P13). No syllabus unit moves relative to another. |
| **D2** | Functions gets a third lesson, **6C "Spells You Can Hand Over"** (functions as values, a dict holding a function, passing a function without `()`), plus two campaign-shaped rehearsals. The syllabus's lambda and `map()` articles stay, as optional deep dives. | The campaign needs `add_spell(..., strengthen_magic)` and `spell["spell_function"](caster)`. The syllabus covers functions as values only through lambda and `map()`, which the campaign never uses. |
| **D3** | One string method, `.lower()`, is introduced in **Control Flow** (exercise 2A-04), for case-safe comparisons. Everything else about string methods stays in Strings. | Comparing answers in any case is a control-flow use. It makes the `input()` article usable, and it previews Module 1's `.lower().capitalize()` lines. Strings revisits it in depth. |
| **D4** | **String repetition `"█" * n`** appears in Unit 1 (1C-08), with arithmetic. It comes back in Units 5, 6 and 8. | `*` is already being taught there, and the block-letter project needs it. The campaign's `mana-bars` part depends on it, including the `(max - mana)` parentheses. Spaced over four units instead of one. |
| **D5** | A **debugging strand** starts in Unit 1. Every lesson ends with a "Broken spell" exercise. The syllabus's full Errors lesson stays in place at the end of Unit 2. KeyError and AttributeError are added in Unit 4, IndexError in Unit 3, and `None` errors in Unit 6. | Persona evidence: unclosed and missing quotes (A-02, A-03, A-04, A-05, A-08, B-01), and `def` versus `=` (A-02). Research P11 asks for "Broken spell" debugging in every unit. |
| **D6** | Unit 1's single syllabus lesson becomes **three short lessons** (1A, 1B, 1C). | Small steps and early wins for G1. The structure changes, not the order. |
| **D7** | Some syllabus items are marked **OPTIONAL** but kept. See the table below. | The campaign doesn't use them, and class time is limited (section 6). All of them stay available for stretch. |
| **D8** | Code Challenges gets a **Dictionaries** set. | It fills the same gap as D1. |
| **D9** | Add the **Campaign Readiness Check** (Unit 9), with a spaced re-check before Module 2. | This is the operational ZPD definition (research §4.5). |
| **D10** | The `input()` article becomes interactive (the replay shim in architecture §4.2). | Fixes Codecademy's known weakness. The content is otherwise the same. |

Items D7 marks optional:

| Unit | Optional items |
|---|---|
| 1 | Clock Math article (`**`, `%`, `//`), the Ward Sign print-art project, the `input()` article |
| 2 | `match` article, Three Roads project |
| 3 | "More List Tools" lesson (insert/pop/remove/max/min/sum), the second Lists quiz, the Basement Inventory project, the Tuples and `zip()` articles |
| 5 | Comprehensions and `continue` lesson (5C) |
| 6 | lambda, `map()` and "Two things back" (multiple returns) articles |
| 7 | the whole Code Challenges unit (as in the syllabus) |
| 8 | the Water-Stained Log cleanup project and the Institute Cipher project |

## 1.5 Milestones

- **Ready for Module 2.** All core items plus the Campaign Readiness Check (section 5). This is the default goal.
- **Ready for Module 1 (fast lane, needs the teacher to turn it on).** Units 1 and 2 (core), then Lesson 6A and
  exercise 8B-02 (`chain-the-spells`).
  - This route works because Lesson 6A is built from Unit 1–2 concepts only, and 8B-02 adds just one token
    (`attr:capitalize`). The gate script checks this.
  - The teacher can therefore send students to Module 1's coding parts after about 9 periods, then return for
    Units 3–9 before Module 2. See open question Q1.

---

# 2. Site experience

## 2.1 The exercise loop (how every lesson feels)

Every lesson has the same shape, so the routine itself becomes familiar. This is PRIMM / Use-Modify-Create
(research P2, P3).

| Step | What the student sees | Notes |
|---|---|---|
| 0. **Mar'tu remembers…** | 1–2 recall items from at least two lessons back (e.g., "Which line makes a box?"). | Unscored and skippable. Missed items feed the spaced queue and the mastery map. Dictionaries and functions come back here in every unit after they are taught. |
| 1. **Learn pane** | Mar'tu's explanation (≤ 120 words before the first action), then a labeled **Worked example** with Run and Step through. | Example names and values are **visibly different** from the task (G2 copying evidence). The example is collapsed under the "Keep it short" preset. |
| 2. **Predict** | A one-click multiple-choice or "type what it prints" prompt *before* Run. | Free. It is a thinking prompt, not a test. Its accuracy feeds the teacher's signals (research §4.6). |
| 3. **Run and compare** | "Were you right? Which line surprised you?" | |
| 4. **Investigate** | 1–3 "change X and run" or "which line does Y?" questions. | |
| 5. **Modify / Make** | Numbered checkpoints, one action each, checked in order. | Scaffolds fade within each unit: comments with blanks → one blank → a whole line → a whole body. |
| 6. **Broken spell** | A debugging exercise in every lesson. | |
| 7. **Wrap** | In pair mode, a **solo checkpoint** ("Show Mar'tu"). Then a pulse: *too easy / just right / too hard*. | |

**On the exercise screen (architecture §3.1):**
- Checkpoints show as ✓ passed, ● active, ○ locked.
- Each Run re-checks every checkpoint, so a regression is caught.
- The failing check's message appears under the active checkpoint, as one sentence of behavior-based feedback.
- **Hint ladder, per checkpoint:**
  1. **Point:** where to look.
  2. **Teach:** the concept, with a tiny example that is *not* the answer.
  3. **Show:** the bottom-out line.
  - After a Show, a **your-turn variant** follows (same pattern, new names and values) and must be typed.
  - Rungs need about 10 seconds or a Run between them. Hint use is private (the teacher sees it).
- **Proactive offer:** after 3 failed runs on one checkpoint, or 4 minutes with no progress, Mar'tu asks: "You
  have been staring at that colon for a while. Want a nudge, yes?" Students can dismiss it. Both numbers are
  heuristics to tune.
- **Compare with Mar'tu's version** unlocks after 5 minutes, *or* 4 failed runs, *or* when the ladder is used
  up:
  - "Retype it" is the default.
  - Checkpoints passed after a reveal are marked *assisted*.
  - A twin exercise is queued into a later warm-up.
  - A reveal never counts toward mastery.

**How scaffolds fade across the course.** The function strand shows the pattern:
1. 6A-03: the starter gives `def … : pass` and the exact line to type.
2. 6A-04/05: one-line bodies, with the example shown.
3. 6B-03: comments say "replace each placeholder with the matching parameter".
4. 6B-07: comments name the expressions but not the code.
5. 6C-05: only numbered comments (campaign style).
6. Readiness mini-boss: numbered comments, hints capped at level 2.
7. Trials: a signature only.

After a hint-free pass, the next similar exercise offers "Start from blank". After repeated failures, it offers
"Assemble it" or one more comment (contingent fading, research P5, P8).

**Example walk-through (exercise 1C-08 `repeat-a-mark`).**
1. *Predict:* What does `print("█" * 3)` show? (`███` / `█3` / an error)
2. *Run.*
3. *Investigate:* What does `"█" * 0` show? `"█" * 1`?
4. *Modify:* Make Gearshift's full bar: 20 blocks.
5. *Make:* `bar = "█" * mana + "░" * (max_mana - mana)`, printed inside `[` `]`.
6. *Lucky's side quest:* add ` 3/5` at the end with `str()`.

## 2.2 Item kinds

| Kind | Shape | Grading | Support |
|---|---|---|---|
| **Lesson** | 5–11 exercises: warm-up, then the PRIMM order above. | Auto-checked checkpoints. | Full: hints, another way, tracer, assemble, compare. |
| **Quiz** | 6–10 questions of five types: **mc**, **predict**, **fill**, **parsons**, **bug**. One per card. | Delayed review: the score first, then an explanation for each wrong choice, with "Review this" links. Unlimited retakes with reshuffled choices. A "Ready" badge appears at 70% (it never blocks). | No hints during the quiz. A "Show choices" accommodation turns a predict question into multiple choice. |
| **Project** | A task checklist under group headings, with one editor and optional stretch goals. | Every task is auto-checked where possible. | Light: hints unlock after the first failed run. A text walkthrough reveals one step per task. |
| **Challenge** | A function signature plus a table of tests (visible, then hidden). Core and advanced variants. | Test table. A hidden test names its label ("an empty list"), not its values. | Light. |
| **Article** | Readable page with runnable examples, plus an optional try-it exercise. | "Mark as read" completes it. | Full on the try-it. |
| **Cheatsheet** | "Mar'tu's chalk notes": a concept, a snippet, its output, and a note. Printable. Each entry links back to the exercise that taught it. | No grading. | |
| **Quick Check (test-out)** | 3–6 items per unit, about 10 minutes, tagged by skill, always including campaign idioms. | Pass all skills: the unit is *Tested out (provisional)* and the student gets a one-screen "Mar'tu's notes" recap. Pass some skills: the student skips only those lessons. Fail: no penalty, and support defaults are set from the result. | None: no hints, tracer or compare. |
| **Readiness Check** | 12 unaided items plus a supported mini-boss (section 5). | Per-skill routing. | Unaided items get none. The mini-boss allows up to 2 hint levels. |

## 2.3 Check pattern library (used by every checkpoint below)

Checks test **behavior**, not text:
- They call the student's functions with fresh values.
- They re-run the program with changed inputs.
- They accept any quoted text the student picks, so silly, personal and in-world values all pass (G1, G2).

Messages are one sentence. Each says what the code did, what was expected, and the next step (research P10).

| Code | Pattern | Example message (student-facing) | Catches (persona evidence) |
|---|---|---|---|
| **NAME** | The variable or function has the exact required name. Near misses are recognized: the example's name (`companion`, `player_name`), case variants (`Character`), typos one edit away (`charcter`). | "You used the example's name `companion`. This task asks for `character`." / "Python matches names letter for letter: you wrote `Health`, the task needs `health`." | A-05, A-06, A-07, A-08 `player_name`. A-08 `heath`, A-05 `Powrup`, B-01 `power_UP`. B-02/B-03 `Pizza`/`pizzas`. |
| **TEXT** | The value is a non-empty `str`. Any text is accepted. If the run crashed with a NameError on an assignment line, the explainer says the text needs quotes (§2.4). | "`character` holds `7`. This step wants text in quotes, like `"Zelda"`." | A-08 `kratos`, A-05 `fireball`, B-01's unquoted joke name. |
| **NUM** | The value is an `int`, not `"3"`. | "`armor_bonus` holds the text `"3"`. Numbers don't need quotes. With quotes, Python can't do math with it." | Quoting mix-ups. |
| **CMB** | "Let the code combine it": `_rerun(values={...})` re-executes the program with changed inputs and expects the result to follow. Backed by an AST check (`_assigned_from_expression`, `_uses`). | "When I changed `lantern_count` to 7, `total_cost` stayed 22. Build it from the variables (`lantern_cost + rope_cost`), not a number you worked out." | Everyone's hard-coded 68. A-05, A-07, A-08 `pizzas * 48`. |
| **PAR** | Calls the student's function with **two or more fresh argument sets** the task never mentions (`"Tester"`, 7, 11). | "`warn("Tester")` printed `Lucky, get inside!`. Use the parameter `hero_name` instead of a name you typed." | A-06, A-07, B-02 `10 * 5`. A-08 `25 * 2`. A-01 `attack * bonus`. |
| **RET** | The function **returns** the value. Detects `None` and print-instead-of-return. | "`max_mana_for(9)` printed 18 but handed back `None`. Use `return total` so the caller gets the number." / "`max_mana_for(9)` handed back `None`. Is the `return` line missing?" | B-02 blank `return`. A-07 "return value = 3 + 4". |
| **RNM** | A NameError raised *inside* a function names the example's variable. | "You returned `result`, but this recipe's box is called `total`." | A-01 `return reslt`. |
| **DEF** | `def` was used to make a variable. This shows up as a SyntaxError on a `def name =` or `def (` line, and is handled by the explainer. | "`def` makes a recipe (a function). To make a box (a variable), write `name = value`." | A-02 `def ("character")`. |
| **BND** | Boundary test at `needed - 1`, `needed`, `needed + 1`, and "exactly enough mana". `needed` is read from the student's own code, so any chosen difficulty passes. | "With a roll of 12 and `needed = 12`, your check said fail. Exactly enough should pass: use `>=`." | The campaign's `<` vs `<=` and `>=` boundaries. |
| **RND** | `_rerun(rolls=[...])` scripts what `random.randint` returns and records its arguments. | "`roll_die(6)` rolled `random.randint(1, 20)`. Use the parameter: `random.randint(1, die_size)`." / "A d6 has faces 1 to 6, and `randint` includes both ends, so use `random.randint(1, 6)`." | Literal sizes, the exclusive-range belief. |
| **CALL** | Setup helpers (`show_on_ley_board`, `scout.step`, `mar_tu_says`, `draw_bar`) record every call. Checks read the record. | "`step_south()` moved the scout north. Use the direction in the function's name." | Copy-paste branches. |
| **STO** | Inside the named function, a call's result is assigned to a variable, and that variable is passed on (AST check). | "Store what `get_greeting()` returns in a variable first, then pass that variable to `show_on_ley_board()`." | The campaign's "the line is stored in a variable" check. |
| **NOP** | A function is handed over as a value. Detects `None` where a recipe was expected. | "You ran `warm_hands(lucky)` and handed over what it gave back (`None`). Hand over the recipe itself: `warm_hands`, no parentheses." | The campaign's `strengthen_magic` without `()`. |
| **LOOP** | Re-runs with a roster or list of a different length. Output must grow or shrink with it. | "With 5 heroes in `roster`, only 4 lines appeared. Use a `for` loop so every hero gets a line." | Hard-coded repetition. |
| **KEEP** | Code marked "already finished" is unchanged (AST compare). | "`draw_bar` changed. It is already finished, so leave it as it is." | Campaign reading discipline (P19). |
| **KEY** | Dictionary keys are exactly as specified (quoted, spelled, cased). | "`gearshift` has a key `"Max_Mana"`. The sheet uses `"max_mana"`, all lowercase." | Exact-name evidence. |

**Proposed helper additions to `course_helpers.py` and the harness.** The current harness lacks these, so each
check falls back to the AST helpers where noted:
- `_rerun(values=None, rolls=None, stdin=None)` re-executes `_source` in a fresh namespace:
  - It replaces the value of the first top-level assignment to each named variable.
  - It scripts and records `random.randint`.
  - It returns `(namespace, printed_lines, randint_calls)`.
- `_calls(helper_name)` returns the recorded calls to a setup helper.
- `_func_ast(name)` returns the AST of a student function (for STO and BND).
- `_near_names(name)` returns case, typo and example-name near misses (for NAME).

**Authoring rule from the harness (stays in force):** a check must remain true as later checkpoints are
completed. Use `'48' in _lines()`, not `_lines() == ['48']`.

## 2.4 Error-explainer additions, mapped to the class's actual slips

These go into `explain.ts`. They were checked against Python 3.13 messages.

| Raw message | Trigger on the sheets | What the explainer says |
|---|---|---|
| `SyntaxError: unterminated string literal` | A-02 `("Fire Ball`, A-03 `"Fierball.`, A-04 `"Fireball` | "A quote opened on line N but never closed. Quotes come in pairs: one before the text, one after." |
| `NameError: name 'kratos' is not defined` on a line with `=` or `print(` | A-05, A-08, B-01: unquoted text | "Python looked for a box named `kratos` and found none. If you meant the words, put them in quotes: `"kratos"`." |
| `SyntaxError: invalid syntax` on `def (`, or `expected '('` on `def name =` | A-02 `def ("character")` | "`def` makes a recipe (a function). To make a box (a variable), write `name = value`, with no `def`." |
| `SyntaxError: cannot assign to literal here. Maybe you meant '=='…` on `"weapon" = …` | A-02 name in quotes | "The name of a box never goes in quotes. Write `weapon = "Telegun"`." (Python's own hint misleads here.) |
| `NameError` on `name - value` | A-04 `chicken_sandwich - "Fireball` | "To put a value in a box, use `=`. The `-` sign subtracts." |
| `TypeError: can only concatenate str (not "int") to str` | campaign `+ str(...) +` | "You glued text to a number. Wrap the number in `str()` first." |
| `TypeError: unsupported operand type(s) for -: 'str' and 'int'` | campaign `"░" * a - b` | "Python did `"░" * a` first, then tried to subtract from text. Put the subtraction in parentheses: `"░" * (a - b)`." |
| `TypeError: '>=' not supported between instances of 'int' and 'str'` | `needed = "15"` | "One side is a number and the other is text. Remove the quotes from the number." |
| `KeyError: 'dexterity'` | dict work | "The dictionary has no key spelled exactly `'dexterity'`. Check spelling, capitals, quotes, and whether it lives one level deeper (`["abilities"]["dexterity"]`)." |
| `AttributeError: 'dict' object has no attribute 'mana'` | `hero.mana` | "Read a dictionary with square brackets: `hero["mana"]`." |
| `AttributeError: 'list' object has no attribute 'join'` | `words.join(" ")` | "`join` belongs to the separator: `" ".join(words)`." |
| `TypeError: 'NoneType' object is not callable` | calling `chosen = warm(h)` later | "This box holds `None`, not a recipe. Did you run the function (with `()`) when you meant to hand it over (no `()`)?" |
| `TypeError: can only concatenate str (not "NoneType") to str` | missing `return` (B-02) | "A function gave back `None`. That usually means it has no `return` line." |
| `TypeError: 'NoneType' object is not subscriptable` | `wall.sort()[-1]` | "`.sort()` changes the list and gives back `None`. Use `sorted(wall)` to get a new list." |
| `TypeError: list indices must be integers or slices, not str` | `roster["Lucky"]` | "`roster` is a list, so use a position number like `roster[3]`. Names work as keys in dictionaries." |
| `TypeError: 'str' object does not support item assignment` | `word[0] = "C"` | "Strings can't be changed in place. Build a new one: `"C" + word[1:]`." |
| `IndexError: list index out of range` | `chalk_wall[7]` | "This list has 7 items, at positions 0 to 6. Position 7 doesn't exist." |
| step-limit error (course runs) | infinite `while` | "Line N ran 200,000 times. Does something inside the loop ever make the condition False?" |

## 2.5 Accommodations: opt-in layers, each removable

The default for every layer comes from the student's chosen preset, which they can switch at any time:
- **"Show me more":** examples open, tracer open, warm-ups on, Assemble-it offered.
- **"Keep it short":** examples and flavor collapsed, Quick Checks suggested.

Placement can suggest a preset, but placement is provisional. The two preset names are neutral and descriptive.
Paths are never named by ability, and nothing is called "remedial".

| Feature | What it does | Who it serves (evidence) | Why it won't impede others / how it fades |
|---|---|---|---|
| **Explain it another way** | 2–4 pre-written angles per concept: *analogy* (box with a label, recipe), *picture* (memory-box diagram), *step-by-step* (a trace table), *in Tor* (stat sheets, spell books), *shorter* (two sentences), *from the campaign* (the real snippet). | G1 asked for "the same idea from another angle, not louder" (A-02, A-03, A-04). G2 needs meaning rather than shape. | Collapsed. Offered automatically after the first failed check (G1 need), otherwise on demand. Costs nothing if never opened. Usage is logged so weak angles can be retired. |
| **Glossary** | Hover or tap on `[[term]]`. Plain definition first, jargon second, plus a tiny example. Covers *string, variable, parameter, argument, return, key, index, concatenate, None…* | G1: "Parameter, argument, return: those words mean nothing to me yet." | Inline and dismissible. Never interrupts. |
| **Step-through tracer ("Mar'tu's ledger")** | Python Tutor-style stepping. Shows the boxes and their values, nested dicts as boxes in boxes, and a call/return arrow showing where a return value lands. | G1 traced by adding the code's constants (A-03, A-04 `10 + 5`) and lost the return value (A-03, A-04 `gold_value`). G2: A-07 "return = 3 + 4". | Open by default only under "Show me more". Hidden in Quick Checks. Experts can ignore it. |
| **Read aloud** | Web Speech reads Mar'tu's text and the instructions. An authored `say` text reads code lines naturally. | G1 fast readers who hunt for code. English learners. | A button. Hidden if the device has no voices. |
| **Assemble it instead (Parsons)** | Available on **any editor that is blank or still matches the starter after about 90 s**, and on every multi-line task. Adaptive: after 2 failed checks it removes a distractor or merges two blocks. Indentation is part of the puzzle. Distractors come from real misconceptions (`<=`, missing `()`, unquoted `option 2`, `caster["magical_affinity"]`). | G2 left functions blank or erased them (A-05, B-01). G3 stalls at a blank (B-03 blank Part 3). | Offered, never forced. Lessons accept it, but **mastery needs typing**: Quick Checks, solo checkpoints and the Readiness Check are typed. |
| **Proactive hint offers** | After 3 failed runs on the same checkpoint, or 4 minutes without progress, Mar'tu offers the next rung. | G1 won't ask. G3 "would rather leave a blank than guess" (B-02, B-03). | Shows only on failure or idle signals. One click dismisses it. Turns off after a hint-free pass streak. |
| **Hint ladder + your-turn variant** | Point → teach → show, then a fresh variant to type. | G1: "hints that teach before they reveal, then a fresh one to try". | Private. Never scored. Spaced against gaming (research P16). |
| **Pair mode with solo checkpoints** | Two seats (anonymous ids). Prompts: "Navigator predicts, driver runs", "Swap seats", "Explain to your partner why this passed". Each lesson ends with one **"Show Mar'tu"** solo checkpoint that each seat completes alone, framed as a chance to show off. | A-03 and A-04 worked as one unit. B-02 and B-03 share handwriting. Their individual levels are unknown. | Off by default. Turned on by the teacher or by a pair. Solo checkpoints are never framed as cheating detection. |
| **Instructions-light mode** | Shows only the goal sentence and the check names. Starters are trimmed to the signature where safe. | G4 (A-01, A-06): "redoing variables I already know". | Suggested only after a hint-free pass streak or a Quick Check pass. One click to turn it off. Never on by default for G1–G3. |
| **Collapsible examples and flavor; Calm mode** | Collapse worked examples and story lines. Calm mode hides cameos. | G4 "long worked examples I can't collapse". | Remembers the choice. Story beats stay one tap away, so the plot is never lost. |
| **Default for creative prompts** | A "Can't decide? Use Mar'tu's pick" button on every open prompt. | A-01: "not my favorite I just can't think of a character". | Optional. Every quoted value is still accepted. |
| **Quick Check test-outs (per skill, provisional)** | Described in §2.2. Always includes campaign idioms (dicts, `return a >= b`, functions as values). | G4. Also anyone who feels ready. | A failed attempt costs nothing. Every pass is re-verified by spaced warm-ups and the Readiness Check, because the A-01 and A-06 sheets show they would skip functions too early. |
| **Lucky's side quests (bonus) and the Trials unit** | One optional extra per exercise ("What's in it for me?"), plus challenges with advanced variants and write-from-blank Trials. | G4 (A-06's unprompted mini-program). Also offered to anyone on a fast, hint-free streak (boredom signal, research P18). | Never required. Framed as side quests, not "advanced". |
| **"Why does this work?" sidebars** | Deep dives: precedence, mutation through a parameter, why keys are unique, why `.sort()` returns `None`. | G4. | Collapsed. |
| **Skill / mastery map** | "Mar'tu's chalk wall of skills": a tally per skill marked *not yet / practicing / solid / tested out*. Solid means passed unaided twice, including one spaced item. | G3: "a checklist of what I've already mastered". | Private to the student and the teacher. No comparison view. |
| **Warm-up lesson 1W** | What text is, why quotes matter, what an error looks like, what Run does, where the symbols are on the keyboard. | G1. | Optional. Default-on only under the "Show me more" preset. |
| **No timers, leaderboards or public scores** | Nothing on the site is timed, ranked or public. | G1 ("comparison with faster classmates"). | Applies to everyone. |

## 2.6 Skills tracked on the mastery map

The map shows the skills grouped by unit. Each skill's evidence comes from its tagged checkpoints, quiz items,
and Quick Check items.

| Unit | Skills |
|---|---|
| 1 | `print-text`, `quote-text`, `make-variable`, `exact-names`, `numbers-vs-text`, `combine-values`, `reassign`, `concat-str`, `repeat-string` |
| 2 | `compare`, `boundary`, `if-else`, `elif-chain`, `and-or-not`, `randint`, `read-traceback` |
| 3 | `list-make`, `list-index`, `list-append-len`, `list-nested`, `range-slice-sort` |
| 4 | `dict-make`, `dict-read`, `dict-write`, `dict-in`, `dict-key-from-variable`, `dict-nested`, `list-of-dicts` |
| 5 | `for-each`, `accumulate`, `loop-with-if`, `while-loop`, `break` |
| 6 | `def-call`, `replace-pass`, `param-use`, `return-value`, `return-right-name`, `store-then-pass`, `return-comparison`, `early-return`, `func-takes-dict`, `read-helper`, `func-as-value`, `call-stored-func` |
| 8 | `string-index-slice`, `string-methods`, `chain-methods`, `split-join`, `fstring-read` |

The campaign-critical skills (the Readiness Check must see them solid):
- `combine-values`, `concat-str`, `repeat-string`
- `boundary`, `elif-chain`, `randint`
- `dict-read`, `dict-write`, `dict-nested`, `dict-in`, `list-of-dicts`
- `replace-pass`, `param-use`, `return-value`, `store-then-pass`, `return-comparison`, `early-return`
- `func-as-value`, `call-stored-func`, `read-helper`, `chain-methods`

## 2.7 Authoring rules (verifiable)

1. **Concept gate.** Code a student sees (starter, example, solution, partials, quiz code, cheatsheet) uses only
   tokens introduced earlier in course order, or in the same exercise.
2. **Core-only rule (new).** Core items may rely only on tokens first introduced in **core** items. Optional
   items may use tokens from earlier optional items only when they list those items as prerequisites; the UI
   then shows a recap card. The gate script checks the core-only path separately (section 4).
3. **Setup gotcha (found while verifying).** The tokenizer exempts attributes on names defined in hidden
   `setup`. So if `chalk_wall` came from setup, `chalk_wall.append(...)` would *not* register as
   `attr:append`. Data whose methods a lesson teaches must be built in the **visible starter**. Only engine-like
   helpers (`scout`, `ley_board`, `show_on_ley_board`, `draw_bar`, `light_lantern`, `show_mana`) live in setup.
4. **Engine names are off-limits** as student variables: `party`, `user`, `stage`, `print_prompt` and the other
   GUARD names. The course uses `roster`, not `party`. In the harness those names are always defined, so they
   would hide NameErrors. Course runs use the plain prelude (architecture §4.2).
5. Examples use **different names and values** from their task, and are labeled "Example".
6. Checkpoint text: one action, ≤ 2 sentences, numbered by the UI, code in backticks. Flesch-Kincaid grade ≤ 7
   is the target (the harness warns above 9). Mar'tu's text before the first action: ≤ 120 words.
7. Lore never appears inside a checkpoint, a check message, or a quiz question's correct-answer logic. Quizzes
   never test lore.
8. Every checkpoint has ≥ 2 hints (target 3: point, teach, show) and at least one wrong answer from the class's
   evidence in `wrong_answers`, so the harness can prove it fails with the intended message.
9. Never print a function object or a random value in an `example_output`, because those vary between runs.
10. Formatting is off for the course, because Ruff's double-quote rewrite breaks escape lessons (architecture
    §4.7).

## 2.8 Legend for section 3

- **Item flags:** **[C]** core (everyone) · **[O]** optional (stretch or support). Minutes are for a typical
  student; G1 may take about 1.4× and G4 about 0.6×.
- **Stages:** **P** predict · **R** run · **I** investigate · **M** modify · **Mk** make · **A** assemble
  (Parsons) · **D** debug ("broken spell") · **PF** productive-failure hook (≤ 3 minutes, ungraded).
- **Hooks:**
  - **AW**[angles] explain-another-way · **TR** tracer · **PA** Parsons fallback (distractors listed)
  - **BQ** Lucky's side quest · **DF** default-value button · **PR** pair-mode prompt
  - **SOLO** the lesson's solo checkpoint · **WT** "Why does this work?" sidebar
  - Glossary, read-aloud and proactive hints are on every exercise, so they aren't repeated.
- **Checks** refer to the codes in §2.3. **"Catches"** cites persona evidence by sheet ID.
- **intro:** lists the exact harness tokens the exercise introduces. "—" means none new.

---

# 3. Units

## Unit 1 · Hello World: "Words by the Fire"

**Mar'tu's framing.** "Every spell begins as words. Python is fussy about words. More fussy than Lucky is
about glug, yes? Tonight we learn three things: how to say something, how to keep something in a box, and how
to let Python do the sums."

**RPG tie-in.** Mar'tu's chalk wall, the party's stat sheets, and the night's supplies all become printed lines
and labeled boxes. Mana bars appear here for the first time.

**Learning objectives (syllabus-aligned). Student can…**
1. Use `print()` with text in matching quotes, print several lines in order, and print a blank line.
2. Write `#` comments and use them to switch a line off.
3. Write a multi-line string with triple quotes.
4. Create a variable with `name = value`, naming it **exactly** as asked, quoting text and not numbers, and
   tell `name` apart from `"name"`.
5. Reassign a variable, including `mana = mana - cost`, and use `+=` / `-=`.
6. Use `+ - * /` (and know `/` gives a decimal), with parentheses for order. **Optional:** `** % //`.
7. Turn a word problem into labeled variables (how many? how much each?) and **let the code combine them**.
8. Join text with `+`, converting numbers with `str()`.
9. Repeat a string with `*` to draw a bar.
10. Recognize and fix a missing or unclosed quote (SyntaxError), unquoted text and wrong case (NameError), and
    text plus a number (TypeError).

**Campaign links.**
- Obj 1, 4, 10 → `program-movement` / `program-dialogue-options` (quoted strings `"left"`, `"option 1"`).
- Obj 5, 7 → `hold-the-barrier` (`caster["mana"] = caster["mana"] - spell["mana_cost"]`) and `mana-bars`
  (`caster["max_mana"] - caster["mana"]`).
- Obj 8 → the `mana-bars` return line (`"Mana [" + filled + empty + "] " + str(...)`).
- Obj 9 → `mana-bars` (`"█" * caster["mana"]`).

**Items in order**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Article 1-A1 "How Mar'tu Teaches" (making the most of the course) | C | 5 |
| 2 | Lesson 1W "Before the First Spell" (warm-ups) | O (default-on under "Show me more") | 10 |
| 3 | Lesson 1A "Words in Quotes" | C | 25 |
| 4 | Lesson 1B "Boxes With Labels" | C | 22 |
| 5 | Lesson 1C "Math and Glue" | C | 38 |
| 6 | Article 1-A2 "Clock Math" (`**`, `%`, `//`) | O | 12 |
| 7 | Quiz 1 "Chalk Quiz" | C | 10 |
| 8 | Project 1P1 "The Night Watch Ledger" | C | 40 |
| 9 | Project 1P2 "The Ward Sign" | O | 25 |
| 10 | Article 1-A3 "Asking the Traveler: `input()`" | O | 15 |
| 11 | Quick Check 1 | O (test-out) | 10 |
| 12 | Cheatsheet 1 | reference | – |

### Article 1-A1 "How Mar'tu Teaches" [C, 5 min]

This is our version of the syllabus's "making the most of the course" article. It is one screen with a
labeled picture of the exercise screen and covers:
- Run, and what checkpoints are;
- the hint ladder ("Mar'tu leans closer…"), and that hints are private and never cost anything;
- Explain it another way, Step through, and Assemble it;
- Compare with Mar'tu's version, and why "Retype it" beats copying;
- Quick Checks;
- the cheatsheet;
- the Help options presets;
- pair mode;
- that nothing on the site is timed.

It ends with a "Where should I start?" choice: start Unit 1, or take Quick Check 1. There is no exercise.

### Lesson 1W "Before the First Spell" [O, warm-ups, 4 × 2 min]

- **1W-01 `what-run-does`**: intro `call:print` `const:str` · R. Press Run. The words appear in the console.
  Then press Run again: nothing breaks. CP1 prints `glug`.
- **1W-02 `what-an-error-looks-like`**: D. Run a line with a missing quote and read the friendly explainer. The
  point is that red text means "Python needs help reading this", not "you failed". CP1: fix it.
- **1W-03 `why-quotes`**: P→R. `print("Lucky")` versus `print(Lucky)`. Predict which one works.
- **1W-04 `keyboard-symbols`**: M. Find `"`, `(`, `)`, `_`, `#` and `=` on a Chromebook keyboard by typing
  `print("( ) # _ =")`.

### Lesson 1A "Words in Quotes" [C]

*Mar'tu asks (first lesson, no recall):* "Have you typed code before? (never / a little / yes)". This only
suggests a preset and is never scored.

- **1A-01 `press-run` · Press Run** · intro `call:print` `const:str` · **P→R** · *starter passes*
  - Task: Mar'tu's line `print("Hi. It is me, Mar'tu.")` is already written. Predict what the console will show
    (the words / the words with quotes / an error), then press Run.
  - CP1: run it (prints the line).
  - Catches: no model of running code (G1).
  - Hooks: AW[in Tor: "`print` is my chalk. What is inside the quotes goes on the wall."; shorter]. A win in
    under a minute.
- **1A-02 `your-own-words` · Your own words** · intro — · **M**
  - Example: `print("Shield up.")` (Bomb Shell).
  - Task: print one line Oogrish might say to calm the party. Any words, in quotes.
  - CP1: prints a line different from the example's [TEXT, OUT].
  - Catches: copying the example line (G2: "skip to the example and copy it").
  - Hooks: DF ("Steady, now."); Mar'tu echoes the student's line deadpan; BQ: print a second line from Lucky.
- **1A-03 `close-the-quote` · Close the quote** · intro — · **D**
  - Task: run `print("It is not a compass)`, read the explainer, and fix it.
  - CP1: runs and prints `It is not a compass` (with or without a final period).
  - Catches: A-02 `("Fire Ball`, A-03 `"Fierball.`, A-04 `"Fireball` (unclosed quotes).
  - Hooks: AW[analogy: "quotes are bookends: one opens, one closes"; picture of a bookend pair].
- **1A-04 `words-need-quotes` · Words need quotes** · intro — · **D→I**
  - Task: run `print(Fireball)` and read the NameError ("Python looked for a box called Fireball"). Fix it with
    quotes; single quotes are fine too.
  - Investigate: "Why does Python say *name* is not defined?" This foreshadows variables.
  - CP1: prints `Fireball`.
  - Catches: A-05 `fireball`, A-08 `kratos`, B-01's unquoted joke name.
  - Hooks: AW[step-by-step: what Python tries first]. WT: "Names versus words".
- **1A-05 `top-to-bottom` · Top to bottom** · intro — · **P→R→M**
  - Task: predict the order of three printed lines of a Ley Clock report. Then move the warning line so it
    prints last, and add `print()` for a blank line before it.
  - CP1: the warning prints last [OUT]. CP2: a blank line comes before it.
  - Hooks: TR (step through three lines); PR: the navigator predicts the order.
- **1A-06 `notes-for-humans` · Notes for humans** · intro — (comments aren't tokens) · **I→M**
  - Task: put `#` in front of the line Lucky shouldn't say out loud. Then add a note of your own above the
    code.
  - CP1: that line no longer prints. CP2: the source has a new `#` line.
  - Hooks: AW[shorter].
- **1A-07 `many-lines-at-once` · Many lines at once** · intro `const:multiline_str` · **P→R→M**
  - Example: a 2-line `"""` note about the glug canteen.
  - Task: print a 3-line chalk note with one `print("""...""")`. Any words.
  - CP1: at least 3 lines printed from a single `print` call [OUT + `_count('call:print') == 1`].
  - Prepares the Ward Sign project.
  - Hooks: BQ: draw a tiny box out of `|` and `-`.
- **1A-08 `broken-spell-1A` · Broken spell: three slips** · intro — · **D** · **SOLO**
  - Task: fix three lines: `Print("Barrier's holding.")` (capital P), `print("Shield up.)` (unclosed quote),
    and `print(Steady)` (unquoted text).
  - CP1–3: each line prints, one checkpoint per line, so each fix gets its own green tick.
  - Catches: A-08 `heath` and A-05 `Powrup` (case is exact), plus the quote slips above.
  - Hooks: Mar'tu's wise-feedback line on the first fizzle.

### Lesson 1B "Boxes With Labels" [C]

*Mar'tu remembers…*
1. "Which line prints the word glug: `print(glug)` or `print("glug")`?" (1A)
2. "What does Python do with a line that starts with `#`?" (1A)

- **1B-01 `label-a-box` · A box with a label** · intro `node:Assign` · **P→R→I**
  - Example (it is also the code): `companion = "Gearshift"`, `print(companion)`, `print("companion")`.
  - Task: predict both lines, then run. Investigate: which line has quotes, and what did each print?
  - CP1: change the value to another hero and run [TEXT, and `companion` ≠ `"Gearshift"`].
  - Catches: A-02 name in quotes; B-02, B-03 value-without-name.
  - Hooks: AW[analogy: a box with a label: the label is the name, what's inside is the value; picture: the
    labeled box drawn; in Tor: "a jar on my shelf with a chalk label"]. TR.
- **1B-02 `name-and-value` · Name AND value** · intro — · **M**
  - Task: make a variable named `character` that holds your hero, in quotes, then print it using the variable.
  - CP1: `character` exists and holds text [NAME (example name `companion` and `player_name` detected), TEXT].
  - CP2: printed through the variable, not retyped (an AST check that `print`'s argument is `Name('character')`).
  - Catches:
    - B-02 `"Spiderman"` and B-03 `"Superman"` (value with no name): "I don't see a box named `character`.
      Write `character =` before your hero."
    - A-02 `def ("character")` [DEF].
    - A-04 `character - "Zelda"` [explainer, `-` vs `=`].
    - A-05, A-06, A-07 `player_name` [NAME].
    - A-08 `character = kratos` [TEXT explainer].
  - Hooks: DF ("a very tired adventurer"); any quoted value passes (Kratos, Spiderman, jokes); Mar'tu reacts:
    "*Kratos.* Hm. Welcome to the cabin."; PA (2 blocks plus distractors `def ("character")` and
    `"character" = "Zelda"`); AW[box; shorter: "name, then `=`, then the value"].
- **1B-03 `numbers-stand-alone` · Numbers stand alone** · intro `const:int` · **P→I→M**
  - Example: `max_mana = 26`, then `print(max_mana)` versus `print("max_mana")`.
  - Task: make `armor_bonus` holding Lucky's armor bonus (3, a number), and `weapon` holding any weapon name
    (text).
  - CP1: `armor_bonus` is the int 3 [NUM]. CP2: `weapon` is text [TEXT].
  - Catches: quoting numbers. Writing the value without a name (B-01).
  - Hooks: AW[picture: number box versus text box]. WT: "Why `"3"` isn't 3".
- **1B-04 `exact-names` · Exact names** · intro — · **D**
  - Task: the starter has `Max_Mana = 18` followed by `print(max_mana)` (NameError), and
    `magical affinity = 9` (SyntaxError: a space in the name). Fix both.
  - CP1: `max_mana` prints 18. CP2: `magical_affinity` holds 9 [NAME].
  - Catches: A-08 `heath`, A-05 `Powrup`, B-01 `power_UP`, B-02/B-03 `Pizza` vs `pizzas`, A-06 `pizza party`
    (spaces).
  - Hooks: AW[step-by-step: Python compares names letter by letter, like a key in a lock].
- **1B-05 `change-the-box` · A box can change** · intro — · **P→R→I**
  - Task: `mana = 26`, then `mana = 21`, then `print(mana)`. Predict 26, 21, or both. Then step through it.
  - CP1: add a third value and print it [OUT].
  - Catches: "both values stay" and "print shows everything computed earlier" (A-03, A-04 printed sums).
  - Hooks: **TR default-open** (the ledger shows the value being replaced); AW[picture].
- **1B-06 `broken-spell-1B` · Broken spell** · intro — · **D** · **SOLO**
  - Task: fix `"weapon" = "Telegun"` (name in quotes; Python's message misleads, so the explainer catches it),
    `"Lucky"` alone on a line where `hero` should be made, `glug_sips - 3` used where `=` was meant, and an
    unclosed quote.
  - CP1–4: one per line [NAME, TEXT, NUM].
  - Catches: A-02, A-04, B-02, B-03 (the exact slips listed above).

### Lesson 1C "Math and Glue" [C]

*Mar'tu remembers…*
1. "Which line makes a box: `"hero" = "Lucky"` or `hero = "Lucky"`?" (1B)
2. "Fix: `print("Shield up.)`" (1A)

- **1C-01 `chalk-math` · Mar'tu's chalk math** · intro `op:Add` `op:Sub` `op:Mult` `op:Div` · **P→R→I→M**
  - Predict `48 - 37`, `9 * 2`, `48 / 2` (it prints `24.0`; investigate why).
  - Task: with `first_gap = 48` and `last_gap = 37`, print how much the gap shrank.
  - CP1: prints 11 [OUT]. CP2: computed from the two variables [CMB: rerun with `last_gap = 41` gives 7].
  - Catches: typing 11 by hand (everyone's 68).
  - Hooks: AW[shorter]. Arithmetic is the class's strength, so this is a confidence bridge (personas,
    class-wide pattern 10).
- **1C-02 `what-each-number-means` · What does each number mean?** · intro — · **I→M**
  - Task: "Mar'tu needs 3 lanterns that cost 4 coins each, and 5 coils of rope that cost 2 coins each."
  - The starter has four labeled boxes set to 0, with comments `# how many?` and `# how much is one?`. Fill
    them in.
  - CP1: `lantern_count == 3` and `lantern_price == 4` (if they are swapped: "You swapped them: 3 is how many
    lanterns, 4 is the price of one."). CP2: the rope values.
  - Catches: A-05, A-07, A-08 `pizzas = 12` / `pizzas * 48` (prices in count boxes). A-02 5s and A-03, A-04
    180/1000 (numbers unlinked to the problem).
  - Hooks: AW[in Tor: "How many jars? How much for one jar?"; picture of a price tag versus a tally].
- **1C-03 `let-the-code-combine` · Let the code combine it** · intro — · **M→Mk**
  - Example: "Oogrish buys 2 maps at 6 coins." `map_count = 2`, `map_price = 6`,
    `map_cost = map_count * map_price`. Different names and values from the task.
  - Task: continue 1C-02 by making `lantern_cost`, `rope_cost` and `total_cost`, then print `total_cost`.
  - CP1: `lantern_cost` is built from the variables [CMB]. CP2: `rope_cost` the same [CMB]. CP3: `total_cost`
    is 22 and built from the two costs [CMB: rerun with `lantern_count = 7` gives 38].
  - Catches: `total_cost = 22` (everyone's 68), `total_cost = 12 + 10` (literals), `lantern_count * 4` (the
    price typed in; a rerun with a new price catches it).
  - **Hint ladder (CP3):**
    1. Point: "Look at `total_cost = 0`. Which two costs make the total?"
    2. Teach: "Python can add boxes. If `a = 2` and `b = 5`, then `c = a + b` puts 7 in `c`, and it stays right
       when `a` changes."
    3. Show: "`total_cost = lantern_cost + rope_cost`".
    - Your-turn variant: "2 maps at 6 coins and 3 candles at 1 coin: write `map_cost`, `candle_cost` and
      `supply_total`."
  - Hooks: PA (distractor `total_cost = 22`); TR; AW[recipe: "write the recipe, not the answer"; from the
    campaign: `caster["max_mana"] - caster["mana"]`]; PR: "Explain to your partner why 22 typed in is a trap."
- **1C-04 `spend-mana` · Spend some mana** · intro — · **P→R→M**
  - Task: Lucky has `mana = 26`, and Warm Hands has `spell_cost = 3`. Predict `mana` after
    `mana = mana - spell_cost` runs twice. Then make it three casts.
  - CP1: `mana == 17` [CMB: rerun with `spell_cost = 5` gives 11].
  - Catches: A-03, A-04 tracing by adding the visible constants; the belief that `=` means "equals forever".
  - Hooks: **TR default-open**; AW[step-by-step trace table]; campaign link
    `caster["mana"] = caster["mana"] - spell["mana_cost"]`.
- **1C-05 `the-short-way` · The short way** · intro `node:AugAssign` · **P→M**
  - Task: predict `hours_waited += 6` and `mana -= 3`. Rewrite two long reassignments in the short form.
  - CP1: values are right. CP2: the code uses `+=` or `-=` (`_uses('node:AugAssign')`).
  - Hooks: AW[shorter]. Loops reuse this for running totals.
- **1C-06 `glue-words` · Glue words together** · intro `call:str` · **P→R→I→M**
  - Investigate: `"Mana: " + 26` raises a TypeError (read the explainer); `"Lucky" + "is"` is missing a space.
  - Task: from `name` and `mana`, print `Lucky has 26 mana.`
  - CP1: the line is exact for the given values [OUT]. CP2: built from the variables [CMB: rerun with
    `name = "Tester"` and `mana = 4`].
  - Catches: `print("Lucky has 26 mana.")` typed in; `"mana"` in quotes, which prints the word "mana".
  - Hooks: AW[analogy: glue and labels]; campaign link: the mana-bar return line.
- **1C-07 `status-line` · A status line** · intro — · **Mk**
  - Task: make `hero_name`, `magical_affinity` (Oogrish: 9), `max_mana = magical_affinity * 2` (the real rule:
    max mana is twice the affinity), and `mana = max_mana`. Print `Oogrish: 18/18 mana`.
  - CP1: `max_mana` is computed [CMB: affinity 13 gives 26]. CP2: the status line is exact [OUT].
  - Hooks: DF (Oogrish); BQ: do Lucky's line too with the real table value (13 → 26).
- **1C-08 `repeat-a-mark` · Repeat a mark** · intro — (`op:Mult` on text) · **P→R→I→M→Mk**
  - This is the PRIMM template described in §2.1.
  - Task: with `mana = 3` and `max_mana = 5`, make
    `bar = "█" * mana + "░" * (max_mana - mana)` and print `"[" + bar + "]"`.
  - CP1: Gearshift's full bar, 20 blocks. CP2: `[███░░]` [OUT]. CP3: correct when empty and when full [CMB:
    reruns with mana 0 and 5].
  - Catches: `"░" * max_mana - mana` (a TypeError; the explainer covers precedence).
  - Hooks: PA (distractor without parentheses); AW[picture of a fuel gauge; from the campaign:
    `get_mana_bar`]; WT: "Why parentheses?"; BQ: add ` 3/5` with `str()`.
- **1C-09 `broken-spell-1C` · Broken spell** · intro — · **D** · **SOLO**
  - Task: four bugs: `"Mana: " + mana` (TypeError), a total typed by hand (the output looks right, but the
    rerun check fails, which shows students that checks change inputs), a swapped count and price, and a bar
    missing its parentheses.
  - CP1–4: one per bug.

### Article 1-A2 "Clock Math" [O, 12 min]

Covers `**`, `%` and `//`, with order of operations.
- Ley Clock example: "The hand moves one mark an hour around 12 marks. 50 hours from mark 9, where is it?"
  `(9 + 50) % 12` → 11.
- Also: `2 + 3 * 4` → 14 versus `(2 + 3) * 4` → 20, `2 ** 3` → 8, `50 // 12` → 4.
- intro `op:Pow` `op:Mod` `op:FloorDiv`.
- **Try-it 1-A2a `where-is-the-hand`**: write `hand = (start + hours) % 12` for two given starts [CMB].
- Prerequisite card for the optional Cipher project (8P2).

### Quiz 1 "Chalk Quiz" [C, 10 questions]

**Types:** 3 mc · 4 predict · 1 fill · 2 bug.

**Samples** (keys executed):
1. **mc.** "Which line makes a box named `hero` that holds the text Lucky?"
   - Choices: `def ("hero")` / `"hero" = "Lucky"` / `hero = "Lucky"` / `hero - "Lucky"`. **Answer:** 3rd.
   - Why each wrong choice is wrong:
     - `def` makes a recipe, not a box (A-02).
     - The name never goes in quotes.
     - `-` subtracts. Use `=` (A-04).
2. **predict.** `mana = 18` / `mana = mana - 5` / `mana = mana - 5` / `print(mana)` → `8`.
   - Why `13` or `18 5 5` are wrong: the box keeps only its latest value.
3. **bug.** `print("It is not a compass)` → add the closing quote.

**Other questions:**
- predict `print("█" * 2 + "░" * 3)` → `██░░░`
- fill `print("Mana: " + ___(7))` → `str`
- predict `lantern_count * lantern_price + 2` → 14
- mc "Mar'tu changes `lantern_count` to 5. Which `total` line stays right?" (only the one built from the
  variables)
- bug: a quoted number in a sum
- mc: names are exact (`Health` vs `health`)
- predict a two-line print order

### Project 1P1 "The Night Watch Ledger" [C, 40 min]

**Premise.** The barrier must hold until the next burst, 37 hours away. Mar'tu keeps a ledger of what the night
will cost: mana for the barrier, flasks of lantern oil, and the sips of glug Lucky insists are "medical".

**Tasks:**
- **A. What we know**
  1. Make `hours_until_burst = 37`.
  2. Make `mana_per_hour` (2), `oil_per_hour` (1), `oil_price` (3 coins a flask), and `glug_sips` (any
     number).
- **B. Let the code combine it**
  3. `mana_needed` from hours and mana per hour.
  4. `oil_needed` and `oil_cost`.
  5. `total_coins` = oil cost plus Lucky's glug fee (`glug_sips * glug_price`, with `glug_price` your choice).
- **C. Write the ledger**
  6. Print a title and a divider made with `"~" * 24`.
  7. Print one ledger line per value, built with `+` and `str()`.
  8. Print who keeps first watch (any hero, in quotes).

**Checks:** each value is right. [CMB] Rerunning with `hours_until_burst = 32` updates every line. The divider
uses repetition, not 24 typed characters. Any watch-keeper name passes.

**Stretch:**
- A "reserve" mana bar for the barrier (1C-08).
- Lucky's line: "What's in it for me?", priced.

**Consolidates:** 1B–1C (variables, combine, concatenation, repetition).

**Not a store receipt:** it's a night's resource ledger set in the cabin.

### Project 1P2 "The Ward Sign" [O, 25 min]

**Premise.** Mar'tu wants a ward sign painted on the barrier post, in big block letters. The word is your choice;
the default is `TOR`.

**Tasks:**
1. Draw each letter five rows tall with `print` and `"█" * n`.
2. Draw a border made with repetition.
3. Store the ink in a variable (`ink = "█"`) so one change repaints the whole sign.
4. Use a triple-quoted string for one letter.

**Checks:** at least 5 printed rows; the ink variable is used (rerun with `ink = "#"` changes the output).

**Stretch:** sign the post with your hero's spell color.

**Consolidates:** 1A, 1C-08.

### Article 1-A3 "Asking the Traveler: `input()`" [O, 15 min]

`input()` always returns text, so convert with `int()` for math.
- intro `call:input` `call:int`.
- The interactive replay shim lets students answer in the console.
- **Try-it 1-A3a `who-goes-there`**: ask the traveler's name and greet them. Then ask for sips of glug and
  double the number.
  - `stdin=["Lucky", "3"]`.
  - Checks: `_inputs_used() == 2`; the greeting uses the answer [CMB via stdin].
- Campaign link: `user.clicked()` also hands back text, which is compared with `==`.

### Quick Check 1 (test-out) [10 min]

1. predict `"Mana [" + "█" * 3 + "░" * 2 + "] " + str(3) + "/" + str(5)` → `Mana [███░░] 3/5` (campaign idiom).
2. Make `character` holding any text and print it [NAME, TEXT].
3. Given counts and prices, make `total_cost` [CMB].
4. Build `"<name>: <mana>/<max_mana> mana"` from variables, with `max_mana` computed from affinity [CMB].
5. Fix `print("Shield up.)` and `mana = mana - "3"`.

**Skills:** `quote-text`, `make-variable`, `exact-names`, `combine-values`, `concat-str`, `repeat-string`.

### Cheatsheet 1 "Mar'tu's Chalk Notes: First Words"

`print("text")` · quotes come in pairs · `# comment` · `"""many lines"""` · `name = value` (name never in
quotes) · numbers without quotes · reassign `mana = mana - cost` · `+=` / `-=` · `+ - * /` (`/` gives a decimal)
· how many × how much each · `"Mana: " + str(7)` · `"█" * 3 + "░" * 2` → `███░░` · `"░" * (a - b)` needs
parentheses · error quick-reference (unclosed quote / NameError / TypeError).

---

## Unit 2 · Control Flow: "The Ley Clock Decides"

**Mar'tu's framing.** "The Ley Clock does not panic. It checks. If the hand is near the arc, it warns.
Otherwise, it waits. Today you teach Python to check, the same way. And you learn to roll dice, because the
world is not fair, yes?"

**RPG tie-in.** These are skill checks: a d20 roll against a required roll. Other examples: the clock's color
by hours left, Lucky's Dumb Luck reroll, and a four-answer dialogue chain.

**Learning objectives. Student can…**
1. Evaluate comparisons (`== != < > <= >=`) to `True` / `False`, and store a comparison in a variable.
2. Tell `=` (put in a box) from `==` (ask "same?").
3. Predict boundary results (`roll >= needed` when they are equal), and choose `<` versus `<=` on purpose.
4. Compare text case-safely with `.lower()`. Text comparison is exact, including quotes and case.
5. Write `if`, `if/else`, and `if/elif/else` with colons and indentation, and know the first true branch wins.
6. Combine conditions with `and`, `or` and `not`.
7. Use `import random` and `random.randint(a, b)`, knowing both ends are included.
8. Read a traceback (line, type, message) and fix a SyntaxError, IndentationError, NameError, or TypeError.
   Debug a wrong answer by printing values.

**Campaign links.**
- Obj 1–3 → `skill-checks` (`return roll >= required_roll`) and `hold-the-barrier` (`<` not `<=`).
- Obj 4–5 → `program-dialogue-options` (four-branch `elif` on `user.clicked() == "option 1"`) and the
  `program-dialogue-prompt` methods.
- Obj 6 → reading the affinity-and-mana logic in `hold-the-barrier`.
- Obj 7 → `perform_roll(die_size)`.
- Obj 8 → every part.

**Items in order:**
| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 2A "True or False, Yes?" | C | 18 |
| 2 | Lesson 2B "If the Clock Turns Red" | C | 40 |
| 3 | Article 2-A1 "Match: Another Way to Choose" | O | 12 |
| 4 | Quiz 2 | C | 10 |
| 5 | Project 2P1 "Road Encounter Table" | C | 40 |
| 6 | Project 2P2 "Three Roads to the Institute" | O | 35 |
| 7 | Lesson 2C "When Spells Fizzle: Reading Errors" | C | 30 |
| 8 | Quick Check 2 | O | 10 |
| 9 | Cheatsheet 2 | ref | — |

### Lesson 2A "True or False, Yes?" [C]

*Mar'tu remembers…*
1. Predict `"█" * 2 + "░" * 3`. (1C)
2. In `rope_count * rope_price`, which one is "how many"? (1C)

- **2A-01 `true-or-false` · True or False** · intro `const:bool` `op:Gt` `op:Lt` · **P→R**
  - Task: predict `print(18 > 12)` and `print(6 > 15)`. Bomb Shell's DEX is 6 and the latch needs 15.
  - Store `barrier_up = True` and print it.
  - CP1: print whether `dex` is less than `needed` [OUT, CMB].
  - Hooks: AW[analogy: "a yes/no question Python answers"]; WT: `True` has no quotes.
- **2A-02 `ask-with-double-equals` · Asking with `==`** · intro `op:Eq` `op:NotEq` · **P→I→M**
  - Task: make `clock_is_red = clock_color == "red"`, then print `clock_color != "red"`.
  - CP1: `clock_is_red` is a bool built from a comparison [CMB: rerun with `"red"`]. CP2: the `!=` line prints.
  - Catches: `=` versus `==`; `"Red" == "red"` is False.
  - Hooks: AW[shorter: "`=` puts; `==` asks"; picture]; PA.
- **2A-03 `enough-to-pass` · Enough to pass** · intro `op:GtE` `op:LtE` · **P→I→M**
  - Task: predict `roll >= needed` for rolls 14, 15 and 16 against `needed = 15`. Then make
    `passed = roll >= needed`.
  - CP1: `passed` follows the roll [BND via rerun]. CP2: `can_cast = mana >= cost`, where exactly enough mana
    still casts [BND].
  - Hooks: AW[in Tor: "a 15 opens a latch that needs 15"; from the campaign: "Use `<` and not `<=`, because a
    caster with exactly enough mana can still cast."]; TR.
- **2A-04 `any-case-answer` · Any case, same answer** · intro `attr:lower` · **P→I→M** (deviation D3)
  - Task: `"YES" == "yes"` is False. Lucky shouts his answers. Make `said_yes = answer.lower() == "yes"`.
  - CP1: True for `"YES"`, `"yes"` and `"YeS"`, and False for `"no"` [CMB, 4 reruns].
  - Catches: `answer.lower == "yes"` (missing `()`).
  - Hooks: AW[shorter]; campaign link `.lower().capitalize()`.
- **2A-05 `broken-spell-2A` · Broken spell** · intro — · **D** · **SOLO**
  - Task: fix `passed = roll => needed` (SyntaxError), `needed = "15"` (TypeError int vs str), and
    `clock_is_red = "red"` (assigns instead of asking).
  - CP1–3.

### Lesson 2B "If the Clock Turns Red" [C]

*Mar'tu remembers…*
1. "`=` or `==`: which one asks?" (2A)
2. Predict `"Mana: " + str(4 + 3)`. (1C)

- **2B-01 `first-if` · If** · intro `node:If` · **P→R→I**
  - Code: `if hours_left < 3:` followed by an indented `print("Get inside!")`.
  - Investigate: change `hours_left` to 10. Nothing prints. Why?
  - CP1: the warning prints only when hours are low [CMB, 2 reruns].
  - Hooks: TR; AW[picture of a fork in the road; analogy: "the barrier door opens only if…"].
- **2B-02 `colon-and-indent` · Colon and indent** · intro — · **D**
  - Task: fix a missing colon (SyntaxError), a body with no indent (IndentationError), and an un-indented line
    that always runs.
  - CP1–3 [CMB].
  - Hooks: AW[step-by-step: the colon says "here comes the block"; indentation says "this belongs to it"].
- **2B-03 `otherwise` · Otherwise** · intro — (`else` has no token) · **M**
  - Example: Oogrish's perception check (`spot_roll`, `spot_needed`).
  - Task: Bomb Shell pries the latch. Write an if/else on `strength_roll >= strength_needed` that prints
    "The latch pops open." or "That latch hates me."
  - CP1: the success line prints at and above `needed`, the failure line below it [BND via 3 reruns]. Any text
    is accepted as long as the two lines differ.
  - Catches: copying the example's names [NAME].
  - Hooks: PA; DF.
- **2B-04 `clock-colors` · Clock colors** · intro — (`elif`) · **P→I→M**
  - Code: `hours_left <= 2` gives `"red"`, `<= 12` gives `"bright blue"`, otherwise `"calm blue"`.
  - Investigate: swap the first two branches. Which hours now get the wrong color? The first true branch wins.
  - CP1: the color is right for 1, 2, 3, 12, 13 and 40 [BND, CMB].
  - Hooks: TR; AW[analogy: "a line of doors; you take the first one that opens"].
- **2B-05 `four-answers` · Four answers** · intro — · **A→M**
  - This is the near-transfer for `program-dialogue-options`.
  - Task:
    1. Assemble a four-branch chain on `choice == "option 1"` through `"option 4"`. Each branch calls
       `mar_tu_says(...)`, a setup helper.
    2. Add `light_up_box()` under each `mar_tu_says` line.
  - CP1: each choice says its own line [CALL, 4 reruns]. CP2: the box lights once per choice [CALL].
  - Catches: `elif choice == option 2:` (missing quotes; Parsons distractor and NameError explainer);
    `elif choice = "option 3":`; the helper added under only one branch.
  - Hooks: PA (distractors as listed; adaptive); BQ: a fifth "option 5" Lucky line.
- **2B-06 `and-or-not` · And, or, not** · intro `op:And` `op:Or` `op:Not` · **P→I→M**
  - Task:
    - `can_cast = mana >= cost and affinity >= required`. Oogrish has affinity 9, and Lantern Ward needs 9.
    - `lucky_passes = first_roll >= needed or second_roll >= needed` (Dumb Luck).
    - `not barrier_up`.
  - CP1–3: each value is right across reruns [CMB].
  - Hooks: AW[step-by-step truth table using the real stats]; WT: "and needs both; or needs one".
- **2B-07 `roll-a-die` · Roll a die** · intro `node:Import` `import:random` `attr:randint` · **P→R→I**
  - Predict: can `random.randint(1, 6)` give 6? 0? Run it several times.
  - Task: roll the Staff of Wisdom (d6) and the longsword (d8).
  - CP1: `randint` was called with `(1, 6)` and `(1, 8)` [RND].
  - Catches: `randint(0, 6)`; `randint(1, 5)` (believing the top is excluded).
  - Hooks: AW[picture: the die's faces; contrast "`range` stops before the end; `randint` includes both ends"
    (revisited in 3B)].
- **2B-08 `roll-and-decide` · Roll and decide** · intro — · **Mk**
  - Task: pick an action (any text) and a needed roll from 2 to 20 (default: "pry the trap door open", 12).
    Roll a d20, and print success or failure, including the roll via `str()`.
  - CP1: d20 rolled [RND]. CP2: the right branch for scripted rolls `needed-1`, `needed` and `needed+1` [BND +
    RND]. CP3: the printed line includes the roll [OUT].
  - Hooks: DF; PA; BQ "Dumb Luck": if the first roll fails, roll once more.
- **2B-09 `broken-spell-2B` · Broken spell** · intro — · **D** · **SOLO**
  - Task: fix `if roll = 20:`, `random.randint(1, 20)` with no `import random` (NameError), an `elif` written
    after `else`, an unquoted `option 1`, and a `<=` that should be `<` (no error, wrong behavior, so the check
    uses rerun output).
  - CP1–5.

### Article 2-A1 "Match: Another Way to Choose" [O, 12 min]

Rewrite the four-answers chain with `match choice:` / `case "option 1":` / `case _:`.
- intro `node:Match`.
- Try-it: the five-option version [CALL].
- Note: the campaign uses `elif`, so read both.

### Quiz 2 [C, 10 questions]

**Types:** 2 mc · 5 predict · 1 parsons · 2 bug.

**Samples:**
1. **predict.** `roll = 12` / `needed = 12` / `print(roll >= needed)` / `print(roll > needed)` → `True` then
   `False`.
2. **predict.** The 3-branch clock chain with `hours_left = 2` → `red`.
3. **mc.** "Which values can `random.randint(1, 6)` give?" Choices: 0–5 / 1–5 / 1–6 / 0–6. **Answer:** 1–6.

**Other questions:**
- predict `mana >= cost and affinity >= required` with affinity 8 and required 9 → `False`
- parsons: a four-option chain with indentation (distractor `elif choice == option 2:`)
- bug: `if roll = 20:`
- bug: a missing `import random`
- mc: `=` versus `==`
- predict: `not` on a variable
- predict: the order-matters chain

### Project 2P1 "Road Encounter Table" [C, 40 min]

**Premise.** The road to the old Institute is long. Oogrish insists on an encounter table: roll a d20 and see what
the road throws at you. You write the encounters.

**Tasks:**
- **A. Roll**
  1. `import random`.
  2. Roll `road_roll` with a d20.
- **B. Table**
  3. Use `if/elif/else` with these tiers:
     - 1: Lucky fires the Telegun (hedge).
     - 2–6: a ley-line hums under the road.
     - 7–15: a quiet road.
     - 16–19: a brass-cart peddler.
     - 20: a starlode vein for Gearshift.
  4. Store the result in `encounter`. Any text per tier.
- **C. Tell it**
  5. Print `"Rolled " + str(road_roll) + ": " + encounter`.
- **D. React**
  6. Roll a perception check against a needed roll you choose. Print whether the party spots the encounter
     early, using `and` with a second condition (e.g., `not night_time`).

**Checks:**
- [RND + BND] Scripted rolls 1, 2, 6, 7, 15, 16, 19 and 20.
- Same-tier rolls give the same `encounter`. Neighboring tiers give different ones.
- The printed line includes the roll.

**Stretch:**
- Dumb Luck (Lucky may reroll a 1 once).
- A sixth tier.

**Consolidates:** 2A–2B and `randint`.

### Project 2P2 "Three Roads to the Institute" [O, 35 min]

**Premise.** Three ways to travel:
- **Gearshift's jeep form:** burns starlode at 2 units a mile, plus 5 to start.
- **On foot:** free, but costs glug rations by distance tier.
- **Lucky's Telegun:** free, but a roll under 15 lands you in a hedge.

**Tasks:**
1. Ration cost with `elif` tiers.
2. The jeep's cost formula.
3. Pick the cheapest with comparisons and `and`.
4. Print the choice and its cost.

**Checks:** [CMB] reruns at distances 5, 30 and 80 pick the right road.

**Consolidates:** tiers and comparisons. Not a shipping premise.

### Lesson 2C "When Spells Fizzle: Reading Errors" [C]

This is the syllabus's Errors lesson, kept at the end of the unit.

*Mar'tu remembers…*
1. "Can `random.randint(1, 6)` give 6?" (2B)
2. A two-branch trace. (2B)

- **2C-01 `anatomy-of-a-fizzle` · Anatomy of a fizzle** · intro — · **I**
  - Task: run a 5-line program that fails on line 4. Record what the traceback says in three variables:
    `bad_line = 4`, `error_type = "NameError"`, `missing_name = "mana_cost"`.
  - CP1–3: each answer is right [NUM, TEXT]. This practices variables, too.
  - Hooks: AW[picture: an annotated traceback, with "read the last line first"].
- **2C-02 `syntax-fizzles` · Syntax fizzles** · intro — · **D→I**
  - Task: fix three SyntaxErrors: a missing `)`, a missing `:`, and an unclosed quote.
  - Investigate: why does Python report only one at a time?
  - CP1–3.
- **2C-03 `name-fizzles` · Name fizzles** · intro — · **D**
  - Task: fix a typo (`mama`), a variable used before it is made, unquoted text, and a case slip. Read Python
    3.13's "Did you mean…?" suggestion.
  - CP1–4 [NAME].
- **2C-04 `type-fizzles` · Type fizzles** · intro — · **D**
  - Task: fix text plus a number, and a number compared with quoted text.
  - CP1–2.
- **2C-05 `no-error-wrong-answer` · No error, wrong answer** · intro — · **D/I**
  - Task: a caster with exactly enough mana doesn't cast. Add `print(mana)` and `print(cost)` above the `if` to
    see the values, then fix the comparison.
  - CP1: exactly enough now casts [BND].
  - Hooks: WT: "print-debugging is a real technique".
- **2C-06 `equals-is-not-def` · `=` is not `def`** · intro — · **D**
  - Task: the starter `def hero = "Lucky"` gives a SyntaxError. Mar'tu: "`def` is for making recipes. We learn
    those later. A box needs only `=`." Fix it.
  - CP1: `hero` holds text [NAME, TEXT].
  - Catches: A-02 `def ("character")`. It also inoculates against the campaign's `def`-heavy starters
    reactivating that belief (personas G1 risk).
  - The starter is deliberately unparseable; the harness allows that with a warning.
- **2C-07 `debug-routine` · The four-step routine** · intro — · **D** · **SOLO**
  - The routine:
    1. Read the last line.
    2. Go to that line.
    3. Check the line above.
    4. Print the values.
  - Task: apply it to a 12-line encounter script with three different bugs.
  - CP1–3.
  - Hooks: Oogrish's line "Steady, now. Read the last line of the error first."

### Quick Check 2 (test-out)

1. Predict booleans at the boundary (rolls 11, 12 and 13 against 12).
2. Trace a three-branch `elif` for three values.
3. mc: the values `randint(1, 8)` can give.
4. **Code:** roll a d20 against a needed roll with if/else [RND, BND].
5. **Bug:** `if choice = "option 1":` plus an unquoted `option 2`.

**Skills:** `compare`, `boundary`, `if-else`, `elif-chain`, `randint`, `read-traceback`.

### Cheatsheet 2

`True`/`False` · `==` asks, `=` puts · `< <= > >= !=` · exactly enough: `>=` · `if x:` + indent ·
`else:` · `elif:` (first true wins) · `and`/`or`/`not` · `text.lower() == "yes"` ·
`import random` · `random.randint(1, 20)` includes 1 and 20 · read the last line of a traceback first.

---

## Unit 3 · Lists: "The Chalk Wall"

**Mar'tu's framing.** "Seven numbers on my wall. I could give each one its own box. I could also lose my mind.
A list keeps them together, in order, yes?"

**RPG tie-in.** The chalk wall `[48, 48, 47, 46, 44, 41, 37]` is the unit's data. The gaps between bursts are
shrinking, and students find that out themselves in Unit 5. Other lists: the hero roster as name-and-mana
pairs, and Oogrish's training log.

**Learning objectives. Student can…**
1. Create a list with `[ ]` and commas.
2. Read an item by zero-based index, including negative indexes. Recognize an `IndexError`.
3. Change an item by index.
4. Grow a list with `.append()`, and join two lists with `+`.
5. Use `len()`, and know that the last index is `len - 1`.
6. Read a nested list `roster[3][1]`.
7. Make `range(...)` and know the stop value is excluded.
8. Slice with `[a:b]` and `[-3:]`.
9. Use `sorted()` versus `.sort()` (which returns `None`), and `.count()`.

Optional: `.insert`, `.pop`, `.remove`, `in`, `max`/`min`/`sum`, tuples, `zip()`.

**Campaign links.**
- Obj 1–2, 6 → `party.members` is a list. A nested read is the stepping stone to
  `caster["abilities"]["magical_affinity"]`.
- Obj 9 → `.sort()` returning `None` prepares the missing-`return` lessons in Unit 6.

**Items in order:**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 3A "Many Values, One Name" | C | 35 |
| 2 | Quiz 3A | C | 8 |
| 3 | Project 3P1 "Oogrish's Training Log" | C | 25 |
| 4 | Lesson 3B "Reading the Wall Closely" | C | 18 |
| 5 | Lesson 3C "More List Tools" | O | 15 |
| 6 | Quiz 3B | O | 8 |
| 7 | Article 3-A1 Tuples | O | 10 |
| 8 | Article 3-A2 `zip()` | O | 10 |
| 9 | Project 3P2 "The Basement Inventory" | O | 35 |
| 10 | Quick Check 3 | O | — |
| 11 | Cheatsheet 3 | ref | — |

### Lesson 3A "Many Values, One Name" [C]

*Mar'tu remembers…*
1. Trace: `mana = 18` / `mana = mana - 5`. (1C)
2. `roll >= needed` at the boundary. (2A)

- **3A-01 `how-would-you-store-it` · How would you store it?** · intro — · **PF** · *starter passes*
  - Task: "Store the seven hours from my wall so you can ask about them later." Students try anything for up
    to 3 minutes (most write `hour_1 = 48`, …). Mar'tu then compares their attempt with a list.
  - CP1: run any attempt.
  - Hooks: never offered when the student shows frustration signals (research P12).
- **3A-02 `make-the-wall` · Make the wall** · intro `node:List` · **M**
  - Example: `party_colors = ["gold", "fire orange"]`.
  - Task: make `chalk_wall` holding the seven hours in order, then print it.
  - CP1: `chalk_wall == [48, 48, 47, 46, 44, 41, 37]` [NAME].
  - Catches: missing commas (SyntaxError), quoted numbers [NUM].
  - Hooks: AW[analogy: a shelf of jars; picture].
- **3A-03 `first-is-zero` · The first is zero** · intro `node:Subscript` · **P→R→I**
  - Predict `chalk_wall[1]` and `chalk_wall[6]`. Then run `chalk_wall[7]` and read the IndexError.
  - Task: print the oldest hour.
  - CP1: prints 48. CP2: read from the list [`_uses('node:Subscript')`, CMB with a changed wall].
  - Hooks: TR; AW[picture: numbered jars from 0].
- **3A-04 `count-from-the-end` · Count from the end** · intro `op:USub` · **P→M**
  - Task: print the newest gap and the one before it with `[-1]` and `[-2]`.
  - CP1–2 [CMB].
  - Hooks: BQ: print the newest gap without negative indexes (a `len()` preview: "you'll need a tool from the
    next steps").
- **3A-05 `new-chalk-mark` · A new chalk mark** · intro `attr:append` · **P→R→M**
  - Task: append **your own guess** for the next gap (a number below 37).
  - CP1: the wall has 8 items, and the last is an int smaller than 37.
  - Catches: `chalk_wall + 33` (TypeError: list + int); `.append("33")` [NUM].
  - Hooks: DF (33).
- **3A-06 `how-long` · How long is the wall?** · intro `call:len` · **P→I**
  - Task: print `len(chalk_wall)`, then use it to read the last item: `chalk_wall[len(chalk_wall) - 1]`.
  - CP1–2.
  - Hooks: WT: "why the last index is length minus one".
- **3A-07 `fix-a-mark` · Fix a mark** · intro — · **M**
  - Task: the starter wall has `74` where `47` belongs (Lucky's handwriting). Fix it by index; don't retype the
    list.
  - CP1: the wall is right, and there is an index assignment (AST: an `Assign` whose target is a `Subscript`).
- **3A-08 `join-two-walls` · Join two walls** · intro — (`+` on lists) · **P→M**
  - Task: `old_marks + new_marks`.
  - CP1 [OUT].
- **3A-09 `lists-inside-lists` · Lists inside lists** · intro — · **P→I→M**
  - Code: `roster = [["Oogrish", 18], ["Gearshift", 20], ["Bomb Shell", 24], ["Lucky", 26]]`.
  - Predict `roster[3][1]`.
  - Task: print Bomb Shell's name and Oogrish's mana.
  - CP1–2 [CMB].
  - Hooks: **TR** (boxes in boxes); AW[picture: a shelf of small shelves; step-by-step: "outer number first,
    then inner"]; "a box of boxes" prepares nested dicts.
- **3A-10 `broken-spell-3A` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `chalk_wall[7]` (IndexError), `chalk_wall(0)` (TypeError: 'list' object is not callable),
    `.append(33, 30)`, and `[48 48]`.
  - CP1–4.

### Quiz 3A [C, 8 questions]

**Types:** 4 predict · 2 mc · 1 parsons · 1 bug.

**Samples:**
1. **predict.** `chalk_wall[-1]` and `len(chalk_wall)` → `37` and `7`.
2. **predict.** `roster[2][0]` → `Bomb Shell`.
3. **bug.** `chalk_wall[7]` should read the last item.

### Project 3P1 "Oogrish's Training Log" [C, 25 min]

**Premise.** Oogrish logs each yard drill and its score.

**Tasks:**
1. Make `log` as a list of `[drill, score]` pairs (any drills).
2. Append a new drill.
3. Fix a score by nested index.
4. Add next week's pairs with `+`.
5. Print the last drill and its score using `[-1]` and `str()`.
6. Print how many drills there are with `len`.

**Checks:** [CMB] reruns with other starting logs.

**Stretch:** say whether the last score beat the first (`if`).

**Consolidates:** 3A and Unit 2 (spaced practice).

**Not a gradebook.**

### Lesson 3B "Reading the Wall Closely" [C]

*Mar'tu remembers…*
1. Predict `"█" * 0`. (1C)
2. Fix a missing colon. (2B/2C)

- **3B-01 `range-of-marks` · Ranges** · intro `call:range` `call:list` · **P→I**
  - Predict `list(range(5))` and `list(range(1, 7))`. A d6's faces are `range(1, 7)`, but `randint(1, 6)`.
  - CP1: make `d8_faces` with `range` [OUT].
  - Hooks: AW[picture of a ruler: the stop mark isn't included].
- **3B-02 `slice-the-wall` · Slice the wall** · intro `node:Slice` · **P→M**
  - Task: make `last_three = chalk_wall[-3:]` and `first_two = chalk_wall[0:2]`.
  - CP1–2 [CMB].
  - Hooks: WT: "a slice is a new list".
- **3B-03 `sorted-or-sort` · `sorted` or `.sort`** · intro `call:sorted` `attr:sort` · **P→I**
  - Investigate: `result = chalk_wall.sort()`, then print `result` → `None`.
  - Task: make `shortest_first` with `sorted()`, leaving `chalk_wall` unchanged.
  - CP1–2.
  - Hooks: WT: "`None` means 'nothing handed back'. You'll meet it again with recipes."
- **3B-04 `how-many-times` · How many times?** · intro `attr:count` · **P→M**
  - Task: count the 48s.
  - CP1.
- **3B-05 `broken-spell-3B` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `chalk_wall.sort()[0]` (TypeError on `None`), and a slice that is one off.
  - CP1–2.

### Lesson 3C "More List Tools" [O]

- **3C-01 `insert-and-pop`** · intro `attr:insert` `attr:pop` · **P→M**: rearrange the resonance-array parts.
- **3C-02 `remove-and-in`** · intro `attr:remove` `op:In` · **P→M**: Lucky wanders off the roster list. Is
  `"Lucky" in names`?
- **3C-03 `biggest-and-smallest`** · intro `call:max` `call:min` `call:sum` · **P→M**: the longest and shortest
  gap, and the total hours.

### Quiz 3B [O, 8 questions]

**Samples:**
- predict `list(range(1, 7))` → `[1, 2, 3, 4, 5, 6]`
- predict `wall.sort()` → `None` and the sorted `wall`
- predict `chalk_wall[-3:]` → `[44, 41, 37]`

### Articles 3-A1 Tuples [O] and 3-A2 `zip()` [O]

- **Tuples:** `("Lucky", 26)`, unpacking `name, mana = hero`, and immutability. intro `node:Tuple`.
- **`zip()`:** pair `names` with `manas`. It stops at the shorter list. intro `call:zip`.
- Each article has one try-it.

### Project 3P2 "The Basement Inventory" [O, 35 min]

**Premise.** Mar'tu's basement is full of brass parts from the Institute's resonance array. Two parallel lists
hold part names and counts.

**Tasks:**
1. Insert a new part at the front.
2. Pop the part Gearshift borrows.
3. Sort the counts and slice the top 3.
4. Count duplicate parts.
5. `zip` the two lists into pairs.

**Prerequisites:** 3C, 3-A2.

**Consolidates:** 3B–3C.

### Quick Check 3

1. Predict `chalk_wall[-2]`, `len(chalk_wall)` and `roster[1][0]`.
2. **Code:** append a guess and print the last item.
3. mc: what `x = wall.sort()` holds.
4. **Code:** slice the last three gaps.

**Skills:** `list-make`, `list-index`, `list-append-len`, `list-nested`, `range-slice-sort`.

### Cheatsheet 3

`[48, 47]` · `wall[0]` first · `wall[-1]` last · `wall[i] = x` · `.append(x)` · `a + b` · `len(wall)` ·
`roster[3][1]` · `range(1, 7)` stops before 7 · `wall[-3:]` · `sorted(wall)` versus `wall.sort()` → `None` ·
`.count(x)` · IndexError means "no such position".

---

## Unit 4 · Dictionaries: "Stat Sheets and Spell Books" (NEW: deviation D1)

**Mar'tu's framing.** "A list remembers order. It does not remember *meaning*. Which number is Lucky's armor?
Which is his mana? A dictionary keeps a label on every value. At the Institute, every student had a record like
this. Mine said 'talks too little'."

**RPG tie-in.** Hero stat sheets use the real values from the party table. Abilities nest inside each sheet. The
spell book is a dict of spells, and the roster is a list of sheets. This is the campaign's data model, rehearsed
with near-transfer names.

**Learning objectives. Student can…**
1. Write a dict literal with quoted string keys, `:` and commas.
2. Read a value by key (`hero["mana"]`), and fix a `KeyError` caused by spelling, case or nesting.
3. Change a value and add a new key by assignment, including `hero["mana"] = hero["mana"] - cost`.
4. Test membership with `in` / `not in` (on keys, not values).
5. Use a key stored in a variable (`book[spell_name]` versus `book["spell_name"]`).
6. Read and write nested values: `hero["abilities"]["magical_affinity"]`.
7. Read from a list of dicts: `roster[2]["name"]`.
8. Build a dict from variables and store it by key: `spell_book[spell_name] = spell`.
9. Combine nested reads with `if/elif/else`: get it, compare, act.

**Campaign links.**
- Obj 1, 8 → `spell-book` (the `spell` dict filled from parameters, then `spell_book[spell_name] = spell`).
- Obj 2–3 → `mana-bars` (`caster["mana"]`, `caster["max_mana"]`) and `hold-the-barrier` (the mana
  subtraction).
- Obj 4 → `hold-the-barrier` (`if spell_name not in caster["spell_book"]:`).
- Obj 6 → `caster["abilities"]["magical_affinity"]`.
- Obj 7 → `member["spell_book"]` and `party.members`.
- Obj 9 → the body of `hold-the-barrier`.

**Items in order:**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 4A "Stat Sheets" | C | 32 |
| 2 | Lesson 4B "Sheets Inside Sheets" | C | 30 |
| 3 | Quiz 4 | C | 10 |
| 4 | Project 4P "Mar'tu's Ledger of Heroes" | C | 40 |
| 5 | Article 4-A1 "Why Does This Work? Keys and `.get()`" | O | 8 |
| 6 | Quick Check 4 | O | — |
| 7 | Cheatsheet 4 | ref | — |

### Lesson 4A "Stat Sheets" [C]

*Mar'tu remembers…*
1. `roster[3][1]` from the list version. (3A)
2. What does `x = wall.sort()` hold? (3B)

- **4A-01 `which-number-is-which` · Which number is which?** · intro — · **P (hook)**
  - Code: `lucky = ["Lucky", 13, 26, 3]`.
  - Task: print Lucky's armor bonus. Which index is it? Students guess, then check.
  - CP1: prints 3.
  - Mar'tu: "You had to remember that position 3 means armor. Python can remember for you."
- **4A-02 `make-a-sheet` · Make a sheet** · intro `node:Dict` · **M**
  - Example: `bomb_shell = {"name": "Bomb Shell", "dexterity": 6}`.
  - Task: make `gearshift` with `"name"`, `"magical_affinity"` (10), `"max_mana"` (20) and `"armor_bonus"` (3),
    from his sheet.
  - CP1: the keys are exact [KEY]. CP2: the values match the table [NUM, TEXT].
  - Catches:
    - `{name: "Gearshift"}`: a NameError, explained as "keys are text, so they need quotes".
    - `{"name" = ...}`: a SyntaxError, explained as "use `:` between a key and its value".
  - Hooks: AW[analogy: a stat sheet with labeled lines; picture: labeled boxes in one big box; from the
    campaign: the `spell` dict]; PA.
- **4A-03 `read-by-key` · Read by key** · intro — · **P→R→M**
  - Task: print `"Gearshift: 20 mana"` built from the dict.
  - CP1 [OUT, CMB: rerun with changed sheet values].
  - Hooks: spaced practice of `+ str()`.
- **4A-04 `key-errors` · Key errors** · intro — · **D**
  - Task: fix `gearshift["Max_Mana"]` and `gearshift["max mana"]`.
  - CP1–2.
  - Hooks: the KeyError explainer (§2.4).
- **4A-05 `write-by-key` · Write by key** · intro — · **P→R→M**
  - Task:
    1. Gearshift casts Fire Bolt (`fire_bolt_cost = 6`):
       `gearshift["mana"] = gearshift["mana"] - fire_bolt_cost`.
    2. Add a new key: `gearshift["fuel"] = "starlode"`.
  - CP1: mana drops by the cost [CMB: rerun with cost 4]. CP2: the new key exists [KEY].
  - Catches: subtracting a typed 6 instead of the variable [CMB].
  - Hooks: TR; campaign link `caster["mana"] = caster["mana"] - spell["mana_cost"]`.
- **4A-06 `is-it-in` · Is it in the book?** · intro `op:In` `op:NotIn` · **P→I→M**
  - Code: `spell_book = {"Glow": 2, "Warm Hands": 3}`.
  - Predict `"Glow" in spell_book` → True, and `2 in spell_book` → False, because `in` looks at keys.
  - Task: if `"Fire Bolt" not in spell_book`, print a message.
  - CP1 [CMB: rerun with Fire Bolt added, so no message].
  - Hooks: WT: "`in` checks keys".
- **4A-07 `key-from-a-box` · A key from a box** · intro — · **P→I→M**
  - Code: `spell_name = "Warm Hands"`.
  - Predict `spell_book[spell_name]` versus `spell_book["spell_name"]` (KeyError: `'spell_name'`).
  - Task: print the cost of whichever spell `spell_name` names.
  - CP1 [CMB: rerun with `spell_name = "Glow"`].
  - Catches: A-02's name-in-quotes habit in a new form.
  - Hooks: AW[step-by-step: what Python looks up in each case]; PA.
- **4A-08 `broken-spell-4A` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `{"name" = "Lucky"}`, `lucky[name]`, `lucky["Mana"]`, and `lucky.mana` (an AttributeError, explained
    as "use square brackets").
  - CP1–4.

### Lesson 4B "Sheets Inside Sheets" [C]

*Mar'tu remembers…*
1. Reading a nested list element. (3A)
2. A truth value for an `and`. (2B)

- **4B-01 `abilities-inside` · Abilities inside** · intro — · **P→R→I**
  - Code: `bomb_shell = {"name": "Bomb Shell", "mana": 24, "abilities": {"dexterity": 6, "wisdom": 8,
    "magical_affinity": 12}}`.
  - Task: print Bomb Shell's wisdom.
  - Subgoal label: *Get it out of the dictionary: outer key, then inner key.*
  - CP1: prints 8, read through both keys [CMB].
  - Catches: `bomb_shell["wisdom"]` (KeyError, explained as "wisdom lives inside abilities");
    `bomb_shell["abilities"]` alone prints the whole inner dict.
  - Hooks: **TR** (boxes in boxes); AW[picture: a sheet with an inner card; from the campaign:
    `caster["abilities"]["magical_affinity"]`].
- **4B-02 `change-inside` · Change inside** · intro — · **M**
  - Task: Gearshift tunes Bomb Shell's hands, adding +2 to dexterity, written as a nested read-modify-write.
    Lucky's comment: "That latch might stop hating you."
  - CP1 [CMB: rerun with a different starting dexterity].
- **4B-03 `the-roster` · The roster** · intro — · **P→M**
  - Setup: the four sheets (real stats) are built in the starter, and `roster = [oogrish, gearshift,
    bomb_shell, lucky]`.
  - Task: print `roster[2]["name"]`, then Oogrish's intelligence through `roster`.
  - CP1–2 [CMB].
  - Hooks: Lucky's box: "In the campaign, this list is called `party.members`."
- **4B-04 `spell-book-of-spells` · A spell book of spells** · intro — · **P→I→M**
  - Code: `spell_book = {"Glow": {"mana_cost": 2, "required_affinity": 3}}`. Predict
    `spell_book["Glow"]["mana_cost"]`.
  - Task: the starter makes `spell_name = "Lantern Ward"`, `cost = 6`, `needed = 9`, and
    `spell = {"mana_cost": 0, "required_affinity": 0}` with the comment "replace each 0 with the matching
    variable".
    1. Replace each 0.
    2. Store the spell: `spell_book[spell_name] = spell`.
  - CP1: the spell's values come from the variables [CMB: rerun with cost 5 and needed 7]. CP2: stored under
    its name, and Glow is kept [KEY, CMB].
  - Catches: literals left in the blanks (A-08 `25 * 2`, and the campaign's "replace each placeholder" step);
    `spell_book["spell_name"] = spell`.
  - Hooks: PA; this is the campaign's instruction style, rehearsed.
- **4B-05 `can-they-cast` · Can they cast?** · intro — · **A→M**
  - Task: given `caster` and `spell = spell_book["Lantern Ward"]`, write an `if/elif/else`:
    - If affinity is too low (nested read), print "isn't skilled enough".
    - Else if mana is too low, print "needs more mana".
    - Else subtract the cost and print the mana left.
  - Subgoal labels: *Get it → Compare → Act.*
  - CP1: the low-affinity case. CP2: the low-mana case. CP3: the casting case, including exactly enough
    mana [BND, via reruns with 4 caster setups].
  - Catches: `<=` instead of `<`; `caster["magical_affinity"]` (skipping a level).
  - Hooks: **PA** (distractors `<=` and the flat key); AW[step-by-step; from the campaign: the
    `hold-the-barrier` comments]; PR: "Navigator reads each condition aloud in plain English".
- **4B-06 `broken-spell-4B` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `bomb_shell["dexterity"]`, `roster["Lucky"]` (TypeError: list indices must be integers), and
    `spell_book[Glow]`.
  - CP1–3.

### Quiz 4 [C, 10 questions]

**Types:** 5 predict · 2 mc · 1 fill · 1 parsons · 1 bug.

**Samples:**
1. **predict.** `print("Glow" in spell_book)` / `print(2 in spell_book)` → `True` then `False`.
2. **mc.** `spell_name = "Glow"`. Which line prints Glow's cost: `spell_book["spell_name"]` /
   `spell_book[spell_name]` / `spell_book.spell_name`? **Answer:** the 2nd.
3. **parsons.** Build a `spell` from `cost` and `needed`, then store it by `spell_name` (distractor:
   `spell_book["spell_name"] = spell`).

**Other questions:**
- predict a nested read → 8
- fill `hero["mana"] = hero["mana"] ___ cost` → `-`
- bug: a KeyError from the wrong nesting level
- predict a list-of-dicts read
- mc: what `in` checks (keys)

### Project 4P "Mar'tu's Ledger of Heroes" [C, 40 min]

**Premise.** Mar'tu copies each hero's record into the cabin ledger, Institute-style.

**Tasks:**
- **A. Sheets**
  1. Make four sheets with `"name"`, an `"abilities"` dict (`magical_affinity` plus two other real abilities
     of the student's choice from the table), and an empty `"spell_book"` dict.
- **B. Let the code combine it**
  2. Set each `["max_mana"]` from `["abilities"]["magical_affinity"] * 2`.
  3. Set `["mana"]` to max.
- **C. Roster**
  4. `roster = [...]`.
  5. Print Bomb Shell's dexterity and Oogrish's intelligence through `roster`.
- **D. Spend**
  6. Gearshift casts Fire Bolt (6).
  7. Lucky drinks glug: +2 mana, but never over max (`if`).
- **E. Spell books**
  8. Add `"Glow"` to Oogrish's book with `spell_book[spell_name] = spell`.
  9. Print whether `"Glow" in` / `not in` each hero's book.

**Checks:**
- Values match the table.
- [CMB] `max_mana` follows affinity.
- Nested reads are right.
- Glug is capped.
- [KEY] Spell-book entries use exact keys.

**Stretch:**
- A status line for two heroes.
- Lucky's "What's in it for me?" line, which prints his mana as a bar with `"█" *`.

**Consolidates:** 4A–4B and Unit 1 (bars, `str`).

### Article 4-A1 "Why Does This Work? Keys and `.get()`" [O]

- Keys are unique, so a second assignment overwrites.
- `.get("glug", 0)` gives a default instead of a KeyError. intro `attr:get`.
- Why `in` is fast.

### Quick Check 4

1. **Code:** make a sheet with given keys [KEY].
2. **Code:** read `["abilities"]["wisdom"]`.
3. **Code:** `book[spell_name] = spell` from variables [CMB].
4. predict `in` / `not in`.
5. **Bug:** a KeyError from a skipped nesting level.

**Skills:** `dict-make`, `dict-read`, `dict-write`, `dict-in`, `dict-key-from-variable`, `dict-nested`,
`list-of-dicts`.

### Cheatsheet 4

`{"name": "Lucky", "mana": 26}` · `hero["mana"]` · `hero["mana"] = hero["mana"] - 3` · `hero["glug"] = 2` (new
key) · `"Glow" in book` / `not in` (keys) · `book[spell_name]` (a variable) versus `book["spell_name"]` (a
literal) · `hero["abilities"]["wisdom"]` · `roster[2]["name"]` · `book[name] = spell` · KeyError means
"no key spelled exactly like that".

---

## Unit 5 · Loops: "Every Member of the Party"

**Mar'tu's framing.** "Four heroes. Four bars to draw. Write it four times? No. Write it once, and let Python
walk down the line, yes?"

**RPG tie-in:**
- The roster loop is the campaign's `for member in party.members:`.
- The chalk-wall gaps reveal that "the decay is accelerating".
- A countdown to the burst.
- Bomb Shell's Velocite watch.

**Learning objectives. Student can…**
1. Explain why loops exist, then write `for item in list:` with an indented body.
2. Loop over a list of dicts, reading keys from each item, and call a helper for each one.
3. Accumulate a total or count, with the reset *before* the loop.
4. Put an `if` inside a loop to filter.
5. Loop with `range(len(...))` to compare neighbors.
6. Write a `while` loop with an update, recognize an infinite loop and stop it, and use `break`.

Optional: `continue`, nested loops, list comprehensions, `a if c else b`, and `.items()`.

**Campaign links:**
- Obj 1–2 → the bottom loops of `spell-book` and `mana-bars` (`for member in party.members: show_mana(member)`).
- Obj 3 → the `hold-the-barrier` mana arithmetic (spaced practice).
- Obj 6 (`break`) → a bridge to early `return` in Unit 6.

**Items in order:**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 5A "For Each, Yes?" | C | 35 |
| 2 | Lesson 5B "While the Clock Ticks" | C | 20 |
| 3 | Lesson 5C "Loops in One Line" | O | 20 |
| 4 | Article 5-A1 "Looping Over a Dictionary" | O | 10 |
| 5 | Quiz 5 | C | 8 |
| 6 | Project 5P "The Velocite Watch" | C | 35 |
| 7 | Quick Check 5 | O | — |
| 8 | Cheatsheet 5 | ref | — |

### Lesson 5A "For Each, Yes?" [C]

*Mar'tu remembers…*
1. A nested dict read: `bomb_shell["abilities"]["wisdom"]`. (4B)
2. Which values can `random.randint(1, 8)` give? (2B)

- **5A-01 `predict-the-loop` · Predict the loop** · intro `node:For` · **P→R→I**
  - Task: predict how many lines `for color in ["gold", "fire orange", "teal", "silver"]: print(color)` prints.
    Then add a fifth color, violet, for Mar'tu.
  - CP1: five lines appear [OUT].
  - Hooks: **TR default-open** (the loop variable changes each pass); AW[analogy: "Mar'tu walks down the line
    and taps each hero"].
- **5A-02 `each-mark` · Each mark on the wall** · intro — · **M**
  - Example: a loop over spell colors.
  - Task: print every gap on the chalk wall as `"48 hours"`.
  - CP1 [LOOP: rerun with a 3-item wall].
  - Catches: seven separate `print` lines [LOOP]; using the example's loop variable is fine. Names matter only
    when the task names them.
- **5A-03 `each-member` · Each member of the party** · intro — · **M**
  - Setup provides `roster` (4 hero dicts) and `show_on_ley_board(text)`.
  - Task: for each `member`, show `member["name"] + ": " + str(member["mana"])`.
  - CP1: 4 lines on the board, in order [CALL]. CP2: still correct with 5 heroes [LOOP].
  - Catches: `print(roster["name"])` (TypeError); writing `roster` where `member` belongs.
  - Hooks: PA; Lucky's box: `for member in party.members: show_mana(member)`; AW[step-by-step trace table:
    `member` on each pass].
- **5A-04 `running-total` · Running total** · intro — · **P→M**
  - Task: add up the party's mana into `total` (start at 0 before the loop).
  - CP1: 88 for the real party [CMB, LOOP].
  - Catches: `total = 0` inside the loop. The total ends as only the last hero's mana, and the explainer note
    says "your total restarts every pass".
  - Hooks: **TR**; AW[picture of a tally jar].
- **5A-05 `the-gaps` · The gaps** · intro — · **P→I→M**
  - Task: use `for i in range(1, len(chalk_wall)):` to print `chalk_wall[i - 1] - chalk_wall[i]`.
  - The output is 0, 1, 1, 2, 3, 4. Mar'tu (after it passes): "The decay is accelerating. Now you have seen it
    yourself."
  - CP1 [OUT, LOOP: rerun with another wall].
  - Hooks: TR; AW[picture: neighbors on the wall].
- **5A-06 `loop-with-a-check` · A check inside the loop** · intro — · **M**
  - Task: print the names of heroes with less than 10 mana ("needs rest").
  - CP1 [CMB: rerun with altered mana].
  - Hooks: BQ: also count them.
- **5A-07 `bars-for-everyone` · Bars for everyone** · intro — · **Mk**
  - Task: for each member, print the name and a bar:
    `"█" * member["mana"] + "░" * (member["max_mana"] - member["mana"])`. This is spaced practice of 1C and
    Unit 4.
  - CP1: each line is right [LOOP, CMB with mana 0 and full].
  - Hooks: PA; Lucky's box: `get_mana_bar`.
- **5A-08 `broken-spell-5A` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: a body that isn't indented, `total = 0` inside the loop, `print(roster["name"])`, and a loop over
    `roster` that prints `roster`.
  - CP1–4.

### Lesson 5B "While the Clock Ticks" [C]

*Mar'tu remembers…*
1. `"Glow" in spell_book`. (4A)
2. Fix `x = wall.sort()`. (3B)

- **5B-01 `countdown` · Countdown** · intro `node:While` · **P→R→I**
  - Task: count `hours_left` from 5 down to 1, then print "Burst!".
  - CP1 [OUT, CMB: rerun with 3].
  - Hooks: TR.
- **5B-02 `the-loop-that-never-ends` · The loop that never ends** · intro — · **D**
  - Task: the glug loop forgets `glug = glug - 1`. Run it, read the step-limit explainer ("Line 3 ran 200,000
    times…"), and fix it.
  - CP1.
  - Hooks: WT: "what the step limit is".
- **5B-03 `stop-at-the-first` · Stop at the first** · intro `node:Break` · **M**
  - Task: find the first gap under 45, print it, and `break`.
  - CP1: exactly one line [OUT, LOOP].
  - Hooks: WT: "`break` leaves the loop. Later, `return` leaves a whole recipe."
- **5B-04 `forecast` · Forecast** · intro — · **Mk**
  - Task: model the decay. Start with `gap = 37` and `shrink = 5` (the student may choose a different
    `shrink`). While `gap > 24`: subtract `shrink`, add 1 to `shrink`, and print `gap`.
  - With the default this prints 32, 26 and 19. Mar'tu is grim: "If this is right, we run out of nights."
  - CP1: works for the default and for a chosen `shrink` [CMB].
  - Hooks: AW[trace table]; story beat (see open question Q8 on foreshadowing).
- **5B-05 `broken-spell-5B` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: a `while` whose update moves the wrong way, and a countdown that is off by one.
  - CP1–2.

### Lesson 5C "Loops in One Line" [O]

- **5C-01 `skip-the-empty`** · intro `node:Continue`: skip heroes with 0 mana.
- **5C-02 `loops-in-loops`** · intro —: print every entry of the 2D training log (nested loops).
- **5C-03 `one-line-loops`** · intro `node:ListComp`: `[h for h in chalk_wall if h < 45]` and
  `[h * 2 for h in chalk_wall]`.
- **5C-04 `choose-in-one-line`** · intro `node:IfExp`: `"ready" if mana >= 3 else "resting"`.
- The comprehensions note says the tracer shows a comprehension as repeated steps on one line.

### Article 5-A1 "Looping Over a Dictionary" [O]

`for name, cost in spell_book.items():`, plus `.keys()` and `.values()`. intro `attr:items` `attr:keys`
`attr:values` `node:Tuple`. One try-it. It recaps Tuples (3-A1) on the page.

### Quiz 5 [C, 8 questions]

**Types:** 5 predict · 1 mc · 2 bug.

**Samples:**
1. **predict.** An accumulator over `[18, 20, 24, 26]` → `88`.
2. **bug.** `total = 0` inside the loop prints `26`. Fix it so it prints `88`.
3. **predict.** `while hours_left > 0` from 3 → `3` `2` `1`.

**Other questions:**
- predict the gaps loop
- mc: how many times a loop body runs
- bug: an infinite while
- predict `break` output
- predict a loop over a roster that reads a key

### Project 5P "The Velocite Watch" [C, 35 min]

**Premise.** Bomb Shell has about a week of Velocite ore left. Gearshift wants numbers, not guesses: "Run the
math."

**Tasks:**
- **A. Use log**
  1. `velocite_used` holds the daily amounts (given).
  2. Total them with a loop.
  3. Average: `total / len(...)`.
- **B. Days left**
  4. A `while` loop counts the days until `ore_left` drops below one day's average use.
- **C. Party check**
  5. For each member, print the name and a mana bar.
  6. Flag anyone under 10 mana.
- **D. Spike**
  7. `break` at the first day over 4 and print it.

**Checks:** [CMB, LOOP] reruns with other logs and rosters.

**Stretch:** a comprehension of the days above average (5C).

**Consolidates:** 5A–5B and Unit 4.

### Quick Check 5

1. **Code:** call a helper for each roster member [CALL, LOOP].
2. **Code:** total the party's mana [CMB].
3. predict a `while` countdown.
4. **Bug:** an accumulator that resets inside the loop.

**Skills:** `for-each`, `accumulate`, `loop-with-if`, `while-loop`, `break`.

### Cheatsheet 5

`for item in items:` + indent · `for member in roster: member["name"]` · `total = 0` before the loop ·
`for i in range(1, len(wall)):` · `while x > 0:` + an update · the step limit means an infinite loop · `break`.

---

## Unit 6 · Functions: "Mar'tu's Recipes"

**Mar'tu's framing.** "At the Institute we called these *recipes*. You write the steps once and give them a name.
When you need them, you call the name. Some recipes need ingredients. Some hand something back. The barrier spell
you will cast one day is a recipe. So is the clock, I think."

**RPG tie-in.** Recipes appear everywhere in the course: rolling dice, max-mana rules, reading stat sheets,
drawing bars, learning spells, and casting from a spell book. This unit is the near-transfer rehearsal of
**every** campaign part. It is also the class's cliff: 0 of 11 students wrote a working function.

**Learning objectives. Student can…**
1. Tell `=` (a box) from `def` (a recipe), and know that defining a recipe doesn't run it. Call a function with
   `()`.
2. Replace `pass` in a function body with a call, with correct indentation.
3. Define parameters and pass arguments. **Use the parameters in the body**, never the test values. Show every
   function with at least two calls.
4. `return` a value. Store a call's result in a variable. Explain `None` when `return` is missing. Return the
   right variable.
5. Store what a helper returns, then pass it to another function (store-then-pass).
6. Return a comparison (`return roll >= needed`). Use `random.randint(1, die_size)` with a parameter.
7. Write functions that read and change a dict passed in (changes are visible to the caller), and build a dict
   from parameters.
8. Guard with an early `return` (`if name not in book: …; return`).
9. Read a helper you didn't write and call it correctly. Know which lines to change and which to leave.
10. Use default and keyword arguments. Explain local scope.
11. Use a function as a value: assign it, pass it without `()`, store it in a dict, and call it from there with
    `book[name]["effect"](hero)`.

**Campaign links:**
- Obj 1–2 → `program-movement`.
- Obj 4–5 → `program-dialogue-prompt` and `show_mana`.
- Obj 6 → `skill-checks`.
- Obj 7 → `spell-book` and `get_mana_bar`.
- Obj 8 → the opening of `hold-the-barrier`.
- Obj 9 → `print_mana` and `reinforce_barrier`.
- Obj 11 → `spell-book` (`strengthen_magic` without `()`) and `hold-the-barrier`
  (`spell["spell_function"](caster)`).

**Items in order:**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 6A "Recipes With Names" | C | 45 |
| 2 | Quiz 6A | C | 10 |
| 3 | Lesson 6B "Recipes That Read Stat Sheets" | C | 45 |
| 4 | Lesson 6C "Spells You Can Hand Over" | C | 35 |
| 5 | Quiz 6B | C | 10 |
| 6 | Article 6-A1 "lambda: Tiny Nameless Recipes" | O | 10 |
| 7 | Article 6-A2 "`map()`: One Recipe, Every Item" | O | 10 |
| 8 | Article 6-A3 "Two Things Back" (multiple returns) | O | 10 |
| 9 | Project 6P "The Resonance Array" | C | 45 |
| 10 | Quick Check 6 | O | — |
| 11 | Cheatsheet 6 | ref | — |

### Lesson 6A "Recipes With Names" [C]

This lesson is **portable**: it uses only Unit 1–2 concepts, so the fast lane can run it right after Unit 2
(§1.5). Its warm-ups are drawn from Units 1–2 for the same reason.

*Mar'tu remembers…*
1. "`=` or `==`: which asks?" (2A)
2. "What does `mana = mana - 3` do?" (1C)

- **6A-01 `box-or-recipe` · A box or a recipe?** · intro `node:FunctionDef` · **P→R→I**
  - Code: `steadying_words = "Steady, now."` (a box) next to `def say_steady():` with an indented
    `print("Steady, now.")` (a recipe).
  - Predict what Run prints: nothing. Defining doesn't run it.
  - Task: call the recipe, then call it twice.
  - CP1: the line prints once [OUT]. CP2: twice, using two calls rather than two prints
    (`_count('call:print') == 1` in the source).
  - Catches: A-02 `def ("character")`. This is the explicit `=` versus `def` contrast the G1 needs list asks for.
  - Hooks: AW[analogy: a box holds a thing, a recipe card holds steps; picture of both side by side;
    from the campaign: "Each `def` line makes a function: a named set of steps."]; TR (watch the `def` line
    being skipped until the call).
- **6A-02 `call-it` · Call it** · intro — · **M→I**
  - Task: write `barrier_report()` with two print lines and call it.
  - Investigate: `barrier_report` with no `()` does nothing.
  - CP1 [OUT].
  - Catches: forgetting `()`. Indentation [explainer].
- **6A-03 `replace-pass` · Replace pass** · intro `node:Pass` · **M**
  - Near-transfer for `program-movement`.
  - Starter: four recipes, `def step_north(): pass` and so on. Setup provides `scout.step(direction)`.
  - Task:
    1. Replace each `pass` with `scout.step("north")` and so on, using the direction in the recipe's name.
    2. Press Run.
  - CP1–4: each recipe, when called, moves the scout in its own direction [CALL].
  - Catches: `scout.step(north)` (NameError, so quotes); all four stepping "north" (copy-paste); a body that
    isn't indented.
  - Hooks: PA (per recipe); AW[in Tor: "`pass` is a blank recipe card"]; Lucky's box: `party.move("left")`.
- **6A-04 `ingredients` · Ingredients** · intro — · **P→R→M**
  - Example: `def cheer(name):` with `print(name + " is ready.")`, called twice with different names.
  - Task: `def warn(hero_name):` prints `<hero_name>, get inside!`. Call it for two heroes.
  - CP1 [PAR: `warn("Tester")`]. CP2: two calls in the code.
  - Catches: a typed `"Lucky, get inside!"` inside the body [PAR].
  - Glossary: *parameter* (the ingredient's name on the card) and *argument* (the actual ingredient you hand
    over).
  - Hooks: AW[analogy: a recipe card says "1 hero"; you hand it Lucky]; TR.
- **6A-05 `use-the-ingredients` · Use the ingredients** · intro — · **M**
  - This is the worksheet's Part 3 cliff, reframed in Tor.
  - Task: `def show_hit(base_damage, bonus):` prints `base_damage + bonus`. Call it with (4, 3) and (8, 2).
  - CP1 [PAR with (6, 1) and (11, 0)]. CP2: both calls are present.
  - Catches:
    - A-06, A-07, B-02 test values: `print(4 + 3)` [PAR].
    - A-01 approximate names: `print(damage + bonus)` raises a NameError, explained as "this recipe's
      ingredients are `base_damage` and `bonus`; Python matches names letter for letter".
    - A-08 picks a literal to hit the answer: `print(7)` [PAR].
  - Hooks: AW[step-by-step: a call table showing parameter → value for each call]; **TR** (parameter boxes
    filled per call); PR: "Explain to your partner why `4 + 3` inside the recipe breaks the second call."
- **6A-06 `send-it-back` · Send it back** · intro `node:Return` · **P→R→I→M**
  - Example: `def triple(n):` with `result = n * 3` and `return result`.
  - Task: `def max_mana_for(affinity):` with `total = affinity * 2` and `return total`. Store
    `lucky_max = max_mana_for(13)` and print it.
  - CP1 [RET: `max_mana_for(9) == 18` and `(12) == 24`]. CP2: `lucky_max` holds 26, assigned from the call
    (STO-style AST check).
  - Catches:
    - Printing instead of returning: "printed 18 but handed back `None`" [RET].
    - B-02 blank `return` [RET].
    - A-07 "the return value is the raw inputs".
  - Hooks: **TR** shows the return arrow landing in `lucky_max` (A-03, A-04 lost the return value); AW[analogy:
    "the recipe hands you a bowl; catch it in a box"; picture].
- **6A-07 `return-the-right-box` · Return the right box** · intro — · **D→M**
  - Task:
    1. `armor_total(base, bonus)` computes `total` but `return result` (copied from 6A-06's example). Fix the
       NameError.
    2. A second function has no `return`, so `"Lucky: " + str(armor_total(10, 3))` prints `Lucky: None`. Add
       the `return` and explain `None`.
  - CP1 [RNM]. CP2 [RET].
  - Catches: A-01 `return reslt`; B-02 missing `return`.
  - Hooks: WT: "`None` is Python's word for 'nothing came back'" (callback to 3B-03).
- **6A-08 `store-then-pass` · Store, then pass it on** · intro — · **M**
  - Near-transfer for `program-dialogue-prompt`.
  - Starter: `get_greeting()` returns `"WELCOME TO THE CABIN."`. Setup provides `show_on_ley_board(text)`.
  - Task: finish `present_greeting()`.
  - Subgoal labels: *Call the helper → Store what it returns → Pass it on.*
  - CP1: calling `present_greeting()` shows the greeting once [CALL]. CP2: the greeting is stored in a variable
    first [STO].
  - Catches:
    - `show_on_ley_board("WELCOME TO THE CABIN.")` typed in [CMB: setup swaps `get_greeting` to return
      another line].
    - `show_on_ley_board(get_greeting)` with no `()` [CALL: "the board showed `<function …>`"].
    - A result that is never stored [STO].
  - Hooks: PA; AW[from the campaign: `dialogue = get_dialogue_prompt_string()` / `print_prompt(dialogue)`].
- **6A-09 `return-a-comparison` · Return a comparison** · intro — · **P→I→M**
  - Example: `spot_check(roll)` written as an if/else that returns `True` or `False`. Then its one-line form
    `return roll >= needed`.
  - Task: write `strength_check(roll)`. Set `needed` to any number from 2 to 20, and return whether the roll
    succeeds.
  - CP1: the result is a bool [RET]. CP2: it succeeds from `needed` up [BND: `needed` is read from the student's
    code, then rolls `needed - 1`, `needed`, `needed + 1`, 1 and 20 are tested].
  - Both the if/else form and the one-line form pass.
  - Catches: `return True` always; `>` versus `>=`.
  - Hooks: PA; Lucky's box: `return roll >= required_roll`.
- **6A-10 `roll-recipe` · A rolling recipe** · intro — · **M**
  - Near-transfer for `perform_roll`.
  - Task: replace `return 1` in `roll_die(die_size)` with a random roll from 1 to `die_size`.
  - CP1 [RND: `roll_die(6)` calls `randint(1, 6)`; `roll_die(20)` calls `randint(1, 20)`].
  - Catches: `random.randint(1, 20)` with a typed size (A-06 test values) [RND message]; a missing
    `import random`.
  - Hooks: AW[from the campaign].
- **6A-11 `broken-spell-6A` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs:
    - a missing colon after `def`
    - a body that isn't indented
    - `def max_mana = 18` [DEF]
    - a call made before the `def` (NameError: order matters)
    - a returned wrong name
  - CP1–5.

### Quiz 6A [C, 10 questions]

**Types:** 5 predict · 2 mc · 1 parsons · 1 fill · 1 bug.

**Samples:**
1. **predict.** A program that only defines `say_steady()` and never calls it → *(nothing)*.
2. **predict.** `def max_mana_for(affinity): print(affinity * 2)`, then `lucky_max = max_mana_for(13)` and
   `print(lucky_max)` → `26` then `None`.
3. **predict.** `latch_check` with `needed = 11` called on 10, 11 and 12 → `False` `True` `True`.

**Other questions:**
- mc: parameter or argument?
- parsons: store-then-pass, with distractor `show_on_ley_board(get_greeting)`
- fill `return roll ___ needed` → `>=`
- bug: test values in the body
- predict `y = double(4)` / `print(y + 1)` → `9`
- mc: which line runs first?

### Lesson 6B "Recipes That Read Stat Sheets" [C]

*Mar'tu remembers…*
1. A nested dict write. (4B)
2. A for-each over the roster. (5A)

- **6B-01 `hand-over-a-sheet` · Hand over a sheet** · intro — · **M**
  - Task: `mana_line(hero)` returns `"<name>: <mana>/<max_mana>"`. Call it for two heroes.
  - CP1 [PAR: a test dict named `"Tester"`, RET].
  - Hooks: AW[from the campaign: `get_mana_bar(caster)`].
- **6B-02 `recipes-change-sheets` · Recipes change sheets** · intro — · **P→I→M**
  - Investigate: after `rest(lucky)`, the caller's `lucky` has full mana.
  - Task: `spend(hero, cost)` subtracts the cost from `hero["mana"]`. No return is needed.
  - CP1 [PAR with a test dict; the caller's dict changes].
  - Hooks: WT: "same sheet, two labels"; TR.
- **6B-03 `many-ingredients` · Many ingredients** · intro — · **M**
  - Starter: `make_spell(mana_cost, required_affinity, color)` builds `spell = {"mana_cost": 0, ...}` with the
    comment "replace each placeholder with the matching parameter".
  - CP1: values follow the arguments [PAR: `make_spell(5, 2, "teal")` and `(9, 7, "gold")`]. CP2: returns the
    dict [RET].
  - Catches:
    - literals left in place (A-08)
    - `"mana_cost": "mana_cost"` (A-02's name-in-quotes habit), with the message "`mana_cost` holds the text
      `'mana_cost'`. Use the parameter without quotes."
  - Hooks: PA; campaign `spell-book` step 1.
- **6B-04 `store-by-name` · Store by name** · intro — · **M**
  - Task: `add_to_book(book, spell_name, spell)` stores the spell under its name.
  - CP1: one spell is stored [KEY]. CP2: a second spell keeps the first.
  - Catches: `book["spell_name"] = spell`; `book = {spell_name: spell}`, which replaces the local name so the
    caller's book is unchanged (message: "the book outside didn't change").
  - Hooks: WT: "why `book = {...}` doesn't reach the caller".
- **6B-05 `guard-at-the-door` · Guard at the door** · intro — · **P→I→M**
  - Task: add an early `return` to `cast_glow(hero, spell_name)`. If the spell is `not in`
    `hero["spell_book"]`, show `"<name> doesn't know <spell>."` and `return`.
  - CP1: an unknown spell gives one message and the mana is unchanged [CALL]. CP2: a known spell still
    proceeds.
  - Hooks: AW[analogy: "a guard checks your name at the door before anything else happens"]; WT: the early
    `return` is like `break` for a whole recipe; Lucky's box: the opening of `cast_spell`.
- **6B-06 `read-the-helper` · Read the helper** · intro — · **I→R**
  - Starter: a visible `draw_bar(hero, bar)` with the comments "# This function is already finished. Leave it
    as it is." and "It draws bar in this hero's row."
  - Questions:
    - "Which lines should you change?" (none in `draw_bar`)
    - "What two things does it need?"
  - Task: call it for Lucky with a bar string.
  - CP1 [KEEP]. CP2 [CALL with `(lucky, <str>)`].
  - Hooks: Lucky's box: `print_mana(caster, mana_bar)`; P19 practice.
- **6B-07 `bar-then-draw` · Build the bar, then draw it** · intro — · **Mk**
  - Near-transfer for `mana-bars`, using Gearshift's starlode gauge.
  - Starter: `get_fuel_bar(robot)` has `"▮" * 0` and `"▯" * 0`, with comments naming
    `robot["fuel"]` and `robot["max_fuel"] - robot["fuel"]`. `show_fuel(robot)` has comments for
    store-then-pass. A loop at the bottom covers `robots`.
  - CP1: 3 of 5 gives `Fuel [▮▮▮▯▯] 3/5`. CP2: empty and full gauges. CP3: `show_fuel` draws once [CALL]. CP4:
    the bar is stored in a variable [STO]. These mirror the campaign's four checks.
  - Catches: `"▯" * robot["max_fuel"] - robot["fuel"]` (TypeError, precedence); `draw_bar(robot, get_fuel_bar)`.
  - Hooks: PA (per function); TR; BQ: a glug gauge for Lucky.
- **6B-08 `defaults-and-names` · Defaults and names** · intro `node:DefaultArg` `node:KeywordArg` · **P→M**
  - Task: `roll_die(die_size=20)`; `roll_die()` rolls a d20 and `roll_die(die_size=6)` a d6.
  - CP1 [RND].
  - Hooks: WT.
- **6B-09 `inside-stays-inside` · Inside stays inside** · intro — · **P→I**
  - Predict: printing `restored` outside `rest()` gives a NameError. Parameters and inner boxes live only
    inside the recipe.
  - Task: return `restored` and print the returned value.
  - CP1 [RET].
  - Hooks: AW[picture: the recipe's own kitchen].
- **6B-10 `broken-spell-6B` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: a missing `return` in `mana_line`, so `"Status: " + mana_line(lucky)` raises a TypeError on
    `NoneType`; `book["spell_name"]`; `"░" * a - b`; a literal used instead of a parameter.
  - CP1–4.

### Lesson 6C "Spells You Can Hand Over" [C] (deviation D2)

*Mar'tu remembers…*
1. Store-then-pass. (6A)
2. `spell_book[spell_name] = spell`. (4B)

- **6C-01 `name-without-parentheses` · A name without parentheses** · intro — · **P→I→M**
  - Task: `warm_hands(hero)` shows a message.
    1. Predict what `chosen_spell = warm_hands` does: nothing visible. The box now holds the *recipe*.
    2. Call `chosen_spell(lucky)`.
  - CP1: `chosen_spell` holds the function [NOP]. CP2: one call happened [CALL].
  - Catches: `chosen_spell = warm_hands(lucky)`, which stores `None`; the later call then raises "NoneType
    not callable" [explainer].
  - Hooks: AW[picture: a box holding a recipe card; analogy: "handing someone the card versus cooking the meal
    and handing them the empty pot"]; WT; TR.
- **6C-02 `hand-it-over` · Hand it over** · intro — · **M→Mk**
  - Given: `cast_on_everyone(roster, effect)` loops and calls `effect(hero)`.
  - Task:
    1. Call it with `warm_hands`, no parentheses.
    2. Write your own `cool_down(hero)` and hand it over too.
  - CP1 [CALL ×4]. CP2: your effect ran for every hero [CALL, NOP].
  - Catches: `cast_on_everyone(roster, warm_hands(lucky))` [NOP].
  - Hooks: Lucky's box: `add_spell(..., strengthen_magic)`; BQ: an effect that changes mana.
- **6C-03 `recipe-in-a-box` · A recipe in a box** · intro — · **P→M**
  - Code: `glow = {"mana_cost": 2, "required_affinity": 3, "effect": light_lantern}`.
  - Predict: `glow["effect"]` alone does nothing; `glow["effect"](lucky)` runs it.
  - Task: cast Glow on Lucky from the dict.
  - CP1 [CALL].
  - Catches: missing `(lucky)`.
  - Hooks: AW[picture; from the campaign: `spell["spell_function"](caster)` with "the parentheses on the end are
    what call it"].
- **6C-04 `write-the-spell-book` · Write the spell book** · intro `const:None` · **A→M**
  - Near-transfer for `spell-book`.
  - The starter's placeholders are `0, 0, None`, exactly like the campaign's `"spell_function": None`. That is
    why this exercise introduces the literal `None`.
  - Starter: `learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect)` builds a dict with
    those placeholders, plus the comment "Store the spell in spell_book, using spell_name as the key". A loop at the
    bottom gives every hero Lantern Ward (6 mana, affinity 9, `lantern_ward`).
  - CP1: stored under its name. CP2: the values match the arguments [PAR]. CP3: a second spell keeps the first.
    CP4: every hero knows Lantern Ward. These mirror the campaign's checks.
  - Catches: literals left in place; the effect called in the bottom loop (`lantern_ward(hero)`) [NOP].
  - Hooks: **PA**; AW.
- **6C-05 `cast-from-the-book` · Cast from the book** · intro — · **A→Mk**
  - The supported rehearsal of `hold-the-barrier`.
  - Starter: `cast(hero, spell_name)` with the guard and `spell = hero["spell_book"][spell_name]` given, then
    three comments.
  - Task: write the `if/elif/else`:
    - nested affinity `<` required → message
    - `elif` mana `<` cost → message
    - `else`: call `spell["effect"](hero)`, subtract the cost, and call `show_mana(hero)`
  - CP1: a skilled caster with enough mana casts. CP2: the mana bar updates. CP3: too little affinity doesn't
    cast. CP4: too little mana doesn't cast. CP5: exactly enough mana still casts. CP6: the spell's own cost is
    used. These mirror the campaign's six checks.
  - Catches: `<=`; `spell["effect"]` with no `(hero)`; `hero["magical_affinity"]`; subtracting a typed number;
    `hero["mana"] - cost` without assigning it back.
  - Hooks: **PA** (adaptive; distractors as listed); subgoal labels; AW[step-by-step; from the campaign]; this
    is the most important exercise for the hint ladder and the proactive offer.
- **6C-06 `broken-spell-6C` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `spell["effect"]` not called; `learn_spell(..., lantern_ward(hero))`; `<=`; a subtraction that is
    never stored.
  - CP1–4.

### Quiz 6B [C, 10 questions]

**Types:** 4 predict · 3 mc · 2 parsons · 1 bug.

**Samples:**
1. **predict.** `spells = {"glow": glow}` / `print(spells["glow"]("Lucky"))` → `Lucky glows.`
2. **mc.** "Which line hands over the recipe without running it?"
   - Choices: `cast_on_everyone(roster, warm_hands)` / `cast_on_everyone(roster, warm_hands())` /
     `cast_on_everyone(roster, "warm_hands")`. **Answer:** the 1st.
3. **predict.** `spend(lucky, 3)` changes the caller's dict: `print(lucky["mana"])` → `23`.

**Other questions:**
- parsons: the `cast` body with indentation (distractors `<=` and `spell["effect"]`)
- parsons: `learn_spell`
- bug: `"░" * a - b`
- mc: what does `return` with nothing after it do?
- predict: the guard clause's output

### Article 6-A1 "lambda: Tiny Nameless Recipes" [O]

`sorted(roster, key=lambda hero: hero["mana"])`. intro `node:Lambda`. One try-it.

### Article 6-A2 "`map()`: One Recipe, Every Item" [O]

`list(map(max_mana_for, [9, 10, 12, 13]))`. intro `call:map`. One try-it. Compare it with a loop.

### Article 6-A3 "Two Things Back" [O]

`return hero["mana"], hero["max_mana"]` / `now, most = mana_range(lucky)`. intro `node:Tuple` (a recap card if
3-A1 was skipped).

### Project 6P "The Resonance Array" [C, 45 min]

**Premise.** The brass resonance array Mar'tu hauled from the Institute has dials, and each dial needs a formula.
Mar'tu: "At the Institute we wrote every dial as a recipe. Then nobody argued about the arithmetic."

**Tasks:**
- **A. Dials**
  1. `max_mana_for(affinity)`.
  2. `average_damage(die_size)` returns `(1 + die_size) / 2`.
  3. `hit_strength(die_size, armor_bonus=0)` uses `average_damage` (composition).
  4. `next_gap(last_gap, shrink)`.
- **B. Calibrate**
  5. `calibrate(hero)` returns a dict of readings for one hero, built by calling the dial recipes on the hero's
     sheet.
- **C. Run the array**
  6. Loop over `roster` and print each hero's readings with `+ str()`.
- **D. Swap a dial**
  7. `run_array(roster, dial)` takes a recipe as a value and prints `dial(hero)` for each hero.

**Checks:** [PAR, RET] fresh values for every dial; [CALL, NOP] for D.

**Stretch:**
- A keyword-argument call.
- A dial for Lucky's Telegun hedge odds.

**Consolidates:** all of Unit 6 plus Units 4–5.

### Quick Check 6 (test-out; G4 must not skip this unit untested)

1. **Code:** a two-parameter function that uses and returns its parameters [PAR, RET].
2. **Code:** store-then-pass with a helper [STO, CALL].
3. **Code:** `return roll >= needed` with boundaries [BND].
4. **Code:** build a dict from parameters and store it by name [PAR, KEY].
5. mc: hand over versus call (`warm_hands` versus `warm_hands()`).
6. predict: a stored function call, and a missing `return` → `None`.

**Skills:** all of the Unit 6 skills in §2.6.

### Cheatsheet 6

`def name():` + indent · defining isn't calling · `name()` calls · `pass` · parameter versus argument ·
`return value` · `x = f()` catches it · no `return` → `None` · `return a >= b` · `random.randint(1, die_size)` ·
store, then pass · the early-`return` guard · `def f(x=20)` / `f(x=6)` · changes to a dict reach the caller ·
`f` (the recipe) versus `f()` (the result) · `book[name]["effect"](hero)`.

---

## Unit 7 · Code Challenges (optional): "Trials of the Yard"

**Framing.**
- **Mar'tu:** "Oogrish says a weapon is learned in the yard, not in the book. These are his trials. They are
  optional."
- **Lucky:** "What's in it for me?"
- **Mar'tu:** "Practice. And Oogrish stops lecturing you."

**Format** (kind `challenge`):
- A signature, a short in-world prompt, and a test table (2–3 visible tests plus hidden labeled tests).
- Support "light": hints unlock after the first failed run.
- Every core challenge has an **advanced variant**: edge cases, a stricter spec, a blank file, or a refactor.
- **Unlock:** the whole unit opens after Unit 6, as in the syllabus. The Control Flow, Lists and Dictionaries
  sets are also offered as "Trials" to anyone on a hint-free streak in Units 2–4, written from a blank file as
  scripts (no `def`) so the concept gate holds.

**Objectives:** apply Units 2–6 to unseen problems from a signature, handle boundary and empty cases, and read
test tables (the debugging habit).

**Campaign links:**
- T-CF-1 and its advanced variant → the `hold-the-barrier` logic.
- T-CF-3 → skill checks with Dumb Luck.
- T-D → `spell-book` and nested reads.
- T-F-3 advanced (a dict of recipes) → `spell["spell_function"](caster)`.
- T-Own → reading check messages the way the campaign's checks are written.

| Set | Core challenge (prompt) | Advanced variant |
|---|---|---|
| **Control Flow** | **T-CF-1** `can_cast(mana, cost)` → True when mana covers the cost (exactly enough counts). | `can_cast(mana, cost, affinity, required)` → returns `"ok"`, `"skill"` or `"mana"`, checking skill first. |
| | **T-CF-2** `clock_color(hours_left)` → `"red"` (≤ 2), `"bright blue"` (≤ 12), else `"calm blue"`. | Negative hours → `"broken"`. Adds `flashing=False` (default arg): when flashing, always `"red"`. |
| | **T-CF-3** `passes_with_luck(first_roll, second_roll, needed, has_luck)` → passes on the first roll, or on the reroll if `has_luck`. | Return `"first"`, `"reroll"` or `"none"`. |
| **Lists** | **T-L-1** `newest_gap(wall)` → the last item. | An empty wall → `None`. |
| | **T-L-2** `last_three(wall)` → the slice. | `total_drop(wall)` = first − last, with 0 when there are fewer than 2 items. |
| | **T-L-3** `add_guess(wall, guess)` → appends only if `guess` is below the newest gap, and returns the wall. | Return a **new** list and leave the original unchanged (`wall[:] + [...]`). |
| **Dictionaries** (D8) | **T-D-1** `spell_cost(book, name)` → the cost, or 0 if unknown. | `cheapest_spell(book)` → the name of the cheapest spell (loop). |
| | **T-D-2** `affinity_of(hero)` → the nested read. | `meets(hero, spell)` → both checks, nested, `<` versus `<=` exact. |
| | **T-D-3** `rename_spell(book, old, new)`. | Refuse (return False) when `new` already exists or `old` is missing. |
| **Loops** | **T-Lo-1** `total_mana(roster)`. | `average_mana(roster)` with an empty roster → 0. |
| | **T-Lo-2** `count_below(wall, limit)`. | `first_drop_over(wall, amount)` → the index of the first gap shrink larger than `amount`, else -1 (early exit). |
| | **T-Lo-3** `lowest_mana_name(roster)`. | On a tie, the alphabetically first name. |
| **Functions** | **T-F-1** `make_bar(current, maximum, full="█", empty="░")`. | Clamp `current` into 0..maximum. |
| | **T-F-2** `apply_to_all(roster, effect)` → a list of the names affected. | Only include a name when `effect(hero)` returns True. |
| | **T-F-3** **Refactor:** replace a four-branch `elif` that maps options to lines with a dict lookup `lines[choice]`, with a default. | A dict of *recipes*: `actions[choice](hero)`. Unknown choice → False. |
| **Write your own checks** | **T-Own** Write 4 `assert` lines that would catch a wrong `can_cast`. intro `node:Assert`. | Write asserts that catch the `<=` bug in a given `cast` *and* pass the correct one. |

**Quick Check / Cheatsheet:** none (this unit is optional). The Trials cheatsheet is "how to read a test table".

---

## Unit 8 · Strings: "Runes and Ribbons"

**Mar'tu's framing.** "Runes are only letters in a row. Python sees words the same way. Today we cut them,
stretch them, and make them behave. Lucky, your notes are next."

**RPG tie-in:**
- Bomb Shell's clipped sentences (`.split()`).
- Lucky's "What's in it for me?" (methods).
- The greenroom sign ("Greenroom, Interior" / "EXIT"; slicing).
- "It is NOT a compass" (`.replace`).
- Mar'tu's dialogue lines tidied with `.lower().capitalize()`.
- Bars one more time.

**Learning objectives. Student can…**
1. Index and slice strings, and use `len()`.
2. Explain that strings can't be changed in place, and build new ones instead.
3. Test for a substring with `in`, and loop over the characters.
4. Use escape characters `\" \n \t`.
5. Call methods (`.lower() .upper() .title() .capitalize() .strip() .replace() .find()`), knowing they *return
   new strings*, so reassign (`line = line.lower()`). Chain them (`.lower().capitalize()`).
6. Use `.split()` and `" ".join(...)`, and convert digits with `int()`.
7. Read and write f-strings, **and** read `+ str()` lines fluently (the campaign uses the latter).
8. Build a status bar with `"█" * n` and `str()` for any values.

**Campaign links:**
- Obj 5 → `program-dialogue-prompt` (`dialogue_input = dialogue_input.lower()`) and `program-dialogue-options`
  (`option_1.lower().capitalize()`).
- Obj 7–8 → the `mana-bars` return line.

**Items in order:**

| # | Item | Flag | Min |
|---|---|---|---|
| 1 | Lesson 8A "Strings Are Rows of Letters" | C | 30 |
| 2 | Quiz 8A | C | 6 |
| 3 | Lesson 8B "Words That Change Shape" | C | 35 |
| 4 | Quiz 8B | C | 8 |
| 5 | Project 8P1 "The Water-Stained Log" | O, recommended | 40 |
| 6 | Project 8P2 "The Institute Cipher" | O, off-platform option | 60 |
| 7 | Quick Check 8 | O | — |
| 8 | Cheatsheet 8 | ref | — |

### Lesson 8A "Strings Are Rows of Letters" [C]

*Mar'tu remembers…*
1. `spells["glow"]` versus `spells["glow"](hero)`. (6C)
2. Why `"░" * (max_mana - mana)` needs parentheses. (1C/6B)

- **8A-01 `letters-have-places` · Letters have places** · intro — · **P→R→M**
  - Predict `"Telegun"[0]`, `[-1]` and `len`.
  - Task: build `initials` from the roster's names with a loop (spaced practice of Units 4–5).
  - CP1 [LOOP, CMB].
  - Hooks: AW[picture: letters in numbered tiles, like the chalk wall].
- **8A-02 `slice-a-word` · Slice a word** · intro — · **P→M**
  - Task: from `sign = "Greenroom, Interior"`, slice out `Greenroom` and `Interior`.
  - CP1–2.
- **8A-03 `letters-cant-change` · Letters can't change** · intro — · **D→M**
  - Task: `word[0] = "C"` raises a TypeError. Build `"C" + word[1:]` instead.
  - CP1.
  - Hooks: WT: immutability.
- **8A-04 `is-it-in-there` · Is it in there?** · intro — · **M**
  - Task: `clock_warning(report)` returns whether `"red"` appears in `report.lower()`. This is a function-shaped
    exercise, for spaced practice.
  - CP1 [PAR, RET; "The clock is RED." → True].
- **8A-05 `letter-by-letter` · Letter by letter** · intro — · **M**
  - Task: `count_full(bar)` counts the `"█"` blocks with a loop.
  - CP1 [PAR, RET].
  - Hooks: BQ: count the empty blocks too.
- **8A-06 `escape-marks` · Escape marks** · intro `const:escape` · **P→I**
  - Task: print `Mar'tu said, "It is not a compass."` with `\"`, and the chalk wall one hour per line with
    `\n`.
  - CP1–2 [OUT].
  - Hooks: a note that formatting is off, so quotes stay as typed.
- **8A-07 `bars-one-more-time` · Bars one more time** · intro — · **Mk**
  - Task: `make_bar(current, maximum)` returns `"Glug [▓▓░] 2/3"`-style text for any values.
  - CP1: 2 of 3. CP2: empty and full [PAR, RET].
  - Hooks: Lucky's box: the `mana-bars` return line; PA.
- **8A-08 `broken-spell-8A` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs: `"░" * 10 - 3`, an index past the end, `word[0] = "X"`, and `len(26)`.
  - CP1–4.

### Quiz 8A [C, 6 questions]

**Samples:**
1. **predict.** `"Telegun"[-1]` and `"Greenroom, Interior"[:9]` → `n` and `Greenroom`.
2. **bug.** `word[0] = "C"` should produce `Compass`. Fix: `"C" + word[1:]`.
3. **predict.** `"red" in "The clock is red."` → `True`.

The rest: a slice and `len`.

### Lesson 8B "Words That Change Shape" [C]

*Mar'tu remembers…*
1. `return` versus print, and `None`. (6A)
2. Loop over the roster and read a nested key. (5A/4B)

- **8B-01 `loud-and-quiet` · Loud and quiet** · intro `attr:upper` `attr:title` `attr:capitalize` · **P→R→I**
  - Investigate: `line.upper()` alone doesn't change `line`. Reassign it.
  - CP1: `line` is now uppercase.
  - Catches: forgetting to reassign.
  - Hooks: AW[analogy: "a method hands you a new copy; catch it"].
- **8B-02 `chain-the-spells` · Chain the spells** · intro — (adds `attr:capitalize` on the fast lane) ·
  **P→I→M**
  - Near-transfer for `program-dialogue-prompt`.
  - Task: `tidy_line(raw)` lowercases, then capitalizes, then returns. First in two steps
    (`line = raw.lower()`, `line = line.capitalize()`), then chained: `raw.lower().capitalize()`.
  - CP1: `"WHAT IS THE DECAY?"` → `"What is the decay?"` [PAR, RET]. Both forms pass.
  - Hooks: Lucky's box: `option_1.lower().capitalize()`. **Portable for the Module 1 fast lane.**
- **8B-03 `split-the-clipped` · Split the clipped** · intro `attr:split` `call:int` · **P→M**
  - Task: split Bomb Shell's report `"Shield up. Latch stuck. Moving out."` on `". "`. Count its words with
    `len(report.split())`. Turn `"48"` into 48 with `int()`.
  - CP1–3.
- **8B-04 `join-them-back` · Join them back** · intro `attr:join` · **P→M**
  - Task: `" ".join(words)` (called on the separator), and `", ".join(colors)`.
  - CP1–2.
  - Catches: `words.join(" ")` (AttributeError).
- **8B-05 `strip-and-replace` · Strip and replace** · intro `attr:strip` `attr:replace` · **P→M**
  - Task: in Lucky's note `"  It's a compass.  "`, strip the spaces and replace `compass` with `Ley Clock`.
    Mar'tu: "Thank you."
  - CP1–2.
- **8B-06 `find-a-rune` · Find a rune** · intro `attr:find` · **P→I**
  - `.find` returns an index, or -1 when the text isn't there.
  - CP1.
- **8B-07 `f-strings` · f-strings** · intro `node:FString` · **P→I→M**
  - Read both forms: `name + ": " + str(mana) + " mana"` and `f"{name}: {mana} mana"`.
  - Task: rewrite one `+ str()` line as an f-string, then translate one f-string back to `+ str()`.
  - CP1: the f-string gives identical output [`_uses('node:FString')`]. CP2: the `+ str()` version gives
    identical output.
  - Hooks: WT: "the campaign uses `+` and `str()`, so read both".
- **8B-08 `whats-in-it-for-me` · What's in it for me?** · intro — · **Mk**
  - Task:
    - `lucky_reply(request)` returns the stripped, capitalized request plus `" What's in it for me?"`.
    - `clip(sentence)` returns Bomb Shell's version: the first three words, then a period.
  - CP1–2 [PAR, RET]. Any text passes.
  - Hooks: DF; BQ: `martu_reply` adds ", yes?".
- **8B-09 `broken-spell-8B` · Broken spell** · intro — · **D** · **SOLO**
  - Bugs:
    - `line.lower` with no `()` (prints `<built-in method…>`)
    - `line.lower()` that is never stored
    - `words.join(" ")`
    - an index past the end of a `split` result
  - CP1–4.

### Quiz 8B [C, 8 questions]

**Samples:**
1. **predict.** `"WHAT IS THE DECAY?".lower().capitalize()` → `What is the decay?`
2. **predict.** `" ".join(["Shield", "up."])` and `"gold,teal".split(",")` → `Shield up.` and
   `['gold', 'teal']`
3. **predict.** `"EXIT".find("Z")` → `-1`

**Other questions:**
- bug: `words.join(" ")`
- mc: an f-string versus its `+ str()` twin
- predict: strip and replace
- fill `.___()` → `capitalize`
- bug: a forgotten reassignment

### Project 8P1 "The Water-Stained Log" [O, recommended, 40 min]

**Premise.** Lucky copied the chalk wall onto paper in the rain:
`" 48 hrs| 48 hrs |47 hrs|46hrs | 44 hrs|41 hrs | 37hrs "`.
Mar'tu needs clean numbers. Lucky: "You're welcome."

**Tasks:**
1. `split("|")`.
2. `strip` and `replace("hrs", "")` on each mark, then `int()`.
3. Build a list.
4. Total it and compute the gaps.
5. `join` a clean `48, 48, 47, …` line.
6. Write an f-string summary.

**Checks:** [CMB] reruns with other messy strings.

**Stretch:** skip a smudged mark like `"4?"` (`if`, or `continue` from 5C).

**Consolidates:** 8A–8B and Unit 5.

### Project 8P2 "The Institute Cipher" [O, off-platform option, 60 min]

**Premise.** Mar'tu's old Institute notes are written in "ley shift": every letter moved forward by the hour shown
on the Ley Clock.

**Tasks:**
1. `shift_letter(letter, key)` uses `alphabet.find` and `% 26`, and leaves non-letters as they are.
2. `encode(message, key)` and `decode(message, key)`.
3. Decode Mar'tu's note.
4. Write your own coded note for a classmate.

**Prerequisite:** the Clock Math article (1-A2, `%`).

**Stretch:** a keyword shift that changes per letter.

**Off-platform:** students may run it in IDLE or another local Python if the teacher wants. It runs fully in
the browser too.

### Quick Check 8

1. **Code:** `tidy_line` chained.
2. **Code:** split, then join.
3. predict an index and a slice.
4. **Code:** `make_bar` with `(max - cur)` and `str()`.

**Skills:** `string-index-slice`, `string-methods`, `chain-methods`, `split-join`, `fstring-read`.

### Cheatsheet 8

`s[0]`, `s[-1]`, `s[2:5]`, `len(s)` · strings can't change in place: `"C" + s[1:]` · `"red" in s` ·
`for ch in s:` · `\" \n \t` · methods return a new string, so `s = s.lower()` · `.lower().capitalize()` ·
`.split()` / `" ".join(list)` · `.strip()`, `.replace(a, b)`, `.find(x)` → -1 · `int("48")` ·
`f"{name}: {mana}"` equals `name + ": " + str(mana)`.

---

## Unit 9 · Campaign Readiness Check: "Before We Continue" [C, 1 period + review]

**Mar'tu:** "You have learned enough to help, yes? Show me without the hints. Then we continue."

Full specification in section 5.

---

# 4. Concept introduction map

Generated by `design/curriculum_v1_gate.py`, which runs the harness tokenizer over representative code for all
166 coded items. **Core path: 0 violations. Full path: 0 violations.**

The planned per-unit token lists are in `design/concept_map.json`, in the harness's planned-units format. Copy it
into `docs/intro-to-python/prototypes/` in the prototype phase, so `harness.py u04` can gate a unit before the
earlier units exist.

The "first on core path" column is where a student who skips every optional item first meets the token. A token
marked *optional only* never appears in core code.

| Token | First on core path | First on full path (if earlier) | Concept |
|---|---|---|---|
| `call:print` | 1A-01 | 1W-01 (O) | print |
| `const:str` | 1A-01 | 1W-01 (O) | text in quotes |
| `const:multiline_str` | 1A-07 | | `"""…"""` |
| `node:Assign` | 1B-01 | | `name = value` |
| `const:int` | 1B-03 | | whole numbers |
| `op:Add` `op:Sub` `op:Mult` `op:Div` | 1C-01 | | arithmetic. `op:Mult` on text (`"█" * n`) is taught at 1C-08 |
| `node:AugAssign` | 1C-05 | | `+=` `-=` |
| `call:str` | 1C-06 | | `str()` before `+` |
| `op:Pow` `op:Mod` `op:FloorDiv` | *optional only* | 1-A2 (O) | Clock Math |
| `call:input` | *optional only* | 1-A3 (O) | `input()` |
| `call:int` | 8B-03 | 1-A3 (O) | `int("48")` |
| `const:bool` `op:Gt` `op:Lt` | 2A-01 | | True/False, `>` `<` |
| `op:Eq` `op:NotEq` | 2A-02 | | `==` `!=` |
| `op:GtE` `op:LtE` | 2A-03 | | boundaries |
| `attr:lower` | 2A-04 | | case-safe compare (D3) |
| `node:If` | 2B-01 | | if / elif / else (`elif` and `else` have no tokens) |
| `op:And` `op:Or` `op:Not` | 2B-06 | | logic |
| `node:Import` `import:random` `attr:randint` | 2B-07 | | dice |
| `node:Match` | *optional only* | 2-A1 (O) | match/case |
| `node:List` | 3A-02 | | lists |
| `node:Subscript` | 3A-03 | | `x[0]`, later `d["k"]` |
| `op:USub` | 3A-04 | | `[-1]`, later `-1` from `.find` |
| `attr:append` | 3A-05 | | `.append` |
| `call:len` | 3A-06 | | `len` |
| `call:range` `call:list` | 3B-01 | | ranges |
| `node:Slice` | 3B-02 | | slices |
| `call:sorted` `attr:sort` | 3B-03 | | sorting, `None` |
| `attr:count` | 3B-04 | | `.count` |
| `attr:insert` `attr:pop` | *optional only* | 3C-01 (O) | |
| `attr:remove` | *optional only* | 3C-02 (O) | |
| `op:In` | 4A-06 | 3C-02 (O) | membership |
| `call:max` `call:min` `call:sum` | *optional only* | 3C-03 (O) | |
| `node:Tuple` | *optional only* | 3-A1 (O); also 5-A1, 6-A3 | tuples, multiple returns |
| `call:zip` | *optional only* | 3-A2 (O) | |
| `node:Dict` | 4A-02 | | dictionaries |
| `op:NotIn` | 4A-06 | | `not in` |
| `attr:get` | *optional only* | 4-A1 (O) | |
| `node:For` | 5A-01 | | for loops |
| `node:While` | 5B-01 | | while |
| `node:Break` | 5B-03 | | break |
| `node:Continue` `node:ListComp` `node:IfExp` | *optional only* | 5C-01 / 5C-03 / 5C-04 (O) | |
| `attr:items` `attr:keys` `attr:values` | *optional only* | 5-A1 (O) | |
| `node:FunctionDef` | 6A-01 | | def |
| `node:Pass` | 6A-03 | | pass |
| `node:Return` | 6A-06 | | return |
| `node:DefaultArg` `node:KeywordArg` | 6B-08 | | defaults and keywords |
| `const:None` | 6C-04 (starter placeholder, as in the campaign) | | the literal `None` |
| `node:Lambda` | *optional only* | 6-A1 (O) | |
| `call:map` | *optional only* | 6-A2 (O) | |
| `node:Assert` | *optional only* | T-Own (O) | writing checks |
| `const:escape` | 8A-06 | | `\" \n \t` |
| `attr:upper` `attr:title` `attr:capitalize` | 8B-01 (fast lane: 8B-02 adds `attr:capitalize`) | | case methods |
| `attr:split` | 8B-03 | | split |
| `attr:join` | 8B-04 | | join |
| `attr:strip` `attr:replace` | 8B-05 | | clean-up |
| `attr:find` | 8B-06 | | find |
| `node:FString` | 8B-07 | | f-strings |

**Never introduced (out of scope, and the gate keeps them out):** `node:Set`, `node:DictComp`, `node:Try`,
`node:Global`, `node:Starred`, `node:With`, `node:Class`, `op:Is`, `op:IsNot`.

**Campaign idioms that have no token.** The harness tokenizer can't see these patterns, so they are gated by
lesson order and skill tags. Harness v2 could add pseudo-tokens for them so the gate enforces them too.

| Idiom (skill tag) | First taught | Proposed pseudo-token |
|---|---|---|
| String repetition `"█" * n` (`repeat-string`) | 1C-08 | `pattern:StrRepeat` (a `Mult` with a `str` operand) |
| Nested subscript `a["x"]["y"]` / `a[3][1]` (`dict-nested`, `list-nested`) | 3A-09 (list), 4B-01 (dict) | `pattern:NestedSubscript` |
| List of dicts (`list-of-dicts`) | 4B-03 | — |
| Store-then-pass (`store-then-pass`) | 6A-06 / 6A-08 | — |
| Return a comparison (`return-comparison`) | 6A-09 | `pattern:ReturnCompare` |
| Early `return` guard (`early-return`) | 6B-05 | `pattern:EarlyReturn` (a `Return` inside an `If`, with statements after the `If`) |
| Function as a value, passed without `()` (`func-as-value`) | 6C-01 / 6C-02 | `pattern:FuncValue` (the name of a user `def` used outside a call) |
| Calling a stored function `d["k"](x)` (`call-stored-func`) | 6C-03 | `pattern:CallOnSubscript` |

---

# 5. Campaign Readiness Check (operationalizing "arriving in the ZPD")

**Definition being measured** (research §4.1). A student is ready when they can:
- **read and explain every line** of a campaign part's starter code,
- **write the one-line edits unaided**, and
- **complete a whole part using only the campaign's built-in support**,

with the multi-concept composition in `hold-the-barrier` as a real but winnable stretch.

**Format.**
- **Part 1 (unaided).** 12 short items, about 25 minutes. No hints, tracer, another-way or Assemble-it. Code
  answers are **typed**. Every item uses our-world analogs, never the campaign's exact code.
- **Part 2 (supported).** A mini-boss with campaign-level support (numbered steps, check messages, the error
  explainer), with hints capped at level 2 and no reveal. About 15 minutes.
- There are three parallel forms (A, B, C), so a retake never repeats an item.

## 5.1 Part 1 items

| # | Item (our world) | Type | Skill tag | Prepares campaign part |
|---|---|---|---|---|
| 1 | Predict `print("Mana: " + str(7) + "/" + str(10))` → `Mana: 7/10`. | predict | `concat-str` | `mana-bars` return line |
| 2 | Replace `pass` in `def step_west():` with a helper call that takes a string (`scout.step("west")`). | code | `replace-pass` | `program-movement` |
| 3 | Finish `present_warning()`: store what `get_warning()` returns, then pass it to `show_on_ley_board()`. | code | `store-then-pass` | `program-dialogue-prompt`, `show_mana` |
| 4 | `latch_check(roll)` has `needed = 11` and `return roll >= needed`. Predict True/False for rolls 10, 11 and 12. | predict | `boundary`, `return-comparison` | `skill-checks` |
| 5 | Trace a three-branch `if/elif/else` on `choice == "option 2"` and say which line runs. Then fix an unquoted `option 3`. | predict + bug | `elif-chain`, `quote-text` | `program-dialogue-options` |
| 6 | Given a hero sheet: (a) read `hero["mana"]`; (b) read `hero["abilities"]["wisdom"]`; (c) write `book[spell_name] = spell`; (d) True/False for `"Glow" in book`. | 4-part code/predict | `dict-read`, `dict-nested`, `dict-write`, `dict-in` | `spell-book`, `hold-the-barrier` |
| 7 | Predict `"█" * 3 + "░" * 2`. Fix `"░" * 10 - 3`. | predict + bug | `repeat-string` | `mana-bars` |
| 8 | Which values can `random.randint(1, 6)` return? Then write `roll_die(die_size)`. | mc + code | `randint`, `param-use` | `skill-checks` |
| 9 | **Explain:** what is the difference between `spells["glow"]` and `spells["glow"](hero)`? (Choose the right plain-English sentence, then predict the output.) | explain + predict | `func-as-value`, `call-stored-func` | `spell-book`, `hold-the-barrier` |
| 10 | Trace `for hero in roster: show_status(hero)` over 3 hero dicts: how many calls, and with what? **Explain** in one sentence what the loop does. | trace + explain | `list-of-dicts`, `for-each` | bottom loops of `spell-book` and `mana-bars` |
| 11 | Read three tracebacks (`KeyError: 'dexterity'`, `TypeError: can only concatenate str (not "int")`, `NameError: name 'mana_cots'`) and fix each one-line bug. | bug ×3 | `read-traceback` | every part |
| 12 | Predict `hero["mana"]` after `hero["mana"] = hero["mana"] - 3`, starting from 20 → 17. | predict | `dict-write`, `reassign` | `hold-the-barrier` |

## 5.2 Part 2: the mini-boss "Hold the Lantern Ward"

`cast_ward(hero, ward_name)`, in our world. This is the near-transfer of `hold-the-barrier`, with different
names and data.

**Given:**
- the guard clause (`if ward_name not in hero["wards"]: …; return`),
- `ward = hero["wards"][ward_name]`,
- a finished `show_mana(hero)` helper,
- numbered comments in the campaign's style.

**The student writes the `if/elif/else`:**
- nested affinity check,
- `<` mana check,
- stored-effect call `ward["effect"](hero)`,
- subtraction,
- redraw.

**Six checks**, mirroring the campaign's:
1. skilled with enough mana casts,
2. the bar updates,
3. low affinity doesn't cast,
4. low mana doesn't cast,
5. exactly enough mana still casts,
6. the ward's own cost is used.

**Assemble-it is not offered** (typed). The tracer is allowed.

## 5.3 Pass heuristic (tunable, research §4.5)

| Result (neutral names) | Rule | What happens |
|---|---|---|
| **Ready** | Part 1 ≥ 10/12 (≥ 80%), with item 6 at ≥ 3 of 4 parts. **And** the mini-boss passes all 6 checks using hints of level ≤ 2 and no reveal. | Milestone "Ready for Module 2". Each skill shown solid on the map. |
| **Ready, with a review list** | Part 1 is 8–9/12, **or** the mini-boss needed one level-3 hint. | Go on to the campaign with "Mar'tu's notes": a short list of the missed skills. Each links to its review lesson and one parallel practice item. The teacher sees the flags. |
| **Review first** | Part 1 ≤ 7/12, **or** the mini-boss needed a reveal. | Targeted review for each missed skill in a **different representation** (Parsons, the tracer ledger, a worked example), then parallel items from another form. After two review cycles the student continues anyway, with a teacher flag (no wheel-spinning, research P14). The story never blocks. |

**Per-part readiness.** The item-to-part column in 5.1 gives the teacher a per-campaign-part readiness view,
matching research §4.4:
- **Band A (unaided)** expected for `program-movement`, `program-dialogue-prompt` and `skill-checks`.
- **Band B (with built-in support)** for `spell-book`, `mana-bars` and `hold-the-barrier`.

**Spaced re-check.**
- Six parallel items (from the student's misses, plus items 4, 6 and 9 for everyone), run right before Module 2,
  or about a week after the first check.
- Tested-out skills are re-verified here too, so a Quick Check pass never stands unverified.

**Confirmed in the campaign itself.** The ZPD target is met when campaign telemetry shows, per part:
- 2–6 runs, with different errors and recovery,
- mostly level 1–2 hints,
- at most 1 Show solution per module,
- and the student can explain a line they wrote.

Signals in the red (8 or more runs; the same error 3 or more times; reveals on most parts) mean the course
under-prepared that skill. Signals in the blue (1 run on every part; no hints ever) mean the campaign sits below
the zone for that student, so offer the instructions-light toggle (research §4.2 note).

---

# 6. Pacing (≈ 45–50 min periods, about 40 working minutes each)

Minutes are for a typical student. G1 takes about 1.3–1.4×. G4 takes about 0.6× and can test out of Units 1–3
in about 30 minutes total.

| Unit | Core items | Core min | **Core periods** | Optional items | Optional periods |
|---|---|---|---|---|---|
| 1 Hello World | 1-A1, 1A, 1B, 1C, Quiz 1, 1P1 | ~146 | **3.5** | 1W, 1-A2, 1-A3, 1P2, QC1 | 1.8 |
| 2 Control Flow | 2A, 2B, Quiz 2, 2P1, 2C | ~147 | **3.5** | 2-A1, 2P2, QC2 | 1.4 |
| 3 Lists | 3A, Quiz 3A, 3P1, 3B | ~92 | **2.5** | 3C, Quiz 3B, 3-A1, 3-A2, 3P2, QC3 | 2.1 |
| 4 Dictionaries | 4A, 4B, Quiz 4, 4P | ~118 | **3** | 4-A1, QC4 | 0.5 |
| 5 Loops | 5A, 5B, Quiz 5, 5P | ~104 | **2.5** | 5C, 5-A1, QC5 | 1 |
| 6 Functions | 6A, Quiz 6A, 6B, 6C, Quiz 6B, 6P | ~199 | **5** | 6-A1, 6-A2, 6-A3, QC6 | 1 |
| 7 Code Challenges | — | — | — | 16 core challenges (~10 min each) + 16 advanced variants | 4–8 |
| 8 Strings | 8A, Quiz 8A, 8B, Quiz 8B | ~85 | **2** | 8P1, 8P2, QC8 | 2.8 |
| 9 Readiness Check | Parts 1–2, plus review routing | ~60 | **1.5** | spaced re-check (~15 min) | 0.4 |
| **Total** | 17 lessons, 130 exercises, 9 quizzes, 6 projects, 1 check | ~950 | **≈ 23.5 periods** (about 5 weeks of daily classes) | 3 lessons, 10 articles, 5 projects, Trials, 7 Quick Checks | **≈ 15–19** |

These include warm-ups (about 3 minutes per lesson) and one Run-feedback loop per exercise at about 3.5 minutes
on average:
- predict/run items take about 2 minutes,
- debug items about 4,
- make items about 6.

**Item mix compared with the syllabus** (14 lessons, 14 projects, 13 quizzes):

| | Lessons | Projects | Quizzes | Articles | Other |
|---|---|---|---|---|---|
| This course | 20 (17 core) | 11 (6 core) | 10 (9 core) | 11 (1 core) | 7 Quick Checks, 7 cheatsheets, 32 challenge variants, 1 Readiness Check |

**Lean core (≈ 18 periods), if time is short.** Trim these, in this order. None of them cuts a campaign-critical
skill.
1. 3P1 becomes optional (−25 min).
2. 2C keeps only 2C-01, 2C-05 and 2C-06 (−15).
3. 3B keeps only 3B-01 and 3B-03 (−8).
4. Quiz 3A and Quiz 8A fold into the next lesson's warm-ups (−14).
5. 1C-05 and 6B-08/09 become optional (−15).
6. 5B keeps 5B-01 to 5B-03 (−12).
7. 8A keeps 8A-01, 8A-03, 8A-07 and 8A-08 (−12).
8. Projects 1P1, 2P1, 4P, 5P and 6P drop their last task group (−20 each, −100 total).
9. Quizzes 6A and 6B merge into one 12-question quiz (−8).

That totals about 210 minutes, roughly 5–5.5 periods. **Below about 18 periods**, don't cut further. Interleave
instead: use the fast lane (Units 1, 2, 6A and 8B-02, about 9 periods) and send students into Module 1, then
finish Units 3–9 before Module 2.

**Suggested calendar (core, daily classes).**

| Week | Units |
|---|---|
| 1 | Unit 1, start of Unit 2 |
| 2 | Unit 2, Unit 3 |
| 3 | Unit 4, Unit 5 |
| 4 | Unit 6 |
| 5 | Unit 6 project, Unit 8, Readiness Check |

Trials and optional items run alongside, for students who finish early or test out. They never block anyone.

---

# 7. Open questions for the teacher

1. **Where does the course sit in the campaign?**
   - Default assumption: the whole core runs before campaign Module 2's coding parts.
   - If Module 1's coding hasn't started yet, should we enable the **Module 1 fast lane** (Units 1–2, Lesson 6A
     and 8B-02, about 9 periods)?
   - If Module 1 is already done, should the course skip its rehearsals or keep them as review?
2. **Approve or adjust the deviations D1–D10** (§1.4), especially:
   - D1, the placement of Dictionaries after Lists rather than after Functions;
   - D3, `.lower()` in Control Flow;
   - D4, `"█" * n` in Unit 1.
3. **How many class periods are available?**
   - The core is about 23.5 periods and the lean core about 18.
   - If you add any optional item back, we recommend Project 8P1 (Water-Stained Log) and the Ward Sign (1P2,
     engaging for G1).
4. **Spoilers and foreshadowing.**
   - Things the course shows early: Bomb Shell and Lucky (they arrive in Module 2), the chalk-wall numbers (a
     Module 2 beat), and the 5B-04 forecast, which produces 32 hours with the default (Module 2's last line).
   - Things it avoids: `Strengthen Magic`, the red clock event, and the campaign's function names.
   - Is that acceptable, or should Units 1–5 use only Oogrish and Gearshift until Module 2 is played?
5. **Reading level.** Is grade 6–7 the right target for Mar'tu's text and checkpoints? Is Mar'tu's accent at
   the right intensity (one ", yes?" per screen, no misspellings)?
6. **Pair mode.** Should it be on by default for known pairs (e.g., the A-03/A-04 and B-02/B-03 pairs the
   sheets suggest)? Should solo "Show Mar'tu" checkpoints be required to complete a lesson, or only recorded?
7. **Quick Check rules.**
   - Proposed pass rule: every code task plus 80% of the questions.
   - Should "Tested out" count as complete in your report?
   - Retakes: unlimited (proposed), or one per day?
   - Should placement presets be set from the paper diagnostic? We'd treat them as provisional and confirm with
     Quick Check 1, because of the help caveats.
8. **Productive-failure hooks** (3A-01 "How would you store it?", 4A-01 "Which number is which?"). These are
   ungraded, at most 3 minutes, and skipped for students showing frustration signals. Do you want them?
9. **Readiness Check stakes.** We recommend practice only, with results visible to the student and you, and
   never a grade, because answers are visible in a static site's source. Do you agree with the pass heuristic in
   §5.3?
10. **Project and unit names.** Are "Night Watch Ledger", "Road Encounter Table", "Ledger of Heroes",
    "Velocite Watch", "Resonance Array", "Water-Stained Log", "Institute Cipher" and "Trials of the Yard" (run
    by Oogrish) acceptable in your world? Can Mar'tu reference their Institute past this freely?
11. **Engineering approvals.**
    - The new check helpers: `_rerun`, `_calls`, `_func_ast`, `_near_names`.
    - The proposed no-token pseudo-tokens (§4).
    - The core-only gate rule.
    - Using `roster` (never `party`) for the course's list of heroes.
12. **f-strings.** The campaign uses `+` and `str()`. Is teaching f-strings as "read both, write either" (8B-07)
    the right weight, or should they be optional?
13. **Cameos and Calm mode.** Should Calm mode (no cameo lines) be off by default for everyone, or on under the
    "Keep it short" preset?
14. **The off-platform cipher option.** Do students have a local Python (IDLE) available, or should 8P2 stay
    browser-only?

