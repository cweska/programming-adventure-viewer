"""Unit 8 "Code Challenges" ("Trials of the Yard"), part c: the Functions set (T-F-1, T-F-2, T-F-3) and the
Write-your-own-checks set (T-Own), each core challenge followed by its advanced variant (`level="advanced"`,
`variant_of=<core id>`), then the unit cheatsheet "How to Read a Test Table".

Spec: design/curriculum.md, "## Unit 8 · Code Challenges (optional)", the u08c rows of the set table, in order:
  T-F-1   make_bar(current, maximum, full="█", empty="░")   (prerequisite card 6B-08 defaults-and-names)
  T-F-1a  make_bar(...) that clamps `current` into 0..maximum
  T-F-2   apply_to_all(heroes, effect) -> a list of the names affected
  T-F-2a  apply_to_all(heroes, effect) -> only the names for which `effect(hero)` hands back True
  T-F-3   Refactor: the four-branch `elif` in reply(choice) becomes `lines[choice]`, with a default
  T-F-3a  A dict of functions: `actions[choice](hero)`; an unknown choice -> False
  T-Own   4 `assert` lines that would catch a wrong can_cast ("Mar'tu's seal", prerequisite 2-A2)
  T-Own-a seals that catch the `<=` slip in a given cast_ok and pass the correct one
  Cheatsheet "How to read a test table" (the unit's cheatsheet; u08a's framing card points here).
Every challenge is kind="challenge", optional, support="light", explainer on (the default "full"), engine False.
Nothing here is new to the concept gate: concept_map.json gives u08c no tokens.

Unlock ceiling (the curriculum's table: "Functions and T-Own | Unit 7 | Units 1-7, plus the 6B-08 and 2-A2 cards").
The harness gates by course order only, so every code field a student SEES (starter, solution, partials, assemble,
predict code, cheatsheet code) was also tokenized with the harness's own tokenizer against concept_map.json up to
u07c (see "Ceiling check" in the report): `def` / `return` / `pass`, lists, `.append`, `for`, dictionaries, `in` /
`not in`, `.get`, `None`, a function as a value, default values and keyword arguments (6B-08, u07c, pool: named in
each T-F-1 item as its prerequisite card) and `assert` (2-A2, u02c, optional: named in each T-Own item). No
f-strings, no escapes (`\\n` in a string), no `.items()` needed, no lambda in visible code.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. Every campaign link is "you've
seen this, now you'll get it": `get_mana_bar` and its typed `█` / `░` (mana-bars), `strengthen_magic` handed to
`add_spell` with no `()` and the `for member in party.members:` loop (spell-book), the trap-door checks that hand
back True or False (skill-checks), the four dialogue options as an `if/elif` chain (program-dialogue-options), and
`cast_spell`: `spell["spell_function"](caster)`, "Use `<` and not `<=`", and its check messages ("exactly enough mana
still casts") (hold-the-barrier). Every student has their own device; pair talk is optional and every checkpoint is
done solo.

The test table. FORMAT.md has `level` and `variant_of` for challenges (used), but no test-table field, so the table
is modelled with what exists (no invented fields), the same way as u08a and u08b:
  * Mar'tu's Learn pane shows the visible rows as a fenced table (36 characters a line at most), then "+ N hidden
    tests" (counted from the checks at the bottom of this file).
  * The starter prints the visible rows under u08a/b's comment, "# Visible tests. They should show" then the
    answers ("# ███░░, then ▮▮▯▯, then █--."; 36 characters a line or fewer), and, where the function starts as
    `pass`, "# (With only pass, each shows None.)" (make-bar, make-bar-clamped, apply-to-all, apply-if-it-worked;
    apply-to-all prints its `party[0]["mana"]` line after the two calls, under its own comment, so the None line
    is true of every line it covers). Run shows the student's answers next to the table's. Rows whose slip would
    crash the program are in the starter as well: the crash is Python's own error (the explainer's row), proven
    by a wrong answer at fails_at 0, and a twin wrong answer with the prints taken out proves Mar'tu's own
    message for the same slip (the site request: run the checks after such a crash, only to choose the message).
  * Each visible row is one named check ("row 2: make_bar(2, 4, "▮", "▯")"), and its message ends with u08a/b's
    evidence bracket, "(Mar'tu's check called `make_bar(2, 4, "▮", "▯")`: it handed back `"██░░"`, not
    `"▮▮▯▯"`.)". A row whose want is also an action (warm each hero once, take the mana from 5 to 8, stop at a
    seal) says what it should do, then what happened: "(Mar'tu's check called `apply_to_all(party, warm)`: it
    should hand back `['Oogrish', 'Lucky']` and warm each hero once; the effect ran 0 times for 2 heroes.)"; a
    T-Own row is not a call, so it says "Mar'tu's check ran a copy with `mana > cost`: ...". A visible row's
    list is shown as it is when every item is None, True, False, a number or one of the test's own names
    (`[None, None]`); a crash or `None` has no "not ...".
  * Each hidden test is one named check ("hidden: a full bar"). Its message names the label, never the values:
    "(Hidden test: a full bar. It handed back a different bar.)"; a list shows only its length.
  * T-Own turns the table round: the student writes the rows (seals), and the rows the trial checks are WRONG
    COPIES of the function ("row 1: a copy with mana > cost", "hidden: a copy that always says False"). The check
    reruns the student's whole program with the function's body swapped for the wrong copy, in a fresh namespace;
    a seal must stop it (AssertionError).
  * Core challenges: the table, then the hidden tests (T-F-2 adds "row 3 is yours": the student writes the call
    that hands `shout` over; T-Own: the seals, the two visible copies, the hidden copies). Advanced variants and the
    refactors: one checkpoint per new rule (the clamp's top and bottom; the refactor's dictionary, the lookup, the
    default), then the hidden tests. Each multi-step item has partials (staged solutions).
Site support that would make this nicer (for the report): a `tests=[dict(call=..., want=..., hidden=False,
label=...)]` field rendered as a real table with a pass/fail column; "Run the table" that shows every row's result
even when a row crashes the program; hidden rows shown as locked labels until they pass; for T-Own, a "wrong
copies" table whose rows turn green as each copy is stopped.

Check helpers (_TX below; check() puts in front of each check only the helpers it uses, as u07a/u08b do). Every
call a check makes uses Mar'tu's own data, deep-copied, prints captured, inside a line budget on the student's own
lines (u06c's guard), so a loop that never ends can't freeze the page. Every name starts with `_` and builtins come
from `_B`, so a student's `list = ...` can't break a check.
  _need() / _bar_sig()  the function exists with the signature's parameters, letter for letter, in order (the table
              read backwards gets its own message); make_bar keeps its default marks (gone, swapped or changed).
  _run() / _verdict()   one row: an error inside the function (row rules first, then _why), print instead of
              return, None, the wrong kind of value, value rules (the campaign's `Mana [` label), a value from the
              table typed in (hard-coding), the class's slips (each simulated at build time on the row's own data,
              so a slip's message is attached only when that slip really gives that answer), then the fallback.
  _fx()       apply_to_all rows: Mar'tu's recorder effect is handed over (it logs every call, then acts), so the
              check sees whether the effect ran, how often, on which sheets, in which order (not called, `effect`
              alone, `if effect:`, `effect()`, `effect(heroes)`, the global `warm` called by name, twice per hero),
              whether the roster was changed, and what came back (print, None, the roster itself, sheets, the
              effect's own `None`s or `True`s, a global accumulator, a typed list, the last name only, all names
              where only some are wanted, `"True"` in quotes, the sheet's mana read or the sheet watched for a
              change instead of the effect's answer, the names in another order). _lit_ret() first: when the
              function's only `return` is a typed list equal to a visible row's answer (`return ["Oogrish",
              "Lucky"]`, with or without a loop), "typed in it" comes before "nothing called the effect".
  _book() / _no_chain() / _keep_defs()  the refactors: the dictionary exists at the top (not inside the function, not
              a list, not keys and values swapped, every option a key letter for letter, every value the chain's own
              reply or the starter's own function object: `None` from `rest(...)`, `"rest"` in quotes and a shuffled
              function each named); the function no longer asks `choice == ...` and reads the dictionary; the four
              finished actions are left as they are.
  _act()      act rows: the hero's sheet before and after, and in hidden rows Mar'tu's recorders put in `actions` in
              place of the student's functions (the lookup must go through the dictionary, call once, on the hero
              handed in), then put back.
  _seal_*()   T-Own: the function left as Mar'tu wrote it (AST compare), the seals counted (top level, each calls the
              function, each says True or False instead of repeating the question), and each wrong copy rerun; for
              cast_ok a seal whose other value hides the slip (exact mana with too little skill) is named.
Messages: the fix first, then what happened, then the evidence in brackets (the Unit 2/3 ruling). Terminology
(2.9, one voice with u08a/b): a function "hands back" its answer ("Hand back only the names the effect said
`True` for"); `return` is named only as the keyword ("Put `return` after the loop"). A student's own text is
never shown (2.11): text handed back is shown only when it is one of the test's own names or replies, the
test's own marks, or "True"/"False". Invented Tor names only in hidden data (Pell, Brakka, Moss, Glug, Ivo, Ash,
Moth, Bree, Tinplate); never "Tester" and never a worksheet name.

The class's slips for this unit, each proven by a wrong_answers entry (item in brackets):
  * hard-coding the visible test's answer instead of computing it: one row's answer typed (`return "███░░"`, `return
    "█████"`: the next row says "typed in it"; `return ["Oogrish", "Lucky"]`, alone or after the loop: row 1 itself
    says "typed in it", before "nothing called the effect") and the whole table typed behind an
    `if` (passes every visible row; the hidden labeled tests catch it): make-bar, make-bar-clamped (a typed 5),
    apply-to-all, apply-if-it-worked, reply-lookup (`return "Steady, now."`: "Read the answer from the dictionary";
    a reply typed anywhere in `reply`, behind an `in [...]` question or in a second dictionary, is refused at CP2),
    act-lookup (the sheet changes typed behind `in [...]` questions: the hidden recorders catch it), and a typed
    table read with `[]` (make-bar: the hidden test's KeyError names the typed value).
  * `<` versus `<=` at the exact boundary, exactly enough counts: seal-can-cast (a copy with `>`; a copy that lets
    one short through; seals with no edge seal), seal-cast-ok (Bomb Shell's `<=` on the mana line, `<=` on the
    skill line, an exact-mana seal hidden behind too little skill, one mana short), make-bar-clamped (exactly full,
    exactly 0, one short of full in the hidden tests).
  * the empty case: an empty roster hands back `[]` (apply-to-all: None from a bare return, IndexError from
    `heroes[0]`), a bar of length 0 and an empty bar (make-bar), an unknown or empty choice gets the default
    (reply-lookup: KeyError; act-lookup: KeyError). (IndexError on `wall[-1]` and ZeroDivisionError for the
    average are T-L-1a and T-Lo-1a, in u08a and u08b; the cheatsheet's "empty case" entry names all three.)
  * the wrong type: `"True"` / `"False"` in quotes (act-lookup's unknown choice, a T-Own copy that hands back
    text), a list for a bar, a number for a bar, the effect's `None`s or `True`s for names, the roster's sheets for
    names, the function itself for `True` (act-lookup `return actions[choice]`).
  * print instead of return: make-bar, make-bar-clamped, apply-to-all, apply-if-it-worked, reply-lookup, act-lookup.
  * changing the list passed in when a new list was asked for: apply-to-all (the roster emptied with `.pop(0)`; the
    roster itself returned), reply-lookup (a key added to `lines` for an unknown choice), act-lookup (the hero
    changed for an unknown choice); and the reverse, a new list kept outside: apply-to-all (a global `names` list).
  * a KeyError for an unknown choice instead of the default (reply-lookup, act-lookup; `lines["choice"]` and
    `actions["choice"]` too). (The unknown-spell KeyError itself is T-D-1, in u08b.)
  * tie-breaking: not in this set's functions (T-D-1a / T-Lo-3a in u08b). The nearest Functions slip, the order of
    two questions, is T-Own-a: `cast_ok` asks about skill first, so a seal must give the other value plenty.
  * calling the effect function with () when passing it, or not calling it at all: apply-to-all row 3
    (`shout()`, `shout(party[0])`, `"shout"`: Python's own errors at the call, fails_at 0; an own loop; no print),
    apply-to-all inside the function (`effect` alone, never called, `effect()`, `effect(heroes)`, the global
    `warm`), apply-if-it-worked (`if effect:`, called twice), act-lookup (`rest()` / `rest(hero)` /
    `rest(lucky)` stored in the dictionary, `"rest"` quoted, `actions[choice]` with no `(hero)`, `return
    actions[choice]`, `actions[choice]()`, `return actions[choice](hero)`).
  * asserts that pass on a wrong function (weak checks): seal-can-cast and seal-cast-ok (no edge seal, only True
    seals, no one-short seal, seals that never use `== True` / `== False`, a seal that repeats the question, a seal
    that never calls the function, seals inside a `def`, the same seal twice to make up the count), and the
    function changed to fit the seals.
  * reading the test table backwards (input versus expected): the parameters in the other order (make-bar,
    apply-to-all row 3 `apply_to_all(shout, party)`), `current` and `maximum` used the other way round, keys and
    values swapped (reply-lookup, act-lookup), `max()` for `min()` in the clamp, a seal with mana and cost in the
    wrong order (`can_cast(10, 20) == True`, `cast_ok(10, 20, 9, 8) == True`: AssertionError on Mar'tu's own
    function, the explainer's "Your assert caught something" row), `if not effect(hero):`.

Help ladder (FORMAT.md and the Unit 2 walkthrough conventions): hints[0] Where to look; the middle hints Teach me,
with tiny examples on other names (listed in foreign_names); the last hint is Show me how, with a line from Mar'tu's
own solution first in backticks (its start is Start me off when the site can cut one; the harness checks it is in
the solution); never "Start like this" first. Then another_way (2+ angles), assemble (More structure: lines that
pass every checkpoint on their own) and the solution (Compare). Support is "light".
Two unit-wide rules for Show me how (the Nov 14 ruling, as in u08a and u08b):
  * No crash. Every Show rung, pasted word for word into the starter (in place of `pass`, or in place of the
    chain it replaces, in the order given, with the indentation its words describe), on top of the earlier
    checkpoints' rungs, runs with no crash: no `if` with nothing under it, no name that no line makes, and no
    starter row that the pasted lines make crash (reply-lookup's and act-lookup's row-3 prints: those CP2 rungs
    now carry the question that row needs). A part left to the student is named in words only ("then one for
    plenty", "one pair a line"). Each item's notes record the probe ("Show-rung copy-test"); a rung that is not
    the solution or a partial has its own wrong_answers entry ("Show me how ..., pasted word for word").
  * The sign at the edge. Where the visible rows cannot tell two edge signs apart, CP1's rung offers both
    complete lines and names the hidden test that decides. No u08c rung meets that case: the clamps' signs give
    the same bar either way (the clamp sets the number it was compared with), and the T-Own seals are numbers,
    not signs.

Setup: apply-to-all repeats the starter's `warm`, `shout` and `party`, and act-lookup repeats the four finished
actions, as hidden setup, so the Assemble lines (the function, and the row-3 call or the dictionary) run on their
own. The student's own copies in the starter replace them.

Phone width: fenced pictures, predict code, cheatsheet code and every starter and solution line keep to 36
characters or fewer, except two `def` lines whose signature the spec fixes and that read as broken code when
wrapped (u08a's ruling): `def make_bar(current, maximum, full="█", empty="░"):` and `def cast_ok(mana, cost,
affinity, required):`; and one solution line, apply-if-it-worked's `            names.append(hero["name"])` (38
characters), kept whole so Compare matches the Show rungs word for word (the Nov 14 ruling dropped the
`name = hero["name"]` line that used to keep it short).

Predicts: the right answer's place is mixed across the unit (u08c: make-bar 1, make-bar-clamped 2, apply-to-all 0,
apply-if-it-worked 1, reply-lookup 2, act-lookup 1, seal-can-cast 2, seal-cast-ok 0; the two at 0 have their
distractors reordered), so a choice's place never gives the answer away.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u08c
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
MODULE = "friends-in-low-places"


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# Check helpers (plain Python, run in the student's namespace after their code)
# ---------------------------------------------------------------------------------------------

_TX = r'''import ast as _ast
import copy as _copy
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__


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


def _quiet(_fn):
    # Run _fn with prints captured, inside the line budget: (value, printed lines, error).
    _buf = _Cap()
    _old = _sys.stdout
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _guarded(_fn)
    except _Runaway as _x:
        _err = _x
    except _B.Exception as _x:
        _err = _x
    finally:
        _sys.stdout = _old
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err


def _edits(_a, _b):
    _prev = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _x in _B.enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in _B.enumerate(_b, 1):
            _cur.append(_B.min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b):
    # NAME near miss: case, plural, or 1-2 edits.
    if _tn(_a) != 'str' or _tn(_b) != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower(), _b.lower()
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    return _B.min(_B.len(_la), _B.len(_lb)) >= 3 and _edits(_la, _lb) <= 2


def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    if not _q:
        return 'no parameters'
    return _q[0] if _B.len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _params(_f):
    _c = _f.__code__
    return _B.list(_c.co_varnames[:_c.co_argcount])


def _defs():
    return {_n.name: _n for _n in _tree.body if _tn(_n) == 'FunctionDef'}


def _need(_name, _want, _shown=''):
    # The function exists, made with `def`, with the signature's parameters in the signature's order.
    _line = _shown or '`def ' + _name + '(' + ', '.join(_want) + '):`'
    _v = _g.get(_name)
    if _tn(_v) != 'function':
        if _name in _g:
            assert False, ('`' + _name + '` is a variable, made with `=`. Keep the first line from the starter, '
                           + _line + ', with the steps indented under it.')
        _near = _B.sorted([_k for _k, _x in _B.list(_g.items()) if _tn(_x) == 'function' and not _k.startswith('_')
                           and _close(_k, _name)])
        if _near:
            assert False, ('Python matches names letter for letter: you wrote `' + _near[0] + '`, the trial needs `'
                           + _name + '`.')
        assert False, 'Keep the first line from the starter, ' + _line + ', with the steps indented under it.'
    _ps = _params(_v)
    if _ps != _B.list(_want):
        if _B.sorted(_ps) == _B.sorted(_want):
            assert False, ('Keep the parameters in the order of the first line, ' + _line + '. The table hands '
                           'them over in that order: ' + _names(_want) + '.')
        if _B.len(_ps) != _B.len(_want):
            assert False, ('`' + _name + '` takes ' + _B.str(_B.len(_want)) + ' parameter'
                           + ('' if _B.len(_want) == 1 else 's') + ': ' + _names(_want) + '. Keep ' + _line + '.')
        assert False, 'Keep the parameter names from the first line, ' + _line + '. Python matches names letter for letter.'
    return _v


def _an(_k):
    return ('an ' if _k[:1] in 'AEIOU' else 'a ') + _k


def _cap(_s):
    return _s[:1].upper() + _s[1:]


def _same(_v, _w):
    # Equal AND the same kind: True is not 1, "2" is not 2.
    _kv, _kw = _tn(_v), _tn(_w)
    if 'bool' in (_kv, _kw):
        return _kv == _kw and _v == _w
    if _kw in ('int', 'float'):
        return _kv in ('int', 'float') and _B.abs(_v - _w) < 1e-9
    return _kv == _kw and _v == _w


def _lit(_v):
    if _tn(_v) == 'str':
        return '"' + _v + '"'
    return _B.str(_v)


def _karg(_e):
    return _e.args[0] if _tn(_e) == 'KeyError' and _e.args else None


def _run(_f, _args, _kw=None):
    # One call, on deep copies of Mar'tu's data, prints captured, inside the line budget.
    _in = _copy.deepcopy(_B.list(_args))
    _work = _copy.deepcopy(_B.list(_args))
    _k = _B.dict(_kw or {})
    _val, _rows, _err = _quiet(lambda: _f(*_work, **_k))
    return {'val': _val, 'rows': _rows, 'err': _err, 'args': _in, 'after': _work}


def _item(_x):
    # One list item, shown as Python shows it, when it is safe to show: None, True, False, a number, or one of the
    # test's own names. Anything else (a student's own text, a sheet) gives None.
    _k = _tn(_x)
    if _k in ('NoneType', 'bool', 'int', 'float'):
        return _B.str(_x)
    if _k == 'str' and _x in _OK:
        return "'" + _x + "'"
    return None


def _sh(_v):
    # A value handed back, in words. Text only when it is one of the test's own names or replies, the test's own
    # marks, or "True"/"False"; never a student's own words (2.11). A hidden test never shows a number, a bar or
    # a list's items (only its length).
    _k = _tn(_v)
    _hid = _ROW[0] == 'h'
    if _k == 'NoneType':
        return '`None`'
    if _k == 'bool':
        return '`' + _B.str(_v) + '`'
    if _k in ('int', 'float'):
        return 'a different number' if _hid else '`' + _B.str(_v) + '`'
    if _k == 'str':
        if _v == '':
            return 'empty text, `""`'
        if _v in _OK or _v in ('True', 'False'):
            return 'the text `"' + _v + '"`'
        if _MARKS and _B.all(_c in _MARKS for _c in _v):
            return 'a different bar' if _hid else '`"' + _v + '"`'
        return 'some other text'
    if _k == 'list':
        if not _v:
            return 'an empty list, `[]`'
        _shown = [_item(_x) for _x in _v]
        if not _hid and None not in _shown:
            return '`[' + ', '.join(_shown) + ']`'
        return 'a list of ' + _B.str(_B.len(_v)) + (' item' if _B.len(_v) == 1 else ' items')
    if _k == 'dict':
        return 'a whole dictionary'
    if _k == 'function':
        return 'a function'
    return _an(_k)


def _did(_r):
    if _r['err'] is not None:
        if _tn(_r['err']) == '_Runaway':
            return 'it never finished'
        return 'Python stopped with ' + _an(_tn(_r['err']))
    if _r['val'] is None and _r['rows']:
        return 'it printed a line but handed back `None`'
    return 'it handed back ' + _sh(_r['val'])


def _evs(_r=None, _what=''):
    # The evidence bracket (u08a/b's form). A visible test shows its call: for a value row "it handed back Y, not
    # Z"; for a row whose want is also an action (warm each hero once, the mana from 5 to 8, stop at a seal) "it
    # should <want>; <what it did>". A hidden test shows only its label.
    _d = _what or _did(_r)
    if _ROW[0] == 'v':
        _how = "(Mar'tu's check " + ('called ' if _ROW[2][:1] == '`' else 'ran ') + _ROW[2] + ': '
        if _ROW[4]:
            if (not _what and _r['err'] is None and _r['val'] is not None
                    and not _same(_r['val'], _g.get('_WANT'))):
                _d = _d + ', not ' + _ROW[4]
            return _how + _d + '.)'
        return _how + 'it should ' + _ROW[3] + '; ' + _d + '.)'
    return '(Hidden test: ' + _ROW[1] + '. ' + _cap(_d) + '.)'


def _why(_e):
    # A kind message for an error raised inside the student's function while Mar'tu's check called it.
    _k = _tn(_e)
    _s = _B.str(_e)
    _f = _g.get(_FN)
    _ps = _params(_f) if _tn(_f) == 'function' else []
    _ing = 'The parameters of `' + _FN + '` are ' + _names(_ps) + '.'
    if _k == '_Runaway':
        return 'Make every loop end: with these values your function never finished.'
    if _k == 'KeyError':
        _x = _karg(_e)
        if _tn(_x) == 'str' and _x in _ps:
            return ('Take the quotes off `"' + _x + '"` to use the parameter `' + _x + '`. With quotes, Python looks '
                    'for a key spelled ' + _x + '. ' + _QUOTES)
        return 'Use a key the dictionary really has, or ask with `in` first: Python found no such key.'
    if _k == 'IndexError':
        return 'Loop over the list with `for`, not typed positions: Python went past the end of the list.'
    if _k in ('NameError', 'UnboundLocalError'):
        _x = _B.getattr(_e, 'name', None) or ''
        if not _x:
            _m = _re.search(r"'(\w+)'", _s)
            _x = _m.group(1) if _m else ''
        if _k == 'UnboundLocalError' or 'local variable' in _s or 'not associated' in _s:
            return 'Make `' + _x + '` before the line that uses it. Python runs a function from the top down.'
        if [_p for _p in _ps if _close(_x, _p)]:
            return _ing + ' You wrote `' + _x + '`. Python matches names letter for letter.'
        return 'Inside `' + _FN + '`, Python found a name it does not know: `' + _x + '`. ' + _ing
    if _k == 'TypeError':
        if 'not callable' in _s:
            return 'Put `(...)` only after a function: the value before your brackets is not a function.'
        if 'positional argument' in _s:
            return 'Count the values against the `def` line: a call inside your function hands over the wrong number.'
        if "can't multiply sequence" in _s:
            return 'Multiply a mark by a number, like `full * current`: one side of your `*` must be a number.'
        if 'unsupported operand' in _s or 'concatenate' in _s:
            return ('Add and take away numbers with numbers, and glue text to text: one side of a sign holds the '
                    'wrong kind of value.')
        if 'list indices must be integers' in _s:
            return 'Read a list by position, or loop over it: a list has no keys.'
        if 'string indices must be integers' in _s:
            return 'Read the dictionary, not text: take the quotes off the parameter\'s name. ' + _QUOTES
        if 'not iterable' in _s:
            return 'A `for` loop walks a list: check which value your loop walks.'
        if 'not subscriptable' in _s:
            return 'Use square brackets only on a list or a dictionary.'
    if _k == 'AttributeError':
        return 'Check the value before the dot: it has no tool with that name.'
    return 'Mend this, then Run again: ' + _k + (': ' + _s if _s else '') + '.'


def _none_msg():
    # Why the function handed back None.
    _d = _defs().get(_FN)
    if _d is None:
        return 'Hand back the answer with `return`.'
    _rets = [_n for _n in _ast.walk(_d) if _tn(_n) == 'Return']
    if _B.all(_tn(_n) == 'Pass' for _n in _d.body):
        return 'Replace `pass` with the steps, and `return` the answer.'
    if not _rets:
        return 'Add a `return` line: a function with no `return` hands back `None`.'
    if [_n for _n in _rets if _n.value is None]:
        return 'Put the answer after `return`: a bare `return` hands back `None`.'
    return ('Give every path a `return`: with these values your function reached its end without one, so it handed '
            'back `None`.')


def _kind_msg(_v, _w):
    # The wrong KIND of value: text for True, a list for a bar ...
    _kv, _kw = _tn(_v), _tn(_w)
    if _kv == _kw or (_kv in ('int', 'float') and _kw in ('int', 'float')):
        return ''
    if _kv in _KIND:
        return _KIND[_kv]
    if _kw == 'bool':
        if _kv == 'str' and _v in ('True', 'False'):
            return ('Hand back `True` or `False` with no quotes. With quotes it is text, and text is not a yes or '
                    'a no.')
        return 'Hand back `True` or `False`: this trial asks a yes-or-no question.'
    if _kw == 'str':
        return 'Hand back text: this trial wants a piece of text.'
    if _kw == 'list':
        return 'Hand back a list, in square brackets.'
    return ''


def _typed_in(_v=None, _only=False):
    # A value from the table typed into the function's steps (hard-coding). The `def` line is not read, so its
    # default values never count. With _v and _only: only that value.
    _d = _defs().get(_FN)
    if _d is None or not _TYPED:
        return ''
    for _st in _d.body:
        for _n in _ast.walk(_st):
            if _tn(_n) != 'Constant' or _tn(_n.value) not in ('str', 'int'):
                continue
            if _n.value in _TYPED and (not _only or _same(_n.value, _v)):
                return ('Use the parameters, not values from the table: your function has `' + _lit(_n.value)
                        + '` typed in it, so it only works for those rows.')
    return ''


def _outer():
    # A list or dictionary made at the top level and read inside the function instead of its parameter.
    _d = _defs().get(_FN)
    if _d is None:
        return ''
    _ps = [_a.arg for _a in _d.args.args]
    _local = _B.set(_x.id for _x in _ast.walk(_d) if _tn(_x) == 'Name' and _tn(_x.ctx) == 'Store')
    for _n in _ast.walk(_d):
        if (_tn(_n) == 'Name' and _tn(_n.ctx) == 'Load' and _n.id not in _ps and _n.id not in _local
                and _n.id not in _GLOB and _tn(_g.get(_n.id)) in ('dict', 'list')):
            return ('Use the parameters, ' + _names(_ps) + ', not `' + _n.id + '`: the function must work on what '
                    'the call hands it.')
    return ''


def _has(_s):
    # True when the function's own code holds the constant _s (a key such as "mana", or the text "True").
    _d = _defs().get(_FN)
    return _d is not None and _B.any(_tn(_n) == 'Constant' and _tn(_n.value) == 'str' and _n.value == _s
                                     for _n in _ast.walk(_d))


def _sets(_name):
    # True when the function gives the name _name a new value with `=`.
    _d = _defs().get(_FN)
    return _d is not None and _B.any(_tn(_n) == 'Assign' and _B.any(_tn(_t) == 'Name' and _t.id == _name
                                                                     for _t in _n.targets) for _n in _ast.walk(_d))


def _verdict(_r, _want, _errs=(), _alts=(), _keep=True, _vr=()):
    # One table row, checked in the order the notes give.
    _v, _e = _r['val'], _r['err']
    if _e is not None:
        for _c, _m in _errs:
            if _c(_e):
                assert False, _m + ' ' + _evs(_r)
        if _tn(_e) in ('KeyError', 'IndexError'):
            _ty = _typed_in()
            if _ty:
                assert False, _ty + ' ' + _evs(_r)
        assert False, _why(_e) + ' ' + _evs(_r)
    if _v is None and not _same(_v, _want):
        if _r['rows']:
            assert False, ('Use `return`, not `print`: the test reads what your function hands back, and `print` '
                           'only shows it. ' + _evs(_r))
        assert False, (_NONE or _none_msg()) + ' ' + _evs(_r)
    _t = _kind_msg(_v, _want)
    if _t:
        assert False, _t + ' ' + _evs(_r)
    if not _same(_v, _want):
        for _c, _m in _vr:
            if _c(_v):
                assert False, _m + ' ' + _evs(_r)
        _ty = _typed_in(_v, True) or _typed_in() or _outer()
        if _ty:
            assert False, _ty + ' ' + _evs(_r)
        for _a, _m, _c in _alts:
            if _same(_v, _a) and (_c is None or _c()):
                assert False, _m + ' ' + _evs(_r)
        assert False, _FALL + ' ' + _evs(_r)
    if _keep:
        _ps = _params(_g[_FN])
        for _i, (_a, _b) in _B.enumerate(_B.zip(_r['args'], _r['after'])):
            if _a != _b:
                assert False, (_KEEPMSG or ('Leave `' + _ps[_i] + '` as it was: your function changed what it was '
                                            'handed. Read it; don\'t change it.')) + ' ' + _evs(
                    _r, 'it changed `' + _ps[_i] + '`')


def _bar_sig():
    # make_bar keeps its default marks on the `def` line.
    _line = '`def make_bar(current, maximum, full="█", empty="░"):`'
    _f = _need('make_bar', ['current', 'maximum', 'full', 'empty'], _line)
    _d = _B.tuple(_f.__defaults__ or ())
    if _d == ('░', '█'):
        assert False, ('Swap the default marks back: `full="█"` is the full mark, and `empty="░"` the empty one. '
                       'Keep ' + _line + '.')
    assert _B.len(_d) == 2, ('Keep the default marks on the `def` line: ' + _line + '. A call like `make_bar(3, 5)` '
                             'hands over no marks, so the function needs its own.')
    assert _d == ('█', '░'), 'Keep the default marks from the starter: ' + _line + '.'


def _fx_outer(_d):
    # apply_to_all reads a list made at the top level: the roster (`party`), or a list of names kept outside.
    if _d is None:
        return ''
    _ps = [_a.arg for _a in _d.args.args]
    _local = _B.set(_x.id for _x in _ast.walk(_d) if _tn(_x) == 'Name' and _tn(_x.ctx) == 'Store')
    for _x in _ast.walk(_d):
        if _tn(_x) == 'Name' and _tn(_x.ctx) == 'Load' and _x.id not in _ps and _x.id not in _local:
            _val = _g.get(_x.id)
            if _tn(_val) == 'list':
                if _val and _B.all(_tn(_y) == 'dict' for _y in _val):
                    return ('Use the parameter `heroes`, not `' + _x.id + '`: the function must work on the roster '
                            'it is handed.')
                return ('Make the list of names inside the function, before the loop: `' + _x.id + '` lives '
                        'outside it, so it keeps the names from every call.')
    return ''


def _lit_ret():
    # Hard-coding: the function's only `return` hands back a list typed in, equal to a visible row's answer
    # (`return ["Oogrish", "Lucky"]`, with or without a loop). Asked before "nothing called the effect".
    _d = _defs().get(_FN)
    if _d is None:
        return ''
    _rets = [_x for _x in _ast.walk(_d) if _tn(_x) == 'Return']
    if _B.len(_rets) != 1 or _tn(_rets[0].value) != 'List' or not _rets[0].value.elts:
        return ''
    if not _B.all(_tn(_x) == 'Constant' for _x in _rets[0].value.elts):
        return ''
    if [_x.value for _x in _rets[0].value.elts] not in _SEEN:
        return ''
    return _typed_in() or ('Use the parameters, not values from the table: your function hands back a list '
                           'typed in it, so it only works for one row.')


def _fx(_r, _hs, _given, _log, _want, _after, _alts=(), _calls_only=False):
    # One apply_to_all row: Mar'tu's recorder effect logged every call (_log) before it acted.
    _d = _defs().get(_FN)
    _n = _B.len(_given)
    _ids = [_B.id(_h) for _h in _given]
    _v, _e = _r['val'], _r['err']
    _bad = [_x for _x in _log if _B.id(_x) not in _ids]
    _ran = ('the effect ran ' + _B.str(_B.len(_log)) + (' time' if _B.len(_log) == 1 else ' times') + ' for '
            + _B.str(_n) + (' hero' if _n == 1 else ' heroes'))
    if _e is not None:
        _s = _B.str(_e)
        _k = _tn(_e)
        if [_x for _x in _bad if _tn(_x) in ('list', 'tuple')]:
            assert False, ('Hand over one hero, `effect(hero)`, not the whole list: an effect works on one sheet at '
                           'a time. ' + _evs(_r))
        if [_x for _x in _bad if _tn(_x) == 'str']:
            assert False, ('Hand over the whole sheet, `effect(hero)`: the effect reads and changes the sheet, not '
                           'only the name. ' + _evs(_r))
        if _k == 'TypeError' and 'required positional argument' in _s and not _log:
            assert False, ('Hand the hero to the effect: `effect(hero)`. With empty `()`, the effect has no hero '
                           'to work on. ' + _evs(_r))
        if _k == 'TypeError' and "'list' object is not callable" in _s:
            assert False, 'Call `effect`, the function, not `heroes`, the list: `effect(hero)`. ' + _evs(_r)
        if _k == 'TypeError' and 'not iterable' in _s:
            assert False, ('Loop over `heroes`, the list: `for hero in heroes:`. `effect` is the function. '
                           + _evs(_r))
        if _k == 'IndexError':
            assert False, ('Walk the roster with `for hero in heroes:`, not typed positions: an empty roster has no '
                           '`heroes[0]`. ' + _evs(_r))
        assert False, _why(_e) + ' ' + _evs(_r)
    if _d is not None and _B.all(_tn(_x) == 'Pass' for _x in _d.body):
        assert False, ('Replace `pass` with the steps: a loop that calls `effect(hero)`, and a list of names to '
                       'hand back. ' + _evs(_r, _ran if _calls_only else ''))
    _lt = _lit_ret()
    if _lt:
        assert False, _lt + ' ' + _evs(_r, _did(_r) + ', typed in the `return` line'
                                        + ('' if _B.len(_log) == _n else ', and ' + _ran))
    _o = _fx_outer(_d)
    if _o:
        assert False, _o + ' ' + _evs(_r, 'it read a list from outside the function')
    _w = _B.list(_ast.walk(_d)) if _d is not None else []
    if _n and not _log:
        _msg = 'Call `effect(hero)` inside the loop: nothing called the effect, so no hero changed.'
        _own = [_x.func.id for _x in _w if _tn(_x) == 'Call' and _tn(_x.func) == 'Name'
                and _tn(_g.get(_x.func.id)) == 'function' and _x.func.id != _FN]
        if [_x for _x in _w if _tn(_x) == 'Expr' and _tn(_x.value) == 'Name' and _x.value.id == 'effect']:
            _msg = ('`effect` on its own line names the function but does not run it. Add `(hero)`: '
                    '`effect(hero)`.')
        elif [_x for _x in _w if _tn(_x) == 'If' and _tn(_x.test) == 'Name' and _x.test.id == 'effect']:
            _msg = ('`if effect:` only asks whether there is a function, and there always is. Call it: '
                    '`if effect(hero):`.')
        elif _own:
            _msg = ('Call `effect(hero)`, the function you were handed: your function calls `' + _own[0]
                    + '` itself, so any other effect would never run.')
        assert False, _msg + ' ' + _evs(_r, _ran)
    if _bad:
        assert False, 'Hand each hero from `heroes` to the effect: `effect(hero)`. ' + _evs(_r, _ran)
    _early = False
    for _x in _w:
        if _tn(_x) in ('For', 'While'):
            for _y in _x.body:
                if [_z for _z in _ast.walk(_y) if _tn(_z) == 'Return']:
                    _early = True
    if _B.len(_log) < _n:
        if _early:
            assert False, ('Put `return` after the loop, not inside it: your function stopped after the first '
                           'hero. ' + _evs(_r, _ran))
        assert False, 'Call `effect(hero)` once for every hero in `heroes`. ' + _evs(_r, _ran)
    if _B.len(_log) > _n:
        if _VAR:
            assert False, ('Call `effect(hero)` once for each hero, and keep what it hands back: `if '
                           'effect(hero):` runs it and asks in one line. A second call runs the effect again. '
                           + _evs(_r, _ran))
        assert False, 'Call `effect(hero)` once for each hero, not more. ' + _evs(_r, _ran)
    if [_B.id(_x) for _x in _log] != _ids:
        assert False, 'Call `effect(hero)` once on each hero, in the order of `heroes`. ' + _evs(_r, _ran)
    if _B.len(_hs) != _n or _B.any(_a is not _b for _a, _b in _B.zip(_hs, _given)):
        assert False, ('Leave `heroes` as it was: your function changed the roster it was handed. Walk it with '
                       '`for hero in heroes:`, and take no hero out. ' + _evs(_r, 'the roster changed'))
    if [_B.dict(_h) for _h in _given] != _after:
        assert False, ('Let the effect do the changing: your function changed a hero\'s sheet itself. '
                       + _evs(_r, 'a sheet changed'))
    if _calls_only:
        return
    if _v is None:
        if _r['rows']:
            assert False, ('Use `return`, not `print`: the test reads what your function hands back, and `print` '
                           'only shows it. ' + _evs(_r))
        if not _n:
            assert False, ('Hand back a list even for an empty roster: make the empty list before the loop, and '
                           'put `return` after the loop. ' + _evs(_r))
        assert False, _none_msg() + ' ' + _evs(_r)
    if _tn(_v) != 'list':
        assert False, ('Hand back a list of names, in square brackets: make an empty list before the loop, and '
                       '`.append()` each name. ' + _evs(_r))
    if _v is _hs:
        assert False, ('Make a new list of names: your function handed back the same roster it was given. '
                       + _evs(_r))
    if _v and _B.all(_tn(_x) == 'dict' for _x in _v):
        assert False, 'Put each hero\'s name in the list, `hero["name"]`, not the whole sheet. ' + _evs(_r)
    if _v and _B.all(_x is None for _x in _v):
        assert False, ('`effect(hero)` changes the sheet and hands back `None`. Append the hero\'s name, '
                       '`hero["name"]`, not what the effect hands back. ' + _evs(_r))
    if _v and _B.all(_tn(_x) == 'bool' for _x in _v):
        assert False, ('Append the hero\'s name when the effect hands back `True`, not the `True` itself. '
                       + _evs(_r))
    if _v != _want:
        _ty = _typed_in()
        if _ty:
            assert False, _ty + ' ' + _evs(_r)
        for _a, _m, _c in _alts:
            if _v == _a and (_c is None or _c()):
                assert False, _m + ' ' + _evs(_r)
        if _B.all(_tn(_x) == 'str' for _x in _v) and _B.sorted(_v) == _B.sorted(_want):
            assert False, ('Keep the names in the order of `heroes`: append each name as the loop reaches its '
                           'hero. ' + _evs(_r))
        assert False, _FALL + ' ' + _evs(_r)


def _arg(_c, _i, _k):
    # A call's value number _i (from 0), by position or by keyword _k.
    if _B.len(_c.args) > _i:
        return _c.args[_i]
    for _x in _c.keywords:
        if _x.arg == _k:
            return _x.value
    return None


def _book(_name, _want, _funcs):
    # The refactor's dictionary: at the top, a dictionary, read by option, every option, every value its own.
    _d = _defs().get(_FN)
    _where = 'above `def ' + _FN + '`'
    if _name not in _g or _tn(_g.get(_name)) == 'function':
        if _d is not None and [_x for _x in _ast.walk(_d) if _tn(_x) == 'Dict']:
            assert False, ('Make `' + _name + '` at the top of the program, ' + _where + ', not inside the '
                           'function: the trial reads it from there.')
        assert False, ('Make the dictionary `' + _name + '` at the top of the program, ' + _where + ': `' + _name
                       + ' = {`, then one pair a line, then `}`.')
    _L = _g[_name]
    if _tn(_L) in ('list', 'tuple'):
        assert False, ('Make `' + _name + '` a dictionary, with `{ }` and `"option 1": ...` pairs: a list is read by '
                       'position, not by option.')
    assert _tn(_L) == 'dict', 'Make `' + _name + '` a dictionary: `{`, then pairs like `"option 1": ...`, then `}`.'
    _vals = [(_g.get(_x) if _funcs else _x) for _x in _want.values()] + _B.list(_want.values())
    _keys = _B.list(_L)
    if _keys and _B.all(_B.any(_k is _x or (_tn(_k) == 'str' and _k == _x) for _x in _vals) for _k in _keys):
        assert False, ('Put the option on the left of each `:`, and its ' + ('function' if _funcs else 'reply')
                       + ' on the right: `' + _name + '` is read by the option.')
    for _k in _want:
        if _k not in _L:
            _near = [_x for _x in _keys if _tn(_x) == 'str' and _x.lower().replace(' ', '') == _k.replace(' ', '')]
            if _near:
                assert False, ('Use the keys exactly as the `elif` chain has them: `"' + _k + '"`, all lower case, '
                               'with one space. Every letter, space and capital counts.')
            assert False, 'Give `' + _name + '` all four options as keys: `"' + _k + '"` is missing.'
    for _k, _w in _want.items():
        _x = _L[_k]
        if _funcs:
            if _x is _g.get(_w):
                continue
            if _x is None:
                assert False, ('Store the function itself, `' + _w + '`, with no `()`: `' + _name + '["' + _k
                               + '"]` holds `None`, because `' + _w + '(...)` ran the function and stored what it '
                               'handed back.')
            if _tn(_x) == 'str':
                if _x == _w:
                    assert False, ('Take the quotes off `' + _w + '`: with quotes, `' + _name + '["' + _k + '"]` '
                                   'holds text, and text cannot be called. ' + _QUOTES)
                assert False, 'Store the function `' + _w + '` itself under `"' + _k + '"`: no quotes and no `()`.'
            _others = [_y for _y in _want.values() if _g.get(_y) is _x]
            if _others:
                assert False, ('Match each option with its own function, as the `elif` chain does: `"' + _k
                               + '"` runs `' + _w + '`, not `' + _others[0] + '`.')
            assert False, 'Store the starter\'s function `' + _w + '` under `"' + _k + '"`, with no `()`.'
        else:
            if _x == _w:
                continue
            if _x in _want.values():
                assert False, ('Match each option with its own reply, as the `elif` chain does: `"' + _k + '"` '
                               'holds the reply of another option.')
            assert False, ('Copy each reply exactly from the `elif` chain: `' + _name + '["' + _k + '"]` is not the '
                           'same text. Every letter, space and capital counts.')


def _no_chain(_fn, _p, _dict, _show):
    # The refactor: the function asks no `choice == ...` questions, and reads the dictionary.
    _d = _defs().get(_fn)
    assert _d is not None, 'Keep the function `' + _fn + '`, made with `def`, and change only its steps.'
    _eq = [_x for _x in _ast.walk(_d) if _tn(_x) == 'Compare'
           and _B.any(_tn(_o) in ('Eq', 'NotEq') for _o in _x.ops)
           and _B.any(_tn(_y) == 'Name' and _y.id == _p for _y in [_x.left] + _B.list(_x.comparators))]
    assert not _eq, ('Replace the `elif` chain with one lookup, `' + _show + '`: `' + _fn + '` still asks `' + _p
                     + ' == ...`.')
    assert [_x for _x in _ast.walk(_d) if _tn(_x) == 'Name' and _x.id == _dict], (
        'Read the answer from the dictionary: `' + _show + '`, inside `' + _fn + '`.')


def _keep_defs(_srcs):
    # The finished actions are left as they are (when the student's code defines them).
    _have = _defs()
    for _src in _srcs:
        _w = _ast.parse(_src).body[0]
        _x = _have.get(_w.name)
        if _x is not None and _ast.dump(_x) != _ast.dump(_w):
            assert False, ('Leave `' + _w.name + '` as it is: the four actions are finished. Change only `act`, and '
                           'add `actions` above it.')


def _act(_choice, _hero, _want, _after, _rec=False, _extra=''):
    # One act row. _rec: Mar'tu's recorders go into `actions` in place of the student's functions, then back.
    _f = _need('act', ['choice', 'hero'])
    _d = _defs().get('act')
    _A = _g.get('actions')
    _h = _copy.deepcopy(_hero)
    _h0 = _copy.deepcopy(_hero)
    _log = []
    _saved = None
    if _rec and _tn(_A) == 'dict':
        _saved = _B.dict(_A)
        _A.clear()
        for _k in _B.list(_saved) + ([_extra] if _extra else []):
            _A[_k] = (lambda _kk: (lambda hero: _log.append((_kk, hero))))(_k)
    _keys0 = _B.list(_A) if _tn(_A) == 'dict' else None
    try:
        _v, _rows, _e = _quiet(lambda: _f(_choice, _h))
        _keys1 = _B.list(_A) if _tn(_A) == 'dict' else None
    finally:
        if _saved is not None:
            _A.clear()
            _A.update(_saved)
    _r = {'val': _v, 'rows': _rows, 'err': _e}
    _ran = _B.len(_log) > 0 if _rec else _h != _h0
    if _e is not None:
        _s = _B.str(_e)
        _k = _tn(_e)
        if _k == 'KeyError' and _karg(_e) == _choice:
            assert False, ('Ask first: `if choice not in actions:`, then `return False`. Python stopped with a '
                           'KeyError: `actions` has no such key. ' + _evs(_r))
        if _k == 'KeyError' and _karg(_e) == 'choice':
            assert False, ('Take the quotes off `"choice"` to use the parameter `choice`. ' + _QUOTES + ' '
                           + _evs(_r))
        if _k == 'TypeError' and 'required positional argument' in _s:
            assert False, ('Hand over the hero: `actions[choice](hero)`. Empty `()` gives the function no hero to '
                           'work on. ' + _evs(_r))
        if _k == 'TypeError' and 'not callable' in _s:
            assert False, ('Store the functions themselves in `actions`, with no quotes and no `()`, so '
                           '`actions[choice]` is a function you can call. ' + _evs(_r))
        if _k == 'NameError' and 'actions' in _s:
            assert False, 'Make `actions` at the top, above `def act`, so `act` can read it. ' + _evs(_r)
        assert False, _why(_e) + ' ' + _evs(_r)
    if _keys0 is not None and _keys1 != _keys0:
        assert False, 'Leave `actions` as it was: your `act` added or took out a key. ' + _evs(_r)
    if _d is not None:
        _local = _B.set(_x.id for _x in _ast.walk(_d) if _tn(_x) == 'Name' and _tn(_x.ctx) == 'Store')
        for _x in _ast.walk(_d):
            if (_tn(_x) == 'Name' and _tn(_x.ctx) == 'Load' and _x.id not in ('choice', 'hero', 'actions')
                    and _x.id not in _local and _tn(_g.get(_x.id)) == 'dict'):
                assert False, ('Use the parameter `hero`, not `' + _x.id + '`: `act` must work on the hero it is '
                               'handed. ' + _evs(_r, 'it worked on `' + _x.id + '` instead'))
    _w = _B.list(_ast.walk(_d)) if _d is not None else []
    if _want is True:
        if _tn(_v) == 'function':
            assert False, ('Call the function, then hand back `True`: `actions[choice]` finds it, and `(hero)` on '
                           'the end runs it. Your `act` handed back the function itself. ' + _evs(_r))
        if _rec and not _log and _h != _h0:
            assert False, ('Read the function from `actions` itself, inside `act`: when Mar\'tu\'s test put other '
                           'functions in `actions`, your `act` did not call them. ' + _evs(_r, 'it skipped them'))
        if not _ran:
            if [_x for _x in _w if _tn(_x) == 'Expr' and _tn(_x.value) == 'Subscript']:
                assert False, ('Add `(hero)` on the end: `actions[choice](hero)`. Without it, Python finds the '
                               'function but never runs it. ' + _evs(_r, 'the hero did not change'))
            assert False, ('Call the function you looked up: `actions[choice](hero)`. '
                           + _evs(_r, 'the hero did not change'))
        if _v is None:
            if [_x for _x in _w if _tn(_x) == 'Return' and _tn(_x.value) == 'Call']:
                assert False, ('The action changes the sheet and hands back `None`. Call it on one line, then `return '
                               'True` on the next. ' + _evs(_r))
            if _rows:
                assert False, ('Use `return`, not `print`: the test reads what your function hands back. '
                               + _evs(_r))
            assert False, 'Hand back `True` after the action runs. ' + _evs(_r)
        _t = _kind_msg(_v, True)
        if _t:
            assert False, _t + ' ' + _evs(_r)
        if _v is not True:
            assert False, 'Hand back `True` when the action ran. ' + _evs(_r)
        if _rec:
            if _B.len(_log) > 1:
                assert False, ('Call the action once: `actions[choice](hero)`, on one line. '
                               + _evs(_r, 'it ran ' + _B.str(_B.len(_log)) + ' times'))
            if _log[0][0] != _choice:
                assert False, ('Look up the option you were handed: `actions[choice]`, with no quotes on `choice`. '
                               + _evs(_r, 'another option ran'))
            if _log[0][1] is not _h:
                assert False, ('Hand over the hero you were handed: `actions[choice](hero)`. '
                               + _evs(_r, 'the action ran on another sheet'))
        elif _h != _after:
            assert False, ('Call the action once, on the hero you were handed: `actions[choice](hero)`. '
                           + _evs(_r, 'the mana came out wrong'))
    else:
        if _ran:
            if _uses('attr:lower'):
                assert False, ('Leave `choice` as it is, with no `.lower()`: the old `act` did nothing for a choice '
                               'with a capital letter, and a refactor keeps what the code did. '
                               + _evs(_r, _did(_r) + ', and the hero changed'))
            assert False, ('Hand back `False` before you call anything: for a choice `actions` does not have, the hero '
                           'must not change. ' + _evs(_r, _did(_r) + ', and the hero changed'))
        if _v is None:
            if _rows:
                assert False, ('Use `return`, not `print`: the test reads what your function hands back. '
                               + _evs(_r))
            assert False, ('Hand back `False` for a choice `actions` does not have: a bare `return`, or no `return`, '
                           'hands back `None`. ' + _evs(_r))
        _t = _kind_msg(_v, False)
        if _t:
            assert False, _t + ' ' + _evs(_r)
        if _v is not False:
            assert False, ('Hand back `False` for a choice `actions` does not have: ask `if choice not in actions:` '
                           'first. ' + _evs(_r))


def _seal_list():
    # (asserts outside every function, asserts inside one)
    _inside = _B.set()
    for _n in _ast.walk(_tree):
        if _tn(_n) == 'FunctionDef':
            for _x in _ast.walk(_n):
                if _x is not _n:
                    _inside.add(_B.id(_x))
    _all = [_n for _n in _ast.walk(_tree) if _tn(_n) == 'Assert']
    return [_a for _a in _all if _B.id(_a) not in _inside], [_a for _a in _all if _B.id(_a) in _inside]


def _calls_to(_node, _target):
    return _B.any(_tn(_x) == 'Call' and _tn(_x.func) == 'Name' and _x.func.id == _target for _x in _ast.walk(_node))


def _about(_a, _target):
    # The seal calls the function, or reads a variable made from a call to it.
    if _calls_to(_a.test, _target):
        return True
    _fed = _B.set()
    for _x in _ast.walk(_tree):
        if _tn(_x) == 'Assign' and _calls_to(_x.value, _target):
            for _t in _x.targets:
                if _tn(_t) == 'Name':
                    _fed.add(_t.id)
    return _B.any(_tn(_y) == 'Name' and _y.id in _fed for _y in _ast.walk(_a.test))


def _says(_a, _t=None):
    # The seal says the answer: the call (or `not` the call), or the call compared with True or False. Seals joined
    # with `and` say it when every part does.
    _t = _a.test if _t is None else _t
    if _tn(_t) == 'BoolOp' and _tn(_t.op) == 'And':
        return _B.all(_says(_a, _x) for _x in _t.values)
    if _tn(_t) == 'UnaryOp' and _tn(_t.op) == 'Not':
        _t = _t.operand
    if _tn(_t) in ('Call', 'Name'):
        return True
    if _tn(_t) == 'Compare' and _B.len(_t.ops) == 1 and _tn(_t.ops[0]) in ('Eq', 'NotEq', 'Is', 'IsNot'):
        return _B.any(_tn(_x) == 'Constant' and _tn(_x.value) == 'bool' for _x in (_t.left, _t.comparators[0]))
    return False


def _seal_keep(_target, _src, _line):
    _d = _defs().get(_target)
    assert _d is not None and _tn(_g.get(_target)) == 'function', (
        'Keep Mar\'tu\'s `' + _target + '` from the starter, made with `def`: the seals test it.')
    _w = _ast.parse(_src).body[0]
    assert _ast.dump(_d) == _ast.dump(_w), ('Put `' + _target + '` back as Mar\'tu wrote it' + _line + '. It is '
                                            'right: the seals test the function, they never change it.')


def _seal_count(_tg, _n):
    _out, _in = _seal_list()
    if not _out and _in:
        assert False, ('Write the seals at the top level, under the comment, not inside a function: a seal inside '
                       'a `def` only runs when that function is called.')
    assert _out, ('Write your seals under the comment: each one is a line that starts with `assert`, calls `' + _tg
                  + '`, and says what it must hand back.')
    assert _B.all(_about(_a, _tg) for _a in _out), ('Make every seal call `' + _tg + '`: one of your asserts never '
                                                     'calls it, so it tests nothing about the function.')
    assert _B.len(_out) >= _n, ('Write ' + _B.str(_n) + ' seals in all: you have ' + _B.str(_B.len(_out))
                                + '. Give each one other numbers.')
    _diff = _B.len(_B.set(_ast.dump(_a.test) for _a in _out))
    assert _diff >= _n, ('Write ' + _B.str(_n) + ' different seals: some of yours are the same line twice, so you '
                         'have ' + _B.str(_diff) + '. Give each one other numbers.')


def _seal_says():
    _bad = [_a for _a in _seal_list()[0] if not _says(_a)]
    if not _bad:
        return
    _signs = [_x for _x in _ast.walk(_bad[0].test) if _tn(_x) == 'Compare'
              and _B.any(_tn(_o) in ('GtE', 'Gt', 'Lt', 'LtE') for _o in _x.ops)]
    if _signs:
        assert False, ('Say the answer in each seal, `True` or `False`: a seal that works the answer out with a sign '
                       'repeats Mar\'tu\'s question, and would repeat its bug too.')
    assert False, 'Say the answer in each seal: compare the call with `True` or `False`, like `== True`.'


def _seal_run(_target, _body):
    # The student's whole program again, in a fresh namespace, with the function's steps swapped for a wrong copy.
    _t = _ast.parse(_source)
    for _n in _t.body:
        if _tn(_n) == 'FunctionDef' and _n.name == _target:
            _n.body = _ast.parse('def _copy_of():\n' + _body).body[0].body
    _ast.fix_missing_locations(_t)
    _code = _B.compile(_t, 'main.py', 'exec')
    _ns = {'__name__': '__main__'}
    _v, _rows, _e = _quiet(lambda: _B.exec(_code, _ns))
    if _e is None:
        return 'through'
    if _tn(_e) == '_Runaway':
        return 'runaway'
    return 'caught'


def _lits(_target):
    # [(the call's numbers, the answer the seal wants)] for seals like `assert cast_ok(9, 9, 8, 8) == True`.
    _out = []
    for _a in _seal_list()[0]:
        _t = _a.test
        _want = True
        if _tn(_t) == 'UnaryOp' and _tn(_t.op) == 'Not':
            _want, _t = False, _t.operand
        if (_tn(_t) == 'Compare' and _B.len(_t.ops) == 1 and _tn(_t.comparators[0]) == 'Constant'
                and _tn(_t.comparators[0].value) == 'bool'):
            _c = _t.comparators[0].value
            _want = _c if _tn(_t.ops[0]) in ('Eq', 'Is') else (not _c)
            _t = _t.left
        if _tn(_t) == 'Call' and _tn(_t.func) == 'Name' and _t.func.id == _target:
            try:
                _args = _B.tuple(_ast.literal_eval(_x) for _x in _t.args)
            except _B.Exception:
                continue
            _out.append((_args, _want))
    return _out
'''.replace("__QUOTES__", repr(QUOTES_RULE))


def _tx_parts():
    """_TX split into its setup lines (imports, _g, _tree, ...) and its helper functions and classes, each with the
    helper names it uses, so a check can carry only the helpers it needs (the unit JSON stays small)."""
    import ast

    tree = ast.parse(_TX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_TX, node)
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_TX_HEAD, _TX_DEFS = _tx_parts()


def check(label, body):
    """(label, code): the _TX setup lines, the helpers this body uses (and the helpers those use), then the body."""
    import re

    need, todo = [], set(re.findall(r"\b_\w+", body))
    while todo:
        name = todo.pop()
        if name in _TX_DEFS and name not in need:
            need.append(name)
            todo |= _TX_DEFS[name][1]
    helpers = [text for name, (text, _) in _TX_DEFS.items() if name in need]
    return (label, "\n".join(_TX_HEAD) + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + body)


# ---------------------------------------------------------------------------------------------
# Row builders. Slips are simulated HERE, at build time, on the row's own data, so a slip's message is attached
# only when that slip really gives a different answer from the table's.
# ---------------------------------------------------------------------------------------------

_FALL_V = "Work this row out by hand first, then follow your function line by line with the same values."
_FALL_H = ("It passes the table, not this test. Make this case yourself: under the table, add a `print(...)` call "
           "that tries what the label says, and Run. Use only the parameters inside the function, never a value "
           "from the table.")


def _same_py(a, b):
    """Build-time twin of the check's _same()."""
    ka, kb = type(a).__name__, type(b).__name__
    if "bool" in (ka, kb):
        return ka == kb and a == b
    if kb in ("int", "float"):
        return ka in ("int", "float") and abs(a - b) < 1e-9
    return ka == kb and a == b


