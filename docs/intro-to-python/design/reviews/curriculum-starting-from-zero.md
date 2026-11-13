# Curriculum v1 review: "Starting from zero" (A-02, A-03, A-04)

**Reviewer role:** student representative for group 1 (`starting-from-zero`).
**Read:** personas.md (group 1 and class-wide patterns), A-verified.json (A-02, A-03, A-04), brief.md,
campaign-python-inventory.md, curriculum-v1.md (all of it), the current `src/lib/languages/python/explain.ts`.
**Verified:** every Python error quoted below was produced by running our sheets' exact lines in CPython 3.13.18.

---

## 0. Who I speak for (the evidence I'm holding the draft to)

None of us wrote a working variable. These are the exact things on our sheets that the course has to catch:

| Slip | Sheet | What Python actually does with it (3.13) |
|---|---|---|
| `def ("character")` | A-02 | `SyntaxError: invalid syntax` |
| `def: Power_up= ("Fire Ball` | A-02 | `unterminated string literal` first. Once the quote is closed: `invalid syntax` (the line starts `def:`, not `def (`) |
| `("Fire Ball` (no closing quote **or** paren) | A-02 | `unterminated string literal`, then `'(' was never closed` after the quote is fixed |
| `total_cost = 5P + 2S` | A-02 | `SyntaxError: invalid decimal literal` |
| `Health = 100` when the task wants `health` | A-02 | `NameError` on later use |
| `canes_women` alone on a line | A-03 | `NameError: name 'canes_women' is not defined`, on a line with **no** `=` and **no** `print(` |
| `"chick-fa-le_women"` alone on a line | A-04 | **No error at all.** Python runs it and nothing happens |
| `chicken_sandwich - "Fireball` | A-04 | `unterminated string literal` first, then `NameError` once the quote is closed. Two errors back to back |
| 180 pizzas, 1000 sodas, `* 0`, `return 35` | A-03, A-04 | No error. Only a check can catch it |
| Trace: `10 + 5 = 15`, bonus line from `gold_value`/`silver_value`, "printed" 55 / 45 | A-03, A-04 | (paper) adding the code's constants, losing the return value, `print` = sum of everything so far |

Our arithmetic is fine (3 x 10, 4 x 5 on all three sheets). What we're missing is what the code *means*.

---

## 1. Verdict

**It's closer to working for us than anything we've had, but as written, the supports we need most might never
switch on, and three of our core mistakes still get through.**

The draft clearly read our sheets. 1A-03, 1B-02, 1B-05, 1B-06, 1C-02, 6A-01 and 6A-06 each name one of our
slips and have a check or explainer row for it. The hint ladder with a your-turn variant, "a reveal never counts
toward mastery", accepting any quoted value, no timers, and Mar'tu never saying "Wrong" are all what we asked for.

Where it breaks for us:
1. **Ordering bug:** the "Have you typed code before?" question that sets the preset is asked in **1A**, but
   the warm-ups (1W) come **before** 1A and are "default-on only under Show me more". No default preset is
   named. So we may skip the warm-ups that were built for us.
2. **Our tracing mistakes only get passive help.** Adding the code's constants (`10 + 5`), using `gold_value`
   instead of the return, and "print adds up everything" appear as catches in 1B-05 and 6A-06, but the fix is
   the tracer, which only displays. No exercise makes us *do* the trace, and nothing asks us to trace a function
   that has constants inside, the exact thing we got wrong.
