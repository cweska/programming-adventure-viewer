"""Unit 10 "Campaign Readiness Check" ("Before We Continue"), part a, in the order students meet it: the intro card,
Part 1 form A (the 13 unaided items of curriculum 5.3: first the quiz rc-part1-a-questions with the 12 questions of
the 9 predict / mc / explain items, so the first win is a prediction, then the testout rc-part1-a with its 9 code
tasks), Mar'tu's Notes: Where to Look Again (rc-review, the review routing of 5.2 / 5.5, right after Part 1 so a
student who misses something finds the way back), mini-boss A "Hold the Lantern Ward" (rc-miniboss-a, campaign mode
for everyone, 5.4) and the one-click "Explain a line you wrote" (rc-explain, 5.2). Core time: 2 + 10 + 18 + 15 + 1 =
46 minutes, inside the ~60-minute budget; rc-review (15) is optional, for a miss.

Spec: design/curriculum.md "## Unit 10" and "# 5. Campaign Readiness Check" (5.1 to 5.5), with the teacher's
decisions (design/teacher-decisions.md). Introduces nothing (concept_map.json plans nothing for u10a). Independent of
Strings (T1): no code a student sees uses a Unit 9 token (const:escape, attr:upper, attr:title, attr:split,
attr:join, attr:strip, attr:replace, attr:find, node:FString), and no optional-only token either (tuples, zip,
comprehensions, .items(), defaults, keyword arguments, lambda, map, match, assert, input, int, **, %, //). Proved
two ways: a scan of every visible code field with the harness's own tokenizer, and a harness run on a copy of the
staging folder whose concept_map.json plans nothing for u08 / u09 (0 errors; a control `.upper()` is rejected).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN `move_left()`,
`present_dialogue_option()` with `.lower().capitalize()`, the four dialogue options, `perform_roll(die_size)` and
`return roll >= required_roll`, `add_spell(...)`, the mana bars and `cast_spell` holding the barrier. This check is
"you've seen this, now show me you get it", practice only, never a grade (Q9). Every student has their own device and
does every item alone: no pair talk here (the evidence must be each student's own), and no step is shared.

How the parts are represented with the schema's existing fields (no new fields; what the site still lacks is in
the handback report and in each item's notes):
  * Part 1 is unaided: the testout's exercises are support="none" (the player forces it in testout mode: no hints,
    Another way, Assemble it, tracer, predict or Compare) and explainer="lean". The glossary and read-aloud stay on.
    Their hints exist only because the schema needs two; they never hold a finished line. No assemble, no
    another_way. Every typed task is behavior-checked with other values (CMB, PAR, BND, CALL, RND), never OUT alone.
    Check messages are lean: the slip and the evidence, never the fix (as QC2, QC-R1 and QC-R2), in words the class
    reads correctly ("holds a typed 24", "`None`, Python's word for nothing"). rc-part1-a is the required form
    (optional=False, the only required testout in the course): the site's Readiness flow should list it as a core
    item and never test the unit out with it (site request).
  * The 12 questions (items 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, 10a, 10b) are the quiz rc-part1-a-questions,
    listed before the testout (the harness and the exporter find `<id>-questions` anywhere in the unit);
    questions_to_pass=10 on the testout approximates "Part 1 >= 11/13" (every code task is required by the
    testout; two question misses allowed). Each question's notes give its item, skill tags and the campaign part it
    prepares (5.3). i4b (the ledger shape) is typed, with no choices, as in forms B and C (honest tracing).
  * rc-review is an article (optional): one line per Part 1 item, starting with the titles students saw in each
    form (task titles, and the questions by number), with a "Start here" lesson (the item's first route), the other
    lessons to open (Also), and the twins of forms B and C by title. ROUTES lives here; u10c keeps an identical copy
    for its `review=` meta.
  * Part 2, the mini-boss, is a project with support="light", solo=True (every student alone; solo also turns off
    Start me off and the Learn-pane Another way) and explainer="lean" (the teacher's ruling for SOLO items; closest
    to the campaign's shorter messages). No assemble, no tracer, no predict. Hints are capped at rung 2 by writing:
    each checkpoint's ladder is Where to look + two Teach rungs, and the last rung (which the site labels "Show me
    how") is written at teach level with no finished line. The comments are numbered in check order, and the intro
    and the starter both say so. Compare with Mar'tu's version should open after 5 minutes only (site request; the
    course setting also opens it after 4 counted failed runs today).
  * rc-explain is a one-question quiz about the mini-boss's pay line, `hero["mana"] = hero["mana"] - ward["mana_cost"]`
    (the class-wide combine-values gap; i9a already covers `ward["effect"](hero)`'s shape).

Check codes (curriculum 2.5), built from one helper prelude (_RX). check() puts in front of each check only the
helpers it uses (as u07a / u07c do). Every call a check makes uses fresh values the task never uses (lint b), with
prints kept private; nothing a check does shows in the console:
  NAME/DEF  _FN_OK: a function made with `def`, its exact name (near misses, the Example's name, a variable made with
           `=`), its exact parameters in order. Lean wording, never the `def` line.
  CALL     _STEP: the scout recorder (setup) moves once, in the function's direction, only when it is called.
           _BOARD: the ley board recorder gets the helper's line once (a line handed back to the caller is named);
           _ANSWER: oogrish_says() records each reply.
  CMB      _rerun() runs the program again in a fresh namespace (setup first, prints private) with a line slipped in
           right after the statement that makes a name: another sheet in `hero` / `sheet`, another `spell_name`,
           other mana numbers, another list of costs. A typed value cannot follow, and is named as "`mana` holds a
           typed 24. Mar'tu's check put another sheet in `hero`, and `mana` still said 24." _BOARD also swaps the
           helper for one that hands back another line.
  STO      _STO: inside present_warning, the helper's result is stored in a variable and that variable is passed on.
  KEEP     the finished helpers (`get_warning`, the mini-boss's `show_mana`) are unchanged (AST compare). The
           mini-boss's given guard is behavior-checked in CP1 (a ward the hero doesn't know is still turned away).
  KEY      _BOOK: the page is stored under the name in `spell_name` (a quoted variable name, a typed key, a rebuilt
           book that loses its first page, a value that is not the page are each named).
  RND      _ROLL: `random.randint` swapped for a scripted die that records its arguments; sizes 8 and 12.
  PAR / PAR-CONST / RET / PNM / RNM  _RET: glug_cost called with (5, 4) and (7, 6); print for return, no return,
           the same answer twice (the numbers typed in the function), a typed number with a parameter never read
           (`sips * 3`), a parameter handed back as it came in, text, a near-miss parameter, the Example's `result`.
  BND      the mini-boss casts for fresh heroes at need - 1, need, need + 1, mana below, at and above the cost; CP4
           also needs two different messages for the two reasons (form B's check).
Evidence (plain-language pass, guide 4.3): Part 1 ends a message with a labelled test, "Mar'tu tested your code: he
called ..., and ...", and a typed value reads "`mana` holds a typed-in 24. Mar'tu tested your code with a test sheet
in `hero`, ..."; the mini-boss ends it with short sentences built from the cast (_test), never brackets: "Mar'tu
tested your code with a made-up hero and ward: Brakka has affinity 12 and mana 5. Moon Step costs 5 and needs
affinity 7. Brakka was turned away." Messages use invented Tor names only in check data (Pell, Brakka, Moss, Moon Step, Frost
Veil) and the party's real values; a student's own text is never repeated back (text shows as "some text").

The class's slips, each proven by a wrong_answers entry (in the task named):
  * typed values instead of reading or handing over (CMB): C2 (a typed board line), C4 (24, 8, the key "Glow"), C5
    (7 typed blocks, `10 - 3`, a typed 10 or a typed 3), C7 (7, 14, 9 typed, a typed 3 added each time round), C8
    (`hero["mana"] = 17`, a typed cost, a typed start), C9 (`return 12`, one call's numbers, `sips * 3`, `sips * 4`,
    `4 * price_per_sip`, `sips + 3`), the mini-boss (a typed cost, a typed result, typed numbers in the tests, a
    typed hero name, a typed ward name or Gearshift's page);
  * print instead of return: C6 (print the roll), C9 (and a print after a stored total), C2 (the line handed back, not
    shown); = vs ==: C3, C2, C4 (c), C8; > vs >= at the boundary: the mini-boss CP3/CP5 (`<=`) and question i4a;
    unquoted text: C1 (`west`), C3 (`option 3`, `option_3`); quoted names (KEY): C4 (`book["spell_name"]`), C2
    (`show_on_ley_board("words")`, the call in quotes), C6 (`"die_size"`), C7 line 7 (`str("mana")`), C9 (`return
    "total"`); a missing colon: C3, C9, the mini-boss; a missing indent: C1 (the scout line at the edge), C2 (the
    second line), the mini-boss (cast lines not under `else:`, the cost paid outside it); def vs =: C9 (`def
    glug_cost = ...`, `glug_cost = 12`), C2 (`def words = ...`); calling vs handing over (): C2 (no `()` on the
    helper), the mini-boss (the effect read, never called; `show_mana` with no `()`; `ward_name["effect"](hero)`,
    the name read as the page), questions i9a / i9b; skipping a nesting level: C4 (`hero["wisdom"]`), C7 line 6
    (also a dexterity key typed onto the top of the sheet), the mini-boss (`hero["magical_affinity"]`); str() before
    +: C7 line 7 (and the comma's extra space); parentheses in "░" * (10 - 3): C5; resetting a total inside a loop:
    C7 line 11 (`total = 0` moved into the loop); approximate names: C9 (`price`), C4 (`Mana`); editing a helper you
    were told to leave alone: C2 (`get_warning`), the mini-boss (`show_mana`, and the given guard's `return`); one
    message for two reasons: the mini-boss CP4 (the affinity print copied into the `elif`).

Phone width: starters, examples, question code and fenced pictures (the hint ladders' too) keep to 36 characters,
except the campaign's own guard in the mini-boss starter (`if ward_name not in hero["wards"]:` and its print line),
as Units 5 and 7 did. The mini-boss's solution lines (the nested affinity test, the subtraction) are the campaign's
shapes too, and rc-explain shows the subtraction, the pay line (47 characters), as the same solution-line exception.
Checked by script.

Python's messages were checked in CPython 3.13 (the site runs 3.13): `elif choice == option 3:` -> "invalid syntax";
`if choice = "option 3":` -> "invalid syntax. Maybe you meant '==' or ':=' instead of '='?"; a missing colon ->
"expected ':'"; `"░" * max_mana - mana` -> "unsupported operand type(s) for -: 'str' and 'int'"; `sheet["dexterity"]`
-> KeyError: 'dexterity'; `"Mana: " + 14` -> "can only concatenate str (not "int") to str"; `mana_cots` -> "name
'mana_cots' is not defined"; `def glug_cost = 12` -> "expected '('"; `random.randint(die_size)` -> "missing 1
required positional argument: 'b'"; `ward_name["effect"]` -> "string indices must be integers, not 'str'".

Unit 10 reconciliation (one voice for u10a, u10b and u10c, and the words live Units 1-5 use; words only, checked
by script: every code field, id, order and Start me off span is unchanged, and every check's AST with its strings
blanked is unchanged):
  * Debugging steps and titles say "Fix" (live Units 1-5; the site reads Fix or Mend), so "*Mend* means fix." is
    gone. Titles: "Store, then pass it on", "Fix the reply", "Fix the bar" / "Fix the gauge", "Fix three mistakes"
    (rc-review's _TASKS map says the same; ROUTES item 11 reads "read the error box, then fix the line", in u10a
    and in u10c's copy).
  * "hands back" / "handed back" became "hands back" / "handed back" (guide 5.2; live Units 3-5) in prose and messages.
  * An `if` asks a "question" (guide 5.2). A Part 1 exercise is a "task"; a project's checkpoints are "tasks".
  * Evidence always starts "Mar'tu tested your code": "...: he called ...", "... with a test sheet / test number /
    test cost / test name ...", the mini-bosses "... with a made-up hero and ward: ...". Python's own words read
    "Python stopped with the error ...". Data the check made up is a "test sheet", names are "made-up".
  * One analogy per idea, the same in every form: a blank recipe card (`pass`), a basketball pass (store, then pass
    it on), a grading scale (the chain), the glossary and a table of contents (sheets), 3 × 4 = 4 + 4 + 4 (repeated
    text), PEMDAS, a fair die, a teacher's note in the margin (the error box), a password (names), a bank balance,
    area = length × width and Mad Libs (a function from its goal), f(3) (a function stored in a dictionary), a
    teacher calling roll (a loop over sheets), Google Docs' sentence case (`.capitalize()`).

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u10a
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
M1 = "leylines-awaken"
M2 = "friends-in-low-places"


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def fill(template, **values):
    """Check code from a template: each __NAME__ token becomes repr(value) (a message, a number, a list)."""
    out = template
    for key, value in values.items():
        out = out.replace("__" + key.upper() + "__", repr(value))
    return out


# ---------------------------------------------------------------------------------------------
# Check helpers (plain Python, run in the student's namespace after their code). check() puts in front of each
# check only the helpers it uses, and the helpers those use, so the unit JSON stays small (as u07a / u07c do).
# ---------------------------------------------------------------------------------------------

_RX = r'''import ast as _ast
import io as _io
import random as _random
import sys as _sys
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__
_SETUP = __SETUP__


def _show(_v):
    # A value in a message: numbers and code names only, never a student's own words (2.11).
    if _v is None:
        return '`None`'
    _t = type(_v).__name__
    if _t == 'function':
        return 'the function `' + _v.__name__ + '`'
    if _t in ('int', 'float', 'bool'):
        return '`' + str(_v) + '`'
    if _t == 'str':
        return 'some text'
    return {'dict': 'a dictionary', 'list': 'a list'}.get(_t, 'a ' + _t)


def _num(_v):
    # A number as it is (evidence), anything else as _show says.
    return str(_v) if type(_v).__name__ in ('int', 'float') else _show(_v)


def _ev(_what, _said=''):
    return " Mar'tu tested your code: he " + _what + ((', and ' + _said) if _said else '') + '.'


def _err(_e):
    return type(_e).__name__ + (': ' + str(_e) if str(_e) else '')


def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b):
    # A near miss for a name: case, a plural, 1-2 edits, a shared word, or one inside the other.
    if type(_a).__name__ != 'str' or type(_b).__name__ != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower(), _b.lower()
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    if min(len(_la), len(_lb)) >= 3 and _edits(_la, _lb) <= 2:
        return True
    _wa = set(_w for _w in _la.split('_') if len(_w) >= 4)
    _wb = set(_w for _w in _lb.split('_') if len(_w) >= 4)
    return bool(_wa & _wb) or (len(_la) >= 4 and (_la in _lb or _lb in _la))


def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    if not _q:
        return 'nothing'
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _many(_n, _word):
    return ('no ' + _word + 's') if _n == 0 else ('1 ' + _word if _n == 1 else str(_n) + ' ' + _word + 's')


def _defs():
    return {_n.name: _n for _n in _tree.body if type(_n).__name__ == 'FunctionDef'}


def _top():
    return [_n for _n in _tree.body if type(_n).__name__ != 'FunctionDef']


def _is_call(_n, _name):
    return type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == _name


def _calls_in(_nodes, _name):
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if _is_call(_c, _name)]


def _made_by(_n):
    # The names a statement makes with `=`, `+=` or `def`.
    _k = type(_n).__name__
    if _k in ('FunctionDef', 'ClassDef'):
        return [_n.name]
    _ts = list(_n.targets) if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'AnnAssign') else [])
    return [_t.id for _t in _ts if type(_t).__name__ == 'Name']


def _locals_of(_d):
    # The variables a function makes inside itself (not its parameters).
    _out = []
    for _n in _ast.walk(_d):
        for _x in (_made_by(_n) if _n is not _d else []):
            if _x not in _out:
                _out.append(_x)
    return _out


def _arg(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)


def _sig(_fn, _args):
    return '`' + _fn + '(' + ', '.join(_arg(_a) for _a in _args) + ')`'


def _call(_f, _args=()):
    # Call _f with its prints kept private. Returns (value, printed lines, error or None).
    _buf = _io.StringIO()
    _keep_out = _sys.stdout
    _sys.stdout = _buf
    _val, _e = None, None
    try:
        _val = _f(*_args)
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _e


def _keep(_name, _orig):
    # KEEP: '' when the function is exactly the starter's (comments aside), else 'gone' or 'changed'.
    _d = _defs().get(_name)
    if _d is None:
        return 'gone'
    _o = [_n for _n in _ast.parse(_orig).body if type(_n).__name__ == 'FunctionDef' and _n.name == _name][0]
    return '' if _ast.dump(_d) == _ast.dump(_o) else 'changed'


def _rerun(_changes=()):
    # The program again in a fresh namespace: setup, then the student's code, prints kept private. Each change's
    # line runs right after the first top-level statement of the student's code that makes its name.
    _body, _found = [], []
    for _code, _mine in ((_SETUP, False), (_source, True)):
        for _n in (_ast.parse(_code).body if _code.strip() else []):
            _body.append(_n)
            if _mine:
                for _anchor, _line in _changes:
                    if _anchor not in _found and _anchor in _made_by(_n):
                        _found.append(_anchor)
                        _body.extend(_ast.parse(_line).body)
    _mod = _ast.Module(body=_body, type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _ns = {'__name__': '__main__'}
    _out, _keep_out, _e = _io.StringIO(), _sys.stdout, None
    _sys.stdout = _out
    try:
        exec(compile(_mod, 'main.py', 'exec'), _ns)
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _e, [_a for _a, _l in _changes if _a not in _found]


def _inside(_fn, _ps, _e, _foreign=()):
    # Lean: what stopped a call inside the student's function, never the name to write instead.
    if type(_e).__name__ == 'NameError':
        _m = getattr(_e, 'name', '') or ''
        if _m in _foreign or [_x for _x in _foreign if len(_x) > 3 and _edits(_m.lower(), _x.lower()) <= 2]:
            return '`' + _m + '` is a name from the Example, not from this function.'
        _d = _defs().get(_fn)
        if [_x for _x in (_locals_of(_d) if _d else []) if _close(_m, _x)]:
            return '`' + _m + '` is not a variable in this function, letter for letter.'
        if [_p for _p in _ps if _close(_m, _p)]:
            return '`' + _m + "` is not one of this function's parameters, letter for letter."
        return 'No variable named `' + _m + '` is made inside `' + _fn + '`.'
    return 'Inside `' + _fn + '`, Python stopped with the error ' + _err(_e) + '.'
'''


def _rx_parts():
    """_RX split into its setup lines and its helper functions, each with the helper names it uses."""
    import ast

    tree = ast.parse(_RX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_RX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_RX_HEAD, _RX_DEFS = _rx_parts()


def check(label, body, setup="", **values):
    """(label, code): the _RX setup lines, the helpers this check uses (and the helpers those use), then the body."""
    import re

    code = fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _RX_DEFS and name not in need:
            need.add(name)
            todo |= _RX_DEFS[name][1]
    head = "\n".join(_RX_HEAD).replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))
    helpers = [text for name, (text, _) in _RX_DEFS.items() if name in need]
    return (label, head + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + code.strip("\n") + "\n")


# =============================================================================================
# UNIT (u10b and u10c must copy this dict verbatim: the exporter requires every field two parts give to match)
# =============================================================================================

UNIT = dict(
    id="readiness-check",
    order=10,
    title="Campaign Readiness Check",
    subtitle="Before We Continue",
    published=True,
    martu_intro=(
        "Before the campaign goes on, show me what you can do on your own. This is practice, never a grade.\n"
        "Part 1: twelve questions, then nine short tasks, with no hints. Part 2: the mini-boss, a whole campaign "
        "part with only the help the campaign gives. Then one click: explain a line you wrote.\n"
        "Missed something? The page *Mar'tu's Notes: Where to Look Again* shows which lesson to open.\n"
        "Once, this code was a wall. Now you take it apart yourself, yes?"
    ),
    goals=[
        "Read every line of the code a campaign part starts with, and say what it does",
        "Make small campaign changes with no hints: replace `pass`, store a result and pass it on, change a stat "
        "sheet, roll a die",
        "Read Python's error message and fix the line it points to",
        "Finish a whole campaign part with only the campaign's help: hold the ward with `if`, `elif` and `else`",
        "Explain a line you wrote, in plain words",
    ],
    campaign_links=[M1, M2],
)

# Only the term this file is first to link. Every other [[link]] here is defined in an earlier unit.
GLOSSARY = [
    dict(
        term="campaign mode",
        aliases=["the campaign's help"],
        plain=(
            "A way to work with only the help the campaign gives: the numbered comments, the check messages, the "
            "error box, and Mar'tu's version after 5 minutes. Help stops before the answer."
        ),
        example="# 1. If the hero's affinity is lower ...",
    ),
]


# =============================================================================================
# Part 1 form A: shared pieces
# =============================================================================================

DIRECTIONS = ["north", "south", "east", "west"]
# A skipped task counts as tried only once it was run with the student's own code (readiness.ts taskAttempted): the
# Stuck line says so, so a skip never leaves forms B and C locked with no reason (the fixer's review, skip path).
_STUCK = ("Stuck? Type your best try, press Run once, then skip this task and come back to it later. Tasks you pass "
          "here stay ✓ done.")


def _rc_meta(item, skills, prepares, foreign="", level="S4", dictates=""):
    """The meta line for a Part 1 task: its 5.3 item number, skill tags and the campaign part it prepares."""
    return meta(starter_level=level, path="READY", form="A", item=item, skills=skills, prepares=prepares,
                solo="true", dictates=dictates, foreign_names=foreign)


# Hidden setup recorders (engine-like helpers, 2.12 rule 3): the scout, the ley board, Oogrish's replies.
SCOUT_SETUP = (
    "class _Scout:\n"
    "    def __init__(self):\n"
    "        self.steps = []\n"
    "\n"
    "    def step(self, direction):\n"
    "        self.steps.append(direction)\n"
    "        print(\"The scout steps \" + str(direction) + \".\")\n"
    "\n"
    "\n"
    "scout = _Scout()\n"
)
BOARD_SETUP = (
    "_board = []\n"
    "\n"
    "\n"
    "def show_on_ley_board(text):\n"
    "    _board.append(text)\n"
    "    print(\"[Ley board] \" + str(text))\n"
)
SAY_SETUP = (
    "_said = []\n"
    "\n"
    "\n"
    "def oogrish_says(text):\n"
    "    _said.append(text)\n"
    "    print(\"Oogrish: \" + str(text))\n"
)

# ---- check bodies (filled with fill(); every message is lean: the slip and the evidence, never the fix) ----

_FN_OK = r'''
_fn, _want, _foreign = __FN__, __PARAMS__, __FOREIGN__
_d = _defs().get(_fn)
if _d is None:
    assert _fn not in [_x for _n in _top() for _x in _made_by(_n)], (
        '`' + _fn + '` is a variable, made with `=`, not a function made with `def`.')
    _near = [_n for _n in _defs() if _close(_n, _fn)]
    assert not _near, 'The function is named `' + (_near or [''])[0] + '`, not `' + _fn + '`, letter for letter.'
    _left = [_n for _n in _defs() if _n in _foreign]
    assert not _left, '`' + (_left or [''])[0] + "` is the Example's function, not this task's."
    assert False, 'No line makes a function named `' + _fn + '` yet.'
_got = [_a.arg for _a in _d.args.args]
if _got != _want:
    assert len(_got) == len(_want), ('The task gives `' + _fn + '` ' + _many(len(_want), 'parameter') + ', but its '
                                     'parentheses hold ' + str(len(_got)) + '.')
    assert sorted(_got) != sorted(_want), "The parameters are in another order than the task's."
    assert False, 'The parentheses hold ' + _names(_got) + ", not the task's parameter names, letter for letter."
assert callable(_g.get(_fn)), 'A later line put a value in `' + _fn + '` with `=`, after `def` made it.'
# A line that is only the function's name, with no `()`: it hands the function over to nobody and calls nothing.
_bare = [_n.lineno for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Name'
         and _n.value.id == _fn]
assert not _bare, ('Line ' + str((_bare or [0])[0]) + ' names `' + _fn + '` with no `()` after it, so that line '
                   'never calls it.')
'''

_KEEP_FN = r'''
_helper, _orig = __HELPER__, __ORIG__
_k = _keep(_helper, _orig)
assert _k != 'gone', '`' + _helper + '` was already finished, and now it is gone.'
assert _k == '', '`' + _helper + '` was already finished, and it changed.'
'''


def fn_ok(name, params, foreign=()):
    return check(f"{name} is a function with the task's parameters", _FN_OK, fn=name, params=list(params),
                 foreign=list(foreign))


def keep_fn(name, orig):
    return check(f"{name} is unchanged", _KEEP_FN, helper=name, orig=orig)


# =============================================================================================
# C1 (item 2) step-west: replace pass (replace-pass; program-movement). CALL.
# =============================================================================================

_STEP = r'''
_fn, _dir, _known = __FN__, __DIR__, __KNOWN__
assert type(_g.get('scout')).__name__ == '_Scout', ('A variable of your own is named `scout`, so the scout from the '
                                                    'code you started with is gone.')
_main = list(scout.steps)
del scout.steps[:]
try:
    _val, _rows, _e = _call(_g[_fn])
    _got = list(scout.steps)
finally:
    del scout.steps[:]
    scout.steps.extend(_main)
_what = 'called `' + _fn + '()`'
if type(_e).__name__ == 'AttributeError' and getattr(_e, 'obj', None) is scout:
    assert False, ('The scout has no `.' + str(getattr(_e, 'name', '') or '') + '`.'
                   + _ev(_what, 'Python stopped with an AttributeError'))
if type(_e).__name__ == 'NameError':
    _m = getattr(_e, 'name', '') or ''
    assert not (_m == 'party' or _m.startswith('move_')), (
        '`' + _m + "` is from the campaign's cabin door, not from this program."
        + _ev(_what, 'Python stopped with a NameError'))
    assert _m not in _known, ('`' + _m + '` has no quotes, so Python looked for a variable with that name.'
                              + _ev(_what, 'Python stopped with a NameError'))
assert _e is None, _inside(_fn, [], _e) + _ev(_what)
if not _got:
    _loose = [_n for _s in _top() for _n in _ast.walk(_s) if type(_n).__name__ == 'Call'
              and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'step']
    assert not _loose, ('The scout line runs on its own, outside the function, so calling the function moves nothing.'
                        + _ev(_what, 'the scout did not move'))
    # The scout's words printed, not a step: the Console shows them, so say so (as Step north does).
    assert not _rows, '`' + _fn + '` printed a line, but the scout did not move.' + _ev(_what, 'the scout stayed where it was')
    assert False, 'Nothing in `' + _fn + '` moves the scout.' + _ev(_what, 'the scout did not move')
assert len(_got) == 1, 'The function moves the scout more than once.' + _ev(_what, 'the scout moved ' + str(len(_got)) + ' times')
_d = _got[0]
if _d != _dir:
    assert not (type(_d).__name__ == 'str' and _d.lower().replace(' ', '') == _dir), (
        'The direction has a capital letter or a space in it. Python matches text letter for letter.'
        + _ev(_what, 'the direction did not match'))
    assert False, ("The scout moved another way than the function's name says."
                   + _ev(_what, 'the scout moved ' + (_d if _d in _known else 'another way')))
'''

WEST_OK = '    scout.step("west")'


def _west(body="    pass", calls=True, head="def step_west():"):
    return (
        "# Replace pass with a command\n"
        "# that moves the scout west.\n"
        "# The scout moves like this:\n"
        "#     scout.step(\"south\")\n"
        f"{head}\n"
        f"{body}\n"
        + ("\n\n# Mar'tu's test call. Leave it.\nstep_west()\n" if calls else "")
    )


WEST_STARTER = _west()
WEST_SOLUTION = _west(WEST_OK)

C1_STEP_WEST = dict(
    id="step-west",
    title="Step west",
    martu=(
        "`step_west` holds only `pass`. It saves the spot, like a blank recipe card, the same as the code at the "
        "cabin door in the campaign. Make the function move the scout west. The scout is the party member who "
        "goes ahead, and line 4 shows how the scout moves. I test it by calling `step_west()` myself.\n"
        + _STUCK
    ),
    names=["step_west", "scout"],
    setup=SCOUT_SETUP,
    support="none",
    explainer="lean",
    starter=WEST_STARTER,
    checkpoints=[
        dict(
            id="replace-pass-west",
            text="Replace `pass` on line 6 with a line that moves the scout west.",
            dictated=False,
            hints=[
                "Look at line 4: it shows how the scout moves. Which word in the name `step_west` says where to go?",
                "`pass` holds the spot for one indented line, like a blank recipe card. Your line takes its place.",
                "In `scout.step(`, the way to go goes in quotes, inside the parentheses.",
            ],
            checks=[
                fn_ok("step_west", []),
                check("step_west moves the scout west", _STEP, setup=SCOUT_SETUP, fn="step_west", dir="west",
                      known=DIRECTIONS),
            ],
            pass_line="`step_west()` moves the scout west. Mar'tu: Good, yes?",
        ),
    ],
    solution=WEST_SOLUTION,
    takeaway="Replace `pass` with one indented line. The function's name says what that line must do.",
    wrong_answers=[
        dict(why="the starter (pass)", code=WEST_STARTER, fails_at=1, message_contains="did not move"),
        dict(why="the direction unquoted (spec: scout.step(west) -> crash)", code=_west("    scout.step(west)"),
             fails_at=0, message_contains="'west' is not defined"),
        dict(why="the direction unquoted, test call removed", code=_west("    scout.step(west)", calls=False),
             fails_at=1, message_contains="has no quotes"),
        dict(why="the wrong direction (spec: \"east\" -> CALL)", code=_west('    scout.step("east")'), fails_at=1,
             message_contains="the scout moved east"),
        dict(why="the comment's example direction copied", code=_west('    scout.step("south")'), fails_at=1,
             message_contains="the scout moved south"),
        dict(why="a capital letter in the direction", code=_west('    scout.step("West")'), fails_at=1,
             message_contains="capital letter"),
        dict(why="a space typed inside the quotes", code=_west('    scout.step("west ")'), fails_at=1,
             message_contains="or a space"),
        dict(why="the line not indented, pass kept above it", code=_west('    pass\nscout.step("west")'), fails_at=1,
             message_contains="runs on its own"),
        dict(why="the line not indented, pass removed (a missing indent)", code=_west('scout.step("west")'),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="two steps", code=_west(WEST_OK + "\n" + WEST_OK), fails_at=1, message_contains="more than once"),
        dict(why="the scout's words printed, not a step", code=_west('    print("The scout steps west.")'),
             fails_at=1, message_contains="printed a line, but the scout did not move"),
        dict(why="the campaign's party.move (with the test call: the run stops)",
             code=_west('    party.move("west")'), fails_at=0, message_contains="'party' is not defined"),
        dict(why="the campaign's party.move, test call removed", code=_west('    party.move("west")', calls=False),
             fails_at=1, message_contains="campaign's cabin door"),
        dict(why="scout.move in place of scout.step, test call removed",
             code=_west('    scout.move("west")', calls=False), fails_at=1, message_contains="has no `.move`"),
        dict(why="the colon left off the def line", code=_west(WEST_OK, head="def step_west()"), fails_at=0,
             message_contains="expected ':'"),
        dict(why="a capital letter in the function's name, test call removed",
             code=_west(WEST_OK, calls=False, head="def Step_west():"), fails_at=1,
             message_contains="letter for letter"),
        dict(why="= used to make the function (def vs =), test call removed",
             code="step_west = scout.step(\"west\")\n", fails_at=1, message_contains="made with `=`"),
    ],
    notes=_rc_meta(2, "replace-pass", "program-movement", foreign="south", level="S4") + "\n"
    "Part 1 item 2 (G3 R18, the campaign-style starter): `def step_west():` / `pass`. CALL through the scout recorder "
    "in setup: the check calls `step_west()` itself, so the result does not depend on the test call. Fails on "
    "(spec): `scout.step(west)` -> the run stops (the explainer answers); `\"east\"` -> CALL ('moved east'). The "
    "comment's example uses `south`, a direction no task asks for. Lean messages (never the finished line). "
    "Review routing (5.5, UI work): first-recipes/recipes-with-names/replace-pass, then call-it.",
)


# =============================================================================================
# C2 (item 3b) present-warning: store then pass (store-then-pass, chain-methods; program-dialogue-prompt,
# show_mana). KEEP + CALL + CMB + STO.
# =============================================================================================

_BOARD = r'''
_fn, _helper, _other = __FN__, __HELPER__, __OTHER__
assert type(_g.get('_board')).__name__ == 'list', 'A variable of your own is named `_board`, so the ley board is gone.'
_main_board = list(_board)


def _board_after(_fake=None):
    _f = _g.get(_fn)
    _old = _g.get(_helper)
    if _fake is not None:
        _g[_helper] = _fake
    del _board[:]
    try:
        _res = _call(_f)
        _got = list(_board)
    finally:
        if _fake is not None:
            _g[_helper] = _old
        del _board[:]
        _board.extend(_main_board)
    return _got, _res[1], _res[2]


_hv, _hr, _he = _call(_g[_helper])
assert _he is None, _inside(_helper, [], _he) + _ev('called `' + _helper + '()`')
_what = 'called `' + _fn + '()`'
_got, _rows, _e = _board_after()
assert _e is None, _inside(_fn, [], _e) + _ev(_what)
_fd = _defs().get(_fn)
_body = [type(_s).__name__ for _s in _fd.body] if _fd else []
if not _got:
    assert _body != ['Pass'], '`' + _fn + '()` still holds only `pass`.'
    assert not _rows, ('The line was printed, not shown on the ley board.'
                       + _ev(_what, 'it printed a line, but the ley board stayed empty'))
    # Stored, then handed back (or handed back straight away): the line goes back to the caller, never to the board.
    _gives = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Return' and _n.value is not None] if _fd else []
    assert not _gives, ('The function hands back the line, so it goes back to the line that called it and never '
                        'reaches the ley '
                        'board.' + _ev(_what, 'nothing reached the ley board'))
    assert False, 'The ley board stayed empty.' + _ev(_what, 'nothing reached the ley board')
assert len(_got) == 1, ('The board got more than one line.'
                        + _ev(_what, 'it put ' + str(len(_got)) + ' lines on the ley board'))
_s = _got[0]
assert type(_s).__name__ != 'function', ('`' + _helper + '` has no `()` after it, so it is never called.'
                                         + _ev(_what, 'the board got the function itself, not its line'))
assert _s is not None, ("What reached the board holds `None`, Python's word for nothing, not a line."
                        + _ev(_what, 'the board got `None`'))
if _s != _hv:
    assert not (type(_s).__name__ == 'str' and _fd is not None and _s in _locals_of(_fd)), (
        "The board showed a variable's name in quotes, not what the variable holds. Quotes mean these exact "
        "letters. No quotes means look inside the box with this label.")
    assert not (type(_s).__name__ == 'str' and _helper in _s), (
        'The board showed `' + _helper + '()` as text in quotes, so the function never ran.'
        + _ev(_what, 'the board got some text'))
    assert False, ('The board did not get the line that `' + _helper + '()` hands back.'
                   + _ev(_what, 'the board showed another line'))
_got2, _rows2, _e2 = _board_after(lambda: _other)
assert _e2 is None, _inside(_fn, [], _e2) + _ev(_what)
_tried = _ev('made `' + _helper + '()` hand back a test line', 'the board did not change')
_made = _locals_of(_fd) if _fd else []
_outside = [_a.id for _c in _calls_in([_fd], 'show_on_ley_board') for _a in _c.args
            if type(_a).__name__ == 'Name' and _a.id not in _made]
assert _got2 == [_other] or not _outside, ('`' + (_outside or [''])[0] + '` was made outside `' + _fn + '()`, so it '
                                           'does not change to match `' + _helper + '()`.' + _tried)
assert _got2 == [_other], 'The board shows a typed-in line, not what `' + _helper + '()` hands back.' + _tried
'''

_STO = r'''
_fn, _helper, _to = __FN__, __HELPER__, __TO__
_fd = _defs().get(_fn)
# The stored value may go on from the call (`get_warning().lower()`): the board check above already proved the line.
_stores = [_s for _s in _ast.walk(_fd) if type(_s).__name__ == 'Assign' and _calls_in([_s.value], _helper)
           and len(_s.targets) == 1 and type(_s.targets[0]).__name__ == 'Name']
_held = [_s.targets[0].id for _s in _stores]
# A plain copy into another variable (`line = words`) still passes the stored line on.
_copies = [_s for _s in _ast.walk(_fd) if type(_s).__name__ == 'Assign' and len(_s.targets) == 1
           and type(_s.targets[0]).__name__ == 'Name' and type(_s.value).__name__ == 'Name']
for _round in range(len(_copies)):
    _held += [_s.targets[0].id for _s in _copies if _s.value.id in _held and _s.targets[0].id not in _held]
# The stored variable may sit inside the argument (`str(words)`): the board check above already proved the line.
_passes = [_c for _c in _calls_in([_fd], _to) if [_x for _a in _c.args for _x in _ast.walk(_a)
                                                   if type(_x).__name__ == 'Name' and _x.id in _held]]
assert _stores and _passes, ('`' + _to + '()` does not get a '
                             'variable that holds what `' + _helper + '()` hands back. The board shows the line, but the '
                             'campaign checks for that stored variable.')
'''

WARN_SHOUT = "THE ARC IS NEAR. HURRY."
WARN_SHOWN = "The arc is near. hurry."
PRESENT_OK = "    words = get_warning()\n    show_on_ley_board(words)"


def _warning(present="    pass", get_line="    return line", shout=WARN_SHOUT, calls=True, between=""):
    return (
        "# Already finished. Leave it be.\n"
        "def get_warning():\n"
        f"    line = \"{shout}\"\n"
        "    line = line.lower()\n"
        "    line = line.capitalize()\n"
        f"{get_line}\n"
        "\n\n"
        "# Finish present_warning():\n"
        "# 1. Store the result of\n"
        "#    get_warning() in a variable.\n"
        "# 2. Pass that variable to\n"
        "#    show_on_ley_board().\n"
        "def present_warning():\n"
        f"{present}\n"
        + between
        + ("\n\n# Mar'tu's test call. Leave it.\npresent_warning()\n" if calls else "")
    )


WARN_STARTER = _warning()
WARN_SOLUTION = _warning(PRESENT_OK)
WARN_HELPER = (
    "def get_warning():\n"
    f"    line = \"{WARN_SHOUT}\"\n"
    "    line = line.lower()\n"
    "    line = line.capitalize()\n"
    "    return line\n"
)

C2_PRESENT_WARNING = dict(
    id="present-warning",
    title="Store, then pass it on",
    martu=(
        "`get_warning()` is finished. It tidies its line with `.lower()`, then `.capitalize()`, like my dialogue "
        "line in the campaign, and hands it back. Finish `present_warning()` so that line reaches the ley board, "
        "a message board that shows it in the Console. As in Unit 3, catch the line in a variable, then pass it "
        "on, like a basketball pass. I test it by making `get_warning()` hand back a test line.\n" + _STUCK
    ),
    names=["present_warning", "get_warning", "show_on_ley_board"],
    setup=BOARD_SETUP,
    support="none",
    explainer="lean",
    starter=WARN_STARTER,
    checkpoints=[
        dict(
            id="finish-present-warning",
            text="Replace `pass` on line 15 with two lines:\n1. Store what `get_warning()` hands back in a "
                 "variable.\n2. Pass that variable to `show_on_ley_board()`.",
            dictated=False,
            hints=[
                "Read the numbered comments on lines 10 to 13. Two lines go inside `present_warning()`, where "
                "`pass` is now.",
                "A variable can catch what a function hands back, like catching a basketball. Then you pass that "
                "variable to another function.",
                "The first line starts with a name for your variable, then `=`.",
            ],
            checks=[
                keep_fn("get_warning", WARN_HELPER),
                fn_ok("present_warning", []),
                check("the board shows the helper's line", _BOARD, setup=BOARD_SETUP, fn="present_warning",
                      helper="get_warning", other="Pell says: shutters down."),
                check("the line is stored in a variable", _STO, fn="present_warning", helper="get_warning",
                      to="show_on_ley_board"),
            ],
            pass_line=f"Your warning reached the ley board: `{WARN_SHOWN}`",
        ),
    ],
    solution=WARN_SOLUTION,
    takeaway="Catch what a function hands back in a variable. Then pass that variable on, like a basketball pass.",
    wrong_answers=[
        dict(why="the starter (pass)", code=WARN_STARTER, fails_at=1, message_contains="still holds only `pass`"),
        dict(why="the line typed (spec: a typed line -> CMB)",
             code=_warning(f"    show_on_ley_board(\"{WARN_SHOWN}\")"), fails_at=1,
             message_contains="a typed-in line"),
        dict(why="no () on the helper (spec: no () -> CALL)", code=_warning("    show_on_ley_board(get_warning)"),
             fails_at=1, message_contains="has no `()`"),
        dict(why="no () on the helper, stored", code=_warning("    words = get_warning\n    show_on_ley_board(words)"),
             fails_at=1, message_contains="has no `()`"),
        dict(why="passed straight on, not stored (spec: no store -> STO)",
             code=_warning("    show_on_ley_board(get_warning())"), fails_at=1,
             message_contains="does not get a variable"),
        dict(why="stored, then printed", code=_warning("    words = get_warning()\n    print(words)"), fails_at=1,
             message_contains="printed, not shown"),
        dict(why="stored, then handed back (the line goes back to the caller)",
             code=_warning("    words = get_warning()\n    return words"), fails_at=1,
             message_contains="goes back to the line that called it and never reaches the ley board"),
        dict(why="the helper's line handed back straight away, never stored or shown",
             code=_warning("    return get_warning()"), fails_at=1, message_contains="never reaches the ley board"),
        dict(why="the variable's name in quotes (a quoted name)",
             code=_warning("    words = get_warning()\n    show_on_ley_board(\"words\")"), fails_at=1,
             message_contains="name in quotes"),
        dict(why="a variable never stored", code=_warning("    show_on_ley_board(words)"), fails_at=0,
             message_contains="'words' is not defined"),
        dict(why="== for = (= vs ==): nothing is stored, so the name is never made",
             code=_warning("    words == get_warning()\n    show_on_ley_board(words)"), fails_at=0,
             message_contains="'words' is not defined"),
        dict(why="the second line not indented (a missing indent): it runs outside the function",
             code=_warning("    words = get_warning()\nshow_on_ley_board(words)"), fails_at=0,
             message_contains="'words' is not defined"),
        dict(why="the call typed in quotes (a quoted name): text, never run",
             code=_warning("    show_on_ley_board(\"get_warning()\")"), fails_at=1,
             message_contains="as text in quotes"),
        dict(why="def used to make a variable (def vs =)",
             code=_warning("    def words = get_warning()\n    show_on_ley_board(words)"), fails_at=0,
             message_contains="expected '('"),
        dict(why="the finished helper edited (its words changed): told to leave it be",
             code=_warning(PRESENT_OK, shout="GET INSIDE."), fails_at=1, message_contains="it changed"),
        dict(why="the finished helper edited (its return removed)", code=_warning(PRESENT_OK, get_line=""),
             fails_at=1, message_contains="it changed"),
        dict(why="shown twice", code=_warning(PRESENT_OK + "\n    show_on_ley_board(words)"), fails_at=1,
             message_contains="more than one line"),
        dict(why="stored outside the function; the function passes that outside variable",
             code=_warning("    show_on_ley_board(words)", between="\n\nwords = get_warning()\n"), fails_at=1,
             message_contains="was made outside"),
        dict(why="the campaign's print_prompt (the run stops)",
             code=_warning("    words = get_warning()\n    print_prompt(words)"), fails_at=0,
             message_contains="'print_prompt' is not defined"),
    ],
    notes=_rc_meta("3b", "store-then-pass,chain-methods", "program-dialogue-prompt,mana-bars (show_mana)",
                   foreign="note,get_note,show_it", level="S4") + "\n"
    "Part 1 item 3 (b), the campaign-style `pass` starter (G3 R18). Item 3 (a), the one-click prediction of what "
    "the board shows, is question i3a in rc-part1-a-questions, with another line (so this task's run never answers "
    "it). KEEP: `get_warning` is compared with the starter's (AST, comments aside); an edited helper fails first "
    "(the class's 'edited a helper you were told to leave alone'). CALL + CMB: the board recorder in setup gets "
    "the helper's line once, and follows when the check swaps `get_warning` for one that hands back another line "
    "(a typed line fails). STO: a variable inside the function holds the helper's result and is passed on (a "
    "plain copy counts). Fails on (spec): a typed line -> CMB; no store -> STO; no `()` -> CALL. Also named: the "
    "line handed back (stored then handed back, or handed back straight away), which goes back to the caller and never "
    "reaches the board (print instead of return's mirror). Lean messages. "
    "Review routing: first-recipes/recipes-with-names/store-then-pass; spell-recipes/recipes-read-sheets/"
    "bar-then-draw.",
)


# =============================================================================================
# C3 (item 5b) mend-the-choice: an unquoted option (quote-text, elif-chain; program-dialogue-options). CALL.
# =============================================================================================

_ANSWER = r'''
_fn, _cases = __FN__, __CASES__
_f = _g.get(_fn)
_said = _g.get('_said')
assert type(_said).__name__ == 'list', "A variable of your own is named `_said`, so Oogrish's replies are gone."
_fd = _defs().get(_fn)
_texts = [_x.value for _n in _ast.walk(_fd) if type(_n).__name__ == 'Compare'
          for _x in [_n.left] + list(_n.comparators)
          if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str']
for _c, _want in _cases:
    _before = list(_said)
    del _said[:]
    try:
        _val, _rows, _e = _call(_f, (_c,))
        _got = list(_said)
    finally:
        del _said[:]
        _said.extend(_before)
    _what = 'called ' + _sig(_fn, (_c,))
    if type(_e).__name__ == 'NameError':
        _m = getattr(_e, 'name', '') or ''
        assert not _m.lower().startswith('option'), ('`' + _m + '` has no quotes, so Python looked for a variable '
                                                     'with that name.' + _ev(_what, 'Python stopped with a NameError'))
    assert _e is None, _inside(_fn, ['choice'], _e) + _ev(_what)
    if _got == _want:
        continue
    _for = 'For `"' + _c + '"`, '
    if not _got:
        _odd = [_x for _x in _texts if _x != _c and _x.lower().replace(' ', '') == _c.lower().replace(' ', '')]
        assert not _odd, ('A question compares `choice` with text that differs from `"' + _c + '"` in its capitals '
                          'or spaces. Python matches text letter for letter.' + _ev(_what, 'Oogrish said nothing'))
        _twice = [_x for _x in _texts if _texts.count(_x) > 1]
        assert not _twice, 'Two questions compare with the same text, so one reply never runs.' + _ev(_what, 'Oogrish said nothing')
        # Another option's text in place of this one (`"option 4"`): name the line and both texts, never the fix.
        _listed = [_x for _x, _ws in _cases]
        _other = [(_x.lineno, _x.value) for _n in _ast.walk(_fd) if type(_n).__name__ == 'Compare'
                  for _x in [_n.left] + list(_n.comparators)
                  if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str' and _x.value != _c
                  and _x.value in _listed and _texts.count(_x.value) == 1 and _c not in _texts
                  and _x.value not in [_y for _y, _ws in _cases[:_listed.index(_c)]]]
        assert not _other, ('Line ' + str(_other[0][0]) + ' compares `choice` with `"' + _other[0][1] + '"`, and no '
                            'question compares it with `"' + _c + '"`.' + _ev(_what, 'Oogrish said nothing'))
        assert False, _for + 'Oogrish said nothing.' + _ev(_what)
    assert _want, _for + 'Oogrish still said a reply: a branch runs for any choice.' + _ev(_what)
    assert len(_got) == 1, _for + 'Oogrish said ' + str(len(_got)) + ' replies.' + _ev(_what)
    assert _got[0] in [_w for _x, _ws in _cases for _w in _ws], (
        _for + 'Oogrish said a reply that is not in the code you started with: a reply line changed.' + _ev(_what))
    assert False, _for + "Oogrish said another branch's reply." + _ev(_what)
'''

CHOICE_REPLIES = ["Steady, now.", "We go soon.", "Rest first."]
THIRD_BAD = "    elif choice == option 3:"
THIRD_OK = "    elif choice == \"option 3\":"


def _choice(third=THIRD_BAD, calls=True):
    return (
        "def answer(choice):\n"
        "    if choice == \"option 1\":\n"
        f"        oogrish_says(\"{CHOICE_REPLIES[0]}\")\n"
        "    elif choice == \"option 2\":\n"
        f"        oogrish_says(\"{CHOICE_REPLIES[1]}\")\n"
        f"{third}\n"
        f"        oogrish_says(\"{CHOICE_REPLIES[2]}\")\n"
        + ("\n\n# Mar'tu's test call. Leave it.\nanswer(\"option 3\")\n" if calls else "")
    )


CHOICE_STARTER = _choice()
CHOICE_SOLUTION = _choice(THIRD_OK)
CHOICE_CASES = [("option 1", [CHOICE_REPLIES[0]]), ("option 2", [CHOICE_REPLIES[1]]),
                ("option 3", [CHOICE_REPLIES[2]]), ("option 4", [])]

C3_MEND_THE_CHOICE = dict(
    id="mend-the-choice",
    title="Fix the third choice",
    martu=(
        "`answer` picks Oogrish's reply for each choice, like the four dialogue options in the campaign. Python "
        "checks the chain from the top, like a grading scale. One question is broken, so Python stops. Read the "
        "box in the Console like a teacher's note in the margin: its title says what went wrong, and Python's last "
        "line says it in Python's words. Then fix the line the box points to, and press Run again. I test every "
        "choice myself, and one that is not on the list.\n"
        + _STUCK
    ),
    names=["answer", "choice"],
    setup=SAY_SETUP,
    support="none",
    explainer="lean",
    starter=CHOICE_STARTER,
    checkpoints=[
        dict(
            id="mend-option-3",
            text=("Fix line 6 so `answer(\"option 3\")` makes Oogrish say his third reply, `Rest first.` Keep line 6 "
                  "a question: a choice not on the list still gets no reply."),
            dictated=False,
            hints=[
                "Press Run. Read the title of the box in the Console, then Python's last line. Both point to line 6.",
                "Compare line 6 with the two questions above it, on lines 2 and 4, mark by mark.",
                "Look at how `option 3` is written on line 6, and how the other two options are written.",
            ],
            checks=[check("each choice gets its own reply", _ANSWER, setup=SAY_SETUP, fn="answer", cases=CHOICE_CASES)],
            pass_line=f"Each choice gets its own reply now. Oogrish: {CHOICE_REPLIES[2]}",
        ),
    ],
    solution=CHOICE_SOLUTION,
    takeaway="Text in an `if` question needs quotes, with exactly the letters the call hands over.",
    wrong_answers=[
        dict(why="the starter: option 3 unquoted (spec: left unquoted -> crash)", code=CHOICE_STARTER, fails_at=0,
             message_contains="invalid syntax"),
        dict(why="an underscore in place of the quotes (a name, not text)",
             code=_choice("    elif choice == option_3:"), fails_at=0, message_contains="'option_3' is not defined"),
        dict(why="an underscore in place of the quotes, test call removed (unquoted text)",
             code=_choice("    elif choice == option_3:", calls=False), fails_at=1, message_contains="has no quotes"),
        dict(why="a capital letter (STREXACT)", code=_choice("    elif choice == \"Option 3\":"), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="the space left out (STREXACT)", code=_choice("    elif choice == \"option3\":"), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="= for == (= vs ==)", code=_choice("    elif choice = \"option 3\":"), fails_at=0,
             message_contains="Maybe you meant '=='"),
        dict(why="the line above copied (option 2 twice)", code=_choice("    elif choice == \"option 2\":"),
             fails_at=1, message_contains="Two questions compare with the same text"),
        dict(why="the colon left off", code=_choice("    elif choice == \"option 3\""), fails_at=0,
             message_contains="expected ':'"),
        dict(why="else in place of the third test: the reply runs for any choice", code=_choice("    else:"),
             fails_at=1, message_contains="a branch runs for any choice"),
        dict(why="the wrong option number", code=_choice("    elif choice == \"option 4\":"), fails_at=1,
             message_contains="Line 6 compares `choice` with `\"option 4\"`, and no question compares it with `\"option 3\"`."),
    ],
    notes=_rc_meta("5b", "quote-text,elif-chain", "program-dialogue-options", level="S4") + "\n"
    "Part 1 item 5 (b): mend `elif choice == option 3:` (a SyntaxError, so the explainer names the line first). "
    "Item 5 (a), which branch runs for `\"option 2\"`, is question i5a. CALL: `oogrish_says` (setup) records each "
    "reply; the check calls `answer` with option 1 to 4 and every reply must match its own branch (option 4 says "
    "nothing). Fails on (spec): left unquoted -> the run stops. Also: `option_3`, capitals or a missing space "
    "(STREXACT, named without the student's text), `=` for `==`, the missing colon, the line above copied, `else:` "
    "(the reply for every choice). Review routing: control-flow/if-the-clock-turns-red/four-answers; "
    "hello-world/words-in-quotes/words-need-quotes.",
)



# =============================================================================================
# C4 (item 6 a-c) read-the-sheet: read, read inside, write by a key from a variable (dict-read, dict-nested,
# dict-write, dict-key-from-variable; spell-book, hold-the-barrier). CMB / KEY.
# =============================================================================================

SHEET_OTHER = 'hero = {"name": "Pell", "mana": 11, "abilities": {"wisdom": 5, "dexterity": 9}}'

_SHEET_READ = r'''
_box, _want, _typed, _other, _path = __BOX__, __WANT__, __TYPED__, __OTHER__, __PATH__
if _box not in _g:
    _near = [_x for _n in _top() for _x in _made_by(_n) if _close(_x, _box)]
    assert not _near, 'A variable named `' + (_near or [''])[0] + '` is made, not `' + _box + '`, letter for letter.'
    _shown = [_x for _c in _calls_in(_top(), 'print') for _a in _c.args for _x in _ast.walk(_a)
              if type(_x).__name__ == 'Subscript' and type(_x.slice).__name__ == 'Constant' and _x.slice.value == _box]
    assert not _shown, 'The ' + _box + ' is read and printed, but no variable named `' + _box + '` holds it.'
    assert False, 'No variable named `' + _box + '` is made yet.'
_ns, _ls, _e, _miss = _rerun([('hero', __SHEET__)])
_what = 'ran it again with a test sheet in `hero`'
assert not _miss, "The line from the code you started with that makes `hero` is gone."
assert _e is None, 'With a test sheet in `hero`, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
_v = _ns.get(_box)
if _v != _want:
    assert _v != _typed, ('`' + _box + '` holds a typed-in ' + str(_typed) + ". Mar'tu tested your code with a test sheet in "
                          '`hero`, and `' + _box + '` still said ' + str(_typed) + '.')
    assert type(_v).__name__ != 'dict', '`' + _box + '` holds a whole dictionary, not one value from it.' + _ev(_what)
    assert type(_v).__name__ != 'str', '`' + _box + '` holds some text, not a number from the sheet.' + _ev(_what)
    assert _v != _other[0], '`' + _box + '` holds the ' + _other[1] + ', not the ' + _box + '.' + _ev(_what)
    assert False, '`' + _box + '` holds ' + _show(_v) + ', not the ' + _box + ' on the sheet.' + _ev(_what)
# The sheet as it stands now (a sheet with other numbers typed in is still read right).
_main = _g.get('hero')
for _k in _path:
    _main = _main.get(_k) if type(_main).__name__ == 'dict' else None
assert _g[_box] == _main, ('`' + _box + '` holds ' + _num(_g[_box]) + ', and the sheet' + "'s " + _box + ' is '
                           + _num(_main) + '.')
'''

_BOOK = r'''
_first = book
# Another book too (one more page, "Ember"), so a book typed out again, old page and all, does not follow.
_ns, _ls, _e, _miss = _rerun([('book', 'book = {"Hush": {"mana_cost": 2}, "Ember": {"mana_cost": 7}}'),
                              ('spell_name', 'spell_name = "Moon Step"'), ('spell', 'spell = {"mana_cost": 9}')])
_what = 'used a test name, `"Moon Step"`, a test `book` and a test `spell`'
assert not _miss, "The line from the code you started with that makes `" + (_miss or [''])[0] + '` is gone.'
assert _e is None, 'With a test name and spell, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
_b = _ns.get('book')
assert type(_b).__name__ == 'dict', '`book` is not a dictionary any more: it holds ' + _show(_b) + '.' + _ev(_what)
_page = _b.get('Moon Step')
if _page is not _ns.get('spell'):
    _named = [_k for _k in _b if _k in ('spell_name', 'spell')]
    assert not _named, ('`book` got the key `"' + (_named or [''])[0] + '"`, a variable' + "'s name in quotes, not "
                        'what the variable holds.' + _ev(_what))
    assert 'Glow' not in _b, ('The key is a typed-in `"Glow"`. Mar' + "'tu tested your code with a test name in `spell_name`, "
                              'and the key still said `"Glow"`.')
    if type(_page).__name__ == 'dict':
        assert _page != {'mana_cost': 4}, 'The page under the name is a typed-in dictionary, not the one in `spell`.' + _ev(_what)
        assert False, 'The page under the name is another dictionary, not the one in `spell`.' + _ev(_what)
    assert _page is None, 'The page under the name holds ' + _show(_page) + ', not `spell`.' + _ev(_what)
    assert False, 'Nothing was stored in `book` under the name in `spell_name`.' + _ev(_what)
assert 'Hush' in _b and 'Ember' in _b, ('A page that `book` already held is gone from `book`: a new book was made, '
                                        'not added to.' + _ev(_what))
'''

SHEET_HEAD = (
    "hero = {\n"
    "    \"name\": \"Bomb Shell\",\n"
    "    \"mana\": 24,\n"
    "    \"abilities\": {\n"
    "        \"wisdom\": 8,\n"
    "        \"dexterity\": 6,\n"
    "    },\n"
    "}\n"
    "book = {\"Hush\": {\"mana_cost\": 2}}\n"
    "spell_name = \"Glow\"\n"
    "spell = {\"mana_cost\": 4}\n"
)
SHEET_A = "mana = hero[\"mana\"]\n"
SHEET_B = "wisdom = hero[\"abilities\"][\"wisdom\"]\n"
SHEET_C = "book[spell_name] = spell\n"


def _sheet(a="", b="", c=""):
    return (
        SHEET_HEAD
        + "\n# 1. Store the hero's mana in a\n#    variable named mana.\n" + a
        + "\n# 2. Store the hero's wisdom in a\n#    variable named wisdom.\n" + b
        + "\n# 3. Store spell in book, using\n#    spell_name as the key.\n" + c
    )


SHEET_STARTER = _sheet()
SHEET_SOLUTION = _sheet(SHEET_A, SHEET_B, SHEET_C)

C4_READ_THE_SHEET = dict(
    id="read-the-sheet",
    title="Read and write the sheet",
    martu=(
        "Bomb Shell's stat sheet is a [[dictionary]]: you look a value up by its key, like a word in the glossary "
        "of a textbook. A sheet inside a sheet reads outside first, like a chapter and then a section. Write three "
        "lines, one under each numbered comment. I test your code with a test sheet, a test spell name and a test "
        "spell.\n"
        + _STUCK
    ),
    names=["hero", "mana", "wisdom", "book", "spell_name", "spell"],
    support="none",
    explainer="lean",
    starter=SHEET_STARTER,
    checkpoints=[
        dict(
            id="read-mana",
            text="Store the mana from the sheet `hero` in a variable named `mana`. Write it under `# 1.`.",
            dictated=False,
            hints=[
                "Look at the sheet `hero` at the top of your code. Which key holds the mana?",
                "You read a value by its key, like looking a word up in a glossary: the sheet's name, then the key "
                "in square brackets.",
                "The line starts `mana =`, then a read from `hero`.",
            ],
            checks=[check("mana is read from the sheet", _SHEET_READ, box="mana", want=11, typed=24,
                          other=(9, "dexterity"), sheet=SHEET_OTHER, path=["mana"])],
        ),
        dict(
            id="read-wisdom",
            text="Store the wisdom from the sheet `hero` in a variable named `wisdom`. Write it under `# 2.`.",
            dictated=False,
            hints=[
                "Look at the sheet `hero`. Is `\"wisdom\"` on the big sheet, or inside `\"abilities\"`?",
                "A sheet inside a sheet needs two keys in a row, outside first. It's like a table of contents: the "
                "chapter, then the section.",
                "The line starts `wisdom =`, then two reads from `hero`.",
            ],
            checks=[check("wisdom is read from inside the sheet", _SHEET_READ, box="wisdom", want=5, typed=8,
                          other=(9, "dexterity"), sheet=SHEET_OTHER, path=["abilities", "wisdom"])],
        ),
        dict(
            id="store-the-spell",
            text="Store `spell` in `book`, using the name that `spell_name` holds as the key. Write it under `# 3.`.",
            dictated=False,
            hints=[
                "The key is the name that `spell_name` holds, not the word spell_name.",
                "Writing to a dictionary puts the key in square brackets on the left of `=`.",
                "The line starts with `book[`, and `spell` goes on the right of `=`.",
            ],
            checks=[check("the spell is stored under the name in spell_name", _BOOK)],
            pass_line="You read the sheet, read inside it, and wrote to the book by name. Mar'tu: The spell book holds.",
        ),
    ],
    solution=SHEET_SOLUTION,
    partials=[_sheet(SHEET_A), _sheet(SHEET_A, SHEET_B)],
    takeaway="`hero[\"mana\"]` reads a value. `hero[\"abilities\"][\"wisdom\"]` reads inside, outside key first. "
             "`book[spell_name] = spell` writes under the name in `spell_name`.",
    wrong_answers=[
        dict(why="the starter (nothing made)", code=SHEET_STARTER, fails_at=1, message_contains="`mana`"),
        dict(why="(a) the mana typed (CMB)", code=_sheet("mana = 24\n", SHEET_B, SHEET_C), fails_at=1,
             message_contains="`mana` holds a typed-in 24. Mar'tu tested your code with a test sheet in `hero`"),
        dict(why="(a) a capital in the key (KEY: KeyError)", code=_sheet("mana = hero[\"Mana\"]\n", SHEET_B, SHEET_C),
             fails_at=0, message_contains="KeyError: 'Mana'"),
        dict(why="(a) the key unquoted (a variable, not text)", code=_sheet("mana = hero[mana]\n", SHEET_B, SHEET_C),
             fails_at=0, message_contains="'mana' is not defined"),
        dict(why="(a) the check's own other value typed (main run)", code=_sheet("mana = 11\n", SHEET_B, SHEET_C),
             fails_at=1, message_contains="and the sheet's mana is 24"),
        dict(why="(a) the whole sheet stored", code=_sheet("mana = hero\n", SHEET_B, SHEET_C), fails_at=1,
             message_contains="a whole dictionary"),
        dict(why="(a) a capital in the variable's name (approximate names)",
             code=_sheet("Mana = hero[\"mana\"]\n", SHEET_B, SHEET_C), fails_at=1,
             message_contains="`Mana` is made, not `mana`"),
        dict(why="(a) the read printed, never stored", code=_sheet("print(hero[\"mana\"])\n", SHEET_B, SHEET_C),
             fails_at=1, message_contains="read and printed"),
        dict(why="(a) the key word itself stored (quotes on the value)", code=_sheet("mana = \"mana\"\n", SHEET_B,
                                                                                   SHEET_C),
             fails_at=1, message_contains="some text"),
        dict(why="(b) a nesting level skipped (spec: hero[\"wisdom\"])",
             code=_sheet(SHEET_A, "wisdom = hero[\"wisdom\"]\n", SHEET_C), fails_at=0,
             message_contains="KeyError: 'wisdom'"),
        dict(why="(b) one level short: the inner sheet stored", code=_sheet(SHEET_A, "wisdom = hero[\"abilities\"]\n",
                                                                           SHEET_C),
             fails_at=2, message_contains="a whole dictionary"),
        dict(why="(b) the wisdom typed (CMB)", code=_sheet(SHEET_A, "wisdom = 8\n", SHEET_C), fails_at=2,
             message_contains="`wisdom` holds a typed-in 8"),
        dict(why="(b) the other ability read", code=_sheet(SHEET_A, "wisdom = hero[\"abilities\"][\"dexterity\"]\n",
                                                          SHEET_C),
             fails_at=2, message_contains="holds the dexterity"),
        dict(why="(c) the variable's name in quotes (spec: book[\"spell_name\"], KEY)",
             code=_sheet(SHEET_A, SHEET_B, "book[\"spell_name\"] = spell\n"), fails_at=3,
             message_contains="a variable's name in quotes"),
        dict(why="(c) the key typed (CMB)", code=_sheet(SHEET_A, SHEET_B, "book[\"Glow\"] = spell\n"), fails_at=3,
             message_contains="The key is a typed-in `\"Glow\"`"),
        dict(why="(c) a new book made: the first page is lost", code=_sheet(SHEET_A, SHEET_B, "book = {spell_name: spell}\n"),
             fails_at=3, message_contains="is gone from `book`"),
        dict(why="(c) the page typed in", code=_sheet(SHEET_A, SHEET_B, "book[spell_name] = {\"mana_cost\": 4}\n"),
             fails_at=3, message_contains="typed-in dictionary"),
        dict(why="(c) the word spell stored, not the page", code=_sheet(SHEET_A, SHEET_B, "book[spell_name] = \"spell\"\n"),
             fails_at=3, message_contains="holds some text"),
        dict(why="(c) the key and the value swapped", code=_sheet(SHEET_A, SHEET_B, "book[spell] = spell_name\n"),
             fails_at=0, message_contains="unhashable type: 'dict'"),
        dict(why="(c) a list's append used on a dictionary", code=_sheet(SHEET_A, SHEET_B, "book.append(spell)\n"),
             fails_at=0, message_contains="AttributeError"),
        dict(why="(c) == for = (= vs ==): a comparison reads a page that is not there yet",
             code=_sheet(SHEET_A, SHEET_B, "book[spell_name] == spell\n"), fails_at=0,
             message_contains="KeyError: 'Glow'"),
    ],
    notes=_rc_meta("6a-c", "dict-read,dict-nested,dict-write,dict-key-from-variable", "spell-book,hold-the-barrier",
                   level="S2") + "\n"
    "Part 1 item 6 (a) to (c), one checkpoint each, behavior-checked with CMB reruns (another sheet in `hero`: "
    "Pell, mana 11, wisdom 5, dexterity 9; another `spell_name` and `spell`), never OUT. Item 6 (d), True or False "
    "for `\"Glow\" in book`, is question i6d. The 5.5 rule 'item 6 at 3 of 4 parts' needs per-checkpoint scoring "
    "(site work): here every checkpoint is required, as in any testout. The book starts with `\"Hush\"`, so a new "
    "book that loses it fails (the campaign's 'a second spell keeps the first'). Fails on (spec): `hero[\"wisdom\"]` "
    "(KeyError: a skipped level), `book[\"spell_name\"]` (KEY). Review routing: dictionaries/stat-sheets/read-by-key, "
    "key-from-a-box; dictionaries/sheets-inside-sheets/abilities-inside.",
)


# =============================================================================================
# C5 (item 7b) mend-the-bar: "░" * (max_mana - mana) (repeat-string; mana-bars). CMB.
# =============================================================================================

_BAR = r'''
_first = empty
# 4 / 8 tells a typed 7, a typed 10 (`10 - mana`) and a typed 3 (`max_mana - 3`) apart: 7, 6 and 5 blocks, not 4.
for _m, _x in ((3, 10), (4, 8), (0, 4)):
    _ns, _ls, _e, _miss = _rerun([('mana', 'mana = ' + str(_m)), ('max_mana', 'max_mana = ' + str(_x))])
    _with = '`mana = ' + str(_m) + '` and `max_mana = ' + str(_x) + '`'
    _what = 'ran it again with ' + _with
    assert not _miss, "The line from the code you started with that makes `" + (_miss or [''])[0] + '` is gone.'
    assert _e is None, 'With ' + _with + ', Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
    _emp = _ns.get('empty')
    _need = _x - _m
    if _emp != '░' * _need:
        _said = '`empty` had ' + (str(len(_emp)) if type(_emp).__name__ == 'str' else 'no') + ' blocks, but ' + str(_need) + ' points are used'
        assert type(_emp).__name__ == 'str', '`empty` holds ' + _show(_emp) + ', not blocks.' + _ev(_what)
        assert not [_c for _c in _emp if _c != '░'], '`empty` holds other marks than `░`.' + _ev(_what)
        assert len(_emp) != _x, ('`empty` has one `░` for each point of `max_mana`, not one for each point used.'
                                 + _ev(_what, _said))
        _not = ' blocks, not ' + str(_need) + '.'
        assert len(_emp) != 7, ('`empty` holds 7 typed-in blocks. ' + "Mar'tu tested your code with test numbers, " + str(_m) + ' in `mana` '
                                'and ' + str(_x) + ' in `max_mana`, and `empty` still had 7' + _not)
        # Every test value the result depends on is named, then the answer: no hidden number to work out.
        _both = "Mar'tu tested your code with test numbers, " + str(_m) + ' in `mana` and ' + str(_x) + ' in `max_mana`: '
        _should = '`empty` should have ' + str(_need) + ' blocks, but it had ' + str(len(_emp)) + '.'
        assert not (_x != 10 and len(_emp) == 10 - _m), (
            'Your `empty` line holds a typed-in 10, not `max_mana`. ' + _both + _should)
        assert not (_m != 3 and len(_emp) == _x - 3), (
            'Your `empty` line holds a typed-in 3, not `mana`. ' + _both + _should)
        assert False, '`empty` does not have one `░` for each point used.' + _ev(_what, _said)
    assert 'Mana [' + '█' * _m + '░' * _need + ']' in _ls, ('The printed bar does not show `full` and then `empty`.'
                                                          + _ev(_what))
'''

BAR_BAD = "empty = \"░\" * max_mana - mana"
BAR_OK = "empty = \"░\" * (max_mana - mana)"


def _bar(line=BAR_BAD):
    return (
        "mana = 3\n"
        "max_mana = 10\n"
        "full = \"█\" * mana\n"
        f"{line}\n"
        "print(\"Mana [\" + full + empty + \"]\")\n"
    )


BAR_STARTER = _bar()
BAR_SOLUTION = _bar(BAR_OK)

C5_MEND_THE_BAR = dict(
    id="mend-the-bar",
    title="Fix the mana bar",
    martu=(
        "Mana is a hero's magic power. A mana bar, like the ones in the campaign, shows one `█` for each point of "
        "mana, then one `░` for each point used. Python repeats text the way 3 × 4 means 4 + 4 + 4: `\"█\" * 3` is "
        "`███`. Line 4 "
        "is broken, so Python stops. Read the box in the Console, then fix line 4. I test it with other "
        "numbers.\n" + _STUCK
    ),
    names=["empty", "mana", "max_mana"],
    support="none",
    explainer="lean",
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="mend-line-4",
            text="Fix line 4 so `empty` holds one `░` for each point of mana used.",
            dictated=False,
            hints=[
                "Press Run. Read the title of the box in the Console, then Python's last line. Both point to line 4.",
                "Python uses PEMDAS, so it does `*` before `-`. Text times a number is text, and you can't take "
                "a number away from text.",
                "Which part of line 4 must Python work out first?",
            ],
            checks=[check("empty follows mana and max_mana", _BAR)],
            pass_line="`empty` changes to match the mana now. Mana [███░░░░░░░]",
        ),
    ],
    solution=BAR_SOLUTION,
    takeaway="`\"░\" * (max_mana - mana)`: the parentheses make Python subtract first, like PEMDAS in math class.",
    wrong_answers=[
        dict(why="the starter: no brackets (spec: no parentheses)", code=BAR_STARTER, fails_at=0,
             message_contains="unsupported operand type(s) for -: 'str' and 'int'"),
        dict(why="the subtraction dropped", code=_bar("empty = \"░\" * max_mana"), fails_at=1,
             message_contains="each point of `max_mana`"),
        dict(why="the 7 typed (CMB)", code=_bar("empty = \"░\" * 7"), fails_at=1,
             message_contains="`empty` holds 7 typed-in blocks. Mar'tu tested your code with test numbers, 4 in `mana` and 8 in `max_mana`"),
        dict(why="the bar typed (CMB)", code=_bar("empty = \"░░░░░░░\""), fails_at=1,
             message_contains="holds 7 typed-in blocks"),
        dict(why="the spec's own numbers bracketed: \"░\" * (10 - 3) (CMB)", code=_bar("empty = \"░\" * (10 - 3)"),
             fails_at=1, message_contains="still had 7 blocks, not 4"),
        dict(why="max_mana typed: \"░\" * (10 - mana) (CMB)", code=_bar("empty = \"░\" * (10 - mana)"), fails_at=1,
             message_contains="holds a typed-in 10, not `max_mana`. Mar'tu tested your code with test numbers, 4 in `mana` and 8 in `max_mana`: `empty` should have 4 blocks, but it had 6."),
        dict(why="mana typed: \"░\" * (max_mana - 3) (CMB)", code=_bar("empty = \"░\" * (max_mana - 3)"), fails_at=1,
             message_contains="holds a typed-in 3, not `mana`. Mar'tu tested your code with test numbers, 4 in `mana` and 8 in `max_mana`: `empty` should have 4 blocks, but it had 5."),
        dict(why="the subtraction the wrong way round", code=_bar("empty = \"░\" * (mana - max_mana)"), fails_at=1,
             message_contains="one `░` for each point used"),
        dict(why="brackets around the wrong part", code=_bar("empty = (\"░\" * max_mana) - mana"), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the full block used", code=_bar("empty = \"█\" * (max_mana - mana)"), fails_at=1,
             message_contains="other marks than"),
        dict(why="two bars taken away (text minus text)", code=_bar("empty = \"░\" * max_mana - \"░\" * mana"),
             fails_at=0, message_contains="unsupported operand type(s) for -: 'str' and 'str'"),
    ],
    notes=_rc_meta("7b", "repeat-string", "mana-bars", level="S4") + "\n"
    "Part 1 item 7 (b): mend `\"░\" * 10 - 3` with the blocks pre-typed, written with the starter's own variables "
    "(`\"░\" * max_mana - mana`), so the mend is rechecked with other numbers (CMB: 3/10, 5/8 and 0/4; a typed 7 "
    "or a typed bar fails). The printed bar must follow too. Item 7 (a), `\"█\" * 3 + \"░\" * 2`, is question i7a. "
    "Fails on (spec): no parentheses -> the run stops. Review routing: hello-world/math-and-glue/repeat-a-mark; "
    "spell-recipes/recipes-read-sheets/bar-then-draw.",
)


# =============================================================================================
# C6 (item 8b) roll-the-die: random.randint(1, die_size) (randint-param; skill-checks). RND.
# =============================================================================================

_ROLL = r'''
_fn, _cases = __FN__, __CASES__
_rfn = _g.get(_fn)
_real = _random.randint
for _size, _roll in _cases:
    _log = []

    def _fake(*_ab, _log=_log, _roll=_roll):
        if len(_ab) != 2:
            return _real(*_ab)  # Python's own TypeError for one number, or three
        _log.append(tuple(_ab))
        return _roll

    _swap = _g.get('randint') is _real
    _random.randint = _fake
    if _swap:
        _g['randint'] = _fake
    try:
        _val, _rows, _e = _call(_rfn, (_size,))
    finally:
        _random.randint = _real
        if _swap:
            _g['randint'] = _real
    _what = 'called ' + _sig(_fn, (_size,))
    assert _e is None, _inside(_fn, ['die_size'], _e) + _ev(_what)
    if not _log:
        assert _val != _size, ('The function does not roll.'
                               + _ev(_what, 'it handed back ' + str(_size) + ', which is `die_size` as it came in'))
        assert False, 'The function does not roll.' + _ev(_what, 'it handed back ' + _num(_val) + ' without rolling')
    _lo, _hi = _log[0]
    _rolled = 'it rolled `random.randint(' + str(_lo) + ', ' + str(_hi) + ')`'
    assert _lo <= _hi, 'The numbers in the roll are in the wrong order.' + _ev(_what, _rolled)
    assert _lo >= 1, 'The roll can give a face the die does not have.' + _ev(_what, _rolled)
    assert _lo == 1, 'The roll misses the lowest face.' + _ev(_what, _rolled + ', which never gives 1')
    assert _hi != _size - 1, 'The roll misses the top face.' + _ev(_what, _rolled + ', which never gives ' + str(_size))
    assert _hi != _size + 1, 'The roll can go past the top face.' + _ev(_what, _rolled)
    assert _hi == _size, 'The top face does not change to match `die_size`.' + _ev(_what, _rolled)
    if _val != _roll:
        assert not (_val is None and _rows), ("The function prints its roll, but hands back `None`, Python's word for "
                                              'nothing.'
                                              + _ev(_what, 'it printed its roll, then handed back `None`'))
        assert _val is not None, ("The roll is never handed back, so the call gets back `None`, Python's word for "
                                  'nothing.' + _ev(_what, 'it rolled, then handed back `None`'))
        assert False, 'The function hands back something other than the roll.' + _ev(_what, 'it handed back ' + _num(_val))
'''

ROLL_OK = "    return random.randint(1, die_size)"


def _roll(body="    return 1", imp="import random\n"):
    return (
        imp
        + "\n\n"
        "# Replace return 1 with a random\n"
        "# number from 1 to die_size.\n"
        "def roll_die(die_size):\n"
        f"{body}\n"
        "\n\n"
        "print(roll_die(6))\n"
    )


ROLL_STARTER = _roll()
ROLL_SOLUTION = _roll(ROLL_OK)

C6_ROLL_THE_DIE = dict(
    id="roll-the-die",
    title="Roll any die",
    martu=(
        "`roll_die` always hands back 1, so the die never really rolls. Make it roll a die with `die_size` faces, "
        "like `perform_roll(die_size)` at the trap door in the campaign. A fair die can land on any of its faces: "
        "a d6 can give 1, 2, 3, 4, 5 or 6. I test it with dice of other sizes.\n" + _STUCK
    ),
    names=["roll_die", "die_size", "random"],
    support="none",
    explainer="lean",
    starter=ROLL_STARTER,
    checkpoints=[
        dict(
            id="roll-to-die-size",
            text="Replace `return 1` on line 7 so `roll_die` hands back a random whole number from 1 to `die_size`.",
            dictated=False,
            hints=[
                "Look at line 1, `import random`. The random numbers come from there.",
                "`random.randint` takes the lowest number and the highest number, and both can come up, like the "
                "faces of a fair die.",
                "The highest face is whatever `die_size` holds when the function is called.",
            ],
            checks=[
                fn_ok("roll_die", ["die_size"]),
                check("roll_die rolls 1 to die_size and returns it", _ROLL, fn="roll_die", cases=[(8, 5), (12, 7)]),
            ],
            pass_line="`roll_die` rolls a die of any size now. Lucky: A d8, a d12, a d6. I'll take any of them.",
        ),
    ],
    solution=ROLL_SOLUTION,
    takeaway="`return random.randint(1, die_size)`: both ends can come up, and the top face changes to match "
             "`die_size`.",
    wrong_answers=[
        dict(why="the starter (return 1)", code=ROLL_STARTER, fails_at=1, message_contains="does not roll"),
        dict(why="a typed d6 (spec: randint(1, 6) -> RND)", code=_roll("    return random.randint(1, 6)"), fails_at=1,
             message_contains="does not change to match `die_size`"),
        dict(why="a typed d20", code=_roll("    return random.randint(1, 20)"), fails_at=1,
             message_contains="does not change to match `die_size`"),
        dict(why="from 0", code=_roll("    return random.randint(0, die_size)"), fails_at=1,
             message_contains="a face the die does not have"),
        dict(why="one short at the top (the range() belief)", code=_roll("    return random.randint(1, die_size - 1)"),
             fails_at=1, message_contains="misses the top face"),
        dict(why="one past the top", code=_roll("    return random.randint(1, die_size + 1)"), fails_at=1,
             message_contains="past the top face"),
        dict(why="print instead of return", code=_roll("    print(random.randint(1, die_size))"), fails_at=1,
             message_contains="prints its roll, but hands back `None`, Python's word for nothing."),
        dict(why="rolled but never handed back", code=_roll("    random.randint(1, die_size)"), fails_at=1,
             message_contains="never handed back"),
        dict(why="the parameter handed back as it came in", code=_roll("    return die_size"), fails_at=1,
             message_contains="as it came in"),
        dict(why="one number in the roll", code=_roll("    return random.randint(die_size)"), fails_at=0,
             message_contains="missing 1 required positional argument: 'b'"),
        dict(why="the numbers swapped", code=_roll("    return random.randint(die_size, 1)"), fails_at=0,
             message_contains="empty range"),
        dict(why="the import removed", code=_roll(ROLL_OK, imp=""), fails_at=0, message_contains="'random' is not defined"),
        dict(why="the parameter's name in quotes (a quoted name): text, not the number it holds",
             code=_roll("    return random.randint(1, \"die_size\")"), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="the parameter renamed", code=_roll(ROLL_OK.replace("die_size", "size")).replace(
            "def roll_die(die_size):", "def roll_die(size):"), fails_at=1, message_contains="parameter names"),
    ],
    notes=_rc_meta("8b", "randint,randint-param", "skill-checks", level="S4") + "\n"
    "Part 1 item 8 (b), the campaign-style starter `def roll_die(die_size): return 1` (G3 R18). RND: the check "
    "swaps `random.randint` for a scripted die that records its arguments, and calls `roll_die(8)` and "
    "`roll_die(12)` (never the task's 6): the roll must be randint(1, die_size) and be handed back. Item 8 (a), which "
    "faces `random.randint(1, 6)` gives, is question i8a. Fails on (spec): `randint(1, 6)` -> RND. Review "
    "routing: control-flow/if-the-clock-turns-red/roll-a-die; first-recipes/recipes-with-names/roll-recipe.",
)


# =============================================================================================
# C7 (item 11) mend-three: three tracebacks, three one-line mends (read-traceback; every part). CMB per line.
# =============================================================================================

MEND_OTHER = 'sheet = {"name": "Pell", "mana": 9, "abilities": {"dexterity": 3}}'
MEND_OTHER_2 = 'sheet = {"name": "Moss", "mana": 31, "abilities": {"dexterity": 3}}'

_MEND_DEX = r'''
_first = dex
_ns, _ls, _e, _miss = _rerun([('sheet', __SHEET__)])
_what = 'ran it again with a test sheet in `sheet`'
assert not _miss, "The line from the code you started with that makes `sheet` is gone."
# A mended sheet, not a mended line: the test sheet keeps only the keys the task names (plain words, then Python's).
assert not (type(_e).__name__ == 'KeyError' and _e.args), ('Your line asks the test sheet for the key `' + repr(_e.args[0] if _e.args else '').replace("'", '"') + '`, and the test sheet has no key spelled that way: it keeps the dexterity inside `"abilities"`.' + _ev(_what))
assert _e is None, 'With a test sheet, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
_v = _ns.get('dex')
if _v != 3:
    assert _v != 7, "`dex` holds a typed-in 7. Mar'tu tested your code with a test sheet in `sheet`, and `dex` still said 7."
    assert type(_v).__name__ != 'dict', '`dex` holds a whole dictionary, not one value from it.' + _ev(_what)
    assert False, '`dex` holds ' + _show(_v) + ', not the dexterity on the sheet.' + _ev(_what)
assert dex == 7, "`dex` holds " + _num(dex) + ", and the sheet's dexterity is 7."
'''

_MEND_MANA = r'''
# Two other sheets: mana 9 (named in the message) and mana 31 (never named), so lines typed to match a message fail.
for _m, _sheet, _shown in __SHEETS__:
    _ns, _ls, _e, _miss = _rerun([('sheet', _sheet)])
    _what = 'ran it again with a test sheet in `sheet`' + _shown
    assert not _miss, "The line from the code you started with that makes `sheet` is gone."
    assert _e is None, 'With a test sheet, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
    if 'Mana: ' + str(_m) not in _ls:
        assert 'Mana: 14' not in _ls, ("The line shows a typed-in 14. Mar'tu tested your code with a test sheet in `sheet`, and "
                                       'the line still said `Mana: 14`.')
        assert 'Mana:  ' + str(_m) not in _ls, ('The line shows two spaces after `Mana:`: the comma adds a space of '
                                                'its own, after the one inside the quotes.' + _ev(_what))
        assert 'Mana: mana' not in _ls, ("The line shows the key's name, `mana`, not the number on the sheet."
                                         + _ev(_what))
        assert False, 'No line shows the mana the way `Mana: 14` does.' + _ev(_what)
    assert 'Mana: 14' not in _ls, ("A line shows a typed-in 14. Mar'tu tested your code with a test sheet in `sheet`, and a "
                                   'line still said `Mana: 14`.')
assert 'Mana: 14' in _lines(), "No line shows Gearshift's mana the way `Mana: 14` does."
'''

_MEND_TOTAL = r'''
_first = total
_ns, _ls, _e, _miss = _rerun([('costs', 'costs = [5, 1, 6, 2]')])
_what = 'used test costs, `[5, 1, 6, 2]`'
assert not _miss, "The line from the code you started with that makes `costs` is gone."
assert _e is None, 'With test costs, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
_v = _ns.get('total')
_loops = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'For']
_reset = [_n for _l in _loops for _s in _l.body for _n in _ast.walk(_s) if type(_n).__name__ == 'Assign'
          and 'total' in _made_by(_n) and type(_n.value).__name__ == 'Constant']
if _v != 14:
    _said = '`total` ended at ' + _num(_v) + ', but the test costs add up to 14'
    assert not (_reset and _v == 2), '`total` goes back to 0 each time through the loop.' + _ev(_what, _said)
    assert _v != 2, '`total` holds only the last cost: each time through the loop, it is replaced, not added to.' + _ev(_what, _said)
    assert _v != 9, ("`total` holds a typed-in 9. Mar'tu tested your code with test costs, `[5, 1, 6, 2]`, and `total` still "
                     'said 9.')
    _typed_add = [_n for _l in _loops for _s in _l.body for _n in _ast.walk(_s)
                  if type(_n).__name__ in ('Assign', 'AugAssign') and 'total' in _made_by(_n)
                  and [_c for _c in _ast.walk(_n.value) if type(_c).__name__ == 'Constant'
                       and type(_c.value).__name__ == 'int']]
    assert not _typed_add, '`total` grows by a typed-in number each time through the loop, not by each cost.' + _ev(_what, _said)
    assert False, '`total` does not add up every cost.' + _ev(_what, _said)
assert '14' in _ls, 'The last line does not print `total`.' + _ev(_what)
assert total == 9, '`total` holds ' + _num(total) + ', and the costs add up to 9.'
'''

MEND_FIXES = [("dex = sheet[\"dexterity\"]", "dex = sheet[\"abilities\"][\"dexterity\"]"),
              ("print(\"Mana: \" + sheet[\"mana\"])", "print(\"Mana: \" + str(sheet[\"mana\"]))"),
              ("    total = total + mana_cots", "    total = total + mana_cost")]


def _mend(line6=None, line7=None, line11=None, before_loop="total = 0\n", in_loop=""):
    """The starter's three broken lines, each one mended (the default) or given."""
    l6, l7, l11 = [fix if mine is None else mine for (bad, fix), mine in zip(MEND_FIXES, (line6, line7, line11))]
    return (
        "sheet = {\n"
        "    \"name\": \"Gearshift\",\n"
        "    \"mana\": 14,\n"
        "    \"abilities\": {\"dexterity\": 7},\n"
        "}\n"
        f"{l6}\n"
        f"{l7}\n"
        "costs = [4, 2, 3]\n"
        f"{before_loop}"
        "for mana_cost in costs:\n"
        f"{in_loop}"
        f"{l11}\n"
        "print(total)\n"
    )


