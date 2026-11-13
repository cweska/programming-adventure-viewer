"""Sample unit: a small, complete tour of every item kind and feature in the Intro to Python course.

It is the teacher's preview (unpublished, so it shows only with ?preview=1) and the e2e test fixture.
Verify it with:

    PROTOTYPE_DIR=scripts/course/sample python3 docs/intro-to-python/prototypes/harness.py

Export it (with every other unit) with `npm run course:export`. Field reference:
docs/intro-to-python/prototypes/FORMAT.md.

What it covers:
  lesson "first-words"
    1. read-the-chalk     starter_passes ("run and read"), worked example, preview token, predict (one click,
                          with its own code)
    2. ask-the-traveler   stdin + input(), a known wrong answer, names ("Names to use"), pick (Mar'tu's pick),
                          a goal-only checkpoint (dictated=False)
    3. barrier-report     3 checkpoints with hint ladders and pass lines, dictated=True, another_way, bonus,
                          assemble, campaign_link, tracer, takeaway, partials, wrong answers (one that crashes),
                          names, pair_talk
  quiz "chalk-quiz"        mc (with and without code), predict, fill, parsons, bug
  project "night-watch-sign"   hidden setup, intro, light support
  challenge "mar-tu-speaks"    engine helpers (print_prompt), core level
  challenge "mar-tu-speaks-advanced"   advanced variant_of the core challenge, stdin
  article "asking-the-traveler"   body with a list, code fence and glossary links, runnable examples, a try-it
                                  that is a SOLO item (solo=True)
  cheatsheet "chalk-notes"
  testout "quick-check"
"""

UNIT = dict(
    id="sample",
    order=99,
    title="Sample Unit (teacher preview)",
    subtitle="A Tour of the Cabin",
    published=False,
    martu_intro=(
        "Hi. It is me, Mar'tu. This is not a real lesson, yes? It is a tour of the cabin.\n"
        "Every kind of page in this course lives here: a lesson, a quiz, a project, two challenges, "
        "an article, a cheat sheet and a Quick Check.\n"
        "Try them all. Nothing here counts toward anything.\n"
        "Lucky asked what is in it for him. Existing, Lucky. Existing."
    ),
    goals=[
        "Show words on the screen with `print()`",
        "Store a value in a [[variable]]",
        "Ask the traveler a question with `input()`",
        "Glue [[string|strings]] together with `+`",
    ],
    campaign_links=["leylines-awaken"],
    notes="Keep this unit small. Every feature the player supports should appear here at least once.",
)

GLOSSARY = [
    dict(
        term="string",
        aliases=["strings", "text"],
        plain="Text inside quotes. Python treats it as words, not as code.",
        example='"Barrier is holding."',
    ),
    dict(
        term="variable",
        aliases=["variables"],
        plain="A name that holds a value, so you can use the value later.",
        example="mana = 20",
    ),
    dict(
        term="output",
        aliases=["prints", "printed"],
        plain="What your program shows on the screen when it runs.",
    ),
    dict(
        term="input",
        aliases=["input()"],
        plain="Something the person running the program types in. `input()` waits for it and hands it back as a string.",
        example='name = input("Who goes there? ")',
    ),
    dict(
        # Same entry as Unit 1's (u01c), so the merged glossary keeps one "glue" with no clashing aliases.
        term="glue",
        aliases=["glues", "gluing", "concatenate", "concatenation"],
        plain="Join texts end to end with `+`. Python adds no spaces, so put the spaces inside the quotes.",
        example='"Shield" + " up."',
    ),
    dict(
        term="comment",
        aliases=["comments"],
        plain="A line that starts with `#`. Python skips it. It is a note for people.",
        example="# Mar'tu was here",
    ),
    dict(
        term="checkpoint",
        aliases=["checkpoints"],
        plain="One small task in an exercise. It turns green when your code does it.",
    ),
]

