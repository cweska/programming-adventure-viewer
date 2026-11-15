"""Unit 6 "Loops", part b: Project 5P "The Velocite Watch" (with Lucky's side quest), the optional advanced
challenge "Gearshift's Forecast" (write-from-blank, after the project as in Units 3 and 4), Extra practice 6X
"Loops That End" (pool: 5B-05), the optional Lesson 5C "Loops in One Line" (with its SOLO) and the optional
Article 5-A1 "Looping Over a Dictionary" (with a try-it).

Revised on the teacher's rulings on the Unit 6 reviews: the project's `average` starts from a skeleton (`total = 0`
and the loop given, `pass` and `return 0` holding the two places) and its intro says to Run task 1 first; every
"With other names" rung is a fenced block with real indents (slashes hid the indent, and a task that divides with
`/` invites copying them); the two 5C one-liners are no longer dictated (the full line is in their Show rungs
only); the new challenge is honest practice for the stronger groups and costs no one core time.

Spec: design/curriculum.md, "## Unit 6 · Loops", items 4 to 7 ("### Project 5P", "### Extra practice 6X",
"### Lesson 5C ... and Article 5-A1"). Not in this file (by assignment): Lesson 5A, Lesson 5B and Quiz 5 (u06a),
Quick Check 5 and the Loops cheatsheet.
Introduces node:Continue (5C-01), node:ListComp (5C-03), node:IfExp (5C-04), and attr:items, attr:keys,
attr:values (5-A1). `for`, `while` and `break` come from u06a (planned in concept_map.json while u06a is written).
Dictionaries stay inside Unit 5's planned concepts (u05a-u05c): dict literals, reading by key, a list of dicts
(`roster`). Recipes stay inside Unit 3 (`def`, one parameter, `return`). No f-strings (Unit 9), no keyword
arguments or default values (u07c). Tuples come from the optional Tuples article (u04c), the named prerequisite of
5-A1 (2.12 rule 2); 5-A1 recaps them on the page.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN loops there:
`for member in party.members:` at the bottom of the spell-book and mana-bars parts, and the chalk wall's shrink
("the decay is accelerating"). Campaign links are "you've seen this, now you'll get it" moments. Every student
has their own device; pair talk is optional and every checkpoint is solo.

Help ladder as fields (the Unit 2 walkthrough conventions): hints[0] is "Where to look" (the step's place, or in a
debug step "Read Python's last line"), the middle hints teach with other names (listed in foreign_names), and the
last hint holds the step's own line in backticks ("Write `total = 0` ..."), so the site cuts Start me off from it;
that line is always in the solution. another_way = the angle bank; assemble = More structure; solution = Show.
Terminology (2.9): "variable" (Mar'tu may still say "box"), "recipe" / "ingredient" / "hands back" for functions,
"key" for dictionary labels, "gaps" and "shrink" for the chalk wall.

Real data: the party table (max_mana 18, 20, 24, 26; after one Strengthen Magic each, at 10 mana a cast, the
project's mana is 8, 10, 14, 16), the chalk wall 48, 48, 47, 46, 44, 41, 37, Bomb Shell's Velocite ore (about a
week left: `velocite_used = [3, 4, 4, 5, 4]`, 30 chunks, average 4.0, so 7 days), the spell book (Glow 2, Warm
Hands 3, Lantern Ward 6). Rerun data uses invented names only (Pell, Brakka, Moss, Glug, Tester, Zelda, Kratos,
Captain Glug; 2.11), and messages never repeat a student's own text.

Check builders (Units 1-4's rerun idea, made safe for loops):
  _guarded(thunk)    runs student code (a rerun, or a direct call of a student recipe) with its prints captured
                     and a step budget: a sys.settrace line counter on main.py frames (40,000 lines) plus an output
                     cap (60,000 characters). A loop that never ends inside a CHECK stops in milliseconds with
                     err 'ENDLESS', and the step says so plainly. The student's own run is the site's: a `while`
                     with no update that prints each pass stops at the 200,000-character output limit
                     (TooMuchOutput, "Printing forever?"), and one that prints nothing stops at the 5-second limit
                     ("Ran too long"). Every endless-loop wrong answer below prints each pass, so the harness sees
                     TooMuchOutput in well under a second instead of waiting for its 6-second timeout. That is why
                     the project's loop prints `ore_left` every pass (a real "watch") and the countdowns print each
                     hour.
  _rerun(values, roster)  the student's program again with top-level `name = <literal>` lines replaced (lists,
                     dicts, numbers) and, for exercises whose roster lives in hidden setup, the setup re-run with
                     `roster` swapped for other heroes (a deep copy). Returns (namespace, rows, err, missing names).
  _inorder(rows, seq)  every number of `seq` shows, in order, on the printed rows (other rows may sit between).
  _ev(...)           the evidence bracket, "(Mar'tu's check tried `ore_left = 20`, only inside the check.)".
Messages lead with the fix, then say what happened, then the evidence; about 35 words or fewer.

The class's slips for this unit, each proven by a wrong_answers entry (see each exercise):
  a missing colon on the `for` line (project task 4); a body that is not indented (project task 4, 5C SOLO is the
  one-line form's colon); printing the list instead of the item (project task 4 `print(roster)`, 5C-02
  `print(row)` and `print(training)`, 5-A1 `print(spell_book)`); the total reset INSIDE the loop (project task 1,
  5-A1 CP2); the final print indented inside the loop (project task 3 `days`, 5-A1 CP2 `total`) and a filter
  print outside it (project task 5: the `if` outside the loop, or its print left below the loop); `for i in 5` / `for i in len(...)` ("'int' object is not iterable", 5C-02);
  the item used as an index (project task 4 `roster[member]`, 5C-02 `row[score]`); neighbors one past the end
  (5C-03 CP2 `chalk_wall[i + 1]`, IndexError: the loop must stop one early); `roster["name"]` for
  `member["name"]` (project task 4, 5C-01 `roster["mana"]`); a `while` with no update, or the update outside the
  loop (project task 2, 6X: both print forever and stop at the output limit); `while` versus `if` (project task 2, 6X CP1);
  `break` in the wrong place (5C-01: `break` where `continue` belongs, `continue` outside its `if`; the side quest's
  checks name `break` outside the `if` and `break` before the print); values typed by hand instead of read from
  each item (every step, through reruns); the example's list name copied (5C-01 `lanterns`, 5C-02 `shelves`,
  5C-03 `coins`, 5-A1 `pack`, the challenge's hint `hills`). The challenge repeats the unit's hardest ones on a
  blank page: neighbors one past the end (`chalk_wall[i + 1]`), the item as an index, the list reset inside the
  loop, a `while` with no update (or the update outside it), `if` for `while`, `break` inside the loop, the count
  printed every pass or reset inside the loop, and every start typed (37, 5, the shrinks, the count).

Phone width (as u04a-c): fenced pictures, examples, predict code and starter lines keep to 36 characters or fewer.
The one exception is the real wall, `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` (41 characters), kept whole on one
line in editor code (5C-03 and the 5C SOLO), as in Unit 4. Solution lines the student types may run longer.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u06b
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
import copy as _cp
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_SETUP = __SETUP__
class _Endless(_B.BaseException):
    pass
class _Cap(_io.StringIO):
    def __init__(self):
        _io.StringIO.__init__(self)
        self.room = 60000
    def write(self, _t):
        self.room = self.room - _B.len(_t)
        if self.room < 0:
            raise _Endless('print')
        return _io.StringIO.write(self, _t)
_left = [0]
def _tick(_f, _event, _arg):
    if _event == 'line':
        _left[0] = _left[0] - 1
        if _left[0] < 0:
            raise _Endless('steps')
    return _tick
def _watch(_f, _event, _arg):
    if _f.f_code.co_filename == 'main.py':
        return _tick
    return None
def _guarded(_thunk):
    # (value, printed rows, err): err is 'ENDLESS' when a loop never ended (step budget or output cap).
    _out = _Cap()
    _old = _sys.stdout
    _tr = _sys.gettrace()
    _left[0] = 40000
    _val, _err = None, ''
    _sys.stdout = _out
    try:
        try:
            _sys.settrace(_watch)
        except Exception:
            pass
        _val = _thunk()
    except _Endless:
        _err = 'ENDLESS'
    except Exception as _e:
        _err = _B.type(_e).__name__ + ': ' + _B.str(_e)
    finally:
        try:
            _sys.settrace(_tr)
        except Exception:
            pass
        _sys.stdout = _old
    return _val, [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()], _err
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _rerun(_values=None, _roster=None):
    _tree = _ast.parse(_source)
    _vals = _B.dict(_values or {})
    _seen = []
    for _n in _tree.body:
        if (_B.type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
                and _B.type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id in _vals
                and _B.type(_n.value).__name__ in ('List', 'Dict', 'Constant', 'Tuple', 'UnaryOp')):
            _n.value = _lit(_vals[_n.targets[0].id], _n.value)
            _seen.append(_n.targets[0].id)
    _ast.fix_missing_locations(_tree)
    _ns = {'__name__': '__main__'}
    def _go():
        if _SETUP:
            _B.exec(_B.compile(_SETUP, '<setup>', 'exec'), _ns)
        if _roster is not None:
            _ns['roster'] = _cp.deepcopy(_roster)
        _B.exec(_B.compile(_tree, 'main.py', 'exec'), _ns)
    _v, _rows, _err = _guarded(_go)
    return _ns, _rows, _err, [_k for _k in _vals if _k not in _seen]
def _sh(_v):
    _k = _B.type(_v).__name__
    if _k == 'str':
        return '"' + _v + '"'
    if _k == 'list':
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    if _k == 'dict':
        return '{' + ', '.join([_sh(_a) + ': ' + _sh(_b) for _a, _b in _v.items()]) + '}'
    return _B.str(_v)
def _shv(_v):
    # A student's own value is shown only when it is a number or None: never their words (2.11).
    if _B.type(_v).__name__ == 'float' and _B.len(_B.str(_v)) > 8:
        return 'about ' + _B.str(_B.round(_v, 2))
    if _v is None or _B.type(_v).__name__ in ('int', 'float', 'bool'):
        return _B.str(_v)
    return 'something else'
def _ev(_vals=None, _note=''):
    _bits = ['`' + _k + ' = ' + _sh(_v) + '`' for _k, _v in (_vals or {}).items()]
    if _note:
        _bits.append(_note)
    if not _bits:
        return ''
    return " (Mar'tu's check tried " + ' and '.join(_bits) + ', only inside the check.)'
def _keep(_name):
    return ('Keep the line `' + _name + " = ...` from the starter, so Mar'tu's check can try other values there.")
def _stop(_err, _e=''):
    return 'Mend this slip, then Run again: ' + _err + '.' + _e
def _is_num(_v):
    return _B.type(_v).__name__ in ('int', 'float')
def _close(_a, _b):
    return _is_num(_a) and _is_num(_b) and _B.abs(_a - _b) < 1e-6
def _nums(_l):
    return [_B.float(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?:\.\d+)?(?!\d)', _l)]
def _ints(_l):
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?:\.\d+)?(?!\d)', _l) if '.' not in _x]
def _inorder(_rows, _seq):
    # (True, index of the row that showed the last item) when every number of _seq shows, in order.
    _at, _last = 0, -1
    for _i, _l in _B.enumerate(_rows):
        if _at < _B.len(_seq) and _B.any(_close(_x, _seq[_at]) for _x in _nums(_l)):
            _at = _at + 1
            _last = _i
    return _at == _B.len(_seq), _last
def _tree():
    return _ast.parse(_source)
def _kind(_n):
    return _B.type(_n).__name__
def _def(_name):
    _ds = [_n for _n in _tree().body if _kind(_n) == 'FunctionDef' and _n.name == _name]
    return _ds[-1] if _ds else None
def _mentions(_node, _name):
    return _B.any(_kind(_x) == 'Name' and _x.id == _name for _x in _ast.walk(_node))
def _in_loops(_t, _kinds=('For', 'While')):
    # ids of every node inside a loop's body (the loop line itself not counted).
    _ids = _B.set()
    for _n in _ast.walk(_t):
        if _kind(_n) in _kinds:
            for _part in _n.body + _n.orelse:
                for _x in _ast.walk(_part):
                    _ids.add(_B.id(_x))
    return _ids
def _prints(_t):
    return [_n for _n in _ast.walk(_t) if _kind(_n) == 'Call' and _kind(_n.func) == 'Name' and _n.func.id == 'print']
def _runs(_l):
    return _re.findall('[█░]+', _l)
'''


def chk(label, body, setup="", **subs):
    """A check: the shared _PRE (with the exercise's hidden setup), then `body` with each __NAME__ replaced by
    repr(value)."""
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    return (label, _PRE.replace("__SETUP__", repr(setup)) + body)


WALL = [48, 48, 47, 46, 44, 41, 37]
WALL_LINE = "chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"


def _sheet_lines(roster):
    out = "roster = [\n"
    for hero in roster:
        out += "    " + repr(hero).replace("'", '"') + ",\n"
    return out + "]\n"


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of loops)
# ---------------------------------------------------------------------------------------------

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
        "bars. Somebody else wrote them for you. Since then you have written recipes and lists of your own. "
        "Tonight you write them yourself, one pass at a time."
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

# New terms only (this part's tools). u06a defines the unit's core loop terms; Units 1-5 define theirs.
GLOSSARY = [
    dict(
        term="continue",
        aliases=["continue statement"],
        plain=(
            "Skips the rest of this pass of a loop and goes straight on to the next item. `break` leaves the whole "
            "loop; `continue` only skips one pass."
        ),
        example="if mana == 0:\n    continue",
    ),
    dict(
        term="loop inside a loop",
        aliases=["loops inside loops", "nested loop", "nested loops", "inner loop", "outer loop"],
        plain=(
            "A loop written in another loop's body. The inner loop runs all the way through on every pass of the "
            "outer one."
        ),
        example="for row in log:\n    for score in row:\n        print(score)",
    ),
    dict(
        term="list comprehension",
        aliases=["list comprehensions", "comprehension", "one-line loop", "one-line loops"],
        plain=(
            "A loop in one line that builds a new list: what to keep, then `for`, then an `if` if you want to pick. "
            "It always sits inside square brackets."
        ),
        example="[c for c in coins if c > 4]",
    ),
    dict(
        term="one-line choice",
        aliases=["one-line choices", "conditional expression", "one-line if"],
        plain=(
            "Picks one of two values in one line: the value before `if` when the question is True, the value "
            "after `else` when it is False."
        ),
        example='"lit" if oil > 0 else "dark"',
    ),
    dict(
        term=".items()",
        aliases=["items()"],
        plain=(
            "Hands back each key of a dictionary together with its value, as a pair. A loop can give the pair two "
            "names."
        ),
        example="for name, cost in book.items():",
    ),
    dict(
        term=".keys()",
        aliases=["keys()"],
        plain="Hands back a dictionary's keys. A plain loop over a dictionary walks its keys too.",
        example="list(book.keys())",
    ),
    dict(
        term=".values()",
        aliases=["values()"],
        plain="Hands back a dictionary's values, without their keys.",
        example="sum(book.values())",
    ),
]


# =============================================================================================
# Project 5P "The Velocite Watch" (SC, 20 min)
# =============================================================================================

# After a night holding the barrier: the same night as u06a's 5A-06 and 5A-07 (NIGHT_SHEETS), max_mana from the
# party table. Under 10: Oogrish (6) and Bomb Shell (3).
ROSTER_5P = [
    {"name": "Oogrish", "mana": 6, "max_mana": 18},
    {"name": "Gearshift", "mana": 14, "max_mana": 20},
    {"name": "Bomb Shell", "mana": 3, "max_mana": 24},
    {"name": "Lucky", "mana": 22, "max_mana": 26},
]
SETUP_5P = _sheet_lines(ROSTER_5P)

# The other rosters Mar'tu's check tries (invented names). Under 10 mana: Pell, Moss and Tester in A; Zelda in B.
# Glug has exactly 10 (not under 10: the BND for `<`); the last hero is under 10 in A and not in B, so an `if`
# outside the loop (which only sees the last member) fails, and so does a typed flag. Zelda (7 of 12) is under 10
# but over half her bar, so a flag on "under half of max_mana" (right for the real night and roster A) fails.
ROSTER_A = [
    {"name": "Pell", "mana": 3, "max_mana": 12},
    {"name": "Brakka", "mana": 12, "max_mana": 15},
    {"name": "Moss", "mana": 9, "max_mana": 20},
    {"name": "Glug", "mana": 10, "max_mana": 10},
    {"name": "Tester", "mana": 0, "max_mana": 14},
]
ROSTER_B = [
    {"name": "Kratos", "mana": 15, "max_mana": 16},
    {"name": "Zelda", "mana": 7, "max_mana": 12},
    {"name": "Captain Glug", "mana": 11, "max_mana": 12},
]
ROSTER_CASES = [(None, ""), (ROSTER_A, "a roster of 5 other heroes"), (ROSTER_B, "a roster of 3 other heroes")]

VELO_LOG = [3, 4, 4, 5, 4]
VELO_ORE = 30
# (velocite_used, ore_left) reruns: averages 3.0, 1.5 and 6.0. The 1.5 log lands exactly on one day's use (1.5 left),
# so `>` stops a day early; 6 and 8 days differ from the real 7, so a typed count fails.
VELO_CASES = [
    None,
    {"velocite_used": [2, 3, 3, 4], "ore_left": 20},
    {"velocite_used": [1, 2], "ore_left": 6},
    {"velocite_used": [5, 6, 7, 6], "ore_left": 50},
]

BAR_SRC = (
    "def mana_bar(hero):\n"
    "    # Finished (Bars for everyone).\n"
    "    mana = hero[\"mana\"]\n"
    "    used = hero[\"max_mana\"] - mana\n"
    "    return \"█\" * mana + \"░\" * used\n"
)

# The recipe's skeleton (teacher ruling on the Unit 6 reviews): `total = 0` and the loop are given, and the two
# lines a student fills hold places with `pass` and `return 0`.
AVG_SKELETON = (
    "    total = 0\n"
    "    for value in values:\n"
    "        pass  # add value to total\n"
    "    return 0  # total / how many\n"
)

VELO_STARTER = (
    "# The Velocite Watch\n"
    "# Bomb Shell's Velocite ore: chunks\n"
    "# used each day this week.\n"
    "velocite_used = [3, 4, 4, 5, 4]\n"
    "ore_left = 30\n"
    "\n"
    "# A. Use log\n"
    "# 1. Hand back the average: add up\n"
    "#    values with a loop, then divide\n"
    "#    by how many there are.\n"
    "def average(values):\n"
    + AVG_SKELETON
    + "\n"
    "# This should show 3.0:\n"
    "print(average([2, 4]))\n"
    "\n"
    "# B. Days left\n"
    "daily = average(velocite_used)\n"
    "days = 0\n"
    "# 2. While ore_left is at least\n"
    "#    daily, take daily off ore_left\n"
    "#    and print ore_left.\n"
    "# 3. Count each pass in days. Then\n"
    "#    print days, after the loop.\n"
    "\n"
    "# C. Party check (roster is ready)\n"
    + BAR_SRC
    + "\n"
    "# 4. For each member of roster,\n"
    "#    print the name and its bar.\n"
    "# 5. In the same loop, flag anyone\n"
    "#    under 10 mana: print the name\n"
    "#    and \"needs rest\".\n"
)

AVG_BODY = (
    "    total = 0\n"
    "    for value in values:\n"
    "        total = total + value\n"
    "    return total / len(values)\n"
)
WATCH = (
    "while ore_left >= daily:\n"
    "    ore_left = ore_left - daily\n"
    "    print(\"Ore left: \" + str(ore_left))\n"
)
LOOP_FULL = (
    "while ore_left >= daily:\n"
    "    ore_left = ore_left - daily\n"
    "    days = days + 1\n"
    "    print(\"Ore left: \" + str(ore_left))\n"
    "print(\"Days left: \" + str(days))\n"
)
PARTY = (
    "for member in roster:\n"
    "    print(member[\"name\"], mana_bar(member))\n"
)
PARTY_FLAG = PARTY + (
    "    if member[\"mana\"] < 10:\n"
    "        print(member[\"name\"], \"needs rest\")\n"
)
SIDE = (
    "day = 0\n"
    "for used in velocite_used:\n"
    "    day = day + 1\n"
    "    if used > 4:\n"
    "        print(\"First day over 4: day \" + str(day))\n"
    "        break\n"
)


def _fill(add=None, ret=None):
    """The recipe's skeleton with its `pass` line and/or its `return 0` line replaced (None = left as given)."""
    body = AVG_SKELETON
    if add is not None:
        body = body.replace("        pass  # add value to total\n", add)
    if ret is not None:
        body = body.replace("    return 0  # total / how many\n", ret)
    return body


def _velo(avg=None, loop="", party="", extra="", head=None):
    """The project program with any of its parts filled in (None / "" = the starter's). `avg` replaces the
    recipe's whole skeleton body (AVG_SKELETON)."""
    code = VELO_STARTER
    if head is not None:
        code = code.replace("velocite_used = [3, 4, 4, 5, 4]\nore_left = 30\n", head)
    if avg is not None:
        assert AVG_SKELETON in code
        code = code.replace(AVG_SKELETON, avg, 1)
    if loop:
        code = code.replace("#    print days, after the loop.\n", "#    print days, after the loop.\n" + loop)
    if party:
        code = code.replace("#    and \"needs rest\".\n", "#    and \"needs rest\".\n" + party)
    return code + extra


VELO_SOLUTION = _velo(AVG_BODY, LOOP_FULL, PARTY_FLAG)

AVERAGE_CHECK = chk(
    "average hands back the total divided by the count, with a loop",
    r'''
_d = _def('average')
assert _d is not None and _B.callable(globals().get('average')), (
    'Keep the recipe `def average(values):` from the starter, and finish its body.')
_ps = [_a.arg for _a in _d.args.args]
_p = _ps[0] if _ps else 'values'
assert not ('velocite_used' not in _ps and _mentions(_d, 'velocite_used')), (
    'Use the ingredient `' + _p + '` inside the recipe, not `velocite_used`. The recipe works on whatever list it '
    'is handed.')
# The skeleton's two placeholders: a loop whose body is only `pass`, and `return 0`.
_rets0 = [_r for _r in _ast.walk(_d) if _kind(_r) == 'Return' and _r.value is not None
          and _kind(_r.value) == 'Constant' and _kind(_r.value.value) == 'int' and _r.value.value == 0]
_idle = [_n for _n in _ast.walk(_d) if _kind(_n) in ('For', 'While')
         and _B.all(_kind(_x) == 'Pass' for _x in _n.body)]
_fn = globals()['average']
_res = []
for _arg in __CASES__:
    _r, _rows, _err = _guarded(lambda: _fn(_B.list(_arg)))
    _call = '`average(' + _sh(_arg) + ')`'
    assert _err != 'ENDLESS', 'Mend the recipe so it always ends. ' + _call + ' never finished: a loop in it kept going.'
    if _err:
        _tip = ''
        if _err.startswith('TypeError') and 'list' in _err:
            _tip = ' Inside the loop, add the one value from this pass, not the whole list.'
        assert False, ('Mend the recipe so it works for any list.' + _tip + ' ' + _call + ' stopped Python: ' + _err
                       + '.')
    _res.append((_arg, _r, _rows))
_got = [_r for _a, _r, _o in _res]
if _B.all(_is_num(_v) and _close(_v, 0) for _v in _got):
    _e0 = (" (Mar'tu's check called `average(" + _sh(_res[0][0]) + ")`, only inside the check: it handed back "
           + _shv(_got[0]) + '.)')
    assert not (_rets0 and _idle), (
        "Fill in the starter's `pass` and `return 0`. Inside the loop, add each value to `total`. After it, hand "
        'back `total` divided by how many values there are.' + _e0)
    assert not _rets0, ('Replace `return 0` with the answer: `total` divided by how many values there are. The '
                        'recipe still hands back 0, whatever list it gets.' + _e0)
    assert not _idle, ('Replace `pass` with a line that adds this pass\'s value to `total`, eight spaces in. '
                       '`total` stayed 0 all the way through the loop.' + _e0)
if _B.all(_is_num(_v) for _v in _got) and _B.all(_close(_v, _got[0]) for _v in _got):
    assert False, ('Work it out from `' + _p + '`, the list the recipe is handed, not from a number you typed. '
                   "(Mar'tu's check called " + ' and '.join('`average(' + _sh(_a) + ')`' for _a, _r, _o in _res[:2])
                   + ', only inside the check: both gave back ' + _B.str(_got[0]) + '.)')
def _resets(_node):
    for _n in _ast.walk(_node):
        if _kind(_n) == 'For':
            for _part in _n.body:
                for _x in _ast.walk(_part):
                    if _kind(_x) == 'Assign' and _kind(_x.value) == 'Constant' and _x.value.value == 0:
                        return True
    return False
def _early(_node):
    for _n in _ast.walk(_node):
        if _kind(_n) in ('For', 'While'):
            for _part in _n.body:
                if _B.any(_kind(_x) == 'Return' for _x in _ast.walk(_part)):
                    return True
    return False
_ks = [_B.sum(_a) / _v for _a, _v, _o in _res if _is_num(_v) and _v]
for _arg, _r, _rows in _res:
    _want = _B.sum(_arg) / _B.len(_arg)
    if _is_num(_r) and _close(_r, _want):
        continue
    _call = '`average(' + _sh(_arg) + ')`'
    _e = (" (Mar'tu's check called " + _call + ', only inside the check: it handed back ' + _shv(_r)
          + ', but the average is ' + _sh(_want) + '.)')
    if _r is None:
        assert not _rows, ('Hand the answer back with `return`. `print` only shows it on the screen.'
                           " (Mar'tu's check called " + _call + ', only inside the check: it printed a line but '
                           'handed back `None`.)')
        assert False, 'Put `return` in front of the answer, at the end of the recipe.' + _e
    assert _is_num(_r), 'Hand back a number: the total divided by the count.' + _e
    _n = _B.len(_arg)
    assert not (_B.any(_kind(_x) == 'FloorDiv' for _x in _ast.walk(_d)) and _close(_r, _B.sum(_arg) // _n)), (
        'Use `/`, not `//`. `//` throws away the part after the point.' + _e)
    assert not (_close(_r, _arg[-1] / _n) and _resets(_d)), (
        'Take `total = 0` out of the loop: it goes above the `for` line, once. Inside the loop, the total starts '
        'again every pass, so only the last value counts.' + _e)
    assert not (_close(_r, _arg[0] / _n) and _early(_d)), (
        'Take one indent off `return`, so it runs after the loop. Inside the loop, the recipe hands back after the '
        'first value.' + _e)
    assert not (_close(_r, _arg[-1] / _n) and _idle), (
        'Put the adding line inside the loop, in place of `pass`, with eight spaces in front. Below the loop, it '
        'adds only the last value.' + _e)
    assert not _close(_r, _arg[-1] / _n), (
        'Add each value to the total: `total = total + value`. Your total held only the last value.' + _e)
    assert not _close(_r, _B.sum(_arg)), 'Divide the total by how many values there are: `len(' + _p + ')`.' + _e
    assert not (_B.len(_ks) == _B.len(_res) and _B.all(_close(_k, _ks[0]) for _k in _ks)), (
        'Divide by `len(' + _p + ')`, not by a number you typed: a list can be any length.' + _e)
    assert False, 'Hand back the total divided by the count.' + _e
_loops = [_n for _n in _ast.walk(_d) if _kind(_n) in ('For', 'While')]
assert _loops, ('Add up the values with a `for` loop, as task 1 asks. `sum()` gets the same number, but this step '
                'is loop practice: `total = 0`, then `for value in ' + _p + ':`.')
# The loop must change a name the answer is built from (`total`, or a `count` beside it), so a loop that only
# sits beside `return sum(values) / len(values)` does not count.
_need = _B.set(_x.id for _r in _ast.walk(_d) if _kind(_r) == 'Return' and _r.value is not None
               for _x in _ast.walk(_r.value) if _kind(_x) == 'Name')
_sets = [_x for _x in _ast.walk(_d) if _kind(_x) in ('Assign', 'AugAssign')]
def _target_ids(_x):
    _ts = _x.targets if _kind(_x) == 'Assign' else [_x.target]
    return [_y.id for _t in _ts for _y in _ast.walk(_t) if _kind(_y) == 'Name']
for _round in _B.range(6):
    for _x in _sets:
        if _B.set(_target_ids(_x)) & _need:
            _need = _need | _B.set(_y.id for _y in _ast.walk(_x.value) if _kind(_y) == 'Name')
_adds = [_x for _l in _loops for _part in _l.body for _x in _ast.walk(_part) if _kind(_x) in ('Assign', 'AugAssign')
         and _B.set(_target_ids(_x)) & _need]
assert _adds, ('Add each value to the total inside the loop, `total = total + value`, and hand back that total '
               'divided by the count. Your loop runs, but the answer does not come from it. This step is loop '
               'practice.')
''',
    setup=SETUP_5P,
    CASES=[[5, 6, 10], [1, 2], [8, 2, 1, 3]],
)

# The watch and the count share one rerun per log. `_after` is ore_left after each pass; `_before` before it.
_VELO_RUN = r'''
def _velo_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', [], __LOG__, __ORE__, ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    return _ns, _rows, _err, _miss, _vals['velocite_used'], _vals['ore_left'], _ev(_vals)
def _plan(_log, _ore):
    _d = _B.sum(_log) / _B.len(_log)
    _after, _o = [], _ore
    while _o >= _d - 1e-9 and _B.len(_after) < 200:
        _o = _o - _d
        _after.append(_o)
    return _d, _after, [_ore] + _after[:-1], _o
'''

WATCH_CHECK = chk(
    "each pass takes a day's use off ore_left and prints what is left",
    _VELO_RUN + r'''
_t = _tree()
_whiles = [_n for _n in _ast.walk(_t) if _kind(_n) == 'While']
_ifs = [_n for _n in _ast.walk(_t) if _kind(_n) == 'If' and _mentions(_n.test, 'ore_left')]
def _uses_daily(_node):
    return _B.any(_mentions(_node, _x) for _x in ('daily', 'average', 'velocite_used'))
_w_ids = _in_loops(_t, ('While',))
_updates = [_n for _n in _ast.walk(_t) if _kind(_n) in ('Assign', 'AugAssign') and _B.id(_n) in _w_ids
            and _B.any(_kind(_x) == 'Name' and _x.id == 'ore_left'
                       for _x in (_n.targets if _kind(_n) == 'Assign' else [_n.target]))]
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _log, _ore, _e = _velo_case(_vals)
    assert not _miss, _keep(_miss[0])
    assert not (_err == 'ENDLESS' and _updates), (
        'Let `ore_left` decide when to stop: `while ore_left >= daily:`. With another log, your `while` loop never '
        'stopped.' + _e)
    assert _err != 'ENDLESS', ('Take `daily` off `ore_left` inside the loop, every pass, so the loop can end. Your '
                               '`while` loop never stopped.' + _e)
    _d, _after, _before, _o = _plan(_log, _ore)
    if _err:
        # A slip further down (the party check, the side quest) must not turn this step red: judge what ran.
        _ok_a, _la = _inorder(_rows, _after)
        _ok_b, _lb = _inorder(_rows, _before)
        assert (_whiles and _close(_ns.get('daily'), _d) and _close(_ns.get('ore_left'), _o)
                and (_ok_a or _ok_b)), _stop(_err, _e)
        continue
    _daily = _ns.get('daily')
    assert _close(_daily, _d), ("Keep `daily = average(velocite_used)` from the starter, so `daily` is one day's "
                                'average use: ' + _sh(_d) + ' here.' + _e)
    assert _whiles or not _ifs, ('Use `while`, not `if`. `if` asks once; `while` asks again before every pass, so '
                                 'the loop goes on day after day.' + _e)
    assert _whiles, 'Write a `while` loop: `while ore_left >= daily:`, with the day\'s steps indented under it.' + _e
    _got = _ns.get('ore_left')
    if not _close(_got, _o):
        _gs = _shv(_got)
        assert _B.any(_mentions(_w.test, 'ore_left') for _w in _whiles), (
            'Let `ore_left` decide when to stop: `while ore_left >= daily:`. A loop that counts to a number you '
            'typed cannot follow another log.' + _e)
        assert not _close(_got, _o - _d), ('Stop when less than one day is left: `while ore_left >= daily:`. Your '
                                           'loop ran one day too many, so `ore_left` ended at ' + _gs + '.' + _e)
        assert _B.any(_uses_daily(_w.test) for _w in _whiles if _mentions(_w.test, 'ore_left')), (
            'Compare `ore_left` with `daily`, not with a number you typed: `while ore_left >= daily:`. Another log '
            'has another daily use.' + _e)
        assert not (_updates and not _B.any(_uses_daily(_u.value) for _u in _updates)), (
            'Take `daily` off each pass, not a number you typed: `ore_left = ore_left - daily`. Another log has '
            'another daily use.' + _e)
        assert not _close(_got, _o + _d), ('Use `>=`: with exactly one day of ore left, Bomb Shell still has a day. '
                                           'Your loop stopped one day early.' + _e)
        assert not _close(_got, _ore), ("Take a day's use off each pass: `ore_left = ore_left - daily`, indented "
                                        'under the `while` line. `ore_left` stayed ' + _gs + '.' + _e)
        assert False, ('Each pass, take `daily` off `ore_left`, until less than `daily` is left. It should end at '
                       + _sh(_o) + ', and it ended at ' + _gs + '.' + _e)
    _ok_a, _la = _inorder(_rows, _after)
    _ok_b, _lb = _inorder(_rows, _before)
    if not (_ok_a or _ok_b):
        _whole = [_B.int(_x) for _x in _after]
        _near = [_B.round(_x) for _x in _after]
        assert not (_inorder(_rows, _whole)[0] or _inorder(_rows, _near)[0]), (
            'Print `ore_left` just as it is, with `str(ore_left)`, not rounded. Another log leaves halves, like '
            '4.5.' + _e)
    assert _ok_a or _ok_b, ('Print `ore_left` inside the loop, after you take the day off, so each day shows what '
                            'is left.' + _e)
''',
    setup=SETUP_5P,
    CASES=VELO_CASES,
    LOG=VELO_LOG,
    ORE=VELO_ORE,
)

DAYS_CHECK = chk(
    "days counts the passes and prints once, after the loop",
    _VELO_RUN + r'''
_t = _tree()
_inside = _in_loops(_t)
_dprints = [_n for _n in _prints(_t) if _mentions(_n, 'days')]
_in_print = [_n for _n in _dprints if _B.id(_n) in _inside and not _mentions(_n, 'ore_left')]
_top_print = [_n for _n in _dprints if _B.id(_n) not in _inside]
_counts = [_n for _n in _ast.walk(_t) if _kind(_n) in ('Assign', 'AugAssign') and _mentions(_n, 'days')
           and not (_kind(_n) == 'Assign' and _kind(_n.value) == 'Constant')]
_counted_inside = [_n for _n in _counts if _B.id(_n) in _inside]
_reset_inside = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Assign' and _kind(_n.value) == 'Constant'
                 and _B.id(_n) in _inside and _B.any(_kind(_x) == 'Name' and _x.id == 'days' for _x in _n.targets)]
_own_days = globals().get('days')
_DIVIDE = ('Count the passes inside the loop: `days = days + 1`, indented under the `while` line. Dividing gets the '
           'same number here, but this step is loop practice: the loop counts its own days.')
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _log, _ore, _e = _velo_case(_vals)
    assert not _miss, _keep(_miss[0])
    assert _err != 'ENDLESS', 'Make sure the `while` loop can end.' + _e
    _d, _after, _before, _o = _plan(_log, _ore)
    _n = _B.len(_after)
    _got = _ns.get('days')
    if _err:
        # A slip further down (the party check, the side quest) must not turn this step red: judge what ran.
        _ok_a, _la = _inorder(_rows, _after)
        _ok_b, _lb = _inorder(_rows, _before)
        _last = _B.max(_la if _ok_a else -1, _lb if _ok_b else -1)
        assert (_kind(_got) == 'int' and _got == _n and _counted_inside
                and [_l for _l in _rows[_last + 1:] if _n in _ints(_l)]), _stop(_err, _e)
        continue
    if not (_kind(_got) == 'int' and _got == _n):
        assert not (_is_num(_got) and _close(_got, _n) and not _counted_inside), _DIVIDE + _e
        assert not (_reset_inside and _got == 1), (
            'Move `days = 0` above the `while` line. Inside the loop, the count starts again every pass, so it '
            'never gets past 1.' + _e)
        assert not (_kind(_got) == 'int' and _got == 0), ('Add 1 to `days` inside the loop, each pass: '
                                                          '`days = days + 1`. `days` is still 0.' + _e)
        assert not (_got == 1 and _counts and not _counted_inside), (
            'Indent `days = days + 1` under the `while` line, so it counts every pass. Outside the loop, it adds 1 '
            'only once.' + _e)
        assert not (_vals is not None and _got == _own_days), (
            'Count the passes with `days = days + 1`, so `days` follows the log. Your `days` stayed '
            + _shv(_got) + ', a number typed by hand.' + _e)
        assert False, ('Make `days` count the passes: 1 more each time the loop runs. It should end at '
                       + _B.str(_n) + ', and it ended at ' + _shv(_got) + '.' + _e)
    assert not (_in_print and not _top_print), (
        'Print `days` once, after the loop: take the indent off that print line. Inside the loop, it prints every '
        'pass.')
    _ok_a, _la = _inorder(_rows, _after)
    _ok_b, _lb = _inorder(_rows, _before)
    _last = _B.max(_la if _ok_a else -1, _lb if _ok_b else -1)
    if not [_l for _l in _rows[_last + 1:] if _n in _ints(_l)]:
        assert not (_vals is not None and [_l for _l in _rows[_last + 1:] if _own_days in _ints(_l)]), (
            'Print `days` itself, so the line follows the log. Your line shows a number typed by hand.' + _e)
        assert False, 'After the loop, print `days`: `print("Days left: " + str(days))`.' + _e
assert _counted_inside, _DIVIDE
''',
    setup=SETUP_5P,
    CASES=VELO_CASES,
    LOG=VELO_LOG,
    ORE=VELO_ORE,
)

_ROSTER_RUN = r'''
def _ros_case(_ros, _note):
    if _ros is None:
        return globals(), _lines(), '', __OWN__, ''
    _ns, _rows, _err, _miss = _rerun(None, _ros)
    return _ns, _rows, _err, _ros, _ev(None, _note)
def _bar(_h):
    return '█' * _h['mana'] + '░' * (_h['max_mana'] - _h['mana'])
_own_names = [_h['name'] for _h in __OWN__]
_t = _tree()
_typed_roster = [_n for _n in _t.body if _kind(_n) == 'Assign'
                 and _B.any(_kind(_x) == 'Name' and _x.id == 'roster' for _x in _n.targets)]
'''

BARS_CHECK = chk(
    "each member's name and bar print, from one loop",
    _ROSTER_RUN + r'''
_bar_def = [_n for _n in _t.body if _kind(_n) == 'FunctionDef' and _n.name == 'mana_bar']
assert _bar_def, 'Keep the recipe `mana_bar(hero)` from the starter. It is already finished.'
assert _ast.dump(_bar_def[-1]) == _ast.dump(_ast.parse(__BAR__).body[0]), (
    '`mana_bar` changed. It is already finished, so leave it as it is, and call it: `mana_bar(member)`.')
assert not _typed_roster, ("Use the `roster` that is ready for you, and don't make your own. Mar'tu's check swaps "
                           'in other heroes there.')
_fors = [_n for _n in _ast.walk(_t) if _kind(_n) == 'For']
for _ros, _note in __CASES__:
    _ns, _rows, _err, _ros, _e = _ros_case(_ros, _note)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _want = [(_h['name'].lower(), _bar(_h)) for _h in _ros]
    _at = 0
    for _l in _rows:
        if _at < _B.len(_want) and _want[_at][0] in _l.lower() and _want[_at][1] in _runs(_l):
            _at = _at + 1
    if _at == _B.len(_want):
        continue
    assert not [_l for _l in _rows if _l.startswith('[{')], (
        'Print one member at a time: use `member`, the hero for this pass, not `roster`. Your loop printed the '
        'whole roster.' + _e)
    assert not [_l for _l in _rows if _l.startswith("{'")], (
        'Print the name, `member["name"]`, and the bar, not the whole sheet. Your loop printed each sheet with its '
        'brackets.' + _e)
    assert _fors, 'Use a `for` loop over `roster`, so every member gets a line: `for member in roster:`.' + _e
    assert not (_e and [_l for _l in _rows if _B.any(_x.lower() in _l.lower() for _x in _own_names)]), (
        'Let one print inside the loop do every member. Lines typed for each hero cannot follow a new roster.' + _e)
    _hits = [_w for _w in _want if [_l for _l in _rows if _w[0] in _l.lower() and _w[1] in _runs(_l)]]
    assert not (_B.len(_want) > 1 and _hits == _want[-1:]), (
        'Indent the print under the `for` line, so it runs for every member. Only the last member printed.' + _e)
    assert not [_l for _l in _rows if '<function' in _l], (
        'Call the recipe with brackets: `mana_bar(member)`. Without them, Python prints the recipe itself, not '
        'the bar it hands back.' + _e)
    _bar_rows = [_l for _l in _rows if _B.any(_w[1] in _runs(_l) for _w in _want)]
    assert _bar_rows, 'Add the bar to each line: `mana_bar(member)`.' + _e
    assert [_l for _l in _rows if _B.any(_w[0] in _l.lower() for _w in _want)], (
        'Put the name on the same line as the bar: `member["name"]`.' + _e)
    assert _hits, ('Print the name and the bar in one `print`, with a comma between them, so they share a line: '
                   '`print(member["name"], mana_bar(member))`.' + _e)
    assert False, ("Print each member's name and bar, one line each, in roster order: "
                   '`print(member["name"], mana_bar(member))`.' + _e)
_calls = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Call' and _kind(_n.func) == 'Name' and _n.func.id == 'mana_bar']
assert _calls, ('Call the recipe for each member: `mana_bar(member)`. It is already finished, so the loop does not '
                'need to build the bar again.')
''',
    setup=SETUP_5P,
    OWN=ROSTER_5P,
    CASES=ROSTER_CASES,
    BAR=BAR_SRC,
)

FLAG_CHECK = chk(
    "anyone under 10 mana is flagged, from inside the loop",
    _ROSTER_RUN + r'''
_inside = _in_loops(_t, ('For',))
_out_ifs = [_n for _n in _ast.walk(_t) if _kind(_n) == 'If' and _B.id(_n) not in _inside
            and _mentions(_n.test, 'member')]
# prints that say "needs rest", and prints below the roster loop that sit in no loop (a flag printed once, after it)
_rest_prints = [_n for _n in _prints(_t) if _B.any(_kind(_x) == 'Constant' and _kind(_x.value) == 'str'
                                                    and 'needs rest' in _x.value.lower() for _x in _ast.walk(_n))]
_all_inside = _in_loops(_t)
_ends = [_n.end_lineno for _n in _ast.walk(_t) if _kind(_n) == 'For' and _mentions(_n.iter, 'roster')]
_late_prints = [_n for _n in _prints(_t) if _ends and _n.lineno > _B.max(_ends) and _B.id(_n) not in _all_inside
                and (_n in _rest_prints or _mentions(_n, 'member'))]
for _ros, _note in __CASES__:
    _ns, _rows, _err, _ros, _e = _ros_case(_ros, _note)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _flags = [_l for _l in _rows if 'needs rest' in _l.lower()]
    _want = [_h for _h in _ros if _h['mana'] < 10]
    _hit = [_h for _h in _ros if [_l for _l in _flags if _h['name'].lower() in _l.lower()]]
    if _B.len(_flags) == _B.len(_want) and _hit == _want:
        continue
    assert not (_out_ifs and _want and not _hit), (
        'Indent the `if` under the `for` line, so every member is checked. Outside the loop, it only checks the '
        'last member.' + _e)
    _extra = [_h for _h in _hit if _h['mana'] >= 10]
    assert not [_h for _h in _extra if _h['mana'] == 10], (
        'Use `< 10`: 10 is not under 10. Your code flagged a member with exactly 10 mana.' + _e)
    assert not _extra, ('Flag only members under 10 mana. Your code flagged one with ' + _B.str(_extra[0]['mana'])
                        + ' mana.' + _e)
    assert not (_e and [_l for _l in _flags if _B.any(_x.lower() in _l.lower() for _x in _own_names)]), (
        'Let the `if` decide, from `member["mana"]`. A flag typed for one hero cannot follow a new roster.' + _e)
    assert not (_flags and not _hit), 'Put the name in each flag line: `print(member["name"], "needs rest")`.' + _e
    if not _flags:
        assert not _rest_prints, ('Ask about each member\'s mana, inside the loop: `if member["mana"] < 10:`. Nobody '
                                  'was flagged, but a member with ' + _B.str(_want[0]['mana']) + ' mana is under 10.'
                                  + _e)
        assert False, ('Print the words `needs rest` with the name of each member under 10 mana: '
                       '`print(member["name"], "needs rest")`. No line said `needs rest`.' + _e)
    _missed = [_h for _h in _want if _h not in _hit]
    assert not (_missed and _late_prints), (
        "Indent the flag's print under the `if`, inside the loop. After the loop, it prints only once, for one "
        'member.' + _e)
    assert not _missed, ('Flag every member under 10 mana: inside the loop, `if member["mana"] < 10:`. A member '
                         'with ' + _B.str(_missed[0]['mana']) + ' mana was not flagged.' + _e)
    assert False, 'Flag each member under 10 mana once: print the name and `needs rest`.' + _e
''',
    setup=SETUP_5P,
    OWN=ROSTER_5P,
    CASES=ROSTER_CASES,
)

# Lucky's side quest: the first day over 4, then `break`. Logs: the real one (day 4), one whose very first day is
# over 4 (day 1), and one with three days over 4 (only day 2 may print).
SIDE_CHECK = chk(
    "the first day over 4 prints, then the loop stops",
    r'''
_t = _tree()
def _brk_spots():
    _loose, _first = False, False
    for _n in _ast.walk(_t):
        if _kind(_n) == 'For' and _B.any(_kind(_x) == 'Break' for _x in _n.body):
            _loose = True
        if _kind(_n) == 'If' and _n.body and _kind(_n.body[0]) == 'Break' and _B.len(_n.body) > 1:
            _first = True
    return _loose, _first
_loose, _first = _brk_spots()
def _day_of(_rows):
    return [_ints(_l)[-1] for _l in _rows if _l.lower().startswith('first day over') and _ints(_l)]
_own_day = _day_of(_lines())
for _log, _want in __CASES__:
    if _log is None:
        _rows, _err, _log, _e = _lines(), '', __LOG__, ''
    else:
        _ns, _rows, _err, _miss = _rerun({'velocite_used': _log})
        _e = _ev({'velocite_used': _log})
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _marked = [_l for _l in _rows if _l.lower().startswith('first day over')]
    _last = _day_of(_rows)
    if _B.len(_marked) == 1 and _last == [_want]:
        continue
    _at4 = [_i + 1 for _i, _x in _B.enumerate(_log) if _x >= 4][:1]
    assert not (_last and _last == _at4), (
        'Over 4 means `> 4`: a day with exactly 4 chunks is not over 4. Your loop stopped at day '
        + _B.str(_last[0]) + '.' + _e)
    assert not (_e and _last and _last == _own_day), (
        'Let the loop find the day, so it follows the log. A day typed by hand cannot follow another log.' + _e)
    assert _B.len(_marked) < 2, ('Stop at the first one: put `break` right after the print, under the `if`. Your '
                                 'loop printed ' + _B.str(_B.len(_marked)) + ' days.' + _e)
    if not _marked:
        assert not _loose, ('Put `break` under the `if`, after the print. Right under the `for` line, it stops the '
                            'loop on the very first day.' + _e)
        assert not _first, 'Print first, then `break`. Lines under `break` never run.' + _e
        assert False, ('Print `First day over 4: day ` and the day number, for the first day over 4.' + _e)
    assert not (_last and _last[0] == _want - 1), ('Count days from 1: the first day is day 1, at position 0.' + _e)
    assert not (_last and _last[0] == _log[_want - 1]), ('Print the day number, not the chunks used that day.' + _e)
    assert False, ('Print the number of the first day over 4: day ' + _B.str(_want) + ' here.' + _e)
''',
    setup=SETUP_5P,
    CASES=[(None, 4), ([5, 2, 6, 7], 1), ([2, 6, 5, 9], 2)],
    LOG=VELO_LOG,
)

PROJECT_5P = dict(
    kind="project",
    id="the-velocite-watch",
    title="The Velocite Watch",
    minutes=20,
    summary="Run Bomb Shell's numbers: an average with a loop, the days of ore left with `while`, and a party check.",
    intro=(
        "Bomb Shell runs on Velocite ore, and he has about a week of it left. Gearshift wants numbers, not "
        "guesses: \"Run the math.\"\n"
        "Three parts, in order: A. the use log, B. days left, C. a party check. The comments in the editor mark "
        "each task.\n"
        "Do A first, and press Run: the line under `# This should show 3.0:` shows 0. That is task 1. Until "
        "`average` works, `daily` is 0, and the ore never goes down.\n"
        "The party held the barrier all night, and it cost mana. `roster` is ready for you, four sheets with "
        "`\"name\"`, `\"mana\"` and `\"max_mana\"`:\n"
        "```text\nname        mana  max_mana\nOogrish        6        18\nGearshift     14        20\n"
        "Bomb Shell     3        24\nLucky         22        26\n```"
    ),
    martu=(
        "Two kinds of loop tonight, yes? A [[for loop]] walks a list, one item each pass. A [[while loop]] keeps "
        "going while its question is True, so something inside it must change, or it never stops.\n"
        "My check tries other logs and other rosters. So read every number from the list, and never type one you "
        "can see."
    ),
    names=["average", "values", "ore_left", "daily", "days", "roster", "member", "mana_bar"],
    predict=dict(
        q="Before you start: what does this little `while` loop print?",
        code="ore = 10\nwhile ore >= 4:\n    ore = ore - 4\n    print(ore)\n",
        choices=["6\n2", "6\n2\n-2", "10\n6\n2", "6"],
        answer=0,
        explain=(
            "10 is at least 4, so take 4: 6. 6 is at least 4: 2. Then 2 is not at least 4, so the loop stops. "
            "`while` asks its question again before every pass."
        ),
    ),
    pair_talk=(
        "Before task 2, tell your partner in plain words when the loop should stop. Then each of you writes the "
        "`while` line on your own screen."
    ),
    setup=SETUP_5P,
    starter=VELO_STARTER,
    checkpoints=[
        dict(
            id="average-recipe",
            text="Inside the loop, add each value to `total`. Then hand back `total` divided by how many values there are.",
            dictated=False,
            hints=[
                "Look at the recipe under task 1. `total = 0` and the `for` line are ready. Two lines hold places "
                "for you: `pass` and `return 0`.",
                "A [[running total]] starts at 0 *before* the loop, and grows by one value each pass. After the "
                "loop, divide it by `len(values)`.",
                "With other names, a loop inside a recipe:\n```python\ndef coin_total(purse):\n    count = 0\n"
                "    for coin in purse:\n        count = count + coin\n    return count\n```\n`count` grows by "
                "each coin. The recipe hands it back after the loop.",
                "Write `total = total + value` in place of `pass`, with eight spaces in front. Then write "
                "`return total / len(values)` in place of `return 0`.",
            ],
            checks=[AVERAGE_CHECK],
            pass_line="Gearshift: Visor dims. Four chunks a day. That is the number.",
        ),
        dict(
            id="watch-the-ore",
            text="Write a `while` loop that runs while `ore_left` is at least `daily`. Each pass, take `daily` off `ore_left` and print `ore_left`.",
            dictated=False,
            hints=[
                "Is task 1 ticked? Until `average` works, `daily` is 0, and this loop never ends. Then look under "
                "task 2: the question is *at least*, so the `while` line uses `>=`.",
                "A `while` loop needs an update: a line inside it that changes what the question asks about. "
                "Without one, the question never turns False.",
                "With other names:\n```python\nwhile fuel >= 2:\n    fuel = fuel - 2\n    print(fuel)\n```\n"
                "`fuel = fuel - 2` is the update. It is what lets the loop end.",
                "Write `while ore_left >= daily:`, then indent `ore_left = ore_left - daily` and "
                "`print(\"Ore left: \" + str(ore_left))` under it.",
            ],
            checks=[WATCH_CHECK],
            pass_line="Bomb Shell: Watching it go down. Noted.",
        ),
        dict(
            id="count-the-days",
            text="Add 1 to `days` on every pass. After the loop, print `days` once.",
            dictated=False,
            hints=[
                "Look at task 3. The counting line goes *inside* the loop. The print goes *after* it, with no indent.",
                "A count is a running total that grows by 1 each pass. `days = 0` is already above the loop.",
                "With other names:\n```python\nlaps = 0\nwhile fuel >= 2:\n    fuel = fuel - 2\n"
                "    laps = laps + 1\nprint(laps)\n```\n`laps` grows inside the loop. Its print is at the left edge, so it runs once.",
                "Write `days = days + 1` on the line after `ore_left = ore_left - daily`, inside the loop. Then, "
                "after the loop, write `print(\"Days left: \" + str(days))`.",
            ],
            checks=[DAYS_CHECK],
            pass_line="Mar'tu: Seven days. About a week, like he said. Bomb Shell does not exaggerate.",
        ),
        dict(
            id="party-bars",
            text="For each `member` of `roster`, print the name and the bar from `mana_bar(member)` on one line.",
            dictated=False,
            hints=[
                "Look at part C. `mana_bar` is already finished. Your loop calls it once for each member.",
                "Inside the loop, `member` is one hero's sheet. Read the name with `member[\"name\"]`, not "
                "`roster[\"name\"]`: `roster` is the whole list.",
                "With other names:\n```python\nfor jar in shelf:\n    print(jar[\"label\"], fill(jar))\n```\n"
                "One line for each jar: its label, then what `fill(jar)` hands back.",
                "Write `for member in roster:`, then indent `print(member[\"name\"], mana_bar(member))` under it.",
            ],
            checks=[BARS_CHECK],
            pass_line="Lucky: That's me, the long one. Obviously.",
        ),
        dict(
            id="flag-the-tired",
            text="In the same loop, flag anyone under 10 mana: print their name and `needs rest`.",
            dictated=False,
            hints=[
                "Look at task 5. The `if` goes inside the `for` loop, so it asks about every member, one by one.",
                "*Under 10* means `< 10`. A hero with exactly 10 is not under 10.",
                "With other names:\n```python\nfor jar in shelf:\n    if jar[\"level\"] < 3:\n"
                "        print(jar[\"label\"], \"low\")\n```\nThe `if` is inside the loop, so it asks about every "
                "jar.",
                "Inside the loop, write `if member[\"mana\"] < 10:`, then indent "
                "`print(member[\"name\"], \"needs rest\")` under it.",
            ],
            checks=[FLAG_CHECK],
            pass_line="Oogrish: Steady, now. Bomb Shell and I will rest. After the watch.",
        ),
    ],
    solution=VELO_SOLUTION,
    partials=[
        _velo(AVG_BODY),
        _velo(AVG_BODY, WATCH),
        _velo(AVG_BODY, LOOP_FULL),
        _velo(AVG_BODY, LOOP_FULL, PARTY),
    ],
    assemble=dict(
        lines=[line for line in VELO_SOLUTION.splitlines() if line.strip() and not line.strip().startswith("#")],
        distractors=[
            "        total = 0",
            "if ore_left >= daily:",
            "    print(roster[\"name\"])",
            "    if member[\"mana\"] <= 10:",
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The ore going down",
            text=(
                "```text\nore_left  daily  again?\n30       4.0    yes\n26.0     4.0    yes\n...\n"
                "6.0      4.0    yes\n2.0      4.0    no: stop\n```\n"
                "Each *yes* is one pass, and one more day."
            ),
        ),
        dict(
            angle="everyday",
            label="A bag of snacks",
            text=(
                "You eat 4 snacks a day. While the bag has at least 4, eat a day's worth and count the day. When "
                "fewer than 4 are left, you stop and say how many days you got. That is the `while` loop."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Each loop in order",
            text=(
                "1. `average`: `total` starts at 0, grows by each value, then is divided by `len(values)`.\n"
                "2. `while ore_left >= daily:` asks before every pass.\n"
                "3. Inside it: take `daily` off, add 1 to `days`, print what is left.\n"
                "4. After it: print `days`, once.\n"
                "5. `for member in roster:` prints a bar, then asks the `if`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The mana bars ended with `for member in party.members:` and `show_mana(member)`. Task 4 is the same "
                "loop: one member each pass, one bar each."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's side quest",
        text=(
            "Lucky bets Bomb Shell had one big day. At the bottom, loop over `velocite_used` and find the first day "
            "he used more than 4 chunks. Print `First day over 4: day ` and that day's number (the first day is day "
            "1), then stop the loop with `break`."
        ),
        hints=[
            "Count the days yourself: start `day = 0` above the loop, and add 1 at the top of each pass. The "
            "`break` goes under the `if`, right after the print.",
            "Write `day = 0`, then `for used in velocite_used:` with `day = day + 1` and an `if used > 4:` that "
            "prints the day and then breaks.",
        ],
        checks=[SIDE_CHECK],
        solution=VELO_SOLUTION + SIDE,
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="for member in party.members:\n    show_mana(member)",
        why=(
            "You have run this loop: it drew every hero's bar. Now you wrote one like it yourself, and you know "
            "what `member` holds on each pass."
        ),
    ),
    takeaway=(
        "`for` walks every item of a list. `while` keeps going while its question is True, so a line inside it must "
        "change the answer."
    ),
    wrong_answers=[
        dict(why="the starter (the skeleton's pass and return 0 left)", code=VELO_STARTER, fails_at=1,
             message_contains="Fill in the starter's `pass` and `return 0`"),
        dict(why="pass filled in, return 0 left (hands back 0 for every list)",
             code=_velo(_fill(add="        total = total + value\n")), fails_at=1,
             message_contains="Replace `return 0`"),
        dict(why="return filled in, pass left (total stays 0)",
             code=_velo(_fill(ret="    return total / len(values)\n")), fails_at=1, message_contains="Replace `pass`"),
        dict(why="the adding line written below the loop, pass left (adds only the last value)",
             code=_velo(_fill(add="        pass\n    total = total + value\n", ret="    return total / len(values)\n")),
             fails_at=1, message_contains="in place of `pass`, with eight spaces"),
        dict(why="the adding line with four spaces, in place of pass (the loop body is not indented)",
             code=_velo(_fill(add="    total = total + value\n", ret="    return total / len(values)\n")),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the total reset inside the loop (a second total = 0 under the for line)",
             code=_velo(_fill(add="        total = 0\n        total = total + value\n",
                              ret="    return total / len(values)\n")),
             fails_at=1, message_contains="Take `total = 0` out of the loop"),
        dict(why="the total reset inside the loop (total = 0 moved under the for line)",
             code=_velo("    for value in values:\n        total = 0\n        total = total + value\n"
                        "    return total / len(values)\n"),
             fails_at=1, message_contains="Take `total = 0` out of the loop"),
        dict(why="return inside the loop (hands back after the first value)",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "        return total / len(values)\n"),
             fails_at=1, message_contains="Take one indent off `return`"),
        dict(why="velocite_used read inside the recipe (PAR-CONST)",
             code=_velo("    total = 0\n    for value in velocite_used:\n        total = total + value\n"
                        "    return total / len(velocite_used)\n"),
             fails_at=1, message_contains="ingredient"),
        dict(why="sum() with no loop (this step is loop practice)",
             code=_velo("    return sum(values) / len(values)\n"), fails_at=1, message_contains="`for` loop"),
        dict(why="a loop added beside sum(), but the answer never comes from it",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "    return sum(values) / len(values)\n"),
             fails_at=1, message_contains="the answer does not come from it"),
        dict(why="print instead of return (RET)",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "    print(total / len(values))\n"),
             fails_at=1, message_contains="`return`"),
        dict(why="divided by a typed 5 (fits this log only)",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "    return total / 5\n"),
             fails_at=1, message_contains="not by a number you typed"),
        dict(why="the total, not divided",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "    return total\n"),
             fails_at=1, message_contains="Divide the total"),
        dict(why="each value assigned, not added (the last value only)",
             code=_velo("    total = 0\n    for value in values:\n        total = value\n"
                        "    return total / len(values)\n"),
             fails_at=1, message_contains="Add each value"),
        dict(why="// for / (whole division)",
             code=_velo("    total = 0\n    for value in values:\n        total = total + value\n"
                        "    return total // len(values)\n"),
             fails_at=1, message_contains="`//`"),
        dict(why="the whole list added instead of the item (TypeError in the starter's own call)",
             code=_velo("    total = 0\n    for value in values:\n        total = total + values\n"
                        "    return total / len(values)\n"),
             fails_at=0, message_contains="unsupported operand"),
        dict(why="a while loop with no update (prints forever: the output limit stops it)",
             code=_velo(AVG_BODY, "while ore_left >= daily:\n    days = days + 1\n"
                                  "    print(\"Ore left: \" + str(ore_left))\n"),
             fails_at=0, message_contains="printed more than"),
        dict(why="the update outside the loop (prints forever)",
             code=_velo(AVG_BODY, "while ore_left >= daily:\n    print(\"Ore left: \" + str(ore_left))\n"
                                  "ore_left = ore_left - daily\n"),
             fails_at=0, message_contains="printed more than"),
        dict(why="if instead of while (runs once)",
             code=_velo(AVG_BODY, "if ore_left >= daily:\n    ore_left = ore_left - daily\n"
                                  "    print(\"Ore left: \" + str(ore_left))\n"),
             fails_at=2, message_contains="Use `while`, not `if`"),
        dict(why="while ore_left > 0 (one day too many)",
             code=_velo(AVG_BODY, WATCH.replace(">= daily", "> 0")), fails_at=2,
             message_contains="one day too many"),
        dict(why="> instead of >= (stops a day early when exactly one day is left)",
             code=_velo(AVG_BODY, WATCH.replace(">= daily", "> daily")), fails_at=2, message_contains="Use `>=`"),
        dict(why="ore_left printed rounded (right for this log; another log leaves halves)",
             code=_velo(AVG_BODY, WATCH.replace("str(ore_left)", "str(round(ore_left))")), fails_at=2,
             message_contains="not rounded"),
        dict(why="ore_left printed once, after the loop (not each pass)",
             code=_velo(AVG_BODY, "while ore_left >= daily:\n    ore_left = ore_left - daily\n"
                                  "print(\"Ore left: \" + str(ore_left))\n"),
             fails_at=2, message_contains="inside the loop"),
        dict(why="a while that stops at a typed 2.0 (right for this log, never ends on another)",
             code=_velo(AVG_BODY, LOOP_FULL.replace("ore_left >= daily", "ore_left != 2.0")), fails_at=2,
             message_contains="never stopped"),
        dict(why="a while loop that counts to a typed 7 (fits this log only)",
             code=_velo(AVG_BODY, LOOP_FULL.replace("ore_left >= daily", "days < 7")), fails_at=2,
             message_contains="Let `ore_left` decide"),
        dict(why="daily typed as 4 (fits this log only)",
             code=_velo(AVG_BODY, WATCH).replace("daily = average(velocite_used)", "daily = 4"), fails_at=2,
             message_contains="average(velocite_used)"),
        dict(why="days never counted", code=_velo(AVG_BODY, WATCH + "print(\"Days left: \" + str(days))\n"),
             fails_at=3, message_contains="`days` is still 0"),
        dict(why="the days print indented inside the loop (prints every pass)",
             code=_velo(AVG_BODY, LOOP_FULL.replace("print(\"Days left", "    print(\"Days left")), fails_at=3,
             message_contains="prints every pass"),
        dict(why="days = 0 reset inside the loop (the count never gets past 1)",
             code=_velo(AVG_BODY, LOOP_FULL.replace("    days = days + 1\n", "    days = 0\n    days = days + 1\n")),
             fails_at=3, message_contains="Move `days = 0` above"),
        dict(why="the while line without its colon",
             code=_velo(AVG_BODY, WATCH.replace("daily:", "daily")), fails_at=0, message_contains="expected ':'"),
        dict(why="days counted outside the loop (adds 1 once)",
             code=_velo(AVG_BODY, WATCH + "days = days + 1\nprint(\"Days left: \" + str(days))\n"), fails_at=3,
             message_contains="Indent `days = days + 1`"),
        dict(why="the days line typed by hand",
             code=_velo(AVG_BODY, LOOP_FULL.replace("print(\"Days left: \" + str(days))", "print(\"Days left: 7\")")),
             fails_at=3, message_contains="typed by hand"),
        dict(why="four typed prints instead of a loop",
             code=_velo(AVG_BODY, LOOP_FULL, "".join(
                 f"print(\"{h['name']} \" + mana_bar(roster[{i}]))\n" for i, h in enumerate(ROSTER_5P))),
             fails_at=4, message_contains="cannot follow a new roster"),
        dict(why="the whole roster printed each pass (the list, not the item)",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    print(roster)\n"), fails_at=4,
             message_contains="whole roster"),
        dict(why="the whole sheet printed each pass",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    print(member)\n"), fails_at=4,
             message_contains="whole sheet"),
        dict(why="roster[\"name\"] for member[\"name\"] (TypeError)",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    print(roster[\"name\"], mana_bar(member))\n"),
             fails_at=0, message_contains="list indices must be integers or slices, not str"),
        dict(why="the item used as an index (roster[member])",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    hero = roster[member]\n"
                                             "    print(hero[\"name\"], mana_bar(hero))\n"),
             fails_at=0, message_contains="not dict"),
        dict(why="the for line without its colon", code=_velo(AVG_BODY, LOOP_FULL, PARTY.replace("roster:", "roster")),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the list's name in quotes: the loop walks the letters of the text roster (TypeError)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY.replace("in roster:", 'in "roster":')), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="mana_bar's own ingredient name handed over in the loop: mana_bar(hero) (NameError)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY.replace("mana_bar(member)", "mana_bar(hero)")), fails_at=0,
             message_contains="'hero' is not defined"),
        dict(why="the loop body not indented",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY.replace("    print(member", "print(member")), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="mana_bar changed (it is already finished)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY).replace("    return \"█\" * mana + \"░\" * used\n",
                                                            "    return \"█\" * mana\n"),
             fails_at=4, message_contains="already finished"),
        dict(why="a roster typed by hand (hides the check's other heroes)",
             code=_velo(AVG_BODY, LOOP_FULL, SETUP_5P + PARTY), fails_at=4, message_contains="ready for you"),
        dict(why="the bar built again by hand in the loop (mana_bar never called)",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    print(member[\"name\"], \"█\" * member[\"mana\"]"
                                             " + \"░\" * (member[\"max_mana\"] - member[\"mana\"]))\n"),
             fails_at=4, message_contains="Call the recipe"),
        dict(why="only the bar printed, no name",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    print(mana_bar(member))\n"), fails_at=4,
             message_contains="same line"),
        dict(why="the print outside the loop (only the last member)",
             code=_velo(AVG_BODY, LOOP_FULL, "for member in roster:\n    bar = mana_bar(member)\n"
                                             "print(member[\"name\"], bar)\n"),
             fails_at=4, message_contains="Only the last member"),
        dict(why="the flag's if outside the loop (checks only the last member)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY + "if member[\"mana\"] < 10:\n"
                                                     "    print(member[\"name\"], \"needs rest\")\n"),
             fails_at=5, message_contains="Outside the loop, it only checks the last member"),
        dict(why="<= 10 (flags Glug's exactly 10 in the rerun roster)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY_FLAG.replace("< 10", "<= 10")),
             fails_at=5, message_contains="exactly 10"),
        dict(why="the two flags typed by hand (right for this roster only)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY + "print(\"Oogrish needs rest\")\nprint(\"Bomb Shell needs rest\")\n"),
             fails_at=5, message_contains="cannot follow a new roster"),
        dict(why="the flag line without the name",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY + "    if member[\"mana\"] < 10:\n        print(\"needs rest\")\n"),
             fails_at=5, message_contains="Put the name"),
        dict(why="max_mana read for the flag (nobody is flagged)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY_FLAG.replace("member[\"mana\"] < 10", "member[\"max_mana\"] < 10")),
             fails_at=5, message_contains="Nobody was flagged"),
        dict(why="the flag in other words (no `needs rest` for the check to find)",
             code=_velo(AVG_BODY, LOOP_FULL, PARTY_FLAG.replace("\"needs rest\"", "\"is tired\"")),
             fails_at=5, message_contains="No line said"),
        dict(why="the filter print outside the loop (the if is inside; only the last tired member prints)",
             code=_velo(AVG_BODY, LOOP_FULL, "tired = \"\"\n" + PARTY + "    if member[\"mana\"] < 10:\n"
                                             "        tired = member[\"name\"]\nprint(tired, \"needs rest\")\n"),
             fails_at=5, message_contains="After the loop, it prints only once"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="for-each,list-of-dicts,accumulate,while-loop,loop-with-if",
             solo="false", dictates="", foreign_names="coin_total,purse,coin,count,fuel,laps,shelf,jar,fill,ore",
             par="([5, 6, 10],),([1, 2],),([8, 2, 1, 3],)") + "\n"
        "Project 5P (SC). Starter: the task-group headers (A, B, C) with numbered comments, the given log, "
        "`average` as a skeleton (teacher ruling on the Unit 6 reviews: `total = 0` and `for value in values:` "
        "given, with `pass  # add value to total` and `return 0  # total / how many` holding the two places) and "
        "the starter's own call `average([2, 4])` (3.0; the intro says to Run it first: it shows 0, and until "
        "`average` works `daily` is 0, so task 2's loop would never end; task 2's Where to look says so too), "
        "`daily = average(velocite_used)` and `days = 0` given, and 5A-07's `mana_bar` already finished "
        "(KEEP: an AST compare). `roster` lives in setup (2.12 rule 3: prebuilt rosters), shown in the intro. "
        "Task 1 PAR with [5, 6, 10], [1, 2], [8, 2, 1, 3] (7.0, 1.5, 3.5: no collision with 3.0 or 4.0, lint b) and "
        "RET; the skeleton left as given, `pass` filled but `return 0` left, `return` filled but `pass` left, the "
        "adding line put below the loop (only the last value) or with four spaces (IndentationError), the reset "
        "inside the loop, `return` inside the loop, a typed divisor, `//`, the list added instead of "
        "the item, `sum()` with no loop, and a loop beside `sum()` that the answer never uses (the loop must change a name the `return` is built from) each get their own message. Tasks 2-3 CMB: reruns with "
        "(log, ore) = ([2, 3, 3, 4], 20), ([1, 2], 6), ([5, 6, 7, 6], 50): 6, 4 and 8 days, and the [1, 2] log lands "
        "exactly on one day's use, so `>` fails (BND). The loop prints `ore_left` each pass, so a missing update "
        "prints forever and the site stops it at the output limit (TooMuchOutput) in under a second; the checks' "
        "own reruns carry a step budget, so no check can hang. Printing `ore_left` before the subtraction passes "
        "too; a rounded print fails on the [1, 2] log (4.5 left) with its own message, and a `while` that stops at a typed value (`!= 2.0`) never ends on that log, which the check names as the question, not the update. Task 3 needs `days` printed after the loop's last watch line, and no `days` print inside the loop "
        "unless one also prints after it (a 'Day 3: 18.0' watch line is fine). Tasks 4-5 LOOP and CMB with a 5-hero "
        "and a 3-hero roster (invented names), Glug at exactly 10 (BND for `<`). The own roster is u06a's night "
        "(6, 14, 3, 22: the same night as 5A-06/5A-07). Task 4 also needs a call of `mana_bar` (the "
        "recipe is reused, not rebuilt). The flag may sit on its own line or the bar's line; a flag in other words "
        "(no `needs rest`), an `if` that flags nobody, and the filter print left below the loop each get their own "
        "message. The side quest (Lucky, old group D) is `break` at the first day over 4, rerun with "
        "[5, 2, 6, 7] (day 1) and [2, 6, 5, 9] (day 2; three days over 4)."
    ),
)



