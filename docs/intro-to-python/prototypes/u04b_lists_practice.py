"""Unit 4 "Lists", part b: Extra practice 4X "Reading the Wall" (pool: 3B-04, 3B-05), Project 3P1 "Oogrish's
Training Log" (pool), Lesson 3C "More List Tools" (optional, with its SOLO) and Quiz 3B (optional).

Spec: design/curriculum.md, "## Unit 4 · Lists", "### Extra practice 4X [pool] and the optional items", items 4 to 7.
Not in this file (by assignment): Articles 3-A1 Tuples and 3-A2 `zip()`, Project 3P2 "The Basement Inventory",
Quick Check 3 and the Lists cheatsheet.
Introduces attr:count (3B-04), attr:insert and attr:pop (3C-01), attr:remove and op:In (3C-02), call:max, call:min
and call:sum (3C-03). No `for` (Unit 6), no f-strings (Unit 9), no dictionaries (Unit 5), no `not in` (u05a), no
keyword arguments (u07c), no tuples. Recipes stay inside Unit 3's planned concepts: `def` with a parameter and a
`return` (Project task 4, Quiz 3B question 8).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN lists there:
`party.members` (the loop in the spell-book and mana-bars parts), the chalk wall's gaps (Module 2, the chalk-wall
beat) and Mar'tu's four dialogue options (Module 1, program-dialogue-options), four strings in a row. Campaign
links are "you've seen this, now you'll get it" moments. Every student has their own device; pair talk is
optional and every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them, as Units 2 and 3): hints[0] Where to look (point),
the middle hints Teach me (a tiny example with other names), the last hint Show me how: the step's own line in
backticks (``Write `x = 1`.``), whose start up to its first `(` or `=` becomes Start me off. another_way, assemble
(More structure), then Compare. Where the start would hand over the step's decision (fix-a-mark's position), the
last hint's first code span has no `=`, so there is no Start me off.
In debug steps hints[0] is "Read Python's last line" (for a quiet bug: what the program printed). Terminology (2.9): "variable" (Mar'tu may still say
"box"); "recipe", "ingredient" and "hands back" for functions, as in Unit 3; chalk-wall values are "gaps".

Check builders (the rerun idea is Units 1-2's CMB: the student's program again, with a starter line changed):
  _rerun(values, appends)  re-runs the student's code with top-level `name = [...]` lines replaced, and the item of
                a top-level `name.append(...)`, `name = name + [...]` or `name += [...]` replaced (so a line typed
                from the student's own log cannot hide). Prints go to a private buffer.
  _case(None)   the student's own run (no evidence bracket); _case(values) a rerun.
  _same_row     a printed answer must come from the SAME print line in the student's own run and in each rerun, so
                typing one answer per wall the evidence bracket showed (`print(1)`, `print(2)`, `print(3)`) fails.
                Runs that print a different number of lines (an `if` that prints) fall back to "printed anywhere".
  _handback     `chalk_wall = chalk_wall.insert(...)` / `log = log.append(...)` / `= .pop()`: names the tool that
                handed back `None` (or the popped item) instead of a generic "the wall became None".
  _stop(..., _ifix=)  a step's own advice for an IndexError on a shorter rerun (a typed position), where the
                default "count from the end with `[-1]`" would point the wrong way (min, sum, sorted()[0]).
  Messages lead with the fix, then say what happened, then give the evidence in brackets at the end,
  "(Mar'tu's check tried `chalk_wall = [44, 39, 45, 41]`, only inside the check.)", about 35 words or fewer.
  A starter line still holding its placeholder is named as the starter's; a starter line that went missing gets
  "Keep the line ... from the starter". Messages use invented values only and never repeat a student's own text
  (2.11): the project's checks say "a drill you typed", never the student's words.
The class's slips for this unit, each proven by a wrong_answers entry (see each exercise):
  index from 0 (project task 3 `log[1][1]`, 3C-01 `.insert(3, 47)`); `-1` versus `len` (project task 4
  `training[len(training)]`, 3B-04 `chalk_wall[6]` on a shorter wall); `len` used as an index (project task 5
  `log[len(log)]`); append versus `+` versus a new list (project task 2); `.sort()` hands back None (3B-05, Quiz 3B);
  the slice end is left out (3B-05 `[-3:-1]`); values typed by hand instead of read from the list (3B-04, 3B-05,
  3C-03, project tasks 5-6); the example's list name copied (3B-04 `bells`, 3C-01 `jars`, 3C-03 `coins`); a copy
  changed instead of the original (3B-05 in-place `.sort()`, 3C-01 a slice, project task 3 `first = log[0][1]`);
  square brackets versus round ones (3B-04 `.count[48]`, 3C-03 and SOLO `max[chalk_wall]`, project task 1 tuples).
  Added by the check-breaker pass: index from 1 (3C-03 and SOLO `chalk_wall[1]`, 3C-02 `chalk_wall[1] == 32`: the
  rerun walls put the answer away from positions 0, 1 and -1); `x = x.sort()` (3B-05), `x = x.append()` (task 2),
  `x = x.insert()` / `.remove()` / `.pop()` (3C); `+` without inner brackets and two appends (task 2); a second
  name for the wall sorted in place, and a sort hidden by retyping the wall (3B-05); counting `min()` for the
  newest (3B-04); a label glued to `str(log[-1])` (task 5); `len(log[0])` (task 6); one typed answer per rerun
  wall (3B-04, 3C-03, SOLO, tasks 5-6).
Earlier checkpoints read the program's state even when a LATER line stops a rerun (a typed `[6]` in step 2 is step
2's message, not step 1's); the crash is reported by the first checkpoint whose own value is wrong.

Phone width (as u04a): fenced pictures, examples, predict code and quiz code keep lines to 36 characters or fewer.
The real wall (41 characters, 45 with Lucky's 99) stays whole on one line in editor code; Quiz 3B's slice question
keeps it in `setup` and shows it in the question text.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u04b
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# Shared by every check: the rerun, the evidence bracket and a few readers. Plain Python, run in the student's
# namespace after their code, so every name starts with `_` and builtins come from `_B` (a student's `max = 48`
# can't break a check).
_PRE = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import builtins as _B
def _sh(_v):
    _k = type(_v).__name__
    if _k == 'str':
        return '"' + _v + '"'
    if _k in ('list', 'tuple'):
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    return _B.str(_v)
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _one_item(_node):
    return type(_node).__name__ == 'List' and _B.len(_node.elts) == 1
def _rerun(_values=None, _appends=None):
    _tree = _ast.parse(_source)
    _vals = _B.dict(_values or {})
    _apps = _B.dict(_appends or {})
    _seen = []
    for _n in _tree.body:
        _k = type(_n).__name__
        if _k == 'Assign' and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name':
            _id = _n.targets[0].id
            _v = _n.value
            if _id in _vals and type(_v).__name__ in ('List', 'Tuple', 'Constant'):
                _n.value = _lit(_vals[_id], _v)
                _seen.append(_id)
            elif (_id in _apps and type(_v).__name__ == 'BinOp' and type(_v.op).__name__ == 'Add'
                  and _one_item(_v.right)):
                _v.right.elts[0] = _lit(_apps[_id], _v.right.elts[0])
                _seen.append(_id + '.append')
        elif (_k == 'AugAssign' and type(_n.target).__name__ == 'Name' and _n.target.id in _apps
              and type(_n.op).__name__ == 'Add' and _one_item(_n.value)):
            _n.value.elts[0] = _lit(_apps[_n.target.id], _n.value.elts[0])
            _seen.append(_n.target.id + '.append')
        elif _k == 'Expr' and type(_n.value).__name__ == 'Call':
            _f = _n.value.func
            if (type(_f).__name__ == 'Attribute' and _f.attr == 'append' and type(_f.value).__name__ == 'Name'
                    and _f.value.id in _apps and _B.len(_n.value.args) == 1
                    and type(_n.value.args[0]).__name__ in ('List', 'Name')):
                _n.value.args[0] = _lit(_apps[_f.value.id], _n.value.args[0])
                _seen.append(_f.value.id + '.append')
    _ast.fix_missing_locations(_tree)
    _ns = {'__name__': '__main__'}
    _keep_out = _sys.stdout
    _buf = _io.StringIO()
    _err = ''
    _sys.stdout = _buf
    try:
        _B.exec(_B.compile(_tree, 'main.py', 'exec'), _ns)
    except Exception as _e:
        _err = type(_e).__name__ + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _keep_out
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    return _ns, _rows, _err, [_x for _x in _vals if _x not in _seen], _seen
def _case(_vals, _apps=None):
    # None: the student's own run, as it is now (no evidence bracket).
    if _vals is None:
        return globals(), _lines(), '', [], []
    return _rerun(_vals, _apps)
def _ev(_vals, _apps=None):
    if _vals is None:
        return ''
    _bits = []
    for _k, _v in _vals.items():
        if type(_v).__name__ == 'list' and _v and type(_v[0]).__name__ == 'list':
            _bits.append('`' + _k + '` with ' + _B.str(_B.len(_v)) + ' other drills')
        else:
            _bits.append('`' + _k + ' = ' + _sh(_v) + '`')
    _t = " (Mar'tu's check tried " + ' and '.join(_bits)
    for _k, _v in (_apps or {}).items():
        _t += ', then appended `' + _sh(_v) + '`'
    return _t + ', only inside the check.)'
def _keep(_name):
    return ('Keep the line `' + _name + " = [...]` from the starter, so Mar'tu's check can try another list there.")
def _stop(_vals, _apps, _err, _fix='Make it work for another list too.', _ifix=None):
    # _ifix: this step's own fix for an IndexError (a position typed for one length), when `[-1]` is not it.
    if _err.startswith('IndexError'):
        _fix = _ifix or 'Count from the end with `[-1]`, so it works for a list of any length.'
    return _fix + ' With another list, Python stopped: ' + _err + '.' + _ev(_vals, _apps)
def _handback(_name, _uses):
    # `name = name.tool(...)` at the top level: the tool changed the list and handed back something else.
    # _uses: the line to write for each tool, e.g. {'insert': 'chalk_wall.insert(2, 47)'}.
    for _n in _ast.parse(_source).body:
        if (type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id == _name and type(_n.value).__name__ == 'Call'
                and type(_n.value.func).__name__ == 'Attribute' and type(_n.value.func.value).__name__ == 'Name'
                and _n.value.func.value.id == _name):
            _t = _n.value.func.attr
            _use = _uses.get(_t, _name + '.' + _t + '(...)')
            if _t == 'pop':
                return ('Keep the list in `' + _name + '`: write `' + _use + '`. `' + _name + ' = ' + _name
                        + '.pop()` swapped the whole list for the one item it popped.')
            return ('Write `' + _use + '` on its own line, with no `' + _name + ' = ` in front. `.' + _t
                    + '()` changes the list itself and hands back `None`, so `' + _name + '` became `None`.')
    return ''
def _rows_with(_rows, _test):
    return [_i for _i, _l in _B.enumerate(_rows) if _test(_l)]
def _same_row(_own_rows, _own_hits, _rows, _hits):
    # One print line answers in both runs. (Runs that print a different number of lines, or a student's own run
    # the reader can't match, are not compared.)
    if _B.len(_own_rows) != _B.len(_rows) or not _own_hits:
        return _B.bool(_hits)
    return _B.bool(_B.set(_own_hits) & _B.set(_hits))
def _nums(_l):
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?!\d)(?!\.\d)', _l)]
def _ends(_rows):
    return [((_l.split() or [''])[-1]).rstrip('.,!?;:)') for _l in _rows]
def _calls_of(_attr):
    return [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call'
            and type(_n.func).__name__ == 'Attribute' and _n.func.attr == _attr]
def _starter_line(_name, _value):
    for _n in _ast.parse(_source).body:
        if (type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id == _name and type(_n.value).__name__ == 'Constant'
                and _B.repr(_n.value.value) == _B.repr(_value)):
            return True
    return False
def _is_int(_v):
    return type(_v).__name__ == 'int'
def _is_num(_v):
    return type(_v).__name__ in ('int', 'float')
'''


def chk(label, body, **subs):
    """A check: the shared _PRE, then `body` with each __NAME__ replaced by repr(value)."""
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    return (label, _PRE + body)


WALL = [48, 48, 47, 46, 44, 41, 37]
WALL_LINE = "chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of lists)
# ---------------------------------------------------------------------------------------------

UNIT = dict(
    id="lists",
    order=4,
    title="Lists",
    subtitle="The Chalk Wall",
    published=True,
    martu_intro=(
        "Seven numbers on my wall. I could give each one its own box. I could also lose my mind. A list keeps "
        "them together, in order, yes?\n"
        "You have met lists already. `party.members` was one: the four of you, in order, under one name. "
        "Tonight we read a list closely, one position at a time."
    ),
    goals=[
        "Make a [[list]] with square brackets and commas",
        "Read an item by its [[index|position]], counting from 0, and from the end with `-1`",
        "Change an item by its position, grow a list with `.append()`, and join two lists with `+`",
        "Count items with `len()`, and know the last position is `len - 1`",
        "Read a list inside a list, like `roster[3][1]`",
        "Count with `range()`, cut a [[slice]] like `[-3:]`, and sort with `sorted()`",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

# New terms only (this part's tools). u04a defines the unit's core list terms; Units 1-3 define theirs.
GLOSSARY = [
    dict(
        term=".count()",
        aliases=["count()"],
        plain="Counts how many items in a list are the same as the value you hand it. A value that isn't there counts 0.",
        example="[48, 48, 47].count(48)",
    ),
    dict(
        term=".insert()",
        aliases=["insert()"],
        plain=(
            "Puts a new item into a list at a position: the position first, then the value. Every item after it "
            "moves one place along."
        ),
        example="wall.insert(2, 47)",
    ),
    dict(
        term=".pop()",
        aliases=["pop()"],
        plain=(
            "Takes the last item off a list and hands it back. `.pop(0)` takes the first item instead. The list "
            "gets shorter."
        ),
        example="newest = wall.pop()",
    ),
    dict(
        term=".remove()",
        aliases=["remove()"],
        plain=(
            "Takes the first item that is the same as the value you hand it out of a list. You give the value, not "
            "the position. If the value isn't there, Python stops with a ValueError."
        ),
        example="wall.remove(99)",
    ),
    dict(
        term="in",
        aliases=["in (a list)"],
        plain="Asks whether a value is somewhere in a list. Python answers `True` or `False`.",
        example="32 in wall",
    ),
    dict(
        term="max() and min()",
        aliases=["max()", "min()"],
        plain="`max()` hands back the biggest item in a list, and `min()` the smallest, wherever they are.",
        example="max([41, 46, 39])",
    ),
    dict(
        term="sum()",
        aliases=["sum"],
        plain="Adds up every number in a list and hands back the total.",
        example="sum([3, 9, 2])",
    ),
    dict(
        term="ValueError",
        aliases=["value error"],
        plain=(
            "The value is the right kind, but Python can't use it here. With a list, often `.remove()` of a "
            "value that is not in it."
        ),
        example="[48, 47].remove(99)\nValueError: list.remove(x): x not in list",
    ),
]


# =============================================================================================
# Extra practice 4X "Reading the Wall" (pool: 3B-04, 3B-05)
# =============================================================================================

# ---- 3B-04 how-many-times: count the 48s ----------------------------------------------------------------

COUNT_STARTER = WALL_LINE + "times_48 = 0\nprint(times_48)\n"


def _count(times="times_48 = chalk_wall.count(48)", newest="print(chalk_wall.count(chalk_wall[-1]))", extra=""):
    return WALL_LINE + f"{times}\nprint(times_48)\n" + (f"{newest}\n" if newest else "") + extra


COUNT_SOLUTION = _count()

COUNT_48S = chk(
    "times_48 counts the 48s",
    r'''
# Only this step's own line: a quoted count in a later line is that step's slip, not this one's.
_quoted = [_n for _n in _calls_of('count') if _n.args and type(_n.args[0]).__name__ == 'Constant'
           and _n.args[0].value == '48']
_own = globals().get('times_48')
for _vals, _want in ((None, None), ({'chalk_wall': [48, 47, 48, 48, 45]}, 3), ({'chalk_wall': [50, 49, 47]}, 0)):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _wall = _ns.get('chalk_wall')
    if _want is None:
        _want = _wall.count(48) if type(_wall).__name__ == 'list' else 2
    _got = _ns.get('times_48')
    if _is_int(_got) and _got == _want:
        continue
    assert not _quoted, 'Take the quotes off: `"48"` is text, and the wall holds numbers. Use `chalk_wall.count(48)`.'
    assert not _err, _stop(_vals, None, _err)
    assert 'times_48' in _ns, 'Keep the line `times_48 = ` from the starter, and put `chalk_wall.count(48)` after the `=`.'
    assert not (_got == 0 and _starter_line('times_48', 0)), (
        "`times_48` still holds the starter's `0`. Replace the 0 with `chalk_wall.count(48)`." + _ev(_vals))
    assert _is_int(_got), ('Make `times_48` hold a number: how many 48s, from `chalk_wall.count(48)`. It holds '
                           + _sh(_got) + '.' + _ev(_vals))
    assert not (type(_wall).__name__ == 'list' and _got == _B.len(_wall)), (
        'Use `.count(48)`: `len()` counts every gap, and `.count(48)` counts only the 48s.' + _ev(_vals))
    assert not (_vals is not None and _got == _own), ('Read it from the list: `chalk_wall.count(48)`. `times_48` '
                                                     'stayed ' + _sh(_got) + ', a number typed by hand.' + _ev(_vals))
    assert False, ('Count the 48s with `chalk_wall.count(48)`. `times_48` holds ' + _sh(_got) + ', not '
                   + _sh(_want) + '.' + _ev(_vals))
''',
)

COUNT_NEWEST = chk(
    "the newest gap is counted from the list",
    r'''
_counts = _calls_of('count')
_minus = [_n for _n in _counts if _n.args and type(_n.args[0]).__name__ == 'UnaryOp']
_quoted = [_n for _n in _counts if _n.args and type(_n.args[0]).__name__ == 'Constant'
           and type(_n.args[0].value).__name__ == 'str']
_typed = [_n for _n in _counts if _n.args and type(_n.args[0]).__name__ == 'Constant'
          and _n.args[0].value != 48]
_low = [_n for _n in _counts if _n.args and any(type(_x).__name__ == 'Name' and _x.id in ('min', 'sorted')
                                                for _x in _ast.walk(_n.args[0]))]
def _pick(_l):
    # The count can come first or last on its line: `1 time for 37` or `37 shows up 1 time`.
    _v = _nums(_l)
    return _v[:1] + _v[-1:]
_w0 = globals().get('chalk_wall')
_own_rows = _lines()
_own_want = _w0.count(_w0[-1]) if type(_w0).__name__ == 'list' and _w0 else 1
_own_hits = _rows_with(_own_rows, lambda _l: _own_want in _pick(_l))
# [44, 39, 40, 40]: the newest gap (40) is not the shortest (39), so counting min() or sorted()[0] fails.
for _vals in (None, {'chalk_wall': [44, 39, 40, 40]}, {'chalk_wall': [37, 41, 37, 37]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _wall = _ns.get('chalk_wall')
    _want = _wall.count(_wall[-1]) if type(_wall).__name__ == 'list' and _wall else 1
    _hits = _rows_with(_rows, lambda _l: _want in _pick(_l))
    if _hits and (_vals is None or _same_row(_own_rows, _own_hits, _rows, _hits)):
        continue
    assert not _err, _stop(_vals, None, _err)
    assert not _quoted, ('Take the quotes off: text in quotes is never on the wall. Count the newest gap itself: '
                         '`chalk_wall.count(chalk_wall[-1])`.')
    assert not _minus, ('Put the newest gap in the brackets: `chalk_wall.count(chalk_wall[-1])`. `-1` on its own is '
                        'just the number -1, and the wall has none.')
    assert not _typed, ('Ask with the newest gap itself, `chalk_wall[-1]`, so it works for any wall. Your line '
                        'counts a number you typed.' + _ev(_vals))
    assert not _low, ('Count the newest gap, `chalk_wall[-1]`. The newest gap is not always the shortest.'
                      + _ev(_vals))
    assert not _hits, ('Let one line work it out from the list: `print(chalk_wall.count(chalk_wall[-1]))`. A number '
                       'typed for each wall cannot follow a new one.' + _ev(_vals))
    assert False, ('Print `chalk_wall.count(chalk_wall[-1])`: how many times the newest gap shows up. '
                   + ('On your wall' if _vals is None else "On Mar'tu's other wall") + ' it is ' + _B.str(_want)
                   + '.' + _ev(_vals))
''',
)

COUNT_BONUS = chk(
    "the answer follows the wall",
    r'''
for _vals, _want in (({'chalk_wall': [48, 47, 48]}, 'True'), ({'chalk_wall': [48, 46, 45]}, 'False')):
    _ns, _rows, _err, _miss, _seen = _rerun(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_vals, None, _err)
    _e = _ends(_rows)
    assert _want in _e and not (_want == 'False' and 'True' in _e), (
        'Print the question itself, `chalk_wall.count(48) > 1`, so Python answers True or False for any wall.'
        + _ev(_vals))
''',
)

HOW_MANY_TIMES = dict(
    id="how-many-times",
    title="How many times?",
    martu=(
        "Oogrish ran a finger down my wall. *Every forty-eight hours. At first.* Twice, the gap was 48.\n"
        "You could count by eye. On a long wall you would lose count, yes? Ask the list instead. "
        "[[.count()]] counts how many items are the same as the value in the brackets.\n"
        "The dot means: ask this list to do something. Round brackets after it, like every call."
    ),
    introduces=["attr:count"],
    example="bells = [3, 5, 3, 3]\nprint(bells.count(3))\n",
    example_output="3",
    names=["chalk_wall", "times_48"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code="marks = [9, 9, 4, 9]\nprint(marks.count(9))\nprint(marks.count(7))\n",
        choices=["3\nERROR", "2\n0", "3\n0", "9\n7"],
        answer=2,
        explain=(
            "There are three 9s, so 3. There is no 7, and that is fine: `.count(7)` gives 0. "
            "No error, just nothing to count."
        ),
    ),
    pair_talk="Pair talk: count the 48s on the wall by eye. Agree on a number. Then each of you asks the list.",
    starter=COUNT_STARTER,
    checkpoints=[
        dict(
            id="count-the-48s",
            text="Make `times_48` count the 48s on the wall, with `.count()`.",
            dictated=False,
            hints=[
                "Line 2 still holds the starter's 0. Ask the list: its name, a dot, `count`, then the value in "
                "round brackets.",
                "`bells.count(3)` counts the 3s in `bells`. A number has no quotes.",
                "Write `times_48 = chalk_wall.count(48)` on line 2.",
            ],
            checks=[COUNT_48S],
            pass_line="Oogrish: Two forty-eights. At first. Steady, now.",
        ),
        dict(
            id="count-the-newest",
            text="Print how many times the newest gap shows up on the wall. Read the newest gap from the list.",
            dictated=False,
            hints=[
                "Two tools in one line: `.count()` counts, and the newest gap is `chalk_wall[-1]`. Put the newest "
                "gap inside the count's brackets.",
                "With other names: `bells.count(bells[0])` counts how many times the first bell shows up.",
                "Write `print(chalk_wall.count(chalk_wall[-1]))` on a new line.",
            ],
            checks=[COUNT_NEWEST],
            pass_line="Gearshift: Visor dims. One 37. So far.",
        ),
    ],
    solution=COUNT_SOLUTION,
    partials=[_count(newest=None)],
    assemble=dict(
        lines=[line for line in COUNT_SOLUTION.splitlines()],
        distractors=["times_48 = chalk_wall.count(\"48\")", "times_48 = len(chalk_wall)",
                     "print(chalk_wall.count(-1))"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Tally marks",
            text=(
                "```text\nwall:  48 48 47 46 44 41 37\n48?    ✓  ✓  .  .  .  .  .\n```\n"
                "`.count(48)` makes one tally mark for each 48: two."
            ),
        ),
        dict(
            angle="everyday",
            label="Counting socks",
            text=(
                "How many red socks are in the drawer? You don't count every sock. You count only the red ones. "
                "`len()` counts every sock. `.count(\"red\")` counts only the red ones."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`chalk_wall.count(48)`:\n"
                "1. Python takes the list `chalk_wall`.\n"
                "2. It checks each item: is it the same as 48?\n"
                "3. It hands back how many said yes: 2."
            ),
        ),
        dict(angle="shorter", text="`.count(x)`: how many items are `x`. Round brackets, no quotes on numbers."),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's bet",
        text=(
            "Lucky bets the wall has 48 more than once. On a new line, print whether `chalk_wall.count(48)` is more "
            "than 1."
        ),
        hints=["More than is `>`. Python answers True or False.",
               "Write `print(chalk_wall.count(48) > 1)` on a new line at the bottom."],
        checks=[COUNT_BONUS],
        solution=COUNT_SOLUTION + "print(chalk_wall.count(48) > 1)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "You read this wall in the campaign. Oogrish said *every forty-eight hours, at first*. The first two "
            "gaps were the same. `.count(48)` is that finger running down the column."
        ),
    ),
    takeaway="`chalk_wall.count(48)` counts how many items are 48. `len()` counts them all.",
    wrong_answers=[
        dict(why="the starter (placeholder 0)", code=COUNT_STARTER, fails_at=1, message_contains="starter's `0`"),
        dict(why="the count typed by hand (print(48) style)", code=_count(times="times_48 = 2"), fails_at=1,
             message_contains="typed by hand"),
        dict(why="48 in quotes", code=_count(times='times_48 = chalk_wall.count("48")'), fails_at=1,
             message_contains="quotes"),
        dict(why="len counts every gap", code=_count(times="times_48 = len(chalk_wall)"), fails_at=1,
             message_contains="len()"),
        dict(why="square brackets instead of round ones", code=_count(times="times_48 = chalk_wall.count[48]"),
             fails_at=0, message_contains="not subscriptable"),
        dict(why="the example's list name copied", code=_count(times="times_48 = bells.count(48)"), fails_at=0,
             message_contains="not defined"),
        dict(why="nothing in the brackets", code=_count(times="times_48 = chalk_wall.count()"), fails_at=0,
             message_contains="one argument"),
        dict(why="the newest count typed by hand", code=_count(newest="print(1)"), fails_at=2,
             message_contains="On Mar'tu's other wall it is 2"),
        dict(why="the newest gap printed, not its count (the student's own wall answers)",
             code=_count(newest="print(chalk_wall[-1])"), fails_at=2, message_contains="On your wall it is 1"),
        dict(why="the newest gap typed (37)", code=_count(newest="print(chalk_wall.count(37))"), fails_at=2,
             message_contains="a number you typed"),
        dict(why="-1 alone in the brackets", code=_count(newest="print(chalk_wall.count(-1))"), fails_at=2,
             message_contains="just the number -1"),
        dict(why="newest by a position from the start (6): a shorter wall has no 6",
             code=_count(newest="print(chalk_wall.count(chalk_wall[6]))"), fails_at=2,
             message_contains="[-1]"),
        dict(why="the shortest gap counted (min), not the newest", code=_count(newest="print(chalk_wall.count(min(chalk_wall)))"),
             fails_at=2, message_contains="not always the shortest"),
        dict(why="the shortest gap counted (a sorted copy's first), not the newest",
             code=_count(newest="print(chalk_wall.count(sorted(chalk_wall)[0]))"), fails_at=2,
             message_contains="not always the shortest"),
        dict(why="an answer typed for each wall the check showed (print the expected result directly)",
             code=_count(newest="print(1)\nprint(2)\nprint(3)"), fails_at=2, message_contains="typed for each wall"),
        dict(why="the newest gap in quotes (step 1 stays green)", code=_count(newest="print(chalk_wall.count(\"37\"))"),
             fails_at=2, message_contains="quotes"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="list-index,count", solo="false", dictates="",
             foreign_names="bells,marks") + "\n"
        "3B-04 (pool). Intro attr:count. CP1 [ND] count the 48s (goal-first text, teacher ruling; the last hint "
        "holds the line), CMB with two other walls ([48, 47, 48, 48, 45] -> 3, "
        "[50, 49, 47] -> 0), which fixes the v1 OUT-only check: a typed 2 fails. CP2 [ND] combines index and count "
        "(the newest gap's count): reruns [44, 39, 40, 40] (the newest is not the shortest, so counting `min()` or "
        "`sorted()[0]` fails) and [37, 41, 37, 37] read the first or last whole number of each printed line (`1 time "
        "for 37` passes), from the same print line as the student's own run. Catches: quoted 48 (always 0, and only "
        "this step's own quoted 48 turns step 1 red), `len` for count, `.count[48]` (square brackets: a crash), the "
        "example's `bells`, `.count(-1)`, a typed 37, a quoted \"37\", `chalk_wall[6]` (an IndexError on a shorter "
        "wall), one typed answer per wall. Bonus: count + comparison."
    ),
)

# ---- 3B-05 broken-spell-3b: a sort that hands back None, a slice one short ---------------------------------


def _broken3b(line2="shortest = chalk_wall.sort()[0]", slice_line="newest_three = chalk_wall[-3:-1]"):
    return (
        WALL_LINE
        + f"{line2}\n"
        + "print(\"Shortest: \" + str(shortest))\n"
        + f"{slice_line}\n"
        + "print(newest_three)\n"
    )


BROKEN_3B_STARTER = _broken3b()
BROKEN_3B_SOLUTION = _broken3b("shortest = sorted(chalk_wall)[0]", "newest_three = chalk_wall[-3:]")

SHORTEST_FROM_COPY = chk(
    "shortest is the smallest gap, and the wall keeps its order",
    r'''
_top = _ast.parse(_source).body
_walls = [_n for _n in _top if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
          and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'chalk_wall'
          and type(_n.value).__name__ == 'List']
# `other = chalk_wall`: a second name for the same wall, not a copy.
_alias = [_n.targets[0].id for _n in _top if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
          and type(_n.targets[0]).__name__ == 'Name' and type(_n.value).__name__ == 'Name'
          and _n.value.id == 'chalk_wall']
_sorts = [_n.func.value.id for _n in _calls_of('sort') if type(_n.func.value).__name__ == 'Name']
_hid = [_x for _x in _sorts if _x == 'chalk_wall' or _x in _alias]
# A `.sort()` and then the wall typed out again: the reruns would never see the wall change.
assert not (_hid and _B.len(_walls) > 1), (
    'Use `sorted(chalk_wall)[0]`, and keep just one `chalk_wall = [...]` line. Typing the wall out again after '
    '`.sort()` hides the change instead of leaving the wall alone.')
for _vals in (None, {'chalk_wall': [44, 39, 45, 41]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _wall = _ns.get('chalk_wall')
    _sorted = _B.sorted(_start)
    _s = _ns.get('shortest')
    if _wall == _start and _is_int(_s) and _s == _sorted[0]:
        continue
    assert not _err, _stop(_vals, None, _err, _ifix='Use `sorted(chalk_wall)[0]`: the first item of a sorted copy, '
                                                    'on a wall of any length.')
    assert 'shortest' in _ns, 'Keep `shortest = ` on line 2, and mend what comes after the `=`.'
    assert type(_s).__name__ != 'NoneType', ('Use `sorted(chalk_wall)[0]`: a sorted copy, then its first item. '
                                             '`.sort()` hands back `None`, so `shortest` holds `None`.')
    if _wall != _start:
        _same = [_x for _x in _hid if _x != 'chalk_wall']
        assert not (_same and _wall == _sorted), (
            '`' + _same[0] + ' = chalk_wall` gives the same wall a second name. It is not a copy, so `.sort()` sorted '
            'the wall itself. Use `sorted(chalk_wall)[0]`.' + _ev(_vals))
        assert _wall != _sorted, ('Keep the wall in its order: `.sort()` sorted `chalk_wall` itself. `sorted(chalk_wall)` '
                                  'sorts a copy and leaves the wall alone.' + _ev(_vals))
        assert False, 'Keep `chalk_wall` as it was: only `shortest` should change.' + _ev(_vals)
    if _is_int(_s) and _s == _sorted[0]:
        continue
    assert type(_s).__name__ != 'list', ('Take the first item of the sorted copy: `sorted(chalk_wall)[0]`. `shortest` '
                                         'holds a whole list.' + _ev(_vals))
    assert _s != _sorted[-1], ('The shortest gap comes first in a sorted copy: `[0]`, not `[-1]`.' + _ev(_vals))
    assert not (_vals is not None and _s == _start[-1]), ('Sort a copy first: `sorted(chalk_wall)[0]`. The newest '
                                                         'gap is not always the shortest.' + _ev(_vals))
    assert not (_vals is not None and _s == globals().get('shortest')), (
        'Read it from the wall: `sorted(chalk_wall)[0]`. `shortest` stayed ' + _sh(_s) + ', a number typed by hand.'
        + _ev(_vals))
    assert False, ('Make `shortest` the smallest gap: `sorted(chalk_wall)[0]`. It holds ' + _sh(_s) + ', not '
                   + _sh(_sorted[0]) + '.' + _ev(_vals))
''',
)

NEWEST_THREE = chk(
    "newest_three holds the three newest gaps",
    r'''
_ups = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Slice' and _n.lower is not None
        and type(_n.lower).__name__ == 'Constant' and _is_int(_n.lower.value) and _n.lower.value > 0]
for _vals in (None, {'chalk_wall': [44, 39, 45, 41]}, {'chalk_wall': [50, 49, 49, 48, 47, 45, 43, 40, 38]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _got = _ns.get('newest_three')
    if _got == _start[-3:]:
        continue
    assert not _err, _stop(_vals, None, _err)
    assert 'newest_three' in _ns, 'Keep `newest_three = ` from the starter, and mend the slice after the `=`.'
    assert _got != _start[-3:-1], ('Leave the end empty: `chalk_wall[-3:]`. A slice stops *before* its end number, '
                                   'so `[-3:-1]` leaves out the newest gap.' + _ev(_vals))
    assert _got != _start[-2:], 'Start three from the end: `[-3:]`. That slice holds two gaps.' + _ev(_vals)
    assert not _ups, ('Count from the end, so it works for a wall of any length: `chalk_wall[-3:]`.' + _ev(_vals))
    assert not (_vals is not None and _got == globals().get('newest_three')), (
        'Slice it from the wall: `chalk_wall[-3:]`. `newest_three` stayed ' + _sh(_got) + ', typed by hand.'
        + _ev(_vals))
    assert False, ('Make `newest_three` the three newest gaps: `chalk_wall[-3:]`. It holds ' + _sh(_got) + ', not '
                   + _sh(_start[-3:]) + '.' + _ev(_vals))
''',
)

BROKEN_SPELL_3B = dict(
    id="broken-spell-3b",
    title="Broken spell",
    martu=(
        "Gearshift wrote this spell to read the wall. It fizzles. Then it tells a small lie.\n"
        "Two slips. Read Python's last line first and mend that one. Then read what the program prints, and "
        "count the gaps."
    ),
    names=["chalk_wall", "shortest", "newest_three", "sorted"],
    predict=dict(
        q="Run Gearshift's spell. What happens?",
        choices=[
            "Shortest: 37\n[44, 41]",
            "ERROR: 'NoneType' object is not subscriptable",
            "Shortest: 37\n[44, 41, 37]",
        ],
        answer=1,
        explain=(
            "`.sort()` sorts the wall and hands back `None`: nothing. `None` has no `[0]`, so Python stops on line "
            "2. Like a recipe with no `return`."
        ),
    ),
    starter=BROKEN_3B_STARTER,
    checkpoints=[
        dict(
            id="sort-a-copy",
            text="Mend line 2 so `shortest` holds the shortest gap, and the wall keeps its order.",
            dictated=False,
            hints=[
                "Read Python's last line. Which value can't take `[0]`?",
                "Line 2. `chalk_wall.sort()` sorts the wall itself and hands back `None`. Nothing to take `[0]` "
                "from.",
                "`sorted(bells)` hands back a sorted copy, and `bells` keeps its order. `sorted(bells)[0]` is the "
                "smallest bell.",
                "Write `shortest = sorted(chalk_wall)[0]` on line 2.",
            ],
            checks=[SHORTEST_FROM_COPY],
            pass_line="Gearshift: Visor dims. Thirty-seven. The wall is still in order.",
        ),
        dict(
            id="three-not-two",
            text="Mend the slice so `newest_three` holds the three newest gaps.",
            dictated=False,
            hints=[
                "Read what the program printed last. How many gaps are in that list?",
                "Look at the slice on line 4. A slice stops *before* its end number.",
                "`bells[-2:]` is the last two bells: start two from the end, and leave the end empty, so the slice "
                "runs to the very end.",
                "Write `newest_three = chalk_wall[-3:]` on line 4.",
            ],
            checks=[NEWEST_THREE],
            pass_line="Mar'tu: Forty-four, forty-one, thirty-seven. Now the spell tells the truth.",
        ),
    ],
    solution=BROKEN_3B_SOLUTION,
    partials=[_broken3b(line2="shortest = sorted(chalk_wall)[0]")],
    assemble=dict(
        lines=BROKEN_3B_SOLUTION.splitlines(),
        distractors=["shortest = chalk_wall.sort()", "newest_three = chalk_wall[-3:-1]", "chalk_wall.sort()"],
    ),
    # Step 1 is the sort, so its angle comes first (Help's Another way opens on the first angle).
    another_way=[
        dict(
            angle="everyday",
            label="A copy, or the original",
            text=(
                "`sorted(chalk_wall)` is like copying the wall onto a scrap of paper and sorting the scrap. "
                "`.sort()` rubs out the wall and rewrites it in order. Mar'tu wants the wall left alone."
            ),
        ),
        dict(
            angle="picture",
            label="Where the slice stops",
            text=(
                "```text\n44  41  37\n-3  -2  -1   (end)\n```\n"
                "`[-3:-1]` starts at -3 and stops *before* -1: 44 and 41. "
                "`[-3:]` has no end number, so it runs to the end: 44, 41 and 37."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Run. Read the last line: `'NoneType' object is not subscriptable`.\n"
                "2. Line 2: `.sort()` handed back `None`. Use `sorted(chalk_wall)[0]`.\n"
                "3. Run again. Count the gaps in the last line printed: two.\n"
                "4. Line 4: leave the end of the slice empty."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "Unit 3's recipes with no `return` handed back `None`. `.sort()` is the same: it does its job, "
                "then hands back nothing."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="mana_bar = get_mana_bar(caster)",
        why=(
            "This line worked because `get_mana_bar` hands back the bar with `return`. `.sort()` hands back nothing, "
            "so `x = wall.sort()` stores `None`. Store what hands something back: `sorted(wall)`."
        ),
    ),
    takeaway="`.sort()` sorts the list itself and hands back `None`. `sorted(wall)` hands back a sorted copy.",
    wrong_answers=[
        dict(why="the starter: .sort() hands back None", code=BROKEN_3B_STARTER, fails_at=0,
             message_contains="not subscriptable"),
        dict(why="x = x.sort(): None stored, then printed",
             code=_broken3b("shortest = chalk_wall.sort()"), fails_at=1, message_contains="holds `None`"),
        dict(why="sorted in place, then [0] (the wall loses its order: a copy versus the original)",
             code=_broken3b("chalk_wall.sort()\nshortest = chalk_wall[0]"), fails_at=1,
             message_contains="in its order"),
        dict(why="the shortest typed by hand", code=_broken3b("shortest = 37"), fails_at=1,
             message_contains="typed by hand"),
        dict(why="x = x.sort(): the wall itself becomes None", code=_broken3b("chalk_wall = chalk_wall.sort()\n"
             "shortest = chalk_wall[0]"), fails_at=0, message_contains="NoneType"),
        dict(why="a second name for the wall, sorted (not a copy: the original changes)",
             code=_broken3b("sorted_wall = chalk_wall\nsorted_wall.sort()\nshortest = sorted_wall[0]"), fails_at=1,
             message_contains="second name"),
        dict(why="sorted in place, then the wall typed out again to hide it",
             code=_broken3b("chalk_wall.sort()\nshortest = chalk_wall[0]\n" + WALL_LINE.strip()), fails_at=1,
             message_contains="hides the change"),
        dict(why="the shortest read by a position from the start (6)", code=_broken3b("shortest = chalk_wall[6]"),
             fails_at=1, message_contains="sorted copy"),
        dict(why="the newest gap taken as the shortest", code=_broken3b("shortest = chalk_wall[-1]"), fails_at=1,
             message_contains="not always the shortest"),
        dict(why="the sorted copy kept whole", code=_broken3b("shortest = sorted(chalk_wall)"), fails_at=1,
             message_contains="whole list"),
        dict(why="the wrong end of the sorted copy", code=_broken3b("shortest = sorted(chalk_wall)[-1]"), fails_at=1,
             message_contains="comes first"),
        dict(why="the slice left one short (end not included)",
             code=_broken3b("shortest = sorted(chalk_wall)[0]"), fails_at=2, message_contains="*before*"),
        dict(why="a slice of two", code=_broken3b("shortest = sorted(chalk_wall)[0]", "newest_three = chalk_wall[-2:]"),
             fails_at=2, message_contains="two gaps"),
        dict(why="positions from the start (4:7) only fit a wall of seven",
             code=_broken3b("shortest = sorted(chalk_wall)[0]", "newest_three = chalk_wall[4:7]"), fails_at=2,
             message_contains="any length"),
        dict(why="the three gaps typed by hand",
             code=_broken3b("shortest = sorted(chalk_wall)[0]", "newest_three = [44, 41, 37]"), fails_at=2,
             message_contains="typed by hand"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="range-slice-sort,read-traceback", solo="false", dictates="",
             foreign_names="bells") + "\n"
        "3B-05 (pool). Two bugs, one checkpoint each: `chalk_wall.sort()[0]` (TypeError on None: a loud bug) and "
        "`[-3:-1]` (a quiet bug, one short). CP1 reruns with [44, 39, 45, 41] (the shortest is not the newest, so "
        "`chalk_wall[-1]` fails) and checks the wall keeps its order, so the in-place fix (`.sort()` then `[0]`) "
        "is caught where it happens, not later. Also caught at CP1: a second name for the wall (`other = chalk_wall`, "
        "then `other.sort()`: not a copy), and `.sort()` followed by the wall typed out again (the reruns replace "
        "every `chalk_wall = [...]` line, so that would hide the change). `min()` and a sliced copy sorted in place "
        "also pass (`min` is taught in 3C, a later optional lesson). CP2 reruns with a 4-gap and a 9-gap wall, so `[4:7]` fails. The predict shows Python's own message."
    ),
)

EXTRA_4X = dict(
    kind="lesson",
    id="extra-reading-the-wall",
    title="Extra practice: Reading the Wall",
    optional=True,
    minutes=6,
    summary="Count the marks with `.count()`, then mend a spell whose sort hands back nothing and whose slice is one short.",
    notes="4X pool (3B-04, 3B-05). Optional; feeds twins, the spaced queue and early finishers.",
    exercises=[HOW_MANY_TIMES, BROKEN_SPELL_3B],
)


# =============================================================================================
# Project 3P1 "Oogrish's Training Log" (pool, 25 min)
# =============================================================================================

LOG_STARTER = (
    "# Oogrish's training log.\n"
    "# Each drill is a pair:\n"
    "# [drill, score]\n"
    "\n"
    "# 1. Make log: 3 or more pairs.\n"
    "log = []\n"
    "\n"
    "# 2. Append one more drill.\n"
    "\n"
    "# 3. Add 2 to the first drill's\n"
    "#    score, by position.\n"
    "\n"
    "# 4. Hand back the newest score.\n"
    "def last_score(training):\n"
    "    return 0\n"
    "\n"
    "print(last_score([[\"kick\", 3], [\"jump\", 9]]))  # This should show 9\n"
    "\n"
    "# 5. Print the last drill and its\n"
    "#    score, on one line. Get the\n"
    "#    score from last_score(log).\n"
    "\n"
    "# 6. Print how many drills there\n"
    "#    are, with len().\n"
)

LOG_LITERAL = (
    "log = [\n"
    "    [\"cane parry\", 7],\n"
    "    [\"shield wall\", 5],\n"
    "    [\"slow breaths\", 9],\n"
    "]\n"
)
LOG_APPEND = "log.append([\"roll and rise\", 6])\n"
LOG_FIX = "log[0][1] = log[0][1] + 2\n"
LOG_RETURN = "    return training[-1][1]\n"
LOG_LAST = (
    "newest = log[-1]\n"
    "score = str(last_score(log))\n"
    "print(newest[0] + \": \" + score)\n"
)
LOG_LEN = "print(\"Drills: \" + str(len(log)))\n"


def _log(literal=None, append=None, fix=None, ret=None, last=None, count=None, extra=""):
    """The project program with any of its parts filled in (None = the starter's)."""
    code = LOG_STARTER
    if literal is not None:
        code = code.replace("log = []\n", literal)
    if append is not None:
        code = code.replace("# 2. Append one more drill.\n", "# 2. Append one more drill.\n" + append)
    if fix is not None:
        code = code.replace("#    score, by position.\n", "#    score, by position.\n" + fix)
    if ret is not None:
        code = code.replace("    return 0\n", ret)
    if last is not None:
        code = code.replace("#    score from last_score(log).\n", "#    score from last_score(log).\n" + last)
    if count is not None:
        code = code.replace("#    are, with len().\n", "#    are, with len().\n" + count)
    return code + extra


LOG_SOLUTION = _log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST, LOG_LEN)

