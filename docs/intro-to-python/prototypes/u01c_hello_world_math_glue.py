"""Unit 1 "Hello World", part c: Lesson 1C "Math and Glue", Extra practice 1X-C, Quiz 1 "Chalk Quiz" and
Project 1P1 "The Night Watch Ledger".

Spec: design/curriculum.md, "## Unit 1", items 6 to 9 (1c-remembers; 1C-01 to 1C-04, 1C-06 to 1C-09, 1C-S;
1C-05 and 1C-T in the pool; Quiz 1; Project 1P1). Introduces op:Add, op:Sub, op:Mult, op:Div (1C-01),
call:str (1C-06) and node:AugAssign (1C-05, pool only: no core code shows `+=`).

Who this is for: the class already played campaign Modules 1 and 2 and struggled most with exactly this part:
nobody let the code combine values (everyone hard-coded 68), counts and prices were swapped, and `mana-bars` /
`hold-the-barrier` felt like a wall. So every combine step is checked by BEHAVIOR: the check re-runs the
student's program with other numbers (CMB, curriculum 2.5). The message gives the one fix first, then the
labelled evidence (plain-language guide 4.3): "`total_cost` has a typed-in number. Use the box names, not
numbers: `lantern_cost + rope_cost`. Mar'tu tested your code with a test number, `lantern_count = 7`:
`total_cost` should be 38, but it stayed 22. Don't type the test number." Mar'tu says once, in chalk-math, that
he tests the line with other numbers, like a formula.

Check builders below (plain string templates, no student values ever echoed back):
  slot()        NAME / LEFT / NEWBOX / BARE / TEXT-vs-NUM plus per-exercise rules, for one box's value
  story_pair()  SWAP / LINE-TOTAL / wild count / placeholder / NEWBOX, for a count box and a price box from a story
                (a right pair always passes; the diagnosis runs only when it is wrong; swap_extra adds to SWAP)
  rerun()       CMB: re-runs _source with some input lines changed (the "Try other numbers" mechanism). Every
                input a combine line reads is changed by at least one rerun, so no half-typed line survives.
                When the rerun stops with an error, the message says so in plain words (_plain: "line 4 glues
                text and a number with `+`"), never Python's raw error (guide 4.3.6, S8).
  rerun_line()  CMB on output. The wanted line must come from a line that CHANGED with the inputs: a line that
                prints the same in both runs is typed in (stops `print(11)` + `print(7)` after the message shows 7).
                word=True accepts labelled output (`The gap shrank by 7` holds 7 as a whole number); starts=True
                accepts a line that starts with the wanted text (glue-words' first bead, `Tester has`).
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
TEXT_NOT_NUM = "`%s` holds text, because of the quotes. Numbers don't get quotes: take them off."

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
    "import ast as _ast, io as _io, re as _re, sys as _sys\n"
    # What stopped a rerun, in plain words (guide 4.3.6, S8): the student's line number, then what it tried.
    "def _plain(_x):\n"
    "    _t, _s = type(_x).__name__, str(_x)\n"
    "    _tb, _at = _x.__traceback__, None\n"
    "    while _tb is not None:\n"
    "        if _tb.tb_frame.f_code.co_filename == 'main.py':\n"
    "            _at = _tb.tb_lineno\n"
    "        _tb = _tb.tb_next\n"
    "    _where = ('line ' + str(_at)) if _at else 'one line'\n"
    "    if _t == 'NameError':\n"
    "        _m = _re.search(r\"'(\\w+)'\", _s)\n"
    "        return _where + ' uses `' + (_m.group(1) if _m else '?') + '`, but no box has that exact name'\n"
    "    if _t == 'ZeroDivisionError':\n"
    "        return _where + ' divides by 0'\n"
    "    if _t == 'TypeError' and ('concatenate' in _s or (\"'str'\" in _s and '+' in _s)):\n"
    "        return _where + ' glues text and a number with `+`'\n"
    "    if _t == 'TypeError' and 'multiply sequence' in _s:\n"
    "        return _where + ' repeats text by something that is not a whole number'\n"
    "    if _t == 'TypeError':\n"
    "        return _where + ' does math with text'\n"
    "    return _where + ' could not finish'\n"
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
    "        _err = _plain(_x)\n"
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


def _test_words(changes):
    """How a rerun's made-up values are named in its message (curriculum 2.5; plain-language guide 4.3.3):
    ("a test number", "the test number", "Don't type the test number.")."""
    names = [value for value in changes.values() if isinstance(value, str)]
    count = len(changes) - len(names)
    nums = "a test number" if count == 1 else "test numbers"
    the_nums = "the test number" if count == 1 else "the test numbers"
    if not names:
        return nums, the_nums, "Don't type %s." % the_nums
    if not count:
        return "a made-up name", "the made-up name", "Don't type %s." % " or ".join(names)
    return ("a made-up name and " + nums, "them", "Don't type %s or %s." % (" or ".join(names), the_nums))


def rerun(label, changes, pre, cond, msg, fix):
    """CMB. Re-runs the student's program with `changes` swapped in, inside the check only (the student's own
    code and numbers are never touched). `pre` sets up names from the rerun (_r its namespace, _R = _r.get, _p its
    printed lines); `cond` must hold. The message puts the one thing to try first, then the labelled evidence
    (plain-language guide 4.3): `fix` (plain words, the step's own names), then "Mar'tu tested your code with a test
    number, `last_gap = 41`: " + `msg` (an expression: what the rerun should show, and what it showed), then
    "Don't type the test number." A rerun that stops with an error says what stopped it in plain words
    (_plain), never Python's raw error (guide 4.3.6, S8)."""
    kind = "number" if all(isinstance(v, int) for v in changes.values()) else "value"
    what, _, tail = _test_words(changes)
    lead = " Mar'tu tested your code with %s, %s: " % (what, _with_text(changes))
    keep = " = ` and a " + kind + " on a line of its own. Mar'tu tests your code by changing that line."
    crash = "Your code stopped when Mar'tu tested it with %s, %s: " % (what, _with_text(changes))
    crash_end = ". It has to work for other %ss too." % kind
    code = _RERUN_DEF + (
        f"_r, _p, _f, _e = _rerun({changes!r})\n"
        "_R = _r.get\n"
        "_g0 = globals()\n"
        f"_miss = [_k for _k in {list(changes)!r} if _k not in _f]\n"
        "assert not _miss or _miss[0] in _g0, 'Make a box named `' + (_miss[0] if _miss else '') + "
        "'`: start a line with `' + (_miss[0] if _miss else '') + ' = `.'\n"
        f"assert not _miss, 'Keep `' + (_miss[0] if _miss else '') + {keep!r}\n"
        f"assert not _e, {crash!r} + _e + {crash_end!r}\n"
        f"{pre}\n"
        f"assert {cond}, {fix!r} + {lead!r} + {msg} + ' ' + {tail!r}\n"
    )
    return (label, code)


def rerun_box(label, changes, target, want, fix):
    """CMB on one box: after the rerun, `target` must equal `want` (an expression over _R)."""
    return rerun(
        label,
        changes,
        f"_want = {want}\n_got = _R({target!r})\n_was = _g0.get({target!r})",
        "_got == _want and type(_got).__name__ == type(_want).__name__",
        f"'`{target}` should be ' + str(_want) + ', but it ' + ('stayed ' if _got == _was else 'became ') + str(_got) + '.'",
        fix,
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
        "(', but it showed nothing' if not _p else ('' if (_hide and _hide in _nn) else ', but it showed `' + _nn + '` instead'))"
        if show
        else "''"
    )
    the_what = _test_words(changes)[1]
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
            "('your line that starts with `' + _want + '` shows the same with or without " + the_what
            + ", so it is typed in.')"
        )
        should = f"('it should show a line that starts with `' + _want + '`' + {shown} + '.')"
    else:
        typed = "('your line `' + _want + '` shows the same with or without " + the_what + ", so it is typed in.')"
        should = f"('it should show `' + _want + '`' + {shown} + '.')"
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
        f"({typed} if _at else {should})",
        fix,
    )


def slot(label, name, want, *, known, default, foreign=(), rules=(), step="step"):
    """One box must hold `want` (an expression over the student's names). The message says why not:
    a rule (rules = [(condition, message)]), text instead of a number, a near-miss name (NAME), an example's
    name (LEFT), a new box holding the answer (NEWBOX), a lone value (BARE), or the default.
    `step` is what the screen calls it: "step", or "task" in a project."""
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
        f"    _msg = 'Your box is named `' + _near[0] + {'`, but this ' + step + ' needs `' + name + '`. Names match letter for letter, capitals too.'!r}\n"
        "if not _ok and not _msg and _left:\n"
        f"    _msg = '`' + _left[0] + {'` is a name from the Example or an earlier ' + step + '. This ' + step + ' needs the box `' + name + '`: use that name instead.'!r}\n"
        "if not _ok and not _msg and _newb:\n"
        f"    _msg = 'Your new box `' + _newb[0] + '` holds ' + str(_want) + ', but `{name}` ' + "
        f"('still holds ' + str(_have) if _name in _g else 'is not made yet') + {'. This ' + step + ' needs the name `' + name + '`: use it instead of the new name.'!r}\n"
        "if not _ok and not _msg and _name not in _g and _bare:\n"
        f"    _msg = 'Line ' + str(_bare[0]) + {' is a value with no name in front, so Python reads it and throws it away, like a phone number saved with no contact name. Put `' + name + ' = ` in front of it.'!r}\n"
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
    swap = "You swapped them: %d is how many %s, and %d is the price of one." % (count, things, price)
    if price_first:
        swap += " This story gives the price first."
    swap += swap_extra
    line_total = "%d is already the cost of all %d %s. `%s` needs the price of one." % (
        count * price, count, things, price_name)
    count_total = "%d is already the cost of all %d %s. `%s` needs how many." % (
        count * price, count, things, count_name)
    code = _NAMES_PRE + (
        f"_names = {[count_name, price_name]!r}\n"
        f"_known = {list(known)!r}\n"
        f"_wants = {{{count_name!r}: {count}, {price_name!r}: {price}}}\n"
        "_num = lambda _v: type(_v).__name__ in ('int', 'float')\n"
        "_ok = all(_w in _g and _num(_g[_w]) and _g[_w] == _wants[_w] for _w in _names)\n"
        "_msg = ''\n"
        "_near = [(_m, _w) for _w in _names for _m in _made if _m not in _known and _m not in _names and _close(_m, _w)]\n"
        "if not _ok and _near:\n"
        "    _msg = 'Your box is named `' + _near[0][0] + '`, but this step needs `' + _near[0][1] + '`. "
        "Names match letter for letter, capitals too.'\n"
        "for _w in _names:\n"
        "    if not _ok and not _msg and _w not in _g and _bare:\n"
        "        _msg = 'Line ' + str(_bare[0]) + ' is a value with no name in front, so Python reads it and throws it "
        "away, like a phone number saved with no contact name. Put `' + _w + ' = ` in front of it.'\n"
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
        "'` still holds 0. Put the number in `' + _newb[0][1] + '` instead.'\n"
        f"    elif _c not in (0, {count}, {price}):\n"
        f"        _msg = {wild!r}\n"
        "    elif _c == 0 or _p == 0:\n"
        f"        _msg = '`' + ({count_name!r} if _c == 0 else {price_name!r}) + '` still holds the placeholder 0. "
        "Replace the 0 with the number from the story in the `#` note.'\n"
        f"    elif _c != {count}:\n"
        f"        _msg = {'`' + count_name + '` answers how many ' + things + '. Read the story in the `#` note again: which number is how many?'!r}\n"
        "    else:\n"
        f"        _msg = {'`' + price_name + '` answers how much one costs. Read the story in the `#` note again: which number is the price of one?'!r}\n"
        "assert _ok, _msg\n"
    )
    return (label, code)


def out_line(label, want, missing, privacy=False, spaces="Check the spaces in your line: every space counts.", hide="''",
             early=None):
    """OUT diff: `want` (an expression) must be printed. Shows the nearest printed line and where it first
    differs, unless privacy=True (the line holds the student's own creative text). `hide` (an expression, e.g. a
    creative hero box) keeps other lines that hold the student's own text out of the diff. A line that is right so far
    but stops early says so first (never "a space is missing" for the space the next piece brings); `early` (the
    next thing to type, in the step's words) then follows "Your line stops after ...". The pass/fail is unchanged."""
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
        f"    _msg = 'Nothing shows in the Console yet. ' + {missing!r}\n"
        "elif _want not in _ls and not _cands:\n"
        f"    _msg = 'No line in the Console shows `' + _want + '` yet. ' + {missing!r}\n"
        "elif _want not in _ls:\n"
        "    _near = max(_cands, key=_pre)\n"
        "    _i = _pre(_near)\n"
        "    _shown = _near.replace('`', \"'\")\n"
        "    _head = 'Your line shows `' + _shown + '`, but it should show `' + _want + '`. '\n"
        "    _before = _want[:_i].strip()\n"
        "    if _i == 0:\n"
        "        _msg = _head + 'They are different from the very start. ' + " + repr(missing) + "\n"
        "    elif _i >= len(_near):\n"
        + ("        _msg = 'Your line stops after `' + _before + '`. ' + " + repr(early) + "\n" if early else
           "        _msg = _head + 'Your line stops early, right after `' + _before + '`.'\n") +
        "    elif _want[_i:_i + 1] == ' ' and _near[_i:_i + 1] != ' ':\n"
        "        _msg = _head + 'A space is missing right after `' + _before + '`.'\n"
        "    elif _near[_i:_i + 1] == ' ' and _want[_i:_i + 1] != ' ':\n"
        "        _msg = _head + 'There is an extra space right after `' + _before + '`.'\n"
        "    else:\n"
        "        _msg = _head + 'They are different right after `' + _before + '`.'\n"
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
        f"{' works out a new number, but `' + box + '` didn' + chr(39) + 't change, so Python throws the answer away. Put `' + box + ' = ` in front of that line.'!r}",
    )


def loose_math(label, box=None):
    """BARE for math: a line that works out a number but keeps it nowhere (`lantern_count * lantern_price` on its
    own raises no error, and the box keeps its 0). `box` is the step's own box, named in the one thing to try
    (guide 4.3.2: the step's own names, never a general shape to copy)."""
    fix = (" Put `%s = ` in front of that line." % box) if box else (
        " In front of that line, put the name of the box that should hold it, then `=`.")
    return (
        label,
        "import ast as _ast\n"
        "_loose = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'BinOp']\n"
        "assert not _loose, 'Line ' + str(_loose[0] if _loose else 0) + ' works out a number, but no box keeps the "
        "answer, so Python throws it away.' + " + repr(fix),
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
        "assert not _late, 'You put a new number in `' + (_late[0][0] if _late else '') + '` on line ' + "
        "str(_late[0][2] if _late else 0) + ', but the lines above it already used the old number. "
        "Python reads top to bottom. Change the number on line ' + str(_late[0][1] if _late else 0) + "
        "' instead, and delete line ' + str(_late[0][2] if _late else 0) + '.'",
    )