# ---------------------------------------------------------------------------------------------
# Lesson
# ---------------------------------------------------------------------------------------------

READ_THE_CHALK = dict(
    id="read-the-chalk",
    title="Read the chalk",
    martu=(
        "Before we cast anything, we read, yes?\n"
        "`print()` shows words on the screen. The words go inside quotes. Python calls quoted words a [[string]].\n"
        "Numbers do not need quotes. A comma lets you print a string and a number on one line.\n"
        "This code already works. Press Run and read the [[output]]."
    ),
    example='print("Steady, now.")\nprint("Hours left:", 42 - 5)\n',
    example_output="Steady, now.\nHours left: 37",
    introduces=["call:print", "const:str", "const:int"],
    preview=["op:Sub"],
    starter=(
        "# Mar'tu's first spell: words in quotes.\n"
        'print("The barrier is holding.")\n'
        'print("Hours until the next burst:", 37)\n'
    ),
    checkpoints=[
        dict(
            text="1. Press Run and read what prints.",
            hints=[
                "Press the Run button. Pressing Ctrl and Enter together works too.",
                "You do not need to change anything. Just press Run and look at the console.",
            ],
            checks=[
                ("prints the barrier line", "assert 'The barrier is holding.' in _lines(), 'Press Run to see the barrier line.'"),
            ],
            pass_line="Oogrish: Steady, now. You read it well.",
        ),
    ],
    solution=(
        "# Mar'tu's first spell: words in quotes.\n"
        'print("The barrier is holding.")\n'
        'print("Hours until the next burst:", 37)\n'
    ),
    starter_passes=True,
    predict=dict(
        q="Before you press Run: what will this line print?",
        code='print("Hours until the next burst:", 37)\n',
        choices=[
            "Hours until the next burst: 37",
            "Hours until the next burst:37",
            '"Hours until the next burst:", 37',
        ],
        answer=0,
        explain="The quotes are not printed. The comma becomes one space between the words and the number.",
    ),
    takeaway="`print()` shows words and numbers on the screen.",
    notes="Run-and-read: the starter passes on purpose, so the first press of Run is a win. The predict is free and never blocks Run.",
)

ASK_THE_TRAVELER = dict(
    id="ask-the-traveler",
    title="Ask the traveler",
    martu=(
        "Someone knocks on the cabin door. I must ask who it is, yes?\n"
        "`input()` asks a question and waits for an answer. Put the answer in a [[variable]] with `=`.\n"
        "Then you can [[concatenate|glue]] it to other words with `+`.\n"
        "In this exercise the traveler always answers `Lucky`. Of course it is Lucky."
    ),
    example='traveler = input("Name? ")\nprint("Hello, " + traveler)\n',
    example_output="Name? Lucky\nHello, Lucky",
    introduces=["node:Assign", "call:input", "op:Add"],
    stdin=["Lucky"],
    starter='name = input("Who goes there? ")\n# Greet the traveler on the next line.\n',
    checkpoints=[
        dict(
            id="greet",
            text="Print a greeting that uses `name`.",
            dictated=False,
            hints=[
                "The traveler's answer is stored in `name`.",
                "Glue words and `name` together with `+` inside `print()`.",
                'Try `print("Welcome to the cabin, " + name)`.',
            ],
            checks=[
                ("still asks for a name", "assert _inputs_used() == 1, 'Keep the input() line so the cabin can ask who is there.'"),
                (
                    "greets the traveler",
                    "assert any('Lucky' in line and 'Who goes there?' not in line for line in _lines()), "
                    "'Print a greeting that includes the name.'",
                ),
                ("uses the variable", "assert 'Lucky' not in _source, 'Use the variable name instead of typing Lucky.'"),
            ],
            pass_line="Lucky: Took you long enough.",
        ),
    ],
    solution='name = input("Who goes there? ")\nprint("Welcome to the cabin, " + name)\n',
    names=["name"],
    pick='"Welcome to the cabin, "',
    wrong_answers=[
        dict(
            why="types the name instead of using the variable",
            code='name = input("Who goes there? ")\nprint("Welcome to the cabin, Lucky")\n',
            fails_at=1,
            message_contains="variable",
        ),
    ],
    takeaway="`input()` asks a question. `=` keeps the answer in a variable.",
)

