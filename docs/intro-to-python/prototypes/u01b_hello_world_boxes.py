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
assert not ("__NAME__" in _defs and callable(globals().get("__NAME__"))), "`def` makes a recipe (a function), not a box. To make a box, write `__NAME__ = ` and then the value, with no `def`."
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
        _msg = "Python matches names letter for letter: you wrote `" + _near[0] + "`, the task needs `__NAME__`.__EXTRA__"
    elif _left and _left[0][0] == _left[0][1]:
        _msg = "`" + _left[0][0] + "` is a name from an example or an earlier step. This task's box is `__NAME__`."
    elif _left:
        _msg = "`" + _left[0][0] + "` looks like `" + _left[0][1] + "`, a name from an example or an earlier step. This task's box is `__NAME__`."
    elif _bare:
        _msg = "Line " + str(_bare[0]) + " is a value with no box, so Python made it and forgot it. Put `__NAME__ = ` in front of it."
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
        f"assert type(_v).__name__ == 'str', {'`' + name + '` holds `'!r} + repr(_v) + {'`. This step wants ' + want + '.'!r}\n"
        f"assert _v.strip(), '`{name}` holds empty quotes. Put some words between them.'",
    )


def num_check(name):
    """NUM: the box holds a whole number, not text that looks like one."""
    return (
        f"{name} holds a number",
        f"_v = {name}\n"
        f"assert type(_v).__name__ != 'str', \"`{name}` holds text, because of the quotes. Numbers don't need quotes.\"\n"
        f"assert type(_v).__name__ == 'int', '`{name}` should hold a whole number, like `3`.'",
    )


def bare_check(kinds=("str", "int", "float")):
    """BARE: no line is just a value (it raises no error, so only a check can catch it)."""
    return (
        "no value is left without a box",
        "import ast as _ast\n"
        "_bare = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        f"and type(_n.value).__name__ == 'Constant' and type(_n.value.value).__name__ in {tuple(kinds)!r}]\n"
        "assert not _bare, 'Line ' + str(_bare[0]) + ' is a value with no box, so Python made it and forgot it. "
        "Delete it, or put a name and `=` in front of it.'",
    )


