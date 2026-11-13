# Intro to Python — project brief (shared context for every agent)

## The ask (from the teacher who owns this repo)
Create a new section on the site called **"Intro to Python"**. Its modules should behave closer to what
Codecademy offers for teaching Python (narrative lesson text + guided exercises with checkpoints + hints,
quizzes, projects, optional code challenges, review material). The learning goals follow the sample syllabus
below. The main goal: get students comfortable with the Python they will see in the main campaign
(see `campaign-python-inventory.md`). Students should arrive at the campaign's Python inside their
**zone of proximal development**: stretched, but able to succeed with the support the game gives them.

Story frame: **Mar'tu** (from the main campaign) pulls the "adventurer" (the student, addressed as "you")
aside to teach them Python. Opening vibe: *"Hi. It is me, Mar'tu. Before we continue on our adventure you
must learn some of the language we call, Python."* Pepper in fun from the main RPG, never at the expense of
learning.

Accommodation stance: we are building with AI, so we CAN and SHOULD build accommodating features (opt-in
alternate explanations, hint ladders, test-out paths, bonus challenges, etc.) to a greater degree than a
single human teacher could, as long as they don't significantly impede learners at other levels.

The students are school-age (middle/high school), playing a classroom TTRPG-style campaign. A teacher runs it.
Never record student names anywhere in the repo.

## The sample syllabus (learning goals to base our units on; it is Codecademy's "Learn Python 3" outline —
use it ONLY for learning goals and structure. All content, projects, names and text must be ORIGINAL and set
in our world. Do not reproduce Codecademy's exercise text or project premises.)
1. **Hello World** — Get started with Python syntax. Lesson: Hello World; Quiz; Project ×2 (a block-letters
   print art project; a point-of-sale receipt project using variables + arithmetic + string concatenation);
   Articles: making the most of the course; User Input (`input()`).
2. **Control Flow** — if/else/elif, booleans, comparison & logical operators. Lesson; Article: match
   statements; Quiz; Projects ×2 (a magic-8-ball random-answer project; a shipping-cost comparison project);
   Lesson: Errors in Python (reading tracebacks, SyntaxError/NameError/TypeError, debugging).
3. **Lists** — ordered groups of data. Lesson: Intro to Lists (create, index, append, +, len, nested); Quiz;
   Project (a gradebook); Lesson: Working with Lists (range, slicing, count, sort/sorted, len); Quiz;
   Project (a pizza-shop list-manipulation project); Articles: Tuples; zip().
4. **Loops** — for, while, range, break/continue, nested loops, list comprehensions. Lesson; Quiz; Project
   (a hair-salon data project with loops & comprehensions).
5. **Functions** — def, parameters/arguments, default & keyword args, return, multiple returns, scope.
   Lesson; Quiz; Articles: lambda; map(); Project (physics-formula functions).
6. **Code Challenges (optional)** — short graded challenges on control flow, lists, loops, functions,
   each with an advanced variant.
7. **Strings** — strings as sequences, indexing, slicing, len, concatenation, escape chars, immutability,
   `in`, iterating; String methods (lower/upper/title/capitalize, split, join, strip, replace, find,
   format/f-strings). Lesson ×2; Quiz ×2; Project (a messy-transaction-data cleanup project); Off-platform
   project (a cipher / coded-correspondence project).
Totals in the original: 14 lessons, 14 projects, 13 quizzes.

**Gap vs. campaign:** the campaign leans heavily on **dictionaries** (literal, nested access, assignment by key,
`in`/`not in`, a dict holding a function) and **random.randint**, **passing functions as values**, and
**string repetition** (`"█" * n`). The syllabus above has none of dictionaries. The design must close that gap.

## The world and its people (from the teacher's campaign document "Leylines Awaken")
- **World: Tor.** Glowing blue **ley-lines** run under every continent. They used to be quiet and gave a little
  magic to anyone who knew how to ask. Now they've woken up: periodically a ley-line **bursts** and a tidal
  wave of blue-white magic rolls across the land; anyone caught outside a barrier is "unmade". Magic comes
  from **the Alatium**, the source of all magic. Characters have **mana**, **max_mana**, **magical_affinity**,
  ability scores (strength, constitution, athletics, dexterity, personality, perception, intelligence, wisdom,
  magical affinity), weapon damage dice (d6, d8), armor bonus, and do **skill checks** (roll a d20 vs. a
  required roll).
