"""Unit 1 "Hello World", part d: Project 1P2 "The Ward Sign", Article 1-A2 "Clock Math", Article 1-A3
"Asking the Traveler: input()", Quick Check 1 (forms A and B, code tasks + questions) and Cheatsheet 1.

Spec: design/curriculum.md, "## Unit 1", items 10 to 14 (u01d).
Introduces op:Pow, op:Mod, op:FloorDiv (article 1-A2) and call:input, call:int (article 1-A3). The project and
the Quick Check use only core Unit 1 tokens (1P2 also uses const:multiline_str from the 1A-07 pool card, which it
names as its prerequisite card).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. Everything here is optional
except as a test-out route, so the tone is "you already know more than you think". Every student has their own
device; pair talk is optional, every checkpoint is solo.

Help ladder (curriculum 2.2) as fields: hints[0] Start me off, hints[1] Point (where to look), another_way,
hints[2] Teach (tiny example with other names), assemble (More structure), solution (Show).

Check codes (curriculum 2.5) built by the helpers below:
  NAME / LEFT  a near-miss name, or the example's name, instead of the task's name
  BARE         a value on a line by itself (made and forgotten), which raises no error
  TEXT / NUM   text needs quotes, numbers don't
  CMB          the program is run again with other numbers (or other input answers); the result must follow
  SWAP / LINE-TOTAL, NEWBOX, OUT (diff)
The harness has no _rerun() helper yet, so CMB is done in the check itself: the student's code is parsed, EVERY
plain-value line of each named box gets the new value (so a new line added under a placeholder still reruns
fairly), and the program runs again in a fresh namespace. The input() try-it uses _quiet(): two reruns with fixed
answers and no echo, so line i of one run can be compared with line i of the other (a typed line stays put).
Messages use invented values only (Tester, Zelda, Captain Glug, moth-grey) and never repeat a student's text.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u01d
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates, filled in per exercise)
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."

_BOX_TEMPLATE = '''import ast as _ast
if "__NAME__" not in globals():
    _tree = _ast.parse(_source)
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
    def _close(_m):
        _a, _b = _m.lower(), "__NAME__".lower()
        return _a.rstrip("s") == _b.rstrip("s") or _a.replace("_", "") == _b.replace("_", "") or _edits(_a, _b) <= 2
    _foreign = __FOREIGN__
    _left = [_m for _m in _made if _m in _foreign]
    _near = [_m for _m in _made if _m not in _foreign and _close(_m)]
    _bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == "Expr" and type(_n.value).__name__ == "Constant" and type(_n.value.value).__name__ in ("str", "int", "float")]
    if _near:
        _msg = "Your box is named `" + _near[0] + "`, but this step needs `__NAME__`. Names match letter for letter, capitals too."
    elif _left:
        _msg = "`" + _left[0] + "` is a name from the Example or an earlier step. This step's box is named `__NAME__`."
    elif _bare:
        _msg = "Line " + str(_bare[0]) + " is a value with no name in front, so Python reads it and throws it away__BARE_FIX__"
    elif [_m for _m in _made if _m not in __SKIP__]:
        _msg = "Your box is named `" + [_m for _m in _made if _m not in __SKIP__][0] + "`, but this step needs `__NAME__`. Names match letter for letter."
    else:
        _msg = "__NONE__"
    assert False, _msg'''


def box_check(name, foreign=(), skip=(), lean=False):
    """NAME + LEFT + BARE (+ another name): the box exists, or the message says why not.
    `skip` = boxes the starter already makes, never named as the student's wrong box.
    `lean` (Quick Check): the same checks, with messages that say what is wrong and where, never the fix."""
    bare_fix = "." if lean else ", like a phone number saved with no contact name. Put `__NAME__ = ` in front of it."
    none_msg = "There is no box named `__NAME__` yet." if lean else "Make a box named `__NAME__`: start a line with `__NAME__ = `."
    code = (_BOX_TEMPLATE.replace("__BARE_FIX__", bare_fix).replace("__NONE__", none_msg)
            .replace("__NAME__", name).replace("__FOREIGN__", repr(list(foreign)))
            .replace("__SKIP__", repr(list(skip))))
    return (f"there is a box named {name}", code)


def text_check(name):
    """TEXT: the box holds non-empty text. (Quick Check only, so the messages are lean.)"""
    return (
        f"{name} holds text",
        f"_v = {name}\n"
        f"assert type(_v).__name__ == 'str', {'`' + name + '` holds `'!r} + repr(_v) + '`, which is not text in quotes.'\n"
        f"assert _v.strip(), '`{name}` holds empty quotes, with nothing between them.'",
    )


def bare_check():
    """BARE: no line is just a value (it raises no error, so only a check can catch it). (Quick Check only: lean.)"""
    return (
        "no value is left without a box",
        "import ast as _ast\n"
        "_bare = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'Constant' and type(_n.value.value).__name__ in ('str', 'int', 'float')]\n"
        "assert not _bare, 'Line ' + str(_bare[0]) + ' is a value with no name in front, so Python reads it and "
        "throws it away.'",
    )


def print_check(name):
    """PRINT: a print uses the box (alone, or glued: `print("Hero: " + name)`), and its value shows.
    (Quick Check only, so the messages are lean.)"""
    return (
        f"prints the box {name}",
        "import ast as _ast\n"
        "_args = [_a for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
        "and type(_n.func).__name__ == 'Name' and _n.func.id == 'print' for _a in _n.args]\n"
        f"_named = [_x for _a in _args for _x in _ast.walk(_a) if type(_x).__name__ == 'Name' and _x.id == '{name}']\n"
        f"_quoted = [_a for _a in _args if type(_a).__name__ == 'Constant' and _a.value == '{name}']\n"
        f"assert _named or not _quoted, 'Your `print` shows the word {name}, because of the quotes.'\n"
        f"assert _named, 'Your code never prints the box `{name}`.'\n"
        f"assert any(str({name}).strip() in _l for _l in _lines()), 'The Console does not show what is inside `{name}`.'",
    )


_NEAR_TEMPLATE = '''import ast as _ast
_made = []
for _n in _ast.walk(_ast.parse(_source)):
    if type(_n).__name__ == "Assign":
        for _t in _n.targets:
            if type(_t).__name__ == "Name" and _t.id not in _made:
                _made.append(_t.id)
def _squash(_m):
    return _m.lower().replace("_", "").rstrip("s")
_near = [_m for _m in _made if _m != "__NAME__" and _squash(_m) == _squash("__NAME__")]
assert not _near, "Your box is named `" + (_near or ["?"])[0] + "`, but this step needs `__NAME__`. Names match letter for letter, capitals too."'''


def near_check(name):
    """NAME on a box the starter already made: a near-miss spelling (case, plural, underscore) was made too."""
    return (f"no near-miss of {name}", _NEAR_TEMPLATE.replace("__NAME__", name))


def num_story_check(count_name, price_name, count, price, what):
    """NUM + SWAP + LINE-TOTAL + the story's values, for one "how many? / how much is one?" pair.
    (Quick Check only, so the messages are lean: what is wrong and where, never the fix.)"""
    return (
        f"{count_name} and {price_name} hold the story's numbers",
        f"_c, _p = {count_name}, {price_name}\n"
        f"for _n, _v in (({count_name!r}, _c), ({price_name!r}, _p)):\n"
        "    assert type(_v).__name__ != 'str', '`' + _n + '` holds text, because of the quotes.'\n"
        f"assert not (_c == {price} and _p == {count}), "
        f"{f'You swapped `{count_name}` and `{price_name}`: each one holds the other one' + chr(39) + 's number.'!r}\n"
        f"assert _p != {count * price}, "
        f"{f'`{price_name}` holds {count * price}, which is already the cost of all {count} {what}, not the price of one.'!r}\n"
        f"assert _c == {count}, ({f'`{count_name}` still holds the placeholder 0.'!r} if _c == 0 else "
        f"{'`' + count_name + '` holds '!r} + str(_c) + {f', not how many {what} the story needs.'!r})\n"
        f"assert _p == {price}, ({f'`{price_name}` still holds the placeholder 0.'!r} if _p == 0 else "
        f"{'`' + price_name + '` holds '!r} + str(_p) + {', not the price of one in the story.'!r})",
    )


_RERUN = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
def _show(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
# What stopped a rerun, in plain words (guide 4.3.6, S8): the student's line number, then what it tried.
def _plain(_x):
    _t, _s = type(_x).__name__, str(_x)
    _tb, _at = _x.__traceback__, None
    while _tb is not None:
        if _tb.tb_frame.f_code.co_filename == 'main.py':
            _at = _tb.tb_lineno
        _tb = _tb.tb_next
    _where = ('line ' + str(_at)) if _at else 'one line'
    if _t == 'NameError':
        _m = _re.search(r"'(\w+)'", _s)
        return _where + ' uses `' + (_m.group(1) if _m else '?') + '`, but no box has that exact name'
    if _t == 'ZeroDivisionError':
        return _where + ' divides by 0'
    if _t == 'TypeError' and ('concatenate' in _s or ("'str'" in _s and '+' in _s)):
        return _where + ' glues text and a number with `+`'
    if _t == 'TypeError' and 'multiply sequence' in _s:
        return _where + ' repeats text by something that is not a whole number'
    if _t == 'TypeError':
        return _where + ' does math with text'
    if _t == 'EOFError':
        return _where + ' asks more questions than there are answers'
    if _t == 'ValueError':
        return _where + ' turns text into a number, but the text is not a whole number'
    return _where + ' could not finish'
def _rerun(_values=None, _answers=None):
    # Every plain `name = value` line of a changed box gets the new value (not only the first), so a student
    # who added a new line under the starter's placeholder instead of editing it is still rerun fairly.
    _tree = _ast.parse(_source)
    _vals = dict(_values or {})
    _seen = set()
    for _n in _tree.body:
        if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name':
            _id = _n.targets[0].id
            if _id in _vals and type(_n.value).__name__ == 'Constant':
                _n.value = _ast.copy_location(_ast.Constant(_vals[_id]), _n.value)
                _seen.add(_id)
    _left = [_k for _k in _vals if _k not in _seen]
    _ns = {'__name__': '__main__', 'input': input}
    _buf, _old, _err = _io.StringIO(), _sys.stdout, ''
    _sys.stdout = _buf
    try:
        if _answers is not None:
            _set_stdin(list(_answers))
        exec(compile(_tree, 'main.py', 'exec'), _ns)
    except Exception as _e:
        _err = _plain(_e)
    finally:
        _sys.stdout = _old
    return _ns, _buf.getvalue(), _err, sorted(_left)
'''

_CMB_HEAD = r'''
    _kind = 'numbers' if all(type(_v).__name__ == 'int' for _v in _vals.values()) else 'values'
    _parts = ['`' + _k + ' = ' + _show(_v) + '`' for _k, _v in _vals.items()]
    _what = _parts[0] if len(_parts) == 1 else ', '.join(_parts[:-1]) + ' and ' + _parts[-1]
    _t = 'test ' + ('number' if _kind == 'numbers' else 'value') + ('' if len(_parts) == 1 else 's')
    _test = ('a ' if len(_parts) == 1 else '') + _t
    _ns, _out, _err, _miss = _rerun(_vals)
    assert not _miss, 'Keep `' + _miss[0] + ' = ` and a ' + _kind[:-1] + ' on a line of its own. Mar\'tu tests your code by changing that line.'
    assert not _err, 'Your code stopped when Mar\'tu tested it with ' + _test + ', ' + _what + ': ' + _err + '. It has to work for other ' + _kind + ' too.'
'''

# CMB message, in the order of the plain-language guide (section 4.3): what happened to the student's line, then
# the step's one fix (the tail: empty in the Quick Check, which stays lean), then the labeled evidence. A box that
# still holds the starter's 0 is named as the placeholder, with no evidence. It says "values" instead of "numbers"
# when the check also swaps in text (C3's made-up hero name Tester).
_CMB_VALUE = "for _vals, _want in __CASES__:" + _CMB_HEAD + r'''    _got = _ns.get('__TARGET__')
    _was = globals().get('__TARGET__')
    _proof = 'Mar\'tu tested your code with ' + _test + ', ' + _what + ': `__TARGET__` should be ' + _show(_want) + ', but it ' + ('stayed ' if _got == _was else 'became ') + _show(_got) + '. Don\'t type the ' + _t + '.'
    _typed = 'a typed-in number' if type(_want).__name__ in ('int', 'float') else 'typed-in text'
    if _got == _was and type(_got).__name__ == 'int' and _got == 0:
        _msg = '`__TARGET__` still holds the placeholder 0. ' + __TAIL__
    elif _got == _was:
        _msg = '`__TARGET__` has ' + _typed + '. ' + __TAIL__ + _proof
    else:
        _msg = '`__TARGET__` comes out wrong for other ' + _kind + '. ' + __TAIL__ + _proof
    assert _got == _want, _msg.strip()
'''

_CMB_LINE = "for _vals, _want in __CASES__:" + _CMB_HEAD + r'''    _rows = [_l.strip() for _l in _out.splitlines() if _l.strip()]
    _said = ('it showed `' + _rows[-1] + '`') if _rows else 'it showed nothing'
    assert _want in _rows, (__TAIL__ + 'Mar\'tu tested your code with ' + _test + ', ' + _what + ': it should show `' + _want + '`, but ' + _said + '. Don\'t type the ' + _t + '.').strip()
'''


def _tail(text):
    """A tail sentence ends with one space, so the evidence can follow it; an empty tail stays empty."""
    return text.strip() + " " if text.strip() else ""


def cmb_check(target, cases, tail=""):
    """CMB on a box: run again with other values; `target` must change to match. cases = [(values, expected), ...].
    `tail` is the step's one fix, between what happened and the evidence. Leave it empty in the Quick Check."""
    code = (_RERUN + _CMB_VALUE.replace("__CASES__", repr(cases)).replace("__TARGET__", target)
            .replace("__TAIL__", repr(_tail(tail))))
    return (f"{target} follows other numbers", code)


def cmb_line_check(cases, tail="Your line has typed-in words or numbers.",
                   label="the line follows other values"):
    """CMB on printed output: run again with other values; the expected line must appear. `tail` says what
    happened (it comes first): the Quick Check's status line, already right for the student's own numbers."""
    code = _RERUN + _CMB_LINE.replace("__CASES__", repr(cases)).replace("__TAIL__", repr(_tail(tail)))
    return (label, code)


