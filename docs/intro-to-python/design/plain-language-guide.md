# Plain-language guide: Intro to Python, Units 1–5

This guide is for the strings pass, which rewrites every word a student reads in Units 1–5. Across Unit 1,
students said the directions were unclear. Every writer follows this guide, line by line.

The pass changes **words only**. §8 lists what has to stay exactly as it is, and §9 lists problems that need
site code or a change to an exercise's structure. Those are not for writers.

**Which document wins.** First `teacher-decisions.md`. Then this guide, for every student-facing word (it
replaces the parts of curriculum §2.9 listed in §5.1). Then `prototypes/FORMAT.md`, for every field the site or
the harness reads.

---

## The rules on one card

1. Write for a careful 8th grader who has never programmed and reads every word literally.
2. A step asks for one action and starts with the verb. It says where (the line and the exact text), and what the student sees when it worked.
3. Call things on screen by the names the screen uses: ▶ Run, your code, the Console, Your steps, Step 2, 💡 Help.
4. Define a new word before you use it: plain words, one analogy (from math class, English class or an earlier lesson), and one tiny example. All three go in Mar'tu's first paragraph, never only in a hover or under Another way.
5. Teach one new idea per exercise.
6. Where math or English class disagrees with Python (`=`, `x = x - 3`, `*` for ×, `( )`, `%`), say so out loud, and say where the comparison stops working.
7. Use one word per idea, from the word list (§5). Never use a word from a later lesson.
8. Put the plain instruction first and Mar'tu's joke after it. Keep stray or wrong numbers away from the task's number.
9. A check message says what happened, then the one thing to try, using the step's own names. Lean messages say only what went wrong and where. They never give the fix.
10. Every direction must match the code on screen: the right line, the right count, the right mistake.
11. Change words only. Leave alone the code, starters, the logic of checks, ids, the order of hints, and the phrases the site reads (§8).
12. Run the harness for your file prefix until it reports 0 errors. Then export and run the content test (§8.12).

---

## 1. Who we write for

- **8th graders, 13 or 14 years old, who had never programmed before this course.** They all played campaign
  Modules 1 and 2 and struggled. Many decided code is "a wall". This course rebuilds their confidence, so errors
  are normal, wins come early, and we never imply they should already know something.
- **Their reference points are English class, math class and the campaign.** Use them, and name them.
  - *Math class:* variables in algebra (x); `=` meaning "both sides are equal"; × and ÷; PEMDAS with parentheses;
    formulas (area = length × width); unit rate (miles per hour) and unit price; division with a remainder
    (50 ÷ 12 = 4 R 2); multiplication as repeated addition; the commutative property; "show your work"; number
    lines with a filled or an open dot; input–output tables; f(x).
  - *English class:* quotation marks for someone's exact words; a word talked about as a word ("'Lucky' has five
    letters"); compound words; syntax (how a sentence is put together); stage directions in a play script;
    outlines; sentence frames and Mad Libs; a teacher's note in the margin; looking a word up in a glossary.
  - *The campaign:* the cabin door (`move_left()`), Mar'tu's dialogue line, the four dialogue options, the trap-door
    skill checks, the spell book, the mana bars, and `cast_spell` holding the barrier. A callback looks back:
    "You've seen this. Now you'll get it."
