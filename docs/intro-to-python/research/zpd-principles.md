# Designing "Intro to Python" for the Zone of Proximal Development

**Who this is for:** the curriculum designers and engineers building the Intro to Python section, plus the teacher who runs the campaign.
**What it is:** a research summary turned into design rules for our lessons, exercises, hints, quizzes, projects, and adaptive features.
**Read with:** `context/brief.md` (the ask, the world, the site) and `context/campaign-python-inventory.md` (the exact Python students meet in campaign Modules 1–2).

> **About the numbers.** Thresholds such as "≤ 2 hint levels" or "≥ 80 %" are our own starting heuristics for tuning. They are labeled *heuristic* wherever they appear. The research supports the direction of each rule, not the exact cut-offs.

---

## 0. The short version

1. **The ZPD is the gap between what a student can do alone and what they can do with help.** The goal is for campaign Python to sit in that gap: students can't quite do it alone yet, but they can do it with the help the game gives.
2. **Help has to respond to the student and fade over time.** Give more after a failure and less after a success. Every support needs a planned exit.
3. **Read before write.** Sequence every concept as predict/trace → explain → complete or assemble (Parsons) → modify → write from blank. PRIMM and Use-Modify-Create are our lesson skeletons.
4. **Worked examples first for novices, problems first for experienced students.** The same support that helps a novice can hurt an expert (the expertise-reversal effect), so support is layered and removable, never forced on everyone.
5. **Hints are a ladder: point, then teach, then show.** Showing the answer (the "bottom-out" hint) only counts as learning if it is followed by a your-turn variant.
6. **Opt-in help alone fails the students who need it most,** because novices avoid asking. Offer help proactively when signals show a student is stuck, and never penalize hint use.
7. **The story serves the learning.** Use Tor and Mar'tu as meaningful context, but keep lore off the critical path. Seductive details measurably hurt learning.
8. **Close the campaign gap deliberately:** dictionaries, functions as values, `random.randint`, `"█" * n`, `KeyError`. Revisit them with spaced retrieval, because the campaign leans on all of them.
9. **"Arriving in the ZPD" is measurable.** Every campaign part should be completable using the instructions and check messages, with an occasional hint. Show solution should be rare. Every line should be explainable in plain English afterward.
10. **Watch the affect.** Confusion that gets resolved is good. Prolonged confusion turns into frustration, and boredom is the most persistent and most harmful state. Offer a challenge to the bored and a hint to the stuck.

---

## 1. The zone of proximal development in plain language

### 1.1 The idea

Vygotsky defined the ZPD as "the distance between the actual developmental level as determined by independent problem solving and the level of potential development as determined through problem solving under adult guidance or in collaboration with more capable peers" (Vygotsky, 1978, p. 86).

Picture three rings around a learner:

| Ring | What it means | What it feels like |
|---|---|---|
| **Can do alone** | Independent level. Already mastered. | Easy, sometimes boring. |
| **Can do with help** (the ZPD) | Skills that are *maturing*: the student can't do it alone yet, but succeeds with the right support. | "This is hard, but I can figure it out." Curious, a bit confused, then a click. |
| **Can't do yet, even with help** | Too far beyond current understanding. Help just turns into copying. | Lost, frustrated, "I don't even know what to ask." |

The **"more knowledgeable other"** (MKO) is whoever or whatever provides the help: a teacher, a stronger peer, or a well-designed tool. **On our site the MKO is spread across many parts:** Mar'tu's lesson voice, the worked examples, the check messages, the friendly error explainer (`explain.ts`), the hint ladder, Show solution, classmates, and the teacher. Designing for the ZPD means designing *all* of these to work together.

### 1.2 Common misreadings (and what we do instead)

1. **"The ZPD is a difficulty level."** It is not a label on a task. It describes the *relationship between a learner and the available support*, and it moves as the learner grows. Chaiklin (2003) argues the concept is more precise than its popular use: it is about the *next* maturing capability, not "any task a student can do with help." *For us:* the "next capability" is fixed and concrete. It is the campaign's Python. Every lesson should move students toward it.
2. **"ZPD = scaffolding."** Vygotsky never used the scaffolding metaphor. Wood, Bruner & Ross (1976) introduced it, and conflating the two trivializes the ZPD (Smagorinsky, 2018). Scaffolding is *one way* of working inside the zone. *For us:* scaffolds are tools, and the ZPD is the target.
3. **"Any help is good help."** Help that does the thinking *for* the learner moves them nowhere. Support must be contingent and must fade (van de Pol et al., 2010).
4. **"Struggle is bad," or its mirror, "struggle is good."** Struggle is productive *only when support is in reach* (Kapur, 2016; Bjork & Bjork, 2011). That is what the zone is.
5. **"Measure only what they do alone."** The ZPD is defined by *assisted* performance too. Two students with the same unaided score can have very different zones. *For us:* log how much help a student needed, not just pass or fail.
6. **"One placement number per student."** A student can be advanced in strings and a novice in dictionaries. Place per skill, and keep placement provisional.

### 1.3 How students should feel when they reach the campaign's Python

> *"I recognize all of this. I can read every line and tell you what it does. A couple of parts make me think hard, and I might need a hint or two, but I know how to use the instructions and the error messages to get there."*

They should **not** feel *"I'm just typing what the instructions say"* (below the zone) or *"I have no idea what any of this means"* (beyond the zone).

---

## 2. Background: scaffolding, contingency, fading, and computing-specific methods

### 2.1 The six scaffolding functions (Wood, Bruner & Ross, 1976) mapped to our product

| Function | Meaning | Where it lives on our site |
|---|---|---|
| **Recruitment** | Get the learner interested in the task as the tutor defines it | Mar'tu's framing of *why* this matters on Tor ("the barrier fails without this, yes?"), kept to one or two lines |
| **Reduction in degrees of freedom** | Simplify the task so the learner handles only what they can | Starter code, fill-in-the-blank, Parsons blocks, one new idea per step |
| **Direction maintenance** | Keep the learner pursuing the goal | Numbered steps, check names as a visible to-do list, progress through the story |
| **Marking critical features** | Point out the difference between what the learner produced and the ideal | Check failure messages ("`spell_book` still has no key `'Glow'`"), highlighting the line in a traceback |
| **Frustration control** | Make failure less stressful without removing challenge | No penalty for hints or errors, normalizing error language, offering a hint after repeated failures |
| **Demonstration** | Model a solution so the learner can imitate it | Worked examples, the bottom-out hint, Show solution followed by a your-turn variant |

### 2.2 Contingency and fading

- **Contingency rule** (Wood, Wood & Middleton, 1978; Wood & Wood, 1999): after a success, give *less* help the next time; after a failure, give *more*. Our hint ladder and adaptive defaults implement this directly.
- **A caveat:** a 2025 preregistered direct replication (N = 285 three-year-olds) did *not* reproduce the original advantage of contingent instruction on later independent performance (Smit, de Kleijn, Wicherts & van de Pol, 2025). Contingency remains the consensus design principle in the scaffolding literature (van de Pol et al., 2010), and tutoring-system research supports it. We should still treat our contingency rules as hypotheses and *log the data to check them.*
- **Fading and transfer of responsibility:** van de Pol et al. (2010) define scaffolding by three features: contingency, fading, and transfer of responsibility to the learner. The **gradual release of responsibility** model is the classroom version: "I do, we do, you do" (Pearson & Gallagher, 1983).

### 2.3 Computing-education methods we will use