BARRIER_REPORT = dict(
    id="barrier-report",
    title="The barrier report",
    martu=(
        "Every night, someone reports who holds the barrier and how much mana they have left.\n"
        "A [[variable]] keeps a value under a name. Text needs quotes. Numbers do not.\n"
        "You cannot glue a number straight onto a string. Turn it into text first with `str()`.\n"
        "Three small steps, yes? Then the report."
    ),
    example=(
        'guard = "Oogrish"\n'
        "arrows = 12\n"
        'print("Arrows left for " + guard + ": " + str(arrows))\n'
    ),
    example_output="Arrows left for Oogrish: 12",
    another_way=[
        dict(
            angle="analogy",
            label="Think of jars",
            text=(
                "A variable is a jar with a label. `caster` is the label. `\"Gearshift\"` is what is inside.\n"
                "`str()` is like writing the number on a scrap of paper, so it can join the other words."
            ),
        ),
        dict(
            angle="step by step",
            text=(
                "1. Type `caster = \"Gearshift\"` and press Run.\n"
                "2. Type `mana = 20` on the next line and press Run.\n"
                "3. Build the sentence: `caster`, then `\" has \"`, then `str(mana)`, then `\" mana.\"`, joined with `+`."
            ),
        ),
    ],
    introduces=["call:str"],
    starter=(
        "# Gearshift's barrier report\n"
        "# 1. Make caster\n"
        "# 2. Make mana\n"
        "# 3. Print the report\n"
    ),
    checkpoints=[
        dict(
            id="make-caster",
            text='1. Make a variable called `caster` that holds the text `"Gearshift"`.',
            dictated=True,
            hints=[
                "A variable is a name, an equals sign, then a value.",
                "Text needs quotes around it.",
                'Write `caster = "Gearshift"` on the first line.',
            ],
            checks=[("caster holds Gearshift", "assert caster == 'Gearshift', 'Store the text Gearshift in caster, with quotes.'")],
            pass_line="Gearshift: Visor dims. Name logged.",
        ),
        dict(
            id="make-mana",
            text="2. Make a variable called `mana` that holds the number `20`.",
            hints=[
                "Numbers do not need quotes.",
                "Write `mana = 20` on its own line.",
            ],
            checks=[("mana is the number 20", "assert mana == 20, 'Store the number 20 in mana, with no quotes.'")],
        ),
        dict(
            id="print-report",
            text="3. Print `Gearshift has 20 mana.` Build it from `caster` and `mana`.",
            hints=[
                "Glue strings together with `+`.",
                "`mana` is a number. Turn it into text with `str(mana)` before you glue it.",
                'Try `print(caster + " has " + str(mana) + " mana.")`.',
            ],
            checks=[
                ("prints the report", "assert 'Gearshift has 20 mana.' in _lines(), 'Print exactly: Gearshift has 20 mana.'"),
                (
                    "uses the variables",
                    "assert _source.count('Gearshift') == 1, 'Use caster in the print line instead of typing Gearshift again.'",
                ),
            ],
            pass_line="Gearshift: Barrier's holding.",
        ),
    ],
    solution='caster = "Gearshift"\nmana = 20\nprint(caster + " has " + str(mana) + " mana.")\n',
    partials=[
        'caster = "Gearshift"\n',
        'caster = "Gearshift"\nmana = 20\n',
    ],
    wrong_answers=[
        dict(
            why="puts the number in quotes",
            code='caster = "Gearshift"\nmana = "20"\nprint(caster + " has " + mana + " mana.")\n',
            fails_at=2,
            message_contains="no quotes",
        ),
        dict(
            why="types the sentence instead of using the variables",
            code='caster = "Gearshift"\nmana = 20\nprint("Gearshift has 20 mana.")\n',
            fails_at=3,
            message_contains="caster",
        ),
        dict(
            why="forgets str() and crashes",
            code='caster = "Gearshift"\nmana = 20\nprint(caster + " has " + mana + " mana.")\n',
            fails_at=0,
            message_contains="can only concatenate",
        ),
    ],
    tracer=True,
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky wants a report too. Add a line that prints `Lucky has 26 mana.` Use two new variables.",
        hints=["Copy your three lines and change the names and values.", "Try `lucky_mana = 26`."],
        checks=[
            ("prints Lucky's report", "assert 'Lucky has 26 mana.' in _lines(), 'Print exactly: Lucky has 26 mana.'"),
            ("keeps Gearshift's report", "assert 'Gearshift has 20 mana.' in _lines(), 'Keep the Gearshift line too.'"),
        ],
        solution=(
            'caster = "Gearshift"\n'
            "mana = 20\n"
            'print(caster + " has " + str(mana) + " mana.")\n'
            'lucky = "Lucky"\n'
            "lucky_mana = 26\n"
            'print(lucky + " has " + str(lucky_mana) + " mana.")\n'
        ),
    ),
    assemble=dict(
        lines=['caster = "Gearshift"', "mana = 20", 'print(caster + " has " + str(mana) + " mana.")'],
        distractors=['mana = "20"', 'print(caster + " has " + mana + " mana.")'],
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet='dialogue = get_dialogue_prompt_string()\nprint_prompt(dialogue)\n',
        why="In the campaign you keep Mar'tu's line in a [[variable]] and hand it to `print_prompt()`. Same idea as `caster`, yes?",
    ),
    takeaway="Keep values in variables. Use `str()` to glue a number to text.",
    names=["caster", "mana"],
    pair_talk="Tell your partner why `mana` needs `str()` but `caster` does not. Then each of you types your own report.",
    notes=(
        "The crash wrong answer (fails_at=0) proves the TypeError path reaches the explainer. The example uses "
        "other names (guard, arrows) and another sentence shape, so it cannot be copied as the answer."
    ),
)