def _simulate(slips, args, kw, want):
    """[(value, message, condition)] for every slip that gives a different answer on these arguments, in order."""
    import copy

    out = []
    for slip in slips:
        fn, message, cond = (tuple(slip) + (None,))[:3]
        try:
            got = fn(*copy.deepcopy(tuple(args)), **copy.deepcopy(dict(kw)))
        except Exception:
            continue
        if got is None or _same_py(got, want):
            continue
        out.append((got, message, cond))
    return out


def _alts_code(alts):
    return "[" + ", ".join(f"({v!r}, {m!r}, {('(lambda: ' + c + ')') if c else 'None'})" for v, m, c in alts) + "]"


def _errs_code(errs):
    return "[" + ", ".join(f"(lambda _e: {cond}, {message!r})" for cond, message in errs) + "]"


def _vr_code(rules):
    return "[" + ", ".join(f"(lambda _v: {cond}, {message!r})" for cond, message in rules) + "]"


def _head(fn, where, *, ok=(), marks="", typed=(), kind=None, keepmsg="", none="", glob=(), fall=None, var=False,
          want=None, seen=()):
    """The globals every check body sets before it calls a helper. want: the row's answer (the evidence bracket's
    "not Z" is shown only when the value handed back differs from it); seen: the visible rows' answers (a list typed
    in as the only `return` is hard-coding, apply_to_all)."""
    return (
        f"_FN = {fn!r}\n"
        f"_OK = {list(ok)!r}\n"
        f"_MARKS = {marks!r}\n"
        f"_TYPED = {list(typed)!r}\n"
        f"_KIND = {dict(kind or {})!r}\n"
        f"_KEEPMSG = {keepmsg!r}\n"
        f"_NONE = {none!r}\n"
        f"_GLOB = {list(glob)!r}\n"
        f"_ROW = {tuple(where)!r}\n"
        f"_FALL = {(fall or (_FALL_V if where[0] == 'v' else _FALL_H))!r}\n"
        f"_VAR = {var!r}\n"
        f"_WANT = {want!r}\n"
        f"_SEEN = {list(seen)!r}\n"
    )


