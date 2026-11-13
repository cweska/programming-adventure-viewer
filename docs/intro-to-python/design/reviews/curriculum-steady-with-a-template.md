# Curriculum v1 review: group 3, "Steady with a template, stalls at the blank"

**Representing:** B-02 and B-03 (personas.md, group 3). I argue for these two sheets, not for the class
average.
**Read:** personas.md (roster, group 3, help caveats, class-wide patterns); B-verified.json (B-02, B-03,
page_notes); brief.md; campaign-python-inventory.md; curriculum-v1.md end to end; architecture.md §1.2 and §3.1
(support levels, hint ladder, solution gating).
**Checked in CPython 3.13.18** with a scratch probe (not the harness): the exact behavior of each of my
students' slips. Results are quoted below where they change the design.

---

## 0. Who we are, in one paragraph

Our sheets look tidy and correct wherever the worksheet gave us a structure, and empty where it didn't.
- We quote text correctly (`power_up= "Fireball"`) and write `health=100`.
- We wrote `Pizza=4 / Soda=10` on the front page before we even turned to the template.
- We got every pizza blank right (4, 10, 12, 2).

The gaps:
- Asked to make a variable for our hero, we wrote only the value: `"Spiderman"` (B-02), `"Superman"` (B-03).
  We think writing a variable means writing its value.
