"""Unit 2 "Control Flow", part a: Mar'tu remembers (2a-remembers) and Lesson 2A "True or False, Yes?".

Spec: design/curriculum.md, "## Unit 2 · Control Flow", item 1 (2a-remembers; 2A-01 to 2A-05, 2A-S).
Introduces const:bool, op:Gt, op:Lt (2A-01), op:Eq, op:NotEq (2A-02), op:GtE, op:LtE (2A-03) and attr:lower (2A-04).
No `if` yet: that starts in 2B. Every answer here is a True or False kept in a box or printed.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`return roll >= required_roll` at the trap door, `user.clicked() == "option 1"` in the dialogue part,
`dialogue_input.lower()` in Mar'tu's line and `caster["mana"] < spell["mana_cost"]` in `cast_spell`. Campaign links
are "you've seen this, now you'll get it" moments. Every student has their own device; pair talk is optional and
every checkpoint is solo.

Help ladder as fields (same as Unit 1): hints[0] Start me off, hints[1] Point (where to look), another_way,
hints[2+] Teach (a tiny example with other names), assemble = More structure, solution = Show.
Rung 0 follows the help-stack contract (2.2) as written: the line's left side or first tokens only, stopping
before the sign (`passed = roll `, `print(clock_color `), so it never makes the step's decision. A bonus's rung 0
is a few tokens (`close_call = `). In the debug steps (2A-05, 2A-S) rung 0 is "Read Python's last line" (or, for a
quiet bug, the last line the program printed). The SOLO sets `explainer="lean"`: the crash explainer names the
kind of slip and the line, not the fix (not applied back to the live Unit 1).
Terminology (2.9): "box (variable)" in Units 1-2; `=` is read "gets", `==` is read "is the same as".

Check builders below (plain string templates; messages never repeat a student's own text back):
  bool_box()    the box exists and holds True or False. NAME / LEFT / BARE (a question kept nowhere) / `:` for `=` /
                two `=` signs in one line / `==` used to fill a box / text or a number instead of True or False
  flip()        CMB on printed output: a line that ended in `True` must end in `False` when the check changes a
                box (catches `print(True)`, a typed `print(6 < 15)` and half-typed lines like `print(dex < 15)`).
                It reads each line's last word, so a label passes (`print("Less?", dex < needed)`). `rel=` sets the
                rerun value from the student's own other box (dex = needed + 1), so changed numbers still pass.
  rerun_bool()  CMB on one box: after the check changes some boxes, the box must hold the new right answer
  bnd()         BND (2.5): reruns at needed - 1, needed, needed + 1 (needed read from the student's own code),
                then moves `needed` too, so a typed number (`roll >= 15`) is caught. A mirrored sign
                (`roll <= needed`, `needed >= roll`) gets its own "faces the wrong way" note.
  no_is()       `is` / `is not` in a comparison on the step's boxes. `hero is "Lucky"` reads like English and even
                comes out right for two literals, so only this check catches it.
  strexact()    STREXACT: quoted text in a comparison differs from the wanted text only by capitals or spaces
                (the all-small spelling next to a `.lower()` copy is fine)
  quoted_name() a box's name in quotes inside a comparison (`"hero" == "Lucky"`)
  no_quoted_question()  a printed line that shows the question itself (`print("dex < needed")`), but not a line
                that ends in its answer
  print_check() PRINT (from Unit 1): print(name), not the value typed by hand, and AFTER the box's last `=` line
                (read from the code: True and False appear on other lines, so the console cannot tell)
Rerun messages (teacher ruling on the Unit 2 reviews): the fix comes first, and the evidence goes in brackets at
the end, "(Mar'tu's check tried `dex = 16`, only inside the check: ...)", about 35 words or fewer in all. So the
student reads what to do before why, and the rerun still reads as fair, not as a trick. A box the starter makes
that has gone missing gets "Keep the box `x` from the starter" (STARTER_BOXES, and `kept=True` in bool_box); a
box the student makes gets "Make a box named `x`". A box still holding the starter's placeholder says so.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u02a
"""

# ---------------------------------------------------------------------------------------------
# Check builders
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."

# Which names the student made, a near-miss test, lone values, and the namespace (same as Unit 1's _NAMES_PRE).
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

# The boxes the reruns change that the exercise's own starter makes (dex, needed, clock_color, hero, roll, mana,
# cost, answer). The bonus boxes (martu_color, lucky_color, first, second) are the student's own.
STARTER_BOXES = ["dex", "needed", "clock_color", "hero", "roll", "mana", "cost", "answer"]

# CMB: re-run the student's program with some `name = <literal>` lines changed (Unit 1's _rerun, unchanged).
# Prints go to a private buffer; the student's own code and values are never touched. `_gone(name)` is the
# message for a box the rerun needs that is not there; `_keepline(name, kind)` for a box made some other way.
_RERUN_DEF = (
    f"_KEPT = {STARTER_BOXES!r}\n"
    "def _gone(_k):\n"
    "    if _k in _KEPT:\n"
    "        return 'Keep the box `' + _k + '` from the starter: a line that starts `' + _k + ' = `.'\n"
    "    return 'Make a box named `' + _k + '`: start a line with `' + _k + ' = `.'\n"
    "def _keepline(_k, _kind):\n"
    "    return ('Keep the line that sets `' + _k + '` as `' + _k + \" = value`. Mar'tu's check changes that line \"\n"
    "            'to try other ' + _kind + '.')\n"
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
)


def _fmt(value):
    return '"' + value + '"' if isinstance(value, str) else str(value)


def _with_text(changes):
    parts = ["`%s = %s`" % (key, _fmt(value)) for key, value in changes.items()]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def _kind(changes):
    return "numbers" if all(type(v) is int for v in changes.values()) else "values"


def _ev(changes):
    """The evidence bracket's opening, for fixed changes: `(Mar'tu's check tried `dex = 16`, only inside the check`."""
    return "(Mar'tu's check tried %s, only inside the check" % _with_text(changes)


# The rerun crashed: the fix (work for other values too) first, Python's own words, then the evidence.
_CRASH = (
    "'Make your code work for other ' + _kd + ' too. With them, Python stopped: ' + _e + ' ' + _ev_txt + '.)'"
)


def _rerun_pre(changes):
    """Run the rerun and stop early (with a kind message) when it cannot be done or crashes. Sets `_ev_txt`, the
    evidence bracket's opening, for the message that follows."""
    return _RERUN_DEF + (
        f"_r, _p, _f, _e = _rerun({changes!r})\n"
        "_R = _r.get\n"
        "_g0 = globals()\n"
        f"_kd = {_kind(changes)!r}\n"
        f"_ev_txt = {_ev(changes)!r}\n"
        f"_miss = [_k for _k in {list(changes)!r} if _k not in _f]\n"
        "assert not _miss or _miss[0] in _g0, _gone(_miss[0] if _miss else '')\n"
        "assert not _miss, _keepline(_miss[0] if _miss else '', _kd)\n"
        f"assert not _e, {_CRASH}\n"
    )


# The answer a printed line shows is its last word, so a label is fine: `print("Less?", dex < needed)` shows
# `Less? True`. Trailing marks are ignored (`True.`).
_END_DEF = "_end = lambda _s: ((_s.split() or [''])[-1]).rstrip('.,!?;:)')\n"


def flip(label, changes, before, after, fix, rel=None):
    """CMB on printed output: some line ended in `before` in the student's run and ends in `after` in the rerun.
    A typed answer (`print(True)`, `print(6 < 15)`) prints the same both times, so it never flips.
    `rel` = {name: (other_box, offset)}: try `name = <the student's own other_box> + offset` instead of the fixed
    number in `changes`, so a student who changed the numbers still gets a fair test (the fixed number is used
    when the other box does not hold a whole number).
    Message: the fix, then "(Mar'tu's check tried `dex = 16`, only inside the check: the answer should turn
    `False`, but it stayed the same.)"."""
    if not rel:
        pre = _rerun_pre(changes)
    else:
        pre = _RERUN_DEF + (
            "_g0 = globals()\n"
            f"_ch = dict({changes!r})\n"
            f"for _k, (_o, _d) in {rel!r}.items():\n"
            "    if type(_g0.get(_o)).__name__ == 'int':\n"
            "        _ch[_k] = _g0[_o] + _d\n"
            "_r, _p, _f, _e = _rerun(_ch)\n"
            f"_kd = {_kind(changes)!r}\n"
            "_with = ' and '.join('`' + _k + ' = ' + str(_v) + '`' for _k, _v in _ch.items())\n"
            "_ev_txt = \"(Mar'tu's check tried \" + _with + ', only inside the check'\n"
            "_miss = [_k for _k in _ch if _k not in _f]\n"
            "assert not _miss or _miss[0] in _g0, _gone(_miss[0] if _miss else '')\n"
            "assert not _miss, _keepline(_miss[0] if _miss else '', _kd)\n"
            f"assert not _e, {_CRASH}\n"
        )
    turn = ": the answer should turn `" + after + "`, but "
    same = "it stayed the same.)"
    other = "no line changed from `" + before + "` to `" + after + "`.)"
    code = pre + _END_DEF + (
        "_old = _lines()\n"
        f"_at = [_i for _i, _l in enumerate(_p) if _end(_l) == {after!r} and _i < len(_old) and _end(_old[_i]) == {before!r}]\n"
        f"assert _at, {fix + ' '!r} + _ev_txt + {turn!r} + ({same!r} if _p == _old else {other!r})\n"
    )
    return (label, code)


def no_is(label, names, msg=None):
    """`is` / `is not` in a comparison that uses one of these boxes. `hero is "Lucky"` reads like English and can
    even come out right here, but `is` does not ask whether two values match, so it fails on typed answers later.
    Scoped to the step's own boxes, so a slip in another step stays there."""
    msg = msg or (
        "`is` asks a different question in Python, and it can say False even when two values match. Use `==` "
        "for *is the same as*, and `!=` for *is not the same as*."
    )
    code = (
        "import ast as _ast\n"
        "_bad = [_n.lineno for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare' "
        "and any(type(_o).__name__ in ('Is', 'IsNot') for _o in _n.ops) "
        "and any(type(_x).__name__ == 'Name' and _x.id in " + repr(list(names)) + " "
        "for _c in [_n.left] + list(_n.comparators) for _x in _ast.walk(_c))]\n"
        f"assert not _bad, 'Line ' + str(_bad[0] if _bad else 0) + ': ' + {msg!r}\n"
    )
    return (label, code)


def rerun_bool(label, changes, target, want, fix):
    """CMB on one box: after the rerun, `target` must hold `want` (an expression over _R, the rerun's names).
    Message: the fix, then "(Mar'tu's check tried `hero = "Lucky"`, only inside the check: `is_lucky` stayed
    False, but it should be True.)". When the tried values are the ones already in the code (the starter's
    `answer = "YES"`), the bracket says so instead of claiming a change: "(With `answer = "YES"`, as in your code
    now, `said_yes` is False, but it should be True.)"."""
    asnow = "(With " + _with_text(changes) + ", as in your code now, `" + target + "` is "
    code = _rerun_pre(changes) + (
        f"_want = {want}\n"
        f"_got = _R({target!r})\n"
        f"_was = _g0.get({target!r})\n"
        "_isb = type(_got).__name__ == 'bool'\n"
        "_should = str(_got) + ', but it should be ' + str(_want) + '.)'\n"
        f"if all(_g0.get(_k) == _v for _k, _v in {changes!r}.items()):\n"
        f"    _said = {asnow!r} + (_should if _isb else 'not True or False.)')\n"
        "else:\n"
        f"    _said = _ev_txt + ': `' + {target!r} + '` ' + ((('stayed ' if _got == _was else 'became ') + _should) "
        "if _isb else 'held something that is not True or False.)')\n"
        f"assert _isb and _got == _want, {fix + ' '!r} + _said\n"
    )
    return (label, code)