def _check_name(where):
    if where[0] == "v":
        return f"row {where[1]}: {where[2].replace('`', '')}"
    return f"hidden: {where[1].replace('`', '')}"


def row(fn, params, args, want, where, *, kw=None, ok=(), marks="", typed=(), errs=(), slips=(), vrules=(),
        keep=True, kind=None, keepmsg="", none="", glob=(), fall=None, pre="", after_run="", post=""):
    """One test-table row as a check. where = ("v", n, "`call`", "hand back `x`", "`x`") for a visible row (the
    last two are the want in words and the want alone; a row whose want is also an action has "" last), or ("h",
    "label") for a hidden test. errs = [(condition on `_e`, message)]; vrules = [(condition on `_v`, message)];
    slips = [(python function, message[, check condition])], simulated now."""
    kw = dict(kw or {})
    alts = _simulate(slips, args, kw, want)
    body = (
        _head(fn, where, ok=ok, marks=marks, typed=typed, kind=kind, keepmsg=keepmsg, none=none, glob=glob, fall=fall,
              want=want)
        + pre
        + f"_f = _need({fn!r}, {list(params)!r})\n"
        + f"_r = _run(_f, {tuple(args)!r}, {kw!r})\n"
        + after_run
        + f"_verdict(_r, {want!r}, {_errs_code(errs)}, {_alts_code(alts)}, {keep!r}, {_vr_code(vrules)})\n"
        + post
    )
    return check(_check_name(where), body)


def lines_of(code):
    """Assemble lines: the code's non-blank lines, comments dropped."""
    return [line for line in code.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def _call_text(fn, args, kw=None):
    parts = [repr(a) if not isinstance(a, str) else '"' + a + '"' for a in args]
    parts += [f'{k}="{v}"' for k, v in (kw or {}).items()]
    return f"`{fn}({', '.join(parts)})`"


def _lit_text(value):
    """A row's answer in backticks, as the evidence bracket shows it."""
    if isinstance(value, str):
        return f'`"{value}"`'
    if isinstance(value, list):
        return "`[" + ", ".join(f"'{x}'" for x in value) + "]`"
    return f"`{value}`"


def _vis(n, call, value):
    """A visible value row's `where`: ("v", n, "`call`", "hand back `x`", "`x`")."""
    return ("v", n, call, "hand back " + _lit_text(value), _lit_text(value))


# =============================================================================================
# UNIT (repeated in every part file of code-challenges; copied from u08a, the first part, exactly)
# =============================================================================================

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

# New terms only: earlier units define assert, default value, keyword argument, function as a value, test table,
# hidden test, edge case, hard-coded, KeyError and the rest.
GLOSSARY = [
    dict(
        term="clamp",
        aliases=["clamps", "clamped", "clamping"],
        plain=(
            "Keep a number inside its limits. A number past the top becomes the top, and a number below the bottom "
            "becomes the bottom."
        ),
        example="if mana > top:\n    mana = top",
    ),
    dict(
        term="lookup",
        aliases=["lookups", "look up", "dictionary lookup"],
        plain=(
            "Finding a value in a dictionary by its key, like `lines[choice]`. One lookup can do the work of a long "
            "`if` / `elif` chain."
        ),
        example='moods = {"fog": "Grey."}\nprint(moods["fog"])',
    ),
    dict(
        term="AssertionError",
        aliases=["assertion error"],
        plain=(
            "The error Python gives when an `assert` line finds its question `False`. Python stops on that line: "
            "the seal caught something."
        ),
        example="assert 3 > 5   # AssertionError",
    ),
]


# =============================================================================================
# T-F-1 "A Bar for Any Gauge": make_bar(current, maximum, full="█", empty="░") (core; prerequisite card 6B-08)
# =============================================================================================

BAR_DEF = 'def make_bar(current, maximum, full="█", empty="░"):\n'
BAR_HEAD = "# Trial: a bar for any gauge.\n" + BAR_DEF
BAR_TAIL = (
    "\n\n# Visible tests. They should show\n"
    "# ███░░, then ▮▮▯▯, then █--.\n"
    "# (With only pass, each shows None.)\n"
    "print(make_bar(3, 5))\n"
    'print(make_bar(2, 4, "▮", "▯"))\n'
    'print(make_bar(1, 3, empty="-"))\n'
)
# `missing` counts the empty marks: the part of the bar that is not full.
BAR_BODY = (
    "    filled = full * current\n"
    "    missing = maximum - current\n"
    "    return filled + empty * missing\n"
)


def _bar(body="    pass\n", tail=BAR_TAIL, head=BAR_HEAD):
    return head + body + tail


BAR_STARTER = _bar()
BAR_SOLUTION = _bar(BAR_BODY)
BAR_MARKS = "█░▮▯-#.▓"
BAR_TYPED = ["███░░", "▮▮▯▯", "█--", "▮", "▯", "-", 3, 5]
BAR_KIND = {
    "list": "Hand back text, not a list: `full * current` already makes a piece of text.",
    "int": "Hand back the bar itself, the marks, not a number.",
    "bool": "Hand back the bar itself, the marks, not `True` or `False`.",
}
BAR_BRACKETS = ("Put brackets around the count: `empty * (maximum - current)`. Without them, Python works out "
                "`empty * maximum` first, then tries to take a number away from text.")
BAR_ERRS = [
    ("'unsupported operand' in _B.str(_e) and \"'str' and 'int'\" in _B.str(_e)", BAR_BRACKETS),
    ("'can only concatenate str' in _B.str(_e)",
     "Use `*` to repeat a mark: `full * current` makes `current` marks. `+` only glues text to text."),
    ("\"can't multiply sequence by non-int of type 'str'\" in _B.str(_e)",
     "Multiply a mark by a number, like `full * current`: both sides of your `*` are text."),
]
BAR_VRULES = [
    ("_tn(_v) == 'str' and ('[' in _v or 'Mana' in _v)",
     "Hand back only the marks: no `Mana [` label, no brackets and no numbers. The caller can add those."),
    ("_tn(_v) == 'str' and (' ' in _v or '\\n' in _v)",
     "Hand back only the marks, with no spaces or new lines: glue the full part and the empty part straight "
     "together with `+`."),
]


BAR_COUNT = ("Count the marks: `current` full ones, then `maximum - current` empty ones, with no `+ 1` or `- 1`. "
             "The whole bar is `maximum` marks long.")


def _bar_of(c, m, f="█", e="░"):
    return f * c + e * (m - c)


def _slip(fn):
    """A bar slip as a function of the call's own values (defaults included)."""
    def run(current, maximum, full="█", empty="░"):
        return fn(current, maximum, full, empty)
    return run


BAR_SLIPS = [
    (_slip(lambda c, m, f, e: "full" * c + "empty" * (m - c)),
     "Take the quotes off `full` and `empty` to use the parameters. " + QUOTES_RULE),
    (_slip(lambda c, m, f, e: "█" * c + "░" * (m - c)),
     "Use the parameters `full` and `empty`, not typed marks: this row hands over its own marks."),
    (_slip(lambda c, m, f, e: e * c + f * (m - c)),
     "Full marks come first: `full * current`, then the empty ones."),
    (_slip(lambda c, m, f, e: f * m + e * (c - m)),
     "`current` is how many marks are full, and `maximum` is how long the whole bar is. Your bar uses them the "
     "other way round."),
    (_slip(lambda c, m, f, e: f * c + e * m),
     "Take the full part away: the bar is `maximum` marks long in all, so the empty part is `maximum - current` "
     "marks."),
    (_slip(lambda c, m, f, e: f * c),
     "Add the empty marks after the full ones: the whole bar is `maximum` marks long."),
    (_slip(lambda c, m, f, e: f * c + e * (m - c - 1)), BAR_COUNT),
    (_slip(lambda c, m, f, e: f * (c + 1) + e * (m - c - 1)), BAR_COUNT),
    (_slip(lambda c, m, f, e: f * c + e * (m - c + 1)), BAR_COUNT),
]


def _bar_row(args, where, kw=None, *, slips=BAR_SLIPS, typed=BAR_TYPED, fall=None, want=None):
    kw = dict(kw or {})
    if want is None:
        want = _bar_of(*args, **{"f" if k == "full" else "e": v for k, v in kw.items()})
    return row("make_bar", ["current", "maximum", "full", "empty"], args, want, where, kw=kw, marks=BAR_MARKS,
               typed=typed, errs=BAR_ERRS, slips=slips, vrules=BAR_VRULES, kind=BAR_KIND, fall=fall)


def _vis_bar(n, args, kw=None, **extra):
    want = _bar_of(*args, **{"f" if k == "full" else "e": v for k, v in (kw or {}).items()})
    if "want" in extra:
        want = extra.pop("want")
    return _bar_row(args, _vis(n, _call_text("make_bar", args, kw), want), kw, want=want, **extra)


BAR_SIG = check("the def line keeps its default marks", "_FN = 'make_bar'\n_bar_sig()\n")

MAKE_BAR = dict(
    kind="challenge",
    id="make-bar",
    title="A Bar for Any Gauge",
    level="core",
    optional=True,
    minutes=7,
    support="light",
    tracer=True,
    summary="Write `make_bar`: full marks, then empty marks, with marks a call can hand over or leave to the "
            "defaults.",
    martu=(
        "Gearshift wants one function (a recipe) for every gauge: mana, fuel, glug. Write `make_bar`. It hands "
        "back `current` full marks, then empty marks, so the whole bar is `maximum` marks long.\n"
        "`full` and `empty` have [[default value|default values]]. A call that hands over no marks gets `█` and "
        "`░`. A call can hand over its own marks, in order or [[keyword argument|by name]].\n"
        "```text\nmake_bar(3, 5)\n  → \"███░░\"\nmake_bar(2, 4, \"▮\", \"▯\")\n  → \"▮▮▯▯\"\n"
        "make_bar(1, 3, empty=\"-\")\n  → \"█--\"\n```\n"
        "Run it and compare with the table, yes?"
    ),
    names=["make_bar", "current", "maximum", "full", "empty"],
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="table",
            text="Write `make_bar` so every row of the table passes.",
            dictated=False,
            hints=[
                "Each row hands over two numbers, and sometimes marks. The full marks come first, `current` of "
                "them. The rest of the bar, `maximum - current` marks, is empty.",
                "Text times a number repeats it: `\"*\" * 3` is `\"***\"`, and `+` glues two pieces of text. Use "
                "the parameters `full` and `empty`, never typed marks: a row can hand over its own.",
                "Write `filled = full * current`, then `missing = maximum - current`, then `return filled + empty "
                "* missing`.",
            ],
            checks=[
                BAR_SIG,
                _vis_bar(1, (3, 5)),
                _vis_bar(2, (2, 4, "▮", "▯")),
                _vis_bar(3, (1, 3), {"empty": "-"}),
            ],
            pass_line="Gearshift: Visor dims. One function, three gauges. Math checks out.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: full bars, empty bars and other marks.",
            dictated=False,
            hints=[
                "The hidden tests try the edges: every mark full, no mark full, and a bar of length 0. They hand "
                "over other marks too. Use only the parameters inside the function.",
                "`\"#\" * 0` is empty text, `\"\"`, so a bar with no full marks still works. A typed "
                "`\"███░░\"` fits one row only.",
                "Keep `return filled + empty * missing`: it works for any numbers and any marks.",
            ],
            checks=[
                _bar_row((6, 6), ("h", "a full bar")),
                _bar_row((0, 4), ("h", "an empty bar")),
                _bar_row((2, 5), ("h", "other marks, both by name"), {"full": "#", "empty": "."}),
                _bar_row((3, 4), ("h", "only the full mark, by name"), {"full": "▓"}),
                _bar_row((0, 0), ("h", "a bar of length 0")),
                _bar_row((13, 20), ("h", "a long bar")),
            ],
            pass_line="Mar'tu: Any gauge, any marks. Lucky's glug bar too, yes?",
        ),
    ],
    solution=BAR_SOLUTION,
    assemble=dict(
        lines=lines_of(BAR_DEF + BAR_BODY),
        distractors=[
            "    missing = maximum * current",
            '    filled = "█" * current',
            "    missing = current - maximum",
        ],
    ),
    another_way=[
        dict(angle="picture", label="Two pieces, glued", text=(
            "```text\nmake_bar(3, 5)\n\nfull * 3   → ███\nempty * 2  → ░░\n            (5 - 3)\nglued      → "
            "███░░\n```\nTwo pieces of text, glued with `+`. Together they are `maximum` marks long.")),
        dict(angle="step-by-step", text=(
            "1. Make the full part: `full` times `current`.\n2. Work out how many are left: `maximum - current`.\n"
            "3. Make the empty part: `empty` times that number.\n4. Glue them, and hand back the bar.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`get_mana_bar(caster)` built `\"█\" * caster[\"mana\"]`, then the `░` part. The marks were typed in. "
            "Here they come in as parameters, with the same marks as defaults, so one function draws any gauge.")),
    ],
    predict=dict(
        q="Before you write it: what do these two lines print?",
        code=(
            'def tag(word, mark="*"):\n'
            "    return mark + word + mark\n"
            "\n\n"
            'print(tag("glug"))\n'
            'print(tag("glug", mark="!"))\n'
        ),
        choices=["*glug*\n*glug*", "*glug*\n!glug!", "glug\n!glug!"],
        answer=1,
        explain=(
            "The first call hands over no `mark`, so the default `\"*\"` is used. The second hands over `mark=\"!\"` "
            "by name, and a value handed over wins. `make_bar` works the same way."
        ),
    ),
    pair_talk="Read row 3 to your partner: which mark does it hand over, and which one does it leave to the "
              "default?",
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        snippet='filled = "█" * caster["mana"]',
        why=(
            "You built this bar in `get_mana_bar`, with the marks typed in. `make_bar` is the same bar with the "
            "marks handed over, so one function draws Lucky's mana, Gearshift's fuel and the glug canteen."
        ),
    ),
    takeaway="Text times a number repeats it. Use the parameters, defaults included, and never typed marks.",
    wrong_answers=[
        dict(why="the starter (pass)", code=BAR_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="row 1's answer typed (return \"███░░\")", code=_bar('    return "███░░"\n'), fails_at=1,
             message_contains='`"███░░"` typed in it'),
        dict(why="the whole table typed behind ifs (passes every visible row; the hidden tests catch it)",
             code=_bar('    if current == 3:\n        return "███░░"\n    if current == 2:\n'
                       '        return "▮▮▯▯"\n    return "█--"\n'), fails_at=2, message_contains="typed in it"),
        dict(why="the campaign's typed marks (full and empty never used)",
             code=_bar('    return "█" * current + "░" * (maximum - current)\n'), fails_at=1,
             message_contains="not typed marks"),
        dict(why="no brackets round maximum - current: the bottom prints stop with Python's TypeError",
             code=_bar("    return full * current + empty * maximum - current\n"), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="no brackets round maximum - current, the bottom prints gone: Mar'tu's message",
             code=_bar("    return full * current + empty * maximum - current\n", tail=""), fails_at=1,
             message_contains="Put brackets around the count"),
        dict(why="the empty part not shortened (empty * maximum)",
             code=_bar("    return full * current + empty * maximum\n"), fails_at=1,
             message_contains="Take the full part away"),
        dict(why="print instead of return", code=_bar("    print(full * current + empty * (maximum - current))\n"),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="the default marks taken off the def line: the bottom prints stop with Python's TypeError",
             code=_bar(BAR_BODY, head=BAR_HEAD.replace('full="█", empty="░"', "full, empty")), fails_at=0,
             message_contains="missing 2 required positional arguments"),
        dict(why="the default marks taken off, the bottom prints gone: Mar'tu's message",
             code=_bar(BAR_BODY, head=BAR_HEAD.replace('full="█", empty="░"', "full, empty"), tail=""), fails_at=1,
             message_contains="Keep the default marks on the `def` line"),
        dict(why="the default marks swapped", code=_bar(BAR_BODY, head=BAR_HEAD.replace(
            'full="█", empty="░"', 'full="░", empty="█"')), fails_at=1, message_contains="Swap the default marks back"),
        dict(why="the parameters quoted (\"full\" * current)",
             code=_bar('    return "full" * current + "empty" * (maximum - current)\n'), fails_at=1,
             message_contains="Take the quotes off `full`"),
        dict(why="the campaign's Mana [ ] label kept",
             code=_bar('    return "Mana [" + full * current + empty * (maximum - current) + "]"\n'), fails_at=1,
             message_contains="no `Mana [` label"),
        dict(why="the marks the other way round (empty first)",
             code=_bar("    return empty * current + full * (maximum - current)\n"), fails_at=1,
             message_contains="Full marks come first"),
        dict(why="current and maximum used the other way round",
             code=_bar("    return full * maximum + empty * (current - maximum)\n"), fails_at=1,
             message_contains="the other way round"),
        dict(why="the parameters in the other order (the table read backwards)",
             code=_bar(BAR_BODY, head=BAR_HEAD.replace("(current, maximum,", "(maximum, current,")), fails_at=1,
             message_contains="in the order of the first line"),
        dict(why="a list of marks, not text", code=_bar("    return [full] * current + [empty] * (maximum - current)\n"),
             fails_at=1, message_contains="not a list"),
        dict(why="+ for * (full + current), the prints gone", code=_bar("    return full + current\n", tail=""),
             fails_at=1, message_contains="Use `*` to repeat a mark"),
        dict(why="only the full part", code=_bar("    return full * current\n"), fails_at=1,
             message_contains="Add the empty marks"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Functions", trial="T-F-1", opens="after Unit 7",
             ceiling="Units 1-7 + card 6B-08", prereq="6B-08 defaults-and-names (u07c, pool): recap in the Learn "
             "pane and the predict", skills="repeat-string,default-arg,keyword-arg,return-value,read-test-table",
             solo="false", dictates="", foreign_names="tag,word,mark",
             par="a full bar (6, 6); an empty bar (0, 4); other marks by name (2, 5, full=#, empty=.); only the "
                 "full mark by name (3, 4, full=▓); a bar of length 0; a long bar (13, 20)") + "\n"
        "T-F-1. The spec gives the signature only; Mar'tu states what the bar is (current full marks, then "
        "maximum - current empty ones, no label), the campaign's get_mana_bar without its `Mana [` frame. The "
        "starter keeps the spec's def line whole (u08a's ruling on fixed signatures). Row 2 hands its marks over "
        "by position and row 3 one mark by name, so the 6B-08 card's two ideas (a default, a keyword argument) are "
        "each tested; typed `█`/`░` pass row 1 and fail row 2 with their own message. The class's slips here: "
        "typed values from the table (A-06/A-07), the campaign's precedence slip `\"░\" * a - b` (6B-07, 6B-10), "
        "quoted parameters (A-02), print for return. A crash inside make_bar also crashes the starter's bottom "
        "prints, so it is Python's own error first (the explainer's row); twins with the prints gone prove "
        "Mar'tu's messages. A loop that builds the bar mark by mark passes too. Teacher ruling (Nov 14): the "
        "solution's `used` is now `missing` (it counts the empty marks) in the solution, partials, hints, assemble "
        "and wrong answers; tracer=True (step through the two pieces being glued). The starter's visible tests "
        "sit under \"# Visible tests. They should show\" and \"# (With only pass, each shows None.)\" (u08a/b's "
        "form). Predict answer index 1 (the unit mixes the right answer's place). Show-rung copy-test: CP1's rung "
        "(`filled = ...`, `missing = ...`, `return filled + empty * missing`) pasted in place of `pass` is the "
        "solution: no crash, every checkpoint passes; CP2's rung keeps it. No edge sign in this trial."
    ),
)


# =============================================================================================
# T-F-1a "A Bar That Fits Its Box": make_bar(...) clamps current into 0..maximum (advanced, variant_of make-bar)
# =============================================================================================

CLAMP_HEAD = "# Trial: a bar that fits its box.\n" + BAR_DEF
CLAMP_TAIL = (
    "\n\n# Visible tests. They should show\n"
    "# ███░░, then █████, then ░░░░.\n"
    "# (With only pass, each shows None.)\n"
    "print(make_bar(3, 5))\n"
    "print(make_bar(7, 5))\n"
    "print(make_bar(-2, 4))\n"
)
CLAMP_TOP = "    if current > maximum:\n        current = maximum\n"
CLAMP_BOTTOM = "    if current < 0:\n        current = 0\n"
CLAMP_BODY = CLAMP_TOP + CLAMP_BOTTOM + BAR_BODY


