"""Unit 4 "Lists", part c: Article 3-A1 "Tuples", Article 3-A2 "zip()", Project 3P2 "The Basement Inventory",
the optional advanced challenge "One List, Same Answer", Quick Check 3 (forms qc3-a and qc3-b, with their question
forms qc3-a-questions and qc3-b-questions) and the Lists cheatsheet ("Mar'tu's Chalk Notes: Lists").

Spec: design/curriculum.md, "## Unit 4 · Lists", "### Extra practice 4X [pool] and the optional items" (3-A1, 3-A2,
3P2), "### Quick Check 3" and "### Cheatsheet: Lists" (items 8 to 11).
Introduces node:Tuple (3-A1) and call:zip (3-A2). Everything else comes from u04a (lists, positions, append, len,
range, slices, sorted / .sort()), u04b (.count, .insert, .pop, .remove, in, max / min / sum) and Unit 3's planned
concepts (u03a/u03b: a simple def with a parameter and return, used only in QC C2's recipe `newest_three` and the
cheatsheet's recipe entry). No `for` (Unit 6), no f-strings or `\\n` escapes (Unit 9), no dictionaries (Unit 5), no
`not in` (u05a), no keyword arguments (u07c), and `None` only ever appears as printed output (u07b).
The project names its prerequisites (core-only rule, 2.12 rule 2): More List Tools (insert, pop), How many times?
(.count) and the zip() article.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN lists there:
`party.members` (the loop in the spell-book and mana-bars parts), the chalk wall's gaps (Module 2 part 9,
chalk-wall), Mar'tu's four dialogue options (Module 1 part 7, program-dialogue-options) and Mar'tu's basement full
of brass instruments (the-resonance-array). Campaign links are "you've seen this, now you'll get it" moments.
Every student has their own device; pair talk is optional and every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them, as Units 2 and 3): hints[0] Where to look (point),
the middle hints Teach me (a tiny example with other names), the last hint Show me how: the step's own line in
backticks (``Write `x = 1`.``), whose start up to its first `(` or `=` becomes Start me off. another_way, assemble
(More structure), then Compare. Where the start would hand over the step's decision (fix-a-mark's position), the
last hint's first code span has no `=`, so there is no Start me off.
In debug steps hints[0] is "Read Python's last line" (for a quiet bug: what the program printed). Quick Check exercises are
support="none" (the hints are written because the schema needs them) and explainer="lean" (teacher ruling: every
QC exercise from Unit 2 on).

Check builders (u04b's rerun idea, extended): _rerun(values, appends, watch) re-runs the student's code with
top-level `name = [...]` / `name = (...)` lines replaced, the item of a top-level `name.append(x)`,
`name = name + [x]` or `name += [x]` replaced, and, when `watch` names lists, a snapshot of those lists taken after
every top-level line. The project's checks read the snapshots, so task 3 is judged on the lists right after the
insert, even when a later line (a pop, or a slip like `counts.sort()`) changes them again.
In the articles, the project and the challenge, messages lead with the fix, then what happened, then the evidence
in brackets, "(Mar'tu's check tried `counts = [4, 0, 11, 0, 8]`, only inside the check.)", about 35 words or
fewer, invented values only (2.11): the project's messages say "a part you typed", never the student's own words.
Quick Check messages are lean (Unit 2 ruling): they name the slip and keep the evidence bracket, never the line to
type; a near-miss name gets the lesson's "Python matches names letter for letter: you wrote `mark`, the task needs
`marks`." The rerun data uses invented Tor-style names only (Pell, Brakka, Moss, Glug, as u04a).

The class's slips for this unit, each proven by a wrong_answers entry:
  index from 0: project task 3 `.insert(2, ...)`, QC C1 CP3 `marks[2] = 43`, QC C3 `roster[3][1]` /
  `drills[2][1]`, tuples try-it `cabin[1]` / `cabin[2]`, challenge `chalk_wall[1]` for the oldest;
  `-1` versus `len`: QC C1 `marks[3]` (a longer list in the rerun) and `min(marks)` / `max(ore_used)` (the
  rerun's appended guess sits mid-list, so only a read from the end finds it), QC C2 a start counted for 7
  (`wall[4:]`), challenge `chalk_wall[6]`, zip try-it `pairs[3]`;
  `len` used as an index (IndexError): QC C1 `marks[len(marks)]`, QC C2 `wall[len(wall)]`, challenge
  `chalk_wall[len(chalk_wall)]`, project `parts.pop(len(parts))`;
  append versus `+` versus a new list: QC C1 (`marks + [33]` thrown away, `marks + 33` TypeError, a second
  `marks = [...]`, and CP3's `.append(43)` for a change by position), project task 3 (`.append` for `.insert`, an
  append left beside the insert);
  `.sort()` hands back None (nothing came back): project task 5 `top_three = counts.sort()`, QC C3 (the starter);
  the slice end is left out: project task 5 `[-3:-1]`, QC C2 `[-3:-1]`, QC Q2 (`range(1, 4)` stops before 4);
  values typed by hand: every task (a typed print, a typed list, a typed pair, a typed count), and values read
  some other way: QC C1 `print(guess)`, QC C3 the same number read from `manas`, QC C2 three reads with no slice,
  pairs read one by one with no `zip()` (try-it and project task 7), QC C2 `sorted(...)[-3:]` (the biggest, not
  the newest: the longer list the check hands the recipe is not in order), QC C1 CP3 the whole list retyped with
  43 (a rerun catches `list([...])` too), the challenge's typed shrink (`11`, `48 - 37`);
  the example's name copied: tuples try-it `row, seat = cabin`, zip try-it `zip(coins, values)`, the hints' names
  `tools` / `stock` / `taken` (project) and `steps` (QC C1), the challenge's example list `nights`, and QC C2's
  outer `chalk_wall` / `ore_used` read inside the recipe in place of its ingredient;
  a copy changed instead of the original (and the other way round): project task 5 `counts.sort()` (the counts no
  longer line up with their parts) and `biggest = counts` then `biggest.sort()`, QC C3 `ordered = manas` then
  `ordered.sort()`, QC C2 `wall.sort()` inside the recipe (the list it is handed, sorted in place);
  square brackets versus round ones: tuples try-it (`cabin` left a list; the predict's `.append` on a tuple),
  project task 1 `parts = (...)`, QC C1 `marks = (46, 44, 41)` and `marks.append[33]`, QC C2 `wall(-3:)`,
  challenge `chalk_wall = (48, ...)`, project task 6 `counts.count[0]`.
Parallel lists kept in step (the project's point): two pops off one list, an insert after the pop, two inserts.
`zip()` stops at the shorter list, so task 7 alone would hide a list that slipped out of step: task 4 checks that
both lists end exactly one item shorter than after task 3.

Quick Check 3 has three code tasks per form: C1 make, append, fix by position, read the last; C2 the recipe
`newest_three(wall)` (`newest_three(days)` in form B), a recipe that takes a list and slices it, called by
Mar'tu's check on fresh lists; C3 a nested read and a sorted copy, mended. The site gates on the code tasks and the
two questions (questions_to_pass=2: "Both right is a pass", as QC2 gates on its questions), and, as with the
teacher's Unit 2 ruling, the code tasks alone cover every skill the QC claims. Teacher ruling on the Unit 4 reviews: a true fast path with no fourth task (C1's
fix by position is objective 3, C2's recipe objective 5), Q2 is a `range` + `+` predict (C3 tests sort/None in
code), 14 minutes. Form B's list is Bomb Shell's Velocite ore, `ore_used` (chunks used each day). Every choice
question authors its right answer in a different place (the site also shuffles).
The challenge "One List, Same Answer" (optional, advanced, about 10 minutes, support light) refactors 3A-01's seven
boxes into `chalk_wall`, for the ready-to-stretch group; it costs no one any core time.

Phone width (as u04a/u04b): fenced pictures, examples, predict code, quiz code, cheatsheet code and starter lines
keep to 36 characters or fewer. The exceptions are the real wall, `chalk_wall = [48, 48, 47, 46, 44, 41, 37]`
(41 characters), kept whole on one line in editor code (QC C2 form A and the challenge); and, as in u04a, the
teacher's second recipe call in QC C2 (both forms) keeps its "# This should show ..." comment on the same line,
as dictated (editor code). Quiz questions keep the wall in `setup` and show it in the question text. Form B's story
comment "# Bomb Shell's Velocite ore: chunks used each day." is wrapped onto two comment lines to fit.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u04c
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# Shared by every check: the rerun, the snapshots, the evidence bracket and a few readers. Plain Python, run in the
# student's namespace after their code, so every name starts with `_` and builtins come from `_B` (a student's
# `max = 48` can't break a check).
_PRE = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import builtins as _B
def _sh(_v):
    _k = type(_v).__name__
    if _k == 'str':
        return '"' + _v + '"'
    if _k == 'list':
        return '[' + ', '.join([_sh(_x) for _x in _v]) + ']'
    if _k == 'tuple':
        return '(' + ', '.join([_sh(_x) for _x in _v]) + (',)' if _B.len(_v) == 1 else ')')
    return _B.str(_v)
def _numsonly(_v):
    _k = type(_v).__name__
    if _k == 'int':
        return True
    if _k in ('list', 'tuple'):
        return _B.all([_numsonly(_x) for _x in _v])
    return False
def _shn(_v, _other='something else'):
    # A student's own value is shown only when it is numbers: never their words (2.11).
    return _sh(_v) if _numsonly(_v) else _other
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _one_item(_node):
    return type(_node).__name__ == 'List' and _B.len(_node.elts) == 1
def _copy(_v):
    return _B.list(_v) if type(_v).__name__ == 'list' else _v
def _rerun(_values=None, _appends=None, _watch=()):
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
                    and type(_n.value.args[0]).__name__ in ('List', 'Name', 'Constant', 'UnaryOp')):
                _n.value.args[0] = _lit(_apps[_f.value.id], _n.value.args[0])
                _seen.append(_f.value.id + '.append')
    _ns = {'__name__': '__main__'}
    _snaps = []
    if _watch:
        _body = []
        for _n in _tree.body:
            _body.append(_n)
            _snap = _ast.Expr(_ast.Call(_ast.Name('_course_snap_', _ast.Load()), [], []))
            _body.append(_ast.copy_location(_snap, _n))
        _tree.body = _body
        _ns['_course_snap_'] = lambda: _snaps.append(_B.dict([(_w, _copy(_ns.get(_w))) for _w in _watch]))
    _ast.fix_missing_locations(_tree)
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
    return _ns, _rows, _err, [_x for _x in _vals if _x not in _seen], _seen, _snaps
def _case(_vals, _apps=None, _watch=()):
    # None: the student's own run, as it is now (no evidence bracket). With _watch, a plain rerun for snapshots.
    if _vals is None and not _watch:
        return globals(), _lines(), '', [], [], []
    return _rerun(_vals, _apps, _watch)
def _ev(_vals, _apps=None, _only=None):
    if _vals is None:
        return ''
    _bits = ['`' + _k + ' = ' + _sh(_v) + '`' for _k, _v in _vals.items() if _only is None or _k in _only]
    _t = " (Mar'tu's check tried " + (' and '.join(_bits) if _bits else 'other lists')
    for _k, _v in (_apps or {}).items():
        _t += ', then appended `' + _sh(_v) + '`'
    return _t + ', only inside the check.)'
def _keep(_name):
    return ('Keep the line `' + _name + " = [...]` from the starter, so Mar'tu's check can try another list there.")
def _stop(_vals, _apps, _err, _fix='Make it work for another list too.', _only=None):
    if _err.startswith('IndexError'):
        _fix = 'Count from the end with `[-1]`, so it works for a list of any length.'
    return _fix + ' With another list, Python stopped: ' + _err + '.' + _ev(_vals, _apps, _only)
def _nums(_l):
    return [_B.int(_x) for _x in _re.findall(r'(?<![\d.])-?\d+(?!\d)(?!\.\d)', _l)]
def _plain(_rows):
    # printed lines that are not a whole list or tuple
    return [_l for _l in _rows if not _l.startswith('[') and not _l.startswith('(')]
def _lastnums(_rows):
    return [_nums(_l)[-1] for _l in _plain(_rows) if _nums(_l)]
def _calls_of(_attr, _on=None):
    return [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call'
            and type(_n.func).__name__ == 'Attribute' and _n.func.attr == _attr
            and (_on is None or (type(_n.func.value).__name__ == 'Name' and _n.func.value.id == _on))]
def _assigns(_name):
    return [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' and _B.len(_n.targets) == 1
            and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == _name]
def _first_lit(_name):
    # The first `name = ...` that holds something (a `name = []` above it is still the starter's line).
    _made = _assigns(_name)
    if not _made:
        return 'missing', None
    _full = [_n for _n in _made if not (type(_n.value).__name__ in ('List', 'Tuple') and not _n.value.elts)]
    _node = (_full or _made)[0].value
    try:
        return type(_node).__name__, _ast.literal_eval(_node)
    except Exception:
        return type(_node).__name__, globals().get(_name)
def _is_int(_v):
    return type(_v).__name__ == 'int'
def _is_list(_v):
    return type(_v).__name__ == 'list'
def _ins_at(_got, _orig):
    # The position where one item was squeezed into _orig to make _got, or -1.
    if not (_is_list(_got) and _is_list(_orig)) or _B.len(_got) != _B.len(_orig) + 1:
        return -1
    for _k in [1] + _B.list(_B.range(_B.len(_got))):
        if _got[:_k] + _got[_k + 1:] == _orig:
            return _k
    return -1
def _same_items(_a, _b):
    try:
        return _B.sorted(_a) == _B.sorted(_b)
    except Exception:
        return False
def _typed_list(_name):
    # `name = [...]` lines whose items are all typed values (no names, no reads).
    _out = []
    for _n in _assigns(_name):
        if type(_n.value).__name__ == 'List' and _n.value.elts:
            try:
                _ast.literal_eval(_n.value)
                _out.append(_n)
            except Exception:
                pass
    return _out
def _typed_print():
    # a print(...) whose arguments are all typed values
    return [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call'
            and type(_n.func).__name__ == 'Name' and _n.func.id == 'print' and _n.args
            and _B.all([type(_a).__name__ == 'Constant' for _a in _n.args])]
# Near-miss names (as Unit 1 and u04a): the names the student made, and the ones close to a task name.
def _made_names():
    _out = []
    for _n in _ast.walk(_ast.parse(_source)):
        _k = type(_n).__name__
        _ts = _n.targets if _k == 'Assign' else ([_n.target] if _k == 'AugAssign' else [])
        _ids = [_t.id for _t in _ts if type(_t).__name__ == 'Name'] + ([_n.name] if _k == 'FunctionDef' else [])
        for _i in _ids:
            if _i not in _out:
                _out.append(_i)
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
def _near(_w):
    return [_m for _m in _made_names() if _m != _w and _close(_m, _w)]
def _lost(_w, _what='list'):
    # Lean (Quick Check): a near-miss name gets the lesson's sentence; otherwise the slip, with no line to type.
    _n = _near(_w)
    if _n:
        return 'Python matches names letter for letter: you wrote `' + _n[0] + '`, the task needs `' + _w + '`.'
    return ("Mar'tu's check found no `" + _w + ' = ...` line, so it has no ' + _what + ' to try.')
def _lstop(_vals, _apps, _err, _only=None):
    # Lean _stop: what stopped Python, and the evidence. No fix.
    return 'With another list, Python stopped: ' + _err + '.' + _ev(_vals, _apps, _only)
def _call(_fn, _a):
    # Call a recipe with a fresh copy of a list, quietly: (what it handed back, what it printed, the error).
    _keep_out = _sys.stdout
    _sys.stdout = _io.StringIO()
    _out, _err = None, ''
    try:
        _out = _fn(_B.list(_a))
    except Exception as _x:
        _err = type(_x).__name__ + ': ' + _B.str(_x)
    finally:
        _pr = _sys.stdout.getvalue().strip()
        _sys.stdout = _keep_out
    return _out, _pr, _err
'''


def chk(label, body, **subs):
    """A check: the shared _PRE, then `body` with each __NAME__ replaced by repr(value)."""
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    return (label, _PRE + body)


WALL = [48, 48, 47, 46, 44, 41, 37]
WALL_LINE = "chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"
ROSTER = [["Oogrish", 18], ["Gearshift", 20], ["Bomb Shell", 24], ["Lucky", 26]]
ROSTER_CODE = (
    "roster = [\n"
    '    ["Oogrish", 18],\n'
    '    ["Gearshift", 20],\n'
    '    ["Bomb Shell", 24],\n'
    '    ["Lucky", 26],\n'
    "]\n"
)
DRILLS = [["cane parry", 7], ["shield wall", 5], ["slow breaths", 9], ["roll and rise", 6]]
DRILLS_CODE = (
    "drills = [\n"
    '    ["cane parry", 7],\n'
    '    ["shield wall", 5],\n'
    '    ["slow breaths", 9],\n'
    '    ["roll and rise", 6],\n'
    "]\n"
)
ORE = [2, 3, 3, 4, 5, 7]
ORE_LINE = "ore_used = [2, 3, 3, 4, 5, 7]\n"
# Form B's story line, as a starter comment (two lines, for phone width).
ORE_STORY = "# Bomb Shell's Velocite ore:\n# chunks used each day.\n"


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

# New terms only (this part's). u04a and u04b define the unit's other list terms; Units 1-3 define theirs.
GLOSSARY = [
    dict(
        term="tuple",
        aliases=["tuples"],
        plain=(
            "Like a list that can't change. Round brackets instead of square ones. You read it by position, like a "
            "list, but you can't add, remove or swap its items."
        ),
        example='hero = ("Lucky", 26)',
    ),
    dict(
        term="zip()",
        aliases=["zip"],
        plain=(
            "Pairs up two lists, item by item: first with first, second with second. Each pair is a tuple. Wrap it "
            "in `list()` to see the pairs."
        ),
        example="list(zip(heroes, manas))",
    ),
    dict(
        term="parallel lists",
        aliases=["parallel list", "lists in step"],
        plain=(
            "Two lists kept in step: item 0 of one goes with item 0 of the other, and so on. Change one, and you "
            "must change the other the same way."
        ),
        example='parts = ["lens", "coil"]\ncounts = [3, 7]',
    ),
]


# =============================================================================================
# Article 3-A1 "Tuples" (optional, node:Tuple), with one try-it
# =============================================================================================

CABIN_STARTER = (
    "# Mar'tu's cabin on the map:\n"
    "# 12 across, 5 down.\n"
    "# 1. Make cabin a tuple.\n"
    "cabin = [12, 5]\n"
    "# 2. Unpack it: across, down.\n"
    "\n"
    "# 3. Print across, then down.\n"
    "\n"
)


def _cabin(make="cabin = (12, 5)", unpack="across, down = cabin", show="print(across, down)"):
    code = CABIN_STARTER.replace("cabin = [12, 5]\n", make + "\n")
    if unpack is not None:
        code = code.replace("# 2. Unpack it: across, down.\n\n", "# 2. Unpack it: across, down.\n" + unpack + "\n")
    if show is not None:
        code = code.replace("# 3. Print across, then down.\n\n", "# 3. Print across, then down.\n" + show + "\n")
    return code


CABIN_SOLUTION = _cabin()
CABIN_OTHER = {"cabin": (30, 9)}

CABIN_MADE = chk(
    "cabin is a tuple: 12 across, 5 down",
    r'''
_g = globals()
assert 'cabin' in _g, 'Keep the line `cabin = ...` from the starter, and change its brackets.'
_c = _g['cabin']
_k = type(_c).__name__
assert _k != 'list', '`cabin` is still a list: square brackets. Use round brackets for a tuple: `cabin = (12, 5)`.'
assert _k != 'int', '`(12)` on its own is just a number. A tuple needs a comma between its items: `(12, 5)`.'
assert _k == 'tuple', 'Make `cabin` a tuple: two numbers between round brackets, `(12, 5)`.'
assert not [_x for _x in _c if type(_x).__name__ == 'str'], 'Take the quotes off: 12 and 5 are numbers.'
assert _c != (5, 12), 'Across comes first, then down: `(12, 5)`.'
assert _c == (12, 5), 'Keep the two numbers, 12 across and 5 down: `cabin = (12, 5)`. `cabin` holds ' + _shn(_c) + '.'
''',
)

CABIN_UNPACKED = chk(
    "across and down are read from cabin",
    r'''
_g = globals()
_left = [_m for _m in ('row', 'seat', 'door') if _m in _g]
assert not (_left and not ('across' in _g and 'down' in _g)), (
    '`' + (_left[0] if _left else '') + '` is a name from the example. This task' + chr(39)
    + 's names are `across` and `down`: `across, down = cabin`.')
assert 'across' in _g and 'down' in _g, 'Make `across` and `down` in one line: `across, down = cabin`.'
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    assert not _miss, 'Keep the line `cabin = (12, 5)`, so Mar' + chr(39) + 'tu' + chr(39) + 's check can try another spot there.'
    _c = _ns.get('cabin')
    _a, _d = _ns.get('across'), _ns.get('down')
    _two = type(_c).__name__ == 'tuple' and _B.len(_c) == 2
    if _two and _a == _c[0] and _d == _c[1]:
        continue
    assert not _err, _stop(_vals, None, _err, 'Make it work for another spot too.')
    assert type(_a).__name__ not in ('tuple', 'list'), ('`across` holds the whole tuple. Put two names on the left, '
                                                        'and Python hands out the items: `across, down = cabin`.')
    assert not (_two and _a == _c[1] and _d == _c[0]), ('Across comes first: `across, down = cabin`. Your two names '
                                                        'are the other way round.' + _ev(_vals))
    assert not (_vals is not None and _a == _g['across'] and _d == _g['down']), (
        'Read them from `cabin`: `across, down = cabin`. `across` stayed ' + _shn(_a, 'the same') + ', typed by hand.'
        + _ev(_vals))
    assert False, 'Unpack `cabin` into `across` and `down`: `across, down = cabin`.' + _ev(_vals)
''',
    OTHER=CABIN_OTHER,
)

CABIN_SHOWN = chk(
    "across, then down, are printed",
    r'''
_own = _B.sum([_nums(_l) for _l in _plain(_lines())], [])
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    _c = _ns.get('cabin')
    _want = _B.list(_c) if type(_c).__name__ == 'tuple' and _B.len(_c) == 2 else [12, 5]
    _got = _B.sum([_nums(_l) for _l in _plain(_rows)], [])
    _at = [_i for _i, _x in _B.enumerate(_got) if _x == _want[0]]
    if _at and _want[1] in _got[_at[0] + 1:]:
        continue
    assert not _err, _stop(_vals, None, _err, 'Make it work for another spot too.')
    assert not [_l for _l in _rows if _l.startswith('(')], ('Print the two numbers with their names, `across` and '
                                                            '`down`. Your line shows the whole tuple.')
    assert _got, 'Print `across`, then `down`: `print(across, down)`.'
    assert not (_vals is not None and _got == _own), ('Print the variables, `across` and `down`, so the line follows '
                                                     'the map. Your line shows numbers typed by hand.' + _ev(_vals))
    assert not (_want[1] in _got and _want[0] in _got), 'Print across first, then down.'
    assert False, 'Print both: `across`, then `down`. Your program printed ' + _B.str(_got) + '.' + _ev(_vals)
''',
    OTHER=CABIN_OTHER,
)

CABIN_ON_THE_MAP = dict(
    id="cabin-on-the-map",
    title="A spot on the map",
    martu=(
        "A spot on the map of Tor is two numbers: across, then down. My cabin sits at 12 across, 5 down. The "
        "cabin does not move, so a [[tuple]] fits, yes?\n"
        "Round brackets make a tuple. Two names on the left of `=` unpack it: each name takes one item, in order."
    ),
    example="door = (3, 8)\nrow, seat = door\nprint(row)\nprint(seat)\n",
    example_output="3\n8",
    introduces=["node:Tuple"],
    names=["cabin", "across", "down"],
    predict=dict(
        q="A tuple can't change. Before you press Run: what happens here?",
        code='bag = ("rope", "lamp")\nbag.append("glug")\nprint(bag)\n',
        choices=[
            "('rope', 'lamp', 'glug')",
            "ERROR: 'tuple' object has no attribute 'append'",
            "['rope', 'lamp', 'glug']",
        ],
        answer=1,
        explain=(
            "Round brackets made a tuple, and a tuple can't grow, so it has no `.append()`. For a list that grows, "
            "use square brackets: `[\"rope\", \"lamp\"]`."
        ),
    ),
    pair_talk="Pair talk: before step 2, tell your partner what `across` and `down` will hold. Then each of you checks on your own screen.",
    starter=CABIN_STARTER,
    checkpoints=[
        dict(
            id="make-a-tuple",
            text="Change `cabin` into a tuple: round brackets instead of square ones.",
            dictated=True,
            hints=[
                "Look at line 4. Square brackets make a list. Which brackets make a tuple?",
                "With other names: `door = (3, 8)` is a tuple. Same numbers, round brackets.",
                "Write `cabin = (12, 5)` on line 4.",
            ],
            checks=[CABIN_MADE],
            pass_line="Mar'tu: Twelve across, five down. It stays put, like the cabin.",
        ),
        dict(
            id="unpack-it",
            text="Unpack `cabin` into `across` and `down`, in one line.",
            dictated=False,
            hints=[
                "Look under task 2. Two names on the left, one tuple on the right. Python hands out the items in order.",
                "With other names: `row, seat = door` puts 3 in `row` and 8 in `seat`.",
                "Write `across, down = cabin` under task 2.",
            ],
            checks=[CABIN_UNPACKED],
            pass_line="Gearshift: Visor dims. Two names, two numbers. Clean.",
        ),
        dict(
            id="print-the-spot",
            text="Print `across`, then `down`.",
            dictated=True,
            hints=[
                "Look under task 3. Use the two names you just made, in one `print` with a comma between them.",
                "With other names: `print(row, seat)` shows `3 8`.",
                "Write `print(across, down)` under task 3.",
            ],
            checks=[CABIN_SHOWN],
            pass_line="Lucky: Twelve across. I could find that. Probably.",
        ),
    ],
    solution=CABIN_SOLUTION,
    partials=[_cabin(unpack=None, show=None), _cabin(show=None)],
    assemble=dict(
        lines=["cabin = (12, 5)", "across, down = cabin", "print(across, down)"],
        distractors=["cabin = [12, 5]", "across, down = 12, 5", "cabin = (12 5)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two seats, bolted down",
            text=(
                "```text\ncabin = (12, 5)\n         |   |\n    across   down\n```\n"
                "A tuple is a row of seats bolted to the floor. You can read who sits where. You can't add a seat."
            ),
        ),
        dict(
            angle="everyday",
            label="A street address",
            text=(
                "A street address is a house number, then a street. Always both, always in that order, and it "
                "doesn't change when you visit. That is a tuple's job."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `cabin = (12, 5)`: round brackets, a comma between.\n"
                "2. `across, down = cabin`: `across` takes item 0, `down` takes item 1.\n"
                "3. `print(across, down)` shows `12 5`."
            ),
        ),
        dict(
            angle="shorter",
            text="`( )` makes a tuple that can't change. `a, b = pair` unpacks it, in order.",
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="The far corner",
        text=(
            "Gearshift wants the spot one step further across. On a new line, print `across + 1`, then `down`."
        ),
        hints=["Add 1 to `across` only. `down` stays as it is.", "Write `print(across + 1, down)` at the bottom."],
        checks=[
            chk(
                "one step further across is printed",
                r'''
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    assert not _err, _stop(_vals, None, _err, 'Make it work for another spot too.')
    _c = _ns.get('cabin')
    _want = [_c[0] + 1, _c[1]]
    # one line or two: across + 1 somewhere, then down after it
    _got = _B.sum([_nums(_l) for _l in _plain(_rows)], [])
    _ok = [_i for _i, _x in _B.enumerate(_got) if _x == _want[0] and _want[1] in _got[_i + 1:]]
    assert _ok, 'Print `across + 1`, then `down`: `print(across + 1, down)`.' + _ev(_vals)
''',
                OTHER=CABIN_OTHER,
            )
        ],
        solution=CABIN_SOLUTION + "print(across + 1, down)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="map-of-tor",
        why=(
            "You looked at the map of Tor in the campaign. A spot on a map is always two numbers, in the same order. "
            "That fixed shape is a tuple's job."
        ),
    ),
    takeaway="`cabin = (12, 5)` is a tuple: read it like a list, but it can't change. `across, down = cabin` unpacks it.",
    wrong_answers=[
        dict(why="the starter (still a list: square brackets vs round ones)", code=CABIN_STARTER, fails_at=1,
             message_contains="still a list"),
        dict(why="no comma in the tuple", code=_cabin("cabin = (12 5)"), fails_at=0, message_contains="invalid syntax"),
        dict(why="(12) alone is a number", code=_cabin("cabin = (12)", unpack=None, show=None), fails_at=1,
             message_contains="comma"),
        dict(why="quoted numbers", code=_cabin('cabin = ("12", "5")'), fails_at=1, message_contains="quotes"),
        dict(why="the two numbers swapped", code=_cabin("cabin = (5, 12)"), fails_at=1, message_contains="Across comes first"),
        dict(why="the example's names copied (row, seat)", code=_cabin(unpack="row, seat = cabin", show="print(row, seat)"),
             fails_at=2, message_contains="from the example"),
        dict(why="the values typed by hand", code=_cabin(unpack="across, down = 12, 5"), fails_at=2,
             message_contains="typed by hand"),
        dict(why="one name takes the whole tuple", code=_cabin(unpack="across = cabin\ndown = cabin", show=None),
             fails_at=2, message_contains="whole tuple"),
        dict(why="the names the other way round", code=_cabin(unpack="down, across = cabin"), fails_at=2,
             message_contains="other way round"),
        dict(why="three names for two items", code=_cabin(unpack="across, down, up = cabin"), fails_at=0,
             message_contains="not enough values"),
        dict(why="read by position, counting from 1 (IndexError)",
             code=_cabin(unpack="across = cabin[1]\ndown = cabin[2]"), fails_at=0,
             message_contains="tuple index out of range"),
        dict(why="the numbers typed in the print", code=_cabin(show="print(12, 5)"), fails_at=3,
             message_contains="typed by hand"),
        dict(why="the whole tuple printed", code=_cabin(show="print(cabin)"), fails_at=3, message_contains="whole tuple"),
        dict(why="down printed first", code=_cabin(show="print(down, across)"), fails_at=3,
             message_contains="across first"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="tuple", solo="false", dictates="1,3",
             foreign_names="door,row,seat,bag") + "\n"
        "3-A1 try-it. CP1 [D] list -> tuple (the class's square-versus-round slip, both ways: the starter is a list, "
        "the predict shows `.append` on a tuple). CP2 [ND] unpacking, CMB with cabin = (30, 9), so `across, down = "
        "12, 5` fails; reading by index (`across = cabin[0]`) also passes. CP3 [D] the two numbers in order, CMB. "
        "LEFT: the example's `row`/`seat`. Bonus: arithmetic on an unpacked item."
    ),
)

TUPLES_ARTICLE = dict(
    kind="article",
    id="tuples",
    title="Tuples: Pairs That Stay Put",
    optional=True,
    minutes=10,
    summary="A tuple is a list that can't change: round brackets, read by position, and unpacked into names.",
    introduces=["node:Tuple"],
    body=(
        "Some things come in a fixed shape. A spot on the map of Tor is two numbers: across, then down. A hero's "
        "row is a name, then a mana number.\n"
        "For these, Python has the [[tuple]]. It is like a list, with round brackets instead of square ones:\n"
        "```python\nspot = (12, 5)\n```\n"
        "You read a tuple like a list. `spot[0]` is 12, `spot[-1]` is 5, and `len(spot)` is 2.\n"
        "But a tuple can't change. `spot[0] = 3` stops Python with a [[TypeError]]: a tuple *does not support item "
        "assignment*. And a tuple has no `.append()` at all.\n"
        "Why want a list you can't change? A tuple says: these belong together, in this order, and they stay put. "
        "Nobody changes one by mistake.\n"
        "Watch your brackets. `[48, 47]` is a list. `(48, 47)` is a tuple. If Python says a tuple *has no "
        "attribute 'append'*, you used round brackets where square ones belong.\n"
        "One more trick, called unpacking. Two names on the left take the items in order:\n"
        "```python\nname, mana = (\"Lucky\", 26)\n```\n"
        "Now `name` holds `\"Lucky\"` and `mana` holds 26."
    ),
    examples=[
        dict(code="spot = (12, 5)\nprint(spot[0])\nprint(spot[-1])\nprint(len(spot))\n", output="12\n5\n2"),
        dict(code='hero = ("Lucky", 26)\nname, mana = hero\nprint(name + " has " + str(mana))\n',
             output="Lucky has 26"),
        dict(code='roster = [\n    ("Oogrish", 18),\n    ("Lucky", 26),\n]\nprint(roster[1][0])\n', output="Lucky"),
    ],
    exercises=[CABIN_ON_THE_MAP],
    notes=(
        "meta: path=optional. 3-A1 (O, 10 min). Intro node:Tuple (optional-only token: no core item uses it). The "
        "errors are shown as words in the body (an example that crashes can't be verified). Reading a tuple by "
        "position and `len()` reuse u04a. The try-it is one exercise (3 checkpoints)."
    ),
)


# =============================================================================================
# Article 3-A2 "zip()" (optional, call:zip), with one try-it
# =============================================================================================

COLORS_STARTER = (
    'heroes = ["Oogrish", "Gearshift",\n'
    '          "Bomb Shell", "Lucky"]\n'
    'colors = ["gold", "fire orange",\n'
    '          "teal", "silver"]\n'
    "# 1. Zip them into pairs.\n"
    "pairs = []\n"
    "print(pairs)\n"
    "# 2. Print the last pair.\n"
    "\n"
)


def _colors(make="pairs = list(zip(heroes, colors))", last="print(pairs[-1])"):
    code = COLORS_STARTER.replace("pairs = []\n", make + "\n")
    if last is not None:
        code = code.replace("# 2. Print the last pair.\n\n", "# 2. Print the last pair.\n" + last + "\n")
    return code


COLORS_SOLUTION = _colors()
COLORS_OTHER = {"heroes": ["Pell", "Brakka", "Moss"], "colors": ["green", "grey", "red"]}
# The evidence bracket for this try-it names the other lists in words (both lists in code would be long).
COLORS_EV = " (Mar'tu's check tried 3 other heroes and colors, only inside the check.)"

PAIRS_MADE = chk(
    "pairs holds each hero with their color",
    r'''
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    assert not _miss, _keep(_miss[0] if _miss else 'heroes')
    _h, _c = _ns.get('heroes'), _ns.get('colors')
    _lists = _is_list(_h) and _is_list(_c)
    _p = _ns.get('pairs')
    if _lists and _p == _B.list(_B.zip(_h, _c)):
        continue
    assert not (_err and not _uses('call:zip')), ('Make the pairs with `zip()`: `list(zip(heroes, colors))`. It '
                                                 'pairs lists of any length, first with first.' + __EV__)
    assert not _err, _stop(None, None, _err) + __EV__
    assert 'pairs' in _ns, 'Keep the line `pairs = ` from the starter, and put `list(zip(heroes, colors))` after the `=`.'
    assert type(_p).__name__ != 'zip', ('Wrap it in `list()`: `list(zip(heroes, colors))`. On its own, `zip()` hands '
                                        'back a zip object, not pairs you can see.')
    assert _p != [], "`pairs` is still the starter's `[]`. Make it `list(zip(heroes, colors))`."
    assert not (_lists and _p == [_h, _c]), ('`[heroes, colors]` sets the two whole lists side by side. `zip()` makes '
                                             'pairs: the first hero with the first color, and so on.')
    assert not (_lists and _p == _B.list(_B.zip(_c, _h))), 'Heroes first, then colors: `zip(heroes, colors)`.'
    assert not (_lists and _p == _B.list(_B.zip(_h))), 'Hand `zip()` both lists, heroes first: `zip(heroes, colors)`.'
    assert not _typed_list('pairs'), (
        'Zip them from the lists: `list(zip(heroes, colors))`, so the pairs follow the lists. `pairs` holds pairs '
        'typed by hand.')
    assert _uses('call:zip'), ('Make the pairs with `zip()`: `list(zip(heroes, colors))`. It pairs lists of any '
                               'length, first with first.' + (__EV__ if _vals is not None else ''))
    assert not (_vals is not None and _p == globals().get('pairs')), (
        'Zip them from the lists: `list(zip(heroes, colors))`. `pairs` stayed the same: pairs typed by hand.'
        + (__EV__ if _vals is not None else ''))
    assert False, 'Make `pairs` with `list(zip(heroes, colors))`.' + (__EV__ if _vals is not None else '')
''',
    OTHER=COLORS_OTHER, EV=COLORS_EV,
)

LAST_PAIR = chk(
    "the last pair is printed",
    r'''
_own = [_l for _l in _lines() if not _l.startswith('[')]
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    _h, _c = _ns.get('heroes'), _ns.get('colors')
    _all = _B.list(_B.zip(_h, _c)) if _is_list(_h) and _is_list(_c) and _h and _c else [('', '')]
    _want, _first = _all[-1], _all[0]
    _p = [_l for _l in _rows if not _l.startswith('[')]
    if [_l for _l in _p if _want[0] in _l and _want[1] in _l]:
        continue
    assert not _err, _stop(None, None, _err) + __EV__
    assert not [_l for _l in _p if _first[0] in _l and _first[1] in _l], (
        'That is the first pair. The last one is at the end: count from the end, `pairs[-1]`.' + (__EV__ if _vals is not None else ''))
    assert not [_l for _l in _p if _want[0] in _l], 'Print the whole pair, hero and color: `pairs[-1]`.'
    assert not (_vals is not None and _p and _p == _own), (
        'Read it from `pairs`: `pairs[-1]`, so it follows the lists. Your line shows a pair typed by hand.' + (__EV__ if _vals is not None else ''))
    assert _p, ('Print one pair on its own, the last: `pairs[-1]`. Your program prints only lists, in square '
                'brackets.' + (__EV__ if _vals is not None else ''))
    assert False, 'Print the last pair in `pairs`: count from the end, `pairs[-1]`.' + (__EV__ if _vals is not None else '')
''',
    OTHER=COLORS_OTHER, EV=COLORS_EV,
)

SPELL_COLORS = dict(
    id="spell-colors",
    title="Spell colors",
    martu=(
        "Every hero's magic has a color. Oogrish's is gold. Gearshift's is fire orange. Two lists, kept in step, "
        "yes? The first hero goes with the first color.\n"
        "[[zip()]] pairs them up for you. Wrap it in `list()`, so you can see the pairs."
    ),
    example='coins = ["copper", "brass"]\nvalues = [1, 5]\nprint(list(zip(coins, values)))\n',
    example_output="[('copper', 1), ('brass', 5)]",
    introduces=["call:zip"],
    names=["heroes", "colors", "pairs"],
    predict=dict(
        q="One list is longer. Before you press Run: what will this print?",
        code='names = ["Pell", "Brakka"]\nhats = ["red", "blue", "green"]\nprint(list(zip(names, hats)))\n',
        choices=[
            "[('Pell', 'red'), ('Brakka', 'blue'), ('green',)]",
            "[['Pell', 'Brakka'], ['red', 'blue', 'green']]",
            "[('Pell', 'red'), ('Brakka', 'blue')]",
            "ERROR: the lists are not the same length",
        ],
        answer=2,
        explain=(
            "`zip()` makes pairs until the shorter list runs out. `\"green\"` has no partner, so it is left out. "
            "No error."
        ),
    ),
    pair_talk="Pair talk: before you run step 1, tell your partner what `pairs[0]` will be. Then each of you checks on your own screen.",
    starter=COLORS_STARTER,
    checkpoints=[
        dict(
            id="zip-them",
            text="Make `pairs` with `list(zip(heroes, colors))`.",
            dictated=True,
            hints=[
                "Look at the `pairs = []` line. `zip()` takes both lists, heroes first. `list()` around it turns "
                "the zip into pairs you can see.",
                "With other names: `list(zip(coins, values))` pairs each coin with its value.",
                "Write `pairs = list(zip(heroes, colors))` in place of `pairs = []`.",
            ],
            checks=[PAIRS_MADE],
            pass_line="Bomb Shell: Teal. Mine. Logged.",
        ),
        dict(
            id="last-pair",
            text="Print the last pair in `pairs`.",
            dictated=False,
            hints=[
                "Look under task 2. The last pair is at the end of `pairs`. Count from the end.",
                "With other names: `print(steps[-1])` shows the last item of `steps`, whatever its length.",
                "Write `print(pairs[-1])` under task 2.",
            ],
            checks=[LAST_PAIR],
            pass_line="Lucky: Silver. Obviously. It goes with the armor.",
        ),
    ],
    solution=COLORS_SOLUTION,
    partials=[_colors(last=None)],
    assemble=dict(
        lines=[line for line in COLORS_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=["pairs = zip(heroes, colors)", "pairs = [heroes, colors]", "print(pairs[4])"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A zipper",
            text=(
                "```text\nheroes  Oogrish  Gearshift ...\n           |        |\n"
                "colors  gold     fire orange ...\n```\n"
                "`zip()` joins the two sides tooth by tooth: the first with the first, the second with the second."
            ),
        ),
        dict(
            angle="everyday",
            label="Socks from the wash",
            text=(
                "Two piles from the wash: left socks and right socks, in the same order. You take one from each "
                "pile and roll them into a pair. `zip()` does that, pile by pile."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `zip(heroes, colors)` makes the pairs, but hides them.\n"
                "2. `list(...)` around it shows them: `[('Oogrish', 'gold'), ...]`.\n"
                "3. `pairs[-1]` is the last pair."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, Mar'tu's four replies sat in four boxes, and the game matched `\"option 1\"` to "
                "the first one. Two lists and a `zip()` do that matching."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky wants his color only. On a new line, print just the color from the last pair.",
        hints=["A pair is a tuple: the hero is `[0]`, the color is `[1]`.", "Write `print(pairs[-1][1])` at the bottom."],
        checks=[
            chk(
                "the last color is printed on its own",
                r'''
for _vals in (None, __OTHER__):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    assert not _err, _stop(_vals, None, _err)
    _want = _ns['colors'][_B.len(_ns['heroes']) - 1]
    assert [_l for _l in _plain(_rows) if _l.rstrip('.!') == _want], (
        'Print only the color from the last pair: `pairs[-1][1]`.' + _ev(_vals))
''',
                OTHER=COLORS_OTHER,
            )
        ],
        solution=COLORS_SOLUTION + "print(pairs[-1][1])\n",
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='option_1 = "We will help you."\noption_2 = "What is the decay?"',
        why=(
            "You wrote four replies in four boxes, `option_1` to `option_4`, and the game matched `\"option 1\"` to "
            "the first. As two lists, labels and replies, `zip()` would pair each label with its reply."
        ),
    ),
    takeaway="`list(zip(heroes, colors))` pairs two lists, first with first. `pairs[-1]` is the last pair.",
    wrong_answers=[
        dict(why="the starter (pairs is still [])", code=COLORS_STARTER, fails_at=1, message_contains="still the starter"),
        dict(why="no list(): a zip object", code=_colors("pairs = zip(heroes, colors)", last=None), fails_at=1,
             message_contains="Wrap it in `list()`"),
        dict(why="the two lists side by side", code=_colors("pairs = [heroes, colors]", last=None), fails_at=1,
             message_contains="side by side"),
        dict(why="colors first", code=_colors("pairs = list(zip(colors, heroes))", last=None), fails_at=1,
             message_contains="Heroes first"),
        dict(why="zip with one list", code=_colors("pairs = list(zip(heroes))", last=None), fails_at=1,
             message_contains="both lists"),
        dict(why="the pairs typed by hand",
             code=_colors('pairs = [("Oogrish", "gold"), ("Lucky", "silver")]', last=None), fails_at=1,
             message_contains="typed by hand"),
        dict(why="the example's names copied", code=_colors("pairs = list(zip(coins, values))", last=None), fails_at=0,
             message_contains="'coins' is not defined"),
        dict(why="the pairs read one by one: right for 4 heroes, not for 3 (no zip)",
             code=_colors("pairs = [\n    (heroes[0], colors[0]),\n    (heroes[1], colors[1]),\n"
                          "    (heroes[2], colors[2]),\n    (heroes[3], colors[3]),\n]", last=None),
             fails_at=1, message_contains="with `zip()`"),
        dict(why="square brackets for zip's round ones", code=_colors("pairs = list(zip[heroes, colors])", last=None),
             fails_at=0, message_contains="not subscriptable"),
        dict(why="the first pair (index from 0 read as the last)", code=_colors(last="print(pairs[0])"), fails_at=2,
             message_contains="first pair"),
        dict(why="a position from the start (3) only fits four heroes", code=_colors(last="print(pairs[3])"),
             fails_at=2, message_contains="[-1]"),
        dict(why="another pair from the middle", code=_colors(last="print(pairs[1])"), fails_at=2,
             message_contains="count from the end"),
        dict(why="a slice for one item ([-1:] is a list)", code=_colors(last="print(pairs[-1:])"), fails_at=2,
             message_contains="only lists"),
        dict(why="len used as a position (IndexError)", code=_colors(last="print(pairs[len(pairs)])"), fails_at=0,
             message_contains="out of range"),
        dict(why="the last pair typed by hand", code=_colors(last='print(("Lucky", "silver"))'), fails_at=2,
             message_contains="typed by hand"),
        dict(why="the hero without the color", code=_colors(last="print(pairs[-1][0])"), fails_at=2,
             message_contains="whole pair"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="zip,list-index", solo="false", dictates="1",
             foreign_names="coins,values,names,hats,steps") + "\n"
        "3-A2 try-it. CP1 [D] `list(zip(heroes, colors))`, CMB with three other heroes and colors, so a typed list "
        "fails; catches a bare zip object, `[heroes, colors]`, the order swapped, one list only. CP2 [ND] the last "
        "pair: the rerun has 3 pairs, so `pairs[3]` stops with an IndexError ('count from the end'); a line holding "
        "the hero and the color passes (`print(pairs[-1][0], pairs[-1][1])` too). Bonus: the color only, "
        "`pairs[-1][1]` (a tuple read by position)."
    ),
)

ZIP_ARTICLE = dict(
    kind="article",
    id="zip",
    title="zip(): Two Lists, Side by Side",
    optional=True,
    minutes=10,
    summary="Two lists kept in step, paired up item by item with `zip()`: first with first, second with second.",
    introduces=["call:zip"],
    body=(
        "Sometimes two lists go together, item by item:\n"
        "```python\nheroes = [\"Oogrish\", \"Lucky\"]\nmanas = [18, 26]\n```\n"
        "`heroes[0]` goes with `manas[0]`, and `heroes[1]` goes with `manas[1]`. Two lists kept in step like "
        "this are [[parallel lists]].\n"
        "[[zip()]] works like the zipper on a coat. It joins the two sides tooth by tooth: first with first, "
        "second with second. Each pair is a [[tuple]].\n"
        "```python\npairs = list(zip(heroes, manas))\n```\n"
        "Now `pairs` holds `[('Oogrish', 18), ('Lucky', 26)]`.\n"
        "Why the `list()`? On its own, `zip()` hands back a zipper nobody has pulled yet. Print it, and you see "
        "something like `<zip object at 0x7f3a...>`. `list()` pulls the zipper, and you get the pairs.\n"
        "If one list is shorter, `zip()` stops when it runs out. There is no error. The extra items are left out.\n"
        "You have seen this. In the campaign, Mar'tu's four replies sat in four boxes, `option_1` to `option_4`, "
        "and the game matched `\"option 1\"` to the first one. Two lists and a `zip()` do that matching."
    ),
    examples=[
        dict(
            code=(
                'heroes = ["Oogrish", "Lucky"]\nmanas = [18, 26]\npairs = list(zip(heroes, manas))\nprint(pairs)\n'
                "print(pairs[1])\n"
            ),
            output="[('Oogrish', 18), ('Lucky', 26)]\n('Lucky', 26)",
        ),
        dict(
            code='labels = ["option 1", "option 2"]\nlines = ["Help.", "Rest.", "Run!"]\nprint(list(zip(labels, lines)))\n',
            output="[('option 1', 'Help.'), ('option 2', 'Rest.')]",
        ),
    ],
    exercises=[SPELL_COLORS],
    notes=(
        "meta: path=optional. 3-A2 (O, 10 min). Intro call:zip (optional-only token). The zip object's address is "
        "random, so it is shown as words in the body, never in an example output (lint 9). Prerequisite for 3P2."
    ),
)


# =============================================================================================
# Project 3P2 "The Basement Inventory" (optional, 35 min)
# =============================================================================================

INV_STARTER = (
    "# Mar'tu's basement: the parts of\n"
    "# the resonance array. Two lists,\n"
    "# kept in step: counts[0] is how\n"
    "# many of parts[0] there are.\n"
    "\n"
    "# 1. parts: 4 or more part names.\n"
    "parts = []\n"
    "\n"
    "# 2. counts: one whole number for\n"
    "#    each part, in the same order.\n"
    "counts = []\n"
    "\n"
    "# 3. A new part turned up. Put it\n"
    "#    second in parts, and its count\n"
    "#    second in counts.\n"
    "\n"
    "# 4. Lucky borrowed the last part.\n"
    "#    Pop it off both lists. Keep\n"
    "#    its name in borrowed.\n"
    "\n"
    "# 5. top_three: the 3 biggest\n"
    "#    counts, from a sorted copy.\n"
    "top_three = []\n"
    "print(top_three)\n"
    "\n"
    "# 6. Print how many parts are\n"
    "#    used up: a count of 0.\n"
    "\n"
    "# 7. Zip the lists into pairs.\n"
    "inventory = []\n"
    "print(inventory)\n"
)

INV_PARTS = (
    "parts = [\n"
    '    "brass lens",\n'
    '    "tuning fork",\n'
    '    "copper coil",\n'
    '    "glass bell",\n'
    "]\n"
)
INV_COUNTS = "counts = [3, 0, 7, 5]\n"
INV_INSERT = 'parts.insert(1, "ley needle")\ncounts.insert(1, 2)\n'
INV_POP = "borrowed = parts.pop()\ncounts.pop()\n"
INV_TOP = "top_three = sorted(counts)[-3:]\n"
INV_ZEROS = "print(counts.count(0))\n"
INV_ZIP = "inventory = list(zip(parts, counts))\n"


def _inv(parts=None, counts=None, insert=None, pop=None, top=None, zeros=None, zipped=None, extra=""):
    """The project program with any of its parts filled in (None = the starter's)."""
    code = INV_STARTER
    if parts is not None:
        code = code.replace("parts = []\n", parts)
    if counts is not None:
        code = code.replace("counts = []\n", counts)
    if insert is not None:
        code = code.replace("#    second in counts.\n", "#    second in counts.\n" + insert)
    if pop is not None:
        code = code.replace("#    its name in borrowed.\n", "#    its name in borrowed.\n" + pop)
    if top is not None:
        code = code.replace("top_three = []\n", top)
    if zeros is not None:
        code = code.replace("#    used up: a count of 0.\n", "#    used up: a count of 0.\n" + zeros)
    if zipped is not None:
        code = code.replace("inventory = []\n", zipped)
    return code + extra


INV_SOLUTION = _inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS, INV_ZIP)