# =============================================================================================
# Challenge "Gearshift's Forecast" (optional, advanced, about 10 min): Mar'tu's forecast, read off the wall
# =============================================================================================

# Write-from-blank (teacher ruling on the Unit 6 reviews, as Units 3 and 4 had): the starter is the real wall and
# one goal comment. Concepts: u06a (`for`, `while`) plus Unit 4's `.append()` and `[-1]`; no `continue`, list
# comprehension or one-line choice (those come in Lesson 5C, after this item).
FC_STARTER = WALL_LINE + "# Goal: forecast the next gaps.\n"
FC_SHRINKS = (
    "shrinks = []\n"
    "for i in range(1, len(chalk_wall)):\n"
    "    shrinks.append(chalk_wall[i - 1] - chalk_wall[i])\n"
    "print(shrinks)\n"
)
FC_START = "gap = chalk_wall[-1]\nshrink = shrinks[-1] + 1\nbursts = 0\n"
FC_WHILE = (
    "while gap > 24:\n"
    "    gap = gap - shrink\n"
    "    shrink = shrink + 1\n"
    "    bursts = bursts + 1\n"
    "    print(gap)\n"
)
FC_COUNT = "print(\"Bursts: \" + str(bursts))\n"


def _fc(shrinks=FC_SHRINKS, start="", loop="", count=""):
    """The challenge program: the starter, then the shrinks, then the forecast's parts (each replaceable)."""
    tail = start + loop + count
    return FC_STARTER + shrinks + ("\n" + tail if tail else "")