- **The Ley Clock**: a pendulum clock with one hand and a glowing blue arc; when the hand reaches the arc a
  burst arrives. "It is NOT a compass." It turned **red** once before a huge burst. Mar'tu's **chalk wall**
  records hours between bursts: **48, 48, 47, 46, 44, 41, 37** (then ~32). "The decay is accelerating."
- **The greenroom**: a bare white room where the four heroes blinked into existence beside the Ley Clock,
  a door labeled "Greenroom, Interior" and a sign "EXIT". Nobody knows why. They're aliens to this world.
- **Mar'tu** (they/them): a figure in a **purple shroud**; only tired **yellow eyes** are visible. Thick accent.
  Speech tics: ends sentences with **", yes?"**; dry and grim but caring; weary patience ("Lucky... Once
  again, it is not a compass. It is a Ley Clock."); deadpan humor (Lucky: "What's in it for me?" Mar'tu:
  "Existing."). Mar'tu used to **teach at the Institute** and hauled brass instruments (the resonance array)
  back from it. Lives in a one-room oak cabin on the moonlit hills with a cherrywood mantle, stone fireplace,
  a trap door to a basement full of instruments. Raises a violet lattice **barrier** around the cabin.
- **Master Oogrish**: an old **turtle** with a cane, the party leader (General class), wise weapons master,
  carries a humming golden **medallion** with clockwork and a glowing blue marble. Says things like
  "Steady, now." INT 17, WIS 17, magical_affinity 9, max_mana 18.
- **Gearshift**: a ~20-foot **alien robot** (Warrior/tank) with a visor that dims when he runs the math;
  transforms into a backpack weapon system and a jeep; mechanic/technician; runs on rare **starlode ore**.
  "Barrier's holding." magical_affinity 10, max_mana 20.
- **Bomb Shell**: a stocky gunmetal **robot** with a single round **teal optic**, arm cannon / arm blade,
  quiet, watchful, talks in **short clipped sentences**, powered by **Velocite ore** (about a week left),
  DEX 6 (clumsy hands), WIS 8 (acts before he thinks). "Shield up." "That latch hates me." magical_affinity 12,
  max_mana 24.
- **Lucky**: a huge shaggy furred warrior in mirror-bright **platinum armor**, cocky and funny, "only in it
  for himself", always asks **"What's in it for me?"**, carries the **Telegun** (a pistol whose shots
  teleport him — has worked once since the greenroom, landed him in a hedge), a gold **pocket watch** that
  mind-controls whoever looks at it, and a dented canteen of **"glug"** (heals, smells terrible). Once per day
  he can reroll a failed roll (Dumb Luck). "Fine. But I'm keeping track." magical_affinity 13, max_mana 26.
- Spell colors: gold (Oogrish), fire orange (Gearshift), teal (Bomb Shell), silver (Lucky); Mar'tu violet.
- Engine helpers students have used: `party.move("left")`, `print_prompt(text)`, `print_options(...)`,
  `user.clicked()`, `speak_dialogue(...)`, `make_option_green()`, `print_mana(caster, bar)`,
  `reinforce_barrier(caster)`. Setting rule: modern guns didn't cross over; firearms on Tor are brass-and-rune
  steampunk machines. Keep content PG and classroom-safe.

## Current site (repo: /home/user/programming-adventure-viewer, Next.js 15 + React 19 + Pyodide in a web worker,
static export to GitHub Pages)
- Home page `/` = `ModulePicker` listing campaign modules (`content/modules/*/module.json`, schema in
  `src/lib/lesson/schema.ts`: module → lessons → beats; a beat has a scene (art + caption), `instructions`,
  optional `activity` {starterCode, checks[], passFeedback, failFeedback, solution}).
- `/play/[moduleId]` = `src/components/Player.tsx` (1100 lines): Theater (scene art/caption or game board),
  instructions, ConsolePanel (output, friendly error explainer `src/lib/languages/python/explain.ts`, failed
  checks), CodeMirror `PythonEditor`, Run / Reset code / Show solution (after 5 minutes on a part), Continue.
  Autosave + optional classroom join code (`/classroom` teacher page, progress API).
- Checks are Python snippets run after the student's code in the same namespace; `_captured_stdout` holds
  printed output; `assert ..., "student-facing message"`. `src/lib/lesson/run-checks.ts` runs them in CPython
  for unit tests using the same prelude as the browser worker (`public/workers/python-worker.js` GUARD).
- Tests: vitest (`npm test`), Playwright e2e, typecheck, lint, all in CI.