# The other lists Mar'tu's check tries (invented parts; counts chosen so the slips give different answers:
# the last count of B is its biggest, so a top three taken before the pop fails, and an unsorted slice never
# matches).
INV_A = {"parts": ["lens", "fork", "coil", "bell", "dial"], "counts": [4, 0, 11, 0, 8]}
INV_B = {"parts": ["gear", "pipe", "wire", "plate"], "counts": [9, 1, 0, 13]}
INV_CASES = [None, INV_A, INV_B]

# Shared by tasks 3 to 7: the original lists of a case (the student's own literals, or the rerun's) and the lists
# as they stood right after task 3's inserts (None until both inserts happened).
_INV_CASE = r'''
_WATCH = ('parts', 'counts')
def _orig(_vals):
    if _vals is not None:
        return _vals['parts'], _vals['counts']
    return _first_lit('parts')[1], _first_lit('counts')[1]
def _inserted(_snaps, _P, _C):
    _ip = [_s['parts'] for _s in _snaps if _ins_at(_s['parts'], _P) == 1]
    _ic = [_s['counts'] for _s in _snaps if _ins_at(_s['counts'], _C) == 1]
    return (_ip[0] if _ip else None), (_ic[0] if _ic else None)
def _seen_list(_snaps, _name, _want):
    return _want is not None and any(_s[_name] == _want for _s in _snaps)
def _inv_stop(_vals, _err, _only=None):
    if _err.startswith('ValueError') and _calls_of('remove'):
        return ('Use `.pop()`, which takes the last part, whatever its name. With other parts, `.remove()` stopped '
                'Python with a ValueError.' + _ev(_vals, None, ('parts',)))
    return _stop(_vals, None, _err, 'Make it work for other lists too.', _only)
'''