def bnd(label, target, left, right, verb, *, short_fix, exact_fix, over_fix, shift_fix, lt_note="", rev_fix=None):
    """BND (2.5): `target` must say whether `left` reaches `right`. `right` is read from the student's own code,
    so any chosen difficulty passes. Reruns: one short (False), exactly enough (True), one over (True), then
    `right` moved up by 3 with `left` exactly on it (True) and one short of it (False): that last pair catches a
    typed number such as `roll >= 15` (its fix is `shift_fix`). The first wrong case is the message: the fix, then
    "(Mar'tu's check tried `roll = 14` and `needed = 15`, only inside the check: `passed` was True, so one short
    passed.)". `verb` is "pass" or "cast". `lt_note` follows the one-short fix only when the student's code uses
    `<` (the campaign's *not enough* test). When the sign faces the wrong way (`roll <= needed` or
    `needed >= roll`: *at most*, the class's mirror slip), `rev_fix` takes the one-short fix's place."""
    if rev_fix is None:
        rev_fix = "Your sign faces the wrong way: it asks *at most*. *At least* is `>=`."
    did, did_not = {"pass": ("passed", "did not pass"), "cast": ("could cast", "could not cast")}[verb]
    fixes = {"short": short_fix, "exact": exact_fix, "over": over_fix, "shift": shift_fix}
    said = {
        "short": "was True, so one short " + did + ".)",
        "exact": "was False, so exactly enough " + did_not + ".)",
        "over": "was False, so more than enough " + did_not + ".)",
    }
    code = _RERUN_DEF + (
        "_g0 = globals()\n"
        f"_T, _L, _Rt = {target!r}, {left!r}, {right!r}\n"
        f"_fixes = {fixes!r}\n"
        f"_said = {said!r}\n"
        "_rev_at = [1 for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare' and len(_n.ops) == 1 "
        "and ((getattr(_n.left, 'id', ''), type(_n.ops[0]).__name__, getattr(_n.comparators[0], 'id', '')) "
        "in ((_L, 'LtE', _Rt), (_Rt, 'GtE', _L)))]\n"
        f"_lt = {lt_note!r} if _uses('op:Lt') and not _rev_at else ''\n"
        f"_rev = {rev_fix!r} if _rev_at else ''\n"
        "_base = _g0.get(_Rt)\n"
        "_msg = ''\n"
        "if _Rt not in _g0:\n"
        "    _msg = _gone(_Rt)\n"
        "elif type(_base).__name__ != 'int':\n"
        "    _msg = '`' + _Rt + '` should hold a whole number, with no quotes. Numbers don' + chr(39) + 't need quotes.'\n"
        "else:\n"
        # (changes, wanted answer, which case the bracket names, which fix leads)
        "    _cases = [({_L: _base - 1}, False, 'short', 'short'), ({_L: _base}, True, 'exact', 'exact'),\n"
        "              ({_L: _base + 1}, True, 'over', 'over'), ({_Rt: _base + 3, _L: _base + 3}, True, 'exact', 'shift'),\n"
        "              ({_Rt: _base + 3, _L: _base + 2}, False, 'short', 'shift')]\n"
        "    for _ch, _want, _case, _fx in _cases:\n"
        "        _r, _p, _f, _e = _rerun(_ch)\n"
        "        _ev_txt = (\"(Mar'tu's check tried `\" + _L + ' = ' + str(_ch[_L]) + '` and `' + _Rt + ' = ' + "
        "str(_ch.get(_Rt, _base)) + '`, only inside the check')\n"
        "        _miss = [_k for _k in _ch if _k not in _f]\n"
        "        _got = _r.get(_T)\n"
        "        if _miss:\n"
        "            _msg = _gone(_miss[0]) if _miss[0] not in _g0 else _keepline(_miss[0], 'numbers')\n"
        "        elif _e:\n"
        "            _kd = 'numbers'\n"
        f"            _msg = {_CRASH}\n"
        "        elif type(_got).__name__ != 'bool':\n"
        "            _msg = ('Make `' + _T + '` hold a yes/no answer, `True` or `False`. ' + _ev_txt + ': `' + _T + "
        "'` held something else.)')\n"
        "        elif _got != _want:\n"
        "            _lead = (_rev or _fixes[_fx] + _lt) if _fx == 'short' else _fixes[_fx]\n"
        "            _msg = _lead + ' ' + _ev_txt + ': `' + _T + '` ' + _said[_case]\n"
        "        if _msg:\n"
        "            break\n"
        "assert not _msg, _msg\n"
    )
    return (label, code)


def _gone_text(name, kept):
    """The missing-box message (the same words as `_gone` inside the rerun checks)."""
    if kept:
        return "Keep the box `" + name + "` from the starter: a line that starts `" + name + " = `."
    return "Make a box named `" + name + "`: start a line with `" + name + " = `."


CHAIN = (
    " has two `=` signs, so it puts the same value in two boxes. This box should hold a yes/no answer, "
    "`True` or `False`: ask the question with `==`."
)


def bool_box(label, name, *, known, foreign=(), rules=(), text_msg=None, kept=False):
    """The box exists and holds True or False, or the message says why not (in this order): two `=` signs in one
    line, `==` used to fill the box, the exercise's own rules [(condition, message)], text, a number; and when the
    box is missing: `:` instead of `=`, a near-miss name (NAME), an example's name (LEFT), a question kept in no
    box (BARE), or the plain message: "Keep the box `x` from the starter" when the starter makes it (`kept=True`),
    else "Make a box named `x`"."""
    text_msg = text_msg or (
        "`" + name + "` holds text, because of the quotes. It should hold a yes/no answer, `True` or `False`."
    )
    rule_code = "".join(f"    if not _msg and ({cond}):\n        _msg = {message!r}\n" for cond, message in rules)
    cmp_on = (
        " asks whether `" + name + "` is the same as something, with `==`. That does not change the box. "
        "To put a value in, use one `=`."
    )
    code = _NAMES_PRE + (
        f"_name = {name!r}\n"
        f"_known = {list(known)!r}\n"
        f"_foreign = {list(foreign)!r}\n"
        "_have = _g.get(_name)\n"
        "_msg = ''\n"
        "_ann = [_n.lineno for _n in _ast.walk(_tree) if type(_n).__name__ == 'AnnAssign' "
        "and getattr(_n.target, 'id', '') == _name]\n"
        "_chain = [_n.lineno for _n in _ast.walk(_tree) if type(_n).__name__ == 'Assign' and len(_n.targets) > 1 "
        "and any(getattr(_t, 'id', '') == _name for _t in _n.targets)]\n"
        "_cmp = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare']\n"
        "_cmp_on = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare' "
        "and getattr(_n.value.left, 'id', '') == _name]\n"
        # `passed == roll >= needed` under an earlier `passed = False`: the = / == slip, even though the box holds a bool.
        "if _name in _g and _cmp_on:\n"
        f"    _msg = 'Line ' + str(_cmp_on[0]) + {cmp_on!r}\n"
        "if not _msg and _name in _g and type(_have).__name__ != 'bool':\n"
        "    if _chain:\n"
        f"        _msg = 'Line ' + str(_chain[0]) + {CHAIN!r}\n"
        f"{rule_code}"
        "    if not _msg and type(_have).__name__ == 'str':\n"
        f"        _msg = {text_msg!r}\n"
        "    if not _msg and type(_have).__name__ in ('int', 'float'):\n"
        f"        _msg = {'`' + name + '` holds a number. It should hold a yes/no answer, `True` or `False`.'!r}\n"
        "    if not _msg:\n"
        f"        _msg = {'`' + name + '` should hold a yes/no answer, `True` or `False`.'!r}\n"
        "if _name not in _g:\n"
        "    _near = [_m for _m in _made if _m != _name and _m not in _known and _m not in _foreign and _close(_m, _name)]\n"
        "    _left = [_m for _m in _made if _m in _foreign]\n"
        "    if _ann:\n"
        f"        _msg = 'Line ' + str(_ann[0]) + {' uses `:` after `' + name + '`. To put a value in a box, use `=`.'!r}\n"
        "    elif _near:\n"
        f"        _msg = 'Python matches names letter for letter: you wrote `' + _near[0] + {'`, the task needs `' + name + '`.'!r}\n"
        "    elif _left:\n"
        f"        _msg = '`' + _left[0] + {'` is a name from the example or a hint. This task' + chr(39) + 's box is `' + name + '`.'!r}\n"
        "    elif _cmp:\n"
        f"        _msg = 'Line ' + str(_cmp[0]) + {' asks a question, but keeps the answer nowhere. Put `' + name + ' = ` in front of it.'!r}\n"
        "    else:\n"
        f"        _msg = {_gone_text(name, kept)!r}\n"
        "assert not _msg, _msg\n"
    )
    return (label, code)


def strexact(label, want, ops=None):
    """STREXACT: quoted text in a comparison differs from `want` only by capitals or spaces (`"Red"` for `"red"`).
    `ops` limits it to comparisons using those signs (e.g. ("NotEq",)). A comparison with a `.lower()` copy on
    one side (`hero.lower() == "lucky"`) ignores capitals on purpose, so the all-small spelling is left alone
    there (a stray space is still caught)."""
    op_test = f" and any(type(_o).__name__ in {tuple(ops)!r} for _o in _n.ops)" if ops else ""
    head = '`"'
    tail = '"` and `"' + want + '"` are different text to Python: every letter, space and capital counts.'
    code = (
        "import ast as _ast\n"
        f"_want = {want!r}\n"
        "_key = lambda _s: ''.join(_c for _c in _s.lower() if not _c.isspace())\n"
        "_lowered = lambda _n: any(type(_c).__name__ == 'Call' and getattr(_c.func, 'attr', '') == 'lower' "
        "for _c in [_n.left] + list(_n.comparators))\n"
        "_odd = []\n"
        "for _n in _ast.walk(_ast.parse(_source)):\n"
        f"    if type(_n).__name__ == 'Compare'{op_test}:\n"
        "        for _c in [_n.left] + list(_n.comparators):\n"
        "            if type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'str' "
        "and _c.value != _want and _key(_c.value) == _key(_want) "
        "and not (_lowered(_n) and _c.value == _want.lower()):\n"
        "                _odd.append(_c.value)\n"
        f"assert not _odd, {head!r} + (_odd[0] if _odd else '') + {tail!r}\n"
    )
    return (label, code)


def quoted_name(label, names):
    """A box's name in quotes inside a comparison: `"hero" == "Lucky"` compares two words and is always False."""
    code = (
        "import ast as _ast\n"
        "_q = [_c.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare' "
        "for _c in [_n.left] + list(_n.comparators) if type(_c).__name__ == 'Constant' "
        f"and _c.value in {list(names)!r}]\n"
        "assert not _q, '`\"' + (_q[0] if _q else '') + '\"` in quotes is just that word, not the box. ' + "
        f"{QUOTES_RULE!r}\n"
    )
    return (label, code)


def no_quoted_question(label, words, signs):
    """A printed line that shows the question itself: the question was in quotes, so Python showed the letters.
    A line that ends in the answer (`dex < needed: True`, a label plus the question) is fine."""
    msg = "That printed the letters, because of the quotes. Take the quotes off so Python works out the question. " + QUOTES_RULE
    code = _END_DEF + (
        f"_bad = [_l for _l in _lines() if any(_w in _l for _w in {list(words)!r}) and any(_s in _l for _s in {list(signs)!r}) "
        "and _end(_l) not in ('True', 'False')]\n"
        f"assert not _bad, {msg!r}\n"
    )
    return (label, code)


def print_check(name, missing=None):
    """PRINT (Unit 1): print(name) with no quotes (not the word, not a value typed by hand), and the value shows.
    The box may be glued or labelled (`print("Barrier:", barrier_up)`, `str(barrier_up)`). Order is read from
    the code, not the console: True and False show up from other lines too, so a `print(barrier_up)` that runs
    while the box still holds 0 must not pass because another line printed True."""
    missing = missing or f"Add a line that prints the box: `print({name})`."
    code = (
        "import ast as _ast\n"
        "_tree = _ast.parse(_source)\n"
        "_pcalls = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Call' "
        "and type(_n.func).__name__ == 'Name' and _n.func.id == 'print']\n"
        "_args = [_a for _n in _pcalls for _a in _n.args]\n"
        f"_inside = lambda _a: any(type(_x).__name__ == 'Name' and _x.id == '{name}' for _x in _ast.walk(_a))\n"
        "_named = [_a for _a in _args if _inside(_a)]\n"
        f"_quoted = [_a for _a in _args if type(_a).__name__ == 'Constant' and _a.value == '{name}']\n"
        f"_typed = [_a for _a in _args if type(_a).__name__ == 'Constant' and _a.value != '{name}' "
        f"and str(_a.value).strip() == str(globals().get('{name}')).strip()]\n"
        f"_sets = [(_n.end_lineno, _n.end_col_offset) for _n in _tree.body if type(_n).__name__ in ('Assign', 'AugAssign') "
        f"and any(getattr(_t, 'id', '') == '{name}' for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target]))]\n"
        "_after = [_n for _n in _pcalls if any(_inside(_a) for _a in _n.args) "
        "and (not _sets or (_n.lineno, _n.col_offset) > max(_sets))]\n"
        f"assert _named or not _typed, 'That `print` shows a value typed by hand. Print the box instead: "
        f"`print({name})`, so Python opens it and shows what is inside.'\n"
        f"assert _named or not _quoted, 'That prints the word \"{name}\". Take the quotes off so Python opens the box.'\n"
        f"assert _named, {missing!r}\n"
        f"assert _after and any(str({name}).strip() in _l for _l in _lines()), "
        f"'Your `print({name})` runs before `{name}` gets its last value. "
        f"Move it below the line that puts the value in.'"
    )
    return (f"prints the box {name}", code)


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# UNIT (repeated in every part file of control-flow)
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
        term="True and False",
        aliases=["True", "False", "True or False", "bool", "bools", "boolean", "booleans", "yes/no answer"],
        plain=(
            "Python's yes and no. They have capital letters and no quotes. A question like `6 > 15` gives back "
            "one of them."
        ),
        example="print(18 > 12)",
    ),
    dict(
        term="comparison",
        aliases=["comparisons", "compare", "comparison sign", "comparison signs"],
        plain=(
            "A yes/no question about two values, like `dex < needed`. The signs are `<` `>` `<=` `>=` `==` `!=`. "
            "Python answers `True` or `False`."
        ),
        example="dex < needed",
    ),
    dict(
        term="is the same as",
        aliases=["==", "double equals", "is not the same as", "!="],
        plain=(
            "`==` asks whether two values are the same. `!=` asks whether they are different. One `=` does "
            "something else: it puts a value in a box (read it as *gets*)."
        ),
        example='clock_color == "red"',
    ),
    dict(
        term="at least",
        aliases=[">=", "at most", "<=", "exactly enough", "boundary"],
        plain=(
            "`>=` means *at least*: exactly the number still counts. `<=` means *at most*. `>` and `<` leave the "
            "number itself out."
        ),
        example="roll >= needed",
    ),
    dict(
        term=".lower()",
        aliases=["lower()", "lower", "lower-case copy"],
        plain=(
            "The dot means: ask this text to do something. `.lower()` gives a copy in small letters. "
            "The text in the box does not change."
        ),
        example='"YES".lower()',
    ),
]

