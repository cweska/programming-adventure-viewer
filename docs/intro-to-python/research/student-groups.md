> Anonymized evidence from the class's 'Python Power-Up' diagnostic worksheets. Student names were never read (covered on the scans). Ids (A-01..A-08, B-01..B-03) follow the scan order. Hero answers that could be real first names, joke names that could be about a classmate, and handwritten dates are redacted.

# Student groups and representative personas: "Python Power-Up" diagnostic

Source: verified transcriptions of 11 anonymous worksheets (`assessments/A-verified.json`: A-01 to A-08;
`assessments/B-verified.json`: B-01 to B-03). The worksheet has four parts: Part 1 variables (`character`,
`health = 100`, `power_up = "Fireball"`), Part 2 a pizza-party arithmetic template (4 pizzas at 12, 10 sodas
at 2, `total_cost = pizza_cost + soda_cost`), Part 3 a function body (`total = base_attack * bonus_multiplier`,
`return total`), and Part 4 a scaffolded trace of `score_points(3, 4)` plus a bonus (answer 60).
Raw totals are out of 16 (3 + 5 + 3 + 5).

**Privacy:** no student names appear here. Some hero values students wrote could be real first names or a joke
about a classmate. Those are redacted as "a first name" or "a joke name". Only clearly fictional characters
(Zelda, Kratos, Spiderman, Superman) are quoted.

## Roster at a glance (least to most experienced/comfortable)

| Group | Students | Defining evidence | Placement confidence |
|---|---|---|---|
| 1. Starting from zero | A-02, A-03, A-04 | No working model of a variable: `def ("character")`, a dash for `=`, numbers unrelated to the problem, traces that add the code's constants | A-02 high; A-03, A-04 medium (joint goofing may hide a higher floor) |
| 2. Right shape, wrong meaning | A-05, A-07, A-08, B-01 | Know `name = value`, but copy the example's names, leave text unquoted, put "the numbers from my math" into blanks, and avoid or reverse-engineer the function | A-05, A-07 high; A-08 medium (edge of group 1); B-01 medium (edge of group 3) |
| 3. Steady with a template, stalls at the blank | B-02, B-03 | Correct quotes and every Part 2 blank right, but the hero is a bare value and the function is blank or has no return; heavy shared handwriting | B-02 low; B-03 medium |
| 4. Ready to stretch | A-01, A-06 | Independent, solid on variables, modeling and tracing; closest attempts at the function, but still no parameters or correct return | A-01 high; A-06 high (edge of group 3) |

| Student | Raw total /16 | Part scores (P1/P2/P3/P4) | Help suspicion | Group |
|---|---|---|---|---|
| A-02 | 6.5 | 0.5 / 1 / 0.5 / 4.5 | low | 1 |
| A-03 | 3 | 0 / 1 / 0 / 2 | high (peer goofing with A-04, no score gain) | 1 |
| A-04 | 3.5 | 0.5 / 1 / 0 / 2 | high (peer goofing with A-03, no score gain) | 1 |
| A-05 | 7 | 1.5 / 0.5 / 0 / 5 | low-medium | 2 |
| A-07 | 6 | 2 / 0.5 / 1.5 / 2 | low | 2 |
| A-08 | 2.5 | 0.5 / 0.5 / 0.5 / 1 | low | 2 |
| B-01 | 10.5 (5.5/11 without Part 4) | 1 / 4.5 / 0 / (5, not own hand) | medium, Part 4 only | 2 |
| B-02 | 13 | 2.5 / 4.5 / 1 / 5 | high (two hands on one packet) | 3 |
| B-03 | 12 | 2.5 / 4.5 / 0 / 5 | medium (may be the helper) | 3 |
| A-06 | 12.5 | 2.5 / 4.5 / 1.5 / 4 | low | 4 |
| A-01 | 13.5 | 3 / 4.5 / 1 / 5 | none | 4 |

---

## Group 1: Starting from zero (no working model of a variable yet)

**Students:** A-02, A-03, A-04 (key `starting-from-zero`)

### Evidence
Raw totals: A-02 6.5, A-03 3, A-04 3.5. Part 1 and Part 2 place them here, not the totals.
- **Part 1:** none wrote a working assignment for the hero. A-02 wrote `def ("character")`, `def ("health")`,
  `def: Power_up= ("Fire Ball`. That uses the function keyword and puts the NAME in quotes. Only later did A-02
  squeeze in `Health = 100`. A-03 wrote `canes_women` (no `=`, no quotes), `meidicine = 80`, `fries_up = "Fierball.`.
  A-04 wrote a bare `"chick-fa-le_women"`, `medicine = 100`, `chicken_sandwich - "Fireball` (a dash for `=`, an
  unclosed quote).
- **Part 2:** the numbers have no link to the problem. A-02 wrote 5 pizzas, 5 sodas, `* 5`, `total_cost = 5P + 2S`.
  A-03 and A-04 wrote 180 pizzas, 1000 sodas, totals 18 and 15.