def out_line_check(expr, label, tail):
    """OUT (diff): a printed line equals `expr`, computed from the student's own boxes, with the first difference shown."""
    return (
        label,
        f"_want = {expr}\n"
        "_rows = _lines()\n"
        "_got = _rows[-1] if _rows else ''\n"
        "_at = 0\n"
        "while _at < min(len(_want), len(_got)) and _want[_at] == _got[_at]:\n"
        "    _at += 1\n"
        "_same = (' They match up to `' + _want[:_at] + '`, then differ.') if _at else ''\n"
        "assert _rows, 'Your code prints nothing yet. The line should show `' + _want + '`.'\n"
        "assert _want in _rows, 'Your last line shows `' + _got + '`, but it should show `' + _want + '`.' + _same + "
        f"{(' ' + tail) if tail else ''!r}",
    )


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of hello-world; must match u01a/u01b exactly)
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
        term="power",
        aliases=["powers", "exponent"],
        plain="A number multiplied by itself, like 2³ in math class. In Python, `2 ** 3` means 2 × 2 × 2, which is 8.",
        example="print(2 ** 3)",
    ),
    dict(
        term="floor division",
        aliases=["whole division"],
        plain=(
            "Divide and keep only the whole part (floor means round down). In math class, 50 ÷ 12 = 4 R 2, "
            "and `50 // 12` gives the 4."
        ),
        example="print(50 // 12)",
    ),
    dict(
        term="remainder",
        aliases=["remainders", "modulo"],
        plain=(
            "What is left over after dividing. In 50 ÷ 12 = 4 R 2, the remainder is 2, and `50 % 12` gives it. "
            "Here `%` is not percent."
        ),
        example="print(50 % 12)",
    ),
    dict(
        term="order of operations",
        aliases=["operator order"],
        plain=(
            "The order Python does math in: PEMDAS, as in math class. Parentheses first, then `**`, then "
            "`*` `/` `//` `%`, then `+` and `-`, so `2 + 3 * 4` is 14."
        ),
        example="print((2 + 3) * 4)",
    ),
    dict(
        term="input",
        aliases=["input()"],
        plain="`input()` asks a question and waits for an answer. The answer always comes back as text, even a 3.",
        example='name = input("Who goes there? ")',
    ),
    dict(
        term="prompt",
        aliases=["prompts"],
        plain="The question `input()` shows before it waits for an answer, like `\"Who goes there? \"`.",
        example='input("How many sips? ")',
    ),
    dict(
        term="int()",
        aliases=["int"],
        plain=(
            "`int` is short for integer, a whole number. `int()` turns text like `\"3\"` into the number 3, "
            "so you can do math with it."
        ),
        example='sips = int("3")',
    ),
]


# =============================================================================================
# Project 1P2 "The Ward Sign" (optional, 25 min)
# =============================================================================================

_T_ROWS = (
    "# T\n"
    "print(ink * 5)\n"
    'print("  " + ink)\n'
    'print("  " + ink)\n'
    'print("  " + ink)\n'
    'print("  " + ink)\n'
    "print()\n"
)
_O_ROWS = (
    "# O\n"
    "print(ink * 5)\n"
    'print(ink + "   " + ink)\n'
    'print(ink + "   " + ink)\n'
    'print(ink + "   " + ink)\n'
    "print(ink * 5)\n"
    "print()\n"
)
_R_ROWS = (
    "# R\n"
    "print(ink * 4)\n"
    'print(ink + "   " + ink)\n'
    "print(ink * 4)\n"
    'print(ink + "  " + ink)\n'
    'print(ink + "   " + ink)\n'
)
_M_LETTER = 'print("""\n█   █\n██ ██\n█ █ █\n█   █\n█   █""")\n'

_SIGN_HEAD = "# The ward sign, painted down the barrier post.\n"


def _sign(ink="█", top="", o=_O_ROWS, r=_R_ROWS, bottom="", mark=""):
    return (
        _SIGN_HEAD
        + f'ink = "{ink}"\n\n'
        + "# A. Top border\n" + top + "\n"
        + "# B. The letters, five rows each\n" + _T_ROWS + o + r + "\n"
        + "# C. Bottom border\n" + bottom + "\n"
        + "# D. One more letter, in triple quotes\n" + mark
    )


_BORDER = 'print("=" * 9)\n'
SIGN_STARTER = _sign(o="# O\n\n", r="# R\n\n")
SIGN_SOLUTION = _sign(ink="▓", top=_BORDER, bottom=_BORDER, mark=_M_LETTER)

# Rows that change when `ink` changes: run the sign twice, with ink "#" and ink "@", and compare line by line.
_INK_ROWS = _RERUN + r'''
_a = _rerun({'ink': '#'})
_b = _rerun({'ink': '@'})
assert not _a[3], 'Keep a line like `ink = "█"` near the top, with one mark in quotes. Mar\'tu tests your sign by changing that mark.'
assert not _a[2], 'Your sign stopped when Mar\'tu tested it with `ink = "#"`: ' + _a[2] + '. Check each row that uses `ink`.'
_ra, _rb = _a[1].split('\n'), _b[1].split('\n')
_ink_rows = [_i for _i in range(min(len(_ra), len(_rb))) if _ra[_i] != _rb[_i]]
_texts = [_n.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Constant' and type(_n.value).__name__ == 'str']
'''


def ink_rows_check(at_least, letter, group, shape_msg, next_note):
    """CMB with ink, plus: no row half-typed (a mark that stays put when ink changes), and the letter's own five
    ink rows (group 1 = O, 2 = R, after the T's five) have a gap row, so a copied T or a column of marks fails.
    With no `print` at all between `# <letter>` and `next_note` (the untouched starter), the message says the
    letter isn't there yet, instead of counting the T's rows (guide 9, S12)."""
    return (
        f"at least {at_least} rows follow ink",
        _INK_ROWS
        + "assert 'ink' not in _texts, 'Your code has `\"ink\"` in quotes, so Python shows the word ink. "
        "Take the quotes off `ink`. Quotes mean these exact letters. No quotes means look inside the box with this label.'\n"
        + "_src = _source.split('\\n')\n"
        f"_at = [_i + 1 for _i, _l in enumerate(_src) if _l.strip() == '# {letter}']\n"
        f"_end = [_i + 1 for _i, _l in enumerate(_src) if _l.strip().startswith({next_note!r}) and _at and _i + 1 > _at[0]]\n"
        "_drawn = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
        "and getattr(_n.func, 'id', '') == 'print' and _at and _at[0] < _n.lineno < (_end or [len(_src) + 1])[0]]\n"
        + f"assert len(_ink_rows) >= {at_least}, ('Your sign has no {letter} yet. Under `# {letter}`, draw its 5 rows, "
        f"one `print` for each row, with `ink` for every mark.' if _at and not _drawn else 'So far, ' + "
        f"str(len(_ink_rows)) + ' rows of your sign change when `ink` changes. Draw all 5 rows of the {letter} under "
        f"`# {letter}` with `ink`, not a typed █, so they repaint too.')\n"
        + "_mixed = [_i for _i in _ink_rows if any(_x == _y and _x.strip() for _x, _y in zip(_ra[_i], _rb[_i]))]\n"
        "assert not _mixed, 'One row has a typed mark: when Mar\\'tu repainted the sign with `#`, it came out `' + "
        "_ra[_mixed[0]].strip() + '`. Make every mark in that row come from `ink`.'\n"
        + f"_mine = _ink_rows[{5 * group}:{5 * group + 5}]\n"
        + "assert any(_re.search(r'#\\s+#', _ra[_i]) for _i in _mine), " + repr(shape_msg),
    )


BORDER_CHECK = (
    "a stamped border above and below the letters",
    _INK_ROWS
    + r'''
_shown = [(_i, _l.strip()) for _i, _l in enumerate(_captured_stdout.split('\n')) if _l.strip()]
assert _shown, 'Your sign printed nothing. Keep the rows of the letters, and press Run again.'
_ti, _top = _shown[0]
assert _ti not in _ink_rows, 'Your first line changes when `ink` changes, so it is part of a letter, not a border. Under `# A. Top border`, print a border made from another mark: `print("=" * 9)`.'
_stamped = len(_top) >= 5 and any((_top[:_k] * len(_top))[:len(_top)] == _top for _k in (1, 2, 3))
assert _stamped, 'Your top line is not one mark repeated. Stamp one mark many times with `*`: `print("=" * 9)`.'
assert not any(_top in _t for _t in _texts), 'Your border is typed out, mark by mark. Let Python stamp it with `*`: `print("=" * 9)`.'
_last_ink = max(_ink_rows) if _ink_rows else -1
assert any(_i > _last_ink and _l == _top for _i, _l in _shown), 'Your sign has a top border but no bottom one. Under `# C. Bottom border`, print the same border again.'
''',
)

REPAINT_CHECK = (
    "ink holds a new mark",
    _NEAR_TEMPLATE.replace("__NAME__", "ink").replace("but this step needs", "but the sign's box is")
    + "\nassert type(ink).__name__ == 'str' and ink.strip(), 'Keep `ink` as one mark in quotes, like `\"▓\"`.'\n"
    "assert ink != '█', '`ink` still holds █. On line 2, change it to another mark, like `#` or `@`, and press Run.'\n"
    + _INK_ROWS
    + "_now = _captured_stdout.split('\\n')\n"
    "_stale = [_i for _i in _ink_rows if _i < len(_now) and ink not in _now[_i]]\n"
    "assert not _stale, 'The sign still shows the old mark, because your new `ink` line comes after the letters are drawn. "
    "Python reads top to bottom. Change the mark on line 2 instead, and delete the new line.'",
)

TRIPLE_LETTER_CHECK = (
    "one print draws a 5-row letter in triple quotes",
    r'''import ast as _ast
_best = 0
for _n in _ast.walk(_ast.parse(_source)):
    if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == 'print':
        for _a in _n.args:
            _v = _a.value if type(_a).__name__ == 'Constant' else globals().get(_a.id) if type(_a).__name__ == 'Name' else None
            if type(_v).__name__ == 'str':
                _best = max(_best, len([_l for _l in _v.splitlines() if _l.strip()]))
assert _uses('const:multiline_str'), 'Your code has no text in triple quotes yet. Under `# D`, put one `print` with your letter between triple quotes `"""`.'
assert _best >= 5, 'Your triple-quoted letter has ' + str(_best) + (' row' if _best == 1 else ' rows') + '. Make it five rows tall, like the others.'
''',
)

