"""Unit 1 "Hello World", part a: the 1-A1 card, warm-ups 1W, and Lesson 1A "Words in Quotes".

Spec: curriculum.md, "## Unit 1 · Hello World" (1-A1, 1W-02, 1W-04, 1A-01 to 1A-06, 1A-08, 1A-S).
1A-07 (triple quotes) is a pool item and lives in u01b.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. This part re-grounds them:
early, certain wins; errors framed as information; campaign links are "you've seen this, now you'll get it".
Every student has their own device. Pair talk is optional; every checkpoint is solo.

Help ladder (curriculum 2.2) as fields: hints[0] Start me off, hints[1] Point (where to look), another_way,
hints[2] Teach (tiny example with other words), assemble (More structure), solution (Show).

Terminology (2.9): no "box" and no "variable" anywhere in 1A. That word starts in 1B-01.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u01a
"""

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
        term="string",
        aliases=["strings", "text"],
        plain="Text inside quotes: letters, digits, spaces or marks, strung together like beads on a string. "
        "Python shows it exactly as you typed it.",
        example='"Shield up."',
    ),
    dict(
        term="quotes",
        aliases=["quote", "quote mark", "quote marks"],
        plain="The marks `\"` or `'` around text. They come in pairs, one before and one after, like quotation "
        "marks around someone's exact words in English class.",
        example='"Steady, now."',
    ),
    dict(
        term="parentheses",
        aliases=["parenthesis", "brackets", "bracket", "round brackets"],
        plain="The marks `(` and `)`, the same marks you use in math class. They come in pairs: `print` keeps "
        "what it shows between them.",
        example='print("Hi")',
    ),
    dict(
        term="print",
        aliases=["print()"],
        plain="Shows something on the screen, in the Console under your code. In Python, print means show on "
        "the screen, not print on paper.",
        example='print("Barrier\'s holding.")',
    ),
    dict(
        term="run",
        aliases=["runs", "Run button"],
        plain="Tell Python to do your code, from the top line down. Press ▶ Run, just above your code, as often "
        "as you like: running unfinished code is fine.",
    ),
    dict(
        term="console",
        aliases=["the console"],
        plain="The space under your code where Python's answers appear: what `print` shows, and Python's "
        "error messages.",
    ),
    dict(
        term="error message",
        aliases=["error messages", "message from Python"],
        plain="Python's note that it stopped at a line it couldn't run, like a teacher's note in the margin: it "
        "points to the spot, and it isn't a grade. Read the box's title, then Python's last line, then fix the "
        "line with that number.",
        example="SyntaxError: unterminated string literal",
    ),
    dict(
        term="comment",
        aliases=["comments"],
        plain="A note for people: a line that starts with `#` (Shift+3). Python skips it, the way actors skip "
        "saying the stage directions in a play script.",
        example="# Lucky's lines for tonight",
    ),
    dict(
        term="mend",
        aliases=["mends", "mended", "slip", "slips"],
        plain="To fix a small mistake in your code, the way you mend a small tear in a sleeve. A slip is a "
        "small mistake.",
        example='print("Hi)   becomes   print("Hi")',
    ),
]

# ---------------------------------------------------------------------------------------------
# Shared hidden check code (never shown to students)
# ---------------------------------------------------------------------------------------------

# BARE (2.5): words on their own line with no print. Python makes the text and forgets it, silently.
BARE_WORDS = (
    "import ast as _ast\n"
    "_bare = [n.lineno for n in _ast.parse(_source).body if isinstance(n, _ast.Expr) "
    "and isinstance(n.value, _ast.Constant) and isinstance(n.value.value, str)]\n"
    "assert not _bare, 'Line %d has words in quotes but no `print`, so nothing shows. "
    "Put `print(` before the quotes and `)` after.' % (_bare[0] if _bare else 0)"
)

# Every # note in the student's code, as (line number, text). Tokenizing ignores a # inside quotes.
NOTES = (
    "import io as _io, tokenize as _tk\n"
    "_notes = [(t.start[0], t.string) for t in _tk.generate_tokens(_io.StringIO(_source).readline) "
    "if t.type == _tk.COMMENT]\n"
)


def shows(text, where, extra_ok=(".",), starts_ok=False):
    """A check that some printed line is exactly `text` (a final mark in extra_ok is optional).

    With starts_ok, a line that starts with `text` and goes on after a space or mark counts too
    ("Get inside, yes?" shows "Get inside"). A curly apostrophe counts as a straight one (phone and tablet
    keyboards type them). When the line is not there, the message names the nearest slip, in this order:
      1. the words are in quotes on their own line with no `print` (BARE),
      2. a printed line differs only by capitals (STREXACT),
      3. only by spaces or marks (STREXACT),
      4. the words are inside a longer printed line,
      5. by a letter or two (a spelling slip),
    and otherwise says the line is not showing yet, plus `where`.
    """
    bare = text.rstrip(".!?")
    options = [bare] + [bare + mark for mark in extra_ok]
    head = "Your line shows `"
    should = "`, but it should show `" + text + "`: "
    longer = ("`, which has more than `" + text + "` in it. Show `" + text + "` on a line of its own.")
    missing = "`" + text + "` is not showing yet. " + where
    return (
        f"_want = {options!r}\n"
        "_fix = lambda s: s.replace('\\u2019', \"'\")\n"
        f"_starts = {bool(starts_ok)!r}\n"
        "_ok = lambda l: _fix(l) in _want or (_starts and _fix(l).startswith(_want[0]) "
        "and _fix(l)[len(_want[0]):][:1] in (' ', ',', '.', '!', '?'))\n"
        "_msg = ''\n"
        "if not any(_ok(l) for l in _lines()):\n"
        "    import ast as _ast, difflib as _dl\n"
        "    _key = lambda s: ''.join(c for c in _fix(s).lower() if c.isalnum())\n"
        "    _sim = lambda s: _dl.SequenceMatcher(None, _key(s), _key(_want[0])).ratio()\n"
        "    _bare = [n.lineno for n in _ast.parse(_source).body if isinstance(n, _ast.Expr) "
        "and isinstance(n.value, _ast.Constant) and isinstance(n.value.value, str) "
        "and _key(n.value.value) == _key(_want[0])]\n"
        "    _close = sorted(_lines(), key=lambda l: -_sim(l))\n"
        "    _l = _close[0] if _close else ''\n"
        "    _longer = [l for l in _lines() if _key(_want[0]) in _key(l)]\n"
        "    if _bare:\n"
        "        _msg = ('Line ' + str(_bare[0]) + ' has the words in quotes but no `print`, so nothing shows. '\n"
        "                'Put `print(` before the quotes and `)` after.')\n"
        "    elif _l and _fix(_l).lower().rstrip('.!?') == _want[0].lower() and _fix(_l).rstrip('.!?') != _want[0]:\n"
        f"        _msg = {head!r} + _l + {should!r} + 'capitals count. Python shows exactly what is inside the quotes.'\n"
        "    elif _l and _key(_l) == _key(_want[0]):\n"
        f"        _msg = {head!r} + _l + {should!r} + 'spaces, marks and capitals all count. Python shows exactly what is inside the quotes.'\n"
        "    elif _longer:\n"
        f"        _msg = 'Your line shows `' + _longer[0] + {longer!r}\n"
        "    elif _l and _sim(_l) >= 0.75:\n"
        f"        _msg = {head!r} + _l + {should!r} + 'check it letter by letter. Python shows exactly what is inside the quotes.'\n"
        "    else:\n"
        f"        _msg = {missing!r}\n"
        "assert not _msg, _msg"
    )


# ---------------------------------------------------------------------------------------------
# 1-A1 card
# ---------------------------------------------------------------------------------------------

HOW_MARTU_TEACHES = dict(
    kind="article",
    id="how-martu-teaches",
    title="How Mar'tu Teaches",
    minutes=1,
    summary="One minute: how ▶ Run, 💡 Help and Your steps work.",
    body=(
        "Press ▶ [[run|Run]], above your code. Python answers in the [[console|Console]], under your code.\n"
        "Running unfinished code is fine. An error is not a grade: it says what Python couldn't read.\n"
        "Your steps: ✓ done, ● the step you're on, ○ still to come.\n"
        "Stuck? Press 💡 Help, under the Console. Each press gives more, up to the line itself. "
        "Your hints are private.\n"
        "Nothing here is timed."
    ),
    notes=(
        "meta: path=CC; kind=card; words<=60. Draft text from the curriculum (49 words) plus the checkpoint "
        "legend line. Still needed from the site: the three pictures (Run button -> console; the Help control "
        "under a checkpoint; the checkpoint list) and the [Start 1A] button. The lessons are the main path. "
        "The Quick Check is not a button on this card: the site's unit page already shows its offer to everyone "
        "as a quieter secondary choice ('Already know this? About 12 minutes, no hints'). "
        "The article schema has no image or button fields, so they are not in this prototype. Every other "
        "feature is introduced by just-in-time coach marks (2.2). Body unchanged (words<=60)."
    ),
)

# ---------------------------------------------------------------------------------------------
# Lesson 1W "Before the First Spell" (warm-ups, on under "Show me more")
# ---------------------------------------------------------------------------------------------