FC_SOLUTION = _fc(FC_SHRINKS, FC_START, FC_WHILE, FC_COUNT)
# The real wall forecasts 32, 26, 19: 3 bursts (5B-04's numbers, read off the wall). Gearshift's other wall has
# shrinks 2, 3, 4, 5, so the forecast is 40, 33, 25, 16: 4 bursts (a typed 37, 5 or 3 cannot follow it). The third
# wall's forecast lands on exactly 24 (shrinks 1 to 5: 30 - 6 = 24, 1 burst), so `>=` runs one pass more, to 17.
FC_WALL_B = [60, 58, 55, 51, 46]
FC_WALL_C = [45, 44, 42, 39, 35, 30]
FC_CASES = [None, {"chalk_wall": FC_WALL_B}, {"chalk_wall": FC_WALL_C}]

_FC_RUN = r'''
def _fc_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', __WALL__, ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    assert not _miss, _keep('chalk_wall')
    return _ns, _rows, _err, _vals['chalk_wall'], _ev(_vals)
def _shrinks_of(_w):
    return [_w[_i - 1] - _w[_i] for _i in _B.range(1, _B.len(_w))]
def _forecast(_w, _g=None, _s=None, _grow=1, _ge=False):
    # The forecast gaps: from the newest gap, with a shrink one bigger than the last shrink, while gap > 24.
    _g = _w[-1] if _g is None else _g
    _s = _shrinks_of(_w)[-1] + 1 if _s is None else _s
    _out = []
    while (_g >= 24 if _ge else _g > 24) and _B.len(_out) < 200:
        _g = _g - _s
        _s = _s + _grow
        _out.append(_g)
    return _out
def _rows_of(_rows, _seq):
    # The indexes of the rows that show the numbers of _seq, in order (one per row), or None.
    _at, _hit = 0, []
    for _i, _l in _B.enumerate(_rows):
        if _at < _B.len(_seq) and _B.any(_close(_x, _seq[_at]) for _x in _nums(_l)):
            _hit.append(_i)
            _at = _at + 1
    return _hit if _at == _B.len(_seq) else None
'''