WARD_SIGN = dict(
    kind="project",
    id="ward-sign",
    title="The Ward Sign",
    optional=True,
    minutes=25,
    summary=(
        "Draw the word TOR in big block letters, one letter under another. Every mark comes from one box, `ink`, "
        "so one change to `ink` changes the whole sign."
    ),
    intro=(
        "Mar'tu wants a ward sign on the barrier post: a sign that helps protect the barrier. It spells `TOR` in "
        "big block letters, one letter under another, because the post is tall and thin.\n"
        "Wards work better when they are tidy. Probably."
    ),
    martu=(
        "Each `print` draws one row of a letter. `ink * 5` stamps the mark in `ink` 5 times: `█████`. "
        "`\"  \" + ink` glues 2 spaces in front of one mark. Each letter is 5 rows tall.\n"
        "Every row uses the box `ink`, so one change to `ink` changes the whole sign. I drew the T. "
        "You draw the rest, yes?"
    ),
    example='chalk = "#"\nprint(chalk)\nprint(chalk)\nprint(chalk)\nprint(chalk)\nprint(chalk * 4)\n',
    example_output="#\n#\n#\n#\n####",
    names=["ink"],
    pick="▓",
    pair_talk=(
        "Pair talk: before you change `ink`, ask your partner which rows will change. "
        "Then each of you presses Run on your own screen."
    ),
    predict=dict(
        q="Before you press Run: what will the 5 lines under `# T` print?",
        choices=[
            "█████\n  █\n  █\n  █\n  █",
            "inkinkinkinkink\n  ink\n  ink\n  ink\n  ink",
            "█5\n  █\n  █\n  █\n  █",
        ],
        answer=0,
        explain=(
            "`ink` has no quotes, so Python looks inside the box and finds █. "
            "`ink * 5` stamps it five times. `\"  \" + ink` glues two spaces in front of one mark."
        ),
    ),
    starter=SIGN_STARTER,
    checkpoints=[
        dict(
            id="letter-o",
            text="Under `# O`, draw an O that is 5 rows tall, with one `print` for each row. Use `ink` for every mark.",
            dictated=False,
            hints=[
                "Find `# O` in your code, under the T. Start under `# O` with the top row: `print(ink * 5)`.",
                "Look at the T. Every row has `ink` in it. An O needs a top row, three rows with two sides, "
                "and a bottom row.",
                "`ink * 5` stamps 5 marks. `ink + \"   \" + ink` is a mark, 3 spaces, a mark. "
                "With other names, `print(chalk + \"  \" + chalk)` shows `#  #`.",
                "Top and bottom: `print(ink * 5)`. The three rows between: `print(ink + \"   \" + ink)`.",
            ],
            checks=[ink_rows_check(10, "O", 1, "Your O has no hole in the middle. Draw its sides with a gap between two "
                                  "marks: `ink + \"   \" + ink`.", "# R")],
            pass_line="Mar'tu: An O. Round enough for a post, yes?",
        ),
        dict(
            id="letter-r",
            text="Under `# R`, draw an R that is 5 rows tall, with one `print` for each row. Use `ink` for every mark again.",
            dictated=False,
            hints=[
                "Find `# R` in your code, under your O. Start under `# R` with the top of the R: `print(ink * 4)`.",
                "An R is a top bar, a row with two sides, a middle bar, then two rows of legs. Count your rows: five.",
                "Mix stamps and spaces. `ink * 4` is a bar. `ink + \"   \" + ink` is two sides. "
                "`ink + \"  \" + ink` is a leg that leans in.",
                "All five rows of the R, top to bottom:\n"
                "```python\nprint(ink * 4)\nprint(ink + \"   \" + ink)\nprint(ink * 4)\n"
                "print(ink + \"  \" + ink)\nprint(ink + \"   \" + ink)\n```",
            ],
            checks=[ink_rows_check(15, "R", 2, "Your R needs rows with a gap between two marks, for its side and its "
                                  "leg: `ink + \"   \" + ink`.", "# C")],
            pass_line="Mar'tu: T, O, R. Tor. Good.",
        ),
        dict(
            id="border",
            text=(
                "Add a border line, `print(\"=\" * 9)`, in two places:\n"
                "1. Under `# A. Top border`, so it comes before the T.\n"
                "2. Under `# C. Bottom border`, so it comes after the R."
            ),
            dictated=True,
            hints=[
                "Under `# A. Top border`, type `print(\"=\" * 9)`.",
                "The first line of the sign should be the border. The same line goes again under the R, at `# C`.",
                "`*` stamps a mark many times: `\"~\" * 4` gives `~~~~`. Use a mark that is not `ink`, so the border "
                "stays the same when the ink changes.",
                "Put `print(\"=\" * 9)` under `# A. Top border`, and again under `# C. Bottom border`.",
            ],
            checks=[BORDER_CHECK],
            pass_line="Mar'tu: A frame. Now it looks official.",
        ),
        dict(
            id="repaint",
            text=(
                "Change the mark in `ink`, in two moves:\n"
                "1. On line 2, change the `█` between the quotes to another mark, like `#` or `@`. Or press the "
                "Mar'tu's pick button, next to Names to use.\n"
                "2. Press Run. Every letter of the sign changes to the new mark."
            ),
            dictated=True,
            hints=[
                "Line 2 starts `ink = `. Change only what is inside the quotes.",
                "Look at line 2: `ink = \"█\"`. That one box paints every letter.",
                "A box holds one value at a time. Put a new mark in it and press Run: every line that uses it "
                "changes to match. In the Example, `chalk = \"*\"` would repaint the whole L.",
                "Type `#` in place of the `█` on line 2. Line 2 becomes `ink = \"#\"`.",
            ],
            checks=[REPAINT_CHECK],
            pass_line="Mar'tu: One change, whole sign. That is why we keep the ink in a box.",
        ),
        dict(
            id="triple-letter",
            text=(
                "Under `# D`, draw one more letter, 5 rows tall, inside one `print`. Three quote marks `\"\"\"` start "
                "text that can go over many lines, and three more end it. Draw with any key, like `#` or `X`: "
                "your hero's first letter, maybe."
            ),
            dictated=False,
            hints=[
                "Find `# D` at the bottom of your code. Under `# D`, start with `print(\"\"\"` and press Enter.",
                "Type one `print(`, then three quotes, then five rows of marks, then three quotes and `)`.",
                "Triple quotes hold many lines. This draws a small L:\n```python\nprint(\"\"\"#\n#\n###\"\"\")\n```",
                "```python\nprint(\"\"\"\n█   █\n██ ██\n█ █ █\n█   █\n█   █\"\"\")\n```",
            ],
            checks=[TRIPLE_LETTER_CHECK],
            pass_line=(
                "Mar'tu: Try changing `ink` again and press Run. Your new letter keeps its own marks, yes? "
                "Quotes mean these exact letters."
            ),
        ),
    ],
    solution=SIGN_SOLUTION,
    partials=[
        _sign(r="# R\n\n"),
        _sign(),
        _sign(top=_BORDER, bottom=_BORDER),
        _sign(ink="▓", top=_BORDER, bottom=_BORDER),
    ],
    assemble=dict(
        lines=[
            'ink = "▓"',
            'print("=" * 9)',
            "print(ink * 5)", 'print("  " + ink)', 'print("  " + ink)', 'print("  " + ink)', 'print("  " + ink)',
            "print(ink * 5)", 'print(ink + "   " + ink)', 'print(ink + "   " + ink)', 'print(ink + "   " + ink)',
            "print(ink * 5)",
            "print(ink * 4)", 'print(ink + "   " + ink)', "print(ink * 4)", 'print(ink + "  " + ink)',
            'print(ink + "   " + ink)',
            'print("=" * 9)',
            'print("""', "█   █", "██ ██", "█ █ █", "█   █", '█   █""")',
        ],
        distractors=['print("█   █")', 'print("=========")', 'print("ink" * 5)'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Graph paper",
            text=(
                "Draw the letter on graph paper first. Each row of squares is one `print`. "
                "A filled square is `ink`. An empty square is a space inside quotes.\n"
                "```\n█████   print(ink * 5)\n█   █   print(ink + \"   \" + ink)\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A stamp pad",
            text=(
                "`ink` is the stamp pad. Every row stamps from it. Swap the pad for a new color once, "
                "and every stamp after that is the new color."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Look at one row of your letter.\n"
                "2. Count the marks and the gaps.\n"
                "3. Write one `print` for that row: marks from `ink`, gaps as spaces in quotes.\n"
                "4. Run. Then do the next row."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Mar'tu paints wards from one pot of paint. Swap the pot, and the whole sign is a new color. "
                "`ink` is the pot. A mark typed straight into a `print` is paint from somewhere else."
            ),
        ),
        dict(angle="shorter", text="One `print` per row. Marks come from `ink`. Gaps are spaces in quotes."),
    ],
    bonus=dict(
        by="lucky",
        title="Sign it in your spell color",
        text=(
            "Lucky wants credit. Two moves, at the very bottom of your code:\n"
            "1. Make a box named `spell_color` that holds your hero's spell color in quotes, like `\"silver\"`.\n"
            "2. Under it, print one last line that glues words to `spell_color` with `+`, like `Painted in silver`."
        ),
        hints=[
            "Make the box first: `spell_color = \"silver\"`.",
            "At the very bottom, glue words to the box: `print(\"Painted in \" + spell_color)`.",
        ],
        checks=[
            (
                "spell_color holds text",
                "assert type(spell_color).__name__ == 'str' and spell_color.strip(), "
                "'Make `spell_color` hold a color word in quotes, like `\"silver\"`.'",
            ),
            (
                "the last line is built from spell_color",
                _RERUN
                + "_rows = _lines()\n"
                "assert _rows and spell_color in _rows[-1], "
                "'Your last line does not show your spell color yet. Under the box, print a line that uses "
                "`spell_color`, like `print(\"Painted in \" + spell_color)`.'\n"
                "_t = _rerun({'spell_color': 'moth-grey'})\n"
                "_tr = [_l.strip() for _l in _t[1].splitlines() if _l.strip()]\n"
                "assert _tr and 'moth-grey' in _tr[-1], "
                "'Your last line has the color typed in. Glue the box instead: `print(\"Painted in \" + spell_color)`. "
                "Mar\\'tu tested it with a made-up color, moth-grey, and your line did not change. Don\\'t type moth-grey.'",
            ),
        ],
        solution=SIGN_SOLUTION + 'spell_color = "silver"\nprint("Painted in " + spell_color)\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]',
        why=(
            "You've seen this stamp. The campaign's mana bars were `\"█\"` times the caster's mana. "
            "Same `*`, same blocks. Tonight it paints a sign."
        ),
    ),
    takeaway="One `print` per row, every mark from `ink`: change one box and the whole sign repaints.",
    wrong_answers=[
        dict(why="the starter run as it is: no O yet", code=SIGN_STARTER, fails_at=1, message_contains="no O yet"),
        dict(why="the O drawn, the R not started", code=_sign(r="# R\n\n"), fails_at=2, message_contains="no R yet"),
        dict(
            why="the O typed with blocks instead of ink",
            code=_sign(o='# O\nprint("█████")\nprint("█   █")\nprint("█   █")\nprint("█   █")\nprint("█████")\n', r="# R\n\n"),
            fails_at=1,
            message_contains="repaint",
        ),
        dict(
            why="the O copied from the T's rows (every row uses ink, but there is no O)",
            code=_sign(o="# O\nprint(ink * 5)\n" + 'print("  " + ink)\n' * 4, r="# R\n\n"),
            fails_at=1,
            message_contains="hole",
        ),
        dict(
            why="the O as a column of single marks",
            code=_sign(o="# O\n" + "print(ink)\n" * 5, r="# R\n\n"),
            fails_at=1,
            message_contains="hole",
        ),
        dict(
            why="the O half typed: ink glued to a typed block, so only half of each side repaints",
            code=_sign(o='# O\nprint(ink * 5)\nprint(ink + "   █")\nprint(ink + "   █")\nprint(ink + "   █")\nprint(ink * 5)\n',
                       r="# R\n\n"),
            fails_at=1,
            message_contains="typed mark",
        ),
        dict(
            why="the R drawn as a straight column (a copied T shape)",
            code=_sign(r="# R\nprint(ink * 4)\n" + 'print("  " + ink)\n' * 4),
            fails_at=2,
            message_contains="gap",
        ),
        dict(
            why="ink put in quotes, so the word ink is stamped",
            code=_sign(o='# O\nprint("ink" * 5)\nprint("ink" + "   " + "ink")\nprint("ink" * 5)\n', r="# R\n\n"),
            fails_at=1,
            message_contains="quotes",
        ),
        dict(why="ink with no quotes around the mark", code=_sign(ink="█").replace('ink = "█"', "ink = █"),
             fails_at=0, message_contains="invalid character"),
        dict(why="def used to make the ink box", code=_sign().replace('ink = "█"', 'def ink = "█"'),
             fails_at=0, message_contains="expected"),
        dict(why="the border typed out by hand", code=_sign(top='print("=========")\n', bottom='print("=========")\n'),
             fails_at=3, message_contains="typed out"),
        dict(why="a border on top only", code=_sign(top=_BORDER), fails_at=3, message_contains="again"),
        dict(why="the border made from ink, so it is part of the letters",
             code=_sign(top="print(ink * 9)\n", bottom="print(ink * 9)\n"), fails_at=3, message_contains="changes when"),
        dict(why="ink changed only at the end, after the letters are drawn, so the sign never repaints",
             code=_sign(top=_BORDER, bottom=_BORDER) + 'ink = "▓"\n', fails_at=4, message_contains="after the letters"),
        dict(why="a new box Ink with a capital I", code=_sign(top=_BORDER, bottom=_BORDER).replace('ink = "█"\n', 'ink = "█"\nInk = "▓"\n'),
             fails_at=4, message_contains="letter for letter"),
        dict(why="the extra letter drawn with five separate prints",
             code=_sign(ink="▓", top=_BORDER, bottom=_BORDER,
                        mark='print("█   █")\nprint("██ ██")\nprint("█ █ █")\nprint("█   █")\nprint("█   █")\n'),
             fails_at=5, message_contains="triple quotes"),
        dict(why="a triple-quoted letter only 3 rows tall",
             code=_sign(ink="▓", top=_BORDER, bottom=_BORDER, mark='print("""█   █\n█ █ █\n█   █""")\n'),
             fails_at=5, message_contains="five rows"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="repeat-string,print-text,make-variable", solo="false",
             dictates="3,4", foreign_names="chalk", prereq_card="1A-07 many-lines-at-once") + "\n"
        "Spec 1P2. Letters go DOWN the post (one under another), so each row is one print and no row needs "
        "side-by-side glue. Checks: CP1/CP2 count rows that change between two reruns (ink '#' and ink '@'), so "
        "rows typed with █ are caught (CMB with ink); a row with a mark that is the same in both reruns is half "
        "typed (caught); the letter's own five ink rows (after the T's five) need a row with a gap between two "
        "marks, so a copied T, a column of marks or a filled block fails while any real O or R design passes; CP3 the border is the first "
        "line, not an ink row, stamped (a 1-3 character unit repeated), not typed as one literal, and repeated after "
        "the last ink row (a later side-quest line under the sign keeps it green); CP4 ink changed (near-miss name "
        "caught first) AND the printed letters use the new mark (ink changed after the letters fails). CP4 suggests "
        "`#` or `@` (or Mar'tu's pick ▓); any mark passes all five steps, `#`, `@`, `X`, `*` and even `=` (the "
        "reruns use their own marks, so the `=` border is never an ink row). CP5 one print with a triple-quoted "
        "string of 5+ non-blank rows, drawn with any key. The triple-quoted letter does "
        "not follow ink on purpose: CP5's pass line asks the student to notice that (the quotes rule again). "
        "Side quest (spec): sign the post in your hero's spell color, checked with a rerun (spell_color 'moth-grey'). "
        "Structure pass (guide 9, S12): run untouched, the starter used to get 'So far, 5 rows of your sign change "
        "when ink changes', which counts the T Mar'tu drew. With no `print` between `# O` and `# R` (or `# R` and "
        "`# C`), the message now says the sign has no O (or R) yet and where to draw it (WAs: the starter, and "
        "the O done with the R empty). A sign that stops on a rerun says what stopped it in plain words (_plain, "
        "S8). "
        "Trial mode after a QC1 pass: premise + required output + the check table, from blank (site work)."
    ),
)


# =============================================================================================
# Article 1-A2 "Clock Math" (optional, 12 min) and try-it 1-A2a
# =============================================================================================

WHERE_IS_THE_HAND = dict(
    id="where-is-the-hand",
    title="Where is the hand?",
    martu=(
        "`%` gives the remainder. In math class, 50 ÷ 12 = 4 R 2, and `50 % 12` gives the 2. The Ley Clock has "
        "12 marks, 0 to 11, so `% 12` wraps any count back onto the clock. Here `%` is not percent.\n"
        "`50 // 12` gives the 4, the whole part. PEMDAS still works: add inside parentheses first, then wrap."
    ),
    example="glass_mark = 8\nhours_slept = 6\nprint((glass_mark + hours_slept) % 12)\n",
    example_output="2",
    names=["hand", "turns"],
    pair_talk=(
        "Pair talk: each of you picks a new `start` and `hours`. Your partner guesses the mark before you press Run."
    ),
    predict=dict(
        q="Warm-up, before you press Run: what will this line print?",
        code="print(10 - 2 * 3)\n",
        choices=["24", "4", "10 - 2 * 3"],
        answer=1,
        explain=(
            "PEMDAS, as in math class: Python does `*` (times) before `-`. 2 × 3 is 6, and 10 − 6 is 4. "
            "Parentheses would go first: `(10 - 2) * 3` is 24."
        ),
    ),
    starter=(
        "start = 10    # the mark the hand is on now\n"
        "hours = 5     # hours until Mar'tu looks again\n"
        "hand = 0      # which mark will the hand be on?\n"
        "turns = 0     # how many times will it pass mark 0?\n"
        "print(hand)\n"
        "print(turns)\n"
    ),
    checkpoints=[
        dict(
            id="find-the-hand",
            text=(
                "On line 3, replace the `0` in `hand = 0` with math that finds the mark where the hand stops: add "
                "`start` and `hours`, then wrap the total with `% 12`. Use the box names, not numbers."
            ),
            dictated=False,
            hints=[
                "Look at line 3. Replace the 0 in `hand = 0`. Start with `(start + hours)`.",
                "Which two boxes say where the hand starts and how far it moves? They are on lines 1 and 2.",
                "`%` wraps a count onto the clock: `14 % 12` is 2. With other names: "
                "`(glass_mark + hours_slept) % 12`. Add inside parentheses first.",
                "Write `hand = (start + hours) % 12` in place of `hand = 0`.",
            ],
            checks=[
                near_check("hand"),
                (
                    "hand is a mark on the clock",
                    "_v = hand\n"
                    "assert type(_v).__name__ != 'float', '`hand` holds ' + str(_v) + ', a decimal, because `/` divides. "
                    "Use `%`: it gives what is left over, the remainder, and that is the mark.'\n"
                    "assert _v != start + hours, '`hand` holds ' + str(_v) + ', but the clock only has marks 0 to 11. "
                    "Add inside parentheses first, then wrap with `% 12`.'\n"
                    "assert _v == (start + hours) % 12, ('`hand` still holds the placeholder 0. ' if _v == 0 else "
                    "'`hand` holds ' + str(_v) + '. ') + 'Start at `start`, move `hours` marks, then wrap with `% 12`.'",
                ),
                cmb_check("hand", [({"start": 9, "hours": 50}, 11), ({"start": 11, "hours": 1}, 0)],
                          tail="Use the box names `start` and `hours`, not numbers."),
            ],
            pass_line="Mar'tu: Mark 3. It is not a compass, Lucky. It goes around.",
        ),
        dict(
            id="count-the-turns",
            text=(
                "On line 4, replace the `0` in `turns = 0` with how many times the hand passes mark 0. Use `//` "
                "on the same total: it keeps only the whole part, like the 4 in 50 ÷ 12 = 4 R 2."
            ),
            dictated=False,
            hints=[
                "Look at line 4. Replace the 0 in `turns = 0`. Start with `(start + hours) //`.",
                "Every 12 hours, the hand passes mark 0 once.",
                "`//` divides and keeps the whole part: `26 // 12` is 2, so 26 hours from mark 0 pass it twice.",
                "Write `turns = (start + hours) // 12` in place of `turns = 0`.",
            ],
            checks=[
                near_check("turns"),
                (
                    "turns counts whole trips",
                    "assert type(turns).__name__ != 'float', '`turns` holds ' + str(turns) + ', a decimal, because `/` "
                    "gives decimals. Use `//`: it keeps only the whole part.'\n"
                    "assert turns == (start + hours) // 12, '`turns` holds ' + str(turns) + '. Count whole trips around "
                    "12 marks: divide the total by 12 with `//`.'",
                ),
                cmb_check("turns", [({"start": 9, "hours": 50}, 4), ({"start": 1, "hours": 2}, 0)],
                          tail="Use the box names `start` and `hours`, not numbers."),
            ],
        ),
    ],
    solution=(
        "start = 10    # the mark the hand is on now\n"
        "hours = 5     # hours until Mar'tu looks again\n"
        "hand = (start + hours) % 12\n"
        "turns = (start + hours) // 12\n"
        "print(hand)\n"
        "print(turns)\n"
    ),
    partials=[
        "start = 10\nhours = 5\nhand = (start + hours) % 12\nturns = 0\nprint(hand)\nprint(turns)\n",
    ],
    assemble=dict(
        lines=["start = 10", "hours = 5", "hand = (start + hours) % 12", "turns = (start + hours) // 12",
               "print(hand)", "print(turns)"],
        distractors=["hand = start + hours % 12", "turns = (start + hours) / 12", "hand = 3"],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "The marks go around, then start again:\n```\n... 9 10 11 0 1 2 3 ...\n```\n"
                "Count 4 steps from 9: 10, 11, 0, 1. The hand stops on mark 1."
            ),
        ),
        dict(
            angle="everyday",
            label="A wall clock",
            text="A wall clock does this. Three hours after 11 o'clock is 2 o'clock, not 14 o'clock. `(11 + 3) % 12` is 2.",
        ),
        dict(
            angle="math class",
            label="From math class",
            text=(
                "This is long division with a remainder. 50 ÷ 12 = 4 R 2: 12 fits into 50 four whole times, and 2 "
                "is left over. `50 // 12` gives the 4, and `50 % 12` gives the 2."
            ),
        ),
        dict(
            angle="step-by-step",
            text="1. Add: `start + hours`.\n2. Too big for the clock? Take away 12, and again, until it fits.\n"
            "3. What is left is the mark. `% 12` does steps 2 and 3 at once.",
        ),
        dict(angle="shorter", text="`hand = (start + hours) % 12`. Parentheses first, then wrap."),
    ],
    takeaway=(
        "In 50 ÷ 12 = 4 R 2, `50 // 12` gives the 4 and `50 % 12` gives the 2. `(start + hours) % 12` wraps a "
        "count onto the clock."
    ),
    wrong_answers=[
        dict(why="the mark worked out by hand", code="start = 10\nhours = 5\nhand = 3\nturns = 1\nprint(hand)\nprint(turns)\n",
             fails_at=1, message_contains="11"),
        dict(why="the story's numbers typed into the formula",
             code="start = 10\nhours = 5\nhand = (10 + 5) % 12\nturns = 0\nprint(hand)\n", fails_at=1, message_contains="11"),
        dict(why="no brackets, so % happens first",
             code="start = 10\nhours = 5\nhand = start + hours % 12\nturns = 0\nprint(hand)\n", fails_at=1, message_contains="parentheses"),
        dict(why="added but never wrapped",
             code="start = 10\nhours = 5\nhand = start + hours\nturns = 0\nprint(hand)\n", fails_at=1, message_contains="0 to 11"),
        dict(why="/ instead of %",
             code="start = 10\nhours = 5\nhand = (start + hours) / 12\nturns = 0\nprint(hand)\n", fails_at=1, message_contains="left over"),
        dict(why="a new box Hand with a capital H",
             code="start = 10\nhours = 5\nhand = 0\nHand = (start + hours) % 12\nturns = 0\nprint(Hand)\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="/ instead of // for the turns",
             code="start = 10\nhours = 5\nhand = (start + hours) % 12\nturns = (start + hours) / 12\nprint(turns)\n",
             fails_at=2, message_contains="decimal"),
        dict(why="the turns with the numbers typed into the formula",
             code="start = 10\nhours = 5\nhand = (start + hours) % 12\nturns = (10 + 5) // 12\n", fails_at=2,
             message_contains="4"),
        dict(why="the turns typed in",
             code="start = 10\nhours = 5\nhand = (start + hours) % 12\nturns = 1\nprint(turns)\n", fails_at=2, message_contains="4"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="clock-math", solo="false", dictates="",
             foreign_names="glass_mark,hours_slept") + "\n"
        "Spec 1-A2a [CMB]. Values 10 + 5 chosen so the no-brackets slip (10 + 5 % 12 = 15) gives a different answer "
        "from (10 + 5) % 12 = 3; with 9 + 50 both give 11, so that pair is only a CMB rerun. CP2 (`//`) is an addition: "
        "the article is the prerequisite card for 1C-08's 10-wide side quest, which needs `//`."
    ),
)