- **Part 3:** unrelated literals: A-02 `100 * 5` / `return 500`; A-03 `30 * 0` / `return 10`; A-04 `50 * 0` / `return 35`.
- **Part 4:** A-02 reached 60 only because the scratchpad supplies the arithmetic (answers written a line off).
  A-03 and A-04 added the code's constants (`10 + 5 = 15`). They started the bonus line from `gold_value` or
  `silver_value` instead of the returned value. Their "printed" answers (55, 45) are sums of earlier results.
- **Arithmetic is fine:** all three computed 3 x 10 and 4 x 5 correctly. The gap is what the Python means, not the math.

### Typical misconceptions
- `def` creates a variable, and the variable's name goes in quotes or parentheses (A-02 `def ("character")`).
- A bare value or string counts as a variable, and `=` is optional or can be swapped for `-` (A-03 `canes_women`; A-04 `"chick-fa-le_women"`, `chicken_sandwich - "Fireball`).
- Quotes don't need to be closed (A-02 `("Fire Ball`, A-03 `"Fierball.`, A-04 `"Fireball`).
- Names are flexible and case doesn't matter (A-02 `Health`, `Power_up`; A-03 and A-04 replaced the required names).
- Numbers in code don't have to come from the problem, and counts and prices are interchangeable (A-02 5s; A-03/A-04 180 and 1000).
- Python works like algebra shorthand (A-02 `total_cost = 5P + 2S`).
- Function blanks take any numbers (A-02 `100 * 5`, A-03 `30 * 0`, A-04 `50 * 0`).
- Tracing means adding the constants visible in the code, not the variables' current values (A-03, A-04: `10 + 5 = 15`).
- A function's return value doesn't land in the variable on the left of the call (A-03's bonus line uses `gold_value`, A-04's uses `silver_value`).
- `print` shows a sum of everything computed earlier (A-03 printed 55 = 40 + 15; A-04 printed 45 = 30 + 15).

### Comfort and affect
Low confidence, shown in two ways. **A-02 is earnest:** every blank attempted, hesitation dots after item 1,
overwritten digits, and a late, smaller `Health = 100` added as a self-correction. There are no margin
questions or comments. **A-03 and A-04 deflect with humor:** matching fast-food joke answers (`canes_women` /
`chick-fa-le_women`, `meidicine` / `medicine`, `fries_up` / `chicken_sandwich`), absurd counts (180 pizzas,
1000 sodas) and `* 0`, worked out together. They still filled every blank, so they weren't refusing. The task
felt out of reach, so they made it social. Their correct arithmetic gives them a confidence foothold: they can
succeed once the code's meaning is made concrete.

### Needs
- A ground-up model of a variable: name, `=`, value, all three required, and the name never in quotes. This answers A-02's `def ("character")`, A-04's bare `"chick-fa-le_women"` and `chicken_sandwich - "Fireball`, and A-03's `canes_women`.
- An explicit contrast between `=` (make a variable) and `def` (make a function), taught before the campaign's first starter code (`def move_left(): pass`). A-02 believes `def` makes variables.
- Quotes taught as "open and close around text", showing and explaining the error a missing quote causes (A-02 `("Fire Ball`, A-03 `"Fierball.`, A-04 `"Fireball`).
- Turning a word problem into variables with labels ("how many?" vs "how much each?"), plus a note that Python is not algebra shorthand (A-02 `5P + 2S`; A-03/A-04 180 and 1000).
- Tracing support that shows each variable's current value (a ledger or step-through). Then they stop adding the constants they can see (A-03/A-04 `10 + 5 = 15`) and see the return value land in `final_score` (A-03/A-04 used `gold_value`/`silver_value`).
- Two or three alternate explanations per concept (box-and-label analogy, recipe, picture, step-by-step trace, everyday example), offered automatically after a failed check, not hidden.
- Plain language first and jargon second, with glossary hovers for parameter, argument, return, string and concatenate.
- Very small steps with Run after each, and a success in the first couple of minutes.
- A legitimate outlet for humor: checks that accept their own silly names and values (in quotes), and Mar'tu's deadpan reactions.
- Pair-friendly activities with short individual checkpoints. A-03 and A-04 worked as a unit, so neither student's own level is visible.

### Frustrations and risks
- Walls of instruction text and undefined jargon; they read fast, looking for something to copy.
- Bare error names (SyntaxError, NameError) with no translation, and red text that feels like blame.
- The same explanation repeated louder instead of a different angle.
- A blank editor, or a five-step task before any visible result.
- Comparison with faster classmates, timers, visible scores.
- Goofing off as cover when lost (A-03/A-04), or copying a partner to get through, so mastery is never built.
- Gaming the hint ladder or Show solution straight to the answer with no follow-up attempt.
- The campaign's `def`-heavy starter code reactivating the "def makes a variable" belief (A-02).
- Strict checks that reject a creative but valid value, which they will read as "I'm bad at this".

