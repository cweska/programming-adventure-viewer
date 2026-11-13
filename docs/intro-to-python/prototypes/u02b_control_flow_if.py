"""Unit 2 "Control Flow", part b: Lesson 2B "If the Clock Turns Red" (with 2b-remembers), Article 2-A1
"Match: Another Way to Choose", Quiz 2 and Project 2P1 "Road Encounter Table".

Spec: design/curriculum.md, "## Unit 2 · Control Flow", items 2 to 5 (u02b): 2b-remembers; 2B-01 to 2B-09 and
2B-S; Article 2-A1 (with its five-option try-it); Quiz 2 (2 mc, 4 predict, 1 parsons, 1 bug); Project 2P1 (with
Lucky's side quest). Introduces node:If (2B-01), op:And, op:Or, op:Not (2B-06), node:Import, import:random,
attr:randint (2B-07) and node:Match (2-A1, optional only: no core code uses `match`).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN this code: the
four `if`/`elif` dialogue options on `"option 1"`, the trap-door skill checks with `random.randint` and
`return roll >= required_roll`, and `cast_spell`'s `<`, not `<=`. So every campaign link here is "you've seen
this, now you'll get it". Every student has their own device; pair talk is optional, every checkpoint is solo.

Help ladder (curriculum 2.2) as fields, the same as Unit 1: hints[0] Start me off, hints[1] Point (where to look),
another_way, hints[2+] Teach (a tiny example with other names), assemble (More structure), solution (Show).

Check codes (curriculum 2.5) built by the helpers below. The harness has no _rerun() helper yet, so every rerun
is done inside the check itself: the student's code is parsed, each named top-level `name = value` line gets the
new value, `random.randint` is swapped for a scripted die that records its arguments (and puts the real one back
afterwards, because the browser reuses one interpreter), any hidden setup (the CALL recorders) runs again, and the
program runs in a fresh namespace with its prints kept private. Nothing a check does changes the student's code.
  lines_check()  CMB on printed lines: after a rerun, some lines must print and some must not
  box_check()    CMB on a box: after a rerun, the box must hold the expected value (TEXT-vs-bool too)
  bnd_check()    BND: rolls of needed - 1, needed, needed + 1, a low and a high roll, then another `needed`, read
                 from the student's own code, so any difficulty passes. Lines are compared with every whole
                 number masked, so "Rolled 14: success" counts as the same line for 14 and 18.
                 The line printed for a high roll is the success line; the one for a low roll is the failure line.
                 Exactly one of them prints per roll, so a failure line with no indent (no `else:`) fails.
  rnd_check()    RND: the box holds the value of a scripted `random.randint` call, and that call had (1, faces);
                 a box still holding the starter's placeholder number is named as such
  dialogue_check() / options_lit_check()  CALL: mar_tu_says / light_up_option recorders (each record keeps the
                 caller's line number, so a check knows WHICH branch spoke), four reruns plus "option 5"
  from_boxes_check()  a box made with two `=` signs (`can_cast = mana = cost ...`), from typed values (`True`,
                 `12 >= 9 and 9 >= 9`), or still holding the starter's placeholder (`False`) gets its own message
                 before the CMB check
  dead_branch_check()  an if/elif chain on `box <= n` whose later test can never run (the old chain kept and
                 patched by a second `if`)
  one_chain_check()  the box is set by one `if` chain, not by several separate `if`s
  name_check()   NAME / LEFT / BARE, as in Unit 1
  strexact_check() STREXACT: a quoted literal that differs from the wanted text only by capitals or spaces
  blanks_check() the starter's "___" left inside quotes
Messages use invented values only (Tester, a grumpy moth) and never repeat a student's own text (2.11): BND says
"the success line" and "the failure line", never the words the student wrote.
Teacher ruling on the Unit 2 reviews (cross-cutting): every rerun message starts with the fix, then says what
happened, and ends with the evidence in brackets, "(Mar'tu's check tried X, only inside the check.)", in about 35
words or fewer. One order rule everywhere: "first, the test that lets the fewest numbers through". A box that
still holds the starter's placeholder is named as such ("still holds the starter's `0`"), and a missing starter
box gets "Keep the box X from the starter". Rung 0 (hints[0]) gives only the line's left side or first tokens and
stops before the sign or the and/or; in debug steps it is "Read Python's last line"; bonus rung 0 is a few tokens.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u02b
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates, filled in per exercise)
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# The rerun: the student's code again, with some `name = value` lines changed and a scripted die. `_rolls` is a
# list: each randint call takes the next roll, and the last one repeats (so a reroll gets the same number).
_RERUN = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import random as _random
_SETUP = __SETUP__
def _show(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
def _whole(_v):
    # a whole number in a line: `Rolled 7.` and `(7h)` count; `17`, `0.7` and `7.5` do not
    return r'(?<![\w.])' + _re.escape(str(_v)) + r'(?!\w)(?!\.\d)'
def _with(_vals):
    _parts = ['`' + _k + ' = ' + _show(_v) + '`' for _k, _v in _vals.items()]
    return _parts[0] if len(_parts) == 1 else ', '.join(_parts[:-1]) + ' and ' + _parts[-1]
def _a_roll(_r):
    return ('an ' if str(_r)[:1] == '8' or _r in (11, 18) else 'a ') + str(_r)
def _did(_vals, _rolls, _end=''):
    # The evidence, always in brackets at the END of a message: what the rerun changed.
    _bits = []
    if _vals:
        _bits.append('tried ' + _with(_vals))
    if _rolls:
        _bits.append('rolled ' + ', then '.join(_a_roll(_r) for _r in _rolls) + ' for you')
    return "(Mar'tu's check " + ' and '.join(_bits or ['ran your code again']) + ', only inside the check' + _end + '.)'
def _mend(_first, _what, _vals, _rolls):
    # A rerun message: the fix first, then what happened, then the evidence in brackets.
    return _first + ' ' + (_what + ' ' if _what else '') + _did(_vals, _rolls)
def _stop(_vals, _rolls, _err):
    return 'Mend this slip, then Run again: ' + _err + ' ' + _did(_vals, _rolls, ', and your program stopped there')
_YOURS = ('dumb_luck', 'perception_roll', 'night_time')
def _keep(_name):
    _how = ('`' + _name + " = value` on its own line, so Mar'tu's check can change that line to try other values.")
    if _name in _YOURS:
        return 'Keep your box `' + _name + '` as ' + _how
    return 'Keep the box `' + _name + '` from the starter, as ' + _how
def _rerun(_values=None, _rolls=None):
    _tree = _ast.parse(_source)
    _vals = dict(_values or {})
    _seen = set()
    for _n in _tree.body:
        if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name':
            _id = _n.targets[0].id
            if _id in _vals and type(_n.value).__name__ == 'Constant':
                _n.value = _ast.copy_location(_ast.Constant(_vals[_id]), _n.value)
                _seen.add(_id)
    _ast.fix_missing_locations(_tree)
    _ns = {'__name__': '__main__'}
    _calls = []
    _seq = list(_rolls or [])
    def _fake(a, b):
        if len(_seq) > 1:
            _v = _seq.pop(0)
        elif _seq:
            _v = _seq[0]
        else:
            _v = a
        _calls.append((a, b, _v))
        return _v
    _real = _random.randint
    _keep_out = _sys.stdout
    _buf = _io.StringIO()
    _err = ''
    _random.randint = _fake
    _sys.stdout = _buf
    try:
        if _SETUP:
            exec(compile(_SETUP, '<setup>', 'exec'), _ns)
        exec(compile(_tree, 'main.py', 'exec'), _ns)
    except Exception as _e:
        _err = type(_e).__name__ + ': ' + str(_e)
    finally:
        _sys.stdout = _keep_out
        _random.randint = _real
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    return _ns, _rows, _calls, _err, sorted(_k for _k in _vals if _k not in _seen)
'''


def _rerun_code(setup=""):
    return _RERUN.replace("__SETUP__", repr(setup))


def _case(values=None, rolls=None):
    return (dict(values or {}), list(rolls or []))


def lines_check(label, cases, setup=""):
    """CMB on printed lines. cases = [(values, rolls, must_print, must_not_print, tail), ...]."""
    rows = [(dict(v or {}), list(r or []), list(want), list(never), tail) for v, r, want, never, tail in cases]
    code = _rerun_code(setup) + (
        f"for _vals, _rolls, _want, _never, _tail in {rows!r}:\n"
        "    _ns, _rows, _calls, _err, _miss = _rerun(_vals, _rolls)\n"
        "    assert not _miss, _keep(_miss[0])\n"
        "    assert not _err, _stop(_vals, _rolls, _err)\n"
        "    for _w in _want:\n"
        "        assert _w in _rows, _mend(_tail, '`' + _w + '` did not print.', _vals, _rolls)\n"
        "    for _w in _never:\n"
        "        assert _w not in _rows, _mend(_tail, '`' + _w + '` printed anyway.', _vals, _rolls)\n"
    )
    return (label, code)


def box_check(label, target, cases, setup="", show=None, kept=False):
    """CMB on a box. cases = [(values, rolls, expected, tail), ...]: after the rerun, `target` holds expected.
    `tail` is the fix, so it comes first. `show` = the value names the message mentions (all of them when None):
    the rerun may set more, so a student's own numbers never change the expected answer. `kept=True`: the starter
    already makes `target`, so a missing one gets "Keep the box ... from the starter"."""
    rows = [(dict(v or {}), list(r or []), want, tail) for v, r, want, tail in cases]
    missing = (f"'Keep the box `{target}` from the starter.'" if kept else
               f"'Make a box named `{target}`: start a line with `{target} = `.'")
    code = _rerun_code(setup) + (
        f"_target = {target!r}\n"
        f"_show_only = {list(show or [])!r}\n"
        f"for _vals, _rolls, _want, _tail in {rows!r}:\n"
        "    _ns, _rows, _calls, _err, _miss = _rerun(_vals, _rolls)\n"
        "    assert not _miss, _keep(_miss[0])\n"
        "    _shown = {_k: _v for _k, _v in _vals.items() if _k in _show_only} if _show_only else _vals\n"
        "    assert not _err, _stop(_shown, _rolls, _err)\n"
        f"    assert _target in _ns, {missing}\n"
        "    _got = _ns[_target]\n"
        "    _was = globals().get(_target)\n"
        "    if type(_got).__name__ == 'str' and type(_want).__name__ == 'bool':\n"
        "        assert False, ('Take the quotes off: `' + _target + '` holds the text ' + _show(_got) + '. '\n"
        "                       '`True` and `False` have no quotes: they are Python' + chr(39) + 's yes and no.')\n"
        "    assert type(_got).__name__ == type(_want).__name__ and _got == _want, _mend(_tail, '`' + _target + '` '\n"
        "        + ('stayed ' if _got == _was else 'became ') + _show(_got) + ', not ' + _show(_want) + '.', _shown, _rolls)\n"
    )
    return (label, code)


_BND = r'''
_R, _N_name = __ROLL__, __NEEDED__
_via_rolls = __VIA_ROLLS__
_N = globals().get(_N_name)
assert _N is not None, 'Keep the box `' + _N_name + '` from the starter, as `' + _N_name + ' = ` and a whole number.'
assert type(_N).__name__ == 'int', 'Give `' + _N_name + '` a whole number, with no quotes.'
if _via_rolls:
    assert 2 <= _N <= 20, 'Pick a `' + _N_name + '` from 2 to 20: a d20 roll is 1 to 20.'
    _lo, _hi = 1, 20
else:
    _lo, _hi = _N - 6, _N + 6
def _mask(_rows, _nums):
    # Every whole number becomes '#', so `Rolled 14: it opens.` and `Rolled 18: it opens.` are the same line.
    return [_re.sub(r'(?<![\w.])-?\d+(?!\w)(?!\.\d)', '#', _l) for _l in _rows]
def _case_of(_r, _n):
    _vals = {} if _n == _N else {_N_name: _n}
    if not _via_rolls:
        _vals[_R] = _r
    return _vals, ([_r] if _via_rolls else [])
def _ev(_r, _n=None):
    return _did(*_case_of(_r, _N if _n is None else _n))
def _ev_many(_rs):
    _list = ', '.join(str(_r) for _r in _rs[:-1]) + ' and ' + str(_rs[-1])
    if _via_rolls:
        return "(Mar'tu's check rolled " + _list + ' for you, only inside the check.)'
    return "(Mar'tu's check tried `" + _R + '` at ' + _list + ', only inside the check.)'
def _try(_r, _n=None):
    _n = _N if _n is None else _n
    _vals, _rolls = _case_of(_r, _n)
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, _rolls)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, _rolls, _err)
    if _via_rolls:
        assert _calls, ('Roll the die into `' + _R + "` with `random.randint(1, 20)`, so Mar'tu's check can roll "
                        'for you.')
    return _mask(_rows, [_r, _n])
_H = _try(_hi)
_L = _try(_lo)
assert _H, ('Print a success line when `' + _R + '` reaches `' + _N_name + '`. Your program printed nothing. '
            + _ev(_hi))
assert _L, 'Add `else:` with a failure line under it. Your program printed nothing. ' + _ev(_lo)
_E = _try(_N)
if _H == _L:
    assert _E == _H, ('Use `>=`, so a higher roll passes too. Only a roll of exactly ' + str(_N) + ' gave the success '
                      'line. ' + _ev_many([_lo, _N, _hi]))
    assert False, ('Ask whether `' + _R + '` reaches `' + _N_name + '`, and give the two lines different words. Both '
                   'rolls printed the same thing. ' + _ev_many([_lo, _hi]))
# Exactly one of the two lines prints. A failure line with no indent (no `else:`) prints after every roll.
assert [_l for _l in _L if _l not in _H], ('Put the failure line under `else:`, indented, so only one line prints. It '
                                           'printed the failure line as well as the success line. ' + _ev(_hi))
assert [_l for _l in _H if _l not in _L], ('Indent the success line under the `if`, and the failure line under '
                                           '`else:`. It printed the success line as well as the failure line. ' + _ev(_lo))
assert _E == _H, (('Use `>=`, so exactly enough passes: a roll of ' + str(_N) + ' or more gives the success line. It '
                   'gave the failure line. ' if _E == _L else
                   'Print the success line here, the same as for a high roll. ') + _ev(_N))
_B = _try(_N - 1)
assert _B == _L, (('Give a roll below `' + _N_name + '` the failure line. It gave the success line. ' if _B == _H else
                   'Print the failure line here, the same as for a low roll. ') + _ev(_N - 1))
if _N + 1 <= _hi:
    _A = _try(_N + 1)
    assert _A == _H, 'Print the success line here, the same as for a high roll. ' + _ev(_N + 1)
_M = _N + 3 if (not _via_rolls or _N + 3 <= 20) else _N - 3
_B2 = _try(_M - 1, _M)
_E2 = _try(_M, _M)
assert _B2 == _L and _E2 == _H, ('Ask with the box `' + _N_name + '`, not a number you typed. With `' + _N_name + ' = '
                                 + str(_M) + '`, your program ' + ('passed ' + _a_roll(_M - 1) if _B2 != _L else
                                 'failed ' + _a_roll(_M)) + ". (Mar'tu's check tried `" + _N_name + ' = ' + str(_M)
                                 + '`, only inside the check.)')
'''


def bnd_check(label, roll, needed, via_rolls=False, setup=""):
    """BND: exactly enough passes, one below fails, and the test follows the box `needed` (not a typed number)."""
    code = _rerun_code(setup) + (
        _BND.replace("__ROLL__", repr(roll)).replace("__NEEDED__", repr(needed))
        .replace("__VIA_ROLLS__", repr(bool(via_rolls)))
    )
    return (label, code)


_RND = r'''
_target, _faces, _placeholder = __TARGET__, __FACES__, __PLACEHOLDER__
_ns, _rows, _calls, _err, _miss = _rerun({}, __ROLLS__)
assert not _err, _stop({}, __ROLLS__, _err)
_fix = '`' + _target + ' = random.randint(1, ' + str(_faces) + ')`'
assert _target in _ns, 'Keep the box `' + _target + '` from the starter, and roll it: ' + _fix + '.'
_got = _ns[_target]
_left = [_n for _n in _ast.parse(_source).body if _placeholder is not None and type(_n).__name__ == 'Assign'
         and len(_n.targets) == 1
         and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == _target
         and type(_n.value).__name__ == 'Constant' and _n.value.value == _placeholder]
assert not (_left and _got == _placeholder and not [_c for _c in _calls if _c[2] == _got]), ('Roll it: ' + _fix + ". `" + _target + "` still holds the starter's `"
                                    + str(_placeholder) + '`.')
assert _assigned_from_expression(_target) and _calls, 'Roll it: ' + _fix + '. `' + _target + '` holds a number you typed.'
_from = [_c for _c in _calls if _c[2] == _got]
assert _from, 'Roll it: ' + _fix + '. `' + _target + '` does not hold the roll yet.'
_a, _b = _from[0][0], _from[0][1]
_call = '`random.randint(' + str(_a) + ', ' + str(_b) + ')`'
_die = ('Use ' + _fix + ': a d' + str(_faces) + ' has faces 1 to ' + str(_faces) + ', and `randint` includes both '
        'ends. ')
assert _a >= 1, _die + _call + ' can give ' + str(_a) + '.'
assert _b <= _faces, _die + _call + ' can give ' + str(_b) + '.'
assert _b >= _faces, _die + _call + ' never gives ' + str(_faces) + '.'
assert _a <= 1, _die + _call + ' never gives 1.'
'''


def rnd_check(label, target, faces, rolls, placeholder=None):
    """RND: `target` holds the value of a scripted randint call, and that call was randint(1, faces).
    `rolls` are distinct values, so each box can be traced back to its own call. `placeholder`: the number the
    starter puts in the box (`sword_roll = 0`), named as the starter's when it is still there."""
    code = _rerun_code() + (
        _RND.replace("__TARGET__", repr(target)).replace("__FACES__", repr(faces)).replace("__ROLLS__", repr(list(rolls)))
        .replace("__PLACEHOLDER__", repr(placeholder))
    )
    return (label, code)


_NAME_TEMPLATE = '''import ast as _ast
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
    _skip = __SKIP__
    _left = [_m for _m in _made if _m in _foreign]
    _near = [_m for _m in _made if _m not in _foreign and _m not in _skip and _close(_m)]
    _bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == "Expr" and type(_n.value).__name__ == "Constant" and type(_n.value.value).__name__ in ("str", "int", "float")]
    _other = [_m for _m in _made if _m not in _skip]
    if _near:
        _msg = "Python matches names letter for letter: you wrote `" + _near[0] + "`, the task needs `__NAME__`."
    elif _left:
        _msg = "`" + _left[0] + "` is a name from an example or an earlier step. This task's box is `__NAME__`."
    elif _bare:
        _msg = "Line " + str(_bare[0]) + " is a value with no box, so Python made it and forgot it. Put `__NAME__ = ` in front of it."
    elif _other:
        _msg = "You made a box named `" + _other[0] + "`, but this task's box is `__NAME__`. Python matches names letter for letter."
    else:
        _msg = "Make a box named `__NAME__`: start a line with `__NAME__ = `."
    assert False, _msg'''


def name_check(name, foreign=(), skip=()):
    """NAME + LEFT + BARE: the box exists, or the message says why not. `skip` = boxes the starter already makes."""
    code = (_NAME_TEMPLATE.replace("__NAME__", name).replace("__FOREIGN__", repr(list(foreign)))
            .replace("__SKIP__", repr(list(skip))))
    return (f"there is a box named {name}", code)


def strexact_check(wanted, label="the quoted text is exact"):
    """STREXACT: a quoted literal differs from one of `wanted` only by capitals or spaces."""
    return (
        label,
        "import ast as _ast\n"
        f"_wanted = {list(wanted)!r}\n"
        "def _squash(_s):\n"
        "    return _s.lower().replace(' ', '')\n"
        "_bad = [(_c.value, _w) for _c in _ast.walk(_ast.parse(_source)) if type(_c).__name__ == 'Constant' "
        "and type(_c.value).__name__ == 'str' for _w in _wanted if _c.value != _w and _squash(_c.value) == _squash(_w)]\n"
        "assert not _bad, ('`\"' + (_bad[0][0] if _bad else '') + '\"` and `\"' + (_bad[0][1] if _bad else '') + "
        "'\"` are different text to Python: every letter, space and capital counts.')\n",
    )


