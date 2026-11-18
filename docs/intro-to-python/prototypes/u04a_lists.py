"""Unit 4 "Lists", part a: Mar'tu remembers (3a-remembers), Lesson 3A "Many Values, One Name",
Mar'tu remembers (3b-remembers), Lesson 3B "Reading the Wall Closely" and Quiz 3.

Spec: design/curriculum.md, "## Unit 4 · Lists", items 1 to 3 (3a-remembers; 3A-01, 3A-02, 3A-03 with 3A-04,
3A-05 with 3A-08, 3A-06, 3A-07, 3A-09, 3A-10, 3A-S; 3b-remembers; 3B-01 to 3B-03, 3B-S; Quiz 3).
Introduces node:List (3A-02), node:Subscript and op:USub (3A-03), attr:append (3A-05), call:len (3A-06),
call:range and call:list (3B-01), node:Slice (3B-02), call:sorted and attr:sort (3B-03).
Recipes (def / return) come from Unit 3 (u03a, written at the same time): 3A-06, 3A-S and three warm-up or quiz
items use only a simple `def` with a parameter and `return`. No loops (Unit 6), no `in`, `max`, `sum`, tuples (u04b), and no
`None` written in code (u07b): `None` only ever appears as printed output.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`for member in party.members:` (a list the campaign walked down), the chalk wall gaps (Module 2, `chalk-wall`),
four dialogue options kept in four boxes (Module 1, `program-dialogue-options`), and the nested read
`caster["abilities"]["magical_affinity"]`. Campaign links are "you've seen this, now you'll get it".
Every student has their own device; pair talk is optional and every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them, as Units 2 and 3): hints[0] Where to look (point),
the middle hints Teach me (a tiny example with other names), the last hint Show me how: the step's own line in
backticks (``Write `x = 1`.``), whose start up to its first `(` or `=` becomes Start me off. another_way, assemble
(More structure), then Compare. Where the start would hand over the step's decision (fix-a-mark's position), the
last hint's first code span has no `=`, so there is no Start me off.
In debug steps (3A-10, 3A-S, 3B-S) hints[0] is "Read Python's last line" (or the last line printed). The SOLOs
have no Assemble it: its pieces would set the fix beside the starter's slip, the SOLO's one decision.
Terminology (2.9): from Unit 4 on "variable" (Mar'tu may still say "box"); "recipe (function)",
"ingredient (parameter)" and "hands back (returns)" as in Unit 3; "gaps" / "shrink" for the chalk wall.

Check builders below (plain string templates; messages never repeat a student's own creative value):
  have_list()   NAME / LEFT / BARE: the list exists under the exact name, or the message says why not
  wall_value()  `chalk_wall` is the seven gaps: round brackets, no brackets, curly brackets, text, one number,
                the empty starter list, a list inside a list, quoted numbers, a missing gap, the wrong order
  follows()     CMB for lists: re-runs the student's program with another wall (or roster, or marks) swapped
                into the `name = [...]` line, inside the check only, and the printed line or the list must
                follow. Each failure is diagnosed (off by one, typed by hand, slice end left out, a whole row,
                a crash on a shorter wall, ...). A printed line counts when it holds the value as a whole word
                and is not a printed list, so `print(chalk_wall)` never passes for one gap, and a label passes
                (`print("Oldest gap:", chalk_wall[0])`). With `own=`, the student's own run must be right too,
                so a position that only fits the check's wall (`[4]` is the last of 5 gaps; `[2:5]`, the Learn
                pane's own example, is the last three of 5) fails with "On your wall ...".
  not_reset()   the student's line sits above the starter's `name = []`, which empties the list again
  recipe_par()  PAR / PAR-CONST / RET for `newest_mark(wall)`: called with three fresh walls the task never uses
                (one unsorted, so `min(wall)` fails). Values only, so `wall[-1]` and `wall[len(wall) - 1]` both
                pass. `None` is always "nothing came back". lean=True (the SOLO): the slip and the evidence, no fix
Rerun messages follow the plain-language guide 4.3 (as Units 2 and 3): what happened, then the one thing to try,
then the labelled evidence with no brackets, "Mar'tu tested your code with a test wall, `[60, 58, 55, 51, 46]`: it
printed `48`.", about 35 words or fewer. The other walls are 5, 6 and 8 gaps long, so a position typed for 7 gaps (`[6]`, `[4:7]`) fails fairly.
Mar'tu says so in the Learn pane (first-is-zero) before the first rerun message shows one. SOLO messages (solo-3a,
solo-3b) name the mistake and keep the evidence, with no fix. Goal-only steps' messages name the slip and
the tool, not the line to type.

Teacher ruling on the Unit 4 reviews (applied here): right answers sit in varied choice positions (the site
shuffles too); how-long is split (CP1 the plain `len - 1` line, CP2 the recipe, which accepts `[-1]` or `len`);
new-chalk-mark's joined list is `both_pages`; slice-the-wall's easier step comes first; sorted-or-sort is
goal-only; solo-3a is the quiet recipe slip; Quiz 3's bug is `wall[len(wall)]`; the check data uses invented
Tor-style names only (Pell, Brakka, Moss, Glug).

Phone width: fenced pictures, examples, predict code and quiz code keep lines to 36 characters or fewer. The one
exception is the real wall, `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` (41 characters), kept whole on one
line in editor code (starters, solutions) because a wrapped list in the very first list lesson reads as two
lists; quiz questions show it in the question text and keep it in `setup`. The teacher's recipe calls in
how-long and solo-3a keep their "# This should show 37" comment on the same line, as dictated (editor code).

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u04a
"""

# ---------------------------------------------------------------------------------------------
# The data
# ---------------------------------------------------------------------------------------------

WALL = [48, 48, 47, 46, 44, 41, 37]
WALL_LINE = "chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"
W5 = [60, 58, 55, 51, 46]  # another wall, 5 gaps: a typed position like [6] stops with IndexError
W6 = [60, 58, 55, 51, 46, 40]  # 6 gaps (3B-S)
W8 = [50, 49, 47, 44, 40, 35, 29, 22]  # 8 gaps (3A-S)
MIXED = [50, 31, 44, 39, 47]  # an unsorted wall (3B-03)
ROSTER_CODE = (
    "roster = [\n"
    '    ["Oogrish", 18],\n'
    '    ["Gearshift", 20],\n'
    '    ["Bomb Shell", 24],\n'
    '    ["Lucky", 26],\n'
    "]\n"
)
OTHER_ROSTER = [["Pell", 31], ["Brakka", 7], ["Moss", 15], ["Glug", 3]]
ROSTER_EV = "Mar'tu tested your code with a test roster of Pell 31, Brakka 7, Moss 15 and Glug 3"


def _ev(value, what="wall"):
    """The labelled evidence (plain-language guide 4.3.3): "Mar'tu tested your code with a test wall, `[60, 58]`"."""
    return "Mar'tu tested your code with a test %s, `%s`" % (what, value)


WALL_EV5 = _ev(W5)

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------

# Which names the student made, a near-miss test, and the namespace (same as Unit 2's _NAMES_PRE).
_NAMES_PRE = (
    "import ast as _ast\n"
    "_tree = _ast.parse(_source)\n"
    "_made = []\n"
    "for _n in _ast.walk(_tree):\n"
    "    _ts = _n.targets if type(_n).__name__ == 'Assign' else ([_n.target] if type(_n).__name__ == 'AugAssign' else [])\n"
    "    for _t in _ts:\n"
    "        if type(_t).__name__ == 'Name' and _t.id not in _made:\n"
    "            _made.append(_t.id)\n"
    "def _edits(_a, _b):\n"
    "    _row = list(range(len(_b) + 1))\n"
    "    for _i, _ca in enumerate(_a, 1):\n"
    "        _new = [_i]\n"
    "        for _j, _cb in enumerate(_b, 1):\n"
    "            _new.append(min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))\n"
    "        _row = _new\n"
    "    return _row[-1]\n"
    "def _close(_m, _w):\n"
    "    _a, _b = _m.lower(), _w.lower()\n"
    "    return _a.rstrip('s') == _b.rstrip('s') or _a.replace('_', '') == _b.replace('_', '') "
    "or (_a[:1] == _b[:1] and _edits(_a, _b) <= 2)\n"
    "_g = globals()\n"
)

# Lists the starters make: a missing one gets "Keep the list `x` from the starter".
STARTER_LISTS = [
    "chalk_wall", "roster", "old_marks", "new_marks", "both_pages", "d8_faces", "last_three", "first_two",
    "shortest_first", "newest_four", "oldest", "newest",
]


def have_list(name, *, kept=True, known=(), foreign=(), what="list"):
    """NAME + LEFT + BARE: the list (or box) `name` exists, or the message says why not."""
    code = _NAMES_PRE + (
        f"_name = {name!r}\n"
        f"_known = {list(known)!r}\n"
        f"_foreign = {list(foreign)!r}\n"
        "if _name not in _g:\n"
        "    _near = [_m for _m in _made if _m != _name and _m not in _known and _m not in _foreign and _close(_m, _name)]\n"
        "    _left = [_m for _m in _made if _m != _name and _m not in _known and any(_m == _f or _close(_m, _f) for _f in _foreign)]\n"
        "    _bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ in ('List', 'Constant', 'Tuple')]\n"
        "    if _near:\n"
        "        _msg = 'You wrote `' + _near[0] + '`, but the task needs `' + _name + '`. Python matches names letter for letter.'\n"
        "    elif _left:\n"
        "        _msg = ('`' + _left[0] + '` is a name from the Example or an earlier step. This task' + chr(39) + "
        f"'s {what} is named `' + _name + '`.')\n"
        "    elif _bare:\n"
        f"        _msg = 'Line ' + str(_bare[0]) + ' is a value with no name in front, so Python reads it and throws it away, "
        "like a phone number saved with no contact name. Put `' + _name + ' = ` in front of it.'\n"
        f"    elif {bool(kept)!r}:\n"
        f"        _msg = 'Python can' + chr(39) + 't find the {what} `' + _name + '`. Put back the line that starts `' + _name + ' = `, the way it was at the start.'\n"
        "    else:\n"
        f"        _msg = 'Python can' + chr(39) + 't find a {what} named `' + _name + '`. Make one: start a line with `' + _name + ' = `.'\n"
        "    assert False, _msg\n"
    )
    return (f"there is a {what} named {name}", code)


def wall_value(label="chalk_wall holds the seven gaps, in order", line=""):
    """`chalk_wall` is exactly the seven gaps, in order; otherwise the message names the slip. `line` adds
    "on line 1" style pointers for the broken spell."""
    at = (" " + line) if line else ""
    code = (
        "import ast as _ast\n"
        "_v = chalk_wall\n"
        f"_want = {WALL!r}\n"
        "_t = type(_v).__name__\n"
        "_as = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
        "and any(type(_x).__name__ == 'Name' and _x.id == 'chalk_wall' for _x in _n.targets)]\n"
        "_seg = (_ast.get_source_segment(_source, _as[-1].value) or '') if _as else ''\n"
        "assert not (_t == 'tuple' and _seg.lstrip().startswith('(')), ('Your gaps are inside parentheses `( )`, and '"
        f"'parentheses don' + chr(39) + 't make a list. Use square brackets{at}: `[48, 48, ...]`.')\n"
        f"assert _t != 'tuple', 'Your gaps have no square brackets around them, so they don' + chr(39) + 't make one list. "
        f"Put square brackets around them{at}: `[48, 48, ...]`.'\n"
        "assert _t not in ('set', 'dict'), "
        f"'Curly braces `{{ }}` make something else in Python, not a list. Use square brackets{at}: `[48, 48, ...]`.'\n"
        "assert _t != 'str', ('`chalk_wall` holds text, because of the quotes. Put the gaps between square '\n"
        "    'brackets, with no quotes.')\n"
        "assert _t not in ('int', 'float'), ('`chalk_wall` holds one number. Put all seven gaps between the square '\n"
        "    'brackets, with a comma between each two.')\n"
        "assert _t == 'list', '`chalk_wall` doesn' + chr(39) + 't hold a list. Put the gaps between square brackets: `[48, 48, ...]`.'\n"
        "_lone = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'List' and _n.value.elts]\n"
        "assert not (_v == [] and _lone), ('Line ' + str(_lone[0] if _lone else 0) + ' is a list with no name in front, so '\n"
        "    'Python reads it and throws it away. Put the gaps inside the square brackets of `chalk_wall = []` instead.')\n"
        "assert _v != [], ('`chalk_wall` is still empty: `[]`. Put the seven gaps between its square brackets, with a '\n"
        "    'comma between each two.')\n"
        "assert not (len(_v) == 1 and type(_v[0]).__name__ == 'list'), ('Your gaps are in a list inside another '\n"
        "    'list, because there are two pairs of square brackets. Use one pair: `[48, 48, ...]`.')\n"
        "_txt = [_x for _x in _v if type(_x).__name__ == 'str']\n"
        "assert not _txt, ('`\"' + (_txt[0] if _txt else '') + '\"` is text, because of the quotes. Gaps are numbers: '\n"
        "    'take the quotes off.')\n"
        "_dec = [_x for _x in _v if type(_x).__name__ == 'float']\n"
        "assert not _dec, ('`' + str(_dec[0] if _dec else '') + '` has a decimal point. The gaps are whole hours: '\n"
        "    'write `48`, not `48.0`.')\n"
        "assert len(_v) == 7, ('`chalk_wall` holds ' + str(len(_v)) + (' gap' if len(_v) == 1 else ' gaps') + '. '\n"
        "    'The wall has 7: 48, 48, 47, 46, 44, 41, 37.')\n"
        "assert _v != sorted(_want), ('Your gaps are smallest first. Keep the wall' + chr(39) + 's order, oldest first: '\n"
        "    'start with 48 and end with 37.')\n"
        "_bad = [_i for _i in range(7) if _v[_i] != _want[_i]]\n"
        "_nth = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']\n"
        "assert not _bad, ('The ' + (_nth[_bad[0]] if _bad else '') + ' gap is ' + str(_v[_bad[0]] if _bad else '') "
        "+ ', but the wall says ' + str(_want[_bad[0]] if _bad else '') + '. Check each gap against the wall.')\n"
    )
    return (label, code)


# CMB for lists: re-run the student's program with some `name = [...]` lines changed (a list literal, or the
# first line that sets the name). Prints go to a private buffer; the student's own code and values are never
# touched. `_hit(line, value)`: the line holds the value as a whole word and is not a printed list.
_RERUN_DEF = (
    "import ast as _ast, io as _io, sys as _sys, re as _re\n"
    f"_KEPT = {STARTER_LISTS!r}\n"
    "def _gone(_k):\n"
    "    if _k in _KEPT:\n"
    "        return 'Python can' + chr(39) + 't find the list `' + _k + '`. Put back the line that starts `' + _k + ' = `, the way it was at the start.'\n"
    "    return 'Python can' + chr(39) + 't find a list named `' + _k + '`. Make one: start a line with `' + _k + ' = `.'\n"
    "def _rerun(_changes, _drop=()):\n"
    "    _tree = _ast.parse(_source)\n"
    "    # Top-level lines that call a recipe in _drop are left out of the rerun, so only the plain lines print.\n"
    "    _tree.body = [_n for _n in _tree.body if type(_n).__name__ == 'FunctionDef' or not any("
    "type(_c).__name__ == 'Call' and type(_c.func).__name__ == 'Name' and _c.func.id in _drop "
    "for _c in _ast.walk(_n))]\n"
    "    _found = []\n"
    "    _sets = {}\n"
    "    for _n in _tree.body:\n"
    "        if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name' "
    "and _n.targets[0].id in _changes:\n"
    "            _sets.setdefault(_n.targets[0].id, []).append(_n)\n"
    "    for _k, _ns_ in _sets.items():\n"
    "        _lit = [_n for _n in _ns_ if type(_n.value).__name__ in ('Constant', 'List')]\n"
    "        for _n in (_lit or _ns_[:1]):\n"
    "            _n.value = _ast.parse(repr(_changes[_k]), mode='eval').body\n"
    "            _found.append(_k)\n"
    "    _ast.fix_missing_locations(_tree)\n"
    "    _ns = {'__name__': '__main__', 'input': lambda *_a: ''}\n"
    "    _keep = _sys.stdout\n"
    "    _sys.stdout = _io.StringIO()\n"
    "    _err = ''\n"
    "    try:\n"
    "        exec(compile(_tree, 'main.py', 'exec'), _ns)\n"
    "    except Exception as _x:\n"
    "        _err = type(_x).__name__ + ': ' + str(_x)\n"
    "    finally:\n"
    "        _out = _sys.stdout.getvalue()\n"
    "        _sys.stdout = _keep\n"
    "    return _ns, [_l.strip() for _l in _out.splitlines() if _l.strip()], _found, _err\n"
    "def _hit(_l, _v):\n"
    "    return '[' not in _l and bool(_re.search(r'(?<![\\w.-])' + _re.escape(str(_v)) + r'(?![\\w.])', _l))\n"
    "def _row(_l, _v):\n"
    "    return str(_v) in _l\n"
    "def _show(_ls, _most=2):\n"
    "    _ls = [_l.replace('`', chr(39)) for _l in _ls][:_most]\n"
    "    return 'nothing' if not _ls else ', '.join('`' + _l + '`' for _l in _ls[:-1]) + (' and ' if len(_ls) > 1 else '') + '`' + _ls[-1] + '`'\n"
    "def _sh(_v):\n"
    "    return '`' + str(_v).replace('`', chr(39)) + '`'\n"
    "def _ownl(_k):\n"
    "    _v = globals().get(_k)\n"
    "    return _v if type(_v).__name__ == 'list' and len(_v) > 1 else None\n"
    "def _plain(_k):\n"
    "    # True when the last line that sets _k reads no list by name: its values were typed in.\n"
    "    _as = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 "
    "and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == _k]\n"
    "    if not _as:\n"
    "        return False\n"
    "    _fn = [id(_c.func) for _c in _ast.walk(_as[-1].value) if type(_c).__name__ == 'Call']\n"
    "    return not any(type(_m).__name__ == 'Name' and id(_m) not in _fn for _m in _ast.walk(_as[-1].value))\n"
    "_W0 = _ownl('chalk_wall')\n"
)


class Code(str):
    """A rule's fix written as a Python expression (for a fix that names something from the student's code)."""


def _lit(text):
    return str(text) if isinstance(text, Code) else repr(text)


def follows(label, changes, ok, rules=(), fix="", ev="", saw=None, crash=(), pre="", kind="wall", own=None, drop=()):
    """CMB. Re-runs the program with `changes` swapped in (inside the check only). `ok` must hold (an expression
    over _R = the rerun's names, _p = its printed lines, _said(v) = some rerun line shows v, _said0(v) = the
    student's own run showed v, _g0 = the student's own names, _W0 = the student's own `chalk_wall` or None).
    When it does not, the first matching rule (cond, fix, saw-or-None) gives the message: what happened and the fix,
    then `ev` + ": " + what the rerun showed + ".". `crash` rules (cond over _e, fix) explain a rerun that stopped.
    `own` = (cond, message expression): once the other wall passes, the student's OWN run must be right too, so a
    position counted for the check's wall (`[4]` is the last of 5 gaps, `[2:5]` the last three of 5) fails.
    `drop` = recipe names: top-level lines that call one are left out of the rerun, so a plain line is checked
    on its own (the recipe's printed line cannot pass for it)."""
    saw = saw or "'it printed ' + _show(_p)"
    rule_code = "".join(
        f"    if not _msg and ({cond}):\n        _msg = {_lit(f)} + ' ' + _ev_txt + ': ' + ({s or saw}) + '.'\n"
        for cond, f, s in rules
    )
    crash_code = "".join(
        f"    if not _msg and ({cond}):\n        _msg = {f!r} + ' ' + _ev_txt + (', and Python stopped: that {kind} doesn' "
        "+ chr(39) + 't have a position your code asked for.' if _e.startswith('IndexError') else ', and Python "
        "stopped with an error: ' + _e.split(':')[0] + '.')\n"
        for cond, f in crash
    )
    code = _RERUN_DEF + (
        f"_C = {changes!r}\n"
        f"_r, _p, _f, _e = _rerun(_C, {tuple(drop)!r})\n"
        "_R = _r.get\n"
        "_g0 = globals()\n"
        "_old = _lines()\n"
        f"_ev_txt = {ev!r}\n"
        "_miss = [_k for _k in _C if _k not in _f]\n"
        "assert not _miss or _miss[0] in _g0, _gone(_miss[0] if _miss else '')\n"
        "assert not _miss, (\"Mar'tu can't find a line that starts `\" + (_miss[0] if _miss else '') + \" = `. Keep that \" "
        f"\"line the way it was at the start: he tests your code by changing it to another {kind}.\")\n"
        "_said = lambda _v: any(_hit(_l, _v) for _l in _p)\n"
        "_said0 = lambda _v: any(_hit(_l, _v) for _l in _old)\n"
        "_rowp = lambda _v: any(_row(_l, _v) for _l in _p)\n"
        f"{pre}"
        # A crash after the wanted line (a later step's line that only fits 7 gaps) is that later step's
        # business: the output printed before the crash is checked first.
        f"if not ({ok}) and _e:\n"
        "    _msg = ''\n"
        f"{crash_code}"
        "    if not _msg:\n"
        f"        _msg = _ev_txt + ', and your code stopped with an error. Python said: ' + _e + '. Make your code work for any {kind}.'\n"
        "    assert False, _msg\n"
        f"if not ({ok}):\n"
        "    _msg = ''\n"
        f"{rule_code}"
        "    if not _msg:\n"
        f"        _msg = {fix!r} + ' ' + _ev_txt + ': ' + ({saw}) + '.'\n"
        "    assert False, _msg\n"
    )
    if own:
        code += f"assert ({own[0]}), {own[1]}\n"
    return (label, code)


def not_reset(name):
    """The class's NEWBOX habit, the other way round: the student's line sits ABOVE the starter's `name = []`,
    which then empties the list again."""
    return (
        f"{name} is not emptied again by a later line",
        "import ast as _ast\n"
        "_as = [_n for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 "
        f"and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == {name!r}]\n"
        "_empty = lambda _n: type(_n.value).__name__ == 'List' and not _n.value.elts\n"
        "_mine = [_n.lineno for _n in _as[:-1] if not _empty(_n)]\n"
        "assert not (_as and _empty(_as[-1]) and _mine), ('Line ' + str(_as[-1].lineno if _as else 0) + "
        f"' sets `{name} = []` again, after your line ' + str(_mine[-1] if _mine else 0) + ', so `{name}` ends up '\n"
        "    'empty. Delete line ' + str(_as[-1].lineno if _as else 0) + '.')",
    )


def printed_after(name, what):
    """The console shows the list as it ends up: `print(name)` runs after the change (`what`)."""
    return (
        f"the console shows {name} after the change",
        "import ast as _ast\n"
        f"_shown = str({name}) in _lines()\n"
        "_pr = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
        "and type(_n.func).__name__ == 'Name' and _n.func.id == 'print' "
        f"and any(type(_a).__name__ == 'Name' and _a.id == {name!r} for _a in _n.args)]\n"
        f"assert _shown or not _pr, 'Your `print({name})` runs before {what}, so the Console shows the old list. Move "
        f"{what} above `print({name})`.'\n"
        f"assert _shown, '`print({name})` is missing, so the Console can' + chr(39) + 't show the list. Put `print({name})` "
        "back at the bottom.'",
    )