# The other logs Mar'tu's check tries (invented drills; scores chosen so no two printed numbers can collide).
LOG_A, PAIR_A = [["kick", 11], ["leap", 14], ["block", 17], ["dodge", 19]], ["swim", 23]
LOG_B, PAIR_B = [["run", 31], ["duck", 37]], ["climb", 41]
LOG_RERUNS = [(LOG_A, PAIR_A), (LOG_B, PAIR_B)]

LOG_MADE = chk(
    "log is a list of drill-and-score pairs",
    r'''
_made = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
         and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'log']
assert _made, 'Keep the line `log = []` from the starter, and put your pairs inside its square brackets.'
# The first `log = ...` that holds something (a `log = []` above it, then appends, is still the starter's line).
_full = [_n for _n in _made if not (type(_n.value).__name__ in ('List', 'Tuple') and not _n.value.elts)]
_node = (_full or _made)[0].value
assert type(_node).__name__ != 'Tuple', 'Use square brackets for the list: `log = [ ... ]`. Round brackets make something else.'
try:
    _first = _ast.literal_eval(_node)
except Exception:
    _first = globals().get('log')
assert type(_first).__name__ == 'list', 'Make `log` a list: square brackets around the pairs, like `log = [["kick", 3], ["leap", 5]]`.'
_built = globals().get('log')
assert _first or not (type(_built).__name__ == 'list' and _built), (
    'Type your first 3 pairs inside the square brackets of `log = []` itself, like `log = [["kick", 3], ...]`. '
    'Keep `.append()` for task 2: one more drill.')
assert _first, '`log` is still empty. Put 3 pairs inside the square brackets, like `["kick", 3]`: a drill, then its score.'
for _p in _first:
    _k = type(_p).__name__
    assert _k != 'tuple', 'Put each pair in square brackets too: `["kick", 3]`, not round ones.'
    assert _k == 'list', ('Make each drill its own pair, in its own square brackets: `["kick", 3]`. `log` holds '
                          + _sh(_p) + ' on its own.')
    assert _B.len(_p) == 2, ('Give each pair two things: the drill, then its score. ' + _sh(_p) + ' holds '
                             + _B.str(_B.len(_p)) + '.')
    _d, _s = _p[0], _p[1]
    assert not (_is_num(_d) and type(_s).__name__ == 'str'), ('Put the drill first, then its score: `["kick", 3]`. '
                                                             + _sh(_p) + ' is the other way round.')
    assert type(_d).__name__ == 'str' and _d.strip(), 'Name each drill in quotes, first in its pair: `["kick", 3]`.'
    assert type(_s).__name__ != 'str', ('Take the quotes off the score: in ' + _sh(_p) + ', the score is text. '
                                        'Scores are numbers.')
    assert _is_num(_s), 'Make each score a number, like `3`.'
assert _B.len(_first) >= 3, 'Put at least 3 drills in `log`. It has ' + _B.str(_B.len(_first)) + '.'
''',
)