def inv_chk(label, body, **subs):
    return chk(label, _INV_CASE + body, CASES=INV_CASES, **subs)


INV_PARTS_MADE = chk(
    "parts is a list of 4 or more part names",
    r'''
_kind, _v = _first_lit('parts')
assert not ('tools' in globals() and (_kind == 'missing' or not _v)), (
    '`tools` is the name from the hint. This task' + chr(39) + 's list is `parts`: put your part names in `parts = []`.')
assert _kind != 'missing', 'Keep the line `parts = []` from the starter, and put your part names inside its square brackets.'
assert _kind != 'Tuple', ('Use square brackets for the list: `parts = [ ... ]`. Round brackets make a tuple, and a '
                          'tuple can' + chr(39) + 't grow.')
assert _is_list(_v), 'Make `parts` a list: part names between square brackets, like `["lens", "coil"]`.'
assert _v, '`parts` is still empty. Put 4 or more part names between the square brackets, each in quotes.'
for _x in _v:
    _k = type(_x).__name__
    assert _k not in ('list', 'tuple'), 'Keep only names in `parts`, like `"lens"`. The counts get their own list in task 2.'
    assert _k != 'int', '`parts` holds names, each in quotes. The numbers go in `counts`, in task 2.'
    assert _k == 'str' and _x.strip(), 'Put each part' + chr(39) + 's name in quotes, like `"brass lens"`.'
assert _B.len(_v) >= 4, 'Put at least 4 parts in `parts`. It has ' + _B.str(_B.len(_v)) + '.'
''',
)

INV_COUNTS_MADE = chk(
    "counts holds one whole number for each part",
    r'''
_kind, _v = _first_lit('counts')
_pk, _pv = _first_lit('parts')
assert not ('stock' in globals() and (_kind == 'missing' or not _v)), (
    '`stock` is the name from the hint. This task' + chr(39) + 's list is `counts`: put your numbers in `counts = []`.')
assert _kind != 'missing', 'Keep the line `counts = []` from the starter, and put your numbers inside its square brackets.'
assert _kind != 'Tuple', 'Use square brackets for the list: `counts = [ ... ]`. Round brackets make a tuple.'
assert _is_list(_v), 'Make `counts` a list: whole numbers between square brackets, like `[3, 0, 7]`.'
assert _v, '`counts` is still empty. Put one whole number in it for each part, in the same order.'
_txt = [_x for _x in _v if type(_x).__name__ == 'str']
assert not _txt, 'Take the quotes off the counts. With quotes they are text, and counts are numbers, like `3`.'
assert _B.all([_is_int(_x) for _x in _v]), 'Make each count a whole number, like `3`.'
_n = _B.len(_pv) if _is_list(_pv) else 0
assert _B.len(_v) == _n, ('Give each part one count: `parts` has ' + _B.str(_n) + ' names, but `counts` has '
                          + _B.str(_B.len(_v)) + ' numbers.')
''',
)

INV_INSERTED = inv_chk(
    "a new part and its count are second in both lists",
    r'''
_body = _ast.parse(_source).body
def _set_at(_name):
    return [_n for _n in _body if type(_n).__name__ == 'Assign' and type(_n.targets[0]).__name__ == 'Subscript'
            and type(_n.targets[0].value).__name__ == 'Name' and _n.targets[0].value.id == _name]
_swapped = [_n for _n in _calls_of('insert') if _B.len(_n.args) == 2 and type(_n.args[1]).__name__ == 'Constant'
            and _n.args[1].value == 1 and not (type(_n.args[0]).__name__ == 'Constant' and _n.args[0].value == 1)]
def _where(_k, _name, _demo):
    if _k == 2:
        return ('Positions start at 0: second place is position 1. Use `' + _name + '.insert(1, ' + _demo
                + ')`.')
    if _k == 0:
        return 'Position 0 is the first place. The new one goes second: `' + _name + '.insert(1, ' + _demo + ')`.'
    return ('Put it second, at position 1: `' + _name + '.insert(1, ' + _demo + ')`. It went in at position '
            + _B.str(_k) + '.')
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _miss, _keep(_miss[0] if _miss else 'parts')
    _P, _C = _orig(_vals)
    if not (_is_list(_P) and _is_list(_C)):
        assert False, 'Finish tasks 1 and 2 first: `parts` and `counts`, each a list.'
    _kp = [_ins_at(_s['parts'], _P) for _s in _snaps]
    _kc = [_ins_at(_s['counts'], _C) for _s in _snaps]
    _okp = [_s['parts'][1] for _s, _k in _B.zip(_snaps, _kp) if _k == 1 and type(_s['parts'][1]).__name__ == 'str']
    _okc = [_s['counts'][1] for _s, _k in _B.zip(_snaps, _kc) if _k == 1 and _is_int(_s['counts'][1])]
    _grow_p = _B.max([_B.len(_s['parts']) for _s in _snaps if _is_list(_s['parts'])] + [0]) - _B.len(_P)
    _grow_c = _B.max([_B.len(_s['counts']) for _s in _snaps if _is_list(_s['counts'])] + [0]) - _B.len(_C)
    if _okp and _okc and _grow_p <= 1 and _grow_c <= 1:
        continue
    assert not _err, _inv_stop(_vals, _err)
    assert _grow_p <= 1, ('Put in one new part, once: `parts.insert(1, ...)`. `parts` grew by ' + _B.str(_grow_p)
                          + '.' + _ev(_vals, None, ('parts',)))
    assert _grow_c <= 1, ('Put in one new count, once: `counts.insert(1, ...)`. `counts` grew by ' + _B.str(_grow_c)
                          + '.' + _ev(_vals, None, ('counts',)))
    def _pop_first(_name):
        _i = [_n.lineno for _n in _calls_of('insert', _name)]
        _p = [_n.lineno for _n in _calls_of('pop', _name)]
        return _i and _p and _B.min(_p) < _B.min(_i)
    if not _okp:
        _ev_p = _ev(_vals, None, ('parts',))
        assert not _set_at('parts'), ('Use `parts.insert(1, ...)`, which squeezes the new part in. `parts[1] = ...` '
                                      'swapped out a part instead.')
        assert not (_calls_of('append', 'parts') and not _calls_of('insert', 'parts')), (
            'Use `parts.insert(1, ...)`: `.append()` adds at the end, and the new part goes second.')
        assert not _pop_first('parts'), ('Do task 3 before task 4: insert first, then pop. Lines run top to bottom, '
                                         'so your pop ran before your insert.')
        _ks = [_k for _k in _kp if _k >= 0]
        if _ks:
            _new = [_s['parts'][_k] for _s, _k in _B.zip(_snaps, _kp) if _k >= 0][0]
            assert type(_new).__name__ == 'str', 'Put the new part' + chr(39) + 's name in quotes, like `"ley needle"`.'
            assert False, _where(_ks[0], 'parts', '"ley needle"') + _ev_p
        assert False, ('Put a new part second in `parts` with `.insert()`: `parts.insert(1, "ley needle")`, or a part '
                       'of your own.' + _ev_p)
    _ev_c = _ev(_vals, None, ('counts',))
    assert not _set_at('counts'), ('Use `counts.insert(1, ...)`, which squeezes the new count in. `counts[1] = ...` '
                                   'swapped out a count instead.')
    assert not [_n for _n in _swapped if type(_n.func.value).__name__ == 'Name' and _n.func.value.id == 'counts'], (
        'Position first, then the value: `counts.insert(1, 2)` puts 2 at position 1.')
    assert not (_calls_of('append', 'counts') and not _calls_of('insert', 'counts')), (
        'Use `counts.insert(1, ...)`: `.append()` adds at the end, and the new count goes second, next to its part.')
    assert not _pop_first('counts'), ('Do task 3 before task 4: insert first, then pop. Lines run top to bottom, '
                                      'so your pop ran before your insert.')
    _ks = [_k for _k in _kc if _k >= 0]
    if _ks:
        _new = [_s['counts'][_k] for _s, _k in _B.zip(_snaps, _kc) if _k >= 0][0]
        assert type(_new).__name__ != 'str', 'Take the quotes off the new count. Counts are numbers.'
        assert _is_int(_new), 'Make the new count a whole number, like `2`.'
        assert False, _where(_ks[0], 'counts', '2') + _ev_c
    assert False, ('Insert its count too: `counts.insert(1, 2)`, so each count stays in step with its part.' + _ev_c)
''',
)

INV_POPPED = inv_chk(
    "the last part and its count are popped off, and borrowed holds the part",
    r'''
_own_b = globals().get('borrowed')
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _miss, _keep(_miss[0] if _miss else 'parts')
    _P, _C = _orig(_vals)
    _IP, _IC = _inserted(_snaps, _P, _C)
    assert _IP is not None and _IC is not None, 'Finish task 3 first: the new part and its count, second in both lists.'
    # Seen right after the pop, and still one shorter at the end (a second pop would hide behind the first).
    _fp, _fcn = _ns.get('parts'), _ns.get('counts')
    _okp = _seen_list(_snaps, 'parts', _IP[:-1]) and _is_list(_fp) and _B.len(_fp) == _B.len(_IP) - 1
    _okc = _seen_list(_snaps, 'counts', _IC[:-1]) and _is_list(_fcn) and _B.len(_fcn) == _B.len(_IC) - 1
    _b = _ns.get('borrowed')
    if _okp and _okc and _b == _IP[-1]:
        continue
    assert not _err, _inv_stop(_vals, _err)
    _evp = _ev(_vals, None, ('parts',))
    assert not _seen_list(_snaps, 'parts', _IP[1:]), ('Leave the brackets empty: `parts.pop()` takes the last part. '
                                                      '`.pop(0)` took the first.' + _evp)
    assert not _B.callable(_b), 'Add `()` after `.pop`: `parts.pop()`. Without them, nothing is popped.'
    if not _okp:
        assert not _seen_list(_snaps, 'parts', _IP[:-2]), ('Pop once. Two parts came off `parts`, so it no longer '
                                                           'lines up with `counts`.' + _evp)
        assert not _seen_list(_snaps, 'parts', _IP[:-1]), ('Pop once, then leave `parts` alone: it should end one '
                                                           'part shorter than after task 3.' + _evp)
        assert not (_b == _IP[-1]), ('Use `.pop()`: it reads the last part *and* takes it off. `parts[-1]` only reads '
                                     'it.' + _evp)
        assert not _calls_of('pop', 'parts'), 'Pop the last part off `parts` itself: `borrowed = parts.pop()`.' + _evp
        assert False, 'Take the last part off `parts` and keep it: `borrowed = parts.pop()`.' + _evp
    if not _okc:
        _evc = _ev(_vals, None, ('counts',))
        assert not _seen_list(_snaps, 'counts', _IC[1:]), ('Leave the brackets empty: `counts.pop()` takes the last '
                                                           'count. `.pop(0)` took the first.' + _evc)
        assert not _seen_list(_snaps, 'counts', _IC[:-2]), ('Pop once. Two counts came off `counts`, so it no longer '
                                                            'lines up with `parts`.' + _evc)
        assert not _seen_list(_snaps, 'counts', _IC[:-1]), ('Pop once, then leave `counts` alone: it should end one '
                                                            'count shorter than after task 3.' + _evc)
        assert False, 'Pop `counts` too: `counts.pop()`, so each count stays in step with its part.' + _evc
    assert not ('taken' in _ns and 'borrowed' not in _ns), ('`taken` is the name from the hint. This task keeps the '
                                                            'part in `borrowed`: `borrowed = parts.pop()`.')
    assert 'borrowed' in _ns, 'Keep what `.pop()` hands back: `borrowed = parts.pop()`.'
    assert not _B.callable(_b), 'Add `()` after `.pop`: `parts.pop()`. Without them, nothing is popped.'
    assert not _is_int(_b), '`borrowed` holds a count. Keep the part' + chr(39) + 's name: `borrowed = parts.pop()`.'
    assert not (_vals is not None and _b == _own_b), ('Keep what `.pop()` hands back: `borrowed = parts.pop()`. '
                                                     '`borrowed` stayed the same: a part typed by hand.' + _evp)
    assert False, 'Keep the popped part in `borrowed`: `borrowed = parts.pop()`.' + _evp
''',
)