def _clamp(body="    pass\n", tail=CLAMP_TAIL):
    return CLAMP_HEAD + body + tail


CLAMP_STARTER = _clamp()
CLAMP_SOLUTION = _clamp(CLAMP_BODY)
CLAMP_TYPED = ["███░░", "█████", "░░░░", 5, 7, 4]


def _fit(c, m):
    return max(0, min(c, m))


def _cslip(fn):
    def run(current, maximum, full="█", empty="░"):
        return fn(current, maximum, full, empty)
    return run


CLAMP_SLIPS = [
    (_cslip(lambda c, m, f, e: _bar_of(max(max(c, m), 0), m, f, e)),
     "To keep `current` at most `maximum`, use `min(current, maximum)`: `max()` hands back the bigger number.",
     "_uses('call:max')"),
    (_cslip(lambda c, m, f, e: _bar_of(min(c, m, 0), m, f, e)),
     "To keep `current` at least 0, use `max(current, 0)`: `min()` hands back the smaller number.",
     "_uses('call:min')"),
    (_cslip(lambda c, m, f, e: f * max(c, 0) + e * (max(m, c) - max(c, 0))),
     "Change `current`, not `maximum`: the box stays the same size, so the bar stays `maximum` marks long.",
     "_sets('maximum')"),
    (_cslip(lambda c, m, f, e: _bar_of(max(m - 1 if c > m else c, 0), m, f, e)),
     "Clamp to `maximum` itself: a full bar has `maximum` full marks. `maximum - 1` is a list's last position, "
     "not a bar's length."),
    (_cslip(lambda c, m, f, e: "" if c > m else _bar_of(max(c, 0), m, f, e)),
     "Clamp, don't refuse: a bar with too much mana is a full bar, `maximum` full marks."),
    (_cslip(lambda c, m, f, e: "" if c < 0 else _bar_of(min(c, m), m, f, e)),
     "Clamp, don't drop the bar: below 0 counts as 0, so the bar is all empty marks, `maximum` of them."),
    (_cslip(lambda c, m, f, e: _bar_of(_fit(c, m), m, "█", "░")),
     "Use the parameters `full` and `empty`, not typed marks: this test hands over its own marks."),
]
CLAMP_TOO_MUCH = ("Clamp `current` before you build the bar: when it is more than `maximum`, use `maximum` "
                  "instead.")
CLAMP_TOO_LOW = "Clamp `current` before you build the bar: when it is below 0, use 0 instead."


def _clamp_row(args, where, kw=None, fall=None):
    kw = dict(kw or {})
    marks = {"f" if k == "full" else "e": v for k, v in kw.items()}
    if len(args) == 4:
        marks = {"f": args[2], "e": args[3]}
    want = _bar_of(_fit(args[0], args[1]), args[1], **marks)
    return _bar_row(args, where, kw, slips=CLAMP_SLIPS, typed=CLAMP_TYPED, fall=fall, want=want)


def _vis_clamp(n, args, fall=None):
    want = _bar_of(_fit(args[0], args[1]), args[1])
    return _clamp_row(args, _vis(n, _call_text("make_bar", args), want), fall=fall)


MAKE_BAR_CLAMPED = dict(
    kind="challenge",
    id="make-bar-clamped",
    title="A Bar That Fits Its Box",
    level="advanced",
    variant_of="make-bar",
    optional=True,
    minutes=9,
    support="light",
    summary="The advanced twin of A Bar for Any Gauge: clamp `current` into 0 to `maximum`, so the bar always fits "
            "its box.",
    martu=(
        "The advanced bar trial. Lucky drank three canteens of glug, and his mana went past its maximum. "
        "Gearshift's gauge drew a bar too long for its box.\n"
        "Write `make_bar` again, so a bar is always `maximum` marks long. [[clamp|Clamp]] `current` first: more "
        "than `maximum` counts as `maximum`, and below 0 counts as 0.\n"
        "```text\nmake_bar(3, 5)  → \"███░░\"\nmake_bar(7, 5)  → \"█████\"\nmake_bar(-2, 4) → \"░░░░\"\n```\n"
        "Then my hidden tests try the edges, yes?"
    ),
    names=["make_bar", "current", "maximum", "full", "empty"],
    starter=CLAMP_STARTER,
    checkpoints=[
        dict(
            id="in-the-box",
            text="Write `make_bar` so row 1 of the table passes: a bar inside its box.",
            dictated=False,
            hints=[
                "Row 1 is the plain bar from the core trial: 3 full marks, then 2 empty ones.",
                "`\"*\" * 3` is `\"***\"`. Use the parameters `full` and `empty`, so a call can hand over its own "
                "marks.",
                "Write `filled = full * current`, then `missing = maximum - current`, then `return filled + empty "
                "* missing`.",
            ],
            checks=[BAR_SIG, _vis_clamp(1, (3, 5))],
            pass_line="Gearshift: Plain bar. Holding.",
        ),
        dict(
            id="too-much",
            text="Make row 2 pass: more than `maximum` counts as `maximum`.",
            dictated=False,
            hints=[
                "Row 2 has 7 mana in a box of 5. The bar must still be 5 marks long, all of them full.",
                "Change the number before you build the bar. With other names: `if count > size:` then "
                "`count = size` on the next line, indented.",
                "Write `current = maximum` inside `if current > maximum:`, at the top of the function, before the "
                "bar is built.",
            ],
            checks=[_vis_clamp(2, (7, 5), fall=CLAMP_TOO_MUCH)],
            pass_line="Lucky: Full is full. I'll take it.",
        ),
        dict(
            id="below-zero",
            text="Make row 3 pass: below 0 counts as 0.",
            dictated=False,
            hints=[
                "Row 3 has -2 mana. A bar can't have fewer than 0 full marks, so this one is all empty.",
                "`\"█\" * -2` is empty text, but `\"░\" * 6` is 6 marks, so the bar comes out too long. Change "
                "`current` before you build it.",
                "Write `current = 0` inside `if current < 0:`, next to the first clamp.",
            ],
            checks=[_vis_clamp(3, (-2, 4), fall=CLAMP_TOO_LOW)],
            pass_line="Bomb Shell: Empty. Still fits.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: exactly full, exactly 0, other marks, and far past both edges.",
            dictated=False,
            hints=[
                "The hidden tests sit on the edges: exactly `maximum`, exactly 0, and far past both. Some hand "
                "over other marks.",
                "A clamp changes only `current`. `maximum` stays the length of the box. `min(a, b)` hands back the "
                "smaller number, and `max(a, b)` the bigger one.",
                "Keep both clamps at the top, then `return filled + empty * missing`.",
            ],
            checks=[
                _clamp_row((5, 5), ("h", "exactly full")),
                _clamp_row((0, 3), ("h", "exactly 0")),
                _clamp_row((12, 3, "▮", "▯"), ("h", "far too much, with other marks")),
                _clamp_row((-9, 2), ("h", "far below 0")),
                _clamp_row((4, 2), ("h", "too much, the empty mark by name"), {"empty": "-"}),
                _clamp_row((4, 5), ("h", "one short of full")),
            ],
            pass_line="Mar'tu: However much glug Lucky drinks, the bar fits its box, yes?",
        ),
    ],
    solution=CLAMP_SOLUTION,
    partials=[_clamp(BAR_BODY), _clamp(CLAMP_TOP + BAR_BODY)],
    assemble=dict(
        lines=lines_of(BAR_DEF + CLAMP_BODY),
        distractors=["        maximum = current", "        current = maximum - 1", '        return ""'],
    ),
    another_way=[
        dict(angle="picture", label="A number line with two walls", text=(
            "```text\n -2   0         5   7\n  ·   |█████████|   ·\n  └─→ 0     5 ←─┘\n```\nPast a wall? Move "
            "back to it. Then build the bar as before.")),
        dict(angle="step-by-step", text=(
            "1. Too much? `current = maximum`.\n2. Below 0? `current = 0`.\n3. Now `current` fits: build the bar "
            "from it, the same as the core trial.")),
        dict(angle="in Tor", label="Gearshift's gauge", text=(
            "Gearshift's starlode gauge has a glass box five marks wide. Pour in more, and the box is just full. "
            "Drain it past empty, and the box is just empty. The glass never stretches.")),
        dict(angle="shorter", text="`current = min(current, maximum)`, then `current = max(current, 0)`."),
    ],
    predict=dict(
        q="Before you write the clamp: what does this line print?",
        code='print("█" * -2 + "░" * 6)\n',
        choices=["░░░░", "██░░░░░░", "░░░░░░"],
        answer=2,
        explain=(
            "Text times a negative number is empty text, with no error. So with `current` at -2, the empty part "
            "is 6 marks, and the bar is too long. That is why the clamp comes first."
        ),
    ),
    pair_talk="Tell your partner what `\"█\" * -2` gives, and why row 3's bar would be too long without a clamp.",
    campaign_link=dict(
        module=MODULE,
        part="mana-bars",
        why=(
            "`get_mana_bar` trusted the sheet: mana past `max_mana` would have drawn a bar too long for the party "
            "panel. A clamp keeps any gauge inside its box."
        ),
    ),
    takeaway="Clamp first, then build: past the top becomes the top, below 0 becomes 0, and the box never stretches.",
    wrong_answers=[
        dict(why="the starter (pass)", code=CLAMP_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the core solution, no clamp at all (the partial)", code=_clamp(BAR_BODY), fails_at=2,
             message_contains="more than `maximum`, use `maximum`"),
        dict(why="the top clamp only (the empty case forgotten)", code=_clamp(CLAMP_TOP + BAR_BODY), fails_at=3,
             message_contains="below 0, use 0"),
        dict(why="clamped to maximum - 1 (a list's last position)",
             code=_clamp("    if current > maximum:\n        current = maximum - 1\n" + CLAMP_BOTTOM + BAR_BODY),
             fails_at=2, message_contains="`maximum` itself"),
        dict(why="maximum changed, not current",
             code=_clamp("    if current > maximum:\n        maximum = current\n" + CLAMP_BOTTOM + BAR_BODY),
             fails_at=2, message_contains="not `maximum`"),
        dict(why="refuses instead of clamping (too much -> empty text)",
             code=_clamp('    if current > maximum:\n        return ""\n' + CLAMP_BOTTOM + BAR_BODY), fails_at=2,
             message_contains="don't refuse"),
        dict(why="drops the bar below 0 (empty text)",
             code=_clamp(CLAMP_TOP + '    if current < 0:\n        return ""\n' + BAR_BODY), fails_at=3,
             message_contains="don't drop the bar"),
        dict(why="max() where min() belongs (the table read backwards)",
             code=_clamp("    current = max(current, maximum)\n" + CLAMP_BOTTOM + BAR_BODY), fails_at=1,
             message_contains="`max()` hands back the bigger"),
        dict(why="min() where max() belongs",
             code=_clamp("    current = min(current, maximum)\n    current = min(current, 0)\n" + BAR_BODY),
             fails_at=1, message_contains="`min()` hands back the smaller"),
        dict(why="the clamp after the bar is built (Python runs from the top down)",
             code=_clamp(BAR_BODY.replace("    return filled + empty * missing\n", "") + CLAMP_TOP + CLAMP_BOTTOM
                         + "    return filled + empty * missing\n"), fails_at=2,
             message_contains="before you build the bar"),
        dict(why="row 2's maximum typed in the clamp (passes the table; a hidden box of 3 catches it)",
             code=_clamp("    if current > maximum:\n        current = 5\n" + CLAMP_BOTTOM + BAR_BODY), fails_at=4,
             message_contains="`5` typed in it"),
        dict(why="print instead of return",
             code=_clamp(CLAMP_TOP + CLAMP_BOTTOM + "    print(full * current + empty * (maximum - current))\n"),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="row 1's answer typed", code=_clamp('    return "███░░"\n'), fails_at=2,
             message_contains='`"███░░"` typed in it'),
        dict(why="typed marks (the hidden other-marks test catches it)",
             code=_clamp(CLAMP_TOP + CLAMP_BOTTOM + '    return "█" * current + "░" * (maximum - current)\n'),
             fails_at=4, message_contains="not typed marks"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Functions (advanced)", trial="T-F-1a", variant_of="make-bar",
             opens="after Unit 7", ceiling="Units 1-7 + card 6B-08", prereq="6B-08 defaults-and-names",
             skills="clamp,boundary,if-guard,repeat-string,return-value", solo="false", dictates="",
             foreign_names="count,size",
             par="exactly full (5, 5); exactly 0 (0, 3); far too much with other marks (12, 3); far below 0 (-9, 2); "
                 "too much, empty by name (4, 2); one short of full (4, 5)") + "\n"
        "T-F-1a, variant_of make-bar (the spec: 'Clamp current into 0..maximum'). One checkpoint per rule, so the "
        "partials stage it: the core bar (passes row 1, fails row 2), the top clamp (fails row 3, the empty case). "
        "Row 3's negative count is a minus sign on a number (Unit 4's op:USub), allowed at this unlock point. "
        "`\"█\" * -2` is empty text with no error, so a missing bottom clamp is a quiet bug: the predict shows it. "
        "`min()` / `max()` (Unit 4) pass as well as two `if`s; using them the wrong way round is the table read "
        "backwards and gets its own message. The hidden 'box of 3' catches a typed 5 in the clamp. The hidden "
        "exact cases (exactly full, exactly 0, one short of full) sit on the edges, the boundary habit of this "
        "unit. `missing` for `used`, as in make-bar. Predict answer index 2. Show-rung copy-test: CP1's rung in "
        "place of `pass` is partial 1 (no crash; row 2 needs the top clamp); CP2's on top is partial 2 (no crash; "
        "row 3 needs the bottom clamp); CP3's on top is the solution; CP4's keeps it. Sign rule: neither clamp is "
        "an edge question (`>` or `>=` at the top, `<` or `<=` at 0, give the same bar, since the clamp sets the "
        "number it was compared with), so each rung keeps its one sign."
    ),
)


# =============================================================================================
# T-F-2 "One Spell for Everyone": apply_to_all(heroes, effect) -> a list of the names affected (core)
# =============================================================================================

FX_OK = ["Oogrish", "Gearshift", "Bomb Shell", "Lucky", "Pell", "Brakka", "Moss", "Glug", "Ivo", "Ash", "Moth",
         "Bree", "Tinplate"]
FX_TYPED = ["Oogrish", "Lucky", "Gearshift"]
FX_SEEN = [["Oogrish", "Lucky"], []]   # the visible rows' answers (core)
IF_SEEN = [["Oogrish"], []]            # the visible rows' answers (advanced)
FX_RESET = ("Make the empty list once, before the loop: your list starts again for each hero, so only the last "
            "name is left.")
VAR_ALL = ("Keep only the heroes the effect worked on: ask `if effect(hero):`, and append the name only then.")
VAR_INV = "Keep a name when the effect hands back `True`, not `False`."
VAR_QUOTES = ("Compare with `True` without quotes, or just write `if effect(hero):`. `\"True\"` in quotes is text, "
              "and the effect hands back `True`, not text.")
VAR_NONE_KEPT = "Your function kept no names. Append the name when `effect(hero)` hands back `True`."
VAR_SHEET = ("Keep a name when `effect(hero)` hands back `True`, even if the sheet stays the same. This effect only "
             "answers and changes nothing, so watching the sheet misses it.")
VAR_MANA = ("Ask the effect, not the sheet: `if effect(hero):`. Each effect has its own rule, so reading "
            "`hero[\"mana\"]` yourself only fits one of them.")


def _effect_lines(action):
    kind, _, n = action.partition(":")
    if kind == "add":
        return [f"hero['mana'] = hero['mana'] + {n}"]
    if kind == "set":
        return [f"hero['mana'] = {n}"]
    if kind == "none":
        return ["return None"]
    if kind == "top":
        return [f"if hero['mana'] < {n}:", f"    hero['mana'] = {n}", "    return True", "return False"]
    if kind == "wake":
        return ["if hero['mana'] == 0:", "    hero['mana'] = 5", "    return True", "return False"]
    if kind == "yes":
        return ["hero['mana'] = hero['mana'] + 1", "return True"]
    if kind == "no":
        return ["return False"]
    if kind == "ask":
        return [f"return hero['mana'] >= {n}"]
    raise ValueError(action)


def _effect_py(action, hero):
    """Build-time twin of the recorder's action: changes `hero`, returns what the effect returns."""
    kind, _, n = action.partition(":")
    if kind == "add":
        hero["mana"] = hero["mana"] + int(n)
        return None
    if kind == "set":
        hero["mana"] = int(n)
        return None
    if kind == "none":
        return None
    if kind == "top":
        if hero["mana"] < int(n):
            hero["mana"] = int(n)
            return True
        return False
    if kind == "wake":
        if hero["mana"] == 0:
            hero["mana"] = 5
            return True
        return False
    if kind == "yes":
        hero["mana"] = hero["mana"] + 1
        return True
    if kind == "ask":
        return hero["mana"] >= int(n)
    return False


def fx_row(where, heroes, action, *, variant=False, calls_only=False, fall=None, name=None, empty_msg=None):
    """One apply_to_all row. Mar'tu's recorder effect (_eff) logs each call, then does `action` to the sheet."""
    import copy

    after = copy.deepcopy(heroes)
    worked = [_effect_py(action, h) for h in after]
    names = [h["name"] for h in heroes]
    want = [h["name"] for h, w in zip(heroes, worked) if w is True] if variant else names
    alts = []
    if variant:
        mana = [h["name"] for h in heroes if h["mana"] < 10]
        if mana != want:
            alts.append((mana, VAR_MANA, "_has('mana')"))
        if names != want:
            alts.append((names, VAR_ALL, None))
        inverse = [h["name"] for h, w in zip(heroes, worked) if w is not True]
        if inverse != want:
            alts.append((inverse, VAR_INV, None))
        if want:
            alts.append(([], VAR_QUOTES, "_has('True')"))
            alts.append(([], empty_msg or VAR_NONE_KEPT, None))
    elif len(names) > 1:
        alts.append((names[-1:], FX_RESET, None))
    effect = "def _eff(hero):\n    _log.append(hero)\n" + "".join("    " + line + "\n" for line in _effect_lines(action))
    body = (
        _head("apply_to_all", where, ok=FX_OK, typed=FX_TYPED, fall=fall, var=variant, want=want,
              seen=IF_SEEN if variant else FX_SEEN)
        + "_f = _need('apply_to_all', ['heroes', 'effect'])\n"
        + "_log = []\n\n\n" + effect + "\n\n"
        + f"_hs = {copy.deepcopy(heroes)!r}\n"
        + "_given = _B.list(_hs)\n"
        + "_val, _rows, _err = _quiet(lambda: _f(_hs, _eff))\n"
        + "_r = {'val': _val, 'rows': _rows, 'err': _err}\n"
        + f"_fx(_r, _hs, _given, _log, {want!r}, {after!r}, {_alts_code(alts)}, {calls_only!r})\n"
    )
    return check(name or _check_name(where), body)


def _h(name, mana):
    return {"name": name, "mana": mana}


FX_HEAD = "# Trial: one spell for everyone.\ndef apply_to_all(heroes, effect):\n"
FX_REST = (
    "\n\ndef warm(hero):\n"
    '    hero["mana"] = hero["mana"] + 2\n'
    "\n\ndef shout(hero):\n"
    '    print(hero["name"], "shouts!")\n'
    "\n\nparty = [\n"
    '    {"name": "Oogrish", "mana": 12},\n'
    '    {"name": "Lucky", "mana": 20},\n'
    "]\n"
)
FX_TABLE = (
    "\n# Visible tests. They should show\n"
    "# ['Oogrish', 'Lucky'], then [].\n"
    "# (With only pass, each shows None.)\n"
    "print(apply_to_all(party, warm))\n"
    "print(apply_to_all([], warm))\n"
    "# Row 1 warms each hero once, so\n"
    "# this should show 14.\n"
    'print(party[0]["mana"])\n'
    "\n# Row 3 is yours: hand shout to\n"
    "# apply_to_all with party, and\n"
    "# print what it hands back.\n"
)
FX_BODY = (
    "    names = []\n"
    "    for hero in heroes:\n"
    "        effect(hero)\n"
    '        names.append(hero["name"])\n'
    "    return names\n"
)
FX_ROW3 = "print(apply_to_all(party, shout))\n"
FX_SETUP = FX_REST.lstrip("\n")


def _fxc(body="    pass\n", row3="", table=FX_TABLE, rest=FX_REST):
    return FX_HEAD + body + rest + table + row3


FX_STARTER = _fxc()
FX_SOLUTION = _fxc(FX_BODY, FX_ROW3)
FX_PARTY = [_h("Oogrish", 12), _h("Lucky", 20)]

FX_ROW3_CHECK = check("row 3: apply_to_all(party, shout), yours", r'''_FN = 'apply_to_all'
_top = [_n for _n in _tree.body if _tn(_n) != 'FunctionDef']
_calls = [_n for _s in _top for _n in _ast.walk(_s) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name'
          and _n.func.id == 'apply_to_all']
_mine = [_c for _c in _calls if _tn(_arg(_c, 1, 'effect')) == 'Name' and _arg(_c, 1, 'effect').id == 'shout']
if not _mine:
    _own = [_n for _s in _top for _n in _ast.walk(_s) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name'
            and _n.func.id == 'shout']
    assert not _own, ('Hand `shout` to `apply_to_all`, with no `()`: it walks the party and calls `shout` for '
                      'you.')
    assert False, ('Write row 3 at the bottom: call `apply_to_all` with `party` and `shout`, no `()` on `shout`, '
                   'inside `print(...)`.')
_c = _mine[0]
_who = _arg(_c, 0, 'heroes')
assert _tn(_who) == 'Name' and _who.id == 'party', 'Hand over `party` first, then `shout`: the roster, then the effect.'
_prints = [_p for _s in _top for _p in _ast.walk(_s) if _tn(_p) == 'Call' and _tn(_p.func) == 'Name'
           and _p.func.id == 'print']
_shown = _B.any(_a is _c for _p in _prints for _a in _p.args)
if not _shown:
    _vars = [_t.id for _s in _top if _tn(_s) == 'Assign' and _s.value is _c for _t in _s.targets if _tn(_t) == 'Name']
    _shown = _B.any(_tn(_a) == 'Name' and _a.id in _vars for _p in _prints for _a in _p.args)
assert _shown, 'Print what `apply_to_all` hands back: put the call inside `print(...)`.'
# shout's own lines (any words, and any heroes the student gave `party`), not the printed lists of names
_p = _g.get('party')
_crew = ([_h.get('name') for _h in _p if _tn(_h) == 'dict' and _tn(_h.get('name')) == 'str']
         if _tn(_p) == 'list' else [])
_crew = _crew or ['Oogrish', 'Lucky']
_said = [_l for _l in _lines() if not _B.any("'" + _n + "'" in _l for _n in _crew)]
assert _B.all(_B.any(_n in _l for _l in _said) for _n in _crew), (
    'Let row 3 run, with `shout` printing each hero\'s name: every hero should shout once when row 3 runs.')
''')

