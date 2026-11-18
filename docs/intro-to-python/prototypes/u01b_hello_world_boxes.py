"""Unit 1 "Hello World", part b: Lesson 1B "Boxes With Labels" and Extra practice 1X-AB "Words and boxes".

Spec: design/curriculum.md, "## Unit 1", items 4 and 5 (1b-remembers; 1B-01 to 1B-06, 1B-S; 1A-07, 1B-T).
Introduces node:Assign (1B-01), const:int (1B-03) and const:multiline_str (1A-07, pool).

The check code is built by the small helpers below, so every box check gives the same kind of message:
  DEF          `def` used to make a box (valid Python like `def hero(): "Zelda"`, so no crash catches it)
  NAME / LEFT  a near-miss name, or an example's name (or a misspelling of one), instead of the task's name
  BARE         a value on a line by itself (made and forgotten), which raises no error
  TEXT / NUM   text needs quotes, numbers don't
  PRINT        print(name) with no quotes and not a value typed by hand, and the box's value really appears
Messages use invented values only and never repeat a student's text back.
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates; NAME / FOREIGN / EXTRA are filled in per exercise)
# ---------------------------------------------------------------------------------------------

_BOX_TEMPLATE = '''import ast as _ast
_tree = _ast.parse(_source)
_defs = [_n.name for _n in _ast.walk(_tree) if type(_n).__name__ == "FunctionDef"]
assert not ("__NAME__" in _defs and callable(globals().get("__NAME__"))), "`def` is for something you'll learn in Unit 3. To make a box, write `__NAME__ = ` and then the value, with no `def`."
if "__NAME__" not in globals():
    _made = []
    for _n in _ast.walk(_tree):
        if type(_n).__name__ == "Assign":
            for _t in _n.targets:
                if type(_t).__name__ == "Name" and _t.id not in _made:
                    _made.append(_t.id)
    def _edits(_a, _b):
        _row = list(range(len(_b) + 1))
        for _i, _ca in enumerate(_a, 1):
            _new = [_i]
            for _j, _cb in enumerate(_b, 1):
                _new.append(min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))
            _row = _new
        return _row[-1]
    def _close(_m, _want, _short_ok=True):
        _a, _b = _m.lower(), _want.lower()
        return _a.rstrip("s") == _b.rstrip("s") or _a.replace("_", "") == _b.replace("_", "") or ((_short_ok or len(_b) >= 5) and _edits(_a, _b) <= 2)
    _foreign = __FOREIGN__
    _near = [_m for _m in _made if _m not in _foreign and _close(_m, "__NAME__")]
    _left = [(_m, _f) for _m in _made for _f in _foreign if _m == _f or (_m not in _foreign and _close(_m, _f, False))]
    _bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == "Expr" and type(_n.value).__name__ == "Constant" and type(_n.value.value).__name__ in ("str", "int", "float")]
    if _near:
        _msg = "Your box is named `" + _near[0] + "`, but this step needs `__NAME__`. Names match letter for letter, capitals too, so use `__NAME__` on every line.__EXTRA__"
    elif _left and _left[0][0] == _left[0][1]:
        _msg = "`" + _left[0][0] + "` is a name from the Example or an earlier step. This step's box is named `__NAME__`, so use `__NAME__` on every line."
    elif _left:
        _msg = "`" + _left[0][0] + "` looks like `" + _left[0][1] + "`, a name from the Example or an earlier step. This step's box is named `__NAME__`, so use `__NAME__` on every line."
    elif _bare:
        _msg = "Line " + str(_bare[0]) + " is a value with no name in front, so Python reads it and throws it away, like a phone number saved with no contact name. Put `__NAME__ = ` in front of it."
    else:
        _msg = "Make a box named `__NAME__`: start a line with `__NAME__ = `."
    assert False, _msg'''


def box_check(name, foreign=(), extra=""):
    """NAME + LEFT + BARE: the box exists, or the message says why not."""
    code = _BOX_TEMPLATE.replace("__NAME__", name).replace("__FOREIGN__", repr(list(foreign)))
    return (f"there is a box named {name}", code.replace("__EXTRA__", (" " + extra) if extra else ""))


def text_check(name, want="text in quotes"):
    """TEXT: the box holds non-empty text."""
    return (
        f"{name} holds text",
        f"_v = {name}\n"
        f"assert type(_v).__name__ == 'str', {'`' + name + '` holds `'!r} + repr(_v) + {'`. This step needs ' + want + '.'!r}\n"
        f"assert _v.strip(), '`{name}` holds empty quotes. Put some words between them.'",
    )


def num_check(name):
    """NUM: the box holds a whole number, not text that looks like one."""
    return (
        f"{name} holds a number",
        f"_v = {name}\n"
        f"assert type(_v).__name__ != 'str', \"`{name}` holds text, because of the quotes. Numbers don't get quotes: take them off.\"\n"
        f"assert type(_v).__name__ == 'int', '`{name}` should hold a whole number, like `3`.'",
    )


def bare_check(kinds=("str", "int", "float")):
    """BARE: no line is just a value (it raises no error, so only a check can catch it)."""
    return (
        "no value is left without a box",
        "import ast as _ast\n"
        "_bare = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        f"and type(_n.value).__name__ == 'Constant' and type(_n.value.value).__name__ in {tuple(kinds)!r}]\n"
        "assert not _bare, 'Line ' + str(_bare[0]) + ' is a value with no name in front, so Python reads it and throws it "
        "away. Your box is already made, so delete line ' + str(_bare[0]) + '.'",
    )


def print_check(name, missing=None, show=True, typed="the value typed in"):
    """PRINT: print(name) with no quotes (not the word, not a value typed by hand), and the value shows.

    ``missing`` replaces the "add a print" message (for starters that already had the print line).
    ``show=False`` leaves out the "the value shows in the console" part, for exercises with their own message.
    ``typed`` only words the typed-in message ("the hero typed in quotes", "the number typed in").
    """
    missing = missing or f"Add a line that prints the box: `print({name})`."
    code = (
        "import ast as _ast\n"
        "_args = [_a for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
        "and type(_n.func).__name__ == 'Name' and _n.func.id == 'print' for _a in _n.args]\n"
        f"_named = [_a for _a in _args if type(_a).__name__ == 'Name' and _a.id == '{name}']\n"
        f"_quoted = [_a for _a in _args if type(_a).__name__ == 'Constant' and _a.value == '{name}']\n"
        f"_typed = [_a for _a in _args if type(_a).__name__ == 'Constant' and _a.value != '{name}' "
        f"and str(_a.value).strip() == str(globals().get('{name}')).strip()]\n"
        f"assert _named or not _typed, 'Your `print` has {typed}, not the box. Print the box instead: "
        f"`print({name})`. Then Python looks inside the box and shows what is there.'\n"
        f"assert _named or not _quoted, 'Your `print` shows the word {name}, because of the quotes. Take the quotes off: "
        f"`print({name})`. {QUOTES_RULE}'\n"
        f"assert _named, {missing!r}"
    )
    if show:
        code += (
            f"\nassert any(str({name}).strip() in _l for _l in _lines()), "
            f"'Your `print({name})` runs before `{name}` gets its last value. Python reads top to bottom, "
            f"so move `print({name})` below the line that puts the value in.'"
        )
    return (f"prints the box {name}", code)


def value_check(name, value):
    """The box holds this exact number (and says so kindly when it holds text that looks like one)."""
    return (
        f"{name} is {value}",
        f"_v = {name}\n"
        f"assert type(_v).__name__ != 'str', \"`{name}` holds text, because of the quotes. Numbers don't get quotes: take them off.\"\n"
        f"assert _v == {value!r}, '`{name}` holds ' + str(_v) + '. Keep {value} in `{name}`.'",
    )


def meta(**fields):
    """The §2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of hello-world)
# ---------------------------------------------------------------------------------------------

