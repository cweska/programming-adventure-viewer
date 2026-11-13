# Curriculum v1 review: group 2, "Right shape, wrong meaning"

**Representing:** A-05, A-07, A-08, B-01 (personas.md, group 2). I am arguing for these four sheets, not the
class average.
**Read:** personas.md §Group 2, A-verified.json (A-05, A-07, A-08), B-verified.json (B-01), brief.md,
campaign-python-inventory.md, curriculum-v1.md end to end, architecture.md §3.1 and §4.6.
**Verified in CPython 3.13.18** (scratch probe, not the harness): the exact error each of my students'
slips produces. Results are quoted below where they change the design.

---

## 0. Who we are, in one paragraph

We know the shape `name = value` (all four of us wrote `health = 100`; B-01 wrote `PiZZa= 4 / sodaS = 10`
before even seeing the template). We break on **meaning**:
- We copy the example's names: `player_name` instead of `character` (A-05, A-07, A-08).
- We leave our own text unquoted: `kratos`, `spartin rage in barsed hamah` (A-08), `fireball` (A-05, B-01),
  B-01's unquoted joke name.
- We grab the word problem's numbers in the order they appear. We put prices into the count boxes and line
  totals into the multiplier slots (`pizzas = 12`, `pizzas * 48`: A-05, A-07, A-08, independently).
- We type the answer we worked out by hand (`total_cost = 68`, all four of us).
- At functions we either freeze (A-05 blank, B-01 erased its one mark) or work backward to the expected
  number (A-08 `25 * 2`, A-07 `10 * 5` / `return 50`). A-07 also traced the return value as the raw inputs
  (`3 + 4 = 7`).
- A-08 copied a previous template word for word (`print(total_frait)`).

Our confidence is partly false: we got 68, felt right, and the code was wrong. We love making things ours.
We skip long reading and go straight to the example.

---

## 1. Verdict: would it work for us?

**Mostly yes, if about seven specific holes get closed.** This draft was clearly built on our sheets. CMB
reruns, NAME with example-name detection, PAR with fresh arguments, "any quoted value passes", 1C-02's
"what does each number mean?" step and Assemble-it on blank editors are exactly what we asked for.

It still has places where a shape-copier **passes without learning the meaning**:
1. Many checkpoints hand us the exact line to type, and some of those checks are output-only.
2. 1C-02 can be passed by grabbing numbers in reading order, which is the strategy that failed us on paper.
3. Two of our four unquoted-text slips raise a SyntaxError the explainer doesn't cover.
4. One check rejects our own hero (1C-07).
5. A-07's "the function returns its raw inputs" belief is cited as caught, but no item actually tests it.
6. Our false confidence could fade our support too early.

Each of these has a concrete fix below. None of the fixes needs a new unit.

---

## 2. Walking through it as us

### Unit 1: where we live or die

**1A-02 `your-own-words`**: good. "prints a line different from the example's" is precisely our copy trap.
Mar'tu echoing the line is the delight we want.

**1A-04 `words-need-quotes`**: good for A-05 (`fireball`) and single-word cases. **But it misses half of
us.** I ran our actual values:

```
power_up = spartin rage in barsed hamah   -> SyntaxError: invalid syntax      (A-08)
character = [joke name]             -> SyntaxError: invalid syntax      (B-01's pattern)
power_up = Fire ball                      -> SyntaxError: invalid syntax      (A-07's value, unquoted)
print(Spartan Rage)                       -> SyntaxError: invalid syntax. Perhaps you forgot a comma?
character = kratos                        -> NameError: name 'kratos' is not defined
power_UP= fireball                        -> NameError: name 'fireball' is not defined
```

§2.4 maps unquoted text **only** to NameError. Our personal, multi-word values (the ones we care about most)
get a bare "invalid syntax", and inside `print(...)` Python actively misleads ("forgot a comma?").
→ **Must:** add an explainer row for this, and add a multi-word case to 1A-04 (see R2).