FC_SHRINKS_CHECK = chk(
    "shrinks holds how much each gap shrank, from a loop over the wall",
    _FC_RUN + r'''
_t = _tree()
_own = globals().get('shrinks')
_typed_range = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Call' and _kind(_n.func) == 'Name' and _n.func.id == 'range'
                and _B.any(_kind(_a) == 'Constant' and _kind(_a.value) == 'int' and _a.value > 1 for _a in _n.args)]
for _vals in __CASES__:
    _ns, _rows, _err, _w, _e = _fc_case(_vals)
    _want = _shrinks_of(_w)
    _got = _ns.get('shrinks')
    # A typed range stops Python on a shorter wall after the list is already full: still this step's slip.
    assert not (_err.startswith('IndexError') and _typed_range), (
        'Use `len(chalk_wall)` in the `range`, not a number you typed: another wall can be shorter. With another '
        'wall, Python stopped: ' + _err + '.' + _e)
    if _got == _want:
        # A slip in step 2's lines (they run later) is step 2's to name, not this step's.
        continue
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    if _err.startswith('IndexError'):
        assert False, ('Stop one early: the newest gap has no gap after it. Loop over `range(1, len(chalk_wall))`, '
                       'and take `chalk_wall[i]` from `chalk_wall[i - 1]`. With another wall, Python stopped: '
                       + _err + '.' + _e)
    assert not _err, _stop(_err, _e)
    assert 'shrinks' in _ns, 'Make a list called `shrinks`: start it empty, above the loop.' + _e
    assert _kind(_got) == 'list', ('Keep `shrinks` a list: start it at `[]` above the loop, and `.append()` one '
                                   'shrink each pass. Yours holds ' + _shv(_got) + '.' + _e)
    assert not (_B.len(_want) > 1 and _got == _want[-1:]), (
        'Make `shrinks = []` once, above the `for` line. Inside the loop, the list starts again every pass, so only '
        'the last shrink is left.' + _e)
    assert _got != [-_x for _x in _want], ('Take this gap from the gap before: `chalk_wall[i - 1] - chalk_wall[i]`. '
                                           'Your shrinks came out the other way round.' + _e)
    assert not (_B.len(_got) == _B.len(_want) + 1 and _got[1:] == _want), (
        'Start at 1: `range(1, len(chalk_wall))`. At 0, `chalk_wall[i - 1]` is the newest gap, so your first '
        'shrink compares the two ends of the wall.' + _e)
    assert not (_vals is not None and _got == _own), (
        'Build `shrinks` with a loop over the wall, not typed in the code. With another wall, yours stayed the '
        'same.' + _e)
    assert False, 'Each shrink is the gap before minus this gap. On this wall: ' + _sh(_want) + '.' + _e
_loops = [_n for _n in _ast.walk(_t) if _kind(_n) in ('For', 'While', 'ListComp')]
assert _loops, 'Build `shrinks` with a loop over `range(1, len(chalk_wall))`, one shrink each pass.'
''',
    WALL=WALL,
    CASES=FC_CASES,
)

FC_FORECAST_CHECK = chk(
    "the forecast gaps print, then how many bursts, after the loop",
    _FC_RUN + r'''
_t = _tree()
_whiles = [_n for _n in _ast.walk(_t) if _kind(_n) == 'While']
_ifs = [_n for _n in _ast.walk(_t) if _kind(_n) == 'If']
_in_while = _in_loops(_t, ('While',))
_breaks = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Break' and _B.id(_n) in _in_while]
_zeros = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Assign' and _B.id(_n) in _in_while
          and _kind(_n.value) == 'Constant' and _kind(_n.value.value) == 'int' and _n.value.value == 0]
_WHILE = 'Forecast with a `while` loop: it asks if the gap is more than 24 again before every pass.'
for _vals in __CASES__:
    _ns, _rows, _err, _w, _e = _fc_case(_vals)
    assert _err != 'ENDLESS', ('Make the loop end: take the shrink off the gap every pass, and go on only while the '
                               'gap is more than 24. With another wall, your `while` loop never stopped.' + _e)
    _want = _forecast(_w)
    _n = _B.len(_want)
    _hit = _rows_of(_rows, _want)
    if _hit is None:
        assert not _err, _stop(_err, _e)
        assert _whiles or not _ifs, ('Use `while`, not `if`. `if` asks once, so only one gap was forecast. '
                                     '`while` asks again before every pass.' + _e)
        assert _whiles, _WHILE + _e
        assert not (_breaks and _rows_of(_rows, _want[:1]) is not None), (
            'Take out the `break`: the `while` question already decides when to stop. Your loop stopped after one '
            'pass.' + _e)
        if _vals is not None:
            _typed = [_forecast(_w, _g=__G0__), _forecast(_w, _s=__S0__), _forecast(_w, _g=__G0__, _s=__S0__)]
            assert not [_x for _x in _typed if _rows_of(_rows, _x) is not None], (
                'Read the start from the wall, not typed in the code: the newest gap is `chalk_wall[-1]`, and the '
                'first shrink is one bigger than `shrinks[-1]`.' + _e)
        _last = _shrinks_of(_w)[-1]
        assert _rows_of(_rows, _forecast(_w, _s=_last)) is None, (
            'Start the shrink one bigger than the last shrink: `shrinks[-1] + 1`. Your first gap fell by just the '
            'last shrink, ' + _B.str(_last) + '.' + _e)
        assert _rows_of(_rows, _forecast(_w, _grow=0)) is None, (
            'Make the shrink 1 bigger every pass, inside the loop. Your gaps fell by the same amount each time.' + _e)
        assert _rows_of(_rows, _forecast(_w, _g=_w[0])) is None, (
            'Start from the newest gap, the last one on the wall: `chalk_wall[-1]`. Your forecast started from the '
            'oldest.' + _e)
        assert _rows_of(_rows, [_w[-1]] + _want[:-1]) is None, (
            'Print the gap after you take the shrink off, so each line is a new forecast. Your first line was the '
            'newest gap on the wall.' + _e)
        assert False, ('Print each forecast gap inside the loop, after you take the shrink off. On this wall: '
                       + ', '.join(_B.str(_x) for _x in _want) + '.' + _e)
    _ge = _forecast(_w, _ge=True)
    assert not (_ge != _want and _rows_of(_rows, _ge) is not None), (
        'Use `>`, not `>=`: at exactly 24 hours the forecast stops. Your loop ran one pass too many.' + _e)
    _next = _want[-1] - (_shrinks_of(_w)[-1] + 1 + _n)
    _after = _rows[_hit[-1] + 1:]
    assert not [_l for _l in _after if _nums(_l) and _B.all(_close(_x, _next) for _x in _nums(_l))], (
        'Stop when the gap is 24 or less: the `while` question asks for more than 24. Your loop forecast a gap past '
        'that line.' + _e)
    _between = [_rows[_i] for _i in _B.range(_hit[0], _hit[-1] + 1) if _i not in _hit]
    assert not (_n > 2 and _rows_of(_between, _B.list(_B.range(2, _n))) is not None), (
        'Print the count once, after the loop: take the indent off that print line. Inside the loop, it prints '
        'every pass.' + _e)
    if not [_l for _l in _after if _n in _ints(_l)]:
        assert not (_vals is not None and [_l for _l in _after if __N0__ in _ints(_l)]), (
            'Count the passes inside the loop, so the count follows the wall. Yours is typed in the code: it still '
            'showed ' + _B.str(__N0__) + '.' + _e)
        assert not (_zeros and [_l for _l in _after if 1 in _ints(_l)]), (
            'Set the count to 0 above the `while` line, once. Inside the loop, it starts again every pass, so it '
            'never gets past 1.' + _e)
        assert not [_l for _l in _after if 0 in _ints(_l)], (
            'Add 1 to the count inside the loop, every pass. Your count stayed 0.' + _e)
        assert False, 'After the loop, print how many bursts it forecast: ' + _B.str(_n) + ' here.' + _e
assert _whiles, _WHILE
''',
    WALL=WALL,
    CASES=FC_CASES,
    G0=WALL[-1],
    S0=WALL[-2] - WALL[-1] + 1,
    N0=3,
)

CHALLENGE_FORECAST = dict(
    kind="challenge",
    id="gearshifts-forecast",
    title="Gearshift's Forecast",
    level="advanced",
    optional=True,
    minutes=10,
    support="light",
    summary=(
        "A stretch, from a blank page: build the wall's shrinks with a loop, then let a `while` loop forecast the "
        "bursts."
    ),
    martu=(
        "In Lesson 5B, my forecast started from numbers I typed: `gap = 37` and `shrink = 5`. Gearshift's visor "
        "dimmed. \"Typed numbers go stale. Read them off the wall.\"\n"
        "So, from a blank page. First build `shrinks`, how much each gap shrank, with a loop. Then forecast from "
        "the newest gap, with a shrink one bigger than the last one, and count the bursts.\n"
        "My check tries other walls, only inside the check. So read every number from the wall, yes?"
    ),
    names=["chalk_wall", "shrinks", "gap", "shrink", "bursts"],
    starter=FC_STARTER,
    checkpoints=[
        dict(
            id="build-the-shrinks",
            text="Build `shrinks`, how much each gap shrank, with a loop over `range(1, len(chalk_wall))`.",
            dictated=False,
            hints=[
                "Start under the wall line. `shrinks` begins as an empty list. Then the loop walks positions from 1 "
                "on, so every gap has a gap before it.",
                "Each shrink is the gap before minus this gap: `chalk_wall[i - 1] - chalk_wall[i]`. The range stops "
                "at the newest gap, so `i` never goes one past the end.",
                "With other names:\n```python\nsteps = []\nfor i in range(1, len(hills)):\n"
                "    drop = hills[i - 1] - hills[i]\n    steps.append(drop)\n```\nEach pass adds one drop to the "
                "list.",
                "Write `shrinks = []`, then `for i in range(1, len(chalk_wall)):` with "
                "`shrinks.append(chalk_wall[i - 1] - chalk_wall[i])` under it, four spaces in.",
            ],
            checks=[FC_SHRINKS_CHECK],
            pass_line="Gearshift: Zero, one, one, two, three, four. Read off the wall, not typed. Good.",
        ),
        dict(
            id="forecast-the-bursts",
            text=(
                "Forecast from the newest gap, with `shrink` one bigger than the last shrink: while `gap` is more "
                "than 24, take `shrink` off, make it 1 bigger, and print `gap`. Then print how many bursts it "
                "forecast."
            ),
            dictated=False,
            hints=[
                "Three names come before the loop: `gap` starts at the newest gap, `chalk_wall[-1]`. `shrink` is one "
                "bigger than `shrinks[-1]`. The count starts at 0.",
                "It is Mar'tu's forecast from Lesson 5B, with every start read off the wall. Each pass: take the "
                "shrink off the gap, make the shrink 1 bigger, add 1 to the count, and print the gap.",
                "With other names:\n```python\nfuel = tank[-1]\nburn = 2\ntrips = 0\nwhile fuel > 10:\n"
                "    fuel = fuel - burn\n    burn = burn + 1\n    trips = trips + 1\n    print(fuel)\n"
                "print(trips)\n```\n`fuel` changes every pass, so the loop can end. `trips` prints once, after it.",
                "Write `gap = chalk_wall[-1]` under your shrinks, then:\n```python\nshrink = shrinks[-1] + 1\n"
                "bursts = 0\nwhile gap > 24:\n    gap = gap - shrink\n    shrink = shrink + 1\n"
                "    bursts = bursts + 1\n    print(gap)\nprint(\"Bursts: \" + str(bursts))\n```",
            ],
            checks=[FC_FORECAST_CHECK],
            pass_line="Gearshift: Three bursts, read off the wall itself. The math agrees with Mar'tu. I wish it did not.",
        ),
    ],
    solution=FC_SOLUTION,
    partials=[_fc(FC_SHRINKS)],
    assemble=dict(
        lines=[line for line in FC_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=[
            "    shrinks.append(chalk_wall[i] - chalk_wall[i + 1])",
            "for i in range(len(chalk_wall)):",
            "if gap > 24:",
            "shrink = shrinks[-1]",
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The forecast, pass by pass",
            text=(
                "```text\ngap  shrink  gap > 24?  new gap\n37   5       yes        32\n32   6       yes        26\n"
                "26   7       yes        19\n19   8       no: stop\n```\n"
                "Three passes, so three bursts forecast. The 37 and the 5 come from the wall."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Build `shrinks` from the wall: 0, 1, 1, 2, 3, 4.\n"
                "2. The newest gap is `chalk_wall[-1]`. The last shrink is `shrinks[-1]`, so the first forecast "
                "shrink is one more.\n"
                "3. While the gap is more than 24: take the shrink off, make it 1 bigger, count, print.\n"
                "4. After the loop, print the count, once."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In Lesson 5B, Mar'tu's forecast started from `gap = 37` and `shrink = 5`, typed in. Yours reads both "
                "off the wall, so a new gap on the wall gives a new forecast."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "At the end of the module, Bomb Shell read the wall: *thirty-two hours, maybe less.* Your forecast "
            "reads that first number off the wall itself: the newest gap, 37, take away a shrink of 5."
        ),
    ),
    takeaway=(
        "Read every start from the data: a loop builds the list, and `while` runs the forecast until the line is "
        "crossed."
    ),
    wrong_answers=[
        dict(why="the starter (nothing built yet)", code=FC_STARTER, fails_at=1,
             message_contains="Make a list called `shrinks`"),
        dict(why="neighbors one past the end (wall[i + 1] over the whole range: the loop must stop one early)",
             code=_fc("shrinks = []\nfor i in range(len(chalk_wall)):\n"
                      "    shrinks.append(chalk_wall[i] - chalk_wall[i + 1])\n"), fails_at=0,
             message_contains="index out of range"),
        dict(why="the item used as an index (chalk_wall[gap])",
             code=_fc("shrinks = []\nfor gap in chalk_wall:\n    shrinks.append(chalk_wall[gap - 1] - chalk_wall[gap])\n"),
             fails_at=0, message_contains="index out of range"),
        dict(why="range from 0 (compares the two ends first)",
             code=_fc(FC_SHRINKS.replace("range(1, len(chalk_wall))", "range(len(chalk_wall))")), fails_at=1,
             message_contains="Start at 1"),
        dict(why="this gap minus the one before (the other way round)",
             code=_fc(FC_SHRINKS.replace("chalk_wall[i - 1] - chalk_wall[i]", "chalk_wall[i] - chalk_wall[i - 1]")),
             fails_at=1, message_contains="other way round"),
        dict(why="shrinks = [] reset inside the loop (only the last shrink is left)",
             code=_fc("for i in range(1, len(chalk_wall)):\n    shrinks = []\n"
                      "    shrinks.append(chalk_wall[i - 1] - chalk_wall[i])\nprint(shrinks)\n"), fails_at=1,
             message_contains="Make `shrinks = []` once"),
        dict(why="no .append(): shrinks holds one number",
             code=_fc("for i in range(1, len(chalk_wall)):\n    shrinks = chalk_wall[i - 1] - chalk_wall[i]\n"),
             fails_at=1, message_contains="Keep `shrinks` a list"),
        dict(why="the shrinks typed by hand (right for this wall only)", code=_fc("shrinks = [0, 1, 1, 2, 3, 4]\n"),
             fails_at=1, message_contains="typed in the code"),
        dict(why="the range typed for 7 gaps (another wall is shorter)",
             code=_fc(FC_SHRINKS.replace("range(1, len(chalk_wall))", "range(1, 7)")), fails_at=1,
             message_contains="not a number you typed"),
        dict(why="the for line without its colon",
             code=_fc(FC_SHRINKS.replace("len(chalk_wall)):", "len(chalk_wall))")), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the hint's list name copied (hills)",
             code=_fc("steps = []\nfor i in range(1, len(hills)):\n    steps.append(hills[i - 1] - hills[i])\n"),
             fails_at=0, message_contains="not defined"),
        dict(why="task 1 done, no forecast yet", code=_fc(FC_SHRINKS), fails_at=2, message_contains="`while` loop"),
        dict(why="a while loop with no update (prints 37 forever: the output limit stops it)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("    gap = gap - shrink\n", ""), FC_COUNT), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update outside the loop (prints forever)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("    gap = gap - shrink\n", ""),
                      "gap = gap - shrink\n" + FC_COUNT), fails_at=0, message_contains="printed more than"),
        dict(why="if instead of while (asks once: one gap)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("while gap", "if gap"), FC_COUNT), fails_at=2,
             message_contains="Use `while`, not `if`"),
        dict(why="the while line without its colon",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("> 24:", "> 24"), FC_COUNT), fails_at=0,
             message_contains="expected ':'"),
        dict(why="break inside the while (stops after one pass)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE + "    break\n", FC_COUNT), fails_at=2,
             message_contains="Take out the `break`"),
        dict(why="the newest gap typed as 37 (right for this wall only)",
             code=_fc(FC_SHRINKS, FC_START.replace("chalk_wall[-1]", "37"), FC_WHILE, FC_COUNT), fails_at=2,
             message_contains="typed in the code"),
        dict(why="the first shrink typed as 5 (right for this wall only)",
             code=_fc(FC_SHRINKS, FC_START.replace("shrinks[-1] + 1", "5"), FC_WHILE, FC_COUNT), fails_at=2,
             message_contains="typed in the code"),
        dict(why="the count typed as 3 (right for this wall only)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE, "print(\"Bursts: 3\")\n"), fails_at=2,
             message_contains="typed in the code"),
        dict(why="the shrink starts at the last shrink, not one bigger",
             code=_fc(FC_SHRINKS, FC_START.replace("shrinks[-1] + 1", "shrinks[-1]"), FC_WHILE, FC_COUNT),
             fails_at=2, message_contains="one bigger than the last shrink"),
        dict(why="the shrink never grows",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("    shrink = shrink + 1\n", ""), FC_COUNT), fails_at=2,
             message_contains="1 bigger every pass"),
        dict(why="the forecast starts from the oldest gap",
             code=_fc(FC_SHRINKS, FC_START.replace("chalk_wall[-1]", "chalk_wall[0]"), FC_WHILE, FC_COUNT),
             fails_at=2, message_contains="newest gap"),
        dict(why="the gap printed before the shrink comes off",
             code=_fc(FC_SHRINKS, FC_START, "while gap > 24:\n    print(gap)\n    gap = gap - shrink\n"
                                            "    shrink = shrink + 1\n    bursts = bursts + 1\n", FC_COUNT),
             fails_at=2, message_contains="after you take the shrink off"),
        dict(why=">= 24 (the third wall lands on exactly 24: one pass too many)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("> 24", ">= 24"), FC_COUNT), fails_at=2,
             message_contains="Use `>`, not `>=`"),
        dict(why="while gap > 0 (forecasts past the line)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("> 24", "> 0"), FC_COUNT), fails_at=2,
             message_contains="past that line"),
        dict(why="the count printed inside the loop (every pass)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE + "    " + FC_COUNT), fails_at=2,
             message_contains="prints every pass"),
        dict(why="the count reset inside the loop (never gets past 1)",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("    bursts = bursts + 1\n",
                                                             "    bursts = 0\n    bursts = bursts + 1\n"), FC_COUNT),
             fails_at=2, message_contains="never gets past 1"),
        dict(why="the count never grows",
             code=_fc(FC_SHRINKS, FC_START, FC_WHILE.replace("    bursts = bursts + 1\n", ""), FC_COUNT), fails_at=2,
             message_contains="Your count stayed 0"),
    ],
    notes=(
        meta(starter_level="S0", path="optional", skills="neighbors,while-loop,accumulate", solo="false",
             dictates="", foreign_names="hills,steps,drop,fuel,tank,burn,trips") + "\n"
        "Optional advanced challenge for the ready-to-stretch group (teacher ruling on the Unit 6 reviews: honest "
        "practice for the stronger groups, a write-from-blank task as Units 3 and 4 had; it costs no one core "
        "time). Placed after the project, as Units 3 and 4 placed theirs. Starter: the real wall line (41 "
        "characters, the Unit 4 exception) and one goal comment. CP1 [ND] builds `shrinks` with a loop over "
        "`range(1, len(chalk_wall))` (any loop that follows the wall passes, a comprehension too). CP2 [ND] is "
        "5B-04's forecast with every start read off the wall: from `chalk_wall[-1]`, with a shrink one bigger than "
        "`shrinks[-1]`; while the gap is more than 24, take the shrink off, grow it by 1, print the gap; then print "
        "the count. On the real wall it prints 32, 26, 19 and then 3 (5B-04's numbers). Reruns with "
        "[60, 58, 55, 51, 46] (shrinks 2, 3, 4, 5; 40, 33, 25, 16; 4 bursts), so a typed 37, 5, shrink list or "
        "count fails ('typed in the code'), and with [45, 44, 42, 39, 35, 30] (30 - 6 lands on exactly 24: `>=` "
        "runs one pass more, BND). Each pass prints, so a missing update prints forever and stops fast at the "
        "output limit (TooMuchOutput); the checks' own reruns carry the step budget. Caught: neighbors one past "
        "the end (`chalk_wall[i + 1]`, IndexError), the item as an index, a range from 0, the other way round, "
        "the list reset inside the loop, no `.append()`, a typed range, a missing colon, the hint's `hills`; no "
        "update (or the update outside the loop), `if` for `while`, `break` inside the loop, the shrink not one "
        "bigger or never growing, the oldest gap, the print above the take-away, `>=`, `> 0`, the count printed "
        "every pass, reset inside the loop or never grown. Concepts: u06a plus Unit 4's `.append()` and `[-1]`."
    ),
)


