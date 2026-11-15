"""Unit 6 "Loops", part c: Quick Check 5 (forms qc5-a and qc5-b, with their question forms qc5-a-questions and
qc5-b-questions) and the Loops cheatsheet ("Mar'tu's Chalk Notes: Loops").

Spec: design/curriculum.md, "## Unit 6 · Loops", items 8 and 9 ("### Quick Check 5" and "### Cheatsheet: Loops").
The spec files these under u06b; by assignment they live here, after u06a (Lessons 5A and 5B, Quiz 5) and u06b
(Project 5P, Extra practice 6X, Lesson 5C, Article 5-A1). This part introduces no concept. It uses `for`, `while`
and `break` (u06a), `continue`, a list in one line, a one-line choice and `.items()` (u06b, cheatsheet extras
only), `range()` and `len()` (Unit 4), `if` (Unit 2), and Unit 5's planned concepts only (u05a-c): dictionary
literals, reading by key and a list of dictionaries (`roster`). No recipes are written, no f-strings (Unit 9), no
`None` in code (u07b).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`for member in party.members:` at the bottom of the spell-book and mana-bars parts (written for them), the chalk
wall's shrink and Bomb Shell's Velocite watch. Every student has their own device; a Quick Check is done alone.

Titles follow the unit's order, as Unit 4 did (its qc3 forms are titled "Quick Check 4"): the forms are
"Quick Check 6 · Form A / B", and the ids keep the curriculum's names, qc5-a and qc5-b.

Revised on the teacher's rulings on the Unit 6 reviews (the Quick Check was not yet an honest fast path): C3 is
now a lean `while` write task, not a third repeat of the reset slip; Q3 tests the neighbor form students
practiced, `[i - 1]` with `range(1, len(wall))`; C1's lead and starter no longer read as a promise that `name`
or `mana` exists; the last pass line gives a student who tests out the story recap the lessons would have given
them; the forms take 14 minutes, not 12.

What the forms hold (spec table, in order: C1, C2, Q1, Q2, C3; C3 as the teacher ruled):
  C1  call a helper for each roster member. Form A `light_lantern(member["name"])`, form B
      `draw_bar(member["mana"])`. The roster and the helper live in hidden setup (2.12 rule 3: an engine-like
      helper and a prebuilt roster); the helper records every call (CALL) and prints a line. LOOP: a rerun with
      5 other heroes, so four typed calls fail (spec). The lead and the starter write the helper as
      `light_lantern(...)` / `draw_bar(...)` and say "hand it one hero's name / mana": the setup's own parameter
      word, `light_lantern(name)`, read as a promise, and `light_lantern(name)` in the loop is a NameError
      (proven; the crash wording is the site explainer's, a request to explain.ts).
  C2  total the party's mana, then print the names under 10 mana (2 CPs). The roster is visible (the student can
      SEE the numbers, so the typed total is a real temptation): form A after a night holding the barrier
      (6, 14, 3, 22: total 45; Oogrish and Bomb Shell), form B after one Strengthen Magic each at 10 mana a cast
      (8, 10, 14, 16: total 48; only Oogrish, and Gearshift's exactly-10 catches `<=` on the student's own run).
      CMB reruns with other mana (one sheet at exactly 10) and LOOP with 5 heroes.
  Q1  a `while` countdown (predict; off-by-one distractors). Q2 `break` at the first match (predict; "prints every
      match" distractor). Both in the question form.
  C3  a lean `while` write task (teacher ruling: it replaces the spec's "mend an accumulator that resets inside
      the loop", the third repeat of the reset slip). Form A, the ore watch, uses Bomb Shell's real numbers:
      `ore_left = 30` and `daily = 4`. While `ore_left` is at least `daily`, take `daily` off and print
      `ore_left`; count each pass in `days` and print it once, after the loop (26 ... 2, then 7). Form B, the
      barrier watch: `mana_left = 30`, `cost = 7` a night (23, 16, 9, 2, then 4 `nights`). Two reruns swap the two
      starter lines: the first lands exactly on a multiple, so `>` for `>=` stops one pass early, and both counts
      differ from the real run, so a typed count fails. The reset slip is still evidence here: `days = 0`
      inside the loop is a wrong answer.
Added beyond the spec's table (say so to the teacher): the question forms carry two more questions, Q3 "stop one
early" (which `range` keeps `wall[i - 1]` on the wall, in the neighbor form students practiced, `range(1,
len(wall))`: objective 5, which the spec's QC never tests) and Q4 "the loop that never ends" (an update outside the
loop / no update: objective 6's "recognize an infinite loop"). That gives four questions and questions_to_pass=3,
the shape of Unit 2's QC2 (the Unit 2 play-through ruling: the questions are gated, and they are the only place
some skills appear). Removing them means questions_to_pass=2 on two questions, with no slack for one misread
predict.

Help ladder (FORMAT.md, the Unit 2 walkthrough conventions): hints[0] Where to look, the middle hint teaches with
other names (`jars`, `coins`, `bags`, `sacks`, listed in foreign_names), the last hint holds the step's own line
in backticks, and its start is always in the solution. Quick Check exercises are support="none" (the hints are
written because the schema needs them) and explainer="lean" (teacher ruling: every QC exercise from Unit 2 on).
Every exercise also has another_way angles and assemble lines (a complete program that passes every checkpoint).

Check builders (u06a's guarded rerun, copied: each part file is plain data):
  _rerun(values)  the student's program again in a fresh namespace, with the FIRST top-level `name = <literal>`
                  line of each named variable swapped; a roster from hidden setup (C1) is swapped after the setup
                  runs. Guarded twice, so a loop that only never ends with the check's values can't freeze the
                  page: the buffer stops at 20,000 characters and a line budget (sys.settrace, main.py frames
                  only) stops it after 20,000 lines; either one gives "With other values, the loop never stopped."
  _case(None)     the student's own run, as it is (no evidence bracket); _case(values) a rerun.
  C3 adds _watch_case (the own run, with its two start values read from the student's own starter lines, or a
  rerun), _plan (what the watch should print and count) and _inorder (every number of the watch shows, in order).
Messages are lean (Unit 2 ruling for Quick Checks): they name the slip and keep the evidence bracket, "(Mar'tu's
check tried a roster of 5 other heroes, only inside the check.)", but never the line to type or the fix. A
near-miss name gets the lesson's sentence, "Python matches names letter for letter: you wrote `Total`, the task
needs `total`." Invented values only in reruns (Pell, Brakka, Moss, Glug, Ivo); a student's own text is never
repeated (a student's number may be). Proved at import, as Units 2-5 do: `_leaned` builds the lean helpers (`_gone`,
`_lstop`) from u06a's lesson helpers word for word (each rewrite must match, and the copy must still be u06a's text),
and `_lean_guard` fails the import if any check of either form shows a line of Mar'tu's version the starter does not,
or opens a sentence with a fix.

INFINITE LOOPS (read before writing any while-loop wrong answer): the site gives a run 5 seconds
(src/lib/languages/python/run.ts, "TimeoutError: The program ran too long and was stopped.") and stops a run that
prints more than 200,000 characters (public/workers/course_helpers.py, TooMuchOutput, then the always-full
"Printing forever?" explainer). The harness gives a run 6 seconds. Every endless-loop wrong answer here PRINTS on
each pass (C1's helper prints a line per call; C2's `while` for `if` prints a name; C3's watch prints the value
it takes off every pass), so it stops in milliseconds with "TooMuchOutput: This program printed more than
200,000 characters, so it was stopped." (fails_at 0), never waiting for the timeout. A student's own loop that
never ends and prints nothing gets the site's 5-second row. A loop that ends with the student's own numbers but
not with a rerun's stops at the check's own guard ("With other values, the loop never stopped.").

The class's slips, each proven by a wrong_answers entry:
  the for line's colon (C1, C2) and the body's indent (C1); handing over or printing the list, not the item (C1
  `light_lantern(roster)`, C2 `print(roster)`); `roster["name"]` / `roster["mana"]` for `member[...]` (C1, C2:
  the TypeError row); the item used as an index (C1 `roster[member]`); `for i in 4` and `for i in len(roster)`
  ('int' object is not iterable, C1) against a `range(4)` typed for one length (C1, LOOP); the total or count
  reset INSIDE the loop (C2 CP1, and C3's `days = 0` inside the loop); the final print indented inside the loop
  (C2 CP1, C3 `print(days)`) and a filter print outside it (C2 CP2, one name only; C3's watch print below the
  loop), the `if` outside the loop (C2 CP2); a `while` with no update, the update outside the loop or the update
  the wrong way (C3, all three print forever; C1 too); `while` for `if` (C2 CP2, prints forever) and `if` for
  `while` (C3: it asks once); `>` for `>=` (C3: a rerun lands exactly on a multiple) and `> 0` (C3: one pass too
  many); the count added to below the loop (C3); `break` in the wrong place (C2 CP2: a `break` after the first
  name; C3: a `break` after one pass; Q2's distractors); values typed by hand (four typed calls, the total or the
  sum typed, the names typed, the count typed, the daily use typed in the `while` line or the update, a typed
  print, and in every task a loop over a list typed in the code: each says 'typed in the code' or 'did not
  follow'); a `range()` typed for this length (C1 `range(4)`, C2 CP2: every LOOP rerun is longer and its last
  item counts); the campaign's list name copied (C1 `party.members`, a NameError with engine off) and a hint's
  names copied (C2 `bags`, C3 `sacks`). Neighbors are Q3's evidence, in the `[i - 1]` form the lessons practiced
  (its distractors: the full range, which reads `wall[-1]` on the first pass, a number for a range, and one past
  the end); the code tasks have no neighbor loop (the lessons and 5C-03 prove it in code).

Phone width (as u06a/u06b): fenced pictures, question code, starter comments and cheatsheet code keep to 36
characters a line. The one exception is editor code kept whole on one line because a wrapped list reads as two
lists: a visible roster sheet (up to 39 characters, C2).

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u06c
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# Shared by every check: the guarded rerun, the evidence bracket and a few readers. Plain Python, run in the
# student's namespace after their code, so every name starts with `_` and builtins come from `_B` (a student's
# `total = 0` or `sum = 3` can't break a check).
_PRE = r'''import ast as _ast
import copy as _copy
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_len, _str, _int, _rng, _any, _all, _zip, _set, _repr = (_B.len, _B.str, _B.int, _B.range, _B.any, _B.all,
                                                         _B.zip, _B.set, _B.repr)
def _tn(_v):
    return _B.type(_v).__name__
_SETUP = __SETUP__
_FROM_SETUP = __FROM_SETUP__
_LIT = ('List', 'Dict', 'Constant', 'Tuple', 'UnaryOp')
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
def _sh(_v):
    _k = _tn(_v)
    if _k == 'str':
        return '"' + _v + '"'
    if _k in ('list', 'tuple'):
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    if _k == 'dict':
        return '{' + ', '.join([_sh(_a) + ': ' + _sh(_b) for _a, _b in _v.items()]) + '}'
    return _B.str(_v)
def _shv(_v):
    # A student's own value is shown only when it is a number: never their words (2.11).
    if _tn(_v) in ('int', 'float', 'bool'):
        return _B.str(_v)
    return 'something else'
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
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
def _rerun(_values=None):
    _t = _ast.parse(_source)
    _vals = _B.dict(_values or {})
    _seen = []
    for _n in _t.body:
        if (_tn(_n) == 'Assign' and _B.len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id in _vals and _n.targets[0].id not in _seen and _tn(_n.value) in _LIT):
            _n.value = _lit(_vals[_n.targets[0].id], _n.value)
            _seen.append(_n.targets[0].id)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__'}
    _out = _sys.stdout
    _buf = _Cap()
    _err = ''
    _sys.stdout = _buf
    try:
        if _SETUP:
            _B.exec(_B.compile(_SETUP, '<setup>', 'exec'), _ns)
        for _k in _vals:
            if _k in _FROM_SETUP:
                _ns[_k] = _copy.deepcopy(_vals[_k])
        _code = _B.compile(_t, 'main.py', 'exec')
        _guarded(lambda: _B.exec(_code, _ns))
    except _Runaway as _e:
        _err = 'Runaway: ' + _B.str(_e)
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    _miss = [_k for _k in _vals if _k not in _seen and _k not in _FROM_SETUP]
    return _ns, _rows, _err, _miss
def _case(_vals):
    # None: the student's own run, as it is now (no evidence bracket).
    if _vals is None:
        return globals(), _lines(), '', []
    return _rerun(_vals)
__LEAN_HELPERS__
def _nums(_l):
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?!\d)(?!\.\d)', _l)]
def _parsed():
    return _ast.parse(_source)
def _in_loops(_t):
    # ids of every node inside a loop's body (the loop line itself not counted)
    _ids = _B.set()
    for _n in _ast.walk(_t):
        if _tn(_n) in ('For', 'While'):
            for _part in _n.body + _n.orelse:
                for _x in _ast.walk(_part):
                    _ids.add(_B.id(_x))
    return _ids
def _prints_of(_t, _name):
    return [_n for _n in _ast.walk(_t) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'print'
            and _any(_tn(_x) == 'Name' and _x.id == _name for _a in _n.args for _x in _ast.walk(_a))]
def _typed(_t, _name):
    # values typed by hand: a loop over a list written in the code, or `name = <numbers only>` (not 0)
    _walks = [_n for _n in _ast.walk(_t) if _tn(_n) == 'For' and _tn(_n.iter) == 'List']
    _sets = [_n for _n in _ast.walk(_t) if _tn(_n) == 'Assign'
             and _any(_tn(_x) == 'Name' and _x.id == _name for _x in _n.targets)
             and _tn(_n.value) in ('BinOp', 'Constant') and not (_tn(_n.value) == 'Constant' and _n.value.value == 0)
             and _all(_tn(_x) not in ('Name', 'Subscript', 'Call') for _x in _ast.walk(_n.value))]
    if _walks:
        return ': the loop walks a list typed in the code.'
    if _sets:
        return ': the number is typed in the code.'
    return '.'
def _zeros(_t, _name):
    # every `name = 0` line
    return [_n for _n in _ast.walk(_t) if _tn(_n) == 'Assign' and _tn(_n.value) == 'Constant'
            and _n.value.value == 0 and _any(_tn(_x) == 'Name' and _x.id == _name for _x in _n.targets)]
# Near-miss names (as Unit 1 and u04c): the names the student made, and the ones close to a task name.
def _made_names():
    _out = []
    for _n in _ast.walk(_parsed()):
        _k = _tn(_n)
        _ts = _n.targets if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'For') else [])
        for _x in _ts:
            if _tn(_x) == 'Name' and _x.id not in _out:
                _out.append(_x.id)
    return _out
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
def _lost(_w, _skip=()):
    # _skip: the task's other names, never offered as the near miss
    _n = [_m for _m in _made_names() if _m != _w and _m not in _skip and _close(_m, _w)]
    if _n:
        return 'Python matches names letter for letter: you wrote `' + _n[0] + '`, the task needs `' + _w + '`.'
    return 'No variable named `' + _w + '` was made.'
'''


def _leaned(code, pairs):
    """A Quick Check's helper (a test-out, no hints): the lesson's helper messages, rewritten to name the slip and the
    evidence, never the fix (the teacher's lean ruling, as Unit 2's QC2 does). Each pair must match, so a reworded
    lesson message cannot silently leave a fix in the Quick Check."""
    for old, new in pairs:
        assert old in code, f"lean rewrite does not match: {old[:70]!r}"
        code = code.replace(old, new)
    return code


# u06a's lesson helpers, word for word (Lessons 5A and 5B). Their messages lead with the fix ("Keep the line ...",
# "Make sure the loop can end ...", "Make it work for another roster too."), so the Quick Check says the slip and the
# evidence instead: _gone (the starter's line is gone) and _lstop (what stopped Python, and the evidence).
_LESSON_HELPERS = """def _keep(_name):
    return ('Keep the line `' + _name + " = ...` from the starter, so Mar'tu's check can try other values there.")