**1B-01 → 1B-02**: the NAME check that says "You used the example's name `companion`. This task asks for
`character`" is the single most important message in the course for us. Keep it. Also keep B-01's catch:
"I don't see a box named `character`. Write `character =` before your hero."
- Make sure 1B-02's editor does **not** still contain 1B-01's `companion = ...` code. If it does, we will edit
  `companion` and wonder why it fails.
- Add our exact wrong lines as Parsons distractors: `player_name = "Kratos"` and `character = Kratos`
  (unquoted). Right now there are only `def ("character")` and `"character" = "Zelda"`, which are group 1's
  errors.

**1B-04 `exact-names`**: the near-miss detection (`heath`, `Powrup`, `power_UP`) is right. Two asks:
- A-08 struggles with spelling (`plager`, `spartin`, `barsed`). A plain "names must match" message will feel
  like a spelling test. Show the two names aligned with the differing letter marked: `heath` vs
  `hea`**`l`**`th`.
- Give us the **why** from the campaign: "The game calls `move_left()` when you press the arrow. If your
  recipe is called `Move_left`, the game can't find it and nothing happens." That is a reason, not a rule.

**1C-01 `chalk-math`**: CMB from the first arithmetic exercise. Good. But a CMB failure is the first time a
check "changes our numbers behind our back". We need to **see** that happen (R10).

**1C-02 `what-each-number-means`**: this is our exercise, and it can be passed **without reading meaning**.
The prompt says "3 lanterns that cost 4 coins each, and 5 coils of rope that cost 2 coins each". The count
comes first, and the boxes are presumably count-then-price. So grabbing numbers in reading order (our exact
strategy, per the persona: "I grab the word problem's numbers in the order they show up") lands every
number in the right box. On paper the prices came first, and that's what broke us.
→ **Must:** make CP2 (the rope) state the price first: "Rope is 2 coins a coil, and Mar'tu needs 5 coils."
Then order-grabbing fails, and the existing swap message ("You swapped them: 5 is how many…") does its job.
Do the same in the 1C-03 your-turn variant ("Candles are 1 coin each; Oogrish wants 3").

**1C-03 `let-the-code-combine`**: the CMB check and hint ladder are great, but two specific gaps:
- **Our second error has no message.** We didn't just swap; we put **line totals into multiplier slots**
  (`pizzas * 48`, `sodas * 20`). The course version is `lantern_cost = lantern_count * 12`. CMB catches it
  (a rerun with 7 lanterns gives 84, not 28), but the message only says "build it from the variables". Add a
  named wrong answer with its own message: "You multiplied by 12, which is already the cost of **all 3**
  lanterns. Multiply the count by the price of **one**."
- **Term collision.** The AW angle "write the recipe, not the answer" calls `total_cost = lantern_cost +
  rope_cost` a *recipe*. Then 6A-01 teaches "a box (`=`) versus a recipe (`def`)". We map words to things
  literally; we will be told in Unit 6 that the thing we called a recipe in Unit 1 is a box. Use **"Show your
  working"** in Unit 1 instead. It's a phrase from math class, where we are strong: "In math you show your
  working. In Python, the working **is** the answer." Save "recipe" for `def`, and call back to 1C in 6A-05.
- The hint-2 Teach example (`a = 2`, `b = 5`, `c = a + b`) will get pasted. Expect `total_cost = a + b`. The
  NameError explainer should recognize hint names: "`a` and `b` were in Mar'tu's hint. Your boxes are
  `lantern_cost` and `rope_cost`."

**1C-07 `status-line`**: **this check punishes personalization.** It has a DF button, so `hero_name` is a
creative prompt, but CP2 is "the status line is exact [OUT]" against `Oogrish: 18/18 mana`. If A-08 types
`hero_name = "Kratos"`, CP2 fails. That is the first item on our "what makes me quit" list.
→ **Must:** check `hero_name + ": " + str(mana) + "/" + str(max_mana) + " mana"` for **whatever hero they
chose** (CMB rerun with `hero_name = "Tester"`).

**1C-08 `repeat-a-mark`**: the task text gives the whole line, so we'll type it and pass. CP3's empty and
full reruns are good. What's missing is any check that we know what `(max_mana - mana)` counts (R9).