INV_TOPPED = inv_chk(
    "top_three holds the 3 biggest counts, and counts keeps its order",
    r'''
_own_t = globals().get('top_three')
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _miss, _keep(_miss[0] if _miss else 'counts')
    _P, _C = _orig(_vals)
    _IP, _IC = _inserted(_snaps, _P, _C)
    assert _IC is not None, 'Finish tasks 3 and 4 first.'
    _PC = _IC[:-1]
    _E = _B.sorted(_PC)[-3:]
    _t = _ns.get('top_three')
    _fc = _ns.get('counts')
    if _is_list(_t) and _B.len(_t) == 3 and _same_items(_t, _E) and _fc == _PC:
        continue
    assert not _err, _inv_stop(_vals, _err, ('counts',))
    _evc = _ev(_vals, None, ('counts',))
    assert 'top_three' in _ns, 'Keep the line `top_three = ` from the starter, and build it after the `=`.'
    assert type(_t).__name__ != 'NoneType', ('Use `sorted(counts)`: `.sort()` hands back `None`, so `top_three` '
                                             'holds `None`.')
    if _fc != _PC:
        _alias = [_n.targets[0].id for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign'
                  and _B.len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                  and type(_n.value).__name__ == 'Name' and _n.value.id == 'counts' and _n.targets[0].id != 'counts']
        _sorted_alias = [_a for _a in _alias if _calls_of('sort', _a)]
        # The student's own name is never echoed back (2.11): the message names the pattern instead.
        assert not _sorted_alias, ('A second name for `counts`, like `copy = counts`, is still the same list, so '
                                   'sorting one sorts both. Use `sorted(counts)`: a real copy.' + _evc)
        assert _fc != _B.sorted(_PC), ('Sort a copy: `sorted(counts)`. `.sort()` sorted `counts` itself, so the counts '
                                       'no longer line up with their parts.' + _evc)
        assert False, 'Leave `counts` as it was after task 4. Only `top_three` should change.' + _evc
    assert _t != [], "`top_three` is still the starter's `[]`. Make it `sorted(counts)[-3:]`."
    assert not _is_int(_t), 'That is one count. A slice has a colon: `sorted(counts)[-3:]`.' + _evc
    assert _is_list(_t), 'Make `top_three` a list: `sorted(counts)[-3:]`.'
    assert _t != _B.sorted(_PC)[:3], ('Those are the 3 smallest. A sorted copy has the biggest at the end: '
                                      '`sorted(counts)[-3:]`.' + _evc)
    assert _t != _B.sorted(_PC)[-3:-1], ('Leave the end empty: `[-3:]`. A slice stops *before* its end number, so '
                                         '`[-3:-1]` leaves out the biggest.' + _evc)
    assert not _same_items(_t, _PC[-3:]), ('Sort first, then slice: `sorted(counts)[-3:]`. The last 3 counts are not '
                                           'always the biggest.' + _evc)
    assert _t != _B.sorted(_PC), 'Slice off the last 3: `sorted(counts)[-3:]`. `top_three` holds every count.'
    assert not (_vals is not None and _t == _own_t), ('Build it from `counts`: `sorted(counts)[-3:]`. `top_three` '
                                                     'stayed ' + _shn(_t, 'the same') + ', typed by hand.' + _evc)
    assert False, 'Make `top_three` the 3 biggest counts: `sorted(counts)[-3:]`. It holds ' + _shn(_t) + '.' + _evc
''',
)

INV_ZEROS_SAID = inv_chk(
    "the number of 0 counts is printed, read from counts",
    r'''
_quoted = [_n for _n in _calls_of('count') if _n.args and type(_n.args[0]).__name__ == 'Constant'
           and type(_n.args[0].value).__name__ == 'str']
assert not _quoted, 'Take the quotes off: `"0"` is text, and `counts` holds numbers. Use `counts.count(0)`.'
_own = _lastnums(_lines())
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _miss, _keep(_miss[0] if _miss else 'counts')
    _fc = _ns.get('counts')
    _want = _fc.count(0) if _is_list(_fc) else -1
    _got = _lastnums(_rows)
    if _want in _got:
        continue
    assert not _err, _inv_stop(_vals, _err, ('counts',))
    _evc = _ev(_vals, None, ('counts',))
    assert not _calls_of('count', 'parts'), 'Count in `counts`: the numbers live there. `parts` holds names, so it has no 0s.'
    assert _got, 'Print how many counts are 0: `print(counts.count(0))`.'
    assert not (_is_list(_fc) and _B.len(_fc) in _got), ('Use `.count(0)`: `len()` counts every part, and `.count(0)` '
                                                       'counts only the 0s.' + _evc)
    assert not (_vals is not None and _got == _own), ('Count with `counts.count(0)`, so it follows the list. Your line '
                                                     'shows ' + _B.str(_got[-1]) + ', a number typed by hand.' + _evc)
    assert False, ('Print how many parts are used up: `counts.count(0)`. With these lists it is ' + _B.str(_want) + '.'
                   + _evc)
''',
)

INV_ZIPPED = inv_chk(
    "inventory pairs each part with its count",
    r'''
_own_i = globals().get('inventory')
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _miss, _keep(_miss[0] if _miss else 'parts')
    _fp, _fc = _ns.get('parts'), _ns.get('counts')
    _lists = _is_list(_fp) and _is_list(_fc)
    _i = _ns.get('inventory')
    if _lists and _i == _B.list(_B.zip(_fp, _fc)):
        continue
    assert not _err, _inv_stop(_vals, _err)
    assert 'inventory' in _ns, 'Keep the line `inventory = ` from the starter, and put `list(zip(parts, counts))` after the `=`.'
    assert type(_i).__name__ != 'zip', ('Wrap it in `list()`: `list(zip(parts, counts))`. On its own, `zip()` hands '
                                        'back a zip object, not the pairs.')
    assert _i != [], "`inventory` is still the starter's `[]`. Make it `list(zip(parts, counts))`."
    assert not (_lists and _i == [_fp, _fc]), ('`[parts, counts]` sets the two whole lists side by side. `zip()` makes '
                                               'pairs: each part with its count.')
    assert not (_lists and _i == _B.list(_B.zip(_fc, _fp))), 'Parts first, then counts: `zip(parts, counts)`.'
    assert not (_lists and _i == _B.list(_B.zip(_fp))), 'Hand `zip()` both lists: `zip(parts, counts)`.'
    _early = [_s for _s in _snaps if _is_list(_s['parts']) and _is_list(_s['counts'])
              and _i == _B.list(_B.zip(_s['parts'], _s['counts']))]
    assert not _early, ('Make `inventory` at the bottom, after the insert and the pop, so it pairs the lists as they '
                        'end up.' + _ev(_vals))
    assert not _typed_list('inventory'), (
        'Zip it from the lists: `list(zip(parts, counts))`, so the pairs follow them. `inventory` holds pairs typed '
        'by hand.')
    assert _uses('call:zip'), ('Make the pairs with `zip()`: `list(zip(parts, counts))`. It pairs every part with its '
                               'count, however many parts there are.' + _ev(_vals, None, ('parts',)))
    assert not (_vals is not None and _i == _own_i), ('Zip it from the lists: `list(zip(parts, counts))`. `inventory` '
                                                     'stayed the same: pairs typed by hand.' + _ev(_vals))
    assert False, 'Make `inventory` with `list(zip(parts, counts))`.' + _ev(_vals)
''',
)

INV_BONUS = inv_chk(
    "the total of every count is printed",
    r'''
for _vals in __CASES__:
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, _WATCH)
    assert not _err, _inv_stop(_vals, _err, ('counts',))
    _fc = _ns.get('counts')
    _want = _B.sum(_fc) if _is_list(_fc) else -1
    assert _want in _lastnums(_rows), ('Print the total of every count: `print(sum(counts))`, at the bottom.'
                                       + _ev(_vals, None, ('counts',)))
''',
)

INV_PICK = (
    "# Mar'tu's picks, ready to copy:\n"
    "# \"brass lens\", \"tuning fork\",\n"
    "# \"copper coil\", \"glass bell\"\n"
    "# counts: 3, 0, 7, 5\n"
    "# new part: \"ley needle\", 2"
)

PROJECT_3P2 = dict(
    kind="project",
    id="the-basement-inventory",
    title="The Basement Inventory",
    optional=True,
    minutes=35,
    summary="Keep the resonance array's parts in two lists that stay in step: insert, pop, sort a copy, count and zip.",
    intro=(
        "Under the trap door, Mar'tu's basement is full of brass. These are the parts of the resonance array, "
        "hauled back from the Institute. Bomb Shell keeps the inventory.\n"
        "Two [[parallel lists|lists kept in step]]: `parts` holds the names, and `counts` holds how many of each. "
        "`counts[0]` goes with `parts[0]`. Whatever you do to one list, do to the other.\n"
        "Seven tasks, in order. The comments in the editor mark each one. Any parts you like.\n"
        "Before this: the lesson More List Tools (insert and pop), How many times? in Extra practice (`.count()`), "
        "and the zip() article."
    ),
    martu=(
        "Two lists, one inventory. If the lists slip out of step, the lens gets the coil's count. Then my array "
        "lies to me, yes?\n"
        "My check tries other lists, with other parts. So read everything from the lists, and never type a number "
        "you can see."
    ),
    names=["parts", "counts", "borrowed", "top_three", "inventory"],
    pick=INV_PICK,
    pair_talk=(
        "Pair talk: before task 5, tell your partner why `counts.sort()` would break the inventory, but "
        "`sorted(counts)` would not. Then each of you types it on your own screen."
    ),
    starter=INV_STARTER,
    checkpoints=[
        dict(
            id="list-the-parts",
            text="1. Make `parts` a list of 4 or more part names, each in quotes.",
            dictated=False,
            hints=[
                "Look at task 1. Put the names between the square brackets, each in quotes, with a comma between "
                "them.",
                "A list of names with other names: `tools = [\"saw\", \"rope\", \"lamp\", \"pick\"]`.",
                "Write `parts = [\"brass lens\", \"tuning fork\", \"copper coil\", \"glass bell\"]`, or your own parts.",
            ],
            checks=[INV_PARTS_MADE],
            pass_line="Bomb Shell: Parts. Listed.",
        ),
        dict(
            id="count-each-part",
            text="2. Make `counts`: one whole number for each part, in the same order.",
            dictated=False,
            hints=[
                "Look at task 2. `counts[0]` is how many of `parts[0]` there are. One number per part, no quotes.",
                "With other names: `tools` has 4 names, so `stock = [2, 0, 5, 1]` has 4 numbers.",
                "Write `counts = [3, 0, 7, 5]`, one number for each of your parts.",
            ],
            checks=[INV_COUNTS_MADE],
            pass_line="Gearshift: Visor dims. Two lists, same length. In step.",
        ),
        dict(
            id="insert-a-new-part",
            text="3. A new part turned up. Put it second in `parts`, and its count second in `counts`.",
            dictated=False,
            hints=[
                "Look at task 3. `.insert()` takes the position first, then the value. Second place is position 1, "
                "because positions start at 0. Do it to both lists.",
                "With other names: `tools.insert(1, \"hook\")` and `stock.insert(1, 4)` keep the two lists in step.",
                "Write `parts.insert(1, \"ley needle\")`, then `counts.insert(1, 2)`.",
            ],
            checks=[INV_INSERTED],
            pass_line="Lucky: A new part. Is it worth anything?",
        ),
        dict(
            id="pop-the-last-part",
            text="4. Lucky borrowed the last part. Pop it off both lists, and keep its name in `borrowed`.",
            dictated=False,
            hints=[
                "Look at task 4. `.pop()` with empty brackets takes the last item off and hands it back. Pop "
                "`counts` too, or the lists slip out of step.",
                "With other names: `taken = tools.pop()` and `stock.pop()` take the last tool and its number.",
                "Write `borrowed = parts.pop()`, then `counts.pop()`.",
            ],
            checks=[INV_POPPED],
            pass_line="Bomb Shell: Borrowed. Noted. Lucky.",
        ),
        dict(
            id="top-three",
            text="5. Make `top_three` the 3 biggest counts, from a sorted copy of `counts`.",
            dictated=False,
            hints=[
                "Look at task 5. `sorted(counts)` is a copy, smallest first, so the biggest 3 are at the end. "
                "Slice them off with a colon.",
                "With other names: `sorted(stock)[-2:]` is the 2 biggest numbers in `stock`, and `stock` keeps its "
                "order.",
                "Write `top_three = sorted(counts)[-3:]` in place of `top_three = []`.",
            ],
            checks=[INV_TOPPED],
            pass_line="Gearshift: The counts still line up. Copy sorted, list untouched.",
        ),
        dict(
            id="used-up",
            text="6. Print how many parts are used up: how many counts are 0. Use `.count()`.",
            dictated=False,
            hints=[
                "Look at task 6. `.count(0)` counts how many items in the list are 0. Ask `counts`, where the numbers "
                "live.",
                "With other names: `stock.count(5)` counts how many 5s `stock` holds.",
                "Write `print(counts.count(0))` under task 6.",
            ],
            checks=[INV_ZEROS_SAID],
            pass_line="Mar'tu: Used up. I will add it to the list of things to fetch. Another list, yes?",
        ),
        dict(
            id="zip-the-inventory",
            text="7. Make `inventory` with `zip()`, so each part sits with its count.",
            dictated=False,
            hints=[
                "Look at task 7. `zip()` takes both lists, parts first. Wrap it in `list()` so you can see the "
                "pairs.",
                "With other names: `list(zip(tools, stock))` gives `[(\"saw\", 2), (\"rope\", 0), ...]`.",
                "Write `inventory = list(zip(parts, counts))` in place of `inventory = []`.",
            ],
            checks=[INV_ZIPPED],
            pass_line="Mar'tu: Every part with its count. The array may stop lying to me. Good work.",
        ),
    ],
    solution=INV_SOLUTION,
    partials=[
        _inv(INV_PARTS),
        _inv(INV_PARTS, INV_COUNTS),
        _inv(INV_PARTS, INV_COUNTS, INV_INSERT),
        _inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP),
        _inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP),
        _inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS),
    ],
    assemble=dict(
        lines=[line for line in INV_SOLUTION.splitlines() if line.strip() and not line.lstrip().startswith("#")],
        distractors=[
            "parts.insert(2, \"ley needle\")",
            "top_three = counts.sort()",
            "inventory = zip(parts, counts)",
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two shelves, in step",
            text=(
                "```text\n         0      1      2\nparts  lens   fork   coil\ncounts    3      0      7\n```\n"
                "Position 0 on one shelf goes with position 0 on the other. Insert on one shelf, insert on the other."
            ),
        ),
        dict(
            angle="everyday",
            label="A shopping list with amounts",
            text=(
                "A list of things to buy, and next to it how many of each. Cross out the eggs, and you must cross "
                "out the 12 too. Otherwise the milk gets the eggs' number."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `parts = [...]` and `counts = [...]`, same length.\n"
                "2. `.insert(1, ...)` into both.\n"
                "3. `borrowed = parts.pop()`, then `counts.pop()`.\n"
                "4. `sorted(counts)[-3:]`: a copy, so `counts` stays in step.\n"
                "5. `counts.count(0)`.\n"
                "6. `list(zip(parts, counts))`."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, `party.members` held the four of you, in order. The party panel showed each "
                "member's mana bar in that same order: two things kept in step."
            ),
        ),
    ],
    bonus=dict(
        by="bomb-shell",
        title="Bomb Shell's tally",
        text="Bomb Shell wants the total. At the bottom, print how many parts there are in all: every count added up.",
        hints=["`sum()` adds up every number in a list.", "Write `print(sum(counts))` at the bottom."],
        checks=[INV_BONUS],
        solution=INV_SOLUTION + "print(sum(counts))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="the-resonance-array",
        why=(
            "Bomb Shell and Lucky spent two weeks in this basement, hunched over Mar'tu's brass instruments. This "
            "time you keep the list of what is down there."
        ),
    ),
    takeaway=(
        "Parallel lists: do the same to both. `.insert(1, x)` puts x second, `.pop()` takes the last, `sorted()` "
        "copies, `zip()` pairs."
    ),
    wrong_answers=[
        dict(why="the starter (empty lists)", code=INV_STARTER, fails_at=1, message_contains="still empty"),
        dict(why="a part with no quotes, one item of a list over several lines (SyntaxError)",
             code=_inv(INV_PARTS.replace('"tuning fork"', "tuning fork")), fails_at=0,
             message_contains="Perhaps you forgot a comma"),
        dict(why="parts in round brackets (square brackets vs parentheses)",
             code=_inv('parts = ("lens", "fork", "coil", "bell")\n'), fails_at=1, message_contains="square brackets"),
        dict(why="pairs instead of names (3P1's shape)", code=_inv('parts = [["lens", 3], ["fork", 0]]\n'), fails_at=1,
             message_contains="only names"),
        dict(why="numbers in parts", code=_inv('parts = ["lens", 3, "fork", 0]\n'), fails_at=1,
             message_contains="each in quotes"),
        dict(why="only three parts", code=_inv('parts = ["lens", "fork", "coil"]\n'), fails_at=1,
             message_contains="at least 4"),
        dict(why="counts in quotes (numbers vs text)", code=_inv(INV_PARTS, 'counts = ["3", "0", "7", "5"]\n'),
             fails_at=2, message_contains="quotes off"),
        dict(why="a count missing (lists out of step)", code=_inv(INV_PARTS, "counts = [3, 0, 7]\n"), fails_at=2,
             message_contains="one count"),
        dict(why="inserted third (index from 1)",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(2, "ley needle")\ncounts.insert(2, 2)\n'), fails_at=3,
             message_contains="Positions start at 0"),
        dict(why="inserted first", code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(0, "ley needle")\ncounts.insert(0, 2)\n'),
             fails_at=3, message_contains="Position 0"),
        dict(why="the part inserted, its count forgotten (lists out of step)",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(1, "ley needle")\n'), fails_at=3,
             message_contains="Insert its count too"),
        dict(why="append for insert", code=_inv(INV_PARTS, INV_COUNTS, 'parts.append("ley needle")\ncounts.append(2)\n'),
             fails_at=3, message_contains="adds at the end"),
        dict(why="assigned over the second item instead of inserting",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts[1] = "ley needle"\ncounts[1] = 2\n'), fails_at=3,
             message_contains="swapped out"),
        dict(why="insert's value and position swapped",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(1, "ley needle")\ncounts.insert(2, 1)\n'), fails_at=3,
             message_contains="Position first"),
        dict(why="the new count in quotes",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(1, "ley needle")\ncounts.insert(1, "2")\n'), fails_at=3,
             message_contains="quotes off"),
        dict(why="the new part typed into the list, no insert",
             code=_inv('parts = ["brass lens", "ley needle", "tuning fork", "copper coil", "glass bell"]\n',
                       "counts = [3, 2, 0, 7, 5]\n"), fails_at=3, message_contains=".insert()"),
        dict(why="the first part popped", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT,
                                                    "borrowed = parts.pop(0)\ncounts.pop(0)\n"),
             fails_at=4, message_contains="`.pop(0)` took the first"),
        dict(why="the last part read, not popped", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT,
                                                             "borrowed = parts[-1]\ncounts.pop()\n"),
             fails_at=4, message_contains="only reads"),
        dict(why="counts not popped (lists out of step)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "borrowed = parts.pop()\n"), fails_at=4,
             message_contains="Pop `counts` too"),
        dict(why="len used as a position (IndexError)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "borrowed = parts.pop(len(parts))\ncounts.pop()\n"),
             fails_at=0, message_contains="pop index out of range"),
        dict(why="the popped part not kept", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "parts.pop()\ncounts.pop()\n"),
             fails_at=4, message_contains="Keep what `.pop()` hands back"),
        dict(why=".pop with no ()", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "borrowed = parts.pop\ncounts.pop()\n"),
             fails_at=4, message_contains="Add `()`"),
        dict(why="the borrowed part typed by hand, removed by name",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT,
                       'borrowed = "glass bell"\nparts.remove("glass bell")\ncounts.pop()\n'), fails_at=4,
             message_contains="`.remove()` stopped"),
        dict(why="x = x.sort(): None", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = counts.sort()\n"),
             fails_at=5, message_contains="`None`"),
        dict(why="a second name for counts, then sorted (changing the original through the copy)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP,
                       "biggest = counts\nbiggest.sort()\ntop_three = biggest[-3:]\n"),
             fails_at=5, message_contains="second name"),
        dict(why="sorted the original, not a copy (the counts slip out of step)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "counts.sort()\ntop_three = counts[-3:]\n"),
             fails_at=5, message_contains="no longer line up"),
        dict(why="the 3 smallest", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = sorted(counts)[:3]\n"),
             fails_at=5, message_contains="smallest"),
        dict(why="the slice end left out ([-3:-1])",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = sorted(counts)[-3:-1]\n"), fails_at=5,
             message_contains="*before*"),
        dict(why="sliced without sorting", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = counts[-3:]\n"),
             fails_at=5, message_contains="Sort first"),
        dict(why="the top three typed by hand", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = [2, 3, 7]\n"),
             fails_at=5, message_contains="typed by hand"),
        dict(why="one count, not a slice", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, "top_three = sorted(counts)[-3]\n"),
             fails_at=5, message_contains="one count"),
        dict(why="the used-up count typed by hand",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, "print(1)\n"), fails_at=6,
             message_contains="typed by hand"),
        dict(why="0 in quotes", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, 'print(counts.count("0"))\n'),
             fails_at=6, message_contains="quotes off"),
        dict(why="len counts every part", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, "print(len(counts))\n"),
             fails_at=6, message_contains="len()"),
        dict(why="parts asked instead of counts",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, "print(parts.count(0))\n"), fails_at=6,
             message_contains="Count in `counts`"),
        dict(why="square brackets for count's round ones",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, "print(counts.count[0])\n"), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="no list(): a zip object", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS,
                                                      "inventory = zip(parts, counts)\n"),
             fails_at=7, message_contains="Wrap it in `list()`"),
        dict(why="the two lists side by side", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS,
                                                         "inventory = [parts, counts]\n"),
             fails_at=7, message_contains="side by side"),
        dict(why="counts first", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS,
                                           "inventory = list(zip(counts, parts))\n"),
             fails_at=7, message_contains="Parts first"),
        dict(why="the pairs typed by hand",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS,
                       'inventory = [("brass lens", 3), ("ley needle", 2)]\n'), fails_at=7,
             message_contains="typed by hand"),
        dict(why="zipped before the insert and pop (top to bottom)",
             code=_inv(INV_PARTS, INV_COUNTS + "inventory = list(zip(parts, counts))\n", INV_INSERT, INV_POP, INV_TOP,
                       INV_ZEROS, ""),
             fails_at=7, message_contains="at the bottom"),
        dict(why="the pairs read one by one: right for 4 parts, not for 5 (no zip)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, INV_POP, INV_TOP, INV_ZEROS,
                       "inventory = [\n    (parts[0], counts[0]),\n    (parts[1], counts[1]),\n"
                       "    (parts[2], counts[2]),\n    (parts[3], counts[3]),\n]\n"),
             fails_at=7, message_contains="with `zip()`"),
        dict(why="parts popped twice (zip would hide it: the lists slip out of step)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "borrowed = parts.pop()\nparts.pop()\ncounts.pop()\n", INV_TOP,
                       INV_ZEROS, INV_ZIP),
             fails_at=4, message_contains="Pop once"),
        dict(why="a pop to throw away, then a pop to keep (two pops)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "parts.pop()\nborrowed = parts.pop()\ncounts.pop()\n"),
             fails_at=4, message_contains="Pop once"),
        dict(why="counts popped twice", code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT,
                                                  "borrowed = parts.pop()\ncounts.pop()\ncounts.pop()\n", INV_TOP),
             fails_at=4, message_contains="Pop once"),
        dict(why="two new parts inserted",
             code=_inv(INV_PARTS, INV_COUNTS, 'parts.insert(1, "ley needle")\nparts.insert(1, "ley needle")\n'
                       "counts.insert(1, 2)\n"),
             fails_at=3, message_contains="once"),
        dict(why="task 4 written above task 3 (popped before the insert)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_POP + INV_INSERT), fails_at=3, message_contains="insert first"),
        dict(why="the hint's name copied (tools)", code=_inv('tools = ["saw", "rope", "lamp", "pick"]\n'), fails_at=1,
             message_contains="name from the hint"),
        dict(why="the hint's name copied (stock)", code=_inv(INV_PARTS, "stock = [2, 0, 5, 1]\n"), fails_at=2,
             message_contains="name from the hint"),
        dict(why="the hint's name copied (taken)",
             code=_inv(INV_PARTS, INV_COUNTS, INV_INSERT, "taken = parts.pop()\ncounts.pop()\n"), fails_at=4,
             message_contains="name from the hint"),
    ],
    notes=(
        meta(starter_level="S2", path="optional", skills="list-make,insert-pop,range-slice-sort,count,zip,"
             "list-index", solo="false", dictates="", foreign_names="tools,stock,taken") + "\n"
        "Project 3P2 (O, 35 min; prerequisites 3C, 4X 3B-04 and 3-A2, named in the intro). Task comments are in "
        "the starter (S2); `parts = []`, `counts = []`, `top_three = []` and `inventory = []` are placeholders, "
        "so the program always runs. Tasks 1-2 read the student's own literals (any parts, any counts: lint e). "
        "Tasks 3-7 rerun the program with two other pairs of lists (5 and 4 parts) and read snapshots of `parts` "
        "and `counts` taken after every top-level line, so each task is judged on the lists right after its own "
        "lines: a later `counts.sort()` is task 5's message, not task 3's. The inserted part and count are the "
        "student's own (creative) and stay put in the reruns; one insert per list (two inserts, or an append left "
        "beside the insert, get 'once'), and an insert below the pop gets 'insert first, then pop'. Task 4 checks "
        "both lists lost their last item and end exactly one item shorter than after task 3 (a second pop would "
        "otherwise hide behind the first, and zip() in task 7 would hide the slip), and that `borrowed` is the "
        "part (a typed name, `.remove()` by name, `[-1]` read-only, `.pop(0)`, counts not popped). Task 5: the 3 "
        "biggest of the post-pop counts in any order, and `counts` unchanged (the in-place `.sort()` breaks the "
        "parallel lists: a copy versus the original; `biggest = counts` then `biggest.sort()` gets 'second "
        "name'). Rerun B's last count (13) is its biggest, so a top three taken before the pop fails. Task 6 "
        "reads the last number of each printed line that is not a list. Task 7 `list(zip(parts, counts))` of the "
        "final lists; a zip made above the insert is caught by the snapshots, and pairs read one by one (right "
        "for 4 parts, not 5) get 'with zip()'. Hint names (`tools`, `stock`, `taken`) get their own message. "
        "Side quest (Bomb Shell): `sum(counts)`. Partials 1-6 pass tasks 1..k."
    ),
)


