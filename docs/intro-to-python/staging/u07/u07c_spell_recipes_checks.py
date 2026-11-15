"""Unit 7 "Functions II" ("Spells You Can Hand Over"), part c: Extra practice 7X (6B-08 defaults-and-names, 6B-09
inside-stays-inside), the optional articles 6-A1 "lambda", 6-A2 "map()" and 6-A3 "Two Things Back" (one try-it each),
Quick Check Recipes II (forms qc-r2-a and qc-r2-b, four code tasks each, as testout items, with their question forms
qc-r2-a-questions and qc-r2-b-questions as optional quiz items) and the cheatsheet "Mar'tu's Chalk Notes: Spell
Recipes".

Spec: design/curriculum.md, "## Unit 7 · Functions II", items 5 to 8 (u07c): "### Extra practice 7X [pool] and the
optional articles", "### Quick Check Recipes II" and "### Cheatsheet: Spell Recipes".
Introduces exactly what concept_map.json plans for u07c: node:DefaultArg and node:KeywordArg (6B-08, pool only),
node:Lambda (6-A1) and call:map (6-A2), optional only. Everything else comes from earlier units: `def` / `return` /
`pass` (Unit 3), lists, `in`, `.append`, `list()` and tuples (Unit 4; node:Tuple is 3-A1's, optional, and 6-A3 carries
the recap card the spec asks for), dictionaries and `not in` (Unit 5), `None` (u07b's 6C-04), and from Unit 6 (planned
concepts only, u06a: `for` over a list or a list of dicts) in the articles' loops and `run_array`. No `while`,
`continue`, comprehensions, `.items()`, f-strings or escapes in any code a student sees. The Quick Check uses core
tokens only (no defaults, lambdas, `map` or tuples).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN `perform_roll(die_size)`
(skill-checks), `strengthen_magic` handed to `add_spell(...)` with no `()` (spell-book), `show_mana` storing
`get_mana_bar(caster)` and passing it to the finished `print_mana` (mana-bars), and `cast_spell`'s guard and
`spell["spell_function"](caster)` (hold-the-barrier). Every campaign link is "you've seen this, now you'll get it".
The Quick Check is framed as "it only shows Mar'tu where to start", never as a test of what they should know. Every
student has their own device; pair talk is optional and every checkpoint is solo.

Terminology (2.9): "function" in all plain text, checks and messages ("recipe" only in Mar'tu's kitchen pictures);
"parameter", "argument", "returns", "variable", "key"; "matching" means an exact name. The quotes sentence word for word.

Help ladder as fields (FORMAT.md, the Unit 2 fix pass, as u07a/u07b): hints[0] Where to look, the middle hints Teach me
(a tiny example with other names, listed in foreign_names), the last hint Show me how: the step's own line in
backticks, whose start up to its first `(` or `=` is Start me off (always a start Mar'tu's version uses; no hint 1 is a
"Start like this"). 3 or 4 hints per checkpoint, then another_way (2 to 4 angles), assemble (More structure) on every
exercise, and the solution (Compare). Quick Check exercises are support="none" and explainer="lean"; their hints are
written because the schema needs them and never hold a finished line.

Check codes (curriculum 2.5), built from the _PX helpers below. check() puts in front of each check only the helpers it
uses (as u07a does). Every call a check makes uses fresh values the task never uses (lint b), with prints kept private;
nothing a check does shows in the console, and the student's own sheets are never touched:
  RND      6B-08: `random.randint` is swapped for a scripted die that records what it was asked and rolls one below the
           top face; `roll_die()`, `roll_die(8)` and `roll_die(die_size=12)` (a typed 20, `die_size = 20` inside, the
           parameter taken out, `print` for `return`); the named d6 is found in the AST, then a rerun must print 5,
           and the line that prints must hold the named call (a d6 printed by position beside an unshown named one
           fails).
  RET / PAR / PAR-CONST  6B-09 (`rest` on Pell 3/10 and Brakka 13/22, never the task's 6), 6-A1 (the lambda on
           affinities 7 and 4), 6-A2 (`get_mana`), 6-A3 (`bar_parts` must return the pair), QC C1 (the local `ward`,
           read from the frame as the call returns), QC C3 CP1 (the student's own `build_bar` on Pell, mana 7, and
           Moss, mana 3: a typed bar or `oogrish` can't give both).
  CMB      `_rerun()` runs the program again in a fresh namespace (setup, then a replaced roster or a line slipped in
           after `lucky = ...`): the lambda dial, `names` / `manas` and the bar must follow; a typed value fails. 6-A3's
           bar reruns with an invented sheet (Pell, 7 of 12) put in `lucky`, so a typed 20, 6 or 26 can't follow it.
  KEY / SWAP  QC C1: near-miss keys (`"cost"`, capitals, the campaign's `"spell_function"`), keys with no quotes, a
           quoted parameter, swapped values; `wards["ward_name"]`, a typed name, a rebinding, `return` for a store.
  VAL      QC C1 CP3: after the program runs, the book's own page holds the function itself as its effect (still
           the 0, a name in quotes, `None` from a call, another function: each named).
  CALL     QC C2 (an unknown name must leave the mana alone and must not print the work's own `Raised:` line; the
           AST names why: no guard, the guard after the work, an if/else that falls through, no `return`, a typed
           name, `in` for `not in`, `return` outside the `if`; an if/else that keeps the work under `else` behaves
           like a guard and passes), QC C3 CP3
           (the helper swapped for a pretend one that only writes down what it is handed: once, (hero, bar), in that
           order), QC C4 (recorder effects in a fresh book: the page under the name handed in, once, on the hero
           handed in).
  STO      QC C3 CP2: a variable inside `show_row` holds this hero's bar (the function itself, the outer sheet, a typed
           bar and a call passed straight on each get named); CP3: `draw_row` must be handed a variable made inside
           `show_row` (a new call, or a bar built right in the call, fails).
  KEEP     6-A1 (`run_array`) and QC C3 (the finished `draw_row`; `build_bar` is the student's own), an AST compare
           with the starter's own copy.
  NOP      the function handed over with `()`, one call's result handed over, the name in quotes: Python's own errors
           at the call (the explainer's rows), each proven by a wrong answer (6-A1, 6-A2, QC C1 CP3).
Messages outside the Quick Check: the fix first, then what happened, then the evidence in brackets, "(Mar'tu's check
called `rest` with a sheet for Pell, mana 3 of 10, only inside the check: it printed 7, then returned `None`.)".
Quick Check messages are lean (the Unit 2 ruling, as QC2's `_leaned`): the slip and the evidence, never the fix
("With a name Pell doesn't know, there is no `return` under the guard, so the function carried on: Pell's mana still
went down, from 10 to 7."). Invented Tor names only in check data (Pell, Brakka, Moss, Frost Veil, Moon Step, Rust Ward,
Glimmer, Glow, Ember Wall); the party table's real values for the heroes (max mana 18, 20, 24, 26; affinity 9, 10, 12,
13). A student's own text is never repeated back: text values show as "some text", and a typed page name is named only
when it is one of the starter's own.

The class's slips for this unit, each proven by a wrong_answers entry (in the exercise named):
  * a function that must return a value returns nothing (print inside, no return, `pass`): 6B-08, 6B-09 CP2, 6-A1,
    6-A2 CP2, 6-A3 CP1, QC C3 CP1 (`pass`, print for return), Q2; thinking the caller won't see a change, so it is
    returned instead: QC C1 CP2 (`return ward`), QC C4 CP2 (`return hero["mana"] - ...`, or the new mana kept in a
    local variable), the rebinding `wards = {...}` (C1 CP2), Q3;
  * keys that don't exactly match the names the reader uses: 6-A1 (`hero["magic"]`), 6-A2 (`"Mana"`), QC C1 (`"cost"`,
    `"Mana_Cost"`, `"spell_function"`), Q4 (a KeyError);
  * a parameter quoted inside the dict or as a key (`"mana_cost": "mana_cost"`, `wards["ward_name"]`, `"ward_name" not
    in ...`, `wards["name"]`): QC C1 (CP1 and CP2), C2, C4;
  * typed test values instead of the parameters (still the biggest slip: A-06/A-07): 6B-08 (a typed 20), 6B-09
    (`return 6`, `gained = 6`, Lucky's 20 or 26 typed inside `rest`), 6-A1 (`lambda hero: 26`), 6-A2 (typed names and
    manas), 6-A3 (`return 20, 6`, a typed bar, `26 - full`), QC C1 (4, `ash_ward`, a second page under the starter's
    name), C2 (the starter's name in the `if`), C3 (a typed bar, in `build_bar` and in `show_row`), C4 (a typed
    cost); copying the Example's names instead: 6B-08 (`count`), 6B-09 (`tea`), 6-A2 (`get_name`'s key left in
    `get_mana`, step 1's `get_name` handed over again), 6-A3 (`share, spare`);
  * an early return in the wrong place, or a guard that never returns: QC C2 (after the work, if/else, an if/else with
    only the mana line under `else`, no `return`, `return` outside the `if`) and 6B-09 (`return` above the refill, so
    the refill never runs; `return` not indented);
  * a helper called with the wrong number or order of values, or edited: QC C3 (swapped, too few, too many, edited),
    6-A1 (`run_array(max_mana_dial, roster)`, `run_array` edited), 6-A2 (`map(roster, get_name)`);
  * a function handed over WITH `()` (it runs now: a missing argument, or its result handed over): 6-A1
    (`max_mana_dial()`, `max_mana_dial(lucky)`), 6-A2 (`get_name()`, `get_mana(lucky)`), QC C1 (`effect()`; CP3:
    `ash_ward()`, `ash_ward({...})`, `"ash_ward"`, the 0 left), Q1 (the NoneType row in its explanation);
  * the stored effect read without `(hero)`: QC C4 CP1 ("nothing calls it");
  * the result of a call stored where the function was wanted: 6-A1 (`max_mana_dial = lucky[...] * 2`), QC C4
    (`effect = wards[name]["effect"](hero)`, then `effect(hero)`: 'NoneType' object is not callable); the reverse,
    the function stored where its result was wanted: 6B-09 (`gained = rest`), QC C3 (`bar = build_bar`), 6-A3
    (`full, empty = bar_parts`);
  * reading or writing the wrong sheet: the outer sheet for the parameter (6-A1, 6-A2, 6-A3, QC C3, QC C4), the cost
    read from the hero's sheet and the mana read from the page (QC C4 CP2, KeyErrors), the page's cost written instead
    of the hero's mana (QC C4 CP2);
  * skipping the step's point while the output still looks right: 6B-08 (the named d6 never printed), 6-A3 (both
    values caught, then the bar read off the sheet again), QC C3 (stored, then a hand-built bar passed on).

Deviations from the spec, each small and noted on its item:
  * 6B-09's two steps run in the order that shows progress on every Run: catch the value first (it shows `None`), then
    `return restored`. The spec's NameError predict comes first, on the starter.
  * Quick Check Recipes II (the Unit 5 "honest fast path" ruling, tightened by the teacher's Unit 7 review): C3 also
    carries objective 1 (CP1: the student's own `build_bar` must `return` the bar, the class's biggest slip) and
    objective 6 (store-then-pass, the mana-bars shape), C1 a third checkpoint that hands the effect over with no
    `()` (func-as-value in code, not only in Q1), and C4 a second checkpoint that pays the cost (objective 2 in
    code, not only in Q3), so the code tasks alone cover every objective. C1 and C3 have three checkpoints each,
    C4 two. The forms take 16 minutes (was 12, then 14).
  * The question forms hold four questions (the spec's Q1-Q3, plus Q4: keys must match exactly) and
    questions_to_pass=3, as Unit 2's QC2.
  * QC C2's work spends a fixed cost per ward ("Every ward costs 3 mana."), so a guard that lets an unknown name
    through shows in the mana, not as a crash (the spec's "no return -> it carries on (CALL)").
  * QC C3's finished `draw_row` calls a hidden panel recorder that takes either order (as the campaign's
    `party.show_mana_bar`), so swapped values reach the CALL check instead of crashing in the helper.
  * Each Quick Check task's "Stuck?" line names the one or two exercises that teach its skill, and their lesson,
    never "a whole lesson". The last pass line adds two sentences of the story (the resonance array's dials) for
    students who test out and miss 6P.

Python's messages were checked in CPython 3.13 (the site runs 3.13): `def roll_die(die_size == 20):` and `def
roll_die(20):` -> "invalid syntax"; `roll_die("die_size"=6)` -> "expression cannot contain assignment, perhaps you meant
"=="?"; `roll_die(size=6)` -> "got an unexpected keyword argument 'size'"; `random.randint(1, "20")` -> "can only
concatenate str (not "int") to str"; `lambda hero: return ...` -> "invalid syntax"; `map(roster, get_name)` ->
"'function' object is not iterable"; `full = bar_parts(lucky)` then `"█" * full` -> "can't multiply sequence by non-int
of type 'tuple'"; `full, empty = bar_parts` -> "cannot unpack non-iterable function object"; three names for two
values -> "not enough values to unpack (expected 3, got 2)"; `wards[ward] = ward_name` -> "unhashable type: 'dict'".

Phone width: fenced pictures, examples, predict and quiz code, cheatsheet code and starter lines keep to 36 characters,
except the campaign's own shapes (checked by script): the `add_spell`-style `def learn_ward(wards, ward_name,
mana_cost, effect):` signature and its bottom call, the `cast_ward(...)` call line, and `perform_roll`'s
`return random.randint(1, die_size)`. QC C1's comment 3 keeps the teacher's words, wrapped at 36 so form B's
`teal_shield` fits.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u07c
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
# Check helpers (plain Python, run in the student's namespace after their code). check() puts in front of each
# check only the helpers it uses, and the helpers those use, so the unit JSON stays small (as u07a does).
# ---------------------------------------------------------------------------------------------

_PX = r'''import ast as _ast
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
        return 'a lambda' if _v.__name__ == '<lambda>' else 'the function `' + _v.__name__ + '`'
    if _t in ('int', 'float', 'bool'):
        return '`' + str(_v) + '`'
    if _t == 'str':
        return 'some text'
    return {'dict': 'a dictionary', 'list': 'a list', 'tuple': 'a tuple'}.get(_t, 'a ' + _t)


def _ev(_what, _said=''):
    return " (Mar'tu's check " + _what + ', only inside the check' + ((': ' + _said) if _said else '') + '.)'


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
    # A near miss for a name or a key: case, spaces, a plural, 1-2 edits, a shared word, or one inside the other.
    if type(_a).__name__ != 'str' or type(_b).__name__ != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower().replace(' ', '_'), _b.lower().replace(' ', '_')
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
        return 'no parameters'
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _params(_f):
    _c = getattr(_f, '__code__', None)
    return list(_c.co_varnames[:_c.co_argcount]) if _c is not None else []


def _defaults(_f):
    _ps = _params(_f)
    _d = getattr(_f, '__defaults__', None) or ()
    return dict(zip(_ps[len(_ps) - len(_d):], _d))


def _defs():
    return {_n.name: _n for _n in _tree.body if type(_n).__name__ == 'FunctionDef'}


def _top():
    return [_n for _n in _tree.body if type(_n).__name__ != 'FunctionDef']


def _calls_in(_nodes, _name):
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
            and type(_c.func).__name__ == 'Name' and _c.func.id == _name]


def _made_by(_n):
    # The names a statement makes with `=`, `+=` or `def`, unpacked names included.
    _k = type(_n).__name__
    if _k in ('FunctionDef', 'ClassDef'):
        return [_n.name]
    _ts = list(_n.targets) if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'AnnAssign') else [])
    return [_x.id for _t in _ts for _x in _ast.walk(_t) if type(_x).__name__ == 'Name' and type(_t).__name__ != 'Subscript']


def _find(_name, _lean=False):
    # The student's function `_name`, or the message that says why it isn't there.
    _v = _g.get(_name)
    if callable(_v) and type(_v).__name__ == 'function':
        return _v, ''
    if _name in _g:
        return None, ('`' + _name + '` is not a function: a line with `=` put a value in it.' if _lean else
                      '`' + _name + '` is a variable now. Make it with `def`: a line that starts `def ' + _name + '(`.')
    _near = sorted(_k for _k, _x in list(_g.items()) if type(_x).__name__ == 'function' and not _k.startswith('_')
                   and _close(_k, _name))
    if _near:
        return None, 'Python matches names letter for letter: you wrote `' + _near[0] + '`, the task needs `' + _name + '`.'
    if _lean:
        return None, 'No function called `' + _name + '` was made.'
    return None, 'Keep the function `' + _name + '` from the starter, with its `def` line.'


def _need(_name, _want, _lean=False):
    _f, _m = _find(_name, _lean)
    assert _f, _m
    _ps = _params(_f)
    if _lean:
        assert _ps == _want, ('The `def` line of `' + _name + '` has ' + _names(_ps) + ', and the starter has '
                              + _names(_want) + '.')
    else:
        assert _ps == _want, ('Keep the parameters from the starter: `def ' + _name + '(' + ', '.join(_want) + '):`. '
                              'Python matches names letter for letter.')
    return _f


def _call(_f, _args=(), _kw=None):
    # Call _f with its prints kept private. Returns (value, printed lines, error or None).
    _buf = _io.StringIO()
    _keep_out = _sys.stdout
    _sys.stdout = _buf
    _val, _e = None, None
    try:
        _val = _f(*_args, **(_kw or {}))
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _e


def _capture(_f, _args=(), _kw=None):
    # Like _call, and also the function's own variables as it returns (read from its frame, not from the text).
    _box = {}
    _code = getattr(_f, '__code__', None)

    def _prof(_fr, _evt, _arg):
        if _evt == 'return' and _fr.f_code is _code:
            _box['l'] = dict(_fr.f_locals)

    _old = _sys.getprofile()
    _sys.setprofile(_prof)
    try:
        _val, _rows, _e = _call(_f, _args, _kw)
    finally:
        _sys.setprofile(_old)
    return _box.get('l', {}), _val, _rows, _e


def _stubbed(_f, _args, _name):
    # Call _f with the helper `_name` swapped for a recorder, only inside the check.
    _G = _f.__globals__
    _rec = []
    _had = _name in _G
    _real = _G.get(_name)

    _ps = _params(_real) if _real is not None else []

    def _fake(*_a, **_k):
        _rec.append(tuple(_a) + tuple(_k[_p] for _p in _ps[len(_a):] if _p in _k))

    _G[_name] = _fake
    try:
        _val, _rows, _e = _call(_f, _args)
    finally:
        if _had:
            _G[_name] = _real
        else:
            _G.pop(_name, None)
    return _val, _rows, _e, _rec


def _keep(_name, _orig):
    # KEEP: '' when the function is exactly the starter's (comments aside), else 'gone' or 'changed'.
    _d = _defs().get(_name)
    if _d is None:
        return 'gone'
    _o = [_n for _n in _ast.parse(_orig).body if type(_n).__name__ == 'FunctionDef' and _n.name == _name][0]
    return '' if _ast.dump(_d) == _ast.dump(_o) else 'changed'


def _die(_log, _half=False):
    # A scripted randint: records what it was asked, and rolls one below the top face (a d6 rolls 5), or, with
    # _half, half the top face (a d6 rolls 3, a d20 rolls 10), so a typed number can't follow both dice.
    def randint(_a, _b):
        _log.append((_a, _b))
        if type(_a).__name__ == 'int' and type(_b).__name__ == 'int' and _b > _a:
            return _b // 2 if _half else _b - 1
        return _a
    return randint


def _rolled(_f, _args=(), _kw=None):
    _log = []
    _real = _random.randint
    _random.randint = _die(_log)
    try:
        _val, _rows, _e = _call(_f, _args, _kw)
    finally:
        _random.randint = _real
    return _val, _rows, _e, _log


def _rerun(_changes=(), _pre='', _roll=False):
    # The program again in a fresh namespace: setup, then _pre, then the student's code, prints kept private.
    # Each change's line runs right after the first top-level statement of the student's code that makes its name.
    _body, _found = [], []
    for _code, _mine in ((_SETUP, False), (_pre, False), (_source, True)):
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
    _log = []
    _real = _random.randint
    _out, _keep_out, _e = _io.StringIO(), _sys.stdout, None
    _sys.stdout = _out
    if _roll:
        _random.randint = _die(_log, _roll == 'half')
    try:
        exec(compile(_mod, 'main.py', 'exec'), _ns)
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
        _random.randint = _real
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _e, [_a for _a, _l in _changes if _a not in _found], _log


def _words(_l):
    # A printed line split into words, with the marks around them dropped (for "is 5 on this line?").
    return [_w.strip('.,:;!?()[]"' + "'") for _w in _l.split()]
'''


def _px_parts():
    """_PX split into its setup lines and its helper functions, each with the helper names it uses."""
    import ast

    tree = ast.parse(_PX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_PX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_PX_HEAD, _PX_DEFS = _px_parts()


def check(label, body, setup="", **values):
    """(label, code): the _PX setup lines, the helpers this check uses (and the helpers those use), then the body."""
    import re

    code = fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _PX_DEFS and name not in need:
            need.add(name)
            todo |= _PX_DEFS[name][1]
    head = "\n".join(_PX_HEAD).replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))
    helpers = [text for name, (text, _) in _PX_DEFS.items() if name in need]
    return (label, head + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + code.strip("\n") + "\n")


# =============================================================================================
# UNIT (repeated in every part file of spell-recipes; copied verbatim from u07a / u07b, so the parts agree)
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
    campaign_links=["friends-in-low-places"],
)

# Only the terms this file is first to link. Every other [[link]] here (recipe/function, parameter, argument,
# return, None, guard, helper, matching parameter, same sheet, function as a value, tuple, NameError, KeyError,
# TypeError, dictionary, key) is defined in an earlier unit or part.
GLOSSARY = [
    dict(
        term="default value",
        aliases=["default", "defaults", "default values", "default argument"],
        plain=(
            "A value a parameter takes when the call hands over nothing for it. It is written on the `def` line "
            "with `=`. A value handed over in the call wins."
        ),
        example="def roll_die(die_size=20):",
    ),
    dict(
        term="keyword argument",
        aliases=["keyword arguments", "named argument", "by name"],
        plain=(
            "A value handed over with its parameter's name in front: `roll_die(die_size=6)`. With names, the order "
            "of the values doesn't matter."
        ),
        example="roll_die(die_size=6)",
    ),
    dict(
        term="scope",
        aliases=["inside stays inside", "local variable", "local variables"],
        plain=(
            "Where a name can be seen. A function's parameters, and the variables made inside it, live only inside "
            "that function while it runs. Outside, Python has never heard of them."
        ),
        example="def rest(hero):\n    restored = 6\n\nprint(restored)   # NameError",
    ),
    dict(
        term="lambda",
        aliases=["lambdas"],
        plain=(
            "A one-line function with no name and no `return`: `lambda n: n * 2`. Before the colon are the "
            "parameters. After it is the value it returns."
        ),
        example="double = lambda n: n * 2",
    ),
    dict(
        term="map()",
        aliases=["map"],
        plain=(
            "Calls a function on every item of a list, and collects what each call returns. Hand it the function "
            "with no `()`, then the list. Wrap it in `list()` to see the results."
        ),
        example="list(map(double, [2, 6]))   # [4, 12]",
    ),
    dict(
        term="unpacking",
        aliases=["unpack", "unpacks"],
        plain=(
            "Catching the values of a tuple in names, one name for each value, in order: `share, spare = (4, 1)`."
        ),
        example="share, spare = split_loot(17, 4)",
    ),
]

# The party table (curriculum 1.2): max_mana is 2 x magical_affinity.
PARTY = [
    # var, name, max_mana, affinity
    ("oogrish", "Oogrish", 18, 9),
    ("gearshift", "Gearshift", 20, 10),
    ("bomb_shell", "Bomb Shell", 24, 12),
    ("lucky", "Lucky", 26, 13),
]


def _roster_setup(extra=""):
    """Hidden setup: the four heroes' sheets (real party values, full mana) and `roster`."""
    out = extra
    for var, name, mana, affinity in PARTY:
        out += (f'{var} = {{"name": "{name}", "mana": {mana}, "max_mana": {mana}, '
                f'"magical_affinity": {affinity}}}\n')
    return out + "roster = [oogrish, gearshift, bomb_shell, lucky]\n"


ROSTER_SETUP = _roster_setup()
# A fresh roster for reruns (invented Tor names; set after setup, before the student's code).
OTHER_ROSTER = (
    'roster = [{"name": "Pell", "mana": 7, "max_mana": 12, "magical_affinity": 6}, '
    '{"name": "Brakka", "mana": 15, "max_mana": 16, "magical_affinity": 8}, '
    '{"name": "Moss", "mana": 3, "max_mana": 10, "magical_affinity": 5}]\n'
)


# =============================================================================================
# Extra practice 7X (pool): 6B-08 defaults-and-names, 6B-09 inside-stays-inside
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 6B-08 defaults-and-names (pool): introduces node:DefaultArg and node:KeywordArg. RND.
# ---------------------------------------------------------------------------------------------

ROLL_PLAIN = "def roll_die(die_size):\n    return random.randint(1, die_size)\n"
ROLL_GOOD = "def roll_die(die_size=20):\n    return random.randint(1, die_size)\n"
ROLL_STEP1 = "# 1. Give die_size a default of 20.\n"
ROLL_STEP2 = "# 2. Roll a d6, naming the value:\n#    die_size=6.\n"
ROLL_D6 = "print(roll_die(die_size=6))\n"


def _roll(defn=ROLL_PLAIN, first="print(roll_die())\n", second=""):
    return "import random\n\n\n" + defn + "\n\n" + ROLL_STEP1 + first + "\n" + ROLL_STEP2 + second


ROLL_STARTER = _roll()
ROLL_SOLUTION = _roll(ROLL_GOOD, second=ROLL_D6)
assert ROLL_STARTER == (
    "import random\n"
    "\n"
    "\n"
    "def roll_die(die_size):\n"
    "    return random.randint(1, die_size)\n"
    "\n"
    "\n"
    "# 1. Give die_size a default of 20.\n"
    "print(roll_die())\n"
    "\n"
    "# 2. Roll a d6, naming the value:\n"
    "#    die_size=6.\n"
)
LAMPS_EXAMPLE = (
    "def light_lamps(count=3):\n"
    '    print("Lamps lit:", count)\n'
    "\n\n"
    "light_lamps()\n"
    "light_lamps(count=5)\n"
)

_ROLL_NEED = r'''
_f, _m = _find('roll_die')
assert _f, _m
assert _params(_f)[:1] == ['die_size'], (
    'Keep `die_size` as the parameter of `roll_die`, and give it its default there: `def roll_die(die_size=20):`.'
    + ('' if _params(_f) else ' Right now `roll_die` takes no values, so `roll_die(8)` has nowhere to put the 8.'))
'''

_ROLL_DEFAULT = _ROLL_NEED + r'''
_d = _defs().get('roll_die')
_dft = _defaults(_f)
if 'die_size' not in _dft:
    _a = _d.args.args[0] if _d is not None and _d.args.args else None
    assert not (_a is not None and _a.annotation is not None), (
        'Use `=` for a default: `die_size=20`. With a colon, `die_size: 20` is only a note about the parameter, so '
        '`roll_die()` still has no value for it.')
    assert False, ('Give `die_size` a default on the `def` line: `def roll_die(die_size=20):`. Then `roll_die()`, '
                   'with nothing in the brackets, rolls a d20.')
_v = _dft['die_size']
assert type(_v).__name__ != 'str', ('Take the quotes off the default: `die_size=20`. In quotes, 20 is text, and a '
                                    'die needs a number. ' + _QUOTES)
assert _v == 20, 'Make the default 20, for a d20: `die_size=20`. The default is ' + _show(_v) + ' now.'
_inner = [_n for _n in _ast.walk(_d) if 'die_size' in _made_by(_n)]
for _args, _kw, _want in (((), {}, 20), ((8,), {}, 8), ((), {'die_size': 12}, 12)):
    _c = '`roll_die(' + (str(_args[0]) if _args else ('die_size=' + str(_kw['die_size']) if _kw else '')) + ')`'
    _what = 'called ' + _c + ' with a scripted die'
    _val, _rows, _e, _log = _rolled(_f, _args, _kw)
    assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    assert _log, 'Roll with `random.randint(1, die_size)`, and return the roll.' + _ev(_what, 'it never rolled')
    _a, _b = _log[0]
    if _b != _want:
        assert not _inner, ('Take out the line inside `roll_die` that sets `die_size`. It throws away the value that '
                            'was handed over.' + _ev(_what, 'it rolled from 1 to ' + str(_b)))
        assert _b != 20, ('Use the parameter in the roll: `random.randint(1, die_size)`, not a typed 20.'
                          + _ev(_what, 'it rolled a d20'))
        assert False, ('Roll from 1 to `die_size`: `random.randint(1, die_size)`.'
                       + _ev(_what, 'it rolled from ' + str(_a) + ' to ' + str(_b)))
    assert _a == 1, 'Start the roll at 1: a die has no ' + str(_a) + ' face.' + _ev(_what)
    if _val != _b - 1:
        assert not (_val is None and _rows), ('Use `return` in place of `print`, so the roll goes back to the call.'
                                              + _ev(_what, 'it printed the roll, then returned `None`'))
        assert False, 'Return the roll itself: `return random.randint(1, die_size)`.' + _ev(_what, 'it returned ' + _show(_val))
'''

