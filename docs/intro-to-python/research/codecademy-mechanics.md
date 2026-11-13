# Codecademy "Learn Python 3": how it works as a learning experience, and what we should build

Research for the "Intro to Python" section (Mar'tu's lessons). This covers **mechanics and learning objectives
only**. Nothing here is meant to be copied as content. **IP rule for builders:** do not reuse Codecademy's
exercise text, example values, project premises, project names, character names, or quiz questions. Write every
explanation, example and project from scratch in the world of Tor.

## 0. Method, confidence and gaps

- **Network limit.** This session's network does not resolve `www.codecademy.com` or `help.codecademy.com`, so
  WebFetch failed for every Codecademy page. Everything below comes from WebSearch result excerpts (Codecademy
  help-centre articles, Codecademy blog posts, Codecademy's 2015 Medium design posts, cheatsheet mirrors, forum
  threads, reviews, and one peer-reviewed paper), plus well-established knowledge of how the platform works.
  To fetch the primary pages, `www.codecademy.com` and `help.codecademy.com` would have to be allowed in the
  session's network settings.
- Every claim carries a confidence tag:
  - **[S]** a source found this session says so (listed in Sources at the end).
  - **[K]** widely known platform behaviour, but no source confirmed it this session. Treat it as very likely, with
    exact labels possibly out of date.
  - **[?]** uncertain, or it varies by course or version.
- Codecademy changes its UI labels often. One source puts "Get Unstuck" in the lower right of the screen and a
  newer help article puts it in the upper right [S]. **Build our own mechanics from the behaviour described here,
  not from label wording.**

---

## 1. Feature-by-feature description

### 1.1 Course shape
- **Hierarchy:** course → modules (units) → items. An item is one of: lesson (a sequence of exercises), quiz,
  project, article/informational, cheatsheet, and sometimes a video [S/K]. Learn Python 3 lists **14 lessons,
  14 projects and 13 quizzes**, is rated Beginner, takes about 24 hours, gives a certificate on paid plans, and has
  a learner rating of about 4.6/5 [S].
- **The syllabus page** shows each module with its items in order and a check mark on finished items. Each module
  has a cheatsheet link [S/K]. One 2018 post says lessons can be opened in any order but individual exercises
  cannot [S].
- **Ordering inside a module:** lesson → quiz → project(s), with articles in between. Most modules end in a
  project [S].

### 1.2 Lesson exercise screen (the core loop)
- **Layout:** a multi-pane "learning environment". Codecademy's 2015 redesign defined six panes: lesson content and
  support, code editor, terminal, browser, visual aids, and file navigator. Each exercise shows only the panes it
  needs [S]. For Python the usual layout is: left column = narrative "Learn" text with short code examples, then
  the numbered **Instructions**; middle = editor (file tabs, Run button); right = output terminal [S/K].
- **Exercise size:** each exercise teaches about one concept. A lesson has roughly 8–15 exercises, and the last is
  a "Review" exercise that sums up the lesson and often leaves room for free play [K].
- **Instructions are numbered checkpoints.** Each checkpoint is one small action, such as "create a variable
  named…" or "print…" [K].
  - **Run** executes the code and then runs hidden tests for the current checkpoint [K]. Codecademy's term is
    "test" [S]. DataCamp calls the same idea an SCT (submission correctness test), and it is the same model [S].
  - When a checkpoint passes it turns green with a check mark and the next one opens. Learners do checkpoints in
    order [K].
  - When all checkpoints pass, **Next** unlocks. Some narrative-only exercises have no checkpoints and only need
    a Run [K].
- **Failure feedback** comes in two layers:
  - (a) A real Python traceback in the terminal.
  - (b) An authored test message under the instructions, usually phrased as a question, such as "Did you…?" [K].
    One Codecademy blog post describes errors that start "Oops!… The test returned an error" and frames error
    messages as clues to where to debug [S].
  - Forum guidance says spelling and capitalisation must match the instructions exactly for tests to pass [S].
- **Hints:** each checkpoint has a collapsed hint at the bottom of its instruction, labelled "Stuck? Get a hint"
  or similar [S]. A hint is usually a nudge plus a syntax example, and sometimes a partial line [K]. There is one
  hint per checkpoint, with no ladder [K].
- **"Get Unstuck" menu** (exercise level) [S]:
  - concept review
  - solution code ("Get Code Solution"), which replaces or shows the solution
  - a **diff** that compares the learner's code with the solution
  - FAQs: community Q&A threads tied to that exercise
  - report a bug, and contact support
  - The help centre also suggests **resetting** the exercise and writing the code again [S]. "Reset" restores the
    starter code [K].
- **AI Learning Assistant** (newer, paid plans) [S]:
  - It knows the current exercise, its instructions and its solution code.
  - Learners can highlight code and click "Explain code".
  - It explains errors and concepts and checks the learner's solution.
  - It can be turned off under Tools.
  - Third-party pages say it gives hints without the whole answer [?].