**1C-09 `broken-spell-1C`**: "a total typed by hand (the output looks right, but the rerun check fails,
which shows students that checks change inputs)". Love it, but it comes at the end of 1C. By then we've
already been confused by four CMB failures. Teach "checks try other numbers" at 1C-01 (R10), and let 1C-09
be the payoff.

**Quick Check 1**: items 3 and 4 are CMB, so we can't test out by accident. Good. Keep it that way.

### Unit 2

- **2A-03 / 2A-04 / 2B-06**: again the task gives the line (`passed = roll >= needed`,
  `said_yes = answer.lower() == "yes"`). Transcription passes. This is fine because the campaign does the same,
  but add a one-click "point at it" after the pass (R9).
- **2B-03 `otherwise`**: NAME for copying the example's `spot_roll` is right. "Any text is accepted as long
  as the two lines differ" is exactly right for us.
- **2B-05 `four-answers`**: catches unquoted `option 2`. Also add a message for **exact text in a
  comparison**: if we write `"Option 1"` or `"option1"`, say "`choice` was `"option 1"`, but your branch checks
  `"Option 1"`. Text comparison is exact: every letter, space and capital." This is A-07's `"Fire ball"`
  problem, and the campaign's `user.clicked() == "option 1"` needs it.
- **2C-01 `anatomy-of-a-fizzle`**: **a trap built for us.** We drop quotes, and `error_type = NameError`
  **runs without error** (verified: it stores `<class 'NameError'>`). The TEXT check's template would then
  say "`error_type` holds `<class 'NameError'>`…", which means nothing to us. Special-case it: "`error_type`
  holds Python's own NameError, not the words. Put it in quotes: `"NameError"`."
- **2C-03 `name-fizzles`** asks us to "Read Python 3.13's 'Did you mean…?' suggestion". When **our typo is
  the defined name**, Python points us the wrong way. I verified: `heath = 100` then `print(health)` gives
  `Did you mean: 'heath'?`. A-08 would "fix" it by spreading the typo, and then the NAME check rejects it.
  The explainer should reframe it: "Python found two names that almost match, `health` and `heath`. Pick the
  spelling the task asks for and use it in both places."

### Unit 3: output-only checks we can fake

We will type answers we can see. These checkpoints are OUT-only or unspecified, and a hard-coded print
passes:

| Item | What we'd type | Fix |
|---|---|---|
| 3A-06 CP2 `chalk_wall[len(chalk_wall) - 1]` | `chalk_wall[6]` or `print(37)` | AST: uses `len` inside the subscript; CMB with an 8-item wall |
| 3A-08 `join-two-walls` [OUT] | the joined list typed out | CMB with other walls |
| 3B-01 `d8_faces` with `range` [OUT] | `[1, 2, 3, 4, 5, 6, 7, 8]` | `_uses('call:range')` |
| 3B-04 count the 48s | `print(2)` | CMB with a wall that has three 48s |
| QC3 item 2 "append a guess and print the last item" | `print(33)` | read the last item through the list (CMB) |

Same pattern later: **8A-02** (slice `Greenroom`; we'd type `"Greenroom"`) and **8B-03** (`int("48")`; we'd
type `48`). → **Must** (R3): a rule, not a list.

### Unit 4: quotes flip on us

Unit 1 taught "text needs quotes". Unit 4 adds "keys need quotes, but a key that lives in a variable
doesn't" (4A-07), and 6B-03 adds `"mana_cost": mana_cost`. For B-01, A-05 and A-08 this is where "always
quote text" collapses into guessing. We need **one principle, worded the same way every time**:

> **Quotes mean "these exact letters". No quotes means "look inside the box with this label".**

That one sentence explains `print("glug")` vs `print(glug)`, `"name"` as a key, `spell_book[spell_name]` vs
`spell_book["spell_name"]`, and `"mana_cost": mana_cost`. Put it in the AW for 1A-04, 1B-01, 4A-02, 4A-07
and 6B-03, plus a six-card "quotes or no quotes?" sort as a recall card at 4A-07 (R11).