# Tasks 2 and 3 read the log as it stands when the program ends (or stops: a slip in a later task that stops a
# rerun is that task's message, not this one's).
LOG_APPENDED = chk(
    "one more pair is appended",
    r'''
_body = _ast.parse(_source).body
_lits = [_n for _n in _body if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
         and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'log' and type(_n.value).__name__ == 'List']
_bare = [_n for _n in _body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp'
         and type(_n.value.op).__name__ == 'Add']
_early = [_n for _n in _calls_of('append') if type(_n.func.value).__name__ == 'Name' and _n.func.value.id == 'log'
          and _lits and _n.lineno < _lits[-1].lineno]
for _L, _P in __RERUNS__:
    _ns, _rows, _err, _miss, _seen = _rerun({'log': _L}, {'log': _P})
    assert not _miss, _keep('log')
    _apps = {'log': _P} if 'log.append' in _seen else None
    _got = _ns.get('log')
    _k = _B.len(_L)
    _ok = (type(_got).__name__ == 'list' and _B.len(_got) == _k + 1 and type(_got[-1]).__name__ == 'list'
           and _B.len(_got[-1]) == 2 and type(_got[-1][0]).__name__ == 'str' and _is_num(_got[-1][1]))
    if _ok:
        continue
    assert not _err, _stop({'log': _L}, _apps, _err)
    assert type(_got).__name__ == 'list', (_handback('log', {'append': 'log.append(["swim", 6])'})
                                           or 'Keep `log` a list: add to it with `log.append([...])`.')
    # The drill and its score went in as two loose items: `log + ["swim", 6]`, or two appends.
    assert not (_B.len(_got) == _k + 2 and type(_got[-2]).__name__ == 'str' and _is_num(_got[-1])), (
        'Keep the drill and its score together, in their own square brackets: `log.append(["swim", 6])`. Your '
        'code added them as two loose items.')
    if _B.len(_got) == _k:
        assert not _bare, ('Use `log.append([...])` to add to `log` itself. `+` makes a new, longer list, and that '
                           'line throws it away.')
        assert not _early, 'Put `log.append(...)` below the line that makes `log`. Lines run top to bottom.'
        assert _B.len(_lits) < 2, ('Keep one `log = [...]` line, and add to it with `log.append([...])`. A second '
                                   '`log = [...]` makes a brand-new list.')
        assert False, ('Add one more drill to the end: `log.append(["swim", 6])`, a drill and its score in square '
                       'brackets. `log` did not grow.' + _ev({'log': _L}))
    assert _B.len(_got) == _k + 1, ('Append one drill, once. `log` grew by ' + _B.str(_B.len(_got) - _k) + '.'
                                     + _ev({'log': _L}, _apps))
    _new = _got[-1]
    assert type(_new).__name__ not in ('str', 'int'), ('Append one pair, in square brackets: `log.append(["swim", 6])`. '
                                                       'You appended ' + _sh(_new) + ' on its own.')
    assert type(_new).__name__ == 'list' and _B.len(_new) == 2, ('Append one pair: the drill, then its score, in '
                                                                 'square brackets: `log.append(["swim", 6])`.')
    assert type(_new[1]).__name__ != 'str', 'Take the quotes off the new score. Scores are numbers.'
    assert not (_is_num(_new[0]) and type(_new[1]).__name__ == 'str'), (
        'Put the drill first, then its score: `log.append(["swim", 6])`.')
    assert False, 'Append a pair like `["swim", 6]`: the drill in quotes, then its score.'
# The reruns swap in their own pair, so read the student's own appended pair from their own run.
_mine = globals().get('log')
if (type(_mine).__name__ == 'list' and _lits and _B.len(_mine) == _B.len(_lits[-1].value.elts) + 1
        and type(_mine[-1]).__name__ == 'list' and _B.len(_mine[-1]) == 2):
    _d, _s = _mine[-1][0], _mine[-1][1]
    assert not (_is_num(_d) and type(_s).__name__ == 'str'), (
        'Put the drill first, then its score: `log.append(["swim", 6])`. Your new pair is the other way round.')
    assert type(_s).__name__ != 'str', 'Take the quotes off the new score. Scores are numbers.'
    assert type(_d).__name__ == 'str', 'Name the new drill in quotes, first in its pair: `log.append(["swim", 6])`.'
''',
    RERUNS=LOG_RERUNS,
)

LOG_FIXED = chk(
    "the first score is 2 more, changed by position",
    r'''
_tree = _ast.parse(_source)
def _deep(_x):
    return (type(_x).__name__ == 'Subscript' and type(_x.value).__name__ == 'Subscript'
            and type(_x.value.value).__name__ == 'Name' and _x.value.value.id == 'log')
_bare = [_n for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp'
         and any(_deep(_x) for _x in _ast.walk(_n.value))]
_copies = [_n.targets[0].id for _n in _tree.body if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
           and type(_n.targets[0]).__name__ == 'Name' and _deep(_n.value)]
_own = globals().get('log')
for _L, _P in __RERUNS__:
    _ns, _rows, _err, _miss, _seen = _rerun({'log': _L}, {'log': _P})
    assert not _miss, _keep('log')
    _apps = {'log': _P} if 'log.append' in _seen else None
    _vals = {'log': _L}
    _got = _ns.get('log')
    _k = _B.len(_L)
    _want = _L[0][1] + 2
    _f = _got[0] if type(_got).__name__ == 'list' and _got else None
    if (type(_f).__name__ == 'list' and _B.len(_f) == 2 and _f[1] == _want and _f[0] == _L[0][0]
            and _got[1:_k] == _L[1:]):
        continue
    assert not _err, _stop(_vals, _apps, _err)
    assert type(_f).__name__ == 'list', ('Change the score inside the first pair, `log[0][1]`, and keep the pair. '
                                         '`log[0]` is the whole first pair.' + _ev(_vals, _apps))
    _second = _B.len(_got) > 1 and type(_got[1]).__name__ == 'list' and _B.len(_got[1]) == 2
    assert not (_f[1] == _L[0][1] and _second and _got[1][1] == _L[1][1] + 2), (
        'Positions start at 0: the first drill is `log[0]`, so its score is `log[0][1]`. You changed the second '
        'drill.' + _ev(_vals, _apps))
    assert _got[1:_k] == _L[1:], "Change only the first drill's score. Another pair changed too." + _ev(_vals, _apps)
    if _f[1] == _L[0][1]:
        assert not _bare, ('Put the new score back in the list: `log[0][1] = log[0][1] + 2`. That line works it out, '
                           'then keeps it nowhere.')
        assert not _copies, ('Change the score in the list itself: `log[0][1] = ...`. `' + _copies[0] + '` holds a '
                             'copy of the number, so `log` did not change.')
        assert False, ('Add 2 to the first score by position: `log[0][1] = log[0][1] + 2`. The first score stayed '
                       + _sh(_f[1]) + '.' + _ev(_vals, _apps))
    assert not (type(_own).__name__ == 'list' and _own and type(_own[0]).__name__ == 'list' and _B.len(_own[0]) == 2
                and _f[1] == _own[0][1]), (
        "Build it from the old score, so it works for any log. On Mar'tu's other log the first score was "
        + _sh(_L[0][1]) + ', so it should become ' + _sh(_want) + '. Yours became ' + _sh(_f[1]) + '.'
        + _ev(_vals, _apps))
    assert False, ('Make the first score 2 more than it was: `log[0][1] + 2`. It became ' + _sh(_f[1]) + ', not '
                   + _sh(_want) + '.' + _ev(_vals, _apps))
''',
    RERUNS=LOG_RERUNS,
)

