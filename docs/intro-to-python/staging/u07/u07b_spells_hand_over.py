"""Unit 7 "Functions II" ("Spells You Can Hand Over"), part b: Mar'tu remembers (6c-remembers), Lesson 6C "Spells
You Can Hand Over" (6C-01 to 6C-06 and the SOLO 6C-S), Quiz 6B, Project 6P "The Resonance Array" (with Lucky's
side quest, the old group D: a dictionary of dials), and the optional advanced challenge "The Spell Book, From
Blank" (spell-book-from-blank, 12 min, after the project; costs no one core time).

Release order: this part uses Unit 6's `for` loops (cast_on_everyone, the given learn_spell loop, run_array), so it
is published only after Unit 6.

Spec: design/curriculum.md, "## Unit 7 · Functions II", items 2, 3 and 4 (u07b). Introduces `const:None` (6C-04,
exactly as concept_map.json plans: the campaign's own `"spell_function": None` placeholder). Everything else comes
from earlier units: `def` / `return` / `pass` (Unit 3), lists and `in` (Unit 4), dictionaries, nested reads and
`not in` (Unit 5), and from Unit 6 (planned concepts only, u06a: `for` over a list or a list of dicts). No
`while`, `continue`, comprehensions, `.items()`, f-strings, defaults or keyword arguments. `None` is never written
in visible code before 6C-04; before that it only appears in prose, messages and printed output.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN `strengthen_magic`
handed to `add_spell(...)` with no `()`, the `"spell_function": None` placeholder, `spell["spell_function"](caster)`
in `cast_spell`, and the six checks of hold-the-barrier. Campaign links are "you've seen this, now you'll get it".
Every student has their own device; pair talk is optional and every checkpoint is solo.

Terminology (2.9): "function" in all plain text, checks and messages; Mar'tu still says "recipe" in the Learn pane.
"Matching" means an exact name (6C-04). "Parameter" / "argument" / "returns". The quotes rule word for word.

Help ladder as fields (FORMAT.md, the order the site shows them): hints[0] Where to look, the middle hints Teach me
(a tiny example with other names, listed in foreign_names), the last hint Show me how: the step's own line in
backticks, whose start up to its first `(` or `=` becomes Start me off (always a start the solution uses). Then
another_way (2+ angles), assemble (More structure) where the spec allows it, then Compare.
Campaign mode (2.10) on 6C-04, 6C-05 and 6P is recorded in each `notes` meta line (camp=true; hints capped at rung
2, Compare after 5 minutes, no Assemble it on 6C-04). 6C-05 keeps its four-level More-structure ladder (L1 the
starter, L2 the `if ___ < ___` shape as an another_way angle, L3 the assemble lines, L4 a worked twin angle).

Check codes (curriculum 2.5), built from one helper prelude (_SX) and a body per check. Plain Python, run in the
student's namespace after their code; every helper name starts with `_`:
  NOP    the value IS the function (identity): `None` (the `()` ran it now and handed back nothing), the name in
         quotes (text), the starter's placeholder, another function.
  CALL   recorders. `_rerun(changes)` runs the student's program again in a fresh namespace (setup first, prints
         private) with a line slipped in right after the statement that makes a name: a function wrapped so every
         call is counted (`_wrap`), or a dictionary's effect swapped for a stand-in. So a call must go THROUGH the
         variable or the dictionary (`chosen_spell(lucky)`, `glow["effect"](lucky)`): a call by the function's own
         name, a typed print, or a bare name with no `()` fails, each with its own message.
  PAR / SWAP / KEY  learn_spell is called with fresh values (never the task's 6, 9, lantern_ward), and the local
         `spell` is read when the call returns (sys.settrace, the frame's locals): placeholders left, typed values,
         a quoted parameter (`"mana_cost": "mana_cost"`), swapped values, near-miss or approximate keys
         (`"Mana_Cost"`, `"magic"`), then the book handed in (`book["spell_name"]`, a rebinding
         `spell_book = {...}`, `return spell` instead of storing, a typed key).
  BND    cast(): fresh casters and spells at need - 1, need, need + 1, mana below, at and above the cost.
  RET / PAR-CONST  the project's dials, with two fresh argument sets each (lint b).
  KEEP   the project's finished dials are unchanged (AST compare).
Messages lead with what to try, then what happened, then the evidence in brackets: "(Mar'tu's check called
`learn_spell(book, "Frost Veil", 5, 7, spark)`, only inside the check: ...)". SOLO messages (explainer "lean") name
the slip and keep the evidence, without the finished line. Check data uses invented Tor names only (Brakka, Moss,
Frost Veil, Moon Step, spark, glimmer); a student's own text is never repeated back.

Python's messages were checked in CPython 3.13 (the site runs 3.13): `x = f(lucky)` then `x(lucky)` ->
"'NoneType' object is not callable"; `cast_on_everyone(roster, "warm_hands")` -> "'str' object is not callable";
`cast_on_everyone(warm_hands, roster)` -> "'function' object is not iterable"; `warm_hands()` -> "warm_hands()
missing 1 required positional argument: 'hero'"; `glow("effect")` -> "'dict' object is not callable";
`"░" * a - b` -> "unsupported operand type(s) for -: 'str' and 'int'".

Phone width: starters, examples, question code and fenced pictures keep to 36 characters where the campaign's own
shape allows. The rehearsals keep the campaign's long lines on purpose (the `learn_spell` signature, the
bottom loop's call, `cast`'s guard), as Unit 5 did.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u07b
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
MODULE = "friends-in-low-places"


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
# Check helpers, put in front of every check (plain Python, run in the student's namespace)
# ---------------------------------------------------------------------------------------------

_SX = r'''import ast as _ast
import io as _io
import sys as _sys
_QUOTES = __QUOTES__
_SETUP = __SETUP__
_g = globals()
def _lit(_v):
    if _v is None:
        return '`None`'
    _k = type(_v).__name__
    if _k == 'str':
        return '`"' + _v + '"`'
    if _k == 'function':
        return 'the function `' + _v.__name__ + '`'
    return '`' + str(_v) + '`'
def _ev(_what, _end=''):
    return "(Mar'tu's check " + _what + ', only inside the check' + (': ' + _end if _end else '') + '.)'
def _err_text(_e):
    return type(_e).__name__ + (': ' + str(_e) if str(_e) else '')
def _tree():
    return _ast.parse(_source)
def _fdef(_name):
    _f = [_n for _n in _tree().body if type(_n).__name__ == 'FunctionDef' and _n.name == _name]
    return _f[-1] if _f else None
def _is_call(_n, _f):
    return type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == _f
def _top():
    return [_s for _s in _tree().body if type(_s).__name__ != 'FunctionDef']
def _top_calls(_f):
    return [_c for _s in _top() for _c in _ast.walk(_s) if _is_call(_c, _f)]
def _printed_call(_test):
    # a top-level print(...) with a call that _test accepts inside it
    return [_c for _s in _top() for _c in _ast.walk(_s) if _is_call(_c, 'print')
            and [_a for _a in _c.args if type(_a).__name__ == 'Call' and _test(_a)]]
def _quiet(_f, *_args):
    _keep = _sys.stdout
    _buf = _io.StringIO()
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _f(*_args)
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _keep
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err
def _peek(_f, _args, _var):
    # Call _f with print captured, and read the local variable _var as the call ends.
    _seen = {}
    _code = getattr(_f, '__code__', None)
    def _local(_fr, _evt, _a):
        if _evt == 'return' and _fr.f_code is _code:
            for _k in list(_fr.f_locals):
                _seen[_k] = _fr.f_locals[_k]
        return _local
    def _glob(_fr, _evt, _a):
        return _local if _fr.f_code is _code else None
    _old = _sys.gettrace()
    _sys.settrace(_glob)
    try:
        _val, _ls, _err = _quiet(_f, *_args)
    finally:
        _sys.settrace(_old)
    _out = _seen.get(_var, getattr(_f, '__globals__', {}).get(_var))
    return _out, _val, _ls, _err
def _made(_n):
    _k = type(_n).__name__
    if _k in ('FunctionDef', 'ClassDef'):
        return [_n.name]
    _ts = list(_n.targets) if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'AnnAssign') else [])
    return [_t.id for _t in _ts if type(_t).__name__ == 'Name']
def _changed(_n):
    # Names a top-level statement makes or changes, including by key: `roar["effect"] = shout` changes roar.
    _k = type(_n).__name__
    _ts = list(_n.targets) if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'AnnAssign') else [])
    _out = list(_made(_n))
    for _t in _ts:
        while type(_t).__name__ == 'Subscript':
            _t = _t.value
        if type(_t).__name__ == 'Name':
            _out.append(_t.id)
    return _out
def _rerun(_changes=(), _tail=''):
    # The program again in a fresh namespace (setup first, prints private). Each change's code runs right after
    # the first top-level statement that makes its name, or, for a name written '*name', after EVERY top-level
    # statement that makes or changes it (a dictionary built in steps); _tail runs at the end.
    _body, _found = [], []
    for _code in (_SETUP, _source):
        for _n in (_ast.parse(_code).body if _code.strip() else []):
            _body.append(_n)
            for _anchor, _line in _changes:
                _every = _anchor.startswith('*')
                if (_anchor[1:] in _changed(_n)) if _every else (_anchor in _made(_n) and _anchor not in _found):
                    if _anchor not in _found:
                        _found.append(_anchor)
                    _body.extend(_ast.parse(_line).body)
    if _tail:
        _body.extend(_ast.parse(_tail).body)
    _mod = _ast.Module(body=_body, type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _ns = {'__name__': '__main__'}
    _out, _old, _err = _io.StringIO(), _sys.stdout, None
    _sys.stdout = _out
    try:
        exec(compile(_mod, 'main.py', 'exec'), _ns)
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _old
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _err, [_a for _a, _l in _changes if _a not in _found]
def _wrap(_name, _log):
    # Code that counts every call of the function _name (it still runs), into the list _log. Each entry is the
    # values in parameter order, so a call with names (`effect=warm_hands`) is logged like one without.
    return (_log + ' = []\n_real_' + _name + ' = ' + _name + '\n'
            'def ' + _name + '(*_a, **_k):\n'
            '    import inspect as _inspect\n'
            '    try:\n'
            '        ' + _log + '.append(tuple(_inspect.signature(_real_' + _name + ').bind(*_a, **_k)'
            '.arguments.values()))\n'
            '    except TypeError:\n'
            '        ' + _log + '.append(_a)\n'
            '    return _real_' + _name + '(*_a, **_k)\n')
def _stand_in(_log):
    # Code for a stand-in effect `_fx` that records the hero it is handed (by position or by name).
    return (_log + ' = []\ndef _fx(*_a, **_k):\n    ' + _log + '.append(_a[0] if _a else '
            '(list(_k.values()) or [None])[0])\n    return "x"\n')
def _same_def(_name, _src):
    # True when the student's def of _name is exactly the finished one (comments and blank lines aside).
    _mine = _fdef(_name)
    return _mine is not None and _ast.dump(_mine) == _ast.dump(_ast.parse(_src).body[0])
def _stop(_err, _what):
    return 'Mend this, then Run again: ' + _err_text(_err) + ' ' + _ev(_what, 'Python stopped there')
def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]
def _squash(_s):
    return str(_s).lower().replace('_', '').replace(' ', '').replace('-', '')
def _near(_a, _b):
    if type(_a).__name__ != 'str' or _a == _b:
        return False
    _x, _y = _a.lower().strip(), _b.lower()
    return (_x == _y or _squash(_a) == _squash(_b) or _x.rstrip('s') == _y.rstrip('s')
            or (min(len(_x), len(_y)) >= 5 and _edits(_x, _y) <= 2))
def _key_slip(_d, _want):
    # The first key in _want that _d lacks, with the student's key that stands in for it (or None).
    for _k in _want:
        if _k in _d:
            continue
        for _x in _d:
            if _x not in _want and _near(_x, _k):
                return _k, _x
        _odd = [_x for _x in _d if _x not in _want]
        return _k, (_odd[0] if _odd else None)
    return None, None
def _def_names():
    return [_n.name for _n in _tree().body if type(_n).__name__ == 'FunctionDef']
def _need_def(_name, _nparams, _example):
    _fd = _fdef(_name)
    if _fd is None:
        _close = [_n for _n in _def_names() if _near(_n, _name)]
        assert not _close, ('Name the function `' + _name + '`, letter for letter: you wrote `' + _close[0] + '`.')
        assert False, 'Write the function with `def`: `' + _example + '`.'
    assert callable(_g.get(_name)), ('Keep `' + _name + '` a function: a later line put a value in it with `=`.')
    _n = len(_fd.args.args)
    assert _n == _nparams, ('Give `' + _name + '` ' + ('one parameter' if _nparams == 1 else str(_nparams)
                            + ' parameters') + ', like `' + _example + '`. It has ' + str(_n) + '.')
    return _fd
'''


def sx(setup=""):
    """The helpers, with the exercise's hidden setup (reruns run it first, like the site does)."""
    return _SX.replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))


def chk(label, body, setup="", **messages):
    """A check: the helper prelude, then a body template filled with its messages."""
    return (label, sx(setup) + fill(body, **messages))


# =============================================================================================
# The unit (the same UNIT dict in every Unit 7 part file)
# =============================================================================================

UNIT = dict(
    id="spell-recipes",
    order=7,
    title="Functions II",
    subtitle="Spells You Can Hand Over",
    published=True,
    martu_intro=(
        "You know recipes. Now they read stat sheets, write spell books, and guard the door. And one more thing, "
        "the strange one: a recipe can sit in a box, like any value. You can hand it to someone without cooking "
        "it.\n"
        "You have seen all of this in the campaign: `get_mana_bar(caster)`, `add_spell(...)` with "
        "`strengthen_magic` and no `()`, and `cast_spell` holding the barrier. A lot of that code felt like a "
        "wall, yes? This unit takes the wall apart. By the end, it is your code."
    ),
    goals=[
        "Write a function that takes a hero's sheet and returns a value from it",
        "Change a dictionary passed in, know the caller sees the change, and know when a function needs `return`",
        "Build a dictionary from parameters with exact matching names, and store it by key",
        "Guard a function with an early `return`",
        "Read a helper you didn't write, call it correctly, and leave it unchanged",
        "Wire two functions together: build the bar, then pass it on",
        "Use a function as a value: store it, hand it over without `()`, and call it from a dictionary with "
        "`book[name][\"effect\"](hero)`",
    ],
    campaign_links=[MODULE],
)

GLOSSARY = [
    dict(
        term="function as a value",
        aliases=["functions as values", "hand over a function", "handing over a function"],
        plain=(
            "A function's name with no () is the function itself, like any value. You can store it in a variable "
            "or a dictionary, or hand it to another function, and call it later with ()."
        ),
        example="chosen_spell = warm_hands\nchosen_spell(lucky)",
    ),
]

# The party table (curriculum 1.2): the real values every sheet uses.
PARTY = [
    # var, name, max_mana (= 2 x affinity), affinity, weapon die
    ("oogrish", "Oogrish", 18, 9, 6),
    ("gearshift", "Gearshift", 20, 10, 8),
    ("bomb_shell", "Bomb Shell", 24, 12, 8),
    ("lucky", "Lucky", 26, 13, 6),
]
HERO_NAMES = [name for _, name, _, _, _ in PARTY]


def _roster_setup(extra="", book=None):
    """Hidden setup: four hero sheets made by a hidden helper, and `roster`. `book` is each spell book's code."""
    book = "{}" if book is None else book
    out = extra + (
        "def _sheet(name, mana, affinity):\n"
        "    return {\n"
        '        "name": name,\n'
        '        "mana": mana,\n'
        '        "max_mana": mana,\n'
        '        "abilities": {"magical_affinity": affinity},\n'
        f'        "spell_book": {book},\n'
        "    }\n"
        "\n\n"
    )
    for var, name, mana, affinity, _ in PARTY:
        out += f'{var} = _sheet("{name}", {mana}, {affinity})\n'
    return out + "roster = [oogrish, gearshift, bomb_shell, lucky]\n"


# =============================================================================================
# Mar'tu remembers... (6c-remembers): store-then-pass (Unit 3) and `spell_book[spell_name] = spell` (Unit 5)
# =============================================================================================

REMEMBERS_6C = dict(
    kind="quiz",
    id="6c-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from earlier units. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 6C; recall from Unit 3 (store-then-pass, "
        "6A-08: the def/return item every warm-up carries from Unit 4 on) and Unit 5 (`spell_book[spell_name] = "
        "spell`, 4B-04). A miss shows the answer and a one-line why, with no red X. Both set up the lesson: the "
        "first stores what a call hands back (6C-01 then stores the function itself), the second is the line "
        "learn_spell ends with (6C-04)."
    ),
    questions=[
        dict(
            type="predict",
            id="store-then-pass",
            q="What will this print?",
            code=(
                "def get_glow():\n"
                '    return "Glow on"\n'
                "\n"
                "def show(words):\n"
                '    print("Board: " + words)\n'
                "\n"
                "line = get_glow()\n"
                "show(line)\n"
            ),
            choices=["Board: Glow on", "Board: line", "Glow on", "an error"],
            answer="Board: Glow on",
            explain=(
                "`get_glow()` runs and hands back `\"Glow on\"`. The variable `line` stores it. Then `show(line)` "
                "passes that variable on, so `words` holds `\"Glow on\"` inside `show`. Store it, then pass it on."
            ),
            notes=(
                "store-then-pass (Unit 3, 6A-08). 'Board: line' is the quoted-name belief; 'Glow on' is 'the "
                "first function prints'; 'an error' is 'a variable can't go into a call'."
            ),
        ),
        dict(
            type="predict",
            id="store-by-name",
            q="What will this print?",
            code=(
                'book = {"Glow": 2}\n'
                'spell_name = "Mist"\n'
                "book[spell_name] = 4\n"
                "print(book)\n"
            ),
            choices=["{'Glow': 2, 'Mist': 4}", "{'Glow': 2, 'spell_name': 4}", "{'Mist': 4}", "an error"],
            answer="{'Glow': 2, 'Mist': 4}",
            explain=(
                "`spell_name` has no quotes, so Python looks inside it and finds `\"Mist\"`. The book gets a new "
                "page, Mist, and keeps Glow. " + QUOTES_RULE
            ),
            notes=(
                "dict-key-from-variable (Unit 5, 4B-04). The second choice is the quoted-variable key; the third is "
                "'a store replaces the book'."
            ),
        ),
    ],
)

# =============================================================================================
# Lesson 6C "Spells You Can Hand Over"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 6C-01 name-without-parentheses (moment: the box holds the recipe)
# ---------------------------------------------------------------------------------------------

WARM_DEF = (
    "def warm_hands(hero):\n"
    '    print(hero["name"], "warms up.")\n'
)
LUCKY_SMALL = 'lucky = {\n    "name": "Lucky",\n    "mana": 26,\n}\n'
NAME_HEAD = WARM_DEF + "\n\n" + LUCKY_SMALL + "\n"
NAME_STORE_COMMENT = (
    "# 1. Replace the 0 with the\n"
    "#    function itself: warm_hands,\n"
    "#    with no ().\n"
)
NAME_CALL_COMMENT = "# 2. Call chosen_spell on lucky.\n"


def _name(store="chosen_spell = 0\n", call=""):
    return NAME_HEAD + NAME_STORE_COMMENT + store + "\n" + NAME_CALL_COMMENT + call


NAME_STARTER = _name()
NAME_SOLUTION = _name("chosen_spell = warm_hands\n", "chosen_spell(lucky)\n")
HUM_EXAMPLE = (
    "def hum(sheet):\n"
    '    print(sheet["name"], "hums.")\n'
    "\n\n"
    'oogrish = {"name": "Oogrish"}\n'
    "tune = hum\n"
    "tune(oogrish)\n"
)

_HOLDS_WARM = r'''
_f = _g.get('warm_hands')
assert callable(_f), __KEEP__
_v = chosen_spell
if _v is not _f:
    _self = [_s for _s in _top() if type(_s).__name__ == 'Assign' and 'chosen_spell' in _made(_s)
             and _is_call(_s.value, 'chosen_spell')]
    assert not (_v is None and _self), __REBOUND__
    assert _v is not None, __NONE__
    assert type(_v).__name__ != 'str', __TEXT__ + ' ' + _QUOTES
    _copied = [_n for _s in _top() for _n in _made(_s) if _n in ('tune', 'hum')]
    assert not _copied, ('Use the name this step asks for, `chosen_spell`. `' + (_copied or [''])[0] + '` was the '
                         + "Example's name.")
    assert not (type(_v).__name__ == 'int' and _v == 0), __ZERO__
    assert False, __FIX__
'''

_CALLED_THROUGH = r'''
assert not _printed_call(lambda _c: _is_call(_c, 'chosen_spell')), __PRINTED__
_ns, _ls, _err, _miss = _rerun([('warm_hands', _wrap('warm_hands', '_log'))])
assert not _err, _stop(_err, 'ran your program again')
_log = _ns.get('_log', [])
_bare = [_s for _s in _top() if type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Name'
         and _s.value.id == 'chosen_spell']
if not _log:
    assert not _bare, __BARE__
    assert False, __CALL__
assert len(_log) == 1, __ONCE__ + ' ' + _ev('ran your program again', 'the function ran ' + str(len(_log)) + ' times')
assert _log[0] and _log[0][0] is _ns.get('lucky'), __LUCKY__
assert _top_calls('chosen_spell'), __THROUGH__
'''