- **PRIMM: Predict, Run, Investigate, Modify, Make** (Sentance & Waite, 2017). It was evaluated in 13 schools with 493 students aged 11–14. PRIMM classes outperformed a control group on the post-test, and teachers reported it helped them teach mixed-ability classes (Sentance, Waite & Kallia, 2019). That age range and mixed-ability setting are ours.
- **Use-Modify-Create** (Lee et al., 2011) moves learners from using someone else's artifact, to modifying it, to creating their own. Lytle et al. (2019) compared a UMC-scaffolded progression against code-from-scratch in middle-school classes, looking at perceived difficulty and ownership. The lesson for us: the "Create" step has to be real, or scaffolding costs students their sense of ownership.
- **Parsons problems** (Parsons & Haden, 2006): students arrange given lines of code into a working program. Ericson, Margulieux & Rick (2017) found they took much less time than fixing or writing the equivalent code, with no significant difference in learning. **Adaptive Parsons problems** get easier when a student struggles and were more efficient but just as effective as writing code (Ericson, Foley & Rick, 2018). **Faded Parsons problems** blank out some tokens. They beat code tracing and code writing for learning programming patterns, improved general code writing, and students preferred them (Weinman, Fox & Hearst, 2021).
- **Worked examples and subgoal labels.** Conventional problem solving consumes the working memory novices need to learn (Sweller, 1988). Worked examples whose steps are grouped under labeled subgoals improved novices' performance on new programming tasks (Margulieux, Guzdial & Catrambone, 2012). A later intro-CS study found mixed results depending on whether labels were given or generated and on other material features (Morrison, Margulieux & Guzdial, 2015). Use labels, keep them consistent, and test.
- **Completion problems.** High-school students who practiced by *completing* partly written programs did better on program construction, and fewer dropped out, than students who wrote programs from scratch (van Merriënboer, 1990). The campaign's own exercises are completion problems, so this format is a good fit.
- **Tracing and the notional machine.** Many novices cannot reliably predict what short code does (Lister et al., 2004). Tracing and "explain in plain English" skills sit between knowing constructs and writing code, and they correlate with writing ability (Lopez et al., 2008). Novices pass through stages before they can reason about code abstractly (Lister, 2011). Explicitly teaching tracing, then syntax, then templates, then writing with templates improved completion and reduced errors (Xie et al., 2019). The *notional machine*, a simplified model of how the computer runs code, should be an explicit learning objective (du Boulay, 1986; Sorva, 2013). Program visualization tools such as Python Tutor make that model visible (Guo, 2013).

---

## 3. Design principles

Each principle gives the rule, its research basis, and what it means for our modules. "Heuristic" marks our own tunable numbers.

### P1. Aim every lesson at the campaign's Python, and close the gaps on purpose
**Rule:** Start from the campaign inventory. Every concept students will meet must be introduced, practiced, assessed, and revisited before they need it. Spend less time on syllabus topics the campaign doesn't use, unless they lead into one it does.
**Basis:** Xie et al. (2019) on explicitly identifying and sequencing skills. In ZPD terms, the zone is about the *next* capability (Chaiklin, 2003), and our next capability is concrete.
**Do:** Give dictionaries their own unit, placed before Functions finishes. It covers literals, `d["k"]` reads, nested `d["a"]["b"]`, `d[k] = v` writes, `in`/`not in`, looping over a list of dicts, and a dict holding a function. Add `random.randint` to Control Flow (its range is inclusive at both ends). Add `"█" * n` to Strings. Add **`KeyError`** and **`AttributeError`** to the Errors lesson, because dictionary work produces them constantly. Teach the campaign's idioms by name: return a comparison (`return roll >= required_roll`), store a return value and then pass it on, chain string methods, return early inside an `if`, and pass a function without parentheses.
**Watch out:** keep notation consistent with the campaign. The campaign uses `+` concatenation and `str()`. Introduce f-strings as an *alternative*, but make sure students fluently read `"Mana [" + filled + "] " + str(n)`.

### P2. Read before you write
**Rule:** For every new construct, sequence predict → trace → explain → complete or assemble → modify → write.
**Basis:** Lister et al. (2004); Lopez et al. (2008); Lister (2011); Xie et al. (2019).
**Do:** Each lesson opens with a **Predict** prompt (multiple choice or "type the output") *before* the student presses Run. After the run, ask: "Were you right? Which line surprised you?" Include **explain-in-plain-English** items, such as "In one sentence, what does `show_mana` do?", using multiple choice or short answer.
**Watch out:** prediction must be cheap to attempt and wrong answers free. It is a thinking prompt, not a test.

### P3. Use PRIMM / Use-Modify-Create as the default lesson skeleton
**Rule:** Predict → Run → Investigate (two to three questions) → Modify (change one thing) → Make (a small new thing in the same pattern).
**Basis:** Sentance et al. (2019); Lee et al. (2011); Lytle et al. (2019).
**Do:** Here is one way to template a lesson beat for `"█" * n`: *Predict* what `print("█" * 3)` shows. *Run* it. *Investigate:* what happens with `* 0`? With `* -1`? *Modify:* make a bar for 7 mana. *Make:* build `"█" * mana + "░" * (max_mana - mana)`.
**Watch out:** the Make step must leave real choices (names, numbers, flavor text) so students own it.

### P4. Make the notional machine visible
**Rule:** Show what the program *does* to its values, not just what it prints.
**Basis:** du Boulay (1986); Sorva (2013); Guo (2013).
**Do:** After a run, show an optional **"Mar'tu's ledger"** panel listing variables and dictionaries with their current values, with nested dicts expanded. For tricky lines, add trace tables ("fill in `mana` after each line"). For functions, show a call/return arrow ("`get_mana_bar` handed this string back to `show_mana`"). Give "a dict holding a function" its own diagram: the box holds the *function*, and `(...)` runs it.
**Watch out:** keep the panel collapsed by default for advanced students (P15). It is a support, not a requirement.

### P5. Worked examples with subgoal labels first, then fade
**Rule:** Novices study a fully worked, labeled example. Then they complete a version with one step removed, then two (backward fading), then solve independently. Fade on evidence, not on a fixed schedule.
**Basis:** Sweller (1988); Renkl & Atkinson (2003) on fading; Salden et al. (2010) on adaptive fading; Margulieux et al. (2012) and Morrison et al. (2015) on subgoals; van Merriënboer (1990) on completion problems; Chi et al. (1989) on self-explanation.
**Do:** Define a small set of **reusable subgoal labels** and use them in lessons, hints, *and* bridging notes for the campaign. Examples:
- *Get it out of the dictionary*, then *Compare*, then *Act on the result*.
- *Call the helper*, then *Store what it returns*, then *Pass it on*.

Attach a one-line self-explanation prompt to worked examples: "Why `<` and not `<=` here?"
**Watch out:** worked examples *hurt* students who already know the skill (P15). Let them skip straight to the problem.

### P6. Use Parsons problems (adaptive and faded) as the bridge from reading to writing
**Rule:** Before asking a novice to write a multi-line function from scratch, let them assemble it from blocks. Then let them complete a faded version with blanks.
**Basis:** Parsons & Haden (2006); Ericson et al. (2017, 2018); Weinman et al. (2021).
**Do:** Add an **"Assemble it instead"** option to multi-line writing exercises, especially `if/elif/else` chains and functions with a dictionary in the body. Make it adaptive: after two failed checks, remove a distractor block or merge two blocks. Include *indentation* as part of the puzzle, since it is a top novice error in Python. Use distractors drawn from real misconceptions: `<=` vs `<`, `spell["spell_function"]` without the call parentheses, and missing quotes around `"option 1"`.
**Watch out:** Parsons solving is not the end goal. The module's mastery check still requires typing.