- **4B-04 `spell-book-of-spells`**: the variables (`cost`, `needed`) have different names from the keys
  (`mana_cost`, `required_affinity`), so matching them takes meaning. **Keep that.** The likely error from
  us is a swap (`"mana_cost": needed`). CMB catches it, but the message should name the swap (R7).

### Unit 5

- **5A-02 / 5A-05: the course is ambiguous about "gap".** The chalk wall's values are "gaps" (hours between
  bursts: 3A-04, 3A-05, 5A-02, 1C-01's `first_gap`). But 5A-05 "The gaps" and §1.2 ("The gaps between them
  are 0, 1, 1, 2, 3, 4") use the same word for the **differences**. For students whose problem is "what does
  each number mean?", this is the course making our mistake for us. Wall values = **gaps**; differences =
  **shrink** (5B-04 already uses `shrink`). Rename 5A-05 to "How much each gap shrank".
- **5A-02** "using the example's loop variable is fine. Names matter only when the task names them." This is
  correct and important, so **say it to us out loud**. "A name you invent is yours. A name the task gives you
  is a promise the checks (and later the game) rely on." Otherwise the NAME messages feel random.
- **5A-03 `each-member`**: the LOOP check reruns with 5 heroes. Let the fifth be **our hero from 1B-02**
  (R21).

### Unit 6: the cliff

**6A-04 / 6A-05: show the two calls before we write.** PAR is the right check, but it fires *after* we've
typed `print(7)`. The persona's need is "functions shown being called with two different inputs, **so fixed
numbers visibly break**". A-08 worked backward to 50 because there was only one target. Put both calls
(with expected outputs) in the starter:

```python
def show_hit(base_damage, bonus):
    pass

show_hit(4, 3)   # should show 7
show_hit(8, 2)   # should show 10
```

If we write `print(7)`, **our own Run** shows `7` and `7`, and we catch it ourselves (our favorite moment).
PAR's fresh `(6, 1)` stays as the real check. Turn CP2 ("both calls are present") into "add a third call for
your own hero" so there's still something to write.

**6A-04 heads-up.** The example is `cheer(name)` and the task is `warn(hero_name)`. We will write
`def warn(name):`. It works behaviorally and PAR passes. That's fine, but give a non-blocking heads-up: "Works!
The task named this ingredient `hero_name`; you used the example's `name`. In the campaign the names are
already written for you, so match them."

**A-07's raw-inputs return is not actually tested.** 6A-06 lists "A-07 'the return value is the raw inputs'"
under Catches, but 6A-06 has one parameter and one local (`total = affinity * 2`). A-07's error was on a
**two-parameter, two-local** function: the `score_points(3, 4)` trace with `gold_value`/`silver_value`,
traced as `3 + 4 = 7`. → **Must:** add a predict item between 6A-06 and 6A-07:

```python
def loot_value(gems, coins):
    gem_worth = gems * 10
    coin_worth = coins * 5
    return gem_worth + coin_worth

print(loot_value(3, 4))
```

Choices: `7` / `50` / `34` / `gem_worth + coin_worth`. The `whyWrong` for `7`: "3 and 4 are the ingredients
you handed in. The recipe hands back the boxes it **made** from them: 30 + 20." The tracer auto-opens on a
wrong answer (R16). Also, in 6A-06 add a RET message for returning the parameter: "`max_mana_for(9)` handed
back 9. That's the ingredient you passed in. Hand back the box you computed, `total`."

**6A-07 `return-the-right-box`**: `return result` "copied from 6A-06's example" turns our copying habit into
a bug we can find. **Keep this exactly.**

**6B-03 / 6C-04 (placeholders → parameters)**: the campaign's `add_spell` says "replace each placeholder
with the matching parameter". The meaning error we'll make is **the right shape with the wrong parameter in
the slot**, i.e. the pizza error in dict form. PAR with `(5, 2, "teal")` and `(9, 7, "gold")` catches it.
The message should name it: "`"mana_cost"` got 2, which is the `required_affinity` you passed. Match each key
to the parameter with the same name." (R7)

**Blank function bodies.** Assemble-it "on any editor that is blank or still matches the starter after
about 90 s", plus the proactive hint at 4 minutes, is the first move A-05 and B-01 never had. Keep it. For B-01
especially, 90 s is the right number. Don't let it creep up.