LOG_RECIPE = chk(
    "last_score hands back the newest score of any log",
    r'''
_g = globals()
assert 'last_score' in _g and _B.callable(_g['last_score']), ('Keep the recipe `def last_score(training):` from the '
                                                              'starter, and finish its `return` line.')
_fn = _g['last_score']
_defs = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef' and _n.name == 'last_score']
_params = [_a.arg for _a in _defs[-1].args.args] if _defs else []
_param = _params[0] if _params else 'training'
_global = _defs and 'log' not in _params and any(type(_n).__name__ == 'Name' and _n.id == 'log'
                                                 for _n in _ast.walk(_defs[-1]))
assert not _global, ('Use the ingredient `' + _param + '` inside the recipe, not `log`. The recipe works on whatever '
                     'log it is handed.')
_body = _defs[-1].body if _defs else []
_starter = (_B.len(_body) == 1 and type(_body[0]).__name__ == 'Return' and type(_body[0].value).__name__ == 'Constant'
            and _body[0].value.value == 0)
_res = []
for _arg in ([["kick", 3], ["jump", 9]], [["swim", 12]], [["parry", 5], ["dodge", 8], ["wall", 1]]):
    _keep_out = _sys.stdout
    _buf = _io.StringIO()
    _sys.stdout = _buf
    _e = ''
    _r = 0
    try:
        _r = _fn([[_p[0], _p[1]] for _p in _arg])
    except Exception as _x:
        _e = type(_x).__name__ + ': ' + _B.str(_x)
    finally:
        _sys.stdout = _keep_out
    _call = '`last_score(' + _sh(_arg) + ')`'
    if _e:
        _tip = (' The newest pair is `' + _param + '[-1]`, in a log of any length.' if _e.startswith('IndexError')
                else '')
        assert False, 'Mend the recipe so it works for any log.' + _tip + ' ' + _call + ' stopped Python: ' + _e + '.'
    _res.append((_call, _r, _arg[-1][1], _buf.getvalue().strip(), _arg))
assert not (_starter and all(_r == 0 for _c, _r, _w, _p, _a in _res)), (
    "Replace the starter's `return 0` with the newest score: `return " + _param + "[-1][1]`.")
for _call, _r, _want, _printed, _arg in _res:
    if _is_int(_r) and _r == _want:
        continue
    if type(_r).__name__ == 'NoneType':
        assert not _printed, ('Use `return`, not `print`: ' + _call + ' printed ' + _printed + ' but handed back '
                              '`None`.')
        assert False, 'Put `return` in front of the newest score. ' + _call + ' handed back `None`: nothing.'
    assert type(_r).__name__ != 'list', ('Take the score out of the pair with `[-1][1]`. ' + _call + ' handed back '
                                         'the whole pair ' + _sh(_r) + '.')
    assert type(_r).__name__ != 'str', ('Hand back the score, the second item in the pair: `[-1][1]`. ' + _call
                                        + ' handed back the drill.')
    assert _B.len(set([_B.repr(_x[1]) for _x in _res])) > 1, (
        'Read the score from `' + _param + '`, so it follows the log it is handed. ' + _res[0][0] + ' and '
        + _res[1][0] + ' both handed back ' + _sh(_r) + '.')
    assert _r != _arg[0][1] or _B.len(_arg) == 1, ('Take the newest score, from the end: `[-1][1]`. ' + _call
                                                    + ' handed back the first score.')
    assert False, _call + ' should hand back ' + _B.str(_want) + ', the newest score. It handed back ' + _sh(_r) + '.'
''',
)

LOG_LAST_LINE = chk(
    "the last drill and its score print on one line",
    r'''
_own = globals().get('log')
_own_last = _own[-1] if type(_own).__name__ == 'list' and _own else None
def _has_score(_l, _s):
    return _s in _nums(_l) if _is_int(_s) else _B.str(_s) in _l
def _says(_pair):
    # A line that shows the drill and its score as text (not the pair printed with its brackets).
    if type(_pair).__name__ != 'list' or _B.len(_pair) < 2:
        return lambda _l: False
    _d, _s = _B.str(_pair[0]), _pair[1]
    return lambda _l: (_d in _l and _has_score(_l, _s) and _B.repr(_pair) not in _l and _B.str(_pair) not in _l
                       and not _l.startswith('['))
_own_rows = _lines()
_own_hits = _rows_with(_own_rows, _says(_own_last))
# The student's own run first (their own log), then Mar'tu's two other logs.
for _L, _P in [(None, None)] + __RERUNS__:
    if _L is None:
        _ns, _rows, _err, _apps, _vals = globals(), _own_rows, '', None, None
    else:
        _ns, _rows, _err, _miss, _seen = _rerun({'log': _L}, {'log': _P})
        assert not _miss, _keep('log')
        _apps = {'log': _P} if 'log.append' in _seen else None
        _vals = {'log': _L}
    _last = _ns['log'][-1] if type(_ns.get('log')).__name__ == 'list' and _ns['log'] else ['', -1]
    if type(_last).__name__ != 'list' or _B.len(_last) < 2:
        _last = ['', -1]
    _d, _s = _B.str(_last[0]), _last[1]
    _text = _rows_with(_rows, _says(_last))
    if _text and (_L is None or _same_row(_own_rows, _own_hits, _rows, _text)):
        continue
    assert not _err, _stop(_vals, _apps, _err)
    _hits = [_l for _l in _rows if _d and _d in _l and _has_score(_l, _s)]
    assert not (_hits and not _text), ('Glue the drill and its score into one line of text: the drill from '
                                       '`log[-1]`, then `str()` of `last_score(log)`. Your line shows the pair with '
                                       'its brackets.')
    assert not _text, ('Let one line read the last drill from the list and its score from `last_score(log)`. A line '
                       'typed for each log cannot follow a new one.' + _ev(_vals, _apps))
    _own_s = _own_last[1] if type(_own_last).__name__ == 'list' and _B.len(_own_last) > 1 else None
    assert not (_vals is not None and [_l for _l in _rows if _d in _l and _own_s in _nums(_l)]), (
        'Get the score from `last_score(log)` too, so it follows the log. Your line shows a score you typed.'
        + _ev(_vals, _apps))
    assert not [_l for _l in _rows if _d and _d in _l], ('Add the score to the same line, glued after the drill: '
                                                         '`str()` of `last_score(log)`.' + _ev(_vals, _apps))
    _typed = _vals is not None and type(_own_last).__name__ == 'list' and _own_last and \
        [_l for _l in _rows if _B.str(_own_last[0]) in _l]
    assert not _typed, ('Read the last drill from the list, `log[-1][0]`, so it follows the log. Your line shows a '
                        'drill you typed.' + _ev(_vals, _apps))
    _other = [_p for _p in (_ns['log'][:-1] if type(_ns.get('log')).__name__ == 'list' else [])
              if type(_p).__name__ == 'list' and _p and [_l for _l in _rows if _B.str(_p[0]) in _l]]
    assert not _other, ('Count from the end: `log[-1]` is the last pair in a log of any length. Your line shows '
                        'another drill.' + _ev(_vals, _apps))
    assert False, ('Print the last drill and its score on one line: the drill from `log[-1]`, the score from '
                   '`last_score(log)`.' + _ev(_vals, _apps))
''',
    RERUNS=LOG_RERUNS,
)

LOG_COUNTED = chk(
    "the number of drills follows the log",
    r'''
_own = globals().get('log')
_own_n = _B.len(_own) if type(_own).__name__ == 'list' else -1
_own_rows = _lines()
_own_hits = _rows_with(_own_rows, lambda _l: _own_n in _nums(_l))
# `len(log[0])`: the length of one pair (always 2), not of the log.
_inner = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call'
          and type(_n.func).__name__ == 'Name' and _n.func.id == 'len' and _n.args
          and type(_n.args[0]).__name__ == 'Subscript' and type(_n.args[0].value).__name__ == 'Name'
          and _n.args[0].value.id == 'log']
_fails = []
# The student's own run first (their own log), then Mar'tu's two other logs.
for _L, _P in [(None, None)] + __RERUNS__:
    if _L is None:
        _ns, _rows, _err, _apps, _vals = globals(), _own_rows, '', None, None
    else:
        _ns, _rows, _err, _miss, _seen = _rerun({'log': _L}, {'log': _P})
        assert not _miss, _keep('log')
        _apps = {'log': _P} if 'log.append' in _seen else None
        _vals = {'log': _L}
    _n = _B.len(_ns['log']) if type(_ns.get('log')).__name__ == 'list' else -1
    _all = [_x for _l in _rows for _x in _nums(_l)]
    _hits = _rows_with(_rows, lambda _l: _n in _nums(_l))
    if _hits and (_L is None or _same_row(_own_rows, _own_hits, _rows, _hits)):
        continue
    assert not _err, _stop(_vals, _apps, _err)
    _fails.append((_vals, _apps, _n, _all, _hits))
for _vals, _apps, _n, _all, _hits in _fails:
    assert not _inner, ('Count the pairs with `len(log)`. `len(log[0])` counts the two parts of one pair.'
                        + _ev(_vals, _apps))
# A rerun of another length tells a typed count from a count printed before the append.
for _vals, _apps, _n, _all, _hits in _fails:
    assert not (_vals is not None and _own_n in _all and _own_n != _n - 1), (
        'Count with `len(log)`, so the number follows the log. Your line shows ' + _B.str(_own_n) + ', a number '
        'typed by hand.' + _ev(_vals, _apps))
for _vals, _apps, _n, _all, _hits in _fails:
    assert not (_vals is not None and _hits and not _inner), ('Let one line count the log: `print(len(log))`. A number typed for each log '
                                        'cannot follow a new one.' + _ev(_vals, _apps))
for _vals, _apps, _n, _all, _hits in _fails:
    assert not (_n - 1 in _all and _apps and _own_n - 1 in [_x for _l in _own_rows for _x in _nums(_l)]), (
        'Print it at the bottom, after the append, so it counts every drill. Your line counted one too few.'
        + _ev(_vals, _apps))
for _vals, _apps, _n, _all, _hits in _fails[:1]:
    assert False, ('Print how many drills there are: `len(log)`. '
                   + ('In your own log' if _vals is None else "On Mar'tu's other log") + ' it is ' + _B.str(_n)
                   + '.' + _ev(_vals, _apps))
''',
    RERUNS=LOG_RERUNS,
)

# Task 5 asks for the score from `last_score(log)`. Mar'tu's check runs the program once more with the recipe's body
# swapped for `return <mark>`: the line that shows the last drill must then show the mark. A line that reads
# `log[-1][1]` (or calls the recipe and throws the answer away) still shows the real score.
LOG_USES_RECIPE = chk(
    "the score on that line comes from last_score(log)",
    r'''
_own = globals().get('log')
_own_last = _own[-1] if type(_own).__name__ == 'list' and _own else None
_d = _B.str(_own_last[0]) if type(_own_last).__name__ == 'list' and _own_last else ''
_tree = _ast.parse(_source)
_defs = [_n for _n in _tree.body if type(_n).__name__ == 'FunctionDef' and _n.name == 'last_score']
_seen_nums = [_x for _l in _lines() for _x in _nums(_l)]
_mark = [_m for _m in __MARKS__ if _m not in _seen_nums][0]
if _defs and _d:
    for _n in _defs:
        _n.body = [_ast.copy_location(_ast.Return(value=_ast.Constant(value=_mark)), _n.body[0])]
    _ast.fix_missing_locations(_tree)
    _ns = {'__name__': '__main__'}
    _keep_out = _sys.stdout
    _buf = _io.StringIO()
    _sys.stdout = _buf
    try:
        _B.exec(_B.compile(_tree, 'main.py', 'exec'), _ns)
    except Exception:
        pass
    finally:
        _sys.stdout = _keep_out
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    assert [_l for _l in _rows if _d in _l and _mark in _nums(_l)], (
        "Get the score from `last_score(log)`, as task 5 asks. Your line reads it another way. (Mar'tu's check "
        'tried a recipe that hands back ' + _B.str(_mark) + ', only inside the check, and your line did not show it.)')
''',
    MARKS=[70707, 80808, 90909],
)

BETTER_LINE = "Better than the first drill!"

LOG_BONUS = chk(
    "the line shows only when the last score beats the first",
    r'''
for _L, _P, _beat in __CASES__:
    _ns, _rows, _err, _miss, _seen = _rerun({'log': _L}, {'log': _P})
    assert not _miss, _keep('log')
    _apps = {'log': _P} if 'log.append' in _seen else None
    _vals = {'log': _L}
    assert not _err, _stop(_vals, _apps, _err, 'Make it work for another log too.')
    _said = [_l for _l in _rows if _l.lower().rstrip('.!').startswith('better than the first drill')]
    _first, _last = _ns['log'][0][1], _ns['log'][-1][1]
    if _beat:
        assert _said, ('Print `Better than the first drill!` when the last score is bigger: '
                       '`if log[-1][1] > log[0][1]:`.' + _ev(_vals, _apps))
    elif _first == _last:
        assert not _said, ('Use `>`: the last score must *beat* the first. A tie printed the line too.'
                           + _ev(_vals, _apps))
    else:
        assert not _said, 'Print it only when the last score is bigger. It printed anyway.' + _ev(_vals, _apps)
''',
    CASES=[(LOG_A, PAIR_A, True), ([["parry", 30], ["kick", 12]], ["swim", 20], False),
           ([["parry", 18]], ["swim", 20], False)],
)

# Task 1's pairs end with a comma, ready for the log's own rows; task 2's pair goes inside `.append( )` on its own.
LOG_PICK = (
    "# Mar'tu's picks, ready to copy.\n"
    "# For task 1, a comma after each pair:\n"
    "# [\"cane parry\", 7],\n"
    "# [\"shield wall\", 5],\n"
    "# [\"slow breaths\", 9],\n"
    "# For task 2:\n"
    "# [\"roll and rise\", 6]"
)