### What their representative will fight for
1. Every concept explained in plain words first, then an "Explain it another way" option with genuinely different angles (picture, analogy, trace, real-world example).
2. Tiny steps, early wins, and Run feedback after every step.
3. Error explanations mapped to the exact slips on the sheets (missing or unclosed quote, `def` vs `=`, a dash for `=`, a name in quotes), saying what happened and what to try.
4. Hint ladders that point, then teach, then show, followed by a fresh "your turn" variant, so a reveal is never a dead end.
5. A worked example before each "your turn", clearly labeled as an example.
6. Optional warm-ups (what text is, why quotes, what an error looks like, what Run does), on by default for this group.
7. Room to be funny inside the code legitimately, and Mar'tu's dry humor kept in.
8. No timers, no leaderboards, private hint use, and neutral path names (never "remedial").

### Persona brief
> I speak for the students in this class who are newest to Python (sheets A-02, A-03, A-04). None of us wrote a working variable on the worksheet. Some of us tried every blank in earnest; some of us turned it into a joke with a friend. Either way, the page didn't make sense, so we did what we could.
>
> What I can do: arithmetic when you hand it to me. I got 3 x 10 = 30 and 4 x 5 = 20. When the trace spelled out the math, one of us followed it to 60. I've seen that code looks like `name = value` (one of us wrote `medicine = 100`).
>
> What I can't do yet: I don't know what a variable is. One of us wrote `def ("character")` because `def` looked like the Python word for making things. One of us wrote `chicken_sandwich - "Fireball`, with a dash for the equals sign and no closing quote. For 4 pizzas and 10 sodas we wrote 5 and 5, or 180 and 1000, and one of us wrote `5P + 2S`, algebra-style. Tracing, we added the numbers printed in the code (10 + 5) instead of what the variables held, and lost track of what ends up in `final_score`. In the function we wrote any numbers (`30 * 0`, `return 10`).
>
> How it feels: like everyone else got a manual I didn't. For some of us, joking is easier than being wrong.
>
> How I read instructions: fast, hunting for something to copy. Long paragraphs lose me by the second sentence. Parameter, argument, return: those words mean nothing to me yet.
>
> What makes me zone out: walls of text; the same explanation said louder; an error that just says SyntaxError; a blank editor; five steps before anything happens.
>
> What delights me: a win in the first two minutes; Mar'tu saying something silly because I typed it; a picture of the box with its label; being allowed to be funny in the code.
>
> What I'll fight for: plain words first, then the same idea from another angle (a box, a recipe, a picture, a trace) when it doesn't land; tiny steps with Run after each; errors that say what to try; hints that teach before they reveal, then a fresh one to try; no timers or public scores; and checks that I can do it myself, not just my partner.

---

## Group 2: Right shape, wrong meaning (eager pattern-copiers)

**Students:** A-05, A-07, A-08, B-01 (key `right-shape-wrong-meaning`)

### Evidence
Raw totals: A-05 7, A-07 6, A-08 2.5. B-01 scored 10.5 on paper, but its Part 4 is in another student's
handwriting, so B-01 is placed on Parts 1-3 only (5.5/11).
- **They know the shape:** A-05 `health = 100`, A-07 `health=100`, A-08 `heath = 100`, B-01 `health=100`. B-01 even
  wrote `PiZZa= 4 / sodaS = 10` before reaching the template.
- **They copy shapes rather than meanings:**
  - A-05, A-07 and A-08 used the example's `player_name` for the hero instead of `character`.
  - A-05 (`Powrup = fireball`), A-08 (`plager_name = kratos`, `power_up = spartin rage in barsed hamah`) and
    B-01 (a joke name with no quotes and no `character =`; `power_UP= fireball`) left text unquoted.
- **The shared Part 2 error:** A-05, A-07 and A-08 each made the same error: `pizzas = 12`, `sodas = 2`,
  `pizza_cost = pizzas * 48`, `soda_cost = sodas * 20`, `total_cost = 68`. They reached it independently. A-07's
  margin plan (`pizzas = 12 / sodas = 2 / total_cost = 48 + 20`) and A-08's red-pen drafts show them putting "the
  numbers from my math" into the blanks. A-08 also copied the apples/oranges template word for word (`print(total_frait)`).
- **Functions:**
  - A-05 left it blank.
  - B-01 abandoned it (one faint, erased `10`).
  - A-08 picked `25 * 2` to hit 50.
  - A-07 used the test values `10 * 5` / `return 50`, then traced the return as `3 + 4 = 7` (the raw inputs).
- **Boundary cases:**
  - **A-08** has the lowest raw total in the class but sits here, not in group 1. Every item has the right
    structure (`name = value`; add the two values, then add 10). The low score comes from unquoted creative values,
    a slip carried forward (`gold_value = 50`) and the shared Part 2 misreading.
  - **B-01** got Part 2 right (like group 3) but left strings unquoted (like this group).