### P7. Manage cognitive load deliberately
**Rule:** One new idea per step. Put the explanation next to the code it explains. Keep instructions short and numbered. Reuse familiar contexts so the setting itself isn't new information.
**Basis:** Sweller (1988); Mayer & Moreno (2003) on reducing split attention and redundancy and on segmenting; Kirschner, Sweller & Clark (2006) on guidance for novices.
**Do:** Keep lesson prose before the first interaction to about 120 words (*heuristic*). Use the campaign's numbered-step instruction style, so following numbered steps is itself practice for the campaign. Introduce new syntax in lessons, never for the first time inside a project. Projects *combine* known ideas.
**Watch out:** Mar'tu's accent and lore belong in the flavor lines, not inside the step that carries the instruction (P17).

### P8. Make support respond to the student: a hint ladder that answers on demand and offers itself when needed
**Rule:** Every exercise has a three-level hint ladder:
1. **Point.** Where to look: "Look at the line that compares mana, yes?"
2. **Teach.** The concept, with a tiny example that is *not* the answer: "`a < b` is True when a is smaller. For example `3 < 5`."
3. **Show.** The bottom-out line itself, then a follow-up task (P9).

Give more help after failure and less after success.
**Basis:** Wood et al. (1976, 1978); Wood & Wood (1999); VanLehn (2006) on point, teach, and bottom-out hint sequences; van de Pol et al. (2010); Koedinger & Aleven (2007) on the assistance dilemma.
**Do:** Students can open a hint at any time. The platform also **offers** the next hint (it does not force it) after N failed runs on the same check or M minutes without progress (*heuristic*: N = 3, M = 4). After a student passes without hints, the next similar exercise starts with less scaffolding, for example a blank function body instead of comments.
**Watch out:** see P16 on gaming. Require a run, or a few seconds, between hint levels.

### P9. Turn the bottom-out reveal into learning, not an exit
**Rule:** Seeing the answer is a worked example only if the student then engages with it. After any bottom-out hint or Show solution, give a short **your-turn variant**: same pattern, different values or names. Or ask a "which line does X?" question.
**Basis:** Shih, Koedinger & Scheines (2008) found bottom-out hints can act as worked examples when students spend time on them. Baker et al. (2004) found that rapid hint-clicking ("gaming the system") goes with substantially lower learning. Chi et al. (1989) showed self-explanation drives learning from examples.
**Do:** The site currently shows Show solution after five minutes on a part. Keep it, but (a) also unlock it after several failed runs, so stuck students aren't trapped by the clock; (b) don't allow a pasted solution to count as *mastery*; (c) follow it with the variant. Record "passed with reveal" separately for the teacher.
**Watch out:** never shame a student for revealing. Treat it as a normal, logged step.

### P10. Give feedback that names the gap and the next step, in plain language
**Rule:** Every check message should answer three questions. *Where am I going?* (the goal). *How am I doing?* (what the code did versus what was expected). *Where to next?* (one concrete action). Keep feedback about the task, never about the person.
**Basis:** Hattie & Timperley (2007), including the finding that feedback about the self is least effective; Shute (2008) on specific, elaborated, non-controlling feedback; Becker et al. (2019) on error message guidelines such as plain language, context, and examples; Marwan, Williams & Price (2019), where hints with textual explanations improved immediate performance.
**Do:** Write check messages in the form: "`cast_spell` used the spell when mana was 3 and the cost was 5. Check the mana comparison." Extend `explain.ts` so tracebacks name the line *and* the likely fix in student words (for example, *"KeyError: 'mana_cost' means the dictionary has no key spelled exactly like that. Check the spelling and the quotes."*). Avoid "Wrong" and "Try again" with nothing else.
**Watch out:** checks must not reject valid alternatives such as different flavor text, `x >= y` written as `not x < y`, or an extra print, unless the campaign truly requires the exact form. False negatives breed frustration.

### P11. Treat errors as information, and practice debugging on purpose
**Rule:** Build exercises *around* errors. Plant bugs, ask students to read the traceback, and let students make reasonable mistakes and then guide them to find and fix them. Praise the process, not ability.
**Basis:** Keith & Frese (2008) meta-analysis: error-management training, which combines active exploration with encouragement to make errors, transfers better to new tasks than error-avoidant training. Mathan & Koedinger (2005): letting students make reasonable errors and then coaching error detection beat immediate correction on problem solving, conceptual understanding, transfer, and retention. Mindset framing helps modestly and depends on context (Yeager et al., 2019; Sisk et al., 2018). One CS1 study combined mindset teaching with growth-oriented feedback (Cutts et al., 2010). "Wise feedback," which pairs high standards with assurance that the student can meet them, builds trust (Yeager et al., 2014).
**Do:** Add **"Broken spell"** debugging exercises in every unit. Make sure they include the campaign's likely bugs:
- `"░" * caster["max_mana"] - caster["mana"]`, missing parentheses, which raises a `TypeError`
- `<=` instead of `<`
- calling `spell["spell_function"]` without `(caster)`
- `user.clicked() == option 1` with the quotes missing
- an indentation slip

Use Mar'tu's voice for wise feedback: *"Your spell fizzled. Good. Now we can see why, yes? I would not give you this if I thought you could not mend it."*
**Watch out:** generic slogans ("You can do it!") without specific process feedback do little. Never say "you're a natural."

### P12. Use productive struggle in small, safe doses, always followed by consolidation
**Rule:** Sometimes let students *try before we teach*: a short, low-stakes challenge on a concept they haven't learned yet. Then deliver instruction that builds on what they attempted.
**Basis:** Kapur (2008, 2016): productive failure needs a problem-solving phase *and* a consolidation phase tied to student attempts. Unguided discovery alone is "unproductive failure." Bjork & Bjork (2011): difficulties are *desirable* only when the learner can respond to them successfully.
**Do:** Use this for conceptual hooks, not syntax. Example: "Mar'tu's chalk wall says 48, 48, 47, 46, 44, 41, 37. Before we learn lists, how would *you* store these?" Or: "Write a check that tells whether a d20 roll succeeds" before introducing returning a comparison. Then show the canonical approach and how it relates to student attempts. Cap the attempt time at about three minutes (*heuristic*). Nothing is graded.
**Watch out:** never use productive failure for a student who has shown frustration signals in the same session (P18).

### P13. Build in retrieval and spacing
**Rule:** Bring back earlier ideas, especially dictionaries and functions, in short recall prompts spread across later lessons.
**Basis:** Roediger & Karpicke (2006) on the testing effect; Cepeda et al. (2006) on distributed practice; Dunlosky et al. (2013), who rate practice testing and distributed practice as the highest-utility techniques.
**Do:** Each lesson opens with one or two **"Mar'tu remembers…"** recall questions from at least two lessons back. Dictionaries reappear in every unit after they are introduced, for example a dict of shop prices in Loops or a dict of options in Functions. Run a cumulative **Campaign Readiness Check** before campaign Module 2 (section 4.5).
**Watch out:** recall prompts are short and unscored, and students can skip them.

### P14. Require mastery, with multiple routes and an escape hatch
**Rule:** Each module ends with a mastery check. Failing a skill routes the student to *targeted* review: a different explanation, then a parallel item. No one is stuck forever.
**Basis:** Bloom (1984); Kulik, Kulik & Bangert-Drowns (1990), a meta-analysis of 108 mastery-learning evaluations with positive effects on exam performance; Corbett & Anderson (1995) on estimating mastery per skill; Beck & Gong (2013) on "wheel-spinning": students who don't master a skill fairly quickly often never do without a change in approach.
**Do:** Track mastery per skill (for example `dict-read`, `dict-write`, `elif-chain`, `return-comparison`, `func-as-value`). If a student fails the same skill after about 10 attempts (*heuristic*, from Beck & Gong), stop serving more of the same. Switch to a different representation (a Parsons version, a ledger trace, or a worked example) and **flag it to the teacher**.
**Watch out:** don't let mastery gates block the *story*. A student can continue the narrative while a skill stays flagged for review.