# =============================================================================================
# Extra practice 6X "Loops That End" (pool): 5B-05 broken-spell-5b
# =============================================================================================

COUNT_STARTER = (
    "# Mar'tu's countdown to the burst.\n"
    "hours_left = 5\n"
    "while hours_left > 1:\n"
    "    print(hours_left)\n"
    "    hours_left = hours_left + 1\n"
    "print(\"Burst!\")\n"
)


def _count(cond="hours_left > 1", update="    hours_left = hours_left + 1\n", body=None, extra=""):
    """The countdown with its `while` question and its update line swapped in."""
    inner = body if body is not None else "    print(hours_left)\n" + update
    return ("# Mar'tu's countdown to the burst.\n" "hours_left = 5\n" "while " + cond + ":\n" + inner + extra
            + "print(\"Burst!\")\n")


COUNT_DOWN = "    hours_left = hours_left - 1\n"
COUNT_SOLUTION = _count("hours_left > 0", COUNT_DOWN)

_HOURS = r'''
def _hours_case(_start):
    if _start is None:
        return _lines(), '', 5, ''
    _ns, _rows, _err, _miss = _rerun({'hours_left': _start})
    assert not _miss, _keep('hours_left')
    return _rows, _err, _start, _ev({'hours_left': _start})
def _before_burst(_rows):
    _b = [_i for _i, _l in _B.enumerate(_rows) if 'burst' in _l.lower()]
    assert _b, 'Keep `print("Burst!")` from the starter, after the loop.'
    return [_ints(_l)[0] for _l in _rows[:_b[0]] if _ints(_l)]
def _typed_hours():
    # prints of a typed whole number, or prints of the hours outside the loop (both show an hour the loop never
    # decided on).
    # One parse: _in_loops keeps node ids, so the prints must come from the same tree.
    _t = _tree()
    _inside = _in_loops(_t)
    _out = []
    for _n in _prints(_t):
        _num = _n.args and _kind(_n.args[0]) == 'Constant' and _kind(_n.args[0].value) == 'int'
        if _num or (_B.id(_n) not in _inside and _mentions(_n, 'hours_left')):
            _out.append(_n)
    return _out
'''

GOES_DOWN = chk(
    "the hours go down by 1 and the loop ends",
    _HOURS + r'''
_whiles = [_n for _n in _ast.walk(_tree()) if _kind(_n) == 'While']
_ifs = [_n for _n in _ast.walk(_tree()) if _kind(_n) == 'If' and _mentions(_n.test, 'hours_left')]
for _start in __STARTS__:
    _rows, _err, _s, _e = _hours_case(_start)
    assert _err != 'ENDLESS', ('Make the hours go down each pass: `hours_left = hours_left - 1`. Your loop never '
                               'stopped.' + _e)
    assert not _err, _stop(_err, _e)
    _hrs = _before_burst(_rows)
    _steps = [_hrs[_i + 1] - _hrs[_i] for _i in _B.range(_B.len(_hrs) - 1)]
    # From the start (or one below it), down by 1, with at least the hours a `> 1` countdown shows.
    if (_hrs and _hrs[0] in (_s, _s - 1) and _B.all(_x == -1 for _x in _steps)
            and _B.len(_hrs) >= _s - 1):
        continue
    assert not (_steps and _B.all(_x > 0 for _x in _steps)), (
        'This is a countdown: take 1 away each pass, `hours_left = hours_left - 1`. Your hours went up.' + _e)
    assert not (_B.len(_hrs) == 1 and not _whiles and _ifs), (
        'Use `while`, not `if`. `if` asks once, so only one hour printed. `while` asks again before every '
        'pass.' + _e)
    assert not (_start is not None and ((_hrs and _hrs[0] == 5) or _typed_hours())), (
        'Let the loop count from `hours_left`, so it follows the start. Your lines show hours typed by hand.' + _e)
    assert not (_steps and _B.all(_x < 0 for _x in _steps)), (
        'Take away 1 each pass: `hours_left - 1`. Your countdown jumped from ' + _B.str(_hrs[0]) + ' to '
        + _B.str(_hrs[1]) + '.' + _e)
    assert not (_hrs and _B.all(_x == -1 for _x in _steps) and _hrs[0] in (_s, _s - 1)), (
        'Let the countdown run all the way down. It printed only ' + _B.str(_B.len(_hrs)) + ' hours, from '
        + _B.str(_hrs[0]) + '.' + _e)
    assert False, ('Print `hours_left` inside the loop, each pass, counting down from ' + _B.str(_s) + '.' + _e)
''',
    STARTS=[None, 8, 3],
)

SHOWS_ONE = chk(
    "the countdown shows 1, then Burst!",
    _HOURS + r'''
# An hour printed by hand, or by a print outside the loop (even one that only prints at the right moment), is a
# patch: the step is to mend the `while` line.
assert not _typed_hours(), (
    'Let the `while` line decide when to stop: mend line 3 itself. An hour printed by hand, or by a print outside '
    'the loop, does not come from the countdown.')
for _start in __STARTS__:
    _rows, _err, _s, _e = _hours_case(_start)
    assert _err != 'ENDLESS', 'Make sure the loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _hrs = _before_burst(_rows)
    _want = _B.list(_B.range(_s, 0, -1))
    if _hrs == _want:
        continue
    assert not (_want and _hrs == _want[:-1]), ('Let the countdown reach 1: `while hours_left > 0:`. It stopped '
                                                'before 1.' + _e)
    assert _hrs != _want + [0], 'Stop before 0: use `> 0`, not `>= 0`. Your countdown printed 0.' + _e
    assert not (_hrs and _hrs == [_x - 1 for _x in _want]), (
        'Print `hours_left` first, then take 1 away. Your countdown started at ' + _B.str(_hrs[0]) + ', not '
        + _B.str(_s) + '.' + _e)
    assert False, ('The countdown should show ' + ', '.join(_B.str(_x) for _x in _want) + ', then Burst!.' + _e)
''',
    STARTS=[None, 3, 1, 0],
)