def _stop(_err, _ev, _fix='Make it work for another roster too.'):
    if _err.startswith('Runaway'):
        return 'Make sure the loop can end, whatever the values. With other values, your loop never stopped.' + _ev
    return _fix + ' With other values, Python stopped: ' + _err + '.' + _ev
"""
_HELPERS_LEAN = [
    ("""def _keep(_name):
    return ('Keep the line `' + _name + " = ...` from the starter, so Mar'tu's check can try other values there.")""",
     "def _gone(_name):\n"
     "    return 'The line `' + _name + \" = [` from the starter is gone, so Mar'tu's check has nothing to swap.\""),
    ("def _stop(_err, _ev, _fix='Make it work for another roster too.'):",
     "def _lstop(_err, _ev):\n    # Lean: what stopped Python, and the evidence. No fix."),
    ("return 'Make sure the loop can end, whatever the values. With other values, your loop never stopped.' + _ev",
     "return 'With other values, the loop never stopped.' + _ev"),
    ("return _fix + ' With other values, Python stopped: ' + _err", "return 'With other values, Python stopped: ' + _err"),
]


def _lesson_helpers_match():
    """The copy above is u06a's own text (when u06a sits beside this file, as in the repo and in a staging folder)."""
    try:
        lesson = __import__("pathlib").Path(__file__).with_name("u06a_loops_for_while.py")
    except NameError:
        return
    if lesson.exists():
        text = lesson.read_text(encoding="utf8")
        for row in _LESSON_HELPERS.strip("\n").split("\n"):
            assert row in text, f"u06c's copy of the lesson helpers no longer matches u06a: {row[:70]!r}"


_lesson_helpers_match()
_PRE = _PRE.replace("__LEAN_HELPERS__\n", _leaned(_LESSON_HELPERS, _HELPERS_LEAN))

def chk(label, body, setup="", from_setup=(), **subs):
    """A check: the shared _PRE (with this exercise's hidden setup), then `body` with each __NAME__ replaced by
    repr(value)."""
    pre = _PRE.replace("__SETUP__", repr(setup)).replace("__FROM_SETUP__", repr(tuple(from_setup)))
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    return (label, pre + body)


# ---------------------------------------------------------------------------------------------
# The data (the real party table and the real chalk wall; reruns use invented heroes)
# ---------------------------------------------------------------------------------------------

# The real chalk wall: its shrinks, 0, 1, 1, 2, 3, 4, are the ones the last pass line recaps.
WALL = [48, 48, 47, 46, 44, 41, 37]


def sheet(name, mana, max_mana=None, affinity=None):
    out = {"name": name, "mana": mana}
    if max_mana is not None:
        out["max_mana"] = max_mana
    if affinity is not None:
        out["abilities"] = {"magical_affinity": affinity}
    return out


def roster_code(sheets):
    """A visible roster, one sheet per line, name and mana only (up to 39 characters a line)."""
    lines = ["roster = ["] + ['    {"name": "%s", "mana": %d},' % (s["name"], s["mana"]) for s in sheets] + ["]"]
    return "\n".join(lines) + "\n"


# The party at full mana (C1, both forms): max mana is the real table, 18 / 20 / 24 / 26.
FULL_SHEETS = [sheet("Oogrish", 18, 18, 9), sheet("Gearshift", 20, 20, 10), sheet("Bomb Shell", 24, 24, 12),
               sheet("Lucky", 26, 26, 13)]
# After a night holding the barrier (as u06a): C2 form A. Total 45; under 10: Oogrish, Bomb Shell.
NIGHT = [sheet("Oogrish", 6), sheet("Gearshift", 14), sheet("Bomb Shell", 3), sheet("Lucky", 22)]
# After one Strengthen Magic each, at 10 mana a cast (as u06b's project): C2 form B. Total 48; under 10: Oogrish
# only, and Gearshift sits at exactly 10.
STRONG = [sheet("Oogrish", 8), sheet("Gearshift", 10), sheet("Bomb Shell", 14), sheet("Lucky", 16)]
# Five other heroes (invented names): the LOOP rerun. A program written for 4 lines cannot follow 5.
OTHER5 = [sheet("Pell", 31), sheet("Brakka", 7), sheet("Moss", 15), sheet("Glug", 3), sheet("Ivo", 9)]
OTHER_SHEETS = [sheet("Pell", 31, 34, 17), sheet("Brakka", 7, 12, 6), sheet("Moss", 15, 16, 8),
                sheet("Glug", 3, 10, 5), sheet("Ivo", 9, 22, 11)]

EV_FIVE = " (Mar'tu's check tried a roster of 5 other heroes, only inside the check.)"


def ev_mana(values):
    return (" (Mar'tu's check tried the same heroes with other mana: " + ", ".join(str(v) for v in values[:-1])
            + " and " + str(values[-1]) + ", only inside the check.)")


def ev_list(name, values):
    return " (Mar'tu's check tried `%s = %s`, only inside the check.)" % (name, values)


def same_heroes(sheets, manas):
    return [sheet(s["name"], m) for s, m in zip(sheets, manas)]


# =============================================================================================
# UNIT (repeated in every part file of loops)
# =============================================================================================

UNIT = dict(
    id="loops",
    order=6,
    title="Loops",
    subtitle="Every Member of the Party",
    published=True,
    martu_intro=(
        "Four heroes. Four bars to draw. Write it four times? No. Write it once, and let Python walk down the "
        "line, yes?\n"
        "You have seen loops already: `for member in party.members:` at the bottom of the spell book and the mana "
        "bars. Somebody else wrote them for you. Since then you have written recipes and lists of your own. Tonight "
        "you write them yourself, one pass at a time."
    ),
    goals=[
        "Say why loops exist, and write `for item in items:` with an indented body",
        "Loop over a list of sheets, read keys from each `member`, and call a recipe for each one",
        "Keep a running total, with `total = 0` before the loop",
        "Put an `if` inside a loop to pick out some items",
        "Compare neighbors with `range(1, len(chalk_wall))`, and see the decay for yourself",
        "Write a `while` loop that changes its value each pass, stop a loop that never ends, and leave early "
        "with `break`",
    ],
    campaign_links=["friends-in-low-places"],
)

# No new terms: u06a and u06b define the unit's loop terms (for loop, loop variable, running total, while loop,
# infinite loop, break, continue, ...), and Units 1-5 define theirs.
GLOSSARY = []


# =============================================================================================
# Quick Check 5 (test-out), forms A and B: three code tasks each, plus four questions each.
# =============================================================================================

_STUCK = "Stuck? Skip it, or try the lesson For Each, Yes? Tasks you pass here stay ticked."