PROJECT_3P1 = dict(
    kind="project",
    id="oogrishs-training-log",
    title="Oogrish's Training Log",
    optional=True,
    minutes=25,
    summary="Keep Oogrish's yard log as a list of pairs: add a drill, fix a score, and hand back the newest one.",
    intro=(
        "Oogrish trains in the yard every morning. Cane, shield, breath. He gives each drill a score, and he "
        "wants a log.\n"
        "Each drill is a pair: `[drill, score]`. The log is a list of pairs: a list inside a list.\n"
        "Six tasks, in order. The comments in the editor mark each one. Any drills you like."
    ),
    martu=(
        "A list inside a list, yes? Outer number first: which drill. Inner number second: `0` for the drill, `1` "
        "for its score.\n"
        "My check tries other logs, with other drills. So read everything from the list, and never type a score "
        "you can see."
    ),
    names=["log", "last_score", "training", "len", "str"],
    pick=LOG_PICK,
    pair_talk=(
        "Pair talk: before task 3, tell your partner which two numbers reach the first drill's score, and why the "
        "first one is 0. Then each of you types it on your own screen."
    ),
    starter=LOG_STARTER,
    checkpoints=[
        dict(
            id="make-the-log",
            text="1. Make `log` a list of 3 or more pairs. Each pair is a drill in quotes, then its score.",
            dictated=False,
            hints=[
                "Look at task 1. One pair looks like `[\"kick\", 3]`. Put the pairs inside the outer square "
                "brackets, with a comma between them.",
                "A list of pairs with other names: `menu = [[\"soup\", 4], [\"bread\", 2]]`. Square brackets "
                "outside, square brackets around each pair.",
                "Write `log = [[\"cane parry\", 7], [\"shield wall\", 5], [\"slow breaths\", 9]]`, or your own drills.",
            ],
            checks=[LOG_MADE],
            pass_line="Oogrish: A log. Good. Memory is a poor weapons master.",
        ),
        dict(
            id="append-a-drill",
            text="2. Append one more drill and its score to `log`.",
            dictated=False,
            hints=[
                "Look at task 2. `.append()` adds one item to the end. Here one item is a whole pair, in its own "
                "square brackets.",
                "With other names: `menu.append([\"pie\", 5])` adds one pair to the end of `menu`.",
                "Write `log.append([\"roll and rise\", 6])` under task 2, or your own drill.",
            ],
            checks=[LOG_APPENDED],
            pass_line="Lucky: A new drill. Logged before Oogrish forgets it.",
        ),
        dict(
            id="fix-the-first-score",
            text="3. Oogrish misread the first score. Add 2 to it, by position.",
            dictated=False,
            hints=[
                "Outer number first: the first drill is `log[0]`. Inner number second: its score is `[1]`. Then "
                "build the new score from the old one.",
                "With other names: `menu[0][1] = menu[0][1] + 1` makes the first price 1 more.",
                "Write `log[0][1] = log[0][1] + 2` under task 3.",
            ],
            checks=[LOG_FIXED],
            pass_line="Oogrish: Two more. My eyes, not my cane.",
        ),
        dict(
            id="newest-score-recipe",
            text="4. Make `last_score(training)` hand back the newest score of any log it is handed.",
            dictated=False,
            hints=[
                "Look at the recipe under task 4. Use its ingredient, `training`. The newest pair is at the end, "
                "and the score is its second item.",
                "With other names: `def first_price(menu):` / `    return menu[0][1]` hands back the first price.",
                "Write `return training[-1][1]` in place of `return 0`.",
            ],
            checks=[LOG_RECIPE],
            pass_line="Gearshift: Visor dims. Recipe holds for any log.",
        ),
        dict(
            id="say-the-last-drill",
            text="5. Print the last drill and its score on one line. Get the score from `last_score(log)`.",
            dictated=True,
            hints=[
                "Look at task 5. `log[-1]` is the newest pair, and its `[0]` is the drill. The recipe hands back "
                "the score: `last_score(log)`. It is a number, so wrap it in `str()` before you glue it.",
                "With other names: `last = menu[-1]` / `price = str(last_price(menu))` / "
                "`print(last[0] + \": \" + price)`.",
                "Write `newest = log[-1]` and `score = str(last_score(log))`, then `print(newest[0] + \": \" + score)`.",
            ],
            checks=[LOG_LAST_LINE, LOG_USES_RECIPE],
            pass_line="Bomb Shell: Logged.",
        ),
        dict(
            id="count-the-drills",
            text="6. Print how many drills are in the log, with `len()`.",
            dictated=True,
            hints=[
                "Look at task 6. `len(log)` counts the pairs. Glue it with `str()`, or print it on its own.",
                "With other names: `print(len(menu))` shows how many dishes `menu` has.",
                "Write `print(\"Drills: \" + str(len(log)))` at the bottom.",
            ],
            checks=[LOG_COUNTED],
            pass_line="Mar'tu: Six tasks. One log. The turtle is pleased, which is rare.",
        ),
    ],
    solution=LOG_SOLUTION,
    partials=[
        _log(LOG_LITERAL),
        _log(LOG_LITERAL, LOG_APPEND),
        _log(LOG_LITERAL, LOG_APPEND, LOG_FIX),
        _log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN),
        _log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST),
    ],
    assemble=dict(
        lines=[line for line in LOG_SOLUTION.splitlines() if line.strip() and not line.lstrip().startswith("#")],
        distractors=[
            "log.append(\"roll and rise\", 6)",
            "log[1][1] = log[1][1] + 2",
            "    return training[len(training)][1]",
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Shelves of small shelves",
            text=(
                "```text\nlog[0] -> [\"cane parry\", 7]\nlog[1] -> [\"shield wall\", 5]\n"
                "log[2] -> [\"slow breaths\", 9]\n\nlog[0][0] -> \"cane parry\"\nlog[0][1] -> 7\n```\n"
                "Outer number: which pair. Inner number: which part of it."
            ),
        ),
        dict(
            angle="everyday",
            label="A score card",
            text=(
                "A score card has one row per drill: the drill's name, then its score. The log is the card. "
                "Each pair is a row. `log[0][1]` is row one, the score column."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Make the list of pairs.\n"
                "2. `.append()` one more pair.\n"
                "3. `log[0][1] = log[0][1] + 2`.\n"
                "4. The recipe hands back `training[-1][1]`.\n"
                "5. The drill from `log[-1]`, the score from `last_score(log)`. Glue them, with `str()`.\n"
                "6. `len(log)`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "`party.members` was a list too: one item per hero. The campaign handed each one to "
                "`add_spell(...)`. Your log is the same shape: a list, and inside it, one item per drill."
            ),
        ),
    ],
    bonus=dict(
        by="oogrish",
        title="Did I get better?",
        text=(
            "Oogrish wants to know if training works. At the bottom, if the last score is bigger than the first, "
            "print `Better than the first drill!`"
        ),
        hints=[
            "Bigger than is `>`. A tie is not better. Indent the `print` under the `if`.",
            "Write `if log[-1][1] > log[0][1]:` at the bottom, then `    print(\"Better than the first drill!\")` under it.",
        ],
        checks=[LOG_BONUS],
        solution=LOG_SOLUTION + "if log[-1][1] > log[0][1]:\n    print(\"" + BETTER_LINE + "\")\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet='for member in party.members:\n    add_spell(member["spell_book"], ...)',
        why=(
            "You ran this line in the campaign. `party.members` is a list, like your log: one item per hero, in "
            "order. Unit 6 teaches the loop. For now, you can read any one member by position."
        ),
    ),
    takeaway="A list of pairs: `log[0][1]` is the first pair's score, `log[-1]` the newest pair, `len(log)` how many.",
    wrong_answers=[
        dict(why="the starter (an empty log)", code=LOG_STARTER, fails_at=1, message_contains="still empty"),
        dict(why="a drill with no quotes, on one line (bare words inside [ ]: SyntaxError)",
             code=_log('log = [[storm kick, 7], ["shield wall", 5], ["slow breaths", 9]]\n'), fails_at=0,
             message_contains="Perhaps you forgot a comma"),
        dict(why="a drill with no quotes, one row of a list over several lines (SyntaxError)",
             code=_log(LOG_LITERAL.replace('["shield wall", 5]', "[shield wall, 5]")), fails_at=0,
             message_contains="Perhaps you forgot a comma"),
        # Mar'tu's pick, its rows copied with no comma at their ends: the next row reads as a position (TypeError).
        dict(why="rows over several lines with no comma between them (TypeError: not tuple)",
             code=_log(LOG_LITERAL.replace("7],", "7]").replace("5],", "5]")), fails_at=0, message_contains="not tuple"),
        dict(why="pairs in round brackets (square brackets vs parentheses)",
             code=_log("log = [(\"cane parry\", 7), (\"shield wall\", 5), (\"slow breaths\", 9)]\n"), fails_at=1,
             message_contains="square brackets too"),
        dict(why="the whole log in round brackets",
             code=_log("log = ([\"cane parry\", 7], [\"shield wall\", 5], [\"slow breaths\", 9])\n"), fails_at=1,
             message_contains="Round brackets"),
        dict(why="scores in quotes (A-05/A-08 quoting slip, reversed)",
             code=_log("log = [[\"cane parry\", \"7\"], [\"shield wall\", \"5\"], [\"slow breaths\", \"9\"]]\n"),
             fails_at=1, message_contains="quotes off"),
        dict(why="a flat list, not pairs", code=_log("log = [\"cane parry\", 7, \"shield wall\", 5]\n"), fails_at=1,
             message_contains="its own pair"),
        dict(why="only two drills", code=_log("log = [[\"cane parry\", 7], [\"shield wall\", 5]]\n"), fails_at=1,
             message_contains="at least 3"),
        dict(why="the first pairs appended to an empty log (task 1 is the list itself)",
             code=_log("log = []\nlog.append([\"cane parry\", 7])\nlog.append([\"shield wall\", 5])\n"
                       "log.append([\"slow breaths\", 9])\n"), fails_at=1, message_contains="square brackets of `log = []`"),
        dict(why="+ without keeping the new list", code=_log(LOG_LITERAL, "log + [[\"roll and rise\", 6]]\n"),
             fails_at=2, message_contains="throws it away"),
        dict(why="a second log = [...] (assigning a new list)",
             code=_log(LOG_LITERAL, "log = [[\"roll and rise\", 6]]\n"), fails_at=2, message_contains="brand-new"),
        dict(why="append with two things, not one pair", code=_log(LOG_LITERAL, "log.append(\"roll and rise\", 6)\n"),
             fails_at=0, message_contains="one argument"),
        dict(why="the drill appended on its own", code=_log(LOG_LITERAL, "log.append(\"roll and rise\")\n"),
             fails_at=2, message_contains="on its own"),
        dict(why="log = log.append(...): append hands back None",
             code=_log(LOG_LITERAL, "log = log.append([\"roll and rise\", 6])\n"), fails_at=2,
             message_contains="hands back `None`"),
        dict(why="+ with no inner brackets: the drill and score go in as two items",
             code=_log(LOG_LITERAL, "log = log + [\"roll and rise\", 6]\n"), fails_at=2, message_contains="two loose items"),
        dict(why="+= with no inner brackets", code=_log(LOG_LITERAL, "log += [\"roll and rise\", 6]\n"), fails_at=2,
             message_contains="two loose items"),
        dict(why="the drill and the score appended one at a time",
             code=_log(LOG_LITERAL, "log.append(\"roll and rise\")\nlog.append(6)\n"), fails_at=2,
             message_contains="two loose items"),
        dict(why="the new pair the other way round (the reruns swap the pair, so the own run is read)",
             code=_log(LOG_LITERAL, "log.append([6, \"roll and rise\"])\n"), fails_at=2, message_contains="other way round"),
        dict(why="the new score in quotes", code=_log(LOG_LITERAL, "log.append([\"roll and rise\", \"6\"])\n"), fails_at=2,
             message_contains="quotes off the new score"),
        dict(why="the append above the list (top to bottom)",
             code=_log("log = []\nlog.append([\"roll and rise\", 6])\n" + LOG_LITERAL), fails_at=2,
             message_contains="top to bottom"),
        dict(why="log = log + [pair] is fine (passes task 2), but the fix is missing",
             code=_log(LOG_LITERAL, "log = log + [[\"roll and rise\", 6]]\n"), fails_at=3, message_contains="stayed"),
        dict(why="the second drill's score changed (index from 1)",
             code=_log(LOG_LITERAL, LOG_APPEND, "log[1][1] = log[1][1] + 2\n"), fails_at=3,
             message_contains="Positions start at 0"),
        dict(why="the new score typed by hand", code=_log(LOG_LITERAL, LOG_APPEND, "log[0][1] = 9\n"), fails_at=3,
             message_contains="On Mar'tu's other log the first score was 11, so it should become 13. Yours became 9."),
        dict(why="the whole pair replaced by a number", code=_log(LOG_LITERAL, LOG_APPEND, "log[0] = log[0][1] + 2\n"),
             fails_at=3, message_contains="whole first pair"),
        dict(why="the inner position forgotten: a whole pair + 2 (TypeError)",
             code=_log(LOG_LITERAL, LOG_APPEND, "log[0] = log[0] + 2\n"), fails_at=0,
             message_contains="can only concatenate list"),
        dict(why="the new score worked out and kept nowhere", code=_log(LOG_LITERAL, LOG_APPEND, "log[0][1] + 2\n"),
             fails_at=3, message_contains="keeps it nowhere"),
        dict(why="a copy changed, not the list", code=_log(LOG_LITERAL, LOG_APPEND, "first = log[0][1]\nfirst = first + 2\n"),
             fails_at=3, message_contains="copy"),
        dict(why="the recipe hands back a typed score", code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    return 6\n"),
             fails_at=4, message_contains="follows the log"),
        dict(why="the recipe reads the outside list, not its ingredient",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    return log[-1][1]\n"), fails_at=4,
             message_contains="ingredient `training`"),
        dict(why="the recipe hands back the whole pair",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    return training[-1]\n"), fails_at=4,
             message_contains="whole pair"),
        dict(why="len used as a position (IndexError): the starter's should-show call stops the student's own Run",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    return training[len(training)][1]\n"), fails_at=0,
             message_contains="out of range"),
        dict(why="print instead of return (B-02 blank return)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    print(training[-1][1])\n"), fails_at=4,
             message_contains="not `print`"),
        dict(why="the first score handed back", code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, "    return training[0][1]\n"),
             fails_at=4, message_contains="from the end"),
        dict(why="the starter's return 0 left", code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX), fails_at=4,
             message_contains="starter's `return 0`"),
        dict(why="the last drill typed by hand",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(\"roll and rise: 6\")\n"), fails_at=5,
             message_contains="a drill you typed"),
        dict(why="the score glued without str()",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "newest = log[-1]\nprint(newest[0] + \": \" + newest[1])\n"),
             fails_at=0, message_contains="concatenate"),
        dict(why="len used as a position when printing (IndexError)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(log[len(log)][0])\n"), fails_at=0,
             message_contains="out of range"),
        dict(why="a position from the start (3) only fits a log of four",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(log[3][0] + \": \" + str(log[3][1]))\n"),
             fails_at=5, message_contains="another drill"),
        dict(why="the pair printed with its brackets",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(log[-1])\n"), fails_at=5,
             message_contains="brackets"),
        dict(why="the drill without its score",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(log[-1][0])\n"), fails_at=5,
             message_contains="same line"),
        dict(why="a label glued to the whole pair (the pair still prints with its brackets)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(\"Last: \" + str(log[-1]))\n"), fails_at=5,
             message_contains="brackets"),
        dict(why="task 5 done without the recipe: the score read from the list (log[-1][1])",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN,
                       "newest = log[-1]\nprint(newest[0] + \": \" + str(newest[1]))\n"), fails_at=5,
             message_contains="as task 5 asks"),
        dict(why="the recipe called, but its answer thrown away (the line still reads the list)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN,
                       "score = str(last_score(log))\nprint(log[-1][0] + \": \" + str(log[-1][1]))\n"), fails_at=5,
             message_contains="`last_score(log)`"),
        dict(why="the drill read from the list, the score typed",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, "print(log[-1][0] + \": \" + str(6))\n"),
             fails_at=5, message_contains="a score you typed"),
        dict(why="a line typed for each log the check showed (print the expected result directly)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN,
                       "print(\"roll and rise: 6\")\nprint(\"swim: 23\")\nprint(\"climb: 41\")\n"), fails_at=5,
             message_contains="typed for each log"),
        dict(why="the count typed by hand", code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST, "print(4)\n"),
             fails_at=6, message_contains="typed by hand"),
        dict(why="len of the first pair, not of the log", code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST,
             "print(len(log[0]))\n"), fails_at=6, message_contains="two parts of one pair"),
        dict(why="a count typed for each log the check showed, and not the student's own (the own run answers)",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST, "print(5)\nprint(3)\n"), fails_at=6,
             message_contains="In your own log it is 4"),
        dict(why="a count printed only for a log as long as the student's own",
             code=_log(LOG_LITERAL, LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST,
                       "if len(log) == 4:\n    print(\"Drills: 4\")\n"), fails_at=6,
             message_contains="On Mar'tu's other log it is 5"),
        dict(why="the count printed before the append",
             code=_log(LOG_LITERAL, "print(len(log))\n" + LOG_APPEND, LOG_FIX, LOG_RETURN, LOG_LAST), fails_at=6,
             message_contains="after the append"),
    ],
    notes=(
        meta(starter_level="S2", path="pool", skills="list-make,list-append-len,list-nested,list-index,param-use,"
             "return-value", solo="false", dictates="5,6", foreign_names="menu,last,first_price") + "\n"
        "Project 3P1 (pool, 25 min). Task comments are in the starter (S2), `log = []` and `return 0` are "
        "placeholders, so the program always runs. Tasks: 1 a list of [drill, score] pairs (any drills: the check "
        "reads the student's own literal, so lint e holds); 2 append (CMB: Mar'tu's check swaps the log AND the "
        "appended pair, `log.append(...)`, `log = log + [...]` or `log += [...]`); 3 `log[0][1] + 2` (CMB with "
        "other first scores, so a typed score fails); 4 `last_score(training)` (PAR with three fresh logs, RET, "
        "PAR-CONST, and the global `log` inside the recipe: the parameter is named `training`, so the 3A-06 "
        "`chalk_wall`-inside slip shows up here too; the spec's `last_score(log)` is the call; the starter's "
        "`# This should show 9` call under the def lets the student's own Run catch a slip, so "
        "`training[len(training)]` stops it: fails_at 0); 5 the last drill and its score on one line (reruns swap "
        "the appended pair, so a typed line fails; a comma print passes, a printed pair with brackets does not), "
        "with the score from `last_score(log)` (teacher ruling: a second check runs the program once more with "
        "the recipe swapped for `return 70707`, so `log[-1][1]` read straight from the list, or the recipe called "
        "and its answer thrown away, fails); 6 `len(log)` (reruns of 5 and 3 drills). Rerun scores are chosen "
        "so no two printed numbers collide (11/14/17/19 + 23, 31/37 + 41). Tasks 5-6 also read the student's own "
        "run, and the answer must come from the same print line in every run (a line typed per log fails). Task 2 "
        "reads the student's own appended pair too, since the reruns swap it out. Scores may be whole or decimal "
        "numbers. Messages name whose log a number is for: \"In your own log it is 4\" for the student's own run, "
        "\"On Mar'tu's other log it is 5\" for a rerun (teacher ruling). Side quest: did the last score beat the "
        "first (`if`, BND: a tie does not print). Partials 1-5 pass tasks 1..k. Pool item (optional); Quiz 3 "
        "points to it."
    ),
)


# =============================================================================================
# Lesson 3C "More List Tools" (optional, 15 min)
# =============================================================================================

# ---- 3C-01 insert-and-pop -------------------------------------------------------------------------------------

GAP_WALL = [48, 48, 46, 44, 41, 37]
GAP_LINE = "chalk_wall = [48, 48, 46, 44, 41, 37]\n"
INSERT_STARTER = (
    "# A mark is missing: 47.\n"
    + GAP_LINE
    + "# 1. Put 47 back at position 2.\n"
    + "\n"
    + "# 2. Pop the newest gap into newest.\n"
    + "\n"
    + "print(chalk_wall)\n"
)


def _insert(ins="chalk_wall.insert(2, 47)", pop="newest = chalk_wall.pop()", show="print(newest)", extra=""):
    code = INSERT_STARTER
    if ins is not None:
        code = code.replace("# 1. Put 47 back at position 2.\n", "# 1. Put 47 back at position 2.\n" + ins + "\n")
    if pop is not None:
        code = code.replace("# 2. Pop the newest gap into newest.\n", "# 2. Pop the newest gap into newest.\n" + pop + "\n")
    if show:
        code += show + "\n"
    return code + extra


INSERT_SOLUTION = _insert()

PUT_47_BACK = chk(
    "47 is back at position 2",
    r'''
_ins = _calls_of('insert')
_swap = [_n for _n in _ins if _B.len(_n.args) == 2 and type(_n.args[0]).__name__ == 'Constant'
         and _n.args[0].value == 47]
assert not _swap, 'Position first, then the value: `chalk_wall.insert(2, 47)`.'
_app = [_n for _n in _calls_of('append') if _n.args and type(_n.args[0]).__name__ == 'Constant'
        and _n.args[0].value == 47]
assert not _app, 'Use `.insert(2, 47)`: `.append()` always adds at the end, and 47 belongs at position 2.'
_copy = [_n.func.value.id for _n in _ins if type(_n.func.value).__name__ == 'Name' and _n.func.value.id != 'chalk_wall']
for _vals, _start in ((None, __GAP__), ({'chalk_wall': [50, 49, 45, 40]}, [50, 49, 45, 40])):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _got = _ns.get('chalk_wall')
    _E = _start[:2] + [47] + _start[2:]
    if any(_got == _E[_a:_B.len(_E) - _b] for _a in (0, 1) for _b in (0, 1, 2)) and 47 in _got:
        continue
    assert not _err, _stop(_vals, None, _err)
    assert type(_got).__name__ == 'list', (
        _handback('chalk_wall', {'insert': 'chalk_wall.insert(2, 47)', 'pop': 'newest = chalk_wall.pop()'})
        or 'Keep `chalk_wall` a list, and put 47 in with `chalk_wall.insert(2, 47)`.')
    _three = _start[:3] + [47] + _start[3:]
    assert not (_got == _three or _got == _three[:-1]), ('Positions start at 0: the third place is position 2. Use '
                                                        '`.insert(2, 47)`.' + _ev(_vals))
    assert not (type(_got).__name__ == 'list' and _B.len(_got) in (_B.len(_start), _B.len(_start) - 1)
                and _B.len(_got) > 2 and _got[2] == 47), (
        'Use `.insert(2, 47)`, which squeezes 47 in and moves the rest along. `chalk_wall[2] = 47` swapped out a gap.'
        + _ev(_vals))
    if _got == _start or _got == _start[:-1]:
        assert not _copy, ('Insert into `chalk_wall` itself. `' + _copy[0] + '` is a copy, so the wall did not '
                           'change.')
        assert _vals is not None, '`chalk_wall` has no 47 yet. Put it back at position 2: `chalk_wall.insert(2, 47)`.'
        assert False, ('Put 47 in with `chalk_wall.insert(2, 47)`, not by typing it into the list, so it works for '
                       'any wall. 47 never went in.' + _ev(_vals))
    assert False, 'Put 47 at position 2 with `chalk_wall.insert(2, 47)`. The wall became ' + _sh(_got) + '.' + _ev(_vals)
''',
    GAP=GAP_WALL,
)