APPLY_TO_ALL = dict(
    kind="challenge",
    id="apply-to-all",
    title="One Spell for Everyone",
    level="core",
    optional=True,
    minutes=8,
    support="light",
    tracer=True,
    summary="Write `apply_to_all(heroes, effect)`: call the effect on every hero, and hand back their names. "
            "Then hand it a function yourself.",
    martu=(
        "Oogrish's spell trial. A function can be handed to another function, like any value. Write "
        "`apply_to_all(heroes, effect)`. It calls `effect(hero)` once for each hero, then hands back a list of "
        "their names, in order.\n"
        "```text\napply_to_all(party, warm)\n  → ['Oogrish', 'Lucky']\napply_to_all([], warm)\n  → []\n```\n"
        "Row 3 is yours to write: hand over `shout`, with no `()`. Then my hidden tests hand over other heroes and "
        "other effects, yes?"
    ),
    names=["apply_to_all", "heroes", "effect", "hero", "shout", "party"],
    setup=FX_SETUP,
    starter=FX_STARTER,
    checkpoints=[
        dict(
            id="table",
            text="Write `apply_to_all` so rows 1 and 2 pass: each hero gets the effect once, and the names come "
                 "back in a list.",
            dictated=False,
            hints=[
                "Row 1 hands over two heroes and the function `warm`. Inside, `effect` holds `warm`. Call it on "
                "each hero, and collect each name. Row 2 hands over an empty roster.",
                "With other names: `for jar in shelf:` with `fill(jar)` and `labels.append(jar[\"label\"])` inside. "
                "Make `labels = []` before the loop, and hand it back with `return` after the loop.",
                "Write `names = []`, then `for hero in heroes:` with `effect(hero)` and `names.append(hero[\"name\"])` "
                "inside it, then `return names` after the loop.",
            ],
            checks=[
                fx_row(("v", 1, "`apply_to_all(party, warm)`", "hand back `['Oogrish', 'Lucky']` and warm each "
                        "hero once", ""), FX_PARTY, "add:2"),
                fx_row(_vis(2, "`apply_to_all([], warm)`", []), [], "add:2"),
            ],
            pass_line="Oogrish: Steady, now. One spell, every hero.",
        ),
        dict(
            id="row-3",
            text="Row 3 is yours: hand `shout` to `apply_to_all` with `party`, and print what it hands back.",
            dictated=False,
            hints=[
                "At the bottom, under the row 3 comment. `shout` goes in the way `warm` does in row 1: just its "
                "name.",
                "With no `()`, the name is the function itself, and `apply_to_all` calls it later. With `()`, "
                "`shout` would run once, right now, and hand over `None`.",
                "Write `print(apply_to_all(party, shout))` at the bottom.",
            ],
            checks=[FX_ROW3_CHECK],
            pass_line="Lucky: Everyone shouts. My kind of spell.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: other rosters, other effects, one hero.",
            dictated=False,
            hints=[
                "The hidden tests hand over other heroes and other effects. Inside the function, use only `heroes` "
                "and `effect`.",
                "A function that calls `warm` by name works for one effect only. `effect(hero)` works for any "
                "effect it is handed.",
                "Keep `effect(hero)` and `names.append(hero[\"name\"])` inside `for hero in heroes:`, and `return "
                "names` after the loop.",
            ],
            checks=[
                fx_row(("h", "another roster and another effect"), [_h("Pell", 3), _h("Brakka", 8), _h("Moss", 0)],
                       "set:30"),
                fx_row(("h", "a roster of one"), [_h("Glug", 6)], "add:1"),
                fx_row(("h", "an effect that changes nothing"), [_h("Ivo", 5), _h("Ash", 2)], "none"),
                fx_row(("h", "four heroes, in order"), [_h("Moth", 1), _h("Bree", 4), _h("Tinplate", 9),
                                                        _h("Ash", 2)], "add:2"),
            ],
            pass_line="Mar'tu: Any roster, any spell. That is a function as a value, yes?",
        ),
    ],
    solution=FX_SOLUTION,
    partials=[_fxc(FX_BODY)],
    assemble=dict(
        lines=lines_of(FX_HEAD + FX_BODY) + [FX_ROW3.strip()],
        distractors=["        effect()", "        names.append(effect(hero))", "print(apply_to_all(party, shout()))"],
    ),
    another_way=[
        dict(angle="picture", label="Handing over the card", text=(
            "```text\napply_to_all(party, warm)\n\ninside: effect = warm\n  Oogrish: effect(hero)\n"
            "  Lucky:   effect(hero)\n  names → ['Oogrish',\n           'Lucky']\n```\nYou hand over the recipe "
            "card once. The loop cooks it for each hero.")),
        dict(angle="step-by-step", text=(
            "1. Make an empty list for the names.\n2. For each hero: call `effect(hero)`, then append the hero's "
            "name.\n3. After the loop, hand back the list with `return`. An empty roster skips the loop and hands "
            "back `[]`.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`add_spell(..., strengthen_magic)` handed over `strengthen_magic` with no `()`, so the game could call "
            "it later. Here `apply_to_all` is the one calling it later: `effect(hero)`.")),
    ],
    predict=dict(
        q="Before you write it: what does this print?",
        code='def cheer(sheet):\n    print(sheet["name"], "cheers")\n\n\nprint(cheer({"name": "Moth"}))\n',
        choices=["Moth cheers\nNone", "None", "Moth cheers"],
        answer=0,
        explain=(
            "`cheer` prints its line, then hands back `None`, because it has no `return`. So `effect(hero)` gives "
            "you nothing to put in the list: append the hero's name instead."
        ),
    ),
    pair_talk="Tell your partner what `effect` holds inside `apply_to_all` during row 1, and during row 3.",
    campaign_link=dict(
        module=MODULE,
        part="spell-book",
        snippet='add_spell(member["spell_book"], "Strengthen Magic", 10, 8, strengthen_magic)',
        why=(
            "`strengthen_magic` went into `add_spell` with no `()`: the game was handed the function, to call later. "
            "`apply_to_all` is the other side of that handover. It receives a function and calls it."
        ),
    ),
    takeaway="Hand a function over by its name, no `()`. The function that receives it calls it: `effect(hero)`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=FX_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the effect never called (names only)",
             code=_fxc('    names = []\n    for hero in heroes:\n        names.append(hero["name"])\n'
                       "    return names\n"), fails_at=1, message_contains="nothing called the effect"),
        dict(why="`effect` on its own line, not called",
             code=_fxc(FX_BODY.replace("effect(hero)", "effect")), fails_at=1,
             message_contains="names the function but does not run it"),
        dict(why="effect() with no hero: the bottom prints stop with Python's TypeError",
             code=_fxc(FX_BODY.replace("effect(hero)", "effect()")), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="effect() with no hero, the bottom prints gone: Mar'tu's message",
             code=_fxc(FX_BODY.replace("effect(hero)", "effect()"), table=""), fails_at=1,
             message_contains="Hand the hero to the effect"),
        dict(why="effect(heroes), the whole list, the prints gone",
             code=_fxc(FX_BODY.replace("effect(hero)", "effect(heroes)"), table=""), fails_at=1,
             message_contains="not the whole list"),
        dict(why="the name handed to the effect, effect(hero[\"name\"]): the bottom prints stop with Python's "
                 "TypeError", code=_fxc(FX_BODY.replace("effect(hero)", 'effect(hero["name"])')), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="the name handed to the effect, the prints gone: Mar'tu's message",
             code=_fxc(FX_BODY.replace("effect(hero)", 'effect(hero["name"])'), table=""), fails_at=1,
             message_contains="Hand over the whole sheet"),
        dict(why="the names sorted (not the roster's order)",
             code=_fxc(FX_BODY.replace("    return names\n", "    return sorted(names)\n")), fails_at=1,
             message_contains="in the order of `heroes`"),
        dict(why="what the effect hands back appended (None)",
             code=_fxc("    names = []\n    for hero in heroes:\n        names.append(effect(hero))\n"
                       "    return names\n"), fails_at=1, message_contains="hands back `None`"),
        dict(why="what the effect hands back appended: the evidence shows the list as it is, [None, None]",
             code=_fxc("    names = []\n    for hero in heroes:\n        names.append(effect(hero))\n"
                       "    return names\n"), fails_at=1, message_contains="it handed back `[None, None]`"),
        dict(why="the sheets appended, not the names", code=_fxc(FX_BODY.replace('hero["name"]', "hero")),
             fails_at=1, message_contains="not the whole sheet"),
        dict(why="the roster itself handed back",
             code=_fxc("    for hero in heroes:\n        effect(hero)\n    return heroes\n"), fails_at=1,
             message_contains="handed back the same roster"),
        dict(why="return inside the loop (the first hero only)",
             code=_fxc(FX_BODY.replace("    return names\n", "").replace('hero["name"])\n',
                                                                      'hero["name"])\n        return names\n')),
             fails_at=1, message_contains="`return` after the loop"),
        dict(why="the list made again inside the loop (the last name only)",
             code=_fxc("    for hero in heroes:\n        names = []\n        effect(hero)\n"
                       '        names.append(hero["name"])\n    return names\n', table=""), fails_at=1,
             message_contains="before the loop"),
        dict(why="print instead of return", code=_fxc(FX_BODY.replace("    return names\n", "    print(names)\n")),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="row 1's answer typed after the loop (its only `return` is a typed list: caught at row 1)",
             code=_fxc('    for hero in heroes:\n        effect(hero)\n    return ["Oogrish", "Lucky"]\n'),
             fails_at=1, message_contains="typed in it"),
        dict(why='row 1\'s answer typed alone, return ["Oogrish", "Lucky"] (no loop: "typed in it" comes before '
                 '"nothing called the effect")',
             code=_fxc('    return ["Oogrish", "Lucky"]\n'), fails_at=1, message_contains="typed in it"),
        dict(why="the table typed behind an if (passes rows 1-3; the hidden tests catch it)",
             code=_fxc("    for hero in heroes:\n        effect(hero)\n    if heroes == []:\n        return []\n"
                       '    return ["Oogrish", "Lucky"]\n', FX_ROW3), fails_at=3, message_contains="typed in it"),
        dict(why="the global warm called by name, not effect",
             code=_fxc(FX_BODY.replace("effect(hero)", "warm(hero)")), fails_at=1,
             message_contains="calls `warm` itself"),
        dict(why="the global party read, not the parameter",
             code=_fxc(FX_BODY.replace("in heroes", "in party")), fails_at=1,
             message_contains="Use the parameter `heroes`, not `party`"),
        dict(why="a list kept outside the function (it keeps names from every call)",
             code=_fxc('    for hero in heroes:\n        effect(hero)\n        names.append(hero["name"])\n'
                       "    return names\n", rest=FX_REST + "\n\nnames = []\n"), fails_at=1,
             message_contains="Make the list of names inside the function"),
        dict(why="None for an empty roster (a bare return)",
             code=_fxc("    if len(heroes) == 0:\n        return\n" + FX_BODY), fails_at=1,
             message_contains="even for an empty roster"),
        dict(why="typed positions, the prints gone: an empty roster has no heroes[0]",
             code=_fxc('    effect(heroes[0])\n    effect(heroes[1])\n'
                       '    return [heroes[0]["name"], heroes[1]["name"]]\n', table=""), fails_at=1,
             message_contains="not typed positions"),
        dict(why="the effect called twice for each hero", code=_fxc(FX_BODY.replace(
            "        effect(hero)\n", "        effect(hero)\n        effect(hero)\n")), fails_at=1,
             message_contains="once for each hero, not more"),
        dict(why="the roster emptied with .pop(0): the starter's own party[0] print stops with an IndexError",
             code=_fxc("    names = []\n    while len(heroes) > 0:\n        hero = heroes.pop(0)\n"
                       '        effect(hero)\n        names.append(hero["name"])\n    return names\n'), fails_at=0,
             message_contains="IndexError"),
        dict(why="the roster emptied with .pop(0), the prints gone: the list handed in changed",
             code=_fxc("    names = []\n    while len(heroes) > 0:\n        hero = heroes.pop(0)\n"
                       '        effect(hero)\n        names.append(hero["name"])\n    return names\n', table=""),
             fails_at=1, message_contains="Leave `heroes` as it was"),
        dict(why="row 3 not written (the partial)", code=_fxc(FX_BODY), fails_at=2, message_contains="Write row 3"),
        dict(why="row 3 hands over shout() with brackets: Python's TypeError at the call",
             code=_fxc(FX_BODY, "print(apply_to_all(party, shout()))\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="row 3 hands over what shout(party[0]) returned (None): Python's error at the call",
             code=_fxc(FX_BODY, "print(apply_to_all(party, shout(party[0])))\n"), fails_at=0,
             message_contains="'NoneType' object is not callable"),
        dict(why="row 3 hands over the name in quotes", code=_fxc(FX_BODY, 'print(apply_to_all(party, "shout"))\n'),
             fails_at=0, message_contains="'str' object is not callable"),
        dict(why="row 3 with the values the other way round", code=_fxc(FX_BODY, "print(apply_to_all(shout, party))\n"),
             fails_at=0, message_contains="not iterable"),
        dict(why="row 3 not printed", code=_fxc(FX_BODY, "apply_to_all(party, shout)\n"), fails_at=2,
             message_contains="Print what `apply_to_all` hands back"),
        dict(why="row 3 as a loop of its own, shout called directly",
             code=_fxc(FX_BODY, "for hero in party:\n    shout(hero)\n"), fails_at=2,
             message_contains="Hand `shout` to `apply_to_all`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Functions", trial="T-F-2", opens="after Unit 7",
             ceiling="Units 1-7", skills="func-as-value,loop-list,append,return-value,read-test-table",
             solo="false", dictates="", foreign_names="jar,shelf,fill,labels,label,cheer,sheet",
             par="another roster and another effect (Pell, Brakka, Moss; mana set to 30); a roster of one (Glug); "
                 "an effect that changes nothing (Ivo, Ash); four heroes in order (Moth, Bree, Tinplate, Ash)")
        + "\n"
        "T-F-2 (the spec: 'apply_to_all(heroes, effect) -> a list of the names affected'). In the core every hero "
        "is affected; the variant keeps only the ones the effect worked on. The checks hand over Mar'tu's recorder "
        "effect, not the starter's `warm`, so a function that calls `warm` by name is caught on the first row. "
        "Row 3 is the caller side of the brief's slip 'calling the effect function with () when passing it': "
        "`shout()`, `shout(party[0])` and `\"shout\"` are Python's own errors at the call (fails_at 0, the "
        "explainer's rows; u07b's 6C-02 catches). The setup repeats the starter's `warm`, `shout` and `party` so "
        "the Assemble lines (the function and the row-3 line) run on their own. Evidence: u07b's "
        "`cast_on_everyone(roster, warm_hands(lucky))`, print for return (A-07), typed test values (A-06). "
        "Teacher ruling (Nov 14): the starter prints the two calls under \"# Visible tests. They should show\" and "
        "\"# (With only pass, each shows None.)\", then `party[0][\"mana\"]` under its own comment (\"should show "
        "14\"), so the None line is true of every line it covers. Evidence: row 1's want is also an action, so its "
        "bracket reads \"it should hand back ... and warm each hero once; <what happened>\"; a visible row's list "
        "is shown as it is when every item is None, True, False, a number or one of the test's names "
        "(`[None, None]` for `names.append(effect(hero))`), and a hidden row shows only its length. Check order: "
        "when the function's only `return` is a typed list equal to a visible row's answer (`return [\"Oogrish\", "
        "\"Lucky\"]`, with or without a loop), \"typed in it\" comes before \"nothing called the effect\". Predict "
        "answer index 0, its distractors reordered (2 of the unit's 18 predicts keep the answer first, so its "
        "place is never a giveaway). Show-rung copy-test: CP1's rung in place of `pass` is the partial (no crash; "
        "row 3 is the student's line); CP2's line at the bottom is the solution; CP3's keeps it."
    ),
)


# =============================================================================================
# T-F-2a "Only the Ones It Worked On": include a name only when effect(hero) returns True (advanced,
# variant_of apply-to-all)
# =============================================================================================

IF_HEAD = "# Trial: only the ones it worked on.\ndef apply_to_all(heroes, effect):\n"
IF_REST = (
    "\n\ndef top_up(hero):\n"
    "    # Works on a hero below 10.\n"
    '    if hero["mana"] < 10:\n'
    '        hero["mana"] = 10\n'
    "        return True\n"
    "    return False\n"
    "\n\nparty = [\n"
    '    {"name": "Oogrish", "mana": 4},\n'
    '    {"name": "Lucky", "mana": 20},\n'
    "]\n"
)
IF_TABLE = (
    "\n# Visible tests. They should show\n"
    "# ['Oogrish'], then [] (all full\n"
    "# now), then [].\n"
    "# (With only pass, each shows None.)\n"
    "print(apply_to_all(party, top_up))\n"
    "print(apply_to_all(party, top_up))\n"
    "print(apply_to_all([], top_up))\n"
)
# The append line is 38 characters (the phone-width exception the notes give): it matches the Show rungs.
IF_BODY = (
    "    names = []\n"
    "    for hero in heroes:\n"
    "        if effect(hero):\n"
    '            names.append(hero["name"])\n'
    "    return names\n"
)


def _ifc(body="    pass\n", table=IF_TABLE):
    return IF_HEAD + body + IF_REST + table


IF_STARTER = _ifc()
IF_SOLUTION = _ifc(IF_BODY)
IF_PARTY = [_h("Oogrish", 4), _h("Lucky", 20)]
IF_FULL = [_h("Oogrish", 10), _h("Lucky", 20)]

APPLY_IF_WORKED = dict(
    kind="challenge",
    id="apply-if-it-worked",
    title="Only the Ones It Worked On",
    level="advanced",
    variant_of="apply-to-all",
    optional=True,
    minutes=9,
    support="light",
    tracer=True,
    summary="The advanced twin of One Spell for Everyone: an effect hands back `True` when it worked, and only "
            "those heroes' names come back.",
    martu=(
        "The advanced spell trial. Some effects only work on some heroes. Now an effect hands back `True` when it "
        "worked, and `False` when it did not.\n"
        "Write `apply_to_all(heroes, effect)` again. Call `effect(hero)` once for each hero, and hand back the "
        "names of only the heroes it worked on.\n"
        "```text\napply_to_all(party, top_up)\n  → ['Oogrish']\napply_to_all(party, top_up)\n"
        "  → []  (all full now)\napply_to_all([], top_up)\n  → []\n```\n"
        "Call it once, and keep what it hands back, yes?"
    ),
    names=["apply_to_all", "heroes", "effect", "hero"],
    starter=IF_STARTER,
    checkpoints=[
        dict(
            id="every-hero",
            text="Write `apply_to_all` so `effect(hero)` runs once on each hero in row 1.",
            dictated=False,
            hints=[
                "Start with the loop from the core trial. Every hero gets the effect, even the heroes it does not "
                "work on.",
                "With other names: `for jar in shelf:` with `fill(jar)` inside runs `fill` once on each jar.",
                "Write `names = []`, then `for hero in heroes:` with `effect(hero)` and `names.append(hero[\"name\"])` "
                "inside it, then `return names` after the loop.",
            ],
            checks=[
                fx_row(("v", 1, "`apply_to_all(party, top_up)`", "run `top_up` once on each hero", ""), IF_PARTY,
                       "top:10", variant=True, calls_only=True, name="row 1: top_up runs once on each hero"),
            ],
            pass_line="Gearshift: Every hero checked. Visor dims.",
        ),
        dict(
            id="only-if-true",
            text="Hand back only the names the effect said `True` for: rows 1, 2 and 3.",
            dictated=False,
            hints=[
                "Row 1: the effect works on Oogrish, who is below 10, and not on Lucky. Row 2: everyone is full "
                "now, so it works on no one.",
                "`if fill(jar):` runs `fill` and asks about its answer, in one line. Calling it twice would fill "
                "the jar twice, and the second answer would be `False`.",
                "Change `effect(hero)` to `if effect(hero):`, and move `names.append(hero[\"name\"])` inside it. "
                "Keep `return names` after the loop.",
            ],
            checks=[
                fx_row(_vis(1, "`apply_to_all(party, top_up)`", ["Oogrish"]), IF_PARTY,
                       "top:10", variant=True),
                fx_row(_vis(2, "`apply_to_all(party, top_up)` a second time", []), IF_FULL,
                       "top:10", variant=True),
                fx_row(_vis(3, "`apply_to_all([], top_up)`", []), [], "top:10", variant=True),
            ],
            pass_line="Lucky: Only the ones it worked on. Like a good deal.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: new effects, one that just answers, one that works on all, and one "
                 "that works on none.",
            dictated=False,
            hints=[
                "The hidden effects have their own rules, and one only answers: it changes no sheet. Ask the "
                "effect, never the sheet: no `hero[\"mana\"]` inside your function.",
                "`True` and `\"True\"` are not the same. `if effect(hero):` asks the effect's own answer, with no "
                "quotes.",
                "Keep `if effect(hero):` inside the loop, with `names.append(hero[\"name\"])` under it.",
            ],
            checks=[
                fx_row(("h", "another effect, with its own rule"), [_h("Pell", 0), _h("Moss", 3), _h("Ash", 0)],
                       "wake", variant=True),
                fx_row(("h", "an effect that works on no one"), [_h("Ivo", 5), _h("Bree", 2)], "no", variant=True),
                fx_row(("h", "an effect that works on everyone"), [_h("Moth", 3), _h("Glug", 1)], "yes",
                       variant=True),
                fx_row(("h", "a roster of one"), [_h("Tinplate", 2)], "top:10", variant=True),
                fx_row(("h", "an effect that only answers, and changes nothing"),
                       [_h("Bree", 7), _h("Glug", 2), _h("Moth", 12)], "ask:5", variant=True, empty_msg=VAR_SHEET),
            ],
            pass_line="Mar'tu: The effect answers, and you listen. Good, yes?",
        ),
    ],
    solution=IF_SOLUTION,
    partials=[_ifc(FX_BODY)],
    assemble=dict(
        lines=lines_of(IF_HEAD + IF_BODY),
        distractors=["        if effect:", '        if effect(hero) == "True":', "        names.append(effect(hero))"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Make an empty list.\n2. For each hero: call `effect(hero)` once, inside the `if`.\n3. `True`? "
            "Append the name. `False`? Skip it.\n4. After the loop, hand back the list.")),
        dict(angle="in Tor", label="Bomb Shell's roll call", text=(
            "Bomb Shell tries the latch on every door. A door that opens, he writes down. A door that stays shut, "
            "he leaves off the list. He tries each door once: twice would tell him nothing new.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The trap-door checks handed back a yes or a no: `return roll >= required_roll`. An effect here does "
            "the same. `if effect(hero):` asks that yes-or-no answer, like an `if` on a skill check.")),
    ],
    predict=dict(
        q="Before you write it: what do the two prints show?",
        code=(
            "def nap(sheet):\n"
            '    if sheet["mana"] < 5:\n'
            '        sheet["mana"] = 5\n'
            "        return True\n"
            "    return False\n"
            "\n\n"
            'moth = {"mana": 2}\n'
            "print(nap(moth))\n"
            "print(nap(moth))\n"
        ),
        choices=["True\nTrue", "True\nFalse", "False\nFalse"],
        answer=1,
        explain=(
            "The first call tops Moth up and hands back `True`. The second finds Moth already at 5, so it hands "
            "back `False`. Call an effect once, and keep its answer."
        ),
    ),
    pair_talk="Row 2 gives `[]`. Tell your partner why, and what a second `effect(hero)` call inside your loop "
              "would do.",
    campaign_link=dict(
        module=MODULE,
        part="skill-checks",
        snippet="return roll >= required_roll",
        why=(
            "The trap-door checks handed back `True` or `False`, and the game asked that answer with an `if`. Here "
            "the effect hands back the answer, and `if effect(hero):` asks it."
        ),
    ),
    takeaway="`if effect(hero):` calls the function and asks its answer in one line. Call it once.",
    wrong_answers=[
        dict(why="the starter (pass)", code=IF_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the core solution, every name (the partial)", code=_ifc(FX_BODY), fails_at=2,
             message_contains="Keep only the heroes the effect worked on"),
        dict(why="`if effect:` (asks whether there is a function; never calls it)",
             code=_ifc(IF_BODY.replace("if effect(hero):", "if effect:")), fails_at=1,
             message_contains="`if effect:` only asks"),
        dict(why="the effect called twice: once alone, once in the if",
             code=_ifc(IF_BODY.replace("        if effect(hero):\n", "        effect(hero)\n        if effect(hero):\n")),
             fails_at=1, message_contains="A second call runs the effect again"),
        dict(why='"True" in quotes (text, never equal to True)',
             code=_ifc(IF_BODY.replace("if effect(hero):", 'if effect(hero) == "True":')), fails_at=2,
             message_contains="without quotes"),
        dict(why="the names it did not work on (if not)",
             code=_ifc(IF_BODY.replace("if effect(hero):", "if not effect(hero):")), fails_at=2,
             message_contains="not `False`"),
        dict(why="the effect's answers appended, not the names",
             code=_ifc("    names = []\n    for hero in heroes:\n        names.append(effect(hero))\n"
                       "    return names\n"), fails_at=2, message_contains="not the `True` itself"),
        dict(why="the sheet's mana read instead of the effect's answer (passes the table; the hidden effect "
                 "catches it)",
             code=_ifc('    names = []\n    for hero in heroes:\n        if hero["mana"] < 10:\n'
                       '            names.append(hero["name"])\n        effect(hero)\n'
                       "    return names\n"), fails_at=3, message_contains="Ask the effect, not the sheet"),
        dict(why="the sheet watched instead of the effect's answer (a copy before, compared after: passes the table; "
                 "the hidden effect that only answers catches it)",
             code=_ifc('    names = []\n    for hero in heroes:\n        before = dict(hero)\n        effect(hero)\n'
                       '        if hero != before:\n            names.append(hero["name"])\n    return names\n'),
             fails_at=3, message_contains="even if the sheet stays the same"),
        dict(why="the mana watched instead of the effect's answer (passes the table; the hidden effect that only "
                 "answers catches it)",
             code=_ifc('    names = []\n    for hero in heroes:\n        before = hero["mana"]\n        effect(hero)\n'
                       '        if hero["mana"] != before:\n            names.append(hero["name"])\n    return names\n'),
             fails_at=3, message_contains="even if the sheet stays the same"),
        dict(why="print instead of return", code=_ifc(IF_BODY.replace("    return names\n", "    print(names)\n")),
             fails_at=2, message_contains="Use `return`, not `print`"),
        dict(why="return inside the loop",
             code=_ifc(IF_BODY.replace("    return names\n", "        return names\n")),
             fails_at=1, message_contains="`return` after the loop"),
        dict(why="row 1's answer typed after the loop (its only `return` is a typed list: caught at row 1, before "
                 "the filter step)",
             code=_ifc('    for hero in heroes:\n        effect(hero)\n    return ["Oogrish"]\n'),
             fails_at=1, message_contains="typed in it"),
        dict(why="the whole table typed: the effect's answers collected, then a typed name (passes rows 1-3; the "
                 "hidden tests catch it)",
             code=_ifc("    results = []\n    for hero in heroes:\n        results.append(effect(hero))\n"
                       "    if True in results:\n        return [\"Oogrish\"]\n    return []\n"), fails_at=3,
             message_contains='`"Oogrish"` typed in it'),
        dict(why="None for an empty roster", code=_ifc("    if len(heroes) == 0:\n        return\n" + IF_BODY),
             fails_at=2, message_contains="even for an empty roster"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Functions (advanced)", trial="T-F-2a",
             variant_of="apply-to-all", opens="after Unit 7", ceiling="Units 1-7",
             skills="func-as-value,call-once,if-on-call,loop-list,return-value", solo="false", dictates="",
             foreign_names="jar,shelf,fill,nap,sheet,moth",
             par="another effect with its own rule (Pell 0, Moss 3, Ash 0: wakes the ones at 0); an effect that "
                 "works on no one; an effect that works on everyone; a roster of one (Tinplate); an effect that only "
                 "answers (True at 5 mana or more) and changes nothing (Bree 7, Glug 2, Moth 12)") + "\n"
        "T-F-2a, variant_of apply-to-all (the spec: 'Include a name only when effect(hero) returns True'). CP1 is "
        "the call itself (once on each hero), CP2 the filter, CP3 the hidden effects; the core solution is the "
        "partial (passes CP1, fails CP2). Row 2 calls the same effect on a roster it has already topped up, so a "
        "second call per hero shows (it returns False the second time, and the recorder counts it). The hidden "
        "'own rule' effect catches a function that reads `hero[\"mana\"] < 10` itself instead of asking the "
        "effect. The hidden 'only answers' effect returns True without changing any sheet, so a function that watches "
        "the sheet (a copy before the call, compared after) instead of keeping the effect's answer is caught: it "
        "passes every other row. Teacher ruling (Nov 14): CP1's Show rung ended on `if effect(hero):` with "
        "nothing under it (pasted, an IndentationError), and CP2's appended `name`, which no line made (a "
        "NameError). Now CP1's rung is the core loop (`effect(hero)` and `names.append(hero[\"name\"])`, partial "
        "1, `_ifc(FX_BODY)`); CP2's changes `effect(hero)` to `if effect(hero):` and moves the append inside it "
        "(the solution); CP3's keeps it. The solution no longer makes `name = hero[\"name\"]`: it appends "
        "`hero[\"name\"]` directly, so Compare matches the rungs word for word; that append line is 38 characters "
        "(the docstring's phone-width exception). Wrong answers that copied the old `name` line now use the new "
        "shape. Check order: the typed `return [\"Oogrish\"]` is caught at CP1 (\"typed in it\" before the filter "
        "step). Predict answer index 1. Show-rung copy-test: CP1 pasted in place of `pass`: no crash, CP1 passes, "
        "CP2 says 'Keep only the heroes the effect worked on'; CP2 pasted on top: no crash, every checkpoint "
        "passes."
    ),
)


# =============================================================================================
# T-F-3 "Four Branches, One Lookup": refactor a four-branch elif into `lines[choice]`, with a default (core)
# =============================================================================================

REPLIES = {"option 1": "Steady, now.", "option 2": "Not a compass.", "option 3": "Rest first.",
           "option 4": "Ask Mar'tu."}
REPLY_DEFAULT_TEXT = "Say that again?"
REPLY_HEAD = "# Trial: four branches, one lookup.\n# reply works. Make it shorter.\n"
REPLY_CHAIN = (
    "def reply(choice):\n"
    '    if choice == "option 1":\n'
    '        return "Steady, now."\n'
    '    elif choice == "option 2":\n'
    '        return "Not a compass."\n'
    '    elif choice == "option 3":\n'
    '        return "Rest first."\n'
    '    elif choice == "option 4":\n'
    "        return \"Ask Mar'tu.\"\n"
    "    else:\n"
    '        return "Say that again?"\n'
)
LINES_DICT = (
    "lines = {\n"
    '    "option 1": "Steady, now.",\n'
    '    "option 2": "Not a compass.",\n'
    '    "option 3": "Rest first.",\n'
    "    \"option 4\": \"Ask Mar'tu.\",\n"
    "}\n"
)
REPLY_NEW = (
    "def reply(choice):\n"
    "    if choice in lines:\n"
    "        return lines[choice]\n"
    '    return "Say that again?"\n'
)
REPLY_TABLE = (
    "\n\n# Visible tests. They should show\n"
    "# Steady, now.\n"
    "# Ask Mar'tu.\n"
    "# Say that again?\n"
    'print(reply("option 1"))\n'
    'print(reply("option 4"))\n'
    'print(reply("option 9"))\n'
)


