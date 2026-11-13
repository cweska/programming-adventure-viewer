"""Unit 1 "Hello World", part c: Lesson 1C "Math and Glue", Extra practice 1X-C, Quiz 1 "Chalk Quiz" and
Project 1P1 "The Night Watch Ledger".

Spec: design/curriculum.md, "## Unit 1", items 6 to 9 (1c-remembers; 1C-01 to 1C-04, 1C-06 to 1C-09, 1C-S;
1C-05 and 1C-T in the pool; Quiz 1; Project 1P1). Introduces op:Add, op:Sub, op:Mult, op:Div (1C-01),
call:str (1C-06) and node:AugAssign (1C-05, pool only: no core code shows `+=`).

Who this is for: the class already played campaign Modules 1 and 2 and struggled most with exactly this part:
nobody let the code combine values (everyone hard-coded 68), counts and prices were swapped, and `mana-bars` /
`hold-the-barrier` felt like a wall. So every combine step is checked by BEHAVIOR: the check re-runs the
student's program with other numbers (CMB, curriculum 2.5) and the message shows the little rerun table in one
sentence ("Mar'tu's check tried your code with `lantern_count = 7` (only inside the check: leave your own numbers
as they are). This time, `total_cost` stayed 22, but it should be 38."). Mar'tu says once, in chalk-math, that
the checks swap in other numbers.

Check builders below (plain string templates, no student values ever echoed back):
  slot()        NAME / LEFT / NEWBOX / BARE / TEXT-vs-NUM plus per-exercise rules, for one box's value
  story_pair()  SWAP / LINE-TOTAL / wild count / placeholder / NEWBOX, for a count box and a price box from a story
                (a right pair always passes; the diagnosis runs only when it is wrong)
  rerun()       CMB: re-runs _source with some input lines changed (the "Try other numbers" mechanism). Every
                input a combine line reads is changed by at least one rerun, so no half-typed line survives.
  rerun_line()  CMB on output. The wanted line must come from a line that CHANGED with the inputs: a line that
                prints the same in both runs is typed in (stops `print(11)` + `print(7)` after the message shows 7).
  out_line()    OUT diff: the expected line, the nearest printed line, and where they first differ. `hide=own(box)`
                keeps lines holding a student's creative value out of every diff (privacy, 2.11).
  loose_math() / set_once() / near_names()   BARE math, a box re-set below its uses, NAME on its own
Help ladder as fields: hints[0] Start me off, hints[1] Point, another_way, hints[2] Teach (other names),
assemble = More structure, solution = Show.
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
TEXT_NOT_NUM = "`%s` holds text, because of the quotes. Numbers don't need quotes."

# Shared preamble: which names the student made, near-miss test, lone values, and the namespace.
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
    "_bare = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Constant']\n"
    "_g = globals()\n"
)

# CMB: re-run the student's program with some `name = <literal>` lines changed. Prints go to a private buffer.
_RERUN_DEF = (
    "import ast as _ast, io as _io, sys as _sys\n"
    "def _rerun(_changes):\n"
    "    _tree = _ast.parse(_source)\n"
    "    _found = []\n"
    "    _sets = {}\n"
    "    for _n in _tree.body:\n"
    "        if type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name' "
    "and _n.targets[0].id in _changes:\n"
    "            _sets.setdefault(_n.targets[0].id, []).append(_n)\n"
    "    for _k, _ns_ in _sets.items():\n"
    "        _lit = [_n for _n in _ns_ if type(_n.value).__name__ == 'Constant']\n"
    "        for _n in (_lit or _ns_[:1]):\n"
    "            _n.value = _ast.Constant(_changes[_k])\n"
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
    "def _nearest(_lines_, _want):\n"
    "    def _pre(_l):\n"
    "        _k = 0\n"
    "        while _k < len(_l) and _k < len(_want) and _l[_k] == _want[_k]:\n"
    "            _k += 1\n"
    "        return _k\n"
    "    return max(_lines_, key=_pre).replace('`', \"'\") if _lines_ else ''\n"
)


def _fmt(value):
    return '"' + value + '"' if isinstance(value, str) else str(value)


def _with_text(changes):
    parts = ["`%s = %s`" % (key, _fmt(value)) for key, value in changes.items()]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def rerun(label, changes, pre, cond, msg):
    """CMB. Re-runs the student's program with `changes` swapped in, inside the check only (the student's own
    code and numbers are never touched). `pre` sets up names from the rerun (_r its namespace, _R = _r.get, _p its
    printed lines); `cond` must hold; `msg` is an expression for the rest of the message after the shared lead:
    "Mar'tu's check tried your code with `last_gap = 41` (only inside the check: leave your own numbers as they
    are). This time, " + msg. One lead for every rerun message, so the check reads as fair, not as a trick. A rerun
    that crashes says "Mar'tu's check tried your code with ... (only inside the check) and it stopped: " + error."""
    kind = "numbers" if all(isinstance(v, int) for v in changes.values()) else "values"
    lead = (
        "Mar'tu's check tried your code with %s (only inside the check: leave your own numbers as they are). "
        "This time, " % _with_text(changes)
    )
    keep = "`. Mar'tu's check changes that line to try other " + kind + ", so keep it as `name = value`."
    crash = "Mar'tu's check tried your code with %s (only inside the check) and it stopped: " % _with_text(changes)
    code = _RERUN_DEF + (
        f"_r, _p, _f, _e = _rerun({changes!r})\n"
        "_R = _r.get\n"
        "_g0 = globals()\n"
        f"_miss = [_k for _k in {list(changes)!r} if _k not in _f]\n"
        "assert not _miss or _miss[0] in _g0, 'Make a box named `' + (_miss[0] if _miss else '') + "
        "'`: start a line with `' + (_miss[0] if _miss else '') + ' = `.'\n"
        f"assert not _miss, 'Keep the line that sets `' + (_miss[0] if _miss else '') + {keep!r}\n"
        f"assert not _e, {crash!r} + _e\n"
        f"{pre}\n"
        f"assert {cond}, {lead!r} + {msg}\n"
    )
    return (label, code)


def rerun_box(label, changes, target, want, fix):
    """CMB on one box: after the rerun, `target` must equal `want` (an expression over _R)."""
    return rerun(
        label,
        changes,
        f"_want = {want}\n_got = _R({target!r})\n_was = _g0.get({target!r})",
        "_got == _want and type(_got).__name__ == type(_want).__name__",
        f"'`{target}` ' + ('stayed ' if _got == _was else 'became ') + str(_got) + ', but it should be ' + str(_want) + '. ' + {fix!r}",
    )


def rerun_line(label, changes, want, fix, show=True, hide="''", word=False, starts=False):
    """CMB on printed output: after the rerun, the line `want` (an expression over _R) must be printed, by a
    line that FOLLOWED the change. A line that prints `want` in the normal run too (at the same place) is typed
    in: that stops `print(11)` + `print(7)` once the message has shown 7 (unless the rerun changed nothing).
    word=True: a printed line counts when it holds `want` as a whole number (labelled output such as
    `The gap shrank by 7` counts; `17`, `-7` and `7.5` do not). starts=True: a printed line counts when it starts
    with `want` (a first bead such as `Tester has`). The typed-in test against the normal run uses the same match.
    `hide` (an expression over the student's names, e.g. a creative hero box) is never repeated back: the nearest
    printed line is left out of the message when it contains it (privacy, 2.11)."""
    shown = (
        "(', but it printed nothing' if not _p else ('' if (_hide and _hide in _nn) else ', but it printed `' + _nn + '`'))"
        if show
        else "''"
    )
    if word:
        hit = (
            "import re as _re\n"
            r"_pat = _re.compile(r'(?<![\w.-])' + _re.escape(_want) + r'(?![\w.])')" "\n"
            "_hit = lambda _l: bool(_pat.search(_l))\n"
        )
    elif starts:
        hit = "_hit = lambda _l: _l.startswith(_want)\n"
    else:
        hit = "_hit = lambda _l: _l == _want\n"
    if starts:
        typed = (
            "('your program printed a line that starts with `' + _want + '`, but that line is the same even without "
            "the change, so it is typed in. ')"
        )
        should = f"('your program should print a line that starts with `' + _want + '`' + {shown} + '. ')"
    else:
        typed = (
            "('your program printed `' + _want + '`, but that line prints `' + _want + '` even without the change, "
            "so it is typed in. ')"
        )
        should = f"('your program should print `' + _want + '`' + {shown} + '. ')"
    return rerun(
        label,
        changes,
        f"_want = {want}\n"
        f"_hide = str({hide} or '').strip()\n"
        + hit
        + "_nn = _nearest(_p, _want) if _p else ''\n"
        "_old = _lines()\n"
        f"_same = all(_g0.get(_k) == _v for _k, _v in {changes!r}.items())\n"
        "_at = [_i for _i, _l in enumerate(_p) if _hit(_l)]\n"
        "_ok = bool(_at) and (_same or any(_i >= len(_old) or not _hit(_old[_i]) for _i in _at))",
        "_ok",
        f"({typed} if _at else {should}) + {fix!r}",
    )


def slot(label, name, want, *, known, default, foreign=(), rules=()):
    """One box must hold `want` (an expression over the student's names). The message says why not:
    a rule (rules = [(condition, message)]), text instead of a number, a near-miss name (NAME), an example's
    name (LEFT), a new box holding the answer (NEWBOX), a lone value (BARE), or the default."""
    rule_code = "".join(
        f"    if not _msg and ({cond}):\n        _msg = {message!r}\n" for cond, message in rules
    )
    code = _NAMES_PRE + (
        f"_name = {name!r}\n"
        f"_known = {list(known)!r}\n"
        f"_foreign = {list(foreign)!r}\n"
        f"_want = {want}\n"
        "_have = _g.get(_name)\n"
        "_ok = _name in _g and type(_have).__name__ == type(_want).__name__ and _have == _want\n"
        "_msg = ''\n"
        "if not _ok and _name in _g:\n"
        f"{rule_code}"
        "    if not _msg and type(_have).__name__ == 'str' and type(_want).__name__ != 'str':\n"
        f"        _msg = {TEXT_NOT_NUM % name!r}\n"
        "_near = [_m for _m in _made if _m != _name and _m not in _known and _m not in _foreign and _close(_m, _name)]\n"
        "_left = [_m for _m in _made if _m in _foreign and _m != _name]\n"
        "_newb = [_m for _m in _made if _m != _name and _m not in _known and _m not in _foreign "
        "and type(_g.get(_m)).__name__ == type(_want).__name__ and _g.get(_m) == _want]\n"
        "if not _ok and not _msg and _near:\n"
        f"    _msg = 'Python matches names letter for letter: you wrote `' + _near[0] + {'`, the task needs `' + name + '`.'!r}\n"
        "if not _ok and not _msg and _left:\n"
        f"    _msg = '`' + _left[0] + {'` is a name from the example or an earlier step. This task' + chr(39) + 's box is `' + name + '`.'!r}\n"
        "if not _ok and not _msg and _newb:\n"
        f"    _msg = 'Your new box `' + _newb[0] + '` holds ' + str(_want) + ', but `{name}` ' + "
        f"('still holds ' + str(_have) if _name in _g else 'is not made yet') + {'. Put it in `' + name + '`.'!r}\n"
        "if not _ok and not _msg and _name not in _g and _bare:\n"
        f"    _msg = 'Line ' + str(_bare[0]) + {' is a value with no box, so Python made it and forgot it. Put `' + name + ' = ` in front of it.'!r}\n"
        "if not _ok and not _msg and _name not in _g:\n"
        f"    _msg = {'Make a box named `' + name + '`: start a line with `' + name + ' = `.'!r}\n"
        "if not _ok and not _msg and _have == 0 and _want != 0:\n"
        f"    _msg = {'`' + name + '` still holds the placeholder 0. ' + default!r}\n"
        "if not _ok and not _msg:\n"
        f"    _msg = {default!r}\n"
        "assert _ok, _msg\n"
    )
    return (label, code)


def story_pair(label, count_name, price_name, count, price, things, *, known, wild, price_first=False, swap_extra=""):
    """SWAP / LINE-TOTAL / wild count / placeholder / NEWBOX for a count box and a price box filled from a story.
    A right pair always passes (no near-miss nagging about other boxes); the diagnosis runs only when it is wrong.
    `swap_extra` is appended to the SWAP message (e.g. why a swapped pair still gives the right product)."""
    swap = "You swapped them: %d is how many %s, %d is the price of one." % (count, things, price)
    if price_first:
        swap += " This story gives the price first."
    swap += swap_extra
    line_total = "%d is already the cost of all %d %s. This box wants the price of one." % (count * price, count, things)
    count_total = "%d is already the cost of all %d %s. This box wants how many." % (count * price, count, things)
    code = _NAMES_PRE + (
        f"_names = {[count_name, price_name]!r}\n"
        f"_known = {list(known)!r}\n"
        f"_wants = {{{count_name!r}: {count}, {price_name!r}: {price}}}\n"
        "_num = lambda _v: type(_v).__name__ in ('int', 'float')\n"
        "_ok = all(_w in _g and _num(_g[_w]) and _g[_w] == _wants[_w] for _w in _names)\n"
        "_msg = ''\n"
        "_near = [(_m, _w) for _w in _names for _m in _made if _m not in _known and _m not in _names and _close(_m, _w)]\n"
        "if not _ok and _near:\n"
        "    _msg = 'Python matches names letter for letter: you wrote `' + _near[0][0] + '`, the task needs `' + _near[0][1] + '`.'\n"
        "for _w in _names:\n"
        "    if not _ok and not _msg and _w not in _g and _bare:\n"
        "        _msg = 'Line ' + str(_bare[0]) + ' is a value with no box, so Python made it and forgot it. "
        "Put `' + _w + ' = ` in front of it.'\n"
        "    if not _ok and not _msg and _w not in _g:\n"
        "        _msg = 'Make a box named `' + _w + '`: start a line with `' + _w + ' = `.'\n"
        "    if not _ok and not _msg and type(_g[_w]).__name__ == 'str':\n"
        f"        _msg = '`' + _w + {TEXT_NOT_NUM[3:]!r}\n"
        "if not _ok and not _msg:\n"
        f"    _c, _p = _g[{count_name!r}], _g[{price_name!r}]\n"
        "    _newb = [(_m, _w) for _w in _names for _m in _made if _m not in _known and _m not in _names "
        "and _g[_w] == 0 and _num(_g.get(_m)) and _g.get(_m) == _wants[_w]]\n"
        f"    if _c == {price} and _p == {count}:\n"
        f"        _msg = {swap!r}\n"
        f"    elif _p == {count * price}:\n"
        f"        _msg = {line_total!r}\n"
        f"    elif _c == {count * price}:\n"
        f"        _msg = {count_total!r}\n"
        "    elif _newb:\n"
        "        _msg = 'Your new box `' + _newb[0][0] + '` holds ' + str(_wants[_newb[0][1]]) + ', but `' + _newb[0][1] + "
        "'` still holds 0. Put the number in `' + _newb[0][1] + '`.'\n"
        f"    elif _c not in (0, {count}, {price}):\n"
        f"        _msg = {wild!r}\n"
        "    elif _c == 0 or _p == 0:\n"
        "        _msg = 'A 0 is a placeholder: replace it with the number from the story.'\n"
        f"    elif _c != {count}:\n"
        f"        _msg = {'`' + count_name + '` answers how many ' + things + '. Read the story again.'!r}\n"
        "    else:\n"
        f"        _msg = {'`' + price_name + '` answers how much one costs. Read the story again.'!r}\n"
        "assert _ok, _msg\n"
    )
    return (label, code)


def out_line(label, want, missing, privacy=False, spaces="Check the spaces in your line: every space counts.", hide="''"):
    """OUT diff: `want` (an expression) must be printed. Shows the nearest printed line and where it first
    differs, unless privacy=True (the line holds the student's own creative text). `hide` (an expression, e.g. a
    creative hero box) keeps other lines that hold the student's own text out of the diff."""
    if privacy:
        code = (
            f"_want = ({want}).strip()\n"
            "_flat = [_l.replace(' ', '') for _l in _lines()]\n"
            f"assert _want in _lines() or _want.replace(' ', '') not in _flat, {spaces!r}\n"
            f"assert _want in _lines(), {missing!r}\n"
        )
        return (label, code)
    code = (
        f"_want = {want}\n"
        f"_hide = str({hide} or '').strip()\n"
        "_ls = _lines()\n"
        "_cands = [_l for _l in _ls if not (_hide and _hide in _l)]\n"
        "def _pre(_l):\n"
        "    _k = 0\n"
        "    while _k < len(_l) and _k < len(_want) and _l[_k] == _want[_k]:\n"
        "        _k += 1\n"
        "    return _k\n"
        "_msg = ''\n"
        "if _want not in _ls and not _ls:\n"
        f"    _msg = 'Nothing is printed yet. ' + {missing!r}\n"
        "elif _want not in _ls and not _cands:\n"
        f"    _msg = 'Expected `' + _want + '`, and no printed line matches it yet. ' + {missing!r}\n"
        "elif _want not in _ls:\n"
        "    _near = max(_cands, key=_pre)\n"
        "    _i = _pre(_near)\n"
        "    _shown = _near.replace('`', \"'\")\n"
        "    _head = 'Expected `' + _want + '`, you printed `' + _shown + '`. '\n"
        "    _before = _want[:_i].strip()\n"
        "    if _i == 0:\n"
        "        _msg = _head + 'They differ at the very start. ' + " + repr(missing) + "\n"
        "    elif _want[_i:_i + 1] == ' ' and _near[_i:_i + 1] != ' ':\n"
        "        _msg = _head + 'A space is missing right after `' + _before + '`.'\n"
        "    elif _near[_i:_i + 1] == ' ' and _want[_i:_i + 1] != ' ':\n"
        "        _msg = _head + 'There is an extra space right after `' + _before + '`.'\n"
        "    elif _i >= len(_near):\n"
        "        _msg = _head + 'Your line stops early, right after `' + _before + '`.'\n"
        "    else:\n"
        "        _msg = _head + 'They differ right after `' + _before + '`.'\n"
        "assert not _msg, _msg\n"
    )
    return (label, code)


def no_bare_math(label, box):
    """A line that works out a sum but keeps it nowhere: `mana - spell_cost` on its own raises no error."""
    return (
        label,
        "import ast as _ast\n"
        "_loose = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'BinOp']\n"
        "assert not _loose, 'Line ' + str(_loose[0] if _loose else 0) + "
        f"{' works out a new number, but `' + box + '` didn' + chr(39) + 't change: put the answer back with `' + box + ' = ` in front.'!r}",
    )


def loose_math(label):
    """BARE for math: a line that works out a number but keeps it nowhere (`lantern_count * lantern_price` on its
    own raises no error, and the box keeps its 0)."""
    return (
        label,
        "import ast as _ast\n"
        "_loose = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'BinOp']\n"
        "assert not _loose, 'Line ' + str(_loose[0] if _loose else 0) + ' works out a number, but keeps it nowhere. "
        "Which box should keep it? Put that box' + chr(39) + 's name and `=` in front.'",
    )


def set_once(label, names):
    """A box that is set again BELOW the lines that use it: those lines never see the new number, because Python
    runs from the top down (`rope_count = 1000` added at the bottom instead of changing line 3)."""
    return (
        label,
        "import ast as _ast\n"
        "_body = _ast.parse(_source).body\n"
        "_late = []\n"
        f"for _k in {list(names)!r}:\n"
        "    _sets = [_n.lineno for _n in _body if type(_n).__name__ == 'Assign' and any(getattr(_t, 'id', '') == _k for _t in _n.targets)]\n"
        "    _uses = [_n.lineno for _n in _ast.walk(_ast.Module(body=_body, type_ignores=[])) if type(_n).__name__ == 'Name' "
        "and _n.id == _k and type(_n.ctx).__name__ == 'Load']\n"
        "    if len(_sets) > 1 and any(_sets[0] < _u < _sets[-1] for _u in _uses):\n"
        "        _late.append((_k, _sets[0], _sets[-1]))\n"
        "assert not _late, '`' + (_late[0][0] if _late else '') + '` is set again on line ' + str(_late[0][2] if _late else 0) + "
        "', below the lines that use it. Python runs from the top down, so those lines never see the new number. "
        "Change line ' + str(_late[0][1] if _late else 0) + ' instead.'",
    )


def near_names(label, names, known):
    """NAME on its own: a box whose name is a near miss of a required name (`Mana` for `mana`)."""
    return (
        label,
        _NAMES_PRE
        + f"_names = {list(names)!r}\n_known = {list(known)!r}\n"
        "_near = [(_m, _w) for _w in _names for _m in _made if _m not in _known and _m not in _names and _close(_m, _w)]\n"
        "assert not _near, 'Python matches names letter for letter: you wrote `' + (_near[0][0] if _near else '') + "
        "'`, the task needs `' + (_near[0][1] if _near else '') + '`.'\n",
    )


# The party's own names are no secret; any other value in a creative box is the student's and is never shown back.
WORLD_NAMES = ("Lucky", "Oogrish", "Gearshift", "Bomb Shell", "Mar'tu", "Tester")


def own(box):
    """`hide` expression: the student's text in `box`, unless it is one of the party's names."""
    return f"(globals().get({box!r}) if globals().get({box!r}) not in {WORLD_NAMES!r} else '')"


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of hello-world)
# ---------------------------------------------------------------------------------------------

UNIT = dict(
    id="hello-world",
    order=1,
    title="Hello World",
    subtitle="Words by the Fire",
    published=True,
    martu_intro=(
        "Hi. It is me, Mar'tu. Before we continue on our adventure, we go back to the first words, yes?\n"
        "A lot of that campaign code felt like a wall, yes? We will take the wall apart, one stone at a time.\n"
        "Every spell begins as words. Python is fussy about words. More fussy than Lucky is about glug, yes?\n"
        "Tonight: how to say something, how to keep something in a box, and how to let Python do the sums."
    ),
    goals=[
        "Show words on the screen with `print()`, in matching quotes",
        "Write `#` notes for humans, and switch a line off",
        "Make a box (variable) with `name = value`, using the exact name the task asks for",
        "Put a new value in a box, like `mana = mana - cost`",
        "Do math with `+`, `-`, `*` and `/`, and let the code combine your boxes",
        "Glue text together with `+` and `str()`, and draw a bar with `\"█\" * mana`",
        "Read Python's message and mend the slips everyone makes",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="math signs",
        aliases=["math sign", "operator", "operators"],
        plain="The signs Python does math with: `+` adds, `-` subtracts, `*` multiplies (times), `/` divides.",
        example="print(48 - 37)",
    ),
    dict(
        term="decimal",
        aliases=["decimals", "decimal number"],
        plain="A number with a point in it, like `24.0` or `42.5`. Dividing with `/` always gives one.",
        example="print(48 / 2)",
    ),
    dict(
        term="placeholder",
        aliases=["placeholders"],
        plain="A stand-in value, like the `0` in a starter. It holds the place until you put the real thing there.",
        example="lantern_count = 0",
    ),
    dict(
        term="show your working",
        aliases=["combine", "let the code combine it", "build it from the boxes"],
        plain=(
            "Build a value from boxes, like `total_cost = lantern_cost + rope_cost`, instead of typing the answer. "
            "Then it stays right when a box changes."
        ),
        example="total_cost = lantern_cost + rope_cost",
    ),
    dict(
        term="glue",
        aliases=["glues", "gluing", "concatenate", "concatenation"],
        plain="Join texts end to end with `+`. Python adds no spaces, so put the spaces inside the quotes.",
        example='"Shield" + " up."',
    ),
    dict(
        term="str()",
        aliases=["str"],
        plain="Turns a value into text. `str(26)` gives the text `\"26\"`, which can be glued to other text.",
        example='"Mana: " + str(26)',
    ),
    dict(
        term="stamp",
        aliases=["stamps", "repetition", "repeat a mark"],
        plain="`*` with text and a number stamps the text that many times. `\"█\" * 3` gives `███`.",
        example='"█" * 3',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (1c-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_1C = dict(
    kind="quiz",
    id="1c-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from earlier lessons. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 1C; recall from 1B (box vs quoted name) and "
        "1A (closing quote). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="which-makes-a-box",
            q="Which line makes a box?",
            choices=['"hero" = "Lucky"', 'hero = "Lucky"'],
            answer=1,
            why_wrong={0: "A box's name never goes in quotes. The name is a label, not text to show."},
            explain="`hero = \"Lucky\"` makes a box named `hero` with Lucky inside. " + QUOTES_RULE,
        ),
        dict(
            type="bug",
            id="mend-shield-up",
            q="Mend this line so it shows Shield up.",
            code='print("Shield up.)\n',
            fix='print("Shield up.")\n',
            expected_output="Shield up.",
            explain="Quotes come in pairs. Add the closing `\"` right after the period.",
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 1C "Math and Glue"
# ---------------------------------------------------------------------------------------------

LANTERN_STORY = "# Mar'tu needs 3 lanterns that cost 4 coins each.\n"
ROPE_STORY = "# Rope costs 2 coins a coil, and Mar'tu needs 5 coils.\n"

CHALK_MATH = dict(
    id="chalk-math",
    title="Mar'tu's chalk math",
    martu=(
        "Python does math with `+`, `-`, `*` and `/`. Guess each answer, then run.\n"
        "These are the [[math signs]]. No quotes around the math, so Python works it out.\n"
        "My checks are sneaky: they put other numbers in your boxes and run your code again, to see if your line "
        "follows. Your own code is not changed. A typed answer can't keep up."
    ),
    introduces=["op:Add", "op:Sub", "op:Mult", "op:Div"],
    example="owl_hoots = 6\nwolf_howls = 3\nprint(owl_hoots + wolf_howls)\n",
    example_output="9",
    names=["first_gap", "last_gap"],
    predict=dict(
        q="What will this print?",
        code="print(46 + 44)\nprint(48 - 37)\nprint(9 * 2)\n",
        choices=["90\n11\n18", "46 + 44\n48 - 37\n9 * 2", "90 11 18 all on one line"],
        answer=0,
        explain=(
            "Python works out each sum and prints the answer, not the sum. Now add `print(48 / 2)` and run. "
            "Surprised? Dividing with `/` always gives a [[decimal]]: `24.0` is the same amount as 24."
        ),
    ),
    pair_talk=(
        "Pair talk: each of you guesses the three answers first. Compare, then each of you runs your own code. "
        "Then both add `print(48 / 2)`: who expected the `.0`?"
    ),
    starter=(
        "first_gap = 48\n"
        "last_gap = 37\n"
        "# Replace 0 with how much the gap shrank, using the two boxes.\n"
        "print(0)\n"
    ),
    checkpoints=[
        dict(
            id="print-the-shrink",
            text="Replace the `0` so the line prints how much the gap shrank. Use `first_gap` and `last_gap`.",
            dictated=True,
            hints=[
                "Start like this: `print(first_gap - `",
                "Which two boxes hold the gaps? The line should use both, with no numbers typed in.",
                "Python can subtract boxes. If `a = 9` and `b = 4`, then `print(a - b)` shows 5. "
                "No quotes around it, so Python does the math.",
            ],
            checks=[
                # Labelled output counts (A-06): a line holding 11 as a whole number, like `The gap shrank by 11`.
                (
                    "no quotes around the math",
                    "import re as _re\n"
                    r"_eleven = any(_re.search(r'(?<![\w.-])11(?![\w.])', _l) for _l in _lines())" "\n"
                    "assert _eleven or not any('first_gap' in _l or 'last_gap' in _l for _l in _lines()), "
                    "'That printed the letters, because of the quotes. Take the quotes off so Python does the math. "
                    + QUOTES_RULE + "'",
                ),
                (
                    "bigger gap first",
                    "import re as _re\n"
                    r"assert not any(_re.search(r'(?<![\w.])-11(?![\w.])', _l) for _l in _lines()), "
                    "'Your line printed -11. Put the bigger gap first: `first_gap - last_gap`.'",
                ),
                (
                    "prints 11",
                    "import re as _re\n"
                    r"assert any(_re.search(r'(?<![\w.-])11(?![\w.])', _l) for _l in _lines()), "
                    "'The gap shrank by 11, and your program does not print 11 yet. "
                    "Replace the 0 with the two boxes and a minus sign.'",
                ),
                rerun_line(
                    "the shrink is built from the boxes",
                    {"last_gap": 41},
                    "str(_R('first_gap') - _R('last_gap'))",
                    "Your 11 is right for 48 and 37. Use the two boxes, so Python does the math for any numbers.",
                    word=True,
                ),
                rerun_line(
                    "the shrink uses first_gap too",
                    {"first_gap": 52},
                    "str(_R('first_gap') - _R('last_gap'))",
                    "Use the box `first_gap` too, not the number 48.",
                    word=True,
                ),
            ],
            pass_line="Gearshift: Math checks out.",
        ),
    ],
    solution=(
        "first_gap = 48\n"
        "last_gap = 37\n"
        "# Replace 0 with how much the gap shrank, using the two boxes.\n"
        "print(first_gap - last_gap)\n"
    ),
    assemble=dict(
        lines=["first_gap = 48", "last_gap = 37", "print(first_gap - last_gap)"],
        distractors=["print(11)", 'print("first_gap - last_gap")', "print(last_gap - first_gap)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two jars",
            text=(
                "Two jars and a minus sign:\n"
                "```text\n[ first_gap: 48 ]  -  [ last_gap: 37 ]  ->  11\n```\n"
                "Python opens both jars, takes one number from the other, and prints the answer."
            ),
        ),
        dict(
            angle="everyday",
            label="A calculator that remembers",
            text=(
                "A box is a calculator memory. `first_gap - last_gap` says: take the number saved as first_gap, "
                "minus the one saved as last_gap. Change a saved number, and the answer changes with it."
            ),
        ),
        dict(
            angle="in Tor",
            label="The chalk wall",
            text=(
                "My chalk wall: 48, 48, 47, 46, 44, 41, 37. Each number is the hours between two bursts. "
                "The first gap was 48. The last was 37. How much did it shrink? 48 take away 37."
            ),
        ),
        dict(angle="shorter", text="`print(first_gap - last_gap)`: two boxes, a minus sign, no quotes."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants the middle of it. On a new line, print the average of the first and last gap: "
            "add them in brackets, then divide by 2."
        ),
        hints=[
            "Start like this: `print((first_gap + last_gap) / 2)`",
            "Python does `/` before `+`, so the brackets make it add first.",
        ],
        checks=[
            (
                "prints the average",
                "import re as _re\n"
                r"assert any(_re.search(r'(?<![\w.-])42\.5(?![\w.])', _l) for _l in _lines()), "
                "'Print the average: `(first_gap + last_gap) / 2` gives 42.5.'",
            ),
            rerun_line(
                "the average is built from the boxes",
                {"last_gap": 41},
                "str((_R('first_gap') + _R('last_gap')) / 2)",
                "Use the two boxes in brackets, then `/ 2`.",
                word=True,
            ),
        ],
        solution=(
            "first_gap = 48\nlast_gap = 37\nprint(first_gap - last_gap)\nprint((first_gap + last_gap) / 2)\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "You have seen this wall: 48, 48, 47, 46, 44, 41, 37. Gearshift's visor dimmed while he ran the math in "
            "his head. Now Python runs it for you."
        ),
    ),
    takeaway="`+ - * /` do math. Use the boxes, not the answer: `print(first_gap - last_gap)`. `/` gives a decimal.",
    wrong_answers=[
        dict(why="the answer typed by hand (everyone's 68)", code="first_gap = 48\nlast_gap = 37\nprint(11)\n",
             fails_at=1, message_contains="41"),
        dict(why="numbers instead of boxes", code="first_gap = 48\nlast_gap = 37\nprint(48 - 37)\n",
             fails_at=1, message_contains="41"),
        dict(why="the math in quotes", code='first_gap = 48\nlast_gap = 37\nprint("first_gap - last_gap")\n',
             fails_at=1, message_contains="exact letters"),
        dict(why="boxes the wrong way round", code="first_gap = 48\nlast_gap = 37\nprint(last_gap - first_gap)\n",
             fails_at=1, message_contains="bigger gap first"),
        dict(why="a name spelled differently", code="first_gap = 48\nlast_gap = 37\nprint(first_gap - lastgap)\n",
             fails_at=0, message_contains="not defined"),
        dict(why="half typed: 48 instead of first_gap (passes the last_gap rerun)",
             code="first_gap = 48\nlast_gap = 37\nprint(48 - last_gap)\n", fails_at=1, message_contains="first_gap = 52"),
        dict(why="gaming the message: the typed 11 plus the 7 the message showed",
             code="first_gap = 48\nlast_gap = 37\nprint(11)\nprint(7)\n", fails_at=1, message_contains="typed in"),
        dict(why="the example's names copied (A-05/A-07/A-08 player_name)",
             code="first_gap = 48\nlast_gap = 37\nprint(owl_hoots - wolf_howls)\n", fails_at=0, message_contains="not defined"),
        dict(why="labelled answer typed in whole (A-06 style, but no boxes)",
             code='first_gap = 48\nlast_gap = 37\nprint("The gap shrank by 11")\n', fails_at=1,
             message_contains="Your 11 is right for 48 and 37"),
        dict(why="labelled output with the boxes the wrong way round",
             code='first_gap = 48\nlast_gap = 37\nprint("The gap shrank by", last_gap - first_gap)\n', fails_at=1,
             message_contains="bigger gap first"),
        dict(why="labelled output typed in, then the 7 the message showed added (gaming, word match)",
             code='first_gap = 48\nlast_gap = 37\nprint("The gap shrank by 11")\nprint("or by 7")\n', fails_at=1,
             message_contains="typed in"),
        dict(why="the math in quotes next to a typed label",
             code='first_gap = 48\nlast_gap = 37\nprint("The gap shrank by", "first_gap - last_gap")\n', fails_at=1,
             message_contains="exact letters"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="combine-values", solo="false", dictates="1",
             foreign_names="owl_hoots,wolf_howls,a,b") + "\n"
        "Predict = three of the spec's sums (90, 11, 18); Investigate (why 24.0) is the predict explanation, which "
        "asks the student to add `print(48 / 2)` and run, so the `.0` is a discovery, not a trap. Mar'tu's Learn "
        "text says once that the checks swap in other numbers (inside the check only), so the reruns read as fair. "
        "Try other numbers: the CMB rerun (last_gap 41 -> 7) is the mechanism; its message names the changed line. "
        "Labelled output counts (A-06): every check matches 11 / the rerun's number as a whole number in any printed "
        "line (`The gap shrank by 11` and `first_gap - last_gap = 11` pass; a typed `The gap shrank by 11` still "
        "fails the reruns). "
        "WA evidence: everyone's hard-coded 68 (A-05, A-07, A-08, B-01, B-02, B-03, A-01, A-06)."
    ),
)

WHAT_EACH_NUMBER_MEANS = dict(
    id="what-each-number-means",
    title="What does each number mean?",
    martu=(
        "Before any math, ask two questions about each number: how many? how much is one? "
        "Put each number in the box that means that.\n"
        "A number in the wrong box trips up everyone once. Normal. Now we ask first, yes?"
    ),
    names=["lantern_count", "lantern_price", "rope_count", "rope_price"],
    pair_talk=(
        "Pair talk: read the rope story out loud to your partner. Which number answers how many? Which answers "
        "how much is one? Then each of you fills in your own boxes."
    ),
    starter=(
        LANTERN_STORY + ROPE_STORY +
        "lantern_count = 0  # how many?\n"
        "lantern_price = 0  # how much is one?\n"
        "rope_count = 0  # how many?\n"
        "rope_price = 0  # how much is one?\n"
    ),
    checkpoints=[
        dict(
            id="lantern-boxes",
            text="Mar'tu needs 3 lanterns that cost 4 coins each. Fill in the two lantern boxes from this story.",
            dictated=True,
            hints=[
                "Start with how many lanterns: change the 0 after `lantern_count = `.",
                "Ask each number: how many? or how much is one?",
                "In '2 maps at 6 coins', 2 is how many and 6 is the price of one. "
                "A 0 in the starter is a [[placeholder]]: replace it.",
            ],
            checks=[
                story_pair(
                    "the lantern boxes match the story", "lantern_count", "lantern_price", 3, 4, "lanterns",
                    known=["lantern_count", "lantern_price", "rope_count", "rope_price"],
                    wild="Lucky would like 1000 lanterns. The story says 3. Use the story's numbers here: "
                    "you get your 1000 in the next exercise.",
                ),
            ],
            pass_line="Mar'tu: 3 lanterns, 4 coins for one. Each number in its own box.",
        ),
        dict(
            id="rope-boxes",
            text="Fill in the two rope boxes. This story gives the price first.",
            dictated=False,
            hints=[
                "Find how many coils Mar'tu needs. That number goes after `rope_count = `.",
                "Read the rope story slowly. Which number has 'a coil' after it?",
                "'Candles cost 1 coin each, and I need 3': the price comes first, but 3 is still how many. "
                "Ask the question, not the order.",
            ],
            checks=[
                story_pair(
                    "the rope boxes match the story", "rope_count", "rope_price", 5, 2, "coils",
                    known=["lantern_count", "lantern_price", "rope_count", "rope_price"],
                    wild="Lucky would like 1000 coils of rope. The story says 5. Use the story's numbers here: "
                    "you get your 1000 in the next exercise.",
                    price_first=True,
                ),
            ],
            pass_line="Mar'tu: Price first, count second, and you still put them right. Good.",
        ),
    ],
    solution=(
        LANTERN_STORY + ROPE_STORY +
        "lantern_count = 3  # how many?\n"
        "lantern_price = 4  # how much is one?\n"
        "rope_count = 5  # how many?\n"
        "rope_price = 2  # how much is one?\n"
    ),
    partials=[
        LANTERN_STORY + ROPE_STORY +
        "lantern_count = 3  # how many?\n"
        "lantern_price = 4  # how much is one?\n"
        "rope_count = 0  # how many?\n"
        "rope_price = 0  # how much is one?\n"
    ],
    assemble=dict(
        lines=["lantern_count = 3", "lantern_price = 4", "rope_count = 5", "rope_price = 2"],
        distractors=["lantern_count = 4", "rope_count = 2", "lantern_price = 12"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Tally marks and a price tag",
            text=(
                "How many is a row of tally marks. How much is one is a price tag.\n"
                "```text\nlanterns:  ||| (3)     price tag: [4 coins]\nrope:      ||||| (5)   price tag: [2 coins]\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A shopping list",
            text=(
                "A shopping list says '3 lanterns'. The shop's sign says '4 coins each'. "
                "The list is how many. The sign is how much one costs. They never swap jobs."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Find a number in the story.\n2. Ask: is it how many, or how much is one?\n"
                "3. Put it in the box whose note asks that question.\n4. Do the next number."
            ),
        ),
        dict(
            angle="in Tor",
            label="My jar shelf",
            text="How many jars? How much for one jar? Two questions, two boxes. Ask before you write, yes?",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky has his own shopping in mind. Write your own small shopping story in a `#` note, "
            "then make two new boxes for it: how many, and how much is one."
        ),
        hints=[
            "A note starts with `#`, like `# Lucky needs 2 canteens that cost 7 coins each.`",
            "Then two boxes with new names, like `canteen_count = 2` and `canteen_price = 7`.",
        ],
        checks=[
            (
                "a story note of your own",
                "import io as _io, tokenize as _tk\n"
                "_notes = [_t.string.strip() for _t in _tk.generate_tokens(_io.StringIO(_source).readline) if _t.type == _tk.COMMENT]\n"
                "_starter = ['# how many?', '# how much is one?', \"# Mar'tu needs 3 lanterns that cost 4 coins each.\", "
                "\"# Rope costs 2 coins a coil, and Mar'tu needs 5 coils.\"]\n"
                "assert [_n for _n in _notes if _n not in _starter and len(_n) > 3], "
                "'Write your shopping story in a note of your own: a line that starts with `#`.'",
            ),
            (
                "two new number boxes",
                "import ast as _ast\n"
                "_old = ['lantern_count', 'lantern_price', 'rope_count', 'rope_price']\n"
                "_new = [_t.id for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' for _t in _n.targets "
                "if type(_t).__name__ == 'Name' and _t.id not in _old and type(globals().get(_t.id)).__name__ == 'int']\n"
                "assert len(set(_new)) >= 2, 'Make two new boxes with numbers for your story: how many, and how much is one.'",
            ),
        ],
        solution=(
            LANTERN_STORY + ROPE_STORY +
            "lantern_count = 3\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n"
            "# Lucky needs 2 canteens that cost 7 coins each.\ncanteen_count = 2\ncanteen_price = 7\n"
        ),
    ),
    takeaway="Ask every number: how many? or how much is one? Then put it in the box that means that.",
    wrong_answers=[
        dict(why="lantern numbers swapped",
             code="lantern_count = 4\nlantern_price = 3\nrope_count = 0\nrope_price = 0\n",
             fails_at=1, message_contains="swapped"),
        dict(why="rope numbers in reading order (price first)",
             code="lantern_count = 3\nlantern_price = 4\nrope_count = 2\nrope_price = 5\n",
             fails_at=2, message_contains="swapped"),
        dict(why="a wild count (G1's 1000)",
             code="lantern_count = 3\nlantern_price = 4\nrope_count = 1000\nrope_price = 2\n",
             fails_at=2, message_contains="story"),
        dict(why="the line total in the price box",
             code="lantern_count = 3\nlantern_price = 12\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="all 3"),
        dict(why="the line total in the count box (A-05/A-07/A-08 'numbers from my math')",
             code="lantern_count = 12\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="wants how many"),
        dict(why="a number in quotes",
             code='lantern_count = "3"\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n',
             fails_at=1, message_contains="quotes"),
        dict(why="a lone number replaces the box line",
             code="3\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="no box"),
        dict(why="placeholders left in",
             code="lantern_count = 3\nlantern_price = 0\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="placeholder"),
        dict(why="capital letter in a name, placeholder left",
             code="Lantern_count = 3\nlantern_count = 0\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="side work in a new box (B-02/B-03 Pizza=4 before the template), placeholder left",
             code="lanterns = 3\nlantern_count = 0\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="new box `lanterns`"),
        dict(why="a price in quotes (rope)",
             code='lantern_count = 3\nlantern_price = 4\nrope_count = 5\nrope_price = "2"\n',
             fails_at=2, message_contains="quotes"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="combine-values", solo="false", dictates="1",
             foreign_names="maps,candles") + "\n"
        "C9: the second story gives the price first. The starter boxes are count-first. G3 teach line: a 0 is a "
        "placeholder. WA evidence: A-05/A-07/A-08 pizzas = 12 (prices in count slots), A-03/A-04 180 and 1000."
    ),
)

COST_KNOWN = ["lantern_count", "lantern_price", "rope_count", "rope_price", "lantern_cost", "rope_cost", "total_cost"]
COST_FOREIGN = ["map_count", "map_price", "map_cost", "a", "b", "c"]
COST_BOXES = "lantern_count = 3\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n"
COST_BOXES_1000 = "lantern_count = 3\nlantern_price = 4\nrope_count = 1000\nrope_price = 2\n"
COMBINE_FIX = "Build it from the boxes, so the code does the math."
COST_INPUTS = ["lantern_count", "lantern_price", "rope_count", "rope_price"]

LET_THE_CODE_COMBINE = dict(
    id="let-the-code-combine",
    title="Let the code combine it",
    martu=(
        "Do not work the total out yourself. Let Python combine the boxes. "
        "Then the total stays right when a number changes.\n"
        "Some call this [[show your working|showing your working]]. Watch the Example."
    ),
    example=(
        "# Oogrish buys 2 maps at 6 coins.\n"
        "map_count = 2\n"
        "map_price = 6\n"
        "map_cost = map_count * map_price\n"
        "print(map_cost)\n"
    ),
    example_output="12",
    names=["lantern_cost", "rope_cost", "total_cost", "lantern_count", "lantern_price", "rope_count", "rope_price"],
    pair_talk=(
        "Pair talk: each of you gives one reason why typing 22 is a trap. Hint: what happens when Lucky changes "
        "`rope_count`? Then each of you finishes on your own screen."
    ),
    starter=(
        COST_BOXES +
        "lantern_cost = 0\n"
        "rope_cost = 0\n"
        "total_cost = 0\n"
        "print(total_cost)\n"
    ),
    checkpoints=[
        dict(
            id="lantern-cost",
            text="Replace the `0` in `lantern_cost` so Python multiplies the two lantern boxes.",
            dictated=True,
            hints=[
                "Start like this: `lantern_cost = lantern_count * `",
                "Look at the Example: `map_cost = map_count * map_price`. Which two lantern boxes match those?",
                "`*` multiplies. If `a = 2` and `b = 6`, then `c = a * b` puts 12 in `c`.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                set_once("each box is set once, at the top", COST_INPUTS[:2]),
                slot(
                    "lantern_cost multiplies the lantern boxes", "lantern_cost", "lantern_count * lantern_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[
                        ("_have == lantern_count + lantern_price",
                         "That adds the two boxes. A cost is how many times the price of one: use `*`."),
                        # LINE-TOTAL: `lantern_count * 12` multiplies by the line total again.
                        ("_have in (lantern_count * lantern_count * lantern_price, "
                         "lantern_price * lantern_count * lantern_price)",
                         "12 is already the cost of all 3 lanterns, so multiplying by it again gives too much. "
                         "Multiply how many by the price of one: `lantern_count * lantern_price`."),
                    ],
                    default="Make `lantern_cost` from the two lantern boxes: how many `*` the price of one.",
                ),
                rerun_box(
                    "lantern_cost follows its boxes", {"lantern_count": 7, "lantern_price": 5}, "lantern_cost",
                    "_R('lantern_count') * _R('lantern_price')", COMBINE_FIX,
                ),
            ],
        ),
        dict(
            id="rope-cost",
            text="Do the same for `rope_cost`.",
            dictated=False,
            hints=[
                "Start like this: `rope_cost = rope_count * `",
                "Your `lantern_cost` line is the pattern. Which boxes are about rope?",
                "If `a = 2` and `b = 6`, then `c = a * b` puts 12 in `c`. Same shape, rope boxes.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                set_once("each box is set once, at the top", COST_INPUTS[2:]),
                slot(
                    "rope_cost multiplies the rope boxes", "rope_cost", "rope_count * rope_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[
                        ("_have == rope_count + rope_price",
                         "That adds the two boxes. A cost is how many times the price of one: use `*`."),
                        # LINE-TOTAL: `rope_count * 10` multiplies by the line total again.
                        ("_have in (rope_count * rope_count * rope_price, rope_price * rope_count * rope_price)",
                         "10 is already the cost of all 5 coils, so multiplying by it again gives too much. "
                         "Multiply how many by the price of one: `rope_count * rope_price`."),
                    ],
                    default="Make `rope_cost` from the two rope boxes, the same way as `lantern_cost`.",
                ),
                rerun_box(
                    "rope_cost follows its boxes", {"rope_count": 6, "rope_price": 3}, "rope_cost",
                    "_R('rope_count') * _R('rope_price')", COMBINE_FIX,
                ),
            ],
        ),
        dict(
            id="total-cost",
            text="Make `total_cost` the sum of the two costs.",
            dictated=False,
            hints=[
                "Start like this: `total_cost = lantern_cost + `",
                "Look at `total_cost = 0`. Which two costs make the total?",
                "Python can add boxes. If `a = 2` and `b = 5`, then `c = a + b` puts 7 in `c`, "
                "and it stays right when `a` changes.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                set_once("each box is set once, at the top", COST_INPUTS),
                slot(
                    "total_cost adds the two costs", "total_cost",
                    "lantern_count * lantern_price + rope_count * rope_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[("_have == lantern_count + rope_count",
                            "You added how many, not costs. Add the two cost boxes: `lantern_cost + rope_cost`.")],
                    default="Make `total_cost` from the two cost boxes, added together.",
                ),
                rerun_box(
                    "total_cost follows the lantern boxes", {"lantern_count": 7}, "total_cost",
                    "_R('lantern_count') * _R('lantern_price') + _R('rope_count') * _R('rope_price')", COMBINE_FIX,
                ),
                rerun_box(
                    "total_cost follows every box", {"lantern_price": 5, "rope_count": 6, "rope_price": 3}, "total_cost",
                    "_R('lantern_count') * _R('lantern_price') + _R('rope_count') * _R('rope_price')", COMBINE_FIX,
                ),
            ],
            pass_line="Mar'tu: 22 coins, and you never did the sum. Good. Now watch this.",
        ),
        dict(
            id="a-thousand-ropes",
            text="Now change `rope_count` to 1000 and run. Watch `total_cost` follow.",
            dictated=True,
            hints=[
                "Change line 3 to `rope_count = 1000`.",
                "Which line says how many coils? Change only that one.",
                "Change a box at the top, and every line built from it follows. That is why we let the code combine.",
            ],
            checks=[
                ("rope_count is 1000", "assert rope_count == 1000, 'Change line 3 to `rope_count = 1000`, then run.'"),
                (
                    "the total is printed",
                    "assert str(total_cost) in _lines(), 'Keep `print(total_cost)` at the bottom, so you can watch it follow.'",
                ),
            ],
            pass_line="Mar'tu: 2012 coins. You did not do that sum, yes? The code did. Lucky, put the rope down.",
        ),
    ],
    solution=(
        COST_BOXES_1000 +
        "lantern_cost = lantern_count * lantern_price\n"
        "rope_cost = rope_count * rope_price\n"
        "total_cost = lantern_cost + rope_cost\n"
        "print(total_cost)\n"
    ),
    partials=[
        COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = 0\ntotal_cost = 0\nprint(total_cost)\n",
        COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
        "total_cost = 0\nprint(total_cost)\n",
        COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
        "total_cost = lantern_cost + rope_cost\nprint(total_cost)\n",
    ],
    assemble=dict(
        lines=[
            "lantern_count = 3", "lantern_price = 4", "rope_count = 1000", "rope_price = 2",
            "lantern_cost = lantern_count * lantern_price", "rope_cost = rope_count * rope_price",
            "total_cost = lantern_cost + rope_cost", "print(total_cost)",
        ],
        distractors=["total_cost = 22", "lantern_cost = 12", "total_cost = lantern_count + rope_count"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Arrows into the total",
            text=(
                "```text\nlantern_count --\\\n                 *--> lantern_cost --\\\nlantern_price --/                     \\\n"
                "                                       +--> total_cost\nrope_count -----\\                     /\n"
                "                 *--> rope_cost ----/\nrope_price -----/\n```\n"
                "Change any box on the left, and the arrows carry it all the way to the total."
            ),
        ),
        dict(
            angle="everyday",
            label="An online cart",
            text=(
                "In an online cart, change the quantity from 3 to 7 and the total updates by itself. "
                "That only works because the cart multiplies and adds. It never stores the total as a typed number."
            ),
        ),
        dict(
            angle="show your working",
            label="Show your working",
            text=(
                "In math class, a teacher wants the working, not just the answer. Python is the same. "
                "`total_cost = 22` is just the answer. `total_cost = lantern_cost + rope_cost` is the working, "
                "and Python checks it every time it runs."
            ),
        ),
        dict(angle="shorter", text="Cost = how many `*` price of one. Total = cost `+` cost. Never type the answer."),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The mana bar needed the mana used: `caster[\"max_mana\"] - caster[\"mana\"]`. "
                "No one typed the answer there either. The code worked it out for every caster, from their boxes."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Mar'tu has 30 coins. Make `coins = 30`, then print how many coins are left after the shopping, "
            "built from the boxes. With 1000 ropes, expect bad news."
        ),
        hints=[
            "Start like this: `coins = 30`, then `print(coins - `",
            "What is left is the coins take away the total cost.",
        ],
        checks=[
            ("coins is 30", "assert coins == 30, 'Make `coins = 30`.'"),
            (
                "prints what is left",
                "assert str(coins - total_cost) in _lines(), 'Print what is left: `coins - total_cost`.'",
            ),
            rerun_line(
                "what is left follows the boxes", {"lantern_count": 7},
                "str(_R('coins') - _R('lantern_count') * _R('lantern_price') - _R('rope_count') * _R('rope_price'))",
                "Use `coins - total_cost`, so it follows the boxes.",
            ),
        ],
        solution=(
            COST_BOXES_1000 +
            "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
            "total_cost = lantern_cost + rope_cost\nprint(total_cost)\ncoins = 30\nprint(coins - total_cost)\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='empty = "░" * (caster["max_mana"] - caster["mana"])',
        why=(
            "You have seen this line. Nobody typed how much mana was used. The code took it from the caster's "
            "boxes, so the bar was right for Oogrish, Gearshift, Bomb Shell and Lucky. Same idea as your total."
        ),
    ),
    takeaway="Let the code combine it: `total_cost = lantern_cost + rope_cost`. Then it follows when a box changes.",
    wrong_answers=[
        dict(why="the total typed by hand (everyone's 68)",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = 22\nprint(total_cost)\n",
             fails_at=3, message_contains="38"),
        dict(why="the line totals typed as numbers",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = 12 + 10\nprint(total_cost)\n",
             fails_at=3, message_contains="38"),
        dict(why="a new box for the total (NEWBOX)",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = 0\nmy_total = lantern_cost + rope_cost\nprint(my_total)\n",
             fails_at=3, message_contains="still holds 0"),
        dict(why="algebra shorthand (A-02 5P + 2S)",
             code=COST_BOXES + "lantern_cost = 0\nrope_cost = 0\ntotal_cost = 3L + 5R\nprint(total_cost)\n",
             fails_at=0, message_contains="decimal"),
        dict(why="adds the counts, not the costs",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_count + rope_count\nprint(total_cost)\n",
             fails_at=3, message_contains="how many"),
        dict(why="one price typed in (half combined)",
             code=COST_BOXES + "lantern_cost = lantern_count * 4\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_cost + rope_cost\nprint(total_cost)\n",
             fails_at=1, message_contains="lantern_price"),
        dict(why="the example's name copied (A-08 total_frait)",
             code=COST_BOXES + "lantern_cost = 0\nmap_cost = lantern_count * lantern_price\nrope_cost = 0\n"
             "total_cost = 0\nprint(total_cost)\n",
             fails_at=1, message_contains="example"),
        dict(why="capital letter in the name",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = 0\nTotal_cost = lantern_cost + rope_cost\nprint(Total_cost)\n",
             fails_at=3, message_contains="letter for letter"),
        dict(why="def used to make a box (A-02)",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "def total_cost = lantern_cost + rope_cost\nprint(total_cost)\n",
             fails_at=0, message_contains="SyntaxError"),
        dict(why="half the rope cost typed (passes the count rerun, caught by the price rerun)",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_cost + 10\nprint(total_cost)\n",
             fails_at=3, message_contains="rope_price"),
        dict(why="rope count typed inside the total (passes a lantern-only and a price-only rerun)",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_cost + 5 * rope_price\nprint(total_cost)\n",
             fails_at=3, message_contains="rope_count = 6"),
        dict(why="lantern price typed inside the total, cost boxes skipped",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_count * 4 + rope_cost\nprint(total_cost)\n",
             fails_at=3, message_contains="lantern_price = 5"),
        dict(why="the math in quotes",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             'total_cost = "lantern_cost + rope_cost"\nprint(total_cost)\n',
             fails_at=3, message_contains="quotes"),
        dict(why="the math worked out on a line of its own, kept in no box (B-02/B-03 lone value)",
             code=COST_BOXES + "lantern_cost = 0\nlantern_count * lantern_price\nrope_cost = 0\ntotal_cost = 0\nprint(total_cost)\n",
             fails_at=1, message_contains="keeps it nowhere"),
        dict(why="adds the rope boxes instead of multiplying",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count + rope_price\n"
             "total_cost = 0\nprint(total_cost)\n",
             fails_at=2, message_contains="use `*`"),
        dict(why="LINE-TOTAL: the lantern count times the line total 12",
             code=COST_BOXES + "lantern_cost = lantern_count * 12\nrope_cost = 0\ntotal_cost = 0\nprint(total_cost)\n",
             fails_at=1, message_contains="already the cost"),
        dict(why="LINE-TOTAL: the rope count times the line total 10",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * 10\n"
             "total_cost = 0\nprint(total_cost)\n",
             fails_at=2, message_contains="already the cost"),
        dict(why="CP4 done as a new line at the bottom (side-work habit): the total never sees 1000",
             code=COST_BOXES + "lantern_cost = lantern_count * lantern_price\nrope_cost = rope_count * rope_price\n"
             "total_cost = lantern_cost + rope_cost\nprint(total_cost)\nrope_count = 1000\n",
             fails_at=2, message_contains="top down"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="combine-values", solo="false", dictates="1,4",
             foreign_names="map_count,map_price,map_cost,a,b,c",
             twin="Candles cost 1 coin each and Mar'tu needs 3; maps cost 6 and he needs 2. Make candle_cost, "
             "map_cost and supply_total (price-first, C9)") + "\n"
        "The Investigate (rope_count = 1000, total 2012) is checkpoint 4 so everyone does it; checks 1-3 compare "
        "against the student's own boxes, so they stay green at 1000. CMB uses two reruns on CP3 (lantern_count 7 -> "
        "38; lantern_price 5, rope_count 6, rope_price 3 -> 33): every input changes in some rerun, so a total with "
        "any one number typed in fails. set_once: `rope_count = 1000` added at the bottom (instead of changing line 3) "
        "gets a top-down message, not a confusing slot message. LINE-TOTAL (`lantern_count * 12`, `rope_count * 10`) "
        "gets its own message instead of the placeholder default. PR (each partner gives one reason why typing 22 is "
        "a trap) is the pair_talk prompt. Point-at-it: 'Which part of your line is the price of one?' after CP1 (site feature)."
    ),
)

SPEND_STARTER = "mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nprint(mana)\n"
SPEND_SOLUTION = (
    "mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nmana = mana - spell_cost\n"
    "print(mana)\n"
)

SPEND_MANA = dict(
    id="spend-mana",
    title="Spend some mana",
    martu=(
        "`mana = mana - spell_cost` means: take what is in `mana` now, subtract the cost, "
        "and put the answer back in `mana`.\n"
        "Read `=` as gets: mana gets mana minus spell cost."
    ),
    names=["mana", "spell_cost"],
    tracer=True,
    predict=dict(
        q="What will this print?",
        choices=["20", "23", "26", "29"],
        answer=0,
        explain=(
            "Each cast takes 3 from what is in the box at that moment:\n"
            "```text\nline  code                      mana holds\n1     mana = 26                 26\n"
            "2     spell_cost = 3            26\n3     mana = mana - spell_cost  23\n"
            "4     mana = mana - spell_cost  20\n5     print(mana)               20, so 20 prints\n```"
        ),
    ),
    pair_talk=(
        "Pair talk: each of you picks an answer without showing. Reveal together. Then both of you read line 4 "
        "out loud, saying \"gets\" for `=`."
    ),
    starter=SPEND_STARTER,
    checkpoints=[
        dict(
            id="three-casts",
            text="Make it three casts.",
            dictated=True,
            hints=[
                "Click at the end of line 4, press Enter, and type `mana = `.",
                "Which line spends mana? You need one more of it, above the `print`.",
                "Python works out the right side first, using what is in the box now. If `glow = 8`, then "
                "`glow = glow - 2` puts 6 back in `glow`.",
            ],
            checks=[
                near_names("the names are exact", ["mana", "spell_cost"], ["mana", "spell_cost"]),
                no_bare_math("the answer goes back in the box", "mana"),
                (
                    "three casts print 17",
                    "assert '-17' not in _lines(), 'Your new line takes `mana` away from `spell_cost`, so it gives -17. "
                    "Put `mana` first: `mana = mana - spell_cost`.'\n"
                    "assert '17' in _lines() or mana != 17, '`mana` holds 17, but it was printed too early. "
                    "Put `print(mana)` below the third cast.'\n"
                    "assert '17' in _lines() or mana != 20, '`mana` is 20, which is two casts. "
                    "Add one more `mana = mana - spell_cost` line above the `print`.'\n"
                    "assert '17' in _lines() or mana != 14, '`mana` is 14, which is four casts. "
                    "Keep three `mana = mana - spell_cost` lines, then the `print`.'\n"
                    "assert '17' in _lines(), 'Three casts of 3 from 26 leave 17. "
                    "Add a third `mana = mana - spell_cost` line above the `print`.'",
                ),
                rerun_line(
                    "the casts use spell_cost", {"spell_cost": 5}, "str(26 - 3 * _R('spell_cost'))",
                    "Spend `spell_cost` in each cast, not a number.",
                ),
                (
                    "each cast changes the box",
                    "import ast as _ast\n"
                    "_casts = [_n for _n in _ast.parse(_source).body if (type(_n).__name__ == 'Assign' "
                    "and any(getattr(_t, 'id', '') == 'mana' for _t in _n.targets) and type(_n.value).__name__ == 'BinOp' "
                    "and type(_n.value.op).__name__ == 'Sub') or (type(_n).__name__ == 'AugAssign' "
                    "and getattr(_n.target, 'id', '') == 'mana' and type(_n.op).__name__ == 'Sub')]\n"
                    "assert len(_casts) >= 3, 'Your program prints 17, but `mana` only changed ' + str(len(_casts)) + "
                    "' times. Give the third cast its own line, `mana = mana - spell_cost`, so the box keeps the answer.'",
                ),
            ],
            pass_line=(
                "Mar'tu: 26, 23, 20, 17. The box keeps only the newest value, yes? Halfway through tonight's math. "
                "A good place to rest if you need one: your work is saved."
            ),
        ),
    ],
    solution=SPEND_SOLUTION,
    assemble=dict(
        lines=["mana = 26", "spell_cost = 3", "mana = mana - spell_cost", "mana = mana - spell_cost",
               "mana = mana - spell_cost", "print(mana)"],
        distractors=["mana - spell_cost", "mana = 17"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Coins out of a jar",
            text=(
                "```text\n[ mana: 26 ]  -> take out 3 ->  23  -> put it back ->  [ mana: 23 ]\n```\n"
                "Each cast: open the jar, take out the cost, put what is left back in the same jar."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "```text\nline  code                      mana holds\n1     mana = 26                 26\n"
                "3     mana = mana - spell_cost  23\n4     mana = mana - spell_cost  20\n"
                "5     mana = mana - spell_cost  17\n6     print(mana)               17\n```"
            ),
        ),
        dict(
            angle="read aloud",
            label="Say it out loud",
            text="Say `mana = mana - spell_cost` as: mana gets mana minus spell cost. The right side happens first.",
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In `cast_spell`, the line `caster[\"mana\"] = caster[\"mana\"] - spell[\"mana_cost\"]` held the barrier. "
                "Same shape: take what is there now, subtract the cost, put it back."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "After the third cast, Lucky shares his glug: +2 mana. Below the `print`, add 2 to `mana` the same way, "
            "then print `mana` again."
        ),
        hints=[
            "Start like this: `mana = mana + `",
            "Then another `print(mana)` under it.",
        ],
        checks=[
            ("prints 19 after the glug", "assert '19' in _lines(), 'After the glug, `mana` should be 19. Add 2 the same way, then print it.'"),
            rerun_line(
                "the glug line uses the box", {"spell_cost": 5}, "str(26 - 3 * _R('spell_cost') + 2)",
                "Add 2 to what is in `mana` now: `mana = mana + 2`.",
            ),
        ],
        solution=SPEND_SOLUTION + "mana = mana + 2\nprint(mana)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "You have seen this line in `cast_spell`. It is `mana = mana - spell_cost` with longer labels: "
            "take the caster's mana now, subtract the spell's cost, put the answer back."
        ),
    ),
    takeaway="`mana = mana - spell_cost`: the right side first, with what is in the box now; the answer goes back in.",
    wrong_answers=[
        dict(why="the final mana typed by hand", code="mana = 26\nspell_cost = 3\nmana = 17\nprint(mana)\n",
             fails_at=1, message_contains="5"),
        dict(why="subtracts but never stores it",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nmana - spell_cost\nprint(mana)\n",
             fails_at=1, message_contains="didn't change"),
        dict(why="a number instead of spell_cost",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nmana = mana - 3\nprint(mana)\n",
             fails_at=1, message_contains="spell_cost"),
        dict(why="third cast below the print",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nprint(mana)\nmana = mana - spell_cost\n",
             fails_at=1, message_contains="too early"),
        dict(why="the starter left as two casts", code=SPEND_STARTER, fails_at=1, message_contains="two casts"),
        dict(why="gaming the message: typed 17 plus the 11 the rerun message showed",
             code="mana = 26\nspell_cost = 3\nprint(17)\nprint(11)\n", fails_at=1, message_contains="typed in"),
        dict(why="capital letter: a new box Mana (prints 17, but mana is still 20)",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nMana = mana - spell_cost\nprint(Mana)\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="one cast too many", code=SPEND_SOLUTION.replace("print(mana)", "mana = mana - spell_cost\nprint(mana)"),
             fails_at=1, message_contains="four casts"),
        dict(why="the third cast worked out inside the print, never stored (mana stays 20)",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nprint(mana - spell_cost)\n",
             fails_at=1, message_contains="only changed 2 times"),
        dict(why="subtracts the wrong way round on the new line",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nmana = spell_cost - mana\nprint(mana)\n",
             fails_at=1, message_contains="Put `mana` first"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="reassign", solo="false", dictates="1",
             foreign_names="glow") + "\n"
        "The step table is the predict explanation (shown after any guess) and the step-by-step angle (TR). "
        "Checks read the printed 17 (not the final value) so Lucky's +2 side quest does not undo the checkpoint. "
        "WA evidence: tracing by adding the printed constants (A-03/A-04), typed answers (everyone's 68)."
    ),
)

# OUT for 1C-06. Lucky (the starter's name) gets the full diff; another name a student picked is accepted, and
# its diff never repeats the name back (privacy, 2.11).
def named_out(label, tail, missing_lucky, missing_own, spaces):
    """OUT for a line that starts with `name`: Lucky gets the full diff; any other name is accepted and its diff
    never repeats the student's name back."""
    full = out_line("", "'Lucky' + " + tail, missing_lucky)[1]
    own = out_line("", "str(name) + " + tail, missing_own, privacy=True, spaces=spaces)[1]
    return (
        label,
        "if name == 'Lucky':\n" + "".join("    " + _l + "\n" for _l in full.splitlines())
        + "else:\n" + "".join("    " + _l + "\n" for _l in own.splitlines()),
    )


GLUE_OUT = named_out(
    "prints Lucky has 26 mana.", "' has ' + str(mana) + ' mana.'",
    "Print `Lucky has 26 mana.`, glued from `name`, fixed words and `str(mana)`.",
    "Print the line glued from `name`, fixed words and `str(mana)`, like `Tester has 4 mana.`",
    "Check the spaces: one after the name, and one on each side of the number.",
)

# Both glue-words checkpoints: a box name in quotes is just letters (the finished line is always accepted).
GLUE_NO_QUOTED_NAMES = (
    "box names are not in quotes",
    "import ast as _ast\n"
    "_q = [_n.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Constant' "
    "and type(_n.value).__name__ == 'str' and _n.value.strip() in ('mana', 'name')]\n"
    "_right = str(name) + ' has ' + str(mana) + ' mana.' in _lines()\n"
    "assert _right or not _q, '`\"' + (_q[0].strip() if _q else '') + '\"` in quotes is just those letters. "
    + QUOTES_RULE + "'",
)

# CP1 of glue-words: some printed line starts with the name and ` has` (the finished line does too). The message
# never repeats a student's own name: it shows the Tester example instead (privacy, 2.11).
GLUE_FIRST_BEAD = (
    "prints the name, then has",
    "_first = str(name) + ' has'\n"
    "_ls = _lines()\n"
    "_msg = ''\n"
    "if not any(_l.startswith(_first) for _l in _ls):\n"
    "    if not _ls:\n"
    "        _msg = 'Nothing is printed yet. Type `print(name + \" has \")` and run.'\n"
    "    elif any(_l.startswith(str(name) + 'has') for _l in _ls):\n"
    "        _msg = 'A space is missing between the name and `has`. Spaces are text too: put them inside the quotes, `\" has \"`.'\n"
    "    else:\n"
    "        _msg = 'Print the name from the box, then ` has`. For a hero named Tester, that is `Tester has`. "
    "Type `print(name + \" has \")`.'\n"
    "assert not _msg, _msg\n",
)

GLUE_WORDS = dict(
    id="glue-words",
    title="Glue words together",
    martu=(
        "`+` [[glue|glues]] text to text. A number must become text first: `str(26)` gives `\"26\"`. "
        "Spaces are text too.\n"
        "`\"Mana: \" + 26` makes Python stop: it will not glue text to a number. `\"Mana: \" + str(26)` works."
    ),
    introduces=["call:str"],
    example='drink = "glug"\nsips = 5\nprint("Lucky drinks " + drink + ".")\nprint("Sips left: " + str(sips))\n',
    example_output="Lucky drinks glug.\nSips left: 5",
    names=["name", "mana", "str"],
    predict=dict(
        q="What will this print?",
        code='print("Lucky" + "is" + "ready.")\n',
        choices=["Lucky is ready.", "Luckyisready.", "Lucky + is + ready."],
        answer=1,
        explain=(
            "`+` glues the texts exactly as they are. It adds no spaces. "
            "Spaces are text too, so put them inside the quotes: `\"Lucky\" + \" is \" + \"ready.\"`."
        ),
    ),
    starter='name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\n',
    checkpoints=[
        dict(
            id="lucky-has",
            text="Start small: print `Lucky has`, built from `name` and the words `\" has \"`. Run it.",
            dictated=True,
            hints=[
                "Type `print(name + \" has \")` and run.",
                "`name` has no quotes: it is a box. ` has ` is fixed words, so it goes in quotes, spaces and all.",
                "`\"Hi \" + pet` glues fixed words to the text in the box `pet`.",
            ],
            checks=[
                GLUE_NO_QUOTED_NAMES,
                GLUE_FIRST_BEAD,
                rerun_line(
                    "the name comes from the box", {"name": "Tester"}, "'Tester has'",
                    "Glue the box `name`, not typed letters: `print(name + \" has \")`.", hide=own("name"), starts=True,
                ),
            ],
            pass_line="Mar'tu: Two beads on the string. Now the number.",
        ),
        dict(
            id="lucky-has-mana",
            text="Now add the number and the end, `+ str(mana) + \" mana.\"`, so it prints `Lucky has 26 mana.`",
            dictated=True,
            hints=[
                "Click just before the last `)` and type `+ str(mana) + \" mana.\"`",
                "`mana` holds a number. What does a number need before it can be glued?",
                "The frame: `print(name + \" has \" + ___ + \" mana.\")`. The blank turns the number into text.",
            ],
            checks=[
                GLUE_NO_QUOTED_NAMES,
                (
                    "mana holds a number",
                    "assert type(mana).__name__ == 'int', '`mana` holds text, because of the quotes. Numbers don' + "
                    "chr(39) + 't need quotes: keep `mana = 26`, and turn it into text in the line with `str(mana)`.'",
                ),
                GLUE_OUT,
                rerun_line(
                    "the line is built from the boxes", {"name": "Tester", "mana": 4},
                    "_R('name') + ' has ' + str(_R('mana')) + ' mana.'",
                    "Build the line from `name` and `str(mana)`, so it follows the boxes.", hide=own("name"),
                ),
                rerun_line(
                    "the line follows other boxes too", {"name": "Zelda", "mana": 7},
                    "_R('name') + ' has ' + str(_R('mana')) + ' mana.'",
                    "Build the line from `name` and `str(mana)`, so it follows the boxes.", hide=own("name"),
                ),
                (
                    "glued with + and str()",
                    "assert _uses('op:Add') and _uses('call:str'), 'Your line prints the right words. This step "
                    "practises glue: join the pieces with `+`, and turn the number into text with `str(mana)`.'",
                ),
            ],
            pass_line="Lucky: Twenty-six. Fine. But I'm keeping track.",
        ),
    ],
    solution='name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\nprint(name + " has " + str(mana) + " mana.")\n',
    partials=['name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\nprint(name + " has ")\n'],
    assemble=dict(
        lines=['name = "Lucky"', "mana = 26", 'print(name + " has " + str(mana) + " mana.")'],
        distractors=['print(name + " has " + mana + " mana.")', 'print("Lucky has 26 mana.")',
                     'print(name + "has" + str(mana) + "mana.")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Beads on a string",
            text=(
                "Each piece is a bead. Only text beads go on the string. A number needs `str()` to become a bead.\n"
                "```text\n[Lucky] + [ has ] + [26] + [ mana.]\n name     text    str(mana)  text\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Gluing labels",
            text=(
                "Glue three paper labels in a row. Nothing adds the gaps for you: if you want a gap, it must be "
                "printed on a label. In Python, the gap is a space inside the quotes."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Build it piece by piece",
            text=(
                "1. `print(name)`, run.\n2. `print(name + \" has \")`, run.\n"
                "3. `print(name + \" has \" + str(mana))`, run.\n4. Add `+ \" mana.\"`, run. Check every space."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "The mana bar ended with `\"] \" + str(caster[\"mana\"]) + \"/\" + str(caster[\"max_mana\"])`. "
                "Text glued to text, and `str()` on every number. Now you can read every piece of it."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants it to look bigger. Make a box `max_mana = 26`, then on a new line print "
            "`Lucky has 26 of 26 mana.`, built from the boxes."
        ),
        hints=[
            "Start like this: `max_mana = 26`",
            "Copy your `print` line and add `+ \" of \" + str(max_mana)` in the right place.",
        ],
        checks=[
            ("max_mana is 26", "assert max_mana == 26, 'Make a box `max_mana = 26`.'"),
            named_out("prints the of-line", "' has ' + str(mana) + ' of ' + str(max_mana) + ' mana.'",
                      "Print `Lucky has 26 of 26 mana.` on a new line.",
                      "Print the of-line on a new line, like `Tester has 4 of 30 mana.`",
                      "Check the spaces: one on each side of `has` and `of`, and one before `mana.`"),
            rerun_line(
                "the of-line is built from the boxes", {"name": "Tester", "mana": 4, "max_mana": 30},
                "_R('name') + ' has ' + str(_R('mana')) + ' of ' + str(_R('max_mana')) + ' mana.'",
                "Build it from `name`, `str(mana)` and `str(max_mana)`.", hide=own("name"),
            ),
        ],
        solution=(
            'name = "Lucky"\nmana = 26\nprint(name + " has " + str(mana) + " mana.")\nmax_mana = 26\n'
            'print(name + " has " + str(mana) + " of " + str(max_mana) + " mana.")\n'
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])',
        why=(
            "You have seen this line, and it probably looked like a wall. Now read it as beads: text, text, "
            "text, `str()` of a number, text, `str()` of a number. That is all it ever was."
        ),
    ),
    takeaway="`+` glues text to text. Numbers need `str()` first. Spaces go inside the quotes.",
    wrong_answers=[
        dict(why="the whole line typed", code='name = "Lucky"\nmana = 26\nprint("Lucky has 26 mana.")\n',
             fails_at=1, message_contains="Tester"),
        dict(why="a number glued without str()", code='name = "Lucky"\nmana = 26\nprint(name + " has " + mana + " mana.")\n',
             fails_at=0, message_contains="concatenate"),
        dict(why="spaces missing", code='name = "Lucky"\nmana = 26\nprint(name + "has" + str(mana) + "mana.")\n',
             fails_at=1, message_contains="space"),
        dict(why="the box name in quotes", code='name = "Lucky"\nmana = 26\nprint(name + " has " + "mana" + " mana.")\n',
             fails_at=1, message_contains="exact letters"),
        dict(why="the number typed into str()", code='name = "Lucky"\nmana = 26\nprint(name + " has " + str(26) + " mana.")\n',
             fails_at=2, message_contains="Tester"),
        dict(why="gaming the message: the typed line plus the Tester line the message showed",
             code='name = "Lucky"\nmana = 26\nprint(name + " has " + str(26) + " mana.")\nprint("Tester has " + str(4) + " mana.")\n',
             fails_at=2, message_contains="typed in"),
        dict(why="the number quoted so it glues without str() (NUM)",
             code='name = "Lucky"\nmana = "26"\nprint(name + " has " + mana + " mana.")\n',
             fails_at=2, message_contains="Numbers don't need quotes"),
        dict(why="commas instead of glue: right output, skips + and str()",
             code='name = "Lucky"\nmana = 26\nprint(name, "has", mana, "mana.")\n',
             fails_at=2, message_contains="practises glue"),
        dict(why="a closing quote missing", code='name = "Lucky"\nmana = 26\nprint(name + " has + str(mana) + " mana.")\n',
             fails_at=0, message_contains="SyntaxError"),
        dict(why="gaming: boxes set to the rerun's values, then the line typed",
             code='name = "Tester"\nmana = 4\nprint("Tester has " + str(4) + " mana.")\n', fails_at=2, message_contains="Zelda"),
        dict(why="CP1: the first bead typed, not glued from the box", code='name = "Lucky"\nmana = 26\nprint("Lucky has")\n',
             fails_at=1, message_contains="starts with `Tester has`"),
        dict(why="CP1: no space between the name and has (Lucky has26mana)", code='name = "Lucky"\nmana = 26\nprint(name + "has")\n',
             fails_at=1, message_contains="space is missing"),
        dict(why="CP1: the box name in quotes", code='name = "Lucky"\nmana = 26\nprint("name" + " has ")\n',
             fails_at=1, message_contains="exact letters"),
        dict(why="CP1: gaming the message: the typed bead plus the Tester bead the message showed",
             code='name = "Lucky"\nmana = 26\nprint("Lucky has")\nprint("Tester has")\n', fails_at=1, message_contains="typed in"),
        dict(why="CP1: the student's own hero typed (the message shows Tester, never the hero)",
             code='name = "Kai"\nmana = 26\nprint("Kai has")\n', fails_at=1, message_contains="should print a line that starts with `Tester has`. Glue"),
        dict(why="CP1: the starter run as it is (nothing printed)",
             code='name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\n', fails_at=1,
             message_contains="Nothing is printed yet"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="concat-str", solo="false", dictates="1,2",
             foreign_names="drink,sips,pet") + "\n"
        "Dictated in two steps: CP1 prints the first two beads (`print(name + \" has \")` -> `Lucky has`), CP2 adds "
        "`+ str(mana) + \" mana.\"`. CP1's checks (no quoted box names, a line starting with the name and ` has`, a "
        "starts-with rerun with name Tester) stay true for the finished line, so both pass in one run. "
        "Investigate 1 (`\"Mana: \" + 26`, TypeError + explainer) is told in the Learn pane (no try-it that crashes "
        "on purpose); Investigate 2 (missing space) is the predict. OUT diff shows the first difference; CMB reruns with Tester / 4 and Zelda / 7 (two, so setting the boxes to "
        "the rerun's values and typing the line still fails). Any name a student puts in `name` passes; its diff "
        "never repeats it. The last check asks for `+` and `str()` (commas give the same output but skip the "
        "lesson), with a kind message. "
        "WA evidence: Lucky has26mana (spaces), typed answers (68)."
    ),
)

STATUS_STARTER = (
    'hero_name = "Oogrish"\n'
    "magical_affinity = 9\n"
    "max_mana = 0  # twice the affinity\n"
    "mana = 0  # starts full\n"
    "# Print: Oogrish: 18/18 mana\n"
)
STATUS_KNOWN = ["hero_name", "magical_affinity", "max_mana", "mana"]
STATUS_LINE = 'print(hero_name + ": " + str(mana) + "/" + str(max_mana) + " mana")\n'


def _status(hero, maxline="max_mana = magical_affinity * 2", manaline="mana = max_mana", printed=True):
    return (
        f'hero_name = "{hero}"\nmagical_affinity = 9\n{maxline}  # twice the affinity\n{manaline}  # starts full\n'
        "# Print: Oogrish: 18/18 mana\n" + (STATUS_LINE if printed else "")
    )


STATUS_LINE_EX = dict(
    id="status-line",
    title="A status line",
    martu=(
        "Build Oogrish's status line from boxes. Max mana is twice the magical affinity.\n"
        "You may put any hero in `hero_name`. The boxes do the rest."
    ),
    names=["hero_name", "magical_affinity", "max_mana", "mana", "str"],
    pick='"Oogrish"',
    starter=STATUS_STARTER,
    checkpoints=[
        dict(
            id="max-mana",
            text="Make `max_mana` twice as big as `magical_affinity`.",
            dictated=False,
            hints=[
                "Start like this: `max_mana = magical_affinity * `",
                "Twice means times 2. Which box holds the affinity?",
                "If `power = 7`, then `double = power * 2` puts 14 in `double`, and it follows when `power` changes.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                slot(
                    "max_mana is twice the affinity", "max_mana", "magical_affinity * 2",
                    known=STATUS_KNOWN, foreign=["power", "double"],
                    rules=[
                        ("_have == magical_affinity + 2", "That adds 2. Twice means times 2: use `* 2`."),
                        ("_have == magical_affinity", "That is the affinity once. Twice means times 2."),
                    ],
                    default="Make `max_mana` from the box `magical_affinity`, times 2.",
                ),
                rerun_box("max_mana follows the affinity", {"magical_affinity": 13}, "max_mana",
                          "_R('magical_affinity') * 2", "Build it from `magical_affinity`."),
            ],
        ),
        dict(
            id="mana-full",
            text="Make `mana` start full: `mana = max_mana`.",
            dictated=True,
            hints=[
                "Change line 4 to start with `mana = `.",
                "Full means mana is the same as the max. Which box holds the max?",
                "A box can get what is in another box: `spare = backpack` copies what is in `backpack`.",
            ],
            checks=[
                slot("mana starts full", "mana", "max_mana", known=STATUS_KNOWN, foreign=["spare", "backpack"],
                     default="Mana starts full: write `mana = max_mana`."),
                rerun_box("mana follows max_mana", {"magical_affinity": 13}, "mana", "_R('magical_affinity') * 2",
                          "Use the box: `mana = max_mana`."),
            ],
        ),
        dict(
            id="print-status",
            text="Print the status line for your hero, like `Oogrish: 18/18 mana`. Build it from the boxes.",
            dictated=False,
            hints=[
                "Start like this: `print(hero_name + \": \" + `",
                "Which boxes go between the fixed words? Name, then mana, then max mana.",
                "Same beads, other names: `print(pet + \": \" + str(hp) + \"/\" + str(max_hp) + \" hp\")` shows "
                "`Moth: 3/5 hp`. Your frame: `print(hero_name + \": \" + ___ + \"/\" + ___ + \" mana\")`.",
            ],
            checks=[
                out_line(
                    "prints the status line",
                    "hero_name + ': ' + str(mana) + '/' + str(max_mana) + ' mana'",
                    "Your status line should be the hero's name, `: `, the mana, `/`, the max mana, then ` mana`. "
                    "For a hero named Tester with 26 mana, that is `Tester: 26/26 mana`.",
                    privacy=True,
                    spaces="Check the spaces: one after the colon, and one before `mana`. Like `Tester: 26/26 mana`.",
                ),
                rerun_line(
                    "the status line is built from the boxes", {"hero_name": "Tester", "magical_affinity": 13},
                    "'Tester: 26/26 mana'", "Build the line from the boxes, with `str()` on each number.", show=False,
                ),
                rerun_line(
                    "the status line follows other boxes too", {"hero_name": "Zelda", "magical_affinity": 5},
                    "'Zelda: 10/10 mana'", "Build the line from the boxes, with `str()` on each number.", show=False,
                ),
                (
                    "the first number is mana",
                    "import ast as _ast\n"
                    "assert [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Name' and _n.id == 'mana' "
                    "and type(_n.ctx).__name__ == 'Load'], 'Your line never uses the box `mana`. The first number is the "
                    "mana the hero has now: glue in `str(mana)` there, and `str(max_mana)` after the `/`.'",
                ),
            ],
            pass_line="Mar'tu: Hm. That one goes in my ledger.",
        ),
    ],
    solution=_status("Captain Glug"),
    partials=[
        _status("Oogrish", manaline="mana = 0", printed=False),
        _status("Oogrish", printed=False),
    ],
    assemble=dict(
        lines=['hero_name = "Oogrish"', "magical_affinity = 9", "max_mana = magical_affinity * 2", "mana = max_mana",
               STATUS_LINE.strip()],
        distractors=["max_mana = 18", 'print("Oogrish: 18/18 mana")',
                     'print(hero_name + ": " + mana + "/" + max_mana + " mana")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A status bar",
            text=(
                "```text\nOogrish  :   18   /   18   mana\nhero_name    mana     max_mana\n```\n"
                "Three pieces come from boxes. The rest are fixed words in quotes."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `max_mana = magical_affinity * 2`, run.\n2. `mana = max_mana`, run.\n"
                "3. `print(hero_name + \": \")`, run.\n4. Add `+ str(mana) + \"/\" + str(max_mana) + \" mana\"`, run."
            ),
        ),
        dict(
            angle="in Tor",
            label="My ledger",
            text="In my ledger, every hero gets one line: name, colon, mana over max mana. Same shape, every night.",
        ),
        dict(angle="shorter", text="Max is affinity `* 2`. Mana gets max. Glue: name, `\": \"`, mana, `\"/\"`, max, `\" mana\"`."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky's turn. Make `lucky_affinity = 13`, then `lucky_max` (twice it) and `lucky_mana` (full). "
            "Spend 3 from `lucky_mana`, then print `Lucky: 23/26 mana`, built from the boxes."
        ),
        hints=[
            "Same shape as Oogrish: `lucky_max = lucky_affinity * 2`, then `lucky_mana = lucky_max`.",
            "Spend: `lucky_mana = lucky_mana - 3`. Then glue the line with `str()`.",
        ],
        checks=[
            out_line("prints Lucky's line", "'Lucky: 23/26 mana'", "Print `Lucky: 23/26 mana`, built from the lucky boxes.",
                     hide=own("hero_name")),
            rerun_line("Lucky's line follows his boxes", {"lucky_affinity": 10}, "'Lucky: 17/20 mana'",
                       "Build every number from `lucky_affinity`.", hide=own("hero_name")),
        ],
        solution=_status("Oogrish") + (
            "lucky_affinity = 13\nlucky_max = lucky_affinity * 2\nlucky_mana = lucky_max\nlucky_mana = lucky_mana - 3\n"
            'print("Lucky: " + str(lucky_mana) + "/" + str(lucky_max) + " mana")\n'
        ),
    ),
    takeaway="Build a line from boxes: `hero_name + \": \" + str(mana) + \"/\" + str(max_mana) + \" mana\"`.",
    wrong_answers=[
        dict(why="max mana worked out by hand", code=_status("Oogrish", maxline="max_mana = 18"),
             fails_at=1, message_contains="13"),
        dict(why="mana typed by hand", code=_status("Oogrish", manaline="mana = 18"),
             fails_at=2, message_contains="13"),
        dict(why="the status line typed", code=_status("Oogrish", printed=False) + 'print("Oogrish: 18/18 mana")\n',
             fails_at=3, message_contains="Tester"),
        dict(why="numbers glued without str()",
             code=_status("Oogrish", printed=False) + 'print(hero_name + ": " + mana + "/" + max_mana + " mana")\n',
             fails_at=0, message_contains="concatenate"),
        dict(why="adds 2 instead of doubling", code=_status("Oogrish", maxline="max_mana = magical_affinity + 2"),
             fails_at=1, message_contains="adds 2"),
        dict(why="space missing after the colon",
             code=_status("Oogrish", printed=False) + 'print(hero_name + ":" + str(mana) + "/" + str(max_mana) + " mana")\n',
             fails_at=3, message_contains="spaces"),
        dict(why="gaming the message: the typed line plus the Tester line the message showed",
             code=_status("Oogrish", printed=False) + 'print("Oogrish: 18/18 mana")\nprint("Tester: 26/26 mana")\n',
             fails_at=3, message_contains="typed in"),
        dict(why="max_mana shown twice (right output only because mana starts full)",
             code=_status("Oogrish", printed=False) + 'print(hero_name + ": " + str(max_mana) + "/" + str(max_mana) + " mana")\n',
             fails_at=3, message_contains="str(mana)"),
        dict(why="capital letter: a new box Max_mana, placeholder left",
             code=_status("Oogrish", maxline="max_mana = 0\nMax_mana = magical_affinity * 2", manaline="mana = Max_mana"),
             fails_at=1, message_contains="letter for letter"),
        dict(why="the hero with no quotes (A-08 kratos)", code=_status("Oogrish").replace('"Oogrish"', "Kratos", 1),
             fails_at=0, message_contains="not defined"),
        dict(why="gaming: hero and affinity set to the rerun's values, the max typed",
             code=_status("Tester", printed=False).replace("magical_affinity = 9", "magical_affinity = 13")
             + 'print(hero_name + ": " + str(mana) + "/26 mana")\n', fails_at=3, message_contains="Zelda"),
        dict(why="twice worked out on a line of its own, kept in no box",
             code=_status("Oogrish", maxline="max_mana = 0\nmagical_affinity * 2"),
             fails_at=1, message_contains="keeps it nowhere"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="combine-values,concat-str,reassign", solo="false", dictates="2",
             foreign_names="power,double,spare,backpack,pet,hp,max_hp") + "\n"
        "Lint (e): the solution uses another hero (Captain Glug) and passes; the assemble lines use Mar'tu's pick "
        "(Oogrish). The status-line check never echoes the student's hero: its message uses Tester / Zelda, and the side "
        "quest's diffs hide lines holding the hero (own('hero_name')). CP3 also needs `mana` read somewhere, so "
        "`str(max_mana)` twice (same output while mana starts full) is caught. More structure "
        "(G1 R13): the Teach hint shows the same beads with other names (pet / hp / max_hp, `Moth: 3/5 hp`), then "
        "the student's frame with ___ blanks. Lucky's side quest uses new lucky_* boxes so it "
        "never turns a finished checkpoint red."
    ),
)

BAR_STARTER = (
    'full = "█"\nempty = "░"\nmana = 3\nmax_mana = 5\nbar = full * 0 + empty * 0\nprint("[" + bar + "]")\n'
)
BAR_LINE = "bar = full * mana + empty * (max_mana - mana)"


def _bar(line, mana=3, max_mana=5):
    return f'full = "█"\nempty = "░"\nmana = {mana}\nmax_mana = {max_mana}\n{line}\nprint("[" + bar + "]")\n'


REPEAT_A_MARK = dict(
    id="repeat-a-mark",
    title="Repeat a mark",
    martu=(
        "`*` also [[stamp|stamps]] text: `\"█\" * 3` stamps three blocks. A mana bar is full blocks for the mana "
        "you have, then light blocks for the mana used.\n"
        "`+` glues two texts. `*` stamps one text a number of times."
    ),
    names=["full", "empty", "mana", "max_mana", "bar"],
    predict=dict(
        q="What will this print?",
        code='print("█" * 3)\n',
        choices=["███", "█3", "an error"],
        answer=0,
        explain=(
            "`*` stamps the text 3 times. Try it in your head: `\"█\" * 0` stamps nothing at all, "
            "and `\"█\" * 1` stamps one block."
        ),
    ),
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="full-part",
            text="Replace the first `0` with `mana`.",
            dictated=True,
            hints=[
                "Change `full * 0` to `full * `, then the box name.",
                "Which box says how much mana there is right now?",
                "`\"*\" * stars` stamps one star for every star in the box `stars`. If `stars = 2`, that is `**`.",
            ],
            checks=[
                (
                    "full blocks for the mana",
                    "assert bar.count(full) == mana, 'The bar has ' + str(bar.count(full)) + ' full blocks, but `mana` is ' "
                    "+ str(mana) + '. Replace the first 0 with `mana`.'",
                ),
                rerun(
                    "the full part follows mana (0)", {"mana": 0, "max_mana": 5}, "_n = _R('bar').count(_R('full'))",
                    "_n == 0", "'the bar had ' + str(_n) + ' full blocks, but it should have 0. Use `mana`, not a number.'",
                ),
                rerun(
                    "the full part follows mana (5)", {"mana": 5, "max_mana": 5}, "_n = _R('bar').count(_R('full'))",
                    "_n == 5", "'the bar had ' + str(_n) + ' full blocks, but it should have 5. Use `mana`, not a number.'",
                ),
            ],
        ),
        dict(
            id="empty-part",
            text="Replace the second `0` with the mana used: `(max_mana - mana)`, in brackets.",
            dictated=True,
            hints=[
                "Change `empty * 0` to `empty * (`, then the subtraction, then `)`.",
                "How many light blocks are there when mana is 3 of 5?",
                "Python does `*` before `-`, so wrap the subtraction: `(a - b)`. "
                "`\"-\" * (8 - 3)` stamps 5 dashes.",
            ],
            checks=[
                rerun_line("empty bar at mana 0", {"mana": 0, "max_mana": 5}, "'[░░░░░]'",
                           "The light part is the mana used: `empty * (max_mana - mana)`."),
                rerun_line("bar at mana 3", {"mana": 3, "max_mana": 5}, "'[███░░]'",
                           "The light part is the mana used: `empty * (max_mana - mana)`."),
                rerun_line("full bar at mana 5", {"mana": 5, "max_mana": 5}, "'[█████]'",
                           "The light part is the mana used: `empty * (max_mana - mana)`."),
                rerun_line("bar at mana 2 of 6", {"mana": 2, "max_mana": 6}, "'[██░░░░]'",
                           "Use the box `max_mana` in the brackets, not the number 5: `(max_mana - mana)`."),
            ],
            pass_line="Mar'tu: Which part of your line is the mana used? Point at it. Yes. The part in brackets.",
        ),
        dict(
            id="gearshift-bar",
            text="Change the boxes to show Gearshift's full bar: 20 of 20.",
            dictated=False,
            hints=[
                "Change line 3 to `mana = 20`.",
                "Two boxes need new numbers: the mana he has, and his max mana.",
                "A full bar means no mana is used: the mana is the same as the max.",
            ],
            checks=[
                ("max_mana is 20", "assert max_mana == 20, \"Gearshift's max mana is 20: change `max_mana`.\""),
                ("mana is 20", "assert mana == 20, 'His bar is full, so `mana` is 20 too.'"),
                (
                    "a full bar is printed",
                    "assert bar == full * 20 and '[' + full * 20 + ']' in _lines(), "
                    "'The bar should be 20 full blocks. Keep your `bar` line and the `print` as they are.'",
                ),
            ],
            pass_line="Gearshift: Barrier's holding. Twenty of twenty.",
        ),
    ],
    solution=_bar(BAR_LINE, 20, 20),
    partials=[
        _bar("bar = full * mana + empty * 0"),
        _bar(BAR_LINE),
    ],
    assemble=dict(
        lines=['full = "█"', 'empty = "░"', "mana = 20", "max_mana = 20", BAR_LINE, 'print("[" + bar + "]")'],
        distractors=["bar = full * mana + empty * max_mana - mana", "bar = full * 20"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A fuel gauge",
            text=(
                "```text\nmana 3 of 5:   [ █ █ █ ░ ░ ]\n                 have   used\n                 3      5 - 3\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A stamp",
            text=(
                "A rubber stamp makes the same mark again and again. `full * mana` presses the full stamp mana times. "
                "`empty * (max_mana - mana)` presses the light stamp once for each point used."
            ),
        ),
        dict(
            angle="step-by-step",
            label="What Python does first",
            text=(
                "For `empty * (max_mana - mana)` with mana 3 of 5:\n1. Brackets first: `5 - 3` is 2.\n"
                "2. Then `empty * 2` stamps `░░`.\nWithout brackets, Python tries `empty * 5` first, then `\"░░░░░\" - 3`, "
                "and text minus a number is an error."
            ),
        ),
        dict(
            angle="why",
            label="Why brackets?",
            text="Python does `*` before `-`, just like in math class. Brackets say: do this part first.",
        ),
        dict(angle="shorter", text="Full: `full * mana`. Light: `empty * (max_mana - mana)`. Glue them with `+`."),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "`get_mana_bar` had `filled = \"█\" * caster[\"mana\"]` and "
                "`empty = \"░\" * (caster[\"max_mana\"] - caster[\"mana\"])`. Your line is the same bar."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants numbers too. Print a second line: the bar with the numbers after it, like `[███░░] 3/5`. "
            "Use `str()` for each number."
        ),
        hints=[
            "Start like this: `print(\"[\" + bar + \"] \" + str(mana) + `",
            "After the number comes `\"/\"`, then `str(max_mana)`.",
        ],
        checks=[
            out_line("prints bar and numbers", "'[' + bar + '] ' + str(mana) + '/' + str(max_mana)",
                     "Print the bar, a space, then `mana/max_mana`, like `[███░░] 3/5`."),
            rerun_line("the numbers follow the boxes", {"mana": 3, "max_mana": 5}, "'[███░░] 3/5'",
                       "Use `str(mana)` and `str(max_mana)`."),
        ],
        solution=_bar(BAR_LINE, 20, 20) + 'print("[" + bar + "] " + str(mana) + "/" + str(max_mana))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]\nempty = "░" * (caster["max_mana"] - caster["mana"])',
        why=(
            "You have seen these two lines. Replace the first 0, replace the second 0 with the mana used. "
            "You just did the same steps with shorter labels."
        ),
    ),
    takeaway=(
        "`\"█\" * mana` stamps a mark. Brackets first: `empty * (max_mana - mana)`. Why brackets: Python does `*` "
        "before `-`, so the brackets make the subtraction happen first."
    ),
    wrong_answers=[
        dict(why="no brackets around the mana used", code=_bar("bar = full * mana + empty * max_mana - mana"),
             fails_at=0, message_contains="operand"),
        dict(why="the light part typed as a number", code=_bar("bar = full * mana + empty * 2"),
             fails_at=2, message_contains="mana"),
        dict(why="the full part typed as a number", code=_bar("bar = full * 3 + empty * (max_mana - mana)"),
             fails_at=1, message_contains="not a number"),
        dict(why="text plus a number", code=_bar('bar = "█" + mana'),
             fails_at=0, message_contains="concatenate"),
        dict(why="Gearshift's bar typed as 20 blocks", code=_bar("bar = full * 20", 20, 20),
             fails_at=1, message_contains="not a number"),
        dict(why="max mana typed as 5 inside the brackets (passes every rerun at max 5, and the 20/20 bar)",
             code=_bar("bar = full * mana + empty * (5 - mana)", 20, 20), fails_at=2, message_contains="max_mana = 6"),
        dict(why="gaming the message: the 3-of-5 bar typed",
             code=_bar("bar = full * mana + empty * 0") + 'print("[░░░░░]")\nprint("[███░░]")\nprint("[█████]")\n',
             fails_at=2, message_contains="typed in"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="repeat-string", solo="false", dictates="1,2",
             foreign_names="stars,a,b", twin="a glug bar with ▓: glug = 2 of 6 -> [▓▓░░░░]") + "\n"
        "Skill gate pattern:StrRepeat (op:Mult on text; no new token). Blocks are pre-typed (G1 R8). "
        "CP2's reruns set mana AND max_mana, so they stay true after CP3 changes the boxes to 20/20; the 2-of-6 "
        "rerun catches `(5 - mana)`, which passes every max-5 rerun and the 20/20 bar. "
        "Point-at-it (G2 R9) is CP2's pass line. BQ variant for students who read 1-A2 (`//`, 10 blocks wide) "
        "needs a per-student condition the schema does not have."
    ),
)

BROKEN_STARTER = (
    LANTERN_STORY +
    "lantern_count = 3\nlantern_price = 4\nlantern_cost = lantern_count * lantern_price\n" +
    ROPE_STORY +
    "rope_count = 2\nrope_price = 5\nrope_cost = 10\n"
    'print("Rope: " + str(rope_cost) + " coins")\n'
    "mana = 3\nmax_mana = 5\n"
    'print("Mana: " + mana)\n'
    'bar = "█" * mana + "░" * max_mana - mana\n'
    'print("[" + bar + "]")\n'
)


def _broken(mana_line='print("Mana: " + str(mana))', rope_cost="rope_cost = rope_count * rope_price",
            rope_boxes="rope_count = 5\nrope_price = 2", bar='bar = "█" * mana + "░" * (max_mana - mana)'):
    return (
        LANTERN_STORY +
        "lantern_count = 3\nlantern_price = 4\nlantern_cost = lantern_count * lantern_price\n" +
        ROPE_STORY +
        f"{rope_boxes}\n{rope_cost}\n"
        'print("Rope: " + str(rope_cost) + " coins")\n'
        "mana = 3\nmax_mana = 5\n"
        f"{mana_line}\n{bar}\n"
        'print("[" + bar + "]")\n'
    )


BROKEN_KNOWN = ["lantern_count", "lantern_price", "lantern_cost", "rope_count", "rope_price", "rope_cost",
                "mana", "max_mana", "bar", "total_cost"]

BROKEN_SPELL_1C = dict(
    id="broken-spell-1c",
    title="Broken spell",
    martu=(
        "Four bugs. Two are loud: they crash, and Python names their line. Mend those first. Two are quiet: they "
        "hide in the Rope line, which prints the right thing. Mar'tu's checks try other numbers to find them."
    ),
    names=["rope_count", "rope_price", "rope_cost", "mana", "max_mana", "bar", "str"],
    pair_talk=(
        "Pair talk: you may hunt these bugs together. Talk through each one, then each of you mends it on your "
        "own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-mana-line",
            text="Mend the `Mana:` line so it prints `Mana: 3`.",
            dictated=False,
            hints=[
                "Look at `print(\"Mana: \" + mana)`. The number needs to become text: `str(mana)`.",
                "Python's message names this line. Text and a number cannot glue.",
                "`\"Sips: \" + str(5)` works. `\"Sips: \" + 5` does not.",
            ],
            checks=[
                out_line("prints Mana: 3", "'Mana: ' + str(mana)", "Print `Mana: ` glued to `str(mana)`."),
                rerun_line("the mana line follows the box", {"mana": 4}, "'Mana: 4'",
                           "Glue the box, not a number: `\"Mana: \" + str(mana)`."),
                rerun_line("the mana line follows the box (1)", {"mana": 1}, "'Mana: 1'",
                           "Glue the box, not a number: `\"Mana: \" + str(mana)`."),
            ],
        ),
        dict(
            id="mend-bar",
            text="Mend the bar so the light blocks show the mana used.",
            dictated=False,
            hints=[
                "Look at the `bar` line. Which part should happen first?",
                "Python does `*` before `-`. Which part needs brackets?",
                "`\"-\" * (8 - 3)` stamps 5 dashes. Without brackets, Python tries text minus a number.",
            ],
            checks=[
                rerun_line("bar at mana 3", {"mana": 3, "max_mana": 5}, "'[███░░]'",
                           "The light part is the mana used: `\"░\" * (max_mana - mana)`."),
                rerun_line("bar at mana 0", {"mana": 0, "max_mana": 5}, "'[░░░░░]'",
                           "The light part is the mana used: `\"░\" * (max_mana - mana)`."),
                rerun_line("bar at mana 2 of 6", {"mana": 2, "max_mana": 6}, "'[██░░░░]'",
                           "Use the box `max_mana` in the brackets, not the number 5: `(max_mana - mana)`."),
            ],
            pass_line="Mar'tu: Both loud bugs mended. Now the quiet ones.",
        ),
        dict(
            id="mend-rope-cost",
            text="`rope_cost` prints the right number, but it is typed by hand. Make Python work it out from the rope boxes.",
            dictated=False,
            hints=[
                "Start like this: `rope_cost = rope_count * `",
                "Look at how `lantern_cost` is made, two lines up.",
                "A cost is how many times the price of one: `c = a * b`.",
            ],
            checks=[
                slot("rope_cost is built from the boxes", "rope_cost", "rope_count * rope_price", known=BROKEN_KNOWN,
                     default="Make `rope_cost` from the two rope boxes, like `lantern_cost`."),
                rerun_box("rope_cost follows the rope boxes", {"rope_count": 6, "rope_price": 3}, "rope_cost",
                          "_R('rope_count') * _R('rope_price')", "Build it from the rope boxes."),
            ],
            pass_line="Mar'tu: Right answer, wrong reason, now mended. That one fools everyone once.",
        ),
        dict(
            id="mend-rope-boxes",
            text="Read the rope story note. Put each rope number in the box that means it.",
            dictated=False,
            hints=[
                "Find how many coils Mar'tu needs. That number goes after `rope_count = `.",
                "The cost came out right, 10, because 2 times 5 is 5 times 2. Ask each number what it means.",
                "'Candles cost 1 coin each, and I need 3': 3 is how many, 1 is the price of one.",
            ],
            checks=[
                story_pair("the rope boxes match the story", "rope_count", "rope_price", 5, 2, "coils",
                           known=BROKEN_KNOWN, wild="The story says Mar'tu needs 5 coils.", price_first=True,
                           swap_extra=" It still comes out 10, because 2 times 5 is 5 times 2. But if Mar'tu needs one "
                           "more coil, which box changes?"),
            ],
            pass_line="Mar'tu: Four bugs, four mends. The spell holds, yes?",
        ),
    ],
    solution=_broken(),
    assemble=dict(
        lines=[
            "lantern_count = 3", "lantern_price = 4", "lantern_cost = lantern_count * lantern_price",
            "rope_count = 5", "rope_price = 2", "rope_cost = rope_count * rope_price",
            'print("Rope: " + str(rope_cost) + " coins")', "mana = 3", "max_mana = 5",
            'print("Mana: " + str(mana))', 'bar = "█" * mana + "░" * (max_mana - mana)', 'print("[" + bar + "]")',
        ],
        distractors=['print("Mana: " + mana)', "rope_cost = 10", 'bar = "█" * mana + "░" * max_mana - mana'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Run. Python stops at the first crash and names the line. Mend it.\n"
                "2. Run again. Mend the next crash.\n"
                "3. When nothing crashes, the checks speak. Read the message under the step."
            ),
        ),
        dict(
            angle="picture",
            label="Two kinds of bug",
            text=(
                "```text\nloud bugs:  Python stops, and its message names the line\n"
                "quiet bugs: the program runs, but the code is wrong\n```\n"
                "The quiet ones only show up when someone tries other numbers."
            ),
        ),
        dict(
            angle="shorter",
            text="`str(mana)`. `rope_count * rope_price`. Count 5, price 2. Brackets around `max_mana - mana`.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Make `total_cost` from the two costs, then print `Total: 22 coins`, built from the boxes.",
        hints=[
            "Start like this: `total_cost = lantern_cost + rope_cost`",
            "Then glue: `\"Total: \" + str(total_cost) + \" coins\"`.",
        ],
        checks=[
            out_line("prints the total", "'Total: 22 coins'", "Print `Total: 22 coins`, built from `total_cost`."),
            rerun_line("the total follows the boxes", {"lantern_count": 7}, "'Total: 38 coins'",
                       "Build it from the cost boxes, with `str()`."),
        ],
        solution=_broken() + 'total_cost = lantern_cost + rope_cost\nprint("Total: " + str(total_cost) + " coins")\n',
    ),
    takeaway="Loud bugs crash and name a line. Quiet bugs print the right thing for the wrong reason: try other numbers.",
    wrong_answers=[
        dict(why="the starter (two crashes)", code=BROKEN_STARTER, fails_at=0, message_contains="concatenate"),
        dict(why="mana line left alone", code=_broken(mana_line='print("Mana: " + mana)'),
             fails_at=0, message_contains="concatenate"),
        dict(why="the mana line typed", code=_broken(mana_line='print("Mana: 3")'),
             fails_at=1, message_contains="4"),
        dict(why="rope_cost still typed by hand", code=_broken(rope_cost="rope_cost = 10"),
             fails_at=3, message_contains="18"),
        dict(why="rope boxes still swapped", code=_broken(rope_boxes="rope_count = 2\nrope_price = 5"),
             fails_at=4, message_contains="which box changes"),
        dict(why="bar brackets still missing", code=_broken(bar='bar = "█" * mana + "░" * max_mana - mana'),
             fails_at=0, message_contains="operand"),
        dict(why="bar mended with the max typed as 5", code=_broken(bar='bar = "█" * mana + "░" * (5 - mana)'),
             fails_at=2, message_contains="max_mana = 6"),
        dict(why="gaming the message: the typed Mana line plus the one the message showed",
             code=_broken(mana_line='print("Mana: 3")\nprint("Mana: 4")'), fails_at=1, message_contains="typed in"),
        dict(why="rope_cost typed as a sum instead of from the boxes", code=_broken(rope_cost="rope_cost = 5 * 2"),
             fails_at=3, message_contains="18"),
        dict(why="gaming: mana set to the rerun's value, then the line typed",
             code=_broken(mana_line='print("Mana: 4")').replace("mana = 3\n", "mana = 4\n"), fails_at=1,
             message_contains="Mana: 1"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="combine-values,concat-str,repeat-string,read-traceback",
             solo="false", dictates="", foreign_names="candles,sips") + "\n"
        "Two loud bugs (TypeError) and two quiet ones (typed rope_cost passes OUT but fails CMB; swapped rope boxes "
        "give the same product, so only SWAP catches them). Checkpoint order follows Python's messages: the two "
        "loud bugs first (mana line, then bar), then the two quiet ones in the Rope line (typed cost, then the "
        "swapped boxes, whose SWAP message says why the product still came out 10). On the site a crash fails "
        "every checkpoint, so no partials (mending only the mana line still crashes on the bar line). Can be done "
        "in pairs; every student mends it on their own screen."
    ),
)

CANDLE_STORY = "# Mar'tu needs 4 candles that cost 2 coins each.\n"
CANDLE_KNOWN = ["candle_count", "candle_price", "candle_cost"]

SOLO_1C = dict(
    id="solo-1c",
    title="Show Mar'tu",
    martu="A short problem, just for you. Let the code combine it.",
    solo=True,
    names=["candle_count", "candle_price", "candle_cost"],
    starter=CANDLE_STORY + "candle_count = 0\ncandle_price = 0\ncandle_cost = 0\nprint(candle_cost)\n",
    checkpoints=[
        dict(
            id="candle-boxes",
            text="Fill in `candle_count` and `candle_price` from the story.",
            dictated=False,
            hints=[
                "Start with how many candles: change the 0 after `candle_count = `.",
                "Ask each number: how many? or how much is one?",
                "In '2 maps at 6 coins', 2 is how many and 6 is the price of one.",
            ],
            checks=[
                story_pair("the candle boxes match the story", "candle_count", "candle_price", 4, 2, "candles",
                           known=CANDLE_KNOWN + ["lantern_count", "lantern_price"],
                           wild="The story says 4 candles. Use the story's numbers here."),
            ],
        ),
        dict(
            id="candle-cost",
            text="Make `candle_cost` from the two candle boxes.",
            dictated=False,
            hints=[
                "Start like this: `candle_cost = candle_count * `",
                "A cost is how many times the price of one.",
                "If `a = 2` and `b = 6`, then `c = a * b` puts 12 in `c`.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                slot("candle_cost multiplies the boxes", "candle_cost", "candle_count * candle_price",
                     known=CANDLE_KNOWN, foreign=["lantern_count", "lantern_price", "lantern_cost", "map_cost"],
                     rules=[
                         # LINE-TOTAL: `candle_count * 8` multiplies by the line total again.
                         ("_have in (candle_count * candle_count * candle_price, "
                          "candle_price * candle_count * candle_price)",
                          "8 is already the cost of all 4 candles, so multiplying by it again gives too much. "
                          "Multiply how many by the price of one: `candle_count * candle_price`."),
                     ],
                     default="Make `candle_cost` from the two candle boxes."),
                rerun_box("candle_cost follows the boxes", {"candle_count": 7, "candle_price": 3}, "candle_cost",
                          "_R('candle_count') * _R('candle_price')", COMBINE_FIX),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ let the code combine your boxes.",
        ),
    ],
    solution=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = candle_count * candle_price\nprint(candle_cost)\n",
    partials=[CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = 0\nprint(candle_cost)\n"],
    assemble=dict(
        lines=["candle_count = 4", "candle_price = 2", "candle_cost = candle_count * candle_price", "print(candle_cost)"],
        distractors=["candle_count = 2", "candle_cost = 8"],
    ),
    another_way=[
        dict(angle="step-by-step", text="1. How many candles? 2. How much is one? 3. Cost = how many `*` price of one."),
        dict(angle="shorter", text="Count, price, then `candle_cost = candle_count * candle_price`."),
    ],
    takeaway="On your own: boxes from the story, then let the code combine them.",
    wrong_answers=[
        dict(why="candle numbers swapped",
             code=CANDLE_STORY + "candle_count = 2\ncandle_price = 4\ncandle_cost = candle_count * candle_price\nprint(candle_cost)\n",
             fails_at=1, message_contains="swapped"),
        dict(why="the cost typed by hand",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = 8\nprint(candle_cost)\n",
             fails_at=2, message_contains="stayed 8"),
        dict(why="an earlier exercise's names",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = 0\n"
             "lantern_cost = candle_count * candle_price\nprint(lantern_cost)\n",
             fails_at=2, message_contains="earlier step"),
        dict(why="capital letter in a name",
             code=CANDLE_STORY + "Candle_count = 4\ncandle_count = 0\ncandle_price = 2\ncandle_cost = 0\nprint(candle_cost)\n",
             fails_at=1, message_contains="letter for letter"),
        dict(why="the math worked out on a line of its own, kept in no box",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = 0\ncandle_count * candle_price\nprint(candle_cost)\n",
             fails_at=2, message_contains="keeps it nowhere"),
        dict(why="the price typed into the cost",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = candle_count * 2\nprint(candle_cost)\n",
             fails_at=2, message_contains="candle_price = 3"),
        dict(why="numbers in quotes", code=CANDLE_STORY + 'candle_count = "4"\ncandle_price = 2\ncandle_cost = 0\nprint(candle_cost)\n',
             fails_at=1, message_contains="quotes"),
        dict(why="LINE-TOTAL: the candle count times the line total 8",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = candle_count * 8\nprint(candle_cost)\n",
             fails_at=2, message_contains="already the cost of all 4 candles"),
        dict(why="LINE-TOTAL: the price times the line total 8",
             code=CANDLE_STORY + "candle_count = 4\ncandle_price = 2\ncandle_cost = candle_price * 8\nprint(candle_cost)\n",
             fails_at=2, message_contains="already the cost of all 4 candles"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="combine-values", solo="true", dictates="",
             foreign_names="lantern_count,lantern_price,lantern_cost,map_cost,a,b,c",
             seat_b="Arrows cost 3 coins each, and Lucky wants 6 (price-first; arrow_count, arrow_price, arrow_cost)") + "\n"
        "SOLO make-twin. Seat A (and anyone solo) gets candles; seat B would get arrows (price-first) once pair "
        "mode ships. Recorded, never blocking, never shown to a partner. Left sides are given (S3) with 0 "
        "placeholders so the starter runs (`candle_cost = 0` stays). The pass line reads as showing off a skill on "
        "the map, not as being watched. LINE-TOTAL (`candle_count * 8`) gets its own message."
    ),
)

LESSON_1C = dict(
    kind="lesson",
    id="math-and-glue",
    title="Math and Glue",
    minutes=39,
    summary="Let Python do the sums, spend mana, glue words with `str()`, and stamp a mana bar.",
    notes=(
        "Lesson 1C (CC; 1C-09 SC). Preceded by 1c-remembers. Exactly one SOLO (solo-1c). Non-dictated checkpoints: "
        "1C-02 CP2, 1C-03 CP2-3, 1C-07 CP1/CP3, 1C-08 CP3, 1C-09, 1C-S. 1C-04 (spend-mana) and 1C-06 (glue-words) are "
        "dictated; glue-words now in two steps (`print(name + \" has \")`, then `+ str(mana) + \" mana.\"`), "
        "which is the extra minute (38 -> 39). Rest marker: spend-mana's pass line says halfway, a good place to "
        "rest, work saved. 1C-05 lives in the pool."
    ),
    exercises=[CHALK_MATH, WHAT_EACH_NUMBER_MEANS, LET_THE_CODE_COMBINE, SPEND_MANA, GLUE_WORDS, STATUS_LINE_EX,
               REPEAT_A_MARK, BROKEN_SPELL_1C, SOLO_1C],
)

# ---------------------------------------------------------------------------------------------
# Extra practice 1X-C "Math" (pool)
# ---------------------------------------------------------------------------------------------

SHORT_STARTER = (
    "hours_waited = 30\nhours_waited = hours_waited + 6\nmana = 20\nmana = mana - 3\n"
    "print(hours_waited)\nprint(mana)\n"
)

THE_SHORT_WAY = dict(
    id="the-short-way",
    title="The short way",
    martu=(
        "`hours_waited += 6` is a short way to write `hours_waited = hours_waited + 6`. "
        "`mana -= 3` means `mana = mana - 3`.\n"
        "Same answer, less typing. You never have to use it. Lazy wizards love it."
    ),
    introduces=["node:AugAssign"],
    names=["hours_waited", "mana"],
    predict=dict(
        q="What will this print?",
        code="hours_waited = 30\nhours_waited += 6\nmana = 20\nmana -= 3\nprint(hours_waited)\nprint(mana)\n",
        choices=["36\n17", "6\n3", "30\n20"],
        answer=0,
        explain="`+= 6` adds 6 to what is in the box and puts it back: 30 becomes 36. `-= 3` takes 3 away: 20 becomes 17.",
    ),
    starter=SHORT_STARTER,
    checkpoints=[
        dict(
            id="plus-equals",
            text="Rewrite line 2 the short way: `hours_waited += 6`.",
            dictated=True,
            hints=[
                "Change line 2 to start with `hours_waited += `.",
                "Which box is on both sides of line 2? The short way names it once.",
                "`glow += 2` means `glow = glow + 2`. The `+` comes before the `=`.",
            ],
            checks=[
                (
                    "plus before equals",
                    "import ast as _ast\n"
                    "_flip = [_n.lineno for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                    "and type(_n.value).__name__ == 'UnaryOp']\n"
                    "assert not _flip, 'Line ' + str(_flip[0] if _flip else 0) + ' has `=+` or `=-`, which puts a "
                    "plain number in the box. The short way is `+=`: the sign first, then the `=`.'",
                ),
                (
                    "hours_waited is 36",
                    "assert hours_waited != 66, '`+=` already adds to what is in the box. Write `hours_waited += 6`, "
                    "not `hours_waited += hours_waited + 6`.'\n"
                    "assert hours_waited == 36, '`hours_waited` should end at 36: 30, then 6 more.'",
                ),
                (
                    "uses += on hours_waited",
                    "import ast as _ast\n"
                    "assert [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'AugAssign' "
                    "and type(_n.op).__name__ == 'Add' and getattr(_n.target, 'id', '') == 'hours_waited'], "
                    "'Line 2 still uses the long way. Write it as `hours_waited += 6`.'",
                ),
            ],
        ),
        dict(
            id="minus-equals",
            text="Rewrite line 4 the short way too.",
            dictated=False,
            hints=[
                "Change line 4 to start with `mana -= `.",
                "Line 4 takes 3 away from `mana`. Which sign goes before the `=`?",
                "`glow -= 2` means `glow = glow - 2`.",
            ],
            checks=[
                ("mana is 17", "assert mana == 17, '`mana` should end at 17: 20, take away 3.'"),
                (
                    "uses -= on mana",
                    "import ast as _ast\n"
                    "assert [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'AugAssign' "
                    "and type(_n.op).__name__ == 'Sub' and getattr(_n.target, 'id', '') == 'mana'], "
                    "'Line 4 still uses the long way. Write it with `-=`.'",
                ),
            ],
            pass_line="Mar'tu: Shorter. Same mana. Use whichever you like, yes?",
        ),
    ],
    solution="hours_waited = 30\nhours_waited += 6\nmana = 20\nmana -= 3\nprint(hours_waited)\nprint(mana)\n",
    partials=["hours_waited = 30\nhours_waited += 6\nmana = 20\nmana = mana - 3\nprint(hours_waited)\nprint(mana)\n"],
    assemble=dict(
        lines=["hours_waited = 30", "hours_waited += 6", "mana = 20", "mana -= 3", "print(hours_waited)", "print(mana)"],
        distractors=["hours_waited =+ 6", "mana =- 3"],
    ),
    another_way=[
        dict(angle="read aloud", label="Say it out loud", text="`hours_waited += 6`: hours waited goes up by 6. `mana -= 3`: mana goes down by 3."),
        dict(angle="shorter", text="`box += n` is `box = box + n`. `box -= n` is `box = box - n`."),
    ],
    takeaway="`x += 6` is `x = x + 6`. `x -= 3` is `x = x - 3`. Both forms are always fine.",
    wrong_answers=[
        dict(why="=+ instead of +=",
             code="hours_waited = 30\nhours_waited =+ 6\nmana = 20\nmana = mana - 3\nprint(hours_waited)\nprint(mana)\n",
             fails_at=1, message_contains="+="),
        dict(why="still the long way", code=SHORT_STARTER, fails_at=1, message_contains="long way"),
        dict(why="mixes both forms: += with the long right side",
             code="hours_waited = 30\nhours_waited += hours_waited + 6\nmana = 20\nmana = mana - 3\nprint(hours_waited)\nprint(mana)\n",
             fails_at=1, message_contains="already adds"),
        dict(why="+= on the wrong line",
             code="hours_waited = 30\nhours_waited = hours_waited + 6\nmana = 20\nmana -= 3\nprint(hours_waited)\nprint(mana)\n",
             fails_at=1, message_contains="hours_waited += 6"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="reassign", solo="false", dictates="1", foreign_names="glow") + "\n"
        "1C-05 (kept id). node:AugAssign is pool-only: no core starter or solution shows `+=`, and every later "
        "check accepts both forms. The spec's CP1 (values right) and CP2 (_uses AugAssign) become one checkpoint "
        "per rewritten line, each checking that box's value and its `+=` / `-=`."
    ),
)

SUPPLY_STORY = "# Chalk costs 5 coins a stick, and Oogrish wants 3.\n# Oil costs 3 coins a flask, and he needs 4.\n"
SUPPLY_KNOWN = ["chalk_count", "chalk_price", "oil_count", "oil_price", "supply_total", "chalk_cost", "oil_cost"]
SUPPLY_TOTAL = "chalk_count * chalk_price + oil_count * oil_price"
SUPPLY_BOXES = "chalk_count = 3\nchalk_price = 5\noil_count = 4\noil_price = 3\n"


def _supply(total_line):
    return SUPPLY_STORY + SUPPLY_BOXES + total_line + "\nprint(supply_total)\n"


COMBINE_AGAIN = dict(
    id="combine-again",
    title="Combine it again",
    martu=(
        "Same idea, new shop. Both lines of this story give the price first. "
        "Ask each number its question, then let the code combine it."
    ),
    names=["chalk_count", "chalk_price", "oil_count", "oil_price", "supply_total"],
    starter=SUPPLY_STORY + "chalk_count = 0\nchalk_price = 0\noil_count = 0\noil_price = 0\nsupply_total = 0\nprint(supply_total)\n",
    checkpoints=[
        dict(
            id="supply-boxes",
            text="Fill in the four boxes from the story.",
            dictated=False,
            hints=[
                "Start with chalk: how many sticks does Oogrish want? That goes after `chalk_count = `.",
                "Each line gives the price first. Ask: how many? how much is one?",
                "'Candles cost 1 coin each, and I need 3': 3 is how many, 1 is the price of one.",
            ],
            checks=[
                story_pair("the chalk boxes match the story", "chalk_count", "chalk_price", 3, 5, "sticks",
                           known=SUPPLY_KNOWN, wild="The story says Oogrish wants 3 sticks.", price_first=True),
                story_pair("the oil boxes match the story", "oil_count", "oil_price", 4, 3, "flasks",
                           known=SUPPLY_KNOWN, wild="The story says he needs 4 flasks.", price_first=True),
            ],
        ),
        dict(
            id="supply-total",
            text="Make `supply_total` the cost of everything, built from the boxes.",
            dictated=False,
            hints=[
                "Start like this: `supply_total = chalk_count * chalk_price + `",
                "Two costs: chalk, then oil. Each is how many times the price of one.",
                "If `a = 2`, `b = 6`, `c = 4` and `d = 3`, then `a * b + c * d` is 24. Python does `*` before `+`.",
            ],
            checks=[
                slot("supply_total adds both costs", "supply_total", SUPPLY_TOTAL, known=SUPPLY_KNOWN,
                     rules=[("_have == chalk_count + oil_count", "You added how many, not costs. Each cost is how many times the price.")],
                     default="Make `supply_total` from the boxes: chalk cost plus oil cost."),
                rerun_box("supply_total follows the chalk", {"chalk_count": 5, "chalk_price": 7}, "supply_total",
                          "_R('chalk_count') * _R('chalk_price') + _R('oil_count') * _R('oil_price')", COMBINE_FIX),
                rerun_box("supply_total follows the oil", {"oil_count": 9, "oil_price": 4}, "supply_total",
                          "_R('chalk_count') * _R('chalk_price') + _R('oil_count') * _R('oil_price')", COMBINE_FIX),
            ],
        ),
    ],
    solution=_supply("supply_total = chalk_count * chalk_price + oil_count * oil_price"),
    partials=[_supply("supply_total = 0")],
    assemble=dict(
        lines=["chalk_count = 3", "chalk_price = 5", "oil_count = 4", "oil_price = 3",
               "supply_total = chalk_count * chalk_price + oil_count * oil_price", "print(supply_total)"],
        distractors=["supply_total = 27", "chalk_count = 5"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            text=(
                "1. Fill the four boxes. 2. Chalk cost: `chalk_count * chalk_price`. 3. Oil cost the same way. "
                "4. Add them."
            ),
        ),
        dict(angle="shorter", text="`supply_total = chalk_count * chalk_price + oil_count * oil_price`, never 27."),
    ],
    takeaway="Price first or count first, ask the question. Then combine: count `*` price `+` count `*` price.",
    wrong_answers=[
        dict(why="chalk numbers in reading order (price first)",
             code="chalk_count = 5\nchalk_price = 3\noil_count = 4\noil_price = 3\nsupply_total = 27\nprint(supply_total)\n",
             fails_at=1, message_contains="swapped"),
        dict(why="the total typed by hand",
             code=_supply("supply_total = 27"),
             fails_at=2, message_contains="stayed 27"),
        dict(why="chalk price typed inside the total (passes a count-only rerun)",
             code=_supply("supply_total = chalk_count * 5 + oil_count * oil_price"),
             fails_at=2, message_contains="chalk_price = 7"),
        dict(why="oil count typed inside the total (passes a price-only rerun)",
             code=_supply("supply_total = chalk_count * chalk_price + 4 * oil_price"),
             fails_at=2, message_contains="oil_count = 9"),
        dict(why="the line totals typed as numbers",
             code=_supply("supply_total = 15 + 12"),
             fails_at=2, message_contains="stayed 27"),
        dict(why="adds the counts, not the costs",
             code=_supply("supply_total = chalk_count + oil_count"),
             fails_at=2, message_contains="how many, not costs"),
        dict(why="the line total in the chalk price box",
             code="chalk_count = 3\nchalk_price = 15\noil_count = 4\noil_price = 3\nsupply_total = 0\nprint(supply_total)\n",
             fails_at=1, message_contains="all 3 sticks"),
        dict(why="the earlier exercise's map names (the Example's names)",
             code="map_count = 3\nmap_price = 5\nchalk_count = 0\nchalk_price = 0\noil_count = 4\noil_price = 3\n"
             "supply_total = 0\nprint(supply_total)\n",
             fails_at=1, message_contains="new box `map_count`"),
    ],
    notes=(
        meta(starter_level="S4", path="pool", skills="combine-values", solo="false", dictates="",
             foreign_names="a,b,c,d") + "\n"
        "1C-T: the price-first twin (C9), for deferral time and the spaced queue. Chalk (not maps) so the twin "
        "never reuses the let-the-code-combine Example's names (map_count, map_price). Chalk 3 x 5 + oil 4 x 3 = "
        "27. CMB: one rerun changes both chalk boxes (5, 7 -> 47), one both oil boxes (9, 4 -> 51), so any typed "
        "number in the total fails."
    ),
)

EXTRA_1X_C = dict(
    kind="lesson",
    id="extra-math",
    title="Extra practice: Math",
    optional=True,
    minutes=6,
    summary="The short way to change a box, and one more shop to combine. For whenever you want it.",
    notes="1X-C pool (1C-05, 1C-T). Optional; feeds twins, the spaced queue and early finishers.",
    exercises=[THE_SHORT_WAY, COMBINE_AGAIN],
)

# ---------------------------------------------------------------------------------------------
# Quiz 1 "Chalk Quiz"
# ---------------------------------------------------------------------------------------------

QUIZ_1 = dict(
    kind="quiz",
    id="chalk-quiz",
    title="Chalk Quiz",
    minutes=8,
    summary="Eight questions on quotes, boxes, math and glue. Retake as often as you like.",
    notes="Quiz 1 (SC): 3 mc, 3 predict, 1 fill, 1 bug. Review order: right answers first (G1 R26).",
    questions=[
        dict(
            type="mc",
            id="make-a-box",
            q="Which line makes a box named `hero` that holds the text Lucky?",
            choices=['def ("hero")', '"hero" = "Lucky"', 'hero = "Lucky"', 'hero - "Lucky"'],
            answer=2,
            why_wrong={
                0: "`def` makes a recipe, not a box.",
                1: "A box's name never goes in quotes.",
                3: "`-` subtracts. To make a box, use `=`.",
            },
            explain="A box is `name = value`: the name with no quotes, `=`, then the text in quotes.",
            notes="WA evidence: A-02 def; A-04 dash; B-02/B-03 lone value.",
        ),
        dict(
            type="predict",
            id="mana-twice",
            q="What will this print?",
            code="mana = 18\nmana = mana - 5\nmana = mana - 5\nprint(mana)\n",
            choices=["8", "13", "18", "28"],
            answer="8",
            explain="Each line uses what is in the box now: 18, then 13, then 8. The box keeps only its latest value.",
        ),
        dict(
            type="bug",
            id="not-a-compass",
            q="This line should show It is not a compass. Mend it.",
            code='print("It is not a compass)\n',
            fix='print("It is not a compass")\n',
            expected_output="It is not a compass",
            explain="Quotes come in pairs. Add the closing `\"` before the `)`.",
        ),
        dict(
            type="predict",
            id="stamp-a-bar",
            q="What will this print?",
            code='print("█" * 2 + "░" * 3)\n',
            choices=["██░░░", "█2░3", "█░", "an error"],
            answer="██░░░",
            explain="`*` stamps each text: two full blocks, then three light blocks, glued with `+`.",
        ),
        dict(
            type="fill",
            id="glue-a-number",
            q="Fill the blank so this prints `Mana: 7`.",
            code='print("Mana: " + ___(7))\n',
            answer="str",
            expected_output="Mana: 7",
            explain="`str(7)` turns the number into text, so it can be glued to `\"Mana: \"`.",
        ),
        dict(
            type="mc",
            id="which-total-stays-right",
            q="Mar'tu changes `lantern_count` to 5. Which `total` line stays right?",
            code="lantern_count = 5\nlantern_price = 4\nrope_cost = 10\n",
            choices=[
                "total = 22",
                "total = 12 + 10",
                "total = lantern_count * lantern_price + rope_cost",
                "total = 3 * 4 + 10",
            ],
            answer=2,
            why_wrong={
                0: "22 was worked out by hand for 3 lanterns. It does not change when the count does.",
                1: "12 was the old lantern cost, typed in. It does not follow the box.",
                3: "3 is the old count, typed in. Use the box `lantern_count`.",
            },
            explain="Only the line built from the boxes follows when a box changes. Let the code combine it.",
        ),
        dict(
            type="mc",
            id="names-are-exact",
            q="What happens when this runs?",
            code="Health = 100\nprint(health)\n",
            choices=["It prints 100.", "It prints health.", "Python stops: `health` is not defined."],
            answer=2,
            why_wrong={
                0: "The box is named `Health`, with a capital H. `health` is a different name.",
                1: "No quotes, so Python looks for a box named `health`. It does not show the word.",
            },
            explain="Names are exact, letter for letter. `Health` and `health` are two different names.",
        ),
        dict(
            type="predict",
            id="times-before-plus",
            q="What will this print?",
            code="rope_count = 5\nrope_price = 2\nprint(rope_count * rope_price + 2)\n",
            choices=["12", "20", "10", "9"],
            answer="12",
            explain="Python does `*` before `+`: 5 times 2 is 10, then plus 2 is 12.",
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Project 1P1 "The Night Watch Ledger"
# ---------------------------------------------------------------------------------------------

LEDGER_STARTER = (
    "# A. What we know\n"
    "hours_until_burst = 0\n"
    "mana_per_hour = 0\n"
    "oil_per_hour = 0\n"
    "oil_price = 0\n"
    "\n"
    "# B. Let the code combine it\n"
    "mana_needed = 0\n"
    "oil_needed = 0\n"
    "oil_cost = 0\n"
    "\n"
    "# C. Write the ledger\n"
    'watch_keeper = ""  # any hero, in quotes\n'
)

LEDGER_A1 = "# A. What we know\nhours_until_burst = 37\n"
LEDGER_A1_32 = "# A. What we know\nhours_until_burst = 32\n"  # the last task: Bomb Shell's thirty-two hours
LEDGER_A2 = "mana_per_hour = 2\noil_per_hour = 1\noil_price = 3\n"
LEDGER_A2_ZERO = "mana_per_hour = 0\noil_per_hour = 0\noil_price = 0\n"
LEDGER_B3 = "\n# B. Let the code combine it\nmana_needed = hours_until_burst * mana_per_hour\n"
LEDGER_B3_ZERO = "\n# B. Let the code combine it\nmana_needed = 0\n"
LEDGER_B4 = "oil_needed = hours_until_burst * oil_per_hour\noil_cost = oil_needed * oil_price\n"
LEDGER_B4_ZERO = "oil_needed = 0\noil_cost = 0\n"
LEDGER_C = "\n# C. Write the ledger\n"
LEDGER_C5 = 'print("Mana for the barrier: " + str(mana_needed))\n'
LEDGER_C6 = 'print("Lantern oil: " + str(oil_needed) + " flasks for " + str(oil_cost) + " coins")\n'
LEDGER_C7_EMPTY = 'watch_keeper = ""  # any hero, in quotes\n'


def _c7(hero):
    return f'watch_keeper = "{hero}"  # any hero, in quotes\nprint("First watch: " + watch_keeper)\n'


LEDGER_AT_37 = LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C6 + _c7("Captain Glug")
LEDGER_SOLUTION = LEDGER_AT_37.replace(LEDGER_A1, LEDGER_A1_32)
LEDGER_KNOWN = ["hours_until_burst", "mana_per_hour", "oil_per_hour", "oil_price", "mana_needed", "oil_needed",
                "oil_cost", "watch_keeper"]
OIL_LINE = "'Lantern oil: ' + str(%s) + ' flasks for ' + str(%s) + ' coins'"
LEDGER_FIX = "Build it from the boxes, so the ledger follows when the hours change."


def _ledger(a1=LEDGER_A1, a2=LEDGER_A2, b3=LEDGER_B3, b4=LEDGER_B4, c5=LEDGER_C5, c6=LEDGER_C6, c7=None):
    return a1 + a2 + b3 + b4 + LEDGER_C + c5 + c6 + (c7 if c7 is not None else _c7("Bomb Shell"))


# Any hero passes (lint e). When it does not, say why without ever repeating the hero back (privacy, 2.11):
# a near-miss name (NAME), a lone value (BARE), the hero in another box (NEWBOX / a hint's `guard`), no quotes.
WATCH_KEEPER_CHECK = (
    "watch_keeper holds a hero",
    _NAMES_PRE + (
        f"_known = {LEDGER_KNOWN!r}\n"
        "_have = _g.get('watch_keeper')\n"
        "_ok = type(_have).__name__ == 'str' and _have.strip() != ''\n"
        "_msg = ''\n"
        "if not _ok:\n"
        "    _near = [_m for _m in _made if _m not in _known and _close(_m, 'watch_keeper')]\n"
        "    _newb = [_m for _m in _made if _m not in _known and type(_g.get(_m)).__name__ == 'str' and _g[_m].strip()]\n"
        "    if _near:\n"
        "        _msg = 'Python matches names letter for letter: you wrote `' + _near[0] + '`, the task needs `watch_keeper`.'\n"
        "    elif _bare:\n"
        "        _msg = 'Line ' + str(_bare[0]) + ' is a value with no box, so Python made it and forgot it. "
        "Put `watch_keeper = ` in front of it.'\n"
        "    elif _newb:\n"
        "        _msg = 'Your new box `' + _newb[0] + '` holds the hero, but `watch_keeper` is still empty. "
        "Put the hero in `watch_keeper`.'\n"
        "    elif 'watch_keeper' not in _g:\n"
        "        _msg = 'Make a box named `watch_keeper`: start a line with `watch_keeper = `.'\n"
        "    elif type(_have).__name__ != 'str':\n"
        "        _msg = '`watch_keeper` should hold a hero, in quotes.'\n"
        "    else:\n"
        "        _msg = '`watch_keeper` holds empty quotes. Put any hero between them, or use Mar' + chr(39) + 'tu' + "
        "chr(39) + 's pick.'\n"
        "assert _ok, _msg\n"
    ),
)

PROJECT_1P1 = dict(
    kind="project",
    id="night-watch-ledger",
    title="The Night Watch Ledger",
    minutes=19,
    summary="Mar'tu's ledger for the long night: mana for the barrier, oil for the lanterns, and who keeps watch.",
    intro=(
        "The barrier must hold until the next burst, 37 hours away. Mar'tu keeps a ledger of what the night will "
        "cost: mana for the barrier, and flasks of lantern oil.\n"
        "Three parts, in order: A. what we know, B. let the code combine it, C. write the ledger.\n"
        "The barrier eats 2 mana an hour. The lanterns burn 1 flask of oil an hour, and a flask costs 3 coins."
    ),
    martu=(
        "Thirty-seven hours, yes? I do not want to do these sums by hand at 3 in the morning. "
        "Put what we know in boxes, let the code combine them, then write the ledger lines. "
        "If the clock changes its mind, the ledger follows."
    ),
    names=["hours_until_burst", "mana_per_hour", "oil_per_hour", "oil_price", "mana_needed", "oil_needed",
           "oil_cost", "watch_keeper", "str"],
    pick='"Bomb Shell"',
    starter=LEDGER_STARTER,
    checkpoints=[
        dict(
            id="hours-until-burst",
            text="A. Make `hours_until_burst` hold 37.",
            dictated=True,
            hints=[
                "Change the 0 after `hours_until_burst = ` to 37.",
                "Look under `# A. What we know`, line 2.",
                "A box gets a number with `name = value`, no quotes: `steps = 12`.",
            ],
            checks=[
                # 32 is accepted too, so this task stays green after the last task (thirty-two-hours).
                slot("hours_until_burst is 37", "hours_until_burst",
                     "(32 if globals().get('hours_until_burst') == 32 else 37)", known=LEDGER_KNOWN,
                     default="The burst is 37 hours away: `hours_until_burst = 37`."),
            ],
        ),
        dict(
            id="what-we-know",
            text="A. Fill in the other three boxes from the story: mana per hour, flasks per hour, and the price of one flask.",
            dictated=False,
            hints=[
                "Start like this: `mana_per_hour = 2`. The other two numbers are in the story too.",
                "The barrier eats 2 mana an hour. The lanterns burn 1 flask an hour. A flask costs 3 coins.",
                "Each box gets its own number: how much per hour, or how much is one.",
            ],
            checks=[
                slot("mana_per_hour is 2", "mana_per_hour", "2", known=LEDGER_KNOWN,
                     default="The barrier needs 2 mana each hour: `mana_per_hour = 2`."),
                (
                    "oil boxes are not swapped",
                    "assert not (oil_per_hour == 3 and oil_price == 1), "
                    "'You swapped them: 1 is how many flasks burn each hour, 3 is the price of one flask.'",
                ),
                slot("oil_per_hour is 1", "oil_per_hour", "1", known=LEDGER_KNOWN,
                     default="The lanterns burn 1 flask each hour: `oil_per_hour = 1`."),
                slot("oil_price is 3", "oil_price", "3", known=LEDGER_KNOWN,
                     default="One flask costs 3 coins: `oil_price = 3`."),
            ],
        ),
        dict(
            id="mana-needed",
            text="B. Make `mana_needed` from the hours and the mana per hour.",
            dictated=False,
            hints=[
                "Start like this: `mana_needed = hours_until_burst * `",
                "2 mana for each of 37 hours. Which two boxes hold those?",
                "If `days = 3` and `meals_per_day = 2`, then `days * meals_per_day` is 6 meals.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                set_once("each box is set once, at the top", ["hours_until_burst", "mana_per_hour"]),
                slot("mana_needed multiplies the boxes", "mana_needed", "hours_until_burst * mana_per_hour",
                     known=LEDGER_KNOWN, foreign=["days", "meals_per_day"],
                     rules=[
                         ("_have == hours_until_burst + mana_per_hour",
                          "You added. The barrier needs 2 mana for each hour: multiply with `*`."),
                         # LINE-TOTAL (no numbers in the message: the hours change in the last task).
                         ("_have in (hours_until_burst * hours_until_burst * mana_per_hour, "
                          "mana_per_hour * hours_until_burst * mana_per_hour)",
                          "That multiplies by a total that is already worked out. Multiply the hours by the mana for "
                          "ONE hour: `hours_until_burst * mana_per_hour`."),
                     ],
                     default="Make `mana_needed` from `hours_until_burst` and `mana_per_hour`."),
                rerun_box("mana_needed follows the hours", {"hours_until_burst": 32, "mana_per_hour": 3}, "mana_needed",
                          "_R('hours_until_burst') * _R('mana_per_hour')", LEDGER_FIX),
            ],
            pass_line="Gearshift: Math checks out.",
        ),
        dict(
            id="oil-needed-and-cost",
            text="B. Make `oil_needed` from the hours, then `oil_cost` from the flasks and the price.",
            dictated=False,
            hints=[
                "Start like this: `oil_needed = hours_until_burst * `",
                "Flasks: hours times flasks per hour. Coins: flasks times the price of one.",
                "If `bags = 4` and `bag_price = 5`, then `bags * bag_price` is 20 coins.",
            ],
            checks=[
                loose_math("the math is kept in a box"),
                set_once("each box is set once, at the top", ["hours_until_burst", "oil_per_hour", "oil_price"]),
                slot("oil_needed multiplies the boxes", "oil_needed", "hours_until_burst * oil_per_hour",
                     known=LEDGER_KNOWN, foreign=["bags", "bag_price"],
                     default="Make `oil_needed` from `hours_until_burst` and `oil_per_hour`."),
                slot("oil_cost multiplies the boxes", "oil_cost", "hours_until_burst * oil_per_hour * oil_price",
                     known=LEDGER_KNOWN, foreign=["bags", "bag_price"],
                     rules=[
                         # LINE-TOTAL: the flasks times the whole oil cost (or the price times it).
                         ("_have in (hours_until_burst * oil_per_hour * hours_until_burst * oil_per_hour * oil_price, "
                          "oil_price * hours_until_burst * oil_per_hour * oil_price)",
                          "That multiplies by a total that is already worked out. Multiply the flasks by the price of "
                          "ONE flask: `oil_needed * oil_price`."),
                     ],
                     default="Make `oil_cost` from `oil_needed` and `oil_price`."),
                rerun_box("oil_needed follows the boxes", {"hours_until_burst": 32, "oil_per_hour": 2}, "oil_needed",
                          "_R('hours_until_burst') * _R('oil_per_hour')", LEDGER_FIX),
                rerun_box("oil_cost follows the boxes", {"hours_until_burst": 32, "oil_per_hour": 2, "oil_price": 5}, "oil_cost",
                          "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')", LEDGER_FIX),
            ],
        ),
        dict(
            id="mana-line",
            text="C. Print `Mana for the barrier: 74`, built from the boxes.",
            dictated=False,
            hints=[
                "Start like this: `print(\"Mana for the barrier: \" + `",
                "The number comes from `mana_needed`. What does a number need before it can be glued?",
                "`\"Sips: \" + str(sips)` glues text and a box with a number in it.",
            ],
            checks=[
                out_line("prints the mana line", "'Mana for the barrier: ' + str(hours_until_burst * mana_per_hour)",
                         "Print `Mana for the barrier: ` glued to `str(mana_needed)`.", hide=own("watch_keeper")),
                rerun_line("the mana line follows the hours", {"hours_until_burst": 32, "mana_per_hour": 3},
                           "'Mana for the barrier: ' + str(_R('hours_until_burst') * _R('mana_per_hour'))", LEDGER_FIX,
                           hide=own("watch_keeper")),
            ],
        ),
        dict(
            id="oil-line",
            text="C. Print `Lantern oil: 37 flasks for 111 coins`, built from the boxes.",
            dictated=False,
            hints=[
                "Start like this: `print(\"Lantern oil: \" + str(oil_needed) + `",
                "Two numbers come from boxes: the flasks and the coins. Everything else is fixed words.",
                "`print(\"Lantern oil: \" + str(___) + \" flasks for \" + str(___) + \" coins\")`",
            ],
            checks=[
                out_line("prints the oil line",
                         OIL_LINE % ("hours_until_burst * oil_per_hour", "hours_until_burst * oil_per_hour * oil_price"),
                         "Print the oil line, glued from text, `str(oil_needed)` and `str(oil_cost)`.",
                         hide=own("watch_keeper")),
                rerun_line("the oil line follows the hours", {"hours_until_burst": 32, "oil_per_hour": 2, "oil_price": 5},
                           OIL_LINE % ("_R('hours_until_burst') * _R('oil_per_hour')",
                                       "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')"),
                           LEDGER_FIX, hide=own("watch_keeper")),
            ],
        ),
        dict(
            id="watch-keeper",
            text="C. Make `watch_keeper` hold any hero, in quotes. Print `First watch: ` with the hero after it.",
            dictated=False,
            hints=[
                "Put a hero between the quotes after `watch_keeper = `.",
                "Two lines: the box, then a `print` that glues `\"First watch: \"` to `watch_keeper`.",
                "`\"Guard: \" + guard` glues fixed words to the text inside the box `guard`.",
            ],
            checks=[
                WATCH_KEEPER_CHECK,
                out_line("prints the watch line", "'First watch: ' + watch_keeper",
                         "Print `First watch: ` glued to `watch_keeper`. For a hero named Tester, that is "
                         "`First watch: Tester`.", privacy=True,
                         spaces="Check the spaces: one after the colon, like `First watch: Tester`."),
                rerun_line("the watch line is built from the box", {"watch_keeper": "Tester"}, "'First watch: Tester'",
                           "Glue `\"First watch: \"` to the box `watch_keeper`.", show=False),
                rerun_line("the watch line follows another hero", {"watch_keeper": "Zelda"}, "'First watch: Zelda'",
                           "Glue `\"First watch: \"` to the box `watch_keeper`.", show=False),
            ],
            pass_line="Mar'tu: Hm. Noted. First watch is theirs, then.",
        ),
        dict(
            id="thirty-two-hours",
            text=(
                "Bomb Shell studied the chalk wall: thirty-two hours, maybe less. Change only `hours_until_burst` to "
                "32 and run. Watch every ledger line follow."
            ),
            dictated=True,
            hints=[
                "Change line 2 to `hours_until_burst = 32`.",
                "Which box holds the hours? Change only that one.",
                "Change a box at the top, and every line built from it follows.",
            ],
            checks=[
                set_once("the hours are set once, at the top", ["hours_until_burst"]),
                ("hours_until_burst is 32",
                 "assert hours_until_burst == 32, 'Change line 2 to `hours_until_burst = 32`, then run.'"),
                ("the mana line shows 64",
                 "assert 'Mana for the barrier: 64' in _lines(), 'With 32 hours, your mana line should print "
                 "`Mana for the barrier: 64`. Change only line 2, and keep the line built from `mana_needed`.'"),
                # Back to 37 inside the check: a line with 32 typed into it (e.g. `32 * mana_per_hour`) cannot follow.
                rerun_line("the mana line still follows the hours", {"hours_until_burst": 37},
                           "'Mana for the barrier: ' + str(_R('hours_until_burst') * _R('mana_per_hour'))",
                           "Change only line 2, and keep every ledger line built from the boxes.",
                           hide=own("watch_keeper")),
                rerun_line("the oil line still follows the hours", {"hours_until_burst": 37},
                           OIL_LINE % ("_R('hours_until_burst') * _R('oil_per_hour')",
                                       "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')"),
                           "Change only line 2, and keep every ledger line built from the boxes.",
                           hide=own("watch_keeper")),
            ],
            pass_line="Mar'tu: 64 mana, 32 flasks, 96 coins. You changed one box. The ledger did the rest.",
        ),
    ],
    solution=LEDGER_SOLUTION,
    partials=[
        LEDGER_A1 + LEDGER_A2_ZERO + LEDGER_B3_ZERO + LEDGER_B4_ZERO + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3_ZERO + LEDGER_B4_ZERO + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4_ZERO + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C6 + LEDGER_C7_EMPTY,
        LEDGER_AT_37,
    ],
    assemble=dict(
        lines=[
            "hours_until_burst = 32", "mana_per_hour = 2", "oil_per_hour = 1", "oil_price = 3",
            "mana_needed = hours_until_burst * mana_per_hour",
            "oil_needed = hours_until_burst * oil_per_hour", "oil_cost = oil_needed * oil_price",
            LEDGER_C5.strip(), LEDGER_C6.strip(), 'watch_keeper = "Bomb Shell"', 'print("First watch: " + watch_keeper)',
        ],
        distractors=["mana_needed = 64", 'print("Mana for the barrier: 64")',
                     'print("Mana for the barrier: " + mana_needed)'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The ledger page",
            text=(
                "```text\nA. what we know        37 hours, 2 mana/hour, 1 flask/hour, 3 coins/flask\n"
                "B. let the code ...   mana_needed, oil_needed, oil_cost\nC. the ledger          three printed lines\n```\n"
                "Each part only uses boxes from the parts above it."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Fill the four boxes in A.\n2. In B, multiply: hours times per hour; flasks times price.\n"
                "3. In C, glue text and `str()` of each box.\n4. Run after every line."
            ),
        ),
        dict(
            angle="in Tor",
            label="Why a ledger?",
            text=(
                "The chalk wall says the next burst may come sooner: 32 hours, maybe. "
                "If you typed the answers, the whole ledger is wrong. If the code combines them, change one box."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, the bursts came closer: 48, then 37, then about 32 hours. "
                "Mar'tu's checks here try 32 hours to see if your ledger follows."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's side quest",
        text=(
            "Lucky wants his cut. Below the ledger:\n"
            "1. Make `glug_sips = 4`, a `glug_price` of your choice, and `glug_fee` built from them.\n"
            "2. Print a divider of 24 `~` marks, stamped with `*`.\n"
            "3. Make `total_coins`, the oil cost plus the glug fee, and print it.\n"
            "4. Print a reserve bar for `reserve = 4` of `reserve_max = 6`, like `[████░░]`."
        ),
        hints=[
            "Glug: `glug_fee = glug_sips * glug_price`. Divider: `print(\"~\" * 24)`.",
            "Bar: `\"[\" + \"█\" * reserve + \"░\" * (reserve_max - reserve) + \"]\"`.",
        ],
        checks=[
            ("glug fee is built from the boxes", "assert glug_fee == glug_sips * glug_price and glug_sips == 4, "
             "'Make `glug_sips = 4`, any `glug_price`, and `glug_fee = glug_sips * glug_price`.'"),
            rerun_box("glug fee follows the price", {"glug_price": 11}, "glug_fee", "_R('glug_sips') * 11",
                      "Build it from the boxes."),
            (
                "divider made with repetition",
                "import ast as _ast\n"
                "_tree = _ast.parse(_source)\n"
                "_stamped = [id(_s) for _n in _ast.walk(_tree) if type(_n).__name__ == 'BinOp' "
                "and type(_n.op).__name__ == 'Mult' for _s in (_n.left, _n.right)]\n"
                "_typed = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Constant' "
                "and type(_n.value).__name__ == 'str' and '~~' in _n.value and id(_n) not in _stamped]\n"
                "assert not _typed, 'Make the divider with repetition: `\"~\" * 24`. Typing the marks is how Lucky loses count.'\n"
                "assert '~' * 24 in _lines(), 'Print a divider of exactly 24 marks: `print(\"~\" * 24)`.'",
            ),
            (
                "total coins",
                "assert total_coins == oil_cost + glug_fee, 'Make `total_coins = oil_cost + glug_fee`.'\n"
                "assert any(str(total_coins) in _l for _l in _lines()), 'Print `total_coins`.'",
            ),
            rerun_box("total coins follows the hours", {"hours_until_burst": 30}, "total_coins",
                      "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price') + _R('glug_fee')",
                      "Build it from `oil_cost` and `glug_fee`."),
            rerun_line("reserve bar follows its boxes", {"reserve": 1, "reserve_max": 6}, "'[█░░░░░]'",
                       "Stamp `\"█\" * reserve`, then `\"░\" * (reserve_max - reserve)`.", hide=own("watch_keeper")),
        ],
        solution=LEDGER_SOLUTION + (
            "glug_sips = 4\nglug_price = 2\nglug_fee = glug_sips * glug_price\nprint(\"~\" * 24)\n"
            "total_coins = oil_cost + glug_fee\nprint(\"Coins tonight: \" + str(total_coins))\n"
            "reserve = 4\nreserve_max = 6\nprint(\"[\" + \"█\" * reserve + \"░\" * (reserve_max - reserve) + \"]\")\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="thirty-two-hours",
        why=(
            "You have seen this moment: Bomb Shell studied the chalk wall and said thirty-two hours, maybe less. "
            "A ledger built from boxes is ready for that news. Change one number."
        ),
    ),
    takeaway="A ledger built from boxes follows when one box changes: change the hours, every line follows.",
    wrong_answers=[
        dict(why="mana_needed typed (everyone's 68)", code=_ledger(b3="\nmana_needed = 74\n"),
             fails_at=3, message_contains="32"),
        dict(why="a ledger line typed", code=_ledger(c5='print("Mana for the barrier: 74")\n'),
             fails_at=5, message_contains="32"),
        dict(why="oil cost skips the flasks per hour",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = hours_until_burst * oil_price\n"),
             fails_at=4, message_contains="oil_per_hour"),
        dict(why="a number glued without str()", code=_ledger(c5='print("Mana for the barrier: " + mana_needed)\n'),
             fails_at=0, message_contains="concatenate"),
        dict(why="oil boxes swapped", code=_ledger(a2="mana_per_hour = 2\noil_per_hour = 3\noil_price = 1\n"),
             fails_at=2, message_contains="swapped"),
        dict(why="capital letter in a name",
             code=_ledger(a1="# A. What we know\nhours_until_burst = 0\nHours_until_burst = 37\n"),
             fails_at=1, message_contains="letter for letter"),
        dict(why="hero with no quotes", code=_ledger(c7='watch_keeper = Bomb Shell\nprint("First watch: " + watch_keeper)\n'),
             fails_at=0, message_contains="SyntaxError"),
        dict(why="a lone hero with no box",
             code=_ledger(c7='watch_keeper = ""\n"Bomb Shell"\nprint("First watch: " + watch_keeper)\n'),
             fails_at=7, message_contains="no box"),
        dict(why="the watch line typed", code=_ledger(c7='watch_keeper = "Bomb Shell"\nprint("First watch: Bomb Shell")\n'),
             fails_at=7, message_contains="Tester"),
        dict(why="the oil line with a missing space",
             code=_ledger(c6='print("Lantern oil: " + str(oil_needed) + "flasks for " + str(oil_cost) + " coins")\n'),
             fails_at=6, message_contains="space"),
        dict(why="mana per hour typed into mana_needed (passes an hours-only rerun)",
             code=_ledger(b3="\n# B. Let the code combine it\nmana_needed = hours_until_burst * 2\n"),
             fails_at=3, message_contains="mana_per_hour = 3"),
        dict(why="oil price typed into oil_cost (passes an hours-only rerun)",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = oil_needed * 3\n"),
             fails_at=4, message_contains="oil_price = 5"),
        dict(why="gaming the message: the typed watch line plus the Tester line the message showed",
             code=_ledger(c7='watch_keeper = "Bomb Shell"\nprint("First watch: Bomb Shell")\nprint("First watch: Tester")\n'),
             fails_at=7, message_contains="typed in"),
        dict(why="gaming: the hero set to the rerun's Tester, then the watch line typed",
             code=_ledger(c7='watch_keeper = "Tester"\nprint("First watch: Tester")\n'), fails_at=7, message_contains="Zelda"),
        dict(why="the hint's name copied: the hero in `guard`, watch_keeper left empty",
             code=_ledger(c7='watch_keeper = ""\nguard = "Bomb Shell"\nprint("First watch: " + guard)\n'),
             fails_at=7, message_contains="new box `guard`"),
        dict(why="capital letter: Watch_keeper",
             code=_ledger(c7='watch_keeper = ""\nWatch_keeper = "Bomb Shell"\nprint("First watch: " + Watch_keeper)\n'),
             fails_at=7, message_contains="letter for letter"),
        dict(why="a number in quotes", code=_ledger(a1='# A. What we know\nhours_until_burst = "37"\n'),
             fails_at=1, message_contains="quotes"),
        dict(why="a one-word hero with no quotes (A-08 kratos)",
             code=_ledger(c7='watch_keeper = Kratos\nprint("First watch: " + watch_keeper)\n'),
             fails_at=0, message_contains="not defined"),
        dict(why="def used to make the box (A-02)",
             code=_ledger(c7='def watch_keeper = "Bomb Shell"\nprint("First watch: " + watch_keeper)\n'),
             fails_at=0, message_contains="SyntaxError"),
        dict(why="the closing quote missing (A-02/A-03/A-04)",
             code=_ledger(c7='watch_keeper = "Bomb Shell\nprint("First watch: " + watch_keeper)\n'),
             fails_at=0, message_contains="SyntaxError"),
        dict(why="the mana line built from the hours and a typed 2, skipping mana_needed",
             code=_ledger(c5='print("Mana for the barrier: " + str(hours_until_burst * 2))\n'),
             fails_at=5, message_contains="mana_per_hour = 3"),
        dict(why="LINE-TOTAL: the hours times the mana total 74",
             code=_ledger(b3="\n# B. Let the code combine it\nmana_needed = hours_until_burst * 74\n"),
             fails_at=3, message_contains="already worked out"),
        dict(why="LINE-TOTAL: the flasks times the oil total 111",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = oil_needed * 111\n"),
             fails_at=4, message_contains="price of ONE flask"),
        dict(why="the last task not done: the hours still 37", code=_ledger(), fails_at=8,
             message_contains="`hours_until_burst = 32`"),
        dict(why="the last task as a new line at the bottom (side-work habit): the ledger never sees 32",
             code=_ledger() + "hours_until_burst = 32\n", fails_at=3, message_contains="top down"),
        dict(why="the last task changes the wrong box (mana_per_hour to 32)",
             code=_ledger(a2="mana_per_hour = 32\noil_per_hour = 1\noil_price = 3\n"), fails_at=2,
             message_contains="2 mana each hour"),
        dict(why="after the change, 64 typed into mana_needed",
             code=_ledger(a1=LEDGER_A1_32, b3="\n# B. Let the code combine it\nmana_needed = 64\n"),
             fails_at=3, message_contains="stayed 64"),
        dict(why="after the change, the hours typed into mana_needed (passes every rerun at 32)",
             code=_ledger(a1=LEDGER_A1_32, b3="\n# B. Let the code combine it\nmana_needed = 32 * mana_per_hour\n"),
             fails_at=8, message_contains="`hours_until_burst = 37`"),
        dict(why="after the change, the hours typed into oil_needed (passes every rerun at 32)",
             code=_ledger(a1=LEDGER_A1_32, b4="oil_needed = 32 * oil_per_hour\noil_cost = oil_needed * oil_price\n"),
             fails_at=8, message_contains="Lantern oil: 37 flasks for 111 coins"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="combine-values,concat-str,make-variable", solo="false",
             dictates="1,8", foreign_names="days,meals_per_day,bags,bag_price,guard,steps,sips") + "\n"
        "Starter: the task-group headers (always) plus the `= 0` placeholders, because 'Show me more' is the "
        "default preset and the prototype has one starter. CMB: every combine task and ledger line is rerun with "
        "hours_until_burst = 32 and every other input it reads changed too (mana_per_hour 3; oil_per_hour 2, "
        "oil_price 5), so `hours_until_burst * 2` or `oil_needed * 3` fail. C5/C6 diffs hide lines holding the hero. Lint (e): the solution "
        "uses Captain Glug, the assemble lines use Mar'tu's pick (Bomb Shell); the watch line check never echoes "
        "the hero (Tester only). Echo spot: the site would repeat the hero in the pass line through the blocklist; "
        "a static pass_line cannot, so it says 'Noted'. Side quest WA (typed ~~~ divider -> 'repetition') is "
        "proven by the u01c self-test, since harness wrong_answers only run against the main checkpoints. "
        "Trial mode (after a QC1 pass) is a site feature, not in this prototype. "
        "The story numbers (2 mana, 1 flask, 3 coins) are in the intro, so task A2 is not dictated (find them). "
        "LINE-TOTAL rules on mana_needed and oil_cost name no numbers, because the hours change in the last task. "
        "Last task (thirty-two-hours) mirrors the 1000 ropes: Bomb Shell's 32 hours, change one box, every line "
        "follows (64 / 32 / 96). So every task can pass in one run, task 1 accepts 37 or 32, and the solution "
        "uses 32 (the ledger at 37 is the last partial). set_once on tasks 3, 4 and 8 gives `hours_until_burst = 32` "
        "added at the bottom a top-down message (task 8's copy matters on the site, where task 3 stays green from "
        "an earlier run). Task 8 reruns at 37: a line with 32 typed into it cannot follow. The side quest's total "
        "reruns at 30 hours (the finished ledger is already at 32)."
    ),
)

ITEMS = [REMEMBERS_1C, LESSON_1C, EXTRA_1X_C, QUIZ_1, PROJECT_1P1]