def blanks_check(what="a line of your own", verb="prints"):
    """The starter's `"___"` placeholder left inside quotes (it runs, so only a check can catch it)."""
    return (
        "no ___ left in the quotes",
        "import ast as _ast\n"
        "_left = [_c.lineno for _c in _ast.walk(_ast.parse(_source)) if type(_c).__name__ == 'Constant' "
        "and type(_c.value).__name__ == 'str' and _c.value.strip() == '___']\n"
        f"assert not _left, 'Replace the `___` with {what}, inside the quotes. Line ' + str(_left[0] if _left else 0) + "
        f"\" still {verb} the starter's `___`.\"\n",
    )


def out_check(want, label, near_msg, missing_msg):
    """OUT on a fixed line (never the only check on a computed value): the exact line is printed. A line that
    matches it except for capitals, spaces or the end mark gets `near_msg`."""
    return (
        label,
        f"_want = {want!r}\n"
        "def _squash(_s):\n"
        "    return _s.lower().replace(' ', '').rstrip('.!?')\n"
        "_near = [_l for _l in _lines() if _l != _want and _squash(_l) == _squash(_want)]\n"
        f"assert _want in _lines() or not _near, {near_msg!r}\n"
        f"assert _want in _lines(), {missing_msg!r}\n",
    )


_FROM_BOXES = r'''import ast as _ast
_target, _boxes, _fix, _placeholder = __TARGET__, __BOXES__, __FIX__, __PLACEHOLDER__
_tree = _ast.parse(_source)
def _sets(_n):
    return type(_n).__name__ == 'Assign' and any(type(_t).__name__ == 'Name' and _t.id == _target for _t in _n.targets)
_made = [_n for _n in _ast.walk(_tree) if _sets(_n)]
_two = [_n for _n in _made if len(_n.targets) > 1]
_also = [_t.id for _n in _two for _t in _n.targets if type(_t).__name__ == 'Name' and _t.id != _target]
assert not _two, (_fix + ' Your `' + _target + '` line has two `=` signs, so it puts a value in `'
                  + (_also[0] if _also else _target) + '` too. `=` puts a value in a box.')
def _names(_n):
    return {_x.id for _x in _ast.walk(_n) if type(_x).__name__ == 'Name'}
_used = set()
for _n in _made:
    _used |= _names(_n.value)
for _n in _ast.walk(_tree):
    if type(_n).__name__ == 'If' and any(_sets(_x) for _x in _ast.walk(_n)):
        _used |= _names(_n.test)
# Quoted text (`can_cast = "True"`) is left to the box check, whose message is about the quotes.
_quoted = [_n for _n in _made if type(_n.value).__name__ == 'Constant' and type(_n.value.value).__name__ == 'str']
_asked = bool(_used & set(_boxes))
_still = [_n for _n in _made if _placeholder is not None and type(_n.value).__name__ == 'Constant'
          and repr(_n.value.value) == repr(_placeholder)]
assert not _still or _asked, _fix + ' `' + _target + "` still holds the starter's `" + repr(_placeholder) + '`.'
assert not _made or not __CHECK_TYPED__ or _quoted or _asked, (_fix + ' `' + _target + '` is made from values you '
    'typed, so it can never change when the boxes change.')
'''


def from_boxes_check(target, boxes, fix, typed=True, label=None, placeholder=None):
    """`target` is not made with two `=` signs (`can_cast = mana = cost`), and (typed=True) it is worked out from the
    boxes, not from typed values (`can_cast = True`, `can_cast = 12 >= 9 and 9 >= 9`). An `if` whose test uses the
    boxes and whose branches set `target` to True or False counts as worked out from the boxes. `placeholder`: the
    starter's value for `target` (`False`); while it is still there, the message says so. `fix` comes first."""
    code = (_FROM_BOXES.replace("__TARGET__", repr(target)).replace("__BOXES__", repr(list(boxes)))
            .replace("__FIX__", repr(fix)).replace("__CHECK_TYPED__", repr(bool(typed)))
            .replace("__PLACEHOLDER__", repr(placeholder)))
    return (label or f"{target} is asked, not typed", code)


_DEAD_BRANCH = r'''import ast as _ast
_box = __BOX__
def _top(_t):
    # `box <= 12` and `box < 13` both mean "at most 12": the highest number that passes, or None
    if type(_t).__name__ != 'Compare' or len(_t.ops) != 1 or type(_t.left).__name__ != 'Name' or _t.left.id != _box:
        return None
    _c = _t.comparators[0]
    if type(_c).__name__ != 'Constant' or type(_c.value).__name__ != 'int':
        return None
    _op = type(_t.ops[0]).__name__
    return _c.value if _op == 'LtE' else _c.value - 1 if _op == 'Lt' else None
_dead = None
for _n in _ast.walk(_ast.parse(_source)):
    if type(_n).__name__ != 'If':
        continue
    _seen, _at = [], _n
    while _at is not None and _dead is None:
        _cap = _top(_at.test)
        if _cap is not None:
            _wider = [_w for _w in _seen if _w >= _cap]
            if _wider:
                _dead = (_wider[0], _cap)
            _seen.append(_cap)
        _at = _at.orelse[0] if len(_at.orelse) == 1 and type(_at.orelse[0]).__name__ == 'If' else None
assert _dead is None, ('Mend the chain itself: first, the test that lets the fewest numbers through. Right colors, but '
    'the old chain still asks `' + _box + ' <= ' + str(_dead[0] if _dead else 0) + '` before `' + _box + ' <= '
    + str(_dead[1] if _dead else 0) + '`, so that branch never runs.')
'''


def dead_branch_check(box, label="the chain itself is in order"):
    """In an if/elif chain on `box <= n` tests, a later test that is no wider than an earlier one can never run.
    Placed after the behavior check, so it only speaks when the colors are right but the old chain was kept and a
    second `if` patches it afterwards."""
    return (label, _DEAD_BRANCH.replace("__BOX__", repr(box)))


_ONE_CHAIN = r'''import ast as _ast
_box = __BOX__
def _sets(_n):
    return any(type(_x).__name__ == 'Assign' and any(type(_t).__name__ == 'Name' and _t.id == _box for _t in _x.targets)
               for _x in _ast.walk(_n))
_chains = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'If' and _sets(_n)]
assert len(_chains) <= 1, ('Make it one chain: one `if`, then `elif`, then `else`. Right colors, but `' + _box
                           + '` comes from ' + str(len(_chains)) + ' separate `if`s.')
'''


def one_chain_check(box, label="one chain sets the box"):
    """The box is set inside ONE top-level `if` chain (if / elif / else), not by several separate `if`s. A default
    line before the chain (`box = ...` with no `if`) is fine. Placed after the behavior check and the dead-branch
    check, so it only speaks when the colors are already right."""
    return (label, _ONE_CHAIN.replace("__BOX__", repr(box)))


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of control-flow; must match u02a and u02c exactly)
# ---------------------------------------------------------------------------------------------

