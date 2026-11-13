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
        term="string",
        aliases=["strings", "text"],
        plain="Words inside quotes. Python shows them exactly as you typed them.",
        example='"Shield up."',
    ),
    dict(
        term="quotes",
        aliases=["quote", "quote mark", "quote marks"],
        plain="The marks around words: `\"` or `'`. They come in pairs, one before the words and one after.",
        example='"Steady, now."',
    ),
    dict(
        term="brackets",
        aliases=["bracket"],
        plain="The marks `(` and `)`. They come in pairs too. `print` keeps what it shows between them.",
        example='print("Hi")',
    ),
    dict(
        term="print",
        aliases=["print()"],
        plain="The Python command that shows words on the screen, in the console.",
        example='print("Barrier\'s holding.")',
    ),
    dict(
        term="run",
        aliases=["runs", "Run button"],
        plain="Tell Python to do your lines, from top to bottom. Press Run as often as you like. It costs nothing.",
    ),
    dict(
        term="console",
        aliases=["the console"],
        plain="The space under the editor. Your printed lines and Python's messages show up there.",
    ),
    dict(
        term="error message",
        aliases=["error messages", "message from Python"],
        plain="Python's note that it could not finish your code. It is information, not a mark. "
        "Read the last line first, then look at the line it names.",
        example="SyntaxError: unterminated string literal",
    ),
    dict(
        term="comment",
        aliases=["comments"],
        plain="A line that starts with `#`. Python skips it. It is a note for people.",
        example="# Lucky's lines for tonight",
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
    "assert not _bare, 'Line %d is words with no `print`, so Python made them and forgot them. "
    "Write `print(` before them and `)` after.' % (_bare[0] if _bare else 0)"
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
    head = "The task needs `" + text + "`, and your line shows `"
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
        "        _msg = ('Line ' + str(_bare[0]) + ' has the words in quotes, but no `print`, so Python made them '\n"
        "                'and forgot them. Write `print(` before the quotes and `)` after.')\n"
        "    elif _l and _fix(_l).lower().rstrip('.!?') == _want[0].lower() and _fix(_l).rstrip('.!?') != _want[0]:\n"
        f"        _msg = {head!r} + _l + '`. Capitals count: Python shows exactly what is inside the quotes.'\n"
        "    elif _l and _key(_l) == _key(_want[0]):\n"
        f"        _msg = {head!r} + _l + '`. Spaces, marks and capitals all count: Python shows exactly what is inside the quotes.'\n"
        "    elif _longer:\n"
        f"        _msg = 'Your line shows `' + _longer[0] + {longer!r}\n"
        "    elif _l and _sim(_l) >= 0.75:\n"
        f"        _msg = {head!r} + _l + '`. Check it letter by letter: Python shows exactly what is inside the quotes.'\n"
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
    summary="One minute: how Run, Help and the checkpoints work.",
    body=(
        "Write a line. Press [[run|Run]]. Python answers below.\n"
        "Pressing Run on unfinished code is allowed and costs nothing. "
        "A message from Python is information, not a mark.\n"
        "Stuck? Press Help. You can always ask for a starting line or more structure.\n"
        "Checkpoints: ✓ done · ● now · ○ next.\n"
        "Nothing here is timed. Your hints are private."
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
        "Press Run first. Then you will break it on purpose and read Python's [[error message|message]]. "
        "A message is not a mark against you: it says what Python could not read. "
        "Read the last line first. Then look at the line it names."
    ),
    introduces=["call:print", "const:str"],
    starter='print("Shield up.")\n',
    checkpoints=[
        dict(
            id="press-run",
            text="Press Run.",
            dictated=True,
            hints=[
                "You don't need to type anything. Just press Run.",
                "Run is the button above the editor.",
                'Run sends your line to Python. What `print` holds appears below: `print("Fine.")` shows `Fine.`',
            ],
            checks=[
                ("shows a line", "assert _lines(), 'Press Run to see the line.'"),
            ],
            pass_line="Mar'tu: Shield up. Now we break it, on purpose. That is safe, yes?",
        ),
        dict(
            id="close-the-quote",
            text=(
                'Break it on purpose: delete the last `"` and Run. Read the last line of Python\'s message. '
                'Then put the `"` back, change the `.` to `!`, and Run.'
            ),
            dictated=True,
            hints=[
                'Click just after `Shield up."` and press Backspace once. Then Run.',
                "*Unterminated* means the words never ended: the closing quote is missing. "
                "Put it back after the words.",
                'Quotes come in pairs. `print("Fine.")` has one `"` before the words and one after.',
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
                    "        _msg = ('Line ' + str(_bare[0]) + ' has the words in quotes, but no `print`, so Python '\n"
                    "                'made them and forgot them. Write `print(` before the quotes and `)` after.')\n"
                    "    elif 'Shield up.' in _l:\n"
                    "        _msg = ('Your line still shows `Shield up.`, with a `.` at the end. Break it on purpose '\n"
                    "                'first: delete the last `\"` and Run, and read the last line of the message. '\n"
                    "                'Then put the `\"` back, change the `.` to `!`, and Run.')\n"
                    "    elif _near and _near[0].rstrip('.!?') != 'Shield up' and _near[0].rstrip('.!?').lower() == 'shield up':\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. Capitals count: Python shows exactly what is '\n"
                    "                'inside the quotes. Make it `Shield up!`, with a capital S.')\n"
                    "    elif _near and _near[0].rstrip('.!?') == 'Shield up':\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. The task needs `!` at the end: '\n"
                    "                'make it `Shield up!`, then Run.')\n"
                    "    elif _near:\n"
                    "        _msg = ('Your line shows `' + _near[0] + '`. Spaces, marks and capitals all count: '\n"
                    "                'make it `Shield up!`, then Run.')\n"
                    "    else:\n"
                    "        _msg = ('`Shield up!` is not showing yet. Keep the line `print(\"Shield up.\")`, '\n"
                    "                'change the `.` to `!`, and Run.')\n"
                    "assert not _msg, _msg",
                ),
            ],
            pass_line="Mar'tu: You read the message. Good. That is the whole trick.",
        ),
    ],
    solution='print("Shield up!")\n',
    partials=['print("Shield up.")\n'],
    another_way=[
        dict(
            angle="picture",
            text=(
                "Two places to look. Read 1 first, then 2.\n"
                "```text\n"
                '  File "main.py", line 1     <- 2. this line\n'
                '    print("Shield up.)\n'
                "          ^\n"
                "SyntaxError: unterminated string literal     <- 1. first\n"
                "```\n"
                "Unterminated means the words never ended: the closing quote is missing."
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
            text='Delete the last `"`. Run. Read. Put the `"` back, make the `.` a `!`, and Run.',
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
    ],
    takeaway="Read the last line of Python's message first. Then look at the line it names.",
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
        "a space lost."
    ),
)