def meta(**fields):
    """The §2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


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
        "A [[list]] keeps many values under one name, in order, like a data set in math class.\n"
        "My chalk wall holds seven numbers. I could give each one its own box. I could also lose my mind, yes?\n"
        "You have met a list already: `party.members` held the four of you, in order, under one name. "
        "Tonight we read a list closely, one position at a time."
    ),
    goals=[
        "Keep many values in one [[list]], in order, with square brackets and commas",
        "Read an item by its [[index|position]], counting from 0 like a ruler, or counting from the end",
        "Change one item by its position, add an item to the end, and join two lists",
        "Count the items in a list, and find the last one",
        "Read a list inside a list: the row first, then the item in that row",
        "Count with `range()`, copy part of a list with a [[slice]], and make a sorted copy",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="list",
        aliases=["lists"],
        plain=(
            "Many values kept in order under one name, like a data set in math class. Square brackets hold the "
            "list, and a comma goes between each two items."
        ),
        example="marks = [9, 8, 7]",
    ),
    dict(
        term="index",
        aliases=["indexes", "indices", "position", "positions"],
        plain=(
            "An item's place in a list. Positions count from 0, like a ruler, so `[0]` is the first item. `[-1]` "
            "counts from the end: the last item."
        ),
        example="marks[0]",
    ),
    dict(
        term="IndexError",
        aliases=["index error", "list index out of range"],
        plain=(
            "The error Python shows when you ask for a position the list doesn't have. A list of 7 items has "
            "positions 0 to 6, so `[7]` is out of range."
        ),
        example="IndexError: list index out of range",
    ),
    dict(
        term="append",
        aliases=[".append()", "append()", "appends"],
        plain=(
            "Adds one item to the end of a list, the way an appendix goes at the end of a book. It changes the "
            "list itself and hands back nothing."
        ),
        example="marks.append(6)",
    ),
    dict(
        term="len()",
        aliases=["len", "length"],
        plain=(
            "Counts the items in a list. The last position is always one less than `len()`, because positions "
            "count from 0."
        ),
        example="len(marks)",
    ),
    dict(
        term="list inside a list",
        aliases=["lists inside lists", "nested list", "nested lists"],
        plain=(
            "A list whose items are lists. Read it like a theater ticket: the row first, then the seat in that "
            "row: `seats[3][1]`."
        ),
        example="seats[3][1]",
    ),
    dict(
        term="range()",
        aliases=["range"],
        plain=(
            "Counts from a start number and stops before the stop number: `range(1, 7)` gives 1 to 6. "
            "`list(range(1, 7))` turns the count into a list."
        ),
        example="list(range(1, 4))",
    ),
    dict(
        term="slice",
        aliases=["slices", "slicing"],
        plain=(
            "A copy of part of a list, like an excerpt from a poem. `[2:5]` copies positions 2, 3 and 4: the end "
            "is left out, and the list itself doesn't change."
        ),
        example="marks[-3:]",
    ),
    dict(
        term="sorted()",
        aliases=["sorted", ".sort()", "sort()", "sort"],
        plain=(
            "`sorted(marks)` hands back a sorted copy, smallest first, and leaves `marks` as it is. "
            "`marks.sort()` sorts the list itself and hands back nothing."
        ),
        example="low_first = sorted(marks)",
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (3a-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_3A = dict(
    kind="quiz",
    id="3a-remembers",
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from Units 1 and 3, before you start lists. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 3A. Q1 is the def/return item (Unit 3, the "
        "def/return exercise; from Unit 4 on one warm-up item is always def/return, 2.1). Its distractor 11 is the "
        "class's 'add the code's constants' trace (A-03, A-04: 9 + 2). Q2 is the 1C trace "
        "(`mana = mana - 5`). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="double-nine",
            q="What will this print?",
            code="def double(n):\n    return n * 2\n\nprint(double(9))\n",
            choices=["9", "11", "18", "n * 2"],
            answer="18",
            explain=(
                "The call hands over 9, so inside the recipe `n` is 9. The recipe works out `9 * 2` and hands back "
                "18. `print` shows what came back."
            ),
        ),
        dict(
            type="predict",
            id="mana-minus-five",
            q="What will this print?",
            code="mana = 18\nmana = mana - 5\nprint(mana)\n",
            choices=["18", "13", "-5", "mana - 5"],
            answer="13",
            explain=(
                "Python works out the right side first, with what's in the box now: 18 − 5 is 13. Then 13 goes "
                "back in the box, in place of the 18."
            ),
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 3A "Many Values, One Name"
# ---------------------------------------------------------------------------------------------

# 3A-01 ------------------------------------------------------------------------------------------

STORE_STARTER = "hour_1 = 48\n# Store the other six gaps too.\n# Any way you like. Then press Run.\n"

HOW_WOULD_YOU_STORE_IT = dict(
    id="how-would-you-store-it",
    title="How would you store it?",
    martu=(
        "Store the seven gaps from my chalk wall in your code, any way you like. A *gap* is the hours between "
        "two bursts, the blasts from the leylines. I chalk each gap on my wall as a *mark*. Oldest first:\n"
        "```text\n48  48  47  46  44  41  37\n```\n"
        "In Unit 1 you kept one number in one box (a variable). Line 1, `hour_1 = 48`, keeps the first gap. "
        "It's done for you.\n"
        "Try for two minutes, then press Run. There's no wrong try here, yes? If Python stops with an error, "
        "that's a try too. Read what the Console says, then try one variable per gap."
    ),
    names=["hour_1"],
    starter=STORE_STARTER,
    checkpoints=[
        dict(
            id="run-a-try",
            text=(
                "Two moves:\n"
                "1. On line 4, under the two notes, type a way to keep the other six gaps. Any way you like.\n"
                "2. Press Run. If Python stops with an error, read the error in the Console and try again."
            ),
            dictated=False,
            hints=[
                "Look at line 1: `hour_1 = 48` keeps one gap in one box. If Python stopped, read the error in the "
                "Console. Its title says what went wrong.",
                "A box (a variable) keeps one value under one name. What would you name the box for the second gap?",
                "One box per gap works: `night_1 = 9`, then `night_2 = 8`, and so on. Seven gaps, seven lines.",
                "Write `hour_2 = 48` under `hour_1 = 48`, then one line for each gap after it, down to `hour_7 = 37`.",
            ],
            checks=[
                (
                    "ran a try",
                    "assert _source.strip(), 'Your code is empty. Type a way to keep the gaps, even only `hour_1 = 48`, "
                    "then press Run.'",
                ),
            ],
            pass_line=(
                "You kept the gaps your way. Mar'tu: Look, one name can hold all seven: "
                "`chalk_wall = [48, 48, 47, 46, 44, 41, 37]`. That's a list. In the next exercise, you make it."
            ),
        ),
    ],
    solution="hour_1 = 48\nhour_2 = 48\nhour_3 = 47\nhour_4 = 46\nhour_5 = 44\nhour_6 = 41\nhour_7 = 37\n",
    starter_passes=True,
    another_way=[
        dict(
            angle="picture",
            label="Seven boxes or one list",
            text=(
                "```text\nseven boxes:\n hour_1  hour_2  ...  hour_7\n [48]    [48]    ...  [37]\n\n"
                "one list:\n chalk_wall\n [48, 48, 47, 46, 44, 41, 37]\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Like a shopping list",
            text=(
                "You could write each thing to buy on its own scrap of paper. Or you could write one list, in "
                "order, on one page. Same things. One is easier to carry."
            ),
        ),
        dict(
            angle="shorter",
            text="Any try is fine. Seven boxes work. The next exercise shows a shorter way.",
        ),
    ],
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='option_1 = "Write option 1 here"\noption_2 = "Write option 2 here"',
        why=(
            "You've seen this. In Module 1, the four dialogue options lived in four boxes, `option_1` to "
            "`option_4`. Four boxes was fine. For seven gaps, or a hundred, one list is better."
        ),
    ),
    takeaway="Seven boxes can hold seven gaps. A list holds them all under one name.",
    wrong_answers=[
        dict(why="empty editor, nothing tried", code="", fails_at=1, message_contains="press Run"),
        dict(why="the row copied as shown on the wall: numbers with spaces, no commas or brackets",
             code=STORE_STARTER + "hours = 48 48 47 46 44 41 37\n", fails_at=0, message_contains="SyntaxError"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-make", solo="false", dictates="", foreign_names="night_1,night_2",
             stages="PF") + "\n"
        "Productive-failure hook (PF, two minutes, ungraded): `hour_1 = 48` is pre-typed (G1 R29), so Run "
        "passes at once. Mar'tu says a Python stop counts as a try (read the last line, then one box per gap); the "
        "row copied as shown (`hours = 48 48 47 ...`) is the SyntaxError that sentence is for. Skipped on frustration signals (site behavior, not in the prototype). Mar'tu sets the "
        "attempt beside a list in the pass line. Any attempt, even the starter, passes: the check only needs code "
        "in the editor that ran without an error."
    ),
)

# 3A-02 ------------------------------------------------------------------------------------------

MAKE_STARTER = "# Put the seven gaps in, in order.\nchalk_wall = []\nprint(chalk_wall)\n"
MAKE_SOLUTION = "# Put the seven gaps in, in order.\n" + WALL_LINE + "print(chalk_wall)\n"
MAKE_FOREIGN = ["party_colors", "marks", "hour_1", "hour_2"]


def _make(wall_line):
    return "# Put the seven gaps in, in order.\n" + wall_line + "\nprint(chalk_wall)\n"


MAKE_THE_WALL = dict(
    id="make-the-wall",
    title="Make the wall",
    martu=(
        "A [[list]] keeps many values under one name, in order. In math class, a data set is a group of numbers "
        "you study together. A list is Python's data set: square brackets `[ ]` around it, and a comma between "
        "each two items. `marks = [46, 44, 41]` is a list of three items.\n"
        "In math class, square brackets can group numbers, like parentheses. In Python they never group math. "
        "They make a list.\n"
        "Numbers in a list get no quotes. Text keeps its quotes, like `[\"gold\", \"teal\"]` in the Example.\n"
        "```text\n chalk_wall = [48, 48, 47, ...]\n             ^   ^   ^\n   square bracket  commas\n```"
    ),
    introduces=["node:List"],
    example='party_colors = ["gold", "teal"]\nprint(party_colors)\n',
    example_output="['gold', 'teal']",
    names=["chalk_wall"],
    predict=dict(
        q="What will this print?",
        code="marks = [46, 44, 41]\nprint(marks)\n",
        choices=["46, 44, 41", "46 44 41", "marks", "[46, 44, 41]"],
        answer=3,
        explain=(
            "`print` shows the whole list, square brackets and commas too. Text in a list shows with single quotes "
            "`'`, like the Example's `['gold', 'teal']`. That's Python's own way of showing text in a list."
        ),
    ),
    pair_talk=(
        "Pair talk: read your list out loud to your partner, and say \"comma\" at every comma. Did you both count "
        "six commas? Then each of you presses Run on your own screen."
    ),
    starter=MAKE_STARTER,
    checkpoints=[
        dict(
            id="seven-gaps",
            text=(
                "Put the seven gaps between the square brackets of `chalk_wall = []` on line 2, oldest first: "
                "48 48 47 46 44 41 37. Put a comma between each two."
            ),
            dictated=False,
            hints=[
                "Look at the Example, `[\"gold\", \"teal\"]`. What goes between the two items? Put the same thing "
                "between each two gaps.",
                "A list is square brackets with a comma between each two items: `[5, 9, 2]`. Numbers get no quotes.",
                "Write `chalk_wall = [48, 48, 47, 46, 44, 41, 37]` in place of `chalk_wall = []`.",
            ],
            checks=[
                have_list("chalk_wall", known=["chalk_wall"], foreign=MAKE_FOREIGN),
                not_reset("chalk_wall"),
                wall_value(),
            ],
            pass_line="Your list holds all seven gaps. Mar'tu: Seven gaps, one name. My wall, in Python. Good.",
        ),
    ],
    solution=MAKE_SOLUTION,
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "print(chalk_wall)"],
        distractors=[
            "chalk_wall = [48 48 47 46 44 41 37]",
            'chalk_wall = "48, 48, 47, 46, 44, 41, 37"',
            "chalk_wall = (48, 48, 47, 46, 44, 41, 37)",
        ],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="A shelf of jars",
            text=(
                "Picture a shelf with seven jars in a row. The shelf has one name: `chalk_wall`. Each jar holds "
                "one gap. The order on the shelf is the order on the wall."
            ),
        ),
        dict(
            angle="picture",
            label="The wall as a list",
            text=(
                "```text\nchalk wall    48 48 47 46 44 41 37\n"
                "               |  |  |  |  |  |  |\nPython      [48,48,47,46,44,41,37]\n```\n"
                "Same numbers, same order. Square brackets at the ends, commas in between."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "I wrote each gap under the last, oldest at the top. Python reads a list left to right, oldest "
                "first. Same idea, turned on its side."
            ),
        ),
        dict(
            angle="English class",
            label="From English class",
            text=(
                "In English, a series uses commas: 48, 48, 47 and 46. A Python list uses commas too, but no *and*, "
                "and it has square brackets at both ends: `[48, 48, 47, 46]`."
            ),
        ),
        dict(
            angle="shorter",
            text="`[`, the gaps with commas between, `]`. No quotes.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="A heading for Lucky",
        text=(
            "Lucky wants a heading. Add one line that shows `Gaps: ` and then the whole wall. Glue them with `+`, "
            "and turn the list into text first with `str()`."
        ),
        hints=[
            "`+` glues only text to text. `str(chalk_wall)` turns the list into text first.",
            "Write `print(\"Gaps: \" + str(chalk_wall))` on a new line at the bottom.",
        ],
        checks=[
            (
                "prints Gaps: and the wall from the list",
                "import ast as _ast\n"
                "_prints = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
                "and type(_n.func).__name__ == 'Name' and _n.func.id == 'print']\n"
                "_strs = [_n for _p in _prints for _n in _ast.walk(_p) if type(_n).__name__ == 'Call' "
                "and type(_n.func).__name__ == 'Name' and _n.func.id == 'str' "
                "and any(type(_a).__name__ == 'Name' and _a.id == 'chalk_wall' for _a in _n.args)]\n"
                "assert _strs, 'Your line doesn' + chr(39) + 't glue the list itself. Use `str(chalk_wall)`, so the "
                "line changes when the wall changes: `\"Gaps: \" + str(chalk_wall)`.'\n"
                "assert ('Gaps: ' + str(chalk_wall)) in _lines(), "
                "'The Console doesn' + chr(39) + 't show `Gaps: ` and the wall on one line. Write "
                "`print(\"Gaps: \" + str(chalk_wall))`.'",
            ),
        ],
        solution=MAKE_SOLUTION + 'print("Gaps: " + str(chalk_wall))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="for member in party.members:",
        why=(
            "You've seen this line three times in Module 2. `party.members` is a list: the four heroes, in "
            "order, under one name. The `for` line went down it, one hero at a time. You'll write loops like that "
            "in Unit 6."
        ),
    ),
    takeaway="A list: `[48, 48, 47]`. Square brackets, commas between the items, no quotes for numbers.",
    wrong_answers=[
        dict(why="starter unchanged: the empty list", code=MAKE_STARTER, fails_at=1, message_contains="still empty"),
        dict(why="no commas (spec)", code=_make("chalk_wall = [48 48 47 46 44 41 37]"), fails_at=0,
             message_contains="forgot a comma"),
        dict(why="one comma missing", code=_make("chalk_wall = [48, 48 47, 46, 44, 41, 37]"), fails_at=0,
             message_contains="forgot a comma"),
        dict(why="quoted numbers (spec)", code=_make('chalk_wall = ["48", "48", "47", "46", "44", "41", "37"]'),
             fails_at=1, message_contains="numbers"),
        dict(why="the whole wall as one piece of text", code=_make('chalk_wall = "48, 48, 47, 46, 44, 41, 37"'),
             fails_at=1, message_contains="holds text"),
        dict(why="round brackets instead of square ones", code=_make("chalk_wall = (48, 48, 47, 46, 44, 41, 37)"),
             fails_at=1, message_contains="square brackets"),
        dict(why="no brackets at all (makes a tuple)", code=_make("chalk_wall = 48, 48, 47, 46, 44, 41, 37"),
             fails_at=1, message_contains="square brackets"),
        dict(why="curly brackets", code=_make("chalk_wall = {48, 48, 47, 46, 44, 41, 37}"), fails_at=1,
             message_contains="Curly"),
        dict(why="gaps typed inside the starter's brackets: a list inside a list",
             code=_make("chalk_wall = [[48, 48, 47, 46, 44, 41, 37]]"), fails_at=1, message_contains="inside another"),
        dict(why="a gap left out", code=_make("chalk_wall = [48, 47, 46, 44, 41, 37]"), fails_at=1,
             message_contains="holds 6 gaps"),
        dict(why="smallest first instead of the wall's order", code=_make("chalk_wall = [37, 41, 44, 46, 47, 48, 48]"),
             fails_at=1, message_contains="order"),
        dict(why="digits swapped in one gap", code=_make("chalk_wall = [48, 48, 47, 64, 44, 41, 37]"), fails_at=1,
             message_contains="The 4th gap is 64"),
        dict(why="the example's list name copied", code="party_colors = [48, 48, 47, 46, 44, 41, 37]\nprint(party_colors)\n",
             fails_at=1, message_contains="example"),
        dict(why="capital C", code="Chalk_wall = [48, 48, 47, 46, 44, 41, 37]\nprint(Chalk_wall)\n", fails_at=1,
             message_contains="letter for letter"),
        dict(why="seven boxes from 3A-01, the list left empty",
             code="hour_1 = 48\nhour_2 = 48\nhour_3 = 47\nchalk_wall = []\nprint(chalk_wall)\n", fails_at=1,
             message_contains="still empty"),
        dict(why="a list with no name", code="[48, 48, 47, 46, 44, 41, 37]\nprint(chalk_wall)\n", fails_at=0,
             message_contains="not defined"),
        dict(why="a variable is just its value (B-02/B-03): the list typed on its own line under `chalk_wall = []`",
             code="# Put the seven gaps in, in order.\nchalk_wall = []\n[48, 48, 47, 46, 44, 41, 37]\nprint(chalk_wall)\n",
             fails_at=1, message_contains="no name"),
        dict(why="the list typed above the starter's `chalk_wall = []`, which empties it again",
             code="# Put the seven gaps in, in order.\n" + WALL_LINE + "chalk_wall = []\nprint(chalk_wall)\n",
             fails_at=1, message_contains="again"),
        dict(why="decimal gaps", code=_make("chalk_wall = [48.0, 48.0, 47.0, 46.0, 44.0, 41.0, 37.0]"), fails_at=1,
             message_contains="whole hours"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="list-make", solo="false", dictates="",
             foreign_names=",".join(MAKE_FOREIGN)) + "\n"
        "Spec catches: no commas -> Python's own 'Perhaps you forgot a comma?' (the site's explainer row extends to "
        "`[ ]`: 'Inside a list, items are separated by commas'); quoted numbers -> 'These are text. Gaps are "
        "numbers: no quotes.' Added from the class's slips: round brackets and no brackets (both make a tuple), "
        "curly brackets, gaps typed inside the starter's `[]` (a list in a list), a missing gap, smallest-first "
        "order, the example's name (`party_colors`, LEFT; G2 copies example names: A-05, A-07, A-08). "
        "The Example uses `party_colors = [\"gold\", \"teal\"]` (spec: `[\"gold\", \"fire orange\"]`, shortened to "
        "fit a phone line). Starter comment moved above the line (phone width). BQ (combining list + glue): "
        "`print(\"Gaps: \" + str(chalk_wall))`. AW: everyday (jars), picture (the wall), in Tor, shorter."
    ),
)

# 3A-03 (absorbs 3A-04) --------------------------------------------------------------------------

ZERO_STARTER = WALL_LINE + "# 1. Print the oldest gap.\n\n# 2. Newest, then the one before.\n\n"


def _zero(first="print(chalk_wall[0])", newest="print(chalk_wall[-1])\nprint(chalk_wall[-2])"):
    return WALL_LINE + "# 1. Print the oldest gap.\n" + first + "\n# 2. Newest, then the one before.\n" + newest + "\n"


ZERO_FOREIGN = ["party_colors", "colors"]
_W = "_C['chalk_wall']"
_MINE = "_g0.get('chalk_wall')"

# A printed line that is a list: the whole wall, or a one-item slice like `[0:1]` (still a list, brackets and all).
WHOLE_LIST = ("any(_l == str(_C['chalk_wall']) for _l in _p)", "'it printed the whole list'")
SOME_LIST = ("any('[' in _l for _l in _p)", "'it printed a list, with square brackets'")
# Every gap printed (a loop down the wall, or one line per position): the middle gaps the task never prints show.
EVERY_GAP = f"_said({_W}[1]) and _said({_W}[2]) and _said({_W}[3])"

OLDEST_CHECK = follows(
    "the oldest gap follows the wall (position 0)",
    {"chalk_wall": W5},
    f"_said({_W}[0]) and not ({EVERY_GAP})",
    rules=[
        (EVERY_GAP, "Your code shows every gap. Show only the oldest one, at position 0: `chalk_wall[0]`.",
         "'it printed every gap'"),
        (f"_said({_W}[1])", "Your line reads position 1, the second gap. Positions start at 0, so the oldest gap "
         "is at position 0: `chalk_wall[0]`.",
         f"'it printed `' + str({_W}[1]) + '`, the second gap'"),
        (f"_said({_MINE}[0])",
         "You typed the gap instead of reading it from the list. Read it by its position: `chalk_wall[0]`.",
         f"'it still printed `' + str({_MINE}[0]) + '`'"),
        (WHOLE_LIST[0], "Your line shows the whole list. Show one gap, the one at position 0: `chalk_wall[0]`.",
         WHOLE_LIST[1]),
        (SOME_LIST[0], "The colon in your square brackets makes a list of gaps, not one gap. Put only the position "
         "in the brackets: `chalk_wall[0]`.", SOME_LIST[1]),
    ],
    fix="Your code doesn't show the oldest gap yet. Read it at position 0: `chalk_wall[0]`.",
    ev=WALL_EV5,
    crash=[
        (EVERY_GAP, "Your code shows every gap, one position at a time. Show only the oldest one: `chalk_wall[0]`."),
        ("_e.startswith('IndexError')", "The oldest gap is at position 0 on a wall of any length: `chalk_wall[0]`."),
    ],
    own=(
        "_W0 is None or _said0(_W0[0])",
        "'The oldest gap on your wall is ' + str(_W0[0]) + ', at position 0, but your Console shows ' + "
        "_show(_old, 3) + '. Use `chalk_wall[0]`.'",
    ),
)

NEWEST_CHECK = follows(
    "the newest two gaps follow the wall (counting from the end)",
    {"chalk_wall": W5},
    f"_said({_W}[-1]) and _said({_W}[-2])",
    rules=[
        (f"not _said({_W}[-1]) and _said({_MINE}[-1])",
         "You typed the newest gap instead of reading it from the list. `chalk_wall[-1]` is the last item of a wall "
         "of any length.",
         f"'it still printed `' + str({_MINE}[-1]) + '`'"),
        (f"not _said({_W}[-1])", "Your code doesn't show the newest gap yet. Show it with `chalk_wall[-1]`: the "
         "minus counts from the end.", None),
        (f"_said({_MINE}[-2])", "You typed the gap before the newest instead of reading it from the list. Count from "
         "the end for that one too.",
         f"'it still printed `' + str({_MINE}[-2]) + '`'"),
    ],
    fix="Your code shows the newest gap, but not the one before it. Show that one too, counting from the end.",
    ev=WALL_EV5,
    crash=[("_e.startswith('IndexError')",
            "Your positions fit only 7 gaps. Count from the end with a minus, so they fit a wall of any length.")],
    own=(
        "_W0 is None or (_said0(_W0[-1]) and _said0(_W0[-2]))",
        "'On your wall the newest gap is ' + str(_W0[-1]) + ' and the one before it is ' + str(_W0[-2]) + ', but "
        "your Console shows ' + _show(_old, 3) + '. Count from the end, with a minus.'",
    ),
)

FIRST_IS_ZERO = dict(
    id="first-is-zero",
    title="The first is zero",
    martu=(
        "Each item in a list has a position, its [[index]]. Positions count from 0, like a ruler: a ruler starts "
        "at 0, no steps from the start. So `chalk_wall[0]` is the oldest gap. A minus counts from the end: "
        "`chalk_wall[-1]` is the newest. The positions:\n"
        "```text\n 0  1  2  3  4  5  6\n48 48 47 46 44 41 37\n-7 -6 -5 -4 -3 -2 -1\n```\n"
        "As in English class, *seven* says how many and *seventh* says which one. The seventh gap is at position "
        "6. There is no position 7, and no `-0`.\n"
        "I test your code with other walls too, so read each gap by its position. Never type a number you see.\n"
        "Try it if you like (it's not a step): add `print(chalk_wall[7])` and press Run. You'll see an "
        "[[IndexError]]. Then delete that line."
    ),
    introduces=["node:Subscript", "op:USub"],
    example='party_colors = ["gold", "teal"]\nprint(party_colors[0])\nprint(party_colors[-1])\n',
    example_output="gold\nteal",
    names=["chalk_wall"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code=WALL_LINE + "print(chalk_wall[1])\nprint(chalk_wall[6])\n",
        choices=["48\n41", "48\n37", "47\n37", "48\n44"],
        answer=1,
        explain=(
            "Position 1 is the second gap. It's 48 too: the first two gaps match, so `[1]` looks right here by "
            "luck. Position 6 is the seventh gap, 37: the last position is one less than the count."
        ),
    ),
    pair_talk=(
        "Pair talk: tell your partner why the oldest gap is at position 0, not 1. Then each of you prints it on "
        "your own screen."
    ),
    starter=ZERO_STARTER,
    checkpoints=[
        dict(
            id="oldest",
            text=(
                "On line 3, under `# 1. Print the oldest gap.`, type `print(chalk_wall[0])`. You should see 48 in "
                "the Console."
            ),
            dictated=True,
            hints=[
                "Look at Mar'tu's picture. Which position number sits above the first 48, the oldest gap?",
                "Positions start at 0. In the Example, `party_colors[0]` is the first color, gold.",
                "Write `print(chalk_wall[0])` under the `# 1.` note.",
            ],
            checks=[
                have_list("chalk_wall", known=["chalk_wall"], foreign=ZERO_FOREIGN),
                OLDEST_CHECK,
                (
                    "reads the gap with square brackets",
                    "assert _uses('node:Subscript'), 'Your line doesn' + chr(39) + 't read from the list. Read the gap "
                    "from `chalk_wall` by its position, in square brackets: `chalk_wall[0]`.'",
                ),
            ],
            pass_line="You read the oldest gap at position 0. Mar'tu: Strange at first. Normal by Tuesday, yes?",
        ),
        dict(
            id="count-from-the-end",
            text=(
                "On line 5, under `# 2.`, show the newest gap, then the gap before it, one per line. Count from the "
                "end, with a minus."
            ),
            dictated=False,
            hints=[
                "Look at the bottom row of Mar'tu's picture: the minus numbers count from the end.",
                "`party_colors[-1]` is the last color, and `party_colors[-2]` is the one before it, on a list of any "
                "length.",
                "Write `print(chalk_wall[-1])` under the `# 2.` note, then `print(chalk_wall[-2])` under it.",
            ],
            checks=[
                NEWEST_CHECK,
                (
                    "counts from the end with a minus",
                    "assert _uses('op:USub'), \"This step practices counting from the end. Use a minus, like "
                    "`chalk_wall[-1]` in Mar'tu's words.\"",
                ),
            ],
            pass_line="You counted from the end. Gearshift: Newest, then the one before. The gap is shrinking. Visor dims.",
        ),
    ],
    solution=_zero(),
    partials=[_zero(newest="")],
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "print(chalk_wall[0])", "print(chalk_wall[-1])",
               "print(chalk_wall[-2])"],
        distractors=["print(chalk_wall[1])", "print(chalk_wall[7])", "print(48)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Jars numbered from 0",
            text=(
                "```text\njar:  0   1   2   3   4   5   6\n     [48][48][47][46][44][41][37]\n```\n"
                "The first jar's number is 0. Seven jars end at jar 6."
            ),
        ),
        dict(
            angle="everyday",
            label="A ruler starts at 0",
            text=(
                "Look at a ruler. The first number on it is 0, not 1. Position 0 means no steps from the start, and "
                "position 2 means two steps in: the third item."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "```text\nchalk_wall[0]   -> 48 (oldest)\nchalk_wall[1]   -> 48\nchalk_wall[6]   -> 37\n"
                "chalk_wall[7]   -> IndexError\nchalk_wall[-1]  -> 37 (newest)\nchalk_wall[-2]  -> 41\n```"
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Oogrish counts drills from the first stance, stance 0. Then one, two... He says the first one is "
                "only a warm-up. Python agrees with him."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="How much did it shrink?",
        text=(
            "Lucky wants the bad news: how much did the newest gap shrink? At the bottom, show the gap before the "
            "newest minus the newest gap."
        ),
        hints=[
            "The gap before the newest is the bigger one. Take the newest away from it.",
            "Write `print(chalk_wall[-2] - chalk_wall[-1])` on a new line at the bottom.",
        ],
        checks=[
            follows(
                "the shrink follows the wall",
                {"chalk_wall": W5},
                f"_said({_W}[-2] - {_W}[-1])",
                rules=[
                    (f"_said({_MINE}[-2] - {_MINE}[-1])",
                     "You typed the answer instead of the math. Read the gaps from the list: "
                     "`chalk_wall[-2] - chalk_wall[-1]`.", None),
                    (f"any(str({_W}[-1] - {_W}[-2]) in _l for _l in _p)",
                     "Your answer is below 0, because the subtraction is backwards. Take the newest gap away from "
                     "the one before it.", None),
                ],
                fix="Your code doesn't show the shrink yet. Show the gap before the newest minus the newest: "
                    "`chalk_wall[-2] - chalk_wall[-1]`.",
                ev=WALL_EV5,
            ),
        ],
        solution=_zero() + "print(chalk_wall[-2] - chalk_wall[-1])\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "You've seen this wall. Oogrish ran a finger down it, and the newest number, 37, was circled twice. In "
            "Python that's `chalk_wall[-1]`, and the oldest is `chalk_wall[0]`."
        ),
    ),
    takeaway="Positions start at 0: `wall[0]` is the first item. `wall[-1]` is the last, on a list of any length.",
    wrong_answers=[
        dict(why="starter unchanged: nothing printed", code=ZERO_STARTER, fails_at=1, message_contains="position 0"),
        dict(why="the value typed by hand (spec)", code=_zero(first="print(48)"), fails_at=1,
             message_contains="by its position"),
        dict(why="asks for item 1 to get the first (spec)", code=_zero(first="print(chalk_wall[1])"), fails_at=1,
             message_contains="Positions start at 0"),
        dict(why="the whole list printed", code=_zero(first="print(chalk_wall)"), fails_at=1, message_contains="whole list"),
        dict(why="position 7 for the newest: IndexError", code=_zero(newest="print(chalk_wall[7])"), fails_at=0,
             message_contains="out of range"),
        dict(why="round brackets: the list called like a recipe", code=_zero(first="print(chalk_wall(0))"), fails_at=0,
             message_contains="not callable"),
        dict(why="len(list) used as a position", code=_zero(newest="print(chalk_wall[len(chalk_wall)])"), fails_at=0,
             message_contains="out of range"),
        dict(why="a counted position for the newest: fits 7 gaps only",
             code=_zero(newest="print(chalk_wall[6])\nprint(chalk_wall[5])"), fails_at=2, message_contains="any length"),
        dict(why="the newest two typed by hand", code=_zero(newest="print(37)\nprint(41)"), fails_at=2,
             message_contains="typed the newest gap"),
        dict(why="only the newest, not the one before", code=_zero(newest="print(chalk_wall[-1])"), fails_at=2,
             message_contains="one before"),
        dict(why="-1 written as 1 from the end of the line: [1] and [2]",
             code=_zero(newest="print(chalk_wall[1])\nprint(chalk_wall[2])"), fails_at=2, message_contains="`chalk_wall[-1]`"),
        dict(why="-7 for the oldest: fits 7 gaps only", code=_zero(first="print(chalk_wall[-7])"), fails_at=1,
             message_contains="position 0"),
        dict(why="the wall line deleted, the positions kept", code="print(chalk_wall[0])\n", fails_at=0,
             message_contains="not defined"),
        dict(why="a position counted for the check's 5-gap wall: [-5] is the first of 5, not of 7",
             code=_zero(first="print(chalk_wall[-5])"), fails_at=1, message_contains="oldest gap on your wall is 48"),
        dict(why="[4] for the newest: the last of 5 gaps, not of 7", code=_zero(newest="print(chalk_wall[4])\nprint(chalk_wall[-2])"),
             fails_at=2, message_contains="newest gap is 37"),
        dict(why="every gap printed (a loop from Module 2), then the newest two",
             code=_zero(first="for gap in chalk_wall:\n    print(gap)"), fails_at=1, message_contains="every gap"),
        dict(why="a one-item slice: still a list", code=_zero(first="print(chalk_wall[0:1])"), fails_at=1,
             message_contains="makes a list of gaps"),
        dict(why="one print per position, 0 to 6: every gap (and IndexError on a shorter wall)",
             code=_zero(first="\n".join(f"print(chalk_wall[{i}])" for i in range(7))), fails_at=1,
             message_contains="one position at a time"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="list-index", solo="false", dictates="1,2",
             foreign_names=",".join(ZERO_FOREIGN)) + "\n"
        "3A-03 with 3A-04 (count-from-the-end) folded in as CP2. Predict (spec): `chalk_wall[1]` and "
        "`chalk_wall[6]`; the explain says `[1]` only looks right by luck (the first two gaps are both 48), "
        "which is why CP1 is checked on another wall (CMB, a 5-gap wall: `[1]` shows 58, `[6]` and `[7]` stop "
        "with IndexError). The `[7]` IndexError is the Learn pane's try-it (spec: 'then run chalk_wall[7] and read "
        "the IndexError'). TR (static table) = the step-by-step angle. Checks read printed lines as whole words, "
        "and a printed list never counts as one gap. BQ (combining index + subtraction): the shrink, checked on "
        "another wall. Campaign link: Module 2's chalk-wall story beat (part 9)."
    ),
)


# 3A-05 (absorbs 3A-08) --------------------------------------------------------------------------

MARK_TOP = WALL_LINE + "# 1. Append your guess.\n"
MARK_BOTTOM = "old_marks = [48, 48, 47, 46]\nnew_marks = [44, 41, 37]\n# 2. Join both pages with +.\n"
MARK_STARTER = MARK_TOP + "\nprint(chalk_wall)\n\n" + MARK_BOTTOM + "both_pages = []\nprint(both_pages)\n"
MARK_KNOWN = ["chalk_wall", "old_marks", "new_marks", "both_pages"]


def _mark(append="chalk_wall.append(33)", pages="both_pages = old_marks + new_marks", after=""):
    return MARK_TOP + append + "\nprint(chalk_wall)\n" + after + "\n" + MARK_BOTTOM + pages + "\nprint(both_pages)\n"


GUESS_CHECK = (
    "chalk_wall grows by your guess",
    "import ast as _ast\n"
    "_tree = _ast.parse(_source)\n"
    f"_base = {WALL!r}\n"
    "_v = chalk_wall\n"
    "assert _v is not None, ('`chalk_wall` now holds `None`, Python' + chr(39) + 's word for nothing. `.append()` '\n"
    "    'changes the list and hands back nothing, so `chalk_wall = ` threw the wall away. Write '\n"
    "    '`chalk_wall.append(...)` on a line of its own.')\n"
    "assert type(_v).__name__ == 'list', ('`chalk_wall` isn' + chr(39) + 't a list anymore. Keep it as the wall, a '\n"
    "    'list of gaps, and add your guess with `.append()`.')\n"
    "_lost = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp' "
    "and type(_n.value.op).__name__ == 'Add' and type(_n.value.left).__name__ == 'Name' "
    "and _n.value.left.id == 'chalk_wall']\n"
    "assert not (_lost and len(_v) < 8), ('Line ' + str(_lost[0] if _lost else 0) + ' makes a joined list with no '\n"
    "    'name in front, so Python reads it and throws it away, and `chalk_wall` doesn' + chr(39) + 't change. Use '\n"
    "    '`chalk_wall.append(...)` instead.')\n"
    "assert len(_v) >= 7 and _v[:7] == _base, ('The first seven gaps have changed. Put them back the way they were '\n"
    "    'on line 1. Your guess goes at the end.')\n"
    "assert len(_v) > 7, ('`chalk_wall` still has 7 gaps. Add your guess to the end: `chalk_wall.append(` and '\n"
    "    'your number `)`.')\n"
    "_g8 = _v[7]\n"
    "assert type(_g8).__name__ != 'str', 'Your guess is text, because of the quotes. Gaps are numbers: take the quotes off.'\n"
    "assert type(_g8).__name__ != 'list', ('Your guess went in as a list inside the wall, because of its square '\n"
    "    'brackets. Append the number itself, with no square brackets: `chalk_wall.append(` and your number `)`.')\n"
    "assert type(_g8).__name__ == 'int', 'Your guess isn' + chr(39) + 't a whole number. Use a whole number of hours, like `33`.'\n"
    "assert _g8 < 37, 'Your guess is 37 or more, but the gaps keep shrinking. Guess a number below 37.'\n"
    "assert _g8 > 0, 'Your guess is 0 or less, but a gap is some hours long. Guess a number above 0 and below 37.'\n"
    "_more = [_x for _x in _v[8:] if type(_x).__name__ != 'int']\n"
    "assert not _more, ('One of the gaps you added isn' + chr(39) + 't a whole number. Every gap on the wall is a '\n"
    "    'whole number, with no quotes.')",
)

APPEND_USED = (
    "the guess goes in with .append()",
    "import ast as _ast\n"
    "_app = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
    "and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'append' "
    "and type(_n.func.value).__name__ == 'Name' and _n.func.value.id == 'chalk_wall']\n"
    "assert _app, ('Your line makes a new list for `chalk_wall` instead of adding to it. This step practices '\n"
    "    '`.append()`: `chalk_wall.append(` and your guess `)`.')",
)

JOIN_CHECK = follows(
    "both_pages joins old_marks and new_marks, in order",
    {"old_marks": [50, 49], "new_marks": [45, 40, 36]},
    "_R('both_pages') == [50, 49, 45, 40, 36]",
    rules=[
        ("_R('both_pages') is None", "`both_pages` got `None`, Python's word for nothing, because `.append()` hands "
         "back nothing. Join the lists with `+` instead: `both_pages = old_marks + new_marks`.",
         "'`both_pages` became `None`'"),
        ("_R('both_pages') == [45, 40, 36, 50, 49]", "Your join puts the new marks first. Old marks go first: "
         "`old_marks + new_marks`.", None),
        ("_R('both_pages') == [[50, 49], [45, 40, 36]]", "Your line makes a list that holds two lists. `+` joins "
         "them into one list: `old_marks + new_marks`.", None),
        ("type(_R('both_pages')).__name__ == 'list' and _R('both_pages')[-1:] == [[45, 40, 36]]", "`.append()` put "
         "the whole list `new_marks` inside as one item. `+` joins two lists into one: `old_marks + new_marks`.", None),
        ("_R('both_pages') == [] and _named", Code("'`' + _named[0] + '` holds the joined list, but this task' + "
         "chr(39) + 's list is `both_pages`. Put the join on the right side of `both_pages = `.'"), None),
        ("_R('both_pages') == []", "`both_pages` is still the empty list `[]`. Put `old_marks + new_marks` on its "
         "right side, in place of `[]`.", None),
        ("_R('both_pages') == [50, 49, 44, 41, 37]", "You typed in the numbers from `new_marks` instead of using its "
         "name. Join the lists: `old_marks + new_marks`.", None),
        ("_R('both_pages') == [48, 48, 47, 46, 45, 40, 36]", "You typed in the numbers from `old_marks` instead of "
         "using its name. Join the lists: `old_marks + new_marks`.", None),
        ("_R('both_pages') == _g0.get('both_pages') and _plain('both_pages')", "You typed in the numbers for "
         "`both_pages` instead of joining the two lists. Write `both_pages = old_marks + new_marks`.",
         "'`both_pages` stayed the same'"),
        ("_R('both_pages') == _g0.get('both_pages')", "`both_pages` isn't made from `old_marks` and `new_marks`. "
         "Join the two lists: `both_pages = old_marks + new_marks`.", "'`both_pages` stayed the same'"),
    ],
    fix="`both_pages` doesn't join the two lists yet. Join them with `+`, old marks first: "
        "`both_pages = old_marks + new_marks`.",
    ev="Mar'tu tested your code with test marks, `old_marks = [50, 49]` and `new_marks = [45, 40, 36]`",
    saw="'`both_pages` became ' + _sh(_R('both_pages'))",
    kind="set of marks",
    # A join kept under another name (`wall = old_marks + new_marks`, the name this step used before the rename).
    pre=("_named = [_k for _k in _r if not _k.startswith('_') and _k not in ('old_marks', 'new_marks', 'both_pages') "
         "and _r[_k] == [50, 49, 45, 40, 36]]\n"),
)

PLUS_USED = (
    "the two lists are joined with +",
    "import ast as _ast\n"
    "_names = lambda _x: {_m.id for _m in _ast.walk(_x) if type(_m).__name__ == 'Name'}\n"
    "_adds = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'BinOp' "
    "and type(_n.op).__name__ == 'Add' and {'old_marks', 'new_marks'} <= _names(_n)]\n"
    "assert _adds, 'This step practices joining lists with `+`: `both_pages = old_marks + new_marks`.'",
)

NEW_CHALK_MARK = dict(
    id="new-chalk-mark",
    title="A new chalk mark",
    martu=(
        "[[append|`.append()`]] adds one item to the end of a list, the way an *appendix* goes at the end of a "
        "book. The dot asks the list to do something, the way it asked text in Unit 2: `chalk_wall.append(33)` "
        "means *chalk wall, add 33 to your end*. It changes the list itself.\n"
        "`+` joins two lists into one new list, the way it glued text in Unit 1: `[41, 37] + [33]` makes "
        "`[41, 37, 33]`. The two old lists stay as they were.\n"
        "Bursts keep coming, so my wall keeps growing: each new gap is a new mark. Your guess for the next gap "
        "goes on the end. For Step 2, I copied my marks onto two pages, `old_marks` and `new_marks`."
    ),
    introduces=["attr:append"],
    example='party_colors = ["gold", "teal"]\nparty_colors.append("silver")\nprint(party_colors)\n',
    example_output="['gold', 'teal', 'silver']",
    names=["chalk_wall", "old_marks", "new_marks", "both_pages"],
    pick="33",
    predict=dict(
        q="What will this print?",
        code="marks = [41, 37]\nmarks.append(33)\nprint(marks)\nprint(marks + [30])\n",
        choices=["[41, 37]\n[41, 37, 30]", "[33, 41, 37]\n[30, 33, 41, 37]", "[41, 37, 33]\n[41, 37, 33, 30]",
                 "[41, 37, 33]\n[41, 37, 33]"],
        answer=2,
        explain=(
            "`.append(33)` adds 33 to the end of `marks` itself. `marks + [30]` makes a new, longer list to "
            "show. It leaves `marks` as it was, because no name keeps the new list."
        ),
    ),
    starter=MARK_STARTER,
    checkpoints=[
        dict(
            id="append-your-guess",
            text=(
                "On line 3, under `# 1. Append your guess.`, add your own guess for the next gap to the end of "
                "`chalk_wall`, with `.append()`. Use a whole number below 37."
            ),
            dictated=False,
            hints=[
                "Look at the Example: the list's name, a dot, `append`, then the new item in parentheses.",
                "`party_colors.append(\"silver\")` puts silver on the end of `party_colors`. Your guess is a number, "
                "so it gets no quotes.",
                "Write `chalk_wall.append(33)` under the `# 1.` note, with your own guess in place of 33.",
            ],
            checks=[
                have_list("chalk_wall", known=MARK_KNOWN, foreign=["party_colors", "marks"]),
                GUESS_CHECK,
                APPEND_USED,
                printed_after("chalk_wall", "the append"),
            ],
            pass_line="Your guess is on the end of the wall. Mar'tu: I hope you're wrong, yes? Too short is bad news.",
        ),
        dict(
            id="join-two-walls",
            text=(
                "On the line `both_pages = []`, put `old_marks + new_marks` in place of the `[]`, so the old marks "
                "come first."
            ),
            dictated=True,
            hints=[
                "Find the line `both_pages = []`. The two lists go on its right side, with `+` between them.",
                "`+` joins two lists into one new list: `[1, 2] + [3, 4]` makes `[1, 2, 3, 4]`.",
                "Write `both_pages = old_marks + new_marks` in place of `both_pages = []`.",
            ],
            checks=[
                have_list("both_pages", known=MARK_KNOWN, foreign=["party_colors", "marks"]),
                not_reset("both_pages"),
                JOIN_CHECK,
                PLUS_USED,
            ],
            pass_line="You joined two lists into one. Oogrish: Two pages of marks, one list. Steady, now.",
        ),
    ],
    solution=_mark(),
    partials=[_mark(pages="both_pages = []")],
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "chalk_wall.append(33)", "print(chalk_wall)",
               "old_marks = [48, 48, 47, 46]", "new_marks = [44, 41, 37]", "both_pages = old_marks + new_marks",
               "print(both_pages)"],
        distractors=['chalk_wall.append("33")', "chalk_wall = chalk_wall.append(33)",
                     "both_pages = new_marks + old_marks"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A jar on the end",
            text=(
                "```text\nbefore: [48][48]...[41][37]\nappend(33)          adds  ^\n"
                "after:  [48][48]...[41][37][33]\n```\nOne new jar, at the end of the same shelf."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `chalk_wall.append(33)`: the wall itself grows to 8 gaps.\n"
                "2. `old_marks + new_marks`: Python makes a NEW list, old marks then new.\n"
                "3. `both_pages = ...` keeps that new list in `both_pages`. Without `both_pages =` in front, Python "
                "makes the new list and throws it away."
            ),
        ),
        dict(
            angle="everyday",
            label="A notebook and a new sheet",
            text=(
                "`.append()` writes one more line in your notebook. `+` puts two pages together on a new sheet. "
                "Your old pages stay as they were."
            ),
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `chalk_wall.append(\"33\")` (text, not a number). Not this: `chalk_wall + 33` (a "
                "number won't join a list). Not this: `chalk_wall = chalk_wall.append(33)` (append hands back "
                "nothing).\nThis: `chalk_wall.append(33)`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's bet: 4 less each time",
        text=(
            "Lucky bets the gaps shrink by 4 each time. Add two more gaps with `.append()`, each one 4 less than "
            "the newest gap: `chalk_wall[-1] - 4`. Put both lines above `print(chalk_wall)`."
        ),
        hints=[
            "Each new gap is the newest minus 4. Do it twice: the second time, `[-1]` is the gap you added a "
            "moment ago.",
            "Write `chalk_wall.append(chalk_wall[-1] - 4)` on two lines, both under your guess and above `print(chalk_wall)`.",
        ],
        checks=[
            (
                "two more gaps, each 4 less than the one before",
                "import ast as _ast\n"
                "_calc = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
                "and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'append' and _n.args "
                "and type(_n.args[0]).__name__ == 'BinOp' and any(type(_m).__name__ == 'Subscript' "
                "for _m in _ast.walk(_n.args[0]))]\n"
                "_w = chalk_wall\n"
                "assert len(_calc) >= 2, 'Your code doesn' + chr(39) + 't add two gaps worked out from the list yet. "
                "Write `chalk_wall.append(chalk_wall[-1] - 4)` twice.'\n"
                "assert len(_w) >= 10 and _w[-2] == _w[-3] - 4 and _w[-1] == _w[-2] - 4, "
                "'One of the new gaps isn' + chr(39) + 't 4 less than the gap before it. Work each one out with "
                "`chalk_wall[-1] - 4`.'",
            ),
        ],
        solution=_mark(append="chalk_wall.append(33)\nchalk_wall.append(chalk_wall[-1] - 4)\n"
                              "chalk_wall.append(chalk_wall[-1] - 4)"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "You've seen this night. Bomb Shell studied the wall and said: thirty-two hours, maybe less. That's a "
            "new mark at the bottom of the wall. In Python, it's one `.append()`: `chalk_wall.append(32)`."
        ),
    ),
    takeaway="`wall.append(33)` adds one item to the end of the list itself. `old + new` makes a new, joined list.",
    wrong_answers=[
        dict(why="starter unchanged: still 7 gaps", code=MARK_STARTER, fails_at=1, message_contains="still has 7 gaps"),
        dict(why="the guess appended as text (spec)", code=_mark(append='chalk_wall.append("33")'), fails_at=1,
             message_contains="number"),
        dict(why="a number joined with + (spec): TypeError", code=_mark(append="chalk_wall = chalk_wall + 33"),
             fails_at=0, message_contains="concatenate"),
        dict(why="+ joins a new list and forgets it", code=_mark(append="chalk_wall + [33]"), fails_at=1,
             message_contains="throws it away"),
        dict(why="append stored back: x = x.append(...) leaves None", code=_mark(append="chalk_wall = chalk_wall.append(33)"),
             fails_at=1, message_contains="None"),
        dict(why="the wall retyped with an 8th gap (assigning a new list)",
             code=_mark(append="chalk_wall = [48, 48, 47, 46, 44, 41, 37, 33]"), fails_at=1, message_contains=".append()"),
        dict(why="+ used instead of append", code=_mark(append="chalk_wall = chalk_wall + [33]"), fails_at=1,
             message_contains=".append()"),
        dict(why="a guess that is not below 37", code=_mark(append="chalk_wall.append(40)"), fails_at=1,
             message_contains="below 37"),
        dict(why="a list appended inside the list", code=_mark(append="chalk_wall.append([33])"), fails_at=1,
             message_contains="list inside"),
        dict(why="square brackets for append's round ones", code=_mark(append="chalk_wall.append[33]"), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="the append put after the print", code=_mark(append="", after="chalk_wall.append(33)"), fails_at=1,
             message_contains="runs before"),
        dict(why="the example's list name copied", code=_mark(append="party_colors.append(33)"), fails_at=0,
             message_contains="not defined"),
        dict(why="both_pages typed by hand (spec)", code=_mark(pages="both_pages = [48, 48, 47, 46, 44, 41, 37]"), fails_at=2,
             message_contains="typed in the numbers for `both_pages`"),
        dict(why="new marks first", code=_mark(pages="both_pages = new_marks + old_marks"), fails_at=2,
             message_contains="Old marks go first"),
        dict(why="a list of two lists", code=_mark(pages="both_pages = [old_marks, new_marks]"), fails_at=2,
             message_contains="two lists"),
        dict(why="append used to join: hands back None", code=_mark(pages="both_pages = old_marks.append(new_marks)"),
             fails_at=2, message_contains="hands back nothing"),
        dict(why="joined but not kept: both_pages stays empty", code=_mark(pages="old_marks + new_marks\nboth_pages = []"),
             fails_at=2, message_contains="empty list"),
        dict(why="a guess of 0 or less is no gap at all", code=_mark(append="chalk_wall.append(-5)"), fails_at=1,
             message_contains="above 0"),
        dict(why="typing a list's values by hand: new_marks' numbers typed in", code=_mark(pages="both_pages = old_marks + [44, 41, 37]"),
             fails_at=2, message_contains="numbers from `new_marks`"),
        dict(why="typing a list's values by hand: old_marks' numbers typed in",
             code=_mark(pages="both_pages = [48, 48, 47, 46] + new_marks"), fails_at=2, message_contains="numbers from `old_marks`"),
        dict(why="append used to join: the whole list goes in as one item",
             code=_mark(pages="both_pages = old_marks\nboth_pages.append(new_marks)"), fails_at=2, message_contains="as one item"),
        dict(why="the other list's name on the right: both_pages = chalk_wall (not typed, but not joined)",
             code=_mark(pages="both_pages = chalk_wall"), fails_at=2, message_contains="isn't made from"),
        dict(why="the join typed above the starter's `both_pages = []`, which empties it again",
             code=MARK_TOP + "chalk_wall.append(33)\nprint(chalk_wall)\n\n" + MARK_BOTTOM
             + "both_pages = old_marks + new_marks\nboth_pages = []\nprint(both_pages)\n", fails_at=2,
             message_contains="again"),
        dict(why="the join kept under another name (`wall`), so both_pages stays empty",
             code=_mark(pages="wall = old_marks + new_marks\nboth_pages = []"), fails_at=2,
             message_contains="this task's list is `both_pages`"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-append-len", solo="false", dictates="2",
             foreign_names="party_colors,marks", pick="33") + "\n"
        "3A-05 with 3A-08 (join-two-walls) folded in as CP2. CP1 is creative: any whole number below 37 passes "
        "(lint e); DF = 33. CP1 counts the first 8 items, so Lucky's side quest (two more appends) never undoes "
        "it. Investigate (spec: `chalk_wall + [33]` versus `chalk_wall + 33`): the Learn text keeps only "
        "`[41, 37] + [33]` (teacher ruling: the TypeError sentence is cut), the contrast angle keeps 'Not this: "
        "`chalk_wall + 33`', and the TypeError row ('`+` joins two lists') is the site explainer's. The class's "
        "'append vs + vs a new list' slip gets three messages: a retyped wall and `chalk_wall = chalk_wall + [33]` "
        "are told this step practices `.append()`; a lone `chalk_wall + [33]` is made and forgotten; `chalk_wall = "
        "chalk_wall.append(33)` leaves `None` ('nothing came back'). CP2's list is `both_pages` (teacher ruling: "
        "not `wall`, the recipe's ingredient name in the next exercise); it is CMB (other marks), which fixes v1's "
        "OUT-only check, and a join kept under another name (`wall = ...`) is named. "
        "BQ (combining append + index + arithmetic): `chalk_wall.append(chalk_wall[-1] - 4)` twice. Campaign "
        "link: Module 2's closing beat, thirty-two hours (the next mark)."
    ),
)


# 3A-06 (split: CP1 the long way on a plain line, CP2 the recipe) ------------------------------------

LONG_TOP = WALL_LINE + "print(len(chalk_wall))\n# 1. The newest gap, the long way:\n"
LONG_MID = "\n# 2. Hand back the last item of any wall.\n"
LONG_DEF = "def newest_mark(wall):\n"
LONG_CALLS = (
    "\nprint(newest_mark(chalk_wall))  # This should show 37\n"
    "print(newest_mark([9, 8, 7]))  # This should show 7\n"
)
LONG_PLAIN = "print(chalk_wall[len(chalk_wall) - 1])"


def _long(body="    return wall[len(wall) - 1]", plain=LONG_PLAIN, head=LONG_DEF):
    return LONG_TOP + plain + LONG_MID + head + body + "\n" + LONG_CALLS


LONG_STARTER = _long("    return 0", plain="")

# PAR / PAR-CONST / RET for newest_mark(wall): three fresh walls the task never shows ([9, 6, 4] -> 4, [5] -> 5,
# and the unsorted [8, 12, 10] -> 10, so `min(wall)` or a sorted read fails; no fresh call gives the task's 37 or
# the starter's own second call, `[9, 8, 7]`, lint b). The first wrong call is diagnosed.
_PAR_DEF = (
    "import ast as _ast, io as _io, sys as _sys\n"
    "def _call(_fn, _a):\n"
    "    _keep = _sys.stdout\n"
    "    _sys.stdout = _io.StringIO()\n"
    "    _out, _err = None, ''\n"
    "    try:\n"
    "        _out = _fn(list(_a))\n"
    "    except Exception as _x:\n"
    "        _err = type(_x).__name__ + ': ' + str(_x)\n"
    "    finally:\n"
    "        _pr = _sys.stdout.getvalue().strip()\n"
    "        _sys.stdout = _keep\n"
    "    return _out, _pr, _err\n"
)

PAR_CASES = [[9, 6, 4], [5], [8, 12, 10]]
NOTHING = "`None`: nothing came back"


def recipe_par(label, fname, pick, word, missing=None, lean=False):
    """PAR for a recipe that hands back one item of a wall. `pick` is the right position as Python code over
    `wall` (`len(wall) - 1` or `0`), `word` names the item ("last", "first"). Only the values are compared, so
    `wall[-1]` and `wall[len(wall) - 1]` both pass for the last item. `lean=True` (SOLO): each message names the
    slip and keeps the evidence bracket, with no code and no fix."""
    want_line = f"`wall[{pick}]`"
    if lean:
        m = dict(
            missing="The recipe `newest_mark` is gone, so Mar'tu has nothing to test.",
            args="The ingredient on the `def` line is no longer named `wall`.",
            outer="The recipe reads the list from outside, not the one it is handed.",
            idx="The recipe asks for a position the wall doesn't have.",
            err="The recipe stops with an error on some walls.",
            text="The recipe hands back text, not the item.",
            printed="The recipe prints the item but does not hand it back.",
            box="The recipe makes a variable, then hands back nothing.",
            none="The recipe hands back nothing.",
            zero="The recipe still hands back the placeholder.",
            same="The recipe hands back the same answer for every wall.",
            count="The recipe hands back the count, not an item.",
            pos="The recipe hands back a position, not the item there.",
            whole="The recipe hands back the whole list, not one item.",
            other=f"The recipe hands back the wrong item, not the {word} one.",
        )
    else:
        m = dict(
            missing=missing or (f"Python can't find the recipe `{fname}`. Put its `def` line back the way it was: "
                                f"`def {fname}(wall):`."),
            args=(f"The ingredient on the `def` line has changed. Put it back the way it was: `def {fname}(wall):`. "
                  "Mar'tu hands his test walls to `wall`."),
            outer="Your recipe reads `chalk_wall`, the list outside, so every call gets the same wall. Use the "
                  "ingredient `wall`, not `chalk_wall`.",
            err="Make the recipe work for a wall of any length.",
            text="Your recipe hands back the item as text. Hand back the item itself, with no `str()` and no quotes.",
            printed="Your recipe shows the item with `print`, but doesn't hand it back. Hand it back with `return`, "
                    "not `print`.",
            box="Your recipe makes a variable, but its `return` hands back nothing. Hand back the variable you made: `return ",
            none=f"Your recipe hands back nothing. Put `return` in front of the {word} item, so it hands that back.",
            zero=f"Your recipe still hands back the placeholder 0. Replace the `0` with the {word} item of `wall`.",
            same="Your recipe hands back the same answer for every wall, because the answer is typed in. Read the "
                 "item from `wall` instead.",
        )
        if word == "last":
            m.update(
                idx="Your recipe asks for a position that fits one wall only, so some walls don't have it. The last "
                    "position is one less than the count.",
                count="Your recipe hands back the count: how many items there are. The last position is one less "
                      "than the count.",
                pos="Your recipe hands back a position, not the item there. Read the item at that position from "
                    "`wall`, with square brackets.",
                whole="Your recipe hands back the whole list. Hand back one item: the last.",
                other="Your recipe hands back the wrong item. Hand back the last item of `wall`.",
            )
        else:
            m.update(
                idx=f"The {word} item is at {want_line} on a wall of any length.",
                count=f"Your recipe hands back the count: how many items there are. Hand back the {word} item: "
                      f"{want_line}.",
                pos=f"Your recipe hands back a position, not the item there. Hand back the item: {want_line}.",
                whole=f"Your recipe hands back the whole list. Hand back one item: {want_line}.",
                other=f"Your recipe hands back the wrong item. Hand back the {word} item of `wall`: {want_line}.",
            )
    box_end = "" if lean else " + _box[-1] + '`.'"
    code = _PAR_DEF + (
        f"_fn = globals().get({fname!r})\n"
        f"assert callable(_fn), {m['missing']!r}\n"
        f"_defs = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef' and _n.name == {fname!r}]\n"
        "_args = [_a.arg for _a in _defs[-1].args.args] if _defs else []\n"
        f"assert _args == ['wall'], {m['args']!r}\n"
        "_inner = {_m.id for _m in _ast.walk(_defs[-1]) if type(_m).__name__ == 'Name'} if _defs else set()\n"
        "_box = [_t.id for _n in (_ast.walk(_defs[-1]) if _defs else []) if type(_n).__name__ == 'Assign' "
        "for _t in _n.targets if type(_t).__name__ == 'Name']\n"
        "_bare = any(type(_n).__name__ == 'Return' and _n.value is None for _n in (_ast.walk(_defs[-1]) if _defs else []))\n"
        f"_cases = {PAR_CASES!r}\n"
        f"_want = [_c[{pick.replace('wall', '_c')}] for _c in _cases]\n"
        "_got = [_call(_fn, _c) for _c in _cases]\n"
        f"_c = lambda _a: '`{fname}(' + str(_a) + ')`'\n"
        "_bad = [_i for _i in range(len(_cases)) if _got[_i][2] or _got[_i][0] != _want[_i] or type(_got[_i][0]).__name__ != 'int']\n"
        "if _bad:\n"
        "    _i = _bad[0]\n"
        "    _a, (_out, _pr, _err) = _cases[_i], _got[_i]\n"
        "    _ev = \" Mar'tu tested your recipe with a test call, \" + _c(_a)\n"
        "    _then = ', and it stopped with an error: ' + _err.split(':')[0] + '.' if _err else ': it handed back ' + str(_out) + '.'\n"
        f"    _none = ': it handed back {NOTHING}.'\n"
        "    if 'chalk_wall' in _inner:\n"
        f"        _msg = {m['outer']!r} + _ev + _then\n"
        "    elif _err.startswith('IndexError'):\n"
        f"        _msg = {m['idx']!r} + _ev + ', and it stopped with an error: IndexError.'\n"
        "    elif _err:\n"
        f"        _msg = _ev.strip() + ', and it stopped with an error. Python said: ' + _err + '. ' + {m['err']!r}\n"
        "    elif type(_out).__name__ == 'str':\n"
        f"        _msg = {m['text']!r} + _ev + ': it handed back ' + repr(_out) + '.'\n"
        "    elif _out is None and _pr:\n"
        f"        _msg = {m['printed']!r} + _ev + ': it printed ' + _pr + ' and handed back {NOTHING}.'\n"
        "    elif _out is None and _bare and _box:\n"
        f"        _msg = {m['box']!r}{box_end} + _ev + _none\n"
        "    elif _out is None:\n"
        f"        _msg = {m['none']!r} + _ev + _none\n"
        "    elif _got[0][0] == 0 and _got[1][0] == 0:\n"
        f"        _msg = {m['zero']!r} + _ev + ': it still handed back 0.'\n"
        "    elif _got[0][0] == _got[1][0]:\n"
        f"        _msg = {m['same']!r} + \" Mar'tu tested your recipe with two test calls, \" + "
        "_c(_cases[0]) + ' and ' + _c(_cases[1]) + ': both handed back ' + str(_got[0][0]) + '.'\n"
        "    elif _out == len(_a):\n"
        f"        _msg = {m['count']!r} + _ev + ': it handed back ' + str(_out) + '.'\n"
        "    elif _out == len(_a) - 1:\n"
        f"        _msg = {m['pos']!r} + _ev + ': it handed back ' + str(_out) + '.'\n"
        "    elif type(_out).__name__ == 'list':\n"
        f"        _msg = {m['whole']!r} + _ev + ': it handed back ' + str(_out) + '.'\n"
        "    else:\n"
        f"        _msg = {m['other']!r} + _ev + ': it handed back ' + str(_out) + ', not ' + str(_want[_i]) + '.'\n"
        "    assert False, _msg\n"
    )
    return (label, code)


# CP1 reads the plain line only: top-level code, outside any recipe. `_subs`: its reads of `chalk_wall[...]`;
# `_lenp`: those that find the position with `len` (inside the brackets, or through a box made from `len`);
# `_cnum`: those with a counted number, like `[6]`.
_TOP_READS = (
    "_tops = [_s for _s in _ast.parse(_source).body if type(_s).__name__ != 'FunctionDef']\n"
    "_lenx = lambda _x: any(type(_m).__name__ == 'Call' and type(_m.func).__name__ == 'Name' and _m.func.id == 'len' "
    "for _m in _ast.walk(_x))\n"
    "_lenv = [_t.id for _s in _tops if type(_s).__name__ == 'Assign' and _lenx(_s.value) for _t in _s.targets "
    "if type(_t).__name__ == 'Name']\n"
    "_subs = [_n for _s in _tops for _n in _ast.walk(_s) if type(_n).__name__ == 'Subscript' "
    "and type(_n.value).__name__ == 'Name' and _n.value.id == 'chalk_wall']\n"
    "_lenp = [_n for _n in _subs if _lenx(_n.slice) or any(type(_m).__name__ == 'Name' and _m.id in _lenv "
    "for _m in _ast.walk(_n.slice))]\n"
    "_cnum = [_n for _n in _subs if type(_n.slice).__name__ == 'Constant' and type(_n.slice.value).__name__ == 'int']\n"
)

LONG_FIX = "`chalk_wall[len(chalk_wall) - 1]`"


def long_line(wall):
    """CP1: the plain line prints the newest gap, on another wall. Top-level lines that call `newest_mark` are left
    out of the rerun, so the recipe's own printed line can never pass for the plain line."""
    return follows(
        f"the plain line prints the newest gap on a wall of {len(wall)} gaps",
        {"chalk_wall": wall},
        f"_said({_W}[-1])",
        rules=[
            ("_cnum", "Your line uses a position you counted, and that fits one wall only. Let `len` count: "
             + LONG_FIX + ".", None),
            (f"_said(len({_W}) - 1)", "Your line shows the last position, not the gap there. Read the gap: "
             + LONG_FIX + ".", None),
            (f"_said({_MINE}[-1])", "You typed the gap instead of reading it from the list. Read it the long way: "
             + LONG_FIX + ".",
             f"'it still printed `' + str({_MINE}[-1]) + '`'"),
            (WHOLE_LIST[0], "Your line shows the whole list. Show one gap, the newest: " + LONG_FIX + ".", WHOLE_LIST[1]),
        ],
        fix="Your code doesn't show the newest gap the long way yet. Show it inside `print( )`: " + LONG_FIX + ".",
        ev=_ev(wall),
        crash=[
            ("_e.startswith('IndexError') and _cnum", "Your line uses a position you counted, and that fits one wall "
             "only. Let `len` count: " + LONG_FIX + "."),
            ("_e.startswith('IndexError')", "`len(chalk_wall)` is one past the last position. Take 1 away: "
             "`len(chalk_wall) - 1`."),
        ],
        pre=_TOP_READS,
        drop=("newest_mark",),
    )