MEND_STARTER = _mend(*[bad for bad, fix in MEND_FIXES])
MEND_SOLUTION = _mend()

C7_MEND_THREE = dict(
    id="mend-three",
    title="Fix three mistakes",
    martu=(
        "Three mistakes, so Python stops three times: first with a `KeyError`, then a `TypeError`, then a "
        "`NameError`. Each time, read the box in the Console like a teacher's note in the margin: "
        "its title says what went wrong, Python's last line says it in Python's words, and the line number says "
        "where. Fix that one line, then press Run again. I test your code with a test sheet and test costs.\n"
        + _STUCK
    ),
    names=["sheet", "dex", "costs", "total", "mana_cost"],
    support="none",
    explainer="lean",
    starter=MEND_STARTER,
    checkpoints=[
        dict(
            id="mend-line-6",
            text="Fix line 6 so `dex` holds the dexterity on the sheet.",
            dictated=False,
            hints=[
                "Press Run. Read the box in the Console: which key could Python not find?",
                "Look at the sheet on lines 1 to 5. Is `\"dexterity\"` on the big sheet, or inside `\"abilities\"`?",
                "A value in a sheet inside a sheet needs two keys in a row, outside first.",
            ],
            checks=[check("dex is read from inside the sheet", _MEND_DEX, sheet=MEND_OTHER)],
        ),
        dict(
            id="mend-line-7",
            text="Fix line 7 so it prints the mana, like `Mana: 14`.",
            dictated=False,
            hints=[
                "Read the box in the Console. What can text be glued to with `+`?",
                "`+` glues text to text, like a compound word. A number has to become text first.",
                "Look at `sheet[\"mana\"]` on line 7: is it text or a number?",
            ],
            checks=[check("the mana line follows the sheet", _MEND_MANA,
                          sheets=[(9, MEND_OTHER, ", mana 9"), (31, MEND_OTHER_2, "")])],
        ),
        dict(
            id="mend-line-11",
            text="Fix line 11 so `total` adds up every cost.",
            dictated=False,
            hints=[
                "Read the box in the Console. Which name is not defined?",
                "Python matches names letter for letter, like a password. Compare line 11 with the `for` line, line 10.",
                "Look at the loop variable's name on line 10, letter by letter.",
            ],
            checks=[check("total adds up every cost", _MEND_TOTAL)],
            pass_line="All three lines are fixed, and `total` adds up. Gearshift: Three mistakes, three fixes. Math checks out.",
        ),
    ],
    solution=MEND_SOLUTION,
    takeaway="Read the box: its title, then Python's last line, then the line number. Here: a missing key, text "
             "glued to a number, a misspelled name.",
    wrong_answers=[
        dict(why="the starter (line 6 first)", code=MEND_STARTER, fails_at=0, message_contains="KeyError: 'dexterity'"),
        dict(why="line 6 left: a skipped nesting level", code=_mend(line6=MEND_FIXES[0][0]), fails_at=0,
             message_contains="KeyError: 'dexterity'"),
        dict(why="line 6 typed (CMB)", code=_mend(line6="dex = 7"), fails_at=1,
             message_contains="`dex` holds a typed-in 7. Mar'tu tested your code with a test sheet in `sheet`"),
        dict(why="line 6 one level short", code=_mend(line6="dex = sheet[\"abilities\"]"), fails_at=1,
             message_contains="a whole dictionary"),
        dict(why="line 7 left: str() missing before + (spec)", code=_mend(line7=MEND_FIXES[1][0]), fails_at=0,
             message_contains="can only concatenate str (not \"int\") to str"),
        dict(why="line 7 typed (CMB)", code=_mend(line7="print(\"Mana: \" + \"14\")"), fails_at=2,
             message_contains="The line shows a typed-in 14"),
        dict(why="line 7: the key's name glued on (a quoted name), not the number",
             code=_mend(line7="print(\"Mana: \" + str(\"mana\"))"), fails_at=2, message_contains="the key's name"),
        dict(why="line 6 dodged: a dexterity key typed onto the top of the sheet (the nesting level still skipped)",
             code=_mend(line6=MEND_FIXES[0][0]).replace("\"abilities\": {\"dexterity\": 7},\n",
                                                       "\"abilities\": {\"dexterity\": 7},\n    \"dexterity\": 7,\n"),
             fails_at=1, message_contains="asks the test sheet for the key `\"dexterity\"`"),
        dict(why="line 7 with a comma and the space kept (two spaces)",
             code=_mend(line7="print(\"Mana: \", sheet[\"mana\"])"), fails_at=2,
             message_contains="the comma adds a space of its own"),
        dict(why="line 11 left (spec: the NameError)", code=_mend(line11=MEND_FIXES[2][0]), fails_at=0,
             message_contains="'mana_cots' is not defined"),
        dict(why="the total reset inside the loop (resetting a total inside a loop)",
             code=_mend(before_loop="", in_loop="    total = 0\n"), fails_at=3, message_contains="back to 0 each time"),
        dict(why="the rerun's total typed (main run)", code=_mend(line11="    total = 14"), fails_at=3,
             message_contains="add up to 9"),
        dict(why="the total replaced, not added to", code=_mend(line11="    total = mana_cost"), fails_at=3,
             message_contains="only the last cost"),
        dict(why="a typed 3 added each time round (9 for these costs, by luck)", code=_mend(line11="    total = total + 3"),
             fails_at=3, message_contains="grows by a typed-in number"),
        dict(why="the total typed (CMB)", code=_mend(line11="    total = 9"), fails_at=3,
             message_contains="`total` holds a typed-in 9. Mar'tu tested your code with test costs, `[5, 1, 6, 2]`"),
        dict(why="line 11 mended to the list, not the loop variable", code=_mend(line11="    total = total + costs"),
             fails_at=0, message_contains="unsupported operand"),
    ],
    notes=_rc_meta(11, "read-traceback", "every part", level="S4") + "\n"
    "Part 1 item 11: three one-line bugs, top to bottom, so Python reports them in order: `KeyError: 'dexterity'` "
    "(a skipped nesting level, line 6), `TypeError: can only concatenate str (not \"int\") to str` (line 7), "
    "`NameError: name 'mana_cots' is not defined` (line 11, inside a loop that totals the costs). Every slip "
    "crashes until it is mended, so there are no partials (as QC1 C5): reading the message is the skill. Each "
    "checkpoint reruns with other values (another sheet: Pell, mana 9, dexterity 3; costs 5, 1, 6, 2), so a typed "
    "7, 14 or 9 fails. The loop catches the class's 'resetting a total inside a loop' (`total = 0` moved in). "
    "Fails on (spec): each left -> the run stops. Review routing: control-flow/when-spells-fizzle/debug-routine; "
    "dictionaries/stat-sheets/key-errors; loops/for-each-yes/running-total.",
)