def _qc_meta(skills, dictates="", foreign="", form="A", level="S2"):
    return meta(starter_level=level, path="QC5", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# ---- C1: call a helper for each roster member (for-each, list-of-dicts) ----------------------------------------

def _qc_each(form, helper, key, rec, setup_def, starter, noun, past, what, whats, a_what, same, lead, pass_line):
    """helper(member[key]) once per member, in roster order. rec: the setup's call record. noun/past: "lantern" /
    "lit" (form A), "bar" / "drawn" (form B); what / a_what: "name" / "a name", "mana" / "a number"."""
    setup = setup_def + "roster = " + repr(FULL_SHEETS) + "\n"
    line = f'    {helper}(member["{key}"])'

    def program(body=line, head="for member in roster:", tail=""):
        return starter + (head + "\n" if head else "") + body + "\n" + tail

    solution = program()
    each = chk(
        f"{helper} gets each member's {what}, in roster order",
        r'''
_b = globals().get(__REC__)
_want = [_m[__KEY__] for _m in __SHEETS__]
if _b != _want:
    _b = _b if _tn(_b) == 'list' else []
    _shown = [_l for _l in _lines() if _any(_str(_w) in _l for _w in _want)]
    if not _b:
        assert not _shown, 'The ' + __WHATS__ + ' were printed, but `' + __HELPER__ + '` was never called.'
        assert False, 'No ' + __NOUN__ + ' was ' + __PAST__ + ': `' + __HELPER__ + '` was never called.'
    assert not _any(_tn(_x) == 'dict' for _x in _b), '`' + __HELPER__ + '` was handed a whole sheet, not ' + __AWHAT__ + '.'
    assert not _any(_tn(_x) == 'list' for _x in _b), (
        '`' + __HELPER__ + '` was handed the whole roster, not ' + __AWHAT__ + '.')
    _odd = [_x for _x in _b if _tn(_x) != _tn(_want[0])]
    assert not _odd, ('`' + __HELPER__ + '` was handed ' + ('text' if _tn(_odd[0]) == 'str' else 'a number')
                      + ', not ' + __AWHAT__ + '.')
    assert _len(_b) != 1, '`' + __HELPER__ + '` ran once, not once for each member.'
    assert _len(_set([_repr(_x) for _x in _b])) > 1, __SAME__
    assert _len(_b) == _len(_want), ('`' + __HELPER__ + '` ran ' + _str(_len(_b)) + ' times for '
                                     + _str(_len(_want)) + ' members.')
    assert False, 'The ' + __NOUN__ + 's do not follow the members, in roster order.'
''',
        REC=rec, KEY=key, SHEETS=FULL_SHEETS, WHAT=what, WHATS=whats, HELPER=helper, NOUN=noun, PAST=past,
        AWHAT=a_what, SAME=same,
    )
    five = chk(
        "the loop follows a roster of 5",
        r'''
_ns, _rows, _err, _miss = _rerun({'roster': __OTHER__})
assert not _err, _lstop(_err, __EV__)
_b = _ns.get(__REC__) or []
_want = [_m[__KEY__] for _m in __OTHER__]
if _b != _want:
    # the same values as the real party: typed in the code, not read from each sheet
    assert _b != [_m[__KEY__] for _m in __SHEETS__], (
        'With another roster, the same 4 ' + __NOUN__ + 's were ' + __PAST__ + ' as before: the ' + __WHATS__
        + ' are typed in the code, not read from each sheet.' + __EV__)
    assert _b != [_m.get('max_mana') for _m in __OTHER__], (
        "With another roster, the bars showed each hero's `max_mana`, not their `mana`." + __EV__)
    assert _len(_b) != 4, 'With 5 heroes in `roster`, only 4 ' + __NOUN__ + 's were ' + __PAST__ + '.' + __EV__
    assert False, 'With another roster, the ' + __NOUN__ + 's did not follow its sheets.' + __EV__
''',
        setup=setup,
        from_setup=("roster",),
        REC=rec, KEY=key, OTHER=OTHER_SHEETS, EV=EV_FIVE, NOUN=noun, PAST=past, SHEETS=FULL_SHEETS, WHATS=whats,
    )
    typed = "".join(f'{helper}({s[key]!r})\n'.replace("'", '"') for s in FULL_SHEETS)
    other_key = "mana" if key == "name" else "name"
    return dict(
        id="a-helper-for-each",
        title="One call for each member",
        martu=lead + "My check also tries a roster of other heroes, only inside the check, so let the loop do the "
        "work.\n" + _STUCK,
        names=["roster", helper],
        support="none",
        explainer="lean",
        setup=setup,
        starter=starter,
        checkpoints=[
            dict(
                id="call-for-each",
                text=f"For each member of `roster`, call `{helper}(...)` with that member's {what}.",
                dictated=False,
                hints=[
                    "`roster` is a list of sheets. A `for` line walks it, one sheet at a time. The call goes "
                    "inside the loop, with four spaces in front.",
                    "With other names:\n```python\nfor jar in jars:\n    refill(jar[\"spice\"])\n```\nEach pass "
                    "hands over one jar's spice.",
                    f"Write `{helper}(member[\"{key}\"])` inside `for member in roster:`, with four spaces in "
                    "front.",
                ],
                checks=[each, five],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=["for member in roster:", line],
            distractors=[f'    {helper}(roster["{key}"])', f"    {helper}(member)", "for member in roster"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                "1. `for member in roster:` takes the first sheet and calls it `member`.\n"
                f"2. The indented call hands over that sheet's `\"{key}\"`.\n"
                "3. Python takes the next sheet, until the roster runs out.")),
            dict(angle="from the campaign", text=(
                "At the bottom of the spell book: `for member in party.members:`, then one call with "
                "`member[\"spell_book\"]`. One call, inside the loop, for every member.")),
            dict(angle="shorter", text=f"One `for` line, one indented call, `member[\"{key}\"]` inside it."),
        ],
        takeaway=f"`for member in roster:` then `{helper}(member[\"{key}\"])`, indented: one call per sheet.",
        wrong_answers=[
            dict(why="the starter (comments only: nothing called)", code=starter, fails_at=1,
                 message_contains="never called"),
            dict(why="four typed calls, no loop (CALL passes, LOOP fails)", code=starter + typed, fails_at=1,
                 message_contains="typed in the code"),
            dict(why="a loop, but over the values typed by hand (CALL passes, LOOP fails)",
                 code=starter + "for x in [" + ", ".join(repr(s[key]).replace("'", '"') for s in FULL_SHEETS)
                 + f"]:\n    {helper}(x)\n", fails_at=1, message_contains="typed in the code"),
            dict(why="four reads by position, no loop (CALL passes, LOOP fails)",
                 code=starter + "".join(f'{helper}(roster[{i}]["{key}"])\n' for i in range(4)), fails_at=1,
                 message_contains="only 4"),
            dict(why="the whole sheet handed over", code=program(f"    {helper}(member)"), fails_at=1,
                 message_contains="whole sheet"),
            dict(why="the list handed over, not the item (roster where member belongs)",
                 code=program(f"    {helper}(roster)"), fails_at=1, message_contains="whole roster"),
            dict(why=f'roster["{key}"] for member["{key}"] (the TypeError row)',
                 code=program(f'    {helper}(roster["{key}"])'), fails_at=0,
                 message_contains="list indices must be integers"),
            dict(why="the item used as an index (roster[member])",
                 code=program(f'    {helper}(roster[member]["{key}"])'), fails_at=0,
                 message_contains="list indices must be integers"),
            dict(why=f"print for {helper}", code=program(f'    print(member["{key}"])'), fails_at=1,
                 message_contains="was never called"),
            dict(why="the other key handed over", code=program(f'    {helper}(member["{other_key}"])'), fails_at=1,
                 message_contains="was handed " + ("a number" if key == "name" else "text")),
            dict(why="the for line without its colon", code=program(head="for member in roster"), fails_at=0,
                 message_contains="expected ':'"),
            dict(why="the body not indented", code=program(line.strip()), fails_at=0,
                 message_contains="expected an indented block"),
            dict(why="the call below the loop, not indented: it runs once",
                 code=program("    pass", tail=line.strip() + "\n"), fails_at=1, message_contains="ran once"),
            dict(why="the first sheet every pass (roster[0])", code=program(f'    {helper}(roster[0]["{key}"])'),
                 fails_at=1, message_contains=same[:20]),
            dict(why="the campaign's list name copied (engine off: party is not defined)",
                 code=program(head="for member in party.members:"), fails_at=0,
                 message_contains="'party' is not defined"),
            dict(why="a loop over a number: for i in 4", code=program(f'    {helper}(roster[i]["{key}"])',
                                                                    head="for i in 4:"), fails_at=0,
                 message_contains="'int' object is not iterable"),
            dict(why="len without range: for i in len(roster)",
                 code=program(f'    {helper}(roster[i]["{key}"])', head="for i in len(roster):"), fails_at=0,
                 message_contains="'int' object is not iterable"),
            dict(why="range typed for this length: range(4)",
                 code=program(f'    {helper}(roster[i]["{key}"])', head="for i in range(4):"), fails_at=1,
                 message_contains="only 4"),
            dict(why="the key without quotes (NameError)", code=program(f"    {helper}(member[{key}])"), fails_at=0,
                 message_contains=f"'{key}' is not defined"),
            dict(why=f"the helper's own word read as a promise: {helper}({key}) in the loop (NameError)",
                 code=program(f"    {helper}({key})"), fails_at=0, message_contains=f"'{key}' is not defined"),
            dict(why="the key with a capital (KeyError)", code=program(f'    {helper}(member["{key.capitalize()}"])'),
                 fails_at=0, message_contains="KeyError"),
            dict(why="a while loop over positions with no update: it never ends (prints forever)",
                 code=starter + f'i = 0\nwhile i < len(roster):\n    {helper}(roster[i]["{key}"])\n', fails_at=0,
                 message_contains="printed more than"),
            dict(why="the while loop's update outside the loop: it never ends",
                 code=starter + f'i = 0\nwhile i < len(roster):\n    {helper}(roster[i]["{key}"])\ni = i + 1\n',
                 fails_at=0, message_contains="printed more than"),
        ] + ([
            dict(why="max_mana for mana (the same at full mana: only the rerun tells them apart)",
                 code=program(f'    {helper}(member["max_mana"])'), fails_at=1, message_contains="`max_mana`"),
        ] if key == "mana" else []),
        notes=_qc_meta("for-each,list-of-dicts", foreign="jars,jar,refill,spice", form=form) + "\n"
        f"QC5 C1, form {form}. Hidden setup (2.12 rule 3): the four sheets at full mana (real table values) and "
        f"`{helper}({what})`, a CALL recorder (it keeps each value in `{rec}` and prints a line). CP1 [ND]: the "
        f"record must be the members' `\"{key}\"` values in roster order (CALL), and a rerun with 5 other heroes "
        "swapped in after the setup must follow (LOOP): four typed calls, or a loop over the values typed by hand, "
        "repeat the real party ('typed in the code'), and `range(4)` or four reads by position show 4 (spec: 'four "
        "typed calls -> LOOP'). Any loop variable passes, and so do `for i in range(len(roster))` and a `while` with "
        "its update inside. Catches: the whole sheet, the whole roster, `roster[...]` / `roster[member]` "
        "(TypeError), print for the call, the other key, the colon, the indent, a call that runs once, "
        "`roster[0]`, the campaign's `party.members` (NameError, engine off), `for i in 4` / `len(roster)` "
        "('int' object is not iterable), the unquoted key, the capital key, "
        f"`{helper}({key})` in the loop (the setup's own parameter word read as a promise: NameError; the lead "
        f"and the starter now write `{helper}(...)` and say what to hand it, as the teacher ruled, and the "
        "crash wording is a site request to explain.ts), a `while` with no update or the "
        "update outside the loop (both print forever: TooMuchOutput at once), and in form B `member[\"max_mana\"]` "
        "(equal at full mana, so only the rerun tells them apart). Lean messages. explainer='lean'."
    )


LANTERN_SETUP = (
    "_lanterns = []\n"
    "def light_lantern(name):\n"
    "    _lanterns.append(name)\n"
    '    print("A lantern glows for " + str(name) + ".")\n'
)
LANTERN_STARTER = (
    "# roster holds 4 hero sheets, like\n"
    '# {"name": "Oogrish", "mana": 18}\n'
    "# For each member of roster, light\n"
    "# a lantern with their name:\n"
    "# light_lantern(...) with one\n"
    "# hero's name\n"
)
BAR_SETUP = (
    "_bars = []\n"
    "def draw_bar(mana):\n"
    "    _bars.append(mana)\n"
    "    if type(mana) == int:\n"
    '        print("█" * mana + " " + str(mana))\n'
    "    else:\n"
    "        print(mana)\n"
)
BAR_STARTER = (
    "# roster holds 4 hero sheets, like\n"
    '# {"name": "Oogrish", "mana": 18}\n'
    "# For each member of roster, draw\n"
    "# a bar with their mana:\n"
    "# draw_bar(...) with one\n"
    "# hero's mana\n"
)


# ---- C2: a running total, then a check inside the loop (accumulate, loop-with-if) -------------------------------

STEP1 = "# 1. Add up the party's mana in\n#    total. Print total once.\n"
STEP2 = "# 2. Print the name of each member\n#    with less than 10 mana.\n"
TOTAL_PART = 'total = 0\nfor member in roster:\n    total = total + member["mana"]\nprint(total)\n'
TIRED_PART = 'for member in roster:\n    if member["mana"] < 10:\n        print(member["name"])\n'


def _qc_tally(form, story, sheets, other_mana, lead, pass_total, pass_tired):
    roster = story + roster_code(sheets)
    mana_other = same_heroes(sheets, other_mana)
    ev_m = ev_mana(other_mana)
    own_total = sum(s["mana"] for s in sheets)
    tired = [s["name"] for s in sheets if s["mana"] < 10]

    def program(total=TOTAL_PART, tired_code=TIRED_PART):
        return roster + STEP1 + total + STEP2 + tired_code

    starter = roster + STEP1 + "\n" + STEP2
    solution = program()
    total_check = chk(
        "total holds the party's mana, and follows other sheets",
        r'''
_t0 = _parsed()
_ins = _in_loops(_t0)
_reset = [_n for _n in _zeros(_t0, 'total') if _B.id(_n) in _ins]
_loops = [_n for _n in _ast.walk(_t0) if _tn(_n) in ('For', 'While')]
_bare = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'Expr' and _tn(_n.value) == 'BinOp' and _B.id(_n) in _ins]
# a top-level loop that adds to total, and a `total = 0` below it (the sum wiped once it is made)
_adders = [_n for _n in _t0.body if _tn(_n) in ('For', 'While') and _any(
    _tn(_x) == 'Name' and _x.id == 'total' and _tn(_x.ctx) == 'Store' for _x in _ast.walk(_n))]
_wiped = [_z for _z in _zeros(_t0, 'total') if _B.id(_z) not in _ins and _adders and _z.lineno > _adders[0].lineno]
_own = None
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__), ({'roster': __FIVE__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _gone('roster')
    assert not _err, _lstop(_err, _ev)
    _r = _ns.get('roster')
    assert _tn(_r) == 'list' and _r and _all(_tn(_m) == 'dict' and 'mana' in _m for _m in _r), (
        "`roster` no longer holds the starter's sheets.")
    assert 'total' in _ns, _lost('total')
    _want = 0
    for _m in _r:
        _want = _want + _m['mana']
    _got = _ns['total']
    if _vals is None:
        _own = _got
    if _got == _want:
        continue
    _last = _r[-1]['mana']
    assert not (_got == _last and _reset), (
        "`total` restarts every pass: it ended as only the last member's mana, " + _str(_last) + '.' + _ev)
    assert not (_bare and _got == 0), 'The sum is worked out on a line of its own, then forgotten: `total` is still 0.'
    assert not (_wiped and _got == 0), '`total` is set back to 0 after the loop, so the sum is wiped: it ends as 0.'
    assert _got != 0, '`total` is still 0: nothing was added to it.' + _ev
    assert _got != _last, ("`total` ended as only the last member's mana, " + _str(_last) + ': each pass replaced '
                           'it.' + _ev)
    assert not (_vals is not None and _got == _own), (
        '`total` stayed ' + _shv(_own) + ' when the sheets held other mana' + _typed(_t0, 'total') + _ev)
    _four = 0
    for _m in _r[:4]:
        _four = _four + _m['mana']
    assert not (_len(_r) == 5 and _got == _four), 'With 5 heroes in `roster`, `total` left one out.' + _ev
    assert _loops, "`total` ended as " + _shv(_got) + ", not the party's mana added up, and there is no loop."
    assert False, "`total` ended as " + _shv(_got) + ", not the party's mana added up." + _ev
''',
        MANA=mana_other, EVM=ev_m, FIVE=OTHER5, EV5=EV_FIVE,
    )
    total_printed = chk(
        "the total prints once, after the loop",
        r'''
_t0 = _parsed()
_ins = _in_loops(_t0)
assert not [_p for _p in _prints_of(_t0, 'total') if _B.id(_p) in _ins], (
    '`total` printed on every pass, not once after the loop.')
_tops = [_n for _n in _t0.body if _tn(_n) in ('For', 'While') and _any(
    _tn(_x) == 'Name' and _x.id == 'total' and _tn(_x.ctx) == 'Store' for _x in _ast.walk(_n))]
_early = [_p for _p in _prints_of(_t0, 'total') if _tops and _p.lineno < _tops[0].lineno]
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _err, _lstop(_err, _ev)
    _seen = [_x for _l in _rows for _x in _nums(_l)]
    if _ns.get('total') in _seen:
        continue
    assert not _early, '`total` printed above the loop, before anything was added to it.'
    assert _vals is not None, '`total` was never printed.'
    assert False, 'The printed total did not follow the sheets.' + _ev
''',
        MANA=mana_other, EVM=ev_m,
    )
    tired_check = chk(
        "only the members under 10 mana print, and the names follow other sheets",
        r'''
_t0 = _parsed()
_fors = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For']
_targets = [_n.target.id for _n in _fors if _tn(_n.target) == 'Name']
_outside = [_n for _n in _t0.body if _tn(_n) == 'If'
            and _any(_tn(_x) == 'Name' and _x.id in _targets for _x in _ast.walk(_n.test))]
_ins = _in_loops(_t0)
_in_prints = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'print'
              and _B.id(_n) in _ins]
_own = None
for _vals, _ev in ((None, ''), ({'roster': __MANA__}, __EVM__), ({'roster': __FIVE__}, __EV5__)):
    _ns, _rows, _err, _miss = _case(_vals)
    assert not _miss, _gone('roster')
    assert not _err, _lstop(_err, _ev)
    _r = _ns.get('roster')
    _names = [_m['name'] for _m in _r]
    _want = [_m['name'] for _m in _r if _m['mana'] < 10]
    _said = []
    for _l in _rows:
        # a whole sheet or a whole roster printed is not a name; a printed list of names is (append, 5C-03)
        if _l.startswith('{') or (_l.startswith('[') and '{' in _l):
            continue
        if _l.startswith('['):
            try:
                _v = _ast.literal_eval(_l)
            except Exception:
                _v = None
            if _tn(_v) == 'list' and _all(_tn(_x) == 'str' for _x in _v):
                _said.extend([_x for _x in _v if _x in _names])
                continue
        # every name on the line, in the order it appears
        _said.extend([_n for _p, _n in _B.sorted([(_l.find(_n), _n) for _n in _names if _n in _l])])
    if _vals is None:
        _own = _said
    if _said == _want:
        continue
    assert not _any(_l.startswith('[') and '{' in _l for _l in _rows), 'The whole roster printed, not one name.'
    assert not _any(_l.startswith('{') for _l in _rows), 'A whole sheet printed, not a name.'
    assert not _outside, 'The `if` ran once, after the loop, so only the last member was checked.'
    assert _said, 'No names printed.' + _ev
    assert _said != _names, "Every member's name printed, not only those under 10 mana." + _ev
    assert not (_uses('node:Break') and _len(_said) == 1 and _len(_want) > 1), (
        'Only one name printed: the loop stopped at the first.' + _ev)
    assert not (_vals is not None and _said == _own), 'With other mana on the sheets, the same names printed.' + _ev
    _extra = [_n for _n in _said if _n not in _want]
    # the `<=` slip: every extra name is a member at exactly 10
    _ten = [_m['name'] for _m in _r if _m['mana'] == 10 and _m['name'] in _said]
    assert not (_ten and _all(_n in _ten for _n in _extra)), 'A member with exactly 10 mana printed too.' + _ev
    _big = [_m['name'] for _m in _r if _m['mana'] > 10]
    assert not _all(_n in _big for _n in _said), 'The members with more than 10 mana printed, not those under 10.' + _ev
    # one name, printed from outside every loop (the filter print below the loop)
    assert not (_len(_said) == 1 and _len(_want) > 1 and not _in_prints), (
        'Only one name printed, not one for each member under 10 mana.' + _ev)
    assert not (_extra and _all(_w in _said for _w in _want)), 'Members with 10 mana or more printed too.' + _ev
    _left = [_m for _m in _r if _m['name'] in _want and _m['name'] not in _said]
    assert not (_left and not _extra), (_left[0]['name'] + ', with ' + _str(_left[0]['mana'])
                                       + ' mana, did not print.' + _ev) if _left else ''
    assert False, 'The names printed are not the members under 10 mana, in roster order.' + _ev
''',
        MANA=mana_other, EVM=ev_m, FIVE=OTHER5, EV5=EV_FIVE,
    )
    one_loop = (
        'total = 0\nfor member in roster:\n    total = total + member["mana"]\n    if member["mana"] < 10:\n'
        '        print(member["name"])\nprint(total)\n'
    )
    typed_names = "".join(f'print("{name}")\n' for name in tired)
    return dict(
        id="total-and-tired",
        title="A total, then who needs rest",
        martu=lead + "My check tries other sheets, only inside the check, so never type a number or a name you "
        "can see.\n" + _STUCK,
        names=["roster", "total"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="add-up-the-mana",
                text="Add up every member's mana in `total`, and print `total` once, after the loop.",
                dictated=False,
                hints=[
                    "A tally starts once, above the loop. Each pass adds one member's mana. The print goes below "
                    "the loop, with no spaces in front.",
                    "With other names:\n```python\ncoins = 0\nfor bag in bags:\n    coins = coins + bag[\"left\"]\n"
                    "print(coins)\n```",
                    "Write `total = 0` above `for member in roster:`, then `total = total + member[\"mana\"]` "
                    "inside it, and `print(total)` below it.",
                ],
                checks=[total_check, total_printed],
                pass_line=pass_total,
            ),
            dict(
                id="who-needs-rest",
                text="Print the name of each member with less than 10 mana.",
                dictated=False,
                hints=[
                    "Loop over `roster` again. An `if` inside the loop picks the tired ones, and the print goes "
                    "inside the `if`.",
                    "With other names:\n```python\nfor jar in jars:\n    if jar[\"left\"] < 1:\n"
                    "        print(jar[\"spice\"])\n```",
                    "Write `print(member[\"name\"])` under `if member[\"mana\"] < 10:`, and put that `if` inside a "
                    "loop over `roster`.",
                ],
                checks=[tired_check],
                pass_line=pass_tired,
            ),
        ],
        solution=solution,
        partials=[program(tired_code="")],
        assemble=dict(
            lines=[roster.strip(), "total = 0", "for member in roster:", '    total = total + member["mana"]',
                   '    if member["mana"] < 10:', '        print(member["name"])', "print(total)"],
            distractors=["    total = 0", "    print(total)", '    if roster["mana"] < 10:'],
        ),
        another_way=[
            dict(angle="picture", label="A tally jar and a gate", text=(
                "```text\ntotal = 0       empty the jar\nfor each member drop in mana\nprint(total)    "
                "read the jar\n```\nThen walk the line again: the `if` is a gate that stops only the tired ones.")),
            dict(angle="step-by-step", text=(
                f"1. `total` starts at 0, once. 2. Each pass adds one sheet's mana. 3. After the loop it holds "
                f"{own_total}: print it. 4. A second loop asks each sheet `< 10`, and prints the name when it is "
                "True.")),
            dict(angle="shorter", text="Reset above, add inside, print below. Then an `if` inside a loop."),
        ],
        takeaway="`total = 0` above the loop, `total = total + ...` inside it, `print(total)` below; an `if` inside "
        "a loop picks.",
        wrong_answers=[
            dict(why="the starter (no total)", code=starter, fails_at=1, message_contains="No variable named"),
            dict(why=f"the total typed by hand ({own_total})",
                 code=program(f"total = {own_total}\nprint(total)\n"), fails_at=1,
                 message_contains=f"stayed {own_total}"),
            dict(why="total = 0 inside the loop: it restarts every pass",
                 code=program('for member in roster:\n    total = 0\n    total = total + member["mana"]\nprint(total)\n'),
                 fails_at=1, message_contains="restarts every pass"),
            dict(why="the final print indented inside the loop: it prints every pass",
                 code=program('total = 0\nfor member in roster:\n    total = total + member["mana"]\n'
                              '    print(total)\n'), fails_at=1, message_contains="every pass"),
            dict(why="each pass replaces total (= member's mana, no +)",
                 code=program('total = 0\nfor member in roster:\n    total = member["mana"]\nprint(total)\n'),
                 fails_at=1, message_contains="each pass replaced it"),
            dict(why="a sum on a line of its own (worked out, then forgotten)",
                 code=program('total = 0\nfor member in roster:\n    total + member["mana"]\nprint(total)\n'),
                 fails_at=1, message_contains="forgotten"),
            dict(why="four typed reads, no loop (CMB passes, LOOP fails)",
                 code=program('total = (roster[0]["mana"] + roster[1]["mana"]\n'
                              '         + roster[2]["mana"] + roster[3]["mana"])\nprint(total)\n'),
                 fails_at=1, message_contains="left one out"),
            dict(why="the total worked out, but its value typed in the print",
                 code=program(TOTAL_PART.replace("print(total)", f"print({own_total})")), fails_at=1,
                 message_contains="did not follow"),
            dict(why="the total never printed", code=program(TOTAL_PART.replace("print(total)\n", "")), fails_at=1,
                 message_contains="never printed"),
            dict(why="roster[\"mana\"] for member[\"mana\"] (TypeError)",
                 code=program(TOTAL_PART.replace('member["mana"]', 'roster["mana"]')), fails_at=0,
                 message_contains="list indices must be integers"),
            dict(why="the whole sheet added (TypeError)",
                 code=program(TOTAL_PART.replace('member["mana"]', "member")), fails_at=0,
                 message_contains="unsupported operand"),
            dict(why="total = 0 left out (NameError)", code=program(TOTAL_PART.replace("total = 0\n", "")), fails_at=0,
                 message_contains="'total' is not defined"),
            dict(why="a near-miss name (Total)", code=program(TOTAL_PART.replace("total", "Total")), fails_at=1,
                 message_contains="letter for letter"),
            dict(why="the for line without its colon", code=program(TOTAL_PART.replace("in roster:", "in roster")),
                 fails_at=0, message_contains="expected ':'"),
            dict(why="no if: every name prints", code=program(tired_code='for member in roster:\n'
                                                                       '    print(member["name"])\n'),
                 fails_at=2, message_contains="Every member's name"),
            dict(why="the if outside the loop: it checks the last member once",
                 code=program(tired_code='for member in roster:\n    pass\nif member["mana"] < 10:\n'
                                         '    print(member["name"])\n'), fails_at=2, message_contains="ran once"),
            dict(why="the filter print outside the loop: one name only",
                 code=program(tired_code='for member in roster:\n    if member["mana"] < 10:\n'
                                         '        tired = member["name"]\nprint(tired)\n'), fails_at=2,
                 message_contains="Only one name"),
            dict(why="<= for <: exactly 10 is not less than 10",
                 code=program(tired_code=TIRED_PART.replace("< 10", "<= 10")), fails_at=2,
                 message_contains="exactly 10"),
            dict(why="> for <: the wrong side", code=program(tired_code=TIRED_PART.replace("< 10", "> 10")),
                 fails_at=2, message_contains="more than 10"),
            dict(why="roster[\"mana\"] in the if (TypeError)",
                 code=program(tired_code=TIRED_PART.replace('if member["mana"]', 'if roster["mana"]')), fails_at=0,
                 message_contains="list indices must be integers"),
            dict(why="the whole sheet printed", code=program(tired_code=TIRED_PART.replace('print(member["name"])',
                                                                                          "print(member)")),
                 fails_at=2, message_contains="whole sheet"),
            dict(why="the list printed, not the item (print(roster))",
                 code=program(tired_code=TIRED_PART.replace('print(member["name"])', "print(roster)")), fails_at=2,
                 message_contains="whole roster"),
            dict(why="the names typed by hand", code=program(tired_code=typed_names), fails_at=2,
                 message_contains="same names"),
            dict(why="break after the first name (break in the wrong place)",
                 code=program(tired_code=TIRED_PART + "        break\n"), fails_at=2, message_contains="Only one name"),
            dict(why="while for if: the loop never ends (prints forever)",
                 code=program(tired_code=TIRED_PART.replace("    if ", "    while ")), fails_at=0,
                 message_contains="printed more than"),
            dict(why="the sum typed from the sheets (values by hand, no loop)",
                 code=program("total = " + " + ".join(str(s["mana"]) for s in sheets) + "\nprint(total)\n"),
                 fails_at=1, message_contains="the number is typed in the code"),
            dict(why="a loop, but over the mana values typed by hand",
                 code=program("total = 0\nfor mana in [" + ", ".join(str(s["mana"]) for s in sheets) + "]:\n"
                              "    total = total + mana\nprint(total)\n"), fails_at=1,
                 message_contains="the loop walks a list typed in the code"),
            dict(why="the print above the loop: it shows 0",
                 code=program('total = 0\nprint(total)\nfor member in roster:\n    total = total + member["mana"]\n'),
                 fails_at=1, message_contains="above the loop"),
            dict(why="total = 0 again after the print (a reset for every loop): the sum is wiped",
                 code=program(TOTAL_PART + "total = 0\n"), fails_at=1, message_contains="wiped"),
            dict(why="the hint's names copied (bags is not defined)",
                 code=program('coins = 0\nfor bag in bags:\n    coins = coins + bag["left"]\nprint(coins)\n'),
                 fails_at=0, message_contains="'bags' is not defined"),
            dict(why="every name printed in the adding loop as well (CP2: extra names)",
                 code=program('total = 0\nfor member in roster:\n    total = total + member["mana"]\n'
                              '    print(member["name"], member["mana"])\nprint(total)\n'), fails_at=2,
                 message_contains="10 mana or more printed too"),
            dict(why="< 9 for < 10: a member with 9 mana is left out",
                 code=program(tired_code=TIRED_PART.replace("< 10", "< 9")), fails_at=2,
                 message_contains="with 9 mana, did not print"),
            dict(why="range(4) typed for this roster: the fifth hero is never checked (LOOP)",
                 code=program(tired_code='for i in range(4):\n    if roster[i]["mana"] < 10:\n'
                                         '        print(roster[i]["name"])\n'), fails_at=2,
                 message_contains="Ivo, with 9 mana, did not print"),
        ],
        notes=_qc_meta("accumulate,loop-with-if", foreign="coins,bag,bags,jars,jar,spice,left", form=form) + "\n"
        f"QC5 C2, form {form}: {', '.join(str(s['mana']) for s in sheets)} (total {own_total}; under 10: "
        f"{', '.join(tired)}). The roster is visible, so reruns swap its `roster = [...]` line: CMB with the same "
        f"heroes at {', '.join(str(m) for m in other_mana)} (one at exactly 10, so `<=` fails) and LOOP with 5 "
        "other heroes. CP1 [ND]: `total` follows every roster (spec: the typed total -> CMB; the reset inside the "
        "loop), and it prints once, after the loop (a `print` naming `total` inside a loop fails; a typed print "
        "fails the rerun; a print above the loop is named). CP2 [ND]: the names printed are exactly the members "
        "under 10, in order: any extra words, several names on one line, or a printed list of names (built with "
        "`.append` or 5C-03's one-line list) all pass. One loop doing both steps passes too (the assemble lines use it), "
        "and so does `+=`. Catches: the starter, typed 45/48, the reset inside, the print inside, `total = "
        "member[...]`, a bare sum, four typed reads (LOOP), a typed print, no print, `roster[...]`, the whole "
        "sheet added, no reset (NameError), a near-miss name, the colon; no `if`, the `if` outside the loop, the "
        "filter print outside it, `<=`, `>`, `roster[...]` in the `if`, the whole sheet or roster printed, typed "
        "names, a `break` after the first name, `while` for `if` (prints forever: TooMuchOutput at once). Added "
        "by the check-breaker: the sum typed from the sheets and a loop over typed mana (both 'typed in the "
        "code'), the print above the loop, `total = 0` again after the print (a reset for every loop), the hint's "
        "`bags` copied, every name printed in the adding loop too ('10 mana or more printed too'), `< 9` and "
        "`range(4)` in the filter (each names the member who did not print). Lean messages. explainer='lean'."
    )