### Typical misconceptions
- Use the example's variable name, not the one the task asks for (A-05 `player name`, A-07 `player_name`, A-08 `plager_name`).
- Text values don't need quotes, especially multi-word or personal ones (A-08 `kratos`, `spartin rage ...`; B-01's unquoted joke name and `fireball`; A-05 `fireball`).
- Exact spelling and case of names don't matter (A-08 `heath`, A-05 `Powrup`, B-01 `power_UP`).
- Blanks are slots for the numbers from my own math, not quantities with meanings: prices go into count variables and line totals into multiplier slots (A-05, A-07, A-08: `pizzas = 12`, `pizzas * 48`, `sodas * 20`).
- Work the answer out by hand and type it in (A-05, A-07, A-08, B-01: `total_cost = 68`).
- A function is a calculation that should produce the expected number, so pick literals that make it (A-08 `25 * 2` makes 50; A-07 `10 * 5` / `return 50`).
- A function returns its raw inputs added together (A-07: return value = `3 + 4 = 7`).
- Copying a template word for word works even when its names don't fit (A-08 `print(total_frait)`).
- Writing a variable means writing its value (B-01's hero with no `character =`).

### Comfort and affect
Engaged, inventive and willing to try, but on shaky footing.
- A-08 personalized everything in red pen (Kratos, "Spartan Rage") and drafted, then crossed out, side code.
- A-07 planned in the margin before filling blanks.
- B-01 gave the hero a joke name and wrote assignments before seeing the template.
- A-05 did all the mental math correctly.

Their confidence is partly false: they got 68 and felt right while the code was wrong. At functions the
confidence runs out. A-05 left Part 3 blank, B-01 wrote a 10 and then erased it, and A-08 worked backward to hit
the expected 50. They invest when the work is theirs and retreat when there is nothing to copy.

### Needs
- Examples that use visibly different names and values from the task, plus a check that says "you used the example's name (`player_name`); this task asks for `character`" (A-05, A-07, A-08).
- Quotes on text every time, including multi-word and personalized values, with the NameError shown when they're missing (A-08 `kratos`, `spartin rage ...`; B-01's joke name and `fireball`; A-05 `fireball`).
- A "what does each number mean?" step before filling numbers in, separating counts from prices. This targets the shared A-05/A-07/A-08 `pizzas = 12` / `pizzas * 48` error.
- "Write the recipe, not the answer": checks that change the inputs and re-run, so a hard-coded 68 fails with a friendly explanation (A-05, A-07, A-08, B-01).
- Functions shown being called with two different inputs, so fixed numbers visibly break (A-07 `10 * 5`, A-08 `25 * 2`).
- A visual trace of what `return` sends back and where it goes (A-07: "return value = 3 + 4").
- Practice adapting a template to new names rather than copying it (A-08 `print(total_frait)`).
- Exact-name feedback explaining that Python matches names letter for letter (A-08 `heath`, A-05 `Powrup`, B-01 `power_UP`).
- A first move at every blank function: a hint offered after idle time, or an "assemble it" (Parsons) version (A-05 blank, B-01 erased).
- Room to personalize: checks that accept any quoted value they choose.

### Frustrations and risks
- Checks that only test printed output let "right answer, wrong reason" pass, because a hand-typed 68 prints the same as the formula.
- Strict checks that reject a personal value (Kratos instead of Fireball) feel like punishment for creativity.
- Long reading before doing; they skip to the example anyway.
- An empty function stub with nothing to start from: they leave it blank or work backward to the expected number.
- Believing they understand because the number came out right, then hitting the campaign's `caster["max_mana"] - caster["mana"]` and `add_spell(...)` parameters with no model of why.
- Examples that use the same names as the task, which they will copy.

### What their representative will fight for
1. Checks that catch hard-coding and copied example names, with feedback that explains why it matters, not just "wrong".
2. Examples visually separated from tasks (different names, an "Example" label), and a heads-up when they reuse an example's name.
3. Predict-then-run loops so they find their own mistakes.
4. Personalization everywhere: any hero name, any quoted value, with Mar'tu reacting to it.
5. Functions taught as reusable recipes, always shown with two or more calls.
6. A hint ladder and an "assemble it" option on every multi-line task, so nothing is left blank.
7. A "name the meaning" micro-step (count vs price, input vs output) before fill-ins.