# =============================================================================================
# C8 (item 12) spend-the-cost: hero["mana"] = hero["mana"] - cost (dict-write, reassign, combine-values;
# hold-the-barrier). Typed (G2 R17), CMB.
# =============================================================================================

_SPEND = r'''
_first = hero
_ns, _ls, _e, _miss = _rerun([('hero', 'hero = {"name": "Pell", "mana": 15}'), ('cost', 'cost = 4')])
_what = "used a test hero, Pell, with mana 15, and a test cost of 4"
assert not _miss, "The line from the code you started with that makes `" + (_miss or [''])[0] + '` is gone.'
assert _e is None, 'With a test sheet and cost, Python stopped with the error ' + _err(_e) + '.' + _ev(_what)
_h = _ns.get('hero')
assert type(_h).__name__ == 'dict', '`hero` is not a dictionary any more: it holds ' + _show(_h) + '.' + _ev(_what)
_now = _h.get('mana')
if _now != 11:
    _said = "Pell's mana ended at " + _num(_now)
    if _now == 15:
        _cmp = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare'
                and type(_n.value.ops[0]).__name__ == 'Eq']
        assert not _cmp, ('Line ' + str(_cmp[0].lineno if _cmp else 0) + ' uses `==`, which only compares, so nothing '
                          'was stored.' + _ev(_what, _said))
        _loose = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ in ('Constant', 'BinOp')]
        assert not _loose, ('Line ' + str(_loose[0].lineno if _loose else 0) + ' works out a value, but nothing stores '
                            'it, so Python reads it and throws it away.' + _ev(_what, _said))
        _extra = [_k for _k in _h if _k not in ('name', 'mana')]
        assert not _extra, 'A new key went into `hero`, and its `"mana"` did not change.' + _ev(_what, _said)
        _kept = sorted(_k for _k, _x in _ns.items() if not _k.startswith('_') and type(_x).__name__ == 'int'
                       and _x == 11)
        assert not _kept, ('The new mana went into `' + (_kept or [''])[0] + '`, and `hero["mana"]` did not change.'
                           + _ev(_what, _said))
        assert '11' not in _ls, 'The new mana was printed, but `hero["mana"]` did not change.' + _ev(_what, _said)
        assert False, '`hero["mana"]` did not change.' + _ev(_what, _said)
    assert _now != 17, ('`hero["mana"]` holds a typed-in 17. ' + "Mar'tu tested your code with a test sheet in `hero` and "
                        'a test cost in `cost`, and `hero["mana"]` still said 17.')
    # Both test values the result depends on are named (Pell's 15 mana and the cost of 4), then the answer.
    assert _now != 15 - 9, ("The line takes away a typed-in 9, not what `cost` holds. Mar'tu tested it with a made-up "
                            "hero, Pell, with 15 mana, and a test cost of 4: Pell should end at 11, but ended at 6.")
    assert _now != 26 - 4, ('The line starts from a typed-in 26, not from `hero["mana"]`. ' + "Mar'tu tested it with a "
                            "made-up hero, Pell, with 15 mana, and a test cost of 4: Pell should end at 11, but ended "
                            "at 22.")
    assert _now != 15 + 4, '`hero["mana"]` went up.' + _ev(_what, _said)
    assert False, '`hero["mana"]` does not drop by `cost`.' + _ev(_what, _said + ', not 11')
# The main run, read against the starter's own numbers (a sheet or a cost with other numbers typed in still passes).
_ns0, _ls0, _e0, _miss0 = _rerun([('hero', '_start = hero["mana"]'), ('cost', '_spent = cost')])
_s0, _c0 = _ns0.get('_start'), _ns0.get('_spent')
if type(_s0).__name__ == 'int' and type(_c0).__name__ == 'int':
    assert hero.get('mana') == _s0 - _c0, ("Lucky's mana ended at " + _num(hero.get('mana')) + ', and ' + str(_s0)
                                           + ' minus ' + str(_c0) + ' is ' + str(_s0 - _c0) + '.')
'''