WHAT_AN_ERROR_LOOKS_LIKE = dict(
    id="what-an-error-looks-like",
    title="What an error looks like",
    martu=(
        "`print` means show on the screen, not on paper: this line shows `Shield up.` in the "
        "[[console|Console]], the box under your code. Press ▶ Run, just above your code. Then you'll break it "
        "on purpose, and Python will show an [[error message]]. That's not a grade. It's like a teacher's note "
        "in the margin: it points to the spot."
    ),
    introduces=["call:print", "const:str"],
    starter='print("Shield up.")\n',
    checkpoints=[
        dict(
            id="press-run",
            text="Press the ▶ Run button, just above your code. You should see `Shield up.` in the Console.",
            dictated=True,
            hints=[
                "You don't need to type anything yet. Find the ▶ Run button, just above your code.",
                "▶ Run sends your code to Python. Python does each line, and what `print` shows appears in the "
                "Console, under your code.",
                'Press ▶ Run. Line 1 shows `Shield up.` in the Console: the text between the quotes of '
                '`print("Shield up.")`.',
            ],
            checks=[
                ("shows a line", "assert _lines(), 'Nothing showed in the Console. Press Reset code to get "
                 "`print(\"Shield up.\")` back, then press Run.'"),
            ],
            pass_line="Mar'tu: Shield up. Next, you break it on purpose. That is safe, yes?",
        ),
        dict(
            id="close-the-quote",
            text=(
                "Three moves, in order:\n"
                '1. Delete the `"` right after `Shield up.` and press Run. An error appears. That\'s the plan.\n'
                "2. Read the box in the Console. Its title says what went wrong.\n"
                '3. Put the `"` back, change the `.` to `!`, and press Run. You should see `Shield up!`.'
            ),
            dictated=True,
            hints=[
                'Look at the `"` right after `Shield up.` on line 1.\n'
                'To break the line: click right after that `"` and press Backspace once.\n'
                'Already broken? Type the `"` back in the same spot (Shift and the `\'` key).',
                "The box's title says a quote is missing. Python's last line says *unterminated*, which means "
                'never ended: the text has no closing `"`.',
                'Type `"` right after `Shield up.`, then change the `.` to `!`. Line 1 becomes '
                '`print("Shield up!")`. Press Run.',
            ],
            checks=[
                (
                    "shows Shield up!",
                    "import ast as _ast\n"
                    "_l = [l.replace('\\u2019', \"'\") for l in _lines()]\n"
                    "_key = lambda s: ''.join(c for c in s.lower() if c.isalnum())\n"
                    "_bare = [n.lineno for n in _ast.parse(_source).body if isinstance(n, _ast.Expr) "
                    "and isinstance(n.value, _ast.Constant) and isinstance(n.value.value, str)]\n"
                    "_near = [l for l in _l if _key(l) == 'shieldup']\n"
                    "_msg = ''\n"
                    "if 'Shield up!' not in _l:\n"
                    "    if _bare:\n"
                    "        _msg = ('Line ' + str(_bare[0]) + ' has the words in quotes but no `print`, so nothing '\n"
                    "                'shows. Put `print(` before the quotes and `)` after.')\n"
                    "    elif 'Shield up.' in _l:\n"
                    "        _msg = ('Your line still shows `Shield up.`, with a `.` at the end. If you have not broken it '\n"
                    "                'yet, do move 1 first. Then put the `\"` back, change the `.` to `!`, and press Run.')\n"
                    "    elif _near and _near[0].rstrip('.!?') != 'Shield up' and _near[0].rstrip('.!?').lower() == 'shield up':\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. Capitals count: Python shows exactly what is '\n"
                    "                'inside the quotes. Make it `Shield up!`, with a capital S.')\n"
                    "    elif _near and _near[0].rstrip('.!?') == 'Shield up':\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. Step 2 needs a `!` at the end: '\n"
                    "                'make it `Shield up!` and press Run.')\n"
                    "    elif _near:\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. Spaces, marks and capitals all count. '\n"
                    "                'Make it `Shield up!` and press Run.')\n"
                    "    else:\n"
                    "        _msg = ('`Shield up!` is not showing yet. Press Reset code, next to Run, to get '\n"
                    "                '`print(\"Shield up.\")` back. Then change the `.` to `!` and press Run.')\n"
                    "assert not _msg, _msg",
                ),
            ],
            pass_line="Mar'tu: You broke it, read the box, and fixed it. That is the whole trick.",
        ),
    ],
    solution='print("Shield up!")\n',
    partials=['print("Shield up.")\n'],
    another_way=[
        dict(
            angle="picture",
            text=(
                "Press *Show Python's full message* in the box, and you see this:\n"
                "```text\n"
                'File "main.py", line 1\n'
                '  print("Shield up.)\n'
                "        ^\n"
                "SyntaxError: unterminated ...\n"
                "```\n"
                "1. Read the last line first. *Syntax* is how a line is put together, as in English class, so a "
                "*SyntaxError* is a line Python can't read.\n"
                "2. *Unterminated* means never ended: the text has no closing quote.\n"
                "3. The top line gives the line number, line 1. Fix that line."
            ),
        ),
        dict(
            angle="everyday",
            label="Something everyday",
            text=(
                "It is like a friend saying \"I couldn't read the end of your note.\" "
                "They are not upset. They are telling you where to look."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text='Delete the `"` after `Shield up.` and press Run. Read the box. Put the `"` back, make the `.` '
                 'a `!`, and press Run.',
        ),
    ],
    wrong_answers=[
        dict(why="broken on purpose and not mended yet: the quote is still open", code='print("Shield up.)\n',
             fails_at=0, message_contains="unterminated"),
        dict(why="starter unchanged: ran it, but never broke it or changed the mark", code='print("Shield up.")\n',
             fails_at=2, message_contains="change the `.` to `!`"),
        dict(why="puts the quote back with the other quote mark", code="print(\"Shield up!')\n", fails_at=0,
             message_contains="unterminated"),
        dict(why="puts the quote back after the bracket instead of before it", code='print("Shield up!)"\n',
             fails_at=0, message_contains="never closed"),
        dict(why="removes the opening quote instead of the closing one", code="print(Shield up.)\n",
             fails_at=0, message_contains="comma"),
        dict(why="deletes the `.` instead of the quote, and never adds `!`", code='print("Shield up")\n',
             fails_at=2, message_contains="`!` at the end"),
        dict(why="retyped in lower case", code='print("shield up!")\n', fails_at=2, message_contains="Capitals"),
        dict(why="words in quotes with no print: nothing shows at all", code='"Shield up!"\n', fails_at=1,
             message_contains="Press Run"),
        dict(why="check-breaker: old line kept, new words added with no print (BARE)",
             code='print("Shield up.")\n"Shield up!"\n', fails_at=2, message_contains="no `print`"),
        dict(why="check-breaker: a space lost", code='print("Shieldup!")\n', fails_at=2,
             message_contains="Spaces, marks and capitals"),
        dict(why="check-breaker: line replaced with other words", code='print("Ready.")\n', fails_at=2,
             message_contains="Reset code"),
    ],
    takeaway="When Python stops, read the box's title, then Python's last line. Fix the line it gives and press "
             "Run again.",
    notes=(
        "meta: starter_level=S4; path=CC; contingent=show-me-more (K); skills=print-text,read-traceback; "
        "solo=false; dictates=1,2; foreign_names=. "
        "Teaches the explainer footer ('Read the last line first. Then look at the line it names.'), which the "
        "site shows on every crash from here on. Teacher ruling: the starter is valid and the first Run is a win "
        "for a Show-me-more student (G1: a success in the first two minutes): it turns CP1 green (proven by "
        "partial 1, which is the starter). CP2 then has them break the quote on purpose, read 'unterminated', "
        "and mend it. starter_passes stays False on purpose: that field means the starter passes EVERY "
        "checkpoint (harness rule, the site's exercise-flow test, and the 'Run it and read the output' "
        "heading), and here the starter passes CP1 only. CP2 checks for exactly `Shield up!` (the "
        "`.` to `!` change proves they edited and re-ran; shows() would treat the end mark as optional, so the "
        "check is written directly). Checkpoint passes are a union across runs, so CP1 stays green while the "
        "line is broken; the deliberate crash is the point of CP2 and never blocks the exercise. A bare "
        "`\"Shield up!\"` fails CP1 in a single run (nothing printed); the site shows CP2's message, which names "
        "the missing print (proven by the check-breaker WA). Hint 1 says `Shield up.\"` (with the quote) so "
        "clicking there and pressing Backspace deletes the quote, not the period. "
        "Evidence: unclosed quotes on A-02 ('Fire Ball'), A-03 ('Fierball.'), A-04 ('Fireball'). "
        "No Assemble: the whole answer is one line. WAs: open quote (crash), starter unchanged, other quote "
        "mark, quote put back after the bracket, the period deleted instead of the quote, lower case, no print, "
        "a space lost, other words (points to Reset code)."
    ),
)

KEYBOARD_SYMBOLS = dict(
    id="keyboard-symbols",
    title="Where the symbols live",
    martu=(
        "`-` is minus, as in math. `_` is the underscore (Shift and `-`): it stands in for a space, as in "
        "`max_mana`. `=` is the equals key, but in Python it won't mean equals. More in Boxes With Labels. "
        "Top right of your keyboard:\n"
        "```text\n"
        "with Shift:   (   )   _   +\n"
        "no Shift:     9   0   -   =\n"
        "```\n"
        "`print` means show on the screen, not on paper. `#` is Shift+3."
    ),
    example='print("( ) #")\n',
    example_output="( ) #",
    starter="# Print a line that has _ and - and = in it.\n",
    names=["print"],
    pick="_ - = are side by side.",
    checkpoints=[
        dict(
            id="print-the-symbols",
            text=(
                "Show `_`, `-` and `=` on the screen, all on one line. On line 2, copy the Example's shape and "
                "put the three marks inside its quotes."
            ),
            dictated=False,
            hints=[
                "Click at the end of line 1 and press Enter. Line 1 starts with `#`, so Python skips it. "
                'Start a new line with `print("` and add the symbols after it.',
                "Quotes mean *show these exact marks*. Python shows whatever is between them, as it is: "
                '`print("( )")` shows `( )`.',
                'Type `print("_ - = are side by side.")` on line 2. Anything inside the quotes shows as it is.',
            ],
            checks=[
                ("prints something", "assert _lines(), 'Nothing shows in the Console yet. Line 1 starts with `#`, "
                 "so Python skips it. On line 2, write a `print` line with the three marks inside quotes.'"),
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
    solution='print("_ - = are side by side.")\n',
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
        dict(why="starter unchanged: only the note, nothing printed", code="# Print a line that has _ and - and = in it.\n",
             fails_at=1, message_contains="Nothing shows"),
        dict(why="symbols with no quotes", code="print(_ - =)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="leaves one symbol out", code='print("_ -")\n', fails_at=1, message_contains="missing `=`"),
        dict(why="check-breaker: each symbol on its own line, not one line with all three",
             code='print("_")\nprint("-")\nprint("=")\n', fails_at=1, message_contains="missing"),
    ],
    takeaway="`-` is minus. `_` (Shift and `-`) stands in for a space. `=` is not math's equals: its job comes "
             "in Boxes With Labels.",
    notes=(
        "meta: starter_level=S2; path=CC; contingent=show-me-more (K); skills=print-text; solo=false; "
        "dictates=; foreign_names=. G1 R30 (dash for =: A-04 `chicken_sandwich - \"Fireball`). Any line with "
        "all three symbols passes; Mar'tu's pick is the solution's line. Check-breaker: WA for one symbol per line."
    ),
)

# ---------------------------------------------------------------------------------------------
# Lesson 1A "Words in Quotes"
# ---------------------------------------------------------------------------------------------

PRESS_RUN = dict(
    id="press-run",
    title="Press Run",
    martu=(
        "In Python, *print* means show on the screen, not on paper. `print` shows text in the "
        "[[console|Console]], the box under your code where Python's answers appear. Think of a play script: "
        "your code is the script, ▶ [[run|Run]] is \"Action!\", and the Console is the stage. Guess what will "
        "show, then press Run."
    ),
    introduces=["call:print", "const:str"],
    starter='print("Hi. It is me, Mar\'tu.")\n',
    predict=dict(
        q="Before you press Run: what will this line show in the Console?",
        choices=["Hi. It is me, Mar'tu.", '"Hi. It is me, Mar\'tu."', "An error message"],
        answer=0,
        explain=(
            "`print` shows what is inside the quotes, but not the quotes. They only mark where the text starts "
            "and stops, like quotation marks in English class. Text in quotes is called a [[string]]: letters "
            "strung together like beads on a string. This course mostly says *text*."
        ),
    ),
    checkpoints=[
        dict(
            id="press-run",
            text="Press the ▶ Run button, just above your code. You should see Mar'tu's line in the Console.",
            dictated=True,
            hints=[
                "You don't need to type anything. Find the ▶ Run button, just above your code.",
                "▶ Run sends your code to Python. Python does each line, and what `print` shows appears in the "
                "Console, under your code.",
                "Press ▶ Run. Line 1 shows `Hi. It is me, Mar'tu.` in the Console: the text between the quotes "
                "of `print(\"Hi. It is me, Mar'tu.\")`.",
            ],
            checks=[
                (
                    "shows Mar'tu's line",
                    "assert \"Hi. It is me, Mar'tu.\" in _lines(), "
                    "\"Mar'tu's line is not showing in the Console. Press Reset code to get it back, then press Run.\"",
                ),
            ],
            pass_line="Mar'tu: Yes. That is me.",
        ),
    ],
    solution='print("Hi. It is me, Mar\'tu.")\n',
    starter_passes=True,
    another_way=[
        dict(
            angle="picture",
            text=(
                "```text\n"
                "your code:\n"
                'print("Hi. It is me, Mar\'tu.")\n'
                "   |  press ▶ Run\n"
                "   v\n"
                "Console:\n"
                "Hi. It is me, Mar'tu.\n"
                "```"
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text="`print` is my chalk. What is inside the quotes goes on the wall.",
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Press Run. Read the Console.",
        ),
    ],
    wrong_answers=[
        dict(why="empty editor, nothing to show", code="", fails_at=1, message_contains="Run"),
    ],
    takeaway="`print` shows the text inside the quotes in the Console, under your code. The quotes don't show.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=print-text; solo=false; dictates=1; foreign_names=; "
        "stages=P,R. Starter passes on purpose: the first press of Run is a win (G1: a success in the first "
        "two minutes)."
    ),
)

YOUR_OWN_WORDS = dict(
    id="your-own-words",
    title="Your own words",
    martu=(
        "The words inside the [[quotes]] are yours to choose. Python shows them exactly, like a quotation in "
        "English class. Change them to something Oogrish might say.\n"
        "Stuck for words? Three moves:\n"
        "1. Delete the words between the quotes. Keep both quotes.\n"
        "2. Click between the two quotes.\n"
        "3. Press the *Can't decide? Mar'tu's pick* button, under Your steps."
    ),
    example='print("Shield up.")\n',
    example_output="Shield up.",
    starter='print("Write Oogrish\'s words here")\n',
    pick="Steady, now.",
    checkpoints=[
        dict(
            id="oogrish-speaks",
            text=(
                "On line 1, change `Write Oogrish's words here` to a line Oogrish might say to calm the party. "
                "Keep both quotes and both parentheses."
            ),
            dictated=False,
            hints=[
                'Look between the two `"` on line 1. Those are the words to change. Keep the quotes and the '
                "parentheses `( )`.",
                "Quotes mean *show these exact words*. Anything between them shows in the Console: "
                '`print("Fine.")` shows `Fine.`',
                'Make line 1 `print("Steady, now. We go together.")`, or any calm words inside the quotes.',
            ],
            checks=[
                ("words are printed, not left bare", BARE_WORDS),
                (
                    "prints a line",
                    "assert _lines(), 'Nothing shows in the Console yet. Keep `print(\"...\")` and put Oogrish\\'s "
                    "words inside the quotes.'",
                ),
                (
                    "the words are in quotes",
                    "import ast as _ast\n"
                    "_quoted = [n for n in _ast.walk(_ast.parse(_source)) if isinstance(n, _ast.Call) "
                    "and getattr(n.func, 'id', '') == 'print' and any(isinstance(c, _ast.Constant) "
                    "and isinstance(c.value, str) and c.value.strip() for a in n.args for c in _ast.walk(a))]\n"
                    "assert _quoted, 'Your line shows `' + (_lines() or [''])[0] + '` with no quotes around it. "
                    "Put Oogrish\\'s words inside quotes: `print(\"...\")`.'",
                ),
                (
                    "not the placeholder",
                    "_ph = [l for l in _lines() if any(p in l.lower().replace('\\u2019', \"'\") "
                    "for p in ('words here', 'write oogrish', \"oogrish's words\", 'oogrishs words'))]\n"
                    "assert not _ph, 'Your line still says `' + (_ph or [''])[0] + '`. Delete those words, keep the "
                    "two quotes, and type a line Oogrish would say between them.'",
                ),
                (
                    "not the example's line",
                    "assert ''.join(c for c in _lines()[0].lower() if c.isalnum()) != 'shieldup', "
                    "\"That's the Example's line. Write your own words between the quotes. Can't decide? Use "
                    "Mar'tu's pick: `Steady, now.`\"",
                ),
            ],
            pass_line="Mar'tu: Hm. He would say that.",
        ),
    ],
    solution='print("Steady, now. We go together.")\n',
    assemble=dict(
        lines=['print("Steady, now.")', 'print("We go together.")'],
        distractors=["print(Steady, now.)", 'print("We go together.)', 'print("Write Oogrish\'s words here")'],
    ),
    bonus=dict(
        by="lucky",
        title="Lucky answers back",
        text=(
            "Add a second `print` line under line 1, with Lucky's reply. Then the Console shows a conversation: "
            "Oogrish first, then Lucky."
        ),
        hints=[
            "Click at the end of line 1 and press Enter. Type the new `print` line there.",
            'Lucky might say `print("Fine. But I\'m keeping track.")`',
        ],
        checks=[
            ("two lines, two speakers", "assert len(_lines()) >= 2 and _lines()[1] != _lines()[0], "
             "'The Console needs a second, different line. Add a `print` line under line 1, with Lucky\\'s "
             "own reply in quotes.'"),
        ],
        solution='print("Steady, now. We go together.")\nprint("Fine. But I\'m keeping track.")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet='dialogue_input = "Write what Mar\'tu asks here"',
        why=(
            "You've done this before, yes? In the campaign, you changed the words between the quotes in Mar'tu's "
            "dialogue line. Same move here: the quotes stay, and the words become yours."
        ),
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "```text\n"
                'print("your words")\n'
                "      ^          ^\n"
                "      |          keep this quote\n"
                "      keep this quote\n"
                "```"
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text="Oogrish talks like a calm old teacher. Short and kind. Write one line like that, inside the quotes.",
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Swap the words. Keep the quotes.",
        ),
    ],
    wrong_answers=[
        dict(why="placeholder unchanged", code='print("Write Oogrish\'s words here")\n', fails_at=1,
             message_contains="still says"),
        dict(why="copies the example's line", code='print("Shield up.")\n', fails_at=1, message_contains="example"),
        dict(why="words left on their own, with no print (a bare value)", code='"Steady, now."\n', fails_at=1,
             message_contains="no `print`"),
        dict(why="new words with no quotes", code="print(Steady, now)\n", fails_at=0, message_contains="not defined"),
        dict(why="quote never closed", code='print("Steady, now.)\n', fails_at=0, message_contains="unterminated"),
        dict(why="check-breaker: deletes only part of the placeholder", code='print("Write words here")\n', fails_at=1,
             message_contains="still says `Write words here`"),
        dict(why="check-breaker: own line added, placeholder line still printing",
             code='print("Steady, now.")\nprint("Write Oogrish\'s words here")\n', fails_at=1,
             message_contains="still says"),
        dict(why="check-breaker: the example's line with another final mark", code='print("Shield up?")\n', fails_at=1,
             message_contains="example"),
        dict(why="check-breaker: a number with no quotes still prints", code="print(42)\n", fails_at=1,
             message_contains="no quotes"),
    ],
    takeaway="The text inside the quotes is yours to choose. Python shows it exactly.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=print-text,quote-text; solo=false; dictates=; "
        "foreign_names=; echo=true. "
        "Echo spot (2.11): the site repeats the student's first printed line deadpan "
        "('*<line>.* Hm. He would say that.') through the blocklist, with the class-level teacher switch; "
        "pass_line is the privacy-safe static fallback. C3: the example check offers Mar'tu's pick inline, and "
        "the pick counts as the student's own. Any other quoted line passes (lint e). "
        "twin: text='Change the words to a line Gearshift might say.', "
        "starter='print(\"Write Gearshift's words here\")', checks=first line is not the placeholder or the "
        "example, solution='print(\"Barrier's holding.\")'. "
        "Evidence: B-02/B-03 bare values (\"Spiderman\" with no name), A-05/A-07/A-08 copying the example, "
        "A-08/B-01 unquoted text. Check-breaker pass: the placeholder is caught on any printed line and when only part of it is deleted ('Write words here'); the example check ignores capitals, spaces and marks ('Shield up?'); a new TEXT check needs quoted words in a print, because `print(42)` used to pass. Concatenation, two arguments, apostrophes and any silly line still pass."
    ),
)

CLOSE_THE_QUOTE = dict(
    id="close-the-quote",
    title="Quotes and parentheses come in pairs",
    martu=(
        "[[quotes|Quotes]] come in pairs, like quotation marks in English class. [[parentheses|Parentheses]] "
        "`( )` come in pairs too, as in math: 3 × (2 + 4). Line 1 needs a closing quote, and line 2 needs a "
        "`)`. To [[mend]] a line means to fix it, and a *slip* is a small mistake. Press Run, read the box, and "
        "mend one line at a time."
    ),
    example='print("Two quotes, two brackets.")\n',
    example_output="Two quotes, two brackets.",
    starter='print("It is not a compass)\nprint("Shield up."\n',
    pair_talk=(
        "Pair talk: read the title of the box in the Console out loud to your partner. Which line number does "
        "it give? Then each of you fixes your own code."
    ),
    checkpoints=[
        dict(
            id="mend-line-1",
            text=(
                'Mend line 1: it needs a closing `"` right after the word `compass`. Then press Run, and '
                "Python moves on to line 2."
            ),
            dictated=True,
            hints=[
                'Look at the end of line 1, right after the word `compass`. Is there a `"` to close the words?',
                'Count the `"` marks on line 1. There is only one. Quotes come in pairs, so the text never '
                "ends: Python calls that *unterminated*.",
                'Type `"` right after `compass`. Line 1 becomes `print("It is not a compass")`.',
            ],
            checks=[
                ("line 1 shows its words", shows("It is not a compass", 'Type a `"` right after `compass` on line 1, '
                                                 "and keep its words.")),
            ],
            pass_line="Lucky: Fine. It's a clock.",
        ),
        dict(
            id="mend-line-2",
            text="Mend line 2: one of its marks has no partner. Count its `(` and `)`.",
            dictated=False,
            hints=[
                "Look at the very end of line 2. Which mark opened, but never closed?",
                "Count the parentheses on line 2. A `(` opens and a `)` closes, the same as in math: (2 + 4).",
                'Type `)` at the very end of line 2. Line 2 becomes `print("Shield up.")`.',
            ],
            checks=[
                ("line 2 shows its words", shows("Shield up.", "Keep line 2, and fix it so its `(` has a partner.")),
            ],
            pass_line="Bomb Shell: Shield up.",
        ),
    ],
    solution='print("It is not a compass")\nprint("Shield up.")\n',
    partials=['print("It is not a compass")\n'],
    assemble=dict(
        lines=['print("It is not a compass")', 'print("Shield up.")'],
        distractors=['print("It is not a compass)', 'print("Shield up."', "print(''Shield up'')"],
    ),
    bonus=dict(
        by="lucky",
        title="Gearshift's nightly line",
        text=(
            "Gearshift says this every night. Add a new `print` line, under line 2, that shows `Barrier's holding.` "
            "exactly. The `'` won't break it: Python ends the text only at the same mark it opened with, `\"`. "
            "In English, an apostrophe inside a quotation is fine too."
        ),
        hints=[
            'Put `"` quotes around the words. Then the `\'` inside is only a mark, like an apostrophe in English.',
            'Type `print("Barrier\'s holding.")` under line 2. Python ends the text only at the same mark it '
            "opened with.",
        ],
        checks=[
            ("prints Gearshift's line", shows("Barrier's holding.", "Add a new `print` line under line 2, with "
                                              "Gearshift's words inside `\"` quotes.")),
        ],
        solution='print("It is not a compass")\nprint("Shield up.")\nprint("Barrier\'s holding.")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='party.move("left")',
        why=(
            "At the cabin door you wrote this line. Count the marks: two quotes around the word, "
            "two parentheses around the quotes. That is why it worked."
        ),
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Quotes are bookends. Words stand between them:\n"
                "```text\n"
                'print("It is not a compass")\n'
                "     ^^                   ^^\n"
                "   ( and \"           \" and )\n"
                "    open               close\n"
                "```\n"
                "The `(` opens first and the `)` closes last, around the quotes, like (2 + 4) in math."
            ),
        ),
        dict(
            angle="everyday",
            label="Something everyday",
            text="Shoes come in pairs. One shoe is not a pair. One quote mark is not a pair either.",
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Python finds the first quote and starts reading words.\n"
                "2. It looks for the next quote, to know where the words stop.\n"
                "3. It never comes. Python reaches the end of the line and stops: *unterminated*, which means "
                "never ended."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Line 1 needs a `\"`. Line 2 needs a `)`.",
        ),
    ],
    wrong_answers=[
        dict(why="starter unchanged: the explainer's 'unterminated' row", code='print("It is not a compass)\nprint("Shield up."\n',
             fails_at=0, message_contains="unterminated"),
        dict(why="mixed quotes: opens with \" and closes with '",
             code="print(\"It is not a compass')\nprint(\"Shield up.\")\n", fails_at=0, message_contains="unterminated"),
        dict(why="two apostrophes used as a double quote",
             code="print(\"It is not a compass\")\nprint(''Shield up'')\n", fails_at=0, message_contains="comma"),
        dict(why="line 1 mended, line 2's bracket still open",
             code='print("It is not a compass")\nprint("Shield up."\n', fails_at=0, message_contains="never closed"),
        dict(why="mends line 2 by deleting it", code='print("It is not a compass")\n', fails_at=2,
             message_contains="Shield up."),
        dict(why="check-breaker: both lines squeezed into one print",
             code='print("It is not a compass", "Shield up.")\n', fails_at=1, message_contains="line of its own"),
    ],
    takeaway="Quotes come in pairs, and parentheses come in pairs. To mend a line means to fix it.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=quote-text; solo=false; dictates=1; foreign_names=; "
        "stages=D,I. Explainer rows proven here (2.6): unterminated (starter), mixed quotes (WA), two "
        "apostrophes (WA), '(' was never closed (WA). Line 1's error shows first (verified on 3.12 and 3.13); "
        "after it is mended, the site prefixes line 2's error with 'One fixed. Python found the next one:'. "
        "Both checkpoints turn green together, because Python reads the whole file before it runs any of it. "
        "The starter is deliberately not valid Python, so the harness warns about it. "
        "Evidence: A-02 '(\"Fire Ball', A-03 '\"Fierball.', A-04 '\"Fireball', A-01 '\"Fireball\\''. "
        "Check-breaker pass: shows() names the nearest slip (words with no print, capitals, spaces or marks, a longer line, a letter or two) and accepts a curly apostrophe from tablet keyboards. WA: both lines in one print. Swapping the two lines still passes (both are mended)."
    ),
)