# ---- C3: a lean `while` write task (while-loop, accumulate) ----------------------------------------------------

_STUCK_WHILE = "Stuck? Skip it, or try the lesson While the Clock Ticks. Tasks you pass here stay ticked."

# Shared by C3's two checks: the student's own run (its two start values read from the student's own starter
# lines, so a changed number is followed) or a rerun with both lines swapped, and what the watch should show.
_WATCH_RUN = r'''
def _near(_a, _b):
    return _tn(_a) in ('int', 'float') and _tn(_b) in ('int', 'float') and _B.abs(_a - _b) < 1e-6
def _number(_v):
    return _tn(_v) in ('int', 'float')
def _fnums(_l):
    return [_B.float(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?:\.\d+)?(?!\d)', _l)]
def _inorder(_rows, _seq):
    # (True, index of the row that showed the last number) when every number of _seq shows, in order.
    _at, _last = 0, -1
    for _i, _l in _B.enumerate(_rows):
        if _at < _len(_seq) and _any(_near(_x, _seq[_at]) for _x in _fnums(_l)):
            _at = _at + 1
            _last = _i
    return _at == _len(_seq), _last
def _plan(_o, _d):
    # (the value after each pass, the value before each pass, the value left at the end)
    _after, _first = [], _o
    while _number(_d) and _d > 0 and _o >= _d - 1e-9 and _len(_after) < 500:
        _o = _o - _d
        _after.append(_o)
    return _after, [_first] + _after[:-1], _o
def _start(_name):
    for _n in _parsed().body:
        if (_tn(_n) == 'Assign' and _len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id == _name and _tn(_n.value) in _LIT):
            try:
                return _ast.literal_eval(_n.value)
            except Exception:
                return None
    return None
def _gone_n(_name):
    return 'The line `' + __LINES__[_name] + "` from the starter is gone, so Mar'tu's check has nothing to swap."
def _says(_node, _name):
    return _any(_tn(_x) == 'Name' and _x.id == _name for _x in _ast.walk(_node))
def _watch_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', [], _start(__LEFT__), _start(__PER__), ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    _ev = (" (Mar'tu's check tried `" + __LEFT__ + ' = ' + _str(_vals[__LEFT__]) + '` and `' + __PER__ + ' = '
           + _str(_vals[__PER__]) + '`, only inside the check.)')
    return _ns, _rows, _err, _miss, _vals[__LEFT__], _vals[__PER__], _ev
'''