### P15. Adapt to prior knowledge, because the same support helps novices and hurts experts
**Rule:** Fit support to the learner's current expertise in each skill. Make worked examples, extra explanations, and step-by-step comments *removable*.
**Basis:** Kalyuga, Ayres, Chandler & Sweller (2003) and Kalyuga (2007) on the expertise-reversal effect. Kalyuga & Sweller (2004) on rapid "first-step" diagnostic tests that agree closely with longer tests and can drive adaptation. Salden et al. (2010) on adaptive fading.
**Do:** See section 5. In short: per-module **Quick Check** test-outs, a support level per skill, "start from blank" versus "start from scaffold" modes for the same exercise, and extension Trials.

### P16. Make help easy and safe to take, and hard to game
**Rule:** Never penalize hints or reveals in anything a student sees. Offer help proactively, because novices avoid asking. Prevent rapid click-through of the ladder.
**Basis:** Aleven et al. (2003): learners often use on-demand help poorly, avoiding it when they need it or abusing it. Baker et al. (2004) on gaming. Koedinger & Aleven (2007) on the assistance dilemma. Kirschner & van Merriënboer (2013): novices are poor judges of what help they need.
**Do:** Attach no score or star penalty to hints. Show hint use only to the teacher. Require at least one run, or about 10 seconds (*heuristic*), between hint levels. Phrase proactive offers in Mar'tu's voice: *"You have been staring at that colon for a while. Want a nudge, yes?"*

### P17. Let the story serve the learning
**Rule:** Use Tor, the party, and Mar'tu as *meaningful context* for the data and the tasks. Keep jokes and lore off the critical path of an explanation. Write instructions in plain, friendly second person.
**Basis:** Walkington (2013): personalizing problems to students' interests improved performance and learning in an Algebra I tutor. Mayer et al. (2004): conversational, personalized wording improves transfer. Harp & Mayer (1998) and Rey (2012): interesting but irrelevant "seductive details" reduce learning. Adams et al. (2012): narrative games were *less* effective than plain slideshows for retention and transfer, so narrative is not automatically a win.
**Do:**
- Use the world as *data*: party stats dicts, the chalk-wall list, spell books, d20 skill checks, Lucky's "What's in it for me?" as a string-method target, Bomb Shell's clipped sentences as `.split()` practice.
- Put flavor in a scene caption or a single Mar'tu line *before or after* the instruction block, never in the middle of it.
- Keep Mar'tu's ", yes?" tic to roughly one per beat (*heuristic*).
- Never quiz lore.

**Watch out:** the accent must not make instructions harder to read for English learners or weak readers. Keep the instructions themselves in standard English.

### P18. Aim for "confused but progressing," and watch for boredom and stuck frustration
**Rule:** Design for engaged concentration with resolvable confusion. Detect and break up both boredom and prolonged frustration.
**Basis:** D'Mello & Graesser (2012): confusion arises at impasses and helps when resolved. Baker et al. (2010): boredom was the most persistent state and was associated with poorer learning and gaming, while frustration was less harmful than expected. Bosch & D'Mello (2017): in 99 Python novices, confusion and frustration often co-occurred, as did curiosity and engagement. Shernoff et al. (2003): engagement peaks when challenge and skill are both high and in balance, the task is relevant, and students have some control.
**Do:**
- If a student passes quickly with no hints across a run of exercises, offer a Trial (boredom risk).
- If a student keeps failing with no progress on the checks, offer a hint, a different representation, or a break (frustration risk).
- At the end of each lesson, ask one question: "That felt: too easy / just right / too hard."

### P19. Teach students to work with code they didn't write
**Rule:** Students must practice using helper functions they didn't write, reading comments, and telling apart the lines to change from the lines to leave alone. The campaign demands all three.
**Basis:** Xie et al. (2019) on comprehending and using templates; the "Use" stage of UMC (Lee et al., 2011); reading-before-writing research (Lopez et al., 2008).
**Do:** Give each unit at least one exercise that calls a provided "engine helper" (in our world, for example `show_on_ley_board(text)`), with a comment like `# This function is already finished`. Ask: "Which lines should you change? Which should you leave?" Practice following the campaign's instruction style: numbered steps, "replace the 0 with…", "replace `pass` with…".

### P20. Design for many kinds of learners from the start
**Rule:** Offer multiple representations (text, diagram, analogy, trace), multiple ways to engage (story, puzzle, challenge), and multiple ways to show understanding (predict, assemble, explain, write).
**Basis:** CAST Universal Design for Learning Guidelines (version 3.0, 2024). Liffiton et al. (2023) on putting guardrails on AI help so it supports learning without handing out solutions.
**Do:**
- Add an "Explain it another way" option on every concept, drawing on a reviewed bank: a box analogy, a ledger trace, a tiny game example, or an everyday analogy.
- Add hover glossaries for terms such as *parameter*, *return*, and *key*.
- Support read-aloud and keyboard navigation.
- If we add AI-generated explanations, constrain them: use course notation only, give no full solutions, and spot-check them against the lesson.

---

## 4. Operational definition: arriving at the campaign's Python inside the ZPD

### 4.1 The target in one sentence

> A student is in the ZPD for the campaign when they can **read and explain every line** of a campaign part's starter code, **write the one-line edits unaided**, and **complete the full part using only the campaign's built-in support** (instructions, check messages, the error explainer, and the occasional hint or nudge), with the **multi-concept composition** in the hardest parts feeling like a real but winnable stretch.

### 4.2 What support the campaign gives (fixed, so we rehearse with it)

The campaign provides:
- numbered instructions that often spell out the exact code to type
- commented starter code
- check names and failure messages
- the friendly error explainer
- **Show solution** after five minutes
- the teacher and classmates

Because this support is fixed, Intro to Python should **rehearse working with exactly these supports**: reading numbered steps, mapping "replace X with Y" onto code, reading a failed-check message, and using a traceback. This is a large part of what "arriving inside the ZPD" means for us.

**A note for the teacher:** the campaign's instructions are very explicit and often give the literal code. For experienced students that can push the campaign *below* their ZPD (they just follow steps, get bored, and learn little). Novices can likewise complete steps by copying without understanding. Two cheap fixes follow from the expertise-reversal research: an optional **"instructions-light" toggle** in the campaign (show only the goal and the checks), and **"why?" self-explanation prompts** after key parts.

### 4.3 The three bands, with campaign Python as the yardstick

| Band | The student can… | Concrete campaign examples |
|---|---|---|
| **A. Unaided (independent level)**, the floor every student should reach | Read and predict short code. Write single statements and one-line edits. Fix common slips from the error message. | Replace `pass` with `party.move("left")`. Store a return value and pass it on (`dialogue = get_dialogue_prompt_string()` then `print_prompt(dialogue)`). Read `.lower().capitalize()`. Put `"option 1"` with quotes into `user.clicked() == ...`. Use `return random.randint(1, die_size)` and know its range is 1 to `die_size` *inclusive*. Write `return roll >= required_roll`. Read and write `caster["mana"]` and `spell_book[spell_name] = spell`. Write `"█" * caster["mana"]`. Read `+ str(...) +` concatenation. Explain what `for member in party.members:` does. Fix a `NameError`, a missing quote or colon, an indentation error, `str + int`, and a `KeyError`. |
| **B. With the campaign's built-in support** (the ZPD proper) | Combine several known pieces into one function body by following numbered steps. Use helpers they didn't write. | *spell-book:* fill a dict literal from parameters, then store it by key. *mana-bars:* build the bar with the correct `max_mana - mana` expression, then wire `show_mana`. *hold-the-barrier:* a full `if/elif/else` using nested `caster["abilities"]["magical_affinity"]`, calling `spell["spell_function"](caster)`, subtracting mana, and redrawing. *dialogue-options:* a four-branch `elif` chain plus `make_option_green()`. |
| **C. Stretch** (understood with explanation, not yet authored alone) | Explain these ideas when asked, but not invent them unprompted yet. | Functions as values: passing `strengthen_magic` without parentheses, and a dict holding a function. Operator precedence in `"░" * (a - b)`. The `<` versus `<=` boundary ("exactly enough mana can still cast"). An early `return` as a guard clause. Why the bottom loop adds a spell to every member. |
| *Out of zone: too far* | — | Writing an event-driven program from a blank file. Reading engine internals. Classes and closures. If students land here, Intro to Python under-prepared them. |
| *Out of zone: too easy* | — | Retyping given code with no decisions. If advanced students land here, offer the instructions-light toggle. |