def _spend(line=""):
    return (
        "hero = {\"name\": \"Lucky\", \"mana\": 26}\n"
        "cost = 9\n"
        "# Spend cost from hero[\"mana\"].\n"
        f"{line}"
        "\n"
        "print(hero[\"mana\"])\n"
    )


SPEND_OK = "hero[\"mana\"] = hero[\"mana\"] - cost\n"
SPEND_STARTER = _spend()
SPEND_SOLUTION = _spend(SPEND_OK)

C8_SPEND_THE_COST = dict(
    id="spend-the-cost",
    title="Spend the cost",
    martu=(
        "Lucky casts a spell, and it costs mana, his magic power. Write one line that spends `cost` from the mana "
        "on his sheet, so the sheet's mana goes down, like a bank balance after you buy something. I test your code "
        "with a test sheet and a test cost.\n" + _STUCK
    ),
    names=["hero", "cost"],
    support="none",
    explainer="lean",
    starter=SPEND_STARTER,
    checkpoints=[
        dict(
            id="spend-cost",
            text="Take `cost` away from `hero[\"mana\"]`, so the sheet keeps the new mana. Write the line under the "
                 "comment on line 3.",
            dictated=False,
            hints=[
                "Look at the comment on line 3, then at the `print` line. Which value must change?",
                "Like a bank balance: a new value goes back into the same key with `=`, and the right side can read "
                "the old value first.",
                "The line starts `hero[\"mana\"] =`.",
            ],
            checks=[check("the hero's mana drops by cost", _SPEND)],
            pass_line="The mana on Lucky's sheet went down by `cost`. Lucky: 17 left. I'm keeping track.",
        ),
    ],
    solution=SPEND_SOLUTION,
    takeaway="`hero[\"mana\"] = hero[\"mana\"] - cost` reads the old mana, takes away the cost, and stores the "
             "new mana on the sheet, like a bank balance.",
    wrong_answers=[
        dict(why="the starter (nothing spent)", code=SPEND_STARTER, fails_at=1, message_contains="did not change"),
        dict(why="the answer typed (spec: hero[\"mana\"] = 17 -> CMB)", code=_spend("hero[\"mana\"] = 17\n"),
             fails_at=1, message_contains="`hero[\"mana\"]` holds a typed-in 17"),
        dict(why="worked out, never stored (spec: hero[\"mana\"] - cost with no store)",
             code=_spend("hero[\"mana\"] - cost\n"), fails_at=1, message_contains="nothing stores it"),
        dict(why="a dash for = (group 1's slip): one long subtraction, never stored",
             code=_spend("hero[\"mana\"] - hero[\"mana\"] - cost\n"), fails_at=1, message_contains="nothing stores it"),
        dict(why="the answer as a lone number (BARE)", code=_spend("17\n"), fails_at=1,
             message_contains="nothing stores it"),
        dict(why="== for = (= vs ==): compared, never stored",
             code=_spend("hero[\"mana\"] == hero[\"mana\"] - cost\n"), fails_at=1, message_contains="only compares"),
        dict(why="stored in a new variable", code=_spend("mana = hero[\"mana\"] - cost\n"), fails_at=1,
             message_contains="went into `mana`"),
        dict(why="stored in cost", code=_spend("cost = hero[\"mana\"] - cost\n"), fails_at=1,
             message_contains="went into `cost`"),
        dict(why="printed, never stored", code=_spend("print(hero[\"mana\"] - cost)\n"), fails_at=1,
             message_contains="was printed"),
        dict(why="the cost typed (CMB)", code=_spend("hero[\"mana\"] = hero[\"mana\"] - 9\n"), fails_at=1,
             message_contains="The line takes away a typed-in 9, not what `cost` holds"),
        dict(why="the starting mana typed (CMB)", code=_spend("hero[\"mana\"] = 26 - cost\n"), fails_at=1,
             message_contains="The line starts from a typed-in 26"),
        dict(why="a new key with a capital (KEY)", code=_spend("hero[\"Mana\"] = hero[\"mana\"] - cost\n"), fails_at=1,
             message_contains="A new key"),
        dict(why="the rerun's answer typed (main run)", code=_spend("hero[\"mana\"] = 11\n"), fails_at=1,
             message_contains="26 minus 9 is 17"),
        dict(why="the sign the other way", code=_spend("hero[\"mana\"] = hero[\"mana\"] + cost\n"), fails_at=1,
             message_contains="went up"),
        dict(why="the subtraction the wrong way round", code=_spend("hero[\"mana\"] = cost - hero[\"mana\"]\n"),
             fails_at=1, message_contains="does not drop by `cost`"),
        dict(why="the whole sheet replaced by the number", code=_spend("hero = hero[\"mana\"] - cost\n"), fails_at=0,
             message_contains="'int' object is not subscriptable"),
    ],
    notes=_rc_meta(12, "dict-write,reassign,combine-values", "hold-the-barrier", level="S2") + "\n"
    "Part 1 item 12, typed (G2 R17): the check reruns with another sheet (Pell, mana 15) and another cost (4), so "
    "only the line built from the sheet and `cost` passes (CMB). `-=` passes too. Fails on (spec): "
    "`hero[\"mana\"] = 17` -> CMB; `hero[\"mana\"] - cost` with no store. Also named: the new mana kept in a new "
    "variable or in `cost`, printed only, a typed cost or start, a capital key, the sign or the order reversed. "
    "Review routing: hello-world/math-and-glue/spend-mana; dictionaries/stat-sheets/write-by-key.",
)


