"""Unit 8 "Code Challenges" ("Trials of the Yard"), part a: the framing card, the Refactor set (T-HCL "The
Hard-Coded Ledger"), the Control Flow set (T-CF-1, T-CF-2, T-CF-3) and the Lists set (T-L-1, T-L-2, T-L-3), each
core challenge followed by its advanced variant (`level="advanced"`, `variant_of=<core id>`).

Spec: design/curriculum.md, "## Unit 8 · Code Challenges (optional)": the Framing lines (Mar'tu / Lucky / Mar'tu),
the Format, the unlock-ceiling table and the u08a rows of the set table. The §7 work package lists 13 items for
u08a (T-HCL; T-CF-1/1a/2/2a/3/3a; T-L-1/1a/2/2a/3/3a); a one-minute framing card ("Trials of the Yard", an
optional article with no exercises) goes first, so 14 items. Introduces nothing.

Unlock ceilings (the spec's TRIALS gate path), checked by hand against the staging files' `introduces` (the
harness gate itself allows all of Units 1-7 here, so it cannot see a ceiling):
  T-HCL          opens after Unit 1   Unit 1 tokens only: boxes, `+ - *`, `print`. No `def`, no `if`.
  T-CF-1 .. 3a   opens after Unit 3   Units 1-3: `def`, `return`, `if/elif/else`, `and/or/not`, comparisons.
  T-L-1 .. 3a    opens after Unit 4   Units 1-4: lists, `[-1]`, slices, `len`, `.append()`. No loops, no `None`
                                      in code (u07b), no dictionaries, no `not in`.
Every starter, solution, partial, assemble line, example, predict and bonus solution (65 code fields, with the
ledger's predict and bonus) was tokenized against its ceiling: 0 violations. The framing card's Example
(`double(n)`) uses `def` and `return`, Units 1-3: the card is about `def` lines. A minus sign on a number
(`op:USub`) is a Unit 4 token, so T-CF-2a keeps every negative hour in a hidden row (check code is not
student-visible); `hours_left < 0` itself needs no minus.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. The Trials are optional practice
for anyone on a streak (and, after Unit 7, for everyone); they are framed as Oogrish's yard, never as "advanced
students only". Campaign links are "you've seen this, now you'll get it": the `cast_spell` chain
(hold-the-barrier), the trap-door checks with `return roll >= required_roll` (skill-checks), the red clock, the
chalk wall and Bomb Shell's "Thirty-two hours" guess. Every student has their own device; pair talk is optional
and every checkpoint is done solo.

Format (FORMAT.md has `level` and `variant_of`, so they are used; it has no test-table field):
  * The starter is the signature (S1): the `def` line with `pass`, then the visible tests as `print` lines under a
    "# Visible tests. They should show ..." comment and "# (With only pass, each shows None.)", so Run shows the
    student's answers next to the table. Two advanced twins, Can I Cast? Skill First and The Clock's Color:
    Flashing, have a blank-def starter for the stretch group (S0 for the `def` line): a comment names the
    function and its parameters in order ("# Write the def line yourself: ..."), then the visible tests; their
    `def` line check says "Write the `def` line with these names, letter for letter" (sig_check(own=True)).
  * Mar'tu's Learn text carries the test table as a fenced picture (visible rows, then "+ N hidden tests").
  * The test table is modeled with checkpoints and named checks: CP1 "visible tests" = the `def` line check plus
    one check per visible row (the message shows the call and both values); CP2 "hidden tests" = a typed-answer
    check plus one named check per hidden row. A hidden check's message names its LABEL ("Hidden test: an empty
    wall."), never its values: a number or a list that came back is shown as "a different number" / "a list of 2
    items"; `True`/`False`, `None`, an error name and the spec's own category words ("red", "skill") are shown.
  * T-HCL is a top-level Unit 1 script (no functions exist yet at its unlock point): CP1-CP4 are CMB per box (the
    rerun table), CP5 the printed lines against the visible rerun row, CP6 the hidden "new night" rerun.
Help ladder (FORMAT.md, the Unit 2 walkthrough conventions): hints[0] Where to look, the middle hints teach with
other names (listed in foreign_names), the last hint (Show me how) holds the step's own line in backticks (its
Start me off, when the site can cut one, is in the solution; a comparison span or a bare `def` gives none, so the
harness stays quiet). The sign rule: where the visible rows cannot tell two edge signs apart, CP1's Show me how
offers BOTH complete lines, says both pass the visible rows, and names the hidden test that decides (which sign
comes first varies from trial to trial: `>` first in Can I Cast? and Dumb Luck (both trials), the right sign first
in Skill First, The Clock's Color and Bomb Shell's Guess); CP2's Show me how gives the one right line. Where a
visible row already decides the sign (the tie rows), the sign stays. Copy-test (unit-wide rule): every Show me how
rung, pasted into the starter exactly as written (in the order given, with the indentation its words describe),
runs without a crash: no NameError, no `if`/`elif`/`else` with nothing under it. A part left to the student is
named in words only ("Then ask about `has_luck`", "under your `def` line"). Each item's notes record its probe,
and a pasted rung that does not pass everything is a wrong_answers entry ("Show me how ..., pasted"), so the
harness re-proves it on every run.
Then another_way (2+ angles), assemble (a complete program, with distractors from the class's slips), solution.
Every trial is support="light", engine False, explainer full. No Start-like-this first hints.

Check builders (each part file is plain data, so the code lives here). All check code runs in the student's
namespace after their code; every name starts with `_`, builtins come from `_B`, and calls are guarded:
  sig_check()     NAME + KEEP for the `def` line: exact name (near misses named letter for letter), exact
                  parameters in order, still a function (not overwritten with `=`). own=True (the blank-def
                  starters): "Write the `def` line with these names, letter for letter: ..." in place of "Keep the
                  `def` line from the starter".
  row_check()     one test-table row. Calls the function with deep copies (so the row can see what it did to the
                  list it was handed), print captured, a 20,000-line budget on main.py frames (a loop that never ends
                  stops the check, not the page). Diagnoses, in order: a crash (row-specific crash rules first, e.g.
                  the empty wall's IndexError; then NameError near misses of a parameter; then Python's own words);
                  `None` (print instead of return, `pass` left, no `return`, `return wall.append(...)`, a bare
                  `return`, a path with no `return`); the wrong type (`"True"` in quotes, `True` where text is
                  wanted, capitals or spaces in a text answer, a number as text); row-specific rules (the oldest
                  gap, the smallest gap, `[-3:-1]`, last minus first, `<=` at the edge, the order of a chain, ...);
                  a value read from outside the function or a parameter set again inside it (`needed = 12`); on a
                  visible row, the answer to another visible test (hard-coding); then the row's own fix. `after`
                  rules then test what the call did to the list: kept (no `.pop()`), grown in place (T-L-3), or
                  copied (T-L-3a: a new list, the original unchanged, an alias `new_wall = wall` named).
  typed_check()   first in every CP2: a comparison of a parameter with a visible test's own value (`mana == 26`,
                  `wall == [48, 47, 44]`, `first_roll >= 12`) or `return <a visible answer>` fails with "Work the
                  answer out from ..., not from the visible tests" (the spec's thresholds and defaults are allowed).
  ledger checks   (T-HCL) _rerun(values) swaps the first `name = <number>` line of each named box and runs the
                  program again in a fresh namespace (guarded the same way): "a copy of your ledger". keep_numbers:
                  the starter's numbers are unchanged (reading the rerun table backwards, as the answer to type in,
                  fails here); box_check: the box still holds the starter's answer (a refactor keeps the output)
                  and follows each rerun ("stayed 12, but should be 28"); a box whose own line has no name on its
                  right side (`3 * 4`, `12 + 10`) is told "Your line still types the numbers" and given the
                  expression (the starter's plain `lamp_cost = 12` keeps "stayed 12": it is CP1's own point);
                  lines_check: the own run still prints the four lines exactly (spaces named; a box name in quotes,
                  `print("Lamps: lamp_cost")`, gets the quotes sentence) and the rerun prints the new ones; the
                  hidden "new night" says which box or line did not follow, without its numbers. The bonus (Lucky's
                  own item) finds a new box built from two new number boxes, reruns with one changed, and needs the
                  cost to follow and a printed line to show it; the student's own names are never echoed (2.11).
Messages: the fix first, then what happened, then the evidence in brackets, about 35 words or fewer (the Unit 2
ruling). Invented values only; the student's own words are never repeated (2.11): text that came back is shown
only when it is one of the spec's own answers, `"True"`/`"False"` or digits.

The class's slips for this unit, each proven by a wrong_answers entry (the item named):
  hard-coding a visible answer (`return 44`, `return True`: the "another visible test" message, every item) and
  typing each visible test's answer behind an `if` (`if mana == 26:`, `if wall == [48, 47, 44]:`: the typed check,
  CP2 of every function trial); T-HCL's typed boxes and lines (`total = 22`, `12 + 10`, a half-typed
  `lamp_count * 4`, `print("Total: 22")`) and the one typed line the visible rerun cannot see (the hidden test);
  `<` vs `<=` at the exact edge (T-CF-1 `>`, T-CF-1a `<=` for both reasons, T-CF-2/2a `< 2` and `< 12`, T-CF-2a
  `<= 0` for broken, T-CF-3/3a `>`, T-L-2a `<= 2`, T-L-3/3a `<=`); the empty case (T-L-1a: IndexError on
  `wall[-1]`, `<= 1`, `return 0`, `print(-1)`; T-L-2a: IndexError, and max-min's ValueError path avoided by order;
  T-L-2: IndexError and `len(wall) - 3` on a short wall); the wrong type (`"True"` in quotes, `"Ok"` / `"Red"`
  capitals, `True` where `"skill"` is wanted, `str(wall[-1])`, `wall[-1:]`); printing instead of returning (every
  function trial); changing the list passed in when a new list was asked for (T-L-3a: the core solution, the alias
  `new_wall = wall`) and the reverse (T-L-3: `wall + [guess]`); a list read by `.pop()` (T-L-1, T-L-1a, T-L-2a);
  tie-breaking and order (T-CF-1a mana asked first, T-CF-2 the bright-blue branch first, T-CF-2a broken before
  flashing, T-CF-3 luck asked first, T-CF-3a reroll before first); reading the test table backwards (T-HCL: the
  rerun row's numbers typed into the ledger; T-CF-1: `cost >= mana`, the two values read in the wrong order;
  T-L-3a: the visible test's own `old` read inside the function instead of the parameter); the
  campaign's `required_roll = 12` habit (`needed = 12` inside T-CF-3/3a); `flashing == "True"` / `has_luck ==
  "True"`. Added by the Nov 14 ruling: T-HCL's line of only numbers (`3 * 4`, `12 + 10`, `30 - 22`: "still types
  the numbers") and a box name in quotes (`print("Lamps: lamp_cost")`: the quotes sentence); the blank-def twins'
  missing `def` (Python's NameError), a near-miss parameter (`afinity`, `flasing`) and a capital in the name
  (`can_Cast`, `Clock_color`); and every Show me how rung that does not pass everything, pasted word for word
  (no crash; a sign the visible rows cannot tell apart fails only its named hidden test). The other slips in the
  unit brief (KeyError, ZeroDivisionError, `effect()` passed with brackets, weak
  asserts) belong to the u08b/u08c sets.
Check-breaker pass (each hole proven by a wrong_answers entry): a typed threshold no visible test shows passed
  where every hidden row shared the visible constant (`mana > 9`, `elif mana < 7`, `affinity < 7`,
  `second_roll > 11`): new rows "a bigger spell" (T-CF-1/1a) and "other numbers, with luck" (T-CF-3/3a), plus
  `_unused()` rules that name the parameter never read; T-CF-2a had no row at 3 or 13 hours (`<= 3`, `<= 20`
  passed): the "just over" rows; T-L-3/3a's walls all fell, so `min(wall)` passed for `wall[-1]`: "a newest gap
  that is not the smallest"; T-HCL accepted a computed print line added beside the typed one (the output doubled):
  each line once. Messages sharpened: `.sort()` (SORT_RULE), `.remove()`/`.append()` on a wall that must keep its
  gaps (WALL_KEEP, `.pop()` keeps its own words), `.insert(0, ...)`, a typed position crashing on a short wall,
  `guess < 45`, "appended, then a copy handed back", and spaces inside a text answer ("bright  blue").

Phone width: fenced pictures, predict code and example code keep to 36 characters a line; so do starters and
solutions, except the `def` lines whose signature the spec fixes (`can_cast(mana, cost, affinity, required)`,
`clock_color(hours_left, flashing)`, `passes_with_luck(...)`, `which_roll(...)`) and the visible-test calls of
the four-parameter trials: a wrapped signature or call reads as broken code. They stay whole on one line.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u08a
"""

# ---------------------------------------------------------------------------------------------
# Small builders
# ---------------------------------------------------------------------------------------------


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def _fill(template, **values):
    code = template
    for key, value in values.items():
        code = code.replace(f"__{key.upper()}__", repr(value))
    return code


def _code_val(value):
    if isinstance(value, str):
        return '"' + value + '"'
    return str(value)


# ---------------------------------------------------------------------------------------------
# Shared check code for the function trials (T-CF, T-L)
# ---------------------------------------------------------------------------------------------

_T = r'''import ast as _ast
import copy as _copy
import io as _io
import sys as _sys
import builtins as _B
def _tn(_v):
    return _B.type(_v).__name__
class _Runaway(_B.BaseException):
    pass
class _Cap(_io.StringIO):
    def __init__(self):
        _io.StringIO.__init__(self)
        self.room = 20000
    def write(self, _t):
        self.room -= _B.len(_t)
        if self.room < 0:
            raise _Runaway('printed too much')
        return _io.StringIO.write(self, _t)
def _guarded(_fn):
    # A line budget on the student's own lines (main.py), so a loop that never ends inside a check stops.
    _left = [20000]
    def _tr(_f, _e, _a):
        if _f.f_code.co_filename != 'main.py':
            return None
        if _e == 'line':
            _left[0] -= 1
            if _left[0] < 0:
                raise _Runaway('ran too long')
        return _tr
    _old = _sys.gettrace()
    _sys.settrace(_tr)
    try:
        return _fn()
    finally:
        _sys.settrace(_old)
def _sh(_v):
    _k = _tn(_v)
    if _k == 'str':
        return '"' + _v + '"'
    if _k == 'list':
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    return _B.str(_v)
def _shw(_w):
    if _tn(_w) in ('int', 'float'):
        return _B.str(_w)
    return '`' + _sh(_w) + '`'
def _c(_name, _args):
    return '`' + _name + '(' + ', '.join([_sh(_a) for _a in _args]) + ')`'
def _names(_xs, _join=' and '):
    _q = ['`' + _x + '`' for _x in _xs]
    if _B.len(_q) == 1:
        return _q[0]
    return ', '.join(_q[:-1]) + _join + _q[-1]
def _edits(_a, _b):
    _row = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _ca in _B.enumerate(_a, 1):
        _new = [_i]
        for _j, _cb in _B.enumerate(_b, 1):
            _new.append(_B.min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))
        _row = _new
    return _row[-1]
def _close(_m, _w):
    # NAME: the same name except for capitals, a plural s, underscores, or 1-2 letters
    _a, _b = _m.lower(), _w.lower()
    return (_a.rstrip('s') == _b.rstrip('s') or _a.replace('_', '') == _b.replace('_', '')
            or (_a[:1] == _b[:1] and _edits(_a, _b) <= 2))
def _near(_m, _w):
    _a, _b = _m.lower(), _w.lower()
    if _B.len(_a) >= 3 and (_a in _b or _b in _a):
        return True
    return _edits(_a, _b) <= 2
def _fdef(_name):
    _found = [_n for _n in _ast.parse(_source).body if _tn(_n) == 'FunctionDef' and _n.name == _name]
    return _found[-1] if _found else None
def _call(_f, _args):
    # The function with deep copies of the arguments; _in shows what the call did to them.
    _in = _copy.deepcopy(_B.list(_args))
    _keep = _sys.stdout
    _buf = _Cap()
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _guarded(lambda: _f(*_in))
    except _Runaway as _x:
        _err = _x
    except Exception as _x:
        _err = _x
    finally:
        _sys.stdout = _keep
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    return _val, _rows, _err, _in
def _same(_v, _w):
    _nums = ('int', 'float')
    return _v == _w and (_tn(_v) == _tn(_w) or (_tn(_v) in _nums and _tn(_w) in _nums))
def _shv(_v, _cats, _hidden):
    # What came back, without the student's own words (2.11). A hidden test never shows a number or a list.
    _k = _tn(_v)
    if _v is None:
        return '`None`'
    if _k == 'bool':
        return '`' + _B.str(_v) + '`'
    if _k in ('int', 'float'):
        return 'a different number' if _hidden else _B.str(_v)
    if _k == 'list':
        if _hidden:
            return 'a list of ' + _B.str(_B.len(_v)) + (' item' if _B.len(_v) == 1 else ' items')
        if _B.all(_tn(_x) in ('int', 'float') for _x in _v):
            return '`' + _sh(_v) + '`'
        return 'a list'
    if _k == 'str':
        _s = _v.strip().lower()
        if _s in [_x.lower() for _x in _cats] or _s in ('true', 'false') or _s.lstrip('-').isdigit():
            return '`"' + _v + '"`'
        return 'other text'
    if _k == 'function':
        return 'a function'
    return 'a ' + _k
def _outer(_fd, _params):
    # names the function reads from outside: not a parameter, not made inside, not a function
    _made = _B.set(_params)
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Name' and _tn(_n.ctx) == 'Store':
            _made.add(_n.id)
    _out = []
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Name' and _tn(_n.ctx) == 'Load' and _n.id not in _made and _n.id not in _out:
            if _n.id in globals() and not _B.callable(globals()[_n.id]) and not _n.id.startswith('_'):
                _out.append(_n.id)
    return _out
def _reset(_fd, _params):
    # a parameter given a typed value inside the function (`needed = 12`)
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Assign' and _tn(_n.value) == 'Constant':
            for _t in _n.targets:
                if _tn(_t) == 'Name' and _t.id in _params:
                    return _t.id + ' = ' + _B.repr(_n.value.value)
    return ''
def _cmp_text(_fd, _name):
    # the function compares `_name` with text in quotes (`flashing == "True"`)
    if _fd is None:
        return False
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Compare':
            _parts = [_n.left] + _B.list(_n.comparators)
            if (_B.any(_tn(_p) == 'Name' and _p.id == _name for _p in _parts)
                    and _B.any(_tn(_p) == 'Constant' and _tn(_p.value) == 'str' for _p in _parts)):
                return True
    return False
def _alias(_fd, _name):
    # `new_wall = wall`: a second name for the same list
    if _fd is None:
        return False
    return _B.any(_tn(_n) == 'Assign' and _tn(_n.value) == 'Name' and _n.value.id == _name for _n in _ast.walk(_fd))
def _ret_tool(_fd):
    # `return wall.append(guess)`: a list tool that changes the list and hands back None
    if _fd is None:
        return ''
    for _n in _ast.walk(_fd):
        if (_tn(_n) == 'Return' and _n.value is not None and _tn(_n.value) == 'Call'
                and _tn(_n.value.func) == 'Attribute'
                and _n.value.func.attr in ('append', 'sort', 'insert', 'remove', 'reverse', 'extend')):
            return _n.value.func.attr
    return ''
def _unused(_fd, _params):
    # parameters the function never reads (`return mana > 9` never reads `cost`)
    if _fd is None:
        return []
    _read = _B.set(_n.id for _n in _ast.walk(_fd) if _tn(_n) == 'Name' and _tn(_n.ctx) == 'Load')
    return [_p for _p in _params if _p not in _read]
def _typed_cmp(_fd, _name):
    # `_name` compared with a typed number (`guess < 45`), not with another value
    if _fd is None:
        return False
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Compare':
            _parts = [_n.left] + _B.list(_n.comparators)
            if (_B.any(_tn(_p) == 'Name' and _p.id == _name for _p in _parts)
                    and _B.any(_tn(_p) == 'Constant' and _tn(_p.value) in ('int', 'float') for _p in _parts)):
                return True
    return False
def _calls_attr(_fd, _attr):
    # the function calls a list tool such as `.pop()`
    if _fd is None:
        return False
    return _B.any(_tn(_n) == 'Attribute' and _n.attr == _attr for _n in _ast.walk(_fd))
def _try(_cond):
    try:
        return _B.bool(_B.eval(_cond, globals()))
    except Exception:
        return False
'''

_SIG = r'''
_name, _params, _owndef = __NAME__, __PARAMS__, __OWNDEF__
_sig = '`def ' + _name + '(' + ', '.join(_params) + '):`'
_keep = ('Write the `def` line with these names, letter for letter: ' if _owndef
         else 'Keep the `def` line from the starter: ')
_defs = [_n for _n in _ast.parse(_source).body if _tn(_n) == 'FunctionDef']
_fds = [_n for _n in _defs if _n.name == _name]
if not _fds:
    _miss = [_n.name for _n in _defs if _close(_n.name, _name)]
    assert not _miss, ('Python matches names letter for letter: you wrote `' + (_miss or [''])[0] + '`, the task '
                       'needs `' + _name + '`.')
    assert False, _keep + _sig + '.'
_got = [_x.arg for _x in _fds[-1].args.args]
assert _got == _params, (_keep + _sig + '. The tests hand over their values in that order.')
assert _B.callable(globals().get(_name)), ('Keep `' + _name + '` a function: a line below the `def` gives that '
                                            'name a value with `=`.')
'''

_ROW = r'''
_name, _params, _args, _want, _label = __NAME__, __PARAMS__, __ARGS__, __WANT__, __LABEL__
_fix, _rules, _crash, _after, _others = __FIX__, __RULES__, __CRASH__, __AFTER__, __OTHERS__
_foreign, _cats, _owndef = __FOREIGN__, __CATS__, __OWNDEF__
_hidden = _label is not None
_f = globals().get(_name)
assert _B.callable(_f), (('Write the `def` line with these names, letter for letter: `def ' if _owndef
                          else 'Keep the function `' + _name + '` from the starter: `def ') + _name + '('
                         + ', '.join(_params) + '):`.')
_fd = _fdef(_name)
_a = _copy.deepcopy(_B.list(_args))
_val, _rows, _err, _in = _call(_f, _args)
def _ev(_what):
    if _hidden:
        return ' (Hidden test: ' + _label + '. ' + _what[:1].upper() + _what[1:] + '.)'
    return " (Mar'tu's check called " + _c(_name, _args) + ': ' + _what + '.)'
if _err is not None:
    _k = _tn(_err)
    _e = _k + ': ' + _B.str(_err)
    _stop = 'Python stopped with ' + ('an ' if _k[:1] in 'AEIOU' else 'a ') + _k
    _msg = ''
    for _cond, _m in _crash:
        if not _msg and _try(_cond):
            _msg = _m + _ev(_stop)
    if not _msg and _k == '_Runaway':
        _msg = 'Make the function finish: it ran too long, or printed too much.' + _ev('it never stopped')
    if not _msg and _k == 'NameError':
        _miss = _B.getattr(_err, 'name', None) or ''
        _p = [_x for _x in _params if _near(_miss, _x)]
        if _miss in _foreign:
            _msg = ('Use ' + _names(_params) + (', the value' if _B.len(_params) == 1 else ', the values')
                    + ' the function is handed: `' + _miss + '` is a name from outside this function.')
        elif _p:
            _msg = 'Use the parameter `' + _p[0] + '`, letter for letter: you wrote `' + _miss + '`.'
        else:
            _msg = 'Make `' + _miss + '` inside the function before you use it, or use ' + _names(_params) + '.'
        _msg = _msg + _ev(_stop)
    if not _msg:
        _msg = 'Mend this, then Run again: ' + _e + '.' + _ev(_stop)
    assert False, _msg
_kw = _tn(_want)
if not _same(_val, _want):
    _msg = ''
    _shown = _shv(_val, _cats, _hidden)
    _got = 'it handed back ' + _shown + ('' if _hidden else ', not ' + _shw(_want))
    _rets = [_n for _n in _ast.walk(_fd) if _tn(_n) == 'Return'] if _fd is not None else []
    if _val is None:
        _grew = _B.any(_x != _y for _x, _y in _B.zip(_in, _a))
        _tool = _ret_tool(_fd)
        if _rows:
            _msg = ('Use `return` in place of `print`, so the caller gets the answer.'
                    + _ev('it printed a line but handed back `None`'))
        elif _fd is not None and [_tn(_s) for _s in _fd.body] == ['Pass']:
            _msg = 'Replace `pass` with lines that work out the answer and `return` it.' + _ev('it handed back `None`')
        elif not _rets:
            _msg = 'Hand back the answer with `return`: the function has no `return` line.' + _ev('it handed back `None`')
        elif _tool:
            _msg = ('`.' + _tool + '()` changes the list but hands back `None`. Use it on one line, then `return` '
                    'the list on the next.' + _ev('it handed back `None`'))
        elif _B.any(_r.value is None for _r in _rets):
            _msg = 'Put the answer after `return`: on its own, `return` hands back `None`.' + _ev('it handed back `None`')
        else:
            _msg = ('Every case needs a `return`: this call reached the end of the function without one.'
                    + _ev('it handed back `None`'))
    elif _kw == 'bool' and _tn(_val) == 'str':
        _msg = "Hand back `True` or `False` with no quotes: they are Python's yes and no." + _ev(_got)
    elif _kw == 'bool' and _tn(_val) != 'bool':
        _msg = 'Hand back `True` or `False`, the answer to a comparison.' + _ev(_got)
    elif _kw == 'str' and _tn(_val) == 'bool':
        _msg = ('Hand back text in quotes, ' + _names(['"' + _x + '"' for _x in _cats], ' or ') + ', not `True` or '
                '`False`.' + _ev(_got))
    elif _kw == 'str' and _tn(_val) == 'str' and ' '.join(_val.lower().split()) == ' '.join(_want.lower().split()):
        _msg = 'Match the text exactly: every letter, space and capital counts.' + _ev(_got)
    elif _kw in ('int', 'float') and _tn(_val) == 'str':
        _msg = 'Hand back a number: no quotes, no `str()`.' + _ev(_got)
    if not _msg and not _hidden and _others:
        # PAR-CONST: a function that never reads its parameters gives every visible test one typed answer
        _ovals = [_call(_f, _x) for _x, _w in _others]
        _uses = _fd is not None and _B.any(_tn(_n) == 'Name' and _n.id in _params for _n in _ast.walk(_fd))
        if (not _uses and _B.all(_ov[2] is None and _same(_ov[0], _val) for _ov in _ovals)
                and _B.any(not _same(_w, _want) for _x, _w in _others)):
            _msg = ('Work it out from ' + _names(_params) + ': your function hands back ' + _shown
                    + ' for every visible test.' + _ev(_got))
    if not _msg:
        for _cond, _m in _rules:
            if not _msg and _try(_cond):
                _msg = _m + _ev(_got)
    if not _msg and _kw == 'list' and _tn(_val) != 'list':
        _msg = 'Hand back a list, in square brackets.' + _ev(_got)
    if not _msg and _fd is not None:
        _o = _outer(_fd, _params)
        _r = _reset(_fd, _params)
        if _o:
            _msg = ('Use ' + _names(_params) + (', the value' if _B.len(_params) == 1 else ', the values')
                    + ' the function is handed: it reads `' + _o[0] + '` from outside.' + _ev(_got))
        elif _r:
            _msg = ('Use the `' + _r.split(' ')[0] + '` the function is handed: a line inside sets it again (`'
                    + _r + '`).' + _ev(_got))
    if not _msg:
        _msg = _fix + _ev(_got)
    assert False, _msg
for _ok, _m, _what in _after:
    assert _try(_ok), _m + _ev(_what)
'''