def near_names(label, names, known):
    """NAME on its own: a box whose name is a near miss of a required name (`Mana` for `mana`)."""
    return (
        label,
        _NAMES_PRE
        + f"_names = {list(names)!r}\n_known = {list(known)!r}\n"
        "_near = [(_m, _w) for _w in _names for _m in _made if _m not in _known and _m not in _names and _close(_m, _w)]\n"
        "assert not _near, 'Your box is named `' + (_near[0][0] if _near else '') + "
        "'`, but this step needs `' + (_near[0][1] if _near else '') + '`. Names match letter for letter, capitals too.'\n",
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
        "Tonight: how to say something, how to keep something in a box, and how to let Python do the math."
    ),
    goals=[
        "Make Python show words on the screen",
        "Write notes that Python skips",
        "Keep words or a number in a named box (a variable)",
        "Change what is in a box",
        "Let Python do the math with your boxes",
        "Join words and numbers into one line, and draw a mana bar from blocks",
        "Read Python's error messages and fix small mistakes",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="math signs",
        aliases=["math sign", "operator", "operators"],
        plain=(
            "The signs Python does math with: `+` plus, `-` minus, `*` times (×) and `/` divided by (÷). "
            "The keyboard has no × or ÷ key, so Python uses `*` and `/`."
        ),
        example="print(48 - 37)",
    ),
    dict(
        term="decimal",
        aliases=["decimals", "decimal number"],
        plain="A number with a decimal point, like `24.0` or `42.5`, as in math class. Dividing with `/` always gives one.",
        example="print(48 / 2)",
    ),
    dict(
        term="placeholder",
        aliases=["placeholders"],
        plain="A stand-in value, like a `0` in the code you start with. It holds the place until you put the real number there.",
        example="lantern_count = 0",
    ),
    dict(
        term="show your work",
        aliases=["show your working", "combine", "let the code combine it", "build it from the boxes"],
        plain=(
            "Write the math with box names, like `area = length * width`, instead of typing the answer, the way math "
            "class asks you to show your work. Then, when a box changes and you press Run again, the answer changes "
            "to match."
        ),
        example="area = length * width",
    ),
    dict(
        term="glue",
        aliases=["glues", "gluing", "concatenate", "concatenation"],
        plain=(
            "Join texts end to end with `+`, like a compound word: sun + flower is sunflower. Python adds no spaces, "
            "so put the spaces inside the quotes."
        ),
        example='"Shield" + " up."',
    ),
    dict(
        term="str()",
        aliases=["str"],
        plain=(
            "`str` is short for string, Python's word for text. `str(26)` gives the text `\"26\"`, which can be glued "
            "to other text."
        ),
        example='"Mana: " + str(26)',
    ),
    dict(
        term="stamp",
        aliases=["stamps", "repetition", "repeat a mark"],
        plain=(
            "`*` with text and a number repeats the text, like pressing a stamp that many times. In math, 3 × 4 means "
            "4 + 4 + 4, and `\"█\" * 3` means `\"█\" + \"█\" + \"█\"`: `███`."
        ),
        example='"█" * 3',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (1c-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_1C = dict(
    kind="quiz",
    id="1c-remembers",
    title="Quick review: 2 questions (not scored)",
    optional=True,
    minutes=1,
    summary="Two quick questions from earlier lessons, to warm up. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 1C; recall from 1B (box vs quoted name) and "
        "1A (closing quote). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="which-makes-a-box",
            q="Which line makes a box named `hero` that holds the text Lucky?",
            choices=['"hero" = "Lucky"', 'hero = "Lucky"'],
            answer=1,
            why_wrong={0: "A box's name never goes in quotes. In quotes, `\"hero\"` is only the letters h-e-r-o, "
                          "and letters can't hold a value."},
            explain="`hero = \"Lucky\"` makes a box named `hero` with Lucky inside: hero gets Lucky. " + QUOTES_RULE,
        ),
        dict(
            type="bug",
            id="mend-shield-up",
            q="Fix this line so it shows Shield up.",
            code='print("Shield up.)\n',
            fix='print("Shield up.")\n',
            expected_output="Shield up.",
            explain="Quotes come in pairs, like quotation marks in English class. Add the closing `\"` right after the period.",
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
        "Python does math with [[math signs]]: `+` (plus), `-` (minus), `*` (times: there's no × key) and `/` "
        "(divided by). `print(9 * 2)` shows 18.\n"
        "A gap is the hours between two bursts, blasts from the leylines. The first gap was 48, the last 37.\n"
        "In math, area = length × width works for any rectangle. Make your line a formula too: I test it with "
        "other numbers."
    ),
    introduces=["op:Add", "op:Sub", "op:Mult", "op:Div"],
    example="owl_hoots = 6\nwolf_howls = 3\nprint(owl_hoots + wolf_howls)\n",
    example_output="9",
    names=["first_gap", "last_gap"],
    predict=dict(
        q="What will these three lines show in the Console?",
        code="print(46 + 44)\nprint(48 - 37)\nprint(9 * 2)\n",
        choices=["90\n11\n18", "46 + 44\n48 - 37\n9 * 2", "90 11 18 all on one line"],
        answer=0,
        explain=(
            "Python works out each math problem and shows the answer, not the problem. Try it if you like (it's not "
            "a step): add `print(48 / 2)` and press Run. Dividing with `/` always gives a [[decimal]]: `24.0` is the "
            "same amount as 24."
        ),
    ),
    pair_talk=(
        "Pair talk: each of you picks an answer in the Predict first box, just above ▶ Run, without showing. "
        "Compare your picks, then each of you presses Run on your own screen."
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
            text=(
                "Replace the `0` on line 4 with the bigger gap minus the smaller gap. Use the box names `first_gap` "
                "and `last_gap`, not the numbers."
            ),
            dictated=True,
            hints=[
                "Look at line 4, `print(0)`. The `0` is the part to replace. Start like this: `print(first_gap - `",
                "Python can subtract boxes, the same way it subtracts numbers. If `owls = 9` and `wolves = 4`, then "
                "`print(owls - wolves)` shows 5. No quotes around the math, so Python works it out.",
                "Replace the `0` on line 4 with `first_gap - last_gap`. Line 4 becomes `print(first_gap - last_gap)`.",
            ],
            checks=[
                # Labelled output counts (A-06): a line holding 11 as a whole number, like `The gap shrank by 11`.
                (
                    "no quotes around the math",
                    "import re as _re\n"
                    r"_eleven = any(_re.search(r'(?<![\w.-])11(?![\w.])', _l) for _l in _lines())" "\n"
                    "assert _eleven or not any('first_gap' in _l or 'last_gap' in _l for _l in _lines()), "
                    "'Your line shows the box names as letters, because they are in quotes. Take the quotes off the "
                    "math so Python works it out. " + QUOTES_RULE + "'",
                ),
                (
                    "bigger gap first",
                    "import re as _re\n"
                    r"assert not any(_re.search(r'(?<![\w.])-11(?![\w.])', _l) for _l in _lines()), "
                    "'Your line shows -11, because the smaller gap comes first. Put the bigger gap first: "
                    "`first_gap - last_gap`.'",
                ),
                (
                    "prints 11",
                    "import re as _re\n"
                    r"assert any(_re.search(r'(?<![\w.-])11(?![\w.])', _l) for _l in _lines()), "
                    "'Your line does not show the answer yet. Replace the `0` on line 4 with the two box names and a "
                    "minus sign: `first_gap - last_gap`.'",
                ),
                rerun_line(
                    "the shrink is built from the boxes",
                    {"last_gap": 41},
                    "str(_R('first_gap') - _R('last_gap'))",
                    "Your line has a typed-in number where a box name should go. Use the box names, not numbers: "
                    "`print(first_gap - last_gap)`.",
                    word=True,
                ),
                rerun_line(
                    "the shrink uses first_gap too",
                    {"first_gap": 52},
                    "str(_R('first_gap') - _R('last_gap'))",
                    "Your line uses the number 48 instead of the box `first_gap`. Use the box names, not numbers: "
                    "`print(first_gap - last_gap)`.",
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
                "```text\n[ first_gap: 48 ]\n        -\n[ last_gap: 37 ]\n        ->  11\n```\n"
                "Python looks inside both jars, takes the second number away from the first, and shows the answer."
            ),
        ),
        dict(
            angle="everyday",
            label="A calculator that remembers",
            text=(
                "A box is like a calculator's memory. `first_gap - last_gap` says: take the number saved as "
                "first_gap, minus the one saved as last_gap. Change a saved number and press Run again, and the "
                "answer changes to match."
            ),
        ),
        dict(
            angle="in Tor",
            label="The chalk wall",
            text=(
                "My chalk wall: 48, 48, 47, 46, 44, 41, 37. Each number is a gap, the hours between two bursts "
                "(blasts from the leylines). The first gap was 48. The last was 37. How much did the gap shrink? "
                "48 take away 37."
            ),
        ),
        dict(angle="shorter", text="`print(first_gap - last_gap)`: two box names, a minus sign, no quotes."),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky wants the middle",
        text=(
            "Lucky wants the middle. On a new line under line 4, show the average of the two gaps: add them inside "
            "parentheses, then divide by 2. It's PEMDAS: parentheses first."
        ),
        hints=[
            "Make a new line under line 4. Start like this: `print((first_gap + last_gap) / 2)`",
            "PEMDAS: Python divides before it adds, as in math class. So put parentheses around "
            "`first_gap + last_gap` to make it add first.",
        ],
        checks=[
            (
                "prints the average",
                "import re as _re\n"
                r"assert any(_re.search(r'(?<![\w.-])42\.5(?![\w.])', _l) for _l in _lines()), "
                "'The average does not show yet. On a new line, write `print((first_gap + last_gap) / 2)`. "
                "It should show 42.5.'",
            ),
            rerun_line(
                "the average is built from the boxes",
                {"last_gap": 41},
                "str((_R('first_gap') + _R('last_gap')) / 2)",
                "Your average has a typed-in number. Use the box names, not numbers: "
                "`(first_gap + last_gap) / 2`.",
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
            "You've seen this wall: 48, 48, 47, 46, 44, 41, 37. Gearshift's visor dimmed while he did the math in "
            "his head. Now Python does it for you."
        ),
    ),
    takeaway=(
        "`+` plus, `-` minus, `*` times, `/` divided by. Write the math with box names, like a formula: "
        "`print(first_gap - last_gap)`. `/` always gives a decimal."
    ),
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
             message_contains="typed-in number where a box name should go"),
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
        "Ask each number a question: is it *how many*, or *how much is one*? How much is one is the unit price "
        "from math class, like \"4 coins each\".\n"
        "A `#` can go at the end of a line too. In `rope_count = 0  # how many?`, Python runs the code and skips "
        "the note. Each 0 is a [[placeholder]]: it holds the place for your number."
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
            text=(
                "On line 3 and line 4, replace each 0 with a number from the lantern story on line 1. The story: "
                "Mar'tu needs 3 lanterns that cost 4 coins each."
            ),
            dictated=True,
            hints=[
                "Look at line 3, `lantern_count = 0  # how many?`. How many lanterns does Mar'tu need?",
                "Ask each number its question. In '2 maps at 6 coins', 2 is how many maps, and 6 is the price of one "
                "map. Each 0 is a [[placeholder]]: it holds the place until you put the real number there.",
                "Replace the 0 on line 3 with `3`, and the 0 on line 4 with `4`. Keep the `#` notes as they are.",
            ],
            checks=[
                story_pair(
                    "the lantern boxes match the story", "lantern_count", "lantern_price", 3, 4, "lanterns",
                    known=["lantern_count", "lantern_price", "rope_count", "rope_price"],
                    wild="`lantern_count` holds a number that isn't in the story. The story on line 1 says Mar'tu "
                    "needs 3 lanterns: put 3 in `lantern_count`.",
                ),
            ],
            pass_line="Mar'tu: 3 lanterns, 4 coins for one. Each number in its own box.",
        ),
        dict(
            id="rope-boxes",
            text=(
                "On line 5 and line 6, fill in the two rope boxes from the rope story on line 2. A coil is one roll "
                "of rope. This story gives the price first."
            ),
            dictated=False,
            hints=[
                "Look at the rope story on line 2. Which number is how many coils Mar'tu needs? That one goes on "
                "line 5, after `rope_count = `.",
                "A coil is one roll of rope. \"I need 5 coils\": 5 is how many. \"2 coins a coil\": 2 is the price "
                "of one. The price comes first here, but ask the question, not the order.",
                "Replace the 0 on line 5 with `5`, and the 0 on line 6 with `2`. Then `rope_count` holds how many "
                "coils, and `rope_price` holds the price of one.",
            ],
            checks=[
                story_pair(
                    "the rope boxes match the story", "rope_count", "rope_price", 5, 2, "coils",
                    known=["lantern_count", "lantern_price", "rope_count", "rope_price"],
                    wild="`rope_count` holds a number that isn't in the story. The story on line 2 says Mar'tu "
                    "needs 5 coils: put 5 in `rope_count`.",
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
                "```text\nlanterns: ||| (3)\nprice tag: [4 coins]\n\nrope: ||||| (5)\nprice tag: [2 coins]\n```"
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
        dict(
            angle="math class",
            label="From math class",
            text=(
                "A ratio table shows the unit price:\n"
                "```text\nlanterns  coins\n   1        4\n   3       12\n```\n"
                "4 coins is how much one lantern costs. 3 is how many lanterns. 12 is the cost of all of them, "
                "so it goes in neither box."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's own shopping",
        text=(
            "Lucky has his own shopping in mind. Under line 6, write a short shopping story in a `#` note. "
            "Then make two new boxes for it: how many, and how much is one."
        ),
        hints=[
            "A note starts with `#`, like `# Lucky needs 2 canteens that cost 7 coins each.` A canteen is a water "
            "bottle.",
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
                "'Your own shopping story is not there yet. Write it in a new note: a line that starts with `#`.'",
            ),
            (
                "two new number boxes",
                "import ast as _ast\n"
                "_old = ['lantern_count', 'lantern_price', 'rope_count', 'rope_price']\n"
                "_new = [_t.id for _n in _ast.parse(_source).body if type(_n).__name__ == 'Assign' for _t in _n.targets "
                "if type(_t).__name__ == 'Name' and _t.id not in _old and type(globals().get(_t.id)).__name__ == 'int']\n"
                "assert len(set(_new)) >= 2, 'Make two new boxes with numbers for your story, with new names: how many, "
                "and how much is one.'",
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
             fails_at=1, message_contains="needs how many"),
        dict(why="a number in quotes",
             code='lantern_count = "3"\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n',
             fails_at=1, message_contains="quotes"),
        dict(why="a lone number replaces the box line",
             code="3\nlantern_price = 4\nrope_count = 5\nrope_price = 2\n",
             fails_at=1, message_contains="no name in front"),
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
COST_INPUTS = ["lantern_count", "lantern_price", "rope_count", "rope_price"]

LET_THE_CODE_COMBINE = dict(
    id="let-the-code-combine",
    title="Let Python do the math",
    martu=(
        "Don't work the total out yourself. Write the math with the box names and let Python work it out, like a "
        "formula. In math class, this is [[show your work]]. The Example does it: "
        "`map_cost = map_count * map_price`.\n"
        "Python is not like Google Sheets, which updates by itself. When a number changes, press Run again, and the "
        "total changes to match."
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
            text=(
                "On line 5, replace the `0` with `lantern_count * lantern_price`: how many lanterns times the price "
                "of one."
            ),
            dictated=True,
            hints=[
                "Look at line 5, `lantern_cost = 0`. The `0` is the part to replace. "
                "Start like this: `lantern_cost = lantern_count * `",
                "`*` means times. The Example does the same: `map_cost = map_count * map_price`. Which two lantern "
                "boxes match `map_count` and `map_price`? If `bags = 2` and `bag_price = 6`, `bags * bag_price` is 12.",
                "Replace the `0` on line 5 with `lantern_count * lantern_price`. Line 5 becomes "
                "`lantern_cost = lantern_count * lantern_price`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "lantern_cost"),
                set_once("each box is set once, at the top", COST_INPUTS[:2]),
                slot(
                    "lantern_cost multiplies the lantern boxes", "lantern_cost", "lantern_count * lantern_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[
                        ("_have == lantern_count + lantern_price",
                         "Your line adds the two boxes with `+`. A cost is how many times the price of one, so "
                         "use `*`."),
                        # LINE-TOTAL: `lantern_count * 12` multiplies by the line total again.
                        ("_have in (lantern_count * lantern_count * lantern_price, "
                         "lantern_price * lantern_count * lantern_price)",
                         "Your line multiplies by 12, which is already the cost of all 3 lanterns. Multiply how many "
                         "by the price of one: `lantern_count * lantern_price`."),
                    ],
                    default="Make `lantern_cost` the two lantern boxes multiplied: `lantern_count * lantern_price`.",
                ),
                rerun_box(
                    "lantern_cost follows its boxes", {"lantern_count": 7, "lantern_price": 5}, "lantern_cost",
                    "_R('lantern_count') * _R('lantern_price')",
                    "`lantern_cost` has a typed-in number. Use the box names, not numbers: "
                    "`lantern_count * lantern_price`.",
                ),
            ],
        ),
        dict(
            id="rope-cost",
            text="On line 6, replace the `0` in `rope_cost = 0` the same way: multiply the two rope boxes.",
            dictated=False,
            hints=[
                "Look at line 6, `rope_cost = 0`. Start like this: `rope_cost = rope_count * `",
                "Your `lantern_cost` line on line 5 is the pattern: how many times the price of one. Which two boxes "
                "are about rope?",
                "Replace the `0` on line 6 with `rope_count * rope_price`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "rope_cost"),
                set_once("each box is set once, at the top", COST_INPUTS[2:]),
                slot(
                    "rope_cost multiplies the rope boxes", "rope_cost", "rope_count * rope_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[
                        ("_have == rope_count + rope_price",
                         "Your line adds the two boxes with `+`. A cost is how many times the price of one, so "
                         "use `*`."),
                        # LINE-TOTAL: `rope_count * 10` multiplies by the line total again.
                        ("_have in (rope_count * rope_count * rope_price, rope_price * rope_count * rope_price)",
                         "Your line multiplies by 10, which is already the cost of all 5 coils. Multiply how many by "
                         "the price of one: `rope_count * rope_price`."),
                    ],
                    default="Multiply the two rope boxes, the same way line 5 makes `lantern_cost`.",
                ),
                rerun_box(
                    "rope_cost follows its boxes", {"rope_count": 6, "rope_price": 3}, "rope_cost",
                    "_R('rope_count') * _R('rope_price')",
                    "`rope_cost` has a typed-in number. Use the box names, not numbers: multiply the two rope boxes.",
                ),
            ],
        ),
        dict(
            id="total-cost",
            text="On line 7, replace the `0` so `total_cost` adds the two cost boxes, `lantern_cost` and `rope_cost`.",
            dictated=False,
            hints=[
                "Look at line 7, `total_cost = 0`. Start like this: `total_cost = lantern_cost + `",
                "The total is the lantern cost plus the rope cost. Python can add boxes: if `apples = 2` and "
                "`pears = 5`, then `apples + pears` is 7.",
                "Replace the `0` on line 7 with `lantern_cost + rope_cost`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "total_cost"),
                set_once("each box is set once, at the top", COST_INPUTS),
                slot(
                    "total_cost adds the two costs", "total_cost",
                    "lantern_count * lantern_price + rope_count * rope_price",
                    known=COST_KNOWN, foreign=COST_FOREIGN,
                    rules=[("_have == lantern_count + rope_count",
                            "Your line adds how many lanterns and coils, not costs. Add the two cost boxes: "
                            "`lantern_cost + rope_cost`.")],
                    default="Add the two cost boxes: `lantern_cost + rope_cost`.",
                ),
                rerun_box(
                    "total_cost follows the lantern boxes", {"lantern_count": 7}, "total_cost",
                    "_R('lantern_count') * _R('lantern_price') + _R('rope_count') * _R('rope_price')",
                    "`total_cost` has a typed-in number. Use the box names, not numbers: `lantern_cost + rope_cost`.",
                ),
                rerun_box(
                    "total_cost follows every box", {"lantern_price": 5, "rope_count": 6, "rope_price": 3}, "total_cost",
                    "_R('lantern_count') * _R('lantern_price') + _R('rope_count') * _R('rope_price')",
                    "`total_cost` has a typed-in number. Use the box names, not numbers: `lantern_cost + rope_cost`.",
                ),
            ],
            pass_line="Mar'tu: 22 coins, and Python did the math. Next: change one number and watch the total change.",
        ),
        dict(
            id="a-thousand-ropes",
            text=(
                "On line 3, change `rope_count = 5` to `rope_count = 1000`. Press Run. `total_cost` changes too, even "
                "though you never touched line 7."
            ),
            dictated=True,
            hints=[
                "Look at line 3, `rope_count = 5`. It is the only line to change.",
                "Every line built from `rope_count` uses its new number when you press Run again. Python is not "
                "like Google Sheets, which updates by itself: nothing changes until you press Run.",
                "Change the `5` on line 3 to `1000`. Line 3 becomes `rope_count = 1000`. Press Run.",
            ],
            checks=[
                ("rope_count is 1000",
                 "assert rope_count == 1000, '`rope_count` is not 1000 yet. Change line 3 to `rope_count = 1000`, "
                 "then press Run.'"),
                (
                    "the total is printed",
                    "assert str(total_cost) in _lines(), 'Keep `print(total_cost)` as the last line, so the total "
                    "shows in the Console.'",
                ),
            ],
            pass_line="Mar'tu: 2012 coins. You didn't do that math, yes? Python did. Lucky, put the rope down.",
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
                "```text\nlantern_count * lantern_price\n  --> lantern_cost\n\nrope_count * rope_price\n  --> rope_cost\n\n"
                "lantern_cost + rope_cost\n  --> total_cost\n```\n"
                "Change any box on the left and press Run again: the arrows carry the new number all the way to the "
                "total."
            ),
        ),
        dict(
            angle="everyday",
            label="An online cart",
            text=(
                "In an online cart, you change the quantity from 3 to 7 and press Update. The cart works out the "
                "total again from quantity × price. It never keeps a typed-in total. In Python, Run is your Update "
                "button."
            ),
        ),
        dict(
            angle="show your working",
            label="Show your work",
            text=(
                "In math class, a teacher wants your work, not only the answer. Python is the same. "
                "`total_cost = 22` is only the answer. `total_cost = lantern_cost + rope_cost` is the work, "
                "and Python does it again every time you press Run."
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
        title="Coins left over",
        text=(
            "Mar'tu has 30 coins. Under `print(total_cost)`, make a box `coins = 30`. Then show how many coins are "
            "left: the coins minus the total cost, using the box names. With 1000 ropes, expect bad news."
        ),
        hints=[
            "Add two lines under `print(total_cost)`. Start like this: `coins = 30`, then `print(coins - `",
            "`print(coins - total_cost)` shows what is left: the coins take away the total cost.",
        ],
        checks=[
            ("coins is 30", "assert coins == 30, 'Make a box `coins = 30` on a new line.'"),
            (
                "prints what is left",
                "assert str(coins - total_cost) in _lines(), 'What is left does not show yet. Add "
                "`print(coins - total_cost)`.'",
            ),
            rerun_line(
                "what is left follows the boxes", {"lantern_count": 7},
                "str(_R('coins') - _R('lantern_count') * _R('lantern_price') - _R('rope_count') * _R('rope_price'))",
                "Your line has a typed-in number. Use the box names, not numbers: `print(coins - total_cost)`.",
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
            "You've seen this line. Nobody typed how much mana was used. The code worked it out from the caster's "
            "boxes, so the bar was right for Oogrish, Gearshift, Bomb Shell and Lucky. Same idea as your total."
        ),
    ),
    takeaway=(
        "Write the math with box names: `total_cost = lantern_cost + rope_cost`. Change a box and press Run again, "
        "and the total changes to match."
    ),
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
             fails_at=1, message_contains="no box keeps the answer"),
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
             fails_at=2, message_contains="top to bottom"),
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
        "In math class, x = x − 3 has no answer. In Python, `=` isn't a math statement. Python works out the "
        "right side first, with what's in the box now: 26 − 3 is 23. Then 23 goes back in the box. Read "
        "`mana = mana - spell_cost` as: mana gets mana minus spell cost.\n"
        "Mana is a hero's magic power. To cast a spell means to use it once."
    ),
    names=["mana", "spell_cost"],
    tracer=True,
    predict=dict(
        q="Before you press Run: what will this code show in the Console?",
        choices=["20", "23", "26", "29"],
        answer=0,
        explain=(
            "Each cast takes 3 from what is in the box at that moment:\n"
            "1. `mana = 26`: mana holds 26.\n"
            "2. `spell_cost = 3`: mana still holds 26.\n"
            "3. `mana = mana - spell_cost`: 26 - 3, so 23.\n"
            "4. The same line again: 23 - 3, so 20.\n"
            "5. `print(mana)`: mana holds 20, so 20 shows."
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
            text=(
                "Each `mana = mana - spell_cost` line casts (uses) the spell once. Add one more of those lines, "
                "right above `print(mana)`. You should see 17."
            ),
            dictated=True,
            hints=[
                "Look at lines 3 and 4: each one casts the spell once. Click at the end of line 4, press Enter, and "
                "type `mana = `.",
                "Python works out the right side first, using what is in the box now. If `glow = 8`, then "
                "`glow = glow - 2` puts 6 back in `glow`.",
                "Write `mana = mana - spell_cost` above `print(mana)`.",
            ],
            checks=[
                near_names("the names are exact", ["mana", "spell_cost"], ["mana", "spell_cost"]),
                no_bare_math("the answer goes back in the box", "mana"),
                (
                    "three casts print 17",
                    "assert '-17' not in _lines(), 'Your new line takes `mana` away from `spell_cost`, so it shows -17. "
                    "Put `mana` first: `mana = mana - spell_cost`.'\n"
                    "assert '17' in _lines() or mana != 17, '`mana` ends at 17, but `print(mana)` ran too early, "
                    "before the third cast. Move `print(mana)` to the last line.'\n"
                    "assert '17' in _lines() or mana != 20, '`mana` ends at 20: that is only two casts. "
                    "Add one more `mana = mana - spell_cost` line above `print(mana)`.'\n"
                    "assert '17' in _lines() or mana != 14, '`mana` ends at 14: that is four casts. "
                    "Keep three `mana = mana - spell_cost` lines, then `print(mana)`.'\n"
                    "assert '17' in _lines(), 'The Console does not show three casts yet. "
                    "Add a third `mana = mana - spell_cost` line above `print(mana)`.'",
                ),
                rerun_line(
                    "the casts use spell_cost", {"spell_cost": 5}, "str(26 - 3 * _R('spell_cost'))",
                    "Some of your code has a typed-in number. Use the box names, not numbers: every cast is "
                    "`mana = mana - spell_cost`.",
                ),
                (
                    "each cast changes the box",
                    "import ast as _ast\n"
                    "_casts = [_n for _n in _ast.parse(_source).body if (type(_n).__name__ == 'Assign' "
                    "and any(getattr(_t, 'id', '') == 'mana' for _t in _n.targets) and type(_n.value).__name__ == 'BinOp' "
                    "and type(_n.value.op).__name__ == 'Sub') or (type(_n).__name__ == 'AugAssign' "
                    "and getattr(_n.target, 'id', '') == 'mana' and type(_n.op).__name__ == 'Sub')]\n"
                    "assert len(_casts) >= 3, '17 shows, but `mana` only changed ' + str(len(_casts)) + "
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
                "```text\n[ mana: 26 ]\n  -> take out 3: 23\n  -> put it back\n[ mana: 23 ]\n```\n"
                "Each cast: open the jar, take out the cost, put what is left back in the same jar."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "1. `mana = 26`: mana holds 26.\n"
                "2. `mana = mana - spell_cost`: 26 - 3, so mana holds 23.\n"
                "3. The same line again: 23 - 3, so 20.\n"
                "4. Once more: 20 - 3, so 17.\n"
                "5. `print(mana)` shows 17."
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
        title="Lucky shares his glug",
        text=(
            "After the third cast, Lucky shares his glug (his drink): +2 mana. Under `print(mana)`, add 2 to `mana` "
            "the same way, then show `mana` again."
        ),
        hints=[
            "Add two lines under `print(mana)`. Start like this: `mana = mana + `",
            "`mana = mana + 2` puts 2 more in the box. Then add another `print(mana)` under it.",
        ],
        checks=[
            ("prints 19 after the glug", "assert '19' in _lines(), '19 does not show yet. Under `print(mana)`, add "
             "`mana = mana + 2`, then another `print(mana)`.'"),
            rerun_line(
                "the glug line uses the box", {"spell_cost": 5}, "str(26 - 3 * _R('spell_cost') + 2)",
                "Your code has a typed-in number. Add 2 to what is in `mana` now: `mana = mana + 2`.",
            ),
        ],
        solution=SPEND_SOLUTION + "mana = mana + 2\nprint(mana)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "You've seen this line in `cast_spell`. It is `mana = mana - spell_cost` with longer names: "
            "take the caster's mana now, subtract the spell's cost, put the answer back."
        ),
    ),
    takeaway=(
        "`mana = mana - spell_cost`: Python works out the right side first, with what is in the box now, then puts "
        "the answer back in the box."
    ),
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
        dict(why="the old dash advice followed: the third cast stores only the cost",
             code="mana = 26\nspell_cost = 3\nmana = mana - spell_cost\nmana = mana - spell_cost\nmana = spell_cost\nprint(mana)\n",
             fails_at=1, message_contains="mana = mana - spell_cost"),
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
def named_out(label, tail, missing_lucky, missing_own, spaces, early=None):
    """OUT for a line that starts with `name`: Lucky gets the full diff; any other name is accepted and its diff
    never repeats the student's name back. `early`: what to type next when Lucky's line is right so far but stops."""
    full = out_line("", "'Lucky' + " + tail, missing_lucky, early=early)[1]
    own = out_line("", "str(name) + " + tail, missing_own, privacy=True, spaces=spaces)[1]
    return (
        label,
        "if name == 'Lucky':\n" + "".join("    " + _l + "\n" for _l in full.splitlines())
        + "else:\n" + "".join("    " + _l + "\n" for _l in own.splitlines()),
    )


GLUE_OUT = named_out(
    "prints Lucky has 26 mana.", "' has ' + str(mana) + ' mana.'",
    "Show `Lucky has 26 mana.`, glued from `name`, the words in quotes, and `str(mana)`.",
    "Show the line glued from `name`, the words in quotes, and `str(mana)`. With a made-up name, Tester, and 4 "
    "mana, it would show `Tester has 4 mana.`",
    "Check the spaces: one after the name, and one on each side of the number.",
    early="Now add the mana: click just before the last `)` on your `print` line and type `+ str(mana) + \" mana.\"`.",
)

# Both glue-words checkpoints: a box name in quotes is just letters (the finished line is always accepted).
GLUE_NO_QUOTED_NAMES = (
    "box names are not in quotes",
    "import ast as _ast\n"
    "_q = [_n.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Constant' "
    "and type(_n.value).__name__ == 'str' and _n.value.strip() in ('mana', 'name')]\n"
    "_right = str(name) + ' has ' + str(mana) + ' mana.' in _lines()\n"
    "assert _right or not _q, 'Take the quotes off `' + (_q[0].strip() if _q else '') + '`. In quotes, it is only "
    "those letters, not the box. " + QUOTES_RULE + "'",
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
    "        _msg = 'Nothing shows in the Console yet. Type `print(name + \" has \")` on a new line under the `#` note, and press Run.'\n"
    "    elif any(_l.startswith(str(name) + 'has') for _l in _ls):\n"
    "        _msg = 'A space is missing between the name and `has`. Spaces are text too: put them inside the quotes, `\" has \"`.'\n"
    "    else:\n"
    "        _msg = 'Your line does not start with the name from the box, then ` has`. Type `print(name + \" has \")`. "
    "With a made-up name, Tester, it would show `Tester has`.'\n"
    "assert not _msg, _msg\n",
)

GLUE_WORDS = dict(
    id="glue-words",
    title="Glue words together",
    martu=(
        "`+` has two jobs. Between numbers it adds: `2 + 3` is 5. Between texts it [[glue|glues]], like a compound "
        "word: `\"sun\" + \"flower\"` is `\"sunflower\"`, with no space. To glue a number, make it text first with "
        "[[str()|`str()`]], short for *string*: `str(26)` gives `\"26\"`.\n"
        "`\"Mana: \" + 26` makes Python stop. `\"Mana: \" + str(26)` works. Spaces are text too, so put them inside "
        "the quotes."
    ),
    introduces=["call:str"],
    example='drink = "glug"\nsips = 5\nprint("Lucky drinks " + drink + ".")\nprint("Sips left: " + str(sips))\n',
    example_output="Lucky drinks glug.\nSips left: 5",
    names=["name", "mana", "str"],
    predict=dict(
        q="What will this line show in the Console?",
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
            text=(
                "On a new line under the `#` note, type `print(name + \" has \")` and press Run. The spaces inside the "
                "quotes matter. You should see `Lucky has`."
            ),
            dictated=True,
            hints=[
                "Click at the end of line 3, the `#` note, and press Enter. Then type `print(name + \" has \")` on the "
                "new line 4 and press Run.",
                "Words to show go in quotes, spaces and all. A box name has no quotes, so Python looks inside it: "
                "`\"Hi \" + pet` glues `Hi ` to the text in the box `pet`.",
                "Type `print(name + \" has \")` on line 4, under the `#` note.",
            ],
            checks=[
                GLUE_NO_QUOTED_NAMES,
                GLUE_FIRST_BEAD,
                rerun_line(
                    "the name comes from the box", {"name": "Tester"}, "'Tester has'",
                    "Your line has the name typed in, not the box. Use the box instead: `print(name + \" has \")`.",
                    hide=own("name"), starts=True,
                ),
            ],
            pass_line="Mar'tu: Two beads on the string. Now the number.",
        ),
        dict(
            id="lucky-has-mana",
            text=(
                "Click just before the last `)` on your `print` line and type `+ str(mana) + \" mana.\"`. You should "
                "see `Lucky has 26 mana.`"
            ),
            dictated=True,
            hints=[
                "Look at the last `)` on your `print` line. The new pieces go just before it.",
                "`mana` holds a number, and `+` won't glue text to a number. `str(mana)` makes a text copy of the "
                "number, so it can be glued.",
                "Click just before the last `)` on line 4 and type `+ str(mana) + \" mana.\"`. Line 4 becomes "
                "`print(name + \" has \" + str(mana) + \" mana.\")`.",
            ],
            checks=[
                GLUE_NO_QUOTED_NAMES,
                (
                    "mana holds a number",
                    "assert type(mana).__name__ == 'int', '`mana` holds text, because of the quotes. Numbers don' + "
                    "chr(39) + 't get quotes: change line 2 back to `mana = 26`, and use `str(mana)` in your `print` line.'",
                ),
                GLUE_OUT,
                rerun_line(
                    "the line is built from the boxes", {"name": "Tester", "mana": 4},
                    "_R('name') + ' has ' + str(_R('mana')) + ' mana.'",
                    "Your line has typed-in words or numbers. Use the box names instead: `name` and `str(mana)`.",
                    hide=own("name"),
                ),
                rerun_line(
                    "the line follows other boxes too", {"name": "Zelda", "mana": 7},
                    "_R('name') + ' has ' + str(_R('mana')) + ' mana.'",
                    "Your line has typed-in words or numbers. Use the box names instead: `name` and `str(mana)`.",
                    hide=own("name"),
                ),
                (
                    "glued with + and str()",
                    "assert _uses('op:Add') and _uses('call:str'), 'Your line uses commas, which add the spaces for "
                    "you. This step practices gluing: put `+` between the pieces, and turn the number into text with "
                    "`str(mana)`.'",
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
                "written on a label. In Python, the gap is a space inside the quotes."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Build it piece by piece",
            text=(
                "1. `print(name)`, press Run.\n2. `print(name + \" has \")`, press Run.\n"
                "3. `print(name + \" has \" + str(mana))`, press Run.\n4. Add `+ \" mana.\"`, press Run. Check every "
                "space."
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
        title="Lucky wants a bigger line",
        text=(
            "Lucky wants it to look bigger. Under your `print` line, make a box `max_mana = 26`. Then add a new "
            "`print` line that shows `Lucky has 26 of 26 mana.`, glued from the boxes."
        ),
        hints=[
            "Add the new lines under your `print` line. Start like this: `max_mana = 26`",
            "Copy your `print` line. Then put `+ \" of \" + str(max_mana)` right after `str(mana)`.",
        ],
        checks=[
            ("max_mana is 26", "assert max_mana == 26, 'Make a box `max_mana = 26` on a new line.'"),
            named_out("prints the of-line", "' has ' + str(mana) + ' of ' + str(max_mana) + ' mana.'",
                      "Show `Lucky has 26 of 26 mana.` on a new line.",
                      "Show the new line, glued from the boxes. With a made-up name, Tester, it would look like "
                      "`Tester has 4 of 30 mana.`",
                      "Check the spaces: one on each side of `has` and `of`, and one before `mana.`"),
            rerun_line(
                "the of-line is built from the boxes", {"name": "Tester", "mana": 4, "max_mana": 30},
                "_R('name') + ' has ' + str(_R('mana')) + ' of ' + str(_R('max_mana')) + ' mana.'",
                "Your line has typed-in words or numbers. Use the box names: `name`, `str(mana)` and "
                "`str(max_mana)`.",
                hide=own("name"),
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
            "You've seen this line, and it probably looked like a wall. Now read it as beads: text, text, "
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
             fails_at=2, message_contains="Numbers don't get quotes"),
        dict(why="commas instead of glue: right output, skips + and str()",
             code='name = "Lucky"\nmana = 26\nprint(name, "has", mana, "mana.")\n',
             fails_at=2, message_contains="practices gluing"),
        dict(why="a closing quote missing", code='name = "Lucky"\nmana = 26\nprint(name + " has + str(mana) + " mana.")\n',
             fails_at=0, message_contains="SyntaxError"),
        dict(why="gaming: boxes set to the rerun's values, then the line typed",
             code='name = "Tester"\nmana = 4\nprint("Tester has " + str(4) + " mana.")\n', fails_at=2, message_contains="Zelda"),
        dict(why="CP1: the first bead typed, not glued from the box", code='name = "Lucky"\nmana = 26\nprint("Lucky has")\n',
             fails_at=1, message_contains="starts with `Tester has`"),
        dict(why="CP1: no space between the name and has (Lucky has26mana)", code='name = "Lucky"\nmana = 26\nprint(name + "has")\n',
             fails_at=1, message_contains="space is missing"),
        dict(why="step 1 done, step 2 not started: the line stops early (never 'a space is missing')",
             code='name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\nprint(name + " has ")\n',
             fails_at=2, message_contains="Your line stops after `Lucky has`. Now add the mana"),
        dict(why="CP1: the box name in quotes", code='name = "Lucky"\nmana = 26\nprint("name" + " has ")\n',
             fails_at=1, message_contains="exact letters"),
        dict(why="CP1: gaming the message: the typed bead plus the Tester bead the message showed",
             code='name = "Lucky"\nmana = 26\nprint("Lucky has")\nprint("Tester has")\n', fails_at=1, message_contains="typed in"),
        dict(why="CP1: the student's own hero typed (the message shows Tester, never the hero)",
             code='name = "Kai"\nmana = 26\nprint("Kai has")\n', fails_at=1, message_contains="it should show a line that starts with `Tester has`. Don't type Tester"),
        dict(why="CP1: the starter run as it is (nothing printed)",
             code='name = "Lucky"\nmana = 26\n# Print: Lucky has 26 mana.  Build it from the boxes.\n', fails_at=1,
             message_contains="Nothing shows in the Console yet"),
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
    "mana = 0  # full: the same as max_mana\n"
    "# Print: Oogrish: 18/18 mana\n"
)
STATUS_KNOWN = ["hero_name", "magical_affinity", "max_mana", "mana"]
STATUS_LINE = 'print(hero_name + ": " + str(mana) + "/" + str(max_mana) + " mana")\n'


def _status(hero, maxline="max_mana = magical_affinity * 2", manaline="mana = max_mana", printed=True):
    return (
        f'hero_name = "{hero}"\nmagical_affinity = 9\n{maxline}  # twice the affinity\n{manaline}  # full: the same as max_mana\n'
        "# Print: Oogrish: 18/18 mana\n" + (STATUS_LINE if printed else "")
    )


STATUS_LINE_EX = dict(
    id="status-line",
    title="A status line",
    martu=(
        "A status line shows a hero's name and mana, like the stats text in a game: `Oogrish: 18/18 mana`. Max "
        "mana is the most mana a hero can hold. It is twice the magical affinity, how strong the hero's magic is.\n"
        "The 0s on lines 3 and 4 are placeholders: their `#` notes say what goes there. Any hero can go in "
        "`hero_name`."
    ),
    names=["hero_name", "magical_affinity", "max_mana", "mana", "str"],
    pick='"Oogrish"',
    starter=STATUS_STARTER,
    checkpoints=[
        dict(
            id="max-mana",
            text="On line 3, replace the `0` so `max_mana` is `magical_affinity` times 2.",
            dictated=False,
            hints=[
                "Look at line 3, `max_mana = 0  # twice the affinity`. Start like this: `max_mana = magical_affinity * `",
                "Twice means times 2. If `power = 7`, then `power * 2` is 14. Which box holds the affinity?",
                "Replace the `0` on line 3 with `magical_affinity * 2`. Keep the `#` note as it is.",
            ],
            checks=[
                loose_math("the math is kept in a box", "max_mana"),
                slot(
                    "max_mana is twice the affinity", "max_mana", "magical_affinity * 2",
                    known=STATUS_KNOWN, foreign=["power", "double"],
                    rules=[
                        ("_have == magical_affinity + 2", "Your line adds 2. Twice means times 2, so use `* 2`."),
                        ("_have == magical_affinity", "That is the affinity only once. Twice means times 2: "
                         "`magical_affinity * 2`."),
                    ],
                    default="Make `max_mana` the affinity times 2: `magical_affinity * 2`.",
                ),
                rerun_box("max_mana follows the affinity", {"magical_affinity": 13}, "max_mana",
                          "_R('magical_affinity') * 2",
                          "`max_mana` has a typed-in number. Use the box name, not a number: `magical_affinity * 2`."),
            ],
        ),
        dict(
            id="mana-full",
            text="On line 4, replace the `0` with `max_mana`, so `mana` starts full: `mana = max_mana`.",
            dictated=True,
            hints=[
                "Look at line 4, `mana = 0  # full: the same as max_mana`. The `0` is only a placeholder.",
                "Full means the mana is as big as the max. A box can get what is in another box: "
                "`spare = backpack` copies what is in `backpack`. Which box holds the max?",
                "Replace the `0` on line 4 with `max_mana`. Line 4 becomes "
                "`mana = max_mana  # full: the same as max_mana`.",
            ],
            checks=[
                slot("mana starts full", "mana", "max_mana", known=STATUS_KNOWN, foreign=["spare", "backpack"],
                     default="`mana` should start full, the same as `max_mana`. Write `mana = max_mana`."),
                rerun_box("mana follows max_mana", {"magical_affinity": 13}, "mana", "_R('magical_affinity') * 2",
                          "`mana` has a typed-in number. Use the box name, not a number: `mana = max_mana`."),
            ],
        ),
        dict(
            id="print-status",
            text=(
                "On line 6, a new line at the bottom, show your hero's status line, like `Oogrish: 18/18 mana`. Glue "
                "it from the boxes with `+` and `str()`. The `\"/\"` goes in quotes, so it's a slash, not divide."
            ),
            dictated=False,
            hints=[
                "Add a new line under line 5, the `# Print:` note. Start like this: `print(hero_name + \": \" + `",
                "Between the words in quotes go three boxes: the name, then the mana, then the max mana. The two "
                "numbers need `str()`.",
                "Same beads, other names: `print(pet + \": \" + str(hp) + \"/\" + str(max_hp) + \" hp\")` shows "
                "`Moth: 3/5 hp`. Your frame: `print(hero_name + \": \" + ___ + \"/\" + ___ + \" mana\")`. Fill each "
                "___ with `str()` of a box.",
            ],
            checks=[
                out_line(
                    "prints the status line",
                    "hero_name + ': ' + str(mana) + '/' + str(max_mana) + ' mana'",
                    "Your status line is not showing yet. Glue the hero's name, `: `, the mana, `/`, the max mana, "
                    "then ` mana`. With a made-up name, Tester, and 26 mana, it would show `Tester: 26/26 mana`.",
                    privacy=True,
                    spaces="Check the spaces: one after the colon, and one before `mana`. Like `Tester: 26/26 mana`.",
                ),
                rerun_line(
                    "the status line is built from the boxes", {"hero_name": "Tester", "magical_affinity": 13},
                    "'Tester: 26/26 mana'",
                    "Your line has typed-in words or numbers. Use the box names: `hero_name`, `str(mana)` and "
                    "`str(max_mana)`.",
                    show=False,
                ),
                rerun_line(
                    "the status line follows other boxes too", {"hero_name": "Zelda", "magical_affinity": 5},
                    "'Zelda: 10/10 mana'",
                    "Your line has typed-in words or numbers. Use the box names: `hero_name`, `str(mana)` and "
                    "`str(max_mana)`.",
                    show=False,
                ),
                (
                    "the first number is mana",
                    "import ast as _ast\n"
                    "assert [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Name' and _n.id == 'mana' "
                    "and type(_n.ctx).__name__ == 'Load'], 'Your line never uses the box `mana`. The first number is the "
                    "mana the hero has now: glue in `str(mana)` there, and `str(max_mana)` after the `/`.'",
                ),
            ],
            pass_line="Mar'tu: Hm. That one goes in my ledger, my notebook for the night.",
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
                "1. `max_mana = magical_affinity * 2`, press Run.\n2. `mana = max_mana`, press Run.\n"
                "3. `print(hero_name + \": \")`, press Run.\n"
                "4. Add `+ str(mana) + \"/\" + str(max_mana) + \" mana\"`, press Run."
            ),
        ),
        dict(
            angle="in Tor",
            label="My ledger",
            text=(
                "My ledger is my notebook for the night. In it, every hero gets one line: name, colon, mana over max "
                "mana. Same shape, every night."
            ),
        ),
        dict(angle="shorter", text="Max is affinity `* 2`. Mana gets max. Glue: name, `\": \"`, mana, `\"/\"`, max, `\" mana\"`."),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's status line",
        text=(
            "Lucky's turn. At the bottom of your code:\n"
            "1. Make `lucky_affinity = 13`, then `lucky_max` (twice it) and `lucky_mana` (full).\n"
            "2. Take 3 away from `lucky_mana`.\n"
            "3. Show `Lucky: 23/26 mana`, glued from the boxes."
        ),
        hints=[
            "Same shape as Oogrish: `lucky_max = lucky_affinity * 2`, then `lucky_mana = lucky_max`.",
            "Take 3 away: `lucky_mana = lucky_mana - 3`. Then glue the line with `+` and `str()`.",
        ],
        checks=[
            out_line("prints Lucky's line", "'Lucky: 23/26 mana'",
                     "Glue `Lucky: 23/26 mana` from the `lucky_` boxes with `+` and `str()`.",
                     hide=own("hero_name")),
            rerun_line("Lucky's line follows his boxes", {"lucky_affinity": 10}, "'Lucky: 17/20 mana'",
                       "Your line has a typed-in number. Use the box names, not numbers: `lucky_max` and `lucky_mana` "
                       "both come from `lucky_affinity`.",
                       hide=own("hero_name")),
        ],
        solution=_status("Oogrish") + (
            "lucky_affinity = 13\nlucky_max = lucky_affinity * 2\nlucky_mana = lucky_max\nlucky_mana = lucky_mana - 3\n"
            'print("Lucky: " + str(lucky_mana) + "/" + str(lucky_max) + " mana")\n'
        ),
    ),
    takeaway="Glue a line from boxes: `hero_name + \": \" + str(mana) + \"/\" + str(max_mana) + \" mana\"`.",
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
             fails_at=1, message_contains="no box keeps the answer"),
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
        "never turns a finished checkpoint red. Structure pass (guide 9, S12): line 4's note was `# starts full` on "
        "a line that holds 0, which a literal reader takes as 'full is 0'. Like line 3's note, it now says what "
        "goes there: `# full: the same as max_mana`. Mar'tu's 'Twice means times 2.' moved out of his text (the "
        "step and its Teach hint say it) to keep him under 60 words."
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
        "In math, 3 × 4 means 4 + 4 + 4. Python can [[stamp]] (repeat) text the same way: `\"█\" * 3` means "
        "`\"█\" + \"█\" + \"█\"`, so it shows `███`.\n"
        "A mana bar is full blocks `█` for the mana you have, then empty blocks `░` for the mana used. `+` glues "
        "the two parts. `*` repeats one text a number of times."
    ),
    names=["full", "empty", "mana", "max_mana", "bar"],
    predict=dict(
        q="What will this line show in the Console?",
        code='print("█" * 3)\n',
        choices=["███", "█3", "an error"],
        answer=0,
        explain=(
            "`*` repeats the text 3 times, the way 3 × 4 means 4 + 4 + 4. In the same way, `\"█\" * 0` shows "
            "nothing at all, and `\"█\" * 1` shows one block."
        ),
    ),
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="full-part",
            text="In the `bar` line, replace the first `0`, in `full * 0`, with `mana`.",
            dictated=True,
            hints=[
                "Look at line 5, `bar = full * 0 + empty * 0`. The first `0` is the one in `full * 0`.",
                "`\"*\" * stars` stamps one star for each point in the box `stars`: if `stars = 2`, that is `**`. "
                "Which box holds the mana you have now?",
                "Replace the first `0` on line 5 with `mana`. Line 5 becomes `bar = full * mana + empty * 0`.",
            ],
            checks=[
                (
                    "full blocks for the mana",
                    "assert bar.count(full) == mana, 'Your bar has ' + str(bar.count(full)) + ' full blocks, but `mana` is ' "
                    "+ str(mana) + '. Replace the first `0` on line 5 with `mana`.'",
                ),
                rerun(
                    "the full part follows mana (0)", {"mana": 0, "max_mana": 5}, "_n = _R('bar').count(_R('full'))",
                    "_n == 0", "'the bar should have 0 full blocks, but it had ' + str(_n) + '.'",
                    "The full part has a typed-in number. Use the box `mana` instead, so the bar changes to match the "
                    "mana: `full * mana`.",
                ),
                rerun(
                    "the full part follows mana (5)", {"mana": 5, "max_mana": 5}, "_n = _R('bar').count(_R('full'))",
                    "_n == 5", "'the bar should have 5 full blocks, but it had ' + str(_n) + '.'",
                    "The full part has a typed-in number. Use the box `mana` instead, so the bar changes to match the "
                    "mana: `full * mana`.",
                ),
            ],
        ),
        dict(
            id="empty-part",
            text=(
                "In the `bar` line, replace the second `0`, in `empty * 0`, with the mana used: `(max_mana - mana)`. "
                "PEMDAS: Python does the part in parentheses first, then it multiplies."
            ),
            dictated=True,
            hints=[
                "Look at the second `0` on line 5, in `empty * 0`. How many empty blocks are there when mana is 3 of 5?",
                "PEMDAS: Python does `*` before `-`, so put parentheses around the subtraction. "
                "`\"-\" * (8 - 3)` stamps 5 dashes.",
                "Replace the second `0` on line 5 with `(max_mana - mana)`. Line 5 becomes "
                "`bar = full * mana + empty * (max_mana - mana)`.",
            ],
            checks=[
                rerun_line("empty bar at mana 0", {"mana": 0, "max_mana": 5}, "'[░░░░░]'",
                           "The empty part should be the mana used, in parentheses: `empty * (max_mana - mana)`."),
                rerun_line("bar at mana 3", {"mana": 3, "max_mana": 5}, "'[███░░]'",
                           "The empty part should be the mana used, in parentheses: `empty * (max_mana - mana)`."),
                rerun_line("full bar at mana 5", {"mana": 5, "max_mana": 5}, "'[█████]'",
                           "The empty part should be the mana used, in parentheses: `empty * (max_mana - mana)`."),
                rerun_line("bar at mana 2 of 6", {"mana": 2, "max_mana": 6}, "'[██░░░░]'",
                           "Use the box `max_mana` inside the parentheses, not the number 5: `(max_mana - mana)`."),
            ],
            pass_line="Mar'tu: Which part of your line is the mana used? Point at it. Yes. The part in parentheses.",
        ),
        dict(
            id="gearshift-bar",
            text=(
                "Gearshift has 20 mana out of a max of 20. Put his numbers in the two boxes, `mana` and `max_mana`."
            ),
            dictated=False,
            hints=[
                "Look at lines 3 and 4, `mana = 3` and `max_mana = 5`. They are the only lines to change.",
                "A full bar means no mana is used: the mana is the same as the max. Your `bar` line works out the "
                "rest from the boxes.",
                "Change the `3` on line 3 to `20`, and the `5` on line 4 to `20`. Line 3 becomes `mana = 20`, and "
                "line 4 becomes `max_mana = 20`.",
            ],
            checks=[
                ("max_mana is 20", "assert max_mana == 20, \"`max_mana` is not 20 yet. Gearshift's max mana is 20: "
                 "change line 4 to `max_mana = 20`.\""),
                ("mana is 20", "assert mana == 20, '`mana` is not 20 yet. His bar is full, so change line 3 to "
                 "`mana = 20`.'"),
                (
                    "a full bar is printed",
                    "assert bar == full * 20 and '[' + full * 20 + ']' in _lines(), "
                    "'The bar is not 20 full blocks yet. Keep your `bar` line and `print(\"[\" + bar + \"]\")` as they "
                    "are, and press Run.'",
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
                "`empty * (max_mana - mana)` presses the empty stamp once for each point used."
            ),
        ),
        dict(
            angle="step-by-step",
            label="What Python does first",
            text=(
                "For `empty * (max_mana - mana)` with mana 3 of 5:\n1. PEMDAS, parentheses first: `5 - 3` is 2.\n"
                "2. Then `empty * 2` stamps `░░`.\nWithout parentheses, Python does `empty * 5` first, then "
                "`\"░░░░░\" - 3`, and text minus a number is an error."
            ),
        ),
        dict(
            angle="why",
            label="Why parentheses?",
            text="Python does `*` before `-`, the same as PEMDAS in math class. Parentheses say: do this part first.",
        ),
        dict(angle="shorter", text="Full: `full * mana`. Empty: `empty * (max_mana - mana)`. Glue them with `+`."),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "`get_mana_bar` had `filled = \"█\" * caster[\"mana\"]` and "
                "`empty = \"░\" * (caster[\"max_mana\"] - caster[\"mana\"])`. Your line is the same bar."
            ),
        ),
        dict(
            angle="math class",
            label="From math class",
            text=(
                "A mana bar is a tape diagram. The full part and the empty part make the whole: 3 have + 2 used = 5 "
                "max. So the empty part is the whole minus the full part, `max_mana - mana`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky wants numbers",
        text=(
            "Lucky wants numbers too. Under the last line, add a second `print` line: the bar with the numbers after "
            "it, like `[███░░] 3/5`. Use `str()` for each number."
        ),
        hints=[
            "Add a new line at the bottom. Start like this: `print(\"[\" + bar + \"] \" + str(mana) + `",
            "After the number comes `\"/\"`, then `str(max_mana)`.",
        ],
        checks=[
            out_line("prints bar and numbers", "'[' + bar + '] ' + str(mana) + '/' + str(max_mana)",
                     "Show the bar, a space, then the mana, `/` and the max mana, like `[███░░] 3/5`."),
            rerun_line("the numbers follow the boxes", {"mana": 3, "max_mana": 5}, "'[███░░] 3/5'",
                       "Your line has typed-in numbers. Use the box names, not numbers: `str(mana)` and "
                       "`str(max_mana)`."),
        ],
        solution=_bar(BAR_LINE, 20, 20) + 'print("[" + bar + "] " + str(mana) + "/" + str(max_mana))\n',
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]\nempty = "░" * (caster["max_mana"] - caster["mana"])',
        why=(
            "You've seen these two lines. Replace the first 0, then replace the second 0 with the mana used. "
            "You did the same steps with shorter names."
        ),
    ),
    takeaway=(
        "`\"█\" * mana` repeats a mark, the way 3 × 4 means 4 + 4 + 4. PEMDAS: parentheses first, so "
        "`empty * (max_mana - mana)` subtracts before it multiplies."
    ),
    wrong_answers=[
        dict(why="no brackets around the mana used", code=_bar("bar = full * mana + empty * max_mana - mana"),
             fails_at=0, message_contains="operand"),
        dict(why="the light part typed as a number", code=_bar("bar = full * mana + empty * 2"),
             fails_at=2, message_contains="mana"),
        dict(why="the full part typed as a number", code=_bar("bar = full * 3 + empty * (max_mana - mana)"),
             fails_at=1, message_contains="Use the box `mana` instead"),
        dict(why="text plus a number", code=_bar('bar = "█" + mana'),
             fails_at=0, message_contains="concatenate"),
        dict(why="Gearshift's bar typed as 20 blocks", code=_bar("bar = full * 20", 20, 20),
             fails_at=1, message_contains="Use the box `mana` instead"),
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
        "This spell has four [[bug|bugs]]: mistakes in code. Two are loud: they make Python stop with an error. Fix "
        "those first, one at a time. Two are quiet: Python runs, and `Rope: 10 coins` looks right, but for the "
        "wrong reason.\n"
        "Check the three rope boxes. I test your code with other numbers, and that finds quiet bugs."
    ),
    names=["rope_count", "rope_price", "rope_cost", "mana", "max_mana", "bar", "str"],
    pair_talk=(
        "Pair talk: you may hunt these bugs together. Talk through each one, then each of you fixes it on your "
        "own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-mana-line",
            text="Fix line 12, `print(\"Mana: \" + mana)`, so it shows `Mana: 3`.",
            dictated=False,
            hints=[
                "Press Run and read the error box: first its title, then Python's last line. It points at line 12. "
                "Look at `mana` there: is it text or a number?",
                "`+` glues text to text only, so a number has to become text first. `\"Sips: \" + str(5)` works, "
                "but `\"Sips: \" + 5` makes Python stop.",
                "Type `str(` right before `mana` on line 12, and `)` right after it. Line 12 becomes "
                "`print(\"Mana: \" + str(mana))`.",
            ],
            checks=[
                out_line("prints Mana: 3", "'Mana: ' + str(mana)", "Show `Mana: ` glued to `str(mana)`."),
                rerun_line("the mana line follows the box", {"mana": 4}, "'Mana: 4'",
                           "Your line has the number typed in. Glue the box instead: `\"Mana: \" + str(mana)`."),
                rerun_line("the mana line follows the box (1)", {"mana": 1}, "'Mana: 1'",
                           "Your line has the number typed in. Glue the box instead: `\"Mana: \" + str(mana)`."),
            ],
        ),
        dict(
            id="mend-bar",
            text="Fix line 13, the `bar` line, so the empty blocks show the mana used.",
            dictated=False,
            hints=[
                "Press Run and read the error box: its title, then Python's last line. It points at line 13. In the "
                "`bar` line, which part should Python do first?",
                "PEMDAS: Python does `*` before `-`, so put parentheses around the part to do first. "
                "`\"-\" * (8 - 3)` stamps 5 dashes.",
                "Type `(` right before `max_mana` on line 13, and `)` at the very end. Line 13 becomes "
                "`bar = \"█\" * mana + \"░\" * (max_mana - mana)`.",
            ],
            checks=[
                rerun_line("bar at mana 3", {"mana": 3, "max_mana": 5}, "'[███░░]'",
                           "The empty part should be the mana used, in parentheses: `\"░\" * (max_mana - mana)`."),
                rerun_line("bar at mana 0", {"mana": 0, "max_mana": 5}, "'[░░░░░]'",
                           "The empty part should be the mana used, in parentheses: `\"░\" * (max_mana - mana)`."),
                rerun_line("bar at mana 2 of 6", {"mana": 2, "max_mana": 6}, "'[██░░░░]'",
                           "Use the box `max_mana` inside the parentheses, not the number 5: `(max_mana - mana)`."),
            ],
            pass_line="Mar'tu: Both loud bugs fixed. Now the quiet ones.",
        ),
        dict(
            id="mend-rope-cost",
            text=(
                "Fix line 8: `rope_cost = 10` has the answer typed in. Make Python work it out from the rope boxes."
            ),
            dictated=False,
            hints=[
                "Look at line 8, `rope_cost = 10`. Start like this: `rope_cost = rope_count * `",
                "Look at line 4: `lantern_cost` is worked out from the two lantern boxes, how many times the price "
                "of one. Do the same with the rope boxes.",
                "Replace the `10` on line 8 with `rope_count * rope_price`.",
            ],
            checks=[
                slot("rope_cost is built from the boxes", "rope_cost", "rope_count * rope_price", known=BROKEN_KNOWN,
                     default="Multiply the two rope boxes, the same way line 4 makes `lantern_cost`."),
                rerun_box("rope_cost follows the rope boxes", {"rope_count": 6, "rope_price": 3}, "rope_cost",
                          "_R('rope_count') * _R('rope_price')",
                          "`rope_cost` has the answer typed in. Use the box names, not numbers: "
                          "`rope_count * rope_price`."),
            ],
            pass_line="Mar'tu: Right answer, wrong reason, now fixed. That one fools everyone once.",
        ),
        dict(
            id="mend-rope-boxes",
            text=(
                "Fix line 6 and line 7, the rope boxes. Read the rope note on line 5: which number is how many "
                "coils (rolls of rope), and which is the price of one?"
            ),
            dictated=False,
            hints=[
                "Read the rope note on line 5. How many coils does Mar'tu need? That number goes on line 6, after "
                "`rope_count = `.",
                "The cost came out 10 either way, because 2 × 5 = 5 × 2: in math class, that's the commutative "
                "property. But the boxes still mean the wrong things. If Mar'tu needs one more coil, which box "
                "should change?",
                "Swap the `2` on line 6 and the `5` on line 7. Line 6 becomes `rope_count = 5`, and line 7 becomes "
                "`rope_price = 2`.",
            ],
            checks=[
                story_pair("the rope boxes match the story", "rope_count", "rope_price", 5, 2, "coils",
                           known=BROKEN_KNOWN, wild="`rope_count` should be how many coils the note on line 5 says: 5.",
                           price_first=True,
                           swap_extra=" The cost still comes out 10, because 2 × 5 = 5 × 2. But if Mar'tu needs one "
                           "more coil, which box changes?"),
            ],
            pass_line="Mar'tu: Four bugs, four fixes. The spell holds, yes?",
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
                "1. Press Run. Python stops at the first loud bug. Read the error box: its title, then Python's last "
                "line. Find the line number and fix that line.\n"
                "2. Press Run again, and fix the next one.\n"
                "3. When Python no longer stops, read the message under each step."
            ),
        ),
        dict(
            angle="picture",
            label="Two kinds of bug",
            text=(
                "```text\nloud bugs:\nPython stops, and its\nerror box gives the line.\n\n"
                "quiet bugs:\nthe program runs, but\nthe answer is wrong.\n```\n"
                "The quiet ones only show up when someone tries other numbers."
            ),
        ),
        dict(
            angle="shorter",
            text="`str(mana)`. `rope_count * rope_price`. Count 5, price 2. Parentheses around `max_mana - mana`.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's total",
        text=(
            "At the bottom, make `total_cost` from the two cost boxes. Then show `Total: 22 coins`, glued from the "
            "boxes."
        ),
        hints=[
            "Add the new lines at the bottom. Start like this: `total_cost = lantern_cost + rope_cost`",
            "Then show it: `print(\"Total: \" + str(total_cost) + \" coins\")`.",
        ],
        checks=[
            out_line("prints the total", "'Total: 22 coins'", "Show `Total: 22 coins`, glued from `total_cost` with `str()`."),
            rerun_line("the total follows the boxes", {"lantern_count": 7}, "'Total: 38 coins'",
                       "Your total has a typed-in number. Use the box names, not numbers: `lantern_cost + rope_cost`, "
                       "then `str(total_cost)`."),
        ],
        solution=_broken() + 'total_cost = lantern_cost + rope_cost\nprint("Total: " + str(total_cost) + " coins")\n',
    ),
    takeaway=(
        "Loud bugs make Python stop: read the error box, find the line number, and fix that line. Quiet bugs show "
        "the right thing for the wrong reason: test with other numbers."
    ),
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
    martu=(
        "A short problem, all yours. Fill in the boxes from the story, then let Python do the math with the box "
        "names."
    ),
    solo=True,
    names=["candle_count", "candle_price", "candle_cost"],
    starter=CANDLE_STORY + "candle_count = 0\ncandle_price = 0\ncandle_cost = 0\nprint(candle_cost)\n",
    checkpoints=[
        dict(
            id="candle-boxes",
            text="On line 2 and line 3, fill in `candle_count` and `candle_price` from the story on line 1.",
            dictated=False,
            hints=[
                "Look at the story on line 1. How many candles does Mar'tu need? That number replaces the 0 on "
                "line 2.",
                "Ask each number its question: how many, or how much is one? In '2 maps at 6 coins', 2 is how many "
                "and 6 is the price of one.",
                "Replace the 0 on line 2 with `4`, and the 0 on line 3 with `2`.",
            ],
            checks=[
                story_pair("the candle boxes match the story", "candle_count", "candle_price", 4, 2, "candles",
                           known=CANDLE_KNOWN + ["lantern_count", "lantern_price"],
                           wild="`candle_count` should be how many candles the story on line 1 says: 4."),
            ],
        ),
        dict(
            id="candle-cost",
            text="On line 4, replace the `0` so `candle_cost` is how many candles times the price of one. Use the two candle boxes.",
            dictated=False,
            hints=[
                "Look at line 4, `candle_cost = 0`. Start like this: `candle_cost = candle_count * `",
                "A cost is how many times the price of one. If `bags = 4` and `bag_price = 5`, then "
                "`bags * bag_price` is 20.",
                "Replace the `0` on line 4 with `candle_count * candle_price`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "candle_cost"),
                slot("candle_cost multiplies the boxes", "candle_cost", "candle_count * candle_price",
                     known=CANDLE_KNOWN, foreign=["lantern_count", "lantern_price", "lantern_cost", "map_cost"],
                     rules=[
                         # LINE-TOTAL: `candle_count * 8` multiplies by the line total again.
                         ("_have in (candle_count * candle_count * candle_price, "
                          "candle_price * candle_count * candle_price)",
                          "Your line multiplies by 8, which is already the cost of all 4 candles. Multiply how many by "
                          "the price of one: `candle_count * candle_price`."),
                     ],
                     default="Multiply the two candle boxes: how many `*` the price of one."),
                rerun_box("candle_cost follows the boxes", {"candle_count": 7, "candle_price": 3}, "candle_cost",
                          "_R('candle_count') * _R('candle_price')",
                          "`candle_cost` has a typed-in number. Use the box names, not numbers: "
                          "`candle_count * candle_price`."),
            ],
            pass_line="Mar'tu: You did that on your own. The boxes came from the story, and Python did the math.",
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
    takeaway="On your own: fill the boxes from the story, then let Python do the math with the box names.",
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
             fails_at=2, message_contains="no box keeps the answer"),
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
        "placeholders so the starter runs (`candle_cost = 0` stays). The pass line reads as showing off a skill, "
        "not as being watched (no 'On your map:': no skills map is on screen yet, guide 4.6 and S10). LINE-TOTAL (`candle_count * 8`) gets its own message."
    ),
)

LESSON_1C = dict(
    kind="lesson",
    id="math-and-glue",
    title="Math and Glue",
    minutes=39,
    summary="Let Python do the math with your boxes, spend mana, glue words and numbers with `str()`, and draw a mana bar.",
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
        "`hours_waited += 6` is a short way to write `hours_waited = hours_waited + 6`. Read it as *hours waited "
        "goes up by 6*. `mana -= 3` means `mana = mana - 3`: mana goes down by 3.\n"
        "Same answer, less typing. You never have to use it. Lazy wizards love it."
    ),
    introduces=["node:AugAssign"],
    names=["hours_waited", "mana"],
    predict=dict(
        q="What will this code show in the Console?",
        code="hours_waited = 30\nhours_waited += 6\nmana = 20\nmana -= 3\nprint(hours_waited)\nprint(mana)\n",
        choices=["36\n17", "6\n3", "30\n20"],
        answer=0,
        explain="`+= 6` adds 6 to what is in the box and puts it back: 30 becomes 36. `-= 3` takes 3 away: 20 becomes 17.",
    ),
    starter=SHORT_STARTER,
    checkpoints=[
        dict(
            id="plus-equals",
            text="Change line 2 to the short way: `hours_waited += 6`.",
            dictated=True,
            hints=[
                "Look at line 2, `hours_waited = hours_waited + 6`. The box name is on both sides. The short way "
                "names it once.",
                "`glow += 2` means `glow = glow + 2`. The `+` comes before the `=`.",
                "Write `hours_waited += 6` in place of `hours_waited = hours_waited + 6`.",
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
                    "assert hours_waited == 36, '`hours_waited` should end at 36: 30, then 6 more. Write line 2 as "
                    "`hours_waited += 6`.'",
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
            text="Change line 4, `mana = mana - 3`, to the short way too.",
            dictated=False,
            hints=[
                "Look at line 4, `mana = mana - 3`. It takes 3 away from `mana`.",
                "`glow -= 2` means `glow = glow - 2`. Which sign goes before the `=` this time?",
                "Write `mana -= 3` in place of `mana = mana - 3`.",
            ],
            checks=[
                ("mana is 17", "assert mana == 17, '`mana` should end at 17: 20, take away 3. Keep the 3 on line 4, "
                 "and put the `-` before the `=`.'"),
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
    takeaway="`box += 6` is `box = box + 6`. `box -= 3` is `box = box - 3`. Both ways are always fine.",
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
    title="One more shop",
    martu=(
        "Same idea, new shop. Both lines of the story give the price first. Ask each number its question: how "
        "many, or how much is one? Then let Python do the math with the box names. A flask is a small bottle."
    ),
    names=["chalk_count", "chalk_price", "oil_count", "oil_price", "supply_total"],
    starter=SUPPLY_STORY + "chalk_count = 0\nchalk_price = 0\noil_count = 0\noil_price = 0\nsupply_total = 0\nprint(supply_total)\n",
    checkpoints=[
        dict(
            id="supply-boxes",
            text="Fill in the four boxes under the story, using the two `#` notes at the top.",
            dictated=False,
            hints=[
                "Look at line 1, the chalk story. How many sticks does Oogrish want? That number goes after "
                "`chalk_count = `.",
                "Each line gives the price first. 'Candles cost 1 coin each, and I need 3': 3 is how many, and 1 is "
                "the price of one. Ask the question, not the order.",
                "Replace the four 0s: `3` on line 3, `5` on line 4, `4` on line 5 and `3` on line 6.",
            ],
            checks=[
                story_pair("the chalk boxes match the story", "chalk_count", "chalk_price", 3, 5, "sticks",
                           known=SUPPLY_KNOWN, wild="`chalk_count` should be how many sticks the story says: 3.",
                           price_first=True),
                story_pair("the oil boxes match the story", "oil_count", "oil_price", 4, 3, "flasks",
                           known=SUPPLY_KNOWN, wild="`oil_count` should be how many flasks the story says: 4.",
                           price_first=True),
            ],
        ),
        dict(
            id="supply-total",
            text=(
                "Replace the `0` in `supply_total = 0` with the cost of everything. Add the chalk cost and the oil "
                "cost, and use the box names."
            ),
            dictated=False,
            hints=[
                "Look at line 7, `supply_total = 0`. Start like this: `supply_total = chalk_count * chalk_price + `",
                "Two costs: chalk, then oil. Each is how many times the price of one. PEMDAS: Python multiplies "
                "before it adds, so you need no parentheses here.",
                "Replace the `0` on line 7 with `chalk_count * chalk_price + oil_count * oil_price`.",
            ],
            checks=[
                slot("supply_total adds both costs", "supply_total", SUPPLY_TOTAL, known=SUPPLY_KNOWN,
                     rules=[("_have == chalk_count + oil_count", "You added how many, not costs. Each cost is how "
                             "many times the price of one.")],
                     default="Add the chalk cost and the oil cost. Each one is how many `*` the price of one."),
                rerun_box("supply_total follows the chalk", {"chalk_count": 5, "chalk_price": 7}, "supply_total",
                          "_R('chalk_count') * _R('chalk_price') + _R('oil_count') * _R('oil_price')",
                          "`supply_total` has a typed-in number. Use the box names, not numbers, for chalk and oil."),
                rerun_box("supply_total follows the oil", {"oil_count": 9, "oil_price": 4}, "supply_total",
                          "_R('chalk_count') * _R('chalk_price') + _R('oil_count') * _R('oil_price')",
                          "`supply_total` has a typed-in number. Use the box names, not numbers, for chalk and oil."),
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
    takeaway=(
        "Price first or count first, ask each number its question. Then let Python do the math: count `*` price `+` "
        "count `*` price."
    ),
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
    summary="The short way to change a box, and one more shop to add up. For whenever you want it.",
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
                0: "`def` is for something you'll learn in Unit 3. To make a box, write the name, `=`, then the value.",
                1: "A box's name never goes in quotes. In quotes, `\"hero\"` is only the letters h-e-r-o.",
                3: "`-` is minus. To make a box, use `=`.",
            },
            explain="A box is `name = value`: the name with no quotes, `=`, then the text in quotes. Hero gets Lucky.",
            notes="WA evidence: A-02 def; A-04 dash; B-02/B-03 lone value.",
        ),
        dict(
            type="predict",
            id="mana-twice",
            q="What will this code show in the Console?",
            code="mana = 18\nmana = mana - 5\nmana = mana - 5\nprint(mana)\n",
            choices=["8", "13", "18", "28"],
            answer="8",
            explain=(
                "Each line works out the right side with what is in the box now: 18, then 13, then 8. The box keeps "
                "only its newest value."
            ),
        ),
        dict(
            type="bug",
            id="not-a-compass",
            q="This line should show It is not a compass. Fix it.",
            code='print("It is not a compass)\n',
            fix='print("It is not a compass")\n',
            expected_output="It is not a compass",
            explain="Quotes come in pairs, like quotation marks in English class. Add the closing `\"` before the `)`.",
        ),
        dict(
            type="predict",
            id="stamp-a-bar",
            q="What will this line show in the Console?",
            code='print("█" * 2 + "░" * 3)\n',
            choices=["██░░░", "█2░3", "█░", "an error"],
            answer="██░░░",
            explain="`*` repeats each text: two full blocks, then three empty blocks, glued together with `+`.",
        ),
        dict(
            type="fill",
            id="glue-a-number",
            q="Fill the blank so this line shows `Mana: 7`.",
            code='print("Mana: " + ___(7))\n',
            answer="str",
            expected_output="Mana: 7",
            explain="`str(7)` turns the number into text, so it can be glued to `\"Mana: \"`. `str` is short for string.",
        ),
        dict(
            type="mc",
            id="which-total-stays-right",
            q=(
                "Mar'tu had 3 lanterns, and the total was 22. Now he changes `lantern_count` to 5 and presses Run "
                "again. Which `total` line still gives the right answer, with nobody retyping it?"
            ),
            code="lantern_count = 5\nlantern_price = 4\nrope_cost = 10\n",
            choices=[
                "total = 22",
                "total = 12 + 10",
                "total = lantern_count * lantern_price + rope_cost",
                "total = 3 * 4 + 10",
            ],
            answer=2,
            why_wrong={
                0: "22 is a typed-in answer for 3 lanterns. It stays 22 when the count changes.",
                1: "12 is the old lantern cost, typed in. It doesn't change to match the new count.",
                3: "3 is the old count, typed in. Use the box `lantern_count`.",
            },
            explain=(
                "Only the line with the box names changes to match when a box changes and the code runs again. "
                "It's a formula, not a typed-in answer."
            ),
        ),
        dict(
            type="mc",
            id="names-are-exact",
            q="What happens when this code runs?",
            code="Health = 100\nprint(health)\n",
            choices=["It shows 100.", "It shows the word health.", "Python stops: `health` is not defined."],
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
            q="What will this code show in the Console?",
            code="rope_count = 5\nrope_price = 2\nprint(rope_count * rope_price + 2)\n",
            choices=["12", "20", "10", "9"],
            answer="12",
            explain="PEMDAS: Python multiplies before it adds, as in math class. 5 times 2 is 10, then plus 2 is 12.",
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
LEDGER_B4_HALF = "oil_needed = hours_until_burst * oil_per_hour\noil_cost = 0\n"
LEDGER_C = "\n# C. Write the ledger\n"
LEDGER_C5 = 'print("Mana for the barrier: " + str(mana_needed))\n'
LEDGER_C6 = 'print("Lantern oil: " + str(oil_needed) + " flasks for " + str(oil_cost) + " coins")\n'
LEDGER_C7_EMPTY = 'watch_keeper = ""  # any hero, in quotes\n'
LEDGER_C7_BOX = 'watch_keeper = "Captain Glug"  # any hero, in quotes\n'


def _c7(hero):
    return f'watch_keeper = "{hero}"  # any hero, in quotes\nprint("First watch: " + watch_keeper)\n'


LEDGER_AT_37 = LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C6 + _c7("Captain Glug")
LEDGER_SOLUTION = LEDGER_AT_37.replace(LEDGER_A1, LEDGER_A1_32)
LEDGER_KNOWN = ["hours_until_burst", "mana_per_hour", "oil_per_hour", "oil_price", "mana_needed", "oil_needed",
                "oil_cost", "watch_keeper"]
OIL_LINE = "'Lantern oil: ' + str(%s) + ' flasks for ' + str(%s) + ' coins'"


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
        "        _msg = 'Your box is named `' + _near[0] + '`, but this task needs `watch_keeper`. Names match letter "
        "for letter, capitals too.'\n"
        "    elif _bare:\n"
        "        _msg = 'Line ' + str(_bare[0]) + ' is a value with no name in front, so Python reads it and throws it "
        "away, like a phone number saved with no contact name. Put `watch_keeper = ` in front of it.'\n"
        "    elif _newb:\n"
        "        _msg = 'Your new box `' + _newb[0] + '` holds the hero, but `watch_keeper` is still empty. "
        "Put the hero in `watch_keeper` instead.'\n"
        "    elif 'watch_keeper' not in _g:\n"
        "        _msg = 'Make a box named `watch_keeper`: start a line with `watch_keeper = `.'\n"
        "    elif type(_have).__name__ != 'str':\n"
        "        _msg = '`watch_keeper` should hold a hero, in quotes.'\n"
        "    else:\n"
        "        _msg = '`watch_keeper` holds empty quotes. Put any hero between them, or press the Mar' + chr(39) + "
        "'tu' + chr(39) + 's pick button, next to Names to use.'\n"
        "assert _ok, _msg\n"
    ),
)

PROJECT_1P1 = dict(
    kind="project",
    id="night-watch-ledger",
    title="The Night Watch Ledger",
    minutes=19,
    summary=(
        "Mar'tu's ledger, his notebook of costs, for the long night: mana for the barrier, oil for the lanterns, "
        "and who keeps watch."
    ),
    intro=(
        "A ledger is a notebook where you write down what things cost. Mar'tu keeps one for tonight. The barrier "
        "must hold until the next burst (a blast from the leylines), 37 hours away.\n"
        "Three parts, in order: A. what we know, B. let the code combine it (do the math with the box names), "
        "C. write the ledger.\n"
        "The barrier eats 2 mana an hour. The lanterns burn 1 flask (a small bottle) of oil an hour, and a flask "
        "costs 3 coins. *Per hour* is a unit rate, like miles per hour."
    ),
    martu=(
        "Thirty-seven hours, yes? I don't want to do this math by hand in the middle of the night. Put what we "
        "know in boxes, let Python do the math with the box names, then write the ledger lines. If the clock "
        "changes its mind, change one box and press Run again: every line changes to match."
    ),
    names=["hours_until_burst", "mana_per_hour", "oil_per_hour", "oil_price", "mana_needed", "oil_needed",
           "oil_cost", "watch_keeper", "str"],
    pick='"Bomb Shell"',
    starter=LEDGER_STARTER,
    checkpoints=[
        dict(
            id="hours-until-burst",
            text="A. Under `# A. What we know`, replace the 0 in `hours_until_burst = 0` with 37.",
            dictated=True,
            hints=[
                "Look under `# A. What we know`, at line 2: `hours_until_burst = 0`.",
                "A box gets a number with `name = value`, and a number gets no quotes: `steps = 12`.",
                "Replace the 0 on line 2 with `37`. Line 2 becomes `hours_until_burst = 37`.",
            ],
            checks=[
                # 32 is accepted too, so this task stays green after the last task (thirty-two-hours).
                slot("hours_until_burst is 37", "hours_until_burst",
                     "(32 if globals().get('hours_until_burst') == 32 else 37)", known=LEDGER_KNOWN, step="task",
                     default="The burst is 37 hours away. Write `hours_until_burst = 37` on line 2."),
            ],
        ),
        dict(
            id="what-we-know",
            text=(
                "A. Fill in the other three boxes under `# A.` from the story at the top of this page: mana per "
                "hour, flasks per hour, and the price of one flask."
            ),
            dictated=False,
            hints=[
                "The story is at the top of this page, above Your tasks. Start like this: `mana_per_hour = 2`. The "
                "other two numbers are in the story too.",
                "The barrier eats 2 mana an hour. The lanterns burn 1 flask an hour. A flask costs 3 coins.",
                "Replace the 0s: `2` on line 3, `1` on line 4 and `3` on line 5.",
            ],
            checks=[
                slot("mana_per_hour is 2", "mana_per_hour", "2", known=LEDGER_KNOWN, step="task",
                     default="The barrier needs 2 mana each hour: `mana_per_hour = 2`."),
                (
                    "oil boxes are not swapped",
                    "assert not (oil_per_hour == 3 and oil_price == 1), "
                    "'You swapped them: 1 is how many flasks burn each hour, and 3 is the price of one flask.'",
                ),
                slot("oil_per_hour is 1", "oil_per_hour", "1", known=LEDGER_KNOWN, step="task",
                     default="The lanterns burn 1 flask each hour: `oil_per_hour = 1`."),
                slot("oil_price is 3", "oil_price", "3", known=LEDGER_KNOWN, step="task",
                     default="One flask costs 3 coins: `oil_price = 3`."),
            ],
        ),
        dict(
            id="mana-needed",
            text=(
                "B. Replace the 0 in `mana_needed = 0` with the hours times the mana per hour: use `*` and the two "
                "box names."
            ),
            dictated=False,
            hints=[
                "Look under `# B. Let the code combine it`, at line 8. Start like this: "
                "`mana_needed = hours_until_burst * `",
                "2 mana for each of 37 hours is 37 × 2. If `days = 3` and `meals_per_day = 2`, then "
                "`days * meals_per_day` is 6 meals. Which two boxes hold the hours and the mana per hour?",
                "Replace the 0 on line 8 with `hours_until_burst * mana_per_hour`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "mana_needed"),
                set_once("each box is set once, at the top", ["hours_until_burst", "mana_per_hour"]),
                slot("mana_needed multiplies the boxes", "mana_needed", "hours_until_burst * mana_per_hour",
                     known=LEDGER_KNOWN, foreign=["days", "meals_per_day"], step="task",
                     rules=[
                         ("_have == hours_until_burst + mana_per_hour",
                          "Your line adds. The barrier needs 2 mana for each hour, so multiply with `*`."),
                         # LINE-TOTAL (no numbers in the message: the hours change in the last task).
                         ("_have in (hours_until_burst * hours_until_burst * mana_per_hour, "
                          "mana_per_hour * hours_until_burst * mana_per_hour)",
                          "Your line multiplies by a total that is already worked out. Multiply the hours by the mana "
                          "for one hour: `hours_until_burst * mana_per_hour`."),
                     ],
                     default="`mana_needed` is not worked out yet. Multiply `hours_until_burst` by `mana_per_hour`."),
                rerun_box("mana_needed follows the hours", {"hours_until_burst": 32, "mana_per_hour": 3}, "mana_needed",
                          "_R('hours_until_burst') * _R('mana_per_hour')",
                          "`mana_needed` has a typed-in number. Use the box names, not numbers: `hours_until_burst` "
                          "times `mana_per_hour`."),
            ],
            pass_line="Gearshift: Math checks out.",
        ),
        dict(
            id="oil-needed-and-cost",
            text=(
                "B. Replace the 0 in `oil_needed = 0` with the hours times the flasks per hour: use `*` and the boxes "
                "`hours_until_burst` and `oil_per_hour`."
            ),
            dictated=False,
            hints=[
                "Look at line 9, `oil_needed = 0`, under `mana_needed`. Start like this: "
                "`oil_needed = hours_until_burst * `",
                "Flasks: the hours times the flasks per hour, the same shape as your `mana_needed` line. Which box "
                "holds the flasks per hour?",
                "Replace the 0 on line 9 with `hours_until_burst * oil_per_hour`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "oil_needed"),
                set_once("each box is set once, at the top", ["hours_until_burst", "oil_per_hour"]),
                slot("oil_needed multiplies the boxes", "oil_needed", "hours_until_burst * oil_per_hour",
                     known=LEDGER_KNOWN, foreign=["bags", "bag_price"], step="task",
                     default="`oil_needed` is not worked out yet. Multiply `hours_until_burst` by `oil_per_hour`."),
                rerun_box("oil_needed follows the boxes", {"hours_until_burst": 32, "oil_per_hour": 2}, "oil_needed",
                          "_R('hours_until_burst') * _R('oil_per_hour')",
                          "`oil_needed` has a typed-in number. Use the box names, not numbers: multiply "
                          "`hours_until_burst` by `oil_per_hour`."),
            ],
        ),
        dict(
            id="oil-cost",
            text=(
                "B. Replace the 0 in `oil_cost = 0` with the flasks times the price of one flask: use `*` and the "
                "boxes `oil_needed` and `oil_price`."
            ),
            dictated=False,
            hints=[
                "Look at line 10, `oil_cost = 0`. Start like this: `oil_cost = oil_needed * `",
                "Coins: how many flasks times the price of one, the way `bags * bag_price` is 20 coins when "
                "`bags = 4` and `bag_price = 5`.",
                "Replace the 0 on line 10 with `oil_needed * oil_price`.",
            ],
            checks=[
                loose_math("the math is kept in a box", "oil_cost"),
                set_once("each box is set once, at the top", ["hours_until_burst", "oil_per_hour", "oil_price"]),
                slot("oil_cost multiplies the boxes", "oil_cost", "hours_until_burst * oil_per_hour * oil_price",
                     known=LEDGER_KNOWN, foreign=["bags", "bag_price"], step="task",
                     rules=[
                         # LINE-TOTAL: the flasks times the whole oil cost (or the price times it).
                         ("_have in (hours_until_burst * oil_per_hour * hours_until_burst * oil_per_hour * oil_price, "
                          "oil_price * hours_until_burst * oil_per_hour * oil_price)",
                          "Your line multiplies by a total that is already worked out. Multiply the flasks by the "
                          "price of one flask: `oil_needed * oil_price`."),
                     ],
                     default="`oil_cost` is not worked out yet. Multiply `oil_needed` by `oil_price`."),
                rerun_box("oil_cost follows the boxes", {"hours_until_burst": 32, "oil_per_hour": 2, "oil_price": 5}, "oil_cost",
                          "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')",
                          "`oil_cost` has a typed-in number or skips a box. Use the box names: multiply `oil_needed` "
                          "by `oil_price`."),
            ],
        ),
        dict(
            id="mana-line",
            text=(
                "C. Under `# C. Write the ledger`, add a `print` line that shows `Mana for the barrier: ` glued to the "
                "box `mana_needed`. Use the box name, not a number you worked out."
            ),
            dictated=False,
            hints=[
                "Click at the end of line 12, `# C. Write the ledger`, and press Enter. "
                "Start like this: `print(\"Mana for the barrier: \" + `",
                "The number comes from `mana_needed`. What does a number need before it can be glued? "
                "`\"Sips: \" + str(sips)` glues text to a box with a number in it.",
                "Write `print(\"Mana for the barrier: \" + str(mana_needed))` under `# C. Write the ledger`.",
            ],
            checks=[
                out_line("prints the mana line", "'Mana for the barrier: ' + str(hours_until_burst * mana_per_hour)",
                         "Show `Mana for the barrier: ` glued to `str(mana_needed)`.", hide=own("watch_keeper")),
                rerun_line("the mana line follows the hours", {"hours_until_burst": 32, "mana_per_hour": 3},
                           "'Mana for the barrier: ' + str(_R('hours_until_burst') * _R('mana_per_hour'))",
                           "Your mana line has a typed-in number. Use the box name, not a number: `str(mana_needed)`.",
                           hide=own("watch_keeper")),
            ],
        ),
        dict(
            id="oil-line",
            text=(
                "C. Add a `print` line that shows `Lantern oil: 37 flasks for 111 coins`, glued from the words and "
                "the boxes `oil_needed` and `oil_cost`. Don't type the numbers."
            ),
            dictated=False,
            hints=[
                "Add it under your mana line. Start like this: `print(\"Lantern oil: \" + str(oil_needed) + `",
                "Two numbers come from boxes: the flasks and the coins. Everything else is words in quotes.",
                "`print(\"Lantern oil: \" + str(___) + \" flasks for \" + str(___) + \" coins\")`. Fill each ___ "
                "with a box name.",
            ],
            checks=[
                out_line("prints the oil line",
                         OIL_LINE % ("hours_until_burst * oil_per_hour", "hours_until_burst * oil_per_hour * oil_price"),
                         "Show the oil line, glued from words in quotes, `str(oil_needed)` and `str(oil_cost)`.",
                         hide=own("watch_keeper")),
                rerun_line("the oil line follows the hours", {"hours_until_burst": 32, "oil_per_hour": 2, "oil_price": 5},
                           OIL_LINE % ("_R('hours_until_burst') * _R('oil_per_hour')",
                                       "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')"),
                           "Your oil line has typed-in numbers. Use the box names, not numbers: `str(oil_needed)` and "
                           "`str(oil_cost)`.",
                           hide=own("watch_keeper")),
            ],
        ),
        dict(
            id="watch-keeper",
            text="C. On the last line, `watch_keeper = \"\"`, put any hero between the two quotes.",
            dictated=False,
            hints=[
                "Look at the last line, `watch_keeper = \"\"`. Click between its two quotes.",
                "A hero's name is text, so it goes between quotes: `guard = \"Zelda\"` puts Zelda in the box "
                "`guard`. Can't decide? Press the Mar'tu's pick button, next to Names to use.",
                "Type a hero, like `Bomb Shell`, between the two quotes. The line becomes "
                "`watch_keeper = \"Bomb Shell\"`, or any hero you like.",
            ],
            checks=[WATCH_KEEPER_CHECK],
        ),
        dict(
            id="watch-line",
            text=(
                "C. Under the `watch_keeper` line, add a `print` line that shows `First watch: ` glued with `+` to "
                "the box `watch_keeper`."
            ),
            dictated=False,
            hints=[
                "Click at the end of the `watch_keeper` line and press Enter. "
                "Start like this: `print(\"First watch: \" + `",
                "The `print` glues `\"First watch: \"` to `watch_keeper`, the way `\"Guard: \" + guard` glues words "
                "to the text inside the box `guard`.",
                "Write `print(\"First watch: \" + watch_keeper)` as the last line, under the `watch_keeper` line.",
            ],
            checks=[
                # The class's most common slip: the box's name in quotes shows the letters `watch_keeper`. The words
                # only (the pass/fail is the next check's): say what happened, then take the quotes off.
                (
                    "the box name is not in quotes",
                    "assert ('First watch: ' + str(watch_keeper)) in _lines() or not any('watch_keeper' in _l for _l "
                    "in _lines()), 'Your line shows the word watch_keeper, because of the quotes. Take the quotes off: "
                    "`+ watch_keeper`. " + QUOTES_RULE + "'",
                ),
                out_line("prints the watch line", "'First watch: ' + watch_keeper",
                         "Show `First watch: ` glued to `watch_keeper`. With a made-up name, Tester, it would show "
                         "`First watch: Tester`. Don't type Tester.", privacy=True,
                         spaces="Check the spaces: one after the colon, like `First watch: Tester`."),
                rerun_line("the watch line is built from the box", {"watch_keeper": "Tester"}, "'First watch: Tester'",
                           "Your line has the hero typed in. Glue `\"First watch: \"` to the box instead: "
                           "`\"First watch: \" + watch_keeper`.",
                           show=False),
                rerun_line("the watch line follows another hero", {"watch_keeper": "Zelda"}, "'First watch: Zelda'",
                           "Your line has the hero typed in. Glue `\"First watch: \"` to the box instead: "
                           "`\"First watch: \" + watch_keeper`.",
                           show=False),
            ],
            pass_line="Mar'tu: Hm. Noted. First watch is theirs, then.",
        ),
        dict(
            id="thirty-two-hours",
            text=(
                "Change only `hours_until_burst = 37` to `hours_until_burst = 32`, and press Run. Bomb Shell read the "
                "chalk wall: thirty-two hours, maybe less. Every ledger line changes to match."
            ),
            dictated=True,
            hints=[
                "Look at line 2, `hours_until_burst = 37`. It is the only line to change.",
                "Every ledger line is worked out from `hours_until_burst`. Change it once and press Run again: "
                "every line changes to match.",
                "Change the `37` on line 2 to `32`, and press Run.",
            ],
            checks=[
                set_once("the hours are set once, at the top", ["hours_until_burst"]),
                ("hours_until_burst is 32",
                 "assert hours_until_burst == 32, '`hours_until_burst` is not 32 yet. Change line 2 to "
                 "`hours_until_burst = 32`, then press Run.'"),
                ("the mana line shows 64",
                 "assert 'Mana for the barrier: 64' in _lines(), 'With 32 hours, your mana line should show "
                 "`Mana for the barrier: 64`. Change only line 2, and keep the mana line glued from `str(mana_needed)`.'"),
                # Back to 37 inside the check: a line with 32 typed into it (e.g. `32 * mana_per_hour`) cannot follow.
                rerun_line("the mana line still follows the hours", {"hours_until_burst": 37},
                           "'Mana for the barrier: ' + str(_R('hours_until_burst') * _R('mana_per_hour'))",
                           "A ledger line has 32 typed in. Change only line 2, and keep the box names, not numbers, "
                           "on every other line.",
                           hide=own("watch_keeper")),
                rerun_line("the oil line still follows the hours", {"hours_until_burst": 37},
                           OIL_LINE % ("_R('hours_until_burst') * _R('oil_per_hour')",
                                       "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price')"),
                           "A ledger line has 32 typed in. Change only line 2, and keep the box names, not numbers, "
                           "on every other line.",
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
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4_HALF + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C6 + LEDGER_C7_EMPTY,
        LEDGER_A1 + LEDGER_A2 + LEDGER_B3 + LEDGER_B4 + LEDGER_C + LEDGER_C5 + LEDGER_C6 + LEDGER_C7_BOX,
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
                "```text\nA. what we know\n   37 hours, 2 mana/hour,\n   1 flask/hour, 3 coins/flask\n"
                "B. let the code combine it\n   mana_needed, oil_needed,\n   oil_cost\nC. the ledger\n   three printed lines\n```\n"
                "Each part only uses boxes from the parts above it."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Fill the four boxes in A.\n2. In B, multiply: hours times per hour; flasks times price.\n"
                "3. In C, glue words and `str()` of each box.\n4. Press Run after every line."
            ),
        ),
        dict(
            angle="in Tor",
            label="Why a ledger?",
            text=(
                "The chalk wall says the next burst may come sooner: 32 hours, maybe. If you typed the answers, "
                "every line of the ledger would be wrong. With box names, you change one box and press Run again."
            ),
        ),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In the campaign, the bursts came closer: 48, then 37, then about 32 hours. "
                "Here, I test your ledger with 32 hours, to see if it changes to match."
            ),
        ),
        dict(
            angle="math class",
            label="From math class",
            text=(
                "*Per hour* is a unit rate, like miles per hour. 37 hours at 2 mana per hour is 37 × 2 = 74 mana, "
                "the same way 3 hours at 60 miles per hour is 180 miles."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Lucky's cut",
        text=(
            "Lucky wants his cut. Under your last line:\n"
            "1. Make `glug_sips = 4`, a `glug_price` of your choice, and `glug_fee` worked out from them with `*`.\n"
            "2. Show a divider of 24 `~` marks, stamped with `*`.\n"
            "3. Make `total_coins`, the oil cost plus the glug fee, and show it.\n"
            "4. Show a reserve bar for `reserve = 4` of `reserve_max = 6`, like `[████░░]`."
        ),
        hints=[
            "Glug: `glug_fee = glug_sips * glug_price`. Divider: `print(\"~\" * 24)`.",
            "Bar: `\"[\" + \"█\" * reserve + \"░\" * (reserve_max - reserve) + \"]\"`.",
        ],
        checks=[
            ("glug fee is built from the boxes", "assert glug_fee == glug_sips * glug_price and glug_sips == 4, "
             "'Make `glug_sips = 4`, any `glug_price`, and `glug_fee = glug_sips * glug_price`.'"),
            rerun_box("glug fee follows the price", {"glug_price": 11}, "glug_fee", "_R('glug_sips') * 11",
                      "`glug_fee` has a typed-in number. Use the box names, not numbers: `glug_sips * glug_price`."),
            (
                "divider made with repetition",
                "import ast as _ast\n"
                "_tree = _ast.parse(_source)\n"
                "_stamped = [id(_s) for _n in _ast.walk(_tree) if type(_n).__name__ == 'BinOp' "
                "and type(_n.op).__name__ == 'Mult' for _s in (_n.left, _n.right)]\n"
                "_typed = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Constant' "
                "and type(_n.value).__name__ == 'str' and '~~' in _n.value and id(_n) not in _stamped]\n"
                "assert not _typed, 'Make the divider with repetition: `\"~\" * 24`. Typing the marks is how Lucky loses count.'\n"
                "assert '~' * 24 in _lines(), 'Show a divider of exactly 24 marks: `print(\"~\" * 24)`.'",
            ),
            (
                "total coins",
                "assert total_coins == oil_cost + glug_fee, 'Make `total_coins = oil_cost + glug_fee`.'\n"
                "assert any(str(total_coins) in _l for _l in _lines()), 'Show `total_coins` with `print`.'",
            ),
            rerun_box("total coins follows the hours", {"hours_until_burst": 30}, "total_coins",
                      "_R('hours_until_burst') * _R('oil_per_hour') * _R('oil_price') + _R('glug_fee')",
                      "`total_coins` has a typed-in number. Use the box names, not numbers: `oil_cost + glug_fee`."),
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
            "You've seen this moment: Bomb Shell studied the chalk wall and said thirty-two hours, maybe less. "
            "A ledger written with box names is ready for that news. Change one number."
        ),
    ),
    takeaway=(
        "A ledger written with box names changes to match: change the hours, press Run again, and every line "
        "changes."
    ),
    wrong_answers=[
        dict(why="mana_needed typed (everyone's 68)", code=_ledger(b3="\nmana_needed = 74\n"),
             fails_at=3, message_contains="32"),
        dict(why="a ledger line typed", code=_ledger(c5='print("Mana for the barrier: 74")\n'),
             fails_at=6, message_contains="32"),
        dict(why="oil cost skips the flasks per hour",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = hours_until_burst * oil_price\n"),
             fails_at=5, message_contains="oil_per_hour"),
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
             fails_at=8, message_contains="no name in front"),
        dict(why="the watch line typed", code=_ledger(c7='watch_keeper = "Bomb Shell"\nprint("First watch: Bomb Shell")\n'),
             fails_at=9, message_contains="Tester"),
        dict(why="the oil line with a missing space",
             code=_ledger(c6='print("Lantern oil: " + str(oil_needed) + "flasks for " + str(oil_cost) + " coins")\n'),
             fails_at=7, message_contains="space"),
        dict(why="mana per hour typed into mana_needed (passes an hours-only rerun)",
             code=_ledger(b3="\n# B. Let the code combine it\nmana_needed = hours_until_burst * 2\n"),
             fails_at=3, message_contains="mana_per_hour = 3"),
        dict(why="oil price typed into oil_cost (passes an hours-only rerun)",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = oil_needed * 3\n"),
             fails_at=5, message_contains="oil_price = 5"),
        dict(why="gaming the message: the typed watch line plus the Tester line the message showed",
             code=_ledger(c7='watch_keeper = "Bomb Shell"\nprint("First watch: Bomb Shell")\nprint("First watch: Tester")\n'),
             fails_at=9, message_contains="typed in"),
        dict(why="gaming: the hero set to the rerun's Tester, then the watch line typed",
             code=_ledger(c7='watch_keeper = "Tester"\nprint("First watch: Tester")\n'), fails_at=9, message_contains="Zelda"),
        dict(why="the hint's name copied: the hero in `guard`, watch_keeper left empty",
             code=_ledger(c7='watch_keeper = ""\nguard = "Bomb Shell"\nprint("First watch: " + guard)\n'),
             fails_at=8, message_contains="new box `guard`"),
        dict(why="capital letter: Watch_keeper",
             code=_ledger(c7='watch_keeper = ""\nWatch_keeper = "Bomb Shell"\nprint("First watch: " + Watch_keeper)\n'),
             fails_at=8, message_contains="letter for letter"),
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
             fails_at=6, message_contains="mana_per_hour = 3"),
        dict(why="LINE-TOTAL: the hours times the mana total 74",
             code=_ledger(b3="\n# B. Let the code combine it\nmana_needed = hours_until_burst * 74\n"),
             fails_at=3, message_contains="already worked out"),
        dict(why="LINE-TOTAL: the flasks times the oil total 111",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = oil_needed * 111\n"),
             fails_at=5, message_contains="price of ONE flask"),
        dict(why="split task: oil_needed worked out, oil_cost left at its 0",
             code=_ledger(b4="oil_needed = hours_until_burst * oil_per_hour\noil_cost = 0\n"), fails_at=5,
             message_contains="placeholder"),
        dict(why="split task: oil_needed typed in as 37", code=_ledger(b4="oil_needed = 37\noil_cost = oil_needed * oil_price\n"),
             fails_at=4, message_contains="typed-in"),
        dict(why="split task: the hero put in, but no watch line yet",
             code=_ledger(c7='watch_keeper = "Bomb Shell"  # any hero, in quotes\n'), fails_at=9,
             message_contains="glued to `watch_keeper`"),
        dict(why="split task: the watch line glued to the word watch_keeper in quotes",
             code=_ledger(c7='watch_keeper = "Bomb Shell"\nprint("First watch: " + "watch_keeper")\n'), fails_at=9,
             message_contains="because of the quotes. Take the quotes off"),
        dict(why="the last task not done: the hours still 37", code=_ledger(), fails_at=10,
             message_contains="`hours_until_burst = 32`"),
        dict(why="the last task as a new line at the bottom (side-work habit): the ledger never sees 32",
             code=_ledger() + "hours_until_burst = 32\n", fails_at=3, message_contains="top to bottom"),
        dict(why="the last task changes the wrong box (mana_per_hour to 32)",
             code=_ledger(a2="mana_per_hour = 32\noil_per_hour = 1\noil_price = 3\n"), fails_at=2,
             message_contains="2 mana each hour"),
        dict(why="after the change, 64 typed into mana_needed",
             code=_ledger(a1=LEDGER_A1_32, b3="\n# B. Let the code combine it\nmana_needed = 64\n"),
             fails_at=3, message_contains="stayed 64"),
        dict(why="after the change, the hours typed into mana_needed (passes every rerun at 32)",
             code=_ledger(a1=LEDGER_A1_32, b3="\n# B. Let the code combine it\nmana_needed = 32 * mana_per_hour\n"),
             fails_at=10, message_contains="`hours_until_burst = 37`"),
        dict(why="after the change, the hours typed into oil_needed (passes every rerun at 32)",
             code=_ledger(a1=LEDGER_A1_32, b4="oil_needed = 32 * oil_per_hour\noil_cost = oil_needed * oil_price\n"),
             fails_at=10, message_contains="Lantern oil: 37 flasks for 111 coins"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="combine-values,concat-str,make-variable", solo="false",
             dictates="1,10", foreign_names="days,meals_per_day,bags,bag_price,guard,steps,sips") + "\n"
        "Structure pass (guide 9, S12): two packed tasks are now four, each with its own hints and checks. The old "
        "task 4 (oil_needed and oil_cost) is task 4 (oil_needed, the old id oil-needed-and-cost, so a pass already "
        "saved still counts) and task 5 (oil-cost). The old task 7 (put a hero in, then print the watch line) is "
        "task 8 (watch-keeper, the old id) and task 9 (watch-line). Ten tasks, nine partials (B4_HALF and "
        "C7_BOX are the new in-between states), and the wrong answers moved to their new task numbers. Ledger "
        "slots say 'this task' (the screen says Your tasks). "
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
        "uses 32 (the ledger at 37 is the last partial). set_once on tasks 3, 4, 5 and 10 gives `hours_until_burst = 32` "
        "added at the bottom a top-down message (task 10's copy matters on the site, where task 3 stays green from "
        "an earlier run). Task 10 reruns at 37: a line with 32 typed into it cannot follow. The side quest's total "
        "reruns at 30 hours (the finished ledger is already at 32)."
    ),
)

ITEMS = [REMEMBERS_1C, LESSON_1C, EXTRA_1X_C, QUIZ_1, PROJECT_1P1]