LEN_PLAIN_USED = (
    "the plain line finds the position with len",
    "import ast as _ast\n" + _TOP_READS +
    "_neg = [_n for _n in _subs if type(_n.slice).__name__ == 'UnaryOp']\n"
    "assert _lenp or not _neg, ('Your line uses `[-1]`, the short way. This step practices the long way, with '\n"
    "    '`len - 1`. In Unit 6, you' + chr(39) + 'll count positions this way.')\n"
    "assert _lenp, 'Your line doesn' + chr(39) + 't use `len`. Find the position with `len`: " + LONG_FIX + ".'",
)

HOW_LONG = dict(
    id="how-long",
    title="How long is the wall?",
    martu=(
        "[[len()|`len(wall)`]] counts the items in a list: `len(chalk_wall)` is 7. Positions start at 0, so the "
        "last position is one less, `len(wall) - 1`. It's *seven* and *seventh* again: 7 gaps, and the seventh "
        "is at position 6:\n"
        "```text\nlen(wall)      ->  7\nlast position  ->  7 - 1 = 6\nwall[6]        ->  37\n```\n"
        "A recipe (function) can take a whole list as its ingredient (parameter). Whatever list the call hands "
        "over, inside the recipe it's called `wall`. So `newest_mark(chalk_wall)` and `newest_mark([9, 8, 7])` "
        "both work.\n"
        "Why the long way, when `[-1]` exists? In Unit 6, you'll go down a list one position at a time, from 0 to "
        "`len - 1`."
    ),
    introduces=["call:len"],
    example='colors = ["gold", "teal", "silver"]\nprint(len(colors))\nprint(colors[len(colors) - 1])\n',
    example_output="3\nsilver",
    names=["chalk_wall", "newest_mark", "wall"],
    predict=dict(
        q="Before you change anything: what does the code that's already there print?",
        choices=["7\n37\n7", "6\n37\n7", "7\n0\n7", "7\n0\n0"],
        answer=3,
        explain=(
            "`len(chalk_wall)` counts 7 gaps. Line 4 is empty for now. The recipe still hands back its "
            "placeholder, 0, whatever wall it is handed. When you're done, the Console shows what the notes say: "
            "37, then 7."
        ),
    ),
    pair_talk=(
        "Pair talk: the call is `newest_mark([9, 8, 7])`. One of you says what `wall` holds inside the recipe. The "
        "other says what `len(wall) - 1` is. Then each of you writes your own `return` line."
    ),
    starter=LONG_STARTER,
    tracer=True,
    checkpoints=[
        dict(
            id="len-minus-one",
            text=(
                "On line 4, under the note `# 1.`, type `print(chalk_wall[len(chalk_wall) - 1])`. You should see 37 "
                "in the Console."
            ),
            dictated=True,
            hints=[
                "Look at the last line of the Example. It reads the last color the long way.",
                "`len(chalk_wall)` counts the items. The last position is one less: `len(chalk_wall) - 1`.",
                "Write `print(chalk_wall[len(chalk_wall) - 1])` under the `# 1.` note.",
            ],
            checks=[
                have_list("chalk_wall", known=["chalk_wall", "wall"], foreign=["colors"]),
                long_line(W5),
                long_line(W8),
                LEN_PLAIN_USED,
            ],
            pass_line="You found 37 the long way. Mar'tu: `len` counted 7, and one less is 6. Positions start at 0.",
        ),
        dict(
            id="newest-mark",
            text=(
                "Change `return 0` in `newest_mark`. Make the recipe hand back the last item of `wall`, for a wall of "
                "any length."
            ),
            dictated=False,
            hints=[
                "Look at `return 0` inside `newest_mark`. Inside the recipe, the list is called `wall`, whatever its "
                "name outside.",
                "The 0 is a placeholder: a stand-in until you write the real answer. It becomes the last item of "
                "`wall`.",
                "In the Example, the last color is `colors[len(colors) - 1]`. Write the same with `wall` in place "
                "of `colors`.",
                "Write `return wall[len(wall) - 1]` in place of `return 0`. `return wall[-1]` works too.",
            ],
            checks=[
                recipe_par("newest_mark hands back the last item of a fresh wall", "newest_mark", "len(wall) - 1", "last"),
            ],
            pass_line=(
                "Your recipe finds the newest mark of any wall. Mar'tu: `wall[-1]` or `wall[len(wall) - 1]`: both "
                "land on the last item."
            ),
        ),
    ],
    solution=_long(),
    partials=[_long("    return 0")],
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "print(len(chalk_wall))",
               "print(chalk_wall[len(chalk_wall) - 1])", "def newest_mark(wall):", "    return wall[len(wall) - 1]",
               "print(newest_mark(chalk_wall))", "print(newest_mark([9, 8, 7]))"],
        distractors=["print(chalk_wall[len(chalk_wall)])", "    return wall[len(wall)]", "    return len(wall) - 1"],
    ),
    another_way=[
        dict(
            angle="picture",
            text=(
                "```text\nposition: 0  1  2  3  4  5  6\n          48 48 47 46 44 41 37\n"
                "len = 7 items\nlast position = 7 - 1 = 6\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Step 1, on the wall: `len(chalk_wall)` is 7, so `chalk_wall[len(chalk_wall) - 1]` is "
                "`chalk_wall[6]`, which is 37.\n"
                "Step 2, in the recipe, for `newest_mark([9, 8, 7])`:\n1. `wall` is `[9, 8, 7]`.\n"
                "2. `len(wall)` is 3.\n3. `len(wall) - 1` is 2.\n4. `wall[2]` is 7. The recipe hands back 7."
            ),
        ),
        dict(
            angle="everyday",
            label="Seven jars",
            text=(
                "Seven jars on a shelf, numbered from 0. The last jar is jar 6, not jar 7. The count is one more "
                "than the last number, every time."
            ),
        ),
        dict(
            angle="from Unit 3",
            label="Like any recipe",
            text=(
                "Same as Unit 3's recipes: the call hands something over, the ingredient's name holds it, and "
                "`return` hands the answer back. This time the thing handed over is a whole list."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work?",
            text=(
                "`len` counts from 1, but positions count from 0. So the count is always one past the last "
                "position. Take 1 away and you land on the last item, on a wall of any length."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Oldest and newest",
        text=(
            "Lucky wants the whole story. Two parts:\n"
            "1. Under `newest_mark`, write a second recipe, `oldest_mark(wall)`, that hands back the first item.\n"
            "2. At the bottom, show the shrink from oldest to newest, using both recipes."
        ),
        hints=[
            "The oldest is at position 0 on any wall: `return wall[0]`. Store each recipe's answer in a variable, "
            "then show the first minus the last.",
            "Write `def oldest_mark(wall):` at the bottom, with `    return wall[0]` under it. Then `first = oldest_mark(chalk_wall)`, `last = newest_mark(chalk_wall)` and `print(first - last)`.",
        ],
        checks=[
            recipe_par("oldest_mark hands back the first item of a fresh wall", "oldest_mark", "0", "first",
                       missing="Python can't find a recipe named `oldest_mark`. Write it under the first one: "
                               "`def oldest_mark(wall):`."),
            (
                "prints the shrink from the two recipes",
                "import ast as _ast\n"
                "_top = [_n for _s in _ast.parse(_source).body if type(_s).__name__ != 'FunctionDef' "
                "for _n in _ast.walk(_s)]\n"
                "_called = {_n.func.id for _n in _top if type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name'}\n"
                "_subs = [_n for _n in _top if type(_n).__name__ == 'BinOp' and type(_n.op).__name__ == 'Sub']\n"
                "assert {'oldest_mark', 'newest_mark'} <= _called and _subs, ('Your code doesn' + chr(39) + 't call '\n"
                "    'both recipes and subtract yet. Call each one on `chalk_wall`, like `first = oldest_mark(chalk_wall)`, '\n"
                "    'then show the first minus the last.')\n"
                "assert str(oldest_mark(chalk_wall) - newest_mark(chalk_wall)) in _lines(), "
                "'The Console doesn' + chr(39) + 't show the shrink yet: the oldest gap minus the newest.'",
            ),
            follows(
                "the shrink follows the wall",
                {"chalk_wall": W5},
                f"_said({_W}[0] - {_W}[-1])",
                fix="Your shrink doesn't change when the wall changes. Work it out from the two recipes' answers.",
                ev=WALL_EV5,
                saw="'the last line it printed was ' + _show(_p[-1:])",
            ),
        ],
        solution=_long() + "\ndef oldest_mark(wall):\n    return wall[0]\n\n"
                           "first = oldest_mark(chalk_wall)\nlast = newest_mark(chalk_wall)\nprint(first - last)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="def show_mana(caster):\n    mana_bar = get_mana_bar(caster)",
        why=(
            "You've seen this. `show_mana(caster)` took a whole hero as its ingredient and read what it needed "
            "from inside. `newest_mark(wall)` takes a whole list the same way."
        ),
    ),
    takeaway="`len(wall)` counts the items. The last position is `len(wall) - 1`: the same item as `wall[-1]`.",
    wrong_answers=[
        # CP1: the plain line, the long way
        dict(why="starter unchanged: line 4 still empty", code=LONG_STARTER, fails_at=1, message_contains="the long way"),
        dict(why="[-1]: right, the short way, but this line practices len - 1", code=_long(plain="print(chalk_wall[-1])"),
             fails_at=1, message_contains="the short way"),
        dict(why="a counted position [6]: fits 7 gaps only (re-run on 5 gaps stops with IndexError)",
             code=_long(plain="print(chalk_wall[6])"), fails_at=1, message_contains="fits one wall only"),
        dict(why="[4]: the last of the check's 5-gap wall, caught on the 8-gap wall",
             code=_long(plain="print(chalk_wall[4])"), fails_at=1, message_contains="`[50, 49, 47, 44, 40, 35, 29, 22]`"),
        dict(why="len(list) used as an index (spec): IndexError on the student's own Run",
             code=_long(plain="print(chalk_wall[len(chalk_wall)])"), fails_at=0, message_contains="out of range"),
        dict(why="the value typed by hand instead of read from the list", code=_long(plain="print(37)"), fails_at=1,
             message_contains="typed the gap instead"),
        dict(why="the last position printed, not the gap there", code=_long(plain="print(len(chalk_wall) - 1)"),
             fails_at=1, message_contains="shows the last position"),
        dict(why="the whole list printed", code=_long(plain="print(chalk_wall)"), fails_at=1, message_contains="whole list"),
        dict(why="round brackets: the list called like a recipe (on the plain line)",
             code=_long(plain="print(chalk_wall(len(chalk_wall) - 1))"), fails_at=0, message_contains="not callable"),
        dict(why="the recipe done first, line 4 left empty: the recipe's printed 37 must not pass the plain line",
             code=_long("    return wall[-1]", plain=""), fails_at=1, message_contains="the long way"),
        # CP2: the recipe (wall[-1] and wall[len(wall) - 1] both pass)
        dict(why="starter's recipe unchanged: the placeholder 0", code=_long("    return 0"), fails_at=2,
             message_contains="placeholder"),
        dict(why="the answer typed in (spec): PAR-CONST", code=_long("    return 37"), fails_at=2,
             message_contains="both handed back 37"),
        dict(why="len(list) used as a position (spec): IndexError on the student's own Run",
             code=_long("    return wall[len(wall)]"), fails_at=0, message_contains="out of range"),
        dict(why="the outside name chalk_wall used inside (spec)",
             code=_long("    return chalk_wall[len(chalk_wall) - 1]"), fails_at=2, message_contains="not `chalk_wall`"),
        dict(why="printed instead of handed back", code=_long("    print(wall[len(wall) - 1])"), fails_at=2,
             message_contains="not `print`"),
        dict(why="a box made, then a bare return: nothing comes back",
             code=_long("    last = wall[len(wall) - 1]\n    return"), fails_at=2, message_contains="`return last`"),
        dict(why="a box made, no return at all", code=_long("    last = wall[-1]"), fails_at=2,
             message_contains="nothing came back"),
        dict(why="hands back the count", code=_long("    return len(wall)"), fails_at=2, message_contains="how many items"),
        dict(why="hands back the last position, not the item", code=_long("    return len(wall) - 1"), fails_at=2,
             message_contains="a position, not the item"),
        dict(why="a counted position [6]: the starter's second call, on [9, 8, 7], stops the student's own Run",
             code=_long("    return wall[6]"), fails_at=0, message_contains="out of range"),
        dict(why="a counted position [2] that fits the starter's [9, 8, 7] only", code=_long("    return wall[2]"),
             fails_at=2, message_contains="fits one wall only"),
        dict(why="the first item, not the last", code=_long("    return wall[0]"), fails_at=2,
             message_contains="last item"),
        dict(why="round brackets: the list called like a recipe (inside the recipe)", code=_long("    return wall(len(wall) - 1)"),
             fails_at=0, message_contains="not callable"),
        dict(why="the new line put under the old return 0", code=_long("    return 0\n    return wall[len(wall) - 1]"),
             fails_at=2, message_contains="placeholder"),
        dict(why="the ingredient renamed to the outside name",
             code=_long("    return chalk_wall[len(chalk_wall) - 1]", head="def newest_mark(chalk_wall):\n"),
             fails_at=2, message_contains="The ingredient on the `def` line"),
        dict(why="the whole list handed back", code=_long("    return wall"), fails_at=2, message_contains="whole list"),
        dict(why="the recipe's return left out entirely: no body", code=_long(""), fails_at=0,
             message_contains="indented block"),
        dict(why="min(wall): right only while the wall shrinks (the unsorted fresh wall catches it)",
             code=_long("    n = len(wall)\n    return min(wall)"), fails_at=2, message_contains="not 10"),
        dict(why="the last item handed back as text", code=_long("    return str(wall[len(wall) - 1])"), fails_at=2,
             message_contains="as text"),
        dict(why="the ingredient and the outside name mixed: stops the student's own Run on [9, 8, 7]",
             code=_long("    return wall[len(chalk_wall) - 1]"), fails_at=0, message_contains="out of range"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="list-append-len,param-use,return-value", solo="false",
             dictates="1", foreign_names="colors", par="([9, 6, 4],),([5],),([8, 12, 10],)") + "\n"
        "Recipe-shaped (D11), split in two (teacher ruling): CP1 [D] `len-minus-one`, a plain line with "
        "`chalk_wall[len(chalk_wall) - 1]`, then CP2 [ND] `newest-mark`, the recipe. tracer=True. Starter in file "
        "order (#1 above #2), with the teacher's two 'This should show' calls: the second, on `[9, 8, 7]`, makes a "
        "counted `wall[6]` or `wall[len(chalk_wall) - 1]` stop on the student's own Run. CP1 is CMB on a 5-gap and an "
        "8-gap wall with every top-level line that calls `newest_mark` left out of the rerun, so the recipe's printed "
        "line can never pass the plain line; `[6]` gets a rerun diagnosis (IndexError on 5 gaps), `[4]` too (wrong on "
        "8 gaps), and `[-1]` is told it works and this line practices `len - 1` (Unit 6's loops). `[len(chalk_wall)]` "
        "stops the student's own Run, so Python's IndexError and the explainer row name it before any check runs. "
        "CP2 accepts `wall[-1]` and `wall[len(wall) - 1]` (PAR compares values only): PAR on `[9, 6, 4]` -> 4, `[5]` "
        "-> 5 and the unsorted `[8, 12, 10]` -> 10 (none is the task's 37 or the starter's `[9, 8, 7]`, lint b), RET "
        "('handed back `None`: nothing came back', plus 'or hand back the box you made' for a box and a bare "
        "`return`), PAR-CONST ('both handed back 37'), and `chalk_wall` inside the recipe. WT = the 'Why does this "
        "work?' angle. BQ (combining two recipes): `oldest_mark(wall)` with PAR, then the shrink printed from both. "
        "Uses only u03a's planned concepts (def, a parameter, return)."
    ),
)


# 3A-07 ------------------------------------------------------------------------------------------

TYPO_LINE = "chalk_wall = [48, 48, 74, 46, 44, 41, 37]\n"
FIX_HEAD = "# Lucky copied the wall. One mark\n# is wrong: 74 should be 47.\n" + TYPO_LINE + "# Fix it by position here:\n"
FIX_STARTER = FIX_HEAD + "\nprint(chalk_wall)\n"


def _fix(line="chalk_wall[2] = 47", after=""):
    return FIX_HEAD + line + "\nprint(chalk_wall)\n" + after


FIX_CHECK = (
    "the wall reads 48, 48, 47, 46, 44, 41, 37",
    "import ast as _ast\n"
    "_tree = _ast.parse(_source)\n"
    "_v = chalk_wall\n"
    f"_right = {WALL!r}\n"
    "_typo = [48, 48, 74, 46, 44, 41, 37]\n"
    "assert type(_v).__name__ == 'list', ('`chalk_wall` isn' + chr(39) + 't a list anymore. Keep the wall' + chr(39) + 's '\n"
    "    'line as it is, and change one mark by its position, with `=`.')\n"
    "if _v != _right:\n"
    "    _asks = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare' "
    "and type(_n.value.left).__name__ == 'Subscript']\n"
    "    _diff = [_i for _i in range(min(7, len(_v))) if _v[_i] != _typo[_i]]\n"
    "    if _v == _typo and _asks:\n"
    "        _msg = ('Line ' + str(_asks[0]) + ' asks a yes-or-no question with `==`, so nothing changes. One `=` '\n"
    "                'puts 47 in its place.')\n"
    "    elif len(_v) > 7 and _v[:7] == _typo:\n"
    "        _msg = ('`.append()` added a new mark at the end, so the 74 is still there. Change the 74 where it is, '\n"
    "                'by its position, with `=`.')\n"
    "    elif '47' in _v:\n"
    "        _msg = '`\"47\"` is text, because of the quotes. Marks are numbers: take the quotes off.'\n"
    "    elif 74 in _v and _diff:\n"
    "        _msg = ('You changed position ' + str(_diff[0]) + ', but the 74 isn' + chr(39) + 't there. Positions start '\n"
    "                'at 0: 48 is at 0, 48 is at 1. Count on from there.')\n"
    "    elif _v == _typo:\n"
    "        _msg = ('74 is still on the wall. Change it by its position: `chalk_wall[`, the position, `] = 47`.')\n"
    "    elif len(_v) == 7 and 74 not in _v and _v[2] != 47:\n"
    "        _msg = 'You changed the right position, but not to 47. Put 47 there.'\n"
    "    else:\n"
    "        _msg = 'Your wall doesn' + chr(39) + 't read 48, 48, 47, 46, 44, 41, 37. Change only the 74.'\n"
    "    assert False, _msg",
)

BY_POSITION = (
    "fixed by position, not retyped",
    "import ast as _ast\n"
    "_set = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
    "and any(type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name' "
    "and (_t.value.id == 'chalk_wall' or globals().get(_t.value.id) is chalk_wall) for _t in _n.targets)]\n"
    "assert _set, ('You fixed the wall without a line that changes it by position. Fix it by position. Lists '\n"
    "    'often come from somewhere you can' + chr(39) + 't retype, like `caster` in the campaign: `chalk_wall[`, '\n"
    "    'the position, `] = 47` on line 5.')",
)

# The fix by position must do the mending: with Lucky's line put back (74 and all), the wall still ends right.
# Catches an edited line 3 (or a retyped wall) plus a do-nothing `chalk_wall[0] = 48`.
FIX_DOES_IT = follows(
    "the fix by position mends Lucky's 74",
    {"chalk_wall": [48, 48, 74, 46, 44, 41, 37]},
    f"_R('chalk_wall') == {WALL!r}",
    fix="You changed the wall's line, not the 74's position. Leave the wall's line as it was, 74 and all, and fix "
        "the 74 on line 5.",
    ev="Mar'tu tested your code with the 74 put back",
    saw="'the wall still read ' + _sh(_R('chalk_wall'))",
)

FIX_A_MARK = dict(
    id="fix-a-mark",
    title="Fix a mark",
    martu=(
        "You can change one item by its position. `party_colors[1] = \"violet\"` puts violet at position 1, in "
        "place of teal. It's like the whiteboard in Unit 1, where a new `=` wiped the old value. Here it wipes "
        "only one spot. The rest of the list stays as it is.\n"
        "Lucky copied my wall, and one mark is wrong: 74 where 47 belongs. His handwriting, yes? Fix it by its "
        "position. No need to retype anything."
    ),
    example='party_colors = ["gold", "teal"]\nparty_colors[1] = "violet"\nprint(party_colors)\n',
    example_output="['gold', 'violet']",
    names=["chalk_wall"],
    starter=FIX_STARTER,
    checkpoints=[
        dict(
            id="fix-by-position",
            text=(
                "On line 5, the empty line under `# Fix it by position here:`, change the 74 to 47 by its position. "
                "Don't retype the list."
            ),
            dictated=False,
            hints=[
                "Count the positions from 0: 48 is at 0, 48 is at 1, and 74 is at...?",
                "`party_colors[1] = \"violet\"` puts a new value at position 1. Position in square brackets, then "
                "`=`, then the new value.",
                "On line 5, the empty line, write `chalk_wall[` and the 74's position, then `] = 47`: "
                "`chalk_wall[2] = 47`.",
            ],
            checks=[
                have_list("chalk_wall", known=["chalk_wall"], foreign=["party_colors"]),
                FIX_CHECK,
                BY_POSITION,
                FIX_DOES_IT,
                printed_after("chalk_wall", "the fix"),
            ],
            pass_line="You fixed one mark by its position, with nothing retyped. Mar'tu: Lucky will deny it was him.",
        ),
    ],
    solution=_fix(),
    assemble=dict(
        lines=["chalk_wall = [48, 48, 74, 46, 44, 41, 37]", "chalk_wall[2] = 47", "print(chalk_wall)"],
        distractors=["chalk_wall[3] = 47", "chalk_wall[2] == 47", "chalk_wall.append(47)"],
    ),
    another_way=[
        dict(
            angle="picture",
            text="```text\nposition: 0  1  2  3 ...\n          48 48 74 46 ...\n                ^\n          chalk_wall[2] = 47\n```",
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Find the wrong mark: 74.\n2. Count its position from 0: 0, 1, 2.\n"
                "3. Write the list's name, the position in square brackets, `=`, and the right mark."
            ),
        ),
        dict(
            angle="everyday",
            label="Fix one word",
            text=(
                "When one word in your notes is wrong, you erase that word. You don't copy out the whole page "
                "again. Same here: change one item, keep the rest."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        why=(
            "You've seen this shape in `cast_spell`: `caster[\"mana\"] = ...`. A name, square brackets, then `=`. "
            "It changed one value inside the caster and left the rest alone. `chalk_wall[2] = 47` does the same to "
            "one mark."
        ),
    ),
    takeaway="`wall[2] = 47` changes the item at position 2. The rest of the list stays as it is.",
    wrong_answers=[
        dict(why="starter unchanged: 74 still there", code=FIX_STARTER, fails_at=1, message_contains="still on the wall"),
        dict(why="the whole list retyped (spec)", code=_fix("chalk_wall = [48, 48, 47, 46, 44, 41, 37]"), fails_at=1,
             message_contains="Fix it by position. Lists often come from somewhere you can't retype"),
        dict(why="Lucky's line edited instead of fixed by position",
             code=FIX_STARTER.replace(TYPO_LINE, WALL_LINE), fails_at=1,
             message_contains="like `caster` in the campaign"),
        dict(why="asks for item 3 for the third mark: off by one", code=_fix("chalk_wall[3] = 47"), fails_at=1,
             message_contains="Positions start at 0"),
        dict(why="== asks instead of = changing", code=_fix("chalk_wall[2] == 47"), fails_at=1, message_contains="`=="),
        dict(why="round brackets: assigning to a call", code=_fix("chalk_wall(2) = 47"), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="the new mark in quotes", code=_fix('chalk_wall[2] = "47"'), fails_at=1, message_contains="text"),
        dict(why="append adds an 8th mark instead", code=_fix("chalk_wall.append(47)"), fails_at=1,
             message_contains=".append()"),
        dict(why="the fix put after the print", code=_fix("", after="chalk_wall[2] = 47\n"), fails_at=1,
             message_contains="runs before"),
        dict(why="position 7: IndexError", code=_fix("chalk_wall[7] = 47"), fails_at=0, message_contains="out of range"),
        dict(why="right place, wrong mark", code=_fix("chalk_wall[2] = 46"), fails_at=1, message_contains="right position"),
        dict(why="Lucky's line edited by hand, plus a do-nothing change by position to pass",
             code=FIX_STARTER.replace(TYPO_LINE, WALL_LINE).replace("\nprint", "chalk_wall[0] = 48\nprint"), fails_at=1,
             message_contains="Leave the wall's line"),
        dict(why="the wall retyped, plus a do-nothing change by position", code=_fix("chalk_wall = [48, 48, 47, 46, 44, 41, 37]\n"
             "chalk_wall[0] = 48"), fails_at=1, message_contains="Leave the wall's line"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-index", solo="false", dictates="",
             foreign_names="party_colors") + "\n"
        "Spec flags CP1 [D]; the text gives the goal and the name ('Fix the 74 by its position. Don't retype the "
        "list.') but not the position, which is the point of the step, so it is marked dictated=False. Checks: the "
        "wall is right (with the off-by-one, `==`, `.append()` and text slips named), an Assign to a Subscript of "
        "`chalk_wall` (a retyped list or an edited starter line fails with 'Fix it by position. Lists often come "
        "from somewhere you can't retype, like `caster` in the campaign', spec WA; teacher ruling), a rerun with Lucky's "
        "line put back (so an edited line 3 plus a do-nothing `chalk_wall[0] = 48` fails), and the print shows "
        "the fixed wall. Campaign link: `caster[\"mana\"] = ...` in `cast_spell`, the same name-brackets-equals shape."
    ),
)

# 3A-09 ------------------------------------------------------------------------------------------

NEST_STARTER = ROSTER_CODE + "# 1. Print Bomb Shell's name.\n\n# 2. Print Oogrish's mana.\n\n"


def _nest(name="print(roster[2][0])", mana="print(roster[0][1])"):
    return ROSTER_CODE + "# 1. Print Bomb Shell's name.\n" + name + "\n# 2. Print Oogrish's mana.\n" + mana + "\n"


_RO = "_C['roster']"
_RM = "_g0.get('roster')"

NAME_CHECK = follows(
    "Bomb Shell's name follows the roster",
    {"roster": OTHER_ROSTER},
    f"_said({_RO}[2][0])",
    rules=[
        (f"_rowp({_RO}[2])", "Your line shows Bomb Shell's whole row. Add a second position for the name: `[0]`.",
         None),
        (f"_said({_RO}[2][1])", "Your line shows the mana. The name is item 0 of the row.", None),
        (f"_said({_RO}[3][0]) or _said({_RO}[1][0])",
         "Your line reads the wrong row. Count the rows from 0: Bomb Shell is row 2.", None),
        (f"_said({_RM}[2][0])", "You typed the name instead of reading it from `roster`. Read it by position: "
         "`roster[2][0]`.",
         f"'it still printed `' + str({_RM}[2][0]) + '`'"),
    ],
    fix="Your code doesn't show Bomb Shell's name yet. Read it at row 2, then item 0: `roster[2][0]`.",
    ev=ROSTER_EV,
    kind="roster",
)

MANA_CHECK = follows(
    "Oogrish's mana follows the roster",
    {"roster": OTHER_ROSTER},
    f"_said({_RO}[0][1])",
    rules=[
        (f"_rowp({_RO}[0])", "Your line shows Oogrish's whole row. Add a second position for the mana.", None),
        (f"_said({_RO}[0][0])", "Your line shows the name. The mana is item 1 of the row.", None),
        (f"_said({_RO}[1][1])", "Your line reads the wrong row. Count the rows from 0: Oogrish's row is row 0.", None),
        (f"_said({_RM}[0][1])", "You typed the mana instead of reading it from `roster`. Read it by position: row "
         "first, then item.",
         f"'it still printed `' + str({_RM}[0][1]) + '`'"),
    ],
    fix="Your code doesn't show Oogrish's mana yet. Read it from `roster`: his row first, then the mana's "
        "position in the row.",
    ev=ROSTER_EV,
    kind="roster",
)

ROSTER_ROWS = [["Oogrish", 18], ["Gearshift", 20], ["Bomb Shell", 24], ["Lucky", 26]]

# Lucky's side quest: your own hero's row, appended. Any name (text) and any whole-number mana pass; the messages
# never repeat the student's own name or number.
OWN_ROW = (
    "roster grows by one row",
    "_v = roster\n"
    f"_base = {ROSTER_ROWS!r}\n"
    "assert type(_v).__name__ == 'list', ('`roster` isn' + chr(39) + 't a list of rows anymore. Keep its lines as '\n"
    "    'they were, and add your row with `.append()`.')\n"
    "assert _v[:4] == _base, 'The four rows at the top have changed. Put them back the way they were. Your hero goes at the end.'\n"
    "assert len(_v) > 4, ('`roster` still has 4 rows. Add your hero' + chr(39) + 's row to the end: '\n"
    "    '`roster.append(`.')\n"
    "_new = _v[4:]\n"
    "assert not (len(_new) > 1 and not any(type(_x).__name__ == 'list' for _x in _new)), ('Your code added the '\n"
    "    'name and the mana as two separate items. Put them in one row, inside square brackets, like Lucky' + chr(39) + "
    "'s row.')\n"
    "assert len(_new) == 1, ('Your code added more than one row: `roster` now has ' + str(len(_v)) + ' rows. Add '\n"
    "    'one row, your hero' + chr(39) + 's.')",
)

OWN_ROW_SHAPE = (
    "the new row is a name and a whole number",
    "_r = roster[4]\n"
    "assert type(_r).__name__ == 'list', ('Your code added one item on its own, not a row. A row is a small list: '\n"
    "    'the name and the mana inside square brackets, like Lucky' + chr(39) + 's row.')\n"
    "assert len(_r) == 2, 'Your row doesn' + chr(39) + 't hold two items. A row holds a name, then a mana number.'\n"
    "_t0, _t1 = type(_r[0]).__name__, type(_r[1]).__name__\n"
    "assert not (_t0 == 'int' and _t1 == 'str'), 'Your row has the mana first. Name first, then mana, like every other row: swap the two.'\n"
    "assert _t0 == 'str', 'The first item in your row isn' + chr(39) + 't text. The name goes first, in quotes, like `\"Lucky\"`.'\n"
    "assert _t1 != 'str', 'The mana is text, because of the quotes. Mana is a number: take the quotes off.'\n"
    "assert _t1 == 'int', 'Your mana isn' + chr(39) + 't a whole number. Use a whole number, like the other rows.'",
)

OWN_ROW_APPEND = (
    "the row goes in with .append()",
    "import ast as _ast\n"
    "_app = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
    "and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'append' "
    "and type(_n.func.value).__name__ == 'Name' and _n.func.value.id == 'roster']\n"
    "assert _app, ('Your code makes a new roster instead of adding to it. This side quest practices `.append()`: '\n"
    "    '`roster.append(` and your row `)`.')",
)

LISTS_INSIDE_LISTS = dict(
    id="lists-inside-lists",
    title="Lists inside lists",
    martu=(
        "A list can hold lists: a [[list inside a list]]. Read it like a theater ticket: row first, then seat. "
        "In `roster`, each row is a small list: a hero's name, then their mana (magic power). `roster[3]` is row "
        "3, Lucky's. `roster[3][1]` reads row 3, then item 1 inside it:\n"
        "```text\nroster[3][1]\n      |  |\n      |  +-- item 1 of that row\n      +----- row 3: [\"Lucky\", 26]\n```\n"
        "Rows and items both count from 0, so row 3 is the fourth row."
    ),
    example='shelf = [["salt", 3], ["chalk", 9]]\nprint(shelf[1][0])\nprint(shelf[1][1])\n',
    example_output="chalk\n9",
    names=["roster"],
    predict=dict(
        q="What will `roster[3][1]` print?",
        code=ROSTER_CODE + "print(roster[3][1])\n",
        choices=["26", "Lucky", "24", "['Lucky', 26]"],
        answer=0,
        explain=(
            "`roster[3]` is row 3, Lucky's: `[\"Lucky\", 26]`. Then `[1]` is item 1 of that row: 26. Row first, "
            "then item."
        ),
    ),
    pair_talk=(
        "Pair talk: before you run, each of you writes down what `roster[3][1]` shows. Compare your answers, "
        "then run it on your own screens."
    ),
    starter=NEST_STARTER,
    checkpoints=[
        dict(
            id="bomb-shell-name",
            text=(
                "On line 8, under `# 1.`, type `print(roster[2][0])`: row 2, then item 0. You should see Bomb "
                "Shell."
            ),
            dictated=True,
            hints=[
                "Look at the roster. Bomb Shell's row is the third row, and rows count from 0. The name is first in "
                "the row.",
                "In the Example, `shelf[1][0]` reads row 1, then item 0 of that row: chalk.",
                "Write `print(roster[2][0])` under the `# 1.` note.",
            ],
            checks=[have_list("roster", known=["roster"], foreign=["shelf"]), NAME_CHECK],
            pass_line="You read Bomb Shell's name: row 2, then item 0. Bomb Shell: Correct.",
        ),
        dict(
            id="oogrish-mana",
            text=(
                "On line 10, under `# 2.`, show Oogrish's mana from `roster`. Read his row first, then the mana's "
                "place in that row."
            ),
            dictated=False,
            hints=[
                "Which row is Oogrish's? Rows count from 0. Where is the mana inside a row?",
                "Row first, then item: `shelf[1][1]` is row 1, item 1, which is 9.",
                "Write `print(roster[0][1])` under the `# 2.` note.",
            ],
            checks=[MANA_CHECK],
            pass_line="You read Oogrish's mana from his row. Oogrish: Eighteen. Not much, but steady.",
        ),
    ],
    solution=_nest(),
    partials=[_nest(mana="")],
    assemble=dict(
        lines=["roster = [", '    ["Oogrish", 18],', '    ["Gearshift", 20],', '    ["Bomb Shell", 24],',
               '    ["Lucky", 26],', "]", "print(roster[2][0])", "print(roster[0][1])"],
        distractors=["print(roster[2])", "print(roster[3][0])", "print(roster[1][2])"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A table of rows",
            text=(
                "```text\nrow  item 0         item 1\n 0   \"Oogrish\"      18\n 1   \"Gearshift\"    20\n"
                " 2   \"Bomb Shell\"   24\n 3   \"Lucky\"        26\n```\nRow first, then the item."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "Read `roster[2][0]` left to right:\n1. `roster[2]` is the row `[\"Bomb Shell\", 24]`.\n"
                "2. `[0]` of that row is `\"Bomb Shell\"`.\nRow first, then item."
            ),
        ),
        dict(
            angle="everyday",
            label="A shelf of small shelves",
            text=(
                "A big shelf holds four small shelves. Pick a small shelf first, then a jar on it. Two numbers, "
                "always in that order."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Think of each hero's row as a small card with a name and a mana number on it. In Unit 5, each card "
                "gets a tag for each value, in place of a position."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Put your hero on the roster",
        text=(
            "Lucky wants you on the roster. At the bottom, add your own hero's row with `roster.append( )`: a name "
            "in quotes, then a mana number, in square brackets."
        ),
        hints=[
            "A row is a small list, like `[\"Lucky\", 26]`: the name in quotes, a comma, then the mana. The whole "
            "row goes inside the parentheses of `.append( )`.",
            "Write `roster.append([\"Fenn\", 12])` at the bottom, with your own hero's name and mana.",
        ],
        checks=[OWN_ROW, OWN_ROW_SHAPE, OWN_ROW_APPEND],
        solution=_nest() + 'roster.append(["Fenn", 12])\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["abilities"]["magical_affinity"]',
        why=(
            "You've seen this in `cast_spell`: two lookups in a row. First the caster's abilities, then the "
            "affinity (how strong the hero's magic is) inside them. `roster[3][1]` reads the same way: outside "
            "first, then inside."
        ),
    ),
    takeaway="`roster[2][0]` reads row 2 first, then item 0 of that row. Row first, then item.",
    wrong_answers=[
        dict(why="starter unchanged: nothing printed", code=NEST_STARTER, fails_at=1, message_contains="row 2, then item 0"),
        dict(why="only the row (spec)", code=_nest(name="print(roster[2])"), fails_at=1, message_contains="whole row"),
        dict(why="the name typed by hand", code=_nest(name='print("Bomb Shell")'), fails_at=1,
             message_contains="reading it from `roster`"),
        dict(why="asks for row 3 for the third hero: off by one", code=_nest(name="print(roster[3][0])"), fails_at=1,
             message_contains="from 0"),
        dict(why="the mana, not the name", code=_nest(name="print(roster[2][1])"), fails_at=1, message_contains="item 0"),
        dict(why="the inner position too big (spec): IndexError", code=_nest(mana="print(roster[1][2])"), fails_at=0,
             message_contains="out of range"),
        dict(why="Oogrish's whole row", code=_nest(mana="print(roster[0])"), fails_at=2, message_contains="whole row"),
        dict(why="the mana typed by hand", code=_nest(mana="print(18)"), fails_at=2, message_contains="typed the mana"),
        dict(why="row 1 for the first hero: off by one", code=_nest(mana="print(roster[1][1])"), fails_at=2,
             message_contains="row 0"),
        dict(why="Oogrish's name, not his mana", code=_nest(mana="print(roster[0][0])"), fails_at=2,
             message_contains="item 1"),
        dict(why="a comma between the positions: TypeError", code=_nest(name="print(roster[2, 0])"), fails_at=0,
             message_contains="not tuple"),
        dict(why="Lucky's side quest: the hero's name with no quotes (NameError)",
             code=_nest() + "roster.append([Fenn, 12])\n", fails_at=0, message_contains="not defined"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-nested", solo="false", dictates="1",
             foreign_names="shelf") + "\n"
        "Spec: predict `roster[3][1]`; CP1 [D] Bomb Shell's name, CP2 [ND] Oogrish's mana; checks CMB on another "
        "roster (Pell 31, Brakka 7, Moss 15, Glug 3: invented values), so a typed name or number fails and each "
        "slip is named (a whole row, the other item of the row, the row off by one). The roster is written one row "
        "per line (phone width; it also looks like boxes in boxes). TR = the boxes-in-boxes picture angle. "
        "The Example reads `shelf[1][0]` and `shelf[1][1]` (teacher ruling), so CP2 (`roster[0][1]`) cannot be "
        "done by copying the Example and renaming it. BQ (combining append + a list inside a list; teacher ruling, "
        "in place of the total mana): your own hero's row appended to `roster`, any name and any whole-number mana "
        "(checks: one new row, `[text, whole number]`, made with `.append`); the unquoted name is a NameError (WA). "
        "Prepares nested dicts (Unit 5)."
    ),
)


# 3A-10 ------------------------------------------------------------------------------------------

BROKEN_WALL = "chalk_wall = [48 48, 47, 46, 44, 41, 37]"
BROKEN_TAIL = 'print("Oldest gap:", oldest)\nprint("Newest gap:", newest)\n'


def _broken(wall=WALL_LINE.strip(), oldest="oldest = chalk_wall[0]", newest="newest = chalk_wall[-1]"):
    return f"{wall}\n{oldest}\n{newest}\n" + BROKEN_TAIL


BROKEN_STARTER = _broken(BROKEN_WALL, "oldest = chalk_wall(0)", "newest = chalk_wall[7]")

BROKEN_OLDEST = follows(
    "oldest reads the first gap (another wall)",
    {"chalk_wall": W5},
    f"_R('oldest') == {_W}[0]",
    rules=[
        (f"_R('oldest') == {_W}[1]", "`oldest` reads position 1, the second gap. Positions start at 0, so the first "
         "gap is `chalk_wall[0]`.", None),
        ("_R('oldest') == _g0.get('oldest')", "You typed the gap into `oldest` instead of reading it from the list. "
         "Use `chalk_wall[0]`.",
         "'`oldest` stayed ' + _sh(_g0.get('oldest'))"),
    ],
    fix="`oldest` doesn't hold the first gap. Read it with square brackets: `chalk_wall[0]`.",
    ev=WALL_EV5,
    saw="'`oldest` became ' + _sh(_R('oldest'))",
    crash=[("_e.startswith('IndexError')", "The first gap is at position 0 on a wall of any length: `chalk_wall[0]`.")],
    own=(
        "_W0 is None or _g0.get('oldest') == _W0[0]",
        "'On your wall `oldest` holds ' + _sh(_g0.get('oldest')) + ', but the first gap is ' + str(_W0[0]) + '. "
        "Positions start at 0: `chalk_wall[0]`.'",
    ),
)

BROKEN_NEWEST = follows(
    "newest reads the last gap (another wall)",
    {"chalk_wall": W5},
    f"_R('newest') == {_W}[-1]",
    rules=[
        ("_R('newest') == _g0.get('newest')", "You typed the gap into `newest` instead of reading it from the list. "
         "Count from the end: `-1`.",
         "'`newest` stayed ' + _sh(_g0.get('newest'))"),
    ],
    fix="`newest` doesn't hold the last gap. Read it by counting from the end: `-1`.",
    ev=WALL_EV5,
    saw="'`newest` became ' + _sh(_R('newest'))",
    crash=[("_e.startswith('IndexError')", "Count from the end with `[-1]`, so `newest` fits a wall of any length.")],
    own=(
        "_W0 is None or _g0.get('newest') == _W0[-1]",
        "'On your wall `newest` holds ' + _sh(_g0.get('newest')) + ', but the last gap is ' + str(_W0[-1]) + '. "
        "Count from the end: `-1`.'",
    ),
)

BROKEN_SPELL_3A = dict(
    id="broken-spell-3a",
    title="Broken spell",
    martu=(
        "This code has three [[bug|bugs]], all loud: each one makes Python stop with an error. "
        "Python shows one error at a time, so fix one, press Run again, and see what Python finds next. A new "
        "error is good news: Python got further.\n"
        "When Python stops, read the box in the Console, in this order:\n"
        "1. Read its title. It says what went wrong.\n"
        "2. Read *Python's last line*. It says the same thing in Python's words.\n"
        "3. Find the line number, and fix that line."
    ),
    names=["chalk_wall", "oldest", "newest"],
    pair_talk=(
        "Pair talk: you may hunt these bugs together. One of you reads the box's title and Python's last line out "
        "loud. The other finds the line number. Then each of you fixes it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-the-commas",
            text="Fix line 1 so `chalk_wall` holds the seven gaps.",
            dictated=False,
            hints=[
                "Read the box in the Console: first its title, then Python's last line, `SyntaxError: invalid "
                "syntax. Perhaps you forgot a comma?`",
                "Inside a list, a comma goes between each two items: `[5, 9, 2]`, never `[5 9, 2]`. Look at line 1, "
                "between the first two gaps.",
                "Type `,` right after the first `48` on line 1. Line 1 becomes "
                "`chalk_wall = [48, 48, 47, 46, 44, 41, 37]`.",
            ],
            checks=[have_list("chalk_wall", known=["chalk_wall", "oldest", "newest"]), wall_value(line="on line 1")],
        ),
        dict(
            id="mend-the-brackets",
            text="Fix line 2 so `oldest` reads the first gap from the list.",
            dictated=False,
            hints=[
                "Press Run again and read the new box: first its title, then Python's last line, `TypeError: "
                "'list' object is not callable`.",
                "Look at line 2. Parentheses `( )` after a name call it, like a recipe. Square brackets `[ ]` read a "
                "list: `colors[0]`.",
                "Change `(0)` to `[0]` on line 2. Line 2 becomes `oldest = chalk_wall[0]`.",
            ],
            checks=[have_list("oldest", known=["chalk_wall", "oldest", "newest"], what="box"), BROKEN_OLDEST],
            pass_line="Two loud bugs fixed. Mar'tu: Square brackets read a list. Parentheses call a recipe.",
        ),
        dict(
            id="mend-the-position",
            text="Fix line 3 so `newest` reads the last gap, on a wall of any length.",
            dictated=False,
            hints=[
                "Press Run again and read the new box: first its title, then Python's last line, `IndexError: list "
                "index out of range`.",
                "Look at line 3. Seven gaps sit at positions 0 to 6, so there is no position 7. `colors[-1]` is the "
                "last item of a list of any length.",
                "Change `[7]` to `[-1]` on line 3. Line 3 becomes `newest = chalk_wall[-1]`.",
            ],
            checks=[have_list("newest", known=["chalk_wall", "oldest", "newest"], what="box"), BROKEN_NEWEST],
            pass_line="All three bugs fixed. Mar'tu: You read the box first, every time. Good habit, yes?",
        ),
    ],
    solution=_broken(),
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "oldest = chalk_wall[0]", "newest = chalk_wall[-1]",
               'print("Oldest gap:", oldest)', 'print("Newest gap:", newest)'],
        distractors=["oldest = chalk_wall(0)", "newest = chalk_wall[7]", "newest = chalk_wall[len(chalk_wall)]"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Press Run. Python checks the grammar (the syntax) of every line before it runs any of them, so "
                "the comma bug on line 1 shows first.\n"
                "2. Fix it and press Run again. A new error is good news: Python got further.\n"
                "3. Fix line 2, then line 3, the same way."
            ),
        ),
        dict(
            angle="picture",
            label="Three bugs, three messages",
            text=(
                "```text\n[48 48, ...]  -> forgot a comma\nwall(0)       -> not callable\n"
                "wall[7]       -> out of range\n```"
            ),
        ),
        dict(
            angle="shorter",
            text="A comma between gaps. Square brackets to read. `-1` for the last.",
        ),
    ],
    takeaway="Commas between items, square brackets to read, and `[-1]` for the last item on any list.",
    wrong_answers=[
        dict(why="the starter: no comma between 48 and 48 (SyntaxError first)", code=BROKEN_STARTER, fails_at=0,
             message_contains="forgot a comma"),
        dict(why="commas mended, the list still called with ()", code=_broken(oldest="oldest = chalk_wall(0)",
             newest="newest = chalk_wall[7]"), fails_at=0, message_contains="not callable"),
        dict(why="commas and brackets mended, position 7 left", code=_broken(newest="newest = chalk_wall[7]"),
             fails_at=0, message_contains="out of range"),
        dict(why="len(list) used as the position", code=_broken(newest="newest = chalk_wall[len(chalk_wall)]"),
             fails_at=0, message_contains="out of range"),
        dict(why="mended to [6]: fits 7 gaps only", code=_broken(newest="newest = chalk_wall[6]"), fails_at=3,
             message_contains="any length"),
        dict(why="the newest gap typed by hand", code=_broken(newest="newest = 37"), fails_at=3,
             message_contains="instead of reading it from the list"),
        dict(why="item 1 asked for to get the first", code=_broken(oldest="oldest = chalk_wall[1]"), fails_at=2,
             message_contains="Positions start at 0"),
        dict(why="the oldest gap typed by hand", code=_broken(oldest="oldest = 48"), fails_at=2,
             message_contains="instead of reading it from the list"),
        dict(why="comma mended by dropping a gap", code=_broken(wall="chalk_wall = [48, 47, 46, 44, 41, 37]"),
             fails_at=1, message_contains="6 gaps"),
        dict(why="quotes added around the gaps", code=_broken(wall='chalk_wall = ["48", "48", "47", "46", "44", "41", "37"]'),
             fails_at=1, message_contains="numbers"),
        dict(why="-7 for the first gap: fits 7 gaps only", code=_broken(oldest="oldest = chalk_wall[-7]"), fails_at=2,
             message_contains="position 0 on a wall of any length"),
        dict(why="a position counted for the check's 5-gap wall: [-5] is the first of 5, not of 7",
             code=_broken(oldest="oldest = chalk_wall[-5]"), fails_at=2, message_contains="On your wall `oldest` holds"),
        dict(why="[4] for the newest: the last of 5 gaps, not of 7", code=_broken(newest="newest = chalk_wall[4]"),
             fails_at=3, message_contains="On your wall `newest` holds"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="list-make,list-index,read-traceback", solo="false", dictates="",
             foreign_names="colors") + "\n"
        "Spec bugs, one checkpoint each, in the order Python's messages arrive (verified, Python 3.13): `[48 48, ...]` "
        "(SyntaxError 'Perhaps you forgot a comma?', found before anything runs), `chalk_wall(0)` (TypeError "
        "''list' object is not callable'; the spec's new explainer row, 'Read a list with square brackets: "
        "`chalk_wall[0]`', is site work in explain.ts, not in this file), `chalk_wall[7]` (IndexError). A crash "
        "fails every checkpoint, so each loud bug left fails at 0 and there are no partials (as 2A's broken spell). "
        "CP2 and CP3 are CMB on another wall, so a typed 48 or 37, `[1]`, and a mend to `[6]` are all caught; the "
        "student's own wall is checked too, so a position that only fits the 5-gap wall (`[-5]`, `[4]`) fails. "
        "Rung 0 is 'Read Python's last line'. Can be done in pairs; every student mends it on their own screen."
    ),
)

# 3A-S -------------------------------------------------------------------------------------------

# Teacher ruling on the Unit 4 reviews: the quiet recipe slip, `chalk_wall` read inside `newest_mark`, so the
# SOLO gives evidence on the CC recipe skill (objective 5) instead of a third copy of the `[7]` to `[-1]` fix.
# Python never stops; the starter's second "This should show" call, on `[9, 8, 7]`, shows 37 where 7 belongs.
SOLO_A_CALLS = (
    "\nprint(newest_mark(chalk_wall))  # This should show 37\n"
    "print(newest_mark([9, 8, 7]))  # This should show 7\n"
)


def _solo_a(body="    return wall[-1]", head="def newest_mark(wall):\n"):
    return WALL_LINE + head + body + "\n" + SOLO_A_CALLS


SOLO_A_STARTER = _solo_a("    return chalk_wall[-1]")

SOLO_3A = dict(
    id="solo-3a",
    title="Show Mar'tu",
    martu=(
        "This code has one quiet [[bug]]: it runs, but gives a wrong answer. Python won't stop, so compare the "
        "Console with the notes on the last two lines. Does the recipe find the newest mark of any wall it is "
        "handed? Fix it on your own."
    ),
    solo=True,
    explainer="lean",
    names=["newest_mark", "wall"],
    starter=SOLO_A_STARTER,
    checkpoints=[
        dict(
            id="newest-of-any-wall",
            text="Change `newest_mark` so it hands back the last item of any wall it is handed.",
            dictated=False,
            hints=[
                "Look at the Console. The second line should show 7, as the note on the last line says. What does "
                "it show?",
                "Line 3 reads `chalk_wall`. What is the list called inside the recipe?",
                "Inside a recipe, use the ingredient's name: `return wall[-1]` works on any wall the call hands over.",
            ],
            checks=[
                recipe_par("newest_mark hands back the last item of a fresh wall", "newest_mark", "len(wall) - 1",
                           "last", lean=True),
            ],
            pass_line="Mar'tu: You did that on your own. Your recipe reads the list it is handed.",
        ),
    ],
    solution=_solo_a(),
    # No Assemble it (honest evidence, as Unit 3's ledger): its pieces would put `return wall[-1]` beside the
    # starter's `return chalk_wall[-1]`, the SOLO's one decision, ahead of every hint.
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "The call `newest_mark([9, 8, 7])` hands over `[9, 8, 7]`. Inside the recipe, that list is `wall`. "
                "`chalk_wall` is still the big wall outside."
            ),
        ),
        dict(angle="shorter", text="Inside a recipe, read the ingredient, not the outside name."),
    ],
    takeaway="On your own: a recipe reads the list it is handed (`wall`), not a list from outside.",
    wrong_answers=[
        dict(why="starter unchanged: the outside name read inside the recipe (the quiet slip)", code=SOLO_A_STARTER,
             fails_at=1, message_contains="reads the list from outside"),
        dict(why="the second call's answer typed in: return 7", code=_solo_a("    return 7"), fails_at=1,
             message_contains="same answer for every wall"),
        dict(why="the first call's answer typed in: return 37", code=_solo_a("    return 37"), fails_at=1,
             message_contains="same answer for every wall"),
        dict(why="the outside name kept, the long way: chalk_wall[len(chalk_wall) - 1]",
             code=_solo_a("    return chalk_wall[len(chalk_wall) - 1]"), fails_at=1,
             message_contains="reads the list from outside"),
        dict(why="the ingredient and the outside name mixed: chalk_wall[len(wall) - 1]",
             code=_solo_a("    return chalk_wall[len(wall) - 1]"), fails_at=1, message_contains="reads the list from outside"),
        dict(why="print for return: the item is shown, nothing comes back", code=_solo_a("    print(wall[-1])"),
             fails_at=1, message_contains="prints the item but does not hand it back"),
        dict(why="len(list) used as the position: IndexError on the student's own Run",
             code=_solo_a("    return wall[len(wall)]"), fails_at=0, message_contains="out of range"),
        dict(why="a counted position [6]: the call on [9, 8, 7] stops the student's own Run",
             code=_solo_a("    return wall[6]"), fails_at=0, message_contains="out of range"),
        dict(why="a counted position [2] that fits [9, 8, 7] only", code=_solo_a("    return wall[2]"), fails_at=1,
             message_contains="a position the wall doesn't have"),
        dict(why="the first item, not the last", code=_solo_a("    return wall[0]"), fails_at=1,
             message_contains="wrong item"),
        dict(why="hands back the count", code=_solo_a("    return len(wall)"), fails_at=1, message_contains="the count"),
        dict(why="hands back the last position, not the item", code=_solo_a("    return len(wall) - 1"), fails_at=1,
             message_contains="a position, not the item"),
        dict(why="a box made, then a bare return", code=_solo_a("    last = wall[-1]\n    return"), fails_at=1,
             message_contains="makes a variable, then hands back nothing"),
        dict(why="the ingredient renamed to the outside name", code=_solo_a("    return chalk_wall[-1]",
             head="def newest_mark(chalk_wall):\n"), fails_at=1, message_contains="ingredient"),
        dict(why="round brackets: the list called like a recipe", code=_solo_a("    return wall(-1)"), fails_at=0,
             message_contains="not callable"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="param-use,return-value,list-index", solo="true", dictates="",
             foreign_names="", par="([9, 6, 4],),([5],),([8, 12, 10],)",
             seat_b='chalk_wall.append("33") (the guess as text; the mend is to take the quotes off)') + "\n"
        "SOLO, one bug (C6), explainer='lean' (teacher ruling from Unit 2 on: the crash explainer names the kind of "
        "slip and the line, not the fix). Teacher ruling on the Unit 4 reviews: seat A (and anyone solo) gets the "
        "quiet recipe slip, `return chalk_wall[-1]` inside `newest_mark(wall)`, so the SOLO gives evidence on the "
        "CC recipe skill (3A-06 CP2) rather than a third `[7]` to `[-1]` fix. Python never stops: the starter's "
        "second call, `newest_mark([9, 8, 7])`, shows 37 where its comment says 7 (rung 0: 'Read what it printed'). "
        "Checked with recipe_par(lean=True) on the fresh walls `[9, 6, 4]`, `[5]` and `[8, 12, 10]`, so "
        "`wall[-1]` and `wall[len(wall) - 1]` both pass and a typed 7 or 37, `chalk_wall` inside, `print` for "
        "`return`, `[2]`, the count and the position all fail; each lean message names the slip and keeps the "
        "evidence bracket ('Mar'tu's check called ...'), with no code and no fix. `wall[len(wall)]` and `wall[6]` "
        "stop the student's own Run (IndexError), so the lean explainer names them. Seat B would get "
        "`chalk_wall.append(\"33\")` once pair mode ships. Recorded, never blocking, never shown to a partner. "
        "Pass line in Unit 2's ruled SOLO wording."
    ),
)