_TYPED = r'''
_name, _params, _vals, _wants, _allowed = __NAME__, __PARAMS__, __VALS__, __WANTS__, __ALLOWED__
_fd = _fdef(_name)
_hits = []
def _litv(_p):
    try:
        return True, _ast.literal_eval(_p)
    except Exception:
        return False, None
if _fd is not None:
    for _n in _ast.walk(_fd):
        if _tn(_n) == 'Compare':
            _parts = [_n.left] + _B.list(_n.comparators)
            if _B.any(_tn(_p) == 'Name' and _p.id in _params for _p in _parts):
                for _p in _parts:
                    if _tn(_p) in ('Constant', 'List', 'UnaryOp'):
                        _ok, _v = _litv(_p)
                        if _ok and _tn(_v) in ('int', 'list') and _v in _vals and _v not in _allowed:
                            _hits.append(_n)
        if _tn(_n) == 'Return' and _n.value is not None and _tn(_n.value) in ('Constant', 'List', 'UnaryOp'):
            _ok, _v = _litv(_n.value)
            if _ok and _tn(_v) in ('int', 'list') and _v in _wants and _v not in _allowed:
                _hits.append(_n)
_hits = [_h for _h in _hits if _tn(_h) == 'Compare'] + [_h for _h in _hits if _tn(_h) != 'Compare']
_seg = (_ast.get_source_segment(_source, _hits[0]) or '').strip() if _hits else ''
assert not _hits, ('Work the answer out from ' + _names(_params) + ', not from the visible tests: `' + _seg
                   + '` is typed for one test, and the hidden tests use other values.')
'''


def sig_check(fn, params, own=False):
    """NAME + KEEP for the `def` line. own=True: the starter has no `def` line, so the student writes it."""
    return (f"the def line is {fn}({', '.join(params)})",
            _T + _fill(_SIG, name=fn, params=list(params), owndef=bool(own)))


def row_check(fn, params, args, want, *, label=None, fix, rules=(), crash=(), after=(), others=(), foreign=(),
              cats=(), own=False):
    """One test-table row. label=None: a visible row (the call and both values are shown); a label: a hidden row
    (only the label is shown). rules / crash: [(condition, message)], tried in order; after: [(ok_condition,
    message, what_happened)], tested after the value is right."""
    code = _T + _fill(
        _ROW, name=fn, params=list(params), args=tuple(args), want=want, label=label, fix=fix,
        rules=[list(r) for r in rules], crash=[list(c) for c in crash], after=[list(a) for a in after],
        others=[(tuple(a), w) for a, w in others], foreign=list(foreign), cats=list(cats), owndef=bool(own),
    )
    if label is None:
        name = f"{fn}({', '.join(_code_val(a) for a in args)}) hands back {_code_val(want)}"
    else:
        name = f"hidden test: {label}"
    return (name, code)


def _flat(values):
    out = []
    for value in values:
        if isinstance(value, bool) or isinstance(value, str):
            continue
        if isinstance(value, list):
            out.append(value)
            out.extend(v for v in value if isinstance(v, int) and not isinstance(v, bool))
        elif isinstance(value, int):
            out.append(value)
    return out


def typed_check(fn, params, visible, allowed=()):
    vals = _flat([a for row in visible for a in row["args"]])
    wants = _flat([row["want"] for row in visible])
    code = _T + _fill(_TYPED, name=fn, params=list(params), vals=vals, wants=wants, allowed=list(allowed))
    return ("worked out, not typed for the visible tests", code)


def trial(*, id, title, minutes, summary, martu, fn, params, starter, solution, visible, hidden, cp1, cp2,
          assemble, another_way, wrong_answers, partials, takeaway, notes, level="core", variant_of=None, cats=(),
          foreign=(), allowed=(), rules=(), names=None, predict=None, pair_talk=None, campaign_link=None,
          example=None, example_output=None, own_def=False, tracer=None):
    """A function trial: CP1 = the def line + the visible rows, CP2 = the typed check + the hidden rows.
    own_def=True: a blank-def starter (the student writes the `def` line; the messages say so)."""
    def rows(spec_rows, hidden):
        out = []
        for row in spec_rows:
            others = [] if hidden else [(r["args"], r["want"]) for r in spec_rows if r is not row]
            out.append(row_check(
                fn, params, row["args"], row["want"], label=row.get("label") if hidden else None, fix=row["fix"],
                rules=list(row.get("rules", ())) + list(rules), crash=row.get("crash", ()),
                after=row.get("after", ()), others=others, foreign=foreign, cats=cats, own=own_def,
            ))
        return out

    cp1_checks = [sig_check(fn, params, own=own_def)] + rows(visible, False)
    cp2_checks = [typed_check(fn, params, visible, allowed)] + rows(hidden, True)
    item = dict(
        kind="challenge",
        id=id,
        title=title,
        level=level,
        optional=True,
        minutes=minutes,
        summary=summary,
        martu=martu,
        names=names or [fn, *params],
        support="light",
        engine=False,
        starter=starter,
        checkpoints=[
            dict(id="visible-tests", text=cp1["text"], dictated=False, hints=cp1["hints"], checks=cp1_checks,
                 pass_line=cp1["pass_line"]),
            dict(id="hidden-tests", text=cp2["text"], dictated=False, hints=cp2["hints"], checks=cp2_checks,
                 pass_line=cp2["pass_line"]),
        ],
        solution=solution,
        partials=partials,
        assemble=assemble,
        another_way=another_way,
        takeaway=takeaway,
        wrong_answers=wrong_answers,
        notes=notes,
    )
    if variant_of:
        item["variant_of"] = variant_of
    for key, value in (("predict", predict), ("pair_talk", pair_talk), ("campaign_link", campaign_link),
                       ("example", example), ("example_output", example_output), ("tracer", tracer)):
        if value is not None:
            item[key] = value
    return item


def _calls(tests):
    """The visible-test lines that run (the assemble blocks drop the comments, as the player does)."""
    return [line for line in tests.splitlines() if line and not line.startswith("#")]


# The line under "They should show ..." in every starter that is `pass` plus printed visible tests.
PASS_NOTE = "# (With only pass, each shows None.)\n"


# Rule pieces shared by the list trials (conditions run inside the row check: _val came back, _args went in).
POP_KEEP = ("_in[0] == _a[0] or not _calls_attr(_fd, 'pop')",
            "Read the gaps without taking them off the wall: `.pop()` removes them.",
            "the wall it was handed lost a gap")
# Any other change to the wall it was handed (`.sort()`, `.remove()`, `.insert()`, `.append()`).
WALL_KEEP = ("_in[0] == _a[0]",
             "Read the gaps without changing the wall: a list tool inside the function changed the list it was handed.",
             "the wall it was handed changed")
KEEP_WALL = [POP_KEEP, WALL_KEEP]
# `.sort()` (Unit 4) puts the gaps in size order and changes the wall: a wrong value with it is its fault.
SORT_RULE = ("_calls_attr(_fd, 'sort')",
             "Leave out `.sort()`: it puts the gaps in size order and changes the wall. Read the wall as it stands.")

# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of code-challenges; u08b and u08c must match it exactly)
# ---------------------------------------------------------------------------------------------