### 4.4 Readiness map by campaign part (what to aim for)

| Campaign part | Target band for a typical student | Most likely friction to rehearse in Intro to Python |
|---|---|---|
| `program-movement` | A | Indentation after `def`. Replacing `pass`. |
| `program-dialogue-prompt` | A | Storing a return value, then passing the variable. Method chaining. |
| `program-dialogue-options` | A, with B for the full chain | Quotes around `"option 1"`. Adding a statement inside each branch. |
| `skill-checks` | A | `randint` inclusive range. Returning a comparison instead of an `if` returning `True`/`False` (accept both; teach the short form). |
| `spell-book` | B | Dict literal values from parameters. Assignment by key. Passing a function without `()`. |
| `mana-bars` | B | `"░" * (max - mana)` precedence. Wiring two functions together. |
| `hold-the-barrier` | B, top of the zone | Nested dict access. `if/elif/else` order. `<` vs `<=`. Calling a stored function. Reassigning `caster["mana"] = caster["mana"] - cost`. |

### 4.5 The Campaign Readiness Check

Run this at the end of Intro to Python and again as a spaced check before campaign Module 2. It has 10–12 short items, done unaided (no hints), using *our-world analogs* rather than the campaign's exact code:

1. Predict the output of a `+`/`str()` concatenation, for example `"Mana: " + str(7) + "/" + str(10)`.
2. Replace `pass` with a helper call that takes a string argument.
3. Store a function's return value, then pass it to another function.
4. Predict `True`/`False` for `return roll >= needed` at the boundary values (`roll == needed`, one below, one above).
5. Trace a three-branch `if/elif/else` on string equality and say which branch runs.
6. Dictionaries: read a key, read a nested key, write a key, and say whether `"x" in d` is true or false.
7. Predict `"█" * 3 + "░" * 2`, and fix `"░" * 10 - 3`.
8. Say which values `random.randint(1, 6)` can return.
9. Explain the difference between `spells["glow"]` and `spells["glow"](hero)`.
10. Trace a `for` loop over a list of dicts that calls a function on each one.
11. Read a traceback (`KeyError`, `TypeError`, `NameError`) and fix the bug.
12. Predict the value after `hero["mana"] = hero["mana"] - 3`.

**Heuristic pass criteria:** at least 80 % correct unaided. Any missed *skill* routes to its review lesson (P14). Then a supported mini-boss, a "hold-the-barrier"-like function in our world, is completed with at most two hint levels and no full reveal.

### 4.6 Signals the teacher can watch

All signals are per student and per skill. They use the classroom progress API keyed by join code and anonymous ID, and **never store student names in the repo**. Thresholds are *heuristics* to tune after the first class.

| Signal | In zone (green) | Below zone, under-challenged (blue) | Above zone or stuck (amber or red) |
|---|---|---|---|
| Runs before passing a part | 2–6, with *different* errors and recovery | 1 run on every part, many parts in a row | 8 or more, or the same error 3 or more times in a row (wheel-spinning) |
| Hint depth used | Mostly level 1–2 | None, ever | Bottom-out on most parts |
| Hint timing | Seconds to minutes between levels | — | Under 10 s between levels (gaming) |
| Show solution | 1 or fewer per module | 0 | More than 1 per module, or used before any run |
| Idle time on a part | Short pauses between runs | Very fast completion | More than about 2× the expected time with no runs (stuck and not asking) |
| Predict-prompt accuracy | 60–90 % | Above 90 % → offer a Trial | Below 50 % → tracing support (ledger, trace tables) |
| Recall items ("Mar'tu remembers") | Mostly correct | All correct, fast | Repeated misses on the same skill → spaced review |
| End-of-lesson pulse | "Just right" | "Too easy" (check against performance) | "Too hard," especially paired with red signals |
| Teacher observation | Questions sound like "Why does…?" | Helping neighbors, finishing early | Questions sound like "What do I type?"; can't explain a line they wrote |

Combine the self-report pulse with the performance data. Novices are often poorly calibrated (Kirschner & van Merriënboer, 2013), so "too easy" plus red signals means "copying," not "bored."

### 4.7 What it should feel like (affect target)

Mostly **engaged concentration**, with **short confusion that resolves** ("Oh, the box holds the *function*!") and **rare, brief frustration**. Boredom is a signal to offer challenge, and repeated confusion followed by frustration is a signal to change representation (D'Mello & Graesser, 2012; Baker et al., 2010; Bosch & D'Mello, 2017).

---

## 5. Supporting the least comfortable and the most experienced without hurting either

### 5.1 Why one path can't fit everyone: the expertise-reversal effect

Techniques that help novices, such as worked examples, integrated step-by-step explanations, and heavy guidance, **lose their benefit and can become harmful** as learners gain expertise. Experts must process redundant information against knowledge they already have, which adds load (Kalyuga et al., 2003; Kalyuga, 2007). The reverse also holds: minimal guidance that suits experts overloads novices (Kirschner, Sweller & Clark, 2006). Adaptive fading of support, based on each learner's performance, outperformed fixed fading (Salden et al., 2010).

There are **two opposite failure modes** to design against:
- **Forced redundancy for experts:** every student must read the full explanation and do every warm-up. Experienced students get bored, learn less, and disengage.
- **Opt-in-only support for novices:** help exists but is hidden behind buttons. Novices tend not to seek help, or use it poorly (Aleven et al., 2003), and are poor judges of what they need (Kirschner & van Merriënboer, 2013).

**The resolution:** set *defaults* by evidence (placement plus in-app signals), let everyone **turn support up or down**, and **offer** support proactively when signals warrant it.

### 5.2 A layered design for each lesson step

| Layer | Content | Novice default | Experienced default |
|---|---|---|---|
| Core | Goal, numbered steps, starter code, checks | Shown | Shown, with "start from blank" offered |
| Worked example | Full labeled example and self-explanation prompt | Shown first | Collapsed ("Show me an example") |
| Another way to see it | Analogy, diagram, ledger trace, everyday example | Offered after the first failed check | Hidden, available |
| Why does this work? | Deeper detail, such as precedence or how `in` works on dict keys | Hidden | Offered as a sidebar |
| Assemble it instead | Parsons or faded Parsons version | Offered on multi-line tasks | Hidden |
| Hint ladder | Point → teach → show, then a your-turn variant | On demand plus proactive offers | On demand |
| Trial | An extension challenge | After mastery | After mastery or test-out |

### 5.3 Placement and test-out

- **Placement is provisional.** Use the paper assessment only to set *initial defaults*. The teacher suspects some students had help on it, so confirm placement inside the app with the first Quick Check.
- **Quick Check per module.** This is a rapid "first-step" diagnostic (Kalyuga & Sweller, 2004): 3–6 short items covering the module's skills, *including the campaign's specific idioms* (an experienced student may know Python but not `return a >= b` or functions stored in a dict). It takes about five minutes.
  - **Pass all skills:** the module is marked *Tested out*. The student gets a one-screen story recap ("Mar'tu's notes") so the narrative stays continuous, and unlocks Trials.
  - **Pass some skills:** skip only those lessons and do the rest.
  - **Fail:** no penalty. The student continues normally with the support level matched to what the Quick Check showed.