**6C-05 / Readiness mini-boss**: fine for us **if** the earlier fixes land. We'll lean on Parsons in 6C-05,
and "mastery needs typing" is the right counterweight.

### Units 7–8

- Trials are not for us yet. That's fine; they're optional.
- **8B-01 / 8B-09** "forgetting to reassign" is our kind of error: the shape is right, but the result is
  thrown away. Good.
- 8A-02 and 8B-03 need non-OUT checks (see the Unit 3 table).

### Unit 9: Readiness Check over-credits us

Our strength is arithmetic and guided tracing (A-05 traced Part 4 perfectly). Our weakness is **writing** the
combination. Part 1 has several predict-only items we'd ace by mental math, especially **item 12** ("predict
`hero["mana"]` after `hero["mana"] = hero["mana"] - 3`, from 20 → 17"). But no typed item tests
`combine-values` (campaign-critical in §2.6) with a CMB rerun.
- → **Should:** make item 12 typed: "Write the line that spends `cost` from `hero["mana"]`", with a CMB rerun
  at a different cost.
- State that every typed item uses CMB/PAR, never OUT alone. Otherwise a hard-coded answer marks us "Ready"
  and the campaign's `caster["max_mana"] - caster["mana"]` catches us instead, in front of the class.

---

## 3. Cross-cutting asks

### False confidence
We will click "too easy" on the pulse, because the number came out right. We'd likely answer "a little" or
"yes" to "Have you typed code before?". If either signal fades our support (examples collapsed,
instructions-light, Quick Checks suggested), we skate.
- The pulse and self-report should **never** change support defaults on their own. Only unaided passes plus
  predict accuracy should.
- Show us our **predict calibration**: "You predicted 4 of 6 right this lesson. The two you missed were both
  about what a function hands back." That is honest feedback that doesn't feel like a grade, and it targets
  the "I'm getting it, until suddenly I'm not" feeling.

### Transcription without meaning: a "point at it" check
Where the checkpoint text gives the exact line (1C-08, 2A-03, 4A-05, 4B-04, 5A-07, 6A-06), add **one
one-click question after the pass**. It is unscored, feeds the mastery map, and is skipped under
instructions-light. Example for 1C-08: "Mar'tu taps `(max_mana - mana)`. What does it count?"
→ the used mana / the full blocks / the max. One click. It turns a copied shape into a checked meaning.

### Examples vs tasks: make the task's names un-missable
We skip reading and jump to the example, so the required names have to be where our eyes land. Put a **"Names
to use:"** chip row on every checkpoint that requires exact names (`character`, `hero_name`, `total_cost`).
Pair it with a **LEFT** check (leftover identifiers): any identifier that appears only in the example, a hint
we opened, or the previous exercise triggers "`total_frait` is left over from the example. This task's box is
`total_cost`." That is A-08's `print(total_frait)`, caught by name.

### "Try other numbers" before the check does it
A button next to Run that reruns our code with Mar'tu's alternate inputs and shows a tiny table:

| `lantern_count` | your `total_cost` | Mar'tu expects |
|---|---|---|
| 3 | 22 | 22 ✓ |
| 7 | 22 | 38 ✗ |

The CMB failure message shows the same table. It makes "write the working, not the answer" something we
**see**, and it gives us the "I caught my own mistake by running it" moment the persona says delights us.
Introduce it at 1C-01.

### Personalization that sticks
- Every DF/creative prompt gets a Mar'tu reaction that **quotes our value** ("*Kratos.* Hm. Welcome to the
  cabin." is perfect; make it a template, not one line).