UNIT = dict(
    id="code-challenges",
    order=8,
    title="Code Challenges",
    subtitle="Trials of the Yard",
    published=True,
    martu_intro=(
        "Oogrish says a weapon is learned in the yard, not in the book. These are his trials. They are optional.\n"
        "Lucky asked what is in it for him. Practice, I said. And Oogrish stops lecturing him.\n"
        "Each trial is one small function and a [[test table]]. The visible tests show the idea. The "
        "[[hidden test|hidden tests]] try other values, so a typed answer will not pass. You saw checks like these "
        "in the campaign. Now you can read them."
    ),
    goals=[
        "Write a function from its `def` line and a [[test table]]",
        "Make exactly enough count, with `>=` or `<=` at the edge",
        "Handle the [[edge case|edge cases]]: one gap, an empty wall, a tie",
        "Hand back the right kind of value: `True` or `False`, a number, a list, or text",
        "Read a [[hidden test]]'s label and find the case it tries",
        "Turn [[hard-coded]] answers into values worked out from the boxes",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

# New terms only: earlier units define return, parameter, slice, append, at least, at most and the rest. (No u08a
# prose links [[IndexError]] any more: The Newest Gap: An Empty Wall leaves the crash to its hidden test.)
# No term or alias here repeats one in any unit (checked across u01-u08c, with u07's concept_map names).
GLOSSARY = [
    dict(
        term="test table",
        aliases=["test tables", "visible test", "visible tests"],
        plain=(
            "A list of calls and what each one should hand back. Run your function on each row and compare its "
            "answer with the table."
        ),
        example="can_cast(10, 10)  ->  True",
    ),
    dict(
        term="hidden test",
        aliases=["hidden tests"],
        plain=(
            "A test you cannot see. Its label says what it tries, like an empty wall, but not its numbers. It "
            "catches answers that only fit the visible tests."
        ),
        example="Hidden test: an empty wall.",
    ),
    dict(
        term="edge case",
        aliases=["edge cases"],
        plain=(
            "A value right at the edge of a rule: exactly enough, a wall of one gap, an empty list. Bugs like to "
            "hide there, so test it."
        ),
        example="can_cast(10, 10)  # exactly enough",
    ),
    dict(
        term="hard-coded",
        aliases=["hard-code", "hard-coding", "typed answer", "typed answers"],
        plain=(
            "An answer typed in by hand instead of worked out. It is right for one test and wrong as soon as a "
            "number changes."
        ),
        example="total = 22  # hard-coded",
    ),
    dict(
        term="refactor",
        aliases=["refactoring"],
        plain="Change how code works inside, without changing what it shows.",
        example="total = 22  ->  total = lamp_cost + rope_cost",
    ),
    dict(
        term="rerun table",
        aliases=["rerun", "reruns"],
        plain=(
            "Mar'tu's check runs a copy of your code with other numbers, and says what it should print then. Your "
            "own numbers stay as they are."
        ),
        example="lamp_count = 7  ->  Lamps: 28",
    ),
]

# =============================================================================================
# The framing card
# =============================================================================================

TRIALS_INTRO = dict(
    kind="article",
    id="trials-of-the-yard",
    title="Trials of the Yard",
    optional=True,
    minutes=3,
    summary="Oogrish's trials: what they are, where to start, and how to read a test table.",
    body=(
        "Mar'tu: Oogrish says a weapon is learned in the yard, not in the book. These are his trials. They are "
        "optional.\n"
        "Lucky: What's in it for me?\n"
        "Mar'tu: Practice. And Oogrish stops lecturing you.\n"
        "Oogrish: Steady, now. Most trials give you a `def` line and a [[test table]]: some calls, and what each "
        "one should hand back. A table's [[hidden test|hidden tests]] try other values, named like *an empty "
        "wall*. A typed answer fails them.\n"
        "So: write it, Run, compare each line with the table, then make the hidden test's case yourself with a "
        "`print`. The Example below does that for `double(n)`, which is not a trial.\n"
        "First time? Start with *The Hard-Coded Ledger*, then *Can I Cast?*. Do the core trials first. An "
        "*advanced* trial is a harder twin of the trial before it.\n"
        "Some trials open early, as soon as you have the tools for them. After Unit 7, they are all open.\n"
        "Mar'tu's notes on reading a table are the last card of the unit: *How to Read a Test Table*."
    ),
    examples=[
        dict(
            code=(
                "def double(n):\n"
                "    return n * 2\n"
                "\n"
                "\n"
                "# Visible tests. They should show\n"
                "# 6, then 10.\n"
                "print(double(3))\n"
                "print(double(5))\n"
                "# Hidden test: zero.\n"
                "print(double(0))\n"
            ),
            output="6\n10\n0",
        ),
    ],
    notes=(
        "meta: path=TRIALS; kind=card; words~174; example=double(n) (neutral: no trial's answer, no edge sign; "
        "foreign_names=double,n). The spec's Framing lines, word for word (Mar'tu, Lucky, Mar'tu), plus Oogrish's "
        "routine for reading a test table in one line (the unit's objective: read test tables, the debugging "
        "habit; it replaces the old three numbered steps, which said the same at more length): write it, Run, "
        "compare line by line, then make the hidden test's case with a `print`. One worked Example walks it (2.12 "
        "rule 5: other names, labelled \"Example\"; the site's article heading says Example too): `double(3)` and "
        "`double(5)` against the comment's table, then `# Hidden test: zero.` and `print(double(0))`; output "
        "6, 10, 0 (verified by the harness). 'First time?' names the way in: the ledger (Unit 1 tokens, opens "
        "first), then Can I Cast? (the shortest function trial). The cheatsheet 'How to Read a Test Table' is the last card of "
        "the unit (u08c). The opening line is only as true as the site: it holds with the site request (the "
        "Hard-Coded Ledger open to everyone after Unit 1; the other sets on a hint-free streak, a QC pass or "
        "'Ready for more'; everything after Unit 7), and while the site gates nothing every trial is open, which "
        "does not make it false. Each trial's meta line records its set, its unlock point and its token ceiling. "
        "The example uses `def` (Unit 3): this card is about `def` lines anyway, and the ledger's own Learn text "
        "explains its rerun table in Unit 1 words."
    ),
)

# =============================================================================================
# T-HCL "The Hard-Coded Ledger" (Refactor set; opens after Unit 1; Unit 1 tokens only)
# =============================================================================================

LEDGER_START = {"lamp_count": 3, "lamp_price": 4, "rope_count": 5, "rope_price": 2, "purse": 30}
LEDGER_BOXES = ["lamp_cost", "rope_cost", "total", "change"]
LEDGER_KNOWN = list(LEDGER_START) + LEDGER_BOXES
LEDGER_LINES = ["Lamps: 12", "Rope: 10", "Total: 22", "Change: 8"]
LEDGER_LABELS = {"Lamps": "lamp_cost", "Rope": "rope_cost", "Total": "total", "Change": "change"}
TABLE_RERUN = {"lamp_count": 7, "purse": 50}
TABLE_LINES = ["Lamps: 28", "Rope: 10", "Total: 38", "Change: 12"]
NEW_NIGHT = {"lamp_count": 2, "lamp_price": 5, "rope_count": 6, "rope_price": 3, "purse": 40}
NEW_NIGHT_BOXES = {"lamp_cost": 10, "rope_cost": 18, "total": 28, "change": 12}
NEW_NIGHT_LINES = ["Lamps: 10", "Rope: 18", "Total: 28", "Change: 12"]
NEW_NIGHT_LABEL = "a new night, with every count and price changed"
LEDGER_FOREIGN = ["map_count", "map_price", "map_cost", "ink_cost", "both", "coins", "spent", "left"]
# Each box's own expression (named by the numbers-only rule: "Build it from the boxes that hold them").
LEDGER_EXPR = {"lamp_cost": "lamp_count * lamp_price", "rope_cost": "rope_count * rope_price",
               "total": "lamp_cost + rope_cost", "change": "purse - total"}
# The bonus's Teach names (not LEDGER_FOREIGN's, not the solution's nail_*).
BONUS_FOREIGN = ["seed_count", "seed_price", "seed_cost"]

_H = r'''import ast as _ast
import io as _io
import sys as _sys
import builtins as _B
def _tn(_v):
    return _B.type(_v).__name__
class _Runaway(_B.BaseException):
    pass
class _Cap(_io.StringIO):
    def __init__(self):
        _io.StringIO.__init__(self)
        self.room = 20000
    def write(self, _t):
        self.room -= _B.len(_t)
        if self.room < 0:
            raise _Runaway('printed too much')
        return _io.StringIO.write(self, _t)
def _guarded(_fn):
    _left = [20000]
    def _tr(_f, _e, _a):
        if _f.f_code.co_filename != 'main.py':
            return None
        if _e == 'line':
            _left[0] -= 1
            if _left[0] < 0:
                raise _Runaway('ran too long')
        return _tr
    _old = _sys.gettrace()
    _sys.settrace(_tr)
    try:
        return _fn()
    finally:
        _sys.settrace(_old)
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _rerun(_values):
    # The ledger again, in a fresh namespace, with the FIRST `name = <number>` line of each named box swapped.
    _t = _ast.parse(_source)
    _vals = _B.dict(_values)
    _seen = []
    for _n in _t.body:
        if (_tn(_n) == 'Assign' and _B.len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id in _vals and _n.targets[0].id not in _seen
                and _tn(_n.value) in ('Constant', 'UnaryOp')):
            _n.value = _lit(_vals[_n.targets[0].id], _n.value)
            _seen.append(_n.targets[0].id)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__', 'input': lambda *_x: ''}
    _out = _sys.stdout
    _buf = _Cap()
    _err = ''
    _sys.stdout = _buf
    try:
        _code = _B.compile(_t, 'main.py', 'exec')
        _guarded(lambda: _B.exec(_code, _ns))
    except _Runaway as _x:
        _err = 'Runaway: ' + _B.str(_x)
    except Exception as _x:
        _err = _tn(_x) + ': ' + _B.str(_x)
    finally:
        _sys.stdout = _out
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    _miss = [_k for _k in _vals if _k not in _seen]
    return _ns, _rows, _err, _miss
def _tried(_values):
    _p = ['`' + _k + ' = ' + _B.str(_v) + '`' for _k, _v in _values.items()]
    return _p[0] if _B.len(_p) == 1 else ', '.join(_p[:-1]) + ' and ' + _p[-1]
def _ev(_values, _what, _hidden=None):
    if _hidden:
        return ' (Hidden test: ' + _hidden + '. ' + _what[:1].upper() + _what[1:] + '.)'
    return " (Mar'tu's check ran a copy of your ledger with " + _tried(_values) + ': ' + _what + '.)'
def _edits(_a, _b):
    _row = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _ca in _B.enumerate(_a, 1):
        _new = [_i]
        for _j, _cb in _B.enumerate(_b, 1):
            _new.append(_B.min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))
        _row = _new
    return _row[-1]
def _close(_m, _w):
    _a, _b = _m.lower(), _w.lower()
    return (_a.rstrip('s') == _b.rstrip('s') or _a.replace('_', '') == _b.replace('_', '')
            or (_a[:1] == _b[:1] and _edits(_a, _b) <= 2))
_made = []
for _n in _ast.walk(_ast.parse(_source)):
    if _tn(_n) == 'Assign':
        for _t in _n.targets:
            if _tn(_t) == 'Name' and _t.id not in _made:
                _made.append(_t.id)
_START = __START__
_KNOWN = __KNOWN__
_g = globals()
def _miss_msg(_k):
    return ('Keep the line `' + _k + ' = ' + _B.str(_START[_k]) + "` from the starter: Mar'tu's check changes that "
            'line on a copy of your ledger, to try other numbers.')
def _box_line(_box):
    # the box's own (last) top-level `name = ...` line, or None
    _ls = [_n for _n in _ast.parse(_source).body if _tn(_n) == 'Assign'
           and _B.any(_tn(_t) == 'Name' and _t.id == _box for _t in _n.targets)]
    return _ls[-1] if _ls else None
def _typed_sum(_box):
    # `3 * 4`, `12 + 10`: only numbers and signs on the right (a plain `12` is the starter's own line, not this)
    _n = _box_line(_box)
    return (_n is not None and _tn(_n.value) not in ('Constant', 'Name')
            and not _B.any(_tn(_x) == 'Name' for _x in _ast.walk(_n.value)))
def _num_line(_l, _lab):
    _rest = _l[_B.len(_lab) + 1:].strip()
    return _l.startswith(_lab + ':') and _rest.lstrip('-').isdigit()
'''

_KEEP_NUMBERS = r'''
for _k, _v in _START.items():
    assert _k in _g, 'Keep the box `' + _k + '` from the starter: `' + _k + ' = ' + _B.str(_v) + '`.'
    assert _g[_k] == _v and _tn(_g[_k]) == 'int', (
        'Keep `' + _k + ' = ' + _B.str(_v) + "` as the starter has it: Mar'tu's check tries the table's numbers on "
        'a copy of your ledger.')
'''

_LEDGER_BOX = r'''
_box, _own, _cases, _fix, _hidden, _expr = __BOX__, __OWN__, __CASES__, __FIX__, __HIDDEN__, __EXPR__
_near = [_m for _m in _made if _m not in _KNOWN and _close(_m, _box)]
assert not _near, ('Python matches names letter for letter: you wrote `' + (_near or [''])[0] + '`, the task '
                   'needs `' + _box + '`.')
assert _box in _g, 'Keep the box `' + _box + '` from the starter.'
_have = _g[_box]
assert _tn(_have) != 'str', '`' + _box + '` holds text, because of the quotes. Numbers do not need quotes.'
assert _have == _own, ('Keep the answer the same with the starter' + chr(39) + 's numbers: `' + _box + '` should '
                       'still hold ' + _B.str(_own) + '. A refactor changes how, not what.')
for _vals, _want in _cases:
    _ns, _rows, _err, _miss = _rerun(_vals)
    assert not _miss, _miss_msg(_miss[0])
    assert not _err, ('Mend this, so the ledger runs with other numbers too.'
                      + _ev(_vals, 'Python stopped with ' + _err.split(':')[0], _hidden))
    _got = _ns.get(_box)
    if _got != _want:
        if _hidden:
            _what = '`' + _box + '` did not follow'
        else:
            _what = ('`' + _box + '` ' + ('stayed ' if _got == _own else 'became ') + _B.str(_got)
                     + ', but should be ' + _B.str(_want))
        if _typed_sum(_box):
            # the box's line is only numbers and signs: name the boxes that hold them (the line is not echoed)
            assert False, ('Your line still types the numbers, so it cannot follow a change. Build it from the '
                           'boxes that hold them: `' + _expr + '`.' + _ev(_vals, _what, _hidden))
        assert False, _fix + _ev(_vals, _what, _hidden)
'''

_LEDGER_LINES = r'''
_vals, _wants, _own_lines, _labels, _hidden = __VALS__, __WANTS__, __OWN_LINES__, __LABELS__, __HIDDEN__
_ls = _lines()
for _w in _own_lines:
    if _w not in _ls:
        _lab = _w.split(':')[0]
        _sq = [_l for _l in _ls if _l.replace(' ', '') == _w.replace(' ', '')]
        assert not _sq, ('Check the spaces in the ' + _lab + ' line: a comma inside `print(...)` already adds one '
                         'space. It should still print `' + _w + '`.')
        # a box name in quotes: the line printed the word, not what is inside the box (the task's own names only)
        _box, _num, _shown = _labels[_lab], _w.split(':')[1].strip(), ''
        for _l in _ls:
            if not _shown and _l.startswith(_lab + ':') and _l[_B.len(_lab) + 1:].strip() in _KNOWN:
                _shown = _l[_B.len(_lab) + 1:].strip()
        for _n in _ast.walk(_ast.parse(_source)):
            if (not _shown and _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'print'):
                _strs = [_a.value for _a in _n.args if _tn(_a) == 'Constant' and _tn(_a.value) == 'str']
                if _strs and _strs[0].startswith(_lab + ':'):
                    for _s in [_strs[0][_B.len(_lab) + 1:]] + _strs[1:]:
                        if not _shown and _s.strip() in _KNOWN:
                            _shown = _s.strip()
        if _shown:
            _line = '`print("' + _lab + ':", ' + _box + ')`'
            _do = ('Take `' + _box + '` out of the quotes and put it after the comma: ' if _shown == _box
                   else 'Put `' + _box + '` after the comma, out of the quotes: ')
            assert False, (_do + _line + '. Quotes mean these exact letters. No quotes means look inside the box '
                           'with this label. (It printed the word `' + _shown + '`, not ' + _num + '.)')
        assert False, ('Keep the output the same: the ledger should still print `' + _w + '` with the starter'
                       + chr(39) + 's numbers. A refactor changes how, not what.')
_ns, _rows, _err, _miss = _rerun(_vals)
assert not _miss, _miss_msg(_miss[0])
assert not _err, ('Mend this, so the ledger runs with other numbers too.'
                  + _ev(_vals, 'Python stopped with ' + _err.split(':')[0], _hidden))
for _w in _wants:
    if _w not in _rows:
        _lab = _w.split(':')[0]
        _box = _labels[_lab]
        _mine = [_l for _l in _rows if _num_line(_l, _lab)]
        if _hidden:
            _what = 'the ' + _lab + ' line did not follow'
        elif _mine:
            _what = 'it printed `' + _mine[0] + '`, not `' + _w + '`'
        else:
            _what = 'it printed no ' + _lab + ' line with a number, not `' + _w + '`'
        assert False, 'Print `' + _box + '` in the ' + _lab + ' line, not a typed number.' + _ev(_vals, _what, _hidden)
for _w in _wants:
    # a new line added beside the typed one: each line once (the ledger must not print a stale number too)
    _lab = _w.split(':')[0]
    _mine = [_l for _l in _rows if _num_line(_l, _lab)]
    if _B.len(_mine) > 1:
        _stale = [_l for _l in _mine if _l != _w]
        if _hidden:
            _what = 'it printed ' + _B.str(_B.len(_mine)) + ' ' + _lab + ' lines'
        elif _stale:
            _what = 'it printed `' + _stale[0] + '` as well as `' + _w + '`'
        else:
            _what = 'it printed `' + _w + '` ' + _B.str(_B.len(_mine)) + ' times'
        assert False, ('Replace the typed ' + _lab + ' line, do not add a second one: the ledger prints each line '
                       'once.' + _ev(_vals, _what, _hidden))
'''


def _ledger_pre():
    return _fill(_H, start=dict(LEDGER_START), known=list(LEDGER_KNOWN))


KEEP_NUMBERS = ("the starter's own numbers are kept", _ledger_pre() + _KEEP_NUMBERS)


def ledger_box(label, box, own, cases, fix, hidden=None):
    return (label, _ledger_pre() + _fill(_LEDGER_BOX, box=box, own=own, cases=[(dict(v), w) for v, w in cases],
                                         fix=fix, hidden=hidden, expr=LEDGER_EXPR[box]))


def ledger_lines(label, values, wants, own_lines=(), hidden=None):
    return (label, _ledger_pre() + _fill(_LEDGER_LINES, vals=dict(values), wants=list(wants),
                                         own_lines=list(own_lines), labels=dict(LEDGER_LABELS), hidden=hidden))


# Lucky's bonus: an item of the student's own. Any names: the check finds, from the code, a new box built from two
# new boxes that hold numbers, reruns with one of them changed, and needs the cost to follow and a printed line
# (not one of the ledger's four) to show the new cost. The student's own names are never echoed (2.11).
_LEDGER_BONUS = r'''
_labels = __LABELS__
_t = _ast.parse(_source)
_nums = {}
for _n in _t.body:
    if (_tn(_n) == 'Assign' and _B.len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
            and _n.targets[0].id not in _KNOWN and _n.targets[0].id not in _nums
            and _tn(_n.value) == 'Constant' and _tn(_n.value.value) in ('int', 'float')):
        _nums[_n.targets[0].id] = _n.value.value
assert _B.len(_nums) >= 2, ('Add two new boxes for your item, each holding a number: how many, and the price of '
                            'one. Any item, any names.')
_costs = []
for _n in _t.body:
    if (_tn(_n) == 'Assign' and _B.len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
            and _n.targets[0].id not in _KNOWN and _n.targets[0].id not in _nums):
        _used = []
        for _x in _ast.walk(_n.value):
            if _tn(_x) == 'Name' and _x.id in _nums and _x.id not in _used:
                _used.append(_x.id)
        if _B.len(_used) >= 2:
            _costs.append((_n.targets[0].id, _used))
assert _costs, ('Add a cost box for your item, built from your two new boxes, the way `lamp_cost` is built from '
                '`lamp_count` and `lamp_price`.')
_moved, _err, _shown = False, '', False
for _c, _used in _costs:
    for _u in _used:
        if _moved:
            break
        _ns, _rows, _e, _miss = _rerun({_u: _nums[_u] + 2})
        if _e:
            _err = _err or _e
            continue
        if _c in _ns and _c in _g and _ns[_c] != _g[_c]:
            _moved = True
            _mine = [_l for _l in _rows if _l.split(':')[0] not in _labels]
            _shown = _B.any(_B.str(_ns[_c]) in _l.replace(',', ' ').split() for _l in _mine)
assert _moved or not _err, ("Mend this, so your ledger runs with other numbers too. (Mar'tu's check ran a copy "
                            'of your ledger with one of your new boxes changed: Python stopped with '
                            + _err.split(':')[0] + '.)')
assert _moved, ("Build your cost box from your two new boxes, so it follows them. (Mar'tu's check ran a copy of "
                'your ledger with one of them changed: your cost box stayed the same.)')
assert _shown, ('Print your cost box on its own line, after a comma, the way `print("Lamps:", lamp_cost)` does. '
                "(Mar'tu's check ran a copy of your ledger with one of your new boxes changed: no line showed the "
                'new cost.)')
'''


def ledger_bonus(label):
    return (label, _ledger_pre() + _fill(_LEDGER_BONUS, labels=dict(LEDGER_LABELS)))


LEDGER_HEAD = (
    "# Lucky's ledger: right tonight,\n"
    "# but the answers are typed in.\n"
    "lamp_count = 3\n"
    "lamp_price = 4\n"
    "rope_count = 5\n"
    "rope_price = 2\n"
    "purse = 30\n"
    "\n"
)
L_LAMP = ("lamp_cost = 12\n", "lamp_cost = lamp_count * lamp_price\n")
L_ROPE = ("rope_cost = 10\n", "rope_cost = rope_count * rope_price\n")
L_TOTAL = ("total = 22\n", "total = lamp_cost + rope_cost\n")
L_CHANGE = ("change = 8\n", "change = purse - total\n")
P_LAMP = ('print("Lamps: 12")\n', 'print("Lamps:", lamp_cost)\n')
P_ROPE = ('print("Rope: 10")\n', 'print("Rope:", rope_cost)\n')
P_TOTAL = ('print("Total: 22")\n', 'print("Total:", total)\n')
P_CHANGE = ('print("Change: 8")\n', 'print("Change:", change)\n')


def _ledger(lamp=0, rope=0, total=0, change=0, p_lamp=0, p_rope=0, p_total=0, p_change=0, head=LEDGER_HEAD, **swap):
    """The ledger with each line typed (0) or worked out (1); swap= replaces a line by its starter text."""
    parts = [L_LAMP[lamp], L_ROPE[rope], L_TOTAL[total], L_CHANGE[change], "\n",
             P_LAMP[p_lamp], P_ROPE[p_rope], P_TOTAL[p_total], P_CHANGE[p_change]]
    code = head + "".join(parts)
    for old, new in swap.values():
        code = code.replace(old, new)
    return code


LEDGER_STARTER = _ledger()
LEDGER_SOLUTION = _ledger(1, 1, 1, 1, 1, 1, 1, 1)
assert LEDGER_STARTER.count("\n") == 17
# Lucky's bonus, Mar'tu's version: one more item at the end, not added to `total` (the Total line must not move).
LEDGER_BONUS_LINES = (
    "\n"
    "nail_count = 2\n"
    "nail_price = 3\n"
    "nail_cost = nail_count * nail_price\n"
    'print("Nails:", nail_cost)\n'
)
LEDGER_BONUS_SOLUTION = LEDGER_SOLUTION + LEDGER_BONUS_LINES

HARD_CODED_LEDGER = dict(
    kind="challenge",
    id="hard-coded-ledger",
    title="The Hard-Coded Ledger",
    level="core",
    optional=True,
    minutes=11,
    summary="A refactor: make Lucky's typed answers show their working, so the ledger follows any numbers.",
    martu=(
        "Lucky's shopping ledger prints the right numbers tonight. Look closer: four boxes and four lines have "
        "their answers typed in. Change one count, and the ledger lies.\n"
        "Make every typed answer show its working, built from the box names, not the numbers inside them. The "
        "output must stay the same. That is a [[refactor]].\n"
        "Mar'tu's [[rerun table|rerun]] tries `lamp_count = 7` and `purse = 50`. Then your ledger should print:\n"
        "```text\nLamps: 28\nRope: 10\nTotal: 38\nChange: 12\n```\n"
        "+ 1 hidden test: a new night\n"
        "Mar'tu's check makes these changes on a copy of your ledger. Leave your own numbers as they are."
    ),
    names=["lamp_cost", "rope_cost", "total", "change", "lamp_count", "lamp_price", "rope_count", "rope_price",
           "purse"],
    support="light",
    engine=False,
    starter=LEDGER_STARTER,
    predict=dict(
        q="Lucky buys 7 lamps. What does this print now?",
        code='lamp_count = 7\nprint("Lamps: 12")\n',
        choices=["Lamps: 28", "Lamps: 12"],
        answer=1,
        explain=(
            "A typed number never moves: that line prints 12 whatever `lamp_count` holds. That is the bug you are "
            "about to fix."
        ),
    ),
    pair_talk="Pair talk: point at one typed number and tell your partner which boxes it really comes from.",
    checkpoints=[
        dict(
            id="lamp-cost",
            text="Make `lamp_cost` show its working: build it from the box names `lamp_count` and `lamp_price`, "
                 "not the numbers in them.",
            dictated=False,
            hints=[
                "`lamp_cost` is what all the lamps cost: how many lamps, times the price of one. Which two boxes "
                "hold those?",
                "Build it from the boxes, so the code does the math: `map_cost = map_count * map_price` multiplies "
                "what is inside the two boxes.",
                "Write `lamp_cost = lamp_count * lamp_price` in place of `lamp_cost = 12`.",
            ],
            checks=[
                KEEP_NUMBERS,
                ledger_box("lamp_cost follows the lamp boxes", "lamp_cost", 12,
                           [({"lamp_count": 7}, 28), ({"lamp_price": 5}, 15)],
                           "Build `lamp_cost` from `lamp_count` and `lamp_price`, so it follows them both."),
            ],
            pass_line="Lucky: Seven lamps, and it still adds up? Fine. Less work for me.",
        ),
        dict(
            id="rope-cost",
            text="Make `rope_cost` show its working too.",
            dictated=False,
            hints=[
                "Find `rope_cost = 10`. It is the rope count times the price of one coil.",
                "The same shape as the lamp line, with the rope boxes: count times price.",
                "Write `rope_cost = rope_count * rope_price` in place of `rope_cost = 10`.",
            ],
            checks=[
                ledger_box("rope_cost follows the rope boxes", "rope_cost", 10,
                           [({"rope_count": 4}, 8), ({"rope_price": 3}, 15)],
                           "Build `rope_cost` from `rope_count` and `rope_price`, so it follows them both."),
            ],
            pass_line="Mar'tu: Two lines that think for themselves. Good.",
        ),
        dict(
            id="total",
            text="Make `total` add the two cost boxes.",
            dictated=False,
            hints=[
                "The total is the lamp cost plus the rope cost. Which two boxes hold those?",
                "Boxes add like numbers: `both = map_cost + ink_cost` adds what is inside them.",
                "Write `total = lamp_cost + rope_cost` in place of `total = 22`.",
            ],
            checks=[
                ledger_box("total follows both costs", "total", 22,
                           [({"lamp_count": 7}, 38), ({"rope_count": 1}, 14)],
                           "Build `total` from `lamp_cost` and `rope_cost`, so a change to either one counts."),
            ],
            pass_line="Gearshift: Visor dims. The total follows the parts. That is how it should be.",
        ),
        dict(
            id="change",
            text="Make `change` show its working: what is left of `purse` after `total`.",
            dictated=False,
            hints=[
                "The change is what is left in `purse` after Lucky pays the `total`. Which two boxes hold those?",
                "Take away with `-`: `left = coins - spent` keeps what is left over.",
                "Write `change = purse - total` in place of `change = 8`.",
            ],
            checks=[
                ledger_box("change follows the purse and the total", "change", 8,
                           [({"purse": 50}, 28), ({"lamp_count": 7, "purse": 50}, 12)],
                           "Build `change` from `purse` and `total`, so it follows them both."),
            ],
            pass_line="Lucky: Change I can count on. Literally.",
        ),
        dict(
            id="print-the-boxes",
            text="Make the four lines print the boxes, so the rerun table's numbers show up.",
            dictated=False,
            hints=[
                "Each `print` line types its number. Which box holds each one?",
                "A comma in `print(...)` puts one space between the parts: `print(\"Maps:\", map_cost)` shows "
                "`Maps: 9` when `map_cost` holds 9.",
                "Write `print(\"Lamps:\", lamp_cost)` in place of `print(\"Lamps: 12\")`, and the same for the "
                "other three lines.",
            ],
            checks=[
                ledger_lines("the lines follow the rerun table", TABLE_RERUN, TABLE_LINES, own_lines=LEDGER_LINES),
            ],
            pass_line="Mar'tu: The table's numbers, on your screen, and you typed none of them. Yes.",
        ),
        dict(
            id="new-night",
            text="Pass the hidden test: a new night, with every count and price changed.",
            dictated=False,
            hints=[
                "The visible rerun only changed `lamp_count` and `purse`. Look for a line it could not see.",
                "The rope numbers did not change in the table, so a typed Rope line still looked right. The hidden "
                "test changes the rope too.",
                "Make every line print its box, like `print(\"Rope:\", rope_cost)`.",
            ],
            checks=[
                *[ledger_box(f"hidden test: {box} on a new night", box, own, [(NEW_NIGHT, NEW_NIGHT_BOXES[box])],
                             f"Build `{box}` from the boxes, so it follows every change.", hidden=NEW_NIGHT_LABEL)
                  for box, own in zip(LEDGER_BOXES, (12, 10, 22, 8))],
                ledger_lines("hidden test: the lines on a new night", NEW_NIGHT, NEW_NIGHT_LINES,
                             hidden=NEW_NIGHT_LABEL),
            ],
            pass_line=("Mar'tu: The visible rerun never changed the rope. Only the hidden test could prove your Rope "
                       "line. Nothing typed, nothing to lie."),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Add your own item to the ledger: a count box, a price box, a cost box built from those two, and its "
            "own print line. Any item, any names. Leave the four lines and `total` as they are."
        ),
        hints=[
            "Look at the lamp lines: a count box, a price box, a cost box built from them, and a print line. Your "
            "item needs the same four, at the end.",
            "Any names work, one word with `_` for spaces: `seed_count = 6` and `seed_price = 2` hold numbers, and "
            "`seed_cost = seed_count * seed_price` builds the cost from them.",
            "Add four lines at the end, for example `nail_count = 2`, `nail_price = 3`, "
            "`nail_cost = nail_count * nail_price` and `print(\"Nails:\", nail_cost)`.",
        ],
        checks=[ledger_bonus("your own item follows its boxes, and prints")],
        solution=LEDGER_BONUS_SOLUTION,
    ),
    solution=LEDGER_SOLUTION,
    partials=[
        _ledger(1),
        _ledger(1, 1),
        _ledger(1, 1, 1),
        _ledger(1, 1, 1, 1),
        _ledger(1, 1, 1, 1, 1, 0, 1, 1),
    ],
    assemble=dict(
        lines=[line for line in LEDGER_SOLUTION.splitlines() if line and not line.startswith("#")],
        distractors=["total = 22", "lamp_cost = 3 * 4", 'print("Total: 22")'],
    ),
    another_way=[
        dict(angle="picture", label="Typed or worked out", text=(
            "```text\nline             with 7 lamps\nlamp_cost = 12   still 12\n"
            "lamp_cost =      28\n  lamp_count *\n  lamp_price\n```\n"
            "A typed number never moves. A line built from the boxes follows them.")),
        dict(angle="everyday", label="A receipt and a till", text=(
            "A receipt written by hand is right for one shop visit. A till works it out again every time. Make each "
            "line a till, not a receipt.")),
        dict(angle="step-by-step", text=(
            "1. `lamp_cost` from the two lamp boxes. 2. `rope_cost` from the two rope boxes. 3. `total` adds the "
            "costs. 4. `change` takes `total` from `purse`. 5. Each `print` shows its box.")),
        dict(angle="campaign", label="You've seen this", text=(
            "In `hold-the-barrier`, one check was called *the spell's own cost is used*. It tried another cost, so "
            "a typed `- 10` failed. This ledger's checks work the same way.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "The campaign's check *the spell's own cost is used* swapped in another spell. A typed cost would "
            "have failed it. Build it from the boxes, and every check like that passes."
        ),
    ),
    takeaway="Typed answers are right once. Build every answer from the boxes, and it stays right when they change.",
    wrong_answers=[
        dict(why="the starter: every answer typed (its plain `lamp_cost = 12` keeps the rerun's words: CP1's point)",
             code=LEDGER_STARTER, fails_at=1,
             message_contains="(Mar'tu's check ran a copy of your ledger with `lamp_count = 7`: `lamp_cost` stayed "
                              "12, but should be 28.)"),
        dict(why="the rerun table read backwards: its numbers typed into the ledger (lamp_count = 7, lamp_cost = 28)",
             code=_ledger(swap_a=("lamp_count = 3\n", "lamp_count = 7\n"), swap_b=("lamp_cost = 12\n", "lamp_cost = 28\n")),
             fails_at=1, message_contains="Keep `lamp_count = 3`"),
        dict(why="worked out by hand as math (3 * 4), not from the boxes",
             code=_ledger(swap=("lamp_cost = 12\n", "lamp_cost = 3 * 4\n")), fails_at=1,
             message_contains="still types the numbers"),
        dict(why="half typed: lamp_count * 4 (the price typed)",
             code=_ledger(swap=("lamp_cost = 12\n", "lamp_cost = lamp_count * 4\n")), fails_at=1,
             message_contains="ran a copy of your ledger with `lamp_price = 5`"),
        dict(why="the wrong sign: count + price",
             code=_ledger(swap=("lamp_cost = 12\n", "lamp_cost = lamp_count + lamp_price\n")), fails_at=1,
             message_contains="should still hold 12"),
        dict(why="a near-miss box name (the old box keeps its typed 12)",
             code=_ledger(swap=("lamp_cost = 12\n", "lamp_cost = 12\nlamp_cst = lamp_count * lamp_price\n")),
             fails_at=1, message_contains="you wrote `lamp_cst`"),
        dict(why="the rope cost left typed", code=_ledger(1), fails_at=2, message_contains="`rope_cost` stayed 10"),
        dict(why="the total typed as a sum of the answers (12 + 10)",
             code=_ledger(1, 1, swap=("total = 22\n", "total = 12 + 10\n")), fails_at=3,
             message_contains="still types the numbers"),
        dict(why="the total half typed (lamp_cost + 10)",
             code=_ledger(1, 1, swap=("total = 22\n", "total = lamp_cost + 10\n")), fails_at=3,
             message_contains="ran a copy of your ledger with `rope_count = 1`"),
        dict(why="the change typed as a sum (30 - 22)",
             code=_ledger(1, 1, 1, swap=("change = 8\n", "change = 30 - 22\n")), fails_at=4,
             message_contains="still types the numbers"),
        dict(why="the change left typed as the starter has it: a plain number keeps the rerun's own words",
             code=_ledger(1, 1, 1), fails_at=4, message_contains="`change` stayed 8, but should be 28"),
        dict(why="every print line typed (the boxes all fixed)", code=_ledger(1, 1, 1, 1), fails_at=5,
             message_contains="it printed `Lamps: 12`, not `Lamps: 28`"),
        dict(why="the change line still typed", code=_ledger(1, 1, 1, 1, 1, 1, 1, 0), fails_at=5,
             message_contains="Print `change` in the Change line"),
        dict(why="the box name inside the quotes: print(\"Lamps: lamp_cost\") prints the word, not the box",
             code=_ledger(1, 1, 1, 1, 0, 1, 1, 1, swap=('print("Lamps: 12")\n', 'print("Lamps: lamp_cost")\n')),
             fails_at=5, message_contains="Take `lamp_cost` out of the quotes and put it after the comma"),
        dict(why="the box name in its own quotes after the comma: print(\"Lamps:\", \"lamp_cost\")",
             code=_ledger(1, 1, 1, 1, 0, 1, 1, 1, swap=('print("Lamps: 12")\n', 'print("Lamps:", "lamp_cost")\n')),
             fails_at=5, message_contains="out of the quotes"),
        dict(why="another box's name in quotes (Rope: \"rope_count\"): the line's own box named, the word shown",
             code=_ledger(1, 1, 1, 1, 1, 0, 1, 1, swap=('print("Rope: 10")\n', 'print("Rope:", "rope_count")\n')),
             fails_at=5, message_contains="Put `rope_cost` after the comma, out of the quotes"),
        dict(why="a comma and a space inside the quotes (two spaces: Total:  22)",
             code=_ledger(1, 1, 1, 1, 1, 1, 1, 1, swap=('print("Total:", total)\n', 'print("Total: ", total)\n')),
             fails_at=5, message_contains="Check the spaces in the Total line"),
        dict(why="a new print line added under the typed one (the old line still prints its stale number)",
             code=_ledger(1, 1, 1, 1, 1, 1, 1, 1, swap=('print("Lamps:", lamp_cost)\n',
                                                        'print("Lamps: 12")\nprint("Lamps:", lamp_cost)\n')),
             fails_at=5, message_contains="it printed `Lamps: 12` as well as `Lamps: 28`"),
        dict(why="the four new print lines added at the end, the typed ones kept (the output doubles)",
             code=LEDGER_SOLUTION + 'print("Lamps: 12")\nprint("Rope: 10")\nprint("Total: 22")\nprint("Change: 8")\n',
             fails_at=5, message_contains="Replace the typed Lamps line, do not add a second one"),
        dict(why="the Rope line typed: the visible rerun cannot see it (only the hidden test changes the rope)",
             code=_ledger(1, 1, 1, 1, 1, 0, 1, 1), fails_at=6,
             message_contains="Hidden test: a new night, with every count and price changed. The Rope line did not follow"),
        dict(why="change built with a typed rope cost (passes the visible reruns, fails the new night)",
             code=_ledger(1, 1, 1, 1, 1, 1, 1, 1, swap=("change = purse - total\n",
                                                        "change = purse - lamp_cost - 10\n")),
             fails_at=6, message_contains="`change` did not follow"),
        dict(why="text glued to a number with + (no str())",
             code=_ledger(1, 1, 1, 1, 1, 1, 1, 1, swap=('print("Total:", total)\n', 'print("Total: " + total)\n')),
             fails_at=0, message_contains="can only concatenate str"),
    ],
    notes=(
        meta(starter_level="S0-refactor", path="TRIALS", set="T-HCL", opens_after="unit-1", ceiling="unit-1",
             skills="combine-values,cmb,read-test-table", solo="false", dictates="",
             foreign_names=",".join(LEDGER_FOREIGN), bonus_foreign_names=",".join(BONUS_FOREIGN),
             reruns="CP1 lamp_count=7,lamp_price=5; CP2 rope_count=4,"
             "rope_price=3; CP3 lamp_count=7,rope_count=1; CP4 purse=50,(lamp_count=7,purse=50); CP5 table "
             "(lamp_count=7,purse=50); CP6 hidden new night (2,5,6,3,40)") + "\n"
        "Spec: 'A working Unit 1 script full of 68-style literals (lantern_cost = 12, total = 22, a typed status "
        "line). It prints the right thing but fails the rerun table until every literal that should be an "
        "expression becomes one. Checks: CMB per line; a hidden test reruns with new counts.' The boxes are "
        "renamed lamp_* (not lantern_*) so every solution line fits a phone (36 characters); the numbers are 1C's "
        "own (3 x 4 + 5 x 2 = 22), so it is a 'you've seen this' moment. Unit 1 words only: box, show your "
        "working, build it from the boxes; no `def`, no `if` (ceiling Unit 1). Evidence: everyone hard-coded 68 on "
        "the worksheet (A-05, A-07, A-08 total_cost = 68; A-07's margin plan typed 48 + 20), which is what CP1-CP4 "
        "catch; 'leave your own numbers as they are' answers the rerun-table-read-as-answer slip (CP1's first "
        "check). The visible rerun table never changes the rope, so a typed Rope line passes CP5 and only the "
        "hidden 'new night' catches it: the unit's lesson that visible tests cannot prove everything. A comma "
        "print and a `+ str()` print both pass (exact lines). 6 checkpoints, one action each.\n"
        "Teacher ruling (Nov 14): the Learn text shows only what the ledger should print after Mar'tu's rerun "
        "(lamp_count = 7, purse = 50), not a two-column fence that lined `lamp_count = 7` up beside `Lamps: 28` "
        "(read as input = output); 'built from the box names, not the numbers inside them'; the evidence bracket "
        "says 'ran a copy of your ledger with ...' (the copy is what the check changes). The predict (Unit 1 "
        "tokens, answer 1) shows a typed line not moving when `lamp_count` changes: the bug before the fix. Where "
        "to look asks what each box MEANS (all the lamps: how many times the price of one), not which numbers "
        "multiply to 12, so the hint is not number-hunting. Two signature slips get their own words: a line of "
        "only numbers and signs (`3 * 4`, `12 + 10`, `30 - 22`: 'Your line still types the numbers ... Build it "
        "from the boxes that hold them: `lamp_count * lamp_price`', the line itself never echoed; the starter's "
        "plain `lamp_cost = 12` keeps 'stayed 12', CP1's own point) and a box name in quotes (`print(\"Lamps: "
        "lamp_cost\")` or `print(\"Lamps:\", \"lamp_cost\")`: the 2.9 quotes sentence word for word, then "
        "'(It printed the word `lamp_cost`, not 12.)'; a box name is the task's own name, so 2.11 allows it). The "
        "new night's pass line says why only the hidden test could prove the Rope line.\n"
        "Bonus (Lucky, optional): an item of the student's own, any names (lint e: Mar'tu's nail_* is one of "
        "many). It is NOT added to `total`: that would move the Total line and fail CP3/CP5's same-output checks. "
        "The check finds a new box built from two new number boxes in the code, reruns with one of them changed "
        "(+2), and needs the cost to follow and a line other than the ledger's four to show the new cost. Its "
        "messages never echo the student's names. Probed: Mar'tu's bonus solution passes CP1-CP6 and the bonus; "
        "the plain solution fails the bonus ('Add two new boxes'); a typed cost (`nail_cost = 6`), a cost from one "
        "new box and a typed number, and a typed print line each fail it with their own message. Teach names "
        "seed_* (BONUS_FOREIGN).\n"
        "Show-rung copy-test (each last hint pasted into the starter word for word): CP1 `lamp_cost = lamp_count * "
        "lamp_price` in place of `lamp_cost = 12` runs, passes CP1 and stops at CP2 (the rope still typed: "
        "partial 1); CP2, CP3 and CP4's single lines and CP5's four print lines, each pasted on its own into the "
        "starter, run without a crash (the earlier typed boxes then fail the earlier checkpoint, as they should); "
        "CP6's `print(\"Rope:\", rope_cost)` runs. The bonus's last hint, its four lines added at the end of the "
        "solution, passes everything."
    ),
)

# =============================================================================================
# Control Flow set (opens after Unit 3; Units 1-3 tokens): T-CF-1, T-CF-2, T-CF-3 and their variants
# =============================================================================================

# ---- T-CF-1 can_cast(mana, cost) ----

CAST_TESTS = (
    "# Visible tests. They should show\n"
    "# True, then False.\n"
    + PASS_NOTE +
    "print(can_cast(26, 10))\n"
    "print(can_cast(6, 10))\n"
)


def _cast(body):
    return "def can_cast(mana, cost):\n" + body + "\n\n" + CAST_TESTS


CAST_SOLUTION = _cast("    return mana >= cost\n")
CAST_FIX = "Hand back whether `mana` covers `cost`: `True` when it does, `False` when it does not."
CAST_SWAP = ("_same(_call(_f, [_args[1], _args[0]])[0], _want) and _args[0] != _args[1]",
             "Check which value is which: the first one handed over is `mana`, the second is `cost`.")
COST_UNREAD = ("'cost' in _unused(_fd, _params)",
               "Compare `mana` with `cost`: your function never reads `cost`, so a bigger spell changes nothing.")

CAN_CAST = trial(
    id="can-cast",
    title="Can I Cast?",
    minutes=6,
    summary="`can_cast(mana, cost)`: `True` when the mana covers the cost. Exactly enough counts.",
    martu=(
        "Bomb Shell wants a yes or no before every cast. Write `can_cast(mana, cost)`. It hands back `True` when "
        "`mana` covers `cost`, and `False` when it does not. [[exactly enough|Exactly enough]] counts.\n"
        "```text\ncall              hands back\ncan_cast(26, 10)  True\ncan_cast(6, 10)   False\n"
        "+ 4 hidden tests\n```\n"
        "Run, and compare your answers with the table. Then the hidden tests try other numbers."
    ),
    fn="can_cast",
    params=["mana", "cost"],
    predict=dict(
        q="Before you write: what will these two lines print?",
        code="print(10 >= 10)\nprint(10 > 10)\n",
        choices=["True\nTrue", "False\nFalse", "False\nTrue", "True\nFalse"],
        answer=3,
        explain=(
            "`>=` means *at least*, and 10 is at least 10. `>` means *more than*, and 10 is not more than 10. "
            "Exactly enough needs `>=`."
        ),
    ),
    pair_talk="Pair talk: before you Run, tell your partner which hidden test `>` would fail, and why.",
    tracer=True,
    starter=_cast("    pass\n"),
    solution=CAST_SOLUTION,
    visible=[
        dict(args=(26, 10), want=True, fix=CAST_FIX, rules=[CAST_SWAP]),
        dict(args=(6, 10), want=False, fix=CAST_FIX, rules=[CAST_SWAP]),
    ],
    hidden=[
        dict(label="plenty of mana", args=(40, 25), want=True,
             fix="Compare `mana` with `cost`, whatever numbers come in.", rules=[CAST_SWAP]),
        dict(label="exactly enough mana", args=(10, 10), want=True,
             fix="Exactly enough should pass. Which sign means *at least*?"),
        dict(label="one mana short", args=(9, 10), want=False,
             fix="One short must fail: the mana does not cover the cost."),
        dict(label="a bigger spell, not enough mana", args=(20, 25), want=False, rules=[CAST_SWAP],
             fix="Compare `mana` with the `cost` the function is handed: a bigger spell needs more mana."),
    ],
    cp1=dict(
        text="Make the two visible tests hand back `True`, then `False`.",
        hints=[
            "Read row 1 of the table: 26 mana and a cost of 10. Does 26 cover 10?",
            "A comparison is already `True` or `False`, so a function can hand it back as it is: "
            "`return speed > limit`.",
            "Write `return mana > cost` or `return mana >= cost` in place of `pass`. Both pass these two rows. The "
            "hidden test *exactly enough mana* decides which is right.",
        ],
        pass_line="Bomb Shell: Yes or no. Good. I like short answers.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests: plenty of mana, exactly enough, one short, and a bigger spell.",
        hints=[
            "Read the labels. Which one sits on the edge, where the mana and the cost are the same?",
            "`>` means *more than*, and `>=` means [[at least]]. `10 > 10` is `False`, but `10 >= 10` is `True`.",
            "Use `return mana >= cost`: exactly enough passes, and one short fails.",
        ],
        pass_line="Oogrish: Steady, now. Exactly enough is enough. Remember that at the barrier.",
    ),
    foreign=["speed", "limit"],
    rules=[COST_UNREAD],
    assemble=dict(
        lines=["def can_cast(mana, cost):", "    return mana >= cost", *_calls(CAST_TESTS)],
        distractors=["    return mana > cost", "    print(mana >= cost)", '    return "True"'],
    ),
    another_way=[
        dict(angle="everyday", label="A ticket", text=(
            "A ticket costs 10 coins. With 12 coins you get in. With exactly 10 you get in too. With 9 you wait "
            "outside. *Covers* means at least the cost.")),
        dict(angle="step-by-step", text=(
            "1. Compare `mana` with `cost` using `>=`. 2. That comparison is already `True` or `False`. 3. Hand it "
            "back with `return`. One line does all three.")),
        dict(angle="campaign", label="You've seen this", text=(
            "`return roll >= required_roll` in the trap-door checks handed back a comparison, too. `can_cast` is "
            "the same shape with mana.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "`cast_spell` asked the opposite question: is the mana *lower than* the cost? It used `<`, not `<=`, "
            "so exactly enough still cast. `can_cast` asks it the other way round, with `>=`."
        ),
    ),
    takeaway="A comparison is already `True` or `False`: hand it back. `>=` lets exactly enough through.",
    partials=[_cast("    return mana > cost\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_cast("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="> for >= (exactly enough fails): the campaign's < vs <= slip", code=_cast("    return mana > cost\n"),
             fails_at=2, message_contains="Exactly enough should pass"),
        dict(why='"True" in quotes', code=_cast('    if mana >= cost:\n        return "True"\n    else:\n'
                                                '        return "False"\n'),
             fails_at=1, message_contains="no quotes"),
        dict(why="print instead of return", code=_cast("    print(mana >= cost)\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the table's two values read in the wrong order (cost >= mana)", code=_cast("    return cost >= mana\n"),
             fails_at=1, message_contains="Check which value is which"),
        dict(why="each visible test's answer typed behind an if (A-06 test values)",
             code=_cast("    if mana == 26:\n        return True\n    return False\n"), fails_at=2,
             message_contains="`mana == 26` is typed for one test"),
        dict(why="the visible cost typed (mana >= 10)", code=_cast("    return mana >= 10\n"), fails_at=2,
             message_contains="`mana >= 10`"),
        dict(why="hard-coded True", code=_cast("    return True\n"), fails_at=1,
             message_contains="for every visible test"),
        dict(why="an if with no else (False never handed back)", code=_cast("    if mana >= cost:\n        return True\n"),
             fails_at=1, message_contains="Every case needs a `return`"),
        dict(why="a number, not True or False (mana - cost)", code=_cast("    return mana - cost\n"), fails_at=1,
             message_contains="the answer to a comparison"),
        dict(why="the parameters renamed", code=_cast("    return mana >= cost\n").replace(
            "def can_cast(mana, cost):\n    return mana >= cost", "def can_cast(m, c):\n    return m >= c"),
             fails_at=1, message_contains="Keep the `def` line"),
        dict(why="one short let through (cost - 1)", code=_cast("    return mana >= cost - 1\n"), fails_at=2,
             message_contains="One short must fail"),
        dict(why="a typed threshold no visible test shows (mana > 9): cost never read, so only a bigger spell "
                 "catches it", code=_cast("    return mana > 9\n"), fails_at=2,
             message_contains="your function never reads `cost`"),
        dict(why="a typed threshold (mana > 20): the cost never read", code=_cast("    return mana > 20\n"),
             fails_at=2, message_contains="Hidden test: exactly enough mana"),
        dict(why="Show me how (CP1), pasted with its first sign, `>`: no crash, both visible rows pass; the hidden "
                 "test exactly enough mana decides", code=_cast("    return mana > cost\n"), fails_at=2,
             message_contains="Exactly enough should pass. Which sign means *at least*? (Hidden test: exactly "
                              "enough mana. It handed back `False`.)"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-1", opens_after="unit-3",
             ceiling="units-1-3", skills="compare,return-bool,boundary,read-test-table", solo="false", dictates="",
             foreign_names="speed,limit", tests="visible=(26,10)->True,(6,10)->False; hidden=plenty (40,25), "
             "exactly enough (10,10), one short (9,10), a bigger spell (20,25)") + "\n"
        "Spec: T-CF-1 `can_cast(mana, cost)` -> True when the mana covers the cost (exactly enough counts). The "
        "hidden 'plenty' row comes first so a typed answer gets the typed check or 'plenty', not the boundary "
        "message. Evidence: the campaign's `<` vs `<=` (hold-the-barrier: 'exactly enough mana still casts'); "
        "test values typed in (A-06, A-02 `return 500`: 7 of 11 typed numbers into the function), caught by the "
        "typed check and the 'another visible test' message; `cost >= mana` is the test row read in the wrong "
        "order (the swap rule calls the function with the two values swapped). Check-breaker: `return mana > 9` "
        "never reads `cost` and passed every row while three of four costs were 10 (9 is no visible value, so "
        "the typed check cannot see it); the 'bigger spell' row (20, 25) and the COST_UNREAD rule catch it. "
        "Both CPs goal-only. tracer=True: a student can step through and watch `return` hand back the comparison. "
        "Predict answer index 3 (the unit mixes the right answer's place). Sign rule: the visible rows (26, 10) "
        "and (6, 10) cannot tell `>` from `>=`, so CP1's Show me how offers both lines, `>` first, and names "
        "*exactly enough mana*; CP2's gives `>=` alone. Show-rung copy-test: CP1 `return mana > cost` and `return "
        "mana >= cost`, each pasted in place of `pass`: no crash, both pass CP1; `>` fails CP2 at exactly enough "
        "mana (wrong answer 'Show me how ..., pasted with its first sign'; also partial 1), `>=` is the solution. "
        "CP2 `return mana >= cost` in place of `pass`: the solution."
    ),
)

# ---- T-CF-1a can_cast(mana, cost, affinity, required) -> "ok" / "skill" / "mana" ----

CAST2_TESTS = (
    "# Visible tests. They should show\n"
    "# ok, skill, mana.\n"
    "print(can_cast(26, 10, 13, 8))\n"
    "print(can_cast(26, 10, 6, 8))\n"
    "print(can_cast(5, 10, 13, 8))\n"
)
CAST2_DEF = "def can_cast(mana, cost, affinity, required):\n"
# The blank-def starter (the stretch group writes the `def` line): the comment names it, then the visible tests.
CAST2_HEAD = (
    "# Write the def line yourself:\n"
    "# can_cast, with mana, cost,\n"
    "# affinity and required, in order.\n"
)
CAST2_STARTER = CAST2_HEAD + "\n\n" + CAST2_TESTS


def _cast2(body):
    return CAST2_HEAD + CAST2_DEF + body + "\n\n" + CAST2_TESTS


CAST2_BODY = (
    "    if affinity < required:\n"
    "        return \"skill\"\n"
    "    elif mana < cost:\n"
    "        return \"mana\"\n"
    "    else:\n"
    "        return \"ok\"\n"
)
CAST2_MANA_FIRST = (
    "    if mana < cost:\n"
    "        return \"mana\"\n"
    "    elif affinity < required:\n"
    "        return \"skill\"\n"
    "    else:\n"
    "        return \"ok\"\n"
)
CAST2_CATS = ["ok", "skill", "mana"]
CAST2_UNREAD = [
    ("'cost' in _unused(_fd, _params)",
     "Compare `mana` with `cost`: your function never reads `cost`, so a bigger spell changes nothing."),
    ("'required' in _unused(_fd, _params)",
     "Compare `affinity` with `required`: your function never reads `required`, so a harder spell changes "
     "nothing."),
]

CAN_CAST_SKILL_FIRST = trial(
    id="can-cast-skill-first",
    title="Can I Cast? Skill First",
    level="advanced",
    variant_of="can-cast",
    minutes=8,
    summary="The advanced twin of Can I Cast?: hand back `\"ok\"`, `\"skill\"` or `\"mana\"`, asking about skill first.",
    martu=(
        "Now the full rule from `cast_spell`. Hand back the reason, as text:\n"
        "1. `\"skill\"` when `affinity` is below `required`. When both are low, the reason is `\"skill\"`.\n"
        "2. `\"mana\"` when `mana` is below `cost`.\n"
        "3. `\"ok\"` when neither is true.\n"
        "Exactly enough counts, for both.\n"
        "```text\ncall                     back\ncan_cast(26, 10, 13, 8)  \"ok\"\ncan_cast(26, 10, 6, 8)   \"skill\"\n"
        "can_cast(5, 10, 13, 8)   \"mana\"\n+ 5 hidden tests\n```\n"
        "Write `can_cast(mana, cost, affinity, required)` yourself, `def` line and all."
    ),
    fn="can_cast",
    params=["mana", "cost", "affinity", "required"],
    own_def=True,
    starter=CAST2_STARTER,
    solution=_cast2(CAST2_BODY),
    cats=CAST2_CATS,
    visible=[
        dict(args=(26, 10, 13, 8), want="ok", fix="Hand back `\"ok\"` when the skill and the mana are both enough."),
        dict(args=(26, 10, 6, 8), want="skill", fix="Hand back `\"skill\"` when `affinity` is below `required`."),
        dict(args=(5, 10, 13, 8), want="mana", fix="Hand back `\"mana\"` when `mana` is below `cost`."),
    ],
    hidden=[
        dict(label="low skill and low mana", args=(5, 10, 6, 8), want="skill",
             fix="Ask about skill first: when both are low, the reason is `\"skill\"`."),
        dict(label="exactly enough mana", args=(10, 10, 13, 8), want="ok",
             fix="Exactly enough mana should cast. *Below* means `<`, not `<=`."),
        dict(label="exactly enough skill", args=(26, 10, 8, 8), want="ok",
             fix="Exactly enough skill should cast. *Below* means `<`, not `<=`."),
        dict(label="other numbers", args=(40, 25, 9, 12), want="skill",
             fix="Compare the parameters, whatever numbers come in."),
        dict(label="a bigger spell, not enough mana", args=(20, 25, 14, 9), want="mana",
             fix="Hand back `\"mana\"` when `mana` is below the `cost` the function is handed, whatever it is."),
    ],
    cp1=dict(
        text="Write the function, `def` line and all, so the visible tests hand back `\"ok\"`, `\"skill\"` and "
             "`\"mana\"`.",
        hints=[
            "Each visible row is short of one thing at most. Row 2 is low on skill: 6 is below 8.",
            "An `if` / `elif` / `else` chain can hand back a different text from each branch:\n```python\n"
            "if speed < 3:\n    return \"slow\"\nelif speed < 8:\n    return \"fair\"\nelse:\n"
            "    return \"fast\"\n```",
            "Under the comments, write the `def` line: `def can_cast(mana, cost, affinity, required):`. Under it, "
            "start the chain with `if affinity < required:` or `if affinity <= required:`, with `return "
            "\"skill\"` under that. Then ask about `mana` and `cost` with `elif`. Both signs pass the visible "
            "rows. The hidden tests for *exactly enough* decide the sign.",
        ],
        pass_line="Mar'tu: Three answers, three reasons. Like the barrier, yes?",
    ),
    cp2=dict(
        text="Pass the 5 hidden tests, including low skill *and* low mana, exactly enough of each, and a bigger "
             "spell.",
        hints=[
            "Read the label *low skill and low mana*. Which reason should win?",
            "The first true branch wins. So the question that must win goes first: skill, then mana.",
            "Under your `def` line, ask `if affinity < required:` with `return \"skill\"` under it, then `elif "
            "mana < cost:` with `return \"mana\"` under it, then `else:` with `return \"ok\"`. Use `<`, not "
            "`<=`: exactly enough is not below.",
        ],
        pass_line="Oogrish: Skill first. Mana second. You held the barrier the same way.",
    ),
    foreign=["speed"],
    rules=CAST2_UNREAD,
    assemble=dict(
        lines=CAST2_DEF.splitlines() + CAST2_BODY.splitlines() + _calls(CAST2_TESTS),
        distractors=["    if mana < cost:", "    elif mana <= cost:", "        return False"],
    ),
    another_way=[
        dict(angle="picture", label="The chain, top to bottom", text=(
            "```text\naffinity < required?\n  yes -> \"skill\"  (stop)\nmana < cost?\n  yes -> \"mana\"   (stop)\n"
            "else  -> \"ok\"\n```")),
        dict(angle="everyday", label="Two gates", text=(
            "Two gates stand in a row. The first checks your skill, the second your mana. If the first gate stops "
            "you, the second never asks. So the first gate's reason is the one you hear.")),
        dict(angle="campaign", label="You've seen this", text=(
            "`cast_spell` printed *isn't skilled enough* first, then *doesn't have enough mana*. Same order, same "
            "`<`. Now the function hands back the reason.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet=(
            'if caster["abilities"]["magical_affinity"] < spell["required_affinity"]:\n    ...\n'
            'elif caster["mana"] < spell["mana_cost"]:\n    ...\nelse:\n    ...'
        ),
        why=(
            "You held the barrier with this chain. Skill was asked first, then mana, with `<`, so exactly enough "
            "still cast. Your `can_cast` is the same chain, handing back the reason."
        ),
    ),
    takeaway="First true branch wins: the reason that must win is asked first. *Below* is `<`.",
    partials=[_cast2(CAST2_MANA_FIRST)],
    wrong_answers=[
        dict(why="the def missing entirely: the starter as it stands (Python's NameError at the first visible test)",
             code=CAST2_STARTER, fails_at=0, message_contains="name 'can_cast' is not defined"),
        dict(why="the def line written, the body left as pass", code=_cast2("    pass\n"), fails_at=1,
             message_contains="Replace `pass`"),
        dict(why="a near-miss parameter in the def line (afinity, used the same way in the body)",
             code=_cast2(CAST2_BODY).replace("affinity", "afinity"), fails_at=1,
             message_contains="Write the `def` line with these names, letter for letter: `def can_cast(mana, cost, "
                              "affinity, required):`"),
        dict(why="the parameters in another order (the table read in the wrong order)",
             code=_cast2(CAST2_BODY).replace(CAST2_DEF, "def can_cast(affinity, required, mana, cost):\n"),
             fails_at=1, message_contains="letter for letter"),
        dict(why="a near-miss function name (can_Cast), the visible tests changed to match",
             code=_cast2(CAST2_BODY).replace("can_cast", "can_Cast"), fails_at=1,
             message_contains="you wrote `can_Cast`"),
        dict(why="Show me how (CP1), pasted word for word with `<`: the def line, the skill question; no crash, "
                 "row 1 needs the rest", code=_cast2('    if affinity < required:\n        return "skill"\n'),
             fails_at=1, message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP1), pasted with its other sign `<=`: no crash, row 1 needs the rest",
             code=_cast2('    if affinity <= required:\n        return "skill"\n'), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP1) with `<=`, the chain finished: the visible rows pass; the hidden test exactly "
                 "enough skill decides", code=_cast2(CAST2_BODY.replace("affinity < required", "affinity <= required")),
             fails_at=2, message_contains="Hidden test: exactly enough skill"),
        dict(why="mana asked first (the order of the chain)", code=_cast2(CAST2_MANA_FIRST), fails_at=2,
             message_contains="Ask about skill first"),
        dict(why="<= for the mana (exactly enough mana fails)",
             code=_cast2(CAST2_BODY.replace("mana < cost", "mana <= cost")), fails_at=2,
             message_contains="Exactly enough mana should cast"),
        dict(why="<= for the skill (exactly enough skill fails)",
             code=_cast2(CAST2_BODY.replace("affinity < required", "affinity <= required")), fails_at=2,
             message_contains="Exactly enough skill should cast"),
        dict(why="True / False kept from the core trial",
             code=_cast2("    return mana >= cost and affinity >= required\n"), fails_at=1,
             message_contains="Hand back text in quotes"),
        dict(why='a capital letter ("Ok")', code=_cast2(CAST2_BODY.replace('"ok"', '"Ok"')), fails_at=1,
             message_contains="every letter, space and capital"),
        dict(why="print instead of return", code=_cast2(CAST2_BODY.replace("return", "print(").replace(
            '"skill"\n', '"skill")\n').replace('"mana"\n', '"mana")\n').replace('"ok"\n', '"ok")\n').replace(
            "print( ", "print(")), fails_at=1, message_contains="in place of `print`"),
        dict(why="the visible tests' values typed (affinity == 6)",
             code=_cast2("    if affinity == 6:\n        return \"skill\"\n    if mana == 5:\n"
                         "        return \"mana\"\n    return \"ok\"\n"),
             fails_at=2, message_contains="is typed for one test"),
        dict(why="a visible required value typed (affinity < 8)", code=_cast2(CAST2_BODY.replace("required:", "8:")),
             fails_at=2, message_contains="`affinity < 8`"),
        dict(why="the skill test the wrong way round (required < affinity)",
             code=_cast2(CAST2_BODY.replace("affinity < required", "required < affinity")), fails_at=1,
             message_contains="Hand back `\"ok\"` when the skill and the mana are both enough"),
        dict(why="no else (ok never handed back)",
             code=_cast2("    if affinity < required:\n        return \"skill\"\n    elif mana < cost:\n"
                         "        return \"mana\"\n"),
             fails_at=1, message_contains="Every case needs a `return`"),
        dict(why="a typed mana threshold no visible test shows (mana < 7): cost never read",
             code=_cast2(CAST2_BODY.replace("mana < cost", "mana < 7")), fails_at=2,
             message_contains="your function never reads `cost`"),
        dict(why="a typed skill threshold (affinity < 7): required never read",
             code=_cast2(CAST2_BODY.replace("affinity < required", "affinity < 7")), fails_at=2,
             message_contains="your function never reads `required`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-1a", opens_after="unit-3",
             ceiling="units-1-3", skills="elif-chain,order,boundary,return-text", solo="false", dictates="",
             foreign_names="speed", tests="visible=(26,10,13,8)ok,(26,10,6,8)skill,(5,10,13,8)mana; hidden=low skill "
             "and low mana, exactly enough mana, exactly enough skill, other numbers, a bigger spell "
             "(20,25,14,9)mana") + "\n"
        "Spec: `can_cast(mana, cost, affinity, required)` -> \"ok\", \"skill\" or \"mana\", checking skill first. "
        "Campaign link (spec): the hold-the-barrier logic. Each visible row is short of at most one thing, so the "
        "chain's ORDER is invisible there and only the hidden 'low skill and low mana' row tests it (partial 1 is "
        "the mana-first chain). Exactly enough counts for both reasons (cast_spell's `<`). The def line (45 "
        "characters) is kept whole: the signature is the spec's. Separate `if`s with returns pass too (each "
        "return ends the function). Check-breaker: every cost was 10 except in a row that hands back skill, so "
        "`elif mana < 7:` (never reading `cost`) passed everything; the 'bigger spell' row and CAST2_UNREAD "
        "catch it.\n"
        "Teacher ruling (Nov 14): a blank-def starter for the stretch group (starter_level S0 for the `def` line): "
        "the comment names `can_cast` and its parameters in order, then the visible tests, so Run stops with "
        "Python's NameError until the `def` line exists (wrong answer 1, fails_at 0). sig_check(own=True) says "
        "'Write the `def` line with these names, letter for letter: ...' (a near miss like `afinity` and the "
        "table read in another order both get it); the function-name near miss keeps 'you wrote `can_Cast`'. "
        "Learn text: 'When both are low, the reason is \"skill\"' (the order, said as the rule). Sign rule: "
        "the visible rows cannot tell `<` from `<=` for either reason, so CP1's Show me how offers both, the "
        "right one first, and names the *exactly enough* tests; CP2's gives the whole chain with `<`. The Show "
        "rungs start with a bare `def` span, so the site cuts no Start me off (the stretch group writes the line). "
        "Show-rung copy-test: CP1, the def line and the skill question pasted under the comments (with `<`, and "
        "again with `<=`): no crash, row 1 needs the rest ('Every case needs a `return`'); with the chain "
        "finished, `<=` fails only the hidden test *exactly enough skill*. CP2, its whole chain under the `def` "
        "line: the solution."
    ),
)

# ---- T-CF-2 clock_color(hours_left) ----

CLOCK_TESTS = (
    "# Visible tests. They should show\n"
    "# red, bright blue, calm blue.\n"
    + PASS_NOTE +
    "print(clock_color(1))\n"
    "print(clock_color(7))\n"
    "print(clock_color(30))\n"
)


def _clock(body):
    return "def clock_color(hours_left):\n" + body + "\n\n" + CLOCK_TESTS


CLOCK_BODY = (
    "    if hours_left <= 2:\n"
    "        return \"red\"\n"
    "    elif hours_left <= 12:\n"
    "        return \"bright blue\"\n"
    "    else:\n"
    "        return \"calm blue\"\n"
)
CLOCK_CATS = ["red", "bright blue", "calm blue"]
CLOCK_ORDER = ('_val == "bright blue" and _want == "red" and _same(_call(_f, [1])[0], "bright blue")',
               "First true wins: ask `hours_left <= 2` before `hours_left <= 12`, or 1 hour is never red.")

CLOCK_COLOR = trial(
    id="clock-color",
    title="The Clock's Color",
    minutes=6,
    summary="`clock_color(hours_left)`: red up to 2 hours, bright blue up to 12, calm blue after that.",
    martu=(
        "My Ley Clock glows `\"red\"` when 2 hours or fewer are left, `\"bright blue\"` up to 12 hours, and "
        "`\"calm blue\"` after that. Write `clock_color(hours_left)` to hand back the color.\n"
        "```text\ncall             hands back\nclock_color(1)   \"red\"\nclock_color(7)   \"bright blue\"\n"
        "clock_color(30)  \"calm blue\"\n+ 5 hidden tests\n```\n"
        "You built this chain once with a box. Now it is a function."
    ),
    fn="clock_color",
    params=["hours_left"],
    predict=dict(
        q="Before you write: what will these lines print?",
        code="hours_left = 2\nprint(hours_left < 2)\nprint(hours_left <= 2)\n",
        choices=["True\nFalse", "True\nTrue", "False\nTrue", "False\nFalse"],
        answer=2,
        explain=(
            "2 is not *less than* 2, so `<` gives `False`. 2 is [[at most]] 2, so `<=` gives `True`. Exactly 2 "
            "hours is red: use `<=`."
        ),
    ),
    starter=_clock("    pass\n"),
    solution=_clock(CLOCK_BODY),
    cats=CLOCK_CATS,
    allowed=[0, 2, 3, 12, 13],
    visible=[
        dict(args=(1,), want="red", fix="Hand back `\"red\"` when 2 hours or fewer are left.", rules=[CLOCK_ORDER]),
        dict(args=(7,), want="bright blue", fix="Hand back `\"bright blue\"` from 3 up to 12 hours."),
        dict(args=(30,), want="calm blue", fix="Hand back `\"calm blue\"` for more than 12 hours, with `else`."),
    ],
    hidden=[
        dict(label="exactly 2 hours left", args=(2,), want="red", rules=[CLOCK_ORDER],
             fix="Exactly 2 hours is still red. Which sign means *at most*?"),
        dict(label="exactly 12 hours left", args=(12,), want="bright blue",
             fix="Exactly 12 hours is still bright blue. Which sign means *at most*?"),
        dict(label="just over 2 hours", args=(3,), want="bright blue",
             fix="Just over 2 hours is bright blue: only 2 or fewer is red."),
        dict(label="just over 12 hours", args=(13,), want="calm blue",
             fix="Just over 12 hours is calm blue: only 12 or fewer is bright blue."),
        dict(label="no hours left", args=(0,), want="red", rules=[CLOCK_ORDER],
             fix="0 hours left is red too: it is fewer than 2."),
    ],
    cp1=dict(
        text="Make the three visible tests hand back their colors.",
        hints=[
            "Row 1 has 1 hour left. 1 is 2 or fewer, so it is red.",
            "In a chain, the first true branch wins. So first ask the test that lets the fewest numbers through:"
            "\n```python\nif age <= 5:\n    return \"free\"\nelif age <= 15:\n    return \"child\"\nelse:\n"
            "    return \"adult\"\n```",
            "Start with `if hours_left <= 2:` or `if hours_left < 2:`, with `return \"red\"` under it. Then "
            "`elif hours_left <= 12:` or `elif hours_left < 12:`, with `return \"bright blue\"` under it. Then "
            "`else:`, with `return \"calm blue\"` under it. Both signs pass the visible rows. The hidden edge "
            "tests at 2 and 12 hours decide the sign.",
        ],
        pass_line="Mar'tu: Red at one hour. Let us hope we never need that branch.",
    ),
    cp2=dict(
        text="Pass the 5 hidden tests: the edges at 2 and 12 hours, just past them, and 0 hours.",
        hints=[
            "The hidden tests sit on the edges: exactly 2, exactly 12, and one hour past each.",
            "*2 hours or fewer* includes 2. `hours < 2` leaves 2 out, but `hours <= 2` keeps it in.",
            "Use `if hours_left <= 2:` with `return \"red\"` under it, and `elif hours_left <= 12:` with "
            "`return \"bright blue\"` under it: `<=` both times. Then `else:`, with `return \"calm blue\"`.",
        ],
        pass_line="Oogrish: The edges are where the trouble is. You looked there. Good.",
    ),
    foreign=["age"],
    assemble=dict(
        lines=["def clock_color(hours_left):", *CLOCK_BODY.splitlines(), *_calls(CLOCK_TESTS)],
        distractors=["    if hours_left < 2:", "    elif hours_left <= 2:", "        return red"],
    ),
    another_way=[
        dict(angle="picture", label="The chain, top to bottom", text=(
            "```text\n<= 2 ?   yes -> \"red\"\n  no\n<= 12 ?  yes -> \"bright blue\"\n  no\n"
            "else  ->  \"calm blue\"\n```")),
        dict(angle="step-by-step", label="Trace 2, 7 and 13", text=(
            "1. 2 hours: `2 <= 2` is `True`. Red. 2. 7 hours: `7 <= 2` is `False`, `7 <= 12` is `True`. Bright "
            "blue. 3. 13 hours: both `False`, so the `else`. Calm blue.")),
        dict(angle="shorter", text="First true wins, so the smallest range goes first. *Or fewer* means `<=`."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="red-clock",
        why=(
            "You saw the Ley Clock flash red before the worst burst. Mar'tu reads the color off the glass. Your "
            "function works it out from the hours."
        ),
    ),
    takeaway="In a chain the first true branch wins: the smallest range first. *Or fewer* is `<=`.",
    partials=[_clock(CLOCK_BODY.replace("<= 2", "< 2"))],
    wrong_answers=[
        dict(why="the starter (pass)", code=_clock("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="the chain in the wrong order (bright blue first)",
             code=_clock("    if hours_left <= 12:\n        return \"bright blue\"\n    elif hours_left <= 2:\n"
                         "        return \"red\"\n    else:\n        return \"calm blue\"\n"),
             fails_at=1, message_contains="First true wins"),
        dict(why="< for <= at 2 (exactly 2 hours is not red)", code=_clock(CLOCK_BODY.replace("<= 2", "< 2")),
             fails_at=2, message_contains="Exactly 2 hours is still red"),
        dict(why="< for <= at 12", code=_clock(CLOCK_BODY.replace("<= 12", "< 12")), fails_at=2,
             message_contains="Exactly 12 hours is still bright blue"),
        dict(why='a capital letter ("Red")', code=_clock(CLOCK_BODY.replace('"red"', '"Red"')), fails_at=1,
             message_contains="every letter, space and capital"),
        dict(why="print instead of return",
             code=_clock(CLOCK_BODY.replace('return "red"', 'print("red")').replace(
                 'return "bright blue"', 'print("bright blue")').replace('return "calm blue"', 'print("calm blue")')),
             fails_at=1, message_contains="in place of `print`"),
        dict(why="each visible test's answer typed (hours_left == 1, == 7)",
             code=_clock("    if hours_left == 1:\n        return \"red\"\n    if hours_left == 7:\n"
                         "        return \"bright blue\"\n    return \"calm blue\"\n"),
             fails_at=2, message_contains="`hours_left == 1` is typed for one test"),
        dict(why='"blue" for "bright blue" (the words not matched)',
             code=_clock(CLOCK_BODY.replace('"bright blue"', '"blue"')), fails_at=1,
             message_contains="from 3 up to 12 hours"),
        dict(why="no else (calm blue never handed back)",
             code=_clock("    if hours_left <= 2:\n        return \"red\"\n    elif hours_left <= 12:\n"
                         "        return \"bright blue\"\n"),
             fails_at=1, message_contains="Every case needs a `return`"),
        dict(why='hard-coded "red"', code=_clock('    return "red"\n'), fails_at=1,
             message_contains="for every visible test"),
        dict(why="Show me how (CP1), pasted with its second sign, `<` both times: no crash, the visible rows "
                 "pass; the hidden test exactly 2 hours left decides",
             code=_clock(CLOCK_BODY.replace("<=", "<")), fails_at=2,
             message_contains="Exactly 2 hours is still red. Which sign means *at most*? (Hidden test: exactly 2 "
                              "hours left."),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-2", opens_after="unit-3",
             ceiling="units-1-3", skills="elif-chain,order,boundary,return-text", solo="false", dictates="",
             foreign_names="age", tests="visible=1 red, 7 bright blue, 30 calm blue; hidden=exactly 2, exactly 12, "
             "just over 2 (3), just over 12 (13), no hours (0)") + "\n"
        "Spec: T-CF-2 `clock_color(hours_left)` -> \"red\" (<= 2), \"bright blue\" (<= 12), else \"calm blue\". "
        "The function form of 2B's clock-colors (Unit 2): same order rule wording, 'the test that lets the fewest "
        "numbers through' first. The typed check allows the spec's own edges (0, 2, 3, 12, 13), so `< 3` and "
        "`< 13` pass; only a visible test's value (1, 7, 30) compared with `hours_left` is flagged. Evidence: the "
        "campaign `<` vs `<=`; 2B's wrong-order chain; capitals (2B-03 STREXACT).\n"
        "Teacher ruling (Nov 14): CP1's Show me how ended on an empty `elif` (pasted, an IndentationError), and "
        "it handed over `<=` though 1, 7 and 30 cannot tell `<` from `<=`. Now it gives every line complete, "
        "both signs for both edges (the right one first) and names the hidden edge tests at 2 and 12 hours; "
        "CP2's gives the one right chain, each branch with its `return`. Predict answer index 2. Show-rung "
        "copy-test: CP1 pasted with `<=` both times is the solution; with `<` both times (and with `<= 2`, "
        "`< 12`) it runs, passes the visible rows and fails only the hidden edge test (wrong answers 'Show me "
        "how ..., pasted' and '< for <= at 12'); CP2 pasted in place of `pass` is the solution."
    ),
)

# ---- T-CF-2a clock_color(hours_left, flashing) ----

CLOCK2_TESTS = (
    "# Visible tests. They should show\n"
    "# bright blue, red, calm blue.\n"
    "print(clock_color(7, False))\n"
    "print(clock_color(30, True))\n"
    "print(clock_color(40, False))\n"
)
CLOCK2_DEF = "def clock_color(hours_left, flashing):\n"
# The blank-def starter (the stretch group writes the `def` line), as in Can I Cast? Skill First.
CLOCK2_HEAD = (
    "# Write the def line yourself:\n"
    "# clock_color, with hours_left\n"
    "# and flashing, in order.\n"
)
CLOCK2_STARTER = CLOCK2_HEAD + "\n\n" + CLOCK2_TESTS


def _clock2(body):
    return CLOCK2_HEAD + CLOCK2_DEF + body + "\n\n" + CLOCK2_TESTS


CLOCK2_BODY = (
    "    if flashing:\n"
    "        return \"red\"\n"
    "    elif hours_left < 0:\n"
    "        return \"broken\"\n"
    "    elif hours_left <= 2:\n"
    "        return \"red\"\n"
    "    elif hours_left <= 12:\n"
    "        return \"bright blue\"\n"
    "    else:\n"
    "        return \"calm blue\"\n"
)
CLOCK2_BROKEN_FIRST = (
    "    if hours_left < 0:\n"
    "        return \"broken\"\n"
    "    elif flashing:\n"
    "        return \"red\"\n"
    "    elif hours_left <= 2:\n"
    "        return \"red\"\n"
    "    elif hours_left <= 12:\n"
    "        return \"bright blue\"\n"
    "    else:\n"
    "        return \"calm blue\"\n"
)
CLOCK2_CATS = ["red", "bright blue", "calm blue", "broken"]
FLASH_TEXT = ("_cmp_text(_fd, 'flashing')",
              "Ask `if flashing:`, with no quotes: `flashing` holds Python's `True`, not the text `\"True\"`.")

CLOCK_COLOR_FLASHING = trial(
    id="clock-color-flashing",
    title="The Clock's Color: Flashing",
    level="advanced",
    variant_of="clock-color",
    minutes=8,
    summary="The advanced twin of The Clock's Color: a flashing clock is always red, and hours below 0 are broken.",
    martu=(
        "Two new rules, on top of the old ones:\n"
        "1. When `flashing` is `True`, the clock is `\"red\"`, always. Even with broken hours.\n"
        "2. Hours below 0 are `\"broken\"`.\n"
        "Otherwise, the old colors: red up to 2 hours, bright blue up to 12, then calm blue.\n"
        "```text\ncall                   back\nclock_color(7, False)  \"bright blue\"\n"
        "clock_color(30, True)  \"red\"\nclock_color(40, False) \"calm blue\"\n+ 7 hidden tests\n```\n"
        "Write `clock_color(hours_left, flashing)` yourself, `def` line and all."
    ),
    fn="clock_color",
    params=["hours_left", "flashing"],
    own_def=True,
    starter=CLOCK2_STARTER,
    solution=_clock2(CLOCK2_BODY),
    cats=CLOCK2_CATS,
    allowed=[-2, -1, 0, 2, 3, 12, 13],
    visible=[
        dict(args=(7, False), want="bright blue", fix="Keep the old colors when the clock is not flashing."),
        dict(args=(30, True), want="red", fix="A flashing clock is always `\"red\"`: ask about `flashing` first.",
             rules=[FLASH_TEXT]),
        dict(args=(40, False), want="calm blue", fix="Keep the old colors when the clock is not flashing."),
    ],
    hidden=[
        dict(label="hours below 0", args=(-2, False), want="broken",
             fix="Hand back `\"broken\"` when `hours_left` is below 0."),
        dict(label="flashing, with broken hours", args=(-1, True), want="red",
             fix="Flashing always wins: ask about `flashing` before the broken hours."),
        dict(label="exactly 0 hours left", args=(0, False), want="red",
             fix="0 hours is not below 0, so it is not broken: it is red. *Below* means `<`."),
        dict(label="exactly 2 hours left", args=(2, False), want="red",
             fix="Exactly 2 hours is still red. Which sign means *at most*?"),
        dict(label="exactly 12 hours left", args=(12, False), want="bright blue",
             fix="Exactly 12 hours is still bright blue. Which sign means *at most*?"),
        dict(label="just over 2 hours", args=(3, False), want="bright blue",
             fix="Just over 2 hours is bright blue: only 2 or fewer is red."),
        dict(label="just over 12 hours", args=(13, False), want="calm blue",
             fix="Just over 12 hours is calm blue: only 12 or fewer is bright blue."),
    ],
    cp1=dict(
        text="Write the function, `def` line and all, so the three visible tests hand back their colors.",
        hints=[
            "Row 2 is flashing, so it is red, whatever the hours say.",
            "`flashing` already holds `True` or `False`, so `if flashing:` asks it. No `==`, no quotes:\n"
            "```python\nif raining:\n    return \"stay in\"\n```",
            "Under the comments, write the `def` line: `def clock_color(hours_left, flashing):`. Under it, start "
            "with `if flashing:`, with `return \"red\"` under that. Then the whole chain from The Clock's Color. "
            "Where the *broken* rule goes, and its sign, is for the hidden tests.",
        ],
        pass_line="Mar'tu: Flashing red. I have seen that once. Once was enough.",
    ),
    cp2=dict(
        text="Pass the 7 hidden tests. They try hours below 0, flashing with broken hours, the edges at 0, 2 and "
             "12 hours, and just past them.",
        hints=[
            "Two labels are about order and edges: *flashing, with broken hours*, and *exactly 0 hours left*.",
            "The first true branch wins, so the rule that always wins goes first. And 0 is not below 0: `0 < 0` is "
            "`False`.",
            "Under your `def` line, ask `if flashing:` first, with `return \"red\"` under it. Then `elif "
            "hours_left < 0:` with `return \"broken\"` under it. Then the old chain, from `elif hours_left <= 2:` "
            "on.",
        ],
        pass_line="Oogrish: Flashing first. When that clock flashes, nothing else matters.",
    ),
    foreign=["raining"],
    assemble=dict(
        lines=[CLOCK2_DEF.strip("\n"), *CLOCK2_BODY.splitlines(), *_calls(CLOCK2_TESTS)],
        distractors=["    if flashing == \"True\":", "    elif hours_left <= 0:", "    if hours_left < 0:"],
    ),
    another_way=[
        dict(angle="picture", label="Five questions, in order", text=(
            "```text\nflashing?      -> \"red\"\nhours < 0?     -> \"broken\"\nhours <= 2?    -> \"red\"\n"
            "hours <= 12?   -> \"bright blue\"\nelse           -> \"calm blue\"\n```")),
        dict(angle="in-tor", label="The red clock", text=(
            "When the clock flashed red, nobody read the hours. Everyone ran for the barrier. That is why "
            "`flashing` is asked first.")),
        dict(angle="shorter", text="The rule that always wins goes first. *Below 0* is `< 0`, so 0 itself is not broken."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="red-clock",
        why=(
            "The clock flashed red, then again, then again, and the burst nearly tore the barrier apart. A "
            "flashing clock is red, whatever its hand says. Your first branch says exactly that."
        ),
    ),
    takeaway="The rule that always wins goes first. `if flashing:` asks a `True` or `False` box, no quotes.",
    partials=[_clock2(CLOCK2_BROKEN_FIRST)],
    wrong_answers=[
        dict(why="the def missing entirely: the starter as it stands (Python's NameError at the first visible test)",
             code=CLOCK2_STARTER, fails_at=0, message_contains="name 'clock_color' is not defined"),
        dict(why="the def line written, the body left as pass", code=_clock2("    pass\n"), fails_at=1,
             message_contains="Replace `pass`"),
        dict(why="a near-miss parameter in the def line (flasing, used the same way in the body)",
             code=_clock2(CLOCK2_BODY).replace("flashing", "flasing"), fails_at=1,
             message_contains="Write the `def` line with these names, letter for letter: `def clock_color("
                              "hours_left, flashing):`"),
        dict(why="a capital in the def name (Clock_color), the visible tests changed to match",
             code=_clock2(CLOCK2_BODY).replace("clock_color", "Clock_color"), fails_at=1,
             message_contains="you wrote `Clock_color`"),
        dict(why="Show me how (CP1), pasted word for word: the def line and the flashing question; no crash, row 1 "
                 "needs the old chain", code=_clock2('    if flashing:\n        return "red"\n'), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP2), pasted under the def line: flashing, then broken; no crash, the old chain is "
                 "named in words", code=_clock2('    if flashing:\n        return "red"\n    elif hours_left < 0:\n'
                                                '        return "broken"\n'),
             fails_at=1, message_contains="Every case needs a `return`"),
        dict(why="the core solution kept (one parameter: the visible calls crash)",
             code="def clock_color(hours_left):\n" + CLOCK_BODY + "\n\n" + CLOCK2_TESTS, fails_at=0,
             message_contains="takes 1 positional argument but 2 were given"),
        dict(why='flashing compared with the text "True"',
             code=_clock2(CLOCK2_BODY.replace("    if flashing:", "    if flashing == \"True\":")), fails_at=1,
             message_contains="not the text"),
        dict(why="broken asked before flashing (the order)", code=_clock2(CLOCK2_BROKEN_FIRST), fails_at=2,
             message_contains="Flashing always wins"),
        dict(why="<= 0 for broken (0 hours is broken)", code=_clock2(CLOCK2_BODY.replace("< 0", "<= 0")), fails_at=2,
             message_contains="0 hours is not below 0"),
        dict(why="< 2 for <= 2", code=_clock2(CLOCK2_BODY.replace("<= 2", "< 2")), fails_at=2,
             message_contains="Exactly 2 hours is still red"),
        dict(why="no broken rule", code=_clock2(CLOCK2_BODY.replace(
            "    elif hours_left < 0:\n        return \"broken\"\n", "")), fails_at=2,
             message_contains="when `hours_left` is below 0"),
        dict(why="print instead of return", code=_clock2(CLOCK2_BODY.replace("return ", "print(").replace(
            '"\n', '")\n')), fails_at=1, message_contains="in place of `print`"),
        dict(why="a visible test's hours typed (hours_left == 7 for bright blue)",
             code=_clock2(CLOCK2_BODY.replace("hours_left <= 12", "hours_left == 7")), fails_at=2,
             message_contains="`hours_left == 7` is typed for one test"),
        dict(why="a wrong edge no other row tries (red up to 3 hours)",
             code=_clock2(CLOCK2_BODY.replace("<= 2", "<= 3")), fails_at=2,
             message_contains="Just over 2 hours is bright blue"),
        dict(why="a wrong edge between the visible rows (bright blue up to 20 hours)",
             code=_clock2(CLOCK2_BODY.replace("<= 12", "<= 20")), fails_at=2,
             message_contains="Just over 12 hours is calm blue"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-2a", opens_after="unit-3",
             ceiling="units-1-3", skills="elif-chain,order,boundary,bool-param", solo="false", dictates="",
             foreign_names="raining", tests="visible=(7,F) bright blue,(30,T) red,(40,F) calm blue; hidden=hours "
             "below 0 (-2), flashing with broken hours (-1,T), exactly 0, exactly 2, exactly 12, just over 2 (3), "
             "just over 12 (13)") + "\n"
        "Spec: negative hours -> \"broken\"; a second parameter `flashing`: when True, always \"red\" (a default "
        "value waits for the 6B-08 card, so `flashing` is required). The spec leaves 'flashing AND broken' open; "
        "'always' is read literally and the Learn text says so ('Even with broken hours'), and the hidden "
        "'flashing, with broken hours' row tests it (partial 1 asks about broken first). Exactly 0 is not "
        "negative (red). Every negative value is in a HIDDEN row: a minus sign on a number (`op:USub`) is a Unit 4 "
        "token, above this set's Units 1-3 ceiling, so no student-visible code holds one (`hours_left < 0` does "
        "not). Evidence: `== \"True\"` (2A's text-vs-bool slips), the order rule, `<` vs `<=`. The def line (38 "
        "characters) stays whole. Check-breaker: with no row at 3 or 13, `<= 3` for red and `<= 20` for bright "
        "blue passed; the 'just over' rows (the core's own) are back.\n"
        "Teacher ruling (Nov 14): a blank-def starter for the stretch group, as in Skill First (starter_level S0 "
        "for the `def` line): the comment names `clock_color`, `hours_left` and `flashing` in order; Run stops "
        "with Python's NameError until the `def` line exists. sig_check(own=True) says 'Write the `def` line with "
        "these names, letter for letter'; a capital in the name keeps 'you wrote `Clock_color`'. CP1's Show me "
        "how gives the `def` line and `if flashing:` with its `return`, names the old chain in words, and leaves "
        "the broken rule's place and sign to the hidden tests (the visible rows hold no negative hours). CP2's "
        "gives the full order, each branch with its `return`, the old chain named in words. Both start with a "
        "bare `def` span, so the site cuts no Start me off. Show-rung copy-test: CP1 pasted under the comments "
        "and CP2 pasted under the `def` line both run without a crash and stop at row 1 ('Every case needs a "
        "`return`': the old chain, named in words, is the student's part); the old chain added, both are the "
        "solution."
    ),
)

# ---- T-CF-3 passes_with_luck(first_roll, second_roll, needed, has_luck) ----

LUCK_DEF = "def passes_with_luck(first_roll, second_roll, needed, has_luck):\n"
LUCK_TESTS = (
    "# Visible tests. They should show\n"
    "# True, True, False.\n"
    + PASS_NOTE +
    "print(passes_with_luck(15, 2, 12, False))\n"
    "print(passes_with_luck(5, 14, 12, True))\n"
    "print(passes_with_luck(5, 14, 12, False))\n"
)


def _luck(body):
    return LUCK_DEF + body + "\n\n" + LUCK_TESTS


LUCK_BODY = (
    "    if first_roll >= needed:\n"
    "        return True\n"
    "    if has_luck:\n"
    "        return second_roll >= needed\n"
    "    return False\n"
)
LUCK_FIX = "Pass on the first roll, or on the reroll when `has_luck` is `True`."
LUCK_TEXT = ("_cmp_text(_fd, 'has_luck')",
             "Ask `if has_luck:`, with no quotes: `has_luck` holds Python's `True`, not the text `\"True\"`.")

PASSES_WITH_LUCK = trial(
    id="passes-with-luck",
    title="Dumb Luck",
    minutes=8,
    summary="`passes_with_luck(...)`: a skill check where Lucky may reroll once. `True` or `False`.",
    martu=(
        "Lucky can reroll a failed roll once a day. He calls it Dumb Luck. Write `passes_with_luck`, with the four "
        "parameters in the starter. It hands back `True` when:\n"
        "1. `first_roll` is at least `needed`, or\n"
        "2. the first roll fails, `has_luck` is `True`, and `second_roll` is at least `needed`.\n"
        "Otherwise it hands back `False`.\n"
        "```text\nfirst second needed has_luck back\n15    2      12     False    True\n"
        "5     14     12     True     True\n5     14     12     False    False\n+ 6 hidden tests\n```"
    ),
    fn="passes_with_luck",
    params=["first_roll", "second_roll", "needed", "has_luck"],
    starter=_luck("    pass\n"),
    solution=_luck(LUCK_BODY),
    visible=[
        dict(args=(15, 2, 12, False), want=True, fix=LUCK_FIX),
        dict(args=(5, 14, 12, True), want=True, fix=LUCK_FIX, rules=[LUCK_TEXT]),
        dict(args=(5, 14, 12, False), want=False, fix="Without luck, a failed first roll is a fail: the reroll does not count."),
    ],
    hidden=[
        dict(label="exactly enough on the first roll", args=(12, 1, 12, False), want=True,
             fix="Exactly enough passes. Which sign means *at least*?"),
        dict(label="exactly enough on the reroll", args=(3, 12, 12, True), want=True,
             fix="Exactly enough passes on the reroll too. Which sign means *at least*?"),
        dict(label="luck, but the reroll fails too", args=(3, 7, 12, True), want=False,
             fix="Luck gives a second roll, not a pass: the reroll must reach `needed` too."),
        dict(label="luck left, and the first roll passes", args=(16, 2, 12, True), want=True,
             fix="A first roll that passes is a pass, luck or not: ask about the first roll first."),
        dict(label="other numbers", args=(9, 4, 8, False), want=True,
             fix="Compare with the `needed` the function is handed, whatever it is."),
        dict(label="other numbers, with luck", args=(2, 9, 8, True), want=True,
             fix="Compare the reroll with the `needed` the function is handed, whatever it is."),
    ],
    cp1=dict(
        text="Make the three visible tests hand back `True`, `True`, then `False`.",
        hints=[
            "Row 2: the first roll, 5, fails 12. Lucky has luck, and the reroll, 14, passes. So `True`.",
            "One question at a time works well. Each `return` ends the function, so a later `if` only runs when the "
            "earlier ones said no:\n```python\nif coins >= price:\n    return True\n```",
            "With a spare purse, the shape grows by one question:\n```python\nif coins >= price:\n    return True\n"
            "if has_spare:\n    return spare_coins >= price\nreturn False\n```",
            "Start with `if first_roll > needed:` or `if first_roll >= needed:`, and `return True` under it. Then "
            "ask about `has_luck`. Both signs pass the visible rows. The hidden test *exactly enough on the first "
            "roll* decides the sign.",
        ],
        pass_line="Lucky: See? Dumb Luck. Works every time. Well. Once a day.",
    ),
    cp2=dict(
        text="Pass the 6 hidden tests. They try exactly enough on each roll, a failed reroll, luck left over, and "
             "other numbers, with and without luck.",
        hints=[
            "Read *luck, but the reroll fails too*: luck alone is not a pass.",
            "`needed` comes in with every call. A line like `needed = 12` inside the function throws that away. "
            "*At least* is `>=`.",
            "Hand back the reroll's answer only when `has_luck` is `True`: `return second_roll >= needed`.",
        ],
        pass_line="Oogrish: Luck is a second chance, not a pass. Lucky forgets that.",
    ),
    foreign=["coins", "price", "has_spare", "spare_coins"],
    assemble=dict(
        lines=[LUCK_DEF.strip("\n"), *LUCK_BODY.splitlines(), *_calls(LUCK_TESTS)],
        distractors=["    return first_roll >= needed or has_luck", "    needed = 12", "    if has_luck == \"True\":"],
    ),
    another_way=[
        dict(angle="picture", label="Two chances", text=(
            "```text\nfirst roll >= needed?\n  yes -> True\nhas_luck?\n  no  -> False\n  yes -> second roll\n"
            "         >= needed?\n```")),
        dict(angle="everyday", label="A second try", text=(
            "A door code gets one retry. If the first code works, you are in, retry or not. If it fails and you "
            "have a retry, the second code decides. No retry left: you stay out.")),
        dict(angle="step-by-step", text=(
            "1. Ask about the first roll: pass, and you are done. 2. No luck: fail. 3. With luck, the second roll "
            "decides, with the same `>=`.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def strength_check(roll):\n    required_roll = 12\n    return roll >= required_roll",
        why=(
            "You wrote the trap-door checks. `>=` let exactly 12 pass. Lucky's Dumb Luck is one more chance at the "
            "same check: a second roll, the same `>=`."
        ),
    ),
    takeaway="Ask one question at a time, and `return` as soon as you know. Luck is a second roll, not a pass.",
    partials=[_luck(LUCK_BODY.replace(">=", ">"))],
    wrong_answers=[
        dict(why="the starter (pass)", code=_luck("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="luck counted as a pass (or has_luck)", code=_luck("    return first_roll >= needed or has_luck\n"),
             fails_at=2, message_contains="Luck gives a second roll, not a pass"),
        dict(why="the reroll counted without luck",
             code=_luck("    return first_roll >= needed or second_roll >= needed\n"), fails_at=1,
             message_contains="the reroll does not count"),
        dict(why="> for >= (exactly enough fails)", code=_luck(LUCK_BODY.replace(">=", ">")), fails_at=2,
             message_contains="Exactly enough passes"),
        dict(why="luck asked first: the reroll replaces a first roll that passed",
             code=_luck("    if has_luck:\n        return second_roll >= needed\n    return first_roll >= needed\n"),
             fails_at=2, message_contains="A first roll that passes is a pass"),
        dict(why="the campaign's required_roll = 12 habit: needed set again inside",
             code=_luck("    needed = 12\n" + LUCK_BODY), fails_at=2, message_contains="a line inside sets it again"),
        dict(why="the visible needed typed (first_roll >= 12)", code=_luck(LUCK_BODY.replace(
            "first_roll >= needed", "first_roll >= 12")), fails_at=2, message_contains="`first_roll >= 12`"),
        dict(why='has_luck compared with the text "True"',
             code=_luck(LUCK_BODY.replace("    if has_luck:", "    if has_luck == \"True\":")), fails_at=1,
             message_contains="not the text"),
        dict(why='"True" in quotes', code=_luck('    if first_roll >= needed:\n        return "True"\n'
                                                '    return "False"\n'),
             fails_at=1, message_contains="no quotes"),
        dict(why="print instead of return", code=_luck("    print(first_roll >= needed)\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the reroll compared with a typed number no visible test shows (second_roll > 11)",
             code=_luck(LUCK_BODY.replace("second_roll >= needed", "second_roll > 11")), fails_at=2,
             message_contains="Compare the reroll with the `needed`"),
        dict(why="Show me how (CP1), pasted word for word with its first sign `>`: no crash, row 2 needs the luck "
                 "question", code=_luck("    if first_roll > needed:\n        return True\n"), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP1), pasted with `>=`: no crash, row 2 needs the luck question",
             code=_luck("    if first_roll >= needed:\n        return True\n"), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP1) with `>`, the luck question added: the visible rows pass; the hidden test "
                 "exactly enough on the first roll decides",
             code=_luck(LUCK_BODY.replace("first_roll >= needed", "first_roll > needed")), fails_at=2,
             message_contains="Exactly enough passes. Which sign means *at least*? (Hidden test: exactly enough "
                              "on the first roll."),
        dict(why="Show me how (CP2), pasted in place of pass on its own: no crash; the first roll is CP1's part",
             code=_luck("    return second_roll >= needed\n"), fails_at=1, message_contains=LUCK_FIX),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-3", opens_after="unit-3",
             ceiling="units-1-3", skills="and-or,boundary,return-bool,early-return", solo="false", dictates="",
             foreign_names="coins,price,has_spare,spare_coins", tests="visible=(15,2,12,F)T,(5,14,12,T)T,(5,14,12,F)F; "
             "hidden=exactly enough first, exactly enough reroll, luck but the reroll fails, luck left and the first "
             "passes, other numbers (needed 8), other numbers with luck (2,9,8,T)") + "\n"
        "Spec: T-CF-3 `passes_with_luck(first_roll, second_roll, needed, has_luck)`. Campaign link (spec): skill "
        "checks with Dumb Luck (Lucky's once-a-day reroll, brief). Rolls are parameters, so every check is "
        "deterministic (no randint). Every visible row has needed = 12, so `needed = 12` inside the function (the "
        "campaign's `required_roll = 12` habit) and `>= 12` typed pass the visible tests and fail only the hidden "
        "'other numbers' row (needed 8) or the typed check. Check-breaker: every row with luck had needed = 12, "
        "so `second_roll > 11` passed; 'other numbers, with luck' (needed 8) catches it. The def line and the "
        "visible calls stay whole on one line (the spec's signature).\n"
        "Teacher ruling (Nov 14): the Teach rung is split in two (FORMAT allows 5 rungs): one question with its "
        "`return` (why a later `if` only runs when the earlier ones said no), then the whole shape with names "
        "that make sense (`has_spare`, `spare_coins`, not a coupon compared with a price). The table's header "
        "says `has_luck`, the parameter's own name, not `luck`. Sign rule: the visible first rolls (15, 5) "
        "against 12 cannot tell `>` from `>=`, so CP1's Show me how offers both, `>` first, and names *exactly "
        "enough on the first roll*; CP2's keeps the one right line, `return second_roll >= needed`. Show-rung "
        "copy-test: CP1 pasted in place of `pass` (with `>`, and with `>=`): no crash, row 2 needs the luck "
        "question ('Every case needs a `return`'); with the luck question added, `>` fails only that hidden "
        "test. CP2's line pasted on its own in place of `pass`: no crash, row 1 fails with the row's own fix; "
        "inside the CP1 shape, under `if has_luck:`, it is the solution."
    ),
)

# ---- T-CF-3a which_roll(...) -> "first" / "reroll" / "none" ----

ROLL_DEF = "def which_roll(first_roll, second_roll, needed, has_luck):\n"
ROLL_TESTS = (
    "# Visible tests. They should show\n"
    "# first, reroll, none.\n"
    + PASS_NOTE +
    "print(which_roll(15, 2, 12, True))\n"
    "print(which_roll(5, 14, 12, True))\n"
    "print(which_roll(5, 14, 12, False))\n"
)


def _roll(body):
    return ROLL_DEF + body + "\n\n" + ROLL_TESTS


ROLL_BODY = (
    "    if first_roll >= needed:\n"
    "        return \"first\"\n"
    "    if has_luck:\n"
    "        if second_roll >= needed:\n"
    "            return \"reroll\"\n"
    "    return \"none\"\n"
)
ROLL_REROLL_FIRST = (
    "    if has_luck:\n"
    "        if second_roll >= needed:\n"
    "            return \"reroll\"\n"
    "    if first_roll >= needed:\n"
    "        return \"first\"\n"
    "    return \"none\"\n"
)
ROLL_CATS = ["first", "reroll", "none"]

WHICH_ROLL = trial(
    id="which-roll",
    title="Dumb Luck: Which Roll?",
    level="advanced",
    variant_of="passes-with-luck",
    minutes=8,
    summary="The advanced twin of Dumb Luck: hand back `\"first\"`, `\"reroll\"` or `\"none\"`.",
    martu=(
        "Lucky wants to know which roll saved him. Write `which_roll`, with the same four parameters as Dumb Luck. "
        "It hands back text:\n"
        "1. `\"first\"` when the first roll passes.\n"
        "2. `\"reroll\"` when the first fails, `has_luck` is `True`, and the second passes.\n"
        "3. `\"none\"` otherwise.\n"
        "```text\n1st 2nd needed has_luck back\n15  2   12     True     \"first\"\n"
        "5   14  12     True     \"reroll\"\n5   14  12     False    \"none\"\n+ 6 hidden tests\n```"
    ),
    fn="which_roll",
    params=["first_roll", "second_roll", "needed", "has_luck"],
    starter=_roll("    pass\n"),
    solution=_roll(ROLL_BODY),
    cats=ROLL_CATS,
    visible=[
        dict(args=(15, 2, 12, True), want="first", fix="Hand back `\"first\"` when the first roll passes, luck or not."),
        dict(args=(5, 14, 12, True), want="reroll",
             fix="Hand back `\"reroll\"` when the first roll fails, `has_luck` is `True`, and the second passes."),
        dict(args=(5, 14, 12, False), want="none", fix="Without luck, a failed first roll is `\"none\"`."),
    ],
    hidden=[
        dict(label="both rolls pass", args=(13, 18, 12, True), want="first",
             fix="When both pass, the first roll counts: ask about it first."),
        dict(label="exactly enough on the reroll", args=(4, 12, 12, True), want="reroll",
             fix="Exactly enough passes. Which sign means *at least*?"),
        dict(label="exactly enough on the first roll", args=(12, 20, 12, False), want="first",
             fix="Exactly enough passes. Which sign means *at least*?"),
        dict(label="luck, but the reroll fails too", args=(4, 9, 12, True), want="none",
             fix="A reroll that fails is still `\"none\"`: luck is a second chance, not a pass."),
        dict(label="other numbers", args=(7, 3, 6, False), want="first",
             fix="Compare with the `needed` the function is handed, whatever it is."),
        dict(label="other numbers, with luck", args=(3, 7, 6, True), want="reroll",
             fix="Compare the reroll with the `needed` the function is handed, whatever it is."),
    ],
    cp1=dict(
        text="Make the visible tests hand back `\"first\"`, `\"reroll\"` and `\"none\"`.",
        hints=[
            "Row 1 has luck, but the first roll, 15, already passes 12. So `\"first\"`: no luck used.",
            "Each `return` ends the function, so a later question only runs when the earlier ones said no:\n"
            "```python\nif coins >= price:\n    return \"paid\"\nif has_spare:\n    return \"spare\"\n"
            "return \"no sale\"\n```",
            "Start with `if first_roll > needed:` or `if first_roll >= needed:`, and `return \"first\"` under it. "
            "Then ask about `has_luck` and `second_roll`. Both signs pass the visible rows. The hidden tests for "
            "*exactly enough on each roll* decide the sign.",
        ],
        pass_line="Lucky: First, reroll, none. I prefer first. Less paperwork.",
    ),
    cp2=dict(
        text="Pass the 6 hidden tests. They try both rolls passing, exactly enough on each roll, and other numbers.",
        hints=[
            "Read *both rolls pass*. Which roll counts?",
            "The first true answer wins. The first roll is asked first, so it wins a tie.",
            "Ask `if first_roll >= needed:`, with `return \"first\"` under it, before any question about the "
            "reroll.",
        ],
        pass_line="Oogrish: The first roll counts first. Luck waits its turn.",
    ),
    foreign=["coins", "price", "has_spare"],
    assemble=dict(
        lines=[ROLL_DEF.strip("\n"), *ROLL_BODY.splitlines(), *_calls(ROLL_TESTS)],
        distractors=["    if second_roll >= needed:", "        return True", "    return \"reroll\""],
    ),
    another_way=[
        dict(angle="picture", label="Three answers", text=(
            "```text\nfirst >= needed?  -> \"first\"\nluck and\nsecond >= needed? -> \"reroll\"\n"
            "else              -> \"none\"\n```")),
        dict(angle="everyday", label="Which key opened it", text=(
            "You try your own key first. If it opens the door, that is the answer, even if the spare would work "
            "too. Only when it fails do you try the spare.")),
        dict(angle="shorter", text="Same checks as Dumb Luck, in the same order. Each `return` hands back a word."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="return roll >= required_roll",
        why="The same `>=` check as the trap door, asked once, and once more with luck. Now it says which roll did it.",
    ),
    takeaway="Order breaks ties: the question asked first wins when two would both say yes.",
    partials=[_roll(ROLL_REROLL_FIRST)],
    wrong_answers=[
        dict(why="the starter (pass)", code=_roll("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="the reroll asked first (tie-break wrong)", code=_roll(ROLL_REROLL_FIRST), fails_at=2,
             message_contains="the first roll counts"),
        dict(why="> for >=", code=_roll(ROLL_BODY.replace(">=", ">")), fails_at=2,
             message_contains="Exactly enough passes"),
        dict(why="True / False kept from the core trial", code=_roll(LUCK_BODY), fails_at=1,
             message_contains="Hand back text in quotes"),
        dict(why='a capital letter ("First")', code=_roll(ROLL_BODY.replace('"first"', '"First"')), fails_at=1,
             message_contains="every letter, space and capital"),
        dict(why="luck counted as a reroll without checking the second roll",
             code=_roll("    if first_roll >= needed:\n        return \"first\"\n    if has_luck:\n"
                        "        return \"reroll\"\n    return \"none\"\n"),
             fails_at=2, message_contains="luck is a second chance, not a pass"),
        dict(why="needed set again inside", code=_roll("    needed = 12\n" + ROLL_BODY), fails_at=2,
             message_contains="a line inside sets it again"),
        dict(why="print instead of return", code=_roll(ROLL_BODY.replace('return "first"', 'print("first")').replace(
            'return "reroll"', 'print("reroll")').replace('return "none"', 'print("none")')), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the reroll compared with a typed number no visible test shows (second_roll > 11)",
             code=_roll(ROLL_BODY.replace("second_roll >= needed", "second_roll > 11")), fails_at=2,
             message_contains="Compare the reroll with the `needed`"),
        dict(why="Show me how (CP1), pasted word for word with its first sign `>`: no crash, row 2 needs the luck "
                 "question", code=_roll('    if first_roll > needed:\n        return "first"\n'), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="Show me how (CP1) with `>` on the first roll, the rest added: the visible rows pass; the hidden "
                 "test exactly enough on the first roll decides",
             code=_roll(ROLL_BODY.replace("first_roll >= needed", "first_roll > needed")), fails_at=2,
             message_contains="Hidden test: exactly enough on the first roll"),
        dict(why="Show me how (CP1) with `>` on the reroll: the hidden test exactly enough on the reroll decides",
             code=_roll(ROLL_BODY.replace("second_roll >= needed", "second_roll > needed")), fails_at=2,
             message_contains="Hidden test: exactly enough on the reroll"),
        dict(why="Show me how (CP2), pasted in place of pass: no crash; the reroll is the student's part",
             code=_roll('    if first_roll >= needed:\n        return "first"\n'), fails_at=1,
             message_contains="Every case needs a `return`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-CF", trial="T-CF-3a", opens_after="unit-3",
             ceiling="units-1-3", skills="order,tie-break,boundary,return-text", solo="false", dictates="",
             foreign_names="coins,price,has_spare", tests="visible=(15,2,12,T)first,(5,14,12,T)reroll,(5,14,12,F)none; "
             "hidden=both pass, exactly enough reroll, exactly enough first, luck but the reroll fails, other "
             "numbers, other numbers with luck (3,7,6,T)")
        + "\n"
        "Spec: returns \"first\", \"reroll\" or \"none\". The spec names no function for the variant; "
        "`which_roll` keeps the core's four parameters, because a `passes_with_luck` that hands back \"none\" would "
        "read as a pass. The tie-break slip (both rolls pass: which counts?) is the hidden 'both rolls pass' row; "
        "partial 1 asks about the reroll first. The nested `if` keeps every body line within 36 characters.\n"
        "Teacher ruling (Nov 14): the table's header says `has_luck`, the parameter's own name (the rolls are "
        "`1st` and `2nd` there, so a row like `5   14  12     True     \"reroll\"` fits 36 characters); the "
        "Teach fence uses Dumb Luck's new names (`has_spare`). Sign rule: the visible rolls (15, 5, 14 against "
        "12) cannot tell `>` from `>=`, so CP1's Show me how offers both, `>` first as in its core twin, and names "
        "the *exactly enough* tests on each roll; CP2's keeps the one right line, now with its `return`. The tie "
        "row (both rolls pass) is not a sign question: its order stays. Show-rung copy-test: CP1 pasted in place "
        "of `pass` (either sign) and CP2 pasted in place of `pass`: no crash, row 2 needs the reroll question "
        "('Every case needs a `return`'); with the rest added, `>` on either roll fails only its hidden exactly-"
        "enough test (wrong answers 'Show me how ...')."
    ),
)

# =============================================================================================
# Lists set (opens after Unit 4; Units 1-4 tokens): T-L-1, T-L-2, T-L-3 and their variants
# =============================================================================================

# ---- T-L-1 newest_gap(wall) ----

NEWEST_TESTS = (
    "# Visible tests. They should show\n"
    "# 44, then 51.\n"
    + PASS_NOTE +
    "print(newest_gap([48, 47, 44]))\n"
    "print(newest_gap([60, 58, 55, 51]))\n"
)


def _newest(body):
    return "def newest_gap(wall):\n" + body + "\n\n" + NEWEST_TESTS


NEWEST_RULES = [
    SORT_RULE,
    ("_tn(_val) == 'list'", "That hands back a list. Hand back one gap: the last one."),
    ("_val == _args[0][0] and _B.len(_args[0]) > 1", "That is the oldest gap, at position 0. The newest is the last: count from the end."),
    ("_val == _B.len(_args[0])", "That is how many gaps there are, not the newest gap."),
    ("_val == _B.len(_args[0]) - 1", "That is the last position. Hand back the gap at that position."),
    ("_val == _B.min(_args[0])", "That is the smallest gap. The newest is the last one, whatever its size."),
    ("_val in _args[0]", "That is another gap on the wall. A typed position fits one wall only: count from the end."),
]
NEWEST_FIX = "Hand back the newest gap: the last item of `wall`."
TYPED_POS_CRASH = ("_k == 'IndexError'",
                   "A typed position fits one wall only: count from the end, so a wall of any length works.")
LONG_WALL = [48, 48, 47, 46, 44, 41, 37, 32, 26]

NEWEST_GAP = trial(
    id="newest-gap",
    title="The Newest Gap",
    minutes=5,
    summary="`newest_gap(wall)`: hand back the last gap on the chalk wall, on a wall of any length.",
    martu=(
        "Gearshift reads the chalk wall from the bottom up. Write `newest_gap(wall)`. It hands back the newest gap: "
        "the last one on the wall. The wall always has at least one gap.\n"
        "```text\ncall                          back\nnewest_gap([48, 47, 44])      44\n"
        "newest_gap([60, 58, 55, 51])  51\n+ 4 hidden tests\n```"
    ),
    fn="newest_gap",
    params=["wall"],
    starter=_newest("    pass\n"),
    solution=_newest("    return wall[-1]\n"),
    rules=NEWEST_RULES,
    visible=[
        dict(args=([48, 47, 44],), want=44, fix=NEWEST_FIX),
        dict(args=([60, 58, 55, 51],), want=51, fix=NEWEST_FIX),
    ],
    hidden=[
        dict(label="a wall of one gap", args=([30],), want=30, fix="On a wall of one gap, that gap is the newest.",
             crash=[TYPED_POS_CRASH]),
        dict(label="a long wall", args=(LONG_WALL,), want=26, fix="Count from the end, so a wall of any length works.",
             crash=[TYPED_POS_CRASH]),
        dict(label="a newest gap that is not the smallest", args=([40, 36, 38],), want=38, fix=NEWEST_FIX),
        dict(label="a wall that keeps its gaps", args=([20, 18, 15],), want=15, fix=NEWEST_FIX,
             after=KEEP_WALL),
    ],
    cp1=dict(
        text="Make the two visible tests hand back 44, then 51.",
        hints=[
            "The newest gap is the last item, whatever the wall's length.",
            "A minus counts from the end of a list: in `bells = [3, 6, 9]`, `bells[-1]` is 9.",
            "Write `return wall[-1]` in place of `pass`.",
        ],
        pass_line="Gearshift: Visor dims. Bottom of the wall. Newest gap. Logged.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests: one gap, a long wall, a newest gap that is not the smallest, and a wall that "
             "keeps its gaps.",
        hints=[
            "Read *a wall that keeps its gaps*: your function may read the wall, but not change it.",
            "`.pop()` hands back the last item, but takes it off the list. `min()` finds the smallest, and the "
            "smallest is not always the newest.",
            "Use `return wall[-1]`: it reads the last gap and leaves the wall as it was.",
        ],
        pass_line="Mar'tu: Any wall, any length. Read, not rubbed out. Good.",
    ),
    foreign=["bells", "chalk_wall"],
    assemble=dict(
        lines=["def newest_gap(wall):", "    return wall[-1]", *_calls(NEWEST_TESTS)],
        distractors=["    return wall[2]", "    return wall.pop()", "    return min(wall)"],
    ),
    another_way=[
        dict(angle="picture", label="Counting from the end", text=(
            "```text\nwall:   48   47   44\nfront:  0    1    2\nend:   -3   -2   -1\n```\n"
            "`-1` is always the last item, on a wall of any length.")),
        dict(angle="everyday", label="The last page", text=(
            "The newest entry in a diary is on the last written page, however thick the diary is. You flip to the "
            "end, not to page 3.")),
        dict(angle="campaign", label="You've seen this", text=(
            "37 was circled twice at the bottom of the chalk wall: the newest gap. In code, that is `wall[-1]`.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="The wall read 48, 48, 47, 46, 44, 41, 37, and 37 was circled twice. The newest gap is the last one.",
    ),
    takeaway="`wall[-1]` is the last item of a list of any length, and reading it leaves the list as it was.",
    partials=[_newest("    return min(wall)\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_newest("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="a typed position (wall[2]) that fits a 3-gap wall only", code=_newest("    return wall[2]\n"),
             fails_at=1, message_contains="A typed position fits one wall only"),
        dict(why="the oldest gap (wall[0])", code=_newest("    return wall[0]\n"), fails_at=1,
             message_contains="the oldest gap"),
        dict(why="the smallest gap (min) for the newest", code=_newest("    return min(wall)\n"), fails_at=2,
             message_contains="That is the smallest gap"),
        dict(why=".pop() takes the gap off the wall", code=_newest("    return wall.pop()\n"), fails_at=2,
             message_contains="`.pop()` removes them"),
        dict(why="print instead of return", code=_newest("    print(wall[-1])\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="wall[len(wall)]: one past the end (the visible calls crash)",
             code=_newest("    return wall[len(wall)]\n"), fails_at=0, message_contains="IndexError"),
        dict(why="each visible test's answer typed behind an if",
             code=_newest("    if wall == [48, 47, 44]:\n        return 44\n    return 51\n"), fails_at=2,
             message_contains="`wall == [48, 47, 44]` is typed for one test"),
        dict(why="the count, not the gap (len)", code=_newest("    return len(wall)\n"), fails_at=1,
             message_contains="how many gaps"),
        dict(why="the gap as text (str)", code=_newest("    return str(wall[-1])\n"), fails_at=1,
             message_contains="Hand back a number"),
        dict(why="a one-item slice (a list, not a gap)", code=_newest("    return wall[-1:]\n"), fails_at=1,
             message_contains="That hands back a list"),
        dict(why="the first visible answer hard-coded (return 44)", code=_newest("    return 44\n"), fails_at=1,
             message_contains="for every visible test"),
        dict(why="a typed position for each visible wall length (wall[2] or wall[3])",
             code=_newest("    if len(wall) == 3:\n        return wall[2]\n    return wall[3]\n"), fails_at=2,
             message_contains="A typed position fits one wall only"),
        dict(why=".sort() first: the gaps in size order, so [-1] is the biggest",
             code=_newest("    wall.sort()\n    return wall[-1]\n"), fails_at=1, message_contains="Leave out `.sort()`"),
        dict(why="the gap read, then rubbed off with .remove() (the value is right, the wall is not)",
             code=_newest("    gap = wall[-1]\n    wall.remove(gap)\n    return gap\n"), fails_at=2,
             message_contains="Read the gaps without changing the wall"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-1", opens_after="unit-4", ceiling="units-1-4",
             skills="index-from-end,return-value,read-test-table", solo="false", dictates="", foreign_names="bells",
             tests="visible=[48,47,44]->44,[60,58,55,51]->51; hidden=one gap, a long wall (9), not the smallest "
             "([40,36,38]), keeps its gaps (pop)") + "\n"
        "Spec: T-L-1 `newest_gap(wall)` -> the last item (3A-06's newest_mark as a trial). The core states the "
        "wall always has a gap; the empty wall is the variant's. Evidence: `-1` vs `len` (3B-04 `chalk_wall[6]`), "
        "`min()` counted for the newest (u04b check-breaker), `.pop()` hands back AND removes (3C), hard-coded "
        "answers (A-02 `return 500`). `wall[len(wall) - 1]` passes (values only). Show-rung copy-test: CP1 and "
        "CP2's `return wall[-1]` in place of `pass`: the solution (no sign to hand over)."
    ),
)

# ---- T-L-1a newest_gap(wall): an empty wall -> -1 ----

NEWEST2_BODY = "    if len(wall) == 0:\n        return -1\n    return wall[-1]\n"
PRINTED_CRASH = ("_k == 'IndexError' and _rows",
                 "Use `return` in place of `print`: after printing, the function went on and read a gap that is not "
                 "there.")
EMPTY_CRASH = ("_k == 'IndexError'", "An empty wall has no last gap: check for an empty wall first, and hand back `-1`.")

NEWEST_GAP_EMPTY = trial(
    id="newest-gap-empty-wall",
    title="The Newest Gap: An Empty Wall",
    level="advanced",
    variant_of="newest-gap",
    minutes=6,
    summary="The advanced twin of The Newest Gap: an empty wall hands back `-1`.",
    martu=(
        "I wiped the wall clean once. Same function, one more rule: an empty wall hands back `-1`, a number "
        "no gap can be.\n"
        "```text\ncall                          back\nnewest_gap([48, 47, 44])      44\n"
        "newest_gap([60, 58, 55, 51])  51\n+ 4 hidden tests\n```"
    ),
    fn="newest_gap",
    params=["wall"],
    predict=dict(
        q="Before you write: what will this print?",
        code="gaps = []\nprint(len(gaps))\n",
        choices=["-1", "0", "1"],
        answer=1,
        explain=(
            "An empty list has 0 items, so `len(gaps)` is 0. That is how a function can ask whether a wall is "
            "empty: `len(wall) == 0`."
        ),
    ),
    starter=_newest("    pass\n"),
    solution=_newest(NEWEST2_BODY),
    rules=NEWEST_RULES,
    allowed=[-1, 0],
    visible=[
        dict(args=([48, 47, 44],), want=44, fix=NEWEST_FIX),
        dict(args=([60, 58, 55, 51],), want=51, fix=NEWEST_FIX),
    ],
    hidden=[
        dict(label="an empty wall", args=([],), want=-1, fix="An empty wall hands back `-1`.",
             crash=[PRINTED_CRASH, EMPTY_CRASH], rules=[("True", "An empty wall hands back `-1`, a number no gap can be.")]),
        dict(label="a wall of one gap", args=([30],), want=30,
             rules=[("_val == -1", "A wall of one gap is not empty: only a wall with no gaps hands back `-1`.")],
             fix="On a wall of one gap, that gap is the newest."),
        dict(label="a newest gap that is not the smallest", args=([40, 36, 38],), want=38, fix=NEWEST_FIX),
        dict(label="a wall that keeps its gaps", args=([20, 18, 15],), want=15, fix=NEWEST_FIX, after=KEEP_WALL),
    ],
    cp1=dict(
        text="Make the two visible tests hand back 44, then 51.",
        hints=[
            "The visible walls both have gaps, so the newest gap is the last item.",
            "A minus counts from the end of a list: in `bells = [3, 6, 9]`, `bells[-1]` is 9.",
            "Write `return wall[-1]` as the function's last line.",
        ],
        pass_line="Gearshift: Two walls, two newest gaps. Now the empty one.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests: an empty wall, one gap, a newest gap that is not the smallest, and a wall "
             "that keeps its gaps.",
        hints=[
            "Read *an empty wall*: what should come back, and what does `wall[-1]` do there?",
            "Ask before you read: `if len(bags) == 0:` is `True` only for an empty list. Hand back the default "
            "inside it.",
            "Start the body with `if len(wall) == 0:`, with `return -1` under it. Then `return wall[-1]` below "
            "the `if`.",
        ],
        pass_line="Mar'tu: An empty wall, and no crash. I wiped it once. Never again, I hope.",
    ),
    foreign=["bells", "bags", "gaps", "chalk_wall"],
    assemble=dict(
        lines=["def newest_gap(wall):", *NEWEST2_BODY.splitlines(), *_calls(NEWEST_TESTS)],
        distractors=["    if len(wall) <= 1:", "        return 0", "    if wall[-1] == 0:"],
    ),
    another_way=[
        dict(angle="picture", label="Ask, then read", text=(
            "```text\nlen(wall) == 0 ?\n  yes -> -1\n  no  -> wall[-1]\n```")),
        dict(angle="everyday", label="Check the jar first", text=(
            "Before you take the last biscuit, look in the jar. An empty jar gets a note, not a grab in the dark.")),
        dict(angle="step-by-step", text=(
            "1. Ask `len(wall) == 0`. 2. If so, hand back `-1` and stop. 3. Otherwise hand back `wall[-1]`. The "
            "order matters: ask before you read.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="Two weeks of gaps went on that wall. A fresh wall starts empty, and your function now copes with that too.",
    ),
    takeaway="Ask about the empty case before you read an item: `if len(wall) == 0:` comes first.",
    partials=[_newest("    return wall[-1]\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_newest("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="the empty case forgotten: IndexError on wall[-1]", code=_newest("    return wall[-1]\n"), fails_at=2,
             message_contains="An empty wall has no last gap"),
        dict(why="<= 1 for the empty test (one gap counted as empty)",
             code=_newest(NEWEST2_BODY.replace("== 0", "<= 1")), fails_at=2, message_contains="is not empty"),
        dict(why="0 for the empty wall, not -1", code=_newest(NEWEST2_BODY.replace("return -1", "return 0")),
             fails_at=2, message_contains="hands back `-1`"),
        dict(why='"-1" in quotes', code=_newest(NEWEST2_BODY.replace("return -1", 'return "-1"')), fails_at=2,
             message_contains="Hand back a number"),
        dict(why="print(-1) instead of return", code=_newest(NEWEST2_BODY.replace("return -1", "print(-1)")),
             fails_at=2, message_contains="in place of `print`"),
        dict(why="a blank return for the empty wall", code=_newest(NEWEST2_BODY.replace("return -1", "return")),
             fails_at=2, message_contains="on its own, `return` hands back `None`"),
        dict(why=".pop() with the guard", code=_newest(NEWEST2_BODY.replace("return wall[-1]", "return wall.pop()")),
             fails_at=2, message_contains="`.pop()` removes them"),
        dict(why="the smallest gap with the guard", code=_newest(NEWEST2_BODY.replace("wall[-1]", "min(wall)")),
             fails_at=2, message_contains="That is the smallest gap"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-1a", opens_after="unit-4", ceiling="units-1-4",
             skills="empty-case,index-from-end", solo="false", dictates="", foreign_names="bells,bags,gaps",
             tests="visible=[48,47,44]->44,[60,58,55,51]->51; hidden=an empty wall (-1), one gap, not the smallest, "
             "keeps its gaps") + "\n"
        "Spec: an empty wall -> -1. The empty wall is a HIDDEN row on purpose (the format's own example label, 'an "
        "empty wall'): as a visible print it would crash the run before any check, and the student would get "
        "Python's IndexError instead of the labeled message. The rule is stated in the Learn text, so nothing is a "
        "surprise. Evidence: the IndexError on `wall[-1]` of an empty list (unit brief), `<= 1` (the boundary). "
        "`if wall == []:` and `if not wall:` would pass too (not taught; allowed).\n"
        "Teacher ruling (Nov 14): the Learn text no longer says that `wall[-1]` on an empty list stops Python, or "
        "'Ask first': the empty case is this twin's lesson, the hidden test's EMPTY_CRASH message teaches it, and "
        "the predict already cues `len(wall) == 0` (answer index 1 now). Show-rung copy-test: CP1's `return "
        "wall[-1]` as the last line, in place of `pass`: no crash on the visible walls, passes CP1 (partial 1: the "
        "empty wall's crash is CP2's lesson, inside Mar'tu's check). CP2's `if len(wall) == 0:` with `return -1` "
        "under it, then `return wall[-1]` below the `if` (the old rung's 'and `return -1`' did not say where): "
        "the solution."
    ),
)

# ---- T-L-2 last_three(wall) ----

THREE_TESTS = (
    "# Visible tests. They should show\n"
    "# [46, 44, 41], then [7, 4, 2].\n"
    + PASS_NOTE +
    "print(last_three([47, 46, 44, 41]))\n"
    "print(last_three([12, 9, 7, 4, 2]))\n"
)


def _three(body):
    return "def last_three(wall):\n" + body + "\n\n" + THREE_TESTS


THREE_RULES = [
    SORT_RULE,
    ("_tn(_val) in ('int', 'float')", "That is one gap. Hand back a list of the last three."),
    ("_val == _args[0][-3:-1]", "Drop the `-1` after the colon: `[-3:]` runs to the end, so the newest gap is kept."),
    ("_val == _args[0][-3:][::-1] and _B.len(_val) > 1", "Keep the wall's order: the oldest of the three comes first."),
    ("_val == _args[0] and _B.len(_args[0]) > 3", "That is the whole wall. Hand back only the last three gaps."),
    ("_tn(_val) == 'list' and _B.len(_val) == 3",
     "Those are three gaps, but not the last three. A typed position fits one wall only: count from the end."),
]
THREE_FIX = "Hand back the last three gaps, oldest first, as a list."
SHORT_CRASH = ("_k == 'IndexError'", "A wall can have fewer than three gaps. A slice takes what is there, and never "
               "stops Python.")

LAST_THREE = trial(
    id="last-three",
    title="The Last Three Gaps",
    minutes=6,
    summary="`last_three(wall)`: hand back the last three gaps as a list, or all of them on a short wall.",
    martu=(
        "Oogrish studies only the last three gaps. Write `last_three(wall)`. It hands back a list of the last three "
        "gaps, oldest first. A wall with fewer than three gaps hands back all of them.\n"
        "```text\nlast_three([47, 46, 44, 41])\n  -> [46, 44, 41]\nlast_three([12, 9, 7, 4, 2])\n  -> [7, 4, 2]\n"
        "+ 4 hidden tests\n```"
    ),
    fn="last_three",
    params=["wall"],
    predict=dict(
        q="Before you write: what will this print?",
        code="gaps = [20, 18]\nprint(gaps[-3:])\n",
        choices=["[]", "[18]", "[20, 18]"],
        answer=2,
        explain=(
            "A [[slice]] never runs off the end of a list: it takes the items that are there. So `[-3:]` on a short "
            "wall hands back all of it."
        ),
    ),
    starter=_three("    pass\n"),
    solution=_three("    return wall[-3:]\n"),
    rules=THREE_RULES,
    visible=[
        dict(args=([47, 46, 44, 41],), want=[46, 44, 41], fix=THREE_FIX),
        dict(args=([12, 9, 7, 4, 2],), want=[7, 4, 2], fix=THREE_FIX),
    ],
    hidden=[
        dict(label="exactly three gaps", args=([9, 8, 7],), want=[9, 8, 7], fix="Three gaps: hand back all three."),
        dict(label="a short wall of two gaps", args=([20, 18],), want=[20, 18], crash=[SHORT_CRASH],
             rules=[("_val == _args[0][_B.len(_args[0]) - 3:]",
                     "On a short wall, `len(wall) - 3` is below 0, so the slice counts from the end and cuts too "
                     "much. Count from the end yourself, with `-3`.")],
             fix="A wall of two gaps hands back both of them."),
        dict(label="a long wall", args=(LONG_WALL,), want=[37, 32, 26], fix="Count from the end, so any length works."),
        dict(label="a wall that keeps its gaps", args=([30, 26, 21, 15],), want=[26, 21, 15], fix=THREE_FIX,
             after=KEEP_WALL),
    ],
    cp1=dict(
        text="Make the two visible tests hand back `[46, 44, 41]`, then `[7, 4, 2]`.",
        hints=[
            "You want the last three items, in their order. A slice cuts a piece out of a list.",
            "In `bells = [3, 6, 9, 12]`, `bells[-2:]` is `[9, 12]`: from the second-to-last to the end. With "
            "nothing after the colon, the slice runs to the end and keeps the last item.",
            "Write `return wall[-3:]` in place of `pass`.",
        ],
        pass_line="Oogrish: Three gaps. The rest is history. Literally.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests: exactly three gaps, a short wall of two, a long wall, and a wall that keeps "
             "its gaps.",
        hints=[
            "Read *a short wall of two gaps*: what should come back? Does your line stop Python, or cut too much?",
            "A slice like `[-3:]` takes what is there. A start worked out as `len(wall) - 3` goes below 0 on a "
            "short wall, and a minus start counts from the end.",
            "Use `return wall[-3:]`: it works for a wall of any length.",
        ],
        pass_line="Mar'tu: Short wall, long wall, the same line. That is a good line.",
    ),
    foreign=["bells", "chalk_wall"],
    assemble=dict(
        lines=["def last_three(wall):", "    return wall[-3:]", *_calls(THREE_TESTS)],
        distractors=["    return wall[-3:-1]", "    return wall[1:4]", "    return wall[-3]"],
    ),
    another_way=[
        dict(angle="picture", label="Where the slice starts", text=(
            "```text\nwall:  12   9   7   4   2\nend:   -5  -4  -3  -2  -1\n              [-3:] -> 7, 4, 2\n```")),
        dict(angle="everyday", label="The last three pages", text=(
            "Tear out the last three pages of a notebook. With only two pages left, you get two. You never get a "
            "page that is not there.")),
        dict(angle="shorter", text="`wall[-3:]`: from the third-to-last to the end. Short walls give what they have."),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="Gearshift said the gaps are shrinking faster every time. The last three gaps are where you see it.",
    ),
    takeaway="A slice from the end, `wall[-3:]`, works on any length: it takes what is there.",
    partials=[_three("    return wall[len(wall) - 3:]\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_three("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="an end typed into the slice ([-3:-1]): it stops before the newest gap",
             code=_three("    return wall[-3:-1]\n"), fails_at=1, message_contains="Drop the `-1` after the colon"),
        dict(why="typed positions ([1:4], the first visible wall only)", code=_three("    return wall[1:4]\n"),
             fails_at=1, message_contains="not the last three"),
        dict(why="three reads by position (IndexError on a short wall)",
             code=_three("    return [wall[-3], wall[-2], wall[-1]]\n"), fails_at=2,
             message_contains="fewer than three gaps"),
        dict(why="len(wall) - 3 as the start (cuts too much on a short wall)",
             code=_three("    return wall[len(wall) - 3:]\n"), fails_at=2, message_contains="below 0"),
        dict(why="three .pop() calls (the wall is emptied; a short wall stops Python)",
             code=_three("    c = wall.pop()\n    b = wall.pop()\n    a = wall.pop()\n    return [a, b, c]\n"),
             fails_at=2, message_contains="fewer than three gaps"),
        dict(why="print instead of return", code=_three("    print(wall[-3:])\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="one gap, not a slice (wall[-3])", code=_three("    return wall[-3]\n"), fails_at=1,
             message_contains="That is one gap"),
        dict(why="the first visible answer hard-coded", code=_three("    return [46, 44, 41]\n"), fails_at=1,
             message_contains="for every visible test"),
        dict(why="each visible answer typed behind an if",
             code=_three("    if wall == [47, 46, 44, 41]:\n        return [46, 44, 41]\n    return [7, 4, 2]\n"),
             fails_at=2, message_contains="is typed for one test"),
        dict(why="the order reversed", code=_three("    return [wall[-1], wall[-2], wall[-3]]\n"), fails_at=1,
             message_contains="Keep the wall's order"),
        dict(why=".sort() first (the slice is right, the order is not)",
             code=_three("    wall.sort()\n    return wall[-3:]\n"), fails_at=1, message_contains="Leave out `.sort()`"),
        dict(why="the slice right, but the wall changed (.append() inside)",
             code=_three("    piece = wall[-3:]\n    wall.append(0)\n    return piece\n"), fails_at=2,
             message_contains="Read the gaps without changing the wall"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-2", opens_after="unit-4", ceiling="units-1-4",
             skills="slice,read-test-table", solo="false", dictates="", foreign_names="bells",
             tests="visible=[47,46,44,41]->[46,44,41],[12,9,7,4,2]->[7,4,2]; hidden=exactly three, a short wall "
             "of two, a long wall, keeps its gaps") + "\n"
        "Spec: T-L-2 `last_three(wall)` -> the slice. The Learn text states what a short wall gives (all of it), "
        "which is what `[-3:]` does. The two visible walls have different lengths, so a typed `[1:4]` fails "
        "visibly; `wall[len(wall) - 3:]` passes every visible row and exactly three, and fails only the short "
        "wall (partial 1). Evidence: 3B-05's `[-3:-1]` (end left out), typed positions (3B-04), `.pop()` (3C). "
        "The visible walls are short (12, 9, 7, 4, 2 is a wall near the end) so each call fits 36 characters.\n"
        "Teacher ruling (Nov 14): `[-3:-1]` gets 'Drop the `-1` after the colon: `[-3:]` runs to the end, so the "
        "newest gap is kept' (the old 'Leave the end out' read as the slip itself), and the Teach rung says what "
        "an empty end does. Predict answer index 2. Show-rung copy-test: CP1 and CP2's `return wall[-3:]` in "
        "place of `pass`: the solution."
    ),
)

# ---- T-L-2a total_drop(wall) ----

DROP_TESTS = (
    "# Visible tests. They should show\n"
    "# 4, then 9.\n"
    + PASS_NOTE +
    "print(total_drop([48, 47, 44]))\n"
    "print(total_drop([60, 58, 55, 51]))\n"
)


def _drop(body):
    return "def total_drop(wall):\n" + body + "\n\n" + DROP_TESTS


DROP_BODY = "    if len(wall) < 2:\n        return 0\n    return wall[0] - wall[-1]\n"
DROP_RULES = [
    SORT_RULE,
    ("_val == _args[0][-1] - _args[0][0] and _val != 0",
     "Take the last from the first, not the first from the last: the drop is first minus last."),
    ("_val == _B.max(_args[0]) - _B.min(_args[0])",
     "That is the biggest minus the smallest. The drop is the first gap minus the last."),
    ("_B.len(_args[0]) > 2 and _val == _args[0][0] - _args[0][1]",
     "That is only the first shrink. Take the last gap from the first gap."),
    ("_val == 0 and _B.len(_args[0]) == 2",
     "A wall of exactly 2 gaps has a drop. Only fewer than 2 hands back 0: which sign means *less than*?"),
]
DROP_FIX = "Hand back the first gap minus the last gap."

TOTAL_DROP = trial(
    id="total-drop",
    title="The Total Drop",
    level="advanced",
    variant_of="last-three",
    minutes=7,
    summary="The advanced twin of The Last Three Gaps: the first gap minus the last, and 0 on a wall of fewer than 2.",
    martu=(
        "Gearshift wants one number: how far the gaps fell. Write `total_drop(wall)`: the first gap minus the last. "
        "A wall with fewer than 2 gaps hands back `0`.\n"
        "```text\ntotal_drop([48, 47, 44])\n  -> 4\ntotal_drop([60, 58, 55, 51])\n  -> 9\n+ 5 hidden tests\n```"
    ),
    fn="total_drop",
    params=["wall"],
    starter=_drop("    pass\n"),
    solution=_drop(DROP_BODY),
    rules=DROP_RULES,
    allowed=[0, 1, 2],
    visible=[
        dict(args=([48, 47, 44],), want=4, fix=DROP_FIX),
        dict(args=([60, 58, 55, 51],), want=9, fix=DROP_FIX),
    ],
    hidden=[
        dict(label="exactly two gaps", args=([30, 26],), want=4, fix="A wall of two gaps has a drop: first minus last."),
        dict(label="a wall of one gap", args=([30],), want=0, fix="A wall of one gap hands back 0: nothing fell yet."),
        dict(label="a gap that grew along the way", args=([40, 44, 39],), want=1, fix=DROP_FIX),
        dict(label="an empty wall", args=([],), want=0, fix="An empty wall hands back 0.",
             crash=[("_k in ('IndexError', 'ValueError')",
                     "An empty wall has no first or last gap: hand back 0 first, when the wall has fewer than 2 gaps.")]),
        dict(label="a wall that keeps its gaps", args=([30, 26, 21],), want=9, fix=DROP_FIX, after=KEEP_WALL),
    ],
    cp1=dict(
        text="Make the two visible tests hand back 4, then 9.",
        hints=[
            "48 was first and 44 is last: 48 minus 44 is 4.",
            "Position 0 is the first item, and `-1` the last: in `bells = [9, 6, 2]`, `bells[0] - bells[-1]` is 7.",
            "Hand back the first minus the last: `return wall[0] - wall[-1]`.",
        ],
        pass_line="Gearshift: Visor dims. Forty-eight down to forty-four. Four hours gone.",
    ),
    cp2=dict(
        text="Pass the 5 hidden tests: exactly two gaps, one gap, a gap that grew, an empty wall, and a wall that "
             "keeps its gaps.",
        hints=[
            "Read *an empty wall* and *a wall of one gap*: nothing fell, so the answer is 0.",
            "*Fewer than 2* means 0 or 1 gaps: `len(bags) < 2`. A wall of exactly 2 gaps has a drop.",
            "Start with `if len(wall) < 2:`, with `return 0` under it. Then `return wall[0] - wall[-1]` below "
            "the `if`.",
        ],
        pass_line="Mar'tu: Empty, one gap, two gaps. Each edge answered. The wall is honest now.",
    ),
    foreign=["bells", "bags", "chalk_wall"],
    assemble=dict(
        lines=["def total_drop(wall):", *DROP_BODY.splitlines(), *_calls(DROP_TESTS)],
        distractors=["    if len(wall) <= 2:", "    return wall[-1] - wall[0]", "    return max(wall) - min(wall)"],
    ),
    another_way=[
        dict(angle="picture", label="First and last only", text=(
            "```text\nwall:  48   47   44\n       ^first     ^last\n48 - 44 = 4\n```\n"
            "The gaps in between do not matter.")),
        dict(angle="everyday", label="A long walk down", text=(
            "You start a hike at 48 meters and end at 44. Up and down in between, the drop is still start minus "
            "end. With no walk at all, the drop is 0.")),
        dict(angle="step-by-step", text=(
            "1. Ask `len(wall) < 2`: 0 or 1 gaps hand back 0. 2. Otherwise take `wall[-1]` from `wall[0]`. 3. Read "
            "the wall, do not change it.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="Oogrish: every forty-eight hours, at first. The total drop is how far it has fallen since then.",
    ),
    takeaway="Guard the short case first (`len(wall) < 2`), then read `wall[0]` and `wall[-1]`.",
    partials=[_drop("    return wall[0] - wall[-1]\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_drop("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="last minus first (the drop backwards)", code=_drop("    return wall[-1] - wall[0]\n"), fails_at=1,
             message_contains="Take the last from the first"),
        dict(why="max minus min (fails when a gap grew)",
             code=_drop("    if len(wall) < 2:\n        return 0\n    return max(wall) - min(wall)\n"), fails_at=2,
             message_contains="biggest minus the smallest"),
        dict(why="<= 2 for < 2 (exactly two gaps hands back 0)", code=_drop(DROP_BODY.replace("< 2", "<= 2")),
             fails_at=2, message_contains="A wall of exactly 2 gaps has a drop"),
        dict(why="the empty case forgotten (IndexError)", code=_drop("    return wall[0] - wall[-1]\n"), fails_at=2,
             message_contains="An empty wall has no first or last gap"),
        dict(why="only the first shrink (wall[0] - wall[1])", code=_drop("    return wall[0] - wall[1]\n"),
             fails_at=1, message_contains="only the first shrink"),
        dict(why="print instead of return", code=_drop("    print(wall[0] - wall[-1])\n"), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="the first visible answer hard-coded", code=_drop("    return 4\n"), fails_at=1,
             message_contains="for every visible test"),
        dict(why=".pop() for the last gap", code=_drop(DROP_BODY.replace("wall[-1]", "wall.pop()")), fails_at=2,
             message_contains="`.pop()` removes them"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-2a", opens_after="unit-4", ceiling="units-1-4",
             skills="empty-case,boundary,index-from-end", solo="false", dictates="", foreign_names="bells,bags",
             tests="visible=[48,47,44]->4,[60,58,55,51]->9; hidden=exactly two, one gap, a gap that grew, an empty "
             "wall, keeps its gaps") + "\n"
        "Spec: `total_drop(wall)` = first - last, and 0 with fewer than 2 items. The hidden order matters: 'a gap "
        "that grew' comes before 'an empty wall', so max - min gets its own message before `max([])`'s ValueError "
        "(both empty-wall crashes share one message anyway). One gap without a guard already gives 0 (first - last "
        "of one item), so only the empty wall catches a missing guard. Evidence: `<` vs `<=` (the unit brief), the "
        "empty case, the shrink as one pair (5A's neighbor loop).\n"
        "Show-rung copy-test: CP1's `return wall[0] - wall[-1]` in place of `pass`: no crash on the visible walls, "
        "passes CP1 (partial 1; the empty wall's IndexError is CP2's lesson, inside Mar'tu's check). CP2's `if "
        "len(wall) < 2:` with `return 0` under it, then the first-minus-last line below the `if` (the old rung's "
        "'and `return 0`' did not say where): the solution. CP1 hands over no sign; CP2 gives the one right `< 2`."
    ),
)

# ---- T-L-3 add_guess(wall, guess) ----

GUESS_TESTS = (
    "# Visible tests. They should show\n"
    "# [48, 47, 44, 40], then\n"
    "# [48, 47, 44].\n"
    + PASS_NOTE +
    "print(add_guess([48, 47, 44], 40))\n"
    "print(add_guess([48, 47, 44], 46))\n"
)


def _guess(body, tests=None):
    return "def add_guess(wall, guess):\n" + body + "\n\n" + (tests or GUESS_TESTS)


GUESS_BODY = "    if guess < wall[-1]:\n        wall.append(guess)\n    return wall\n"
GUESS_RULES = [
    ("_typed_cmp(_fd, 'guess')", "Compare `guess` with the newest gap, `wall[-1]`, not with a typed number."),
    ("_tn(_val) == 'list' and _val == [_args[1]] + _args[0]",
     "Put the guess at the end of the wall with `.append()`: `.insert(0, ...)` puts it at the front."),
    ("_tn(_val) == 'list' and _val == _args[0] + [_args[1]] and _args[1] == _args[0][-1]",
     "*Below* means smaller: a guess the same as the newest gap is not below it."),
    ("_tn(_val) == 'list' and _val == _args[0] + [_args[1]] and "
     "_call(_f, [_args[0], _args[0][0] + 5])[0] == _args[0] + [_args[0][0] + 5]",
     "Append only when the guess is below the newest gap: your function adds every guess."),
    ("_tn(_val) == 'list' and _val == _args[0] + [_args[1]] and _args[1] < _args[0][0]",
     "Compare the guess with the newest gap, `wall[-1]`, not the first one."),
    ("_tn(_val) == 'list' and _val == _args[0] + [_args[1]]",
     "Append only when the guess is below the newest gap."),
    ("_tn(_val) == 'list' and _val == _args[0]", "A guess below the newest gap should be appended."),
]
GUESS_FIX = "Append the guess only when it is below the newest gap, then hand back the wall."
GUESS_NOT_MIN = ("_val == _args[0] and _args[1] < _args[0][-1] and _args[1] >= _B.min(_args[0])",
                 "Compare the guess with the newest gap, `wall[-1]`, not the smallest gap: the newest is the last "
                 "one, whatever its size.")
GROW_COPY = ("_val is _in[0] or _in[0] == _a[0]",
             "Hand back the wall itself with `return wall`, not a copy: the guess is already on the caller's wall.",
             "it handed back a copy of the wall")
GROW = ("_val is _in[0]",
        "Append to the wall you are handed, then hand that wall back: your function made a new list, so the "
        "caller's wall did not change.",
        "the wall it was handed did not get the guess")

ADD_GUESS = trial(
    id="add-guess",
    title="Bomb Shell's Guess",
    minutes=7,
    summary="`add_guess(wall, guess)`: append the guess only if it is below the newest gap, then hand back the wall.",
    martu=(
        "Bomb Shell guesses the next gap: \"Thirty-two hours. Maybe less.\" Write `add_guess(wall, guess)`. It "
        "appends `guess` to the wall only if `guess` is below the newest gap. Then it hands back the wall. The wall "
        "always has at least one gap.\n"
        "```text\nadd_guess([48, 47, 44], 40)\n  -> [48, 47, 44, 40]\nadd_guess([48, 47, 44], 46)\n"
        "  -> [48, 47, 44]\n+ 4 hidden tests\n```"
    ),
    fn="add_guess",
    params=["wall", "guess"],
    predict=dict(
        q="Before you write: what will this print?",
        code="gaps = [9, 8]\nmore = gaps.append(7)\nprint(gaps)\nprint(more)\n",
        choices=["[9, 8, 7]\n[9, 8, 7]", "[9, 8, 7]\nNone", "[9, 8]\n[9, 8, 7]"],
        answer=1,
        explain=(
            "`.append()` changes the list it is called on, and hands back `None`. So append on one line, then hand "
            "back the wall on its own line."
        ),
    ),
    pair_talk=(
        "Pair talk: tell your partner why `return wall.append(guess)` hands back `None`. Then each of you writes "
        "your own version."
    ),
    starter=_guess("    pass\n"),
    solution=_guess(GUESS_BODY),
    rules=GUESS_RULES,
    visible=[
        dict(args=([48, 47, 44], 40), want=[48, 47, 44, 40], fix=GUESS_FIX),
        dict(args=([48, 47, 44], 46), want=[48, 47, 44], fix=GUESS_FIX),
    ],
    hidden=[
        dict(label="a guess the same as the newest gap", args=([30, 28], 28), want=[30, 28], fix=GUESS_FIX),
        dict(label="the wall you hand over gets the guess", args=([20, 18], 15), want=[20, 18, 15], fix=GUESS_FIX,
             after=[GROW_COPY, GROW]),
        dict(label="a wall of one gap", args=([37], 32), want=[37, 32], fix=GUESS_FIX),
        dict(label="a newest gap that is not the smallest", args=([40, 36, 38], 37), want=[40, 36, 38, 37],
             fix=GUESS_FIX, rules=[GUESS_NOT_MIN]),
    ],
    cp1=dict(
        text="Make the two visible tests hand back their walls.",
        hints=[
            "Row 2's guess, 46, is not below the newest gap, 44. So the wall stays as it is.",
            "Ask first, then change: `if coin < 5:` with `purse.append(coin)` inside it. Hand the list back after "
            "the `if`, not inside it.",
            "Inside `if guess < wall[-1]:` or `if guess <= wall[-1]:`, write `wall.append(guess)`. Below the "
            "`if`, write `return wall`. Both signs pass these two rows. The hidden test *a guess the same as the "
            "newest gap* decides the sign.",
        ],
        pass_line="Bomb Shell: Forty. Noted. Forty-six. Not noted.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests. They try a guess the same as the newest gap, the wall you hand over, one "
             "gap, and a newest gap that is not the smallest.",
        hints=[
            "Read *a guess the same as the newest gap*: is the same *below*?",
            "*Below* means smaller, so `<`. And `.append()` changes the very list you were handed, so the caller's "
            "wall gets the guess too.",
            "Use `if guess < wall[-1]:`, with `wall.append(guess)` inside it, and `return wall` below the `if`.",
        ],
        pass_line="Bomb Shell: Thirty-two. Maybe less. On the wall now.",
    ),
    foreign=["coin", "purse", "gaps", "more"],
    assemble=dict(
        lines=["def add_guess(wall, guess):", *GUESS_BODY.splitlines(), *_calls(GUESS_TESTS)],
        distractors=["    return wall.append(guess)", "    if guess <= wall[-1]:", "    if guess < wall[0]:"],
    ),
    another_way=[
        dict(angle="picture", label="Ask, change, hand back", text=(
            "```text\nguess < wall[-1] ?\n  yes -> wall.append(guess)\nthen   -> return wall\n```\n"
            "The `return` is not inside the `if`: both answers hand back the wall.")),
        dict(angle="everyday", label="A guest list", text=(
            "You add a name to the list only if they are invited. Either way, you hand the list back at the end.")),
        dict(angle="step-by-step", text=(
            "1. Compare `guess` with the newest gap, `wall[-1]`. 2. If it is smaller, `.append()` it. 3. After the "
            "`if`, `return wall`.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why='Bomb Shell studied the wall: "Thirty-two hours. Maybe less." 32 is below 37, so it goes on the wall.',
    ),
    takeaway="`.append()` changes the list and hands back `None`: append first, then `return` the list.",
    partials=[_guess("    if guess < wall[-1]:\n        return wall + [guess]\n    return wall\n")],
    wrong_answers=[
        dict(why="the starter (pass)", code=_guess("    pass\n"), fails_at=1, message_contains="Replace `pass`"),
        dict(why="return wall.append(guess): append hands back None",
             code=_guess("    if guess < wall[-1]:\n        return wall.append(guess)\n    return wall\n"), fails_at=1,
             message_contains="`.append()` changes the list but hands back `None`"),
        dict(why="<= for < (a guess the same as the newest is added)", code=_guess(GUESS_BODY.replace("<", "<=")),
             fails_at=2, message_contains="a guess the same as the newest gap is not below it"),
        dict(why="compared with the first gap, not the newest", code=_guess(GUESS_BODY.replace("wall[-1]", "wall[0]")),
             fails_at=1, message_contains="not the first one"),
        dict(why="a new list (wall + [guess]): the caller's wall never changes",
             code=_guess("    if guess < wall[-1]:\n        return wall + [guess]\n    return wall\n"), fails_at=2,
             message_contains="your function made a new list"),
        dict(why="appended always (no if)", code=_guess("    wall.append(guess)\n    return wall\n"), fails_at=1,
             message_contains="Append only when"),
        dict(why="the comparison backwards (guess > newest)", code=_guess(GUESS_BODY.replace("<", ">")), fails_at=1,
             message_contains="should be appended"),
        dict(why="print instead of return", code=_guess(GUESS_BODY.replace("return wall", "print(wall)")), fails_at=1,
             message_contains="in place of `print`"),
        dict(why="return only inside the if (a guess too high hands back None)",
             code=_guess("    if guess < wall[-1]:\n        wall.append(guess)\n        return wall\n"), fails_at=1,
             message_contains="Every case needs a `return`"),
        dict(why="the visible guess typed (guess == 40)",
             code=_guess("    if guess == 40:\n        wall.append(guess)\n    return wall\n"), fails_at=2,
             message_contains="`guess == 40` is typed for one test"),
        dict(why="append with no return", code=_guess("    if guess < wall[-1]:\n        wall.append(guess)\n"),
             fails_at=1, message_contains="has no `return` line"),
        dict(why="the smallest gap (min) for the newest: right on every falling wall",
             code=_guess(GUESS_BODY.replace("wall[-1]", "min(wall)")), fails_at=2,
             message_contains="not the smallest gap"),
        dict(why=".insert(0, guess): the guess at the front of the wall",
             code=_guess(GUESS_BODY.replace("wall.append(guess)", "wall.insert(0, guess)")), fails_at=1,
             message_contains="puts it at the front"),
        dict(why="appended in place, then a copy handed back (return wall[:])",
             code=_guess(GUESS_BODY.replace("return wall", "return wall[:]")), fails_at=2,
             message_contains="not a copy"),
        dict(why="a typed number between the visible guesses (guess < 45), not the newest gap",
             code=_guess(GUESS_BODY.replace("wall[-1]", "45")), fails_at=2,
             message_contains="not with a typed number"),
        dict(why="Show me how (CP1), pasted with its second sign `<=`: no crash, both visible rows pass; the hidden "
                 "test a guess the same as the newest gap decides", code=_guess(GUESS_BODY.replace("<", "<=")),
             fails_at=2, message_contains="(Hidden test: a guess the same as the newest gap."),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-3", opens_after="unit-4", ceiling="units-1-4",
             skills="append,compare,return-list,mutation", solo="false", dictates="", foreign_names="coin,purse,gaps",
             tests="visible=([48,47,44],40)->+40,([48,47,44],46)->same; hidden=a guess the same as the newest, the "
             "wall you hand over gets it (same list), one gap, a newest gap that is not the smallest "
             "([40,36,38],37)") + "\n"
        "Spec: T-L-3 `add_guess(wall, guess)` appends only if guess is below the newest gap, and returns the wall. "
        "'Returns the wall' is read as the SAME list (the core changes it in place; the variant asks for a new "
        "one), so the hidden 'the wall you hand over gets the guess' row checks identity: `wall + [guess]` passes "
        "every value and fails there (the reverse of T-L-3a's slip; partial 1). Evidence: `x = x.append()` / "
        "`return x.append()` (u04b `_handback`), `<` vs `<=`, wall[0] for the newest. The predict shows "
        "`.append()` handing back None (printed output only: no `None` in code before u07b). Check-breaker: "
        "every wall fell, so `min(wall)` passed for `wall[-1]` (T-L-1's own slip); the 'not the smallest' row "
        "catches it. `guess < 45` (a typed edge between the visible guesses) gets its own message.\n"
        "Teacher ruling (Nov 14): the visible guesses (40 and 46 against 44) cannot tell `<` from `<=`, so CP1's "
        "Show me how offers both, the right one first, and names *a guess the same as the newest gap*; CP2's "
        "gives `<` alone, with `wall.append(guess)` said to go inside the `if` (the old 'then' did not say "
        "where). Predict answer index 1. Show-rung copy-test: CP1 pasted in place of `pass` with `<` is the "
        "solution; with `<=` it runs, passes both visible rows and fails only that hidden test (wrong answer "
        "'Show me how ..., pasted with its second sign'). CP2 pasted in place of `pass`: the solution."
    ),
)

# ---- T-L-3a add_guess(wall, guess): a new list, the original unchanged ----

GUESS2_TESTS = (
    "# Visible tests. They should show\n"
    "# [48, 47, 44, 40], then\n"
    "# [48, 47, 44] (old, unchanged),\n"
    "# then [48, 47, 44] again.\n"
    "# (With only pass, calls show None.)\n"
    "old = [48, 47, 44]\n"
    "print(add_guess(old, 40))\n"
    "print(old)\n"
    "print(add_guess(old, 46))\n"
)
GUESS2_BODY = (
    "    new_wall = wall[:]\n"
    "    if guess < new_wall[-1]:\n"
    "        new_wall.append(guess)\n"
    "    return new_wall\n"
)
GUESS2_COPY_SOMETIMES = "    if guess < wall[-1]:\n        return wall[:] + [guess]\n    return wall\n"
KEEP_OLD = [
    ("not (_in[0] != _a[0] and _alias(_fd, 'wall'))",
     "A line like `new_wall = wall` gives the same list a second name, so appending changes the wall too. Copy "
     "it: `wall[:]`.",
     "the wall it was handed changed too"),
    ("_in[0] == _a[0]",
     "Leave the wall you were handed as it was: copy it first with `wall[:]`, and append to the copy.",
     "the wall it was handed changed too"),
]
NEW_LIST = ("_val is not _in[0]",
            "Hand back a new list here too: when the guess is not added, copy the wall with `wall[:]`.",
            "it handed back the very wall it was handed")

ADD_GUESS_NEW_LIST = trial(
    id="add-guess-new-list",
    title="Bomb Shell's Guess: A New List",
    level="advanced",
    variant_of="add-guess",
    minutes=7,
    summary="The advanced twin of Bomb Shell's Guess: hand back a new list, and leave the old wall unchanged.",
    martu=(
        "I want the old wall kept as it was, so a guess never smudges the chalk. Same rule, stricter: hand "
        "back a *new* list, and leave the wall you were handed unchanged. Hand back a new list even when the guess "
        "is not added.\n"
        "```text\nold = [48, 47, 44]\nadd_guess(old, 40)\n  -> [48, 47, 44, 40]\nold\n  -> [48, 47, 44]\n"
        "+ 4 hidden tests\n```"
    ),
    fn="add_guess",
    params=["wall", "guess"],
    example="coins = [5, 3]\nspare = coins[:]\nspare.append(1)\nprint(coins)\nprint(spare)\n",
    example_output="[5, 3]\n[5, 3, 1]",
    starter=_guess("    pass\n", GUESS2_TESTS),
    solution=_guess(GUESS2_BODY, GUESS2_TESTS),
    rules=GUESS_RULES,
    visible=[
        dict(args=([48, 47, 44], 40), want=[48, 47, 44, 40], fix=GUESS_FIX, after=KEEP_OLD),
        dict(args=([48, 47, 44], 46), want=[48, 47, 44], fix=GUESS_FIX, after=KEEP_OLD),
    ],
    hidden=[
        dict(label="a new list even when the guess is not added", args=([30, 28], 29), want=[30, 28], fix=GUESS_FIX,
             after=[NEW_LIST]),
        dict(label="a guess the same as the newest gap", args=([30, 28], 28), want=[30, 28], fix=GUESS_FIX,
             after=KEEP_OLD),
        dict(label="a wall of one gap", args=([37], 32), want=[37, 32], fix=GUESS_FIX, after=[*KEEP_OLD, NEW_LIST]),
        dict(label="a newest gap that is not the smallest", args=([40, 36, 38], 37), want=[40, 36, 38, 37],
             fix=GUESS_FIX, rules=[GUESS_NOT_MIN], after=KEEP_OLD),
    ],
    cp1=dict(
        text="Make the visible tests pass: the new list gets the guess, and `old` stays the same.",
        hints=[
            "Look at the second line printed: `old` must still be `[48, 47, 44]` after the call.",
            "`spare = coins[:]` makes a new list with the same items, so changing `spare` leaves `coins` alone. "
            "`spare = coins` only gives the same list a second name.",
            "Start with `new_wall = wall[:]`. Then append to `new_wall`, and hand it back.",
        ],
        pass_line="Mar'tu: The old wall is untouched. The chalk stays clean.",
    ),
    cp2=dict(
        text="Pass the 4 hidden tests. They try a new list even when the guess is not added, a guess the same as "
             "the newest gap, one gap, and a newest gap that is not the smallest.",
        hints=[
            "Read *a new list even when the guess is not added*: which list comes back when the `if` says no?",
            "Make the copy first, before the `if`, so both paths hand back the copy.",
            "Write `new_wall = wall[:]` as the first line of the function, and `return new_wall` as the last.",
        ],
        pass_line="Bomb Shell: New list. Old wall. Both correct. Good.",
    ),
    foreign=["coins", "spare", "chalk_wall"],
    assemble=dict(
        lines=["def add_guess(wall, guess):", *GUESS2_BODY.splitlines(), *_calls(GUESS2_TESTS)],
        distractors=["    new_wall = wall", "    wall.append(guess)", "    return wall"],
    ),
    another_way=[
        dict(angle="picture", label="Two lists, or one list with two names", text=(
            "```text\nnew_wall = wall     one list,\n                    two names\nnew_wall = wall[:]  two lists\n```")),
        dict(angle="everyday", label="A photocopy", text=(
            "Write your guess on a photocopy of the wall, not on the wall itself. The original stays clean, and you "
            "hand over the copy, guess or no guess.")),
        dict(angle="step-by-step", text=(
            "1. Copy: `new_wall = wall[:]`. 2. If the guess is below the newest gap, append it to `new_wall`. "
            "3. Hand back `new_wall`.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="Two weeks of real gaps are on that wall. A guess belongs on a copy, not on the record.",
    ),
    takeaway="`wall[:]` is a new list; `new = wall` is the same list with a second name. Copy before you change.",
    partials=[_guess(GUESS2_COPY_SOMETIMES, GUESS2_TESTS)],
    wrong_answers=[
        dict(why="the starter (pass)", code=_guess("    pass\n", GUESS2_TESTS), fails_at=1,
             message_contains="Replace `pass`"),
        dict(why="the core solution: the old wall changes", code=_guess(GUESS_BODY, GUESS2_TESTS), fails_at=1,
             message_contains="copy it first with `wall[:]`"),
        dict(why="new_wall = wall: a second name, not a copy",
             code=_guess(GUESS2_BODY.replace("wall[:]", "wall"), GUESS2_TESTS), fails_at=1,
             message_contains="a second name"),
        dict(why="the wall itself handed back when the guess is not added",
             code=_guess(GUESS2_COPY_SOMETIMES, GUESS2_TESTS), fails_at=2,
             message_contains="Hand back a new list here too"),
        dict(why="<= for <", code=_guess(GUESS2_BODY.replace("<", "<="), GUESS2_TESTS), fails_at=2,
             message_contains="not below it"),
        dict(why="return wall[:].append(guess): append hands back None",
             code=_guess("    if guess < wall[-1]:\n        return wall[:].append(guess)\n    return wall[:]\n",
                         GUESS2_TESTS), fails_at=1, message_contains="`.append()` changes the list but hands back `None`"),
        dict(why="the visible test's `old` read inside the function (the test table used as the input)",
             code=_guess(GUESS2_BODY.replace("new_wall = wall[:]", "new_wall = old[:]"), GUESS2_TESTS), fails_at=2,
             message_contains="it reads `old` from outside"),
        dict(why="print instead of return", code=_guess(GUESS2_BODY.replace("return new_wall", "print(new_wall)"),
                                                        GUESS2_TESTS),
             fails_at=1, message_contains="in place of `print`"),
        dict(why="the smallest gap (min) for the newest, on the copy",
             code=_guess(GUESS2_BODY.replace("new_wall[-1]", "min(new_wall)"), GUESS2_TESTS), fails_at=2,
             message_contains="not the smallest gap"),
        dict(why="Show me how (CP1), pasted in place of pass: the copy alone; no crash, the rest is named in words",
             code=_guess("    new_wall = wall[:]\n", GUESS2_TESTS), fails_at=1,
             message_contains="the function has no `return` line"),
        dict(why="Show me how (CP2), pasted in place of pass: the first and last lines; no crash, the append is "
                 "CP1's part", code=_guess("    new_wall = wall[:]\n    return new_wall\n", GUESS2_TESTS),
             fails_at=1, message_contains="A guess below the newest gap should be appended"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="T-L", trial="T-L-3a", opens_after="unit-4", ceiling="units-1-4",
             skills="copy-vs-alias,append,return-list", solo="false", dictates="", foreign_names="coins,spare",
             tests="visible=(old,40)->+40 and old unchanged,(old,46)->same; hidden=a new list even when not added "
             "(identity), the same as the newest, one gap, a newest gap that is not the smallest") + "\n"
        "Spec: returns a NEW list and leaves the original unchanged (`wall[:] + [guess]`). 'A new list' is read "
        "strictly (always a new list), which the Learn text says; the hidden identity row is the stricter spec's "
        "edge, and partial 1 copies only when it adds. The visible tests print `old` after the call, so the change "
        "to the caller's list is on screen. `list(wall)` and `wall[:] + [guess]` pass; `.copy()` passes too (not "
        "taught, allowed). Evidence: 3B-05 a copy changed instead of the original (and the reverse), 3C-01 a "
        "slice; the alias is the u04b check-breaker's 'second name for the wall'.\n"
        "The starter's note says '(With only pass, calls show None.)': here `print(old)` shows the wall, not "
        "`None`. Show-rung copy-test: CP1's `new_wall = wall[:]` in place of `pass` runs (no `return` yet: 'the "
        "function has no `return` line'; the append and the hand-back are named in words); CP2's first and last "
        "lines in place of `pass` run and hand back an unchanged copy (row 1 asks for the append, CP1's part); "
        "with the `if` from CP1 between them, the solution. Neither rung hands over a sign (the `<` is the core "
        "twin's, and the hidden test *a guess the same as the newest gap* still checks it)."
    ),
)

# ---------------------------------------------------------------------------------------------
# ITEMS
# ---------------------------------------------------------------------------------------------

ITEMS = [
    TRIALS_INTRO,
    HARD_CODED_LEDGER,
    CAN_CAST,
    CAN_CAST_SKILL_FIRST,
    CLOCK_COLOR,
    CLOCK_COLOR_FLASHING,
    PASSES_WITH_LUCK,
    WHICH_ROLL,
    NEWEST_GAP,
    NEWEST_GAP_EMPTY,
    LAST_THREE,
    TOTAL_DROP,
    ADD_GUESS,
    ADD_GUESS_NEW_LIST,
]