# =============================================================================================
# C9 (item 13) glug-cost: a function from its goal, with an Example on screen (param-use, return-right-name,
# exact-names; every part with parameters). NAME/DEF + PAR / PAR-CONST / RET / PNM / RNM.
# =============================================================================================

_RET = r'''
_fn, _ps, _cases, _foreign, _goal, _follow = __FN__, __PARAMS__, __CASES__, __FOREIGN__, __GOAL__, __FOLLOW__
_f = _g[_fn]
_d = _defs().get(_fn)
_rets = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return'] if _d else []
_nothing = ", Python's word for nothing."
_seen = []
for _args, _want in _cases:
    _args = tuple(_args)
    _val, _rows, _e = _call(_f, _args)
    _what = 'called ' + _sig(_fn, _args)
    assert _e is None, _inside(_fn, _ps, _e, _foreign) + _ev(_what)
    _seen.append((_args, _want, _val, _rows, _what))
for _args, _want, _val, _rows, _what in _seen:
    if _val is None:
        assert not _rows, 'The function prints its answer, but hands back `None`' + _nothing + _ev(_what)
        assert _rets, ('`' + _fn + '` has no `return` line, so the call gets back `None`' + _nothing + _ev(_what))
        assert [_x for _x in _rets if _x.value is not None], ('The `return` line has nothing after it, so the function hands back `None`'
                                                             + _nothing + _ev(_what))
        assert False, 'No `return` line ran for this call, so it got back `None`' + _nothing + _ev(_what)
_made = (_locals_of(_d) if _d else []) + list(_ps)
for _args, _want, _val, _rows, _what in _seen:
    if type(_val).__name__ == 'str':
        assert _val not in _made, ("The function hands back a variable's name in quotes, not what the variable holds."
                                   + _ev(_what, 'it handed back some text'))
        assert False, 'The function hands back text, not a number.' + _ev(_what, 'it handed back some text')
(_a1, _w1, _v1, _r1, _t1), (_a2, _w2, _v2, _r2, _t2) = _seen[0], _seen[1]
assert not (_v1 == _v2 and type(_v1) == type(_v2) and _w1 != _w2), (
    'Two calls with different numbers handed back the same answer, ' + _num(_v1) + '. The numbers are typed into the '
    'function, so the answer does not change to match ' + _names(_ps) + '.'
    + " Mar'tu tested your code: he called " + _sig(_fn, _a1) + ' and ' + _sig(_fn, _a2) + '.')
# A typed number in a sum, and a parameter the function never reads: `sips * 3` in place of `sips * price_per_sip`.
_read = set(_n.id for _n in _ast.walk(_d) if type(_n).__name__ == 'Name') if _d else set()
_unread = [_p for _p in _ps if _p not in _read]
_how = {'Mult': ('multiplies by', 'not by'), 'Add': ('adds', 'not'), 'Sub': ('takes away', 'not'),
        'Div': ('divides by', 'not by')}
_typed = [(_how[type(_b.op).__name__], _x.value) for _b in (_ast.walk(_d) if _d else [])
          if type(_b).__name__ == 'BinOp' and type(_b.op).__name__ in _how for _x in (_b.left, _b.right)
          if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'int']
for _args, _want, _val, _rows, _what in _seen:
    if _val != _want:
        _same = [_p for _p, _x in zip(_ps, _args) if _x == _val and type(_x) == type(_val)]
        assert not _same, 'The function hands back `' + (_same or [''])[0] + '` as it came in.' + _ev(_what, 'it handed back ' + _num(_val))
        _said = 'it handed back ' + _num(_val) + ', not ' + str(_want)
        if _typed and _unread:
            (_verb, _nob), _k = _typed[0]
            assert False, ('The function ' + _verb + ' a typed-in ' + str(_k) + ', ' + _nob + ' `' + _unread[0]
                           + '`, so the answer does not change when ' + _follow.get(_unread[0], '`' + _unread[0]
                                                                                   + '` does') + '.'
                           + _ev(_what, _said))
        assert False, _goal + _ev(_what, _said)
'''

GLUG_SIG = "def glug_cost(sips, price_per_sip):"
GLUG_BODY = "    total = sips * price_per_sip\n    return total"
GLUG_FOREIGN = ["triple", "n", "result"]
GLUG_CALL = "# Lucky: 4 sips, 3 coins a sip.\nprint(glug_cost(4, 3))\n"
# The same numbered comments as forms B and C give their function-from-its-goal task.
GLUG_HEAD = (
    "# 1. Make glug_cost, with the\n"
    "#    parameters sips and\n"
    "#    price_per_sip.\n"
    "# 2. Return the total cost.\n"
)


def _glug(body=None, sig=GLUG_SIG, call=True):
    fn = f"{sig}\n{body}\n\n\n" if body is not None else "\n\n"
    return GLUG_HEAD + fn + (GLUG_CALL if call else "")


GLUG_STARTER = _glug()
GLUG_SOLUTION = _glug(GLUG_BODY)

C9_GLUG_COST = dict(
    id="glug-cost",
    title="Write a function from its goal",
    martu=(
        "Lucky sells sips of glug, his drink. Write the whole function from its goal. Like a formula in math, "
        "area = length × width, it must work for any numbers, not only for one call. The Example shows the shape "
        "with its own names, not yours. I test your function with other numbers.\n" + _STUCK
    ),
    example=(
        "def triple(n):\n"
        "    result = n * 3\n"
        "    return result\n"
        "\n\n"
        "print(triple(5))\n"
    ),
    example_output="15",
    names=["glug_cost", "sips", "price_per_sip"],
    support="none",
    explainer="lean",
    starter=GLUG_STARTER,
    checkpoints=[
        dict(
            id="write-glug-cost",
            text="Make a function named `glug_cost` with two parameters, `sips` and `price_per_sip`. Write it on "
                 "line 5, under the numbered comments. It hands back the total cost: the number of sips times the "
                 "price of one sip.",
            dictated=False,
            hints=[
                "The `def` line names the function and both parameters, then a colon. The body is indented.",
                "Inside, use the parameters' names, like the blanks in a Mad Lib. Each call fills them with its own "
                "numbers.",
                "The Example's last line is `return result`. This function hands back its own total.",
            ],
            checks=[
                fn_ok("glug_cost", ["sips", "price_per_sip"], GLUG_FOREIGN),
                check("glug_cost returns the total", _RET, fn="glug_cost", params=["sips", "price_per_sip"],
                      cases=[((5, 4), 20), ((7, 6), 42)], foreign=GLUG_FOREIGN,
                      goal="The function does not hand back the number of sips times the price of one sip.",
                      follow={"sips": "the number of sips does", "price_per_sip": "the price does"}),
            ],
            pass_line="`glug_cost` works for any sips at any price. Lucky: 12 coins for 4 sips. Deal.",
        ),
    ],
    solution=GLUG_SOLUTION,
    takeaway="Use the task's own names, not the Example's. The parameters go in, and your function hands back its "
             "own total.",
    wrong_answers=[
        dict(why="the starter (no function yet: the call stops the run)", code=GLUG_STARTER, fails_at=0,
             message_contains="'glug_cost' is not defined"),
        dict(why="no function and no call", code=_glug(call=False), fails_at=1,
             message_contains="No line makes a function"),
        dict(why="return result (spec: RNM), with the call",
             code=_glug("    total = sips * price_per_sip\n    return result"), fails_at=0,
             message_contains="'result' is not defined"),
        dict(why="return result (spec: RNM), no call",
             code=_glug("    total = sips * price_per_sip\n    return result", call=False), fails_at=1,
             message_contains="a name from the Example"),
        dict(why="return sips * 2 (spec: PAR)", code=_glug("    return sips * 2"), fails_at=1,
             message_contains="The function multiplies by a typed-in 2, not by `price_per_sip`, so the answer does not "
                              "change when the price does."),
        dict(why="the Example's 3 copied (PAR: a typed number, a parameter never read)",
             code=_glug("    return sips * 3"), fails_at=1,
             message_contains="multiplies by a typed-in 3, not by `price_per_sip`"),
        dict(why="a typed 4, the first check call's price: right for (5, 4), wrong for (7, 6)",
             code=_glug("    total = sips * 4\n    return total"), fails_at=1,
             message_contains="a typed-in 4, not by `price_per_sip`"),
        dict(why="the sips typed, the price read (the other parameter never read)",
             code=_glug("    return 4 * price_per_sip"), fails_at=1,
             message_contains="not by `sips`, so the answer does not change when the number of sips does"),
        dict(why="a typed number added, the price never read", code=_glug("    return sips + 3"), fails_at=1,
             message_contains="The function adds a typed-in 3, not `price_per_sip`"),
        dict(why="price * sips (spec: PNM), with the call", code=_glug("    return price * sips"), fails_at=0,
             message_contains="'price' is not defined"),
        dict(why="price * sips (spec: PNM), no call", code=_glug("    return price * sips", call=False), fails_at=1,
             message_contains="not one of this function's parameters"),
        dict(why="a literal (spec: PAR-CONST)", code=_glug("    return 12"), fails_at=1,
             message_contains="handed back the same answer, 12. The numbers are typed into the function, so the answer "
                              "does not change to match `sips` and `price_per_sip`."),
        dict(why="one call's numbers typed (the class's `10 * 5` slip)", code=_glug("    return 4 * 3"), fails_at=1,
             message_contains="the answer does not change to match `sips` and `price_per_sip`"),
        dict(why="print instead of return (None)", code=_glug("    print(sips * price_per_sip)"), fails_at=1,
             message_contains="prints its answer, but hands back `None`, Python's word for nothing."),
        dict(why="stored, then printed, never handed back (None)",
             code=_glug("    total = sips * price_per_sip\n    print(total)"), fails_at=1,
             message_contains="but hands back `None`, Python's word for nothing"),
        dict(why="no return (None)", code=_glug("    total = sips * price_per_sip"), fails_at=1,
             message_contains="`glug_cost` has no `return` line, so the call gets back `None`, Python's word for "
                              "nothing."),
        dict(why="a blank return (None)", code=_glug("    total = sips * price_per_sip\n    return"), fails_at=1,
             message_contains="has nothing after it, so the function hands back `None`, Python's word for nothing"),
        dict(why="the return inside a test that never runs (None)",
             code=_glug("    total = sips * price_per_sip\n    if total > 100:\n        return total"), fails_at=1,
             message_contains="No `return` line ran for this call, so it got back `None`"),
        dict(why="a parameter handed back as it came in", code=_glug("    return sips"), fails_at=1,
             message_contains="as it came in"),
        dict(why="plus for times", code=_glug("    return sips + price_per_sip"), fails_at=1, message_contains="not 20"),
        dict(why="handed back as text", code=_glug("    return str(sips * price_per_sip)"), fails_at=1,
             message_contains="hands back text"),
        dict(why="the total's name handed back in quotes (a quoted name)",
             code=_glug("    total = sips * price_per_sip\n    return \"total\""), fails_at=1,
             message_contains="name in quotes"),
        dict(why="short parameter names (approximate names)",
             code=_glug("    return sips * price", sig="def glug_cost(sips, price):"), fails_at=1,
             message_contains="not the task's parameter names"),
        dict(why="the parameters in the other order",
             code=_glug(GLUG_BODY, sig="def glug_cost(price_per_sip, sips):"), fails_at=1,
             message_contains="another order"),
        dict(why="one parameter", code=_glug("    return sips * 3", sig="def glug_cost(sips):"), fails_at=0,
             message_contains="takes 1 positional argument"),
        dict(why="one parameter, no call", code=_glug("    return sips * 3", sig="def glug_cost(sips):", call=False),
             fails_at=1, message_contains="parentheses hold 1"),
        dict(why="the colon left off", code=_glug(GLUG_BODY, sig=GLUG_SIG[:-1]), fails_at=0,
             message_contains="expected ':'"),
        dict(why="def used to make a variable (def vs =)", code="def glug_cost = 12\n" + GLUG_CALL, fails_at=0,
             message_contains="expected '('"),
        dict(why="= used for the function (def vs =), no call", code="glug_cost = 4 * 3\n", fails_at=1,
             message_contains="made with `=`"),
        dict(why="the Example's name, no call", code=_glug(GLUG_BODY, sig="def triple(sips, price_per_sip):", call=False),
             fails_at=1, message_contains="Example's function"),
        dict(why="a capital letter in the name, no call",
             code=_glug(GLUG_BODY, sig="def Glug_cost(sips, price_per_sip):", call=False), fails_at=1,
             message_contains="letter for letter"),
        dict(why="a typo of its own variable, no call",
             code=_glug("    total = sips * price_per_sip\n    return totl", call=False), fails_at=1,
             message_contains="not a variable in this function"),
    ],
    notes=_rc_meta(13, "param-use,return-right-name,exact-names", "every part with parameters",
                   foreign="triple,n,result", level="S0") + "\n"
    "Part 1 item 13 (directive 4.6): a goal and an Example (`def triple(n): result = n * 3; return result`) on "
    "screen; the starter has two numbered comments (make it with its parameters, return the total cost), as "
    "forms B and C give theirs, and the call. PAR with fresh calls (5, 4) -> 20 and (7, 6) -> 42 "
    "(neither is 12, the task's own call, lint b; and neither price is 2 or 3, so `sips * 2` and the Example's "
    "`* 3` fail). Fails on (spec): `return result` -> RNM; `return sips * 2` -> PAR; `price * sips` -> PNM; a "
    "literal -> PAR-CONST. With the call in place, `result` and `price` stop the run first and the explainer "
    "answers; without it, the check's own lean RNM / PNM messages answer (both proven). Messages name the slip "
    "in the class's words: `None` is 'Python's word for nothing' (no return, a print, a blank return, a return "
    "that never ran); PAR-CONST says the numbers are typed in the function, so the answer does not follow the "
    "parameters; a typed number with a parameter never read names both (`sips * 3`: 'multiplies by a typed 3, "
    "not by `price_per_sip`'; `sips * 4` passes the first call and fails the second). Required to pass for "
    "'Ready' (5.5). Review routing: first-recipes/recipes-with-names/use-the-ingredients, return-the-right-box.",
)



# =============================================================================================
# Part 1 form A: the testout (the 9 code tasks) and its questions (12 questions from items 1, 3-10)
# =============================================================================================

RC_PART1_A = dict(
    kind="testout",
    id="rc-part1-a",
    title="Readiness Check · Part 1 · Form A",
    optional=False,
    minutes=18,
    summary=(
        "Part 1, second half: nine short tasks, with no hints. The glossary, read-aloud and the error box in the "
        "Console still work. To pass Part 1, pass all nine tasks and get 10 of the 12 questions right. Missed one? "
        "Open *Mar'tu's Notes: Where to Look Again*, right after this."
    ),
    questions_to_pass=10,
    exercises=[C1_STEP_WEST, C2_PRESENT_WARNING, C3_MEND_THE_CHOICE, C4_READ_THE_SHEET, C5_MEND_THE_BAR,
               C6_ROLL_THE_DIE, C7_MEND_THREE, C8_SPEND_THE_COST, C9_GLUG_COST],
    notes=(
        "Readiness Check Part 1, form A (curriculum 5.2, 5.3): the 9 code items, in the spec's order (items 2, 3b, "
        "5b, 6a-c, 7b, 8b, 11, 12, 13). The questions (items 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, 10a, 10b) live "
        "in rc-part1-a-questions, which comes first in the unit's list, so the first win is a prediction; this "
        "form follows it, and rc-review (Mar'tu's Notes) follows this form. Unaided: support='none' and "
        "explainer='lean' on every task; glossary and read-aloud stay on (G1 R25). Every typed task is "
        "behavior-checked (CMB, PAR, BND, CALL, RND, STO, KEY), never OUT alone (T5). Pass heuristic (5.5), as far "
        "as the schema can hold it: every code task (the testout's rule) plus questions_to_pass=10 of 12, which "
        "approximates 'Part 1 >= 11/13' (two question misses allowed). 'Item 6 at >= 3 of 4 parts' and 'item 13 "
        "passed' hold automatically, since items 6a-c and 13 are required tasks.\n"
        "This is the required form: optional=False, the only testout in the course that is not optional. The "
        "site's Readiness flow lists it as a core item and never tests the unit out with it (site request: a "
        "required testout is a core item, with no unit test-out, so passing it, or a later form or rc-recheck, "
        "never marks the mini-boss or rc-explain as tested out). Forms B (u10b) and C (u10c) are the optional "
        "retakes.\n"
        "What the site still lacks (site work): per-item scoring (13 items, mixed code and question parts), the "
        "Ready / Ready with a review list / Review first result, per-skill review routing as links (rc-review "
        "names them in prose; each task's notes list its review exercises), and form choice (a retake draws form "
        "B or C, and a quiz retake draws another form's questions). ~28 minutes in all (10 for the questions, 18 "
        "for the tasks)."
    ),
)


def _q(item, skills, prepares, fails, extra=""):
    return (f"Item {item}. Skills: {skills}. Prepares: {prepares}. Fails on (spec): {fails}." + (" " + extra if extra
                                                                                               else ""))