WORDS_NEED_QUOTES = dict(
    id="words-need-quotes",
    title="Words need quotes",
    martu=(
        "Text you want to show needs [[quotes]], like someone's exact words in English class. Without quotes, "
        "Python thinks the word is a name it should already know, and looks it up. (You'll make names like that "
        "in Boxes With Labels.) Here it finds nothing, so it stops and says *not defined*."
    ),
    example='print("Lantern")\n',
    example_output="Lantern",
    starter="print(Fireball)\n",
    names=["print"],
    predict=dict(
        q="Before you press Run: what will line 1 show in the Console?",
        choices=["Fireball", "ERROR: name 'Fireball' is not defined", "An empty line"],
        answer=1,
        explain=(
            "No quotes, so Python looked for a name `Fireball` that it should already know. Nothing has that "
            "name yet, so it says *not defined*. It isn't about spelling, and the word isn't too long."
        ),
    ),
    checkpoints=[
        dict(
            id="quote-fireball",
            text='Put a `"` on each side of `Fireball` on line 1. You should see the word `Fireball` in the Console.',
            dictated=True,
            hints=[
                "Look at `Fireball` on line 1. Does it have quotes around it?",
                "Quotes mean *show these exact letters*. Without them, Python looks for a name instead: "
                '`print("Lantern")` shows `Lantern`.',
                'Type `"` right before `Fireball` and another `"` right after it. Line 1 becomes '
                '`print("Fireball")`.',
            ],
            checks=[
                ("shows Fireball", shows("Fireball", 'Put a `"` on each side of `Fireball` on line 1.',
                                         extra_ok=(".", "!"))),
            ],
            pass_line="Mar'tu: Words in quotes. Good.",
        ),
        dict(
            id="get-inside",
            text="Make a new line 2 that shows the words `Get inside` in the Console.",
            dictated=False,
            hints=[
                "Click at the end of line 1 and press Enter to make line 2. "
                'Start a new line with `print("`.',
                "Two words still need only one pair of quotes, with the space inside: "
                '`print("Good night")` shows `Good night`.',
                'Type `print("Get inside")` on line 2.',
            ],
            checks=[
                ("words are printed, not left bare", BARE_WORDS),
                (
                    "no glued words",
                    "assert 'Getinside' not in _lines(), "
                    "'Your line shows `Getinside`. Put both words inside one pair of quotes, with the space between them.'",
                ),
                ("shows Get inside", shows("Get inside", "Make a new line 2 that shows those two words, inside "
                                           "one pair of quotes.", extra_ok=(".", "!"), starts_ok=True)),
            ],
            pass_line="Oogrish: Steady, now. Everyone inside.",
        ),
    ],
    solution='print("Fireball")\nprint("Get inside")\n',
    partials=['print("Fireball")\n'],
    assemble=dict(
        lines=['print("Fireball")', 'print("Get inside")'],
        distractors=["print(Fireball)", "print(Get inside)", 'print("Get" "inside")'],
    ),
    bonus=dict(
        by="lucky",
        title="Announce Lucky's spell",
        text="Add a line 3 that shows `Lucky's Fire Ball!` exactly, capitals and all.",
        hints=[
            "Three words, one apostrophe, one `!`. All of it goes inside one pair of `\"` quotes.",
            'Type `print("Lucky\'s Fire Ball!")` on line 3.',
        ],
        checks=[
            ("announces the spell", "assert \"Lucky's Fire Ball!\" in [l.replace('\\u2019', \"'\") for l in _lines()], "
             "'Lucky\\'s spell is not showing yet. Add a line 3 that shows `Lucky\\'s Fire Ball!`, capitals and all.'"),
        ],
        solution='print("Fireball")\nprint("Get inside")\nprint("Lucky\'s Fire Ball!")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='speak_dialogue("option 1")',
        why=(
            "The dialogue part said to keep the quotes around `\"option 1\"`. Now you know why: "
            "with quotes, Python reads those exact letters. Without them, it looks for a name."
        ),
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "What Python tries with `print(Fireball)`:\n"
                "1. No quotes, so this is not text to show.\n"
                "2. Then it must be a name Python should already know.\n"
                "3. Python looks for the name `Fireball`. Nothing has that name yet.\n"
                "4. It stops and says *not defined*."
            ),
        ),
        dict(
            angle="everyday",
            label="From English class",
            text=(
                "In English, quotes can show you mean the word itself: *'Lucky' has five letters.* Without "
                "quotes, *Lucky* means the hero. Python works the same way: quotes mean the word itself."
            ),
        ),
        dict(
            angle="contrast",
            label="This, not this",
            text=(
                "Not this: `print(Fireball)`. Python looks for a name and finds nothing.\n"
                "This: `print(\"Fireball\")`. Python shows the word."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? Names versus words",
            text=(
                "Python has two kinds of words. Words in quotes are shown exactly. Words without quotes are names: "
                "Python looks them up. `print` itself is a name with no quotes, and Python finds it. "
                "`Fireball` is a name with no quotes too, and Python finds nothing."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Show words? Use quotes.",
        ),
    ],
    wrong_answers=[
        dict(why="starter unchanged: the explainer's 1A rule 9", code="print(Fireball)\n", fails_at=0,
             message_contains="not defined"),
        dict(why="a space and no quotes", code="print(Fire ball)\n", fails_at=0, message_contains="comma"),
        dict(why="only the closing quote", code='print(Fireball")\n', fails_at=0, message_contains="unterminated"),
        dict(why="second line with no quotes (the C13 row)", code='print("Fireball")\nprint(Get inside)\n',
             fails_at=0, message_contains="comma"),
        dict(why="follows Python's comma hint instead of adding quotes", code='print("Fireball")\nprint(Get, inside)\n',
             fails_at=0, message_contains="not defined"),
        dict(why="quotes each word, so they glue together", code='print("Fireball")\nprint("Get" "inside")\n',
             fails_at=2, message_contains="one pair of quotes"),
        dict(why="words left on their own, with no print", code='print("Fireball")\n"Get inside"\n',
             fails_at=2, message_contains="no `print`"),
        dict(why="changes the capitals", code='print("fireball")\nprint("Get inside")\n', fails_at=1,
             message_contains="capitals"),
        dict(why="check-breaker: quotes added, but the spell split in two",
             code='print("Fire Ball")\nprint("Get inside")\n', fails_at=1, message_contains="space"),
        dict(why="check-breaker: quotes added, but no print (BARE)", code='"Fireball"\nprint("Get inside")\n',
             fails_at=1, message_contains="no `print`"),
        dict(why="check-breaker: both in one line", code='print("Fireball Get inside")\n', fails_at=1,
             message_contains="line of its own"),
    ],
    takeaway="Text you want to show needs quotes. Without quotes, Python looks for a name it should already know.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=quote-text; solo=false; dictates=1; foreign_names=; "
        "stages=P,D,I,M. "
        "Change from the spec, on purpose: the spec's starter has line 2 `print(Get inside)` too, but that line "
        "is a SyntaxError, and Python reports a SyntaxError anywhere before it runs any line. The student would "
        "see the comma message for line 2 while checkpoint 1 asks about line 1, and rule 9 (the Learn text's "
        "idea) would never show first. So the starter is line 1 only, rule 9 fires first, and CP2 is a "
        "non-dictated make ('Add a second line that shows the words Get inside'). The C13 row still fires on "
        "the real slip `print(Get inside)` (proven by a wrong answer). "
        "The Investigate ('Why does Python say not defined?' with its three options) is the predict step; its "
        "explanation answers all three options. Single quotes pass (not a wrong answer). "
        "Evidence: A-05 `fireball`, A-08 `kratos` / `spartin rage ...`, B-01 `fireball` (unquoted text). "
        "Check-breaker pass: shows() names the nearest slip (words with no print, capitals, spaces or marks, a longer line, a letter or two) and accepts a curly apostrophe from tablet keyboards. Loosened: `Fireball!` and `Fireball.` pass, and so does a line that starts with `Get inside` (`Get inside, yes?`). `print(\"Get\", \"inside\")` passes too (it shows the words). WAs added: `Fire Ball` in quotes (A-02), words with no print, both words on one line."
    ),
)