POP_NEWEST = chk(
    "newest holds the popped gap, and the wall is one shorter",
    r'''
_pops = _calls_of('pop')
_own = globals().get('newest')
# `newest = 37`: the newest gap typed by hand, with no `.pop()`, so it is still on the wall.
_typed = [_x for _x in _ast.parse(_source).body if type(_x).__name__ == 'Assign' and _B.len(_x.targets) == 1
          and type(_x.targets[0]).__name__ == 'Name' and _x.targets[0].id == 'newest'
          and type(_x.value).__name__ == 'Constant']
for _vals, _start in ((None, __GAP__), ({'chalk_wall': [50, 49, 45, 40]}, [50, 49, 45, 40])):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _E = _start[:2] + [47] + _start[2:]
    _got = _ns.get('chalk_wall')
    if _ns.get('newest') == _E[-1] and _got == _E[:-1]:
        continue
    assert not _err.startswith('ValueError'), (
        'Use `newest = chalk_wall.pop()`: it takes off whatever gap is newest. `.remove()` needs a value that is on '
        'the wall. With another wall, Python stopped: ' + _err + '.' + _ev(_vals))
    assert not _err, _stop(_vals, None, _err, _ifix='Leave the brackets empty: `chalk_wall.pop()` takes the newest gap '
                                                    'off a wall of any length.')
    if 'newest' not in _ns:
        assert not _pops, 'Keep what `.pop()` hands back: `newest = chalk_wall.pop()`.'
        assert False, 'Make `newest` with `newest = chalk_wall.pop()`: it takes the newest gap off and hands it back.'
    _n = _ns['newest']
    assert not _B.callable(_n), 'Add `()` after `.pop`: `chalk_wall.pop()`. Without them, nothing is popped.'
    if _n == _E[-1] and _got == _E[:-1]:
        continue
    assert not (_typed and _n == _E[-1] and _got == _E), (
        _sh(_n) + ' is typed by hand, and it is still on the wall. `.pop()` takes it off and hands it back.'
        + _ev(_vals))
    assert not (_n == _E[-1] and _got == _E), ('Use `.pop()`: it reads the newest gap *and* takes it off the wall. '
                                               '`[-1]` only reads it.' + _ev(_vals))
    assert not (_n == _E[0] and _got == _E[1:]), ('Leave the brackets empty: `.pop()` takes the newest gap. '
                                                  '`.pop(0)` took the first one.' + _ev(_vals))
    assert _got != _E[:-2], 'Pop once. Two gaps came off the wall.' + _ev(_vals)
    assert not (_vals is not None and _n == _own), ('Keep what `.pop()` hands back: `newest = chalk_wall.pop()`. '
                                                   '`newest` stayed ' + _sh(_n) + ', a number typed by hand.' + _ev(_vals))
    assert _n != _E[-1], ('Pop the newest gap with `newest = chalk_wall.pop()`, and keep the rest of the wall as '
                          'step 1 left it. The wall became ' + _sh(_got) + '.' + _ev(_vals))
    assert False, ('Make `newest` the popped gap: `newest = chalk_wall.pop()`. `newest` holds ' + _sh(_n) + ', not '
                   + _sh(_E[-1]) + '.' + _ev(_vals))
''',
    GAP=GAP_WALL,
)

POP_BONUS = chk(
    "the answer follows the wall",
    r'''
for _vals, _want in (({'chalk_wall': [50, 49, 45, 40]}, 'True'), ({'chalk_wall': [50, 49, 45, 46]}, 'False')):
    _ns, _rows, _err, _miss, _seen = _rerun(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_vals, None, _err)
    _e = _ends(_rows)
    assert _want in _e and not (_want == 'False' and 'True' in _e), (
        'Print the question itself, `newest < chalk_wall[-1]`, so Python answers for any wall.' + _ev(_vals))
''',
)

INSERT_AND_POP = dict(
    id="insert-and-pop",
    title="Insert and pop",
    martu=(
        "Lucky leaned on my wall. A mark rubbed off: the 47.\n"
        "[[.insert()]] puts an item at a position: position first, then the value. Everything after it moves one "
        "place along. No retyping.\n"
        "[[.pop()]] does the opposite. It takes the last item off and hands it back, so you can keep it in a "
        "variable."
    ),
    introduces=["attr:insert", "attr:pop"],
    example=(
        "jars = [\"salt\", \"glug\", \"oil\"]\n"
        "jars.insert(1, \"honey\")\n"
        "print(jars)\n"
        "last = jars.pop()\n"
        "print(last)\n"
        "print(jars)\n"
    ),
    example_output="['salt', 'honey', 'glug', 'oil']\noil\n['salt', 'honey', 'glug']",
    names=["chalk_wall", "newest"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code="x = [5, 6, 7]\nprint(x.pop())\nprint(x)\n",
        choices=["7\n[5, 6, 7]", "5\n[6, 7]", "[5, 6]\n7", "7\n[5, 6]"],
        answer=3,
        explain="`.pop()` hands back the last item, 7, and takes it off. So the list left is `[5, 6]`.",
    ),
    starter=INSERT_STARTER,
    checkpoints=[
        dict(
            id="put-47-back",
            text="Put the 47 back where it belongs, with `.insert()`.",
            dictated=False,
            hints=[
                "Look under `# 1.` Position first, then the value. Positions start at 0, so the third place is 2.",
                "`jars.insert(1, \"honey\")` puts honey at position 1, and the glug moves along.",
                "Write `chalk_wall.insert(2, 47)` under `# 1.`",
            ],
            checks=[PUT_47_BACK],
            pass_line="Mar'tu: Forty-seven. Back where it belongs. Lucky, off my wall.",
        ),
        dict(
            id="pop-the-newest",
            text="Take the newest gap off the wall with `.pop()`, and keep it in `newest`.",
            dictated=True,
            hints=[
                "Look under `# 2.` `.pop()` hands back what it takes off, so put `newest = ` in front of it.",
                "`last = jars.pop()` takes the oil off and keeps it in `last`.",
                "Write `newest = chalk_wall.pop()` under `# 2.`",
            ],
            checks=[POP_NEWEST],
            pass_line="Gearshift: Thirty-seven, in hand. The wall is one shorter.",
        ),
    ],
    solution=INSERT_SOLUTION,
    partials=[_insert(pop=None, show="")],
    assemble=dict(
        lines=[line for line in INSERT_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["chalk_wall.insert(47, 2)", "newest = chalk_wall[-1]", "chalk_wall.append(47)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Squeezing in",
            text=(
                "```text\nbefore: 48 48 46 44 41 37\nplace:   0  1  2  3  4  5\n\n"
                ".insert(2, 47)\nafter:  48 48 47 46 44 41 37\n```\n"
                "46 and everything after it moved one place along."
            ),
        ),
        dict(
            angle="everyday",
            label="A queue",
            text=(
                "Someone cuts into a queue at place 2: everyone behind moves back one. That is `.insert()`. The "
                "last person walks off, and you note who it was: that is `.pop()`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `chalk_wall.insert(2, 47)`: 47 goes in at position 2.\n"
                "2. `newest = chalk_wall.pop()`: the last gap comes off, into `newest`.\n"
                "3. Print both and look."
            ),
        ),
        dict(angle="shorter", text="`.insert(position, value)` adds. `.pop()` takes the last off and hands it back."),
    ],
    bonus=dict(
        by="lucky",
        title="Still shrinking?",
        text=(
            "Lucky says the wall stopped shrinking. At the bottom, print whether `newest` is less than the new "
            "newest gap, `chalk_wall[-1]`."
        ),
        hints=["Less than is `<`. Python answers True or False.",
               "Write `print(newest < chalk_wall[-1])` at the bottom."],
        checks=[POP_BONUS],
        solution=INSERT_SOLUTION + "print(newest < chalk_wall[-1])\n",
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='option_1 = "We will help you."\noption_2 = "What is the decay?"',
        why=(
            "You wrote four options, in four boxes. A list holds all four in order. Then `.insert()` adds a new "
            "answer, and `.pop()` drops the last one, without retyping the rest."
        ),
    ),
    takeaway="`wall.insert(2, 47)` puts 47 at position 2. `newest = wall.pop()` takes the last item off and keeps it.",
    wrong_answers=[
        dict(why="the starter (no 47)", code=INSERT_STARTER, fails_at=1, message_contains="no 47 yet"),
        dict(why="value and position swapped", code=_insert(ins="chalk_wall.insert(47, 2)", pop=None, show=""),
             fails_at=1, message_contains="Position first"),
        dict(why="position counted from 1", code=_insert(ins="chalk_wall.insert(3, 47)", pop=None, show=""), fails_at=1,
             message_contains="Positions start at 0"),
        dict(why="append puts it at the end", code=_insert(ins="chalk_wall.append(47)", pop=None, show=""), fails_at=1,
             message_contains="at the end"),
        dict(why="a gap swapped out by position", code=_insert(ins="chalk_wall[2] = 47", pop=None, show=""),
             fails_at=1, message_contains="swapped out"),
        dict(why="the wall retyped with 47 in it",
             code=_insert(ins="chalk_wall = [48, 48, 47, 46, 44, 41, 37]", pop=None, show=""), fails_at=1,
             message_contains="not by typing"),
        dict(why="a copy changed (a slice), not the wall",
             code=_insert(ins="new_wall = chalk_wall[0:6]\nnew_wall.insert(2, 47)", pop=None, show=""), fails_at=1,
             message_contains="is a copy"),
        dict(why="the example's list name copied", code=_insert(ins="jars.insert(2, 47)", pop=None, show=""),
             fails_at=0, message_contains="not defined"),
        dict(why="x = x.insert(...): insert hands back None",
             code=_insert(ins="chalk_wall = chalk_wall.insert(2, 47)", pop=None, show=""), fails_at=1,
             message_contains="hands back `None`"),
        dict(why="x = x.pop(): the wall swapped for the popped gap (step 1 turns red, and says why)",
             code=_insert(pop="chalk_wall = chalk_wall.pop()", show=""), fails_at=1, message_contains="swapped the whole list"),
        dict(why="pop at the last position typed (6): a shorter wall has no 6", code=_insert(pop="newest = chalk_wall.pop(6)"),
             fails_at=2, message_contains="Leave the brackets empty"),
        dict(why="the newest gap removed by its typed value", code=_insert(pop="chalk_wall.remove(37)\nnewest = 37"),
             fails_at=2, message_contains="whatever gap is newest"),
        dict(why="[-1] reads but does not pop", code=_insert(pop="newest = chalk_wall[-1]"), fails_at=2,
             message_contains="only reads"),
        dict(why="pop(0) takes the first", code=_insert(pop="newest = chalk_wall.pop(0)"), fails_at=2,
             message_contains="took the first"),
        dict(why="popped but not kept", code=_insert(pop="chalk_wall.pop()", show=""), fails_at=2,
             message_contains="Keep what"),
        dict(why="no () after pop", code=_insert(pop="newest = chalk_wall.pop", show=""), fails_at=2,
             message_contains="Add `()`"),
        dict(why="popped twice", code=_insert(pop="chalk_wall.pop()\nnewest = chalk_wall.pop()"), fails_at=2,
             message_contains="Pop once"),
        dict(why="the newest gap typed by hand, after a pop", code=_insert(pop="chalk_wall.pop()\nnewest = 37"),
             fails_at=2, message_contains="typed by hand"),
        dict(why="newest = 37: the newest gap typed by hand, and never popped",
             code=_insert(pop="newest = 37"), fails_at=2,
             message_contains="37 is typed by hand, and it is still on the wall. `.pop()` takes it off and hands it "
                              "back."),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="list-insert-pop,list-index", solo="false", dictates="2",
             foreign_names="jars,last,x") + "\n"
        "3C-01 (O). Intro attr:insert, attr:pop. The starter wall is the real wall with 47 missing. CP1 [ND] "
        "goal-first (teacher ruling; the starter's `# 1.` comment names position 2, the last hint holds the "
        "line). CP1 CMB: a "
        "rerun with [50, 49, 45, 40] must become [50, 49, 47, 45, 40], so a retyped wall fails. The CP1 check "
        "accepts the wall with or without its last gap, so it stays true after CP2's pop. CP2 CMB on the same "
        "rerun: `newest` is 40 and the wall lost it. Catches: swapped arguments, position 3 (counting from 1), "
        "`.append(47)`, `chalk_wall[2] = 47`, a copy changed, `[-1]` (reads, no pop), `.pop(0)`, `.pop` with no "
        "`()`, popping twice, and `newest = 37` typed with no pop (its own message: still on the wall). Bonus: pop + "
        "index + comparison."
    ),
)

# ---- 3C-02 remove-and-in ------------------------------------------------------------------------------------

JOKE_WALL = [48, 48, 47, 99, 46, 44, 41, 37]
JOKE_LINE = "chalk_wall = [48, 48, 47, 99, 46, 44, 41, 37]\n"
REMOVE_STARTER = (
    "# Lucky wrote a 99 on the wall.\n"
    + JOKE_LINE
    + "has_32 = False\n"
    + "print(has_32)\n"
    + "# Take the 99 off here.\n"
    + "\n"
    + "print(chalk_wall)\n"
)


def _remove(has="has_32 = 32 in chalk_wall", take="if 99 in chalk_wall:\n    chalk_wall.remove(99)", extra=""):
    code = REMOVE_STARTER.replace("has_32 = False\n", has + "\n")
    if take:
        code = code.replace("# Take the 99 off here.\n", "# Take the 99 off here.\n" + take + "\n")
    return code + extra


REMOVE_SOLUTION = _remove()

HAS_32 = chk(
    "has_32 asks the list",
    r'''
_cmp = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare']
# Only a quoted 32 is this step's slip (a quoted value in a later line is that line's).
_quoted = [_n for _n in _cmp if any(type(_o).__name__ == 'In' for _o in _n.ops)
           and type(_n.left).__name__ == 'Constant' and _n.left.value == '32']
# `chalk_wall[1] == 32`: one position asked about, not the whole wall.
_one = [_n for _n in _cmp if any(type(_o).__name__ == 'Eq' for _o in _n.ops)
        and any(type(_x).__name__ == 'Subscript' for _x in [_n.left] + _n.comparators)
        and any(type(_x).__name__ == 'Constant' and _x.value == 32 for _x in [_n.left] + _n.comparators)]
# Each wall holds a 99, so step 2's plain remove can't stop a rerun before step 3. 32 sits at different positions,
# and 132 holds the text "32" without being 32 (a search of `str(chalk_wall)` fails).
for _vals, _want in ((None, False), ({'chalk_wall': [40, 32, 99, 36]}, True), ({'chalk_wall': [40, 99, 36, 32]}, True),
                     ({'chalk_wall': [40, 99, 36, 132]}, False)):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _got = _ns.get('has_32')
    if type(_got).__name__ == 'bool' and _got == _want:
        continue
    assert not _quoted, 'Take the quotes off: `"32"` is text, and the wall holds numbers. Ask `32 in chalk_wall`.'
    assert not _err, _stop(_vals, None, _err)
    assert 'has_32' in _ns, 'Keep the line `has_32 = ` from the starter, and put `32 in chalk_wall` after the `=`.'
    assert type(_got).__name__ == 'bool', ('Make `has_32` a yes/no answer: `32 in chalk_wall` gives True or False. It '
                                           'holds ' + _sh(_got) + '.' + _ev(_vals))
    if _got == _want:
        continue
    assert not (_got is False and _starter_line('has_32', False)), (
        "`has_32` still holds the starter's `False`. Ask the list: `has_32 = 32 in chalk_wall`." + _ev(_vals))
    assert not _one, ('Ask the whole wall with `in`: `has_32 = 32 in chalk_wall`. Your line asks about one position, '
                      'and 32 could be anywhere.' + _ev(_vals))
    assert False, ('Ask the list, so the answer follows the wall: `has_32 = 32 in chalk_wall`. `has_32` became '
                   + _sh(_got) + '.' + _ev(_vals))
''',
)

REMOVE_99 = chk(
    "the 99 is gone, and only the 99",
    r'''
for _vals, _start in ((None, __JOKE__), ({'chalk_wall': [50, 99, 49, 45]}, [50, 99, 49, 45])):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _got = _ns.get('chalk_wall')
    _want = [_x for _x in _start]
    _want.remove(99)
    if _got == _want:
        continue
    assert not _err, _stop(_vals, None, _err)
    assert type(_got).__name__ == 'list', (_handback('chalk_wall', {'remove': 'chalk_wall.remove(99)'})
                                           or 'Keep `chalk_wall` a list, and take the 99 off with `chalk_wall.remove(99)`.')
    if _got == _start:
        assert _vals is not None, 'The 99 is still on the wall. Take it off with `chalk_wall.remove(99)`.'
        assert False, ('Take it off with `chalk_wall.remove(99)`, so it works for any wall. The 99 is still there.'
                       + _ev(_vals))
    assert not (type(_got).__name__ == 'list' and 99 in _got and _B.len(_got) == _B.len(_start) - 1), (
        'Remove it by value: `.remove(99)` finds the 99 wherever it is. Your line took off another gap.' + _ev(_vals))
    assert False, 'Take off only the 99, with `chalk_wall.remove(99)`. The wall became ' + _sh(_got) + '.' + _ev(_vals)
''',
    JOKE=JOKE_WALL,
)

REMOVE_SAFE = chk(
    "a wall with no 99 is left alone",
    r'''
_vals = {'chalk_wall': [50, 49, 45]}
_ns, _rows, _err, _miss, _seen = _rerun(_vals)
assert not _miss, _keep('chalk_wall')
assert not _err.startswith('ValueError'), ('Ask first: put `if 99 in chalk_wall:` above `chalk_wall.remove(99)`, and '
                                           'indent the remove under it. A wall with no 99 stopped Python: ' + _err
                                           + '.' + _ev(_vals))
assert not _err, _stop(_vals, None, _err)
assert _ns.get('chalk_wall') == [50, 49, 45], ('Leave a wall with no 99 as it was. It became '
                                               + _sh(_ns.get('chalk_wall')) + '.' + _ev(_vals))
# Leaving every wall alone is not this step either: the 99 comes off your wall, under an `if` that asks with `in`.
_asks = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'If'
         and any(type(_o).__name__ in ('In', 'NotIn') for _c in _ast.walk(_n.test) if type(_c).__name__ == 'Compare'
                 for _o in _c.ops)]
assert type(chalk_wall).__name__ == 'list' and 99 not in chalk_wall and _uses('attr:remove') and _asks, (
    'Take the 99 off with `chalk_wall.remove(99)`, and ask first: `if 99 in chalk_wall:` above it, with the remove '
    'indented under it.')
''',
)