_ROLL_NAMED = _ROLL_NEED + r'''
def _kwv(_c, _k):
    for _x in _c.keywords:
        if _x.arg == _k:
            return _x.value
    return None
_calls = _calls_in(_top(), 'roll_die')
_named = [_kwv(_c, 'die_size') for _c in _calls if _kwv(_c, 'die_size') is not None]
_six = [_x for _x in _named if type(_x).__name__ != 'Constant' or _x.value == 6]
if not _six:
    _nums = [_x.value for _x in _named if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'int']
    assert not _nums, 'Make it a d6: `roll_die(die_size=6)`. Your call names the value, but it is ' + str(_nums[0]) + '.'
    assert not _named, 'Take the quotes off the 6: `roll_die(die_size=6)`. ' + _QUOTES
    _pos6 = [_c for _c in _calls if _c.args and type(_c.args[0]).__name__ == 'Constant' and _c.args[0].value == 6]
    assert not _pos6, ('Name the value in the call: `roll_die(die_size=6)`. `roll_die(6)` rolls a d6 too, but this step '
                       'is about the name.')
    _outside = [_n for _n in _top() if 'die_size' in _made_by(_n)]
    assert not _outside, ('Name the value inside the call: `roll_die(die_size=6)`. A variable `die_size` made outside '
                          'the function never reaches inside it, so `roll_die()` still rolled a d20.')
    assert False, 'Under step 2, roll a d6 by name and print it: `print(roll_die(die_size=6))`.'
_ns, _ls, _e, _miss, _log = _rerun(_roll=True)
_what = 'ran your program again with a scripted die that rolls 5 on a d6'
assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
assert (1, 6) in _log, 'Roll a d6 with `roll_die(die_size=6)`.' + _ev(_what, 'no d6 was rolled')
assert [_l for _l in _ls if '5' in _words(_l)], ('Print the roll: put the call inside `print(...)`.'
                                                + _ev(_what, 'the d6 rolled, but no line showed the 5'))
_ns, _ls, _e, _miss, _log = _rerun(_roll='half')
assert _e is None, 'Mend this, then Run again: ' + _err(_e)
assert [_l for _l in _ls if '3' in _words(_l)], (
    'Print the roll itself: `print(roll_die(die_size=6))`. A typed number shows the same whatever the die rolls.'
    + _ev('ran your program again with a die that rolls 3 on a d6', 'no line showed the 3'))
_ncalls = [_c for _c in _calls if _kwv(_c, 'die_size') is not None and (type(_kwv(_c, 'die_size')).__name__ != 'Constant'
                                                                     or _kwv(_c, 'die_size').value == 6)]
_held = [_x for _n in _top() if type(_n).__name__ == 'Assign' and [_c for _c in _ncalls if _c in list(_ast.walk(_n.value))]
         for _x in _made_by(_n)]
_shown = [_p for _p in _calls_in(_top(), 'print') for _a in _p.args for _x in _ast.walk(_a)
          if _x in _ncalls or (type(_x).__name__ == 'Name' and _x.id in _held)]
assert _shown, ('Print the roll you named: `print(roll_die(die_size=6))`. The d6 that printed came from a call with no '
                'name, and the named one was never shown.')
'''

_ROLL_BONUS = _ROLL_NEED + r'''
_dft = _defaults(_f)
assert _params(_f)[:2] == ['die_size', 'bonus'], ('Add the parameter `bonus` after `die_size`: '
                                                 '`def roll_die(die_size=20, bonus=0):`.')
assert _dft.get('bonus') == 0, 'Give `bonus` a default of 0: `bonus=0`.'
for _args, _kw, _want in (((), {}, 19), ((6,), {}, 5), ((), {'bonus': 3}, 22), ((8,), {'bonus': 2}, 9)):
    _c = 'roll_die(' + ', '.join([str(_x) for _x in _args] + [_k + '=' + str(_v) for _k, _v in _kw.items()]) + ')'
    _val, _rows, _e, _log = _rolled(_f, _args, _kw)
    _what = 'called `' + _c + '` with a scripted die that rolls one below the top face'
    assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    assert _val == _want, ('Add `bonus` to the roll: `return random.randint(1, die_size) + bonus`.'
                           + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_want)))
_b3 = [_c for _c in _calls_in(_top(), 'roll_die') if [_k for _k in _c.keywords if _k.arg == 'bonus']]
assert _b3, 'Print a roll with the bonus named: `print(roll_die(bonus=3))`.'
_ns, _ls, _e, _miss, _log = _rerun(_roll=True)
assert [_l for _l in _ls if '22' in _words(_l)], ('Print `roll_die(bonus=3)`: a d20, plus 3.'
                                                 + _ev('ran your program with a die that rolls 19', 'no line showed 22'))
_ns, _ls, _e, _miss, _log = _rerun(_roll='half')
assert [_l for _l in _ls if '13' in _words(_l)], ('Print the roll itself: `print(roll_die(bonus=3))`, not a typed '
                                                 'number.' + _ev('ran your program with a die that rolls 10', 'no line showed 13'))
'''