LESSON_3A = dict(
    kind="lesson",
    id="many-values-one-name",
    title="Many Values, One Name",
    minutes=33,
    summary=(
        "Put the chalk wall's gaps in one list. Then read an item by its position, add to the list, count its "
        "items, and read a list inside a list."
    ),
    notes=(
        "Lesson 3A (CC: 3A-02, 3A-03, 3A-06, 3A-S; the rest SC). Preceded by 3a-remembers. Exactly one SOLO "
        "(solo-3a, the quiet recipe slip). Non-dictated checkpoints: 3A-01, 3A-02, 3A-03 CP2, 3A-05 CP1, 3A-06 CP2, "
        "3A-07, 3A-09 CP2, 3A-10 CP1-3, 3A-S. 33 minutes (teacher ruling on the Unit 4 reviews: the `how-long` split "
        "adds about 2, the shorter productive-failure opener saves 1; with 3B the core is about 46 minutes). "
        "3A-04 is folded into 3A-03 (CP2) and 3A-08 into 3A-05 (CP2), as the spec says. Campaign links are 'you "
        "have seen this': the four dialogue boxes, `party.members`, the chalk wall, `show_mana(caster)`, "
        "`caster[\"mana\"] = ...` and `caster[\"abilities\"][\"magical_affinity\"]`."
    ),
    exercises=[
        HOW_WOULD_YOU_STORE_IT, MAKE_THE_WALL, FIRST_IS_ZERO, NEW_CHALK_MARK, HOW_LONG, FIX_A_MARK, LISTS_INSIDE_LISTS,
        BROKEN_SPELL_3A, SOLO_3A,
    ],
)


# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (3b-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_3B = dict(
    kind="quiz",
    id="3b-remembers",
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from Units 1 and 3, before you read the wall closely. Nothing is scored.",
    notes=(
        "meta: path=SC; unscored warm-up shown inline before Lesson 3B. Q1 is the spec's 1C item (`\"█\" * 0 + "
        "\"!\"`). Q2 is added for the 2.1 rule (from Unit 4 on, one warm-up item is always def/return): a recipe "
        "with two ingredients, from Unit 3."
    ),
    questions=[
        dict(
            type="predict",
            id="zero-blocks",
            q="What will this print?",
            code='print("█" * 0 + "!")\n',
            choices=["█!", "0!", "█", "!"],
            answer="!",
            explain=(
                "`\"█\" * 0` stamps the block zero times, so it's empty text, the way 0 × 4 is 0 in math. Glue `!` "
                "on, and only `!` shows."
            ),
        ),
        dict(
            type="predict",
            id="shrink-recipe",
            q="What will this print?",
            code="def shrink(old, new):\n    return old - new\n\nprint(shrink(48, 41))\n",
            choices=["7", "-7", "89", "old - new"],
            answer="7",
            explain=(
                "The call hands over 48 and 41, in order: `old` is 48 and `new` is 41. The recipe hands back "
                "48 - 41, which is 7."
            ),
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 3B "Reading the Wall Closely"
# ---------------------------------------------------------------------------------------------

# 3B-01 ------------------------------------------------------------------------------------------

RANGE_STARTER = "# A d8 has 8 faces: 1 to 8.\nd8_faces = []\nprint(d8_faces)\n"


def _range(line="d8_faces = list(range(1, 9))", extra=""):
    return extra + "# A d8 has 8 faces: 1 to 8.\n" + line + "\nprint(d8_faces)\n"


RANGE_CHECK = (
    "d8_faces holds 1 to 8",
    "_v = d8_faces\n"
    "_t = type(_v).__name__\n"
    "assert _t != 'range', '`d8_faces` holds a range, not a list. Wrap it in `list()`: `list(range(...))`.'\n"
    "assert _t != 'int', ('`d8_faces` holds one number. `randint` rolls one face, but this step needs every face: '\n"
    "    '`list(range(...))`.')\n"
    "assert _t == 'list', '`d8_faces` doesn' + chr(39) + 't hold a list. Make it a list of faces: `list(range(...))`.'\n"
    "assert _v != [], '`d8_faces` is still the empty list `[]`. Fill it with `list(range(...))`.'\n"
    "assert _v != [1, 2, 3, 4, 5, 6, 7], ('Your list stops at 7, because the stop number is left out. Make the stop '\n"
    "    'one more than the last face you want.')\n"
    "assert not (_v[:1] == [0]), 'Your list starts at 0. A d8 has no 0 face: start at 1, `range(1, ...)`.'\n"
    "assert _v != [1, 2, 3, 4, 5, 6, 7, 8, 9], ('Your list goes up to 9. The stop is left out, so pick the stop that '\n"
    "    'ends on 8.')\n"
    "assert _v == [1, 2, 3, 4, 5, 6, 7, 8], ('Your list isn' + chr(39) + 't 1 to 8. A d8' + chr(39) + 's faces are 1, '\n"
    "    '2, 3, 4, 5, 6, 7 and 8.')",
)

RANGE_USED = (
    "d8_faces itself is made with range, and range reaches 8 on its own",
    "import ast as _ast\n"
    "_tree = _ast.parse(_source)\n"
    "_as = [_n for _n in _tree.body if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 "
    "and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'd8_faces']\n"
    "_rng = lambda _x: any(type(_m).__name__ == 'Call' and type(_m.func).__name__ == 'Name' and _m.func.id == 'range' "
    "for _m in _ast.walk(_x))\n"
    "assert _uses('call:range'), 'You typed the faces in. Use `range`, so Python does the counting: `list(range(...))`.'\n"
    "assert _as and _rng(_as[-1].value), ('`d8_faces` isn' + chr(39) + 't made with `range`. Make `d8_faces` itself '\n"
    "    'with `range`: `d8_faces = list(range(...))`.')\n"
    "_patch = type(_as[-1].value).__name__ == 'BinOp' or any((type(_n).__name__ == 'AugAssign' "
    "and type(_n.target).__name__ == 'Name' and _n.target.id == 'd8_faces') or (type(_n).__name__ == 'Call' "
    "and type(_n.func).__name__ == 'Attribute' and _n.func.attr in ('append', 'insert', 'extend') "
    "and type(_n.func.value).__name__ == 'Name' and _n.func.value.id == 'd8_faces') for _n in _ast.walk(_tree))\n"
    "assert not _patch, ('Your code adds the 8 on by itself. Let `range` reach 8 on its own: the stop is left out, '\n"
    "    'so make it one more than the last face.')",
)

RANGE_OF_MARKS = dict(
    id="range-of-marks",
    title="Ranges",
    martu=(
        "In math class, *range* means the biggest number minus the smallest. In Python, "
        "[[range()|`range(1, 7)`]] means something else: count from 1, and stop before 7. It's like a number line "
        "with a filled dot at 1 and an open dot at 7: 1 ≤ n < 7. `list(range(1, 7))` turns the count into a "
        "list, `[1, 2, 3, 4, 5, 6]`:\n"
        "```text\nrange(1, 7)\n 1 2 3 4 5 6 | 7\n             stop: left out\n```\n"
        "A *d8* is a die with 8 faces, numbered 1 to 8."
    ),
    introduces=["call:range", "call:list"],
    example="steps = list(range(3, 6))\nprint(steps)\n",
    example_output="[3, 4, 5]",
    names=["d8_faces"],
    predict=dict(
        q="Before you press Run: what will these two lines print?",
        code="print(list(range(5)))\nprint(list(range(1, 7)))\n",
        choices=[
            "[1, 2, 3, 4, 5]\n[1, 2, 3, 4, 5, 6, 7]",
            "[0, 1, 2, 3, 4]\n[1, 2, 3, 4, 5, 6]",
            "[0, 1, 2, 3, 4, 5]\n[1, 2, 3, 4, 5, 6]",
            "[0, 1, 2, 3, 4]\n[1, 2, 3, 4, 5, 6, 7]",
        ],
        answer=1,
        explain=(
            "With one number, `range` starts at 0 and stops before it: 0 to 4, five numbers. `range(1, 7)` starts "
            "at 1 and stops before 7: the six faces of a d6, a six-sided die."
        ),
    ),
    starter=RANGE_STARTER,
    checkpoints=[
        dict(
            id="d8-faces",
            text=(
                "Make `d8_faces` hold every face of a d8, 1 to 8. On line 2, put `list(range(...))` in place of the "
                "`[]`, with the right two numbers."
            ),
            dictated=True,
            hints=[
                "The stop number is left out. To end on 8, what must the stop be?",
                "`list(range(3, 6))` makes `[3, 4, 5]`: it starts at 3 and stops before 6.",
                "Write `d8_faces = list(range(1, 9))` in place of `d8_faces = []`.",
            ],
            checks=[
                have_list("d8_faces", known=["d8_faces"], foreign=["steps", "d6_faces"]),
                RANGE_CHECK,
                RANGE_USED,
            ],
            pass_line="`d8_faces` holds all 8 faces. Bomb Shell: One to eight. Counted.",
        ),
    ],
    solution=_range(),
    assemble=dict(
        lines=["d8_faces = list(range(1, 9))", "print(d8_faces)"],
        distractors=["d8_faces = list(range(1, 8))", "d8_faces = list(range(8))", "d8_faces = range(1, 9)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A ruler",
            text=(
                "```text\nrange(1, 9)\n|--|--|--|--|--|--|--|--|\n1  2  3  4  5  6  7  8  9\n"
                "^ start          stop ^\n```\nThe stop number is where you stop. You don't take it."
            ),
        ),
        dict(
            angle="contrast",
            label="range or randint?",
            text=(
                "`random.randint(1, 8)` rolls ONE face, and 8 can come up. `list(range(1, 9))` lists EVERY face, "
                "and the 9 is left out. Different jobs, different ends."
            ),
        ),
        dict(
            angle="step-by-step",
            text="1. Start at 1.\n2. Count up by one.\n3. Stop before the stop number.\n4. `list(...)` collects them.",
        ),
        dict(angle="shorter", text="`range(start, stop)`: from the start, up to but not including the stop."),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's d20",
        text=(
            "Lucky wants a d20, a die with 20 faces. At the bottom, make `d20_faces` with `range`. Then show how "
            "many faces it has, with `len()`."
        ),
        hints=[
            "The stop is left out, so a d20 needs a stop one past 20. Then `len()` counts the faces: it should show 20.",
            "Write `d20_faces = list(range(1, 21))` at the bottom, then `print(len(d20_faces))`.",
        ],
        checks=[
            (
                "d20_faces is 1 to 20, and its length is printed",
                "import ast as _ast\n"
                "assert d20_faces == list(range(1, 21)), '`d20_faces` doesn' + chr(39) + 't hold 1 to 20. Remember, the stop is left out.'\n"
                "_lens = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
                "and type(_n.func).__name__ == 'Name' and _n.func.id == 'len' "
                "and any(type(_a).__name__ == 'Name' and _a.id == 'd20_faces' for _a in _n.args)]\n"
                "assert _lens and '20' in _lines(), 'The Console doesn' + chr(39) + 't show how many faces yet. Write `print(len(d20_faces))`.'",
            ),
        ],
        solution=_range() + "d20_faces = list(range(1, 21))\nprint(len(d20_faces))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="return random.randint(1, die_size)",
        why=(
            "You've seen this at the trap door. `randint(1, die_size)` rolled one face, and both ends could come "
            "up. `range(1, die_size + 1)` would list every face, because its stop is left out."
        ),
    ),
    takeaway="`range(1, 9)` counts 1 to 8: the stop is left out. `list(range(...))` makes it a list.",
    wrong_answers=[
        dict(why="starter unchanged: the empty list", code=RANGE_STARTER, fails_at=1, message_contains="empty list"),
        dict(why="the faces typed by hand (spec)", code=_range("d8_faces = [1, 2, 3, 4, 5, 6, 7, 8]"), fails_at=1,
             message_contains="Use `range`"),
        dict(why="the stop is left out: range(1, 8) (spec)", code=_range("d8_faces = list(range(1, 8))"), fails_at=1,
             message_contains="stops at 7"),
        dict(why="range(8) starts at 0", code=_range("d8_faces = list(range(8))"), fails_at=1, message_contains="starts at 0"),
        dict(why="range(9) starts at 0 too", code=_range("d8_faces = list(range(9))"), fails_at=1, message_contains="starts at 0"),
        dict(why="no list(): a range, not a list", code=_range("d8_faces = range(1, 9)"), fails_at=1,
             message_contains="Wrap it"),
        dict(why="randint rolls one face", code=_range("d8_faces = random.randint(1, 8)", extra="import random\n"),
             fails_at=1, message_contains="one number"),
        dict(why="one past the end", code=_range("d8_faces = list(range(1, 10))"), fails_at=1, message_contains="up to 9"),
        dict(why="square brackets for range's round ones", code=_range("d8_faces = list(range[1, 9])"), fails_at=0,
             message_contains="not subscriptable"),
        dict(why="the example's name copied", code="steps = list(range(1, 9))\nprint(steps)\n", fails_at=1,
             message_contains="example"),
        dict(why="typing a list's values by hand, then a range printed to pass the check",
             code=_range("d8_faces = [1, 2, 3, 4, 5, 6, 7, 8]\nprint(list(range(1, 9)))"), fails_at=1,
             message_contains="`d8_faces` itself"),
        dict(why="the stop left out, patched by adding 8 on: range(1, 8) + [8]",
             code=_range("d8_faces = list(range(1, 8)) + [8]"), fails_at=1, message_contains="on its own"),
        dict(why="the stop left out, patched with an append", code=_range("d8_faces = list(range(1, 8))\nd8_faces.append(8)"),
             fails_at=1, message_contains="on its own"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="range-slice-sort", solo="false", dictates="1",
             foreign_names="steps,d6_faces") + "\n"
        "Spec: predict `list(range(5))` and `list(range(1, 7))`; CP1 [D] `d8_faces` with `range`; checks: the "
        "list is 1 to 8 and `range` makes `d8_faces` itself (a typed list gets 'Use `range` to make it', or "
        "'Make `d8_faces` itself with `range`' when a range is printed beside it; a short range patched with `+ [8]` "
        "or `.append(8)` is told to let `range` reach 8 on its own: the stop-left-out idea is the point). The Example "
        "(`list(range(3, 6))`) is not the d6, so the predict stays a real prediction. Extra catches: a bare range "
        "(no `list()`), `range(8)` from 0, one past the end, `randint` (one face). AW: a ruler (the stop mark is "
        "not taken), contrast with `randint` (2B-07), step-by-step, shorter. The spec's d6 / `randint` sentence is "
        "cut from the Learn text (teacher ruling): the contrast angle and the campaign link carry it. BQ (combining "
        "range + len): a d20 and its length."
    ),
)

# 3B-02 ------------------------------------------------------------------------------------------

# Teacher ruling: the easier step first. CP1 `first-two` (the two oldest), CP2 `last-three` (the three newest),
# both goal-only; the starter comments name the goal, never the slice.
SLICE_STARTER = (
    WALL_LINE + "# 1. The two oldest gaps:\nfirst_two = []\n# 2. The three newest gaps:\nlast_three = []\n"
    "print(first_two)\nprint(last_three)\n"
)


def _slice(first="first_two = chalk_wall[:2]", last="last_three = chalk_wall[-3:]", extra=""):
    return (
        WALL_LINE + "# 1. The two oldest gaps:\n" + first + "\n# 2. The three newest gaps:\n" + last + "\n"
        "print(first_two)\nprint(last_three)\n" + extra
    )


SLICE_KNOWN = ["chalk_wall", "first_two", "last_three"]

FIRST_TWO_CHECK = follows(
    "first_two follows the wall",
    {"chalk_wall": W5},
    f"_R('first_two') == {_W}[0:2]",
    rules=[
        (f"_R('first_two') == {_W}[0:1]", "Your slice takes only one gap, because the end of a slice is left out. "
         "Make the end number one past the last gap you want.", None),
        (f"_R('first_two') == {_W}[1:3]", "Your slice starts at position 1, the second gap. Positions start at 0, so "
         "start the slice at 0.", None),
        (f"_R('first_two') == {_W}[0:3]", "Your slice takes three gaps. The end is left out, so the end number is one "
         "past the last gap you take.", None),
        ("_R('first_two') == []", "`first_two` is still empty. Put a slice of `chalk_wall` on its right side.", None),
        ("_R('first_two') == _g0.get('first_two') and _plain('first_two')", "You typed the gaps into `first_two` "
         "instead of slicing them from the wall. Slice `chalk_wall` from the start.", "'`first_two` stayed the same'"),
        ("_R('first_two') == _g0.get('first_two')", "`first_two` isn't made from `chalk_wall`. Slice it from "
         "`chalk_wall`.", "'`first_two` stayed the same'"),
    ],
    fix="Your slice doesn't hold the two oldest gaps. Start at position 0, or leave the start empty.",
    ev=WALL_EV5,
    saw="'`first_two` became ' + _sh(_R('first_two'))",
    own=(
        "_W0 is None or _g0.get('first_two') == _W0[0:2]",
        "'On your wall `first_two` holds ' + _sh(_g0.get('first_two')) + ', but the two oldest gaps are ' + "
        "_sh(_W0[0:2]) + '. Start at position 0, so it fits a wall of any length.'",
    ),
)

LAST_THREE_CHECK = follows(
    "last_three follows the wall",
    {"chalk_wall": W5},
    f"_R('last_three') == {_W}[-3:]",
    rules=[
        (f"_R('last_three') == {_W}[-3:-1]",
         "Your slice misses the newest gap. A slice leaves its end out, so `[-3:-1]` stops before `-1`. Leave the "
         "end side empty to run to the edge.", None),
        ("_R('last_three') == []", "`last_three` is still empty. Put a slice of `chalk_wall` on its right side.", None),
        ("_R('last_three') == _g0.get('last_three') and _plain('last_three')", "You typed the gaps into `last_three` "
         "instead of slicing them from the wall. Slice `chalk_wall`, counting from the end.",
         "'`last_three` stayed the same'"),
        ("_R('last_three') == _g0.get('last_three')", "`last_three` isn't made from `chalk_wall`. Slice it from "
         "`chalk_wall`, counting from the end.", "'`last_three` stayed the same'"),
        ("type(_R('last_three')).__name__ == 'int'", "`last_three` holds one gap, not a list. A slice has a colon "
         "inside the square brackets.", None),
        (f"_R('last_three') == {_W}[:3]", "Your slice takes the three oldest gaps. The newest are at the end: count "
         "from the end.", None),
        (f"_R('last_three') == {_W}[-2:]", "Your slice takes the two newest gaps. Start one further from the end for "
         "three.", None),
        (f"_R('last_three') == {_W}[4:]", "Your slice starts at a position you counted, and that fits only a wall of "
         "7 gaps. Count from the end instead.", None),
    ],
    fix="Your slice doesn't hold the three newest gaps. Start 3 from the end, and leave the end empty.",
    ev=WALL_EV5,
    saw="'`last_three` became ' + _sh(_R('last_three'))",
    own=(
        "_W0 is None or _g0.get('last_three') == _W0[-3:]",
        "'On your wall `last_three` holds ' + _sh(_g0.get('last_three')) + ', but the three newest gaps are ' + "
        "_sh(_W0[-3:]) + '. Start 3 from the end and leave the end empty, so it fits a wall of any length.'",
    ),
)


def slice_used(name, tip):
    """The list is made with a slice (a colon), not read item by item. `tip` points at the Example's slice."""
    return (
        f"{name} is made with a slice",
        "import ast as _ast\n"
        "_cut = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
        f"and any(type(_t).__name__ == 'Name' and _t.id == {name!r} for _t in _n.targets) "
        "and any(type(_m).__name__ == 'Slice' for _m in _ast.walk(_n.value))]\n"
        f"assert _cut, 'You read the gaps one at a time. This step practices slices: a colon inside the square brackets, {tip}.'",
    )


SLICE_THE_WALL = dict(
    id="slice-the-wall",
    title="Slice the wall",
    martu=(
        "A [[slice]] copies part of a list, like quoting a few lines of a poem in English class: you get an "
        "excerpt, and the poem doesn't change. `chalk_wall[2:5]` copies positions 2, 3 and 4. The end is left "
        "out, the same as `range`:\n"
        "```text\n 0  1  2  3  4  5  6\n48 48 47 46 44 41 37\n      [2:5] -> 47 46 44\n```\n"
        "In a book, \"pages 2 to 5\" includes page 5. A slice doesn't: it stops before its end number.\n"
        "Leave a side empty to run to the edge. `chalk_wall[:3]` is the first three gaps. `chalk_wall[-2:]` is the "
        "last two.\n"
        "As before, each number on my chalk wall is a *gap*: the hours between two bursts, oldest first."
    ),
    introduces=["node:Slice"],
    example="notes = [5, 6, 7, 8, 9]\nprint(notes[1:3])\nprint(notes[-2:])\n",
    example_output="[6, 7]\n[8, 9]",
    names=["chalk_wall", "first_two", "last_three"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code=WALL_LINE + "print(chalk_wall[1:3])\n",
        choices=["[48, 47, 46]", "[48, 48]", "[48, 47]", "[47, 46]"],
        answer=2,
        explain="`[1:3]` starts at position 1 and stops before 3: positions 1 and 2, which are 48 and 47.",
    ),
    starter=SLICE_STARTER,
    checkpoints=[
        dict(
            id="first-two",
            text=(
                "On line 3, put a slice of `chalk_wall` in place of the `[]` in `first_two = []`, so `first_two` "
                "holds the two oldest gaps."
            ),
            dictated=False,
            hints=[
                "Look at Mar'tu's example `chalk_wall[:3]`: an empty start runs to the edge. The oldest gaps are at "
                "the start of the wall.",
                "`notes[1:3]` starts at position 1 and stops before 3, so it takes two items. Which start gives the "
                "two oldest?",
                "Write `first_two = chalk_wall[:2]` in place of `first_two = []`.",
            ],
            checks=[
                have_list("first_two", known=SLICE_KNOWN, foreign=["notes"]),
                not_reset("first_two"),
                FIRST_TWO_CHECK,
                slice_used("first_two", "like `notes[1:3]` in the Example"),
            ],
            pass_line="`first_two` holds the two oldest gaps, 48 and 48. Mar'tu: Back when the clock was calm.",
        ),
        dict(
            id="last-three",
            text=(
                "On line 5, put a slice of `chalk_wall` in place of the `[]` in `last_three = []`, so `last_three` "
                "holds the three newest gaps."
            ),
            dictated=False,
            hints=[
                "The newest gaps are at the end. Count from the end with a minus, and leave the end side empty.",
                "`notes[-2:]` is the last two items: start 2 from the end and run to the edge.",
                "Write `last_three = chalk_wall[-3:]` in place of `last_three = []`.",
            ],
            checks=[
                have_list("last_three", known=SLICE_KNOWN, foreign=["notes"]),
                not_reset("last_three"),
                LAST_THREE_CHECK,
                slice_used("last_three", "like `notes[-2:]` in the Example"),
            ],
            pass_line="`last_three` holds the three newest gaps. Gearshift: 44, 41, 37. Shrinking. Visor dims.",
        ),
    ],
    solution=_slice(),
    partials=[_slice(last="last_three = []")],
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "first_two = chalk_wall[:2]",
               "last_three = chalk_wall[-3:]", "print(first_two)", "print(last_three)"],
        distractors=["first_two = chalk_wall[0:1]", "last_three = chalk_wall[-3:-1]", "last_three = [44, 41, 37]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Cuts between the items",
            text=(
                "Cuts go BETWEEN the items:\n```text\n | 48 | 48 | 47 | 46 |\n 0    1    2    3    4\n```\n"
                "`[1:3]` cuts at 1 and at 3. What lies between: 48 and 47."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`chalk_wall[-3:]`:\n1. Start 3 from the end: position -3, the 44.\n"
                "2. No end number, so run to the edge.\n3. You get `[44, 41, 37]`, a new list."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work?",
            text=(
                "A slice is a new list. Python copies the items out. Change `last_three` later, and `chalk_wall` "
                "stays the same. Change the wall, and the copy you made stays the same too."
            ),
        ),
        dict(angle="shorter", text="`[start:end]`: from the start, and stop before the end. Leave a side empty to "
             "reach the edge."),
    ],
    bonus=dict(
        by="lucky",
        title="The shrink in one number",
        text=(
            "Lucky wants it in one number. At the bottom, show how much the wall shrank across `last_three`: its "
            "first gap minus its last."
        ),
        hints=[
            "The first gap of `last_three` is `last_three[0]`, and its last gap is `last_three[-1]`.",
            "Write `print(last_three[0] - last_three[-1])` at the bottom.",
        ],
        checks=[
            follows(
                "the shrink across last_three follows the wall",
                {"chalk_wall": W5},
                f"_said({_W}[-3] - {_W}[-1])",
                rules=[
                    (f"_said({_MINE}[-3] - {_MINE}[-1])", "You typed the answer instead of the math. Work it out "
                     "from `last_three`: its first gap minus its last.", None),
                ],
                fix="Your code doesn't show the shrink across `last_three` yet. Show its first gap minus its last: "
                    "`last_three[0] - last_three[-1]`.",
                ev=WALL_EV5,
            ),
        ],
        solution=_slice(extra="print(last_three[0] - last_three[-1])\n"),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "You've seen this. Bomb Shell studied the wall, then the clock, and guessed thirty-two hours. "
            "The newest marks tell you the most, and `chalk_wall[-3:]` is the newest three."
        ),
    ),
    takeaway=(
        "`wall[2:5]` copies positions 2, 3 and 4: it stops before the end number. `wall[-3:]` is the last three. A "
        "slice is a new list."
    ),
    wrong_answers=[
        # CP1: first_two, the two oldest
        dict(why="starter unchanged: still empty", code=SLICE_STARTER, fails_at=1, message_contains="still empty"),
        dict(why="slice end is not included: [0:1] (spec)", code=_slice(first="first_two = chalk_wall[0:1]"),
             fails_at=1, message_contains="left out"),
        dict(why="asks for item 1 to start: [1:3]", code=_slice(first="first_two = chalk_wall[1:3]"), fails_at=1,
             message_contains="Positions start at 0"),
        dict(why="the Learn pane's `[:3]` copied: three gaps", code=_slice(first="first_two = chalk_wall[:3]"),
             fails_at=1, message_contains="takes three gaps"),
        dict(why="first two typed by hand", code=_slice(first="first_two = [48, 48]"), fails_at=1,
             message_contains="typed the gaps into `first_two`"),
        dict(why="a comma for the colon: TypeError", code=_slice(first="first_two = chalk_wall[0, 2]"), fails_at=0,
             message_contains="not tuple"),
        dict(why="square brackets vs parentheses: the list called", code=_slice(first="first_two = chalk_wall(0, 2)"),
             fails_at=0, message_contains="not callable"),
        dict(why="the two read one by one, not sliced", code=_slice(first="first_two = [chalk_wall[0], chalk_wall[1]]"),
             fails_at=1, message_contains="practices slices"),
        dict(why="a slice counted for the check's 5-gap wall: [-5:-3]", code=_slice(first="first_two = chalk_wall[-5:-3]"),
             fails_at=1, message_contains="two oldest gaps are"),
        dict(why="the slice typed above the starter's `first_two = []`, which empties it again",
             code=WALL_LINE + "# 1. The two oldest gaps:\nfirst_two = chalk_wall[:2]\nfirst_two = []\n"
             "# 2. The three newest gaps:\nlast_three = []\nprint(first_two)\nprint(last_three)\n", fails_at=1,
             message_contains="Line 4 sets `first_two = []` again"),
        # CP2: last_three, the three newest
        dict(why="CP1 done, last_three still empty", code=_slice(last="last_three = []"), fails_at=2,
             message_contains="still empty"),
        dict(why="the newest three typed by hand (spec)", code=_slice(last="last_three = [44, 41, 37]"), fails_at=2,
             message_contains="typed the gaps into `last_three`"),
        dict(why="slice end is not included: [-3:-1] (spec)", code=_slice(last="last_three = chalk_wall[-3:-1]"),
             fails_at=2, message_contains="leaves its end out"),
        dict(why="one gap, no colon", code=_slice(last="last_three = chalk_wall[-3]"), fails_at=2,
             message_contains="colon"),
        dict(why="a start counted for 7 gaps: [4:7]", code=_slice(last="last_three = chalk_wall[4:7]"), fails_at=2,
             message_contains="fits only"),
        dict(why="the three oldest", code=_slice(last="last_three = chalk_wall[0:3]"), fails_at=2,
             message_contains="oldest"),
        dict(why="the Learn pane's `[-2:]` copied: the two newest", code=_slice(last="last_three = chalk_wall[-2:]"),
             fails_at=2, message_contains="two newest"),
        dict(why="read one by one, not sliced", code=_slice(last="last_three = [chalk_wall[-3], chalk_wall[-2], chalk_wall[-1]]"),
             fails_at=2, message_contains="practices slices"),
        dict(why="the Learn pane's example copied, [2:5]: the last three of a 5-gap wall, not of 7",
             code=_slice(last="last_three = chalk_wall[2:5]"), fails_at=2, message_contains="three newest gaps are"),
        dict(why="a start counted from the wrong end: [2:]", code=_slice(last="last_three = chalk_wall[2:]"), fails_at=2,
             message_contains="three newest gaps are"),
        dict(why="the slice typed above the starter's `last_three = []`, which empties it again",
             code=WALL_LINE + "# 1. The two oldest gaps:\nfirst_two = chalk_wall[:2]\n# 2. The three newest gaps:\n"
             "last_three = chalk_wall[-3:]\nlast_three = []\nprint(first_two)\nprint(last_three)\n", fails_at=2,
             message_contains="Line 6 sets `last_three = []` again"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="range-slice-sort", solo="false", dictates="",
             foreign_names="notes") + "\n"
        "Teacher ruling on the Unit 4 reviews: the easier step comes first, and both are goal-only. CP1 [ND] "
        "`first-two` (the two oldest), CP2 [ND] `last-three` (the three newest); each keeps its id. Starter comments "
        "name the goal, never the slice, and the Learn pane's edge examples are `chalk_wall[:3]` (the first three) "
        "and `chalk_wall[-2:]` (the last two), so it gives neither answer; copying either one is named (three gaps; "
        "the two newest). Both are CMB on another wall (5 gaps), so a typed `[44, 41, 37]` and a start counted for "
        "7 gaps (`[4:7]`) fail; the student's own wall is checked too, so a slice that only fits 5 gaps fails "
        "(`[2:5]`, the Learn pane's own example, `[2:]`, `[-5:-3]`). Both steps need a colon (read item by item is "
        "told this step practices slices). Messages name the slip without the line. WT 'A slice is a new list' = "
        "the 'Why does this work?' angle (changing a copy never changes the original). The predict (`[1:3]`) "
        "catches 'the slice end is included' before Run. BQ (combining slice + index + subtraction): the shrink "
        "across `last_three`."
    ),
)