_WATCH_BODY = r'''
_t0 = _parsed()
_ins = _in_loops(_t0)
_whiles = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'While']
_fors = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'For']
_ifs = [_n for _n in _ast.walk(_t0) if _tn(_n) == 'If' and _says(_n.test, __LEFT__)]
_w_ids = _B.set()
for _w in _whiles:
    for _part in _w.body:
        for _x in _ast.walk(_part):
            _w_ids.add(_B.id(_x))
def _sets_left(_n):
    _ts = _n.targets if _tn(_n) == 'Assign' else [_n.target]
    return _any(_tn(_x) == 'Name' and _x.id == __LEFT__ for _x in _ts)
_updates = [_n for _n in _ast.walk(_t0) if _tn(_n) in ('Assign', 'AugAssign') and _B.id(_n) in _w_ids
            and _sets_left(_n)]
def _consts(_node):
    return [_x for _x in _ast.walk(_node) if _tn(_x) == 'Constant' and _tn(_x.value) in ('int', 'float')
            and _x.value != 0]
# a number typed where the daily use belongs: in the `while` line, or in the update
_typed_w = [_w for _w in _whiles if _says(_w.test, __LEFT__) and _consts(_w.test)]
_typed_u = [_u for _u in _updates if _consts(_u.value)]
_shows = _prints_of(_t0, __LEFT__)
_shows_in = [_p for _p in _shows if _B.id(_p) in _ins]
_breaks = _uses('node:Break')
_own = None
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _o0, _d, _ev = _watch_case(_vals)
    assert not _miss, _gone_n(_miss[0])
    assert _number(_o0), _gone_n(__LEFT__)
    assert _number(_d), _gone_n(__PER__)
    assert not _err, _lstop(_err, _ev)
    _after, _before, _end = _plan(_o0, _d)
    _got = _ns.get(__LEFT__)
    if _vals is None:
        _own = _got
    if _near(_got, _end):
        if _inorder(_rows, _after)[0] or _inorder(_rows, _before)[0]:
            continue
        assert _shows, '`' + __LEFT__ + '` was never printed.'
        assert _shows_in, '`' + __LEFT__ + '` printed once, after the loop, not on every pass.'
        assert False, 'The printed ' + __STUFF__ + ' did not follow the numbers.' + _ev
    _gs = _shv(_got)
    assert _whiles or _fors or not _ifs, (
        'There is no loop: an `if` asks once, so `' + __LEFT__ + '` went down only once.')
    assert not _near(_got, _o0), '`' + __LEFT__ + '` never changed: it is still ' + _gs + '.' + _ev
    assert _whiles, '`' + __LEFT__ + '` ended at ' + _gs + ', and there is no `while` loop.' + _ev
    assert not (_breaks and _near(_got, _o0 - _d)), 'The loop stopped after one pass, at a `break`.' + _ev
    assert not (_vals is not None and _typed_w), (
        '`' + __LEFT__ + '` ended at ' + _gs + ': the `while` line compares with a number typed in the code.' + _ev)
    assert not (_vals is not None and _typed_u), (
        '`' + __LEFT__ + '` ended at ' + _gs + ': each pass takes off a number typed in the code.' + _ev)
    assert not _near(_got, _d), 'The loop stopped with exactly `' + __PER__ + '` still left, one pass short.' + _ev
    assert not _near(_got, _end - _d), (
        'The loop ran one pass too many: `' + __LEFT__ + '` ended at ' + _gs + '.' + _ev)
    assert not (_vals is not None and _near(_got, _own)), (
        'With other numbers, `' + __LEFT__ + '` still ended at ' + _gs + '.' + _ev)
    assert False, ('`' + __LEFT__ + '` ended at ' + _gs + ', not what is left after the last full ' + __NOUN__
                   + '.' + _ev)
assert _whiles, 'This task checks the `while` skill, and there is no `while` loop.'
'''

_COUNT_BODY = r'''
_t0 = _parsed()
_ins = _in_loops(_t0)
_reset = [_z for _z in _zeros(_t0, __COUNT__) if _B.id(_z) in _ins]
_cprints = _prints_of(_t0, __COUNT__)
# a print of the count alone inside the loop (a print that also shows the watch value is a fine watch line)
_in_print = [_p for _p in _cprints if _B.id(_p) in _ins and not _says(_p, __LEFT__)]
_loops = [_n for _n in _t0.body if _tn(_n) in ('For', 'While')]
_early = [_p for _p in _cprints if _B.id(_p) not in _ins and _loops and _p.lineno < _loops[0].lineno]
def _bumps(_n):
    if _tn(_n) == 'AugAssign':
        return _tn(_n.target) == 'Name' and _n.target.id == __COUNT__
    return (_tn(_n) == 'Assign' and _tn(_n.value) != 'Constant'
            and _any(_tn(_x) == 'Name' and _x.id == __COUNT__ for _x in _n.targets))
_counts = [_n for _n in _ast.walk(_t0) if _bumps(_n)]
_counted_in = [_n for _n in _counts if _B.id(_n) in _ins]
_own = None
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _o0, _d, _ev = _watch_case(_vals)
    assert not _miss, _gone_n(_miss[0])
    assert _number(_o0), _gone_n(__LEFT__)
    assert _number(_d), _gone_n(__PER__)
    assert not _err, _lstop(_err, _ev)
    _after, _before, _end = _plan(_o0, _d)
    _n = _len(_after)
    assert __COUNT__ in _ns, _lost(__COUNT__, (__LEFT__, __PER__))
    _got = _ns[__COUNT__]
    if _vals is None:
        _own = _got
    if not _near(_got, _n):
        assert not (_reset and _near(_got, 1)), '`' + __COUNT__ + '` restarts every pass, so it ended as 1.' + _ev
        assert not _near(_got, 0), '`' + __COUNT__ + '` is still 0: nothing was added to it.' + _ev
        assert not (_near(_got, 1) and _counts and not _counted_in), (
            '`' + __COUNT__ + '` was added to once, outside the loop, so it ended as 1.' + _ev)
        assert not (_vals is not None and _near(_got, _own)), (
            '`' + __COUNT__ + '` stayed ' + _shv(_own) + ' with other numbers' + _typed(_t0, __COUNT__) + _ev)
        assert False, ('`' + __COUNT__ + '` ended as ' + _shv(_got) + ', but ' + __LASTS__ + ' ' + _str(_n) + ' '
                       + __NOUN__ + ('s.' if _n != 1 else '.') + _ev)
    assert not _in_print, '`' + __COUNT__ + '` printed on every pass, not once after the loop.'
    _ok_a, _la = _inorder(_rows, _after)
    _ok_b, _lb = _inorder(_rows, _before)
    _last = _B.max(_la if _ok_a else -1, _lb if _ok_b else -1)
    if _any(_near(_x, _n) for _l in _rows[_last + 1:] for _x in _fnums(_l)):
        continue
    assert not _early, '`' + __COUNT__ + '` printed above the loop, before anything was counted.'
    assert _cprints or _vals is not None, '`' + __COUNT__ + '` was never printed.'
    assert False, 'The printed count did not follow the numbers.' + _ev
'''


def _picture(start, per, count):
    """The watch as a table (36 characters a line): the first two passes, the last one, and the stop."""
    rows, o = [], start
    while o >= per:
        rows.append((o, o - per, len(rows) + 1))
        o -= per
    shown = rows[:2] + (["..."] if len(rows) > 3 else []) + rows[2:][-1:]
    out = [f"{'before':<8}{'ask':<9}{'after':<7}{count}"]
    for r in shown:
        out.append(r if r == "..." else f"{r[0]:<8}{f'{r[0]} >= {per}':<9}{r[1]:<7}{r[2]}")
    out.append(f"{o:<8}{f'{o} >= {per}?':<9}False: stop")
    return "```text\n" + "\n".join(out) + "\n```"