BROKEN_5B = dict(
    id="broken-spell-5b",
    title="Broken spell",
    martu=(
        "My countdown to the burst. It should say 5, 4, 3, 2, 1, then Burst!. It does not.\n"
        "Two slips. Run it first and watch. [[infinite loop|A loop that never ends]] is no disaster: the site stops "
        "it for you. Then mend line 5, Run again, and count what it prints."
    ),
    names=["hours_left"],
    predict=dict(
        q="Before you Run the spell: what does this print?",
        code="hours_left = 5\nhours_left = hours_left + 1\nprint(hours_left)\n",
        choices=["4", "6", "5"],
        answer=1,
        explain=(
            "`+ 1` makes it bigger: 6. In the spell, `hours_left` grows every pass, so `hours_left > 1` stays True "
            "and the loop never ends."
        ),
    ),
    starter=COUNT_STARTER,
    checkpoints=[
        dict(
            id="count-down",
            text="Mend line 5 so the hours go down each pass, and the loop can end.",
            dictated=False,
            hints=[
                "Read the last line of the console: the program printed so much that it was stopped. Look at the "
                "numbers it printed. Which way do they go?",
                "Line 5 is the update: the line that changes what the `while` question asks about. Here it makes "
                "the hours bigger, so `hours_left > 1` is True forever.",
                "With other names: `steps = steps - 1` takes one step off each pass.",
                "Write `hours_left = hours_left - 1` in place of `hours_left = hours_left + 1`.",
            ],
            checks=[GOES_DOWN],
            pass_line="Mar'tu: Down it goes. Good. Now count.",
        ),
        dict(
            id="show-the-one",
            text="Mend line 3 so the countdown shows 1, then stops.",
            dictated=False,
            hints=[
                "Read what the program printed. Which hour is missing before `Burst!`?",
                "Line 3 asks `hours_left > 1`. When `hours_left` is 1, is 1 bigger than 1?",
                "With other names: `while steps > 0:` keeps going down to 1, and stops before 0.",
                "Write `while hours_left > 0:` in place of `while hours_left > 1:`.",
            ],
            checks=[SHOWS_ONE],
            pass_line="Bomb Shell: Five. Four. Three. Two. One. Shield up.",
        ),
    ],
    solution=COUNT_SOLUTION,
    partials=[_count(update=COUNT_DOWN)],
    assemble=dict(
        lines=[line for line in COUNT_SOLUTION.splitlines() if not line.startswith("#")],
        distractors=["    hours_left = hours_left + 1", "while hours_left > 1:", "while hours_left >= 0:"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="What the loop asks",
            text=(
                "```text\nhours  > 1 ?  > 0 ?\n5      yes    yes\n...\n2      yes    yes\n1      no     yes\n"
                "0      no     no\n```\n"
                "With `> 1`, the loop stops before 1 can print. With `> 0`, it prints 1 and stops at 0."
            ),
        ),
        dict(
            angle="everyday",
            label="A rocket launch",
            text=(
                "Five, four, three, two, one, go. If you count *up* from five, you never reach go. If you stop at "
                "two, the crowd waits forever for the one."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Run. The numbers grow: 5, 6, 7 ... The update goes the wrong way.\n"
                "2. Line 5: `- 1`, not `+ 1`.\n"
                "3. Run again: 5, 4, 3, 2, Burst!. The 1 is missing.\n"
                "4. Line 3: ask `> 0`, so 1 still gets its pass."
            ),
        ),
        dict(
            angle="in Tor",
            label="The Ley Clock",
            text=(
                "The Ley Clock's hand only moves one way: toward the burst. A countdown is the same. Every pass "
                "takes an hour off, and the last hour still counts."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "Thirty-two hours to the next burst, by the chalk wall's count. A countdown that never ends is a clock "
            "that never rings, and one that stops early rings an hour late."
        ),
    ),
    takeaway="A `while` loop needs an update that moves toward the end. Check the last pass: `> 0` still shows 1.",
    wrong_answers=[
        dict(why="the starter: the update moves the wrong way (prints forever, stopped by the output limit)",
             code=COUNT_STARTER, fails_at=0, message_contains="printed more than"),
        dict(why="no update at all (prints forever)", code=_count(update=""), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update outside the loop (prints forever)",
             code=_count(update="", extra="hours_left = hours_left - 1\n"), fails_at=0,
             message_contains="printed more than"),
        dict(why="the update with no `hours_left =` (worked out, then kept nowhere: prints forever)",
             code=_count(update="    hours_left - 1\n"), fails_at=0, message_contains="printed more than"),
        dict(why="takes away 2", code=_count(update="    hours_left = hours_left - 2\n"), fails_at=1,
             message_contains="jumped from 5 to 3"),
        dict(why="the question flipped instead, so it counts up", code=_count("hours_left < 9"), fails_at=1,
             message_contains="Your hours went up"),
        dict(why="the countdown typed by hand",
             code="hours_left = 5\nprint(5)\nprint(4)\nprint(3)\nprint(2)\nprint(1)\nprint(\"Burst!\")\n",
             fails_at=1, message_contains="typed by hand"),
        dict(why="if instead of while (asks once: one hour)",
             code=_count("hours_left > 0", COUNT_DOWN).replace("while hours_left", "if hours_left"), fails_at=1,
             message_contains="Use `while`, not `if`"),
        dict(why="only line 5 mended: off by one, 1 never shows", code=_count(update=COUNT_DOWN), fails_at=2,
             message_contains="reach 1"),
        dict(why=">= 0 (prints 0 too)", code=_count("hours_left >= 0", COUNT_DOWN), fails_at=2,
             message_contains="printed 0"),
        dict(why="a print(1) typed after the loop instead of mending line 3",
             code=_count(update=COUNT_DOWN, extra="print(1)\n"), fails_at=2, message_contains="decide when to stop"),
        dict(why="a patch after the loop (`if hours_left == 1:` prints it) instead of mending line 3",
             code=_count(update=COUNT_DOWN, extra="if hours_left == 1:\n    print(hours_left)\n"), fails_at=2,
             message_contains="mend line 3 itself"),
        dict(why="update before the print (starts at 4)",
             code=_count("hours_left > 0", body="    hours_left = hours_left - 1\n    print(hours_left)\n"),
             fails_at=2, message_contains="started at 4"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="while-loop,read-traceback", solo="false", dictates="",
             foreign_names="steps") + "\n"
        "5B-05 (pool). Two bugs, one checkpoint each: an update that moves the wrong way (`+ 1`: a loud bug, the "
        "loop prints forever and the site stops it at the output limit, TooMuchOutput, 'Printing forever?'), and "
        "a countdown off by one (`> 1`: a quiet bug, 1 never shows). CP1 also needs the countdown to run (an `if` in place of `while` prints one hour: named). CP2 refuses a patch (a typed hour, or a print outside the loop, even one under `if hours_left == 1:` that prints at the right moment): the step is to mend line 3. The predict shows `+ 1` on its own, so it "
        "never runs the endless loop. CP1 reruns with `hours_left = 8` and `= 3`: the hours must go down by 1 from "
        "the start (or from one below it, which CP2 then names), so a typed countdown fails. CP2 reruns with 3, 1 "
        "and 0: only `Burst!` shows for 0, so a `print(1)` typed after the loop fails. `> 0`, `>= 1` and `!= 0` "
        "all pass. Every endless-loop wrong answer prints each pass, so the harness meets the output limit in "
        "well under a second."
    ),
)

EXTRA_6X = dict(
    kind="lesson",
    id="extra-loops-that-end",
    title="Extra practice: Loops That End",
    optional=True,
    minutes=3,
    summary="Mend a countdown whose update runs the wrong way, and that stops one hour short.",
    notes="6X pool (5B-05). Optional; feeds twins, the spaced queue and early finishers.",
    exercises=[BROKEN_5B],
)


# =============================================================================================
# Lesson 5C "Loops in One Line" (optional, 20 min)
# =============================================================================================

# ---- 5C-01 skip-the-empty -------------------------------------------------------------------------------------

ROSTER_5C1 = [
    {"name": "Oogrish", "mana": 6, "max_mana": 18},
    {"name": "Gearshift", "mana": 0, "max_mana": 20},
    {"name": "Bomb Shell", "mana": 11, "max_mana": 24},
    {"name": "Lucky", "mana": 0, "max_mana": 26},
]
SETUP_5C1 = _sheet_lines(ROSTER_5C1)
# Reruns: the first hero is empty in A (a `break` sends nobody), and the last in B.
ROSTER_5C1_A = [
    {"name": "Pell", "mana": 0, "max_mana": 12},
    {"name": "Moss", "mana": 4, "max_mana": 20},
    {"name": "Brakka", "mana": 0, "max_mana": 15},
    {"name": "Glug", "mana": 7, "max_mana": 10},
    {"name": "Tester", "mana": 2, "max_mana": 14},
]
ROSTER_5C1_B = [
    {"name": "Zelda", "mana": 5, "max_mana": 9},
    {"name": "Kratos", "mana": 0, "max_mana": 16},
]

SKIP_HEAD = "# roster is ready for you.\nfor member in roster:\n    # Skip anyone with 0 mana.\n"
SKIP_PRINT = "    print(\"Send \" + member[\"name\"])\n"
SKIP_STARTER = SKIP_HEAD + SKIP_PRINT
SKIP_IF = "    if member[\"mana\"] == 0:\n        continue\n"
SKIP_SOLUTION = SKIP_HEAD + SKIP_IF + SKIP_PRINT


def _skip(middle, tail=SKIP_PRINT):
    return SKIP_HEAD + middle + tail


SEND_CHECK = chk(
    "only heroes with mana are sent",
    r'''
_t = _tree()
_cont = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Continue']
_brk = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Break']
def _late():
    for _f in _ast.walk(_t):
        if _kind(_f) != 'For':
            continue
        _c = [_i for _i, _x in _B.enumerate(_f.body) if _B.any(_kind(_y) == 'Continue' for _y in _ast.walk(_x))]
        _p = [_i for _i, _x in _B.enumerate(_f.body) if _prints(_x)]
        if _c and _p and _c[0] > _p[0]:
            return True
    return False
_own_names = [_h['name'] for _h in __OWN__]
for _ros, _note in __CASES__:
    if _ros is None:
        _rows, _err, _ros, _e = _lines(), '', __OWN__, ''
    else:
        _ns, _rows, _err, _miss = _rerun(None, _ros)
        _e = _ev(None, _note)
    assert _err != 'ENDLESS', 'Make sure the loop can end.' + _e
    assert not _err, _stop(_err, _e)
    assert not [_l for _l in _rows if _l.startswith('{') or _l.startswith('[')], (
        'Send each hero by name: `"Send " + member["name"]`. Your loop printed whole sheets, brackets and all.' + _e)
    # When the lines say "Send", only those lines send: a "Gearshift rests" line for a skipped hero is fine.
    _send_rows = [_l for _l in _rows if 'send' in _l.lower()] or _rows
    _sent = [_h['name'] for _l in _send_rows for _h in _ros if _h['name'].lower() in _l.lower()]
    _want = [_h['name'] for _h in _ros if _h['mana'] != 0]
    if _sent == _want:
        continue
    _mine = [_x for _x in _own_names if _x not in [_h['name'] for _h in _ros]]
    assert not (_e and [_l for _l in _rows if _B.any(_x.lower() in _l.lower() for _x in _mine)]), (
        'Let the loop send each member. Names typed by hand cannot follow a new roster.' + _e)
    _zero = [_i for _i, _h in _B.enumerate(_ros) if _h['mana'] == 0]
    assert not (_brk and _zero and _sent == [_h['name'] for _h in _ros[:_zero[0]]]), (
        'Use `continue`, not `break`. `break` leaves the whole loop, so nobody after the first empty hero was sent. '
        '`continue` skips just that one.' + _e)
    assert not (_cont and not _sent and _want), (
        'Put `continue` under an `if` that asks about the mana, one indent further in. Right now it runs every '
        'pass, so everyone was skipped.' + _e)
    if [_h for _h in _ros if _h['mana'] == 0 and _h['name'] in _sent]:
        assert not (_cont and _late()), ('Put the `if` and `continue` above the print. Below it, the skip comes too '
                                         'late: the name is already printed.' + _e)
        assert False, ('Skip anyone with 0 mana: above the print, `if member["mana"] == 0:` with `continue` under '
                       'it. A member with 0 mana was sent.' + _e)
    assert False, 'Send every member who has mana: skip only when `member["mana"]` is 0.' + _e
''',
    setup=SETUP_5C1,
    OWN=ROSTER_5C1,
    CASES=[(None, ""), (ROSTER_5C1_A, "a roster of 5 other heroes"), (ROSTER_5C1_B, "a roster of 2 other heroes")],
)

USES_CONTINUE = (
    "the skip uses continue",
    "assert 'node:Continue' in _concept_tokens(_source), ('This step is for `continue`: put `continue` under the "
    "`if`, and keep the print below it. An `if` around the print works too, but today we meet `continue`.')\n"
    "import ast as _ast\n"
    "import builtins as _B\n"
    "_tr = _ast.parse(_source)\n"
    "_in_if = _B.set(_B.id(_x) for _n in _ast.walk(_tr) if _B.type(_n).__name__ == 'If' "
    "for _part in _n.body + _n.orelse for _x in _ast.walk(_part))\n"
    "_cs = [_n for _n in _ast.walk(_tr) if _B.type(_n).__name__ == 'Continue']\n"
    "assert [_n for _n in _cs if _B.id(_n) in _in_if], ('Put `continue` under the `if` that asks about the mana, so "
    "it skips only the empty heroes. Outside an `if`, it skips nothing useful.')",
)

SKIP_THE_EMPTY = dict(
    id="skip-the-empty",
    title="Skip the empty",
    martu=(
        "A long night. Two of you have no mana left. I send the others to the barrier, and the empty ones rest.\n"
        "[[continue|`continue`]] skips the rest of this pass and goes on to the next member. `break` leaves the whole loop; "
        "`continue` only skips one pass. It goes under an `if`, so only some members are skipped."
    ),
    introduces=["node:Continue"],
    example=(
        "lanterns = [3, 0, 5]\n"
        "for oil in lanterns:\n"
        "    if oil == 0:\n"
        "        continue\n"
        "    print(\"Light it: \" + str(oil))\n"
    ),
    example_output="Light it: 3\nLight it: 5",
    names=["roster", "member"],
    predict=dict(
        q="Before you press Run: what does this print?",
        code="for n in [3, 0, 5]:\n    if n == 0:\n        continue\n    print(n)\n",
        choices=["3\n5", "3", "3\n0\n5"],
        answer=0,
        explain="At 0, `continue` skips the print and goes on to 5. `break` would have stopped at 0, leaving only 3.",
    ),
    setup=SETUP_5C1,
    starter=SKIP_STARTER,
    checkpoints=[
        dict(
            id="skip-with-continue",
            text="Skip anyone with 0 mana, with `continue`, so only heroes with mana are sent.",
            dictated=False,
            hints=[
                "Look at the comment inside the loop. The skip goes there: above the print, so the print never runs "
                "for an empty hero.",
                "An `if` asks about this member's mana. Under it, indented, `continue` jumps to the next member.",
                "With other names:\n```python\nfor oil in lanterns:\n    if oil == 0:\n        continue\n"
                "    print(oil)\n```\nAn empty lantern is skipped, so its print never runs.",
                "Write `if member[\"mana\"] == 0:` above the print, with `continue` under it, indented.",
            ],
            checks=[SEND_CHECK, USES_CONTINUE],
            pass_line="Mar'tu: Gearshift and Lucky rest. The rest of you, to the barrier.",
        ),
    ],
    solution=SKIP_SOLUTION,
    assemble=dict(
        lines=["for member in roster:", "    if member[\"mana\"] == 0:", "        continue",
               "    print(\"Send \" + member[\"name\"])"],
        distractors=["        break", "    if roster[\"mana\"] == 0:", "    if member[\"mana\"] = 0:"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Down the line",
            text=(
                "```text\nOogrish     6  send\nGearshift   0  skip\nBomb Shell 11  send\nLucky       0  skip\n```\n"
                "`continue` is the *skip*: that pass ends early, and the loop goes on."
            ),
        ),
        dict(
            angle="everyday",
            label="Handing out lanterns",
            text=(
                "You walk along a shelf of lanterns. An empty one? Skip it and go on to the next. You don't go home "
                "at the first empty one: that would be `break`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `member` is Oogrish: 6 is not 0, so print.\n"
                "2. `member` is Gearshift: 0 is 0, so `continue`. The print is skipped.\n"
                "3. Bomb Shell: print. 4. Lucky: skip."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet="elif caster[\"mana\"] < spell[\"mana_cost\"]:",
        why=(
            "Holding the barrier, a caster without enough mana could not cast. A loop over the party can skip "
            "them the same way, and go on to the next caster."
        ),
    ),
    takeaway="`continue` skips the rest of this pass and goes on to the next item. `break` leaves the loop.",
    wrong_answers=[
        dict(why="the starter (nobody skipped)", code=SKIP_STARTER, fails_at=1, message_contains="0 mana was sent"),
        dict(why="break where continue belongs", code=_skip("    if member[\"mana\"] == 0:\n        break\n"),
             fails_at=1, message_contains="not `break`"),
        dict(why="continue outside its if (runs every pass)",
             code=_skip("    if member[\"mana\"] == 0:\n        pass\n    continue\n"), fails_at=1,
             message_contains="runs every pass"),
        dict(why="continue under the if, but below the print (too late)",
             code=SKIP_HEAD + SKIP_PRINT + SKIP_IF, fails_at=1, message_contains="too late"),
        dict(why="an if around the print, and a continue at the end that skips nothing",
             code=SKIP_HEAD + "    if member[\"mana\"] != 0:\n        print(\"Send \" + member[\"name\"])\n    continue\n",
             fails_at=1, message_contains="Outside an `if`"),
        dict(why="an if around the print, no continue (works, but this step meets continue)",
             code=_skip("    if member[\"mana\"] != 0:\n    ", SKIP_PRINT.replace("    print", "    print")),
             fails_at=1, message_contains="This step is for `continue`"),
        dict(why="continue not indented under the if", code=_skip("    if member[\"mana\"] == 0:\n    continue\n"),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="= for == in the if", code=_skip("    if member[\"mana\"] = 0:\n        continue\n"), fails_at=0,
             message_contains="Maybe you meant '=='"),
        dict(why="roster[\"mana\"] for member[\"mana\"]", code=_skip("    if roster[\"mana\"] == 0:\n        continue\n"),
             fails_at=0, message_contains="not str"),
        dict(why="the if without its colon", code=_skip("    if member[\"mana\"] == 0\n        continue\n"),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the example's list name copied",
             code="for oil in lanterns:\n    if oil == 0:\n        continue\n    print(\"Send \" + oil)\n",
             fails_at=0, message_contains="not defined"),
        dict(why="the two names typed by hand",
             code="print(\"Send Oogrish\")\nprint(\"Send Bomb Shell\")\n", fails_at=1,
             message_contains="cannot follow a new roster"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="continue,loop-with-if", solo="false", dictates="",
             foreign_names="lanterns,oil,n") + "\n"
        "5C-01 (O). Intro node:Continue. The roster (after the long night: 6, 0, 11, 0) lives in setup, as in 5A-03. "
        "CP1 [ND] reruns with a 5-hero roster whose FIRST hero is empty (a `break` sends nobody) and a 2-hero roster "
        "whose LAST is empty. When the lines say 'Send', only those lines count, so a 'Gearshift rests' line for a "
        "skipped hero passes. Caught: `break` for `continue`, `continue` outside its `if`, the skip below the print, "
        "an `if` with no `continue` (right output, but the step meets `continue`: a second check names it), a "
        "`continue` outside any `if` (it skips nothing), "
        "`roster[\"mana\"]`, `=` for `==`, a missing colon or indent, the example's `lanterns`, typed names."
    ),
)

# ---- 5C-02 loops-in-loops -------------------------------------------------------------------------------------

TRAINING = [[7, 5, 9], [8, 6, 9], [9, 7, 10]]
TRAIN_HEAD = (
    "# Oogrish's training log: one row\n"
    "# a morning, one score a drill.\n"
    "training = [\n"
    "    [7, 5, 9],\n"
    "    [8, 6, 9],\n"
    "    [9, 7, 10],\n"
    "]\n"
)
TRAIN_STARTER = TRAIN_HEAD + "for row in training:\n    print(row)\n"
TRAIN_LOOPS = "for row in training:\n    for score in row:\n        print(score)\n"
TRAIN_SOLUTION = TRAIN_HEAD + TRAIN_LOOPS
TRAIN_BONUS = TRAIN_HEAD + (
    "for row in training:\n"
    "    total = 0\n"
    "    for score in row:\n"
    "        print(score)\n"
    "        total = total + score\n"
    "    print(\"Total: \" + str(total))\n"
)
TRAIN_CASES = [None, {"training": [[1, 2], [3, 4], [5, 6], [11, 12]]}, {"training": [[20, 21, 22, 23]]}]

_TRAIN_RUN = r'''
def _train_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', __OWN__, ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    assert not _miss, _keep('training')
    return _ns, _rows, _err, _vals['training'], _ev(None, 'a log of ' + _B.str(_B.len(_vals['training']))
                                                     + (' other rows' if _B.len(_vals['training']) > 1 else ' other row'))
def _subseq(_xs, _seq):
    _at = 0
    for _x in _xs:
        if _at < _B.len(_seq) and _x == _seq[_at]:
            _at = _at + 1
    return _at == _B.len(_seq)
'''

EVERY_SCORE = chk(
    "every score prints on its own line, row by row",
    _TRAIN_RUN + r'''
_t = _tree()
_fors = [_n for _n in _ast.walk(_t) if _kind(_n) == 'For']
_inner = [_x for _f in _fors for _part in _f.body for _x in _ast.walk(_part) if _kind(_x) == 'For']
_typed_range = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Call' and _kind(_n.func) == 'Name' and _n.func.id == 'range'
                and _B.any(_kind(_a) == 'Constant' and _kind(_a.value) == 'int' and _a.value > 1 for _a in _n.args)]
for _vals in __CASES__:
    _ns, _rows, _err, _log, _e = _train_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not (_err.startswith('IndexError') and _typed_range), (
        'Let the loops walk the lists themselves: `for row in training:`, then `for score in row:`. A number typed '
        'in `range()` fits this log only. With another log, Python stopped: ' + _err + '.' + _e)
    assert not (_err.startswith('IndexError') and not _inner), (
        'Put a second `for` inside the first, `for score in row:`, and print each `score`. Reading `row[0]`, '
        '`row[1]` and `row[2]` fits rows of 3 scores only. With another log, Python stopped: ' + _err + '.' + _e)
    assert not _err, _stop(_err, _e)
    _flat = [_x for _row in _log for _x in _row]
    _single = [_ints(_l)[0] for _l in _rows if _B.len(_nums(_l)) == 1 and _ints(_l) and not _l.startswith('[')]
    if _subseq(_single, _flat):
        continue
    _lists = [_l for _l in _rows if _l.startswith('[')]
    assert _B.str(_log) not in _lists, ('Print one score at a time, not `training`: inside the inner loop, print '
                                        '`score`. Your loop printed the whole log.' + _e)
    if _lists:
        assert _inner, ('Each row is a list, so `print(row)` shows the whole row. Put a second `for` inside the '
                        'first, `for score in row:`, and print each `score`.' + _e)
        assert not _B.any(_kind(_x.iter) == 'Name' and _x.iter.id == 'training' for _x in _inner), (
            'Let the inner loop walk `row`, the row from the outer loop: `for score in row:`.' + _e)
        assert False, 'Print `score`, the one number this pass, not `row`.' + _e
    _mine = [_x for _x in __OWN_FLAT__ if _x not in _flat]
    assert not (_e and [_x for _x in _single if _x in _mine]), (
        'Let the loops read the log. Scores typed by hand cannot follow a new one.' + _e)
    assert not (_B.len(_log) > 1 and _single == _log[-1]), (
        'Indent the second `for` under `for row in training:`, so it runs for every row. Only the last row '
        'printed.' + _e)
    assert False, 'Print every score in the log, one per line, row by row.' + _e
''',
    OWN=TRAINING,
    OWN_FLAT=[x for row in TRAINING for x in row],
    CASES=TRAIN_CASES,
)

ROW_TOTALS = chk(
    "each morning's total prints after its scores",
    _TRAIN_RUN + r'''
for _vals in __CASES__:
    _ns, _rows, _err, _log, _e = _train_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _tot = [_ints(_l)[-1] for _l in _rows if _l.lower().startswith('total') and _ints(_l)]
    _want = [_B.sum(_row) for _row in _log]
    if _tot == _want:
        continue
    _run = []
    _s = 0
    for _row in _log:
        _s = _s + _B.sum(_row)
        _run.append(_s)
    assert _tot != _run, ('Start `total = 0` inside the outer loop, above the inner one: each morning starts from '
                          '0. Yours kept adding from the morning before.' + _e)
    assert not (_B.len(_tot) > _B.len(_want) and _B.len(_tot) == _B.sum(_B.len(_row) for _row in _log)), (
        "Take one indent off the total's print, so it sits after the inner loop, not in it. Yours printed a total "
        'after every score.' + _e)
    assert _tot, 'After each row, print `Total: ` and the row\'s total.' + _e
    assert False, ('Print one total per morning, after its scores: ' + ', '.join(_B.str(_x) for _x in _want)
                   + ' here.' + _e)
''',
    OWN=TRAINING,
    CASES=TRAIN_CASES,
)

LOOPS_IN_LOOPS = dict(
    id="loops-in-loops",
    title="Loops in loops",
    martu=(
        "Oogrish keeps a training log: one row a morning, three scores a row. A list of lists, yes?\n"
        "One loop walks the rows. But each row is a list too. So put a second loop *inside* the first: a "
        "[[loop inside a loop]]. For every row, the inner loop walks all of its scores."
    ),
    example=(
        "shelves = [[\"map\", \"rope\"], [\"oil\"]]\n"
        "for shelf in shelves:\n"
        "    for thing in shelf:\n"
        "        print(thing)\n"
    ),
    example_output="map\nrope\noil",
    names=["training", "row", "score"],
    predict=dict(
        q="Before you press Run: what does this print?",
        code="for row in [[1, 2], [3]]:\n    for x in row:\n        print(x)\n",
        choices=["1\n2\n3", "[1, 2]\n[3]", "1\n3"],
        answer=0,
        explain="The outer loop hands over `[1, 2]`, and the inner loop prints 1, then 2. Then `[3]`: it prints 3.",
    ),
    pair_talk=(
        "Before you Run, tell your partner how many times `print(score)` will run, and why. Then check it on your "
        "own screen."
    ),
    starter=TRAIN_STARTER,
    checkpoints=[
        dict(
            id="every-score",
            text="Print every score on its own line: put a second `for` inside the first, over `row`.",
            dictated=False,
            hints=[
                "Run the starter. Each line is a whole row, in square brackets. Look at `print(row)`.",
                "The inner loop goes in the outer loop's body, indented, and walks `row`. Its body is indented "
                "one step more.",
                "With other names:\n```python\nfor shelf in shelves:\n    for thing in shelf:\n"
                "        print(thing)\n```\nThe inner `for` is one indent in. Its print is one more.",
                "Under `for row in training:`, write `for score in row:`, then `print(score)` indented under it.",
            ],
            checks=[EVERY_SCORE],
            pass_line="Oogrish: Nine scores. I remember each one. My knees remember them better.",
        ),
    ],
    solution=TRAIN_SOLUTION,
    assemble=dict(
        lines=TRAIN_HEAD.splitlines()[2:] + TRAIN_LOOPS.splitlines(),
        distractors=["        print(row)", "    for score in training:", "for i in len(training):"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Rows, then scores",
            text=(
                "```text\nrow [7, 5, 9]  -> 7, 5, 9\nrow [8, 6, 9]  -> 8, 6, 9\nrow [9, 7, 10] -> 9, 7, 10\n```\n"
                "The outer loop picks a row. The inner loop reads it, left to right."
            ),
        ),
        dict(
            angle="everyday",
            label="A bookcase",
            text=(
                "To read every book, take one shelf, read every book on it, then go to the next shelf. Shelves are "
                "the outer loop; books are the inner one."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `row` is `[7, 5, 9]`. The inner loop prints 7, 5, 9.\n"
                "2. `row` is `[8, 6, 9]`. The inner loop prints 8, 6, 9.\n"
                "3. `row` is `[9, 7, 10]`. 9, 7, 10. Nine prints in all."
            ),
        ),
    ],
    bonus=dict(
        by="oogrish",
        title="Each morning's total",
        text=(
            "Oogrish wants each morning's total too. After each row's scores, print `Total: ` and that row's total. "
            "Start the total again for every row."
        ),
        hints=[
            "The reset goes inside the outer loop, above the inner one: each morning starts from 0. The print goes "
            "after the inner loop, still inside the outer one.",
            "Write `total = 0` under `for row in training:`, add `total = total + score` in the inner loop, then "
            "`print(\"Total: \" + str(total))` after it.",
        ],
        checks=[ROW_TOTALS],
        solution=TRAIN_BONUS,
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="for member in party.members:\n    add_spell(member[\"spell_book\"], ...)",
        why=(
            "The roster is a list of sheets, and each sheet holds a spell book. A loop inside a loop could walk "
            "every member, then every spell in that member's book."
        ),
    ),
    takeaway="A loop inside a loop: for every pass of the outer loop, the inner loop runs all the way through.",
    wrong_answers=[
        dict(why="the starter (each row printed whole)", code=TRAIN_STARTER, fails_at=1,
             message_contains="Put a second `for` inside the first"),
        dict(why="print(row) inside the inner loop (the list, not the item)",
             code=TRAIN_HEAD + "for row in training:\n    for score in row:\n        print(row)\n", fails_at=1,
             message_contains="not `row`"),
        dict(why="the inner loop walks training, not row",
             code=TRAIN_HEAD + "for row in training:\n    for score in training:\n        print(score)\n", fails_at=1,
             message_contains="walk `row`"),
        dict(why="the whole log printed", code=TRAIN_HEAD + "for row in training:\n    print(training)\n", fails_at=1,
             message_contains="whole log"),
        dict(why="the second loop not inside the first (only the last row)",
             code=TRAIN_HEAD + "for row in training:\n    print(\"Row\")\nfor score in row:\n    print(score)\n",
             fails_at=1, message_contains="Only the last row"),
        dict(why="positions typed in range(3) (fits 3 rows of 3 only)",
             code=TRAIN_HEAD + "for i in range(3):\n    for j in range(3):\n        print(training[i][j])\n",
             fails_at=1, message_contains="A number typed in `range()`"),
        dict(why="for i in len(...) (an int after `in`)",
             code=TRAIN_HEAD + "for i in len(training):\n    print(training[i])\n", fails_at=0,
             message_contains="'int' object is not iterable"),
        dict(why="the item used as an index (row[score])",
             code=TRAIN_HEAD + "for row in training:\n    for score in row:\n        print(row[score])\n",
             fails_at=0, message_contains="index out of range"),
        dict(why="the scores typed by hand",
             code=TRAIN_HEAD + "".join(f"print({x})\n" for row in TRAINING for x in row), fails_at=1,
             message_contains="typed by hand"),
        dict(why="the example's list name copied",
             code=TRAIN_HEAD + "for shelf in shelves:\n    for thing in shelf:\n        print(thing)\n", fails_at=0,
             message_contains="not defined"),
        dict(why="the inner loop's body not indented",
             code=TRAIN_HEAD + "for row in training:\n    for score in row:\n    print(score)\n", fails_at=0,
             message_contains="expected an indented block"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="nested-loop,for-each", solo="false", dictates="",
             foreign_names="shelves,shelf,thing,x") + "\n"
        "5C-02 (O). The 2D training log (3 mornings x 3 drills; Oogrish's yard from 3P1). CP1 [ND] reruns with a "
        "4-row and a 1-row log: the scores must show in order, one per line (other lines, like the side quest's "
        "totals, may sit between). Caught: `print(row)` / `print(training)` (the list, not the item), the inner "
        "loop over `training`, a second loop not nested (only the last row), `for i in len(training)` (the "
        "'int' object is not iterable slip, Unit 6's `for i in 5`), `row[score]` (the item as an index), typed "
        "scores, positions typed in `range(3)` (fits 3 x 3 only), the example's `shelves`. Side quest (Oogrish): a total per morning, where the reset belongs "
        "INSIDE the outer loop (the running-total slip turned around)."
    ),
)

# ---- 5C-03 one-line-loops -------------------------------------------------------------------------------------

ONE_HEAD = WALL_LINE + "\n# 1. The long way. Make it one line.\n"
ONE_LONG = (
    "short_gaps = []\n"
    "for h in chalk_wall:\n"
    "    if h < 45:\n"
    "        short_gaps.append(h)\n"
)
ONE_MID = "print(short_gaps)\n\n# 2. How much each gap shrank,\n#    in one line.\n"
ONE_SHORT = "short_gaps = [h for h in chalk_wall if h < 45]\n"
ONE_SHRINKS = "shrinks = [chalk_wall[i - 1] - chalk_wall[i] for i in range(1, len(chalk_wall))]\n"
ONE_STARTER = ONE_HEAD + ONE_LONG + ONE_MID + "shrinks = []\nprint(shrinks)\n"


def _one(short=ONE_LONG, shrinks="shrinks = []\n"):
    return ONE_HEAD + short + ONE_MID + shrinks + "print(shrinks)\n"


ONE_SOLUTION = _one(ONE_SHORT, ONE_SHRINKS)
ONE_CASES = [None, {"chalk_wall": [50, 44, 46, 30, 45]}, {"chalk_wall": [40, 37]}]

_WALL_RUN = r'''
def _wall_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', __WALL__, ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    assert not _miss, _keep(__WNAME__)
    return _ns, _rows, _err, _vals[__WNAME__], _ev(_vals)
def _made_by_comp(_name):
    return [_n for _n in _tree().body if _kind(_n) == 'Assign' and _kind(_n.value) == 'ListComp'
            and _B.any(_kind(_x) == 'Name' and _x.id == _name for _x in _n.targets)]
'''

SHORT_GAPS = chk(
    "short_gaps holds the gaps under 45, built in one line",
    _WALL_RUN + r'''
_own = globals().get('short_gaps')
for _vals in __CASES__:
    _ns, _rows, _err, _w, _e = _wall_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    _want = [_h for _h in _w if _h < 45]
    _got = _ns.get('short_gaps')
    if _got == _want:
        # A slip in task 2's line (it runs later) is task 2's to name, not this step's.
        continue
    assert not _err, _stop(_err, _e)
    assert _kind(_got) == 'list', 'Keep `short_gaps = `, with the one-line loop after it, in square brackets.' + _e
    assert _got != [_h for _h in _w if _h > 45], 'Under 45 means `< 45`. Your list holds the gaps over 45.' + _e
    assert _got != [_h for _h in _w if _h <= 45], 'Use `<`: 45 is not under 45.' + _e
    assert _got != _w, 'Add the `if` at the end: `if h < 45`. Without it, the list keeps every gap.' + _e
    assert not (_vals is not None and _got == _own), (
        'Build the list from `chalk_wall`, so it follows the wall. Yours stayed the same, typed by hand.' + _e)
    assert False, 'Keep only the gaps under 45, in wall order, read from `chalk_wall`.' + _e
assert _made_by_comp('short_gaps'), ('Build `short_gaps` in one line, a list comprehension: square brackets, what to '
                                     'keep first, then the `for`, then the `if`.')
_apps = [_n for _n in _ast.walk(_tree()) if _kind(_n) == 'Call' and _kind(_n.func) == 'Attribute'
         and _n.func.attr == 'append' and _kind(_n.func.value) == 'Name' and _n.func.value.id == 'short_gaps']
assert not _apps, ('Replace the long way with your one line. The `for` loop and its `.append()` are still there, '
                   'so `short_gaps` is built twice.')
''',
    WALL=WALL,
    WNAME="chalk_wall",
    CASES=ONE_CASES,
)

SHRINKS = chk(
    "shrinks holds how much each gap shrank, built in one line",
    _WALL_RUN + r'''
_own = globals().get('shrinks')
_typed_len = [_n for _n in _ast.walk(_tree()) if _kind(_n) == 'Call' and _kind(_n.func) == 'Name'
              and _n.func.id == 'range' and _B.any(_kind(_a) == 'Constant' and _kind(_a.value) == 'int'
                                                   and _a.value > 1 for _a in _n.args)]
for _vals in __CASES__:
    _ns, _rows, _err, _w, _e = _wall_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    if _err.startswith('IndexError') and _typed_len:
        assert False, ('Use `len(chalk_wall)` in the `range`, not a number you typed: another wall can be '
                       'shorter. With another wall, Python stopped: ' + _err + '.' + _e)
    if _err.startswith('IndexError'):
        assert False, ('Stop one early: the last gap has no gap after it. Use `range(1, len(chalk_wall))` with '
                       '`chalk_wall[i - 1] - chalk_wall[i]`. With another wall, Python stopped: ' + _err + '.' + _e)
    assert not _err, _stop(_err, _e)
    _want = [_w[_i - 1] - _w[_i] for _i in _B.range(1, _B.len(_w))]
    _got = _ns.get('shrinks')
    if _got == _want:
        continue
    assert _kind(_got) == 'list', 'Keep `shrinks = `, with the one-line loop after it, in square brackets.' + _e
    assert _got, ('Make `shrinks` hold how much each gap shrank: for each position `i` from 1 on, '
                  '`chalk_wall[i - 1] - chalk_wall[i]`.' + _e)
    assert _got != [-_x for _x in _want], ('Take this gap from the gap before: `chalk_wall[i - 1] - chalk_wall[i]`. '
                                           'Your shrinks came out the other way round.' + _e)
    assert not (_B.len(_got) == _B.len(_want) + 1 and _got[1:] == _want), (
        'Start at 1: `range(1, len(chalk_wall))`. At 0, `chalk_wall[i - 1]` is the newest gap, so your first '
        'shrink compares the two ends of the wall.' + _e)
    assert not (_vals is not None and _got == _own), (
        'Build `shrinks` from `chalk_wall`, so it follows the wall. Yours stayed the same, typed by hand.' + _e)
    assert False, ('Each shrink is the gap before minus this gap. On this wall: ' + _sh(_want) + '.' + _e)
assert _made_by_comp('shrinks'), ('Build `shrinks` in one line, in square brackets, like `short_gaps`: what to keep '
                                  'first, then `for i in range(1, len(chalk_wall))`.')
''',
    WALL=WALL,
    WNAME="chalk_wall",
    CASES=ONE_CASES,
)

ONE_LINE_LOOPS = dict(
    id="one-line-loops",
    title="Loops in one line",
    martu=(
        "Four lines to build one small list: make it empty, loop, ask, append. Python has a shorter way, yes?\n"
        "A [[list comprehension]] is that loop in one line, inside square brackets. What to keep comes first, then "
        "the `for`, then the `if`. No colons, no `.append()`. It hands back a brand-new list."
    ),
    introduces=["node:ListComp"],
    example=(
        "coins = [5, 12, 3]\n"
        "doubled = [c * 2 for c in coins]\n"
        "big = [c for c in coins if c > 4]\n"
        "print(doubled)\n"
        "print(big)\n"
    ),
    example_output="[10, 24, 6]\n[5, 12]",
    names=["chalk_wall", "short_gaps", "shrinks", "h", "i"],
    predict=dict(
        q="Before you press Run: what does this print?",
        code="nums = [5, 12, 3, 20]\nprint([n for n in nums if n > 4])\n",
        choices=["[5, 12, 20]", "[12, 20]", "[5, 12, 3, 20]"],
        answer=0,
        explain="Every `n` that is over 4 is kept, in order: 5, 12 and 20. The 3 is left out.",
    ),
    starter=ONE_STARTER,
    checkpoints=[
        dict(
            id="short-gaps-one-line",
            text="Replace the four lines that build `short_gaps` with one list comprehension.",
            dictated=False,
            hints=[
                "Look at task 1: `short_gaps = []`, the `for` line, the `if` line and the `.append()` line. All "
                "four go, and one line takes their place.",
                "Read the long way from the inside out: keep `h`, for each `h` in the wall, if `h < 45`. The one "
                "line says it in that order.",
                "With other names: `big = [c for c in coins if c > 4]`.",
                "Write `short_gaps = [h for h in chalk_wall if h < 45]` in place of the four lines.",
            ],
            checks=[SHORT_GAPS],
            pass_line="Gearshift: Forty-four, forty-one, thirty-seven. Same list. Fewer lines.",
        ),
        dict(
            id="shrinks-one-line",
            text="Make `shrinks` in one line: for each position from 1 on, the gap before minus this gap.",
            dictated=False,
            hints=[
                "Look at task 2. This loop walks positions, not gaps: `for i in range(1, len(chalk_wall))`.",
                "Start at 1, so every gap has a gap before it. What to keep comes first: "
                "`chalk_wall[i - 1] - chalk_wall[i]`.",
                "With other names: `steps = [path[i] - path[i - 1] for i in range(1, len(path))]`.",
                "Write `shrinks = [chalk_wall[i - 1] - chalk_wall[i] for i in range(1, len(chalk_wall))]` in place "
                "of `shrinks = []`.",
            ],
            checks=[SHRINKS],
            pass_line="Mar'tu: Zero, one, one, two, three, four. The decay, in one line. It is still accelerating.",
        ),
    ],
    solution=ONE_SOLUTION,
    partials=[_one(ONE_SHORT)],
    assemble=dict(
        lines=[WALL_LINE.strip(), ONE_SHORT.strip(), "print(short_gaps)", ONE_SHRINKS.strip(), "print(shrinks)"],
        distractors=["short_gaps = [h for h in chalk_wall: if h < 45]",
                     "shrinks = [chalk_wall[i] - chalk_wall[i + 1] for i in range(len(chalk_wall))]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The same loop, folded",
            text=(
                "```text\nfor c in coins:\n    if c > 4:\n        keep c\n\n[c  for c in coins  if c > 4]\n"
                " ^  ^ the for line  ^ the if\n keep\n```\n"
                "The same fold works for the wall: keep `h`, the `for`, then the `if`."
            ),
        ),
        dict(
            angle="everyday",
            label="A sieve",
            text=(
                "Pour the gaps through a sieve: only the small ones fall through into the new bowl. The bowl is the "
                "new list; the sieve is the `if`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `h` is 48: not under 45, skip. Then 48, 47, 46: skip.\n"
                "2. `h` is 44: keep it. 41: keep. 37: keep.\n"
                "3. The new list is `[44, 41, 37]`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The chalk wall showed the gaps shrinking, and Mar'tu said the decay is accelerating. The shrinks "
                "list is that same reading, built in one line."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "Gearshift ran the math at the chalk wall: the gaps were getting shorter, and shrinking faster. Your "
            "`shrinks` list is that math, and it fits on one line."
        ),
    ),
    takeaway="`[h for h in wall if h < 45]` builds a new list in one line: what to keep, the `for`, then the `if`.",
    wrong_answers=[
        dict(why="the starter (the long way left)", code=ONE_STARTER, fails_at=1, message_contains="in one line"),
        dict(why="over 45 instead of under", code=_one("short_gaps = [h for h in chalk_wall if h > 45]\n"), fails_at=1,
             message_contains="over 45"),
        dict(why="<= 45 (the rerun wall has a 45)", code=_one("short_gaps = [h for h in chalk_wall if h <= 45]\n"),
             fails_at=1, message_contains="45 is not under 45"),
        dict(why="no if (every gap kept)", code=_one("short_gaps = [h for h in chalk_wall]\n"), fails_at=1,
             message_contains="Add the `if`"),
        dict(why="the long way kept beside the one line", code=_one(ONE_LONG + ONE_SHORT), fails_at=1,
             message_contains="still there"),
        dict(why="the list typed by hand", code=_one("short_gaps = [44, 41, 37]\n"), fails_at=1,
             message_contains="typed by hand"),
        dict(why="a colon inside the one-line loop (the for-line habit)",
             code=_one("short_gaps = [h for h in chalk_wall: if h < 45]\n"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the example's list name copied", code=_one("short_gaps = [c for c in coins if c < 45]\n"),
             fails_at=0, message_contains="not defined"),
        dict(why="task 1 done, shrinks still empty", code=_one(ONE_SHORT), fails_at=2, message_contains="each gap shrank"),
        dict(why="neighbors one past the end (the loop must stop one early)",
             code=_one(ONE_SHORT, "shrinks = [chalk_wall[i] - chalk_wall[i + 1] for i in range(len(chalk_wall))]\n"),
             fails_at=0, message_contains="index out of range"),
        dict(why="range from 0 (compares the two ends first)",
             code=_one(ONE_SHORT, "shrinks = [chalk_wall[i - 1] - chalk_wall[i] for i in range(len(chalk_wall))]\n"),
             fails_at=2, message_contains="Start at 1"),
        dict(why="this gap minus the one before (the other way round)",
             code=_one(ONE_SHORT, "shrinks = [chalk_wall[i] - chalk_wall[i - 1] for i in range(1, len(chalk_wall))]\n"),
             fails_at=2, message_contains="other way round"),
        dict(why="the shrinks typed by hand", code=_one(ONE_SHORT, "shrinks = [0, 1, 1, 2, 3, 4]\n"), fails_at=2,
             message_contains="typed by hand"),
        dict(why="the shrinks built the long way",
             code=_one(ONE_SHORT, "shrinks = []\nfor i in range(1, len(chalk_wall)):\n"
                                  "    shrinks.append(chalk_wall[i - 1] - chalk_wall[i])\n"),
             fails_at=2, message_contains="in one line"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="list-comprehension,neighbors", solo="false", dictates="",
             foreign_names="coins,c,doubled,big,nums,n,path,steps") + "\n"
        "5C-03 (O). Intro node:ListComp. CP1 [ND] (teacher ruling on the Unit 6 reviews: no longer dictated) is "
        "the spec's line, `[h for h in chalk_wall if h < 45]`, replacing the long way shown in the starter (a "
        "refactor: the value already passes, so the check also needs the comprehension, and no `.append()` left). "
        "The full line is in the Show rung only: the text, the other rungs, the folded picture (the example's "
        "`coins`) and the check messages never spell it out. CP2 [ND] is the decay reveal (5A-05) in one line, with positions: "
        "it carries the neighbors slip, `chalk_wall[i + 1]` over the whole range (IndexError: stop one early). "
        "`chalk_wall[i] - chalk_wall[i + 1] for i in range(len(chalk_wall) - 1)` passes too. Reruns with "
        "[50, 44, 46, 30, 45] (a 45, for `<=`; shrinks that go both ways) and [40, 37]. The real wall line is 41 "
        "characters, kept whole (the Unit 4 exception)."
    ),
)

# ---- 5C-04 choose-in-one-line ---------------------------------------------------------------------------------

ROSTER_5C4 = [
    {"name": "Oogrish", "mana": 3, "max_mana": 18},
    {"name": "Gearshift", "mana": 0, "max_mana": 20},
    {"name": "Bomb Shell", "mana": 2, "max_mana": 24},
    {"name": "Lucky", "mana": 12, "max_mana": 26},
]
SETUP_5C4 = _sheet_lines(ROSTER_5C4)
ROSTER_5C4_A = [
    {"name": "Pell", "mana": 4, "max_mana": 12},
    {"name": "Moss", "mana": 3, "max_mana": 20},
    {"name": "Brakka", "mana": 1, "max_mana": 15},
    {"name": "Tester", "mana": 0, "max_mana": 14},
]
ROSTER_5C4_B = [
    {"name": "Zelda", "mana": 2, "max_mana": 9},
    {"name": "Kratos", "mana": 9, "max_mana": 16},
]
CHOOSE_HEAD = "# roster is ready for you.\nfor member in roster:\n    name = member[\"name\"]\n    mana = member[\"mana\"]\n"
CHOOSE_LONG = (
    "    if mana >= 3:\n"
    "        status = \"ready\"\n"
    "    else:\n"
    "        status = \"resting\"\n"
)
CHOOSE_PRINT = "    print(name + \": \" + status)\n"
CHOOSE_ONE = "    status = \"ready\" if mana >= 3 else \"resting\"\n"
CHOOSE_STARTER = CHOOSE_HEAD + CHOOSE_LONG + CHOOSE_PRINT


def _choose(middle, tail=CHOOSE_PRINT):
    return CHOOSE_HEAD + middle + tail


CHOOSE_SOLUTION = _choose(CHOOSE_ONE)

_CHOOSE_RUN = r'''
def _status_case(_ros, _note):
    if _ros is None:
        return _lines(), '', __OWN__, ''
    _ns, _rows, _err, _miss = _rerun(None, _ros)
    return _rows, _err, _ros, _ev(None, _note)
def _line_of(_rows, _h):
    _ls = [_l.lower() for _l in _rows if _h['name'].lower() in _l.lower()]
    return _ls[0] if _ls else ''
'''

STATUS_LINES = chk(
    "each hero's line says ready or resting",
    _CHOOSE_RUN + r'''
_own_names = [_h['name'] for _h in __OWN__]
for _ros, _note in __CASES__:
    _rows, _err, _ros, _e = _status_case(_ros, _note)
    assert _err != 'ENDLESS', 'Make sure the loop can end.' + _e
    assert not _err, _stop(_err, _e)
    _bad = []
    for _h in _ros:
        _l = _line_of(_rows, _h)
        _word = 'ready' if _h['mana'] >= 3 else 'resting'
        _other = 'resting' if _word == 'ready' else 'ready'
        if not (_word in _l and _other not in _l):
            _bad.append((_h, _l, _word))
    if not _bad:
        continue
    _mine = [_x for _x in _own_names if _x not in [_h['name'] for _h in _ros]]
    assert not (_e and [_l for _l in _rows if _B.any(_x.lower() in _l.lower() for _x in _mine)]), (
        'Let the loop write each line. Lines typed by hand cannot follow a new roster.' + _e)
    assert not _B.all(_l and _w not in _l for _h, _l, _w in _bad) or _B.len(_bad) < _B.len(_ros), (
        'Swap the words: the word before `if` is the one for True, `"ready"`, and the word after `else` is for '
        'False.' + _e)
    assert not [_h for _h, _l, _w in _bad if _h['mana'] == 3], (
        'Use `>=`: a hero with exactly 3 mana is ready.' + _e)
    assert not [_h for _h, _l, _w in _bad if not _l], 'Print a line for every member: the name, then the word.' + _e
    assert False, 'Print `ready` for 3 mana or more, and `resting` for less.' + _e
''',
    setup=SETUP_5C4,
    OWN=ROSTER_5C4,
    CASES=[(None, ""), (ROSTER_5C4_A, "a roster of 4 other heroes"), (ROSTER_5C4_B, "a roster of 2 other heroes")],
)

ONE_LINE_CHOICE = (
    "the choice is made in one line",
    "assert 'node:IfExp' in _concept_tokens(_source), ('Choose `status` in one line, in place of the four `if` / "
    "`else` lines: the True value, then `if` and the question, then `else` and the False value.')\n"
    "assert 'node:If' not in _concept_tokens(_source), ('Replace the four `if` / `else` lines with your one line. The "
    "`if` statement is still there.')",
)

AMOUNTS = chk(
    "each line shows the mana, or empty",
    _CHOOSE_RUN + r'''
for _ros, _note in __CASES__:
    _rows, _err, _ros, _e = _status_case(_ros, _note)
    assert not _err, _stop(_err, _e)
    for _h in _ros:
        _l = _line_of(_rows, _h)
        if _h['mana'] == 0:
            assert 'empty' in _l, ('Show `empty` for a hero with 0 mana: `str(mana) if mana > 0 else "empty"`.' + _e)
        else:
            assert _h['mana'] in _ints(_l), ("Show each hero's mana after the word: `str(mana)`." + _e)
''',
    setup=SETUP_5C4,
    OWN=ROSTER_5C4,
    CASES=[(None, ""), (ROSTER_5C4_A, "a roster of 4 other heroes")],
)

CHOOSE_IN_ONE_LINE = dict(
    id="choose-in-one-line",
    title="Choose in one line",
    martu=(
        "Ready, or resting? Four lines of `if` and `else` to pick one word. You can pick it in one line, yes?\n"
        "A [[one-line choice]] reads like a sentence: `\"full\" if coins > 5 else \"low\"`. The value before "
        "`if` is used when the question is True. The value after `else` is used when it is False. Then it goes "
        "into a variable, like any value."
    ),
    introduces=["node:IfExp"],
    example="coins = 7\nbag = \"full\" if coins > 5 else \"low\"\nprint(bag)\n",
    example_output="full",
    names=["status", "mana"],
    predict=dict(
        q="Before you press Run: what does this print?",
        code="oil = 0\nlamp = \"lit\" if oil > 0 else \"dark\"\nprint(lamp)\n",
        choices=["dark", "lit", "lit if oil > 0 else dark"],
        answer=0,
        explain="`oil > 0` is False, so the value after `else` is used: `dark`.",
    ),
    setup=SETUP_5C4,
    starter=CHOOSE_STARTER,
    checkpoints=[
        dict(
            id="status-in-one-line",
            text="Replace the four `if` / `else` lines with one line that chooses `status`.",
            dictated=False,
            hints=[
                "Look at the four lines that make `status`. They go, and one line inside the loop takes their place.",
                "The order is: the True value, `if`, the question, `else`, the False value.",
                "With other names: `bag = \"full\" if coins > 5 else \"low\"`.",
                "Write `status = \"ready\" if mana >= 3 else \"resting\"` in place of the four lines, indented "
                "inside the loop.",
            ],
            checks=[STATUS_LINES, ONE_LINE_CHOICE],
            pass_line="Lucky: Ready. Obviously.",
        ),
    ],
    solution=CHOOSE_SOLUTION,
    assemble=dict(
        lines=[line for line in CHOOSE_SOLUTION.splitlines() if not line.startswith("#")],
        distractors=["    status = \"ready\" if mana > 3 else \"resting\"",
                     "    status = \"resting\" if mana >= 3 else \"ready\""],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One line, two roads",
            text=(
                "```text\n\"full\" if coins > 5 else \"low\"\n ^ True   ^ question     ^ False\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Say it out loud",
            text=(
                "\"Ready if you have 3 mana, otherwise resting.\" You say it in one breath. Python lets you write it "
                "the same way."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Oogrish has 3: `3 >= 3` is True, so `ready`.\n"
                "2. Gearshift has 0: False, so `resting`.\n"
                "3. Bomb Shell has 2: `resting`. Lucky has 12: `ready`."
            ),
        ),
    ],
    bonus=dict(
        by="bomb-shell",
        title="Numbers too",
        text=(
            "Bomb Shell wants numbers. Add a second one-line choice: `amount` is `str(mana)`, or `\"empty\"` when "
            "mana is 0. Print it after the word."
        ),
        hints=[
            "A second choice, on its own line inside the loop: the True value first, the question, then `else`.",
            "Write `amount = str(mana) if mana > 0 else \"empty\"`, then print `name + \": \" + status + \", \" "
            "+ amount`.",
        ],
        checks=[AMOUNTS],
        solution=_choose(CHOOSE_ONE + "    amount = str(mana) if mana > 0 else \"empty\"\n",
                         "    print(name + \": \" + status + \", \" + amount)\n"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet="if caster[\"mana\"] < spell[\"mana_cost\"]:",
        why=(
            "Holding the barrier, an `if` chose what happened next. When the choice is only between two values, "
            "one line can make it."
        ),
    ),
    takeaway="`a if question else b` picks `a` when the question is True and `b` when it is False, in one line.",
    wrong_answers=[
        dict(why="the starter (four lines of if / else)", code=CHOOSE_STARTER, fails_at=1, message_contains="in one line"),
        dict(why="> 3 (exactly 3 is ready)", code=_choose(CHOOSE_ONE.replace(">=", ">")), fails_at=1,
             message_contains="exactly 3"),
        dict(why="the two words swapped", code=_choose("    status = \"resting\" if mana >= 3 else \"ready\"\n"),
             fails_at=1, message_contains="Swap the words"),
        dict(why="no else", code=_choose("    status = \"ready\" if mana >= 3\n"), fails_at=0,
             message_contains="expected 'else'"),
        dict(why="the words without quotes", code=_choose("    status = ready if mana >= 3 else resting\n"),
             fails_at=0, message_contains="not defined"),
        dict(why="the if / else kept beside the one line", code=_choose(CHOOSE_LONG + CHOOSE_ONE), fails_at=1,
             message_contains="still there"),
        dict(why="roster[\"mana\"] for member[\"mana\"]",
             code=CHOOSE_HEAD.replace("member[\"mana\"]", "roster[\"mana\"]") + CHOOSE_ONE + CHOOSE_PRINT,
             fails_at=0, message_contains="not str"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="conditional-expression", solo="false", dictates="",
             foreign_names="coins,bag,oil,lamp") + "\n"
        "5C-04 (O). Intro node:IfExp, the spec's line `\"ready\" if mana >= 3 else \"resting\"`. CP1 [ND] (teacher "
        "ruling on the Unit 6 reviews: no longer dictated); the full line is in the Show rung only (Mar'tu's text "
        "and the picture use the example's `coins`, and the check messages name the shape, never the line). A "
        "refactor of the starter's four lines: the output already passes, so a second check needs the one-line choice and no `if` "
        "statement left. Roster in setup (3, 0, 2, 12: Oogrish at exactly 3 is the boundary); reruns with 4 and 2 "
        "other heroes (Moss at exactly 3). Side quest (Bomb Shell): a second choice, `str(mana)` or `empty`."
    ),
)

# ---- SOLO 5C ---------------------------------------------------------------------------------------------------

SOLO_WALL = "wall = [48, 48, 47, 46, 44, 41, 37]\n"


def _solo(line):
    return SOLO_WALL + line + "\nprint(high)\n"


SOLO_5C_STARTER = _solo("high = [h for h in wall: if h > 45]")
SOLO_5C_SOLUTION = _solo("high = [h for h in wall if h > 45]")

SOLO_LONG = chk(
    "high holds the gaps over 45",
    _WALL_RUN + r'''
_own = globals().get('high')
for _vals in __CASES__:
    _ns, _rows, _err, _w, _e = _wall_case(_vals)
    assert not _err, _stop(_err, _e)
    _want = [_h for _h in _w if _h > 45]
    _got = _ns.get('high')
    if _got == _want:
        continue
    assert not (_vals is not None and _got == _own), (
        'Let the one-line loop build the list from `wall`. Yours stayed the same, typed by hand.' + _e)
    assert _got != [_h for _h in _w if _h >= 45], 'Use `>`: 45 is not over 45.' + _e
    assert False, 'Keep the gaps over 45, in wall order.' + _e
assert _made_by_comp('high'), 'Keep it a one-line loop: mend the slip in line 2, and keep the rest.'
''',
    WALL=WALL,
    WNAME="wall",
    CASES=[None, {"wall": [50, 45, 47, 30]}],
)

SOLO_5C = dict(
    id="solo-5c",
    title="Show Mar'tu",
    martu="A short one, just for you. One slip. Read the last line, then mend it.",
    solo=True,
    explainer="lean",
    names=["wall", "high"],
    starter=SOLO_5C_STARTER,
    checkpoints=[
        dict(
            id="mend-the-one-line-loop",
            text="Mend line 2 so `high` holds every gap over 45.",
            dictated=False,
            hints=[
                "Read Python's last line, and the line it names. The little `^` points near the slip.",
                "A one-line loop is not a `for` line. It has no colon anywhere.",
                "With other names: `[c for c in coins if c > 4]`. Nothing between `coins` and `if`.",
            ],
            checks=[SOLO_LONG],
            pass_line="Mar'tu: You did that on your own. I saw. On your map: a one-line loop has no colon.",
        ),
    ],
    solution=SOLO_5C_SOLUTION,
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line. 2. Line 2. 3. Take out what a `for` line needs, but "
                                        "a one-line loop does not."),
        dict(angle="shorter", text="A `for` line needs a colon. A one-line loop does not."),
    ],
    takeaway="On your own: a one-line loop has no colon: `[h for h in wall if h > 45]`.",
    wrong_answers=[
        dict(why="the starter (a colon inside the one-line loop)", code=SOLO_5C_STARTER, fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the colon moved to the end", code=_solo("high = [h for h in wall if h > 45:]"), fails_at=0,
             message_contains="SyntaxError"),
        dict(why="the list typed by hand", code=_solo("high = [48, 48, 47, 46]"), fails_at=1,
             message_contains="typed by hand"),
        dict(why=">= 45 (the rerun wall has a 45)", code=_solo("high = [h for h in wall if h >= 45]"), fails_at=1,
             message_contains="45 is not over 45"),
        dict(why="rewritten the long way (the step keeps the one-line loop)",
             code=_solo("high = []\nfor h in wall:\n    if h > 45:\n        high.append(h)"), fails_at=1,
             message_contains="Keep it a one-line loop"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="list-comprehension,read-traceback", solo="true",
             dictates="", foreign_names="coins,c",
             seat_b="high = [h for h in wall if h > 45 (the closing bracket left off)") + "\n"
        "SOLO, one bug: a colon inside the one-line loop, the `for`-line habit (SyntaxError 'invalid syntax'). "
        "Rung 0 is 'Read Python's last line'; explainer='lean' (teacher ruling: every SOLO from Unit 2 on). Added "
        "to Lesson 5C so the lesson has its one SOLO (2.12 lint g); the spec lists 5C-01 to 5C-04 only. The list "
        "is `wall` and the result `high`, so every starter line fits a phone (36 characters). CMB with "
        "[50, 45, 47, 30] (a 45, for `>=`). The harness warns that the starter is not valid Python: intended, as "
        "in Unit 2's syntax-slip SOLO items."
    ),
)

LESSON_5C = dict(
    kind="lesson",
    id="loops-in-one-line",
    title="Loops in One Line",
    optional=True,
    minutes=20,
    summary="Skip a pass with `continue`, put a loop inside a loop, and build lists and choices in one line.",
    notes=(
        "Lesson 5C (O). 5C-01 skip-the-empty, 5C-02 loops-in-loops, 5C-03 one-line-loops, 5C-04 choose-in-one-line, "
        "then one SOLO (solo-5c, added for lint g). Every checkpoint is non-dictated (teacher ruling on the Unit 6 "
        "reviews: the two one-liners, 5C-03 CP1 and 5C-04, are no longer dictated; the full line sits in their Show "
        "rungs only): 5C-01, 5C-02, 5C-03 CP1 and CP2, 5C-04, solo-5c."
    ),
    exercises=[SKIP_THE_EMPTY, LOOPS_IN_LOOPS, ONE_LINE_LOOPS, CHOOSE_IN_ONE_LINE, SOLO_5C],
)


# =============================================================================================
# Article 5-A1 "Looping Over a Dictionary" (optional, 10 min), with the try-it spell-costs
# =============================================================================================

BOOK = {"Glow": 2, "Warm Hands": 3, "Lantern Ward": 6}
BOOK_HEAD = (
    "spell_book = {\n"
    "    \"Glow\": 2,\n"
    "    \"Warm Hands\": 3,\n"
    "    \"Lantern Ward\": 6,\n"
    "}\n"
)
BOOK_T1 = "# 1. Print each spell and its cost.\n"
BOOK_T2 = "\n# 2. Add up every cost in total,\n#    then print total.\n"
BOOK_EACH = "for name, cost in spell_book.items():\n    print(name + \": \" + str(cost))\n"
BOOK_TOTAL = (
    "total = 0\n"
    "for cost in spell_book.values():\n"
    "    total = total + cost\n"
    "print(\"Total: \" + str(total))\n"
)


def _book(each="", total=""):
    return BOOK_HEAD + BOOK_T1 + each + BOOK_T2 + total


BOOK_STARTER = _book()
BOOK_SOLUTION = _book(BOOK_EACH, BOOK_TOTAL)
BOOK_CASES = [None, {"spell_book": {"Mend": 4, "Spark": 1}},
              {"spell_book": {"Shield Up": 7, "Glow": 2, "Fire Bolt": 5, "Hum": 3}}]

_BOOK_RUN = r'''
def _book_case(_vals):
    if _vals is None:
        return globals(), _lines(), '', __OWN__, ''
    _ns, _rows, _err, _miss = _rerun(_vals)
    assert not _miss, _keep('spell_book')
    return _ns, _rows, _err, _vals['spell_book'], _ev(_vals)
_own_names = _B.list(__OWN__)
'''

EACH_SPELL = chk(
    "each spell prints with its cost",
    _BOOK_RUN + r'''
for _vals in __CASES__:
    _ns, _rows, _err, _book, _e = _book_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    _at = 0
    _want = _B.list(_book.items())
    for _l in _rows:
        if (_at < _B.len(_want) and _l[:1] not in '({[' and _want[_at][0].lower() in _l.lower()
                and _want[_at][1] in _ints(_l)):
            _at = _at + 1
    if _at == _B.len(_want):
        # A slip in task 2 (it runs later) is task 2's to name, not this step's.
        continue
    assert not _err, _stop(_err, _e)
    assert not [_l for _l in _rows if _l.startswith("('")], (
        'Give the pair two names: `for name, cost in spell_book.items():`. One name gets the whole pair, brackets '
        'and all.' + _e)
    assert not [_l for _l in _rows if _l.startswith("{'")], (
        'Print one spell at a time, inside the loop, not the whole spell book.' + _e)
    _mine = [_x for _x in _own_names if _x not in _book]
    assert not (_e and [_l for _l in _rows if _B.any(_x.lower() in _l.lower() for _x in _mine)]), (
        'Let the loop read the spell book. Lines typed by hand cannot follow another book.' + _e)
    assert not [_l for _l in _rows if _B.any(_k.lower() in _l.lower() for _k in _book) and not _ints(_l)], (
        'Add the cost to each line: `name + ": " + str(cost)`.' + _e)
    assert False, ('Print every spell with its cost, one line each: `for name, cost in spell_book.items():`.' + _e)
''',
    OWN=BOOK,
    CASES=BOOK_CASES,
)

USES_ITEMS = (
    "the loop uses .items()",
    "assert 'attr:items' in _concept_tokens(_source), ('This try-it is for `.items()`: `for name, cost in "
    "spell_book.items():`. Reading `spell_book[name]` works too, but meet `.items()` here.')\n"
    "import ast as _ast\n"
    "import builtins as _B\n"
    "_tr = _ast.parse(_source)\n"
    "assert [_n for _n in _ast.walk(_tr) if _B.type(_n).__name__ == 'For' and [_x for _x in _ast.walk(_n.iter) "
    "if _B.type(_x).__name__ == 'Attribute' and _x.attr == 'items']], ('Put `.items()` in the `for` line, so the "
    "loop walks the pairs: `for name, cost in spell_book.items():`. Yours uses `.items()` somewhere else.')",
)

BOOK_TOTAL_CHECK = chk(
    "total adds up every cost and prints once, after the loop",
    _BOOK_RUN + r'''
_t = _tree()
_inside = _in_loops(_t)
_tprints = [_n for _n in _prints(_t) if _mentions(_n, 'total')]
_resets = [_n for _n in _ast.walk(_t) if _kind(_n) == 'Assign' and _kind(_n.value) == 'Constant'
           and _B.any(_kind(_x) == 'Name' and _x.id == 'total' for _x in _n.targets) and _B.id(_n) in _inside]
_own = globals().get('total')
for _vals in __CASES__:
    _ns, _rows, _err, _book, _e = _book_case(_vals)
    assert _err != 'ENDLESS', 'Make sure every loop can end.' + _e
    assert not _err.startswith('KeyError'), (
        'Let the loop read every cost with `.values()`. Spell names typed by hand are not in every book. With '
        'another book, Python stopped: ' + _err + '.' + _e)
    assert not _err, _stop(_err, _e)
    _want = _B.sum(_book.values())
    _got = _ns.get('total')
    assert 'total' in _ns, 'Make `total`: start it at 0 above the loop, then add each cost to it.' + _e
    if not _close(_got, _want):
        _last = _B.list(_book.values())[-1]
        assert not (_resets and _close(_got, _last)), (
            'Move `total = 0` above the loop. Inside it, the total starts again every pass, so only the last cost '
            'counts.' + _e)
        assert not (_B.len(_book) > 1 and _close(_got, _last)), (
            'Add each cost to the total: `total = total + cost`. Your total held only the last cost.' + _e)
        assert not (_vals is not None and _close(_got, _own)), (
            'Add up the costs from `spell_book`, so `total` follows the book. Yours stayed the same, typed by hand.'
            + _e)
        assert False, ('Add every cost to `total`: it should be ' + _B.str(_want) + ', and it is ' + _shv(_got) + '.'
                       + _e)
    assert _tprints, 'Print `total` after the loop.'
    assert [_n for _n in _tprints if _B.id(_n) not in _inside], (
        'Print `total` once, after the loop: take the indent off the print line. Inside the loop, it prints every '
        'pass.')
    assert [_l for _l in _rows if _want in _ints(_l)], 'Print `total` after the loop: `print("Total: " + str(total))`.' + _e
''',
    OWN=BOOK,
    CASES=BOOK_CASES,
)

USES_VALUES = (
    "the costs come from .values()",
    "assert 'attr:values' in _concept_tokens(_source), ('This step is for `.values()`: `for cost in "
    "spell_book.values():`. Adding up the costs from `.items()` works too, but meet `.values()` here.')\n"
    "import ast as _ast\n"
    "import builtins as _B\n"
    "_tr = _ast.parse(_source)\n"
    "def _has_values(_node):\n"
    "    return [_x for _x in _ast.walk(_node) if _B.type(_x).__name__ == 'Attribute' and _x.attr == 'values']\n"
    "_fed = [_n for _n in _ast.walk(_tr) if (_B.type(_n).__name__ == 'For' and _has_values(_n.iter)) or "
    "(_B.type(_n).__name__ == 'Call' and _B.type(_n.func).__name__ == 'Name' and _n.func.id == 'sum' "
    "and _has_values(_n))]\n"
    "assert _fed, ('Let `.values()` hand over the costs you add: `for cost in spell_book.values():`. Yours uses "
    "`.values()`, but the total does not come from it.')",
)

SPELL_COSTS = dict(
    id="spell-costs",
    title="Try it: the spell book's costs",
    martu=(
        "Your turn. Walk the spell book twice: once with `.items()` for each name and its cost, once with "
        "`.values()` for the costs alone."
    ),
    names=["spell_book", "name", "cost", "total"],
    starter=BOOK_STARTER,
    checkpoints=[
        dict(
            id="each-spell",
            text="Print each spell's name and cost on one line, like `Glow: 2`. Use `.items()`.",
            dictated=False,
            hints=[
                "Look at task 1. `.items()` hands over each name with its cost, as a pair. Give the pair two names "
                "in the `for` line.",
                "Two names, then `in`, then the book with `.items()`. The cost is a number, so it needs `str()` "
                "before you glue it.",
                "With other names:\n```python\nfor item, count in pack.items():\n"
                "    print(item + \": \" + str(count))\n```\nTwo names in the `for` line, one for each half of the pair.",
                "Write `for name, cost in spell_book.items():` under `# 1.`, then indent `print(name + \": \" + str(cost))` "
                "under it.",
            ],
            checks=[EACH_SPELL, USES_ITEMS],
            pass_line="Mar'tu: Every spell, and what it costs. Good.",
        ),
        dict(
            id="add-the-costs",
            text="Add up every cost in `total`, with `.values()`. Then print `total` once, after the loop.",
            dictated=False,
            hints=[
                "Look at task 2. `total = 0` goes *above* the loop, and the print goes *after* it.",
                "`.values()` hands over the costs alone. Each pass, add the one cost to `total`.",
                "With other names:\n```python\ncount = 0\nfor n in pack.values():\n    count = count + n\n"
                "print(count)\n```\n`count` starts above the loop. Its print sits after it, at the left edge.",
                "Write `total = 0`, then `for cost in spell_book.values():` with `total = total + cost` under it, "
                "then `print(\"Total: \" + str(total))` with no indent.",
            ],
            checks=[BOOK_TOTAL_CHECK, USES_VALUES],
            pass_line="Gearshift: Eleven mana for the whole book. Visor dims. Noted.",
        ),
    ],
    solution=BOOK_SOLUTION,
    partials=[_book(BOOK_EACH)],
    assemble=dict(
        lines=[line for line in BOOK_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["for name, cost in spell_book:", "    total = 0", "for pair in spell_book.items():"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Pairs out of the book",
            text=(
                "```text\nspell_book.items()\n(\"Glow\", 2)\n(\"Warm Hands\", 3)\n(\"Lantern Ward\", 6)\n```\n"
                "`for name, cost in ...` gives each pair two names."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Pass 1: `name` is `\"Glow\"`, `cost` is 2.\n"
                "2. Pass 2: `\"Warm Hands\"`, 3. Pass 3: `\"Lantern Ward\"`, 6.\n"
                "3. `.values()` hands over 2, 3, 6: add them up for 11."
            ),
        ),
    ],
    takeaway="`for name, cost in book.items():` gives each key and its value. `.values()` gives the values alone.",
    wrong_answers=[
        dict(why="the starter", code=BOOK_STARTER, fails_at=1, message_contains="Print every spell"),
        dict(why="two names with no .items() (each key is unpacked)",
             code=_book("for name, cost in spell_book:\n    print(name + \": \" + str(cost))\n"), fails_at=0,
             message_contains="too many values to unpack"),
        dict(why="one name for the pair (prints the tuple)",
             code=_book("for pair in spell_book.items():\n    print(pair)\n"), fails_at=1,
             message_contains="two names"),
        dict(why="the names only, no cost", code=_book("for name in spell_book:\n    print(name)\n"), fails_at=1,
             message_contains="Add the cost"),
        dict(why="the whole spell book printed", code=_book("for name in spell_book:\n    print(spell_book)\n"),
             fails_at=1, message_contains="whole spell book"),
        dict(why="the lines typed by hand",
             code=_book("print(\"Glow: 2\")\nprint(\"Warm Hands: 3\")\nprint(\"Lantern Ward: 6\")\n"), fails_at=1,
             message_contains="typed by hand"),
        dict(why="spell_book[name] instead of .items() (works, but the try-it meets .items())",
             code=_book("for name in spell_book:\n    print(name + \": \" + str(spell_book[name]))\n"), fails_at=1,
             message_contains="meet `.items()`"),
        dict(why=".items() made, but not looped over (the loop reads spell_book[name])",
             code=_book("pairs = spell_book.items()\nfor name in spell_book:\n"
                        "    print(name + \": \" + str(spell_book[name]))\n"), fails_at=1,
             message_contains="somewhere else"),
        dict(why=".items without brackets", code=_book("for name, cost in spell_book.items:\n    print(name)\n"),
             fails_at=0, message_contains="not iterable"),
        dict(why="the example's dictionary name copied",
             code=_book("for item, count in pack.items():\n    print(item + \": \" + str(count))\n"), fails_at=0,
             message_contains="not defined"),
        dict(why="task 1 done, no total yet", code=_book(BOOK_EACH), fails_at=2, message_contains="Make `total`"),
        dict(why="the total reset inside the loop",
             code=_book(BOOK_EACH, "for cost in spell_book.values():\n    total = 0\n    total = total + cost\n"
                                   "print(\"Total: \" + str(total))\n"),
             fails_at=2, message_contains="Move `total = 0` above the loop"),
        dict(why="the total printed inside the loop (every pass)",
             code=_book(BOOK_EACH, BOOK_TOTAL.replace("print(\"Total", "    print(\"Total")), fails_at=2,
             message_contains="Print `total` once"),
        dict(why="the total typed by hand", code=_book(BOOK_EACH, "total = 11\nprint(\"Total: \" + str(total))\n"),
             fails_at=2, message_contains="typed by hand"),
        dict(why=".values() only printed; the total added from .items()",
             code=_book(BOOK_EACH, "total = 0\nfor name, cost in spell_book.items():\n    total = total + cost\n"
                                   "print(\"Total: \" + str(total))\nprint(spell_book.values())\n"),
             fails_at=2, message_contains="the total does not come from it"),
        dict(why="added up from .items() (works, but the step meets .values())",
             code=_book(BOOK_EACH, "total = 0\nfor name, cost in spell_book.items():\n    total = total + cost\n"
                                   "print(\"Total: \" + str(total))\n"),
             fails_at=2, message_contains="meet `.values()`"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="dict-items,dict-values,accumulate", solo="false",
             dictates="", foreign_names="pack,item,count,n") + "\n"
        "5-A1 try-it. CP1 [ND] `.items()` with two names; CP2 [ND] a total from `.values()` (`sum(spell_book.values())` "
        "passes too). Reruns with {Mend: 4, Spark: 1} and a 4-spell book. Caught: two names with no `.items()` "
        "(ValueError: too many values to unpack), one name for the pair (prints the tuple), keys only, the whole "
        "book, typed lines, `.items` with no brackets, the example's `pack`, the reset inside the loop, the total "
        "printed every pass, a typed total. Reading `spell_book[name]`, or adding from `.items()`, gives the "
        "right output but gets a kind second check that names the tool this try-it is for; that check also wants "
        "`.items()` in the `for` line and `.values()` feeding the total (a `for` line or `sum()`), not just "
        "somewhere in the code."
    ),
)

ARTICLE_5A1 = dict(
    kind="article",
    id="looping-over-a-dictionary",
    title="Looping Over a Dictionary",
    optional=True,
    minutes=10,
    summary="Walk a whole dictionary: its keys, its values, or each key with its value, using `.items()`.",
    introduces=["attr:items", "attr:keys", "attr:values", "node:Tuple"],
    body=(
        "A spell book is a [[dictionary]]: a name for each spell, and a cost beside it. You know how to read one "
        "key. Tonight, every key.\n"
        "A plain `for` loop over a dictionary walks its [[key|keys]], in the order they were put in. The first "
        "example shows it.\n"
        "Most of the time you want each key *and* its value. [[.items()|`.items()`]] hands them back in pairs. Each pair is a "
        "[[tuple]]: two values in round brackets, like `(\"rope\", 2)`. You met tuples in the Tuples article. Write "
        "two names on the left, and Python puts one value in each. The second example shows that on its own.\n"
        "So `for name, cost in spell_book.items():` gives `name` the key and `cost` its value, every pass. Two "
        "names, two things in each pair. Write only one name, and you get the whole pair, brackets and all.\n"
        "[[.keys()|`.keys()`]] hands back only the keys, and [[.values()|`.values()`]] only the values. `sum(spell_book.values())` adds "
        "up every cost in the book.\n"
        "You have seen this shape in the campaign: every hero's sheet was a dictionary, and Lucky's pack could be "
        "one too."
    ),
    examples=[
        dict(code="pack = {\"rope\": 2, \"lamp\": 1}\nfor item in pack:\n    print(item)\n", output="rope\nlamp"),
        dict(code="item, count = (\"rope\", 2)\nprint(item)\nprint(count)\n", output="rope\n2"),
        dict(
            code=(
                "pack = {\"rope\": 2, \"lamp\": 1}\n"
                "print(list(pack.items()))\n"
                "for item, count in pack.items():\n"
                "    print(item + \": \" + str(count))\n"
            ),
            output="[('rope', 2), ('lamp', 1)]\nrope: 2\nlamp: 1",
        ),
        dict(
            code=(
                "pack = {\"rope\": 2, \"lamp\": 1}\n"
                "print(list(pack.keys()))\n"
                "print(list(pack.values()))\n"
                "print(sum(pack.values()))\n"
            ),
            output="['rope', 'lamp']\n[2, 1]\n3",
        ),
    ],
    exercises=[SPELL_COSTS],
    notes=(
        "Article 5-A1 (O). Intro attr:items, attr:keys, attr:values (and node:Tuple, as the spec lists it; the gate "
        "first opened it in u04c). Prerequisite (2.12 rule 2): the Tuples article (u04c, `tuples`), recapped on the "
        "page (the second example unpacks a pair on its own). Examples use Lucky's `pack` (foreign to the try-it's `spell_book`), and every example line "
        "fits a phone (36 characters)."
    ),
)


ITEMS = [PROJECT_5P, CHALLENGE_FORECAST, EXTRA_6X, LESSON_5C, ARTICLE_5A1]