def _rep(body, table=REPLY_TABLE):
    return REPLY_HEAD + body + table


REPLY_STARTER = _rep(REPLY_CHAIN)
REPLY_SOLUTION = _rep(LINES_DICT + "\n\n" + REPLY_NEW)
REPLY_PARTIAL = _rep(LINES_DICT + "\n\n" + REPLY_CHAIN)
# CP2's Show me how, pasted word for word: the lookup behind `in`, no default yet (row 3 shows None, no crash).
REPLY_ASKED = _rep(LINES_DICT + "\n\ndef reply(choice):\n    if choice in lines:\n        return lines[choice]\n")
REPLY_OK = list(REPLIES) + list(REPLIES.values()) + [REPLY_DEFAULT_TEXT, "Mind the barrier.", "Glug break."]
REPLY_KEY = ("Keep the default: ask `if choice in lines:` first, or use `lines.get(choice, \"Say that again?\")`. "
             "Python stopped with a KeyError: `lines` has no such key.")
REPLY_NONE = ("Give the default a home: ask `if choice in lines:` first, and below it hand back `\"Say that "
              "again?\"` with `return`. For a choice `lines` does not have, your function handed back `None`.")
REPLY_KEEP_DEFAULT = ("Keep the old default: a choice `lines` does not have still hands back `\"Say that again?\"`, "
                      "letter for letter.")
REPLY_ERRS = [
    ("_tn(_e) == 'NameError' and 'lines' in _B.str(_e)",
     "Make `lines` at the top of the program, above `def reply`, so `reply` can read it."),
    ("'list indices must be integers' in _B.str(_e)",
     "Make `lines` a dictionary, not a list: a list is read by position, not by option."),
]
REPLY_SLIPS = [
    (lambda c: c, "Hand back the reply, `lines[choice]`, not the choice itself."),
    (lambda c: REPLY_DEFAULT_TEXT,
     "Ask about the keys: `choice in lines`. `lines.values()` holds the replies, not the options.",
     "_uses('attr:values')"),
]
REPLY_LOWER = (lambda c: REPLIES.get(c.lower(), REPLY_DEFAULT_TEXT),
               "Leave `choice` as it is, with no `.lower()`: the old `reply` gave a choice with a capital letter the "
               "default, and a refactor keeps what the code did.", "_uses('attr:lower')")
REPLY_ADDED_KEY = ("Leave `lines` as it was: your function added a key for a choice `lines` did not have. Just "
                   "hand back the default.")
REPLY_KEEP_LINES = (
    "_L0 = _copy.deepcopy(_g.get('lines'))\n",
    "assert _g.get('lines') == _L0, ('Leave `lines` as it was: your function added or changed a key. For an unknown "
    "choice, just hand back the default. ' + _evs(_r, 'it changed `lines`'))\n",
)


def reply_row(choice, where, *, unknown=False, pre="", after_run="", post="", fall=None, keep_lines=True):
    want = REPLY_DEFAULT_TEXT if unknown else REPLIES.get(choice)
    errs = ([(f"_karg(_e) == {choice!r}", REPLY_KEY)] if unknown else []) + REPLY_ERRS
    if keep_lines:
        pre, post = pre + REPLY_KEEP_LINES[0], post + REPLY_KEEP_LINES[1]
    if unknown:
        # The program's own run (the starter's row-3 print) may already have added the key: ask about the key.
        post += (f"assert _tn(_g.get('lines')) != 'dict' or {choice!r} not in _g['lines'], (" + repr(REPLY_ADDED_KEY)
                 + " + ' ' + _evs(_r, 'it added that choice to `lines`'))\n")
    slips = REPLY_SLIPS + ([REPLY_LOWER] if unknown else [])
    return row("reply", ["choice"], (choice,), want, where, ok=REPLY_OK, errs=errs, slips=slips,
               none=REPLY_NONE if unknown else "", glob=["lines"], fall=fall or (REPLY_KEEP_DEFAULT if unknown else None),
               pre=pre, after_run=after_run, post=post)


def _vis_reply(n, choice, unknown=False, fall=None):
    want = REPLY_DEFAULT_TEXT if unknown else REPLIES[choice]
    return reply_row(choice, _vis(n, f'`reply("{choice}")`', want), unknown=unknown, fall=fall)


LINES_CHECK = check("lines holds the four options and their replies",
                    f"_FN = 'reply'\n_book('lines', {REPLIES!r}, False)\n")
REPLY_CHAIN_CHECK = check("reply asks no == questions, and reads lines",
                          "_FN = 'reply'\n_no_chain('reply', 'choice', 'lines', 'lines[choice]')\n")
REPLY_TYPED_CHECK = check("reply has no reply typed in it", (
    f"_FN = 'reply'\n_want = {list(REPLIES.values())!r}\n"
    "_d = _defs().get('reply')\n"
    "_t = [_n.value for _n in _ast.walk(_d) if _tn(_n) == 'Constant' and _n.value in _want] if _d else []\n"
    "assert not _t, ('Read every reply from `lines`: `reply` still has `\"' + _t[0] + '\"` typed in it, so a '\n"
    "                'line changed in `lines` would never reach it. Only the default stays in `reply`.')\n"
))
REPLY_ADDED = (
    "_L = _g.get('lines')\n_had = _tn(_L) == 'dict'\nif _had:\n    _L['option 5'] = 'Glug break.'\n",
    "if _had:\n    _L.pop('option 5', None)\n",
)
REPLY_CHANGED = (
    "_L = _g.get('lines')\n_had = _tn(_L) == 'dict' and 'option 2' in _L\nif _had:\n    _old = _L['option 2']\n"
    "    _L['option 2'] = 'Mind the barrier.'\n",
    "if _had:\n    _L['option 2'] = _old\n",
)
REPLY_FROM_LINES = ("Read every reply from `lines` itself, inside `reply`: a line Mar'tu's test changed in `lines` "
                    "never reached your function.")


def _reply_hidden_changed(label, choice, want, change):
    body_pre, body_after = change
    return row("reply", ["choice"], (choice,), want, ("h", label), ok=REPLY_OK, errs=REPLY_ERRS, slips=REPLY_SLIPS,
               glob=["lines"], fall=REPLY_FROM_LINES, pre=body_pre, after_run=body_after)


REPLY_LOOKUP = dict(
    kind="challenge",
    id="reply-lookup",
    title="Four Branches, One Lookup",
    level="core",
    optional=True,
    minutes=8,
    support="light",
    summary="Refactor: turn a four-branch `elif` chain into a dictionary `lines` and one lookup, `lines[choice]`, "
            "and keep its default.",
    martu=(
        "A refactor trial. `reply` works, but it is a long `elif` chain: four questions to find one line. You've "
        "seen this shape: Oogrish's four dialogue options.\n"
        "A dictionary can do the finding. Make `lines`, with each option as a key and its reply as the value. Then "
        "`reply` hands back `lines[choice]`, one [[lookup]]. Keep the default: a choice `lines` doesn't have still "
        "gets `\"Say that again?\"`.\n"
        "```text\nreply(\"option 1\") → \"Steady, now.\"\nreply(\"option 4\") → \"Ask Mar'tu.\"\nreply(\"option 9\")\n"
        "  → \"Say that again?\"\n```\n"
        "The table must pass before and after, yes?"
    ),
    names=["lines", "reply", "choice"],
    starter=REPLY_STARTER,
    starter_passes=False,
    checkpoints=[
        dict(
            id="make-lines",
            text="Above `def reply`, make the dictionary `lines`: each option as a key, and its reply as the value.",
            dictated=False,
            hints=[
                "Read the `elif` chain: each `choice == \"option 1\"` gives you a key, and the `return` under it "
                "gives you its value.",
                "With other names: `moods = {\"sun\": \"Bright.\", \"fog\": \"Grey.\"}`. The key goes left of the "
                "`:`, the value right of it, and a comma goes between pairs.",
                "Write `lines = {` above `def reply`, then one pair a line, like `\"option 1\": \"Steady, now.\",`, "
                "then `}`.",
            ],
            checks=[LINES_CHECK],
            pass_line="Mar'tu: Four lines, one dictionary. Good.",
        ),
        dict(
            id="use-lines",
            text="Make `reply` hand back `lines[choice]` in place of the `elif` chain. Rows 1 and 2 must still pass.",
            dictated=False,
            hints=[
                "Inside `reply`, the four `if` and `elif` questions go. One lookup does their work.",
                "`moods[\"fog\"]` reads the value for the key `\"fog\"`. With a parameter, `moods[weather]` reads "
                "the key that `weather` holds: no quotes on the parameter.",
                "Replace the whole chain with `if choice in lines:`, and `return lines[choice]` under it. Row 3's "
                "default is the next step.",
            ],
            checks=[
                REPLY_CHAIN_CHECK,
                REPLY_TYPED_CHECK,
                _vis_reply(1, "option 1"),
                _vis_reply(2, "option 4"),
            ],
            pass_line="Oogrish: One look, and the line is found. Steady, now.",
        ),
        dict(
            id="keep-default",
            text="Keep the default: row 3, a choice `lines` does not have, still hands back `\"Say that again?\"`.",
            dictated=False,
            hints=[
                "Row 3 hands over `\"option 9\"`, a key `lines` does not have. Read with no question first, "
                "`lines[\"option 9\"]` stops Python with a KeyError. Asked with `in`, the `if` is skipped, and the "
                "function hands back `None`.",
                "Ask before you read: `if weather in moods:` is `True` only for a key the dictionary has. "
                "`.get(key, default)` works too: it hands back the default for a missing key.",
                "Write `if choice in lines:` with `return lines[choice]` under it. Below it, `return \"Say that "
                "again?\"`.",
            ],
            checks=[_vis_reply(3, "option 9", unknown=True)],
            pass_line="Lucky: Say that again? I like that line.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: every option, odd choices, and a changed `lines`.",
            dictated=False,
            hints=[
                "The hidden tests try the other two options, an empty choice and a capital letter. Then they "
                "change one line in `lines`, and add one.",
                "Keys match letter for letter: `\"Option 1\"` is not `\"option 1\"`, so it gets the default. A new "
                "key in `lines` should just work, with no change to `reply`.",
                "Read every reply from `lines` itself with `lines[choice]`, and keep `return \"Say that again?\"` "
                "for the rest.",
            ],
            checks=[
                reply_row("option 2", ("h", "the second option")),
                reply_row("option 3", ("h", "the third option")),
                reply_row("", ("h", "an empty choice"), unknown=True),
                reply_row("Option 1", ("h", "a choice with a capital letter"), unknown=True),
                _reply_hidden_changed("a line changed in `lines`", "option 2", "Mind the barrier.", REPLY_CHANGED),
                _reply_hidden_changed("a line added to `lines`", "option 5", "Glug break.", REPLY_ADDED),
            ],
            pass_line="Mar'tu: Add a fifth line, and `reply` knows it. That is why we refactor, yes?",
        ),
    ],
    solution=REPLY_SOLUTION,
    partials=[REPLY_PARTIAL, REPLY_ASKED],
    assemble=dict(
        lines=lines_of(LINES_DICT + REPLY_NEW),
        distractors=['        return lines["choice"]', "    return lines.get(choice)", '    "Option 1": "Steady, now.",'],
    ),
    another_way=[
        dict(angle="picture", label="One question, not four", text=(
            "```text\nchoice = \"option 4\"\n\nelif chain: 1? no 2? no\n            3? no 4? yes\nlookup:     "
            "lines[\"option 4\"]\n            → \"Ask Mar'tu.\"\n```\nThe chain asks until one says yes. The "
            "lookup goes straight to the key.")),
        dict(angle="step-by-step", text=(
            "1. Each `if choice == \"...\":` line gives a key.\n2. The `return` under it gives the value.\n3. The "
            "`else` gives the default: it stays in `reply`.\n4. `reply` asks `if choice in lines:`, and hands back "
            "`lines[choice]` or the default.")),
        dict(angle="everyday", text=(
            "A chain is asking each person in a line, one by one, whether they have your parcel. A lookup is a wall "
            "of labeled pigeonholes: read the label, take the parcel. An empty pigeonhole gets the default note.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`dialogue_option_selected()` asked `user.clicked() == \"option 1\"`, then option 2, 3 and 4. A "
            "dictionary keyed by `\"option 1\"` ... `\"option 4\"` would answer all four in one lookup.")),
    ],
    predict=dict(
        q="Before you refactor: what do these two lines print?",
        code=(
            "moods = {\n"
            '    "sun": "Bright.",\n'
            '    "fog": "Grey.",\n'
            "}\n"
            'print(moods.get("rain", "Hm?"))\n'
            'print("fog" in moods)\n'
        ),
        choices=["None\nTrue", "Hm?\nFalse", "Hm?\nTrue"],
        answer=2,
        explain=(
            "`.get()` hands back its second value, the default, for a key the dictionary does not have. `in` asks "
            "about the keys, and `\"fog\"` is one. No KeyError either way."
        ),
    ),
    pair_talk="Point to one `elif` line and the `return` under it. Tell your partner which part becomes the key, "
              "and which the value.",
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-options",
        snippet='elif (user.clicked() == "option 2"):',
        why=(
            "Oogrish's four dialogue options were a four-branch `elif` chain, one branch for each box. A dictionary "
            "keyed by the option does the same work with one lookup, and a new option is one new line."
        ),
    ),
    takeaway="A dictionary can replace an `if` / `elif` chain: `lines[choice]`, with `in` (or `.get`) for the "
             "default.",
    wrong_answers=[
        dict(why="the starter (the elif chain, no dictionary yet)", code=REPLY_STARTER, fails_at=1,
             message_contains="Make the dictionary `lines`"),
        dict(why="the dictionary made, the chain still in reply (the partial)", code=REPLY_PARTIAL, fails_at=2,
             message_contains="Replace the `elif` chain"),
        dict(why="Show me how (CP1), pasted word for word: one pair, the rest named in words; no crash, CP1 asks for "
                 "the other options", code=_rep('lines = {\n    "option 1": "Steady, now.",\n}\n\n\n' + REPLY_CHAIN),
             fails_at=1, message_contains="all four options as keys"),
        dict(why="lines[choice] with no default: the bottom prints stop with Python's KeyError",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    return lines[choice]\n"), fails_at=0,
             message_contains="KeyError: 'option 9'"),
        dict(why="lines[choice] with no default, the prints gone: Mar'tu's message",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    return lines[choice]\n", table=""), fails_at=3,
             message_contains="Keep the default"),
        dict(why=".get(choice) with no default (None for an unknown choice)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    return lines.get(choice)\n"), fails_at=3,
             message_contains="handed back `None`"),
        dict(why="Show me how (CP2), pasted word for word: the lookup behind `in`; no crash, row 3 hands back None "
                 "until the next step (also partial 2)", code=REPLY_ASKED, fails_at=3,
             message_contains="Give the default a home"),
        dict(why='the parameter quoted, lines["choice"], the prints gone',
             code=_rep(LINES_DICT + '\n\ndef reply(choice):\n    if choice in lines:\n'
                                    '        return lines["choice"]\n    return "Say that again?"\n', table=""),
             fails_at=2, message_contains='Take the quotes off `"choice"`'),
        dict(why="the keys in capitals (\"Option 1\")",
             code=_rep(LINES_DICT.replace('"option', '"Option') + "\n\n" + REPLY_NEW), fails_at=1,
             message_contains="exactly as the `elif` chain has them"),
        dict(why="keys and values swapped (the chain read backwards)",
             code=_rep('lines = {\n    "Steady, now.": "option 1",\n    "Not a compass.": "option 2",\n'
                       '    "Rest first.": "option 3",\n    "Ask Mar\'tu.": "option 4",\n}\n\n\n' + REPLY_NEW),
             fails_at=1, message_contains="on the left of each `:`"),
        dict(why="a list, not a dictionary",
             code=_rep('lines = [\n    "Steady, now.",\n    "Not a compass.",\n    "Rest first.",\n'
                       '    "Ask Mar\'tu.",\n]\n\n\n' + REPLY_CHAIN), fails_at=1, message_contains="a list is read by "
                                                                                     "position"),
        dict(why="two replies swapped between options",
             code=_rep(LINES_DICT.replace('"Not a compass."', '"TMP"').replace('"Rest first."', '"Not a compass."')
                       .replace('"TMP"', '"Rest first."') + "\n\n" + REPLY_NEW), fails_at=1,
             message_contains="its own reply"),
        dict(why="a reply copied wrong (a missing comma)",
             code=_rep(LINES_DICT.replace('"Steady, now."', '"Steady now."') + "\n\n" + REPLY_NEW), fails_at=1,
             message_contains="Copy each reply exactly"),
        dict(why="the dictionary made inside reply only",
             code=_rep("def reply(choice):\n" + "".join("    " + line + "\n" for line in LINES_DICT.splitlines())
                       + "    if choice in lines:\n        return lines[choice]\n    return \"Say that again?\"\n"),
             fails_at=1, message_contains="not inside the function"),
        dict(why="a second copy of the dictionary inside reply (passes the table; the replies typed in reply give it "
                 "away)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    book = {\n"
                       + "".join("    " + line + "\n" for line in LINES_DICT.splitlines()[1:-1])
                       + "    }\n    if choice in book:\n        return book[choice]\n    return lines.get(choice, "
                         "\"Say that again?\")\n"), fails_at=2, message_contains="typed in it"),
        dict(why="the choice returned, not its reply",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    if choice in lines:\n        return choice\n"
                                    "    return \"Say that again?\"\n"), fails_at=2,
             message_contains="not the choice itself"),
        dict(why="the default changed",
             code=_rep(LINES_DICT + "\n\n" + REPLY_NEW.replace('"Say that again?"', '"Huh?"')), fails_at=3,
             message_contains="Keep the old default"),
        dict(why="a key added to lines for an unknown choice (lines changed)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    if choice not in lines:\n"
                                    "        lines[choice] = \"Say that again?\"\n    return lines[choice]\n"),
             fails_at=3, message_contains="added a key for a choice"),
        dict(why="`in lines.values()`: asks about the replies, not the keys",
             code=_rep(LINES_DICT + "\n\n" + REPLY_NEW.replace("in lines:", "in lines.values():")), fails_at=2,
             message_contains="Ask about the keys"),
        dict(why="print instead of return",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    if choice in lines:\n        print(lines[choice])\n"
                                    "    else:\n        print(\"Say that again?\")\n"), fails_at=2,
             message_contains="Use `return`, not `print`"),
        dict(why="rows 1 and 2 typed behind `in` questions, the lookup for the rest (passes the table and the "
                 "hidden rows that change other lines)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    if choice in [\"option 1\"]:\n"
                                    "        return \"Steady, now.\"\n    if choice in lines:\n"
                                    "        return lines[choice]\n    return \"Say that again?\"\n"), fails_at=2,
             message_contains='`"Steady, now."` typed in it'),
        dict(why="the choice lowered first (a refactor must keep the old answers)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    choice = choice.lower()\n" + REPLY_NEW.split("\n", 1)[1]),
             fails_at=4, message_contains="no `.lower()`"),
        dict(why="row 1's answer typed (the dictionary never read)",
             code=_rep(LINES_DICT + "\n\ndef reply(choice):\n    return \"Steady, now.\"\n"), fails_at=2,
             message_contains="Read the answer from the dictionary"),
    ],
    notes=(
        meta(starter_level="refactor (a working elif chain)", path="TRIALS", set="Functions", trial="T-F-3",
             opens="after Unit 7", ceiling="Units 1-7",
             skills="dict-lookup,in-guard,default,refactor,read-test-table", solo="false", dictates="",
             foreign_names="moods,weather,sun,fog,rain",
             par="the second and third options; an empty choice; a choice with a capital letter; a line changed "
                 "in lines (option 2: Mind the barrier.); a line added to lines (option 5: Glug break.)") + "\n"
        "T-F-3 (the spec: 'Refactor: replace a four-branch elif that maps options to lines with a dict lookup "
        "lines[choice], with a default'). A refactor keeps the behaviour, so the starter passes the table already "
        "and fails CP1 (no dictionary). CP1 the dictionary (at the top, so the hidden tests can change it), CP2 the "
        "lookup (no `choice ==` left, `lines` read), CP3 the default (the class's KeyError slip: with the bottom "
        "prints in place it is Python's own KeyError, the explainer's row; with them gone, Mar'tu's message), CP4 "
        "hidden. CP2 also refuses a reply typed inside `reply` (a second copy of the dictionary there, or a row's reply "
        "behind an `in [...]` question: both pass the table), and the hidden 'changed' and 'added' lines prove the "
        "lookup really reads `lines` at call time. A `.lower()` on the choice changes the old behaviour (the capital-"
        "letter hidden test) and is named. The replies are new Oogrish lines, not the "
        "campaign's example options. `.get(choice, \"Say that again?\")` passes as well as `in`. Show-rung "
        "copy-test (Nov 14 rule): CP2's rung used to be `return lines[choice]` alone; pasted, the starter's own "
        "row-3 print stopped Python with a KeyError before Mar'tu's checks ran. Now CP2's rung gives the lookup "
        "behind its question, `if choice in lines:` with `return lines[choice]` under it, and names the default "
        "as the next step: no crash, row 3 shows None, and CP3 says 'Give the default a home' (partial 2, and its "
        "wrong answer). CP3's rung on top is the solution; CP4's keeps it. CP1's rung as written gives one pair "
        "and names the rest in words: no crash, CP1 asks for the other options (its wrong answer). The KeyError "
        "slip itself (`return lines[choice]` with no question) is still Python's own error at the bottom print, "
        "and Mar'tu's message with the prints gone. Starter: the replies one to a comment line under \"# Visible "
        "tests. They should show\". Predict answer index 2."
    ),
)


# =============================================================================================
# T-F-3a "A Book of Actions": a dict of functions, `actions[choice](hero)`; an unknown choice -> False
# (advanced, variant_of reply-lookup)
# =============================================================================================

ACT_FUNC_SRCS = [
    'def rest(hero):\n    hero["mana"] = hero["max_mana"]\n',
    'def glug(hero):\n    hero["mana"] = hero["mana"] + 3\n',
    'def glow(hero):\n    hero["mana"] = hero["mana"] - 2\n',
    'def ward(hero):\n    hero["mana"] = hero["mana"] - 4\n',
]
ACT_FUNCS = "\n\n".join(ACT_FUNC_SRCS)
ACT_OPTIONS = {"option 1": "rest", "option 2": "glug", "option 3": "glow", "option 4": "ward"}
ACT_HEAD = "# Trial: a book of actions.\n# act works. Make it shorter.\n"
ACT_CHAIN = (
    "def act(choice, hero):\n"
    '    if choice == "option 1":\n'
    "        rest(hero)\n"
    '    elif choice == "option 2":\n'
    "        glug(hero)\n"
    '    elif choice == "option 3":\n'
    "        glow(hero)\n"
    '    elif choice == "option 4":\n'
    "        ward(hero)\n"
    "    else:\n"
    "        return False\n"
    "    return True\n"
)
ACTIONS_DICT = (
    "actions = {\n"
    '    "option 1": rest,\n'
    '    "option 2": glug,\n'
    '    "option 3": glow,\n'
    '    "option 4": ward,\n'
    "}\n"
)
ACT_NEW = (
    "def act(choice, hero):\n"
    "    if choice not in actions:\n"
    "        return False\n"
    "    actions[choice](hero)\n"
    "    return True\n"
)
ACT_NO_GUARD = "def act(choice, hero):\n    actions[choice](hero)\n    return True\n"
ACT_TABLE = (
    '\n\nlucky = {"mana": 5, "max_mana": 26}\n'
    "\n# Visible tests. They should show\n"
    "# True, 8, True, 26, False, 26.\n"
    'print(act("option 2", lucky))\n'
    'print(lucky["mana"])\n'
    'print(act("option 1", lucky))\n'
    'print(lucky["mana"])\n'
    'print(act("option 7", lucky))\n'
    'print(lucky["mana"])\n'
)


def _actc(middle, table=ACT_TABLE):
    return ACT_HEAD + ACT_FUNCS + "\n\n" + middle + table


ACT_STARTER = _actc(ACT_CHAIN)
ACT_SOLUTION = _actc(ACTIONS_DICT + "\n\n" + ACT_NEW)
ACT_PARTIAL = _actc(ACTIONS_DICT + "\n\n" + ACT_CHAIN)
ACT_OK = list(ACT_OPTIONS) + ["option 5"]


def act_row(where, choice, hero, want, after=None, *, rec=False, extra="", name=None):
    body = (_head("act", where, ok=ACT_OK, want=want)
            + f"_act({choice!r}, {hero!r}, {want!r}, {after!r}, {rec!r}, {extra!r})\n")
    return check(name or _check_name(where), body)


def _sheet(mana, top=26, **more):
    out = {"mana": mana, "max_mana": top}
    out.update(more)
    return out


ACTIONS_CHECK = check("actions holds the four options and their functions",
                      f"_FN = 'act'\n_book('actions', {ACT_OPTIONS!r}, True)\n")
ACT_KEEP = check("the four actions are left as they are", f"_FN = 'act'\n_keep_defs({ACT_FUNC_SRCS!r})\n")
ACT_CHAIN_CHECK = check("act asks no == questions, and reads actions",
                        "_FN = 'act'\n_no_chain('act', 'choice', 'actions', 'actions[choice](hero)')\n")
ACT_EVERY = check("hidden: every option, through the dictionary", (
    _head("act", ("h", "every option, through the dictionary"), ok=ACT_OK)
    + "for _c in ['option 1', 'option 2', 'option 3', 'option 4']:\n"
    + f"    _act(_c, {_sheet(9, 20)!r}, True, None, True, '')\n"
))