UNIT = dict(
    id="hello-world",
    order=1,
    title="Hello World",
    subtitle="Words by the Fire",
    published=True,
    martu_intro=(
        "Hi. It is me, Mar'tu. Before we continue on our adventure, we go back to the first words, yes?\n"
        "A lot of that campaign code felt like a wall, yes? We will take the wall apart, one stone at a time.\n"
        "Every spell begins as words. Python is fussy about words. More fussy than Lucky is about glug, yes?\n"
        "Tonight: how to say something, how to keep something in a box, and how to let Python do the math."
    ),
    goals=[
        "Make Python show words on the screen",
        "Write notes that Python skips",
        "Keep words or a number in a named box (a variable)",
        "Change what is in a box",
        "Let Python do the math with your boxes",
        "Join words and numbers into one line, and draw a mana bar from blocks",
        "Read Python's error messages and fix small mistakes",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="variable",
        aliases=["variables", "box", "boxes"],
        plain="A box with a name on it and a value inside. It's like x in math, but you pick the name, and "
        "`name = value` makes one.",
        example='companion = "Gearshift"',
    ),
    dict(
        term="value",
        aliases=["values"],
        plain="What goes in a box: text in quotes, like `\"Lucky\"`, or a number, like `26`.",
        example="mana = 26",
    ),
    dict(
        term="number",
        aliases=["numbers"],
        plain="An amount Python can do math with, like points in a game. Numbers get no quotes: `3` is a "
        "number, and `\"3\"` is text.",
        example="armor_bonus = 3",
    ),
    dict(
        term="defined",
        aliases=["not defined", "define"],
        plain=(
            "Python has a definition for the name: a line like `name = value` already ran. "
            "\"Not defined\" means Python looked for the name and found nothing, like a word missing from a glossary."
        ),
        example="NameError: name 'hero' is not defined",
    ),
    dict(
        term="triple quotes",
        aliases=["triple-quoted", "multi-line string"],
        plain="Three quote marks in a row, `\"\"\"`. They start text that can go over many lines, and three more "
        "end it, the way a poem keeps its line breaks.",
        example='print("""Line one\nLine two""")',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (1b-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_1B = dict(
    kind="quiz",
    id="1b-remembers",
    title="Quick review: 2 questions (not scored)",
    optional=True,
    minutes=1,
    summary="Two quick questions from the last lesson, Words in Quotes. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 1B; recall from 1A. "
        "A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="glug-in-quotes",
            q="Which line shows the word glug on the screen?",
            choices=["print(glug)", 'print("glug")', 'print("glug)'],
            answer=1,
            why_wrong={
                0: "With no quotes, Python thinks glug is a name it should already know. It finds none, so it stops "
                "and says *not defined*.",
                2: "The quote opens but never closes, so Python can't tell where the text ends. It stops with an error.",
            },
            explain="Text you want to show needs quotes, like someone's exact words in English class. "
            "`print(\"glug\")` shows glug.",
        ),
        dict(
            type="mc",
            id="hash-line",
            q="What does Python do with a line that starts with `#`?",
            choices=[
                "It skips it. The line is a note for people.",
                "It shows it on the screen.",
                "It stops the program.",
            ],
            answer=0,
            why_wrong={
                1: "Only `print` shows things on the screen. Python skips a `#` line.",
                2: "Nothing stops. Python skips that line and goes on to the next one.",
            },
            explain="A line that starts with `#` is a note for people, like the stage directions in a play script. "
            "Python skips it.",
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 1B "Boxes With Labels"
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."

KEYBOARD_SYMBOLS = dict(
    id="keyboard-symbols",
    title="Where the symbols live",
    martu=(
        "Three keys you'll need in this lesson. `-` is minus. `_` is the underscore (Shift and `-`): a name can't "
        "have a space, so `_` stands in for one, as in `max_mana`. `=` is the equals key, but in Python it won't "
        "mean equals: the next exercise shows its job. Top right of your keyboard:\n"
        "```text\n"
        "with Shift:   (   )   _   +\n"
        "no Shift:     9   0   -   =\n"
        "```"
    ),
    example='print("( ) #")\n',
    example_output="( ) #",
    starter="# Your line goes here:\n\n",
    names=["print"],
    pick="_ - = are side by side.",
    checkpoints=[
        dict(
            id="print-the-symbols",
            text=(
                "On line 2, under the note, show `_`, `-` and `=` on the screen, all on one line. Copy the Example's "
                "shape, and put the three marks inside its quotes."
            ),
            dictated=False,
            hints=[
                "Click on the empty line 2, under `# Your line goes here:`. Line 1 starts with `#`, so Python "
                'skips it. Start line 2 with `print("` and add the three marks after it.',
                "Quotes mean *show these exact marks*. Python shows whatever is between them, as it is: "
                '`print("( )")` shows `( )`.',
                'Type `print("_ - = are side by side.")` on line 2. Anything inside the quotes shows as it is.',
            ],
            checks=[
                ("prints something", "assert _lines(), 'Nothing shows in the Console yet. Line 1 is a note, so "
                 "Python skips it. On line 2, write a `print` line with the three marks inside quotes.'"),
                (
                    "one line has all three symbols",
                    "_best = max(_lines(), key=lambda line: sum(s in line for s in '_-='))\n"
                    "_missing = [s for s in '_-=' if s not in _best]\n"
                    "assert not _missing, 'Your line is missing ' + ' and '.join('`' + s + '`' for s in _missing) "
                    "+ '. Put all three marks inside one pair of quotes, on one `print` line.'",
                ),
            ],
            pass_line="Mar'tu: Now you know where they live.",
        ),
    ],
    solution='# Your line goes here:\nprint("_ - = are side by side.")\n',
    assemble=dict(
        lines=['print("Keys:")', 'print("_ - =")'],
        distractors=["print(_ - =)", 'print("_ - =)'],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "The three keys, circled:\n"
                "```text\n"
                "  9   0  (-)  (=)   Backspace\n"
                "         Shift + (-) gives (_)\n"
                "```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `-` is the key right after `0`.\n"
                "2. `_` is the same key with Shift held down.\n"
                "3. `=` is the next key to the right.\n"
                '4. `"` is Shift with the `\'` key, next to Enter.\n'
                "5. `#` is Shift with the `3` key."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text='Type `print("`, then the three symbols, then `")`.',
        ),
    ],
    wrong_answers=[
        dict(why="starter unchanged: only the note, nothing printed", code="# Your line goes here:\n\n",
             fails_at=1, message_contains="Nothing shows"),
        dict(why="symbols with no quotes", code="print(_ - =)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="leaves one symbol out", code='print("_ -")\n', fails_at=1, message_contains="missing `=`"),
        dict(why="the marks typed into the note, not shown", code="# Your line goes here: _ - =\n\n", fails_at=1,
             message_contains="Nothing shows"),
        dict(why="check-breaker: each symbol on its own line, not one line with all three",
             code='print("_")\nprint("-")\nprint("=")\n', fails_at=1, message_contains="missing"),
    ],
    takeaway="`-` is minus. `_` (Shift and `-`) stands in for a space in a name. `=` is not math's equals: "
             "you'll read it as *gets*.",
    notes=(
        "meta: starter_level=S2; path=CC; contingent=show-me-more (K); skills=print-text; solo=false; "
        "dictates=; foreign_names=. G1 R30 (dash for =: A-04 `chicken_sandwich - \"Fireball`). Any line with "
        "all three symbols passes; Mar'tu's pick is the solution's line. Check-breaker: WA for one symbol per line. "
        "Structure pass (guide 9, S12): moved from the 1W warm-ups (before print and # were taught) to the start "
        "of Boxes With Labels, right before `=` and `_` are used; print and # are known by now, so Mar'tu no "
        "longer explains them. The starter note was `# Print a line that has _ and - and = in it.`: it held the "
        "marks themselves (a literal reader could think line 1 was already done) and used print before 1B's "
        "plain word show. It is now a place note in the shape of name-and-value's, `# Your line goes here:`, "
        "with an empty line 2 to type on."
    ),
)


LABEL_A_BOX = dict(
    id="label-a-box",
    title="A box with a name",
    martu=(
        "In math, a letter like x stands for a number. A box (a [[variable]]) is like that, but you pick its name, "
        "and it can hold words. In `companion = \"Gearshift\"`, the box's name is `companion`, like a label on the "
        "box. In math, `=` means both sides are equal. In Python, read `=` as *gets*: companion gets Gearshift.\n"
        "```\n  companion\n+-----------+\n| Gearshift |\n+-----------+\n```"
    ),
    introduces=["node:Assign"],
    names=["companion"],
    pick="Bomb Shell",
    pair_talk=(
        "Pair talk: before you press Run, tell your partner what each `print` line will show. "
        "Then each of you runs it on your own screen. Who was right about line 3?"
    ),
    predict=dict(
        q="Before you press Run: what will these three lines show in the Console?",
        choices=["Gearshift\ncompanion", "companion\nGearshift", "Gearshift\nGearshift", "companion\ncompanion"],
        answer=0,
        explain=(
            "Line 2 has no quotes, so Python looks inside the box and shows what is there: Gearshift. "
            "Line 3 has quotes, so it shows those exact letters: companion. " + QUOTES_RULE
        ),
    ),
    starter='companion = "Gearshift"\nprint(companion)\nprint("companion")\n',
    checkpoints=[
        dict(
            id="another-hero",
            text="On line 1, change `Gearshift` to a different hero. Keep `companion = ` and both quotes as they are.",
            dictated=True,
            hints=[
                "Look at line 1. Delete `Gearshift`, then type a new hero between the two quotes.",
                "The box's name, `companion`, is left of `=`. The hero goes on the right, in quotes.",
                "Delete `Gearshift` and type a new hero, so line 1 reads `companion = \"Bomb Shell\"`, or any hero "
                "inside the quotes.",
            ],
            checks=[
                box_check("companion", foreign=["snack"]),
                text_check("companion", "a hero's name in quotes"),
                (
                    "companion is not the example's hero",
                    "assert companion.strip().lower() != 'gearshift', "
                    "\"`companion` still holds Gearshift, the hero that was already there. Change `Gearshift` to another "
                    "hero. Can't decide? Use the Mar'tu's pick button, next to Names to use.\"",
                ),
                print_check("companion", missing="Keep `print(companion)` on line 2, so you can see the new hero in the box.",
                            typed="the hero typed in quotes"),
            ],
            pass_line="Mar'tu: Hm. A new face in the box.",
        ),
    ],
    solution='companion = "Bomb Shell"\nprint(companion)\nprint("companion")\n',
    assemble=dict(
        lines=['companion = "Bomb Shell"', "print(companion)", 'print("companion")'],
        distractors=['"Bomb Shell"', '"companion" = "Bomb Shell"'],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Two lines, two answers:\n"
                "```\nprint(companion)\n-> looks inside the box\n-> shows Gearshift\n\n"
                "print(\"companion\")\n-> these exact letters\n-> shows companion\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a phone contact",
            text=(
                "A phone contact has a name with a number saved under it. Tap the name, and the phone uses what "
                "is saved. `print(companion)` taps the name. `print(\"companion\")` only reads the word out loud."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "A jar on my shelf with a name chalked on it: `companion`. Inside is Gearshift. "
                "Ask for the jar by its name, and you get what is inside."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Python reads one line at a time:\n"
                "1. `companion = \"Gearshift\"`: the box `companion` gets Gearshift.\n"
                "2. `print(companion)`: looks inside the box and shows Gearshift.\n"
                "3. `print(\"companion\")`: shows the letters companion."
            ),
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `\"companion\" = \"Gearshift\"` (a box's name never goes in quotes). "
                "Not this: `companion - \"Gearshift\"` (`-` means minus). "
                "Not this: `\"Gearshift\"` on its own (no name in front, so Python reads it and throws it away).\n"
                "This: `companion = \"Gearshift\"`."
            ),
        ),
        dict(
            angle="sentence frame",
            label="Fill the frame",
            text=(
                "Fill the frame: `____ = ____`. The left blank is the box's name, with no quotes. "
                "The right blank is the value: text in quotes. Like `companion = \"Bomb Shell\"`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky wants a turn",
        text=(
            "Lucky wants to be the companion. At the bottom of your code, add a line that puts a new hero in "
            "`companion`. Then add `print(companion)` under it, so the box shows once before the change and once after."
        ),
        hints=[
            "Click at the end of the last line and press Enter. Type `companion = ` and a new hero in quotes.",
            "Then add `print(companion)` under it. The first `print(companion)` already shows the old hero.",
        ],
        checks=[
            (
                "companion gets two different heroes, both printed",
                "import ast as _ast\n"
                "_vals = [_n.value.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                "and any(type(_t).__name__ == 'Name' and _t.id == 'companion' for _t in _n.targets) "
                "and type(_n.value).__name__ == 'Constant']\n"
                "assert len(_vals) >= 2 and _vals[-1] != _vals[-2], 'At the bottom, add a line that puts a different hero in `companion`.'\n"
                "assert str(_vals[-2]).strip() in _lines() and str(_vals[-1]).strip() in _lines(), "
                "'Show `companion` twice: keep `print(companion)` on line 2, and add another `print(companion)` under your new line.'",
            ),
        ],
        solution='companion = "Bomb Shell"\nprint(companion)\nprint("companion")\ncompanion = "Lucky"\nprint(companion)\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet="dialogue_input = \"Write what Mar'tu asks here\"",
        why=(
            "You've seen this. Mar'tu's dialogue line lived in a box named `dialogue_input`, "
            "with your words inside, in quotes. Now you know why it was written that way."
        ),
    ),
    takeaway="`name = value` makes a box: name gets value. `print(name)` shows what is inside, and `print(\"name\")` shows the word.",
    wrong_answers=[
        dict(why="value left as the example's Gearshift", code='companion = "Gearshift"\nprint(companion)\nprint("companion")\n',
             fails_at=1, message_contains="still holds Gearshift"),
        dict(why="`companion = ` deleted: a bare value with no box", code='"Gearshift"\nprint(companion)\nprint("companion")\n',
             fails_at=0, message_contains="companion"),
        dict(why="hero name with no quotes", code="companion = Bomb Shell\nprint(companion)\n",
             fails_at=0, message_contains="invalid syntax"),
        dict(why="capital letter in the name", code='Companion = "Bomb Shell"\nprint(Companion)\n',
             fails_at=1, message_contains="letter for letter"),
        dict(why="prints the new hero typed by hand instead of the box", code='companion = "Bomb Shell"\nprint("Bomb Shell")\nprint("companion")\n',
             fails_at=1, message_contains="Print the box instead"),
        dict(why="quotes put on line 2 too, so the box is never opened", code='companion = "Bomb Shell"\nprint("companion")\nprint("companion")\n',
             fails_at=1, message_contains="Take the quotes off"),
        dict(why="print lines deleted", code='companion = "Bomb Shell"\n', fails_at=1, message_contains="Keep `print(companion)`"),
        dict(why="def used to make the box (valid Python, but a recipe, not a box)", code='def companion(): "Bomb Shell"\nprint(companion)\nprint("companion")\n',
             fails_at=1, message_contains="learn in Unit 3"),
        dict(why="unclosed quote", code='companion = "Bomb Shell\nprint(companion)\nprint("companion")\n',
             fails_at=0, message_contains="unterminated string"),
        dict(why="new hero added after the prints, so it never shows", code='companion = "Gearshift"\nprint(companion)\nprint("companion")\ncompanion = "Bomb Shell"\n',
             fails_at=1, message_contains="runs before"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="make-variable", solo="false", dictates="1",
             foreign_names="snack", twin='rival = "<any>" then print(rival)') + "\n"
        "Investigate (G3 R2) moved out of the Learn text (teacher ruling): the 'delete `companion = `' dare is now "
        "the name-and-value predict (a value with no name, then `print(character)` -> not defined), so Learn ends "
        "on the box picture. CP hints[0] says to delete Gearshift and type between the quotes, so following it "
        "cannot break a quote. "
        "C3: the example's value fails with an inline offer of Mar'tu's pick. TR = the step-by-step angle."
    ),
)

NAME_AND_VALUE = dict(
    id="name-and-value",
    title="Name AND value",
    martu=(
        "A box needs a name AND a [[value]]: what goes inside, like text in quotes. Write the name, then `=`, "
        "then the value: `companion = \"Gearshift\"`. It's like a phone contact: a phone number saved with no "
        "name is lost. The name gets no quotes. The value, your hero, does.\n"
        "Any hero works. Silly is allowed. I have seen worse, yes?"
    ),
    example='companion = "Gearshift"\nprint(companion)\n',
    example_output="Gearshift",
    names=["character"],
    pick="a very tired adventurer",
    pair_talk=(
        "Pair talk: each of you makes your own box on your own screen. Then read your partner's line 1 out "
        "loud, saying \"gets\" for `=`."
    ),
    predict=dict(
        q="What will these two lines show in the Console?",
        code='"Bomb Shell"\nprint(character)\n',
        choices=["Bomb Shell", "ERROR: name 'character' is not defined", "character"],
        answer=1,
        explain=(
            "Line 1 is a value with no name in front, so Python reads it and throws it away. No box named "
            "`character` was ever made, so line 2 stops with *not defined*. A box needs a name AND a value: "
            "`character = \"Bomb Shell\"`."
        ),
    ),
    starter="# Your box goes here:\n\n# Print it here:\n",
    checkpoints=[
        dict(
            id="make-character",
            text="Make a box named `character`. Put your hero inside it, in quotes.",
            dictated=False,
            hints=[
                "Click on the empty line under `# Your box goes here:`. Start the line with `character = `.",
                "The box's name is `character`, from this step. It goes left of `=`, with no quotes.",
                "Write `character = \"a very tired adventurer\"` under `# Your box goes here:`, or put any hero "
                "inside the quotes.",
            ],
            checks=[
                box_check("character", foreign=["companion", "player_name", "hero", "snack"]),
                text_check("character"),
                bare_check(),
            ],
            pass_line="Mar'tu: Hm. Welcome to the cabin.",
        ),
        dict(
            id="print-character",
            text="Type `print(character)` on the empty line under `# Print it here:`. No quotes around `character`: Python looks inside the box.",
            dictated=True,
            hints=[
                "Click on the empty line under `# Print it here:`. Start the line with `print(`.",
                "The Example prints its box by name, with no quotes. Do the same with your box: `character`.",
                "Write `print(character)` under `# Print it here:`, with no quotes around `character`. " + QUOTES_RULE,
            ],
            checks=[print_check("character", typed="your hero typed in quotes")],
        ),
    ],
    solution='# Your box goes here:\ncharacter = "a very tired adventurer"\n# Print it here:\nprint(character)\n',
    partials=['# Your box goes here:\ncharacter = "a very tired adventurer"\n# Print it here:\n'],
    assemble=dict(
        lines=['character = "a very tired adventurer"', "print(character)"],
        distractors=['"a very tired adventurer"', 'character - "a very tired adventurer"', 'print("character")'],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Three parts, always in this order:\n"
                "```\ncharacter    =     \"Zelda\"\n  name      gets    value\n(no quotes)        (quotes)\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a phone contact",
            text=(
                "Saving a contact needs a name AND a number. A number with no name is lost in the list. "
                "A box needs a name AND a value, the same way."
            ),
        ),
        dict(
            angle="sentence frame",
            label="Fill the frame",
            text="Say it as you type it: the name with no quotes, then *gets*, then the value in quotes: `character = \"Zelda\"`.",
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `def (\"character\")` (`def` is for Unit 3). Not this: `\"character\" = \"Zelda\"`. "
                "Not this: `character - \"Zelda\"`. Not this: `\"Zelda\"` on its own, with no name.\n"
                "This: `character = \"Zelda\"`."
            ),
        ),
        dict(
            angle="shorter",
            text="Name, `=`, value in quotes. Then `print(character)`.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="A weapon for Lucky",
        text=(
            "Lucky wants a weapon too. Two moves:\n"
            "1. Make a box named `weapon` that holds any weapon, in quotes.\n"
            "2. Write your own `#` note on the line right above each box, saying what it holds."
        ),
        hints=[
            "A note is a line that starts with `#` (Shift+3), like `# my hero`.",
            "Put your note on the line right above `character = ...`, and another right above `weapon = ...`. "
            "The notes that were already there don't count.",
        ],
        checks=[
            ("weapon holds text", "assert type(weapon).__name__ == 'str' and weapon.strip(), 'Make `weapon` hold a weapon, in quotes.'"),
            (
                "a note of your own sits above each box",
                "import ast as _ast\n"
                "_src = _source.splitlines()\n"
                "_starter = ('# Your box goes here:', '# Print it here:')\n"
                "_rows = {_t.id: _n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' "
                "for _t in _n.targets if type(_t).__name__ == 'Name'}\n"
                "for _box in ('character', 'weapon'):\n"
                "    _above = _src[_rows[_box] - 2].strip() if _rows.get(_box, 1) > 1 else ''\n"
                "    assert _above.startswith('#') and _above not in _starter, "
                "'Write your own `#` note on the line right above `' + _box + ' = ...`.'",
            ),
        ],
        solution=(
            "# My hero:\ncharacter = \"a very tired adventurer\"\n"
            "# My hero's weapon:\nweapon = \"a brass rune-axe\"\n"
            "print(character)\n"
        ),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='option_1 = "Write option 1 here"\noption_2 = "Write option 2 here"',
        why=(
            "You've seen this. The four dialogue options were four boxes: a name, then `=`, then words in "
            "quotes. Name AND value, every time."
        ),
    ),
    takeaway="A box needs a name AND a value: `character = \"Zelda\"`. Then `print(character)`, no quotes.",
    wrong_answers=[
        dict(why="a lone value, then print the value", code='"Zelda"\nprint("Zelda")\n', fails_at=1, message_contains="no name in front"),
        dict(why="a lone value, then print(character)", code='"Zelda"\nprint(character)\n', fails_at=0, message_contains="character"),
        dict(why="def used to make a box", code='def ("character")\nprint(character)\n', fails_at=0, message_contains="invalid syntax"),
        dict(why="a dash instead of =", code='character - "Zelda"\nprint(character)\n', fails_at=0, message_contains="not defined"),
        dict(why="the worksheet's name player_name", code='player_name = "Zelda"\nprint(player_name)\n', fails_at=1, message_contains="character"),
        dict(why="the example's name companion", code='companion = "Zelda"\nprint(companion)\n', fails_at=1, message_contains="example"),
        dict(why="capital C", code='Character = "Zelda"\nprint(Character)\n', fails_at=1, message_contains="letter for letter"),
        dict(why="misspelled name", code='charcter = "Zelda"\nprint(charcter)\n', fails_at=1, message_contains="charcter"),
        dict(why="text with no quotes", code="character = Kratos\nprint(character)\n", fails_at=0, message_contains="Kratos"),
        dict(why="two words with no quotes", code="character = Captain Glug\nprint(character)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="the name in quotes on the left", code='"character" = "Zelda"\n', fails_at=0, message_contains="literal"),
        dict(why="a number, not text", code="character = 7\nprint(character)\n", fails_at=1, message_contains="text in quotes"),
        dict(why="print with quotes around the name", code='character = "Zelda"\nprint("character")\n', fails_at=2, message_contains="word"),
        dict(why="box made but a lone value left too", code='"Zelda"\ncharacter = "Zelda"\nprint(character)\n', fails_at=1, message_contains="delete line 1"),
        dict(why="prints the hero typed by hand instead of the box", code='character = "Zelda"\nprint("Zelda")\n', fails_at=2, message_contains="Print the box instead"),
        dict(why="def used to make the box (valid Python: a recipe, not a box)", code='def character(): "Zelda"\nprint(character)\n',
             fails_at=1, message_contains="learn in Unit 3"),
        dict(why="def with the box inside it", code='def character():\n    character = "Zelda"\nprint(character)\n',
             fails_at=1, message_contains="learn in Unit 3"),
        dict(why="the example's name, misspelled (plager_name)", code='plager_name = "Zelda"\nprint(plager_name)\n',
             fails_at=1, message_contains="looks like `player_name`"),
        dict(why="unclosed quote", code='character = "Zelda\nprint(character)\n', fails_at=0, message_contains="unterminated string"),
        dict(why="mismatched quotes", code='character = "Zelda\'\nprint(character)\n', fails_at=0, message_contains="unterminated string"),
        dict(why="capitals all through the name", code='CHARACTER = "Zelda"\nprint(CHARACTER)\n', fails_at=1, message_contains="letter for letter"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="make-variable,exact-names,quote-text", solo="false", dictates="2",
             foreign_names="companion,player_name,hero,snack", echo="character", twin='familiar = "<any>" then print(familiar)') + "\n"
        "Echo spot: on a CP1 pass Mar'tu says '*<value>.* Hm. Welcome to the cabin.' through the blocklist (§2.11); "
        "pass_line is the fallback. "
        "Predict (teacher ruling) carries the old 1B-01 investigate dare: a lone \"Bomb Shell\" then "
        "`print(character)` is a NameError. The right choice reads 'ERROR: ...' because the harness matches an "
        "error answer only by that prefix (same form as u01a's Fireball predict); the teacher's wording was "
        "'An error: name 'character' is not defined'. "
        "WA `\"character\" = \"Zelda\"` checks Python's raw text ('literal'): the harness never runs explain.ts. "
        "Once the explain.ts change lands, the site's row for it reads 'The name of a box never goes in quotes'; "
        "switch message_contains to 'never goes in quotes' when the harness checks crashes through explain.ts. "
        "WA evidence: lone value (B-02, B-03, A-04); def (A-02); dash (A-04); player_name (A-05, A-07, A-08); "
        "unquoted text (A-08 Kratos shape, B-01); multi-word (G2 R2); misspelling (A-03, A-08)."
    ),
)

NUMBERS_STAND_ALONE = dict(
    id="numbers-stand-alone",
    title="Numbers don't get quotes",
    martu=(
        "A [[number]] gets no quotes. `3` is an amount you can do math with, like points in a game. `\"3\"` in "
        "quotes is text, like the 3 on a jersey: nobody adds two jerseys. In the Example, `points + points` adds "
        "up to 6, but `jersey + jersey` only sets two 3s side by side. Lucky's armor bonus is 3."
    ),
    introduces=["const:int"],
    # The Example shows a number versus text (guide 9, S12), so it previews `+`: plus, as in math class.
    preview=["op:Add"],
    example='points = 3\njersey = "3"\nprint(points + points)\nprint(jersey + jersey)\n',
    example_output="6\n33",
    names=["armor_bonus", "weapon"],
    pick="a brass rune-axe",
    pair_talk="Pair talk: point at one value on your screen and ask your partner: number or text? Then swap.",
    predict=dict(
        q="What will the Example show in the Console?",
        code='points = 3\njersey = "3"\nprint(points + points)\nprint(jersey + jersey)\n',
        choices=["6\n33", "6\n6", "33\n33"],
        answer=0,
        explain=(
            "`points` holds the number 3, so `+` adds: 6. `jersey` holds the text `\"3\"`, so `+` only sets the "
            "two marks side by side: 33. Ask about any value: would I ever do math with this?"
        ),
    ),
    starter="# Lucky's armor bonus (a number):\n\n# Any weapon name (text):\n",
    checkpoints=[
        dict(
            id="armor-bonus",
            text="Make a box named `armor_bonus` that holds the number 3. No quotes: it's a number.",
            dictated=False,
            hints=[
                "Click on the empty line under `# Lucky's armor bonus (a number):`. Start the line with `armor_bonus = `.",
                "Does a number get quotes? Think of points in a game: you add them up.",
                "Write `armor_bonus = 3` under `# Lucky's armor bonus (a number):`, with no quotes around the 3.",
            ],
            checks=[
                box_check("armor_bonus", foreign=["points", "jersey", "max_mana", "dice", "character"]),
                num_check("armor_bonus"),
                (
                    "armor_bonus is 3",
                    "import ast as _ast\n"
                    "_threes = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                    "and any(type(_t).__name__ == 'Name' and _t.id == 'armor_bonus' for _t in _n.targets) "
                    "and type(_n.value).__name__ == 'Constant' and _n.value.value == 3]\n"
                    "assert armor_bonus == 3 or (_threes and armor_bonus == 4), "
                    "'`armor_bonus` holds ' + str(armor_bonus) + \". Lucky's armor bonus is 3: put 3 in `armor_bonus`.\"",
                ),
                bare_check(("int", "float")),
            ],
        ),
        dict(
            id="weapon",
            text="Make a box named `weapon` that holds any weapon you like, in quotes. Words are text, so they get quotes.",
            dictated=False,
            hints=[
                "Click on the empty line under `# Any weapon name (text):`. Start the line with `weapon = `.",
                "A weapon is words, and words are text. Text gets quotes.",
                "Write `weapon = \"a brass rune-axe\"` under `# Any weapon name (text):`, or put any weapon inside "
                "the quotes.",
            ],
            checks=[
                box_check("weapon", foreign=["points", "jersey", "max_mana", "dice", "snack", "character"]),
                text_check("weapon", "a weapon in quotes"),
                bare_check(("str",)),
            ],
            pass_line="Gearshift: Visor dims. One number, one piece of text. Logged.",
        ),
    ],
    solution=(
        "# Lucky's armor bonus (a number):\narmor_bonus = 3\n"
        "# Any weapon name (text):\nweapon = \"a brass rune-axe\"\n"
    ),
    partials=["# Lucky's armor bonus (a number):\narmor_bonus = 3\n# Any weapon name (text):\n"],
    assemble=dict(
        lines=["armor_bonus = 3", 'weapon = "a brass rune-axe"'],
        distractors=['armor_bonus = "3"', "3", "weapon = a brass rune-axe"],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Two boxes that look alike:\n"
                "```\narmor_bonus = 3\n^ a number: Python can\n  do math with it\n\n"
                "armor_bonus = \"3\"\n^ text: the mark 3,\n  like a word\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A jersey number",
            text=(
                "The 3 on a jersey names a player. Nobody adds two jerseys, so that 3 is like text. "
                "Points in a game are an amount you add up, so they are a number. Ask: would I ever do math with this?"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Python looks at the value. It sees `3` and makes a number. It sees `\"3\"` and makes text, "
                "because quotes always mean text."
            ),
        ),
        dict(
            angle="why",
            label="Why \"3\" isn't 3",
            text=(
                "Quotes mean these exact letters. `\"3\"` is the mark 3, the way `\"glug\"` is the letters g-l-u-g. "
                "Python won't do math with text. Next lesson you will add numbers, so keep them free of quotes."
            ),
        ),
        dict(angle="shorter", text="Words get quotes. Numbers don't."),
    ],
    bonus=dict(
        by="lucky",
        title="Polished armor",
        text=(
            "Gearshift polishes Lucky's armor, so the bonus goes up to 4. Add a new line that puts 4 in "
            "`armor_bonus`. Show the box once before the change and once after."
        ),
        hints=[
            "Put `print(armor_bonus)` right under `armor_bonus = 3`.",
            "Then add `armor_bonus = 4` and another `print(armor_bonus)`.",
        ],
        checks=[
            (
                "armor_bonus goes from 3 to 4, printed both times",
                "import ast as _ast\n"
                "_vals = [_n.value.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                "and any(type(_t).__name__ == 'Name' and _t.id == 'armor_bonus' for _t in _n.targets) "
                "and type(_n.value).__name__ == 'Constant']\n"
                "assert 4 in _vals and armor_bonus == 4, 'Add a line that makes `armor_bonus` hold 4.'\n"
                "assert '3' in _lines() and '4' in _lines() and _lines().index('3') < _lines().index('4'), "
                "'Print `armor_bonus` before the change (3) and after it (4).'",
            ),
        ],
        solution=(
            "# Lucky's armor bonus (a number):\narmor_bonus = 3\nprint(armor_bonus)\narmor_bonus = 4\nprint(armor_bonus)\n"
            "# Any weapon name (text):\nweapon = \"a brass rune-axe\"\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="required_roll = 12",
        why=(
            "You've seen this at the trap door. `required_roll = 12` had no quotes, because Python had to "
            "compare it with a dice roll. Numbers don't get quotes."
        ),
    ),
    takeaway="Numbers get no quotes: `armor_bonus = 3`. Text does: `weapon = \"Telegun\"`.",
    wrong_answers=[
        dict(why="the number in quotes", code='armor_bonus = "3"\nweapon = "Telegun"\n', fails_at=1, message_contains="quotes"),
        dict(why="a lone 3 with no box", code='3\nweapon = "Telegun"\n', fails_at=1, message_contains="no name in front"),
        dict(why="the wrong number", code='armor_bonus = 30\nweapon = "Telegun"\n', fails_at=1, message_contains="3"),
        dict(why="capital letters in the name", code='Armor_Bonus = 3\nweapon = "Telegun"\n', fails_at=1, message_contains="letter for letter"),
        dict(why="the example's name", code='points = 3\nweapon = "Telegun"\n', fails_at=1, message_contains="Example"),
        dict(why="the example's text box for the weapon", code='armor_bonus = 3\njersey = "Telegun"\n', fails_at=2,
             message_contains="Example"),
        dict(why="an earlier step's name (max_mana, from the keyboard warm-up)", code='max_mana = 3\nweapon = "Telegun"\n',
             fails_at=1, message_contains="earlier step"),
        dict(why="weapon text with no quotes", code="armor_bonus = 3\nweapon = Telegun\n", fails_at=0, message_contains="Telegun"),
        dict(why="weapon is a number", code="armor_bonus = 3\nweapon = 7\n", fails_at=2, message_contains="quotes"),
        dict(why="a lone weapon name with no box", code='armor_bonus = 3\n"Telegun"\n', fails_at=2, message_contains="no name in front"),
        dict(why="3, then a later line changes it to 30", code='armor_bonus = 3\narmor_bonus = 30\nweapon = "Telegun"\n',
             fails_at=1, message_contains="holds 30"),
        dict(why="def used to make the weapon box", code='armor_bonus = 3\ndef weapon(): "Telegun"\n', fails_at=2, message_contains="learn in Unit 3"),
        dict(why="unclosed quote on the weapon", code='armor_bonus = 3\nweapon = "Telegun\n', fails_at=0, message_contains="unterminated string"),
        dict(why="a space in the name", code='armor bonus = 3\nweapon = "Telegun"\n', fails_at=0, message_contains="invalid syntax"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="numbers-vs-text,make-variable", solo="false", dictates="",
             foreign_names="points,jersey,max_mana,dice,snack,character", twin="dice_count = 2") + "\n"
        "Structure pass (guide 9, S12): the Example was a box versus a word (`print(max_mana)` and "
        "`print(\"max_mana\")`, the quotes rule again), not a number versus text. It now puts 3 and `\"3\"` in two "
        "boxes and adds each to itself: 6 and 33, the jersey picture from Mar'tu's text. That needs `+`, so the "
        "exercise previews op:Add (plus, as in math class; gluing text is taught in 1C). The predict asks about "
        "the new Example. "
        "CP1 accepts armor_bonus == 3 (so `+3` passes too), or 3 followed by the side quest's `armor_bonus = 4`, "
        "so doing the side quest keeps CP1 green; 3 then 30 fails. WT 'Why \"3\" isn't 3' is the `why` angle. "
        "WA evidence: quoting numbers; lone values (A-04, B-02, B-03); Pizza/pizzas case (B-02, B-03)."
    ),
)

EXACT_NAMES = dict(
    id="exact-names",
    title="Exact names",
    martu=(
        "Names match letter for letter, capitals too, like a password. `Max_Mana` and `max_mana` are two "
        "different names. A name can't have a space, so use `_`, the underscore (Shift and `-`).\n"
        "Press Run. Read the title of the error box, then Python's last line. The mistake is on that line or "
        "the one above."
    ),
    names=["magical_affinity", "max_mana"],
    pair_talk=(
        "Pair talk: spell the name on line 1 and the name on line 2 out loud to your partner, letter by letter. "
        "Where do they differ?"
    ),
    starter="Max_Mana = 18\nprint(max_mana)\nmagical affinity = 9\nprint(magical_affinity)\n",
    checkpoints=[
        dict(
            id="no-spaces",
            text="Change the name on line 3 to `magical_affinity`. A name can't have a space, so `_` takes the place of the space.",
            dictated=True,
            hints=[
                "Look at the name on line 3. Start line 3 with `magical_affinity = `.",
                "Find the space between `magical` and `affinity`. Python can't read a name with a space in it.",
                "Type `_` in place of the space, so line 3 reads `magical_affinity = 9`. A name is one word, and `_` "
                "(Shift and `-`) joins the words.",
            ],
            checks=[
                box_check("magical_affinity", foreign=["glug_sips", "armor_bonus", "weapon"]),
                value_check("magical_affinity", 9),
                print_check("magical_affinity", typed="the number typed in",
                            missing="Keep the last line, `print(magical_affinity)`, so Python looks inside the box and shows what is there."),
            ],
        ),
        dict(
            id="same-name",
            text="Line 1 makes a box named `Max_Mana`, but line 2 asks for `max_mana`. Rename the box on line 1 so the two names match, letter for letter.",
            dictated=False,
            hints=[
                "Look at the names on lines 1 and 2. Line 1 should start with `max_mana = `.",
                "Spell the name on line 1 and the name on line 2, letter by letter. Which letters are capitals?",
                "Change `Max_Mana` on line 1 to `max_mana`, all small letters, so line 1 reads `max_mana = 18`. A name "
                "is like a password: every letter and capital counts.",
            ],
            checks=[
                box_check("max_mana", foreign=["glug_sips", "armor_bonus", "weapon"], extra="The box is made on line 1."),
                value_check("max_mana", 18),
                print_check("max_mana", typed="the number typed in"),
            ],
            pass_line="Oogrish: Steady, now. Letter for letter.",
        ),
    ],
    solution="max_mana = 18\nprint(max_mana)\nmagical_affinity = 9\nprint(magical_affinity)\n",
    assemble=dict(
        lines=["max_mana = 18", "print(max_mana)", "magical_affinity = 9", "print(magical_affinity)"],
        distractors=["Max_Mana = 18", "magical affinity = 9", "print(Max_Mana)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Spot the difference",
            text=(
                "Line them up, letter by letter:\n"
                "```\nMax_Mana\nmax_mana\n^   ^\nTwo letters differ, so\nPython sees two names.\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a password",
            text=(
                "A password with one wrong capital does not open your account. "
                "A name with one wrong capital does not open the box."
            ),
        ),
        dict(
            angle="step-by-step",
            label="A key in a lock",
            text=(
                "Python takes the name on line 2 like a key. It tries every box it has. `Max_Mana` is close, "
                "but close is not the same key. So Python says the name is not [[defined]]."
            ),
        ),
        dict(
            angle="English class",
            label="From English class",
            text=(
                "In English, a capital can change a word: Polish (from Poland) and polish (for shoes). "
                "Python goes further. Every capital, and every `_`, makes a different name."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "At the cabin door, pressing the left arrow made the game look for `move_left`, letter for letter. "
                "`Move_left` or `move left` would never be found. Your boxes work the same way."
            ),
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="Gearshift's sheet",
        text=(
            "Gearshift's sheet says `MAX MANA: 20`. Make a new box that holds 20, with a name Python accepts, "
            "and print it."
        ),
        hints=[
            "A name can't have a space or a colon. Try joining words with `_`.",
            "For example, a name like `gearshift_max_mana`, then `= 20`.",
        ],
        checks=[
            (
                "a new box holds 20 and is printed",
                "import ast as _ast\n"
                "_new = [_t.id for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' for _t in _n.targets "
                "if type(_t).__name__ == 'Name' and _t.id not in ('max_mana', 'Max_Mana', 'magical_affinity')]\n"
                "assert any(globals().get(_m) == 20 for _m in _new), 'Make a new box, with its own name, that holds 20.'\n"
                "assert '20' in _lines(), 'Print your new box so 20 shows.'",
            ),
        ],
        solution=(
            "max_mana = 18\nprint(max_mana)\nmagical_affinity = 9\nprint(magical_affinity)\n"
            "gearshift_max_mana = 20\nprint(gearshift_max_mana)\n"
        ),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='def move_left():\n    party.move("left")',
        why=(
            "You've seen this at the cabin door. The game pressed the left arrow and looked for `move_left`, "
            "letter for letter. Now you know why one capital would have broken it."
        ),
    ),
    takeaway="Names match letter for letter, capitals too. No spaces: use `_`.",
    wrong_answers=[
        dict(why="the starter: a space in a name", code="Max_Mana = 18\nprint(max_mana)\nmagical affinity = 9\nprint(magical_affinity)\n",
             fails_at=0, message_contains="invalid syntax"),
        dict(why="print(Max_Mana) instead of renaming", code="Max_Mana = 18\nprint(Max_Mana)\nmagical_affinity = 9\nprint(magical_affinity)\n",
             fails_at=2, message_contains="max_mana"),
        dict(why="words joined with no _", code="max_mana = 18\nprint(max_mana)\nmagicalaffinity = 9\nprint(magicalaffinity)\n",
             fails_at=1, message_contains="magical_affinity"),
        dict(why="capitals on the new name", code="max_mana = 18\nprint(max_mana)\nMagical_Affinity = 9\nprint(Magical_Affinity)\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="typed 18 instead of using the box", code="Max_Mana = 18\nprint(18)\nmagical_affinity = 9\nprint(magical_affinity)\n",
             fails_at=2, message_contains="max_mana"),
        dict(why="only line 3 mended: line 2 still breaks", code="Max_Mana = 18\nprint(max_mana)\nmagical_affinity = 9\nprint(magical_affinity)\n",
             fails_at=0, message_contains="max_mana"),
        dict(why="typed 9 on the last line instead of using the box", code="max_mana = 18\nprint(max_mana)\nmagical_affinity = 9\nprint(9)\n",
             fails_at=1, message_contains="Print the box instead"),
        dict(why="last line deleted", code="max_mana = 18\nprint(max_mana)\nmagical_affinity = 9\n",
             fails_at=1, message_contains="Keep the last line"),
        dict(why="18 put in quotes while renaming", code='max_mana = "18"\nprint(max_mana)\nmagical_affinity = 9\nprint(magical_affinity)\n',
             fails_at=2, message_contains="quotes"),
        dict(why="a dash in the name instead of _", code="max_mana = 18\nprint(max_mana)\nmagical-affinity = 9\nprint(magical_affinity)\n",
             fails_at=0, message_contains="cannot assign"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="exact-names", solo="false", dictates="1",
             foreign_names="glug_sips,Glug,armor_bonus,weapon", twin="Armor_Bonus versus armor_bonus") + "\n"
        "Python reports line 3 first (the space-in-name row), then line 2's NameError with "
        "\"Did you mean: 'Max_Mana'?\", where explainer rule 5 fires. No partials: a half-mended program crashes. "
        "WA evidence: space in a name (A-06); heath (A-08); Powrup (A-05); power_UP (B-01); Pizza/pizzas (B-02, B-03)."
    ),
)

# Every top-level `mana = <number>` line, in order (shared by two 1B-05 checks, which run separately).
MANA_VALUES = (
    "import ast as _ast\n"
    "_sets = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign']\n"
    "_mine = [_n.value.value for _n in _sets if type(_n.value).__name__ == 'Constant' "
    "and any(type(_t).__name__ == 'Name' and _t.id == 'mana' for _t in _n.targets)]\n"
)

CHANGE_THE_BOX = dict(
    id="change-the-box",
    title="A box can change",
    martu=(
        "Mana is a hero's magic power. A box holds one value at a time, like a small whiteboard: write 26, wipe "
        "it, write 21. In math, x = 26 "
        "and x = 21 can't both be true. In Python they happen one after the other, top to bottom, and only the "
        "newest value stays.\n"
        "Guess what prints, then press Run."
    ),
    names=["mana"],
    pair_talk=(
        "Pair talk: each of you picks 26, 21 or both, without showing. Reveal together, then run it on your "
        "own screens."
    ),
    predict=dict(
        q="What will `print(mana)` show in the Console?",
        choices=["26", "21", "26\n21"],
        answer=1,
        explain=(
            "Line 2 put 21 in the box, so 26 was gone. `print` shows what is in the box when it runs: 21.\n"
            "```\nline  code         mana holds\n1     mana = 26    26\n2     mana = 21    21\n"
            "3     print(mana)  21, so 21 prints\n```"
        ),
    ),
    starter="mana = 26\nmana = 21\nprint(mana)\n",
    checkpoints=[
        dict(
            id="mana-14",
            text="Add a new line right above `print(mana)`, and type `mana = 14` on it. You should see 14 in the Console.",
            dictated=True,
            hints=[
                "Look at line 2, `mana = 21`. Click at the end of line 2, press Enter, and start the new line with `mana = `.",
                "Which value is in the box when `print` runs?",
                "Write `mana = 14` above `print(mana)`. Then read it top to bottom:\n"
                "```\nline  code         mana holds\n1     mana = 26    26\n2     mana = 21    21\n"
                "3     mana = 14    14\n4     print(mana)  14, so 14 prints\n```",
            ],
            checks=[
                (
                    "mana holds 14",
                    MANA_VALUES +
                    "assert 'mana' in globals(), 'Make a box named `mana`: start a line with `mana = `.'\n"
                    "_v = mana\n"
                    "_near = [_t.id for _n in _sets for _t in _n.targets if type(_t).__name__ == 'Name' "
                    "and _t.id != 'mana' and _t.id.lower().rstrip('s') == 'mana']\n"
                    "assert type(_v).__name__ != 'str', \"`mana` holds text, because of the quotes. Numbers don't get quotes: take them off.\"\n"
                    "assert _v == 14 or not _near, 'Your new line uses the name `' + _near[0] + "
                    "'`, but the box is `mana`. Names match letter for letter, capitals too, so use `mana`.'\n"
                    "_newbox = [_t.id for _n in _sets for _t in _n.targets if type(_t).__name__ == 'Name' "
                    "and _t.id != 'mana' and globals().get(_t.id) == 14]\n"
                    "assert _v == 14 or not _newbox, 'Your new box `' + _newbox[0] + '` holds 14, but `mana` still holds ' + "
                    "str(_v) + '. Put 14 in `mana` itself: `mana = 14`.'\n"
                    "assert _v == 14 or 14 not in _mine, '`mana` got 14, but a later line put ' + str(_v) + "
                    "' back in. Python reads top to bottom, so put `mana = 14` last, right above `print(mana)`.'\n"
                    "assert _v == 14, '`mana` still holds ' + str(_v) + '. To put a new value in a box, use `=`: `mana = 14`.'",
                ),
                (
                    "the first two values are kept",
                    MANA_VALUES +
                    "assert 26 in _mine and 21 in _mine, 'Keep `mana = 26` and `mana = 21`. This step adds a new line "
                    "under them, so you can watch the box change.'",
                ),
                print_check(
                    "mana",
                    missing="Keep `print(mana)` at the end, so Python looks inside the box and shows what is there.",
                    show=False,
                    typed="the number typed in",
                ),
                (
                    "14 is printed",
                    "import re as _re\n"
                    "assert any(_re.search(r'\\b14\\b', _l) for _l in _lines()), '`print(mana)` ran before `mana` got 14, so it showed the old value. "
                    "Python reads top to bottom, so move `mana = 14` above `print(mana)`.'",
                ),
                (
                    "the last printed line shows 14",
                    "import re as _re\n"
                    "assert _lines() and _re.search(r'\\b14\\b', _lines()[-1]), "
                    "'Your last printed line should show 14. Keep `print(mana)` at the end, below `mana = 14`.'",
                ),
            ],
            pass_line="Mar'tu: 26, then 21, then 14. The old ones are gone, yes?",
        ),
    ],
    solution="mana = 26\nmana = 21\nmana = 14\nprint(mana)\n",
    assemble=dict(
        lines=["mana = 26", "mana = 21", "mana = 14", "print(mana)"],
        distractors=["mana - 14", 'mana = "14"'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "Read it one line at a time, and track the box:\n"
                "```\nline  code         mana holds\n1     mana = 26    26\n2     mana = 21    21  (26 is gone)\n"
                "3     print(mana)  21, so 21 prints\n```"
            ),
        ),
        dict(
            angle="picture",
            text="```\nmana:  26  ->  21  ->  14\n       --      --\n   (crossed out, gone)\n```",
        ),
        dict(
            angle="everyday",
            label="A whiteboard",
            text=(
                "A box is like a small whiteboard. Write 26. Wipe it, write 21. "
                "Anyone who reads it now sees only 21."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "When the barrier spell ran, the caster's mana got a new, smaller number, and the old one was gone. "
                "Same idea: new value in, old value out."
            ),
        ),
        dict(angle="shorter", text="One box, one value. The newest one wins."),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's glug",
        text=(
            "Lucky's glug (his drink) runs low: 5 sips, then 3, then 1. Above `mana = 26`, make a box named "
            "`glug_sips` that gets 5, then 3, then 1, with a `print(glug_sips)` after each one. Keep them at the top, "
            "so `print(mana)` still shows last."
        ),
        hints=[
            "Click at the start of line 1 and press Enter. On the new top line: `glug_sips = 5`, then `print(glug_sips)`.",
            "Then `glug_sips = 3`, print again, then `glug_sips = 1`, print again. All of it above `mana = 26`.",
        ],
        checks=[
            (
                "glug_sips goes 5, 3, 1, printed each time",
                "import ast as _ast\n"
                "_vals = [_n.value.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                "and any(type(_t).__name__ == 'Name' and _t.id == 'glug_sips' for _t in _n.targets) "
                "and type(_n.value).__name__ == 'Constant']\n"
                "assert _vals[-3:] == [5, 3, 1], 'Give `glug_sips` the values 5, then 3, then 1.'\n"
                "_seen = [_l for _l in _lines() if _l in ('5', '3', '1')]\n"
                "assert _seen[-3:] == ['5', '3', '1'], 'Print `glug_sips` after each change, so 5, 3 and 1 all show.'",
            ),
        ],
        solution=(
            "glug_sips = 5\nprint(glug_sips)\nglug_sips = 3\nprint(glug_sips)\nglug_sips = 1\nprint(glug_sips)\n"
            "mana = 26\nmana = 21\nmana = 14\nprint(mana)\n"
        ),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet=(
            "dialogue_input = \"Write what Mar'tu asks here\"\n"
            "dialogue_input = dialogue_input.lower()"
        ),
        why=(
            "You've seen this: Mar'tu's dialogue line. Line 2 put a new value in `dialogue_input`, and the old "
            "one was gone. That is all a box changing is."
        ),
    ),
    takeaway="A box holds one value at a time. A new `=` replaces the old value.",
    wrong_answers=[
        dict(why="the new line placed below the print", code="mana = 26\nmana = 21\nprint(mana)\nmana = 14\n",
             fails_at=1, message_contains="14"),
        dict(why="a dash instead of =", code="mana = 26\nmana = 21\nmana - 14\nprint(mana)\n",
             fails_at=1, message_contains="use `=`"),
        dict(why="the number in quotes", code='mana = 26\nmana = 21\nmana = "14"\nprint(mana)\n',
             fails_at=1, message_contains="quotes"),
        dict(why="the word mana printed last, so the last line is not 14",
             code='mana = 26\nmana = 21\nmana = 14\nprint(mana)\nprint("mana")\n',
             fails_at=1, message_contains="last printed line should show 14"),
        dict(why="an old value typed into a print below the box's print",
             code="mana = 26\nmana = 21\nmana = 14\nprint(mana)\nprint(21)\n",
             fails_at=1, message_contains="last printed line should show 14"),
        dict(why="typed 14 in the print instead of using the box", code="mana = 26\nmana = 21\nmana = 14\nprint(14)\n",
             fails_at=1, message_contains="Print the box instead"),
        dict(why="typed \"14\" as text in the print", code='mana = 26\nmana = 21\nmana = 14\nprint("14")\n',
             fails_at=1, message_contains="Print the box instead"),
        dict(why="quotes around the name in the print", code='mana = 26\nmana = 21\nmana = 14\nprint("mana")\n',
             fails_at=1, message_contains="Take the quotes off"),
        dict(why="old lines deleted, so the box never changes", code="mana = 14\nprint(mana)\n",
             fails_at=1, message_contains="Keep `mana = 26`"),
        dict(why="14 put in the middle, so 21 replaces it", code="mana = 26\nmana = 14\nmana = 21\nprint(mana)\n",
             fails_at=1, message_contains="a later line put 21 back"),
        dict(why="capital M on the new line", code="mana = 26\nmana = 21\nMana = 14\nprint(mana)\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="14 put in a new box, printed instead of mana (NEWBOX)", code="mana = 26\nmana = 21\nnew_mana = 14\nprint(new_mana)\n",
             fails_at=1, message_contains="Your new box `new_mana`"),
        dict(why="line 2 changed to 14 instead of adding a line", code="mana = 26\nmana = 14\nprint(mana)\n",
             fails_at=1, message_contains="Keep `mana = 26` and `mana = 21`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="reassign", solo="false", dictates="1",
             foreign_names="glow,max_mana,magical_affinity") + "\n"
        "Static step table: in the predict explanation (shown after any predict, so a wrong one sees it, G2 R16) "
        "and as the first angle (TR, open by default under Show me more). "
        "Catches 'both values stay' (the predict and its step table) and 'print shows everything computed "
        "earlier' (the new line below the `print` -> '14 is printed') (A-03, A-04). "
        "The step says ADD a line, so the checks keep `mana = 26` and `mana = 21` (deleting them, or changing line 2 "
        "to 14, skips watching the box change), need `print(mana)` itself (not a typed 14), and catch NEWBOX "
        "(14 put in a new box). Printed values are matched as whole words, so `print(\"mana is\", mana)` passes.\n"
        "Teacher ruling: the old no-26 rule ('only the newest value is printed') is gone, so printing after each "
        "change is allowed (`mana = 26`, `print(mana)`, `mana = 21`, `print(mana)`, `mana = 14`, `print(mana)` "
        "passes). In its place, 'the last printed line shows 14' (`_lines()[-1]`), which keeps `print(mana)` at "
        "the end, below `mana = 14`. The WA 'prints every value, believing they all stay' now passes and was "
        "removed. Because the last printed line must show 14, the side quest's glug lines go at the TOP (its text, "
        "hints and solution say so); appended at the bottom they would turn CP1 red on that run."
    ),
)

BROKEN_SPELL_1B = dict(
    id="broken-spell-1b",
    title="Broken spell",
    martu=(
        "Six lines, and lines 1 to 4 each have one mistake you've seen before. Fix one at a time: press Run, "
        "read the title of the error box, then Python's last line, and fix that line. "
        "Line 4 gets no error of its own. When Python stops on line 5 and can't find `hero`, the fix is on line 4."
    ),
    names=["weapon", "companion", "glug_sips", "hero"],
    pair_talk=(
        "Pair talk: take turns. One of you reads the title of the error box out loud, and the other "
        "points at the line number it gives. Each of you fixes it on your own screen."
    ),
    starter='"weapon" = "Telegun"\ndef companion = "Gearshift"\nglug_sips - 3\n"Lucky"\nprint(hero)\nprint(weapon)\n',
    checkpoints=[
        dict(
            id="line-1",
            text="Fix line 1 so it reads `weapon = \"Telegun\"`: take the quotes off the name `weapon`.",
            dictated=True,
            hints=[
                "Read the title of the error box: it points at line 1. Start line 1 with `weapon = `, "
                "with no quotes on the name.",
                "Look at line 1. Which word is the box's name? Does it have quotes around it?",
                "Delete the two `\"` around `weapon` on line 1, so line 1 reads `weapon = \"Telegun\"`. A box's name "
                "never goes in quotes. Only the value does.",
            ],
            checks=[
                box_check("weapon", foreign=["snack", "mana"]),
                text_check("weapon", "a weapon in quotes"),
                print_check("weapon", typed="the weapon typed in quotes",
                            missing="Keep the last line, `print(weapon)`, so Python looks inside the box and shows what is there."),
            ],
        ),
        dict(
            id="line-2",
            text="Fix line 2 so it reads `companion = \"Gearshift\"`: take out the word `def`.",
            dictated=True,
            hints=[
                "Read the title of the error box: it points at line 2. Start line 2 with `companion = `.",
                "Look at the first word on line 2. Does a box need it?",
                "Delete `def` and the space after it, so line 2 reads `companion = \"Gearshift\"`. `def` is for "
                "something you'll learn in Unit 3. A box is the name, `=`, then the value.",
            ],
            checks=[box_check("companion", foreign=["snack", "mana"]), text_check("companion", "a hero in quotes")],
        ),
        dict(
            id="line-3",
            text="Fix line 3 so `glug_sips` holds 3: change the `-` to `=`.",
            dictated=True,
            hints=[
                "Read the title of the error box: it points at line 3. Start line 3 with `glug_sips = `.",
                "Look at the sign between `glug_sips` and 3.",
                "Change the `-` on line 3 to `=`, so line 3 reads `glug_sips = 3`. The `-` sign means minus. "
                "The `=` sign puts a value in a box.",
            ],
            checks=[box_check("glug_sips", foreign=["snack", "mana"]), num_check("glug_sips"),
                    ("glug_sips is 3", "assert glug_sips == 3, 'Put 3 in `glug_sips`.'")],
        ),
        dict(
            id="line-4",
            text="Fix line 4: it has the value `\"Lucky\"` but no name, so line 5 can't find `hero`. Make line 4 a "
                 "box named `hero`.",
            dictated=False,
            hints=[
                "Python stops on line 5, but the fix is on line 4. Start line 4 with `hero = `.",
                "Line 5 prints `hero`. Which line should make that box?",
                "Type `hero = ` in front of `\"Lucky\"` on line 4. A value with no name in front is read and thrown "
                "away, so it needs a name.",
            ],
            checks=[
                box_check("hero", foreign=["snack", "mana"]),
                text_check("hero"),
                bare_check(),
                print_check("hero", typed="the hero typed in quotes",
                            missing="Keep `print(hero)`, so Python looks inside the box and shows what is there."),
            ],
            pass_line="Bomb Shell: Works.",
        ),
    ],
    solution='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
    assemble=dict(
        lines=['weapon = "Telegun"', 'companion = "Gearshift"', "glug_sips = 3", 'hero = "Lucky"', "print(hero)", "print(weapon)"],
        distractors=['"weapon" = "Telegun"', 'def companion = "Gearshift"', "glug_sips - 3"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Read the error box",
            text=(
                "1. Read the title at the top of the error box. It says what went wrong.\n"
                "2. Read *Python's last line*. It says the same thing in Python's words.\n"
                "3. Find the line number and fix that line. Press Run again.\n"
                "4. A new error is good news: Python got further."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Each mistake is a crack in the barrier. Patch one, press Run, and Python shows you the next crack. "
                "You don't need to see them all at once."
            ),
        ),
        dict(
            angle="shorter",
            text="Every box is `name = value`. No quotes on the name, no `def`, no `-`, and never a value with no name.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Break one on purpose",
        text=(
            "Three moves:\n"
            "1. At the bottom, add a line that makes a box whose name has a space in it. Press Run and read the "
            "error box.\n"
            "2. Put `#` at the start of that line, so it becomes a note.\n"
            "3. On the next line, write it again with `_` in place of the space."
        ),
        hints=[
            "A broken line looks like `glug left = 2`.",
            "Make it `# glug left = 2`, then write `glug_left = 2` on the next line.",
        ],
        checks=[
            (
                "the broken line is a note, with the mended line under it",
                "import re as _re\n"
                "_src = _source.splitlines()\n"
                "_ok = False\n"
                "for _i in range(len(_src) - 1):\n"
                "    _m = _re.match(r'\\s*#\\s*([A-Za-z_]\\w*)\\s+([A-Za-z_]\\w*)\\s*=', _src[_i])\n"
                "    if _m and _src[_i + 1].strip().startswith(_m.group(1) + '_' + _m.group(2)) "
                "and (_m.group(1) + '_' + _m.group(2)) in globals():\n"
                "        _ok = True\n"
                "assert _ok, 'Keep the broken line as a note, like `# glug left = 2`, and put the fixed line right under it.'",
            ),
        ],
        solution=(
            'weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n'
            "# glug left = 2\nglug_left = 2\n"
        ),
    ),
    takeaway="Every box is `name = value`: no quotes on the name, no `def`, no `-`.",
    wrong_answers=[
        dict(why="the starter: a quoted name on line 1", code='"weapon" = "Telegun"\ndef companion = "Gearshift"\nglug_sips - 3\n"Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="literal"),
        dict(why="def left on line 2", code='weapon = "Telegun"\ndef companion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="expected '('"),
        dict(why="def with brackets", code='weapon = "Telegun"\ndef companion() = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="expected ':'"),
        dict(why="the dash left on line 3", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips - 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="glug_sips"),
        dict(why="lines 1 to 3 mended, the lone \"Lucky\" left on line 4: Python's next message is about `hero`",
             code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\n"Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="'hero' is not defined"),
        dict(why="line 4 as a bare name (explainer rule 7)", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nLucky\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="Lucky"),
        dict(why="the lone value kept, hero made elsewhere", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\n"Lucky"\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=4, message_contains="no name in front"),
        dict(why="glug_sips in quotes", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = "3"\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=3, message_contains="quotes"),
        dict(why="prints mended by typing the values instead of using the boxes",
             code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint("Lucky")\nprint("Telegun")\n',
             fails_at=1, message_contains="Print the box instead"),
        dict(why="print lines deleted instead of mending the boxes they need",
             code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\n',
             fails_at=1, message_contains="Keep the last line"),
        dict(why="def made valid with brackets and a colon (a recipe, not a box)",
             code='weapon = "Telegun"\ndef companion(): "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=2, message_contains="learn in Unit 3"),
        dict(why="unclosed quote on line 4", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky\nprint(hero)\nprint(weapon)\n',
             fails_at=0, message_contains="unterminated string"),
        dict(why="Hero with a capital, on both lines", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nHero = "Lucky"\nprint(Hero)\nprint(weapon)\n',
             fails_at=4, message_contains="letter for letter"),
        dict(why="glug_sips given the wrong number while mending the dash", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 30\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=3, message_contains="Put 3"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="make-variable,read-traceback", solo="false", dictates="1,2,3",
             foreign_names="snack,mana") + "\n"
        "Teacher ruling: starter lines 3 and 4 swapped so the checkpoints follow Python's messages in order: "
        "cannot assign to literal (line 1), the DEF row (line 2, G1 R15), then at runtime rule 8 (the dash, "
        "line 3: `glug_sips` not defined), then rule 4 (`print(hero)` on line 5: `hero` not defined, with the "
        "bare \"Lucky\" on line 4). The bare value raises no error of its own; Mar'tu's last Learn line warns "
        "about it, and the WA 'lone \"Lucky\" left on line 4' proves Python's next message names `hero`. "
        "Checks run only once the program runs, so the per-line ticks all turn green together; no partials. "
        "pass_line sits on the last checkpoint (line-4). "
        "Can be done in pairs (pair_talk); every student mends it on their own screen."
    ),
)

SOLO_1B = dict(
    id="solo-1b",
    title="Show Mar'tu",
    martu=(
        "Your turn to show off: make one box of your own and show what is inside. A familiar is a wizard's "
        "animal helper, like an owl. Put any creature you like in a box named `familiar`. "
        "You have done this already tonight, yes?"
    ),
    solo=True,
    names=["familiar"],
    pick="a grumpy moth",
    starter="# 1. Make a box named familiar that holds any creature, in quotes.\n# 2. Print familiar.\n",
    checkpoints=[
        dict(
            id="make-familiar",
            text="Make a box named `familiar` that holds any creature, in quotes.",
            dictated=False,
            hints=[
                "Click at the end of the `# 1.` note and press Enter. Start the new line with `familiar = `.",
                "Name, then `=`, then a value. Which part needs quotes?",
            ],
            checks=[
                box_check("familiar", foreign=["companion", "character", "hero", "snack"]),
                text_check("familiar", "a creature in quotes"),
                bare_check(),
            ],
        ),
        dict(
            id="show-familiar",
            text="Show what is inside `familiar`. Put your line under the `# 2.` note.",
            dictated=False,
            hints=[
                "Click at the end of the `# 2.` note and press Enter. Start the new line with `print(`.",
                QUOTES_RULE,
            ],
            checks=[print_check("familiar", typed="the creature typed in quotes")],
            pass_line="Mar'tu: You did that on your own. One box, made and shown.",
        ),
    ],
    solution='# 1. Make a box named familiar that holds any creature, in quotes.\nfamiliar = "a grumpy moth"\n# 2. Print familiar.\nprint(familiar)\n',
    partials=['# 1. Make a box named familiar that holds any creature, in quotes.\nfamiliar = "a grumpy moth"\n# 2. Print familiar.\n'],
    assemble=dict(
        lines=['familiar = "a grumpy moth"', "print(familiar)"],
        distractors=['"a grumpy moth"', 'print("familiar")'],
    ),
    another_way=[
        dict(
            angle="picture",
            text="```\n  familiar\n+---------------+\n| your creature |\n+---------------+\n```\nThe name has no quotes. What goes inside does.",
        ),
        dict(angle="sentence frame", label="Fill the frame", text="The name with no quotes, then *gets* (`=`), then the value in quotes. Then print the box by its name."),
        dict(angle="shorter", text="`familiar = ` a creature in quotes. Then `print(familiar)`."),
    ],
    takeaway="On your own: `name = value`, then `print(name)`.",
    wrong_answers=[
        dict(why="a lone value, then print the value", code='"a grumpy moth"\nprint("a grumpy moth")\n', fails_at=1, message_contains="no name in front"),
        dict(why="print with quotes around the name", code='familiar = "a grumpy moth"\nprint("familiar")\n', fails_at=2, message_contains="word"),
        dict(why="an earlier exercise's name", code='character = "a grumpy moth"\nprint(character)\n', fails_at=1, message_contains="familiar"),
        dict(why="creature with no quotes", code="familiar = a grumpy moth\nprint(familiar)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="capital F", code='Familiar = "a grumpy moth"\nprint(Familiar)\n', fails_at=1, message_contains="letter for letter"),
        dict(why="prints the creature typed by hand instead of the box", code='familiar = "a grumpy moth"\nprint("a grumpy moth")\n',
             fails_at=2, message_contains="Print the box instead"),
        dict(why="def used to make the box", code='def familiar(): "a grumpy moth"\nprint(familiar)\n', fails_at=1, message_contains="learn in Unit 3"),
        dict(why="unclosed quote", code='familiar = "a grumpy moth\nprint(familiar)\n', fails_at=0, message_contains="unterminated string"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="make-variable,exact-names,quote-text", solo="true", dictates="",
             foreign_names="companion,character,hero,snack", seat_b="lantern_name (same checks, starter says lantern_name)") + "\n"
        "SOLO make-twin. Seat A (and anyone solo) gets familiar; seat B would get lantern_name once pair mode "
        "ships. Recorded, never blocking, never shown to a partner. Two hints only (schema); using one records "
        "the pass 'with structure'. Teacher ruling: the solo reads as showing off, not being watched, so Learn "
        "drops 'Nobody helps on this one'. The pass line keeps 'You did that on your own.' and says what they did "
        "(no 'On your map:': no skills map is on screen yet, guide 4.6 and S10)."
    ),
)

LESSON_1B = dict(
    kind="lesson",
    id="boxes-with-labels",
    title="Boxes With Labels",
    minutes=27,
    summary="Find the `_` and `=` keys, keep words or a number in a named box, use the exact name, and change what "
    "is inside.",
    notes="Lesson 1B (CC). Preceded by 1b-remembers. Exactly one SOLO (solo-1b); non-dictated checkpoints in 1B-02, "
    "1B-03, 1B-04, 1B-06, 1B-S. Structure pass (guide 9, S12): opens with keyboard-symbols (1W-04), moved here from "
    "the 1W warm-ups so it comes after print and # are taught (two more minutes).",
    exercises=[KEYBOARD_SYMBOLS, LABEL_A_BOX, NAME_AND_VALUE, NUMBERS_STAND_ALONE, EXACT_NAMES, CHANGE_THE_BOX, BROKEN_SPELL_1B, SOLO_1B],
)

# ---------------------------------------------------------------------------------------------
# Extra practice 1X-AB "Words and boxes" (pool)
# ---------------------------------------------------------------------------------------------

_NOTE_PICK = "Hours between bursts:\n48, 48, 47, 46\nThe decay is speeding up, yes?"

# For 1A-07: the most lines one `print` shows (_best), and whether that note is written in triple quotes
# (_best_triple; a triple quote inside a comment does not count). A note kept in a box and printed by name counts too.
NOTE_LINES = (
    "import ast as _ast\n"
    "_tree = _ast.parse(_source)\n"
    "def _note(_node):\n"
    "    if type(_node).__name__ == 'Constant' and type(_node.value).__name__ == 'str':\n"
    "        _seg = (_ast.get_source_segment(_source, _node) or '').lstrip('rRuU')\n"
    "        return len([_l for _l in _node.value.splitlines() if _l.strip()]), _seg[:3] in (chr(34) * 3, chr(39) * 3)\n"
    "    return None\n"
    "_boxes = {}\n"
    "for _n in _ast.walk(_tree):\n"
    "    if type(_n).__name__ == 'Assign' and _note(_n.value):\n"
    "        for _t in _n.targets:\n"
    "            if type(_t).__name__ == 'Name':\n"
    "                _boxes[_t.id] = _note(_n.value)\n"
    "_best, _best_triple = 0, False\n"
    "for _n in _ast.walk(_tree):\n"
    "    if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == 'print':\n"
    "        for _a in _n.args:\n"
    "            _info = _note(_a) or (_boxes.get(_a.id) if type(_a).__name__ == 'Name' else None)\n"
    "            if _info and (_info[0] > _best or (_info[0] == _best and _info[1])):\n"
    "                _best, _best_triple = _info\n"
)

MANY_LINES_AT_ONCE = dict(
    id="many-lines-at-once",
    title="Many lines at once",
    martu=(
        "Three quote marks in a row, `\"\"\"`, start text that can go over many lines. Three more end it. "
        "One `print` shows all of it, line by line, the way a poem keeps its line breaks. This is not a `#` note: "
        "Python prints it.\n"
        "My chalk wall works the same way. Mostly."
    ),
    introduces=["const:multiline_str"],
    example='print("""Glug canteen: half full.\nSmell: still terrible.""")\n',
    example_output="Glug canteen: half full.\nSmell: still terrible.",
    pick=_NOTE_PICK,
    predict=dict(
        q="What will this line show in the Console?",
        choices=["Hours between bursts:\n48, 48, 47", "Hours between bursts: 48, 48, 47"],
        answer=0,
        explain="Triple quotes keep the line break. The text prints on two lines, exactly as it is written.",
    ),
    starter='print("""Hours between bursts:\n48, 48, 47""")\n',
    checkpoints=[
        dict(
            id="three-line-note",
            text="Make one `print` show at least 3 lines of text. Keep the triple quotes.",
            dictated=False,
            hints=[
                "Click just before the closing `\"\"\"`, press Enter, and type a third line.",
                "Where does the text end? The closing `\"\"\")` goes after your last line.",
                "Add a line inside the triple quotes, like this:\n```python\nprint(\"\"\"Hours between bursts:\n"
                "48, 48, 47, 46\nThe decay is speeding up, yes?\"\"\")\n```\nThat shows three lines.",
            ],
            checks=[
                (
                    "one print shows 3 or more lines",
                    NOTE_LINES +
                    "assert _best >= 2 or _count('call:print') < 3, "
                    "'Those are separate `print` lines. Put all the text inside one `print`, between triple quotes.'\n"
                    "assert _best >= 3, 'Your longest `print` shows ' + str(_best) + (' line' if _best == 1 else ' lines') + "
                    "'. Press Enter inside the triple quotes and add a line, until one `print` shows 3.'",
                ),
                (
                    "uses triple quotes",
                    NOTE_LINES +
                    "assert _best_triple, 'Put triple quotes `\"\"\"` around the text, so it can go over many lines.'",
                ),
            ],
            pass_line="Mar'tu: Three lines, one spell. Good chalk.",
        ),
    ],
    solution='print("""Hours between bursts:\n48, 48, 47, 46\nThe decay is speeding up, yes?""")\n',
    assemble=dict(
        lines=['print("""Hours between bursts:', "48, 48, 47, 46", 'The decay is speeding up, yes?""")'],
        distractors=['print("Hours between bursts:")', 'The decay is speeding up, yes?")'],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Everything between the two sets of triple quotes shows, line breaks and all:\n"
                "```\nprint(\"\"\"  <- open\nline one\nline two\nline three\"\"\")  <- close\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Python finds the first `\"\"\"` and starts collecting. It keeps every letter and every line break "
                "until it finds the next `\"\"\"`. Then `print` shows it all."
            ),
        ),
        dict(angle="shorter", text="`\"\"\"` opens, `\"\"\"` closes. Press Enter in between for a new line."),
    ],
    bonus=dict(
        by="lucky",
        title="A sign for Lucky",
        text=(
            "Lucky wants a sign with his name in a frame. Inside one `print` with triple quotes, draw a frame around "
            "a word: a line of `-`, a line with `|` at each end, then a line of `-`. (`|` is Shift and the backslash key, right above Enter.)"
        ),
        hints=[
            "Three lines: a top edge of `-`, a middle line like `| Lucky |`, and a bottom edge of `-`.",
            "```python\nprint(\"\"\"+-----+\n| Hi! |\n+-----+\"\"\")\n```",
        ],
        checks=[
            (
                "one print draws a box with | and -",
                "import ast as _ast\n"
                "_ok = False\n"
                "for _n in _ast.walk(_ast.parse(_source)):\n"
                "    if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == 'print':\n"
                "        for _a in _n.args:\n"
                "            if type(_a).__name__ == 'Constant' and type(_a.value).__name__ == 'str':\n"
                "                _rows = [_l for _l in _a.value.splitlines() if _l.strip()]\n"
                "                if len(_rows) >= 3 and '|' in _a.value and '-' in _rows[0] and '-' in _rows[-1]:\n"
                "                    _ok = True\n"
                "assert _ok, 'Draw the frame in one `print`: a line of `-`, a line with `|` at each end, then a line of `-`.'",
            ),
        ],
        solution=(
            'print("""Hours between bursts:\n48, 48, 47, 46\nThe decay is speeding up, yes?""")\n'
            'print("""+-------+\n| Lucky |\n+-------+""")\n'
        ),
    ),
    takeaway="Triple quotes `\"\"\"` let one `print` show many lines of text.",
    wrong_answers=[
        dict(why="the starter: only 2 lines", code='print("""Hours between bursts:\n48, 48, 47""")\n', fails_at=1, message_contains="2 lines"),
        dict(why="three separate prints", code='print("Hours between bursts:")\nprint("48, 48, 47")\nprint("Get inside.")\n',
             fails_at=1, message_contains="one `print`"),
        dict(why="closing triple quotes missing", code='print("""Hours between bursts:\n48, 48, 47\nGet inside.)\n',
             fails_at=0, message_contains="unterminated triple-quoted"),
        dict(why="no triple quotes: line breaks typed as \\n, with a triple quote hidden in a comment",
             code='# """\nprint("Hours between bursts:\\n48, 48, 47\\nGet inside.")\n',
             fails_at=1, message_contains="triple quotes"),
        dict(why="two prints of 2 lines each", code='print("""Hours between bursts:\n48, 48""")\nprint("""47, 46\nGet inside.""")\n',
             fails_at=1, message_contains="2 lines"),
        dict(why="blank lines padding a 2-line note", code='print("""Hours between bursts:\n\n\n48, 48, 47""")\n',
             fails_at=1, message_contains="2 lines"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="print-text", solo="false", dictates="",
             foreign_names="") + "\n"
        "Kept id 1A-07. CP1 is checked on the longest single print (not `_count('call:print') == 1`), so the "
        "side quest's second print keeps CP1 green. The side quest is the prerequisite card for 1P2."
    ),
)

NAME_AND_VALUE_AGAIN = dict(
    id="name-and-value-again",
    title="Name and value, again",
    martu=(
        "Two boxes this time: one holds words, and one holds a number. Words get quotes, like someone's exact "
        "words in English class. Numbers don't get quotes. A satchel is a shoulder bag. Lucky's holds odd things.\n"
        "Then show both, yes?"
    ),
    example='backpack = "rope"\ngems = 2\nprint(backpack)\nprint(gems)\n',
    example_output="rope\n2",
    names=["satchel", "coins"],
    pick="three candles and a map",
    starter="# 1. A box named satchel (text):\n\n# 2. A box named coins (a number):\n\n# 3. Print both boxes:\n",
    checkpoints=[
        dict(
            id="satchel-box",
            text=(
                "Under the `# 1.` note, make a box named `satchel`. Put the things in Lucky's satchel (his "
                "shoulder bag) in it, in quotes."
            ),
            dictated=False,
            hints=[
                "Click on the empty line under `# 1. A box named satchel (text):`. Start the line with `satchel = `.",
                "What's in a bag is words, and words are text. Text gets quotes: `bag = \"rope\"`.",
                "Write `satchel = \"three candles and a map\"` under `# 1. A box named satchel (text):`, or put any "
                "words inside the quotes.",
            ],
            checks=[
                box_check("satchel", foreign=["backpack", "gems", "armor_bonus", "weapon"]),
                text_check("satchel", "words in quotes"),
                bare_check(("str",)),
            ],
        ),
        dict(
            id="two-boxes",
            text="Under the `# 2.` note, make a box named `coins` that holds any number, with no quotes.",
            dictated=False,
            hints=[
                "Click on the empty line under `# 2. A box named coins (a number):`. Start the line with `coins = `.",
                "Coins are an amount you can count, like points in a game. Does a number get quotes?",
                "Write `coins = 7` under `# 2. A box named coins (a number):`. Any number is fine.",
            ],
            checks=[
                box_check("coins", foreign=["backpack", "gems", "armor_bonus", "weapon"]),
                num_check("coins"),
                bare_check(("int", "float")),
            ],
        ),
        dict(
            id="print-both",
            text="Show both boxes: under the `# 3.` note, type `print(satchel)`, then `print(coins)` on the line after it.",
            dictated=True,
            hints=[
                "Click on the empty line under the `# 3.` note. Start the line with `print(`.",
                "The Example prints each box by name, with no quotes. Do the same with `satchel` and `coins`.",
                "Write `print(satchel)` under `# 3. Print both boxes:`, then `print(coins)` under it. " + QUOTES_RULE,
            ],
            checks=[print_check("satchel", typed="the words typed in quotes"), print_check("coins", typed="the number typed in")],
            pass_line="Lucky: Fine. But I'm keeping track.",
        ),
    ],
    solution=(
        "# 1. A box named satchel (text):\nsatchel = \"three candles and a map\"\n"
        "# 2. A box named coins (a number):\ncoins = 7\n"
        "# 3. Print both boxes:\nprint(satchel)\nprint(coins)\n"
    ),
    partials=[
        "# 1. A box named satchel (text):\nsatchel = \"three candles and a map\"\n"
        "# 2. A box named coins (a number):\n\n# 3. Print both boxes:\n",
        "# 1. A box named satchel (text):\nsatchel = \"three candles and a map\"\n"
        "# 2. A box named coins (a number):\ncoins = 7\n# 3. Print both boxes:\n",
    ],
    assemble=dict(
        lines=['satchel = "three candles and a map"', "coins = 7", "print(satchel)", "print(coins)"],
        distractors=['coins = "7"', 'print("satchel")'],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "```\nsatchel = \"three candles and a map\"\n^ words: quotes\n\n"
                "coins = 7\n^ a number: no quotes\n```"
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Two jars on my shelf. One has `satchel` chalked on it, and inside are words in quotes. "
                "The other has `coins`, and inside are coins you can count. No quotes on coins."
            ),
        ),
        dict(angle="shorter", text="Words get quotes. Numbers and box names don't."),
    ],
    takeaway="Text gets quotes. Numbers and box names don't.",
    wrong_answers=[
        dict(why="coins in quotes", code='satchel = "rope"\ncoins = "7"\nprint(satchel)\nprint(coins)\n', fails_at=2, message_contains="quotes"),
        dict(why="a lone number for coins", code='satchel = "rope"\n7\nprint(satchel)\nprint(7)\n', fails_at=2,
             message_contains="Put `coins = ` in front"),
        dict(why="coins left out", code='satchel = "rope"\nprint(satchel)\n', fails_at=2, message_contains="Make a box named `coins`"),
        dict(why="a lone value for satchel", code='"rope"\ncoins = 7\nprint("rope")\nprint(coins)\n', fails_at=1, message_contains="no name in front"),
        dict(why="print with quotes around the name", code='satchel = "rope"\ncoins = 7\nprint("satchel")\nprint(coins)\n', fails_at=3, message_contains="word"),
        dict(why="capital S", code='Satchel = "rope"\ncoins = 7\nprint(Satchel)\nprint(coins)\n', fails_at=1, message_contains="letter for letter"),
        dict(why="the example's names", code='backpack = "rope"\ngems = 2\nprint(backpack)\nprint(gems)\n', fails_at=1, message_contains="example"),
        dict(why="the example's name, misspelled", code='backpak = "rope"\ncoins = 7\nprint(backpak)\nprint(coins)\n', fails_at=1,
             message_contains="looks like `backpack`"),
        dict(why="prints the values typed by hand", code='satchel = "rope"\ncoins = 7\nprint("rope")\nprint(7)\n', fails_at=3,
             message_contains="Print the box instead"),
        dict(why="def used to make a box", code='def satchel(): "rope"\ncoins = 7\nprint(satchel)\nprint(coins)\n', fails_at=1,
             message_contains="learn in Unit 3"),
        dict(why="satchel holds a number", code='satchel = 4\ncoins = 7\nprint(satchel)\nprint(coins)\n', fails_at=1, message_contains="words in quotes"),
    ],
    notes=(
        meta(starter_level="S2", path="pool", skills="make-variable,numbers-vs-text,exact-names", solo="false",
             dictates="2", foreign_names="backpack,gems,armor_bonus,weapon") + "\n"
        "1B-T: the twin for deferral time (and a spaced twin for 1B-02/1B-03). Structure pass (guide 9, S12): the "
        "old step 1 made both boxes; it is now one step per box (satchel-box, then coins under the old id "
        "two-boxes, so a pass already saved still counts), each with its own hints and checks. The BARE check is "
        "split by kind, so a lone 7 for coins gets coins' own message (put `coins = ` in front), not satchel's."
    ),
)

EXTRA_1X_AB = dict(
    kind="lesson",
    id="extra-words-and-boxes",
    title="Extra practice: Words and boxes",
    optional=True,
    minutes=6,
    summary="More practice with quotes and boxes, for whenever you want it.",
    notes="1X-AB pool (1A-07, 1B-T). Optional; feeds twins, the spaced queue and early finishers.",
    exercises=[MANY_LINES_AT_ONCE, NAME_AND_VALUE_AGAIN],
)

ITEMS = [REMEMBERS_1B, LESSON_1B, EXTRA_1X_AB]