- **Execution:** Python runs on Codecademy's servers in containers. A help article covers "Connection lost"
  problems [S]. Critics note that programs which use `input()` cannot really be tried inside the platform [S].
  Learners can open a free-form sandbox ("Workspace") or embed runnable snippets ("Codebytes") in forum posts [K].

### 1.3 Quizzes
- Quizzes are short and low-stakes, with a few multiple-choice or true/false questions after a lesson [S]. Some
  courses also have code-completion questions, where the learner picks tokens to fill blanks in a snippet [K/?].
- **Retakes are unlimited** [S]. Codecademy recommends a minimum score before moving on, but this does not block
  progress [S].
- **Post-quiz review (added 2024):** explanations come after the quiz, not during it (*delayed feedback*). This
  helps learners understand their mistakes and remember the material [S]. The team could not write a custom
  explanation for every question. Learners can come back to the review later [S]. Codecademy reports that average
  assessment scores rose from 84% to 87% after launch [S].
- Quizzes are different from **assessments and exams** [S]:
  - Assessments and exams mix multiple-choice and coding questions and may be timed.
  - They do not show which questions were wrong.
  - Retakes are limited to a 24-hour window.
  - The pass mark is 70%.

### 1.4 Projects
- **Guided projects** sit at the end of modules [S]:
  - There is starter code and a **task checklist**: numbered tasks grouped under small headings [S].
  - Each task has a checkbox the learner ticks themselves. Tasks are **not auto-graded** [S/K].
  - Each task has its own hint [S].
  - Projects are freeform and **have no code solution** in Get Unstuck [S].
- **Project support:**
  - **Walkthrough videos**, where a staff member builds the project step by step [S]. Learners say these are
    sometimes confusing or wrong [S].
  - Community forum threads for the project [S].
  - Weekly live sessions where curriculum developers walk through projects [S].
- **Project tiers** [S]:
  - Guided projects, which are more open than exercises.
  - Challenge projects, which give a spec with little guidance.
  - Portfolio projects, which bring a whole path together and are shared for peer feedback.
  - **Off-platform projects**, which tell the learner to set up a local environment and build outside the
    browser. In the sample syllabus the cipher project is one of these.

### 1.5 Articles / informationals
- An article is a reading page with code samples, marked complete when read. Learn Python 3 has articles on
  getting the most out of the course, `input()`, match statements, tuples, `zip()`, lambda and `map()` [S, brief].
  They cover side topics without checkpoint exercises [K].

### 1.6 Cheatsheets / concept review
- Each module has a **cheatsheet**: concept headings, each with 1–3 sentences and a short code snippet [S].
  Examples include `print`, comments, `+=`, modulo, relational operators, `and`/`or`/`not`, slicing, `.count()`,
  `.sort()` vs `sorted()`, `.format()`, `.find()` and `.join()`.
- Cheatsheets can be printed or downloaded [K]. "Concept Review" in Get Unstuck links to the matching entry [S].
- Separately, **Codecademy Docs** is a community-edited reference that lessons link to [K].

### 1.7 Code challenges
- Learn Python 3 has an **optional "Code Challenges" module** of short problems on control flow, lists, loops and
  functions, each with an advanced variant. It has its own cheatsheet [S].
- Each challenge gives a function name and signature and asks the learner to fill in the body. Run then checks it
  against hidden test cases [K/?]. Failure messages name the input that failed and what the code returned [?].
- Solutions are shown after the learner tries [K].

### 1.8 Progress, motivation and practice
- **Progress indicators** [S]:
  - check marks on items, and a percentage per course or module
  - Skill XP and skill tracking
  - badges
  - **weekly targets**: the learner picks how many days a week they will make progress, and the weekly streak
    grows each week the target is met
- Codecademy moved away from daily streaks because its research showed weekly targets work better. It also
  retired points [S].
- **Smart Practice / personalised practice** [S]:
  - It uses spaced repetition to pick the concepts each learner should review.
  - Practice packs and Smart Flashcards are on web and mobile.
  - It is a separate area from the course flow.
  - The selection algorithm is not public.
- **Skip / placement:** this session found no test-out or placement option for Learn Python 3. Lessons can be
  opened out of order (2018 change), but not individual exercises [S]. By contrast, DataCamp has one-time
  test-out assessments with a 75% pass mark [S].
- **Community:** each exercise has an FAQ thread on the forum. The forum is the advertised route when stuck [S].

### 1.9 What learners and educators say
- **Praise** [S]:
  - very approachable for complete beginners
  - instant feedback
  - no setup
  - bite-sized steps that build momentum
  - well-organised syllabus
  - cheatsheets are useful
- **Criticism**, mostly reviews and forums, so anecdotal [S]:
  - **Too much hand-holding.** Learners finish exercises by doing exactly what the instruction says, then cannot
    reproduce the code alone. Reviewers call it "fill-in-the-blank" and say some concepts "didn't stick".
  - Learners stall when the scaffolding stops, at projects and after the course.
  - **Overly strict checkers**, for example "they will mark them wrong if it's not the exact one they're looking
    for". A forum thread is titled "you need to write the exact code whoever set up the lesson made".
  - Relying on hints means learners never practise debugging.
  - `input()` programs cannot really run inside the platform.
  - Some content is outdated, and there are complaints about pricing and subscriptions.