CLOCK_MATH = dict(
    kind="article",
    id="clock-math",
    title="Clock Math",
    optional=True,
    minutes=12,
    summary=(
        "Three more math signs, `**`, `//` and `%`, and PEMDAS in Python. Then you work out where the Ley Clock's "
        "hand stops."
    ),
    introduces=["op:Pow", "op:Mod", "op:FloorDiv"],
    body=(
        "Three more math signs. You don't need them for the campaign. They are here for the curious, yes?\n"
        "1. `**` is a [[power]], like 2³ in math class: `2 ** 3` means 2 × 2 × 2, which is 8.\n"
        "2. `//` is [[floor division]]. *Floor* means round down: divide, then keep only the whole part. "
        "In math class, 50 ÷ 12 = 4 R 2, and `50 // 12` gives the 4.\n"
        "3. `%` gives the [[remainder]], what is left over: `50 % 12` gives the 2. Here `%` is not percent.\n"
        "Python uses the [[order of operations]] you know from math class as PEMDAS. Parentheses first. "
        "Then `**`. Then `*`, `/`, `//` and `%`. Then `+` and `-`. So `2 + 3 * 4` is 14, but `(2 + 3) * 4` is 20.\n"
        "Now the Ley Clock. It has 12 marks, numbered 0 to 11. After mark 11 comes mark 0 again, the way a wall "
        "clock goes from 12 back to 1. The hand moves one mark each hour.\n"
        "The hand is on mark 9. Where is it 50 hours from now? Add first, then wrap: `(9 + 50) % 12` is 11.\n"
        "The parentheses matter. `9 + 7 % 12` does the `%` first and gives 16, which is not even a mark. "
        "`(9 + 7) % 12` gives 4.\n"
        "It is not a compass, Lucky. It is a clock. It goes around."
    ),
    examples=[
        dict(code="print(2 + 3 * 4)\nprint((2 + 3) * 4)\n", output="14\n20"),
        dict(code="print(2 ** 3)\nprint(50 // 12)\nprint(50 % 12)\n", output="8\n4\n2"),
        dict(code="print((9 + 50) % 12)\nprint(9 + 7 % 12)\nprint((9 + 7) % 12)\n", output="11\n16\n4"),
    ],
    exercises=[WHERE_IS_THE_HAND],
    notes=(
        "meta: path=optional; prereq_for=8P2,1C-08 side quest (10 wide). Intro op:Pow op:Mod op:FloorDiv. "
        "The article examples use bare numbers; the try-it uses boxes, so the examples never show the try-it's "
        "names or values."
    ),
)


# =============================================================================================
# Article 1-A3 "Asking the Traveler: input()" (optional, 15 min) and try-it 1-A3a
# =============================================================================================

# The try-it's checks run the program again twice with fixed answers (Lucky/3 and Tester/5), whatever the
# student typed in their own Input box. The answer is NOT echoed in these runs, so line i of one run can be
# compared with line i of the other: a line that FOLLOWS the answer was built from the box; a typed one stays put.
_QUIET = r'''import io as _io
import re as _re
import sys as _sys
def _show(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
# What stopped a rerun, in plain words (guide 4.3.6, S8): the student's line number, then what it tried.
def _plain(_x):
    _t, _s = type(_x).__name__, str(_x)
    _tb, _at = _x.__traceback__, None
    while _tb is not None:
        if _tb.tb_frame.f_code.co_filename == 'main.py':
            _at = _tb.tb_lineno
        _tb = _tb.tb_next
    _where = ('line ' + str(_at)) if _at else 'one line'
    if _t == 'NameError':
        _m = _re.search(r"'(\w+)'", _s)
        return _where + ' uses `' + (_m.group(1) if _m else '?') + '`, but no box has that exact name'
    if _t == 'ZeroDivisionError':
        return _where + ' divides by 0'
    if _t == 'TypeError' and ('concatenate' in _s or ("'str'" in _s and '+' in _s)):
        return _where + ' glues text and a number with `+`'
    if _t == 'TypeError' and 'multiply sequence' in _s:
        return _where + ' repeats text by something that is not a whole number'
    if _t == 'TypeError':
        return _where + ' does math with text'
    if _t == 'EOFError':
        return _where + ' asks more questions than there are answers'
    if _t == 'ValueError':
        return _where + ' turns text into a number, but the text is not a whole number'
    return _where + ' could not finish'
def _quiet(_answers):
    _left, _asked = list(_answers), []
    def _ask(_prompt=''):
        _asked.append(_prompt)
        _sys.stdout.write(str(_prompt) + '\n')
        if not _left:
            raise EOFError('This program asked for more input than it was given.')
        return _left.pop(0)
    _ns = {'__name__': '__main__', 'input': _ask}
    _buf, _old, _err, _why = _io.StringIO(), _sys.stdout, '', ''
    _sys.stdout = _buf
    try:
        exec(compile(_source, 'main.py', 'exec'), _ns)
    except Exception as _e:
        _err, _why = type(_e).__name__ + ': ' + str(_e), _plain(_e)
    finally:
        _sys.stdout = _old
    return _ns, [_l.strip() for _l in _buf.getvalue().split('\n')], _err, len(_asked), _why
_nsA, _a, _errA, _usedA, _whyA = _quiet(['Lucky', '3'])
_nsB, _b, _errB, _usedB, _whyB = _quiet(['Tester', '5'])
_pairs = list(zip(_a, _b))
'''

_GREET_CHECK = (
    "the greeting is built from traveler",
    _QUIET
    + r'''
assert _usedA >= 1, 'Your program never asks the traveler\'s name. Keep line 1: `traveler = input("Who goes there? ")`.'
assert not _errB or 'EOF' in _errB, 'Your code stopped when Mar\'tu tested it with a made-up name, Tester: ' + _whyB + '. It has to work for any name.'
_follow = [_y for _x, _y in _pairs if 'Lucky' in _x and 'Tester' in _y]
assert _follow or not any('traveler' in _x for _x in _a), 'Your greeting shows the word traveler, because `traveler` is in quotes. Take the quotes off `traveler`. Quotes mean these exact letters. No quotes means look inside the box with this label.'
assert _follow or not any('Lucky' in _x for _x in _a), 'Your greeting says Lucky because the name is typed in. Use the box instead: `print("Welcome, " + traveler)`. Mar\'tu tested your code with a made-up name, Tester, and it still said Lucky. Don\'t type Tester.'
assert _follow, 'Under `# 1.`, print a greeting with the traveler\'s name in it, like `print("Welcome, " + traveler + ".")`.'
assert any(_y.replace('Tester', '').strip(' .,!?:;-') for _y in _follow), 'Your line shows only the name. Add a greeting word too, like `print("Welcome, " + traveler)`.'
''',
)

_SIPS_CHECK = (
    "sips holds a number from a second input()",
    _QUIET
    + r'''
assert _usedA == 2, 'Your program asked ' + str(_usedA) + (' question' if _usedA == 1 else ' questions') + '. It needs 2: the name, then the sips.'
_s = _nsA.get('sips')
assert type(_s).__name__ != 'str', '`sips` holds the text ' + _show(_s) + '. `input()` always hands back text. Wrap it to make a number: `int(input(...))`.'
assert type(_s).__name__ != 'float', '`sips` holds ' + str(_s) + ', a decimal. Use `int()` for a whole number of sips.'
# `sips = sips * 2` later on (a fair reassign, for step 3) leaves 6 and 10 in the box: that still follows the answer.
assert type(_s).__name__ == 'int' and _s in (3, 6), '`sips` held ' + _show(_s) + ' when the traveler answered 3. Keep the answer to the sips question in `sips`, as a number.'
assert _nsB.get('sips') == _s // 3 * 5, 'Your `sips` has a number typed in. Keep the answer itself in `sips`: `sips = int(input("How many sips? "))`. Mar\'tu tested it with a test answer, 5 sips, and `sips` still held ' + _show(_nsB.get('sips')) + '.'
''',
)