DEFAULTS_AND_NAMES = dict(
    id="defaults-and-names",
    title="Defaults and names",
    martu=(
        "Most rolls in Tor are a d20. Typing `20` every time is how slips get in, yes?\n"
        "A parameter can have a [[default value]], written on the `def` line: `def roll_die(die_size=20):`. "
        "Call `roll_die()` with nothing in the brackets, and `die_size` is 20. Hand over a value, `roll_die(6)`, "
        "and yours wins.\n"
        "You can also name the value in the call: `roll_die(die_size=6)`. That is a [[keyword argument]]. With "
        "names, Python can't mix up which value is which.\n"
        "Run the starter first. Python stops, because `roll_die()` hands over nothing yet."
    ),
    example=LAMPS_EXAMPLE,
    example_output="Lamps lit: 3\nLamps lit: 5",
    introduces=["node:DefaultArg", "node:KeywordArg"],
    names=["roll_die", "die_size"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=(
            "def pour_glug(sips=2):\n"
            '    print(sips, "sips of glug")\n'
            "\n\n"
            "pour_glug()\n"
            "pour_glug(5)\n"
        ),
        choices=[
            "2 sips of glug\n5 sips of glug",
            "2 sips of glug\n2 sips of glug",
            "5 sips of glug",
            "ERROR: pour_glug() missing 1 required positional argument: 'sips'",
        ],
        answer=0,
        explain=(
            "`pour_glug()` hands over nothing, so `sips` takes its default, 2. `pour_glug(5)` hands over 5, and the "
            "value handed over wins. No error: a parameter with a default can be left out."
        ),
    ),
    pair_talk="Tell your partner what `die_size` holds during `roll_die()`, and during `roll_die(die_size=6)`.",
    starter=ROLL_STARTER,
    checkpoints=[
        dict(
            id="default-of-20",
            text="Give `die_size` a default of 20, so `roll_die()` rolls a d20.",
            dictated=True,
            hints=[
                "Look at the `def` line. A default goes right after the parameter's name, inside the brackets.",
                "In the Example, `def light_lamps(count=3):` gives `count` the default 3. `light_lamps()` then "
                "lights 3 lamps.",
                "With `=`, not a colon. A colon there makes a note, not a default, and Python still asks for a "
                "value.",
                "Write `def roll_die(die_size=20):` in place of the `def` line.",
            ],
            checks=[check("roll_die() rolls a d20, and a value handed over wins", _ROLL_DEFAULT)],
            pass_line="Oogrish: A d20 by default. Steady, now.",
        ),
        dict(
            id="d6-by-name",
            text="Under step 2, print a d6 roll, naming the value: `print(roll_die(die_size=6))`.",
            dictated=True,
            hints=[
                "Under the comment for step 2. The name of the parameter goes inside the call's brackets, then "
                "`=`, then the value.",
                "In the Example, `light_lamps(count=5)` names the value it hands over. Only the call changes; the "
                "`def` line stays as it is.",
                "A variable `die_size = 6` made outside would not help: the function's `die_size` lives inside it.",
                "Write `print(roll_die(die_size=6))` under step 2.",
            ],
            checks=[check("a d6 is rolled by name and printed", _ROLL_NAMED)],
            pass_line="Lucky: A d6? Small. But it's mine.",
        ),
    ],
    solution=ROLL_SOLUTION,
    partials=[_roll(ROLL_GOOD)],
    assemble=dict(
        lines=["import random", "def roll_die(die_size=20):", "    return random.randint(1, die_size)",
               "print(roll_die())", "print(roll_die(die_size=6))"],
        distractors=["def roll_die(die_size: 20):", "def roll_die(die_size == 20):", "print(roll_die(size=6))"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A value already on the card",
            text=(
                "```text\ndef roll_die(die_size=20):\n             ^^^^^^^^^^^^\n         used when the\n"
                "         call is empty\n\nroll_die()           20\nroll_die(6)          6\n"
                "roll_die(die_size=6) 6\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="The usual order",
            text=(
                "At a tea stall you can say \"the usual\", and you get medium. Say \"large\", and you get large. "
                "A default is the usual. A value handed over is you saying what you want."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `def roll_die(die_size=20):` gives `die_size` a default.\n"
                "2. `roll_die()` hands over nothing, so `die_size` is 20.\n"
                "3. `roll_die(die_size=6)` names the value, so `die_size` is 6.\n"
                "4. Inside, `random.randint(1, die_size)` rolls whichever it got."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "The skill checks rolled `perform_roll(die_size)`, and every call typed the die. With "
                "`die_size=20` on the `def` line, a plain `perform_roll()` would roll the d20."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants 3 extra on his rolls. Give `roll_die` a second parameter, `bonus=0`, and add it to the "
            "roll. Then print `roll_die(bonus=3)`: a d20, plus 3. The name lets you skip `die_size`."
        ),
        hints=[
            "The `def` line gets two defaults: `def roll_die(die_size=20, bonus=0):`.",
            "The roll becomes `random.randint(1, die_size) + bonus`. Then add `print(roll_die(bonus=3))` at the "
            "bottom.",
        ],
        checks=[check("bonus has a default of 0 and is added to the roll", _ROLL_BONUS)],
        solution=_roll("def roll_die(die_size=20, bonus=0):\n    return random.randint(1, die_size) + bonus\n",
                       second=ROLL_D6 + "print(roll_die(bonus=3))\n"),
    ),
    campaign_link=dict(
        module=MODULE,
        part="skill-checks",
        snippet="def perform_roll(die_size):\n    return random.randint(1, die_size)",
        why=(
            "You wrote `perform_roll(die_size)` for the skill checks, and every call had to say which die. A "
            "default does the usual for you. You'll need defaults for `make_bar` in the Trials."
        ),
    ),
    takeaway="`def roll_die(die_size=20):` gives a default; `roll_die()` uses it, `roll_die(die_size=6)` names a value.",
    tracer=True,
    wrong_answers=[
        dict(why="the starter: roll_die() hands over nothing (no default yet)", code=ROLL_STARTER, fails_at=0,
             message_contains="missing 1 required positional argument: 'die_size'"),
        dict(why="a colon for = (an annotation, not a default)",
             code=_roll("def roll_die(die_size: 20):\n    return random.randint(1, die_size)\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="== for = on the def line", code=_roll("def roll_die(die_size == 20):\n    return random.randint(1, die_size)\n"),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="the number in place of the parameter", code=_roll("def roll_die(20):\n    return random.randint(1, 20)\n"),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="the default in quotes (text, not a number)",
             code=_roll('def roll_die(die_size="20"):\n    return random.randint(1, die_size)\n'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="a typed 20 in the call instead of a default (the error goes away, the def line is unchanged)",
             code=_roll(first="print(roll_die(20))\n"), fails_at=1, message_contains="Give `die_size` a default"),
        dict(why="the wrong default", code=_roll("def roll_die(die_size=6):\n    return random.randint(1, die_size)\n"),
             fails_at=1, message_contains="Make the default 20"),
        dict(why="a typed 20 in the roll (numbers in ink: A-06/A-07 typed test values)",
             code=_roll("def roll_die(die_size=20):\n    return random.randint(1, 20)\n"), fails_at=1,
             message_contains="not a typed 20"),
        dict(why="die_size set again inside the function (throws away what is handed over)",
             code=_roll("def roll_die(die_size=20):\n    die_size = 20\n    return random.randint(1, die_size)\n"),
             fails_at=1, message_contains="throws away"),
        dict(why="the parameter taken out, die_size made inside (roll_die(8) has nowhere to go)",
             code=_roll("def roll_die():\n    die_size = 20\n    return random.randint(1, die_size)\n"), fails_at=1,
             message_contains="Keep `die_size`"),
        dict(why="print inside the function instead of return",
             code=_roll("def roll_die(die_size=20):\n    print(random.randint(1, die_size))\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="CP2 the value handed over by position, not by name", code=_roll(ROLL_GOOD, second="print(roll_die(6))\n"),
             fails_at=2, message_contains="Name the value in the call"),
        dict(why="CP2 a keyword that is not the parameter's name",
             code=_roll(ROLL_GOOD, second="print(roll_die(size=6))\n"), fails_at=0,
             message_contains="unexpected keyword argument 'size'"),
        dict(why="CP2 == in the call (a question, not a name)",
             code=_roll(ROLL_GOOD, second="print(roll_die(die_size == 6))\n"), fails_at=0,
             message_contains="name 'die_size' is not defined"),
        dict(why="CP2 the parameter's name in quotes",
             code=_roll(ROLL_GOOD, second='print(roll_die("die_size"=6))\n'), fails_at=0,
             message_contains="expression cannot contain assignment"),
        dict(why="CP2 a variable die_size made outside (scope: it never reaches inside)",
             code=_roll(ROLL_GOOD, second="die_size = 6\nprint(roll_die())\n"), fails_at=2,
             message_contains="never reaches inside"),
        dict(why="CP2 rolled by name but not printed", code=_roll(ROLL_GOOD, second="roll_die(die_size=6)\n"),
             fails_at=2, message_contains="Print the roll"),
        dict(why="CP2 the wrong die", code=_roll(ROLL_GOOD, second="print(roll_die(die_size=8))\n"), fails_at=2,
             message_contains="Make it a d6"),
        dict(why="CP2 the d6 rolled by name, then a typed 5 printed (the number from Mar'tu's message)",
             code=_roll(ROLL_GOOD, second="roll_die(die_size=6)\nprint(5)\n"), fails_at=2,
             message_contains="Print the roll itself"),
        dict(why="CP2 the 6 in quotes", code=_roll(ROLL_GOOD, second='print(roll_die(die_size="6"))\n'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="the Example's parameter name copied (count for die_size: A-05/A-07/A-08 copied example names)",
             code=_roll("def roll_die(count=20):\n    return random.randint(1, count)\n"), fails_at=1,
             message_contains="Keep `die_size`"),
        dict(why="a keyword 20 in the call for step 1 instead of a default (the name in the wrong place)",
             code=_roll(first="print(roll_die(die_size=20))\n"), fails_at=1, message_contains="on the `def` line"),
        dict(why="CP2 rolled by name but not shown, and a d6 by position printed (the name skipped where it counts)",
             code=_roll(ROLL_GOOD, second="roll_die(die_size=6)\nprint(roll_die(6))\n"), fails_at=2,
             message_contains="Print the roll you named"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="default-arg,keyword-arg", solo="false", dictates="1,2",
             foreign_names="light_lamps,count,pour_glug,sips", par="(),(8,),(die_size=12)",
             card="prerequisite card for T-F-1 (u08c make_bar)") + "\n"
        "6B-08 (pool). Introduces node:DefaultArg and node:KeywordArg. The starter's `print(roll_die())` stops with "
        "Python's 'missing 1 required positional argument' at once: the reason for a default. CP1 RND: Mar'tu's "
        "check swaps `random.randint` for a scripted die and calls `roll_die()`, `roll_die(8)` and "
        "`roll_die(die_size=12)`, so a typed 20, a `die_size = 20` inside and a missing parameter each fail with "
        "their own message; `die_size: 20` (an annotation, the dictionary colon habit) and `\"20\"` stop at the "
        "bottom call (Python's lines, the explainer's rows). CP2: the AST must show `roll_die(die_size=6)` at the "
        "top level, then a rerun with the scripted die must print 5, and a `print` must hold that named call (or a "
        "variable made from it): a d6 printed by position beside an unshown named one fails. A positional 6, a "
        "variable `die_size = 6` outside (the 6B-09 scope slip) and a missing print get messages; `size=6`, `die_size == 6` and "
        "`\"die_size\"=6` are Python's own errors. Lucky's bonus: `bonus=0`, called as `roll_die(bonus=3)` (a "
        "keyword lets you skip a parameter). This is the prerequisite card for T-F-1 (`make_bar(current, maximum, "
        "full=\"█\", empty=\"░\")`)."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-09 inside-stays-inside (pool): scope. Predict the NameError, catch the value, then return it. RET.
# ---------------------------------------------------------------------------------------------

REST_DEF = (
    "def rest(hero):\n"
    '    full = hero["max_mana"]\n'
    '    restored = full - hero["mana"]\n'
    '    hero["mana"] = full\n'
)
REST_RETURN = "    return restored\n"
REST_LUCKY = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 20,\n'
    '    "max_mana": 26,\n'
    "}\n"
)
REST_BOTTOM = "rest(lucky)\nprint(restored)\n"
REST_CAUGHT = "gained = rest(lucky)\nprint(gained)\n"


def _rest(body=REST_DEF, bottom=REST_BOTTOM):
    return body + "\n\n" + REST_LUCKY + bottom


REST_STARTER = _rest()
REST_SOLUTION = _rest(REST_DEF + REST_RETURN, REST_CAUGHT)
assert REST_STARTER == (
    "def rest(hero):\n"
    '    full = hero["max_mana"]\n'
    '    restored = full - hero["mana"]\n'
    '    hero["mana"] = full\n'
    "\n"
    "\n"
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 20,\n'
    '    "max_mana": 26,\n'
    "}\n"
    "rest(lucky)\n"
    "print(restored)\n"
)
KITCHEN_EXAMPLE = (
    "def brew(cups):\n"
    "    pot = cups * 2\n"
    "    return pot\n"
    "\n\n"
    "tea = brew(3)\n"
    "print(tea)\n"
)

_GAINED_CAUGHT = r'''
_as = [_n for _n in _top() if type(_n).__name__ == 'Assign' and 'gained' in _made_by(_n)]
if not _as:
    _same = [_n for _n in _top() if type(_n).__name__ == 'Assign' and 'restored' in _made_by(_n)]
    assert not _same, ('Call the variable outside `gained`: `gained = rest(lucky)`. Inside `rest` there is already a '
                       '`restored`, and two kitchens are easier to follow with two names.')
    _other = [_x for _n in _top() if type(_n).__name__ == 'Assign' and _calls_in([_n.value], 'rest')
              for _x in _made_by(_n)]
    assert not _other, ('Call the variable `gained`, the name the step asks for: `gained = rest(lucky)`. Python '
                        'matches names letter for letter, and this one is `' + _other[0] + '`.')
    assert False, 'Catch what `rest(lucky)` returns in a variable: `gained = rest(lucky)`, in place of `rest(lucky)`.'
_v = _as[-1].value
if not (type(_v).__name__ == 'Call' and type(_v.func).__name__ == 'Name' and _v.func.id == 'rest'):
    assert not (type(_v).__name__ == 'Name' and _v.id == 'rest'), (
        'Add `(lucky)` to call it: `gained = rest(lucky)`. Now `gained` holds the function `rest` itself, not what it '
        'returns.')
    assert False, 'Make `gained` with a call: `gained = rest(lucky)`. A number worked out by hand never follows the sheet.'
assert len(_calls_in(_top(), 'rest')) == 1, (
    "Keep one call to `rest`: the one that catches the value, `gained = rest(lucky)`. The first call refills Lucky's "
    'mana, so a second one has nothing left to restore.')
_pr = _calls_in(_top(), 'print')
_shown = [_c for _c in _pr if [_a for _a in _c.args if type(_a).__name__ == 'Name' and _a.id == 'gained']]
_quoted = [_c for _c in _pr if [_a for _a in _c.args if type(_a).__name__ == 'Constant' and _a.value == 'gained']]
assert not (_quoted and not _shown), 'Take the quotes off: `print(gained)` shows what is in the variable. ' + _QUOTES
assert _shown, 'Print `gained` under the line that makes it: `print(gained)`.'
'''

_REST_RETURNS = r'''
_f = _need('rest', ['hero'])
_d = _defs().get('rest')
_typed = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return' and type(_n.value).__name__ == 'Constant'
          and type(_n.value.value).__name__ == 'int']
for _nm, _mana, _full in (('Pell', 3, 10), ('Brakka', 13, 22)):
    _h = {'name': _nm, 'mana': _mana, 'max_mana': _full}
    _what = 'called `rest` with a sheet for ' + _nm + ', mana ' + str(_mana) + ' of ' + str(_full)
    _val, _rows, _e = _call(_f, (_h,))
    assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    _want = _full - _mana
    if _val != _want:
        assert not (_val is None and [_l for _l in _rows if str(_want) in _words(_l)]), (
            'Use `return` in place of `print`, so the value goes back to the caller.'
            + _ev(_what, 'it printed ' + str(_want) + ', then returned `None`'))
        assert _val is not None, 'Add `return restored` as the last line of `rest`.' + _ev(_what, 'it returned `None`')
        assert type(_val).__name__ != 'str', 'Take the quotes off: `return restored`. ' + _QUOTES
        assert not _typed, ('Return the variable `restored`, not a typed number.'
                            + _ev(_what, 'it returned ' + _show(_val) + ', and ' + str(_want) + ' was restored'))
        _ints = [_n.value for _n in _ast.walk(_d) if type(_n).__name__ == 'Constant' and type(_n.value).__name__ == 'int']
        assert not _ints, ('Read the numbers from the sheet handed in, `hero["max_mana"]` and `hero["mana"]`, so '
                           '`restored` follows each sheet. A number typed inside `rest`, like ' + str(_ints[0]) + ', is '
                           'the same for every hero.'
                           + _ev(_what, 'it returned ' + _show(_val) + ', and ' + str(_want) + ' was restored'))
        assert not [_x for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id == 'lucky'], (
            'Read the sheet handed in, `hero`, inside `rest`. `lucky` is the sheet outside, so every call used '
            "Lucky's numbers." + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_want)))
        assert _val != 6, ('Keep `restored = full - hero["mana"]`, so it follows each sheet. 6 is only what Lucky '
                           'gets back.' + _ev(_what, 'it returned 6, and ' + str(_want) + ' was restored'))
        assert not (_val == 0 and _h['mana'] == _full), (
            'Return `restored`, worked out before the refill. After `hero["mana"] = full`, the mana is full, so '
            'working it out again gives 0.' + _ev(_what, 'it returned 0, and ' + str(_want) + ' was restored'))
        assert _val is not _h, 'Return `restored`, the mana given back, not the whole sheet.' + _ev(_what, 'it returned the sheet')
        assert _val != _full, ('Return `restored`, the mana given back.'
                               + _ev(_what, 'it returned ' + str(_val) + ', the new mana, not the ' + str(_want) + ' given back'))
        assert False, 'Return `restored`: `return restored`.' + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_want))
    assert _h['mana'] == _full, ('Put `return restored` last. A line under `return` never runs, so the mana was never '
                                 'refilled.' + _ev(_what, 'the mana stayed ' + str(_mana)))
_v = _g.get('gained')
assert _v == 6, '`gained` holds ' + _show(_v) + '. Catch the value once: `gained = rest(lucky)`.'
assert [_l for _l in _lines() if '6' in _words(_l)], 'Print `gained` under the line that makes it: `print(gained)`.'
'''

_REST_BONUS = r'''
_as = [_n for _n in _top() if type(_n).__name__ == 'Assign' and 'shell_gained' in _made_by(_n)]
assert _as and _calls_in([_as[-1].value], 'rest'), 'Catch `rest(bomb_shell)` in `shell_gained`.'
assert _g.get('shell_gained') == 15, ("`shell_gained` should be 15: Bomb Shell had 9 of 24. It holds "
                                      + _show(_g.get('shell_gained')) + '.')
assert [_l for _l in _lines() if '15' in _words(_l)], 'Print `shell_gained`.'
'''

INSIDE_STAYS_INSIDE = dict(
    id="inside-stays-inside",
    title="Inside stays inside",
    martu=(
        "A function is a kitchen with its own shelves. Its parameters, like `hero`, and the variables made inside "
        "it, like `restored`, live only in that kitchen while it runs. When the call ends, they are cleared away. "
        "That is called [[scope]].\n"
        "So a line outside can't see `restored`, and Python says it is not defined. If the caller needs the value, "
        "the function must hand it out with [[return]], and the caller catches it in a variable of its own: "
        "`gained = rest(lucky)`.\n"
        "The sheet is different. `hero` is a label on Lucky's own sheet, so the refill reaches him. That part "
        "needs no `return`."
    ),
    example=KITCHEN_EXAMPLE,
    example_output="6",
    names=["rest", "restored", "gained", "lucky"],
    predict=dict(
        q="Before you press Run: what will the last line do?",
        choices=["6", "26", "None", "ERROR: NameError: name 'restored' is not defined"],
        answer=3,
        explain=(
            "`restored` was made inside `rest`. It lives only there, like `hero`, and it is gone when the call ends. "
            "Outside, Python has never heard of it, so the last line stops with a NameError."
        ),
    ),
    tracer=True,
    starter=REST_STARTER,
    checkpoints=[
        dict(
            id="catch-it",
            text="Catch what `rest(lucky)` returns in a variable called `gained`, and print `gained` in place of "
                 "`restored`.",
            dictated=False,
            hints=[
                "Look at the last two lines. The outside can only see what `rest` returns, so catch it there.",
                "In the Example, `tea = brew(3)` catches what `brew` returns, and `print(tea)` shows it. `pot` "
                "stays inside `brew`.",
                "It will show `None` for now. That is the next step's job.",
                "Write `gained = rest(lucky)` in place of `rest(lucky)`, then `print(gained)`.",
            ],
            checks=[check("gained catches what rest(lucky) returns", _GAINED_CAUGHT)],
            pass_line="Mar'tu: `None`. The kitchen made a value and kept it. Now we fix that.",
        ),
        dict(
            id="return-it",
            text="`gained` shows `None`. Make `rest` return `restored`, as its last line.",
            dictated=True,
            hints=[
                "Look inside `rest`, at the bottom. Nothing hands `restored` out yet, so the call returns `None`.",
                "In the Example, `return pot` is the last line of `brew`. It hands the value out of the kitchen.",
                "Last, not first: a line under `return` never runs, and the mana must still be refilled.",
                "Write `return restored` as the last line of `rest`, indented.",
            ],
            checks=[check("rest returns the mana it gave back, and still refills", _REST_RETURNS)],
            pass_line="Lucky: Six mana back. I'm counting it.",
        ),
    ],
    solution=REST_SOLUTION,
    partials=[_rest(bottom=REST_CAUGHT)],
    assemble=dict(
        lines=["def rest(hero):", '    full = hero["max_mana"]', '    restored = full - hero["mana"]',
               '    hero["mana"] = full', "    return restored", 'lucky = {"name": "Lucky", "mana": 20, "max_mana": 26}',
               "gained = rest(lucky)", "print(gained)"],
        distractors=["print(restored)", "    print(restored)", "gained = rest"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two kitchens",
            text=(
                "```text\nrest's kitchen        outside\n  hero                 lucky\n  restored             gained\n"
                "     |                  ^\n     +-- return ------+\n```\n"
                "Only `return` passes a value through the wall."
            ),
        ),
        dict(
            angle="everyday",
            label="The baker's counter",
            text=(
                "A baker weighs the flour on a scale in the back room. You never see the scale. You get the bread "
                "over the counter. `restored` is the scale; `return` is the counter."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `rest(lucky)` starts: `hero` is Lucky's sheet.\n"
                "2. `full` is 26, and `restored` is 26 - 20 = 6.\n"
                "3. Lucky's mana becomes 26.\n"
                "4. `return restored` hands 6 out, and the kitchen is cleared.\n"
                "5. `gained = ...` catches the 6."
            ),
        ),
        dict(
            angle="from Unit 3",
            text=(
                "Unit 3 asked: whose kitchen is `result` in? Same answer here. A variable made in a function belongs "
                "to that function. The caller only gets what is returned."
            ),
        ),
    ],
    bonus=dict(
        by="bomb-shell",
        title="Shield up. Then rest.",
        text=(
            "Bomb Shell is low too. Make `bomb_shell` with `\"mana\": 9` and `\"max_mana\": 24`, catch "
            "`rest(bomb_shell)` in `shell_gained`, and print it."
        ),
        hints=[
            "A sheet like Lucky's, then `shell_gained = rest(bomb_shell)`.",
            "It should print 15: 24 - 9.",
        ],
        checks=[check("shell_gained catches rest(bomb_shell)", _REST_BONUS)],
        solution=REST_SOLUTION + 'bomb_shell = {"name": "Bomb Shell", "mana": 9, "max_mana": 24}\n'
                                 "shell_gained = rest(bomb_shell)\nprint(shell_gained)\n",
    ),
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        snippet="def show_mana(caster):\n    mana_bar = get_mana_bar(caster)\n    print_mana(caster, mana_bar)",
        why=(
            "`mana_bar` was made inside `show_mana`. Nothing outside could see it. That is why `show_mana` passed "
            "it on to `print_mana` right there, before the call ended."
        ),
    ),
    takeaway="Inside stays inside: a function's variables are gone when it ends. Return a value, and catch it outside.",
    wrong_answers=[
        dict(why="the starter: restored printed outside (scope)", code=REST_STARTER, fails_at=0,
             message_contains="name 'restored' is not defined"),
        dict(why="the parameter printed outside (scope)", code=_rest(bottom="rest(lucky)\nprint(hero)\n"), fails_at=0,
             message_contains="name 'hero' is not defined"),
        dict(why="CP1 the same name outside (accepted by Python, but the step asks for gained)",
             code=_rest(REST_DEF + REST_RETURN, "restored = rest(lucky)\nprint(restored)\n"), fails_at=1,
             message_contains="Call the variable outside `gained`"),
        dict(why="CP1 the function stored where its result was wanted (no call)",
             code=_rest(bottom="gained = rest\nprint(gained)\n"), fails_at=1, message_contains="holds the function `rest` itself"),
        dict(why="CP1 the Example's name copied (tea), not the name the step asks for",
             code=_rest(bottom="tea = rest(lucky)\nprint(tea)\n"), fails_at=1, message_contains="Call the variable `gained`"),
        dict(why="CP1 a number worked out by hand (A-06/A-07 typed values)",
             code=_rest(bottom="rest(lucky)\ngained = 6\nprint(gained)\n"), fails_at=1, message_contains="Make `gained` with a call"),
        dict(why="CP1 rest called twice (the second call has nothing to restore)",
             code=_rest(REST_DEF + REST_RETURN, "rest(lucky)\ngained = rest(lucky)\nprint(gained)\n"), fails_at=1,
             message_contains="Keep one call"),
        dict(why="CP1 gained in quotes", code=_rest(bottom='gained = rest(lucky)\nprint("gained")\n'), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="CP2 print inside instead of return (the caller gets None)",
             code=_rest(REST_DEF + "    print(restored)\n", REST_CAUGHT), fails_at=2, message_contains="in place of `print`"),
        dict(why="CP2 the new mana returned, not restored", code=_rest(REST_DEF + '    return hero["mana"]\n', REST_CAUGHT),
             fails_at=2, message_contains="the new mana"),
        dict(why="CP2 return placed before the refill (the line under it never runs)",
             code=_rest("def rest(hero):\n    full = hero[\"max_mana\"]\n    restored = full - hero[\"mana\"]\n"
                        "    return restored\n    hero[\"mana\"] = full\n", REST_CAUGHT),
             fails_at=2, message_contains="never runs"),
        dict(why="CP2 a typed 6 (the task's own answer)", code=_rest(REST_DEF + "    return 6\n", REST_CAUGHT), fails_at=2,
             message_contains="not a typed number"),
        dict(why="CP2 a typed 6 in restored (numbers in ink: the task's own answer, A-06/A-07)",
             code=_rest(REST_DEF.replace('full - hero["mana"]', "6") + REST_RETURN, REST_CAUGHT), fails_at=2,
             message_contains="follows each sheet"),
        dict(why="CP2 the outer sheet read inside rest (the wrong sheet: every call uses Lucky)",
             code=_rest(REST_DEF.replace('full - hero["mana"]', 'full - lucky["mana"]') + REST_RETURN, REST_CAUGHT),
             fails_at=2, message_contains="`lucky` is the sheet outside"),
        dict(why="CP2 the value worked out again after the refill (always 0)",
             code=_rest(REST_DEF + '    return full - hero["mana"]\n', REST_CAUGHT), fails_at=2,
             message_contains="before the refill"),
        dict(why="CP2 restored in quotes", code=_rest(REST_DEF + '    return "restored"\n', REST_CAUGHT), fails_at=2,
             message_contains="Take the quotes off"),
        dict(why="CP2 the whole sheet returned", code=_rest(REST_DEF + "    return hero\n", REST_CAUGHT), fails_at=2,
             message_contains="not the whole sheet"),
        dict(why="CP2 Lucky's mana typed into restored (numbers in ink: A-06/A-07 typed test values)",
             code=_rest(REST_DEF.replace('full - hero["mana"]', "full - 20") + REST_RETURN, REST_CAUGHT), fails_at=2,
             message_contains="like 20, is the same for every hero"),
        dict(why="CP2 Lucky's max mana typed for full (numbers in ink)",
             code=_rest(REST_DEF.replace('full = hero["max_mana"]', "full = 26") + REST_RETURN, REST_CAUGHT), fails_at=2,
             message_contains="like 26, is the same for every hero"),
        dict(why="CP2 return not indented (outside the function)", code=_rest(REST_DEF + "return restored\n", REST_CAUGHT),
             fails_at=0, message_contains="'return' outside function"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="scope,return-value", solo="false", dictates="2",
             foreign_names="brew,cups,pot,tea", par="Pell 3/10, Brakka 13/22") + "\n"
        "6B-09 (pool). Predict on the starter: the NameError (the right choice is 'ERROR: ...'). The order is "
        "reversed from the spec's wording so every Run shows progress: CP1 [ND] catches the value (`gained = "
        "rest(lucky)`, AST: one call, a call and not the bare function, printed), which shows `None`; CP2 [D] adds "
        "`return restored` (RET with two fresh sheets that never give 6: a typed `return 6` fails, a number typed "
        "anywhere inside `rest` (Lucky's 20 or 26) is named, and `return` above the refill fails because the mana "
        "stays). The CP1 'same name outside' message keeps the "
        "task's name; Python itself accepts `restored = rest(lucky)`. Bomb Shell's bonus repeats the catch with "
        "the party value 24 (mana 9). 6A-07's 'Whose kitchen is `result` in?' sidebar is the reading-level "
        "version. Twin assignment: this is the right-shape-wrong-meaning group's assigned twin after 6B-02 "
        "(recipes-change-sheets). Its `return restored` step targets that group's belief that a function hands "
        "back its raw inputs (the sheet it was handed, or a value read straight off it), not the value it worked "
        "out; CP2's 'the whole sheet returned' and 'the new mana returned' wrong answers prove those two readings "
        "fail. It is offered "
        "from u07a's 'more practice' angles (MORE_PRACTICE, after 6B-01, 6B-02 and 6B-10), in the same words "
        "everywhere."
    ),
)

EXTRA_7X = dict(
    kind="lesson",
    id="extra-defaults-and-scope",
    title="Extra practice: Defaults and Scope",
    optional=True,
    minutes=10,
    summary="Defaults and named values with `roll_die`, then why a variable inside a function can't be seen outside it.",
    notes=(
        "7X pool (6B-08 defaults-and-names, 6B-09 inside-stays-inside). Optional; feeds twins, early finishers and "
        "the T-F-1 prerequisite card. Introduces node:DefaultArg and node:KeywordArg (6B-08), pool only: no core "
        "item uses them, and the Quick Check doesn't either."
    ),
    exercises=[DEFAULTS_AND_NAMES, INSIDE_STAYS_INSIDE],
)


# =============================================================================================
# Article 6-A1 "lambda" (optional, node:Lambda), with one try-it
# =============================================================================================

RUN_ARRAY_DEF = (
    "def run_array(heroes, dial):\n"
    "    # Already finished. Leave it.\n"
    "    for hero in heroes:\n"
    "        print(dial(hero))\n"
)
ROSTER_NOTE = (
    "# roster holds the four heroes. Each\n"
    '# sheet has "name", "mana" and\n'
    '# "magical_affinity".\n'
)
DIAL_STEP1 = "# 1. Replace the 0 with a lambda.\n"
DIAL_STEP2 = "# 2. Hand it to run_array.\n"
DIAL_LAMBDA = 'max_mana_dial = lambda hero: hero["magical_affinity"] * 2\n'
DIAL_CALL = "run_array(roster, max_mana_dial)\n"


def _dial(make="max_mana_dial = 0\n", hand=""):
    return RUN_ARRAY_DEF + "\n\n" + ROSTER_NOTE + "\n" + DIAL_STEP1 + make + "\n" + DIAL_STEP2 + hand


DIAL_STARTER = _dial()
DIAL_SOLUTION = _dial(DIAL_LAMBDA, DIAL_CALL)
assert DIAL_STARTER == (
    "def run_array(heroes, dial):\n"
    "    # Already finished. Leave it.\n"
    "    for hero in heroes:\n"
    "        print(dial(hero))\n"
    "\n"
    "\n"
    "# roster holds the four heroes. Each\n"
    '# sheet has "name", "mana" and\n'
    '# "magical_affinity".\n'
    "\n"
    "# 1. Replace the 0 with a lambda.\n"
    "max_mana_dial = 0\n"
    "\n"
    "# 2. Hand it to run_array.\n"
)
HALF_EXAMPLE = "half = lambda n: n // 2\nprint(half(18))\nprint(half(26))\n"
HERO_VARS = ["oogrish", "gearshift", "bomb_shell", "lucky", "roster"]

_DIAL_MADE = r'''
_v = max_mana_dial
if not callable(_v):
    assert not (type(_v).__name__ == 'int' and _v == 0), (
        'Replace the 0 with a lambda: `lambda hero: hero["magical_affinity"] * 2`.')
    assert type(_v).__name__ != 'str', 'Take the quotes off the lambda: in quotes it is just text. ' + _QUOTES
    assert False, ('Make `max_mana_dial` the lambda itself, not what it returns: `lambda hero: '
                   'hero["magical_affinity"] * 2`. It holds ' + _show(_v) + ' now.')
_lam = [_n.value for _n in _top() if 'max_mana_dial' in _made_by(_n) and type(_n.value).__name__ == 'Lambda']
assert _lam, ('Make it with `lambda`, on one line: `max_mana_dial = lambda hero: ...`. A `def` works too, but this '
              'step is about the lambda.')
_ps = _params(_v)
assert len(_ps) == 1, ('Give the lambda one parameter, before the colon: `lambda hero:`.'
                       + (' It has none, so the hero handed over has nowhere to go.' if not _ps else ' It has '
                          + str(len(_ps)) + '.'))
_body = _lam[-1].body
_outer = [_x.id for _x in _ast.walk(_body) if type(_x).__name__ == 'Name' and _x.id in __HEROES__]
for _nm, _aff, _mana, _full in (('Pell', 7, 5, 11), ('Moss', 4, 3, 9)):
    _h = {'name': _nm, 'mana': _mana, 'max_mana': _full, 'magical_affinity': _aff}
    _what = 'called `max_mana_dial` with a sheet for ' + _nm + ', magical affinity ' + str(_aff)
    _val, _rows, _e = _call(_v, (_h,))
    if _e is not None:
        _k = _e.args[0] if type(_e).__name__ == 'KeyError' and _e.args else None
        assert not (type(_k).__name__ == 'str' and _close(_k, 'magical_affinity')), (
            'Use the key `"magical_affinity"`, letter for letter: the sheet has no key `"' + _k + '"`.' + _ev(_what))
        assert type(_e).__name__ != 'NameError' or 'magical_affinity' not in str(_e), (
            'Put quotes around the key: `hero["magical_affinity"]`. ' + _QUOTES)
        assert 'string indices' not in str(_e), ('Take the quotes off `hero`: `"hero"` is text, and text has no '
                                                 'keys. ' + _QUOTES)
        assert False, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    if _val == _aff * 2:
        continue
    assert not _outer, ('Use the parameter `hero` after the colon, not `' + _outer[0] + '`, so each hero handed over '
                        'is the one read.' + _ev(_what, 'it returned ' + _show(_val)))
    assert type(_body).__name__ != 'Constant', ('Read the sheet after the colon: `hero["magical_affinity"] * 2`, not a '
                                                'typed number.' + _ev(_what, 'it returned ' + _show(_val)))
    assert not (_val is None and _rows), ('Take the `print` out: a lambda returns what comes after the colon, and '
                                          '`print(...)` returns `None`.' + _ev(_what, 'it returned `None`'))
    assert _val != _aff, 'Multiply by 2: max mana is twice the affinity.' + _ev(_what, 'it returned ' + str(_aff))
    _read = [_x.slice.value for _x in _ast.walk(_body) if type(_x).__name__ == 'Subscript'
             and type(_x.slice).__name__ == 'Constant' and _x.slice.value in ('max_mana', 'mana')]
    assert not _read, ('Work it out from the affinity: `hero["magical_affinity"] * 2`. `hero["' + (_read or [''])[0]
                       + '"]` reads another number on the sheet.'
                       + _ev(_what, 'its sheet says mana ' + str(_mana) + ' of ' + str(_full) + ', and the lambda '
                             'returned ' + _show(_val) + ', not ' + str(_aff * 2)))
    assert False, ('Return `hero["magical_affinity"] * 2` after the colon.'
                   + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_aff * 2)))
'''

_DIAL_HANDED = r'''
assert _keep('run_array', __ORIG__) == '', ('Leave `run_array` as it is: it is already finished. Your code goes '
                                            'under the steps.')
_runs = _calls_in(_top(), 'run_array')
assert _runs, 'Call `run_array` under step 2, and hand it `roster` and `max_mana_dial`.'
_wrapped = [_c for _c in _calls_in(_top(), 'print') if _calls_in(_c.args, 'run_array')]
assert not _wrapped, ('Call `run_array` on its own line, with no `print(...)` around it. It prints each reading '
                      'itself, and returns `None`, so the extra `print` showed `None`.')
def _dial_arg(_c):
    _k = [_x.value for _x in _c.keywords if _x.arg == 'dial']
    return _c.args[1] if len(_c.args) == 2 else (_k[0] if _k else None)
_ok = [_c for _c in _runs if type(_dial_arg(_c)).__name__ == 'Name' and _dial_arg(_c).id == 'max_mana_dial']
if not _ok:
    assert not [_c for _c in _runs if len(_c.args) == 2 and type(_c.args[1]).__name__ == 'Lambda'], (
        'Hand over the variable `max_mana_dial`: `run_array(roster, max_mana_dial)`. A lambda right inside the call '
        "is Lucky's side quest.")
    assert False, 'Hand `run_array` the lambda with no `()`: `run_array(roster, max_mana_dial)`.'
_ns, _ls, _e, _miss, _log = _rerun(_pre=__OTHER__)
_what = 'ran your program again with another roster: Pell, Brakka and Moss'
assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
_want = ['12', '16', '10']
_got = [_l for _l in _ls if _l in _want]
assert _got[:3] == _want, ('Hand over `roster` itself, the list that is already made, so every hero in it is read.'
                           + _ev(_what, 'their readings, 12, 16 and 10, did not all print'))
'''

_DIAL_NAMES = r'''
_runs = _calls_in(_top(), 'run_array')
_inline = [_c for _c in _runs if len(_c.args) == 2 and type(_c.args[1]).__name__ == 'Lambda']
assert _inline, 'Call `run_array` again, with a lambda right inside the brackets: `run_array(roster, lambda hero: ...)`.'
_ns, _ls, _e, _miss, _log = _rerun(_pre=__OTHER__)
assert _e is None, 'Mend this, then Run again: ' + _err(_e)
assert [_n for _n in ('Pell', 'Brakka', 'Moss') if _n in _ls] == ['Pell', 'Brakka', 'Moss'], (
    'Make the lambda return `hero["name"]`, so each hero handed over says its own name.'
    + _ev('ran your program with another roster', 'Pell, Brakka and Moss did not all print'))
'''

LAMBDA_DIAL = dict(
    id="a-dial-in-one-line",
    title="A dial in one line",
    martu=(
        "The resonance array again. `run_array(heroes, dial)` is finished: it calls `dial(hero)` for each hero and "
        "prints the reading.\n"
        "A dial this small doesn't need a `def`. Write it as a [[lambda]]: the parameter, a colon, then what it "
        "returns. Store it, then hand it over with no `()`, like any [[function as a value]]."
    ),
    example=HALF_EXAMPLE,
    example_output="9\n13",
    introduces=["node:Lambda"],
    setup=ROSTER_SETUP,
    names=["max_mana_dial", "hero", "run_array", "roster"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code="third = lambda n: n // 3\nprint(third(27))\n",
        choices=["9", "27", "None", "ERROR: SyntaxError"],
        answer=0,
        explain=(
            "`third` holds a function. `third(27)` calls it with `n` as 27, and it returns what comes after the "
            "colon: 27 // 3, which is 9. A lambda needs no `return`."
        ),
    ),
    pair_talk="Tell your partner what `dial` holds while `run_array` runs, and why there is no `()` after it.",
    starter=DIAL_STARTER,
    checkpoints=[
        dict(
            id="make-the-lambda",
            text="Replace the 0 with a lambda that takes `hero` and returns `hero[\"magical_affinity\"] * 2`.",
            dictated=True,
            hints=[
                "Look at `max_mana_dial = 0`. The lambda goes after the `=`, all on one line.",
                "In the Example, `lambda n: n // 2` takes `n` and returns `n // 2`. The parameter comes before the "
                "colon; the value to return comes after it.",
                "No `return` inside a lambda: Python stops with *invalid syntax*. The value after the colon is "
                "returned on its own.",
                "Write `max_mana_dial = lambda hero: hero[\"magical_affinity\"] * 2` in place of the 0 line.",
            ],
            checks=[check("max_mana_dial is a lambda that doubles the affinity", _DIAL_MADE, setup=ROSTER_SETUP,
                          heroes=HERO_VARS)],
            pass_line="Gearshift: One line. No arithmetic argument. I approve.",
        ),
        dict(
            id="hand-it-over",
            text="Hand `max_mana_dial` to `run_array`, with `roster`.",
            dictated=False,
            hints=[
                "Under step 2. `run_array` wants two values, in the order of its `def` line: the heroes, then the "
                "dial.",
                "In the unit, `cast_on_everyone(roster, warm_hands)` handed a function over with no `()`. "
                "`run_array` calls it later, once per hero.",
                "With `()`, the lambda would run now, with no hero, and Python stops: *missing 1 required "
                "positional argument*.",
                "Write `run_array(roster, max_mana_dial)` under step 2.",
            ],
            checks=[check("run_array reads every hero with max_mana_dial", _DIAL_HANDED, setup=ROSTER_SETUP,
                          orig=RUN_ARRAY_DEF, other=OTHER_ROSTER)],
            pass_line="Mar'tu: 18, 20, 24, 26. The array agrees with the chalk.",
        ),
    ],
    solution=DIAL_SOLUTION,
    partials=[_dial(DIAL_LAMBDA)],
    assemble=dict(
        lines=[line for line in DIAL_SOLUTION.splitlines() if line.strip() and not line.lstrip().startswith("#")],
        distractors=['max_mana_dial = lambda hero: return hero["magical_affinity"] * 2',
                     "run_array(roster, max_mana_dial())", "run_array(max_mana_dial, roster)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The same function, two ways",
            text=(
                "```text\ndef half(n):\n    return n // 2\n\nhalf = lambda n: n // 2\n"
                "       ^^^^^^ ^^^^^^\n       takes  returns\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A note on a scrap of paper",
            text=(
                "A `def` is a recipe card with a title, kept in the box. A lambda is a quick note on a scrap: "
                "\"double it\". You hand it over and forget it. Fine for one line; use the card for more."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `lambda hero:` starts a function that takes `hero`.\n"
                "2. `hero[\"magical_affinity\"] * 2` after the colon is what it returns.\n"
                "3. `max_mana_dial = ...` stores it. Nothing runs yet.\n"
                "4. `run_array(roster, max_mana_dial)` hands it over, and `run_array` calls it for each hero."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "In the spell book part, `strengthen_magic(caster)` had one line: `reinforce_barrier(caster)`. A "
                "lambda could be that whole function: `lambda caster: reinforce_barrier(caster)`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants his name read out by the array. Call `run_array` again, with a lambda right inside the "
            "brackets that returns each hero's `\"name\"`. No variable needed."
        ),
        hints=[
            "The lambda goes where `max_mana_dial` went: `run_array(roster, lambda hero: ...)`.",
            "After the colon: `hero[\"name\"]`.",
        ],
        checks=[check("run_array reads every name with a lambda in the call", _DIAL_NAMES, setup=ROSTER_SETUP,
                      other=OTHER_ROSTER)],
        solution=DIAL_SOLUTION + 'run_array(roster, lambda hero: hero["name"])\n',
    ),
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet="def strengthen_magic(caster):\n    reinforce_barrier(caster)",
        why=(
            "`strengthen_magic` was a two-line function with one job, handed to `add_spell` with no `()`. A "
            "lambda is the same kind of value, written in one line."
        ),
    ),
    takeaway="`lambda hero: hero[\"mana\"]` is a one-line function: parameter, colon, what it returns. Hand it over with no `()`.",
    wrong_answers=[
        dict(why="the starter (0 placeholder)", code=DIAL_STARTER, fails_at=1, message_contains="Replace the 0"),
        dict(why="return inside a lambda", code=_dial('max_mana_dial = lambda hero: return hero["magical_affinity"] * 2\n'),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="no parameter before the colon (the hero handed over has nowhere to go)",
             code=_dial('max_mana_dial = lambda: lucky["magical_affinity"] * 2\n'), fails_at=1,
             message_contains="one parameter"),
        dict(why="the outer sheet read, not the parameter (numbers in ink: A-06/A-07)",
             code=_dial('max_mana_dial = lambda hero: lucky["magical_affinity"] * 2\n'), fails_at=1,
             message_contains="not `lucky`"),
        dict(why="the max mana copied off the sheet, not worked out from the affinity (the dial skipped)",
             code=_dial('max_mana_dial = lambda hero: hero["max_mana"]\n', DIAL_CALL), fails_at=1,
             message_contains="another number on the sheet"),
        dict(why="the wrong key read (\"mana\", the mana now)", code=_dial('max_mana_dial = lambda hero: hero["mana"] * 2\n'),
             fails_at=1, message_contains="Work it out from the affinity"),
        dict(why="a typed number", code=_dial("max_mana_dial = lambda hero: 26\n"), fails_at=1,
             message_contains="not a typed number"),
        dict(why="an approximate key (\"magic\" for \"magical_affinity\")",
             code=_dial('max_mana_dial = lambda hero: hero["magic"] * 2\n'), fails_at=1,
             message_contains='no key `"magic"`'),
        dict(why="the key with no quotes", code=_dial("max_mana_dial = lambda hero: hero[magical_affinity] * 2\n"),
             fails_at=1, message_contains="Put quotes around the key"),
        dict(why="print inside the lambda (returns None)",
             code=_dial('max_mana_dial = lambda hero: print(hero["magical_affinity"] * 2)\n'), fails_at=1,
             message_contains="Take the `print` out"),
        dict(why="the result stored where the function was wanted (a value, not a lambda)",
             code=_dial('max_mana_dial = lucky["magical_affinity"] * 2\n'), fails_at=1,
             message_contains="not what it returns"),
        dict(why="the lambda in quotes", code=_dial('max_mana_dial = "lambda hero: hero[\'magical_affinity\'] * 2"\n'),
             fails_at=1, message_contains="Take the quotes off"),
        dict(why="a def, not a lambda",
             code=_dial('def max_mana_dial(hero):\n    return hero["magical_affinity"] * 2\n'), fails_at=1,
             message_contains="Make it with `lambda`"),
        dict(why="CP2 handed over WITH () (runs now, with no hero)", code=_dial(DIAL_LAMBDA, "run_array(roster, max_mana_dial())\n"),
             fails_at=0, message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="CP2 the result of a call handed over, not the function ('int' is not callable)",
             code=_dial(DIAL_LAMBDA, "run_array(roster, max_mana_dial(lucky))\n"), fails_at=0,
             message_contains="'int' object is not callable"),
        dict(why="CP2 the two values in the wrong order", code=_dial(DIAL_LAMBDA, "run_array(max_mana_dial, roster)\n"),
             fails_at=0, message_contains="'function' object is not iterable"),
        dict(why="CP2 the function's name in quotes", code=_dial(DIAL_LAMBDA, 'run_array(roster, "max_mana_dial")\n'),
             fails_at=0, message_contains="'str' object is not callable"),
        dict(why="CP2 print around run_array (an extra None)",
             code=_dial(DIAL_LAMBDA, "print(run_array(roster, max_mana_dial))\n"), fails_at=2,
             message_contains="no `print(...)` around it"),
        dict(why="CP2 a loop of its own instead of handing the function over",
             code=_dial(DIAL_LAMBDA, "for hero in roster:\n    print(max_mana_dial(hero))\n"), fails_at=2,
             message_contains="Call `run_array`"),
        dict(why="CP2 one hero only, not the roster", code=_dial(DIAL_LAMBDA, "run_array([lucky], max_mana_dial)\n"),
             fails_at=2, message_contains="Hand over `roster` itself"),
        dict(why="CP2 the finished helper edited", code=_dial(DIAL_LAMBDA, DIAL_CALL).replace(
            "        print(dial(hero))\n", "        print(hero[\"name\"], dial(hero))\n"),
             fails_at=2, message_contains="Leave `run_array` as it is"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="lambda,func-as-value", solo="false", dictates="1",
             foreign_names="half,n,third,warm_hands", par="Pell 7, Moss 4") + "\n"
        "6-A1 try-it. Introduces node:Lambda (optional only: no core item uses it). CP1 [D]: `max_mana_dial` must "
        "be a lambda (AST), with one parameter, called with two fresh sheets (affinity 7 and 4, never a party "
        "value): a typed 26, `lucky[...]` in the body, the approximate key `\"magic\"`, an unquoted key, "
        "`print(...)` inside, a `def` and quotes each get a message; `return` inside is Python's 'invalid "
        "syntax'. CP2 [ND]: KEEP on `run_array`, the AST call `run_array(roster, max_mana_dial)` (a loop of one's "
        "own fails), then CMB with Pell, Brakka and Moss set after setup (readings 12, 16, 10). Handing over with "
        "`()`, the call's result, the order swapped and the name in quotes are Python's errors, shown by the "
        "explainer. Lucky's bonus is a lambda written right in the call. `run_array` is 6P's own dial runner, "
        "finished here."
    ),
)

LAMBDA_ARTICLE = dict(
    kind="article",
    id="lambda",
    title="lambda: A Function in One Line",
    optional=True,
    minutes=10,
    summary="A tiny function with no name: `lambda hero: hero[\"mana\"]`. Store it, or hand it straight over.",
    introduces=["node:Lambda"],
    body=(
        "Some functions are tiny. One line, used once, handed straight to another function. For those, Python has "
        "a short form, the [[lambda]]:\n"
        "```python\nhalf = lambda n: n // 2\n```\n"
        "That is a whole function. Before the colon is the parameter, `n`. After the colon is what it returns. "
        "There is no `def`, no name on the function and no `return`: the value after the colon is the answer.\n"
        "It does the same job as this:\n"
        "```python\ndef half(n):\n    return n // 2\n```\n"
        "Call it the same way: `half(18)` is 9.\n"
        "A lambda shines when you hand a function over, with no `()`, like a dial for the resonance array: "
        "`run_array(roster, lambda hero: hero[\"mana\"])`.\n"
        "Two slips to watch. A lambda can't hold `return`: Python stops with *invalid syntax*. And a lambda is "
        "one line only. For anything longer, or anything you will use again, write a `def`. It has a name, and a "
        "name helps the next reader."
    ),
    examples=[
        dict(code="half = lambda n: n // 2\nprint(half(18))\n", output="9"),
        dict(code="def twice(n):\n    return n * 2\n\n\nalso_twice = lambda n: n * 2\nprint(twice(13))\n"
                  "print(also_twice(13))\n", output="26\n26"),
        dict(code='def show_all(heroes, dial):\n    for hero in heroes:\n        print(dial(hero))\n\n\n'
                  'team = [\n    {"name": "Oogrish", "mana": 18},\n    {"name": "Lucky", "mana": 26},\n]\n'
                  'show_all(team, lambda h: h["name"])\n', output="Oogrish\nLucky"),
    ],
    exercises=[LAMBDA_DIAL],
    notes=(
        "meta: path=optional. 6-A1 (O, 10 min). Introduces node:Lambda. Loops in the examples are Unit 6's planned "
        "`for` over a list of dicts (u06a). The errors are shown as words in the body (an example that crashes "
        "can't be verified). The try-it is one exercise (2 checkpoints and Lucky's side quest)."
    ),
)


# =============================================================================================
# Article 6-A2 "map()" (optional, call:map), with one try-it
# =============================================================================================

GET_NAME_DEF = 'def get_name(hero):\n    return hero["name"]\n'
GET_MANA_DEF = 'def get_mana(hero):\n    return hero["mana"]\n'
MAP_NAMES = "names = list(map(get_name, roster))\n"
MAP_MANAS = "manas = list(map(get_mana, roster))\nprint(manas)\n"


def _mapped(names="names = []\n", get_mana="", manas=""):
    return (GET_NAME_DEF + "\n\n# roster holds the four heroes.\n\n# 1. Make names with map().\n" + names
            + "print(names)\n\n# 2. Write get_mana(hero) here.\n" + get_mana + "\n# 3. Make manas with map(),\n"
            "#    then print it.\n" + manas)


MAP_STARTER = _mapped()
MAP_SOLUTION = _mapped(MAP_NAMES, GET_MANA_DEF, MAP_MANAS)
assert MAP_STARTER == (
    "def get_name(hero):\n"
    '    return hero["name"]\n'
    "\n"
    "\n"
    "# roster holds the four heroes.\n"
    "\n"
    "# 1. Make names with map().\n"
    "names = []\n"
    "print(names)\n"
    "\n"
    "# 2. Write get_mana(hero) here.\n"
    "\n"
    "# 3. Make manas with map(),\n"
    "#    then print it.\n"
)
DOUBLE_EXAMPLE = "def double(n):\n    return n * 2\n\n\ncosts = [2, 6, 10]\nprint(list(map(double, costs)))\n"

_LIST_MAPPED = r'''
_name, _key, _fn = __NAME__, __KEY__, __FN__
assert _name in _g, 'Make `' + _name + '` under its step: `' + _name + ' = list(map(' + _fn + ', roster))`.'
_v = _g[_name]
_want = [_h[_key] for _h in roster]
if _v != _want:
    assert type(_v).__name__ != 'map', ('Wrap it in `list()`: `list(map(' + _fn + ', roster))`. On its own, `map()` '
                                        'returns a map object, not the values.')
    assert _v != [], '`' + _name + "` is still the starter's `[]`. Make it `list(map(" + _fn + ', roster))`.'
    assert not (type(_v).__name__ == 'list' and _v and [_x for _x in _v if _x is None]), (
        '`' + _name + '` is full of `None`: the function prints, and `map()` collects what it returns.')
    assert False, 'Make `' + _name + '` with `list(map(' + _fn + ', roster))`: one value for each hero.'
_mine = [_n for _n in _top() if _name in _made_by(_n) and _calls_in([_n.value], 'map')]
assert _mine, ('Make it with `map()`: `list(map(' + _fn + ', roster))`. `map()` calls the function on every hero for '
               'you.')
_ns, _ls, _e, _miss, _log = _rerun(_pre=__OTHER__)
_what = 'ran your program again with another roster: Pell, Brakka and Moss'
assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
_got = _ns.get(_name)
assert _got == [_h[_key] for _h in _ns['roster']], (
    'Make `' + _name + '` from `roster` with `map()`, not typed values.' + _ev(_what, '`' + _name + '` did not follow it'))
'''

_GET_MANA = r'''
_f, _m = _find('get_mana', True)
assert _f, (_m if 'letter for letter' in _m else 'Write a function called `get_mana`, with one parameter: '
            '`def get_mana(hero):`.')
assert len(_params(_f)) == 1, 'Give `get_mana` one parameter, the hero: `def get_mana(hero):`.'
_d = _defs().get('get_mana')
_outer = [_x.id for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id in __HEROES__] if _d else []
_typed = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return' and type(_n.value).__name__ == 'Constant'] if _d else []
for _nm, _mana, _full in (('Pell', 7, 12), ('Brakka', 15, 16)):
    _h = {'name': _nm, 'mana': _mana, 'max_mana': _full, 'magical_affinity': 6}
    _what = 'called `get_mana` with a sheet for ' + _nm + ', mana ' + str(_mana) + ' of ' + str(_full)
    _val, _rows, _e = _call(_f, (_h,))
    if _e is not None:
        _k = _e.args[0] if type(_e).__name__ == 'KeyError' and _e.args else None
        assert not (type(_k).__name__ == 'str' and _close(_k, 'mana')), (
            'Use the key `"mana"`, letter for letter: the sheet has no key `"' + _k + '"`.' + _ev(_what))
        assert False, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    if _val == _mana:
        continue
    assert not (_val is None and _rows), ('Use `return` in place of `print`: `map()` collects what the function '
                                          'returns.' + _ev(_what, 'it printed the mana, then returned `None`'))
    assert _val is not None, 'Return the mana: `return hero["mana"]`.' + _ev(_what, 'it returned `None`')
    assert _val != _nm, ('Change the key to `"mana"`: `get_mana` still reads `"name"`, copied from `get_name`.'
                         + _ev(_what, 'it returned the name, ' + _nm))
    assert not _outer, ('Read the parameter `hero`, not `' + _outer[0] + '`, so each hero handed over is the one '
                        'read.' + _ev(_what, 'it returned ' + _show(_val)))
    assert not _typed, ('Read the mana from the sheet handed in: `return hero["mana"]`, not a typed number.'
                        + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_mana)))
    assert _val != _full, ('Return `hero["mana"]`, the mana the hero has now, not `"max_mana"`.'
                           + _ev(_what, 'it returned ' + str(_full)))
    assert False, 'Return `hero["mana"]`.' + _ev(_what, 'it returned ' + _show(_val) + ', not ' + str(_mana))
'''

_MANAS_SHOWN = r'''
assert [_l for _l in _lines() if '[18, 20, 24, 26]' in _l], 'Print `manas` under the line that makes it: `print(manas)`.'
_ns, _ls, _e, _miss, _log = _rerun(_pre=__OTHER__)
assert [_l for _l in _ls if '[7, 15, 3]' in _l], (
    'Print the variable: `print(manas)`. A typed list stays the same when the roster changes.'
    + _ev('ran your program again with another roster: Pell, Brakka and Moss', 'no line showed their manas, [7, 15, 3]'))
'''

_MAXES_MAPPED = r'''
_v = _g.get('max_manas')
assert _v == [18, 20, 24, 26], ('Make `max_manas` with `map()` and a lambda that returns '
                                '`hero["magical_affinity"] * 2`. It holds ' + _show(_v) + '.')
_maps = _calls_in(_top(), 'map')
_lams = [_c.args[0] for _c in _maps if _c.args and type(_c.args[0]).__name__ == 'Lambda']
assert _lams, 'Hand `map()` a lambda as its function: `map(lambda hero: ..., roster)`.'
assert [_x for _l in _lams for _x in _ast.walk(_l.body) if type(_x).__name__ == 'Constant'
        and _x.value == 'magical_affinity'], ('Work it out from the affinity: the lambda returns '
                                              '`hero["magical_affinity"] * 2`, not a number copied off the sheet.')
assert [_l for _l in _lines() if _l == '[18, 20, 24, 26]'], 'Print `max_manas`.'
_ns, _ls, _e, _miss, _log = _rerun(_pre=__OTHER__)
assert _e is None, 'Mend this, then Run again: ' + _err(_e)
assert [_l for _l in _ls if _l == '[12, 16, 10]'], (
    'Make `max_manas` from `roster` with `map()`, and print the variable, not a typed list.'
    + _ev('ran your program again with another roster: Pell, Brakka and Moss', 'no line showed [12, 16, 10]'))
'''

MAP_NAMES_EXERCISE = dict(
    id="every-hero-at-once",
    title="Every hero at once",
    martu=(
        "[[map()]] takes a function and a list. It calls the function on every item, and collects what each call "
        "returns. Hand the function over with no `()`: `map()` does the calling.\n"
        "Like `range()`, it hides its answers until you wrap it in `list()`: `list(map(get_name, roster))`."
    ),
    example=DOUBLE_EXAMPLE,
    example_output="[4, 12, 20]",
    introduces=["call:map"],
    setup=ROSTER_SETUP,
    names=["names", "get_name", "roster", "get_mana", "hero", "manas"],
    predict=dict(
        q="This function prints instead of returning. Before you press Run: what will this print?",
        code=("def shout(n):\n    print(n)\n\n\n"
              "print(list(map(shout, [4, 9])))\n"),
        choices=["4\n9\n[None, None]", "[4, 9]", "4\n9\n[4, 9]", "[None, None]"],
        answer=0,
        explain=(
            "`map()` calls `shout` on 4, then on 9, and each call prints its number. But `shout` returns nothing, "
            "so `map()` collects `None` twice. To collect the numbers, the function must `return` them."
        ),
    ),
    starter=MAP_STARTER,
    checkpoints=[
        dict(
            id="map-the-names",
            text="Make `names` with `list(map(get_name, roster))`.",
            dictated=True,
            hints=[
                "Look at `names = []`. `map()` takes the function first, with no `()`, then the list.",
                "In the Example, `list(map(double, costs))` calls `double` on every cost and collects the "
                "answers in a list.",
                "With `get_name()`, the function would run now, with no hero, and Python stops.",
                "Write `names = list(map(get_name, roster))` in place of `names = []`.",
            ],
            checks=[check("names holds every hero's name, from map()", _LIST_MAPPED, setup=ROSTER_SETUP,
                          name="names", key="name", fn="get_name", other=OTHER_ROSTER)],
            pass_line="Bomb Shell: Four names. All present.",
        ),
        dict(
            id="write-get-mana",
            text="Under step 2, write `get_mana(hero)`, which returns the hero's `\"mana\"`.",
            dictated=False,
            hints=[
                "Look at `get_name` at the top. `get_mana` has the same shape, with another key.",
                "A function that `map()` uses must return its answer. `print` would only show it, and `map()` "
                "would collect `None`.",
                "The key is `\"mana\"`, letter for letter.",
                "Write `def get_mana(hero):` under step 2, with `return hero[\"mana\"]` indented under it.",
            ],
            checks=[check("get_mana returns the mana of the hero handed over", _GET_MANA, setup=ROSTER_SETUP,
                          heroes=HERO_VARS)],
            pass_line="Gearshift: A second reader. Logged.",
        ),
        dict(
            id="map-the-manas",
            text="Under step 3, make `manas` with `map()` and `get_mana`, then print it.",
            dictated=False,
            hints=[
                "Under step 3. The same shape as step 1, with your own function.",
                "`map()` takes the function with no `()`, then `roster`. `list()` around it shows the values.",
                "Then `print(manas)` on its own line.",
                "Write `manas = list(map(get_mana, roster))`, then `print(manas)`.",
            ],
            checks=[
                check("manas holds every hero's mana, from map()", _LIST_MAPPED, setup=ROSTER_SETUP,
                      name="manas", key="mana", fn="get_mana", other=OTHER_ROSTER),
                check("manas is printed", _MANAS_SHOWN, setup=ROSTER_SETUP, other=OTHER_ROSTER),
            ],
            pass_line="Mar'tu: 18, 20, 24, 26. Every bar on one line, yes?",
        ),
    ],
    solution=MAP_SOLUTION,
    partials=[_mapped(MAP_NAMES), _mapped(MAP_NAMES, GET_MANA_DEF)],
    assemble=dict(
        lines=[line for line in MAP_SOLUTION.splitlines() if line.strip() and not line.lstrip().startswith("#")],
        distractors=["names = list(map(get_name(), roster))", "names = list(map(roster, get_name))",
                     "    print(hero[\"mana\"])"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One function, every item",
            text=(
                "```text\nroster:   Oogrish  Gearshift ...\n            |         |\n"
                "get_name  get_name  get_name ...\n            |         |\nnames:  \"Oogrish\" \"Gearshift\" ...\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A stamp on every letter",
            text=(
                "You hand a clerk a stamp and a pile of letters. The clerk stamps each one and hands the pile back. "
                "You don't stamp anything yourself. `map()` is the clerk; the function is the stamp."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `map(get_name, roster)` gets the function, not a call.\n"
                "2. It calls `get_name(oogrish)`, then `get_name(gearshift)`, and so on.\n"
                "3. `list(...)` collects every return value, in order."
            ),
        ),
        dict(
            angle="the loop it saves",
            label="The same with a loop",
            text=(
                "`names = []`, then `for hero in roster:` with `names.append(get_name(hero))` inside, makes the "
                "same list. `map()` writes that loop for you."
            ),
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="Max mana, from the affinities",
        text=(
            "Gearshift wants every max mana in one line. Make `max_manas` with `map()` and a lambda that returns "
            "`hero[\"magical_affinity\"] * 2`, then print it. (The lambda article shows how.)"
        ),
        hints=[
            "The lambda goes where the function's name went: `map(lambda hero: ..., roster)`.",
            "Then `list(...)` around it, and `print(max_manas)`.",
        ],
        checks=[check("max_manas comes from map() and a lambda", _MAXES_MAPPED, setup=ROSTER_SETUP, other=OTHER_ROSTER)],
        solution=MAP_SOLUTION + 'max_manas = list(map(lambda hero: hero["magical_affinity"] * 2, roster))\n'
                                "print(max_manas)\n",
    ),
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        snippet="for member in party.members:\n    show_mana(member)",
        why=(
            "The loop at the bottom of the mana bars called one function for every party member. `map()` is that "
            "loop, when you want the answers back in a list."
        ),
    ),
    takeaway="`list(map(get_name, roster))` calls `get_name` on every hero and collects what it returns.",
    wrong_answers=[
        dict(why="the starter (names is [])", code=MAP_STARTER, fails_at=1, message_contains="still the starter"),
        dict(why="no list(): a map object", code=_mapped("names = map(get_name, roster)\n"), fails_at=1,
             message_contains="Wrap it in `list()`"),
        dict(why="handed over WITH () (runs now, with no hero)", code=_mapped("names = list(map(get_name(), roster))\n"),
             fails_at=0, message_contains="missing 1 required positional argument: 'hero'"),
        dict(why="the two values in the wrong order", code=_mapped("names = list(map(roster, get_name))\n"), fails_at=0,
             message_contains="'function' object is not iterable"),
        dict(why="the function's name in quotes", code=_mapped('names = list(map("get_name", roster))\n'), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="the names typed by hand (numbers in ink: A-06/A-07)",
             code=_mapped('names = ["Oogrish", "Gearshift",\n         "Bomb Shell", "Lucky"]\n'), fails_at=1,
             message_contains="Make it with `map()`"),
        dict(why="a loop with append: right, but not map()",
             code=_mapped("names = []\nfor hero in roster:\n    names.append(get_name(hero))\n"), fails_at=1,
             message_contains="Make it with `map()`"),
        dict(why="CP2 print instead of return", code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    print(hero["mana"])\n'),
             fails_at=2, message_contains="in place of `print`"),
        dict(why="CP2 the wrong key (max_mana)", code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    return hero["max_mana"]\n'),
             fails_at=2, message_contains='not `"max_mana"`'),
        dict(why="CP2 the outer sheet, not the parameter", code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    return lucky["mana"]\n'),
             fails_at=2, message_contains="not `lucky`"),
        dict(why="CP2 a near-miss key", code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    return hero["Mana"]\n'),
             fails_at=2, message_contains='no key `"Mana"`'),
        dict(why="CP3 the result of one call handed over ('int' is not callable)",
             code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = list(map(get_mana(lucky), roster))\nprint(manas)\n"),
             fails_at=0, message_contains="'int' object is not callable"),
        dict(why="CP3 no list(): a map object", code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = map(get_mana, roster)\nprint(manas)\n"),
             fails_at=3, message_contains="Wrap it in `list()`"),
        dict(why="CP3 the manas typed by hand", code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = [18, 20, 24, 26]\nprint(manas)\n"),
             fails_at=3, message_contains="Make it with `map()`"),
        dict(why="CP3 the printed list typed by hand (the variable made, then not used)",
             code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = list(map(get_mana, roster))\nprint([18, 20, 24, 26])\n"),
             fails_at=3, message_contains="A typed list stays the same"),
        dict(why="CP2 a typed mana (A-06/A-07 typed test values)",
             code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    return 18\n'), fails_at=2, message_contains="not a typed number"),
        dict(why="CP3 not printed", code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = list(map(get_mana, roster))\n"),
             fails_at=3, message_contains="Print `manas`"),
        dict(why="CP2 get_name copied without changing its key (a template copied word for word, A-08)",
             code=_mapped(MAP_NAMES, 'def get_mana(hero):\n    return hero["name"]\n'), fails_at=2,
             message_contains='still reads `"name"`'),
        dict(why="CP3 step 1 copied: get_name handed over again, not the new function",
             code=_mapped(MAP_NAMES, GET_MANA_DEF, "manas = list(map(get_name, roster))\nprint(manas)\n"), fails_at=3,
             message_contains="Make `manas` with `list(map(get_mana, roster))`"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="map,func-as-value,return-value", solo="false",
             dictates="1", foreign_names="double,costs,shout,n", par="Pell 7/12, Brakka 15/16") + "\n"
        "6-A2 try-it. Introduces call:map (optional only). CP1 [D] `list(map(get_name, roster))`: a map object, "
        "`[]`, a list of `None` and a typed list each get a message; `map()` must be used (a for/append loop is "
        "right but fails 'Make it with `map()`'); CMB with Pell, Brakka and Moss set after setup. CP2 [ND] "
        "`get_mana(hero)`, RET with two fresh sheets: print for return, `\"max_mana\"`, `lucky[...]`, a near-miss "
        "key, `get_name`'s `\"name\"` key left in a copy. CP3 [ND] the same map with the student's own function "
        "(a lambda there also passes), printed; step 1 copied with `get_name` fails. With `()`, the order swapped, the "
        "name in quotes and one call's result handed over are Python's errors (the explainer's rows). The "
        "predict shows why a mapped function must return. Gearshift's bonus uses a lambda (prerequisite: the "
        "6-A1 article, named in its text); its check wants `\"magical_affinity\"` read in the lambda (the setup "
        "heroes are at full mana, so `\"max_mana\"` and `\"mana\"` would give the same list) and a rerun with "
        "Pell, Brakka and Moss printing [12, 16, 10]."
    ),
)

MAP_ARTICLE = dict(
    kind="article",
    id="map",
    title="map(): One Function, Every Item",
    optional=True,
    minutes=10,
    summary="Hand `map()` a function and a list: it calls the function on every item and collects the answers.",
    introduces=["call:map"],
    body=(
        "You have handed functions over before: `cast_on_everyone(roster, warm_hands)`. Python has one such "
        "helper built in: [[map()]].\n"
        "`map()` takes a function and a list. It calls the function on every item, in order, and collects what "
        "each call returns.\n"
        "```python\ncosts = [2, 6, 10]\ndoubled = list(map(double, costs))\n```\n"
        "Now `doubled` is `[4, 12, 20]`. Like `range()`, `map()` keeps its answers hidden until you wrap it in "
        "`list()`.\n"
        "The function goes first, with no `()`, because `map()` does the calling. The list goes second. In the "
        "wrong order, Python stops: *'function' object is not iterable*.\n"
        "The function must `return` its answer. If it only prints, `map()` collects `None` for every item.\n"
        "A [[lambda]] fits well here (see the lambda article): `list(map(lambda n: n * 2, costs))`.\n"
        "`map()` saves you a loop. This does the same job:\n"
        "```python\ndoubled = []\nfor cost in costs:\n    doubled.append(double(cost))\n```"
    ),
    examples=[
        dict(code=DOUBLE_EXAMPLE, output="[4, 12, 20]"),
        dict(code="affs = [9, 10, 12, 13]\ndoubled = map(lambda a: a * 2, affs)\nprint(list(doubled))\n",
             output="[18, 20, 24, 26]"),
        dict(code="halves = []\nfor n in [18, 20, 24, 26]:\n    halves.append(n // 2)\nprint(halves)\n",
             output="[9, 10, 12, 13]"),
    ],
    exercises=[MAP_NAMES_EXERCISE],
    notes=(
        "meta: path=optional. 6-A2 (O, 10 min). Introduces call:map. The lambda example and Gearshift's bonus name "
        "their prerequisite, the 6-A1 article (core-only rule, 2.12 rule 2: an optional item may use an earlier "
        "optional token when it names the item). The loop example uses u06a's `for` and u04a's `.append`."
    ),
)


# =============================================================================================
# Article 6-A3 "Two Things Back" (optional; a recap card for node:Tuple, from 3-A1), with one try-it
# =============================================================================================

PARTS_COMMENT = (
    "    # 1. Return two values: the\n"
    "    #    hero's mana, then the mana\n"
    "    #    used.\n"
)
PARTS_RETURN = '    return hero["mana"], hero["max_mana"] - hero["mana"]\n'
PARTS_STEP2 = "# 2. Catch both, then draw the bar.\n"
PARTS_DRAW = 'full, empty = bar_parts(lucky)\nprint("█" * full + "░" * empty)\n'


def _parts(ret="    pass\n", draw=""):
    return "def bar_parts(hero):\n" + PARTS_COMMENT + ret + "\n\n" + REST_LUCKY + "\n" + PARTS_STEP2 + draw


PARTS_STARTER = _parts()
PARTS_SOLUTION = _parts(PARTS_RETURN, PARTS_DRAW)
assert PARTS_STARTER == (
    "def bar_parts(hero):\n"
    "    # 1. Return two values: the\n"
    "    #    hero's mana, then the mana\n"
    "    #    used.\n"
    "    pass\n"
    "\n"
    "\n"
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 20,\n'
    '    "max_mana": 26,\n'
    "}\n"
    "\n"
    "# 2. Catch both, then draw the bar.\n"
)
LOOT_EXAMPLE = (
    "def split_loot(coins, heroes):\n"
    "    share = coins // heroes\n"
    "    spare = coins % heroes\n"
    "    return share, spare\n"
    "\n\n"
    "share, spare = split_loot(17, 4)\n"
    'print("Each hero gets", share)\n'
    'print("Lucky keeps", spare)\n'
)

_PARTS_BACK = r'''
_f = _need('bar_parts', ['hero'])
_d = _defs().get('bar_parts')
_rets = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return' and _n.value is not None]
_outer = [_x.id for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id in ('lucky',)]
for _nm, _mana, _full in (('Pell', 7, 12), ('Brakka', 15, 16)):
    _h = {'name': _nm, 'mana': _mana, 'max_mana': _full}
    _what = 'called `bar_parts` with a sheet for ' + _nm + ', mana ' + str(_mana) + ' of ' + str(_full)
    _val, _rows, _e = _call(_f, (_h,))
    if _e is not None:
        _k = _e.args[0] if type(_e).__name__ == 'KeyError' and _e.args else None
        assert not (type(_k).__name__ == 'str' and (_close(_k, 'mana') or _close(_k, 'max_mana'))), (
            'Use the keys `"mana"` and `"max_mana"`, letter for letter: the sheet has no key `"' + _k + '"`.' + _ev(_what))
        assert False, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
    _want = (_mana, _full - _mana)
    _two = type(_val).__name__ in ('tuple', 'list') and len(_val) == 2
    if _two and tuple(_val) == _want:
        continue
    if _val is None:
        assert not _rows, ('Use `return` in place of `print`, so both values go back to the caller.'
                           + _ev(_what, 'it printed them, then returned `None`'))
        assert False, ('Return both values with one `return`, a comma between them.'
                       + _ev(_what, 'it returned `None`'))
    assert not (type(_val).__name__ in ('int', 'float') and len(_rets) >= 2), (
        'Put both values on one `return`, with a comma between. The first `return` ends the function, so the '
        'second never runs.' + _ev(_what, 'it returned one number, ' + _show(_val)))
    assert type(_val).__name__ not in ('int', 'float'), ('Return two values, with a comma between them.'
                                                       + _ev(_what, 'it returned one number, ' + _show(_val)))
    assert not (type(_val).__name__ in ('tuple', 'list') and len(_val) != 2), (
        'Return exactly two values: the mana, then the mana used.' + _ev(_what, 'it returned ' + str(len(_val))))
    assert type(_val).__name__ in ('tuple', 'list'), 'Return two values, with a comma between them.' + _ev(_what)
    assert not [_x for _x in _val if type(_x).__name__ == 'str'], ('Take the quotes off: return the values from the '
                                                                   'sheet, not text. ' + _QUOTES)
    _consts = [_x for _n in _rets for _x in _ast.walk(_n.value) if type(_x).__name__ == 'Constant'
               and type(_x.value).__name__ in ('int', 'float')]
    assert not _consts, ('Read both values from the sheet `hero`, not typed numbers.'
                         + _ev(_what, 'it returned (' + str(_val[0]) + ', ' + str(_val[1]) + ')'))
    assert tuple(_val) != (_want[1], _want[0]), ('Put the mana first, then the mana used.'
                                                 + _ev(_what, 'it returned (' + str(_want[1]) + ', ' + str(_want[0]) + ')'))
    assert not _outer, ('Read the parameter `hero`, not `lucky`, so each hero handed over is the one read.'
                        + _ev(_what, 'it returned the same values for every hero'))
    assert _val[0] == _mana, 'The first value is the mana: `hero["mana"]`.' + _ev(_what, 'it returned ' + _show(_val[0]) + ' first')
    assert _val[1] != _full, ('The second value is the mana used: `hero["max_mana"] - hero["mana"]`.'
                              + _ev(_what, 'it returned the max mana, ' + str(_full)))
    assert False, ('The second value is the mana used: `hero["max_mana"] - hero["mana"]`.'
                   + _ev(_what, 'it returned ' + _show(_val[1]) + ', not ' + str(_want[1])))
'''

_BAR_DRAWN = r'''
_calls = [_n for _n in _top() if type(_n).__name__ == 'Assign' and _calls_in([_n.value], 'bar_parts')]
# A call caught in one name and unpacked on the next line (`parts = bar_parts(lucky)`, `full, empty = parts`) counts.
_caught = [_x for _n in _calls for _x in _made_by(_n)]
_pair = [_n for _n in _top() if type(_n).__name__ == 'Assign' and type(_n.targets[0]).__name__ == 'Tuple'
         and (_calls_in([_n.value], 'bar_parts') or (type(_n.value).__name__ == 'Name' and _n.value.id in _caught))]
if not _pair:
    assert not _calls, ('Catch both values, one name each: `full, empty = bar_parts(lucky)`. One name catches the '
                        'whole tuple.')
    _typed = [_n for _n in _top() if type(_n).__name__ == 'Assign' and 'full' in _made_by(_n)]
    assert not _typed, ('Catch them from the call: `full, empty = bar_parts(lucky)`. Typed numbers never follow the '
                        'sheet.')
    assert False, 'Under step 2, catch both values: `full, empty = bar_parts(lucky)`.'
_ts = [_x.id for _x in _pair[-1].targets[0].elts if type(_x).__name__ == 'Name']
assert _ts != ['empty', 'full'], ('Swap the names: `full, empty = bar_parts(lucky)`. The first name catches the '
                                  'first value, the mana.')
assert _ts == ['full', 'empty'], 'Name them `full` and `empty`, in that order: `full, empty = bar_parts(lucky)`.'
def _drawn(_ls, _f, _m):
    # A line that holds this bar, and no other blocks (a label like "Lucky: " in front is fine).
    _b = '█' * _f + '░' * _m
    return [_l for _l in _ls if _b in _l and _l.count('█') == _f and _l.count('░') == _m]
_bar = '█' * 20 + '░' * 6
if not _drawn(_lines(), 20, 6):
    assert not [_l for _l in _lines() if '█' * 20 + ' ' + '░' * 6 in _l], (
        'Join the two parts with `+`, not a comma: a comma adds a space.')
    assert not [_l for _l in _lines() if _words(_l) == ['20', '6']], (
        'Draw the bar: `print("█" * full + "░" * empty)`. Your line prints the two numbers.')
    assert False, 'Print the bar: `print("█" * full + "░" * empty)`, 20 full blocks, then 6 empty ones.'
_ns, _ls, _e, _miss, _log = _rerun([('lucky', __OTHER__)])
_what = 'ran your program again with a sheet for Pell, mana 7 of 12, in `lucky`'
assert _e is None, 'Mend this, then Run again: ' + _err(_e) + _ev(_what, 'Python stopped')
assert _drawn(_ls, 7, 5), ('Draw the bar from `full` and `empty`, not typed numbers.'
                           + _ev(_what, 'the bar did not show 7 full blocks and 5 empty ones'))
_after = max(_n.lineno for _n in _pair)
_used = set(_x.id for _n in _top() if _n.lineno >= _after and _n not in _pair for _x in _ast.walk(_n)
            if type(_x).__name__ == 'Name' and type(_x.ctx).__name__ == 'Load')
_unused = [_x for _x in ('full', 'empty') if _x not in _used]
assert not _unused, ('Draw the bar from the two values you caught: `print("█" * full + "░" * empty)`. `' + _unused[0]
                     + '` is caught, then never used, and the bar reads the sheet again instead.')
'''

_BAR_NUMBERS = r'''
_want = 'Mana [' + '█' * 20 + '░' * 6 + '] 20/26'
assert _want in _lines(), ('Print `"Mana [" + "█" * full + "░" * empty + "] " + str(full) + "/" + str(full + empty)`, '
                           "like the campaign's bar.")
_ns, _ls, _e, _miss, _log = _rerun([('lucky', __OTHER__)])
assert 'Mana [' + '█' * 7 + '░' * 5 + '] 7/12' in _ls, (
    'Build the numbers from `full` and `empty` too, not typed ones.'
    + _ev('ran your program with a sheet for Pell, mana 7 of 12, in `lucky`', 'no line showed `] 7/12`'))
'''
# A fresh sheet for the bar reruns (an invented hero, so a typed 26, 20 or 6 can't follow it).
PELL_IN_LUCKY = 'lucky = {"name": "Pell", "mana": 7, "max_mana": 12}'

PARTS_EXERCISE = dict(
    id="the-bars-two-numbers",
    title="The bar's two numbers",
    martu=(
        "A mana bar needs two numbers: the full blocks, and the empty ones. One function can return both.\n"
        "Put a comma between them: `return a, b`. Python packs them into a [[tuple]], and the caller catches "
        "them with two names, in order: `full, empty = bar_parts(lucky)`. That is [[unpacking]]."
    ),
    example=LOOT_EXAMPLE,
    example_output="Each hero gets 4\nLucky keeps 1",
    names=["bar_parts", "hero", "full", "empty", "lucky"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=("def low_high(a, b):\n    return a, b\n    return b, a\n\n\n"
              "print(low_high(3, 8))\n"),
        choices=["(3, 8)", "(8, 3)", "(3, 8)\n(8, 3)", "3"],
        answer=0,
        explain=(
            "The first `return` sends back `(3, 8)` and ends the function. The second `return` never runs. Two "
            "values come back as one tuple, printed in round brackets."
        ),
    ),
    pair_talk="Before step 2, tell your partner what `full` and `empty` will hold for Lucky. Then check on your own screen.",
    starter=PARTS_STARTER,
    checkpoints=[
        dict(
            id="return-two",
            text="Make `bar_parts` return two values with one `return`: `hero[\"mana\"]`, then "
                 "`hero[\"max_mana\"] - hero[\"mana\"]`.",
            dictated=True,
            hints=[
                "Look at `pass` inside `bar_parts`. One `return` line takes its place, with a comma between the "
                "two values.",
                "In the Example, `return share, spare` sends back two values at once. They arrive as a tuple.",
                "Not two `return` lines: the first one ends the function, so the second never runs.",
                "Write `return hero[\"mana\"], hero[\"max_mana\"] - hero[\"mana\"]` in place of `pass`.",
            ],
            checks=[check("bar_parts returns the mana and the mana used", _PARTS_BACK)],
            pass_line="Gearshift: Two readings, one call. Efficient.",
        ),
        dict(
            id="catch-both",
            text="Catch both with `full, empty = bar_parts(lucky)`, then print `\"█\" * full + \"░\" * empty`.",
            dictated=True,
            hints=[
                "Under step 2. Two names on the left of `=`, a comma between them, in the order the values come "
                "back.",
                "In the Example, `share, spare = split_loot(17, 4)` catches 4 in `share` and 1 in `spare`.",
                "One name alone would catch the whole tuple, and `\"█\" * (20, 6)` stops Python.",
                "Write `full, empty = bar_parts(lucky)`, then `print(\"█\" * full + \"░\" * empty)`.",
            ],
            checks=[check("the bar is drawn from full and empty", _BAR_DRAWN, other=PELL_IN_LUCKY)],
            pass_line="Lucky: Twenty full. Six to go. Fine.",
        ),
    ],
    solution=PARTS_SOLUTION,
    partials=[_parts(PARTS_RETURN)],
    assemble=dict(
        lines=["def bar_parts(hero):", PARTS_RETURN.rstrip("\n"), 'lucky = {"name": "Lucky", "mana": 20, "max_mana": 26}',
               "full, empty = bar_parts(lucky)", 'print("█" * full + "░" * empty)'],
        distractors=['    return hero["mana"]', "full = bar_parts(lucky)", "empty, full = bar_parts(lucky)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two values, one trip",
            text=(
                "```text\nreturn 20, 6\n       |   |\n     (20, 6)   one tuple\n       |   |\n"
                "full, empty = ...\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Two bags from the market",
            text=(
                "You send someone to the market for bread and eggs. They come back once, carrying both. You take "
                "the bread in one hand and the eggs in the other, in the order you asked."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `bar_parts(lucky)` works out 20 and 26 - 20 = 6.\n"
                "2. `return 20, 6` sends back the tuple `(20, 6)`.\n"
                "3. `full, empty = ...` puts 20 in `full` and 6 in `empty`.\n"
                "4. `\"█\" * 20 + \"░\" * 6` draws the bar."
            ),
        ),
        dict(
            angle="from Lists",
            label="Recap: tuples",
            text=(
                "A tuple is like a list in round brackets that can't change: `(20, 6)`. You can read it by position, "
                "`parts[0]`, or unpack it into names. The Tuples article in Unit 4 has more."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants the numbers too, like the campaign's bar. Print `\"Mana [\"`, the bar, `\"] \"`, then "
            "`str(full) + \"/\" + str(full + empty)`, all joined with `+`."
        ),
        hints=[
            "One `print`, with every part joined by `+`.",
            "`str(full + empty)` is the max mana: 26.",
        ],
        checks=[check("the bar shows its numbers", _BAR_NUMBERS, other=PELL_IN_LUCKY)],
        solution=PARTS_SOLUTION + 'print("Mana [" + "█" * full + "░" * empty + "] " + str(full) + "/" + '
                                  "str(full + empty))\n",
    ),
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]\nempty = "░" * (caster["max_mana"] - caster["mana"])',
        why=(
            "`get_mana_bar(caster)` worked out the same two numbers: `caster[\"mana\"]` and "
            "`caster[\"max_mana\"] - caster[\"mana\"]`. `bar_parts` hands both back in one trip."
        ),
    ),
    takeaway="`return a, b` hands back two values as a tuple; `full, empty = bar_parts(lucky)` unpacks them in order.",
    wrong_answers=[
        dict(why="the starter (pass: None)", code=PARTS_STARTER, fails_at=1, message_contains="returned `None`"),
        dict(why="two return lines (the second never runs)",
             code=_parts('    return hero["mana"]\n    return hero["max_mana"] - hero["mana"]\n'), fails_at=1,
             message_contains="second never runs"),
        dict(why="one value only", code=_parts('    return hero["mana"]\n'), fails_at=1, message_contains="Return two values"),
        dict(why="print instead of return (the caller gets None)",
             code=_parts('    print(hero["mana"], hero["max_mana"] - hero["mana"])\n'), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the two values the other way round",
             code=_parts('    return hero["max_mana"] - hero["mana"], hero["mana"]\n'), fails_at=1,
             message_contains="mana first"),
        dict(why="the max mana, not the mana used", code=_parts('    return hero["mana"], hero["max_mana"]\n'),
             fails_at=1, message_contains="the max mana"),
        dict(why="the outer sheet, not the parameter",
             code=_parts('    return lucky["mana"], lucky["max_mana"] - lucky["mana"]\n'), fails_at=1,
             message_contains="not `lucky`"),
        dict(why="typed numbers (A-06/A-07 test values)", code=_parts("    return 20, 6\n"), fails_at=1,
             message_contains="not typed numbers"),
        dict(why="Lucky's max mana typed into the second value (numbers in ink)",
             code=_parts('    return hero["mana"], 26 - hero["mana"]\n'), fails_at=1, message_contains="not typed numbers"),
        dict(why="the second value typed (Lucky's 6)", code=_parts('    return hero["mana"], 6\n'), fails_at=1,
             message_contains="not typed numbers"),
        dict(why="the keys in quotes, not read", code=_parts('    return "mana", "max_mana"\n'), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="CP2 one name catches the whole tuple",
             code=_parts(PARTS_RETURN, 'full = bar_parts(lucky)\nprint("█" * full + "░" * 6)\n'), fails_at=0,
             message_contains="can't multiply sequence by non-int of type 'tuple'"),
        dict(why="CP2 the function stored, not called", code=_parts(PARTS_RETURN, 'full, empty = bar_parts\n'
                                                                     'print("█" * full + "░" * empty)\n'),
             fails_at=0, message_contains="cannot unpack non-iterable function object"),
        dict(why="CP2 the names the other way round",
             code=_parts(PARTS_RETURN, 'empty, full = bar_parts(lucky)\nprint("█" * full + "░" * empty)\n'),
             fails_at=2, message_contains="Swap the names"),
        dict(why="CP2 three names for two values",
             code=_parts(PARTS_RETURN, 'full, empty, extra = bar_parts(lucky)\n'), fails_at=0,
             message_contains="not enough values to unpack"),
        dict(why="CP2 a comma instead of + (an extra space)",
             code=_parts(PARTS_RETURN, 'full, empty = bar_parts(lucky)\nprint("█" * full, "░" * empty)\n'),
             fails_at=2, message_contains="not a comma"),
        dict(why="CP2 the numbers printed, not the bar",
             code=_parts(PARTS_RETURN, "full, empty = bar_parts(lucky)\nprint(full, empty)\n"), fails_at=2,
             message_contains="prints the two numbers"),
        dict(why="CP2 a typed bar (A-06/A-07 typed values)",
             code=_parts(PARTS_RETURN, 'full, empty = bar_parts(lucky)\nprint("█" * 20 + "░" * 6)\n'), fails_at=2,
             message_contains="not typed numbers"),
        dict(why="CP2 typed numbers caught, not the call",
             code=_parts(PARTS_RETURN, 'full, empty = 20, 6\nprint("█" * full + "░" * empty)\n'), fails_at=2,
             message_contains="Typed numbers never follow"),
        dict(why="CP2 the print inside bar_parts never gets the bar (None unpacked)",
             code=_parts('    print(hero["mana"], hero["max_mana"] - hero["mana"])\n', PARTS_DRAW), fails_at=0,
             message_contains="cannot unpack non-iterable NoneType object"),
        dict(why="CP2 both caught, then the bar read off the sheet again (the campaign's get_mana_bar shape copied; "
                 "the two values never used)",
             code=_parts(PARTS_RETURN, 'full, empty = bar_parts(lucky)\nprint("█" * lucky["mana"] + "░" * '
                                       '(lucky["max_mana"] - lucky["mana"]))\n'), fails_at=2,
             message_contains="is caught, then never used"),
        dict(why="CP2 the Example's names copied (share, spare: A-05/A-07/A-08 copied example names)",
             code=_parts(PARTS_RETURN, 'share, spare = bar_parts(lucky)\nprint("█" * share + "░" * spare)\n'),
             fails_at=2, message_contains="Name them `full` and `empty`"),
        dict(why="CP2 Lucky's max mana typed into the empty part (numbers in ink: A-06/A-07)",
             code=_parts(PARTS_RETURN, 'full, empty = bar_parts(lucky)\nprint("█" * full + "░" * (26 - full))\n'),
             fails_at=2, message_contains="not typed numbers"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="two-returns,tuple-unpack,return-value", solo="false",
             dictates="1,2", foreign_names="split_loot,coins,heroes,share,spare,low_high",
             par="Pell 7/12, Brakka 15/16", prerequisite="3-A1 tuples (recap card)") + "\n"
        "6-A3 try-it. Uses node:Tuple (3-A1, optional; the 'Recap: tuples' angle is the recap card for anyone "
        "who skipped it). CP1 [D] RET with two fresh sheets: two `return` lines (the second never runs), one "
        "value, print for return, the order swapped, max mana for mana used, `lucky[...]`, typed numbers, quoted "
        "keys. CP2 [D]: the AST must unpack a call into `full, empty` (one name, a typed pair, swapped names; a call "
        "caught in one name and unpacked on the next line also passes), the bar must print, then CMB with an "
        "invented sheet (Pell, 7 of 12) put in `lucky` after its line, so a typed 20, 6 or 26 can't follow it, and "
        "last both caught names must be read after the unpack (the bar read off the sheet again fails). The "
        "NoneType and tuple errors are Python's, proven by wrong answers. A list return also unpacks and passes. "
        "Lucky's bonus adds the campaign's `] 20/26` (its rerun wants `] 7/12`, so a typed 26 fails)."
    ),
)

TWO_BACK_ARTICLE = dict(
    kind="article",
    id="two-things-back",
    title="Two Things Back",
    optional=True,
    minutes=10,
    summary="One function, two answers: `return share, spare`, caught with `share, spare = ...`.",
    body=(
        "Sometimes a function works out two answers. Lucky splits 17 coins among 4 heroes: each gets 4, and 1 is "
        "left over. Why not hand back both?\n"
        "Put a comma between them:\n"
        "```python\nreturn share, spare\n```\n"
        "Python packs the two values into a [[tuple]]. (Recap: a tuple is like a list in round brackets that can't "
        "change, `(4, 1)`. The Tuples article in Unit 4 has more.)\n"
        "The caller can catch both at once, one name for each, in order. That is [[unpacking]]:\n"
        "```python\nshare, spare = split_loot(17, 4)\n```\n"
        "Now `share` holds 4 and `spare` holds 1.\n"
        "Three slips to watch. Two `return` lines don't send two values: the first `return` ends the function, "
        "so the second never runs. One name on the left catches the whole tuple, `(4, 1)`. And the count must "
        "match: three names for two values stops Python with *not enough values to unpack*."
    ),
    examples=[
        dict(code="def split_loot(coins, heroes):\n    share = coins // heroes\n    spare = coins % heroes\n"
                  "    return share, spare\n\n\nprint(split_loot(17, 4))\n", output="(4, 1)"),
        dict(code=LOOT_EXAMPLE, output="Each hero gets 4\nLucky keeps 1"),
    ],
    exercises=[PARTS_EXERCISE],
    notes=(
        "meta: path=optional; prerequisite=3-A1 (recap card). 6-A3 (O, 10 min). Introduces nothing: node:Tuple is "
        "3-A1's (u04c), and the body carries the recap card the curriculum asks for when 3-A1 was skipped. The "
        "split uses Unit 1's `//` and `%`. The errors are shown as words (an example that crashes can't be "
        "verified)."
    ),
)


# =============================================================================================
# Quick Check Recipes II (forms A and B: four code tasks each as testout items)
# =============================================================================================
#
# Messages are lean (the Unit 2 ruling, as QC2): each names the slip and the evidence, never the fix and never the
# finished line. Every exercise is support="none" and explainer="lean". Check data uses invented Tor names only.

LESSON_6B = "Recipes That Read Stat Sheets"
LESSON_6C = "Spells You Can Hand Over"


def _stuck(lesson, *exercises):
    """Per skill, never "a whole lesson": the exercises that teach this task, then the lesson they sit in."""
    named = " and ".join(f"*{title}*" for title in exercises)
    return f"Stuck? Skip it, or try {named} in the lesson {lesson}. Tasks you pass here stay ticked."


def _qc_meta(skills, form, foreign="", level="S2", dictates=""):
    return meta(starter_level=level, path="QC-R2", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# Each form's names. A: Oogrish's wards; B: Bomb Shell's charms.
FORMS = {
    "A": dict(
        book="wards", page="ward", name_p="ward_name", learn="learn_ward", use="use_ward", cast="cast_ward",
        known="known", hero_var="oogrish", hero="Oogrish", mana=18, spend=3,
        first=("Ash Ward", 4, "ash_ward", "smokes."), second=("Sun Ward", 6, "sun_ward", "glows."),
        unknown="Moon Step", draw="draw_row", build="build_bar", show="show_row", block="█",
        fresh_learn=("Frost Veil", "Rust Ward"), fresh_use=("Frost Veil", "Glow", "Ember Wall"),
    ),
    "B": dict(
        book="charms", page="charm", name_p="charm_name", learn="learn_charm", use="use_charm", cast="cast_charm",
        known="known", hero_var="bomb_shell", hero="Bomb Shell", mana=24, spend=2,
        first=("Teal Shield", 5, "teal_shield", "hides."), second=("Spark Net", 3, "spark_net", "sparks."),
        unknown="Ember Wall", draw="draw_gauge", build="build_gauge", show="show_gauge", block="▮",
        fresh_learn=("Moon Step", "Glimmer"), fresh_use=("Moon Step", "Glimmer", "Rust Ward"),
    ),
}


def _hero_sheet(f, extra=""):
    return (f"{f['hero_var']} = {{\n    \"name\": \"{f['hero']}\",\n    \"mana\": {f['mana']},\n" + extra + "}\n")


def _effect_def(fn, line):
    return f"def {fn}(hero):\n    print(hero[\"name\"], \"{line}\")\n"


# ---- C1: build a dict from parameters with exact keys, and store it by name (dict-from-params, store-by-name) ----

_LEARN_PRE = r'''
_fn, _bk, _pv, _np = __FN__, __BOOK__, __PAGE__, __NAMEP__
_f = _need(_fn, [_bk, _np, 'mana_cost', 'effect'], True)
_d = _defs().get(_fn)


def _spark(_h=None):
    return None


def _glimmer(_h=None):
    return None


def _glow(_h=None):
    return None


_cases = ((__N1__, 7, _spark), (__N2__, 2, _glimmer))


def _run(_name, _cost, _fx):
    _book = {'Glow': {'mana_cost': 1, 'effect': _glow}}
    _loc, _val, _rows, _e = _capture(_f, (_book, _name, _cost, _fx))
    return _book, _loc, _val, _e
'''

_LEARN_BUILT = _LEARN_PRE + r'''
for _name, _cost, _fx in _cases:
    _book, _loc, _val, _e = _run(_name, _cost, _fx)
    _what = 'called `' + _fn + '` with a ' + _pv + ' called "' + _name + '", cost ' + str(_cost)
    assert _e is None, 'Inside `' + _fn + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
    _w = _loc.get(_pv)
    if type(_w).__name__ != 'dict' and type(_book.get(_name)).__name__ == 'dict':
        _w = _book[_name]
    if type(_w).__name__ != 'dict':
        assert _pv in _loc, 'No dictionary called `' + _pv + '` is made inside `' + _fn + '`.' + _ev(_what)
        assert False, '`' + _pv + '` holds ' + _show(_w) + ', not a dictionary.' + _ev(_what)
    for _k in ('mana_cost', 'effect'):
        if _k in _w:
            continue
        assert 'spell_function' not in _w or _k != 'effect', (
            '`' + _pv + '` has the campaign key `"spell_function"`, and this book reads `"effect"`.' + _ev(_what))
        _x = [_y for _y in _w if type(_y).__name__ == 'str' and _close(_y, _k)]
        assert not _x, ('`' + _pv + '` has a key `"' + (_x or [''])[0] + '"`, and the book reads `"' + _k + '"`: the '
                        'names do not match letter for letter.' + _ev(_what))
        _odd = [_y for _y in _w if type(_y).__name__ != 'str']
        assert not _odd, ('A key of `' + _pv + '` has no quotes, so it is a value, not a name: '
                          + _show((_odd or [None])[0]) + '.' + _ev(_what))
        assert False, '`' + _pv + '` has no key `"' + _k + '"`.' + _ev(_what)
    _mc, _ef = _w['mana_cost'], _w['effect']
    assert not (_mc is _fx and _ef == _cost), ('The two values are swapped: `"mana_cost"` holds the effect, and '
                                               '`"effect"` holds the cost.' + _ev(_what))
    assert not (type(_mc).__name__ == 'str' and _mc == 'mana_cost'), (
        '`' + _pv + '["mana_cost"]` holds text: a parameter name in quotes. ' + _QUOTES + _ev(_what))
    assert type(_mc).__name__ != 'str', ('`' + _pv + '["mana_cost"]` holds text, and the cost handed in was the '
                                         'number ' + str(_cost) + '.' + _ev(_what))
    assert _mc == _cost, ('`' + _pv + '["mana_cost"]` holds ' + _show(_mc) + ', and the cost handed in was '
                          + str(_cost) + '.' + _ev(_what))
    if _ef is not _fx:
        _ran = _calls_in([_d], 'effect')
        assert not (_ef is None and _ran), ('`"effect"` holds `None`: the `()` after `effect` ran it while the '
                                            + _pv + ' was being made.' + _ev(_what))
        assert _ef is not None, '`"effect"` holds `None`, the placeholder.' + _ev(_what)
        assert type(_ef).__name__ != 'str', '`"effect"` holds text: a name in quotes. ' + _QUOTES + _ev(_what)
        assert False, '`"effect"` holds ' + _show(_ef) + ', not the effect handed in.' + _ev(_what)
'''

_LEARN_STORED = _LEARN_PRE + r'''
for _name, _cost, _fx in _cases:
    _book, _loc, _val, _e = _run(_name, _cost, _fx)
    _what = 'called `' + _fn + '` with a book that holds Glow, and a ' + _pv + ' called "' + _name + '"'
    assert _e is None, 'Inside `' + _fn + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
    _new = [_k for _k in _book if _k != 'Glow']
    if _name not in _book:
        assert _np not in _book, ('The book got a page called `"' + _np + '"`: the parameter name in quotes. '
                                  + _QUOTES + _ev(_what))
        assert not (_new and _new[0] in __SHOWN__), ('The book got a page called `"' + _new[0] + '"`, a name typed in, '
                                                     'not the name handed in.' + _ev(_what))
        _qn = [_k for _k in _new if type(_k).__name__ == 'str' and (_k == 'name' or _close(_k, _np) or _close(_k, _pv))]
        assert not _qn, ('The book got a page called `"' + (_qn or [''])[0] + '"`: a name from the code in quotes, '
                         'not the name handed in. ' + _QUOTES + _ev(_what))
        assert not _new, 'The book got a page under a name typed in, not under the name handed in.' + _ev(_what)
        assert _loc.get(_bk) is _book, ('`' + _bk + ' = ...` inside `' + _fn + '` made a new dictionary that only the '
                                        'function can see: the book handed in did not change.' + _ev(_what))
        assert type(_val).__name__ != 'dict', ('`' + _fn + '` returned the ' + _pv + ', and the book handed in did not '
                                               'change.' + _ev(_what))
        assert False, 'The book handed in has no page for "' + _name + '".' + _ev(_what)
    assert 'Glow' in _book, 'The page that was already in the book, Glow, is gone.' + _ev(_what)
    _extra = [_k for _k in _book if _k not in ('Glow', _name)]
    assert not _extra, ('The book got a second page too, ' + ('called `"' + _extra[0] + '"`' if _extra[0] in __SHOWN__
                        else 'under a name typed in') + ', and only the name handed in was asked for.' + _ev(_what))
    _pg = _book[_name]
    assert type(_pg).__name__ != 'str', 'The "' + _name + '" page holds text, not the ' + _pv + '.' + _ev(_what)
    assert type(_pg).__name__ == 'dict' and _pg.get('mana_cost') == _cost and _pg.get('effect') is _fx, (
        'The "' + _name + '" page holds ' + _show(_pg) + ', not the ' + _pv + ' that was built.' + _ev(_what))
'''

# CP3 reads the student's own book after their program ran: the bottom call must hand the effect over with no `()`.
_LEARN_HANDED = r'''
_bk, _fx, _nm = __BOOK__, __EFFECT__, __NAME__
_want, _m = _find(_fx, True)
assert _want, _m
_book = _g.get(_bk)
assert type(_book).__name__ == 'dict', 'After the bottom call, `' + _bk + '` holds ' + _show(_book) + ', not a book.'
_pg = _book.get(_nm)
assert type(_pg).__name__ == 'dict' and 'effect' in _pg, ('After the bottom call, `' + _bk + '` has no "' + _nm
                                                         + '" page with an effect.')
_v = _pg['effect']
if _v is not _want:
    assert not (type(_v).__name__ == 'int' and _v == 0), 'The effect handed in is still 0.'
    assert type(_v).__name__ != 'str', 'The effect handed in is text: a name in quotes. ' + _QUOTES
    assert _v is not None, 'The effect is `None`: the `()` after the name ran it in the call.'
    assert False, 'The effect handed in is ' + _show(_v) + ', not the function `' + _fx + '`.'
'''


def _qc_learn(form):
    f = FORMS[form]
    name, cost, fn, line = f["first"]
    book, page, name_p, learn = f["book"], f["page"], f["name_p"], f["learn"]
    head = _effect_def(fn, line) + "\n\n" + f"def {learn}({book}, {name_p}, mana_cost, effect):\n"
    comment = (
        f"    # 1. Make {page}: a dictionary\n"
        "    #    with the keys \"mana_cost\"\n"
        "    #    and \"effect\", holding the\n"
        "    #    matching parameters.\n"
        f"    # 2. Store {page} in {book},\n"
        f"    #    with {name_p} as the key.\n"
    )
    # Step 3 (the honest fast path: func-as-value gated in code, not only by Q1): the bottom call holds a 0 where
    # the effect goes, and the student hands the function over in its place, with no `()`. The teacher's words,
    # wrapped at phone width (36 characters) so both forms fit.
    hand_comment = f"# 3. Hand {fn} over as\n#    the effect, in place of the 0.\n"
    good_dict = f"    {page} = {{\n        \"mana_cost\": mana_cost,\n        \"effect\": effect,\n    }}\n"
    good_store = f"    {book}[{name_p}] = {page}\n"

    def program(body=good_dict + good_store, hand=fn):
        return (head + comment + body + f"\n\n{book} = {{}}\n" + hand_comment
                + f"{learn}({book}, \"{name}\", {cost}, {hand})\nprint(\"{name}\" in {book})\n")

    def built(mc="mana_cost", ef="effect", k1='"mana_cost"', k2='"effect"', store=good_store, hand=fn):
        return program(f"    {page} = {{\n        {k1}: {mc},\n        {k2}: {ef},\n    }}\n" + store, hand)

    starter = program("    pass\n", "0")
    solution = program()
    n1, n2 = f["fresh_learn"]
    pre = dict(fn=learn, book=book, page=page, namep=name_p, n1=n1, n2=n2,
               shown=[f["first"][0], f["second"][0], f["unknown"]])
    other_sheet = '{"name": "' + f["hero"] + '"}'
    return dict(
        id=f"learn-a-{page}",
        title=f"Learn a {page}",
        martu=(
            f"`{learn}` builds a {page} from its parameters and stores it in the book under its name, like "
            "`add_spell` in the campaign. The book reads the keys `\"mana_cost\"` and `\"effect\"`, letter for "
            f"letter. The bottom call holds a 0 where the effect goes: hand `{fn}` over in its place. Mar'tu's "
            "check hands `" + learn + "` other names, costs and effects.\n" + _stuck(LESSON_6C, "Write the spell book")
        ),
        names=[learn, book, name_p, page, "mana_cost", "effect", fn],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id=f"build-the-{page}",
                text=f"Make `{page}` inside `{learn}`: a dictionary with the keys `\"mana_cost\"` and `\"effect\"`. "
                     "Each one holds its matching parameter.",
                dictated=False,
                hints=[
                    f"Look at comment 1 inside `{learn}`. The keys are in quotes; the values are the parameters, "
                    "with no quotes.",
                    "A value in a dictionary can be a parameter: `{\"fuel\": tank}` holds whatever `tank` was "
                    "handed.",
                    f"Start with `{page} = {{`, then one line for each key.",
                ],
                checks=[check(f"{page} holds the cost and the effect handed in", _LEARN_BUILT, **pre)],
                pass_line="Oogrish: The right names, the right values. Steady, now." if form == "A" else
                          "Bomb Shell: Keys match. Good.",
            ),
            dict(
                id=f"store-the-{page}",
                text=f"Store `{page}` in `{book}`, using `{name_p}` as the key.",
                dictated=False,
                hints=[
                    f"Look at comment 2. The book is the parameter `{book}`; the key is the parameter `{name_p}`.",
                    "`pantry[food] = jar` stores `jar` under the key that `food` holds, in the pantry handed in.",
                    f"Start with `{book}[`, then the name, then `=`.",
                ],
                checks=[check(f"the {page} is stored under its name", _LEARN_STORED, **pre)],
                # Honest on screen: the console shows `True` now; the check's own book (Glow) is never named.
                pass_line=f"Mar'tu: `True`. {name} is in the book. Its effect is still a 0.",
            ),
            dict(
                id=f"hand-over-the-{page}",
                text=f"In the bottom call, hand `{fn}` over as the effect.",
                dictated=False,
                hints=[
                    "Look at comment 3, above the bottom call. The 0 only holds the place where the effect goes.",
                    "`serve(soup)` hands the function `soup` over, to be called later. `serve(soup())` calls it "
                    "right now, and hands over what it returns.",
                    "Keep the first three values as they are. In place of the 0, write the function's name: no "
                    "quotes, and no `()`.",
                ],
                checks=[check(f"the book holds {fn} itself as the effect", _LEARN_HANDED, book=book, effect=fn,
                              name=name)],
                pass_line="Mar'tu: Handed over without cooking it. A function as a value, yes?",
            ),
        ],
        solution=solution,
        partials=[program(good_dict, "0"), program(good_dict + good_store, "0")],
        assemble=dict(
            lines=[ln for ln in solution.splitlines() if ln.strip() and not ln.lstrip().startswith("#")],
            distractors=[f"    {book}[\"{name_p}\"] = {page}", "        \"mana_cost\": \"mana_cost\",",
                         f"    {book} = {{{name_p}: {page}}}", f"{learn}({book}, \"{name}\", {cost}, {fn}())"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `{page} = {{...}}`: two keys in quotes, each holding the parameter of the same name, no quotes.\n"
                f"2. `{book}[{name_p}] = {page}` stores it in the book that was handed in, under its name.\n"
                f"3. In the bottom call, `{fn}` with no `()` hands the function itself over. With `()`, it would "
                "run right there.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "`add_spell` replaced each placeholder with the matching parameter, then stored the spell with "
                "`spell_book[spell_name] = spell`. Its call handed `strengthen_magic` over with no `()`.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="spell-book",
            snippet="spell_book[spell_name] = spell",
            why=(
                "This is `add_spell` with other names. The game read `\"mana_cost\"` letter for letter, so the key had "
                "to match exactly."
            ),
        ),
        takeaway=(f"Build `{page}` from the matching parameters, store it with `{book}[{name_p}] = {page}`, and hand "
                  f"`{fn}` over with no `()`."),
        wrong_answers=[
            dict(why="the starter (pass)", code=starter, fails_at=1, message_contains=f"No dictionary called `{page}`"),
            dict(why="CP3 the 0 placeholder left in the bottom call (steps 1 and 2 done)",
                 code=program(hand="0"), fails_at=3, message_contains="The effect handed in is still 0."),
            dict(why="CP3 the function handed over WITH () (it runs now, with no hero)", code=program(hand=f"{fn}()"),
                 fails_at=0, message_contains="missing 1 required positional argument: 'hero'"),
            dict(why="CP3 the function's name in quotes", code=program(hand=f"\"{fn}\""), fails_at=3,
                 message_contains="in quotes"),
            dict(why="CP3 called on a sheet in the call (its result, None, handed over)",
                 code=program(hand=f"{fn}({other_sheet})"), fails_at=3, message_contains="The effect is `None`"),
            dict(why="CP3 the parameter's name written in the bottom call (it lives only inside the function)",
                 code=program(hand="effect"), fails_at=0, message_contains="name 'effect' is not defined"),
            dict(why="CP3 another function handed over", code=program(hand=learn), fails_at=3,
                 message_contains=f"the function `{learn}`, not the function `{fn}`"),
            dict(why="CP3 called on the book in the call (the wrong sheet: the empty book has no name)",
                 code=program(hand=f"{fn}({book})"), fails_at=0, message_contains="KeyError: 'name'"),
            dict(why="CP1 the effect called while the dict is made, before step 3 (the 0 placeholder is called)",
                 code=built(ef="effect()", hand="0"), fails_at=0, message_contains="'int' object is not callable"),
            dict(why="CP1 typed values instead of the parameters (still the class's biggest slip: A-06/A-07)",
                 code=built(mc=str(cost), ef=fn), fails_at=1, message_contains=f"holds `{cost}`"),
            dict(why="CP1 the typed effect (the function from the starter)", code=built(ef=fn), fails_at=1,
                 message_contains=f"the function `{fn}`, not the effect handed in"),
            dict(why="CP1 a parameter quoted inside the dict ({\"mana_cost\": \"mana_cost\"})",
                 code=built(mc='"mana_cost"'), fails_at=1, message_contains="a parameter name in quotes"),
            dict(why="CP1 an approximate key (\"cost\" for \"mana_cost\")", code=built(k1='"cost"'), fails_at=1,
                 message_contains='a key `"cost"`'),
            dict(why="CP1 a key with capitals", code=built(k1='"Mana_Cost"'), fails_at=1,
                 message_contains='a key `"Mana_Cost"`'),
            dict(why="CP1 the campaign's key copied (\"spell_function\")", code=built(k2='"spell_function"'),
                 fails_at=1, message_contains='"spell_function"'),
            dict(why="CP1 keys with no quotes", code=built(k1="mana_cost", k2="effect"), fails_at=1,
                 message_contains="has no quotes"),
            dict(why="CP1 the two values swapped", code=built(mc="effect", ef="mana_cost"), fails_at=1,
                 message_contains="swapped"),
            dict(why="CP1 the effect called while the dict is made (with ())", code=built(ef="effect()"), fails_at=0,
                 message_contains="missing 1 required positional argument: 'hero'"),
            dict(why="CP2 the parameter's name quoted as the key", code=built(store=f"    {book}[\"{name_p}\"] = {page}\n"),
                 fails_at=2, message_contains=f"page called `\"{name_p}\"`"),
            dict(why="CP2 the name typed as the key", code=built(store=f"    {book}[\"{name}\"] = {page}\n"), fails_at=2,
                 message_contains=f"page called `\"{name}\"`"),
            dict(why="CP2 the book replaced inside the function (the caller never sees it)",
                 code=built(store=f"    {book} = {{{name_p}: {page}}}\n"), fails_at=2,
                 message_contains="only the function can see"),
            dict(why="CP2 the book emptied inside the function first (a new book the caller never sees)",
                 code=built(store=f"    {book} = {{}}\n" + good_store), fails_at=2,
                 message_contains="only the function can see"),
            dict(why="CP2 returned instead of stored (thinking the caller won't see a change)",
                 code=built(store=f"    return {page}\n"), fails_at=2, message_contains="returned the"),
            dict(why="CP2 the name in quotes stored as the page", code=built(store=f"    {book}[{name_p}] = \"{page}\"\n"),
                 fails_at=2, message_contains="holds text"),
            dict(why="CP2 key and value swapped (a dict can't be a key)", code=built(store=f"    {book}[{page}] = {name_p}\n"),
                 fails_at=0, message_contains="unhashable type: 'dict'"),
            dict(why="CP2 .append on a dictionary", code=built(store=f"    {book}.append({page})\n"), fails_at=0,
                 message_contains="has no attribute 'append'"),
            dict(why="CP2 an approximate quoted key (\"name\" for the parameter)",
                 code=built(store=f"    {book}[\"name\"] = {page}\n"), fails_at=2,
                 message_contains='page called `"name"`: a name from the code in quotes'),
            dict(why="CP2 stored under the name handed in AND under the starter's typed name (typed test values)",
                 code=built(store=good_store + f"    {book}[\"{name}\"] = {page}\n"), fails_at=2,
                 message_contains=f"a second page too, called `\"{name}\"`"),
        ],
        notes=_qc_meta("dict-from-params,store-by-name,func-as-value", form, "fuel,tank,pantry,food,jar,serve,soup")
        + "\n"
        f"QC-R2 C1, form {form}: `{learn}({book}, {name_p}, mana_cost, effect)`, the campaign's `add_spell` with other "
        f"names (the spec). Starter S2: two numbered comments and `pass` in `{learn}`; the bottom call learns {name} "
        f"({cost}) with a 0 where the effect goes, under comment 3, and prints `\"{name}\" in {book}` (False, then "
        "True). Three checkpoints. CP3 [ND] is the teacher's honest-fast-path fix: func-as-value is now gated in "
        f"code (C1 CP3), not only by Q1, so a student who misses Q1 still shows it. After the program runs, `{book}"
        f"[\"{name}\"][\"effect\"] is {fn}`. Lean messages, never the finished line: still 0; text (a name in quotes, "
        f"with the quotes sentence); `None` (`{fn}(...)` with a sheet ran it in the call); another function, named. "
        f"`{fn}()` crashes at the bottom call with Python's missing-argument line, `effect` with a NameError and "
        f"`{fn}({book})` with KeyError 'name' (lean explainer). Comment 3 keeps the teacher's words, wrapped at "
        "phone width so form B's longer name fits. CP2's pass line names only what the console shows (`True`), "
        "never the check's own book. CP1 [ND] PAR + KEY + SWAP: the check calls "
        f"`{learn}` with a fresh book holding Glow, {n1} (7) and {n2} (2), and stand-in effects, and reads the local "
        f"`{page}` as the call returns (a page built right in the store line also passes). Fails on (spec): literals "
        f"left -> PAR ('holds `{cost}`, and the cost handed in was 7'); the quoted parameter; approximate keys "
        "(`\"cost\"`, capitals, the campaign's `\"spell_function\"`), keys with no quotes, swapped values, the starter's "
        f"own `{fn}` typed in. CP2 [ND] KEY: `{book}[\"{name_p}\"]` (spec), a typed name, a rebinding the caller never "
        "sees, `return` instead of storing, `wards[\"name\"]` (a quoted name from the code, shown), a second page "
        "under the starter's typed name; Glow must stay. `effect()` and the swapped store crash at the bottom "
        "call (Python's lines; lean explainer). support='none', explainer='lean'.",
    )


# ---- C2: an early-return guard (early-return) ----

_GUARD_QC = r'''
_fn, _np, _kn, _cost, _hv, _pg = __FN__, __NAMEP__, __KNOWN__, __COST__, __HERO_VAR__, __PAGE__
_u, _k1, _k2 = __FRESH__
_f = _need(_fn, ['hero', _np], True)
_d = _defs().get(_fn)
_body = _d.body
_ifs = [_i for _i, _s in enumerate(_body) if type(_s).__name__ == 'If']
_work = [_i for _i, _s in enumerate(_body) if type(_s).__name__ in ('Assign', 'AugAssign')
         and [_t for _t in (_s.targets if type(_s).__name__ == 'Assign' else [_s.target]) if type(_t).__name__ == 'Subscript']]
_rets = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return']
_bare_ret = [_i for _i, _s in enumerate(_body) if type(_s).__name__ == 'Return']
_cmps = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Compare']
_typed = [_c for _c in _cmps if [_x for _x in [_c.left] + list(_c.comparators)
          if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str' and _x.value != _np]
          and not [_o for _o in _c.ops if type(_o).__name__ in ('In', 'NotIn')]]
_h = {'name': 'Pell', 'mana': 10, _kn: [_k1, _k2]}
_what = 'called `' + _fn + '` on a sheet for Pell, who knows ' + _k1 + ' and ' + _k2 + ', with "' + _u + '"'
_val, _rows, _e = _call(_f, (_h, _u))
assert _e is None, 'Inside `' + _fn + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
# The work's own line (given in the starter) must not show for an unknown name either: the function stops at the guard.
_raised = [_l for _l in _rows if _l.startswith('Raised:')]
if _h['mana'] != 10 or _raised:
    if not _ifs:
        _how = 'there is no guard yet, so the work ran'
    elif _work and min(_work) < min(_ifs):
        _how = 'the guard comes after the work'
    elif _typed:
        _how = 'the guard asks about a name typed in the `if`, not the one handed in'
    elif [_c for _c in _cmps if [_o for _o in _c.ops if type(_o).__name__ == 'In']]:
        _how = 'the guard stops only names the hero knows, and lets the others through'
    elif [_s for _s in _body if type(_s).__name__ == 'If' and _s.orelse] and not [
            _r for _s in _body if type(_s).__name__ == 'If' for _b in _s.body for _r in _ast.walk(_b)
            if type(_r).__name__ == 'Return']:
        _how = 'the guard is an `if`/`else` with no `return`, and the work below it still ran'
    elif not _rets:
        _how = 'there is no `return` under the guard, so the function carried on'
    else:
        _how = 'the function carried on past the guard'
    _saw = ("Pell's mana still went down, from 10 to " + str(_h['mana'])) if _h['mana'] != 10 else (
        "the mana stayed 10, but the work's line, `Raised:`, still printed")
    assert False, "With a name Pell doesn't know, " + _how + ': ' + _saw + '.' + _ev(_what)
assert _rows, "With a name Pell doesn't know, `" + _fn + '` printed nothing.' + _ev(_what)
assert [_l for _l in _rows if _u in _l], ("With a name Pell doesn't know, the line printed does not name the one "
                                          'handed in.' + _ev(_what))
_h2 = {'name': 'Brakka', 'mana': 9, _kn: [_u, _k1]}
_what2 = 'called `' + _fn + '` on a sheet for Brakka, who knows ' + _u + ' and ' + _k1 + ', with "' + _u + '"'
_val, _rows2, _e = _call(_f, (_h2, _u))
assert _e is None, 'Inside `' + _fn + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what2)
if _h2['mana'] != 9 - _cost:
    assert _h2['mana'] == 9, ('With a name Brakka knows, the mana went from 9 to ' + str(_h2['mana']) + ', and the '
                              "starter's comment says every " + _pg + ' costs ' + str(_cost) + '.' + _ev(_what2))
    _q = [_c for _c in _cmps if type(_c.left).__name__ == 'Constant' and _c.left.value == _np]
    _in = [_c for _c in _cmps if [_o for _o in _c.ops if type(_o).__name__ == 'In']]
    _whole = [_c for _c in _cmps if [_x for _x in _c.comparators if type(_x).__name__ == 'Name' and _x.id == 'hero']]
    _outer = [_x for _c in _cmps for _x in _ast.walk(_c) if type(_x).__name__ == 'Name' and _x.id == _hv]
    _list = [_c for _c in _cmps if [_x for _x in _c.comparators if type(_x).__name__ in ('List', 'Tuple')]]
    if _bare_ret and _work and min(_bare_ret) < min(_work):
        _how = 'the `return` is not inside the `if`, so every call stops there'
    elif _q:
        _how = 'the `if` asks about the text `"' + _np + '"`, a parameter name in quotes'
    elif _whole:
        _how = 'the `if` looks in the whole sheet, whose keys are name, mana and ' + _kn
    elif _outer:
        _how = 'the `if` looks in the list of `' + _hv + '`, the sheet outside, not of the hero handed in'
    elif _list:
        _how = "the `if` looks in a list typed in, not in the hero's own list"
    elif _typed:
        _how = "the `if` asks about names typed in, not about the hero's own list"
    elif _in:
        _how = 'the `if` turns away the names the hero knows'
    else:
        _how = 'the guard turned it away'
    assert False, ('With a name Brakka knows, ' + _how + ': the mana stayed ' + str(_h2['mana']) + '.' + _ev(_what2))
assert len(_rows2) == 1, ('With a name Brakka knows, ' + str(len(_rows2)) + ' lines printed: the guard spoke too.'
                          + _ev(_what2))
'''


def _qc_guard(form):
    f = FORMS[form]
    use, name_p, known = f["use"], f["name_p"], f["known"]
    name1, name2, unknown, spend = f["first"][0], f["second"][0], f["unknown"], f["spend"]
    head = (
        f"def {use}(hero, {name_p}):\n"
        f"    # 1. Guard: if {name_p} is\n"
        f"    #    not in hero[\"{known}\"], print\n"
        "    #    a line that names it, then\n"
        "    #    return.\n"
    )
    work = (
        f"    # Every {f['page']} costs {spend} mana.\n"
        f"    hero[\"mana\"] = hero[\"mana\"] - {spend}\n"
        f"    print(\"Raised:\", {name_p})\n"
    )
    sheet = _hero_sheet(f, f"    \"{known}\": [\"{name1}\",\n              \"{name2}\"],\n")
    tail = (
        "\n\n" + sheet + f"{use}({f['hero_var']}, \"{name1}\")\n"
        f"# {f['hero']} doesn't know this:\n"
        f"{use}({f['hero_var']}, \"{unknown}\")\n"
    )
    guard = (
        f"    if {name_p} not in hero[\"{known}\"]:\n"
        f"        print(hero[\"name\"], \"doesn't know\", {name_p})\n"
        "        return\n"
    )

    def program(g=guard, w=work):
        return head + g + w + tail

    starter = program("")
    solution = program()
    nm = f"print(hero[\"name\"], \"doesn't know\", {name_p})"
    fresh = f["fresh_use"]
    return dict(
        id=f"guard-the-{f['page']}",
        title="Guard at the door",
        martu=(
            f"`{use}` spends the mana and raises the {f['page']}, even when the hero doesn't know it. Add a "
            f"[[guard]] at the top: a name the hero doesn't know gets one line, and the function stops there. Mar'tu's "
            "check tries other heroes and other names.\n" + _stuck(LESSON_6B, "Guard at the door")
        ),
        names=[use, name_p, "hero"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="add-the-guard",
                text=f"At the top of `{use}`, if `{name_p}` is not in `hero[\"{known}\"]`, print a line that names it, "
                     "then `return`.",
                dictated=False,
                hints=[
                    f"Look at comment 1, above the work. The guard comes first, so the mana line never runs for a "
                    "name the hero doesn't know.",
                    "`if food not in pantry:` asks first. A `return` under it, indented, ends the function right "
                    "there.",
                    f"Start with `if {name_p} not in`, then two indented lines: the `print`, then `return`.",
                ],
                checks=[check("an unknown name stops at the guard; a known one goes ahead", _GUARD_QC, fn=use,
                              namep=name_p, known=known, cost=spend, fresh=fresh, hero_var=f["hero_var"],
                              page=f["page"])],
                pass_line=(f"Mar'tu: {f['hero']} turned {unknown} away, and kept the mana. That is a guard, yes?"),
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[ln for ln in solution.splitlines() if ln.strip() and not ln.lstrip().startswith("#")],
            distractors=[f"    if {name_p} in hero[\"{known}\"]:", f"    if \"{name_p}\" not in hero[\"{known}\"]:",
                         "    else:"],
        ),
        another_way=[
            dict(angle="everyday", text=(
                "A guard checks your name at the door before anything else happens. If you are not on the list, "
                "you are turned away, and nothing inside happens.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "`cast_spell` opened with `if spell_name not in caster[\"spell_book\"]:`, one `print_prompt` line, "
                "and `return`. Everything below it ran only for a spell the caster knew.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="hold-the-barrier",
            snippet='if spell_name not in caster["spell_book"]:\n    print_prompt(...)\n    return',
            why="The opening of `cast_spell` was this guard: ask first, say why, and stop with `return`.",
        ),
        takeaway="A guard goes first: `if name not in book:`, one line, then `return`, so the work below never runs.",
        wrong_answers=[
            dict(why="the starter (no guard: the mana is spent for an unknown name)", code=starter, fails_at=1,
                 message_contains="no guard yet"),
            dict(why="no return under the guard (it carries on: the spec's CALL)",
                 code=program(guard.replace("        return\n", "")), fails_at=1,
                 message_contains="no `return` under the guard"),
            dict(why="the guard placed after the work (the early return comes too late)",
                 code=program(g="", w=work + guard), fails_at=1, message_contains="the guard comes after the work"),
            dict(why="a guard written as if/else that never returns",
                 code=program(f"    if {name_p} not in hero[\"{known}\"]:\n        {nm}\n    else:\n"
                              f"        print(hero[\"name\"], \"knows it.\")\n"), fails_at=1,
                 message_contains="`if`/`else` with no `return`"),
            dict(why="the unknown name typed in the if (A-06/A-07 typed test values)",
                 code=program(f"    if {name_p} == \"{unknown}\":\n        {nm}\n        return\n"), fails_at=1,
                 message_contains="a name typed in the `if`"),
            dict(why="in for not in (the names the hero knows are turned away)",
                 code=program(guard.replace(" not in ", " in ")), fails_at=1,
                 message_contains="stops only names the hero knows"),
            dict(why="the parameter in quotes", code=program(guard.replace(f"if {name_p} not", f"if \"{name_p}\" not")),
                 fails_at=1, message_contains="a parameter name in quotes"),
            dict(why="the whole sheet asked, not its list (the wrong place to look)",
                 code=program(guard.replace(f"hero[\"{known}\"]:", "hero:")), fails_at=1,
                 message_contains="the whole sheet"),
            dict(why="the outer hero's list asked, not the hero handed in (the wrong sheet)",
                 code=program(guard.replace("hero[\"" + known + "\"]:", f["hero_var"] + "[\"" + known + "\"]:")),
                 fails_at=1, message_contains="the sheet outside"),
            dict(why="the starter's names typed into the guard's list (typed test values)",
                 code=program(guard.replace("hero[\"" + known + "\"]:", f"[\"{name1}\", \"{name2}\"]:")),
                 fails_at=1, message_contains="a list typed in"),
            dict(why="the starter's names typed into != tests (typed test values, no list asked)",
                 code=program(f"    if {name_p} != \"{name1}\" and {name_p} != \"{name2}\":\n        {nm}\n        return\n"),
                 fails_at=1, message_contains="names typed in, not about"),
            dict(why="the line printed names no ward", code=program(guard.replace(nm, 'print("Not known.")')),
                 fails_at=1, message_contains="does not name the one"),
            dict(why="the guard's print not indented under the if (it speaks every time)",
                 code=program(f"    if {name_p} not in hero[\"{known}\"]:\n        return\n    {nm}\n"), fails_at=1,
                 message_contains="printed nothing"),
            dict(why="return not indented under the if (every call stops)",
                 code=program(f"    if {name_p} not in hero[\"{known}\"]:\n        {nm}\n    return\n"), fails_at=1,
                 message_contains="not inside the `if`"),
            dict(why="an if/else that never returns, with only the mana line moved under else (the mana is safe, but "
                     "the work's line still prints for an unknown name)",
                 code=program(f"    if {name_p} not in hero[\"{known}\"]:\n        {nm}\n    else:\n"
                              f"        hero[\"mana\"] = hero[\"mana\"] - {spend}\n",
                              f"    print(\"Raised:\", {name_p})\n"), fails_at=1,
                 message_contains="`Raised:`, still printed"),
            dict(why="the given work's cost changed (the known name spends the wrong amount)",
                 code=program(w=work.replace(f"- {spend}\n", f"- {spend + 1}\n")), fails_at=1,
                 message_contains=f"every {f['page']} costs {spend}"),
        ],
        notes=_qc_meta("early-return", form, "food,pantry") + "\n"
        f"QC-R2 C2, form {form}: `{use}(hero, {name_p})`, the opening of hold-the-barrier. The work below the comment "
        f"(spend {spend} mana, print a line) is given; the student writes the guard. One checkpoint [ND], CALL: the "
        f"check calls `{use}` on fresh sheets (Pell, who knows {fresh[1]} and {fresh[2]}, with {fresh[0]}; Brakka, who "
        f"knows {fresh[0]}, with {fresh[0]}). An unknown name must leave the mana alone and print one line that names "
        "it (any wording) and must not print the work's own `Raised:` line (an if/else with only the mana line under "
        "`else` fails there); a known name must spend exactly the starter's cost and print only the work's line. An "
        "if/else that keeps all the work under `else` behaves like a guard and passes. Fails on (spec): no `return` -> "
        "it carries on (CALL). Also the class's slips: the guard after the work, an if/else that falls through, the "
        f"starter's own `\"{unknown}\"` typed in the `if`, `in` for `not in`, the quoted parameter, the whole sheet "
        "asked, a line that names no ward, `return` or `print` unindented. Each diagnosis comes from the AST, named "
        "with the evidence and never the fix. support='none', explainer='lean'.",
    )


# ---- C3: return a value from a sheet, store-then-pass, and call a finished helper without changing it
# (sheet-return, store-then-pass, read-helper) ----

# CP1 (RET + PAR-CONST): the student's own `build_bar`, called on two new sheets whose bars differ, so a typed bar
# (the same for both) or the outer sheet can't pass.
_BAR_BUILT = r'''
_bf, _blk, _hv = __BUILD__, __BLOCK__, __HERO_VAR__
_f = _need(_bf, ['hero'], True)
_d = _defs().get(_bf)
_what = 'called `' + _bf + '` on two new sheets'
_got = []
for _nm, _mana in (('Pell', 7), ('Moss', 3)):
    _val, _rows, _e = _call(_f, ({'name': _nm, 'mana': _mana},))
    assert _e is None, 'Inside `' + _bf + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
    _got.append((_nm, _mana, _val, _rows))


def _bar_of(_v):
    # How many blocks, when the value is a bar made only of this form's block; else None.
    return len(_v) if type(_v).__name__ == 'str' and _v and _v == _blk * len(_v) else None


if [_x for _x in _got if _x[2] != _blk * _x[1]]:
    _nm, _mana, _val, _rows = _got[0]
    assert _val is not None, ('`' + _bf + '` returned `None` for ' + _nm + ', mana ' + str(_mana)
                              + ('; it showed the bar first' if [_l for _l in _rows if _blk in _l] else '') + '.'
                              + _ev(_what))
    assert not [_x for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id == _hv], (
        '`' + _bf + '` reads `' + _hv + '`, not the hero handed in.' + _ev(_what))
    _n = _bar_of(_val)
    assert _val != _got[1][2], ('`' + _bf + '` gave the same bar for Pell (mana 7) and Moss (mana 3)'
                                + ((': ' + str(_n) + (' block' if _n == 1 else ' blocks') + ' each') if _n else '')
                                + '.' + _ev(_what))
    for _nm, _mana, _val, _rows in _got:
        if _val == _blk * _mana:
            continue
        _n = _bar_of(_val)
        assert not _n, ('`' + _bf + '` returned a bar of ' + str(_n) + (' block' if _n == 1 else ' blocks') + ' for '
                        + _nm + ', mana ' + str(_mana) + '.' + _ev(_what))
        assert False, ('`' + _bf + '` returned ' + _show(_val) + ' for ' + _nm + ', mana ' + str(_mana) + ', not a bar '
                       'of `' + _blk + '`.' + _ev(_what))
'''

_ROW_STORED = r'''
_sf, _bf, _df, _blk, _hv = __SHOW__, __BUILD__, __DRAW__, __BLOCK__, __HERO_VAR__
_f = _need(_sf, ['hero'], True)
_h = {'name': 'Pell', 'mana': 7}
_what = 'called `' + _sf + '` on a sheet for Pell, mana 7'
_loc, _val, _rows, _e = _capture(_f, (_h,))
assert _e is None, 'Inside `' + _sf + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
_vals = [_v for _k, _v in _loc.items() if _k != 'hero']
if _blk * 7 not in _vals:
    assert not [_v for _v in _vals if _v is _g.get(_bf)], ('`' + _sf + '` stored the function `' + _bf + '` itself, '
                                                          'not what it returns.' + _ev(_what))
    _sd = _defs().get(_sf)
    _typed = [_n for _n in _ast.walk(_sd) if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Constant']
    assert not _typed, ('`' + _sf + '` stores a bar typed in quotes, not one built from the hero handed in.'
                        + _ev(_what))
    assert not [_x for _x in _ast.walk(_sd) if type(_x).__name__ == 'Name' and _x.id == _hv], (
        '`' + _sf + '` stored the bar of `' + _hv + '`, not of the hero handed in.' + _ev(_what))
    _passed = [_c for _c in _calls_in([_defs().get(_sf)], _df) if _calls_in(_c.args, _bf)]
    assert not _passed, ('`' + _bf + '(hero)` goes straight into `' + _df + '`: nothing is stored in a variable '
                         'first.' + _ev(_what))
    assert False, '`' + _sf + '` stores nothing that holds the bar of the hero handed in.' + _ev(_what)
assert _calls_in([_defs().get(_sf)], _bf), ('`' + _sf + '` builds the bar by hand, and `' + _bf
                                            + '` is never called.' + _ev(_what))
'''

_ROW_PASSED = r'''
_sf, _bf, _df, _blk, _hv = __SHOW__, __BUILD__, __DRAW__, __BLOCK__, __HERO_VAR__
assert _keep(_df, __ORIG__) == '', '`' + _df + '` is not as the starter wrote it: a finished helper changed.'
_f = _need(_sf, ['hero'], True)
_h = {'name': 'Brakka', 'mana': 5}
_what = ('called `' + _sf + '` on a sheet for Brakka, mana 5, with a pretend `' + _df + '` that only writes down what '
         'it is handed')
_val, _rows, _e, _rec = _stubbed(_f, (_h,), _df)
assert _e is None, 'Inside `' + _sf + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
assert _rec, '`' + _sf + '` never calls `' + _df + '`' + ('; it prints the bar itself' if _rows else '') + '.' + _ev(_what)
assert len(_rec) == 1, '`' + _df + '` ran ' + str(len(_rec)) + ' times for one hero.' + _ev(_what)
_a = _rec[0]
assert len(_a) == 2, ('`' + _df + '` was handed ' + str(len(_a)) + ' values, and its `def` line takes two.' + _ev(_what))
_bar = _blk * 5
assert not (_a[0] == _bar and _a[1] is _h), ('The two values are swapped: `' + _df + '` got the bar first and the '
                                            'hero second.' + _ev(_what))
assert not (_a[0] is _g.get(_hv)), '`' + _df + '` was handed `' + _hv + '`, not the hero handed in.' + _ev(_what)
assert _a[0] is _h, '`' + _df + '` was handed ' + _show(_a[0]) + ' first, not the hero handed in.' + _ev(_what)
assert not callable(_a[1]), '`' + _df + '` was handed the function `' + _bf + '` itself, not the bar.' + _ev(_what)
assert _a[1] == _bar, ('`' + _df + '` was handed ' + _show(_a[1]) + ' second, not the bar of the hero handed in.'
                       + _ev(_what))
_fresh = [_c for _c in _calls_in([_defs().get(_sf)], _df)
          for _x in list(_c.args) + [_k.value for _k in _c.keywords] if _calls_in([_x], _bf)]
assert not _fresh, ('`' + _df + '` was handed a new call of `' + _bf + '`, not the variable that stored the bar.'
                    + _ev(_what))
_sd = _defs().get(_sf)
_mine = set(_x for _n in _ast.walk(_sd) if type(_n).__name__ in ('Assign', 'AugAssign') for _x in _made_by(_n))
_handed = [(_c.args[1] if len(_c.args) >= 2 else ([_k.value for _k in _c.keywords if _k.arg == 'bar'] or [None])[0])
           for _c in _calls_in([_sd], _df)]
_built = [_b for _b in _handed if _b is not None and not (type(_b).__name__ == 'Name' and _b.id in _mine)]
assert not _built, ('`' + _df + '` was handed a bar built right in the call, not the variable that stored the bar.'
                    + _ev(_what))
'''

PANEL_SETUP = (
    "_panel = []\n"
    "\n\n"
    "def show_on_panel(hero, bar):\n"
    "    _panel.append((hero, bar))\n"
    "    try:\n"
    "        who = hero[\"name\"]\n"
    "    except Exception:\n"
    "        who = \"?\"\n"
    "    print(\"[Panel]\", who, bar)\n"
)


def _qc_helper(form):
    f = FORMS[form]
    draw, build, show, block, hv = f["draw"], f["build"], f["show"], f["block"], f["hero_var"]
    # The one finished helper (KEEP): read its `def` line, call it in its order, and leave it alone.
    helper = (
        f"def {draw}(hero, bar):\n"
        "    # Already finished. Leave it as\n"
        "    # it is. It shows bar in this\n"
        "    # hero's row of the panel.\n"
        "    show_on_panel(hero, bar)\n"
    )
    # The student's own `build_bar` (the honest fast path: objective 1, a function that takes a sheet and returns a
    # value, gated in code). Its starter body is `pass`, not `return ""` (the unit's starter rule).
    build_head = (
        "\n\n"
        f"def {build}(hero):\n"
        f"    # 1. Return a bar: one \"{block}\" for\n"
        "    #    each point of hero[\"mana\"].\n"
    )
    build_good = f"    return \"{block}\" * hero[\"mana\"]\n"
    head = (
        "\n\n"
        f"def {show}(hero):\n"
        "    # 2. Store the result of\n"
        f"    #    {build}(hero) in a\n"
        "    #    variable.\n"
        f"    # 3. Pass hero and that variable\n"
        f"    #    to {draw}.\n"
    )
    tail = "\n\n" + _hero_sheet(f) + f"{show}({hv})\n"
    store = f"    bar = {build}(hero)\n"
    pass_on = f"    {draw}(hero, bar)\n"

    def program(body=store + pass_on, bar=build_good, finished=helper):
        return finished + build_head + bar + head + body + tail

    starter = program("    pass\n", "    pass\n")
    solution = program()
    vals = dict(show=show, build=build, draw=draw, block=block, hero_var=hv)
    shape = "Bar" if form == "A" else "Gauge"
    return dict(
        id="read-the-helper",
        title="Build it, then pass it on",
        martu=(
            f"`{draw}` is a finished [[helper]]: read its `def` line and leave it alone. `{build}` is yours: it "
            f"returns the bar. Then finish `{show}` the campaign's way: store, then pass. Mar'tu's check tries other "
            f"heroes, and checks what `{draw}` is handed.\n"
            + _stuck(LESSON_6B, "Hand over a sheet", "Build the bar, then draw it")
        ),
        names=[show, build, draw, "hero"],
        setup=PANEL_SETUP,
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="build-the-bar",
                text=f"Make `{build}` return a bar: one `\"{block}\"` for each point of `hero[\"mana\"]`.",
                dictated=False,
                hints=[
                    f"Look at comment 1 inside `{build}`. The bar comes from the sheet handed in, and `return` hands "
                    "it back.",
                    "`*` repeats text: `\"*\" * 3` is `***`. A function that reads `box[\"eggs\"]` can repeat a star "
                    "that many times, and return it.",
                    f"Start with `return`, then one `\"{block}\"` times the mana on the sheet handed in.",
                ],
                checks=[check(f"{build} returns the bar of the hero handed in", _BAR_BUILT, **vals)],
                # Honest on screen: `show_row` is still `pass`, so the console is blank, and the line says so.
                pass_line=f"Gearshift: {shape} returned. Nothing on the panel yet: catch it next.",
            ),
            dict(
                id="store-the-bar",
                text=f"Inside `{show}`, store the result of `{build}(hero)` in a variable.",
                dictated=False,
                hints=[
                    f"Look at comment 2 inside `{show}`. The call goes on the right of `=`, a new variable on the left.",
                    "`greeting = get_greeting()` keeps what the call returns, so it can be passed on.",
                    f"Start with `bar = {build}(`, and hand it `hero`.",
                ],
                checks=[check("the bar of the hero handed in is stored", _ROW_STORED, setup=PANEL_SETUP, **vals)],
                pass_line="Gearshift: Stored. Ready to send." if form == "A" else "Gearshift: Gauge stored.",
            ),
            dict(
                id="pass-it-on",
                text=f"Pass `hero` and that variable to `{draw}`, in the order its `def` line asks.",
                dictated=False,
                hints=[
                    f"Look at the `def` line of `{draw}`: what does it take, and in what order?",
                    "`show_on_ley_board(text)` took one value. A helper with two parameters takes two values, in its "
                    "order.",
                    f"Start with `{draw}(hero,`, then the variable.",
                ],
                checks=[check(f"{draw} is handed the hero, then the bar", _ROW_PASSED, setup=PANEL_SETUP,
                              orig=helper, **vals)],
                pass_line="Mar'tu: The bar went to the panel, and the helper is as I left it. Yes.",
            ),
        ],
        solution=solution,
        partials=[program("    pass\n"), program(store)],
        assemble=dict(
            lines=[ln for ln in solution.splitlines() if ln.strip() and not ln.lstrip().startswith("#")],
            distractors=[f"    print(\"{block}\" * hero[\"mana\"])", f"    {draw}(bar, hero)", f"    bar = {build}",
                         f"    {draw}(hero, {build})"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `{build}`: `return` one `\"{block}\"` times `hero[\"mana\"]`, from the sheet handed in.\n"
                f"2. `bar = {build}(hero)`: call it with `()` and the hero, and keep what comes back.\n"
                f"3. `{draw}(hero, bar)`: the hero first, then the bar, as its `def` line says.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "`get_mana_bar(caster)` returned the bar. `show_mana(caster)` stored it in a variable, then passed "
                "the caster and that variable to `print_mana`, which said: already finished, leave it.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="mana-bars",
            snippet="mana_bar = get_mana_bar(caster)\nprint_mana(caster, mana_bar)",
            why=("The same two lines. `get_mana_bar` returned the bar, and `print_mana` was finished: you read its "
                 "`def` line and called it."),
        ),
        takeaway=("Return the bar from the sheet handed in, store it, then call the finished helper in its `def` "
                  "line's order."),
        wrong_answers=[
            dict(why="the starter (pass in both)", code=starter, fails_at=1,
                 message_contains="returned `None` for Pell, mana 7."),
            dict(why=f"CP1 {build} left as pass, {show} finished (nothing returned: the caller gets None)",
                 code=program(bar="    pass\n"), fails_at=1, message_contains="returned `None` for Pell, mana 7."),
            dict(why="CP1 print inside the function instead of return (the class's biggest slip)",
                 code=program(bar=f"    print(\"{block}\" * hero[\"mana\"])\n"), fails_at=1,
                 message_contains="returned `None` for Pell, mana 7; it showed the bar first"),
            dict(why=f"CP1 a typed bar, {hv}'s own (typed test values, still the class's biggest slip: PAR-CONST)",
                 code=program(bar=f"    return \"{block * f['mana']}\"\n"), fails_at=1,
                 message_contains=f"the same bar for Pell (mana 7) and Moss (mana 3): {f['mana']} blocks each"),
            dict(why=f"CP1 the outer sheet `{hv}` read, not the parameter (the wrong sheet)",
                 code=program(bar=f"    return \"{block}\" * {hv}[\"mana\"]\n"), fails_at=1,
                 message_contains=f"reads `{hv}`, not the hero handed in"),
            dict(why="CP1 one block, not one for each point of mana",
                 code=program(bar=f"    return \"{block}\"\n"), fails_at=1,
                 message_contains="the same bar for Pell (mana 7) and Moss (mana 3): 1 block each"),
            dict(why="CP1 a bar one block too long (the wrong length)",
                 code=program(bar=f"    return \"{block}\" * (hero[\"mana\"] + 1)\n"), fails_at=1,
                 message_contains="a bar of 8 blocks for Pell, mana 7"),
            dict(why="CP1 the mana returned, not a bar", code=program(bar="    return hero[\"mana\"]\n"), fails_at=1,
                 message_contains="returned `7` for Pell, mana 7, not a bar"),
            dict(why="CP1 another mark repeated (some text, not this form's block)",
                 code=program(bar="    return \"#\" * hero[\"mana\"]\n"), fails_at=1,
                 message_contains="returned some text for Pell, mana 7, not a bar"),
            dict(why="CP1 the parameter renamed on the def line",
                 code=program(bar=f"    return \"{block}\" * sheet[\"mana\"]\n").replace(
                     f"def {build}(hero):", f"def {build}(sheet):"), fails_at=1,
                 message_contains="has `sheet`, and the starter has `hero`"),
            dict(why=f"CP2 {show} left as pass ({build} done)", code=program("    pass\n"), fails_at=2,
                 message_contains="stores nothing"),
            dict(why="CP2 the function stored where its result was wanted",
                 code=program(f"    bar = {build}\n    {draw}(hero, bar)\n"), fails_at=2,
                 message_contains=f"stored the function `{build}` itself"),
            dict(why="CP2 the outer sheet read, not the parameter (the wrong sheet)",
                 code=program(f"    bar = {build}({hv})\n    {draw}(hero, bar)\n"), fails_at=2,
                 message_contains=f"the bar of `{hv}`"),
            dict(why="CP2 a typed bar (A-06/A-07 typed test values)",
                 code=program(f"    bar = \"{block * f['mana']}\"\n    {draw}(hero, bar)\n"), fails_at=2,
                 message_contains="typed"),
            dict(why="CP2 passed straight on, nothing stored", code=program(f"    {draw}(hero, {build}(hero))\n"),
                 fails_at=2, message_contains="nothing is stored"),
            dict(why=f"CP2 the bar built by hand in {show}, {build} never called (the function skipped)",
                 code=program(f"    bar = \"{block}\" * hero[\"mana\"]\n" + pass_on), fails_at=2,
                 message_contains=f"builds the bar by hand, and `{build}` is never called"),
            dict(why="CP3 stored, then a second call passed on instead of the variable",
                 code=program(store + f"    {draw}(hero, {build}(hero))\n"), fails_at=3,
                 message_contains="a new call of"),
            dict(why="CP2 printed instead of stored", code=program(f"    print({build}(hero))\n"), fails_at=2,
                 message_contains="stores nothing"),
            dict(why="CP3 the values in the wrong order (CALL)", code=program(store + f"    {draw}(bar, hero)\n"),
                 fails_at=3, message_contains="swapped"),
            dict(why="CP3 the function handed over where its result was wanted",
                 code=program(store + f"    {draw}(hero, {build})\n"), fails_at=3,
                 message_contains=f"the function `{build}` itself"),
            dict(why="CP3 the outer sheet handed over", code=program(store + f"    {draw}({hv}, bar)\n"), fails_at=3,
                 message_contains=f"handed `{hv}`"),
            dict(why="CP3 the variable's name in quotes", code=program(store + f"    {draw}(hero, \"bar\")\n"),
                 fails_at=3, message_contains="some text second"),
            dict(why="CP3 the finished helper edited (KEEP)", code=program(finished=helper.replace(
                "    show_on_panel(hero, bar)\n", "    print(hero[\"name\"], bar)\n")), fails_at=3,
                 message_contains="a finished helper changed"),
            dict(why="CP3 the helper called twice", code=program(store + pass_on + pass_on), fails_at=3,
                 message_contains="ran 2 times"),
            dict(why="CP3 one value too few", code=program(store + f"    {draw}(bar)\n"), fails_at=0,
                 message_contains="missing 1 required positional argument: 'bar'"),
            dict(why="CP3 one value too many", code=program(store + f"    {draw}(hero, bar, 5)\n"), fails_at=0,
                 message_contains="takes 2 positional arguments but 3 were given"),
            dict(why="CP3 stored, then a bar built by hand passed on instead of the variable (store-then-pass skipped)",
                 code=program(store + f"    {draw}(hero, \"{block}\" * hero[\"mana\"])\n"), fails_at=3,
                 message_contains="built right in the call"),
        ],
        notes=_qc_meta("func-takes-dict,return-value,store-then-pass,read-helper", form,
                       "box,eggs,greeting,get_greeting,show_on_ley_board") + "\n"
        f"QC-R2 C3, form {form}: one finished helper (`{draw}(hero, bar)` calls a hidden panel recorder), the "
        f"student's own `{build}(hero)` (starter `pass` under comment 1) and `{show}(hero)` to finish, the mana-bars "
        "shape. Deviations (the Unit 5 'honest fast path' ruling, then the teacher's Unit 7 review): C3 also carries "
        f"objective 1 (CP1: a function that takes a sheet and returns a value; no other code task made a student "
        "write `return <value>`, the class's biggest slip) and objective 6 (CP2, store-then-pass), so the code tasks "
        "alone cover every objective; three checkpoints [ND], each one action. CP1 RET + PAR-CONST: the check calls "
        f"`{build}` on two new sheets, Pell (mana 7) and Moss (mana 3), and wants `\"{block}\" * 7` and "
        f"`\"{block}\" * 3`: `None` back (named, plus 'it showed the bar first' when it printed), `{hv}` read, the "
        "same bar for both (a typed bar, one block), the wrong length, other text or a number. CP2 STO: the check "
        f"calls `{show}` on Pell (mana 7) and reads its variables as it returns: the function itself stored, the "
        f"outer `{hv}` read, a typed bar, the call passed straight on, a print, the bar built by hand. CP3 KEEP "
        f"(`{draw}` only, AST) then CALL: `{draw}` swapped for a pretend one that only writes down what it is handed, "
        "called on Brakka (mana 5): exactly once, with (hero, bar), and the bar handed over must be a variable made "
        "inside the function (a new call or a bar built right in the call fails). Fails on (spec): an edited helper "
        "-> KEEP; the arguments swapped -> CALL (the hidden panel takes either order, so the swap reaches the "
        "check). The wrong number of values is Python's own error at the bottom call. The pass lines say only what "
        "the console shows (blank until CP3, then the panel row). support='none', explainer='lean'.",
    )


# ---- C4: call a stored function from the book, then pay its cost from the hero (call-stored-func, func-takes-dict) ----

_CAST_PRE = r'''
_fn, _hv = __FN__, __HERO_VAR__
_f = _need(_fn, [__BOOK__, 'name', 'hero'], True)
_d = _defs().get(_fn)
_log = []


def _frost(*_a):
    _log.append(('Frost Veil', _a))


def _moon(*_a):
    _log.append(('Moon Step', _a))


def _other(*_a):
    _log.append(('another', _a))


def _fresh():
    _b = {_n: {'mana_cost': 9, 'effect': _other} for _n in __PAGES__}
    _b['Frost Veil'] = {'mana_cost': 5, 'effect': _frost}
    _b['Moon Step'] = {'mana_cost': 2, 'effect': _moon}
    return _b


def _stop_why(_e, _what):
    _k = _e.args[0] if type(_e).__name__ == 'KeyError' and _e.args else None
    if _k == 'name':
        return ('Inside `' + _fn + '`, the book was asked for the key `"name"`: a parameter name in quotes. '
                + _QUOTES + _ev(_what))
    if _k == 'mana_cost':
        return ("Inside `" + _fn + "`, `\"mana_cost\"` was read from the hero's sheet, which has only name and mana."
                + _ev(_what))
    if _k == 'mana':
        return "Inside `" + _fn + "`, `\"mana\"` was read from a page of the book, not from the hero's sheet." + _ev(_what)
    if 'not callable' in str(_e) and "'dict'" in str(_e):
        return 'Inside `' + _fn + '`, a whole page of the book was called with `()`, not its effect.' + _ev(_what)
    return 'Inside `' + _fn + '`, Python stopped with ' + _err(_e) + '.' + _ev(_what)
'''

_CAST_CALLS = _CAST_PRE + r'''
_book = _fresh()
_h = {'name': 'Pell', 'mana': 12}
_what = 'called `' + _fn + '` with another book, the name "Moon Step" and a sheet for Pell'
_val, _rows, _e = _call(_f, (_book, 'Moon Step', _h))
assert _e is None, _stop_why(_e, _what)
if not _log:
    _bare = [_s for _s in _ast.walk(_d) if type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Subscript']
    assert not _bare, 'The effect is read from the book, and nothing calls it.' + _ev(_what)
    _own = [_c.func.id for _c in _ast.walk(_d) if type(_c).__name__ == 'Call' and type(_c.func).__name__ == 'Name'
            and _c.func.id in __EFFECTS__]
    assert not _own, ('The function `' + (_own or [''])[0] + '` is called by its own name, not from the book.'
                      + _ev(_what, 'the book held other effects'))
    assert False, 'Nothing called the effect stored under "Moon Step".' + _ev(_what)
assert [_x for _x in _log if _x[0] == 'Moon Step'], ('The effect of another page ran, not the one under the name '
                                                    'handed in.' + _ev(_what))
assert len(_log) == 1, 'The effect ran ' + str(len(_log)) + ' times.' + _ev(_what)
_args = _log[0][1]
assert _args, 'The effect was called with nothing in its brackets.' + _ev(_what)
assert _args[0] is not _g.get(_hv), 'The effect was handed `' + _hv + '`, not the hero handed in.' + _ev(_what)
assert _args[0] is _h, 'The effect was handed ' + _show(_args[0]) + ', not the hero handed in.' + _ev(_what)
assert 'None' not in _rows, 'A `print(...)` around the call showed `None`.' + _ev(_what)
'''

_CAST_PAYS = _CAST_PRE + r'''
for _nm, _mana, _ward, _cost in (('Pell', 12, 'Moon Step', 2), ('Brakka', 9, 'Frost Veil', 5)):
    _book = _fresh()
    _h = {'name': _nm, 'mana': _mana}
    _what = 'called `' + _fn + '` with another book, "' + _ward + '" (cost ' + str(_cost) + ') and ' + _nm + ', mana ' + str(_mana)
    _loc, _val, _rows, _e = _capture(_f, (_book, _ward, _h))
    assert _e is None, _stop_why(_e, _what)
    _now = _h['mana']
    if _now == _mana - _cost:
        continue
    assert _book[_ward]['mana_cost'] == _cost or _now != _mana, (
        "The page's `\"mana_cost\"` changed, and the hero's mana did not: the wrong sheet was written." + _ev(_what))
    if _now == _mana:
        assert not (type(_val).__name__ == 'int' and _val == _mana - _cost), (
            '`' + _fn + '` returned the new mana, ' + str(_val) + ", and the hero's sheet did not change." + _ev(_what))
        assert not [_x for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id == _hv], (
            'The mana was taken from `' + _hv + '`, not from the hero handed in.' + _ev(_what))
        _kept = sorted(_k for _k, _x in _loc.items() if type(_x).__name__ == 'int' and _x == _mana - _cost)
        assert not _kept, ('The new mana, ' + str(_mana - _cost) + ', went into the variable `' + (_kept or [''])[0]
                           + "` inside `" + _fn + "`, and the hero's sheet did not change: it is still " + str(_mana)
                           + '.' + _ev(_what))
        assert False, "The hero's mana did not change: it is still " + str(_mana) + '.' + _ev(_what)
    assert not [_x for _x in _ast.walk(_d) if type(_x).__name__ == 'Name' and _x.id == _hv], (
        "The mana was read from `" + _hv + "`, the sheet outside, not from the hero handed in: " + _nm
        + "'s mana went from " + str(_mana) + ' to ' + str(_now) + '.' + _ev(_what))
    assert _now != _mana + _cost, "The hero's mana went up, from " + str(_mana) + ' to ' + str(_now) + '.' + _ev(_what)
    assert False, (_nm + "'s mana went from " + str(_mana) + ' to ' + str(_now) + ', and "' + _ward + '" costs '
                   + str(_cost) + '.' + _ev(_what))
'''


def _qc_cast(form, last_line):
    f = FORMS[form]
    cast, book, hv = f["cast"], f["book"], f["hero_var"]
    (n1, c1, fn1, l1), (n2, c2, fn2, l2) = f["first"], f["second"]
    head = (
        _effect_def(fn1, l1) + "\n\n" + _effect_def(fn2, l2) + "\n\n"
        f"{book} = {{\n"
        f"    \"{n1}\": {{\n        \"mana_cost\": {c1},\n        \"effect\": {fn1},\n    }},\n"
        f"    \"{n2}\": {{\n        \"mana_cost\": {c2},\n        \"effect\": {fn2},\n    }},\n"
        "}\n" + _hero_sheet(f) + "\n\n"
        f"def {cast}({book}, name, hero):\n"
        "    # 1. Call the effect stored in\n"
        f"    #    {book} under name, on hero.\n"
        "    # 2. Take its mana_cost from\n"
        "    #    hero[\"mana\"].\n"
    )
    tail = f"\n\n{cast}({book}, \"{n2}\", {hv})\nprint({hv}[\"mana\"])\n"
    call = f"    {book}[name][\"effect\"](hero)\n"
    pay = f"    hero[\"mana\"] = hero[\"mana\"] - {book}[name][\"mana_cost\"]\n"

    def program(body=call + pay):
        return head + body + tail

    starter = program("    pass\n")
    solution = program()
    vals = dict(fn=cast, hero_var=hv, book=book, effects=[fn1, fn2], pages=[n1, n2])
    return dict(
        id=f"cast-from-the-{book}",
        title=f"Cast from the {f['page']} book",
        martu=(
            f"Each page of `{book}` holds a cost and an effect: a function, stored with no `()`. Finish `{cast}`: "
            "cast the effect from the book, on the hero, then make the hero pay. Mar'tu's check hands it another "
            "book and another hero.\n" + _stuck(LESSON_6C, "A recipe in a box", "Cast from the book")
        ),
        names=[cast, book, "name", "hero"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="call-the-effect",
                text=f"Inside `{cast}`, call the effect stored in `{book}` under `name`, on `hero`.",
                dictated=False,
                hints=[
                    "Look at comment 1. Read the page by its name, then its `\"effect\"`, then call it.",
                    "`jars[\"Plum\"][\"lid\"]` reads one value inside one page. A function read that way runs only "
                    "when brackets with a value follow it.",
                    f"Start with `{book}[name][\"effect\"](`, and hand it the hero.",
                ],
                checks=[check("the effect under name runs once, on the hero handed in", _CAST_CALLS, **vals)],
                pass_line=f"Lucky: {f['hero']} {l2[:-1]}. From the book. Fine.",
            ),
            dict(
                id="pay-the-cost",
                text="Then take that page's `\"mana_cost\"` from `hero[\"mana\"]`.",
                dictated=False,
                hints=[
                    "Look at comment 2. The cost is on the page in the book; the mana is on the hero's sheet.",
                    "`tank[\"fuel\"] = tank[\"fuel\"] - 3` changes the sheet that was handed in. The caller sees it, with "
                    "no `return`.",
                    "Start with `hero[\"mana\"] =`, then the hero's mana minus the page's cost.",
                ],
                checks=[check("the hero handed in pays the page's own cost", _CAST_PAYS, **vals)],
                pass_line=last_line,
            ),
        ],
        solution=solution,
        partials=[program(call)],
        assemble=dict(
            lines=[ln for ln in solution.splitlines() if ln.strip() and not ln.lstrip().startswith("#")],
            distractors=[f"    {book}[name][\"effect\"]", f"    {book}[\"name\"][\"effect\"](hero)",
                         f"    hero[\"mana\"] - {book}[name][\"mana_cost\"]"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `{book}[name]` is the page. `[\"effect\"]` is the function on it.\n"
                "2. `(hero)` on the end calls it, on this hero.\n"
                "3. Then the hero's mana, minus the page's `\"mana_cost\"`, back into `hero[\"mana\"]`.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "`spell[\"spell_function\"](caster)` cast the spell, then `caster[\"mana\"] = caster[\"mana\"] - "
                "spell[\"mana_cost\"]` paid for it. The parentheses on the end are what call it.")),
        ],
        campaign_link=dict(
            module=MODULE,
            part="hold-the-barrier",
            snippet='spell["spell_function"](caster)\ncaster["mana"] = caster["mana"] - spell["mana_cost"]',
            why="These were the last lines of `cast_spell`: cast from the dictionary, then pay from the caster's sheet.",
        ),
        takeaway=f"`{book}[name][\"effect\"](hero)` calls the stored function; the hero's own sheet pays the cost.",
        wrong_answers=[
            dict(why="the starter (pass)", code=starter, fails_at=1, message_contains="Nothing called the effect"),
            dict(why="CP1 (hero) missing: the effect is read, never called (the spec's CALL)",
                 code=program(f"    {book}[name][\"effect\"]\n"), fails_at=1, message_contains="nothing calls it"),
            dict(why="CP1 the function called by its own name (a typed spell)", code=program(f"    {fn2}(hero)\n"),
                 fails_at=1, message_contains=f"`{fn2}` is called by its own name"),
            dict(why="CP1 the parameter in quotes", code=program(f"    {book}[\"name\"][\"effect\"](hero)\n"),
                 fails_at=0, message_contains="KeyError: 'name'"),
            dict(why="CP1 the page called, not its effect", code=program(f"    {book}[name](hero)\n"), fails_at=0,
                 message_contains="'dict' object is not callable"),
            dict(why="CP1 the outer sheet handed to the effect (the wrong sheet)",
                 code=program(f"    {book}[name][\"effect\"]({hv})\n"), fails_at=1, message_contains=f"handed `{hv}`"),
            dict(why="CP1 the typed page name", code=program(f"    {book}[\"{n2}\"][\"effect\"](hero)\n"), fails_at=1,
                 message_contains="another page ran"),
            dict(why="CP1 print around the call (an extra None)", code=program(f"    print({book}[name][\"effect\"](hero))\n"),
                 fails_at=1, message_contains="showed `None`"),
            dict(why="CP1 () with nothing inside", code=program(f"    {book}[name][\"effect\"]()\n"), fails_at=0,
                 message_contains="missing 1 required positional argument: 'hero'"),
            dict(why="CP2 the subtraction never stored (the sheet doesn't change)",
                 code=program(call + f"    hero[\"mana\"] - {book}[name][\"mana_cost\"]\n"), fails_at=2,
                 message_contains="did not change"),
            dict(why="CP2 returned instead of changed (thinking the caller won't see the change)",
                 code=program(call + f"    return hero[\"mana\"] - {book}[name][\"mana_cost\"]\n"), fails_at=2,
                 message_contains="returned the new mana"),
            dict(why="CP2 the cost typed (A-06/A-07 typed test values)",
                 code=program(call + f"    hero[\"mana\"] = hero[\"mana\"] - {c2}\n"), fails_at=2,
                 message_contains=f"costs 2"),
            dict(why="CP2 the cost read from the hero's sheet (a key from the wrong sheet)",
                 code=program(call + "    hero[\"mana\"] = hero[\"mana\"] - hero[\"mana_cost\"]\n"), fails_at=0,
                 message_contains="KeyError: 'mana_cost'"),
            dict(why="CP2 the page's cost changed, not the hero's mana (the wrong sheet written)",
                 code=program(call + f"    {book}[name][\"mana_cost\"] = hero[\"mana\"] - {book}[name][\"mana_cost\"]\n"),
                 fails_at=2, message_contains="the wrong sheet was written"),
            dict(why="CP2 the sign the other way", code=program(call + f"    hero[\"mana\"] = hero[\"mana\"] + {book}[name][\"mana_cost\"]\n"),
                 fails_at=2, message_contains="went up"),
            dict(why="CP2 the outer hero's mana read, the right hero written (the wrong sheet)",
                 code=program(call + f"    hero[\"mana\"] = {hv}[\"mana\"] - {book}[name][\"mana_cost\"]\n"),
                 fails_at=2, message_contains="the sheet outside"),
            dict(why="CP2 the outer hero pays (the wrong sheet)",
                 code=program(call + f"    {hv}[\"mana\"] = {hv}[\"mana\"] - {book}[name][\"mana_cost\"]\n"),
                 fails_at=2, message_contains=f"taken from `{hv}`"),
            dict(why="CP2 the new mana kept in a variable inside the function (the sheet never changes)",
                 code=program(call + f"    mana = hero[\"mana\"] - {book}[name][\"mana_cost\"]\n"), fails_at=2,
                 message_contains="went into the variable `mana`"),
            dict(why="CP2 the mana read from the page, not the hero (a key from the wrong sheet)",
                 code=program(call + f"    hero[\"mana\"] = {book}[name][\"mana\"] - {book}[name][\"mana_cost\"]\n"),
                 fails_at=0, message_contains="KeyError: 'mana'"),
            dict(why="CP1 the call's result stored where the function was wanted, then called (NoneType)",
                 code=program(f"    effect = {book}[name][\"effect\"](hero)\n    effect(hero)\n"), fails_at=0,
                 message_contains="'NoneType' object is not callable"),
        ],
        notes=_qc_meta("call-stored-func,func-takes-dict", form, "jars,tank,fuel") + "\n"
        f"QC-R2 C4, form {form}: `{book}` holds {n1} ({c1}, `{fn1}`) and {n2} ({c2}, `{fn2}`); `{cast}({book}, name, "
        "hero)` to finish. Deviation (the 'honest fast path' ruling): a second checkpoint pays the cost, so objective 2 "
        "(a dict passed in changes, and the caller sees it) is gated in code too, not only in Q3. CP1 [ND] CALL: the "
        "check hands `" + cast + "` a fresh book whose effects are recorders (Frost Veil 5, Moon Step 2) and Pell: "
        "exactly one call, of the page under the name handed in, with that hero. Fails on (spec): `(hero)` missing "
        "-> CALL ('nothing calls it'). Also: the effect called by its own name, the page called, the quoted "
        f"parameter, `{hv}` handed over, the typed page name, a print around it. CP2 [ND]: two fresh casts (Pell 12 "
        "- 2, Brakka 9 - 5): the subtraction never stored, `return` instead of the change, a typed cost, the cost "
        "read from the hero's sheet (KeyError), the new mana kept in a local variable (read from the frame and "
        "named), the page's cost written instead (the wrong sheet), the sign, the "
        f"outer `{hv}` paying. support='none', explainer='lean'.",
    )


_QC_SUMMARY = (
    "Optional. Four short tasks and four questions, no hints. Pass all four tasks and get 3 of the 4 questions "
    "right to test out of Unit 7. A task you miss just shows Mar'tu where to start. Tasks you pass here stay ticked."
)
# For students who test out and miss 6P (The Resonance Array): two sentences of the story, on the last pass line.
_STORY_RECAP = ("Mar'tu's notes: the resonance array got its dials, one recipe each, and its readings say it plainly. "
                "The decay is accelerating.")
_STRETCH = ("Want more? The articles lambda, map() and Two Things Back, Lucky's side quest in The Resonance Array, or "
            "the extra practice on defaults and scope.")

QC_R2_A = dict(
    kind="testout",
    id="qc-r2-a",
    title="Quick Check Recipes II · Form A",
    optional=True,
    minutes=16,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_learn("A"),
        _qc_guard("A"),
        _qc_helper("A"),
        _qc_cast("A", "Mar'tu: A ward learned and handed over, a guard at the door, a bar built and passed on, and a "
                      "ward cast from the book. That is Unit 7, yes? " + _STORY_RECAP + " " + _STRETCH),
    ],
    notes=(
        "Quick Check Recipes II, form A (code tasks C1-C4, in the spec's order). Questions live in "
        "qc-r2-a-questions. Pass = every code task plus 3 of the 4 questions (questions_to_pass=3, as Unit 2's "
        "QC2); a retake draws form B. The code tasks cover every objective on their own (the Unit 5 'honest fast "
        "path' ruling, tightened by the teacher's Unit 7 review): objective 1 (a function that takes a sheet and "
        "returns a value) is gated in C3 CP1, where the student writes `return <value>` (the class's biggest slip, "
        "print for return); objective 2 in C4 CP2 (and Q3); objective 3 in C1 CP1-CP2; objective 4 in C2; "
        "objectives 5 and 6 in C3 CP3 and CP2; objective 7 in C4 CP1, and func-as-value (handing a function over "
        "with no `()`, the unit's main idea) in C1 CP3 and Q1, so a student who misses Q1 still has to show it in "
        "code. Check messages are lean (the Unit 2 ruling): the slip and the evidence, never the fix. Framing (G4 "
        "R25): it only shows Mar'tu where to start; each task's Stuck? line names the exercises that teach that one "
        "skill, never a whole lesson. Coverage (lint d): dict-from-params -> C1 CP1 (WA typed values, the quoted "
        "parameter, `\"cost\"`, capitals, `\"spell_function\"`, unquoted keys, swapped values); store-by-name -> C1 "
        "CP2 (WA `wards[\"ward_name\"]`, a typed name, `wards = {...}`, `return ward`); func-as-value -> C1 CP3 (WA "
        "`ash_ward()`, `\"ash_ward\"`, the 0 left, `ash_ward({...})`, another function) and Q1; early-return -> C2 "
        "(WA no return, the guard after the work, if/else, a typed name, `in` for `not in`); func-takes-dict and "
        "return-value -> C3 CP1 (WA `pass`, print for return, a typed bar, `oogrish` read, one block); "
        "store-then-pass -> C3 CP2 (WA `bar = build_bar`, the outer sheet, a typed bar, passed straight on); "
        "read-helper -> C3 CP3 (WA an edited helper, the values swapped, too few or too many); call-stored-func -> "
        "C4 CP1 (WA `(hero)` missing, called by its own name, the page called); func-takes-dict (a change the caller "
        "sees) -> C4 CP2 (WA not stored, returned instead, the page's cost written) and Q3; none-return -> C3 CP1, "
        "Q2 and C1 CP2 (`return ward`); exact keys -> Q4. The last task's pass line recaps the form, adds two "
        "sentences of the story for students who test out and miss 6P (the resonance array's dials and readings; "
        "the decay is accelerating), and offers the stretch: the three articles, Lucky's side quest in 6P and the "
        "7X extra practice. support='none' and explainer='lean' everywhere: no hints, tracer or compare; glossary "
        "and read-aloud stay on. 16 minutes (the spec's 12; 14 with C1 CP2 and C4 CP2; plus a minute each for C1 "
        "CP3 and C3 CP1). The summary still says four short tasks: there are four, with more checkpoints."
    ),
)

QC_R2_B = dict(
    kind="testout",
    id="qc-r2-b",
    title="Quick Check Recipes II · Form B",
    optional=True,
    minutes=16,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_learn("B"),
        _qc_guard("B"),
        _qc_helper("B"),
        _qc_cast("B", "Mar'tu: A charm learned and handed over, a guard at the door, a gauge built and passed on, "
                      "and a charm cast from the book. That is Unit 7, yes? " + _STORY_RECAP + " " + _STRETCH),
    ],
    notes=(
        "Quick Check Recipes II, form B: Bomb Shell's charms (`learn_charm`, `use_charm`, `cast_charm`), Teal Shield "
        "(5, `teal_shield` handed over in C1 CP3) and Spark Net (3), Ember Wall unknown, and a `▮` gauge with the "
        "finished `draw_gauge`, the student's own `build_gauge` (C3 CP1, objective 1 gated in code) and "
        "`show_gauge`. Same coverage, order and rules as form A: objective 1 in C3 CP1, func-as-value in C1 CP3 and "
        "Q1. Questions live in qc-r2-b-questions; questions_to_pass=3. 16 minutes."
    ),
)


# =============================================================================================
# Quick Check Recipes II · question forms (scored with their form: 3 of the 4 right, questions_to_pass=3)
# =============================================================================================

def _qc_questions(form, hand, none_back, same_sheet, keys):
    """hand = (fn, line, wrong_call, order, answer index); the others = (code, answer, choices, explain, notes)."""
    fn, line, wrong_call, order, right = hand
    choice_text = {
        "bare": f"cast_on_all(roster, {fn})",
        "empty": f"cast_on_all(roster, {fn}())",
        "called": f"cast_on_all(roster, {fn}({wrong_call}))",
        "quoted": f'cast_on_all(roster, "{fn}")',
    }
    why = {
        "empty": f"With `()`, `{fn}` runs right now, before `cast_on_all` starts, with no hero. Python stops: "
                 "*missing 1 required positional argument*.",
        "called": f"`{fn}({wrong_call})` runs now, for one hero only, and hands over what it returns: `None`. Then "
                  "`cast_on_all` calls `None`, and Python stops: *'NoneType' object is not callable*.",
        "quoted": "In quotes it is just text, and text can't be called: *'str' object is not callable*.",
    }
    choices = [choice_text[k] for k in order]
    assert order[right] == "bare"

    def predict(qid, parts):
        code, answer, opts, explain, notes = parts
        return dict(type="predict", id=qid, q="What will this print?", code=code, answer=answer, choices=opts,
                    explain=explain, notes=notes)

    return dict(
        kind="quiz",
        id=f"qc-r2-{form.lower()}-questions",
        title=f"Quick Check Recipes II · Form {form} questions",
        optional=True,
        minutes=4,
        summary="Four questions that go with Quick Check Recipes II. To pass the Quick Check, get 3 of the 4 right.",
        questions=[
            dict(
                type="mc",
                id="hand-it-over",
                q=f"`cast_on_all` calls `effect(hero)` for each hero. Which line hands `{fn}` over, so it runs once for "
                  "every hero?",
                code=(
                    f"def {fn}(hero):\n"
                    f'    print(hero["name"], "{line}")\n'
                    "\n\n"
                    "def cast_on_all(heroes, effect):\n"
                    "    for hero in heroes:\n"
                    "        effect(hero)\n"
                ),
                choices=choices,
                answer=right,
                why_wrong={i: why[k] for i, k in enumerate(order) if k != "bare"},
                explain=(
                    f"The name with no `()` is the function itself. `cast_on_all` calls it later, once for each hero, "
                    "with `effect(hero)`."
                ),
                notes=("Q1, func-as-value (Obj 7). Fails on (spec): the name with `()`. Distractors from the class's "
                       "slips: `()` (missing argument), one call's result (the NoneType error), the name in quotes."),
            ),
            predict("missing-return", none_back),
            predict("the-caller-sees-it", same_sheet),
            predict("keys-match", keys),
        ],
        notes=(
            f"Quick Check Recipes II, form {form} questions, scored with qc-r2-{form.lower()}: every code task plus 3 "
            "of the 4 questions (questions_to_pass=3 on the form, as Unit 2's QC2). The best score counts, so a retake "
            "can lift it. The spec's Q1-Q3, plus Q4 (keys must match exactly, the campaign's `\"mana_cost\"`), so "
            "three of four mirrors QC2. No hints; read-aloud and glossary stay on. Right answers sit at varied "
            "positions (the site also shuffles)."
        ),
    )


QC_R2_A_QUESTIONS = _qc_questions(
    "A",
    ("shine", "shines.", "lucky", ["empty", "bare", "called", "quoted"], 1),
    (
        'def ward_cost(ward):\n    print(ward["mana_cost"] * 2)\n\n\nash = {"mana_cost": 4}\ntotal = ward_cost(ash)\n'
        "print(total)\n",
        "8\nNone",
        ["8\n8", "8\nNone", "None", "8"],
        (
            "Inside, `print` shows 8. But the function has no `return`, so the call hands back `None`, and `total` "
            "holds `None`. To keep the 8, the function needs `return`."
        ),
        "Q2, none-return: print inside the function instead of return. Fails on (spec): a value instead of `None` "
        "(8 twice). Distractors: no print at all, one line only.",
    ),
    (
        'def drain(hero, amount):\n    left = hero["mana"] - amount\n    hero["mana"] = left\n\n\noogrish = {"mana": 18}\n'
        'result = drain(oogrish, 5)\nprint(oogrish["mana"], result)\n',
        "13 None",
        ["18 None", "13 None", "13 13", "18 13"],
        (
            "`hero` and `oogrish` are two labels on the same sheet, so the change reaches the caller: 18 - 5 = 13. The "
            "function has no `return`, so `result` holds `None`. Changing a sheet needs no `return`."
        ),
        "Q3, func-takes-dict (Obj 2). Fails on (spec): 'the caller's sheet is unchanged' (18). Also: 'a change needs "
        "a return' (13 13). Oogrish's real max mana, 18.",
    ),
    (
        'def make_ward(cost):\n    return {"cost": cost}\n\n\nward = make_ward(4)\nprint(ward["mana_cost"])\n',
        "ERROR: KeyError: 'mana_cost'",
        ["4", "cost", "None", "ERROR: KeyError: 'mana_cost'"],
        (
            "The function built the key `\"cost\"`, and the last line asks for `\"mana_cost\"`. Python matches keys "
            "letter for letter, so it stops with a KeyError. The campaign reads `\"mana_cost\"`, so that is the key "
            "to build."
        ),
        "Q4, dict-from-params: keys that don't exactly match the names the reader uses. Distractors: the value as "
        "if the names were close enough (4), the key's name, None.",
    ),
)

QC_R2_B_QUESTIONS = _qc_questions(
    "B",
    ("hum", "hums.", "bomb_shell", ["called", "quoted", "bare", "empty"], 2),
    (
        'def charm_cost(charm):\n    print(charm["mana_cost"] * 3)\n\n\nspark = {"mana_cost": 5}\n'
        "total = charm_cost(spark)\nprint(total)\n",
        "15\nNone",
        ["15\nNone", "15\n15", "15", "None"],
        (
            "Inside, `print` shows 15. But the function has no `return`, so the call hands back `None`, and `total` "
            "holds `None`. To keep the 15, the function needs `return`."
        ),
        "Form B of missing-return.",
    ),
    (
        'def drain(hero, amount):\n    left = hero["mana"] - amount\n    hero["mana"] = left\n\n\nbomb_shell = {"mana": 24}\n'
        'result = drain(bomb_shell, 6)\nprint(bomb_shell["mana"], result)\n',
        "18 None",
        ["18 18", "24 None", "24 18", "18 None"],
        (
            "`hero` and `bomb_shell` are two labels on the same sheet, so the change reaches the caller: 24 - 6 = 18. "
            "The function has no `return`, so `result` holds `None`. Changing a sheet needs no `return`."
        ),
        "Form B of the-caller-sees-it (Bomb Shell's real max mana, 24).",
    ),
    (
        'def make_charm(need):\n    return {"affinity": need}\n\n\ncharm = make_charm(7)\n'
        'print(charm["required_affinity"])\n',
        "ERROR: KeyError: 'required_affinity'",
        ["ERROR: KeyError: 'required_affinity'", "7", "affinity", "None"],
        (
            "The function built the key `\"affinity\"`, and the last line asks for `\"required_affinity\"`. Close is "
            "not enough: Python matches keys letter for letter, so it stops with a KeyError."
        ),
        "Form B of keys-match.",
    ),
)


# =============================================================================================
# Cheatsheet "Mar'tu's Chalk Notes: Spell Recipes"
# =============================================================================================

HUSH_DEF = 'def hush(hero):\n    print(hero["name"], "hushes.")\n'

CHALK_NOTES_7 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Spell Recipes",
    summary="Everything from Unit 7 on one page. Printable.",
    entries=[
        dict(concept="A function that takes a sheet",
             code='def mana_used(hero):\n    full = hero["max_mana"]\n    return full - hero["mana"]\n\n\n'
                  'gearshift = {\n    "mana": 14,\n    "max_mana": 20,\n}\n'
                  'oogrish = {\n    "mana": 10,\n    "max_mana": 18,\n}\n'
                  'print(mana_used(gearshift))\nprint(mana_used(oogrish))\n',
             output="6\n8",
             note="The parameter `hero` is the sheet handed in. Read it by key, and return the answer. One function, "
                  "any sheet. You've seen this: `get_mana_bar(caster)`. (Lesson: Recipes That Read Stat Sheets)"),
        dict(concept="Changes to a sheet reach the caller",
             code='def charge(hero, amount):\n    now = hero["mana"] + amount\n    hero["mana"] = now\n\n\n'
                  'gearshift = {"mana": 14}\ncharge(gearshift, 4)\nprint(gearshift["mana"])\n',
             output="18",
             note="`hero` and `gearshift` are two labels on the same sheet, so the caller sees the change. No "
                  "`return` is needed for that."),
        dict(concept="When does a function need `return`?",
             code="def doubled(n):\n    return n * 2\n\n\nprint(doubled(9))\n",
             output="18",
             note="When the caller needs a value back, like `mana_used`. A function that only changes a sheet in "
                  "place, like `charge`, doesn't. With no `return`, a call hands back `None`."),
        dict(concept="The matching parameter, exactly",
             code='def make_rune(mana_cost, color):\n    rune = {\n        "mana_cost": mana_cost,\n'
                  '        "color": color,\n    }\n    return rune\n\n\nprint(make_rune(3, "violet"))\n',
             output="{'mana_cost': 3, 'color': 'violet'}",
             note="The key `\"mana_cost\"` gets the parameter `mana_cost`, letter for letter, with no quotes. "
                  "`\"mana_cost\": \"mana_cost\"` would store the text. You've seen this: `add_spell`."),
        dict(concept="Store by name: `book[name] = spell`",
             code="def add_rune(book, rune_name, rune):\n    book[rune_name] = rune\n\n\nrunes = {}\n"
                  'add_rune(runes, "Hush", 1)\nprint(runes)\n',
             output="{'Hush': 1}",
             note="The key comes from the parameter, with no quotes. `book[\"rune_name\"]` would make a page called "
                  "rune_name, and `book = {...}` inside would make a new book the caller never sees."),
        dict(concept="The early-`return` guard",
             code='def read_rune(book, rune_name):\n    if rune_name not in book:\n        print("No rune:", rune_name)\n'
                  '        return\n    print("Reading", rune_name)\n\n\nrunes = {"Hush": 1}\nread_rune(runes, "Blaze")\n'
                  'read_rune(runes, "Hush")\n',
             output="No rune: Blaze\nReading Hush",
             note="The guard goes first. `return` ends the call, so the lines below run only when the guard lets it "
                  "through. You've seen this: the opening of `cast_spell`."),
        dict(concept="Leave finished helpers alone",
             code='def pin_up(hero, badge):\n    # Finished. Leave it as it is.\n    print(hero["name"], badge)\n\n\n'
                  'gearshift = {"name": "Gearshift"}\npin_up(gearshift, "***")\n',
             output="Gearshift ***",
             note="Read its `def` line: what it takes, and in what order. Then call it that way, and change nothing "
                  "inside it. You've seen this: `print_mana(caster, mana_bar)`."),
        dict(concept="Store, then pass",
             code='def pin_up(hero, badge):\n    print(hero["name"], badge)\n\n\ndef get_badge(hero):\n'
                  '    return "*" * hero["rank"]\n\n\ndef show_badge(hero):\n    badge = get_badge(hero)\n'
                  '    pin_up(hero, badge)\n\n\ngearshift = {\n    "name": "Gearshift",\n    "rank": 3,\n}\n'
                  "show_badge(gearshift)\n",
             output="Gearshift ***",
             note="Store what one function returns in a variable, then pass that variable to the next. You've seen "
                  "this: `show_mana(caster)`."),
        dict(concept="`hush` (the function) versus `hush()` (its result)",
             code=HUSH_DEF + '\n\nchosen = hush\nchosen({"name": "Gearshift"})\n',
             output="Gearshift hushes.",
             note="With no `()`, the name is the function itself: store it, or hand it over, and it runs later. "
                  "`hush(...)` runs it now and hands back `None`. You've seen this: `strengthen_magic` with no `()`."),
        dict(concept="Call it from the book: `book[name][\"effect\"](hero)`",
             code=HUSH_DEF + '\n\nrunes = {\n    "Hush": {"effect": hush},\n}\ngearshift = {"name": "Gearshift"}\n'
                  'runes["Hush"]["effect"](gearshift)\n',
             output="Gearshift hushes.",
             note="Read the page, then its `\"effect\"`, then call it: the brackets on the end are what call it. "
                  "Without them, nothing happens. You've seen this: `spell[\"spell_function\"](caster)`."),
        dict(concept="(extra) Defaults and keyword arguments",
             code='def stamp(mark="*", count=3):\n    print(mark * count)\n\n\nstamp()\nstamp(count=5)\n'
                  'stamp(mark="#")\n',
             output="***\n*****\n###",
             note="A default is used when the call hands over nothing. A keyword argument names the value, so the "
                  "order doesn't matter. (Extra practice: Defaults and Scope)"),
        dict(concept="(extra) Inside stays inside",
             code="def fill_lamp(oil):\n    flame = oil * 3\n    return flame\n\n\nlight = fill_lamp(2)\nprint(light)\n",
             output="6",
             note="`flame` lives only inside `fill_lamp`. `print(flame)` outside stops with a NameError. Return it, "
                  "and catch it outside."),
        dict(concept="(extra) A lambda",
             code="triple = lambda n: n * 3\nprint(triple(7))\n",
             output="21",
             note="A one-line function: the parameter, a colon, then what it returns. No `def`, no `return`. "
                  "(Article: lambda)"),
        dict(concept="(extra) map()",
             code="triple = lambda n: n * 3\nprint(list(map(triple, [1, 4, 5])))\n",
             output="[3, 12, 15]",
             note="Calls the function on every item and collects what it returns. The function goes first, with no "
                  "`()`. (Article: map())"),
        dict(concept="(extra) Two things back",
             code="def split_coins(coins, heroes):\n    each = coins // heroes\n    left = coins % heroes\n"
                  "    return each, left\n\n\neach, left = split_coins(23, 4)\nprint(each, left)\n",
             output="5 3",
             note="A comma between two values returns a tuple. Two names, in order, unpack it. (Article: Two Things "
                  "Back)"),
        dict(concept="Error: the call stored, then called",
             code=HUSH_DEF + '\n\nchosen = hush({"name": "Oogrish"})\nchosen({"name": "Oogrish"})\n',
             note="TypeError: 'NoneType' object is not callable. `hush(...)` ran at once and stored `None`. Store the "
                  "function itself: `chosen = hush`."),
        dict(concept="Error: no `return`, then glued",
             code='def label(n):\n    text = "Rank " + str(n)\n\n\nprint("Badge: " + label(2))\n',
             note="TypeError: can only concatenate str (not \"NoneType\") to str. `label` has no `return`, so the call "
                  "hands back `None`."),
        dict(concept="Error: handed over with `()`",
             code=HUSH_DEF + "\n\nprint(list(map(hush(), [])))\n",
             note="TypeError: hush() missing 1 required positional argument: 'hero'. With `()`, it ran right away, "
                  "with no hero. Hand it over with no `()`."),
        dict(concept="Error: a parameter in quotes",
             code='def get_rune(book, rune_name):\n    return book["rune_name"]\n\n\nprint(get_rune({"Hush": 1}, "Hush"))\n',
             note="KeyError: 'rune_name'. In quotes, it is just the letters rune_name. Take the quotes off to use the "
                  "parameter."),
        dict(concept="Error: a key that doesn't match",
             code='rune = {"cost": 3}\nprint(rune["mana_cost"])\n',
             note="KeyError: 'mana_cost'. Keys match letter for letter. Build the key the reader asks for."),
        dict(concept="Error: a page called, not its effect",
             code=HUSH_DEF + '\n\nrunes = {"Hush": {"effect": hush}}\nrunes["Hush"]({"name": "Oogrish"})\n',
             note="TypeError: 'dict' object is not callable. `runes[\"Hush\"]` is the whole page. Read its "
                  "`[\"effect\"]` first, then call that."),
    ],
    notes=(
        "Cheatsheet 7 (the spec's list in order, the four extras from this part, then the errors this unit catches). "
        "Entries with `output` are run and checked by the harness; the errors have none. As Unit 3's ruling asks, no "
        "entry shares a name or number with the Quick Check (runes, badges and `hush`, not wards, charms, "
        "`learn_ward`, `draw_row` or `cast_ward`) or with the lessons' tasks, so the page never hands over an answer."
    ),
)


ITEMS = [EXTRA_7X, LAMBDA_ARTICLE, MAP_ARTICLE, TWO_BACK_ARTICLE, QC_R2_A, QC_R2_A_QUESTIONS, QC_R2_B,
         QC_R2_B_QUESTIONS, CHALK_NOTES_7]