def _qc_watch(form, xid, title, head, steps, left, per, count, reruns, noun, lasts, stuff, lead,
              pass_line):
    """A lean `while` write task: while `left` is at least `per`, take `per` off `left` and print it; count each
    pass in `count` and print it once, after the loop. head: the starter's story with its two lines,
    `left = <n>` and `per = <n>`; steps: the starter's step comments (36 characters a line). reruns: two
    {left: n, per: n} dicts, the first landing exactly on a multiple (so `>` for `>=` stops one pass early),
    both with counts other than the real run's (so a typed count fails). noun: "day" / "night"; lasts: "the ore
    lasts"; stuff: what the watch prints ("ore" / "mana")."""
    start = {}
    for row in head.splitlines():
        if row.startswith((left + " = ", per + " = ")):
            name, value = row.split(" = ")
            start[name] = int(value)
    o0, d0 = start[left], start[per]
    after, o = [], o0
    while o >= d0:
        o -= d0
        after.append(o)
    passes, end = len(after), o
    for case in reruns:
        assert len(case) == 2 and case[left] // case[per] != passes, "a rerun's count must differ from the real run"
    assert reruns[0][left] % reruns[0][per] == 0, "the first rerun lands exactly on a multiple"

    def program(reset=f"{count} = 0\n", test=f"while {left} >= {per}:\n", inside="",
                update=f"    {left} = {left} - {per}\n", show=f"    print({left})\n",
                bump=f"    {count} = {count} + 1\n", tail=f"print({count})\n", top=None):
        return (head if top is None else top) + steps + reset + test + inside + update + show + bump + tail

    starter = head + steps
    solution = program()
    subs = dict(LINES={left: f"{left} = {o0}", per: f"{per} = {d0}"}, LEFT=left, PER=per, CASES=[None] + reruns,
                COUNT=count, NOUN=noun, LASTS=lasts, STUFF=stuff)
    watch = chk(f"each pass takes {per} off {left} and prints it, and follows other numbers",
                _WATCH_RUN + _WATCH_BODY, **subs)
    tally = chk(f"{count} counts the passes and prints once, after the loop", _WATCH_RUN + _COUNT_BODY, **subs)
    near = count[:-1]
    ev = [f"`{left} = {r[left]}` and `{per} = {r[per]}`" for r in reruns]
    return dict(
        id=xid,
        title=title,
        martu=lead + "\n" + _STUCK_WHILE,
        names=[left, per, count],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id=f"count-the-{noun}s",
                text=(f"While `{left}` is at least `{per}`, take `{per}` off `{left}` and print `{left}`. Count "
                      f"each pass in `{count}`, and print `{count}` once, after the loop."),
                dictated=False,
                hints=[
                    f"Two numbers are ready: `{left}` and `{per}`. A `while` loop asks its question before every "
                    "pass. The count starts once, above the loop, and its print goes below it.",
                    "With other names:\n```python\nweeks = 0\nwhile sacks >= 2:\n    sacks = sacks - 2\n"
                    "    print(sacks)\n    weeks = weeks + 1\nprint(weeks)\n```\nEach pass takes 2 sacks off "
                    "and counts one week.",
                    f"Write `{count} = 0` above `while {left} >= {per}:`. Inside it, take `{per}` off `{left}`, "
                    f"print `{left}` and add 1 to `{count}`. Then `print({count})` below it, with no spaces in "
                    "front.",
                ],
                checks=[watch, tally],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[head.strip(), f"{count} = 0", f"while {left} >= {per}:", f"    {left} = {left} - {per}",
                   f"    print({left})", f"    {count} = {count} + 1", f"print({count})"],
            distractors=[f"    {count} = 0", f"    print({count})", f"if {left} >= {per}:"],
        ),
        another_way=[
            dict(angle="picture", label="The watch, pass by pass", text=(
                _picture(o0, d0, count) + f"\nThen `print({count})` runs once, below the loop.")),
            dict(angle="step-by-step", text=(
                f"1. `{count} = 0`, once, above the loop.\n"
                f"2. `while {left} >= {per}:` asks before every pass.\n"
                f"3. Inside: take `{per}` off, print `{left}`, add 1 to `{count}`.\n"
                f"4. When less than `{per}` is left, the answer is `False`: the loop ends, and the count prints "
                "once.")),
            dict(angle="from the campaign", text=(
                "Holding the barrier, every cast took mana off: "
                "`caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]`. A `while` loop runs a line like that "
                "again and again, until too little is left.")),
            dict(angle="shorter", text="Count above. Ask with `while`. Take off, print and count inside. Print the "
                 "count below."),
        ],
        takeaway=(f"`while {left} >= {per}:` asks before every pass; the update inside moves it toward `False`, "
                  "and the count starts above the loop."),
        wrong_answers=[
            dict(why="the starter (two numbers, no loop yet)", code=starter, fails_at=1,
                 message_contains="never changed"),
            dict(why="no update: the loop never ends (prints forever)", code=program(update=""), fails_at=0,
                 message_contains="printed more than"),
            dict(why="the update outside the loop: it never ends (prints forever)",
                 code=program(update="", tail=f"{left} = {left} - {per}\nprint({count})\n"), fails_at=0,
                 message_contains="printed more than"),
            dict(why="the update the wrong way (+): it never ends (prints forever)",
                 code=program(update=f"    {left} = {left} + {per}\n"), fails_at=0,
                 message_contains="printed more than"),
            dict(why="if for while: it asks once", code=program(test=f"if {left} >= {per}:\n"), fails_at=1,
                 message_contains="an `if` asks once"),
            dict(why="> for >=: the first rerun lands exactly on a multiple, so the loop stops one pass early",
                 code=program(test=f"while {left} > {per}:\n"), fails_at=1, message_contains="one pass short"),
            dict(why=f"> 0 for >= {per}: one pass too many, below 0", code=program(test=f"while {left} > 0:\n"),
                 fails_at=1, message_contains="one pass too many"),
            dict(why=f"{count} = 0 inside the loop (the reset slip): it restarts every pass",
                 code=program(reset="", inside=f"    {count} = 0\n"), fails_at=1,
                 message_contains="restarts every pass"),
            dict(why=f"a second {count} = 0 inside the loop, the one above kept",
                 code=program(inside=f"    {count} = 0\n"), fails_at=1, message_contains="restarts every pass"),
            dict(why=f"print({count}) inside the loop: it prints every pass",
                 code=program(bump=f"    {count} = {count} + 1\n    print({count})\n", tail=""), fails_at=1,
                 message_contains="printed on every pass"),
            dict(why=f"{count} = {count} + 1 below the loop: it counts once",
                 code=program(bump="", tail=f"{count} = {count} + 1\nprint({count})\n"), fails_at=1,
                 message_contains="outside the loop"),
            dict(why=f"the count typed by hand ({passes})",
                 code=program(reset="", bump="", tail=f"{count} = {passes}\nprint({count})\n"), fails_at=1,
                 message_contains="the number is typed in the code"),
            dict(why="the count worked out, but its value typed in the print",
                 code=program(tail=f"print({passes})\n"), fails_at=1, message_contains="did not follow"),
            dict(why=f"{per}'s value, {d0}, typed in the while line",
                 code=program(test=f"while {left} >= {d0}:\n"), fails_at=1,
                 message_contains="`while` line compares with a number typed"),
            dict(why=f"{per}'s value, {d0}, typed in the update",
                 code=program(update=f"    {left} = {left} - {d0}\n"), fails_at=1,
                 message_contains="takes off a number typed"),
            dict(why=f"the line {per} = {d0} deleted, its value typed instead",
                 code=program(top=head.replace(f"{per} = {d0}\n", ""), test=f"while {left} >= {d0}:\n",
                              update=f"    {left} = {left} - {d0}\n"), fails_at=1, message_contains="is gone"),
            dict(why=f"the stop typed for this run (while {left} != {end}): with other numbers it never stops",
                 code=program(test=f"while {left} != {end}:\n"), fails_at=1, message_contains="never stopped"),
            dict(why=f"the stop typed as this run's end (while {left} > {end}): a rerun goes one pass too far",
                 code=program(test=f"while {left} > {end}:\n"), fails_at=1,
                 message_contains="`while` line compares with a number typed"),
            dict(why="the watch printed once, below the loop (a print outside the loop)",
                 code=program(show="", tail=f"print({left})\nprint({count})\n"), fails_at=1,
                 message_contains="not on every pass"),
            dict(why=f"{left} never printed", code=program(show=""), fails_at=1,
                 message_contains=f"`{left}` was never printed"),
            dict(why=f"{count} never printed", code=program(tail=""), fails_at=1,
                 message_contains=f"`{count}` was never printed"),
            dict(why=f"print({count}) above the loop: it shows 0",
                 code=program(reset=f"{count} = 0\nprint({count})\n", tail=""), fails_at=1,
                 message_contains="above the loop"),
            dict(why="break after one pass (break in the wrong place)",
                 code=program(bump=f"    {count} = {count} + 1\n    break\n"), fails_at=1,
                 message_contains="at a `break`"),
            dict(why=f"{count} = 0 left out (NameError)", code=program(reset=""), fails_at=0,
                 message_contains=f"'{count}' is not defined"),
            dict(why=f"a near-miss name ({near})",
                 code=program(reset=f"{near} = 0\n", bump=f"    {near} = {near} + 1\n", tail=f"print({near})\n"),
                 fails_at=1, message_contains="letter for letter"),
            dict(why="the hint's names copied (sacks is not defined)",
                 code=starter + "weeks = 0\nwhile sacks >= 2:\n    sacks = sacks - 2\n    print(sacks)\n"
                 "    weeks = weeks + 1\nprint(weeks)\n", fails_at=0, message_contains="'sacks' is not defined"),
            dict(why=f"a for loop over a typed range({passes}), no while: the reruns go wrong",
                 code=program(test=f"for i in range({passes}):\n"), fails_at=1,
                 message_contains="no `while` loop"),
            dict(why="a for loop over a worked-out count: right numbers, but no while",
                 code=program(test=f"for i in range({left} // {per}):\n"), fails_at=1,
                 message_contains="no `while` loop"),
        ],
        notes=_qc_meta("while-loop,accumulate", foreign="sacks,weeks", form=form) + "\n"
        f"QC5 C3, form {form} (teacher ruling on the Unit 6 reviews: a lean `while` write task replaces the "
        f"spec's mend-the-tally, the third repeat of the reset slip). The starter holds `{left} = {o0}` and "
        f"`{per} = {d0}` with step comments; the student's own run prints {', '.join(str(v) for v in after)}, then "
        f"{passes}. CP1 [ND], two checks on the own run and two reruns that swap both starter lines "
        f"({' and '.join(ev)}: {reruns[0][left] // reruns[0][per]} and {reruns[1][left] // reruns[1][per]} "
        f"{noun}s, both other than {passes}; the first lands exactly on a multiple, so `>` for `>=` stops one "
        f"pass early). WATCH: `{left}` ends where it should and every value of the watch prints, in order (the "
        "print before the update passes too, and so does any text around the number). COUNT: "
        f"`{count}` ends as the number of passes and prints once, after the loop (a print that also shows "
        f"`{left}` inside the loop is a fine watch line). The own run's start values are read from the student's "
        "own starter lines, so a changed number is followed. `-=` / `+=` pass, and so does `while True:` with a "
        "`break` at the right place; a `for` loop with a worked-out count gets the right numbers but fails "
        "('this task checks the `while` skill'). Catches (each proven): the starter; no update, the update outside "
        "the loop and the update the wrong way (all three print forever: TooMuchOutput at once, fails_at 0); `if` "
        f"for `while`; `>` for `>=`; `> 0` (one pass too many); `{count} = 0` inside the loop (the reset slip, "
        f"kept as evidence), with or without one above; `print({count})` inside the loop; `{count} = {count} + 1` "
        "below the loop; a typed count; a typed print; the daily value typed in the `while` line or the update; "
        f"the `{per}` line deleted; the stop typed for this run (`!= {end}`: a rerun never stops, and the check's "
        f"guard says so; `> {end}`: a rerun goes one pass too far); the watch print below the loop; nothing printed; the count printed above the loop; a `break` "
        f"after one pass; no `{count} = 0` (NameError); a near-miss name; the hint's `sacks` copied; a `for` over "
        "a typed range; a `for` over a worked-out count. Lean messages, with the evidence bracket. "
        "support='none', explainer='lean'."
    )


# ---- the two forms -----------------------------------------------------------------------------------------

# C3's starters (36 characters a line). Form A is Bomb Shell's real Velocite numbers (30 chunks, 4 a day: about
# a week, 7 days, as in the project); form B is the barrier around the cabin (30 mana, 7 a night: 4 nights).
ORE_HEAD = (
    "# Bomb Shell's Velocite ore.\n"
    "# Chunks he has left:\n"
    "ore_left = 30\n"
    "# Chunks he burns each day:\n"
    "daily = 4\n"
)
ORE_STEPS = (
    "# 1. While ore_left is at least\n"
    "#    daily, take daily off ore_left\n"
    "#    and print ore_left.\n"
    "# 2. Count each pass in days. Print\n"
    "#    days once, after the loop.\n"
)
BARRIER_HEAD = (
    "# Mar'tu's barrier.\n"
    "# Mana stored in it:\n"
    "mana_left = 30\n"
    "# Mana it costs each night:\n"
    "cost = 7\n"
)
BARRIER_STEPS = (
    "# 1. While mana_left is at least\n"
    "#    cost, take cost off mana_left\n"
    "#    and print mana_left.\n"
    "# 2. Count each pass in nights.\n"
    "#    Print nights once, after the\n"
    "#    loop.\n"
)
# The reruns: the first lands exactly on a multiple (24 / 6, 18 / 6), so `>` for `>=` stops one pass early; the
# second (19 / 5, 27 / 4) ends between 2 and the daily use, so `> 2` and a typed daily use go one pass too far.
# Every count (4 and 3 days; 3 and 6 nights) differs from the real run's (7 days; 4 nights).
ORE_RERUNS = [{"ore_left": 24, "daily": 6}, {"ore_left": 19, "daily": 5}]
BARRIER_RERUNS = [{"mana_left": 18, "cost": 6}, {"mana_left": 27, "cost": 4}]