3. **Explainer gaps on our exact lines:** `5P + 2S`, a lone `canes_women`, a lone `"chick-fa-le_women"` (no error
   at all), `def:`, `'(' was never closed`, and the two-errors-in-a-row case. The current `explain.ts` titles
   ("Syntax error", "Unknown name") and its fallback hint ("Python could not read this code: unterminated string
   literal (detected at line 1)") are jargon.
4. **"Another way" isn't always another way.** Several core concepts list only `shorter` or `from the campaign`
   as angles (1A-06, 1C-01, 1C-05, 2A-04, 6A-10), and reassignment (1C-04) has only a trace table. For us,
   "shorter" is the same thing again, more compressed, and "from the campaign" is *more* unfamiliar code.
5. **A rule silently flips.** Unit 1 drills "the name never goes in quotes" (built for A-02). Then 4A-02 puts
   dictionary keys in quotes with no "wait, why?" moment.
6. **Some steps are too big for us:** 1C-07 (four boxes plus a two-`str()` line, all before anything shows), the
   1C-08 Make step (and we can't even type `█` on a Chromebook), Project 1P1 under "light" support, Project 4P
   (four nested sheets), and 4–5-bug SOLO checkpoints (2B-09, 6A-11).
7. **Pacing.** At 1.4×, the 23.5-period core is about 33 periods for us. The week-by-week calendar in §6 means we
   fall visibly behind by week 2.

If the "must" items below are fixed, I think it works for A-02. For A-03 and A-04 it also depends on pair mode
with short solo checkpoints and real places to be funny. That's how we find out what each of them can do alone.

---

## 2. Walking through it as us

### Course map and Unit 1 opening
- **Opening scene:** good. Short lines, Lucky's "Existing." will land. The buttons are fine, but if A-03/A-04
  click "Where should I start? (Quick Checks)" as a joke, the first thing they get is a test with no hints. That's
  OK only if failing it really costs nothing and quietly turns on "Show me more" (the draft says the result sets
  the support defaults, which is right).
- **1-A1 "How Mar'tu Teaches" [C, 5 min]:** nine features on one screen before we've pressed Run once. We read
  fast, hunting for code. We will scroll past it and not remember the hint button exists. This breaks "a win in
  the first two minutes". Teach each feature the first time we need it instead (the hint button appears with a
  coach mark on our first failed check, and so on).
- **1W:** exactly what we asked for. But see the ordering bug above. 1W-02's line "red text means Python needs
  help reading this" is great. Make the panel itself not red, too.

### 1A "Words in Quotes"
- **1A-01:** a win in under a minute. Keep it.
- **1A-02:** Mar'tu echoing our line deadpan is the best thing in Unit 1 for A-03/A-04. This is where they get to be
  funny on purpose.
- **1A-03 `close-the-quote`:** right target (all three of us left quotes open). But A-02's `("Fire Ball` is missing
  the `)` too. After the quote is fixed, Python says `'(' was never closed`, a *second* error. To us that feels like
  "I made it worse." Teach "quotes **and** parentheses come in pairs" here, and add that explainer row.
- **1A-04 `words-need-quotes`:** the explainer says "Python looked for a **box** called Fireball", but boxes don't
  exist until 1B. Either don't say "box" yet, or define it in the same sentence.
- **1A-07 triple quotes:** another quote form right after we just learned "quotes come in pairs." Not used in the
  campaign. Let us defer it (see pacing).
- **1A-08 SOLO:** good bugs (capital `P`, open quote, unquoted word), one tick per fix. As a solo for A-03/A-04,
  three bugs is about the limit.

### 1B "Boxes With Labels": the lesson that decides whether we make it
- **1B-01:** `print(companion)` next to `print("companion")` is exactly the contrast A-02 needs. But the *anatomy* of
  the line should be on screen by default, not hidden behind "another way": a labeled picture of
  `character = "Zelda"` with **label (no quotes) | `=` "gets" | value (quotes because it's text)**.
- **1B-02:** accepting any quoted value plus Mar'tu reacting ("*Kratos.* Hm.") is the delight we asked for.
  Problems:
  - The catches list says "A-04 `character - "Zelda"`". A-04 didn't write that. A-04's item 1 was a lone
    `"chick-fa-le_women"`, which **raises no error**, and A-03's was a lone `canes_women`, which raises a
    NameError the §2.4 rows don't cover (those rows need `=` or `print(` on the line). Both need their own message
    (see §4).
  - Add the CP2 message for `print("character")` specifically: "That prints the word *character*. Take the quotes
    off so Python opens the box." That's A-02's name-in-quotes habit, showing up in the print line.
  - Parsons distractors: add `character - "Zelda"` and a lone `"Zelda"` (our actual forms) next to `def ("character")`
    and `"character" = "Zelda"`.
- **1B-05 `change-the-box`:** tracer open by default, aimed at our "print shows everything" belief. Good.
- **1B-06:** these are our exact slips. Add `def companion = "Gearshift"` as a fifth line. Right now the
  deliberate `def`-vs-`=` exercise is 2C-06, at the end of Unit 2 (about period 7). Until then A-02 relies on the
  explainer every time the belief fires. Quiz 1 Q1 already shows `def ("hero")`, so this doesn't introduce
  anything new.

### 1C "Math and Glue"
- **1C-01:** arithmetic as the confidence bridge is right. We're good at this part.
- **1C-02 `what-each-number-means`:** the `# how many?` / `# how much is one?` comments are aimed straight at A-02's
  5s and A-03/A-04's 180/1000. But A-03/A-04 *will* type 1000 again, for the laugh. Don't fight it. Give the joke a
  job (next point).
- **1C-03 `let-the-code-combine`:** the hint ladder and your-turn variant are great. Add an Investigate step:
  **"Lucky orders 1000 coils of rope. Change `rope_count` to 1000 and Run. What happened to `total_cost`?"** That
  turns A-03/A-04's 1000-sodas joke into the "let the code combine it" lesson itself. Also: A-02 will write
  `5 * lantern_count + 2 * rope_count` or even `3L + 5R`. The second one is `invalid decimal literal`, and nothing
  in §2.4 explains it.
- **1C-04 `spend-mana`:** `mana = mana - spell_cost` is the hardest line in Unit 1 for us (the same name on both
  sides). The only listed angle is a trace table. We need "Python works out the right side first, using what's in
  the box *now*, then puts the answer back in", plus a picture (take out, subtract, put back) and read-aloud that
  says "mana **gets** mana minus spell cost."
- **1C-05 `+=`:** a second way to write what we just barely learned. The campaign uses the long form
  (`caster["mana"] = caster["mana"] - spell["mana_cost"]`). Let us defer this and accept both forms in later checks.
- **1C-06 `glue-words`:** we'll write `"Lucky has" + str(mana) + "mana."` and get `Lucky has26mana.` The OUT check
  then says it's wrong, and we can't see why. Show the expected and actual lines aligned, with the first difference
  marked: "spaces count."
- **1C-07 `status-line`:** five actions before anything shows. Split it (§3, R13).
- **1C-08 `repeat-a-mark`:** two problems. (1) We just learned `"Mana: " + 26` is an error, and now `"█" * 3` works.
  Say why in plain words ("`*` with text means *stamp it this many times*. `+` means *glue*, and you can only glue
  text to text"). (2) **There is no `█` or `░` key on a Chromebook.** The campaign's own starter pre-types
  `"█" * 0`. The course should too (`full = "█"`, `empty = "░"`), or offer a symbol tray. Otherwise the whole
  exercise is about typing, not thinking.
- **1C-09:** "the output looks right but the rerun check fails" will feel like a trick unless the message
  shows the rerun happening ("I changed `lantern_count` to 7 and ran it again. `total_cost` still said 22."). The
  CMB wording in §2.3 does that. Keep it exactly that concrete.

### Quiz 1 and Project 1P1
- **Quiz 1** is aimed at our slips (`def ("hero")`, `hero - "Lucky"`). "Show choices" for predict questions helps.
  Seeing "4/10" before anything else is the moment we decide we're bad at this. Under "Show me more", list what we
  got right first, then "worth another look", then the number.
- **1P1 "Night Watch Ledger":** a fun premise (glug as "medical" will get a laugh), and "any number" for `glug_sips`
  is a legitimate joke slot. But it's 8 tasks in one editor under **light** support (hints only after a failed run),
  three lessons into our coding lives. If the starter is blank, A-03/A-04 will goof and A-02 will freeze. Under
  "Show me more": a comment skeleton with the A/B/C headings and `= 0` placeholders, and the full hint ladder.

### Unit 2 Control Flow
- **2A-02:** `clock_is_red = clock_color == "red"` is the first line with both `=` and `==`, for students who just
  got `=` to stick. Write the first one as `clock_is_red = (clock_color == "red")`, read aloud as "clock_is_red
  **gets** the answer to: is clock_color the same as red?", then drop the parentheses in 2A-03.
- **2A-04:** first dot-method (`answer.lower()`). One plain sentence: "the dot means *ask this text to do something*."
- **2B-09 SOLO (5 bugs)** and **6A-11 SOLO (5 bugs):** too long for a solo. When A-03/A-04 get stuck alone, they
  go back to goofing. Make the solo **one** short item; the rest of the broken spell can be done in pairs.
- **2C "Reading Errors" at the end of Unit 2:** we start making errors in minute one. Give us a two-step version
  of the routine in 1W-02/1A-03 ("Read the last line. Go to that line number."), and expand it in 2C-07.

### Units 3–5
- **3A-01 productive failure:** a blank-ish editor and "try anything" is exactly what we freeze on. Pre-type
  `hour_1 = 48` so we continue a pattern.
- **4A-02 `make-a-sheet`:** "keys are text, so they need quotes". After Unit 1 taught A-02 "the name of a box
  never goes in quotes", this needs a reconciliation card (§4.4). Otherwise it looks like the rules change whenever
  they feel like it.
- **4P "Ledger of Heroes":** four nested sheets is a lot of `{ } : , " "`. A missing comma in a multi-line dict is
  reported as `invalid syntax` on the **next** line (verified: comma missing on line 2, error on line 3). We'll stare
  at the wrong line. Pre-build two sheets under "Show me more", and add an explainer row for `invalid syntax` inside
  `{ }`.
- **5A-05 `the-gaps`:** `chalk_wall[i - 1] - chalk_wall[i]` is index arithmetic in a loop, which is hard for us. But
  Mar'tu's "Now you have seen it yourself" payoff is worth it. Keep it Predict/Investigate-heavy, with the tracer open.

### Unit 6 Functions (the cliff)
- **6A-01 `box-or-recipe`:** exactly the `=` versus `def` contrast A-02 needs. Keep it.
- **6A-04/6A-05:** our function mistake isn't G2's "test values". We wrote **unrelated** numbers (`100 * 5`,
  `30 * 0`, `50 * 0`) because we think a blank takes any number. The PAR check will catch it, but the message has
  to explain *why*: "A recipe doesn't know its numbers yet. It gets them when someone calls it." Show the call table
  in the message. A Mad Libs angle fits us: the card has blanks, and the player fills them in when they play. Add our
  sheet ids to the 6A-05 catches.
- **6A-06 `send-it-back`:** the return arrow landing in `lucky_max` is right. But we need to *do* the trace, not
  watch it. This is the missing exercise (§4.3).
- **6C (functions as values):** abstract for us. The "hand someone the card vs cook the meal and hand them the empty
  pot" analogy is good. Keep the Parsons fallback on 6C-04/6C-05.

### Readiness Check
- Practice-only, "the story never blocks", two review cycles then continue with a teacher flag. Good for us.
  Clarify that **glossary hovers and Read aloud stay on** in Part 1. They're accessibility, not hints.

---

## 3. Requested changes

| # | Where | Change | Why (our evidence) | Priority |
|---|---|---|---|---|
| R1 | site feature (course map, 1A) | Ask "Have you typed code before?" on the **first course-map visit**, before 1-A1 and 1W. If unanswered, default to "Show me more". Let the teacher pre-set it provisionally from the diagnostic (answers Q7). | 1W comes before 1A, where the question is now, so A-02/A-03/A-04 could skip the warm-ups built for them. No default preset is named. | must |
| R2 | 1-A1 | Replace the 9-feature screen with just-in-time coach marks (the hint button explained on the first failed check, Another way on the first auto-offer, etc.). Keep a ≤ 60-word, 3-picture version for the course map. | "Walls of text", "a win in the first two minutes". We read fast, hunting for code. | must |
| R3 | §2.4 explainer + `explain.ts` | Add rows: `invalid decimal literal`; a NameError on a line that is only a bare name; `'(' was never closed`; any `def` line that isn't `def name(...):` (including `def:`); `invalid syntax` inside `{ }` (missing comma on the line above). Show "One fixed. Python found the next one." when a new error follows a fix. Replace jargon titles ("Syntax error", "Unknown name") with plain ones ("Python couldn't read line 3"), with the error name in parentheses second. | A-02 `5P + 2S`, `def: Power_up=`, `("Fire Ball`; A-03 `canes_women`; A-04 `chicken_sandwich - "Fireball` (two errors back to back). The current fallback echoes "unterminated string literal (detected at line 1)". | must |
| R4 | §2.3 check library; 1B-02, 1B-03, 1B-06, QC1 | New **BARE** pattern: a top-level line that is only a value runs with **no error**, so a check must catch it. Message: "This line is a value with no box. Put `character = ` in front of it." Fix the 1B-02 citations (A-04 wrote a lone `"chick-fa-le_women"`, not `character - "Zelda"`; add A-03 `canes_women`). | A-04 item 1; B-02/B-03 have the same form. | must |
| R5 | Unit 6, new **6A-06b `be-the-ledger`** (+ Quiz 6A, Readiness Part 1) | An active trace of a recipe **with constants inside** (spec in §4.3). The student fills in each box's value line by line. Wrong answers 15, 30/20 on the bonus line, and 55/45 get targeted messages. | A-03/A-04 `10 + 5 = 15`, the bonus line from `gold_value`/`silver_value`, printed 55 and 45. A-07 (G2) "return = 3 + 4". The tracer is passive. | must |
| R6 | 4A-02, Cheatsheets 1 and 4 | Add a reconciliation card and a predict contrast: box names never have quotes (`mana = 26`). Dictionary keys are text, so they do (`{"mana": 26}`). | Unit 1 drilled "the name never goes in quotes" for A-02. 4A-02 reverses it without saying so. | must |
| R7 | §2.5 Another way; listed exercises | For our core concepts, at least three genuinely different angles each. Under "Show me more", order them picture → everyday → step-by-step → in Tor → shorter → from the campaign. Each failed check offers the **next unseen** angle. Specific angles are in §4.2. | "The same explanation said louder." 1A-06, 1C-01, 1C-05, 2A-04 list only `shorter`; 6A-10 only `from the campaign`; 1C-04 only a trace table. | must |
| R8 | 1C-08 and every bar task (1P2, 4P stretch, 5A-07, 6B-07 `▮▯`, 8A-07 `▓░`, Readiness item 7) | Pre-type the block characters in the starter (`full = "█"`, `empty = "░"`), or add a one-click symbol tray. | A Chromebook has no `█` key. The campaign starter already pre-types `"█" * 0`. | must |
| R9 | site feature (failed run) | **One help stack.** After a failed run, show one plain message (the explainer if it crashed, otherwise the check message) and **one** "Next step" button that steps through: hint rung → next another-way angle → Assemble it. Oogrish's 3-fail line and Mar'tu's proactive offer go inside that button instead of stacking. | As drafted, a failed run can show at once: the check message, the console explainer, Oogrish's line, Mar'tu's offer, an auto-offered angle and the hint button. That's a wall of text at our worst moment. | must |
| R10 | site feature (Read aloud, AW text) | Read `=` as "gets" (`character gets "Zelda"`, `mana gets mana minus spell_cost`) and `==` as "is the same as", in the `say` text and in the "picture" angles. | A-02 `5P + 2S` (`=` read as math equals). It also supports 1C-04 and 2A-02. | should |
| R11 | 2A-02 | First exposure: `clock_is_red = (clock_color == "red")`. Drop the parentheses in 2A-03. | The first line with both `=` and `==`, for students who just secured `=`. | should |
| R12 | §2.3 OUT pattern | On an exact-output mismatch, show both lines aligned with the first difference marked ("spaces count"). | 1C-06 (`Lucky has26mana.`), 1C-07, 2B-08, 2P1. "Strict checks… I'm bad at this." | should |
| R13 | 1C-07 | Split into 3 checkpoints (`max_mana` computed; `mana = max_mana`; the status line). Under "Show me more", give `print(hero_name + ": " + ___ + "/" + ___ + " mana")`. | "Five steps before anything happens." | should |
| R14 | 1C-02, 1C-03 | 1C-02 message for wild counts: "Lucky would like 1000 ropes. The list says 5. Use the story's numbers here. You get your 1000 next." 1C-03 Investigate/side quest: set `rope_count = 1000`, Run, and watch `total_cost` follow. | A-03/A-04's 180/1000 joke becomes the lesson on letting the code combine values. | should |
| R15 | 1B-06 | Add `def companion = "Gearshift"` as a bug (the DEF explainer fires, then the fix). 2C-06 stays as the review. | A-02's core belief. The persona need is "explicit `=` vs `def` contrast early". | should |
| R16 | 1A-03 / 1A-08 | Teach "quotes and parentheses come in pairs". Add `print("Shield up."` (closing paren missing) to 1A-08 or as an Investigate step in 1A-03. | A-02 `("Fire Ball` is missing both. | should |
| R17 | Projects 1P1, 2P1, 4P | Under "Show me more": a comment skeleton with the task-group headings and placeholders, and the full hint ladder instead of "light". In 4P, pre-build two of the four sheets. | Blank editor plus light support. 4P's missing-comma errors are reported on the next line. | should |
| R18 | all SOLO items (1A-08, 1B-06, 1C-09, 2A-05, 2B-09, 6A-11, …) | The solo is **one** short item (one bug or one line), recorded, never blocking (answers Q6). The other bugs can be done in pairs. | A-03/A-04: neither student's own level is visible. A 5-bug solo invites goofing; one clean item gives a real signal. | should |
| R19 | §6 pacing, site feature | Tag each core item **campaign-critical** or **syllabus-only**. Let a student on "Show me more" defer syllabus-only items (1A-07, 1C-05, 3A-08, 3B-02, 3B-04, 6B-08, 6B-09, 8A-06) and spend the time on extra twin practice for 1B, 1C and 6A. Visible to the teacher, never to peers. | At 1.4×, our core is about 33 periods against a 23.5-period calendar. "Comparison with faster classmates." | should |
| R20 | 6A-05 (and 6A-04) | PAR message for a constant result: "Your recipe printed 0 for both calls. A recipe gets its numbers when it is called: use `base_damage` and `bonus`." Show the call table inside the message. Add A-02/A-03/A-04 to the catches. | A-02 `100 * 5`, A-03 `30 * 0`, A-04 `50 * 0`: unrelated literals, not test values. | should |
| R21 | glossary (§2.5) | Add *defined / not defined*, *syntax*, *run*, *call*, *value*, *assign*, *indent*, *method*. | Every NameError says "not defined". We don't know what it means. | should |
| R22 | check messages, explainer (Units 1–2) | Use one term consistently: "box (variable)" in Units 1–2, then "variable". Right now the explainer says "box", CMB says "variables", and TEXT says "holds". | Mixed words for one idea read as different ideas to us. | should |
| R23 | 1A-04 explainer | Don't say "box" before 1B. Use: "Python thought `Fireball` was the name of something saved earlier (you'll make those next lesson) and found nothing. Words you want to show need quotes." | Jargon before the concept. | should |
| R24 | site feature (error panel) | A neutral, non-red "fizzle" panel style for the explainer. | "Red text that feels like blame." | should |
| R25 | Quick Checks, Readiness Part 1 | State that glossary hovers and Read aloud stay on. | Accessibility, not hints. A-02 reads slowly and carefully. | should |
| R26 | Quiz review (§2.2) | Under "Show me more": what you got right first, then "worth another look", then the score. | The score-first screen is where we decide we're bad at this. | nice |
| R27 | site feature | A pool of Mar'tu deadpan reactions for any typed text (1A-02, 1B-02, the 1P1 watch-keeper, 2P1 encounters), with a filter that falls back to a generic line for anything not classroom-safe. | "Mar'tu saying something silly because I typed it." | nice |
| R28 | "Show me more" preset definition | Make it mean more pictures, steps and angles, **not more words**. Keep the Learn pane to ≤ 60 words before the first action in 1A–1C, with the labeled-box picture shown by default in 1B. | We need more support and less reading. | nice |
| R29 | 3A-01 | Pre-type `hour_1 = 48` so the productive-failure hook isn't a blank editor. | "A blank editor." | nice |
| R30 | 1W-04 | Point out that `-`, `_` and `=` sit side by side on the keyboard and mean different things. | A-04 used `-` for `=`. | nice |
| R31 | "Mar'tu remembers…" | When a recall item is missed, show the answer with a one-line why and no red X. | Unscored, so don't let it feel like a quiz. | nice |

---

## 4. Exact text and specs for the musts

### 4.1 New explainer rows (all messages verified in CPython 3.13.18)

| Raw message / trigger | Our line | Plain title | What the explainer says |
|---|---|---|---|
| `SyntaxError: invalid decimal literal` | A-02 `total_cost = 5P + 2S` | Python couldn't read line N | "Python doesn't read `5P` as '5 times P'. Put `*` between a number and a box: `5 * pizzas`. Better still, use the boxes you already made: `pizza_cost + soda_cost`." |
| `NameError` where the whole line is a single name | A-03 `canes_women` | Python found a name it doesn't know | "This line is just a name by itself, so Python looked for a box called `canes_women` and found none. To make a box: `name = value`. To show words: `print("words")`." |
| *(no error)* a top-level line that is only a string or number (BARE check) | A-04 `"chick-fa-le_women"` | (check message) | "This line is a value with no box, so Python ran it and forgot it. Put `character = ` in front of it." |
| `SyntaxError: '(' was never closed` | A-02 `("Fire Ball` after the quote fix | A bracket is still open | "A `(` opened on line N and never closed. Brackets come in pairs too: add `)` at the end." |
| `SyntaxError` on any line starting `def` that isn't `def name(...):` (includes `def:` and `def (`) | A-02 `def: Power_up= ("Fire Ball")` | `def` is for recipes | "`def` makes a recipe (a function). To make a box (a variable), write `name = value`, with no `def`." |
| `invalid syntax` on a line inside `{ … }` | 4A-02, 4P | Python couldn't read line N | "Inside a dictionary, every line but the last ends with a comma. Check the end of the line **above** line N." |
| any error that appears right after the previous run's error was fixed | A-04 `chicken_sandwich - "Fireball` (unterminated, then NameError) | (prefix) | "One fixed. Python found the next one: …" |

### 4.2 Angles to add to "Explain it another way"

| Concept (exercise) | Angles to add |
|---|---|
| Making a box (1B-01, 1B-02) | **Everyday:** "Your phone's contacts: you tap the *name*, and the phone uses the number saved under it. `print(character)` taps the name." **Contrast gallery ("Not this"):** `def ("character")`, `"character" = "Zelda"`, `character - "Zelda"` and a lone `"Zelda"`, each with a one-line why (our sheets, anonymized). **Sentence frame:** `____ = ____`, "name (no quotes) gets value". |
| Reassigning (1C-04) | **Picture:** take the coins out of the jar, subtract 3, put the rest back. **Step-by-step:** "right side first, using what's in the box *now*". **Read aloud:** "mana gets mana minus spell cost". |
| Let the code combine (1C-03) | **Everyday:** an online cart. Change the quantity from 1 to 3 and the total changes by itself. If you had typed the total in, it wouldn't. |
| Gluing text (1C-06) | **Picture:** beads on a string. Numbers have to be turned into text beads with `str()` before they fit. |
| Repeating text (1C-08) | **Everyday:** a stamp. `"█" * 3` stamps █ three times. Say explicitly why `*` works with text and a number but `+` doesn't. |
| Parameters (6A-04, 6A-05) | **Everyday:** a Mad Libs card. The card has blanks, and whoever plays fills them in. **Picture:** the call table, open by default under "Show me more". |
| Return (6A-06) | **Everyday:** "`print` says the answer out loud to the room. `return` writes it on a note and hands it back to you. Put the note in a box, or it's gone." |
| Comments, arithmetic, `+=`, `.lower()`, `roll_die` (1A-06, 1C-01, 1C-05, 2A-04, 6A-10) | Each needs at least one picture or everyday angle in addition to `shorter` / `from the campaign`. |

### 4.3 New exercise 6A-06b `be-the-ledger` (core; P → fill-ledger → R)

```python
def ward_strength(lanterns, runes):
    light = lanterns * 10
    glow = runes * 5
    return light + glow

barrier = ward_strength(3, 4) + 10
print(barrier)
```
(Verified: prints `60`. The names and values are original, set in Tor, and only the shape matches the worksheet.)

- **Task:** before Run, fill Mar'tu's ledger, one row per line: `lanterns`, `runes`, `light`, `glow`, *handed back*,
  `barrier`, *printed*. Each row is checked as it's typed. Then Run and compare.
- **Targeted wrong-answer messages:**
  - handed back = `15`: "15 is 10 + 5, the numbers written in the recipe. On this line the boxes hold 30 and 20.
    Add what is *in* the boxes."
  - `barrier` = `40` or `30`: "The `barrier` line starts from what the recipe handed back (50), not from `light` or
    `glow`."
  - printed = `55`, `45` or any sum of earlier rows: "`print(barrier)` shows only what's in `barrier`. It doesn't
    add up the earlier lines."
- **Hooks:** tracer to check the ledger afterward; AW[picture: the return arrow landing in `barrier`]; a twin variant
  with new numbers after any reveal.
- **Also:** one predict item of this shape in Quiz 6A and in Readiness Part 1, using the same wrong-answer map.
  Reuse the "fill the ledger" input in 1B-05, 1C-04 and 5A-04. That's an active version of the tracer.

### 4.4 Reconciliation card for 4A-02

> **Wait, quotes on names?**
> A **box's name** (a variable) never has quotes: `mana = 26`.
> A **label inside a dictionary** (a key) is a piece of text, so it does: `{"mana": 26}`.
> Predict: `hero = {"mana": 26}` → `print(hero["mana"])` versus `print(hero[mana])`.

---

## 5. Accommodation requests (switch these on for our group)

1. The preset question asked first (R1), with "Show me more" as the default and the teacher able to pre-set it
   provisionally. **No visible preset badge** on screen, so nobody can tell which preset a neighbor is on.
2. Warm-ups 1W on, and a two-step "read the error" routine from 1W-02 onward.
3. **Pair mode on for A-03 and A-04**, with roles that rotate each exercise ("navigator predicts, driver runs",
   "swap seats"). Solo "Show Mar'tu" checkpoints are one short item, recorded, never blocking.
4. "Explain it another way" auto-offered with a **new angle on each failed check**, picture first.
5. Tracer open by default on 1B-05, 1C-04, 5A-01, 5A-04 and 6A-04 through 6A-06, plus the active "fill the ledger"
   version.
6. Read aloud with `=` read as "gets", and the glossary (with the additions in R21) kept on in Quick Checks and the
   Readiness Check.
7. Block characters pre-typed or a symbol tray (R8).
8. One help stack after a failed run (R9), and a neutral-colored error panel (R24).
9. Diff-style output feedback (R12).
10. Scaffolded starters and the full hint ladder in projects (R17).
11. A per-student lean path that defers syllabus-only items and adds twin practice for 1B, 1C and 6A (R19).
12. Quiz review with right answers first (R26).
13. Mar'tu's deadpan reactions to whatever we type, with a safety fallback (R27).
14. Assemble-it (Parsons) offered as drafted. We understand mastery still needs typing, and that's fair.

---

## 6. Keep these (they work for us)

- **1A-01** "starter passes": a win in under a minute.
- **Broken-spell items mapped to our exact slips** (1A-03, 1A-08, 1B-06), with one checkpoint per bug so each fix
  gets its own green tick.
- **1B-01** `print(companion)` versus `print("companion")` (predict, then run).
- **1B-02** accepts any quoted value, Mar'tu reacts, and the DEF/NAME/TEXT detection.
- **1B-05** and **1C-04** with the tracer open by default.
- **1C-02**'s `# how many?` / `# how much is one?` labels and the swap message.
- **1C-03**'s hint ladder (point → teach → show) plus the your-turn variant.
- **CMB rerun messages** that say what was changed ("When I changed `lantern_count` to 7…").
- The **§2.4 rows** for unclosed quotes, `def (`, name-in-quotes (overriding Python's misleading "Maybe you meant
  '=='") and `-` for `=`.
- **6A-01** box versus recipe, and the **6A-06** return arrow.
- **Mar'tu's voice rules:** never "Wrong", wise feedback, the accent in rhythm and not in misspellings, and lore kept
  out of checkpoints.
- **No timers, leaderboards or public scores.** Neutral preset names, nothing "remedial", "not yet" on the mastery
  map.
- **"A reveal never counts toward mastery"**, a twin exercise after a reveal, and "Retype it" as the default.
- **Arithmetic as the confidence bridge** (1C-01), and the Readiness Check rule that "the story never blocks".

---

## 7. Answers to the teacher's open questions (from our side)

- **Q1 (fast lane):** don't put us on the Module 1 fast lane by default. At 1.4×, its 9 periods are about 13 for us,
  and Module 1's `def`-heavy starter is where A-02's belief comes back. If the class uses it, gate it on Quick
  Check 1 plus 6A-01.
- **Q3 (optional items):** we agree the Ward Sign (1P2) would engage us, but only with the block characters
  pre-typed (R8).
- **Q5 (reading level):** grade 6–7 is fine for checkpoint text. The bigger issue for us is *length* and *jargon*,
  not grade level.
- **Q6 (pair mode):** yes, on for A-03/A-04. Solo checkpoints are recorded, not required, and one item long.
- **Q7 (placement presets):** yes, pre-set "Show me more" for us from the diagnostic, provisionally, and confirm it
  with the first in-app checks. A-03/A-04's sheets may understate their floor.
- **Q8 (productive-failure hooks):** keep them, but with a pre-typed first line (R29), and skip them on frustration
  signals as drafted.

---

## 8. Where our asks could hurt other groups, and how to avoid it

- **Extra steps and checkpoints** (R13, R18, the 6A-06b ledger) add a few minutes for everyone. Fix: the ledger is
  core, because A-07 (G2) shares the return-value error, but "Keep it short" and instructions-light mode can merge
  checkpoints, and G4 can test out of Unit 6's trace items through Quick Check 6.
- **Auto-offered angles and default-on warm-ups** would be noise for G4. Fix: tie them to the preset and to failure
  signals, as the draft already does. R9's single help stack reduces noise for everyone.
- **A `def` bug in 1B-06** (R15) shows `def` to students who never thought of using it for boxes. Fix: it appears
  only as a fixed bug with the explainer's message, and Quiz 1 Q1 already shows `def ("hero")`.
- **Deferring syllabus-only items for us** (R19) means less syllabus coverage for our group. Fix: it's a per-student
  path the teacher can see and override, and it never changes anyone else's core.
- **Mar'tu echoing typed text** (R27) could repeat something unkind about a classmate (the sheets include a joke
  name). Fix: the echo shows only on the student's own screen, with a classroom-safe filter and a generic fallback.
- **Pre-typed block characters, diff-style output feedback, plain explainer titles and a neutral error panel**
  (R3, R8, R12, R24) help every group and cost nothing.