### Persona brief
> I speak for students who will try anything, but who build code by copying shapes, not meanings (sheets A-05, A-07, A-08, B-01).
>
> What I can do: `health = 100`. I know a variable looks like `name = value`; one of us wrote `PiZZa= 4` and `sodaS = 10` before reaching the template. I'm good at the math: I worked out 48 + 20 = 68 in the margin. I plan: one of us wrote `pizzas = 12 / sodas = 2 / total_cost = 48 + 20` beside the prompt, and another drafted in red pen and crossed things out.
>
> What I can't do yet: I copy the example's names. Three of us wrote the example's `player_name` when the task said `character`. I forget quotes on text, especially when I make it mine: `kratos`, `spartin rage ...`, `fireball`, and a joke name for the hero. I put numbers where they seem to fit instead of where they mean something: prices into the count variables and my own totals into the price slots (`pizzas = 12`, `pizza_cost = pizzas * 48`). I type the answer, 68, instead of `pizza_cost + soda_cost`. Functions: I leave them blank, or I pick numbers that make the answer I expect (`25 * 2` to get 50). One of us thought the function returned `3 + 4`, its raw inputs, not the values it had just calculated.
>
> How it feels: like I'm getting it, until suddenly I'm not. I love making it mine: Kratos beats "Fireball".
>
> How I read instructions: I skip to the example and copy it. I grab the word problem's numbers in the order they show up.
>
> What makes me quit: a check that marks me wrong for typing my own hero; long reading before doing; a function with nothing to start from.
>
> What delights me: personalizing everything; my code running and Mar'tu reacting; catching my own mistake by running it.
>
> What I'll fight for: examples that look different from the task, plus a heads-up when I've used the example's name; checks that notice when I typed the answer instead of the recipe, and say why it matters; a "what does each number mean?" step before blanks; functions shown working on two different inputs so I see why fixed numbers break; checks that accept any quoted value I pick; and a hint at every blank so I never leave one empty.

---

## Group 3: Steady with a template, stalls at the blank

**Students:** B-02, B-03 (key `steady-with-a-template`)

### Evidence
Raw totals: B-02 13, B-03 12, but these are the least certain placements in the class. They are placed by
their most authentic and weakest evidence, Part 3 on both sheets.
- **Handwriting:** the second reader found one hand (looped 2s, round 0s, two-tick quotes) across all of B-03's
  sheet, B-02's Parts 1-2 and B-01's Part 4. A different hand wrote B-02's Part 4 (and probably B-02's Part 3).
- **Help suspicion:** B-02 high; B-03 medium (B-03 may be the student who helped).
- **What the sheets show:** correct quoting (`power_up= "Fireball"` / `"fireball"`) and `health=100`. Both wrote
  `Pizza=4 / Soda=10` on their own before reaching the template. Every Part 2 blank is right (4, 10, 12, 2), except
  the hard-coded `total_cost = 68`.
- **Item 1** on both is a quoted value with no variable: `"Spiderman"`, `"Superman"`. Writing a variable means
  writing its value.
- **Functions:** B-03 left all of Part 3 blank. B-02 wrote `total = 10 * 5` and left `return` blank, so the
  function would return None.
- **Part 4 not used:** the 5/5 scores aren't counted as evidence, because of the mixed handwriting and because
  the worksheet supplies the arithmetic.
- **How they differ:** unlike group 2, they don't mix up counts and prices or leave text unquoted. Unlike
  group 4, they made no independent attempt at the function, and their work isn't clearly individual.

### Typical misconceptions
- A variable is just its value: the hero written as `"Spiderman"` or `"Superman"`, with no `character =` (B-02, B-03).
- Work the total out by hand (68) instead of writing `pizza_cost + soda_cost` (both).
- Parameters and arguments are the same thing, so the call's values go in the body (B-02 `10 * 5`).
- `return` is optional, or its job is unclear (B-02 left it blank, so the function returns None).
- No model of a function body at all (B-03 left Part 3 blank).
- Exact names and case are loose: side work `Pizza`/`Soda` vs the template's `pizzas`/`sodas` (both); `fireball` vs `"Fireball"` (B-03).

### Comfort and affect
Cautious and reliant on a template. The work is neat and mostly correct wherever the worksheet gives a
structure, and silent where it doesn't (B-03's Part 3 entirely blank, B-02's `return` blank). They start working
before they reach the template (`Pizza=4 / Soda=10` on the front page), which suggests eagerness, but they
would rather leave a blank than guess. The shared handwriting suggests they lean on each other heavily, perhaps
more than on the material. Collaboration is a source of comfort for them and a risk for verifying what each
knows, never a moral failing. No jokes, doodles or comments: the affect is quiet.

### Needs
- A clear "a variable is a name AND a value" moment. Their item 1 was a quoted value with no `character =` (B-02 `"Spiderman"`, B-03 `"Superman"`).
- Scaffolds that fade gradually: one blank, then two, then a whole line, then a whole function body. They succeed on templates (every Part 2 blank right on both) and stop when the template disappears (B-03 Part 3 blank).
- A guaranteed first move on any empty editor: a skeleton, an "assemble it" version, or a first hint offered automatically after idle time.
- Functions and `return` explained concretely in the game world (what goes in, what comes back), including what None means when `return` is missing (B-02).
- Parameters vs the values passed in (B-02 `10 * 5`).
- "Let the code combine it": both hard-coded 68.
- Exact names and case (side work `Pizza`/`Soda` vs `pizzas`/`sodas`; B-03 `fireball`).
- Legitimate collaboration features (pair discussion prompts, "explain it to your partner") plus short solo checkpoints. The handwriting shows they worked as a unit, so each student's own level is unknown.
- A mastery map, so their real progress is visible to them.