- We typed `68` instead of `pizza_cost + soda_cost`.
- At the function, B-03 left all of Part 3 blank, **even though the `def` line and the blanks were printed**.
  B-02 wrote `total = 10 * 5` (the call's numbers, not the parameters) and left `return` blank.
- We're loose with exact names: `Pizza`/`Soda` instead of `pizzas`/`sodas`, and `fireball` instead of
  `"Fireball"`.

We are quiet and cautious. We would rather leave something blank than guess. The same handwriting appears on
both packets (and on B-01's Part 4), so nobody knows yet what each of us can do alone. Our raw totals (13 and
12) look like group 4's (12.5 and 13.5). **They are inflated by templates and shared work.**

---

## 1. Verdict: would it work for us?

**Mostly yes. The content is right for us, but the support is wired to the wrong signal.**

The draft clearly read our sheets. These are exactly what we asked for:
- the 1B-02 message "I don't see a box named `character`. Write `character =` before your hero.",
- CMB reruns on the hard-coded total,
- the RET messages that name `None`,
- 6A-07 `return-the-right-box`,
- the 4B-04 and 6B-03 "replace each placeholder with the matching parameter" steps,
- pair mode with a solo checkpoint framed as showing off,
- a private mastery map.

The problem: **almost every safety net fires on failed runs, and we don't produce failed runs. We produce
silence.**
- The proactive hint offer needs 3 failed runs or 4 minutes.
- Project and challenge hints (`support: "light"`) unlock only "after the first failed Run" (architecture §3.1).
- "One more comment" contingent fading needs "repeated failures".

A student who stares at an editor that still matches the starter and never presses Run gets none of these,
except Assemble-it after 90 seconds. That is B-03's Part 3, replayed on screen.

There are also four places where Python or the draft's own explainer **gives us silence or a misleading
answer** at exactly our mistakes (§3). And the function lesson skips the one scaffold step that both of us
failed on paper: the body with blanks (§2, Unit 6).

Fix these and the plan works for us. None of the fixes needs a new unit. Most of them cost other groups nothing,
because they show up only on a "stuck and silent" signal.

---

## 2. Walking through it as us

### Unit 1

**1-A1 "How Mar'tu Teaches"**: good. We need it to say two things outright, because we won't ask:
- "Pressing Run on unfinished code is allowed and costs nothing. A red message is information, not a mark."
- "You can always ask for a starting line or more structure." (This needs the button in R5.)

**1A**: comfortable. Our quoting is solid. Quick Check 1 would let us skip what we already know, and it should
still route us into 1B, because QC1 item 2 (`character = ...`) is exactly what we'd miss. Good design.

**1B-01 `label-a-box`: the one exercise that must change for us.**
- CP1 is "change the value to another hero and run". That is a **value-only edit**: we'd retype `"Gearshift"`
  inside the quotes, pass, and never look at `companion =`. It rehearses our misconception: we only ever touch
  the value.
- The Investigate question ("which line has quotes, and what did each print?") is passive.
- What's missing is the moment where we *do our own mistake on purpose* and see what happens. I ran it:

```
"Gearshift"          # companion = deleted
print(companion)   -> NameError: name 'companion' is not defined
```

→ **Must (R2):** add an Investigate step: "Delete `companion =` from line 1, so only `"Gearshift"` is left.
Run. What happened?" The explainer (R1) then says that the words were made and then forgotten, because they
were in no box. Mar'tu: "A box needs a name AND a value." The tracer should draw a bare value line as "made, not
kept" (the value appears, then fades with no label). This is the "name AND value moment" the persona asks for.

**1B-02 `name-and-value`**: the message for `"Spiderman"` is right. Keep it. Two holes:
1. **The explainer trap (R1).** If we write our natural version, it goes like this:
   ```
   "Spiderman"
   print(character)   -> NameError: name 'character' is not defined   (no "Did you mean")
   ```
   The §2.4 row for a NameError on a `print(` line says *"If you meant the words, put them in quotes:
   `"character"`."* That steers us to `print("character")`, which prints the word `character`. **The draft's
   own explainer would walk us deeper into our misconception.**
2. **Parsons distractors.** PA lists `def ("character")` and `"character" = "Zelda"`, which are group 1's
   errors. Add **ours**: a bare `"Zelda"` line, and `print("Zelda")` in place of `print(character)`.

**1B-04 `exact-names`**: the near-miss detection is right, but our slip is two edits away: `Pizza` vs
`pizzas` (capital letter plus a plural). §2.3 NAME covers only "case variants" and "typos one edit away".
Python 3.13 itself does better here: `Pizza=4` followed by `pizzas * 12` gives `NameError: name 'pizzas' is not
defined. Did you mean: 'Pizza'?`. Keep Python's suggestion in the explainer, and extend `_near_names` to
singular/plural and case-plus-plural (R12). That matters for checks that read a variable when there is no
error.

**1B-06 broken spell**: "`"Lucky"` alone on a line where `hero` should be made". That line raises **nothing**.
The error appears later, on whatever uses `hero`, and the same misleading explainer fires (`print("hero")`).
R1 fixes it.

**1C-02 `what-each-number-means`**: the four labeled boxes set to 0 are perfect for us. But we *start writing
before reading the template*. That is literally what our `Pizza=4 / Soda=10` side work is. In this editor we'll
add `lanterns = 3` above the starter's `lantern_count = 0`:

```
lanterns = 3
lantern_count = 0
...
print(lantern_count * lantern_price)   -> prints 0, no error
```

No error at all, and the check just sees `lantern_count == 0`. → **Should (R11):** detect "a new box holding
the expected value while the starter's box is untouched". Message: "You made a new box `lanterns`. The starter's
box `lantern_count` is still 0. Put your 3 there."

**1C-03 `let-the-code-combine`**: good. The hint ladder (point → `c = a + b` → show) and the CMB message ("When
I changed `lantern_count` to 7, `total_cost` stayed 22") are exactly right for our 68. Keep them. One note: a
`total_cost = 0` placeholder looks like a blank that wants a number, which is how our paper template trained us.
The campaign uses 0 placeholders too, so don't remove them. Teach it instead: the Teach rung should say
"A 0 in the starter is a placeholder. It can be replaced by a calculation or a name, not only a number."

**1C-07 `status-line` [Mk]**: this is **the first exercise in the course with no template**. Four lines from an
empty editor. That's our cliff, in Unit 1. → **Should (R19):** give the left sides (`hero_name = `,
`magical_affinity = `, `max_mana = `, `mana = `) as the starter. Offer "Start from blank" only after a
hint-free pass of 1C-06.

**1P1 "The Night Watch Ledger" [C, 40 min]**: a 40-minute project with "light" support. Hints unlock only after
a failed run, and we won't run a blank file. → **Must (R7).**

### Unit 2

Mostly fine for us: control flow is introduced with examples and Parsons (2B-05 is A→M, which we like).
- **2B-08 `roll-and-decide` [Mk]** is a whole program from blank. Give a comment skeleton (`# 1. roll a d20`,
  `# 2. if ... success`, `# 3. else ... failure`) at first exposure (R8, R19).
- B-03 wrote `fireball` for `"Fireball"`. 2B-05's check should name capitals when `"Option 2"` is compared
  with `"option 2"`: "Text comparison is exact: capital letters count." (nice, R24)

### Units 3–5

Lists and dictionaries play to our strength. Most exercises edit given code, and **4B-04's "replace each 0 with
the matching variable"** is the campaign's own instruction style. Keep it.
- **5A-02 `each-mark`** is our first `for` loop, written from blank after a predict-only 5A-01. That's a
  two-level drop. Give `for mark in chalk_wall:` with a `pass` body at first exposure, then fade (R8).

### Unit 6: where we stopped on paper

**6A-01 to 6A-03**: comfortable. 6A-03 gives the exact line and a starter full of `pass`. We'll do it neatly.

**6A-04 `ingredients` and 6A-05 `use-the-ingredients`: the step we both failed is missing.**
- The worksheet's Part 3 was the def line, plus a body with blanks (`total = ____ * ____`, `return ____`).
- B-02 filled the blanks with the call's numbers. B-03, given those same blanks, wrote nothing.
- The draft goes from "the exact line is given" (6A-03) straight to "write the body line" (6A-04, 6A-05).
  §2.1 promises "comments with blanks → one blank → a whole line → a whole body", but in 6A the **blank stage
  for parameters doesn't exist**.

We need the paper shape again, **this time with feedback**. → **Must (R3):** add a bridge exercise,
**6A-05a `fill-the-ingredients`**:

```python
def show_hit(base_damage, bonus):
    print(___ + ___)

show_hit(4, 3)
show_hit(8, 2)
```

- Predict first: "What will the two calls print?"
- B-02's answer `print(4 + 3)` prints 7 twice. That's a visible "huh" moment, and PAR names it: "These blanks
  take the ingredient names from the `def` line (`base_damage`, `bonus`), not the numbers from one call. With
  `show_hit(8, 2)` your recipe still printed 7."
- `___` left in place gives `NameError: name '___' is not defined` (checked). The explainer must say "Fill in
  the blank `___`."
- Show it at first exposure, or contingently (after an assisted or failed 6A-04, or under "Show me more"), so
  group 4 doesn't pay for it.

**Another angle for parameters, built on our strength.** We're good at `name = value`. Make that the bridge.
Add an AW angle "from what you know" to 6A-04 and 6A-05:

> `show_hit(4, 3)` is like writing `base_damage = 4` and `bonus = 3` at the top of the recipe, then running the
> body. The call fills the boxes for you. The body only ever uses the box names.

Add a one-click Predict in 6A-04: "While `warn("Lucky")` runs, what is in the box `hero_name`?" (`"Lucky"` /
`hero_name` / nothing). The call-table angle and the tracer showing parameter boxes are already planned. Keep
them. This new angle reuses the one idea we already own.

**6A-05 PAR values collide with the task's answer (R14).** The fresh sets are (6, 1) and (11, 0). But 6 + 1 =
7, the same as the task call (4, 3). So against B-02's exact slip, copying the first call's numbers
(`print(4 + 3)`), **half of the PAR check is blind**. Only (11, 0) catches it. Authoring rule: a fresh argument
set must never produce the same result as any task call. Use something like (6, 5) → 11 and (20, 1) → 21.

**6A-06 `send-it-back`**: the task text gives `total = affinity * 2` and `return total` word for word. We'll
type it neatly, pass, and still not know what `return` does. That's B-02's blank `return`, papered over. I ran
the version without it:

```
def max_mana_for(affinity):
    total = affinity * 2
lucky_max = max_mana_for(13)
print(lucky_max)        -> prints None. No error, no explanation.
```

The same happens with a bare `return` (B-02's blank). → **Must (R4):**
- Add an Investigate step: "Delete `return total`. Run. What does `lucky_max` hold now? Put it back." `None`
  then shows up while we're safe, not in a crash later.
- Add a site-wide **console None notice** (R4b): when a printed line is exactly `None` and the program defines a
  function with no `return` that has a value (an AST check), add one line under the output: "`None` means a
  recipe gave nothing back. `max_mana_for` has no `return` line." The persona's frustration is literally
  "getting None back with no explanation". The RET check covers checkpoints. This covers the Investigate and
  free runs, where we actually meet it.

**6A-07**: excellent. It is aimed straight at B-02. Keep it.

**6B-02 `recipes-change-sheets` says "No return is needed."** Right after 6A taught us "missing return = bug",
that will confuse a student whose misconception is "return is optional or its job is unclear". → **Should
(R25):** add a one-screen rule card plus a one-click sort:

> **When does a recipe need `return`?** When the caller catches or uses the result (`x = f()`,
> `"Hit: " + f()`). A recipe that only prints, draws, or changes a sheet doesn't need one.

Campaign pair: `get_mana_bar` returns, and `show_mana` doesn't. 6B-07 is exactly that pair, so the card pays
off immediately.

**6B-03 and 6B-07**: our kind of task (placeholders, comments naming the expressions). Keep them. In 6B-07, make
the comment numbers map one-to-one onto the four checkpoints, so we can use the checklist to check ourselves.
That's how we work: "I start right away, then use the template to check myself."

**6C-05 `cast-from-the-book`**: this is where the persona predicts we crash. Persona risk: "success on
scaffolded tasks inflating their confidence, then a crash at the multi-step campaign parts". The draft offers
"Assemble it" or "one more comment" after repeated failures. We need a **defined ladder we can climb down
ourselves**, without failing first (R15):

| Level | What the editor shows |
|---|---|
| L1 (default) | Numbered comments, campaign style. |
| L2 | `if ___ < ___:` / `elif ___ < ___:` / `else:`, each branch's body still a comment. |
| L3 | Adaptive Parsons (distractors as listed). |
| L4 | A worked twin with a different spell, then retype. |

The step down is the "More structure" button (R5), always visible. The step up is offered after a pass.

**Solo checkpoints in Unit 6 (R9).** Every SOLO tag is on the "Broken spell" debug exercise. Our unknown isn't
debugging. It's **whether each of us can write a recipe alone**. In pair mode, 6A, 6B and 6C (and 1B, 1C)
should end with a 2-minute typed **make-twin** for each seat (6A: "write `heal(hero_name, amount)` that prints
…"). Not only the debug.

### Unit 9: Readiness Check

- "Unaided" must not mean "blank editor". The campaign always gives starter code (`def perform_roll(die_size):
  return 1`). → **Should (R18):** every Part 1 code item (2, 3, 8) gets a campaign-style starter. Item 8
  ("write `roll_die(die_size)`") becomes `def roll_die(die_size):` with `return 1`, as in the campaign. It's
  faithful to the campaign, and group 4 loses nothing.
- Good: typed answers, never a grade, "the story never blocks", and review in a different representation.

---

## 3. Where Python or the explainer gives us silence or a wrong steer (all checked in 3.13.18)

| Our slip | What Python does | What the draft's explainer would say | Fix |
|---|---|---|---|
| `"Spiderman"` alone, then `print(character)` (B-02, B-03; 1B-02, 1B-06) | That line is silent. Later: `NameError: name 'character' is not defined` | "If you meant the words, put them in quotes: `"character"`" → **wrong steer** | R1: if the source has a bare string statement, or the missing name is the one the checkpoint asks for, say: "Line 1 has `"Spiderman"` on its own. Python made the words and forgot them, because they're in no box. Write `character = "Spiderman"`." |
| A function with no `return`, or a bare `return` (B-02) | Prints `None`. **No error.** | nothing (no error to explain) | R4b: console None notice |
| Empty function body (B-03's blank Part 3), def line only or a comment only | `IndentationError: expected an indented block after function definition on line 1` | (no row; it reads like an indentation problem) | R13: "A recipe needs at least one line inside it. Write a line under `def`, indented. Not ready? Write `pass` for now." |
| A new box above the starter's (side-work habit) | Runs fine and prints `0` | nothing | R11: NAME/NEW-BOX check message |
| `___` blank left in (if we adopt R3) | `NameError: name '___' is not defined` | "put it in quotes" → wrong steer | R3: "Fill in the blank `___`." |
| `print(base + bonus)` inside `show_hit(base_damage, bonus)` | `NameError: name 'base' is not defined. Did you mean: 'False'?` | passes Python's hint through | R22 (nice): hide Python's suggestion when it's a keyword. List the recipe's ingredient names instead. |
| `''Fireball''` (two apostrophes; our sheets draw `"` as two ticks) | `SyntaxError: invalid syntax` | (no row) | R21 (nice): "Two `'` marks are not one `"`. Use the `"` key." |

---

## 4. Site features we need (and how they avoid hurting others)

- **R5 "Start me off" and "More structure".**
  - Add a rung 0 to the hint ladder: **Start me off** inserts the first few tokens of the line (`total_cost = `,
    `def warn(`, `for member in `) and puts the cursor after them. It gives us a first move, not the answer.
  - Add an always-visible **More structure** button that steps one scaffold level up (comments → skeleton →
    Parsons → worked twin), with no failures needed.
  - Both are private hint use, like the rest of the ladder.
- **R6 A silent-stall trigger.** If the editor still matches the starter and there has been no Run for 90 s,
  offer rung 0/1, not only Assemble-it. It turns off for the exercise after one dismiss, and globally after a
  hint-free streak, as planned.
- **R7 "Light" support that works without failing.** Rung 1 (Point) is always available under `light`. Deeper
  rungs still wait for a failed run. Every project starter carries its task-group comment headers (`# A. What we
  know`, `# 1. hours_until_burst`).
- **R8 Starter level as a field, checked by the gate.** Each Make/Modify exercise declares
  `starterLevel: S4 blanks | S3 left sides / skeleton | S2 numbered comments | S1 signature | S0 blank`.
  - Gate rule: the first exposure of a construct starts at S3 or above, and consecutive exercises on the same
    skill drop at most one level.
  - Today the fade is prose only, and 1C-07, 2B-08, 5A-02, 6A-04 and 6A-05 don't state their starter at all.
- **R9 Pair mode for us.**
  - Answer Q6 "yes": on by default for B-02/B-03.
  - The seat that types alternates every exercise and is tracked, so the helper (possibly B-03) doesn't always
    drive. "Explain to your partner" prompts name a seat ("Seat B explains").
  - The solo "Show Mar'tu" twin uses **different names and values per seat**, so watching doesn't give it away.
    On separate devices, it queues into each student's own login.
  - Solo results are recorded, never shown to the partner, and never framed as checking up on anyone.
- **R10 Placement.** Don't set our preset from the paper totals. Default us to "Show me more" provisionally,
  and let 1B-02 and the first Unit-6 solo twin decide.
- **R16 A mastery map that shows the climb.**
  - Each skill shows the scaffold level we passed it at (with blanks → from comments → from blank), with a
    "next step up" link.
  - "Done together" and "done solo" are **two positive ticks**, not a pass/fail.
  - This is our biggest delight item. It's honest about our template habit without shaming it.
- **R17 After an Assemble-it pass**, a 1–2 line typed twin at "comments" level follows, like the post-Show
  your-turn variant. Otherwise "assemble" becomes our way around typing.
- **R20 Investigate prompts** are one-click choices, with free text optional. We leave free-text "why?" boxes
  blank.

---

## 5. What would delight us

- Ticking up the mastery map from "with blanks" to "from blank", skill by skill.
- A "Start me off" nudge that gets the first line down.
- Working a recipe out with a partner, then a solo "Show Mar'tu" that Mar'tu acknowledges: "You did that
  alone. I saw." (nice, R23)
- Mar'tu reacting to our heroes. We picked Spiderman and Superman. Accept any quoted value, as planned.

## 6. Keep these

- 1B-02's value-without-name message, and 1B-02 CP2 (print through the variable, not retyped).
- CMB reruns and their "When I changed X, Y stayed Z" wording (1C-01, 1C-03, 1C-09).
- The 1C-03 hint ladder and your-turn variant.
- The RET messages, 6A-07 `return-the-right-box`, and the `NoneType` concatenation explainer row.
- 4B-04 and 6B-03 "replace each placeholder with the matching parameter".
- Subgoal labels (6A-08, 4B-05, 6C-05).
- 6A-05's pair prompt "Explain to your partner why `4 + 3` inside the recipe breaks the second call."
- Assemble-it on unchanged editors after 90 s. Mastery needs typing.
- Pair mode plus solo checkpoints framed as showing off, never as cheating detection.
- A private mastery map with no comparison view. No timers. Readiness never a grade, and the story never blocks.

## 7. Where my asks could hurt other groups, and how to avoid it

- **Group 4 (time).** The bridge steps (6A-05a, the 6A-06 None step, the 6C-05 ladder) show only at first
  exposure under "Show me more", or after an assisted or failed previous step. A hint-free group 4 student never
  sees them. Quick Checks still skip whole lessons.
- **Group 4 (nagging).** The 90 s silent-stall offer fires only if the editor is *unchanged* and nothing has
  run. One dismiss silences it for that exercise, and it turns off after a hint-free streak.
- **Group 2 (shape-copying).** Blanks and "Start me off" could let shape-copiers fill shapes without meaning.
  Every blank is graded by behavior (PAR, CMB), so literals fail. "Start me off" gives the *name* side of a
  line, which helps group 2's name-copying problem rather than hiding it.
- **Group 1 (feeling behind).** A map that shows scaffold levels could make someone feel behind. It stays
  private, has no comparison, and frames each level as a next dare, not a deficit.
- **Pairs elsewhere.** Pair mode on by default is right for us, but maybe not for A-03/A-04, who goofed together.
  Make it the teacher's choice per pair.
- **Everyone (time).** Solo make-twins add about 2 minutes per lesson, and only in pair mode.