# 3B-03 ------------------------------------------------------------------------------------------

SORT_HEAD = WALL_LINE + "# 1. A sorted copy, shortest first.\n#    Leave chalk_wall as it is.\n"
SORT_STARTER = SORT_HEAD + "shortest_first = []\nprint(shortest_first)\nprint(chalk_wall)\n"
SORT_KNOWN = ["chalk_wall", "shortest_first"]
SORT_FOREIGN = ["scores", "marks", "result"]


def _sort(line="shortest_first = sorted(chalk_wall)"):
    return SORT_HEAD + line + "\nprint(shortest_first)\nprint(chalk_wall)\n"


_MX = "_C['chalk_wall']"

SORT_NOT_NONE = (
    "nothing holds None",
    "assert chalk_wall is not None, ('`chalk_wall` now holds `None`, Python' + chr(39) + 's word for nothing. '\n"
    "    '`.sort()` hands back nothing, so `chalk_wall = chalk_wall.sort()` threw the wall away. Use `sorted()`, and '\n"
    "    'leave the wall as it is.')\n"
    "assert shortest_first is not None, ('`shortest_first` holds `None`, Python' + chr(39) + 's word for nothing, '\n"
    "    'because `.sort()` hands back nothing. Use `sorted()`: it hands back a new sorted list.')",
)