_DOUBLE_CHECK = (
    "prints double the sips, and follows other answers",
    _QUIET
    + r'''
def _nums(_l):
    return _re.findall(r'\d+', _l)
assert not any('sipssips' in _x for _x in _a), 'Your line doubles the word sips, because `sips` is in quotes. Take the quotes off `sips`. Quotes mean these exact letters. No quotes means look inside the box with this label.'
assert not any('33' in _nums(_x) for _x in _a), 'Your program printed 33. That is the text "3" glued twice. Make `sips` a number with `int()` first.'
assert any('6' in _nums(_x) for _x in _a), 'Nothing shows 6 yet. With 3 sips, double is 6. Under `# 3.`, print `sips` times 2.'
assert not _errB, 'Your code stopped when Mar\'tu tested it with a test answer, 5 sips: ' + _whyB + '. It has to work for any answer.'
assert any('6' in _nums(_x) and '10' in _nums(_y) for _x, _y in _pairs), 'Your line that shows 6 has a number typed in. Use the box instead: `print(sips * 2)`. Mar\'tu tested it with a test answer, 5 sips, and your line did not change to 10. Don\'t type 10.'
''',
)

WHO_GOES_THERE = dict(
    id="who-goes-there",
    title="Who goes there?",
    martu=(
        "`input()` asks a question and waits for the answer. The answer always comes back as text, like writing on "
        "a paper form. For math, wrap it in `int()`. `int` is short for integer, a whole number: `int(\"3\")` gives 3.\n"
        "The answers come from the area labeled Input for your program, under your code, one answer per line."
    ),
    example='visitor = input("Who knocks? ")\nprint("Come in, " + visitor + ".")\n',
    example_output="Who knocks? Lucky\nCome in, Lucky.",
    stdin=["Lucky", "3"],
    names=["traveler", "sips"],
    pair_talk=(
        "Pair talk: each of you changes the answers in the area labeled Input for your program, on your own screen. "
        "Tell your partner what your program will print, then press Run."
    ),
    predict=dict(
        q="Before you press Run: what will this code print?",
        code='coins = "4"\nprint(coins + coins)\n',
        choices=["8", "44", "an error"],
        answer=1,
        explain=(
            "`\"4\"` is in quotes, so it is text, and `+` glues text like a compound word: `44`. "
            "Every answer from `input()` is text like this."
        ),
    ),
    starter=(
        'traveler = input("Who goes there? ")\n'
        "# 1. Greet the traveler by name.\n"
        "\n"
        "# 2. Ask how many sips of glug they want. Keep the answer in sips, as a number.\n"
        "\n"
        "# 3. Print double the sips.\n"
    ),
    checkpoints=[
        dict(
            id="greet",
            text=(
                "Under `# 1.`, print a greeting. Glue words to the box `traveler` with `+`. With the answer Lucky, "
                "you should see something like `Welcome, Lucky.`"
            ),
            dictated=False,
            hints=[
                "Go to the empty line under `# 1.`. Start with `print(\"Welcome, \" + `.",
                "Line 1 already asked the name and keeps it in `traveler`. Use that box, with no quotes.",
                "`+` glues text. With other names: `print(\"Come in, \" + visitor + \".\")`.",
                "Write `print(\"Welcome, \" + traveler + \".\")` under `# 1.`.",
            ],
            checks=[_GREET_CHECK],
            pass_line="Mar'tu: Polite. The barrier likes polite.",
        ),
        dict(
            id="ask-sips",
            text=(
                "Under `# 2.`, ask the traveler how many sips they want, and keep the answer in a box named `sips`, "
                "as a number. Ask with `input()`, as line 1 does, and wrap it in `int( )`."
            ),
            dictated=False,
            hints=[
                "Go to the empty line under `# 2.`. Start the line with `sips = int(input(`.",
                "Look at line 1. It asks a question the same way. This time, wrap the `input(...)` in `int()`.",
                "`input()` hands back text. `int()` turns text like `\"4\"` into the number 4. "
                "With other names: `coins = int(input(\"Coins? \"))`.",
                "Write `sips = int(input(\"How many sips? \"))` under `# 2.`.",
            ],
            checks=[box_check("sips", foreign=["visitor", "coins"], skip=["traveler"]), _SIPS_CHECK],
        ),
        dict(
            id="double",
            text="Make a new line under `# 3.` and print double the sips: the box `sips` times 2.",
            dictated=False,
            hints=[
                "Click at the end of the `# 3.` line and press Enter. Start with `print(sips`.",
                "`sips` is a number now. Python can do math with it.",
                "`*` means times: with other names, `print(coins * 3)`.",
                "Write `print(sips * 2)` under `# 3.`.",
            ],
            checks=[_DOUBLE_CHECK],
            pass_line="Lucky: Six sips. Fine. But I'm keeping track.",
        ),
    ],
    solution=(
        'traveler = input("Who goes there? ")\n'
        "# 1. Greet the traveler by name.\n"
        'print("Welcome, " + traveler + ".")\n'
        "# 2. Ask how many sips of glug they want. Keep the answer in sips, as a number.\n"
        'sips = int(input("How many sips? "))\n'
        "# 3. Print double the sips.\n"
        "print(sips * 2)\n"
    ),
    partials=[
        'traveler = input("Who goes there? ")\nprint("Welcome, " + traveler + ".")\n',
        'traveler = input("Who goes there? ")\nprint("Welcome, " + traveler + ".")\nsips = int(input("How many sips? "))\n',
    ],
    assemble=dict(
        lines=[
            'traveler = input("Who goes there? ")',
            'print("Welcome, " + traveler + ".")',
            'sips = int(input("How many sips? "))',
            "print(sips * 2)",
        ],
        distractors=['sips = input("How many sips? ")', 'print("Welcome, traveler.")', "print(6)"],
    ),
    another_way=[
        dict(
            angle="picture",
            text="```\ntyped 3\n-> input() gives \"3\" (text)\n-> int() gives 3 (a number)\n-> 3 * 2 is 6\n```",
        ),
        dict(
            angle="everyday",
            label="A form",
            text="A paper form only holds writing. Even the line for your age holds the written 13, not a number you "
            "can add. `int()` reads the writing and gives you a number.",
        ),
        dict(
            angle="from the campaign",
            text="`user.clicked()` hands back text too, like `\"option 1\"`. That is why the dialogue code "
            "compared it with words in quotes.",
        ),
        dict(angle="shorter", text="`input()` gives text. `int(input())` gives a number."),
    ],
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='if (user.clicked() == "option 1"):',
        why=(
            "You've seen this. `user.clicked()` hands back text, the same way `input()` does. "
            "So the campaign compared it with text in quotes: `\"option 1\"`."
        ),
    ),
    takeaway="`input()` always hands back text. Use `int(input(...))` when you need a number.",
    wrong_answers=[
        dict(why="the greeting typed with the name",
             code='traveler = input("Who goes there? ")\nprint("Welcome, Lucky.")\n', fails_at=1, message_contains="Tester"),
        dict(why="both greetings typed, one for Lucky and one for Tester",
             code='traveler = input("Who goes there? ")\nprint("Welcome, Lucky.")\nprint("Welcome, Tester.")\n',
             fails_at=1, message_contains="still said Lucky"),
        dict(why="only the name printed, no greeting",
             code='traveler = input("Who goes there? ")\nprint(traveler)\n', fails_at=1, message_contains="only the name"),
        dict(why="the name typed into the box instead of asked",
             code='traveler = "Lucky"\nprint("Welcome, " + traveler)\n', fails_at=1, message_contains="never asks"),
        dict(why="traveler in quotes",
             code='traveler = input("Who goes there? ")\nprint("Welcome, traveler.")\n', fails_at=1, message_contains="quotes"),
        dict(why="sips left as text",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nsips = input("How many sips? ")\nprint(sips * 2)\n',
             fails_at=2, message_contains="int("),
        dict(why="sips typed in, no second question",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nsips = 3\nprint(sips * 2)\n',
             fails_at=2, message_contains="needs 2"),
        dict(why="sips typed in, beside a second question whose answer is never kept",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\ninput("How many sips? ")\nsips = 3\n'
                  'print(sips * 2)\n',
             fails_at=2, message_contains="still held 3"),
        dict(why="Sips with a capital S",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nSips = int(input("How many sips? "))\nprint(Sips * 2)\n',
             fails_at=2, message_contains="letter for letter"),
        dict(why="the double typed in",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nsips = int(input("How many sips? "))\nprint(6)\n',
             fails_at=3, message_contains="10"),
        dict(why="6 and 10 both typed, to match both answers",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nsips = int(input("How many sips? "))\n'
                  'print(6)\nprint(10)\n',
             fails_at=3, message_contains="did not change to 10"),
        dict(why="the word sips doubled",
             code='traveler = input("Who goes there? ")\nprint("Welcome, " + traveler)\nsips = int(input("How many sips? "))\nprint("sips" * 2)\n',
             fails_at=3, message_contains="quotes"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="input-int", solo="false", dictates="",
             foreign_names="visitor,coins") + "\n"
        "Spec 1-A3a: stdin [Lucky, 3]. Every check reruns the program twice, quietly, with [Lucky, 3] and [Tester, 5] "
        "(CMB through stdin), whatever is in the student's own Input box, so pair-talk edits never block a pass. "
        "CP1 a line that follows the name (Lucky -> Tester) and has a greeting word; CP2 two questions asked and "
        "sips follows the answer (3 -> 5; 6 -> 10 also passes, for `sips = sips * 2` in step 3); CP3 a line that "
        "shows 6 and changes to 10. Typed lines (both greetings typed, 6 and 10 both printed) stay put and fail."
    ),
)

ASKING_THE_TRAVELER = dict(
    kind="article",
    id="asking-the-traveler",
    title="Asking the Traveler: input()",
    optional=True,
    minutes=15,
    summary="Let your program ask a question. The answer is always text, so `int()` turns it into a number.",
    introduces=["call:input", "call:int"],
    body=(
        "Sometimes a program should ask. The [[input]] command, `input()`, shows a question, called the [[prompt]], "
        "and waits for an answer.\n"
        "Whatever comes back is text, like writing on a paper form. Even `3` comes back as the text `\"3\"`.\n"
        "Text can't do math: `\"3\" + \"3\"` glues to `33`. To get a real number, use [[int]]: "
        "`int(input(\"Sips? \"))`. `int` is short for integer, a whole number.\n"
        "On this site, the answers come from the area labeled Input for your program, under your code, one answer "
        "per line. Change them and press Run again, as often as you like.\n"
        "You've seen this before. In the campaign, `user.clicked()` handed back text, like `\"option 1\"`. "
        "That is why the dialogue code compared it with words in quotes."
    ),
    examples=[
        dict(code='visitor = input("Who knocks? ")\nprint("Come in, " + visitor + ".")\n',
             output="Who knocks? Gearshift\nCome in, Gearshift.", stdin=["Gearshift"]),
        dict(code='coins = input("Coins? ")\nprint(coins + coins)\n', output="Coins? 4\n44", stdin=["4"]),
        dict(code='coins = int(input("Coins? "))\nprint(coins + coins)\n', output="Coins? 4\n8", stdin=["4"]),
    ],
    exercises=[WHO_GOES_THERE],
    notes=(
        "meta: path=optional. Intro call:input call:int. Campaign link: user.clicked() also hands back text, "
        "compared with ==. The console shows prompt + answer on one line, as a terminal would."
    ),
)


# =============================================================================================
# Quick Check 1 (test-out). Form A and form B: five code tasks each, plus three questions each.
# =============================================================================================

# The site's Quick Check intro already says "No hints in a Quick Check" once, so each task opens with its own lead.
_QC_MARTU = ""