- **Anyone can take a Quick Check,** including novices who feel confident. It doubles as retrieval practice (P13).
- **Tested-out skills are re-verified** by a spaced item later and by the Campaign Readiness Check, so test-out isn't a permanent unverified pass.
- **Re-entry:** a tested-out student can always open a lesson.

### 5.4 On-ramps for the least comfortable students

- **Warm-ups** before Unit 1: what a string is, why quotes matter, what an error message looks like, and how Run works. These are optional, and the default for students who placed as novices.
- Worked example first, faded completion problems, an **Assemble it instead** option, and **Explain it another way** on every concept.
- More frequent and smaller checkpoints. The ledger panel opens by default.
- Glossary hovers, read-aloud, and no time pressure.
- Your-turn variants after every reveal, so a reveal leads to the next attempt instead of being a dead end.
- Proactive hint offers and teacher flags for wheel-spinning.

### 5.5 Extensions for the most experienced students

Extensions should **deepen and broaden**, not just race ahead:
- **Trials** (the syllabus's optional code challenges, each with an advanced variant). Examples: write a function from a blank file, refactor a four-branch `elif` into a dict lookup, handle edge cases (negative mana, a missing spell name), and write your own checks (asserts) for a function.
- **Instructions-light mode** for lessons and, if the teacher chooses, the campaign itself.
- **"Why does this work?"** sidebars on precedence, mutability, and why dict keys must be unique.
- **Optional peer-mentor role** (Vygotsky's "more capable peers"), *opt-in only*. Experienced students are not unpaid assistants by default.

### 5.6 Keep it fair and dignified

- Give paths neutral names. No "remedial" labels. All students see the same story beats.
- All paths **converge at the same Campaign Readiness Check.** The routes differ, but the destination is the same.
- No public leaderboards or speed rankings, and hint use is private. Shernoff et al. (2003) link engagement to a sense of control, and comparison pressure works against novices.

### 5.7 Feature check: who it helps, what it risks, and the mitigation

| Feature | Helps | Risk to others | Mitigation |
|---|---|---|---|
| Worked examples | Novices | Redundant for experts | Collapsed for experts; skippable |
| Parsons and Assemble it instead | Novices, students with syntax trouble | Experts find it slow | Opt-in for experts; typing still required for mastery |
| Ledger and trace panel | Novices, visual learners | Visual clutter | Collapsible; remembers the choice |
| Quick Check test-out | Experts | Novices might over-claim | Provisional; spaced re-verification; no penalty for failing |
| Proactive hint offers | Novices who avoid help | Annoying for experts | Only after failure or idle signals; easy to dismiss |
| Instructions-light mode | Experts | Novices toggling it on and getting lost | Suggest it only after mastery; one click to turn off |
| Trials | Experts | Novices feeling left behind | Unlock for everyone after mastery; framed as optional side quests |
| Story flavor | Engagement for all | Seductive details hurt learning | Kept outside instruction blocks; never quizzed |

---

## 6. Anti-patterns to avoid

1. **Treating the ZPD as a difficulty slider.** The zone is the learner and the support together. Tune the support, not just the task.
2. **Scaffolds that never fade.** If every exercise through Unit 5 still says "replace the 0 with X," students learn to follow instructions, not to program.
3. **A blank editor for novices** ("just try to write it"). Minimal guidance overloads beginners (Kirschner et al., 2006).
4. **Forcing every student through every explanation.** Expertise reversal: it bores experts and can lower their learning.
5. **Hiding all help behind opt-in buttons.** Novices tend not to seek help (Aleven et al., 2003).
6. **Hint ladders that can be clicked through in two seconds,** and reveals that count as mastery (Baker et al., 2004).
7. **Penalties for hints or errors** (lost stars, lower scores). They breed help avoidance and fear of running code.
8. **Show solution as a dead end** (copy, paste, Continue). Always follow it with a your-turn variant (Shih et al., 2008).
9. **Vague or person-focused feedback:** "Wrong," "Try again," "Great job, you're so smart!" (Hattie & Timperley, 2007).
10. **Over-strict checks** that reject correct alternatives, or checks on incidental formatting. These are false negatives that cause frustration.
11. **Seductive details:** a lore joke in the middle of an explanation, story text between code and its explanation, or quizzes on lore (Harp & Mayer, 1998; Rey, 2012).
12. **Assuming narrative equals engagement equals learning.** Narrative wrappers alone don't improve learning (Adams et al., 2012). The story has to give the data and the tasks meaning.
13. **New syntax introduced inside a project.** Projects combine known ideas; lessons introduce new ones.
14. **Testing only writing.** The campaign demands *reading* engine code. Assess tracing and explaining too (Lopez et al., 2008).
15. **Massed practice with no revisiting.** For example, dictionaries taught once in Unit 3 and next seen in campaign Module 2 (Cepeda et al., 2006).
16. **Mastery gates with no escape hatch.** Repeating the same item 15 times is wheel-spinning (Beck & Gong, 2013). Change the representation and flag the teacher.
17. **Notation drift.** Teaching f-strings everywhere and `+` concatenation never, when the campaign uses `+` and `str()`. Or AI-generated explanations that use idioms the course never taught.
18. **Mindset slogans as a substitute for good design.** Effects are modest and depend on context (Sisk et al., 2018; Yeager et al., 2019). Specific process feedback and solvable challenges do the real work.
19. **Unbounded "productive failure."** Struggle without timely consolidation is unproductive failure (Kapur, 2016).
20. **Public comparison:** leaderboards, speed badges, or showing who used hints.
21. **Recording identifying data:** student names in the repo or in logs. Use join codes and anonymous IDs only.

---

## 7. Open questions to measure after the first run

- Do proactive hint offers raise learning, or just completion? Compare hint-level-3 users' performance on the next, unassisted, parallel item.
- Is the contingency rule (less help after success) actually helping our students, given the 2025 replication failure? A/B test the default scaffold after a hint-free pass.
- Are Quick Check test-outs accurate? Compare test-out students' Campaign Readiness Check scores and campaign signals with students who did the full module.
- Which "Explain it another way" representations get used and are followed by passes? Retire the ones that don't help.
- Does the instructions-light campaign toggle reduce boredom signals for experienced students without raising their reveal rate?

---

## References

**ZPD and scaffolding**
- Vygotsky, L. S. (1978). *Mind in Society: The Development of Higher Psychological Processes* (M. Cole, V. John-Steiner, S. Scribner, & E. Souberman, Eds.). Harvard University Press. (ZPD definition on p. 86; excerpt: https://newlearningonline.com/new-learning/chapter-8/vygotsky-on-the-zone-of-proximal-development)
- Chaiklin, S. (2003). The zone of proximal development in Vygotsky's analysis of learning and instruction. In A. Kozulin et al. (Eds.), *Vygotsky's Educational Theory in Cultural Context* (pp. 39–64). Cambridge University Press. https://doi.org/10.1017/CBO9780511840975.004
- Smagorinsky, P. (2018). Deconflating the ZPD and instructional scaffolding: Retranslating and reconceiving the zone of proximal development as the zone of next development. *Learning, Culture and Social Interaction, 16*, 70–75. https://doi.org/10.1016/j.lcsi.2017.10.009
- Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89–100. https://doi.org/10.1111/j.1469-7610.1976.tb00381.x
- Wood, D., Wood, H., & Middleton, D. (1978). An experimental evaluation of four face-to-face teaching strategies. *International Journal of Behavioral Development, 1*(2), 131–147. https://doi.org/10.1177/016502547800100203
- Smit, N., de Kleijn, R., Wicherts, J., & van de Pol, J. (2025). What it takes to tutor: A preregistered direct replication of Wood, Wood & Middleton (1978). *Journal of Educational Psychology, 117*(8), 1313–1329. https://doi.org/10.1037/edu0000965 (title abbreviated from index records)
- Wood, H., & Wood, D. (1999). Help seeking, learning and contingent tutoring. *Computers & Education, 33*(2–3), 153–169. https://doi.org/10.1016/S0360-1315(99)00030-5
- van de Pol, J., Volman, M., & Beishuizen, J. (2010). Scaffolding in teacher–student interaction: A decade of research. *Educational Psychology Review, 22*(3), 271–296. https://doi.org/10.1007/s10648-010-9127-6
- Pearson, P. D., & Gallagher, M. C. (1983). The instruction of reading comprehension. *Contemporary Educational Psychology, 8*(3), 317–344. https://doi.org/10.1016/0361-476X(83)90019-X (also issued as Center for the Study of Reading Technical Report No. 297)

**Computing-education methods**
- Sentance, S., & Waite, J. (2017). PRIMM: Exploring pedagogical approaches for teaching text-based programming in school. *WiPSCE '17*, 113–114. https://doi.org/10.1145/3137065.3137084
- Sentance, S., Waite, J., & Kallia, M. (2019). Teaching computer programming with PRIMM: A sociocultural perspective. *Computer Science Education, 29*(2–3), 136–176. https://doi.org/10.1080/08993408.2019.1608781
- Lee, I., Martin, F., Denner, J., Coulter, B., Allan, W., Erickson, J., Malyn-Smith, J., & Werner, L. (2011). Computational thinking for youth in practice. *ACM Inroads, 2*(1), 32–37. https://doi.org/10.1145/1929887.1929902
- Lytle, N., Cateté, V., Boulden, D., Dong, Y., Houchins, J., Milliken, A., Isvik, A., Bounajim, D., Wiebe, E., & Barnes, T. (2019). Use, Modify, Create: Comparing computational thinking lesson progressions for STEM classes. *ITiCSE '19*, 395–401. https://doi.org/10.1145/3304221.3319786
- Parsons, D., & Haden, P. (2006). Parson's programming puzzles: A fun and effective learning tool for first programming courses. *ACE 2006, CRPIT 52*, 157–163. https://crpit.scem.westernsydney.edu.au/abstracts/CRPITV52Parsons.html
- Ericson, B. J., Margulieux, L. E., & Rick, J. (2017). Solving Parsons problems versus fixing and writing code. *Koli Calling '17*, 20–29. https://doi.org/10.1145/3141880.3141895
- Ericson, B. J., Foley, J. D., & Rick, J. (2018). Evaluating the efficiency and effectiveness of adaptive Parsons problems. *ICER '18*, 60–68. https://doi.org/10.1145/3230977.3231000
- Weinman, N., Fox, A., & Hearst, M. A. (2021). Improving instruction of programming patterns with faded Parsons problems. *CHI '21*. https://doi.org/10.1145/3411764.3445228
- Margulieux, L. E., Guzdial, M., & Catrambone, R. (2012). Subgoal-labeled instructional material improves performance and transfer in learning to develop mobile applications. *ICER '12*, 71–78. https://doi.org/10.1145/2361276.2361291
- Morrison, B. B., Margulieux, L. E., & Guzdial, M. (2015). Subgoals, context, and worked examples in learning computing problem solving. *ICER '15*, 21–29. https://doi.org/10.1145/2787622.2787733
- van Merriënboer, J. J. G. (1990). Strategies for programming instruction in high school: Program completion vs. program generation. *Journal of Educational Computing Research, 6*(3), 265–285. https://doi.org/10.2190/4NK5-17L7-TWQV-1EHL
- Lister, R., et al. (2004). A multi-national study of reading and tracing skills in novice programmers. *ITiCSE-WGR '04*, 119–150. https://doi.org/10.1145/1044550.1041673
- Lopez, M., Whalley, J., Robbins, P., & Lister, R. (2008). Relationships between reading, tracing and writing skills in introductory programming. *ICER '08*, 101–112. https://opus.lib.uts.edu.au/handle/10453/10806
- Lister, R. (2011). Concrete and other neo-Piagetian forms of reasoning in the novice programmer. *ACE 2011, CRPIT 114*, 9–18. https://crpit.scem.westernsydney.edu.au/abstracts/CRPITV114Lister.html
- Xie, B., Loksa, D., Nelson, G. L., Davidson, M. J., Dong, D., Kwik, H., Tan, A. H., Hwa, L., Li, M., & Ko, A. J. (2019). A theory of instruction for introductory programming skills. *Computer Science Education, 29*(2–3), 205–253. https://doi.org/10.1080/08993408.2019.1565235
- du Boulay, B. (1986). Some difficulties of learning to program. *Journal of Educational Computing Research, 2*(1), 57–73. Reprinted in E. Soloway & J. Spohrer (Eds.), *Studying the Novice Programmer* (1989, pp. 283–299). Record: https://bibsonomy.org/bibtex/11972f1aae58e62b81f3c898244e2c33
- Sorva, J. (2013). Notional machines and introductory programming education. *ACM Transactions on Computing Education, 13*(2), Article 8. https://doi.org/10.1145/2483710.2483713
- Guo, P. J. (2013). Online Python Tutor: Embeddable web-based program visualization for CS education. *SIGCSE '13*, 579–584. https://doi.org/10.1145/2445196.2445368
- Becker, B. A., Denny, P., et al. (2019). Compiler error messages considered unhelpful: The landscape of text-based programming error message research. *ITiCSE-WGR '19*, 177–210. https://doi.org/10.1145/3344429.3372508
- Marwan, S., Williams, J. J., & Price, T. W. (2019). An evaluation of the impact of automated programming hints on performance and learning. *ICER '19*, 61–70. https://doi.org/10.1145/3291279.3339420
- Cutts, Q., Cutts, E., Draper, S., O'Donnell, P., & Saffrey, P. (2010). Manipulating mindset to positively influence introductory programming performance. *SIGCSE '10*, 431–435. https://doi.org/10.1145/1734263.1734409
- Bosch, N., & D'Mello, S. (2017). The affective experience of novice computer programmers. *International Journal of Artificial Intelligence in Education, 27*(1), 181–206. https://doi.org/10.1007/s40593-015-0069-5
- Liffiton, M., Sheese, B., Savelka, J., & Denny, P. (2023). CodeHelp: Using large language models with guardrails for scalable support in programming classes. *Koli Calling '23*. https://arxiv.org/abs/2308.06921

**Cognitive load, worked examples, expertise reversal**
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science, 12*(2), 257–285. https://doi.org/10.1207/s15516709cog1202_4
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition: A cognitive load perspective. *Educational Psychologist, 38*(1), 15–22. https://doi.org/10.1207/S15326985EP3801_3
- Salden, R. J. C. M., Aleven, V., Schwonke, R., & Renkl, A. (2010). The expertise reversal effect and worked examples in tutored problem solving. *Instructional Science, 38*(3), 289–307. https://doi.org/10.1007/s11251-009-9107-8
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist, 38*(1), 23–31. https://doi.org/10.1207/S15326985EP3801_4
- Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. *Educational Psychology Review, 19*(4), 509–539. https://doi.org/10.1007/s10648-007-9054-3
- Kalyuga, S., & Sweller, J. (2004). Measuring knowledge to optimize cognitive load factors during instruction. *Journal of Educational Psychology, 96*(3), 558–568. https://doi.org/10.1037/0022-0663.96.3.558
- Mayer, R. E., & Moreno, R. (2003). Nine ways to reduce cognitive load in multimedia learning. *Educational Psychologist, 38*(1), 43–52. https://doi.org/10.1207/S15326985EP3801_6
- Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does not work. *Educational Psychologist, 41*(2), 75–86. https://doi.org/10.1207/s15326985ep4102_1
- Kirschner, P. A., & van Merriënboer, J. J. G. (2013). Do learners really know best? Urban legends in education. *Educational Psychologist, 48*(3), 169–183. https://doi.org/10.1080/00461520.2013.804395
- Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R. (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science, 13*(2), 145–182. https://education.asu.edu/lcl/publications/chi-m-t-h-bassok-m-lewis-m-reimann-p-glaser-r-1989-self-explanations-how-students

**Productive failure, desirable difficulties, retrieval, spacing, mastery**
- Kapur, M. (2008). Productive failure. *Cognition and Instruction, 26*(3), 379–424. https://doi.org/10.1080/07370000802212669
- Kapur, M. (2016). Examining productive failure, productive success, unproductive failure, and unproductive success in learning. *Educational Psychologist, 51*(2), 289–299. https://doi.org/10.1080/00461520.2016.1155457
- Bjork, E. L., & Bjork, R. A. (2011). Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In M. A. Gernsbacher et al. (Eds.), *Psychology and the Real World* (pp. 56–64). Worth. https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science, 17*(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest, 14*(1), 4–58. https://doi.org/10.1177/1529100612453266
- Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective as one-to-one tutoring. *Educational Researcher, 13*(6), 4–16. https://doi.org/10.3102/0013189X013006004
- Kulik, C.-L. C., Kulik, J. A., & Bangert-Drowns, R. L. (1990). Effectiveness of mastery learning programs: A meta-analysis. *Review of Educational Research, 60*(2), 265–299. https://doi.org/10.3102/00346543060002265
- Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction, 4*(4), 253–278. https://doi.org/10.1007/BF01099821
- Beck, J. E., & Gong, Y. (2013). Wheel-spinning: Students who fail to master a skill. *AIED 2013, LNCS 7926*, 431–440. https://doi.org/10.1007/978-3-642-39112-5_44

**Feedback, hints, help seeking**
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487
- Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research, 78*(1), 153–189. https://doi.org/10.3102/0034654307313795
- VanLehn, K. (2006). The behavior of tutoring systems. *International Journal of Artificial Intelligence in Education, 16*(3), 227–265. https://www.cs.uky.edu/~sgware/reading/papers/vanlehn2006behavior.pdf
- Aleven, V., Stahl, E., Schworm, S., Fischer, F., & Wallace, R. (2003). Help seeking and help design in interactive learning environments. *Review of Educational Research, 73*(3), 277–320. https://doi.org/10.3102/00346543073003277
- Koedinger, K. R., & Aleven, V. (2007). Exploring the assistance dilemma in experiments with Cognitive Tutors. *Educational Psychology Review, 19*(3), 239–264. https://doi.org/10.1007/s10648-007-9049-0
- Baker, R. S., Corbett, A. T., Koedinger, K. R., & Wagner, A. Z. (2004). Off-task behavior in the Cognitive Tutor classroom: When students "game the system." *CHI '04*, 383–390. https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p383.pdf
- Shih, B., Koedinger, K. R., & Scheines, R. (2008). A response time model for bottom-out hints as worked examples. *EDM 2008*. https://www.cmu.edu/dietrich/philosophy/docs/scheines/Shih_Koedinger_Scheines_2008_EDM.pdf
- Mathan, S. A., & Koedinger, K. R. (2005). Fostering the intelligent novice: Learning from errors with metacognitive tutoring. *Educational Psychologist, 40*(4), 257–265. https://doi.org/10.1207/s15326985ep4004_7

**Errors, mindset, affect, motivation**
- Keith, N., & Frese, M. (2008). Effectiveness of error management training: A meta-analysis. *Journal of Applied Psychology, 93*(1), 59–69. https://doi.org/10.1037/0021-9010.93.1.59
- Yeager, D. S., et al. (2019). A national experiment reveals where a growth mindset improves achievement. *Nature, 573*, 364–369. https://doi.org/10.1038/s41586-019-1466-y
- Sisk, V. F., Burgoyne, A. P., Sun, J., Butler, J. L., & Macnamara, B. N. (2018). To what extent and under which circumstances are growth mind-sets important to academic achievement? Two meta-analyses. *Psychological Science, 29*(4), 549–571. https://doi.org/10.1177/0956797617739704
- Yeager, D. S., Purdie-Vaughns, V., Garcia, J., Apfel, N., Brzustoski, P., Master, A., Hessert, W. T., Williams, M. E., & Cohen, G. L. (2014). Breaking the cycle of mistrust: Wise interventions to provide critical feedback across the racial divide. *Journal of Experimental Psychology: General, 143*(2), 804–824. https://doi.org/10.1037/a0033906
- D'Mello, S., & Graesser, A. (2012). Dynamics of affective states during complex learning. *Learning and Instruction, 22*(2), 145–157. Record: https://experts.colorado.edu/display/pubid_164504
- Baker, R. S. J. d., D'Mello, S. K., Rodrigo, M. M. T., & Graesser, A. C. (2010). Better to be frustrated than bored: The incidence, persistence, and impact of learners' cognitive–affective states during interactions with three different computer-based learning environments. *International Journal of Human-Computer Studies, 68*(4), 223–241. https://doi.org/10.1016/j.ijhcs.2009.12.003
- Shernoff, D. J., Csikszentmihalyi, M., Schneider, B., & Shernoff, E. S. (2003). Student engagement in high school classrooms from the perspective of flow theory. *School Psychology Quarterly, 18*(2), 158–176. Record: https://typeset.io/papers/student-engagement-in-high-school-classrooms-from-the-19d7kslsau

**Story, context, multimedia**
- Harp, S. F., & Mayer, R. E. (1998). How seductive details do their damage: A theory of cognitive interest in science learning. *Journal of Educational Psychology, 90*(3), 414–434. https://doi.org/10.1037/0022-0663.90.3.414
- Rey, G. D. (2012). A review of research and a meta-analysis of the seductive detail effect. *Educational Research Review, 7*(3), 216–237. (Summary: https://www.learningscientists.org/blog/2019/6/20-1)
- Adams, D. M., Mayer, R. E., MacNamara, A., Koenig, A., & Wainess, R. (2012). Narrative games for learning: Testing the discovery and narrative hypotheses. *Journal of Educational Psychology, 104*(1), 235–249. Record: https://www.scinapse.io/papers/2012039745
- Walkington, C. A. (2013). Using adaptive learning technologies to personalize instruction to student interests: The impact of relevant contexts on performance and learning outcomes. *Journal of Educational Psychology, 105*(4), 932–945. https://doi.org/10.1037/a0031882
- Mayer, R. E., Fennell, S., Farmer, L., & Campbell, J. (2004). A personalization effect in multimedia learning: Students learn better when words are in conversational style rather than formal style. *Journal of Educational Psychology, 96*(2), 389–395. https://doi.org/10.1037/0022-0663.96.2.389
- CAST (2024). *Universal Design for Learning Guidelines version 3.0.* https://udlguidelines.cast.org

*Citation notes: most bibliographic details were checked through web search during this research pass. A few DOIs (Harp & Mayer 1998; Mayer et al. 2004; Renkl & Atkinson 2003; Kalyuga et al. 2003; Hattie & Timperley 2007; Pearson & Gallagher 1983; Corbett & Anderson 1995) follow the publishers' standard patterns but were not resolved directly, because doi.org and Crossref were not reachable from this session. For three items with no verified DOI, a record URL is given instead (Rey 2012; Adams et al. 2012; D'Mello & Graesser 2012).*