ACT_LOOKUP = dict(
    kind="challenge",
    id="act-lookup",
    title="A Book of Actions",
    level="advanced",
    variant_of="reply-lookup",
    optional=True,
    minutes=10,
    support="light",
    summary="The advanced twin of Four Branches, One Lookup: a dictionary of functions, `actions[choice](hero)`, "
            "and `False` for an unknown choice.",
    martu=(
        "The advanced refactor. In the campaign, a spell held its function in a dictionary: "
        "`spell[\"spell_function\"](caster)`. Now you build a book like that.\n"
        "Make `actions`: each option as a key, and its function as the value, with no `()`. Then `act` looks the "
        "function up and calls it, `actions[choice](hero)`, and hands back `True`. For a choice `actions` doesn't "
        "have, it hands back `False`, and leaves the hero alone.\n"
        "```text\nact(\"option 2\", lucky) → True\n  (mana 5 → 8)\nact(\"option 1\", lucky) → True\n"
        "  (mana 8 → 26)\nact(\"option 7\", lucky) → False\n```\n"
        "Then my hidden tests swap in other functions, yes?"
    ),
    names=["actions", "act", "choice", "hero"],
    setup=ACT_FUNCS,
    starter=ACT_STARTER,
    checkpoints=[
        dict(
            id="make-actions",
            text="Above `def act`, make the dictionary `actions`: each option as a key, and its function as the "
                 "value, with no `()`.",
            dictated=False,
            hints=[
                "Read the `elif` chain: `choice == \"option 1\"` gives you a key, and the function called under it "
                "gives you its value.",
                "A function's name with no `()` is the function itself, like any value. With other names: `tunes = "
                "{\"a\": hum}` stores `hum`. `{\"a\": hum()}` would run it now and store `None`.",
                "Write `actions = {` above `def act`, then one pair a line, like `\"option 1\": rest,`, then `}`.",
            ],
            checks=[ACT_KEEP, ACTIONS_CHECK],
            pass_line="Bomb Shell: Book written. Four spells. No brackets.",
        ),
        dict(
            id="use-actions",
            text="Make `act` call `actions[choice](hero)` in place of the `elif` chain, then hand back `True`. Rows "
                 "1 and 2 must still pass.",
            dictated=False,
            hints=[
                "Inside `act`, the four questions go. One lookup finds the function, and `(hero)` on the end calls "
                "it.",
                "`tunes[\"a\"]` finds `hum` but does not run it. `tunes[\"a\"](moth)` finds it and runs it on "
                "`moth`: the brackets on the end are what call it.",
                "Write `actions[choice](hero)`, then `return True` on the next line. Above them, at the top of "
                "`act`, add the guard row 3 needs, or its print stops Python with a KeyError: `if choice not in "
                "actions:` with `return False` under it.",
            ],
            checks=[
                ACT_CHAIN_CHECK,
                act_row(("v", 1, '`act("option 2", lucky)`', "hand back `True` and take the mana from 5 to 8", ""),
                        "option 2", _sheet(5), True, _sheet(8)),
                act_row(("v", 2, '`act("option 1", lucky)`', "hand back `True` and take the mana from 8 to 26", ""),
                        "option 1", _sheet(8), True, _sheet(26)),
            ],
            pass_line="Mar'tu: `actions[choice](hero)`. You read that in the campaign. Now you wrote it, yes?",
        ),
        dict(
            id="unknown-choice",
            text="Make row 3 pass: for a choice `actions` does not have, hand back `False` and leave the hero alone.",
            dictated=False,
            hints=[
                "Run row 3. `actions[\"option 7\"]` stops Python with a KeyError: there is no such key.",
                "Ask first, then act. A guard at the top, `if key not in tunes:` with `return False` under it, "
                "stops the function before the lookup.",
                "At the top of `act`, write `if choice not in actions:` with `return False` under it.",
            ],
            checks=[act_row(("v", 3, '`act("option 7", lucky)`', "hand back `False` and leave the mana at 26", ""),
                            "option 7", _sheet(26), False, _sheet(26))],
            pass_line="Oogrish: An unknown order, and nobody moves. Steady, now.",
        ),
        dict(
            id="hidden-tests",
            text="Pass Mar'tu's hidden tests: each option, a new action, another hero, and odd choices.",
            dictated=False,
            hints=[
                "The hidden tests put other functions in `actions`, add a fifth option, and hand over other "
                "heroes. Read everything from `actions` and `hero`.",
                "Use only `choice` and `hero` inside `act`: `lucky` is one hero from the table, and the tests hand "
                "over others.",
                "Keep `actions[choice](hero)` and `return True` under the guard.",
            ],
            checks=[
                ACT_EVERY,
                act_row(("h", "a new action added to `actions`"), "option 5", _sheet(9, 20), True, None, rec=True,
                        extra="option 5"),
                act_row(("h", "another hero"), "option 3", _sheet(9, 12, name="Pell"), True,
                        _sheet(7, 12, name="Pell")),
                act_row(("h", "a choice with a capital letter"), "Option 1", _sheet(4, 12), False, _sheet(4, 12)),
                act_row(("h", "an empty choice"), "", _sheet(4, 12), False, _sheet(4, 12)),
            ],
            pass_line="Mar'tu: A book of spells, and one line to cast any of them. The barrier will hold, yes?",
        ),
    ],
    solution=ACT_SOLUTION,
    partials=[ACT_PARTIAL],
    assemble=dict(
        lines=lines_of(ACTIONS_DICT + ACT_NEW),
        distractors=['    "option 1": rest(),', "    actions[choice]", "    return actions[choice](hero)"],
    ),
    another_way=[
        dict(angle="picture", label="A book of recipe cards", text=(
            "```text\nactions[\"option 2\"]\n  → glug   (the card)\nactions[\"option 2\"](lucky)\n  → glug runs "
            "on Lucky\n```\nThe lookup hands you the card. The brackets on the end cook it.")),
        dict(angle="step-by-step", text=(
            "1. Guard: `if choice not in actions:` → `return False`.\n2. Look up the function: "
            "`actions[choice]`.\n3. Call it on the hero: add `(hero)`.\n4. `return True`.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`cast_spell` read `spell[\"spell_function\"](caster)`: a dictionary holding a function, called with "
            "the brackets on the end. `actions[choice](hero)` is the same shape, one level up.")),
    ],
    predict=dict(
        q="Before you write it: what do these lines print?",
        code=(
            "def hum(sheet):\n"
            '    print(sheet["name"], "hums.")\n'
            "\n\n"
            'tunes = {"a": hum}\n'
            'tunes["a"]\n'
            'print("...")\n'
            'tunes["a"]({"name": "Moth"})\n'
        ),
        choices=["Moth hums.\n...\nMoth hums.", "...\nMoth hums.", "...\nhum"],
        answer=1,
        explain=(
            "`tunes[\"a\"]` alone finds the function and does nothing with it. Only `tunes[\"a\"](...)`, with the "
            "brackets on the end, runs it."
        ),
    ),
    pair_talk="Tell your partner the difference between `actions[choice]` and `actions[choice](hero)`.",
    campaign_link=dict(
        module=MODULE,
        part="hold-the-barrier",
        snippet='spell["spell_function"](caster)',
        why=(
            "You called this in `cast_spell`: the spell's page held a function, and the brackets on the end called "
            "it on the caster. `actions[choice](hero)` builds that book yourself."
        ),
    ),
    takeaway="A dictionary can hold functions. `actions[choice]` finds one; `(hero)` on the end calls it.",
    wrong_answers=[
        dict(why="the starter (the elif chain, no dictionary yet)", code=ACT_STARTER, fails_at=1,
             message_contains="Make the dictionary `actions`"),
        dict(why="the dictionary made, the chain still in act (the partial)", code=ACT_PARTIAL, fails_at=2,
             message_contains="Replace the `elif` chain"),
        dict(why="Show me how (CP1), pasted word for word: one pair, the rest named in words; no crash, CP1 asks for "
                 "the other options", code=_actc('actions = {\n    "option 1": rest,\n}\n\n\n' + ACT_CHAIN),
             fails_at=1, message_contains="all four options as keys"),
        dict(why="rest() stored with brackets: Python's TypeError where the dictionary is made",
             code=_actc(ACTIONS_DICT.replace("rest,", "rest(),") + "\n\n" + ACT_NEW), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="rest(hero) stored: no hero yet, Python's NameError",
             code=_actc(ACTIONS_DICT.replace("rest,", "rest(hero),") + "\n\n" + ACT_NEW), fails_at=0,
             message_contains="name 'hero' is not defined"),
        dict(why="each action run on lucky and its None stored (the dictionary made after lucky)",
             code=ACT_HEAD + ACT_FUNCS + "\n\n" + ACT_NEW + '\n\nlucky = {"mana": 5, "max_mana": 26}\n'
             + ACTIONS_DICT.replace("rest,", "rest(lucky),").replace("glug,", "glug(lucky),")
             .replace("glow,", "glow(lucky),").replace("ward,", "ward(lucky),"), fails_at=1,
             message_contains="holds `None`"),
        dict(why="the names in quotes: the bottom prints stop with Python's TypeError",
             code=_actc(ACTIONS_DICT.replace("rest,", '"rest",').replace("glug,", '"glug",')
                        .replace("glow,", '"glow",').replace("ward,", '"ward",') + "\n\n" + ACT_NEW), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="the names in quotes, the prints gone: Mar'tu's message",
             code=_actc(ACTIONS_DICT.replace("rest,", '"rest",').replace("glug,", '"glug",')
                        .replace("glow,", '"glow",').replace("ward,", '"ward",') + "\n\n" + ACT_NEW, table=""),
             fails_at=1, message_contains="Take the quotes off `rest`"),
        dict(why="two functions matched to the wrong options",
             code=_actc(ACTIONS_DICT.replace('"option 1": rest', '"option 1": glug')
                        .replace('"option 2": glug', '"option 2": rest') + "\n\n" + ACT_NEW), fails_at=1,
             message_contains="its own function"),
        dict(why="keys and values swapped (functions as keys)",
             code=_actc("actions = {\n    rest: \"option 1\",\n    glug: \"option 2\",\n    glow: \"option 3\",\n"
                        "    ward: \"option 4\",\n}\n\n\n" + ACT_NEW, table=""), fails_at=1,
             message_contains="on the left of each `:`"),
        dict(why="an action changed (glug gives 5)",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW).replace('hero["mana"] + 3', 'hero["mana"] + 5'), fails_at=1,
             message_contains="Leave `glug` as it is"),
        dict(why="the function looked up but never called (no (hero))",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("actions[choice](hero)", "actions[choice]")),
             fails_at=2, message_contains="Add `(hero)` on the end"),
        dict(why="the function itself handed back, not True",
             code=_actc(ACTIONS_DICT + "\n\ndef act(choice, hero):\n    if choice not in actions:\n"
                                       "        return False\n    return actions[choice]\n"), fails_at=2,
             message_contains="handed back the function itself"),
        dict(why="actions[choice]() with no hero: the bottom prints stop with Python's TypeError",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("(hero)\n    return", "()\n    return")), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="actions[choice]() with no hero, the prints gone: Mar'tu's message",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("(hero)\n    return", "()\n    return"), table=""),
             fails_at=2, message_contains="Hand over the hero"),
        dict(why="return actions[choice](hero): the action's own None comes back",
             code=_actc(ACTIONS_DICT + "\n\ndef act(choice, hero):\n    if choice not in actions:\n"
                                       "        return False\n    return actions[choice](hero)\n"), fails_at=2,
             message_contains="Call it on one line, then `return True`"),
        dict(why="no guard: the bottom prints stop with Python's KeyError",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NO_GUARD), fails_at=0, message_contains="KeyError: 'option 7'"),
        dict(why="no guard, the prints gone: Mar'tu's message",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NO_GUARD, table=""), fails_at=3, message_contains="Ask first"),
        dict(why='an unknown choice returns "False" in quotes',
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("return False", 'return "False"')), fails_at=3,
             message_contains="no quotes"),
        dict(why="an unknown choice returns None (a bare return)",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("return False", "return")), fails_at=3,
             message_contains="hands back `None`"),
        dict(why="the action called twice",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("    actions[choice](hero)\n",
                                                                "    actions[choice](hero)\n    actions[choice](hero)\n")),
             fails_at=2, message_contains="Call the action once"),
        dict(why="the global lucky used, not the parameter",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("actions[choice](hero)", "actions[choice](lucky)")),
             fails_at=2, message_contains="Use the parameter `hero`, not `lucky`"),
        dict(why='the parameter quoted, actions["choice"], the prints gone',
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("actions[choice](hero)", 'actions["choice"](hero)'),
                        table=""), fails_at=2, message_contains='Take the quotes off `"choice"`'),
        dict(why="a copy of the dictionary inside act (passes the table; the hidden recorders catch it)",
             code=_actc(ACTIONS_DICT + "\n\ndef act(choice, hero):\n    book = {\n        \"option 1\": rest,\n"
                                       "        \"option 2\": glug,\n        \"option 3\": glow,\n"
                                       "        \"option 4\": ward,\n    }\n    if choice not in actions:\n"
                                       "        return False\n    book[choice](hero)\n    return True\n"), fails_at=4,
             message_contains="Read the function from `actions` itself"),
        dict(why="the table typed as sheet changes behind `in` questions, `actions` only asked about (passes rows "
                 "1-3; the hidden recorders catch it)",
             code=_actc(ACTIONS_DICT + "\n\ndef act(choice, hero):\n    if choice not in actions:\n"
                                       "        return False\n    if choice in [\"option 2\"]:\n"
                                       "        hero[\"mana\"] = 8\n    if choice in [\"option 1\"]:\n"
                                       "        hero[\"mana\"] = 26\n    return True\n"), fails_at=4,
             message_contains="Read the function from `actions` itself"),
        dict(why="a default action for an unknown choice, `actions.get(choice, rest)(hero)` (row 3's hero is already "
                 "full, so only the hidden tests show it)",
             code=_actc(ACTIONS_DICT + "\n\ndef act(choice, hero):\n    actions.get(choice, rest)(hero)\n"
                                       "    return choice in actions\n"), fails_at=4,
             message_contains="and the hero changed"),
        dict(why="the choice lowered first (a refactor must keep the old answers)",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("def act(choice, hero):\n",
                                                                "def act(choice, hero):\n    choice = choice.lower()\n")),
             fails_at=4, message_contains="no `.lower()`"),
        dict(why="print instead of return",
             code=_actc(ACTIONS_DICT + "\n\n" + ACT_NEW.replace("    return True\n", "    print(True)\n")),
             fails_at=2, message_contains="Use `return`, not `print`"),
    ],
    notes=(
        meta(starter_level="refactor (a working elif chain)", path="TRIALS", set="Functions (advanced)",
             trial="T-F-3a", variant_of="reply-lookup", opens="after Unit 7", ceiling="Units 1-7",
             skills="func-as-value,call-stored-func,dict-lookup,not-in-guard,refactor", solo="false", dictates="",
             foreign_names="tunes,hum,moth,key",
             par="every option through the dictionary (Mar'tu's recorders in place of the four actions); a new "
                 "action added (option 5); another hero (Pell, 9 of 12); a capital letter; an empty choice") + "\n"
        "T-F-3a, variant_of reply-lookup (the spec: 'A dict of functions: actions[choice](hero). An unknown choice "
        "-> False'). Known choices return True (the spec names only the unknown answer; the chain the student "
        "refactors returns True after an action, so the behaviour is kept). CP1 the dictionary of functions (NOP: "
        "`None` from `rest(lucky)`, `\"rest\"` quoted, the wrong function each named; `rest()` and `rest(hero)` "
        "are Python's own errors where the dictionary is made), CP2 the stored call (the brief's 'not calling it at "
        "all': `actions[choice]` alone, `return actions[choice]`, `actions[choice]()`), CP3 the guard (KeyError), "
        "CP4 hidden: Mar'tu's recorders are put into `actions` in place of the student's functions, so the call "
        "must go through the dictionary, once, on the hero handed in (a copy of the dictionary inside `act` passes "
        "the table and fails here). The setup repeats the four finished actions so the Assemble lines run on "
        "their own. Show-rung copy-test (Nov 14 rule): CP2's rung used to be the call and `return True` alone; "
        "pasted, the starter's row-3 print stopped Python with a KeyError (no partial is possible there: CP2's "
        "lookup cannot pass while row 3's print has no guard). So CP2's rung now names the guard row 3 needs and "
        "gives it above the call (`if choice not in actions:` with `return False` under it): the solution, no "
        "crash. CP3's rung on top keeps it, CP4's too. CP1's rung as written gives one pair and names the rest in "
        "words: no crash, CP1 asks for the other options (its wrong answer). Predict answer index 1."
    ),
)


# =============================================================================================
# T-Own "Write Your Own Checks": 4 asserts that would catch a wrong can_cast (core; prerequisite card 2-A2)
# =============================================================================================


def seal_keep_check(target, src, line):
    return check(f"{target} is left as Mar'tu wrote it", f"_FN = {target!r}\n_seal_keep({target!r}, {src!r}, {line!r})\n")


def seal_count_check(target, need):
    return check(f"{need} seals that call {target}", f"_FN = {target!r}\n_seal_count({target!r}, {need})\n")


SEAL_SAYS = check("each seal says True or False", "_FN = 'can_cast'\n_seal_says()\n")


def seal_row(target, body, where, msg, diag=""):
    """One wrong copy of the function. The student's whole program runs again with the copy's steps; one of the
    seals must stop it (AssertionError). diag: check code that may set a sharper message `_m`."""
    code = (
        _head(target, where)
        + f"_res = _seal_run({target!r}, {body!r})\n"
        + "if _res == 'through':\n"
        + f"    _m = {msg!r}\n"
        + "".join("    " + line + "\n" for line in diag.splitlines())
        + "    assert False, _m + ' ' + _evs(None, 'it got through every seal')\n"
    )
    return check(_check_name(where), code)


SEAL_DEF = "def can_cast(mana, cost):\n    return mana >= cost\n"
SEAL_HEAD = (
    "# Trial: write your own checks.\n"
    "# This can_cast is right.\n"
    "# Leave it as it is.\n"
    "# If Python stops at a seal, mend\n"
    "# the seal, not can_cast.\n"
    + SEAL_DEF
    + "\n\n# Write 4 seals here. Each one\n"
    "# calls can_cast and says what it\n"
    "# must hand back: True or False.\n"
)
SEAL_TAIL = '\n\nprint("Every seal held.")\n'
SEAL_GOOD = [
    "assert can_cast(20, 10) == True",
    "assert can_cast(10, 10) == True",
    "assert can_cast(9, 10) == False",
    "assert can_cast(2, 10) == False",
]


def _seal(seals=(), head=SEAL_HEAD):
    return head + "".join(line + "\n" for line in seals) + SEAL_TAIL


SEAL_STARTER = _seal()
SEAL_SOLUTION = _seal(SEAL_GOOD)
SEAL_LINE = ": `return mana >= cost`"

SEAL_CAN_CAST = dict(
    kind="challenge",
    id="seal-can-cast",
    title="Write Your Own Checks",
    level="core",
    optional=True,
    minutes=8,
    support="light",
    summary="Turn the table round: write 4 seals that pass on Mar'tu's `can_cast` and stop every wrong copy of it.",
    martu=(
        "Every check in the campaign was a seal: an [[assert]] with a message. When a check like `exactly enough "
        "mana still casts` failed, you read its message. Now you write the seals.\n"
        "My `can_cast` is right. Write 4 seals that pass on it. Then my test swaps in wrong copies of "
        "`can_cast`, and each copy must stop at one of your seals with an [[AssertionError]].\n"
        "```text\nrow 1: a copy with mana > cost\nrow 2: a copy that always\n       says True\n```\n"
        "A seal is `assert`, then a question: `True` lets the program go on, `False` stops it. If Python stops "
        "at one of your seals now, that seal asks the wrong question, yes?"
    ),
    names=["can_cast"],
    starter=SEAL_STARTER,
    checkpoints=[
        dict(
            id="four-seals",
            text="Write 4 `assert` lines that call `can_cast` and say what it must hand back. They must all pass.",
            dictated=False,
            hints=[
                "Pick 4 cases: plenty of mana, exactly enough, one short, and far too little. For each one, what "
                "must `can_cast` hand back?",
                "A seal with other names: `assert is_full(20, 20) == True` stops the program if `is_full` says "
                "anything but `True` there.",
                "Write `assert can_cast(10, 10) == True` for exactly enough. Then one for plenty, one for one "
                "short, and one for far too little.",
            ],
            checks=[seal_keep_check("can_cast", SEAL_DEF, SEAL_LINE), seal_count_check("can_cast", 4), SEAL_SAYS],
            pass_line="Mar'tu: Four seals, and every one holds. Now let us try to break them.",
        ),
        dict(
            id="visible-copies",
            text="Make your seals stop the two wrong copies in the table.",
            dictated=False,
            hints=[
                "Row 1 uses `>`: it is wrong only when the mana and the cost are the same. Row 2 always says "
                "`True`: it is wrong only when the mana is too low.",
                "A seal catches a copy when the copy gives a different answer from Mar'tu's. `is_full` with `>` "
                "says `False` at 20 and 20, so `assert is_full(20, 20) == True` stops it.",
                "Keep `assert can_cast(10, 10) == True` for row 1, and a seal like `assert can_cast(2, 10) == "
                "False` for row 2.",
            ],
            checks=[
                seal_row("can_cast", "    return mana > cost\n",
                         ("v", 1, "a copy with `mana > cost`", "stop at one of your seals", ""),
                         "Add a seal at the edge, where the mana and the cost are the same, that must be `True`: this "
                         "copy says `False` there."),
                seal_row("can_cast", "    return True\n",
                         ("v", 2, "a copy that always says `True`", "stop at one of your seals", ""),
                         "Add a seal where the mana is too low, that must be `False`: this copy says `True` to "
                         "everything."),
            ],
            pass_line="Bomb Shell: Two bad copies. Both stopped.",
        ),
        dict(
            id="hidden-copies",
            text="Stop Mar'tu's hidden copies too.",
            dictated=False,
            hints=[
                "Each hidden copy is wrong in one place. Read its label, then ask: which of my seals would it fail?",
                "Seal both sides of the edge: exactly enough must be `True`, and one short must be `False`. Use "
                "numbers where the mana and the cost differ, too.",
                "Add `assert can_cast(9, 10) == False`, one short of the cost.",
            ],
            checks=[
                seal_row("can_cast", "    return False\n", ("h", "a copy that always says False"),
                         "Add a seal with enough mana, that must be `True`: this copy says `False` to everything."),
                seal_row("can_cast", "    return mana >= cost - 1\n", ("h", "a copy that lets one short through"),
                         "Add a seal one mana short of the cost, that must be `False`: this copy lets one short "
                         "through."),
                seal_row("can_cast", "    return cost >= mana\n", ("h", "a copy with mana and cost swapped"),
                         "Add a seal where the mana and the cost are different numbers: this copy reads them the "
                         "other way round."),
                seal_row("can_cast", "    return mana <= cost\n", ("h", "a copy with the sign turned round"),
                         "Add a seal with plenty of mana, that must be `True`, and one with too little, that must be "
                         "`False`."),
                seal_row("can_cast", '    if mana >= cost:\n        return "True"\n    return "False"\n',
                         ("h", "a copy that hands back text"),
                         "Compare with `True` or `False` in your seals: this copy hands back the text \"True\" or "
                         "\"False\", and `assert` counts any text as a yes."),
                seal_row("can_cast", "    print(mana >= cost)\n", ("h", "a copy that prints and hands back nothing"),
                         "Add a seal that must be `True`, with `== True`: this copy prints its answer and hands back "
                         "`None`."),
            ],
            pass_line="Mar'tu: Every copy stopped. That is a strong seal, yes?",
        ),
    ],
    solution=SEAL_SOLUTION,
    partials=[
        _seal(["assert can_cast(20, 10) == True", "assert can_cast(15, 10) == True",
               "assert can_cast(2, 10) == False", "assert can_cast(5, 10) == False"]),
        _seal(["assert can_cast(20, 10) == True", "assert can_cast(10, 10) == True",
               "assert can_cast(2, 10) == False", "assert can_cast(5, 10) == False"]),
    ],
    assemble=dict(
        lines=lines_of(SEAL_DEF) + SEAL_GOOD,
        distractors=["assert can_cast(10, 10) == False", 'assert can_cast(20, 10) == "True"',
                     "assert can_cast(10, 20) == True"],
    ),
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky: \"The campaign's checks had messages. Mine should too.\" Give every seal a message, the way "
            "the campaign did: after the question, a comma, then text in quotes, like `exactly enough`."
        ),
        hints=[
            "A message goes after the question: `assert is_full(20, 20) == True, \"full at the top\"`.",
            "Write `assert can_cast(10, 10) == True, \"exact\"`, and a message on each of the other seals.",
        ],
        checks=[check("every seal has a message", (
            "_out = _seal_list()[0]\n"
            "assert _out, 'Write your seals first, then give each one a message.'\n"
            "_no = [_a for _a in _out if _a.msg is None or not (_tn(_a.msg) == 'JoinedStr' or (_tn(_a.msg) == "
            "'Constant' and _tn(_a.msg.value) == 'str' and _a.msg.value.strip()))]\n"
            "assert not _no, ('Give every seal a message: after the question, a comma and some text in quotes, like '"
            "'the campaign\\'s checks.')\n"
        ))],
        solution=_seal(["assert can_cast(20, 10), \"plenty\"", "assert can_cast(10, 10), \"exact\"",
                        "assert not can_cast(9, 10), \"short\"", "assert not can_cast(2, 10), \"broke\""]),
    ),
    another_way=[
        dict(angle="picture", label="Seals on a number line", text=(
            "```text\ncost 10:\n  2     9  10     20\n  no    no yes    yes\n        ^   ^\n      the edge\n```\nThe "
            "two seals around the edge do the most work: `>` breaks one, and one short breaks the other.")),
        dict(angle="step-by-step", text=(
            "1. Plenty of mana: `True`.\n2. Exactly enough: `True`.\n3. One short: `False`.\n4. Far too little: "
            "`False`.\nWrite one `assert` for each, with `== True` or `== False`.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The barrier part checked `cast_spell` with lines like `exactly enough mana still casts`. Each was a "
            "seal at the edge. You are writing those checks now, the other way round.")),
    ],
    predict=dict(
        q="Before you write the seals: what does this print?",
        code="def is_full(mana, top):\n    return mana > top\n\n\nprint(is_full(30, 20))\nprint(is_full(20, 20))\n",
        choices=["True\nTrue", "False\nFalse", "True\nFalse"],
        answer=2,
        explain=(
            "`>` says no at exactly 20. That is a quiet bug: no error, just a wrong `False`. A seal at the edge, "
            "`assert is_full(20, 20) == True`, would make it loud."
        ),
    ),
    pair_talk="Swap seals with your partner and look for a wrong `can_cast` that would get past theirs. Then each "
              "of you mends your own seals, on your own screen.",
    campaign_link=dict(
        module=MODULE,
        part="hold-the-barrier",
        why=(
            "The barrier part's checks, like `exactly enough mana still casts`, were seals Mar'tu wrote for your "
            "`cast_spell`. When one failed, its message was what you read. Now you write the seals, and the "
            "messages."
        ),
    ),
    takeaway="A strong seal sits on the edge, on both sides, and says `True` or `False`. A wrong copy must fail one.",
    wrong_answers=[
        dict(why="the starter (no seals yet)", code=SEAL_STARTER, fails_at=1, message_contains="Write your seals"),
        dict(why="only 3 seals", code=_seal(SEAL_GOOD[:3]), fails_at=1, message_contains="4 seals in all"),
        dict(why="Show me how (CP1), pasted word for word: the exact seal, the other three named in words; no crash",
             code=_seal(["assert can_cast(10, 10) == True"]), fails_at=1, message_contains="you have 1"),
        dict(why="Show me how, all three rungs pasted (the exact, too-low and one-short seals; the plenty seal is "
                 "named in words): no crash",
             code=_seal(["assert can_cast(10, 10) == True", "assert can_cast(2, 10) == False",
                         "assert can_cast(9, 10) == False"]), fails_at=1, message_contains="you have 3"),
        dict(why="4 asserts, but two are copies of the other two",
             code=_seal(SEAL_GOOD[1:3] + SEAL_GOOD[1:3]), fails_at=1, message_contains="4 different seals"),
        dict(why="a seal that never calls can_cast", code=_seal(SEAL_GOOD[:3] + ["assert 10 >= 10"]), fails_at=1,
             message_contains="call `can_cast`"),
        dict(why="the question copied into each seal (it repeats the function's own sign)",
             code=_seal(["assert can_cast(20, 10) == (20 >= 10)", "assert can_cast(10, 10) == (10 >= 10)",
                         "assert can_cast(9, 10) == (9 >= 10)", "assert can_cast(2, 10) == (2 >= 10)"]),
             fails_at=1, message_contains="repeats Mar'tu's question"),
        dict(why='"True" in quotes: the seal fails on the right function (AssertionError)',
             code=_seal(['assert can_cast(20, 10) == "True"'] + SEAL_GOOD[1:]), fails_at=0,
             message_contains="AssertionError"),
        dict(why="mana and cost read the wrong way round (the table read backwards): AssertionError",
             code=_seal(["assert can_cast(10, 20) == True"] + SEAL_GOOD[1:]), fails_at=0,
             message_contains="AssertionError"),
        dict(why="can_cast changed to > to fit the seals",
             code=_seal(["assert can_cast(20, 10) == True", "assert can_cast(10, 10) == False",
                         "assert can_cast(9, 10) == False", "assert can_cast(2, 10) == False"],
                        head=SEAL_HEAD.replace("mana >= cost", "mana > cost")), fails_at=1,
             message_contains="Put `can_cast` back"),
        dict(why="weak seals: no seal at the edge (the partial; the > copy gets through)",
             code=_seal(["assert can_cast(20, 10) == True", "assert can_cast(15, 10) == True",
                         "assert can_cast(2, 10) == False", "assert can_cast(5, 10) == False"]), fails_at=2,
             message_contains="at the edge"),
        dict(why="weak seals: every seal says True (the always-True copy gets through)",
             code=_seal(["assert can_cast(20, 10) == True", "assert can_cast(10, 10) == True",
                         "assert can_cast(30, 10) == True", "assert can_cast(11, 10) == True"]), fails_at=2,
             message_contains="too low"),
        dict(why="weak seals: no seal one short (the partial; the one-short copy gets through)",
             code=_seal(["assert can_cast(20, 10) == True", "assert can_cast(10, 10) == True",
                         "assert can_cast(2, 10) == False", "assert can_cast(5, 10) == False"]), fails_at=3,
             message_contains="one mana short"),
        dict(why="weak seals: never == True or == False (the text copy gets through)",
             code=_seal(["assert can_cast(20, 10)", "assert can_cast(10, 10)", "assert can_cast(9, 10) != True",
                         "assert can_cast(2, 10) != True"]), fails_at=3, message_contains="hands back the text"),
        dict(why="the seals inside a function that is never called",
             code=_seal(["def seal():"] + ["    " + line for line in SEAL_GOOD]), fails_at=1,
             message_contains="at the top level"),
        dict(why="= instead of == in a seal", code=_seal(["assert can_cast(10, 10) = True"] + SEAL_GOOD[2:]),
             fails_at=0, message_contains="invalid syntax"),
    ],
    notes=(
        meta(starter_level="S2", path="TRIALS", set="T-Own", trial="T-Own", opens="after Unit 7",
             ceiling="Units 1-7 + card 2-A2", prereq="2-A2 Mar'tu's Seal (u02c, optional): recap in the Learn pane",
             skills="assert,boundary,read-check-message,test-design", solo="false", dictates="",
             foreign_names="is_full,top",
             par="wrong copies: always False; one short let through; mana and cost swapped; the sign turned round; "
                 "text answers; print and no return") + "\n"
        "T-Own (the spec: 'Write 4 assert lines that would catch a wrong can_cast'). The table turned round: the "
        "student writes the rows, and the trial's rows are wrong copies of can_cast. Each copy reruns the "
        "student's whole program in a fresh namespace with can_cast's steps swapped (the def is kept, so seals "
        "that read variables made from calls still work); a seal must raise AssertionError. A seal that fails on "
        "Mar'tu's own function crashes the student's run first: the explainer's 'Your assert caught something' "
        "row, and the Learn pane says Mar'tu's can_cast is right, so that seal asks the wrong question. Weak seals "
        "(the brief's slip) each fail on the copy that gets past them, with the case to add. A seal that repeats "
        "the question (`== (10 >= 10)`) is refused, as in 2-A2's try-it. `assert can_cast(...)` and `assert not "
        "can_cast(...)` count as saying the answer. Lucky's side quest adds messages (T-Own's campaign link: "
        "reading check messages). Teacher ruling (Nov 14): the starter adds, under \"# Leave it as it is.\", the "
        "two lines \"# If Python stops at a seal, mend\" / \"# the seal, not can_cast.\", so an AssertionError on the "
        "student's own run points at the seal. Predict answer index 2. Show-rung copy-test: every rung is seals "
        "that pass on Mar'tu's can_cast (no crash); the rest is named in words, so pasted alone they stop at "
        "CP1's count (wrong answers: CP1's one seal; all three rungs' three seals). Bonus rung: one seal with a "
        "message, no crash."
    ),
)