REMOVE_BONUS = chk(
    "the answer follows the wall",
    r'''
for _vals, _want in (({'chalk_wall': [40, 99, 33]}, 'True'), ({'chalk_wall': [40, 99, 31]}, 'False')):
    _ns, _rows, _err, _miss, _seen = _rerun(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_vals, None, _err)
    _e = _ends(_rows)
    assert ('True' in _e) == (_want == 'True'), (
        'Print the whole question: `32 in chalk_wall or 33 in chalk_wall`. Each side of `or` needs its own `in`.'
        + _ev(_vals))
''',
)

REMOVE_AND_IN = dict(
    id="remove-and-in",
    title="Remove and in",
    martu=(
        "Lucky wrote a 99 on my wall. He thinks he is funny. He is not.\n"
        "[[in]] asks a question: is this value somewhere in the list? Python answers `True` or `False`.\n"
        "[[.remove()]] takes out the first item that is the same as the value you give it. The value, not the "
        "position. If the value is not there, Python stops with a [[ValueError]]. So ask first, yes?"
    ),
    introduces=["attr:remove", "op:In"],
    example=(
        "pack = [\"rope\", \"glug\", \"map\"]\n"
        "print(\"glug\" in pack)\n"
        "pack.remove(\"glug\")\n"
        "print(pack)\n"
    ),
    example_output="True\n['rope', 'map']",
    names=["chalk_wall", "has_32"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code="wall = [48, 47, 46]\nprint(46 in wall)\nprint(\"46\" in wall)\n",
        choices=["True\nFalse", "True\nTrue", "False\nFalse", "46\nFalse"],
        answer=0,
        explain="46 is on the wall: True. `\"46\"` in quotes is text, and the wall holds numbers: False.",
    ),
    pair_talk=(
        "Pair talk: what should happen if the wall has no 99 at all? Say it to your partner before step 3. Then "
        "each of you writes it."
    ),
    starter=REMOVE_STARTER,
    checkpoints=[
        dict(
            id="ask-the-wall",
            text="Make `has_32` ask whether 32 is on the wall, with `in`.",
            dictated=False,
            hints=[
                "Line 3 still holds the starter's `False`. Ask the list instead, with `in`. No quotes on 32.",
                "`\"map\" in pack` is True when the map is in the pack.",
                "Write `has_32 = 32 in chalk_wall` on line 3.",
            ],
            checks=[HAS_32],
            pass_line="Bomb Shell: No 32. Yet.",
        ),
        dict(
            id="take-the-99-off",
            text="Take Lucky's 99 off the wall, with `.remove()`.",
            dictated=False,
            hints=[
                "Look under the comment. `.remove()` takes the value itself, not its position.",
                "`pack.remove(\"glug\")` takes the glug out, wherever it is.",
                "Write `chalk_wall.remove(99)` under the comment.",
            ],
            checks=[REMOVE_99],
            pass_line="Mar'tu: Better. Lucky, the wall is not a joke book.",
        ),
        dict(
            id="ask-before-removing",
            text="Remove the 99 only if it is on the wall, so a wall with no 99 doesn't stop Python.",
            dictated=False,
            hints=[
                "Put an `if` above the remove line. Ask with `in`, then indent the remove under it.",
                "With other names: `if \"map\" in pack:` / `    pack.remove(\"map\")`.",
                "Write `if 99 in chalk_wall:`, then `    chalk_wall.remove(99)` indented under it.",
            ],
            checks=[REMOVE_SAFE],
            pass_line="Oogrish: Look before you swing. Steady, now.",
        ),
    ],
    solution=REMOVE_SOLUTION,
    partials=[
        _remove(take=None),
        _remove(take="chalk_wall.remove(99)"),
    ],
    assemble=dict(
        lines=[line for line in REMOVE_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["chalk_wall.remove(3)", "has_32 = \"32\" in chalk_wall", "if 99 in chalk_wall"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Find it, then take it",
            text=(
                "```text\n48 48 47 99 46 44 41 37\n          ^^\n99 in chalk_wall -> True\n"
                ".remove(99):\n48 48 47 46 44 41 37\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Check your pocket first",
            text=(
                "Before you hand someone your key, check your pocket: is the key in there? `in` is the check. "
                "`.remove()` is handing it over. Reach for a key that isn't there, and you grab air: the ValueError."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `has_32 = 32 in chalk_wall` keeps the yes/no answer.\n"
                "2. `chalk_wall.remove(99)` takes out the value 99.\n"
                "3. `if 99 in chalk_wall:` on the line above, and the remove indented under it."
            ),
        ),
        dict(angle="shorter", text="`x in wall` asks. `wall.remove(x)` takes `x` out. Ask before you take."),
    ],
    bonus=dict(
        by="gearshift",
        title="Two numbers at once",
        text=(
            "Gearshift wants to know whether the next gap is already up. On a new line, print whether 32 *or* 33 is "
            "on the wall."
        ),
        hints=["Each side of `or` is its own question, with its own `in`.",
               "Write `print(32 in chalk_wall or 33 in chalk_wall)` at the bottom."],
        checks=[REMOVE_BONUS],
        solution=REMOVE_SOLUTION + "print(32 in chalk_wall or 33 in chalk_wall)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='if spell_name not in caster["spell_book"]:',
        why=(
            "You have seen this line in `cast_spell`. `not in` is the opposite of `in`. The spell checked the spell "
            "book before casting, the same way you check the wall before `.remove(99)`."
        ),
    ),
    takeaway="`99 in wall` asks; `wall.remove(99)` takes out the value. Ask first: `if 99 in wall:`.",
    wrong_answers=[
        dict(why="the starter (has_32 stays False)", code=REMOVE_STARTER, fails_at=1, message_contains="starter's `False`"),
        dict(why="the answer typed in (True)", code=_remove(has="has_32 = True", take=None), fails_at=1,
             message_contains="follows the wall"),
        dict(why="only the newest gap asked about", code=_remove(has="has_32 = chalk_wall[-1] == 32", take=None),
             fails_at=1, message_contains="one position"),
        dict(why="32 in quotes", code=_remove(has="has_32 = \"32\" in chalk_wall", take=None), fails_at=1,
             message_contains="quotes"),
        dict(why="one position asked about (counting from 1)", code=_remove(has="has_32 = chalk_wall[1] == 32", take=None),
             fails_at=1, message_contains="one position"),
        dict(why="a text search of the printed list (132 holds the text 32)",
             code=_remove(has="has_32 = \"32\" in str(chalk_wall)", take=None), fails_at=1, message_contains="quotes"),
        dict(why="count for a yes/no", code=_remove(has="has_32 = chalk_wall.count(32)", take=None), fails_at=1,
             message_contains="yes/no"),
        dict(why="the sides swapped", code=_remove(has="has_32 = chalk_wall in 32", take=None), fails_at=0,
             message_contains="not iterable"),
        dict(why="remove by position (3), not value", code=_remove(take="chalk_wall.remove(3)"), fails_at=0,
             message_contains="not in list"),
        dict(why="99 in quotes", code=_remove(take="chalk_wall.remove(\"99\")"), fails_at=0,
             message_contains="not in list"),
        dict(why="square brackets after remove", code=_remove(take="chalk_wall.remove[99]"), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="x = x.remove(...): remove hands back None", code=_remove(take="chalk_wall = chalk_wall.remove(99)"),
             fails_at=2, message_contains="hands back `None`"),
        dict(why="the example's list name copied", code=_remove(take="pack.remove(99)"), fails_at=0,
             message_contains="not defined"),
        dict(why="pop at a typed position only fits this wall", code=_remove(take="chalk_wall.pop(3)"), fails_at=2,
             message_contains="by value"),
        dict(why="the wall retyped without the 99", code=_remove(take="chalk_wall = [48, 48, 47, 46, 44, 41, 37]"),
             fails_at=2, message_contains="works for any wall"),
        dict(why="no question first (a clean wall crashes)", code=_remove(take="chalk_wall.remove(99)"), fails_at=3,
             message_contains="Ask first"),
        dict(why="the 99 taken off by position under an if: step 3 needs the remove itself",
             code=_remove(take="if 99 in chalk_wall:\n    chalk_wall.pop(chalk_wall.index(99))"), fails_at=3,
             message_contains="chalk_wall.remove(99)"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="list-remove-in,if-else", solo="false", dictates="",
             foreign_names="pack") + "\n"
        "3C-02 (O). Intro attr:remove, op:In. CP1 [ND] `has_32 = 32 in chalk_wall` (goal-first, teacher "
        "ruling; CMB: walls with 32 at position "
        "1 and at the end, so `chalk_wall[1] == 32` and `chalk_wall[-1] == 32` each fail one, and a wall with 132, "
        "so a text search of `str(chalk_wall)` fails; each holds a 99 so CP2's plain remove can't crash the rerun "
        "before CP3). CP2 [ND] `.remove(99)` (goal-first) "
        "(CMB with the 99 at position 1, so `.pop(3)` fails). CP3 [ND] the safe remove: a rerun with no 99 must "
        "not crash (ValueError) and must leave the wall alone. `remove(3)` and `remove(\"99\")` crash with "
        "ValueError on the student's own run. Bonus: `in` + `or`."
    ),
)

# ---- 3C-03 biggest-and-smallest ---------------------------------------------------------------------------

MAXMIN_STARTER = WALL_LINE + "longest = 0\nshortest = 0\ntotal_hours = 0\n"


def _maxmin(longest="longest = max(chalk_wall)", shortest="shortest = min(chalk_wall)",
            total="total_hours = sum(chalk_wall)", shrink="print(longest - shortest)", extra=""):
    return WALL_LINE + f"{longest}\n{shortest}\n{total}\n" + (f"{shrink}\n" if shrink else "") + extra


MAXMIN_SOLUTION = _maxmin()

LONGEST_SHORTEST = chk(
    "longest and shortest come from the list",
    r'''
_own = globals()
for _vals in (None, {'chalk_wall': [41, 39, 46, 44]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _hi, _lo = _B.max(_start), _B.min(_start)
    if _ns.get('longest') == _hi and _ns.get('shortest') == _lo and _is_int(_hi):
        continue
    assert not _err, _stop(_vals, None, _err, _ifix='Use `max(chalk_wall)` and `min(chalk_wall)`: they look at every '
                                                    'gap, on a wall of any length.')
    for _name, _tool, _want in (('longest', 'max', _hi), ('shortest', 'min', _lo)):
        assert _name in _ns, ('Keep the line `' + _name + ' = ` from the starter, with `' + _tool + '(chalk_wall)` '
                              'after the `=`.')
        _got = _ns[_name]
        if _is_int(_got) and _got == _want:
            continue
        assert not (_got == 0 and _starter_line(_name, 0)), (
            '`' + _name + "` still holds the starter's `0`. Replace the 0 with `" + _tool + '(chalk_wall)`.' + _ev(_vals))
        assert not (_ns.get('longest') == _lo and _ns.get('shortest') == _hi), (
            'Swap them: `max()` finds the biggest gap, and `min()` the smallest.' + _ev(_vals))
        assert not (_vals is not None and _name == 'longest' and _got == _start[0]), (
            '`max(chalk_wall)` finds the longest gap anywhere. The longest is not always the first, `[0]`.' + _ev(_vals))
        assert not (_vals is not None and _name == 'shortest' and _got == _start[-1]), (
            '`min(chalk_wall)` finds the shortest gap anywhere. The shortest is not always the newest, `[-1]`.'
            + _ev(_vals))
        assert not (_vals is not None and _got in _start), (
            'Use `' + _tool + '(chalk_wall)`: it looks at every gap. Your line picked a gap by its position, and the '
            + _name + ' gap is not always there.' + _ev(_vals))
        assert not (_vals is not None and _got == _own.get(_name)), (
            'Read it from the list: `' + _tool + '(chalk_wall)`. `' + _name + '` stayed ' + _sh(_got)
            + ', a number typed by hand.' + _ev(_vals))
        assert False, ('Make `' + _name + '` with `' + _tool + '(chalk_wall)`. It holds ' + _sh(_got) + ', not '
                       + _sh(_want) + '.' + _ev(_vals))
''',
)

TOTAL_HOURS = chk(
    "total_hours adds up the list",
    r'''
_own = globals().get('total_hours')
for _vals in (None, {'chalk_wall': [41, 39, 46, 44]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _got = _ns.get('total_hours')
    _want = _B.sum(_start)
    if _is_int(_got) and _got == _want:
        continue
    assert not _err, _stop(_vals, None, _err, _ifix='Add them all with `sum(chalk_wall)`: it works for a wall of any '
                                                    'length. Adding positions one by one does not.')
    assert 'total_hours' in _ns, 'Keep the line `total_hours = ` from the starter, and add the gaps up after the `=`.'
    assert not (_got == 0 and _starter_line('total_hours', 0)), (
        "`total_hours` still holds the starter's `0`. Add up the gaps: `sum(chalk_wall)`." + _ev(_vals))
    assert _got != _B.len(_start), '`len()` counts the gaps. `sum(chalk_wall)` adds them up.' + _ev(_vals)
    assert not (_vals is not None and _got == _own), (
        'Add them from the list with `sum(chalk_wall)`, not by typing each gap. `total_hours` stayed ' + _sh(_got)
        + '.' + _ev(_vals))
    assert False, ('Add up every gap: `sum(chalk_wall)`. `total_hours` holds ' + _sh(_got) + ', not ' + _sh(_want)
                   + '.' + _ev(_vals))
''',
)

SHRINK_LINE = chk(
    "the shrink follows the wall",
    r'''
_own = globals()
_own_shrink = None
if _is_int(_own.get('longest')) and _is_int(_own.get('shortest')):
    _own_shrink = _own['longest'] - _own['shortest']
_own_rows = _lines()
_w0 = _own.get('chalk_wall')
_own_want = _B.max(_w0) - _B.min(_w0) if type(_w0).__name__ == 'list' and _w0 else 11
_own_hits = _rows_with(_own_rows, lambda _l: _own_want in _nums(_l))
for _vals in (None, {'chalk_wall': [41, 39, 46, 44]}, {'chalk_wall': [60, 30, 45]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _want = _B.max(_start) - _B.min(_start)
    _all = [_x for _l in _rows for _x in _nums(_l)]
    _hits = _rows_with(_rows, lambda _l: _want in _nums(_l))
    if _hits and (_vals is None or _same_row(_own_rows, _own_hits, _rows, _hits)):
        continue
    assert not _err, _stop(_vals, None, _err, _ifix='Print `longest - shortest`: the variables work for a wall of any '
                                                    'length.')
    assert -_want not in _all, 'Longest first: `longest - shortest`, so the shrink is not below zero.' + _ev(_vals)
    assert not (_vals is not None and _own_shrink in _all and not _hits), (
        'Print it from the variables: `longest - shortest`. Your line still shows ' + _B.str(_own_shrink)
        + ', from numbers you typed.' + _ev(_vals))
    assert not _hits, ('Let one line work it out: `print(longest - shortest)`. A number typed for each wall cannot '
                       'follow a new one.' + _ev(_vals))
    assert False, ('Print the longest gap minus the shortest: `print(longest - shortest)`. '
                   + ('On your wall' if _vals is None else "On Mar'tu's other wall") + ' it is ' + _B.str(_want)
                   + '.' + _ev(_vals))
''',
)

AVERAGE_BONUS = chk(
    "the whole-hours average follows the wall",
    r'''
for _vals in ({'chalk_wall': [41, 39, 46, 44]}, {'chalk_wall': [60, 30, 45]}):
    _ns, _rows, _err, _miss, _seen = _rerun(_vals)
    assert not _miss, _keep('chalk_wall')
    assert not _err, _stop(_vals, None, _err)
    _w = _vals['chalk_wall']
    _want = _B.sum(_w) // _B.len(_w)
    assert _want in [_x for _l in _rows for _x in _nums(_l)], (
        'Print `total_hours // len(chalk_wall)`: the total, shared out over the gaps, in whole hours.' + _ev(_vals))
''',
)

BIGGEST_AND_SMALLEST = dict(
    id="biggest-and-smallest",
    title="Biggest and smallest",
    martu=(
        "Three questions Gearshift asks every night. Which gap was longest? Which was shortest? How many hours in "
        "all?\n"
        "[[max() and min()|max()]] hands back the biggest item, and `min()` the smallest, wherever they sit. "
        "[[sum()]] adds every number in the list.\n"
        "Round brackets, with the list inside. Like `len()`, which you know."
    ),
    introduces=["call:max", "call:min", "call:sum"],
    example="coins = [5, 12, 3]\nprint(max(coins))\nprint(min(coins))\nprint(sum(coins))\n",
    example_output="12\n3\n20",
    names=["chalk_wall", "longest", "shortest", "total_hours"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code="print(max([3, 9, 2]))\nprint(sum([3, 9, 2]))\n",
        choices=["2\n14", "9\n3", "9\n14", "[9]\n[14]"],
        answer=2,
        explain="The biggest of 3, 9 and 2 is 9. Added up: 3 + 9 + 2 is 14. `sum()` adds; `len()` would count 3.",
    ),
    starter=MAXMIN_STARTER,
    checkpoints=[
        dict(
            id="longest-and-shortest",
            text="Make `longest` the biggest gap and `shortest` the smallest, with `max()` and `min()`.",
            dictated=False,
            hints=[
                "Lines 2 and 3 still hold the starter's 0s. Hand the whole list to each tool, inside round brackets.",
                "`max(coins)` is the biggest coin, and `min(coins)` the smallest.",
                "Write `longest = max(chalk_wall)` on line 2 and `shortest = min(chalk_wall)` on line 3.",
            ],
            checks=[LONGEST_SHORTEST],
            pass_line="Gearshift: Forty-eight and thirty-seven. Logged.",
        ),
        dict(
            id="all-the-hours",
            text="Make `total_hours` hold every gap added up.",
            dictated=False,
            hints=[
                "One tool adds up a whole list. It is not `len()`: that one counts.",
                "`sum(coins)` adds 5, 12 and 3: 20.",
                "Write `total_hours = sum(chalk_wall)`.",
            ],
            checks=[TOTAL_HOURS],
            pass_line="Mar'tu: Three hundred and eleven hours. Most of them without sleep.",
        ),
        dict(
            id="print-the-shrink",
            text="Print how much the wall shrank: the longest gap minus the shortest.",
            dictated=False,
            hints=[
                "You already have both variables. Build the line from them, biggest first.",
                "With other names: `print(most - least)`.",
                "Write `print(longest - shortest)` at the bottom.",
            ],
            checks=[SHRINK_LINE],
            pass_line="Bomb Shell: Eleven hours gone. Not good.",
        ),
    ],
    solution=MAXMIN_SOLUTION,
    partials=[
        _maxmin(total="total_hours = 0", shrink=None),
        _maxmin(shrink=None),
    ],
    assemble=dict(
        lines=MAXMIN_SOLUTION.splitlines(),
        distractors=["longest = chalk_wall[0]", "total_hours = len(chalk_wall)", "longest = max[chalk_wall]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Three questions, one wall",
            text=(
                "```text\n48 48 47 46 44 41 37\n^^             max -> 48\n"
                "               ^^ min -> 37\nall added  sum -> 311\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A class register",
            text=(
                "Who is tallest? Who is shortest? Measure everyone, then pick: that is `max()` and `min()`. "
                "How much do all the bags weigh together? Add them all: that is `sum()`."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `max(chalk_wall)` looks at every gap and hands back the biggest.\n"
                "2. `min(chalk_wall)` hands back the smallest.\n"
                "3. `sum(chalk_wall)` adds them all.\n"
                "4. `longest - shortest` is the shrink."
            ),
        ),
        dict(angle="shorter", text="`max(wall)` biggest, `min(wall)` smallest, `sum(wall)` all added up."),
    ],
    bonus=dict(
        by="gearshift",
        title="The average gap",
        text=(
            "Gearshift wants the average gap in whole hours: the total shared out over the gaps. At the bottom, "
            "print `total_hours // len(chalk_wall)`."
        ),
        hints=["`//` divides and keeps the whole number. `len()` counts the gaps.",
               "Write `print(total_hours // len(chalk_wall))` at the bottom."],
        checks=[AVERAGE_BONUS],
        solution=MAXMIN_SOLUTION + "print(total_hours // len(chalk_wall))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="for member in party.members:\n    show_mana(member)",
        why=(
            "The bars showed each hero's mana, one by one. Put the four mana numbers in a list, and `sum()` gives "
            "the party's total, and `max()` the fullest bar."
        ),
    ),
    takeaway="`max(wall)` is the biggest, `min(wall)` the smallest, `sum(wall)` the total. `len(wall)` only counts.",
    wrong_answers=[
        dict(why="the starter (placeholders)", code=MAXMIN_STARTER, fails_at=1, message_contains="starter's `0`"),
        dict(why="typed by hand", code=_maxmin(longest="longest = 48", shrink=None), fails_at=1,
             message_contains="typed by hand"),
        dict(why="the first gap taken as the longest", code=_maxmin(longest="longest = chalk_wall[0]", shrink=None),
             fails_at=1, message_contains="not always the first"),
        dict(why="the newest gap taken as the shortest", code=_maxmin(shortest="shortest = chalk_wall[-1]", shrink=None),
             fails_at=1, message_contains="not always the newest"),
        dict(why="the first gap read as item 1 (index from 1): 48 here, 39 on the rerun wall",
             code=_maxmin(longest="longest = chalk_wall[1]", shrink=None), fails_at=1, message_contains="by its position"),
        dict(why="max of two positions only", code=_maxmin(longest="longest = max(chalk_wall[0], chalk_wall[1])", shrink=None),
             fails_at=1, message_contains="max(chalk_wall)"),
        dict(why="the shortest read by a position from the start (6)", code=_maxmin(shortest="shortest = chalk_wall[6]",
             shrink=None), fails_at=1, message_contains="any length"),
        dict(why="max and min swapped",
             code=_maxmin(longest="longest = min(chalk_wall)", shortest="shortest = max(chalk_wall)", shrink=None),
             fails_at=1, message_contains="Swap them"),
        dict(why="square brackets after max", code=_maxmin(longest="longest = max[chalk_wall]"), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="max as a list tool (dot)", code=_maxmin(longest="longest = chalk_wall.max()"), fails_at=0,
             message_contains="no attribute"),
        dict(why="the example's list name copied", code=_maxmin(longest="longest = max(coins)"), fails_at=0,
             message_contains="not defined"),
        dict(why="len counts, sum adds", code=_maxmin(total="total_hours = len(chalk_wall)", shrink=None), fails_at=2,
             message_contains="len()"),
        dict(why="every position added one by one (fits a wall of seven only)",
             code=_maxmin(total="total_hours = chalk_wall[0] + chalk_wall[1] + chalk_wall[2] + chalk_wall[3] + "
                          "chalk_wall[4] + chalk_wall[5] + chalk_wall[6]", shrink=None), fails_at=2,
             message_contains="sum(chalk_wall)"),
        dict(why="every gap typed and added by hand",
             code=_maxmin(total="total_hours = 48 + 48 + 47 + 46 + 44 + 41 + 37", shrink=None), fails_at=2,
             message_contains="not by typing"),
        dict(why="the shrink typed by hand", code=_maxmin(shrink="print(11)"), fails_at=3, message_contains="you typed"),
        dict(why="the gaps typed into the subtraction", code=_maxmin(shrink="print(48 - 37)"), fails_at=3,
             message_contains="you typed"),
        dict(why="shortest minus longest", code=_maxmin(shrink="print(shortest - longest)"), fails_at=3,
             message_contains="Longest first"),
        dict(why="an answer typed for each wall the check showed (print the expected result directly)",
             code=_maxmin(shrink="print(11)\nprint(7)\nprint(30)"), fails_at=3, message_contains="typed for each wall"),
        dict(why="the first gap minus the newest (fits a wall that only shrinks)",
             code=_maxmin(shrink="print(chalk_wall[0] - chalk_wall[-1])"), fails_at=3,
             message_contains="On Mar'tu's other wall it is 7"),
        dict(why="the longest printed, not the shrink (the student's own wall answers)",
             code=_maxmin(shrink="print(longest)"), fails_at=3, message_contains="On your wall it is 11"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="list-max-min-sum", solo="false", dictates="",
             foreign_names="coins,most,least") + "\n"
        "3C-03 (O). Intro call:max, call:min, call:sum. CP1 [ND] goal-first (teacher ruling; the last hint holds the "
        "lines). Reruns with [41, 39, 46, 44] (the longest is at position 2, "
        "so neither `[0]` nor the count-from-1 `[1]` finds it; the shortest is not newest) and [60, 30, 45]. "
        "Catches: typed values, `[0]` / `[1]` / `[-1]` for max / min, swapped tools, `max[chalk_wall]` (square "
        "brackets: a crash), `chalk_wall.max()`, `len` for `sum`, a typed sum, positions added one by one (an "
        "IndexError on a shorter wall, answered with `sum`), a typed, reversed or per-wall shrink (one print line "
        "must answer every wall). Bonus: `//` (1D) + `len` for a whole-hours average."
    ),
)

# ---- SOLO 3C ------------------------------------------------------------------------------------------------

SOLO_3C_STARTER = WALL_LINE + "longest = max[chalk_wall]\nprint(\"Longest: \" + str(longest))\n"
SOLO_3C_SOLUTION = WALL_LINE + "longest = max(chalk_wall)\nprint(\"Longest: \" + str(longest))\n"

SOLO_LONGEST = chk(
    "the longest gap prints, read from the list",
    r'''
_own_rows = _lines()
_w0 = globals().get('chalk_wall')
_own_want = _B.max(_w0) if type(_w0).__name__ == 'list' and _w0 else 48
_own_hits = _rows_with(_own_rows, lambda _l: _own_want in _nums(_l))
# The longest gap sits at position 2 in one wall and position 1 in the other, so no one position fits both.
for _vals in (None, {'chalk_wall': [41, 39, 46, 44]}, {'chalk_wall': [30, 52]}):
    _ns, _rows, _err, _miss, _seen = _case(_vals)
    assert not _miss, _keep('chalk_wall')
    _start = [48, 48, 47, 46, 44, 41, 37] if _vals is None else _vals['chalk_wall']
    _want = _B.max(_start)
    _hits = _rows_with(_rows, lambda _l: _want in _nums(_l))
    if _hits and (_vals is None or _same_row(_own_rows, _own_hits, _rows, _hits)):
        continue
    # SOLO (lean): each message names the slip and keeps the evidence bracket, never the tool to write.
    assert not _err, 'With another wall, Python stopped: ' + _err + '.' + _ev(_vals)
    _got = _ns.get('longest')
    assert not (_vals is not None and _got == _start[0]), (
        'Your line reads the first gap, and the longest gap is not always the first.' + _ev(_vals))
    assert not (_vals is not None and _got in _start), (
        'Your line picked a gap by its position, and the longest gap is not always there.' + _ev(_vals))
    assert not _hits, 'A number was typed for each wall, so a new wall gets no answer.' + _ev(_vals)
    assert False, 'The longest gap was typed, so the line does not follow the wall.' + _ev(_vals)
''',
)

# Lean, proved: the SOLO's check never names its fix (as Unit 2's _leaned asserts for QC2's rewrites).
assert "max(chalk_wall)" not in SOLO_LONGEST[1].replace(" ", ""), "solo-3c's check names its fix"

SOLO_3C = dict(
    id="solo-3c",
    title="Show Mar'tu",
    martu="A short one, just for you. One slip. Read the last line, then mend it.",
    solo=True,
    explainer="lean",
    names=["chalk_wall", "longest"],
    starter=SOLO_3C_STARTER,
    checkpoints=[
        dict(
            id="make-it-print",
            text="Mend line 2 so the program prints the longest gap.",
            dictated=False,
            hints=[
                "Read Python's last line. *Not subscriptable* means: this can't take square brackets.",
                "Look at line 2. `max` is a tool you call, like `print` and `len`.",
                "You call a tool with round brackets: `len(coins)`. Square brackets read a list: `coins[0]`.",
            ],
            checks=[SOLO_LONGEST],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ round brackets call a tool, square ones read a list.",
        ),
    ],
    solution=SOLO_3C_SOLUTION,
    another_way=[
        dict(angle="step-by-step", text="1. Read the last line. 2. Line 2. 3. Round brackets after `max`."),
        dict(angle="shorter", text="Call with `( )`. Read a list with `[ ]`."),
    ],
    takeaway="On your own: round brackets call a tool, `max(chalk_wall)`; square brackets read a list, `chalk_wall[0]`.",
    wrong_answers=[
        dict(why="the starter (square brackets after max)", code=SOLO_3C_STARTER, fails_at=0,
             message_contains="not subscriptable"),
        dict(why="the longest typed by hand", code=WALL_LINE + "longest = 48\nprint(\"Longest: \" + str(longest))\n",
             fails_at=1, message_contains="The longest gap was typed"),
        dict(why="the first gap read instead", code=WALL_LINE + "longest = chalk_wall[0]\nprint(\"Longest: \" + str(longest))\n",
             fails_at=1, message_contains="reads the first gap, and the longest gap is not always the first"),
        dict(why="the line typed by hand", code=WALL_LINE + "print(\"Longest: 48\")\n", fails_at=1,
             message_contains="does not follow the wall"),
        dict(why="the first gap read as item 1 (index from 1)",
             code=WALL_LINE + "longest = chalk_wall[1]\nprint(\"Longest: \" + str(longest))\n", fails_at=1,
             message_contains="by its position"),
        dict(why="an answer typed for each wall the check showed",
             code=WALL_LINE + "print(\"Longest: 48\")\nprint(46)\nprint(52)\n", fails_at=1,
             message_contains="typed for each wall"),
        dict(why="a dot instead of a call", code=WALL_LINE + "longest = chalk_wall.max()\nprint(\"Longest: \" + str(longest))\n",
             fails_at=0, message_contains="no attribute"),
    ],
    notes=(
        meta(starter_level="S4", path="optional", skills="list-max-min-sum,read-traceback", solo="true", dictates="",
             foreign_names="coins",
             seat_b='shortest = min[chalk_wall] (the same TypeError, with min)') + "\n"
        "SOLO, one bug: `max[chalk_wall]` (square brackets versus round ones: TypeError 'not subscriptable'). Rung 0 "
        "is 'Read Python's last line'; the pass line uses Unit 2's form; explainer='lean' (teacher ruling: every "
        "SOLO from Unit 2 on). Added to Lesson 3C so the lesson has its one SOLO (2.12 lint g); the spec lists "
        "3C-01 to 3C-03 only. CMB with [41, 39, 46, 44] and [30, 52]: the longest sits at a different position in each, "
        "so `chalk_wall[1]` (counting from 1) fails. One print line must answer every wall (no typed answer per wall)."
    ),
)

LESSON_3C = dict(
    kind="lesson",
    id="more-list-tools",
    title="More List Tools",
    optional=True,
    minutes=15,
    summary="Insert and pop, remove and `in`, and `max`, `min` and `sum`: more ways to work a list without retyping it.",
    notes=(
        "Lesson 3C (O). 3C-01 insert-and-pop, 3C-02 remove-and-in, 3C-03 biggest-and-smallest, then one SOLO "
        "(solo-3c, added for lint g). Non-dictated checkpoints: 3C-01 CP1, 3C-02 CP1-3, 3C-03 CP1-3, solo-3c. "
        "Prerequisite for "
        "3P2 'The Basement Inventory' (u04c)."
    ),
    exercises=[INSERT_AND_POP, REMOVE_AND_IN, BIGGEST_AND_SMALLEST, SOLO_3C],
)


# =============================================================================================
# Quiz 3B (optional, 8 questions): range, sort -> None, slices
# =============================================================================================

QUIZ_3B = dict(
    kind="quiz",
    id="ranges-and-slices-quiz",
    title="Quiz: Ranges, Slices and Sorting",
    optional=True,
    minutes=8,
    summary="Eight questions on `range`, `sorted` and `.sort()`, and slices. Retake as often as you like.",
    notes="Quiz 3B (O): 4 predict, 1 mc, 1 bug, 1 fill, 1 parsons. One def/return item (question 8), per 2.4.",
    questions=[
        dict(
            type="predict",
            id="range-stops-before",
            q="What will this print?",
            code="print(list(range(3, 7)))\n",
            choices=["[4, 5, 6, 7]", "[3, 7]", "[3, 4, 5, 6]", "[3, 4, 5, 6, 7]"],
            answer="[3, 4, 5, 6]",
            explain="`range` starts at the first number and stops *before* the second. So 7 is left out.",
        ),
        dict(
            type="mc",
            id="d10-faces",
            q="A d10 has faces 1 to 10. Which `range` makes them?",
            choices=["range(1, 10)", "range(10)", "range(0, 10)", "range(1, 11)"],
            answer=3,
            why_wrong={
                0: "`range` stops before its end number, so `range(1, 10)` stops at 9.",
                1: "`range(10)` starts at 0 and stops at 9.",
                2: "This starts at 0, and a d10 has no 0 face. It also stops at 9.",
            },
            explain="`range(1, 11)` gives 1 up to 10: it stops before 11. `randint(1, 10)` includes both ends instead.",
        ),
        dict(
            type="predict",
            id="sort-hands-back-none",
            q="What will this print?",
            code="wall = [48, 37, 44]\nx = wall.sort()\nprint(x)\n",
            choices=["[37, 44, 48]", "None", "[48, 37, 44]", "ERROR"],
            answer="None",
            explain=(
                "`.sort()` sorts `wall` itself and hands back nothing: `None`. So `x` holds `None`. Like a recipe "
                "with no `return`."
            ),
        ),
        dict(
            type="bug",
            id="keep-the-sorted-copy",
            q="This should print the gaps shortest first. Mend it.",
            code="wall = [44, 48, 37]\nordered = wall.sort()\nprint(ordered)\n",
            fix="wall = [44, 48, 37]\nordered = sorted(wall)\nprint(ordered)\n",
            expected_output="[37, 44, 48]",
            explain="`sorted(wall)` hands back a sorted copy, so `ordered` holds it. `wall.sort()` hands back `None`.",
        ),
        dict(
            type="predict",
            id="slice-end-left-out",
            q="`chalk_wall` holds `[48, 48, 47, 46, 44, 41, 37]`. What will this print?",
            setup=WALL_LINE,
            code="print(chalk_wall[1:3])\n",
            choices=["[48, 48, 47]", "[48, 48]", "[48, 47, 46]", "[48, 47]"],
            answer="[48, 47]",
            explain=(
                "Position 1 is the second 48. A slice stops *before* its end number, so it takes positions 1 and "
                "2: `[48, 47]`."
            ),
        ),
        dict(
            type="fill",
            id="newest-two",
            q="Fill the blank so the program prints the two newest gaps. Count from the end, so it works for a wall "
              "of any length.",
            code="wall = [46, 44, 41, 37]\nnewest_two = wall[___]\nprint(newest_two)\n",
            answer="-2:",
            accept=["-2:len(wall)", "len(wall)-2:", "len(wall) - 2:"],
            expected_output="[41, 37]",
            explain=(
                "`[-2:]` starts two from the end and runs to the very end, so it works for a wall of any length. "
                "`[2:]` also prints `[41, 37]` here, but only because this wall has four gaps."
            ),
            notes="Accepts only answers that count from the end (the 3B-05 and 3C rule: a wall of any length).",
        ),
        dict(
            type="parsons",
            id="newest-three-shortest-first",
            q="Put the lines in order so the program prints the three newest gaps in `wall`, shortest first.",
            lines=[
                "wall = [46, 44, 41, 37]",
                "newest_three = wall[-3:]",
                "in_order = sorted(newest_three)",
                "print(in_order)",
            ],
            distractors=["in_order = newest_three.sort()", "newest_three = wall[-3:-1]"],
            expected_output="[37, 41, 44]",
            explain=(
                "Slice first, then sort a copy with `sorted()`. `.sort()` would hand back `None`, and `[-3:-1]` "
                "leaves out the newest gap."
            ),
            notes="Distractors: the two slips this quiz is about (x = x.sort(), the slice end).",
        ),
        dict(
            type="predict",
            id="recipe-hands-back-a-slice",
            q="What will this print?",
            code="def oldest_two(wall):\n    return wall[:2]\n\nprint(oldest_two([9, 8, 7]))\n",
            choices=["[9, 8]", "[9, 8, 7]", "[8, 7]", "[9]"],
            answer="[9, 8]",
            explain=(
                "The recipe gets `[9, 8, 7]` as `wall` and hands back `wall[:2]`: from the start, stopping before "
                "position 2. That is `[9, 8]`."
            ),
            notes="The def/return item (2.4: every unit quiz has one from Unit 4 on).",
        ),
    ],
)


ITEMS = [
    EXTRA_4X,
    PROJECT_3P1,
    LESSON_3C,
    QUIZ_3B,
]