SORTED_VALUE = follows(
    "shortest_first follows the wall",
    {"chalk_wall": MIXED},
    f"_R('shortest_first') == sorted({_MX})",
    rules=[
        (f"_R('shortest_first') == [] and _named", Code("'`' + _named[0] + '` is a name from the Example. This "
         "task' + chr(39) + 's list is named `shortest_first`.'"), None),
        ("_R('shortest_first') == [] and _lone", Code("'Line ' + str(_lone[0]) + ' makes a sorted copy with no name in "
         "front, so Python reads it and throws it away. Keep it: `shortest_first = sorted(chalk_wall)`.'"), None),
        ("_R('shortest_first') == []", "`shortest_first` is still empty. Put a sorted copy of the wall on its right "
         "side: the Example shows how.", None),
        ("_R('shortest_first') == _g0.get('shortest_first')", "You typed the sorted gaps into `shortest_first`. Let "
         "Python sort the wall, with `sorted()`.", "'`shortest_first` stayed the same'"),
        (f"_R('shortest_first') == sorted({_MX})[::-1]", "Your list has the longest gap first. Shortest first means "
         "the smallest gap goes at the front, and `sorted()` puts them that way.", None),
        (f"_R('shortest_first') == {_MX}[::-1]", "Your code turns the wall around. That only looks sorted, because "
         "this wall shrinks. `sorted()` puts any wall in order: `sorted(chalk_wall)`.", None),
    ],
    fix="`shortest_first` isn't a sorted copy of the wall. Make it with `sorted()`.",
    ev=_ev(MIXED),
    saw="'`shortest_first` became ' + _sh(_R('shortest_first'))",
    pre=(
        "_lone = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'Call' and type(_n.value.func).__name__ == 'Name' "
        "and _n.value.func.id == 'sorted']\n"
        f"_named = [_k for _k in {SORT_FOREIGN!r} if _R(_k) == sorted({_MX})]\n"
    ),
)