# ---------------------------------------------------------------------------------------------
# Mar'tu remembers... (2a-remembers)
# ---------------------------------------------------------------------------------------------

REMEMBERS_2A = dict(
    kind="quiz",
    id="2a-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from Unit 1. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 2A; recall from 1C (a stamped bar; how many "
        "versus the price of one). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="stamp-a-bar",
            q="What will this print?",
            code='print("█" * 2 + "░" * 3)\n',
            answer="██░░░",
            choices=["██░░░", "█░█░█", "█░", "█2░3"],
            explain=(
                "`*` stamps a mark: `\"█\" * 2` is `██` and `\"░\" * 3` is `░░░`. Then `+` glues them, with no "
                "space between."
            ),
        ),
        dict(
            type="mc",
            id="which-is-how-many",
            q="In `rope_count * rope_price`, which one is *how many*?",
            choices=["rope_count", "rope_price"],
            answer=0,
            why_wrong={1: "`rope_price` is how much one coil costs. `rope_count` is how many coils."},
            explain="A cost is how many times the price of one: `rope_count` is how many, `rope_price` is the price of one.",
        ),
    ],
)

# ---------------------------------------------------------------------------------------------
# Lesson 2A "True or False, Yes?"
# ---------------------------------------------------------------------------------------------

# 2A-01 ------------------------------------------------------------------------------------------

DEX_STARTER = "dex = 6\nneeded = 15\nprint(dex > needed)\nbarrier_up = 0\n"
DEX_KNOWN = ["dex", "needed", "barrier_up"]
DEX_FOREIGN = ["owls", "wolves", "door_open"]


def _dex(line="print(dex < needed)", barrier="barrier_up = True\nprint(barrier_up)"):
    return f"dex = 6\nneeded = 15\n{line}\n{barrier}\n"