### Frustrations and risks
- Dropping from fill-in blanks straight to a blank editor.
- A function that silently returns None with no explanation.
- Being told to "just try": they would rather leave it blank than be wrong.
- Success on scaffolded tasks inflating their confidence, then a crash at the multi-step campaign parts (`mana-bars`, `hold-the-barrier`) that require combining pieces.
- Solo checks framed as cheating detection, which would feel like an accusation.
- Mastery never verified individually if they always work together.

### What their representative will fight for
1. Scaffolds that fade in small, predictable steps, with the option to step back up.
2. A structured first line on every empty editor, never a bare blank.
3. Concrete in-world function examples (Mar'tu's recipes) that make `return` visible.
4. Check messages that explain None and missing returns.
5. Pair mode and discussion prompts, plus friendly solo "show what you know" checkpoints.
6. A visible checklist of the skills mastered so far.

### Persona brief
> I speak for students whose sheets look tidy and mostly right wherever the worksheet gave a template, and empty where it didn't (sheets B-02, B-03). Our sheets also suggest we worked very closely together: the same handwriting shows up on more than one packet. So some of what I "can do" may be what we could do together.
>
> What I can do: quote text correctly (`power_up= "Fireball"`) and write `health=100`. Before I even turned the page to the template, I wrote `Pizza=4` and `Soda=10` on my own. With the template, I got every pizza blank right: 4, 10, 12 and 2.
>
> What I can't do yet: asked to make a variable for my hero, I just wrote `"Spiderman"` (or `"Superman"`). I knew it was text and needed quotes, but I didn't write `character =`. I thought writing a variable meant writing its value. I typed 68 instead of `pizza_cost + soda_cost`. Functions are where I stopped. One of us left the whole function blank. The other wrote `10 * 5` (the test numbers, not the parameters) and left `return` empty, so it would give back nothing at all. I'm loose with exact names too: `Pizza` and `Soda` instead of `pizzas` and `sodas`.
>
> How it feels: fine while the page holds my hand. When it lets go, I'd rather leave it blank than guess wrong.
>
> How I read instructions: I start right away, then use the template to check myself. If there's no template, I stall.
>
> What makes me zone out: jumping from fill-in-the-blank straight to an empty editor; getting None back with no explanation; being told to "just try".
>
> What delights me: a checklist of what I've already mastered; a nudge that gets me to a first line; working something out with a partner and then proving I can do it alone.
>
> What I'll fight for: scaffolds that fade step by step (one blank, then two, then a whole line, then a whole function); a starting move whenever the editor is empty (a skeleton, an "assemble it" option, a first hint offered when I've been stuck a while); functions and `return` explained with a concrete example from the game; check messages that explain None; and pair work that's allowed, with a short solo checkpoint that feels like a chance to show off, not like getting caught.

---

## Group 4: Ready to stretch (solid basics, one step from functions)

**Students:** A-01, A-06 (key `ready-to-stretch`)