# =============================================================================================
# Challenge "One List, Same Answer" (optional, advanced, about 10 min): seven boxes become one list
# =============================================================================================

REFACTOR_STARTER = (
    "hour_1 = 48\n"
    "hour_2 = 48\n"
    "hour_3 = 47\n"
    "hour_4 = 46\n"
    "hour_5 = 44\n"
    "hour_6 = 41\n"
    "hour_7 = 37\n"
    'print("Oldest gap:", hour_1)\n'
    'print("Newest gap:", hour_7)\n'
    'print("Shrink:", 11)\n'
)
REFACTOR_READS = "oldest = chalk_wall[0]\nnewest = chalk_wall[-1]\n"
REFACTOR_PRINTS = 'print("Oldest gap:", oldest)\nprint("Newest gap:", newest)\nprint("Shrink:", oldest - newest)\n'


def _refactor(wall=WALL_LINE, reads=REFACTOR_READS, prints=REFACTOR_PRINTS, boxes=""):
    """The rewritten program (each part replaceable for wrong answers). `boxes`: lines kept from the starter."""
    return boxes + wall + reads + prints


REFACTOR_SOLUTION = _refactor()
REFACTOR_WANT = ["Oldest gap: 48", "Newest gap: 37", "Shrink: 11"]
# Another wall, 5 gaps: `[1]` reads 58, a counted `[6]` stops with an IndexError, and the shrink is 14, not 11.
REFACTOR_OTHER = [60, 58, 55, 51, 46]
REFACTOR_EV = " (Mar'tu's check tried the wall `[60, 58, 55, 51, 46]`, only inside the check.)"

REFACTOR_ONE_LIST = chk(
    "the hour_ boxes are gone, and chalk_wall holds the seven gaps",
    r'''
_made = _made_names()
_hours = [_m for _m in _made if _m.startswith('hour_')]
assert not _hours, ('The `hour_` boxes are still there. This task keeps all seven gaps in one list, `chalk_wall`, '
                    'and reads every number from it.')
_kind, _v = _first_lit('chalk_wall')
if _kind == 'missing':
    _n = _near('chalk_wall')
    assert not _n, 'Python matches names letter for letter: you wrote `' + _n[0] + '`, the task needs `chalk_wall`.'
    assert 'nights' not in _made, ('`nights` is the name from the example. This task' + chr(39) + 's list is '
                                   '`chalk_wall`.')
    assert False, 'Make one list called `chalk_wall` for the seven gaps, oldest first.'
assert _kind != 'Tuple', 'Round brackets make a tuple. A list has square brackets.'
assert _is_list(_v), '`chalk_wall` should be a list: the seven gaps between square brackets, with commas.'
assert not [_x for _x in _v if type(_x).__name__ == 'str'], ('The gaps have quotes, so they are text. Gaps are '
                                                            'numbers, with no quotes.')
assert _v == __WALL__, ('`chalk_wall` should hold the seven gaps the boxes held, oldest first. It holds '
                        + _shn(_v) + '.')
''',
    WALL=WALL,
)

REFACTOR_SAME = chk(
    "it prints the same three lines as the seven-box program",
    r'''
_got = _lines()
_at = 0
for _w in __WANT__:
    _hit = [_i for _i in _B.range(_at, _B.len(_got)) if _got[_i] == _w]
    if _hit:
        _at = _hit[0] + 1
        continue
    assert _w not in _got, 'Keep the three lines in the old order: the oldest gap, the newest gap, then the shrink.'
    _label = _w.split(':')[0] + ':'
    _same = [_l for _l in _got if _l.startswith(_label)]
    if _same:
        _n = _nums(_same[0])
        _shown = _B.str(_n[-1]) if _n else 'something else'
        assert _shown != '-11', ('The shrink shows -11: the take-away runs the wrong way round. The oldest gap '
                                 'comes first.')
        assert False, ('The `' + _label + '` line shows ' + _shown + '. The seven-box program showed `' + _w + '`.')
    assert False, ('The seven-box program printed `' + _w + '`. Yours has no line like it: keep the words the '
                   'same, and read the number from the list.')
''',
    WANT=REFACTOR_WANT,
)

REFACTOR_FOLLOWS = chk(
    "the three lines follow another wall",
    r'''
_o = __OTHER__
_ns, _rows, _err, _miss, _seen, _snaps = _rerun({'chalk_wall': _o})
assert not _miss, ("Keep one `chalk_wall = [...]` line with the seven gaps, so Mar'tu's check can try "
                   "another wall there.")
_want = ['Oldest gap: ' + _B.str(_o[0]), 'Newest gap: ' + _B.str(_o[-1]), 'Shrink: ' + _B.str(_o[0] - _o[-1])]
if not _B.all([_w in _rows for _w in _want]):
    assert not _err.startswith('IndexError'), ('With another wall, Python stopped: ' + _err + '. A position counted '
                                               'for 7 gaps does not fit a shorter wall. Count from the end for the '
                                               'newest.' + __EV__)
    assert not _err, 'With another wall, Python stopped: ' + _err + '.' + __EV__
    def _shown(_label):
        _l = [_x for _x in _rows if _x.startswith(_label)]
        _n = _nums(_l[0]) if _l else []
        return _n[-1] if _n else None
    _a, _b, _c = _shown('Oldest gap:'), _shown('Newest gap:'), _shown('Shrink:')
    if _a != _o[0]:
        assert _a != 48, 'The oldest gap is typed, not read from `chalk_wall`, so it shows 48 on any wall.' + __EV__
        assert _a != _o[1], 'Positions start at 0, so that read the second gap, not the oldest.' + __EV__
        assert False, ('The oldest gap does not follow the wall: it shows ' + _B.str(_a) + ', not '
                       + _B.str(_o[0]) + '.' + __EV__)
    if _b != _o[-1]:
        assert _b != 37, 'The newest gap is typed, not read from `chalk_wall`, so it shows 37 on any wall.' + __EV__
        assert False, ('The newest gap does not follow the wall: it shows ' + _B.str(_b) + ', not '
                       + _B.str(_o[-1]) + '. Count from the end, so it fits a wall of any length.' + __EV__)
    assert _c != 11, ('The shrink is still a typed number, so it shows 11 on another wall too. Let the code work '
                      'it out from the oldest and newest gaps.' + __EV__)
    assert _c != _o[1] - _o[-1], 'Positions start at 0, so the shrink starts from the second gap.' + __EV__
    assert False, ('The shrink does not follow the wall: it shows ' + _B.str(_c) + ', not '
                   + _B.str(_o[0] - _o[-1]) + '. It is the oldest gap take away the newest.' + __EV__)
''',
    OTHER=REFACTOR_OTHER, EV=REFACTOR_EV,
)

REFACTOR_BONUS = chk(
    "the newest drop is printed, and it follows another wall",
    r'''
for _vals in (None, {'chalk_wall': __OTHER__}):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    _w = _ns.get('chalk_wall')
    _want = 'Last drop: ' + _B.str(_w[-2] - _w[-1]) if _is_list(_w) and _B.len(_w) > 1 else '?'
    _ev_w = '' if _vals is None else __EV__
    assert not _err, 'With another wall, Python stopped: ' + _err + '.' + _ev_w
    assert _want in _rows, ('Print `Last drop:` and the newest gap take away the one before it, both read from '
                            '`chalk_wall`.' + _ev_w)
''',
    OTHER=REFACTOR_OTHER, EV=REFACTOR_EV,
)