KEYBOARD_SYMBOLS = dict(
    id="keyboard-symbols",
    title="Where the symbols live",
    martu=(
        "Look at the top right of your keyboard:\n"
        "```text\n"
        "with Shift:   (   )   _   +\n"
        "no Shift:     9   0   -   =\n"
        "```\n"
        "`-`, `_` and `=` sit side by side. They mean different things. "
        "`-` subtracts, `_` joins words in a name, `=` puts a value in a box."
    ),
    example='print("( ) #")\n',
    example_output="( ) #",
    starter="# Print a line that has _ and - and = in it.\n",
    names=["print"],
    pick="_ - = are side by side.",
    checkpoints=[
        dict(
            id="print-the-symbols",
            text="Print a line that has `_`, `-` and `=` in it.",
            dictated=False,
            hints=[
                'Start a new line with `print("` and add the symbols after it.',
                "Put the symbols inside quotes, so Python shows them as they are.",
                'Anything inside quotes is shown as it is: `print("( )")` shows `( )`.',
            ],
            checks=[
                ("prints something", "assert _lines(), 'Nothing printed yet. Write a `print` line with the symbols inside quotes.'"),
                (
                    "one line has all three symbols",
                    "_best = max(_lines(), key=lambda line: sum(s in line for s in '_-='))\n"
                    "_missing = [s for s in '_-=' if s not in _best]\n"
                    "assert not _missing, 'Your line is missing ' + ' and '.join('`' + s + '`' for s in _missing) "
                    "+ '. Put all three inside one pair of quotes, in one `print` line.'",
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
                '4. `"` is Shift with the `\'` key, next to Enter.'
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
             fails_at=1, message_contains="Nothing printed"),
        dict(why="symbols with no quotes", code="print(_ - =)\n", fails_at=0, message_contains="invalid syntax"),
        dict(why="leaves one symbol out", code='print("_ -")\n', fails_at=1, message_contains="missing `=`"),
        dict(why="check-breaker: each symbol on its own line, not one line with all three",
             code='print("_")\nprint("-")\nprint("=")\n', fails_at=1, message_contains="missing"),
    ],
    takeaway="`-` subtracts, `_` joins words in a name, `=` puts a value in a box.",
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
        "Python reads your instructions and does them. `print` shows words on the screen. "
        "Guess what the [[console]] will show, then press [[run|Run]]."
    ),
    introduces=["call:print", "const:str"],
    starter='print("Hi. It is me, Mar\'tu.")\n',
    predict=dict(
        q="What will this print?",
        choices=["Hi. It is me, Mar'tu.", '"Hi. It is me, Mar\'tu."', "An error message"],
        answer=0,
        explain=(
            "`print` shows the words inside the quotes. The quotes stay in the code; "
            "they only mark where the words start and stop. Words in quotes are called a [[string]]."
        ),
    ),
    checkpoints=[
        dict(
            id="press-run",
            text="Press Run.",
            dictated=True,
            hints=[
                "You don't need to type anything. Just press Run.",
                "Run is the button above the editor.",
                'Run sends your lines to Python. What `print` holds appears below: `print("Fine.")` shows `Fine.`',
            ],
            checks=[
                (
                    "shows Mar'tu's line",
                    "assert \"Hi. It is me, Mar'tu.\" in _lines(), "
                    "'Press Run to see the line. If the editor is empty, press Reset code to get the line back.'",
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
                'editor:    print("Hi. It is me, Mar\'tu.")\n'
                "               |  press Run\n"
                "               v\n"
                "console:   Hi. It is me, Mar'tu.\n"
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
            text="Press Run. Read below.",
        ),
    ],
    wrong_answers=[
        dict(why="empty editor, nothing to show", code="", fails_at=1, message_contains="Run"),
    ],
    takeaway="`print` shows the words inside the quotes in the console.",
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
        "The words inside the [[quotes]] are yours. Python shows them exactly. "
        "Change them to something Oogrish might say. Stuck for words? Press Mar'tu's pick."
    ),
    example='print("Shield up.")\n',
    example_output="Shield up.",
    starter='print("Write Oogrish\'s words here")\n',
    pick="Steady, now.",
    checkpoints=[
        dict(
            id="oogrish-speaks",
            text="Change the words to a line Oogrish might say to calm the party.",
            dictated=False,
            hints=[
                "Delete the words between the two quotes. Keep the quotes and the brackets.",
                "Change only the words between the quotes.",
                'Any words work, as long as they sit inside the quotes: `print("Fine.")` shows `Fine.`',
            ],
            checks=[
                ("words are printed, not left bare", BARE_WORDS),
                (
                    "prints a line",
                    "assert _lines(), 'Nothing printed yet. Keep `print(\"...\")` and put the words inside the quotes.'",
                ),
                (
                    "the words are in quotes",
                    "import ast as _ast\n"
                    "_quoted = [n for n in _ast.walk(_ast.parse(_source)) if isinstance(n, _ast.Call) "
                    "and getattr(n.func, 'id', '') == 'print' and any(isinstance(c, _ast.Constant) "
                    "and isinstance(c.value, str) and c.value.strip() for a in n.args for c in _ast.walk(a))]\n"
                    "assert _quoted, 'Your line shows `' + (_lines() or [''])[0] + '`, but with no quotes. "
                    "Oogrish\\'s words go inside quotes: `print(\"...\")`.'",
                ),
                (
                    "not the placeholder",
                    "_ph = [l for l in _lines() if any(p in l.lower().replace('\\u2019', \"'\") "
                    "for p in ('words here', 'write oogrish', \"oogrish's words\", 'oogrishs words'))]\n"
                    "assert not _ph, 'Your line `' + (_ph or [''])[0] + '` still has the starter\\'s words. "
                    "Change the words between the quotes to something Oogrish would say.'",
                ),
                (
                    "not the example's line",
                    "assert ''.join(c for c in _lines()[0].lower() if c.isalnum()) != 'shieldup', "
                    "\"That's the example's line, so write your own words, or use Mar'tu's pick: `Steady, now.`\"",
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
        title="What's in it for me?",
        text=(
            "Print Lucky's reply on the next line, so the two read like a conversation. "
            "Two `print` lines: Oogrish first, then Lucky."
        ),
        hints=[
            "Add a second `print` line under the first one.",
            'Lucky might say `print("Fine. But I\'m keeping track.")`',
        ],
        checks=[
            ("two lines, two speakers", "assert len(_lines()) >= 2 and _lines()[1] != _lines()[0], "
             "'Add a second `print` line under Oogrish\\'s, with Lucky\\'s reply.'"),
        ],
        solution='print("Steady, now. We go together.")\nprint("Fine. But I\'m keeping track.")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet='dialogue_input = "Write what Mar\'tu asks here"',
        why=(
            "You have done this before, yes? In Mar'tu's dialogue line you changed the words between the quotes. "
            "Same move here: the quotes stay, the words become yours."
        ),
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "```text\n"
                'print("  your words go here  ")\n'
                "      ^                    ^\n"
                "   keep this quote    keep this quote\n"
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
             message_contains="Change"),
        dict(why="copies the example's line", code='print("Shield up.")\n', fails_at=1, message_contains="example"),
        dict(why="words left on their own, with no print (a bare value)", code='"Steady, now."\n', fails_at=1,
             message_contains="no `print`"),
        dict(why="new words with no quotes", code="print(Steady, now)\n", fails_at=0, message_contains="not defined"),
        dict(why="quote never closed", code='print("Steady, now.)\n', fails_at=0, message_contains="unterminated"),
        dict(why="check-breaker: deletes only part of the placeholder", code='print("Write words here")\n', fails_at=1,
             message_contains="starter's words"),
        dict(why="check-breaker: own line added, placeholder line still printing",
             code='print("Steady, now.")\nprint("Write Oogrish\'s words here")\n', fails_at=1,
             message_contains="starter's words"),
        dict(why="check-breaker: the example's line with another final mark", code='print("Shield up?")\n', fails_at=1,
             message_contains="example"),
        dict(why="check-breaker: a number with no quotes still prints", code="print(42)\n", fails_at=1,
             message_contains="no quotes"),
    ],
    takeaway="The words inside the quotes are yours. Python shows them exactly.",
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
    title="Quotes and brackets come in pairs",
    martu=(
        "[[quotes|Quotes]] come in pairs: one before the words, one after. [[brackets|Brackets]] come in pairs too. "
        "This line is missing one. Run it, read the message, then mend it."
    ),
    example='print("Two quotes, two brackets.")\n',
    example_output="Two quotes, two brackets.",
    starter='print("It is not a compass)\nprint("Shield up."\n',
    pair_talk=(
        "Pair talk: read Python's message out loud to your partner. Which line does it name? "
        "Then each of you mends your own code."
    ),
    checkpoints=[
        dict(
            id="mend-line-1",
            text="Mend line 1 so it runs.",
            dictated=True,
            hints=[
                "Put your cursor right after the word `compass` on line 1.",
                "Count the quote marks on line 1. How many are there?",
                'Each mark that opens needs one that closes: `print("Hi")` has two quotes and two brackets.',
            ],
            checks=[
                ("line 1 shows its words", shows("It is not a compass", "Mend line 1 by closing its quote, and keep its words.")),
            ],
            pass_line="Lucky: Fine. It's a clock.",
        ),
        dict(
            id="mend-line-2",
            text="Line 2 is missing something too. Mend it.",
            dictated=False,
            hints=[
                "Go to the very end of line 2.",
                "Count the brackets on line 2.",
                'A `(` opens and a `)` closes: `print("Go.")` has one of each.',
            ],
            checks=[
                ("line 2 shows its words", shows("Shield up.", "Keep line 2 and mend it so it shows its words.")),
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
        title="What's in it for me?",
        text=(
            "Gearshift says this every night. Print `Barrier's holding.` exactly, on a new line. "
            "Why does the `'` inside the `\"` quotes not break anything?"
        ),
        hints=[
            'Use `"` quotes around the words, so the `\'` is just a letter.',
            'Python only looks for the same mark it opened with: `print("It\'s late.")` works.',
        ],
        checks=[
            ("prints Gearshift's line", shows("Barrier's holding.", "Add a new `print` line with Gearshift's words, "
                                              "inside `\"` quotes.")),
        ],
        solution='print("It is not a compass")\nprint("Shield up.")\nprint("Barrier\'s holding.")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='party.move("left")',
        why=(
            "At the cabin door you wrote this line. Count the marks: two quotes around the word, "
            "two brackets around the quotes. That is why it worked."
        ),
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "Quotes are bookends. Words stand between them:\n"
                "```text\n"
                'print(  "  It is not a compass  "  )\n'
                "      |  |                     |  |\n"
                "      (  open quote   close quote  )\n"
                "```"
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
                "3. It never comes. Python reaches the end of the line and stops: *unterminated*."
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
    takeaway="Quotes come in pairs, and brackets come in pairs.",
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
        "Words you want to show need [[quotes]]. Without quotes, Python thinks you mean the name of something "
        "saved earlier, and it finds nothing."
    ),
    example='print("Lantern")\n',
    example_output="Lantern",
    starter="print(Fireball)\n",
    names=["print"],
    predict=dict(
        q="What will this print?",
        choices=["Fireball", "ERROR: name 'Fireball' is not defined", "An empty line"],
        answer=1,
        explain=(
            "No quotes, so Python looked for something saved earlier called `Fireball`. It found nothing, "
            "so it says *not defined*. It is not about spelling, and the word is not too long."
        ),
    ),
    checkpoints=[
        dict(
            id="quote-fireball",
            text="Make line 1 show the word `Fireball`.",
            dictated=True,
            hints=[
                'Put a `"` just before `Fireball` and another just after it.',
                "Which word do you want to see on the screen? It needs quotes.",
                "Words you want to show need quotes. Without quotes, Python looks for something saved earlier "
                'with that name. `print("Lantern")` shows `Lantern`.',
            ],
            checks=[
                ("shows Fireball", shows("Fireball", "Put quotes around it on line 1.", extra_ok=(".", "!"))),
            ],
            pass_line="Mar'tu: Words in quotes. Good.",
        ),
        dict(
            id="get-inside",
            text="Add a second line that shows the words `Get inside`.",
            dictated=False,
            hints=[
                'Start a new line with `print("`.',
                "Both words go inside one pair of quotes.",
                'Two words still need just one pair of quotes: `print("Good night")` shows `Good night`.',
            ],
            checks=[
                ("words are printed, not left bare", BARE_WORDS),
                (
                    "no glued words",
                    "assert 'Getinside' not in _lines(), "
                    "'Your line shows `Getinside`. Put both words inside one pair of quotes, with the space between them.'",
                ),
                ("shows Get inside", shows("Get inside", "Add a new line under line 1 that shows them.", extra_ok=(".", "!"),
                                           starts_ok=True)),
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
        title="What's in it for me?",
        text="Announce Lucky's spell exactly: `Lucky's Fire Ball!`",
        hints=[
            "Three words, one apostrophe, one `!`. All of it goes inside one pair of `\"` quotes.",
            'Like this shape: `print("Bob\'s Big Day!")`',
        ],
        checks=[
            ("announces the spell", "assert \"Lucky's Fire Ball!\" in [l.replace('\\u2019', \"'\") for l in _lines()], "
             "'Print it exactly, capitals and all: Lucky\\'s Fire Ball!'"),
        ],
        solution='print("Fireball")\nprint("Get inside")\nprint("Lucky\'s Fire Ball!")\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='speak_dialogue("option 1")',
        why=(
            "The dialogue part said to keep the quotes around `\"option 1\"`. Now you know why: "
            "with quotes, Python reads words. Without them, it looks for a name."
        ),
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "What Python tries with `print(Fireball)`:\n"
                "1. No quotes, so this is not words.\n"
                "2. Then it must be the name of something saved earlier.\n"
                "3. Python looks for `Fireball`. Nothing is saved with that name.\n"
                "4. It stops and says *not defined*."
            ),
        ),
        dict(
            angle="everyday",
            label="Something everyday",
            text=(
                "\"Say Lucky\" means call Lucky over. \"Say 'Lucky'\" means say the word. "
                "Quotes turn a name into words."
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
    takeaway="Words you want to show need quotes. Without quotes, Python looks for a saved name.",
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
    martu="Python runs your lines from top to bottom, one at a time. An empty `print()` shows a blank line.",
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
        q="What will this print?",
        choices=[
            "Get inside, yes?\nMar'tu checks the clock.\nThe hand is near the arc.",
            "The hand is near the arc.\nMar'tu checks the clock.\nGet inside, yes?",
            "Mar'tu checks the clock.\nThe hand is near the arc.\nGet inside, yes?",
        ],
        answer=0,
        explain=(
            "Python starts at line 1 and goes down. So the warning comes first, even though it should "
            "come last. You will fix that next."
        ),
    ),
    checkpoints=[
        dict(
            id="warning-last",
            text="Move the line `Get inside, yes?` so it prints last.",
            dictated=True,
            hints=[
                "Select the whole first line, `print(\"Get inside, yes?\")`, and cut it.",
                "Which line runs first? The one at the top.",
                "Line 1 runs, then line 2, then line 3. The line at the bottom prints last: "
                '`print("A")` then `print("B")` shows A, then B.',
            ],
            checks=[
                (
                    "the warning still prints",
                    "assert 'Get inside, yes?' in _lines(), "
                    "'I can\\'t find the line `Get inside, yes?`. Keep its words the same and move it to the end.'",
                ),
                (
                    "the other lines still print",
                    "assert \"Mar'tu checks the clock.\" in _lines() and 'The hand is near the arc.' in _lines(), "
                    "'Keep all three lines. Only move `Get inside, yes?`.'",
                ),
                (
                    "the warning prints once",
                    "assert _lines().count('Get inside, yes?') == 1, "
                    "'`Get inside, yes?` prints twice now. Move the line instead of copying it: "
                    "take it away from the top, so it prints once, at the end.'",
                ),
                (
                    "the warning comes after them",
                    "_l = _lines()\n"
                    "assert _l.index('Get inside, yes?') > _l.index(\"Mar'tu checks the clock.\") "
                    "and _l.index('Get inside, yes?') > _l.index('The hand is near the arc.'), "
                    "'`Get inside, yes?` still prints first. Move its whole line to the bottom.'",
                ),
            ],
            pass_line="Mar'tu: The warning comes last, yes? Good.",
        ),
        dict(
            id="blank-line",
            text="Add `print()` just before it, for a blank line.",
            dictated=True,
            hints=[
                "Click at the start of the `Get inside, yes?` line and press Enter.",
                "Where should the blank line go? Right above the warning.",
                "`print()` with nothing inside shows an empty line.",
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
                    "'Line ' + str((_lone or [0])[0]) + ' says `print` with no brackets, so it does nothing. "
                    "Write `print()`, brackets and all.'\n"
                    "assert _i > 0 and _raw[_i - 1] == '', "
                    "'No blank line shows just above the warning yet. An empty line in your code shows nothing: "
                    "write `print()` on the line just above the warning.'",
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
        title="What's in it for me?",
        text="Add Lucky's reply after the warning, with a blank line between.",
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
                "'After the warning: `print()` first, then a `print` line with Lucky\\'s reply.'",
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
                "Read the code like a ladder, top rung first:\n"
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
                "```text\n"
                "line  code                               the console now shows\n"
                "1     print(\"Mar'tu checks the clock.\")   Mar'tu checks the clock.\n"
                "2     print(\"The hand is near the arc.\")  The hand is near the arc.\n"
                "3     print()                            (an empty line)\n"
                "4     print(\"Get inside, yes?\")           Get inside, yes?\n"
                "```"
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
        ), fails_at=1, message_contains="still prints first"),
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
        ), fails_at=2, message_contains="just above"),
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
        ), fails_at=1, message_contains="prints twice"),
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
        ), fails_at=2, message_contains="no brackets"),
    ],
    takeaway="Python runs lines from top to bottom. `print()` shows a blank line.",
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
        "A line that starts with `#` is a [[comment|note for humans]]. Python skips it. "
        "Put `#` in front of a line to switch it off."
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
            text="Line 2 is Lucky's secret. Put `#` at the very start of line 2.",
            dictated=True,
            hints=[
                "Click at the very start of line 2.",
                "Line 2 is the one about his canteen.",
                'Python skips a line that starts with `#`. So `# print("Hi")` shows nothing.',
            ],
            checks=[
                (
                    "the glug line is quiet",
                    "_g = [l for l in _lines() if 'keeping the glug' in l]\n"
                    "assert not any(l.startswith('#') for l in _g), "
                    "'The `#` is inside the quotes, so Python showed it. Put `#` at the very start of the line, before `print`.'\n"
                    "assert not _g, 'Lucky\\'s glug line still prints. Put `#` at the very start of that line.'",
                ),
                (
                    "the line is kept as a note",
                    NOTES + "assert any('keeping the glug' in text and 'print' in text.lower() for _, text in _notes), "
                    "'Keep the whole glug line in your code, `print` and all, and switch it off with `#` at the "
                    "very start.'",
                ),
                (
                    "the other lines still print",
                    "assert 'Steady, now. Rest while you can.' in _lines() and 'I will take first watch.' in _lines(), "
                    "'Only switch off the glug line. The other two lines should still print.'",
                ),
            ],
            pass_line="Lucky: I said nothing. You heard nothing.",
        ),
        dict(
            id="your-own-note",
            text="Add a note of your own above the code.",
            dictated=False,
            hints=[
                "Make a new first line that starts with `#`.",
                "A note starts with `#`. After it, write anything you like.",
                "`# The cabin, at night` is a note. Python skips it, and the code runs the same.",
            ],
            checks=[
                (
                    "a new note",
                    NOTES + "assert any('keeping the glug' not in text and text.strip('# ') for _, text in _notes), "
                    "'Add a note of your own: a new line that starts with `#`, then any words.'",
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
        title="What's in it for me?",
        text="Above each line that prints, write a note that says which hero speaks it.",
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
                "'Put a `#` note on the line just above each `print` line.'",
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
            label="Something everyday",
            text=(
                "A play script has stage directions, like *(Lucky hides the canteen)*. The actors don't say "
                "them out loud. A `#` line is a stage direction for Python: it reads past it."
            ),
        ),
        dict(
            angle="picture",
            text=(
                "A `#` is a sticky note on your code:\n"
                "```text\n"
                "# Lucky, keep quiet.                 <- note: skipped\n"
                "print(\"Steady, now.\")                <- runs\n"
                "# print(\"I am keeping the glug.\")    <- switched off: skipped\n"
                "```"
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this in the campaign",
            text=(
                "In the mana bars part, the starter said `# Replace pass with those two lines.` "
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
        ), fails_at=1, message_contains="still prints"),
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
    takeaway="`#` starts a note for humans. Python skips it. Put `#` in front of a line to switch it off.",
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
    martu="Three lines. Three small slips. Run, read the message, mend one line, run again.",
    starter=(
        'print("Shield up.)\n'
        'Print("Barrier\'s holding.")\n'
        "print(Steady)\n"
    ),
    names=["print"],
    pair_talk=(
        "Pair talk: before you mend anything, tell your partner which line Python names first. "
        "Then each of you mends your own code."
    ),
    checkpoints=[
        dict(
            id="mend-line-1",
            text="Mend line 1 so it shows `Shield up.`",
            dictated=True,
            hints=[
                "Put your cursor right after `Shield up.` on line 1.",
                "Line 1. Count its quote marks.",
                'Quotes come in pairs: `print("Go.")` has one before the words and one after.',
            ],
            checks=[
                ("line 1 shows Shield up", shows("Shield up.", "Mend line 1 so it prints.")),
            ],
            pass_line="Bomb Shell: Shield up.",
        ),
        dict(
            id="mend-line-2",
            text="Mend line 2 so it shows `Barrier's holding.`",
            dictated=True,
            hints=[
                "Look at the first letter of line 2.",
                "Line 2. Compare its first word with `print` on line 1.",
                "Python's commands are lower case. `Print` and `print` are different names to Python.",
            ],
            checks=[
                ("line 2 shows Barrier's holding", shows("Barrier's holding.", "Mend line 2 so it prints.")),
            ],
            pass_line="Gearshift: Barrier's holding.",
        ),
        dict(
            id="mend-line-3",
            text="Mend line 3 so it shows `Steady`.",
            dictated=True,
            hints=[
                'Put a `"` just before `Steady` and another just after it.',
                "Line 3. Is `Steady` a word to show, or a name Python should look up?",
                "Words you want to show need quotes. Without quotes, Python looks for something saved earlier "
                "with that name.",
            ],
            checks=[
                ("line 3 shows Steady", shows("Steady", "Mend line 3 so it prints.", extra_ok=(".", "!"))),
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
            "`print_prompt` from Mar'tu's dialogue line is all lower case too. "
            "Python's commands are lower case, every time."
        ),
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "Each time you run:\n"
                "1. Read the last line of Python's message first.\n"
                "2. Then look at the line it names.\n"
                "3. Mend that one line. Run again.\n"
                "Each mended line shows up in the console before the next message."
            ),
        ),
        dict(
            angle="in Tor",
            label="In Tor",
            text=(
                "Bomb Shell mends one latch at a time. He does not rip the whole door off. "
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
    takeaway="Run, read the last line first, mend one line, run again.",
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
    martu="One line, one slip. Your turn to show off.",
    starter='print("The lantern is lit.)\n',
    solo=True,
    checkpoints=[
        dict(
            id="mend-the-lantern",
            text="Mend the line so it shows `The lantern is lit.`",
            dictated=False,
            hints=[
                "Read the last line of Python's message first. Then look at the line it names.",
                "Count the quote marks.",
            ],
            checks=[
                ("shows the lantern line", shows("The lantern is lit.", "Mend the line so it prints.")),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ words in matching quotes.",
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
    takeaway="You can find and mend a missing quote on your own.",
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
        summary="Show words with print, close every quote and bracket, read Python's message, and switch lines off with #.",
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