_QC_SUMMARY = (
    "Three short tasks and four questions, no hints. Pass all three tasks and get 3 of the 4 questions right to "
    "test out of Unit 6. Stuck on one? The lessons teach all of it, and tasks you pass here stay ticked."
)
_STRETCH = "That is Unit 6, yes? Want a stretch? Try Gearshift's Forecast."
# The last pass line is the story recap a student who tests out would otherwise miss (teacher ruling).
_RECAP = (
    "Mar'tu's notes: the shrinks go 0, 1, 1, 2, 3, 4, so the decay is speeding up. My forecast says 32 hours to "
    "the next burst. "
)

QC5_A = dict(
    kind="testout",
    id="qc5-a",
    title="Quick Check 6 · Form A",
    optional=True,
    minutes=14,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_each(
            "A", "light_lantern", "name", "_lanterns", LANTERN_SETUP, LANTERN_STARTER, "lantern", "lit", "name",
            "names", "a name", "Every lantern went to the same hero.",
            "Night is coming. One lantern by each hero's bed, yes? `light_lantern(...)` lights one lantern: hand "
            "it one hero's name. ",
            "Mar'tu: Four lanterns, four heroes. You wrote the call once, and Python walked the line.",
        ),
        _qc_tally(
            "A", "# After a night holding the barrier:\n", NIGHT, [12, 9, 10, 2],
            "After a night holding the barrier, everyone is low. Add up what the party has left, then tell me who "
            "needs rest. ",
            "Gearshift: 45. That matches my count.",
            "Mar'tu: Two to bed. The rest keep watch.",
        ),
        _qc_watch(
            "A", "the-ore-watch", "The ore watch", ORE_HEAD, ORE_STEPS, "ore_left", "daily", "days", ORE_RERUNS,
            "day", "the ore lasts", "ore",
            "Bomb Shell runs on Velocite ore. He has 30 chunks left, and he burns 4 a day. How many days is that? "
            "Keep watch with a `while` loop, yes? My check also tries other numbers, only inside the check, so let "
            "the loop do the work.",
            _RECAP + "Bomb Shell has about 7 days of ore. You lit the lanterns, kept the tally and ran the watch. "
            + _STRETCH,
        ),
    ],
    notes=(
        "Quick Check 5, form A (code tasks C1, C2, C3; the spec's Q1 and Q2 live in qc5-a-questions, with two "
        "added questions). Pass = every code task plus 3 of the 4 questions (questions_to_pass=3, as Unit 2's "
        "QC2); a retake draws form B. Coverage (lint d): for-each -> C1 (WA four typed calls, `range(4)`, the "
        "colon, the indent, a call that runs once, `for i in 4`); list-of-dicts -> C1 (WA the whole sheet, "
        "`roster[\"name\"]`, `roster[member]`, the other key, `light_lantern(name)`) and C2 CP2 (WA "
        "`roster[\"mana\"]`, the whole sheet printed); accumulate -> C2 CP1 (WA typed 45, the reset inside, the "
        "print inside, four typed reads) and C3 (WA `days = 0` inside the loop, `print(days)` inside, "
        "`days = days + 1` below the loop, a typed count, a typed print): the reset slip is proven by C2 CP1 and "
        "C3's `days = 0` inside the loop; loop-with-if -> C2 CP2 (WA no `if`, the `if` outside, `<=`, the "
        "filter print outside, `break` after one, `while` for `if`); while-loop -> C3 in code (teacher ruling: a "
        "lean `while` write task with Bomb Shell's real numbers, 30 ore at 4 a day, 7 days; WA no update, the "
        "update outside the loop, the update the wrong way, all three printing forever; `if` for `while`, `>` "
        "for `>=`, `> 0`, the daily use typed, the stop typed for this run, `break` after one pass), plus Q1 (off "
        "by one at the stop) and Q4 (the update outside the loop); C1 also catches a `while` over positions with "
        "no update; break -> Q2 (prints every match, stops before the print); range-len, neighbors -> Q3, in the "
        "`[i - 1]` form the lessons practiced (`range(1, len(wall))`; WA choices: the full range reads `wall[-1]` "
        "on the first pass, a number for a range, one past the end). Every message is lean (Unit 2 ruling): the "
        "slip and the evidence bracket, never the line to type. support='none' everywhere: no hints, tracer or "
        "compare; glossary, read-aloud and the lean explainer stay on. The last pass line (C3) is the story recap "
        "a student who tests out would otherwise miss: the shrinks, the 32-hour forecast, the ore. 14 minutes "
        "(spec ~12; teacher ruling on the Unit 6 reviews: +2 for the `while` write task)."
    ),
)

QC5_B = dict(
    kind="testout",
    id="qc5-b",
    title="Quick Check 6 · Form B",
    optional=True,
    minutes=14,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_each(
            "B", "draw_bar", "mana", "_bars", BAR_SETUP, BAR_STARTER, "bar", "drawn", "mana", "mana values",
            "a number",
            "Every bar is the same.",
            "Four heroes, four bars to draw. `draw_bar(...)` draws one bar: hand it one hero's mana. ",
            "Mar'tu: Four bars, one line of yours. The mana bars at the bottom of the campaign did the same.",
        ),
        _qc_tally(
            "B", "# After one Strengthen Magic each:\n", STRONG, [3, 15, 10, 7],
            "Each of you cast Strengthen Magic once, at 10 mana a cast. Add up what the party has left, then tell "
            "me who needs rest. ",
            "Gearshift: 48. That matches my count.",
            "Mar'tu: Only Oogrish. Exactly 10 is not less than 10, so Gearshift keeps watch.",
        ),
        _qc_watch(
            "B", "the-barrier-watch", "The barrier watch", BARRIER_HEAD, BARRIER_STEPS, "mana_left", "cost",
            "nights", BARRIER_RERUNS, "night", "the mana lasts", "mana",
            "My barrier has 30 mana stored, and holding it costs 7 a night. How many nights is that? Keep watch "
            "with a `while` loop, yes? My check also tries other numbers, only inside the check, so let the loop "
            "do the work.",
            _RECAP + "My barrier has 4 nights of mana. You drew the bars, kept the tally and ran the watch. "
            + _STRETCH,
        ),
    ],
    notes=(
        "Quick Check 5, form B: `draw_bar(member[\"mana\"])` (C1), the party after one Strengthen Magic each at 10 "
        "mana a cast (C2: 8, 10, 14, 16, total 48; only Oogrish is under 10, and Gearshift's exactly-10 catches "
        "`<=` on the student's own run), and the barrier watch (C3: `mana_left = 30`, `cost = 7` a night; the watch "
        "prints 23, 16, 9, 2, then 4 `nights`; reruns 18 / 6, exactly 3 nights, and 27 / 4, 6 nights). Same "
        "coverage, rules and minutes as form A (14). Questions live in qc5-b-questions. Pass = every code task "
        "plus 3 of the 4 questions (questions_to_pass=3)."
    ),
)


# Lean, proved (as Unit 2's _leaned asserts its rewrites and Units 4-5's _lean_guard their forms): no check names the
# fix.
_FIX_WORDS = {"Put", "Make", "Add", "Use", "Copy", "Read", "Store", "Take", "Print", "Change", "Replace", "Spend",
              "Fill", "Check", "Write", "Ask", "Indent", "Give", "Build", "Warn", "Swap", "Compare", "Set", "Spell",
              "Move", "Delete", "Remove", "Type", "Try", "Mend", "Keep", "Count", "Hand", "Loop", "Walk", "Call",
              "Start", "Stop", "Break", "Glue", "Unindent", "Indent"}


def _lean_guard(form):
    """Quick Check messages are lean (Unit 2 ruling): the slip and the evidence, never the fix. Proved at import, two
    ways, as u05c does. (1) No check of a form's tasks holds a line of Mar'tu's version that the starter does not
    show, or that line's working part (the read, the call, the `while` question, the update). (2) No text in a check
    opens a sentence with a fix ("Put ...", "Make sure the loop can end ...", "Keep the line ..."): every text that
    opens a sentence is the slip or the evidence."""
    import ast as _ast_guard
    squash = lambda text: "".join(text.split())  # noqa: E731
    for ex in form["exercises"]:
        shown = {squash(line) for line in ex["starter"].split("\n")}
        pieces = set()
        for line in ex["solution"].split("\n"):
            code = squash(line.split("  #")[0])
            if not code or code.startswith("#") or code in shown:
                continue
            pieces.add(code)
            right = code.split("=", 1)[1] if "=" in code and "==" not in code else code
            for head in ("print(", "if", "elif", "while", "for"):
                if right.startswith(head):
                    right = right[len(head):].rstrip(":)")
            if right.strip("[]0123456789,-+") and len(right) >= 6:
                pieces.add(right)
        for cp in ex["checkpoints"]:
            for name, check_code in cp["checks"]:
                for node in _ast_guard.walk(_ast_guard.parse(check_code)):
                    if isinstance(node, _ast_guard.Constant) and isinstance(node.value, str):
                        # Text a student reads (it has `code` marks or ends a sentence) never shows a line of the fix.
                        shown_text = "`" in node.value or node.value.rstrip().endswith(".")
                        named = [piece for piece in pieces if shown_text and len(piece) >= 6 and piece in squash(node.value)]
                        assert not named, f"{form['id']}/{ex['id']}: the check {name!r} shows the fix {named[0]!r}"
                        words = node.value.strip().split(" ")
                        first = words[0] if len(words) > 1 else ""
                        assert first not in _FIX_WORDS, (f"{form['id']}/{ex['id']}: the check {name!r} opens a message "
                                                         f"with the fix: {node.value[:60]!r}")
    return form


_lean_guard(QC5_A)
_lean_guard(QC5_B)


# ---- the question forms ------------------------------------------------------------------------------------

def _qc_questions(form, countdown, first, early, never):
    """countdown / first = (code, answer, choices, explain, notes); early / never = (q, code, choices, answer,
    why_wrong, explain, notes)."""
    def predict(qid, parts):
        code, answer, choices, explain, notes = parts
        return dict(type="predict", id=qid, q="What will this print?", code=code, answer=answer, choices=choices,
                    explain=explain, notes=notes)

    def mc(qid, parts):
        q, code, choices, answer, why_wrong, explain, notes = parts
        return dict(type="mc", id=qid, q=q, code=code, choices=choices, answer=answer, why_wrong=why_wrong,
                    explain=explain, notes=notes)

    return dict(
        kind="quiz",
        id=f"qc5-{form.lower()}-questions",
        title=f"Quick Check 6 · Form {form} questions",
        optional=True,
        minutes=4,
        summary="Four questions that go with Quick Check 6. To pass the Quick Check, get 3 of the 4 right.",
        questions=[
            predict("countdown", countdown),
            predict("break-at-the-first", first),
            mc("stop-one-early", early),
            mc("the-loop-that-never-ends", never),
        ],
        notes=(
            f"Quick Check 5, form {form} questions (scored with qc5-{form.lower()}: every code task plus 3 of the 4 "
            "questions, questions_to_pass=3 on the form). Q1 and Q2 are the spec's; Q3 (objective 5, neighbors in "
            "the `[i - 1]` form students practiced, `range(1, len(...))`, teacher ruling on the Unit 6 reviews: "
            "not an untaught look-ahead) and Q4 (objective 6, recognize a loop that never ends) are added so the "
            "form has Unit 2's 3-of-4 shape and every objective has evidence. `while` is also proven in code by "
            "the form's C3, and `break` by Q2 (and written in 5B-03). The best score counts, so a retake can "
            "lift it. No hints; read-aloud and glossary stay on. The site shuffles the choices; the right one is "
            "also authored in a different place in each question."
        ),
    )