NAME_WITHOUT_PARENTHESES = dict(
    id="name-without-parentheses",
    title="A name without parentheses",
    martu=(
        "In Unit 3, a recipe's name with no `()` did nothing. Now you learn what it *is*.\n"
        "`warm_hands(lucky)` runs the [[function]] now. `warm_hands` with no `()` is the function itself: a recipe "
        "card, not the meal. A variable can hold it, like any value: `chosen_spell = warm_hands`. Nothing runs "
        "yet.\n"
        "Later, `chosen_spell(lucky)` runs what the variable holds. The brackets are what call it.\n"
        "A recipe can sit in a box. You can hand it to someone without cooking it."
    ),
    example=HUM_EXAMPLE,
    example_output="Oogrish hums.",
    names=["chosen_spell", "warm_hands", "lucky"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=WARM_DEF + "\n\nchosen_spell = warm_hands\nprint(\"Spell chosen.\")\n",
        choices=["Spell chosen.", "an error", "warm_hands\nSpell chosen."],
        answer=0,
        explain=(
            "Only `Spell chosen.` The line `chosen_spell = warm_hands` has no `()`, so nothing runs: the variable "
            "now holds the function itself. No hero is needed yet, so there is no error either."
        ),
    ),
    pair_talk=(
        "Tell your partner what `chosen_spell` holds after step 1, and why nothing printed yet. Then each of you "
        "adds the call on your own screen."
    ),
    tracer=True,
    starter=NAME_STARTER,
    checkpoints=[
        dict(
            id="store-the-function",
            text="Replace the 0, so `chosen_spell` holds the function itself: `chosen_spell = warm_hands`, no `()`.",
            dictated=True,
            hints=[
                "Look at the line `chosen_spell = 0`. The 0 is a placeholder.",
                "A variable can hold a function, like any value. In the Example, `tune = hum` puts the function "
                "`hum` in `tune`. No `()`, so it does not run yet.",
                "Write `chosen_spell = warm_hands` in place of `chosen_spell = 0`.",
            ],
            checks=[
                chk(
                    "chosen_spell holds the function", _HOLDS_WARM,
                    keep="Keep the function `warm_hands` from the starter, made with `def`.",
                    rebound=("Call it on a line of its own, `chosen_spell(lucky)`, with nothing in front. "
                             "`chosen_spell = chosen_spell(lucky)` ran the function, then put what it handed back, "
                             "`None`, in `chosen_spell`, over the function."),
                    none=("Take the `()` off. `warm_hands(lucky)` ran the function right away, so `chosen_spell` "
                          "got what it handed back: `None`. Store the function itself."),
                    text="Take the quotes off `warm_hands`: `chosen_spell` holds just those letters.",
                    zero="Replace the 0 with `warm_hands`, the function's name with no `()`.",
                    fix="Store the function itself in `chosen_spell`: its name, `warm_hands`, with no `()`.",
                ),
            ],
            pass_line="Mar'tu: Nothing happened. Good. The box holds the recipe, not the meal.",
        ),
        dict(
            id="call-it-from-the-variable",
            text="Call the function from its new variable: `chosen_spell(lucky)`.",
            dictated=True,
            hints=[
                "Under comment 2, at the bottom. `chosen_spell` holds the function now, so it can be called.",
                "In the Example, `tune(oogrish)` calls the function inside `tune` and hands it the sheet. The "
                "brackets on the end are what call it.",
                "Write `chosen_spell(lucky)` on its own line at the bottom.",
            ],
            checks=[
                chk(
                    "one call, through chosen_spell", _CALLED_THROUGH,
                    printed=("Call it on its own line, with no `print(...)` around it. The function shows its own "
                             "line and hands back `None`, so the extra `print` showed `None`."),
                    bare=("Add `(lucky)` after `chosen_spell`. The name on its own only points at the function: "
                          "the brackets are what call it."),
                    call="Call the function through its variable, `chosen_spell`, with `lucky` in the brackets.",
                    once="Call it once, on one line.",
                    lucky="Hand over the sheet `lucky` in the brackets: `chosen_spell(lucky)`.",
                    through=("Call it through `chosen_spell`. Your line calls `warm_hands` by its own name: it "
                             "runs the same function, but this step is about the variable."),
                ),
            ],
            pass_line="Lucky: Warm hands. Fine. But I'm keeping track.",
        ),
    ],
    solution=NAME_SOLUTION,
    partials=[_name("chosen_spell = warm_hands\n")],
    assemble=dict(
        lines=[line for line in NAME_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["chosen_spell = warm_hands(lucky)", 'chosen_spell = "warm_hands"', "chosen_spell"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A box holding a recipe card",
            text=(
                "```text\nchosen_spell = warm_hands\n  box: [card: warm_hands]\n  nothing runs yet\n\n"
                "chosen_spell(lucky)\n  the card is cooked now\n  Lucky warms up.\n\n"
                "chosen_spell = warm_hands(lucky)\n  warm_hands runs NOW\n  box: None\n```"
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Handing someone a recipe card is not the same as cooking the meal and handing them the empty pot. "
                "`warm_hands` is the card. `warm_hands(lucky)` cooks it now, and what comes back is the empty pot, "
                "`None`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `def warm_hands(hero):` makes the function. Nothing runs.\n"
                "2. `chosen_spell = warm_hands` puts the same function in a second variable. Nothing runs.\n"
                "3. `chosen_spell(lucky)` runs it, with `lucky` as `hero`.\n"
                "4. The screen shows `Lucky warms up.`"
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? A name is a label",
            text=(
                "A function's name is a label on the function, like a variable's name is a label on a value. "
                "`chosen_spell = warm_hands` adds a second label to the same function. Either label can call it."
            ),
        ),
        dict(
            angle="from Unit 3",
            text=(
                "In Unit 3, `barrier_report` on a line by itself did nothing and gave no error. Now you know why: "
                "the name is the function itself. Only `()` runs it."
            ),
        ),
        dict(
            angle="try it",
            label="Cook it too early on purpose",
            text=(
                "After both ticks, change step 1 to `chosen_spell = warm_hands(lucky)` and Run. Read Python's last "
                "line: `chosen_spell` holds `None` now, and `None` can't be called. Then change it back."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet="strengthen_magic",
        why=(
            "The campaign said: notice that `strengthen_magic` is passed in without parentheses. You were handing "
            "over the function itself, so the game could call it later. That is what `chosen_spell = warm_hands` "
            "does."
        ),
    ),
    takeaway="`warm_hands` is the function itself; `warm_hands(lucky)` runs it now. A variable can hold a function.",
    wrong_answers=[
        dict(why="the starter (0 placeholder)", code=NAME_STARTER, fails_at=1, message_contains="Replace the 0"),
        dict(why="the Example's names copied (tune = warm_hands; tune(lucky))",
             code=_name("chosen_spell = 0\ntune = warm_hands\n", "tune(lucky)\n"), fails_at=1,
             message_contains="was the Example's name"),
        dict(why="stored the call (None), then called it: the explainer's NoneType row",
             code=_name("chosen_spell = warm_hands(lucky)\n", "chosen_spell(lucky)\n"), fails_at=0,
             message_contains="'NoneType' object is not callable"),
        dict(why="stored the result of a call where the function was wanted (NOP)",
             code=_name("chosen_spell = warm_hands(lucky)\n"), fails_at=1, message_contains="`None`"),
        dict(why="the function's name in quotes", code=_name('chosen_spell = "warm_hands"\n'), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="() with nothing inside (missing argument)", code=_name("chosen_spell = warm_hands()\n"),
             fails_at=0, message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="CP2 the bare name, no ()", code=_name("chosen_spell = warm_hands\n", "chosen_spell\n"), fails_at=2,
             message_contains="Add `(lucky)`"),
        dict(why="CP2 called by its own name, not through the variable",
             code=_name("chosen_spell = warm_hands\n", "warm_hands(lucky)\n"), fails_at=2,
             message_contains="through `chosen_spell`"),
        dict(why="CP2 a typed print instead of a call",
             code=_name("chosen_spell = warm_hands\n", 'print("Lucky warms up.")\n'), fails_at=2,
             message_contains="Call the function through its variable"),
        dict(why="CP2 print around the call (an extra None)",
             code=_name("chosen_spell = warm_hands\n", "print(chosen_spell(lucky))\n"), fails_at=2,
             message_contains="no `print(...)` around it"),
        dict(why="CP2 called twice", code=_name("chosen_spell = warm_hands\n",
                                                "chosen_spell(lucky)\nchosen_spell(lucky)\n"),
             fails_at=2, message_contains="once"),
        dict(why="CP2 the name typed as text (string indices)",
             code=_name("chosen_spell = warm_hands\n", 'chosen_spell("Lucky")\n'), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="CP2 the call's result stored over the function (chosen_spell = chosen_spell(lucky))",
             code=_name("chosen_spell = warm_hands\n", "chosen_spell = chosen_spell(lucky)\n"), fails_at=1,
             message_contains="over the function"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="func-as-value", solo="false", dictates="1,2",
             foreign_names="hum,sheet,tune,oogrish", stages="P,I,M", skill_gate="pattern:FuncValue",
             moment="the box holds the recipe (teacher-led, 5 min)") + "\n"
        "Mar'tu moment (6C-01, run-kit). Predict first: `chosen_spell = warm_hands` shows nothing. CP1 is NOP "
        "(identity with the starter's function: None, text and the 0 each get a message). CP2 is CALL through a "
        "rerun with warm_hands wrapped right after its def: exactly one call, with `lucky`, and the AST must call "
        "`chosen_spell` (a call by the function's own name gets its own message). The spec's catch, "
        "`chosen_spell = warm_hands(lucky)` then the call, crashes with 'NoneType' object is not callable: the "
        "explainer row, proven by a wrong answer. Investigate (one click, the Learn pane's 'try it'): change the "
        "store to `chosen_spell = warm_hands(lucky)` and read the error. WT: 'A name is a label'. TR: on."
    ),
)



# ---------------------------------------------------------------------------------------------
# 6C-02 hand-it-over
# ---------------------------------------------------------------------------------------------

EVERYONE_SETUP = _roster_setup()
EVERYONE_DEF = (
    "def cast_on_everyone(heroes, effect):\n"
    "    for hero in heroes:\n"
    "        effect(hero)\n"
)
HAND_HEAD = WARM_DEF + "\n\n" + EVERYONE_DEF + "\n\n# roster holds the four heroes.\n"
HAND_CP1_COMMENT = (
    "# 1. Call cast_on_everyone with\n"
    "#    roster and warm_hands, no ().\n"
)
HAND_CP2_COMMENT = (
    "# 2. Write cool_down(hero). It shows\n"
    "#    a line with the hero's name.\n"
    "#    Then hand it to\n"
    "#    cast_on_everyone too.\n"
)
HAND_CALL = "cast_on_everyone(roster, warm_hands)\n"
COOL_DEF = 'def cool_down(hero):\n    print(hero["name"], "cools down.")\n'
COOL_PASS = "cast_on_everyone(roster, cool_down)\n"


def _hand(call="", cool="", pass_on=""):
    out = HAND_HEAD + HAND_CP1_COMMENT + call + "\n" + HAND_CP2_COMMENT
    if cool:
        out += cool + "\n\n"
    return out + pass_on


HAND_STARTER = _hand()
HAND_SOLUTION = _hand(HAND_CALL, COOL_DEF, COOL_PASS)
NOD_EXAMPLE = (
    "def nod(sheet):\n"
    '    print(sheet["name"], "nods.")\n'
    "\n\n"
    "def to_each(sheets, action):\n"
    "    for sheet in sheets:\n"
    "        action(sheet)\n"
    "\n\n"
    'moth = {"name": "The moth"}\n'
    'glug = {"name": "Captain Glug"}\n'
    "to_each([moth, glug], nod)\n"
)

_HANDED_WARM = r'''
_ns, _ls, _err, _miss = _rerun([('warm_hands', _wrap('warm_hands', '_wlog')),
                                ('cast_on_everyone', _wrap('cast_on_everyone', '_clog'))])
assert not _miss, __KEEP__
assert _same_def('cast_on_everyone', __EVERYONE__), __KEEP_EVERYONE__
assert not _err, _stop(_err, 'ran your program again')
_w = _ns.get('_wlog', [])
_hand = [_a for _a in _ns.get('_clog', []) if len(_a) == 2 and _a[1] is _ns.get('warm_hands')]
if not _hand:
    assert not _w, __OWN_LOOP__
    assert False, __CALL__
assert len(_hand) == 1, __ONCE__
assert _hand[0][0] is _ns.get('roster'), __ROSTER__
_names = [_a[0].get('name') for _a in _w if _a and type(_a[0]).__name__ == 'dict']
_cd = _fdef('cool_down')
assert not (_cd is not None and len(_names) > 4 and [_n for _n in _ast.walk(_cd) if _is_call(_n, 'warm_hands')]), (
    __COOL_WARMS__)
assert _names == __NAMES__, __EVERY__ + ' ' + _ev('ran your program again', 'warm_hands ran ' + str(len(_w))
                                                     + ' times, not 4')
'''

_COOL_LINE = r'''
assert not (_fdef('shrug') is not None and _fdef('cool_down') is None), __EXAMPLE_NAME__
_fd = _need_def('cool_down', 1, 'def cool_down(hero):')
_b = {'name': 'Brakka', 'mana': 9, 'max_mana': 9}
_m = {'name': 'Moss', 'mana': 14, 'max_mana': 14}
for _sheet, _who in ((_b, 'brakka'), (_m, 'moss')):
    _v, _l, _e = _quiet(cool_down, _sheet)
    _what = 'called `cool_down(' + _who + ')`, a sheet named ' + _sheet['name']
    if _e is not None:
        assert not ("'dict'" in str(_e) and ('+' in str(_e) or 'concatenate' in str(_e))), __WHOLE_SHEET__
        assert False, _stop(_e, _what)
    if not _l:
        assert _v is None, __RETURNED__
        assert False, __NOTHING__
    assert not [_x for _x in _l if 'hero' in _x and _sheet['name'] not in _x], __QUOTED__ + ' ' + _QUOTES
    assert not [_x for _x in _l if "{'name': " in _x], __SHEET_SHOWN__ + ' ' + _ev(_what, 'the line showed every '
                                                                               'key on the sheet')
    assert [_x for _x in _l if _sheet['name'] in _x], __NAME__ + ' ' + _ev(_what, 'the line did not show '
                                                                          + _sheet['name'])
_wl = _quiet(_g['warm_hands'], _b)[1]
assert _quiet(cool_down, _b)[1] != _wl, __OWN__
'''

_HANDED_COOL = r'''
_ns, _ls, _err, _miss = _rerun([('cool_down', _wrap('cool_down', '_dlog')),
                                ('cast_on_everyone', _wrap('cast_on_everyone', '_clog'))])
assert not _err, _stop(_err, 'ran your program again')
_d = _ns.get('_dlog', [])
_hand = [_a for _a in _ns.get('_clog', []) if len(_a) == 2 and _a[1] is _ns.get('cool_down')]
if not _hand:
    assert not _d, __OWN_LOOP__
    assert False, __HAND__
assert _hand[0][0] is _ns.get('roster'), __ROSTER__
assert len(_d) == 4, __EVERY__ + ' ' + _ev('ran your program again', 'cool_down ran ' + str(len(_d)) + ' times, not 4')
'''

_TWICE = r'''
_fd = _need_def('cast_twice', 2, 'def cast_twice(effect, hero):')
_log = []
def _spark(_h):
    _log.append(_h)
_b = {'name': 'Brakka'}
_v, _ls, _e = _quiet(cast_twice, _spark, _b)
if _e is not None:
    assert 'not callable' not in str(_e), __ORDER__
    assert False, _stop(_e, 'called `cast_twice(spark, brakka)`')
assert _log, __CALL__
assert len(_log) == 2, __TWICE__ + ' ' + _ev('called `cast_twice(spark, brakka)`', 'spark ran ' + str(len(_log))
                                           + ' time' + ('' if len(_log) == 1 else 's'))
assert _log[0] is _b and _log[1] is _b, __HERO__
'''

_ROSTER_MSG = "Hand over `roster` itself, the list that is already made, so every hero in it is reached."

HAND_IT_OVER = dict(
    id="hand-it-over",
    title="Hand it over",
    martu=(
        "Now the strange part pays off. A function can be handed to another function, "
        "[[function as a value|like any value]].\n"
        "`cast_on_everyone(heroes, effect)` is finished. It walks the list, and for each hero it calls "
        "`effect(hero)`. It does not know which spell `effect` is. You choose, when you call it.\n"
        "Hand over the name with no `()`: `cast_on_everyone(roster, warm_hands)`. With `()`, the function would "
        "run once, right now, and hand over `None`.\n"
        "`roster` holds the four heroes. It is already made."
    ),
    example=NOD_EXAMPLE,
    example_output="The moth nods.\nCaptain Glug nods.",
    setup=EVERYONE_SETUP,
    names=["cast_on_everyone", "roster", "warm_hands", "cool_down", "hero"],
    pick='"cools down."',
    pair_talk=(
        "Tell your partner what `effect` holds inside `cast_on_everyone` during your first call. Then each of you "
        "writes `cool_down` on your own screen."
    ),
    starter=HAND_STARTER,
    checkpoints=[
        dict(
            id="hand-over-warm-hands",
            text="Call `cast_on_everyone` with `roster` and `warm_hands`, no parentheses.",
            dictated=True,
            hints=[
                "Below comment 1. The function is already finished: you only call it, with two values.",
                "In the Example, `to_each([moth, glug], nod)` hands over a list and a function. `nod` has no `()`: "
                "`to_each` calls it later, once for each sheet.",
                "Write `cast_on_everyone(roster, warm_hands)` below comment 1.",
            ],
            checks=[
                chk(
                    "warm_hands runs for every hero, through cast_on_everyone", _HANDED_WARM, EVERYONE_SETUP,
                    keep="Keep `warm_hands` and `cast_on_everyone` from the starter, made with `def`.",
                    everyone=EVERYONE_DEF,
                    keep_everyone=("Put `cast_on_everyone` back as the starter had it: it is already finished, so "
                                   "you only call it. Your copy changed it."),
                    cool_warms=("Make `cool_down` show its own line with `print(...)`. It calls `warm_hands`, so "
                                "every hero warms up a second time."),
                    own_loop=("Hand `warm_hands` to `cast_on_everyone`, with no `()`: it does the loop for you. "
                              "Your program calls `warm_hands` itself."),
                    call="Call `cast_on_everyone` below comment 1, with `roster` and `warm_hands`.",
                    once="Call `cast_on_everyone` with `warm_hands` once: one call already reaches every hero.",
                    roster=_ROSTER_MSG,
                    names=HERO_NAMES,
                    every="Hand `warm_hands` over once, so each hero warms up one time.",
                ),
            ],
            pass_line="Oogrish: Four warm hands, one line of code. Steady, now.",
        ),
        dict(
            id="your-own-spell",
            text="Write your own `cool_down(hero)`, which shows a line with the hero's name. Then hand it to "
                 "`cast_on_everyone` too.",
            dictated=False,
            hints=[
                "Copy the shape of `warm_hands`: a `def` line, then one `print` line that uses `hero[\"name\"]`. "
                "Then a second call to `cast_on_everyone`, at the bottom.",
                "`def shrug(sheet):` with `print(sheet[\"name\"], \"shrugs.\")` under it, indented, shows the name of "
                "whichever sheet it is handed.",
                "Hand it over the same way as step 1: the function's name, no `()`.",
                "Write `def cool_down(hero):` with `    print(hero[\"name\"], \"cools down.\")` under it (any words "
                "you like), then `cast_on_everyone(roster, cool_down)` at the bottom.",
            ],
            checks=[
                chk(
                    "cool_down shows each hero's own line", _COOL_LINE, EVERYONE_SETUP,
                    whole_sheet=("Read the name from the sheet, `hero[\"name\"]`. `hero` is the whole sheet, and "
                                 "`+` can't glue a sheet to text."),
                    returned=("Show the line with `print(...)` inside `cool_down`. `cast_on_everyone` does nothing "
                              "with what a function hands back, so a returned line never shows."),
                    nothing="Make `cool_down` show a line with `print(...)`, using the hero's name.",
                    quoted="Take the quotes off `hero`: your line showed the word hero.",
                    example_name=("Name your function `cool_down`, as the step asks. `shrug` was the hint's "
                                  "example name."),
                    sheet_shown=("Show just the name, `hero[\"name\"]`. `hero` on its own is the whole sheet, so "
                                 "your line showed every key and value on it."),
                    name="Use the name from the sheet handed in, `hero[\"name\"]`, so each hero gets their own line.",
                    own="Make `cool_down` show a line of your own: it shows the same line as `warm_hands`.",
                ),
                chk(
                    "cool_down is handed over too", _HANDED_COOL, EVERYONE_SETUP,
                    own_loop="Hand `cool_down` to `cast_on_everyone`, with no `()`. Your program calls `cool_down` "
                             "itself.",
                    hand="Hand `cool_down` over too: call `cast_on_everyone` again, with `roster` and `cool_down`.",
                    roster=_ROSTER_MSG,
                    every="Hand `cool_down` over once, so each hero cools down one time.",
                ),
            ],
            pass_line="Gearshift: Two spells, one loop. Visor dims. Math checks out.",
        ),
    ],
    solution=HAND_SOLUTION,
    partials=[_hand(HAND_CALL)],
    assemble=dict(
        lines=[line for line in HAND_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["cast_on_everyone(roster, warm_hands())", "cast_on_everyone(roster, cool_down(lucky))",
                     '    return hero["name"] + " cools down."'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Handing over the card",
            text=(
                "```text\ncast_on_everyone(roster,\n                 warm_hands)\n\ninside: effect = warm_hands\n"
                "  Oogrish:    effect(hero)\n  Gearshift:  effect(hero)\n"
                "  Bomb Shell: effect(hero)\n  Lucky:      effect(hero)\n```\n"
                "You hand over the card once. The loop cooks it four times."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "You hand a cook a recipe card and a list of guests. The cook makes the dish once for each guest. "
                "If you cooked it yourself first and handed over the empty pot, the cook would have nothing to "
                "follow."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `cast_on_everyone(roster, warm_hands)`: `heroes` holds `roster`, `effect` holds `warm_hands`.\n"
                "2. The loop takes the first hero. `effect(hero)` runs `warm_hands` on Oogrish.\n"
                "3. Then Gearshift, Bomb Shell and Lucky.\n"
                "4. Your `cool_down` works the same way: hand it over, and the loop runs it."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "The loop at the bottom of the spell book part called `add_spell(..., strengthen_magic)`. "
                "`strengthen_magic` had no `()` because the game would call it later, when someone cast the spell."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants double. Write `cast_twice(effect, hero)`: it calls `effect(hero)` two times. Try "
            "`cast_twice(warm_hands, lucky)` at the bottom."
        ),
        hints=[
            "Two parameters, the function first. Inside, the same call twice.",
            "`effect(hero)` runs whatever function `effect` holds, on that hero.",
            "Write `def cast_twice(effect, hero):` with `effect(hero)` twice under it, indented.",
        ],
        checks=[
            chk(
                "cast_twice runs the effect twice", _TWICE, EVERYONE_SETUP,
                order=("Put the parameters in the order `effect, hero`, the function first. Mar'tu's check "
                       "called `cast_twice(spark, brakka)`, and Python tried to call the sheet."),
                call="Call `effect(hero)` inside `cast_twice`: nothing called the function handed in.",
                twice="Call `effect(hero)` two times inside `cast_twice`.",
                hero="Hand the effect the hero that came in: `effect(hero)`.",
            ),
        ],
        solution=HAND_SOLUTION + "\n\ndef cast_twice(effect, hero):\n    effect(hero)\n    effect(hero)\n\n\n"
                                 "cast_twice(warm_hands, lucky)\n",
    ),
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet=(
            'add_spell(member["spell_book"],\n'
            '          "Strengthen Magic", 10, 8,\n'
            "          strengthen_magic)"
        ),
        why=(
            "You've handed a function over before. `strengthen_magic` went into `add_spell` with no `()`, so the "
            "game could call it later. `cast_on_everyone(roster, warm_hands)` is the same move."
        ),
    ),
    takeaway="Hand a function over by its name, no `()`: `cast_on_everyone(roster, warm_hands)`.",
    wrong_answers=[
        dict(why="the starter (nothing called)", code=HAND_STARTER, fails_at=1,
             message_contains="Call `cast_on_everyone`"),
        dict(why="handed over WITH () (missing argument)", code=_hand("cast_on_everyone(roster, warm_hands())\n"),
             fails_at=0, message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="handed over the result of a call: warm_hands(lucky) hands over None (the spec's NOP catch)",
             code=_hand("cast_on_everyone(roster, warm_hands(lucky))\n"), fails_at=0,
             message_contains="'NoneType' object is not callable"),
        dict(why="the function's name in quotes", code=_hand('cast_on_everyone(roster, "warm_hands")\n'), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="the two values in the wrong order", code=_hand("cast_on_everyone(warm_hands, roster)\n"),
             fails_at=0, message_contains="'function' object is not iterable"),
        dict(why="their own loop instead of handing it over",
             code=_hand("for hero in roster:\n    warm_hands(hero)\n"), fails_at=1,
             message_contains="does the loop for you"),
        dict(why="a typed list instead of roster",
             code=_hand("cast_on_everyone([oogrish, gearshift, bomb_shell, lucky], warm_hands)\n"), fails_at=1,
             message_contains="Hand over `roster` itself"),
        dict(why="handed over twice", code=_hand(HAND_CALL + HAND_CALL), fails_at=1, message_contains="once"),
        dict(why="CP2 cool_down returns its line instead of printing it",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    return hero["name"] + " cools down."\n', COOL_PASS),
             fails_at=2, message_contains="never shows"),
        dict(why="CP2 a typed name (the class's biggest slip)",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print("Lucky cools down.")\n', COOL_PASS),
             fails_at=2, message_contains='hero["name"]'),
        dict(why="CP2 the parameter in quotes",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print("hero", "cools down.")\n', COOL_PASS),
             fails_at=2, message_contains="Take the quotes off"),
        dict(why="CP2 the wrong sheet: Lucky's name read inside the function",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print(lucky["name"], "cools down.")\n', COOL_PASS),
             fails_at=2, message_contains="sheet handed in"),
        dict(why="CP2 the whole sheet glued to text, not handed over yet",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print(hero + " cools down.")\n'),
             fails_at=2, message_contains="whole sheet"),
        dict(why="CP2 the whole sheet glued to text, handed over (the loop crashes)",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print(hero + " cools down.")\n', COOL_PASS),
             fails_at=0, message_contains="unsupported operand type(s) for +: 'dict' and 'str'"),
        dict(why="CP2 the same line as warm_hands",
             code=_hand(HAND_CALL, WARM_DEF.replace("warm_hands", "cool_down"), COOL_PASS),
             fails_at=2, message_contains="same line as `warm_hands`"),
        dict(why="CP2 written but never handed over", code=_hand(HAND_CALL, COOL_DEF), fails_at=2,
             message_contains="Hand `cool_down` over too"),
        dict(why="CP2 called by its own loop",
             code=_hand(HAND_CALL, COOL_DEF, "for hero in roster:\n    cool_down(hero)\n"),
             fails_at=2, message_contains="calls `cool_down` itself"),
        dict(why="CP2 handed over WITH (lucky)",
             code=_hand(HAND_CALL, COOL_DEF, "cast_on_everyone(roster, cool_down(lucky))\n"),
             fails_at=0, message_contains="'NoneType' object is not callable"),
        dict(why="CP2 no parameter, but handed over",
             code=_hand(HAND_CALL, 'def cool_down():\n    print("Brr.")\n', COOL_PASS),
             fails_at=0, message_contains="takes 0 positional arguments but 1 was given"),
        dict(why="CP2 no parameter, never handed over",
             code=_hand(HAND_CALL, 'def cool_down():\n    print("Brr.")\n'),
             fails_at=2, message_contains="one parameter"),
        dict(why="CP2 the hint's example function copied (shrug), never named cool_down",
             code=_hand(HAND_CALL, 'def shrug(sheet):\n    print(sheet["name"], "shrugs.")\n',
                        "cast_on_everyone(roster, shrug)\n"),
             fails_at=2, message_contains="`shrug` was the hint's example name"),
        dict(why="CP2 the whole sheet printed, not its name (print(hero, ...))",
             code=_hand(HAND_CALL, 'def cool_down(hero):\n    print(hero, "cools down.")\n', COOL_PASS),
             fails_at=2, message_contains="every key and value"),
        dict(why="CP2 cool_down calls warm_hands instead of showing its own line",
             code=_hand(HAND_CALL, "def cool_down(hero):\n    warm_hands(hero)\n", COOL_PASS),
             fails_at=1, message_contains="a second time"),
        dict(why="a finished helper edited: cast_on_everyone calls warm_hands by name, ignoring effect",
             code=HAND_SOLUTION.replace("        effect(hero)\n", "        warm_hands(hero)\n"), fails_at=1,
             message_contains="already finished"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="func-as-value", solo="false", dictates="1",
             foreign_names="nod,sheet,to_each,sheets,action,moth,glug,shrug", stages="M,Mk") + "\n"
        "CALL x 4 through recorders: the rerun wraps warm_hands (or cool_down) and cast_on_everyone right after "
        "their defs, so the check sees what was handed over (identity) and how many times the effect ran. NOP "
        "slips crash first, so the explainer carries them: `warm_hands(lucky)` (NoneType), `warm_hands()` "
        "(missing argument), the name in quotes (str not callable), the values swapped (function not "
        "iterable); each is proven by a wrong answer. CP2 is creative (lint e): any line with the hero's own name "
        "passes (fresh sheets Brakka and Moss), except the same line as warm_hands. Return-instead-of-print gets "
        "the twist: here the effect must print, because cast_on_everyone ignores what comes back. Lucky's box: "
        "add_spell(..., strengthen_magic). BQ (G4 R16): cast_twice(effect, hero). The `def cast_on_everyone` line "
        "is 37 characters: the spec's names, kept. KEEP: CP1 also compares `cast_on_everyone` with the starter's "
        "(AST), so an edited helper gets its own message. The recorders take keyword calls too (`_wrap` binds them "
        "to parameter order). CP2 also names the whole sheet printed (`print(hero, ...)`), a `cool_down` that "
        "calls `warm_hands`, and the hint's `shrug` copied."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6C-03 recipe-in-a-box
# ---------------------------------------------------------------------------------------------

LANTERN_SETUP = (
    "_lanterns = []\n"
    "\n\n"
    "def light_lantern(hero):\n"
    "    _lanterns.append(hero)\n"
    '    print(hero["name"], "lights a lantern.")\n'
)
GLOW_DICT = (
    "glow = {\n"
    '    "mana_cost": 2,\n'
    '    "required_affinity": 3,\n'
    '    "effect": light_lantern,\n'
    "}\n"
)
LANTERN_NOTE = (
    "# light_lantern is already made.\n"
    "# It shows: <name> lights a lantern.\n"
)
BOX_COMMENT = (
    "# 1. Cast Glow on Lucky from the\n"
    "#    dictionary: glow[\"effect\"],\n"
    "#    then (lucky) on the end.\n"
)
LUCKY_BOOK = 'lucky_book = {"Glow": glow}\n'
BOOK_COMMENT = (
    "# 2. Cast Glow again, from\n"
    "#    lucky_book, in one line.\n"
)
BOX_CAST = 'glow["effect"](lucky)\n'
BOOK_CAST = 'lucky_book["Glow"]["effect"](lucky)\n'


def _box(line="", book_line=""):
    return (LANTERN_NOTE + GLOW_DICT + "\n" + LUCKY_SMALL + "\n" + BOX_COMMENT + line + "\n" + LUCKY_BOOK + "\n"
            + BOOK_COMMENT + book_line)


BOX_STARTER = _box()
BOX_SOLUTION = _box(BOX_CAST, BOOK_CAST)
JAR_EXAMPLE = (
    "def hum(sheet):\n"
    '    print(sheet["name"], "hums.")\n'
    "\n\n"
    'tune = {"notes": 3, "play": hum}\n'
    'moth = {"name": "The moth"}\n'
    'tune["play"](moth)\n'
)

_BOX_ROOT = r'''
def _root_of(_t):
    # The name a chain of keys starts from: lucky_book["Glow"]["effect"] -> lucky_book.
    while type(_t).__name__ == 'Subscript':
        _t = _t.value
    return _t.id if type(_t).__name__ == 'Name' else None
def _from(_c, _name):
    return type(_c.func).__name__ == 'Subscript' and _root_of(_c.func) == _name
def _bare_from(_name):
    return [_s for _s in _top() if type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Subscript'
            and _root_of(_s.value) == _name]
'''

_CAST_FROM_BOX = _BOX_ROOT + r'''
assert not _printed_call(lambda _c: _from(_c, 'glow')), __PRINTED__
_gl = _g.get('glow')
assert not (type(_gl).__name__ == 'dict' and 'effect' in _gl and _gl['effect'] is None), __STORED_CALL__
assert type(_gl).__name__ == 'dict' and _gl.get('effect') is _g.get('light_lantern'), __KEEP__
_lit_for = list(_g.get('_lanterns', []))
if not _lit_for:
    assert not _bare_from('glow'), __BARE__
    assert False, __CALL__
assert _lit_for[0] is _g.get('lucky'), __LUCKY__
# The lanterns lit before lucky_book is made are step 1's (step 2's line sits under it).
_ns, _ls, _err, _miss = _rerun([('*glow', _stand_in('_other') + 'glow["effect"] = _fx\n'),
                                ('lucky_book', '_above = len(_other)\n')])
assert '*glow' not in _miss, __KEEP__
assert not _err, _stop(_err, 'ran your program again')
_o = _ns.get('_other', [])
assert _o, __THROUGH__ + ' ' + _ev('put another effect in `glow`', 'it never ran')
assert [_c for _s in _top() for _c in _ast.walk(_s) if type(_c).__name__ == 'Call' and _from(_c, 'glow')], (
    __GLOW_FIRST__)
assert _ns.get('_above', len(_o)) <= 1, __ONCE__
'''

_CAST_FROM_BOOK = _BOX_ROOT + r'''
assert not _printed_call(lambda _c: _from(_c, 'lucky_book')), __PRINTED__
_bk = _g.get('lucky_book')
assert type(_bk).__name__ == 'dict' and _bk.get('Glow') is _g.get('glow'), __KEEP_BOOK__
_lit_for = list(_g.get('_lanterns', []))
if len(_lit_for) < 2:
    assert not _bare_from('lucky_book'), __BARE__
    assert False, __CALL__
assert len(_lit_for) == 2, __ONCE__
assert _lit_for[1] is _g.get('lucky'), __LUCKY__
# The page IS glow, so a stand-in can't tell the two casts apart: the line itself must read the book.
def _book_call(_c):
    _f = _c.func
    return (type(_f).__name__ == 'Subscript' and type(_f.slice).__name__ == 'Constant'
            and _f.slice.value == 'effect' and type(_f.value).__name__ == 'Subscript'
            and type(_f.value.value).__name__ == 'Name' and _f.value.value.id == 'lucky_book')
if not [_c for _s in _top() for _c in _ast.walk(_s) if type(_c).__name__ == 'Call' and _book_call(_c)]:
    _kept = [_s for _s in _top() if type(_s).__name__ == 'Assign' and type(_s.value).__name__ == 'Subscript'
             and _root_of(_s.value) == 'lucky_book']
    assert not _kept, __ONE_LINE__
    assert False, __FROM_BOOK__
'''

RECIPE_IN_A_BOX = dict(
    id="recipe-in-a-box",
    title="A recipe in a box",
    martu=(
        "A dictionary can hold a function too. Look at `glow`: its `\"effect\"` key holds `light_lantern`, with "
        "no `()`. The spell keeps its recipe on its own page.\n"
        "`glow[\"effect\"]` reads the function out of the dictionary. On its own, it does nothing. Add "
        "`(lucky)` on the end, and the function runs: `glow[\"effect\"](lucky)`.\n"
        "Read it left to right: the dictionary, the key, then the brackets that call it.\n"
        "A spell book is a dictionary of pages. From a book, read the page by its name first, then the key, "
        "then call it."
    ),
    example=JAR_EXAMPLE,
    example_output="The moth hums.",
    setup=LANTERN_SETUP,
    names=["glow", "lucky", "lucky_book"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=(
            "# light_lantern(hero) shows:\n"
            "#   <name> lights a lantern.\n"
            'glow = {"effect": light_lantern}\n'
            'lucky = {"name": "Lucky"}\n'
            'glow["effect"]\n'
            'glow["effect"](lucky)\n'
        ),
        choices=["Lucky lights a lantern.", "Lucky lights a lantern.\nLucky lights a lantern.", "an error",
                 "light_lantern\nLucky lights a lantern."],
        answer=0,
        explain=(
            "One line. `glow[\"effect\"]` on its own reads the function and does nothing with it. The last line "
            "adds `(lucky)`, and that call runs it. The brackets on the end are what call it."
        ),
    ),
    starter=BOX_STARTER,
    checkpoints=[
        dict(
            id="cast-from-the-dictionary",
            text="Cast Glow on Lucky from the dictionary: `glow[\"effect\"]`, then `(lucky)` on the end.",
            dictated=True,
            hints=[
                "Below comment 1. Read the effect out of `glow`, then call it.",
                "In the Example, `tune[\"play\"](moth)` reads the function under `\"play\"`, then calls it with "
                "`moth`.",
                "Write `glow[\"effect\"](lucky)` on its own line under comment 1.",
            ],
            checks=[
                chk(
                    "Glow's effect runs once, on Lucky", _CAST_FROM_BOX, LANTERN_SETUP,
                    printed=("Cast it on its own line, with no `print(...)` around it. The effect shows its own "
                             "line and hands back `None`, so the extra `print` showed `None`."),
                    stored_call=("Keep `glow` as the starter made it, and cast with a line of its own: "
                                 "`glow[\"effect\"](lucky)`. Your line ran `light_lantern(lucky)` and stored what it "
                                 "handed back, `None`, under `\"effect\"`."),
                    keep="Keep `glow` from the starter, with `light_lantern` under `\"effect\"`.",
                    bare=("Add `(lucky)` on the end. `glow[\"effect\"]` on its own reads the function out of the "
                          "dictionary, but nothing calls it: the brackets are what call it."),
                    call="Cast Glow below comment 1: `glow[\"effect\"]`, with `(lucky)` on the end.",
                    once="Cast it once under comment 1, on one line.",
                    lucky="Hand over the sheet `lucky` in the brackets.",
                    through=("Cast it from the dictionary, so Glow's own effect runs. Your line calls "
                             "`light_lantern` by its own name."),
                    glow_first=("Cast it from `glow` first, under comment 1: `glow[\"effect\"]`, then `(lucky)`. "
                                "`lucky_book` is step 2."),
                ),
            ],
            pass_line="Bomb Shell: Lantern's lit. Works.",
        ),
        dict(
            id="cast-from-a-book",
            text="Cast Glow again, from `lucky_book`, in one line.",
            dictated=False,
            hints=[
                "Under comment 2. `lucky_book[\"Glow\"]` is the page.",
                "Two keys in a row read inside a page: `shelf[\"Plum\"][\"lid\"]`. Brackets with a value on the "
                "end call what is there.",
                "Write `lucky_book[\"Glow\"][\"effect\"](lucky)` on its own line.",
            ],
            checks=[
                chk(
                    "Glow is cast a second time, from lucky_book", _CAST_FROM_BOOK, LANTERN_SETUP,
                    printed=("Cast it on its own line, with no `print(...)` around it. The effect shows its own "
                             "line and hands back `None`, so the extra `print` showed `None`."),
                    keep_book="Keep `lucky_book` from the starter: `lucky_book = {\"Glow\": glow}`.",
                    bare=("Add `(lucky)` on the end. `lucky_book[\"Glow\"][\"effect\"]` on its own reads the "
                          "function from the page, but nothing calls it."),
                    call=("Cast Glow again under comment 2, from `lucky_book`: the page by its name, then "
                          "`\"effect\"`, then `(lucky)`."),
                    once="Cast Glow two times in all: once from `glow`, once from `lucky_book`.",
                    lucky="Hand over the sheet `lucky` in the brackets.",
                    from_book="Cast it from `lucky_book` this time: the page by its name, then `\"effect\"`.",
                    one_line=("Cast it in one line, straight from `lucky_book`: the page, then `[\"effect\"]`, then "
                              "`(lucky)`. Your cast goes through a variable in between."),
                ),
            ],
            pass_line="Lucky: From my own book. Now that's a spell I can keep.",
        ),
    ],
    solution=BOX_SOLUTION,
    partials=[_box(BOX_CAST)],
    assemble=dict(
        lines=[line for line in BOX_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=['glow["effect"]', 'glow("effect")(lucky)', "light_lantern(lucky)", 'lucky_book["Glow"](lucky)'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A recipe card on a page",
            text=(
                "```text\nglow\n  \"mana_cost\"         2\n  \"required_affinity\" 3\n"
                "  \"effect\"  [card: light_lantern]\n\nglow[\"effect\"]         the card\n"
                "glow[\"effect\"](lucky)  cook it\n\nlucky_book[\"Glow\"]     the page\n"
                "lucky_book[\"Glow\"][\"effect\"]\n                       the card\n"
                "lucky_book[\"Glow\"][\"effect\"](lucky)\n                       cook it\n```"
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "In `cast_spell`, the campaign wrote `spell[\"spell_function\"](caster)` and said: this works "
                "because the dictionary is holding a function. The parentheses on the end are what call it. "
                "`glow[\"effect\"](lucky)` is the same line with this lesson's names."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `glow` is the dictionary.\n"
                "2. `glow[\"effect\"]` is the value under `\"effect\"`: the function `light_lantern`.\n"
                "3. `(lucky)` calls that function, with `lucky` as its hero.\n"
                "4. The screen shows `Lucky lights a lantern.`"
            ),
        ),
        dict(
            angle="shorter",
            text=(
                "Dictionary, key, brackets: `glow[\"effect\"](lucky)`. A book adds one key in front, the page: "
                "`lucky_book[\"Glow\"][\"effect\"](lucky)`."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE,
        part="hold-the-barrier",
        snippet='spell["spell_function"](caster)',
        why=(
            "This is the line that cast the barrier spell. `spell[\"spell_function\"]` read the function out of "
            "the spell's dictionary, and `(caster)` called it. Now you have written one yourself."
        ),
    ),
    takeaway=(
        "Call a function stored in a dictionary: the key, then the brackets: `glow[\"effect\"](lucky)`. From a "
        "book, the page first: `lucky_book[\"Glow\"][\"effect\"](lucky)`."
    ),
    wrong_answers=[
        dict(why="the starter (nothing cast)", code=BOX_STARTER, fails_at=1, message_contains="Cast Glow below"),
        dict(why="no (lucky): the function is read but never called (the spec's catch)",
             code=_box('glow["effect"]\n'), fails_at=1, message_contains="Add `(lucky)`"),
        dict(why="empty brackets (missing argument)", code=_box('glow["effect"]()\n'), fails_at=0,
             message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="called by its own name, not from the dictionary", code=_box("light_lantern(lucky)\n"), fails_at=1,
             message_contains="by its own name"),
        dict(why="round brackets on the dictionary", code=_box('glow("effect")(lucky)\n'), fails_at=0,
             message_contains="'dict' object is not callable"),
        dict(why="the key without quotes", code=_box("glow[effect](lucky)\n"), fails_at=0,
             message_contains="name 'effect' is not defined"),
        dict(why="print around the call (an extra None)", code=_box('print(glow["effect"](lucky))\n'), fails_at=1,
             message_contains="no `print(...)` around it"),
        dict(why="the dictionary handed to its own effect (KeyError)", code=_box('glow["effect"](glow)\n'),
             fails_at=0, message_contains="KeyError: 'name'"),
        dict(why="cast twice", code=_box('glow["effect"](lucky)\nglow["effect"](lucky)\n'), fails_at=1,
             message_contains="once"),
        dict(why="stored the result of a call where the function was wanted: glow[\"effect\"] = light_lantern(lucky)",
             code=_box('glow["effect"] = light_lantern(lucky)\n'), fails_at=1, message_contains="stored what it"),
        dict(why="step 1 skipped: only the lucky_book line (the same dict, so a stand-in alone can't tell)",
             code=_box("", BOOK_CAST), fails_at=1, message_contains="Cast it from `glow` first"),
        dict(why="CP2 the starter's step 1 done, step 2 not yet", code=_box(BOX_CAST), fails_at=2,
             message_contains="Cast Glow again under comment 2"),
        dict(why="CP2 the page called without \"effect\" (the page is a dict)",
             code=_box(BOX_CAST, 'lucky_book["Glow"](lucky)\n'), fails_at=0,
             message_contains="'dict' object is not callable"),
        dict(why="CP2 the page's name in lower case (KeyError)",
             code=_box(BOX_CAST, 'lucky_book["glow"]["effect"](lucky)\n'), fails_at=0,
             message_contains="KeyError: 'glow'"),
        dict(why="CP2 no (lucky): read from the book, never called",
             code=_box(BOX_CAST, 'lucky_book["Glow"]["effect"]\n'), fails_at=2, message_contains="nothing calls it"),
        dict(why="CP2 glow[\"effect\"](lucky) again instead of from the book",
             code=_box(BOX_CAST, BOX_CAST), fails_at=2, message_contains="Cast it from `lucky_book` this time"),
        dict(why="CP2 print around the call (an extra None)",
             code=_box(BOX_CAST, 'print(lucky_book["Glow"]["effect"](lucky))\n'), fails_at=2,
             message_contains="no `print(...)` around it"),
        dict(why="CP2 light_lantern called by its own name", code=_box(BOX_CAST, "light_lantern(lucky)\n"),
             fails_at=2, message_contains="Cast it from `lucky_book` this time"),
        dict(why="CP2 the page kept in a variable first: two lines, not the one-line form",
             code=_box(BOX_CAST, 'page = lucky_book["Glow"]\npage["effect"](lucky)\n'), fails_at=2,
             message_contains="Cast it in one line"),
        dict(why="CP2 cast twice from the book", code=_box(BOX_CAST, BOOK_CAST + BOOK_CAST), fails_at=2,
             message_contains="two times in all"),
        dict(why="CP2 lucky_book deleted from the starter",
             code=_box(BOX_CAST).replace(LUCKY_BOOK, ""), fails_at=2, message_contains="Keep `lucky_book`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="call-stored-func", solo="false", dictates="1",
             foreign_names="hum,sheet,tune,notes,play,moth,shelf,Plum,lid", stages="P,M",
             skill_gate="pattern:CallOnSubscript")
        + "\n"
        "CP1 is CALL with the setup's light_lantern recorder: the first lantern is for `lucky`. Then a rerun swaps "
        "`glow[\"effect\"]` for a stand-in right after `glow` is made: the stand-in must run, so the call goes "
        "through the dictionary (a call by name fails, the spec's 'from the dict'), and the AST must hold a call "
        "read from `glow` (the lucky_book line alone shares the same dict). 'Once' counts the stand-in's calls "
        "before `lucky_book` is made, so step 2's line under comment 2 never trips step 1. The missing `(lucky)` "
        "gets its own message (a bare subscript statement). `glow` itself must keep light_lantern (KEEP). CP2 "
        "(the teacher's addition, unit goal 7's `book[name][\"effect\"](hero)`, which Quick Check C4 needs; "
        "goal-only): two lanterns, the second on `lucky`. The page IS `glow`, so a stand-in can't tell the two "
        "casts apart: the AST must hold a top-level call whose function is `lucky_book[...][\"effect\"]`; a second "
        "`glow[\"effect\"](lucky)` is told to cast from `lucky_book`. `lucky_book[\"Glow\"](lucky)` ('dict' "
        "object is not callable) and `lucky_book[\"glow\"]` (KeyError) are the explainer's. The predict shows "
        "what `light_lantern` does in two comment lines (the real def stays in the setup, with the recorder); "
        "the starter says the same above `glow`, wrapped to 36 characters."
    ),
)



# ---------------------------------------------------------------------------------------------
# 6C-04 write-the-spell-book (rehearsal: spell-book; campaign mode; introduces None)
# ---------------------------------------------------------------------------------------------

WARD_FNS = (
    "_wards = []\n"
    "\n\n"
    "def lantern_ward(hero):\n"
    "    _wards.append(hero)\n"
    '    print(hero["name"] + "\'s ward glows.")\n'
    "\n\n"
    "def light_lantern(hero):\n"
    '    print(hero["name"], "lights a lantern.")\n'
    "\n\n"
)
GLOW_PAGE = '{"Glow": {"mana_cost": 2, "required_affinity": 3, "effect": light_lantern}}'
BOOK_SETUP = _roster_setup(WARD_FNS, GLOW_PAGE)
LEARN_SIGNATURE = "def learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect):\n"
LEARN_PARAMS = ["spell_book", "spell_name", "mana_cost", "required_affinity", "effect"]
LEARN_LOOP = (
    "# The loop below is already written.\n"
    "# Every hero learns Lantern Ward.\n"
    "for hero in roster:\n"
    '    learn_spell(hero["spell_book"], "Lantern Ward", 6, 9, lantern_ward)\n'
)
LEARN_STORE = "    spell_book[spell_name] = spell\n"
# The last line shows False until the store works (CP2), then True: CP3 and CP4 never pass on a blank console.
LEARN_SHOW = (
    "\n"
    "# Is Lantern Ward in Lucky's book?\n"
    'print("Lantern Ward" in lucky["spell_book"])\n'
)


def _learn(cost="0", need="0", effect="None", store="", loop=LEARN_LOOP, head=LEARN_SIGNATURE, show=LEARN_SHOW):
    return (
        head +
        "    # 1. Replace each placeholder\n"
        "    #    with the matching\n"
        "    #    parameter.\n"
        "    spell = {\n"
        f'        "mana_cost": {cost},\n'
        f'        "required_affinity": {need},\n'
        f'        "effect": {effect},\n'
        "    }\n"
        "    # 2. Store the spell in\n"
        "    #    spell_book, using\n"
        "    #    spell_name as the key.\n"
        + store + "\n\n" + loop + show
    )


LEARN_STARTER = _learn()
LEARN_FILLED = dict(cost="mana_cost", need="required_affinity", effect="effect")
LEARN_SOLUTION = _learn(store=LEARN_STORE, **LEARN_FILLED)
JAR_SHELF_EXAMPLE = (
    "def add_jar(shelf, label, size):\n"
    '    jar = {"size": size}\n'
    "    shelf[label] = jar\n"
    "\n\n"
    "pantry = {}\n"
    'add_jar(pantry, "Honey", 2)\n'
    "print(pantry)\n"
)

_LEARN_PRE = r'''
_fd = _fdef('learn_spell')
assert _fd is not None and callable(_g.get('learn_spell')), __KEEP_DEF__
_params = __PARAMS__
assert [_a.arg for _a in _fd.args.args] == _params, __KEEP_SIG__
_fired = []
def _spark(*_a):
    _fired.append('spark')
_spark.__name__ = 'spark'
def _glimmer(*_a):
    _fired.append('glimmer')
_glimmer.__name__ = 'glimmer'
def _learn_call(_nm, _c, _r, _fx):
    return 'called `learn_spell(book, "' + _nm + '", ' + str(_c) + ', ' + str(_r) + ', ' + _fx.__name__ + ')`'
def _built(_bk, _sp):
    # The spell as built: the local `spell`, or, when there is none, the one page written into the book.
    if type(_sp).__name__ == 'dict':
        return _sp
    _pages = [_p for _p in _bk.values() if type(_p).__name__ == 'dict']
    return _pages[0] if len(_pages) == 1 else _sp
def _root(_t):
    while type(_t).__name__ == 'Subscript':
        _t = _t.value
    return _t.id if type(_t).__name__ == 'Name' else None
_other_book = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Assign'
               and [_t for _t in _n.targets if type(_t).__name__ == 'Subscript'
                    and _root(_t) not in (None, 'spell_book', 'spell')]]
'''

_SPELL_BUILT = r'''
_want = ('mana_cost', 'required_affinity', 'effect')
for _nm, _c, _r, _fx in (('Frost Veil', 5, 7, _spark), ('Moon Step', 11, 4, _glimmer)):
    _call = _learn_call(_nm, _c, _r, _fx)
    _bk = {}
    del _fired[:]
    _w0 = len(_g.get('_wards', []))
    _sp, _val, _ls, _err = _peek(learn_spell, (_bk, _nm, _c, _r, _fx), 'spell')
    assert _err is None, _stop(_err, _call)
    _sp = _built(_bk, _sp)
    assert type(_sp).__name__ == 'dict', __KEEP_SPELL__
    _k, _x = _key_slip(_sp, _want)
    if _k is not None:
        assert _x is None or type(_x).__name__ == 'str', ('Put quotes around the key `"' + _k + '"`: the spell has '
                                                          'a key ' + _lit(_x) + ', a value, not a label. ' + _QUOTES)
        assert _x is None, ('The spell has a key `"' + str(_x) + '"`, and the game reads `"' + _k + '"`, letter '
                            'for letter.')
        assert False, __MISSING_KEY__.replace('<key>', _k)
    _mc, _ra, _ef = _sp['mana_cost'], _sp['required_affinity'], _sp['effect']
    _q = [_p for _p, _v in zip(_want, (_mc, _ra, _ef)) if type(_v).__name__ == 'str' and _v in _params]
    assert not _q, ('Take the quotes off `' + (_q or [''])[0] + '`: the spell holds the text `"' + (_q or [''])[0]
                    + '"`, just those letters. Use the parameter without quotes. ' + _QUOTES)
    assert not (_mc == 0 and _ra == 0 and _ef is None), __PLACEHOLDERS__
    assert not (_mc == _r and _ra == _c), __SWAP__ + ' ' + _ev(_call, '`"mana_cost"` held ' + str(_mc))
    if _mc != _c:
        assert _mc != 0, __ZERO_COST__
        assert _mc != 6, __TYPED_COST__ + ' ' + _ev(_call, 'the spell still held 6')
        assert False, __COST__ + ' ' + _ev(_call, '`"mana_cost"` held ' + _lit(_mc) + ', not ' + str(_c))
    if _ra != _r:
        assert _ra != 0, __ZERO_NEED__
        assert _ra != 9, __TYPED_NEED__ + ' ' + _ev(_call, 'the spell still held 9')
        assert False, __NEED__ + ' ' + _ev(_call, '`"required_affinity"` held ' + _lit(_ra) + ', not ' + str(_r))
    if _ef is not _fx:
        assert not (_ef is None and _fired), __CALLED_EFFECT__ + ' ' + _ev(_call, 'spark ran at once, and the spell '
                                                                         'held `None`')
        assert not (_ef is None and len(_g.get('_wards', [])) > _w0), __CALLED_WARD__ + ' ' + _ev(
            _call, 'Lantern Ward ran at once, and the spell held `None`')
        assert _ef is not None, __NONE_EFFECT__
        assert _ef is not _g.get('lantern_ward'), __TYPED_EFFECT__ + ' ' + _ev(_call, 'the spell still held '
                                                                              '`lantern_ward`')
        assert False, __EFFECT__ + ' ' + _ev(_call, '`"effect"` held ' + _lit(_ef))
'''

_SPELL_STORED = r'''
for _nm, _c, _r, _fx in (('Frost Veil', 5, 7, _spark), ('Moon Step', 11, 4, _glimmer)):
    _bk = {}
    _call = _learn_call(_nm, _c, _r, _fx)
    _sp, _val, _ls, _err = _peek(learn_spell, (_bk, _nm, _c, _r, _fx), 'spell')
    assert _err is None, _stop(_err, _call)
    assert 'spell_name' not in _bk, __QUOTED_KEY__ + ' ' + _QUOTES
    if _nm not in _bk:
        _typed = [_k for _k in _bk if _k in ('Lantern Ward', 'Frost Veil', 'Moon Step')]
        assert not _typed, __TYPED_KEY__ + ' ' + _ev(_call, 'the book got a page called ' + (_typed or [''])[0])
        assert not _bk, __OTHER_KEY__ + ' ' + _ev(_call, 'the book got a page under ' + _lit(list(_bk)[0])
                                                  if _bk else '')
        _reb = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Assign'
                and [_t for _t in _n.targets if type(_t).__name__ == 'Name' and _t.id == 'spell_book']]
        assert not _reb, __REBIND__ + ' ' + _ev(_call, 'the book handed in stayed empty')
        assert not _other_book, __OTHER_BOOK__ + ' ' + _ev(_call, 'the book handed in stayed empty')
        assert _val is None, __RETURNED__ + ' ' + _ev(_call, 'the book handed in stayed empty')
        assert False, __STORE__ + ' ' + _ev(_call, 'the book handed in stayed empty')
    _pg = _bk[_nm]
    assert type(_pg).__name__ == 'dict', __PAGE_TEXT__
    assert type(_sp).__name__ != 'dict' or _pg is _sp or _pg == _sp, __PAGE__
'''

_SECOND_KEEPS_FIRST = r'''
_bk = {}
_call = 'stored Frost Veil, then Moon Step, in one book'
for _nm, _c, _r, _fx in (('Frost Veil', 5, 7, _spark), ('Moon Step', 11, 4, _glimmer)):
    _val, _ls, _err = _quiet(learn_spell, _bk, _nm, _c, _r, _fx)
    assert _err is None, _stop(_err, _learn_call(_nm, _c, _r, _fx))
assert 'Moon Step' in _bk, __SECOND__ + ' ' + _ev(_call, 'the book had no Moon Step page')
assert 'Frost Veil' in _bk, __FIRST_LOST__ + ' ' + _ev(_call, 'the Frost Veil page was gone')
_f = _bk['Frost Veil']
assert type(_f).__name__ == 'dict' and _f.get('mana_cost') == 5 and _f.get('effect') is _spark, (
    __SHARED__ + ' ' + _ev(_call, "Frost Veil's page held Moon Step's values"))
'''

_EVERY_HERO = r'''
assert type(_g.get('roster')).__name__ == 'list' and len(roster) == 4, __KEEP_ROSTER__
_loops = [_s for _s in _tree().body if type(_s).__name__ == 'For']
assert _loops, __KEEP_LOOP__
assert [_c for _s in _loops for _c in _ast.walk(_s) if _is_call(_c, 'learn_spell')], __LOOP_CALL__
for _h in roster:
    _bk = _h.get('spell_book') if type(_h).__name__ == 'dict' else None
    assert type(_bk).__name__ == 'dict', __KEEP_ROSTER__
    assert 'Glow' in _bk, __GLOW__
    _pg = _bk.get('Lantern Ward')
    assert type(_pg).__name__ == 'dict', __MISSING__ + ' ' + _ev('looked in ' + _h.get('name', 'a hero') + "'s book",
                                                                 'no Lantern Ward page')
    _ef = _pg.get('effect')
    if _ef is not _g.get('lantern_ward'):
        assert not (_ef is None and _g.get('_wards')), __CALLED_NOW__
        assert type(_ef).__name__ != 'str', __EFFECT_TEXT__ + ' ' + _QUOTES
        assert False, __EFFECT__
    assert _pg.get('mana_cost') == 6 and _pg.get('required_affinity') == 9, __VALUES__
'''

_LEARN_KEEP = dict(
    keep_def="Keep `learn_spell` from the starter, made with `def`.",
    keep_sig="Keep the `def` line from the starter: its five parameters, in that order, are part of the task.",
    params=LEARN_PARAMS,
)


def learn_check(label, body, **messages):
    return (label, sx(BOOK_SETUP) + fill(_LEARN_PRE, **_LEARN_KEEP) + fill(body, **messages))


_BUILT_MSGS = dict(
    keep_spell="Keep the variable `spell` from the starter, a dictionary inside `learn_spell`.",
    placeholders="Replace each placeholder with the matching parameter: the spell still holds 0, 0 "
                 "and `None`.",
    swap="You swapped them: `\"mana_cost\"` holds the required affinity. Each key takes the "
         "parameter with its own name.",
    zero_cost="Replace the 0 after `\"mana_cost\"` with the matching parameter, `mana_cost`.",
    typed_cost="Use the parameter `mana_cost`, not a typed 6: each call hands over its own cost.",
    cost="`\"mana_cost\"` should hold the parameter `mana_cost`.",
    zero_need="Replace the 0 after `\"required_affinity\"` with the matching parameter, "
              "`required_affinity`.",
    typed_need="Use the parameter `required_affinity`, not a typed 9: each call hands over its "
               "own need.",
    need="`\"required_affinity\"` should hold the parameter `required_affinity`.",
    called_effect=("Take the `()` off: store `effect` itself. `effect(hero)` ran the function "
                   "handed in right away, and the spell kept what it handed back, `None`."),
    called_ward=("Use the parameter `effect`, with no `()`. `lantern_ward(hero)` ran the ward right "
                 "away, and the spell kept what it handed back, `None`."),
    none_effect="Replace `None` with the matching parameter, `effect`.",
    typed_effect="Use the parameter `effect`, not `lantern_ward`: each call hands over its own "
                 "effect.",
    effect="`\"effect\"` should hold the parameter `effect`, the function handed in.",
    missing_key='Keep the key `"<key>"` in `spell`, as the starter has it. Change only the value after the colon.',
)

_STORED_MSGS = dict(
    quoted_key="Take the quotes off `spell_name`: the book got a page called `\"spell_name\"`, "
               "those exact letters.",
    typed_key="Use `spell_name` as the key, not a typed name, so each spell gets its own page.",
    other_key="Use `spell_name` as the key: the book got a page under another key.",
    rebind=("Store into the book handed in: `spell_book[spell_name] = spell`. `spell_book = {...}` "
            "makes a new dictionary inside the function, so the caller's book stayed empty."),
    other_book=("Store the spell in `spell_book`, the book handed in. Your line writes into "
                "another book, so the one handed in stayed empty."),
    returned=("Store the spell in the book itself. `return` hands the spell back, but the book "
              "handed in stays empty, and the loop never uses what comes back."),
    store="Replace comment 2 with one line that stores the spell in `spell_book`, using `spell_name` "
          "as the key.",
    page_text="Store the spell itself, `spell`, with no quotes.",
    page="Store the spell you built, `spell`, on that page.",
)

_SECOND_MSGS = dict(
    second="Store every spell you are handed: the second spell never reached the book.",
    first_lost="Keep the first spell: add a page with `spell_book[spell_name] = spell`, and leave "
               "the other pages alone.",
    shared=("Give each spell its own dictionary: build `spell = {...}` inside `learn_spell`, so "
            "every call makes a new one."),
)


WRITE_THE_SPELL_BOOK = dict(
    id="write-the-spell-book",
    title="Write the spell book",
    martu=(
        "The spell book from the campaign, with our names. `learn_spell` builds a spell, then stores it in a "
        "hero's book.\n"
        "The placeholders are `0`, `0` and `None`. [[None]] is Python's word for *nothing here yet*. You have seen "
        "it printed when a function hands nothing back. Here it holds the place of a function.\n"
        "Replace each placeholder with the matching parameter: the one with exactly the key's name. Then store the "
        "spell by its name.\n"
        "The loop at the bottom is already written. Its `lantern_ward` has no `()`: the ward is handed over, to "
        "be cast later. The last line asks Lucky's book about Lantern Ward: `False` until your store works, then "
        "`True`."
    ),
    example=JAR_SHELF_EXAMPLE,
    example_output="{'Honey': {'size': 2}}",
    introduces=["const:None"],
    setup=BOOK_SETUP,
    names=["learn_spell", "spell", "spell_book", "spell_name", "mana_cost", "required_affinity", "effect"],
    pair_talk=(
        "Tell your partner which key matches which parameter, and why the loop's `lantern_ward` has no `()`. Then "
        "each of you fills the spell on your own screen."
    ),
    starter=LEARN_STARTER,
    checkpoints=[
        dict(
            id="matching-parameters",
            text="Replace each placeholder in `spell` with the matching parameter. Same name, no quotes.",
            dictated=True,
            hints=[
                "Each key in `spell` has a parameter with exactly the same name in the `def` line. That parameter "
                "is its match.",
                "A value can be a parameter: in the Example, `{\"size\": size}` puts whatever was handed in as "
                "`size` there. No quotes on the value: quotes would make it just the letters.",
                "Write `\"mana_cost\": mana_cost,` then `\"required_affinity\": required_affinity,` then "
                "`\"effect\": effect,` in place of the three placeholder lines.",
            ],
            checks=[
                learn_check(
                    "the spell holds the matching parameters", _SPELL_BUILT,
                    **_BUILT_MSGS,
                ),
            ],
            pass_line="Gearshift: Every key, its own parameter. Math checks out.",
        ),
        dict(
            id="store-by-name",
            text="Store the spell in `spell_book`, using `spell_name` as the key.",
            dictated=True,
            hints=[
                "Comment 2 marks the spot, inside the function, under `spell`. The key is the parameter "
                "`spell_name`, with no quotes.",
                "In the Example, `shelf[label] = jar` stores the jar under whatever text `label` holds, in the "
                "shelf that was handed in.",
                "Write `spell_book[spell_name] = spell` under comment 2, indented inside the function.",
            ],
            checks=[
                learn_check(
                    "the spell is stored under its name", _SPELL_STORED,
                    **_STORED_MSGS,
                ),
            ],
            pass_line="Oogrish: One page, under its own name. Steady, now.",
        ),
        dict(
            id="a-second-spell",
            text=("Press Run. Nothing new to type: Mar'tu's check tests this. A second spell stored in the same "
                  "book must keep the first."),
            hints=[
                "Look at your store line. It should add one page to the book, and leave the other pages alone.",
                "`book[name] = page` adds one key. A new `{...}` would make a new book with only that page.",
                "Keep `spell = {...}` inside the function, so every call builds its own spell, and write "
                "`spell_book[spell_name] = spell` under it.",
            ],
            checks=[
                learn_check(
                    "a second spell keeps the first", _SECOND_KEEPS_FIRST,
                    **_SECOND_MSGS,
                ),
            ],
            pass_line="Mar'tu: Two pages. Neither one ate the other. Good.",
        ),
        dict(
            id="every-hero-knows-it",
            text=("Press Run. Nothing new to type: Mar'tu's check tests this. The loop at the bottom gives every "
                  "hero Lantern Ward."),
            hints=[
                "Look at the loop at the bottom. It was already finished: check it still hands over `lantern_ward` "
                "with no `()`.",
                "`lantern_ward` is the function itself. `lantern_ward(hero)` runs it now and hands over what it "
                "gives back, `None`.",
                "Write the loop's line as "
                "`learn_spell(hero[\"spell_book\"], \"Lantern Ward\", 6, 9, lantern_ward)`.",
            ],
            checks=[
                learn_check(
                    "every hero knows Lantern Ward", _EVERY_HERO,
                    keep_roster="Keep `roster` as it is: four hero sheets, each with its spell book.",
                    keep_loop="Keep the loop at the bottom: it is already written, and it teaches every hero.",
                    loop_call=("Keep the loop's call to `learn_spell`, as it was written. Your loop writes the "
                               "pages itself, so `learn_spell` is never used."),
                    glow="Keep Glow in every book: add the new page, don't make a new book.",
                    missing="Keep the loop's call to `learn_spell`, so every hero learns Lantern Ward.",
                    called_now=("Hand over `lantern_ward` itself, with no `()`. `lantern_ward(hero)` ran the ward "
                                "right away (the early lines on screen), and the book stored what it handed back: "
                                "`None`."),
                    effect_text="Hand over the function, `lantern_ward`, with no quotes.",
                    effect="Hand over `lantern_ward`, as the loop had it.",
                    values="Keep the loop's values: Lantern Ward costs 6 and needs an affinity of 9.",
                ),
            ],
            pass_line="Bomb Shell: Four books. One ward each. Shield up.",
        ),
    ],
    solution=LEARN_SOLUTION,
    partials=[_learn(**LEARN_FILLED)],
    another_way=[
        dict(
            angle="picture",
            label="Each key, its matching parameter",
            text=(
                "```text\nkey (quotes)   value (no quotes)\n\"mana_cost\"  <- mana_cost\n"
                "\"required_affinity\"\n             <- required_affinity\n\"effect\"     <- effect\n\n"
                "spell_book[spell_name] = spell\n  the page's name: no quotes\n```"
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "This is `add_spell()`. You replaced each placeholder with the matching parameter, then wrote "
                "`spell_book[spell_name] = spell`. The campaign's `\"spell_function\"` is our `\"effect\"`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The loop calls `learn_spell(hero[\"spell_book\"], \"Lantern Ward\", 6, 9, lantern_ward)`.\n"
                "2. Inside, `mana_cost` holds 6, `required_affinity` holds 9, `effect` holds `lantern_ward`.\n"
                "3. `spell` is built from those parameters.\n"
                "4. `spell_book[spell_name] = spell` writes the page into the hero's own book."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? The book outside changes",
            text=(
                "`spell_book` is not a copy. It is the hero's own book, handed in. A change by key reaches the "
                "caller. Only `spell_book = {...}` would point the name at a new, empty book."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet=(
            "spell = {\n"
            '    "mana_cost": mana_cost,\n'
            '    "required_affinity":\n'
            "        required_affinity,\n"
            '    "spell_function":\n'
            "        spell_function,\n"
            "}\n"
            "spell_book[spell_name] = spell"
        ),
        why=(
            "This was the finished `add_spell`. You replaced each placeholder with the matching parameter and "
            "stored the spell under its name. Now you know why the names had to match exactly."
        ),
    ),
    takeaway="Each key takes the parameter with its exact name; then `spell_book[spell_name] = spell`.",
    wrong_answers=[
        dict(why="the starter (0, 0, None)", code=LEARN_STARTER, fails_at=1, message_contains="still holds 0, 0"),
        dict(why="literal test values typed in (the class's biggest slip)",
             code=_learn("6", "9", "lantern_ward", LEARN_STORE), fails_at=1, message_contains="not a typed 6"),
        dict(why="the parameter quoted inside the dict ({\"mana_cost\": \"mana_cost\"})",
             code=_learn('"mana_cost"', '"required_affinity"', '"effect"', LEARN_STORE), fails_at=1,
             message_contains="Take the quotes off `mana_cost`"),
        dict(why="swapped parameters (SWAP)",
             code=_learn("required_affinity", "mana_cost", "effect", LEARN_STORE), fails_at=1,
             message_contains="swapped"),
        dict(why="an approximate key the game doesn't read (\"magic\" for \"required_affinity\")",
             code=LEARN_SOLUTION.replace('"required_affinity": required_affinity', '"magic": required_affinity'),
             fails_at=1, message_contains='"magic"`, and the game reads'),
        dict(why="a near-miss key (capitals)",
             code=LEARN_SOLUTION.replace('"mana_cost": mana_cost', '"Mana_Cost": mana_cost'), fails_at=1,
             message_contains="letter for letter"),
        dict(why="a key with no quotes (the value became the key)",
             code=LEARN_SOLUTION.replace('"mana_cost": mana_cost', "mana_cost: mana_cost"), fails_at=1,
             message_contains="Put quotes around the key"),
        dict(why="effect left as None", code=_learn("mana_cost", "required_affinity", "None", LEARN_STORE),
             fails_at=1, message_contains="Replace `None`"),
        dict(why="CP2 the variable key in quotes: spell_book[\"spell_name\"]",
             code=_learn(store='    spell_book["spell_name"] = spell\n', **LEARN_FILLED), fails_at=2,
             message_contains='"spell_name"'),
        dict(why="CP2 a new dictionary: the caller won't see the change (spell_book = {...})",
             code=_learn(store="    spell_book = {spell_name: spell}\n", **LEARN_FILLED), fails_at=2,
             message_contains="new dictionary inside the function"),
        dict(why="CP2 return instead of changing the dict passed in",
             code=_learn(store="    return spell\n", **LEARN_FILLED), fails_at=2, message_contains="`return` hands"),
        dict(why="CP2 the name typed as the key",
             code=_learn(store='    spell_book["Lantern Ward"] = spell\n', **LEARN_FILLED), fails_at=2,
             message_contains="its own page"),
        dict(why="CP2 the word spell in quotes",
             code=_learn(store='    spell_book[spell_name] = "spell"\n', **LEARN_FILLED), fails_at=2,
             message_contains="no quotes"),
        dict(why="CP2 the store line not indented (outside the function: NameError)",
             code=_learn(store="spell_book[spell_name] = spell\n", **LEARN_FILLED), fails_at=0,
             message_contains="name 'spell' is not defined"),
        dict(why="CP3 one shared spell for every call (same sheet, two labels)",
             code=('spell = {"mana_cost": 0, "required_affinity": 0, "effect": None}\n\n\n' + LEARN_SIGNATURE
                   + '    spell["mana_cost"] = mana_cost\n'
                   '    spell["required_affinity"] = required_affinity\n'
                   '    spell["effect"] = effect\n' + LEARN_STORE + "\n\n" + LEARN_LOOP),
             fails_at=3, message_contains="its own dictionary"),
        dict(why="CP4 lantern_ward(hero) in the bottom loop (NOP: hands over None)",
             code=_learn(store=LEARN_STORE, loop=LEARN_LOOP.replace("lantern_ward)", "lantern_ward(hero))"),
                         **LEARN_FILLED),
             fails_at=4, message_contains="no `()`"),
        dict(why="CP4 the function's name in quotes in the loop",
             code=_learn(store=LEARN_STORE, loop=LEARN_LOOP.replace("lantern_ward)", '"lantern_ward")'),
                         **LEARN_FILLED),
             fails_at=4, message_contains="no quotes"),
        dict(why="CP4 the finished loop deleted", code=_learn(store=LEARN_STORE, loop="", **LEARN_FILLED),
             fails_at=4, message_contains="Keep the loop"),
        dict(why="the effect called with () inside the dict: effect(hero) stores None (passing a function WITH ())",
             code=_learn("mana_cost", "required_affinity", "effect(hero)", LEARN_STORE), fails_at=1,
             message_contains="Take the `()` off"),
        dict(why="the loop's typed function called inside the dict: lantern_ward(hero)",
             code=_learn("mana_cost", "required_affinity", "lantern_ward(hero)", LEARN_STORE), fails_at=1,
             message_contains="ran the ward right away"),
        dict(why="CP2 the check's own spell name typed as the key (reverse-engineered from the message)",
             code=_learn(store='    spell_book["Frost Veil"] = spell\n', **LEARN_FILLED), fails_at=2,
             message_contains="not a typed name"),
        dict(why="CP2 the wrong sheet: stored in the loop's hero[\"spell_book\"], not the book handed in",
             code=_learn(store='    hero["spell_book"][spell_name] = spell\n', **LEARN_FILLED), fails_at=2,
             message_contains="writes into another book"),
        dict(why="CP4 the finished loop rewritten to skip learn_spell",
             code=_learn(store=LEARN_STORE, loop='for hero in roster:\n    hero["spell_book"]["Lantern Ward"] = '
                                                 '{"mana_cost": 6, "required_affinity": 9, "effect": lantern_ward}\n',
                         **LEARN_FILLED),
             fails_at=4, message_contains="never used"),
        dict(why="the def line changed (a parameter renamed)",
             code=_learn(store=LEARN_STORE, head=LEARN_SIGNATURE.replace("required_affinity", "affinity"),
                         cost="mana_cost", need="affinity", effect="effect"),
             fails_at=1, message_contains="five parameters"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-from-params,store-by-name,func-as-value", solo="false",
             dictates="1,2", foreign_names="add_jar,shelf,label,size,jar,pantry,Honey,book,page",
             rehearsal="spell-book", camp="true", stages="A,M",
             par='("Frost Veil", 5, 7, spark),("Moon Step", 11, 4, glimmer)') + "\n"
        "Rehearsal in campaign mode (2.10): numbered comments, the campaign's phrasing ('Replace each placeholder "
        "with the matching parameter', 'using spell_name as the key'), check messages and the explainer, Compare "
        "after 5 minutes, hints capped at rung 2. No Assemble it, as the spec says (the Show me more Assemble-first "
        "view is off here), so there is no `assemble` field. CP1-CP4 mirror the campaign's four checks. CP1 reads "
        "the local `spell` as the call ends (sys.settrace), so it can be checked before the store exists; fresh "
        "values only (lint b: never 6, 9, lantern_ward). `None` is introduced here, exactly as the campaign's "
        "`\"spell_function\": None` placeholder (concept_map: u07b const:None). The signature and the loop's call "
        "are the campaign's long lines, kept. Every hero's book starts with Glow, so CP4 also proves the store "
        "adds a page. One partial only: once the store line is in, CP3 and CP4 pass too. A spell written straight "
        "into the book (no `spell` variable) is accepted: CP1 then reads the one page the call stored. CP1 names "
        "`effect(hero)` / `lantern_ward(hero)` inside the dict (the recorders show the function ran at once). CP2 "
        "stores two names in fresh books, so a typed key (even the check's own Frost Veil) fails, and a store into "
        "the loop's `hero[\"spell_book\"]` is named. CP4: the loop must still call `learn_spell`. The starter ends "
        "with `print(\"Lantern Ward\" in lucky[\"spell_book\"])` (lucky is a setup sheet): it shows False until CP2's "
        "store works, then True, so CP3 and CP4 (no new typing: 'Nothing new to type: Mar'tu's check tests this') "
        "never turn green on a blank console. CP4's keep_loop looks only for a top-level `for`, so the line is "
        "tolerated."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6C-05 cast-from-the-book (rehearsal: hold-the-barrier; campaign mode, with the More-structure ladder)
# ---------------------------------------------------------------------------------------------

CAST_SETUP = (
    "_wards = []\n"
    "_bars = []\n"
    "\n\n"
    "def lantern_ward(hero):\n"
    "    _wards.append(hero)\n"
    '    print(hero["name"] + "\'s ward glows.")\n'
    "\n\n"
    "def show_mana(hero):\n"
    '    _bars.append((hero, hero["mana"]))\n'
    '    full = "█" * hero["mana"]\n'
    '    empty = "░" * (hero["max_mana"] - hero["mana"])\n'
    '    print(hero["name"] + ": Mana [" + full + empty + "]")\n'
    "\n\n"
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    '    "max_mana": 26,\n'
    '    "abilities": {"magical_affinity": 13},\n'
    '    "spell_book": {\n'
    '        "Lantern Ward": {"mana_cost": 6, "required_affinity": 9, "effect": lantern_ward},\n'
    "    },\n"
    "}\n"
)
CAST_HEAD = (
    "# show_mana(hero) is already made.\n"
    "\n\n"
    "def cast(hero, spell_name):\n"
    '    if spell_name not in hero["spell_book"]:\n'
    '        print(hero["name"], "doesn\'t know", spell_name)\n'
    "        return\n"
    "    # Get it:\n"
    '    spell = hero["spell_book"][spell_name]\n'
    "\n"
    "    # Compare:\n"
    "    # 1. If the hero's affinity is\n"
    "    #    lower than the spell's\n"
    '    #    "required_affinity": print\n'
    "    #    that they aren't skilled.\n"
    '    # 2. Otherwise, if hero["mana"]\n'
    "    #    is lower than the spell's\n"
    '    #    "mana_cost": print that\n'
    "    #    they need more mana.\n"
    "    # Act:\n"
    "    # 3. Otherwise: call the spell's\n"
    "    #    effect on hero, subtract\n"
    '    #    its "mana_cost", and call\n'
    "    #    show_mana(hero).\n"
)
CAST_CALL = '\n\ncast(lucky, "Lantern Ward")\n'
AFF_TEST = 'hero["abilities"]["magical_affinity"] < spell["required_affinity"]'
MANA_TEST = 'hero["mana"] < spell["mana_cost"]'
PAY = '        hero["mana"] = hero["mana"] - spell["mana_cost"]\n'
SKILL_MSG = '        print(hero["name"], "isn\'t skilled enough.")\n'
MANA_MSG = '        print(hero["name"], "needs more mana.")\n'


def _cast_body(aff=AFF_TEST, mana=MANA_TEST, effect='spell["effect"](hero)', pay=PAY, show="        show_mana(hero)\n",
               skill_msg=SKILL_MSG, mana_msg=MANA_MSG):
    return (f"    if {aff}:\n" + skill_msg + f"    elif {mana}:\n" + mana_msg + "    else:\n"
            f"        {effect}\n" + pay + show)


def _cast(body="    pass\n", call=CAST_CALL):
    return CAST_HEAD + body + call


CAST_STARTER = _cast()
CAST_SOLUTION = _cast(_cast_body())
TYPED_PAY = '    hero["mana"] = hero["mana"] - 6\n'
TYPED_PAY_8 = '        hero["mana"] = hero["mana"] - 6\n'
CAST_P1 = _cast('    spell["effect"](hero)\n')
CAST_P2 = _cast('    spell["effect"](hero)\n' + TYPED_PAY + "    show_mana(hero)\n")
CAST_P3 = _cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + "    else:\n        spell[\"effect\"](hero)\n" + TYPED_PAY_8
                + "        show_mana(hero)\n")
CAST_P4 = _cast(_cast_body(mana='hero["mana"] <= spell["mana_cost"]', pay=TYPED_PAY_8))
CAST_P5 = _cast(_cast_body(pay=TYPED_PAY_8))

_CAST_PRE = r'''
_fd = _fdef('cast')
assert _fd is not None and callable(_g.get('cast')), __KEEP_DEF__
assert [_a.arg for _a in _fd.args.args] == ['hero', 'spell_name'], __KEEP_SIG__
_wrong_sheet = bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Name' and _n.id == 'lucky'])
_guard_ifs = [_n for _n in _fd.body if type(_n).__name__ == 'If' and type(_n.test).__name__ == 'Compare'
              and type(_n.test.ops[0]).__name__ == 'NotIn']
_ifs = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'If' and _n not in _guard_ifs]
_typed_cmp = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Compare'
              and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
                   and type(_x.value).__name__ == 'int']]
def _key_read(_key):
    return bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Subscript'
                 and type(_n.slice).__name__ == 'Constant' and _n.slice.value == _key])
_max_read = _key_read('max_mana')
_into_spell = [_n for _n in _ast.walk(_fd) if type(_n).__name__ in ('Assign', 'AugAssign')
               and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
                    if type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name'
                    and _t.value.id == 'spell']]
def _why(_m):
    if _wrong_sheet:
        return __WRONG_SHEET__
    return __MAX_READ__ if _max_read else _m
def _cast(_aff, _mana, _cost, _need):
    _fx = []
    def moon_step(hero):
        _fx.append(hero)
        print('Moon Step lands.')
    _hero = {'name': 'Brakka', 'mana': _mana, 'max_mana': 20, 'abilities': {'magical_affinity': _aff},
             'spell_book': {'Moon Step': {'mana_cost': _cost, 'required_affinity': _need, 'effect': moon_step}}}
    _bars, _wards = _g.get('_bars', []), _g.get('_wards', [])
    _b0, _w0 = len(_bars), len(_wards)
    _val, _ls, _err = _quiet(_g['cast'], _hero, 'Moon Step')
    _what = ('cast Moon Step (cost ' + str(_cost) + ', needs affinity ' + str(_need) + ') for a hero with '
             'affinity ' + str(_aff) + ' and mana ' + str(_mana))
    _msgs = [_l for _l in _ls if _l != 'Moon Step lands.' and 'Mana [' not in _l]
    return dict(fx=_fx, msgs=_msgs, left=_hero['mana'], bars=_bars[_b0:], wards=_wards[_w0:], err=_err,
                hero=_hero, what=_what)
def _crash(_r):
    _e = _r['err']
    if type(_e).__name__ == 'KeyError' and 'magical_affinity' in str(_e):
        return __NESTED__ + ' ' + _ev(_r['what'], 'Python stopped with ' + _err_text(_e))
    if type(_e).__name__ == 'NameError' and getattr(_e, 'name', '') == 'caster':
        return __CASTER__
    if type(_e).__name__ == 'KeyError' and str(_e) in ("'mana_cost'", "'required_affinity'"):
        return __SPELL_KEY__ + ' ' + _ev(_r['what'], 'Python stopped with ' + _err_text(_e))
    if type(_e).__name__ == 'KeyError' and str(_e) in ("'mana'", "'abilities'", "'name'"):
        return __HERO_KEY__ + ' ' + _ev(_r['what'], 'Python stopped with ' + _err_text(_e))
    return _stop(_e, _r['what'])
'''

_CASTS = r'''
_r = _cast(12, 15, 5, 7)
assert _r['err'] is None, _crash(_r)
if not _r['fx']:
    _bare = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Subscript']
    assert not _bare, __BARE__ + ' ' + _ev(_r['what'], 'the spell never ran')
    assert not _r['wards'], __BY_NAME__ + ' ' + _ev(_r['what'], 'Lantern Ward ran instead')
    assert not _r['msgs'], _why(__REFUSED__) + ' ' + _ev(_r['what'], 'the hero was turned away')
    assert False, __CAST__ + ' ' + _ev(_r['what'], 'the spell never ran')
assert len(_r['fx']) == 1, __ONCE__
assert _r['fx'][0] is _r['hero'], _why(__HERO__)
'''

_BAR_UPDATES = r'''
_r = _cast(12, 15, 5, 7)
assert _r['err'] is None, _crash(_r)
if _r['left'] == 15:
    _sub = [_n for _n in _ast.walk(_fd) if (type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp')
            or (type(_n).__name__ == 'Assign' and type(_n.targets[0]).__name__ == 'Name'
                and type(_n.value).__name__ == 'BinOp')]
    assert not _sub, __STORE_BACK__ + ' ' + _ev(_r['what'], 'the mana stayed at 15')
    assert not _into_spell, __INTO_SPELL__ + ' ' + _ev(_r['what'], "the hero's mana stayed at 15")
    assert False, _why(__SUBTRACT__) + ' ' + _ev(_r['what'], 'the mana stayed at 15')
assert _r['left'] < 15, __SUBTRACT__ + ' ' + _ev(_r['what'], 'the mana went up to ' + str(_r['left']))
assert _r['bars'], __SHOW__
_hb, _mb = _r['bars'][-1]
assert _hb is _r['hero'], _why(__SHOW_HERO__)
assert _mb == _r['left'], __SHOW_AFTER__ + ' ' + _ev(_r['what'], 'the bar showed ' + str(_mb)
                                                     + ' mana, and the mana ended at ' + str(_r['left']))
'''

_TURNS_AWAY = r'''
def _effect_line(_s):
    return (type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Call'
            and type(_s.value.func).__name__ == 'Subscript')
def _open_chain(_s):
    # an if (or if / elif chain) with no last `else`
    while len(_s.orelse) == 1 and type(_s.orelse[0]).__name__ == 'If':
        _s = _s.orelse[0]
    return not _s.orelse
# An `if` with no `else` straight in the function, and the cast still at function level below it: the hero hears
# the message, then casts anyway (the cast lines were never moved under `else:`).
_open_if = [_i for _i, _s in enumerate(_fd.body) if type(_s).__name__ == 'If' and _open_chain(_s)
            and _s not in _guard_ifs]
_no_else = bool(_open_if) and bool([_i for _i, _s in enumerate(_fd.body) if _effect_line(_s) and _i > _open_if[0]])
for _aff, _mana, _cost, _need, _kind in __CASES__:
    _r = _cast(_aff, _mana, _cost, _need)
    assert _r['err'] is None, _crash(_r)
    if _kind == 'low':
        if _r['fx']:
            assert not (_r['msgs'] and _no_else), __NO_ELSE__ + ' ' + _ev(_r['what'], 'the message showed, then '
                                                                          'the spell ran anyway')
            assert not _typed_cmp, __TYPED__ + ' ' + _ev(_r['what'], 'the spell ran anyway')
            assert False, _why(__TURN_AWAY__) + ' ' + _ev(_r['what'], 'the spell ran anyway')
        assert _r['left'] == _mana, __SPEND__ + ' ' + _ev(_r['what'], 'the mana went down anyway')
        assert _r['msgs'], __TELL__ + ' ' + _ev(_r['what'], 'nothing was printed')
        assert len(_r['msgs']) == 1, __ONE_MSG__ + ' ' + _ev(_r['what'], str(len(_r['msgs'])) + ' messages showed')
        _named = [_n for _n in __HEROES__ if _n in _r['msgs'][0] and 'Brakka' not in _r['msgs'][0]]
        assert not _named, __TYPED_NAME__ + ' ' + _ev(_r['what'] + ', a hero named Brakka', 'the message named '
                                                      + (_named or [''])[0])
    else:
        assert _r['fx'], __EXACT__ + ' ' + _ev(_r['what'], 'the hero was turned away')
'''

_OWN_COST = r'''
for _cost, _want in ((3, 12), (8, 7)):
    _r = _cast(12, 15, _cost, 7)
    assert _r['err'] is None, _crash(_r)
    if _r['left'] != _want:
        _end = 'the mana ended at ' + str(_r['left']) + ', not ' + str(_want)
        assert _r['left'] != 9, __TYPED_COST__ + ' ' + _ev(_r['what'], _end)
        assert _r['left'] != _cost - 15, __REVERSED__ + ' ' + _ev(_r['what'], _end)
        assert False, _why(__OWN__) + ' ' + _ev(_r['what'], _end)
'''

_CAST_KEEP = dict(
    keep_def="Keep `cast` from the starter, made with `def`.",
    keep_sig="Keep the `def` line from the starter: `def cast(hero, spell_name):`.",
    wrong_sheet=("Read from `hero`, the sheet handed in: your function uses `lucky`, so every caster is judged, or "
                 "cast on, as Lucky."),
    max_read=("Use `hero[\"mana\"]`, the mana the hero has now. Your function reads `\"max_mana\"`, the most the "
              "hero can hold, not what is left."),
    nested="Read the affinity inside `\"abilities\"`: `hero[\"abilities\"][\"magical_affinity\"]`, outer key first.",
    caster="Use this function's parameter, `hero`: `caster` was the campaign's name, and it is not defined here.",
    spell_key=("Read the spell's numbers from its page, like `spell[\"mana_cost\"]`: the hero's sheet has no such "
               "key."),
    hero_key="Read the hero's own values from the hero's sheet, like `hero[\"mana\"]`: the spell's page has no such key.",
)


def cast_check(label, body, **messages):
    return (label, sx(CAST_SETUP) + fill(_CAST_PRE, **_CAST_KEEP) + fill(body, **messages))


_NO_ELSE_MSG = ("Put `else:` above your three cast lines and indent them one more step. Right now they sit outside "
                "the `if`, so the hero hears the message and then casts anyway.")
_TURN_MSGS = dict(
    no_else=_NO_ELSE_MSG,
    spend="Spend nothing when the hero can't cast: keep the subtraction in the last branch, `else`.",
    tell="Print a message when the hero can't cast, so the player knows why.",
    one_msg="Use `elif` for the mana test, so only one message shows.",
    heroes=HERO_NAMES,
    typed_name=("Use `hero[\"name\"]` in the message, so it names whoever is casting. Your message has a typed "
                "name in it."),
)

BREW_TWIN = (
    "```python\ndef brew(cook, name):\n    pot = cook[\"shelf\"][name]\n    if cook[\"skill\"] < pot[\"skill\"]:\n"
    "        print(\"Too hard.\")\n    elif cook[\"herb\"] < pot[\"cost\"]:\n        print(\"Need herbs.\")\n"
    "    else:\n        pot[\"effect\"](cook)\n        # then pay: the line below\n```\n"
    "The pay line is too wide for this picture. It goes last, one step in under `else:`, like the line above "
    "it: `cook[\"herb\"] = cook[\"herb\"] - pot[\"cost\"]`."
)

_CASTS_MSGS = dict(
    bare=("Add `(hero)` on the end: `spell[\"effect\"]` on its own reads the function but doesn't "
          "call it. The brackets on the end are what call it."),
    by_name=("Call the spell's own effect, `spell[\"effect\"](hero)`. Your line calls "
             "`lantern_ward` by name, so every spell would cast Lantern Ward."),
    refused=("Let a skilled caster with enough mana cast. Check each sign: `<` means *lower than*."),
    cast="Call the spell's effect under comment 3, in place of `pass`: `spell[\"effect\"](hero)`.",
    once="Call the effect once per cast.",
    hero="Hand the caster to the effect, `spell[\"effect\"](hero)`: your line handed over another "
         "sheet.",
)

_BAR_MSGS = dict(
    store_back=("Store the new mana back in the sheet: `hero[\"mana\"] = hero[\"mana\"] - "
                "spell[\"mana_cost\"]`. The subtraction on its own works the number out, then "
                "forgets it."),
    into_spell=("Store the new mana in the hero's sheet, `hero[\"mana\"] = ...`. Your line stores "
                "it in the spell's page, so the hero still has all their mana."),
    subtract="Subtract the spell's cost from `hero[\"mana\"]`, after the cast.",
    show="Call `show_mana(hero)` after the subtraction, so the bar updates.",
    show_hero="Hand `show_mana` the caster, `hero`: it drew another sheet's bar.",
    show_after="Call `show_mana(hero)` after the subtraction: the bar showed the old mana.",
)

_OWN_COST_MSGS = dict(
    typed_cost="Subtract the spell's own cost, `spell[\"mana_cost\"]`, not a typed 6.",
    reversed="Put `hero[\"mana\"]` first: the mana minus the cost, not the cost minus the mana.",
    own="Subtract the spell's own cost, `spell[\"mana_cost\"]`.",
)


CAST_FROM_THE_BOOK = dict(
    id="cast-from-the-book",
    title="Cast from the book",
    martu=(
        "The barrier, rebuilt. The guard and the first read are done: the hero must know the spell, then `spell` "
        "holds its page.\n"
        "You write the rest. Get it, compare, act:\n"
        "1. If the affinity is too low, say so.\n"
        "2. Otherwise, if the mana is too low, say so.\n"
        "3. Otherwise, cast: call `spell[\"effect\"](hero)`, pay the cost, show the bar.\n"
        "Lucky's sheet is already made, with Lantern Ward in his book. My check casts for other heroes too, with "
        "other spells, only inside the check. Exactly enough is enough, yes?"
    ),
    setup=CAST_SETUP,
    names=["cast", "hero", "spell", "spell_name", "show_mana"],
    pair_talk=(
        "Tell your partner which branch runs for a hero with exactly enough mana, and why. Then each of you writes "
        "the branches on your own screen."
    ),
    starter=CAST_STARTER,
    checkpoints=[
        dict(
            id="skilled-caster-casts",
            text=("A skilled caster with enough mana casts: under comment 3, in place of `pass`, call "
                  "`spell[\"effect\"](hero)`. In step 3 it moves into the last branch."),
            dictated=True,
            hints=[
                "Under comment 3, replace `pass` with the cast.",
                "A function stored in a dictionary is called with brackets on the end: `pack[\"tool\"](sheet)` runs "
                "the function under `\"tool\"`.",
                "Write `spell[\"effect\"](hero)` in place of `pass`, indented inside the function.",
            ],
            checks=[
                cast_check(
                    "a skilled caster with enough mana casts", _CASTS,
                    **_CASTS_MSGS,
                ),
            ],
            pass_line="Lucky: The ward glows. I'd like that in writing.",
        ),
        dict(
            id="bar-updates",
            text=(
                "The mana bar updates after a cast: subtract `spell[\"mana_cost\"]` from `hero[\"mana\"]`, then "
                "call `show_mana(hero)`."
            ),
            dictated=True,
            hints=[
                "Under the cast line, in the same branch. Two more lines: the subtraction, then the bar.",
                "`jar[\"honey\"] = jar[\"honey\"] - 2` reads the old value on the right and stores the new one on the "
                "left.",
                "Write `hero[\"mana\"] = hero[\"mana\"] - spell[\"mana_cost\"]`, then `show_mana(hero)` under it.",
            ],
            checks=[
                cast_check(
                    "the mana bar updates after a cast", _BAR_UPDATES,
                    **_BAR_MSGS,
                ),
            ],
            pass_line="Gearshift: Mana down, bar redrawn. Math checks out.",
        ),
        dict(
            id="too-little-affinity",
            text=(
                "Too little affinity does not cast: if `hero[\"abilities\"][\"magical_affinity\"]` is lower than "
                "`spell[\"required_affinity\"]`, print a message instead."
            ),
            dictated=True,
            hints=[
                "Comment 1 comes first, above the cast. Two keys in a row read the affinity: the outer key, then "
                "the inner key.",
                "`if a < b:` with its line under it, then `else:` with the cast lines under it, each indented one "
                "more step.",
                "The shape, with your three cast lines moved under `else:`, one step deeper:\n"
                "```python\nif ___ < ___:\n    print(...)\nelse:\n    spell[\"effect\"](hero)\n"
                "    hero[\"mana\"] = ...\n    show_mana(hero)\n```\n"
                "Without the indent, Python stops: *expected an indented block*.",
                "Write `if hero[\"abilities\"][\"magical_affinity\"] < spell[\"required_affinity\"]:` with a "
                "`print(...)` under it, then `else:` above the cast lines, and indent the three cast lines one step "
                "under it.",
            ],
            checks=[
                cast_check(
                    "too little affinity does not cast", _TURNS_AWAY,
                    cases=[(6, 15, 5, 7, "low"), (10, 15, 5, 11, "low"), (7, 15, 5, 7, "exact")],
                    typed="Compare with the spell's own `spell[\"required_affinity\"]`, not a typed number.",
                    turn_away=("Turn away a hero whose affinity is lower than the spell's `\"required_affinity\"`. "
                               "Check the sign, and that the cast sits in the last branch, `else`."),
                    exact="Exactly enough affinity should still cast: use `<`, not `<=`.",
                    **_TURN_MSGS,
                ),
            ],
            pass_line="Oogrish: Not skilled enough is a fair answer. Steady, now.",
        ),
        dict(
            id="too-little-mana",
            text=(
                "Too little mana does not cast: otherwise, if `hero[\"mana\"]` is lower than "
                "`spell[\"mana_cost\"]`, print a message instead."
            ),
            dictated=True,
            hints=[
                "Between the affinity test and `else:`. `elif` asks only when the first test was false.",
                "`elif a < b:` sits at the same indent as the `if`, with its own line under it.",
                "Write `elif hero[\"mana\"] < spell[\"mana_cost\"]:` with a `print(...)` under it, above `else:`.",
            ],
            checks=[
                cast_check(
                    "too little mana does not cast", _TURNS_AWAY,
                    cases=[(12, 4, 5, 7, "low"), (12, 7, 8, 7, "low"), (6, 4, 5, 7, "low")],
                    typed="Compare with the spell's own `spell[\"mana_cost\"]`, not a typed number.",
                    turn_away=("Turn away a hero whose mana is lower than the spell's `\"mana_cost\"`. Check the "
                               "sign, and that the cast sits in the last branch, `else`."),
                    exact="Exactly enough mana should still cast.",
                    **_TURN_MSGS,
                ),
            ],
            pass_line="Bomb Shell: No mana, no spell. Fair.",
        ),
        dict(
            id="exactly-enough-mana",
            text="Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Look at the sign in the mana test. A hero with exactly 5 mana and a spell that costs 5 should "
                "still cast.",
                "`<` means *lower than*. `<=` means *lower than or the same*, so it turns away exactly enough.",
                "Write the mana test as `elif hero[\"mana\"] < spell[\"mana_cost\"]:`.",
            ],
            checks=[
                cast_check(
                    "exactly enough mana still casts", _TURNS_AWAY,
                    cases=[(12, 5, 5, 7, "exact"), (12, 8, 8, 7, "exact")],
                    typed="", turn_away="", spend="", tell="", one_msg="", heroes=[], typed_name="", no_else="",
                    exact="Exactly enough mana should still cast: use `<`, not `<=`.",
                ),
            ],
            pass_line="Mar'tu: Exactly enough is enough. The barrier holds.",
        ),
        dict(
            id="own-cost",
            text="The spell's own cost is used, whatever the spell.",
            dictated=False,
            hints=[
                "Look at the subtraction. Each spell has its own cost, on its own page.",
                "Read the cost from the page you have: `page[\"price\"]`, not a number typed in.",
                "Write `hero[\"mana\"] = hero[\"mana\"] - spell[\"mana_cost\"]`.",
            ],
            checks=[
                cast_check(
                    "the spell's own cost is used", _OWN_COST,
                    **_OWN_COST_MSGS,
                ),
            ],
            pass_line="Mar'tu: Get it, compare, act. You held the barrier yourself.",
        ),
    ],
    solution=CAST_SOLUTION,
    partials=[CAST_P1, CAST_P2, CAST_P3, CAST_P4, CAST_P5],
    assemble=dict(
        lines=[line for line in CAST_SOLUTION.splitlines() if line.strip() and not line.strip().startswith("#")],
        distractors=['    if hero["magical_affinity"] < spell["required_affinity"]:',
                     '    elif hero["mana"] <= spell["mana_cost"]:', '        spell["effect"]'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The shape first (more structure)",
            text=(
                "Fill the blanks, then the comments:\n"
                "```python\nif ___ < ___:\n    # not skilled enough\nelif ___ < ___:\n    # not enough mana\n"
                "else:\n    # cast, pay, show\n```\n"
                "Each `___` pair is one read from `hero` and one from `spell`."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "This is `cast_spell` from hold-the-barrier, with our names: `hero` for `caster`, `\"effect\"` for "
                "`\"spell_function\"`, and `print` for `print_prompt`. The same six checks, in the same order."
            ),
        ),
        dict(
            angle="worked twin",
            label="A worked twin: brewing a potion",
            text=(
                "The same shape with other names. Read it, then write yours:\n" + BREW_TWIN
            ),
        ),
        dict(
            angle="picture",
            label="Get it, compare, act",
            text=(
                "```text\nGet it:  spell = the page\nCompare: affinity < need?\n           -> not skilled\n"
                "         mana < cost?\n           -> need mana\nAct:     cast, pay, show\n```"
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE,
        part="hold-the-barrier",
        snippet=(
            "else:\n"
            '    spell["spell_function"](caster)\n'
            '    caster["mana"] = caster["mana"]\n'
            '        - spell["mana_cost"]\n'
            "    show_mana(caster)"
        ),
        why=(
            "These were the last lines of `cast_spell`, split here to fit. Get it, compare, act: you just wrote "
            "all three yourself, and passed the same six checks."
        ),
    ),
    takeaway="Get it, compare, act: `if` / `elif` with `<`, then `spell[\"effect\"](hero)`, pay, `show_mana(hero)`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=CAST_STARTER, fails_at=1, message_contains="Call the spell's effect"),
        dict(why="spell[\"effect\"] with no (hero): nothing happens",
             code=_cast(_cast_body(effect='spell["effect"]')), fails_at=1, message_contains="Add `(hero)`"),
        dict(why="lantern_ward called by name, not the spell's effect",
             code=_cast(_cast_body(effect="lantern_ward(hero)")), fails_at=1, message_contains="by name"),
        dict(why="the effect handed the wrong sheet (lucky, not hero)",
             code=_cast(_cast_body(effect='spell["effect"](lucky)')), fails_at=1, message_contains="uses `lucky`"),
        dict(why="the affinity sign backwards (turns away a skilled caster)",
             code=_cast(_cast_body(aff=AFF_TEST.replace("<", ">"))), fails_at=1, message_contains="Check each sign"),
        dict(why="hero[\"magical_affinity\"]: a skipped level (KeyError)",
             code=_cast(_cast_body(aff='hero["magical_affinity"] < spell["required_affinity"]')), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the campaign's name caster copied", code=_cast(_cast_body(aff=AFF_TEST.replace("hero", "caster"))),
             fails_at=0, message_contains="name 'caster' is not defined"),
        dict(why="CP2 the subtraction never stored", code=_cast(_cast_body(pay='        hero["mana"] - spell["mana_cost"]\n')),
             fails_at=2, message_contains="Store the new mana back"),
        dict(why="CP2 the subtraction kept in a new variable, never stored back",
             code=_cast(_cast_body(pay='        mana = hero["mana"] - spell["mana_cost"]\n')), fails_at=2,
             message_contains="Store the new mana back"),
        dict(why="CP2 show_mana missing", code=_cast(_cast_body(show="")), fails_at=2,
             message_contains="Call `show_mana(hero)`"),
        dict(why="CP2 show_mana before the subtraction",
             code=_cast(_cast_body(pay="        show_mana(hero)\n" + PAY, show="")), fails_at=2,
             message_contains="old mana"),
        dict(why="CP2 show_mana handed the wrong sheet (lucky)",
             code=_cast(_cast_body(show="        show_mana(lucky)\n")), fails_at=2, message_contains="uses `lucky`"),
        dict(why="CP3 <= on the affinity (exactly enough turned away)",
             code=_cast(_cast_body(aff=AFF_TEST.replace("<", "<="))), fails_at=3,
             message_contains="Exactly enough affinity"),
        dict(why="CP3 a typed number for the required affinity",
             code=_cast(_cast_body(aff='hero["abilities"]["magical_affinity"] < 9')), fails_at=3,
             message_contains="not a typed number"),
        dict(why="CP3 two ifs instead of if / elif (the cast still runs after the first message)",
             code=_cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + f"    if {MANA_TEST}:\n" + MANA_MSG + "    else:\n"
                        '        spell["effect"](hero)\n' + PAY + "        show_mana(hero)\n"),
             fails_at=3, message_contains="last branch"),
        dict(why="CP3 no message when turned away",
             code=_cast(_cast_body(skill_msg="        return\n")), fails_at=3, message_contains="Print a message"),
        dict(why="CP3 the if added above the cast lines, no else: the cast lines never moved (the unit's hardest step)",
             code=_cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + '    spell["effect"](hero)\n'
                        '    hero["mana"] = hero["mana"] - spell["mana_cost"]\n    show_mana(hero)\n'),
             fails_at=3, message_contains="Put `else:` above"),
        dict(why="the elif added too, but still no else: the cast lines at function level (caught at CP3)",
             code=_cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + f"    elif {MANA_TEST}:\n" + MANA_MSG
                        + '    spell["effect"](hero)\n'
                        '    hero["mana"] = hero["mana"] - spell["mana_cost"]\n    show_mana(hero)\n'),
             fails_at=3, message_contains="Put `else:` above"),
        dict(why="CP3 else: written, but the cast lines not indented under it (IndentationError)",
             code=_cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + "    else:\n" + '    spell["effect"](hero)\n'
                        '    hero["mana"] = hero["mana"] - spell["mana_cost"]\n    show_mana(hero)\n'),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="CP4 a typed number for the cost in the test",
             code=_cast(_cast_body(mana='hero["mana"] < 6')), fails_at=4, message_contains="not a typed number"),
        dict(why="CP4 the mana test as a second if (two messages)",
             code=_cast(f"    if {AFF_TEST}:\n" + SKILL_MSG + f"    if {MANA_TEST}:\n" + MANA_MSG
                        + f"    if not {MANA_TEST} and not {AFF_TEST}:\n"
                        '        spell["effect"](hero)\n' + PAY + "        show_mana(hero)\n"),
             fails_at=4, message_contains="Use `elif`"),
        dict(why="CP5 <= on the mana (exactly enough turned away; the campaign's own warning)",
             code=_cast(_cast_body(mana='hero["mana"] <= spell["mana_cost"]')), fails_at=5,
             message_contains="use `<`, not `<=`"),
        dict(why="CP6 a typed cost in the subtraction", code=CAST_P5, fails_at=6, message_contains="not a typed 6"),
        dict(why="CP6 the subtraction the wrong way round",
             code=_cast(_cast_body(pay='        hero["mana"] = spell["mana_cost"] - hero["mana"]\n')), fails_at=6,
             message_contains="Put `hero[\"mana\"]` first"),
        dict(why="CP2 the new mana stored in the spell's page (the wrong sheet)",
             code=_cast(_cast_body(pay='        spell["mana_cost"] = hero["mana"] - spell["mana_cost"]\n')), fails_at=2,
             message_contains="stores it in the spell's page"),
        dict(why="CP2 subtracted from max_mana (the wrong key on the right sheet)",
             code=_cast(_cast_body(pay='        hero["mana"] = hero["max_mana"] - spell["mana_cost"]\n')), fails_at=2,
             message_contains="reads `\"max_mana\"`"),
        dict(why="CP4 max_mana read in the mana test (the wrong key)",
             code=_cast(_cast_body(mana='hero["max_mana"] < spell["mana_cost"]')), fails_at=4,
             message_contains="reads `\"max_mana\"`"),
        dict(why="CP3 a typed hero name in the turn-away message (literal values instead of the parameter)",
             code=_cast(_cast_body(skill_msg='        print("Lucky isn\'t skilled enough.")\n')), fails_at=3,
             message_contains="typed name"),
        dict(why="CP4 a typed hero name in the mana message",
             code=_cast(_cast_body(mana_msg='        print("Lucky needs more mana.")\n')), fails_at=4,
             message_contains="typed name"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="dict-nested,elif-chain,boundary,call-stored-func,dict-write",
             solo="false", dictates="1,2,3,4", foreign_names="pack,tool,sheet,jar,honey,page,price,brew,cook,pot,"
                                                              "shelf,skill,herb",
             rehearsal="hold-the-barrier", camp="true", stages="A,Mk", structure="L1",
             subgoals="Get it -> Compare -> Act") + "\n"
        "Rehearsal in campaign mode; the most important exercise for offers. CP1-CP6 are the campaign's six checks "
        "in order. Every check calls the student's cast() with a fresh hero (Brakka) and a fresh spell (Moon Step, "
        "with its own recorder effect), so the student's run of Lucky never has to show a branch. BND: need - 1, "
        "need, exactly enough affinity (CP3); cost above the mana, a typed 6 caught at 7 vs 8, both too low at once "
        "(CP4: one message, so `elif`); exactly enough mana (CP5, the campaign's '<, not <='); costs 3 and 8 (CP6, "
        "a typed 6 or the subtraction reversed). The wrong sheet (`lucky` inside cast) gets its own message on any "
        "failing check, as do `\"max_mana\"` read for the mana, the new mana stored in the spell's page, and a "
        "typed hero name in a turn-away message. More-structure ladder (G3 R15): L1 the starter (numbered comments, default for everyone); "
        "L2 'The shape first' angle (`if ___ < ___:` / `elif ___ < ___:` / `else:`); L3 Assemble it (adaptive "
        "Parsons; distractors: the skipped level, `<=`, the uncalled effect); L4 the worked twin angle (brew), then "
        "retype. A pass below L1 is recorded 'with structure' (site work). Partials p2-p5 use a typed 6 so CP6 is "
        "the last to turn green, as in the campaign.\n"
        "Teacher's revision: CP1's text names comment 3 and `pass` (the last branch does not exist yet) and says "
        "the line moves in step 3. The hardest step is re-indenting the finished cast lines under a new `else:` in "
        "CP3: an `if` (or `if` / `elif`) with no last `else` straight in the function, with the cast still at "
        "function level below it, gets its own message (the hero hears the message, then casts anyway), ahead of "
        "the typed-number and turn-away messages; CP3's ladder has a shape rung in a fence (the three cast lines "
        "one step under `else:`, and the *expected an indented block* warning). The starter opens with "
        "`# show_mana(hero) is already made.`. The worked twin pays with the rehearsal's own long line "
        "(`cook[\"herb\"] = cook[\"herb\"] - pot[\"cost\"]`), not `-=`; it is 49 characters at that indent, so it "
        "sits in a code span under the fence (fenced lines stay within 36 for a phone)."
    ),
)



# ---------------------------------------------------------------------------------------------
# 6C-06 broken-spell-6c (four slips, one checkpoint each)
# ---------------------------------------------------------------------------------------------

BROKEN_FNS = (
    "_wards = []\n"
    "_bars = []\n"
    "\n\n"
    "def lantern_ward(hero):\n"
    "    _wards.append(hero)\n"
    '    print(hero["name"] + "\'s ward glows.")\n'
    "\n\n"
    "def show_mana(hero):\n"
    '    _bars.append((hero, hero["mana"]))\n'
    '    full = "█" * hero["mana"]\n'
    '    empty = "░" * (hero["max_mana"] - hero["mana"])\n'
    '    print(hero["name"] + ": Mana [" + full + empty + "]")\n'
    "\n\n"
)
BROKEN_SETUP = _roster_setup(BROKEN_FNS)
LEARN_DONE = (
    LEARN_SIGNATURE +
    "    spell = {\n"
    '        "mana_cost": mana_cost,\n'
    '        "required_affinity": required_affinity,\n'
    '        "effect": effect,\n'
    "    }\n"
    "    spell_book[spell_name] = spell\n"
)
LOOP_GOOD = 'learn_spell(hero["spell_book"], "Lantern Ward", 6, 9, lantern_ward)'
LOOP_BAD = 'learn_spell(hero["spell_book"], "Lantern Ward", 6, 9, lantern_ward(hero))'
EFFECT_GOOD = 'spell["effect"](hero)'
EFFECT_BAD = 'spell["effect"]'
MANA_GOOD = 'hero["mana"] < spell["mana_cost"]'
MANA_BAD = 'hero["mana"] <= spell["mana_cost"]'
PAY_GOOD = 'hero["mana"] = hero["mana"] - spell["mana_cost"]'
PAY_BAD = 'hero["mana"] - spell["mana_cost"]'


def _broken(loop=LOOP_BAD, effect=EFFECT_BAD, mana=MANA_BAD, pay=PAY_BAD):
    return (
        LEARN_DONE + "\n\n"
        "def cast(hero, spell_name):\n"
        '    if spell_name not in hero["spell_book"]:\n'
        '        print(hero["name"], "doesn\'t know", spell_name)\n'
        "        return\n"
        '    spell = hero["spell_book"][spell_name]\n'
        f"    if {AFF_TEST}:\n" + SKILL_MSG +
        f"    elif {mana}:\n" + MANA_MSG +
        "    else:\n"
        f"        {effect}\n"
        f"        {pay}\n"
        "        show_mana(hero)\n"
        "\n\n"
        "for hero in roster:\n"
        f"    {loop}\n"
        "\n"
        'cast(lucky, "Lantern Ward")\n'
    )


BROKEN_STARTER = _broken()
BROKEN_SOLUTION = _broken(LOOP_GOOD, EFFECT_GOOD, MANA_GOOD, PAY_GOOD)

_BOOKS_HOLD_WARD = r'''
assert type(_g.get('roster')).__name__ == 'list' and len(roster) == 4, __KEEP_ROSTER__
_loops = [_s for _s in _tree().body if type(_s).__name__ == 'For']
assert [_c for _s in _loops for _c in _ast.walk(_s) if _is_call(_c, 'learn_spell')], __LOOP_CALL__
for _h in roster:
    _pg = _h.get('spell_book', {}).get('Lantern Ward') if type(_h).__name__ == 'dict' else None
    assert type(_pg).__name__ == 'dict', __MISSING__
    _ef = _pg.get('effect')
    if _ef is not _g.get('lantern_ward'):
        assert not (_ef is None and _g.get('_wards')), __CALLED_NOW__ + ' ' + _ev(
            'looked in ' + _h.get('name', 'a hero') + "'s book", 'the effect was `None`')
        assert type(_ef).__name__ != 'str', __TEXT__ + ' ' + _QUOTES
        assert False, __EFFECT__
'''


def broken_check(label, body, **messages):
    return (label, sx(BROKEN_SETUP) + fill(_CAST_PRE, **_CAST_KEEP) + fill(body, **messages))


BROKEN_SPELL_6C = dict(
    id="broken-spell-6c",
    title="Broken spell",
    martu=(
        "Bomb Shell copied the spell book and the barrier from memory. Four slips. The latch hates him.\n"
        "Some slips are loud: Python stops and names a line. Some are quiet: the program runs and does the wrong "
        "thing. Watch the first lines on screen. The wards glow before anyone casts. That is a clue, yes?\n"
        "Mend one slip, then Run again. My check casts for other heroes too, only inside the check."
    ),
    setup=BROKEN_SETUP,
    names=["learn_spell", "lantern_ward", "cast", "spell", "hero"],
    pair_talk=(
        "Tell your partner which slip was quiet and which was loud, and how you spotted each one. Each of you "
        "mends your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="hand-over-the-ward",
            text="Mend the loop at the bottom, so every hero's book holds the ward itself.",
            dictated=False,
            hints=[
                "Look at the first lines on screen: the wards glow while the books are being written. Which line "
                "runs `lantern_ward` that early?",
                "`lantern_ward` is the function itself. `lantern_ward(hero)` runs it now and hands over what it "
                "gives back, `None`.",
                "Write the loop's line as `learn_spell(hero[\"spell_book\"], \"Lantern Ward\", 6, 9, lantern_ward)`.",
            ],
            checks=[
                (
                    "every book holds lantern_ward itself",
                    sx(BROKEN_SETUP) + fill(
                        _BOOKS_HOLD_WARD,
                        keep_roster="Keep `roster` as it is: four hero sheets, each with its spell book.",
                        loop_call=("Keep the loop's call to `learn_spell`, and mend only what it hands over. Your "
                                   "loop no longer calls `learn_spell`."),
                        missing="Keep the loop at the bottom, so every hero learns Lantern Ward.",
                        called_now=("Hand over `lantern_ward` itself, with no `()`. `lantern_ward(hero)` ran the ward "
                                    "while the books were being written (the first lines on screen), and stored "
                                    "`None`."),
                        text="Hand over the function, `lantern_ward`, with no quotes.",
                        effect="Hand over `lantern_ward` itself in the loop.",
                    ),
                ),
            ],
        ),
        dict(
            id="call-the-effect",
            text="Mend the cast line, so the spell's effect really runs.",
            dictated=False,
            hints=[
                "Look at the first line under `else:`. Does anything call the spell?",
                "A function stored in a dictionary runs only with brackets on the end: `pack[\"tool\"](sheet)`.",
                "Write `spell[\"effect\"](hero)` as the first line under `else:`.",
            ],
            checks=[
                broken_check(
                    "a skilled caster with enough mana casts", _CASTS,
                    bare=("Add `(hero)` on the end: `spell[\"effect\"]` on its own reads the function but doesn't "
                          "call it. The brackets on the end are what call it."),
                    by_name=("Call the spell's own effect, `spell[\"effect\"](hero)`. Your line calls "
                             "`lantern_ward` by name, so every spell would cast Lantern Ward."),
                    refused="Let a skilled caster with enough mana cast. Check each sign: `<` means *lower than*.",
                    cast="Call the spell's effect in the last branch: `spell[\"effect\"](hero)`.",
                    once="Call the effect once per cast.",
                    hero="Hand the caster to the effect, `spell[\"effect\"](hero)`: your line handed over another "
                         "sheet.",
                ),
            ],
        ),
        dict(
            id="exactly-enough",
            text="Mend the mana test, so exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Look at the sign in the `elif` line. A hero with 5 mana and a cost of 5 should still cast.",
                "`<=` means *lower than or the same*. `<` means *lower than*.",
                "Write the mana test as `elif hero[\"mana\"] < spell[\"mana_cost\"]:`.",
            ],
            checks=[
                broken_check(
                    "exactly enough mana casts, and too little is turned away", _TURNS_AWAY,
                    cases=[(12, 5, 5, 7, "exact"), (12, 8, 8, 7, "exact"), (12, 4, 5, 7, "low"),
                           (12, 7, 8, 7, "low")],
                    typed="Compare with the spell's own `spell[\"mana_cost\"]`, not a typed number.",
                    turn_away=("Keep turning away a hero whose mana is lower than the spell's `\"mana_cost\"`: "
                               "mend only the sign, `<=` to `<`."),
                    exact="Exactly enough mana should still cast: use `<`, not `<=`.",
                    **_TURN_MSGS,
                ),
            ],
        ),
        dict(
            id="store-the-new-mana",
            text="Mend the subtraction, so the mana really goes down.",
            dictated=False,
            hints=[
                "Look at the line under the cast. It works out the new mana. Where does that number go?",
                "`jar[\"honey\"] - 2` works out a number and forgets it. `jar[\"honey\"] = jar[\"honey\"] - 2` stores it "
                "back.",
                "Write `hero[\"mana\"] = hero[\"mana\"] - spell[\"mana_cost\"]` in place of that line.",
            ],
            checks=[
                broken_check(
                    "the mana goes down and the bar shows it", _BAR_UPDATES,
                    store_back=("Store the new mana back in the sheet: `hero[\"mana\"] = hero[\"mana\"] - "
                                "spell[\"mana_cost\"]`. The subtraction on its own works the number out, then "
                                "forgets it."),
                    into_spell=("Store the new mana in the hero's sheet, `hero[\"mana\"] = ...`. Your line stores "
                                "it in the spell's page, so the hero still has all their mana."),
                    subtract="Subtract the spell's cost from `hero[\"mana\"]`, after the cast.",
                    show="Keep `show_mana(hero)` after the subtraction, so the bar updates.",
                    show_hero="Hand `show_mana` the caster, `hero`.",
                    show_after="Keep `show_mana(hero)` after the subtraction: the bar showed the old mana.",
                ),
                broken_check(
                    "the spell's own cost is used", _OWN_COST,
                    typed_cost="Subtract the spell's own cost, `spell[\"mana_cost\"]`, not a typed 6.",
                    reversed="Put `hero[\"mana\"]` first: the mana minus the cost.",
                    own="Subtract the spell's own cost, `spell[\"mana_cost\"]`.",
                ),
            ],
            pass_line="Bomb Shell: That latch hates me. This spell doesn't. Works.",
        ),
    ],
    solution=BROKEN_SOLUTION,
    partials=[
        _broken(LOOP_GOOD),
        _broken(LOOP_GOOD, EFFECT_GOOD),
        _broken(LOOP_GOOD, EFFECT_GOOD, MANA_GOOD),
    ],
    assemble=dict(
        lines=[line for line in BROKEN_SOLUTION.splitlines() if line.strip()],
        distractors=["    " + LOOP_BAD, "        " + EFFECT_BAD, "    elif " + MANA_BAD + ":"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="One slip at a time",
            text=(
                "1. Run. Read the screen: what happened, and in what order?\n"
                "2. A message from Python? Read its last line, then the line it names.\n"
                "3. No message? Compare what you see with what should happen. The check says what is left.\n"
                "4. Mend one slip, then Run again."
            ),
        ),
        dict(
            angle="picture",
            label="Loud and quiet",
            text=(
                "```text\nlantern_ward(hero)\n  quiet: glows too early,\n  stores None\nspell[\"effect\"]\n"
                "  quiet: nothing is cast\n  (mend it first? then\n  it goes loud: NoneType)\n<=\n"
                "  quiet: exactly enough\n  is turned away\nhero[\"mana\"] - cost\n  quiet: worked out,\n"
                "  then forgotten\n```"
            ),
        ),
        dict(
            angle="shorter",
            text="Hand over without `()`. Call with `()`. `<`, not `<=`. Store the new mana back.",
        ),
    ],
    takeaway="Quiet slips: `f(hero)` handed over, `spell[\"effect\"]` uncalled, `<=`, a subtraction never stored.",
    wrong_answers=[
        dict(why="the starter (the ward handed over as None)", code=BROKEN_STARTER, fails_at=1,
             message_contains="no `()`"),
        dict(why="the effect called first while the loop still hands over None (the chain: NoneType)",
             code=_broken(effect=EFFECT_GOOD), fails_at=0, message_contains="'NoneType' object is not callable"),
        dict(why="the loop mended with the name in quotes",
             code=_broken(LOOP_GOOD.replace("lantern_ward)", '"lantern_ward")')), fails_at=1,
             message_contains="no quotes"),
        dict(why="CP2 lantern_ward called by name in the cast",
             code=_broken(LOOP_GOOD, "lantern_ward(hero)"), fails_at=2, message_contains="by name"),
        dict(why="CP2 the effect handed Lucky's sheet (wrong sheet)",
             code=_broken(LOOP_GOOD, 'spell["effect"](lucky)'), fails_at=2, message_contains="uses `lucky`"),
        dict(why="CP3 the sign flipped the wrong way (> turns away a caster with plenty)",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, 'hero["mana"] > spell["mana_cost"]'), fails_at=2,
             message_contains="Check each sign"),
        dict(why="CP4 the subtraction kept in a new variable",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, MANA_GOOD, 'mana = hero["mana"] - spell["mana_cost"]'),
             fails_at=4, message_contains="Store the new mana back"),
        dict(why="CP4 a typed cost", code=_broken(LOOP_GOOD, EFFECT_GOOD, MANA_GOOD, 'hero["mana"] = hero["mana"] - 6'),
             fails_at=4, message_contains="not a typed 6"),
        dict(why="CP3 the mana test switched off (elif False): exactly enough casts, but so does too little",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, "False"), fails_at=3, message_contains="mend only the sign"),
        dict(why="CP3 a typed cost in the mana test",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, 'hero["mana"] < 5'), fails_at=3,
             message_contains="not a typed number"),
        dict(why="CP3 max_mana read in the mana test",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, 'hero["max_mana"] < spell["mana_cost"]'), fails_at=3,
             message_contains="reads `\"max_mana\"`"),
        dict(why="CP4 the new mana stored in the spell's page",
             code=_broken(LOOP_GOOD, EFFECT_GOOD, MANA_GOOD, 'spell["mana_cost"] = hero["mana"] - spell["mana_cost"]'),
             fails_at=4, message_contains="stores it in the spell's page"),
        dict(why="CP1 the loop rewritten to skip learn_spell",
             code=BROKEN_SOLUTION.replace("    " + LOOP_GOOD, '    hero["spell_book"]["Lantern Ward"] = '
                                          '{"mana_cost": 6, "required_affinity": 9, "effect": lantern_ward}'),
             fails_at=1, message_contains="no longer calls"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="func-as-value,call-stored-func,boundary,dict-write",
             solo="false", dictates="", foreign_names="pack,tool,sheet,jar,honey", stages="D") + "\n"
        "Four bugs, one checkpoint each (the spec's list). Order: the loop's `lantern_ward(hero)` comes first, "
        "then the uncalled `spell[\"effect\"]`, then `<=`, then the unstored subtraction. Reason: with the "
        "spec's order the first mend (calling the effect) makes the program crash on the stored `None` before any "
        "check can run, so partial 1 could never pass checkpoint 1. In this order every partial passes 1..k; a "
        "student who mends the call first still meets the chain (a wrong answer proves the NoneType crash), "
        "which points them at the loop. All four slips are quiet: the checks cast for a fresh hero and a fresh "
        "spell (the same _CAST_PRE as 6C-05), so the student's run of Lucky does not have to show them. CP3 also "
        "casts with too little mana, so switching the test off (`elif False:`), a typed cost or `\"max_mana\"` "
        "cannot pass for the mended sign. CP1: the loop must still call `learn_spell`."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6C-S solo-6c (SOLO make-twin, done alone)
# ---------------------------------------------------------------------------------------------

SHOUT_DEF = 'def shout(hero):\n    print(hero["name"], "shouts!")\n'
SOLO_COMMENT = (
    "# 1. Make a dictionary called roar,\n"
    '#    with the key "effect" holding\n'
    "#    the function shout.\n"
    "# 2. Call shout from roar, on lucky.\n"
)


def _solo(lines=""):
    return SHOUT_DEF + "\n\n" + LUCKY_SMALL + "\n" + SOLO_COMMENT + lines


SOLO_STARTER = _solo()
SOLO_SOLUTION = _solo('roar = {"effect": shout}\nroar["effect"](lucky)\n')

_SOLO_HOLDS = r'''
assert 'roar' in _g, __NO_ROAR__
_r = roar
assert type(_r).__name__ == 'dict', __NOT_DICT__
if 'effect' not in _r:
    _x = [_k for _k in _r if _near(_k, 'effect')]
    assert not _x, '`roar` has the key ' + _lit((_x or [''])[0]) + ', not `"effect"`, letter for letter.'
    assert False, __NO_KEY__
_v = _r['effect']
if _v is not _g.get('shout'):
    assert _v is not None, __NONE__
    assert type(_v).__name__ != 'str', __TEXT__ + ' ' + _QUOTES
    assert False, __OTHER__
'''

_SOLO_CALLS = r'''
assert not _printed_call(lambda _c: type(_c.func).__name__ == 'Subscript'), __PRINTED__
_ns, _ls, _err, _miss = _rerun([('shout', _wrap('shout', '_slog')),
                                ('*roar', _stand_in('_other') + 'roar["effect"] = _fx\n')])
assert not _err, _stop(_err, 'ran your program again')
_o = _ns.get('_other', [])
if not _o:
    _bare = [_s for _s in _top() if type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Subscript']
    assert not _bare, __BARE__
    assert not _ns.get('_slog'), __BY_NAME__ + ' ' + _ev('put another effect in `roar`', 'it never ran')
    assert False, __CALL__
assert len(_o) == 1, __ONCE__
assert _o[0] is _ns.get('lucky'), __LUCKY__
'''

SOLO_6C = dict(
    id="solo-6c",
    title="Show Mar'tu",
    martu="A short one, just for you. Put a recipe in a box, then cook it from there.",
    solo=True,
    explainer="lean",
    names=["roar", "shout", "lucky"],
    starter=SOLO_STARTER,
    checkpoints=[
        dict(
            id="store-and-call",
            text="Store `shout` in a dictionary called `roar`, under the key `\"effect\"`. Then call it from "
                 "`roar` on `lucky`.",
            dictated=False,
            hints=[
                "Two lines. The dictionary first, then the call.",
                "The function goes in with no `()`. The call reads it by its key, then adds brackets.",
                "`tune = {\"play\": hum}` keeps `hum` in a box, no `()`. `tune[\"play\"](moth)` cooks it.",
                "In the lesson: `glow[\"effect\"](lucky)` cast Glow from its dictionary.",
            ],
            checks=[
                chk(
                    "roar holds shout itself", _SOLO_HOLDS,
                    no_roar="No dictionary called `roar` is made yet.",
                    not_dict="`roar` is not a dictionary.",
                    no_key="`roar` has no key `\"effect\"`.",
                    none=("`roar[\"effect\"]` holds `None`: the `()` after `shout` ran it right away, and the "
                          "dictionary kept what it handed back."),
                    text="`roar[\"effect\"]` holds text: `shout` is in quotes.",
                    other="`roar[\"effect\"]` holds something other than the function `shout`.",
                ),
                chk(
                    "shout runs once, from roar, on lucky", _SOLO_CALLS,
                    printed="A `print(...)` wraps the call, so it shows an extra `None`.",
                    bare="`roar[\"effect\"]` sits on a line by itself: it reads the function, and nothing calls it.",
                    by_name="`shout` is called by its own name, not from `roar`.",
                    call="Nothing calls the function from `roar` yet.",
                    once="The function runs more than once.",
                    lucky="The call hands over something other than `lucky`.",
                ),
            ],
            pass_line="Mar'tu: You did that alone. I saw. On your map: ✓ a function kept in a dictionary, then called "
                      "from it.",
        ),
    ],
    solution=SOLO_SOLUTION,
    another_way=[
        dict(angle="step-by-step", text="1. A dictionary with the function as a value, no `()`. 2. The key, then "
                                        "the brackets."),
        dict(angle="shorter", text="Box it, then cook it: `roar[\"effect\"](lucky)`."),
    ],
    takeaway="On your own: a function stored in a dictionary, then called from it.",
    wrong_answers=[
        dict(why="the starter (nothing made)", code=SOLO_STARTER, fails_at=1,
             message_contains="No dictionary called `roar` is made yet."),
        dict(why="stored the call: shout(lucky) puts None in the dict, then the call crashes",
             code=_solo('roar = {"effect": shout(lucky)}\nroar["effect"](lucky)\n'), fails_at=0,
             message_contains="'NoneType' object is not callable"),
        dict(why="stored the call, no call yet (NOP)", code=_solo('roar = {"effect": shout(lucky)}\n'), fails_at=1,
             message_contains="holds `None`"),
        dict(why="the function's name in quotes, no call yet", code=_solo('roar = {"effect": "shout"}\n'),
             fails_at=1, message_contains="in quotes"),
        dict(why="a near-miss key", code=_solo('roar = {"Effect": shout}\nroar["Effect"](lucky)\n'), fails_at=1,
             message_contains="letter for letter"),
        dict(why="no (lucky): read, never called", code=_solo('roar = {"effect": shout}\nroar["effect"]\n'),
             fails_at=1, message_contains="nothing calls it"),
        dict(why="called by its own name", code=_solo('roar = {"effect": shout}\nshout(lucky)\n'), fails_at=1,
             message_contains="by its own name"),
        dict(why="print around the call", code=_solo('roar = {"effect": shout}\nprint(roar["effect"](lucky))\n'),
             fails_at=1, message_contains="extra `None`"),
        dict(why="stored the result of a call into the dict afterwards (roar[\"effect\"] = shout(lucky))",
             code=_solo('roar = {}\nroar["effect"] = shout(lucky)\n'), fails_at=1, message_contains="holds `None`"),
        dict(why="a typed line instead of a call from roar",
             code=_solo('roar = {"effect": shout}\nprint("Lucky shouts!")\n'), fails_at=1,
             message_contains="Nothing calls"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="func-as-value,call-stored-func", solo="true", dictates="",
             foreign_names="glow,tune,play,hum,moth", seat_b="hand `shout` to a given `cast_on_everyone(heroes, effect)` with "
                                          "`roster` (CALL x 4, NOP)") + "\n"
        "SOLO make-twin. Seat A (and anyone solo) stores `shout` in `roar` and calls it from there; seat B would "
        "hand `shout` to `cast_on_everyone` once pair mode ships (6C-02's checks, renamed). Recorded, never "
        "blocking, never shown to a partner. explainer='lean' (from Unit 2 on, SOLO items and Quick Checks): the "
        "messages name the slip and keep the evidence, without the finished line; no hint holds the line either. "
        "Teacher's revision: the first check asks for `roar` by name (a lean 'No dictionary called `roar` is made "
        "yet.' in place of Python's NameError); a Teach rung uses 6C-03's Example names (`tune`, `hum`, `moth`); "
        "the pass line names the skill on the map. The starter stays blank under the comments."
    ),
)

LESSON_6C = dict(
    kind="lesson",
    id="spells-you-can-hand-over",
    title="Spells You Can Hand Over",
    minutes=38,
    summary=(
        "Store a function in a variable, hand it over with no `()`, keep it in a dictionary, then write the spell "
        "book and cast from it."
    ),
    notes=(
        "Lesson 6C (CC; 6C-06 SC). Preceded by 6c-remembers. Exactly one SOLO (solo-6c, explainer='lean'). "
        "Non-dictated checkpoints: 6C-02 CP2, 6C-03 CP2, 6C-05 CP5-CP6, 6C-06, 6C-S. Dictated: 6C-01, 6C-02 CP1, "
        "6C-03 CP1, 6C-04 CP1-CP2, 6C-05 CP1-CP4. Minutes 37 -> 38 (teacher's revision): 6C-03 gains a one-line "
        "step, `lucky_book[\"Glow\"][\"effect\"](lucky)`, the `book[name][\"effect\"](hero)` form unit goal 7 names "
        "and Quick Check C4 needs, which no other lesson step has the student write. Mar'tu moment: 6C-01 'the box holds the recipe' (teacher-led). Campaign "
        "rehearsals in campaign mode: 6C-04 (spell-book) and 6C-05 (hold-the-barrier). Skill gates: 6C-01 "
        "pattern:FuncValue, 6C-03 pattern:CallOnSubscript. Introduces const:None (6C-04)."
    ),
    exercises=[NAME_WITHOUT_PARENTHESES, HAND_IT_OVER, RECIPE_IN_A_BOX, WRITE_THE_SPELL_BOOK, CAST_FROM_THE_BOOK,
               BROKEN_SPELL_6C, SOLO_6C],
)


# =============================================================================================
# Quiz 6B
# =============================================================================================

QUIZ_6B = dict(
    kind="quiz",
    id="spell-recipes-quiz",
    title="Spell Recipes Quiz",
    minutes=8,
    summary="Eight questions on functions as values, changing a sheet, early returns and the spell book.",
    notes=(
        "Quiz 6B (CC, retrieval), the spec's eight in order: 3 predict, 2 mc, 2 parsons, 1 bug. Def/return items: "
        "#3, #6, #7, #8 (every unit quiz from Unit 4 on carries one). Distractors come from this unit's slips: "
        "`warm_hands()` and the quoted name (#2), 'the caller's sheet is unchanged' (#3), `<=` and the uncalled "
        "`spell[\"effect\"]` (#4), the quoted key, the quoted parameter and the rebinding (#5), "
        "`return` read as 'hands back the last value' or 'does nothing' (#7, #8)."
    ),
    questions=[
        dict(
            type="predict",
            id="call-from-the-dictionary",
            q="What will this print?",
            code=(
                "def glow(name):\n"
                '    return name + " glows."\n'
                "\n\n"
                'spells = {"glow": glow}\n'
                'print(spells["glow"]("Lucky"))\n'
            ),
            choices=["Lucky glows.", "None", "glow", "an error"],
            answer="Lucky glows.",
            explain=(
                "`spells[\"glow\"]` is the function `glow`, read from the dictionary. `(\"Lucky\")` calls it, and it "
                "returns `\"Lucky glows.\"`. The `print` shows what came back."
            ),
            notes="call-stored-func (Obj 7). 'an error' is 'you can't call from a dictionary'.",
        ),
        dict(
            type="mc",
            id="hand-it-over-without-running",
            q="Which line hands over the function without running it?",
            code=(
                "def cast_on_everyone(heroes, effect):\n"
                "    for hero in heroes:\n"
                "        effect(hero)\n"
            ),
            choices=[
                "cast_on_everyone(roster, warm_hands)",
                "cast_on_everyone(roster, warm_hands())",
                'cast_on_everyone(roster, "warm_hands")',
            ],
            answer=0,
            why_wrong={
                1: "With `()`, `warm_hands` runs right now, before `cast_on_everyone` starts. It has no hero yet, so "
                   "Python stops: a positional argument is missing.",
                2: "In quotes it is just text. `cast_on_everyone` would try to call the text, and Python stops: "
                   "`'str' object is not callable`.",
            },
            explain=(
                "The name with no `()` is the function itself. `cast_on_everyone` calls it later, once for each "
                "hero, with `effect(hero)`."
            ),
            notes="func-as-value (Obj 7): the class's slip, passing a function WITH ().",
        ),
        dict(
            type="predict",
            id="the-caller-sees-the-change",
            q="What will this print?",
            code=(
                "def spend(hero, cost):\n"
                '    left = hero["mana"] - cost\n'
                '    hero["mana"] = left\n'
                "\n\n"
                'lucky = {"mana": 26}\n'
                "spend(lucky, 3)\n"
                'print(lucky["mana"])\n'
            ),
            choices=["23", "26", "None", "an error"],
            answer="23",
            explain=(
                "`hero` and `lucky` are two labels on the same sheet. The change inside the function reaches the "
                "caller: 26 - 3 = 23. No `return` is needed for that."
            ),
            notes="func-takes-dict (Obj 2): 26 is 'the caller's sheet is unchanged'; None is 'no return, no change'.",
        ),
        dict(
            type="parsons",
            id="cast-body",
            q=("Put the lines in order (with their indents). Lucky has exactly enough mana to cast Glow, and "
               "Moss does not."),
            lines=[
                "def ward(hero):",
                '    print(hero["name"], "is safe.")',
                "def cast(hero, spell):",
                '    if hero["mana"] < spell["cost"]:',
                '        print("No:", hero["name"])',
                "    else:",
                '        spell["effect"](hero)',
                'lucky = {"name": "Lucky", "mana": 6}',
                'moss = {"name": "Moss", "mana": 3}',
                'glow = {"cost": 6, "effect": ward}',
                "cast(lucky, glow)",
                "cast(moss, glow)",
            ],
            distractors=['    if hero["mana"] <= spell["cost"]:', '        spell["effect"]'],
            expected_output="Lucky is safe.\nNo: Moss",
            explain=(
                "`<` lets exactly enough mana cast: 6 is not lower than 6, so Lucky is safe. Moss has 3, which is "
                "lower, so the `if` turns Moss away. In the `else`, `spell[\"effect\"](hero)` reads the function "
                "from the dictionary and calls it. Without `(hero)`, nothing would happen."
            ),
            notes="boundary + call-stored-func (Obj 7, the hold-the-barrier shape). Distractors: `<=`, the uncalled "
                  "effect. Two casters, so both branches must print: the site grades a reordered answer by its "
                  "output, and with one caster a board that skipped the if/else lines still printed the right line.",
        ),
        dict(
            type="parsons",
            id="learn-spell",
            q="Put the lines in order (with their indents). `learn_spell` builds a spell and stores it by name.",
            lines=[
                "def learn_spell(book, name, cost):",
                '    spell = {"mana_cost": cost}',
                "    book[name] = spell",
                "pages = {}",
                'learn_spell(pages, "Glow", 2)',
                "print(pages)",
            ],
            distractors=['    book["name"] = spell', '    spell = {"mana_cost": "cost"}', "    book = {name: spell}"],
            expected_output="{'Glow': {'mana_cost': 2}}",
            explain=(
                "The value is the parameter `cost`, with no quotes. The key is the parameter `name`, with no quotes. "
                "`book[name] = spell` changes the book handed in; `book = {...}` would only make a new one inside."
            ),
            notes="dict-from-params + store-by-name (Obj 3). Distractors: the quoted key, the quoted parameter, the "
                  "rebinding that the caller never sees.",
        ),
        dict(
            type="bug",
            id="bar-brackets",
            q="This program stops with a TypeError. Mend it so it prints 3 full blocks, then 2 empty ones.",
            code=(
                "def get_bar(mana, max_mana):\n"
                '    full = "█" * mana\n'
                '    empty = "░" * max_mana - mana\n'
                "    return full + empty\n"
                "\n\n"
                "print(get_bar(3, 5))\n"
            ),
            fix=(
                "def get_bar(mana, max_mana):\n"
                '    full = "█" * mana\n'
                '    empty = "░" * (max_mana - mana)\n'
                "    return full + empty\n"
                "\n\n"
                "print(get_bar(3, 5))\n"
            ),
            expected_output="███░░",
            explain=(
                "Python does `*` before `-`. Without brackets it makes five blocks, then tries to take a number away "
                "from text, and stops. Brackets make it subtract first: `\"░\" * (max_mana - mana)`."
            ),
            notes="repeat-string precedence (Obj 6, the mana bar), as a def/return item.",
        ),
        dict(
            type="mc",
            id="return-with-nothing",
            q="What does the `return` on line 3 do, with nothing after it?",
            code=(
                "def warn(hero):\n"
                '    if hero["mana"] > 5:\n'
                "        return\n"
                '    print(hero["name"], "is low.")\n'
            ),
            choices=[
                "It ends the function right there. The caller gets `None`.",
                "It returns the hero's mana.",
                "It goes back to the top of the function.",
                "Nothing: the next line still runs.",
            ],
            answer=0,
            why_wrong={
                1: "A `return` with nothing after it returns nothing: `None`. To return the mana, it would need "
                   "`return hero[\"mana\"]`.",
                2: "`return` never loops. It leaves the function.",
                3: "The function stops at `return`. The `print` below it runs only when the `if` was false.",
            },
            explain="`return` ends the function at once. With nothing after it, the caller gets `None`. That is how "
                    "an early-return guard works.",
            notes="early-return (Obj 4) and none-return.",
        ),
        dict(
            type="predict",
            id="the-guard",
            q="What will this print?",
            code=(
                "def cast(book, name):\n"
                "    if name not in book:\n"
                '        print("Unknown:", name)\n'
                "        return\n"
                '    print("Casting", name)\n'
                "\n\n"
                'book = {"Glow": 2}\n'
                'cast(book, "Mist")\n'
                'cast(book, "Glow")\n'
            ),
            choices=[
                "Unknown: Mist\nCasting Glow",
                "Unknown: Mist\nCasting Mist\nCasting Glow",
                "Unknown: Mist",
                "Casting Mist\nCasting Glow",
            ],
            answer="Unknown: Mist\nCasting Glow",
            explain=(
                "Mist is not in the book, so the guard prints `Unknown: Mist` and `return` ends that call. The "
                "second call knows Glow, so it goes past the guard: `Casting Glow`."
            ),
            notes="early-return (Obj 4): the second choice forgets the return; the third thinks return ends the "
                  "whole program; the fourth skips the guard.",
        ),
    ],
)


# =============================================================================================
# Project 6P "The Resonance Array" (campaign mode; Lucky's side quest: a dictionary of dials)
# =============================================================================================

ARRAY_SETUP = "".join(f'{var} = {{"name": "{name}", "magical_affinity": {aff}, "die_size": {die}}}\n'
                      for var, name, _, aff, die in PARTY)
ARRAY_SETUP += "roster = [oogrish, gearshift, bomb_shell, lucky]\n"

MANA_DIAL = (
    "def mana_dial(hero):\n"
    '    aff = hero["magical_affinity"]\n'
    "    mana = max_mana_for(aff)\n"
    '    name = hero["name"]\n'
    '    return name + ": " + str(mana)\n'
)
DAMAGE_DIAL = (
    "def damage_dial(hero):\n"
    '    die = hero["die_size"]\n'
    "    damage = average_damage(die)\n"
    '    name = hero["name"]\n'
    '    return name + ": " + str(damage)\n'
)
DIAL_MAX = "    return affinity * 2\n"
DIAL_AVG = "    return (1 + die_size) / 2\n"
DIAL_GAP = "    return last_gap - shrink\n"
DIAL_CAL = (
    "    return {\n"
    '        "max_mana": max_mana_for(hero["magical_affinity"]),\n'
    '        "average_damage": average_damage(hero["die_size"]),\n'
    "    }\n"
)
DIAL_RUN = "    for hero in heroes:\n        print(dial(hero))\n"
DIAL_CALL = "run_array(roster, mana_dial)\n"


CAL_ZEROS = (
    "    return {\n"
    '        "max_mana": 0,\n'
    '        "average_damage": 0,\n'
    "    }\n"
)


def _array(mx="    return 0\n", avg="    return 0\n", gap="    return 0\n", cal=CAL_ZEROS,
           run="    pass\n", call="", mana_dial=MANA_DIAL, damage_dial=DAMAGE_DIAL):
    return (
        "# The Resonance Array\n"
        "# roster holds four hero sheets,\n"
        '# each with "name",\n'
        '# "magical_affinity" and "die_size".\n'
        "\n"
        "# A. Dials\n"
        "# 1. max_mana_for(affinity) returns\n"
        "#    twice the affinity.\n"
        "def max_mana_for(affinity):\n" + mx + "\n\n"
        "# 2. average_damage(die_size)\n"
        "#    returns (1 + die_size) / 2.\n"
        "def average_damage(die_size):\n" + avg + "\n\n"
        "# 3. next_gap(last_gap, shrink)\n"
        "#    returns the next gap on the\n"
        "#    chalk wall: the last gap\n"
        "#    minus the shrink.\n"
        "def next_gap(last_gap, shrink):\n" + gap + "\n\n"
        "# B. Calibrate\n"
        "# 4. calibrate(hero) returns a\n"
        "#    dictionary with two keys,\n"
        '#    "max_mana" and\n'
        '#    "average_damage". Build each\n'
        "#    value by calling its dial on\n"
        "#    the hero's own sheet.\n"
        "#    Replace each 0 with a call to\n"
        "#    its dial.\n"
        "def calibrate(hero):\n" + cal + "\n\n"
        "# C. Run the array\n"
        "# These two dials are finished.\n"
        "# Leave them as they are.\n" + mana_dial + "\n\n" + damage_dial + "\n\n"
        "# 5. run_array(heroes, dial) prints\n"
        "#    dial(hero) for each hero.\n"
        "def run_array(heroes, dial):\n" + run + "\n\n"
        "# 6. Call run_array with roster\n"
        "#    and mana_dial, no ().\n" + call
    )


ARRAY_STARTER = _array()
ARRAY_SOLUTION = _array(DIAL_MAX, DIAL_AVG, DIAL_GAP, DIAL_CAL, DIAL_RUN, DIAL_CALL)
_ARRAY_DONE = [DIAL_MAX, DIAL_AVG, DIAL_GAP, DIAL_CAL, DIAL_RUN]


def _array_upto(k, **overrides):
    """The array with the first k tasks done (the rest still placeholders), then any overrides."""
    keys = ["mx", "avg", "gap", "cal", "run"]
    fields = {key: _ARRAY_DONE[i] for i, key in enumerate(keys[:k])}
    fields.update(overrides)
    return _array(**fields)


_DIAL = r'''
_name, _cases, _slips = __NAME__, __CASES__, __SLIPS__
_fd = _need_def(_name, len(_cases[0][0]), __SIG__)
def _c(_args):
    return '`' + _name + '(' + ', '.join(str(_a) for _a in _args) + ')`'
_seen = []
_ps = [_a.arg for _a in _fd.args.args]
for _args, _want in _cases:
    _val, _ls, _err = _quiet(_g[_name], *_args)
    if type(_err).__name__ == 'NameError':
        assert False, ("Use this dial's own " + ('parameters ' if len(_ps) > 1 else 'parameter ')
                       + ' and '.join('`' + _p + '`' for _p in _ps) + ', spelled exactly as in its `def` line. Your '
                       'dial uses `' + str(getattr(_err, 'name', '')) + '`, which it does not have. '
                       + _ev('called ' + _c(_args), 'Python stopped with ' + _err_text(_err)))
    assert _err is None, _stop(_err, 'called ' + _c(_args))
    if _val is None:
        assert not _ls, __PRINTED__ + ' ' + _ev('called ' + _c(_args), 'it printed a line, but returned `None`')
        assert False, __NONE__ + ' ' + _ev('called ' + _c(_args), 'it returned `None`')
    assert type(_val).__name__ != 'str', __TEXT__ + ' ' + _ev('called ' + _c(_args), 'it returned text')
    _seen.append((_args, _want, _val))
(_a1, _w1, _v1), (_a2, _w2, _v2) = _seen
if _v1 == _v2:
    assert _v1 != 0, __ZERO__
    assert False, __SAME__ + ' ' + _ev('called ' + _c(_a1) + ' and ' + _c(_a2), 'both returned ' + str(_v1))
for _args, _want, _val in _seen:
    if _val != _want:
        _end = 'it returned ' + str(_val) + ', not ' + str(_want)
        for _sa, _sv, _sm in _slips:
            assert not (tuple(_sa) == tuple(_args) and _val == _sv and type(_val) == type(_sv)), _sm + ' ' + _ev('called ' + _c(_args), _end)
        assert _val not in _args, __PARAM_BACK__ + ' ' + _ev('called ' + _c(_args), _end)
        assert False, __FIX__ + ' ' + _ev('called ' + _c(_args), _end)
_picks = [_c for _n in _ast.walk(_fd) if type(_n).__name__ in ('If', 'IfExp') for _c in _ast.walk(_n.test)
          if type(_c).__name__ == 'Compare' and [_o for _o in _c.ops if type(_o).__name__ == 'Eq']
          and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
               and type(_x.value).__name__ in ('int', 'float')]]
assert not _picks, __LOOKUP__
'''


def dial_check(label, name, sig, cases, slips, fix, **extra):
    messages = dict(
        printed="Use `return` in place of `print`, so the array gets the number back.",
        none="Return the number with `return`.",
        text="Return a number: no quotes, no `str()`.",
        zero="Replace `return 0` with the dial's formula, built from its parameters.",
        same="Use the parameters: a function gets its numbers when it is called.",
        param_back="Return the worked-out number, not a parameter as it came in.",
        lookup=("Build one formula from the parameters, for every number: your dial picks its answer with `if` "
                "and `==`, so a number the check never tried would get the wrong reading."),
        fix=fix,
    )
    messages.update(extra)
    return (label, sx(ARRAY_SETUP) + fill(_DIAL, name=name, sig=sig, cases=[(tuple(a), w) for a, w in cases],
                                          slips=[(tuple(a), v, m) for a, v, m in slips], **messages))


_CALIBRATE = r'''
_fd = _need_def('calibrate', 1, 'def calibrate(hero):')
_want_keys = ('max_mana', 'average_damage')
_party = {}
for _h in roster:
    _party[_h['name']] = (_h['magical_affinity'] * 2, (1 + _h['die_size']) / 2)
for _s, _who, _mm, _ad in ((dict(name='Brakka', magical_affinity=7, die_size=10), 'brakka', 14, 5.5),
                           (dict(name='Moss', magical_affinity=11, die_size=4), 'moss', 22, 2.5)):
    _call = 'called `calibrate(' + _who + ')`, with affinity ' + str(_s['magical_affinity']) + ' and a d' + str(
        _s['die_size'])
    _s0 = dict(_s)
    _val, _ls, _err = _quiet(calibrate, _s)
    if _err is not None:
        _t = str(_err)
        assert type(_err).__name__ != 'KeyError', __SHEET_KEY__ + ' ' + _ev(_call, 'Python stopped with '
                                                                           + _err_text(_err))
        assert not ("'dict'" in _t and ('*' in _t or '+' in _t)), __WHOLE__
        assert not ("'str'" in _t and ('*' in _t or '+' in _t)), __QUOTED_KEY__ + ' ' + _ev(
            _call, 'Python stopped with ' + _err_text(_err))
        assert 'positional argument' not in _t, __COUNT__ + ' ' + _ev(_call, 'Python stopped with ' + _err_text(_err))
        assert False, _stop(_err, _call)
    _added = [_k for _k in _s if _k not in _s0]
    assert _val is not _s, __SAME_SHEET__ + ' ' + _ev(_call, 'it handed back the sheet it was handed')
    if _val is None:
        assert not _ls, __PRINTED__ + ' ' + _ev(_call, 'it printed, but returned `None`')
        assert not _added, __WROTE_SHEET__ + ' ' + _ev(_call, 'the sheet got new keys, and the call returned `None`')
        assert False, __NONE__
    assert type(_val).__name__ == 'dict', __NOT_DICT__
    assert _val, __EMPTY__
    _k, _x = _key_slip(_val, _want_keys)
    if _k is not None:
        assert _x is None, ('The dictionary has a key ' + _lit(_x) + ', and the array reads `"' + _k + '"`, letter '
                            'for letter.')
        assert False, 'Give the dictionary the key `"' + _k + '"`.'
    _got = (_val['max_mana'], _val['average_damage'])
    assert _got != (0, 0), __PLACEHOLDERS__
    _zero = [_k for _k, _v in zip(_want_keys, _got) if _v == 0 and type(_v).__name__ == 'int']
    assert not _zero, ('Replace the 0 after `"' + (_zero or [''])[0] + '"` with a call to its dial, on a number '
                       'read from `hero`.')
    assert not [_v for _v in _got if callable(_v)], __UNCALLED__
    assert not [_v for _v in _got if type(_v).__name__ == 'str' and ('magical_affinity' in _v or 'die_size' in _v)], (
        __QUOTED_KEY__ + ' ' + _ev(_call, 'a reading held text'))
    assert not [_v for _v in _got if type(_v).__name__ == 'str' and _v.startswith(_s['name'] + ':')], (
        __TEXT_DIAL__ + ' ' + _ev(_call, 'a reading held a whole line of text'))
    assert not [_v for _v in _got if type(_v).__name__ == 'str'], __TEXT__ + ' ' + _ev(_call, 'a reading held text')
    if _got != (_mm, _ad):
        _end = 'it returned ' + str(_got[0]) + ' and ' + str(_got[1]) + ', not ' + str(_mm) + ' and ' + str(_ad)
        _named = [_n.id for _n in _ast.walk(_fd) if type(_n).__name__ == 'Name' and _n.id in __SHEETS__]
        assert not _named, (__WRONG_SHEET__ + ' Your function reads `' + (_named or [''])[0] + '`. '
                            + _ev(_call, _end))
        _whose = [_n for _n, _p in _party.items() if _p == _got]
        _typed = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Constant'
                  and type(_n.value).__name__ in ('int', 'float')]
        assert not (_whose and _typed), (__TYPED_READINGS__ + ' ' + (_whose or [''])[0] + '. '
                                         + _ev(_call, _end))
        assert not _whose, (__WRONG_SHEET__ + ' ' + _ev(_call, 'it returned ' + (_whose or [''])[0]
                                                       + "'s readings"))
        assert not (_got[0] == 2 * _s['die_size'] or _got[1] == (1 + _s['magical_affinity']) / 2), (
            __SWAPPED__ + ' ' + _ev(_call, _end))
        assert False, __WRONG__ + ' ' + _ev(_call, _end)
_keep = (_g['max_mana_for'], _g['average_damage'])
def _stand_mm(_a):
    return 1000 + _a
def _stand_ad(_d):
    return 2000 + _d
_g['max_mana_for'], _g['average_damage'] = _stand_mm, _stand_ad
try:
    _val, _ls, _err = _quiet(calibrate, dict(name='Brakka', magical_affinity=7, die_size=10))
finally:
    _g['max_mana_for'], _g['average_damage'] = _keep
def _gave(_key):
    return str(_val.get(_key) if type(_val).__name__ == 'dict' else _val)
assert type(_val).__name__ == 'dict' and _val.get('max_mana') == 1007, (
    __DIAL_MM__ + " (Mar'tu's check made `max_mana_for` give 1007 for affinity 7, only inside the check; your "
    "`calibrate` still gave " + _gave('max_mana') + '.)')
assert _val.get('average_damage') == 2010, (
    __DIAL_AD__ + " (Mar'tu's check made `average_damage` give 2010 for die size 10, only inside the check; your "
    "`calibrate` still gave " + _gave('average_damage') + '.)')
'''

_KEEP_DIALS = r'''
for _name, _src in __DIALS__:
    _mine = _fdef(_name)
    _theirs = _ast.parse(_src).body[0]
    assert _mine is not None and _ast.dump(_mine) == _ast.dump(_theirs), (
        '`' + _name + '` changed. It is already finished, so leave it as it is.')
'''

_RUN_ARRAY = r'''
_fd = _need_def('run_array', 2, 'def run_array(heroes, dial):')
_log = []
def _probe(_h):
    _log.append(_h)
    return 'reading for ' + str(_h.get('name') if type(_h).__name__ == 'dict' else _h)
_hs = [dict(name='Brakka', magical_affinity=7, die_size=10), dict(name='Moss', magical_affinity=11, die_size=4)]
_call = 'called `run_array(heroes, probe)` with two other heroes, Brakka and Moss'
_val, _ls, _err = _quiet(run_array, _hs, _probe)
if _err is not None:
    assert not ('not iterable' in str(_err) or 'not callable' in str(_err)), __ORDER__
    assert False, _stop(_err, _call)
_names = [_h.get('name') for _h in _log if type(_h).__name__ == 'dict']
if not _log:
    assert not [_l for _l in _ls if '<function' in _l], __NO_CALL__
    assert not [_l for _l in _ls if 'Brakka' in _l], __BY_NAME__ + ' ' + _ev(_call, 'the probe never ran')
    assert not [_l for _l in _ls if 'Oogrish' in _l or 'Lucky' in _l], __ROSTER__
    assert False, __CALL__ + ' ' + _ev(_call, 'the dial never ran')
if [_n for _n in _names if _n not in ('Brakka', 'Moss')] or not _names or ('Moss' not in _names and len(_names) > 1):
    _used = [_n.id for _n in _ast.walk(_fd) if type(_n).__name__ == 'Name']
    _handed = 'the dial was handed ' + (', '.join(_names) if _names else 'no hero sheet')
    assert 'roster' not in _used, __ROSTER__ + ' ' + _ev(_call, _handed)
    _sheet = [_v for _v in __SHEETS__ if _v in _used]
    assert not _sheet, ('Hand the dial each `hero` from the loop: your loop hands it `' + (_sheet or [''])[0]
                        + '` every time. ' + _ev(_call, _handed))
    assert False, __EACH__ + ' ' + _ev(_call, _handed)
_shown = [_l for _l in _ls if _l.startswith('reading for')]
if _shown != ['reading for Brakka', 'reading for Moss']:
    _beside = [_l for _l in _ls if 'reading for' in _l and not _l.startswith('reading for')]
    assert not (_beside and not _shown), __BESIDE__ + ' ' + _ev(_call, 'each reading had more beside it')
    assert _shown, (__RETURNED__ if _val is not None else __PRINT__) + ' ' + _ev(_call, 'no reading was printed')
    assert False, __EVERY__ + ' ' + _ev(_call, str(len(_shown)) + ' of 2 readings were printed')
'''

_ARRAY_CALL = r'''
_ns, _ls, _err, _miss = _rerun([('run_array', _wrap('run_array', '_rlog'))])
assert not _miss, __KEEP_RUN__
assert not _err, _stop(_err, 'ran your program again')
_hand = [_a for _a in _ns.get('_rlog', []) if len(_a) == 2 and _a[1] is _ns.get('mana_dial')]
if not _hand:
    assert not [_a for _a in _ns.get('_rlog', []) if len(_a) == 2 and _a[1] is _ns.get('damage_dial')], __OTHER_DIAL__
    assert not [_l for _l in _ls if _l.startswith('Oogrish:')], __OWN__
    assert False, __CALL__
assert _hand[0][0] is _ns.get('roster'), __ROSTER__
for _line in __WANT__:
    assert _line in _lines(), __SHOWN__
'''

_DIAL_BOOK = r'''
_d = _g.get('dials')
assert type(_d).__name__ == 'dict', __MAKE__
for _k, _fname in (('mana', 'mana_dial'), ('damage', 'damage_dial')):
    if _k not in _d:
        _x = [_y for _y in _d if _near(_y, _k)]
        assert not _x, '`dials` has the key ' + _lit((_x or [''])[0]) + ', not `"' + _k + '"`, letter for letter.'
        assert False, 'Give `dials` the key `"' + _k + '"`, holding `' + _fname + '`.'
    _v = _d[_k]
    if _v is not _g.get(_fname):
        assert _v is not None and type(_v).__name__ != 'str', ('Store `' + _fname + '` itself under `"' + _k
                                                               + '"`: no `()`, no quotes.')
        assert False, 'Store `' + _fname + '` under `"' + _k + '"`.'
_ns, _ls, _err, _miss = _rerun([('*dials', _stand_in('_dl') + 'dials["damage"] = _fx\n')])
assert not _err, _stop(_err, 'ran your program again')
_names = [_h.get('name') for _h in _ns.get('_dl', []) if type(_h).__name__ == 'dict']
if _names != __NAMES__:
    if not _names:
        _ev_none = _ev('put another dial in `dials`', 'it never ran')
        assert not _top_calls('damage_dial'), __THROUGH__ + ' ' + _ev_none
        _mana_calls = [_c for _s in _top() for _c in _ast.walk(_s) if type(_c).__name__ == 'Call'
                       and type(_c.func).__name__ == 'Subscript' and type(_c.func.slice).__name__ == 'Constant'
                       and _c.func.slice.value == 'mana']
        assert not _mana_calls, __MANA_KEY__ + ' ' + _ev_none
        assert False, __CALL_FROM__ + ' ' + _ev_none
    assert False, __EVERY__
for _line in __WANT__:
    assert _line in _lines(), __SHOWN__
'''

_ARRAY_HEROES = [name for _, name, _, _, _ in PARTY]
_MANA_LINES = [f"{name}: {mana}" for _, name, mana, _, _ in PARTY]
_DAMAGE_LINES = [f"{name}: {(1 + die) / 2}" for _, name, _, _, die in PARTY]

THE_RESONANCE_ARRAY = dict(
    kind="project",
    id="the-resonance-array",
    title="The Resonance Array",
    minutes=20,
    summary="Write the dials of Mar'tu's brass resonance array as functions, calibrate a hero, and run the array "
            "with a dial handed over.",
    intro=(
        "The brass resonance array Mar'tu hauled from the Institute has dials. Each dial needs a formula.\n"
        "Three parts, in order: A. the dials, B. calibrate a hero, C. run the array.\n"
        "`roster` holds the four heroes:\n"
        "```text\nname        affinity  die\nOogrish         9      d6\nGearshift      10      d8\n"
        "Bomb Shell     12      d8\nLucky          13      d6\n```\n"
        "Their keys are `\"name\"`, `\"magical_affinity\"` and `\"die_size\"`."
    ),
    martu=(
        "At the Institute we wrote every dial as a recipe. Then nobody argued about the arithmetic.\n"
        "Each dial gets its numbers when it is called. My check calls them with other numbers and other heroes, "
        "only inside the check, so typed answers will not hold.\n"
        "Two dials at the bottom are finished. Read them, use them, leave them alone."
    ),
    setup=ARRAY_SETUP,
    names=["max_mana_for", "affinity", "average_damage", "die_size", "next_gap", "last_gap", "shrink", "calibrate",
           "hero", "run_array", "heroes", "dial", "roster", "mana_dial"],
    starter=ARRAY_STARTER,
    checkpoints=[
        dict(
            id="max-mana-dial",
            text="A. `max_mana_for(affinity)` returns twice the affinity.",
            dictated=False,
            hints=[
                "Replace `return 0` in `max_mana_for`. Twice the affinity: the parameter, times 2.",
                "`def double(n):` with `return n * 2` under it returns twice whatever is handed in.",
                "Write `return affinity * 2` in place of `return 0` in `max_mana_for`.",
            ],
            checks=[
                dial_check(
                    "max_mana_for returns twice the affinity", "max_mana_for", "def max_mana_for(affinity):",
                    [((7,), 14), ((11,), 22)],
                    [((7,), 49, "Twice means times 2, not the affinity times itself."),
                     ((7,), 9, "Twice means times 2: `+ 2` adds two.")],
                    "Return twice the affinity: the parameter `affinity`, times 2.",
                ),
            ],
            pass_line="Gearshift: Twice the affinity. Math checks out.",
        ),
        dict(
            id="average-damage-dial",
            text="A. `average_damage(die_size)` returns `(1 + die_size) / 2`.",
            dictated=True,
            hints=[
                "Replace `return 0` in `average_damage`. The brackets matter: add first, then halve.",
                "`(2 + 4) / 2` is 3.0. Without brackets, `2 + 4 / 2` is 4.0, because Python divides first.",
                "Write `return (1 + die_size) / 2` in place of `return 0` in `average_damage`.",
            ],
            checks=[
                dial_check(
                    "average_damage returns the die's average", "average_damage", "def average_damage(die_size):",
                    [((10,), 5.5), ((4,), 2.5)],
                    [((10,), 6.0, "Add first, then halve: put brackets around `1 + die_size`."),
                     ((10,), 5, "Use `/`, not `//`: the average can end in .5."),
                     ((10,), 5.0, "Add 1 before you halve: `(1 + die_size) / 2`.")],
                    "Return `(1 + die_size) / 2`, built from the parameter.",
                ),
            ],
            pass_line="Oogrish: A d6 averages three and a half. Steady, now.",
        ),
        dict(
            id="next-gap-dial",
            text="A. `next_gap(last_gap, shrink)` returns the last gap minus the shrink.",
            dictated=False,
            hints=[
                "Replace `return 0` in `next_gap`. The gaps shrink, so the next one is smaller.",
                "On the chalk wall, a gap of 44 with a shrink of 3 gives 41: `44 - 3`.",
                "Write `return last_gap - shrink` in place of `return 0` in `next_gap`.",
            ],
            checks=[
                dial_check(
                    "next_gap returns the last gap minus the shrink", "next_gap", "def next_gap(last_gap, shrink):",
                    [((30, 6), 24), ((25, 2), 23)],
                    [((30, 6), -24, "Take the shrink from the last gap: `last_gap` comes first."),
                     ((30, 6), 36, "The gaps shrink: subtract the shrink, don't add it.")],
                    "Return the last gap minus the shrink, built from the parameters.",
                ),
            ],
            pass_line="Mar'tu: The decay is accelerating. Now the array can say so.",
        ),
        dict(
            id="calibrate-a-hero",
            text=(
                "B. `calibrate(hero)` returns a dictionary with the keys `\"max_mana\"` and `\"average_damage\"`. "
                "Build each value by calling its dial on the hero's sheet."
            ),
            dictated=False,
            hints=[
                "Replace each 0 in `calibrate`. Each value is a call to its dial, with a number read from `hero`.",
                "`mana_dial` below already does half: `aff = hero[\"magical_affinity\"]`, then `max_mana_for(aff)`. "
                "Do the same with `\"die_size\"` and `average_damage`.",
                "A value in a dictionary can be a call: `{\"double\": double(jar[\"size\"])}`.",
                "Replace the first 0 with `max_mana_for(hero[\"magical_affinity\"])` and the second with "
                "`average_damage(hero[\"die_size\"])`.",
            ],
            checks=[
                (
                    "calibrate builds the readings from the dials",
                    sx(ARRAY_SETUP) + fill(
                        _CALIBRATE,
                        sheet_key="Read the sheet's own keys, letter for letter: `\"magical_affinity\"` and "
                                  "`\"die_size\"`.",
                        whole="Hand each dial a number from the sheet, like `hero[\"magical_affinity\"]`, not the "
                              "whole sheet.",
                        count="Hand each dial one value: each dial has one parameter.",
                        printed="Use `return` in place of `print`, so the array gets the dictionary back.",
                        quoted_key=("Hand each dial a number read from the sheet, like `hero[\"die_size\"]`. A key "
                                    "in quotes on its own is just those letters, so a dial got text."),
                        same_sheet=("Build a new dictionary of readings and return that. Your `calibrate` writes the "
                                    "readings into the hero's own sheet and hands the sheet back."),
                        wrote_sheet=("Build a new dictionary of readings and `return` it. Your `calibrate` writes the "
                                     "readings into the hero's own sheet, so the caller gets `None` back."),
                        uncalled=("Call each dial, with brackets: `max_mana_for(...)`. Your dictionary holds the "
                                  "dial functions themselves, not their readings."),
                        none="Return the dictionary with `return`.",
                        not_dict="Return a dictionary, with `{` and `}`.",
                        empty="Fill the dictionary: it is still empty, `{}`.",
                        placeholders="Replace each 0 with a call to its dial, on a number read from `hero`.",
                        typed_readings=("Build each reading by calling its dial on `hero`, not typed numbers. Typed "
                                        "readings only fit"),
                        text="Use the dials' numbers as they come back: no quotes, no `str()`.",
                        text_dial=("Call the number dials, `max_mana_for` and `average_damage`. `mana_dial` and "
                                   "`damage_dial` hand back a whole line of text, for the array to print."),
                        sheets=[var for var, _, _, _, _ in PARTY],
                        wrong_sheet="Read from `hero`, the sheet handed in.",
                        swapped=("Hand each dial its own value: the affinity to `max_mana_for`, the die size to "
                                 "`average_damage`."),
                        wrong="Build each value by calling its dial on the hero's sheet.",
                        dial_mm=("Build `\"max_mana\"` by calling `max_mana_for(...)`: your `calibrate` works the "
                                 "number out itself, so a change to the dial would never reach it."),
                        dial_ad="Build `\"average_damage\"` by calling `average_damage(...)`, the dial.",
                    ),
                ),
            ],
            pass_line="Gearshift: Readings match the sheet. Visor dims. Math checks out.",
        ),
        dict(
            id="run-the-array",
            text="C. `run_array(heroes, dial)` prints `dial(hero)` for each hero in `heroes`.",
            dictated=False,
            hints=[
                "Replace `pass` in `run_array`. A `for` loop over `heroes`, with one `print` inside it.",
                "In `cast_on_everyone`, the loop called `effect(hero)`. Here, print what `dial(hero)` returns.",
                "Write `for hero in heroes:` with `print(dial(hero))` under it, indented.",
            ],
            checks=[
                ("the finished dials are unchanged",
                 sx(ARRAY_SETUP) + fill(_KEEP_DIALS, dials=[("mana_dial", MANA_DIAL), ("damage_dial", DAMAGE_DIAL)])),
                (
                    "run_array prints the dial's reading for every hero",
                    sx(ARRAY_SETUP) + fill(
                        _RUN_ARRAY,
                        order="Keep the parameters in the order `heroes, dial`: the list first, then the function.",
                        no_call="Call the dial: `dial(hero)`, with the brackets. Printing `dial` alone shows the "
                                "function, not a reading.",
                        by_name="Call `dial`, the function handed in. Your loop calls a dial by its own name, so any "
                                "other dial would be ignored.",
                        roster="Loop over `heroes`, the list handed in: your loop reads `roster`.",
                        sheets=[var for var, _, _, _, _ in PARTY],
                        each="Hand the dial each hero from the loop over `heroes`: `dial(hero)`.",
                        beside=("Print just the reading: `print(dial(hero))`. Your line shows something else beside "
                                "it."),
                        call="Call `dial(hero)` for each hero in `heroes`.",
                        returned="Print each reading with `print(dial(hero))`. A `return` ends `run_array` and "
                                 "shows nothing.",
                        print="Print each reading: `print(dial(hero))`.",
                        every="Print one reading for every hero in `heroes`.",
                    ),
                ),
            ],
            pass_line="Bomb Shell: Array hums. Works.",
        ),
        dict(
            id="hand-over-the-dial",
            text="C. Call `run_array` with `roster` and `mana_dial`, no parentheses.",
            dictated=True,
            hints=[
                "At the bottom, below comment 6. Hand over the dial by its name.",
                "`cast_on_everyone(roster, warm_hands)` handed a function over the same way.",
                "Write `run_array(roster, mana_dial)` at the bottom.",
            ],
            checks=[
                (
                    "mana_dial is handed to run_array",
                    sx(ARRAY_SETUP) + fill(
                        _ARRAY_CALL,
                        keep_run="Keep `run_array` from task 5, made with `def`.",
                        other_dial="Hand over `mana_dial`, as the task asks: your call hands over `damage_dial`.",
                        own="Hand `mana_dial` to `run_array`, with no `()`. Your program shows the readings itself.",
                        call="Call `run_array(roster, mana_dial)` at the bottom.",
                        roster="Hand over `roster` itself, the list that is already made.",
                        want=_MANA_LINES,
                        shown="Show the four mana readings: `run_array(roster, mana_dial)` at the bottom.",
                    ),
                ),
            ],
            pass_line="Mar'tu: Four dials read, one line of yours. The Institute would be jealous.",
        ),
    ],
    solution=ARRAY_SOLUTION,
    partials=[_array_upto(1), _array_upto(2), _array_upto(3), _array_upto(4), _array_upto(5)],
    another_way=[
        dict(
            angle="picture",
            label="The array",
            text=(
                "```text\n dials (functions)\n   max_mana_for  affinity -> mana\n   average_damage die -> damage\n"
                "        |\n calibrate(hero)\n   -> {\"max_mana\": ...,\n       \"average_damage\": ...}\n"
                "        |\n run_array(roster, mana_dial)\n   one reading per hero\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. A dial: replace `return 0` with the formula, using the parameters.\n"
                "2. `calibrate`: read two numbers from `hero`, hand each to its dial, return both in a dictionary.\n"
                "3. `run_array`: a loop over `heroes`, printing `dial(hero)`.\n"
                "4. Hand `mana_dial` over with no `()`."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "`get_mana_bar(caster)` read a sheet and returned a value, and `show_mana(caster)` passed it on. "
                "`calibrate` reads a sheet too. `run_array` takes a function, like `add_spell` took "
                "`strengthen_magic`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants every dial in one place. Make `dials`, a dictionary with `\"mana\"` holding `mana_dial` and "
            "`\"damage\"` holding `damage_dial`. Then, for each hero in `roster`, print `dials[\"damage\"](hero)`."
        ),
        hints=[
            "The functions go in with no `()`. Then a `for` loop with one `print` inside.",
            "Reading and calling at once: `dials[\"damage\"]` is the function, and `(hero)` calls it.",
            "Write `dials = {\"mana\": mana_dial, \"damage\": damage_dial}`, then `for hero in roster:` with "
            "`print(dials[\"damage\"](hero))` under it.",
        ],
        checks=[
            (
                "dials holds both dials, and the damage readings come from it",
                sx(ARRAY_SETUP) + fill(
                    _DIAL_BOOK,
                    make="Make `dials`, a dictionary holding the two finished dials.",
                    names=_ARRAY_HEROES,
                    through="Call the dial from `dials`: `dials[\"damage\"](hero)`. Your loop calls it by its own "
                            "name.",
                    mana_key=("Call the damage dial: `dials[\"damage\"](hero)`. Your loop calls the dial stored "
                              "under `\"mana\"`."),
                    call_from="Call the damage dial from `dials` for each hero: `dials[\"damage\"](hero)`.",
                    every="Call `dials[\"damage\"](hero)` once for each hero in `roster`.",
                    want=_DAMAGE_LINES,
                    shown="Print each reading: `print(dials[\"damage\"](hero))`.",
                ),
            ),
        ],
        solution=ARRAY_SOLUTION + "\n\ndials = {\n    \"mana\": mana_dial,\n    \"damage\": damage_dial,\n}\n"
                                  "for hero in roster:\n    print(dials[\"damage\"](hero))\n",
    ),
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        snippet="mana_bar = get_mana_bar(caster)\nprint_mana(caster, mana_bar)",
        why=(
            "You've wired functions together before: build the bar, then pass it on. The array does the same "
            "with its dials, and hands one over without `()`, like `strengthen_magic`."
        ),
    ),
    takeaway="Dials are functions: parameters in, `return` out. A dial can be handed over: `run_array(roster, "
             "mana_dial)`.",
    wrong_answers=[
        dict(why="the starter (return 0)", code=ARRAY_STARTER, fails_at=1, message_contains="Replace `return 0`"),
        dict(why="a typed answer (the class's biggest slip: Lucky's 26)", code=_array("    return 26\n"),
             fails_at=1, message_contains="Use the parameters"),
        dict(why="print instead of return", code=_array("    print(affinity * 2)\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the affinity as it came in", code=_array("    return affinity\n"), fails_at=1,
             message_contains="not a parameter"),
        dict(why="+ 2 for times 2", code=_array("    return affinity + 2\n"), fails_at=1, message_contains="adds two"),
        dict(why="CP2 no brackets (Python divides first)",
             code=_array_upto(1, avg="    return 1 + die_size / 2\n"), fails_at=2, message_contains="brackets"),
        dict(why="CP2 // for /", code=_array_upto(1, avg="    return (1 + die_size) // 2\n"), fails_at=2,
             message_contains="not `//`"),
        dict(why="CP2 a typed average", code=_array_upto(1, avg="    return 3.5\n"), fails_at=2,
             message_contains="Use the parameters"),
        dict(why="CP3 the subtraction reversed", code=_array_upto(2, gap="    return shrink - last_gap\n"),
             fails_at=3, message_contains="comes first"),
        dict(why="CP3 a typed gap from the chalk wall", code=_array_upto(2, gap="    return 32\n"), fails_at=3,
             message_contains="Use the parameters"),
        dict(why="CP4 an approximate key (\"mana\" for \"max_mana\")",
             code=_array_upto(3, cal=DIAL_CAL.replace('"max_mana":', '"mana":')), fails_at=4,
             message_contains="letter for letter"),
        dict(why="CP4 Lucky's readings typed in (literal test values)",
             code=_array_upto(3, cal='    return {"max_mana": 26, "average_damage": 3.5}\n'), fails_at=4,
             message_contains="Typed readings only fit Lucky."),
        dict(why="CP4 Gearshift's readings typed in, his real 20 and 4.5 (literal test values)",
             code=_array_upto(3, cal='    return {"max_mana": 20, "average_damage": 4.5}\n'), fails_at=4,
             message_contains="not typed numbers. Typed readings only fit Gearshift."),
        dict(why="CP4 the dials called on Lucky's typed numbers, not hero's",
             code=_array_upto(3, cal='    return {\n        "max_mana": max_mana_for(13),\n'
                                     '        "average_damage": average_damage(6),\n    }\n'), fails_at=4,
             message_contains="Typed readings only fit Lucky."),
        dict(why="CP4 the starter's calibrate (each 0 still in place)", code=_array_upto(3), fails_at=4,
             message_contains="Replace each 0 with a call to its dial"),
        dict(why="CP4 one 0 replaced, the other still in place",
             code=_array_upto(3, cal=CAL_ZEROS.replace('"max_mana": 0', '"max_mana": max_mana_for(hero["magical_affinity"])')),
             fails_at=4, message_contains='Replace the 0 after `"average_damage"`'),
        dict(why="CP4 an empty dictionary returned", code=_array_upto(3, cal="    return {}\n"), fails_at=4,
             message_contains="still empty"),
        dict(why="CP4 the wrong sheet: lucky read inside calibrate",
             code=_array_upto(3, cal=DIAL_CAL.replace('hero["', 'lucky["')), fails_at=4,
             message_contains="sheet handed in"),
        dict(why="CP4 the whole sheet handed to a dial",
             code=_array_upto(3, cal='    return {\n        "max_mana": max_mana_for(hero),\n'
                                     '        "average_damage": average_damage(hero["die_size"]),\n    }\n'),
             fails_at=4, message_contains="not the whole sheet"),
        dict(why="CP4 a dial called with the wrong number of values",
             code=_array_upto(3, cal=DIAL_CAL.replace('average_damage(hero["die_size"])',
                                                      'average_damage(hero["die_size"], 2)')),
             fails_at=4, message_contains="one value"),
        dict(why="CP4 each dial handed the other's value",
             code=_array_upto(3, cal='    return {\n        "max_mana": max_mana_for(hero["die_size"]),\n'
                                     '        "average_damage": average_damage(hero["magical_affinity"]),\n    }\n'),
             fails_at=4, message_contains="its own value"),
        dict(why="CP4 the arithmetic done inline, not through the dial",
             code=_array_upto(3, cal='    return {\n        "max_mana": hero["magical_affinity"] * 2,\n'
                                     '        "average_damage": average_damage(hero["die_size"]),\n    }\n'),
             fails_at=4, message_contains="works the number out itself"),
        dict(why="CP4 a near-miss sheet key (KeyError)",
             code=_array_upto(3, cal=DIAL_CAL.replace('"magical_affinity"]', '"affinity"]')), fails_at=4,
             message_contains="letter for letter"),
        dict(why="CP4 print instead of return",
             code=_array_upto(3, cal='    print(max_mana_for(hero["magical_affinity"]))\n'), fails_at=4,
             message_contains="in place of `print`"),
        dict(why="CP5 return instead of print in run_array",
             code=_array_upto(4, run="    for hero in heroes:\n        return dial(hero)\n"), fails_at=5,
             message_contains="A `return` ends"),
        dict(why="CP5 the dial printed, not called",
             code=_array_upto(4, run="    for hero in heroes:\n        print(dial)\n"), fails_at=5,
             message_contains="with the brackets"),
        dict(why="CP5 the loop reads roster, not heroes",
             code=_array_upto(4, run="    for hero in roster:\n        print(dial(hero))\n"), fails_at=5,
             message_contains="reads `roster`"),
        dict(why="CP5 mana_dial called by name, not the dial handed in",
             code=_array_upto(4, run="    for hero in heroes:\n        print(mana_dial(hero))\n"), fails_at=5,
             message_contains="by its own name"),
        dict(why="CP5 a finished helper edited",
             code=_array_upto(5, mana_dial=MANA_DIAL.replace('": "', '" = "')), fails_at=5,
             message_contains="leave it as it is"),
        dict(why="CP6 the dial handed over WITH () (missing argument)",
             code=_array_upto(5, call="run_array(roster, mana_dial())\n"), fails_at=0,
             message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="CP6 the result of a call handed over (text, not a function)",
             code=_array_upto(5, call="run_array(roster, mana_dial(lucky))\n"), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="CP6 the readings typed by hand",
             code=_array_upto(5, call="".join(f'print("{line}")\n' for line in _MANA_LINES)), fails_at=6,
             message_contains="shows the readings itself"),
        dict(why="CP6 the other dial handed over", code=_array_upto(5, call="run_array(roster, damage_dial)\n"),
             fails_at=6, message_contains="as the task asks"),
        dict(why="CP6 never called", code=_array_upto(5), fails_at=6, message_contains="at the bottom"),
        dict(why="CP1 an approximate parameter name in the body (A-01's `attack` for `base_attack`)",
             code=_array("    return aff * 2\n"), fails_at=1, message_contains="spelled exactly as in its `def` line"),
        dict(why="CP1 the hint's example name copied (`n` from `double(n)`)",
             code=_array("    return n * 2\n"), fails_at=1, message_contains="which it does not have"),
        dict(why="CP3 returns a variable that was never made (A-01's `return reslt`)",
             code=_array_upto(2, gap="    gap = last_gap - shrink\n    return reslt\n"), fails_at=3,
             message_contains="`reslt`"),
        dict(why="CP1 reverse-engineered from the check's numbers: an if picks each answer (A-08's backward working)",
             code=_array("    if affinity == 7:\n        return 14\n    return 22\n"), fails_at=1,
             message_contains="picks its answer with `if`"),
        dict(why="CP4 the readings written into the hero's sheet, nothing returned (the caller gets None)",
             code=_array_upto(3, cal='    hero["max_mana"] = max_mana_for(hero["magical_affinity"])\n'
                                     '    hero["average_damage"] = average_damage(hero["die_size"])\n'),
             fails_at=4, message_contains="the caller gets `None` back"),
        dict(why="CP4 the readings written into the hero's sheet, and the sheet handed back",
             code=_array_upto(3, cal='    hero["max_mana"] = max_mana_for(hero["magical_affinity"])\n'
                                     '    hero["average_damage"] = average_damage(hero["die_size"])\n'
                                     '    return hero\n'),
             fails_at=4, message_contains="hands the sheet back"),
        dict(why="CP4 the dials stored, not called (a function where its result was wanted)",
             code=_array_upto(3, cal='    return {"max_mana": max_mana_for, "average_damage": average_damage}\n'),
             fails_at=4, message_contains="dial functions themselves"),
        dict(why="CP4 the sheet's key in quotes on its own, not read from hero",
             code=_array_upto(3, cal=DIAL_CAL.replace('max_mana_for(hero["magical_affinity"])',
                                                      'max_mana_for("magical_affinity")')),
             fails_at=4, message_contains="just those letters"),
        dict(why="CP4 the finished text dials called instead of the number dials",
             code=_array_upto(3, cal='    return {"max_mana": mana_dial(hero), "average_damage": damage_dial(hero)}\n'),
             fails_at=4, message_contains="whole line of text"),
        dict(why="CP4 one reading read from Lucky's sheet (the wrong sheet, half the time)",
             code=_array_upto(3, cal=DIAL_CAL.replace('hero["magical_affinity"]', 'lucky["magical_affinity"]')),
             fails_at=4, message_contains="reads `lucky`"),
        dict(why="CP4 a reading turned into text with str()",
             code=_array_upto(3, cal=DIAL_CAL.replace('max_mana_for(hero["magical_affinity"])',
                                                      'str(max_mana_for(hero["magical_affinity"]))')),
             fails_at=4, message_contains="no `str()`"),
        dict(why="CP5 the dial handed Lucky's sheet every time (the wrong sheet)",
             code=_array_upto(4, run="    for hero in heroes:\n        print(dial(lucky))\n"), fails_at=5,
             message_contains="hands it `lucky` every time"),
        dict(why="CP5 the first hero handed over every time",
             code=_array_upto(4, run="    for hero in heroes:\n        print(dial(heroes[0]))\n"), fails_at=5,
             message_contains="each hero from the loop"),
        dict(why="CP5 the whole sheet printed beside each reading",
             code=_array_upto(4, run="    for hero in heroes:\n        print(hero, dial(hero))\n"), fails_at=5,
             message_contains="something else beside it"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="func-takes-dict,dict-from-params,func-as-value,read-helper",
             solo="false", dictates="2,6", foreign_names="double,n,jar,size", camp="true",
             par="max_mana_for (7),(11); average_damage (10),(4); next_gap (30, 6),(25, 2); calibrate Brakka "
                 "(7, d10), Moss (11, d4)") + "\n"
        "Project 6P in campaign mode (2.10): task-group headers and placeholders in the starter, the campaign's "
        "phrasing, check messages and the explainer, hints capped at rung 2, Compare after 5 minutes, and no "
        "Assemble it (so no `assemble` field). Tasks: A1-A3 the spec's three dials (PAR + RET with two fresh sets "
        "each, never the party's values; slips named: `+ 2`, the missing brackets, `//`, the reversed subtraction); "
        "B4 calibrate (KEY on the two readings; the wrong sheet, typed readings, the whole sheet, the wrong number "
        "or order of values; CALL: each dial is swapped for a stand-in in the student's own globals, so the reading "
        "must come from the dial); C5 run_array (CALL with a probe dial and two fresh heroes; return-instead-of-"
        "print, the uncalled dial, `roster` read instead of `heroes`, a dial called by name; KEEP: the two finished "
        "dials are unchanged, AST compare). Teacher's revision: calibrate starts as the solution's own shape with "
        "each value 0 (comment 4: 'Replace each 0 with a call to its dial.'), and the 0s get their own message; "
        "typed readings that match a party hero's (with numbers in the body and no outer sheet read) are told they "
        "only fit that hero; the stand-in evidence gives the numbers (1007 for affinity 7, 2010 for die size 10, "
        "and what the student's calibrate still gave). Also named: a dial that picks its answer with `if ... == <number>` (the "
        "check's own numbers, worked backward), a name the dial does not have (`n`, `aff`, `reslt`), readings "
        "written into the hero's sheet (returned or not), the dials stored uncalled, the text dials used in "
        "calibrate, the dial handed one sheet every time. C6 hands `mana_dial` over (NOP crashes are the explainer's: `()` and "
        "the call's text result). The spec's task 5 is split in two (write run_array, then hand the dial over), so "
        "CALL and NOP each have their own checkpoint. Side quest (old group D, G4 R16): a dictionary of dials, "
        "called as `dials[\"damage\"](hero)` (the spec writes `dials[\"mana\"]`; damage shows readings the main "
        "task did not, so the side quest has something new to show)."
    ),
)


# =============================================================================================
# Optional advanced challenge "The Spell Book, From Blank" (after the project; costs no one core time)
# =============================================================================================

SHOW_MANA_FN = (
    "_bars = []\n"
    "\n\n"
    "def show_mana(hero):\n"
    '    _bars.append((hero, hero["mana"]))\n'
    '    full = "█" * hero["mana"]\n'
    '    empty = "░" * (hero["max_mana"] - hero["mana"])\n'
    '    print(hero["name"] + ": Mana [" + full + empty + "]")\n'
    "\n\n"
)
BLANK_SETUP = _roster_setup(WARD_FNS + SHOW_MANA_FN, GLOW_PAGE)
BLANK_TESTS = [
    'learn_spell(lucky["spell_book"], "Lantern Ward", 6, 9, lantern_ward)',
    'cast(lucky, "Lantern Ward")',
    'cast(lucky, "Moon Step")',
]
BLANK_STARTER = "".join("# " + line + "\n" for line in BLANK_TESTS)
BLANK_SPELL = (
    "    spell = {\n"
    '        "mana_cost": mana_cost,\n'
    '        "required_affinity": required_affinity,\n'
    '        "effect": effect,\n'
    "    }\n"
)
BLANK_GUARD = (
    "def cast(hero, spell_name):\n"
    '    if spell_name not in hero["spell_book"]:\n'
    '        print(hero["name"], "doesn\'t know", spell_name)\n'
    "        return\n"
)
BLANK_READ = '    spell = hero["spell_book"][spell_name]\n'


def _blank(spell=BLANK_SPELL, store=LEARN_STORE, cast=None, tests=BLANK_STARTER, head=LEARN_SIGNATURE):
    """learn_spell, then (when `cast` is not None) cast with its guard and `cast` as the rest of its body."""
    out = head + spell + store
    if cast is not None:
        out += "\n\n" + BLANK_GUARD + cast
    return out + "\n\n" + tests


BLANK_SOLUTION = _blank(cast=BLANK_READ + _cast_body(), tests="".join(line + "\n" for line in BLANK_TESTS))

# A name that is not in the book: no crash, a message, nothing spent. A `return` straight in the function with lines
# under it (an early return that ends every cast) is named here too, so the guard step stays honest.
_GUARD = r'''
_asks = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'If' and [_c for _c in _ast.walk(_n.test)
         if type(_c).__name__ == 'Compare' and [_o for _o in _c.ops if type(_o).__name__ in ('In', 'NotIn')]]]
_early = [_i for _i, _s in enumerate(_fd.body) if type(_s).__name__ == 'Return' and _i < len(_fd.body) - 1]
assert not _early, __INDENT_RETURN__
def moon_step(hero):
    print('Moon Step lands.')
_hero = {'name': 'Brakka', 'mana': 15, 'max_mana': 20, 'abilities': {'magical_affinity': 12},
         'spell_book': {'Moon Step': {'mana_cost': 5, 'required_affinity': 7, 'effect': moon_step}}}
_what = 'cast Star Fall for a hero whose book holds only Moon Step'
_val, _ls, _err = _quiet(_g['cast'], _hero, 'Star Fall')
if _err is not None:
    _lost = type(_err).__name__ == 'KeyError' and 'Star Fall' in str(_err)
    assert not (_lost and _asks), __ADD_RETURN__ + ' ' + _ev(_what, 'Python stopped with ' + _err_text(_err))
    assert not _lost, __ASK_FIRST__ + ' ' + _ev(_what, 'Python stopped with ' + _err_text(_err))
    assert False, _crash(dict(err=_err, what=_what))
assert [_l for _l in _ls if _l != 'Moon Step lands.'], __SAY__ + ' ' + _ev(_what, 'nothing was printed')
assert _hero['mana'] == 15, __SPEND_NOTHING__ + ' ' + _ev(_what, 'the mana went to ' + str(_hero['mana']))
'''

_BLANK_LEARN_KEEP = dict(
    keep_def=("Write `learn_spell` with `def`, above the test lines: `def learn_spell(spell_book, spell_name, "
              "mana_cost, required_affinity, effect):`."),
    keep_sig=("Give `learn_spell` five parameters, in this order: `spell_book, spell_name, mana_cost, "
              "required_affinity, effect`."),
    params=LEARN_PARAMS,
)
_BLANK_CAST_KEEP = dict(
    _CAST_KEEP,
    keep_def="Write `cast` with `def`, below `learn_spell`: `def cast(hero, spell_name):`.",
    keep_sig="Give `cast` two parameters, in this order: `hero, spell_name`.",
)
_BLANK_NO_ELSE = ("Put `else:` above your cast and indent it one more step. Right now it sits outside the `if`, so "
                  "the hero hears the message and then casts anyway.")


def blank_learn_check(label, body, **messages):
    return (label, sx(BLANK_SETUP) + fill(_LEARN_PRE, **_BLANK_LEARN_KEEP) + fill(body, **messages))


def blank_cast_check(label, body, **messages):
    return (label, sx(BLANK_SETUP) + fill(_CAST_PRE, **_BLANK_CAST_KEEP) + fill(body, **messages))


BOOK_FROM_BLANK = dict(
    kind="challenge",
    id="spell-book-from-blank",
    title="The Spell Book, From Blank",
    level="advanced",
    optional=True,
    minutes=12,
    support="light",
    summary="Write learn_spell and cast from a blank page: the spell book and the barrier, every line yours.",
    martu=(
        "The spell book and the barrier, from a blank page. You have every piece now. Write two functions:\n"
        "1. `learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect)` builds `spell` from the "
        "matching parameters, then stores it in `spell_book` under `spell_name`.\n"
        "2. `cast(hero, spell_name)` asks the book first: a name it doesn't hold gets a message and `return`. "
        "Then get the page, compare, act: too little affinity, then too little mana, each says so; otherwise "
        "cast the effect, pay the cost, and call `show_mana(hero)`.\n"
        "Write them above the three test lines. Take the `#` off a test line to try it. `roster`, "
        "`lantern_ward` and `show_mana` are already made. My check uses other heroes and other spells, only "
        "inside the check."
    ),
    setup=BLANK_SETUP,
    names=["learn_spell", "spell_book", "spell_name", "mana_cost", "required_affinity", "effect", "spell", "cast",
           "hero", "show_mana"],
    starter=BLANK_STARTER,
    checkpoints=[
        dict(
            id="learn-builds-the-spell",
            text=(
                "Write `learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect)`. Inside, build "
                "`spell` with the keys `\"mana_cost\"`, `\"required_affinity\"` and `\"effect\"`, each holding its "
                "matching parameter."
            ),
            dictated=False,
            hints=[
                "The `def` line first, with the five parameters in that order. Each key in `spell` has a parameter "
                "with exactly the same name: that parameter is its match.",
                "A value can be a parameter: `{\"size\": size}` puts whatever was handed in as `size` there. No "
                "quotes on the value: quotes would make it just the letters.",
                "Write `def learn_spell(spell_book, spell_name, mana_cost, required_affinity, effect):`, then "
                "`spell = {` under it, indented, with `\"mana_cost\": mana_cost,` as its first key.",
            ],
            checks=[
                blank_learn_check(
                    "the spell holds the matching parameters", _SPELL_BUILT,
                    **dict(
                        _BUILT_MSGS,
                        keep_spell="Build `spell`, a dictionary, inside `learn_spell`.",
                        placeholders="Use the matching parameters: the spell holds 0, 0 and `None`.",
                        zero_cost="`\"mana_cost\"` holds 0: use the matching parameter, `mana_cost`.",
                        zero_need="`\"required_affinity\"` holds 0: use the matching parameter, `required_affinity`.",
                        none_effect="`\"effect\"` holds `None`: use the matching parameter, `effect`.",
                        missing_key='Give `spell` the key `"<key>"`, letter for letter, holding its matching parameter.',
                    ),
                ),
            ],
        ),
        dict(
            id="store-by-name",
            text="Store the spell in `spell_book`, using `spell_name` as the key. A second spell must keep the first.",
            dictated=False,
            hints=[
                "Inside the function, under `spell`. The key is the parameter `spell_name`, with no quotes.",
                "`shelf[label] = jar` stores the jar under whatever text `label` holds, in the shelf that was handed "
                "in. Every call adds one page and leaves the others alone.",
                "Write `spell_book[spell_name] = spell` under `spell`, indented inside the function.",
            ],
            checks=[
                blank_learn_check(
                    "the spell is stored under its name", _SPELL_STORED,
                    **dict(
                        _STORED_MSGS,
                        returned=("Store the spell in the book itself. `return` hands the spell back, but the book "
                                  "handed in stays empty, and the test line never uses what comes back."),
                        store="Store the spell in `spell_book`, inside `learn_spell`, using `spell_name` as the key.",
                    ),
                ),
                blank_learn_check("a second spell keeps the first", _SECOND_KEEPS_FIRST, **_SECOND_MSGS),
            ],
            pass_line="Gearshift: Every key, its own parameter, its own page. Math checks out.",
        ),
        dict(
            id="unknown-spell",
            text=(
                "Write `cast(hero, spell_name)`. If `spell_name` is not in the hero's `\"spell_book\"`, print a "
                "message and `return`."
            ),
            dictated=False,
            hints=[
                "Below `learn_spell`. The guard is the first thing inside `cast`: ask the hero's book about the "
                "name before any page is read.",
                "`if item not in pack:` asks a dictionary about a key. `return` under it ends the function there, "
                "so the lines below never read a page that isn't there.",
                "Write `if spell_name not in hero[\"spell_book\"]:` with a `print(...)` and then `return` under it, "
                "each indented one more step.",
            ],
            checks=[
                blank_cast_check(
                    "a name that is not in the book gets a message, and nothing breaks", _GUARD,
                    indent_return=("Indent `return` under the message, inside the `if`. At the function's own level "
                                   "it ends every cast, so the lines below it never run."),
                    add_return=("Add `return` under the message, inside the `if`, so `cast` stops there. Without it, Python "
                                "goes on and reads a page the book does not have."),
                    ask_first=("Ask the book first, before any page is read: `if spell_name not in "
                               "hero[\"spell_book\"]:`, with a message under it."),
                    say="Print a message when the name is not in the book, so the player knows why nothing happened.",
                    spend_nothing="Spend nothing when the name is not in the book.",
                ),
            ],
        ),
        dict(
            id="skilled-caster-casts",
            text="Below the guard, read the spell from the hero's book and cast it: a skilled caster with enough "
                 "mana casts.",
            dictated=False,
            hints=[
                "Below the guard. Get the page from the hero's book by its name, then call what is under "
                "`\"effect\"`.",
                "A function stored in a dictionary is called with brackets on the end: `pack[\"tool\"](sheet)` runs "
                "the function under `\"tool\"`.",
                "Write `spell = hero[\"spell_book\"][spell_name]`, then `spell[\"effect\"](hero)` under it.",
            ],
            checks=[
                blank_cast_check(
                    "a skilled caster with enough mana casts", _CASTS,
                    **dict(
                        _CASTS_MSGS,
                        cast=("Below the guard, read the page from the hero's book by its name, then call its "
                              "effect: `spell[\"effect\"](hero)`."),
                    ),
                ),
            ],
            pass_line="Lucky: The ward glows. From my own book. I'd like that in writing.",
        ),
        dict(
            id="too-little-affinity",
            text=(
                "Too little affinity does not cast: if `hero[\"abilities\"][\"magical_affinity\"]` is lower than "
                "`spell[\"required_affinity\"]`, print a message instead."
            ),
            dictated=False,
            hints=[
                "Above the cast. Two keys in a row read the affinity: the outer key, then the inner key.",
                "`if a < b:` with its line under it, then `else:` with the cast under it, each indented one more "
                "step.",
                "The shape, with your cast moved under `else:`, one step deeper:\n"
                "```python\nif ___ < ___:\n    print(...)\nelse:\n    spell[\"effect\"](hero)\n```",
                "Write `if hero[\"abilities\"][\"magical_affinity\"] < spell[\"required_affinity\"]:` with a "
                "`print(...)` under it, then `else:` above the cast.",
            ],
            checks=[
                blank_cast_check(
                    "too little affinity does not cast", _TURNS_AWAY,
                    cases=[(6, 15, 5, 7, "low"), (10, 15, 5, 11, "low"), (7, 15, 5, 7, "exact")],
                    typed="Compare with the spell's own `spell[\"required_affinity\"]`, not a typed number.",
                    turn_away=("Turn away a hero whose affinity is lower than the spell's `\"required_affinity\"`. "
                               "Check the sign, and that the cast sits in the last branch, `else`."),
                    exact="Exactly enough affinity should still cast: use `<`, not `<=`.",
                    **dict(_TURN_MSGS, no_else=_BLANK_NO_ELSE),
                ),
            ],
        ),
        dict(
            id="too-little-mana",
            text=(
                "Too little mana does not cast: otherwise, if `hero[\"mana\"]` is lower than "
                "`spell[\"mana_cost\"]`, print a message instead."
            ),
            dictated=False,
            hints=[
                "Between the affinity test and `else:`. `elif` asks only when the first test was false.",
                "`elif a < b:` sits at the same indent as the `if`, with its own line under it.",
                "Write `elif hero[\"mana\"] < spell[\"mana_cost\"]:` with a `print(...)` under it, above `else:`.",
            ],
            checks=[
                blank_cast_check(
                    "too little mana does not cast", _TURNS_AWAY,
                    cases=[(12, 4, 5, 7, "low"), (12, 7, 8, 7, "low"), (6, 4, 5, 7, "low")],
                    typed="Compare with the spell's own `spell[\"mana_cost\"]`, not a typed number.",
                    turn_away=("Turn away a hero whose mana is lower than the spell's `\"mana_cost\"`. Check the "
                               "sign, and that the cast sits in the last branch, `else`."),
                    exact="Exactly enough mana should still cast.",
                    **dict(_TURN_MSGS, no_else=_BLANK_NO_ELSE),
                ),
            ],
        ),
        dict(
            id="exactly-enough-mana",
            text="Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Look at the sign in the mana test. A hero with exactly 5 mana and a spell that costs 5 should "
                "still cast.",
                "`<` means *lower than*. `<=` means *lower than or the same*, so it turns away exactly enough.",
                "Write the mana test as `elif hero[\"mana\"] < spell[\"mana_cost\"]:`.",
            ],
            checks=[
                blank_cast_check(
                    "exactly enough mana still casts", _TURNS_AWAY,
                    cases=[(12, 5, 5, 7, "exact"), (12, 8, 8, 7, "exact")],
                    typed="", turn_away="", spend="", tell="", one_msg="", heroes=[], typed_name="", no_else="",
                    exact="Exactly enough mana should still cast: use `<`, not `<=`.",
                ),
            ],
            pass_line="Mar'tu: Exactly enough is enough. The barrier holds.",
        ),
        dict(
            id="pay-and-show",
            text=(
                "After the cast, subtract the spell's own `\"mana_cost\"` from `hero[\"mana\"]`, then call "
                "`show_mana(hero)`."
            ),
            dictated=False,
            hints=[
                "Under the cast, in the same branch. Two more lines: the subtraction, then the bar.",
                "`jar[\"honey\"] = jar[\"honey\"] - 2` reads the old value on the right and stores the new one on the "
                "left.",
                "Write `hero[\"mana\"] = hero[\"mana\"] - spell[\"mana_cost\"]`, then `show_mana(hero)` under it.",
            ],
            checks=[
                blank_cast_check("the mana bar updates after a cast", _BAR_UPDATES, **_BAR_MSGS),
                blank_cast_check("the spell's own cost is used", _OWN_COST, **_OWN_COST_MSGS),
            ],
            pass_line="Mar'tu: From a blank page. The book and the barrier, every line yours.",
        ),
    ],
    solution=BLANK_SOLUTION,
    partials=[
        _blank(store=""),
        _blank(),
        _blank(cast=""),
        _blank(cast=BLANK_READ + '    spell["effect"](hero)\n'),
        _blank(cast=BLANK_READ + f"    if {AFF_TEST}:\n" + SKILL_MSG + '    else:\n        spell["effect"](hero)\n'),
        _blank(cast=BLANK_READ + _cast_body(mana='hero["mana"] <= spell["mana_cost"]', pay="", show="")),
        _blank(cast=BLANK_READ + _cast_body(pay="", show="")),
    ],
    assemble=dict(
        lines=[line for line in BLANK_SOLUTION.splitlines() if line.strip()],
        distractors=['    spell_book["spell_name"] = spell', '        "effect": effect(hero),',
                     '    elif hero["mana"] <= spell["mana_cost"]:', '        spell["effect"]'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The campaign's order",
            text=(
                "1. `learn_spell`: build `spell` from the matching parameters.\n"
                "2. Store it: the book, by the name.\n"
                "3. `cast`: ask the book with `not in`; a message, then `return`.\n"
                "4. Get the page. Compare the affinity, then the mana, with `<`.\n"
                "5. `else`: cast, pay, show."
            ),
        ),
        dict(
            angle="picture",
            label="Two functions, one book",
            text=(
                "```text\nlearn_spell(book, name, ...)\n  spell = {...}\n  book[name] = spell\n\n"
                "cast(hero, name)\n  name not in book?\n    -> say so, return\n  spell = the page\n"
                "  affinity low? -> not skilled\n  mana low? -----> need mana\n  else: cast, pay, show\n```"
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen both",
            text=(
                "These are `add_spell` and `cast_spell`, with our names. In the lesson you filled them in: the "
                "placeholders, the store, the branches. Here the page starts blank, and every line is yours."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet="spell_book[spell_name] = spell",
        why=(
            "You've seen this line end `add_spell`, and `cast_spell` hold the barrier. Now you wrote both from a "
            "blank page."
        ),
    ),
    takeaway=(
        "From blank: build the page from matching parameters and store it by name; then guard with `return`, "
        "compare with `<`, and cast with `spell[\"effect\"](hero)`."
    ),
    wrong_answers=[
        dict(why="the starter (only the commented tests)", code=BLANK_STARTER, fails_at=1,
             message_contains="Write `learn_spell` with `def`"),
        dict(why="the tests uncommented before anything is written", code="".join(l + "\n" for l in BLANK_TESTS),
             fails_at=0, message_contains="name 'learn_spell' is not defined"),
        dict(why="literal test values typed in (the class's biggest slip)",
             code=_blank(spell='    spell = {"mana_cost": 6, "required_affinity": 9, "effect": lantern_ward}\n'),
             fails_at=1, message_contains="not a typed 6"),
        dict(why="the parameter quoted inside the dict ({\"mana_cost\": \"mana_cost\"})",
             code=_blank(spell=BLANK_SPELL.replace(": mana_cost,", ': "mana_cost",')), fails_at=1,
             message_contains="Take the quotes off `mana_cost`"),
        dict(why="an approximate key the game doesn't read (\"magic\")",
             code=_blank(spell=BLANK_SPELL.replace('"required_affinity":', '"magic":')), fails_at=1,
             message_contains='"magic"`, and the game reads'),
        dict(why="a key left out",
             code=_blank(spell=BLANK_SPELL.replace('        "effect": effect,\n', "")), fails_at=1,
             message_contains='Give `spell` the key `"effect"`'),
        dict(why="the effect called inside the dict (a function passed WITH ())",
             code=_blank(spell=BLANK_SPELL.replace('"effect": effect,', '"effect": effect(spell_book),')),
             fails_at=1, message_contains="Take the `()` off"),
        dict(why="the parameters in another order",
             code=_blank(head="def learn_spell(spell_name, spell_book, mana_cost, required_affinity, effect):\n"),
             fails_at=1, message_contains="five parameters, in this order"),
        dict(why="CP2 return instead of storing in the dict passed in (the caller won't see it)",
             code=_blank(store="    return spell\n"), fails_at=2, message_contains="`return` hands"),
        dict(why="CP2 the variable key in quotes", code=_blank(store='    spell_book["spell_name"] = spell\n'),
             fails_at=2, message_contains='"spell_name"'),
        dict(why="CP2 a new dictionary inside the function", code=_blank(store="    spell_book = {spell_name: spell}\n"),
             fails_at=2, message_contains="new dictionary inside the function"),
        dict(why="CP2 one shared spell for every call",
             code=('spell = {}\n\n\n' + LEARN_SIGNATURE + '    spell["mana_cost"] = mana_cost\n'
                   '    spell["required_affinity"] = required_affinity\n    spell["effect"] = effect\n'
                   + LEARN_STORE + "\n\n" + BLANK_STARTER),
             fails_at=2, message_contains="its own dictionary"),
        dict(why="CP3 no guard: the page read first (KeyError on an unknown name)",
             code=_blank(cast="").replace(BLANK_GUARD, "def cast(hero, spell_name):\n" + BLANK_READ), fails_at=3,
             message_contains="Ask the book first"),
        dict(why="CP3 a guard with no return (Python reads a page that isn't there)",
             code=_blank(cast=BLANK_READ).replace("        return\n", ""), fails_at=3,
             message_contains="Add `return` under the message"),
        dict(why="CP3 the early return placed after the work",
             code=_blank(cast=BLANK_READ + _cast_body() + "    return\n").replace("        return\n", "", 1),
             fails_at=3, message_contains="Add `return` under the message"),
        dict(why="CP3 return at the function's own level, with the cast under it (ends every cast)",
             code=_blank(cast=BLANK_READ + _cast_body()).replace("        return\n", "    return\n", 1), fails_at=3,
             message_contains="Indent `return`"),
        dict(why="CP3 a guard that prints nothing",
             code=_blank(cast="").replace('        print(hero["name"], "doesn\'t know", spell_name)\n', ""),
             fails_at=3, message_contains="Print a message"),
        dict(why="CP3 the campaign's parameter name caster",
             code=_blank(cast="").replace("def cast(hero, spell_name):", "def cast(caster, spell_name):"),
             fails_at=3, message_contains="two parameters, in this order"),
        dict(why="CP4 spell[\"effect\"] with no (hero): nothing happens",
             code=_blank(cast=BLANK_READ + '    spell["effect"]\n'), fails_at=4, message_contains="Add `(hero)`"),
        dict(why="CP4 lantern_ward called by name", code=_blank(cast=BLANK_READ + "    lantern_ward(hero)\n"),
             fails_at=4, message_contains="by name"),
        dict(why="CP4 the wrong sheet: lucky read inside cast",
             code=_blank(cast=BLANK_READ + '    spell["effect"](lucky)\n'), fails_at=4, message_contains="uses `lucky`"),
        dict(why="CP5 the if added above the cast, no else",
             code=_blank(cast=BLANK_READ + f"    if {AFF_TEST}:\n" + SKILL_MSG + '    spell["effect"](hero)\n'),
             fails_at=5, message_contains="Put `else:` above your cast"),
        dict(why="CP5 a typed affinity", code=_blank(cast=BLANK_READ + _cast_body(
             aff='hero["abilities"]["magical_affinity"] < 9')), fails_at=5, message_contains="not a typed number"),
        dict(why="CP5 <= on the affinity", code=_blank(cast=BLANK_READ + _cast_body(aff=AFF_TEST.replace("<", "<="))),
             fails_at=5, message_contains="Exactly enough affinity"),
        dict(why="CP5 two ifs instead of if / elif",
             code=_blank(cast=BLANK_READ + f"    if {AFF_TEST}:\n" + SKILL_MSG + f"    if {MANA_TEST}:\n" + MANA_MSG
                         + '    else:\n        spell["effect"](hero)\n' + PAY + "        show_mana(hero)\n"),
             fails_at=5, message_contains="last branch"),
        dict(why="the cost read from the hero's sheet, not the spell's (the wrong sheet: KeyError at the first cast)",
             code=_blank(cast=BLANK_READ + _cast_body(mana='hero["mana"] < hero["mana_cost"]')), fails_at=4,
             message_contains="Read the spell's numbers from its page"),
        dict(why="the mana read from the spell's page, not the hero's (the wrong sheet: KeyError at the first cast)",
             code=_blank(cast=BLANK_READ + _cast_body(mana='spell["mana"] < spell["mana_cost"]')), fails_at=4,
             message_contains="Read the hero's own values from the hero's sheet"),
        dict(why="CP7 <= on the mana", code=_blank(cast=BLANK_READ + _cast_body(mana='hero["mana"] <= spell["mana_cost"]')),
             fails_at=7, message_contains="use `<`, not `<=`"),
        dict(why="CP8 the subtraction never stored",
             code=_blank(cast=BLANK_READ + _cast_body(pay='        hero["mana"] - spell["mana_cost"]\n')), fails_at=8,
             message_contains="Store the new mana back"),
        dict(why="CP8 show_mana missing", code=_blank(cast=BLANK_READ + _cast_body(show="")), fails_at=8,
             message_contains="Call `show_mana(hero)`"),
        dict(why="CP8 a typed cost", code=_blank(cast=BLANK_READ + _cast_body(pay=TYPED_PAY_8)), fails_at=8,
             message_contains="not a typed 6"),
        dict(why="a test line hands the ward over WITH (): lantern_ward(lucky) stores None, then the cast crashes",
             code=BLANK_SOLUTION.replace("6, 9, lantern_ward)", "6, 9, lantern_ward(lucky))"), fails_at=0,
             message_contains="'NoneType' object is not callable"),
    ],
    notes=(
        meta(starter_level="S0", path="pool", skills="dict-from-params,store-by-name,early-return,call-stored-func,"
                                                      "elif-chain,boundary,dict-write",
             solo="false", dictates="", foreign_names="size,shelf,label,jar,item,pack,tool,sheet,jar,honey",
             campaign_link="spell-book", par='("Frost Veil", 5, 7, spark),("Moon Step", 11, 4, glimmer); Brakka '
                                             'at affinity 6-12, Moon Step, Star Fall (not in the book)') + "\n"
        "Optional advanced challenge (teacher's revision, for the ready-to-stretch group; 12 min, costs no one "
        "core time), after the project, modelled on Unit 5's barrier-from-blank. Setup: the roster (each book "
        "holds Glow), `lantern_ward`, `light_lantern` and `show_mana` (BOOK_SETUP plus show_mana). The starter is "
        "only the three commented test calls. The checkpoints reuse 6C-04's and 6C-05's check bodies with the "
        "same messages, except where the starter's own lines are named (keep the def -> write the def; 'as the "
        "starter has it' -> 'give spell the key'): CP1 _SPELL_BUILT, CP2 _SPELL_STORED + _SECOND_KEEPS_FIRST, CP3 "
        "a new guard check (an unknown name prints, spends nothing and does not crash; a missing `return`, a "
        "`return` after the work, and a `return` at the function's own level with lines under it are each named), "
        "CP4 _CASTS, CP5-CP7 _TURNS_AWAY (low affinity, low mana, exactly enough), CP8 _BAR_UPDATES + _OWN_COST. "
        "No Show me line holds a whole function: each last hint gives one or two lines. Every check calls the "
        "student's functions inside the check with fresh values (Frost Veil, Moon Step, Brakka, Star Fall), so a "
        "test line left commented never matters, and a typed 6 or 9 fails."
    ),
)


# =============================================================================================
# Items, in the order students see them (after Lesson 6B in u07a)
# =============================================================================================

ITEMS = [REMEMBERS_6C, LESSON_6C, QUIZ_6B, THE_RESONANCE_ARRAY, BOOK_FROM_BLANK]