CHALLENGE_ONE_LIST = dict(
    kind="challenge",
    id="one-list-same-answer",
    title="One List, Same Answer",
    level="advanced",
    optional=True,
    minutes=10,
    support="light",
    summary=(
        "A stretch: rewrite a seven-box program with one list, so it prints the same thing and works out the "
        "shrink itself."
    ),
    martu=(
        "Before you knew lists, my wall lived in seven boxes. The program works. But the shrink is typed by hand, "
        "so one new gap and it lies, yes?\n"
        "Rewrite it with one list. Same three lines, word for word. My check also tries another wall, only inside "
        "the check, so read every number from the list."
    ),
    example=(
        "nights = [9, 8, 6]\nfirst = nights[0]\nlast = nights[-1]\n"
        'print("First:", first)\nprint("Drop:", first - last)\n'
    ),
    example_output="First: 9\nDrop: 3",
    names=["chalk_wall"],
    pair_talk=(
        "Pair talk: before you start, tell your partner which box holds the oldest gap and which holds the newest, "
        "and how a list reads each one. Then each of you rewrites it on your own screen."
    ),
    starter=REFACTOR_STARTER,
    checkpoints=[
        dict(
            id="rewrite-with-one-list",
            text=(
                "Rewrite it with one list, `chalk_wall`, so it prints the same thing, and let the code work out "
                "the shrink."
            ),
            dictated=False,
            hints=[
                "Look at the seven `hour_` lines: their numbers, oldest first, go into one list. Then look at each "
                "print: which position of the list does it need?",
                "With other names: in the example, `nights[0]` is the first item, `nights[-1]` the last, and "
                "`first - last` is how much it dropped.",
                "The shrink is the oldest gap take away the newest. Read both from `chalk_wall`, so a new wall "
                "gets a new shrink.",
                "Write `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` in place of the seven hour lines. Then read the oldest and the newest gap from it, and print the shrink as one take away the other.",
            ],
            checks=[REFACTOR_ONE_LIST, REFACTOR_SAME, REFACTOR_FOLLOWS],
            pass_line=(
                "Mar'tu: Same three lines, one list. Chalk a new gap, and the shrink keeps up. That is why we have "
                "lists, yes?"
            ),
        ),
    ],
    solution=REFACTOR_SOLUTION,
    assemble=dict(
        lines=[line for line in REFACTOR_SOLUTION.splitlines() if line.strip()],
        distractors=['print("Shrink:", 11)', "newest = chalk_wall[7]", "oldest = chalk_wall[1]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Seven boxes, one list",
            text=(
                "```text\nhour_1 ... hour_7\n  48  ...   37\n\nchalk_wall[0] ... [-1]\n  48   ...   37\n```\n"
                "`hour_1` becomes `chalk_wall[0]`. `hour_7` becomes `chalk_wall[-1]`, the newest on a wall of any "
                "length."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Put the seven numbers in `chalk_wall`, oldest first.\n"
                "2. Delete the seven `hour_` lines.\n"
                "3. Each print reads from the list: the oldest at `[0]`, the newest at `[-1]`.\n"
                "4. The shrink is the oldest take away the newest, worked out from those two reads."
            ),
        ),
        dict(
            angle="everyday",
            label="One page, not seven scraps",
            text=(
                "Seven scraps of paper, one number each, and the total written on a scrap by hand. Add a scrap, and "
                "the total is wrong. Write the numbers on one page, and work the total out from the page."
            ),
        ),
    ],
    bonus=dict(
        by="bomb-shell",
        title="The newest drop",
        text=(
            "Bomb Shell wants the newest drop. At the bottom, print `Last drop:` and how much the newest gap "
            "shrank from the one before it."
        ),
        hints=["The one before the newest is `[-2]`. Take the newest away from it.",
               "Write `drop = chalk_wall[-2] - newest` at the bottom, then `print(\"Last drop:\", drop)`."],
        checks=[REFACTOR_BONUS],
        solution=REFACTOR_SOLUTION + 'drop = chalk_wall[-2] - newest\nprint("Last drop:", drop)\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "You have seen this wall. Oogrish ran a finger down it, and the newest number, 37, was circled twice. "
            "One list holds the whole wall, so every read and the shrink keep up when a new gap is chalked."
        ),
    ),
    takeaway=(
        "One list for seven boxes: `[0]` is the oldest, `[-1]` the newest, and the code works out the shrink, so "
        "it keeps up with a new wall."
    ),
    wrong_answers=[
        dict(why="the starter (seven boxes, the shrink typed)", code=REFACTOR_STARTER, fails_at=1,
             message_contains="still there"),
        dict(why="the list added, the hour_ boxes kept", code=_refactor(boxes=REFACTOR_STARTER.split("print(")[0]),
             fails_at=1, message_contains="still there"),
        dict(why="the example's list name copied (nights)",
             code=_refactor("nights = [48, 48, 47, 46, 44, 41, 37]\n", "oldest = nights[0]\nnewest = nights[-1]\n"),
             fails_at=1, message_contains="from the example"),
        dict(why="a near-miss list name", code=_refactor(WALL_LINE.replace("chalk_wall", "chalk_wal"),
                                                         REFACTOR_READS.replace("chalk_wall", "chalk_wal")),
             fails_at=1, message_contains="letter for letter"),
        dict(why="round brackets (square brackets vs parentheses for a list)",
             code=_refactor("chalk_wall = (48, 48, 47, 46, 44, 41, 37)\n"), fails_at=1, message_contains="tuple"),
        dict(why="a gap missing from the list", code=_refactor("chalk_wall = [48, 48, 47, 46, 44, 37]\n"),
             fails_at=1, message_contains="seven gaps"),
        dict(why="quoted numbers (the shrink crashes on text)",
             code=_refactor('chalk_wall = ["48", "48", "47", "46", "44", "41", "37"]\n'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="missing commas", code=_refactor("chalk_wall = [48 48 47 46 44 41 37]\n"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the shrink still typed by hand (print(11))",
             code=_refactor(prints='print("Oldest gap:", oldest)\nprint("Newest gap:", newest)\nprint("Shrink:", 11)\n'),
             fails_at=1, message_contains="still a typed number"),
        dict(why="the shrink worked out from typed numbers (48 - 37)",
             code=_refactor(prints='print("Oldest gap:", oldest)\nprint("Newest gap:", newest)\n'
                                   'print("Shrink:", 48 - 37)\n'),
             fails_at=1, message_contains="still a typed number"),
        dict(why="the shrink the wrong way round (newest - oldest)",
             code=_refactor(prints='print("Oldest gap:", oldest)\nprint("Newest gap:", newest)\n'
                                   'print("Shrink:", newest - oldest)\n'),
             fails_at=1, message_contains="wrong way round"),
        dict(why="the oldest typed by hand (print(48), not chalk_wall[0])",
             code=_refactor(reads="oldest = 48\nnewest = chalk_wall[-1]\n"), fails_at=1, message_contains="typed"),
        dict(why="index from 1: the oldest read with [1] (right here only because the first two gaps are both 48)",
             code=_refactor(reads="oldest = chalk_wall[1]\nnewest = chalk_wall[-1]\n"), fails_at=1,
             message_contains="Positions start at 0"),
        dict(why="index from 1: the newest read with [7] (IndexError)",
             code=_refactor(reads="oldest = chalk_wall[0]\nnewest = chalk_wall[7]\n"), fails_at=0,
             message_contains="out of range"),
        dict(why="len used as a position (IndexError)",
             code=_refactor(reads="oldest = chalk_wall[0]\nnewest = chalk_wall[len(chalk_wall)]\n"), fails_at=0,
             message_contains="out of range"),
        dict(why="the newest counted from the front ([6] fits 7 gaps only)",
             code=_refactor(reads="oldest = chalk_wall[0]\nnewest = chalk_wall[6]\n"), fails_at=1,
             message_contains="counted for 7 gaps"),
        dict(why="a label reworded", code=_refactor(prints='print("Oldest:", oldest)\nprint("Newest gap:", newest)\n'
                                                           'print("Shrink:", oldest - newest)\n'),
             fails_at=1, message_contains="no line like it"),
        dict(why="the lines out of order", code=_refactor(prints='print("Newest gap:", newest)\n'
                                                                 'print("Oldest gap:", oldest)\n'
                                                                 'print("Shrink:", oldest - newest)\n'),
             fails_at=1, message_contains="old order"),
    ],
    notes=(
        meta(starter_level="S3", path="optional", skills="list-make,list-index", solo="false", dictates="",
             foreign_names="nights") + "\n"
        "Optional advanced challenge for the ready-to-stretch group (teacher ruling on the Unit 4 reviews: costs "
        "no one any core time). A refactor of 3A-01's seven boxes (`hour_1` to `hour_7`), whose shrink is typed by "
        "hand (`print(\"Shrink:\", 11)`). One goal-only checkpoint, three checks: no `hour_` names left and "
        "`chalk_wall` the seven gaps (a near-miss name, the example's `nights`, round brackets, a gap missing); "
        "the same three lines on the student's own run, word for word and in order (extra lines are allowed, so "
        "the bonus never turns it red); then a rerun with the 5-gap wall [60, 58, 55, 51, 46], so a typed shrink "
        "(11 or `48 - 37`), a typed gap, `[1]` for the oldest (48 = 48 on the real wall) and a counted `[6]` "
        "(IndexError) all fail. Core tools only: `[0]`, `[-1]` and subtraction; the solution names the two reads "
        "(`oldest`, `newest`) so every line fits a phone (36 characters). Side quest (Bomb Shell): the newest drop, "
        "`[-2]` take away the newest, checked on the rerun wall too."
    ),
)


# =============================================================================================
# Quick Check 3 (test-out). Forms A and B: three code tasks each, plus two questions each.
# Teacher ruling on the Unit 4 reviews: a true fast path. C1 adds a fix by position (objective 3), C2 is the
# recipe `newest_three` (objective 5, a recipe that takes a list, and a slice), Q2 is `range` + `+`. Every
# message is lean (Unit 2 ruling): it names the slip and keeps the evidence bracket, but never the line to type.
# =============================================================================================


def _qc_meta(skills, dictates, foreign="", form="A"):
    return meta(starter_level="S3", path="QC3", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# Assigns to `name[...]` (a change by position), and `name[...] == ...` questions (a change that changes nothing).
_SUBS = r'''
_tree3 = _ast.parse(_source)
_subs = [_n for _n in _ast.walk(_tree3) if type(_n).__name__ == 'Assign'
         and _B.any([type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name'
                     and _t.value.id == __NAME__ for _t in _n.targets])]
_eqs = [_n for _n in _ast.walk(_tree3) if type(_n).__name__ == 'Compare' and type(_n.left).__name__ == 'Subscript'
        and type(_n.left.value).__name__ == 'Name' and _n.left.value.id == __NAME__
        and _B.any([type(_o).__name__ == 'Eq' for _o in _n.ops])]
'''


# ---- C1: make a list, append a guess, fix one item by position, print the last item through the list ----

def _qc_make(form, name, start, rule, guess, fix, other, other_guess, story="", lead="", copied="three marks",
             lesson="Many Values, One Name"):
    """rule = ("below", 41) or ("above", 7): the guess the task asks for (any value on that side passes).
    fix: the right value at position 1 (Lucky miscopied start[1]). story / lead: form B's starter comment and
    Mar'tu's opening line."""
    side, edge = rule
    nums = ", ".join(str(x) for x in start[:-1]) + " and " + str(start[-1])
    old = start[1]
    fixed = start[:1] + [fix] + start[2:]

    def program(make=f"{name} = {start!r}", app=f"{name}.append({guess})", mend=f"{name}[1] = {fix}",
                show=f"print({name}[-1])"):
        return (
            story
            + f"# 1. Make {name}: {nums}.\n"
            + (make + "\n" if make else f"{name} = []\n")
            + "# 2. Append your guess.\n"
            + (app + "\n" if app else "\n")
            + f"# 3. Fix the {old} by position.\n"
            + (mend + "\n" if mend else "\n")
            + "# 4. Print its last item,\n"
            "#    read from the list.\n"
            + (show + "\n" if show else "\n")
        )

    starter = program(make=None, app=None, mend=None, show=None)
    # The guess is the smallest item (below) or the biggest (above), so min() / max() would find it in the own run.
    extreme = "min" if side == "below" else "max"
    ok_rule = f"_g[-1] {'<' if side == 'below' else '>'} {edge}"
    made = chk(
        f"{name} starts as {nums}",
        r'''
_kind, _v = _first_lit(__NAME__)
assert not ('steps' in globals() and (_kind == 'missing' or not _v)), (
    '`steps` is a name from a hint. This task' + chr(39) + 's list is `' + __NAME__ + '`.')
assert _kind != 'missing', _lost(__NAME__)
assert _kind != 'Tuple', 'Round brackets make a tuple, not a list.'
assert _is_list(_v), '`' + __NAME__ + '` is not a list.'
assert _v or not _near(__NAME__), _lost(__NAME__)
assert _v, '`' + __NAME__ + '` is still empty.'
_txt = [_x for _x in _v if type(_x).__name__ == 'str']
assert not _txt, 'The numbers have quotes, so they are text.'
# Lucky's fixed copy is let through here, so a retyped first line gets task 3's message, not this one.
_fine = (__WANT__, __FIXED__)
assert not (_v[:3] in _fine and _B.len(_v) > 3), 'The guess is typed into the first list, so nothing is appended.'
assert _v in _fine, '`' + __NAME__ + '` holds ' + _shn(_v) + ', not ' + __NUMS__ + ' in that order.'
''',
        NAME=name, NUMS=nums, WANT=start, FIXED=fixed,
    )
    appended = chk(
        "your guess is appended",
        r'''
_body = _ast.parse(_source).body
_lits = [_n for _n in _assigns(__NAME__) if type(_n.value).__name__ == 'List']
_bare = [_n for _n in _body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp'
         and type(_n.value.op).__name__ == 'Add']
_early = [_n for _n in _calls_of('append', __NAME__) if _lits and _n.lineno < _lits[-1].lineno]
def _mask(_l):
    # position 1 left out: task 3 changes it, and this task's check must stay true after that
    return [_x for _i, _x in _B.enumerate(_l) if _i != 1]
for _vals in (None, {__NAME__: __OTHER__}):
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, None, (__NAME__,))
    assert not _miss, _lost(__NAME__)
    _start = __WANT__ if _vals is None else _vals[__NAME__]
    # The list right after the first line that changes its length, once it holds the start: a later line (task
    # 3's fix, a slip in task 3) can't hide or fake the append.
    _hist = [_s[__NAME__] for _s in _snaps]
    _began = [_i for _i, _h in _B.enumerate(_hist) if _is_list(_h) and _B.len(_h) == _B.len(_start)
              and _mask(_h) == _mask(_start)]
    _grown = None
    for _h in (_hist[_began[0]:] if _began else []):
        if not (_is_list(_h) and _B.len(_h) == _B.len(_start)):
            _grown = _h
            break
    _g = _grown if _grown is not None else _ns.get(__NAME__)
    _ok = (_is_list(_g) and _B.len(_g) == _B.len(_start) + 1 and _mask(_g[:-1]) == _mask(_start)
           and _is_int(_g[-1]))
    if _ok and (_vals is not None or (__OKRULE__)):
        continue
    assert not _ok, 'Your guess, ' + _B.str(_g[-1]) + ', is not ' + __SIDE__ + ' ' + _B.str(__EDGE__) + '.'
    assert not _err, _lstop(_vals, None, _err)
    if _is_list(_g) and _B.len(_g) == _B.len(_start):
        assert not _bare, '`+` makes a new, longer list, and that line throws it away.'
        assert not _early, ('The append is above the line that makes `' + __NAME__ + '`, and lines run top to '
                            'bottom.')
        assert _B.len(_lits) < 2, 'A second `' + __NAME__ + ' = [...]` line makes a brand-new list.' + _ev(_vals)
        assert False, 'Nothing was added to the end of `' + __NAME__ + '`.' + _ev(_vals)
    assert _is_list(_g), '`' + __NAME__ + '` is no longer a list.'
    assert _B.len(_g) == _B.len(_start) + 1, ('`' + __NAME__ + '` grew by ' + _B.str(_B.len(_g) - _B.len(_start))
                                              + ', not by one guess.' + _ev(_vals))
    _new = _g[-1]
    assert type(_new).__name__ != 'str', 'The guess has quotes, so it is text, not a number.'
    assert type(_new).__name__ != 'list', 'The guess went in with square brackets, so a whole list was appended.'
    assert False, 'The new last item of `' + __NAME__ + '` is not one whole number.' + _ev(_vals)
''',
        NAME=name, WANT=start, OTHER=other[:len(start)], OKRULE=ok_rule, SIDE=side, EDGE=edge,
    )
    # __OKRULE__ is an expression, not a value: put it back unquoted.
    appended = (appended[0], appended[1].replace(repr(ok_rule), ok_rule))
    fix_value = chk(
        f"position 1 now holds {fix}",
        _SUBS + r'''
_g = globals().get(__NAME__)
_want = __FIXED__
if not (_is_list(_g) and _B.len(_g) == _B.len(_want) + 1 and _g[:-1] == _want):
    assert _is_list(_g), '`' + __NAME__ + '` is no longer a list.'
    _top = _g[:_B.len(_want)]
    assert not (_eqs and not _subs), ('`==` only asks whether two things are equal. It changes nothing, so the '
                                      + __OLD__ + ' is still there.')
    assert not (_calls_of('append', __NAME__) and _B.len(_g) > _B.len(_want) + 1 and _g[-1] == __FIXV__
                and _g[1] == __OLDV__), '`.append()` adds ' + __FIX__ + ' at the end, so the ' + __OLD__ + ' is still there.'
    assert not (_B.len(_g) > 1 and _g[1] == __OLDV__ and __FIXV__ in _top), (
        'Positions start at 0, so that changed the wrong item.')
    assert not (_B.len(_g) > 1 and _g[1] == __OLDV__ and _subs), 'Positions start at 0, so that changed the wrong item.'
    assert not (_B.len(_g) > 1 and _g[1] == __OLDV__), 'The ' + __OLD__ + ' is still in `' + __NAME__ + '`.'
    assert not (_B.len(_g) > 1 and type(_g[1]).__name__ == 'str'), 'The new number has quotes, so it is text.'
    assert _B.len(_g) > 1 and _g[1] == __FIXV__, 'Position 1 now holds ' + _shn(_g[1] if _g[1:] else None) + ', not ' + __FIX__ + '.'
    assert _top == _want, 'Another item changed too: `' + __NAME__ + '` holds ' + _shn(_g) + '.'
    assert False, ('`' + __NAME__ + '` ends with ' + _B.str(_B.len(_g)) + ' items, not the three numbers and one '
                   'guess.')
''',
        NAME=name, FIXED=fixed, OLD=str(old), OLDV=old, FIX=str(fix), FIXV=fix,
    )
    fix_line = chk(
        f"the {name} = [...] line still reads {nums}, and the fix follows another list",
        r'''
_lits = _typed_list(__NAME__)
assert not (_B.len(_lits) == 1 and _ast.literal_eval(_lits[0].value) != __WANT__), (
    'The `' + __NAME__ + ' = [...]` line was typed again, with ' + __FIX__ + ' in it, so Lucky' + chr(39) + 's '
    'copy was retyped, not changed by position.')
assert _B.len(_lits) < 2, 'The list was typed again. This task changes one item by its position, not the whole list.'
# The other list has the start's length, so a position counted from the end (`[-2]` before the append, `[-3]`
# after it) lands on the same item as in the student's own run.
_vals, _apps = {__NAME__: __OTHER__}, {__NAME__: __OTHERGUESS__}
_ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals, _apps)
assert not _miss, _lost(__NAME__)
_apps = _apps if (__NAME__ + '.append') in _seen else None
assert not _err, _lstop(_vals, _apps, _err)
_g = _ns.get(__NAME__)
_o = _vals[__NAME__]
_want = _o[:1] + [__FIXV__] + _o[2:]
# The own run already proved position 1 holds the fix. Here the other items must follow the other list, and
# position 1 must have changed, so a worked-out fix (`[1] = [1] - 1`) is fine, but a retyped list is not.
_rest = lambda _l: [_x for _i, _x in _B.enumerate(_l[:_B.len(_o)]) if _i != 1]
_moved = _is_list(_g) and _B.len(_g) > 1 and _rest(_g) == _rest(_o) and _g[1] != _o[1]
if not (_is_list(_g) and _g[:_B.len(_want)] == _want) and not _moved:
    assert not (_is_list(_g) and _g[:_B.len(__FIXED__)] == __FIXED__), (
        'With another list, the fix does not follow: the list was typed again.' + _ev(_vals, _apps))
    assert False, ('With another list, position 1 ends up as ' + _shn(_g[1] if _is_list(_g) and _g[1:] else None)
                   + ', not ' + __FIX__ + '.' + _ev(_vals, _apps))
''',
        NAME=name, WANT=start, FIX=str(fix), FIXV=fix, FIXED=fixed, OTHER=other[:len(start)],
        OTHERGUESS=other_guess,
    )
    fix_by_position = chk(
        f"the change is made by position: {name}[...] = ...",
        _SUBS + r'''
assert _subs, 'That changed the list another way. This task changes the one item by its position.'
''',
        NAME=name,
    )
    last = chk(
        "the last item is printed, read from the list",
        r'''
_own = _lastnums(_lines())
_front = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Subscript'
          and type(_n.ctx).__name__ == 'Load' and type(_n.value).__name__ == 'Name' and _n.value.id == __NAME__
          and type(_n.slice).__name__ == 'Constant' and _is_int(_n.slice.value) and _n.slice.value > 0]
for _vals, _apps in ((None, None), ({__NAME__: __OTHER__}, {__NAME__: __OTHERGUESS__})):
    _ns, _rows, _err, _miss, _seen, _snaps = _rerun(_vals or {}, _apps)
    assert not _miss, _lost(__NAME__)
    _apps = _apps if _apps and (__NAME__ + '.append') in _seen else None
    _g = _ns.get(__NAME__)
    _want = _g[-1] if _is_list(_g) and _g else None
    _got = _lastnums(_rows)
    if _want is not None and _want in _got:
        continue
    assert not _err, _lstop(_vals, _apps, _err)
    assert _got or not [_l for _l in _rows if _l.startswith('[')], 'Your line shows the whole list, not one item.'
    assert _got, 'No number was printed.'
    _apl = [_n.lineno for _n in _calls_of('append', __NAME__)]
    _early = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Call'
              and type(_n.value.func).__name__ == 'Name' and _n.value.func.id == 'print' and _apl
              and _n.lineno < _B.min(_apl)]
    assert not _early, 'The print is above the append, so it ran before the guess was added.'
    assert not (_vals is not None and _got == _own and _typed_print()), (
        'That number was typed, not read from the list.' + _ev(_vals, _apps))
    assert not (_vals is not None and _got == _own), ('Your line shows ' + _B.str(_got[-1]) + ' even when the list '
                                                     'holds other numbers.' + _ev(_vals, _apps))
    assert not _front, ('A position counted from the front fits one length only, so another list' + chr(39) + 's last '
                        'item is missed.' + _ev(_vals, _apps))
    assert False, 'That read does not find the last item of every list.' + _ev(_vals, _apps)
''',
        NAME=name, OTHER=other, OTHERGUESS=other_guess,
    )
    solution = program()
    return dict(
        id="make-append-read",
        title="Make, append, fix, read",
        martu=(
            lead
            + f"Lucky copied {copied} for you. Make the list, append your guess, mend Lucky's slip by its "
            "position, then print the last item, read from the list. My check tries another list, only inside the "
            "check, so never type a number you can see.\n"
            f"Stuck? Skip it, or try the lesson {lesson}. Tasks you pass here stay ticked."
        ),
        names=[name, "append"],
        pick=str(guess),
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="make-the-list",
                text=f"Make `{name}` a list holding {nums}, in that order.",
                dictated=False,
                hints=[
                    "Numbers go between square brackets, with a comma between each two. No quotes.",
                    "With other names: `steps = [9, 8, 6]` is a list of three numbers.",
                    f"Write `{name} = {start!r}` in place of `{name} = []`.",
                ],
                checks=[made],
            ),
            dict(
                id="append-a-guess",
                text=f"Append your guess for the next one: a whole number {side} {edge}.",
                dictated=False,
                hints=[
                    "`.append()` adds one item to the end of the list itself. The number goes in the round brackets.",
                    "With other names: `steps.append(5)` adds 5 to the end of `steps`.",
                    f"Write `{name}.append({guess})` under the `# 2.` note, with your own guess.",
                ],
                checks=[appended],
            ),
            dict(
                id="fix-by-position",
                text=f"Lucky miscopied the {old}: it should be {fix}. Change it by its position. Don't retype the list.",
                dictated=False,
                hints=[
                    f"Positions start at 0, so the {old} sits at position 1. One `=` puts a new item there.",
                    "With other names: `steps[0] = 10` changes the first item of `steps`, and keeps the rest.",
                    f"Write `{name}[1] = {fix}` under the `# 3.` note.",
                ],
                checks=[fix_value, fix_line, fix_by_position],
            ),
            dict(
                id="print-the-last",
                text=f"Print the last item of `{name}`, read from the list.",
                dictated=False,
                hints=[
                    "Count from the end, so it works for a list of any length.",
                    "With other names: `print(steps[-1])` shows the last item of `steps`.",
                    f"Write `print({name}[-1])` under the `# 4.` note.",
                ],
                checks=[last],
            ),
        ],
        solution=solution,
        partials=[program(app=None, mend=None, show=None), program(mend=None, show=None), program(show=None)],
        assemble=dict(
            lines=[f"{name} = {start!r}", f"{name}.append({guess})", f"{name}[1] = {fix}", f"print({name}[-1])"],
            distractors=[f"{name} + [{guess}]", f"{name}[2] = {fix}", f"print({guess})"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `{name} = {start!r}`. 2. `.append()` adds your guess at the end. 3. Position 1 is the second "
                f"item: one `=` swaps the {old} out. 4. `[-1]` reads the last item, however long the list is.")),
            dict(angle="shorter", text="Square brackets and commas, `.append()`, a change by position, then `[-1]`."),
        ],
        takeaway=(
            f"`.append()` adds to the list itself; `{name}[1] = {fix}` changes one item by position; `{name}[-1]` "
            "reads the last item of a list of any length."
        ),
        wrong_answers=[
            dict(why="the starter (empty list)", code=starter, fails_at=1, message_contains="still empty"),
            dict(why="quoted numbers", code=program(make=f"{name} = {[str(x) for x in start]!r}".replace("'", '"')),
                 fails_at=1, message_contains="quotes"),
            dict(why="round brackets (square brackets vs parentheses)",
                 code=program(make=f"{name} = ({', '.join(str(x) for x in start)})", app=None, mend=None),
                 fails_at=1, message_contains="tuple"),
            dict(why="missing commas", code=program(make=f"{name} = [{' '.join(str(x) for x in start)}]"), fails_at=0,
                 message_contains="invalid syntax"),
            dict(why="the guess typed into the list (a new list, not an append)",
                 code=program(make=f"{name} = {start + [guess]!r}", app=None), fails_at=1,
                 message_contains="nothing is appended"),
            dict(why="a near-miss name (one letter off)",
                 code=program(make=f"{name[:-1]} = {start!r}", app=f"{name[:-1]}.append({guess})",
                              mend=f"{name[:-1]}[1] = {fix}", show=f"print({name[:-1]}[-1])"),
                 fails_at=1, message_contains="letter for letter"),
            dict(why="a near-miss name (a capital letter)",
                 code=program(make=f"{name.capitalize()} = {start!r}", app=f"{name.capitalize()}.append({guess})",
                              mend=f"{name.capitalize()}[1] = {fix}", show=f"print({name.capitalize()}[-1])"),
                 fails_at=1, message_contains="letter for letter"),
            dict(why="+ without keeping the new list", code=program(app=f"{name} + [{guess}]"), fails_at=2,
                 message_contains="throws it away"),
            dict(why="+ a number, not a list (TypeError)", code=program(app=f"{name} = {name} + {guess}"), fails_at=0,
                 message_contains="can only concatenate list"),
            dict(why="a second list made (assigning a new list)",
                 code=program(app=f"{name} = {start + [guess]!r}"), fails_at=2, message_contains="brand-new list"),
            dict(why="the guess in quotes", code=program(app=f'{name}.append("{guess}")'), fails_at=2,
                 message_contains="quotes"),
            dict(why="square brackets for append's round ones", code=program(app=f"{name}.append[{guess}]"), fails_at=0,
                 message_contains="not subscriptable"),
            dict(why=f"a guess on the wrong side of {edge}",
                 code=program(app=f"{name}.append({edge + (5 if side == 'below' else -5)})"), fails_at=2,
                 message_contains=f"{side} {edge}"),
            dict(why="the fix: the whole list retyped on the first line",
                 code=program(make=f"{name} = {fixed!r}", mend=None), fails_at=3, message_contains="typed again"),
            dict(why="the fix: the whole list retyped on a new line (a re-run catches it too)",
                 code=program(mend=f"{name} = {fixed + [guess]!r}"), fails_at=3, message_contains="typed again"),
            dict(why="the fix: retyped through list() (only the re-run catches it)",
                 code=program(mend=f"{name} = list({fixed + [guess]!r})"), fails_at=3,
                 message_contains="does not follow"),
            dict(why="the fix one position off (index from 1)", code=program(mend=f"{name}[2] = {fix}"), fails_at=3,
                 message_contains="Positions start at 0"),
            dict(why="the fix with == (a question, not a change)", code=program(mend=f"{name}[1] == {fix}"),
                 fails_at=3, message_contains="`==` only asks"),
            dict(why="the fix appended", code=program(mend=f"{name}.append({fix})"), fails_at=3,
                 message_contains="adds " + str(fix) + " at the end"),
            dict(why="the fix made another way (insert and pop, not by position)",
                 code=program(mend=f"{name}.insert(1, {fix})\n{name}.pop(2)"), fails_at=3,
                 message_contains="another way"),
            dict(why="the fix in quotes", code=program(mend=f'{name}[1] = "{fix}"'), fails_at=3,
                 message_contains="quotes"),
            dict(why="the last item typed by hand", code=program(show=f"print({guess})"), fails_at=4,
                 message_contains="typed, not read"),
            dict(why="a position from the start only fits this length", code=program(show=f"print({name}[3])"),
                 fails_at=4, message_contains="counted from the front"),
            dict(why="len used as a position (IndexError)", code=program(show=f"print({name}[len({name})])"),
                 fails_at=0, message_contains="out of range"),
            dict(why="index from 1: the fourth item is [4] (IndexError)", code=program(show=f"print({name}[4])"),
                 fails_at=0, message_contains="out of range"),
            dict(why="the whole list printed", code=program(show=f"print({name})"), fails_at=4,
                 message_contains="whole list"),
            dict(why="printed above the append (top to bottom)",
                 code=program(app=f"print({name}[-1])\n{name}.append({guess})", show=""), fails_at=4,
                 message_contains="above the append"),
            dict(why=f"{extreme}() finds the guess here, but it is not the last item in every list",
                 code=program(show=f"print({extreme}({name}))"), fails_at=4, message_contains="every list"),
            dict(why="the guess's own name printed, not read from the list",
                 code=program(app=f"guess = {guess}\n{name}.append(guess)", show="print(guess)"), fails_at=4,
                 message_contains="even when the list holds other numbers"),
            dict(why="the hint's name copied (steps)",
                 code=program(make=f"steps = {start!r}", app=f"steps.append({guess})", mend=f"steps[1] = {fix}",
                              show="print(steps[-1])"),
                 fails_at=1, message_contains="from a hint"),
        ],
        notes=_qc_meta("list-make,list-append-len,list-change,list-index", "", "steps", form) + "\n"
        f"QC3 C1, form {form}. CP1 reads the first `{name} = [...]` literal (round brackets, quotes, the guess typed "
        f"into the list, a near-miss name gets the lesson's letter-for-letter sentence); Lucky's fixed copy "
        f"{fixed} is let through, so a retyped first line gets CP3's message. CP2: the list right after its first "
        f"length change (snapshots) must be {start} + one whole number {side} {edge} (Mar'tu's pick {guess}), with "
        f"position 1 left out of the compare so CP3's fix can't turn it red; a rerun with {other[:len(start)]} "
        f"(the start's length, so `[-2]` before the append still means position 1) catches a second "
        f"`{name} = [...]` line (assigning a new list). CP3 (teacher ruling: objective 3, change by position): "
        f"`{name}[1]` is {fix}, the `{name} = [...]` line still reads {nums} (a rerun with {other[:len(start)]} "
        f"catches a retype the static check can't see, like `list([...])`, while a worked-out fix such as "
        f"`{name}[1] = {name}[1] - 1` still passes), and an Assign to `{name}[...]`; any position that lands there "
        f"passes (`[1]`, or `[-3]` after the append), above or below the append; `==`, `.append({fix})`, "
        f"`[2]` and insert-and-pop each get their own message. CP4 reruns with {other} and the appended value "
        f"swapped for {other_guess} (the middle of that list, so `{extreme}()` and a sorted read fail too), so a "
        "typed print and `[3]` fail. Messages are lean: the slip and the evidence, never the line. "
        "explainer='lean'.",
    )