RC_PART1_A_QUESTIONS = dict(
    kind="quiz",
    id="rc-part1-a-questions",
    title="Readiness Check · Part 1 · Form A questions",
    optional=False,
    minutes=10,
    summary=(
        "Part 1 starts here: twelve questions about what code prints, which line runs, and what a line means. "
        "No hints. Then come nine short tasks."
    ),
    questions=[
        dict(
            type="predict",
            id="i1-mana-line",
            q="What will this code print?",
            code=(
                "full = str(7) + \"/\" + str(10)\n"
                "print(\"Mana: \" + full)\n"
            ),
            answer="Mana: 7/10",
            choices=["Mana:7/10", "Mana: 7/10", "Mana: 7 / 10", "Mana: 17"],
            explain=(
                "`str(7)` and `str(10)` turn the numbers into text. Then `+` glues the pieces like a compound word, "
                "with no spaces added. The only space is the one inside `\"Mana: \"`."
            ),
            notes=_q(1, "concat-str", "mana-bars (the return line)", "Mana:7/10, Mana: 7 / 10",
                     "Written on two lines to fit a phone (the spec's one line is 41 characters). 17 is the "
                     "'adds the numbers' belief."),
        ),
        dict(
            type="predict",
            id="i3a-the-board",
            q="`get_warning()` tidies its line with `.lower()`, then `.capitalize()`. What will this code print?",
            code=(
                "def get_warning():\n"
                "    line = \"STAY IN, LUCKY. NOW.\"\n"
                "    line = line.lower()\n"
                "    line = line.capitalize()\n"
                "    return line\n"
                "\n\n"
                "print(get_warning())\n"
            ),
            answer="Stay in, lucky. now.",
            choices=["Stay In, Lucky. Now.", "Stay in, Lucky. Now.", "Stay in, lucky. now.", "stay in, lucky. now."],
            explain=(
                "`.lower()` makes every letter small. Then `.capitalize()` makes only the very first letter big. "
                "It is not like sentence case in Google Docs: names and new sentences get no capital, so even Lucky's "
                "name stays small."
            ),
            notes=_q("3a", "chain-methods", "program-dialogue-prompt", "the line kept as it was, or every word "
                     "capitalized", "Another line than task C2's, so that task's run never answers this."),
        ),
        dict(
            type="predict",
            id="i4a-latch-check",
            q="`latch_check` passes when the roll is at least 11. What will this code print?",
            code=(
                "def latch_check(roll):\n"
                "    needed = 11\n"
                "    return roll >= needed\n"
                "\n\n"
                "print(latch_check(10))\n"
                "print(latch_check(11))\n"
                "print(latch_check(12))\n"
            ),
            answer="False\nTrue\nTrue",
            choices=["False\nFalse\nTrue", "True\nTrue\nTrue", "False\nTrue\nTrue", "False\nTrue\nFalse"],
            explain=(
                "`>=` means *at least*, like the filled dot on a number line: 11 itself counts. 10 is short, so "
                "`False`. 11 is exactly enough, so `True`. 12 is more than enough, so `True`."
            ),
            notes=_q("4a", "boundary,return-comparison", "skill-checks", "11 -> False"),
        ),
        dict(
            type="predict",
            id="i4b-the-ledger",
            q="Trace this program like a ledger: write down what each variable holds, one line at a time, the way "
              "you show your work in math. Then type the number it prints.",
            code=(
                "def lamp_glow(oil, wicks):\n"
                "    light = oil * 10\n"
                "    spark = wicks * 4\n"
                "    return light + spark\n"
                "\n\n"
                "glow = lamp_glow(3, 5) + 8\n"
                "print(glow)\n"
            ),
            answer="58",
            explain=(
                "Here is the same kind of trace for another call, `lamp_glow(1, 2) + 8`. `oil` gets 1 and `wicks` "
                "gets 2, so `light` is 10 and `spark` is 8. The call hands back 18, and the line adds 8, so it prints 26. "
                "Trace yours the same way, with what is *in* the variables.\n"
                "If you got 22, you added the numbers written in the function, 10 + 4, then the 8. If you got 16, "
                "you added the numbers handed over, 3 + 5, then the 8."
            ),
            notes=_q("4b", "trace-call", "skill-checks", "the 15-type value (the code's numbers added: 10 + 4 + 8 = "
                     "22) and the 7-type value (the numbers handed over added: 3 + 5 + 8 = 16)",
                     "The ward_strength ledger shape with new names and numbers. Typed, with no choices, as forms B "
                     "and C: honest tracing, so the right value is in no visible text (no choice shows it, and the "
                     "explanation shown after the answer traces another call, `lamp_glow(1, 2) + 8`, so a retake is "
                     "not handed it). A question, so there is no editor to paste into and nothing to run (no "
                     "paste_stop needed), and no Assemble. 50 is 'forgot the + 8'."),
        ),
        dict(
            type="predict",
            id="i5a-which-branch",
            q="`choice` holds `\"option 2\"`. What will this code print?",
            code=(
                "choice = \"option 2\"\n"
                "if choice == \"option 1\":\n"
                "    print(\"Oogrish waits.\")\n"
                "elif choice == \"option 2\":\n"
                "    print(\"Gearshift goes.\")\n"
                "else:\n"
                "    print(\"Lucky stays.\")\n"
            ),
            answer="Gearshift goes.",
            choices=["Oogrish waits.", "Gearshift goes.", "Gearshift goes.\nLucky stays.", "Oogrish waits.\nGearshift goes."],
            explain=(
                "Python checks the chain from the top and stops at the first question that is `True`, like a grading "
                "scale. `choice == \"option 1\"` is `False`, so it skips that branch. `choice == \"option 2\"` is "
                "`True`, so `Gearshift goes.` prints, and Python skips the rest of the chain."
            ),
            notes=_q("5a", "elif-chain", "program-dialogue-options", "the first branch"),
        ),
        dict(
            type="predict",
            id="i6d-in-the-book",
            q="`in` asks about a dictionary's keys. What will this code print?",
            code=(
                "book = {\"Glow\": 2, \"Hush\": 5}\n"
                "print(\"Glow\" in book)\n"
                "print(2 in book)\n"
            ),
            answer="True\nFalse",
            choices=["True\nTrue", "True\nFalse", "False\nTrue", "False\nFalse"],
            explain=(
                "`in` looks only at the keys, the way you check a glossary for a word, not for its meaning. "
                "`\"Glow\"` is a key, so `True`. 2 is a value, not a key, so `False`."
            ),
            notes=_q("6d", "dict-in", "spell-book, hold-the-barrier (the guard)", "2 in book -> True"),
        ),
        dict(
            type="predict",
            id="i7a-the-bar",
            q="What will this code print?",
            code="print(\"█\" * 3 + \"░\" * 2)\n",
            answer="███░░",
            choices=["█3░2", "███░░", "█████", "█ █ █ ░ ░"],
            explain="Text times a number repeats it, the way 3 × 4 means 4 + 4 + 4: three `█`, then two `░`, glued "
                    "together with no spaces.",
            notes=_q("7a", "repeat-string", "mana-bars", "█3░2"),
        ),
        dict(
            type="mc",
            id="i8a-die-faces",
            q="Which numbers can `random.randint(1, 6)` give?",
            choices=["1, 2, 3, 4 or 5", "0, 1, 2, 3, 4 or 5", "1, 2, 3, 4, 5 or 6", "Only 1 or 6"],
            answer=2,
            why_wrong={
                0: "That is what `range(1, 6)` gives, which stops before 6. `randint` can give both ends.",
                1: "`randint` starts at the first number you give it: 1, not 0.",
                3: "Every whole number from 1 to 6 can come up, not only the two ends.",
            },
            explain="`random.randint(1, 6)` rolls like a fair d6, a die with 6 faces: any whole number from 1 to 6, "
                    "and both 1 and 6 can come up.",
            notes=_q("8a", "randint", "skill-checks", "1-5 (the range() belief)"),
        ),
        dict(
            type="mc",
            id="i9a-explain-the-brackets",
            q="Which sentence says what `spells[\"glow\"]` and `spells[\"glow\"](pell)` each do?",
            code=(
                "def glow(hero):\n"
                "    print(hero[\"name\"] + \" glows.\")\n"
                "\n\n"
                "spells = {\"glow\": glow}\n"
                "pell = {\"name\": \"Pell\"}\n"
            ),
            choices=[
                "Both run the spell on Pell.",
                "The first is the function itself, not run. The second runs it on Pell.",
                "The first runs the spell. The second stores Pell in the book.",
                "The first is the word glow. The parentheses turn it into a function.",
            ],
            answer=1,
            why_wrong={
                0: "Only parentheses after it, like `(pell)`, run a function. `spells[\"glow\"]` on its own only reads it.",
                2: "Nothing is stored: `(pell)` hands Pell to the function and runs it.",
                3: "The value under the key `\"glow\"` is the function `glow`, not text.",
            },
            explain=(
                "In math class, f names a function and f(3) works it out. In the same way, `spells[\"glow\"]` reads "
                "the function stored under `\"glow\"` without running it, and `(pell)` on the end runs it on Pell."
            ),
            notes=_q("9a", "func-as-value,call-stored-func", "spell-book, hold-the-barrier", "'both run the spell'"),
        ),
        dict(
            type="predict",
            id="i9b-what-runs",
            q="Here is the same spell book. What will this code print?",
            code=(
                "def glow(hero):\n"
                "    print(hero[\"name\"] + \" glows.\")\n"
                "\n\n"
                "spells = {\"glow\": glow}\n"
                "pell = {\"name\": \"Pell\"}\n"
                "found = spells[\"glow\"]\n"
                "found(pell)\n"
                "spells[\"glow\"]\n"
            ),
            answer="Pell glows.",
            choices=["Pell glows.\nPell glows.", "glows.", "Pell glows.", "Pell glows.\nNone"],
            explain=(
                "`found = spells[\"glow\"]` stores the function itself, so `found(pell)` runs it on Pell: one line. "
                "The last line only reads the function, with no parentheses after it, so nothing more prints. It is "
                "like writing f without (3): you named the function, but you didn't use it."
            ),
            notes=_q("9b", "func-as-value,call-stored-func", "spell-book, hold-the-barrier",
                     "'both run the spell' (two lines)"),
        ),
        dict(
            type="predict",
            id="i10a-trace-the-loop",
            q="Trace the loop one hero at a time. What will this code print?",
            code=(
                "def show_status(hero):\n"
                "    name = hero[\"name\"]\n"
                "    print(name, hero[\"mana\"])\n"
                "\n\n"
                "roster = [\n"
                "    {\"name\": \"Moss\", \"mana\": 3},\n"
                "    {\"name\": \"Pell\", \"mana\": 7},\n"
                "    {\"name\": \"Brakka\", \"mana\": 9},\n"
                "]\n"
                "for hero in roster:\n"
                "    show_status(hero)\n"
            ),
            answer="Moss 3\nPell 7\nBrakka 9",
            choices=["Brakka 9", "Moss 3\nPell 7\nBrakka 9", "Moss Pell Brakka 3 7 9", "Moss 3"],
            explain=(
                "The loop takes the heroes one at a time, in order, like a teacher calling roll. Each time through, "
                "`show_status` prints one line: Moss 3, then Pell 7, then Brakka 9."
            ),
            notes=_q("10a", "list-of-dicts,for-each", "the bottom loops of spell-book and mana-bars",
                     "'one call with the whole roster' (one line with every name)"),
        ),
        dict(
            type="mc",
            id="i10b-explain-the-loop",
            q="What do the last two lines, the `for` loop, do?",
            code=(
                "def show_status(hero):\n"
                "    name = hero[\"name\"]\n"
                "    print(name, hero[\"mana\"])\n"
                "\n\n"
                "roster = [\n"
                "    {\"name\": \"Moss\", \"mana\": 3},\n"
                "    {\"name\": \"Pell\", \"mana\": 7},\n"
                "    {\"name\": \"Brakka\", \"mana\": 9},\n"
                "]\n"
                "for hero in roster:\n"
                "    show_status(hero)\n"
            ),
            choices=[
                "It calls `show_status` once, with the whole roster.",
                "It calls `show_status` three times, with the whole roster each time.",
                "It makes three new functions, one for each hero.",
                "It calls `show_status` three times, once with each hero's sheet.",
            ],
            answer=3,
            why_wrong={
                0: "The indented line under `for` runs once for each item in the list, so there are three calls, "
                   "not one.",
                1: "Each time through the loop, `hero` holds one sheet from the list, not the whole list.",
                2: "Nothing new is made: the loop calls the same function, three times.",
            },
            explain=(
                "Three sheets, three calls, like a teacher calling roll: one name at a time. Each time through the "
                "loop, `hero` holds the next sheet, and the call hands that one sheet over. The loops at the bottom "
                "of the campaign's code work the same way."
            ),
            notes=_q("10b", "list-of-dicts,for-each", "the bottom loops of spell-book and mana-bars",
                     "'one call with the whole roster'"),
        ),
    ],
    notes=(
        "Readiness Check Part 1, form A questions, first in the unit's list (so the first win is a prediction), "
        "scored with rc-part1-a: every code task plus 10 of these 12 (questions_to_pass=10 on the testout). The "
        "best score counts; a retake should draw another form's questions (site work). i4b is typed, with no "
        "choices (honest tracing). Unaided: no hints; glossary and read-aloud "
        "stay on. Each question's notes give its 5.3 item, skill tags and the campaign part it prepares. Right "
        "answers sit at varied positions (the site also shuffles). Every predict answer is proved by the harness "
        "running the code."
    ),
)


# =============================================================================================
# Review routing (5.2 "Review routing", 5.5 "Review first"): Mar'tu's notes, right after Part 1 form A. For each
# Part 1 item, the earlier exercises to open again, each in a different representation from the unaided check.
# (unit order, unit id, lesson id, lesson title, exercise id, exercise title, the help to use there). Checked against
# the staged units: every id exists, and the help named is on that exercise (a worked example, Assemble it, a
# step-by-step Another way angle, "the step table", or the ledger itself). The first route of each item is its "Start here" lesson.
# u10c keeps an identical copy of ROUTES for its form C tasks' `review=` meta lines: THE TWO MUST MATCH (change both,
# or neither).
# =============================================================================================

ROUTES = {
    1: ("glue text with `+` and `str()`", "concat-str", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "glue-words", "Glue words together", "the worked example"),
        (1, "hello-world", "math-and-glue", "Math and Glue", "status-line", "A status line", "Assemble it"),
    ]),
    2: ("replace `pass`", "replace-pass", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "replace-pass", "Replace pass", "Assemble it"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "call-it", "Call it", "the worked example"),
    ]),
    3: ("tidy a line, store it, then pass it on", "chain-methods,store-then-pass", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "store-then-pass", "Store, then pass it on",
         "Assemble it"),
        (7, "spell-recipes", "recipes-read-sheets", "Recipes That Read Stat Sheets", "bar-then-draw",
         "Build the bar, then draw it", "the step table"),
    ]),
    4: ("exactly enough, and tracing a call", "boundary,return-comparison,trace-call", [
        (2, "control-flow", "true-or-false-yes", "True or False, Yes?", "enough-to-pass", "Enough to pass",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "return-a-comparison", "Return a comparison",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "be-the-ledger", "Be the ledger",
         "the ledger"),
    ]),
    5: ("which branch runs, and text in quotes", "elif-chain,quote-text", [
        (2, "control-flow", "if-the-clock-turns-red", "If the Clock Turns Red", "clock-colors", "Clock colors",
         "the step table"),
        (1, "hello-world", "words-in-quotes", "Words in Quotes", "words-need-quotes", "Words need quotes",
         "the worked example"),
    ]),
    6: ("read and write a stat sheet", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable", [
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "read-by-key", "Read by key", "the worked example"),
        (5, "dictionaries", "sheets-inside-sheets", "Sheets Inside Sheets", "abilities-inside", "Abilities inside",
         "the worked example"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "key-from-a-box", "A key from a box", "Assemble it"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "is-it-in", "Is it in the book?", "the worked example"),
    ]),
    7: ("a bar of blocks", "repeat-string", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "repeat-a-mark", "Repeat a mark", "Assemble it"),
        (7, "spell-recipes", "recipes-read-sheets", "Recipes That Read Stat Sheets", "bar-then-draw",
         "Build the bar, then draw it", "the step table"),
    ]),
    8: ("roll a die", "randint,randint-param", [
        (2, "control-flow", "if-the-clock-turns-red", "If the Clock Turns Red", "roll-a-die", "Roll a die",
         "the worked example"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "roll-recipe", "A rolling recipe",
         "Assemble it"),
    ]),
    9: ("a function stored in a dictionary", "func-as-value,call-stored-func", [
        (7, "spell-recipes", "spells-you-can-hand-over", "Spells You Can Hand Over", "name-without-parentheses",
         "A name without parentheses", "the step table"),
        (7, "spell-recipes", "spells-you-can-hand-over", "Spells You Can Hand Over", "cast-from-the-book",
         "Cast from the book", "Assemble it"),
    ]),
    10: ("a loop over a list of sheets", "list-of-dicts,for-each", [
        (6, "loops", "for-each-yes", "For Each, Yes?", "predict-the-loop", "Predict the loop", "the step table"),
        (5, "dictionaries", "sheets-inside-sheets", "Sheets Inside Sheets", "the-roster", "The roster",
         "the worked example"),
    ]),
    11: ("read the error box, then fix the line", "read-traceback", [
        (2, "control-flow", "when-spells-fizzle", "When Spells Fizzle: Reading Errors", "debug-routine",
         "The four-step routine", "Assemble it"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "key-errors", "Key errors", "Assemble it"),
        (6, "loops", "for-each-yes", "For Each, Yes?", "running-total", "Running total", "the step table"),
    ]),
    12: ("spend mana from a sheet", "dict-write,reassign,combine-values", [
        (1, "hello-world", "math-and-glue", "Math and Glue", "spend-mana", "Spend some mana", "the step table"),
        (5, "dictionaries", "stat-sheets", "Stat Sheets", "write-by-key", "Write by key", "the worked example"),
    ]),
    13: ("write a function from its goal", "param-use,return-right-name,exact-names", [
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "use-the-ingredients", "Use the ingredients",
         "Assemble it"),
        (3, "first-recipes", "recipes-with-names", "Recipes With Names", "return-the-right-box", "Return the right box",
         "Assemble it"),
        (1, "hello-world", "boxes-with-labels", "Boxes With Labels", "exact-names", "Exact names", "Assemble it"),
    ]),
}


def _review(item):
    """`review=` for a meta line: the item's routes as unit/lesson/exercise ids."""
    return ",".join(f"{unit}/{lesson}/{ex}" for _, unit, lesson, _, ex, _, _ in ROUTES[item][2])


# What students saw for each item, form by form (curriculum 5.2 "Review routing", the teacher's directive: each line
# starts with the titles students saw). The questions go by their number in the form's questions (*Readiness Check ·
# Part 1 · Form A / B / C questions*: the same numbers in every form, item for item), the code tasks by their titles.
# The titles are copied from u10a, u10b and u10c as staged: THEY MUST MATCH the three files (checked by script).
# Form A comes first in the class's order, so forms B and C hold the twins.
_QUESTIONS = {1: "question 1", 3: "question 2", 4: "questions 3 and 4", 5: "question 5", 6: "question 6",
              7: "question 7", 8: "question 8", 9: "questions 9 and 10", 10: "questions 11 and 12"}
_TASKS = {
    "A": {2: "Step west", 3: "Store, then pass it on", 5: "Fix the third choice", 6: "Read and write the sheet",
          7: "Fix the mana bar", 8: "Roll any die", 11: "Fix three mistakes", 12: "Spend the cost",
          13: "Write a function from its goal"},
    "B": {2: "Step east", 3: "Store, then pass it on", 5: "Fix the reply", 6: "Read and write the sheets",
          7: "Fix the bar", 8: "Roll the die", 11: "Fix three mistakes", 12: "Spend the mana", 13: "Shield cost"},
    "C": {2: "Step north", 3: "Store, then pass it on", 5: "Fix the reply", 6: "Read and write the sheets",
          7: "Fix the gauge", 8: "Roll the die", 11: "Fix three mistakes", 12: "Spend the mana", 13: "Fuel cost"},
}


def _seen(item, form):
    """What a student of `form` saw for `item`: its question(s) first (they come first), then its task's title."""
    parts = ([_QUESTIONS[item]] if item in _QUESTIONS else []) + (
        ["*" + _TASKS[form][item] + "*"] if item in _TASKS[form] else [])
    return " and ".join(parts)


def _seen_by_form(item):
    """The line's opening: each different thing students saw, with the forms that showed it, e.g.
    '*Fix the third choice* (A) · *Fix the reply* (B, C)'."""
    groups = []
    for form in "ABC":
        label = _seen(item, form)
        same = [g for g in groups if g[0] == label]
        if same:
            same[0][1].append(form)
        else:
            groups.append((label, [form]))
    text = " · ".join(f"{label} (Form{'s' if len(forms) > 1 else ''} {', '.join(forms[:-1]) + ' and ' if len(forms) > 1 else ''}{forms[-1]})"
                      for label, forms in groups)
    return text[0].upper() + text[1:]


_HOW = {"the worked example": "read the Example", "Assemble it": "use Assemble it", "the ledger": "fill in the ledger"}

# "the step table": the exercise's step-by-step Another way angle (the site has no live tracer yet: curriculum "once
# the tracer ships"). The Learn pane's button says "Explain it another way: <label>", then "Another way: <label>", so
# the line names the label the student will see on it (the exported angle labels, checked by script).
_STEP_TABLE = {"clock-colors": "Trace 2, 7 and 20", "spend-mana": "Step table", "predict-the-loop": "The loop table",
               "running-total": "Trace table", "bar-then-draw": "Step by step", "name-without-parentheses": "Step by step"}


def _how(how, ex):
    if how == "the step table":
        return f"press *Explain it another way* until the button says *{_STEP_TABLE[ex]}*"
    return _HOW[how]


def _route_line(item):
    """One line per item: the titles students saw, the skill, the Start here lesson, the other lessons, the twins."""
    what, _skills, routes = ROUTES[item]
    places = [f"Unit {unit_no} · {lesson_title} · *{ex_title}*: {_how(how, ex)}"
              for unit_no, _unit, _lesson, lesson_title, ex, ex_title, how in routes]
    also = (" Also: " + "; ".join(places[1:]) + ".") if places[1:] else ""
    return (f"{_seen_by_form(item)}: {what}. Start here: {places[0]}.{also} "
            f"Then try its twin in Form B, {_seen(item, 'B')}, or in Form C, {_seen(item, 'C')}.")


REVIEW_BODY = (
    "After Part 1, the unit page shows *Your Readiness Check*: your own misses, each with a link to its lesson. "
    "Or find the task or question you missed by its title below. Open the exercise after *Start here*, and use its "
    "help this time: the Example, Assemble it, a step table under *Explain it another way*, or the ledger. Then try "
    "only its twin, the matching task in Form B or Form C, not the whole form. For a question, open that form's "
    "questions and answer up to its number: each right answer counts as soon as you check it.\n"
    + "\n".join(_route_line(item) for item in sorted(ROUTES)) + "\n"
    "In the campaign, the error box is shorter: you see only Python's own message. Read its last line first. It "
    "says what went wrong, and the line number says where.\n"
    "Mar'tu: A miss is not a wall. It only shows me where we look again, yes?\n"
    "After two rounds of review, we go on anyway. The story never waits for a perfect score."
)

RC_REVIEW = dict(
    kind="article",
    id="rc-review",
    title="Mar'tu's Notes: Where to Look Again",
    optional=True,
    minutes=15,
    summary=(
        "Optional. Missed a task or a question in Part 1? Find it here by its title: one lesson to open first, then "
        "the matching task in another form."
    ),
    body=REVIEW_BODY,
    notes=(
        "Review routing (curriculum 5.2 'Review routing', 5.5 'Review first'), as far as the schema can hold it: "
        "an article right after Part 1 form A (moved here from u10c), with one line per Part 1 item, in the "
        "teacher's shape: '*Fix the third choice* (Form A) · *Fix the reply* (Forms B and C): which branch runs. "
        "Start here: ... Also: ... Then try its twin in Form B, *Fix the reply*, or in Form C, *Fix the "
        "reply*.' Each line starts with the "
        "titles students saw in each form (the code tasks' titles, and the questions by their number in the form's "
        "questions, the same numbers in forms A, B and C), names the skill and the item, marks one Start here "
        "lesson (the item's first route), lists the other earlier exercises to open again (Also), each in a "
        "different representation from the unaided check (a worked example, Assemble it, a step table, the ledger), "
        "then names the twins of forms B and C (the titles in _TASKS are copied from u10a, u10b and u10c as staged: "
        "they must match). The opening tells the student to try only the missed task's twin, not the whole form. "
        "The intro card and rc-part1-a's summary "
        "point here by title. The 5.2 'Explainer parity' line is here too. The routes, as unit/lesson/exercise ids "
        "(u10c keeps an identical ROUTES copy for its form C tasks' `review=` meta lines):\n"
        + "\n".join(f"item {item} ({skills}): {_review(item)}" for item, (_, skills, _) in sorted(ROUTES.items()))
        + "\nEvery id was checked against the staged units, and the help named is on that exercise (EX: a worked "
        "example; ASM: Assemble it; TR: the step-by-step Another way angle, named by its button label; be-the-ledger is the ledger itself). Site work: links from the "
        "Readiness result to these exercises (prose has no item links), showing only the missed items' lines, "
        "counting review cycles (two, then continue with the teacher flag 'Needs you now'), and drawing the "
        "parallel item from another form."
    ),
)