- **How the four student groups read** (from the reps' reviews; never name a student):
  - *Starting from zero.* They stop at the first word they don't know, and they never open a hover or Another way.
    If the main text doesn't define a word, for them it is never defined.
  - *Right shape, wrong meaning.* They copy the nearest code shape and grab the story's numbers in reading order.
    They follow a message's example to the letter, even when it names the wrong box.
  - *Steady with a template.* They do exactly what the words say, so a direction that names the wrong line sends
    them to the wrong line. A frame with blanks works well for them.
  - *Ready to stretch.* They skip optional buttons and notice every contradiction. They are strong at math, so they
    read `=` as an equation and want to know why `mana = mana - 3` isn't impossible.
- **What this means for writers:** the meaning has to be in the main text (Mar'tu's first paragraph and the step),
  in plain words, matching the screen exactly.

---

## 2. Step text (checkpoint `text`)

Aim for about **grade 5–6**. The harness estimate should be 6 or lower (it warns above 9). A low score doesn't
prove a step is clear: "Make it three casts." scores below grade 0 and nobody can act on it. Test each step by
asking: *could a literal reader do this without guessing?*

1. **Start with the verb:** Change, Type, Delete, Add, Make, Press, Move. Debugging steps start with "Mend" (§8.5).
2. **Ask for one action.** If a step has to hold more than one action (this pass can't split steps, see §8), write a
   lead line and then number the parts, at most 3, one action each. The text must not start with a number,
   because the site numbers the steps.
   ```text
   Three moves, in order:
   1. Delete the `"` right after `Shield up.` and press Run.
   2. Read the box that appears in the Console.
   3. Put the `"` back, change the `.` to `!`, and press Run.
   ```
3. **Say exactly where.** Give the line number and the exact text to look for: "right above
   `print("Get inside, yes?")`", "just before the last `)` on your `print` line", "under `# B.`". Never write "it",
   "the end", "the story" or "above the code".
4. **Use the code's own words**, spelled as in the code: box names, the exact line, the exact mark. When there are
   two of something, say which one. Not "the last `"`" but "the `"` right after `Shield up.`".
5. **Check every step against the starter.** Is it the right line number? The right count ("six lines", not "four")?
   The right mistake ("take out `def`", not "the same way")? Is it the line where the fix goes, not just the line
   that prints?
6. **Something that is already true is not a step.** "Make sure line 1 starts with `companion = `" becomes
   "Keep `companion = ` as it is."
7. **Say what done looks like** when it helps: "You should see `Shield up!` in the Console."
8. **Name things on screen exactly** (table below). The first time in a lesson, say where the thing is.
9. **Goal-only steps** (`dictated=False`) give the goal, the names, and the kind of math in words ("times", "minus",
   "glue it with `+`"). They never give the finished line in backticks. Don't change `dictated`.
10. **Keep jokes, lore and extra numbers out of steps.** A story word the step needs gets a short gloss: "a coil
    (one roll of rope)".
11. **Projects keep their part letters** ("A.", "B.", "C."), which match the starter's `# A.` notes.
12. **Point only at what is on screen, and say where it is.** An exercise's Example has no Run button: write "Read the
    Example", never "Run the Example". "His sheet is in Mar'tu's words" becomes "the GEARSHIFT table at the end of
    Mar'tu's words". Data the step needs and the student can't see on a phone (Mar'tu's block is screens up) goes in
    the step: "store the other six gaps, 48 47 46 44 41 37".
13. **"The same way", "again", "shape" and "each with its own" are not directions.** Name the frame: the line to copy
    and what changes in each copy ("copy those two lines three times. In each copy, change every `oogrish` to that
    hero's sheet name"), or the pieces in order ("Glue four pieces with `+`: the name by its key, the text `": "`, ...").
    A blank editor gets the shape in words ("a `def` line that ends in `:`, then an indented `return` line").
14. **Say which line, every time.** "You never touched that line" reads as the line just changed: write "you never
    touched line 7". A step that edits in place names the line that holds the thing ("puts 47 at the position of the
    74 on line 3"), not only the empty line where the new code goes.

**Names on screen.** Use exactly these words.

| On screen | Write | Where it is |
|---|---|---|
| ▶ Run | the ▶ Run button, "press Run" | just above your code |
| (no label) | your code | where you type, with line numbers |
| Console | the Console | under your code: what `print` shows, and the box Python shows when it stops |
| Your steps, Step 1 (projects: Your tasks, Task 1) | Your steps, Step 2 / Your tasks, Task 3 | the list under Mar'tu's words |
| ✓ ● ○ ↺ | ✓ done, ● the step you're on, ○ still to come, ↺ was done, check it again | next to each step |
| 💡 Help (its rungs: Where to look, Teach me, Show me how, Start me off, More structure, Another way, Compare with Mar'tu's version) | the 💡 Help button | under the Console |
| Help options | Help options (settings, not hints) | top of the page |
| Names to use: | Names to use | under the heading Your steps |
| Can't decide? Mar'tu's pick: | the Mar'tu's pick button | next to Names to use |
| Example · not your task | the Example | under Mar'tu's words |
| Reset code | the Reset code button | on the same row as Run |
| Input for your program | the area labeled Input for your program | under your code (input exercises only) |
| Python's last line: / Show Python's full message | Python's last line | inside the box in the Console |

---

## 3. Mar'tu's explanations (`martu`)

Aim for about **grade 6–7** (harness estimate 7 or lower). **Word budget:** at most 60 words in Unit 1 lessons,
warm-ups included (curriculum lint f), at most 120 elsewhere, and never more than 230 (the harness warns). To make
room for the definition, the analogy and the example, cut story and jokes. Don't cut the explanation.

1. **Clarity wins.** Mar'tu stays kind, dry and short, but the plain idea and the instruction come first. A joke,
   the story or ", yes?" comes after them, or moves to a pass line or the "In Tor" angle.
2. **The first paragraph is all that "Keep it short" shows.** It has to hold the new idea, its analogy and its
   example. (A first line that ends with ":" keeps the fenced block under it.)
3. **Every new word gets three things before its first use:**
   - plain words for what it is or does;
   - one analogy from §6, from math class, English class or an earlier lesson, named out loud;
   - one tiny example in backticks.

   The pattern: "*Word* means …. In math class, …. In Python, …. `example`." A `[[glossary]]` link adds to the
   definition. It never replaces it.
4. **Teach one new idea per exercise.** Remind students of an old idea in a few words ("Quotes mean these exact
   letters.").
5. **Say where the analogy breaks, every time it matters.** `=` is not math's equal sign. `x = x - 3` is fine in
   Python. `*` is ×. `%` is not percent. Python is not a spreadsheet, and a comparison only helps if the student knows
   the thing: name one they use and what it does ("Python is not like Google Sheets, which updates by itself").
6. **Never explain with a later idea.** No "box", "value" or "name" in 1A. No "recipe" or "function" before Unit 3.
   In Units 1–2, "variable" appears only as "box (variable)".
7. **No stray numbers.** Don't put a wrong number in front of the right one ("He says 30. It is 3."), and don't put
   an extra number in front of the data ("at 3 in the morning").
8. **Define story words** the first time they appear in each lesson (§5.3).
9. **Mar'tu speaks for himself:** "My checks try other numbers", not "Mar'tu's checks".
10. **Build confidence.** Errors are normal and expected. Never write "just", "simply", "easy" or "obviously".
11. **The best analogy goes in the main text**, and the others stay under Another way. You may add one Another way
    per exercise with `angle="math class", label="From math class"` (or English class).
12. **Unit page intro (`martu_intro`):** under "Keep it short", the site hides any line that names a hero or ends
    in ", yes?", unless the line has code or a `[[link]]`. Keep the lines that teach free of hero names, or give
    them a code span.

---

## 4. Hints, error reading, check messages, quizzes, glossary, pass lines

### 4.1 Hints (the Help ladder)

The 💡 Help button shows hint 1 as **Where to look**, the middle hints as **Teach me**, and the last hint as
**Show me how**. **Start me off** is cut from the last hint (§8.4). Write each rung to do what its button says.

1. **Where to look** points at the place, and asks the question to ask there: "Look at `Fireball` on line 1. Does
   it have quotes around it?" It doesn't give the fix.
2. **Teach me** gives the idea in plain words and a tiny example. The example uses names that are not the task's.
   In new text, avoid `x`, `a` and `b`, which look like algebra.
3. **Show me how** gives the step's own finished line first, in backticks, then where it goes, using a place phrase
   (§8.4): "Write `mana = mana - spell_cost` above `print(mana)`."
4. **Unit 1's older ladders.** In Unit 1, hint 1 often says "Start the line with `…`" or "Start like this: `…`".
   Keep that sentence and its code span exactly, and put a plain where-to-look sentence in front of it. If Unit 1's
   last hint shows another program (`snack = "glug"`, `a = 9`, `print("Fine.")`), replace that example with the
   step's own line from the solution (§8.4b), then run the harness.
5. **A step that edits a line in place** (add a `"`, delete a mark, add a `#`): make the first code span in the last
   hint the mark itself, then the whole line: "Type `"` right after `up!`. Line 1 becomes `print("Shield up!")`."
   Then Help doesn't offer a useless Start me off.
6. **Spell out keyboard and editing moves**, as numbered parts after a lead line:
   - Select: drag across the line. Cut: Ctrl+X (Cmd+X on a Mac). Paste: Ctrl+V (Cmd+V). New line: click at the end
     of a line and press Enter.
   - Keys: `#` is Shift+3. `"` is Shift with the `'` key, next to Enter. `(` and `)` are Shift+9 and Shift+0. `_`
     is Shift with the `-` key. `*` is Shift+8. On a tablet, use the row of symbols under your code.
7. **In a debugging step, hint 1 teaches the reading routine** (§4.2). It no longer says "Read the last line first".
8. **One idea per hint, at grade 6 or lower.**

Before, a hint that stops halfway (top-to-bottom, step 1):
```text
Select the whole first line, `print("Get inside, yes?")`, and cut it.
```
After:
```text
Move it in four moves:
1. Drag across all of line 1 to select it.
2. Press Ctrl+X (Cmd+X on a Mac) to cut it.
3. Click at the end of the last line and press Enter.
4. Press Ctrl+V (Cmd+V) to paste it there.
```

### 4.2 Reading an error: one routine everywhere

When Python stops, the Console shows a box with four parts:
- a **title** saying what went wrong in plain words ("Missing quote");
- a line saying what to try;
- **Python's last line**, which says the same thing in Python's own words;
- **Show Python's full message**.

Teach this routine everywhere (Mar'tu, hints, takeaways, the glossary, the Chalk Notes), in this order:
1. Read the title at the top of the box. It says what went wrong.
2. Read *Python's last line*. It says the same thing in Python's words, and in the campaign it is all you get.
3. Find the line number and fix that line. Press Run again.

Replace "Read the last line first. Then look at the line it names." with this routine. In Python's *full* message
(and in the campaign), the last line is still the one to read first. Unit 2's When Spells Fizzle says so.

Two things keep the routine true for a literal reader:
- **When Python's last line guesses wrong**, the box says so, right after what happened: `74 = 47`, `"name" = "Lucky"`
  inside a sheet and `hour_2 = 48, hour_3 = 47` all get "Maybe you meant '=='", so the box adds "Python's last line
  guesses `==`, but that guess is wrong here." The fixed line stays last.
- **The banner names the line the fix goes on.** When the mistake is on another line than the one Python stopped at
  (the value with no name on line 4, above `print(hero)`), it says "The mistake is on line 4." When the fix goes above
  but no line can be named (a box no line makes yet), it says "The mistake is on line 5 or a line above it."

### 4.3 Check messages (the assert message strings)

1. **Start with what happened to their line**, in plain words: "Line 4 is just `"Lucky"` on its own." Don't start
   from the checker's point of view ("Mar'tu's check tried …"), and don't praise a step that fails ("Your line
   prints the right words …").
2. **Then give the one thing to try, using the step's own names:** "Put `hero = ` in front of it." Never offer a
   choice of fixes ("Delete it, or …"). Never use another step's box ("like `armor_bonus = "Telegun"`"). Never give
   a general shape the student will copy ("put a name and `=` in front").
3. **Evidence goes last, and gets a label.** A value the check made up is "a test number" or "a made-up name":
   "Mar'tu tested your line with a made-up name, Tester. Don't type Tester." Never start with a number the student
   might copy.
4. **Say it when they typed the answer:** "You typed the answer, 11, instead of the math." If their line has numbers
   where the box names should be, add: "Use the box names, not numbers."
5. **Keep it short:** about 35 words, three sentences at most, no remarks in parentheses.
6. **Never end a message with a raw Python error.** Say in plain words what stopped the code ("it stopped because
   a name is spelled differently"). Fixing a builder that pastes the raw error needs a logic change: see §9, S8.
7. **Lean messages** (every Quick Check item, and every SOLO item from Unit 2 on) say what is wrong and where, with
   evidence. They never give the fix, the line to type or the operation: "`max_mana` still holds the placeholder 0."
8. **Use the quotes sentence word for word**, and only where a box name is involved: *Quotes mean these exact
   letters. No quotes means look inside the box with this label.*
9. **Never repeat a student's own creative value** (a hero they chose). Quote only the starter's text and the
   task's own values.
10. **Name the slip they really made, and never contradict the screen.** A line with brackets around the join does
    join the lists, so "doesn't join the two lists yet" is false: "Your line puts square brackets around the join".
    The class's common slips get their own branch: a box's name in quotes ("Your line shows the word watch_keeper,
    because of the quotes"), a list retyped, a number typed in.
11. **A line that is right so far but stops early** says so, then the next thing to type: "Your line stops after
    `Lucky has`. Now add the mana: ...". Never "a space is missing" for the space the next piece brings.
12. **Evidence needs no math to read.** Name one test number and the answer it should give: "Mar'tu tested it with a
    test affinity of 4 for Gearshift: the max should be 8, but it stayed 20." Not four test numbers for four heroes.
13. **Say what Python's words mean.** `None` is "`None`, Python's word for nothing", with why it came back ("no
    `return` line hands a number back"). No idioms in messages either ("`print` and all", "74 and all").

Before (glue-words, step 1):
```text
Mar'tu's check tried your code with `name = "Tester"` (only inside the check: leave your own numbers as they
are). This time, your program should print a line that starts with `Tester has`, but it printed `Lucky has`.
```
After:
```text
Your line says Lucky because the name is typed in. Use the box instead: `print(name + " has ")`.
Mar'tu tested your line with a made-up name, Tester, and it still said Lucky. Don't type Tester.
```

### 4.4 Quiz questions (`q`, `explain`, `why_wrong`, mc choices)

1. Put everything the question depends on into the question itself. Example: "Mar'tu had 3 lanterns, and the total
   was 22. Now he changes `lantern_count` to 5. Which `total` line still gives the right answer without anyone
   retyping it?"
2. Ask one thing per `q`, and say what "right" means ("still gives the right answer", not "stays right").
3. `explain` gives the reason in one or two sentences, with the analogy if there is one. `why_wrong` says, in plain
   words, what that choice would do.
4. You may reword mc choices that are plain words. Never change predict choices (they are output), choices that are
   code, `answer`, or the order of the choices.
5. Quiz titles and summaries say what the item is: "Quick review: 2 questions, not scored", not
   "Mar'tu remembers…".

### 4.5 Glossary (`plain`, `example`)

1. `plain` is one or two sentences, at grade 6 or lower. Start with what the thing is, in everyday words, then give
   the math or English link if there is one ("the same marks you use in math class").
2. Don't use another undefined term inside a definition.
3. `example` is tiny, and its names are different from the tasks' names.
4. Renaming a term: see §8.9.

### 4.6 Pass lines (`pass_line`)

1. Write one line. Say plainly what they just did, then add Mar'tu's flavor if there's room.
2. Never promise something that won't happen. "Now watch this." is wrong when the next step is theirs to do. If it
   is, say so: "Next: change one number and watch the total change."
3. Don't put `[[links]]` in pass lines. They show as plain words.
4. A SOLO pass line keeps "You did that on your own." exactly (§8.7). Remove "On your map:", because there is no map
   on screen yet (§9, S10).

### 4.7 Other prose

- **`goals`:** what students will be able to do, in words they know on day one. No code they can't read yet.
- **Titles** say what the item is: "Numbers don't get quotes", not "Numbers stand alone". Give each side quest its
  own title instead of "What's in it for me?", which is also the label on the campaign box.
- **`summary`, `intro`, article `body`:** the same rules as Mar'tu. Say where the story's numbers are ("in the story
  at the top of the page").
- **`takeaway`:** one line that gives the rule in plain words.
- **Predict `q` and `explain`:** don't hide a task in them. "Now add `print(48 / 2)` and run" becomes "Try it if
  you like (it's not a step): …".
- **`pair_talk`:** it shows above Mar'tu's Example, so name where the thing to talk about is ("the Predict first box,
  just above ▶ Run"), and never add a task in it ("Then both add `print(48 / 2)`").
- **Another way:** labels are plain words with no `[[links]]`. Every angle follows §3.
- **Chalk Notes** (cheatsheet `concept`, `note`): translate Python's words. *Syntax* means grammar, `str` means
  text, `int` means a whole number, *concatenate* means glue.

### 4.8 The error box (site code: `explain.ts`)

The box Python's crash opens follows §4.3 too, and the same reps read it literally:
1. **One fix, from the step's own names.** Never "If it's a box, use `armor_bonus`. If it's text, put quotes" when
   Mar'tu's version shows which (`weapon = "sword"`). A note step gets the `#` fix; a step that shows words gets
   `print("...")`.
2. **Never a fix from a later lesson** ("write the recipe with `def`" for `append(33)`): `.append()` needs the list's
   name and a dot in front.
3. **Never a code example that is wrong when copied as it reads**: `chalk_wall = "value"` replaces the whole wall, and
   `hour_2 = 48, hour_3 == 47` is nonsense.
4. **Never send a student hunting for what isn't there.** "Look for a missing quote or a missing parenthesis" on
   `lantern_count lantern_price`, `chalk_wall = [] 48, 48` or `_ - =` gets the row for that slip: two names side by
   side (algebra's LP), items after the `]`, marks with no `print` and no quotes.
5. **Translate Python's words**: never leave `NoneType` as the explanation (`print(...) + more` gets "the pieces after
   the `)` that closes `print( )` are outside it").

---

## 5. Word list

### 5.1 Decisions that change earlier wording

| Was (curriculum §2.9 or current text) | Now | Why |
|---|---|---|
| "show your working" | **show your work** | what US math teachers say |
| "brackets" for `( )` | **parentheses `( )`** | math class says parentheses (PEMDAS); there, "brackets" means `[ ]` |
| "round brackets", "curly brackets" | **parentheses**, **curly braces `{ }`**; `[ ]` stays **square brackets** | the same reason |
| "mend", "slip" in directions | **fix**, **mistake** | everyday words. "Mend" stays only where the site needs it (§8.5) and is defined once |
| "Read the last line first" | the three-part reading routine (§4.2) | the title in the error box already says it in plain words |
| "label (key)" | **tag (key)**, never "label" | the teacher's Unit 5 ruling |
| "follows" (meaning "updates by itself") | **changes to match when you press Run again** | Python is not a spreadsheet |
| "checkpoint" | **step** (in projects, **task**) | what the screen says |
| "a value with no box … made it and forgot it" | **a value with no name in front: Python reads it and throws it away** | a clear picture |

### 5.2 One word per idea

| Idea | Our word | The first time, write | Don't write |
|---|---|---|---|
| where answers appear | the Console | "the Console, the box under your code where Python's answers appear" | below, the output, the console (as in a game console) |
| where you type | your code | "your code (where you type)" | the editor, the starter |
| what an exercise starts with | the code that's already there; "line 3" | — | the starter, the starter's words |
| `print` | show on the screen | "In Python, *print* means show on the screen, not on paper." | — |
| text in quotes | text | "Text in quotes is called a *string*: letters strung together like beads. This course mostly says *text*." | words (for digits or marks), letters |
| variable | box (variable) in Units 1–3; variable from Unit 4 on (Mar'tu may still say box) | "A box (a variable) keeps a value under a name." | jar, slot, container (keep those for Another way) |
| a box's name | name | "`companion` is the box's name, like a label stuck on the box." After that, always "name". | label (except in the quotes sentence) |
| what a box holds | value | "the value: what goes in the box, text in quotes or a number" | data, contents |
| `=` | gets | "Read `=` as *gets*." | equals, is |
| `==` | is the same as | — | equals |
| `( )` / `[ ]` / `{ }` | parentheses / square brackets / curly braces | "parentheses `( )`, the same marks you use in math class" | brackets, round brackets, curly brackets |
| a mistake | mistake | — | slip (Mar'tu's word; define it once), crash |
| Python stops | an error, the error box | "When Python can't run a line, it stops and shows an error in the Console." | crash, break (except "break it on purpose") |
| a mistake in code, as programmers say | bug (from `broken-spell-1c` on) | "A *bug* is a mistake in code. A loud bug makes Python stop. A quiet bug runs, but gives a wrong answer." | — |
| to fix | fix | debugging steps say "Mend"; define it once: "*Mend* means fix." | mend (anywhere else) |
| `+ - * /` | plus, minus, times, divided by | "`*` means times (there's no × key). `/` means divided by." | star, the sums |
| math in general | math, "the math" | — | sum (for anything but adding), sums |
| combining boxes | the operation itself: add, subtract, multiply, glue | — | combine, "build it from" (on their own) |
| an answer typed as a fixed number | a typed-in answer | "a number you worked out yourself and typed in, instead of the math" | typed by hand, hard-coded |
| a value the check made up | a test number, a made-up name | — | an unlabeled number |
| the check runs the code again | Mar'tu tests your line with other numbers | "like testing a formula in math with other numbers" | sneaky, keeps up |
| changes after an edit | changes to match (after you press Run again) | — | follows |
| `+` with text | glue (join) | "`+` glues text, like a compound word." | concatenate |
| `"█" * 3` | stamp (repeat) | "`*` repeats text, like a stamp pressed 3 times." | multiply text |
| a `#` line | note (comment) | "A line that starts with `#` is a note for people (a comment)." | — |
| triple-quoted text | text over many lines | — | note, chalk note, slate |
| a step | step (task in projects) | — | checkpoint |
| what Help gives | Where to look, Teach me, Show me how, Start me off, More structure | — | "a starting line", "more structure" with no explanation |
| what `def` makes | recipe (function), from Unit 3 on | — | recipe or function before Unit 3 |
| parameter / argument | ingredient (parameter) / what you hand over (argument) | — | argument on its own |
| return | hands back (returns) | — | — |
| calling a recipe | call it: run it by its name with `()` | — | invoke, execute |
| condition | question | — | condition |
| block | the indented lines under it | — | block (fine as a glossary link) |
| index | position (index) | "A position counts from 0, like a ruler." | index on its own, element |
| list member | item | — | element |
| dictionary / key | sheet (dictionary) / tag (key) | "A dictionary keeps a tag on every value. Python calls the tag a key." | label, map |
| where `input()` answers come from | the area labeled Input for your program | — | "the Input box" (box means a variable) |

### 5.3 Story words: define each one on first use in a lesson

| Word | Plain gloss |
|---|---|
| mana / max mana | a hero's magic power, and the most they can hold |
| magical affinity | how strong a hero's magic is |
| cast | use a spell once; each `mana = mana - spell_cost` line casts it once |
| burst | a blast from the leylines; the barrier has to hold until the next one |
| gap / shrink | the hours between two bursts / the gaps getting shorter |
| chalk wall | Mar'tu's wall of gap numbers |
| ledger | a notebook where you write down what things cost |
| satchel | a shoulder bag |
| familiar | a wizard's animal helper, like an owl |
| coil | one roll of rope |
| flask | a small bottle (of lantern oil) |
| glug / canteen | Lucky's drink / his water bottle |
| status line | one line showing a hero's name and mana, like the stats text in a game: `Oogrish: 18/18 mana` |
| ward sign | a sign that protects the barrier post |
| barrier, Ley Clock | the shield around the cabin, and the clock that counts down to the next burst |

### 5.4 Words to avoid in student text

- **British or old-fashioned:** brackets for `( )`, sums, show your working, practises, ticked, mark (for a grade),
  squared paper (say graph paper), queue, till, rub out, register, "ground floor is floor 0".
- **Idioms that hide the meaning:** stand alone, made it and forgot it, stays quiet, keep up, follows, set again,
  a mark against you, the line it names.
- **Programmer words** (the error box translates them when Python's message shows one): literal, concatenate,
  operator, operand, boolean, iterate, mutable, object, attribute, scope, parse, execute, increment, edge case,
  callable, subscriptable. *Syntax* is fine once it is linked to English class.
- **Words that suggest students should already know:** just, simply, easy, obviously.

---

## 6. Analogy bank (Units 1–5)

Each entry gives: what to say, the analogy and what it connects to, where the analogy breaks (say that too), and
where the idea is first taught (`unit · lesson · exercise id`). Use the first analogy in Mar'tu's main text, and
keep the others for Another way.

**1. `print`, Run and the Console**
- *First taught:* U1 · Before the First Spell · `what-an-error-looks-like`; taught properly in U1 · Words in Quotes · `press-run`.
- *Say:* "`print` tells Python to show something in the Console, the box under your code."
- *English:* a play script. Your code is the script, Run is "Action!", and the Console is the stage, where only the
  spoken lines show.
- *Earlier:* the campaign's Run button.
- *Breaks:* print has nothing to do with a paper printer. Python shows only what you `print`, and it never shows the
  quote marks. A person skips a line they can't read, but Python stops.

**2. Top to bottom**
- *First taught:* U1 · Words in Quotes · `top-to-bottom`.
- *Say:* "Python reads your code like a page in a book: the top line first, then down, one line at a time."
- *Breaks:* until `if` (Unit 2) and recipes (Unit 3), nothing jumps. Don't use a ladder for this, because you climb a
  ladder from the bottom.

**3. Notes (`#` comments)**
- *First taught:* U1 · Words in Quotes · `notes-for-humans`.
- *Say:* "A line that starts with `#` is a note for people. Python skips it."
- *English:* stage directions in a play script. The actors read them but never say them out loud.
- *Breaks:* a `#` at the end of a line skips only what comes after it (`lantern_count = 0  # how many?`). A `#`
  inside quotes is just a mark.

**4. Text in quotes (strings)**
- *First taught:* the word, U1 · Words in Quotes · `press-run`; why quotes matter, `words-need-quotes`.
- *Say:* "Quotes mean these exact letters. Python shows exactly what's between them."
- *English:* quotation marks around someone's exact words, every letter and comma. A word talked about as a word:
  "'Lucky' has five letters."
- *The name "string":* letters strung together like beads on a string.
- *Breaks:* curly quotes (“ ”) from Google Docs or a phone break the code. An apostrophe inside `"..."` is fine, the
  way an apostrophe inside a quotation is fine in English. `"3"`, `"█"` and `" "` are text too. Without quotes,
  Python looks for a name it should already know, finds none, and says *not defined*.

**5. Errors and the error box**
- *First taught:* U1 · Before the First Spell · `what-an-error-looks-like`; the full traceback, U2 · When Spells Fizzle · `anatomy-of-a-fizzle`.
- *Say:* the reading routine (§4.2).
- *English:* a teacher's note in the margin of a draft. It points to the spot, and it isn't a grade. *Syntax* is
  how a sentence is put together: a SyntaxError is a line Python can't read. A NameError is like "She grabbed it"
  when the story never said who "she" is.
- *Math:* a TypeError is like adding 5 meters to 3 seconds.
- *Breaks:* Python never guesses what you meant. It reports one error at a time, and a new error means it got
  further, which is good news. The line it names is where it *noticed* the problem, so also check the line above.
  No error doesn't mean the code is right (spell-check doesn't catch "their" for "there"): see entry 6.

**6. Mend, slip and bugs (loud and quiet)**
- *First taught:* mend and slip, U1 · Words in Quotes · `close-the-quote`; bug, U1 · Math and Glue · `broken-spell-1c`.
- *Say:* "*Mend* means fix, the way you mend a small tear in a sleeve. A *slip* is a small mistake. A *bug* is a
  mistake in code. A loud bug stops Python with an error. A quiet bug runs but gives a wrong answer."
- *Breaks:* a quiet bug only shows up when you test with other numbers (entry 12).

**7. Boxes (variables) and `=`**
- *First taught:* U1 · Boxes With Labels · `label-a-box`.
- *Say:* "A box keeps a value under a name. `companion = "Gearshift"`: companion gets Gearshift."
- *Math:* a letter like x stands for a number, and math teachers say "define your variables" ("Let L be the number of
  lanterns"). A box is that "let" line.
- *English:* introduce a character before you write about them.
- *Earlier:* in `words-need-quotes`, Python looked for "a name it should already know". Now you make one.
- *Breaks:* in math, `=` says both sides are equal, and you can flip them. In Python, `=` goes one way: work out the
  right side, then put it in the box on the left. `3 = x` is an error. Algebra writes 5P, but Python needs `5 * P`.
  A box always holds a known value, and it gets that value before any line uses it.

**8. Changing a box**
- *First taught:* U1 · Boxes With Labels · `change-the-box`.
- *Say:* "A box holds one value at a time. A new `=` wipes the old value."
- *Analogy:* a small whiteboard: write 26, wipe it, write 21.
- *Math:* x = 26 and x = 21 can't both be true, but in Python they happen one after the other.
- *Breaks:* lines above the change already ran with the old value. Change the number where the box is first made,
  not lower down.

**9. Exact names**
- *First taught:* U1 · Boxes With Labels · `exact-names`.
- *Say:* "Names match letter for letter, capitals too. No spaces: use `_`."
- *Analogies:* a password with one wrong capital doesn't open your account. In English, capitals change meaning
  too (Polish and polish).
- *Earlier:* the game looked for `move_left` exactly at the cabin door.
- *Breaks:* Python never guesses a close name.

**10. Numbers and text: `3` and `"3"`**
- *First taught:* U1 · Boxes With Labels · `numbers-stand-alone`.
- *Say:* "A number gets no quotes, and Python can do math with it. Anything in quotes is text."
- *Math:* a jersey number or a locker number is a name, and nobody adds two jerseys. Points in a game are an amount.
  Ask: "Would I ever do math with this?"
- *Breaks:* mixing the two often gives no error: `"3" + "4"` is `34`. `input()` always hands back text. Don't compare
  it to a price tag, because a price is an amount.

**11. Math signs and order of operations**
- *First taught:* signs, U1 · Math and Glue · `chalk-math`; parentheses, `repeat-a-mark`; `**`, `//` and `%`, U1 · Clock Math.
- *Say:* "`*` means times and `/` means divided by. Python uses PEMDAS: parentheses first."
- *Breaks:* the keyboard has no × or ÷. `2 ^ 3` quietly gives 1 (use `**`). Only `( )` group math: `[ ]` and `{ }`
  mean something else in Python. `2(3 + 4)` is an error, so write `2 * (3 + 4)`. `/` always gives a decimal:
  `48 / 2` is `24.0`.

**12. Use the box names, not the answer**
- *First taught:* U1 · Math and Glue · `chalk-math` (the test); `let-the-code-combine` (show your work).
- *Say:* "Write the math with box names and let Python work it out. I test your line with other numbers."
- *Math:* a formula. area = length × width works for any rectangle, but the answer 12 only works for one. In math
  class, "show your work".
- *Everyday:* an online cart recalculates from quantity × price when you press Update. Run is your Update button.
- *Breaks:* Python is not like Google Sheets, which updates by itself. The total changes only when you press Run
  again, and only lines below the change see the new number.

**13. How many? How much is one?**
- *First taught:* U1 · Math and Glue · `what-each-number-means`; per hour, U1 · The Night Watch Ledger.
- *Say:* "Ask every number: is it how many, or how much is one?"
- *Math:* unit price, and a ratio table (1 lantern → 4 coins, 3 lanterns → 12 coins). "Per hour" is a unit rate,
  like miles per hour. cost = count × unit price.
- *Breaks:* the commutative property (`broken-spell-1c`): 2 × 5 = 5 × 2, so swapped boxes can still print the right
  total. The boxes still mean the wrong things, and the next change goes wrong.

**14. `mana = mana - spell_cost`**
- *First taught:* U1 · Math and Glue · `spend-mana`.
- *Say:* "Python works out the right side first, with what's in the box now (26 − 3 = 23), then puts the answer back
  in the box. Mana gets mana minus spell cost."
- *Math:* x = x − 3 has no answer in algebra. Python's `=` isn't a math statement.
- *Everyday:* a bank balance: new balance = old balance minus what you spent.

**15. Gluing text: `+` and `str()`**
- *First taught:* U1 · Math and Glue · `glue-words`.
- *Say:* "`+` has two jobs. Between numbers it adds. Between texts it glues."
- *English:* compound words: "sun" + "flower" is "sunflower", with no space.
- *About `str()`:* `str` is short for string, Python's word for text. `str(26)` gives `"26"`.
- *Breaks:* `+` adds no spaces, so put them inside the quotes. Text + a number is a TypeError. `str(mana)` makes a
  text copy and leaves the box alone. `print(a, b)` with commas adds spaces; accept it if you see it, but teach `+`.

**16. Repeating text: `*`**
- *First taught:* U1 · Math and Glue · `repeat-a-mark`.
- *Say:* "`"█" * 3` means `"█" + "█" + "█"`: `███`."
- *Math:* multiplication is repeated addition (3 × 4 = 4 + 4 + 4). A mana bar is a tape diagram: the filled part
  plus the empty part make the whole.
- *Breaks:* you can repeat text, but you can't subtract or divide it. The number has to be a whole number.

**17. Text over many lines (`"""`)**
- *First taught:* U1 · Extra practice: Words and boxes · `many-lines-at-once` (optional); used in The Ward Sign.
- *Say:* "Three quote marks start text that can go over many lines. Three more end it."
- *English:* a poem keeps its line breaks.
- *Breaks:* this is not a `#` note. Python prints it.

**18. `//` and `%`**
- *First taught:* U1 · Clock Math (article) · `where-is-the-hand`.
- *Say:* "`50 // 12` is the 4 and `50 % 12` is the 2 in 50 ÷ 12 = 4 R 2."
- *Math:* long division with a remainder. A wall clock wraps around: 3 hours after 11 o'clock is 2.
- *Breaks:* `%` is not percent.

**19. `input()` and `int()`**
- *First taught:* U1 · Asking the Traveler (article) · `who-goes-there`.
- *Say:* "`input()` asks and waits. The answer is always text. `int()` turns it into a whole number."
- *Math:* `int` is short for integer.
- *Everyday:* a paper form holds only writing.
- *Breaks:* `int("3.5")` is an error.

**20. Comparisons, `True` and `False`**
- *First taught:* U2 · True or False, Yes? · `true-or-false`, `ask-with-double-equals`, `enough-to-pass`.
- *Say:* "A comparison is a yes-or-no question. Python answers `True` or `False`. Read `==` as *is the same as*."
- *Math:* substitution, as in "is x + 3 > 8 true when x = 6?" Number lines: `>=` is the filled dot (the number
  counts) and `>` is the open dot.
- *Breaks:* a single `=` is not a question. ≥ is typed `>=`, with the `=` last. Text must match exactly, capitals
  included. `True` has a capital letter and no quotes.

**21. The dot: `.lower()` and other tools**
- *First taught:* `.lower()`, U2 · `any-case-answer`; `.capitalize()`, U3 · `store-then-pass`; list tools, U4; `.get()`, U5 · Keys and .get().
- *Say:* "The dot asks the text to do something: `line.lower()` means *line, give me a small-letter copy*."
- *English:* speaking to someone directly ("Line, give me …").
- *Everyday:* Google Docs' Format → Capitalization.
- *Breaks:* text tools hand back a copy, so `line.lower()` on its own keeps nothing. List tools (`.append()`,
  `.sort()`) change the list itself. Never read the dot as "'s".

**22. `and`, `or`, `not`**
- *First taught:* U2 · If the Clock Turns Red · `and-or-not`.
- *Say:* "`and` needs both answers True. `or` needs at least one. `not` flips the answer."
- *English:* "You may leave when your work is done *and* your desk is clean."
- *Math:* a compound inequality, 2 ≤ hours ≤ 12.
- *Breaks:* in English, "soup or salad" means only one, but Python's `or` is also True when both are. `roll == 1 or 20`
  is always True, so write `roll == 1 or roll == 20`.

**23. `if`, `elif`, `else`**
- *First taught:* U2 · If the Clock Turns Red · `first-if`, `otherwise`, `clock-colors`.
- *Say:* "`if` asks a question. Its indented lines run only when the answer is True. `else` means *otherwise*."
- *School:* a grading scale. Check from the top and stop at the first True, so order matters.
- *English:* choose-your-own-adventure books ("If you open the door, turn to page 12").
- *Earlier:* the campaign's four dialogue options.
- *Breaks:* the question always comes first and ends with `:`. `else` has no question. Separate `if` lines can all
  run; `elif` picks one.

**24. Colon and indent**
- *First taught:* U2 · If the Clock Turns Red · `colon-and-indent`.
- *Say:* "The `:` says *here come its steps*. The indented lines under it belong to it."
- *English:* an outline. A main point (I.) has its sub-points (A., B.) indented under it. A colon introduces a list.
- *Breaks:* every line in the group needs the same 4 spaces. The steps go on the next lines. A heading with nothing
  under it is an error.

**25. `import random` and `randint`**
- *First taught:* U2 · If the Clock Turns Red · `roll-a-die`.
- *Say:* "`random.randint(1, 6)` rolls a fair die: any whole number from 1 to 6, both ends included."
- *Math:* a fair die, where every face is equally likely. `import random` is like fetching the dice bin from the
  shelf, once, at the top.
- *Breaks:* `randint` includes both ends, but `range` and slices leave the end out (entry 30). In everyday talk
  "random" means weird; here it means equally likely.

**26. Recipes: `def` and calling**
- *First taught:* U3 · Recipes With Names · `box-or-recipe`, `call-it`; `pass`, `replace-pass`.
- *Say:* "`def` writes a named recipe. Nothing happens until you call it by name with `()`."
- *Math:* f(x) = 2x is the definition, and f(13) works it out.
- *Science or English:* writing a lab procedure doesn't do the lab. `pass` is a blank recipe card holding the spot.
- *Breaks:* a recipe has no `=` (`def double(x) = x * 2` is an error), and `2x` must be written `2 * x`. The recipe
  has to come above the line that calls it. The name without `()` runs nothing.

**27. Ingredients (parameters) and what you hand over (arguments)**
- *First taught:* U3 · Recipes With Names · `ingredients`, `fill-the-ingredients`, `use-the-ingredients`.
- *Say:* "An ingredient is a named blank in the recipe. Each call fills it."
- *English:* Mad Libs and sentence frames ("____ (hero), get inside!").
- *Math:* the x in f(x), and an input–output table.
- *Breaks:* use the blank's name inside the recipe, never one call's number. Values fill the blanks in order. In
  English class an "argument" is a claim with reasons, so never write "argument" on its own.

**28. Hands back (`return`) and `None`**
- *First taught:* U3 · Recipes With Names · `send-it-back`, `be-the-ledger`, `store-then-pass`.
- *Say:* "`return` hands a value back to the line that called. Catch it in a box, or it's gone."
- *Math:* the function machine. The call is replaced by its output, the way 26 replaces f(13).
- *School:* `print` says the answer out loud, and `return` writes it on the answer sheet.
- *Breaks:* a recipe with no `return` hands back `None`, which is not 0. `return` ends the recipe at once. Printing is
  not returning.

**29. Lists and positions**
- *First taught:* U4 · Many Values, One Name · `make-the-wall`, `first-is-zero`, `new-chalk-mark`, `how-long`, `lists-inside-lists`.
- *Say:* "A list keeps many values under one name, in order. A position counts from 0."
- *Math:* a data set. A ruler starts at 0, so position 0 is no steps from the front.
- *English:* "seven" is how many and "seventh" is which one. The seventh item is at position 6. *Append* shares a
  root with *appendix*.
- *List inside a list:* a theater ticket, row first, then seat.
- *Breaks:* say "position 0", never "zeroth". There is no `-0`: counting from the end starts at `-1`. `[ ]` makes or
  reads a list, and never groups math.

**30. `range()` and slices**
- *First taught:* U4 · Reading the Wall Closely · `range-of-marks`, `slice-the-wall`.
- *Say:* "`range(1, 7)` counts from 1 and stops before 7. `wall[2:5]` copies positions 2, 3 and 4."
- *Math:* a number line with a filled start and an open end (1 ≤ n < 7). The step is skip counting.
- *English:* a slice is an excerpt: you quote some lines, and the poem doesn't change.
- *Breaks:* "pages 2 to 5" includes page 5, but Python leaves the end out. In math, "range" means biggest minus
  smallest, so define the word first.

**31. Sorting and more list tools**
- *First taught:* U4 · `sorted-or-sort`; More List Tools · `insert-and-pop`, `remove-and-in`, `biggest-and-smallest`.
- *Say:* "`sorted(wall)` hands back a sorted copy. `wall.sort()` sorts the list itself and hands back nothing."
- *Everyday:* photocopy the list and rearrange the copy, or rearrange the original.
- *Breaks:* `.remove()` takes a value, and `.pop()` takes a position.

**32. Tuples and `zip()`**
- *First taught:* U4 · Tuples (article) · `cabin-on-the-map`; zip() (article) · `spell-colors`.
- *Say:* "A tuple is a pair that stays put. `zip()` pairs two lists, first with first."
- *Math:* an (x, y) point on a coordinate plane: two values, in order, that go together.
- *Everyday:* a zipper's teeth.
- *Breaks:* the `( )` here makes a tuple, not grouped math.

**33. Dictionaries: tags (keys) and values**
- *First taught:* U5 · Stat Sheets · `make-a-sheet`, `read-by-key`, `key-errors`, `is-it-in`, `key-from-a-box`.
- *Say:* "A dictionary keeps a tag on every value. Python calls the tag a key. You look a value up by its tag."
- *English:* the glossary at the back of a textbook: you look up the word, not entry number 3.
- *Math:* a two-column table where each input appears once.
- *Earlier:* `caster["mana"]` in the mana bars.
- *Breaks:* each key has one value, so writing it again replaces the old one. Python needs the exact spelling, or it
  gives a KeyError. `in` checks keys only. Tags are text, so they get quotes. Write `hero["mana"]`, never
  `hero.mana`, and say "hero, look up mana" rather than "hero's mana". `book[spell_name]` looks inside the box;
  `book["spell_name"]` looks for those exact letters.

**34. Sheets inside sheets**
- *First taught:* U5 · Sheets Inside Sheets · `abilities-inside`, `the-roster`.
- *Say:* "Read one step at a time, outside first."
- *English:* a table of contents: chapter, then section, then page.
- *School:* a class roster: the row (a position), then the column (a tag).
- *Breaks:* English says it inside out ("the wisdom on Bomb Shell's card"). Lists take positions and dictionaries
  take tags.

---

## 7. Before and after (from the student reps)

**1. Unit goals** (the `UNIT` dict; copy it the same into u01a–u01d)
```text
Before: Put a new value in a box, like `mana = mana - cost` / Glue text together with `+` and `str()`, and draw a
        bar with `"█" * mana` / Read Python's message and mend the slips everyone makes
After:  Make Python show words on the screen / Write notes that Python skips / Keep words or a number in a named
        box (a variable) / Change what is in a box / Let Python do the math with your boxes / Join words and
        numbers into one line, and draw a mana bar from blocks / Read Python's error messages and fix small mistakes
```

**2. How Mar'tu Teaches** (u01a article body)
```text
Before: Stuck? Press Help. You can always ask for a starting line or more structure.
        Checkpoints: ✓ done · ● now · ○ next.
After:  Type your code, then press ▶ Run, above it. Python answers in the Console, under your code.
        Running unfinished code is fine. An error is not a grade: it says what Python couldn't read.
        Your steps: ✓ done, ● the step you're on, ○ still to come.
        Stuck? Press 💡 Help, under the Console. Each press gives more: where to look, then why, then the line.
```
(About 60 words, the card's budget. "Help options", at the top, is settings: say so in the first lesson that
uses Help if room is short here.)

**3. Six actions in one step** (u01a `what-an-error-looks-like`, step 2)
```text
Before: Break it on purpose: delete the last `"` and Run. Read *Python's last line* in the message. Then put the
        `"` back, change the `.` to `!`, and Run.
After:  Three moves, in order:
        1. Delete the `"` right after `Shield up.` and press Run. An error appears. That's the plan.
        2. Read the box in the Console. Its title says what went wrong.
        3. Put the `"` back, change the `.` to `!`, and press Run. You should see `Shield up!`.
```
(Its check message keeps "change the `.` to `!`", because a `wrong_answers` entry expects that phrase.)

**4. The first error** (u01a `what-an-error-looks-like`, Mar'tu)
```text
Before: Read the last line first: the message under your code shows it as *Python's last line*. Then look at the
        line it names.
After:  This line tells Python to show `Shield up.` in the Console, the box under your code. Press Run. Then you'll
        break it on purpose. When Python can't read a line, it stops and shows an [[error message]]. That's not a
        grade. It's like a teacher's note in the margin: it points to the spot.
```

**5. Symbols before they're taught** (u01a `keyboard-symbols`, Mar'tu, after the keyboard picture)
```text
Before: `-` subtracts, `_` joins words in a name, `=` puts a value in a box.
After:  `-` is minus, like in math. `_` is the underscore (Shift and `-`): it stands in for a space, like `max_mana`.
        `=` is the equals key, but in Python it doesn't mean equals. Its job comes in Boxes With Labels. In Python,
        *print* means show on the screen, not on paper.
```

**6. `=` and the algebra link** (u01b `label-a-box`, Mar'tu)
```text
Before: A box ([[variable]]) has a label and something inside. ... Read `=` as gets: companion gets Gearshift.
After:  In math, a letter like x stands for a number. A box (a [[variable]]) is like that, but you pick its name, and
        it can hold words. `companion = "Gearshift"` makes a box named `companion` with Gearshift inside. In math,
        `=` means both sides are equal. In Python, read `=` as *gets*: companion gets Gearshift.
```

**7. A step that is already true** (u01b `label-a-box`, step 1)
```text
Before: Make sure line 1 starts with `companion = `. Then change the hero in the quotes to a different hero.
After:  On line 1, change `Gearshift` to a different hero. Keep `companion = ` and both quotes as they are.
```

**8. An idiom and a planted number** (u01b `numbers-stand-alone`: title, Mar'tu, step 1)
```text
Before: Numbers stand alone ... Lucky says his armor bonus is 30. It is 3. We use the 3.
        Make `armor_bonus` holding Lucky's armor bonus, 3, as a number.
After:  Title: Numbers don't get quotes.
        A [[number]] gets no quotes. `3` is an amount you can do math with, like points in a game. `"3"` in quotes
        is text, like the 3 on a jersey: nobody adds two jerseys. Lucky's armor bonus is 3.
        Step: Make a box named `armor_bonus` that holds the number 3. No quotes: it's a number.
```

**9. Pointing at the wrong line** (u01b `exact-names`, step 2)
```text
Before: Make line 2 print 18, using the name the task gives: `max_mana`.
After:  Line 1 makes a box named `Max_Mana`, but line 2 asks for `max_mana`. Rename the box on line 1 so the two
        names match, letter for letter.
```
(The step still names line 2, where Python stops, so Help still points at this step.)

**10. The formula idea** (u01c `chalk-math`, Mar'tu, and step 1)
```text
Before: My checks are sneaky: they put other numbers in your boxes and run your code again, to see if your line
        follows. ... / Replace the `0` so the line prints how much the gap shrank.
After:  Python does math with `+` (plus), `-` (minus), `*` (times: there's no × key) and `/` (divided by). On my chalk
        wall, the first gap between bursts was 48 hours. The last was 37.
        In math, area = length × width works for any rectangle. Make your line a formula too: I test it with other
        numbers.
        Step: Replace the `0` with the bigger gap minus the smaller gap. Use the box names `first_gap` and
        `last_gap`, not the numbers.
```

**11. The rerun message** (u01c, the `rerun()` builder; the same in u01d)
```text
Before: Mar'tu's check tried your code with `last_gap = 41` (only inside the check: leave your own numbers as they
        are). This time, your program should print `7`, but it printed `11`. Your 11 is right for 48 and 37. ...
After:  You typed the answer, 11, instead of the math. Write `print(first_gap - last_gap)` so Python works it out.
        Mar'tu tested your line with a test number, `last_gap = 41`: the answer should change to 7, but yours
        stayed 11. Don't type the test number.
```
(Then update every `message_contains="typed in"` entry to a phrase that is still in the message.)

**12. A value with no name** (the lone-value builders in u01b, u01c and u01d)
```text
Before: Line 4 is a value with no box, so Python made it and forgot it. Delete it, or put a name and `=` in front.
After:  Line 4 is a value with no name in front, so Python reads it and throws it away, like a phone number saved
        with no contact name. Put `hero = ` in front of it.
```

**13. Algebra's objection** (u01c `spend-mana`, Mar'tu, and step 1)
```text
Before: `mana = mana - spell_cost` means: take what is in `mana` now, subtract the cost, and put the answer back in
        `mana`. / Make it three casts.
After:  In math class, x = x − 3 has no answer. In Python, `=` isn't a math statement. Python works out the right side
        first, with what's in the box now: 26 − 3 is 23. Then 23 goes back in the box. Read it as: mana gets mana
        minus spell cost.
        Step: Each `mana = mana - spell_cost` line casts the spell once. Add one more of those lines, right above
        `print(mana)`. You should see 17.
```

**14. Two jobs for `+`** (u01c `glue-words`, Mar'tu)
```text
Before: `+` [[glue|glues]] text to text. A number must become text first: `str(26)` gives `"26"`.
After:  `+` has two jobs. Between numbers it adds: `2 + 3` is 5. Between texts it [[glue|glues]], like a compound
        word: `"sun" + "flower"` is `"sunflower"`, with no space. To glue a number, make it text first with
        [[str()|`str()`]], short for *string*: `str(26)` gives `"26"`.
```

**15. Repeated addition and PEMDAS** (u01c `repeat-a-mark`, Mar'tu, and step 2)
```text
Before: `*` also [[stamp|stamps]] text: `"█" * 3` stamps three blocks. / Replace the second `0` with the mana used:
        `(max_mana - mana)`, in brackets.
After:  In math, 3 × 4 means 4 + 4 + 4. Python does the same with text: `"█" * 3` is `"█" + "█" + "█"`, so it shows
        `███`. A mana bar is dark blocks for the mana you have, then pale blocks `░` for the mana used.
        Step: Replace the second `0` with the mana used, `(max_mana - mana)`, in parentheses. It's PEMDAS:
        parentheses first, so Python subtracts before it multiplies.
```

---

## 8. Don't break the machinery

1. **Edit only `docs/intro-to-python/prototypes/uNN*.py`.** Never edit `content/courses/intro-python/**/*.json` by
   hand.
2. **Words you may change** (student-facing prose): `martu`, checkpoint `text`, `hints`, `pass_line`, `another_way`
   `text` and `label` (and adding one angle), predict `q` and `explain`, `takeaway`, `pair_talk`, bonus `title`,
   `text` and `hints`, `campaign_link.why`, item `title`, `summary`, `intro` and `body`, quiz `q`, `explain`,
   `why_wrong` and prose mc choices, glossary `plain` and `example`, cheatsheet `concept` and `note`, `UNIT` `goals`
   and `martu_intro`, and the **message strings** inside checks.
3. **Never change:** any code field (`starter`, including its `#` notes; `solution`; `setup`; `example` and
   `example_output`; `partials`; `wrong_answers` `code`; bonus `solution`; `snippet`; predict `code` and `choices`;
   quiz `code`, `fix`, `answer`, `accept`, `expected_output`, `lines` and `distractors`; cheatsheet `code` and
   `output`). Also never change check logic (conditions, names, order), any `id`, `names`, `pick`, `introduces`,
   `preview`, `dictated`, `planned_error`, `support`, `solo`, `explainer`, `engine`, `stdin` or `assemble`, or the
   number and order of steps, hints and choices.
4. **The Help ladder.**
   - (a) Keep the number and order of hints in every step and side quest.
   - (b) The first code span in the last hint is the source for Start me off: the site takes it up to the first `(`
     or `=` (or a list's `[`), but only if the solution contains that start. Keep that span, with two exceptions:
     you may replace another program's example with the step's own line from the solution, and in an edit-in-place
     step you may put the mark first (§4.1.5). After either change, run the harness. From Unit 2 on, it warns when
     the start is not in the solution.
   - (c) Place phrases in the last hint: "in place of", "on the line after", "under" (or "under the") and
     "above", each followed by a code span, as in ``above `print(mana)` ``. Keep the phrase and its code span
     exactly, after the step's line. From Unit 5 on, the harness warns about a place written in other words
     ("Change line 4 to", "under comment 2").
   - (d) Keep "Start like this: `…`" and "Start the line with `…`" exactly, code span included.
5. **Debugging exercises.**
   - The site treats an exercise as a debugging exercise only when a step's text contains the word *mend*. That is
     what makes it show "Python got further: that slip is mended.", and its banner also says "Mend line 3 first."
     So keep "Mend" in those step texts, and define it once, in U1 `close-the-quote` (Mar'tu, plus a glossary entry
     `mend`).
   - Never add "mend" to a step outside a debugging exercise.
   - After a crash, Help aims at the step whose text names the line Python stopped on ("line 3"). Keep every
     "line N" in step text, and make sure it is right. You may add the line where the fix goes.
6. **Check messages.**
   - Change only the message text.
   - For each message you change, look at that exercise's `wrong_answers`. Any entry whose `message_contains` quotes
     the old text either keeps a phrase that is still in the new message, or gets its `message_contains` updated to
     one. Never change `fails_at`. Watch for "typed by hand", "typed in", "brackets", "change the `.` to `!`" and
     "Mend this slip".
   - The builders (`rerun`, `rerun_box`, `rerun_line`, `slot`, `story_pair`, `set_once`, `loose_math`, `near_names`,
     the lone-value messages and their Unit 2–5 equivalents) feed many steps, so run the harness for the whole unit
     after you change one.
   - Messages are Python strings inside Python strings. Escape an apostrophe inside `'…'`, or use double quotes. Keep
     `%s`, `%d`, `__NAME__` and `{…}` placeholders as they are.
   - Write "Mar'tu" in full: never `'Mar' + chr(39) + 's'`, because a test fails on "Mar's check".
7. **SOLO pass lines** keep "You did that on your own." exactly. The site swaps that sentence when the student had
   help.
8. **The `UNIT` dict is the same in every part file** (u01a–u01d, and so on). Change it in all of them, or the
   exporter fails.
9. **Glossary.**
   - Every `[[term]]` and `[[term|shown words]]` must match a term or an alias (case doesn't matter).
   - To rename a term, use the new term and keep the old one as an alias. Example: term `parentheses` with aliases
     `parenthesis`, `brackets`, `bracket`, `round brackets`; term `show your work` keeping `show your working` and
     its old aliases.
   - An alias can appear only once in the whole course.
   - No links in `pass_line` or in an Another way `label`.
   - The shown words in a link are either plain words or one whole code span, and a link never goes inside
     backticks.
10. **Prose format.**
    - One paragraph per line (`\n`).
    - Step text never starts with a number. Lines that start with `1. ` render as a list.
    - Backticks are balanced and fences are closed.
    - **Lines inside a fenced block are 36 characters or fewer.**
    - *Single stars* go around words only. No `**bold**`.
11. **Privacy.** No student names and no worksheet ids, anywhere. Use only invented values (Zelda, Kratos, Tester,
    Captain Glug, a grumpy moth).
12. **Run these until clean:**
    ```bash
    python3 docs/intro-to-python/prototypes/harness.py u01a     # your prefix: 0 errors
    npm run course:export                                       # writes the JSON
    npx vitest run src/lib/course/content.test.ts               # links, fences (36), prose marks
    ```
    The content test checks the exported JSON (fence width, glossary links, the marks the site renders), so
    export before you run it.
    The only warnings that should remain are "starter is not valid Python yet" (Unit 1 has 7, Unit 2 has 8, Units
    3–5 have 1 each). Fix any new warning about reading level, Mar'tu's length, links in labels or pass lines, a
    dropped Start me off, or a vague place. Commit the `.py` files and the generated files together.
13. **To check a reading level:**
    `echo 'your text' | python3 -c "import sys; sys.path.insert(0, 'docs/intro-to-python/prototypes'); from harness import reading_stats; print(reading_stats(sys.stdin.read()))"`
    It prints (words, grade).

---

## 9. Not yours to fix: site code and structure (send these to the orchestrator)

Writers who meet these should leave them and report them. They need site code or a structural change.

- **S1.** The site finds debugging exercises by the word *mend*. Its banners say "Mend line N first." and "First, mend
  line N.", and its progress line says "Python got further: that slip is mended." If the site learns "fix" too,
  content can drop "mend".
- **S2.** The crash banner (HelpStack) says "Mend line 1 first. Python stopped there, so it could not check your steps
  yet. Read the message under your code." Better: "Python stopped at line 1, so it couldn't finish your code. Fix
  line 1, then press Run again. The box in the Console says what's wrong."
- **S3.** Start me off shows "Your code already starts this line (`print(`). Finish it yourself." on steps that only
  edit a line. Hide it there.
- **S4.** "Help opens after you press Run once." Add: "Running unfinished code is fine."
- **S5.** Unit 1 rows in `explain.ts`:
  - "def is for making functions, not variables": the words variable and function aren't taught yet.
  - A lone `Lucky` gets "write Lucky =": the wrong box.
  - `print(steady)` gets "If it's a variable, use this task's names: print".
  - `ink = █` gets "type that part again yourself": the real fix is quotes.
  - A lone value gets the advice "like armor_bonus = "Telegun"", the wrong box, plus an unrelated print option.
- **S6.** `explain.ts` and the symbol tray say "brackets", "round brackets", "curly brackets" and "open bracket". They
  should say parentheses and curly braces.
- **S7.** The "Names to use" chips show `str` next to the box names. Show it apart, as a tool.
- **S8.** In the u01c `rerun()` crash version, the raw error is pasted after "it stopped:". Translating it into plain
  words needs a small lookup in the check logic.
- **S9.** The campaign box and the side quests are both titled "What's in it for me?". Retitle the campaign box
  "Where you saw this in the game".
- **S10.** SOLO pass lines promise "On your map: ✓ …", but no skills map is on screen yet.
- **S11.** Oogrish's nudge says "Read the last line first." It should use the reading routine (§4.2).
- **Done in the second read-through (site code, no writer action):** S2's banner wording; a step done by an error made
  on purpose (`planned_error`, FORMAT.md: the first lesson's step 2 ticks on the planned break and stays ticked); the
  banner and "Same error" name the slip's own line; "That's part of this step" only for a line that was there from
  the start; Start me off goes "in place of" the line a "Change line 9" step names, and says so; the error-box rows
  in §4.8.
- **S12. Structure.**
  - Steps to split: `what-an-error-looks-like` step 2; `name-and-value-again` step 1; the ledger's steps 4 and 7.
  - `keyboard-symbols` comes before `print` and `#` are taught.
  - Starter notes to change: `mana = 0  # starts full` in `status-line`, and the `#` starter in `keyboard-symbols`.
  - The `numbers-stand-alone` Example shows a box versus a word, not a number versus text.
  - The ward sign's untouched-starter message ("only 5 rows changed") needs a "no O yet" branch.