TRUE_OR_FALSE = dict(
    id="true-or-false",
    title="True or False",
    martu=(
        "A [[comparison]] is a yes/no question. Python answers [[True and False|True or False]], with no quotes.\n"
        "`>` asks: is it more than? `<` asks: is it less than? The wide side of the sign faces the bigger number.\n"
        "Guess first, then press Run."
    ),
    introduces=["const:bool", "op:Gt", "op:Lt"],
    example="owls = 9\nwolves = 4\nprint(owls > wolves)\n",
    example_output="True",
    names=["dex", "needed", "barrier_up"],
    predict=dict(
        q="Bomb Shell's DEX is 6. The latch needs 15. What will these two lines print?",
        code="print(18 > 12)\nprint(6 > 15)\n",
        choices=["True\nFalse", "True\nTrue", "18 > 12\n6 > 15", "Yes\nNo"],
        answer=0,
        explain=(
            "Python works out each question and prints the answer: `True` for yes, `False` for no. "
            "6 is not more than 15, so Bomb Shell's hands lose to the latch. *That latch hates me.*"
        ),
    ),
    pair_talk=(
        "Pair talk: each of you guesses the two lines before you run. Compare guesses. Then each of you runs your "
        "own code and checks."
    ),
    starter=DEX_STARTER,
    checkpoints=[
        dict(
            id="less-than",
            text="Change the `print` to show whether `dex` is *less than* `needed`.",
            dictated=True,
            hints=[
                "Start like this: `print(dex `",
                "Look at the sign between `dex` and `needed`. Which way should it face?",
                "`<` means *less than*. `3 < 5` is True; `5 < 3` is False.",
            ],
            checks=[
                no_quoted_question("no quotes around the question", ["dex", "needed"], ["<", ">"]),
                (
                    "the question asks less than",
                    # Direction of every dex/needed comparison: `dex < needed` and `needed > dex` ask less than.
                    "import ast as _ast\n"
                    "_less, _more = 0, 0\n"
                    "for _n in _ast.walk(_ast.parse(_source)):\n"
                    "    if type(_n).__name__ == 'Compare' and len(_n.ops) == 1:\n"
                    "        _a, _b, _o = getattr(_n.left, 'id', ''), getattr(_n.comparators[0], 'id', ''), type(_n.ops[0]).__name__\n"
                    "        if (_a, _b) == ('dex', 'needed'):\n"
                    "            _less += _o in ('Lt', 'LtE')\n"
                    "            _more += _o in ('Gt', 'GtE')\n"
                    "        elif (_a, _b) == ('needed', 'dex'):\n"
                    "            _less += _o in ('Gt', 'GtE')\n"
                    "            _more += _o in ('Lt', 'LtE')\n"
                    "assert _less or not _more, ('Your line still asks whether `dex` is *more than* `needed`. '\n"
                    "    'Change the sign so it asks *less than*: the wide side faces the bigger number.')",
                ),
                (
                    "prints True",
                    _END_DEF
                    + "_ends = [_end(_l) for _l in _lines()]\n"
                    "assert 'True' in _ends, ('Your line prints `False`. `dex` is less than `needed`, so the answer '\n"
                    "    'should be `True`. Change the sign so it asks *less than*.' if 'False' in _ends else "
                    "'Nothing prints `True` yet. Change the `print` so it asks whether `dex` is less than `needed`.')",
                ),
                # dex one more than the student's own needed (16 for the starter's 15), needed one less than dex (5).
                flip("the answer follows dex", {"dex": 16}, "True", "False",
                     "Print the question itself, with the boxes, so Python works out the answer each time.",
                     rel={"dex": ("needed", 1)}),
                flip("the answer follows needed", {"needed": 5}, "True", "False",
                     "Use the box `needed` too, not a number you typed.", rel={"needed": ("dex", -1)}),
                # The mirror boundary slip: `<=` (or `dex < needed + 1`) also says True when the two are the same.
                flip("the same number is not less", {"dex": 15}, "True", "False",
                     "Use `<`, which leaves the number itself out: a number is not less than itself.",
                     rel={"dex": ("needed", 0)}),
            ],
            pass_line="Bomb Shell: Hands too slow. Noted.",
        ),
        dict(
            id="barrier-up",
            text="Make `barrier_up` hold `True`, with no quotes, and print it.",
            dictated=True,
            hints=[
                "Start like this: keep `barrier_up = ` on line 4, and change only what comes after it.",
                "Line 4 still holds the starter's 0. `True` and `False` need no quotes: quotes would make them "
                "text. Then a new line prints the box.",
                "Python's yes is `True` and its no is `False`, each with a capital letter: `door_open = False`.",
            ],
            checks=[
                bool_box(
                    "barrier_up holds True or False", "barrier_up", known=DEX_KNOWN, foreign=DEX_FOREIGN, kept=True,
                    rules=[
                        ("type(_have).__name__ == 'str' and _have.strip().lower() == 'true'",
                         "`\"True\"` is text, because of the quotes. `True` with no quotes is Python's yes."),
                        ("type(_have).__name__ == 'int' and _have == 0",
                         "`barrier_up` still holds the starter's placeholder 0. Replace the 0 with `True`, with no quotes."),
                        ("type(_have).__name__ == 'int' and _have == 1",
                         "`barrier_up` holds the number 1. Python's yes is the word `True`, with a capital T and no quotes."),
                    ],
                ),
                ("barrier_up is True",
                 "assert barrier_up is True, '`barrier_up` holds False. Make it hold `True`: the barrier is up.'"),
                print_check("barrier_up"),
            ],
            pass_line="Gearshift: Barrier's holding.",
        ),
    ],
    solution=_dex(),
    partials=[_dex(barrier="barrier_up = 0")],
    assemble=dict(
        lines=["dex = 6", "needed = 15", "print(dex < needed)", "barrier_up = True", "print(barrier_up)"],
        distractors=["print(True)", 'barrier_up = "True"', "print(dex > needed)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A light switch",
            text=(
                "A yes/no answer is a light switch: on or off, nothing in between.\n"
                "```text\n6 < 15   ->  [ON ]  True\n6 > 15   ->  [OFF]  False\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A yes/no question",
            text=(
                "\"Are you taller than the door?\" has only two answers: yes or no. A comparison is that kind of "
                "question. Python says `True` for yes and `False` for no."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`print(dex < needed)`:\n"
                "1. Python looks inside the boxes: `6 < 15`.\n"
                "2. It works out the question: is 6 less than 15? Yes.\n"
                "3. It prints the answer: `True`."
            ),
        ),
        dict(angle="shorter", text="A comparison is a question. Python answers `True` or `False`."),
        dict(
            angle="why",
            label="Why does this work? No quotes",
            text=(
                "`True` has no quotes. It is not a word to show; it is Python's own yes. "
                "`\"True\"` with quotes is just four letters of text, like `\"glug\"`."
            ),
        ),
    ],
    bonus=dict(
        by="gearshift",
        title="Steady hands",
        text=(
            "Gearshift steadies Bomb Shell's hands: +10 DEX. On a new line, print whether `dex + 10` is more than "
            "`needed`."
        ),
        hints=[
            "Start like this: `print(dex + 10 `",
            "Python does the `+` first, then the `>`.",
        ],
        checks=[
            flip("the steady roll follows dex", {"dex": 4}, "True", "False",
                 "Print the question with the boxes: `dex + 10`, then `>`, then `needed`."),
            flip("the steady roll follows needed", {"needed": 20}, "True", "False",
                 "Use the box `needed`, not a number you typed."),
        ],
        solution=_dex() + "print(dex + 10 > needed)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] < spell["mana_cost"]',
        why=(
            "You have seen `<` in `cast_spell`. It asked: is the caster's mana less than the spell's cost? "
            "Python answered `True` or `False`, and the spell used that answer."
        ),
    ),
    takeaway="A comparison is a yes/no question: `print(dex < needed)` shows `True` or `False`, with no quotes.",
    wrong_answers=[
        dict(why="starter unchanged: still asks more than", code=DEX_STARTER, fails_at=1, message_contains="less than"),
        dict(why="the answer typed in (CP1 'True' check passes, the rerun does not)",
             code=_dex(line="print(True)"), fails_at=1, message_contains="16"),
        dict(why="the answer typed in as text", code=_dex(line='print("True")'), fails_at=1, message_contains="16"),
        dict(why="the numbers typed in instead of the boxes", code=_dex(line="print(6 < 15)"), fails_at=1,
             message_contains="dex = 16"),
        dict(why="half typed: the box needed replaced by 15", code=_dex(line="print(dex < 15)"), fails_at=1,
             message_contains="needed = 5"),
        dict(why="the question in quotes", code=_dex(line='print("dex < needed")'), fails_at=1,
             message_contains="exact letters"),
        dict(why="the boxes swapped, so it still asks more than", code=_dex(line="print(needed < dex)"), fails_at=1,
             message_contains="less than"),
        dict(why="the example's names copied", code=_dex(line="print(owls < wolves)"), fails_at=0,
             message_contains="not defined"),
        dict(why="<= for less than: the mirror boundary slip (True when the two are the same)",
             code=_dex(line="print(dex <= needed)"), fails_at=1, message_contains="leaves the number itself out"),
        dict(why="!= for less than: True here, but it never changes", code=_dex(line="print(dex != needed)"), fails_at=1,
             message_contains="dex = 16"),
        dict(why="a label and the answer typed in (the label hides nothing: it never changes)",
             code=_dex(line='print("dex < needed:", True)'), fails_at=1, message_contains="dex = 16"),
        dict(why="True in quotes (A-05/A-08 quoting slip)", code=_dex(barrier='barrier_up = "True"\nprint(barrier_up)'),
             fails_at=2, message_contains="is text"),
        dict(why="true with a small t", code=_dex(barrier="barrier_up = true\nprint(barrier_up)"), fails_at=0,
             message_contains="not defined"),
        dict(why="== used to fill the box (the = / == slip, reversed)",
             code=_dex(barrier="barrier_up = 0\nbarrier_up == True\nprint(barrier_up)"), fails_at=2,
             message_contains="use one `=`"),
        dict(why="the placeholder left, only a print added", code=_dex(barrier="barrier_up = 0\nprint(barrier_up)"),
             fails_at=2, message_contains="starter's placeholder 0"),
        dict(why="1 for yes", code=_dex(barrier="barrier_up = 1\nprint(barrier_up)"), fails_at=2,
             message_contains="number 1"),
        dict(why="True printed by hand, not the box", code=_dex(barrier="barrier_up = True\nprint(True)"), fails_at=2,
             message_contains="typed by hand"),
        dict(why="print(barrier_up) runs while the box still holds 0 (CP1's True line used to hide it)",
             code=_dex(barrier="barrier_up = 0\nprint(barrier_up)\nbarrier_up = True"), fails_at=2,
             message_contains="runs before"),
        dict(why="== used to fill the box after it already held False",
             code=_dex(barrier="barrier_up = False\nbarrier_up == True\nprint(barrier_up)"), fails_at=2,
             message_contains="use one `=`"),
        dict(why="the box name printed in quotes", code=_dex(barrier='barrier_up = True\nprint("barrier_up")'),
             fails_at=2, message_contains="word"),
        dict(why="a starter box renamed everywhere (Dex): the rerun has no dex to change",
             code="Dex = 6\nneeded = 15\nprint(Dex < needed)\nbarrier_up = True\nprint(barrier_up)\n", fails_at=1,
             message_contains="Keep the box `dex` from the starter"),
        dict(why="the starter's barrier_up line replaced by print(True)", code=_dex(barrier="print(True)"), fails_at=2,
             message_contains="Keep the box `barrier_up` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="compare", solo="false", dictates="1,2",
             foreign_names="owls,wolves,door_open") + "\n"
        "Predict = the spec's two lines (18 > 12, 6 > 15) with Bomb Shell's DEX and the latch. CP1 checks: 'True' is "
        "printed, then CMB with `dex = 16` (spec) and `needed = 5` (catches a half-typed `dex < 15`). The CMB is a "
        "flip: some printed line must change from True to False, so `print(True)`, `print(\"True\")` and "
        "`print(6 < 15)` all fail with the rerun message. Adding a new line instead of changing the old one passes "
        "(the behavior is right). CP2: `barrier_up is True` (spec) with the quotes message from the spec, the "
        "placeholder, `1` for yes, and `barrier_up == True` (a question that does not fill the box: the = / == "
        "slip, reversed). WT ('`True` has no quotes') is the 'why' angle. Partial 1 = CP1 done, placeholder left. "
        "BQ (combining arithmetic + comparison) is Gearshift's +10.\n"
        "Check-breaker pass: the flips read each line's last word (a labelled `print(\"Less?\", dex < needed)` "
        "passes) and take their numbers from the student's own boxes (`needed = 20` passes). A third flip at "
        "dex == needed catches the mirror boundary slip `<=`. print_check reads order from the code, so a "
        "`print(barrier_up)` above `barrier_up = True` no longer hides behind CP1's True line.\n"
        "Ruling pass (Unit 2 reviews): rerun messages lead with the fix and keep the evidence in brackets; CP2's "
        "rung 0 no longer types the answer (it names the part to change); the placeholder message says it is the "
        "starter's 0; a renamed `dex` or a dropped `barrier_up` line gets 'Keep the box ... from the starter'."
    ),
)

# 2A-02 ------------------------------------------------------------------------------------------

CLOCK_STARTER = 'clock_color = "blue"\nclock_is_red = (clock_color == "red")\nprint(clock_is_red)\nhero = "Bomb Shell"\n'
CLOCK_KNOWN = ["clock_color", "clock_is_red", "hero", "is_lucky"]
CLOCK_FOREIGN = ["door", "door_is_shut", "same", "a", "b"]


def _clock(color='"Red"', not_red='print(clock_color != "red")', lucky='is_lucky = (hero == "Lucky")'):
    return (
        f"clock_color = {color}\n"
        'clock_is_red = (clock_color == "red")\n'
        "print(clock_is_red)\n"
        f"{not_red}\n"
        'hero = "Bomb Shell"\n'
        f"{lucky}\n"
    )


ASK_WITH_DOUBLE_EQUALS = dict(
    id="ask-with-double-equals",
    title="Asking with ==",
    martu=(
        "`=` puts a value in a box: read it as *gets*. `==` asks a question: read it as [[is the same as]].\n"
        "So `clock_is_red = (clock_color == \"red\")` reads: `clock_is_red` gets the answer to *is `clock_color` "
        "the same as red?*\n"
        "Python works out the question in brackets first. Then the answer goes in the box."
    ),
    introduces=["op:Eq", "op:NotEq"],
    example='door = "open"\ndoor_is_shut = (door == "shut")\nprint(door_is_shut)\n',
    example_output="False",
    names=["clock_color", "clock_is_red", "hero", "is_lucky"],
    predict=dict(
        q="What will this print?",
        choices=["False", "True", "red", "blue"],
        answer=0,
        explain=(
            "`clock_color` holds blue. Blue is not the same as red, so the answer is `False`, and `clock_is_red` "
            "gets it. The brackets hold the question."
        ),
    ),
    starter=CLOCK_STARTER,
    checkpoints=[
        dict(
            id="try-red",
            text=(
                "Change `clock_color` to `\"red\"` and run. Then change it to `\"Red\"`, with a capital R, and run "
                "again."
            ),
            dictated=True,
            hints=[
                "Start like this: `clock_color = ` on line 1, then the new color in quotes.",
                "Line 1 holds the color. Change only the text inside its quotes.",
                "Python compares text letter for letter: `\"owl\" == \"Owl\"` is False.",
            ],
            checks=[
                (
                    "clock_color is Red",
                    f"assert 'clock_color' in globals(), {_gone_text('clock_color', True)!r}\n"
                    "_c = clock_color\n"
                    "_k = ''.join(_x for _x in str(_c).lower() if not _x.isspace())\n"
                    "_msg = ''\n"
                    "if _c == 'blue':\n"
                    "    _msg = 'Change line 1 to `clock_color = \"red\"` and run. Watch what `clock_is_red` says.'\n"
                    "elif _c == 'red':\n"
                    "    _msg = ('`clock_is_red` says True now: red is the same as red. Next, make it `\"Red\"`, with a '\n"
                    "            'capital R, and run again.')\n"
                    "elif _c != 'Red' and _k == 'red':\n"
                    "    _msg = 'Make it exactly `\"Red\"`: a capital R, then small letters, no spaces.'\n"
                    "elif _c != 'Red':\n"
                    "    _msg = 'Set `clock_color` to `\"Red\"`, with a capital R, and run.'\n"
                    "assert not _msg, _msg",
                ),
                (
                    "line 2 still asks about red",
                    # Still the question (not a typed `clock_is_red = False`), and its answer is False for "Red".
                    "import ast as _ast\n"
                    "_asks = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Assign' "
                    "and any(getattr(_t, 'id', '') == 'clock_is_red' for _t in _n.targets) "
                    "and any(type(_c).__name__ == 'Compare' and {getattr(_x, 'id', getattr(_x, 'value', None)) "
                    "for _x in [_c.left] + list(_c.comparators)} == {'clock_color', 'red'} for _c in _ast.walk(_n.value))]\n"
                    "assert _asks and clock_is_red is False, ('Keep line 2 as it was: `clock_is_red = (clock_color == \"red\")`, '\n"
                    "    'with a small r. Then see what Python says about `\"Red\"`.')",
                ),
            ],
            pass_line="Mar'tu: False. To Python, Red and red are different words. Every capital counts, yes?",
        ),
        dict(
            id="not-red",
            text="Add a line that prints whether `clock_color` is *not* `\"red\"`, using `!=`.",
            dictated=True,
            hints=[
                "Start like this: `print(clock_color `",
                "Look at line 2. Your new line asks the opposite question, with `!=`.",
                "`!=` means *is not the same as*. `\"owl\" != \"cat\"` is True.",
            ],
            checks=[
                no_quoted_question("no quotes around the question", ["clock_color"], ["!=", "=="]),
                no_is("not-red asks with !=, not is not", ["clock_color"]),
                ("uses !=", "assert _uses('op:NotEq'), 'Use `!=`. It asks: is it *not* the same as?'"),
                strexact("not-red compares with red exactly", "red", ops=("NotEq",)),
                flip("the answer follows clock_color", {"clock_color": "red"}, "True", "False",
                     "Print the question itself, `clock_color != \"red\"`, so Python works it out."),
            ],
            pass_line="Gearshift: Not red. Good. We wait.",
        ),
        dict(
            id="is-lucky",
            text="Make `is_lucky` hold whether `hero` is the same as `\"Lucky\"`.",
            dictated=False,
            hints=[
                "Start like this: `is_lucky = `",
                "This line has a *gets* and an *is the same as*. Which goes first?",
                "Ask a question, keep the answer: `same = (a == b)`. The `=` gets; the `==` asks.",
            ],
            checks=[
                bool_box(
                    "is_lucky holds True or False", "is_lucky", known=CLOCK_KNOWN, foreign=CLOCK_FOREIGN,
                    rules=[
                        ("_have == 'Lucky'",
                         "That puts the text in the box. Ask with `==`: is `hero` the same as `\"Lucky\"`?"),
                        ("type(_have).__name__ == 'str' and _have == _g.get('hero')",
                         "`is_lucky` holds a copy of what is in `hero`. Ask a question instead: is `hero` the same as "
                         "`\"Lucky\"`? That needs `==`."),
                    ],
                ),
                no_is("is_lucky asks with ==, not is", ["hero"]),
                quoted_name("hero is the box, not the word", ["hero"]),
                strexact("Lucky is spelled exactly", "Lucky"),
                rerun_bool("is_lucky follows hero (Lucky)", {"hero": "Lucky"}, "is_lucky", "True",
                           "Ask the question with the box `hero`, so the answer follows it."),
                rerun_bool("is_lucky follows hero (Oogrish)", {"hero": "Oogrish"}, "is_lucky", "False",
                           "Ask the question with the box `hero`, so the answer follows it."),
            ],
            pass_line="Lucky: True only when it's me. As it should be.",
        ),
    ],
    solution=_clock(),
    partials=[
        _clock(not_red="", lucky=""),
        _clock(lucky=""),
    ],
    assemble=dict(
        lines=[
            'clock_color = "Red"', 'clock_is_red = (clock_color == "red")', "print(clock_is_red)",
            'print(clock_color != "red")', 'hero = "Bomb Shell"', 'is_lucky = (hero == "Lucky")',
        ],
        distractors=['is_lucky = hero = "Lucky"', 'is_lucky = "Lucky"', 'print(clock_color != "Red")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Fill or ask",
            text=(
                "```text\nis_lucky = ...\n[ is_lucky ] <- answer\n\nhero == \"Lucky\"\n[ hero ] ? \"Lucky\"\n```\n"
                "The first line fills a box: one `=` points into it. The second only asks: two `==` put a question "
                "mark between two things."
            ),
        ),
        dict(
            angle="everyday",
            label="Name tag or question",
            text=(
                "Writing your name on a name tag is `=`: you put something there. Asking \"Are you Lucky?\" is `==`: "
                "you only want a yes or a no."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Right side first",
            text=(
                "`is_lucky = (hero == \"Lucky\")`:\n"
                "1. Python looks at the right side first: is `hero` the same as `\"Lucky\"`?\n"
                "2. `hero` holds Bomb Shell, so the answer is `False`.\n"
                "3. Then `is_lucky` gets that answer."
            ),
        ),
        dict(angle="shorter", text="`=` puts; `==` asks."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Mar'tu's spells glow violet. Lucky's glow silver. Make `martu_color` and `lucky_color` hold those colors. "
            "Then make `same_color` say whether they are the same, and print it."
        ),
        hints=[
            "Start like this: `same_color = `",
            "Two boxes, one `==` between them, and the answer goes in `same_color`.",
        ],
        checks=[
            bool_box("same_color holds True or False", "same_color", known=CLOCK_KNOWN + ["martu_color", "lucky_color"]),
            rerun_bool("same_color follows the colors", {"lucky_color": "violet"}, "same_color",
                       "_R('martu_color') == _R('lucky_color')", "Compare the two boxes, not two words you typed."),
            rerun_bool("same_color follows martu_color", {"martu_color": "silver", "lucky_color": "silver"}, "same_color",
                       "True", "Compare the two boxes, `martu_color` and `lucky_color`, not a color you typed."),
            print_check("same_color"),
        ],
        solution=_clock() + 'martu_color = "violet"\nlucky_color = "silver"\nsame_color = (martu_color == lucky_color)\n'
        "print(same_color)\n",
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='if (user.clicked() == "option 1"):',
        why=(
            "You have seen `==` in the dialogue part. `user.clicked() == \"option 1\"` asked: is the box they clicked "
            "the same as option 1? The answer was `True` or `False`. Next lesson, `if` uses that answer."
        ),
    ),
    takeaway="`=` gets a value; `==` asks *is the same as*; `!=` asks *is not the same as*. Text must match exactly.",
    wrong_answers=[
        dict(why="starter unchanged", code=CLOCK_STARTER, fails_at=1, message_contains='clock_color = "red"'),
        dict(why="investigate stopped at red", code=_clock(color='"red"'), fails_at=1, message_contains="capital R"),
        dict(why="Red with a space", code=_clock(color='"Red "'), fails_at=1, message_contains="exactly"),
        dict(why="line 2 changed to match the capital", code=_clock().replace('(clock_color == "red")', '(clock_color == "Red")'),
             fails_at=1, message_contains="small r"),
        dict(why="line 2's question replaced by a typed False (passes the value test, skips the question)",
             code=_clock().replace('(clock_color == "red")', "False"), fails_at=1, message_contains="Keep line 2"),
        dict(why="`is not` for != (reads like English)", code=_clock(not_red='print(clock_color is not "red")'), fails_at=2,
             message_contains="different question"),
        dict(why="one = inside the print: Python reads it as a print setting (TypeError)",
             code=_clock(not_red='print(clock_color = "red")'), fails_at=0, message_contains="unexpected keyword argument"),
        dict(why="== instead of != in the new line", code=_clock(not_red='print(clock_color == "red")'), fails_at=2,
             message_contains="!="),
        dict(why="STREXACT: != \"Red\" (spec)", code=_clock(not_red='print(clock_color != "Red")'), fails_at=2,
             message_contains="every letter, space and capital"),
        dict(why="the question in quotes", code=_clock(not_red='print("clock_color != red")'), fails_at=2,
             message_contains="exact letters"),
        dict(why="the answer typed after a != elsewhere", code=_clock(not_red="print(True != False)"), fails_at=2,
             message_contains="no line changed from `True` to `False`"),
        dict(why="=! instead of !=", code=_clock(not_red='print(clock_color =! "red")'), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="text put in the box instead of asking (spec)", code=_clock(lucky='is_lucky = "Lucky"'), fails_at=3,
             message_contains="Ask with `==`"),
        dict(why="two = signs: puts Lucky in both boxes (spec: not a bool)", code=_clock(lucky='is_lucky = hero = "Lucky"'),
             fails_at=3, message_contains="two `=` signs"),
        dict(why="one = inside the brackets", code=_clock(lucky='is_lucky = (hero = "Lucky")'), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="STREXACT: lucky with a small l", code=_clock(lucky='is_lucky = (hero == "lucky")'), fails_at=3,
             message_contains="every letter"),
        dict(why="the box name in quotes", code=_clock(lucky='is_lucky = ("hero" == "Lucky")'), fails_at=3,
             message_contains="not the box"),
        dict(why="the answer typed in", code=_clock(lucky="is_lucky = False"), fails_at=3, message_contains='"Lucky"'),
        dict(why="the answer typed in after changing hero", code=_clock(lucky="is_lucky = True").replace(
            'hero = "Bomb Shell"', 'hero = "Lucky"'), fails_at=3, message_contains="Oogrish"),
        dict(why="the example's box name copied", code=_clock(lucky='door_is_shut = (hero == "Lucky")'), fails_at=3,
             message_contains="example"),
        dict(why="the hint's box name copied", code=_clock(lucky='same = (hero == "Lucky")'), fails_at=3,
             message_contains="example or a hint"),
        dict(why="a capital I", code=_clock(lucky='Is_lucky = (hero == "Lucky")'), fails_at=3,
             message_contains="letter for letter"),
        dict(why="the question kept nowhere", code=_clock(lucky='hero == "Lucky"'), fails_at=3,
             message_contains="keeps the answer nowhere"),
        dict(why="`is` for == (reads like English, and even comes out right for these two literals)",
             code=_clock(lucky='is_lucky = hero is "Lucky"'), fails_at=3, message_contains="different question"),
        dict(why="the box copied, no question", code=_clock(lucky="is_lucky = hero"), fails_at=3,
             message_contains="copy of what is in"),
        dict(why="hard-coded hero: != the starter's hero", code=_clock(lucky='is_lucky = hero != "Bomb Shell"'),
             fails_at=3, message_contains="Oogrish"),
        dict(why="Lucky without quotes", code=_clock(lucky="is_lucky = (hero == Lucky)"), fails_at=0,
             message_contains="not defined"),
        dict(why="the starter box hero renamed (name): the rerun has no hero to change",
             code=_clock(lucky='is_lucky = (name == "Lucky")').replace('hero = "Bomb Shell"', 'name = "Bomb Shell"'),
             fails_at=3, message_contains="Keep the box `hero` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="compare,gets-vs-same", solo="false", dictates="1,2",
             foreign_names="door,door_is_shut,same,a,b") + "\n"
        "The first exposure keeps the parentheses (G1 R11). Predict = the starter (False). The Investigate (red -> "
        "True, then Red -> False, with the STREXACT note) is checkpoint 1 so everyone does it: its message walks "
        "them through both runs, and the final state is \"Red\" (a lasting demo that capitals count). Spec CP1 "
        "(`!=`) and CP2 (`is_lucky`) are checkpoints 2 and 3 here, so the spec's WA 'is_lucky = \"Lucky\" -> CP2' "
        "is fails_at=3. CP2's CMB reruns with `clock_color = \"red\"` (spec). CP3 [ND]: a bool, then CMB with "
        "hero = Lucky (True, spec) and hero = Oogrish (False, catches a typed True). Catches from the spec: text in "
        "the box ('Ask with `==`'), the chained `is_lucky = hero = \"Lucky\"` ('two `=` signs': it is not a bool), "
        "`!= \"Red\"` (STREXACT). Also the hint's own `same` (LEFT), a quoted name, a question kept in no box. "
        "PA distractor `is_lucky = hero = \"Lucky\"` (spec). BQ (two boxes + `==`): same_color.\n"
        "Check-breaker pass: CP1 also needs line 2 to still be the question (a typed `clock_is_red = False` "
        "passed). `is` / `is not` caught (`hero is \"Lucky\"` came out right and passed). `is_lucky = hero` gets "
        "its own message. A labelled not-red print passes. `hero.lower() == \"lucky\"` is not STREXACT. Pass line "
        "works for True and False. `print(clock_color = \"red\")` is a TypeError (Python 3.13: \"unexpected keyword "
        "argument 'clock_color'\"); the site explainer gives it its own kind (one `=` inside print). Bonus: a second "
        "rerun moves martu_color, so a half-typed `\"violet\" == lucky_color` fails.\n"
        "Ruling pass (Unit 2 reviews): rung 0 stops before the sign (`print(clock_color `; bonus `same_color = `), "
        "`is` messages no longer say 'object', rerun messages lead with the fix, and a renamed `hero` gets 'Keep "
        "the box `hero` from the starter'."
    ),
)

# 2A-03 ------------------------------------------------------------------------------------------

PASS_STARTER = (
    "roll = 15\n"
    "needed = 15\n"
    "# passed: does roll reach needed?\n"
    "mana = 6\n"
    "cost = 6\n"
    "# can_cast: does mana cover cost?\n"
)
PASS_KNOWN = ["roll", "needed", "passed", "mana", "cost", "can_cast"]
PASS_FOREIGN = ["coins", "price", "can_buy"]


def _pass(passed="passed = roll >= needed", can_cast="can_cast = mana >= cost", roll="roll = 15", cost="cost = 6"):
    return (
        f"{roll}\n"
        "needed = 15\n"
        "# passed: does roll reach needed?\n"
        f"{passed}\n"
        "mana = 6\n"
        f"{cost}\n"
        "# can_cast: does mana cover cost?\n"
        f"{can_cast}\n"
    )


NUM_IS = (
    "`is` asks a different question in Python, and it can say False even when two numbers match. Compare "
    "numbers with a comparison sign instead."
)

ROLL_FIX = dict(
    short_fix="Ask: is `roll` at least `needed`? *At least* is `>=`.",
    exact_fix="Use `>=`, which means *at least*: the number itself counts.",
    over_fix="Ask: is `roll` at least `needed`? *At least* is `>=`.",
    shift_fix="Use both boxes, `roll` and `needed`, not a number you typed.",
)
MANA_FIX = dict(
    short_fix="Ask: is `mana` at least `cost`? *At least* is `>=`.",
    exact_fix="Use `>=`, which means *at least*: exactly enough mana still casts.",
    over_fix="Ask: is `mana` at least `cost`? *At least* is `>=`.",
    shift_fix="Use both boxes, `mana` and `cost`, not a number you typed.",
    lt_note=" `mana < cost` asks *not enough?*",
)
# The SOLO's messages say what went wrong but never name the sign: a solo pass stays the student's own.
SOLO_FIX = dict(
    short_fix="Ask whether `mana` is at least `cost`.",
    exact_fix="Which sign counts the number itself?",
    over_fix="Ask whether `mana` is at least `cost`.",
    shift_fix="Use both boxes, `mana` and `cost`, not a number you typed.",
    lt_note=" `mana < cost` asks *not enough?*",
    rev_fix="Your sign faces the wrong way: it asks *at most*.",
)

ENOUGH_TO_PASS = dict(
    id="enough-to-pass",
    title="Enough to pass",
    martu=(
        "`>=` means [[at least]]. A roll of exactly the number needed still passes. "
        "`<=` means *at most*.\n"
        "`>` is stricter: it leaves the number itself out. So `15 > 15` is False, but `15 >= 15` is True.\n"
        "From here on, no brackets: `can_buy = coins >= price` works the same. Python asks the question first, "
        "then fills the box."
    ),
    introduces=["op:GtE", "op:LtE"],
    example="coins = 10\nprice = 10\ncan_buy = coins >= price\nprint(can_buy)\nprint(coins <= price)\n",
    example_output="True\nTrue",
    names=["roll", "needed", "passed", "mana", "cost", "can_cast"],
    predict=dict(
        q="The latch needs 15. Which rolls pass? What will this print?",
        code="needed = 15\nprint(14 >= needed)\nprint(15 >= needed)\nprint(16 >= needed)\n",
        choices=["False\nTrue\nTrue", "False\nFalse\nTrue", "True\nTrue\nTrue", "False\nTrue\nFalse"],
        answer=0,
        explain=(
            "14 is one short: `False`. 15 is exactly enough: `True`, because `>=` counts the number itself. "
            "16 is more than enough: `True`. With `>`, the 15 would fail."
        ),
    ),
    pair_talk=(
        "Pair talk: explain to your partner why a 15 should open a latch that needs 15. Which sign says that? "
        "Then each of you writes your own lines."
    ),
    starter=PASS_STARTER,
    checkpoints=[
        dict(
            id="passed",
            text="Make `passed` say whether `roll` reaches `needed`. Exactly enough counts.",
            dictated=False,
            hints=[
                "Start like this: `passed = roll `",
                "Should a 15 pass when 15 is needed? Pick the sign that says yes.",
                "`>` leaves out the boundary; `>=` includes it. `9 > 9` is False, but `9 >= 9` is True.",
            ],
            checks=[
                bool_box("passed holds True or False", "passed", known=PASS_KNOWN, foreign=PASS_FOREIGN),
                no_is("passed compares with a sign, not is", ["roll", "needed"], msg=NUM_IS + " *At least* is `>=`."),
                bnd("passed: one short fails, exactly enough passes", "passed", "roll", "needed", "pass", **ROLL_FIX),
            ],
            pass_line="Mar'tu: Which sign makes exactly enough pass? Point at it. Yes: the `=` in `>=`.",
        ),
        dict(
            id="can-cast",
            text="Make `can_cast` say whether `mana` covers `cost`. Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Start like this: `can_cast = mana `",
                "Mana 6, cost 6: should the spell cast? Then the sign must include the boundary.",
                "*At least* is `>=`: `coins >= price` is True when the coins are exactly enough.",
            ],
            checks=[
                bool_box("can_cast holds True or False", "can_cast", known=PASS_KNOWN, foreign=PASS_FOREIGN),
                no_is("can_cast compares with a sign, not is", ["mana", "cost"], msg=NUM_IS + " *At least* is `>=`."),
                bnd("can_cast: exactly enough mana casts", "can_cast", "mana", "cost", "cast", **MANA_FIX),
            ],
            pass_line="Oogrish: Exactly enough is enough. Steady, now.",
        ),
    ],
    solution=_pass(),
    partials=[_pass(can_cast="")],
    assemble=dict(
        lines=["roll = 15", "needed = 15", "passed = roll >= needed", "mana = 6", "cost = 6", "can_cast = mana >= cost"],
        distractors=["passed = roll > needed", "can_cast = mana < cost", "passed = True"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A number line",
            text=(
                "The filled dot is the number needed. `>=` starts on the dot. `>` starts just after it.\n"
                "```text\n          13   14   15   16   17\n"
                "roll >= 15            ●=========>\n"
                "roll > 15             o====>\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            label="Try 14, 15, 16",
            text=(
                "```text\nroll | roll > 15 | roll >= 15\n"
                " 14  |  False    |  False\n"
                " 15  |  False    |  True\n"
                " 16  |  True     |  True\n```\n"
                "Only the 15 row is different. That row is the boundary."
            ),
        ),
        dict(
            angle="in Tor",
            text="A 15 opens a latch that needs 15. Bomb Shell does not need 16. Exactly enough is enough.",
        ),
        dict(angle="shorter", text="Exactly enough counts? Use `>=`."),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In `cast_spell` the steps said: use `<` and not `<=`, because a caster with exactly enough mana can "
                "still cast. `mana < cost` asked *not enough?* Here you ask the other side, *enough?*: `mana >= cost`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky likes a close call. Make `close_call` True only when the roll is exactly `needed`. "
            "Then print both `passed` and `close_call`."
        ),
        hints=[
            "Start like this: `close_call = `",
            "Exactly the same number? That is `==`. Then two `print` lines.",
        ],
        checks=[
            bool_box("close_call holds True or False", "close_call", known=PASS_KNOWN + ["close_call"]),
            rerun_bool("close_call at one over", {"roll": 16}, "close_call", "False",
                       "`close_call` is True only for exactly `needed`: use `==`."),
            rerun_bool("close_call at one short", {"roll": 14}, "close_call", "False",
                       "One short is a miss, not a close call. `close_call` is True only for exactly `needed`: use `==`."),
            rerun_bool("close_call at a new needed", {"roll": 12, "needed": 12}, "close_call", "True",
                       "Compare the two boxes, `roll` and `needed`, with `==`."),
            print_check("passed"),
            print_check("close_call"),
        ],
        solution=_pass() + "close_call = roll == needed\nprint(passed)\nprint(close_call)\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="return roll >= required_roll",
        why=(
            "You have seen this line at the trap door. `roll >= required_roll` asked: is the roll at least the "
            "number needed? It handed back `True` or `False`. A roll of exactly 15 opened a latch that needed 15."
        ),
    ),
    takeaway="`>=` means *at least*: exactly enough still passes. `>` leaves the number itself out.",
    wrong_answers=[
        dict(why="starter unchanged: no passed box yet", code=PASS_STARTER, fails_at=1, message_contains="Make a box named `passed`"),
        dict(why="> instead of >= (spec)", code=_pass(passed="passed = roll > needed"), fails_at=1,
             message_contains="exactly"),
        dict(why="the answer typed in", code=_pass(passed="passed = True"), fails_at=1, message_contains="one short"),
        dict(why="a number typed in for needed", code=_pass(passed="passed = roll >= 15"), fails_at=1,
             message_contains="needed = 18"),
        dict(why="the boxes the wrong way round", code=_pass(passed="passed = needed >= roll"), fails_at=1,
             message_contains="faces the wrong way"),
        dict(why="<= for >=: the sign mirrored (asks at most)", code=_pass(passed="passed = roll <= needed"), fails_at=1,
             message_contains="faces the wrong way"),
        dict(why="`is` for a comparison sign", code=_pass(passed="passed = roll is needed"), fails_at=1,
             message_contains="different question"),
        dict(why="== used to fill the box after a placeholder False (the = / == slip)",
             code=_pass(passed="passed = False\npassed == roll >= needed"), fails_at=1, message_contains="use one `=`"),
        dict(why="two = signs: passed = roll = needed", code=_pass(passed="passed = roll = needed"), fails_at=1,
             message_contains="two `=` signs"),
        dict(why="== instead of >=", code=_pass(passed="passed = roll == needed"), fails_at=1,
             message_contains="more than enough"),
        dict(why="=> instead of >=", code=_pass(passed="passed = roll => needed"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="the starter comment's : copied instead of =", code=_pass(passed="passed: roll >= needed"),
             fails_at=1, message_contains="uses `:`"),
        dict(why="the question kept nowhere", code=_pass(passed="roll >= needed"), fails_at=1,
             message_contains="keeps the answer nowhere"),
        dict(why="the question in quotes", code=_pass(passed='passed = "roll >= needed"'), fails_at=1,
             message_contains="holds text"),
        dict(why="a capital P", code=_pass(passed="Passed = roll >= needed"), fails_at=1, message_contains="letter for letter"),
        dict(why="> kept, roll changed to 16 to make it pass", code=_pass(passed="passed = roll > needed", roll="roll = 16"),
             fails_at=1, message_contains="exactly"),
        dict(why="the answer typed in (spec)", code=_pass(can_cast="can_cast = True"), fails_at=2, message_contains="one short"),
        dict(why="> instead of >= for mana", code=_pass(can_cast="can_cast = mana > cost"), fails_at=2,
             message_contains="exactly enough mana"),
        dict(why="the campaign's < copied: asks not enough", code=_pass(can_cast="can_cast = mana < cost"), fails_at=2,
             message_contains="not enough?"),
        dict(why="<= for >= on mana: the sign mirrored", code=_pass(can_cast="can_cast = mana <= cost"), fails_at=2,
             message_contains="faces the wrong way"),
        dict(why="passed reused for can_cast (the wrong boxes)", code=_pass(can_cast="can_cast = passed"), fails_at=2,
             message_contains="one short"),
        dict(why="a number typed in for cost", code=_pass(can_cast="can_cast = mana >= 6"), fails_at=2,
             message_contains="cost = 9"),
        dict(why="the example's box name copied", code=_pass(can_cast="can_buy = mana >= cost"), fails_at=2,
             message_contains="example"),
        dict(why="> kept, cost lowered to make it pass", code=_pass(can_cast="can_cast = mana > cost", cost="cost = 5"),
             fails_at=2, message_contains="exactly enough mana"),
        dict(why="the starter box needed renamed (need)",
             code=_pass(passed="passed = roll >= need").replace("needed = 15", "need = 15"), fails_at=1,
             message_contains="Keep the box `needed` from the starter"),
        dict(why="roll set in a chained line the rerun cannot change", code=_pass(roll="roll = needed = 15"), fails_at=1,
             message_contains="Keep the line that sets `roll`"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="compare,boundary", solo="false", dictates="",
             foreign_names="coins,price,can_buy") + "\n"
        "No brackets from here on (G1 R11). Predict = rolls 14, 15, 16 against 15 (spec). Both checkpoints are "
        "[ND] and BND: reruns at needed - 1, needed, needed + 1 with `needed` read from the student's own code (a "
        "student who changes the numbers still passes), then `needed` moved up by 3 so a typed `roll >= 15` fails. "
        "Messages name the case: one short, exactly enough, more than enough. The campaign's own `mana < cost` "
        "(the *not enough* test in cast_spell) gets its own line in the can_cast message. A student who keeps `>` and "
        "changes the numbers until it passes is caught by the exactly-enough rerun. Point-at-it ('Which sign makes "
        "exactly enough pass?') is CP1's pass line. TR (static table) is the 'Try 14, 15, 16' angle. "
        "BQ (combining `==` + `>=`): close_call, printed with passed.\n"
        "Check-breaker pass: a mirrored sign (`roll <= needed`, `needed >= roll`) gets a 'faces the wrong way' "
        "note; `is` is caught; `passed == roll >= needed` under a placeholder `passed = False` gets the = / == "
        "message (bool_box now flags a `box == ...` line even when the box holds a bool). Bonus: a roll = 14 "
        "rerun catches `close_call = roll <= needed` and `roll < 16`.\n"
        "Ruling pass (Unit 2 reviews): BND messages lead with the fix, then '(Mar'tu's check tried `roll = 14` and "
        "`needed = 15`, only inside the check: `passed` was True, so one short passed.)'; a mirrored sign's "
        "'faces the wrong way' line replaces the one-short fix, so the message stays under 35 words. A renamed "
        "`needed` gets 'Keep the box', a chained `roll = needed = 15` gets 'Keep the line'. Bonus rung 0 is "
        "`close_call = `."
    ),
)

# 2A-04 ------------------------------------------------------------------------------------------

ANSWER_STARTER = 'answer = "YES"\nsaid_yes = answer == "yes"\nprint(said_yes)\n'
ANSWER_KNOWN = ["answer", "said_yes"]
ANSWER_FOREIGN = ["shout", "first", "second", "same"]


def _answer(line='said_yes = answer.lower() == "yes"', answer='answer = "YES"'):
    return f"{answer}\n{line}\nprint(said_yes)\n"


LOWER_CHECKS = [
    (
        "lower has its brackets",
        "import ast as _ast\n"
        "_tree = _ast.parse(_source)\n"
        "_called = [id(_n.func) for _n in _ast.walk(_tree) if type(_n).__name__ == 'Call']\n"
        "_raw = [_n.lineno for _n in _ast.walk(_tree) if type(_n).__name__ == 'Attribute' and _n.attr == 'lower' "
        "and id(_n) not in _called]\n"
        "assert not _raw, 'Line ' + str(_raw[0] if _raw else 0) + ': `.lower` without `()` doesn' + chr(39) + "
        "'t run. Add `()`: `answer.lower()`.'",
    ),
    (
        "the copy is used, not forgotten",
        "import ast as _ast\n"
        "_lone = [_n.lineno for _n in _ast.parse(_source).body if type(_n).__name__ == 'Expr' "
        "and type(_n.value).__name__ == 'Call' and type(_n.value.func).__name__ == 'Attribute' "
        "and _n.value.func.attr == 'lower']\n"
        "assert not _lone, 'Line ' + str(_lone[0] if _lone else 0) + ' makes a lower-case copy, then forgets it. "
        "`answer` itself does not change. Use the copy right inside the question.'",
    ),
    (
        "lower is asked of answer",
        "import ast as _ast\n"
        "_calls = [_n.func.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Call' "
        "and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'lower']\n"
        "_on_text = [_v for _v in _calls if type(_v).__name__ == 'Constant']\n"
        "_on_box = [_v for _v in _calls if type(_v).__name__ != 'Constant']\n"
        "assert not (_on_text and not _on_box and any(_v.value == 'answer' for _v in _on_text)), "
        "'`\"answer\"` in quotes is just that word, not the box. Take the quotes off: `answer.lower()`.'\n"
        "assert not (_on_text and not _on_box), '`.lower()` is on the wrong text: `\"yes\"` is small already. "
        "Ask `answer` for the copy: `answer.lower()`.'",
    ),
]

ANY_CASE_ANSWER = dict(
    id="any-case-answer",
    title="Any case, same answer",
    martu=(
        "`\"YES\" == \"yes\"` is False: every letter, space and capital counts.\n"
        "The dot means: ask this text to do something. `answer.lower()` gives a [[.lower()|lower-case copy]] of "
        "`answer`. The `()` at the end makes it run.\n"
        "The copy is new. The text in `answer` does not change."
    ),
    introduces=["attr:lower"],
    example='shout = "HELLO"\nprint(shout.lower())\nprint(shout)\n',
    example_output="hello\nHELLO",
    names=["answer", "said_yes", "lower"],
    predict=dict(
        q="A traveler shouts YES. What will this print?",
        choices=["False", "True", "yes", "YES"],
        answer=0,
        explain=(
            "`\"YES\"` and `\"yes\"` are different text to Python, so the answer is `False`. But the traveler meant "
            "yes. Let's fix that."
        ),
    ),
    starter=ANSWER_STARTER,
    checkpoints=[
        dict(
            id="any-capitals",
            text="Make `said_yes` True for any capitals: use `answer.lower()`.",
            dictated=True,
            hints=[
                "Start like this: `said_yes = answer.lower() `",
                "Which part changes the capitals? Put it on the left of the `==`.",
                "`\"HI\".lower()` gives `\"hi\"`. Then `\"hi\" == \"hi\"` is True.",
            ],
            checks=LOWER_CHECKS + [
                bool_box(
                    "said_yes holds True or False", "said_yes", known=ANSWER_KNOWN, foreign=ANSWER_FOREIGN, kept=True,
                    text_msg=(
                        "`said_yes` holds the lower-case copy itself. Ask with `==` whether that copy is the same as "
                        "`\"yes\"`."
                    ),
                ),
                (
                    "compare with small letters",
                    "import ast as _ast\n"
                    "_big = [_c.value for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare' "
                    "for _c in [_n.left] + list(_n.comparators) if type(_c).__name__ == 'Constant' "
                    "and type(_c.value).__name__ == 'str' and _c.value != _c.value.lower()]\n"
                    "assert not _big or not _uses('attr:upper'), '`.upper()` works the other way round, and that "
                    "would work too. This step practices `.lower()`, though: `answer.lower() == \"yes\"`.'\n"
                    "assert not _big, '`answer.lower()` gives small letters, so compare it with small letters: "
                    "`\"yes\"`. Every capital counts.'",
                ),
                strexact("yes is spelled exactly", "yes"),
                no_is("said_yes asks with ==, not is", ["answer"]),
                rerun_bool("YES counts", {"answer": "YES"}, "said_yes", "True",
                           "Use `answer.lower()` in the question, so every way of writing yes counts."),
                rerun_bool("yes counts", {"answer": "yes"}, "said_yes", "True",
                           "Use `answer.lower()` in the question, so every way of writing yes counts."),
                rerun_bool("YeS counts", {"answer": "YeS"}, "said_yes", "True",
                           "Use `answer.lower()` in the question, so every way of writing yes counts."),
                rerun_bool("no is not yes", {"answer": "no"}, "said_yes", "False",
                           "Ask the question with `answer.lower()`, so the answer follows what the traveler typed."),
                # `answer != "no"` says yes to YES, yes, YeS and no to no, so a shouted NO must still be a no.
                rerun_bool("NO is not yes", {"answer": "NO"}, "said_yes", "False",
                           "Ask whether the copy is the same as `\"yes\"`: `answer.lower() == \"yes\"`."),
                (
                    "uses lower",
                    "assert _uses('attr:lower'), ('This step practices `.lower()`: `answer.lower() == \"yes\"`. '\n"
                    "    \"Then every way of writing yes counts, even ones Mar'tu's check did not try.\")",
                ),
            ],
            pass_line="Mar'tu: YES, yes, YeS. All the same now. Python only needed to be asked properly, yes?",
        ),
    ],
    solution=_answer(),
    assemble=dict(
        lines=['answer = "YES"', 'said_yes = answer.lower() == "yes"', "print(said_yes)"],
        distractors=['said_yes = answer.lower == "yes"', 'said_yes = answer.lower() == "YES"', "said_yes = True"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A copy in small letters",
            text=(
                "```text\nanswer         -> \"YeS\"\n"
                "answer.lower() -> \"yes\"\n"
                "\"yes\" == \"yes\" -> True\n```\n"
                "`answer` stays the same. `answer.lower()` is a new copy in small letters."
            ),
        ),
        dict(
            angle="everyday",
            label="A kind librarian",
            text=(
                "A librarian who ignores capitals finds your book whether you write HARRY or harry. `.lower()` makes "
                "Python that kind of librarian: it compares small letters with small letters."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`said_yes = answer.lower() == \"yes\"`:\n"
                "1. `answer.lower()` makes a copy in small letters: `\"yes\"`.\n"
                "2. Python asks: is `\"yes\"` the same as `\"yes\"`? `True`.\n"
                "3. `said_yes` gets `True`."
            ),
        ),
        dict(angle="shorter", text="Small letters on both sides: `answer.lower() == \"yes\"`."),
        dict(
            angle="campaign",
            label="You've seen this",
            text=(
                "In Module 1, Mar'tu's dialogue line went through `.lower()` and then `.capitalize()` before it was "
                "shown. That tidied any capitals the player typed. Same dot, same idea."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky asks for glug two ways. Make `first = \"Glug\"` and `second = \"GLUG\"`. Then make `same` say "
            "whether they match, whatever their capitals, and print it."
        ),
        hints=[
            "Start like this: `same = `",
            "Both sides need `.lower()`, so both are small letters.",
        ],
        checks=[
            bool_box("same holds True or False", "same", known=ANSWER_KNOWN + ["first", "second", "same"]),
            rerun_bool("same: different words", {"second": "glum"}, "same", "False",
                       "Compare the two boxes, each with `.lower()`."),
            rerun_bool("same: both sides lowered", {"first": "GLUG", "second": "glug"}, "same", "True",
                       "Put `.lower()` on both boxes, so capitals never matter."),
            rerun_bool("same: first is used too", {"first": "glum"}, "same", "False",
                       "Compare the two boxes, `first` and `second`, each with `.lower()`."),
            print_check("same"),
        ],
        solution=_answer() + 'first = "Glug"\nsecond = "GLUG"\nsame = first.lower() == second.lower()\nprint(same)\n',
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet="dialogue_input = dialogue_input.lower()",
        why=(
            "You have seen this in Mar'tu's dialogue line. `.lower()` made a lower-case copy, and "
            "`dialogue_input = ` put that copy back in the box. The dot asked the text to do something."
        ),
    ),
    takeaway="Text must match exactly. `answer.lower() == \"yes\"` ignores capitals: the dot asks the text for a copy.",
    wrong_answers=[
        dict(why="starter unchanged: the bracket says the tried value is the code's own, not a change",
             code=ANSWER_STARTER, fails_at=1, message_contains='(With `answer = "YES"`, as in your code now'),
        dict(why=".lower without () (spec)", code=_answer(line='said_yes = answer.lower == "yes"'), fails_at=1,
             message_contains="`()`"),
        dict(why="the answer typed in (spec)", code=_answer(line="said_yes = True"), fails_at=1,
             message_contains='`answer = "no"`'),
        dict(why="STREXACT: compares the copy with capitals (spec)", code=_answer(line='said_yes = answer.lower() == "YES"'),
             fails_at=1, message_contains="small letters"),
        dict(why="the copy put in the box, no question", code=_answer(line="said_yes = answer.lower()"), fails_at=1,
             message_contains="lower-case copy itself"),
        dict(why="a lower-case copy made and forgotten (strings do not change)",
             code='answer = "YES"\nanswer.lower()\nsaid_yes = answer == "yes"\nprint(said_yes)\n', fails_at=1,
             message_contains="forgets it"),
        dict(why=".lower() on the wrong side", code=_answer(line='said_yes = answer == "yes".lower()'), fails_at=1,
             message_contains="wrong text"),
        dict(why="lower used like print", code=_answer(line='said_yes = lower(answer) == "yes"'), fails_at=0,
             message_contains="not defined"),
        dict(why="= instead of ==", code=_answer(line='said_yes = answer.lower() = "yes"'), fails_at=0,
             message_contains="cannot assign"),
        dict(why="a capital L", code=_answer(line='said_yes = answer.Lower() == "yes"'), fails_at=0,
             message_contains="no attribute"),
        dict(why="the traveler's answer changed instead of the question",
             code=_answer(line='said_yes = answer == "yes"', answer='answer = "yes"'), fails_at=1,
             message_contains='`answer = "YES"`'),
        dict(why="yes with a space", code=_answer(line='said_yes = answer.lower() == "yes "'), fails_at=1,
             message_contains="every letter, space and capital"),
        dict(why="skips .lower(): anything that is not no counts as yes", code=_answer(line='said_yes = answer != "no"'),
             fails_at=1, message_contains='`answer = "NO"`'),
        dict(why="skips .lower(): yes-length text (passes every rerun)", code=_answer(line="said_yes = len(answer) == 3"),
             fails_at=1, message_contains="practices `.lower()`"),
        dict(why="every capital spelled out by hand instead of .lower()",
             code=_answer(line='said_yes = answer == "yes" or answer == "YES" or answer == "YeS"'), fails_at=1,
             message_contains="small letters"),
        dict(why=".upper() and YES (works, but not this step's skill)", code=_answer(line='said_yes = answer.upper() == "YES"'),
             fails_at=1, message_contains="practices `.lower()`"),
        dict(why="`is` for ==", code=_answer(line='said_yes = answer.lower() is "yes"'), fails_at=1,
             message_contains="different question"),
        dict(why="the box's name in quotes", code=_answer(line='said_yes = "answer".lower() == "yes"'), fails_at=1,
             message_contains="just that word"),
        dict(why="the starter box said_yes renamed (said)", code='answer = "YES"\nsaid = answer.lower() == "yes"\nprint(said)\n',
             fails_at=1, message_contains="Keep the box `said_yes` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="compare,chain-methods-prereq", solo="false", dictates="1",
             foreign_names="shout") + "\n"
        "Introduces attr:lower in the VISIBLE starter and solution (setup gotcha, 2.12 rule 3). Learn says the dot "
        "line (G1 unnumbered). Predict = the starter (False). CP1 CMB: four reruns (spec): YES, yes, YeS -> True; "
        "no -> False. Catches from the spec: `.lower` with no `()` (its own message, before any rerun) and "
        "`== \"YES\"` (STREXACT, phrased as 'compare with small letters'). Also: the copy kept in the box with no "
        "question, a copy made on its own line and forgotten (text never changes in place), `.lower()` on the "
        "wrong side, `lower(answer)`, `.Lower()`, and changing the traveler's answer instead of the question. "
        "`answer = answer.lower()` on its own line, then the old question, is valid and passes (the campaign does "
        "exactly that). Single checkpoint: no partials. BQ (two method calls + `==`): same.\n"
        "Check-breaker pass: `said_yes = answer != \"no\"` passed every rerun without `.lower()`: a fifth rerun "
        "(`\"NO\"` -> False) and a last 'uses lower' check close it. `.upper()` gets a kind redirect (the step "
        "names `.lower()`), `is` is caught, `\"answer\".lower()` gets the quotes rule. Bonus: a rerun with "
        "first = glum catches a half-typed `second.lower() == \"glug\"`.\n"
        "Ruling pass (Unit 2 reviews): the starter's own `answer = \"YES\"` rerun says '(With `answer = \"YES\"`, "
        "as in your code now, ...)' instead of claiming a change; `lower(answer)` is a NameError the site explainer "
        "now gives its own kind; bonus rung 0 is `same = `; the misspelled Mar'tu in the uses-lower message is mended."
    ),
)

# 2A-05 ------------------------------------------------------------------------------------------

BROKEN_STARTER = (
    "roll = 17\n"
    'needed = "15"\n'
    "passed = roll => needed\n"
    "print(passed)\n"
    'clock_color = "blue"\n'
    'clock_is_red = "red"\n'
    "print(clock_is_red)\n"
)
BROKEN_KNOWN = ["roll", "needed", "passed", "clock_color", "clock_is_red"]


def _broken(needed='needed = 15', passed="passed = roll >= needed", clock='clock_is_red = clock_color == "red"'):
    return (
        "roll = 17\n"
        f"{needed}\n"
        f"{passed}\n"
        "print(passed)\n"
        'clock_color = "blue"\n'
        f"{clock}\n"
        "print(clock_is_red)\n"
    )


BROKEN_SPELL_2A = dict(
    id="broken-spell-2a",
    title="Broken spell",
    martu=(
        "Three bugs. Two are loud: Python stops and names a line. One is quiet: the code runs, but a box holds the "
        "wrong kind of thing.\n"
        "Read the last line of Python's message first. Then look at the line it names. Mend it, run again, and see "
        "what Python finds next."
    ),
    names=["roll", "needed", "passed", "clock_color", "clock_is_red"],
    pair_talk=(
        "Pair talk: you may hunt these bugs together. One of you reads the last line of Python's message out loud; "
        "the other points at the line it names. Each of you mends it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-the-sign",
            text="Mend the sign on line 3 so `passed` asks whether `roll` is at least `needed`.",
            dictated=False,
            hints=[
                "Read Python's last line: `SyntaxError: invalid syntax`. Python could not read line 3, so nothing ran.",
                "Python's message names line 3. Look at the two marks between `roll` and `needed`.",
                "*At least* is written `>=`: the `>` first, then the `=`. `=>` is not a sign Python knows.",
            ],
            checks=[
                bool_box("passed holds True or False", "passed", known=BROKEN_KNOWN, kept=True),
                no_is("passed compares with a sign, not is", ["roll", "needed"], msg=NUM_IS + " *At least* is `>=`."),
                (
                    "passed uses >=",
                    "assert _uses('op:GtE') or _uses('op:LtE'), ('`>` leaves out exactly enough. Use `>=`, with the `=` '\n"
                    "    'second.' if _uses('op:Gt') else 'Use `>=`, which means *at least*, with the `=` second.')\n"
                    # `roll <= needed` / `needed >= roll` mend the typo but ask *at most*: say so here, not a step later.
                    "import ast as _ast\n"
                    "_dir = [(getattr(_n.left, 'id', ''), type(_n.ops[0]).__name__, getattr(_n.comparators[0], 'id', '')) "
                    "for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'Compare' and len(_n.ops) == 1]\n"
                    "_good = [_d for _d in _dir if _d in (('roll', 'GtE', 'needed'), ('needed', 'LtE', 'roll'))]\n"
                    "_back = [_d for _d in _dir if _d in (('roll', 'LtE', 'needed'), ('needed', 'GtE', 'roll'))]\n"
                    "assert _good or not _back, ('That sign faces the wrong way: it asks whether `roll` is *at most* '\n"
                    "    '`needed`. Turn it around: `roll >= needed`.')",
                ),
            ],
        ),
        dict(
            id="mend-needed",
            text="Line 3 compares a number with text. Mend the line that makes `needed`, so it holds a number.",
            dictated=False,
            hints=[
                "Read Python's last line: a `TypeError`. `>=` can't compare an `int` (a whole number) with a `str` "
                "(text).",
                "Python's message names line 3, but the text comes from line 2. Look at the quotes there.",
                "Quotes make text. `\"7\" > 3` crashes, but `7 > 3` is True. Numbers don't need quotes.",
            ],
            checks=[
                (
                    "needed holds a number",
                    f"assert 'needed' in globals(), {_gone_text('needed', True)!r}\n"
                    "assert needed != '15', ('Take the quotes off on line 2: numbers don' + chr(39) + 't need quotes. '\n"
                    "    '`needed` still holds the starter' + chr(39) + 's `\"15\"`, which is text because of the quotes.')\n"
                    "assert type(needed).__name__ != 'str', ('Take the quotes off on line 2: numbers don' + chr(39) + 't '\n"
                    "    'need quotes. `needed` holds text, because of the quotes.')\n"
                    "assert type(needed).__name__ == 'int', '`needed` should hold a whole number, like `15`.'",
                ),
                bnd("passed: exactly enough passes", "passed", "roll", "needed", "pass", **ROLL_FIX),
            ],
            pass_line="Mar'tu: Both loud bugs mended. Now the quiet one.",
        ),
        dict(
            id="mend-clock",
            text="`clock_is_red` prints `red`, not a yes/no answer. Make it ask whether `clock_color` is the same as `\"red\"`.",
            dictated=False,
            hints=[
                "Read the last line Python printed: `red`. A yes/no answer would be `True` or `False`.",
                "Line 6 has one `=`. It puts the word red in the box instead of asking.",
                "`=` gets; `==` asks *is the same as*: `door_is_shut = door == \"shut\"`.",
            ],
            checks=[
                bool_box(
                    "clock_is_red holds True or False", "clock_is_red", known=BROKEN_KNOWN, foreign=["door", "door_is_shut"],
                    kept=True,
                    text_msg=(
                        "`clock_is_red` holds text, so it is not a yes/no answer (`True` or `False`). One `=` puts a "
                        "value in; `==` asks."
                    ),
                ),
                no_is("clock_is_red asks with ==, not is", ["clock_color"]),
                quoted_name("clock_color is the box, not the word", ["clock_color"]),
                strexact("red is spelled exactly", "red"),
                rerun_bool("clock_is_red follows the color (red)", {"clock_color": "red"}, "clock_is_red", "True",
                           "Ask the question with the box `clock_color`, so the answer follows it."),
                rerun_bool("clock_is_red follows the color (violet)", {"clock_color": "violet"}, "clock_is_red", "False",
                           "Ask the question with the box `clock_color`, so the answer follows it."),
            ],
            pass_line="Mar'tu: Three bugs, three mends. Two loud, one quiet. The quiet ones are sneaky, yes?",
        ),
    ],
    solution=_broken(),
    assemble=dict(
        lines=["roll = 17", "needed = 15", "passed = roll >= needed", "print(passed)", 'clock_color = "blue"',
               'clock_is_red = clock_color == "red"', "print(clock_is_red)"],
        distractors=["passed = roll => needed", 'needed = "15"', 'clock_is_red = "red"'],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Run. Python stops at the first loud bug and names the line. Mend it.\n"
                "2. Run again. A new message is good news: Python got further.\n"
                "3. When nothing stops, the checks speak. Read the message under the step."
            ),
        ),
        dict(
            angle="picture",
            label="Two kinds of bug",
            text=(
                "```text\nloud bug:\n  Python stops and\n  names the line.\n\n"
                "quiet bug:\n  the code runs, but a\n  box holds the wrong\n  kind of thing.\n```"
            ),
        ),
        dict(
            angle="shorter",
            text="`>=`, not `=>`. `15`, not `\"15\"`. `==` to ask, not `=`.",
        ),
    ],
    takeaway="`=>` is not a sign: write `>=`. Numbers have no quotes. One `=` puts a value in; `==` asks.",
    wrong_answers=[
        dict(why="the starter: => is not a sign (SyntaxError first)", code=BROKEN_STARTER, fails_at=0,
             message_contains="invalid syntax"),
        dict(why="sign mended, needed still text (TypeError)", code=_broken(needed='needed = "15"'), fails_at=0,
             message_contains="not supported between"),
        dict(why="loud bugs mended, clock_is_red still fills with text (not a bool)", code=_broken(clock='clock_is_red = "red"'),
             fails_at=3, message_contains="not a yes/no answer"),
        dict(why="mended to > instead of >=", code=_broken(passed="passed = roll > needed"), fails_at=1,
             message_contains="leaves out exactly enough"),
        dict(why="mended to <=: no error, but the sign faces the wrong way (used to pass CP1)",
             code=_broken(passed="passed = roll <= needed"), fails_at=1, message_contains="faces the wrong way"),
        dict(why="mended by swapping the boxes: needed >= roll asks at most", code=_broken(passed="passed = needed >= roll"),
             fails_at=1, message_contains="faces the wrong way"),
        dict(why="the comparison dropped: a typed True dodges the TypeError", code=_broken(needed='needed = "15"', passed="passed = True"),
             fails_at=1, message_contains="Use `>=`"),
        dict(why="=< instead of >=", code=_broken(passed="passed = roll =< needed"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="text turned into a number inside the question, line 2 left", code=_broken(
            needed='needed = "15"', passed="passed = roll >= int(needed)"), fails_at=2,
             message_contains="still holds the starter's"),
        dict(why="quotes kept but the number changed, mended inside the question", code=_broken(
            needed='needed = "16"', passed="passed = roll >= int(needed)"), fails_at=2,
             message_contains="`needed` holds text"),
        dict(why="two = signs in the clock line", code=_broken(clock='clock_is_red = clock_color = "red"'), fails_at=3,
             message_contains="two `=` signs"),
        dict(why="STREXACT: Red with a capital", code=_broken(clock='clock_is_red = clock_color == "Red"'), fails_at=3,
             message_contains="every letter"),
        dict(why="the answer typed in", code=_broken(clock="clock_is_red = False"), fails_at=3,
             message_contains='"red"'),
        dict(why="the box name in quotes", code=_broken(clock='clock_is_red = "clock_color" == "red"'), fails_at=3,
             message_contains="not the box"),
        dict(why="`is` for == (comes out right for these literals)", code=_broken(clock='clock_is_red = clock_color is "red"'),
             fails_at=3, message_contains="different question"),
        dict(why="hard-coded color: != the starter's blue", code=_broken(clock='clock_is_red = clock_color != "blue"'),
             fails_at=3, message_contains="violet"),
        dict(why="== to fill the box after a placeholder False",
             code=_broken(clock='clock_is_red = False\nclock_is_red == clock_color == "red"'), fails_at=3,
             message_contains="use one `=`"),
        dict(why="== on the box line: clock_is_red is never made", code=_broken(clock='clock_is_red == clock_color'),
             fails_at=0, message_contains="not defined"),
        dict(why="the starter box passed renamed (passed_roll)",
             code=_broken(passed="passed_roll = roll >= needed").replace("print(passed)", "print(passed_roll)"),
             fails_at=1, message_contains="Keep the box `passed` from the starter"),
        dict(why="the starter box needed renamed (need)",
             code=_broken(needed="need = 15", passed="passed = roll >= need"), fails_at=2,
             message_contains="Keep the box `needed` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="compare,boundary,gets-vs-same,read-traceback", solo="false",
             dictates="", foreign_names="door,door_is_shut") + "\n"
        "Three bugs, one checkpoint each, in the order Python's messages arrive: `=>` (SyntaxError on line 3), then "
        "`needed = \"15\"` (TypeError, reported on line 3 but mended on line 2: a lesson in reading the message), "
        "then the quiet `clock_is_red = \"red\"` (no error, so the check is 'not a yes/no answer'). Each bug left "
        "fails its own checkpoint: the two loud ones crash (fails_at=0, Python's own message), the quiet one fails "
        "CP3. On the site a crash fails every checkpoint, so no partials (mending only the sign still crashes on the "
        "TypeError). Can be done in pairs (pair_talk); every student mends it on their own screen.\n"
        "Check-breaker pass: CP1 now checks the sign's direction, so `roll <= needed` (no error, wrong question) "
        "is named at CP1 instead of turning CP1 green; `is` is caught in CP3.\n"
        "Ruling pass (Unit 2 reviews): a debug step's rung 0 is 'Read Python's last line' (Python 3.13: line 3 "
        "`SyntaxError: invalid syntax` for `=>`, then `TypeError: '>=' not supported between instances of 'int' and "
        "'str'`), and the quiet bug's is 'Read the last line Python printed: `red`'. `=>` and number-vs-text each "
        "have their own explainer kind on the site. CP2 says when `needed` still holds the starter's `\"15\"`. A "
        "renamed `passed` or `needed` gets 'Keep the box ... from the starter'."
    ),
)

# 2A-S -------------------------------------------------------------------------------------------

SOLO_STARTER = "mana = 9\ncost = 9\ncan_cast = mana > cost\nprint(can_cast)\n"


def _solo(line="can_cast = mana >= cost", cost="cost = 9"):
    return f"mana = 9\n{cost}\n{line}\nprint(can_cast)\n"


SOLO_2A = dict(
    id="solo-2a",
    title="Show Mar'tu",
    martu="One bug, just for you. Exactly enough mana still casts, yes?",
    solo=True,
    # Teacher ruling on the Unit 2 reviews: in Unit 2 SOLO items (and every QC2 exercise) the crash explainer
    # names the kind of slip and the line, but not the fix. Python's own text stays visible.
    explainer="lean",
    names=["mana", "cost", "can_cast"],
    starter=SOLO_STARTER,
    checkpoints=[
        dict(
            id="can-cast-right",
            text="Make `can_cast` right. Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Read the last line Python printed: `False`. Mana 9, cost 9: should the spell cast?",
                "Look at the sign in `can_cast = mana > cost`. Which sign includes the boundary?",
                "`>` leaves out the boundary; `>=` includes it: `4 >= 4` is True.",
            ],
            checks=[
                bool_box("can_cast holds True or False", "can_cast", known=["mana", "cost", "can_cast"],
                         foreign=["coins", "price", "can_buy", "passed"], kept=True),
                no_is("can_cast compares with a sign, not is", ["mana", "cost"], msg=NUM_IS),
                bnd("can_cast: exactly enough mana casts", "can_cast", "mana", "cost", "cast", **SOLO_FIX),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ exactly enough still passes.",
        ),
    ],
    solution=_solo(),
    assemble=dict(
        lines=["mana = 9", "cost = 9", "can_cast = mana >= cost", "print(can_cast)"],
        distractors=["can_cast = mana > cost", "can_cast = True", "can_cast = mana <= cost"],
    ),
    another_way=[
        dict(angle="step-by-step", text="Try mana 8, 9 and 10 against a cost of 9: only 8 should fail."),
        dict(angle="shorter", text="Exactly enough counts? `>=`."),
    ],
    takeaway="On your own: `>=` when exactly enough should still pass.",
    wrong_answers=[
        dict(why="starter unchanged: the boundary bug", code=SOLO_STARTER, fails_at=1,
             message_contains="Which sign counts the number itself?"),
        dict(why="the answer typed in", code=_solo(line="can_cast = True"), fails_at=1, message_contains="one short"),
        dict(why="a number typed in for cost", code=_solo(line="can_cast = mana >= 9"), fails_at=1,
             message_contains="cost = 12"),
        dict(why="== instead of >=", code=_solo(line="can_cast = mana == cost"), fails_at=1,
             message_contains="more than enough"),
        dict(why="the campaign's < copied", code=_solo(line="can_cast = mana < cost"), fails_at=1,
             message_contains="not enough?"),
        dict(why="seat B's bug: the cost in quotes (TypeError)", code=_solo(line='can_cast = mana >= "9"'), fails_at=0,
             message_contains="not supported between"),
        dict(why="> kept, cost lowered to make it pass", code=_solo(line="can_cast = mana > cost", cost="cost = 8"),
             fails_at=1, message_contains="exactly enough"),
        dict(why="=> instead of >=", code=_solo(line="can_cast = mana => cost"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="<= for >=: the sign mirrored", code=_solo(line="can_cast = mana <= cost"), fails_at=1,
             message_contains="faces the wrong way"),
        dict(why="`is` for a comparison sign", code=_solo(line="can_cast = mana is cost"), fails_at=1,
             message_contains="different question"),
        dict(why="the starter box can_cast dropped, the question printed instead",
             code="mana = 9\ncost = 9\nprint(mana >= cost)\n", fails_at=1,
             message_contains="Keep the box `can_cast` from the starter"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="boundary", solo="true", dictates="",
             foreign_names="coins,price,can_buy,passed",
             seat_b='can_cast = mana >= "9" (TypeError; the mend is to take the quotes off)') + "\n"
        "SOLO, one bug (C6). Seat A (and anyone solo) gets the boundary bug `can_cast = mana > cost` with mana and "
        "cost both 9; seat B would get `can_cast = mana >= \"9\"` (TypeError) once pair mode ships. Recorded, "
        "never blocking, never shown to a partner. BND check, the same as 2A-03 CP2 (needed is read from the "
        "student's own cost). Pass line in the Unit 1 SOLO style (showing off a skill on the map, not being "
        "watched).\n"
        "Ruling pass (Unit 2 reviews): `explainer=\"lean\"` (the crash explainer names the slip and the line, not "
        "the fix; Python's own text stays). Rung 0 is 'Read the last line Python printed: `False`' (the sign is "
        "rung 1). The mirrored-sign message is 'Your sign faces the wrong way: it asks *at most*.' with no sign "
        "named. A dropped `can_cast` line gets 'Keep the box `can_cast` from the starter'."
    ),
)

LESSON_2A = dict(
    kind="lesson",
    id="true-or-false-yes",
    title="True or False, Yes?",
    minutes=20,
    summary="Ask Python yes/no questions with `<`, `>`, `==`, `!=` and `>=`, and ignore capitals with `.lower()`.",
    notes=(
        "Lesson 2A (CC; 2A-05 SC). Preceded by 2a-remembers. Exactly one SOLO (solo-2a). Non-dictated checkpoints: "
        "2A-02 CP3, 2A-03 CP1-2, 2A-05 CP1-3, 2A-S. No `if` yet (2B). Campaign links are 'you have seen this': "
        "cast_spell's `<`, the dialogue part's `==`, the trap door's `>=`, Mar'tu's line's `.lower()`."
    ),
    exercises=[TRUE_OR_FALSE, ASK_WITH_DOUBLE_EQUALS, ENOUGH_TO_PASS, ANY_CASE_ANSWER, BROKEN_SPELL_2A, SOLO_2A],
)

ITEMS = [REMEMBERS_2A, LESSON_2A]