# ---------------------------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------------------------

QUESTIONS = [
    dict(
        type="mc",
        id="store-mana",
        q="Which line stores the number `20` in `mana`?",
        choices=['mana = "20"', "mana = 20", "20 = mana", "mana == 20"],
        answer=1,
        why_wrong={
            0: "The quotes make it text, not a number.",
            2: "The name goes on the left of `=`.",
            3: "`==` compares two values. It does not store anything.",
        },
        explain="The name goes on the left, then `=`, then the value. Numbers have no quotes.",
    ),
    dict(
        type="mc",
        q="What kind of value does `caster` hold?",
        code='caster = "Gearshift"\n',
        choices=["A string", "A number", "Nothing yet"],
        answer=0,
        explain="Quotes make a string. `caster` holds the text `Gearshift`.",
    ),
    dict(
        type="predict",
        q="What does this print?",
        code='hours = 37\nprint("Next burst in " + str(hours) + " hours")\n',
        choices=["Next burst in 37 hours", "Next burst in hours hours", "Next burst in str(hours) hours"],
        answer="Next burst in 37 hours",
        explain="`str(hours)` turns `37` into text, and `+` glues the pieces together.",
    ),
    dict(
        type="fill",
        q="Fill the blank so this prints `Shield up.` with a space in the middle.",
        code='print("Shield" + ___ + "up.")\n',
        answer='" "',
        accept=["' '"],
        expected_output="Shield up.",
        explain="`+` does not add spaces for you. A space is a string too: `\" \"`.",
    ),
    dict(
        type="parsons",
        q="Put the lines in order so the warning reads from top to bottom.",
        lines=['print("The clock turns red.")', 'print("Everyone inside the barrier!")', 'print("Shield up.")'],
        distractors=["print(Shield up.)"],
        expected_output="The clock turns red.\nEveryone inside the barrier!\nShield up.",
        explain="Python runs lines from top to bottom, so the output comes out in the same order.",
    ),
    dict(
        type="bug",
        q="Bomb Shell's line crashes. Fix it.",
        code='print("Barrier is holding.)\n',
        fix='print("Barrier is holding.")\n',
        expected_output="Barrier is holding.",
        explain="A string needs a quote at the start and at the end. The closing quote was missing.",
        notes="SyntaxError case: the buggy code never runs.",
    ),
]