# =============================================================================================
# Part 2: mini-boss A "Hold the Lantern Ward" (5.4), campaign mode for everyone (2.10). The near-transfer of
# hold-the-barrier: cast_ward(hero, ward_name). Six checks, mirroring the campaign's, in its order.
# =============================================================================================

HERO_NAMES = ["Oogrish", "Gearshift", "Bomb Shell", "Lucky"]

# Hidden setup: Gearshift's sheet (the party table: affinity 10, max mana 20) with the Lantern Ward in his wards,
# and the ward's effect, which records who it was cast on (an engine-like helper, 2.12 rule 3).
MB_SETUP = (
    "_effects = []\n"
    "\n\n"
    "def lantern_ward(hero):\n"
    "    _effects.append(hero)\n"
    "    print(hero[\"name\"] + \"'s lantern ward glows.\")\n"
    "\n\n"
    "gearshift = {\n"
    "    \"name\": \"Gearshift\",\n"
    "    \"mana\": 20,\n"
    "    \"max_mana\": 20,\n"
    "    \"abilities\": {\"magical_affinity\": 10},\n"
    "    \"wards\": {\n"
    "        \"Lantern Ward\": {\n"
    "            \"mana_cost\": 6,\n"
    "            \"required_affinity\": 9,\n"
    "            \"effect\": lantern_ward,\n"
    "        },\n"
    "    },\n"
    "}\n"
)
SHOW_MANA = (
    "def show_mana(hero):\n"
    "    full = hero[\"mana\"]\n"
    "    used = hero[\"max_mana\"] - full\n"
    "    bar = \"█\" * full + \"░\" * used\n"
    "    print(hero[\"name\"], bar)\n"
)
MB_HEAD = (
    "# Already finished. Leave it as\n"
    "# it is.\n"
    + SHOW_MANA
    + "\n\n"
    "def cast_ward(hero, ward_name):\n"
    "    if ward_name not in hero[\"wards\"]:\n"
    "        print(hero[\"name\"], \"doesn't know\", ward_name)\n"
    "        return\n"
    "    ward = hero[\"wards\"][ward_name]\n"
    "\n"
    "    # An if, an elif and an else.\n"
    "    # Numbers are the check order.\n"
    "    # Code order: test 3, test 4,\n"
    "    # then else: 1 and 2.\n"
    "    # 1. A skilled hero with enough\n"
    "    #    mana casts the ward's\n"
    "    #    effect.\n"
    "    # 2. Then the mana goes down by\n"
    "    #    the ward's cost, and the\n"
    "    #    bar is drawn again.\n"
    "    # 3. Too little affinity: print\n"
    "    #    why, and no cast.\n"
    "    # 4. Otherwise, too little\n"
    "    #    mana: print why, no cast.\n"
    "    # 5. Exactly enough mana casts.\n"
    "    # 6. Use the ward's own cost.\n"
)
MB_CALL = "\n\ncast_ward(gearshift, \"Lantern Ward\")\n"
AFF = "hero[\"abilities\"][\"magical_affinity\"] < ward[\"required_affinity\"]"
MANA = "hero[\"mana\"] < ward[\"mana_cost\"]"
EFFECT = "ward[\"effect\"](hero)"
PAY = "        hero[\"mana\"] = hero[\"mana\"] - ward[\"mana_cost\"]\n"
TYPED_PAY = "        hero[\"mana\"] = hero[\"mana\"] - 6\n"
SKILL_MSG = "        print(hero[\"name\"], \"isn't skilled enough.\")\n"
MANA_MSG = "        print(hero[\"name\"], \"doesn't have enough mana.\")\n"
SHOW = "        show_mana(hero)\n"


def _mb_body(aff=AFF, mana=MANA, effect=EFFECT, pay=PAY, show=SHOW, skill_msg=SKILL_MSG, mana_msg=MANA_MSG):
    return (f"    if {aff}:\n" + skill_msg + f"    elif {mana}:\n" + mana_msg + "    else:\n"
            f"        {effect}\n" + pay + show)


def _mb(body="    pass\n", head=MB_HEAD, call=MB_CALL):
    return head + body + call


def _flat(lines):
    """Cast lines moved one step out (straight in the function, not under a branch)."""
    return "".join(line[4:] if line.startswith("        ") else line for line in lines)


MB_STARTER = _mb()
MB_SOLUTION = _mb(_mb_body())
MB_P1 = _mb(f"    {EFFECT}\n")
MB_P2 = _mb(_flat([f"        {EFFECT}\n", TYPED_PAY, SHOW]))
MB_P3 = _mb(f"    if {AFF}:\n" + SKILL_MSG + "    else:\n" + f"        {EFFECT}\n" + TYPED_PAY + SHOW)
MB_P4 = _mb(_mb_body(mana=MANA.replace("<", "<="), pay=TYPED_PAY))
MB_P5 = _mb(_mb_body(pay=TYPED_PAY))

_MB_PRE = r'''
_fd = _defs().get('cast_ward')
assert _fd is not None and callable(_g.get('cast_ward')), 'Keep `cast_ward` from the code you started with, made with `def`.'
assert [_a.arg for _a in _fd.args.args] == ['hero', 'ward_name'], (
    'Keep the `def` line from the code you started with: `def cast_ward(hero, ward_name):`.')
_wrong_sheet = bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Name' and _n.id == 'gearshift'])
_guard_ifs = [_n for _n in _fd.body if type(_n).__name__ == 'If' and type(_n.test).__name__ == 'Compare'
              and type(_n.test.ops[0]).__name__ == 'NotIn']
_ifs = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'If' and _n not in _guard_ifs]
_typed_cmp = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Compare'
              and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
                   and type(_x.value).__name__ == 'int']]
_max_read = bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Subscript'
                  and type(_n.slice).__name__ == 'Constant' and _n.slice.value == 'max_mana'])
_into_ward = [_n for _n in _ast.walk(_fd) if type(_n).__name__ in ('Assign', 'AugAssign')
              and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
                   if type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name' and _t.value.id == 'ward']]


def _why(_m):
    if _wrong_sheet:
        return "`cast_ward` uses `gearshift` by name, so Brakka's cast used Gearshift's sheet."
    if _max_read:
        return '`cast_ward` reads `"max_mana"`, the most a hero can hold, not the mana they have now.'
    return _m


def _test(_r, _said=''):
    # The mini-boss's evidence: short sentences after the slip, never brackets inside brackets.
    return (" Mar'tu tested your code with a made-up hero and ward: " + _r['who'] + ' has affinity ' + str(_r['aff']) + ' and mana '
            + str(_r['mana']) + '. Moon Step costs ' + str(_r['cost']) + ' and needs affinity ' + str(_r['need'])
            + '.' + ((' ' + _said) if _said else ''))


def _cast(_aff, _mana, _cost, _need):
    _fx = []

    def moon_step(hero):
        _fx.append(hero)
        print('Moon Step lands.')

    _hero = {'name': 'Brakka', 'mana': _mana, 'max_mana': 20, 'abilities': {'magical_affinity': _aff},
             'wards': {'Moon Step': {'mana_cost': _cost, 'required_affinity': _need, 'effect': moon_step}}}
    _bars = []

    def _drawn(hero):
        _bars.append((hero, hero.get('mana') if type(hero).__name__ == 'dict' else None))

    _real = _g.get('show_mana')
    _w0 = len(_g.get('_effects', []))
    _g['show_mana'] = _drawn
    try:
        _val, _ls, _x = _call(_g['cast_ward'], (_hero, 'Moon Step'))
    finally:
        _g['show_mana'] = _real
    return dict(fx=_fx, msgs=[_l for _l in _ls if _l != 'Moon Step lands.'], left=_hero['mana'], bars=_bars,
                wards=_g.get('_effects', [])[_w0:], err=_x, hero=_hero, who='Brakka', aff=_aff, mana=_mana,
                cost=_cost, need=_need)


def _crash(_r):
    _e = _r['err']
    if type(_e).__name__ == 'NameError' and getattr(_e, 'name', '') == 'caster':
        return "`caster` was the name in the campaign. It is not one of this function's parameters." + _test(_r)
    if type(_e).__name__ == 'KeyError' and _e.args and _e.args[0] == 'Lantern Ward':
        return ('`cast_ward` reads the ward `"Lantern Ward"` by a typed-in name, not by the name in `ward_name`.'
                + _test(_r, "Mar'tu's test hero has no Lantern Ward, so Python could not find that key."))
    return 'Inside `cast_ward`, Python stopped with the error ' + _err(_e) + '.' + _test(_r)
'''

_MB_CASTS = r'''
_r = _cast(12, 15, 5, 7)
assert _r['err'] is None, _crash(_r)
if not _r['fx']:
    _bare = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Subscript']
    assert not _bare, "The ward's effect is read, but nothing calls it." + _test(_r, 'Moon Step never ran.')
    _by_name = [_c for _c in _ast.walk(_fd) if _is_call(_c, 'lantern_ward')]
    assert not (_r['wards'] and _by_name), ('`lantern_ward` is called by its own name, so every ward would cast the '
                                            'Lantern Ward.' + _test(_r, 'The Lantern Ward ran instead.'))
    assert not _r['wards'], (_why("The Lantern Ward ran, not the ward named in `ward_name`.")
                             + _test(_r, 'The Lantern Ward ran instead.'))
    _said_fx = [_l for _l in _r['msgs'] if 'glows' in _l.lower()]
    assert not _said_fx, ("The effect's words were printed, but the ward's effect never ran."
                          + _test(_r, 'Moon Step never ran.'))
    assert not _r['msgs'], _why('A skilled hero with enough mana was turned away.') + _test(_r)
    assert False, "A skilled hero with enough mana did not cast: the ward's effect never ran." + _test(_r)
assert len(_r['fx']) == 1, "The ward's effect ran more than once in one cast." + _test(_r)
assert _r['fx'][0] is _r['hero'], _why("The ward's effect was handed another sheet, not the hero who cast.") + _test(_r)
assert 'None' not in _r['msgs'], ("A `print(...)` around a call showed `None`, Python's word for nothing."
                                  + _test(_r))
'''

_MB_BAR = r'''
_r = _cast(12, 15, 5, 7)
assert _r['err'] is None, _crash(_r)
_still = 'Brakka still has 15 mana.'
if _r['left'] == 15:
    _sub = [_n for _n in _ast.walk(_fd) if (type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp')
            or (type(_n).__name__ == 'Assign' and type(_n.targets[0]).__name__ == 'Name'
                and type(_n.value).__name__ == 'BinOp')]
    assert not _sub, 'The new mana is worked out, but `hero["mana"]` never changes.' + _test(_r, _still)
    assert not _into_ward, "The new mana went into the ward's page, not the hero's sheet." + _test(_r, _still)
    assert False, _why("After the cast, the hero's mana did not go down.") + _test(_r, _still)
assert _r['left'] < 15, ("After the cast, the hero's mana went up."
                         + _test(_r, 'The mana went up to ' + str(_r['left']) + '.'))
_bare_show = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Name'
              and _n.value.id == 'show_mana']
assert _r['bars'] or not _bare_show, ('`show_mana` has no `()` after it, so it is never called.'
                                      + _test(_r, 'The bar was not drawn again.'))
assert _r['bars'], 'After the cast, `show_mana` was not called, so the bar was not drawn again.' + _test(_r)
_hb, _mb = _r['bars'][-1]
assert _hb is _r['hero'], _why('`show_mana` was handed another sheet, not the hero who cast.') + _test(_r)
assert _mb == _r['left'], ('The bar was drawn before the mana went down, so it shows the old mana.'
                           + _test(_r, 'The bar showed ' + str(_mb) + ' mana. The mana ended at '
                                   + str(_r['left']) + '.'))
'''

_MB_TURNS_AWAY = r'''
def _effect_line(_s):
    return (type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Call'
            and type(_s.value.func).__name__ == 'Subscript')


def _open_chain(_s):
    # an if (or an if / elif chain) with no last `else`
    while len(_s.orelse) == 1 and type(_s.orelse[0]).__name__ == 'If':
        _s = _s.orelse[0]
    return not _s.orelse


# An `if` with no `else` straight in the function, and the cast still at function level below it: the hero is told
# why, then casts anyway (the cast lines were never moved under `else:`).
_open_if = [_i for _i, _s in enumerate(_fd.body) if type(_s).__name__ == 'If' and _open_chain(_s)
            and _s not in _guard_ifs]
_no_else = bool(_open_if) and bool([_i for _i, _s in enumerate(_fd.body) if _effect_line(_s) and _i > _open_if[0]])
for _aff, _mana, _cost, _need, _kind in __CASES__:
    _r = _cast(_aff, _mana, _cost, _need)
    assert _r['err'] is None, _crash(_r)
    if _kind == 'low':
        if _r['fx']:
            _anyway = _r['who'] + ' cast it anyway.'
            assert not (_r['msgs'] and _no_else), ('The hero is told why, then casts anyway: the cast lines are not '
                                                   'inside the last branch, `else`.'
                                                   + _test(_r, 'The message showed, then ' + _anyway))
            assert not _typed_cmp, __TYPED__ + _test(_r, _anyway)
            assert False, _why(__TURN_AWAY__) + _test(_r, _anyway)
        assert _r['left'] == _mana, ('Nothing was cast, but the mana still went down.'
                                     + _test(_r, 'The mana ended at ' + str(_r['left']) + '.'))
        assert _r['msgs'], 'The hero was turned away, but nothing was printed to say why.' + _test(_r)
        assert len(_r['msgs']) == 1, 'One cast printed ' + str(len(_r['msgs'])) + ' messages.' + _test(_r)
        _named = [_n for _n in __HEROES__ if _n in _r['msgs'][0]]
        assert not _named, ('A message names ' + (_named or [''])[0] + ', a typed-in name, not the hero who cast.'
                            + _test(_r))
    else:
        assert _r['fx'], __EXACT__ + _test(_r, _r['who'] + ' was turned away.')
'''

# Too little affinity and too little mana are two reasons: one message for each, not the same words for both (form
# B's check, with form A's names).
_MB_TWO_REASONS = r'''
_a = _cast(5, 15, 5, 7)
_b = _cast(12, 3, 5, 7)
assert _a['err'] is None, _crash(_a)
assert _b['err'] is None, _crash(_b)
assert not (_a['msgs'] and _a['msgs'] == _b['msgs']), (
    'Too little mana printed the same message as too little affinity.'
    + " Mar'tu tested your code with a made-up hero and ward. Moon Step costs 5 and needs affinity 7. Brakka tried it twice: with "
    'affinity 5 and mana 15, then with affinity 12 and mana 3. The same message showed both times.')
'''

_MB_OWN_COST = r'''
_res = []
for _mana, _cost in ((15, 3), (14, 8)):
    _r = _cast(12, _mana, _cost, 7)
    assert _r['err'] is None, _crash(_r)
    _res.append((_mana, _cost, _r))
_pays = [_n for _n in _ast.walk(_fd) if type(_n).__name__ in ('Assign', 'AugAssign')
         and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
              if type(_t).__name__ == 'Subscript' and type(_t.slice).__name__ == 'Constant' and _t.slice.value == 'mana']]
_typed_pay = [_c for _p in _pays for _c in _ast.walk(_p.value) if type(_c).__name__ == 'Constant'
              and type(_c.value).__name__ == 'int']
_same = _res[0][2]['left'] == _res[1][2]['left']
for _mana, _cost, _r in _res:
    _want = _mana - _cost
    if _r['left'] != _want:
        _end = _test(_r, 'The mana ended at ' + str(_r['left']) + ', not ' + str(_want) + '.')
        assert _r['left'] != _mana - 6, "The mana went down by a typed-in 6, not by the ward's own cost." + _end
        assert _r['left'] != _cost - _mana, 'The subtraction runs the wrong way: the cost minus the mana.' + _end
        assert _r['left'] != 15 - _cost, 'The new mana starts from a typed-in 15, not from the hero' + "'s mana." + _end
        assert not _same, ('`hero["mana"]` holds a typed-in ' + str(_r['left']) + ": Mar'tu cast twice, with "
                           'test mana and a test cost, and the mana still ended at ' + str(_r['left']) + '.'
                           + _end)
        assert not _typed_pay, "The mana goes down by a typed-in number, not by the ward's own cost." + _end
        assert False, _why("The mana did not go down by the ward's own cost.") + _end
'''


# The starter's guard still turns away a ward the hero doesn't know (it is given; a check keeps it honest).
_MB_GUARD = r'''
_fx = []


def frost_veil(hero):
    _fx.append(hero)


_hero = {'name': 'Moss', 'mana': 15, 'max_mana': 20, 'abilities': {'magical_affinity': 12},
         'wards': {'Frost Veil': {'mana_cost': 5, 'required_affinity': 7, 'effect': frost_veil}}}
_real = _g.get('show_mana')
_w0 = len(_g.get('_effects', []))
_g['show_mana'] = lambda hero: None
try:
    _val, _ls, _e = _call(_g['cast_ward'], (_hero, 'Moon Step'))
finally:
    _g['show_mana'] = _real
_tail = " Mar'tu tested your code with a made-up hero, Moss, who knows only Frost Veil and tried to cast Moon Step."
assert _e is None, ("The guard from the code you started with no longer turns away a ward the hero doesn't know."
                    + _tail + ' Moss has no Moon Step, so Python could not find that ward and stopped.')
assert not _fx and len(_g.get('_effects', [])) == _w0 and _hero['mana'] == 15, (
    "The guard from the code you started with no longer turns away a ward the hero doesn't know." + _tail + ' A ward was cast.')
assert _ls, ("The guard from the code you started with no longer says so when the hero doesn't know the ward." + _tail
             + ' Nothing was printed.')
'''


def mb_check(label, body, **values):
    """A mini-boss check: the shared _MB_PRE, then the body. Both are filled with the same values."""
    return check(label, _MB_PRE + body, setup=MB_SETUP, **values)


_AWAY_UNUSED = dict(typed="", turn_away="", exact="")