UNIT = dict(
    id="control-flow",
    order=2,
    title="Control Flow",
    subtitle="The Ley Clock Decides",
    published=True,
    martu_intro=(
        "The Ley Clock does not panic. It checks. If the hand is near the arc, it warns. Otherwise, it waits.\n"
        "Today you teach Python to check the same way. And you learn to roll dice, because the world is not fair, "
        "yes?\n"
        "You have seen this code already: the four dialogue options, the trap-door skill checks. It felt like a "
        "wall. Now we take it apart, one stone at a time."
    ),
    goals=[
        "Ask yes-or-no questions with `==`, `!=`, `<`, `>`, `<=` and `>=`, and get `True` or `False`",
        "Tell `=` (gets) from `==` (is the same as)",
        "Choose `>=` on purpose, so exactly enough still passes",
        "Compare text exactly, and with `.lower()` so capitals don't matter",
        "Write `if`, `else` and `elif` with colons and indents, knowing the first true branch wins",
        "Join questions with `and`, `or` and `not`",
        "Roll dice with `import random` and `random.randint(1, 20)`, both ends included",
        "Read Python's error message, find the line, and mend it",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="if",
        aliases=["if statement", "if line"],
        plain=(
            "A line that asks a yes-or-no question. When the answer is `True`, Python runs the indented lines "
            "under it. When it is `False`, Python skips them."
        ),
        example='if hours_left < 3:\n    print("Get inside!")',
    ),
    dict(
        term="indent",
        aliases=["indented", "indentation", "indents"],
        plain="Spaces at the start of a line. Four spaces under an `if` mean: this line belongs to the `if`.",
        example='if mana < 6:\n    print("Low mana.")',
    ),
    dict(
        term="colon",
        aliases=["colons"],
        plain="The `:` mark at the end of an `if`, `elif` or `else` line. It says: here comes the block.",
        example="if roll >= needed:",
    ),
    dict(
        term="block",
        aliases=["blocks"],
        plain="The indented lines under an `if`, `elif` or `else`. They run together, or not at all.",
        example='if hours_left < 3:\n    print("Get inside!")\n    print("Shield up.")',
    ),
    dict(
        term="else",
        aliases=["otherwise"],
        plain="The part that runs when the `if` question was `False`. It has no question of its own.",
        example='if roll >= needed:\n    print("It opens.")\nelse:\n    print("It holds.")',
    ),
    dict(
        term="elif",
        aliases=["else if"],
        plain=(
            "Short for else, if: another question, asked only when the ones above were `False`. Python takes the "
            "first branch whose answer is `True`."
        ),
        example='if hours_left <= 2:\n    color = "red"\nelif hours_left <= 12:\n    color = "bright blue"',
    ),
    dict(
        term="branch",
        aliases=["branches"],
        plain="One path through an `if` chain: the `if` part, one `elif` part, or the `else` part. Only one runs.",
        example='elif choice == "option 2":',
    ),
    dict(
        term="and",
        plain="Joins two questions. `a and b` is `True` only when both are `True`.",
        example="mana >= cost and affinity >= required",
    ),
    dict(
        term="or",
        plain="Joins two questions. `a or b` is `True` when at least one of them is `True`.",
        example="first_roll >= needed or second_roll >= needed",
    ),
    dict(
        term="not",
        plain="Flips a yes-or-no answer. `not True` is `False`, and `not False` is `True`.",
        example="not barrier_up",
    ),
    dict(
        term="import",
        aliases=["imports", "import random"],
        plain="Brings in a set of tools Python keeps on the shelf. `import random` brings in Python's dice.",
        example="import random",
    ),
    dict(
        term="randint",
        aliases=["random.randint", "random.randint()"],
        plain="`random.randint(1, 6)` gives a random whole number from 1 to 6. Both ends are included.",
        example="random.randint(1, 20)",
    ),
    dict(
        term="match",
        aliases=["match statement", "case"],
        plain=(
            "Another way to choose: `match choice:` then one `case` for each value. `case _:` catches "
            "anything else."
        ),
        example='match choice:\n    case "option 1":\n        print("Then we leave at dawn.")\n    case _:\n        print("Hm.")',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (2b-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_2B = dict(
    kind="quiz",
    id="2b-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from earlier lessons. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 2B; recall from 2A (= versus ==) and 1C "
        "(str() glue). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="which-one-asks",
            q="`=` or `==`: which one asks a question?",
            choices=["`=`", "`==`"],
            answer=1,
            why_wrong={0: "`=` puts a value in a box. Read it as gets: `mana = 26` means mana gets 26."},
            explain="`==` asks: is the same as? `hero == \"Lucky\"` asks whether hero is Lucky. `=` puts.",
        ),
        dict(
            type="predict",
            id="mana-glue",
            q="What will this print?",
            code='print("Mana: " + str(4 + 3))\n',
            choices=["Mana: 7", "Mana: 4 + 3", "Mana: 43", "an error"],
            answer="Mana: 7",
            explain="Python does the math inside the brackets first: 4 + 3 is 7. `str(7)` turns it into text to glue.",
        ),
    ],
)

# =============================================================================================
# Lesson 2B "If the Clock Turns Red"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 2B-01 first-if
# ---------------------------------------------------------------------------------------------

FIRST_IF_STARTER = 'hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\n'
FIRST_IF_SOLUTION = 'hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\n    print("Shield up.")\n'
SHIELD_INDENT = "Indent `print(\"Shield up.\")` with four spaces, like the line above it, so it belongs to the `if`."

# Both checks rerun the program with their own `hours_left`, so a student who left it at 10 after the Investigate
# still passes. `Get inside` is matched at the start of a line, so Lucky's side quest (`Get inside! 2 hours left.`)
# keeps the step green.
_FIRST_IF_RUNS = r"""
def _inside(_rows):
    return [_l for _l in _rows if _l.startswith('Get inside')]
_runs = {}
for _h in (2, 10, 1):
    _ns, _rows, _calls, _err, _miss = _rerun({'hours_left': _h}, [])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop({'hours_left': _h}, [], _err)
    _runs[_h] = _rows
"""
_FIRST_IF_SHIELD = _FIRST_IF_RUNS + r"""
def _squash(_s):
    return _s.lower().replace(' ', '').rstrip('.!?')
_near = [_l for _l in _runs[2] if _l != 'Shield up.' and _squash(_l) == _squash('Shield up.')]
assert 'Shield up.' in _runs[2] or not _near, ('Close! Print `Shield up.` exactly, period and all: every letter, '
                                               'space and capital counts.')
assert 'Shield up.' in _runs[2], _mend('Add a line that prints `Shield up.`, indented under the `if` like line 3.',
                                       'Your program did not print it.', {'hours_left': 2}, [])
"""
_FIRST_IF_BELONGS = _FIRST_IF_RUNS + r"""
assert not _inside(_runs[10]), _mend('Keep `if hours_left < 3:` above both prints, so they run only when the answer is '
                                     '`True`.', '`Get inside!` printed anyway.', {'hours_left': 10}, [])
assert 'Shield up.' not in _runs[10], _mend(__INDENT__, '`Shield up.` printed anyway.',
                                            {'hours_left': 10}, [])
assert _inside(_runs[1]) and 'Shield up.' in _runs[1], _mend('Keep both prints indented under the `if`.',
                                                             'Your program did not print both lines.', {'hours_left': 1}, [])
""".replace("__INDENT__", repr(SHIELD_INDENT))

FIRST_IF = dict(
    id="first-if",
    title="If",
    martu=(
        "An [[if]] asks a question. When the answer is `True`, Python runs the [[indent|indented]] lines under it. "
        "When it is `False`, Python skips them.\n"
        "The `if` line ends with a [[colon]]. The lines that belong to it start with four spaces.\n"
        "Run it. Then change `hours_left` to 10 and run again. Why does nothing print?"
    ),
    introduces=["node:If"],
    example='oil_flasks = 1\nif oil_flasks < 2:\n    print("Fill the lantern.")\n',
    example_output="Fill the lantern.",
    names=["hours_left"],
    predict=dict(
        q="Before you press Run: what will this print?",
        choices=["Get inside!", "True", "Nothing at all"],
        answer=0,
        explain=(
            "Step by step:\n"
            "1. `hours_left = 2`: the box holds 2.\n"
            "2. `if hours_left < 3:` asks: is 2 less than 3? `True`.\n"
            "3. So the indented line runs: `Get inside!`\n"
            "Now change line 1 to `hours_left = 10` and run. 10 < 3 is `False`, so Python skips the indented line. "
            "Nothing prints. Change it back to 2 for the next step."
        ),
    ),
    pair_talk="Pair talk: tell your partner why nothing printed when `hours_left` was 10. Then each of you does the step.",
    starter=FIRST_IF_STARTER,
    checkpoints=[
        dict(
            id="second-indented-line",
            text="Add a second indented line under the `if` that prints `Shield up.`",
            dictated=True,
            hints=[
                "Start like this: on a new line under line 3, type four spaces, then `print(`",
                "Look at line 3. It starts with four spaces, so it belongs to the `if`. Your new line needs the same.",
                "Every indented line belongs to the `if`:\n```python\nif rain > 0:\n    print(\"Take the umbrella.\")\n"
                "    print(\"Wear boots.\")\n```\nBoth lines run when it rains. Neither runs when it doesn't.",
            ],
            checks=[
                ("prints Shield up.", _rerun_code() + _FIRST_IF_SHIELD),
                ("both lines belong to the if", _rerun_code() + _FIRST_IF_BELONGS),
            ],
            pass_line="Bomb Shell: Shield up.",
        ),
    ],
    solution=FIRST_IF_SOLUTION,
    assemble=dict(
        lines=["hours_left = 2", "if hours_left < 3:", '    print("Get inside!")', '    print("Shield up.")'],
        distractors=['print("Shield up.")', "if hours_left < 3"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A fork in the road",
            text=(
                "```text\nhours_left < 3 ?\n   True  -> run the indented lines\n   False -> skip them, go on\n```\n"
                "The `if` is a fork. The question decides which way Python walks."
            ),
        ),
        dict(
            angle="everyday",
            label="If it rains",
            text=(
                "If it rains, take the umbrella and wear boots. No rain? You skip both. The indented lines are "
                "the things you do only when it rains."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "With `hours_left = 10`:\n"
                "1. `hours_left = 10`: the box holds 10.\n"
                "2. `if hours_left < 3:` asks: is 10 less than 3? `False`.\n"
                "3. Python skips every indented line under the `if`.\n"
                "4. Nothing prints."
            ),
        ),
        dict(
            angle="in Tor",
            label="The barrier door",
            text=(
                "My barrier door opens only if the hours are short. Long hours, the door stays shut, and the "
                "lines behind it never happen."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants numbers. Change the warning so it shows the hours left too, like `Get inside! 2 hours "
            "left.` Glue `hours_left` in with `str()`."
        ),
        hints=[
            "Start like this: `print(\"Get inside! \" + `",
            "A number needs `str()` before it can be glued to text.",
        ],
        checks=[
            (
                "the warning shows the hours",
                _rerun_code() +
                "for _h in (1, 2):\n"
                "    _ns, _rows, _calls, _err, _miss = _rerun({'hours_left': _h}, [])\n"
                "    assert not _err, _stop({'hours_left': _h}, [], _err)\n"
                r"    _hit = [_l for _l in _rows if 'Get inside' in _l and _re.search(_whole(_h), _l)]" "\n"
                "    assert _hit, _mend('Glue in the box: `str(hours_left)`.', 'The `Get inside!` line did not show ' + "
                "str(_h) + '.', {'hours_left': _h}, [])\n",
            ),
        ],
        solution=(
            'hours_left = 2\nif hours_left < 3:\n    print("Get inside! " + str(hours_left) + " hours left.")\n'
            '    print("Shield up.")\n'
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:',
        why=(
            "You have seen this in `cast_spell`. The `if` asked a question: is the affinity too low? When the "
            "answer was True, the indented `print_prompt` line ran. Same shape as today: a question, a colon, "
            "indented lines."
        ),
    ),
    takeaway="`if question:` then indented lines. True: they run. False: Python skips them.",
    wrong_answers=[
        dict(why="the second print not indented (it always runs)",
             code='hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\nprint("Shield up.")\n',
             fails_at=1, message_contains="10"),
        dict(why="the if removed: both lines typed (they always run)",
             code='hours_left = 2\nprint("Get inside!")\nprint("Shield up.")\n', fails_at=1, message_contains="10"),
        dict(why="no period", code='hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\n    print("Shield up")\n',
             fails_at=1, message_contains="period"),
        dict(why="uneven indent (2 spaces under 4)",
             code='hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\n  print("Shield up.")\n',
             fails_at=0, message_contains="indent"),
        dict(why="too many spaces (an unexpected indent)",
             code='hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\n        print("Shield up.")\n',
             fails_at=0, message_contains="unexpected indent"),
        dict(why="the colon dropped", code='hours_left = 2\nif hours_left < 3\n    print("Get inside!")\n    print("Shield up.")\n',
             fails_at=0, message_contains="expected ':'"),
        dict(why="the condition typed as True (it always runs)",
             code='hours_left = 2\nif True:\n    print("Get inside!")\n    print("Shield up.")\n',
             fails_at=1, message_contains="Keep `if hours_left < 3:`"),
        dict(why="the condition widened so both lines print at 10 (check probe: told to keep the if, not to indent)",
             code='hours_left = 2\nif hours_left < 11:\n    print("Get inside!")\n    print("Shield up.")\n',
             fails_at=1, message_contains="Keep `if hours_left < 3:`"),
        dict(why="Shield up. under a second if that asks about this one hour only (hard-coded)",
             code='hours_left = 2\nif hours_left < 3:\n    print("Get inside!")\nif hours_left == 2:\n    print("Shield up.")\n',
             fails_at=1, message_contains="hours_left = 1"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="if-else", solo="false", dictates="1",
             foreign_names="oil_flasks,rain", stages="P,R,I,M", trace="static step table (predict explain + another_way)") + "\n"
        "Investigate (change hours_left to 10, nothing prints) is in the Learn text and the predict explanation, "
        "which also says to change it back. The checks never need that: both rerun with their own hours_left (2, 10 "
        "and 1), so a student who forgot to change it back and indented the line right still passes (check-breaker "
        "probe: the old OUT check read the real run and told them to 'add a line' they had added). `Get inside` is "
        "matched at the start of a line, so Lucky's side quest (`Get inside! 2 hours left.`) keeps the step green. "
        "WA evidence: the unindented second line (G1/G2 shape-without-meaning); the colon and the uneven indent "
        "prove the explainer rows (expected ':' / IndentationError)."
    ),
)


# ---------------------------------------------------------------------------------------------
# 2B-02 colon-and-indent (three bugs, one checkpoint each)
# ---------------------------------------------------------------------------------------------


def _colon(first_if="if hours_left < 3:", low_mana="if mana < 6:\n    print(\"Low mana.\")",
           last="if hours_left < 3:\n    print(\"Shield up.\")\n# This line should print every time, whatever the hours:\n"
                "print(\"The clock ticks on.\")"):
    return (
        "hours_left = 2\nmana = 4\n\n"
        f"{first_if}\n    print(\"Get inside!\")\n\n"
        f"{low_mana}\n\n"
        f"{last}\n"
    )


COLON_STARTER = _colon(
    first_if="if hours_left < 3",
    low_mana="if mana < 6:\nprint(\"Low mana.\")",
    last="if hours_left < 3:\n    print(\"Shield up.\")\n    # This line should print every time, whatever the hours:\n"
         "    print(\"The clock ticks on.\")",
)
COLON_LAST_BUG = ("if hours_left < 3:\n    print(\"Shield up.\")\n    # This line should print every time, whatever the hours:\n"
                  "    print(\"The clock ticks on.\")")

COLON_AND_INDENT = dict(
    id="colon-and-indent",
    title="Colon and indent",
    martu=(
        "Two marks make an `if` work. The [[colon]] at the end says: here comes the [[block]]. The indent says: "
        "this line belongs to it.\n"
        "This spell has three slips. Python names the first two, one at a time. Read the last line of its message "
        "first. The third slip is quiet: the program runs, but one line is in the wrong place."
    ),
    names=["hours_left", "mana"],
    pair_talk=(
        "Pair talk: hunt these slips together if you like. Read each message out loud, then each of you mends it "
        "on your own screen."
    ),
    starter=COLON_STARTER,
    checkpoints=[
        dict(
            id="mend-the-colon",
            text="Add the missing colon to the end of the first `if` line.",
            dictated=True,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Python's message says `expected ':'` and names line 4. Look at the very end of that line.",
                "Every `if` line ends with `:`. For example: `if rain > 0:`. The colon says: the block comes next.",
            ],
            checks=[
                lines_check("the first if works", [
                    ({"hours_left": 2}, None, ["Get inside!"], [],
                     "Keep `if hours_left < 3:` as the first `if`, with `print(\"Get inside!\")` indented under it."),
                    ({"hours_left": 10}, None, [], ["Get inside!"],
                     "Keep `if hours_left < 3:` as the first `if`, with `print(\"Get inside!\")` indented under it."),
                ]),
            ],
            pass_line="Mar'tu: One fixed. Python will show you the next one.",
        ),
        dict(
            id="mend-the-indent",
            text="Make the `Low mana.` line belong to the `if` above it.",
            dictated=False,
            hints=[
                "Read Python's last line first. It names the line to mend.",
                "Python says `expected an indented block` and names the line. The line under an `if` must start "
                "further right.",
                "A line belongs to an `if` when it is indented under it:\n```python\nif rain > 0:\n"
                "    print(\"Take the umbrella.\")\n```",
            ],
            checks=[
                lines_check("Low mana. belongs to its if", [
                    ({"mana": 4}, None, ["Low mana."], [], "Keep `if mana < 6:` and the print under it."),
                    ({"mana": 9}, None, [], ["Low mana."],
                     "Keep `if mana < 6:`, with the print indented under it, so it runs only when mana is low."),
                ]),
            ],
        ),
        dict(
            id="always-runs",
            text="`The clock ticks on.` should print every time, even with 10 hours left. Mend its line.",
            dictated=False,
            hints=[
                "Read Python's last line of output. Would it still print with `hours_left = 10`?",
                "Run the last `if` in your head with `hours_left = 10`. Which lines does it skip?",
                "A line with no indent does not belong to the `if`. It runs every time, after the `if` is done:\n"
                "```python\nif rain > 0:\n    print(\"Take the umbrella.\")\nprint(\"Off we go.\")\n```",
            ],
            checks=[
                lines_check("the last line always runs", [
                    ({"hours_left": 10}, None, ["The clock ticks on."], [],
                     "Take the indent off `print(\"The clock ticks on.\")`, so it does not belong to the `if`."),
                    ({"hours_left": 10}, None, [], ["Shield up."],
                     "Keep `print(\"Shield up.\")` indented under the last `if`. Only the clock line moves."),
                    ({"hours_left": 2}, None, ["Shield up.", "The clock ticks on."], [],
                     "Keep `print(\"Shield up.\")` indented under the last `if`, and the clock line after it."),
                ]),
                (
                    "the clock line is moved, not copied",
                    _rerun_code() +
                    "_ns, _rows, _calls, _err, _miss = _rerun({'hours_left': 2}, [])\n"
                    "assert not _err, _stop({'hours_left': 2}, [], _err)\n"
                    "assert _rows.count('The clock ticks on.') <= 1, _mend('Move the line instead of copying it: keep one, '\n"
                    "    'with no indent.', 'Your program printed `The clock ticks on.` twice.', {'hours_left': 2}, [])\n",
                ),
            ],
            pass_line="Mar'tu: Three slips, three mends. The colon opens the block, the indent fills it, yes?",
        ),
    ],
    solution=_colon(),
    assemble=dict(
        lines=[
            "hours_left = 2", "mana = 4", "if hours_left < 3:", '    print("Get inside!")', "if mana < 6:",
            '    print("Low mana.")', "if hours_left < 3:", '    print("Shield up.")', 'print("The clock ticks on.")',
        ],
        distractors=["if hours_left < 3", 'print("Low mana.")', '    print("The clock ticks on.")'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Colon, then indent",
            text=(
                "1. The colon says: here comes the block.\n"
                "2. The indent says: this line belongs to it.\n"
                "3. The first line with no indent ends the block. It runs every time."
            ),
        ),
        dict(
            angle="picture",
            label="A shelf",
            text=(
                "```text\nif hours_left < 3:\n    print(\"Shield up.\")\nprint(\"The clock ticks on.\")\n```\n"
                "The `if` line is the shelf, and `print(\"Shield up.\")` sits on it. `print(\"The clock ticks on.\")` "
                "is on the floor.\n"
                "Indented lines sit on the `if`'s shelf. They fall only when the answer is True. The floor is always "
                "there."
            ),
        ),
        dict(
            angle="shorter",
            text="Colon at the end of every `if` line. Four spaces for each line that belongs to it. No spaces: always runs.",
        ),
    ],
    takeaway="An `if` line ends with `:`. Indented lines belong to it. A line with no indent runs every time.",
    wrong_answers=[
        dict(why="the starter (missing colon first)", code=COLON_STARTER, fails_at=0, message_contains="expected ':'"),
        dict(why="colon mended, the Low mana line still not indented",
             code=_colon(low_mana="if mana < 6:\nprint(\"Low mana.\")", last=COLON_LAST_BUG),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="a semicolon instead of a colon",
             code=_colon(first_if="if hours_left < 3;", last=COLON_LAST_BUG), fails_at=0, message_contains="SyntaxError"),
        dict(why="both loud slips mended, the clock line still indented", code=_colon(last=COLON_LAST_BUG),
             fails_at=3, message_contains="hours_left = 10"),
        dict(why="indent slip 'mended' by deleting the if mana line (Low mana. always prints)",
             code=_colon(low_mana="print(\"Low mana.\")"), fails_at=2, message_contains="mana = 9"),
        dict(why="clock line mended by taking the indent off Shield up. too",
             code=_colon(last="if hours_left < 3:\n    print(\"Get inside, again!\")\nprint(\"Shield up.\")\n"
                              "print(\"The clock ticks on.\")"),
             fails_at=3, message_contains="Shield up."),
        dict(why="the last if deleted: both lines always print",
             code=_colon(last="print(\"Shield up.\")\nprint(\"The clock ticks on.\")"),
             fails_at=3, message_contains="Shield up."),
        dict(why="the clock line copied out of the block instead of moved (it prints twice at 2 hours)",
             code=_colon(last=COLON_LAST_BUG + "\nprint(\"The clock ticks on.\")"), fails_at=3, message_contains="twice"),
        dict(why="the first if's question replaced by True (Get inside! prints at 10 hours)",
             code=_colon(first_if="if True:"), fails_at=1, message_contains="as the first `if`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="if-else,read-traceback", solo="false", dictates="1",
             foreign_names="rain") + "\n"
        "Broken spell, three slips in Python's reporting order: the missing colon (expected ':'), then the "
        "unindented body (IndentationError: expected an indented block after 'if'), then the quiet one (a line that "
        "should always run is inside the block; behavior only, CMB at hours_left 10). Each loud slip proves its "
        "explainer row (2.6). On the site a crash fails every checkpoint, so no partials. Can be done in pairs; "
        "every student mends it on their own screen."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-03 otherwise (if/else, BND)
# ---------------------------------------------------------------------------------------------


def _latch(test="strength_roll >= strength_needed", win='"The latch pops open."', lose='"That latch hates me."',
           roll=14, needed=12):
    return (
        f"strength_roll = {roll}\nstrength_needed = {needed}\n"
        f"if {test}:\n    print({win})  # success line\nelse:\n    print({lose})  # failure line\n"
    )


OTHERWISE_STARTER = (
    "strength_roll = 14\nstrength_needed = 12\n"
    "if ___:\n    print(\"___\")  # success line\nelse:\n    print(\"___\")  # failure line\n"
)

OTHERWISE = dict(
    id="otherwise",
    title="Otherwise",
    martu=(
        "[[else]] means otherwise. It has no question of its own. It runs when the `if` answer was `False`.\n"
        "So exactly one of the two lines prints: the `if` block, or the `else` block. Never both.\n"
        "Look at the Example: Oogrish's perception check. Then write Bomb Shell's latch check. Keep the starter's "
        "box names, `strength_roll` and `strength_needed`, and use your own words for the two lines."
    ),
    example=(
        "spot_roll = 13\nspot_needed = 11\n"
        "if spot_roll >= spot_needed:\n    print(\"Oogrish spots the tracks.\")\nelse:\n    print(\"Nothing but mud.\")\n"
    ),
    example_output="Oogrish spots the tracks.",
    names=["strength_roll", "strength_needed"],
    pick="The latch pops open.",
    starter=OTHERWISE_STARTER,
    checkpoints=[
        dict(
            id="latch-check",
            text=(
                "Bomb Shell pries the latch. Print a success line when `strength_roll` reaches `strength_needed`, "
                "and a failure line otherwise."
            ),
            dictated=False,
            hints=[
                "Start like this: `if strength_roll `",
                "What question decides which line runs? Fill the `___` after `if` with it. Then replace each `___` "
                "in the quotes with your own words.",
                "`else:` has no question. It runs when the `if` didn't:\n```python\nif coins >= price:\n"
                "    print(\"Sold.\")\nelse:\n    print(\"Not enough coins.\")\n```",
                "Exactly enough passes: a 12 opens a latch that needs 12. That is `>=`, not `>`.",
            ],
            checks=[blanks_check("your own words"), bnd_check("exactly enough passes", "strength_roll", "strength_needed")],
            pass_line="Bomb Shell: The latch pops open.",
        ),
    ],
    solution=_latch(),
    assemble=dict(
        lines=["strength_roll = 14", "strength_needed = 12", "if strength_roll >= strength_needed:",
               '    print("The latch pops open.")', "else:", '    print("That latch hates me.")'],
        distractors=["if strength_roll > strength_needed:", "else strength_roll < strength_needed:"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two doors",
            text=(
                "```text\nstrength_roll >= strength_needed ?\n   True  -> door 1: the if block\n"
                "   False -> door 2: the else block\n```\nOne question, two doors. Python walks through exactly one."
            ),
        ),
        dict(
            angle="everyday",
            label="Coat or sunglasses",
            text="If it rains, take a coat. Otherwise, take sunglasses. You never take both, and you never take neither.",
        ),
        dict(
            angle="step-by-step",
            label="Try 11, 12, 13",
            text=(
                "With `strength_needed = 12`:\n"
                "1. A roll of 11: is 11 >= 12? `False`, so the `else` line prints.\n"
                "2. A roll of 12: is 12 >= 12? `True`. Exactly enough passes.\n"
                "3. A roll of 13: `True` too."
            ),
        ),
        dict(angle="shorter", text="`if` question `:` then the success line. `else:` then the failure line."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants to see the dice. Show the roll in both lines, like `Rolled 14. The latch pops open.` "
            "Glue it in with `str(strength_roll)`."
        ),
        hints=[
            "Start like this: `print(\"Rolled \" + `",
            "Both the `if` line and the `else` line need the roll.",
        ],
        checks=[
            (
                "both lines show the roll",
                _rerun_code() +
                "_N = globals().get('strength_needed', 12)\n"
                "for _r in (_N - 5, _N + 5):\n"
                "    _ns, _rows, _calls, _err, _miss = _rerun({'strength_roll': _r}, [])\n"
                "    assert not _err, _stop({'strength_roll': _r}, [], _err)\n"
                r"    _hit = [_l for _l in _rows if _re.search(_whole(_r), _l)]" "\n"
                "    assert _hit, _mend('Glue in `str(strength_roll)`, in the `if` line and in the `else` line.', "
                "'The line did not show ' + str(_r) + '.', {'strength_roll': _r}, [])\n",
            ),
        ],
        solution=_latch(win='"Rolled " + str(strength_roll) + ". The latch pops open."',
                        lose='"Rolled " + str(strength_roll) + ". That latch hates me."'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="required_roll = 12\nreturn roll >= required_roll",
        why=(
            "You have seen this at the trap door. `strength_check` said `return roll >= required_roll`: the same "
            "question your `if` asks now. With `>=`, a roll of exactly 12 still pried the hatch open."
        ),
    ),
    takeaway="`if` question: success line. `else:` failure line. Exactly one runs. Exactly enough passes: `>=`.",
    wrong_answers=[
        dict(why="the example's names copied (A-05/A-07/A-08 player_name)",
             code=_latch(test="spot_roll >= spot_needed"), fails_at=0, message_contains="spot_roll"),
        dict(why="> instead of >= (exactly enough fails)", code=_latch(test="strength_roll > strength_needed"),
             fails_at=1, message_contains="exactly"),
        dict(why="else with a question", code=(
            "strength_roll = 14\nstrength_needed = 12\nif strength_roll >= strength_needed:\n"
            "    print(\"The latch pops open.\")\nelse strength_roll < strength_needed:\n    print(\"That latch hates me.\")\n"),
             fails_at=0, message_contains="expected ':'"),
        dict(why="= instead of == in the if (assigns instead of asking)", code=_latch(test="strength_roll = strength_needed"),
             fails_at=0, message_contains="=="),
        dict(why="the needed number typed in the if", code=_latch(test="strength_roll >= 12"),
             fails_at=1, message_contains="not a number you typed"),
        dict(why="the comparison worked out by hand (typed True)", code=_latch(test="True"),
             fails_at=1, message_contains="printed the same thing"),
        dict(why="== instead of >= (only exactly 12 passes)", code=_latch(test="strength_roll == strength_needed"),
             fails_at=1, message_contains="exactly"),
        dict(why="the ___ placeholders left in the quotes", code=_latch(win='"___"', lose='"___"'),
             fails_at=1, message_contains="___"),
        dict(why="no else: nothing prints on a failed roll", code=(
            "strength_roll = 14\nstrength_needed = 12\nif strength_roll >= strength_needed:\n"
            "    print(\"The latch pops open.\")\n"), fails_at=1, message_contains="else"),
        dict(why="one below still passes (>= strength_needed - 1)", code=_latch(test="strength_roll >= strength_needed - 1"),
             fails_at=1, message_contains="below"),
        dict(why="no else: the failure line has no indent, so it prints after every roll (it passed before the probe)",
             code=("strength_roll = 14\nstrength_needed = 12\nif strength_roll >= strength_needed:\n"
                   "    print(\"The latch pops open.\")\nprint(\"That latch hates me.\")\n"),
             fails_at=1, message_contains="as well as the success line"),
        dict(why="the reverse: the success line has no indent under an if that asks about failing",
             code=("strength_roll = 14\nstrength_needed = 12\nif strength_roll < strength_needed:\n"
                   "    print(\"That latch hates me.\")\nprint(\"The latch pops open.\")\n"),
             fails_at=1, message_contains="as well as the failure line"),
        dict(why="the comparison typed with the starter's numbers (14 >= 12 is always True)",
             code=_latch(test="14 >= 12"), fails_at=1, message_contains="printed the same thing"),
        dict(why="the failure line uses a box that does not exist (the real roll never reaches it; the check's low roll does)",
             code=_latch(lose='"That latch hates " + bomb_shell'), fails_at=1, message_contains="Mend this slip"),
        dict(why="the starter's box strength_needed deleted and 12 typed in the if (missing starter box)",
             code=_latch(test="strength_roll >= 12").replace("strength_needed = 12\n", ""), fails_at=1,
             message_contains="Keep the box `strength_needed` from the starter"),
        dict(why="the starter's strength_roll line turned into a sum (the check cannot change it: missing starter box)",
             code=_latch().replace("strength_roll = 14", "strength_roll = 10 + 4"), fails_at=1,
             message_contains="Keep the box `strength_roll` from the starter"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="if-else,boundary", solo="false", dictates="",
             foreign_names="spot_roll,spot_needed,coins,price",
             twin="Gearshift lifts the cart: lift_roll vs lift_needed, same BND check") + "\n"
        "Make. BND over strength_needed - 1 / exactly / + 1, a low and a high roll, then strength_needed + 3, all "
        "read from the student's own code (any difficulty passes). Any two different lines pass: the check compares "
        "the lines with every whole number masked and never repeats them. The success line is whichever "
        "line a high roll prints. Lint e (creative values): verified by hand that other line pairs pass. "
        "The example's names (spot_roll) crash with NameError, and explainer rule 3 names the example. A reversed test "
        "(`if strength_roll < strength_needed:` with the lines swapped) is the same program with the two lines the "
        "other way round, so it passes: the check cannot read what the words mean."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-04 clock-colors (elif, first true branch wins)
# ---------------------------------------------------------------------------------------------


def _clock(first=("hours_left <= 2", "red"), second=("hours_left <= 12", "bright blue"), last="calm blue", end="print(clock_color)\n"):
    return (
        "hours_left = 2\n"
        f"if {first[0]}:\n    clock_color = \"{first[1]}\"\n"
        f"elif {second[0]}:\n    clock_color = \"{second[1]}\"\n"
        f"else:\n    clock_color = \"{last}\"\n"
        + end
    )


CLOCK_STARTER = _clock(first=("hours_left <= 12", "bright blue"), second=("hours_left <= 2", "red"))
CLOCK_FIRST_TRUE = ("First true wins. Order the chain: first, the test that lets the fewest numbers through "
                    "(`hours_left <= 2`).")
ORDER_RULE = "first, the test that lets the fewest numbers through"

CLOCK_COLORS = dict(
    id="clock-colors",
    title="Clock colors",
    martu=(
        "[[elif]] means else, if. Python checks the branches from the top and takes the **first** true one. "
        "Then it skips the rest.\n"
        "My Ley Clock glows red when 2 hours or fewer are left, bright blue up to 12 hours, and calm blue after "
        "that. Someone wrote this chain in the wrong order. Which hours get the wrong color?"
    ),
    names=["hours_left", "clock_color"],
    predict=dict(
        q="Before you press Run: what will this print?",
        choices=["bright blue", "red", "calm blue"],
        answer=0,
        explain=(
            "Step by step, with `hours_left = 2`:\n"
            "1. `if hours_left <= 12:` asks: is 2 at most 12? `True`. So `clock_color` gets bright blue.\n"
            "2. The first true branch wins. Python skips the `elif` and the `else`.\n"
            "3. The `red` branch is never even asked. 2 hours should be red."
        ),
    ),
    tracer=True,
    starter=CLOCK_STARTER,
    checkpoints=[
        dict(
            id="reorder-the-chain",
            text="Put the branches in an order where 2 hours gives `\"red\"`.",
            dictated=True,
            hints=[
                "Start like this: `if hours_left `",
                "Which branch does hour 2 reach first? Every hour that is 2 or less is also 12 or less.",
                "First true wins, so the order rule is: " + ORDER_RULE + ".\n```python\nif age <= 5:\n"
                "    ticket = \"free\"\nelif age <= 15:\n    ticket = \"child\"\nelse:\n    ticket = \"adult\"\n```\n"
                "`age <= 5` lets 6 ages through (0 to 5), `age <= 15` lets 16 through, so `<= 5` goes first.",
            ],
            checks=[
                strexact_check(["red", "bright blue", "calm blue"]),
                box_check("each hour gets its color", "clock_color", [
                    ({"hours_left": 2}, None, "red", CLOCK_FIRST_TRUE),
                    ({"hours_left": 1}, None, "red", CLOCK_FIRST_TRUE),
                    ({"hours_left": 3}, None, "bright blue", "Make 3 to 12 hours bright blue, with `hours_left <= 12`."),
                    ({"hours_left": 12}, None, "bright blue", "Make 3 to 12 hours bright blue, with `hours_left <= 12`."),
                    ({"hours_left": 13}, None, "calm blue", "Make more than 12 hours calm blue, with `else:` last."),
                    ({"hours_left": 40}, None, "calm blue", "Make more than 12 hours calm blue, with `else:` last."),
                ], kept=True),
                dead_branch_check("hours_left"),
                one_chain_check("clock_color"),
            ],
            pass_line="Mar'tu: Red at two. Good. I hope we never see it.",
        ),
    ],
    solution=_clock(),
    assemble=dict(
        lines=["hours_left = 2", "if hours_left <= 2:", '    clock_color = "red"', "elif hours_left <= 12:",
               '    clock_color = "bright blue"', "else:", '    clock_color = "calm blue"', "print(clock_color)"],
        distractors=["elif hours_left <= 2:", "else hours_left > 12:"],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="A line of doors",
            text=(
                "Picture a hall of doors. You try them from the front, and you walk through the first one that "
                "opens. A door further back never gets tried."
            ),
        ),
        dict(
            angle="picture",
            label="The chain, top to bottom",
            text=(
                "```text\n<= 2 ?   yes -> red          (stop)\n  no\n<= 12 ?  yes -> bright blue  (stop)\n"
                "  no\nelse         -> calm blue\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            label="Trace 2, 7 and 20",
            text=(
                "In the mended chain:\n"
                "1. 2 hours: `2 <= 2` is True. Red. Stop.\n"
                "2. 7 hours: `7 <= 2` is False. `7 <= 12` is True. Bright blue. Stop.\n"
                "3. 20 hours: both False, so the `else`: calm blue."
            ),
        ),
        dict(angle="shorter", text="First true branch wins. So " + ORDER_RULE + ": `<= 2`, then `<= 12`, then `else`."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky wants a proper reading. Print `Clock: red (2h)`, built from `clock_color` and `hours_left`.",
        hints=[
            "Start like this: `print(\"Clock: \" + `",
            "`clock_color` is already text. `hours_left` is a number, so it needs `str()`.",
        ],
        checks=[
            lines_check("the reading follows the hours", [
                ({"hours_left": 1}, None, ["Clock: red (1h)"], [],
                 "Glue it: `\"Clock: \" + clock_color + \" (\" + str(hours_left) + \"h)\"`."),
                ({"hours_left": 13}, None, ["Clock: calm blue (13h)"], [],
                 "Glue it: `\"Clock: \" + clock_color + \" (\" + str(hours_left) + \"h)\"`."),
            ]),
        ],
        solution=_clock(end='print("Clock: " + clock_color + " (" + str(hours_left) + "h)")\n'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet=(
            'if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:\n    ...\n'
            'elif caster["mana"] < spell["mana_cost"]:\n    ...\nelse:\n    ...'
        ),
        why=(
            "You have seen this chain in `cast_spell`. Python asked about affinity first. Only when that was False "
            "did it ask about mana. Only when both were False did the spell cast. First true branch wins."
        ),
    ),
    takeaway="`elif` = else, if. Python takes the first true branch and skips the rest. So: " + ORDER_RULE + ".",
    wrong_answers=[
        dict(why="the order unchanged", code=CLOCK_STARTER, fails_at=1, message_contains="hours_left = 2"),
        dict(why="the colors swapped instead of the tests",
             code=_clock(first=("hours_left <= 12", "red"), second=("hours_left <= 2", "bright blue")),
             fails_at=1, message_contains="hours_left = 3"),
        dict(why="elif without if (the first line changed to elif)",
             code=_clock().replace("if hours_left <= 2:", "elif hours_left <= 2:", 1), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="else with a question", code=_clock().replace("else:", "else hours_left > 12:"),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the answer typed for this hour (red, whatever the hours)",
             code=CLOCK_STARTER + 'clock_color = "red"\nprint(clock_color)\n', fails_at=1, message_contains="bright blue"),
        dict(why="a capital letter in the color", code=_clock(first=("hours_left <= 2", "Red")),
             fails_at=1, message_contains="capital"),
        dict(why="< instead of <= (2 hours left is not red)", code=_clock(first=("hours_left < 2", "red")),
             fails_at=1, message_contains="hours_left = 2"),
        dict(why="the wrong-order chain kept and patched by a second if after it (right colors; it passed before the probe)",
             code=CLOCK_STARTER.replace("print(clock_color)\n", "")
             + 'if hours_left <= 2:\n    clock_color = "red"\nprint(clock_color)\n',
             fails_at=1, message_contains="old chain still asks"),
        dict(why="three separate ifs instead of one chain (right colors; caught by the one-chain check)",
             code=('hours_left = 2\nif hours_left <= 2:\n    clock_color = "red"\n'
                   'if hours_left > 2 and hours_left <= 12:\n    clock_color = "bright blue"\n'
                   'if hours_left > 12:\n    clock_color = "calm blue"\nprint(clock_color)\n'),
             fails_at=1, message_contains="one chain"),
        dict(why="the starter's hours_left line turned into a sum (the check cannot change it: missing starter box)",
             code=_clock().replace("hours_left = 2", "hours_left = 1 + 1"), fails_at=1,
             message_contains="Keep the box `hours_left` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="elif-chain", solo="false", dictates="1", foreign_names="age,ticket",
             stages="P,I,M", trace="static step table (predict explain, another_way)") + "\n"
        "Investigate (which hours get the wrong color? 2 gives bright blue) is the Learn text's question and the "
        "predict explanation. CMB at 2, 1, 3, 12, 13, 40 on the box clock_color (not the printed line), so moving "
        "the print is fine. Other right chains pass too (probed): `< 3` for red, a top-down chain (`> 12` calm blue, "
        "`> 2` bright blue, else red), `2 < hours_left <= 12`. The one right-colors program that fails: the "
        "wrong-order chain kept as it is, with a second `if hours_left <= 2:` after it that repaints red. Its "
        "`<= 2` branch can never run, which is the lesson, so dead_branch_check names it (after the CMB check, "
        "so it only speaks when the colors are already right). one_chain_check then asks for ONE chain (teacher's "
        "ruling): three separate `if`s with right colors fail with 'Make it one chain'; a default `clock_color = ...` "
        "line before one chain passes. Order rule wording everywhere: 'first, the test that lets the fewest numbers "
        "through'."
    ),
)


# ---------------------------------------------------------------------------------------------
# 2B-05 four-answers (rehearsal of program-dialogue-options; CALL recorders in setup)
# ---------------------------------------------------------------------------------------------

# CALL recorders. Each record keeps the line number of the student's call, so a check can tell WHICH branch spoke,
# even when two branches say the same words. `light_up_option` (not "box": in this course a box is a variable)
# stands in for the campaign's `make_option_green`.
DIALOGUE_SETUP = (
    "_said = []\n"
    "def mar_tu_says(text):\n"
    "    _said.append(('says', text, __import__('sys')._getframe(1).f_lineno))\n"
    "    print(\"Mar'tu: \" + str(text))\n"
    "def light_up_option():\n"
    "    _said.append(('lit', '', __import__('sys')._getframe(1).f_lineno))\n"
    "    print('[ the option lights up ]')\n"
)

REPLIES = [
    "Then we leave at dawn.",
    "The decay? The clock is speeding up.",
    "It turned red once. Never again, I hope.",
    "Rest, yes. One hour.",
]
OPTIONS = ["option 1", "option 2", "option 3", "option 4"]

# Branch k is the k-th `mar_tu_says("...")` line in the file, and option k must make THAT line speak (by line
# number, so two branches with the same words still count as two branches).
_DIALOGUE = r"""
_order = sorted([_c for _c in _ast.walk(_ast.parse(_source)) if type(_c).__name__ == 'Call'
                 and type(_c.func).__name__ == 'Name' and _c.func.id == 'mar_tu_says' and _c.args
                 and type(_c.args[0]).__name__ == 'Constant'], key=lambda _c: (_c.lineno, _c.col_offset))
_order = [_c.lineno for _c in _order]
assert _order, ("Keep one `mar_tu_says(\"...\")` line in each branch, with its words in quotes, so Mar'tu's check can "
                'tell the four replies apart.')
for _k in (1, 2, 3, 4):
    _c = 'option ' + str(_k)
    _vals = {'choice': _c}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    assert not _miss, _keep(_miss[0])
    assert not (_err and "'___'" in _err), _mend('Replace each `___` with an option in quotes, like `"option 1"`.',
                                                 'Python reached a `___` that is still there.', _vals, [])
    assert not _err, _stop(_vals, [], _err)
    _says = [_e for _e in _ns.get('_said', []) if _e[0] == 'says']
    _want = _order[_k - 1] if len(_order) >= _k else None
    assert _says, _mend('Write the branch for it as `choice == "' + _c + '"`, with the quotes and the space.',
                        "Mar'tu said nothing.", _vals, [])
    _j = _order.index(_says[0][2]) + 1 if _says[0][2] in _order else 0
    assert _says[0][2] == _want, (_mend('Put the options in order: `"option 1"` in the first branch, then 2, 3 and 4.',
                                        "Mar'tu said the line for option " + str(_j) + '.', _vals, []) if _j else
                                  _mend('Make branch ' + str(_k) + ' the one that speaks for `"' + _c + '"`.',
                                        "Mar'tu said another line.", _vals, []))
    assert len(_says) == 1, _mend('Give each branch one `mar_tu_says` line: one branch runs, so one line.',
                                  "Mar'tu spoke " + str(len(_says)) + ' times.', _vals, [])
"""

_LIT = r"""
for _c, _n in (('option 1', 1), ('option 2', 1), ('option 3', 1), ('option 4', 1), ('option 5', 0)):
    _vals = {'choice': _c}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [], _err)
    _lit = len([_e for _e in _ns.get('_said', []) if _e[0] == 'lit'])
    assert not (_n and not _lit), _mend('Add `light_up_option()` under each `mar_tu_says` line, indented the same.',
                                        'No option lit up.', _vals, [])
    assert not (_n and _lit > 1), _mend('Give each branch one `light_up_option()`.',
                                        'The option lit ' + str(_lit) + ' times.', _vals, [])
    assert not (not _n and _lit), _mend('Indent each `light_up_option()` under its `mar_tu_says` line, so it belongs to '
                                        'that branch.', 'No option matched, but one still lit.', _vals, [])
"""


def dialogue_check(label="each choice says its own line"):
    return (label, _rerun_code(DIALOGUE_SETUP) + _DIALOGUE)


def options_lit_check(label="the clicked option lights once"):
    return (label, _rerun_code(DIALOGUE_SETUP) + _LIT)


def _dialogue(options=("\"option 1\"", "\"option 2\"", "\"option 3\"", "\"option 4\""), lights=(True, True, True, True),
              comments=True, tail="", choice="option 3", heads=("if", "elif", "elif", "elif"), cmp="=="):
    out = f'choice = "{choice}"  # the option the player clicked\n'
    if comments:
        out += (
            '# 1. Replace each ___ with "option 1", "option 2", "option 3" or "option 4" (keep the quotes), in order.\n'
            "# 2. Add light_up_option() under each mar_tu_says line.\n"
        )
    for head, option, reply, light in zip(heads, options, REPLIES, lights):
        out += f"{head} choice {cmp} {option}:\n    mar_tu_says(\"{reply}\")\n"
        if light:
            out += "    light_up_option()\n"
    return out + tail


FOUR_STARTER = _dialogue(options=("___",) * 4, lights=(False,) * 4)
FOUR_SOLUTION = _dialogue()
FOUR_PARTIAL = _dialogue(lights=(False,) * 4)

FOUR_ANSWERS = dict(
    id="four-answers",
    title="Four answers",
    martu=(
        "Remember the four dialogue options? This is that chain. `choice` holds the option the player clicked. Each "
        "[[branch]] asks about one option, from the top, and the first true one speaks.\n"
        "Follow the numbered comments, one per step. The options are text, so they keep their quotes: "
        "`\"option 1\"`, with the space."
    ),
    setup=DIALOGUE_SETUP,
    names=["choice", "mar_tu_says", "light_up_option"],
    starter=FOUR_STARTER,
    checkpoints=[
        dict(
            id="fill-the-options",
            text=(
                "Replace each `___` with `\"option 1\"`, `\"option 2\"`, `\"option 3\"` or `\"option 4\"` (keep the "
                "quotes), in order."
            ),
            dictated=True,
            hints=[
                "Start like this: `if choice == `",
                "Which part must keep its quotes? The option is text, so it is `\"option 1\"`, quotes and all.",
                QUOTES_RULE + " `choice == \"option 2\"` asks: is the text in `choice` the same as these exact letters?",
                "The first two branches (`...` is Mar'tu's line, already in the starter):\n```python\n"
                "if choice == \"option 1\":\n    mar_tu_says(...)\nelif choice == \"option 2\":\n```",
            ],
            checks=[strexact_check(OPTIONS), dialogue_check()],
            pass_line="Mar'tu: Four answers, four branches. Yes. That is the chain.",
        ),
        dict(
            id="light-each-option",
            text="Add `light_up_option()` under each `mar_tu_says` line, so the clicked option lights up.",
            dictated=True,
            hints=[
                "Start like this: under the first `mar_tu_says` line, type four spaces, then `light_up_`",
                "Four branches, so four `light_up_option()` lines, each indented under its own `mar_tu_says` line.",
                "Indented lines belong to their branch. A line with no indent runs for every choice, even one that "
                "matched nothing.",
            ],
            checks=[options_lit_check()],
            pass_line="Lucky: Ooh, shiny. Fine. But I'm keeping track.",
        ),
    ],
    solution=FOUR_SOLUTION,
    partials=[FOUR_PARTIAL],
    assemble=dict(
        lines=[line for line in FOUR_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["elif choice == option 2:", 'elif choice = "option 3":', "light_up_option()"],
    ),
    another_way=[
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In Module 1, the game showed four options. When a player clicked one, `user.clicked()` gave its "
                "option, and a chain like this one picked the reply. Here `choice` plays the click."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Trace option 3",
            text=(
                "With `choice = \"option 3\"`:\n"
                "1. Is it the same as `\"option 1\"`? No. Skip.\n"
                "2. `\"option 2\"`? No. Skip.\n"
                "3. `\"option 3\"`? Yes. Mar'tu speaks, the option lights up.\n"
                "4. The rest of the chain is skipped."
            ),
        ),
        dict(
            angle="picture",
            label="Four options on a board",
            text=(
                "```text\n[ option 1 ] [ option 2 ]\n[ option 3 ] [ option 4 ]\n```\n"
                "One click, one branch. Each branch has its own reply and its own light."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky clicks things that aren't there. Add an `else:` at the end that makes Mar'tu say `Hm.` for any "
            "other choice. No option to light: nothing was clicked."
        ),
        hints=["Start like this: `else:` at the end of the chain.",
               "`else:` has no question and no option. It is always last."],
        checks=[
            (
                "any other choice gets Hm.",
                _rerun_code(DIALOGUE_SETUP) +
                "_ns, _rows, _calls, _err, _miss = _rerun({'choice': 'a grumpy moth'}, [])\n"
                "assert not _err, _stop({'choice': 'a grumpy moth'}, [], _err)\n"
                "_says = [_e[1] for _e in _ns.get('_said', []) if _e[0] == 'says']\n"
                "assert _says == ['Hm.'], _mend('Add `else:` at the end, with `mar_tu_says(\"Hm.\")` under it.', "
                "'Mar' + chr(39) + 'tu did not say `Hm.`.', {'choice': 'a grumpy moth'}, [])\n",
            ),
        ],
        solution=_dialogue(tail='else:\n    mar_tu_says("Hm.")\n'),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='if (user.clicked() == <option>):\n    speak_dialogue("option 1")',
        why=(
            "You have seen this. The four dialogue options were this chain, on `user.clicked()`. Each `<option>` "
            "became `\"option 1\"` and so on, in quotes, and `make_option_green()` went under each reply. Now you "
            "know why the quotes and the order mattered."
        ),
    ),
    takeaway="A chain of `if` / `elif` picks one reply. Options are text, so they keep their quotes: `\"option 1\"`.",
    wrong_answers=[
        dict(why="the starter (blanks left)", code=FOUR_STARTER, fails_at=0, message_contains="___"),
        dict(why="unquoted options (verified SyntaxError)",
             code=_dialogue(options=("\"option 1\"", "option 2", "\"option 3\"", "\"option 4\"")),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="= instead of == in an elif",
             code=_dialogue().replace('elif choice == "option 3":', 'elif choice = "option 3":'),
             fails_at=0, message_contains="=="),
        dict(why="a capital O (STREXACT)", code=_dialogue(options=("\"Option 1\"", "\"option 2\"", "\"option 3\"", "\"option 4\"")),
             fails_at=1, message_contains="capital"),
        dict(why="no space in the option (STREXACT)",
             code=_dialogue(options=("\"option 1\"", "\"option2\"", "\"option 3\"", "\"option 4\"")),
             fails_at=1, message_contains="space"),
        dict(why="the options out of order",
             code=_dialogue(options=("\"option 2\"", "\"option 1\"", "\"option 3\"", "\"option 4\"")),
             fails_at=1, message_contains="in order"),
        dict(why="only some blanks filled (option 3 is clicked, so it runs until a check tries option 4)",
             code=_dialogue(options=("\"option 1\"", "\"option 2\"", "\"option 3\"", "___")),
             fails_at=1, message_contains="option 4"),
        dict(why="elif without if (the chain starts with elif)",
             code=_dialogue(heads=("elif", "elif", "elif", "elif")), fails_at=0, message_contains="invalid syntax"),
        dict(why="light_up_option() missing under option 3", code=_dialogue(lights=(True, True, False, True)),
             fails_at=2, message_contains="option 3"),
        dict(why="light_up_option() only under the first branch", code=_dialogue(lights=(True, False, False, False)),
             fails_at=2, message_contains="option 2"),
        dict(why="one unindented light_up_option() at the end (lights for every choice)",
             code=_dialogue(lights=(False,) * 4, tail="light_up_option()\n"), fails_at=2, message_contains="option 5"),
        dict(why="every reply changed to the same words, then the options swapped (passed before the probe: the check "
                 "matched replies by their words)",
             code=_dialogue(options=("\"option 2\"", "\"option 1\"", "\"option 3\"", "\"option 4\"")).replace(
                 'mar_tu_says("Then we leave at dawn.")', 'mar_tu_says("Hm.")').replace(
                 'mar_tu_says("The decay? The clock is speeding up.")', 'mar_tu_says("Hm.")'),
             fails_at=1, message_contains="in order"),
        dict(why="the replies moved into a box with one mar_tu_says(reply) at the end",
             code=('choice = "option 3"\n' + "".join(
                 f'{"if" if i == 0 else "elif"} choice == "{o}":\n    reply = "{r}"\n' for i, (o, r) in enumerate(zip(OPTIONS, REPLIES)))
                 + "mar_tu_says(reply)\nlight_up_option()\n"),
             fails_at=1, message_contains="Keep one `mar_tu_says"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="elif-chain,quote-text", solo="false", dictates="1,2",
             foreign_names="", rehearsal="program-dialogue-options") + "\n"
        "A-stage rehearsal: Assemble-first under Show me more (the assemble lines are the whole program, starter "
        "comments dropped), typed starter under Keep it short. Numbered comments map 1:1 onto the checkpoints, and "
        "the checkpoint text copies the campaign's phrasing (rule 13). engine=False: `mar_tu_says` and "
        "`light_up_option` are CALL recorders in setup, standing in for `speak_dialogue` and `make_option_green` "
        "(renamed by the teacher's ruling, so 'box' keeps meaning a variable). "
        "The check reruns with each option (and `\"option 5\"`, which must light nothing). Option k must make the "
        "k-th `mar_tu_says(\"...\")` line speak, matched by LINE NUMBER (the setup recorders keep the caller's line), "
        "so changing a reply's words passes, and two branches with the same words still count as two branches "
        "(the old word-matching let swapped options pass when the replies matched). Separate `if`s, reversed "
        "operands (`\"option 1\" == choice`), `choice.lower() ==`, `light_up_option()` above the reply and the bonus "
        "`else` all pass (probed). The starter "
        "clicks option 3, so the first run stops at the first `___` (explainer rule 1)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-06 and-or-not
# ---------------------------------------------------------------------------------------------


def _logic(can="False", lucky="False", danger=None, extra=""):
    out = (
        "# Oogrish casts Lantern Ward. It costs 9 mana and needs affinity 9.\n"
        "mana = 12\ncost = 9\naffinity = 9\nrequired = 9\n"
        f"can_cast = {can}\n\n"
        "# Lucky's skill check. He may roll twice.\n"
        "needed = 15\nfirst_roll = 11\nsecond_roll = 17\n"
        f"{extra}"
        f"lucky_passes = {lucky}\n\n"
        "barrier_up = True\n"
    )
    if danger:
        out += f"in_danger = {danger}\n"
    out += "\nprint(can_cast)\nprint(lucky_passes)\n"
    if danger:
        out += "print(in_danger)\n"
    return out


CAN_CAST = "mana >= cost and affinity >= required"
LUCKY_PASSES = "first_roll >= needed or second_roll >= needed"
SPELL = {"cost": 9, "required": 9}
ROLLS = {"needed": 15}

AND_OR_NOT = dict(
    id="and-or-not",
    title="And, or, not",
    martu=(
        "Three small words join questions.\n"
        "[[and]]: both must be `True`. To cast, Oogrish needs enough mana and enough affinity.\n"
        "[[or]]: one is enough. Lucky passes if his first roll or his second roll is high enough.\n"
        "[[not]]: flips the answer. `not True` is `False`."
    ),
    introduces=["op:And", "op:Or", "op:Not"],
    names=["can_cast", "lucky_passes", "in_danger", "barrier_up"],
    predict=dict(
        q="Before you run it: what will these three lines print?",
        code="print(12 >= 9 and 9 >= 9)\nprint(11 >= 15 or 17 >= 15)\nprint(not True)\n",
        choices=["True\nTrue\nFalse", "True\nFalse\nFalse", "False\nTrue\nTrue"],
        answer=0,
        explain=(
            "1. `12 >= 9` is True and `9 >= 9` is True. Both, so `and` gives True.\n"
            "2. `11 >= 15` is False, but `17 >= 15` is True. One is enough for `or`: True.\n"
            "3. `not` flips True to False."
        ),
    ),
    starter=_logic(),
    checkpoints=[
        dict(
            id="both-needed",
            text="Make `can_cast` say whether `mana >= cost and affinity >= required`.",
            dictated=True,
            hints=[
                "Start like this: `can_cast = mana `",
                "Two questions: enough mana? enough affinity? Oogrish needs both.",
                "`and` is True only when both sides are True:\n```python\nhas_key = True\ndoor_unlocked = False\n"
                "print(has_key and door_unlocked)\n```\nThat prints False: one side is False.",
            ],
            checks=[
                from_boxes_check("can_cast", ["mana", "cost", "affinity", "required"],
                                 "Write `can_cast = mana >= cost and affinity >= required`.", placeholder=False),
                box_check("can_cast needs both", "can_cast", [
                    (dict(SPELL, mana=12, affinity=9), None, True,
                     "Use `>=`, so exactly enough counts: 12 mana covers 9, and affinity 9 reaches 9."),
                    (dict(SPELL, mana=5, affinity=9), None, False,
                     "Use `and`, which needs both sides `True`: 5 mana is too little."),
                    (dict(SPELL, mana=12, affinity=8), None, False, "Ask about both with `and`: affinity 8 is too low for 9."),
                    (dict(SPELL, mana=9, affinity=9), None, True, "Use `>=`: exactly enough mana and affinity still cast."),
                ], show=["mana", "affinity"], kept=True),
            ],
            pass_line="Oogrish: Steady, now. The ward holds.",
        ),
        dict(
            id="either-roll",
            text="Lucky may roll twice. Make `lucky_passes` say whether at least one of his rolls reaches `needed`.",
            dictated=False,
            hints=[
                "Start like this: `lucky_passes = first_roll `",
                "Lucky needs just one good roll. Ask about `first_roll` and about `second_roll`. Which word means one "
                "is enough?",
                "`or` is True when at least one side is True:\n```python\nprint(False or True)\n```\nThat prints True.",
                "Each side is a whole question, like `can_cast` had: `first_roll >= needed` on one side, the same for "
                "`second_roll` on the other.",
            ],
            checks=[
                from_boxes_check("lucky_passes", ["first_roll", "second_roll", "needed"],
                                 "Ask with `>=`, about `first_roll`, `second_roll` and `needed`.", placeholder=False),
                box_check("lucky_passes needs one", "lucky_passes", [
                    (dict(ROLLS, first_roll=11, second_roll=17), None, True,
                     "Use `or`: one roll reaching `needed` is enough. `and` would need both."),
                    (dict(ROLLS, first_roll=16, second_roll=3), None, True, "Let the first roll count on its own: 16 is enough."),
                    (dict(ROLLS, first_roll=4, second_roll=9), None, False,
                     "Compare both rolls with `needed`: neither 4 nor 9 reaches 15."),
                    (dict(ROLLS, first_roll=15, second_roll=2), None, True, "Use `>=`: exactly 15 reaches 15."),
                ], show=["first_roll", "second_roll"], kept=True),
            ],
        ),
        dict(
            id="not-up",
            text="Make `in_danger` say whether the barrier is down. Use `not`.",
            dictated=False,
            hints=[
                "Start like this: `in_danger = `",
                "Which box says whether the barrier is up? You want the opposite of it.",
                "`not` flips a True or False:\n```python\nlamp_on = True\nprint(not lamp_on)\n```\nThat prints False.",
            ],
            checks=[
                name_check("in_danger", foreign=["lamp_on", "has_key", "door_unlocked"],
                           skip=["mana", "cost", "affinity", "required", "can_cast", "needed", "first_roll",
                                 "second_roll", "lucky_passes", "barrier_up"]),
                from_boxes_check("in_danger", ["barrier_up"], "Flip the barrier's answer with `not`.", typed=False,
                                 label="in_danger has one ="),
                box_check("in_danger flips barrier_up", "in_danger", [
                    ({"barrier_up": False}, None, True, "Build it from `barrier_up`: with the barrier down, we are in danger."),
                    ({"barrier_up": True}, None, False, "Build it from `barrier_up`: with the barrier up, we are safe."),
                ]),
                (
                    "uses not",
                    # `not` inside the in_danger line itself (a `not` elsewhere, say in can_cast, does not count)
                    "import ast as _ast\n"
                    "_flip = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' and any("
                    "type(_t).__name__ == 'Name' and _t.id == 'in_danger' for _t in _n.targets) and any("
                    "type(_x).__name__ == 'Not' for _x in _ast.walk(_n.value))]\n"
                    "assert _flip, 'Right answer. Now say it with `not`: `not barrier_up` flips True to False.'\n",
                ),
            ],
            pass_line="Gearshift: Barrier's holding.",
        ),
    ],
    solution=_logic(can=CAN_CAST, lucky=LUCKY_PASSES, danger="not barrier_up"),
    partials=[_logic(can=CAN_CAST), _logic(can=CAN_CAST, lucky=LUCKY_PASSES)],
    assemble=dict(
        lines=["mana = 12", "cost = 9", "affinity = 9", "required = 9", f"can_cast = {CAN_CAST}", "needed = 15",
               "first_roll = 11", "second_roll = 17", f"lucky_passes = {LUCKY_PASSES}", "barrier_up = True",
               "in_danger = not barrier_up", "print(can_cast)", "print(lucky_passes)", "print(in_danger)"],
        distractors=["can_cast = mana >= cost or affinity >= required", "in_danger = barrier_up"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="A truth table with the real stats",
            text=(
                "Oogrish: mana 12, cost 9, affinity 9, needs 9.\n"
                "1. `mana >= cost`: 12 >= 9, True.\n"
                "2. `affinity >= required`: 9 >= 9, True.\n"
                "3. True `and` True: True. He casts.\n"
                "With only 5 mana: False `and` True is False. With `or`, it would be True, and he would cast with "
                "no mana. Bad."
            ),
        ),
        dict(
            angle="everyday",
            label="Keys",
            text="`and` is a door with two locks: you need both keys. `or` is two doors: either key gets you in.",
        ),
        dict(
            angle="picture",
            label="Two lamps",
            text=(
                "```text\nand: [on]  [on]  -> on\nand: [on]  [off] -> off\n"
                "or:  [on]  [off] -> on\nor:  [off] [off] -> off\nnot: [on]        -> off\n```"
            ),
        ),
        dict(angle="shorter", text="`and` needs both. `or` needs one. `not` flips."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky's second roll is his Dumb Luck: it only counts if he hasn't used it today. Make a box "
            "`dumb_luck = True`. Then change `lucky_passes` so the second roll counts only when `dumb_luck` is True."
        ),
        hints=[
            "Start like this: `lucky_passes = first_roll `",
            "The first roll always counts. The second needs two things at once: `dumb_luck` and a high roll.",
        ],
        checks=[
            name_check("dumb_luck", skip=["mana", "cost", "affinity", "required", "can_cast", "needed", "first_roll",
                                          "second_roll", "lucky_passes", "barrier_up", "in_danger"]),
            box_check("the second roll needs Dumb Luck", "lucky_passes", [
                (dict(ROLLS, first_roll=11, second_roll=17, dumb_luck=False), None, False,
                 "Count the second roll only with `dumb_luck and`: here Dumb Luck is used up."),
                (dict(ROLLS, first_roll=11, second_roll=17, dumb_luck=True), None, True,
                 "Let the second roll count when `dumb_luck` is True: here it is ready."),
                (dict(ROLLS, first_roll=16, second_roll=3, dumb_luck=False), None, True,
                 "Let the first roll always count, Dumb Luck or not: keep `first_roll >= needed or`."),
            ], show=["first_roll", "second_roll", "dumb_luck"]),
        ],
        solution=_logic(can=CAN_CAST, lucky="first_roll >= needed or (dumb_luck and second_roll >= needed)",
                        danger="not barrier_up", extra="dumb_luck = True\n"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "You have seen both questions in `cast_spell`: enough affinity? enough mana? The campaign asked them "
            "one at a time with `if` and `elif`. `and` asks both in one line."
        ),
    ),
    takeaway="`and` needs both. `or` needs one. `not` flips True and False.",
    wrong_answers=[
        dict(why="or instead of and (casts with 5 mana)", code=_logic(can="mana >= cost or affinity >= required"),
             fails_at=1, message_contains="mana = 5"),
        dict(why="the answer typed (True)", code=_logic(can="True"), fails_at=1, message_contains="values you typed"),
        dict(why="the comparison typed with numbers worked out by hand (12 >= 9 and 9 >= 9: it can never change)",
             code=_logic(can="12 >= 9 and 9 >= 9"), fails_at=1, message_contains="values you typed"),
        dict(why="= for >= makes a second assignment (can_cast = mana = cost and ...: puts a value in mana too)",
             code=_logic(can="mana = cost and affinity >= required"), fails_at=1, message_contains="two `=` signs"),
        dict(why="lucky_passes typed with the rolls worked out by hand",
             code=_logic(can=CAN_CAST, lucky="11 >= 15 or 17 >= 15"), fails_at=2, message_contains="values you typed"),
        dict(why="in_danger = barrier_up = False (= for ==: both boxes get False)",
             code=_logic(can=CAN_CAST, lucky=LUCKY_PASSES, danger="barrier_up = False"), fails_at=3,
             message_contains="two `=` signs"),
        dict(why="not used somewhere else, but in_danger still asks with == False",
             code=_logic(can="not (mana < cost or affinity < required)", lucky=LUCKY_PASSES, danger="barrier_up == False"),
             fails_at=3, message_contains="say it with `not`"),
        dict(why="> instead of >= (exactly enough fails)", code=_logic(can="mana > cost and affinity > required"),
             fails_at=1, message_contains="exactly enough counts"),
        dict(why="True in quotes", code=_logic(can='"True"'), fails_at=1, message_contains="quotes"),
        dict(why="and instead of or (both rolls needed)", code=_logic(can=CAN_CAST, lucky="first_roll >= needed and second_roll >= needed"),
             fails_at=2, message_contains="Use `or`"),
        dict(why="only the first roll checked", code=_logic(can=CAN_CAST, lucky="first_roll >= needed"),
             fails_at=2, message_contains="first_roll = 11"),
        dict(why="in_danger copies barrier_up (no not)", code=_logic(can=CAN_CAST, lucky=LUCKY_PASSES, danger="barrier_up"),
             fails_at=3, message_contains="barrier_up = False"),
        dict(why="in_danger typed (False)", code=_logic(can=CAN_CAST, lucky=LUCKY_PASSES, danger="False"),
             fails_at=3, message_contains="barrier_up = False"),
        dict(why="== False instead of not", code=_logic(can=CAN_CAST, lucky=LUCKY_PASSES, danger="barrier_up == False"),
             fails_at=3, message_contains="not"),
        dict(why="a plural name", code=_logic(can=CAN_CAST, lucky=LUCKY_PASSES).replace(
            "barrier_up = True\n", "barrier_up = True\nin_dangers = not barrier_up\n"), fails_at=3,
             message_contains="letter for letter"),
        dict(why="the starter (can_cast still holds the starter's placeholder False, not typed by the student)",
             code=_logic(), fails_at=1, message_contains="still holds the starter's `False`"),
        dict(why="CP1 done, lucky_passes still the starter's placeholder False", code=_logic(can=CAN_CAST), fails_at=2,
             message_contains="still holds the starter's `False`"),
        dict(why="lucky_passes asks about one roll only, twice (or with the same roll on both sides)",
             code=_logic(can=CAN_CAST, lucky="first_roll >= needed or first_roll >= needed"), fails_at=2,
             message_contains="first_roll = 11"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="and-or-not", solo="false", dictates="1",
             foreign_names="has_key,door_unlocked,lamp_on", stages="P,I,M") + "\n"
        "Three checkpoints [D, ND, ND] (either-roll is goal-only since the teacher's ruling: it names the boxes and "
        "the goal, not the line), each CMB on the box (not the printed line). Every rerun sets all four "
        "values of its question, so a student's own numbers never change the expected answer. The not-step "
        "accepts only `not` in the in_danger line (the lesson's point), with a kind 'Right answer' message for "
        "`== False`. Before CMB, from_boxes_check names two slips the CMB tail misread (check-breaker probe): a "
        "value typed in (`True`, or `12 >= 9 and 9 >= 9` worked out by hand) used to get '`or` would let it "
        "through', and a two-`=` line (`can_cast = mana = cost and ...`, `in_danger = barrier_up = False`) used to "
        "get a mana or barrier message. An `if`/`else` that sets True and False from a test on the boxes counts as "
        "asking. The starter's `False` placeholders get 'still holds the starter's `False`', not 'values you typed'. "
        "Reversed operands, swapped halves and `not (mana < cost or affinity < required)` pass (probed)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-07 roll-a-die
# ---------------------------------------------------------------------------------------------


def _dice(staff="random.randint(1, 6)", sword="random.randint(1, 8)", end="print(staff_roll)\nprint(sword_roll)\n"):
    return (
        "import random\n"
        f"staff_roll = {staff}  # the Staff of Wisdom is a d6\n"
        f"sword_roll = {sword}  # the longsword is a d8\n"
        + end
    )


DICE_STARTER = _dice(staff="random.randint(1, 1)", sword="0")

ROLL_A_DIE = dict(
    id="roll-a-die",
    title="Roll a die",
    martu=(
        "The world is not fair, so we roll. [[import]] `random` lends you Python's dice.\n"
        "`random.[[randint]](1, 6)` gives a whole number from 1 to 6, **both ends included**. So 1 can come up, "
        "and 6 can come up. 0 and 7 never do.\n"
        "Run the starter a few times. Then fix the two dice."
    ),
    introduces=["node:Import", "import:random", "attr:randint"],
    example="import random\npebble = random.randint(1, 4)\nprint(pebble <= 4)\n",
    example_output="True",
    names=["staff_roll", "sword_roll"],
    predict=dict(
        q="This rolls a d6. What does the last line print, every time?",
        code="import random\nroll = random.randint(1, 6)\nprint(roll >= 1 and roll <= 6)\n",
        choices=["True", "False", "Sometimes True, sometimes False"],
        answer=0,
        explain=(
            "`random.randint(1, 6)` only ever gives 1, 2, 3, 4, 5 or 6. Both ends are in. So the roll is always "
            "at least 1 and at most 6, and the line always prints True. Run the starter several times: a 6 turns "
            "up sooner or later. A 0, never."
        ),
    ),
    starter=DICE_STARTER,
    checkpoints=[
        dict(
            id="staff-d6",
            text="Make `staff_roll` a d6 roll: `random.randint(1, 6)`.",
            dictated=True,
            hints=[
                "Start like this: `staff_roll = random.randint(`",
                "Line 2 rolls `random.randint(1, 1)`. A die with one face always lands on 1. Which number is the top face?",
                "`random.randint(1, 4)` gives 1, 2, 3 or 4. The first number is the lowest face, the second is the highest.",
            ],
            checks=[rnd_check("staff_roll is a d6", "staff_roll", 6, [5, 3])],
        ),
        dict(
            id="sword-d8",
            text="Make `sword_roll` a d8 roll.",
            dictated=False,
            hints=[
                "Start like this: `sword_roll = random.randint(`",
                "How many faces does a d8 have? The lowest face is 1.",
                "A d10 would be `random.randint(1, 10)`: lowest face, then highest face.",
            ],
            checks=[rnd_check("sword_roll is a d8", "sword_roll", 8, [5, 3], placeholder=0)],
            pass_line="Lucky: An 8 is still worse than my Telegun. Usually.",
        ),
    ],
    solution=_dice(),
    partials=[_dice(sword="0")],
    assemble=dict(
        lines=["import random", "staff_roll = random.randint(1, 6)", "sword_roll = random.randint(1, 8)",
               "print(staff_roll)", "print(sword_roll)"],
        distractors=["staff_roll = random.randint(0, 6)", "sword_roll = random.randint(1, 7)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The die's faces",
            text="```text\nd6:  [1] [2] [3] [4] [5] [6]\n      ^ low            ^ high\nrandom.randint(1, 6)\n```",
        ),
        dict(
            angle="everyday",
            label="A numbered card",
            text=(
                "Shuffle cards numbered 1 to 8 and draw one. Any card can come up, the 1 and the 8 too. That is "
                "`random.randint(1, 8)`."
            ),
        ),
        dict(
            angle="contrast",
            label="Both ends in",
            text=(
                "Later you will meet `range`, which stops just before its end. `randint` is different: both ends "
                "are in. `random.randint(1, 6)` can give 6."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Roll it",
            text=(
                "1. `import random`, once, at the top.\n"
                "2. `random.randint(lowest, highest)` rolls.\n"
                "3. Put the roll in a box with `=`, so you can use it later."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky swings both. Print the total of the two rolls, built from the boxes.",
        hints=["Start like this: `print(staff_roll `",
               "Both boxes hold numbers, so `+` adds them."],
        checks=[
            (
                "prints the total",
                _rerun_code() +
                "for _rolls in ([5, 3], [2, 7]):\n"
                "    _ns, _rows, _calls, _err, _miss = _rerun({}, _rolls)\n"
                "    assert not _err, _stop({}, _rolls, _err)\n"
                "    _t = _rolls[0] + _rolls[1]\n"
                "    assert any(_re.search(_whole(_t), _l) for _l in _rows), _mend('Add `print(staff_roll + sword_roll)`.', "
                "'Your program did not print the total, ' + str(_t) + '.', {}, _rolls)\n",
            ),
        ],
        solution=_dice(end="print(staff_roll)\nprint(sword_roll)\nprint(staff_roll + sword_roll)\n"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def perform_roll(die_size):\n    return random.randint(1, die_size)",
        why=(
            "You have seen this in `perform_roll`. `random.randint(1, die_size)` rolled whatever die it was handed. "
            "For a d20, that is `random.randint(1, 20)`: 1 and 20 can both come up."
        ),
    ),
    takeaway="`import random` once, then `random.randint(1, 6)` rolls a d6. Both ends are included.",
    wrong_answers=[
        dict(why="the top face left out (randint thought to exclude its end)", code=_dice(staff="random.randint(1, 5)"),
             fails_at=1, message_contains="both ends"),
        dict(why="starting at 0", code=_dice(staff="random.randint(0, 6)"), fails_at=1, message_contains="can give 0"),
        dict(why="d8 starting at 0", code=_dice(sword="random.randint(0, 8)"), fails_at=2, message_contains="can give 0"),
        dict(why="d8 top face left out", code=_dice(sword="random.randint(1, 7)"), fails_at=2, message_contains="never gives 8"),
        dict(why="a roll typed by hand", code=_dice(sword="8"), fails_at=2, message_contains="typed"),
        dict(why="no import random", code=_dice().replace("import random\n", ""), fails_at=0,
             message_contains="import 'random'"),
        dict(why="randint without random. in front", code=_dice(staff="randint(1, 6)"), fails_at=0,
             message_contains="randint"),
        dict(why="the starter (the one-faced die rolls only 1)", code=DICE_STARTER, fails_at=1, message_contains="never gives 6"),
        dict(why="CP1 done, sword_roll still the starter's placeholder 0 (not typed by the student)",
             code=_dice(sword="0"), fails_at=2, message_contains="still holds the starter's `0`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="randint", solo="false", dictates="1", foreign_names="pebble,roll",
             stages="P,R,I,M") + "\n"
        "RND: the check rolls a scripted die (5, then 3) and traces each box back to its own `randint` call and its "
        "arguments. The real die is put back afterwards. Predict is deterministic (the roll is always 1 to 6), so "
        "no random value is ever printed in an example_output (rule 9). WA evidence: the top-excluded belief."
    ),
)


# ---------------------------------------------------------------------------------------------
# 2B-08 roll-and-decide (skeleton: randint + BND + str)
# ---------------------------------------------------------------------------------------------

DECIDE_WIN = '"Bomb Shell tries to " + action + ". Rolled " + str(roll) + ": it opens."'
DECIDE_LOSE = '"Bomb Shell tries to " + action + ". Rolled " + str(roll) + ": it holds."'


def _decide(roll="random.randint(1, 20)", test="roll >= needed", win=DECIDE_WIN, lose=DECIDE_LOSE, needed=12,
            action="pry the trap door open", comments=False, extra_else=""):
    c = (lambda text: "  # " + text) if comments else (lambda text: "")
    return (
        "import random\n"
        f'action = "{action}"\n'
        f"needed = {needed}\n"
        f"roll = {roll}{c('1. roll a d20')}\n"
        f"if {test}:{c('2. does roll reach needed?')}\n"
        f"    print({win}){c('success line, with the roll')}\n"
        "else:\n"
        f"    print({lose}){c('failure line, with the roll')}\n"
        + extra_else
    )


DECIDE_STARTER = _decide(roll="___", test="___", win='"___"', lose='"___"', comments=True)

# Any later randint call gets a different number (_o), so a line that rolls again instead of gluing in `roll` shows
# the wrong number. The roll must sit in a line with words, not on a line by itself (`print(roll)`).
_SHOWS_ROLL = r"""
_N = globals().get('needed', 12)
for _r in [_x for _x in (3, 17, 4, 18) if _x != _N][:2]:
    _o = [_x for _x in (11, 9, 13, 5) if _x not in (_r, _N)][0]
    _ns, _rows, _calls, _err, _miss = _rerun({}, [_r, _o])
    assert not _err, _stop({}, [_r], _err)
    _box = _ns.get('roll', _r)
    _with = [_l for _l in _rows if _re.search(_whole(_box), _l)]
    _fresh = [_l for _l in _rows if _re.search(_whole(_o), _l)] if _box != _o else []
    assert _with or not _fresh, _mend('Glue in `str(roll)`, the roll the `if` asked about.',
                                      'Your line shows a new roll, not the one in `roll`.', {}, [_r])
    assert _with, _mend('Glue the roll into both lines with `str(roll)`.',
                        'Your line did not show the roll, ' + str(_r) + '.', {}, [_r])
    assert [_l for _l in _with if _re.sub(r'[\d\s]', '', _l)], _mend('Glue the roll into the words: '
        '`"Rolled " + str(roll) + ": it opens."`.', 'It printed the roll on a line by itself.', {}, [_r])
"""

ROLL_AND_DECIDE = dict(
    id="roll-and-decide",
    title="Roll and decide",
    martu=(
        "Now the whole skill check, like at the trap door: roll a d20, compare it with what you need, and say "
        "what happened.\n"
        "Pick any action and any `needed` from 2 to 20. Mar'tu's check rolls the die for you, so it can try "
        "every kind of roll."
    ),
    names=["roll", "needed", "action"],
    pick="slide a shim under the latch",
    starter=DECIDE_STARTER,
    checkpoints=[
        dict(
            id="roll-a-d20",
            text="Roll a d20 into `roll`.",
            dictated=True,
            hints=[
                "Start like this: `roll = random.randint(`",
                "Look at line 4. A d20 has faces 1 to 20, and `randint` includes both ends.",
                "`random.randint(1, 4)` rolls a d4. Lowest face first, then the highest.",
            ],
            checks=[rnd_check("roll is a d20", "roll", 20, [7])],
        ),
        dict(
            id="success-or-failure",
            text="Print a success line when `roll` reaches `needed`, and a failure line otherwise.",
            dictated=False,
            hints=[
                "Start like this: `if roll `",
                "Line 5 asks the question. Exactly enough passes, so which sign?",
                "A skill check in one line: `passed = roll >= needed`. In an `if`, the same question goes after `if`.",
            ],
            checks=[blanks_check("your own words"), bnd_check("exactly enough passes", "roll", "needed", via_rolls=True)],
            pass_line="Bomb Shell: That latch hates me. Less now.",
        ),
        dict(
            id="show-the-roll",
            text="Put the roll in the line you print.",
            dictated=False,
            hints=[
                "Start like this: `print(\"Rolled \" + `",
                "`roll` holds a number. What does a number need before it can be glued to text?",
                "`\"Mana: \" + str(mana)` glues text and a number. Do the same in both lines.",
            ],
            checks=[("the line shows the roll", _rerun_code() + _SHOWS_ROLL)],
        ),
    ],
    solution=_decide(),
    partials=[
        _decide(test="roll > needed", win='"___"', lose='"___"'),
        _decide(win='"It opens."', lose='"It holds."'),
    ],
    assemble=dict(
        lines=["import random", 'action = "slide a shim under the latch"', "needed = 12", "roll = random.randint(1, 20)",
               "if roll >= needed:", '    print("Rolled " + str(roll) + ": it opens.")', "else:",
               '    print("Rolled " + str(roll) + ": it holds.")'],
        distractors=["roll = random.randint(1, 19)", "if roll > needed:", '    print("Rolled " + roll + ": it holds.")'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The skill check, in order",
            text=(
                "1. Roll: `roll = random.randint(1, 20)`.\n"
                "2. Ask: `if roll >= needed:`.\n"
                "3. Say what happened, with the roll glued in using `str(roll)`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "At the trap door, `perform_roll` rolled the die and each check said `return roll >= required_roll`. "
                "Your `if` asks that same question, then prints what it means."
            ),
        ),
        dict(
            angle="picture",
            label="A d20 against a target",
            text="```text\n1 ........ 11 | 12 ........ 20\n   fail       | pass\n              ^ needed = 12\n```",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Dumb Luck",
        text=(
            "Once a day, Lucky gets a second chance. Inside the `else`, after the failure line, roll `roll` once "
            "more. Then use another `if` (indented inside the `else`) to say whether the new roll passed."
        ),
        hints=[
            "Start like this: inside the `else`, under the failure line, `roll = `",
            "Then `    if roll >= needed:` with its own success line under it, indented once more, and an `else`.",
        ],
        checks=[
            (
                "a failed roll is rolled once more",
                _rerun_code() +
                "_N = globals().get('needed', 12)\n"
                "_ns, _rows1, _c1, _err, _miss = _rerun({}, [1, 20])\n"
                "assert not _err, _stop({}, [1, 20], _err)\n"
                "assert len(_c1) == 2, _mend('Add `roll = random.randint(1, 20)` inside the `else`.', 'The first roll '\n"
                "                            'failed, but Lucky did not roll once more.', {}, [1, 20])\n"
                "_ns, _rows2, _c2, _err, _miss = _rerun({}, [20])\n"
                "assert len(_c2) == 1, _mend('Roll again only inside the `else`.', 'The first roll passed, but there was '\n"
                "                            'a second roll.', {}, [20])\n"
                "_ns, _rows3, _c3, _err, _miss = _rerun({}, [1, 1])\n"
                "assert _rows1 != _rows3, _mend('Ask about the new roll with another `if`.', 'The second roll passed, but '\n"
                "                               'your program said the same as for two failed rolls.', {}, [1, 20])\n",
            ),
        ],
        solution=_decide(
            lose=DECIDE_LOSE,
            extra_else=(
                "    roll = random.randint(1, 20)\n"
                "    if roll >= needed:\n"
                '        print("Dumb Luck! Rolled " + str(roll) + ": it opens.")\n'
                "    else:\n"
                '        print("Dumb Luck ran out. Rolled " + str(roll) + ".")\n'
            ),
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def strength_check(roll):\n    required_roll = 12\n    return roll >= required_roll",
        why=(
            "You have seen this. The trap door had three checks, each with its own `required_roll` and the same "
            "question: `roll >= required_roll`. Now you write the whole check yourself: the roll, the question, "
            "and what happens."
        ),
    ),
    takeaway="A skill check: `roll = random.randint(1, 20)`, then `if roll >= needed:` and `else:`. Glue the roll with `str()`.",
    wrong_answers=[
        dict(why="> instead of >= (exactly enough fails)", code=_decide(test="roll > needed"),
             fails_at=2, message_contains="exactly"),
        dict(why="a d19 (top face left out)", code=_decide(roll="random.randint(1, 19)"), fails_at=1,
             message_contains="never gives 20"),
        dict(why="a roll typed by hand", code=_decide(roll="14"), fails_at=1, message_contains="typed"),
        dict(why="the needed number typed in the if", code=_decide(test="roll >= 12"), fails_at=2,
             message_contains="not a number you typed"),
        dict(why="= instead of == in the if", code=_decide(test="roll = needed"), fails_at=0, message_contains="=="),
        dict(why="the roll glued without str()", code=_decide(win='"Rolled " + roll', lose='"Rolled " + roll'),
             fails_at=0, message_contains="concatenate"),
        dict(why="lines without the roll", code=_decide(win='"It opens."', lose='"It holds."'), fails_at=3,
             message_contains="str(roll)"),
        dict(why="a roll typed into the line", code=_decide(win='"Rolled 14: it opens."', lose='"Rolled 14: it holds."'),
             fails_at=3, message_contains="a 3"),
        dict(why="needed shown instead of the roll",
             code=_decide(win='"Needed " + str(needed) + ": it opens."', lose='"Needed " + str(needed) + ": it holds."'),
             fails_at=3, message_contains="str(roll)"),
        dict(why="___ left in the lines", code=_decide(win='"___"', lose='"___"'), fails_at=2, message_contains="___"),
        dict(why="needed outside a d20", code=_decide(needed=25), fails_at=2, message_contains="from 2 to 20"),
        dict(why="no else: the failure line has no indent, so it prints after a pass too (it passed before the probe)",
             code=_decide().replace("else:\n    print(", "print("), fails_at=2, message_contains="as well as the success line"),
        dict(why="the roll printed on a line by itself, the success and failure lines left without it (passed before)",
             code=_decide(win='"It opens."', lose='"It holds."').replace(
                 "roll = random.randint(1, 20)\n", "roll = random.randint(1, 20)\nprint(roll)\n"),
             fails_at=3, message_contains="line by itself"),
        dict(why="a fresh randint glued into the line instead of the box (it shows another roll; passed before)",
             code=_decide(win='"Rolled " + str(random.randint(1, 20)) + ": it opens."',
                          lose='"Rolled " + str(random.randint(1, 20)) + ": it holds."'),
             fails_at=3, message_contains="new roll"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="randint,boundary,if-else", solo="false", dictates="1",
             foreign_names="mana,passed") + "\n"
        "Make, skeleton (G3 R19). DF: any action text and any needed from 2 to 20 (verified: needed 2 and 20 pass; "
        "the BND rolls 1 and 20 as the low and high rolls, and needed - 1, needed, needed + 1 when that is a face). "
        "RND scripts the die, so no check depends on a real random roll. CP3 rolls two numbers that are not "
        "`needed`, so printing `needed` instead of the roll fails; any second randint call gets another number, so "
        "a line that rolls again instead of gluing in `roll` fails; and the roll must sit in a line with words "
        "(`print(roll)` alone fails). A shared `Rolled 14` line above the if, `print(\"Rolled\", roll, ...)` with "
        "commas, `passed = roll >= needed` / `if passed:` (the hint's name), reversed operands and `roll > needed - 1` "
        "all pass (probed). BND also needs exactly one of the two lines per roll, so an unindented failure line "
        "(no `else`) fails. Partials: 1 = rolled with `>` and the `___` "
        "lines left (passes CP1, fails CP2), 2 = right test without the roll in the lines (fails CP3)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-09 broken-spell-2B (four bugs, in Python's reporting order)
# ---------------------------------------------------------------------------------------------

CHAIN_GOOD = (
    "if hours_left <= 2:\n    print(\"The clock is red.\")\n"
    "elif hours_left <= 12:\n    print(\"The clock is bright blue.\")\n"
    "else:\n    print(\"The clock is calm blue.\")\n"
)
CHAIN_BAD = (
    "if hours_left <= 2:\n    print(\"The clock is red.\")\n"
    "else:\n    print(\"The clock is calm blue.\")\n"
    "elif hours_left <= 12:\n    print(\"The clock is bright blue.\")\n"
)


def _broken(head="import random\n", roll_if="if roll == 20:", option='"option 1"', chain=CHAIN_GOOD, roll="random.randint(1, 20)"):
    return (
        head +
        f"roll = {roll}\n{roll_if}\n    print(\"A perfect roll!\")\n\n"
        f"choice = \"option 1\"\nif choice == {option}:\n    print(\"Mar'tu: Then we leave at dawn.\")\n"
        "elif choice == \"option 2\":\n    print(\"Mar'tu: Rest first, yes?\")\n\n"
        f"hours_left = 5\n{chain}"
    )


BROKEN_STARTER = _broken(head="", roll_if="if roll = 20:", option="option 1", chain=CHAIN_BAD)
DAWN = "Mar'tu: Then we leave at dawn."
REST = "Mar'tu: Rest first, yes?"
RED, BRIGHT, CALM = "The clock is red.", "The clock is bright blue.", "The clock is calm blue."

BROKEN_SPELL_2B = dict(
    id="broken-spell-2b",
    title="Broken spell",
    martu=(
        "Four slips, and Python reports them one at a time. Read the last line of each message first, then go to "
        "the line it names.\n"
        "Mend one, run again, and Python shows you the next. Normal. That is how everyone debugs, yes?"
    ),
    names=["roll", "choice", "hours_left"],
    pair_talk=(
        "Pair talk: swap broken spells if you like. Read each message to your partner and say which line it names. "
        "Then each of you mends it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="ask-with-double-equals",
            text="Mend the line that asks whether `roll` is 20.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Python's message names line 2 and says `Maybe you meant '=='`. Which sign asks a question?",
                "`=` puts a value in a box. `==` asks: is the same as? `if mana == 0:` asks whether mana is 0.",
            ],
            checks=[
                lines_check("a perfect roll only on 20", [
                    ({}, [20], ["A perfect roll!"], [], "Ask with `==`: `if roll == 20:`."),
                    ({}, [7], [], ["A perfect roll!"],
                     "Keep `roll = random.randint(1, 20)`, and ask with `==`: `if roll == 20:`."),
                ]),
            ],
        ),
        dict(
            id="quote-the-option",
            text="Mend the line that checks the first option.",
            dictated=False,
            hints=[
                "Read Python's last line first. Then look at the line it names.",
                "Python says `invalid syntax` on the `option 1` line. Two bare words: is that a box, or text?",
                QUOTES_RULE + " The option is text, so it needs quotes.",
            ],
            checks=[
                strexact_check(["option 1", "option 2"]),
                lines_check("each option gets its reply", [
                    ({"choice": "option 1"}, None, [DAWN], [REST], "Put the option in quotes: `\"option 1\"`."),
                    ({"choice": "option 2"}, None, [REST], [DAWN], "Keep the `elif` for `\"option 2\"` as it is."),
                    ({"choice": "option 3"}, None, [], [DAWN, REST],
                     "Ask whether `choice` is the same as `\"option 1\"`: use `==`."),
                ]),
            ],
        ),
        dict(
            id="else-goes-last",
            text="Mend the clock chain so 5 hours prints `The clock is bright blue.`",
            dictated=False,
            hints=[
                "Read Python's last line first. Then look at the line it names, and the line just before it.",
                "Python says `invalid syntax` on the `elif` line. Look at what comes right before it.",
                "`elif` must come before `else`. `else` is always last:\n```python\nif a:\n    ...\nelif b:\n    ...\n"
                "else:\n    ...\n```",
            ],
            checks=[
                lines_check("one clock line for each hour", [
                    ({"hours_left": 5}, None, [BRIGHT], [RED, CALM], "Put the `elif` before the `else`."),
                    ({"hours_left": 2}, None, [RED], [BRIGHT, CALM], "One chain: `if`, then `elif`, then `else` last."),
                    ({"hours_left": 20}, None, [CALM], [RED, BRIGHT], "Keep the `else:` at the end, for long hours."),
                ]),
            ],
        ),
        dict(
            id="import-the-dice",
            text="Mend the roll so Python knows where `random` comes from.",
            dictated=False,
            hints=[
                "Read Python's last line first. It asks you a question.",
                "Python says `name 'random' is not defined` and asks: `Did you forget to import 'random'?`",
                "Tools on Python's shelf need an `import` first, at the top: `import random`, then `random.randint(1, 6)`.",
            ],
            checks=[rnd_check("roll is a d20", "roll", 20, [9])],
            pass_line="Mar'tu: Four slips, four mends. You read every message. Good.",
        ),
    ],
    solution=_broken(),
    assemble=dict(
        lines=[line for line in _broken().splitlines() if line.strip()],
        distractors=["if roll = 20:", "if choice == option 1:"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="One slip at a time",
            text=(
                "1. Run. Read the last line of the message.\n"
                "2. Go to the line it names. Mend it.\n"
                "3. Run again. A new message? Good: that is the next slip.\n"
                "4. No message? The checks tell you what is left."
            ),
        ),
        dict(
            angle="picture",
            label="Where each slip is",
            text=(
                "```text\nline 1   roll = random...\n  needs import random above it\nline 2   if roll = 20:\n"
                "  = puts, == asks\nline 6   option 1\n  text needs quotes\nline 16  elif after else\n"
                "  else is always last\n```\n"
                "The line numbers are the starter's. Once `import random` is on top, every line moves down one."
            ),
        ),
        dict(
            angle="shorter",
            text="`import random` at the top. `==` to ask. `\"option 1\"` in quotes. `elif` before `else`.",
        ),
    ],
    takeaway="Read the last line, go to the line it names, mend one slip, run again.",
    wrong_answers=[
        dict(why="the starter (= in the if first)", code=BROKEN_STARTER, fails_at=0, message_contains="=="),
        dict(why="== mended, the option still unquoted",
             code=_broken(head="", option="option 1", chain=CHAIN_BAD), fails_at=0, message_contains="invalid syntax"),
        dict(why="option quoted, the elif still after else",
             code=_broken(head="", chain=CHAIN_BAD), fails_at=0, message_contains="invalid syntax"),
        dict(why="three mended, import random still missing (rule 6b)", code=_broken(head=""), fails_at=0,
             message_contains="import 'random'"),
        dict(why="import random at the bottom (too late)", code=_broken(head="") + "import random\n", fails_at=0,
             message_contains="random"),
        dict(why="the option mended with a capital O", code=_broken(option='"Option 1"'), fails_at=2,
             message_contains="capital"),
        dict(why="elif changed to if, after the else (two chains)",
             code=_broken(chain=CHAIN_BAD.replace("elif hours_left", "if hours_left")), fails_at=3,
             message_contains="Put the `elif` before the `else`"),
        dict(why="the else branch deleted", code=_broken(
            chain="if hours_left <= 2:\n    print(\"The clock is red.\")\nelif hours_left <= 12:\n    print(\"The clock is bright blue.\")\n"),
             fails_at=3, message_contains="calm blue"),
        dict(why="roll typed as 20 to make the perfect line print", code=_broken(roll="20"), fails_at=1,
             message_contains="a 7"),
        dict(why="the option line mended as != \"option 2\" (right for options 1 and 2 only; passed before the probe)",
             code=_broken().replace('if choice == "option 1":', 'if choice != "option 2":'), fails_at=2,
             message_contains="option 3"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="read-traceback,elif-chain,quote-text,randint", solo="false",
             dictates="", foreign_names="mana,a,b") + "\n"
        "Broken spell, four slips in the order Python reports them: the three SyntaxErrors in file order (`if roll "
        "= 20:` -> the `=`-in-`if` row; `option 1` unquoted -> the multi-word row; `elif` after `else` -> its "
        "row), then the runtime NameError for the missing import (rule 6b, 'Did you forget to import'). Each "
        "slip left fails at 0 with its own message (WA). No partials: on the site a crash fails every "
        "checkpoint. Can be done in pairs (swap broken spells); every student mends it on their own screen."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2B-S solo-2B (one bug, done alone)
# ---------------------------------------------------------------------------------------------

SOLO_STARTER = 'hours_left = 2\nif hours_left <= 2\n    print("Inside, now.")\n'
INSIDE = "Inside, now."

SOLO_2B = dict(
    id="solo-2b",
    title="Show Mar'tu",
    martu="A short one, just for you. One slip. Read the message, then mend it.",
    solo=True,
    explainer="lean",
    names=["hours_left"],
    starter=SOLO_STARTER,
    checkpoints=[
        dict(
            id="inside-now",
            text="Make it print `Inside, now.` when 2 hours or fewer are left.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Look at the very end of the `if` line.",
                "Every `if` line ends with a colon: `if rain > 0:`.",
            ],
            checks=[
                lines_check("Inside, now. at 2 hours or fewer", [
                    ({"hours_left": 2}, None, [INSIDE], [], "Exactly 2 hours left counts too: keep `<= 2`."),
                    ({"hours_left": 1}, None, [INSIDE], [], "Keep `<= 2`: 1 hour left is fewer than 2, so it should print."),
                    ({"hours_left": 3}, None, [], [INSIDE],
                     "Keep the print indented under the `if`: only 2 hours or fewer should print it."),
                    ({"hours_left": 10}, None, [], [INSIDE],
                     "Keep the print indented under the `if`: only 2 hours or fewer should print it."),
                ]),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ read Python's message and mend an `if`.",
        ),
    ],
    solution='hours_left = 2\nif hours_left <= 2:\n    print("Inside, now.")\n',
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line. 2. Go to the line it names. 3. Look at its end."),
        dict(angle="shorter", text="Colon at the end of the `if` line."),
    ],
    takeaway="On your own: read the message, find the line, mend the slip.",
    wrong_answers=[
        dict(why="the starter (missing colon)", code=SOLO_STARTER, fails_at=0, message_contains="expected ':'"),
        dict(why="< instead of <= (2 hours left does not print)",
             code='hours_left = 2\nif hours_left < 2:\n    print("Inside, now.")\n', fails_at=1, message_contains="hours_left = 2"),
        dict(why="the if removed (always prints)", code='hours_left = 2\nprint("Inside, now.")\n', fails_at=1,
             message_contains="hours_left = 3"),
        dict(why="colon added, but the print unindented",
             code='hours_left = 2\nif hours_left <= 2:\nprint("Inside, now.")\n', fails_at=0, message_contains="indented block"),
        dict(why="the comma dropped", code='hours_left = 2\nif hours_left <= 2:\n    print("Inside now.")\n',
             fails_at=1, message_contains="Inside, now."),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="if-else,read-traceback", solo="true", dictates="",
             foreign_names="rain", seat_b="the same program with an unindented body: `if hours_left <= 2:` / "
             "`print(\"Inside, now.\")` (IndentationError)") + "\n"
        "SOLO, one bug. Seat A (and anyone solo) gets the missing colon; seat B would get the unindented body "
        "once pair mode ships. Recorded, never blocking, never shown to a partner. CMB at 2, 1, 3 and 10 hours. "
        "explainer='lean' (teacher's ruling, Unit 2 solo items and QC2 only): the explainer names the kind of slip "
        "and the line but leaves out the fix; Python's own text stays visible."
    ),
)

LESSON_2B = dict(
    kind="lesson",
    id="if-the-clock-turns-red",
    title="If the Clock Turns Red",
    minutes=42,
    summary="Make Python choose with `if`, `else` and `elif`, join questions with `and` and `or`, and roll dice.",
    notes=(
        "Lesson 2B (CC; 2B-06 and 2B-09 SC). Preceded by 2b-remembers. Exactly one SOLO (solo-2b, explainer='lean'). "
        "Non-dictated checkpoints: 2B-02 CP2-3, 2B-03, 2B-06 CP2-3, 2B-07 CP2, 2B-08 CP2-3, 2B-09, 2B-S. 2B-05 is "
        "the campaign rehearsal (program-dialogue-options). Rest marker: 2B-05's pass line (Lucky) comes about "
        "halfway. 42 minutes (was 41): the teacher's ruling adds about a minute (either-roll no longer dictated, "
        "the clock-colors one-chain check)."
    ),
    exercises=[FIRST_IF, COLON_AND_INDENT, OTHERWISE, CLOCK_COLORS, FOUR_ANSWERS, AND_OR_NOT, ROLL_A_DIE,
               ROLL_AND_DECIDE, BROKEN_SPELL_2B, SOLO_2B],
)


# =============================================================================================
# Article 2-A1 "Match: Another Way to Choose" (optional)
# =============================================================================================


def _match_chain(choice="option 2", say="print", extra_case="", wildcard=True):
    out = f'choice = "{choice}"\nmatch choice:\n'
    for option, reply in zip(OPTIONS, REPLIES):
        out += f'    case "{option}":\n        {say}("{reply}")\n'
    out += extra_case
    if wildcard:
        out += f'    case _:\n        {say}("Hm.")\n'
    return out


MATCH_EXAMPLE = _match_chain()
ELIF_EXAMPLE = (
    'choice = "option 2"\n'
    + "".join(
        f'{"if" if i == 0 else "elif"} choice == "{option}":\n    print("{reply}")\n'
        for i, (option, reply) in enumerate(zip(OPTIONS, REPLIES))
    )
    + 'else:\n    print("Hm.")\n'
)
FIFTH_REPLY = "Ask me again at dawn."
MATCH_TRY_STARTER = _match_chain(choice="option 5", say="mar_tu_says")
MATCH_TRY_SOLUTION = _match_chain(choice="option 5", say="mar_tu_says",
                                  extra_case=f'    case "option 5":\n        mar_tu_says("{FIFTH_REPLY}")\n')

# Each option must make the line inside ITS OWN case speak (by line number), whatever the words: options 1 to 4 their
# cases, "option 5" the new case, anything else `case _:` (or the `else:` of an elif chain, which also passes).
_FIVE = r"""
_tree = _ast.parse(_source)
def _span(_body):
    return (_body[0].lineno, max(getattr(_b, 'end_lineno', None) or _b.lineno for _b in _body))
def _branch(_lit):
    for _n in _ast.walk(_tree):
        _t = type(_n).__name__
        if _t == 'match_case':
            _p = _n.pattern
            if _lit is None and type(_p).__name__ == 'MatchAs' and _p.pattern is None:
                return _span(_n.body)
            if (_lit is not None and type(_p).__name__ == 'MatchValue' and type(_p.value).__name__ == 'Constant'
                    and _p.value.value == _lit):
                return _span(_n.body)
        elif _t == 'If':
            if _lit is not None and any(type(_x).__name__ == 'Constant' and _x.value == _lit for _x in _ast.walk(_n.test)):
                return _span(_n.body)
            if _lit is None and _n.orelse and type(_n.orelse[0]).__name__ != 'If':
                return _span(_n.orelse)
    return None
def _inside(_say, _span_):
    return _span_ is not None and _span_[0] <= _say[2] <= _span_[1]
_rest = _branch(None)
_add5 = 'Add `case "option 5":` above `case _:`, with a `mar_tu_says(...)` line under it.'
for _k in (1, 2, 3, 4, 5, 0):
    _c = 'option ' + str(_k) if _k else 'a grumpy moth'
    _vals = {'choice': _c}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [], _err)
    _says = [_e for _e in _ns.get('_said', []) if _e[0] == 'says']
    _own = _branch(_c) if _k else _rest
    if _k == 5:
        assert _own or not (_says and _inside(_says[0], _rest)), _mend(_add5, "Mar'tu fell through to `case _:`.",
                                                                       _vals, [])
        assert _own and _says, _mend(_add5, "Mar'tu said nothing.", _vals, [])
        assert _inside(_says[0], _own), _mend('Put a `mar_tu_says(...)` line inside `case "option 5":`, indented under '
                                              'it.', "Mar'tu said a line from another case.", _vals, [])
    elif _k:
        assert _says and _inside(_says[0], _own), _mend('Keep `case "' + _c + '":` as it is, with its line.',
                                                        "Mar'tu did not say that case's line.", _vals, [])
    else:
        assert _says and _inside(_says[0], _rest), _mend('Keep `case _:` last, with its `mar_tu_says` line, for anything '
                                                         'else.', "Mar'tu said nothing.", _vals, [])
    assert len(_says) == 1, _mend('Give each case one `mar_tu_says` line: one case runs, so one line.',
                                  "Mar'tu spoke " + str(len(_says)) + ' times.', _vals, [])
"""

MATCH_TRY = dict(
    id="five-options",
    title="A fifth option",
    martu=(
        "Here is the four-answers chain as a `match`, with `case _:` at the end for anything else. A fifth option "
        "appeared on the board. Give it a case of its own."
    ),
    introduces=["node:Match"],
    setup=DIALOGUE_SETUP,
    names=["choice", "mar_tu_says"],
    pick=FIFTH_REPLY,
    starter=MATCH_TRY_STARTER,
    checkpoints=[
        dict(
            id="add-option-5",
            text="Add a `case \"option 5\":` above `case _:`, with any line for Mar'tu to say.",
            dictated=True,
            hints=[
                "Start like this: above `case _:`, type four spaces, then `case `",
                "Copy the shape of `case \"option 4\":` and the line under it. Change the option and the words.",
                "Each `case` is indented under `match`, and its line is indented once more:\n```python\nmatch pet:\n"
                "    case \"owl\":\n        print(\"Hoot.\")\n```",
            ],
            checks=[
                strexact_check(["option 5"]),
                ("each option says its own line", _rerun_code(DIALOGUE_SETUP) + _FIVE),
            ],
            pass_line="Mar'tu: Five options. The board is getting crowded, yes?",
        ),
    ],
    solution=MATCH_TRY_SOLUTION,
    assemble=dict(
        lines=[line for line in MATCH_TRY_SOLUTION.splitlines() if line.strip()],
        distractors=["    case option 5:", "case _:"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="match next to elif",
            text=(
                "With `elif`:\n```text\nif choice == \"option 1\":\nelif choice == \"option 2\":\nelse:\n```\n"
                "With `match`:\n```text\nmatch choice:\n    case \"option 1\":\n    case \"option 2\":\n    case _:\n```\n"
                "Same choices, two ways to write them. Each `if` or `elif` line becomes a `case` line, and `else:` "
                "becomes `case _:`."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Where it goes",
            text="1. Find `case _:`. 2. Above it, add `case \"option 5\":`. 3. Under that, indented once more, `mar_tu_says(\"...\")`.",
        ),
    ],
    takeaway="`match choice:` then `case \"option 1\":` for each value, and `case _:` last for anything else.",
    wrong_answers=[
        dict(why="the new case below case _ (verified SyntaxError)",
             code=MATCH_TRY_STARTER + f'    case "option 5":\n        mar_tu_says("{FIFTH_REPLY}")\n',
             fails_at=0, message_contains="unreachable"),
        dict(why="the option unquoted",
             code=_match_chain(choice="option 5", say="mar_tu_says",
                               extra_case=f'    case option 5:\n        mar_tu_says("{FIFTH_REPLY}")\n'),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="a capital O",
             code=_match_chain(choice="option 5", say="mar_tu_says",
                               extra_case=f'    case "Option 5":\n        mar_tu_says("{FIFTH_REPLY}")\n'),
             fails_at=1, message_contains="capital"),
        dict(why="the starter (no fifth case: option 5 falls to Hm.)", code=MATCH_TRY_STARTER, fails_at=1,
             message_contains="fell through to `case _:`"),
        dict(why="case _ itself changed to say the option 5 words (option 5 still has no case of its own)",
             code=MATCH_TRY_STARTER.replace('    case _:\n        mar_tu_says("Hm.")', f'    case _:\n        mar_tu_says("{FIFTH_REPLY}")'),
             fails_at=1, message_contains="fell through"),
        dict(why="case _ deleted (anything else says nothing)",
             code=_match_chain(choice="option 5", say="mar_tu_says", wildcard=False,
                               extra_case=f'    case "option 5":\n        mar_tu_says("{FIFTH_REPLY}")\n'),
             fails_at=1, message_contains="case _"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="elif-chain", solo="false", dictates="1", foreign_names="pet") + "\n"
        "Try-it [CALL]: the five-option version. Any words for option 5 pass (lint e); options 1 to 4 and "
        "anything else (a grumpy moth) must still make their own case speak. Matched by line number, not words "
        "(loosened after the check-breaker probe: editing option 4's reply used to fail with 'should still say the "
        "line for option 4'). `case \"option 5\":` placed first and the same choices written with `elif` also pass. "
        "node:Match is optional-only: no core item uses it."
    ),
)

ARTICLE_2A1 = dict(
    kind="article",
    id="match-another-way",
    title="Match: Another Way to Choose",
    optional=True,
    minutes=12,
    summary="The four-answers chain, written with `match` and `case`. Learn to read both.",
    introduces=["node:Match"],
    body=(
        "There is another way to write the four-answers chain. It is called [[match]].\n"
        "`match choice:` says: look at what is in `choice`. Each `case \"option 1\":` says: if it is these exact "
        "letters, run the lines under me. `case _:` catches anything else, like `else`.\n"
        "Python tries the cases from the top and runs the first one that fits. Then it stops, the same as `elif`.\n"
        "The two examples below print the same line. Run both and compare them.\n"
        "The campaign uses `elif`, so learn to read both. When you write your own, use whichever reads more "
        "clearly to you."
    ),
    examples=[
        dict(code=MATCH_EXAMPLE, output=REPLIES[1]),
        dict(code=ELIF_EXAMPLE, output=REPLIES[1]),
    ],
    exercises=[MATCH_TRY],
    notes=(
        "Article 2-A1 (optional). Introduces node:Match. Example 1 is the four-answers chain as `match`, example 2 "
        "the same chain with `elif` and `else`, both for option 2. Try-it: the five-option version (CALL)."
    ),
)

# =============================================================================================
# Quiz 2 "Ley Clock Quiz"
# =============================================================================================

QUIZ_2 = dict(
    kind="quiz",
    id="ley-clock-quiz",
    title="Ley Clock Quiz",
    minutes=8,
    summary="Eight questions on comparisons, if/elif/else, and and/or, and dice. Retake as often as you like.",
    notes="Quiz 2 (SC): 2 mc, 4 predict, 1 parsons, 1 bug. Review order: right answers first (G1 R26).",
    questions=[
        dict(
            type="predict",
            id="exactly-enough",
            q="What will this print?",
            code="roll = 12\nneeded = 12\nprint(roll >= needed)\nprint(roll > needed)\n",
            choices=["True\nFalse", "True\nTrue", "False\nFalse", "False\nTrue"],
            answer="True\nFalse",
            explain="`>=` means at least: 12 is at least 12, so True. `>` leaves the boundary out: 12 is not more than 12.",
            notes="Boundary: the campaign's `<` versus `<=` (hold-the-barrier).",
        ),
        dict(
            type="predict",
            id="clock-at-two",
            q="What will this print?",
            code=(
                "hours_left = 2\nif hours_left <= 2:\n    print(\"red\")\nelif hours_left <= 12:\n"
                "    print(\"bright blue\")\nelse:\n    print(\"calm blue\")\n"
            ),
            choices=["red", "bright blue", "calm blue", "red\nbright blue"],
            answer="red",
            explain="`2 <= 2` is True, so the first branch runs. Only one branch of a chain ever runs.",
        ),
        dict(
            type="mc",
            id="d6-faces",
            q="Which values can `random.randint(1, 6)` give?",
            choices=["0 to 5", "1 to 5", "1 to 6", "0 to 6"],
            answer=2,
            why_wrong={
                0: "`randint` starts at the first number you give it: 1, not 0.",
                1: "`randint` includes both ends, so 6 can come up.",
                3: "0 is below the first number, so it never comes up.",
            },
            explain="`random.randint(1, 6)` gives 1, 2, 3, 4, 5 or 6. Both ends are included, like a real d6.",
        ),
        dict(
            type="predict",
            id="both-needed",
            q="What will this print?",
            code="mana = 12\ncost = 9\naffinity = 8\nrequired = 9\nprint(mana >= cost and affinity >= required)\n",
            choices=["True", "False"],
            answer="False",
            explain="Enough mana (12 >= 9), but affinity 8 is below 9. `and` needs both, so False.",
        ),
        dict(
            type="parsons",
            id="four-answers-order",
            q="Put the lines in order (with their indents) so the program prints Mar'tu's reply to option 2.",
            lines=['choice = "option 2"']
            + [
                part
                for i, (option, reply) in enumerate(zip(OPTIONS, REPLIES))
                for part in (f'{"if" if i == 0 else "elif"} choice == "{option}":', f'    print("{reply}")')
            ],
            distractors=["elif choice == option 2:"],
            expected_output=REPLIES[1],
            explain="One `if`, then `elif`s, in order. Each option is text, so it keeps its quotes.",
            notes="Distractor: the unquoted option (2B-05 WA, a verified SyntaxError).",
        ),
        dict(
            type="bug",
            id="ask-not-put",
            q="This should print `A perfect roll!` for a 20. Mend it.",
            code="roll = 20\nif roll = 20:\n    print(\"A perfect roll!\")\n",
            fix="roll = 20\nif roll == 20:\n    print(\"A perfect roll!\")\n",
            expected_output="A perfect roll!",
            explain="`=` puts a value in a box. An `if` asks, so it needs `==`: is the same as.",
        ),
        dict(
            type="mc",
            id="which-asks",
            q="Which line asks whether `hero` is Lucky?",
            choices=['hero = "Lucky"', 'hero == "Lucky"', "hero == Lucky", '"hero" == "Lucky"'],
            answer=1,
            why_wrong={
                0: "`=` puts Lucky in the box. It does not ask anything.",
                2: "With no quotes, Python looks for a box named `Lucky`. The name is text, so it needs quotes.",
                3: "With quotes, `\"hero\"` is the word hero, not the box. That asks whether two different words match.",
            },
            explain="`hero == \"Lucky\"` asks: is the text in the box `hero` the same as these exact letters?",
        ),
        dict(
            type="predict",
            id="wide-test-first",
            q="What will this print?",
            code=(
                "roll = 18\nif roll >= 10:\n    print(\"A good roll.\")\nelif roll >= 15:\n"
                "    print(\"A great roll.\")\nelse:\n    print(\"A poor roll.\")\n"
            ),
            choices=["A good roll.", "A great roll.", "A good roll.\nA great roll.", "A poor roll."],
            answer="A good roll.",
            explain=(
                "`18 >= 10` is True, so the first branch wins and the rest are skipped, even though 18 is also great. "
                "The order rule: " + ORDER_RULE + ". `>= 15` lets fewer numbers through than `>= 10`, so it goes first."
            ),
        ),
    ],
)

# =============================================================================================
# Project 2P1 "Road Encounter Table" (protected story beat)
# =============================================================================================

ROAD_HEADER_A = "# A. Roll\n# 1. Bring in Python's dice.\n# 2. Roll road_roll with a d20.\n"
ROAD_HEADER_B = (
    "\n# B. Table: give each tier its own text in encounter. Replace each ___, then add the other tiers.\n"
    "# 3.  1        Lucky fires the Telegun (and lands in a hedge)\n"
    "#     2 to 6   a ley-line hums under the road\n"
    "#     7 to 15  a quiet road\n"
    "#     16 to 19 a brass-cart peddler\n"
    "#     20       a starlode vein for Gearshift\n"
)
ROAD_HEADER_C = '\n# C. Tell it\n# 4. Print "Rolled " + str(road_roll) + ": " + encounter\n'
# Teacher's ruling: part B starts with the first two branches pre-filled (text blanks), and `road_roll = 0` is a
# placeholder so the starter still runs (0 takes the second branch; nothing is printed yet).
ROAD_PLACEHOLDER = "road_roll = 0\n"
ROAD_PREFILL = 'if road_roll == 1:\n    encounter = "___"\nelif road_roll <= 6:\n    encounter = "___"\n'
ROAD_STARTER = ROAD_HEADER_A + ROAD_PLACEHOLDER + ROAD_HEADER_B + ROAD_PREFILL + ROAD_HEADER_C

ROAD_TEXTS = [
    "Lucky fires the Telegun and lands in a hedge.",
    "A ley-line hums under the road.",
    "A quiet road. Too quiet, yes?",
    "A brass-cart peddler waves you down.",
    "A starlode vein! Gearshift's visor glows.",
]
ROAD_TESTS = ["road_roll == 1", "road_roll <= 6", "road_roll <= 15", "road_roll <= 19"]


def _table(tests=ROAD_TESTS, texts=ROAD_TEXTS, last_else=True):
    out = ""
    for i, test in enumerate(tests):
        out += f'{"if" if i == 0 else "elif"} {test}:\n    encounter = "{texts[i]}"\n'
    if last_else:
        out += f'else:\n    encounter = "{texts[len(tests)]}"\n'
    return out


ROAD_TELL = 'print("Rolled " + str(road_roll) + ": " + encounter)\n'


def _road(imp="import random\n", roll="road_roll = random.randint(1, 20)\n", table=None, tell=ROAD_TELL, extra=""):
    table = _table() if table is None else table
    return ROAD_HEADER_A + imp + roll + extra + ROAD_HEADER_B + table + ROAD_HEADER_C + tell


ROAD_PICK = (
    "# Mar'tu's picks, ready to copy:\n"
    + "".join(f'# "{text}"\n' for text in ROAD_TEXTS)
).rstrip("\n")

_TIERS = r"""
_names = {1: '1', 2: '2 to 6', 4: '2 to 6', 6: '2 to 6', 7: '7 to 15', 11: '7 to 15', 15: '7 to 15',
          16: '16 to 19', 17: '16 to 19', 19: '16 to 19', 20: '20'}
_enc = {}
for _r in (1, 2, 4, 6, 7, 11, 15, 16, 17, 19, 20):
    _ns, _rows, _calls, _err, _miss = _rerun({}, [_r])
    _branch_for = 'Give the chain a branch for ' + _names[_r] + ', with its own `encounter = "..."` line.'
    assert not (_err and "'encounter'" in _err), _mend(_branch_for, 'Python could not find `encounter`.', {}, [_r])
    assert not _err, _stop({}, [_r], _err)
    assert _calls, ("Roll `road_roll` with `random.randint(1, 20)` before the table, so Mar'tu's check can roll "
                    'for you.')
    assert 'encounter' in _ns, _mend(_branch_for, '`encounter` was never set.', {}, [_r])
    _e = _ns['encounter']
    assert type(_e).__name__ == 'str' and _e.strip(), _mend('Put some text in `encounter`, in quotes. Any words you '
                                                            'like.', '', {}, [_r])
    # whole numbers masked, so an encounter that shows the roll ("A quiet road (7)") is still one text per tier
    _enc[_r] = _re.sub(r'\d+', '#', _e)
assert len(set(_enc.values())) > 1, ("Give each tier its own branch and its own text. Every roll gave the same "
                                     "`encounter`. (Mar'tu's check rolled every tier, only inside the check.)")
_order = 'Order the chain: first, the test that lets the fewest numbers through.'
_signs = {6: 'Use `road_roll <= 6`: it includes 6, and `< 6` leaves it out.', 15: 'Use `road_roll <= 15`: it includes 15.',
          19: 'Use `road_roll <= 19`: it includes 19.', 4: _order, 11: _order, 17: _order}
_both = "(Mar'tu's check rolled both, only inside the check.)"
for _a, _b in ((2, 4), (2, 6), (7, 11), (7, 15), (16, 17), (16, 19)):
    assert _enc[_a] == _enc[_b], (_signs[_b] + ' Rolls ' + str(_a) + ' and ' + str(_b) + ' are one tier (' + _names[_a]
                                  + '), but got different text. ' + _both)
for _a, _b in ((1, 2), (6, 7), (15, 16), (19, 20)):
    assert _enc[_a] != _enc[_b], ('Check the test that ends at ' + str(_a) + ', then the order: first, the test that '
                                  'lets the fewest numbers through. Rolls ' + str(_a) + ' and ' + str(_b) + ' got the '
                                  'same text. ' + _both)
"""

# The line is compared with the box `road_roll` (a second randint call gets another number, so a line that rolls
# again is caught). Extra words after the encounter are fine (`... yes?.`, a period); spaces in the glue are not.
_TELL = r"""
for _r, _o in ((7, 12), (20, 3)):
    _ns, _rows, _calls, _err, _miss = _rerun({}, [_r, _o])
    assert not _err, _stop({}, [_r], _err)
    assert 'encounter' in _ns, _mend('Give every tier its own `encounter = "..."` line.', '`encounter` was never set.',
                                     {}, [_r])
    _got = _ns.get('road_roll', _r)
    _want = 'Rolled ' + str(_got) + ': ' + str(_ns['encounter'])
    if not [_l for _l in _rows if _l.startswith(_want)]:
        _fresh = [_l for _l in _rows if _l.startswith('Rolled ' + str(_o))] if _got != _o else []
        assert not _fresh, _mend('Glue in the box itself: `str(road_roll)`.',
                                 'Your line shows a new roll, not the one in `road_roll`.', {}, [_r])
        _near = [_l for _l in _rows if _l.replace(' ', '').startswith(_want.replace(' ', ''))]
        assert not _near, _mend('Check the spaces in the glue: a space after `Rolled`, none before the colon, and one '
                                'after it.', 'Your line is nearly right.', {}, [_r])
        assert False, _mend('Glue it: `"Rolled " + str(road_roll) + ": " + encounter`.', '`Rolled ' + str(_got)
                            + ': ` and the encounter did not print on one line.', {}, [_r])
"""

_DUMB_LUCK = r"""
_ns1, _rows1, _c1, _e1, _m = _rerun({}, [1, 9])
assert not _e1, _stop({}, [1, 9], _e1)
assert len(_c1) == 2, _mend('Right after the first roll, add `if road_roll == 1:` with a new roll under it.',
                            'Lucky rolled a 1, but did not roll again.', {}, [1, 9])
_ns2, _rows2, _c2, _e2, _m = _rerun({}, [9])
assert len(_c2) == 1, _mend('Roll again only when `road_roll` is 1.', 'A 9 is not a 1, but there was a second roll.',
                            {}, [9])
assert _ns1.get('encounter') == _ns2.get('encounter'), _mend('Roll again before the table, so the table uses the new '
    'roll.', 'The second roll was 9, but `encounter` is not the 9 tier.', {}, [1, 9])
_ns3, _rows3, _c3, _e3, _m = _rerun({}, [1, 1])
assert len(_c3) == 2, _mend('Roll again only once: Dumb Luck works once a day.', 'After a second 1, there was a third '
                            'roll.', {}, [1, 1])
"""

ROAD_KNOWN = ["road_roll", "encounter"]

PROJECT_2P1 = dict(
    kind="project",
    id="road-encounter-table",
    title="Road Encounter Table",
    minutes=17,
    summary="Roll a d20 and see what the road to the old Institute throws at you. You write the encounters.",
    intro=(
        "The road to the old Institute is long. Oogrish insists on an encounter table: roll a d20, and the table "
        "says what the road throws at you. You write the encounters.\n"
        "Three parts, in order: A. roll, B. the table, C. tell it.\n"
        "The tiers: 1, then 2 to 6, 7 to 15, 16 to 19, and 20. The first two branches are started for you. Any "
        "words you like for each tier."
    ),
    martu=(
        "Oogrish is right, as usual. Roll first, then let the table decide, then say it out loud.\n"
        "My check rolls the die for you, every number that matters, so it can see each tier. Your words stay yours."
    ),
    names=["random", "road_roll", "encounter", "str"],
    pick=ROAD_PICK,
    starter=ROAD_STARTER,
    checkpoints=[
        dict(
            id="bring-in-the-dice",
            text="A. Bring in Python's dice: `import random`.",
            dictated=True,
            hints=[
                "Start like this: under `# 1.`, type `import `",
                "Python's dice live on a shelf. Which word brings them in?",
                "`import random` goes once, at the top, before any roll.",
            ],
            checks=[
                (
                    "random is imported",
                    "assert _uses('import:random') and type(globals().get('random')).__name__ == 'module', "
                    "'Add `import random` on its own line, under `# 1.`, before any roll.'",
                ),
            ],
        ),
        dict(
            id="roll-the-road",
            text="A. Roll `road_roll` with a d20.",
            dictated=False,
            hints=[
                "Start like this: `road_roll = random.randint(`",
                "A d20 has faces 1 to 20. `randint` includes both ends.",
                "A d12 would be `random.randint(1, 12)`: the lowest face, then the highest.",
            ],
            checks=[rnd_check("road_roll is a d20", "road_roll", 20, [13], placeholder=0)],
        ),
        dict(
            id="encounter-table",
            text="B. Finish the table: give every tier its own text in `encounter`, with `elif` and `else`.",
            dictated=False,
            hints=[
                "Start like this: under the two branches, `elif road_roll `",
                "Replace each `___` with your own words. Five tiers, so five branches: `if`, three `elif`s, and an "
                "`else` for the 20. Order rule: " + ORDER_RULE + ".",
                "The 7 to 15 tier is `elif road_roll <= 15:`. The 1 to 6 were already caught above it, so it only "
                "gets 7 to 15.",
                "The chain:\n```python\nif road_roll == 1:\n    encounter = \"...\"\nelif road_roll <= 6:\n"
                "    encounter = \"...\"\nelif road_roll <= 15:\n```\nand so on, with `else:` last.",
            ],
            checks=[blanks_check("your own words for that tier", verb="holds"),
                    ("each tier gets its own encounter", _rerun_code() + _TIERS)],
            pass_line="Mar'tu: Hm. Noted. The road will throw what it throws, yes?",
        ),
        dict(
            id="tell-it",
            text="C. Print `Rolled `, the roll, a colon, and the encounter, all on one line.",
            dictated=False,
            hints=[
                "Start like this: `print(\"Rolled \" + `",
                "Three pieces of text glued with `+`. Which piece is a number and needs `str()`?",
                "`\"Mana: \" + str(mana)` glues text and a number. Add `+ \": \" + encounter` the same way.",
            ],
            checks=[("the line tells the roll and the encounter", _rerun_code() + _TELL)],
            pass_line="Oogrish: Steady, now. On to the Institute.",
        ),
    ],
    solution=_road(),
    partials=[
        _road(roll=ROAD_PLACEHOLDER, table=ROAD_PREFILL, tell=""),
        _road(table=ROAD_PREFILL, tell=""),
        _road(tell=""),
    ],
    assemble=dict(
        lines=["import random", "road_roll = random.randint(1, 20)"] + [l for l in _table().splitlines()] + [ROAD_TELL.strip()],
        distractors=["elif road_roll < 6:", "road_roll = random.randint(1, 19)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The table",
            text=(
                "```text\nroll 1        -> tier 1\nroll 2 to 6   -> tier 2\nroll 7 to 15  -> tier 3\n"
                "roll 16 to 19 -> tier 4\nroll 20       -> tier 5\n```\n"
                "Each tier is one branch of the chain."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Trace a 6 and a 7",
            text=(
                "1. A 6: `6 == 1`? No. `6 <= 6`? Yes: the ley-line tier. Stop.\n"
                "2. A 7: `7 == 1`? No. `7 <= 6`? No. `7 <= 15`? Yes: the quiet road. Stop."
            ),
        ),
        dict(
            angle="in Tor",
            label="Oogrish's table",
            text=(
                "Oogrish keeps his tables on the back of a map, one tier per line, starting from the 1. The 20 is "
                "everything the other tiers did not catch, so it is the `else`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's side quest",
        text=(
            "Two things Lucky wants.\n"
            "1. Dumb Luck: right after the first roll, if `road_roll` is 1, roll it once more. Only once.\n"
            "2. A perception check: make `night_time = True` and `perception_roll = 14`. Then make `spotted` True "
            "only when `perception_roll` reaches 12 and it is `not night_time`."
        ),
        hints=[
            "Start like this: right after the roll, `if road_roll `",
            "`spotted = perception_roll >= 12 and not night_time`",
        ],
        checks=[
            ("Dumb Luck rerolls a 1 once", _rerun_code() + _DUMB_LUCK),
            name_check("spotted", skip=ROAD_KNOWN + ["night_time", "perception_roll"]),
            box_check("spotted needs a good roll and daylight", "spotted", [
                ({"perception_roll": 14, "night_time": False}, [9], True,
                 "Let a good roll in daylight spot it: `perception_roll >= 12 and not night_time`."),
                ({"perception_roll": 14, "night_time": True}, [9], False,
                 "Add `and not night_time`: at night, nobody spots anything."),
                ({"perception_roll": 11, "night_time": False}, [9], False, "Ask with `>= 12`: 11 does not reach 12."),
                ({"perception_roll": 12, "night_time": False}, [9], True, "Use `>=`: exactly 12 reaches 12."),
            ]),
        ],
        solution=_road(
            extra="if road_roll == 1:\n    road_roll = random.randint(1, 20)\n",
            tell=ROAD_TELL + "night_time = True\nperception_roll = 14\nspotted = perception_roll >= 12 and not night_time\n",
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="return random.randint(1, die_size)",
        why=(
            "You have seen this die at the trap door. There, a roll could only pass or fail. A table turns each "
            "roll into a story: same `randint`, more branches."
        ),
    ),
    takeaway="Roll with `random.randint(1, 20)`, let an `if` / `elif` / `else` table pick the text, then glue it with `str()`.",
    wrong_answers=[
        dict(why="< 6 for the 2 to 6 tier (6 falls into the quiet road)",
             code=_road(table=_table(tests=["road_roll == 1", "road_roll < 6", "road_roll <= 15", "road_roll <= 19"])),
             fails_at=3, message_contains="`< 6` leaves it out"),
        dict(why="the tiers out of order (a wide test first)",
             code=_road(table=_table(tests=["road_roll == 1", "road_roll <= 15", "road_roll <= 6", "road_roll <= 19"])),
             fails_at=3, message_contains="fewest numbers through"),
        dict(why="a d19 (randint thought to exclude its end)", code=_road(roll="road_roll = random.randint(1, 19)\n"),
             fails_at=2, message_contains="never gives 20"),
        dict(why="a d20 from 0", code=_road(roll="road_roll = random.randint(0, 20)\n"), fails_at=2,
             message_contains="can give 0"),
        dict(why="a roll typed by hand", code=_road(roll="road_roll = 13\n"), fails_at=2, message_contains="typed"),
        dict(why="no import random", code=_road(imp=""), fails_at=0, message_contains="import 'random'"),
        dict(why="the 20 folded into the peddler tier",
             code=_road(table=_table(tests=["road_roll == 1", "road_roll <= 6", "road_roll <= 15", "road_roll <= 20"])),
             fails_at=3, message_contains="Rolls 19 and 20 got the same text"),
        dict(why="one text for every tier", code=_road(table='encounter = "A long road."\n'), fails_at=3,
             message_contains="Every roll gave the same"),
        dict(why="the roll glued without str()", code=_road(tell='print("Rolled " + road_roll + ": " + encounter)\n'),
             fails_at=0, message_contains="concatenate"),
        dict(why="the line typed in (right for a 7, so the check's 20 catches it)",
             code=_road(tell='print("Rolled 7: A quiet road. Too quiet, yes?")\n'), fails_at=4, message_contains="Rolled 20"),
        dict(why="= instead of == in the first if",
             code=_road(table=_table(tests=["road_roll = 1", "road_roll <= 6", "road_roll <= 15", "road_roll <= 19"])),
             fails_at=0, message_contains="=="),
        dict(why="a stray space before the colon in the printed line",
             code=_road(tell='print("Rolled " + str(road_roll) + " : " + encounter)\n'), fails_at=4,
             message_contains="Check the spaces"),
        dict(why="a fresh randint glued into the printed line instead of road_roll (shows another roll; passed before)",
             code=_road(tell='print("Rolled " + str(random.randint(1, 20)) + ": " + encounter)\n'), fails_at=4,
             message_contains="new roll"),
        dict(why="no else for the 20 and the last test stops at 19 (a 20 sets no encounter; tell line left out so the "
                 "real die can never crash the main run)",
             code=_road(table=_table(last_else=False), tell=""), fails_at=3, message_contains="branch for 20"),
        dict(why="the starter (pre-filled table, no import yet)", code=ROAD_STARTER, fails_at=1,
             message_contains="import random"),
        dict(why="import added, road_roll still the starter's placeholder 0 (not typed by the student)",
             code=_road(roll=ROAD_PLACEHOLDER, table=ROAD_PREFILL, tell=""), fails_at=2,
             message_contains="still holds the starter's `0`"),
        dict(why="rolled, but the pre-filled ___ texts left (tell line left out so the real die cannot crash the run)",
             code=_road(table=ROAD_PREFILL, tell=""), fails_at=3, message_contains="still holds the starter's `___`"),
        dict(why="the two pre-filled branches given words, but no more tiers added (tell line left out)",
             code=_road(table=_table(tests=ROAD_TESTS[:2], last_else=False), tell=""), fails_at=3,
             message_contains="branch for 7 to 15"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="randint,boundary,elif-chain,concat-str", solo="false", dictates="1",
             foreign_names="mana", story_beat="protected", echo="static fallback") + "\n"
        "Starter: the task-group headers (A, B, C), the tiers as comments, `road_roll = 0` (a placeholder, so the "
        "starter runs) and the first two branches with `___` text blanks (teacher's ruling: part B was a blank "
        "editor; the pre-fill saves groups 1 and 3 a few minutes). The placeholder gets 'still holds the starter's "
        "`0`' and a `___` left gets 'still holds the starter's `___`'. The tier skeleton (Show me more) is "
        "the assemble lines plus the last hint. Checks: RND (scripted die, args (1, 20)) and BND over scripted rolls "
        "1, 2, 4, 6, 7, 11, 15, 16, 17, 19, 20: same-tier rolls give the same encounter, neighbouring tiers give "
        "different ones (whole numbers masked, so an encounter that shows the roll is still one text per tier: "
        "loosened after the check-breaker probe), and the printed line starts with `Rolled <road_roll>: <encounter>` "
        "for rolls 7 and 20 (extra words after it, like a period, are fine: loosened too). A second randint call "
        "gets another number, so a printed line that rolls again instead of gluing in `road_roll` fails. Any "
        "encounter text passes (lint e); 'Use Mar'tu's picks' is a note with five ready-made texts. Other right "
        "tables pass (probed): top-down (`== 20`, `>= 16`, `>= 7`, `>= 2`, else), `and` ranges, `< 7`, `<= 1`, "
        "`<= 20` with no else, and the comma print. Echo spot (2.11): the "
        "spec has Mar'tu react to one tier's text; the schema has no echo field yet, so the pass line is the "
        "privacy-safe static fallback ('Hm. Noted.'). Lucky's side quest (old group D): Dumb Luck rerolls a 1 "
        "once, and a perception check with `and not night_time`. No WA depends on the real die: the main run "
        "never crashes for one roll and not another."
    ),
)

ITEMS = [REMEMBERS_2B, LESSON_2B, ARTICLE_2A1, QUIZ_2, PROJECT_2P1]