def _qc_meta(skills, dictates, foreign="", form="A"):
    return meta(starter_level="S3", path="QC1", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# ---- C1: make a box with the exact name (make-variable, exact-names, quote-text) ----

def _c1(form, name, what, foreign, ex_code, ex_out, pick, wrong_value="Zelda", other_name="hero"):
    # A story word in the box's name gets its gloss in Mar'tu's first paragraph (form B's `familiar`).
    gloss = " A familiar is a wizard's animal helper, like an owl." if name == "familiar" else ""
    return dict(
        id="make-a-box",
        title="A box with the right name",
        martu=_QC_MARTU + (
            f"Make a box (a variable) with the exact name this step asks for, letter for letter. Any {what} "
            f"works.{gloss}\n"
            "Stuck? Skip this task, or practice in the lesson Boxes With Labels. Tasks you pass here stay done."
        ),
        example=ex_code,
        example_output=ex_out,
        names=[name],
        pick=pick,
        support="none",
        starter="# Make the box here:\n\n# Print it here:\n",
        checkpoints=[
            dict(
                id=f"make-{name.replace('_', '-')}",
                text=f"Under `# Make the box here:`, make a box named `{name}` that holds any {what}, in quotes.",
                dictated=False,
                hints=[
                    f"Start the line with `{name} = `.",
                    f"Find the word `{name}` in this step. That is the box's name, not the Example's.",
                    f"Write `{name} = \"{pick}\"` under `# Make the box here:`. The name has no quotes. "
                    f"The {what} in the quotes can be any you like.",
                ],
                checks=[box_check(name, foreign=foreign, lean=True), text_check(name), bare_check()],
            ),
            dict(
                id=f"print-{name.replace('_', '-')}",
                text=f"Under `# Print it here:`, print the box `{name}`, so the Console shows what is inside it.",
                dictated=True,
                hints=[
                    "Start the line with `print(`.",
                    f"The Example prints its box by name, with no quotes. Do the same with `{name}`.",
                    f"Write `print({name})` under `# Print it here:`. {QUOTES_RULE}",
                ],
                checks=[print_check(name)],
            ),
        ],
        solution=f'# Make the box here:\n{name} = "{pick}"\n# Print it here:\nprint({name})\n',
        partials=[f'{name} = "{pick}"\n'],
        assemble=dict(lines=[f'{name} = "{pick}"', f"print({name})"],
                      distractors=[f'{foreign[0]} = "{pick}"', f'print("{name}")']),
        another_way=[
            dict(angle="picture", text=f"```\n{name}   =   \"{wrong_value}\"\n name    gets   value\n```"),
            dict(angle="shorter", text=f"Name, `=`, value in quotes. Then `print({name})`."),
        ],
        takeaway=f"Use the step's exact name: `{name} = \"...\"`, then `print({name})`.",
        wrong_answers=[
            dict(why="the example's name", code=f'{foreign[0]} = "{wrong_value}"\nprint({foreign[0]})\n',
                 fails_at=1, message_contains="example"),
            dict(why="a lone value", code=f'"{wrong_value}"\nprint("{wrong_value}")\n', fails_at=1,
                 message_contains="no name in front"),
            dict(why="a box with another name", code=f'{other_name} = "{wrong_value}"\nprint({other_name})\n', fails_at=1,
                 message_contains="this step needs"),
            dict(why="text with no quotes", code=f"{name} = {wrong_value}\nprint({name})\n", fails_at=0,
                 message_contains=wrong_value),
            dict(why="def used to make a box", code=f'def {name} = "{wrong_value}"\nprint({name})\n', fails_at=0,
                 message_contains="expected"),
            dict(why="a capital letter", code=f'{name.capitalize()} = "{wrong_value}"\nprint({name.capitalize()})\n',
                 fails_at=1, message_contains="letter for letter"),
            dict(why="unclosed quote", code=f'{name} = "{wrong_value}\nprint({name})\n', fails_at=0,
                 message_contains="unterminated"),
            dict(why="print with quotes around the name", code=f'{name} = "{wrong_value}"\nprint("{name}")\n',
                 fails_at=2, message_contains="word"),
        ],
        notes=_qc_meta("make-variable,exact-names,quote-text", "2", ",".join(foreign), form) + "\n"
        "QC1 C1. Evidence: copying the example's name (A-05 to A-08) -> NAME/LEFT; a lone value (B-02, B-03) -> BARE; "
        "unquoted text (A-08, B-01) -> crash; def (A-02) -> crash. DF (Mar'tu's pick) is available.",
    )


# ---- C2: a total built from labeled boxes (combine-values) ----

def _c2(form, story, a, b, total_name, a_vals, b_vals, cases, total):
    """a, b = (count_name, price_name, what). a_vals, b_vals = (count, price)."""
    (ac, ap, aw), (bc, bp, bw) = a, b
    starter = (
        story
        + f"{ac} = 0    # how many?\n{ap} = 0    # how much is one?\n"
        + f"{bc} = 0    # how many?\n{bp} = 0    # how much is one?\n"
        + f"{total_name} = 0    # let the code combine it\nprint({total_name})\n"
    )
    filled = (
        story
        + f"{ac} = {a_vals[0]}    # how many?\n{ap} = {a_vals[1]}    # how much is one?\n"
        + f"{bc} = {b_vals[0]}    # how many?\n{bp} = {b_vals[1]}    # how much is one?\n"
    )
    formula = f"{ac} * {ap} + {bc} * {bp}"
    newbox = (
        "the total is in the right box",
        "import ast as _ast\n"
        "_made = [_t.id for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
        "for _t in _n.targets if type(_t).__name__ == 'Name']\n"
        f"_other = [_m for _m in _made if _m != {total_name!r} and globals().get(_m) == {total} and _m not in "
        f"{[ac, ap, bc, bp]!r}]\n"
        f"assert not ({total_name} == 0 and _other), 'Your new box `' + (_other or ['?'])[0] + '` holds {total}, "
        f"but `{total_name}` still holds 0.'\n"
        f"assert {total_name} != {ac} + {bc}, '`{total_name}` adds up how many of each thing, not what they cost.'\n"
        f"assert {total_name} == {total}, ('`{total_name}` still holds the placeholder 0.' if {total_name} == 0 else "
        f"'`{total_name}` holds ' + str({total_name}) + ', which is not the cost of everything in the story.')",
    )
    return dict(
        id="total-cost",
        title="Show your work: the total",
        martu=_QC_MARTU + (
            "The story is in the `#` notes at the top of your code. Put each of its numbers in its own box. "
            "Then let Python work out the total from the boxes: show your work, as in math class."
        ),
        names=[ac, ap, bc, bp, total_name],
        support="none",
        starter=starter,
        checkpoints=[
            dict(
                id="fill-the-boxes",
                text=(
                    "Replace the `0` in each of the four boxes with a number from the story, in the `#` notes at the "
                    "top. Ask each number: is it how many, or how much is one?"
                ),
                dictated=False,
                hints=[
                    f"Start with the first box: `{ac} = `.",
                    "Read the story again. For each number, ask: how many? or how much is one?",
                    "In '2 maps at 6 coins', 2 is how many and 6 is the price of one. Each 0 in your code is a "
                    "placeholder: replace it.",
                ],
                checks=[num_story_check(ac, ap, a_vals[0], a_vals[1], aw),
                        num_story_check(bc, bp, b_vals[0], b_vals[1], bw)],
            ),
            dict(
                id="combine",
                text=(
                    f"On the `{total_name} = 0` line, replace the `0` with math that works out the cost of everything. "
                    "Use the four box names, not numbers."
                ),
                dictated=False,
                hints=[
                    f"Start with `{total_name} = {ac} * `.",
                    f"Look at `{total_name} = 0`. Each thing costs how many times the price of one. Then add them.",
                    f"Write `{total_name} = {formula}` in place of `{total_name} = 0`. Python can do math with boxes.",
                ],
                checks=[newbox, cmb_check(total_name, cases)],
            ),
        ],
        solution=filled + f"{total_name} = {formula}\nprint({total_name})\n",
        partials=[filled + f"{total_name} = 0\nprint({total_name})\n"],
        assemble=dict(
            lines=[f"{ac} = {a_vals[0]}", f"{ap} = {a_vals[1]}", f"{bc} = {b_vals[0]}", f"{bp} = {b_vals[1]}",
                   f"{total_name} = {formula}", f"print({total_name})"],
            distractors=[f"{total_name} = {total}", f"{total_name} = {ac} + {bc}"],
        ),
        another_way=[
            dict(angle="everyday", label="An online cart",
                 text="Change how many you want and press Update: the cart works the total out again from how many "
                 "times the price. Run is your Update button, and your total should work like that."),
            dict(angle="shorter", text=f"`{total_name} = {formula}`"),
        ],
        takeaway="For each thing, how many × how much is one, then add. Write it with the box names and let Python do it.",
        wrong_answers=[
            dict(why="the total worked out by hand", code=filled + f"{total_name} = {total}\nprint({total_name})\n",
                 fails_at=2, message_contains="typed-in"),
            dict(why="the line totals typed in", code=filled + f"{total_name} = {a_vals[0] * a_vals[1]} + {b_vals[0] * b_vals[1]}\n"
                 f"print({total_name})\n", fails_at=2, message_contains="typed-in"),
            dict(why="the story's numbers typed into the formula",
                 code=filled + f"{total_name} = {a_vals[0]} * {a_vals[1]} + {b_vals[0]} * {b_vals[1]}\nprint({total_name})\n",
                 fails_at=2, message_contains="typed-in"),
            dict(why=f"{aw} count and price swapped",
                 code=story + f"{ac} = {a_vals[1]}\n{ap} = {a_vals[0]}\n{bc} = {b_vals[0]}\n{bp} = {b_vals[1]}\n"
                 f"{total_name} = {formula}\nprint({total_name})\n",
                 fails_at=1, message_contains="swapped"),
            dict(why=f"the line total in {bp}",
                 code=story + f"{ac} = {a_vals[0]}\n{ap} = {a_vals[1]}\n{bc} = {b_vals[0]}\n{bp} = {b_vals[0] * b_vals[1]}\n"
                 f"{total_name} = {formula}\nprint({total_name})\n",
                 fails_at=1, message_contains="already the cost"),
            dict(why="a number in quotes", code=filled.replace(f"{ac} = {a_vals[0]}", f'{ac} = "{a_vals[0]}"')
                 + f"{total_name} = 0\nprint({total_name})\n", fails_at=1, message_contains="quotes"),
            dict(why="a new box instead of the starter's", code=filled + f"{total_name} = 0\nmy_total = {formula}\nprint(my_total)\n",
                 fails_at=2, message_contains="still holds 0"),
            dict(why="counts added, no prices", code=filled + f"{total_name} = {ac} + {bc}\nprint({total_name})\n",
                 fails_at=2, message_contains="how many"),
        ],
        notes=_qc_meta("combine-values", "", "map_count,map_price,map_cost", form) + "\n"
        "QC1 C2. Evidence: everyone's 68 (A-05, A-07, A-08, B-01, B-02, B-03, A-01, A-06) -> CMB; the pizza swap "
        "(A-05, A-07, A-08) -> SWAP; line totals in price slots -> LINE-TOTAL; side-work boxes (G3) -> NEWBOX. "
        "The first thing in the story is given price-first (C9).",
    )


# ---- C3: a status line (combine-values, concat-str, reassign) ----

def _c3(form, who_name, who, affinity, cost_name, cost, aff_case, cost_case, line_case):
    max_mana = affinity * 2
    mana = max_mana - cost
    status = f"{who}: {mana}/{max_mana} mana"
    head = f'{who_name} = "{who}"\nmagical_affinity = {affinity}\n'
    starter = (
        head
        + "max_mana = 0        # twice the magical affinity\n"
        + "mana = max_mana     # starts full\n"
        + f"{cost_name} = {cost}\n"
        + "# Spend one spell here:\n\n"
        + f"# Print the status line here, like: {status}\n"
    )
    p1 = head + f"max_mana = magical_affinity * 2\nmana = max_mana\n{cost_name} = {cost}\n"
    p2 = p1 + f"mana = mana - {cost_name}\n"
    line = f'print({who_name} + ": " + str(mana) + "/" + str(max_mana) + " mana")'
    return dict(
        id="status-line",
        title="A status line",
        martu=_QC_MARTU + (
            "Magical affinity means how strong a hero's magic is. Max mana, the most mana a hero can hold, is twice "
            "the magical affinity. Spend one spell, then print a status line: one line with the hero's name and "
            "mana, like the stats text in a game."
        ),
        names=["max_mana", "mana", cost_name, who_name, "magical_affinity"],
        support="none",
        starter=starter,
        checkpoints=[
            dict(
                id="max-mana",
                text=(
                    "On the `max_mana = 0` line, replace the `0` with twice the magical affinity. Use the box name "
                    "`magical_affinity`, not a number."
                ),
                dictated=False,
                hints=[
                    "Start with `max_mana = magical_affinity`.",
                    "Look at `max_mana = 0`. Replace the 0 with math on `magical_affinity`.",
                    "Twice means times 2. Write `max_mana = magical_affinity * 2` in place of `max_mana = 0`.",
                ],
                checks=[cmb_check("max_mana", [({"magical_affinity": aff_case}, aff_case * 2)])],
            ),
            dict(
                id="spend",
                text=f"Under `# Spend one spell here:`, spend one spell: take `{cost_name}` away from what is in `mana`.",
                dictated=False,
                hints=[
                    "Start the line with `mana = mana - `.",
                    "Find `# Spend one spell here:`. Put the answer back in the same box.",
                    f"Read `=` as gets: mana gets mana minus the cost. Write `mana = mana - {cost_name}` under "
                    "`# Spend one spell here:`.",
                ],
                checks=[
                    (
                        "mana went down",
                        "assert mana != max_mana, '`mana` didn\\'t change, so no spell was spent.'\n"
                        f"assert mana != {cost_name} or mana == max_mana - {cost_name}, '`mana` holds only the cost now, "
                        "not what is left after the spell.'\n"
                        f"assert mana == max_mana - {cost_name}, '`mana` holds ' + str(mana) + ', but full mana minus one "
                        f"spell is ' + str(max_mana - {cost_name}) + '. Python reads top to bottom: look at what `max_mana` "
                        "held when the line `mana = max_mana` ran.'",
                    ),
                    cmb_check("mana", [({cost_name: cost_case}, max_mana - cost_case),
                                       ({"magical_affinity": aff_case}, aff_case * 2 - cost)]),
                ],
            ),
            dict(
                id="status",
                text=(
                    "Under `# Print the status line here`, print the status line from the boxes, glued with `+`, "
                    f"so it looks like `{status}`."
                ),
                dictated=False,
                hints=[
                    f"Start with `print({who_name} + \": \" + `.",
                    "Which parts come from boxes, and which are fixed words? Numbers need `str()` before `+` glues them. "
                    "The `\"/\"` is in quotes, so it is a slash, not divide.",
                    f"`+` glues text, and `str(7)` makes 7 into text. Write `{line}` under `# Print the status line here`.",
                ],
                checks=[
                    out_line_check(f"{who_name} + ': ' + str(mana) + '/' + str(max_mana) + ' mana'", "the status line",
                                   "Look for a missing space or colon."),
                    cmb_line_check([({who_name: "Tester", "magical_affinity": line_case},
                                     f"Tester: {line_case * 2 - cost}/{line_case * 2} mana")],
                                   label="the status line follows other values"),
                ],
            ),
        ],
        solution=p2 + line + "\n",
        partials=[p1, p2],
        assemble=dict(
            lines=[f'{who_name} = "{who}"', f"magical_affinity = {affinity}", "max_mana = magical_affinity * 2",
                   "mana = max_mana", f"{cost_name} = {cost}", f"mana = mana - {cost_name}", line],
            distractors=[f"max_mana = {max_mana}", f'print("{status}")',
                         f'print({who_name} + ": " + mana + "/" + max_mana + " mana")'],
        ),
        another_way=[
            dict(angle="step-by-step",
                 text="1. `max_mana` is the affinity times 2.\n2. `mana` gets `mana` minus the cost.\n"
                 "3. Glue: name, `\": \"`, `str(mana)`, `\"/\"`, `str(max_mana)`, `\" mana\"`. The `\"/\"` is in "
                 "quotes, so it is a slash, not divide."),
            dict(angle="shorter", text=f"`{line}`"),
        ],
        takeaway=(
            "Work out values from boxes, change a box with `mana = mana - cost`, and glue numbers into text "
            "with `str()`."
        ),
        wrong_answers=[
            dict(why="max_mana worked out by hand", code=head + f"max_mana = {max_mana}\nmana = max_mana\n{cost_name} = {cost}\n"
                 f"mana = mana - {cost_name}\n{line}\n", fails_at=1, message_contains=str(aff_case * 2)),
            dict(why="mana typed in", code=p1 + f"mana = {mana}\n{line}\n", fails_at=2, message_contains=str(max_mana - cost_case)),
            dict(why="the subtraction not put back", code=p1 + f"mana - {cost_name}\n{line}\n", fails_at=2,
                 message_contains="didn't change"),
            dict(why="the old dash advice followed: mana gets only the cost", code=p1 + f"mana = {cost_name}\n{line}\n",
                 fails_at=2, message_contains="only the cost"),
            dict(why="the spell cost typed as a number", code=p1 + f"mana = mana - {cost}\n{line}\n", fails_at=2,
                 message_contains=str(max_mana - cost_case)),
            dict(why="mana = max_mana runs before max_mana is worked out",
                 code=head + f"max_mana = 0\nmana = max_mana\nmax_mana = magical_affinity * 2\n{cost_name} = {cost}\n"
                 f"mana = mana - {cost_name}\n{line}\n", fails_at=2, message_contains="top to bottom"),
            dict(why="the status line typed in", code=p2 + f'print("{status}")\n', fails_at=3, message_contains="Tester"),
            dict(why="the numbers typed into the status line",
                 code=p2 + f'print({who_name} + ": {mana}/{max_mana} mana")\n', fails_at=3, message_contains="Tester"),
            dict(why="str() missing", code=p2 + f'print({who_name} + ": " + mana + "/" + max_mana + " mana")\n',
                 fails_at=0, message_contains="concatenate"),
            dict(why="spaces missing", code=p2 + f'print({who_name} + ":" + str(mana) + "/" + str(max_mana) + "mana")\n',
                 fails_at=3, message_contains="match up to"),
        ],
        notes=_qc_meta("combine-values,concat-str,reassign", "", "max_glow,glow,snack,sips", form) + "\n"
        "QC1 C3. The status line is checked against the student's OWN name box (any hero passes, lint e) and with "
        "a rerun (name Tester). Evidence: typed totals (68) -> CMB; `mana - cost` with no assignment (A-03/A-04 "
        "trace model) -> 'didn't change'; text plus a number -> crash.",
    )


# ---- C4: a bar for any mana (repeat-string) ----

def _c4(form, full, count_name, max_name, bar_name, count, maximum, label, cases):
    starter = (
        f'full = "{full}"\nempty = "░"\n{count_name} = {count}\n{max_name} = {maximum}\n'
        f'{bar_name} = ""    # full blocks for {count_name}, then empty blocks for the rest\n'
        f'print("{label} [" + {bar_name} + "]")\n'
    )
    good = f"{bar_name} = full * {count_name} + empty * ({max_name} - {count_name})"

    def code(line):
        return starter.replace(f'{bar_name} = ""    # full blocks for {count_name}, then empty blocks for the rest', line)

    return dict(
        id="mana-bar",
        title="A bar for any number",
        martu=_QC_MARTU + (
            "Draw a bar like a fuel gauge: full blocks for what is left, then empty blocks for what is used. "
            "It must work for any numbers."
        ),
        names=[bar_name],
        support="none",
        starter=starter,
        checkpoints=[
            dict(
                id="build-the-bar",
                text=(
                    f"Replace the `\"\"` in `{bar_name} = \"\"` with the bar: `full` repeated `{count_name}` times, "
                    f"then `empty` for the rest of `{max_name}`."
                ),
                dictated=False,
                hints=[
                    f"Start with `{bar_name} = full * {count_name} + `.",
                    f"How many empty blocks are there when `{count_name}` is {count} of {maximum}?",
                    f"Write `{good}` in place of `{bar_name} = \"\"`. PEMDAS: the parentheses make Python subtract "
                    "before it multiplies.",
                ],
                checks=[
                    (
                        "the bar has both parts",
                        f"_want = full * {count_name} + empty * ({max_name} - {count_name})\n"
                        f"assert {bar_name} != '', '`{bar_name}` is still empty: it holds the placeholder `\"\"`.'\n"
                        f"assert {bar_name} != full * {count_name}, '`{bar_name}` has the full blocks but no empty ones.'\n"
                        f"assert {bar_name} == _want, '`{bar_name}` holds \"' + str({bar_name}) + '\". With these numbers it should hold \"' + _want + '\".'",
                    ),
                    cmb_check(bar_name, cases),
                ],
            ),
        ],
        solution=code(good),
        assemble=dict(
            lines=[f'full = "{full}"', 'empty = "░"', f"{count_name} = {count}", f"{max_name} = {maximum}", good,
                   f'print("{label} [" + {bar_name} + "]")'],
            distractors=[f"{bar_name} = full * {count_name} + empty * {max_name} - {count_name}",
                         f"{bar_name} = full * {count_name} + empty * {maximum - count}"],
        ),
        another_way=[
            dict(angle="picture", label="A fuel gauge",
                 text="A gauge shows what is left and what is used. Left is `full * " + count_name + "`. "
                 "Used is `empty * (" + max_name + " - " + count_name + ")`."),
            dict(angle="shorter", text=f"`{good}`"),
        ],
        takeaway=(
            f"`\"█\" * 4` stamps 4 blocks. Put the subtraction in parentheses so it goes first: "
            f"`empty * ({max_name} - {count_name})`."
        ),
        wrong_answers=[
            dict(why="no brackets around the subtraction",
                 code=code(f"{bar_name} = full * {count_name} + empty * {max_name} - {count_name}"),
                 fails_at=0, message_contains="operand"),
            dict(why="the empty count typed in", code=code(f"{bar_name} = full * {count_name} + empty * {maximum - count}"),
                 fails_at=1, message_contains=count_name),
            dict(why="the bar typed in", code=code(f'{bar_name} = "{full * count + "░" * (maximum - count)}"'),
                 fails_at=1, message_contains="typed-in"),
            dict(why="the full part only", code=code(f"{bar_name} = full * {count_name}"), fails_at=1, message_contains="empty"),
        ],
        notes=_qc_meta("repeat-string", "", "", form) + "\n"
        "QC1 C4. Blocks pre-typed (G1 R8). Evidence: the campaign's `caster[\"max_mana\"] - caster[\"mana\"]` with no "
        "brackets -> crash; a hand-counted empty part -> CMB.",
    )


# ---- C5: fix three lines (quote-text, numbers-vs-text, exact-names, read-traceback) ----

def _c5(form, words, box, start, take, name_bad, name_good, value):
    starter = (
        f'print("{words})\n'
        f"{box} = {start}\n"
        f'{box} = {box} - "{take}"\n'
        f"{name_bad} = {value}\n"
        f"print({name_good})\n"
    )
    fixed = (
        f'print("{words}")\n'
        f"{box} = {start}\n"
        f"{box} = {box} - {take}\n"
        f"{name_good} = {value}\n"
        f"print({name_good})\n"
    )
    return dict(
        id="mend-three",
        title="Fix three mistakes",
        martu=_QC_MARTU + (
            "Three mistakes you've seen before, on three lines. When Python stops, read the title of the error box, "
            "then Python's last line. Find the line number, fix that line, and press Run again."
        ),
        names=[box, name_good],
        support="none",
        starter=starter,
        checkpoints=[
            dict(
                id="mend-the-quote",
                text=f"Fix line 1 so it shows `{words}` in the Console.",
                dictated=False,
                hints=[
                    "Look at the end of line 1, right before the `)`.",
                    "Quotes come in pairs: one before the words, one after.",
                    f"Type `\"` right after `{words}` on line 1. Line 1 becomes `print(\"{words}\")`.",
                ],
                checks=[("prints the words",
                         f"assert {words!r} in _lines(), {'Line 1 does not show exactly `' + words + '` yet.'!r}")],
            ),
            dict(
                id="mend-the-number",
                text=f"Fix line 3 so it takes the number {take} away from `{box}`.",
                dictated=False,
                hints=[
                    f"Look at the `\"{take}\"` on line 3.",
                    "Numbers have no quotes. With quotes, it is text, and Python can't take text away from a number.",
                    f"Delete the two `\"` around the {take} on line 3. Line 3 becomes `{box} = {box} - {take}`.",
                ],
                checks=[
                    (
                        f"{box} is {start - take}, worked out by Python",
                        f"assert type({box}).__name__ == 'int' and {box} == {start - take}, "
                        f"'`{box}` should hold {start - take}, which is {start} take away {take}.'\n"
                        "import ast as _ast\n"
                        "_done = [_n for _n in _ast.walk(_ast.parse(_source)) if (type(_n).__name__ == 'AugAssign' "
                        f"and type(_n.target).__name__ == 'Name' and _n.target.id == {box!r}) or (type(_n).__name__ == "
                        "'Assign' and type(_n.value).__name__ != 'Constant' and any(type(_t).__name__ == 'Name' and "
                        f"_t.id == {box!r} for _t in _n.targets))]\n"
                        f"assert _done, '`{box}` holds {start - take}, but the {start - take} is typed in, not worked out "
                        "by Python.'",
                    ),
                    cmb_check(box, [({box: start + 10}, start + 10 - take)],
                              tail=f"Line 3 does not take {take} away from `{box}` itself."),
                ],
            ),
            dict(
                id="mend-the-name",
                text=f"Fix line 4 so the box's name is `{name_good}`, to match line 5.",
                dictated=False,
                hints=[
                    f"Compare line 4 and line 5 letter by letter.",
                    "Names match letter for letter, capitals too. One capital letter makes a new name.",
                    f"On line 4, change `{name_bad}` to `{name_good}`. Line 4 becomes `{name_good} = {value}`.",
                ],
                checks=[
                    box_check(name_good, skip=[box], lean=True),
                    (f"no {name_bad} left over", f"assert {name_bad!r} not in globals(), '`{name_bad}` is still there, "
                     f"on its own line. To Python it is a different box from `{name_good}`.'"),
                    print_check(name_good),
                    ("the box is printed", f"assert {name_good} == {value} and {str(value)!r} in _lines(), "
                     f"'`{name_good}` should hold {value}, and line 5 should print it.'"),
                ],
                pass_line=(
                    "Mar'tu: Fixed. You skipped ahead, so here are my notes: the hours between bursts keep shrinking, "
                    "48, then 37. Bomb Shell thinks thirty-two, maybe less. The Night Watch Ledger is open whenever "
                    "you like."
                ),
            ),
        ],
        solution=fixed,
        assemble=dict(
            lines=fixed.strip().split("\n"),
            distractors=[f'print("{words})', f'{box} = {box} - "{take}"', f"{name_bad} = {value}"],
        ),
        another_way=[
            dict(angle="step-by-step",
                 text="1. Press Run.\n2. Read the title of the error box, then Python's last line.\n"
                 "3. Find the line number, and fix that one mistake.\n4. Press Run again."),
            dict(angle="shorter", text="Close the quote. Take the quotes off the number. Match the name letter for letter."),
        ],
        takeaway="Quotes come in pairs, numbers get no quotes, and names match letter for letter.",
        wrong_answers=[
            dict(why="the quote left open", code=starter, fails_at=0, message_contains="unterminated"),
            dict(why="the number left in quotes", code=fixed.replace(f"{box} - {take}", f'{box} - "{take}"'),
                 fails_at=0, message_contains="unsupported operand"),
            dict(why="the answer typed in", code=fixed.replace(f"{box} = {box} - {take}", f"{box} = {start - take}"),
                 fails_at=2, message_contains="typed in"),
            dict(why="a subtraction that does not start from the box",
                 code=fixed.replace(f"{box} = {box} - {take}", f"{box} = {start} - {take}"), fails_at=2, message_contains="itself"),
            dict(why="the wrong name left, with a new line for the right one",
                 code=fixed.replace(f"{name_good} = {value}\n", f"{name_bad} = {value}\n{name_good} = {value}\n"),
                 fails_at=3, message_contains="still there"),
            dict(why="the number typed into the print instead of the box",
                 code=fixed.replace(f"print({name_good})", f"print({value})"), fails_at=3, message_contains="never prints the box"),
            dict(why="the name mended on line 5 instead",
                 code=fixed.replace(f"{name_good} = {value}", f"{name_bad} = {value}").replace(f"print({name_good})", f"print({name_bad})"),
                 fails_at=3, message_contains=name_good),
            dict(why="the name left as it was", code=fixed.replace(f"{name_good} = {value}", f"{name_bad} = {value}"),
                 fails_at=0, message_contains="not defined"),
        ],
        notes=_qc_meta("quote-text,numbers-vs-text,exact-names,read-traceback", "", "glow", form) + "\n"
        "QC1 C5 (G4 R1 #6). Every slip crashes until it is mended, so no partials: a program with any slip left "
        "fails every checkpoint with the explainer, which is the read-the-traceback skill being tested. CP2 accepts "
        "`-=` and reruns with a bigger start (a subtraction that does not start from the box stays put); CP3 also "
        "fails a leftover wrong-case box and a typed number in the print. CP3's pass line carries the story for "
        "students who test out and skip 1P1: the bursts' gaps shrink (48 h, 37 h), Bomb Shell thinks 32, and the "
        "Night Watch Ledger is open.",
    )


QC1_A = dict(
    kind="testout",
    id="qc1-a",
    title="Quick Check 1 · Form A",
    optional=True,
    minutes=10,
    summary=(
        "Form A: five short tasks, no hints. Pass all five to test out of Unit 1: you show you know it, so you can "
        "skip its lessons. Stuck on one? The lessons teach all of it, and tasks you pass here stay done."
    ),
    exercises=[
        _c1("A", "party_leader", "hero", ["guide"], 'guide = "Gearshift"\nprint(guide)\n', "Gearshift", "Captain Glug"),
        _c2(
            "A",
            "# Bandages cost 2 coins each, and Oogrish needs 7.\n# Torches: Oogrish needs 3, at 5 coins each.\n",
            ("bandage_count", "bandage_price", "bandages"),
            ("torch_count", "torch_price", "torches"),
            "total_cost",
            (7, 2),
            (3, 5),
            [({"torch_count": 8}, 54), ({"bandage_price": 3}, 36), ({"bandage_count": 1, "torch_price": 6}, 20)],
            29,
        ),
        _c3("A", "scout_name", "Gearshift", 10, "spell_cost", 6, 13, 5, 13),
        _c4("A", "█", "shield", "max_shield", "shield_bar", 4, 7, "Shield",
            [({"shield": 0}, "░" * 7), ({"shield": 7}, "█" * 7), ({"shield": 2, "max_shield": 5}, "██░░░")]),
        _c5("A", "The fire is low.", "stamina", 15, 4, "Max_Stamina", "max_stamina", 16),
    ],
    notes=(
        "Reconciler pass: every lean message here mirrors the lesson's message for the same mistake, minus the fix "
        "(box_check, print_check, num_story_check and the reruns use the lesson's sentences: 'Your box is named "
        "`x`, but this step needs `y`', '`total_cost` has a typed-in number. Mar'tu tested your code with ...'), "
        "and a rerun that stops says what stopped it in plain words (_plain, S8). Task 5 says Fix, not Mend (the "
        "site reads both, S1). "
        "Quick Check 1, form A (code tasks). Questions live in qc1-a-questions. Pass = every code task plus 2 of the "
        "3 questions; a retake draws form B. The site currently gates on the code tasks only; question scoring joins "
        "when QC scoring ships. Form A uses names and numbers no lesson uses, so it can't be passed from memory: "
        "party_leader (example: guide), bandages 7 x 2 + torches 3 x 5 = 29 for Oogrish, scout Gearshift 10 -> "
        "14/20 mana, the Shield bar 4 of 7, and 'The fire is low.' / stamina 15 - 4 / Max_Stamina. "
        "Coverage (lint d): make-variable, exact-names, quote-text -> C1 "
        "(WA: example's name, lone value, unquoted text) and C5; combine-values -> C2, C3 (WA: typed totals); "
        "concat-str -> C3 (WA: typed line, str missing); reassign -> C3 (WA: mana typed, subtraction not put back) "
        "and Q2; repeat-string -> C4 (WA: no brackets, typed gap) and Q1; numbers-vs-text -> C2, C5; read-traceback "
        "-> C5. support='none' everywhere: no hints, tracer or compare; glossary, read-aloud, DF and the explainer "
        "stay on."
    ),
)

QC1_B = dict(
    kind="testout",
    id="qc1-b",
    title="Quick Check 1 · Form B",
    optional=True,
    minutes=10,
    summary=(
        "Form B: the same skills as Form A with different tasks, for a second try. Five short tasks, no hints. "
        "Pass all five to test out of Unit 1. Tasks you pass here stay done."
    ),
    exercises=[
        _c1("B", "familiar", "creature", ["steed"], 'steed = "a brass jeep"\nprint(steed)\n', "a brass jeep",
            "a glowing newt", wrong_value="Kratos", other_name="pet"),
        _c2(
            "B",
            "# Candles cost 3 coins each, and Mar'tu needs 4.\n# Oil: Mar'tu needs 2 flasks, at 6 coins a flask.\n",
            ("candle_count", "candle_price", "candles"),
            ("oil_count", "oil_price", "flasks"),
            "supply_cost",
            (4, 3),
            (2, 6),
            [({"oil_count": 5}, 42), ({"candle_price": 1}, 16), ({"candle_count": 10, "oil_price": 2}, 34)],
            24,
        ),
        _c3("B", "caster_name", "Bomb Shell", 12, "shield_cost", 5, 7, 2, 7),
        _c4("B", "▓", "sips", "max_sips", "meter", 2, 6, "Glug",
            [({"sips": 0}, "░░░░░░"), ({"sips": 6}, "▓▓▓▓▓▓"), ({"sips": 1, "max_sips": 4}, "▓░░░")]),
        _c5("B", "Barrier's holding.", "shield", 24, 5, "Glug_Sips", "glug_sips", 4),
    ],
    notes=(
        "Quick Check 1, form B: every name and value changes (familiar, candles and oil, Bomb Shell's 12 -> 24, the "
        "▓ glug meter, Barrier's holding.). The stat names magical_affinity, max_mana and mana stay, because they "
        "are the campaign's own names. Same coverage as form A. Questions live in qc1-b-questions. Pass = every code "
        "task plus 2 of the 3 questions. The site currently gates on the code tasks only; question scoring joins "
        "when QC scoring ships."
    ),
)

QC1_A_QUESTIONS = dict(
    kind="quiz",
    id="qc1-a-questions",
    title="Quick Check 1 · Form A questions",
    optional=True,
    minutes=3,
    summary="Three questions to check yourself. They don't decide whether you test out.",
    questions=[
        dict(
            type="mc",
            id="read-the-bar",
            q="What does this line show in the Console?",
            code='print("Mana [" + "█" * 3 + "░" * 2 + "] " + str(3) + "/" + str(5))\n',
            choices=["Mana [███░░] 3/5", "Mana [███░░]3/5", "Mana [█3░2] 3/5", "Mana [█░] 3/5"],
            answer=0,
            why_wrong={
                1: "Look at `\"] \"`: there is a space after the `]`, and spaces are text too.",
                2: "`*` stamps the block 3 times. It does not glue the number on.",
                3: "`\"█\" * 3` is three blocks, not one.",
            },
            explain="`*` stamps: 3 full blocks, 2 empty ones. `\"] \"` adds the `]` and a space. `str()` turns 3 and 5 into text, so `+` can glue them.",
            notes="Skills repeat-string, concat-str (reading). G4 R26. Distractors: the missing space, `█3░2`, one stamp.",
        ),
        dict(
            type="predict",
            id="change-the-box",
            q="What does this code print?",
            code="x = 5\nx = x - 2\nprint(x)\n",
            answer="3",
            choices=["3", "5\n2", "7", "5"],
            explain=(
                "In math, x = x − 2 has no answer, but in Python `=` means gets. Line 2 works out 5 − 2 with what is "
                "in `x` now, then puts 3 back in `x`. A box keeps only its latest value."
            ),
            notes="Skill reassign. Distractors: both values stay (A-03/A-04 trace model), added instead (7), first value only.",
        ),
        dict(
            type="mc",
            id="which-name",
            q="Which line makes a box whose name Python accepts?",
            choices=["magical affinity = 9", "magical_affinity = 9", '"magical_affinity" = 9'],
            answer=1,
            why_wrong={
                0: "A name can't have a space. Python reads two names and stops. Use `_` instead.",
                2: "A box's name never has quotes. Quotes make it text, and text can't be a name.",
            },
            explain="Names have no spaces and no quotes: `magical_affinity = 9`.",
            notes="Skill exact-names. Evidence: A-06 `total pizzaparty`; A-02 `def (\"character\")` name-in-quotes.",
        ),
    ],
    notes=(
        "Quick Check 1, form A questions (scored with qc1-a: every code task plus 2 of the 3 questions). The site "
        "currently gates on the code tasks only; question scoring joins when QC scoring ships. No hints; read-aloud "
        "and glossary stay on."
    ),
)

QC1_B_QUESTIONS = dict(
    kind="quiz",
    id="qc1-b-questions",
    title="Quick Check 1 · Form B questions",
    optional=True,
    minutes=3,
    summary="Three questions to check yourself. They don't decide whether you test out.",
    questions=[
        dict(
            type="mc",
            id="read-the-bar",
            q="What does this line show in the Console?",
            code='print("Glug [" + "▓" * 2 + "░" * 4 + "] " + str(2) + "/" + str(6))\n',
            choices=["Glug [▓▓░░░░] 2/6", "Glug [▓▓░░░░]2/6", "Glug [▓2░4] 2/6", "Glug [▓░] 2/6"],
            answer=0,
            why_wrong={
                1: "Look at `\"] \"`: there is a space after the `]`, and spaces are text too.",
                2: "`*` stamps the block 2 times. It does not glue the number on.",
                3: "`\"▓\" * 2` is two blocks, not one.",
            },
            explain="`*` stamps: 2 full blocks, 4 empty ones. `\"] \"` adds the `]` and a space. `str()` turns 2 and 6 into text, so `+` can glue them.",
            notes="Form B of read-the-bar.",
        ),
        dict(
            type="predict",
            id="change-the-box",
            q="What does this code print?",
            code="y = 8\ny = y - 3\nprint(y)\n",
            answer="5",
            choices=["5", "8\n3", "11", "8"],
            explain=(
                "In math, y = y − 3 has no answer, but in Python `=` means gets. Line 2 works out 8 − 3 with what is "
                "in `y` now, then puts 5 back in `y`. A box keeps only its latest value."
            ),
            notes="Form B of change-the-box.",
        ),
        dict(
            type="mc",
            id="which-name",
            q="Which line makes a box whose name Python accepts?",
            choices=['spell color = "teal"', 'spell_color = "teal"', '"spell_color" = "teal"'],
            answer=1,
            why_wrong={
                0: "A name can't have a space. Python reads two names and stops. Use `_` instead.",
                2: "A box's name never has quotes. Quotes make it text, and text can't be a name.",
            },
            explain="Names have no spaces and no quotes: `spell_color = \"teal\"`. The value can have quotes. The name can't.",
            notes="Form B of which-name.",
        ),
    ],
    notes=(
        "Quick Check 1, form B questions (scored with qc1-b: every code task plus 2 of the 3 questions). The site "
        "currently gates on the code tasks only; question scoring joins when QC scoring ships."
    ),
)


# =============================================================================================
# Cheatsheet 1 "Mar'tu's Chalk Notes: First Words"
# =============================================================================================

CHALK_NOTES = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: First Words",
    summary="Everything from Unit 1 on one page. Printable.",
    entries=[
        dict(concept="Show words: `print`", code='print("Shield up.")\n', output="Shield up.",
             note="`print` shows text on the screen, in the Console. Quotes and parentheses come in pairs: one opens, "
             "one closes. (Lesson: Words in Quotes)"),
        dict(concept="A blank line", code='print("Steady, now.")\nprint()\nprint("Barrier\'s holding.")\n',
             output="Steady, now.\n\nBarrier's holding.", note="`print()` with nothing inside prints an empty line."),
        dict(concept="Notes for people: `#`", code="# Lucky's lines for tonight\n# print(\"Not this one.\")\nprint(\"Fine.\")\n",
             output="Fine.", note="A line that starts with `#` is a note for people (a comment), like a stage direction in a "
             "play. Python skips it, so a `#` in front of a line switches that line off."),
        dict(concept="A box: `name = value`", code='companion = "Gearshift"\nprint(companion)\nprint("companion")\n',
             output="Gearshift\ncompanion",
             note="Read `=` as gets: companion gets Gearshift. A box's name never has quotes. " + QUOTES_RULE
             + " (Lesson: Boxes With Labels)"),
        dict(concept="Numbers don't get quotes", code="armor_bonus = 3\nprint(armor_bonus + 2)\n", output="5",
             note="A number gets no quotes, so Python can do math with it. `\"3\"` in quotes is text, like the 3 on a "
             "jersey: nobody adds two jerseys."),
        dict(concept="Change a box", code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nprint(mana)\n", output="23",
             note="Read it as: mana gets mana minus spell cost. In math, x = x − 3 has no answer, but Python works out the "
             "right side first, then puts the answer back in the box."),
        dict(concept="Math: `+ - * /`", code="print(46 + 2)\nprint(48 - 37)\nprint(9 * 2)\nprint(48 / 2)\n",
             output="48\n11\n18\n24.0", note="`*` means times (there's no × key) and `/` means divided by. `/` always gives "
             "a decimal, like `24.0`. (Lesson: Math and Glue)"),
        dict(concept="How many × how much is one",
             code="lantern_count = 3\nlantern_price = 4\nlantern_cost = lantern_count * lantern_price\nprint(lantern_cost)\n",
             output="12",
             note="Put each number in a named box. Then write the math with the box names, like a formula in math class. "
             "Change a number and press Run again: the total changes to match. Never type the total in yourself."),
        dict(concept="Glue text: `+` and `str()`", code='mana = 7\nprint("Mana: " + str(mana))\n', output="Mana: 7",
             note="`+` glues text to text, like a compound word: sun + flower is sunflower. A number must become text "
             "first, with `str()`, short for string (text). Spaces are text too."),
        dict(concept="Stamp a mark: `*`", code='print("█" * 3 + "░" * 2)\n', output="███░░",
             note="`*` stamps one text a number of times, like repeated addition: `\"█\" * 3` is `\"█\" + \"█\" + \"█\"`."),
        dict(concept="Parentheses for the gap", code='mana = 3\nmax_mana = 5\nprint("░" * (max_mana - mana))\n', output="░░",
             note="PEMDAS, as in math class: Python does `*` before `-`, so put the subtraction in parentheses."),
        dict(concept="Error: an unclosed quote", code='print("Shield up.)\n',
             note="When Python stops, read the error box's title, then Python's last line, then fix the line with "
             "that number. Here Python's last line is `SyntaxError: unterminated string literal`. Syntax means how a "
             "line is put together, like grammar. Some text in quotes never closes. Add the missing quote."),
        dict(concept="Error: a missing closing parenthesis", code='print("Shield up."\n',
             note="Python's last line: `SyntaxError: '(' was never closed`. A `(` has no `)` to match it. "
             "Add the missing `)`."),
        dict(concept="Error: a name it doesn't know", code="Max_Mana = 18\nprint(max_mana)\n",
             note="Python's last line: `NameError: name 'max_mana' is not defined`. Python has no box with that exact "
             "name. Names match letter for letter, capitals too."),
        dict(concept="Error: a space in a name", code="magical affinity = 9\n",
             note="Python's last line: `SyntaxError: invalid syntax`. Python can't read the line, because a name can't "
             "have a space. Use `_` instead: `magical_affinity`."),
        dict(concept="Error: text plus a number", code='print("Mana: " + 7)\n',
             note="Python's last line: `TypeError: can only concatenate str (not \"int\") to str`. Concatenate means "
             "glue, str means text and int means a whole number: you can only glue text to text. Use `str(7)`."),
        dict(concept="Error: `def` to make a box", code='def character = "Zelda"\n',
             note="Python's last line starts with `SyntaxError`. `def` is for something you'll learn in Unit 3. To make "
             "a box, write the name, `=`, then the value: `character = \"Zelda\"`."),
        dict(concept="(extra) Many lines at once", code='print("""Glug canteen: half full.\nSmell: still terrible.""")\n',
             output="Glug canteen: half full.\nSmell: still terrible.",
             note="Three quote marks start text that can go over many lines, and three more end it. It is not a `#` "
             "note: Python prints it. (Extra practice: Many lines at once)"),
        dict(concept="(extra) The short way: `+=` and `-=`", code="mana = 26\nmana -= 3\nmana += 1\nprint(mana)\n", output="24",
             note="`mana -= 3` is short for `mana = mana - 3`. (Extra practice: The short way)"),
        dict(concept="(extra) Clock math: `%`, `//`, `**`", code="print((9 + 50) % 12)\nprint(50 // 12)\nprint(2 ** 3)\n",
             output="11\n4\n8", note="In 50 ÷ 12 = 4 R 2, `//` gives the 4 and `%` gives the 2. Here `%` is not "
             "percent. `**` is a power: `2 ** 3` is 8. (Article: Clock Math)"),
        dict(concept="(extra) Asking: `input()`", code='sips = int(input("How many sips? "))\nprint(sips * 2)\n',
             note="`input()` always hands back text. `int()` makes it a number: `int` is short for integer, a whole "
             "number. (Article: Asking the Traveler)"),
    ],
    notes="Cheatsheet 1 (spec items in order, then the extras). Entries with `output` are run and checked by the harness.",
)


ITEMS = [WARD_SIGN, CLOCK_MATH, ASKING_THE_TRAVELER, QC1_A, QC1_A_QUESTIONS, QC1_B, QC1_B_QUESTIONS, CHALK_NOTES]