TOP_TO_BOTTOM = dict(
    id="top-to-bottom",
    title="Top to bottom",
    martu=(
        "Python reads your code like a page in a book: the top line first, then down, one line at a time. "
        "An empty `print()`, with nothing between the parentheses, shows an empty line in the Console."
    ),
    example='print("Line one.")\nprint()\nprint("Line three.")\n',
    example_output="Line one.\n\nLine three.",
    starter=(
        'print("Get inside, yes?")\n'
        'print("Mar\'tu checks the clock.")\n'
        'print("The hand is near the arc.")\n'
    ),
    names=["print"],
    pair_talk=(
        "Pair talk: you and your partner each say the order out loud before you run. "
        "Then each of you runs it on your own device. Who was right?"
    ),
    predict=dict(
        q="Before you press Run: what will the Console show?",
        choices=[
            "Get inside, yes?\nMar'tu checks the clock.\nThe hand is near the arc.",
            "The hand is near the arc.\nMar'tu checks the clock.\nGet inside, yes?",
            "Mar'tu checks the clock.\nThe hand is near the arc.\nGet inside, yes?",
        ],
        answer=0,
        explain=(
            "Python starts at line 1 and goes down, like reading a page. So `Get inside, yes?` shows first, "
            "but it should come last. You'll fix that next."
        ),
    ),
    checkpoints=[
        dict(
            id="warning-last",
            text='Move line 1, `print("Get inside, yes?")`, from the top of your code to the bottom.',
            dictated=True,
            hints=[
                "Move it in four moves:\n"
                "1. Drag across all of line 1 to select it.\n"
                "2. Press Ctrl+X (Cmd+X on a Mac) to cut it.\n"
                "3. Click at the end of the last line and press Enter.\n"
                "4. Press Ctrl+V (Cmd+V) to paste it there.",
                "Python runs the top line first. So the line you want to show last has to be at the bottom.",
                'Put `print("Get inside, yes?")` on the line after `print("The hand is near the arc.")`, '
                "at the bottom of your code.",
            ],
            checks=[
                (
                    "the warning still prints",
                    "assert 'Get inside, yes?' in _lines(), "
                    "'`Get inside, yes?` is not showing anymore. Keep its words exactly the same, and move its "
                    "line to the bottom of your code.'",
                ),
                (
                    "the other lines still print",
                    "assert \"Mar'tu checks the clock.\" in _lines() and 'The hand is near the arc.' in _lines(), "
                    "'A line is missing from the Console. Keep all three lines, and move only `Get inside, yes?`.'",
                ),
                (
                    "the warning prints once",
                    "assert _lines().count('Get inside, yes?') == 1, "
                    "'`Get inside, yes?` shows twice now, so it was copied. Delete the copy at the top, "
                    "so it shows once, at the bottom.'",
                ),
                (
                    "the warning comes after them",
                    "_l = _lines()\n"
                    "assert _l.index('Get inside, yes?') > _l.index(\"Mar'tu checks the clock.\") "
                    "and _l.index('Get inside, yes?') > _l.index('The hand is near the arc.'), "
                    "'`Get inside, yes?` still shows before one of the other lines. Move its whole line to the "
                    "very bottom of your code.'",
                ),
            ],
            pass_line="Mar'tu: `Get inside, yes?` comes last now. Good.",
        ),
        dict(
            id="blank-line",
            text=(
                'Make a new line right above `print("Get inside, yes?")` and type `print()` on it. You should '
                "see an empty line above `Get inside, yes?` in the Console."
            ),
            dictated=True,
            hints=[
                'Click at the very start of the line `print("Get inside, yes?")` and press Enter. That makes a '
                "new empty line right above it. Click on that empty line.",
                "`print()` with nothing between the parentheses shows an empty line. An empty line in your code "
                "shows nothing: it needs `print()` on it.",
                'Type `print()` above `print("Get inside, yes?")`.',
            ],
            checks=[
                (
                    "blank line just before the warning",
                    "import ast as _ast\n"
                    "_raw = [s.strip() for s in _captured_stdout.splitlines()]\n"
                    "_i = _raw.index('Get inside, yes?') if 'Get inside, yes?' in _raw else 0\n"
                    "_lone = [n.lineno for n in _ast.parse(_source).body if isinstance(n, _ast.Expr) "
                    "and isinstance(n.value, _ast.Name) and n.value.id == 'print']\n"
                    "assert (_i > 0 and _raw[_i - 1] == '') or not _lone, "
                    "'Line ' + str((_lone or [0])[0]) + ' says `print` with no parentheses, so it does nothing. "
                    "Write `print()`, parentheses and all.'\n"
                    "assert _i > 0 and _raw[_i - 1] == '', "
                    "'No empty line shows above `Get inside, yes?` yet. An empty line in your code shows nothing. "
                    "Type `print()` on the line right above `print(\"Get inside, yes?\")`.'",
                ),
            ],
            pass_line="Mar'tu: A breath before the warning. Better.",
        ),
    ],
    solution=(
        'print("Mar\'tu checks the clock.")\n'
        'print("The hand is near the arc.")\n'
        "print()\n"
        'print("Get inside, yes?")\n'
    ),
    partials=[
        'print("Mar\'tu checks the clock.")\n'
        'print("The hand is near the arc.")\n'
        'print("Get inside, yes?")\n'
    ],
    assemble=dict(
        lines=[
            'print("Mar\'tu checks the clock.")',
            'print("The hand is near the arc.")',
            "print()",
            'print("Get inside, yes?")',
        ],
        distractors=["print(Get inside, yes?)", "Print()"],
    ),
    bonus=dict(
        by="lucky",
        title="Lucky gets the last word",
        text="Add Lucky's reply at the bottom, under `Get inside, yes?`, with an empty line between them.",
        hints=[
            "Two more lines at the bottom: `print()`, then Lucky's words.",
            'Lucky might say `print("Fine. But I\'m keeping track.")`',
        ],
        checks=[
            (
                "blank line, then Lucky's reply",
                "_raw = [s.strip() for s in _captured_stdout.splitlines()]\n"
                "_i = _raw.index('Get inside, yes?') if 'Get inside, yes?' in _raw else len(_raw)\n"
                "assert len(_raw) > _i + 2 and _raw[_i + 1] == '' and any(_raw[_i + 2:]), "
                "'Lucky\\'s reply is not under `Get inside, yes?` yet. Add `print()` first, then a `print` line "
                "with Lucky\\'s reply.'",
            ),
        ],
        solution=(
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            "print()\n"
            'print("Get inside, yes?")\n'
            "print()\n"
            'print("Fine. But I\'m keeping track.")\n'
        ),
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Python reads your code like a page in a book, top line first:\n"
                "```text\n"
                "line 1  ->  printed first\n"
                "line 2  ->  printed second\n"
                "line 3  ->  printed last\n"
                "```"
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "The finished code, one line at a time:\n"
                "1. `print(\"Mar'tu checks the clock.\")` shows: Mar'tu checks the clock.\n"
                "2. `print(\"The hand is near the arc.\")` shows: The hand is near the arc.\n"
                "3. `print()` shows an empty line.\n"
                "4. `print(\"Get inside, yes?\")` shows: Get inside, yes?"
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Top line first. Bottom line last. `print()` is an empty line.",
        ),
    ],
    wrong_answers=[
        dict(why="the warning still first (starter unchanged)", code=(
            'print("Get inside, yes?")\n'
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
        ), fails_at=1, message_contains="still shows before"),
        dict(why="moved, but no blank line", code=(
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            'print("Get inside, yes?")\n'
        ), fails_at=2, message_contains="print()"),
        dict(why="blank line in the wrong place", code=(
            "print()\n"
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            'print("Get inside, yes?")\n'
        ), fails_at=2, message_contains="right above"),
        dict(why="deletes a line instead of moving one", code=(
            'print("The hand is near the arc.")\n'
            'print("Get inside, yes?")\n'
        ), fails_at=1, message_contains="Keep all three"),
        dict(why="check-breaker: copies the warning to the bottom instead of moving it", code=(
            'print("Get inside, yes?")\n'
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            "print()\n"
            'print("Get inside, yes?")\n'
        ), fails_at=1, message_contains="shows twice"),
        dict(why="check-breaker: an empty line in the code instead of print()", code=(
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            "\n"
            'print("Get inside, yes?")\n'
        ), fails_at=2, message_contains="empty line"),
        dict(why="check-breaker: print with no brackets does nothing", code=(
            'print("Mar\'tu checks the clock.")\n'
            'print("The hand is near the arc.")\n'
            "print\n"
            'print("Get inside, yes?")\n'
        ), fails_at=2, message_contains="no parentheses"),
    ],
    takeaway="Python reads your code like a page: top line first, then down. `print()` shows an empty line.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=print-text; solo=false; dictates=1,2; foreign_names=; "
        "stages=P,R,M; trace=static step table (another_way). "
        "PR (pair prompt): own devices, so 'Seat A predicts, Seat B runs' became predict-and-compare, each on "
        "their own device. The blank-line check reads the raw output, so `print(\"\")` and `print(\" \")` "
        "pass too. Checks stay true when Lucky's side quest adds lines after the warning. Check-breaker pass: copying the warning to the bottom (it prints twice) now fails with its own message; CP2 names an empty code line and a bare `print` with no brackets (both silently print nothing). Loosened: the side quest accepts more than one blank line before Lucky's reply."
    ),
)