- **Research** [S]: Kim & Ko (SIGCSE 2017) analysed 30 popular coding tutorials, Codecademy included, and found:
  - Most did not meet key learning-science principles.
  - Tutorials taught **how** to use commands far more than **when and why** to use them, which hurts transfer.
  - Tutorials lacked **personalised, contextualised feedback**.
  - Games and highly interactive tutorials did best. That supports our RPG framing.

---

## 2. Ranked mechanics to emulate, mapped onto our Next.js + Pyodide player

Our player already has:
- a beat with `instructions`
- an `activity` with `{starterCode, checks[], passFeedback, failFeedback, solution}`
- Python `assert` checks that run in the student's namespace, with `_captured_stdout`
- the `explain.ts` error explainer
- a solution offered after 5 minutes on a part
- autosave and an optional classroom code

Proposed extensions are written as schema sketches. They are additive, so campaign modules keep working.

| # | Mechanic (what to copy) | How it maps onto our stack | Our improvement over Codecademy |
|---|---|---|---|
| 1 | **Learn pane + numbered checkpoints validated in order** (the core loop) | New `lessonExercise` beat (or extend `beat`): `learn` (markdown, Mar'tu's voice), `checkpoints: [{id, instruction, checks[], hints[], passLine?}]`. One Run executes the student code once in the Pyodide worker, then each checkpoint's checks **in order**, and stops at the first failure. The UI shows ✓ on passed checkpoints, the active one expanded with its failure message, and later ones greyed out. Re-run every checkpoint each time so a regression (a later edit that breaks an earlier step) is caught. Persist passed IDs in autosave. `run-checks.ts` can unit-test every checkpoint in CPython. | Name what each checkpoint checks ("I will look for a variable called `mana`…") so the hidden tests never feel like a guessing game. |
| 2 | **Per-checkpoint hint** | `hints: string[]` as a **ladder**: (1) a nudge or question, (2) the concept with a tiny unrelated example, (3) a partial line with blanks, (4) the exact line. Each step is a click: "Mar'tu leans closer…". Record ladder depth in local progress (no names). | Codecademy has one hint per checkpoint. A ladder serves struggling and confident learners without spoilers. |
| 3 | **Authored failure messages + real traceback** | Keep the assert message pattern (`assert ..., "Did you store the roll in a variable?"`), plus the `explain.ts` plain-language traceback. Add cheap pre-run "linters" that run `ast` checks in Pyodide for classic mistakes: `print` vs `return`, `=` vs `==`, missing quotes, an unused variable, a call missing `()`. | Write checks against **behaviour, not text**. Test values, return values and normalised stdout. Accept equivalent solutions. Never require exact whitespace or capitalisation unless that is the lesson. |
| 4 | **Solution + diff** | Keep the `solution` field. Add a "Compare with Mar'tu's version" diff using a small line-diff library such as `diff@5.x` from cdnjs/npm. Open it after the hint ladder is used up **or** N failed runs **or** a time limit. Teacher-configurable. Offer "Retype it" (the solution is shown read-only next to the editor) as well as "Replace my code". | Mark checkpoints passed with a revealed solution as "assisted" and queue a near-transfer twin exercise for later (see #11). That turns copying into practice. |
| 5 | **Quizzes with unlimited retakes and post-quiz review** | New `quiz` beat: `questions: [{kind, prompt, code?, options[], answer, explanations{perOption}}]`. Kinds: multiple choice, **predict the output**, fill in the blank (token chips), **spot the bug**, **Parsons** (put lines in order), true/false. Delayed feedback: score first, then a review with an explanation **for each wrong option**, each linking back to the exercise that taught it. Shuffle options and draw from a question pool on retake. A suggested threshold (e.g. 70%) shows a "Ready" badge but does not block. | Codecademy's explanations are generic and its questions are mostly recall. We target known misconceptions with code-reading items and a link back to the source exercise. |
| 6 | **Projects with a task checklist and per-task hints** | New `project` beat: `tasks: [{id, group, text, hints[], checks?[]}]` over one shared editor. Each task is a checkbox, and tasks with `checks` show an optional "Check this task" button. A text "walkthrough" reveals one step per task, instead of a long video. Optional `stretch: []` goals. Projects rehearse campaign code with stubbed engine helpers (`print_prompt`, `party.move`, `print_mana`) so the campaign feels familiar. | Optional auto-checks where possible, short step-by-step walkthroughs, stretch goals for advanced students, and an in-world payoff. |
| 7 | **Cheatsheet / concept review per unit** | Each exercise lists `takeaways[]` (one concept and one snippet). A unit cheatsheet page is generated from them, styled as Mar'tu's chalk-wall notes or a spellbook page, printable, and linked from the hint ladder and quiz review. Add a hover glossary for terms (variable, argument, return…). | Generate it from the same source as the lessons so it never drifts out of date. Link each concept to where it appears in the campaign. |
| 8 | **Code challenges graded by test cases** | New `challenge` beat: `function`, `tests: [{args, expected, visible: bool}]`, `variants: {standard, advanced}`. Show a table of visible tests (input → expected → got) and count hidden ones. Run tests with a per-test timeout in the worker so an infinite loop cannot freeze the page. | Visible test tables teach debugging. An advanced variant on every challenge gives strong students headroom. |
| 9 | **Reset, autosave, and runnable examples in the Learn text** | Keep Reset and autosave. Make code blocks in `learn` runnable ("Try it" opens a scratch console), like Codebytes. Add a free-play **Sandbox** page. Shim `input()` in Pyodide with an on-page prompt, and let checks feed scripted inputs. | Fixes Codecademy's `input()` weakness, so the `input()` article can have real exercises. |
| 10 | **Progress indicators** | Unit map (a trail of Tor waypoints), check marks per item, and % complete per unit, stored with the existing autosave and classroom progress API. Optional **weekly** target, not a daily streak (Codecademy's own research). | Show "you're ready for the campaign" milestones tied to the campaign inventory. |
| 11 | **Spaced review** (Smart Practice idea, built into the course) | A 2–3 item "Warm-up at the fire" at the start of each lesson, drawn from earlier units and weighted toward missed quiz items and "assisted" checkpoints (stored locally). The items are quiz-style or tiny code tasks. | Codecademy keeps practice separate and paywalled. We weave it into the flow and keep it short and skippable. |
| 12 | **Test-out / placement** (Codecademy has none) | Each unit gets a `testOut` beat: a short quiz plus 1–2 code tasks that cover the unit's objectives. Passing marks the unit "tested out" (green). Content stays open, and the student gets a nudge toward bonus challenges. A failed attempt shows which objectives to visit, and lessons for objectives already shown can be skipped. | Gives experienced students a fast lane without skipping the objectives the campaign needs. |
| 13 | **"Explain it another way"** (AI-assistant idea, without a live LLM) | Each exercise can carry `altExplanations: [{label, markdown}]`, for example "Picture it" (a diagram or memory-box view), "Step by step" (a trace table), "In Tor terms" (a story analogy), and "Shorter please". All of it is pre-written at authoring time, so the static GitHub Pages site needs no runtime AI. | This is the accommodation stance in the brief. It costs nothing to learners who never open it. |
| 14 | **Exercise FAQ** | `faq: [{q, a}]` per exercise, seeded with the common questions predicted from student assessments. No public forum, because this is a classroom and student names must not be stored. | Safe for a classroom. |

**Suggested build order:** 1, 3, 2, 4 (the exercise loop), then 5 and 7, then 6, then 12 and 13 (accommodations),
then 8, 11 and 10. Items 9 and 14 can come at any point.

---

## 3. Known weaknesses we can improve on

### For struggling learners
1. **Single explanation angle.** Each concept is explained once, in dense prose.
   → Alternate explanations (#13), a glossary, shorter sentences, optional read-aloud, diagrams of variables as
   labelled boxes, and trace tables for loops.
2. **Hidden, strict, exact-match tests feel arbitrary** [S].
   → Behaviour-based checks, a statement of what is checked, normalised output comparison, and accepted
   alternative solutions. Unit-test the checks against 2–3 correct variants during authoring.
3. **Cryptic errors.** Raw tracebacks plus terse test messages.
   → `explain.ts`, pre-run linters, highlighting the offending line in the editor, and showing "what Python
   thinks you meant".
4. **The jump from hint to full solution is a cliff.** Copying the solution does not teach anything.
   → Hint ladder (#2), a gated diff (#4), "Retype it", and an "assisted" flag that queues a twin exercise.
5. **Debugging is taught once and briefly.** In the syllabus it comes after control flow.
   → An "Errors" mini-lesson early in unit 1, plus a recurring "Mar'tu's broken spell" fix-the-bug checkpoint in
   every lesson.
6. **Projects lose the scaffolding all at once**, so learners "hit a wall" [S].
   → **Fading:** worked example, then completion problem (some lines given), then write it yourself. Projects keep
   per-task hints and optional checks. Parsons problems bridge reading and writing.
7. **`input()` cannot be tested in the browser** [S].
   → Pyodide `input()` shim (#9).
8. **Motivation and context.** Generic, unconnected premises.
   → Mar'tu's frame, small RPG payoffs (a mana bar fills, the Ley Clock ticks), and Lucky's "What's in it for me?"
   asides that state *why* a concept matters.

### For advanced learners
9. **No placement or test-out** [S].
   → Unit test-outs (#12), plus a "fast lane" toggle that collapses the Learn pane and goes straight to
   checkpoints.
10. **Too easy and too guided** ("typing what the lesson dictates") [S].
    → Optional "Hard mode" per exercise (same goal, no starter code, extra constraint), the advanced variant of
    every code challenge, and stretch goals in projects.
11. **The how is taught more than the when and why** (Kim & Ko 2017) [S].
    → Every lesson ends with "Where you'll see this in the campaign", using real snippets from
    `campaign-python-inventory.md`, and a "choose the right tool" quiz item.

### For everyone
12. **Retention.** Practice is separate from the course and paywalled.
    → Built-in warm-ups (#11).
13. **Quizzes are mostly recall MCQs with generic explanations.**
    → Code-reading item types, an explanation per distractor, and links back to the exercise.
14. **Little teacher visibility in a classroom.**
    → Feed anonymised signals to the existing classroom page: checkpoints passed, hint depth, solution reveals,
    test-out results. Use no names, only join-code seat IDs, as now.

---

## 4. Learning-objective table per syllabus item

Notes on the table:
- Objectives are written as "Student can…". They are inferred from Codecademy cheatsheets, exercise titles,
  third-party notes, and standard Python 3 coverage. They are **not** Codecademy text.
- "Campaign link" points to `campaign-python-inventory.md`.
- Conf. = confidence that Codecademy's item covers this objective. We should teach every objective listed either
  way.

### Unit 1: Hello World

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Hello World | Lesson | Use `print()` (one or more arguments separated by spaces; no argument prints a blank line). Write string literals with single or double quotes, used consistently. Write `#` comments. Create, assign and **reassign** variables, and follow naming rules. Use `int` and `float` numbers. Use `+ - * /` (`/` gives a float), `**` and `%`, with order of operations. Concatenate with `+`, convert with `str()` before joining a number. Use `+=`. Write multi-line strings with triple quotes. Meet the first errors (SyntaxError, NameError). | Concatenation and `str()` in mana bar text. Variable reassignment. | S/K |
| Quiz | Quiz | Recognise valid `print` and string syntax, comment syntax, variable assignment, arithmetic results (including `/` and `%`), and the concatenation type error. | — | K |
| Print-art project (block letters) | Project | Sequence many `print()` calls to draw multi-line text art. Plan output line by line. Combine string literals for layout. | Prepares string repetition (`"█" * n`), which we add as an objective. | S (brief) |
| Receipt project (variables, arithmetic, concatenation) | Project | Store item names and prices in variables. Compute subtotal, tax or total with arithmetic. Update a running total with `+=`. Build and print a readable multi-line receipt with `+` and `str()`. | `caster["mana"] = caster["mana"] - cost`. Building the mana string. | S (brief) |
| Making the most of the course | Article | Study habits only, no Python objective. Our version: how the hint ladder, solutions, test-outs and the cheatsheet work. | — | S |
| User Input | Article | Call `input(prompt)`. Know it **always returns a string**. Convert with `int()`/`float()`. Use the value in output. Know what running a program in a terminal means. | `user.clicked()` returns a string compared with `==`. | S/K |

### Unit 2: Control Flow

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Control Flow | Lesson | Explain Boolean expressions (`True`/`False`, the `bool` type). Use relational operators `== != > < >= <=` and tell `=` from `==`. Store a Boolean in a variable. Write an `if` with a colon and indented block. Use logical operators `and`, `or`, `not`. Write `else`. Write `elif` chains, where the first true branch wins and order matters. | `if/elif/else` on `user.clicked() == "option 1"`. `return roll >= required_roll`. `<` vs `<=` in `cast_spell`. | S |
| match statements | Article | Use `match`/`case` with literal patterns, the wildcard `case _:`, and `|` alternatives. Know when it replaces a long `elif` chain (Python 3.10+, which Pyodide supports). | An alternative way to write the 4-option dialogue chain. | S (brief) / K |
| Quiz | Quiz | Evaluate compound Boolean expressions. Trace `if/elif/else` paths. Spot `=` vs `==` and indentation errors. | — | K |
| Random-answer project (magic-8-ball style) | Project | `import random`. Use `random.randint(a, b)`, which **includes both ends**. Map a number to a message with `if/elif/else`. Concatenate the answer into output. Handle an empty or default input with a condition. | `import random`, `random.randint(1, die_size)`. | S (brief) / K |
| Cost-comparison project (shipping style) | Project | Use `elif` tiers on numeric ranges (`<=` boundaries). Compute cost from rate × amount + flat fee. Compare several options and pick the cheapest with comparisons. Print a decision. | Skill checks: `required_roll` thresholds and boundaries. | S (brief) / K |
| Errors in Python | Lesson | Read a traceback: file, **line number**, error type, message. Find and fix a **SyntaxError** (missing quote, paren or colon, bad indentation), a **NameError** (typo, undefined variable, missing quotes around text), and a **TypeError** (`str + int`, wrong number of arguments, calling a non-function). Use a debugging routine: read the last line, go to the line, check the line above, print values. | Every campaign part, and `explain.ts` output. | S (brief) / K |

### Unit 3: Lists

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Intro to Lists | Lesson | Create list literals with `[]`. Know lists can mix types and can be empty. Use zero-based indexing and **negative indexing**. Recognise `IndexError`. Change an item by index assignment. Grow a list with `.append()` and with `+`. Remove a value with `.remove()`. Use `len()`. Make **2D (nested) lists**, then read and write `grid[i][j]`. | `party.members` is a list. Nested access by analogy for `caster["abilities"]["magical_affinity"]`. | S/K |
| Quiz | Quiz | Predict index results (positive and negative). Read the effects of append, remove and `+`. Read 2D access. | — | K |
| Gradebook project | Project | Build lists of pairs (2D lists). Append rows. Combine lists with `+`. Change a nested value. Remove an entry. Print a whole structure. | Lists of records lead into lists of dicts (`party.members`). | S (brief) |
| Working with Lists | Lesson | Use `.insert(i, x)` and `.pop()` (no argument, or an index). Make `range(stop)`, `range(start, stop)` and `range(start, stop, step)`, and convert with `list(range(...))`. Use `len()`. Slice with `[start:end]`, omitted ends and negative slices, and know a slice is a **new list**. Use `.count(x)`. Use `.sort()` (in place, returns `None`, `reverse=True`) and know how it differs from `sorted()` (returns a new list). | Chalk-wall data `[48, 48, 47, 46, 44, 41, 37]` suits slicing, sorting and counting. | S |
| Quiz | Quiz | Predict `range` contents (stop is excluded), slice results, and `.sort()` vs `sorted()` return values. | — | K |
| List-manipulation project (shop-menu style) | Project | Keep parallel lists (names and prices). Use `len` and `.count`. Combine with `zip` into a list of pairs. `sort`. `insert` and `pop` items. Slice the top or bottom N. | — | S (brief) |
| Tuples | Article | Write tuple literals, including a single-element tuple with a trailing comma. Know tuples are **immutable**: item assignment raises a TypeError. Index a tuple. **Unpack** with `a, b = t`. Know when to choose a tuple over a list. | Multiple return values are tuples (functions unit). | S (brief) / K |
| zip() | Article | Use `zip(a, b)` to pair items. Wrap it in `list(zip(...))` to see it. Know it stops at the **shortest** input. Loop over zip with unpacking `for x, y in zip(a, b)`. | — | S |

### Unit 4: Loops

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Loops | Lesson | Explain why loops exist (DRY). Write `for item in list:`. Write `for i in range(n):`. Write `while condition:` with a counter or state update. Use a `while` loop over a list with an index and `len`. Recognise **infinite loops** and how to stop one. Use `break` and `continue`. Write **nested loops** over 2D lists. Use a **list comprehension** `[expr for x in seq]`, with an `if` filter and with an `a if c else b` expression. Build an accumulator (sum or count in a loop). | `for member in party.members: show_mana(member)`. | S |
| Quiz | Quiz | Count iterations. Trace `break`/`continue`. Predict comprehension output. Spot an infinite loop. | — | K |
| Loops data project (salon-business style) | Project | Loop over parallel price and sales lists to compute total and average. Change prices with a comprehension. Filter with comprehension conditions. Combine lists with `zip` in a comprehension. | — | S (brief) |

### Unit 5: Functions

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Functions | Lesson | Explain why functions exist. `def name():` with an indented body, and `pass`. **Call** a function, and know defining is not calling. Follow whitespace and execution flow. Tell **parameters** from **arguments**. Use multiple parameters. Pass **positional, keyword and default** arguments. Tell built-in from user-defined functions. **Scope**: local vs global, and a parameter is not visible outside its function. `return` vs `print`. Store a return value in a variable. Return **multiple values** and unpack them. Use early `return`. | `def`, `pass`, `return`, store-then-pass (`dialogue = get_...(); print_prompt(dialogue)`), early `return` in `cast_spell`, 5-parameter `add_spell`. | S |
| Quiz | Quiz | Trace function calls and return values. Spot print-vs-return bugs. Read keyword and default arguments. Predict scope errors. | — | K |
| lambda | Article | Write `lambda args: expression`. Assign a lambda to a name. Pass one as an argument (e.g. `sorted(key=...)`). Know its limits (single expression). Know that a **function is a value**. | **Passing a function without parentheses** (`add_spell(..., strengthen_magic)`) and **calling a stored function** (`spell["spell_function"](caster)`). | S (brief) / K |
| map() | Article | Use `map(func, iterable)`, which returns a lazy map object, so wrap it in `list(...)`. Use it with named functions and lambdas. Compare it with a list comprehension. | Functions as values. | S (brief) / K |
| Formula-functions project (physics style) | Project | Write several small functions that take parameters (some with defaults) and return computed values. Compose calls, feeding one function's return into another. Use keyword arguments. Print results. | Our version: mana, damage-dice and barrier formulas. | S (brief) |

### Unit 6: Code Challenges (optional)

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Challenges: Control Flow (+ advanced) | Challenge set | Write functions that return Booleans or values chosen by comparisons, `and`/`or`/`not` and `if/elif/else`. Handle boundary cases. | Skill checks. | S/K |
| Challenges: Lists (+ advanced) | Challenge set | Write functions that index, append, slice, combine and measure lists. Handle short or empty lists. | — | S/K |
| Challenges: Loops (+ advanced) | Challenge set | Write functions that iterate, accumulate, filter, exit early and nest loops over lists. | Party loops. | S/K |
| Challenges: Functions (+ advanced) | Challenge set | Write functions that call other functions, take multiple parameters, and return computed or composed results. | — | S/K |

### Unit 7: Strings

| Item | Type | Learning objectives | Campaign link | Conf. |
|---|---|---|---|---|
| Strings | Lesson | Treat strings as sequences of characters. Index with positive and negative indices. Slice. Concatenate. Use `len()`. Know strings are **immutable** (assigning to `s[0]` raises a TypeError, so build a new string). Use **escape characters** `\" \' \n \t \\`. Loop over a string with `for ch in s`. Use `in` to test for a substring. Write string-processing functions (count letters, test containment, build a result). | `str()` and `+` building, string comparison. Add **string repetition `*`** here (it is not in the syllabus but is in the campaign). | S |
| String Methods | Lesson | Call a method with `s.method()`, and know methods **return new strings**. Use `.lower()`, `.upper()`, `.title()`, `.capitalize()`, `.split()` (default whitespace, a delimiter, `\n`), `.join()` (called on the separator), `.strip()` (with or without characters), `.replace()`, `.find()` (returns -1 if not found), and `.format()` (positional and keyword placeholders) and **f-strings**. **Chain** methods. | `.lower().capitalize()` chaining. Reassigning `x = x.lower()`. | S |
| Quiz ×2 | Quiz | Predict index and slice results and immutability errors. Predict the output of method chains and split/join round trips. | — | K |
| Data-cleanup project (messy transactions style) | Project | Split one raw string into records (`split` on a separator and on newlines). `strip` whitespace. `replace` stray characters. Use nested loops to pull out fields. Convert to `float` and total them. `join` and format a summary. | — | S (brief) |
| Cipher project (off-platform) | Project | Shift letters with an alphabet string and `.find()`/indexing. Wrap around with `%`. Write encode and decode functions with a key parameter. Loop over characters and build a new string. Keep non-letters unchanged. Optionally add a keyword (polyalphabetic) extension. Optionally run Python locally. | Fits Tor well: Mar'tu's coded notes or ley-line runes. | S (brief) |

### Gap objectives the syllabus lacks but the campaign requires

Add these as their own unit, placed between Functions and the campaign.

| Item | Learning objectives | Campaign link |
|---|---|---|
| Dictionaries | Write a literal `{"key": value}` with string keys. Read `d["key"]`. **Add or overwrite** with `d[key] = value`. Use `key in d` / `not in`. Recognise `KeyError`. Use `.get(key, default)`. Loop over `.items()` (and `.keys()`/`.values()`). **Nest** dicts and read or write `d["a"]["b"]`. Use a list of dicts. Know that changing a dict passed into a function changes the caller's dict. Codecademy's separate Dictionaries module covers creation, access, `.get`, `.pop`, `.keys/.values/.items`, and comprehensions with `zip` [S]. | `spell` dict, `spell_book[spell_name] = spell`, `caster["abilities"]["magical_affinity"]`, `not in caster["spell_book"]`. |
| Functions as values | Use a function name without `()` as a value. Store it in a variable, list or dict. Pass it as an argument. Call it later with `stored(args)`. | `strengthen_magic` passed to `add_spell`. `spell["spell_function"](caster)`. |
| `random` | `import random`. `random.randint(a, b)` includes both ends. `random.choice(seq)`. Know results vary from run to run, and how checks deal with that (seeded or property-based checks). | `perform_roll(die_size)`. |
| String repetition and bars | `"█" * n`. Handle `n = 0`. Compute `max - current`, then concatenate and `str()` into a status line. | `get_mana_bar(caster)`. |
| Returning comparisons | `return a >= b` instead of `if ...: return True else: return False`. | Skill checks. |
| Reading code you did not write | Read the signature, docstring and comments of helper functions, call them correctly, and leave "already finished" code alone. | `print_prompt`, `print_mana`, `reinforce_barrier`, `party.show_mana_bar`. |

---

## Sources (found via WebSearch this session; Codecademy pages could not be fetched)

- [Codecademy: Learn Python 3 course page](https://www.codecademy.com/learn/learn-python-3) (14 lessons / 14 projects / 13 quizzes, ratings, projects)
- [Codecademy help: Updates to our Learning Environment](https://help.codecademy.com/hc/en-us/articles/1260803449210-Updates-to-our-Learning-Environment) (Get Unstuck: concept review, solution, diff, FAQs)
- [Codecademy blog: New learning environment platform features](https://www.codecademy.com/resources/blog/new-learning-environment-platform-features)
- [Codecademy help: Understanding Code Errors](https://help.codecademy.com/hc/en-us/articles/220801027-Understanding-Code-Errors) (hints at the bottom of instructions, Get Code Solution, projects have no solution, reset)
- [Codecademy help: AI Features](https://help.codecademy.com/hc/en-us/articles/23400751016859-AI-Features-available-on-Codecademy) and [AI Learning Assistant Availability](https://help.codecademy.com/hc/en-us/articles/25489197408539-AI-Learning-Assistant-Availability)
- [Codecademy blog: GPT-4o AI Learning Assistant](https://www.codecademy.com/resources/blog/gpt4o-ai-learning-assistant) ("Explain code")
- [Codecademy help: Quizzes, Assessments and Exams](https://help.codecademy.com/hc/en-us/articles/15373426748187-Quizzes-Assessments-and-Exams-What-s-the-Difference)
- [Codecademy blog: Behind the Build, Designing Post-Quiz Review](https://www.codecademy.com/resources/blog/behind-the-build-designing-post-quiz-review)
- [Codecademy blog: Behind the Build, Smart Practice](https://www.codecademy.com/resources/blog/behind-the-build-smart-practice/)
- [Codecademy blog: Updates to projects & quizzes (2018)](https://www.codecademy.com/resources/blog/updates-improvements-to-projects-quizzes-march2018) (per-task hints, checklists)
- [Codecademy blog: Which type of project is right for me](https://www.codecademy.com/resources/blog/which-type-of-project-is-right-for-me) and [Portfolio projects in career paths](https://codecademy.com/resources/blog/portfolio-projects-in-career-paths/)
- [Codecademy blog: What to do when you're stuck](https://www.codecademy.com/resources/blog/what-to-do-when-youre-stuck) (walkthrough videos, Get Unstuck, "Oops" test errors)
- [Codecademy blog: Skip through course content](https://www.codecademy.com/resources/blog/skip-though-course-content-and-jump-to-individual-lessons)
- [Codecademy help: Badges and Weekly Targets](https://help.codecademy.com/hc/en-us/articles/115003050088-About-Badges-and-Weekly-Targets), [Weekly Targets](https://help.codecademy.com/hc/en-us/articles/360056218734-Weekly-Targets), [Skill Tracking FAQ](https://help.codecademy.com/hc/en-us/articles/39261734539035-Skill-Tracking-FAQ)
- [Medium/About Codecademy: Redesigning our learning environment (process)](https://medium.com/about-codecademy/redesigning-our-learning-environment-process-101d41eedd6) and [(what we learned)](https://medium.com/about-codecademy/redesigning-our-learning-environment-what-we-learned-a001fac0708f)
- Codecademy Learn Python 3 cheatsheets: [Hello World](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-hello-world/cheatsheet), [Control Flow](https://www.codecademy.com/learn/introduction-to-python-for-finance/modules/learn-python3-control-flow/cheatsheet), [Lists](https://www.codecademy.com/learn/introduction-to-python-for-finance/modules/learn-python3-lists/cheatsheet), [Loops](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-loops/cheatsheet), [Functions](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-functions/cheatsheet), [Strings](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-strings/cheatsheet), [Dictionaries](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-dictionaries/cheatsheet), [Code Challenges](https://www.codecademy.com/learn/learn-python-3/modules/cspath-code-challenges/cheatsheet)
- [Codecademy forums: How does Codecademy check my answer?](https://discuss.codecademy.com/t/how-does-codecademy-check-my-answer/338153) and ["Sometimes you need to write the exact code…"](https://discuss.codecademy.com/t/sometimes-you-need-to-write-the-exact-code-whoever-set-up-the-lesson-made-or-things-wont-work-right/631965), [FAQ: Errors in Python – Type Errors](https://discuss.codecademy.com/t/faq-errors-in-python-type-errors/561601), [walkthrough video mistakes](https://discuss.codecademy.com/t/rock-paper-or-scissors-project-walkthrough-video-mistakes/447114)
- Reviews and criticism: [checkthat.ai reviews](https://checkthat.ai/brands/codecademy/reviews), [boot.dev alternatives](https://www.boot.dev/blog/education/code-academy-alternatives), [coddy.tech vs Codecademy](https://coddy.tech/vs/codecademy), [courseverdict Learn Python 3](https://courseverdict.vercel.app/web-development/codecademy-learn-python-3), [skillscouter review](https://skillscouter.com/codecademy-review/), [RedGreenCode: The problem with Codecademy](https://www.redgreencode.com/the-problem-with-codecademy/)
- Research: [Kim & Ko 2017, A Pedagogical Analysis of Online Coding Tutorials (SIGCSE)](https://faculty.washington.edu/ajko/papers/Kim2017CodingTutorialEvaluation.pdf) and [summary blog post](https://medium.com/bits-and-behavior/coding-tutorials-the-good-the-bad-and-the-ugly-b45afc8821f6)
- Contrast: [DataCamp SCTs](https://instructor-support.datacamp.com/en/articles/2348740-submission-correctness-tests-deep-dive), [DataCamp skip/test-out](https://support.datacamp.com/hc/en-us/articles/33815612139799-What-Does-It-Mean-to-Skip-a-Course-on-DataCamp)