QC5_A_QUESTIONS = _qc_questions(
    "A",
    (
        'hours_left = 5\nwhile hours_left > 2:\n    print(hours_left)\n    hours_left = hours_left - 1\n'
        'print("Burst!")\n',
        "5\n4\n3\nBurst!",
        ["5\n4\n3\n2\nBurst!", "5\n4\n3\nBurst!", "4\n3\n2\nBurst!", "5\n4\n3\n2\n1\nBurst!"],
        (
            "The question is asked before every pass. 5, 4 and 3 are more than 2, so they print. At 2, "
            "`hours_left > 2` is `False`, so 2 never prints. Then `Burst!` runs once, below the loop."
        ),
        "Skill while-loop (spec Q1, off-by-one). Distractors: the stop included (2), the update read as running "
        "before the print (4 3 2), and the loop read as running down to 1. The right one is authored second.",
    ),
    (
        'for mana in [22, 6, 14, 3]:\n    if mana < 10:\n        print(mana)\n        break\nprint("Rest now.")\n',
        "6\nRest now.",
        ["6\n3\nRest now.", "Rest now.", "6\nRest now.", "22\n6\nRest now.", "3\nRest now."],
        (
            "6 is the first mana under 10: it prints, then `break` leaves the loop at once. 14 and 3 are never "
            "looked at. `Rest now.` is below the loop, so it runs."
        ),
        "Skill break (spec Q2). Distractors: every match prints (no break), the break read as running before the "
        "print, every item up to the match, and the last match. The right one is authored third.",
    ),
    (
        "This loop should print how much each gap shrank. Which goes in the blank, so `wall[i - 1]` is always a "
        "gap on the wall?",
        "wall = [48, 47, 44, 37]\nfor i in ___:\n    print(wall[i - 1] - wall[i])\n",
        ["range(len(wall))", "len(wall)", "range(1, len(wall) + 1)", "range(1, len(wall))"],
        3,
        {
            0: "On the first pass `i` is 0, so `wall[i - 1]` is `wall[-1]`, the last gap: the first shrink comes "
               "out 37 - 48, which is -11.",
            1: "`len(wall)` is one number, 4. A loop can't walk through a number: TypeError: 'int' object is not "
               "iterable.",
            2: "The last `i` is 4, and `wall[4]` is past the end of the wall: IndexError.",
        },
        (
            "`range(1, len(wall))` gives 1, 2 and 3, so `i - 1` is always on the wall. The shrinks are 1, 3 and "
            "7: the decay is speeding up."
        ),
        "Added (objective 5, range-len and neighbors), in the `[i - 1]` form the lessons and the cheatsheet "
        "practiced (teacher ruling on the Unit 6 reviews: not an untaught look-ahead). Distractors: the full "
        "range (no error: `wall[-1]` on the first pass gives a quiet wrong shrink, -11), the number with no range "
        "('int' object is not iterable), and the range one past the end (IndexError). The right one is authored "
        "last.",
    ),
    (
        "Lucky wants 3 sips, then the empty canteen. What happens when this runs?",
        'glug = 3\nwhile glug > 0:\n    print("Sip.")\nglug = glug - 1\nprint("Empty.")\n',
        [
            "`Sip.` forever, until the site stops it",
            "`Sip.` 3 times, then `Empty.`",
            "`Sip.` once, then `Empty.`",
            "Nothing: Python stops with an error before it starts",
        ],
        0,
        {
            1: "The line `glug = glug - 1` has no spaces in front, so it is not in the loop. Inside the loop, "
               "`glug` stays 3.",
            2: "A `while` loop asks again after every pass. `glug` never changes inside it, so the answer stays "
               "`True`.",
            3: "Every line is good Python, so it starts. The trouble is that it never stops.",
        },
        (
            "`glug = glug - 1` sits below the loop, so it would run only after the loop ends, and the loop never "
            "ends. `glug > 0` stays `True`. The site stops it once it has printed 200,000 characters."
        ),
        "Added (objective 6, recognize a loop that never ends): the update outside the loop, the class's 5B-02 "
        "slip. Distractors: the loop read as if the update were inside, read as an `if`, and read as an error. "
        "Not run by the harness (mc). The right one is authored first.",
    ),
)

QC5_B_QUESTIONS = _qc_questions(
    "B",
    (
        'ore_left = 12\nwhile ore_left > 4:\n    print(ore_left)\n    ore_left = ore_left - 4\n'
        'print("Low on ore.")\n',
        "12\n8\nLow on ore.",
        ["12\n8\n4\nLow on ore.", "8\n4\nLow on ore.", "12\n8\nLow on ore.", "12\nLow on ore."],
        (
            "12 is more than 4, so 12 prints and 4 comes off. 8 is more than 4, so 8 prints. At 4, `ore_left > 4` "
            "is `False`: exactly 4 is not more than 4. The loop ends, and `Low on ore.` runs once."
        ),
        "Form B of countdown (Bomb Shell's Velocite watch). Distractors: the stop included (4), the update read as "
        "running before the print, one pass only. The right one is authored third.",
    ),
    (
        'for day in [3, 4, 6, 5, 7]:\n    if day > 4:\n        print(day)\n        break\nprint("Too fast.")\n',
        "6\nToo fast.",
        ["6\n5\n7\nToo fast.", "6\nToo fast.", "7\nToo fast.", "Too fast.", "3\n4\n6\nToo fast."],
        (
            "6 is the first day over 4: it prints, then `break` leaves the loop at once. 5 and 7 are never looked "
            "at. `Too fast.` is below the loop, so it runs."
        ),
        "Form B of break-at-the-first (Lucky's side-quest idea: the first day over 4). Distractors as form A. The "
        "right one is authored second.",
    ),
    (
        "This loop should print how much more ore each day used. Which goes in the blank, so `ore[i - 1]` is "
        "always a day in the list?",
        "ore = [2, 3, 5, 8]\nfor i in ___:\n    print(ore[i] - ore[i - 1])\n",
        ["range(1, len(ore))", "range(len(ore))", "len(ore)", "range(1, len(ore) + 1)"],
        0,
        {
            1: "On the first pass `i` is 0, so `ore[i - 1]` is `ore[-1]`, the last day: the first rise comes out "
               "2 - 8, which is -6.",
            2: "`len(ore)` is one number, 4. A loop can't walk through a number: TypeError: 'int' object is not "
               "iterable.",
            3: "The last `i` is 4, and `ore[4]` is past the end of the list: IndexError.",
        },
        (
            "`range(1, len(ore))` gives 1, 2 and 3, so `i - 1` is always in the list. The rises are 1, 2 and 3: "
            "Bomb Shell burns more ore every day."
        ),
        "Form B of stop-one-early, in the same `[i - 1]` form. The right one is authored first.",
    ),
    (
        "This should count down to the burst. What happens when it runs?",
        'hours_left = 3\nwhile hours_left > 0:\n    print(hours_left)\nprint("Burst!")\n',
        [
            "3, 2, 1, then `Burst!`",
            "3, then `Burst!`",
            "Only `Burst!`",
            "3 forever, until the site stops it",
        ],
        3,
        {
            0: "Nothing inside the loop changes `hours_left`, so it never counts down.",
            1: "A `while` loop asks again after every pass. 3 is still more than 0, so it goes round again.",
            2: "3 is more than 0, so the loop runs, and then it never stops.",
        },
        (
            "Nothing inside the loop changes `hours_left`, so `hours_left > 0` stays `True` and `Burst!` is never "
            "reached. The missing line is `hours_left = hours_left - 1`, inside the loop."
        ),
        "Form B of the-loop-that-never-ends: no update at all. The right one is authored last.",
    ),
)


# =============================================================================================
# Cheatsheet "Mar'tu's Chalk Notes: Loops"
# =============================================================================================

CHALK_NOTES_6 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Loops",
    summary="Everything from Unit 6 on one page. Printable.",
    entries=[
        dict(concept="`for item in items:` and an indent",
             code='for color in ["gold", "teal"]:\n    print(color)\n', output="gold\nteal",
             note="The colon says *here comes the body*. Four spaces put a line inside the loop. It runs once for "
                  "each item, and `color` holds the next one each pass. (Lesson: For Each, Yes?)"),
        dict(concept="Each sheet: `member[\"name\"]`",
             code='roster = [\n    {"name": "Oogrish", "mana": 18},\n    {"name": "Lucky", "mana": 26},\n]\n'
                  'for member in roster:\n    print(member["name"])\n',
             output="Oogrish\nLucky",
             note="Inside the loop, read the sheet in your hand, `member`. You've seen this: `for member in "
                  "party.members:` at the bottom of the mana bars."),
        dict(concept="A running total: `total = 0` before the loop",
             code="total = 0\nfor mana in [18, 20, 24, 26]:\n    total = total + mana\nprint(total)\n", output="88",
             note="Set it to 0 once, above the loop. Add inside. Print once, below. `total += mana` works too."),
        dict(concept="An `if` inside the loop",
             code='for mana in [6, 14, 3, 22]:\n    if mana < 10:\n        print(mana, "needs rest")\n',
             output="6 needs rest\n3 needs rest",
             note="Four spaces for the `if`, eight for the lines inside it. The `if` runs every pass; the print "
                  "only when it is `True`."),
        dict(concept="Neighbors: `range(1, len(wall))`",
             code="wall = [48, 48, 47, 46, 44, 41, 37]\nfor i in range(1, len(wall)):\n"
                  "    print(wall[i - 1] - wall[i])\n",
             output="0\n1\n1\n2\n3\n4",
             note="`i` is a position. Start at 1, so `i - 1` is always on the wall. Each shrink is bigger: the "
                  "decay is accelerating."),
        dict(concept="`while` and an update",
             code='hours_left = 3\nwhile hours_left > 0:\n    print(hours_left)\n    hours_left = hours_left - 1\n'
                  'print("Burst!")\n',
             output="3\n2\n1\nBurst!",
             note="The question is asked before every pass. The update inside the loop moves it toward `False`. "
                  "(Lesson: While the Clock Ticks)"),
        dict(concept="A loop that never ends",
             code="glug = 3\nwhile glug > 0:\n    print(glug)\n",
             note="Nothing inside changes `glug`, so it never stops: an [[infinite loop]]. The site stops it after "
                  "200,000 characters of printing (*TooMuchOutput*), or after 5 seconds (*ran too long*). Look "
                  "inside the loop for the missing update, `glug = glug - 1`."),
        dict(concept="`break`: leave early",
             code='for gap in [48, 46, 44, 41]:\n    if gap < 45:\n        print(gap)\n        break\n'
                  'print("done")\n',
             output="44\ndone",
             note="`break` leaves the loop at once, and Python goes on below it. Put it inside the `if`, under the "
                  "print. You know `return`: it stops a recipe the same way."),
        dict(concept="Error: no colon on the `for` line", code="for gap in [48, 47]\n    print(gap)\n",
             note="SyntaxError: expected ':'. Every `for` and `while` line ends with `:`."),
        dict(concept="Error: a body with no indent", code="for gap in [48, 47]:\nprint(gap)\n",
             note="IndentationError: expected an indented block after 'for' statement on line 1. Four spaces put "
                  "a line inside the loop."),
        dict(concept="Error: a loop over a number", code="for i in 5:\n    print(i)\n",
             note="TypeError: 'int' object is not iterable. A loop needs a list or a `range()`: "
                  "`for i in range(5):`."),
        dict(concept="Error: `roster[\"name\"]`",
             code='roster = [{"name": "Lucky"}]\nfor member in roster:\n    print(roster["name"])\n',
             note="TypeError: list indices must be integers or slices, not str. `roster` is the whole list, and a "
                  "list has no keys. Read the sheet in your hand: `member[\"name\"]`."),
        dict(concept="Error: one past the end",
             code="wall = [48, 47, 44]\nfor i in range(len(wall)):\n    print(wall[i] - wall[i + 1])\n",
             note="IndexError: list index out of range. On the last pass there is no next gap. Stop one early, "
                  "`range(len(wall) - 1)`, or start at 1 and use `i - 1`."),
        dict(concept="No error, wrong answer: the total restarts",
             code="for mana in [18, 20, 24, 26]:\n    total = 0\n    total = total + mana\nprint(total)\n",
             output="26",
             note="A quiet bug: `total = 0` runs every pass, so only the last mana is left. Move it above the "
                  "loop."),
        dict(concept="No error, wrong answer: the print inside the loop",
             code="total = 0\nfor mana in [18, 20, 24, 26]:\n    total = total + mana\n    print(total)\n",
             output="18\n38\n62\n88",
             note="Another quiet bug: four spaces put the print inside the loop, so it prints every pass. Take "
                  "them off to print once."),
        dict(concept="(extra) `continue`: skip one pass",
             code="for mana in [6, 0, 14]:\n    if mana == 0:\n        continue\n    print(mana)\n",
             output="6\n14",
             note="`continue` skips the rest of this pass; `break` leaves the whole loop. (Lesson: Loops in One "
                  "Line)"),
        dict(concept="(extra) A loop inside a loop",
             code="log = [[3, 4], [5, 2]]\nfor row in log:\n    for score in row:\n        print(score)\n",
             output="3\n4\n5\n2", note="The inner loop runs all the way through on every pass of the outer one."),
        dict(concept="(extra) A list in one line",
             code="wall = [48, 47, 44, 41, 37]\nprint([h for h in wall if h < 45])\n", output="[44, 41, 37]",
             note="What to keep, then `for`, then an `if` to pick. It builds a new list."),
        dict(concept="(extra) Choose in one line",
             code='mana = 2\nprint("ready" if mana >= 3\n      else "resting")\n', output="resting",
             note="The value before `if` when the question is `True`, the value after `else` when it is `False`."),
        dict(concept="(extra) Loop over a dictionary: `.items()`",
             code='book = {\n    "Glow": 2,\n    "Warm Hands": 3,\n}\nfor name, cost in book.items():\n'
                  "    print(name, cost)\n",
             output="Glow 2\nWarm Hands 3",
             note="Each key with its value, as a pair: two names on the `for` line. `.keys()` gives the keys, "
                  "`.values()` the values. (Article: Looping Over a Dictionary)"),
    ],
    notes=(
        "Cheatsheet 6 (the spec's entries in order: for-plus-indent, `member[\"name\"]`, `total = 0` before the "
        "loop, `range(1, len(wall))`, `while` plus an update, the limit row for a loop that never ends, `break`; "
        "the spec has the filter between the total and the neighbors in its objectives, so `if` inside a loop "
        "sits there too), then the error rows and the quiet bugs, then the extras from the optional Lesson 5C "
        "and Article 5-A1. Entries with `output` are run and checked by the harness; error entries and the "
        "endless loop have none (the page is not runnable). Code lines keep to 36 characters (the neighbors "
        "entry shows the real wall as `wall`, 35 characters). The 'step limit' of the spec is written as what "
        "the site really does: the 200,000-character output limit and the 5-second limit (as u06a's 5B-02)."
    ),
)


ITEMS = [
    QC5_A,
    QC5_A_QUESTIONS,
    QC5_B,
    QC5_B_QUESTIONS,
    CHALK_NOTES_6,
]
