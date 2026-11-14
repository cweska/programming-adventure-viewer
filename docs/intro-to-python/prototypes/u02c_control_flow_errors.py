"""Unit 2 "Control Flow", part c: Project 2P2 "Three Roads to the Institute", Lesson 2C "When Spells Fizzle:
Reading Errors" (with 2c-remembers), Extra practice 2X "More fizzles", Article 2-A2 "Mar'tu's Seal", Quick Check 2
(forms A and B: code tasks as testout items, questions as optional quiz items) and Cheatsheet 2.

Spec: design/curriculum.md, "## Unit 2 · Control Flow", items 6 to 11 (u02c): Project 2P2 (with Lucky's side
quest); 2c-remembers; 2C-01, 2C-05, 2C-06, 2C-07 and 2C-S; the 2X pool (2C-02, 2C-03, 2C-04); Article 2-A2 with its
try-it `seal-the-check`; Quick Check 2 (Q1-Q4 and C1-C3, form B with hours_left tiers, a d12 and option 3 / 4);
Cheatsheet 2. Introduces node:Assert (2-A2, optional only: no core code uses `assert`).

Teacher ruling on the Unit 2 reviews, as applied here:
  * Quick Check 2 is an honest fast path: C1 (a roll against your own `needed`), C2 (mend the choices: two loud
    slips plus a quiet `.lower()` slip, a copy made and forgotten) and C3 "Hold the barrier" (`can_cast` with `and`,
    then cast_spell's chain rebuilt, where the order and the exact boundary both matter) all gate test-out. Every
    QC2 exercise and the SOLO set `explainer="lean"`: the crash explainer names the kind of slip and the line, and
    leaves out the fix (Python's own text stays visible). Not applied back to the live Unit 1. QC2 is 15 minutes.
  * Rerun messages start with the fix, say what happened, and end with the evidence in brackets, "(Mar'tu's check
    tried X, only inside the check.)", in about 35 words or fewer. One order rule: "first, the test that lets the
    fewest numbers through". A box still holding the starter's placeholder is named as such ("still holds the
    starter's `0`"); a missing starter box gets "Keep the box X from the starter".
  * Start me off (from the last hint) gives the line's left side only, before the sign or the and/or. In debug
    steps hints[0] is "Read Python's last line" (for a quiet bug: what the program printed). SOLO pass lines: "You did that on your own. On your map: ✓ ...".
  * Time: 2C-07's quiet bug is tested with `roll = 12` for one Run (then the dice go back), and 2C-01's notes are
    filled in while Python's message is still on screen, before line 4 is switched off.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN this code and
its error messages. So every campaign link here is "you've seen this, now you'll get it". Errors are normal and
expected: Mar'tu never implies they should already know this. Every student has their own device; pair talk is
optional, every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them): hints[0] Where to look (point), the middle hints Teach me
(a tiny example with other names), the last hint Show me how: the step's own line in backticks (``Write `x = 1`.``),
whose start up to its first `(` or `=` becomes Start me off. another_way, assemble (More structure), then Compare.

Check codes (curriculum 2.5). The rerun helpers are u02b's, copied (each part file is self-contained), with one
change: bnd_check() takes the die size, so Quick Check 2 form B can roll a d12. Added here:
  enough_check()   BND for 2C-05, where `mana` is worked out (15 - 6), not typed: the check reads the student's own
                   final mana, then tries `cost` at mana, mana + 1 and mana - 1, then again with `mana = 20`.
  prints_above()   2C-05 CP1: print(mana) and print(cost) sit above the `if`.
  seal_check()     2-A2: the student's asserts hold on the right line, and catch three broken versions of it
                   (`>` for `>=`, `==` for `>=`, and `passed = True`), each run in a fresh namespace.
  road_check() / road_print_check()  2P2: the cheapest road, from the student's own three costs, over 8 reruns;
                   the printed line must name the road the code picked (a line listing every road fails).
  barrier_check()  QC2 C3: cast_spell's chain over 8 reruns. Each run must print exactly one of the three starter
                   lines: low affinity first (so both short gives the not-skilled line), exactly enough casts.
  lower_kept_check() / lower_brackets_check()  QC2 C2: any capitals get their reply; a `.lower()` copy made and
                   forgotten on its own line, or `.lower` with no `()`, gets its own message.
  from_boxes_check()  u02b's: `can_cast` is not made with two `=` signs, from typed values, or left at the starter's
                   placeholder (`False`).
Check-breaker pass (adversarial review): the BND template also tries a roll above a moved `needed`, so `==` can't
hide behind `needed` at the top face; rnd_check() names `:=` (Python's own `=`-in-`if` message suggests it);
box_check() takes `foreign` (LEFT: the hint example's boxes); prints_above() needs each print below the last line
that changes that box (a print above `mana = mana - 6` shows the old 15).
Messages use invented values only and never repeat a student's own text (2.11): the road checks say "the text in
`road`", never the words the student wrote.

Python's messages here were verified in CPython 3.13 through the harness runner (the site runs 3.13 too):
  * an unclosed quote is reported before an earlier missing colon (the tokenizer runs first), so 2C-02 puts the
    quote first, the colon second and the bracket last: Python then reports them top to bottom;
  * `mama`, `encounterr` and `health` (with `Health` made) get "Did you mean: ...?" (explainer rules 6 and 5);
  * `error_type = NameError` runs silently (the TEXT special case in 2C-01).

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u02c
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
    # a whole number in a line: `Rolled 7.`, `(7h)` and `65coins` count; `17`, `0.7` and `7.5` do not
    return r'(?<![\d.])' + _re.escape(str(_v)) + r'(?!\d)(?!\.\d)'
def _with(_vals):
    _parts = ['`' + _k + ' = ' + _show(_v) + '`' for _k, _v in _vals.items()]
    return _parts[0] if len(_parts) == 1 else ', '.join(_parts[:-1]) + ' and ' + _parts[-1]
def _a_roll(_r):
    return ('an ' if str(_r)[:1] == '8' or _r in (11, 18) else 'a ') + str(_r)
def _did(_vals, _rolls, _end='', _again='ran your code again'):
    # The evidence, always in brackets at the END of a message: what the rerun changed.
    _bits = []
    if _vals:
        _bits.append('tried ' + _with(_vals))
    if _rolls:
        _bits.append('rolled ' + ', then '.join(_a_roll(_r) for _r in _rolls) + ' for you')
    return "(Mar'tu's check " + ' and '.join(_bits or [_again]) + ', only inside the check' + _end + '.)'
def _mend(_first, _what, _vals, _rolls, _again='ran your code again'):
    # A rerun message: the fix first, then what happened, then the evidence in brackets.
    return _first + ' ' + (_what + ' ' if _what else '') + _did(_vals, _rolls, '', _again)
def _printed(_line):
    return 'Your program printed `' + _line + '`' + ('' if _line[-1:] in '.!?' else '.')
def _changed(_vals, _base):
    # Only the values a rerun changed from the starter's, so the evidence stays short.
    return {_k: _v for _k, _v in _vals.items() if _base is None or _base.get(_k) != _v}
def _stop(_vals, _rolls, _err):
    return 'Mend this slip, then Run again: ' + _err + ' ' + _did(_vals, _rolls, ', and your program stopped there')
def _keep(_name):
    return ('Keep the box `' + _name + '` from the starter, as `' + _name + " = value` on its own line, so Mar'tu's "
            'check can change that line to try other values.')
def _starters(_name, _value):
    # True when a top-level line still gives `_name` the starter's placeholder value.
    return any(type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
               and _n.targets[0].id == _name and type(_n.value).__name__ == 'Constant'
               and repr(_n.value.value) == repr(_value) for _n in _ast.parse(_source).body)
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


def _leaned(code, pairs):
    """Quick Check 2 (a test-out, no hints): the same check with messages that name the slip and the evidence, never
    the fix (the teacher's lean ruling, as for the explainer). Each pair must match, so a reworded lesson message
    cannot silently leave a fix in the Quick Check."""
    for old, new in pairs:
        assert old in code, f"lean rewrite does not match: {old[:70]!r}"
        code = code.replace(old, new)
    return code


def lines_check(label, cases, setup=""):
    """CMB on printed lines. cases = [(values, rolls, must_print, must_not_print, tail), ...]. `tail` is the fix,
    so it comes first in the message."""
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


def box_check(label, target, cases, setup="", show=None, foreign=(), placeholder=None, base=None, lean=False):
    """CMB on a box. cases = [(values, rolls, expected, tail), ...]: after the rerun, `target` holds expected.
    `tail` is the fix, so it comes first. `show` = the value names the message mentions (all of them when None):
    the rerun may set more, so a student's own numbers never change the expected answer. `foreign` = the hint
    example's boxes (LEFT): a box made with one of those names gets "comes from the example" when `target` is
    missing or wrong. `placeholder` = the starter's value for `target` (`foot_cost = 0`): the starter makes the box,
    so a missing one gets "Keep the box ... from the starter", and while that line is still there and the box
    still holds it, the message says so. `base` = the starter's values: the evidence then names only the values
    a rerun changed ("with the starter's numbers" when it changed none)."""
    rows = [(dict(v or {}), list(r or []), want, tail) for v, r, want, tail in cases]
    code = _rerun_code(setup) + (
        f"_target = {target!r}\n"
        f"_show_only = {list(show or [])!r}\n"
        f"_foreign = {list(foreign)!r}\n"
        f"_placeholder = {placeholder!r}\n"
        f"_base = {base!r}\n"
        "_left = [_t.id for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ in ('Assign', 'AugAssign')\n"
        "         for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])\n"
        "         if type(_t).__name__ == 'Name' and _t.id in _foreign]\n"
        f"for _vals, _rolls, _want, _tail in {rows!r}:\n"
        "    _ns, _rows, _calls, _err, _miss = _rerun(_vals, _rolls)\n"
        "    assert not _miss, _keep(_miss[0])\n"
        "    _shown = {_k: _v for _k, _v in _vals.items() if _k in _show_only} if _show_only else _changed(_vals, _base)\n"
        "    _again = 'ran your code again' if _base is None else 'ran your code again with the starter' + chr(39) + 's numbers'\n"
        "    assert not _err, _stop(_shown, _rolls, _err)\n"
        "    if _left and (_target not in _ns or _ns[_target] != _want):\n"
        "        assert False, ('Use the box `' + _target + '`: `' + _left[0] + '` comes from the example.')\n"
        "    assert _target in _ns, ('Keep the box `' + _target + '` from the starter.' if _placeholder is not None\n"
        "                            else 'Make a box named `' + _target + '`: start a line with `' + _target + ' = `.')\n"
        "    _got = _ns[_target]\n"
        "    _was = globals().get(_target)\n"
        "    if type(_got).__name__ == 'str' and type(_want).__name__ == 'bool':\n"
        "        assert False, ('Take the quotes off: `' + _target + '` holds the text ' + _show(_got) + '. '\n"
        "                       '`True` and `False` have no quotes: they are Python' + chr(39) + 's yes and no.')\n"
        "    if _placeholder is not None and repr(_got) == repr(_placeholder) and _starters(_target, _placeholder):\n"
        "        _how = '`' + _target + '` still holds the starter' + chr(39) + 's `' + repr(_placeholder) + '`.'\n"
        "    else:\n"
        "        _how = ('`' + _target + '` ' + ('stayed ' if _got == _was else 'became ') + _show(_got) + ', not '\n"
        "                + _show(_want) + '.')\n"
        "    assert type(_got).__name__ == type(_want).__name__ and _got == _want, _mend(_tail, _how, _shown, _rolls, _again)\n"
    )
    if lean:
        code = _leaned(code, [("'Take the quotes off: `' + _target + '` holds the text '", "'`' + _target + '` holds the text '")])
    return (label, code)


_BND = r'''
_R, _N_name = __ROLL__, __NEEDED__
_via_rolls = __VIA_ROLLS__
_F = __FACES__
_N = globals().get(_N_name)
assert _N is not None, 'Keep the box `' + _N_name + '` from the starter, as `' + _N_name + ' = ` and a whole number.'
assert type(_N).__name__ == 'int', 'Give `' + _N_name + '` a whole number, with no quotes.'
if _via_rolls:
    assert 2 <= _N <= _F, ('Pick a `' + _N_name + '` from 2 to ' + str(_F) + ': a d' + str(_F) + ' roll is 1 to '
                           + str(_F) + '.')
    _lo, _hi = 1, _F
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
        assert _calls, ('Roll the die into `' + _R + '` with `random.randint(1, ' + str(_F) + ")`, so Mar'tu's check "
                        'can roll for you.')
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
    # The same words in both branches, or an `if` that never asks with the boxes (`if True:`, `if 14 >= 12:`, a
    # lone print): say only what is really wrong.
    _same = False
    for _n in _ast.walk(_ast.parse(_source)):
        if type(_n).__name__ == 'If' and _n.orelse:
            _w = [sorted(_c.value for _x in _b for _c in _ast.walk(_x) if type(_c).__name__ == 'Constant'
                         and type(_c.value).__name__ == 'str') for _b in (_n.body, _n.orelse)]
            _same = _same or bool(_w[0] and _w[0] == _w[1])
    assert not _same, ('Give the success line and the failure line different words: both say the same thing. '
                       + _ev_many([_lo, _hi]))
    assert False, ('Ask whether `' + _R + '` reaches `' + _N_name + '` after `if`, using the boxes, so the answer can '
                   'change. Both rolls printed the same line. ' + _ev_many([_lo, _hi]))
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
_M = _N + 3 if (not _via_rolls or _N + 3 <= _F) else _N - 3
_B2 = _try(_M - 1, _M)
_E2 = _try(_M, _M)
assert _B2 == _L and _E2 == _H, ('Ask with the box `' + _N_name + '`, not a number you typed. With `' + _N_name + ' = '
                                 + str(_M) + '`, your program ' + ('passed ' + _a_roll(_M - 1) if _B2 != _L else
                                 'failed ' + _a_roll(_M)) + ". (Mar'tu's check tried `" + _N_name + ' = ' + str(_M)
                                 + '`, only inside the check.)')
# With `needed` at the top face no roll can go past it, so `==` would hide: one more try, above the new needed.
if _M + 1 <= (_F if _via_rolls else _M + 1):
    _A2 = _try(_M + 1, _M)
    assert _A2 == _H, ('Use `>=`, so a roll that reaches `' + _N_name + '` or goes past it passes. '
                       + _a_roll(_M + 1)[0].upper() + _a_roll(_M + 1)[1:] + ' did not pass. ' + _ev(_M + 1, _M))
'''


_BND_LEAN = [
    ("""('Roll the die into `' + _R + '` with `random.randint(1, ' + str(_F) + ")`, so Mar'tu's check "
                        'can roll for you.')""", """("Mar'tu's check found no die rolled into `" + _R + '`, so it can not roll for you.')"""),
    ("""('Print a success line when `' + _R + '` reaches `' + _N_name + '`. Your program printed nothing. '""",
     """('A roll that reaches `' + _N_name + '` printed nothing. '"""),
    ("""'Add `else:` with a failure line under it. Your program printed nothing. '""", """'A low roll printed nothing. '"""),
    ("""('Use `>=`, so a higher roll passes too. Only a roll of exactly ' + str(_N) + ' gave the success '
                      'line. '""", """('Only a roll of exactly ' + str(_N) + ' gave the success line: a higher roll did not. '"""),
    ("""('Give the success line and the failure line different words: both say the same thing. '""",
     """('The success line and the failure line say the same thing. '"""),
    ("""('Ask whether `' + _R + '` reaches `' + _N_name + '` after `if`, using the boxes, so the answer can '
                   'change. Both rolls printed the same line. '""", """('Both rolls printed the same line, so the answer never changes. '"""),
    ("""('Put the failure line under `else:`, indented, so only one line prints. It '
                                           'printed the failure line as well as the success line. '""",
     """('A high roll printed the failure line as well as the success line. '"""),
    ("""('Indent the success line under the `if`, and the failure line under '
                                           '`else:`. It printed the success line as well as the failure line. '""",
     """('A low roll printed the success line as well as the failure line. '"""),
    ("""(('Use `>=`, so exactly enough passes: a roll of ' + str(_N) + ' or more gives the success line. It '
                   'gave the failure line. ' if _E == _L else
                   'Print the success line here, the same as for a high roll. ')""",
     """(('A roll of exactly ' + str(_N) + ' gave the failure line. ' if _E == _L else
                   'A roll of exactly ' + str(_N) + ' did not give the success line. ')"""),
    ("""(('Give a roll below `' + _N_name + '` the failure line. It gave the success line. ' if _B == _H else
                   'Print the failure line here, the same as for a low roll. ')""",
     """(('A roll below `' + _N_name + '` gave the success line. ' if _B == _H else
                   'A roll below `' + _N_name + '` did not give the failure line. ')"""),
    ("""'Print the success line here, the same as for a high roll. ' + _ev(_N + 1)""",
     """'A roll above `' + _N_name + '` did not give the success line. ' + _ev(_N + 1)"""),
    ("""('Ask with the box `' + _N_name + '`, not a number you typed. With `' + _N_name + ' = '""", """('With `' + _N_name + ' = '"""),
    ('\'failed \' + _a_roll(_M)) + ". (Mar\'tu\'s check tried `"',
     '\'failed \' + _a_roll(_M)) + \': the `if` does not follow the box `\' + _N_name + "`. (Mar\'tu\'s check tried `"'),
    ("""('Use `>=`, so a roll that reaches `' + _N_name + '` or goes past it passes. '""",
     """('A roll that goes past `' + _N_name + '` should pass too. '"""),
]


def bnd_check(label, roll, needed, via_rolls=False, setup="", faces=20, lean=False):
    """BND: exactly enough passes, one below fails, and the test follows the box `needed` (not a typed number).
    With via_rolls, Mar'tu's check scripts a d`faces` (u02b's check, with the die size as a parameter). `lean`:
    Quick Check 2's messages, the slip and the evidence without the fix."""
    code = _rerun_code(setup) + (
        _BND.replace("__ROLL__", repr(roll)).replace("__NEEDED__", repr(needed))
        .replace("__VIA_ROLLS__", repr(bool(via_rolls))).replace("__FACES__", repr(int(faces)))
    )
    return (label, _leaned(code, _BND_LEAN) if lean else code)


_RND = r'''
_target, _faces, _placeholder = __TARGET__, __FACES__, __PLACEHOLDER__
_ns, _rows, _calls, _err, _miss = _rerun({}, __ROLLS__)
assert not _err, _stop({}, __ROLLS__, _err)
_fix = '`' + _target + ' = random.randint(1, ' + str(_faces) + ')`'
assert _target in _ns, 'Keep the box `' + _target + '` from the starter, and roll it: ' + _fix + '.'
_got = _ns[_target]
# Python's own message for `=` in an `if` suggests `:=`, which quietly puts a new value in the box.
_walrus = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'NamedExpr'
           and type(_n.target).__name__ == 'Name' and _n.target.id == _target]
assert not _walrus, ('To ask a question in an `if`, use a sign like `>=` or `==`. `:=` puts a new value in `'
                     + _target + '`, the same as `=`, so it no longer holds the roll.')
_from = [_c for _c in _calls if _c[2] == _got]
assert not (_placeholder is not None and not _from and _starters(_target, _placeholder)), (
    'Roll it: ' + _fix + '. `' + _target + "` still holds the starter's `" + str(_placeholder) + '`.')
assert _assigned_from_expression(_target) and _calls, 'Roll it: ' + _fix + '. `' + _target + '` holds a number you typed.'
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


_RND_LEAN = [
    ("""'Keep the box `' + _target + '` from the starter, and roll it: ' + _fix + '.'""", """'Keep the box `' + _target + '` from the starter.'"""),
    ("""('To ask a question in an `if`, use a sign like `>=` or `==`. `:=` puts a new value in `'""", """('`:=` puts a new value in `'"""),
    ('\'Roll it: \' + _fix + \'. `\' + _target + "` still holds the starter\'s `"', '\'`\' + _target + "` still holds the starter\'s `"'),
    ("""'Roll it: ' + _fix + '. `' + _target + '` holds a number you typed.'""",
     """'`' + _target + '` holds a number you typed, so it is the same every Run.'"""),
    ("""'Roll it: ' + _fix + '. `' + _target + '` does not hold the roll yet.'""", """'`' + _target + '` does not hold the roll yet.'"""),
    ("""('Use ' + _fix + ': a d' + str(_faces) + ' has faces 1 to ' + str(_faces) + ', and `randint` includes both '
        'ends. ')""", """('A d' + str(_faces) + ' has faces 1 to ' + str(_faces) + ', but ')"""),
]


def rnd_check(label, target, faces, rolls, placeholder=None, lean=False):
    """RND: `target` holds the value of a scripted randint call, and that call was randint(1, faces).
    `rolls` are distinct values, so each box can be traced back to its own call. `placeholder`: the number the
    starter puts in the box (`telegun_roll = 0`), named as the starter's while that line is still there."""
    code = _rerun_code() + (
        _RND.replace("__TARGET__", repr(target)).replace("__FACES__", repr(faces)).replace("__ROLLS__", repr(list(rolls)))
        .replace("__PLACEHOLDER__", repr(placeholder))
    )
    return (label, _leaned(code, _RND_LEAN) if lean else code)


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
    elif __KEPT__:
        _msg = "Keep the box `__NAME__` from the starter: a line that starts `__NAME__ = `."
    else:
        _msg = "Make a box named `__NAME__`: start a line with `__NAME__ = `."
    assert False, _msg'''


def name_check(name, foreign=(), skip=(), kept=False):
    """NAME + LEFT + BARE: the box exists, or the message says why not. `skip` = boxes the starter already makes.
    `kept=True`: the starter makes this box too, so a missing one gets "Keep the box ... from the starter"."""
    code = (_NAME_TEMPLATE.replace("__NAME__", name).replace("__FOREIGN__", repr(list(foreign)))
            .replace("__SKIP__", repr(list(skip))).replace("__KEPT__", repr(bool(kept))))
    return (f"there is a box named {name}", code)


def strexact_check(wanted, label="the quoted text is exact", lean=False):
    """STREXACT: quoted text in a comparison differs from one of `wanted` only by capitals or spaces. Only text in
    a comparison counts, so a starter line like `choice = "Option 2"` (the capitals Mar'tu's check copes with) is
    left alone; so is a near miss compared next to the exact text (`== "option 2" or == "Option 2"`: that one is
    a capitals problem, for QC2 C2's `.lower()` step)."""
    return (
        label,
        "import ast as _ast\n"
        f"_wanted = {list(wanted)!r}\n"
        "def _squash(_s):\n"
        "    return _s.lower().replace(' ', '')\n"
        "_asked = [_c for _q in _ast.walk(_ast.parse(_source)) if type(_q).__name__ == 'Compare' "
        "for _c in [_q.left] + list(_q.comparators) if type(_c).__name__ == 'Constant']\n"
        "_texts = [_c.value for _c in _asked if type(_c.value).__name__ == 'str']\n"
        "_bad = [(_t, _w) for _t in _texts for _w in _wanted "
        "if _t != _w and _squash(_t) == _squash(_w) and _w not in _texts]\n"
        "assert not _bad, (" + ("" if lean else "'Copy the option exactly: ' + ") + "'`\"' + (_bad[0][0] if _bad else '') + '\"` and `\"' + "
        "(_bad[0][1] if _bad else '') + '\"` are different text to Python. Every letter, space and capital counts.')\n",
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



def check(label, *lines):
    """A check written as plain lines of code."""
    return (label, "\n".join(lines) + "\n")


def say(message):
    """A Python string literal for a student-facing message, for use inside check code."""
    return repr(message)


# ---- 2C-05: exactly enough, when mana is worked out (15 - 6) ----------------------------------

_ENOUGH = r'''
_CAST, _FAIL = __CAST__, __FAIL__
def _rows_for(_vals):
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [], _err)
    return _ns, _rows
def _said(_rows):
    if _CAST in _rows and _FAIL not in _rows:
        return 'cast'
    if _FAIL in _rows and _CAST not in _rows:
        return 'fail'
    return 'other'
def _ev(_vals, _m):
    return "(Mar'tu's check tried " + _with(_vals) + ', so `mana` was ' + str(_m) + ' at the `if`, only inside the check.)'
def _expect(_vals, _want, _fix, _what):
    _ns2, _rows2 = _rows_for(_vals)
    _m = _ns2.get('mana')
    _got = _said(_rows2)
    if _got == _want:
        return
    _line = _CAST if _want == 'cast' else _FAIL
    assert _got != 'other', ('Keep both lines as they are, and mend only the `if`. Your program did not print `'
                             + _line + '` on its own. ' + _ev(_vals, _m))
    assert False, _fix + ' ' + _what + ' ' + _ev(_vals, _m)
_ns, _rows = _rows_for({})
_M = _ns.get('mana')
assert _M is not None, 'Keep the box `mana` from the starter.'
assert type(_M).__name__ == 'int', 'Keep `mana` a whole number, as in the starter.'
_expect({'cost': _M}, 'cast', 'Use `>=`, which means *at least*: exactly enough mana should cast.',
        'Your program printed `' + _FAIL + '`')
_expect({'cost': _M + 1}, 'fail', 'Compare the boxes `mana` and `cost`: one short is not enough.',
        'Your program cast the ward.')
_expect({'cost': _M - 1}, 'cast', 'Let more than enough mana cast too.', 'Your program printed `' + _FAIL + '`')
_ns3, _rows3 = _rows_for({'mana': 20, 'cost': 99})
_M2 = _ns3.get('mana')
_expect({'mana': 20, 'cost': _M2}, 'cast', 'Ask with the boxes `mana` and `cost`, not numbers you typed.',
        'Exactly enough again, but your program said not enough.')
_expect({'mana': 20, 'cost': _M2 + 1}, 'fail', 'Ask with the boxes `mana` and `cost`, not numbers you typed.',
        'One short again, but your program cast the ward.')
'''


def enough_check(label, cast_line, fail_line):
    code = _rerun_code() + _ENOUGH.replace("__CAST__", repr(cast_line)).replace("__FAIL__", repr(fail_line))
    return (label, code)


_PRINTS_ABOVE = r'''import ast as _ast
_tree = _ast.parse(_source)
_ifs = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'If']
_at = _ifs[0] if _ifs else 10 ** 6
def _prints_of(_name):
    _found = []
    for _n in _ast.walk(_tree):
        if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == 'print':
            if any(type(_x).__name__ == 'Name' and _x.id == _name for _a in _n.args for _x in _ast.walk(_a)):
                _found.append(_n.lineno)
    return _found
def _sets_of(_name):
    # top-level lines above the `if` that put a value in the box (`=` or `-=`)
    _found = []
    for _n in _tree.body:
        if _n.lineno >= _at:
            continue
        _kind = type(_n).__name__
        if _kind == 'Assign' and any(type(_t).__name__ == 'Name' and _t.id == _name for _t in _n.targets):
            _found.append(_n.lineno)
        elif _kind == 'AugAssign' and type(_n.target).__name__ == 'Name' and _n.target.id == _name:
            _found.append(_n.lineno)
    return _found
for _name in __NAMES__:
    _p = _prints_of(_name)
    assert _p, 'Add `print(' + _name + ')` on its own line, just above the `if`, and Run.'
    assert min(_p) < _at, ('Move `print(' + _name + ')` above the `if`, so it shows the value before Python decides. '
                           'Now it is below the `if` line.')
    _last = max(_sets_of(_name) or [0])
    assert any(_last < _x < _at for _x in _p), ('Move `print(' + _name + ')` down, just above the `if`. It sits above '
                                               'line ' + str(_last) + ', which changes `' + _name + '`, so it shows the '
                                               'old value.')
'''


def prints_above(label, names):
    return (label, _PRINTS_ABOVE.replace("__NAMES__", repr(tuple(names))))


# ---- 2-A2: Mar'tu's seal (asserts that catch a broken check) --------------------------------------

_SEAL = r'''import ast as _ast
import io as _io
import sys as _sys
_target = __TARGET__
_tree0 = _ast.parse(_source)
_seals = [_n for _n in _ast.walk(_tree0) if type(_n).__name__ == 'Assert']
assert len(_seals) >= 3, ('Write one `assert` line under each `# seal:` comment: three in all. You have '
                          + str(len(_seals)) + (' seal.' if len(_seals) == 1 else ' seals.'))
_about = [_n for _n in _seals if any(type(_x).__name__ == 'Name' and _x.id == _target for _x in _ast.walk(_n.test))]
assert len(_about) >= 3, ('Make each seal say what `' + _target + '` must be, like `assert ' + _target
                          + ' == True`. ' + str(len(_about)) + ' of yours ' + ('is' if len(_about) == 1 else 'are')
                          + ' about `' + _target + '`.')
def _says_the_answer(_t):
    # `assert passed`, `assert not passed`, or `passed` compared with True / False (either side, any sign)
    _k = type(_t).__name__
    if _k == 'Name':
        return _t.id == _target
    if _k == 'UnaryOp' and type(_t.op).__name__ == 'Not':
        return type(_t.operand).__name__ == 'Name' and _t.operand.id == _target
    if _k == 'Compare' and len(_t.ops) == 1:
        _sides = [_t.left] + list(_t.comparators)
        return (any(type(_s).__name__ == 'Name' and _s.id == _target for _s in _sides)
                and any(type(_s).__name__ == 'Constant' and type(_s.value).__name__ == 'bool' for _s in _sides))
    return False
_plain = [_n for _n in _about if _says_the_answer(_n.test)]
assert len(_plain) >= 3, ('Make each seal say the answer for its roll, `True` or `False`, like `assert ' + _target
                          + ' == True`. A seal that copies the question `roll >= needed` only repeats the line above it.')
def _broken(_how):
    _tree = _ast.parse(_source)
    for _n in _ast.walk(_tree):
        if type(_n).__name__ == 'Assign' and any(type(_t).__name__ == 'Name' and _t.id == _target for _t in _n.targets):
            if _how == 'always':
                _n.value = _ast.copy_location(_ast.Constant(True), _n.value)
            elif type(_n.value).__name__ == 'Compare':
                _n.value.ops = [(_ast.Gt() if _how == 'gt' else _ast.Eq()) if type(_o).__name__ == 'GtE' else _o
                                for _o in _n.value.ops]
    _ast.fix_missing_locations(_tree)
    _keep_out, _buf = _sys.stdout, _io.StringIO()
    _sys.stdout = _buf
    _caught = False
    try:
        exec(compile(_tree, 'main.py', 'exec'), {'__name__': '__main__'})
    except AssertionError:
        _caught = True
    except Exception:
        _caught = True
    finally:
        _sys.stdout = _keep_out
    return _caught
_ev = " (Mar'tu's check broke your `" + _target + "` lines on purpose, only inside the check.)"
assert _broken('gt'), ('Seal the roll of exactly ' + __NEEDED__ + ': `' + _target + '` must be `True` there. None of '
                       'your seals noticed `>=` changed to `>`.' + _ev)
assert _broken('eq'), ('Seal a roll above ' + __NEEDED__ + ': `' + _target + '` must be `True` there too. None of your '
                       'seals noticed `>=` changed to `==`.' + _ev)
assert _broken('always'), ('Seal a roll below ' + __NEEDED__ + ': `' + _target + '` must be `False` there. None of '
                           'your seals noticed `' + _target + '` made always `True`.' + _ev)
'''


def seal_check(label, target, needed):
    return (label, _SEAL.replace("__TARGET__", repr(target)).replace("__NEEDED__", repr(str(needed))))


# ---- 2P2: the cheapest road ------------------------------------------------------------------------

_ROAD = r'''
_cases = __CASES__
# The fix for each road that should have won: always first in the message.
_tails = {
    'foot': 'Ask first: is `foot_cost` less than `jeep_cost`, *and* less than `telegun_cost`?',
    'jeep': 'Walk only when walking beats the jeep *and* the Telegun.',
    'telegun': 'Take the Telegun here: it is free on this roll.',
}
_names = {}
for _d, _r in _cases:
    _vals = {'distance': _d}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [_r])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [_r], _err)
    _f, _j, _t = _ns.get('foot_cost'), _ns.get('jeep_cost'), _ns.get('telegun_cost')
    _want = min(_f, _j, _t)
    _key = 'telegun' if _t == _want else ('jeep' if _j == _want else 'foot')
    _road, _cost = _ns.get('road'), _ns.get('cost')
    assert 'road' in _ns and 'cost' in _ns, 'Keep the boxes `road` and `cost` from the starter: each branch sets both.'
    _held = ("still holds the starter's `0`" if _cost == 0 and _starters('cost', 0) else 'holds ' + _show(_cost))
    assert _cost == _want, _mend(_tails[_key], '`cost` ' + _held + '; the cheapest is ' + str(_want) + '.', _vals, [_r])
    assert not (_road == '___' and _starters('road', '___')), ('Put the road' + chr(39) + 's name in `road`, in quotes, '
        'in each branch: `"on foot"`, `"the jeep"` or `"the Telegun"`. `road` still holds the starter' + chr(39)
        + 's `"___"`.')
    assert type(_road).__name__ == 'str' and _road.strip() and _road.strip() != '___', (
        'Put the road in `road`, as text in quotes, in each branch: `"on foot"`, `"the jeep"` or `"the Telegun"`.')
    if _key in _names:
        assert _road == _names[_key], _mend('Give each road one name, the same every time.', 'The '
            + ('walk' if _key == 'foot' else _key) + ' won again, but `road` held different text.', _vals, [_r])
    else:
        assert _road not in _names.values(), _mend('Give each branch its own road name.', '`road` held the same text '
            'as for another road.', _vals, [_r])
        _names[_key] = _road
'''


def road_check(label, cases):
    """cases = [(distance, telegun_roll), ...]: `cost` is the cheapest of the student's own three costs, and `road`
    names each road the same way every time (any text)."""
    return (label, _rerun_code() + _ROAD.replace("__CASES__", repr([tuple(c) for c in cases])))


_ROAD_PRINT = r'''
_runs = []
for _d, _r in __CASES__:
    _vals = {'distance': _d}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [_r])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [_r], _err)
    _runs.append((_vals, _r, str(_ns.get('road', '')), _ns.get('cost'), _rows))
_all = set(_x[2] for _x in _runs if _x[2])
for _vals, _r, _road, _cost, _rows in _runs:
    _ok = [_l for _l in _rows if _road and _road in _l and _re.search(_whole(_cost), _l)]
    assert _ok, _mend('Print the text in `road` and `str(cost)` in one line, glued with `+`.', 'No line showed both.',
                      _vals, [_r])
    # a line that lists every road and every cost does not tell the party which one the code picked
    _others = [_o for _o in _all if _o != _road and _o not in _road]
    assert any(not any(_o in _l for _o in _others) for _l in _ok), _mend('Tell the party only the road the code '
        'picked.', 'Your line names every road.', _vals, [_r])
'''


def road_print_check(label, cases):
    return (label, _rerun_code() + _ROAD_PRINT.replace("__CASES__", repr([tuple(c) for c in cases])))


_GLUG = r'''
for _d, _r, _want in __CASES__:
    _vals = {'distance': _d}
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [_r])
    assert not _err, _stop(_vals, [_r], _err)
    _cost = _ns.get('cost')
    if _want:
        assert 'Pack extra glug.' in _rows, _mend('Also print `Pack extra glug.` when `cost` is 150 or more: use `>=`.',
                                                 'The trip cost ' + str(_cost) + ' coins.', _vals, [_r])
    else:
        assert 'Pack extra glug.' not in _rows, _mend('Ask about `cost`: under 150, no `Pack extra glug.`', 'The trip '
                                                      'cost ' + str(_cost) + ' coins.', _vals, [_r])
'''


def glug_check(label, cases):
    return (label, _rerun_code() + _GLUG.replace("__CASES__", repr([tuple(c) for c in cases])))



# ---- Quick Check 2, C2 and C3 ---------------------------------------------------------------------------

_FROM_BOXES = r'''import ast as _ast
_target, _boxes, _fix, _placeholder = __TARGET__, __BOXES__, __FIX__, __PLACEHOLDER__
_tree = _ast.parse(_source)
def _sets(_n):
    return type(_n).__name__ == 'Assign' and any(type(_t).__name__ == 'Name' and _t.id == _target for _t in _n.targets)
_made = [_n for _n in _ast.walk(_tree) if _sets(_n)]
_two = [_n for _n in _made if len(_n.targets) > 1]
_also = [_t.id for _n in _two for _t in _n.targets if type(_t).__name__ == 'Name' and _t.id != _target]
_pre = _fix + ' ' if _fix else ''
assert not _two, (_pre + 'Your `' + _target + '` line has two `=` signs, so it puts a value in `'
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
assert not _still or _asked, _pre + '`' + _target + "` still holds the starter's `" + repr(_placeholder) + '`.'
assert not _made or _quoted or _asked, (_pre + '`' + _target + '` is made from values you typed, so it can never '
                                        'change when the boxes change.')
'''


def from_boxes_check(target, boxes, fix, label=None, placeholder=None):
    """u02b's check: `target` is not made with two `=` signs (`can_cast = mana = cost`), and it is worked out from
    the boxes, not from typed values (`can_cast = True`, `can_cast = 12 >= 9 and 9 >= 9`). `placeholder`: the
    starter's value for `target` (`False`); while it is still there, the message says so. `fix` comes first."""
    code = (_FROM_BOXES.replace("__TARGET__", repr(target)).replace("__BOXES__", repr(list(boxes)))
            .replace("__FIX__", repr(fix)).replace("__PLACEHOLDER__", repr(placeholder)))
    return (label or f"{target} is asked, not typed", code)


_GETS = r'''import ast as _ast
_target = __TARGET__
_asks = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr'
         and any(type(_q).__name__ == 'Compare' and type(_q.left).__name__ == 'Name' and _q.left.id == _target
                 and type(_q.ops[0]).__name__ == 'Eq' for _q in _ast.walk(_n.value))]
assert not _asks, ('Use one `=` to put the answer in `' + _target + '`: `=` puts, `==` only asks. Line '
                   + str(_asks[0] if _asks else 0) + ' asks a question and forgets the answer.')
'''


def gets_check(target, lean=False):
    """`can_cast == mana >= cost ...` on its own line: a question asked and thrown away (the `==` for `=` slip).
    It runs, so only a check can catch it."""
    code = _GETS.replace("__TARGET__", repr(target))
    if lean:
        code = _leaned(code, [("""('Use one `=` to put the answer in `' + _target + '`: `=` puts, `==` only asks. Line '
                   + str(_asks[0] if _asks else 0) + ' asks a question and forgets the answer.')""",
                               """('Line ' + str(_asks[0] if _asks else 0) + ' asks a question with `==` and forgets the '
                   'answer: `==` only asks.')""")])
    return (f"{target} gets the answer with =", code)


_BARRIER = r'''
_three = __LINES__
_base = __BASE__
_again = 'ran your code again with the starter' + chr(39) + 's numbers'
_order = ['S', 'M', 'C']
for _vals, _key, _fix in __CASES__:
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    _shown = _changed(_vals, _base)
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_shown, [], _err)
    _got = [_three[_k] for _k in _order if _three[_k] in _rows]
    assert _got, _mend('Keep the three lines from the starter as they are, one under each branch.', 'None of them '
                       'printed.', _shown, [], _again)
    assert len(_got) == 1, _mend('Use one chain, `if`, `elif`, `else`, so only one line prints.',
                                 'It printed all three.' if len(_got) == 3 else 'It printed two of them.', _shown, [],
                                 _again)
    assert _got[0] == _three[_key], _mend(_fix, _printed(_got[0]), _shown, [], _again)
'''


def barrier_check(label, lines, cases, base, lean=False):
    """QC2 C3: cast_spell's chain. `lines` = {'S': not skilled, 'M': not enough mana, 'C': cast}, all three fixed
    starter lines. cases = [(values, key, fix), ...]: after the rerun, exactly one of the three lines prints, and
    it is lines[key]. `fix` comes first in the message. `base` = the starter's values: the evidence names only the
    values a rerun changed."""
    code = (_rerun_code() + _BARRIER.replace("__LINES__", repr(dict(lines))).replace("__BASE__", repr(dict(base)))
            .replace("__CASES__", repr([(dict(v), k, f) for v, k, f in cases])))
    if lean:
        code = _leaned(code, [
            ("""_mend('Keep the three lines from the starter as they are, one under each branch.', 'None of them '
                       'printed.'""", """_mend('None of the three lines from the starter printed.', ''"""),
            ("""_mend('Use one chain, `if`, `elif`, `else`, so only one line prints.',""",
             """_mend('Only one of the three lines should print.',"""),
        ])
    return (label, code)


def lower_brackets_check(box, lean=False):
    """`.lower` with no `()` (it never runs, so `choice.lower == ...` is quietly False)."""
    return (
        "lower has its brackets",
        "import ast as _ast\n"
        "_tree = _ast.parse(_source)\n"
        "_called = [id(_n.func) for _n in _ast.walk(_tree) if type(_n).__name__ == 'Call']\n"
        "_raw = [_n.lineno for _n in _ast.walk(_tree) if type(_n).__name__ == 'Attribute' and _n.attr == 'lower' "
        "and id(_n) not in _called]\n"
        f"assert not _raw, '{'' if lean else f'Add `()`: `{box}.lower()`. '}Line ' + str(_raw[0] if _raw else 0) + ' has `.lower` with no "
        "`()`, so it never runs.'\n",
    )


_LOWER_KEPT = r'''
_box = __BOX__
_lone = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr'
         and type(_n.value).__name__ == 'Call' and type(_n.value.func).__name__ == 'Attribute'
         and _n.value.func.attr == 'lower']
for _vals, _want, _never in __CASES__:
    _ns, _rows, _calls, _err, _miss = _rerun(_vals, [])
    assert not _miss, _keep(_miss[0])
    assert not _err, _stop(_vals, [], _err)
    _ok = all(_w in _rows for _w in _want) and not any(_w in _rows for _w in _never)
    _what = ('`' + _want[0] + '` did not print.' if _want and _want[0] not in _rows else 'Another reply printed too.')
    if _lone:
        assert _ok, _mend('Keep the copy: `' + _box + ' = ' + _box + '.lower()`. Line ' + str(_lone[0]) + ' makes a '
                          'copy, then forgets it.', _what, _vals, [])
    assert _ok, _mend('Use `.lower()`, so any capitals get their reply.', _what, _vals, [])
'''


def lower_kept_check(label, box, cases, lean=False):
    """QC2 C2's quiet slip: any capitals get their reply. cases = [(values, must_print, must_not_print), ...]. A
    `.lower()` copy made and forgotten on its own line (`choice.lower()`: the box itself never changes) gets its
    own message."""
    code = (_rerun_code() + _LOWER_KEPT.replace("__BOX__", repr(box))
            .replace("__CASES__", repr([(dict(v), list(w), list(n)) for v, w, n in cases])))
    if lean:
        code = _leaned(code, [
            ("""_mend('Keep the copy: `' + _box + ' = ' + _box + '.lower()`. Line ' + str(_lone[0]) + ' makes a '
                          'copy, then forgets it.'""", """_mend('Line ' + str(_lone[0]) + ' makes a lower-case copy, then forgets it.'"""),
            ("""_mend('Use `.lower()`, so any capitals get their reply.'""", """_mend('A choice typed with capitals does not get its reply.'"""),
        ])
    return (label, code)


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of control-flow; must match u02a and u02b exactly)
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

# New terms only: Unit 1 defines error message, comment, variable and the rest; u02a/u02b define if, elif, else,
# indent, colon, block, branch, and, or, not, import, randint, match and the comparison terms.
GLOSSARY = [
    dict(
        term="traceback",
        aliases=["tracebacks", "full message"],
        plain=(
            "Python's full message when a program stops. Read the last line first: the error's name, then what "
            "went wrong. Above it, the message names the line where Python stopped."
        ),
        example='File "main.py", line 4\nNameError: name \'mana_cost\' is not defined',
    ),
    dict(
        term="SyntaxError",
        aliases=["syntax error", "syntax errors"],
        plain=(
            "Python could not read a line: a missing quote, bracket or colon, or a sign it does not know. Nothing "
            "runs until it is mended."
        ),
        example="if mana < 6\nSyntaxError: expected ':'",
    ),
    dict(
        term="NameError",
        aliases=["name error", "name errors"],
        plain=(
            "Python met a name that no line has made yet. Often a typo, a capital letter, missing quotes, or a box "
            "used before the line that makes it."
        ),
        example="print(mama)\nNameError: name 'mama' is not defined",
    ),
    dict(
        term="TypeError",
        aliases=["type error", "type errors"],
        plain=(
            "Two values that don't fit together, like text glued to a number. Turn the number into text with "
            "`str()`, or take the quotes off a number."
        ),
        example='print("Mana: " + 7)\nTypeError: can only concatenate str (not "int") to str',
    ),
    dict(
        term="bug",
        aliases=["bugs", "debug", "debugging", "quiet bug", "loud bug"],
        plain=(
            "A slip in the code. A loud bug stops Python with a message. A quiet bug runs, but gives a wrong "
            "answer: print the values to find it."
        ),
        example="print(mana)\nprint(cost)",
    ),
    dict(
        term="assert",
        aliases=["asserts", "seal", "seals"],
        plain=(
            "A line that says what must be true. If it is true, nothing happens. If it is not, Python stops "
            "with `AssertionError`."
        ),
        example="assert passed == True",
    ),
]


# =============================================================================================
# Project 2P2 "Three Roads to the Institute" (optional, 35 min)
# =============================================================================================

ROADS_STARTER = (
    "import random\n"
    "distance = 30\n"
    "\n"
    "# A. Rations on foot\n"
    "# Up to 10 miles: 8 coins. Up to 50 miles: 70 coins. Longer: 150 coins.\n"
    "foot_cost = 0\n"
    "\n"
    "# B. Gearshift's jeep form\n"
    "# 2 coins of starlode a mile, plus 5 coins to start.\n"
    "jeep_cost = 0\n"
    "\n"
    "# C. Lucky's Telegun\n"
    "# Roll a d20. On 15 or more, the jump is free.\n"
    "# Under 15, Lucky lands in a hedge: you walk anyway, plus 10 coins of glug.\n"
    "telegun_roll = 0\n"
    "telegun_cost = 0\n"
    "\n"
    "# D. Pick the cheapest road\n"
    "# If walking costs less than the jeep and less than the Telegun: walk.\n"
    "# Else, if the jeep costs less than the Telegun: take the jeep.\n"
    "# Else: take the Telegun.\n"
    "road = \"___\"\n"
    "cost = 0\n"
    "\n"
    "# E. Tell the party which road, and what it costs\n"
)

FOOT_CHAIN = (
    "if distance <= 10:\n"
    "    foot_cost = 8\n"
    "elif distance <= 50:\n"
    "    foot_cost = 70\n"
    "else:\n"
    "    foot_cost = 150\n"
)
JEEP_LINE = "jeep_cost = 2 * distance + 5\n"
TELEGUN_ROLL = "telegun_roll = random.randint(1, 20)\n"
TELEGUN_CHAIN = (
    "if telegun_roll >= 15:\n"
    "    telegun_cost = 0\n"
    "else:\n"
    "    telegun_cost = foot_cost + 10\n"
)
ROAD_CHAIN = (
    "if foot_cost < jeep_cost and foot_cost < telegun_cost:\n"
    "    road = \"on foot\"\n"
    "    cost = foot_cost\n"
    "elif jeep_cost < telegun_cost:\n"
    "    road = \"the jeep\"\n"
    "    cost = jeep_cost\n"
    "else:\n"
    "    road = \"the Telegun\"\n"
    "    cost = telegun_cost\n"
)
ROAD_PRINT = "print(\"Take \" + road + \": \" + str(cost) + \" coins.\")\n"


def _roads(foot=None, jeep=None, roll=None, telegun=None, choose=None, say_it=None, extra=""):
    """The project program with any of its parts filled in (None = the starter's placeholder)."""
    code = ROADS_STARTER
    if foot is not None:
        code = code.replace("foot_cost = 0\n", foot)
    if jeep is not None:
        code = code.replace("jeep_cost = 0\n", jeep)
    if roll is not None:
        code = code.replace("telegun_roll = 0\n", roll)
    if telegun is not None:
        code = code.replace("telegun_cost = 0\n", telegun)
    if choose is not None:
        code = code.replace("road = \"___\"\ncost = 0\n", choose)
    if say_it is not None:
        code = code + say_it
    return code + extra


ROADS_SOLUTION = _roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN, ROAD_PRINT)
ROADS_NAMES = ["distance", "foot_cost", "jeep_cost", "telegun_roll", "telegun_cost", "road", "cost", "str"]

# (distance, Telegun roll): 5 and 80 miles walk, 30 and 72 take the jeep, a roll of 15 or more jumps.
ROAD_CASES = [(5, 3), (30, 3), (80, 14), (30, 15), (72, 2), (5, 20), (80, 15), (51, 9)]

PROJECT_2P2 = dict(
    kind="project",
    id="three-roads",
    title="Three Roads to the Institute",
    optional=True,
    minutes=35,
    summary="Walk, ride Gearshift's jeep, or trust Lucky's Telegun? Work out each cost, then let the code pick the cheapest.",
    intro=(
        "Mar'tu needs more brass instruments from the old Institute. Three ways to get there:\n"
        "1. On foot: the party eats glug rations, more for a longer road.\n"
        "2. Gearshift's jeep form: 2 coins of starlode a mile, plus 5 coins to start.\n"
        "3. Lucky's Telegun: free on a good roll. On a roll under 15, Lucky lands in a hedge. Again.\n"
        "Nobody agrees how far it is. So the code must pick the cheapest road for any `distance`."
    ),
    martu=(
        "Five parts, in order: A, B, C, D, E. Each part has its comment in the editor.\n"
        "Work out what each road costs, then let the code choose. Mar'tu's check tries other distances and other "
        "rolls, so build every cost from the boxes, yes?\n"
        "I counted everything in coins. Starlode, glug, hedges. Everything."
    ),
    names=ROADS_NAMES,
    pair_talk=(
        "Pair talk: before part D, guess with your partner which road wins at 5, 30 and 80 miles. "
        "Then each of you checks it on your own screen."
    ),
    starter=ROADS_STARTER,
    checkpoints=[
        dict(
            id="rations-on-foot",
            text="A. Replace `foot_cost = 0` with an `if`/`elif`/`else` that sets `foot_cost` from `distance`, using the three tiers.",
            dictated=False,
            hints=[
                "Look at the comment under `# A`. Three tiers means `if`, then `elif`, then `else`. Exactly 10 miles "
                "is still *up to 10*.",
                "A tier chain with other numbers:\n```python\nif weight <= 2:\n    fee = 1\nelif weight <= 9:\n"
                "    fee = 4\nelse:\n    fee = 12\n```\nThe first true branch wins. So: first, the test that lets the "
                "fewest numbers through.",
                "Write `if distance <= 10:` and `foot_cost = 8` under it, indented. Then `elif distance <= "
                "50:` with 70, and `else:` with 150.",
            ],
            checks=[
                box_check("foot_cost follows the tiers", "foot_cost", foreign=["fee", "weight"], placeholder=0, cases=[
                    ({"distance": 5}, None, 8, "Ask `distance <= 10` first: first, the test that lets the fewest "
                     "numbers through."),
                    ({"distance": 10}, None, 8, "Use `<=`: exactly 10 miles is still up to 10, so 8 coins."),
                    ({"distance": 11}, None, 70, "Give 11 miles the middle tier: more than 10, so 70 coins."),
                    ({"distance": 50}, None, 70, "Use `<=`: exactly 50 miles is still up to 50, so 70 coins."),
                    ({"distance": 51}, None, 150, "Give longer than 50 miles 150 coins: that is the `else`."),
                    ({"distance": 80}, None, 150, "Give longer than 50 miles 150 coins: that is the `else`."),
                ]),
            ],
            pass_line="Oogrish: Eight coins of glug for a short walk. Steady, now.",
        ),
        dict(
            id="jeep-cost",
            text="B. Make `jeep_cost` from `distance`: 2 coins a mile, plus 5 to start.",
            dictated=False,
            hints=[
                "Look at the comment under `# B`. The cost changes with the miles, so build it from `distance`.",
                "Per mile, plus a start fee, with other names: `fare = 3 * stops + 2`. Python does `*` before `+`.",
                "Write `jeep_cost = 2 * distance + 5`.",
            ],
            checks=[
                box_check("jeep_cost follows the distance", "jeep_cost", foreign=["fare", "stops"], placeholder=0, cases=[
                    ({"distance": 5}, None, 15, "Build it from `distance`: 2 coins a mile for 5 miles is 10, plus 5 to "
                     "start."),
                    ({"distance": 30}, None, 65, "Build it from `distance`: 2 coins a mile, plus 5 to start."),
                    ({"distance": 80}, None, 165, "Build it from `distance`: 2 coins a mile, plus 5 to start."),
                    ({"distance": 12}, None, 29, "Build it from `distance`, so it works for any distance: 2 coins a mile, "
                     "plus 5 to start."),
                    ({"distance": 72}, None, 149, "Build it from `distance`, so it works for any distance: 2 coins a mile, "
                     "plus 5 to start."),
                ]),
            ],
            pass_line="Gearshift: Visor dims. Fuel math logged.",
        ),
        dict(
            id="telegun-roll",
            text="C. Roll a d20 into `telegun_roll`.",
            dictated=True,
            hints=[
                "Look under `# C`. `import random` is already at the top of the program.",
                "`random.randint(1, 6)` rolls a d6: lowest face first, then the highest. Both ends are included.",
                "Write `telegun_roll = random.randint(1, 20)`.",
            ],
            checks=[rnd_check("telegun_roll is a d20", "telegun_roll", 20, [7], placeholder=0)],
        ),
        dict(
            id="telegun-cost",
            text="C. Set `telegun_cost`: 0 on a roll of 15 or more, or `foot_cost` plus 10 on a lower roll.",
            dictated=False,
            hints=[
                "Two outcomes, so `if` and `else`. Exactly 15 still jumps. On a miss you walk anyway, so start from "
                "`foot_cost`.",
                "With other names: `if dice >= 4:` / `    toll = 0` / `else:` / `    toll = fare + 2`.",
                "Write `if telegun_roll >= 15:` with `telegun_cost = 0` under it. Then `else:` with "
                "`telegun_cost = foot_cost + 10`.",
            ],
            checks=[
                box_check("telegun_cost follows the roll", "telegun_cost", foreign=["toll", "dice"], placeholder=0, cases=[
                    ({"distance": 30}, [14], 80, "Use `foot_cost + 10` under 15: Lucky lands in a hedge, so you walk "
                     "anyway, plus 10 coins of glug."),
                    ({"distance": 30}, [15], 0, "Use `>=`: a roll of exactly 15 still jumps for free."),
                    ({"distance": 30}, [20], 0, "Make it 0 on a roll of 15 or more: the jump is free."),
                    ({"distance": 5}, [1], 18, "Build it from `foot_cost`, not a number you typed."),
                    ({"distance": 80}, [3], 160, "Build it from `foot_cost`: under 15, you walk anyway, plus 10."),
                    ({"distance": 80}, [16], 0, "Make it 0 on a roll of 15 or more: the jump is free."),
                ], show=["distance"]),
            ],
            pass_line="Lucky: Free travel. Mostly. What's in it for me? Not walking.",
        ),
        dict(
            id="pick-the-cheapest",
            text="D. Write an `if`/`elif`/`else` that puts the cheapest road in `road` and its cost in `cost`.",
            dictated=False,
            hints=[
                "Follow the three comments under `# D`. Each branch sets two boxes: `road` gets the road's name, in "
                "quotes, and `cost` gets that road's cost box.",
                "`and` is True only when both questions are True. With other names: `if a < b and a < c:` means *a "
                "is the smallest*.",
                "Each branch sets both boxes, indented under it: for the jeep, `road = \"the jeep\"` and then "
                "`cost = jeep_cost`. The `else:` has no question: it takes the Telegun.",
                "Start with `if foot_cost < jeep_cost and foot_cost < telegun_cost:`, then `elif jeep_cost < "
                "telegun_cost:`, then `else:`. Each branch sets `road` and `cost`.",
            ],
            checks=[road_check("the cheapest road wins", ROAD_CASES)],
            pass_line="Mar'tu: The code chooses. Nobody argues with the code. Except Lucky.",
        ),
        dict(
            id="tell-the-party",
            text="E. Print one line that shows the road and its cost.",
            dictated=False,
            hints=[
                "Glue the text in `road` and the number in `cost` into one line. A number needs `str()` first.",
                "With other names: `print(\"Buy \" + item + \" for \" + str(price) + \" coins.\")`.",
                "Write `print(\"Take \" + road + \": \" + str(cost) + \" coins.\")`.",
            ],
            checks=[road_print_check("the line shows the road and its cost", [(30, 3), (5, 15), (80, 14), (72, 2)])],
            pass_line="Mar'tu: Good. Pack the brass cart. We leave when the Clock allows.",
        ),
    ],
    solution=ROADS_SOLUTION,
    partials=[
        _roads(FOOT_CHAIN),
        _roads(FOOT_CHAIN, JEEP_LINE),
        _roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL),
        _roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN),
        _roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN),
    ],
    assemble=dict(
        lines=[line for line in ROADS_SOLUTION.splitlines() if line.strip() and not line.lstrip().startswith("#")],
        distractors=[
            "elif distance < 50:",
            "if foot_cost < jeep_cost or foot_cost < telegun_cost:",
            "jeep_cost = 65",
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The three roads, side by side",
            text=(
                "Costs in coins, with a Telegun roll under 15 (a hedge):\n"
                "```text\nmiles  walk  jeep  Telegun\n  5      8    15     18\n"
                " 30     70    65     80\n 80    150   165    160\n```\n"
                "On a roll of 15 or more, the Telegun column is 0, and it wins every time."
            ),
        ),
        dict(
            angle="step-by-step",
            label="One part at a time",
            text=(
                "1. A: three tiers, so `if`, `elif`, `else`. First, the test that lets the fewest numbers through.\n"
                "2. B: one line, built from `distance`.\n"
                "3. C: roll, then `if`/`else` on the roll.\n"
                "4. D: ask *is walking the smallest?*, then *is the jeep smaller than the Telegun?*, then `else`.\n"
                "5. E: glue `road` and `str(cost)` into one line."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "`cast_spell` in the barrier part picked one of three paths: not skilled enough, not enough mana, "
                "or cast. Python checked from the top and took the first true branch. Your road chooser works the "
                "same way."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Pack extra glug",
        text=(
            "Long trips make Lucky thirsty. After part E, if the trip costs 150 coins or more, also print "
            "`Pack extra glug.` Ask about `cost`, so it works for every road."
        ),
        hints=[
            "150 or more counts, so `>=`. A cost of 149 should stay quiet.",
            "At the end, write `if cost >= 150:` and `print(\"Pack extra glug.\")` under it, indented.",
        ],
        checks=[glug_check("extra glug on 150 coins or more", [(80, 14, True), (72, 2, False), (30, 3, False),
                                                                (80, 15, False)])],
        solution=ROADS_SOLUTION + "if cost >= 150:\n    print(\"Pack extra glug.\")\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet=(
            'if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:\n    ...\n'
            'elif caster["mana"] < spell["mana_cost"]:\n    ...\nelse:\n    ...'
        ),
        why=(
            "You have seen this shape. `cast_spell` asks one question, then another, then has an `else` for "
            "everything left. You just wrote the same shape for three roads, and joined two questions with `and`."
        ),
    ),
    takeaway="Pick the smallest of three: `if a < b and a < c:`, then `elif b < c:`, then `else:`.",
    wrong_answers=[
        dict(why="tiers with < (exactly 10 miles costs 70)", code=_roads(FOOT_CHAIN.replace("<=", "<")), fails_at=1,
             message_contains="Exactly 10 miles"),
        dict(why="tiers in the wrong order (the wide tier first)",
             code=_roads("if distance <= 50:\n    foot_cost = 70\nelif distance <= 10:\n    foot_cost = 8\nelse:\n"
                         "    foot_cost = 150\n"),
             fails_at=1, message_contains="fewest numbers through"),
        dict(why="the walk's cost typed for 30 miles", code=_roads("foot_cost = 70\n"), fails_at=1,
             message_contains="not 8"),
        dict(why="part A left as the starter's placeholder", code=_roads(), fails_at=1,
             message_contains="still holds the starter's `0`"),
        dict(why="the hint example's box (fee) copied instead of foot_cost",
             code=_roads(FOOT_CHAIN.replace("foot_cost", "fee")), fails_at=1, message_contains="comes from the example"),
        dict(why="the hint example's box (fare) copied, the placeholder kept",
             code=_roads(FOOT_CHAIN, "jeep_cost = 0\nfare = 2 * distance + 5\n"), fails_at=2,
             message_contains="comes from the example"),
        dict(why="elif without the else (long walks cost 0)",
             code=_roads("foot_cost = 0\nif distance <= 10:\n    foot_cost = 8\nelif distance <= 50:\n    foot_cost = 70\n"),
             fails_at=1, message_contains="else"),
        dict(why="else with a condition", code=_roads(FOOT_CHAIN.replace("else:", "else distance > 50:")),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the jeep's cost typed for 30 miles (65)", code=_roads(FOOT_CHAIN, "jeep_cost = 65\n"), fails_at=2,
             message_contains="Build it from"),
        dict(why="the start fee left out", code=_roads(FOOT_CHAIN, "jeep_cost = 2 * distance\n"), fails_at=2,
             message_contains="plus 5"),
        dict(why="the jeep's cost typed for the three spec distances only (5, 30, 80)",
             code=_roads(FOOT_CHAIN, "if distance == 5:\n    jeep_cost = 15\nelif distance == 30:\n    jeep_cost = 65\nelse:\n"
                         "    jeep_cost = 165\n"),
             fails_at=2, message_contains="any distance"),
        dict(why="walrus after Python's hint (:= puts 15 in telegun_roll)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL,
                         TELEGUN_CHAIN.replace("telegun_roll >= 15", "telegun_roll := 15")),
             fails_at=3, message_contains=":="),
        dict(why="the plus 5 inside the brackets", code=_roads(FOOT_CHAIN, "jeep_cost = 2 * (distance + 5)\n"),
             fails_at=2, message_contains="not 15"),
        dict(why="the Telegun never rolled (the starter's placeholder kept)", code=_roads(FOOT_CHAIN, JEEP_LINE),
             fails_at=3, message_contains="still holds the starter's `0`"),
        dict(why="a d19 for the Telegun", code=_roads(FOOT_CHAIN, JEEP_LINE, "telegun_roll = random.randint(1, 19)\n"),
             fails_at=3, message_contains="never gives 20"),
        dict(why="> 15 (a roll of exactly 15 lands in the hedge)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN.replace(">=", ">")), fails_at=4,
             message_contains="exactly 15"),
        dict(why="the hedge cost typed (80) instead of built from foot_cost",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN.replace("foot_cost + 10", "80")),
             fails_at=4, message_contains="not a number you typed"),
        dict(why="= instead of == style slip: = in the if", code=_roads(
            FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN.replace("telegun_roll >= 15", "telegun_roll = 15")),
             fails_at=0, message_contains="=="),
        dict(why="or instead of and (walking always wins)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN,
                         ROAD_CHAIN.replace(" and foot_cost", " or foot_cost")),
             fails_at=5, message_contains="beats the jeep *and*"),
        dict(why="the Telegun left out of the first question",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN,
                         ROAD_CHAIN.replace(" and foot_cost < telegun_cost", "")),
             fails_at=5, message_contains="free on this roll"),
        dict(why="> instead of < (the dearest road)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN.replace(" < ", " > ")),
             fails_at=5, message_contains="cheapest"),
        dict(why="an elif with no if above it",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN.replace("if foot_cost", "elif foot_cost", 1)),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="the same road name in two branches",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN.replace('"the jeep"', '"on foot"')),
             fails_at=5, message_contains="same text"),
        dict(why="the line typed in, not built from the boxes",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN,
                         "print(\"Take the jeep: 65 coins.\")\n"),
             fails_at=6, message_contains="str(cost)"),
        dict(why="the cost glued without str()",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN,
                         "print(\"Take \" + road + \": \" + cost + \" coins.\")\n"),
             fails_at=0, message_contains="concatenate"),
        dict(why="every road and cost printed in one line (the choice is never told)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN,
                         "print(\"on foot \" + str(foot_cost) + \", the jeep \" + str(jeep_cost) + \", the Telegun \" + "
                         "str(telegun_cost))\n"),
             fails_at=6, message_contains="names every road"),
        dict(why="the road's name in quotes (prints the word road)",
             code=_roads(FOOT_CHAIN, JEEP_LINE, TELEGUN_ROLL, TELEGUN_CHAIN, ROAD_CHAIN,
                         "print(\"Take road: \" + str(cost) + \" coins.\")\n"),
             fails_at=6, message_contains="the text in `road`"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="elif-chain,boundary,combine-values,randint,if-else,"
             "and-or-not,concat-str", solo="false", dictates="3", foreign_names="weight,fee,fare,stops,dice,toll,"
             "fare,a,b,c,item,price") + "\n"
        "Project 2P2 (O). Task-group headers A to E are in the starter, with placeholders (`foot_cost = 0` ...) and "
        "part D as three plain-words comments (S2), so the program always runs while a student works part by part. "
        "Everything is counted in coins so the three roads compare. Numbers: walk 8 / 70 / 150 coins (up to 10, up "
        "to 50, longer); jeep 2 * distance + 5 (odd, so it never ties a walk tier); Telegun 0 on 15 or more, "
        "foot_cost + 10 on a miss (so a missed jump never beats walking). Spec reruns 5, 30 and 80 miles pick the "
        "walk, the jeep and the walk on a missed jump; a roll of 15 or more (15 exactly, 20) picks the Telegun at 5, "
        "30 and 80; 72 and 51 miles test the jeep near the 150-coin tier. Tasks 1, 2 and 4 are CMB over distance "
        "and scripted rolls (BND at 10, 50 and a roll of exactly 15); task 3 is RND; task 5 compares `cost` with "
        "the smallest of the student's own three costs and needs one name per road (any text: lint e); task 6 "
        "reruns and looks for the text in `road` and the cost in one printed line, with no other road named in it "
        "(`65coins` without a space is accepted: digits-only boundaries). Jeep CMB adds 12 and 72 miles, so a chain "
        "typed for the spec's 5 / 30 / 80 fails. Tasks 1, 2 and 4 name the hint example's boxes (fee, fare, toll) "
        "as LEFT. Side quest: a 150-coin glug "
        "warning (BND at 149 / 150, on `cost`). Partials 1-5 pass tasks 1..k. Ruling pass: the starter's "
        "placeholders (`foot_cost = 0`, `telegun_roll = 0`, `cost = 0`, `road = \"___\"`) are named as the "
        "starter's in messages (WAs prove two); the tier order uses the one order rule ('first, the test that lets "
        "the fewest numbers through'); rung 0 stops before the sign or the `and` (`if distance `, `if foot_cost `)."
    ),
)


# =============================================================================================
# Mar'tu remembers... (2c-remembers)
# =============================================================================================

REMEMBERS_2C = dict(
    kind="quiz",
    id="2c-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from earlier lessons. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 2C; recall from 2B (randint includes both ends; a "
        "two-branch trace). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="can-it-give-six",
            q="Can `random.randint(1, 6)` give 6?",
            choices=["Yes", "No"],
            answer=0,
            why_wrong={1: "`randint` includes both ends. 6 is the top end, so it can come up, like on a real d6."},
            explain="Yes. `random.randint(1, 6)` gives 1, 2, 3, 4, 5 or 6. Both ends are included.",
            notes="2B-07 recall. Distractor: the top-excluded belief (range-style).",
        ),
        dict(
            type="predict",
            id="two-branch-trace",
            q="What will this print?",
            code=(
                "roll = 11\nneeded = 12\nif roll >= needed:\n    print(\"The latch pops open.\")\nelse:\n"
                "    print(\"That latch hates me.\")\n"
            ),
            choices=["The latch pops open.", "That latch hates me.", "The latch pops open.\nThat latch hates me."],
            answer="That latch hates me.",
            explain="11 is not at least 12, so Python skips the `if` part and runs the `else` part. Only one branch runs.",
            notes="2B-03 recall. Distractors: the wrong branch, and both branches running.",
        ),
    ],
)


# =============================================================================================
# Lesson 2C "When Spells Fizzle: Reading Errors"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 2C-01 anatomy-of-a-fizzle (Investigate, S3: read a traceback, record it in three boxes)
# ---------------------------------------------------------------------------------------------

FIZZLE_SPELL = (
    "hero = \"Bomb Shell\"\n"
    "mana = 12\n"
    "spell_cost = 5\n"
    "print(\"Mana left: \" + str(mana - mana_cost))\n"
    "print(hero + \" casts Shield.\")\n"
)
FIZZLE_NOTES_HEAD = (
    "\n"
    "# Your notes. Press Run, then fill these in while Python's message is on screen.\n"
    "# Then put # at the start of line 4 to switch it off, and Run again.\n"
)


def _fizzle(line="0", kind='""', name='""', spell=None, extra=""):
    spell = FIZZLE_SPELL.replace("print(\"Mana left", "# print(\"Mana left") if spell is None else spell
    return spell + FIZZLE_NOTES_HEAD + f"bad_line = {line}\nerror_type = {kind}\nmissing_name = {name}\n" + extra


FIZZLE_STARTER = _fizzle(spell=FIZZLE_SPELL)
FIZZLE_SOLUTION = _fizzle("4", '"NameError"', '"mana_cost"')
FIZZLE_KNOWN = ["hero", "mana", "spell_cost", "bad_line", "error_type", "missing_name"]


def _record_check(name, lines):
    return check(f"{name} holds what Python said", *lines)


BAD_LINE_CHECKS = [
    name_check("bad_line", skip=FIZZLE_KNOWN, kept=True),
    _record_check("bad_line", [
        "_v = bad_line",
        "assert type(_v).__name__ != 'str', " + say(
            "Take the quotes off: a line number is a number. `bad_line` holds text, because of the quotes."),
        "assert type(_v).__name__ == 'int', " + say("Give `bad_line` a whole number, with no quotes."),
        "assert _v != 0, " + say(
            "Put the line number from Python's message in `bad_line`: look for the word `line` and a number. "
            "`bad_line` still holds the starter's `0`."),
        "assert _v == 4, " + say("Find `line` in Python's message, and the number after it. `bad_line` holds ") + " + str(_v) + " + say(
            ", but Python stopped on another line."),
    ]),
]

ERROR_TYPE_CHECKS = [
    name_check("error_type", skip=FIZZLE_KNOWN, kept=True),
    _record_check("error_type", [
        "_v = error_type",
        "assert _v is not NameError, " + say(
            "`NameError` without quotes is Python's own name for that error. Write the words in quotes: "
            "`\"NameError\"`."),
        "assert type(_v).__name__ == 'str', " + say("Give `error_type` text, in quotes."),
        "_t = _v.strip().strip(chr(39) + chr(34) + ':').strip()",
        "assert _t, " + say("Copy the error's name from the last line of Python's message, between the quotes. "
                            "`error_type` still holds the starter's empty quotes."),
        "assert 'defined' not in _t, " + say(
            "That is the whole last line. The error's name is only the first word, before the `:`."),
        "assert _t != 'mana_cost', " + say(
            "`mana_cost` is the name Python could not find. The error's name is the first word of the last line, "
            "before the `:`."),
        "assert not (' ' in _t and _t.replace(' ', '').lower() == 'nameerror'), " + say(
            "Python writes the error's name as one word, with no space: `NameError`. Every space counts."),
        "assert _t.lower() == 'nameerror', " + say(
            "Python's last line starts with the error's name, then a `:`. Copy that first word into the quotes."),
        "assert _t == 'NameError', " + say("Copy the name exactly as Python writes it: `NameError`, with two capitals."),
    ]),
]

MISSING_NAME_CHECKS = [
    name_check("missing_name", skip=FIZZLE_KNOWN, kept=True),
    _record_check("missing_name", [
        "_v = missing_name",
        "assert type(_v).__name__ == 'str', " + say("Give `missing_name` text, in quotes."),
        "_t = _v.strip().strip(chr(39) + chr(34)).strip()",
        "assert _t, " + say("Copy the name from Python's last line, between the quotes. `missing_name` still holds the "
                            "starter's empty quotes."),
        "assert _t.lower() != 'nameerror', " + say(
            "That is the error's name. This box wants the name Python could not find: it sits inside the little "
            "`'` marks."),
        "assert _t != 'spell_cost', " + say(
            "`spell_cost` is the box the spell really has. Which name could Python not find? It sits inside the "
            "little `'` marks in the last line."),
        "assert not ('mana_cost' in _t and _t != 'mana_cost'), " + say(
            "Put only the name in the box, without the words around it."),
        "assert _t.lower() != 'mana_cost' or _t == 'mana_cost', " + say(
            "Copy the name exactly as Python writes it. Capitals count."),
        "assert _t == 'mana_cost', " + say(
            "Python's last line says `name '...' is not defined`. Copy the name between the little `'` marks."),
    ]),
]

ANATOMY_OF_A_FIZZLE = dict(
    id="anatomy-of-a-fizzle",
    title="Anatomy of a fizzle",
    martu=(
        "When a spell fizzles, Python leaves you a note. The full note is a [[traceback]]. It looks scary. It is "
        "not. Three parts matter:\n"
        "1. The last line: the error's name, then what went wrong.\n"
        "2. The line number: where Python stopped.\n"
        "3. The name or mark it is talking about.\n"
        "Run Bomb Shell's spell. It fizzles on purpose. While the note is still on screen, write down what it "
        "says, in three boxes. Then switch line 4 off with `#` and Run again, so the rest can run. Good practice "
        "for boxes, too."
    ),
    names=["bad_line", "error_type", "missing_name"],
    predict=dict(
        q="Bomb Shell's spell has five lines. What happens when you press Run?",
        choices=[
            "Mana left: 7\nBomb Shell casts Shield.",
            "Bomb Shell casts Shield.",
            "ERROR: name 'mana_cost' is not defined",
        ],
        answer=2,
        explain=(
            "Python stops at line 4. No line made a box called `mana_cost` (the spell's box is `spell_cost`). "
            "Python does not guess, and it does not skip the line: line 5 never runs."
        ),
    ),
    starter=FIZZLE_STARTER,
    checkpoints=[
        dict(
            id="record-the-line",
            text="Make `bad_line` hold the line number that Python's message names.",
            dictated=False,
            hints=[
                "Look for the word `line` in Python's message, still on screen. The number after it is where Python "
                "stopped. Message gone? Take the `#` off line 4 and Run.",
                "In `File \"main.py\", line 9`, the line number is 9. A line number is a number, so no quotes.",
                "Write `bad_line = 4`: Python's message says `line 4`.",
            ],
            checks=BAD_LINE_CHECKS,
        ),
        dict(
            id="record-the-type",
            text="Make `error_type` hold the error's name, as text.",
            dictated=False,
            hints=[
                "Read the last line first. The error's name comes before the `:`.",
                "In `ZeroDivisionError: division by zero`, the error's name is `ZeroDivisionError`. Text goes in quotes.",
                "Write `error_type = \"NameError\"`: the first word of the last line, in quotes.",
            ],
            checks=ERROR_TYPE_CHECKS,
        ),
        dict(
            id="record-the-name",
            text="Make `missing_name` hold the name Python could not find, as text.",
            dictated=False,
            hints=[
                "The last line says `name '...' is not defined`. The name is between the little `'` marks.",
                "In `name 'shield' is not defined`, the missing name is `shield`. Copy it letter for letter.",
                "Write `missing_name = \"mana_cost\"`: the name between the little `'` marks, in quotes.",
            ],
            checks=MISSING_NAME_CHECKS,
            pass_line="Mar'tu: Line, name of the error, the name it could not find. You read the whole note. Good.",
        ),
    ],
    solution=FIZZLE_SOLUTION,
    partials=[
        _fizzle("4"),
        _fizzle("4", '"NameError"'),
    ],
    assemble=dict(
        lines=[line for line in FIZZLE_SOLUTION.splitlines() if line.strip() and not line.startswith("# ")],
        distractors=["error_type = NameError", "bad_line = \"4\"", "missing_name = \"spell_cost\""],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The note, with labels",
            text=(
                "1. The last line, read it first: `NameError: name 'mana_cost' is not defined`. The first word, "
                "`NameError`, is the error's name.\n"
                "2. Above it: `File \"main.py\", line 4`. That is the line where Python stopped.\n"
                "3. Inside the little `'` marks: `mana_cost`, the name Python could not find."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Where to look, in order",
            text=(
                "1. Read the last line first: the error's name, then what went wrong.\n"
                "2. Then look at the line it names.\n"
                "3. On that line, find the name or mark the message talks about."
            ),
        ),
        dict(
            angle="everyday",
            label="A note on the door",
            text=(
                "It is like a note from a courier: *Could not deliver on line 4: nobody called mana_cost lives "
                "here.* The courier is not angry. The note says where, and what was missing."
            ),
        ),
        dict(angle="shorter", text="Last line: the error's name and the missing name. Full message: the line number."),
    ],
    pair_talk=(
        "Pair talk: point at the three parts of the message on your own screen, and tell your partner what each "
        "part says. Then each of you fills in your own notes."
    ),
    bonus=dict(
        by="bomb-shell",
        title="Log it",
        text=(
            "Bomb Shell keeps a fizzle log. Under your notes, print one line built from your three boxes, like "
            "`Line 4: NameError (mana_cost)`."
        ),
        hints=[
            "Glue the parts with `+`. `bad_line` is a number, so it needs `str()`. Add `\" (\"` and `\")\"` around the name.",
            "Write `print(\"Line \" + str(bad_line) + \": \" + error_type + \" (\" + missing_name + \")\")`.",
        ],
        checks=[
            lines_check("the log line is built from the boxes", [
                ({}, None, ["Line 4: NameError (mana_cost)"], [],
                 "Glue the three boxes: `\"Line \" + str(bad_line) + \": \" + error_type + \" (\" + missing_name + \")\"`."),
                ({"bad_line": 9, "error_type": "TypeError", "missing_name": "shield"}, None,
                 ["Line 9: TypeError (shield)"], [], "Build the line from the three boxes, so it follows them."),
            ]),
        ],
        solution=FIZZLE_SOLUTION + "print(\"Line \" + str(bad_line) + \": \" + error_type + \" (\" + missing_name + \")\")\n",
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='party.move("left")',
        why=(
            "You have seen notes like this. At the cabin door, leave the quotes off and write `party.move(left)`, "
            "and Python stops with the same kind of note: `NameError: name 'left' is not defined`. Same three "
            "parts: the error's name, the line, the name it could not find."
        ),
    ),
    takeaway="Read the last line first: the error's name, then what went wrong. The full message names the line.",
    wrong_answers=[
        dict(why="the starter: the spell fizzles on line 4", code=FIZZLE_STARTER, fails_at=0, message_contains="mana_cost"),
        dict(why="notes filled in, but line 4 not switched off", code=_fizzle("4", '"NameError"', '"mana_cost"', spell=FIZZLE_SPELL),
             fails_at=0, message_contains="mana_cost"),
        dict(why="line 4 switched off, the notes still the starter's (nothing read yet)", code=_fizzle(), fails_at=1,
             message_contains="still holds the starter's `0`"),
        dict(why="the line number in quotes", code=_fizzle('"4"'), fails_at=1, message_contains="number"),
        dict(why="the next line's number", code=_fizzle("5"), fails_at=1, message_contains="another line"),
        dict(why="NameError without quotes (runs silently)", code=_fizzle("4", "NameError"), fails_at=2,
             message_contains="quotes"),
        dict(why="the whole last line copied", code=_fizzle("4", "\"name 'mana_cost' is not defined\""), fails_at=2,
             message_contains="whole last line"),
        dict(why="the missing name in the error_type box", code=_fizzle("4", '"mana_cost"'), fails_at=2,
             message_contains="first word"),
        dict(why="lower-case error name", code=_fizzle("4", '"nameerror"'), fails_at=2, message_contains="capitals"),
        dict(why="the error's name split in two (the `Fire ball` slip)", code=_fizzle("4", '"Name Error"'), fails_at=2,
             message_contains="one word"),
        dict(why="the box that exists, not the missing one", code=_fizzle("4", '"NameError"', '"spell_cost"'), fails_at=3,
             message_contains="not find"),
        dict(why="the missing name without quotes", code=_fizzle("4", '"NameError"', "mana_cost"), fails_at=0,
             message_contains="mana_cost"),
        dict(why="the error's name in the missing_name box", code=_fizzle("4", '"NameError"', '"NameError"'), fails_at=3,
             message_contains="error's name"),
        dict(why="the missing name left as the starter's empty quotes", code=_fizzle("4", '"NameError"'), fails_at=3,
             message_contains="starter's empty quotes"),
        dict(why="the missing name with a capital", code=_fizzle("4", '"NameError"', '"Mana_cost"'), fails_at=3,
             message_contains="Capitals"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="read-traceback,make-variable,numbers-vs-text", solo="false",
             dictates="", foreign_names="shield,ZeroDivisionError") + "\n"
        "2C-01 (I). The starter is the five-line spell (NameError on `mana_cost`, line 4; verified: no 'Did you "
        "mean' suggestion) above the three note boxes. A crash stops the checks, so the notes say: Run, fill the "
        "notes in while Python's message is still on screen, then switch line 4 off with `#` and Run again (Unit "
        "1's cheatsheet: 'Put # in front of a line to switch it off'). Time (teacher ruling): the note stays on "
        "screen while the boxes are filled, so nobody has to undo the `#` to read it again. The starter's `0` and "
        "empty quotes are named as the starter's. Mending "
        "line 4 to `spell_cost` instead also works (checked by hand: it passes every checkpoint). Checks: NUM "
        "(`bad_line = \"4\"`), the TEXT special case (`error_type = NameError` runs silently because NameError is a "
        "builtin: G2 R14), and TEXT with the real slips (the whole last line, the box that exists, the error's name "
        "in the wrong box, case). Python's own `'` marks around the name are accepted (stripped): the skill is "
        "reading, not typing. The prediction shows Python stopping instead of guessing or skipping the line."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2C-05 no-error-wrong-answer (Debug/Investigate: print the values, then mend the boundary)
# ---------------------------------------------------------------------------------------------

CAST_LINE = "Oogrish casts Lantern Ward."
LOW_LINE = "Not enough mana."


def _ward(sign=">", prints=False, mana="15", cost="9", where="above"):
    show = "print(mana)\nprint(cost)\n"
    return (
        f"mana = {mana}\n"
        "mana = mana - 6    # Oogrish lit the lanterns earlier\n"
        f"cost = {cost}    # Lantern Ward\n"
        + (show if prints and where == "above" else "")
        + f"if mana {sign} cost:\n"
        f"    print(\"{CAST_LINE}\")\n"
        + ("    print(mana)\n    print(cost)\n" if prints and where == "inside" else "")
        + "else:\n"
        f"    print(\"{LOW_LINE}\")\n"
    )


WARD_STARTER = _ward()
WARD_SOLUTION = _ward(">=", prints=True)

NO_ERROR_WRONG_ANSWER = dict(
    id="no-error-wrong-answer",
    title="No error, wrong answer",
    martu=(
        "No message this time. The code runs. It just gives the wrong answer.\n"
        "Oogrish has exactly enough mana for Lantern Ward, and the ward does not go up. A quiet [[bug]].\n"
        "When there is no message to read, make Python show you the values. Print them, look, then mend."
    ),
    names=["mana", "cost"],
    predict=dict(
        q="Oogrish starts with 15 mana and spends 6. Lantern Ward costs 9. What will this print?",
        choices=[CAST_LINE, LOW_LINE, "ERROR: the mana is wrong"],
        answer=1,
        explain=(
            "15 - 6 is 9, and the ward costs 9. But `9 > 9` is False: 9 is not *more than* 9. So Python runs the "
            "`else`. No error, wrong answer."
        ),
    ),
    starter=WARD_STARTER,
    checkpoints=[
        dict(
            id="show-the-values",
            text="Add `print(mana)` and `print(cost)` just above the `if`, then Run and read the two numbers.",
            dictated=True,
            hints=[
                "Read the last line your program printed: `Not enough mana.` No error, so Python can't tell you why. "
                "The values can.",
                "The prints go on new lines just above `if mana > cost:`, with no spaces in front, so they run before "
                "Python decides.",
                "Printing a box shows what is inside it right now: `print(gold)` shows `12` if `gold` holds 12.",
            ],
            checks=[prints_above("print(mana) and print(cost) are above the if", ["mana", "cost"])],
            pass_line="Mar'tu: 9 and 9. Exactly enough. So why no ward? Look at the sign.",
        ),
        dict(
            id="mend-the-sign",
            text="Mend the `if`, so exactly enough mana casts the ward.",
            dictated=False,
            hints=[
                "Read what your program printed: 9, then 9, then `Not enough mana.` Is that the right answer?",
                "Look at the sign in the `if`. Which sign says *at least*, so 9 against 9 passes?",
                "`>` leaves out the boundary; `>=` includes it. `4 > 4` is False, but `4 >= 4` is True.",
            ],
            checks=[enough_check("exactly enough mana casts", CAST_LINE, LOW_LINE)],
            pass_line="Oogrish: The ward holds. Steady, now. Printing the values found it.",
        ),
    ],
    solution=WARD_SOLUTION,
    partials=[_ward(">", prints=True)],
    assemble=dict(
        lines=["mana = 15", "mana = mana - 6", "cost = 9", "print(mana)", "print(cost)", "if mana >= cost:",
               f"    print(\"{CAST_LINE}\")", "else:", f"    print(\"{LOW_LINE}\")"],
        distractors=["if mana > cost:", "if mana == cost:", "if mana >= 9:"],
    ),
    another_way=[
        dict(
            angle="why",
            label="Why does this work? Print-debugging",
            text=(
                "Printing the values is a real technique. Real programmers do it every day. When the code runs "
                "but the answer is wrong, the values tell you which line to doubt."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Hunt a quiet bug",
            text=(
                "1. Print the values just before the line that decides: here, the `if`.\n"
                "2. Do the question by hand: is 9 > 9? No.\n"
                "3. Should it be yes? Exactly enough should cast. So the sign is the bug."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The barrier part said it plainly: use `<` and not `<=`, because a caster with exactly enough mana "
                "can still cast. Same boundary, seen from the other side."
            ),
        ),
        dict(angle="shorter", text="No error? Print the values. 9 and 9 should cast, so use `>=`."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "You have seen this boundary. `cast_spell` used `<`, not `<=`, so a caster with exactly enough mana "
            "still casts. When a cast fails with no error, print the mana and the cost: the values show the "
            "boundary."
        ),
    ),
    takeaway="No error but a wrong answer? Print the values just before the line that decides.",
    wrong_answers=[
        dict(why="starter unchanged (no prints yet)", code=WARD_STARTER, fails_at=1, message_contains="print(mana)"),
        dict(why="prints added, > kept (the quiet bug)", code=_ward(">", prints=True), fails_at=2,
             message_contains="Exactly enough"),
        dict(why="prints put inside the if", code=_ward(">=", prints=True, where="inside"), fails_at=1,
             message_contains="below"),
        dict(why="== instead of >=", code=_ward("==", prints=True), fails_at=2, message_contains="More than enough"),
        dict(why="the campaign's < copied", code=_ward("<", prints=True), fails_at=2, message_contains="Exactly enough"),
        dict(why="a number typed in the if", code=_ward(">=", prints=True).replace("if mana >= cost", "if mana >= 9"),
             fails_at=2, message_contains="Compare the boxes"),
        dict(why="the cost lowered to dodge the bug", code=_ward(">", prints=True, cost="8"), fails_at=2,
             message_contains="Exactly enough"),
        dict(why="the mana raised to dodge the bug", code=_ward(">", prints=True, mana="16"), fails_at=2,
             message_contains="Exactly enough"),
        dict(why="=> instead of >=", code=_ward("=>", prints=True), fails_at=0, message_contains="invalid syntax"),
        dict(why="print(mana) put above `mana = mana - 6` (it shows 15, not the 9 the if sees)",
             code=_ward(">=").replace("mana = mana - 6", "print(mana)\nmana = mana - 6").replace(
                 "if mana", "print(cost)\nif mana"),
             fails_at=1, message_contains="old value"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="boundary,read-traceback", solo="false", dictates="1",
             foreign_names="gold") + "\n"
        "2C-05 (D/I, SC). The bug is quiet: the code runs and prints `Not enough mana.` with exactly enough mana. "
        "Mana is worked out (15 - 6), so printing it really shows something new. Two checkpoints, one action each "
        "(the spec's 'add the prints, then fix the comparison'): CP1 checks print(mana) and print(cost) sit above "
        "the `if` and below the last line that changes each box (a print above `mana = mana - 6` shows 15, not "
        "the 9 the `if` sees); CP2 is BND on `cost` around the student's own final mana (exact, one short, one over), then "
        "again with `mana = 20`, so typed numbers and dodges (cost 8, mana 16) fail. The two printed lines are "
        "fixed starter text, so the check can tell cast from not-cast even if a branch is flipped (`<`). WT: "
        "print-debugging is a real technique (another_way 'why'). A quiet bug has no Python message, so rung 0 is "
        "'read what your program printed' in both steps."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2C-06 equals-is-not-def (Debug: def used to make a box)
# ---------------------------------------------------------------------------------------------

NOT_DEF_STARTER = "def hero = \"Lucky\"\nprint(hero + \" is ready.\")\n"
NOT_DEF_SOLUTION = "hero = \"Lucky\"\nprint(hero + \" is ready.\")\n"

EQUALS_IS_NOT_DEF = dict(
    id="equals-is-not-def",
    title="`=` is not `def`",
    martu=(
        "You have seen `def` in the campaign, at the very first door: `def move_left():`. It is a big word, so it "
        "feels like the word for making things.\n"
        "`def` is for making recipes. We start those next unit. A box needs only `=`."
    ),
    example="snack = \"glug\"\nprint(snack + \" is ready.\")\n",
    example_output="glug is ready.",
    names=["hero"],
    starter=NOT_DEF_STARTER,
    checkpoints=[
        dict(
            id="make-hero",
            text="Make `hero` a box that holds `\"Lucky\"`.",
            dictated=True,
            hints=[
                "Read Python's last line: `expected '('`. After `def`, Python expects a recipe, not a box.",
                "Look at line 1. One word is extra. A box is a name, `=`, and a value.",
                "A box with other names: `snack = \"glug\"`. No `def`, and no brackets around the name.",
                "Change line 1 to `hero = \"Lucky\"`, with no `def`.",
            ],
            checks=[
                name_check("hero", foreign=["snack"]),
                check(
                    "hero holds text",
                    "_v = hero",
                    "assert not callable(_v), " + say(
                        "To make a box, write `hero = \"Lucky\"`. `hero` is a recipe made with `def`, not a box."),
                    "assert type(_v).__name__ == 'str', " + say("Give `hero` text, in quotes: `\"Lucky\"`."),
                    "assert _v.strip(), " + say("Put the name between the quotes. `hero` holds empty quotes."),
                ),
            ],
            pass_line="Lucky: Lucky is ready. Obviously.",
        ),
    ],
    solution=NOT_DEF_SOLUTION,
    assemble=dict(
        lines=["hero = \"Lucky\"", "print(hero + \" is ready.\")"],
        distractors=["def hero = \"Lucky\"", "\"hero\" = \"Lucky\"", "hero = Lucky"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Box or recipe?",
            text=(
                "1. `hero = \"Lucky\"` is a box: a name, `=`, a value.\n"
                "2. `def move_left():` is a recipe: `def`, a name, `()` and `:`.\n"
                "Next unit you write recipes. Today, only boxes."
            ),
        ),
        dict(angle="everyday", text="A label on a jar needs no instructions. `def` is for writing instructions."),
        dict(angle="shorter", text="A box: `name = value`. No `def`."),
    ],
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet="def move_left():\n    party.move(\"left\")",
        why=(
            "You have seen this. `def move_left():` made a recipe the arrow keys could call. Next unit you write "
            "your own recipes, and then it will make sense. A box never needs `def`."
        ),
    ),
    takeaway="A box is `name = value`. `def` is only for recipes.",
    wrong_answers=[
        dict(why="the starter: def to make a box", code=NOT_DEF_STARTER, fails_at=0, message_contains="expected '('"),
        dict(why="def with brackets around the value", code="def hero = (\"Lucky\")\nprint(hero + \" is ready.\")\n",
             fails_at=0, message_contains="expected"),
        dict(why="def with the name in quotes", code="def (\"hero\") = \"Lucky\"\nprint(hero + \" is ready.\")\n",
             fails_at=0, message_contains="invalid syntax"),
        dict(why="the name in quotes", code="\"hero\" = \"Lucky\"\nprint(hero + \" is ready.\")\n", fails_at=0,
             message_contains="literal"),
        dict(why="the value without quotes", code="hero = Lucky\nprint(hero + \" is ready.\")\n", fails_at=0,
             message_contains="Lucky"),
        dict(why="== instead of =", code="hero == \"Lucky\"\nprint(hero + \" is ready.\")\n", fails_at=0,
             message_contains="not defined"),
        dict(why="a dash for =", code="hero - \"Lucky\"\nprint(hero + \" is ready.\")\n", fails_at=0,
             message_contains="not defined"),
        dict(why="a capital H", code="Hero = \"Lucky\"\nprint(Hero + \" is ready.\")\n", fails_at=1,
             message_contains="letter for letter"),
        dict(why="the example's name", code="snack = \"Lucky\"\nprint(snack + \" is ready.\")\n", fails_at=1,
             message_contains="example"),
        dict(why="an unclosed quote", code="hero = \"Lucky\nprint(hero + \" is ready.\")\n", fails_at=0,
             message_contains="unterminated"),
        dict(why="the value on its own, with no box (a variable is just its value)",
             code="\"Lucky\"\nprint(\"Lucky\" + \" is ready.\")\n", fails_at=1, message_contains="no box"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="make-variable", solo="false", dictates="1",
             foreign_names="snack") + "\n"
        "2C-06 (D). The starter `def hero = \"Lucky\"` is unparseable on purpose (the harness warns about the "
        "starter; the site's explainer has the def-makes-functions row). Inoculates against Unit 3's def-heavy "
        "starters reactivating A-02's belief (`def (\"character\")`). WA evidence: def with the name in quotes "
        "(A-02), a dash for = (A-04). Checks NAME + TEXT (any text passes, though "
        "the step dictates `\"Lucky\"`); a `def` recipe in `hero` gets its own message."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2C-07 debug-routine (Debug: the four-step routine on a 12-line encounter script)
# ---------------------------------------------------------------------------------------------


def _encounter(show="encounter", glue='"Rolled: " + str(roll)', test="roll >= needed", roll="random.randint(1, 20)",
               needed="12"):
    return (
        "import random\n"
        f"needed = {needed}\n"
        f"roll = {roll}\n"
        "print(\"Oogrish checks the road ahead.\")\n"
        f"if {test}:\n"
        "    encounter = \"He spots the peddler's cart first.\"\n"
        "else:\n"
        "    encounter = \"The peddler sells Lucky a hat.\"\n"
        f"print({show})\n"
        f"print({glue})\n"
        "print(\"Needed: \" + str(needed))\n"
        "print(\"Steady, now.\")\n"
    )


ROUTINE_STARTER = _encounter(show="encounterr", glue='"Rolled: " + roll', test="roll > needed")
ROUTINE_SOLUTION = _encounter()

# CP1 reruns with a scripted low roll (3) and high roll (18), far from the boundary, so the quiet `>` bug cannot
# change it, and a typed encounter line can't pass by a lucky real roll.
_SHOWS_ENCOUNTER = r"""
assert 'encounter' in globals(), ('Keep the box' + chr(39) + 's name `encounter`, and mend the line that shows it: '
                                  '`print(encounter)`.')
_seen = {}
for _r in (3, 18):
    _ns, _rows, _calls, _err, _miss = _rerun({}, [_r])
    assert not _err, _stop({}, [_r], _err)
    assert 'encounter' in _ns, ('Keep the box' + chr(39) + 's name `encounter`, and mend the line that shows it: '
                                '`print(encounter)`.')
    _e = str(_ns['encounter'])
    assert _e in _rows, _mend('Print the box `encounter`, spelled the same as where it is made.', 'The encounter '
                              'did not show.', {}, [_r])
    _seen[_r] = (_e, _rows)
if _seen[3][0] != _seen[18][0]:
    for _r, _other in ((3, 18), (18, 3)):
        assert _seen[_other][0] not in _seen[_r][1], _mend('Show only the box `encounter`: the `if` picks one.',
                                                           'Your program showed both encounters.', {}, [_r])
"""
SHOWS_ENCOUNTER = ("the encounter is shown", _rerun_code() + _SHOWS_ENCOUNTER)

_SHOWS_ROLL_LINE = r"""
for _r in (7, 16):
    _ns, _rows, _calls, _err, _miss = _rerun({}, [_r])
    assert not _err, _stop({}, [_r], _err)
    assert _calls, ("Put the dice back on line 3: `roll = random.randint(1, 20)`, so Mar'tu's check can roll for you. "
                    'A typed roll is fine for one Run.')
    assert len(_calls) == 1, ('Roll once, on line 3, and show the box: `str(roll)`. Your program rolls the die more '
                              'than once, so the line can show a different number from the one the `if` used.')
    assert any('Rolled' in _l and _re.search(_whole(_r), _l) for _l in _rows), _mend(
        'Glue the roll in with `str(roll)`.', 'The line did not show `Rolled: ' + str(_r) + '`.', {}, [_r])
"""

DEBUG_ROUTINE = dict(
    id="debug-routine",
    title="The four-step routine",
    martu=(
        "Here is how I hunt [[bug|bugs]]. Four steps, every time:\n"
        "1. Read the last line.\n"
        "2. Go to the line it names.\n"
        "3. Check the line above, and where its boxes were made.\n"
        "4. No message, but a wrong answer? Print the values.\n"
        "This encounter script has three bugs. Two are loud. One is quiet. To test the quiet one, type `roll = 12` "
        "on line 3 for one Run, then put the dice back."
    ),
    names=["encounter", "roll", "needed", "str"],
    pair_talk=(
        "Pair talk: say the four steps out loud to your partner while you hunt the first bug. Then each of you "
        "mends it on your own screen."
    ),
    starter=ROUTINE_STARTER,
    checkpoints=[
        dict(
            id="mend-the-name",
            text="Mend the name Python can't find.",
            dictated=False,
            hints=[
                "Read Python's last line. It even asks: `Did you mean ...?`",
                "Steady, now. Go to line 9, the line Python names, and compare it with lines 6 and 8.",
                "Python matches names letter for letter: `lantern` and `lanternn` are two different names.",
            ],
            checks=[SHOWS_ENCOUNTER],
        ),
        dict(
            id="glue-the-roll",
            text="Mend the line that glues the roll to text.",
            dictated=False,
            hints=[
                "Read Python's last line, from the new Run. Which line does it name?",
                "It can only glue text to text. Go to line 10, then check line 3: what kind of value does `roll` "
                "hold?",
                "`\"Gold: \" + str(gold)` turns the number into text first, so the glue works.",
                "Change line 10 to `print(\"Rolled: \" + str(roll))`.",
            ],
            checks=[("the line shows the roll", _rerun_code() + _SHOWS_ROLL_LINE)],
        ),
        dict(
            id="exactly-enough",
            text="A roll of exactly `needed` should pass. Find the quiet bug and mend it.",
            dictated=False,
            hints=[
                "No message now, so read what your program printed. For one Run, change line 3 to `roll = 12`: does "
                "Oogrish spot the cart?",
                "Look at line 5, the `if`. A roll of 12 against `needed = 12` should pass. Which sign says *at "
                "least*? Then put the dice back on line 3.",
                "`>` leaves out the boundary; `>=` includes it. `12 >= 12` is True.",
            ],
            checks=[bnd_check("exactly enough passes", "roll", "needed", via_rolls=True)],
            pass_line="Oogrish: Three bugs, four steps. Steady, now. You read every one.",
        ),
    ],
    solution=ROUTINE_SOLUTION,
    assemble=dict(
        lines=[line for line in ROUTINE_SOLUTION.splitlines() if line.strip()],
        distractors=["print(encounterr)", "print(\"Rolled: \" + roll)", "if roll > needed:"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The routine on this script",
            text=(
                "1. Last line: `name 'encounterr' is not defined`. Step 2: line 9. Step 3: lines 6 and 8 make "
                "`encounter`, with one r.\n"
                "2. Run again. Last line: `can only concatenate str`. Line 10. Step 3: line 3 makes `roll` a number.\n"
                "3. No message. Step 4: set `roll = 12` for one Run and read what prints. Then put the dice back."
            ),
        ),
        dict(
            angle="picture",
            label="Loud and quiet",
            text=(
                "```text\nloud bug:\n  Python stops, names a line.\n  Steps 1 to 3 find it.\n"
                "quiet bug:\n  no message, wrong answer.\n  Step 4 finds it.\n```"
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The trap-door checks said `return roll >= required_roll`. A roll of exactly the number needed "
                "passed. The quiet bug here is the same boundary."
            ),
        ),
        dict(angle="shorter", text="Read the last line. Go to the line. Check above. Print the values."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="return roll >= required_roll",
        why=(
            "You have seen this. Each trap-door check used `>=`, so a roll of exactly the number needed still "
            "passed. Swap in `>` and nothing crashes, the check is just wrong. Only step 4 finds that."
        ),
    ),
    takeaway="Read the last line. Go to the line it names. Check the line above. No message? Print the values.",
    wrong_answers=[
        dict(why="the starter (the typo is reported first)", code=ROUTINE_STARTER, fails_at=0, message_contains="encounterr"),
        dict(why="typo mended, the roll still glued without str()",
             code=_encounter(glue='"Rolled: " + roll', test="roll > needed"), fails_at=0, message_contains="concatenate"),
        dict(why="loud bugs mended, > kept (the quiet bug)", code=_encounter(test="roll > needed"), fails_at=3,
             message_contains="exactly"),
        dict(why="the needed number shown instead of the roll", code=_encounter(glue='"Rolled: " + str(needed)'),
             fails_at=2, message_contains="str(roll)"),
        dict(why="the word roll in quotes", code=_encounter(glue='"Rolled: " + "roll"'), fails_at=2,
             message_contains="Rolled: 7"),
        dict(why="a roll typed into the line", code=_encounter(glue='"Rolled: 12"'), fails_at=2, message_contains="str(roll)"),
        dict(why="the typo copied into a new box", code=_encounter(show="encounterr").replace(
            "print(encounterr)", "encounterr = \"Lucky\"\nprint(encounterr)"), fails_at=1, message_contains="encounter"),
        dict(why="the roll typed by hand to test, and left", code=_encounter(roll="12"), fails_at=2,
             message_contains="put the dice back"),
        dict(why="the needed number typed in the if", code=_encounter(test="roll >= 12"), fails_at=3,
             message_contains="not a number you typed"),
        dict(why="== in the if (only exactly needed passes)", code=_encounter(test="roll == needed"), fails_at=3,
             message_contains="higher roll"),
        dict(why="a second roll inside the Rolled line (shows a new number, not the roll the if used)",
             code=_encounter(glue='"Rolled: " + str(random.randint(1, 20))'), fails_at=2, message_contains="more than once"),
        dict(why="the box renamed to encounterr everywhere, to match the typo",
             code=_encounter(show="encounterr").replace("    encounter = ", "    encounterr = "), fails_at=1,
             message_contains="Keep the box's name"),
        dict(why="the encounter line typed (passes only on a lucky real roll)",
             code=_encounter(show="\"He spots the peddler's cart first.\""), fails_at=1, message_contains="rolled a 3"),
        dict(why="the box shown, plus a typed encounter line", code=_encounter(
            show="encounter)\nprint(\"He spots the peddler's cart first.\""), fails_at=1, message_contains="both encounters"),
        dict(why="needed moved to the top face so == hides (no roll can go past 20)",
             code=_encounter(test="roll == needed", needed="20"), fails_at=3, message_contains="goes past it"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="read-traceback,boundary,concat-str,exact-names", solo="false",
             dictates="", foreign_names="lantern,lanternn,gold") + "\n"
        "2C-07 (D). The full four-step routine (2.2: the two-step footer has been on since 1W-02). A 12-line "
        "encounter script, three bugs in the order Python reports them: line 9 `encounterr` (NameError with 'Did "
        "you mean: encounter?', explainer rule 6), line 10 `\"Rolled: \" + roll` (TypeError; step 3 finds where "
        "`roll` was made), and line 5 `>` (no error: BND over scripted rolls finds it, step 4). Loud bugs crash, so "
        "each left fails at 0 with Python's own words (no partials: on the site a crash fails every checkpoint). "
        "Oogrish's 'Steady, now. Read the last line first.' is the Help label after 3 failed runs (site) and the "
        "start of hint 2 on the first bug. Time (teacher ruling): the quiet bug is tested with `roll = 12` for one "
        "Run (Mar'tu's text, CP3 rung 0 and the step-by-step angle), not by rolling until a 12 comes up; then the "
        "dice go back. The `roll = 12` WA: left in, the check's scripted die never gets called, so CP2 says to put "
        "the dice back. Rung 0 in every step is 'Read Python's last line' (for the quiet bug: what it printed). CP1 reruns with scripted rolls 3 and 18 (far from the "
        "boundary), so a typed encounter line can't pass on a lucky real roll, and showing both encounters fails. "
        "CP2 needs exactly one randint call (a second roll inside the Rolled line shows a different number)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 2C-S solo-2C (one bug, done alone)
# ---------------------------------------------------------------------------------------------

SOLO_2C_STARTER = "mana = 14\nprint(\"Mana: \" + mana)\n"

SOLO_2C = dict(
    id="solo-2c",
    title="Show Mar'tu",
    martu="A short one, just for you. One fizzle. Read the last line, then mend it.",
    solo=True,
    # Teacher ruling on the Unit 2 reviews: in Unit 2 SOLO items (and every QC2 exercise) the crash explainer
    # names the kind of slip and the line, and leaves out the fix. Python's own text stays visible.
    explainer="lean",
    names=["mana", "str"],
    starter=SOLO_2C_STARTER,
    checkpoints=[
        dict(
            id="make-it-print",
            text="Make the line print.",
            dictated=False,
            hints=[
                "Read Python's last line. What can it only glue?",
                "Look at line 2, the line Python names. `mana` holds a number, and `+` glues text to text.",
                "`\"Gold: \" + str(gold)` turns the number into text first.",
            ],
            checks=[
                lines_check("the line shows the mana", [
                    ({"mana": 14}, None, ["Mana: 14"], [], "Glue the box with `str(mana)`, so it shows `Mana: 14`."),
                    ({"mana": 3}, None, ["Mana: 3"], [], "Build the line from the box `mana`, so it follows it."),
                    ({"mana": 26}, None, ["Mana: 26"], [], "Build the line from the box `mana`, so it follows it."),
                ]),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ read Python's message and glue a number with `str()`.",
        ),
    ],
    solution="mana = 14\nprint(\"Mana: \" + str(mana))\n",
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line: it can only glue text. 2. Line 2. 3. Wrap the number in `str()`."),
        dict(angle="shorter", text="Text + number? Use `str(mana)`."),
    ],
    takeaway="On your own: read the last line, find the line, mend the slip.",
    wrong_answers=[
        dict(why="the starter (text + number)", code=SOLO_2C_STARTER, fails_at=0, message_contains="concatenate"),
        dict(why="the mana typed into the text", code="mana = 14\nprint(\"Mana: 14\")\n", fails_at=1,
             message_contains="mana = 3"),
        dict(why="the word mana in quotes", code="mana = 14\nprint(\"Mana: \" + \"mana\")\n", fails_at=1,
             message_contains="str(mana)"),
        dict(why="mana made into text (breaks any other number)", code="mana = \"14\"\nprint(\"Mana: \" + mana)\n",
             fails_at=1, message_contains="stopped"),
        dict(why="str around the wrong part", code="mana = 14\nprint(str(\"Mana: \") + mana)\n", fails_at=0,
             message_contains="concatenate"),
        dict(why="the space lost", code="mana = 14\nprint(\"Mana:\" + str(mana))\n", fails_at=1,
             message_contains="Mana: 14"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="concat-str,read-traceback", solo="true", dictates="",
             foreign_names="gold", seat_b='roll = 9 / print("Roll: " + roll) (the same TypeError, with the roll)') + "\n"
        "SOLO, one bug (C6), explainer='lean' (teacher ruling: the crash explainer names the kind of slip and the "
        "line, not the fix; Python's own text stays visible). Rung 0 is 'Read Python's last line'; the pass line "
        "uses 2A's form ('You did that on your own. On your map: ✓ ...'). Seat A (and anyone solo) gets "
        "`print(\"Mana: \" + mana)`; seat B would get "
        "`print(\"Roll: \" + roll)` once pair mode ships. Recorded, never blocking, never shown to a partner. CMB "
        "at 14, 3 and 26 (the spec's CMB + str: a comma print, `print(\"Mana:\", mana)`, also shows `Mana: 14` and "
        "passes; a typed number fails)."
    ),
)

LESSON_2C = dict(
    kind="lesson",
    id="when-spells-fizzle",
    title="When Spells Fizzle: Reading Errors",
    minutes=18,
    summary="Read Python's message like Mar'tu does: the last line, the line it names, and the values when there is no message.",
    notes=(
        "Lesson 2C (CC; 2C-05 SC). Preceded by 2c-remembers. The syllabus's Errors lesson, kept at the end of the "
        "unit; the full four-step routine lives in 2C-07. Exactly one SOLO (solo-2c). Non-dictated checkpoints: "
        "2C-01 CP1-3, 2C-05 CP2, 2C-07 CP1-3, 2C-S. More fizzles (2C-02 to 2C-04) are in the 2X pool."
    ),
    exercises=[ANATOMY_OF_A_FIZZLE, NO_ERROR_WRONG_ANSWER, EQUALS_IS_NOT_DEF, DEBUG_ROUTINE, SOLO_2C],
)


# =============================================================================================
# Extra practice 2X "More fizzles" (pool: 2C-02, 2C-03, 2C-04)
# =============================================================================================

# ---- 2C-02 syntax-fizzles: an unclosed quote, a missing colon, a missing bracket ----------------
# Verified order (CPython 3.13): the unclosed quote is reported first wherever it is, so it goes on line 2; then the
# missing colon (line 3); then the missing ) on the last line. Python reports them top to bottom, one per run.


def _syntax(quote='print("Shield up.")', colon="if mana < 6:", bracket='print("Mana: " + str(mana))'):
    return f"mana = 5\n{quote}\n{colon}\n    print(\"Low mana.\")\n{bracket}\n"


SYNTAX_STARTER = _syntax(quote='print("Shield up.)', colon="if mana < 6", bracket='print("Mana: " + str(mana)')
SYNTAX_SOLUTION = _syntax()

SYNTAX_FIZZLES = dict(
    id="syntax-fizzles",
    title="Syntax fizzles",
    martu=(
        "Three slips that stop Python before anything runs: a quote, a colon, a bracket. Each one is a "
        "[[SyntaxError]]: Python could not read a line.\n"
        "Guess first: three slips, so how many messages will you see? Press Run and count.\n"
        "Then mend them one at a time, and read the new message after each Run."
    ),
    names=["mana"],
    starter=SYNTAX_STARTER,
    checkpoints=[
        dict(
            id="close-the-quote",
            text="Mend line 2 so it shows `Shield up.`",
            dictated=False,
            hints=[
                "Read Python's last line. *Unterminated* means the text never ended.",
                "Look at line 2. Quotes come in pairs: one before the words, one after.",
                "`print(\"Fine.\")` has a `\"` before the words and another after them, before the `)`.",
            ],
            checks=[
                check("shows Shield up.", "assert 'Shield up.' in _lines(), " + say(
                    "Put the closing `\"` after the words, before the `)`, so line 2 shows `Shield up.`")),
            ],
        ),
        dict(
            id="add-the-colon",
            text="Mend the `if` line.",
            dictated=False,
            hints=[
                "Read Python's last line, from the new Run: `expected ':'`.",
                "Look at the very end of line 3.",
                "Every `if` line ends with a colon: `if rain > 0:`.",
            ],
            checks=[
                lines_check("Low mana. only when mana is low", [
                    ({"mana": 5}, None, ["Low mana."], [], "Keep `print(\"Low mana.\")` indented under the `if`."),
                    ({"mana": 8}, None, [], ["Low mana."], "Keep the print indented under the `if`, so it belongs to it."),
                    ({"mana": 2}, None, ["Low mana."], [], "Keep the question as it was, `mana < 6`: only the colon "
                     "was missing."),
                    ({"mana": 6}, None, [], ["Low mana."], "Keep the question as it was, `mana < 6`: only the colon "
                     "was missing."),
                ]),
            ],
        ),
        dict(
            id="close-the-bracket",
            text="Mend the last line so it shows the mana.",
            dictated=False,
            hints=[
                "Read Python's last line: `'(' was never closed`.",
                "Count the `(` and the `)` on line 5. Brackets come in pairs.",
                "`print(str(gold))` has two `(` and two `)`.",
            ],
            checks=[
                lines_check("the mana line follows mana", [
                    ({"mana": 5}, None, ["Mana: 5"], [], "Add the missing `)` at the end of line 5."),
                    ({"mana": 2}, None, ["Mana: 2"], [], "Build the line from the box `mana`, so it follows it."),
                ]),
            ],
            pass_line="Mar'tu: Three slips, three runs. One at a time, yes? That is normal.",
        ),
    ],
    solution=SYNTAX_SOLUTION,
    another_way=[
        dict(
            angle="why",
            label="Why only one message?",
            text=(
                "Python reads the whole program before it runs any of it. It stops at the first line it can't "
                "read, so it never gets to the other slips. Mend that one, run again, and it shows you the next. "
                "That is why errors come one at a time."
            ),
        ),
        dict(
            angle="picture",
            label="Python reads, then runs",
            text=(
                "```text\nPython reads every line.\nStuck on line 2?\n  -> stop: one message.\nAll fine?\n"
                "  -> run the program.\n```\n"
                "With a syntax slip, nothing runs at all. Not even line 1."
            ),
        ),
        dict(
            angle="step-by-step",
            text="1. Run. 2. Read the last line. 3. Mend that one slip. 4. Run again: a new message is progress.",
        ),
        dict(angle="shorter", text="Quotes in pairs. Colon after `if`. Brackets in pairs."),
    ],
    takeaway="Python reports one SyntaxError at a time. Mend it, run again, read the next.",
    wrong_answers=[
        dict(why="the starter (the unclosed quote is reported first)", code=SYNTAX_STARTER, fails_at=0,
             message_contains="unterminated"),
        dict(why="quote mended, colon still missing",
             code=_syntax(colon="if mana < 6", bracket='print("Mana: " + str(mana)'), fails_at=0,
             message_contains="expected ':'"),
        dict(why="quote and colon mended, bracket still open", code=_syntax(bracket='print("Mana: " + str(mana)'),
             fails_at=0, message_contains="never closed"),
        dict(why="the quote closed with the other mark", code=_syntax(quote="print(\"Shield up.')"), fails_at=0,
             message_contains="unterminated"),
        dict(why="colon added, the print not indented",
             code="mana = 5\nprint(\"Shield up.\")\nif mana < 6:\nprint(\"Low mana.\")\nprint(\"Mana: \" + str(mana))\n",
             fails_at=0, message_contains="indented block"),
        dict(why="one bracket too many", code=_syntax(bracket='print("Mana: " + str(mana)))'), fails_at=0,
             message_contains="unmatched"),
        dict(why="the mana typed into the last line", code=_syntax(bracket='print("Mana: 5")'), fails_at=3,
             message_contains="mana = 2"),
        dict(why="the question changed to == 5 while mending (mana 2 is low too)", code=_syntax(colon="if mana == 5:"),
             fails_at=2, message_contains="mana = 2"),
        dict(why="the question changed to <= 6 while mending", code=_syntax(colon="if mana <= 6:"), fails_at=2,
             message_contains="only the colon"),
        dict(why="the if line deleted (Low mana. always shows)",
             code="mana = 5\nprint(\"Shield up.\")\nprint(\"Low mana.\")\nprint(\"Mana: \" + str(mana))\n",
             fails_at=2, message_contains="mana = 8"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="read-traceback,quote-text,if-else", solo="false", dictates="",
             foreign_names="rain,gold") + "\n"
        "2C-02 (pool). Investigate: why only one message? (Mar'tu's guess-and-count prompt, answered by the 'why' "
        "angle; a predict card can't hold code Python can't read.) Bug order verified so Python reports "
        "them top to bottom (an unclosed quote is reported before an earlier missing colon, so the quote is on "
        "line 2). Each slip left fails at 0 with Python's words; no partials (nothing runs until all three are "
        "mended, so all three checkpoints turn green on the same run)."
    ),
)

# ---- 2C-03 name-fizzles: a typo, used too early, unquoted text, a capital letter --------------


def _names(mana_line='print("Mana: " + str(mana))', shield_first=True, spell='spell = "Fireball"',
           health_made="health = 100", health_used='print("Health: " + str(health))'):
    shield = 'shield = 8\nprint("Shield: " + str(shield))\n' if shield_first else (
        'print("Shield: " + str(shield))\nshield = 8\n')
    return (
        "mana = 20\n"
        f"{mana_line}\n"
        f"{shield}"
        f"{spell}\n"
        "print(\"Spell: \" + spell)\n"
        f"{health_made}\n"
        f"{health_used}\n"
    )


NAMES_STARTER = _names(mana_line='print("Mana: " + str(mama))', shield_first=False, spell="spell = Fireball",
                       health_made="Health = 100")
NAMES_SOLUTION = _names()

NAME_FIZZLES = dict(
    id="name-fizzles",
    title="Name fizzles",
    martu=(
        "Four [[NameError|NameErrors]]. Each one means: Python met a name that no line has made yet.\n"
        "The causes differ: a typo, a box used too early, words without quotes, a capital letter. Read the last "
        "line each time. Sometimes Python even asks: *Did you mean ...?*"
    ),
    names=["mana", "shield", "spell", "health"],
    starter=NAMES_STARTER,
    checkpoints=[
        dict(
            id="mend-the-typo",
            text="Mend line 2 so it shows the mana.",
            dictated=False,
            hints=[
                "Read Python's last line. It asks: `Did you mean: 'mana'?`",
                "Compare the name on line 2 with the box made on line 1, letter by letter.",
                "`lantern` and `lantren` are two different names to Python. Capitals and plurals count too.",
            ],
            checks=[
                check(
                    "the box is still mana",
                    "assert 'mama' not in globals(), " + say(
                        "Keep line 1 as it was, and mend the name on line 2: the box is `mana`. You renamed the box "
                        "on line 1 to `mama`, to match the slip."),
                ),
                lines_check("the mana line follows mana", [
                    ({"mana": 20}, None, ["Mana: 20"], [], "Use the box's real name on line 2: `str(mana)`."),
                    ({"mana": 7}, None, ["Mana: 7"], [], "Build the line from the box `mana`, so it follows it."),
                ]),
            ],
        ),
        dict(
            id="make-it-first",
            text="Make `shield` before the line that uses it.",
            dictated=False,
            hints=[
                "Read Python's last line: `name 'shield' is not defined`. Which line makes `shield`?",
                "Python runs from top to bottom. On line 3, has any line made `shield` yet?",
                "A box must be made before it is used:\n```python\ngold = 12\nprint(gold)\n```",
            ],
            checks=[
                lines_check("the shield line follows shield", [
                    ({"shield": 8}, None, ["Shield: 8"], [], "Make `shield` first, then print it."),
                    ({"shield": 3}, None, ["Shield: 3"], [], "Keep `shield = 8` and print the box `shield`."),
                ]),
            ],
        ),
        dict(
            id="quote-the-spell",
            text="Make `spell` hold the text `Fireball`.",
            dictated=True,
            hints=[
                "Read Python's last line: `name 'Fireball' is not defined`. Is `Fireball` a box, or words?",
                "Python looked for a box called `Fireball` and found none. You meant the words.",
                QUOTES_RULE,
            ],
            checks=[
                check(
                    "spell holds text",
                    "assert type(spell).__name__ == 'str', " + say("Give `spell` text, in quotes."),
                    "assert spell.strip(), " + say("Put the spell's name between the quotes. `spell` holds empty quotes."),
                ),
            ],
        ),
        dict(
            id="match-the-health",
            text="Make the box and the line that shows it both use the name `health`.",
            dictated=False,
            hints=[
                "Read Python's last line. It asks: `Did you mean: 'Health'?`",
                "Compare line 6 with line 7. One name has a capital, one does not. The task's name is `health`.",
                "Python sees `Gold` and `gold` as two different names. Use the same capitals every time.",
            ],
            checks=[
                name_check("health", skip=["mana", "shield", "spell"]),
                check(
                    "no Health box",
                    "assert 'Health' not in globals(), " + say(
                        "Python matches names letter for letter: you wrote `Health`, the task needs `health`."),
                ),
                lines_check("the health line follows health", [
                    ({"health": 100}, None, ["Health: 100"], [], "Show the box `health` on the last line."),
                    ({"health": 55}, None, ["Health: 55"], [], "Build the line from the box `health`, so it follows it."),
                ]),
            ],
            pass_line="Mar'tu: Four names, four reasons. Python is picky. Now you are too.",
        ),
    ],
    solution=NAMES_SOLUTION,
    another_way=[
        dict(
            angle="picture",
            label="Four ways to lose a name",
            text=(
                "```text\nmama      a typo\nshield    used too early\nFireball  words, no quotes\n"
                "health    made as Health\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Read the last line: which name?\n2. Search the code for that name, letter for letter.\n"
                "3. No line makes it? Make it first, or fix the spelling, or add quotes if you meant words."
            ),
        ),
        dict(angle="shorter", text="Not defined? Check the spelling, the capitals, the order, and the quotes."),
    ],
    takeaway="A NameError means no line made that name: check the spelling, the capitals, the order and the quotes.",
    wrong_answers=[
        dict(why="the starter (the typo comes first)", code=NAMES_STARTER, fails_at=0, message_contains="Did you mean: 'mana'"),
        dict(why="typo mended, shield still used too early",
             code=_names(shield_first=False, spell="spell = Fireball", health_made="Health = 100"), fails_at=0,
             message_contains="'shield' is not defined"),
        dict(why="shield made first, Fireball still unquoted", code=_names(spell="spell = Fireball", health_made="Health = 100"),
             fails_at=0, message_contains="'Fireball'"),
        dict(why="Fireball quoted, the capital H left (rule 5)", code=_names(health_made="Health = 100"), fails_at=0,
             message_contains="Did you mean: 'Health'"),
        dict(why="mended by using Health in both places", code=_names(
            health_made="Health = 100", health_used='print("Health: " + str(Health))'), fails_at=4,
             message_contains="letter for letter"),
        dict(why="the mana typed into the line", code=_names(mana_line='print("Mana: 20")'), fails_at=1,
             message_contains="mana = 7"),
        dict(why="the box renamed to mama, to match the typo",
             code=_names(mana_line='print("Mana: " + str(mama))').replace("mana = 20", "mama = 20"), fails_at=1,
             message_contains="renamed the box"),
        dict(why="an unclosed quote on Fireball",
             code=_names(spell='spell = "Fireball'), fails_at=0, message_contains="unterminated"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="read-traceback,exact-names,quote-text", solo="false", dictates="3",
             foreign_names="lantern,lantren,gold,Gold") + "\n"
        "2C-03 (pool). Four NameErrors, reported in run order (verified in 3.13): `mama` (Did you mean: 'mana'? -> "
        "explainer rule 6), `shield` used before it is made (the 'Used too early' row), `Fireball` unquoted (rule "
        "9), `health` with `Health` made (Did you mean: 'Health'? -> rule 5, since `health` is the task's name). "
        "These are the proving wrong answers for rules 5 and 6 (2.6). The A-08 `heath` slip is the same rule "
        "with a typo instead of a capital. Each slip left fails at 0; mending by using `Health` twice fails "
        "CP4 (the task's name is `health`)."
    ),
)

# ---- 2C-04 type-fizzles: text plus a number; a number compared with quoted text ----------------


def _types(glue='"Mana: " + str(mana)', cost="9"):
    return (
        "mana = 14\n"
        f"print({glue})\n"
        f"cost = {cost}\n"
        "if mana >= cost:\n"
        "    print(\"Lucky casts Silver Shield.\")\n"
    )


TYPES_STARTER = _types(glue='"Mana: " + mana', cost='"9"')
TYPES_SOLUTION = _types()
SILVER = "Lucky casts Silver Shield."

TYPE_FIZZLES = dict(
    id="type-fizzles",
    title="Type fizzles",
    martu=(
        "A [[TypeError]] means two values that don't fit together. Text and a number, mostly.\n"
        "Read the last line. Then look at the line it names, and at where its boxes were made. The slip is not "
        "always on the line Python names."
    ),
    names=["mana", "cost", "str"],
    starter=TYPES_STARTER,
    checkpoints=[
        dict(
            id="glue-the-mana",
            text="Mend line 2 so it shows the mana.",
            dictated=False,
            hints=[
                "Read Python's last line. What can it only glue?",
                "Look at line 2, the line Python names. Python can only glue text to text, and `mana` holds a number.",
                "`\"Gold: \" + str(gold)` turns the number into text first.",
                "Change line 2 to `print(\"Mana: \" + str(mana))`.",
            ],
            checks=[
                lines_check("the mana line follows mana", [
                    ({"mana": 14}, None, ["Mana: 14"], [], "Glue the box with `str(mana)`."),
                    ({"mana": 3}, None, ["Mana: 3"], [], "Build the line from the box `mana`, so it follows it."),
                ]),
            ],
        ),
        dict(
            id="cost-is-a-number",
            text="Line 4 compares a number with text. Mend the line that makes `cost`, so it holds a number.",
            dictated=False,
            hints=[
                "Read Python's last line: `'>=' not supported between instances of 'int' and 'str'`. Which box holds "
                "text?",
                "Python names line 4, but the text comes from line 3. Look at the quotes there.",
                "`\"7\" > 3` crashes, but `7 > 3` is True. Numbers don't need quotes.",
            ],
            checks=[
                check(
                    "cost holds a number",
                    "assert type(cost).__name__ != 'str', " + say(
                        "Take the quotes off on line 3: numbers don't need quotes. `cost` still holds text."),
                    "assert type(cost).__name__ == 'int', " + say("Give `cost` a whole number, like `9`."),
                    "assert cost == 9, " + say("Keep the 9, and take off only the quotes: Silver Shield costs 9. `cost` "
                                               "holds ") + " + str(cost) + '.'",
                ),
                # Only `mana` changes in the rerun, so `cost = int("9")` (Unit 1's int()) passes too.
                lines_check("Lucky casts with enough mana", [
                    ({"mana": 9}, None, [SILVER], [], "Keep `>=`: exactly enough mana still casts."),
                    ({"mana": 8}, None, [], [SILVER], "Keep `if mana >= cost:` as it is."),
                    ({"mana": 30}, None, [SILVER], [], "Keep `if mana >= cost:` as it is: more than enough mana casts too."),
                ]),
            ],
            pass_line="Lucky: Silver Shield. Shiny. Obviously.",
        ),
    ],
    solution=TYPES_SOLUTION,
    another_way=[
        dict(
            angle="picture",
            label="Two kinds of value",
            text="```text\n14     a number: do math\n\"14\"   text: glue it, show it\n```\nMix them, and Python stops.",
        ),
        dict(
            angle="step-by-step",
            text="1. Read the last line: which two kinds? 2. Go to the line. 3. Check the line that made each box.",
        ),
        dict(angle="shorter", text="Gluing? `str()` the number. Comparing? No quotes on numbers."),
    ],
    takeaway="TypeError: text and a number mixed. Use `str()` to glue; take the quotes off numbers you compare.",
    wrong_answers=[
        dict(why="the starter (text + number first)", code=TYPES_STARTER, fails_at=0, message_contains="concatenate"),
        dict(why="glue mended, cost still text", code=_types(cost='"9"'), fails_at=0, message_contains="not supported between"),
        dict(why="text turned into a number inside the if, line 3 left",
             code=_types(cost='"9"').replace("if mana >= cost:", "if mana >= int(cost):"), fails_at=2,
             message_contains="quotes"),
        dict(why="mana typed into the line", code=_types(glue='"Mana: 14"'), fails_at=1, message_contains="mana = 3"),
        dict(why="mana made into text to fix the glue (the compare then breaks)",
             code="mana = \"14\"\nprint(\"Mana: \" + mana)\ncost = 9\nif mana >= cost:\n    print(\"Lucky casts Silver Shield.\")\n",
             fails_at=0, message_contains="not supported between"),
        dict(why="> instead of >= while mending", code=_types().replace(">=", ">"), fails_at=2,
             message_contains="Exactly enough"),
        dict(why="the quotes taken off, but the number changed", code=_types(cost="1"), fails_at=2,
             message_contains="keep the 9"),
        dict(why="the cast typed with no question (always casts)",
             code=_types().replace("if mana >= cost:\n    print", "print").replace("    print(\"Lucky", "print(\"Lucky"),
             fails_at=2, message_contains="mana = 8"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="read-traceback,numbers-vs-text,concat-str", solo="false",
             dictates="", foreign_names="gold") + "\n"
        "2C-04 (pool). Two TypeErrors in run order: line 2 text + number ('can only concatenate'), then line 4 "
        "`'>=' not supported between instances of 'int' and 'str'`, which is reported on line 4 but mended on "
        "line 3 (step 3 of the routine: check where the boxes were made). CP2 reruns with `mana` only (9, 8, 30) and "
        "checks `cost == 9`, so `cost = int(\"9\")` (Unit 1's int()) passes too."
    ),
)

EXTRA_2X = dict(
    kind="lesson",
    id="extra-more-fizzles",
    title="Extra practice: More fizzles",
    optional=True,
    minutes=11,
    summary="More broken spells to mend: syntax slips, names Python can't find, and text mixed with numbers.",
    notes="2X pool (2C-02, 2C-03, 2C-04). Optional; feeds twins, the spaced queue and early finishers.",
    exercises=[SYNTAX_FIZZLES, NAME_FIZZLES, TYPE_FIZZLES],
)


# =============================================================================================
# Article 2-A2 "Mar'tu's Seal" (optional, 10 min) and try-it seal-the-check
# =============================================================================================

SEAL_SECTIONS = [("One below the boundary", 14, "False"), ("Exactly the boundary", 15, "True"),
                 ("One above the boundary", 16, "True")]


def _seal(seals=None, extra=""):
    """seals = the line under each `# seal:` comment (None = left empty)."""
    seals = seals or [None, None, None]
    code = "needed = 15\n"
    for (label, roll, _), seal in zip(SEAL_SECTIONS, seals):
        code += f"\n# {label}:\nroll = {roll}\npassed = roll >= needed\n# seal:\n" + (seal + "\n" if seal else "")
    return code + extra + "\nprint(\"All three seals hold.\")\n"


SEAL_STARTER = _seal()
SEAL_SOLUTION = _seal(["assert passed == False", "assert passed == True", "assert passed == True"])

SEAL_THE_CHECK = dict(
    id="seal-the-check",
    title="Seal the check",
    martu=(
        "Three rolls against a `needed` of 15: one below, one exactly, one above. Under each one, write a seal "
        "that says what `passed` must be.\n"
        "Then Mar'tu's check breaks your `passed` lines on purpose. Good seals catch it."
    ),
    introduces=["node:Assert"],
    names=["passed"],
    starter=SEAL_STARTER,
    checkpoints=[
        dict(
            id="three-seals",
            text="Under each `# seal:` comment, write an `assert` that says what `passed` must be for that roll.",
            dictated=False,
            hints=[
                "A roll of 14 against 15 fails, so `passed` must be `False` there. What must it be for exactly 15? "
                "And for 16?",
                "A seal with other names: `assert door_open == True` stops the program if the door is shut.",
                "Under the first `# seal:`, write `assert passed == False`. Under the other two, `assert "
                "passed == True`.",
            ],
            checks=[seal_check("the seals catch a broken check", "passed", 15)],
            pass_line="Mar'tu: Sealed. If anyone swaps that `>=` for `>`, your seals will shout. Good.",
        ),
    ],
    solution=SEAL_SOLUTION,
    assemble=dict(
        lines=[line for line in SEAL_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["assert passed = True"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Three seals on a number line",
            text=(
                "```text\n   14        15        16\n   fail  |  pass      pass\n   ^          ^          ^\n"
                " False     True       True\n```\nThe seal at exactly 15 is the one that catches `>`."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work?",
            text=(
                "`>` instead of `>=` gives no error: a quiet bug. A seal at the boundary says what must be true. "
                "When it is not, Python stops. The quiet bug becomes a loud one."
            ),
        ),
        dict(angle="shorter", text="Below: `False`. Exactly: `True`. Above: `True`."),
    ],
    takeaway="`assert passed == True` stops the program if `passed` is not True. Seal the boundary.",
    wrong_answers=[
        dict(why="the starter (no seals yet)", code=SEAL_STARTER, fails_at=1, message_contains="three in all"),
        dict(why="every seal says True (the roll of 14 should fail)",
             code=_seal(["assert passed == True", "assert passed == True", "assert passed == True"]), fails_at=0,
             message_contains="AssertionError"),
        dict(why="the exact roll sealed as a fail (> thinking)",
             code=_seal(["assert passed == False", "assert passed == False", "assert passed == True"]), fails_at=0,
             message_contains="AssertionError"),
        dict(why="seals about the roll, not about passed",
             code=_seal(["assert roll == 14", "assert roll == 15", "assert roll == 16"]), fails_at=1,
             message_contains="must be"),
        dict(why="only the easy rolls sealed (the boundary left out)",
             code=_seal(["assert passed == False\nassert passed == False", None, "assert passed == True"]), fails_at=1,
             message_contains="exactly 15"),
        dict(why="only below and exactly sealed (an == bug slips through)",
             code=_seal(["assert passed == False", "assert passed == True\nassert passed == True", None]), fails_at=1,
             message_contains="above 15"),
        dict(why="only exactly and above sealed (always-True slips through)",
             code=_seal([None, "assert passed == True", "assert passed == True\nassert passed == True"]), fails_at=1,
             message_contains="below 15"),
        dict(why="= instead of == in a seal",
             code=_seal(["assert passed = False", "assert passed == True", "assert passed == True"]), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the question copied into each seal (it never says True or False)",
             code=_seal(["assert passed == (roll >= needed)"] * 3), fails_at=1, message_contains="answer for its roll"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="boundary,compare", solo="false", dictates="",
             foreign_names="door_open") + "\n"
        "2-A2 try-it (G4 R15). The check counts the asserts (`node:Assert`, at least 3, at least 3 about "
        "`passed`), and the student's own run proves they hold on the right line (a wrong seal raises "
        "AssertionError: fails at 0). Then it reruns the program three times with the `passed` lines broken on "
        "purpose, in a fresh namespace: `>` for `>=` (caught only by the exactly-15 seal), `==` for `>=` (caught "
        "by the above seal), and `passed = True` (caught by the below seal). `assert passed` and `assert not "
        "passed` also pass. At least 3 seals must say the answer (passed compared with True/False, or `assert "
        "passed` / `assert not passed`): a seal that copies the question, `assert passed == (roll >= needed)`, "
        "fails with its own message. Optional only, so the core gate is unaffected; re-offered in 6A-09 and T-Own. "
        "A seal that does not hold crashes with a bare `AssertionError` (no words after it), which the site's "
        "explainer gives its own kind."
    ),
)

MARTUS_SEAL = dict(
    kind="article",
    id="martus-seal",
    title="Mar'tu's Seal",
    optional=True,
    minutes=10,
    summary="An `assert` line says what must be true. Seal your checks at the boundary, and quiet bugs get loud.",
    introduces=["node:Assert"],
    body=(
        "At the Institute we sealed our work: a line that says what *must* be true. If it isn't, Python stops and "
        "tells you.\n"
        "A seal is an [[assert]] line: the word `assert`, then a yes-or-no question. `assert passed == True` says: "
        "`passed` must be `True` here.\n"
        "If the answer is `True`, nothing happens, and the program goes on. If it is `False`, Python stops with "
        "`AssertionError` and names the line:\n"
        "```text\nFile \"main.py\", line 4\n    assert passed == True\nAssertionError\n```\n"
        "Why bother? Seals catch quiet [[bug|bugs]]. A `>` where `>=` belongs gives no error at all. A seal at the "
        "boundary turns that quiet bug into a loud one.\n"
        "The campaign never asks for seals. They are for the careful, yes?"
    ),
    examples=[
        dict(code="roll = 15\nneeded = 15\npassed = roll >= needed\nassert passed == True\nprint(\"Sealed. A 15 passes.\")\n",
             output="Sealed. A 15 passes."),
        dict(code="roll = 14\nneeded = 15\npassed = roll >= needed\nassert passed == False\n"
                  "print(\"Sealed. A 14 does not pass.\")\n",
             output="Sealed. A 14 does not pass."),
    ],
    exercises=[SEAL_THE_CHECK],
    notes=(
        "meta: path=optional; intro node:Assert (optional-only token: no core item uses it). Examples show seals "
        "that hold (a failing example would not run); the AssertionError is shown as text in the body."
    ),
)


# =============================================================================================
# Quick Check 2 (test-out). Forms A and B: two code tasks each, plus four questions each.
# =============================================================================================

_QC_MARTU = ""


def _qc_meta(skills, dictates, foreign="", form="A"):
    return meta(starter_level="S3", path="QC2", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# ---- C1: a skill check of your own (randint, boundary, if-else) ----

def _qc_roll(form, faces, needed, win, lose):
    def program(roll=f"random.randint(1, {faces})", test="roll >= needed", need=needed, branches=None):
        body = branches if branches is not None else (
            f"if {test}:\n    print(\"{win}\")\nelse:\n    print(\"{lose}\")\n")
        return (
            "import random\n"
            f"# Pick any needed, from 2 to {faces}.\n"
            f"needed = {need}\n"
            f"roll = {roll}\n"
            "# If roll reaches needed, print a success line. Otherwise, print a failure line.\n"
            + body
        )

    starter = program(roll="0", need=0, branches="")
    return dict(
        id="roll-your-own",
        title="A skill check of your own",
        martu=_QC_MARTU + (
            f"Your own skill check. Pick how hard it is, roll a d{faces}, and say what happened. Mar'tu's check "
            "rolls the die for you, so it can try every kind of roll.\n"
            "Stuck? Skip it, or try the lesson If the Clock Turns Red. Tasks you pass here stay ticked."
        ),
        names=["needed", "roll"],
        support="none",
        # Teacher ruling on the Unit 2 reviews: every QC2 exercise (and the Unit 2 SOLOs) gets the lean explainer:
        # the kind of slip and the line, not the fix. Python's own text stays visible.
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="pick-needed",
                text=f"Set `needed` to any number from 2 to {faces}.",
                dictated=False,
                hints=[
                    "Look at line 3. `needed` is how high the roll must be. Numbers have no quotes.",
                    "A box gets a number like this: `target = 7`.",
                    f"Write `needed = {needed}`, or any number from 2 to {faces}.",
                ],
                checks=[
                    name_check("needed", foreign=["target", "score"], skip=["roll"], kept=True),
                    check(
                        "needed is a fair number",
                        "_v = needed",
                        "assert type(_v).__name__ != 'str', " + say("`needed` holds text, because of the quotes."),
                        "assert type(_v).__name__ == 'int', " + say("`needed` does not hold a whole number."),
                        "import ast as _ast",
                        "_zero = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' "
                        "and [getattr(_t, 'id', '') for _t in _n.targets] == ['needed'] "
                        "and type(_n.value).__name__ == 'Constant' and _n.value.value == 0]",
                        "assert not (_v == 0 and _zero), " + say(
                            f"`needed` still holds the starter's `0`, and the task asks for a number from 2 to {faces}."),
                        f"assert 2 <= _v <= {faces}, " + say("`needed` holds ") + " + str(_v) + " + say(
                            f", but the task asks for a number from 2 to {faces}: a d{faces} roll is 1 to {faces}."),
                        "assert not _assigned_from_expression('needed'), " + say(
                            "`needed` is worked out, not one typed number, so Mar'tu's check can not change it to "
                            "try other rolls."),
                    ),
                ],
            ),
            dict(
                id=f"roll-a-d{faces}",
                text=f"Roll a d{faces} into `roll`.",
                dictated=True,
                hints=[
                    f"A d{faces} has faces 1 to {faces}, and `randint` includes both ends.",
                    "`random.randint(1, 4)` rolls a d4: lowest face first, then the highest.",
                    f"Write `roll = random.randint(1, {faces})`.",
                ],
                checks=[rnd_check(f"roll is a d{faces}", "roll", faces, [5], placeholder=0, lean=True)],
            ),
            dict(
                id="succeed-or-fail",
                text="Print a success line when `roll` reaches `needed`, and a failure line otherwise.",
                dictated=False,
                hints=[
                    "Exactly enough passes, so which sign? Then `else:` for the failure line.",
                    "With other names: `if score >= target:` / `    print(\"Yes.\")` / `else:` / `    print(\"No.\")`.",
                    "Write `if roll >= needed:`, a success line under it, then `else:` and a failure line.",
                ],
                checks=[bnd_check("exactly enough passes", "roll", "needed", via_rolls=True, faces=faces, lean=True)],
            ),
        ],
        solution=program(),
        partials=[program(roll="0", branches=""), program(branches="")],
        assemble=dict(
            lines=["import random", f"needed = {needed}", f"roll = random.randint(1, {faces})", "if roll >= needed:",
                   f"    print(\"{win}\")", "else:", f"    print(\"{lose}\")"],
            distractors=[f"roll = random.randint(1, {faces - 1})", "if roll > needed:", "else roll < needed:"],
        ),
        another_way=[
            dict(angle="step-by-step", text=f"1. `needed = ` a number from 2 to {faces}. 2. Roll with `random.randint(1, {faces})`. 3. `if`, a sign, then `else:`."),
            dict(angle="picture", text=f"```text\n1 ... needed-1 | needed ... {faces}\n     fail      |     pass\n```"),
        ],
        takeaway=f"Roll with `random.randint(1, {faces})`, then `if roll >= needed:` and `else:`.",
        wrong_answers=[
            dict(why="the starter (needed still the starter's 0)", code=starter, fails_at=1,
                 message_contains="still holds the starter's `0`"),
            dict(why="> instead of >= (exactly enough fails)", code=program(test="roll > needed"), fails_at=3,
                 message_contains="exactly"),
            dict(why=f"a d{faces - 1} (the top face left out)", code=program(roll=f"random.randint(1, {faces - 1})"),
                 fails_at=2, message_contains=f"never gives {faces}"),
            dict(why="a die that starts at 0", code=program(roll=f"random.randint(0, {faces})"), fails_at=2,
                 message_contains="can give 0"),
            dict(why="a roll typed by hand", code=program(roll="7"), fails_at=2, message_contains="typed"),
            dict(why="the roll left as the starter's 0", code=program(roll="0"), fails_at=2,
                 message_contains="still holds the starter's `0`"),
            dict(why="the needed number typed into the if", code=program(test=f"roll >= {needed}"), fails_at=3,
                 message_contains="does not follow the box `needed`"),
            dict(why="needed left at 0", code=program(need=0), fails_at=1, message_contains=f"from 2 to {faces}"),
            dict(why="needed in quotes (the compare crashes)", code=program(need=f'"{needed}"'), fails_at=0,
                 message_contains="not supported between"),
            dict(why="needed bigger than the die", code=program(need=faces + 5), fails_at=1,
                 message_contains=f"from 2 to {faces}"),
            dict(why="= instead of == style slip: = in the if", code=program(test="roll = needed"), fails_at=0,
                 message_contains="=="),
            dict(why="the colon left off the if", code=program().replace("if roll >= needed:", "if roll >= needed"),
                 fails_at=0, message_contains="expected ':'"),
            dict(why="else with a condition", code=program().replace("else:", "else roll < needed:"), fails_at=0,
                 message_contains="expected ':'"),
            dict(why="no else (a low roll prints nothing)",
                 code=program(branches=f"if roll >= needed:\n    print(\"{win}\")\n"), fails_at=3,
                 message_contains="A low roll printed nothing"),
            dict(why="the print not indented under the if",
                 code=program(branches=f"if roll >= needed:\nprint(\"{win}\")\nelse:\n    print(\"{lose}\")\n"),
                 fails_at=0, message_contains="indented block"),
            dict(why="the same line for success and failure",
                 code=program(branches=f"if roll >= needed:\n    print(\"{win}\")\nelse:\n    print(\"{win}\")\n"),
                 fails_at=3, message_contains="same thing"),
            dict(why="needed at the top face with == (no roll can go past it)", code=program(test="roll == needed", need=faces),
                 fails_at=3, message_contains="goes past `needed` should pass"),
            dict(why="walrus after Python's hint (:= puts needed into roll)", code=program(test="roll := needed"),
                 fails_at=2, message_contains=":="),
            dict(why="the hint example's box name (target) instead of needed",
                 code=program().replace("needed", "target").replace("# Pick any target", "# Pick any needed"),
                 fails_at=1, message_contains="example"),
            dict(why="a random needed (the check can't try rolls against it)",
                 code=program(need=f"random.randint(2, {faces})"), fails_at=1, message_contains="not one typed number"),
            dict(why="lean: the d(faces-1) message names the slip, never the fixed call",
                 code=program(roll=f"random.randint(1, {faces - 1})"), fails_at=2,
                 message_contains=f"A d{faces} has faces 1 to {faces}, but `random.randint(1, {faces - 1})` never gives"),
            dict(why="lean: > for >= names the evidence, not the sign", code=program(test="roll > needed"), fails_at=3,
                 message_contains=f"A roll of exactly {needed} gave the failure line"),
            dict(why="lean: if True names the evidence", code=program(test="True"), fails_at=3,
                 message_contains="Both rolls printed the same line, so the answer never changes"),
        ],
        notes=_qc_meta("randint,boundary,if-else", "2", "score,target", form) + "\n"
        f"QC2 C1, form {form} (a d{faces}). Any needed from 2 to {faces} passes (lint e): BND reads it from the "
        "student's code and scripts the die (needed - 1, needed, needed + 1, 1 and the top face, then needed + 3 or "
        "- 3 to prove the `if` asks with the box). RND catches the top-excluded belief and a die from 0. The "
        "starter's placeholders (`needed = 0`, `roll = 0`) are named as the starter's. explainer='lean'.",
    )


# ---- C2: mend a dialogue chain: two loud slips, one quiet (read-traceback, elif-chain, quote-text, compare) ----

def _qc_mend(form, first, second, first_line, second_line):
    hm = "Mar'tu: Hm."
    big = second.capitalize()  # "Option 2": the capitals a player might type
    num_second = second.split()[-1]

    def program(ask=f"if choice == \"{first}\":", other=f"elif choice == \"{second}\":",
                lower="choice = choice.lower()", value=big):
        return (
            f"choice = \"{value}\"\n"
            + (lower + "\n" if lower else "")
            + f"{ask}\n"
            f"    print(\"{first_line}\")\n"
            f"{other}\n"
            f"    print(\"{second_line}\")\n"
            "else:\n"
            f"    print(\"{hm}\")\n"
        )

    starter = program(ask=f"if choice = \"{first}\":", other=f"elif choice == {second}:", lower="choice.lower()")
    loud_mended = program(lower="choice.lower()")
    return dict(
        id="mend-the-choices",
        title="Mend the choices",
        martu=_QC_MARTU + (
            "Three slips in a dialogue chain: two loud, one quiet. Read Python's last line, go to the line it "
            "names, and mend it. Then run again for the next. When Python goes quiet, read what your program "
            "printed.\n"
            "Stuck? Skip it, or try the lesson When Spells Fizzle. Tasks you pass here stay ticked."
        ),
        names=["choice", "lower"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="mend-the-ask",
                text=f"Mend the line that asks about `\"{first}\"`.",
                dictated=False,
                hints=[
                    "Read Python's last line. Which line does it name?",
                    "Python names line 3 and asks: `Maybe you meant '=='`? Which sign asks a question?",
                    "`=` puts a value in a box. `==` asks: is the same as? `if mana == 0:` asks whether mana is 0.",
                ],
                checks=[
                    lower_brackets_check("choice", lean=True),
                    check(
                        "the if asks with ==",
                        "import ast as _ast",
                        "_walrus = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'NamedExpr']",
                        "assert not _walrus, " + say(
                            "`:=` puts a value in a box, the same as `=`. It does not ask *is it the same as?*"),
                    ),
                    lines_check(f"{first} gets its reply", [
                        ({"choice": first}, None, [first_line], [second_line, hm],
                         f"The choice `\"{first}\"` should get its own reply, and only that one."),
                        ({"choice": second}, None, [], [first_line], f"Only `\"{first}\"` should get this reply."),
                    ]),
                ],
            ),
            dict(
                id="mend-the-quotes",
                text=f"Mend the line that asks about {second}.",
                dictated=False,
                hints=[
                    "Read Python's last line, from the new Run. Which line does it name?",
                    f"Python says `invalid syntax` on line 5. Two bare words: is `{second}` a box, or text?",
                    QUOTES_RULE + " The option is text, so it needs quotes.",
                ],
                checks=[
                    strexact_check([first, second], lean=True),
                    lines_check("each choice gets its reply", [
                        ({"choice": second}, None, [second_line], [first_line, hm],
                         f"The choice `\"{second}\"` should get its own reply."),
                        ({"choice": "option 9"}, None, [hm], [first_line, second_line], "Any other choice should reach the `else`."),
                    ]),
                ],
            ),
            dict(
                id="any-capitals",
                text=f"Make `\"{big}\"`, with a capital, get the same reply as `\"{second}\"`.",
                dictated=False,
                hints=[
                    f"No message now, so read what your program printed: `{hm}` Is that the reply `\"{big}\"` should get?",
                    "Look at line 2. It makes a lower-case copy of `choice`. Where does that copy go?",
                    "`.lower()` gives a copy, and the box itself stays the same. To keep the copy, put it in the "
                    "box: `shout = shout.lower()`.",
                ],
                checks=[
                    lower_kept_check("any capitals get their reply", "choice", lean=True, cases=[
                        ({"choice": big}, [second_line], [first_line, hm]),
                        ({"choice": first.upper()}, [first_line], [second_line, hm]),
                        ({"choice": "oPTION " + num_second}, [second_line], [first_line, hm]),
                    ]),
                ],
            ),
        ],
        solution=program(),
        assemble=dict(
            lines=[line for line in program().splitlines()],
            distractors=[f"if choice = \"{first}\":", f"elif choice == {second}:", "choice.lower()"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                "1. Run and read the last line. 2. Mend the line it names. 3. Run again for the next. 4. No message, "
                f"but `{hm}`? Look at line 2: is the copy kept?")),
            dict(angle="shorter", text=f"`==` asks. `\"{second}\"` needs quotes. Keep the copy: `choice = choice.lower()`."),
        ],
        takeaway="`==` to ask, quotes around text you compare with, and keep the `.lower()` copy: `choice = choice.lower()`.",
        wrong_answers=[
            dict(why="the starter (= in the if is reported first)", code=starter, fails_at=0, message_contains="=="),
            dict(why="the ask mended, the option still unquoted",
                 code=program(other=f"elif choice == {second}:", lower="choice.lower()"), fails_at=0,
                 message_contains="invalid syntax"),
            dict(why="the quotes mended, = still in the if",
                 code=program(ask=f"if choice = \"{first}\":", lower="choice.lower()"), fails_at=0,
                 message_contains="=="),
            dict(why="both loud slips mended, the lower-case copy still forgotten (the quiet slip)", code=loud_mended,
                 fails_at=3, message_contains="then forgets it"),
            dict(why="the option mended with a capital O",
                 code=program(other=f"elif choice == \"{big}\":"), fails_at=2, message_contains="every letter"),
            dict(why="= in the elif too", code=program(other=f"elif choice = \"{second}\":", lower="choice.lower()"),
                 fails_at=0, message_contains="=="),
            dict(why="elif turned into a second if (the else joins it)",
                 code=program(other=f"if choice == \"{second}\":"), fails_at=1, message_contains="printed anyway"),
            dict(why="the option mended without the space",
                 code=program(other=f"elif choice == \"{second.replace(' ', '')}\":"), fails_at=2,
                 message_contains="every letter"),
            dict(why="walrus after Python's hint (`Maybe you meant '==' or ':='`)",
                 code=program(ask=f"if choice := \"{first}\":"), fails_at=1, message_contains=":="),
            dict(why="the question dropped from the if (`if choice:` is always true)",
                 code=program(ask="if choice:"), fails_at=1, message_contains=f"Only `\"{first}\"` should get this reply"),
            dict(why=".lower with no () (the copy never happens)", code=program(lower="choice = choice.lower"),
                 fails_at=1, message_contains="`()`"),
            dict(why="the starter's value lowered by hand, line 2 deleted (a typed fix: capitals still fail)",
                 code=program(lower="", value=second), fails_at=3, message_contains="typed with capitals does not get"),
            dict(why="the starter's value lowered by hand, the forgotten copy left",
                 code=program(lower="choice.lower()", value=second), fails_at=3, message_contains="then forgets it"),
            dict(why="lower(choice) (the dot left out)", code=program(lower="choice = lower(choice)"), fails_at=0,
                 message_contains="'lower' is not defined"),
            dict(why="the copy compared with capitals",
                 code=program(other=f"elif choice == \"{big}\":", lower="choice = choice.lower()"), fails_at=2,
                 message_contains="every letter"),
            dict(why="capitals typed out one by one with or",
                 code=program(lower="", other=f"elif choice == \"{second}\" or choice == \"{big}\":"), fails_at=3,
                 message_contains="typed with capitals does not get"),
            dict(why="lean: the forgotten copy is named, not the fixed line", code=loud_mended, fails_at=3,
                 message_contains="makes a lower-case copy, then forgets it"),
        ],
        notes=_qc_meta("read-traceback,elif-chain,quote-text,compare", "", "mana,shout", form) + "\n"
        f"QC2 C2, form {form}. Two loud slips, both SyntaxErrors (verified in 3.13: `=` in an if -> \"invalid "
        "syntax. Maybe you meant '==' or ':='\" on line 3; two bare words after `==` -> \"invalid syntax\" on line "
        "5), so nothing runs until both are mended: either left fails at 0, and CP1 and CP2 turn green together (no "
        "partial 1). Then the quiet slip (teacher ruling: QC2 must ask for `.lower()`): line 2 `choice.lower()` makes "
        f"a copy and forgets it, so the starter's `\"{big}\"` gets `{hm}` with no error. CP3 reruns with "
        f"`\"{big}\"`, `\"{first.upper()}\"` and `\"oPTION {num_second}\"`, so typing the value in small letters, or "
        "an `or` for each capital, fails. CP1 and CP2 rerun with small letters, so they stay green while the quiet "
        "slip is open. STREXACT looks only at text in a comparison (the starter's capital value is fine). "
        "`.lower` with no `()` is caught in CP1 (it breaks every reply). The WA 'both loud slips mended' stands in "
        "for partial 2. explainer='lean'.",
    )


# ---- C3: hold the barrier (and-or-not, elif-chain, boundary): cast_spell rebuilt ----

def _qc_barrier(form, hero, spell, mana, affinity, lines, pass_line):
    """mana == cost and affinity == required in the starter: exactly enough, so a `<=` shows on the first Run."""
    s_line, m_line, c_line = lines
    can = "can_cast = mana >= cost and affinity >= required"
    chain = (
        "if affinity < required:\n"
        f"    print(\"{s_line}\")\n"
        "elif mana < cost:\n"
        f"    print(\"{m_line}\")\n"
        "else:\n"
        f"    print(\"{c_line}\")\n"
    )
    loose = f"print(\"{s_line}\")\nprint(\"{m_line}\")\nprint(\"{c_line}\")\n"

    def program(can_line="can_cast = False", body=loose):
        return (
            f"# {hero} casts {spell} to hold the barrier.\n"
            f"mana = {mana}\n"
            f"cost = {mana}\n"
            f"affinity = {affinity}\n"
            f"required = {affinity}\n"
            "\n"
            "# 1. can_cast: does mana reach cost, and affinity reach required?\n"
            f"{can_line}\n"
            "print(can_cast)\n"
            "\n"
            "# 2. cast_spell's chain. Put these three lines in an if / elif / else:\n"
            "#    If affinity is lower than required: not skilled enough.\n"
            "#    Otherwise, if mana is lower than cost: not enough mana.\n"
            "#    Otherwise: the barrier holds.\n"
            + body
        )

    def vals(m=mana, c=mana, a=affinity, r=affinity):
        return {"mana": m, "cost": c, "affinity": a, "required": r}

    big_m, big_a = mana + 11, affinity + 4   # the moved spell: proves the questions ask with the boxes
    starter = program()
    solution = program(can, chain)
    # Lean (a test-out, no hints): each message says what should have happened, and the evidence, never the fix.
    typed = "With other values in the boxes, the answer did not follow them."
    return dict(
        id="hold-the-barrier",
        title="Hold the barrier",
        martu=_QC_MARTU + (
            f"`cast_spell`, rebuilt. First `can_cast`: {hero} needs enough mana *and* enough affinity. Then put "
            f"the three lines in one chain, in the order the comments give. Exactly enough still casts. Mar'tu's "
            "check tries other spells, so ask with the boxes.\n"
            "Stuck? Skip it, or try the lesson If the Clock Turns Red. Tasks you pass here stay ticked."
        ),
        names=["can_cast", "mana", "cost", "affinity", "required"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="can-cast",
                text="Make `can_cast` say whether `mana` reaches `cost` and `affinity` reaches `required`. Exactly "
                     "enough counts.",
                dictated=False,
                hints=[
                    "Two questions, and both must be `True`. Which word joins them? Which sign says *at least*?",
                    "`and` is True only when both sides are True: `print(3 >= 3 and 5 >= 9)` prints `False`.",
                    "Write `can_cast = mana >= cost and affinity >= required`.",
                ],
                checks=[
                    gets_check("can_cast", lean=True),
                    from_boxes_check("can_cast", ["mana", "cost", "affinity", "required"], "", placeholder=False),
                    box_check("can_cast needs both", "can_cast", placeholder=False, base=vals(), lean=True, cases=[
                        (vals(), None, True, "Exactly enough mana and affinity should cast here."),
                        (vals(m=mana - 1), None, False, "`mana` is one short here, so the spell should not cast."),
                        (vals(a=affinity - 1), None, False, "`affinity` is one short here, so the spell should not cast."),
                        (vals(m=big_m, a=big_a), None, True, "More than enough mana and affinity should cast too."),
                        (vals(m=big_m - 1, c=big_m), None, False, typed),
                        (vals(a=big_a - 1, r=big_a), None, False, typed),
                        (vals(big_m, big_m, big_a, big_a), None, True, typed),
                    ]),
                ],
            ),
            dict(
                id="cast-spell-chain",
                text="Put the three print lines in an `if` / `elif` / `else`, in the order the comments give. Exactly "
                     "enough still casts.",
                dictated=False,
                hints=[
                    "Follow the comments under `# 2.`: `if`, then `elif`, then `else`, each line indented under its "
                    "branch. *Lower than* is `<`.",
                    "Exactly enough must cast, so the not-enough questions leave the boundary out: `9 < 9` is `False`.",
                    "Both short? Python takes the first true branch, so the affinity question goes first, the way "
                    "`cast_spell` did.",
                    "Write `if affinity < required:`, then `elif mana < cost:`, then `else:`, each with its "
                    "line under it.",
                ],
                checks=[
                    barrier_check("each spell gets one line, in cast_spell's order",
                                  {"S": s_line, "M": m_line, "C": c_line}, [
                        (vals(m=big_m, a=big_a), "C", "A caster with plenty of both should reach the barrier line."),
                        (vals(m=big_m, a=affinity - 5), "S", "Low affinity should get the not-skilled line."),
                        (vals(m=mana - 6, a=big_a), "M", "Low mana should get the not-enough-mana line."),
                        (vals(m=mana - 6, a=affinity - 5), "S",
                         "Both are short here, and cast_spell answered with the not-skilled line."),
                        (vals(), "C", "Exactly enough mana and affinity should still cast."),
                        (vals(a=affinity - 1), "S", "Low affinity should get the not-skilled line."),
                        (vals(m=mana - 1), "M", "Low mana should get the not-enough-mana line."),
                        (vals(big_m, big_m, big_a - 1, big_a), "S", typed),
                        (vals(big_m - 1, big_m, big_a, big_a), "M", typed),
                        (vals(big_m, big_m, big_a, big_a), "C", typed),
                    ], base=vals(), lean=True),
                ],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        partials=[program(can)],
        assemble=dict(
            lines=[line for line in solution.splitlines() if line.strip() and not line.lstrip().startswith("#")],
            distractors=["can_cast = mana >= cost or affinity >= required", "elif mana <= cost:", "if mana < cost:"],
        ),
        another_way=[
            dict(angle="picture", text=(
                "```text\naffinity lower? -> not skilled\n  no\nmana lower?     -> not enough mana\n  no\n"
                "else            -> the barrier holds\n```")),
            dict(angle="step-by-step", text=(
                "1. `can_cast`: two questions with `>=`, joined by `and`. 2. The chain: `if` affinity is lower, "
                "`elif` mana is lower, `else` cast. 3. Exactly enough? `9 < 9` is `False`, so it casts.")),
            dict(angle="campaign", label="You've seen this", text=(
                "`cast_spell` asked about affinity, then mana, then cast. It used `<`, not `<=`, because a caster with "
                "exactly enough mana can still cast.")),
        ],
        campaign_link=dict(
            module="friends-in-low-places",
            part="hold-the-barrier",
            snippet=(
                'if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:\n    ...\n'
                'elif caster["mana"] < spell["mana_cost"]:\n    ...\nelse:\n    ...'
            ),
            why=(
                "You have seen this. You just rebuilt `cast_spell`'s chain with plain boxes: affinity first, then "
                "mana, then `else`, with `<` so exactly enough still casts. Same shape, now yours."
            ),
        ),
        takeaway="`and` needs both. In a chain the first true branch wins, so order matters; `<` lets exactly enough cast.",
        wrong_answers=[
            dict(why="the starter (can_cast still the starter's False)", code=starter, fails_at=1,
                 message_contains="still holds the starter's `False`"),
            dict(why="or instead of and", code=program(can.replace(" and ", " or "), chain), fails_at=1,
                 message_contains="is one short here, so the spell should not cast"),
            dict(why="> instead of >= (exactly enough fails)", code=program(can.replace(">=", ">"), chain), fails_at=1,
                 message_contains="Exactly enough mana and affinity should cast here"),
            dict(why="== instead of >= (more than enough fails)", code=program(can.replace(">=", "=="), chain),
                 fails_at=1, message_contains="More than enough mana and affinity should cast too"),
            dict(why="True typed (worked out by hand)", code=program("can_cast = True", chain), fails_at=1,
                 message_contains="values you typed"),
            dict(why="the starter's numbers typed into the question",
                 code=program(f"can_cast = mana >= {mana} and affinity >= {affinity}", chain), fails_at=1,
                 message_contains="the answer did not follow them"),
            dict(why="only the mana asked", code=program("can_cast = mana >= cost", chain), fails_at=1,
                 message_contains="`affinity` is one short"),
            dict(why="== for = (the answer asked, then forgotten)",
                 code=program("can_cast = False\ncan_cast == mana >= cost and affinity >= required", chain), fails_at=1,
                 message_contains="`==` only asks"),
            dict(why="=> instead of >=", code=program("can_cast = mana => cost and affinity => required", chain),
                 fails_at=0, message_contains="invalid syntax"),
            dict(why="can_cast done, the chain not built yet", code=program(can), fails_at=2,
                 message_contains="Only one of the three lines should print"),
            dict(why="<= in the chain (exactly enough fizzles)", code=program(can, chain.replace(" < ", " <= ")),
                 fails_at=2, message_contains="Exactly enough mana and affinity should still cast"),
            dict(why="mana asked first (both short says not enough mana)",
                 code=program(can, "if mana < cost:\n" f"    print(\"{m_line}\")\n" "elif affinity < required:\n"
                              f"    print(\"{s_line}\")\n" "else:\n" f"    print(\"{c_line}\")\n"),
                 fails_at=2, message_contains="cast_spell answered with the not-skilled line"),
            dict(why="two separate ifs (the else joins the second)",
                 code=program(can, chain.replace("elif mana", "if mana")), fails_at=2,
                 message_contains="Only one of the three lines should print"),
            dict(why="the starter's numbers typed into the chain",
                 code=program(can, chain.replace("affinity < required", f"affinity < {affinity}")
                              .replace("mana < cost", f"mana < {mana}")),
                 fails_at=2, message_contains="the answer did not follow them"),
            dict(why="the signs turned around (> for <)", code=program(can, chain.replace(" < ", " > ")), fails_at=2,
                 message_contains="plenty of both should reach the barrier line"),
            dict(why="a line reworded", code=program(can, chain.replace(c_line, c_line.rstrip(".!") + " now.")),
                 fails_at=2, message_contains="None of the three lines from the starter printed"),
            dict(why="an elif with no if above it", code=program(can, chain.replace("if affinity", "elif affinity", 1)),
                 fails_at=0, message_contains="invalid syntax"),
            dict(why="elif after else",
                 code=program(can, "if affinity < required:\n" f"    print(\"{s_line}\")\n" "else:\n"
                              f"    print(\"{c_line}\")\n" "elif mana < cost:\n" f"    print(\"{m_line}\")\n"),
                 fails_at=0, message_contains="invalid syntax"),
            dict(why="else with a condition", code=program(can, chain.replace("else:", "else mana >= cost:")),
                 fails_at=0, message_contains="expected ':'"),
            dict(why="the colon left off the elif", code=program(can, chain.replace("elif mana < cost:", "elif mana < cost")),
                 fails_at=0, message_contains="expected ':'"),
            dict(why="= in the if", code=program(can, chain.replace("affinity < required", "affinity = required")),
                 fails_at=0, message_contains="=="),
            dict(why="a line not indented under its branch",
                 code=program(can, chain.replace(f"    print(\"{m_line}\")", f"print(\"{m_line}\")")), fails_at=0,
                 message_contains="indented block"),
        ],
        notes=_qc_meta("and-or-not,elif-chain,boundary", "", "", form) + "\n"
        f"QC2 C3, form {form} (teacher ruling: QC2 must ask for `and`, an elif chain and the exact boundary, so it "
        f"is an honest fast path). {hero} casts {spell}: the starter's numbers are exactly enough on both "
        "(mana = cost, affinity = required), so a `<=` or a `>` shows on the first Run. CP1 is u02b's 2B-06 check "
        "(from the boxes, the starter's `False` named, then CMB at exact, one short each, more than enough, and a "
        "moved spell, so `or`, `>`, `==`, `True` and typed numbers all fail). CP2 rebuilds the campaign's "
        "`cast_spell` (friends-in-low-places / hold-the-barrier) with plain boxes, no `def` yet: the three print "
        "lines are fixed starter text (no typing slips; any line reworded fails with 'as they are'). 10 reruns: "
        "plenty, low affinity, low mana, both low (order: affinity first, as cast_spell did), exactly enough (`<` "
        "not `<=`), one short each, then a moved spell. Exactly one of the three lines must print (two separate "
        "`if`s fail). The pass line is the QC's three-beat recap and offers Three Roads as the stretch. "
        "explainer='lean'.",
    )


QC2_A = dict(
    kind="testout",
    id="qc2-a",
    title="Quick Check 2 · Form A",
    optional=True,
    minutes=15,
    summary=(
        "Three short tasks and four questions, no hints. Pass all three tasks and get 3 of the 4 questions right "
        "to test out of Unit 2. Stuck on one? The lessons teach all of it, and tasks you pass here stay ticked."
    ),
    questions_to_pass=3,
    exercises=[
        _qc_roll("A", 20, 13, "Bomb Shell climbs the old wall.", "That wall hates me."),
        _qc_mend("A", "option 1", "option 2", "Mar'tu: Then we take the jeep.", "Mar'tu: Then we walk."),
        _qc_barrier("A", "Oogrish", "Lantern Ward", 9, 9,
                    ("Oogrish isn't skilled enough.", "Oogrish doesn't have enough mana.", "The barrier holds."),
                    "Mar'tu: Bomb Shell rolled for the wall. You mended our choices. Oogrish held the barrier. "
                    "That is Unit 2, yes? Want a stretch? Try Three Roads to the Institute."),
    ],
    notes=(
        "Quick Check 2, form A (code tasks). Questions live in qc2-a-questions. Pass = every code task plus 3 of "
        "the 4 questions; a retake draws form B. The site gates on both (questions_to_pass=3: the Unit 2 play-through "
        "found the unit tested out with no question answered, and the questions are the only place `not` and the "
        "first-true-wins predict appear). The code tasks still cover the unit on their own (teacher ruling on the "
        "Unit 2 reviews: C3 added, and a quiet `.lower()` slip in C2). Check messages are lean, like the explainer: "
        "the slip and the evidence, never the fix (u02c `_leaned`), so a task can't be passed by following them. Coverage (lint d): compare, boundary -> Q1 (fails on > "
        "thinking), C1 (BND: WA `>`) and C3 (WA `<=`, `>`); elif-chain -> Q2 (first true wins), C2 (WA elif as a "
        "second if) and C3 (WA mana first, two separate ifs); randint -> Q3 (0-8, 1-7) and C1 (WA d19, a die from "
        "0); and-or-not -> Q4 (and read as or) and C3 (WA `or`, only the mana asked); if-else -> C1 (WA no else, "
        "else with a condition, missing colon); read-traceback, quote-text -> C2 (each slip left crashes); compare "
        "(`.lower()`) -> C2 CP3 (WA the copy forgotten, `.lower` with no `()`, the value typed in small letters). "
        "support='none' everywhere: no hints, tracer or compare; glossary, read-aloud, DF and the lean explainer "
        "stay on. 15 minutes (was 10)."
    ),
)

QC2_B = dict(
    kind="testout",
    id="qc2-b",
    title="Quick Check 2 · Form B",
    optional=True,
    minutes=15,
    summary=(
        "Three short tasks and four questions, no hints. Pass all three tasks and get 3 of the 4 questions right "
        "to test out of Unit 2. Stuck on one? The lessons teach all of it, and tasks you pass here stay ticked."
    ),
    questions_to_pass=3,
    exercises=[
        _qc_roll("B", 12, 8, "Gearshift lifts the fallen cart.", "Gearshift: Recalculating."),
        _qc_mend("B", "option 3", "option 4", "Mar'tu: Then we rest here.", "Mar'tu: Then we follow the river."),
        _qc_barrier("B", "Gearshift", "Ember Wall", 14, 10,
                    ("Gearshift isn't skilled enough.", "Gearshift doesn't have enough mana.", "Barrier's holding."),
                    "Mar'tu: Gearshift rolled for the cart. You mended our choices. The barrier is holding. "
                    "That is Unit 2, yes? Want a stretch? Try Three Roads to the Institute."),
    ],
    notes=(
        "Quick Check 2, form B: a d12 (needed 2 to 12), option 3 / option 4 (the quiet slip on `\"Option 4\"`), "
        "Gearshift's Ember Wall in C3 (mana 14 = cost, affinity 10 = required), and hours_left tiers in its "
        "questions. Same coverage as form A. Questions live in qc2-b-questions. Pass = every code task plus 3 of "
        "the 4 questions, and the site gates on both (questions_to_pass=3). Lean check messages. 15 minutes (was 10)."
    ),
)


def _qc_questions(form, boundary, chain, faces, logic):
    """boundary/chain/logic = (code, answer, choices, explain, notes)."""
    b_code, b_answer, b_choices, b_explain, b_notes = boundary
    c_code, c_answer, c_choices, c_explain, c_notes = chain
    l_code, l_answer, l_explain, l_notes = logic
    return dict(
        kind="quiz",
        id=f"qc2-{form.lower()}-questions",
        title=f"Quick Check 2 · Form {form} questions",
        optional=True,
        minutes=4,
        summary="Four questions that go with Quick Check 2. To pass the Quick Check, get 3 of the 4 right.",
        questions=[
            dict(type="predict", id="at-the-boundary", q="What will this print?", code=b_code, answer=b_answer,
                 choices=b_choices, explain=b_explain, notes=b_notes),
            dict(type="predict", id="first-true-wins", q="What will this print?", code=c_code, answer=c_answer,
                 choices=c_choices, explain=c_explain, notes=c_notes),
            dict(
                type="mc",
                id="dice-faces",
                q=f"Which values can `random.randint(1, {faces})` give?",
                choices=[f"0 to {faces}", f"1 to {faces - 1}", f"1 to {faces}", f"0 to {faces - 1}"],
                answer=2,
                why_wrong={
                    0: "`randint` starts at the first number you give it: 1, not 0.",
                    1: f"`randint` includes both ends, so {faces} can come up too.",
                    3: f"Both ends are included: 1 and {faces}. A d{faces} has no 0.",
                },
                explain=f"`random.randint(1, {faces})` is a d{faces}: any whole number from 1 to {faces}, both ends included.",
                notes="Skill randint. Distractors: the start-at-0 belief and the top-excluded (range-style) belief.",
            ),
            dict(type="predict", id="not-and", q="What will this print?", code=l_code, answer=l_answer,
                 choices=["True", "False"], explain=l_explain, notes=l_notes),
        ],
        notes=(
            f"Quick Check 2, form {form} questions (scored with qc2-{form.lower()}: every code task plus 3 of the 4 "
            "questions, questions_to_pass=3 on the form). The best score counts, so a retake can lift it. No hints; "
            "read-aloud and glossary stay on."
        ),
    )


QC2_A_QUESTIONS = _qc_questions(
    "A",
    (
        "needed = 12\nroll = 11\nprint(roll >= needed)\nroll = 12\nprint(roll >= needed)\nroll = 13\nprint(roll >= needed)\n",
        "False\nTrue\nTrue",
        ["False\nTrue\nTrue", "False\nFalse\nTrue", "True\nTrue\nTrue", "False\nTrue\nFalse"],
        "`>=` means *at least*. 11 is not at least 12, but 12 is, and so is 13. Exactly enough passes.",
        "Skills compare, boundary (Q1). Distractors: > thinking (12 fails), everything passes, only exactly passes.",
    ),
    (
        "roll = 18\nif roll >= 15:\n    print(\"A strong hit!\")\nelif roll >= 10:\n    print(\"A hit.\")\nelse:\n"
        "    print(\"A miss.\")\n",
        "A strong hit!",
        ["A strong hit!", "A strong hit!\nA hit.", "A hit.", "A miss."],
        (
            "18 is at least 15, so the first branch runs, and Python skips the rest. 18 is also at least 10, but "
            "only the first true branch runs. With 12 it would print `A hit.`, and with 4, `A miss.`"
        ),
        "Skill elif-chain (Q2): a value two branches accept, so it fails on 'every true branch runs' and 'the last "
        "true branch wins'. The explanation traces the other two values (12, 4).",
    ),
    8,
    (
        "mana = 12\ncost = 6\naffinity = 9\nrequired = 10\nprint(not (mana >= cost and affinity >= required))\n",
        "True",
        (
            "`mana >= cost` is True, but `affinity >= required` is False: 9 is not at least 10. `and` needs both, so "
            "the brackets give False. `not` flips it: True. Oogrish can't cast this one yet."
        ),
        "Skill and-or-not (Q4), Oogrish's affinity 9 against a spell that needs 10. Reading `and` as `or` gives "
        "False.",
    ),
)

QC2_B_QUESTIONS = _qc_questions(
    "B",
    (
        "hours_left = 1\nprint(hours_left <= 2)\nhours_left = 2\nprint(hours_left <= 2)\nhours_left = 3\n"
        "print(hours_left <= 2)\n",
        "True\nTrue\nFalse",
        ["True\nTrue\nFalse", "True\nFalse\nFalse", "True\nTrue\nTrue", "False\nTrue\nFalse"],
        "`<=` means *at most*. 1 and 2 are at most 2; 3 is not. Exactly 2 counts.",
        "Form B of at-the-boundary (hours_left tiers). Distractors: < thinking (2 fails), all True, only exactly.",
    ),
    (
        "hours_left = 2\nif hours_left <= 2:\n    print(\"red\")\nelif hours_left <= 12:\n    print(\"bright blue\")\n"
        "else:\n    print(\"calm blue\")\n",
        "red",
        ["red", "red\nbright blue", "bright blue", "calm blue"],
        (
            "2 is at most 2, so the first branch runs, and Python skips the rest. 2 is also at most 12, but only the "
            "first true branch runs. With 12 it would print `bright blue`, and with 40, `calm blue`."
        ),
        "Form B of first-true-wins (the clock chain from 2B-04).",
    ),
    12,
    (
        "mana = 26\ncost = 30\naffinity = 13\nrequired = 12\nprint(not (mana >= cost and affinity >= required))\n",
        "True",
        (
            "`mana >= cost` is False: 26 is not at least 30. `affinity >= required` is True. `and` needs both, so "
            "the brackets give False. `not` flips it: True. Lucky is 4 mana short."
        ),
        "Form B of not-and (Lucky: mana 26, affinity 13). Reading `and` as `or` gives False.",
    ),
)


# =============================================================================================
# Cheatsheet 2 "Mar'tu's Chalk Notes: Choosing"
# =============================================================================================

CHALK_NOTES_2 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Choosing",
    summary="Everything from Unit 2 on one page. Printable.",
    entries=[
        dict(concept="Yes or no: `True` and `False`", code="print(18 > 12)\nprint(6 > 15)\n", output="True\nFalse",
             note="No quotes: `True` and `False` are Python's yes and no. (Lesson: True or False, Yes?)"),
        dict(concept="`=` puts, `==` asks", code="hero = \"Lucky\"\nprint(hero == \"Lucky\")\nprint(hero == \"lucky\")\n",
             output="True\nFalse",
             note="Read `=` as *gets* and `==` as *is the same as*. Every letter, space and capital counts."),
        dict(concept="The other signs", code="print(5 != 6)\nprint(3 <= 3)\nprint(4 < 4)\n", output="True\nTrue\nFalse",
             note="`!=` is not the same as. `<` less than, `>` more than, `<=` at most, `>=` at least."),
        dict(concept="Exactly enough: `>=`", code="roll = 15\nneeded = 15\nprint(roll >= needed)\nprint(roll > needed)\n",
             output="True\nFalse", note="`>` leaves out the boundary. `>=` includes it, so exactly enough still passes."),
        dict(concept="Any capitals: `.lower()`", code="answer = \"YES\"\nprint(answer == \"yes\")\nprint(answer.lower() == \"yes\")\n",
             output="False\nTrue", note="`answer.lower()` gives a lower-case copy, so capitals stop mattering. "
             "Alone on a line, the copy is forgotten: keep it with `answer = answer.lower()`."),
        dict(concept="`if`, a colon, and an indent", code="hours_left = 2\nif hours_left < 3:\n    print(\"Get inside!\")\n",
             output="Get inside!", note="The colon says *here comes the block*. Four spaces say *this belongs to the if*. "
             "(Lesson: If the Clock Turns Red)"),
        dict(concept="`else`: otherwise",
             code="roll = 9\nneeded = 12\nif roll >= needed:\n    print(\"The latch pops open.\")\nelse:\n"
                  "    print(\"That latch hates me.\")\n",
             output="That latch hates me.", note="`else:` has no question. It runs when the `if` did not."),
        dict(concept="`elif`: the first true branch wins",
             code="hours_left = 2\nif hours_left <= 2:\n    print(\"red\")\nelif hours_left <= 12:\n    print(\"bright blue\")\n"
                  "else:\n    print(\"calm blue\")\n",
             output="red", note="Python checks from the top and runs only the first true branch. So: first, the "
             "test that lets the fewest numbers through. `else` is always last."),
        dict(concept="`and`, `or`, `not`",
             code="mana = 9\ncost = 6\naffinity = 9\nrequired = 9\nprint(mana >= cost and affinity >= required)\n"
                  "print(mana >= 20 or affinity >= 9)\nprint(not True)\n",
             output="True\nTrue\nFalse", note="`and` needs both. `or` needs one. `not` flips the answer."),
        dict(concept="Dice: `random.randint`", code="import random\nroll = random.randint(1, 20)\nprint(roll)\n",
             note="`import random` once, at the top. `random.randint(1, 20)` gives 1 to 20, both ends included."),
        dict(concept="The four-step routine", code="print(\"Rolled: \" + 7)\n",
             note="1. Read the last line. 2. Go to the line it names. 3. Check the line above, and where its boxes "
             "were made. 4. No message, but a wrong answer? Print the values. (Lesson: When Spells Fizzle)"),
        dict(concept="Error: `=` in an `if`", code="roll = 20\nif roll = 20:\n    print(\"A perfect roll!\")\n",
             note="SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='? To ask, use `==`. "
             "(`:=` puts a value in a box, like `=`.)"),
        dict(concept="Error: a missing colon", code="if mana < 6\n    print(\"Low mana.\")\n",
             note="SyntaxError: expected ':'. Every `if`, `elif` and `else` line ends with `:`."),
        dict(concept="Error: `elif` after `else`",
             code="if roll >= 15:\n    print(\"Hit.\")\nelse:\n    print(\"Miss.\")\nelif roll >= 10:\n    print(\"Graze.\")\n",
             note="SyntaxError: invalid syntax. `elif` comes before `else`. `else` is always last."),
        dict(concept="Error: a name it doesn't know", code="mana = 20\nprint(mama)\n",
             note="NameError: name 'mama' is not defined. Did you mean: 'mana'? Check the spelling, the capitals, "
             "the order, and the quotes."),
        dict(concept="Error: text and a number", code="cost = \"9\"\nprint(14 >= cost)\n",
             note="TypeError: '>=' not supported between instances of 'int' and 'str'. Take the quotes off the number."),
        dict(concept="No error, wrong answer",
             code="mana = 9\ncost = 9\nprint(mana)\nprint(cost)\nif mana > cost:\n    print(\"Cast.\")\nelse:\n"
                  "    print(\"Not enough mana.\")\n",
             output="9\n9\nNot enough mana.",
             note="A quiet bug. Print the values just before the line that decides: 9 and 9 should cast, so use `>=`."),
        dict(concept="(extra) Another way to choose: `match`",
             code="choice = \"option 2\"\nmatch choice:\n    case \"option 1\":\n        print(\"Then we leave at dawn.\")\n"
                  "    case \"option 2\":\n        print(\"Rest first, yes?\")\n    case _:\n        print(\"Hm.\")\n",
             output="Rest first, yes?", note="`case _:` catches anything else. The campaign uses `elif`, so read both. "
             "(Article: Match)"),
        dict(concept="(extra) Mar'tu's seal: `assert`",
             code="roll = 15\nneeded = 15\npassed = roll >= needed\nassert passed == True\nprint(\"Sealed.\")\n",
             output="Sealed.", note="If the seal is not true, Python stops with AssertionError. Seal the boundary. "
             "(Article: Mar'tu's Seal)"),
    ],
    notes="Cheatsheet 2 (spec items in order, then the error rows and the extras). Entries with `output` are run and "
    "checked by the harness; the dice entry has none (lint 9: never a random value in an output).",
)


ITEMS = [
    PROJECT_2P2,
    REMEMBERS_2C,
    LESSON_2C,
    EXTRA_2X,
    MARTUS_SEAL,
    QC2_A,
    QC2_A_QUESTIONS,
    QC2_B,
    QC2_B_QUESTIONS,
    CHALK_NOTES_2,
]