NOTES_FOR_HUMANS = dict(
    id="notes-for-humans",
    title="Notes for humans",
    martu=(
        "A line that starts with the `#` sign (Shift+3) is a [[comment|note for people]]: Python skips it. It's "
        "like the stage directions in a play script: the actors read them but never say them out loud. Put `#` "
        "at the very start of a line to switch that line off: `# print(\"Hi\")` shows nothing."
    ),
    example='# This note is for humans.\nprint("Python reads this.")\n# print("Python skips this.")\n',
    example_output="Python reads this.",
    starter=(
        'print("Steady, now. Rest while you can.")\n'
        'print("I am keeping the glug.")\n'
        'print("I will take first watch.")\n'
    ),
    pick="# Night watch at the cabin.",
    checkpoints=[
        dict(
            id="switch-off-the-glug",
            text="Put `#` at the very start of line 2, before `print`. Line 2 is Lucky's secret, so it shouldn't show.",
            dictated=True,
            hints=[
                'Look at line 2, `print("I am keeping the glug.")`. Click at its very start, before the `p` of '
                "`print`.",
                "Python skips a line that starts with `#`. The line stays in your code, but nothing from it shows.",
                'Type `#` at the very start of line 2. Line 2 becomes `# print("I am keeping the glug.")`.',
            ],
            checks=[
                (
                    "the glug line is quiet",
                    "_g = [l for l in _lines() if 'keeping the glug' in l]\n"
                    "assert not any(l.startswith('#') for l in _g), "
                    "'The `#` is inside the quotes, so Python showed it. Put `#` at the very start of the line, before `print`.'\n"
                    "assert not _g, 'Lucky\\'s line, `I am keeping the glug.`, still shows. Put `#` at the very "
                    "start of that line.'",
                ),
                (
                    "the line is kept as a note",
                    NOTES + "assert any('keeping the glug' in text and 'print' in text.lower() for _, text in _notes), "
                    "'Your code no longer has the whole glug line, `print` and all. Put it back, and switch it off "
                    "with `#` at its very start.'",
                ),
                (
                    "the other lines still print",
                    "assert 'Steady, now. Rest while you can.' in _lines() and 'I will take first watch.' in _lines(), "
                    "'One of the other lines stopped showing. Switch off only the glug line: "
                    "`Steady, now. Rest while you can.` and `I will take first watch.` should still show.'",
                ),
            ],
            pass_line="Lucky: I said nothing. You heard nothing.",
        ),
        dict(
            id="your-own-note",
            text=(
                "Click at the very start of line 1 and press Enter. Then click on the new empty line 1 and type "
                "`#` and any words."
            ),
            dictated=False,
            hints=[
                'Look at the very top of your code. Your note goes on a new line 1, above `print("Steady, now. '
                'Rest while you can.")`.',
                "A note starts with `#`. After it, write anything you like.",
                'Type `# Night watch at the cabin.` above `print("Steady, now. Rest while you can.")`.',
            ],
            checks=[
                (
                    "a new note",
                    NOTES + "assert any('keeping the glug' not in text and text.strip('# ') for _, text in _notes), "
                    "'Your code has no note of your own yet. On a new line 1, type `#` and then any words.'",
                ),
            ],
            pass_line="Mar'tu: Notes for humans. Python does not mind.",
        ),
    ],
    solution=(
        "# Night watch at the cabin.\n"
        'print("Steady, now. Rest while you can.")\n'
        '# print("I am keeping the glug.")\n'
        'print("I will take first watch.")\n'
    ),
    partials=[
        'print("Steady, now. Rest while you can.")\n'
        '# print("I am keeping the glug.")\n'
        'print("I will take first watch.")\n'
    ],
    assemble=dict(
        lines=[
            "# Night watch at the cabin.",
            'print("Steady, now. Rest while you can.")',
            '# print("I am keeping the glug.")',
            'print("I will take first watch.")',
        ],
        distractors=['print("I am keeping the glug.")', 'print("# I am keeping the glug.")'],
    ),
    bonus=dict(
        by="lucky",
        title="Who says each line?",
        text=(
            "Above each `print` line that isn't switched off, add a `#` note that names the hero who says it. "
            "Any hero is fine."
        ),
        hints=[
            "Put a `#` note on the line just above each `print` line.",
            "Like this: `# Oogrish` on one line, then his `print` line under it.",
        ],
        checks=[
            (
                "a note above each printing line",
                NOTES + "_note_lines = {n for n, text in _notes if 'print(' not in text}\n"
                "_rows = _source.splitlines()\n"
                "_prints = [i + 1 for i, row in enumerate(_rows) if row.strip().startswith('print(')]\n"
                "assert _prints and all(n - 1 in _note_lines for n in _prints), "
                "'A `print` line has no note right above it. Put a `#` note with a hero\\'s name on the line "
                "just above each `print` line.'",
            ),
        ],
        solution=(
            "# Oogrish\n"
            'print("Steady, now. Rest while you can.")\n'
            '# print("I am keeping the glug.")\n'
            "# Gearshift\n"
            'print("I will take first watch.")\n'
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="# This function is already finished. You don't need to change it.",
        why=(
            "Remember the mana bars? Lines like this one started with `#`. They were notes for you, "
            "and Python skipped them. Now you can write your own."
        ),
    ),
    another_way=[
        dict(
            angle="everyday",
            label="From English class",
            text=(
                "A note in the margin of your own essay helps you, but it isn't part of the essay. A `#` note "
                "is like that: it helps the people who read your code, and Python skips it."
            ),
        ),
        dict(
            angle="picture",
            text=(
                "A `#` is a sticky note on your code:\n"
                "```text\n"
                "# Lucky, keep quiet.\n"
                "^ a note: skipped\n"
                "\n"
                "print(\"Steady, now.\")\n"
                "^ runs\n"
                "\n"
                "# print(\"I am keeping the glug.\")\n"
                "^ switched off: skipped\n"
                "```"
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this in the campaign",
            text=(
                "In the mana bars part, the code that was already there said `# Replace pass with those two lines.` "
                "That `#` line was a note for you. Python never ran it."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="`#` at the start means: skip this line.",
        ),
    ],
    wrong_answers=[
        dict(why="deletes the line instead of switching it off", code=(
            'print("Steady, now. Rest while you can.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=1, message_contains="switch it off"),
        dict(why="switches off the wrong line", code=(
            '# print("Steady, now. Rest while you can.")\n'
            'print("I am keeping the glug.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=1, message_contains="still shows"),
        dict(why="puts the # inside the quotes", code=(
            'print("Steady, now. Rest while you can.")\n'
            'print("# I am keeping the glug.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=1, message_contains="inside the quotes"),
        dict(why="no note of their own", code=(
            'print("Steady, now. Rest while you can.")\n'
            '# print("I am keeping the glug.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=2, message_contains="note"),
        dict(why="a note with no words", code=(
            "#\n"
            'print("Steady, now. Rest while you can.")\n'
            '# print("I am keeping the glug.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=2, message_contains="any words"),
        dict(why="check-breaker: swaps `print(` for `#`, so the code line is gone", code=(
            "# Night watch at the cabin.\n"
            'print("Steady, now. Rest while you can.")\n'
            "# I am keeping the glug.\n"
            'print("I will take first watch.")\n'
        ), fails_at=1, message_contains="`print` and all"),
        dict(why="check-breaker: deletes the line and writes a note about it", code=(
            "# Lucky is keeping the glug.\n"
            'print("Steady, now. Rest while you can.")\n'
            'print("I will take first watch.")\n'
        ), fails_at=1, message_contains="`print` and all"),
    ],
    takeaway="`#` (Shift+3) starts a note for people. Python skips it. Put `#` at the start of a line to switch it off.",
    notes=(
        "meta: starter_level=S4; path=SC; skills=print-text; solo=false; dictates=1; foreign_names=; "
        "stages=I,M. SC inside a CC lesson (deferrable by the teacher's switch). Notes are found with the "
        "tokenizer, so a `#` inside quotes is not a note. Any note text passes (lint e); Mar'tu's pick is the "
        "solution's note. Starter lines avoid the red-clock spoiler. Check-breaker pass: the switched-off note must still hold `print`, so deleting the line and writing a note about it, or swapping `print(` for `#`, no longer passes CP1."
    ),
)

BROKEN_SPELL_1A = dict(
    id="broken-spell-1a",
    title="Broken spell: three slips",
    martu=(
        "Three lines, three small mistakes, one on each line. Press Run. Read the title of the box, then "
        "Python's last line. Fix the line it gives, then press Run again. Python stops at the first mistake it "
        "meets, so each fixed line lets it get further."
    ),
    starter=(
        'print("Shield up.)\n'
        'Print("Barrier\'s holding.")\n'
        "print(Steady)\n"
    ),
    names=["print"],
    pair_talk=(
        "Pair talk: before you fix anything, tell your partner which line number the box gives first. "
        "Then each of you fixes your own code."
    ),
    checkpoints=[
        dict(
            id="mend-line-1",
            text="Mend line 1 so it shows `Shield up.` in the Console.",
            dictated=True,
            hints=[
                "Read the title of the box in the Console, then Python's last line. Both point at line 1: look "
                "right after `Shield up.`",
                'Count the `"` marks on line 1. Quotes come in pairs, and line 1 has only one.',
                'Type `"` right after `Shield up.` on line 1. Line 1 becomes `print("Shield up.")`.',
            ],
            checks=[
                ("line 1 shows Shield up", shows("Shield up.", 'Fix line 1: its words need a `"` on each side.')),
            ],
            pass_line="Bomb Shell: Shield up.",
        ),
        dict(
            id="mend-line-2",
            text="Mend line 2 so it shows `Barrier's holding.` in the Console.",
            dictated=True,
            hints=[
                "Read the box's title and Python's last line. Then look at the first letter of line 2.",
                "Compare the first word of line 2 with `print` on line 1. Python's words are all small letters, "
                "so `Print` and `print` are different names to Python.",
                "Change the capital `P` at the start of line 2 to a small `p`. Line 2 becomes "
                "`print(\"Barrier's holding.\")`.",
            ],
            checks=[
                ("line 2 shows Barrier's holding", shows("Barrier's holding.", "Fix line 2: `print` starts with a "
                                                         "small `p`.")),
            ],
            pass_line="Gearshift: Barrier's holding.",
        ),
        dict(
            id="mend-line-3",
            text="Mend line 3 so it shows `Steady` in the Console.",
            dictated=True,
            hints=[
                "Look at `Steady` on line 3. Does it have quotes around it?",
                "Is `Steady` a word to show, or a name Python should look up? Text to show needs quotes. "
                "Without quotes, Python looks for a name it should already know.",
                'Type `"` right before `Steady` and another `"` right after it. Line 3 becomes '
                '`print("Steady")`.',
            ],
            checks=[
                ("line 3 shows Steady", shows("Steady", "Fix line 3: put quotes around `Steady`.",
                                              extra_ok=(".", "!"))),
            ],
            pass_line="Bomb Shell: Works.",
        ),
    ],
    solution='print("Shield up.")\nprint("Barrier\'s holding.")\nprint("Steady")\n',
    partials=[
        'print("Shield up.")\n',
        'print("Shield up.")\nprint("Barrier\'s holding.")\n',
    ],
    assemble=dict(
        lines=['print("Shield up.")', 'print("Barrier\'s holding.")', 'print("Steady")'],
        distractors=['print("Shield up.)', 'Print("Barrier\'s holding.")', "print(Steady)"],
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet="print_prompt(dialogue)",
        why=(
            "`print_prompt` from Mar'tu's dialogue line is all small letters too. "
            "Python's own words are small letters, every time."
        ),
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "Each time you press Run:\n"
                "1. Read the title of the box in the Console. It says what went wrong.\n"
                "2. Read Python's last line. It says the same thing in Python's words.\n"
                "3. Find the line number and fix that line. Press Run again.\n"
                "Each fixed line shows in the Console before the next error."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Bomb Shell fixes one latch at a time. He does not rip the whole door off. "
                "One line, one run, then the next."
            ),
        ),
        dict(
            angle="shorter",
            label="Say it shorter",
            text="Line 1: a quote. Line 2: a capital. Line 3: quotes.",
        ),
    ],
    wrong_answers=[
        dict(why="starter unchanged: the unterminated row first", code=(
            'print("Shield up.)\n'
            'Print("Barrier\'s holding.")\n'
            "print(Steady)\n"
        ), fails_at=0, message_contains="unterminated"),
        dict(why="line 1 mended, `Print` still capital (explainer rule 6)", code=(
            'print("Shield up.")\n'
            'Print("Barrier\'s holding.")\n'
            'print("Steady")\n'
        ), fails_at=0, message_contains="print"),
        dict(why="misspells print", code=(
            'print("Shield up.")\n'
            'prnt("Barrier\'s holding.")\n'
            'print("Steady")\n'
        ), fails_at=0, message_contains="not defined"),
        dict(why="lower case and still no quotes", code=(
            'print("Shield up.")\n'
            'print("Barrier\'s holding.")\n'
            "print(steady)\n"
        ), fails_at=0, message_contains="not defined"),
        dict(why="opens a quote on line 3 but never closes it", code=(
            'print("Shield up.")\n'
            'print("Barrier\'s holding.")\n'
            'print("Steady)\n'
        ), fails_at=0, message_contains="unterminated"),
        dict(why="quotes added, but the capital S lost", code=(
            'print("Shield up.")\n'
            'print("Barrier\'s holding.")\n'
            'print("steady")\n'
        ), fails_at=3, message_contains="capitals"),
        dict(why="check-breaker: single quotes around words with an apostrophe", code=(
            'print("Shield up.")\n'
            "print('Barrier's holding.')\n"
            'print("Steady")\n'
        ), fails_at=0, message_contains="unterminated"),
        dict(why="check-breaker: retyped line 2 without the apostrophe", code=(
            'print("Shield up.")\n'
            'print("Barriers holding.")\n'
            'print("Steady")\n'
        ), fails_at=2, message_contains="mark"),
        dict(why="check-breaker: line 3 quoted but its print removed (BARE)", code=(
            'print("Shield up.")\n'
            'print("Barrier\'s holding.")\n'
            '"Steady"\n'
        ), fails_at=3, message_contains="no `print`"),
    ],
    takeaway="Press Run, read the box's title and Python's last line, fix that one line, and press Run again.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=quote-text,read-traceback; solo=false; dictates=1,2,3; "
        "foreign_names=. "
        "Change from the spec, on purpose: the spec lists the lines as `Print(...)`, `print(\"Shield up.)`, "
        "`print(Steady)`. Python reports a SyntaxError before it runs anything, so that order makes the "
        "student mend line 2 first, then line 1. Putting the SyntaxError line first means the messages come "
        "top to bottom (unterminated, then rule 6 `Print`, then rule 9), matching CP1, CP2, CP3, and each "
        "mended line appears in the console before the next message. All three ticks turn green on the "
        "run where the last slip is mended. The spec's WA `print(steady)` -> CP3 is a crash (NameError), so it "
        "is fails_at=0 here; the CP3 case is `print(\"steady\")` (capitals). Can be done in pairs (pair_talk); "
        "each student mends their own copy. The starter is deliberately not valid Python, so the harness warns. "
        "Check-breaker pass: shows() names the nearest slip (words with no print, capitals, spaces or marks, a longer line, a letter or two) and accepts a curly apostrophe from tablet keyboards. WAs added: single quotes around `Barrier's` (crash), the apostrophe dropped, line 3 quoted with no print."
    ),
)

SOLO_1A = dict(
    id="solo-1a",
    title="Show Mar'tu",
    martu="One line, one mistake. Find it and fix it on your own. Your turn to show off.",
    starter='print("The lantern is lit.)\n',
    solo=True,
    checkpoints=[
        dict(
            id="mend-the-lantern",
            text="Mend line 1 so it shows `The lantern is lit.` in the Console.",
            dictated=False,
            hints=[
                "Read the title of the box in the Console, then Python's last line. Then look at the line "
                "with that number.",
                'Count the `"` marks on line 1. Quotes come in pairs.',
            ],
            checks=[
                ("shows the lantern line", shows("The lantern is lit.", "Fix line 1 so it shows its words.")),
            ],
            pass_line="Mar'tu: You did that on your own. Every quote has its partner.",
        ),
    ],
    solution='print("The lantern is lit.")\n',
    wrong_answers=[
        dict(why="starter unchanged", code='print("The lantern is lit.)\n', fails_at=0, message_contains="unterminated"),
        dict(why="closes with the other quote mark", code="print(\"The lantern is lit.')\n", fails_at=0,
             message_contains="unterminated"),
        dict(why="removes the quote instead of closing it", code="print(The lantern is lit.)\n", fails_at=0,
             message_contains="comma"),
        dict(why="retypes it in lower case", code='print("the lantern is lit.")\n', fails_at=1,
             message_contains="capitals"),
        dict(why="check-breaker: quote closed but print removed (BARE)", code='"The lantern is lit."\n', fails_at=1,
             message_contains="no `print`"),
        dict(why="check-breaker: retyped with a spelling slip", code='print("The lanturn is lit.")\n', fails_at=1,
             message_contains="letter by letter"),
    ],
    takeaway="You can find and fix a missing quote on your own.",
    notes=(
        "meta: starter_level=S4; path=CC; skills=quote-text,read-traceback; solo=true; dictates=; "
        "foreign_names=; one-bug SOLO (C6). Two hints only (schema minimum); using one records the pass "
        "'with structure'. No Assemble or another_way, on purpose: this one is theirs. "
        "Seat B variant for when pair mode ships: starter `print(The lantern is lit)` (no quotes, C13 row), "
        "same check. Every student has their own device, so everyone gets seat A's starter. Check-breaker pass: shows() names the nearest slip (words with no print, capitals, spaces or marks, a longer line, a letter or two) and accepts a curly apostrophe from tablet keyboards."
    ),
)

ITEMS = [
    HOW_MARTU_TEACHES,
    dict(
        kind="lesson",
        id="before-the-first-spell",
        title="Before the First Spell",
        minutes=4,
        summary="Two warm-ups: what an error looks like, and where the symbols live on the keyboard.",
        exercises=[WHAT_AN_ERROR_LOOKS_LIKE, KEYBOARD_SYMBOLS],
        notes=(
            "1W: contingent (K), on under 'Show me more', off under 'Keep it short' and instructions-light. "
            "In the prototype it is an ordinary lesson (curriculum section 7 note). A warm-up, so it has no "
            "SOLO item (lint g applies to 1A)."
        ),
    ),
    dict(
        kind="lesson",
        id="words-in-quotes",
        title="Words in Quotes",
        minutes=19,
        summary="Show text with print, close every quote and parenthesis, read the error box, and switch lines off with #.",
        exercises=[
            PRESS_RUN,
            YOUR_OWN_WORDS,
            CLOSE_THE_QUOTE,
            WORDS_NEED_QUOTES,
            TOP_TO_BOTTOM,
            NOTES_FOR_HUMANS,
            BROKEN_SPELL_1A,
            SOLO_1A,
        ],
        notes=(
            "1A: CC (1A-06 is SC). No warm-up item (first lesson); the preset question already happened on the "
            "course map. 1A-07 (triple quotes) is in the 1X-AB pool (u01b). Non-dictated checkpoints: 1A-02, "
            "1A-03 CP2, 1A-04 CP2, 1A-06 CP2, 1A-S. One SOLO: solo-1a."
        ),
    ),
]