# ---------------------------------------------------------------------------------------------
# The unit
# ---------------------------------------------------------------------------------------------

ITEMS = [
    dict(
        kind="lesson",
        id="first-words",
        title="First Words by the Fire",
        minutes=15,
        summary="Print words, ask a question, and write a barrier report.",
        exercises=[READ_THE_CHALK, ASK_THE_TRAVELER, BARRIER_REPORT],
    ),
    dict(
        kind="quiz",
        id="chalk-quiz",
        title="Chalk Quiz",
        minutes=5,
        summary="Six quick questions, one of each kind.",
        questions=QUESTIONS,
    ),
    dict(
        kind="project",
        id="night-watch-sign",
        title="The Night Watch Sign",
        minutes=10,
        summary="Paint a sign for the cabin door.",
        intro=(
            "The night watch needs a sign on the cabin door, yes?\n"
            "It shows a border, a title, and how many hours are left before the next burst."
        ),
        martu=(
            "I already stored the hours in a [[variable]] called `hours_left`. Do not change it. Use it.\n"
            "Each task is one line of [[output]]. Press Run after each one."
        ),
        setup="hours_left = 37\n",
        starter="# hours_left is already set for you. Use it, do not change it.\n",
        checkpoints=[
            dict(
                text="1. Print a border of exactly ten `=` signs.",
                hints=["A border is just a string of `=` signs.", 'Try `print("==========")`.'],
                checks=[("prints the border", "assert '==========' in _lines(), 'Print a line of exactly ten = signs.'")],
            ),
            dict(
                text="2. Print `NIGHT WATCH` on the next line.",
                hints=["Capital letters, inside quotes.", 'Try `print("NIGHT WATCH")`.'],
                checks=[("prints the title", "assert 'NIGHT WATCH' in _lines(), 'Print NIGHT WATCH in capital letters.'")],
            ),
            dict(
                text="3. Print `Next burst in 37 hours` using `hours_left`.",
                hints=[
                    "`hours_left` is a number, so it needs `str()` before you glue it.",
                    'Try `print("Next burst in " + str(hours_left) + " hours")`.',
                ],
                checks=[
                    ("prints the hours", "assert 'Next burst in 37 hours' in _lines(), 'Print exactly: Next burst in 37 hours'"),
                    ("uses hours_left", "assert '37' not in _source, 'Use hours_left instead of typing 37.'"),
                ],
                pass_line="Oogrish: A fine sign. Steady hands.",
            ),
        ],
        solution='print("==========")\nprint("NIGHT WATCH")\nprint("Next burst in " + str(hours_left) + " hours")\n',
        partials=['print("==========")\n', 'print("==========")\nprint("NIGHT WATCH")\n'],
        wrong_answers=[
            dict(
                why="types 37 instead of using hours_left",
                code='print("==========")\nprint("NIGHT WATCH")\nprint("Next burst in 37 hours")\n',
                fails_at=3,
                message_contains="hours_left",
            ),
        ],
        takeaway="A project is a few small steps. Run after each one.",
    ),
    dict(
        kind="challenge",
        id="mar-tu-speaks",
        title="Mar'tu Speaks",
        level="core",
        minutes=5,
        summary="Put Mar'tu's warning on the game screen.",
        martu=(
            "In the campaign, `print_prompt()` puts my words on the game screen.\n"
            "Store my warning in a variable once. Then show it twice: on the game screen and in the console."
        ),
        engine=True,
        starter="# Show Mar'tu's warning on the game screen and in the console.\n",
        checkpoints=[
            dict(
                text="Store `The decay is accelerating.` in a variable called `line`.",
                hints=["Text needs quotes.", 'Try `line = "The decay is accelerating."`.'],
                checks=[("line holds the warning", "assert line == 'The decay is accelerating.', 'Store the exact warning in line.'")],
            ),
            dict(
                text="Show `line` on the game screen with `print_prompt()`.",
                hints=["Pass the variable inside the brackets.", "Try `print_prompt(line)`."],
                checks=[("shows the prompt", "assert 'The decay is accelerating.' in _prompts, 'Pass line to print_prompt().'")],
            ),
            dict(
                text="Print `line` in the console too.",
                hints=["`print()` works on variables.", "Try `print(line)`."],
                checks=[
                    ("prints the warning", "assert 'The decay is accelerating.' in _lines(), 'Print line with print() as well.'"),
                    ("types it once", "assert _source.count('The decay') == 1, 'Type the warning once and reuse line.'"),
                ],
            ),
        ],
        solution='line = "The decay is accelerating."\nprint_prompt(line)\nprint(line)\n',
    ),
    dict(
        kind="challenge",
        id="mar-tu-speaks-advanced",
        title="Mar'tu Asks",
        level="advanced",
        variant_of="mar-tu-speaks",
        minutes=8,
        summary="Build Mar'tu's question from the traveler's answer.",
        martu=(
            "Harder now, yes? Ask the traveler to name a place. Build my question from their answer.\n"
            "The traveler will answer `greenroom`."
        ),
        engine=True,
        stdin=["greenroom"],
        starter="# Ask for a place, build the question, then show it.\n",
        checkpoints=[
            dict(
                text="Show `What do you remember about the greenroom?` with `print_prompt()`, built from the answer.",
                hints=[
                    'Ask with `place = input("Name a place: ")`.',
                    'Glue it: `"What do you remember about the " + place + "?"`.',
                    "Store that in a variable, then pass it to `print_prompt()`.",
                ],
                checks=[
                    ("asks once", "assert _inputs_used() == 1, 'Ask for the place with input() one time.'"),
                    (
                        "shows the question",
                        "assert 'What do you remember about the greenroom?' in _prompts, "
                        "'Show the full question with print_prompt().'",
                    ),
                    ("builds it from the answer", "assert 'greenroom' not in _source, 'Use the answer from input() instead of typing greenroom.'"),
                ],
            ),
        ],
        solution=(
            'place = input("Name a place: ")\n'
            'question = "What do you remember about the " + place + "?"\n'
            "print_prompt(question)\n"
        ),
    ),
    dict(
        kind="article",
        id="asking-the-traveler",
        title="Asking the Traveler",
        optional=True,
        minutes=6,
        summary="How `input()` works on this site.",
        body=(
            "On this site, `input()` does not wait for you to type. Each exercise brings its own answers, yes?\n"
            "This line asks for a name:\n"
            "```python\n"
            'name = input("Your name? ")\n'
            "```\n"
            "If the answer is `Gearshift`, the console shows the question and the answer together on one line: "
            "`Your name? Gearshift`\n"
            "Three things to remember:\n"
            "1. `input()` always hands back a [[string]], even when the answer looks like a number.\n"
            "2. Keep the answer in a [[variable]], or it is gone.\n"
            "3. If your code asks more questions than the exercise has answers, Python stops with an `EOFError`.\n"
            "Run the examples below. Then try it yourself."
        ),
        examples=[
            dict(code='name = input("Your name? ")\nprint("Hello, " + name)\n', output="Your name? Gearshift\nHello, Gearshift", stdin=["Gearshift"]),
            dict(code='print("Ley Clock check.")\nprint("It is not a compass.")\n', output="Ley Clock check.\nIt is not a compass."),
        ],
        exercises=[
            dict(
                id="try-it",
                title="Try it: Bomb Shell's words",
                martu="Bomb Shell talks in short sentences. Change the words in quotes so he says `Shield up.`",
                solo=True,
                starter="print(\"Write Bomb Shell's words here\")\n",
                checkpoints=[
                    dict(
                        text="Make the code print `Shield up.`",
                        hints=["Change only the words inside the quotes.", 'Try `print("Shield up.")`.'],
                        checks=[("prints Shield up.", "assert 'Shield up.' in _lines(), 'Print exactly: Shield up.'")],
                        pass_line="Bomb Shell: Shield up.",
                    ),
                ],
                solution='print("Shield up.")\n',
            ),
        ],
        notes="Article example output includes the echoed input line, the same as the console shows it.",
    ),
    dict(
        kind="cheatsheet",
        id="chalk-notes",
        title="Mar'tu's Chalk Notes",
        entries=[
            dict(concept="Print words", code='print("Steady, now.")\n', output="Steady, now.", note="Words go inside quotes."),
            dict(concept="Store a value", code="mana = 20\nprint(mana)\n", output="20", note="Name on the left, value on the right."),
            dict(
                concept="Glue strings",
                code='caster = "Lucky"\nprint(caster + " has " + str(26) + " mana.")\n',
                output="Lucky has 26 mana.",
                note="Use `str()` to glue a number to text.",
            ),
            dict(concept="Ask a question", code='name = input("Who goes there? ")\n', note="The answer is always a string."),
        ],
    ),
    dict(
        kind="testout",
        id="quick-check",
        title="Quick Check",
        minutes=5,
        summary="Already know this? Pass both tasks to skip the unit.",
        exercises=[
            dict(
                id="name-the-leader",
                title="Name the leader",
                martu="No hints this time, yes? Show me what you know.",
                support="none",
                starter="",
                checkpoints=[
                    dict(
                        text="Store the text `Oogrish` in a variable called `leader`.",
                        hints=["Text needs quotes.", 'Write `leader = "Oogrish"`.'],
                        checks=[("leader holds Oogrish", "assert leader == 'Oogrish', 'Store the text Oogrish in leader.'")],
                    ),
                    dict(
                        text="Print `leader`.",
                        hints=["Put the variable inside `print()`.", "Write `print(leader)`."],
                        checks=[
                            ("prints Oogrish", "assert 'Oogrish' in _lines(), 'Print the leader.'"),
                            ("prints the variable", "assert _source.count('Oogrish') == 1, 'Print leader instead of typing Oogrish again.'"),
                        ],
                    ),
                ],
                solution='leader = "Oogrish"\nprint(leader)\n',
            ),
            dict(
                id="leader-report",
                title="The leader's report",
                martu="One more. A report, like Gearshift's.",
                support="none",
                setup='leader = "Oogrish"\n',
                starter="# leader is already set for you.\n",
                checkpoints=[
                    dict(
                        text="Print `Oogrish has 18 mana.` using `leader` and a variable called `max_mana`.",
                        hints=["Make `max_mana = 18` first.", 'Then `print(leader + " has " + str(max_mana) + " mana.")`.'],
                        checks=[
                            ("max_mana is 18", "assert max_mana == 18, 'Store the number 18 in max_mana.'"),
                            ("prints the report", "assert 'Oogrish has 18 mana.' in _lines(), 'Print exactly: Oogrish has 18 mana.'"),
                            ("uses the variables", "assert 'Oogrish' not in _source, 'Use leader instead of typing Oogrish.'"),
                        ],
                    ),
                ],
                solution='# leader is already set for you.\nmax_mana = 18\nprint(leader + " has " + str(max_mana) + " mana.")\n',
            ),
        ],
    ),
]