# =============================================================================================
# T-Own-a "Seal the Barrier": seals that catch the `<=` slip in a given cast_ok and pass the correct one
# (advanced, variant_of seal-can-cast)
# =============================================================================================

OK_DEF = (
    "def cast_ok(mana, cost, affinity, required):\n"
    "    if affinity < required:\n"
    "        return False\n"
    "    if mana < cost:\n"
    "        return False\n"
    "    return True\n"
)
OK_HEAD = (
    "# Trial: seal the barrier.\n"
    "# Mar'tu's cast_ok is right.\n"
    "# Leave it as it is.\n"
    "# If Python stops at a seal, mend\n"
    "# the seal, not cast_ok.\n"
    + OK_DEF
    + "\n\n# Bomb Shell's copy had one slip:\n"
    "#     if mana <= cost:\n"
    "# Write seals that pass here, and\n"
    "# would stop his copy.\n"
)
OK_GOOD = [
    "assert cast_ok(9, 9, 8, 8) == True",
    "assert cast_ok(8, 9, 8, 8) == False",
    "assert cast_ok(9, 5, 8, 8) == True",
    "assert cast_ok(9, 5, 7, 8) == False",
]


def _okc(seals=(), head=OK_HEAD):
    return head + "".join(line + "\n" for line in seals) + SEAL_TAIL


OK_STARTER = _okc()
OK_SOLUTION = _okc(OK_GOOD)


def _ok_body(skill="<", mana="<", cost="cost"):
    return (f"    if affinity {skill} required:\n        return False\n    if mana {mana} {cost}:\n"
            "        return False\n    return True\n")


OK_MANA_MASK = (
    "_ex = [_a for _a, _w in _lits('cast_ok') if _B.len(_a) == 4 and _a[0] == _a[1]]\n"
    "if _ex and _B.all(_a[2] < _a[3] for _a in _ex):\n"
    "    _m = ('Give your exact-mana seal enough skill too: with too little skill, `cast_ok` hands back `False` at "
    "the "
    "skill line, so it never reaches the mana line, where the slip is.')\n"
)
OK_SKILL_MASK = (
    "_ex = [_a for _a, _w in _lits('cast_ok') if _B.len(_a) == 4 and _a[2] == _a[3]]\n"
    "if _ex and _B.all(_a[0] < _a[1] for _a in _ex):\n"
    "    _m = ('Give your exact-skill seal enough mana too: with too little mana, both copies say `False`, so that "
    "seal cannot tell them apart.')\n"
)

SEAL_CAST_OK = dict(
    kind="challenge",
    id="seal-cast-ok",
    title="Seal the Barrier",
    level="advanced",
    variant_of="seal-can-cast",
    optional=True,
    minutes=10,
    support="light",
    summary="The advanced twin of Write Your Own Checks: seals that pass on Mar'tu's `cast_ok` and stop Bomb Shell's "
            "`<=` slip.",
    martu=(
        "The advanced seal, at the barrier. `cast_ok` asks two questions: enough skill, then enough mana. Bomb "
        "Shell copied it with one slip, `<=` on the mana line, so exactly enough mana fails.\n"
        "Write seals that pass on my `cast_ok` and stop Bomb Shell's copy. Careful: a seal with too little "
        "skill never reaches the mana line.\n"
        "```text\nrow 1: Bomb Shell's copy,\n       mana <= cost\nrow 2: a copy that always\n       says True\n```\n"
        "To watch a seal work, change `<` to `<=` on the mana line and Run. Python should stop at your seal. Then "
        "change it back, yes?"
    ),
    names=["cast_ok"],
    starter=OK_STARTER,
    checkpoints=[
        dict(
            id="seals",
            text="Write at least 3 `assert` lines that call `cast_ok` and say what it must hand back. They must all "
                 "pass.",
            dictated=False,
            hints=[
                "`cast_ok(mana, cost, affinity, required)` takes 4 numbers, in that order. Pick cases where you know "
                "the answer: enough of both, too little mana, too little skill.",
                "With other names: `assert pass_gate(5, 5, 3, 3) == True` seals a gate check with exactly enough "
                "of both.",
                "Write `assert cast_ok(9, 9, 8, 8) == True`, exactly enough of both. Then seals for too little "
                "mana and too little skill.",
            ],
            checks=[seal_keep_check("cast_ok", OK_DEF, ", with `<` on both lines"), seal_count_check("cast_ok", 3),
                    check("each seal says True or False", "_FN = 'cast_ok'\n_seal_says()\n")],
            pass_line="Gearshift: Seals hold on the right one. Visor dims.",
        ),
        dict(
            id="bomb-shells-copy",
            text="Make your seals stop row 1, Bomb Shell's copy, and row 2.",
            dictated=False,
            hints=[
                "Bomb Shell's copy is wrong only when the mana and the cost are the same *and* the skill is enough. "
                "Then it says `False`, and Mar'tu's says `True`.",
                "`cast_ok` asks about skill first. With too little skill, it hands back `False` before the mana "
                "line, so that seal can't see the slip.",
                "Keep `assert cast_ok(9, 9, 8, 8) == True`: exactly enough mana, and enough skill.",
            ],
            checks=[
                seal_row("cast_ok", _ok_body(mana="<="), ("v", 1, "Bomb Shell's copy, `mana <= cost`",
                                                           "stop at one of your seals", ""),
                         "Add a seal with exactly enough mana, and enough skill, that must be `True`: Bomb Shell's "
                         "copy says `False` there.", OK_MANA_MASK),
                seal_row("cast_ok", "    return True\n", ("v", 2, "a copy that always says `True`",
                                                          "stop at one of your seals", ""),
                         "Add a seal with too little mana or too little skill, that must be `False`: this copy says "
                         "`True` to everything."),
            ],
            pass_line="Bomb Shell: My copy. Stopped. Fair.",
        ),
        dict(
            id="hidden-copies",
            text="Stop Mar'tu's hidden copies too.",
            dictated=False,
            hints=[
                "Each hidden copy is wrong in one place: the skill line, the mana line, or how the two join. Read "
                "the label, then find the seal that would catch it.",
                "Seal each line from both sides: exactly enough must be `True`, and one short must be `False`. Give "
                "the other value plenty, so only one line decides.",
                "Add `assert cast_ok(9, 5, 7, 8) == False`: too little skill, and plenty of mana.",
            ],
            checks=[
                seal_row("cast_ok", _ok_body(skill="<="), ("h", "`<=` on the skill line"),
                         "Add a seal with exactly enough skill, and enough mana, that must be `True`.", OK_SKILL_MASK),
                seal_row("cast_ok", "    if mana < cost:\n        return False\n    return True\n",
                         ("h", "a copy that never checks skill"),
                         "Add a seal with too little skill, and plenty of mana, that must be `False`."),
                seal_row("cast_ok", "    if affinity < required:\n        return False\n    return True\n",
                         ("h", "a copy that never checks mana"),
                         "Add a seal with too little mana, and enough skill, that must be `False`."),
                seal_row("cast_ok", _ok_body(cost="cost - 1"), ("h", "a copy that lets one mana short through"),
                         "Add a seal one mana short of the cost, with enough skill, that must be `False`."),
                seal_row("cast_ok", "    return mana >= cost or affinity >= required\n",
                         ("h", "a copy that needs only one of the two"),
                         "Add a seal where only one of the two is enough, that must be `False`."),
                seal_row("cast_ok", ('    if affinity < required:\n        return "False"\n    if mana < cost:\n'
                                     '        return "False"\n    return "True"\n'),
                         ("h", "a copy that hands back text"),
                         "Compare with `True` or `False` in your seals: this copy hands back the text \"True\" or "
                         "\"False\", and `assert` counts any text as a yes."),
            ],
            pass_line="Mar'tu: The barrier is sealed from both sides. Bomb Shell owes you a latch, yes?",
        ),
    ],
    solution=OK_SOLUTION,
    partials=[
        _okc(["assert cast_ok(9, 5, 9, 8) == True", "assert cast_ok(5, 9, 9, 8) == False",
              "assert cast_ok(9, 5, 2, 8) == False"]),
        _okc(["assert cast_ok(9, 9, 9, 8) == True", "assert cast_ok(8, 9, 9, 8) == False",
              "assert cast_ok(9, 5, 9, 8) == True"]),
    ],
    assemble=dict(
        lines=lines_of(OK_DEF) + OK_GOOD,
        distractors=["assert cast_ok(9, 9, 2, 8) == True", "assert cast_ok(9, 9, 5, 8) == False",
                     "assert cast_ok(9, 9, 8, 8) == False"],
    ),
    another_way=[
        dict(angle="picture", label="Two doors in a row", text=(
            "```text\nseal → skill door → mana door → True\n       too low?     too low?\n       False        "
            "False\n```\nA seal stopped at the skill door never tests the mana door. To test the mana door, open "
            "the skill door first.")),
        dict(angle="step-by-step", text=(
            "1. For the mana line: enough skill, exactly enough mana: `True`.\n2. Enough skill, one mana short: "
            "`False`.\n3. For the skill line: plenty of mana, exactly enough skill: `True`.\n4. Plenty of mana, "
            "too little skill: `False`.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The barrier part said: \"Use `<` and not `<=`, because a caster with exactly enough mana can still "
            "cast.\" Bomb Shell's copy is that slip. Your seal is the check that catches it.")),
    ],
    predict=dict(
        q="Before you write the seals: what does this print?",
        code=(
            "def ok(mana, cost, skill, need):\n"
            "    if skill < need:\n"
            "        return False\n"
            "    if mana <= cost:\n"
            "        return False\n"
            "    return True\n"
            "\n\n"
            "print(ok(9, 9, 2, 8))\n"
            "print(ok(9, 9, 8, 8))\n"
        ),
        choices=["False\nFalse", "True\nTrue", "False\nTrue"],
        answer=0,
        explain=(
            "Both say `False`, but for different reasons. The first stops at the skill line and never reaches the "
            "mana line. The second reaches it, and `<=` says no to exactly enough. Only a seal like the second can "
            "catch the slip."
        ),
    ),
    pair_talk="Show your partner one seal that can see the mana line, and one that can't. Why can't it?",
    campaign_link=dict(
        module=MODULE,
        part="hold-the-barrier",
        snippet='elif caster["mana"] < spell["mana_cost"]:',
        why=(
            "The campaign said: use `<` and not `<=`, because a caster with exactly enough mana can still cast. Its "
            "check `exactly enough mana still casts` was a seal on that line. You just wrote one."
        ),
    ),
    takeaway="To seal one line, make every other line say yes: plenty of the other value, then the exact edge.",
    wrong_answers=[
        dict(why="the starter (no seals yet)", code=OK_STARTER, fails_at=1, message_contains="Write your seals"),
        dict(why="only 2 seals", code=_okc(OK_GOOD[:2]), fails_at=1, message_contains="3 seals in all"),
        dict(why="Show me how, every rung pasted word for word (the exact seal and the too-little-skill seal; the "
                 "too-little-mana seal is named in words): no crash",
             code=_okc(["assert cast_ok(9, 9, 8, 8) == True", "assert cast_ok(9, 5, 7, 8) == False"]), fails_at=1,
             message_contains="you have 2"),
        dict(why="the exact-mana seal hidden behind too little skill (Bomb Shell's copy gets through)",
             code=_okc(["assert cast_ok(9, 9, 5, 8) == False", "assert cast_ok(9, 5, 9, 8) == True",
                        "assert cast_ok(5, 9, 9, 8) == False"]), fails_at=2, message_contains="enough skill too"),
        dict(why="no exact-mana seal (the partial)",
             code=_okc(["assert cast_ok(9, 5, 9, 8) == True", "assert cast_ok(5, 9, 9, 8) == False",
                        "assert cast_ok(9, 5, 2, 8) == False"]), fails_at=2,
             message_contains="exactly enough mana, and enough skill"),
        dict(why="the mana line sealed, the skill line not (the partial)",
             code=_okc(["assert cast_ok(9, 9, 9, 8) == True", "assert cast_ok(8, 9, 9, 8) == False",
                        "assert cast_ok(9, 5, 9, 8) == True"]), fails_at=3,
             message_contains="exactly enough skill, and enough mana"),
        dict(why="the exact-skill seal hidden behind too little mana",
             code=_okc(["assert cast_ok(9, 9, 9, 8) == True", "assert cast_ok(8, 9, 9, 8) == False",
                        "assert cast_ok(5, 9, 8, 8) == False", "assert cast_ok(9, 5, 7, 8) == False"]), fails_at=3,
             message_contains="enough mana too"),
        dict(why="mana and cost read the wrong way round (the table read backwards): AssertionError",
             code=_okc(["assert cast_ok(10, 20, 9, 8) == True"] + OK_GOOD[1:]), fails_at=0,
             message_contains="AssertionError"),
        dict(why="the question copied into a seal",
             code=_okc(["assert cast_ok(9, 9, 8, 8) == (9 >= 9 and 8 >= 8)"] + OK_GOOD[1:]), fails_at=1,
             message_contains="repeats Mar'tu's question"),
        dict(why="a seal that never calls cast_ok", code=_okc(OK_GOOD[:2] + ["assert True"]), fails_at=1,
             message_contains="call `cast_ok`"),
        dict(why="Bomb Shell's <= left in cast_ok after trying it (the seals still let it through)",
             code=_okc(["assert cast_ok(9, 5, 9, 8) == True", "assert cast_ok(5, 9, 9, 8) == False",
                        "assert cast_ok(9, 5, 2, 8) == False"], head=OK_HEAD.replace("    if mana < cost:",
                                                                                         "    if mana <= cost:")),
             fails_at=1, message_contains="Put `cast_ok` back"),
        dict(why="Bomb Shell's <= left in cast_ok, and the seals catch it (Python stops: AssertionError)",
             code=_okc(OK_GOOD, head=OK_HEAD.replace("    if mana < cost:", "    if mana <= cost:")), fails_at=0,
             message_contains="AssertionError"),
    ],
    notes=(
        meta(starter_level="S2", path="TRIALS", set="T-Own (advanced)", trial="T-Own-a", variant_of="seal-can-cast",
             opens="after Unit 7", ceiling="Units 1-7 + card 2-A2", prereq="2-A2 Mar'tu's Seal (u02c, optional)",
             skills="assert,boundary,test-design,two-conditions", solo="false", dictates="",
             foreign_names="pass_gate,ok,skill,need",
             par="wrong copies: <= on the skill line; never checks skill; never checks mana; one mana short let "
                 "through; needs only one of the two (or); text answers") + "\n"
        "T-Own-a, variant_of seal-can-cast (the spec: 'Write asserts that catch the <= bug in a given cast_ok and "
        "pass the correct one'). The given cast_ok is Mar'tu's correct one (so the student's own run passes), and "
        "Bomb Shell's `<=` line is shown in a comment; the check swaps it in. The stricter spec: cast_ok asks about "
        "skill first, so a seal at exactly enough mana with too little skill never reaches the mana line (its own "
        "message, from the seal's literal numbers), and the hidden copies make the student seal the skill line "
        "from both sides too. The Learn pane invites a hands-on test (change `<` to `<=`, Run, see the seal stop "
        "Python, change it back); a student who leaves the `<=` in gets 'Put cast_ok back' or the seal's own "
        "AssertionError. The def line is the spec's four-parameter shape, kept whole (u08a's ruling). Starter: "
        "\"# If Python stops at a seal, mend\" / \"# the seal, not cast_ok.\" under \"# Leave it as it is.\" "
        "(Nov 14). Predict answer index 0, its distractors reordered. Show-rung copy-test: CP1's and CP3's rungs "
        "are seals that pass on Mar'tu's cast_ok (no crash; CP2's keeps CP1's); pasted alone they stop at CP1's "
        "count, the too-little-mana seal being named in words (its wrong answer)."
    ),
)


# =============================================================================================
# Cheatsheet "How to Read a Test Table"
# =============================================================================================

TABLE_SHEET = dict(
    kind="cheatsheet",
    id="read-a-test-table",
    title="How to Read a Test Table",
    summary="Mar'tu's chalk notes for the Trials: rows, edges, hidden labels, the evidence in brackets, and seals.",
    entries=[
        dict(concept="A row: a call, and what it should hand back",
             code="def seats_left(seats, guests):\n    return seats - guests\n\n\n# It should show 3.\n"
                  "print(seats_left(8, 5))\n",
             output="3",
             note="Read a row from left to right: the call is what goes in, and the comment above it says what "
                  "should come back. Run it, then put the line it shows next to the comment. Every trial's starter "
                  "has rows like this."),
        dict(concept="The values go in the order of the `def` line",
             code="def seats_left(seats, guests):\n    return seats - guests\n\n\n# seats is 8, guests is 5\n"
                  "print(seats_left(8, 5))\n# seats is 5, guests is 8\nprint(seats_left(5, 8))\n",
             output="3\n-3",
             note="The first value goes to the first parameter. Read `seats_left(8, 5)` as 8 seats and 5 guests. "
                  "The same two numbers the other way round give another answer."),
        dict(concept="The evidence in brackets",
             code='# (Mar\'tu\'s check called\n#  make_bar(2, 4, "▮", "▯"):\n#  it handed back "██░░",\n'
                  '#  not "▮▮▯▯".)\nprint("██░░" == "▮▮▯▯")\n',
             output="False",
             note="Every message ends with its evidence: the call Mar'tu's check made, what your function handed "
                  "back, and what it should hand back. Put the two side by side, then find the line that made the "
                  "difference. You read messages like this in the campaign."),
        dict(concept="The exact case: exactly enough",
             code="print(10 >= 10)\nprint(10 > 10)\n",
             output="True\nFalse",
             note="A hidden test named *exactly enough* sits right on the edge. `>=` lets it through; `>` does not. "
                  "Test one short of the edge, too."),
        dict(concept="The empty case",
             code="def last_sip(sips):\n    if len(sips) == 0:\n        return 0\n    return sips[-1]\n\n\n"
                  "print(last_sip([]))\nprint(last_sip([3, 5]))\n",
             output="0\n5",
             note="A hidden test named *an empty wall* or *an empty roster* hands over `[]`. Ask about it first: "
                  "`[-1]` of an empty list is an IndexError, and an average of no heroes divides by 0."),
        dict(concept="The right kind of value",
             code='print(True == "True")\nprint(5 == "5")\n',
             output="False\nFalse",
             note="`True` and `\"True\"` are different to Python, and so are `5` and `\"5\"`. Hand back the kind "
                  "the table shows: no quotes on `True`, `False` or a number."),
        dict(concept="Hand back with `return`, don't print",
             code="def shout_cost(cost):\n    print(cost)\n\n\nanswer = shout_cost(4)\nprint(answer)\n",
             output="4\nNone",
             note="The table reads what a function *hands back*. `print` only shows a value, and the call still "
                  "hands back `None`."),
        dict(concept="A typed answer fits one row only",
             code="def total(a, b):\n    return 22\n\n\nprint(total(12, 10))\nprint(total(3, 4))\n",
             output="22\n22",
             note="A [[hard-coded]] answer passes the row it was copied from. The next row, or a hidden test, shows "
                  "it. Work the answer out from the parameters."),
        dict(concept="A hidden test's label",
             code='# Hidden test: a roster of one.\ncrew = [{"name": "Moth"}]\nprint(len(crew))\n',
             output="1",
             note="A hidden test shows its label, not its values. Make that case yourself and run it: *an empty "
                  "wall* is `[]`, *a roster of one* is a list with one sheet, *exactly enough* is two equal numbers."),
        dict(concept="A function in a row: no `()`",
             code='def warm(hero):\n    hero["mana"] = hero["mana"] + 2\n\n\ndef to_each(sheets, action):\n'
                  "    for sheet in sheets:\n        action(sheet)\n\n\n"
                  'crew = [{"mana": 3}]\nto_each(crew, warm)\nprint(crew[0]["mana"])\n',
             output="5",
             note="In a row like `apply_to_all(party, warm)`, the second value is a function. It goes in with no "
                  "`()`, and the function that receives it calls it. (Trial: One Spell for Everyone)"),
        dict(concept="Write your own row: a seal",
             code="def is_full(mana, top):\n    return mana >= top\n\n\nassert is_full(20, 20) == True\n"
                  "assert is_full(19, 20) == False\nprint(\"Sealed.\")\n",
             output="Sealed.",
             note="A seal is a row you write yourself, with `assert`. A wrong function stops at it with an "
                  "AssertionError. Seal the edge from both sides. (Trial: Write Your Own Checks)"),
    ],
    notes=(
        "meta: path=TRIALS; kind=cheatsheet. The unit cheatsheet the spec asks for ('How to read a test table'). "
        "The framing card, u08a's Trials of the Yard, names this sheet: \"Mar'tu's notes on reading a table are the "
        "last card of the unit: *How to Read a Test Table*.\" One entry per reading habit the Trials teach: the row, "
        "the order of "
        "the values, the evidence bracket every check message ends with (T-Own's campaign link: reading check "
        "messages), the exact case, the empty case, the right kind, return versus print, a typed answer, a hidden "
        "label, a function as a value in a row, and a seal. Every snippet runs (the harness checks its output), "
        "uses only Units 1-7 tokens plus `assert` (2-A2), and keeps to 36 characters a line. The snippets use "
        "their own names (seats_left, last_sip, total, to_each, is_full), never a Trial's answer. Teacher ruling "
        "(Nov 14): entries 0 and 1 used to show T-CF-1's answer word for word (`can_cast` with `>=`); they now use "
        "`seats_left(seats, guests)`, which is no trial's answer and has no edge sign (the ruling's example was "
        "`has_room`; `seats_left` names the number it hands back). Entry 1 reads the value order on the same "
        "function, and swapping the two numbers shows why the order matters (3, then -3). Entry 0's comment is "
        "the starters' form, \"# It should show ...\", and the evidence entry uses the unified bracket: \"(Mar'tu's "
        "check called ...: it handed back ..., not ....)\". Concept titles say \"hand back\"; `return` is named only "
        "as the keyword."
    ),
)


# =============================================================================================
# The items, in the spec's order
# =============================================================================================

ITEMS = [
    MAKE_BAR, MAKE_BAR_CLAMPED,
    APPLY_TO_ALL, APPLY_IF_WORKED,
    REPLY_LOOKUP, ACT_LOOKUP,
    SEAL_CAN_CAST, SEAL_CAST_OK,
    TABLE_SHEET,
]


def _hidden_rows(item):
    """The "+ N hidden tests" line under each Learn-pane table (u08a's form), counted from the checks."""
    hidden = sum(1 for cp in item["checkpoints"] for name, _ in cp["checks"] if name.startswith("hidden: "))
    what = "hidden copies" if item["id"].startswith("seal-") else "hidden tests"
    martu = item["martu"]
    close = martu.index("```", martu.index("```text\n") + 8)
    item["martu"] = martu[:close] + f"+ {hidden} {what}\n" + martu[close:]


for _item in ITEMS:
    if _item["kind"] == "challenge":
        _hidden_rows(_item)