# ---- C2: the three newest, as a recipe that takes a list (objective 5) and slices it ----

def _qc_newest(form, outer, param, line, cases, second, story="", lead="", what="wall"):
    """`outer`: the starter's list (its name must not be read inside the recipe); `param`: the ingredient;
    `cases`: the fresh lists Mar'tu's check hands the recipe (one shorter, one longer than the starter's)."""
    start = eval(line.split("=", 1)[1])  # the starter's own list (a literal)
    counted = len(start) - 3  # a start counted for this length, like `[4:]` for 7 gaps

    def program(body="    return []", head=f"def newest_three({param}):"):
        return (
            story + line + head + "\n" + body + "\n\n"
            + f"print(newest_three({outer}))\n"
            + f"print(newest_three({second!r}))  # This should show {second[-3:]!r}\n"
        )

    starter = program()
    solution = program(f"    return {param}[-3:]")
    typed = start[-3:]
    defs = r'''
_defs = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef'
         and _n.name == 'newest_three']
_fn = globals().get('newest_three')
_nm = _near('newest_three')
assert _B.callable(_fn) and _defs, (
    ('Python matches names letter for letter: you wrote `' + _nm[0] + '`, the task needs `newest_three`.') if _nm
    else ('The recipe `newest_three` is gone, so Mar' + chr(39) + 'tu' + chr(39) + 's check has nothing to call.'))
_args = [_a.arg for _a in _defs[-1].args.args]
assert _args == [__PARAM__], 'The ingredient' + chr(39) + 's name changed: the starter named it `' + __PARAM__ + '`.'
'''
    ret = chk(
        "newest_three hands its answer back with return (RET)",
        defs + r'''
_rets = [_n for _n in _ast.walk(_defs[-1]) if type(_n).__name__ == 'Return' and _n.value is not None]
_prints = [_n for _n in _ast.walk(_defs[-1]) if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name'
           and _n.func.id == 'print']
assert _rets or not _prints, 'The recipe prints, but hands nothing back.'
assert _rets, 'The recipe hands nothing back.'
''',
        PARAM=param,
    )
    par = chk(
        "newest_three hands back the three newest of a shorter and a longer list (PAR)",
        defs + r'''
_inner = [_m.id for _m in _ast.walk(_defs[-1]) if type(_m).__name__ == 'Name']
_cases = __CASES__
_got = [_call(_fn, _c) for _c in _cases]
_bad = [_i for _i in _B.range(_B.len(_cases)) if _got[_i][2] or type(_got[_i][0]).__name__ != 'list'
        or _got[_i][0] != _cases[_i][-3:]]
if _bad:
    _i = _bad[0]
    _a = _cases[_i]
    _out, _pr, _err = _got[_i]
    _ev1 = " (Mar'tu's check called `newest_three(" + _sh(_a) + ")`"
    _back = ': it handed back ' + _shn(_out) + '.)'
    _none = ': it handed back `None`: nothing came back.)'
    _both = (" (Mar'tu's check called `newest_three(" + _sh(_cases[0]) + ")` and `newest_three("
             + _sh(_cases[1]) + ")`: both handed back " + _shn(_got[0][0]) + '.)')
    if __OUTER__ in _inner:
        _msg = 'The recipe reads the list from outside, not the one it is handed.' + _ev1 + _back
    elif _err.startswith('IndexError'):
        _msg = 'The recipe asks for a position the list does not have.' + _ev1 + ': Python stopped with IndexError.)'
    elif _err:
        _msg = 'The recipe stops on some lists.' + _ev1 + ': Python stopped with ' + _err.split(':')[0] + '.)'
    elif _out is None and _pr:
        _msg = 'The recipe prints the three, but hands nothing back.' + _ev1 + _none
    elif _out is None:
        _msg = 'The recipe hands nothing back.' + _ev1 + _none
    elif _out == []:
        _msg = 'The recipe still hands back the starter' + chr(39) + 's empty list.' + _ev1 + _back
    elif _got[0][0] == _got[1][0]:
        _msg = 'That list was typed, not cut from the list the recipe is handed.' + _both
    elif type(_out).__name__ == 'tuple':
        _msg = 'That hands back a tuple, in round brackets, not one list.' + _ev1 + _back
    elif type(_out).__name__ == 'str':
        _msg = 'The recipe hands back text, not the items.' + _ev1 + '.)'
    elif _is_int(_out):
        _msg = 'That is one item, not three.' + _ev1 + _back
    elif _out == _a:
        _msg = 'That is the whole list, not the newest three.' + _ev1 + _back
    elif _out == _a[-3:-1]:
        _msg = 'A slice stops before its end, so the newest is missing.' + _ev1 + _back
    elif _out == _a[__COUNTED__:]:
        _msg = ('That start was counted for a list of ' + _B.str(__LEN__) + ', so other lists get the wrong items.'
                + _ev1 + _back)
    elif _out == _a[:3]:
        _msg = 'Those are the three oldest, not the three newest.' + _ev1 + _back
    elif _is_list(_out) and _same_items(_out, _a[-3:]):
        _msg = 'Right three, but sorted: the newest keep the order they have in the list.' + _ev1 + _back
    elif _is_list(_out) and _same_items(_out, _B.sorted(_a)[-3:]):
        _msg = 'Those are the three biggest, not the three newest.' + _ev1 + _back
    else:
        _msg = ('That is not the three newest of every list.' + _ev1 + ': it handed back ' + _shn(_out) + ', not '
                + _sh(_a[-3:]) + '.)')
    assert False, _msg
''',
        PARAM=param, OUTER=outer, CASES=cases, COUNTED=counted, LEN=len(start),
    )
    sliced = chk(
        "newest_three cuts them with one slice",
        defs + r'''
_sl = [_n for _n in _ast.walk(_defs[-1]) if type(_n).__name__ == 'Slice']
assert _sl, 'Right three, but read one by one. This task cuts them with one slice.'
''',
        PARAM=param,
    )
    return dict(
        id="the-three-newest",
        title="The three newest",
        martu=(
            lead
            + f"The three newest, as a recipe that works for a {what} of any length. My check hands it a shorter "
            f"{what} and a longer one, only inside the check, so cut them from the {what} it is handed, yes?\n"
            "Stuck? Skip it, or try the lessons Many Values, One Name and Reading the Wall Closely. Tasks you pass "
            "here stay ticked."
        ),
        names=["newest_three", param],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="slice-the-newest",
                text=(
                    f"Make `newest_three({param})` hand back the three newest items of any {what} it is handed, "
                    "with one slice."
                ),
                dictated=False,
                hints=[
                    f"Inside the recipe, the {what} it is handed is called `{param}`. Slice that: start 3 from the "
                    "end, and leave the end empty.",
                    "With other names: `return steps[-2:]` hands back the last two items of `steps`.",
                    f"Write `return {param}[-3:]` in place of `return []`.",
                ],
                checks=[ret, par, sliced],
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[line.strip(), f"def newest_three({param}):", f"    return {param}[-3:]",
                   f"print(newest_three({outer}))", f"print(newest_three({second!r}))"],
            distractors=[f"    return {param}[-3:-1]", f"    return {outer}[-3:]", f"    print({param}[-3:])"],
        ),
        another_way=[
            dict(angle="picture", text=(
                f"```text\n... {typed[0]}  {typed[1]}  {typed[2]}\n    -3  -2  -1  (end)\n```\n"
                f"Inside the recipe the list is `{param}`. `[-3:]` starts 3 from the end and runs to the very end, "
                "on a list of any length.")),
            dict(angle="campaign", label="You've seen this", text=(
                "In the campaign, a recipe like `add_spell(...)` worked on whatever it was handed. "
                f"`newest_three` is the same: it never asks for `{outer}` by name.")),
            dict(angle="shorter", text=f"`return {param}[-3:]`: the ingredient, three from the end, end left empty."),
        ],
        takeaway=(
            f"`return {param}[-3:]` hands back the three newest of any list the recipe is handed. `[-3:-1]` leaves "
            "out the last."
        ),
        wrong_answers=[
            dict(why="the starter (the placeholder [])", code=starter, fails_at=1, message_contains="empty list"),
            dict(why="the outer list's name used inside the recipe (copying the example list's name)",
                 code=program(f"    return {outer}[-3:]"), fails_at=1, message_contains="from outside"),
            dict(why="the three typed by hand", code=program(f"    return {typed!r}"), fails_at=1,
                 message_contains="was typed"),
            dict(why="print instead of return (RET)", code=program(f"    print({param}[-3:])"), fails_at=1,
                 message_contains="prints, but hands nothing back"),
            dict(why="the slice end left out ([-3:-1])", code=program(f"    return {param}[-3:-1]"), fails_at=1,
                 message_contains="stops before its end"),
            dict(why=f"a start counted for {len(start)} items", code=program(f"    return {param}[{counted}:]"),
                 fails_at=1, message_contains=f"counted for a list of {len(start)}"),
            dict(why="the three oldest", code=program(f"    return {param}[:3]"), fails_at=1,
                 message_contains="oldest"),
            dict(why="sorted first: the three biggest, not the three newest",
                 code=program(f"    return sorted({param})[-3:]"), fails_at=1, message_contains="biggest"),
            dict(why="the list it is handed sorted in place (changing the original, not a copy)",
                 code=program(f"    {param}.sort()\n    return {param}[-3:]"), fails_at=1,
                 message_contains="biggest"),
            dict(why="the newest three, then sorted", code=program(f"    return sorted({param}[-3:])"), fails_at=1,
                 message_contains="but sorted"),
            dict(why="one item, no colon", code=program(f"    return {param}[-3]"), fails_at=1,
                 message_contains="one item"),
            dict(why="the whole list handed back", code=program(f"    return {param}"), fails_at=1,
                 message_contains="whole list"),
            dict(why="three reads with commas (a tuple)",
                 code=program(f"    return {param}[-3], {param}[-2], {param}[-1]"), fails_at=1,
                 message_contains="tuple"),
            dict(why="three reads in a list: right values, but no slice",
                 code=program(f"    return [{param}[-3], {param}[-2], {param}[-1]]"), fails_at=1,
                 message_contains="one slice"),
            dict(why="the ingredient renamed to the outer list's name",
                 code=program(f"    return {outer}[-3:]", head=f"def newest_three({outer}):"), fails_at=1,
                 message_contains="ingredient"),
            dict(why="the recipe's name one letter off (near miss)",
                 code=solution.replace("newest_three", "newest_tree"), fails_at=1,
                 message_contains="letter for letter"),
            dict(why="len used as a position (IndexError)", code=program(f"    return {param}[len({param})]"),
                 fails_at=0, message_contains="out of range"),
            dict(why="round brackets for the slice (square brackets vs parentheses)",
                 code=program(f"    return {param}(-3:)"), fails_at=0, message_contains="invalid syntax"),
        ],
        notes=_qc_meta("list-append-len,param-use,return-value,range-slice-sort", "", "steps", form) + "\n"
        f"QC3 C2, form {form} (teacher ruling on the Unit 4 reviews: a recipe that takes a list, objective 5, and a "
        f"slice, in one task). The starter's second call, `newest_three({second})`, shows the wrong answer on the "
        f"student's own Run (`[]`, or the outer list's newest when `{outer}` is read inside). Three checks: RET "
        f"(static: a `return` with a value; a print in its place gets its own message), PAR (the recipe called on "
        f"two fresh lists the task never shows, {len(cases[0])} and {len(cases[1])} items, the longer one not in "
        f"order so a sorted read fails; first wrong call diagnosed: the outer name inside, a typed list, `[-3:-1]`, "
        f"a start counted for {len(start)}, the oldest, the biggest, a tuple), and a Slice inside the recipe "
        "(three reads in a list get 'one slice'). Lean messages: the slip and the evidence, never the line. "
        "explainer='lean'.",
    )


# ---- C3: a nested read and a sorted copy, mended ----

def _qc_mend(form, table, table_code, row, who, what, nums_name, nums, other_table, other_ev, other_nums,
             pass_line):
    """table: the nested list's name; row: the row the task reads; who: the row's first item (shown in the task)."""
    loud = f"print({table}[{row + 1}][2])"
    fixed = f"print({table}[{row}][1])"
    comment = f"# Print {who}'s {what}.\n" if not who.islower() else f"# Print the {who} {what}.\n"

    def program(read=loud, sort=f"ordered = {nums_name}.sort()"):
        return (
            table_code + comment + read + "\n"
            + f"{nums_name} = {nums!r}\n"
            + f"# A sorted copy. {nums_name} stays put.\n"
            + sort + "\n"
            + "print(ordered)\n"
        )

    starter = program()
    solution = program(fixed, f"ordered = sorted({nums_name})")
    want = (ROSTER if table == "roster" else DRILLS)[row][1]
    label = f"{who}'s {what}" if not who.islower() else f"the {who} {what}"
    read_check = chk(
        f"{label} is printed, read from {table}",
        r'''
_own = _lastnums(_lines())
for _vals in (None, {__TABLE__: __OTHER__}):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    _T = _ns.get(__TABLE__)
    assert not _miss and _is_list(_T), _lost(__TABLE__)
    _ev_t = '' if _vals is None else __OTHEREV__
    _want = _T[__ROW__][1]
    _got = _lastnums(_rows)
    if _want in _got:
        continue
    assert not _err, 'With another `' + __TABLE__ + '`, Python stopped: ' + _err + '.' + _ev_t
    assert not [_l for _l in _rows if _l == _B.str(_T[__ROW__])], 'Your line shows the whole row, not one item in it.'
    assert not [_l for _l in _plain(_rows) if _B.str(_T[__ROW__][0]) in _l and not _nums(_l)], (
        '`[0]` is the name, not the ' + __WHAT__ + '.')
    assert not (_T[__ROW__ + 1][1] in _got), 'Rows start at 0, so that is the wrong row.' + _ev_t
    assert not (_vals is not None and _got == _own and _typed_print()), (
        'That number was typed, not read from `' + __TABLE__ + '`.' + _ev_t)
    assert not (_vals is not None and _got == _own), ('Your line shows ' + _B.str(_got[-1]) + ' even with another `'
                                                     + __TABLE__ + '`.' + _ev_t)
    assert False, 'That is not ' + __LABEL__ + ' on every `' + __TABLE__ + '`.' + _ev_t
''',
        TABLE=table, OTHER=other_table, OTHEREV=other_ev, ROW=row, WHAT=what, LABEL=label,
    )
    sort_check = chk(
        f"ordered is a sorted copy, and {nums_name} keeps its order",
        r'''
_alias = [_n for _n in _assigns('ordered') if type(_n.value).__name__ == 'Name' and _n.value.id == __NUMS__]
_own = globals().get('ordered')
for _vals in (None, {__NUMS__: __OTHERNUMS__}):
    _ns, _rows, _err, _miss, _seen, _snaps = _case(_vals)
    assert not _miss, _lost(__NUMS__)
    _start = __START__ if _vals is None else _vals[__NUMS__]
    _o, _m = _ns.get('ordered'), _ns.get(__NUMS__)
    if _o == _B.sorted(_start) and _m == _start and _o is not _m:
        continue
    assert not _err, _lstop(_vals, None, _err)
    _nm = _near('ordered')
    assert 'ordered' in _ns or not _nm, ('Python matches names letter for letter: you wrote `' + (_nm or [''])[0]
                                         + '`, the task needs `ordered`.')
    assert 'ordered' in _ns, 'The line that makes `ordered` is gone.'
    assert type(_o).__name__ != 'NoneType', '`.sort()` hands back `None`, so `ordered` holds `None`: nothing came back.'
    if _m != _start or _o is _m:
        assert not (_alias and not _calls_of('sort', __NUMS__)), ('`ordered = ' + __NUMS__ + '` gives the same list '
                                                                  'a second name, so sorting one sorts both.')
        assert False, '`.sort()` sorted `' + __NUMS__ + '` itself, so `' + __NUMS__ + '` lost its order.' + _ev(_vals)
    assert not _is_int(_o), '`ordered` holds one number, not a sorted copy.' + _ev(_vals)
    assert not (_vals is not None and _o == _own), '`ordered` was typed, not sorted from `' + __NUMS__ + '`.' + _ev(_vals)
    assert False, '`ordered` holds ' + _shn(_o) + ', not a sorted copy of `' + __NUMS__ + '`.' + _ev(_vals)
''',
        NUMS=nums_name, OTHERNUMS=other_nums, START=nums,
    )
    plain_print = sorted(nums)
    return dict(
        id="mend-the-reads",
        title="Mend the reads",
        martu=(
            "Two slips: one loud, one quiet. Read Python's last line and mend the line it names. Then read what "
            f"the program prints. My check tries another `{table}` and other numbers, only inside the check.\n"
            "Stuck? Skip it, or try the lessons Many Values, One Name and Reading the Wall Closely. Tasks you pass "
            "here stay ticked."
        ),
        names=[table, nums_name, "ordered", "sorted"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="mend-the-read",
                text=f"Mend the line that should print {label}, read from `{table}`.",
                dictated=False,
                hints=[
                    "Read Python's last line. Which line does it name?",
                    "Outer number first: which row. Rows start at 0. Inner number second: `[1]` is the "
                    f"{what}.",
                    "With other names: `shelf[0][1]` is the second item of the first row.",
                    f"Write `{fixed}` in place of `{loud}`.",
                ],
                checks=[read_check],
            ),
            dict(
                id="mend-the-sort",
                text=f"Mend the sort so `ordered` holds a sorted copy, and `{nums_name}` keeps its order.",
                dictated=False,
                hints=[
                    "No message now, so read what the program printed last.",
                    f"`.sort()` sorts `{nums_name}` itself and hands back `None`: nothing comes back. Which tool "
                    "hands back a sorted copy?",
                    "With other names: `ups = sorted(steps)` makes a sorted copy, and `steps` keeps its order.",
                    f"Write `ordered = sorted({nums_name})` in place of `ordered = {nums_name}.sort()`.",
                ],
                checks=[sort_check],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        partials=[program(fixed)],
        assemble=dict(
            lines=[line for line in solution.splitlines() if not line.startswith("#")],
            distractors=[f"print({table}[{row + 1}][1])", f"ordered = {nums_name}.sort()", f"ordered = {nums_name}"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. Run and read the last line: an IndexError. 2. Mend the read: row {row}, then `[1]`. 3. Run again: "
                f"`None` is printed, because nothing came back. 4. Use `sorted({nums_name})`.")),
            dict(angle="shorter", text=f"`{table}[{row}][1]`: row first, then item. `sorted()` copies; `.sort()` hands back `None`."),
        ],
        takeaway=f"`{table}[{row}][1]`: row first, from 0, then the item. `sorted()` hands back a copy; `.sort()` hands back `None`.",
        wrong_answers=[
            dict(why="the starter (IndexError on the read)", code=starter, fails_at=0, message_contains="out of range"),
            dict(why="the read mended, the sort still hands back None (quiet slip)", code=program(fixed), fails_at=2,
                 message_contains="nothing came back"),
            dict(why="the row counted from 1", code=program(f"print({table}[{row + 1}][1])"), fails_at=1,
                 message_contains="Rows start at 0"),
            dict(why="the whole row printed", code=program(f"print({table}[{row}])"), fails_at=1,
                 message_contains="whole row"),
            dict(why="the name printed", code=program(f"print({table}[{row}][0])"), fails_at=1,
                 message_contains="`[0]` is the name"),
            dict(why=f"the {what} typed by hand", code=program(f"print({want})"), fails_at=1,
                 message_contains="typed, not read"),
            dict(why="the inner position still 2 (IndexError)", code=program(f"print({table}[{row}][2])"), fails_at=0,
                 message_contains="out of range"),
            dict(why="sorted the original (a copy versus the original)",
                 code=program(fixed, f"{nums_name}.sort()\nordered = {nums_name}"), fails_at=2,
                 message_contains="lost its order"),
            dict(why="a second name for the same list, then sorted (changing the original through the copy)",
                 code=program(fixed, f"ordered = {nums_name}\nordered.sort()"), fails_at=2,
                 message_contains="second name"),
            dict(why="sorted in place first, then a sorted copy (the original changed)",
                 code=program(fixed, f"{nums_name}.sort()\nordered = sorted({nums_name})"), fails_at=2,
                 message_contains="lost its order"),
            dict(why="the sorted list typed by hand", code=program(fixed, f"ordered = {plain_print!r}"), fails_at=2,
                 message_contains="was typed"),
            dict(why="sorted with square brackets", code=program(fixed, f"ordered = sorted[{nums_name}]"), fails_at=0,
                 message_contains="not subscriptable"),
            dict(why="a near-miss name for ordered",
                 code=program(fixed, f"orderd = sorted({nums_name})").replace("print(ordered)", "print(orderd)"),
                 fails_at=2, message_contains="letter for letter"),
            dict(why=f"the same number read from {nums_name}, not from {table}",
                 code=program("").replace(f"{nums_name} = {nums!r}\n",
                                          f"{nums_name} = {nums!r}\nprint({nums_name}[{nums.index(want)}])\n"),
                 fails_at=1, message_contains=f"even with another `{table}`"),
        ],
        notes=_qc_meta("list-nested,list-index,range-slice-sort,read-traceback", "", "shelf,steps,ups", form) + "\n"
        f"QC3 C3, form {form}. A loud slip, `{loud}` (IndexError: the row and the inner position both counted from "
        f"1), then a quiet one: `ordered = {nums_name}.sort()` prints `None` (nothing came back). CP1 reruns with "
        f"another {table} ({other_ev.strip()}), so a typed number and the next row fail. CP2 reruns with "
        f"{nums_name} = {other_nums}: `ordered` must be a sorted copy and `{nums_name}` unchanged, so the in-place "
        f"`.sort()` and `ordered = {nums_name}` (a second name, not a copy) fail. This is the Quick Check's sort/None "
        "evidence (the questions' sort item became `range` + `+`). Lean messages: the slip and the evidence, never "
        "the line. explainer='lean'.",
    )