### Evidence
Raw totals: A-01 13.5 (the class high), A-06 12.5. Help suspicion is none (A-01) and low (A-06): the
handwriting is consistent and the novice errors look authentic.
- **Part 1:** A-01 is the only student in the class who wrote the requested `character= "Zelda"`. The value was
  borrowed from the example, which A-01 explained in the margin: "not my favorite I just can't think of a
  character". A-01 also wrote `health= 100` and `power_up = "Fireball'` (the closing quote may be a single tick).
  A-06 wrote `player_name ="..."` (the example's name, with a first name as the value), `health = 100` and
  `power_up = "Fireball"`.
- **Part 2:** the only two students outside the B section who modeled the pizza problem correctly (4, 10, `* 12`,
  `* 2`). Both showed their work (A-01 `4·12=48 / 2·10=20 / 68`), but both still hard-coded 68.
- **Part 3:** the strongest attempts in the class, and still not right. A-01 wrote `total = attack * bonus` /
  `return reslt`. Those are approximate parameter names, and "result" was copied from the `double_number` example,
  so it raises a NameError. A-06 wrote the correct test values `10 * 5` / `return 50`.
- **Part 4:** A-01 perfect. A-06 made one slip (`silver_value = 10`) but reached the correct final 60.
- **Self-started work:** A-06 wrote a mini-program unprompted: `Pizza = 4 / soda - 10 / total pizzaparty = pizza +
  soda / print(pizza party) output # 68`. It shows curiosity and experimenting, but it copies the apples/oranges
  shape (no prices, spaces in names).
- **"Most experienced" is relative:** neither has a working concept of parameters or `return` yet.

### Typical misconceptions
- Parameter names are approximate labels (A-01 `attack`, `bonus` for `base_attack`, `bonus_multiplier`).
- Return the example's variable name (A-01 `return reslt`, from `double_number`'s `result`, while this function's variable is `total`), which raises a NameError.
- A function body uses the specific test values (A-06 `10 * 5`, `return 50`).
- Work totals out by hand instead of combining variables (both: 68).
- Copy the example's variable name (A-06 `player_name`).
- Spaces are allowed in variable names, and a template can be reused without adapting it (A-06 `total pizzaparty = pizza + soda`, `print(pizza party)`: adds counts with no prices, yet expects 68).
- Small arithmetic slips while tracing (A-06 `silver_value = 10`).

### Comfort and affect
Comfortable, independent and mildly impatient. A-01 shows work, revises (retraced `attack`), and wrote an honest
note about their own thinking: "not my favorite I just can't think of a character". They seem to dislike
open-ended creative prompts with no default more than they dislike Python. A-06 is curious and experimental:
an unprompted mini-program with an output comment (`# 68`). Neither shows anxiety. The risks are boredom on the
basics, and overconfidence that they "get" functions when their sheets show they don't yet.

### Needs
- Per-skill test-out of variables, arithmetic and tracing (A-01 3/3, 4.5/5, 5/5; A-06 2.5/3, 4.5/5, 4/5), so they don't redo what they already know.
- Focused instruction on what they almost have: exact parameter names and returning the right variable (A-01 `attack * bonus`, `return reslt`), and parameters instead of test values (A-06 `10 * 5`, `return 50`).
- Test-out checks that include the campaign's own idioms (dictionaries, functions stored as values, `return roll >= required_roll`), which their general comfort won't cover.
- "Let the code combine it" (both hard-coded 68) and naming rules (A-06 `pizza party`, `player_name`).
- Room to build: a sandbox, Trials from a blank file, advanced variants (A-06's unprompted mini-program).
- A default or a skip on open creative prompts (A-01: "not my favorite I just can't think of a character").
- Collapsible worked examples and story flavor, an instructions-light mode, and "why does this work?" sidebars.

### Frustrations and risks
- Mandatory repetition of variables and arithmetic they already handle.
- Long worked examples and click-through story text they can't collapse.
- An all-or-nothing test-out that either forces a whole module or skips functions entirely.
- Overconfidence: testing out of functions too early because the basics are solid, when their sheets show parameters and `return` aren't secure.
- Open-ended creative prompts with no default.
- Being turned into unpaid helpers for classmates when they finish early.
- Copying the nearest example under time pressure (A-01's `return result`) and never learning why it works.

### What their representative will fight for
1. A per-skill Quick Check test-out with a short "Mar'tu's notes" story recap, re-checked later.
2. Trials and advanced variants, including write-from-blank and refactoring challenges.
3. An instructions-light mode, and collapsible examples and flavor text.
4. A default answer for every creative prompt.
5. "Why does this work?" deep dives.
6. Honest gating: the test-out must include functions, exact names, dictionaries and campaign idioms.
7. An opt-in (never assumed) peer-mentor role.

### Persona brief
> I speak for the students who were most comfortable on the worksheet and worked on their own (sheets A-01, A-06). Nobody in this class has written a working function yet, me included. So "most experienced" here means solid basics and ready to move faster, not "already knows Python".
>
> What I can do: write variables the way the task asks (`character= "Zelda"`, `health= 100`, `power_up = "Fireball"`), with quotes on text. I can turn a word problem into code: 4 pizzas at 12, 10 sodas at 2. I traced the scoring function to the correct 60 and showed my work. One of us wrote a whole mini-program beside the prompt without being asked (`total pizzaparty = pizza + soda`, `print(pizza party)  # 68`).
>
> What I can't do yet: functions, quite. One of us wrote `total = attack * bonus` and `return reslt`. The names were close to the parameters `base_attack` and `bonus_multiplier` but not exact, and the return copied `result` from the example even though the variable was `total`. The other wrote the test numbers, `10 * 5` and `return 50`, instead of the parameters. I still typed 68 instead of `pizza_cost + soda_cost`. My own program had spaces in variable names and left out the prices.
>
> How it feels: comfortable, a bit impatient. One of us wrote "not my favorite I just can't think of a character". Open-ended creative prompts with no default slow me down more than the Python does.
>
> How I read instructions: I read the actual task, not just the example, and I show my work. When I'm unsure, I copy the nearest pattern and move on.
>
> What makes me zone out: redoing variables I already know; long worked examples I can't collapse; story text I have to click through; an all-or-nothing test-out.
>
> What delights me: a challenge from a blank file; side quests; seeing why something works; building my own thing.
>
> What I'll fight for: a quick per-skill check to test out of what I already know, with a short story recap so I don't miss the plot; Trials and advanced variants; an instructions-light mode; collapsible examples and flavor text; a default for every creative prompt; "why does this work?" sidebars. And I'll be honest: the test-out must still check functions, exact names, dictionaries and the campaign's tricks, because my sheet shows I'd skip them too early.

---

## Help caveats (how suspected help was handled)

1. **A-03 and A-04:** high suspicion of peer collaboration and joint goofing. They share the fast-food jokes,
   the 180/1000 counts, `* 0`, the `10 + 5` trace error, and the unusual "printed = bonus-line result + 15"
   method. Working together raised neither score, so both are placed in group 1 by their shared, weakest
   evidence. Each student's own floor is unknown and could be higher than shown (low effort, not only low skill),
   so confirm with the first in-app check.
2. **B-01:** medium suspicion, limited to Part 4, which is in another student's handwriting. The 5/5 trace is
   excluded. B-01 is placed on Parts 1-3 (5.5/11), which are in B-01's own block print and whose errors look
   authentic (unquoted strings, no `character =`, an abandoned function).
3. **B-02:** high suspicion. At least two hands appear on one packet, and the scans can't show which is B-02's.
   Placed by the weakest section (Part 3: test values, blank `return`) with low confidence. Recheck individually.
4. **B-03:** medium suspicion. The sheet is internally consistent, but the same hand appears on B-02's and
   B-01's packets, so B-03 may be the helper rather than the helped. Placed by the blank Part 3.
5. **A-05, A-07, A-08:** their identical Part 2 answer is a shared misreading that the worksheet's layout
   invites: the prices appear first, and the blanks are labeled "counts". A-07's and A-08's own planning notes
   confirm it. A-05's and A-07's matching hero value is a common pick. Low suspicion, no adjustment.
6. **A-02:** the late `Health = 100` may be a self-correction or a neighbor's hint. No adjustment.
7. **No help reached functions.** Nobody's Part 3 is correct, so Part 3 is the cleanest evidence across the class.

**Other limits:**
- These are 11 anonymous sheets from one worksheet.
- Parts 2 and 4 were heavily scaffolded (Part 4 supplies the arithmetic), so Part 4 scores overstate tracing skill.
- Some transcriptions are uncertain: A-02 low-medium; A-08 and B-01 medium.

Treat every placement as a provisional default and confirm it with a short in-app check. B-01 sits between
groups 2 and 3, A-08 between groups 1 and 2, and A-06 near the top of group 3. No student shows prior Python
experience, so "most experienced" is relative to this class. The test-out path still matters, for group 4 on the
early skills and for any future student who arrives knowing more.

## Class-wide patterns

1. **Functions are the cliff for everyone.** 0 of 11 wrote `total = base_attack * bonus_multiplier` / `return total`.
   - Seven filled the multiplication with literal numbers. Only A-06, A-07 and B-02 used the correct test values,
     10 and 5.
   - A-01 used approximate parameter names.
   - Three avoided it: A-05 and B-03 left it blank, and B-01 erased its only mark. B-02 also left `return` blank.

   The campaign needs parameters from the start (`perform_roll(die_size)`, and `add_spell(...)` with five parameters).
2. **Nobody let the code combine values.** Every student who reached 68 hard-coded it, and nobody wrote
   `pizza_cost + soda_cost`. The campaign depends on exactly this:
   `caster["max_mana"] - caster["mana"]` and `caster["mana"] = caster["mana"] - spell["mana_cost"]`.
3. **Only 1 of 11 (A-01) wrote the requested `character = ...`.**
   - Four copied the example's `player_name` (A-05, A-06, A-07, A-08).
   - Five wrote only a value with no `character =` (A-03, A-04, B-01, B-02, B-03).
   - A-02 wrote `def ("character")`.

   Students copy example identifiers and treat "make a variable" as "write the value". The campaign's
   instructions say "replace each placeholder with the matching parameter", so exact names matter.
4. **Reading beats writing.** Part 4 (the guided trace) was the strongest section. The common trace errors are
   still informative: adding the code's constants (A-03, A-04), returning the raw inputs (A-07), and not carrying
   the return value into the next variable (A-03, A-04). Read-before-write (predict, then run) suits this class.
5. **Quoting is inconsistent.** Text is unquoted on A-05, A-08 and B-01, and quotes are left unclosed on A-02,
   A-03 and A-04. The campaign's first edits are quoted strings (`party.move("left")`, `"option 1"`).
6. **Personalization and humor motivate strongly.** Students wrote Kratos and "Spartan Rage", Spiderman,
   Superman, first names, fast-food jokes and a joke name. Only A-01 disliked the open prompt and copied the
   example's "Zelda". Checks should accept any quoted value, and creative prompts need a default.
7. **Students want to write code.** Six of the 11 wrote code-like side work unprompted: A-06's mini-program,
   A-07's plan, A-08's drafts, and B-01/B-02/B-03's `Pizza=4 / Soda=10`. They reach for the last example they
   saw (A-06's and A-08's copies of the apples/oranges template).
8. **Collaboration is common** (A-03/A-04, and the shared hand in the B section). It didn't lift anyone above
   what the scaffolding gave. Design for legitimate pairing plus individual checkpoints.
9. **The worksheet's layout shaped some errors.** Listing prices before counts and labeling the blanks "counts"
   produced the shared A-05/A-07/A-08 error. An example that used a different variable name produced the
   `player_name` copies. Our modules should keep examples visibly distinct from tasks and label what each value
   means.
10. **Arithmetic is fine across the class** (3 x 10, 4 x 5, 48 + 20 = 68). The gap is what the Python means, not
    the math, so their confidence with arithmetic can be the bridge.