RC_MINIBOSS_A = dict(
    kind="project",
    id="rc-miniboss-a",
    title="Mini-boss: Hold the Lantern Ward",
    optional=False,
    minutes=15,
    summary=(
        "Part 2: one whole campaign part, with only the help the campaign gives. Finish `cast_ward` on your own "
        "and pass all six tasks."
    ),
    intro=(
        "Finish `cast_ward(hero, ward_name)`: replace `pass`, under the numbered comments, with an `if`, an `elif` "
        "and an `else`. This is [[campaign mode]]: you get the numbered comments, the check messages, the error "
        "box, and Mar'tu's version after 5 minutes. There is no Assemble it, and Help stops before the answer, as "
        "in the campaign.\n"
        "The comments are numbered in the order of Your tasks, not in the order of the lines. Line 18 says "
        "`test 3, test 4`: those two questions go on top. The cast, 1 and 2, goes last, under `else:`.\n"
        "In the campaign, the error box is shorter: you see only Python's own message. Read its last line first: "
        "it says what went wrong. The nearest line above it that says `line` and a number tells you where. Fix "
        "that line."
    ),
    martu=(
        "This is the campaign's barrier part, with new names. `cast_ward` casts a ward, a spell that protects, "
        "for a hero. A hero needs enough magical affinity (how strong their magic is) and enough mana (their magic "
        "power). The guard at the top is done: a hero who doesn't know the ward is told so. Then `ward` holds "
        "the ward's page. Your `if`, `elif` and `else` work like a grading scale: Python checks from the top and "
        "takes the first question that is `True`. Gearshift's sheet is already made:\n"
        "```python\ngearshift = {\n    \"name\": \"Gearshift\",\n    \"mana\": 20,\n    \"max_mana\": 20,\n"
        "    \"abilities\": {\n        \"magical_affinity\": 10,\n    },\n    \"wards\": {\n"
        "        \"Lantern Ward\": {\n            \"mana_cost\": 6,\n            \"required_affinity\": 9,\n"
        "            \"effect\": lantern_ward,\n        },\n    },\n}\n```\n"
        "`show_mana(hero)` is finished: it draws the mana bar. I test your code with made-up heroes and wards. "
        "Exactly enough is enough, yes?"
    ),
    setup=MB_SETUP,
    names=["cast_ward", "hero", "ward_name", "ward", "show_mana"],
    support="light",
    solo=True,
    explainer="lean",
    starter=MB_STARTER,
    checkpoints=[
        dict(
            id="skilled-hero-casts",
            text="Replace `pass` on line 32 with the line `ward[\"effect\"](hero)`. It casts the ward for a hero "
                 "who is skilled enough and has enough mana.",
            dictated=True,
            hints=[
                "Look at comment 1. For now, your cast line can go where `pass` is. Task 3 moves it under "
                "`else:`.",
                "A function in a dictionary runs when you put a value in parentheses right after it. It's like f(3) "
                "in math. `pack[\"tool\"](sheet)` runs the tool on that sheet.",
                "Read the effect from `ward`, then hand it the hero who is casting, `hero`, in the parentheses.",
            ],
            checks=[mb_check("a skilled hero with enough mana casts", _MB_CASTS),
                    mb_check("the starter's guard still turns away a ward the hero doesn't know", _MB_GUARD)],
            pass_line="A skilled hero with enough mana casts the ward. Gearshift: Lantern lit. Barrier's holding.",
        ),
        dict(
            id="bar-updates",
            text="Add two lines under your cast line:\n1. Make `hero[\"mana\"]` go down by `ward[\"mana_cost\"]`.\n"
                 "2. Call `show_mana(hero)` to draw the bar again.",
            dictated=True,
            hints=[
                "Look at comment 2. Two more lines go under your cast line, at the same indent.",
                "`jar[\"honey\"] = jar[\"honey\"] - spoon[\"size\"]` works out the right side first: the old honey "
                "minus the spoon's size. Then it stores the new honey on the left, like a bank balance after you spend.",
                "The cost is on the ward's page, `ward[\"mana_cost\"]`. The finished function `show_mana` draws the "
                "bar.",
            ],
            checks=[
                keep_fn("show_mana", SHOW_MANA),
                mb_check("the mana bar updates after a cast", _MB_BAR),
            ],
            pass_line="The mana goes down by the ward's cost, and the bar is drawn again. Bomb Shell: Good.",
        ),
        dict(
            id="low-affinity-no-cast",
            text="Three moves, so a hero with too little affinity doesn't cast:\n"
                 "1. Above your cast lines, add an `if` that asks: is `hero[\"abilities\"][\"magical_affinity\"]` "
                 "lower than `ward[\"required_affinity\"]`?\n"
                 "2. Under it, one indent in, print that the hero isn't skilled enough.\n"
                 "3. Put `else:` under that message, then move your cast lines under it, one indent further in.",
            dictated=True,
            hints=[
                "Look at comment 3. This question goes first, above your cast lines. The cast lines move one indent "
                "further in, under `else:`, which means *otherwise*.",
                "The lines that run when every question is `False` go under `else:`, one indent in:\n"
                "```python\nif jar[\"honey\"] < spoon[\"size\"]:\n    print(\"Too little.\")\nelse:\n"
                "    eat(jar)\n```",
                "Two keys in a row read inside a sheet, the outer key first, like a chapter and then a section: the "
                "affinity sits inside `\"abilities\"`. `<` means *lower than*.",
            ],
            checks=[mb_check("too little affinity does not cast", _MB_TURNS_AWAY,
                             cases=[(6, 15, 5, 7, "low"), (10, 15, 5, 11, "low"), (7, 15, 5, 7, "exact")],
                             typed="A question compares with a typed-in number, not the ward's own `\"required_affinity\"`.",
                             turn_away="A hero with too little affinity still cast.",
                             exact="A hero with exactly enough affinity was turned away.", heroes=HERO_NAMES)],
            pass_line="A hero with too little affinity is told why, and doesn't cast. Oogrish: A fair answer. Steady, now.",
        ),
        dict(
            id="low-mana-no-cast",
            text="Add an `elif` line right above `else:`, with the same spaces in front as `else:`. If "
                 "`hero[\"mana\"]` is lower than `ward[\"mana_cost\"]`, print that the hero doesn't have enough mana, "
                 "and don't cast.",
            dictated=True,
            hints=[
                "Look at comment 4. `elif` sits between the first question and `else:`, at the same indent as the `if`.",
                "`elif` means *else, if*: it asks only when the question above it was `False`, like the next line of a "
                "grading scale. So one cast prints one message at most.",
                "Compare `hero[\"mana\"]` with the ward's own `\"mana_cost\"`.",
            ],
            checks=[mb_check("too little mana does not cast", _MB_TURNS_AWAY,
                             cases=[(12, 4, 5, 7, "low"), (12, 7, 8, 7, "low"), (6, 4, 5, 7, "low")],
                             typed="A question compares with a typed-in number, not the ward's own `\"mana_cost\"`.",
                             turn_away="A hero with too little mana still cast.", exact="", heroes=HERO_NAMES),
                    mb_check("too little mana and too little affinity print different messages",
                             _MB_TWO_REASONS)],
            pass_line="A hero with too little mana gets their own message, and doesn't cast. Lucky: No mana, no ward. I'll allow it.",
        ),
        dict(
            id="exactly-enough-mana",
            text="Check the sign in your mana question. Use `<`, not `<=`, so a hero with exactly enough mana "
                 "still casts.",
            dictated=True,
            hints=[
                "Look at comment 5, then at the sign in the mana question.",
                "`<` means *lower than*, like an open dot on a number line. `<=` means *lower than or the same*, a "
                "filled dot, so it turns away a hero with exactly enough.",
                "A hero with 5 mana and a ward that costs 5 has exactly enough: the question must let them through.",
            ],
            # The low case first, so a program with no mana question yet (partials 1-3) does not turn this task
            # green before its turn; it only fails where task 4 already fails.
            checks=[mb_check("exactly enough mana still casts", _MB_TURNS_AWAY,
                             cases=[(12, 4, 5, 7, "low"), (12, 5, 5, 7, "exact"), (12, 8, 8, 7, "exact")],
                             typed="A question compares with a typed-in number, not the ward's own `\"mana_cost\"`.",
                             turn_away="A hero with too little mana still cast.",
                             exact="A hero with exactly enough mana was turned away.", heroes=HERO_NAMES)],
            pass_line="A hero with exactly enough mana still casts. Mar'tu: Exactly enough is enough.",
        ),
        dict(
            id="own-cost",
            text="Use the ward's own cost in your subtraction. Then it works for any ward, not only the Lantern Ward.",
            dictated=False,
            hints=[
                "Look at comment 6, then at the subtraction. Each ward has its own cost, on its own page.",
                "Read a value from the page you have, like `page[\"price\"]`, not a typed-in number. A formula with "
                "names works for every ward, the way area = length × width works for every rectangle.",
                "The page is `ward`. Its cost is under the key `\"mana_cost\"`.",
            ],
            checks=[mb_check("the ward's own cost is used", _MB_OWN_COST)],
            # Task 2's dictated subtraction already reads the ward's cost, so this step can pass early: its line is about
            # its own task only, never "all six pass" (the finished box says that, at the real finish).
            pass_line="The cost comes from the ward's own page, so the subtraction works for any ward, not only the Lantern Ward.",
        ),
    ],
    solution=MB_SOLUTION,
    partials=[MB_P1, MB_P2, MB_P3, MB_P4, MB_P5],
    another_way=[
        dict(angle="picture", label="Get it, compare, act", text=(
            "```text\nGet it:  ward = the page\nCompare: affinity < need?\n           -> not skilled\n"
            "         mana < cost?\n           -> not enough\nAct:     cast, pay, draw\n```")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "This is `cast_spell` from the campaign's barrier part, with other names: `hero` for `caster`, `ward` "
            "for `spell`, `\"effect\"` for `\"spell_function\"`, and `print` for `print_prompt`. The same six "
            "checks, in the same order.")),
    ],
    campaign_link=dict(
        module=M2,
        part="hold-the-barrier",
        why=(
            "You played this part in the campaign: `cast_spell` with its guard, the affinity read from inside "
            "`\"abilities\"`, `<` and not `<=`, `spell[\"spell_function\"](caster)`, the cost, and `show_mana`. The "
            "campaign checks the same six things, so passing these six on your own means you are ready for it."
        ),
    ),
    takeaway="Get it, compare, act: ask with `if` and `elif` using `<`, then under `else:` call "
             "`ward[\"effect\"](hero)`, pay the cost, and call `show_mana(hero)`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=MB_STARTER, fails_at=1, message_contains="did not cast"),
        dict(why="the effect read, never called (calling vs handing over: no (hero))",
             code=_mb(_mb_body(effect="ward[\"effect\"]")), fails_at=1, message_contains="nothing calls it"),
        dict(why="lantern_ward called by its own name", code=_mb(_mb_body(effect="lantern_ward(hero)")), fails_at=1,
             message_contains="by its own name"),
        dict(why="the effect's line printed, not the effect called (print in place of the call)",
             code=_mb(_mb_body(effect="print(\"Gearshift's lantern ward glows.\")")), fails_at=1,
             message_contains="effect's words were printed"),
        dict(why="the given ward line retyped from Gearshift's sheet (typed values, not the parameters)",
             code=_mb(_mb_body()).replace("    ward = hero[\"wards\"][ward_name]",
                                          "    ward = gearshift[\"wards\"][\"Lantern Ward\"]"),
             fails_at=1, message_contains="uses `gearshift` by name, so Brakka's cast used Gearshift's sheet"),
        dict(why="the given ward line with a typed ward name (not ward_name)",
             code=_mb(_mb_body()).replace("    ward = hero[\"wards\"][ward_name]",
                                          "    ward = hero[\"wards\"][\"Lantern Ward\"]"),
             fails_at=1, message_contains="by a typed-in name"),
        dict(why="the effect read from a typed ward name", code=_mb(_mb_body(
            effect="hero[\"wards\"][\"Lantern Ward\"][\"effect\"](hero)")), fails_at=1,
             message_contains="by a typed-in name"),
        dict(why="the starter's guard broken: its return removed (a given line edited)",
             code=_mb(_mb_body()).replace("        return\n    ward =", "    ward ="), fails_at=1,
             message_contains="The guard from the code you started with"),
        dict(why="the effect handed the wrong sheet (gearshift, not hero)",
             code=_mb(_mb_body(effect="ward[\"effect\"](gearshift)")), fails_at=1, message_contains="uses `gearshift` by name, so Brakka's cast used Gearshift's sheet"),
        dict(why="the affinity sign backwards", code=_mb(_mb_body(aff=AFF.replace("<", ">"))), fails_at=1,
             message_contains="was turned away"),
        dict(why="a nesting level skipped: hero[\"magical_affinity\"] (KeyError)",
             code=_mb(_mb_body(aff="hero[\"magical_affinity\"] < ward[\"required_affinity\"]")), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the campaign's name caster copied", code=_mb(_mb_body(aff=AFF.replace("hero", "caster"))),
             fails_at=0, message_contains="'caster' is not defined"),
        dict(why="CP2 the subtraction never stored", code=_mb(_mb_body(pay="        hero[\"mana\"] - ward[\"mana_cost\"]\n")),
             fails_at=2, message_contains="never changes. Mar'tu tested your code with a made-up hero and ward: Brakka has affinity "
                                          "12 and mana 15. Moon Step costs 5 and needs affinity 7. Brakka still has "
                                          "15 mana."),
        dict(why="CP2 the new mana kept in a new variable",
             code=_mb(_mb_body(pay="        mana = hero[\"mana\"] - ward[\"mana_cost\"]\n")), fails_at=2,
             message_contains="never changes"),
        dict(why="CP2 show_mana not called", code=_mb(_mb_body(show="")), fails_at=2, message_contains="was not called"),
        dict(why="CP2 show_mana named with no () (calling vs handing over)",
             code=_mb(_mb_body(show="        show_mana\n")), fails_at=2, message_contains="has no `()`"),
        dict(why="CP2 show_mana before the subtraction", code=_mb(_mb_body(pay=SHOW + PAY, show="")), fails_at=2,
             message_contains="old mana. Mar'tu tested your code with a made-up hero and ward: Brakka has affinity 12 and mana 15. "
                              "Moon Step costs 5 and needs affinity 7. The bar showed 15 mana. The mana ended at 10."),
        dict(why="CP2 show_mana handed the wrong sheet", code=_mb(_mb_body(show="        show_mana(gearshift)\n")),
             fails_at=2, message_contains="uses `gearshift` by name, so Brakka's cast used Gearshift's sheet"),
        dict(why="CP2 the finished helper edited (told to leave it as it is)",
             code=_mb(_mb_body(), head=MB_HEAD.replace("print(hero[\"name\"], bar)", "print(bar)")), fails_at=2,
             message_contains="was already finished, and it changed"),
        dict(why="CP2 the new mana stored in the ward's page (the wrong sheet)",
             code=_mb(_mb_body(pay="        ward[\"mana_cost\"] = hero[\"mana\"] - ward[\"mana_cost\"]\n")),
             fails_at=2, message_contains="ward's page"),
        dict(why="CP2 subtracted from max_mana (the wrong key)",
             code=_mb(_mb_body(pay="        hero[\"mana\"] = hero[\"max_mana\"] - ward[\"mana_cost\"]\n")),
             fails_at=2, message_contains="`\"max_mana\"`"),
        dict(why="CP3 <= on the affinity (exactly enough turned away)", code=_mb(_mb_body(aff=AFF.replace("<", "<="))),
             fails_at=3, message_contains="exactly enough affinity"),
        dict(why="CP3 a typed number for the required affinity",
             code=_mb(_mb_body(aff="hero[\"abilities\"][\"magical_affinity\"] < 9")), fails_at=3,
             message_contains="typed-in number"),
        dict(why="CP3 two ifs, not if / elif (the second if's else still casts)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    if {MANA}:\n" + MANA_MSG + "    else:\n"
                      f"        {EFFECT}\n" + PAY + SHOW), fails_at=3, message_contains="still cast"),
        dict(why="CP3 no message when turned away", code=_mb(_mb_body(skill_msg="        return\n")), fails_at=3,
             message_contains="nothing was printed"),
        dict(why="CP3 the if added above the cast, no else (the cast lines never moved under else:)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + _flat([f"        {EFFECT}\n", PAY, SHOW])), fails_at=3,
             message_contains="casts anyway: the cast lines are not inside the last branch, `else`. Mar'tu "
                              "tested your code with a made-up hero and ward: Brakka has affinity 6 and mana 15. Moon Step costs 5 "
                              "and needs affinity 7. The message showed, then Brakka cast it anyway."),
        dict(why="the elif added too, still no else (caught at CP3)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    elif {MANA}:\n" + MANA_MSG
                      + _flat([f"        {EFFECT}\n", PAY, SHOW])), fails_at=3, message_contains="casts anyway"),
        dict(why="the cost and the redraw left outside else: (a missing indent): turned away, still paid",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    elif {MANA}:\n" + MANA_MSG + "    else:\n"
                      f"        {EFFECT}\n" + PAY[4:] + SHOW[4:]), fails_at=3, message_contains="mana still went down"),
        dict(why="else: written, the cast lines not indented under it (a missing indent)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + "    else:\n" + _flat([f"        {EFFECT}\n", PAY, SHOW])),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the colon left off else", code=_mb(_mb_body().replace("    else:\n", "    else\n")), fails_at=0,
             message_contains="expected ':'"),
        dict(why="CP3 a typed hero name in the message (a literal instead of the parameter)",
             code=_mb(_mb_body(skill_msg="        print(\"Gearshift isn't skilled enough.\")\n")), fails_at=3,
             message_contains="a typed-in name"),
        dict(why="CP4 a typed number for the cost in the test", code=_mb(_mb_body(mana="hero[\"mana\"] < 6")), fails_at=4,
             message_contains="typed-in number"),
        dict(why="CP4 max_mana read in the mana test (the wrong key)",
             code=_mb(_mb_body(mana="hero[\"max_mana\"] < ward[\"mana_cost\"]")), fails_at=4,
             message_contains="`\"max_mana\"`"),
        dict(why="CP4 the affinity message copied into the elif (two reasons, one message)",
             code=_mb(_mb_body(mana_msg=SKILL_MSG)), fails_at=4,
             message_contains="Too little mana printed the same message as too little affinity. Mar'tu tested "
                              "your code with a made-up hero and ward. Moon Step costs 5 and needs affinity 7."),
        dict(why="the ward's name read as if it were the page (ward_name, not ward): the explainer's string "
                 "indices rule",
             code=_mb(_mb_body(effect="ward_name[\"effect\"](hero)")), fails_at=0,
             message_contains="string indices"),
        dict(why="CP4 the mana test as a second if (two messages)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    if {MANA}:\n" + MANA_MSG
                      + f"    if not {MANA} and not {AFF}:\n" f"        {EFFECT}\n" + PAY + SHOW),
             fails_at=4, message_contains="2 messages"),
        dict(why="CP5 <= on the mana (> vs >= at the exact boundary; the campaign's own warning)",
             code=MB_P4.replace(TYPED_PAY, PAY), fails_at=5,
             message_contains="A hero with exactly enough mana was turned away. Mar'tu tested your code with a "
                              "made-up hero and ward: Brakka has affinity 12 and mana 5. Moon Step costs 5 and needs affinity 7. "
                              "Brakka was turned away."),
        dict(why="CP6 a typed cost in the subtraction", code=MB_P5, fails_at=6,
             message_contains="a typed-in 6, not by the ward's own cost. Mar'tu tested your code with a made-up hero and ward: Brakka "
                              "has affinity 12 and mana 15. Moon Step costs 3 and needs affinity 7. The mana ended "
                              "at 9, not 12."),
        dict(why="CP6 the check's own first answer typed (hero[\"mana\"] = 10)",
             code=_mb(_mb_body(pay="        hero[\"mana\"] = 10\n")), fails_at=6,
             message_contains="`hero[\"mana\"]` holds a typed-in 10: Mar'tu cast twice, with test mana and "
                              "a test cost, and the mana still ended at 10. Mar'tu tested your code with a made-up hero and ward: "
                              "Brakka has affinity 12 and mana 15. Moon Step costs 3 and needs affinity 7. The mana "
                              "ended at 10, not 12."),
        dict(why="CP6 the check's own cost typed (hero[\"mana\"] - 3)",
             code=_mb(_mb_body(pay="        hero[\"mana\"] = hero[\"mana\"] - 3\n")), fails_at=6,
             message_contains="a typed-in number"),
        dict(why="CP6 the starting mana typed from the evidence (15)",
             code=_mb(_mb_body(pay="        hero[\"mana\"] = 15 - ward[\"mana_cost\"]\n")), fails_at=6,
             message_contains="a typed-in 15"),
        dict(why="CP1 a print around the cast (an extra None)",
             code=_mb(_mb_body(effect="print(ward[\"effect\"](hero))")), fails_at=1,
             message_contains="showed `None`, Python's word for nothing."),
        dict(why="CP6 the subtraction the wrong way round",
             code=_mb(_mb_body(pay="        hero[\"mana\"] = ward[\"mana_cost\"] - hero[\"mana\"]\n")), fails_at=6,
             message_contains="the wrong way"),
    ],
    notes=(
        meta(starter_level="S2", path="READY", form="A", part=2,
             skills="dict-nested,elif-chain,boundary,call-stored-func,dict-write,read-helper",
             prepares="hold-the-barrier", solo="true", dictates="1,2,3,4,5", camp="true",
             foreign_names="pack,tool,sheet,jar,honey,spoon,size,eat,page,price") + "\n"
        "Mini-boss A (5.4): the near-transfer of hold-the-barrier, `cast_ward(hero, ward_name)`. Given: the guard, "
        "`ward = hero[\"wards\"][ward_name]`, the finished `show_mana(hero)` (KEEP-checked) and six numbered "
        "comments, one for each checkpoint, in the campaign's check order (2.12 rule 13). The comments are numbered "
        "in check order, not line order, and both the intro and four comment lines above them say so (code order: "
        "test 3, test 4, then `else:` with 1 and 2), so the order is not a trap that tests our wiring. The student "
        "writes the if / elif / else: the nested affinity test, the `<` mana test, `ward[\"effect\"](hero)`, the "
        "subtraction and the redraw. CP1-CP6 are the campaign's six checks, in order; each casts Moon Step (a "
        "recorder effect) for a fresh hero, Brakka, so the student's own run of Gearshift never has to show a "
        "branch; show_mana is swapped for a recorder only during the check's call. CP1 also checks that the given "
        "guard still turns away a ward the hero doesn't know (Moss, who knows only Frost Veil): not one of the "
        "campaign's six, but breaking a given line is the class's 'edited what you were told to leave' slip. BND: "
        "need - 1, need + 1, exactly enough affinity (CP3); cost above the mana, both too low at once (CP4: one "
        "message, so `elif`), and form B's two-reasons check (too little mana must not print the affinity "
        "message); exactly enough mana (CP5); costs 3 and 8, from mana 15 and 14, so a typed 6, a typed start of 15 "
        "or a reversed subtraction each fail (CP6). Partials p2-p5 pay a typed 6, so CP6 turns green last, as in "
        "the campaign.\n"
        "Evidence: every mini-boss message ends with short sentences built from the cast (`_test`), never brackets "
        "inside brackets: \"Mar'tu tested your code with a made-up hero and ward: Brakka has affinity 12 and mana 5. Moon Step costs "
        "5 and needs affinity 7. Brakka was turned away.\" The wrong `gearshift` sheet is named as \"`cast_ward` uses "
        "`gearshift` by name, so Brakka's cast used Gearshift's sheet.\" `ward_name[\"effect\"](hero)` stops the run "
        "(string indices), proof for the explainer's rule.\n"
        "Hint ladders: CP1 and CP3 teach the move under `else:` early (CP1 rung 0: the cast can take `pass`'s "
        "place for now, and check 3 moves it; CP3 rung 1: a fenced picture of an if / else with other names, "
        "`jar`, `spoon`, `eat`), and CP2's picture subtracts a value read from a page, with no typed amount. Rung 2 "
        "never holds a finished line.\n"
        "Campaign mode for everyone (2.10, T4), with the schema's fields: support='light' (Help opens after the "
        "first failed run), solo=True (each student alone; no Start me off, no Learn-pane Another way), "
        "explainer='lean' (the SOLO ruling; nearest to the campaign's shorter messages), no assemble, no tracer, "
        "no predict. Hints capped at rung 2: each ladder is Where to look plus two teach rungs; the last rung, which "
        "the site labels 'Show me how', is written at teach level, never the finished line. CP6's pass line says "
        "\"You did that on your own.\", so soloPassLine swaps it for \"with some help this time\" after Compare or "
        "Help past rung 1. Site work still needed (site requests): a real hint cap at rung 2; Compare by time only, "
        "after 5 minutes, as the intro promises (today the course setting also opens it after 4 counted failed "
        "runs); a pass after Compare recorded as 'Ready with a review list' and pointing the student to mini-boss "
        "B, its immediate twin; the Readiness result (all 6 checks without Compare = Ready) and its 'Compare used' "
        "flag; and the review screen's explainer-parity line (written here in the intro until then). The 6C-05 "
        "More-structure ladder is not offered (5.4). Messages are campaign-like: what the check expects and what "
        "happened, with the "
        "evidence, never the finished line."
    ),
)


# =============================================================================================
# Explain a line you wrote (5.2, G4 R24): one click, for everyone
# =============================================================================================

RC_EXPLAIN = dict(
    kind="quiz",
    id="rc-explain",
    title="Explain a line you wrote",
    optional=False,
    minutes=1,
    summary="One question, one click: pick the sentence that says what one line of your mini-boss does.",
    questions=[
        dict(
            type="mc",
            id="explain-the-pay-line",
            q="Your mini-boss has a line like this one. Which sentence says what it does?",
            code="hero[\"mana\"] = hero[\"mana\"] - ward[\"mana_cost\"]\n",
            choices=[
                "It works out the mana that is left after the cast, but then keeps it nowhere at all.",
                "It stores the hero's mana on the ward's page, under the ward's key `\"mana_cost\"`.",
                "It takes the ward's cost from the hero's mana, and stores what is left as the new mana.",
                "It sets the hero's mana to the most mana they can ever hold, minus the ward's cost.",
            ],
            answer=2,
            why_wrong={
                0: "The `=` stores the result on the hero's sheet, under `\"mana\"`. Nothing is lost.",
                1: "The left side of `=` is `hero[\"mana\"]`, the hero's sheet, not the ward's page.",
                3: "`\"max_mana\"` is not in this line. The right side reads the mana the hero has now.",
            },
            explain=(
                "Python works out the right side first: the hero's mana now, minus the ward's cost. Then `=` stores "
                "the answer back under `\"mana\"` on the hero's sheet, like a new bank balance. In math, x = x − 6 "
                "has no answer, but Python's `=` means *gets*."
            ),
            notes=(
                "rc-explain (5.2, G4 R24 for everyone; 5.7 'the student can explain a line they wrote'). The prototype "
                "asks about the pay line, `hero[\"mana\"] = hero[\"mana\"] - ward[\"mana_cost\"]`, the class-wide "
                "combine-values gap (read the old value, combine it, store it back). `ward[\"effect\"](hero)` is not "
                "asked here: question i9a already covers a stored function and its call. Picking a line from the "
                "student's own mini-boss code is UI work. Skills: combine-values, dict-write, reassign. The code "
                "line is 47 characters, the mini-boss solution-line exception to the 36-character phone rule (the "
                "campaign's own pay-line shape, as in the mini-boss's solution). Distractors from the class's "
                "slips: worked out but never stored, the store put on the wrong sheet (the ward's page), and "
                "`\"max_mana\"` read for the mana now. The four choices are within 6 characters of each other "
                "(81 to 87), so the right one is not the longest by much; the answer sits third here, and the site "
                "shuffles."
            ),
        ),
    ],
    notes=(
        "One question, one click, unscored for the Ready rule (5.5 does not count it) but recorded as 'explains' "
        "evidence. Shown after the mini-boss. The explainer-parity line (5.2) is in the mini-boss intro and in "
        "rc-review until the Readiness review screen exists, so it is not repeated here."
    ),
)


# =============================================================================================
# The intro card
# =============================================================================================

RC_INTRO = dict(
    kind="article",
    id="before-we-continue",
    title="Before We Continue",
    minutes=2,
    summary="What the Readiness Check is, and how it works. Practice, never a grade.",
    body=(
        "Mar'tu: Before the campaign goes on, show me what you can do on your own. This is practice, never a grade.\n"
        "You played the campaign's first two modules, and a lot of that code felt like a wall. Since then, you "
        "took the wall apart, one stone at a time.\n"
        "1. Part 1: twelve questions, then nine short tasks. Hints are off. The glossary, read-aloud and the error "
        "box in the Console still work. Stuck on a task? Type your best try, press Run once, then skip it and come "
        "back later. Tasks you pass stay ✓ done.\n"
        "2. Part 2, the mini-boss: hold the Lantern Ward, a spell that protects, with only the help the campaign "
        "gives: the numbered comments, the check messages, the error box, and my version after 5 minutes. That is "
        "[[campaign mode]].\n"
        "3. Then one click: explain a line you wrote.\n"
        "Missed something? Open *Mar'tu's Notes: Where to Look Again*, right after Part 1. A miss only shows us "
        "which lesson to look at again, together. The story goes on either way.\n"
        "You have learned enough to help, yes? Show me without the hints. Then we continue.\n"
        "About 45 minutes."
    ),
    notes=(
        "The Readiness Check intro card (u10a; 5.1, 5.2). Mar'tu's line is the spec's. Names the struggle kindly "
        "once (teacher decision 2), then the plan in the order the items come: the twelve questions first (so the "
        "first win is a prediction), then the nine tasks, the mini-boss and the one click. It leads with what "
        "stays on, not with what is off, and points to rc-review (Mar'tu's Notes), which comes right after Part 1. "
        "Every student works alone on their own device. Time: 2 + 10 + 18 + 15 + 1 = 46 core minutes; rc-review "
        "(15) is optional and only for a miss."
    ),
)

# The questions come first, so the first win is a prediction; Mar'tu's Notes follow Part 1 right away.
ITEMS = [RC_INTRO, RC_PART1_A_QUESTIONS, RC_PART1_A, RC_REVIEW, RC_MINIBOSS_A, RC_EXPLAIN]