def print_check(name, missing=None, show=True):
    """PRINT: print(name) with no quotes (not the word, not a value typed by hand), and the value shows.

    ``missing`` replaces the "add a print" message (for starters that already had the print line).
    ``show=False`` leaves out the "the value shows in the console" part, for exercises with their own message.
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
        f"assert _named or not _typed, 'That `print` shows a value typed by hand. Print the box instead: "
        f"`print({name})`, so Python opens it and shows what is inside.'\n"
        f"assert _named or not _quoted, 'That prints the word \"{name}\". Take the quotes off so Python opens the box.'\n"
        f"assert _named, {missing!r}"
    )
    if show:
        code += (
            f"\nassert any(str({name}).strip() in _l for _l in _lines()), "
            f"'Your `print({name})` runs before `{name}` gets its last value. "
            f"Move it below the line that puts the value in.'"
        )
    return (f"prints the box {name}", code)


def value_check(name, value):
    """The box holds this exact number (and says so kindly when it holds text that looks like one)."""
    return (
        f"{name} is {value}",
        f"_v = {name}\n"
        f"assert type(_v).__name__ != 'str', \"`{name}` holds text, because of the quotes. Numbers don't need quotes.\"\n"
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
        "Tonight: how to say something, how to keep something in a box, and how to let Python do the sums."
    ),
    goals=[
        "Show words on the screen with `print()`, in matching quotes",
        "Write `#` notes for humans, and switch a line off",
        "Make a box (variable) with `name = value`, using the exact name the task asks for",
        "Put a new value in a box, like `mana = mana - cost`",
        "Do math with `+`, `-`, `*` and `/`, and let the code combine your boxes",
        "Glue text together with `+` and `str()`, and draw a bar with `\"█\" * mana`",
        "Read Python's message and mend the slips everyone makes",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="variable",
        aliases=["variables", "box", "boxes"],
        plain="A box with a label. The label is the name. Inside is a value. You make one with `name = value`.",
        example='companion = "Gearshift"',
    ),
    dict(
        term="value",
        aliases=["values"],
        plain="The thing inside a box: text in quotes, like `\"Lucky\"`, or a number, like `26`.",
        example="mana = 26",
    ),
    dict(
        term="number",
        aliases=["numbers"],
        plain="A value Python can do math with. Numbers have no quotes: `3` is a number, `\"3\"` is text.",
        example="armor_bonus = 3",
    ),
    dict(
        term="defined",
        aliases=["not defined", "define"],
        plain=(
            "Made already. A name is defined once a line like `name = value` has run. "
            "\"Not defined\" means Python looked for something saved with that name and found nothing."
        ),
        example="NameError: name 'hero' is not defined",
    ),
    dict(
        term="triple quotes",
        aliases=["triple-quoted", "multi-line string"],
        plain="Three quote marks in a row, `\"\"\"`. The text between two sets of them can run over many lines.",
        example='print("""Line one\nLine two""")',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (1b-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_1B = dict(
    kind="quiz",
    id="1b-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from last lesson. Nothing is scored.",
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
                0: "With no quotes, Python looks for something saved with the name glug, and finds nothing.",
                2: "The quote opens but never closes, so Python can't tell where the words end. It stops with an error.",
            },
            explain="Words you want to show need quotes. `print(\"glug\")` shows glug.",
        ),
        dict(
            type="mc",
            id="hash-line",
            q="What does Python do with a line that starts with `#`?",
            choices=[
                "It skips it. The line is a note for humans.",
                "It shows it on the screen.",
                "It stops the program.",
            ],
            answer=0,
            why_wrong={
                1: "Only `print` shows things. A `#` line is skipped.",
                2: "Nothing stops. Python just skips that line and keeps going.",
            },
            explain="A line that starts with `#` is a note for humans. Python skips it.",
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 1B "Boxes With Labels"
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."

LABEL_A_BOX = dict(
    id="label-a-box",
    title="A box with a label",
    martu=(
        "A box ([[variable]]) has a label and something inside. `companion = \"Gearshift\"` makes a box labeled "
        "`companion` and puts the text inside. Read `=` as gets: companion gets Gearshift.\n"
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
        q="What will this print?",
        choices=["Gearshift\ncompanion", "companion\nGearshift", "Gearshift\nGearshift", "companion\ncompanion"],
        answer=0,
        explain=(
            "Line 2 has no quotes, so Python opens the box and shows what is inside: Gearshift. "
            "Line 3 has quotes, so it shows the exact letters: companion. " + QUOTES_RULE
        ),
    ),
    starter='companion = "Gearshift"\nprint(companion)\nprint("companion")\n',
    checkpoints=[
        dict(
            id="another-hero",
            text="Make sure line 1 starts with `companion = `. Then change the hero in the quotes to a different hero.",
            dictated=True,
            hints=[
                "Delete `Gearshift`, then type a new hero between the quotes.",
                "The label is left of `=`. The hero goes on the right, in quotes.",
                "Read it as: companion gets Gearshift. A box is `name = value`, so `snack = \"glug\"` makes a box "
                "named `snack` with glug inside. " + QUOTES_RULE,
            ],
            checks=[
                box_check("companion", foreign=["snack"]),
                text_check("companion", "a hero's name in quotes"),
                (
                    "companion is not the example's hero",
                    "assert companion.strip().lower() != 'gearshift', "
                    "\"`companion` still holds Gearshift, the example's hero. Put another hero in the quotes, "
                    "or use Mar'tu's pick.\"",
                ),
                print_check("companion", missing="Keep `print(companion)` on line 2, so you can see the new hero in the box."),
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
                "```\nprint(companion)    ->  opens the box   ->  Gearshift\n"
                "print(\"companion\")  ->  just the letters ->  companion\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a phone contact",
            text=(
                "A phone contact has a name with a number saved under it. Tap the name, and the phone uses what "
                "is saved. `print(companion)` taps the name. `print(\"companion\")` just reads the word out loud."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "A jar on my shelf with a chalk label. The label says `companion`. Inside is Gearshift. "
                "Ask for the jar by its label, and you get what is inside."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Python reads one line at a time:\n"
                "```\nline  code                     what happens\n"
                "1     companion = \"Gearshift\"  box companion gets Gearshift\n"
                "2     print(companion)         opens the box, shows Gearshift\n"
                "3     print(\"companion\")       shows the letters companion\n```"
            ),
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `\"companion\" = \"Gearshift\"` (a label never goes in quotes). "
                "Not this: `companion - \"Gearshift\"` (`-` subtracts). "
                "Not this: a lone `\"Gearshift\"` (made, then forgotten).\n"
                "This: `companion = \"Gearshift\"`."
            ),
        ),
        dict(
            angle="sentence frame",
            label="Fill the frame",
            text=(
                "Fill the frame: `____ = ____`. The left blank is the label, with no quotes. "
                "The right blank is the value, text in quotes. Like `companion = \"Bomb Shell\"`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants to be the companion. On a later line, give `companion` a new hero. "
            "Print it once before the change and once after."
        ),
        hints=[
            "Add a new line at the bottom: `companion = ` and a new hero in quotes.",
            "Then add `print(companion)` under it. The first `print(companion)` already shows the old hero.",
        ],
        checks=[
            (
                "companion gets two different heroes, both printed",
                "import ast as _ast\n"
                "_vals = [_n.value.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                "and any(type(_t).__name__ == 'Name' and _t.id == 'companion' for _t in _n.targets) "
                "and type(_n.value).__name__ == 'Constant']\n"
                "assert len(_vals) >= 2 and _vals[-1] != _vals[-2], 'Give `companion` a second, different hero on a later line.'\n"
                "assert str(_vals[-2]).strip() in _lines() and str(_vals[-1]).strip() in _lines(), "
                "'Print `companion` once before the change and once after it.'",
            ),
        ],
        solution='companion = "Bomb Shell"\nprint(companion)\nprint("companion")\ncompanion = "Lucky"\nprint(companion)\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet="dialogue_input = \"Write what Mar'tu asks here\"",
        why=(
            "You have seen this. Mar'tu's dialogue line lived in a box: the label `dialogue_input`, "
            "and your words inside, in quotes. Now you know why it was written that way."
        ),
    ),
    takeaway="`name = value` makes a box. `print(name)` shows what is inside; `print(\"name\")` shows the word.",
    wrong_answers=[
        dict(why="value left as the example's Gearshift", code='companion = "Gearshift"\nprint(companion)\nprint("companion")\n',
             fails_at=1, message_contains="example"),
        dict(why="`companion = ` deleted: a bare value with no box", code='"Gearshift"\nprint(companion)\nprint("companion")\n',
             fails_at=0, message_contains="companion"),
        dict(why="hero name with no quotes", code="companion = Bomb Shell\nprint(companion)\n",
             fails_at=0, message_contains="invalid syntax"),
        dict(why="capital letter in the name", code='Companion = "Bomb Shell"\nprint(Companion)\n',
             fails_at=1, message_contains="letter for letter"),
        dict(why="prints the new hero typed by hand instead of the box", code='companion = "Bomb Shell"\nprint("Bomb Shell")\nprint("companion")\n',
             fails_at=1, message_contains="typed by hand"),
        dict(why="quotes put on line 2 too, so the box is never opened", code='companion = "Bomb Shell"\nprint("companion")\nprint("companion")\n',
             fails_at=1, message_contains="Take the quotes off"),
        dict(why="print lines deleted", code='companion = "Bomb Shell"\n', fails_at=1, message_contains="Keep `print(companion)`"),
        dict(why="def used to make the box (valid Python, but a recipe, not a box)", code='def companion(): "Bomb Shell"\nprint(companion)\nprint("companion")\n',
             fails_at=1, message_contains="`def` makes a recipe"),
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
        "To make a box, write the name, then `=`, then the [[value]]. The name has no quotes. "
        "The value is your hero, in quotes.\n"
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
        q="What will this print?",
        code='"Bomb Shell"\nprint(character)\n',
        choices=["Bomb Shell", "ERROR: name 'character' is not defined", "character"],
        answer=1,
        explain=(
            "Line 1 is a value with no name, so Python makes it and forgets it. No box called `character` was "
            "ever made, so line 2 says *not defined*. A box needs a name AND a value: `character = \"Bomb Shell\"`."
        ),
    ),
    starter="# Your box goes here:\n\n# Print it here:\n",
    checkpoints=[
        dict(
            id="make-character",
            text="Make a box named `character` that holds your hero's name, in quotes.",
            dictated=False,
            hints=[
                "Start the line with `character = `.",
                "Find the word `character` in this step. That is the box's label.",
                "A box is `name = value`, like `companion = \"Gearshift\"`. The name has no quotes. Text values do.",
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
            text="Print `character`, with no quotes around the name.",
            dictated=True,
            hints=[
                "Start the line with `print(`.",
                "The Example prints its box by name, with no quotes. Do the same with your box: `character`.",
                QUOTES_RULE,
            ],
            checks=[print_check("character")],
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
                "```\ncharacter    =     \"Zelda\"\n  label     gets    value\n(no quotes)        (quotes)\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a phone contact",
            text=(
                "Saving a contact needs a name AND a number. A number with no name is lost in the list. "
                "A box needs a label AND a value, the same way."
            ),
        ),
        dict(
            angle="sentence frame",
            label="Fill the frame",
            text="Say it as you type it: name, no quotes, gets value. `character = \"Zelda\"`.",
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `def (\"character\")`. Not this: `\"character\" = \"Zelda\"`. "
                "Not this: `character - \"Zelda\"`. Not this: a lone `\"Zelda\"`.\n"
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
        title="What's in it for me?",
        text=(
            "Lucky wants a weapon too. Make a box named `weapon` that holds any weapon, in quotes. "
            "Then write your own `#` note right above each box, saying what it holds."
        ),
        hints=[
            "A note is a line that starts with `#`, like `# my hero`.",
            "Put your note on the line just above `character = ...`, and another just above `weapon = ...`.",
        ],
        checks=[
            ("weapon holds text", "assert type(weapon).__name__ == 'str' and weapon.strip(), 'Make `weapon` hold a weapon name, in quotes.'"),
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
                "'Write your own `#` note on the line just above `' + _box + ' = ...`.'",
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
            "You have seen this. The four dialogue options were four boxes: a name, then `=`, then words in "
            "quotes. Name AND value, every time."
        ),
    ),
    takeaway="A box needs a name AND a value: `character = \"Zelda\"`. Then `print(character)`, no quotes.",
    wrong_answers=[
        dict(why="a lone value, then print the value", code='"Zelda"\nprint("Zelda")\n', fails_at=1, message_contains="no box"),
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
        dict(why="box made but a lone value left too", code='"Zelda"\ncharacter = "Zelda"\nprint(character)\n', fails_at=1, message_contains="no box"),
        dict(why="prints the hero typed by hand instead of the box", code='character = "Zelda"\nprint("Zelda")\n', fails_at=2, message_contains="typed by hand"),
        dict(why="def used to make the box (valid Python: a recipe, not a box)", code='def character(): "Zelda"\nprint(character)\n',
             fails_at=1, message_contains="`def` makes a recipe"),
        dict(why="def with the box inside it", code='def character():\n    character = "Zelda"\nprint(character)\n',
             fails_at=1, message_contains="`def` makes a recipe"),
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
    title="Numbers stand alone",
    martu=(
        "Numbers stand alone, with no quotes. `\"3\"` is text that looks like a [[number]]. "
        "`3` is a number Python can do math with.\n"
        "Lucky says his armor bonus is 30. It is 3. We use the 3."
    ),
    introduces=["const:int"],
    example='max_mana = 26\nprint(max_mana)\nprint("max_mana")\n',
    example_output="26\nmax_mana",
    names=["armor_bonus", "weapon"],
    pick="a brass rune-axe",
    pair_talk="Pair talk: point at one value on your screen and ask your partner: number or text? Then swap.",
    predict=dict(
        q="What will the Example print?",
        code='max_mana = 26\nprint(max_mana)\nprint("max_mana")\n',
        choices=["26\nmax_mana", "max_mana\nmax_mana", "26\n26"],
        answer=0,
        explain="`print(max_mana)` opens the box: 26. `print(\"max_mana\")` shows the exact letters. " + QUOTES_RULE,
    ),
    starter="# Lucky's armor bonus (a number):\n\n# Any weapon name (text):\n",
    checkpoints=[
        dict(
            id="armor-bonus",
            text="Make `armor_bonus` holding Lucky's armor bonus, 3, as a number.",
            dictated=False,
            hints=[
                "Start the line with `armor_bonus = `.",
                "Does a number need quotes?",
                "`dice = 2` is a number box. `dice = \"2\"` is text that only looks like a number.",
            ],
            checks=[
                box_check("armor_bonus", foreign=["max_mana", "dice", "character"]),
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
            text="Make `weapon` holding any weapon name, as text.",
            dictated=False,
            hints=[
                "Start the line with `weapon = `.",
                "A weapon name is words. Words need quotes.",
                "`snack = \"glug\"` is a text box. `dice = 2` is a number box.",
            ],
            checks=[
                box_check("weapon", foreign=["max_mana", "dice", "snack", "character"]),
                text_check("weapon", "a weapon name in quotes"),
                bare_check(("str",)),
            ],
            pass_line="Gearshift: Visor dims. One number, one name. Logged.",
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
                "```\narmor_bonus = 3     a number: Python can do math with it\n"
                "armor_bonus = \"3\"   text: just the letter 3, like a word\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A price tag",
            text=(
                "A price tag that says \"3\" is a label. Three coins in your hand are an amount. "
                "Text in quotes is the tag. A number with no quotes is the coins."
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
                "Quotes mean these exact letters. `\"3\"` is the letter 3, like `\"glug\"` is the letters g-l-u-g. "
                "Python won't do math with letters. Next lesson you will add numbers, so keep them free of quotes."
            ),
        ),
        dict(angle="shorter", text="Words get quotes. Numbers don't."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Gearshift polishes Lucky's armor. On a new line, make `armor_bonus` hold 4. "
            "Print it once before the change and once after."
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
            "You have seen this at the trap door. `required_roll = 12` had no quotes, because Python had to "
            "compare it with a dice roll. Numbers stand alone."
        ),
    ),
    takeaway="Numbers have no quotes: `armor_bonus = 3`. Text does: `weapon = \"Telegun\"`.",
    wrong_answers=[
        dict(why="the number in quotes", code='armor_bonus = "3"\nweapon = "Telegun"\n', fails_at=1, message_contains="quotes"),
        dict(why="a lone 3 with no box", code='3\nweapon = "Telegun"\n', fails_at=1, message_contains="no box"),
        dict(why="the wrong number", code='armor_bonus = 30\nweapon = "Telegun"\n', fails_at=1, message_contains="3"),
        dict(why="capital letters in the name", code='Armor_Bonus = 3\nweapon = "Telegun"\n', fails_at=1, message_contains="letter for letter"),
        dict(why="the example's name", code='max_mana = 3\nweapon = "Telegun"\n', fails_at=1, message_contains="example"),
        dict(why="weapon text with no quotes", code="armor_bonus = 3\nweapon = Telegun\n", fails_at=0, message_contains="Telegun"),
        dict(why="weapon is a number", code="armor_bonus = 3\nweapon = 7\n", fails_at=2, message_contains="quotes"),
        dict(why="a lone weapon name with no box", code='armor_bonus = 3\n"Telegun"\n', fails_at=2, message_contains="no box"),
        dict(why="3, then a later line changes it to 30", code='armor_bonus = 3\narmor_bonus = 30\nweapon = "Telegun"\n',
             fails_at=1, message_contains="holds 30"),
        dict(why="def used to make the weapon box", code='armor_bonus = 3\ndef weapon(): "Telegun"\n', fails_at=2, message_contains="`def` makes a recipe"),
        dict(why="unclosed quote on the weapon", code='armor_bonus = 3\nweapon = "Telegun\n', fails_at=0, message_contains="unterminated string"),
        dict(why="a space in the name", code='armor bonus = 3\nweapon = "Telegun"\n', fails_at=0, message_contains="invalid syntax"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="numbers-vs-text,make-variable", solo="false", dictates="",
             foreign_names="max_mana,dice,snack,character", twin="dice_count = 2") + "\n"
        "CP1 accepts armor_bonus == 3 (so `+3` passes too), or 3 followed by the side quest's `armor_bonus = 4`, "
        "so doing the side quest keeps CP1 green; 3 then 30 fails. WT 'Why \"3\" isn't 3' is the `why` angle. "
        "WA evidence: quoting numbers; lone values (A-04, B-02, B-03); Pizza/pizzas case (B-02, B-03)."
    ),
)

EXACT_NAMES = dict(
    id="exact-names",
    title="Exact names",
    martu=(
        "Python matches names letter for letter. `Max_Mana` and `max_mana` are two different names. "
        "A name cannot have a space in it; use `_` instead.\n"
        "Remember the cabin door? The game looked for `move_left` exactly. It could not find `Move_left`.\n"
        "Run it. Read the last line of Python's message first."
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
            text="Line 3: a name can't have a space. Make it `magical_affinity`.",
            dictated=True,
            hints=[
                "Start line 3 with `magical_affinity = `.",
                "Look at line 3. Find the space between the two words.",
                "A name is one word. Join the words with `_`: `glug_sips`, not `glug sips`.",
            ],
            checks=[
                box_check("magical_affinity", foreign=["glug_sips", "armor_bonus", "weapon"]),
                value_check("magical_affinity", 9),
                print_check("magical_affinity",
                            missing="Keep the last line, `print(magical_affinity)`, so Python opens the box and shows what is inside."),
            ],
        ),
        dict(
            id="same-name",
            text="Make line 2 print 18, using the name the task gives: `max_mana`.",
            dictated=False,
            hints=[
                "Line 1 should start with `max_mana = `.",
                "Compare the names on lines 1 and 2, letter by letter.",
                "A name is like a password: every letter and capital counts. `Glug` and `glug` are two different names.",
            ],
            checks=[
                box_check("max_mana", foreign=["glug_sips", "armor_bonus", "weapon"], extra="Rename the box on line 1."),
                value_check("max_mana", 18),
                print_check("max_mana"),
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
                "```\nMax_Mana\nmax_mana\n^   ^      two letters differ, so Python sees two names\n```"
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
            "Gearshift's sheet says `MAX MANA: 20`. Make a box for it with a name Python accepts, "
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
            "You have seen this at the cabin door. The game pressed the left arrow and looked for `move_left`, "
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
             fails_at=1, message_contains="typed by hand"),
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
        "A box holds one value at a time. Put a new value in, and the old one is gone.\n"
        "Mana works like this. So does Lucky's glug, sadly.\n"
        "Guess what prints, then run it."
    ),
    names=["mana"],
    pair_talk=(
        "Pair talk: each of you picks 26, 21 or both, without showing. Reveal together, then run it on your "
        "own screens."
    ),
    predict=dict(
        q="What will this print?",
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
            text="Add a line that puts 14 in `mana`, above the `print`.",
            dictated=True,
            hints=[
                "Click at the end of line 2, press Enter, and start the new line with `mana = `.",
                "Which value is in the box when `print` runs?",
                "Read it top to bottom:\n"
                "```\nline  code          glow holds\n1     glow = 5      5\n2     glow = 8      8\n"
                "3     print(glow)   8, so 8 prints\n```",
            ],
            checks=[
                (
                    "mana holds 14",
                    MANA_VALUES +
                    "assert 'mana' in globals(), 'Make a box named `mana`: start a line with `mana = `.'\n"
                    "_v = mana\n"
                    "_near = [_t.id for _n in _sets for _t in _n.targets if type(_t).__name__ == 'Name' "
                    "and _t.id != 'mana' and _t.id.lower().rstrip('s') == 'mana']\n"
                    "assert type(_v).__name__ != 'str', \"`mana` holds text, because of the quotes. Numbers don't need quotes.\"\n"
                    "assert _v == 14 or not _near, 'Python matches names letter for letter: you wrote `' + _near[0] + "
                    "'`, the task needs `mana`.'\n"
                    "_newbox = [_t.id for _n in _sets for _t in _n.targets if type(_t).__name__ == 'Name' "
                    "and _t.id != 'mana' and globals().get(_t.id) == 14]\n"
                    "assert _v == 14 or not _newbox, 'Your new box `' + _newbox[0] + '` holds 14, but `mana` still holds ' + "
                    "str(_v) + '. Put 14 in `mana` itself: `mana = 14`.'\n"
                    "assert _v == 14 or 14 not in _mine, '`mana` got 14, but a later line put ' + str(_v) + "
                    "' back in. Put `mana = 14` last, just above the `print`.'\n"
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
                    missing="Keep `print(mana)` at the end, so Python opens the box and shows what is inside.",
                    show=False,
                ),
                (
                    "14 is printed",
                    "import re as _re\n"
                    "assert any(_re.search(r'\\b14\\b', _l) for _l in _lines()), '`print(mana)` ran before `mana` got 14, so it showed the old value. "
                    "Put the new line above the `print`.'",
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
        title="What's in it for me?",
        text=(
            "Lucky's glug goes 5, then 3, then 1. Make `glug_sips` and print it after each change. "
            "Put these lines at the top, above `mana = 26`, so `mana` still gets the last word."
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
            "You have seen this: Mar'tu's dialogue line. Line 2 put a new value in `dialogue_input`, and the old "
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
             fails_at=1, message_contains="typed by hand"),
        dict(why="typed \"14\" as text in the print", code='mana = 26\nmana = 21\nmana = 14\nprint("14")\n',
             fails_at=1, message_contains="typed by hand"),
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
        "Four lines, four slips you have seen before. Mend them one at a time.\n"
        "Read the last line of Python's message first. Then look at the line it names. "
        "Mend that line, run again, and see what Python finds next.\n"
        "One slip Python stays quiet about: a value with no box."
    ),
    names=["weapon", "companion", "glug_sips", "hero"],
    pair_talk=(
        "Pair talk: take turns. One of you reads the last line of Python's message out loud; the other points "
        "at the line it names. Each of you mends it on your own screen."
    ),
    starter='"weapon" = "Telegun"\ndef companion = "Gearshift"\nglug_sips - 3\n"Lucky"\nprint(hero)\nprint(weapon)\n',
    checkpoints=[
        dict(
            id="line-1",
            text="Mend line 1 so it makes a box: `weapon = \"Telegun\"`.",
            dictated=True,
            hints=[
                "Start line 1 with `weapon = `, with no quotes on the name.",
                "Look at line 1. Which word is the label?",
                "The name of a box never goes in quotes. Only the value does: `snack = \"glug\"`.",
            ],
            checks=[
                box_check("weapon", foreign=["snack", "mana"]),
                text_check("weapon", "a weapon name in quotes"),
                print_check("weapon", missing="Keep the last line, `print(weapon)`, so Python opens the box and shows what is inside."),
            ],
        ),
        dict(
            id="line-2",
            text="Mend line 2 the same way: `companion = \"Gearshift\"`.",
            dictated=True,
            hints=[
                "Start line 2 with `companion = `.",
                "Look at the first word on line 2.",
                "`def` makes a recipe (a function). To make a box (a variable), write `name = value`, with no `def`.",
            ],
            checks=[box_check("companion", foreign=["snack", "mana"]), text_check("companion", "a hero's name in quotes")],
        ),
        dict(
            id="line-3",
            text="Mend line 3 so `glug_sips` holds 3.",
            dictated=True,
            hints=[
                "Start line 3 with `glug_sips = `.",
                "Look at the sign between `glug_sips` and 3.",
                "To put a value in a box, use `=`. The `-` sign subtracts.",
            ],
            checks=[box_check("glug_sips", foreign=["snack", "mana"]), num_check("glug_sips"),
                    ("glug_sips is 3", "assert glug_sips == 3, 'Put 3 in `glug_sips`.'")],
        ),
        dict(
            id="line-4",
            text="Line 4 should make a box named `hero`.",
            dictated=False,
            hints=[
                "Start line 4 with `hero = `.",
                "Line 5 prints `hero`. Which line should make that box?",
                "A value on its own is made and forgotten. Give it a label: `snack = \"glug\"`.",
            ],
            checks=[
                box_check("hero", foreign=["snack", "mana"]),
                text_check("hero"),
                bare_check(),
                print_check("hero", missing="Keep `print(hero)`, so Python opens the box and shows what is inside."),
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
            label="Read the message",
            text=(
                "1. Read the last line of the message first. It says what went wrong.\n"
                "2. Find the line number it names.\n"
                "3. Mend only that line, then run again.\n"
                "4. A new message is good news: Python got further."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Each slip is a crack in the barrier. Patch one, run, and Python shows you the next crack. "
                "You do not need to see them all at once."
            ),
        ),
        dict(
            angle="shorter",
            text="Every box is `name = value`. No quotes on the name, no `def`, no `-`, never a value alone.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Write one line that gets the \"a name can't have a space\" message. Run it and read the message. "
            "Then turn that line into a `#` note, and write the mended line right under it."
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
                "assert _ok, 'Keep the broken line as a note, like `# glug left = 2`, and put the mended line right under it.'",
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
             fails_at=4, message_contains="no box"),
        dict(why="glug_sips in quotes", code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = "3"\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=3, message_contains="quotes"),
        dict(why="prints mended by typing the values instead of using the boxes",
             code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint("Lucky")\nprint("Telegun")\n',
             fails_at=1, message_contains="typed by hand"),
        dict(why="print lines deleted instead of mending the boxes they need",
             code='weapon = "Telegun"\ncompanion = "Gearshift"\nglug_sips = 3\nhero = "Lucky"\n',
             fails_at=1, message_contains="Keep the last line"),
        dict(why="def made valid with brackets and a colon (a recipe, not a box)",
             code='weapon = "Telegun"\ndef companion(): "Gearshift"\nglug_sips = 3\nhero = "Lucky"\nprint(hero)\nprint(weapon)\n',
             fails_at=2, message_contains="`def` makes a recipe"),
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
        "Your turn to show off: make one box of your own and show what is inside. "
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
                "Start the line with `familiar = `.",
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
            text="Show what is inside `familiar`.",
            dictated=False,
            hints=[
                "Start the line with `print(`.",
                QUOTES_RULE,
            ],
            checks=[print_check("familiar")],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ make a box with `name = value`.",
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
            text="```\n  familiar\n+---------------+\n| your creature |\n+---------------+\n```\nThe label has no quotes. What goes inside does.",
        ),
        dict(angle="sentence frame", label="Fill the frame", text="Name, no quotes, gets value in quotes. Then print the name."),
        dict(angle="shorter", text="`familiar = ` a creature in quotes. Then `print(familiar)`."),
    ],
    takeaway="On your own: `name = value`, then `print(name)`.",
    wrong_answers=[
        dict(why="a lone value, then print the value", code='"a grumpy moth"\nprint("a grumpy moth")\n', fails_at=1, message_contains="no box"),
        dict(why="print with quotes around the name", code='familiar = "a grumpy moth"\nprint("familiar")\n', fails_at=2, message_contains="word"),
        dict(why="an earlier exercise's name", code='character = "a grumpy moth"\nprint(character)\n', fails_at=1, message_contains="familiar"),
        dict(why="creature with no quotes", code="familiar = a grumpy moth\nprint(familiar)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="capital F", code='Familiar = "a grumpy moth"\nprint(Familiar)\n', fails_at=1, message_contains="letter for letter"),
        dict(why="prints the creature typed by hand instead of the box", code='familiar = "a grumpy moth"\nprint("a grumpy moth")\n',
             fails_at=2, message_contains="typed by hand"),
        dict(why="def used to make the box", code='def familiar(): "a grumpy moth"\nprint(familiar)\n', fails_at=1, message_contains="`def` makes a recipe"),
        dict(why="unclosed quote", code='familiar = "a grumpy moth\nprint(familiar)\n', fails_at=0, message_contains="unterminated string"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="make-variable,exact-names,quote-text", solo="true", dictates="",
             foreign_names="companion,character,hero,snack", seat_b="lantern_name (same checks, starter says lantern_name)") + "\n"
        "SOLO make-twin. Seat A (and anyone solo) gets familiar; seat B would get lantern_name once pair mode "
        "ships. Recorded, never blocking, never shown to a partner. Two hints only (schema); using one records "
        "the pass 'with structure'. Teacher ruling: the solo reads as showing off, not being watched, so Learn "
        "drops 'Nobody helps on this one' and the pass line ticks the skill on the student's map."
    ),
)

LESSON_1B = dict(
    kind="lesson",
    id="boxes-with-labels",
    title="Boxes With Labels",
    minutes=25,
    summary="Keep a value in a labeled box, use the exact name, and change what is inside.",
    notes="Lesson 1B (CC). Preceded by 1b-remembers. Exactly one SOLO (solo-1b); non-dictated checkpoints in 1B-02, 1B-03, 1B-04, 1B-06, 1B-S.",
    exercises=[LABEL_A_BOX, NAME_AND_VALUE, NUMBERS_STAND_ALONE, EXACT_NAMES, CHANGE_THE_BOX, BROKEN_SPELL_1B, SOLO_1B],
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
        "Three quote marks in a row, `\"\"\"`, start a note that can run over many lines. "
        "Three more end it. One `print` shows the whole note, line by line.\n"
        "My chalk wall works the same way. Mostly."
    ),
    introduces=["const:multiline_str"],
    example='print("""Glug canteen: half full.\nSmell: still terrible.""")\n',
    example_output="Glug canteen: half full.\nSmell: still terrible.",
    pick=_NOTE_PICK,
    predict=dict(
        q="What will this print?",
        choices=["Hours between bursts:\n48, 48, 47", "Hours between bursts: 48, 48, 47"],
        answer=0,
        explain="Triple quotes keep the line break. The note prints on two lines, just as it is written.",
    ),
    starter='print("""Hours between bursts:\n48, 48, 47""")\n',
    checkpoints=[
        dict(
            id="three-line-note",
            text="Make one `print` show a chalk note of at least 3 lines. Keep the triple quotes.",
            dictated=False,
            hints=[
                "Click just before the closing `\"\"\"`, press Enter, and type a third line.",
                "Where does the note end? The closing `\"\"\")` goes after your last line.",
                "Triple quotes hold many lines:\n```python\nprint(\"\"\"Up\nDown\nUp again\"\"\")\n```\nThat shows three lines.",
            ],
            checks=[
                (
                    "one print shows 3 or more lines",
                    NOTE_LINES +
                    "assert _best >= 2 or _count('call:print') < 3, "
                    "'Those are separate `print` lines. Put the whole note inside one `print`, with triple quotes.'\n"
                    "assert _best >= 3, 'Your longest `print` shows ' + str(_best) + (' line' if _best == 1 else ' lines') + "
                    "'. Press Enter inside the triple quotes and add a line, until one `print` shows 3.'",
                ),
                (
                    "uses triple quotes",
                    NOTE_LINES +
                    "assert _best_triple, 'Use triple quotes `\"\"\"` around the note, so it can run over many lines.'",
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
                "Everything between the two sets of triple quotes goes on the slate, line breaks and all:\n"
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
        title="What's in it for me?",
        text=(
            "Lucky wants a sign with his name in a box. Draw a tiny box around a word, using `|` and `-` "
            "inside one `print` with triple quotes."
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
                "assert _ok, 'Draw the box in one `print`: a line of `-`, a line with `|` at each end, then a line of `-`.'",
            ),
        ],
        solution=(
            'print("""Hours between bursts:\n48, 48, 47, 46\nThe decay is speeding up, yes?""")\n'
            'print("""+-------+\n| Lucky |\n+-------+""")\n'
        ),
    ),
    takeaway="`\"\"\"` lets one `print` show many lines.",
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
        "Two boxes this time. One holds words, one holds a number. Words get quotes. Numbers stand alone.\n"
        "Then show both, yes?"
    ),
    example='backpack = "rope"\ngems = 2\nprint(backpack)\nprint(gems)\n',
    example_output="rope\n2",
    names=["satchel", "coins"],
    pick="three candles and a map",
    starter="# 1. A box named satchel (text):\n\n# 2. A box named coins (a number):\n\n# 3. Print both boxes:\n",
    checkpoints=[
        dict(
            id="two-boxes",
            text="Make `satchel` holding what is in Lucky's satchel, as text, and `coins` holding any number of coins.",
            dictated=False,
            hints=[
                "Start one line with `satchel = ` and the next with `coins = `.",
                "Which box holds words, and which holds a number? Only words get quotes.",
                "`backpack = \"rope\"` is a text box. `gems = 2` is a number box.",
            ],
            checks=[
                box_check("satchel", foreign=["backpack", "gems", "armor_bonus", "weapon"]),
                text_check("satchel", "words in quotes"),
                box_check("coins", foreign=["backpack", "gems", "armor_bonus", "weapon"]),
                num_check("coins"),
                bare_check(),
            ],
        ),
        dict(
            id="print-both",
            text="Print both boxes: `print(satchel)` and `print(coins)`.",
            dictated=True,
            hints=[
                "Start a line with `print(`.",
                "The Example prints each box by name, with no quotes. Do the same with `satchel` and `coins`.",
                QUOTES_RULE,
            ],
            checks=[print_check("satchel"), print_check("coins")],
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
        "# 2. A box named coins (a number):\ncoins = 7\n# 3. Print both boxes:\n"
    ],
    assemble=dict(
        lines=['satchel = "three candles and a map"', "coins = 7", "print(satchel)", "print(coins)"],
        distractors=['coins = "7"', 'print("satchel")'],
    ),
    another_way=[
        dict(
            angle="picture",
            text="```\nsatchel = \"three candles and a map\"   words: quotes\ncoins = 7                            number: no quotes\n```",
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Two jars on my shelf. One label says `satchel`, and inside is a note in quotes. "
                "The other says `coins`, and inside are coins you can count. No quotes on coins."
            ),
        ),
        dict(angle="shorter", text="Words in quotes, numbers alone, names never in quotes."),
    ],
    takeaway="Text in quotes, numbers alone, names never in quotes.",
    wrong_answers=[
        dict(why="coins in quotes", code='satchel = "rope"\ncoins = "7"\nprint(satchel)\nprint(coins)\n', fails_at=1, message_contains="quotes"),
        dict(why="a lone value for satchel", code='"rope"\ncoins = 7\nprint("rope")\nprint(coins)\n', fails_at=1, message_contains="no box"),
        dict(why="print with quotes around the name", code='satchel = "rope"\ncoins = 7\nprint("satchel")\nprint(coins)\n', fails_at=2, message_contains="word"),
        dict(why="capital S", code='Satchel = "rope"\ncoins = 7\nprint(Satchel)\nprint(coins)\n', fails_at=1, message_contains="letter for letter"),
        dict(why="the example's names", code='backpack = "rope"\ngems = 2\nprint(backpack)\nprint(gems)\n', fails_at=1, message_contains="example"),
        dict(why="the example's name, misspelled", code='backpak = "rope"\ncoins = 7\nprint(backpak)\nprint(coins)\n', fails_at=1,
             message_contains="looks like `backpack`"),
        dict(why="prints the values typed by hand", code='satchel = "rope"\ncoins = 7\nprint("rope")\nprint(7)\n', fails_at=2,
             message_contains="typed by hand"),
        dict(why="def used to make a box", code='def satchel(): "rope"\ncoins = 7\nprint(satchel)\nprint(coins)\n', fails_at=1,
             message_contains="`def` makes a recipe"),
        dict(why="satchel holds a number", code='satchel = 4\ncoins = 7\nprint(satchel)\nprint(coins)\n', fails_at=1, message_contains="words in quotes"),
    ],
    notes=(
        meta(starter_level="S2", path="pool", skills="make-variable,numbers-vs-text,exact-names", solo="false",
             dictates="2", foreign_names="backpack,gems,armor_bonus,weapon") + "\n"
        "1B-T: the twin for deferral time (and a spaced twin for 1B-02/1B-03)."
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