- Let our 1B-02 hero come back as the fifth roster member in 5A-03's LOOP rerun and as an optional fifth sheet
  in 4P. **Privacy:** some of our hero values are joke names, maybe about classmates (B-01's), and some sheets
  used real first names. So the value stays in the local save only, never goes to the classroom progress API
  or the teacher view, passes a PG filter, and falls back to "Mar'tu's pick".

### After a reveal: "Make it yours" now, not later
The plan queues a twin "into a later warm-up". For us, retyping Mar'tu's version is pure shape-copying.
Offer an **immediate, optional** twin framed as personalization ("Now do it for your hero / your own
supplies"). It uses new names and values, so it is the adaptation practice the persona asks for.

---

## 4. Requested changes (prioritized)

| ID | Where | Change | Why (our evidence) | Priority |
|---|---|---|---|---|
| R1 | 1C-02 CP2; 1C-03 your-turn variant | State the price **before** the count in the second word problem so order-grabbing fails; keep the swap message. | A-05/A-07/A-08 put prices in count boxes because the worksheet listed prices first; persona: "I grab the numbers in the order they show up." | must |
| R2 | §2.4 explainer; 1A-04 | Add a row: `SyntaxError: invalid syntax` (or "forgot a comma?") on an `=` or `print(` line whose value is two or more bare words → "These look like words. Put all of them inside one pair of quotes: `"spartan rage"`." Add a multi-word case to 1A-04. | Verified in 3.13: A-08 `spartin rage in barsed hamah`, B-01's joke name and an unquoted `Fire ball` all raise SyntaxError, not NameError. | must |
| R3 | §2.7 authoring rules; 3A-06, 3A-08, 3B-01, 3B-04, 8A-02, 8B-03, QC3-2, Readiness typed items | New rule: no OUT-only check on any checkpoint whose answer is a computed value. Its `wrong_answers` must include the hard-coded literal (`print(<expected>)`) and prove it fails. | All four of us hard-coded 68; persona: "a hand-typed 68 prints the same as the formula". | must |
| R4 | 1C-07 CP2 | Check the status line against the student's own `hero_name` (CMB rerun with `"Tester"`), not exact `Oogrish: …`. | The DF prompt invites our hero; persona: "a check that marks me wrong for typing my own hero" makes us quit. | must |
| R5 | 6A (new 6A-06b predict); 6A-06 RET message | Add a two-param, two-local predict (`loot_value(3, 4)`) with a `7` distractor and the whyWrong above; add a RET message for returning a parameter. | A-07 traced `return value = 3 + 4 = 7`; no current item reproduces that structure. | must |
| R6 | 6A-04, 6A-05 starters | Pre-write two calls with `# should show …` comments so fixed numbers visibly break on our own Run; CP2 becomes "add a third call for your hero". | A-08 `25 * 2` to hit 50; A-07 `10 * 5`; persona: "functions shown working on two different inputs". | must |
| R7 | PAR/CMB message library (§2.3); 1C-03, 4B-04, 6B-03, 6C-04 | SWAP detection: when a slot's value equals another input's value, say which one went where. Add the line-total message ("12 is already the cost of all 3"). | The shared pizza error is a swap plus line totals in multiplier slots (A-05, A-07, A-08); `add_spell` placeholders. | must |
| R8 | Site feature; every checkpoint with required names | A "Names to use" chip row; a LEFT check for identifiers that appear only in the example, opened hints or the previous exercise; a non-blocking example-name heads-up when behavior passes (6A-04 `name` vs `hero_name`). | A-05/A-07/A-08 `player_name`; A-08 `print(total_frait)`; persona: "a heads-up when I've used the example's name". | should |
| R9 | 1C-08, 2A-03, 4A-05, 4B-04, 5A-07, 6A-06 | One-click "point at it" meaning question after the pass (unscored, mastery-map evidence, hidden under instructions-light). | Right shape, wrong meaning: these tasks give the line, so we pass by transcription. | should |
| R10 | Site feature; introduced at 1C-01 | A "Try other numbers" self-rerun button and the same rerun table inside CMB failure messages. | Persona delight: "catching my own mistake by running it"; makes CMB visible before 1C-09. | should |
| R11 | AW in 1A-04, 1B-01, 4A-02, 4A-07, 6B-03; recall card at 4A-07 | One quotes principle, worded identically: "Quotes mean these exact letters; no quotes means look inside the box with this label." Add a 6-card quotes sort. | A-05, A-08, B-01 unquoted text; Unit 4 and 6B-03 flip the "always quote text" habit. | should |
| R12 | 1C-03 AW; 6A-05 AW | Replace "write the recipe, not the answer" with "show your working"; reserve "recipe" for `def`; add an explicit 1C callback in 6A-05. | We map words to things literally; 6A-01's "box vs recipe" contradicts a Unit 1 "recipe" that is a box. Arithmetic is our strength (class pattern 10). | should |
| R13 | 5A-05 title; §1.2 world data; T-Lo-2 | Wall values = "gaps"; differences = "shrink". Rename 5A-05 to "How much each gap shrank". | "What does each number mean?" is our core need, and the course uses one word for two quantities. | should |
| R14 | 2C-01; 2C-03 | Special-case `error_type = NameError` (it runs silently); reframe Python's "Did you mean: 'heath'?" when the student's typo is the defined name. | Verified in 3.13. We drop quotes (A-05, A-08, B-01); A-08 `heath`. | should |
| R15 | §2.5 presets, pulse, 1A self-report | Pulse and self-report never fade support on their own; only unaided passes plus predict accuracy do. Show predict calibration per lesson. | Persona: "confidence is partly false: they got 68 and felt right." | should |
| R16 | Tracer (§2.5) at 1B-05, 1C-04, 6A-06, new 6A-06b | Auto-open the tracer when a predict about a return value or reassignment is wrong (one click to close). | A-07 "return value = 3 + 4"; persona: "a visual trace of what `return` sends back and where it goes". | should |
| R17 | §5.1 item 12; all typed Part 1 items | Make item 12 a typed `hero["mana"] = …` with a CMB rerun; state that typed items use CMB/PAR, never OUT alone. | We ace predict-arithmetic but can't write the combination; `combine-values` is campaign-critical and has no typed item. | should |
| R18 | NAME message (§2.3) | Show near-miss names aligned with the differing letter highlighted (`hea`**`l`**`th`). | A-08's spelling (`plager`, `heath`, `spartin`) would otherwise feel like a spelling test. | should |
| R19 | Parsons distractor lists (1B-02, 1C-03, 6A-05, 6A-06, 6B-03) | Add our exact wrong lines: `player_name = …`, unquoted `Kratos`, `total_cost = 22`, `print(7)`, `return gems + coins`, the swapped parameter. | The current distractors are mostly group 1's errors (`def ("character")`). | should |
| R20 | §2.1 Compare / reveal | After a reveal, offer an immediate optional "Make it yours" twin with our own names and values. | Retyping is shape-copying; persona: "practice adapting a template to new names". | nice |
| R21 | 1B-02 → 4P, 5A-03 | The student's hero persists locally and appears as the 5th roster member in the LOOP rerun and as an optional 5th sheet (privacy rules in §3). | Persona: "personalization everywhere … with Mar'tu reacting to it". | nice |
| R22 | All DF prompts | Reaction templates that quote the student's value, with a PG-filter fallback. | A-08's Kratos and Spartan Rage, B-01's joke name: we invest when the work is ours. | nice |
| R23 | 2B-05; message library | A string-exactness message for comparisons (`"Option 1"` vs `"option 1"`). | A-07 `"Fire ball"`; the campaign's `user.clicked() == "option 1"`. | nice |
| R24 | 5A-02 Learn pane | Say the naming rule aloud: "A name you invent is yours. A name the task gives you is a promise." | Otherwise NAME checks feel arbitrary next to "your loop variable is fine". | nice |
| R25 | Article 1-A1 | A 60-second clickable tour (press a hint, open another-way, try Assemble-it once) instead of a reading screen. | Persona: "long reading before doing; they skip to the example anyway". | nice |

---

## 5. Accommodations we're asking for

- "Try other numbers" self-rerun button with a rerun table (R10).
- "Names to use" chips plus a non-blocking example-name heads-up (R8).
- One-click "point at it" meaning questions after transcription checkpoints (R9).
- Tracer auto-open on a wrong return/reassignment predict (R16).
- Predict calibration shown to the student (R15).
- Two-call starters with expected-output comments on first-function exercises (R6).
- Letter-diff highlighting on near-miss names (R18).
- Immediate optional "Make it yours" twin after a reveal (R20).
- Hero value persisted locally only, reused in later rosters, with a PG filter and Mar'tu's pick as fallback (R21).
- Keep Assemble-it at about 90 s on blank or untouched function editors, plus the 4-minute proactive hint.

## 6. Keep these (do not cut in revision)

- The **CMB** pattern and `_rerun`, with messages that say what changed ("When I changed `lantern_count` to 7,
  `total_cost` stayed 22").
- **NAME** with example-name detection (`companion`, `player_name`) and case and typo near misses.
- **TEXT accepts any quoted value**, and Mar'tu's "*Kratos.* Hm. Welcome to the cabin."
- 1B-02's "I don't see a box named `character`. Write `character =` before your hero." (B-01).
- **1C-02** as a dedicated "what does each number mean?" step, with its swap message.
- **PAR** with fresh arguments (`"Tester"`, 6/1, 11/0).
- **6A-07**'s deliberate `return result` copied from the example.
- **1C-09**'s hand-typed total that looks right but fails the rerun.
- 4B-04's variables named differently from the keys (`cost` → `"mana_cost"`), which forces meaning.
- Predict-before-Run in nearly every exercise; ≤ 120 words before the first action.
- Rule 2.7 #5: examples labeled and visibly different from tasks.
- The hint ladder's your-turn variant (same pattern, new names).
- "Mastery needs typing": Assemble-it in lessons, typed in Quick Checks and the Readiness Check.
- Readiness "explain" items 9 and 10.
- No timers, leaderboards or public scores.

## 7. Where our asks could hurt other groups, and how to avoid it

- **Order-breaking word problems (R1)** add reading load for group 1. Put the reversed order only on the
  *second* problem, keep the `# how many?` / `# coins for ONE` comments, offer read-aloud, and treat the swap
  message as teaching, not failure.
- **Meaning questions, heads-ups and chips (R8, R9)** add clicks and noise for group 4 (A-01, A-06). Hide them
  under instructions-light and after a Quick Check pass. Heads-ups never block, and can be muted. A
  deliberate rename by a group 4 student should never fail a check.
- **Two-call starters (R6)** give groups 3 and 4 less to write. Offset this with "add a call for your own
  hero", and keep "Start from blank" for anyone on a hint-free streak.
- **Tracer auto-open (R16)** could feel patronizing. It triggers only on a wrong predict, and one click
  closes it.
- **Hero persistence (R21)** is a privacy and classroom-safety risk (joke names that may target classmates,
  real first names). Keep it in the local save only, out of the classroom API and the teacher dashboard, run a
  PG filter, and fall back to "Mar'tu's pick".
- **Readiness item 12 becoming typed (R17)** raises the bar slightly for everyone, but it measures a
  campaign-critical skill that currently has no typed item. Keep the other predict items.
- **New check patterns (SWAP, LEFT)** cost engineering time. Each should ship with harness `wrong_answers`
  that prove the message fires, under the existing rule 2.7 #8.
- **Renaming "recipe" in Unit 1 (R12)** and **"gap" vs "shrink" (R13)** cost nothing, and they help group 1,
  who also need consistent words.

## 8. In our voice

> Honestly the best part is typing Kratos and having Mar'tu go "Kratos. Hm. Welcome to the cabin." And the
> thing where it secretly changes the lantern number and my 22 breaks? That would totally get me, because I
> already did the math in my head and I'd just type 22. I'd actually like to press a button and watch it try
> other numbers myself, so I find it before it tells me. But then 1C-07 wants exactly "Oogrish: 18/18 mana",
> and I'm obviously putting my own guy, so it's going to say I'm wrong for no reason. And half the steps just
> tell me the line to type, so I'll type it, get the green tick and still not know what the brackets are for.
>
> The functions part is where I'd freeze, same as on paper. If the box is empty I'll leave it empty or pick
> numbers that make the answer. If the two calls are already sitting at the bottom saying "should show 7" and
> "should show 10", and mine shows 7 twice, I'd see it myself. Also, I always thought it just added the two
> numbers you give it, so show me where the answer actually comes from. And please don't make my hero name
> fail anything, ever.