ROSTER_OTHER = [["Pell", 31], ["Brakka", 7], ["Moss", 15], ["Glug", 3]]
ROSTER_OTHER_EV = " (Mar'tu's check tried another roster: Pell 31, Brakka 7, Moss 15, Glug 3, only inside the check.)"
DRILLS_OTHER = [["kick", 11], ["leap", 14], ["block", 17], ["dodge", 19]]
DRILLS_OTHER_EV = " (Mar'tu's check tried other drills: kick 11, leap 14, block 17, dodge 19, only inside the check.)"
ORE_LEAD = (
    "Bomb Shell's Velocite ore powers everything. This list is how many chunks he used each day.\n"
)

QC3_A = dict(
    kind="testout",
    id="qc3-a",
    title="Quick Check 4 · Form A",
    optional=True,
    minutes=14,
    summary=(
        "Three short tasks and two questions, no hints. Pass all three tasks and get both questions right to test "
        "out of Unit 4. Stuck on one? The lessons teach all of it, and tasks you pass here stay ticked."
    ),
    questions_to_pass=2,
    exercises=[
        _qc_make("A", "marks", [46, 44, 41], ("below", 41), 33, 43, [30, 29, 27, 24], 28),
        _qc_newest("A", "chalk_wall", "wall", WALL_LINE, [[60, 58, 55, 51, 46], [50, 49, 49, 48, 47, 45, 40, 43, 38]],
                   [9, 8, 7, 6]),
        _qc_mend("A", "roster", ROSTER_CODE, 2, "Bomb Shell", "mana", "manas", [26, 18, 24, 20], ROSTER_OTHER,
                 ROSTER_OTHER_EV, [12, 30, 8, 21],
                 "Mar'tu: The gaps shrink, 48 down to 37. Bomb Shell studied the wall: thirty-two hours, maybe "
                 "less. That is Unit 4, yes? Want a stretch? Try The Basement Inventory."),
    ],
    notes=(
        "Quick Check 3, form A (code tasks). Questions live in qc3-a-questions. Pass = every code task plus both "
        "questions; a retake draws form B. The site gates on both (questions_to_pass=2, as Unit 2's QC2 gates on "
        "its questions; 'Both right is a pass', the teacher's ruling), and the code tasks alone still cover every "
        "skill the QC claims. Teacher ruling on the Unit 4 reviews (a true fast "
        "path, no fourth task): C1 gets a fix by position (objective 3), C2 becomes the recipe `newest_three(wall)` "
        "(objective 5's recipe that takes a list, and a slice, checked on fresh walls), and Q2 swaps sort/None (C3 "
        "tests it in code) for `range` + `+`. Coverage (lint d): list-make -> C1 CP1 (WA round brackets, quoted "
        "numbers, missing commas, near-miss names); list-append-len -> C1 CP2 (WA `+` thrown away, `+ 33` "
        "TypeError, a second list), C1 CP4 (WA `[len(marks)]`) and Q2 (`+` joins two lists); list-change -> C1 "
        "CP3 (WA retyped, `[2]`, `==`, `.append(43)`); list-index -> Q1 (off-by-one at -2 and len), C1 CP4 (WA "
        "`print(33)` typed, `[3]` from the start) and C3 CP1 (row from 1); recipe that takes a list (param-use, "
        "return-value) -> C2 (WA `chalk_wall` inside, typed list, print for return); list-nested -> Q1 (`[1][0]`) "
        "and C3 CP1 (WA whole row, name, typed); range-slice-sort -> Q2 (the stop left out), C2 (WA `[-3:-1]`, a "
        "start counted for 7, sorted) and C3 CP2 (WA None, in-place sort, `ordered = manas`). Every message is "
        "lean (Unit 2 ruling): the slip and the evidence bracket, never the line to type. support='none' "
        "everywhere: no hints, tracer or compare; glossary, read-aloud, DF and the lean explainer stay on. "
        "14 minutes (12 before: three tasks, plus one checkpoint)."
    ),
)

QC3_B = dict(
    kind="testout",
    id="qc3-b",
    title="Quick Check 4 · Form B",
    optional=True,
    minutes=14,
    summary=(
        "Three short tasks and two questions, no hints. Pass all three tasks and get both questions right to test "
        "out of Unit 4. Stuck on one? The lessons teach all of it, and tasks you pass here stay ticked."
    ),
    questions_to_pass=2,
    exercises=[
        _qc_make("B", "ore_used", [4, 5, 7], ("above", 7), 9, 6, [2, 3, 6, 8], 5, story=ORE_STORY, lead=ORE_LEAD,
                 copied="three of the days"),
        _qc_newest("B", "ore_used", "days", ORE_LINE, [[1, 2, 2, 4, 6], [1, 1, 2, 7, 3, 3, 6, 8, 5]],
                   [1, 2, 4, 8], story=ORE_STORY, lead="Bomb Shell's ore list again. ", what="list"),
        _qc_mend("B", "drills", DRILLS_CODE, 1, "shield wall", "score", "scores", [6, 9, 5, 7], DRILLS_OTHER,
                 DRILLS_OTHER_EV, [12, 4, 15, 10],
                 "Mar'tu: His ore runs low, and the burst comes sooner. Bomb Shell counts every chunk. That is Unit "
                 "4, yes? Want a stretch? Try The Basement Inventory."),
    ],
    notes=(
        "Quick Check 3, form B: Bomb Shell's Velocite ore (`ore_used`: chunks used each day, told in the starter "
        "comment and Mar'tu's first line; C1 4, 5, 7, a guess above 7 and Lucky's miscopied 5 fixed to 6; C2 the "
        "recipe `newest_three(days)`, its second call `newest_three([1, 2, 4, 8])`, and fresh lists of 5 and 9 "
        "days) and Oogrish's `drills` (C3: the shield wall score, row 1, and `scores`). Mirrors every form A "
        "change: the fix by position, the recipe, Q2 as `range` + `+`, lean messages, near-miss names. Same "
        "coverage as form A. Questions live in qc3-b-questions. Pass = every code task plus both questions: the "
        "site gates on both (questions_to_pass=2). 14 minutes."
    ),
)



def _lean_guard(form):
    """Quick Check messages are lean (Unit 2 ruling): the slip and the evidence, never the fix. Proved here, as
    Unit 2's `_leaned` asserts its rewrites: no check of a form's tasks may hold a line of Mar'tu's version that the
    starter does not show, or that line's working part (the read, the call, the slice). Literal values (the start
    list, a guess) are left out: the checks need them to compare."""
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
            for head in ("print(", "return"):
                if right.startswith(head):
                    right = right[len(head):-1] if head == "print(" else right[len(head):]
            if right.strip("[]0123456789,-"):
                pieces.add(right)
        for cp in ex["checkpoints"]:
            for name, check in cp["checks"]:
                found = [piece for piece in pieces if len(piece) >= 4 and piece in squash(check)]
                assert not found, f"{form['id']}/{ex['id']}: the check {name!r} names the fix {found[0]!r}"
    return form


_lean_guard(QC3_A)
_lean_guard(QC3_B)


def _qc_questions(form, read, join):
    r_q, r_setup, r_code, r_answer, r_choices, r_explain, r_notes = read
    j_code, j_answer, j_choices, j_explain, j_notes = join
    return dict(
        kind="quiz",
        id=f"qc3-{form.lower()}-questions",
        title=f"Quick Check 4 · Form {form} questions",
        optional=True,
        minutes=3,
        summary="Two questions that go with Quick Check 4. To pass the Quick Check, get both right.",
        questions=[
            dict(type="predict", id="read-by-position", q=r_q, setup=r_setup, code=r_code, answer=r_answer,
                 choices=r_choices, explain=r_explain, notes=r_notes),
            dict(type="predict", id="count-and-join", q="What will this print?", code=j_code, answer=j_answer,
                 choices=j_choices, explain=j_explain, notes=j_notes),
        ],
        notes=(
            f"Quick Check 3, form {form} questions (scored with qc3-{form.lower()}: every code task plus both "
            "questions, questions_to_pass=2 on the form). The best score counts, so a retake can lift it. No hints; read-aloud and glossary stay on. The site shuffles the choices; the right one is also "
            "authored in a different place in each question (teacher ruling)."
        ),
    )


QC3_A_QUESTIONS = _qc_questions(
    "A",
    (
        "`chalk_wall` holds `[48, 48, 47, 46, 44, 41, 37]`. `roster` holds four rows: `[\"Oogrish\", 18]`, "
        "`[\"Gearshift\", 20]`, `[\"Bomb Shell\", 24]` and `[\"Lucky\", 26]`. What will this print?",
        WALL_LINE + ROSTER_CODE,
        "print(chalk_wall[-2])\nprint(len(chalk_wall))\nprint(roster[1][0])\n",
        "41\n7\nGearshift",
        ["37\n7\nGearshift", "41\n6\nGearshift", "41\n7\nOogrish", "41\n7\nGearshift", "41\n7\nLucky"],
        (
            "`[-2]` is the second from the end: 41. `len` counts the gaps: 7 (the last position is 6). Row 1 is the "
            "second row, because rows start at 0, and `[0]` is its name: Gearshift."
        ),
        "Skills list-index, list-nested. Distractors: -2 read as the last (37), len read as the last position (6), "
        "row 1 read as the first row (Oogrish), row 1 read as -1 (Lucky). The right one is authored fourth.",
    ),
    (
        "print(list(range(1, 4)) + [9])\n",
        "[1, 2, 3, 9]",
        ["[1, 2, 3, 4, 9]", "[0, 1, 2, 3, 9]", "[1, 2, 3, 9]", "[1, 2, 3, [9]]"],
        (
            "`range(1, 4)` counts 1, 2, 3: the stop is left out. `+` joins two lists into one, so the 9 sits at the "
            "end as an item of its own, not inside brackets."
        ),
        "Skills range-slice-sort (the stop is left out) and list-append-len (`+` joins two lists). Replaces "
        "what-sort-hands-back (teacher ruling: C3 CP2 tests sort/None in code). Distractors: the stop included (4), "
        "counted from 0, `+` read as putting a list inside a list. The right one is authored third.",
    ),
)

QC3_B_QUESTIONS = _qc_questions(
    "B",
    (
        "`ore_used` holds `[2, 3, 3, 4, 5, 7]`. `drills` holds four rows: `[\"cane parry\", 7]`, "
        "`[\"shield wall\", 5]`, `[\"slow breaths\", 9]` and `[\"roll and rise\", 6]`. What will this print?",
        ORE_LINE + DRILLS_CODE,
        "print(ore_used[-2])\nprint(len(ore_used))\nprint(drills[1][0])\n",
        "5\n6\nshield wall",
        ["7\n6\nshield wall", "5\n6\nshield wall", "5\n5\nshield wall", "5\n6\ncane parry", "5\n6\nroll and rise"],
        (
            "`[-2]` is the second from the end: 5. `len` counts the days: 6 (the last position is 5). Row 1 is the "
            "second row, because rows start at 0, and `[0]` is its name: shield wall."
        ),
        "Form B of read-by-position. Distractors: -2 read as the last (7), len read as the last position (5), row 1 "
        "read as the first row (cane parry), row 1 read as -1 (roll and rise). The right one is authored second.",
    ),
    (
        "print(list(range(2, 5)) + [8])\n",
        "[2, 3, 4, 8]",
        ["[2, 3, 4, 5, 8]", "[2, 3, 4, [8]]", "[0, 1, 2, 3, 4, 8]", "[2, 3, 4, 8]"],
        (
            "`range(2, 5)` counts 2, 3, 4: the stop is left out. `+` joins two lists into one, so the 8 sits at the "
            "end as an item of its own, not inside brackets."
        ),
        "Form B of count-and-join. Distractors: the stop included (5), counted from 0, `+` read as putting a list "
        "inside a list. The right one is authored last.",
    ),
)


# =============================================================================================
# Cheatsheet "Mar'tu's Chalk Notes: Lists"
# =============================================================================================

CHALK_NOTES_3 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Lists",
    summary="Everything from Unit 4 on one page. Printable.",
    entries=[
        dict(concept="Make a list: `[ ]` and commas", code="wall = [48, 47, 46]\nprint(wall)\n", output="[48, 47, 46]",
             note="Square brackets around, commas between. Numbers have no quotes. (Lesson: Many Values, One Name)"),
        dict(concept="The first is `[0]`", code="wall = [48, 47, 46]\nprint(wall[0])\nprint(wall[1])\n",
             output="48\n47", note="Positions start at 0. `[1]` is the second item."),
        dict(concept="The last is `[-1]`", code="wall = [48, 47, 46]\nprint(wall[-1])\nprint(wall[-2])\n",
             output="46\n47", note="Negative positions count from the end. `[-1]` works for a list of any length."),
        dict(concept="Change one item: `wall[i] = x`", code="wall = [48, 74, 46]\nwall[1] = 47\nprint(wall)\n",
             output="[48, 47, 46]", note="Fix a mark by its position. No retyping the list."),
        dict(concept="Grow it: `.append(x)`", code="wall = [48, 47]\nwall.append(46)\nprint(wall)\n",
             output="[48, 47, 46]", note="Adds one item to the end of the list itself."),
        dict(concept="Join two lists: `a + b`", code="old = [48, 48]\nnew = [47, 46]\nprint(old + new)\n",
             output="[48, 48, 47, 46]", note="`+` joins two lists into a new one. `wall + 33` is a TypeError: "
             "`+` needs a list on both sides."),
        dict(concept="How many: `len()`", code="wall = [48, 47, 46]\nprint(len(wall))\n", output="3",
             note="The last position is `len - 1`, here 2, because positions start at 0."),
        dict(concept="A recipe that takes a list",
             code=("def newest_mark(wall):\n    return wall[len(wall) - 1]\n\nprint(newest_mark([9, 8, 7]))\n"
                   "print(newest_mark([48, 41]))\n"),
             output="7\n41",
             note="Use the ingredient `wall`, so it works for any list it is handed. `wall[-1]` is the short way. "
             "(Lesson: Many Values, One Name)"),
        dict(concept="A list inside a list: `roster[3][1]`",
             code='roster = [\n    ["Oogrish", 18],\n    ["Gearshift", 20],\n    ["Bomb Shell", 24],\n'
                  '    ["Lucky", 26],\n]\nprint(roster[3][1])\n',
             output="26", note="Outer number first: which row. Inner number second: which item in it."),
        dict(concept="Count: `range(1, 7)` stops before 7", code="print(list(range(1, 7)))\n",
             output="[1, 2, 3, 4, 5, 6]", note="The stop is left out. `list()` turns the count into a list. "
             "(Lesson: Reading the Wall Closely)"),
        dict(concept="Slice: `wall[-3:]`",
             code="wall = [48, 48, 47, 46, 44, 41, 37]\nprint(wall[-3:])\nprint(wall[0:2])\n",
             output="[44, 41, 37]\n[48, 48]", note="A slice is a new list. The end is left out: `[0:2]` takes 0 and 1. "
             "An empty end runs to the edge."),
        dict(concept="`sorted(wall)` versus `wall.sort()`",
             code="wall = [46, 41, 44]\nprint(sorted(wall))\nprint(wall)\nx = wall.sort()\nprint(x)\n",
             output="[41, 44, 46]\n[46, 41, 44]\nNone",
             note="`sorted()` hands back a sorted copy and leaves `wall` alone. `.sort()` sorts `wall` itself and "
             "hands back `None`: nothing comes back."),
        dict(concept="Error: no such position", code="wall = [48, 47, 46]\nprint(wall[3])\n",
             note="IndexError: list index out of range. Three items sit at positions 0, 1 and 2. For the last item, "
             "use `[-1]`, never `[len(wall)]`."),
        dict(concept="Error: round brackets after a list", code="wall = [48, 47, 46]\nprint(wall(0))\n",
             note="TypeError: 'list' object is not callable. Read a list with square brackets: `wall[0]`."),
        dict(concept="Error: a missing comma", code="wall = [48 47]\n",
             note="SyntaxError: invalid syntax. Perhaps you forgot a comma? Inside a list, items are separated by "
             "commas."),
        dict(concept="Error: `.sort()` handed back nothing", code="wall = [46, 41]\nx = wall.sort()\nprint(x[0])\n",
             note="TypeError: 'NoneType' object is not subscriptable. `x` holds `None`: nothing came back. Use "
             "`sorted(wall)`."),
        dict(concept="(extra) `.count()`", code="wall = [48, 48, 47]\nprint(wall.count(48))\n", output="2",
             note="How many items are 48. `len()` counts them all. (Extra practice: Reading the Wall)"),
        dict(concept="(extra) `.insert()` and `.pop()`",
             code="wall = [48, 46]\nwall.insert(1, 47)\nnewest = wall.pop()\nprint(wall)\nprint(newest)\n",
             output="[48, 47]\n46", note="`.insert(position, value)` squeezes an item in. `.pop()` takes the last item "
             "off and hands it back. (Lesson: More List Tools)"),
        dict(concept="(extra) `.remove()` and `in`",
             code="wall = [48, 99, 47]\nprint(99 in wall)\nwall.remove(99)\nprint(wall)\n", output="True\n[48, 47]",
             note="`.remove()` takes a value, not a position. `in` asks: is it there?"),
        dict(concept="(extra) `max()`, `min()`, `sum()`",
             code="wall = [41, 46, 39]\nprint(max(wall))\nprint(min(wall))\nprint(sum(wall))\n",
             output="46\n39\n126", note="The biggest, the smallest, and the total, wherever they sit."),
        dict(concept="(extra) A tuple: `( )`", code='hero = ("Lucky", 26)\nname, mana = hero\nprint(name)\nprint(mana)\n',
             output="Lucky\n26", note="Like a list that can't change. Two names on the left unpack it, in order. "
             "(Article: Tuples)"),
        dict(concept="(extra) Pair two lists: `zip()`",
             code='heroes = ["Oogrish", "Lucky"]\nmanas = [18, 26]\nprint(list(zip(heroes, manas)))\n',
             output="[('Oogrish', 18), ('Lucky', 26)]", note="First with first, second with second. Wrap it in "
             "`list()` to see the pairs. (Article: zip())"),
    ],
    notes=(
        "Cheatsheet 3 (the spec's entries in order, then the error rows and the extras from the optional items). "
        "Entries with `output` are run and checked by the harness; error entries have none. Code lines keep to 36 "
        "characters (the slice entry shows the real wall as `wall`, 35 characters). The recipe entry uses only "
        "Unit 3's planned def / return."
    ),
)


ITEMS = [
    TUPLES_ARTICLE,
    ZIP_ARTICLE,
    PROJECT_3P2,
    CHALLENGE_ONE_LIST,
    QC3_A,
    QC3_A_QUESTIONS,
    QC3_B,
    QC3_B_QUESTIONS,
    CHALK_NOTES_3,
]