WALL_KEPT = follows(
    "chalk_wall is left as it was",
    {"chalk_wall": MIXED},
    f"_R('chalk_wall') == {_MX}",
    rules=[
        ("_R('chalk_wall') is not None and _R('chalk_wall') is _R('shortest_first')",
         "`shortest_first = chalk_wall` gives the same list a second name, like a nickname. It is not a copy. Use "
         "`sorted(chalk_wall)`: it makes a new list.", "'`chalk_wall` got sorted too'"),
        (f"_R('chalk_wall') == sorted({_MX})", "`.sort()` sorted the wall itself. Use `sorted(chalk_wall)`: it makes "
         "a sorted copy and leaves the wall as it is.", "'`chalk_wall` got sorted'"),
    ],
    fix="`chalk_wall` changed. Leave it as it is: `sorted(chalk_wall)` makes a new list.",
    ev=_ev(MIXED),
    saw="'`chalk_wall` became ' + _sh(_R('chalk_wall'))",
)

SORTED_USED = (
    "made with sorted()",
    "assert _uses('call:sorted'), 'Your code sorts a copy another way. This step practices `sorted()`: `sorted(chalk_wall)`.'",
)

SORTED_OR_SORT = dict(
    id="sorted-or-sort",
    title="`sorted` or `.sort`",
    martu=(
        "[[sorted()|`sorted(chalk_wall)`]] hands back a sorted copy of the wall, smallest first. It's like "
        "photocopying a list and putting the copy in order: the original stays as it is. "
        "`shortest_first = sorted(chalk_wall)` keeps the copy.\n"
        "`chalk_wall.sort()` puts the wall itself in order and hands back nothing. So `result = chalk_wall.sort()` "
        "puts `None` in `result`, Python's word for nothing. It's like a recipe with no `return` in Unit 3."
    ),
    introduces=["call:sorted", "attr:sort"],
    example="scores = [7, 2, 5]\nprint(sorted(scores))\nprint(scores)\n",
    example_output="[2, 5, 7]\n[7, 2, 5]",
    names=["shortest_first", "chalk_wall", "sorted"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code="marks = [3, 1, 2]\nresult = marks.sort()\nprint(result)\nprint(marks)\n",
        choices=["None\n[1, 2, 3]", "[1, 2, 3]\n[1, 2, 3]", "[1, 2, 3]\n[3, 1, 2]", "None\n[3, 1, 2]"],
        answer=0,
        explain=(
            "`marks.sort()` sorts `marks` itself and hands back nothing, so `result` holds `None`, Python's word "
            "for nothing. The list `marks` did change: `[1, 2, 3]`."
        ),
    ),
    pair_talk=(
        "Pair talk: explain to your partner why `result` printed `None`. Use the word *recipe*. Then each of you "
        "writes your own line."
    ),
    starter=SORT_STARTER,
    checkpoints=[
        dict(
            id="shortest-first",
            text=(
                "On line 4, put a sorted copy of `chalk_wall`, smallest first, in place of the `[]` in "
                "`shortest_first = []`. Leave `chalk_wall` as it is."
            ),
            dictated=False,
            hints=[
                "Find the line `shortest_first = []`. Its right side is where `sorted(...)` goes.",
                "`sorted(scores)` hands back a new list, smallest first. `scores` itself does not change.",
                "Write `shortest_first = sorted(chalk_wall)` in place of `shortest_first = []`.",
            ],
            checks=[
                have_list("shortest_first", known=SORT_KNOWN, foreign=SORT_FOREIGN),
                SORT_NOT_NONE,
                not_reset("shortest_first"),
                SORTED_VALUE,
                WALL_KEPT,
                SORTED_USED,
            ],
            pass_line="You made a sorted copy and kept the wall. Mar'tu: Two lists now, the copy and my wall as I wrote it.",
        ),
    ],
    solution=_sort(),
    assemble=dict(
        lines=["chalk_wall = [48, 48, 47, 46, 44, 41, 37]", "shortest_first = sorted(chalk_wall)",
               "print(shortest_first)", "print(chalk_wall)"],
        distractors=["shortest_first = chalk_wall.sort()", "chalk_wall = chalk_wall.sort()", "sorted(chalk_wall)"],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="A copy or the original",
            text=(
                "`sorted()` is a friend who copies your list onto a new page, in order. `.sort()` rearranges your "
                "own page and hands you nothing back."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`result = chalk_wall.sort()`:\n1. `.sort()` sorts `chalk_wall` itself.\n2. It hands back nothing: "
                "`None`.\n3. `result` gets that `None`.\n`result = sorted(chalk_wall)`: `result` gets a new, sorted "
                "list."
            ),
        ),
        dict(
            angle="from Unit 3",
            label="A recipe with no return",
            text=(
                "In Unit 3, a recipe with no `return` handed back `None`. `.sort()` is like that: it does its job "
                "and hands back nothing. `sorted()` has a `return`, so to speak."
            ),
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `shortest_first = chalk_wall.sort()` (`None`: nothing came back). Not this: "
                "`shortest_first = chalk_wall` "
                "(the same list with a second name, like a nickname).\nThis: `shortest_first = sorted(chalk_wall)`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Shortest and longest",
        text=(
            "Lucky wants the shortest gap and the longest gap. At the bottom, show both, read from `shortest_first` "
            "by position."
        ),
        hints=[
            "The shortest gap is first in `shortest_first`. The longest is at the other end: count from the end.",
            "Write `print(shortest_first[0])` at the bottom, then `print(shortest_first[-1])`.",
        ],
        checks=[
            follows(
                "the shortest and longest follow the wall",
                {"chalk_wall": MIXED},
                f"_said(min({_MX})) and _said(max({_MX}))",
                rules=[
                    (f"_said(min({_MINE})) or _said(max({_MINE}))",
                     "You typed the gaps instead of reading them from `shortest_first`. Read them by position.", None),
                ],
                fix="Your code doesn't show the shortest and longest gaps yet. Show `shortest_first[0]`, the "
                    "shortest, and `shortest_first[-1]`, the longest.",
                ev=_ev(MIXED),
            ),
        ],
        solution=_sort() + "print(shortest_first[0])\nprint(shortest_first[-1])\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="mana_bar = get_mana_bar(caster)",
        why=(
            "You've seen this. `get_mana_bar` ends with `return`, so `mana_bar = ...` caught the bar. `.sort()` "
            "has no answer to hand back, so `result = wall.sort()` catches nothing: `None`."
        ),
    ),
    takeaway="`sorted(wall)` hands back a new sorted list. `wall.sort()` sorts the list itself and hands back `None`.",
    wrong_answers=[
        dict(why="starter unchanged: still empty", code=SORT_STARTER, fails_at=1, message_contains="still empty"),
        dict(why=".sort() returns None: x = x.sort() (spec)", code=_sort("shortest_first = chalk_wall.sort()"),
             fails_at=1, message_contains="None"),
        dict(why="the wall itself sorted and thrown away: chalk_wall = chalk_wall.sort()",
             code=_sort("chalk_wall = chalk_wall.sort()\nshortest_first = []"), fails_at=1, message_contains="threw the wall away"),
        dict(why="changing a copy vs the original: a second name, then .sort()",
             code=_sort("shortest_first = chalk_wall\nshortest_first.sort()"), fails_at=1, message_contains="same list"),
        dict(why="the wall sorted itself, then named", code=_sort("chalk_wall.sort()\nshortest_first = chalk_wall"),
             fails_at=1, message_contains="same list"),
        dict(why="sorted copy made, but the wall sorted too", code=_sort("shortest_first = sorted(chalk_wall)\nchalk_wall.sort()"),
             fails_at=1, message_contains="sorted the wall itself"),
        dict(why="a sorted copy made and forgotten", code=_sort("sorted(chalk_wall)\nshortest_first = []"), fails_at=1,
             message_contains="throws it away"),
        dict(why="the sorted list typed by hand", code=_sort("shortest_first = [37, 41, 44, 46, 47, 48, 48]"),
             fails_at=1, message_contains="typed the sorted gaps"),
        dict(why="square brackets for sorted's round ones", code=_sort("shortest_first = sorted[chalk_wall]"),
             fails_at=0, message_contains="not subscriptable"),
        dict(why="sorted used as a list method", code=_sort("shortest_first = chalk_wall.sorted()"), fails_at=0,
             message_contains="no attribute"),
        dict(why="a slice copy sorted with .sort(): right, but not this step's tool",
             code=_sort("shortest_first = chalk_wall[:]\nshortest_first.sort()"), fails_at=1,
             message_contains="practices `sorted()`"),
        dict(why="the example's list name copied", code=_sort("scores = sorted(chalk_wall)\nshortest_first = []"),
             fails_at=1, message_contains="name from the example"),
        dict(why="the wall turned around: looks sorted only because the real wall shrinks",
             code=_sort("shortest_first = chalk_wall[::-1]"), fails_at=1, message_contains="only looks sorted"),
        dict(why="sorted() line typed above the starter's `shortest_first = []`, which empties it again",
             code=SORT_HEAD + "shortest_first = sorted(chalk_wall)\nshortest_first = []\nprint(shortest_first)\n"
             "print(chalk_wall)\n", fails_at=1, message_contains="again"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="range-slice-sort", solo="false", dictates="",
             foreign_names=",".join(SORT_FOREIGN)) + "\n"
        "Spec: Investigate `result = chalk_wall.sort()` then `print(result)` -> None. It is the predict here, on "
        "`marks`, so the editor's wall is never sorted by the try-it and the check stays fair. CP1 [ND] (teacher "
        "ruling: goal-only; the Example and the `sorted` chip carry the tool, and no CP2, for time): both "
        "values (`shortest_first` sorted, `chalk_wall` unchanged), checked on an unsorted wall `[50, 31, 44, 39, "
        "47]` (the real wall is already in order, newest smallest, so it cannot show a missing sort). Catches the "
        "class's slips: `x = x.sort()` (None, spec WA), `chalk_wall = chalk_wall.sort()`, a second name for the same "
        "list (changing 'a copy' that is really the original), a sorted copy made and forgotten, a typed list, "
        "`sorted[...]`. `None` is only ever printed, never written (const:None is Unit 7). Campaign link: "
        "`get_mana_bar`'s `return` (Obj 7: `.sort()` returning None echoes Unit 3's missing return). BQ (combining "
        "sort + index): the shortest and longest gaps."
    ),
)

# 3B-S -------------------------------------------------------------------------------------------

SOLO_B_STARTER = WALL_LINE + "# The four newest gaps:\nnewest_four = chalk_wall[-4:-1]\nprint(newest_four)\n"


def _solo_b(line="newest_four = chalk_wall[-4:]"):
    return WALL_LINE + "# The four newest gaps:\n" + line + "\nprint(newest_four)\n"


SOLO_3B = dict(
    id="solo-3b",
    title="Show Mar'tu",
    martu=(
        "This code has one [[bug]]. It runs, so read what the Console shows and count the gaps. Is the newest gap, "
        "37, in there? Fix it on your own."
    ),
    solo=True,
    explainer="lean",
    names=["newest_four", "chalk_wall"],
    starter=SOLO_B_STARTER,
    checkpoints=[
        dict(
            id="newest-four",
            text="Change line 3 so `newest_four` holds the four newest gaps.",
            dictated=False,
            hints=[
                "Look at the Console: it shows `[46, 44, 41]`. Is 37, the newest gap, in it?",
                "Line 3's slice ends at `-1`. The end of a slice is left out.",
                "Leave the end empty to run to the edge: `notes[-2:]` is the last two items.",
            ],
            checks=[
                have_list("newest_four", known=["chalk_wall", "newest_four"], foreign=["notes"]),
                follows(
                    "newest_four follows the wall",
                    {"chalk_wall": W6},
                    "_R('newest_four') == _C['chalk_wall'][-4:]",
                    # SOLO (lean): each message names the slip and keeps the evidence bracket, with no fix.
                    rules=[
                        ("_R('newest_four') == _C['chalk_wall'][-4:-1]",
                         "The end of a slice is left out, so the newest gap is missing.", None),
                        ("_R('newest_four') == []", "The slice is empty: it took no gaps.", None),
                        ("_R('newest_four') == _g0.get('newest_four') and _plain('newest_four')",
                         "You typed the gaps into `newest_four` instead of slicing them from the wall.",
                         "'`newest_four` stayed the same'"),
                    ],
                    fix="`newest_four` does not hold the four newest gaps.",
                    ev=_ev(W6),
                    saw="'`newest_four` became ' + _sh(_R('newest_four'))",
                    own=(
                        "_W0 is None or _g0.get('newest_four') == _W0[-4:]",
                        "'The slice fits only the test wall. On your wall, `newest_four` holds ' + "
                        "_sh(_g0.get('newest_four')) + ', not the four newest gaps.'",
                    ),
                ),
            ],
            pass_line="Mar'tu: You did that on your own. Your slice reaches the newest gap.",
        ),
    ],
    solution=_solo_b(),
    # No Assemble it (honest evidence): its pieces would set `[-4:]` beside the starter's `[-4:-1]`, the SOLO's one
    # decision, ahead of every hint.
    another_way=[
        # No fix here (teacher ruling on SOLO messages): these angles are a Help rung, and a SOLO's Learn pane has none.
        dict(angle="step-by-step", text="Count the items it printed. A slice stops before its end number: which item "
             "does `-1` leave out?"),
        dict(angle="shorter", text="The end of a slice is left out. Which gap is missing?"),
    ],
    takeaway="On your own: a slice leaves its end out, so `[-4:]` (not `[-4:-1]`) reaches the newest item.",
    wrong_answers=[
        dict(why="starter unchanged: the slice end is not included", code=SOLO_B_STARTER, fails_at=1,
             message_contains="left out"),
        dict(why="the four typed by hand", code=_solo_b("newest_four = [46, 44, 41, 37]"), fails_at=1,
             message_contains="instead of slicing them"),
        dict(why="the window moved instead of the end opened: [-5:-1]", code=_solo_b("newest_four = chalk_wall[-5:-1]"),
             fails_at=1, message_contains="four newest"),
        dict(why="a start counted for 7 gaps: [3:7]", code=_solo_b("newest_four = chalk_wall[3:7]"), fails_at=1,
             message_contains="four newest"),
        dict(why="a start counted for the check's 6-gap wall: [2:]", code=_solo_b("newest_four = chalk_wall[2:]"),
             fails_at=1, message_contains="On your wall"),
        dict(why="an end of 0 for 'the end': the slice is empty", code=_solo_b("newest_four = chalk_wall[-4:0]"),
             fails_at=1, message_contains="slice is empty"),
        dict(why="seat B's bug: x = wall.sort() used as a list",
             code=WALL_LINE + "newest_four = chalk_wall.sort()\nprint(newest_four[0])\n", fails_at=0,
             message_contains="not subscriptable"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="range-slice-sort", solo="true", dictates="",
             foreign_names="notes",
             seat_b="shortest_first = chalk_wall.sort() then print(shortest_first[0]) (TypeError on None)") + "\n"
        "SOLO, one bug (C6), explainer='lean' (teacher ruling from Unit 2 on). Seat A (and anyone solo) gets a slice "
        "off by one, `chalk_wall[-4:-1]`; seat B would get "
        "`x = wall.sort()` used as a list (`'NoneType' object is not subscriptable`) once pair mode ships. Recorded, "
        "never blocking, never shown to a partner. CMB on a 6-gap wall, so `[3:7]` and a typed list fail, and the "
        "student's own wall too, so a slice that fits only 6 gaps (`[2:]`, `[2:6]`) fails. Teacher ruling on the "
        "Unit 4 reviews: every message names the slip and keeps the evidence bracket, but drops the fix ('The end "
        "of a slice is left out, so the newest gap is missing. (Mar'tu's check tried ...)'), and the pass line uses "
        "Unit 2's ruled SOLO wording."
    ),
)

LESSON_3B = dict(
    kind="lesson",
    id="reading-the-wall-closely",
    title="Reading the Wall Closely",
    minutes=13,
    summary=(
        "Count with `range()`, copy part of a list with a slice like `[-3:]`, and make a sorted copy with "
        "`sorted()`."
    ),
    notes=(
        "Lesson 3B (SC). Preceded by 3b-remembers. Exactly one SOLO (solo-3b). Non-dictated checkpoints: 3B-02 "
        "CP1-2, 3B-03 CP1 and 3B-S. Three ideas, one exercise each, in the spec's order: range (stop left out, like slices), slices "
        "(a new list), sorted versus .sort (None)."
    ),
    exercises=[RANGE_OF_MARKS, SLICE_THE_WALL, SORTED_OR_SORT, SOLO_3B],
)

# ---------------------------------------------------------------------------------------------
# Quiz 3
# ---------------------------------------------------------------------------------------------

QUIZ_3 = dict(
    kind="quiz",
    id="lists-quiz",
    title="Lists Quiz",
    minutes=6,
    summary=(
        "Six questions on positions, lists inside lists, slices, `.sort()` and a recipe. Retake it as often as you like. "
        "Then try Oogrish's Training Log: it puts lists, positions and a recipe together."
    ),
    notes=(
        "Quiz 3 (SC): 4 predict, 1 bug, 1 mc, in the spec's order. Q6 is the def/return item (every unit quiz has one "
        "from Unit 4 on). Q1 and Q4 keep the wall in `setup` and show it in the question (phone width). Review order: "
        "right answers first (G1 R26). Teacher ruling on the Unit 4 reviews: the bug question is the len-as-position "
        "slip (`wall[len(wall)]`), not a third copy of the `[7]` fix; the right choice sits in varied places (the "
        "site shuffles too); the summary points on to the Training Log project."
    ),
    questions=[
        dict(
            type="predict",
            id="last-and-length",
            q="`chalk_wall` holds `[48, 48, 47, 46, 44, 41, 37]`. What will this print?",
            setup=WALL_LINE,
            code="print(chalk_wall[-1])\nprint(len(chalk_wall))\n",
            choices=["48\n7", "37\n7", "37\n6", "41\n7"],
            answer="37\n7",
            explain="`[-1]` counts from the end: the newest gap, 37. `len` counts the gaps: 7.",
            notes="Off-by-one between the count (7) and the last position (6).",
        ),
        dict(
            type="predict",
            id="row-two-name",
            q="What will this print?",
            code=ROSTER_CODE + "print(roster[2][0])\n",
            choices=["Gearshift", "24", "['Bomb Shell', 24]", "Bomb Shell"],
            answer="Bomb Shell",
            explain=(
                "Row 2 is the third row, Bomb Shell's, because rows start at 0. Then `[0]` is the first item in that "
                "row: the name."
            ),
        ),
        dict(
            type="bug",
            id="newest-gap",
            q="This code should show the newest gap, 37, but Python stops with an error. Fix it.",
            code="wall = [48, 48, 47, 46, 44, 41, 37]\nprint(wall[len(wall)])\n",
            fix="wall = [48, 48, 47, 46, 44, 41, 37]\nprint(wall[-1])\n",
            expected_output="37",
            explain=(
                "Seven gaps sit at positions 0 to 6, so `len(wall)`, 7, is one past the end. `[-1]`, or "
                "`[len(wall) - 1]`, reads the last item."
            ),
            notes="The len-as-position slip (an IndexError). Either mend prints 37.",
        ),
        dict(
            type="predict",
            id="last-three",
            q="`chalk_wall` holds `[48, 48, 47, 46, 44, 41, 37]`. What will this print?",
            setup=WALL_LINE,
            code="print(chalk_wall[-3:])\n",
            choices=["[44, 41, 37]", "[44, 41]", "[41, 37]", "44"],
            answer="[44, 41, 37]",
            explain="`[-3:]` starts 3 from the end and runs to the edge: the last three gaps, as a new list.",
            notes="Distractor [44, 41] is the slice-end slip ([-3:-1]).",
        ),
        dict(
            type="mc",
            id="what-sort-hands-back",
            q="`wall` is a list of gaps. After `result = wall.sort()` runs, what does `result` hold?",
            choices=["the sorted list", "the wall, not sorted", "`None`: nothing came back", "the smallest gap"],
            answer=2,
            why_wrong={
                0: "`.sort()` sorts `wall` itself, but hands nothing back. `sorted(wall)` is the one that hands back a list.",
                1: "Nothing comes back from `.sort()` at all, so `result` gets `None`, not a copy of the wall.",
                3: "`.sort()` hands back nothing. The smallest gap would be `sorted(wall)[0]`.",
            },
            explain=(
                "`.sort()` sorts the list itself and hands back nothing, so `result` holds `None`, Python's word for "
                "nothing. It's like a recipe with no `return`."
            ),
        ),
        dict(
            type="predict",
            id="first-mark-recipe",
            q="What will this print?",
            code="def first_mark(wall):\n    return wall[0]\n\nprint(first_mark([9, 8]))\n",
            choices=["8", "9", "[9, 8]", "0"],
            answer="9",
            explain="The call hands over `[9, 8]`, so inside the recipe `wall` is `[9, 8]`. `wall[0]` is 9, handed back.",
        ),
    ],
)

ITEMS = [REMEMBERS_3A, LESSON_3A, REMEMBERS_3B, LESSON_3B, QUIZ_3]
