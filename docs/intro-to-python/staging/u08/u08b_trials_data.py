"""Unit 8 "Code Challenges" ("Trials of the Yard"), part b: the Dictionaries set (T-D-1, T-D-2, T-D-3) and the
Loops set (T-Lo-1, T-Lo-2, T-Lo-3). Each core challenge is followed by its advanced variant (`variant_of`).

Spec: design/curriculum.md, "## Unit 8 · Code Challenges (optional)", the u08b rows of the table, in order:
  T-D-1   spell_cost(book, name)            -> the cost, or 0 if unknown
  T-D-1a  cheapest_spell(book)              -> the name of the cheapest spell (a loop: opens after Unit 6)
  T-D-2   affinity_of(hero)                 -> the nested read
  T-D-2a  meets(hero, spell)                -> both checks, nested, `<` versus `<=` exact
  T-D-3   rename_spell(book, old, new)
  T-D-3a  rename_spell(book, old, new)      -> refuses (returns False) when `new` already exists or `old` is missing
  T-Lo-1  total_mana(heroes)
  T-Lo-1a average_mana(heroes)              -> an empty roster gives 0
  T-Lo-2  count_below(wall, limit)
  T-Lo-2a first_shrink_over(wall, amount)   -> the index of the first gap whose shrink is larger than amount, else -1
  T-Lo-3  lowest_mana_name(heroes)
  T-Lo-3a lowest_mana_name(heroes)          -> on a tie, the alphabetically first name
Every item is kind="challenge", optional, support="light", explainer on (the default "full"), engine off.

Unlock ceilings (the curriculum's table; the harness only gates by course order, so this file was also checked
against each set's ceiling with the harness's own tokenizer, see "Ceiling check" at the bottom of these notes):
  * Dictionaries set (opens after Unit 5): Units 1-5 tokens only. No loops, no one-line choice, no `.items()`.
    rename_spell takes a key out with `.pop(old)` (attr:pop, u04b's list `.pop()`; its Learn pane and an Example
    show that a dictionary has one too). `del` (node:Delete) is never taught, so no visible code uses it.
  * T-D-1a cheapest_spell opens after Unit 6: Units 1-6 (`for`, `.items()`).
  * Loops set (opens after Unit 6): Units 1-6. No `None` in code (u07b), no default values (u07c), no f-strings.
  Nothing here is new: concept_map.json gives u08b no tokens.

The test table. FORMAT.md has `level` and `variant_of` for challenges, but no test-table field, so the table is
modelled with what exists (no invented fields), in the same form as u08a (written at the same time; its framing
card "Trials of the Yard" and its GLOSSARY own [[test table]], [[hidden test]], [[edge case]] and [[hard-coded]],
which this part links to and does not redefine):
  * Mar'tu's Learn pane shows the visible tests as a fenced table (call → what comes back), then "+ N hidden
    tests" (counted from the checks by _hidden_rows() at the bottom of the file), at most 36 characters a line.
  * The starter is the signature with `pass` (S1), then "# Visible tests. They should show ...", the line
    "# (With only pass, each shows None.)" (not in rename-spell, whose print shows the book; rename-safely says
    "both"), and the first checkpoint's calls as `print` lines, so Run shows the student's answers next to the
    table's. A row whose slip would crash the run before Mar'tu's checks (spell-cost row 3, total-mana row 3,
    average-mana row 4, rename-safely row 3) is in the table and a COMMENT in the starter: "Once rows 1 and 2
    pass, add" / "# print(...)" / "It should show 0." So the slip gets Mar'tu's message, not the explainer's
    generic one (which points the wrong way: "Use a key that is already there"); a fails_at 0 twin adds the
    call back and proves Python's own error.
  * Each visible test is one named check ("row 2: ..."); its message ends with u08a's evidence bracket,
    "(Mar'tu's check called `count_below(wall, 48)`: it handed back `4`, not `5`.)".
  * Each hidden test is one named check ("hidden: an empty wall"). Its message names the label, never the test's
    values, and a number or a name that came back is not shown either: "(Hidden test: an empty wall. It handed
    back a different number.)"; `True`/`False`, `None`, text such as `"0"` and an error's name are shown.
  * Checkpoint ids: a core challenge has `visible-tests` and `hidden-tests` (u08a's ids). An advanced variant has 3: the main
    rows, the variant's new rule (the mana question, a tie, the refusals, an empty roster, none found), then the
    hidden tests. Where the new rule is its own step of code, the variant has a partial (a staged solution that
    passes the main rows and fails the new rule): meets, rename-safely, average-mana, first-shrink-over,
    lowest-with-ties. cheapest-spell has none: a strict `<` already keeps the first of a tie.
Site support that would make this nicer (for the report): a `tests=[dict(call=..., want=..., hidden=False,
label=...)]` field rendered as a real table with a pass/fail column per row; "Run the table" that shows each
row's result even when a later row crashes; and hidden rows shown as labels with a lock until they pass. From the
Nov 14 ruling: when the student's function crashes inside a trial, still run Mar'tu's checks, only to choose the
message (never to mark a step passed), so a KeyError in spell_cost gets "Ask the book first", not the explainer's
"Use a key that is already there" (the commented-out rows above are the content-side fallback); explainer rows for
a parameter's name in quotes used as a key (`book["name"]`) and a running total started inside the loop (`total = 0`
under `for`); and a trial passed with no help past Where to look, recorded on the skill map.

Check helpers (_TX, below). Each part file is plain data, so the helpers live here; `check()` puts in front of
each check only the helpers it uses (as u07a does). Every check calls the student's function inside the check,
with deep copies of Mar'tu's own data, prints captured, and a line budget (u06c's guard), so a loop that never
ends can't freeze the page:
  _need()     the function exists with the signature's parameters, letter for letter (NAME near misses), in the
              table's order (the right names in another order get their own message: the table read backwards).
  _run()      one call, on copies: the returned value, the printed lines, the error, and the arguments after the
              call (to see a list or book that was changed).
  _verdict()  one row, in this order: an error inside the function (item messages first, then _why), print
              instead of return, None (no `return`, a bare one, or a path that falls off the end), the wrong kind
              of value (text "True", text "0", a number for a name, a whole sheet), a typed value from the table
              (hard-coding: the constant is read from the function's own code), the class's known slips (each
              simulated at build time on the row's own data, so the message names the slip only when the slip
              really gives that answer), then the input left as it was.
  _renamed()  the rename rows (state, not a returned value): the page moved, the old name gone, the other
              pages kept, the book itself changed (a new book returned instead is caught), and for the variant
              the refusals leave the book exactly as it was.
  _why()      an error raised inside the student's function: a quoted parameter, a name from the table, a
              skipped level, a key with no quotes, a sheet added as a number, a list read by key, `.get()`'s None,
              `min()` of sheets, a dict's `.remove()`, ZeroDivisionError, IndexError, a loop that never ends.
Messages put the fix first, then what happened, then the evidence bracket (the Unit 2/3 ruling). A student's
own text is never shown: returned text is shown only when it is one of the test's own names, "True"/"False" or a
number in quotes (2.11), and on a hidden test not even that. Each check is a standalone string, so it carries its
own copy of the helpers it needs, re-printed without comments (about 18 KB a check; this part's share of the unit
JSON is about 1.6 MB, in line with Units 3-6). Invented Tor names only in hidden data (Pell, Brakka, Moss, Glug, Ivo, Moth, Tinplate,
Ash, Bree; Moon Step, Ash Ward, Ember Coat, Quiet Step, Frost Lace, Hedge Hop, Sun Ward, Star Fall); never
"Tester" and never a worksheet name.

The class's slips for this unit, each proven by a wrong_answers entry (item in brackets):
  * hard-coding the table: one answer typed (`return 2`, `return 45`, `return "Glow"` ...: the next row fails and
    says "typed in"), and the whole table typed as an if-chain on the visible inputs (passes every visible row;
    the hidden labeled tests catch it): every core item.
  * `<` versus `<=` at the exact boundary: exactly enough counts (meets: `>` fails "exactly enough mana"); a gap
    equal to the limit is not below it (count_below: `<=`); a shrink equal to the amount is not larger
    (first_shrink_over: `>=`); a tie keeps the first spell (cheapest_spell: `<=`); a tie goes to the alphabet
    (lowest_mana_name variant: `<` keeps the first, `<=` keeps the last).
  * the empty case: an empty roster divides by 0 (average_mana: ZeroDivisionError, the partial); an empty wall,
    an empty book and an empty roster give the stated default (count_below 0, first_shrink_over -1, spell_cost 0,
    total_mana 0); `wall[i + 1]` off the end (IndexError, first_shrink_over); no `return -1` after the loop (None).
    (`wall[-1]` of an empty list is T-L-1a, in u08a.)
  * the wrong type: `"True"` / `"False"` in quotes (meets, rename_spell variant), `"0"` (spell_cost, average),
    `str(total)` (total_mana), the cost for the name (cheapest_spell), the mana for the name, the whole sheet or
    page for one value (lowest_mana_name, spell_cost, affinity_of).
  * print instead of return: every core item, and the variant's refusals.
  * the input changed when it should be left alone (`wall.sort()`, popping the roster empty while adding, a page
    added for an unknown spell, mana spent inside `meets`), and the reverse: a new book built and returned when the
    book handed in should change (rename_spell, both).
  * a KeyError for an unknown spell instead of returning 0 (spell_cost: in the starter as given, row 3's call a
    comment, Mar'tu's "Ask the book first", fails_at 1; with the call added back, Python's own KeyError, fails_at
    0); the guard written after the read; `.get(name)` then `["mana_cost"]` (None is not subscriptable).
  * tie-breaking wrong: first kept, last kept, the alphabet used for every hero (not only the tied ones).
  * the table read backwards: parameters in the other order (`def count_below(limit, wall)`), counting the gaps
    above instead of below, `len / total` for the average, the shrink returned instead of its index, the index of
    the gap before, `book[old] = book[new]` (the rename backwards), growth instead of shrink.
  * loop slips: the total reset inside the loop, `return` inside the loop (the first hero only), `-1` returned on
    the first gap that does not match, the last match kept (no early exit), `range(len(wall))` reading `wall[-1]`
    on the first pass, a start value typed as 100 or 0 for the lowest, the lowest name kept but not its mana,
    `min(book)` (alphabet, not cost), `sum(heroes)`, `heroes["mana"]`.
  * (Calling the effect function with or without `()` and asserts that pass on a wrong function belong to T-F-2 and
    T-Own, in u08c.)

Check-breaker pass (Nov 14). Cheats and slips that passed, or passed a step, before it, now each a wrong_answers entry:
  * cheapest_spell: names compared instead of costs passed rows 1-2 (the alphabet-first name WAS the answer), so row 1's
    book now has five spells and Ember Coat comes first in the alphabet; a typed start of 9999 passed (the costly hidden
    book is now 1,200,000 and up, and so are lowest_mana_name's "very high mana" and the tie at very high mana).
  * affinity_of: `list(hero["abilities"].values())[1]` passed every row (Moth's card now has the affinity third).
  * first_shrink_over: `range(2, len(wall))` passed every row (no answer was at position 1; a hidden wall now is).
  * lowest_mana_name (ties): the name kept without its mana, and a start at `heroes[1]` (counting from 1), passed every
    row; a middle value after the lowest and a roster of one hero now catch them.
  * A hidden test's value leaked into a message ("your function asks for `"Glow"` by name" when the name came from the
    hidden test, not the function): _why() now names a table value only when the function itself has it typed.
  Messages that named the wrong slip (another slip gave the same answer) now carry a condition read from the student's
  own code: _ret_in_loop() (a `return` in a loop), _set_in_loop() (a count reset inside it), _assigns() (a start such as
  `name = ""` or `low = 0`), _stops_early() (`range(1, len(...) - 1)`), _pops_new() (`book.pop(new)`), `node:Break`,
  `call:abs`. New slips named: low never updated (cheapest), `heroes[0]` of an empty roster (total_mana: IndexError),
  `break` at the first gap that is not short, `abs()` of a shrink, the last gap never read, 0 for "none found", each gap
  taken from the first gap, `name = ""` with `low = heroes[0]["mana"]`, a tie taken without comparing names or compared
  with the first hero's name. A rule row's own message (`fall`): any other wrong number for a missing spell or an empty
  roster is told the rule ("Hand back 0 for ..."), not "work this row out by hand".

Help ladder (FORMAT.md and the Unit 2 walkthrough conventions): hints[0] Where to look; the middle hints Teach me,
with tiny examples on other names (`pack`, `item`, `bags`, `jars`, `coins`, `steps`, `shelf[fresh]`, listed in
foreign_names); the last hint is Show me how, with a line from Mar'tu's own solution first in backticks (its start
is Start me off, and the harness checks it is in the solution); never "Start like this" first. Then another_way
(2+ angles), assemble (More structure: the function's lines, which pass every checkpoint on their own) and the
solution (Compare). Support is "light": Where to look is open from the start, the rest after the first failed run.
Two unit-wide rules for Show me how (the Nov 14 ruling, as in u08a):
  * No crash. Every Show rung, pasted word for word into the starter (in place of `pass`, or above it), and on top
    of the earlier checkpoints' rungs, runs with no crash. A rung leaves a part to the student only by naming it in
    words, never as an `if` with nothing under it or a name no line makes. Each item's notes record the probe
    ("Show-rung copy-test"); a rung that is not the solution or a partial has its own wrong_answers entry.
  * The sign at the edge. Where the visible rows of a checkpoint cannot tell two signs apart, the rung offers both
    complete lines and names the hidden test that decides (meets, both steps); the hidden-tests rung then gives the
    one right line. Where a visible row decides it, the rung keeps the one sign: cheapest-spell row 3 (it says
    "or `<=`: row 3 decides"), count-below row 1, first-shrink-over row 1, the a-tie rows.

Terminology (2.9): these sets open after Units 5 and 6, so Mar'tu's first line in each core Learn pane says "a
function (a recipe)"; everything else says "function", "parameter", "hands back" (Units 3-6's word, and u08a's;
`return` is named only as the keyword: "Put `return` after the loop"), "key", "gap" and "shrink". The quotes
sentence is used word for word where a quoted parameter is the slip.
UNIT is copied from u08a verbatim (the exporter requires every part's UNIT fields to match). New glossary terms
here, linked from this part's prose: [[tie]], [[average]], [[early exit]], [[ZeroDivisionError]]; none of their
names or aliases is used by u08a's or any earlier unit's glossary (the exporter run on a copy of staging passes).

Phone width: fenced tables, examples, predict code and every starter and solution line keep to 36 characters or
fewer, with one exception: a call is never wrapped (u08a's ruling: a wrapped call reads as broken code). So
rename-safely's visible calls (41 and 47 characters) and the commented-out row-3 calls (spell-cost 38, rename-safely
44) stay whole on one line; comment lines around them wrap at a word.

Ceiling check (run while writing, with the harness's own tokenizer over every code a student SEES: starter,
solution, partials, example, predict code, assemble lines; allowed = the base tokens plus concept_map.json up to
the set's unlock point). Dictionaries items (spell-cost, affinity-of, meets, rename-spell, rename-safely) use only
tokens introduced by u05c: Assign, Dict, FunctionDef, If, Pass, Return, Subscript, In, NotIn, Lt, Gt, GtE, bool,
attr:pop, print. cheapest-spell and the Loops items use only tokens introduced by u06b (adding For, List, Slice,
len, range, Add, Sub, USub, Div, FloorDiv in a predict, Eq, Or, attr:items). Nothing needs u07 (no None, no
default values, no lambda, no f-strings). Re-run the same check after any edit: the harness alone would accept
u07 tokens here, because it gates by course order, not by a set's unlock point.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u08b
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# Check helpers (plain Python, run in the student's namespace after their code; every name starts with `_`
# and builtins come from `_B`, so a student's `sum = 0` or `min = 3` can't break a check)
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
_SHEET_KEYS = ('name', 'mana', 'abilities', 'magical_affinity', 'strength', 'mana_cost', 'required_affinity')


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


def _lit(_v):
    # One of Mar'tu's own values, written as code (never a student's).
    if _tn(_v) == 'str':
        return '"' + _v + '"'
    if _tn(_v) in ('list', 'tuple'):
        return '[' + ', '.join([_lit(_x) for _x in _v]) + ']'
    return _B.str(_v)


def _sh(_v):
    # A returned value, in words. Numbers and True/False as they are; text only when it is one of the test's
    # own names, "True"/"False" or a number in quotes; never a student's own words (2.11).
    _k = _tn(_v)
    if _k == 'float':
        return '`' + _B.str(_B.round(_v, 4)) + '`'
    if _k in ('bool', 'int'):
        return '`' + _B.str(_v) + '`'
    if _k == 'NoneType':
        return 'nothing (`None`)'
    if _k == 'str':
        if _v == '':
            return 'empty text, `""`'
        if _v in _OK or _v in ('True', 'False') or _re.fullmatch(r'-?\d+(\.\d+)?', _v):
            return 'the text `"' + _v + '"`'
        return 'a piece of text'
    if _k == 'dict':
        return 'a whole dictionary'
    if _k in ('list', 'tuple'):
        return 'a list'
    if _k == 'function':
        return 'a function'
    return 'a ' + _k


def _cap(_s):
    return _s[:1].upper() + _s[1:]


def _same(_v, _w):
    # Equal AND the same kind: True is not 1, "2" is not 2, and 2.0 counts as 2.
    _kv, _kw = _tn(_v), _tn(_w)
    if 'bool' in (_kv, _kw):
        return _kv == _kw and _v == _w
    if _kw in ('int', 'float'):
        return _kv in ('int', 'float') and _B.abs(_v - _w) < 1e-9
    return _kv == _kw and _v == _w


def _edits(_a, _b):
    _prev = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _x in _B.enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in _B.enumerate(_b, 1):
            _cur.append(_B.min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b):
    # NAME / KEY / PNM near miss: case, plural, or 1-2 edits.
    if _tn(_a) != 'str' or _tn(_b) != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower().replace(' ', '_'), _b.lower().replace(' ', '_')
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


def _need(_name, _want):
    # The function exists, made with `def`, with the signature's parameters in the signature's order.
    _line = '`def ' + _name + '(' + ', '.join(_want) + '):`'
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


def _run(_f, _args):
    # One call, on deep copies of Mar'tu's data, prints captured, inside the line budget.
    _in = _copy.deepcopy(_args)
    _work = _copy.deepcopy(_args)
    _buf = _Cap()
    _old = _sys.stdout
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _guarded(lambda: _f(*_work))
    except _Runaway as _e:
        _err = _e
    except _B.Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _old
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    return {'val': _val, 'rows': _rows, 'err': _err, 'args': _in, 'after': _work}


def _an(_k):
    return ('an ' if _k[:1] in 'AEIOU' else 'a ') + _k


def _did(_r, _hide=False):
    # What the call did, in words. _hide (a hidden test): a number or a name that came back is not shown.
    _v = _r['val']
    if _r['err'] is not None:
        if _tn(_r['err']) == '_Runaway':
            return 'it never finished'
        return 'Python stopped with ' + _an(_tn(_r['err']))
    if _v is None and _r['rows']:
        return 'it printed a line but handed back `None`'
    if _v is None:
        return 'it handed back `None`'
    if _hide and _tn(_v) in ('int', 'float'):
        return 'it handed back a different number'
    if _hide and _tn(_v) == 'str' and _v in _OK:
        return 'it handed back a different name'
    return 'it handed back ' + _sh(_v)


def _evs(_r, _what=''):
    # The evidence bracket: a visible test shows its call; a hidden test shows only its label.
    if _ROW[0] == 'v':
        _d = _what or _did(_r)
        if not _what and _r['err'] is None and _r['val'] is not None:
            _d = _d + ', not `' + _lit(_g.get('_WANT')) + '`'
        return "(Mar'tu's check called `" + _ROW[2] + '`: ' + _d + '.)'
    return '(Hidden test: ' + _ROW[1] + '. ' + _cap(_what or _did(_r, True)) + '.)'


def _evr(_r):
    # The evidence bracket for a rename row: what the book should hold afterwards.
    _stop = (' Python stopped with ' + _an(_tn(_r['err'])) + '.') if _r['err'] is not None else ''
    if _ROW[0] == 'v':
        return "(Mar'tu's check called `" + _ROW[2] + '`: ' + _ROW[3] + '.' + _stop + ')'
    return '(Hidden test: ' + _ROW[1] + '.' + _stop + ')'


def _has(_s):
    # True when the function's own code holds the constant _s (a key such as "mana").
    _d = _defs().get(_FN)
    return _d is not None and _B.any(_tn(_n) == 'Constant' and _n.value == _s for _n in _ast.walk(_d))


def _early_minus():
    # A `return -1` inside a loop's body: the function gives up at the first item that does not match.
    _d = _defs().get(_FN)
    if _d is None:
        return False
    for _n in _ast.walk(_d):
        if _tn(_n) in ('For', 'While'):
            for _x in _ast.walk(_ast.Module(body=_n.body, type_ignores=[])):
                if (_tn(_x) == 'Return' and _tn(_x.value) == 'UnaryOp' and _tn(_x.value.operand) == 'Constant'
                        and _x.value.operand.value == 1):
                    return True
    return False


def _ret_in_loop():
    # A `return` inside a loop's body (the function stops on the first pass).
    _d = _defs().get(_FN)
    if _d is None:
        return False
    for _n in _ast.walk(_d):
        if _tn(_n) in ('For', 'While'):
            for _x in _ast.walk(_ast.Module(body=_n.body, type_ignores=[])):
                if _tn(_x) == 'Return':
                    return True
    return False


def _set_in_loop():
    # A name set to a plain constant inside a loop's body (a count that starts again on every pass).
    _d = _defs().get(_FN)
    if _d is None:
        return False
    for _n in _ast.walk(_d):
        if _tn(_n) in ('For', 'While'):
            for _x in _ast.walk(_ast.Module(body=_n.body, type_ignores=[])):
                if _tn(_x) == 'Assign' and _tn(_x.value) == 'Constant':
                    return True
    return False


def _assigns(_v):
    # True when the function sets a name straight to the constant _v (a start such as `low = 0` or `name = ""`).
    _d = _defs().get(_FN)
    return _d is not None and _B.any(_tn(_n) == 'Assign' and _tn(_n.value) == 'Constant' and _same(_n.value.value, _v)
                                     and _tn(_n.value.value) == _tn(_v) for _n in _ast.walk(_d))


def _stops_early():
    # `range(start, len(...) - 1)`: two arguments, and the stop has a minus in it (the last item never read).
    _d = _defs().get(_FN)
    return _d is not None and _B.any(_tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'range'
                                     and _B.len(_n.args) == 2 and _tn(_n.args[1]) == 'BinOp'
                                     and _tn(_n.args[1].op) == 'Sub' for _n in _ast.walk(_d))


def _pops_new():
    # `.pop(<the third parameter>)`: the page just stored under the new name is taken out again.
    _d = _defs().get(_FN)
    if _d is None or _B.len(_d.args.args) < 3:
        return False
    _p = _d.args.args[2].arg
    return _B.any(_tn(_n) == 'Call' and _tn(_n.func) == 'Attribute' and _n.func.attr == 'pop' and _n.args
                  and _tn(_n.args[0]) == 'Name' and _n.args[0].id == _p for _n in _ast.walk(_d))


def _outer():
    # A list or dictionary made at the top level and read inside the function instead of its parameter.
    _d = _defs().get(_FN)
    if _d is None:
        return ''
    _ps = [_a.arg for _a in _d.args.args]
    _tops = []
    for _n in _tree.body:
        if _tn(_n) == 'Assign':
            _tops += [_t.id for _t in _n.targets if _tn(_t) == 'Name']
    _local = [_t.id for _n in _ast.walk(_d) if _tn(_n) in ('Assign', 'For')
              for _t in ([_n.target] if _tn(_n) == 'For' else _n.targets) if _tn(_t) == 'Name']
    for _n in _ast.walk(_d):
        if (_tn(_n) == 'Name' and _n.id in _tops and _n.id not in _ps and _n.id not in _local
                and _tn(_g.get(_n.id)) in ('dict', 'list')):
            return ('Use the parameter `' + (_ps[0] if _ps else '') + '`, not `' + _n.id + '`: the function must '
                    'read what the call hands it, so it works for any ' + ('list' if _tn(_g.get(_n.id)) == 'list'
                                                                           else 'dictionary') + '.')
    return ''


def _karg(_e):
    return _e.args[0] if _tn(_e) == 'KeyError' and _e.args else None


def _why(_e):
    # A kind message for an error raised inside the student's function while Mar'tu's check called it.
    _k = _tn(_e)
    _s = _B.str(_e)
    _f = _g.get(_FN)
    _ps = _params(_f) if _tn(_f) == 'function' else []
    _ing = 'The parameters of `' + _FN + '` are ' + _names(_ps) + '.'
    if _k == '_Runaway':
        return ('Make every loop end: with these values your function never finished. A `while` loop needs a line '
                'inside it that changes what it asks about.')
    if _k == 'KeyError':
        _x = _karg(_e)
        if _tn(_x) == 'str' and _x in _ps:
            return ('Take the quotes off `"' + _x + '"` to use the parameter `' + _x + '`. With quotes, Python looks '
                    'for a key spelled ' + _x + '. ' + _QUOTES)
        if _x in _TYPED and _has(_x):
            return ('Use the parameters, not a name from the table: your function asks for `' + _lit(_x) + '` by '
                    'name, and this book has no such key.')
        _ty = _typed_in()
        if _ty:
            return _ty
        _near = [_y for _y in _SHEET_KEYS if _close(_x, _y)]
        if _near:
            return 'Use the key `"' + _near[0] + '"`, letter for letter, capitals too. The sheet has no key spelled that way.'
        if _x in ('magical_affinity', 'strength'):
            return ('Go one level in: `"' + _x + '"` is inside `"abilities"`, so read `["abilities"]` first, then `["'
                    + _x + '"]`.')
        if _tn(_x) == 'int':
            return 'Read a dictionary by its key, not by a position: a sheet has keys like `"mana"`, not `[0]`.'
        return 'Use a key the dictionary really has, or ask with `in` first: Python found no such key.'
    if _k == 'IndexError':
        return ('Use a position the list really has: a `for` loop, or `range(len(...))`, never a typed position. '
                'Python went past the end of the list.')
    if _k == 'ZeroDivisionError':
        return 'Check for an empty list first, and hand back the trial\'s answer for it: Python cannot divide by 0.'
    if _k in ('NameError', 'UnboundLocalError'):
        _x = _B.getattr(_e, 'name', None) or ''
        if not _x:
            _m = _re.search(r"'(\w+)'", _s)
            _x = _m.group(1) if _m else ''
        if _k == 'UnboundLocalError' or 'local variable' in _s or 'not associated' in _s:
            return ('Make `' + _x + '` before the line that uses it. Python runs a function from the top down.')
        if _x in _SHEET_KEYS:
            return 'Put quotes around the key: `["' + _x + '"]`. ' + _QUOTES
        if [_p for _p in _ps if _close(_x, _p)]:
            return _ing + ' You wrote `' + _x + '`. Python matches names letter for letter.'
        return 'Inside `' + _FN + '`, Python found a name it does not know: `' + _x + '`. ' + _ing
    if _k == 'TypeError':
        if 'list indices must be integers' in _s and 'not str' in _s:
            return ('Read one item at a time: `' + (_ps[0] if _ps else 'it') + '` is a list, so loop over it, and read '
                    'each item\'s key inside the loop, like `hero["mana"]`.')
        if 'list indices must be integers' in _s and 'not dict' in _s:
            return ('Use the item the loop hands you, like `hero["mana"]`: a `for` loop gives you each sheet, not a '
                    'position.')
        if 'string indices must be integers' in _s:
            return ('Read the dictionary, not text: take the quotes off the parameter\'s name. ' + _QUOTES)
        if 'unsupported operand' in _s and "'dict'" in _s:
            return 'Add a number from each sheet, like `hero["mana"]`, not the whole sheet.'
        if 'unsupported operand' in _s and "'str'" in _s or 'concatenate' in _s:
            return 'Add numbers, not text: read the `"mana"` key, not the `"name"` key.'
        if "'int' object is not iterable" in _s:
            return 'A `for` loop walks a list. To walk the positions, use `range(len(...))`, not a number.'
        if "'NoneType' object is not subscriptable" in _s:
            return ('Ask with `in` or `not in` before you read: `.get()` hands back `None` for a name that is not '
                    'there, and `None` has no keys.')
        if 'not subscriptable' in _s:
            return 'Read the key from a dictionary: that value is a number, not a sheet or a list.'
        if 'not supported between' in _s and "'dict'" in _s:
            return ('Compare numbers, like a hero\'s `"mana"` or a page\'s `"mana_cost"`, not whole dictionaries: '
                    'Python can\'t put dictionaries in order.')
        if 'not supported between' in _s:
            return 'Compare a number with a number: one side of the sign is text.'
        if "'dict' object is not callable" in _s:
            return 'Read a dictionary with square brackets, `book[name]`, not round ones.'
        if 'unhashable' in _s:
            return 'Use a name as the key: a whole dictionary or list cannot be a key.'
        if 'positional argument' in _s:
            return 'Count the values against the `def` line: a call inside your function hands over the wrong number.'
    if _k == 'AttributeError':
        if 'remove' in _s or 'append' in _s:
            return 'Take a key out of a dictionary with `.pop(key)`: a dictionary has no `.remove()` or `.append()`.'
        return 'Read a dictionary with square brackets, like `hero["mana"]`, not a dot.'
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
    # The wrong KIND of value: text for a number, a number for a name, text "True" for True ...
    _kv, _kw = _tn(_v), _tn(_w)
    if _kv in _KIND and not _same(_v, _w) and _kv != _kw:
        return _KIND[_kv]
    if _kw == 'bool' and _kv != 'bool':
        if _kv == 'str' and _v in ('True', 'False'):
            return ('Hand back `True` or `False` with no quotes. With quotes it is text, and text is not a yes/no '
                    'answer.')
        return 'Hand back `True` or `False`: this trial asks a yes/no question.'
    if _kw in ('int', 'float') and _kv not in ('int', 'float'):
        if _kv == 'str':
            return 'Hand back a number, not text: no quotes and no `str()`.'
        if _kv == 'bool':
            return 'Hand back a number, not `True` or `False`.'
        if _kv == 'dict':
            return 'Hand back one number from the sheet, not the whole dictionary.'
        return 'Hand back one number.'
    if _kw == 'str' and _kv != 'str':
        if _kv in ('int', 'float', 'bool'):
            return 'Hand back the name, not a number.'
        if _kv == 'dict':
            return 'Hand back the name, not the whole sheet.'
        return 'Hand back one name.'
    return ''


def _typed_in(_v=None, _only=False):
    # A value from the table typed into the function itself (hard-coding). With _v: only that value.
    _d = _defs().get(_FN)
    if _d is None:
        return ''
    for _n in _ast.walk(_d):
        if _tn(_n) != 'Constant' or _tn(_n.value) not in ('str', 'int', 'float'):
            continue
        if _n.value in _TYPED and (not _only or _same(_n.value, _v)):
            return ('Use the parameters, not values from the table: your function has `' + _lit(_n.value)
                    + '` typed in it, so it only works for those rows.')
    return ''


def _changed(_a, _b):
    # How a list or a dictionary was changed, in words.
    if _tn(_a) == 'list' and _tn(_b) == 'list':
        if _B.len(_b) < _B.len(_a):
            return 'it got shorter'
        if _B.len(_b) > _B.len(_a):
            return 'it got longer'
        return 'its order or its values changed'
    if _tn(_a) == 'dict' and _tn(_b) == 'dict':
        if _B.set(_a) != _B.set(_b):
            return 'a key was added or taken out'
        return 'a value inside it changed'
    return 'it changed'


def _verdict(_r, _want, _errs=(), _alts=(), _keep=True):
    # One table row, checked in the order the notes give.
    _g['_WANT'] = _want
    _v, _e = _r['val'], _r['err']
    if _e is not None:
        for _c, _m in _errs:
            if _c(_e):
                assert False, _m + ' ' + _evs(_r)
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
                                            'handed (' + _changed(_a, _b) + '). Read it; don\'t change it.')) + ' ' + _evs(
                    _r, 'it handed back the right answer, but it changed `' + _ps[_i] + '`')


def _renamed(_r, _old, _new, _part, _ret=None, _errs=()):
    # A rename row. _part: 'page' (the old page is under the new name), 'old' (the old name is gone), 'others'
    # (every other page kept), 'refuse' (nothing changed). _ret: the value the variant must return, or None.
    _v, _e = _r['val'], _r['err']
    if _e is not None:
        for _c, _m in _errs:
            if _c(_e):
                assert False, _m + ' ' + _evr(_r)
        if _karg(_e) == _new and _part != 'refuse':
            assert False, ('Put the new name on the left: `book[new] = book[old]`. Your function read `book[new]`, '
                           'and the book has no page there yet. ' + _evr(_r))
        assert False, _why(_e) + ' ' + _evr(_r)
    _b0, _b = _r['args'][0], _r['after'][0]
    if _part == 'refuse':
        if _tn(_b) != 'dict' or _b != _b0:
            if _tn(_b) == 'dict' and _new in _b0 and _new in _b and _b[_new] != _b0[_new]:
                assert False, ('Ask first, then change: when the new name is already a spell, return `False` before '
                               'you store anything. Your function stored over that spell\'s page. ' + _evr(_r))
            assert False, ('Refuse without changing the book: return `False` first, and the book stays exactly as it '
                           'was. Your function changed it (' + _changed(_b0, _b) + '). ' + _evr(_r))
    else:
        _page = _b0[_old]
        if _b == _b0:
            _ty = _typed_in()
            assert not _ty, _ty + ' ' + _evr(_r)
            if _tn(_v) == 'dict' and _new in _v:
                assert False, ('Change the book you were handed: your function built a new book and handed it back, '
                               'and the caller\'s book stayed the same. Write into `book` itself. ' + _evr(_r))
            if _pops_new():
                assert False, ('Pop the old name, `book.pop(old)`: your function popped `new`, the page it had just '
                               'stored, so the book ended as it began. ' + _evr(_r))
            assert False, ('Store the old page under the new name, `book[new] = book[old]`, in the book you were '
                           'handed: the book did not change. ' + _evr(_r))
        if _part in ('page', 'old', 'others'):
            if _new not in _b:
                _ty = _typed_in()
                assert not _ty, _ty + ' ' + _evr(_r)
                assert False, ('Store the old page under the new name: `book[new] = book[old]`. The book has no '
                               'page under the new name. ' + _evr(_r))
            if _b[_new] != _page:
                if _b[_new] == _old:
                    assert False, ('Store the page, not the name: `book[new] = book[old]` moves the whole page. ' + _evr(_r))
                assert False, ('Move the old page itself, `book[old]`, not values typed in: the page under the new '
                               'name is not the old page. ' + _evr(_r))
        if _part in ('old', 'others') and _old in _b:
            assert False, ('Take the old name out of the book: `book.pop(old)`. Now the spell is in the book twice. '
                           + _evr(_r))
        if _part == 'others':
            _rest0 = {_k: _x for _k, _x in _b0.items() if _k != _old}
            _rest = {_k: _x for _k, _x in _b.items() if _k != _new}
            assert _rest == _rest0, ('Leave the other spells as they were: change only the one you rename. '
                                     + _evr(_r))
    if _ret is not None and not _same(_v, _ret):
        if _v is None and _r['rows']:
            assert False, ('Use `return`, not `print`: the test reads what your function hands back. ' + _evr(_r))
        if _v is None:
            assert False, (('End with `return True` after the rename: your function handed back `None`.' if _ret
                            else 'Refuse with `return False`: a bare `return`, or no `return`, hands back `None`.')
                           + ' ' + _evr(_r))
        _t = _kind_msg(_v, _ret)
        assert not _t, _t + ' ' + _evr(_r)
        assert False, (('Hand back `True` after the rename.' if _ret else 'Hand back `False` when you refuse.') + ' '
                       + _evr(_r))
'''.replace("__QUOTES__", repr(QUOTES_RULE))


def _tx_parts():
    """_TX split into its setup lines (imports, _g, _tree, ...) and its helper functions and classes, each with the
    helper names it uses, so a check can carry only the helpers it needs (the unit JSON stays small). Each piece is
    re-printed by ast.unparse: the same code, without the comments."""
    import ast

    tree = ast.parse(_TX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.unparse(node)  # the same code with its comments dropped, so each check carries less
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
# Row builders: one check per table row. Slips are simulated HERE, at build time, on the row's own data, so a
# slip's message is attached only when that slip really gives a different answer from the table's.
# ---------------------------------------------------------------------------------------------

_FALL_V = "Work this row out by hand first, then follow your function line by line with the same values."
# The teacher's ruling text, its first sentence trimmed ("Your function passes the table but not this test."): the
# other two sentences alone are 35 words, so the first is cut to 7 rather than dropped (what happened, then what
# to try): 41 words, and about 52 with a bracket such as "(Hidden test: an empty wall. It handed back a
# different number.)" (count-below's wrong_answers prove it).
_FALL_H = ("It passes the table, not this test. Make this case yourself: under the table, add a `print(...)` call "
           "that tries what the label says, and Run. Use only the parameters inside the function, never a number or "
           "a name from the table.")


def _same_py(a, b):
    """Build-time twin of the check's _same()."""
    ka, kb = type(a).__name__, type(b).__name__
    if "bool" in (ka, kb):
        return ka == kb and a == b
    if kb in ("int", "float"):
        return ka in ("int", "float") and abs(a - b) < 1e-9
    return ka == kb and a == b


def _simulate(slips, args, want):
    """[(value, message, condition)] for every slip that gives a different answer on these arguments, in the
    order given. A slip is (python function, message) or (python function, message, condition): the condition is
    check code (for example `_uses('op:LtE')`) that tells apart two slips giving the same answer."""
    import copy

    out = []
    for slip in slips:
        fn, message, cond = (tuple(slip) + (None,))[:3]
        try:
            got = fn(*copy.deepcopy(args))
        except Exception:
            continue
        if got is None or _same_py(got, want):
            continue
        out.append((got, message, cond))
    return out


def _alts_code(alts):
    return "[" + ", ".join(f"({v!r}, {m!r}, {('(lambda: ' + c + ')') if c else 'None'})" for v, m, c in alts) + "]"


def _code(value):
    return repr(value)


def _errs_code(errs):
    return "[" + ", ".join(f"(lambda _e: {cond}, {message!r})" for cond, message in errs) + "]"


def row(fn, params, args, want, where, *, ok=(), typed=(), errs=(), slips=(), keep=True, kind=None, keepmsg="",
        none="", fall=""):
    """One test-table row as a check.
    where = ("v", n, "call as shown in the table", "return 2") for a visible row, or ("h", "label") for a hidden test.
    errs = [(condition on `_e`, message)] for errors raised inside the function, before the generic _why().
    slips = [(python function, message)]: simulated now; the check names the slip when the answer matches it.
    fall = the message for any other wrong answer, on a row whose only right path is the trial's rule (a missing
    spell's 0, an empty roster's 0), in place of the generic "work this row out by hand"."""
    alts = _simulate(slips, args, want)
    name = (f"row {where[1]}: {where[2]}" if where[0] == "v" else f"hidden: {where[1]}")
    body = (
        f"_FN = {fn!r}\n"
        f"_OK = {list(ok)!r}\n"
        f"_TYPED = {list(typed)!r}\n"
        f"_KIND = {dict(kind or {})!r}\n"
        f"_KEEPMSG = {keepmsg!r}\n"
        f"_NONE = {none!r}\n"
        f"_ROW = {tuple(where)!r}\n"
        f"_FALL = {(fall or (_FALL_V if where[0] == 'v' else _FALL_H))!r}\n"
        f"_f = _need({fn!r}, {list(params)!r})\n"
        f"_r = _run(_f, {_code(tuple(args))})\n"
        f"_verdict(_r, {_code(want)}, {_errs_code(errs)}, {_alts_code(alts)}, {keep!r})\n"
    )
    return check(name, body)


def rename_row(args, where, part, ret=None, *, ok=(), typed=(), errs=()):
    """One rename_spell row (state, not a returned value), see _renamed()."""
    book, old, new = args
    name = (f"row {where[1]}: {where[2]}" if where[0] == "v" else f"hidden: {where[1]}")
    body = (
        "_FN = 'rename_spell'\n"
        f"_OK = {list(ok)!r}\n"
        f"_TYPED = {list(typed)!r}\n"
        "_KIND = {}\n"
        "_NONE = ''\n"
        f"_ROW = {tuple(where)!r}\n"
        "_f = _need('rename_spell', ['book', 'old', 'new'])\n"
        f"_r = _run(_f, {_code(tuple(args))})\n"
        f"_renamed(_r, {old!r}, {new!r}, {part!r}, {ret!r}, {_errs_code(errs)})\n"
    )
    return check(name, body)


def page(cost, affinity=None):
    """A spell page, as the campaign's spell book keeps it."""
    out = {"mana_cost": cost}
    if affinity is not None:
        out["required_affinity"] = affinity
    return out


def sheet(name, mana):
    return {"name": name, "mana": mana}


def hero(name, mana, affinity, strength=None):
    abilities = {"magical_affinity": affinity}
    if strength is not None:
        abilities = {"strength": strength, "magical_affinity": affinity}
    return {"name": name, "mana": mana, "abilities": abilities}


def roster_code(name, sheets):
    """A visible roster, one key a line (phone width)."""
    lines = [f"{name} = ["]
    for s in sheets:
        lines += ["    {", f'        "name": "{s["name"]}",', f'        "mana": {s["mana"]},', "    },"]
    return "\n".join(lines) + "\n]\n"


def book_code(name, book, one_line=False):
    """A visible spell book, one key a line (or one page a line, when the pages keep only the cost)."""
    lines = [f"{name} = {{"]
    for spell, pg in book.items():
        if one_line:
            lines.append(f'    "{spell}": {{"mana_cost": {pg["mana_cost"]}}},')
        else:
            lines.append(f'    "{spell}": {{')
            lines += [f'        "{k}": {v},' for k, v in pg.items()]
            lines.append("    },")
    return "\n".join(lines) + "\n}\n"


def hero_code(name, h):
    lines = [f"{name} = {{", f'    "name": "{h["name"]}",', f'    "mana": {h["mana"]},', '    "abilities": {']
    lines += [f'        "{k}": {v},' for k, v in h["abilities"].items()]
    return "\n".join(lines) + "\n    },\n}\n"


def lines_of(code):
    """Assemble lines: the code's non-blank lines."""
    return [line for line in code.splitlines() if line.strip()]


# =============================================================================================
# UNIT (repeated in every part file of code-challenges): copied verbatim from u08a, which owns the framing
# (written at the same time). Any change goes into u08a, u08b and u08c together.
# =============================================================================================

UNIT = {'id': 'code-challenges',
 'order': 8,
 'title': 'Code Challenges',
 'subtitle': 'Trials of the Yard',
 'published': True,
 'martu_intro': 'Oogrish says a weapon is learned in the yard, not in the book. These are his trials. They are '
                'optional.\n'
                'Lucky asked what is in it for him. Practice, I said. And Oogrish stops lecturing him.\n'
                'Each trial is one small function and a [[test table]]. The visible tests show the idea. The '
                '[[hidden test|hidden tests]] try other values, so a typed answer will not pass. You saw checks '
                'like these in the campaign. Now you can read them.',
 'goals': ['Write a function from its `def` line and a [[test table]]',
           'Make exactly enough count, with `>=` or `<=` at the edge',
           'Handle the [[edge case|edge cases]]: one gap, an empty wall, a tie',
           'Hand back the right kind of value: `True` or `False`, a number, a list, or text',
           "Read a [[hidden test]]'s label and find the case it tries",
           'Turn [[hard-coded]] answers into values worked out from the boxes'],
 'campaign_links': ['leylines-awaken', 'friends-in-low-places']}

GLOSSARY = [
    dict(term="ZeroDivisionError", aliases=["division by zero", "divide by zero"],
         plain="The error Python gives when a program divides by 0. Check for the empty case first.",
         example="if len(crew) == 0:\n    return 0"),
    dict(term="tie", aliases=["ties", "tie-break", "tie-breaker"],
         plain="Two or more items share the best value. The trial's rule says which one wins.",
         example='"Ash" < "Bree"   # True: A comes first'),
    dict(term="average", aliases=["averages", "mean"],
         plain="The total divided by how many there are. With `/`, it can be a decimal.",
         example="(4 + 5) / 2   # 4.5"),
    dict(term="early exit", aliases=["exit early", "leave early"],
         plain="Leaving a loop as soon as you have the answer, with `return` or `break`, so the rest is never read.",
         example="for i in range(len(steps)):\n    if steps[i] > 9:\n        return i"),
]


# =============================================================================================
# T-D-1 "The Price of a Spell": spell_cost(book, name) -> the cost, or 0 if unknown (core)
# =============================================================================================

COST_BOOK = {"Glow": page(2, 3), "Moon Step": page(5, 4)}
COST_OTHER = {"Sun Ward": page(5, 7), "Ember Coat": page(9, 6), "Ash Ward": page(8, 11)}
COST_HEAD = "# Trial: the price of a spell.\ndef spell_cost(book, name):\n"
# Row 3's call, commented out in the starter: the class's slip (no guard) would stop Python on it before Mar'tu's
# checks run, and the explainer alone points the wrong way ("Use a key that is already there").
COST_ROW3 = '# print(spell_cost(book, "Star Fall"))\n'
COST_TAIL = (
    "\n\n" + book_code("book", COST_BOOK) + "\n"
    "# Visible tests. They should show\n"
    "# 2, then 5.\n"
    "# (With only pass, each shows None.)\n"
    'print(spell_cost(book, "Glow"))\n'
    'print(spell_cost(book, "Moon Step"))\n'
    "# Visible test 3, a spell the book\n"
    "# does not have, is in Mar'tu's\n"
    "# table. Once rows 1 and 2 pass, add\n"
    + COST_ROW3
    + "# It should show 0.\n"
)
COST_BODY = "    if name not in book:\n        return 0\n    return book[name][\"mana_cost\"]\n"


def _cost(body="    pass\n", tail=COST_TAIL, head=COST_HEAD):
    return head + body + tail


COST_STARTER = _cost()
COST_SOLUTION = _cost(COST_BODY)
COST_FN = COST_HEAD.split("\n", 1)[1] + COST_BODY
COST_OK = ["Glow", "Moon Step", "Star Fall", "Sun Ward", "Ember Coat", "Ash Ward", "Frost Lace"]
COST_TYPED = ["Glow", "Moon Step", "Star Fall", 2, 5]
COST_ASK = ("Ask the book first: `if name not in book:`, then `return 0`. Without that question, Python stops with a "
            "KeyError for a spell the book does not have.")
COST_KIND = {"dict": 'Return the `"mana_cost"` from the page, not the whole page.'}
COST_SLIPS = [
    (lambda b, n: b[n]["required_affinity"] if n in b else 0,
     'Read the `"mana_cost"` key, not `"required_affinity"`: the trial asks for the cost.'),
]
COST_MISSING = "Hand back 0 for a spell the book does not have: that is the trial's rule, whatever the spell."


def _cost_errs(name):
    return [
        (f"_karg(_e) == {name!r} and not _typed_in()", COST_ASK),
        ("\"'int' object is not subscriptable\" in _B.str(_e)",
         "Ask with `not in` first, then hand back 0: `.get(name, 0)` hands back 0 for a missing spell, and 0 has no keys."),
    ]


def _cost_row(args, want, where):
    return row("spell_cost", ["book", "name"], args, want, where, ok=COST_OK, typed=COST_TYPED,
               errs=_cost_errs(args[1]), slips=COST_SLIPS, kind=COST_KIND,
               fall=COST_MISSING if args[1] not in args[0] else "")


SPELL_COST = dict(
    kind="challenge",
    id="spell-cost",
    title="The Price of a Spell",
    level="core",
    optional=True,
    minutes=6,
    support="light",
    summary="Hand back a spell's mana cost from a spell book, or 0 when the book has no such spell.",
    martu=(
        "Oogrish's first book trial. A function (a recipe) that reads a spell book. Each page has its own "
        "`\"mana_cost\"`.\n"
        "Write `spell_cost(book, name)`. It hands back the cost of the spell called `name`. If the book has no such "
        "spell, it hands back 0.\n"
        "```text\nspell_cost(book, \"Glow\")      → 2\nspell_cost(book, \"Moon Step\") → 5\n"
        "spell_cost(book, \"Star Fall\") → 0\n```\n"
        "Run it and compare with the [[test table]]. Then my [[hidden test|hidden tests]] try other books, yes?"
    ),
    names=["spell_cost", "book", "name"],
    starter=COST_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `spell_cost(book, name)` so every row of the table passes.",
            dictated=False,
            hints=[
                "Each row hands over a book and a name. Find the name's page, then read its `\"mana_cost\"`. Row 3's "
                "name has no page at all.",
                "Ask before you read: `if item not in pack:` then `return 0`. Under that, `return "
                "pack[item][\"weight\"]` reads two keys in a row.",
                "Write `if name not in book:` with `return 0` under it. Below it, write `return "
                "book[name][\"mana_cost\"]`.",
            ],
            checks=[
                _cost_row((COST_BOOK, "Glow"), 2, ("v", 1, 'spell_cost(book, "Glow")', "return 2")),
                _cost_row((COST_BOOK, "Moon Step"), 5, ("v", 2, 'spell_cost(book, "Moon Step")', "return 5")),
                _cost_row((COST_BOOK, "Star Fall"), 0, ("v", 3, 'spell_cost(book, "Star Fall")', "return 0")),
            ],
            pass_line="Oogrish: Steady, now. The table holds.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try new books, and names no book has.",
            dictated=False,
            hints=[
                "The hidden tests hand over other books. Inside the function, use only `book` and `name`: no spell "
                "names and no costs from the table.",
                "A function that asks `if item == \"Rope\":` works for one row only. `pack[item]` works for any pack "
                "and any item.",
                "Keep `return book[name][\"mana_cost\"]` for every name the book has, and `return 0` only under `if "
                "name not in book:`.",
            ],
            checks=[
                _cost_row((COST_OTHER, "Ember Coat"), 9, ("h", "another book")),
                _cost_row((COST_OTHER, "Glow"), 0, ("h", "a name this other book does not have")),
                _cost_row(({}, "Frost Lace"), 0, ("h", "an empty book")),
            ],
            pass_line="Mar'tu: Any book, any name. That is a function, yes?",
        ),
    ],
    solution=COST_SOLUTION,
    assemble=dict(
        lines=lines_of(COST_FN),
        distractors=["    return book[name]", '    return book["name"]["mana_cost"]', '        return "0"'],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Ask: is `name` in `book`? Use `not in`.\n2. Not there: `return 0`.\n3. There: `book[name]` is the "
            "page, and `book[name][\"mana_cost\"]` is the cost on it.")),
        dict(angle="picture", label="Two keys in a row", text=(
            "```text\nbook[\"Glow\"]\n  → the Glow page\nbook[\"Glow\"][\"mana_cost\"]\n  → 2\n"
            "book[\"Star Fall\"]\n  → KeyError: no page\n```\nAsk with `not in` before the read that would stop.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`cast_spell` asked `if spell_name not in caster[\"spell_book\"]:` before it read a page. Same guard "
            "here. This time the answer for a missing page is 0.")),
    ],
    predict=dict(
        q="Before you write it: what do these two lines print?",
        code='pack = {"Rope": {"weight": 3}}\nprint("Lamp" in pack)\nprint(pack["Rope"]["weight"])\n',
        choices=["True\n3", "False\n3", "False\nweight"],
        answer=1,
        explain="`in` asks about the keys: no `\"Lamp\"` key, so `False`, and no error. Two keys in a row read the "
                "value inside the inner page.",
    ),
    pair_talk="Read row 3 of the table to your partner: what goes in, and what should come back? Then say why "
              "`book[name]` alone would stop Python on that row.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        why=(
            "You have seen this question at the top of `cast_spell`: `if spell_name not in caster[\"spell_book\"]:`. "
            "It kept a missing spell from stopping Python. Here a missing spell costs 0."
        ),
    ),
    takeaway="Ask `not in` before you read a key, and hand back the default for a name the book does not have.",
    wrong_answers=[
        dict(why="the starter (pass)", code=COST_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="no guard, in the starter as given (row 3's call is a comment): Mar'tu's KeyError message",
             code=_cost('    return book[name]["mana_cost"]\n'), fails_at=1, message_contains="Ask the book first"),
        dict(why="no guard, with row 3's call added back as the starter says: Python's own KeyError stops it first",
             code=_cost('    return book[name]["mana_cost"]\n', tail=COST_TAIL.replace(COST_ROW3, COST_ROW3[2:])),
             fails_at=0, message_contains="KeyError: 'Star Fall'"),
        dict(why="the guard after the read (the work first)",
             code=_cost('    cost = book[name]["mana_cost"]\n    if name not in book:\n        return 0\n'
                        "    return cost\n", tail=""), fails_at=1, message_contains="Ask the book first"),
        dict(why="the whole table typed in as an if-chain (passes every visible row; the hidden tests catch it)",
             code=_cost('    if name == "Glow":\n        return 2\n    if name == "Moon Step":\n        return 5\n'
                        "    return 0\n"), fails_at=2, message_contains="typed in it"),
        dict(why="row 1's answer typed (return 2)", code=_cost("    return 2\n"), fails_at=1,
             message_contains="`2` typed in it"),
        dict(why="a name from the table typed in the read", code=_cost(
            '    if name not in book:\n        return 0\n    return book["Glow"]["mana_cost"]\n'), fails_at=1,
             message_contains='`"Glow"` typed in it'),
        dict(why="print instead of return",
             code=_cost('    if name not in book:\n        print(0)\n    else:\n'
                        '        print(book[name]["mana_cost"])\n'), fails_at=1,
             message_contains="Use `return`, not `print`"),
        dict(why="the whole page returned", code=_cost("    if name not in book:\n        return 0\n"
                                                       "    return book[name]\n"), fails_at=1,
             message_contains="not the whole page"),
        dict(why="the wrong key (required_affinity)",
             code=_cost('    if name not in book:\n        return 0\n    return book[name]["required_affinity"]\n'),
             fails_at=1, message_contains='not `"required_affinity"`'),
        dict(why='text "0" for a missing spell (the wrong type)',
             code=_cost('    if name not in book:\n        return "0"\n    return book[name]["mana_cost"]\n'),
             fails_at=1, message_contains="Hand back a number, not text"),
        dict(why="an if with no return for a missing spell (None)",
             code=_cost('    if name in book:\n        return book[name]["mana_cost"]\n'), fails_at=1,
             message_contains="Give every path a `return`"),
        dict(why='a quoted parameter, book["name"] (the bottom prints: Python\'s KeyError)',
             code=_cost('    if name not in book:\n        return 0\n    return book["name"]["mana_cost"]\n'),
             fails_at=0, message_contains="KeyError: 'name'"),
        dict(why='a quoted parameter, book["name"], the prints gone',
             code=_cost('    if name not in book:\n        return 0\n    return book["name"]["mana_cost"]\n',
                        tail=""), fails_at=1, message_contains='Take the quotes off `"name"`'),
        dict(why=".get(name) then a key: None is not subscriptable",
             code=_cost('    return book.get(name)["mana_cost"]\n', tail=""), fails_at=1,
             message_contains="`.get()` hands back `None`"),
        dict(why=".get(name, 0) then a key: 0 is not subscriptable",
             code=_cost('    return book.get(name, 0)["mana_cost"]\n', tail=""), fails_at=1,
             message_contains="`.get(name, 0)` hands back 0"),
        dict(why="a page added for the missing spell (the book handed in is changed)",
             code=_cost('    if name not in book:\n        book[name] = {"mana_cost": 0}\n'
                        '    return book[name]["mana_cost"]\n'), fails_at=1,
             message_contains="Leave `book` as it was"),
        dict(why="the parameters in the other order (the table read backwards)",
             code=_cost(COST_BODY, head=COST_HEAD.replace("(book, name)", "(name, book)"), tail=""), fails_at=1,
             message_contains="in the order of the first line"),
        dict(why="row 3 typed as its own guard, no real guard (the hidden missing name stops; its name is not shown)",
             code=_cost('    if name == "Star Fall":\n        return 0\n    return book[name]["mana_cost"]\n'), fails_at=2,
             message_contains='`"Star Fall"` typed in it'),
        dict(why="-1 for a missing spell (not the trial's default)",
             code=_cost('    if name not in book:\n        return -1\n    return book[name]["mana_cost"]\n'), fails_at=1,
             message_contains="Hand back 0 for a spell the book does not have"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries", opens="after Unit 5", ceiling="Units 1-5",
             skills="dict-read-nested,not-in-guard,return-value", solo="false", dictates="",
             foreign_names="pack,item,weight,Rope,Lamp",
             par="another book (Ember Coat 9); a name this other book does not have (Glow); an empty book") + "\n"
        "T-D-1. The visible book is Lucky's two pages (both keys, as the campaign's pages); the hidden book has three "
        "other spells, and its missing name is Glow, a name that IS in the table's book, so a typed `if name == "
        "\"Star Fall\": return 0` and a read of the table's own book both fail. The KeyError for an unknown spell is "
        "the class's slip. Row 3's call is a comment in the starter (\"Once rows 1 and 2 pass, add ...\"), so the "
        "slip reaches Mar'tu's check and gets 'Ask the book first' (fails_at 1); with the call added back it is "
        "Python's own KeyError at the bottom print (fails_at 0, the explainer's row, which points the wrong way: "
        "\"Use a key that is already there\"). The call line is 38 characters, whole (a wrapped call reads as "
        "broken code). `.get()` answers pass (`book.get(name, {\"mana_cost\": 0})[\"mana_cost\"]`), and so does "
        "`if name in book:` / `return 0`. Show-rung copy-test (each rung pasted word for word in place of `pass`, "
        "and again with `pass` kept below it): CP1's rung is the whole function: no crash, every checkpoint "
        "passes; CP2's rung keeps it."
    ),
)


# =============================================================================================
# T-D-1a "The Cheapest Spell": cheapest_spell(book) -> the name of the cheapest spell (advanced; a loop, so it
# opens after Unit 6). A tie keeps the first spell in the book.
# =============================================================================================


def _costs(pairs):
    return {name: page(cost) for name, cost in pairs}


CHEAP_BOOK = _costs([("Warm Hands", 4), ("Ember Coat", 3), ("Moon Step", 5), ("Glow", 2), ("Quiet Step", 3)])
CHEAP_WARDS = _costs([("Sun Ward", 9), ("Ash Ward", 7)])
CHEAP_TIES = _costs([("Quiet Step", 5), ("Moon Step", 5), ("Hedge Hop", 6)])
CHEAP_HEAD = "# Trial: the cheapest spell.\ndef cheapest_spell(book):\n"
CHEAP_TAIL = (
    "\n\n" + book_code("book", CHEAP_BOOK, True) + book_code("wards", CHEAP_WARDS, True)
    + book_code("ties", CHEAP_TIES, True) + "\n"
    "# Visible tests. They should show\n"
    "# Glow, Ash Ward, then Quiet Step.\n"
    "# (With only pass, each shows None.)\n"
    "print(cheapest_spell(book))\n"
    "print(cheapest_spell(wards))\n"
    "print(cheapest_spell(ties))\n"
)
CHEAP_BODY = (
    '    best = ""\n'
    "    low = 0\n"
    "    for name, page in book.items():\n"
    '        cost = page["mana_cost"]\n'
    '        if best == "" or cost < low:\n'
    "            best = name\n"
    "            low = cost\n"
    "    return best\n"
)


def _cheap(body="    pass\n", tail=CHEAP_TAIL):
    return CHEAP_HEAD + body + tail


CHEAP_STARTER = _cheap()
CHEAP_SOLUTION = _cheap(CHEAP_BODY)
CHEAP_FN = CHEAP_HEAD.split("\n", 1)[1] + CHEAP_BODY
CHEAP_OK = ["Warm Hands", "Moon Step", "Glow", "Quiet Step", "Sun Ward", "Ash Ward", "Hedge Hop", "Star Fall",
            "Frost Lace", "Ember Coat"]
CHEAP_TYPED = ["Glow", "Ash Ward", "Quiet Step"]


def _first_low(book, strict=True, start=None, zero_unset=False, big=False):
    best, low = "", (1000 if big else (0 if start is None else start))
    for name, pg in book.items():
        cost = pg["mana_cost"]
        if big:
            better = cost < low
        elif zero_unset:
            better = low == 0 or cost < low
        else:
            better = best == "" or (cost < low if strict else cost <= low)
        if better:
            best, low = name, cost
    return best


CHEAP_SLIPS = [
    (lambda b: _first_low(b, strict=False),
     "On a tie, keep the first spell: use `<`, so an equal cost does not replace it.", "_uses('op:LtE')"),
    (lambda b: min(b), "`min(book)` finds the name that comes first in the alphabet, not the cheapest spell. Compare "
                       "each page's `\"mana_cost\"`.", "_uses('call:min')"),
    (lambda b: _first_low(b, big=True),
     "Start from the book's own first spell, not a typed number: every cost in this book is higher than your start."),
    (lambda b: _first_low(b, zero_unset=True),
     "Don't use 0 to mean \"no spell yet\": a spell can cost 0. Use `best == \"\"` for that."),
    (lambda b: next(iter(b)), "Put `return` after the loop, not inside it: your function stopped at the first spell.",
     "_ret_in_loop()"),
    (lambda b: next(iter(b)), "When you keep a new name, keep its cost too: `low = cost` on the same pass. Yours kept "
                              "the first spell's name, and nothing ever beat the old `low`."),
    (lambda b: max(b, key=lambda n: b[n]["mana_cost"]),
     "Cheapest means the lowest cost: use `<`, not `>`.", "_uses('op:Gt')"),
    (lambda b: list(b)[-1], "Compare before you keep a name: `if ... cost < low:`, then keep it. Your function kept "
                            "the last spell."),
    (lambda b: min(n for n in b if b[n]["mana_cost"] == min(p["mana_cost"] for p in b.values())),
     "On a tie, the spell that comes first in the book wins, not the one first in the alphabet. With `<`, a later "
     "spell must cost less to take over."),
    (lambda b: min(b), "Compare the costs, `page[\"mana_cost\"]`, not the spell names: comparing names finds the one "
                       "first in the alphabet."),
]
CHEAP_KIND = {"int": "Hand back the spell's name, not its cost: keep the name in its own variable as you loop.",
              "dict": "Hand back the spell's name, not its page."}
CHEAP_ERRS = [
    ("_karg(_e) == 'mana_cost'",
     "Read the cost from each page, `page[\"mana_cost\"]`: the book's own keys are spell names, not `\"mana_cost\"`."),
    ("'string indices' in _B.str(_e)",
     "A `for` loop over a book hands you each spell's name, not its page. Loop over `book.items()` to get both, or "
     "read the page with `book[name]`."),
]


def _cheap_row(book, want, where):
    return row("cheapest_spell", ["book"], (book,), want, where, ok=CHEAP_OK, typed=CHEAP_TYPED, errs=CHEAP_ERRS,
               slips=CHEAP_SLIPS, kind=CHEAP_KIND)


CHEAPEST_SPELL = dict(
    kind="challenge",
    id="cheapest-spell",
    title="The Cheapest Spell",
    level="advanced",
    variant_of="spell-cost",
    optional=True,
    minutes=10,
    support="light",
    tracer=True,
    summary="The advanced twin of The Price of a Spell: loop over a whole book and hand back the name of its cheapest "
            "spell.",
    martu=(
        "The advanced book trial. It needs a loop, so it opens after the Loops unit.\n"
        "Write `cheapest_spell(book)`. It hands back the *name* of the spell with the lowest `\"mana_cost\"`. On a "
        "[[tie]], the spell that comes first in the book wins. These pages keep only the cost.\n"
        "```text\ncheapest_spell(book)  → \"Glow\"\ncheapest_spell(wards) → \"Ash Ward\"\n"
        "cheapest_spell(ties)  → \"Quiet Step\"\n```\n"
        "Then my hidden tests hand over books you have not seen, yes?"
    ),
    names=["cheapest_spell", "book"],
    starter=CHEAP_STARTER,
    checkpoints=[
        dict(
            id="cheapest",
            text="Write `cheapest_spell(book)` so rows 1 and 2 of the table pass.",
            dictated=False,
            hints=[
                "Walk the book with a `for` loop, one page at a time. Keep two things as you go: the best name so far, "
                "and its cost.",
                "With other names: `for name, jar in shelf.items():` hands you each key and its value. Inside, `if "
                "jar[\"size\"] < smallest:` asks about one jar.",
                "Write `best = \"\"` and `low = 0` before the loop. Then `for name, page in book.items():` with "
                "`cost = page[\"mana_cost\"]` inside, and under it `if best == \"\" or cost < low:` (or `<=`: row 3 "
                "decides) with `best = name` and `low = cost`. Then `return best` after the loop.",
            ],
            checks=[
                _cheap_row(CHEAP_BOOK, "Glow", ("v", 1, "cheapest_spell(book)", 'return "Glow"')),
                _cheap_row(CHEAP_WARDS, "Ash Ward", ("v", 2, "cheapest_spell(wards)", 'return "Ash Ward"')),
            ],
            pass_line="Oogrish: Good. You read every page before you chose.",
        ),
        dict(
            id="a-tie",
            text="Make row 3 pass: on a tie, the spell that comes first in the book wins.",
            dictated=False,
            hints=[
                "Row 3 has two spells at 5. The first one in the book wins, so a later spell must cost *less* to "
                "replace it.",
                "`<` is `False` when two numbers are equal, so an equal cost keeps the first. `<=` lets an equal cost "
                "take over.",
                "Write `if best == \"\" or cost < low:`, with `<`, not `<=`.",
            ],
            checks=[_cheap_row(CHEAP_TIES, "Quiet Step", ("v", 3, "cheapest_spell(ties)", 'return "Quiet Step"'))],
            pass_line="Lucky: First come, first served. Fair.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try costly books, free spells and one-spell books.",
            dictated=False,
            hints=[
                "The hidden books are new. Start with no spell yet, `best = \"\"`, never a typed cost such as 100.",
                "`best = \"\"` can mean \"no spell yet\". Then `if best == \"\" or cost < low:` keeps the first spell, "
                "whatever it costs.",
                "Write `best = \"\"` and `low = 0` before the loop, and keep `if best == \"\" or cost < low:` inside "
                "it.",
            ],
            checks=[
                _cheap_row(_costs([("Sun Ward", 1500000), ("Star Fall", 1200000), ("Frost Lace", 1300000)]),
                           "Star Fall", ("h", "very costly spells")),
                _cheap_row(_costs([("Hedge Hop", 0), ("Glow", 2), ("Moon Step", 5)]), "Hedge Hop",
                           ("h", "a free spell first")),
                _cheap_row(_costs([("Ember Coat", 6)]), "Ember Coat", ("h", "a book with one spell")),
                _cheap_row(_costs([("Sun Ward", 9), ("Quiet Step", 4), ("Ember Coat", 4)]), "Quiet Step",
                           ("h", "a tie near the end")),
                _cheap_row(_costs([("Frost Lace", 3), ("Ash Ward", 8), ("Ember Coat", 6)]), "Frost Lace",
                           ("h", "another book")),
            ],
            pass_line="Mar'tu: Any book. Even a book of one, yes?",
        ),
    ],
    solution=CHEAP_SOLUTION,
    assemble=dict(
        lines=lines_of(CHEAP_FN),
        distractors=["        if cost <= low:", "    return low", "    low = 100"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Before the loop: `best = \"\"` and `low = 0`.\n2. For each name and page, read the cost.\n3. No best "
            "yet, or a lower cost? Keep this name and this cost.\n4. After the loop, hand back `best`.")),
        dict(angle="in Tor", label="Oogrish at the market", text=(
            "Oogrish walks the stalls holding the cheapest pie he has seen so far. A cheaper one? He swaps. The same "
            "price? He keeps the pie already in his hand. At the end of the row, he names the pie in his hand.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "You filled every hero's spell book with `add_spell(...)`. A book is a dictionary of pages, and "
            "`for name, page in book.items():` reads every page, the way `for member in party.members:` read every "
            "hero.")),
    ],
    pair_talk="Row 3 has a tie. Tell your partner which sign keeps the first spell, `<` or `<=`, and why.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="for member in party.members:",
        why=(
            "The loop at the bottom of the spell book walked every member. This one walks every page of a book, and "
            "keeps the cheapest."
        ),
    ),
    takeaway="To find the lowest, keep the best so far and its value, compare each item with `<`, and hand back the answer after "
             "the loop.",
    wrong_answers=[
        dict(why="the starter (pass)", code=CHEAP_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the cost returned, not the name (the wrong type)",
             code=_cheap(CHEAP_BODY.replace("    return best\n", "    return low\n")), fails_at=1,
             message_contains="not its cost"),
        dict(why="<= keeps the last spell of a tie (also Show me how for rows 1 and 2, pasted word for word with "
                 "its other sign, `or <=: row 3 decides`: no crash, rows 1-2 pass, row 3 decides)",
             code=_cheap(CHEAP_BODY.replace("cost < low", "cost <= low")),
             fails_at=2, message_contains="keep the first spell"),
        dict(why="min(book): the alphabet, not the cost", code=_cheap("    return min(book)\n"), fails_at=1,
             message_contains="`min(book)`"),
        dict(why="a typed start of 100 (passes the table; the hidden costly book catches it)",
             code=_cheap('    best = ""\n    low = 100\n    for name, page in book.items():\n'
                         '        if page["mana_cost"] < low:\n            best = name\n'
                         '            low = page["mana_cost"]\n    return best\n'), fails_at=3,
             message_contains="not a typed number"),
        dict(why="0 used to mean 'nothing yet' (a free spell first)",
             code=_cheap(CHEAP_BODY.replace('best == "" or cost < low', "low == 0 or cost < low")), fails_at=3,
             message_contains="a spell can cost 0"),
        dict(why="return inside the loop (the first spell)",
             code=_cheap("    for name, page in book.items():\n        return name\n"), fails_at=1,
             message_contains="after the loop, not inside it"),
        dict(why="> (the most costly spell)",
             code=_cheap(CHEAP_BODY.replace("cost < low", "cost > low")), fails_at=1, message_contains="use `<`"),
        dict(why="no comparison: the last spell kept",
             code=_cheap('    best = ""\n    for name, page in book.items():\n        best = name\n    return best\n'),
             fails_at=1, message_contains="Compare before you keep"),
        dict(why="a name from the table typed", code=_cheap('    return "Glow"\n'), fails_at=1,
             message_contains='`"Glow"` typed in it'),
        dict(why="print instead of return", code=_cheap(CHEAP_BODY.replace("    return best\n", "    print(best)\n")),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="the book read like a page (book[\"mana_cost\"])",
             code=_cheap('    for name in book:\n        cost = book["mana_cost"]\n    return name\n', tail=""),
             fails_at=1, message_contains="the book's own keys are spell names"),
        dict(why="the names compared, not the costs (row 1's alphabet-first name is not the cheapest)",
             code=_cheap('    best = ""\n    for name in book:\n        if best == "" or name < best:\n'
                         '            best = name\n    return best\n'), fails_at=1, message_contains="not the spell names"),
        dict(why="a tie settled by the alphabet (the variant rule of lowest-with-ties), not by the book's order",
             code=_cheap('    pairs = []\n    for name in book:\n        pairs.append([book[name]["mana_cost"], name])\n'
                         '    return sorted(pairs)[0][1]\n'), fails_at=2, message_contains="not the one first in the alphabet"),
        dict(why="low never updated: the first spell's name kept (return is after the loop)",
             code=_cheap(CHEAP_BODY.replace("            low = cost\n", "")), fails_at=1,
             message_contains="keep its cost too"),
        dict(why="a typed start of 9999 (very costly spells catch it)",
             code=_cheap('    best = ""\n    low = 9999\n    for name, page in book.items():\n'
                         '        if page["mana_cost"] < low:\n            best = name\n'
                         '            low = page["mana_cost"]\n    return best\n'), fails_at=3,
             message_contains="not a typed number"),
        dict(why="for page in book: the loop hands over names, not pages",
             code=_cheap('    best = ""\n    low = 0\n    for page in book:\n        cost = page["mana_cost"]\n'
                         '        if best == "" or cost < low:\n            best = page\n            low = cost\n'
                         '    return best\n', tail=""), fails_at=1, message_contains="each spell's name, not its page"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries (advanced)", opens="after Unit 6",
             ceiling="Units 1-6", skills="loop-dict-items,find-lowest,tie-break,return-value", solo="false",
             dictates="", foreign_names="shelf,jar,size,smallest",
             par="very costly spells; a free spell first; a book with one spell; a tie near the end; another book")
        + "\n"
        "T-D-1a, variant_of spell-cost (the spec: 'cheapest_spell(book), a loop; opens after Unit 6'). The pages "
        "keep only the cost here (one page a line, phone width). The spec gives no tie rule; Mar'tu states one (the "
        "first in the book), which is what a strict `<` does, so the class's `<` versus `<=` slip has a home here "
        "too. Row 1's book has five spells so that the first spell, the last spell, the most costly and the "
        "alphabet-first name (Ember Coat) all differ from the answer, so each slip gets its own message on the "
        "first row (comparing names, or `min(book)`, fails row 1, not the tie). Row 3's tie puts the alphabet-later "
        "spell first (Quiet Step before Moon Step), so a tie settled by the alphabet fails it, as `<=` does. The costly hidden book (1,200,000 "
        "and up) catches a typed start of 100, 9999 or even 1000000; the free spell first catches 0 used as "
        "'nothing yet'. "
        "No partial: the tie is not a separate step of code (a strict `<` already handles it). Show-rung copy-test: "
        "CP cheapest's rung (best, low, the loop, the `if` with both updates under it, `return best`; it used to "
        "say \"keep best and low\" and start neither) is the solution: no crash, every checkpoint passes; with its "
        "other sign, `<=` (\"row 3 decides\"), rows 1-2 pass and row 3 fails 'keep the first spell' (wrong_answers). "
        "CP a-tie's and CP hidden-tests' rungs keep `<`. The hidden-tests Where to look now says `best = \"\"` means "
        "no spell yet, never a typed cost, so it no longer contradicts the rung's `low = 0`."
    ),
)


# =============================================================================================
# T-D-2 "Read the Affinity": affinity_of(hero) -> the nested read (core)
# =============================================================================================

AFF_LUCKY = hero("Lucky", 20, 13, strength=16)
AFF_OOGRISH = hero("Oogrish", 14, 9, strength=11)
AFF_HEAD = "# Trial: read the affinity.\ndef affinity_of(hero):\n"
AFF_TAIL = (
    "\n\n" + hero_code("lucky", AFF_LUCKY) + hero_code("oogrish", AFF_OOGRISH) + "\n"
    "# Visible tests. They should show\n"
    "# 13, then 9.\n"
    "# (With only pass, each shows None.)\n"
    "print(affinity_of(lucky))\n"
    "print(affinity_of(oogrish))\n"
)
AFF_BODY = '    card = hero["abilities"]\n    return card["magical_affinity"]\n'


def _aff(body="    pass\n", tail=AFF_TAIL):
    return AFF_HEAD + body + tail


AFF_STARTER = _aff()
AFF_SOLUTION = _aff(AFF_BODY)
AFF_FN = AFF_HEAD.split("\n", 1)[1] + AFF_BODY
AFF_OK = ["Lucky", "Oogrish", "Pell", "Moth", "Glug"]
AFF_TYPED = ["Lucky", "Oogrish", 13, 9]
_AFF_POS = ("Read the card by its key, `card[\"magical_affinity\"]`, not by position: another hero's card can hold "
            "its abilities in another order.")
AFF_SLIPS = [
    (lambda h: list(h["abilities"].values())[1], _AFF_POS, "_uses('attr:values')"),
    (lambda h: list(h["abilities"].values())[-1], _AFF_POS, "_uses('attr:values')"),
    (lambda h: h["mana"], "That is the hero's `\"mana\"`. Read `\"magical_affinity\"`, on the inner card "
                          "`\"abilities\"`."),
    (lambda h: h["abilities"].get("strength"), "Read `\"magical_affinity\"`, not `\"strength\"`: both sit on the "
                                               "`\"abilities\"` card.", "_has('strength')"),
]
AFF_KIND = {"dict": "Read one more key: `hero[\"abilities\"]` is the inner card, and its `\"magical_affinity\"` is "
                    "the number."}


def _aff_row(h, want, where):
    return row("affinity_of", ["hero"], (h,), want, where, ok=AFF_OK, typed=AFF_TYPED, slips=AFF_SLIPS,
               kind=AFF_KIND)


AFFINITY_OF = dict(
    kind="challenge",
    id="affinity-of",
    title="Read the Affinity",
    level="core",
    optional=True,
    minutes=5,
    support="light",
    summary="Hand back a hero's magical affinity, read from the inner `\"abilities\"` card of the stat sheet.",
    martu=(
        "A short trial, and a famous one. A function (a recipe) that reads one value from inside a sheet. A hero's "
        "`\"magical_affinity\"` is not on the big sheet. It sits on the inner card, `\"abilities\"`.\n"
        "Write `affinity_of(hero)`. It hands back the hero's magical affinity.\n"
        "```text\naffinity_of(lucky)   → 13\naffinity_of(oogrish) → 9\n```\n"
        "My hidden tests hand over heroes you have not met, yes?"
    ),
    names=["affinity_of", "hero"],
    starter=AFF_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `affinity_of(hero)` so both rows of the table pass.",
            dictated=False,
            hints=[
                "The affinity sits on the inner card, `\"abilities\"`. Read two keys, the outer one first.",
                "With other names: `inner = pack[\"pocket\"]` reads the inner card, then `inner[\"coins\"]` reads one "
                "value from it.",
                "Write `card = hero[\"abilities\"]`, then `return card[\"magical_affinity\"]`.",
            ],
            checks=[
                _aff_row(AFF_LUCKY, 13, ("v", 1, "affinity_of(lucky)", "return 13")),
                _aff_row(AFF_OOGRISH, 9, ("v", 2, "affinity_of(oogrish)", "return 9")),
            ],
            pass_line="Oogrish: Two keys, in order. Steady.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They hand over new heroes.",
            dictated=False,
            hints=[
                "The hidden tests hand over other heroes. Read from `hero`, the sheet the function is handed, never "
                "from `lucky` or `oogrish`.",
                "A function reads its parameter. It reads the sheet the call hands it, so `coins_of(pack)` works "
                "for any pack.",
                "Keep `card = hero[\"abilities\"]`, so the read follows whichever sheet comes in.",
            ],
            checks=[
                _aff_row(hero("Pell", 7, 11, strength=4), 11, ("h", "another hero")),
                _aff_row({"name": "Moth", "mana": 30, "abilities": {"wisdom": 8, "strength": 3,
                                                                    "magical_affinity": 14, "dexterity": 12}},
                         14, ("h", "a hero with more abilities")),
                _aff_row(hero("Glug", 5, 0, strength=18), 0, ("h", "an affinity of 0")),
            ],
            pass_line="Mar'tu: Any hero. You have read this line before, in the barrier. Now it is yours.",
        ),
    ],
    solution=AFF_SOLUTION,
    assemble=dict(
        lines=lines_of(AFF_FN),
        distractors=['    return hero["magical_affinity"]', '    return card', '    card = hero["name"]'],
    ),
    another_way=[
        dict(angle="picture", label="Cards in cards", text=(
            "```text\nhero\n ├ \"name\" → \"Lucky\"\n ├ \"mana\" → 20\n └ \"abilities\"\n"
            "     ├ \"strength\" → 16\n     └ \"magical_affinity\"\n          → 13\n```\n"
            "Outer key first, then the inner one.")),
        dict(angle="shorter", text=(
            "One line does both reads: `return hero[\"abilities\"][\"magical_affinity\"]`. Python reads it left to "
            "right, one key at a time.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`cast_spell` read `caster[\"abilities\"][\"magical_affinity\"]` to see if the caster was skilled enough. "
            "Same two keys, in a function of your own.")),
    ],
    pair_talk="Tell your partner which key comes first, and why `hero[\"magical_affinity\"]` on its own stops Python.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        why=(
            "You read this value when you held the barrier: `caster[\"abilities\"][\"magical_affinity\"]`. Now a "
            "function of your own reads it, for any hero."
        ),
    ),
    takeaway="A nested read names the outer key first, then the inner one.",
    wrong_answers=[
        dict(why="the starter (pass)", code=AFF_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="a skipped level (the bottom prints: Python's KeyError)",
             code=_aff('    return hero["magical_affinity"]\n'), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="a skipped level, the prints gone", code=_aff('    return hero["magical_affinity"]\n', tail=""),
             fails_at=1, message_contains="Go one level in"),
        dict(why="the keys in the wrong order", code=_aff('    return hero["magical_affinity"]["abilities"]\n',
                                                          tail=""), fails_at=1, message_contains="Go one level in"),
        dict(why="the inner card returned (one read short)", code=_aff('    return hero["abilities"]\n'), fails_at=1,
             message_contains="Read one more key"),
        dict(why='a quoted parameter ("hero"[...]): the bottom prints stop with a TypeError',
             code=_aff('    return "hero"["abilities"]["magical_affinity"]\n'), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why='a quoted parameter, the prints gone',
             code=_aff('    return "hero"["abilities"]["magical_affinity"]\n', tail=""), fails_at=1,
             message_contains="take the quotes off"),
        dict(why="keys with no quotes (hero[abilities]), the prints gone",
             code=_aff("    return hero[abilities][magical_affinity]\n", tail=""), fails_at=1,
             message_contains="Put quotes around the key"),
        dict(why="the top-level sheet read inside the function (lucky for hero)",
             code=_aff('    card = lucky["abilities"]\n    return card["magical_affinity"]\n'), fails_at=1,
             message_contains="Use the parameter `hero`, not `lucky`"),
        dict(why="row 1's answer typed (return 13)", code=_aff("    return 13\n"), fails_at=1,
             message_contains="`13` typed in it"),
        dict(why="the table typed as an if-chain on the name (the hidden heroes catch it)",
             code=_aff('    if hero["name"] == "Lucky":\n        return 13\n    return 9\n'), fails_at=2,
             message_contains="typed in it"),
        dict(why="print instead of return", code=_aff('    print(hero["abilities"]["magical_affinity"])\n'),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="str() around the answer (text, not a number)",
             code=_aff('    card = hero["abilities"]\n    return str(card["magical_affinity"])\n'), fails_at=1,
             message_contains="Hand back a number, not text"),
        dict(why="the mana read instead", code=_aff('    return hero["mana"]\n'), fails_at=1,
             message_contains="That is the hero's `\"mana\"`"),
        dict(why="the strength read instead", code=_aff('    return hero["abilities"]["strength"]\n'), fails_at=1,
             message_contains="not `\"strength\"`"),
        dict(why="read by position, not by key (the second value on the card): Moth's card catches it",
             code=_aff('    return list(hero["abilities"].values())[1]\n'), fails_at=2,
             message_contains="not by position"),
        dict(why="a dot for a key (hero.abilities), the prints gone",
             code=_aff("    return hero.abilities\n", tail=""), fails_at=1, message_contains="square brackets"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries", opens="after Unit 5", ceiling="Units 1-5",
             skills="dict-read-nested,param-use,return-value", solo="false", dictates="",
             foreign_names="pack,pocket,coins,inner",
             par="another hero (Pell 11); a hero with more abilities (Moth 14); an affinity of 0 (Glug)") + "\n"
        "T-D-2. Two visible rows (the spec allows 2-3): Lucky 13 and Oogrish 9 from the party table, with mana and "
        "strength chosen so that a read of the wrong key never gives the right answer. The solution reads in two "
        "steps (`card = hero[\"abilities\"]`) to keep every line within 36 characters; the one-line read passes "
        "and is the 'shorter' angle. The top-level sheets are `lucky` and `oogrish`, not `hero`, so a read of a "
        "top-level sheet inside the function is caught by name (Unit 7's slip). Moth's card holds the affinity third, "
        "after wisdom and strength, so a read by position (`list(...values())[1]` or `[-1]`) fails a hidden test. "
        "Show-rung copy-test: CP1's rung is the solution (no crash, every checkpoint passes); CP2's rung keeps it."
    ),
)


# =============================================================================================
# T-D-2a "Can They Cast It?": meets(hero, spell) -> both checks, nested, exactly enough counts (advanced)
# =============================================================================================

MEETS_LUCKY = hero("Lucky", 8, 13)
MEETS_GLOW = page(2, 3)
MEETS_WARD = page(6, 14)
MEETS_STRENGTHEN = page(10, 8)
MEETS_HEAD = "# Trial: can this hero cast it?\ndef meets(hero, spell):\n"


def _spell_code(name, pg):
    return f"{name} = {{\n" + "".join(f'    "{k}": {v},\n' for k, v in pg.items()) + "}\n"


MEETS_TAIL = (
    "\n\n" + hero_code("lucky", MEETS_LUCKY) + _spell_code("glow", MEETS_GLOW) + _spell_code("ward", MEETS_WARD)
    + _spell_code("strengthen", MEETS_STRENGTHEN) + "\n"
    "# Visible tests. They should show\n"
    "# True, False, then False.\n"
    "# (With only pass, each shows None.)\n"
    "print(meets(lucky, glow))\n"
    "print(meets(lucky, ward))\n"
    "print(meets(lucky, strengthen))\n"
)
MEETS_READS = (
    '    card = hero["abilities"]\n'
    '    skill = card["magical_affinity"]\n'
    '    req = spell["required_affinity"]\n'
    '    cost = spell["mana_cost"]\n'
    "    if skill < req:\n"
    "        return False\n"
)
MEETS_BODY = MEETS_READS + '    return hero["mana"] >= cost\n'
# The Show me how rungs, pasted word for word: the affinity step (card, skill, req, the turn-away), then the mana
# step's `cost` line before its `return` (wrong_answers prove each sign, and that the hidden tests decide).
MEETS_RUNG1 = (
    '    card = hero["abilities"]\n'
    '    skill = card["magical_affinity"]\n'
    '    req = spell["required_affinity"]\n'
    "    if skill < req:\n"
    "        return False\n"
)
MEETS_RUNG2 = '    cost = spell["mana_cost"]\n'


def _meets(body="    pass\n", tail=MEETS_TAIL):
    return MEETS_HEAD + body + tail


MEETS_STARTER = _meets()
MEETS_SOLUTION = _meets(MEETS_BODY)
MEETS_FN = MEETS_HEAD.split("\n", 1)[1] + MEETS_BODY
MEETS_TYPED = [3, 14, 2, 6, 10, 8, 13]
MEETS_KEEP = ("Only ask, don't spend: `meets` answers a question and leaves both sheets as they were. Spending the "
              "mana is `cast_spell`'s job.")


def _aff_of(h):
    return h["abilities"]["magical_affinity"]


_M_HAS = "Hand back `True` when the hero has enough: the hero's value on the left, then `>=`, then the spell's value."
_M_AND = "Both must be true: join the two questions with `and`, not `or`."
_M_AFF = "Check the affinity too: the hero's `\"magical_affinity\"` must be at least the spell's `\"required_affinity\"`."
_M_MANA = "Check the mana too: the hero's `\"mana\"` must be at least the spell's `\"mana_cost\"`."
_M_PAIR = ("Compare each value with its partner: the affinity with `\"required_affinity\"`, and the mana with "
           "`\"mana_cost\"`.")
_M_EXACT = "Exactly enough counts: use `>=`, *at least*, not `>`. Or turn away with `<`, which is `False` when equal."
_M_SLIP = {
    "has": (lambda h, s: _aff_of(h) < s["required_affinity"] or h["mana"] < s["mana_cost"], _M_HAS),
    "and": (lambda h, s: _aff_of(h) >= s["required_affinity"] or h["mana"] >= s["mana_cost"], _M_AND,
            "_uses('op:Or')"),
    "aff": (lambda h, s: _aff_of(h) >= s["required_affinity"], _M_MANA, "not _has('mana')"),
    "mana": (lambda h, s: h["mana"] >= s["mana_cost"], _M_AFF),
    "pair": (lambda h, s: _aff_of(h) >= s["mana_cost"] and h["mana"] >= s["required_affinity"], _M_PAIR),
    "exact": (lambda h, s: _aff_of(h) > s["required_affinity"] and h["mana"] > s["mana_cost"], _M_EXACT),
}


def _meets_row(h, s, want, where, slips=()):
    return row("meets", ["hero", "spell"], (h, s), want, where, ok=[], typed=MEETS_TYPED,
               slips=[_M_SLIP[k] for k in slips], keepmsg=MEETS_KEEP)


MEETS = dict(
    kind="challenge",
    id="meets",
    title="Can They Cast It?",
    level="advanced",
    variant_of="affinity-of",
    optional=True,
    minutes=10,
    support="light",
    summary="The advanced twin of Read the Affinity: hand back True when a hero has the affinity and the mana a spell "
            "needs. Exactly enough counts.",
    martu=(
        "The advanced sheet trial: two nested reads and two questions. Write `meets(hero, spell)`. It hands back "
        "`True` when both are true:\n"
        "1. the hero's affinity is at least the spell's `\"required_affinity\"`,\n"
        "2. the hero's `\"mana\"` is at least the spell's `\"mana_cost\"`.\n"
        "Otherwise it hands back `False`. [[at least|Exactly enough]] counts.\n"
        "```text\nmeets(lucky, glow)       → True\nmeets(lucky, ward)       → False\n"
        "meets(lucky, strengthen) → False\n```\n"
        "My hidden tests try exactly enough, and one short, yes?"
    ),
    names=["meets", "hero", "spell"],
    starter=MEETS_STARTER,
    checkpoints=[
        dict(
            id="skill",
            text="Write `meets(hero, spell)`. Make rows 1 and 2 pass: check the hero's affinity first.",
            dictated=False,
            hints=[
                "Row 2's ward needs affinity 14, and Lucky has 13. Read the affinity from `hero`'s inner card and the "
                "need from `spell`, then compare them.",
                "A turn-away test hands back an answer early: `if strength < weight:` then `return False`. Nothing below it runs.",
                "Write `card = hero[\"abilities\"]`, `skill = card[\"magical_affinity\"]` and `req = "
                "spell[\"required_affinity\"]`. Then `if skill < req:` or `if skill <= req:`, with `return False` "
                "under it, and `return True` last. Both pass rows 1 and 2; the hidden test *exactly enough "
                "affinity* decides.",
            ],
            checks=[
                _meets_row(MEETS_LUCKY, MEETS_GLOW, True, ("v", 1, "meets(lucky, glow)", "return True"), ["has"]),
                _meets_row(MEETS_LUCKY, MEETS_WARD, False, ("v", 2, "meets(lucky, ward)", "return False"),
                           ["and", "mana"]),
            ],
            pass_line="Oogrish: Skill first. Good.",
        ),
        dict(
            id="mana",
            text="Make row 3 pass: the hero's `\"mana\"` must also be at least the spell's `\"mana_cost\"`.",
            dictated=False,
            hints=[
                "Lucky is skilled enough for Strengthen Magic, but has 8 mana and it costs 10. The function must ask "
                "about the mana too.",
                "`return coins >= price` hands back `True` or `False` straight from the comparison.",
                "Write `cost = spell[\"mana_cost\"]`, then `return hero[\"mana\"] > cost` or `return "
                "hero[\"mana\"] >= cost` as the last line, in place of `return True`. Both pass row 3; the hidden "
                "test *exactly enough mana* decides.",
            ],
            checks=[_meets_row(MEETS_LUCKY, MEETS_STRENGTHEN, False, ("v", 3, "meets(lucky, strengthen)",
                                                                       "return False"), ["and", "aff", "pair"])],
            pass_line="Lucky: Eight mana. Ten to cast. Fine. I'll sit this one out.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try exactly enough, and one short.",
            dictated=False,
            hints=[
                "The hidden tests try exactly enough of each, and one short of each. Read the rule again: exactly "
                "enough counts.",
                "`5 > 5` is `False`, and `5 >= 5` is `True`. *At least* is `>=`.",
                "Keep `if skill < req:` with `return False`, and `return hero[\"mana\"] >= cost` at the end.",
            ],
            checks=[
                _meets_row(hero("Pell", 20, 13), page(2, 13), True, ("h", "exactly enough affinity"), ["exact"]),
                _meets_row(hero("Moss", 8, 13), page(8, 3), True, ("h", "exactly enough mana"), ["exact"]),
                _meets_row(hero("Ivo", 6, 9), page(6, 9), True, ("h", "exactly enough of both"), ["exact"]),
                _meets_row(hero("Glug", 7, 13), page(8, 3), False, ("h", "one short of mana"), ["and", "aff"]),
                _meets_row(hero("Moth", 20, 12), page(2, 13), False, ("h", "one short of affinity"),
                           ["and", "mana"]),
                _meets_row(hero("Brakka", 9, 12), page(8, 11), True, ("h", "another hero and spell")),
            ],
            pass_line="Mar'tu: Exactly enough still casts. You knew that once, at the barrier. Now you know why.",
        ),
    ],
    solution=MEETS_SOLUTION,
    partials=[_meets(MEETS_READS + "    return True\n")],
    assemble=dict(
        lines=lines_of(MEETS_FN),
        distractors=["    if skill <= req:", '    return hero["mana"] > cost', '    return "True"'],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Read the hero's affinity (two keys) and the spell's need and cost.\n2. Affinity lower than the need? "
            "`return False`.\n3. Otherwise, hand back whether the mana is at least the cost: `>=`.")),
        dict(angle="picture", label="Two doors", text=(
            "```text\naffinity < need? → False\n        │ no\nmana >= cost?    → True\n"
            "                   or False\n```\nExactly enough walks through both doors.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`cast_spell` asked the same two questions with `<`, to turn a caster away: not skilled enough, then not "
            "enough mana. `meets` asks them as one yes/no answer. The barrier told you why: a caster with exactly "
            "enough can still cast.")),
    ],
    predict=dict(
        q="Before you write it: what do these print?",
        code="print(8 > 8)\nprint(8 >= 8)\n",
        choices=["True\nTrue", "False\nFalse", "False\nTrue"],
        answer=2,
        explain="8 is not more than 8, so `>` says `False`. 8 is *at least* 8, so `>=` says `True`. Exactly enough "
                "needs `>=`.",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        why=(
            "Holding the barrier, `cast_spell` turned a caster away when the affinity or the mana was lower, with "
            "`<`. Here you answer the same two questions yourself, with exactly enough counting."
        ),
    ),
    takeaway="*At least* is `>=`: exactly enough passes. Turn away early when the first must-have fails, then hand "
             "back the second as a comparison.",
    wrong_answers=[
        dict(why="the starter (pass)", code=MEETS_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="affinity only (the partial: no mana question)", code=_meets(MEETS_READS + "    return True\n"),
             fails_at=2, message_contains="Check the mana too"),
        dict(why="> for >= in both questions (exactly enough turned away)",
             code=_meets(MEETS_READS.replace("skill < req", "skill <= req") + '    return hero["mana"] > cost\n'),
             fails_at=3, message_contains="Exactly enough counts"),
        dict(why="or for and", code=_meets('    card = hero["abilities"]\n    skill = card["magical_affinity"]\n'
                                           '    req = spell["required_affinity"]\n'
                                           '    return skill >= req or hero["mana"] >= spell["mana_cost"]\n'),
             fails_at=1, message_contains="`and`, not `or`"),
        dict(why="mana only", code=_meets('    return hero["mana"] >= spell["mana_cost"]\n'), fails_at=1,
             message_contains="Check the affinity too"),
        dict(why="the keys swapped (affinity with mana_cost)",
             code=_meets('    card = hero["abilities"]\n    skill = card["magical_affinity"]\n'
                         '    return skill >= spell["mana_cost"] and hero["mana"] >= spell["required_affinity"]\n'),
             fails_at=2, message_contains="Compare each value with its partner"),
        dict(why='"True" / "False" in quotes (text, not a yes/no answer)',
             code=_meets(MEETS_READS.replace("return False", 'return "False"')
                         + '    if hero["mana"] >= cost:\n        return "True"\n    return "False"\n'),
             fails_at=1, message_contains="with no quotes"),
        dict(why="print instead of return",
             code=_meets(MEETS_READS.replace("return False", "print(False)") + '    print(hero["mana"] >= cost)\n'),
             fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="the mana spent inside the check (the barrier's habit)",
             code=_meets(MEETS_READS + '    hero["mana"] = hero["mana"] - cost\n    return hero["mana"] >= 0\n'),
             fails_at=1, message_contains="Only ask, don't spend"),
        dict(why="the turn-away question returned (True when the hero can't cast)",
             code=_meets('    card = hero["abilities"]\n    skill = card["magical_affinity"]\n'
                         '    return skill < spell["required_affinity"] or hero["mana"] < spell["mana_cost"]\n'),
             fails_at=1, message_contains="the hero's value on the left"),
        dict(why="the spell's value on the left (the comparison backwards)",
             code=_meets(MEETS_READS.replace("skill < req", "req < skill") + '    return cost >= hero["mana"]\n'),
             fails_at=1, message_contains="the hero's value on the left"),
        dict(why="an if with no else: None when the hero can't cast",
             code=_meets('    card = hero["abilities"]\n    skill = card["magical_affinity"]\n'
                         '    if skill >= spell["required_affinity"]:\n        if hero["mana"] >= spell["mana_cost"]:\n'
                         '            return True\n'), fails_at=1,
             message_contains="Give every path a `return`"),
        dict(why="a skipped level (the bottom prints: Python's KeyError)",
             code=_meets('    skill = hero["magical_affinity"]\n    return skill >= spell["required_affinity"]\n'),
             fails_at=0, message_contains="KeyError: 'magical_affinity'"),
        dict(why="Show me how for the affinity step, pasted word for word (with `<`): no crash; row 3 needs the mana",
             code=_meets(MEETS_RUNG1 + "    return True\n"), fails_at=2, message_contains="Check the mana too"),
        dict(why="Show me how for the affinity step, pasted word for word with its other sign, `<=`: no crash; "
                 "row 3 needs the mana",
             code=_meets(MEETS_RUNG1.replace("skill < req", "skill <= req") + "    return True\n"), fails_at=2,
             message_contains="Check the mana too"),
        dict(why="Show me how for the affinity step with its other sign, `<=`: rows 1-3 pass; the hidden test "
                 "exactly enough affinity decides",
             code=_meets(MEETS_RUNG1.replace("skill < req", "skill <= req") + MEETS_RUNG2 + '    return hero["mana"] >= cost\n'),
             fails_at=3, message_contains="Hidden test: exactly enough affinity"),
        dict(why="Show me how for the mana step with its other sign, `>`: rows 1-3 pass; the hidden test exactly "
                 "enough mana decides",
             code=_meets(MEETS_RUNG1 + MEETS_RUNG2 + '    return hero["mana"] > cost\n'), fails_at=3,
             message_contains="Hidden test: exactly enough mana"),
        dict(why="typed numbers (row 1's spell)",
             code=_meets('    card = hero["abilities"]\n    skill = card["magical_affinity"]\n'
                         '    return skill >= 3 and hero["mana"] >= 2\n'), fails_at=1,
             message_contains="`3` typed in it"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries (advanced)", opens="after Unit 5",
             ceiling="Units 1-5", skills="dict-read-nested,boundary,and,return-bool", solo="false", dictates="",
             foreign_names="strength,weight,coins,price",
             par="exactly enough affinity; exactly enough mana; exactly enough of both; one short of mana; one short "
                 "of affinity; another hero and spell") + "\n"
        "T-D-2a, variant_of affinity-of. Three checkpoints: the affinity (rows 1-2), the mana (row 3, Strengthen "
        "Magic at 10 mana and affinity 8, the campaign's own spell), then the hidden tests (exactly enough of each "
        "and both, one short of each, another hero). The partial is the affinity question alone. The solution turns "
        "away with `<` (the barrier's own form, 'you've seen this') and returns the mana comparison; `>=` both ways, "
        "the `and` form and an if/else all pass. Each row names only the slips it can tell apart (a yes/no answer "
        "leaves two slips looking the same); `_uses('op:Or')` and `_has('mana')` (the function's own code) settle "
        "the rest. Spending mana inside `meets` is caught on every row ('Only ask, don't spend'). Show-rung "
        "copy-test: CP skill's rung (it used to use `req` with no line making it) now makes `card`, `skill` and "
        "`req`, then the turn-away with `<` or `<=`, and `return True` last: no crash, rows 1-2 pass with either "
        "sign, row 3 fails 'Check the mana too' (the partial; `<=`: wrong_answers). The ruling's wording ends at "
        "`return False`; pasted as it stands, row 1 hands back None, so 'and `return True` last' was added to keep "
        "'Both pass rows 1 and 2' true (and CP mana's rung says 'in place of `return True`'). CP mana's rung (it "
        "used to use `cost` with no line making it) makes `cost`, then `>` or `>=`: no crash, rows 1-3 pass with "
        "either sign; `>` fails the hidden test exactly enough mana, and `<=` in the turn-away fails exactly "
        "enough affinity (wrong_answers). CP hidden-tests' rung keeps the right pair, `<` and `>=` (the solution)."
    ),
)


# =============================================================================================
# T-D-3 "Rename a Spell": rename_spell(book, old, new) changes the book it is handed (core)
# =============================================================================================

REN_BOOK = {"Glow": page(2, 3), "Warm Hands": page(5, 4)}
REN_OTHER = {"Moon Step": page(5, 7), "Ash Ward": page(8, 11), "Sun Ward": page(9, 12)}
REN_HEAD = "# Trial: rename a spell.\ndef rename_spell(book, old, new):\n"
REN_TAIL = (
    "\n\n" + book_code("book", REN_BOOK) + "\n"
    "# The visible test. The book should\n"
    '# have no "Glow" key, and "Halo"\n'
    "# should hold Glow's old page.\n"
    'rename_spell(book, "Glow", "Halo")\n'
    "print(book)\n"
)
REN_BODY = "    book[new] = book[old]\n    book.pop(old)\n"


def _ren(body="    pass\n", tail=REN_TAIL, head=REN_HEAD):
    return head + body + tail


REN_STARTER = _ren()
REN_SOLUTION = _ren(REN_BODY)
REN_FN = REN_HEAD.split("\n", 1)[1] + REN_BODY
REN_OK = ["Glow", "Halo", "Warm Hands"]
REN_TYPED = ["Glow", "Halo"]


def _pop_first(old):
    return (f"_karg(_e) == {old!r}",
            "Read the page before you take it out: `book[new] = book[old]` first, then `book.pop(old)`.")


def _ren_row(args, where, part, ret=None, errs=None):
    return rename_row(args, where, part, ret, ok=REN_OK, typed=REN_TYPED,
                      errs=[_pop_first(args[1])] if errs is None else errs)


_REN_CALL = 'rename_spell(book, "Glow", "Halo")'

RENAME_SPELL = dict(
    kind="challenge",
    id="rename-spell",
    title="Rename a Spell",
    level="core",
    optional=True,
    minutes=6,
    support="light",
    summary="Move a spell's page to a new name in the book you are handed, and take the old name out.",
    martu=(
        "Lucky wants Glow called Halo. \"Sounds better.\" Fine. A function (a recipe) that changes the book it is "
        "handed.\n"
        "Write `rename_spell(book, old, new)`. Afterwards the page that was under `old` is under `new`, and `old` "
        "is gone. It hands back nothing: the caller's book changes. Most trials hand back an answer. This one changes "
        "the book itself, so it needs no `return`.\n"
        "A list's `.pop()` takes an item out. A dictionary has one too: `.pop(key)` takes that key out, page and "
        "all.\n"
        "```text\nafter rename_spell(book,\n        \"Glow\", \"Halo\"):\nbook[\"Halo\"]       Glow's page\n"
        "\"Glow\" in book     False\nbook[\"Warm Hands\"] as it was\n```"
    ),
    example='shelf = {"jam": 2, "tea": 5}\nshelf.pop("jam")\nprint(shelf)\n',
    example_output="{'tea': 5}",
    names=["rename_spell", "book", "old", "new"],
    starter=REN_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `rename_spell(book, old, new)` so every row of the table holds.",
            dictated=False,
            hints=[
                "The book you are handed must change: the old page goes under the new name, and the old name goes "
                "away. Nothing needs to be handed back.",
                "With other names: `shelf[fresh] = shelf[stale]` puts the page under the new name too. Then "
                "`shelf.pop(stale)` takes the old name out. `fresh` and `stale` have no quotes: they hold the names.",
                "Write `book[new] = book[old]`, then `book.pop(old)` on the next line.",
            ],
            checks=[
                _ren_row((REN_BOOK, "Glow", "Halo"), ("v", 1, _REN_CALL, 'after `' + _REN_CALL + '`, `book["Halo"]` should be Glow\'s old page'),
                         "page"),
                _ren_row((REN_BOOK, "Glow", "Halo"), ("v", 2, _REN_CALL, 'after `' + _REN_CALL + '`, `"Glow" in book` should be `False`'),
                         "old"),
                _ren_row((REN_BOOK, "Glow", "Halo"), ("v", 3, _REN_CALL, 'after `' + _REN_CALL + '`, `book["Warm Hands"]` should be as it was'),
                         "others"),
            ],
            pass_line="Lucky: Halo. Much better. I'm keeping track of who named it.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They use new books and names.",
            dictated=False,
            hints=[
                "The hidden tests rename other spells in other books. Use `old` and `new` with no quotes, so any "
                "names work.",
                "Move the page itself, `shelf[stale]`. Values typed into a new page only match one spell.",
                "Keep `book[new] = book[old]` and `book.pop(old)`, with no spell names typed in.",
            ],
            checks=[
                _ren_row((REN_OTHER, "Ash Ward", "Ember Ward"), ("h", "another book and other names"), "others"),
                _ren_row(({"Glow": page(1, 1)}, "Glow", "Sun Glow"), ("h", "a book with one spell"), "others"),
            ],
            pass_line="Mar'tu: No `return`, and still the caller sees it. The book is the same book, yes?",
        ),
    ],
    solution=REN_SOLUTION,
    assemble=dict(
        lines=lines_of(REN_FN),
        distractors=["    book[old] = book[new]", '    book["new"] = book["old"]', "    book.remove(old)"],
    ),
    another_way=[
        dict(angle="picture", label="Before and after", text=(
            "```text\nbook[new] = book[old]\n  \"Glow\" → page\n  \"Halo\" → page\nbook.pop(old)\n"
            "  \"Halo\" → page\n```\nOne page, two names for a moment, then one name.")),
        dict(angle="step-by-step", text=(
            "1. Store the old page under the new name: the new name on the left.\n2. Take the old name out with "
            "`.pop(old)`.\n3. Hand back nothing: the caller's book is the same dictionary, so it sees the change.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`add_spell` stored a page with `spell_book[spell_name] = spell`, and every hero's book changed without "
            "a `return`. A rename is the same store, plus one `.pop()`.")),
    ],
    pair_talk="Tell your partner why the caller's `book` changes, even though `rename_spell` hands back nothing.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="spell_book[spell_name] = spell",
        why=(
            "You stored pages by name in the spell book, and each member's book changed in place. Renaming stores "
            "the same page under a new name, then takes the old name out."
        ),
    ),
    takeaway="A function can change the dictionary it is handed: store under the new key, then `.pop()` the old one.",
    wrong_answers=[
        dict(why="the starter (pass)", code=REN_STARTER, fails_at=1, message_contains="the book did not change"),
        dict(why="the page copied, the old name kept", code=_ren("    book[new] = book[old]\n"), fails_at=1,
             message_contains="Take the old name out"),
        dict(why="pop first, then read (the bottom call: Python's KeyError)",
             code=_ren("    book.pop(old)\n    book[new] = book[old]\n"), fails_at=0,
             message_contains="KeyError: 'Glow'"),
        dict(why="pop first, then read, the call gone",
             code=_ren("    book.pop(old)\n    book[new] = book[old]\n", tail=""), fails_at=1,
             message_contains="Read the page before you take it out"),
        dict(why="the rename backwards, book[old] = book[new] (the bottom call: Python's KeyError)",
             code=_ren("    book[old] = book[new]\n    book.pop(new)\n"), fails_at=0,
             message_contains="KeyError: 'Halo'"),
        dict(why="the rename backwards, the call gone", code=_ren("    book[old] = book[new]\n    book.pop(new)\n",
                                                                  tail=""), fails_at=1,
             message_contains="Put the new name on the left"),
        dict(why="quoted parameters (the bottom call: Python's KeyError)",
             code=_ren('    book["new"] = book["old"]\n    book.pop("old")\n'), fails_at=0,
             message_contains="KeyError: 'old'"),
        dict(why="quoted parameters, the call gone",
             code=_ren('    book["new"] = book["old"]\n    book.pop("old")\n', tail=""), fails_at=1,
             message_contains='Take the quotes off `"old"`'),
        dict(why="a page typed in (passes the table; the other book catches it)",
             code=_ren('    book[new] = {"mana_cost": 2, "required_affinity": 3}\n    book.pop(old)\n'), fails_at=2,
             message_contains="Move the old page itself"),
        dict(why="the names from the table typed in (passes the table; the other book catches it)",
             code=_ren('    book["Halo"] = book["Glow"]\n    book.pop("Glow")\n'), fails_at=2,
             message_contains="not a name from the table"),
        dict(why="a new book built and returned (the caller's book never changes)",
             code=_ren("    new_book = {new: book[old]}\n    return new_book\n"), fails_at=1,
             message_contains="Change the book you were handed"),
        dict(why="the name stored, not the page", code=_ren("    book[new] = old\n    book.pop(old)\n"), fails_at=1,
             message_contains="Store the page, not the name"),
        dict(why="a list's .remove() on a dictionary (the bottom call: Python's AttributeError)",
             code=_ren("    book[new] = book[old]\n    book.remove(old)\n"), fails_at=0,
             message_contains="'dict' object has no attribute 'remove'"),
        dict(why="a list's .remove(), the call gone",
             code=_ren("    book[new] = book[old]\n    book.remove(old)\n", tail=""), fails_at=1,
             message_contains="with `.pop(key)`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries", opens="after Unit 5", ceiling="Units 1-5",
             skills="dict-write,dict-pop,change-in-place", solo="false", dictates="",
             foreign_names="shelf,jam,tea,fresh,stale",
             par="another book and other names (Ash Ward to Ember Ward); a book with one spell (Glow to Sun Glow)")
        + "\n"
        "T-D-3. The spec names only the signature; Mar'tu's version changes the book it is handed and returns "
        "nothing, the campaign's own habit (`add_spell` changed each member's book in place), so the reverse slip "
        "of the unit's list (a new book built and returned, the caller's book unchanged) has a home here. The rows "
        "are states, not returned values: the page under the new name, the old name gone, the other pages kept. "
        "`.pop(key)` on a dictionary is new use of a taught token (attr:pop, u04b); the Learn pane says so and the "
        "Example shows it (`del` is never taught, but passes). `book[new] = book.pop(old)` passes too. The Teach "
        "rungs use `shelf[fresh] = shelf[stale]` and `shelf.pop(stale)`, with no quotes and the names held in "
        "boxes (they used to model `shelf[\"jam\"]`, the class's quoted-key slip). Show-rung copy-test: CP1's "
        "rung is the solution (no crash; the starter's print shows the renamed book); CP2's rung keeps it."
    ),
)


# =============================================================================================
# T-D-3a "Rename, Safely": the same function refuses (returns False) when `new` already exists or `old` is
# missing, and returns True after a rename (advanced)
# =============================================================================================

SAFE_HEAD = "# Trial: rename, but only safely.\ndef rename_spell(book, old, new):\n"
# Row 3's call (Glow is gone after row 1), commented out in the starter: the partial (no guards) would stop there
# with a KeyError and fail every checkpoint.
SAFE_ROW3 = '# print(rename_spell(book, "Glow", "Ember"))\n'
SAFE_AFTER = {"Warm Hands": page(5, 4), "Halo": page(2, 3)}
SAFE_TAIL = (
    "\n\n" + book_code("book", REN_BOOK) + "\n"
    "# Visible tests 1 and 2. They should\n"
    "# show True, then False, and a book\n"
    "# that still has Warm Hands.\n"
    "# (With only pass, both show None.)\n"
    'print(rename_spell(book, "Glow", "Halo"))\n'
    'print(rename_spell(book, "Warm Hands", "Halo"))\n'
    "print(book)\n"
    "# Once rows 1 and 2 pass, add\n"
    + SAFE_ROW3
    + "# It should show False.\n"
)
SAFE_GUARDS = (
    "    if old not in book:\n"
    "        return False\n"
    "    if new in book:\n"
    "        return False\n"
)
SAFE_BODY = SAFE_GUARDS + REN_BODY + "    return True\n"


def _safe(body="    pass\n", tail=SAFE_TAIL):
    return SAFE_HEAD + body + tail


SAFE_STARTER = _safe()
SAFE_SOLUTION = _safe(SAFE_BODY)
SAFE_FN = SAFE_HEAD.split("\n", 1)[1] + SAFE_BODY
SAFE_OK = ["Glow", "Halo", "Warm Hands", "Ember"]
SAFE_TYPED = ["Glow", "Halo", "Warm Hands", "Ember"]
SAFE_MISSING = ("Ask `if old not in book:` first, and hand back `False`: the book has no page to move, so Python "
                "stopped with a KeyError.")


def _safe_row(args, where, part, ret, missing=False):
    errs = [(f"_karg(_e) == {args[1]!r}", SAFE_MISSING if missing else
             "Read the page before you take it out: `book[new] = book[old]` first, then `book.pop(old)`.")]
    return rename_row(args, where, part, ret, ok=SAFE_OK, typed=SAFE_TYPED, errs=errs)


RENAME_SAFELY = dict(
    kind="challenge",
    id="rename-safely",
    title="Rename, Safely",
    level="advanced",
    variant_of="rename-spell",
    optional=True,
    minutes=10,
    support="light",
    summary="The advanced twin of Rename a Spell: refuse, and hand back False, when the new name is taken or the old "
            "one is missing.",
    martu=(
        "The advanced rename. Same function, `rename_spell(book, old, new)`, with a stricter rule. It refuses, and "
        "hands back `False`, when `new` is already a spell, or when `old` is not in the book. A refusal changes "
        "nothing. After a real rename it hands back `True`.\n"
        "```text\nthe calls, in order:\n\"Glow\" → \"Halo\"        True\n\"Warm Hands\" → \"Halo\"  False\n"
        "\"Glow\" → \"Ember\"       False\n```\n"
        "Row 2: Halo is taken now. Row 3: Glow is gone. My hidden tests try other books, yes?"
    ),
    names=["rename_spell", "book", "old", "new"],
    starter=SAFE_STARTER,
    checkpoints=[
        dict(
            id="rename",
            text="Write `rename_spell(book, old, new)` so row 1 passes: rename, then hand back `True`.",
            dictated=False,
            hints=[
                "Row 1 is the rename from the core trial, plus one more line: after the rename, the function "
                "hands back `True`.",
                "`shelf[fresh] = shelf[stale]` and `shelf.pop(stale)` move a page. A last line, `return True`, "
                "reports that it worked.",
                "Write `book[new] = book[old]`, then `book.pop(old)`, then `return True`.",
            ],
            checks=[_safe_row((REN_BOOK, "Glow", "Halo"), ("v", 1, _REN_CALL, "`" + _REN_CALL + "` should return `True` "
                                                                              "and move the page"), "others", True)],
            pass_line="Oogrish: The rename works. Now teach it to say no.",
        ),
        dict(
            id="refusals",
            text="Make rows 2 and 3 pass: hand back `False`, and change nothing, when `new` is taken or `old` is "
                 "missing.",
            dictated=False,
            hints=[
                "Ask before you change anything. Row 2's new name is already a spell, and row 3's old name has no "
                "page. Both get `False`, and the book stays as it was.",
                "A guard hands back an answer early: `if item not in shelf:` then `return False`. Nothing below it runs.",
                "Write `if old not in book:` with `return False` under it, and `if new in book:` with `return "
                "False`, above the rename.",
            ],
            checks=[
                _safe_row((SAFE_AFTER, "Warm Hands", "Halo"),
                          ("v", 2, 'rename_spell(book, "Warm Hands", "Halo")', "`rename_spell(book, \"Warm Hands\", "
                                                                              "\"Halo\")` should return `False` and "
                                                                              "change nothing"), "refuse", False),
                _safe_row((SAFE_AFTER, "Glow", "Ember"),
                          ("v", 3, 'rename_spell(book, "Glow", "Ember")', "`rename_spell(book, \"Glow\", \"Ember\")` "
                                                                         "should return `False` and change nothing"), "refuse", False, missing=True),
            ],
            pass_line="Lucky: It said no to me. Twice. I respect that.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try new books and names.",
            dictated=False,
            hints=[
                "The hidden tests try other books. Every refusal must leave the book exactly as it was, and every "
                "rename must hand back `True`.",
                "Python reads a function from the top: put both questions first, then the change, then `return "
                "True`.",
                "Keep `if old not in book:` and `if new in book:` at the top, each with `return False` under it.",
            ],
            checks=[
                _safe_row((REN_OTHER, "Ash Ward", "Ember Ward"), ("h", "another book"), "others", True),
                _safe_row((REN_OTHER, "Moon Step", "Sun Ward"), ("h", "a new name another book already has"),
                          "refuse", False),
                _safe_row((REN_OTHER, "Star Fall", "Comet"), ("h", "an old name another book does not have"),
                          "refuse", False, missing=True),
                _safe_row((REN_OTHER, "Star Fall", "Ash Ward"), ("h", "an old name that is missing and a new name "
                                                                      "that is taken"), "refuse", False,
                          missing=True),
                _safe_row(({"Glow": page(1, 1)}, "Glow", "Sun Glow"), ("h", "a book with one spell"), "others", True),
            ],
            pass_line="Mar'tu: Ask first, then change. The barrier's guard, in your own words.",
        ),
    ],
    solution=SAFE_SOLUTION,
    partials=[_safe(REN_BODY + "    return True\n")],
    assemble=dict(
        lines=lines_of(SAFE_FN),
        distractors=["    if old in book:", '        return "False"', "    if new not in book:"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. `old` missing? Hand back `False`.\n2. `new` taken? Hand back `False`.\n3. Move the page and pop the old "
            "name.\n4. Hand back `True`.")),
        dict(angle="everyday", label="The clerk says no", text=(
            "A clerk renaming a file checks two things first: is the old file there, and is the new name free? If "
            "either answer is wrong, the clerk says no and touches nothing.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "`cast_spell` began with a guard: `if spell_name not in caster[\"spell_book\"]:`, then `return`. Ask "
            "first, change later. Here each guard hands back `False`.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        why=(
            "The guard at the top of `cast_spell` stopped before anything changed. These two guards do the same "
            "for a rename, and report the answer with `True` or `False`."
        ),
    ),
    takeaway="Guards go first: hand back `False` before you change anything, and `True` once the change is done.",
    wrong_answers=[
        dict(why="the starter (pass)", code=SAFE_STARTER, fails_at=1, message_contains="the book did not change"),
        dict(why="no guards (the partial: the taken name is written over)", code=_safe(REN_BODY + "    return True\n"),
             fails_at=2, message_contains="Ask first, then change"),
        dict(why="the partial with row 3's call added back too early: Python's own KeyError at the bottom print",
             code=_safe(REN_BODY + "    return True\n", tail=SAFE_TAIL.replace(SAFE_ROW3, SAFE_ROW3[2:])), fails_at=0,
             message_contains="KeyError: 'Glow'"),
        dict(why="only the missing-name guard", code=_safe("    if old not in book:\n        return False\n"
                                                           + REN_BODY + "    return True\n"), fails_at=2,
             message_contains="Ask first, then change"),
        dict(why="only the taken-name guard (a missing name stops with a KeyError)",
             code=_safe("    if new in book:\n        return False\n" + REN_BODY + "    return True\n"), fails_at=2,
             message_contains="Ask `if old not in book:` first"),
        dict(why="the two questions joined with and (a taken name still written over)",
             code=_safe("    if old not in book and new in book:\n        return False\n" + REN_BODY
                        + "    return True\n"), fails_at=2, message_contains="Ask first, then change"),
        dict(why='"True" in quotes', code=_safe(SAFE_GUARDS + REN_BODY + '    return "True"\n'), fails_at=1,
             message_contains="with no quotes"),
        dict(why="no return True after the rename (None)", code=_safe(SAFE_GUARDS + REN_BODY), fails_at=1,
             message_contains="End with `return True`"),
        dict(why="a bare return for a refusal (None)",
             code=_safe(SAFE_GUARDS.replace("return False", "return") + REN_BODY + "    return True\n"), fails_at=2,
             message_contains="Refuse with `return False`"),
        dict(why="print instead of return for a refusal",
             code=_safe("    if old not in book:\n        print(False)\n    elif new in book:\n        print(False)\n"
                        "    else:\n        book[new] = book[old]\n        book.pop(old)\n        return True\n"),
             fails_at=2, message_contains="Use `return`, not `print`"),
        dict(why="a new book built and returned (the caller's book never changes)",
             code=_safe(SAFE_GUARDS + "    new_book = {new: book[old]}\n    return new_book\n"), fails_at=1,
             message_contains="Change the book you were handed"),
        dict(why="the names from the table typed in (the other books catch it)",
             code=_safe('    if "Glow" not in book:\n        return False\n    if "Halo" in book:\n'
                        '        return False\n    book["Halo"] = book["Glow"]\n    book.pop("Glow")\n'
                        "    return True\n"), fails_at=3, message_contains="typed in it"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Dictionaries (advanced)", opens="after Unit 5",
             ceiling="Units 1-5", skills="guard,not-in,dict-pop,return-bool", solo="false", dictates="",
             foreign_names="shelf,fresh,stale,item",
             par="another book; a new name another book already has; an old name another book does not have; both; "
                 "a book with one spell") + "\n"
        "T-D-3a, variant_of rename-spell (same function name, a stricter spec, as the spec's table gives it). Rows "
        "are the starter's calls in order (Halo is taken after row 1; Glow is gone), each checked on a fresh copy "
        "of that state. Row 3's call is a comment in the starter (\"Once rows 1 and 2 pass, add ...\", with row 3's "
        "own names): the partial (no guards) would stop there with a KeyError and fail every checkpoint (a "
        "wrong_answers entry adds it back and proves it). The visible calls stay whole on one line (41, 47 and 44 "
        "characters: a wrapped call reads as broken code, u08a's ruling). A refusal must leave the book exactly as it was (a written-over page is named). The combined "
        "guard `if old not in book or new in book:` passes (it is 39 characters, so Mar'tu's version uses two). "
        "Show-rung copy-test: CP rename's rung (the move, then `return True`) is the partial: no crash (row 3's "
        "call is a comment), row 1 passes, row 2 fails 'Ask first, then change'. CP refusals' rung (both guards "
        "above the rename) is the solution; CP hidden-tests' rung keeps it."
    ),
)


# =============================================================================================
# T-Lo-1 "The Party's Mana": total_mana(heroes) (core)
# =============================================================================================

PARTY = [sheet("Oogrish", 8), sheet("Gearshift", 15), sheet("Bomb Shell", 4), sheet("Lucky", 22)]
FIVE = [sheet("Pell", 7), sheet("Brakka", 12), sheet("Moss", 5), sheet("Glug", 9), sheet("Ivo", 30)]
LOOP_OK = ["Oogrish", "Gearshift", "Bomb Shell", "Lucky", "Pell", "Brakka", "Moss", "Glug", "Ivo", "Moth",
           "Tinplate", "Ash", "Bree"]
TOTAL_HEAD = "# Trial: the party's mana.\ndef total_mana(heroes):\n"
# Row 3's call, commented out in the starter: two of the class's slips (a start at `heroes[0]`, the total made
# inside the loop) would stop Python on it before Mar'tu's checks run.
TOTAL_ROW3 = "# print(total_mana([]))\n"
TOTAL_TAIL = (
    "\n\n" + roster_code("roster", PARTY) + "\n"
    "# Visible tests. They should show\n"
    "# 49, then 23.\n"
    "# (With only pass, each shows None.)\n"
    "print(total_mana(roster))\n"
    "print(total_mana(roster[:2]))\n"
    "# Visible test 3, an empty roster,\n"
    "# is in Mar'tu's table. Once rows\n"
    "# 1 and 2 pass, add this line:\n"
    + TOTAL_ROW3
    + "# It should show 0.\n"
)
TOTAL_BODY = '    total = 0\n    for hero in heroes:\n        total = total + hero["mana"]\n    return total\n'


def _total(body="    pass\n", tail=TOTAL_TAIL):
    return TOTAL_HEAD + body + tail


TOTAL_STARTER = _total()
TOTAL_SOLUTION = _total(TOTAL_BODY)
TOTAL_FN = TOTAL_HEAD.split("\n", 1)[1] + TOTAL_BODY
TOTAL_TYPED = [49, 23, 22, 8, 15, 4, 2]
_RESET = ("Make `total = 0` once, before the loop, and add to it inside: `total = total + hero[\"mana\"]`. Yours kept "
          "only the last hero's mana.")
_FIRST_ONLY = "Put `return` after the loop, not inside it: your function stopped after the first hero."
TOTAL_SLIPS = [
    (lambda h: h[-1]["mana"], _RESET),
    (lambda h: h[0]["mana"], _FIRST_ONLY, "_ret_in_loop()"),
    (lambda h: len(h), "Add each hero's `\"mana\"`, not 1: your function counted the heroes."),
    (lambda h: sum(x["mana"] for x in h[:4]),
     "Walk every hero with `for hero in heroes:`, not a typed `range(4)`: this roster has more heroes."),
]
TOTAL_ERRS = [
    ("_tn(_e) == 'IndexError' and _uses('call:range')",
     "Walk the list itself, `for hero in heroes:`: a typed `range(4)` runs past the end of a shorter roster."),
    ("_tn(_e) == 'IndexError'",
     "An empty roster has no first hero: start `total` at 0, not at a hero's mana, and add every hero inside the "
     "loop. Then `[]` hands back 0."),
]


def _total_row(h, want, where):
    return row("total_mana", ["heroes"], (h,), want, where, ok=LOOP_OK, typed=TOTAL_TYPED, errs=TOTAL_ERRS,
               slips=TOTAL_SLIPS)


TOTAL_MANA = dict(
    kind="challenge",
    id="total-mana",
    title="The Party's Mana",
    level="core",
    optional=True,
    minutes=6,
    support="light",
    tracer=True,
    summary="Add up the mana of every hero on a roster, whatever its length.",
    martu=(
        "The first loop trial. After a night holding the barrier, Gearshift wants one number: how much mana is "
        "left in the whole party. A function (a recipe) with a loop inside.\n"
        "Write `total_mana(heroes)`. `heroes` is a list of sheets. It hands back all their `\"mana\"`, added up. An "
        "empty roster has 0.\n"
        "```text\ntotal_mana(roster)     → 49\ntotal_mana(roster[:2]) → 23\ntotal_mana([])         → 0\n```\n"
        "Run it and compare with the [[test table]]. My [[hidden test|hidden tests]] use longer and shorter rosters, yes?"
    ),
    names=["total_mana", "heroes"],
    starter=TOTAL_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `total_mana(heroes)` so every row of the table passes.",
            dictated=False,
            hints=[
                "Start a [[running total]] at 0, before the loop. Add each hero's `\"mana\"` inside the loop. Hand back "
                "the total after the loop.",
                "With other names: `coins = 0`, then `for bag in bags:` with `coins = coins + bag[\"gold\"]` inside, "
                "then `return coins` below the loop.",
                "Write `total = 0`, then `for hero in heroes:` with `total = total + hero[\"mana\"]` inside it, then "
                "`return total`.",
            ],
            checks=[
                _total_row(PARTY, 49, ("v", 1, "total_mana(roster)", "return 49")),
                _total_row(PARTY[:2], 23, ("v", 2, "total_mana(roster[:2])", "return 23")),
                _total_row([], 0, ("v", 3, "total_mana([])", "return 0")),
            ],
            pass_line="Gearshift: Forty-nine. Visor dims. Barrier's holding.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They use rosters of other lengths.",
            dictated=False,
            hints=[
                "The hidden rosters have 1, 2 and 5 heroes. A loop over `heroes` itself fits any length.",
                "`for bag in bags:` runs once for each bag, however many there are. A typed `range(4)` always runs "
                "4 times.",
                "Keep `total = 0` before the loop and `return total` after it, with `for hero in heroes:` between.",
            ],
            checks=[
                _total_row(FIVE, 63, ("h", "a roster of five")),
                _total_row([sheet("Moth", 11)], 11, ("h", "one hero")),
                _total_row([sheet("Pell", 0), sheet("Ivo", 8)], 8, ("h", "a hero with 0 mana")),
            ],
            pass_line="Mar'tu: One loop, any party. Somebody else wrote that loop for you once. Not now.",
        ),
    ],
    solution=TOTAL_SOLUTION,
    assemble=dict(
        lines=lines_of(TOTAL_FN),
        distractors=["        total = 0", "        return total", "    total = total + heroes"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. `total = 0`, before the loop.\n2. `for hero in heroes:`, and inside it add `hero[\"mana\"]` to "
            "`total`.\n3. After the loop, not indented under it: `return total`.")),
        dict(angle="everyday", label="A jar of coins", text=(
            "Start with an empty jar. Each friend drops in their coins, one friend at a time. When the last friend "
            "is done, count the jar. Empty the jar between friends, and you only count the last one.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The mana bars ended with `for member in party.members:`, a loop somebody wrote for you. This one is "
            "yours, and it keeps a running total as it goes.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="for member in party.members:",
        why="The loop at the bottom of the mana bars visited every member once. Yours visits every hero, and adds.",
    ),
    takeaway="A running total starts at 0 before the loop, grows inside it, and is handed back after it.",
    wrong_answers=[
        dict(why="the starter (pass)", code=TOTAL_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the total reset inside the loop, in the starter as given (row 3's call is a comment)",
             code=_total('    for hero in heroes:\n        total = 0\n        total = total + hero["mana"]\n'
                         "    return total\n"), fails_at=1, message_contains="Make `total = 0` once, before the loop"),
        dict(why="the total reset inside the loop, row 3's call added back: Python stops on the empty roster first",
             code=_total('    for hero in heroes:\n        total = 0\n        total = total + hero["mana"]\n'
                         "    return total\n", tail=TOTAL_TAIL.replace(TOTAL_ROW3, TOTAL_ROW3[2:])), fails_at=0,
             message_contains="UnboundLocalError"),
        dict(why="= for + (the total replaced, not added to)",
             code=_total('    total = 0\n    for hero in heroes:\n        total = hero["mana"]\n    return total\n'),
             fails_at=1, message_contains="only the last hero"),
        dict(why="return inside the loop (the first hero only)",
             code=_total('    total = 0\n    for hero in heroes:\n        total = total + hero["mana"]\n'
                         "        return total\n"), fails_at=1, message_contains="after the loop, not inside it"),
        dict(why="row 1's answer typed (return 49)", code=_total("    return 49\n"), fails_at=1,
             message_contains="`49` typed in it"),
        dict(why="the table typed as an if-chain on the length (the hidden rosters catch it)",
             code=_total("    if len(heroes) == 4:\n        return 49\n    if len(heroes) == 2:\n        return 23\n"
                         "    return 0\n"), fails_at=2, message_contains="typed in it"),
        dict(why="print instead of return",
             code=_total('    total = 0\n    for hero in heroes:\n        total = total + hero["mana"]\n'
                         "    print(total)\n"), fails_at=1, message_contains="Use `return`, not `print`"),
        dict(why="sum() of the sheets (the bottom prints: Python's TypeError)", code=_total("    return sum(heroes)\n"),
             fails_at=0, message_contains="unsupported operand type(s) for +: 'int' and 'dict'"),
        dict(why="sum() of the sheets, the prints gone", code=_total("    return sum(heroes)\n", tail=""), fails_at=1,
             message_contains="Add a number from each sheet"),
        dict(why='heroes["mana"]: the list read like a sheet, the prints gone',
             code=_total('    return heroes["mana"]\n', tail=""), fails_at=1, message_contains="Read one item at a time"),
        dict(why="a typed range(4) (the bottom prints: Python's IndexError)",
             code=_total('    total = 0\n    for i in range(4):\n        total = total + heroes[i]["mana"]\n'
                         "    return total\n"), fails_at=0, message_contains="IndexError: list index out of range"),
        dict(why="a typed range(4), the prints gone",
             code=_total('    total = 0\n    for i in range(4):\n        total = total + heroes[i]["mana"]\n'
                         "    return total\n", tail=""), fails_at=1, message_contains="a typed `range(4)`"),
        dict(why="the total started from heroes[0], in the starter as given (row 3's call is a comment)",
             code=_total('    total = heroes[0]["mana"]\n    for hero in heroes[1:]:\n'
                         '        total = total + hero["mana"]\n    return total\n'), fails_at=1,
             message_contains="start `total` at 0"),
        dict(why="the total started from heroes[0], row 3's call added back: Python's IndexError on the empty roster",
             code=_total('    total = heroes[0]["mana"]\n    for hero in heroes[1:]:\n'
                         '        total = total + hero["mana"]\n    return total\n',
                         tail=TOTAL_TAIL.replace(TOTAL_ROW3, TOTAL_ROW3[2:])), fails_at=0,
             message_contains="IndexError: list index out of range"),
        dict(why="the roster popped empty while adding (the list handed in is changed)",
             code=_total('    total = 0\n    while len(heroes) > 0:\n        hero = heroes.pop()\n'
                         '        total = total + hero["mana"]\n    return total\n'), fails_at=1,
             message_contains="Leave `heroes` as it was"),
        dict(why="str(total): text, not a number",
             code=_total('    total = 0\n    for hero in heroes:\n        total = total + hero["mana"]\n'
                         "    return str(total)\n"), fails_at=1, message_contains="Hand back a number, not text"),
        dict(why="the heroes counted, not their mana",
             code=_total("    total = 0\n    for hero in heroes:\n        total = total + 1\n    return total\n"),
             fails_at=1, message_contains="counted the heroes"),
        dict(why="the top-level roster read inside the function (roster for heroes)",
             code=_total('    total = 0\n    for hero in roster:\n        total = total + hero["mana"]\n'
                         "    return total\n"), fails_at=1, message_contains="Use the parameter `heroes`, not `roster`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops", opens="after Unit 6", ceiling="Units 1-6",
             skills="loop-list-of-dicts,accumulate,return-value", solo="false", dictates="",
             foreign_names="coins,bags,bag,gold",
             par="a roster of five (63); one hero (11); a hero with 0 mana (8)") + "\n"
        "T-Lo-1. The party after a night holding the barrier: Oogrish 8, Gearshift 15, Bomb Shell 4, Lucky 22 (49). "
        "The table's second and third rows reuse the roster with a slice (Unit 4) and the empty list, so the roster "
        "is written once, one key a line (phone width). The empty roster is visible (row 3): a running total that "
        "starts at 0 handles it for free, which is the point Mar'tu makes. Its call is a comment in the starter "
        "(\"Once rows 1 and 2 pass, add this line\"): a start at `heroes[0]` and the total made inside the loop "
        "would stop Python on it before Mar'tu's checks run, so each now gets Mar'tu's message (a fails_at 0 twin "
        "adds the call back). `sum([h[\"mana\"] for h in heroes])` and "
        "`range(len(heroes))` pass. Every row also checks the roster is left as it was (popping it empty while "
        "adding is caught). Show-rung copy-test: CP1's rung is the solution (no crash, every checkpoint passes); "
        "CP2's rung keeps it."
    ),
)


# =============================================================================================
# T-Lo-1a "Average Mana": average_mana(heroes), with an empty roster -> 0 (advanced)
# =============================================================================================

AVG_HEAD = "# Trial: the party's average.\ndef average_mana(heroes):\n"
# Row 4's call, commented out in the starter: the partial (no guard) would stop there with a ZeroDivisionError and
# fail every checkpoint.
AVG_ROW4 = "# print(average_mana([]))\n"
AVG_TAIL = (
    "\n\n" + roster_code("roster", PARTY) + "\n"
    "# Visible tests 1 to 3. They should\n"
    "# show 12.25, 11.5, then 22.0.\n"
    "# (With only pass, each shows None.)\n"
    "print(average_mana(roster))\n"
    "print(average_mana(roster[:2]))\n"
    "print(average_mana(roster[3:]))\n"
    "# Visible test 4, an empty roster,\n"
    "# is in Mar'tu's table. Once rows\n"
    "# 1 to 3 pass, add this line:\n"
    + AVG_ROW4
    + "# It should show 0.\n"
)
AVG_GUARD = "    if len(heroes) == 0:\n        return 0\n"
AVG_SUM = '    total = 0\n    for hero in heroes:\n        total = total + hero["mana"]\n'
AVG_BODY = AVG_GUARD + AVG_SUM + "    return total / len(heroes)\n"


def _avg(body="    pass\n", tail=AVG_TAIL):
    return AVG_HEAD + body + tail


AVG_STARTER = _avg()
AVG_SOLUTION = _avg(AVG_BODY)
AVG_FN = AVG_HEAD.split("\n", 1)[1] + AVG_BODY
AVG_TYPED = [49, 23, 22, 12.25, 11.5, 22.0, 4, 2]
AVG_EMPTY = ("Check for an empty roster first, with `len(heroes) == 0`, and hand back 0: Python cannot divide by 0 "
             "heroes.")


def _tot(h):
    return sum(x["mana"] for x in h)


AVG_SLIPS = [
    (lambda h: _tot(h) // len(h), "Use `/` for an average: `//` throws away the part after the point.",
     "_uses('op:FloorDiv')"),
    (lambda h: _tot(h), "Divide the total by how many heroes there are: `total / len(heroes)`."),
    (lambda h: len(h) / _tot(h), "Divide the total by the count, not the count by the total: `total / len(heroes)`."),
    (lambda h: h[0]["mana"] / len(h), "Put `return` after the loop, not inside it: your function stopped after the first "
                                      "hero.", "_ret_in_loop()"),
    (lambda h: h[0]["mana"], "Put `return` after the loop, not inside it: your function stopped after the first hero.",
     "_ret_in_loop()"),
    (lambda h: h[-1]["mana"] / len(h), _RESET),
]


def _avg_row(h, want, where):
    return row("average_mana", ["heroes"], (h,), want, where, ok=LOOP_OK, typed=AVG_TYPED,
               errs=[("_tn(_e) == 'ZeroDivisionError'", AVG_EMPTY)], slips=AVG_SLIPS,
               fall="" if h else "Hand back 0 for an empty roster: that is the trial's rule.")


AVERAGE_MANA = dict(
    kind="challenge",
    id="average-mana",
    title="Average Mana",
    level="advanced",
    variant_of="total-mana",
    optional=True,
    minutes=8,
    support="light",
    tracer=True,
    summary="The advanced twin of The Party's Mana: hand back the average mana, and 0 for an empty roster.",
    martu=(
        "The advanced loop trial. Gearshift wants the [[average]]: the total divided by how many heroes there "
        "are. With `/` it can be a decimal, and that is fine.\n"
        "Write `average_mana(heroes)`. One rule more: an empty roster hands back 0. There is nobody to divide by.\n"
        "```text\naverage_mana(roster)     → 12.25\naverage_mana(roster[:2]) → 11.5\n"
        "average_mana(roster[3:]) → 22.0\naverage_mana([])         → 0\n```\n"
        "Then my hidden rosters, yes?"
    ),
    names=["average_mana", "heroes"],
    starter=AVG_STARTER,
    checkpoints=[
        dict(
            id="average",
            text="Write `average_mana(heroes)` so rows 1 to 3 of the table pass.",
            dictated=False,
            hints=[
                "Add up the mana first, with a running total. Then divide it by how many heroes there are. "
                "`len()` counts them.",
                "With other names: after the loop, `coins / len(bags)` shares the coins out evenly. `/` keeps the "
                "decimal part.",
                "Write `total = 0`, then `for hero in heroes:` with `total = total + hero[\"mana\"]` inside it. Then "
                "`return total / len(heroes)` after the loop.",
            ],
            checks=[
                _avg_row(PARTY, 12.25, ("v", 1, "average_mana(roster)", "return 12.25")),
                _avg_row(PARTY[:2], 11.5, ("v", 2, "average_mana(roster[:2])", "return 11.5")),
                _avg_row(PARTY[3:], 22.0, ("v", 3, "average_mana(roster[3:])", "return 22.0")),
            ],
            pass_line="Gearshift: Twelve and a quarter. Visor dims.",
        ),
        dict(
            id="empty-roster",
            text="Make row 4 pass: an empty roster hands back 0.",
            dictated=False,
            hints=[
                "Row 4 hands over `[]`. Its length is 0. Dividing by 0 stops Python with a [[ZeroDivisionError]], "
                "so ask about the empty roster first.",
                "A guard at the top hands back an answer early: `if len(bags) == 0:` then `return 0`. Nothing below it runs.",
                "Write `if len(heroes) == 0:` with `return 0` under it, as the function's first lines.",
            ],
            checks=[_avg_row([], 0, ("v", 4, "average_mana([])", "return 0"))],
            pass_line="Lucky: An empty party has no average. Finally, a question with my answer.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They use new rosters.",
            dictated=False,
            hints=[
                "The hidden rosters have five heroes, or one hero with 0 mana. Some averages are not whole. Divide "
                "by `len(heroes)`, never a typed 4.",
                "`9 / 2` is 4.5, and `9 // 2` is 4. An average uses `/`.",
                "Keep `return total / len(heroes)` after the loop, and the empty-roster guard at the top.",
            ],
            checks=[
                _avg_row(FIVE, 12.6, ("h", "a roster of five")),
                _avg_row([sheet("Pell", 0)], 0.0, ("h", "one hero with 0 mana")),
                _avg_row([sheet("Moth", 3), sheet("Glug", 6)], 4.5, ("h", "an average that is not whole")),
            ],
            pass_line="Mar'tu: Even the empty party. That is the case that breaks programs, yes?",
        ),
    ],
    solution=AVG_SOLUTION,
    partials=[_avg(AVG_SUM + "    return total / len(heroes)\n")],
    assemble=dict(
        lines=lines_of(AVG_FN),
        distractors=["    return total // len(heroes)", "    return total / 4", '        return "0"'],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. Empty roster? `return 0` straight away.\n2. Add up the mana with a running total.\n3. After the "
            "loop, `return total / len(heroes)`.")),
        dict(angle="picture", label="Share it out", text=(
            "```text\n8 + 15 + 4 + 22 = 49\n49 / 4 heroes   = 12.25\n0 heroes: 49 / 0\n  → ZeroDivisionError\n```\n"
            "Ask about 0 heroes before you divide.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The mana bars showed each member's mana, one at a time, in a loop. The average is one number for "
            "everyone: the same loop, a running total, then one division.")),
    ],
    predict=dict(
        q="Before you write it: what do these print?",
        code="print(49 / 4)\nprint(49 // 4)\n",
        choices=["12\n12", "12.25\n12.25", "12.25\n12"],
        answer=2,
        explain="`/` keeps the part after the point: 12.25. `//` throws it away: 12. An average uses `/`.",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        why=(
            "The mana bars looped over every member to draw each one's mana. This trial loops the same way, then "
            "shares the total out between them."
        ),
    ),
    takeaway="Guard the empty case before you divide: `len(list) == 0` means there is nothing to share.",
    wrong_answers=[
        dict(why="the starter (pass)", code=AVG_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="no empty-roster guard (the partial: ZeroDivisionError)",
             code=_avg(AVG_SUM + "    return total / len(heroes)\n"), fails_at=2,
             message_contains="Check for an empty roster first"),
        dict(why="the partial with row 4's call added back too early: Python's own ZeroDivisionError at the bottom",
             code=_avg(AVG_SUM + "    return total / len(heroes)\n", tail=AVG_TAIL.replace(AVG_ROW4, AVG_ROW4[2:])),
             fails_at=0, message_contains="ZeroDivisionError"),
        dict(why="the guard after the division",
             code=_avg(AVG_SUM + "    average = total / len(heroes)\n" + AVG_GUARD + "    return average\n"),
             fails_at=2, message_contains="Check for an empty roster first"),
        dict(why="a list compared with 0 (heroes == 0 is never true)",
             code=_avg(AVG_GUARD.replace("len(heroes) == 0", "heroes == 0") + AVG_SUM
                       + "    return total / len(heroes)\n"), fails_at=2, message_contains="`len(heroes) == 0`"),
        dict(why='text "0" for the empty roster',
             code=_avg(AVG_GUARD.replace("return 0", 'return "0"') + AVG_SUM + "    return total / len(heroes)\n"),
             fails_at=2, message_contains="Hand back a number, not text"),
        dict(why="-1 for the empty roster (not the trial's rule)",
             code=_avg(AVG_GUARD.replace("return 0", "return -1") + AVG_SUM + "    return total / len(heroes)\n"),
             fails_at=2, message_contains="Hand back 0 for an empty roster"),
        dict(why="a bare return for the empty roster (None)",
             code=_avg(AVG_GUARD.replace("return 0", "return") + AVG_SUM + "    return total / len(heroes)\n"),
             fails_at=2, message_contains="a bare `return`"),
        dict(why="// for / (the decimal part thrown away)",
             code=_avg(AVG_GUARD + AVG_SUM + "    return total // len(heroes)\n"), fails_at=1,
             message_contains="Use `/`"),
        dict(why="the total, not divided", code=_avg(AVG_GUARD + AVG_SUM + "    return total\n"), fails_at=1,
             message_contains="Divide the total by how many heroes"),
        dict(why="a typed 4 for the count", code=_avg(AVG_GUARD + AVG_SUM + "    return total / 4\n"), fails_at=1,
             message_contains="`4` typed in it"),
        dict(why="the count divided by the total (the table read backwards)",
             code=_avg(AVG_GUARD + AVG_SUM + "    return len(heroes) / total\n"), fails_at=1,
             message_contains="not the count by the total"),
        dict(why="return inside the loop",
             code=_avg(AVG_GUARD + AVG_SUM + "        return total / len(heroes)\n"), fails_at=1,
             message_contains="after the loop, not inside it"),
        dict(why="print instead of return",
             code=_avg(AVG_GUARD + AVG_SUM + "    print(total / len(heroes))\n"), fails_at=1,
             message_contains="Use `return`, not `print`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops (advanced)", opens="after Unit 6", ceiling="Units 1-6",
             skills="accumulate,divide,empty-case,guard", solo="false", dictates="",
             foreign_names="coins,bags",
             par="a roster of five (12.6); one hero with 0 mana (0.0); an average that is not whole (4.5)") + "\n"
        "T-Lo-1a, variant_of total-mana. The same roster gives 12.25, 11.5 and 22.0 (row 1 is not whole, so `//` "
        "fails on the first row). Row 4, the empty roster, is in the table and a comment in the starter (\"Once rows "
        "1 to 3 pass, add this line\"): the partial (no guard) would stop there with a ZeroDivisionError and fail "
        "every checkpoint (a wrong_answers entry adds the call back and proves it). Answers compare "
        "with a tiny tolerance, and 0 or 0.0 both pass for the empty roster. `if heroes == []:` and `if not "
        "heroes:` pass. The guard's message names `len(heroes) == 0`, which also mends `heroes == 0`. Show-rung "
        "copy-test: CP average's rung (now spelled out: `total = 0`, the loop, then the division) is the partial: "
        "no crash (row 4's call is a comment), rows 1-3 pass, row 4 fails 'Check for an empty roster first'. CP "
        "empty-roster's rung (the guard as the first lines) is the solution; CP hidden-tests' rung keeps it."
    ),
)


# =============================================================================================
# T-Lo-2 "Count the Short Gaps": count_below(wall, limit) (core). A gap equal to the limit is not below it.
# =============================================================================================

WALL = [48, 48, 47, 46, 44, 41, 37]
BELOW_HEAD = "# Trial: count the short gaps.\ndef count_below(wall, limit):\n"
BELOW_TAIL = (
    "\n\nwall = [48, 48, 47, 46, 44, 41, 37]\n\n"
    "# Visible tests. They should show\n"
    "# 3, then 5, then 0.\n"
    "# (With only pass, each shows None.)\n"
    "print(count_below(wall, 46))\n"
    "print(count_below(wall, 48))\n"
    "print(count_below(wall, 30))\n"
)
BELOW_BODY = ("    count = 0\n    for gap in wall:\n        if gap < limit:\n            count = count + 1\n"
              "    return count\n")


def _below(body="    pass\n", tail=BELOW_TAIL, head=BELOW_HEAD):
    return head + body + tail


BELOW_STARTER = _below()
BELOW_SOLUTION = _below(BELOW_BODY)
BELOW_FN = BELOW_HEAD.split("\n", 1)[1] + BELOW_BODY
BELOW_TYPED = [46, 48, 30, 3, 5]
BELOW_SLIPS = [
    (lambda w, n: sum(1 for g in w if g <= n), "A gap equal to `limit` is not below it: use `<`, not `<=`.",
     "_uses('op:LtE')"),
    (lambda w, n: sum(1 for g in w if g >= n), "Count the gaps *below* the limit, `gap < limit`: yours counted the "
                                               "gaps at or above it.", "_uses('op:GtE')"),
    (lambda w, n: sum(1 for g in w if g > n), "Count the gaps *below* the limit, `gap < limit`: yours counted the "
                                              "gaps above it.", "_uses('op:Gt')"),
    (lambda w, n: w.count(n), "Count the gaps smaller than the limit, not the gaps equal to it: `.count()` finds "
                              "equal items only.", "_uses('attr:count')"),
    (lambda w, n: sum(g for g in w if g < n), "Add 1 for each short gap, `count = count + 1`, not the gap itself."),
    (lambda w, n: sum(1 for g in w[:-1] if g < n), "Walk every gap: your loop skipped the last one. `for gap in "
                                                   "wall:` reads them all.", "_uses('call:range') or _uses('node:Slice')"),
    (lambda w, n: sum(1 for g in w[1:] if g < n), "Walk every gap: your loop skipped the first one. `range(1, ...)` "
                                                  "starts at the second gap.", "_uses('call:range') or _uses('node:Slice')"),
    (lambda w, n: 1 if w and w[-1] < n else 0, "Make `count = 0` once, before the loop. Inside it, only add 1.",
     "_set_in_loop()"),
    (lambda w, n: 1 if w and w[0] < n else 0, "Put `return` after the loop, not inside it: your function stopped after the "
                                              "first gap.", "_ret_in_loop()"),
    (lambda w, n: _leading_below(w, n), "Walk every gap, with no `break`: a gap that is not short does not end the "
                                        "count. The `if` alone decides what counts.", "_uses('node:Break')"),
]


def _leading_below(w, n):
    count = 0
    for g in w:
        if g < n:
            count += 1
        else:
            break
    return count


def _below_row(args, want, where):
    return row("count_below", ["wall", "limit"], args, want, where, typed=BELOW_TYPED, slips=BELOW_SLIPS)


COUNT_BELOW = dict(
    kind="challenge",
    id="count-below",
    title="Count the Short Gaps",
    level="core",
    optional=True,
    minutes=6,
    support="light",
    tracer=True,
    summary="Count the gaps on the chalk wall that are below a limit. A gap equal to the limit does not count.",
    martu=(
        "My chalk wall, the hours between bursts. Oogrish asks: how many gaps are shorter than a day and a half? "
        "A function (a recipe) with a loop and a question inside.\n"
        "Write `count_below(wall, limit)`. It hands back how many gaps are below `limit`. A gap equal to `limit` is "
        "not below it.\n"
        "```text\ncount_below(wall, 46) → 3\ncount_below(wall, 48) → 5\ncount_below(wall, 30) → 0\n```\n"
        "Row 1: the 46 on the wall does not count. My hidden tests try other walls, yes?"
    ),
    names=["count_below", "wall", "limit"],
    starter=BELOW_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `count_below(wall, limit)` so every row of the table passes.",
            dictated=False,
            hints=[
                "Walk the wall one gap at a time. Count a gap only when it is smaller than `limit`: a gap equal to "
                "it does not count.",
                "With other names: `short = 0`, then `for step in steps:` with `if step < 5:` inside it, and `short = "
                "short + 1` under that.",
                "Write `count = 0`, then `for gap in wall:` with `if gap < limit:` inside, `count = count + 1` under "
                "that, and `return count` after the loop.",
            ],
            checks=[
                _below_row((WALL, 46), 3, ("v", 1, "count_below(wall, 46)", "return 3")),
                _below_row((WALL, 48), 5, ("v", 2, "count_below(wall, 48)", "return 5")),
                _below_row((WALL, 30), 0, ("v", 3, "count_below(wall, 30)", "return 0")),
            ],
            pass_line="Oogrish: Three gaps under forty-six. The wall is shrinking. Steady.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try an empty wall, and a gap at the limit.",
            dictated=False,
            hints=[
                "The hidden tests try an empty wall, a gap exactly at the limit, and walls you have not seen. Read "
                "the trial's rule for each one.",
                "`5 < 5` is `False`, and `5 <= 5` is `True`. *Below* means `<`.",
                "Keep `if gap < limit:`, with `<`, and `count = 0` before the loop, so an empty wall hands back 0.",
            ],
            checks=[
                _below_row(([40, 33, 31, 26, 22], 30), 2, ("h", "another wall")),
                _below_row(([20, 25, 25, 30], 25), 1, ("h", "a gap exactly at the limit")),
                _below_row(([], 40), 0, ("h", "an empty wall")),
                _below_row(([12, 9, 5], 50), 3, ("h", "every gap below the limit")),
            ],
            pass_line="Mar'tu: Any wall. Even an empty one. I hope mine never is.",
        ),
    ],
    solution=BELOW_SOLUTION,
    assemble=dict(
        lines=lines_of(BELOW_FN),
        distractors=["        if gap <= limit:", "            count = count + gap", "        count = 0"],
    ),
    another_way=[
        dict(angle="step-by-step", text=(
            "1. `count = 0`, before the loop.\n2. `for gap in wall:`.\n3. Inside: if `gap < limit`, add 1 to "
            "`count`.\n4. After the loop: `return count`.")),
        dict(angle="picture", label="Row 1, gap by gap", text=(
            "```text\ngap  < 46?  count\n48   no     0\n48   no     0\n47   no     0\n46   no     0\n"
            "44   yes    1\n41   yes    2\n37   yes    3\n```\n46 is not below 46.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "Oogrish ran a finger down this wall: 48, 48, 47, 46, 44, 41, 37. \"The decay is accelerating.\" Counting "
            "the short gaps is how you see it in one number.")),
    ],
    pair_talk="Row 1's wall has a gap of exactly 46, and the limit is 46. Tell your partner why that gap does not "
              "count.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why="You have seen this wall: the hours between bursts, shrinking. A loop with an `if` counts how many are "
            "already short.",
    ),
    takeaway="To count with a rule, start at 0, loop, and add 1 inside an `if`. *Below* is `<`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=BELOW_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="<= for < (the gap at the limit counted)", code=_below(BELOW_BODY.replace("gap < limit", "gap <= limit")),
             fails_at=1, message_contains="use `<`, not `<=`"),
        dict(why="> for < (the gaps above counted: the table read backwards)",
             code=_below(BELOW_BODY.replace("gap < limit", "gap > limit")), fails_at=1,
             message_contains="counted the gaps above it"),
        dict(why="the count reset inside the loop",
             code=_below("    for gap in wall:\n        count = 0\n        if gap < limit:\n"
                         "            count = count + 1\n    return count\n"), fails_at=1,
             message_contains="Make `count = 0` once"),
        dict(why="return inside the loop",
             code=_below(BELOW_BODY.replace("    return count\n", "        return count\n")), fails_at=1,
             message_contains="after the loop, not inside it"),
        dict(why="print instead of return",
             code=_below(BELOW_BODY.replace("    return count\n", "    print(count)\n")), fails_at=1,
             message_contains="Use `return`, not `print`"),
        dict(why="row 1's answer typed (return 3)", code=_below("    return 3\n"), fails_at=1,
             message_contains="`3` typed in it"),
        dict(why="the table typed as an if-chain on the limit (the hidden walls catch it)",
             code=_below("    if limit == 46:\n        return 3\n    if limit == 48:\n        return 5\n"
                         "    return 0\n"), fails_at=2, message_contains="typed in it"),
        dict(why="the wall sorted inside the function (the list handed in is changed)",
             code=_below("    wall.sort()\n" + BELOW_BODY), fails_at=1, message_contains="Leave `wall` as it was"),
        dict(why="the parameters in the other order (the table read backwards)",
             code=_below(BELOW_BODY, head=BELOW_HEAD.replace("(wall, limit)", "(limit, wall)"), tail=""), fails_at=1,
             message_contains="in the order of the first line"),
        dict(why="the gaps added, not counted",
             code=_below(BELOW_BODY.replace("count = count + 1", "count = count + gap")), fails_at=1,
             message_contains="Add 1 for each short gap"),
        dict(why="range(len(wall) - 1): the last gap skipped",
             code=_below("    count = 0\n    for i in range(len(wall) - 1):\n        if wall[i] < limit:\n"
                         "            count = count + 1\n    return count\n"), fails_at=1,
             message_contains="skipped the last one"),
        dict(why="range(1, len(wall)): the first gap skipped (only a hidden wall shows it)",
             code=_below("    count = 0\n    for i in range(1, len(wall)):\n        if wall[i] < limit:\n"
                         "            count = count + 1\n    return count\n"), fails_at=2,
             message_contains="skipped the first one"),
        dict(why=".count(limit): equal gaps only", code=_below("    return wall.count(limit)\n"), fails_at=1,
             message_contains="`.count()` finds equal items only"),
        dict(why="-1 for an empty wall (the shrink trial's 'none found'): no slip matches, so the hidden-test "
                 "fallback (make the case yourself with a print)",
             code=_below("    if len(wall) == 0:\n        return -1\n" + BELOW_BODY), fails_at=2,
             message_contains="It passes the table, not this test. Make this case yourself"),
        dict(why="break at the first gap that is not short (the count ends early)",
             code=_below(BELOW_BODY.replace("            count = count + 1\n",
                                            "            count = count + 1\n        else:\n            break\n")),
             fails_at=1, message_contains="with no `break`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops", opens="after Unit 6", ceiling="Units 1-6",
             skills="loop-filter,count,boundary", solo="false", dictates="", foreign_names="short,steps,step",
             par="another wall; a gap exactly at the limit; an empty wall; every gap below the limit") + "\n"
        "T-Lo-2. Mar'tu's own wall (48, 48, 47, 46, 44, 41, 37). Row 1's limit, 46, is ON the wall, so the "
        "boundary is in the visible table: `<=` fails the first row. Row 2's limit is the wall's top, so counting "
        "the gaps above fails visibly (row 1 alone cannot tell: three gaps are above 46 too). The top-level list is "
        "`wall`, the same name as the parameter (it fits 36 characters), so there is no outer-name slip here. A "
        "skipped first gap only shows on a hidden wall whose first gap is short. `range(len(wall))` and a list in "
        "one line (`len([g for g in wall if g < limit])`) pass. Show-rung copy-test: CP1's rung is the solution "
        "(no crash, every checkpoint passes; row 1 decides `<`, so the rung keeps the one sign); CP2's rung keeps it."
    ),
)


# =============================================================================================
# T-Lo-2a "The First Big Shrink": first_shrink_over(wall, amount) -> the index of the first gap whose shrink is
# larger than amount, else -1 (an early exit; advanced)
# =============================================================================================

SHRINK_HEAD = "# Trial: the first big shrink.\ndef first_shrink_over(wall, amount):\n"
SHRINK_TAIL = (
    "\n\nwall = [48, 48, 47, 46, 44, 41, 37]\n\n"
    "# Visible tests. They should show\n"
    "# 5, 2, 6, then -1.\n"
    "# (With only pass, each shows None.)\n"
    "print(first_shrink_over(wall, 2))\n"
    "print(first_shrink_over(wall, 0))\n"
    "print(first_shrink_over(wall, 3))\n"
    "print(first_shrink_over(wall, 4))\n"
)
SHRINK_LOOP = (
    "    for i in range(1, len(wall)):\n"
    "        before = wall[i - 1]\n"
    "        shrink = before - wall[i]\n"
    "        if shrink > amount:\n"
    "            return i\n"
)
SHRINK_BODY = SHRINK_LOOP + "    return -1\n"


def _shrink(body="    pass\n", tail=SHRINK_TAIL):
    return SHRINK_HEAD + body + tail


SHRINK_STARTER = _shrink()
SHRINK_SOLUTION = _shrink(SHRINK_BODY)
SHRINK_FN = SHRINK_HEAD.split("\n", 1)[1] + SHRINK_BODY
SHRINK_TYPED = [5, 2, 6, 3, 4]
SHRINK_NONE = ("After the loop, `return -1`: when no shrink is large enough, the loop ends and the function needs one "
               "more `return`.")


def _first_i(w, a, start=1, cmp=lambda s, a: s > a, give=lambda i, s: i, last=False, flip=False, end=0, none=-1):
    found = none
    for i in range(start, len(w) - end):
        s = (w[i] - w[i - 1]) if flip else (w[i - 1] - w[i])
        if cmp(s, a):
            if not last:
                return give(i, s)
            found = give(i, s)
    return found


def _since_start(w, a):
    for i in range(1, len(w)):
        if w[0] - w[i] > a:
            return i
    return -1


SHRINK_SLIPS = [
    (lambda w, a: _first_i(w, a, cmp=lambda s, a: s >= a), "*Larger than* means `>`: a shrink equal to the amount "
                                                           "does not count.", "_uses('op:GtE')"),
    (lambda w, a: _first_i(w, a, cmp=lambda s, a: abs(s) > a), "A gap that grows is not a shrink: use "
                                                               "`wall[i - 1] - wall[i]` as it is, with no `abs()`.",
     "_uses('call:abs')"),
    (lambda w, a: _first_i(w, a, end=1), "Walk to the end of the wall: `range(1, len(wall))` reads the last gap too. "
                                         "Yours stopped one gap early.", "_stops_early()"),
    (lambda w, a: _first_i(w, a, none=0), "When no shrink is large enough, hand back -1, not 0: 0 is a real position "
                                          "on the wall."),
    (lambda w, a: _since_start(w, a), "Take each gap from the one just before it, `wall[i - 1]`, not from the first "
                                      "gap: a shrink is one step on the wall.", "_has(0)"),
    (lambda w, a: _first_i(w, a, give=lambda i, s: i - 1), "Hand back the position of the gap that shrank, `i`, not "
                                                           "the gap before it."),
    (lambda w, a: _first_i(w, a, give=lambda i, s: s), "Hand back the gap's position, `i`, not the shrink itself."),
    (lambda w, a: _first_i(w, a, last=True), "Stop at the first one: `return i` as soon as a shrink is large enough. "
                                             "Your function kept looking and found a later one."),
    (lambda w, a: (1 if len(w) > 1 and w[0] - w[1] > a else -1),
     "Hand back -1 only after the loop has read every gap: your function gave up at the first gap that did not match.",
     "_early_minus()"),
    (lambda w, a: _first_i(w, a, flip=True), "Take this gap from the one before, `wall[i - 1] - wall[i]`: yours took "
                                             "them the other way round, so a shrink came out negative."),
    (lambda w, a: _first_i(w, a, start=0), "Start the loop at 1, `range(1, len(wall))`: at 0 there is no gap before, "
                                           "so `wall[i - 1]` reads the last gap instead."),
]
SHRINK_ERRS = [
    ("_tn(_e) == 'IndexError'",
     "Stay on the wall: `wall[i + 1]` runs past the last gap. Loop `for i in range(1, len(wall)):` and compare "
     "`wall[i - 1]` with `wall[i]`."),
]


def _shrink_row(args, want, where):
    return row("first_shrink_over", ["wall", "amount"], args, want, where, typed=SHRINK_TYPED, errs=SHRINK_ERRS,
               slips=SHRINK_SLIPS, none=SHRINK_NONE if want == -1 else "")


FIRST_SHRINK_OVER = dict(
    kind="challenge",
    id="first-shrink-over",
    title="The First Big Shrink",
    level="advanced",
    variant_of="count-below",
    optional=True,
    minutes=10,
    support="light",
    tracer=True,
    summary="The advanced twin of Count the Short Gaps: find where the wall first shrank by more than an amount, or "
            "hand back -1.",
    martu=(
        "The advanced wall trial. Each gap's shrink is the gap before it minus this gap. The first gap has no "
        "shrink.\n"
        "Write `first_shrink_over(wall, amount)`. It hands back the *position* of the first gap whose shrink is larger "
        "than `amount`. If there is none, it hands back -1. Stop as soon as you find it: an [[early exit]].\n"
        "```text\nshrinks: -, 0, 1, 1, 2, 3, 4\nfirst_shrink_over(wall, 2) → 5\nfirst_shrink_over(wall, 0) → 2\n"
        "first_shrink_over(wall, 3) → 6\nfirst_shrink_over(wall, 4) → -1\n```"
    ),
    names=["first_shrink_over", "wall", "amount"],
    starter=SHRINK_STARTER,
    checkpoints=[
        dict(
            id="find-it",
            text="Write `first_shrink_over(wall, amount)` so rows 1 to 3 of the table pass.",
            dictated=False,
            hints=[
                "A shrink needs the gap before, so start the loop at position 1. At each position, work out the "
                "shrink, and hand back that position the first time it is larger than `amount`.",
                "With other names: `for i in range(1, len(steps)):` then `drop = steps[i - 1] - steps[i]` reads each "
                "step and the one before it.",
                "Write `for i in range(1, len(wall)):`, with `before = wall[i - 1]` and `shrink = before - wall[i]` "
                "inside, then `if shrink > amount:` with `return i` under it.",
            ],
            checks=[
                _shrink_row((WALL, 2), 5, ("v", 1, "first_shrink_over(wall, 2)", "return 5")),
                _shrink_row((WALL, 0), 2, ("v", 2, "first_shrink_over(wall, 0)", "return 2")),
                _shrink_row((WALL, 3), 6, ("v", 3, "first_shrink_over(wall, 3)", "return 6")),
            ],
            pass_line="Oogrish: Position five. Three hours lost in one burst. Steady, now.",
        ),
        dict(
            id="none-found",
            text="Make row 4 pass: when no shrink is larger than `amount`, hand back -1.",
            dictated=False,
            hints=[
                "Row 4: no shrink on the wall is larger than 4. The loop ends without handing anything back, so the function "
                "needs one more line after it.",
                "A line after the loop runs only when the loop never handed anything back. That is where \"not found\" goes.",
                "Write `return -1` after the loop, not indented under it.",
            ],
            checks=[_shrink_row((WALL, 4), -1, ("v", 4, "first_shrink_over(wall, 4)", "return -1"))],
            pass_line="Lucky: Minus one. Nothing found. My favorite answer.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try short walls, and a shrink equal to `amount`.",
            dictated=False,
            hints=[
                "The hidden tests try an empty wall and a wall of one gap. One shrink equals `amount`. One wall has "
                "two big shrinks, one shrinks at position 1, and one has a gap that grows.",
                "`range(1, len(steps))` is empty when there are fewer than 2 steps, so the loop never runs. *Larger "
                "than* is `>`.",
                "Keep `for i in range(1, len(wall)):` and `if shrink > amount:`, with `return -1` after the loop.",
            ],
            checks=[
                _shrink_row(([40, 39, 30, 29, 20], 5), 2, ("h", "another wall, with two big shrinks")),
                _shrink_row(([30, 24, 22, 21], 4), 1, ("h", "a big shrink at position 1")),
                _shrink_row(([30, 27, 26], 3), -1, ("h", "a shrink exactly equal to the amount")),
                _shrink_row(([], 1), -1, ("h", "an empty wall")),
                _shrink_row(([44], 0), -1, ("h", "a wall with one gap")),
                _shrink_row(([20, 18, 40, 30], 5), 3, ("h", "a wall where one gap grows")),
            ],
            pass_line="Mar'tu: \"The decay is accelerating.\" Now you can say where.",
        ),
    ],
    solution=SHRINK_SOLUTION,
    partials=[_shrink(SHRINK_LOOP)],
    assemble=dict(
        lines=lines_of(SHRINK_FN),
        distractors=["        if shrink >= amount:", "            return shrink", "        return -1"],
    ),
    another_way=[
        dict(angle="picture", label="Row 1, position by position", text=(
            "```text\ni  before  gap  shrink  > 2?\n1  48      48   0       no\n2  48      47   1       no\n"
            "3  47      46   1       no\n4  46      44   2       no\n5  44      41   3       yes\n```\nIt hands back 5. "
            "Position 6 is never read.")),
        dict(angle="step-by-step", text=(
            "1. `for i in range(1, len(wall)):`.\n2. The shrink is `wall[i - 1] - wall[i]`.\n3. Larger than "
            "`amount`? `return i` at once.\n4. After the loop: `return -1`.")),
        dict(angle="another way to stop", label="With break", text=(
            "`found = -1` before the loop, then `found = i` and `break` inside the `if`, and `return found` after "
            "the loop. Same answer: `break` is an early exit too.")),
    ],
    predict=dict(
        q="Before you write it: which positions does this loop visit?",
        code="steps = [9, 7, 4]\nfor i in range(1, len(steps)):\n    print(i)\n",
        choices=["0\n1\n2", "1\n2", "1\n2\n3"],
        answer=1,
        explain="`range(1, 3)` starts at 1 and stops before 3. Position 0 has no step before it, so the loop skips "
                "it.",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="chalk-wall",
        why=(
            "\"The decay is accelerating,\" Mar'tu said at the chalk wall. This function finds the first place where "
            "it sped up by more than you allow."
        ),
    ),
    takeaway="Hand back the answer as soon as you find it; put the \"not found\" answer after the loop.",
    wrong_answers=[
        dict(why="the starter (pass)", code=SHRINK_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="no return -1 after the loop (the partial: None)", code=_shrink(SHRINK_LOOP), fails_at=2,
             message_contains="After the loop, `return -1`"),
        dict(why="return -1 inside the loop (gives up at the first gap)",
             code=_shrink(SHRINK_LOOP + "        else:\n            return -1\n"), fails_at=1,
             message_contains="gave up at the first gap"),
        dict(why="i - 1: the gap before it", code=_shrink(SHRINK_BODY.replace("return i\n", "return i - 1\n")),
             fails_at=1, message_contains="not the gap before it"),
        dict(why=">= for > (a shrink equal to the amount counted)",
             code=_shrink(SHRINK_BODY.replace("shrink > amount", "shrink >= amount")), fails_at=1,
             message_contains="*Larger than* means `>`"),
        dict(why="the shrink returned, not its position (the table read backwards)",
             code=_shrink(SHRINK_BODY.replace("return i\n", "return shrink\n")), fails_at=1,
             message_contains="not the shrink itself"),
        dict(why="no early exit: the last big shrink kept",
             code=_shrink("    found = -1\n    for i in range(1, len(wall)):\n        before = wall[i - 1]\n"
                          "        shrink = before - wall[i]\n        if shrink > amount:\n            found = i\n"
                          "    return found\n"), fails_at=1, message_contains="Stop at the first one"),
        dict(why="range(len(wall)): wall[-1] read on the first pass (only a growing gap shows it)",
             code=_shrink(SHRINK_BODY.replace("range(1, len(wall))", "range(len(wall))")), fails_at=3,
             message_contains="Start the loop at 1"),
        dict(why="growth for shrink (this gap minus the one before)",
             code=_shrink(SHRINK_BODY.replace("shrink = before - wall[i]", "shrink = wall[i] - before")), fails_at=1,
             message_contains="the other way round"),
        dict(why="wall[i] - wall[i + 1] over range(len(wall)) (the bottom prints: Python's IndexError)",
             code=_shrink("    for i in range(len(wall)):\n        if wall[i] - wall[i + 1] > amount:\n"
                          "            return i + 1\n    return -1\n"), fails_at=0,
             message_contains="IndexError: list index out of range"),
        dict(why="wall[i] - wall[i + 1], the prints gone",
             code=_shrink("    for i in range(len(wall)):\n        if wall[i] - wall[i + 1] > amount:\n"
                          "            return i + 1\n    return -1\n", tail=""), fails_at=2,
             message_contains="Stay on the wall"),
        dict(why="row 1's answer typed (return 5)", code=_shrink("    return 5\n"), fails_at=1,
             message_contains="`5` typed in it"),
        dict(why="print instead of return",
             code=_shrink(SHRINK_LOOP.replace("return i", "print(i)") + "    print(-1)\n"), fails_at=1,
             message_contains="Use `return`, not `print`"),
        dict(why="abs() of the shrink (a gap that grows counted as a shrink)",
             code=_shrink(SHRINK_BODY.replace("shrink = before - wall[i]", "shrink = abs(before - wall[i])")),
             fails_at=3, message_contains="with no `abs()`"),
        dict(why="range(1, len(wall) - 1): the last gap never read",
             code=_shrink(SHRINK_BODY.replace("range(1, len(wall))", "range(1, len(wall) - 1)")), fails_at=1,
             message_contains="stopped one gap early"),
        dict(why="each gap taken from the first gap, not the one before it",
             code=_shrink(SHRINK_BODY.replace("before = wall[i - 1]", "before = wall[0]")), fails_at=1,
             message_contains="not from the first gap"),
        dict(why="range(2, len(wall)): position 1 skipped (only a hidden wall that shrinks at position 1 shows it)",
             code=_shrink(SHRINK_BODY.replace("range(1, len(wall))", "range(2, len(wall))")), fails_at=3,
             message_contains="Hidden test: a big shrink at position 1"),
        dict(why="0 for none found (0 is a real position)", code=_shrink(SHRINK_LOOP + "    return 0\n"), fails_at=2,
             message_contains="not 0"),
        dict(why='text "-1" when none is found',
             code=_shrink(SHRINK_LOOP + '    return "-1"\n'), fails_at=2, message_contains="Hand back a number, not text"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops (advanced)", opens="after Unit 6", ceiling="Units 1-6",
             skills="loop-neighbors,early-exit,not-found,boundary", solo="false", dictates="",
             foreign_names="steps,drop",
             par="another wall, with two big shrinks; a big shrink at position 1; a shrink exactly equal to the "
                 "amount; an empty wall; a wall with one gap; a wall where one gap grows") + "\n"
        "T-Lo-2a, variant_of count-below. 'Shrink' is the gap before minus this gap (Unit 6's 5A-05), and the "
        "position returned is the later gap's (the one that shrank). Mar'tu's wall has shrinks 0, 1, 1, 2, 3, 4, so "
        "row 1 (amount 2) passes a shrink EQUAL to 2 before the answer (`>=` fails visibly), row 2 (amount 0) "
        "skips the 0 shrink, row 3 is the last gap, and row 4 (amount 4) finds none because the largest shrink "
        "equals 4. The partial has no `return -1` (None, told 'After the loop, `return -1`'). A `break` with a "
        "`found` variable passes. `range(len(wall))` reads `wall[-1]` on its first pass: harmless on a shrinking "
        "wall, so a hidden wall where one gap grows catches it (u06c Q3's slip). 'A big shrink at position 1' catches "
        "a loop that starts at 2 (no other row's answer is 1). Show-rung copy-test: CP find-it's rung is the "
        "partial: no crash (row 4 prints None), rows 1-3 pass (row 1 decides `>`, so the rung keeps the one sign), "
        "row 4 fails 'After the loop, `return -1`'. CP none-found's rung adds `return -1` (the solution); CP "
        "hidden-tests' rung keeps it."
    ),
)


# =============================================================================================
# T-Lo-3 "Who Needs Glug First?": lowest_mana_name(heroes) (core)
# =============================================================================================

LOW_HEAD = "# Trial: who needs glug first?\ndef lowest_mana_name(heroes):\n"
LOW_TAIL = (
    "\n\n" + roster_code("roster", PARTY) + "\n"
    "# Visible tests. They should show\n"
    "# Bomb Shell, Oogrish, then Lucky.\n"
    "# (With only pass, each shows None.)\n"
    "print(lowest_mana_name(roster))\n"
    "print(lowest_mana_name(roster[:2]))\n"
    "print(lowest_mana_name(roster[3:]))\n"
)
LOW_START = '    name = heroes[0]["name"]\n    low = heroes[0]["mana"]\n'
LOW_LOOP = (
    "    for hero in heroes:\n"
    '        if hero["mana"] < low:\n'
    '            name = hero["name"]\n'
    '            low = hero["mana"]\n'
)
LOW_BODY = LOW_START + LOW_LOOP + "    return name\n"


def _low(body="    pass\n", tail=LOW_TAIL, head=LOW_HEAD):
    return head + body + tail


LOW_STARTER = _low()
LOW_SOLUTION = _low(LOW_BODY)
LOW_FN = LOW_HEAD.split("\n", 1)[1] + LOW_BODY
LOW_TYPED = ["Bomb Shell", "Oogrish", "Lucky", 4, 8, 22]


def _lowest(h, cmp=lambda m, low: m < low, start=None, keep_low=True, zero_unset=False):
    if start is None:
        name, low = h[0]["name"], h[0]["mana"]
    else:
        name, low = "", start
    for x in h:
        better = (low == 0 or x["mana"] < low) if zero_unset else cmp(x["mana"], low)
        if better:
            name = x["name"]
            if keep_low:
                low = x["mana"]
    return name


def _lowest_unnamed(h):
    name, low = "", h[0]["mana"]
    for x in h:
        if x["mana"] < low:
            name, low = x["name"], x["mana"]
    return name


_LOW_START_MSG = ("Start from the first hero, `heroes[0]`, not a typed number: every hero here has more mana than your "
                  "start.")
LOW_SLIPS = [
    (lambda h: _lowest(h, cmp=lambda m, low: m > low), "Lowest means the smallest mana: use `<`, not `>`.",
     "_uses('op:Gt')"),
    (lambda h: _lowest(h, keep_low=False), "When you keep a new name, keep its mana too: update `low` on the same "
                                           "pass."),
    (lambda h: _lowest(h, start=1000), _LOW_START_MSG),
    (lambda h: _lowest(h, start=0, zero_unset=True), "Don't use 0 to mean \"nothing yet\": a hero can have 0 mana. "
                                                     "Start from the first hero, `heroes[0]`."),
    (lambda h: _lowest_unnamed(h), "Start `name` at the first hero's name, `heroes[0][\"name\"]`, as well as `low`: "
                                   "when the first hero is the lowest, nothing ever replaces an empty name.",
     "_assigns('') and not _assigns(0)"),
    (lambda h: _lowest(h, start=0), "Start from the first hero's mana, not 0: no hero has less than 0, so nothing ever "
                                    "replaced your start."),
    (lambda h: h[0]["name"], "Put `return` after the loop, not inside it: your function stopped after the first hero.",
     "_ret_in_loop()"),
    (lambda h: h[-1]["name"], "Compare before you keep a name: `if hero[\"mana\"] < low:`. Your function kept the "
                              "last hero."),
]
LOW_KIND = {"int": "Hand back the hero's name, not their mana: keep the name in its own variable as you loop.",
            "dict": "Hand back the hero's `\"name\"`, not the whole sheet."}


LOW_ERRS = [
    ("_tn(_e) == 'IndexError'",
     "Start from `heroes[0]`, the first hero: positions count from 0, so a roster of one hero has no `heroes[1]`."),
]


def _low_row(h, want, where, slips=LOW_SLIPS, typed=LOW_TYPED):
    return row("lowest_mana_name", ["heroes"], (h,), want, where, ok=LOOP_OK, typed=typed, slips=slips,
               kind=LOW_KIND, errs=LOW_ERRS)


LOWEST_MANA_NAME = dict(
    kind="challenge",
    id="lowest-mana-name",
    title="Who Needs Glug First?",
    level="core",
    optional=True,
    minutes=7,
    support="light",
    tracer=True,
    summary="Hand back the name of the hero with the lowest mana on a roster.",
    martu=(
        "Lucky's canteen of glug heals, and smells terrible. Who gets the first sip? The hero with the least "
        "mana. A function (a recipe) that finds them.\n"
        "Write `lowest_mana_name(heroes)`. It hands back the *name* of the hero with the lowest `\"mana\"`. Every "
        "roster has at least one hero.\n"
        "```text\nlowest_mana_name(roster)\n  → \"Bomb Shell\"\nlowest_mana_name(roster[:2])\n  → \"Oogrish\"\n"
        "lowest_mana_name(roster[3:])\n  → \"Lucky\"\n```\n"
        "My hidden rosters hold heroes you have not met, yes?"
    ),
    names=["lowest_mana_name", "heroes"],
    starter=LOW_STARTER,
    checkpoints=[
        dict(
            id="visible-tests",
            text="Write `lowest_mana_name(heroes)` so every row of the table passes.",
            dictated=False,
            hints=[
                "Start with the first hero as the lowest so far. Walk the roster; when a hero has less mana, keep "
                "that hero's name and mana instead. Hand back the name after the loop.",
                "With other names: `best = jars[0][\"name\"]` and `least = jars[0][\"size\"]` before the loop. Inside, "
                "`if jar[\"size\"] < least:` swaps both.",
                "Write `name = heroes[0][\"name\"]` and `low = heroes[0][\"mana\"]`. Then `for hero in heroes:` with "
                "`if hero[\"mana\"] < low:` inside it, and under that `name = hero[\"name\"]` and `low = "
                "hero[\"mana\"]`. Then `return name` after the loop.",
            ],
            checks=[
                _low_row(PARTY, "Bomb Shell", ("v", 1, "lowest_mana_name(roster)", 'return "Bomb Shell"')),
                _low_row(PARTY[:2], "Oogrish", ("v", 2, "lowest_mana_name(roster[:2])", 'return "Oogrish"')),
                _low_row(PARTY[3:], "Lucky", ("v", 3, "lowest_mana_name(roster[3:])", 'return "Lucky"')),
            ],
            pass_line="Bomb Shell: Glug. Fine.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try high mana, and a hero with 0.",
            dictated=False,
            hints=[
                "The hidden rosters have very high mana, a 0, and the lowest hero last. Start from the roster's own "
                "first hero, never a typed number.",
                "Keep two things together. When the name changes, the mana you check against changes too.",
                "Keep `low = heroes[0][\"mana\"]`, and update `low = hero[\"mana\"]` on the same pass as `name`.",
            ],
            checks=[
                _low_row([sheet("Pell", 1400000), sheet("Brakka", 1200000), sheet("Moss", 1600000)], "Brakka",
                         ("h", "very high mana")),
                _low_row([sheet("Ivo", 12), sheet("Glug", 7), sheet("Moth", 9), sheet("Tinplate", 30)], "Glug",
                         ("h", "another roster")),
                _low_row([sheet("Pell", 10), sheet("Moss", 9), sheet("Ivo", 2)], "Ivo", ("h", "the lowest hero last")),
                _low_row([sheet("Glug", 0), sheet("Moth", 5)], "Glug", ("h", "a hero with 0 mana first")),
            ],
            pass_line="Lucky: Fine. But I'm keeping track of who drinks my glug.",
        ),
    ],
    solution=LOW_SOLUTION,
    assemble=dict(
        lines=lines_of(LOW_FN),
        distractors=['        if hero["mana"] > low:', "    low = 100", '    return low'],
    ),
    another_way=[
        dict(angle="picture", label="Row 1, hero by hero", text=(
            "```text\nhero        mana  name kept\nOogrish     8     Oogrish\nGearshift   15    Oogrish\n"
            "Bomb Shell  4     Bomb Shell\nLucky       22    Bomb Shell\n```")),
        dict(angle="step-by-step", text=(
            "1. Before the loop: the first hero's name and mana.\n2. For each hero: less mana than `low`? Keep "
            "this name AND this mana.\n3. After the loop: hand back the name.")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "The mana bars showed who was running low, one bar at a time. This function reads the same sheets in a "
            "loop and names the lowest.")),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        why=(
            "The mana bars drew each member's mana in a loop. The same loop can keep track of who is lowest, and "
            "hand back that hero's name."
        ),
    ),
    takeaway="To find the lowest, start from the first item, keep the best name and its value, and compare with `<`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=LOW_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the mana returned, not the name (the wrong type)",
             code=_low(LOW_START + LOW_LOOP + "    return low\n"), fails_at=1, message_contains="not their mana"),
        dict(why="the whole sheet returned",
             code=_low("    best = heroes[0]\n    for hero in heroes:\n        if hero[\"mana\"] < best[\"mana\"]:\n"
                       "            best = hero\n    return best\n"), fails_at=1,
             message_contains="not the whole sheet"),
        dict(why="> for < (the highest mana)", code=_low(LOW_BODY.replace('hero["mana"] < low', 'hero["mana"] > low')),
             fails_at=1, message_contains="use `<`, not `>`"),
        dict(why="a typed start of 100 (passes the table; very high mana catches it)",
             code=_low('    name = ""\n    low = 100\n' + LOW_LOOP + "    return name\n"), fails_at=2,
             message_contains="not a typed number"),
        dict(why="a start of 0: nothing is ever lower",
             code=_low('    name = ""\n    low = 0\n' + LOW_LOOP + "    return name\n"), fails_at=1,
             message_contains="not 0"),
        dict(why="0 used to mean 'nothing yet' (a hero with 0 mana first)",
             code=_low('    name = ""\n    low = 0\n    for hero in heroes:\n'
                       '        if low == 0 or hero["mana"] < low:\n            name = hero["name"]\n'
                       '            low = hero["mana"]\n    return name\n'), fails_at=2,
             message_contains="a hero can have 0 mana"),
        dict(why="name started empty while low starts at the first hero (the first hero is the lowest in row 2)",
             code=_low('    name = ""\n    low = heroes[0]["mana"]\n' + LOW_LOOP + "    return name\n"), fails_at=1,
             message_contains="Start `name` at the first hero's name"),
        dict(why="a typed start of 9999 (very high mana catches it)",
             code=_low('    name = ""\n    low = 9999\n' + LOW_LOOP + "    return name\n"), fails_at=2,
             message_contains="not a typed number"),
        dict(why="the name kept, but not its mana (passes the table; another roster catches it)",
             code=_low(LOW_START + LOW_LOOP.replace('            low = hero["mana"]\n', "") + "    return name\n"),
             fails_at=2, message_contains="keep its mana too"),
        dict(why="return inside the loop",
             code=_low(LOW_START + LOW_LOOP + "        return name\n"), fails_at=1,
             message_contains="after the loop, not inside it"),
        dict(why="no comparison: the last hero kept",
             code=_low('    name = ""\n    for hero in heroes:\n        name = hero["name"]\n    return name\n'),
             fails_at=1, message_contains="Compare before you keep"),
        dict(why="min(heroes) (the bottom prints: Python's TypeError)",
             code=_low('    return min(heroes)["name"]\n'), fails_at=0,
             message_contains="'<' not supported between instances of 'dict' and 'dict'"),
        dict(why="min(heroes), the prints gone", code=_low('    return min(heroes)["name"]\n', tail=""), fails_at=1,
             message_contains="not whole dictionaries"),
        dict(why="a name from the table typed", code=_low('    return "Bomb Shell"\n'), fails_at=1,
             message_contains='`"Bomb Shell"` typed in it'),
        dict(why="print instead of return", code=_low(LOW_START + LOW_LOOP + "    print(name)\n"), fails_at=1,
             message_contains="Use `return`, not `print`"),
        dict(why="the top-level roster read inside the function",
             code=_low(LOW_BODY.replace("for hero in heroes:", "for hero in roster:")), fails_at=1,
             message_contains="Use the parameter `heroes`, not `roster`"),
        dict(why="a start at heroes[1], counting from 1 (the bottom prints: Python's IndexError on a one-hero roster)",
             code=_low(LOW_BODY.replace("heroes[0]", "heroes[1]")), fails_at=0,
             message_contains="IndexError: list index out of range"),
        dict(why="a start at heroes[1], the prints gone (row 3 is a roster of one)",
             code=_low(LOW_BODY.replace("heroes[0]", "heroes[1]"), tail=""), fails_at=1,
             message_contains="positions count from 0"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops", opens="after Unit 6", ceiling="Units 1-6",
             skills="loop-list-of-dicts,find-lowest,return-value", solo="false", dictates="",
             foreign_names="jars,jar,best,least,size",
             par="very high mana; another roster; the lowest hero last; a hero with 0 mana first") + "\n"
        "T-Lo-3. The same roster as total-mana, so the student reads one table of heroes for the whole Loops set. "
        "No ties anywhere in the core (the variant's rule). Very high mana (1,200,000 and up) catches a typed start "
        "of 100, 9999 or even 1000000; a hero with 0 mana first catches 0 used as 'nothing yet'; 'another roster' (12, 7, 9, 30) "
        "catches the name kept without its mana, which passes all three visible rows. `min(heroes)` is Python's "
        "TypeError at the bottom print (the explainer's row) and Mar'tu's message without it. Show-rung copy-test: "
        "CP1's rung is now complete (the start, the loop, the `if` with both updates under it, `return name`; it "
        "used to end on an `if` with nothing under it, a crash): no crash, it is the solution; CP2's rung keeps it. "
        "No row tells `<` from `<=` here (the core has no ties), and neither changes an answer."
    ),
)


# =============================================================================================
# T-Lo-3a "Glug, With Ties": lowest_mana_name(heroes); on a tie, the alphabetically first name (advanced)
# =============================================================================================

TIE_ROSTER = [sheet("Lucky", 4), sheet("Oogrish", 9), sheet("Bomb Shell", 4), sheet("Gearshift", 15)]
TIE_HEAD = "# Trial: glug, with ties.\ndef lowest_mana_name(heroes):\n"
TIE_TAIL = (
    "\n\n" + roster_code("roster", TIE_ROSTER) + "\n"
    "# Visible tests. They should show\n"
    "# Lucky, Bomb Shell, then Bomb Shell\n"
    "# (visible test 3 is a tie).\n"
    "# (With only pass, each shows None.)\n"
    "print(lowest_mana_name(roster[:2]))\n"
    "print(lowest_mana_name(roster[1:]))\n"
    "print(lowest_mana_name(roster))\n"
)
TIE_LOOP = (
    "    for hero in heroes:\n"
    '        mana = hero["mana"]\n'
    "        if mana < low:\n"
    '            name = hero["name"]\n'
    "            low = mana\n"
    "        elif mana == low:\n"
    '            if hero["name"] < name:\n'
    '                name = hero["name"]\n'
)
TIE_BODY = LOW_START + TIE_LOOP + "    return name\n"
# CP lowest's Show me how rung, pasted word for word: the start, the loop with `mana = hero["mana"]` and the `if`
# (both updates under it), then `return name`. No tie rule yet (a wrong_answers entry proves it runs).
TIE_RUNG1 = LOW_START + TIE_LOOP.split("        elif")[0] + "    return name\n"


def _tie(body="    pass\n", tail=TIE_TAIL):
    return TIE_HEAD + body + tail


TIE_STARTER = _tie()
TIE_SOLUTION = _tie(TIE_BODY)
TIE_FN = TIE_HEAD.split("\n", 1)[1] + TIE_BODY
TIE_TYPED = ["Bomb Shell", "Lucky", 4, 9, 15]


def _tied(h, rule):
    name, low = h[0]["name"], h[0]["mana"]
    for x in h:
        m = x["mana"]
        if rule == "first":
            better = m < low
        elif rule == "last":
            better = m <= low
        elif rule == "abc-all":
            better = m < low or x["name"] < name
        elif rule == "abc-last":
            better = m < low or (m == low and x["name"] > name)
        elif rule == "abc-first-hero":
            better = m < low or (m == low and x["name"] < h[0]["name"])
        else:
            raise ValueError(rule)
        if better:
            name, low = x["name"], m
    return name


_TIE_KEPT = ("On a tie, compare the new name with the name you are keeping, `if hero[\"name\"] < name:`, and swap only "
             "when the new one comes first in the alphabet.")
TIE_SLIPS = [
    (lambda h: _tied(h, "last"), "An equal mana should not simply take over: on a tie, keep whichever name comes "
                                 "first in the alphabet.", "_uses('op:LtE')"),
    (lambda h: _tied(h, "abc-last"), "Alphabet order means `<`: `\"Acorn\" < \"Birch\"` is `True`, so the smaller "
                                     "name comes first.", "_uses('op:Gt')"),
    (lambda h: _tied(h, "first"), "On a tie, the name that comes first in the alphabet wins: when the mana is equal, "
                                  "compare the names with `<`."),
    (lambda h: _tied(h, "last"), _TIE_KEPT),
    (lambda h: _tied(h, "abc-first-hero"), _TIE_KEPT),
    (lambda h: _tied(h, "abc-all"), "Use the alphabet only on a tie: a hero with more mana never wins, whatever "
                                    "their name."),
    (lambda h: sorted(x["name"] for x in h)[0], "Use the alphabet only on a tie: a hero with more mana never wins, "
                                                "whatever their name."),
] + LOW_SLIPS


def _tie_row(h, want, where):
    return _low_row(h, want, where, slips=TIE_SLIPS, typed=TIE_TYPED)


LOWEST_WITH_TIES = dict(
    kind="challenge",
    id="lowest-with-ties",
    title="Glug, With Ties",
    level="advanced",
    variant_of="lowest-mana-name",
    optional=True,
    minutes=10,
    support="light",
    tracer=True,
    summary="The advanced twin of Who Needs Glug First?: on a tie for the lowest mana, the name first in the alphabet "
            "wins.",
    martu=(
        "The advanced glug trial. Same function, `lowest_mana_name(heroes)`, one rule more. On a [[tie]] for the "
        "lowest mana, the name that comes first in the alphabet wins.\n"
        "Text compares in alphabet order: `\"Acorn\" < \"Birch\"` is `True`.\n"
        "```text\nlowest_mana_name(roster[:2])\n  → \"Lucky\"\nlowest_mana_name(roster[1:])\n  → \"Bomb Shell\"\n"
        "lowest_mana_name(roster)\n  → \"Bomb Shell\" (a tie)\n```\n"
        "Lucky and Bomb Shell both have 4. B comes before L, yes?"
    ),
    example='print("Acorn" < "Birch")\nprint("Oak" < "Elm")\n',
    example_output="True\nFalse",
    names=["lowest_mana_name", "heroes"],
    starter=TIE_STARTER,
    checkpoints=[
        dict(
            id="lowest",
            text="Write `lowest_mana_name(heroes)` so rows 1 and 2 of the table pass.",
            dictated=False,
            hints=[
                "Rows 1 and 2 have no tie: they are the core trial. Keep the first hero's name and mana, and swap "
                "both when a hero has less.",
                "With other names: `best = jars[0][\"name\"]` and `least = jars[0][\"size\"]` before the loop. Inside, "
                "`if size < least:` swaps both.",
                "Write `name = heroes[0][\"name\"]` and `low = heroes[0][\"mana\"]`. Then `for hero in heroes:` with "
                "`mana = hero[\"mana\"]` and `if mana < low:` inside it, and under that `name = hero[\"name\"]` and "
                "`low = mana`. Then `return name` after the loop.",
            ],
            checks=[
                _tie_row(TIE_ROSTER[:2], "Lucky", ("v", 1, "lowest_mana_name(roster[:2])", 'return "Lucky"')),
                _tie_row(TIE_ROSTER[1:], "Bomb Shell", ("v", 2, "lowest_mana_name(roster[1:])",
                                                        'return "Bomb Shell"')),
            ],
            pass_line="Oogrish: The lowest, found. Now the hard part.",
        ),
        dict(
            id="a-tie",
            text="Make row 3 pass: on a tie, the name first in the alphabet wins.",
            dictated=False,
            hints=[
                "Row 3: Lucky and Bomb Shell both have 4 mana. Lucky comes first in the roster, but B comes before L "
                "in the alphabet.",
                "Text compares in alphabet order: `\"Acorn\" < \"Birch\"` is `True`. So `if word < best:` keeps the "
                "earlier word.",
                "Write `elif mana == low:` after the `if` block, lined up with `if mana < low:`. Inside it, write `if "
                "hero[\"name\"] < name:` with `name = hero[\"name\"]` under that.",
            ],
            checks=[_tie_row(TIE_ROSTER, "Bomb Shell", ("v", 3, "lowest_mana_name(roster)", 'return "Bomb Shell"'))],
            pass_line="Bomb Shell: Alphabet. Fine. Glug first.",
        ),
        dict(
            id="hidden-tests",
            text="Pass the hidden tests. They try more ties, and the lowest hero first.",
            dictated=False,
            hints=[
                "The hidden tests try more ties. In one, the first name is already first. One is a three-way tie. In "
                "one, the lowest hero comes first, and one roster has a single hero.",
                "Use the alphabet only when the mana is equal. A hero with more mana never wins, whatever their "
                "name.",
                "Keep `if mana < low:` for a lower mana, and `elif mana == low:` for the tie, in that order.",
            ],
            checks=[
                _tie_row([sheet("Ash", 6), sheet("Moss", 6)], "Ash", ("h", "a tie, the first name already first")),
                _tie_row([sheet("Ivo", 3), sheet("Brakka", 3), sheet("Pell", 3)], "Brakka", ("h", "a three-way tie")),
                _tie_row([sheet("Pell", 2), sheet("Ash", 7), sheet("Moss", 9)], "Pell",
                         ("h", "the lowest hero first")),
                _tie_row([sheet("Moss", 1300000), sheet("Ash", 1300000), sheet("Pell", 1500000)], "Ash",
                         ("h", "a tie at very high mana")),
                _tie_row([sheet("Tinplate", 5), sheet("Glug", 8), sheet("Bree", 5), sheet("Ivo", 5)], "Bree",
                         ("h", "another roster")),
                _tie_row([sheet("Moth", 9), sheet("Ash", 3), sheet("Ivo", 3), sheet("Pell", 6)], "Ash",
                         ("h", "a middle value after the lowest")),
                _tie_row([sheet("Bree", 7)], "Bree", ("h", "a roster of one hero")),
            ],
            pass_line="Mar'tu: Ties, settled. Oogrish would make you a judge, yes?",
        ),
    ],
    solution=TIE_SOLUTION,
    partials=[_tie(LOW_BODY)],
    assemble=dict(
        lines=lines_of(TIE_FN),
        distractors=["        if mana <= low:", '            if hero["name"] > name:', "    low = 0"],
    ),
    another_way=[
        dict(angle="picture", label="Row 3, hero by hero", text=(
            "```text\nhero        mana  kept\nLucky       4     Lucky\nOogrish     9     Lucky\n"
            "Bomb Shell  4     tie: B < L\n                  Bomb Shell\nGearshift   15    Bomb Shell\n```")),
        dict(angle="step-by-step", text=(
            "1. Start from the first hero.\n2. Less mana? Keep the new name and mana.\n3. The same mana? Keep the "
            "name that comes first in the alphabet.\n4. Hand back the name after the loop.")),
        dict(angle="shorter", text=(
            "Another way: find the lowest mana first, with the core trial's loop. Then loop again and collect the "
            "names with that mana, and hand back `sorted(names)[0]`.")),
    ],
    pair_talk="Row 3 is a tie. Tell your partner why `<=` would give Bomb Shell here by luck, and which hidden tie "
              "would catch it.",
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        why=(
            "Two bars the same length on the party panel: who goes first? A rule settles it, and the rule lives in "
            "your code, not in your head."
        ),
    ),
    takeaway="A tie needs its own rule: compare the values first, and the names only when the values are equal.",
    wrong_answers=[
        dict(why="the starter (pass)", code=TIE_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="the core solution: the first of a tie kept (the partial)", code=_tie(LOW_BODY), fails_at=2,
             message_contains="first in the alphabet wins"),
        dict(why="Show me how for rows 1 and 2, pasted word for word (`mana = hero[\"mana\"]`, no tie rule yet): "
                 "no crash; row 3's tie needs the alphabet",
             code=_tie(TIE_RUNG1), fails_at=2, message_contains="first in the alphabet wins"),
        dict(why="<= : the last of a tie kept (row 3 passes by luck; a hidden tie catches it)",
             code=_tie(LOW_BODY.replace('hero["mana"] < low', 'hero["mana"] <= low')), fails_at=3,
             message_contains="should not simply take over"),
        dict(why="the alphabet used for every hero, not only ties",
             code=_tie(LOW_START + '    for hero in heroes:\n        if hero["mana"] < low or hero["name"] < name:\n'
                       '            name = hero["name"]\n            low = hero["mana"]\n    return name\n'),
             fails_at=3, message_contains="Use the alphabet only on a tie"),
        dict(why="> for the names: the alphabet backwards",
             code=_tie(TIE_BODY.replace('if hero["name"] < name:', 'if hero["name"] > name:')), fails_at=2,
             message_contains="Alphabet order means `<`"),
        dict(why="a tie taken without comparing names (elif mana == low: the later hero wins)",
             code=_tie(TIE_BODY.replace('            if hero["name"] < name:\n                name = hero["name"]\n',
                                        '            name = hero["name"]\n')), fails_at=3,
             message_contains="compare the new name with the name you are keeping"),
        dict(why="a tie compared with the first hero's name, not the name kept (another roster catches it)",
             code=_tie(TIE_BODY.replace('if hero["name"] < name:', 'if hero["name"] < heroes[0]["name"]:')),
             fails_at=3, message_contains="compare the new name with the name you are keeping"),
        dict(why="the name kept, but not its mana (a middle value after the lowest catches it)",
             code=_tie(TIE_BODY.replace("            low = mana\n", "")), fails_at=3,
             message_contains="keep its mana too"),
        dict(why="a start at heroes[1], counting from 1 (every visible roster has 2+ heroes; the roster of one catches it)",
             code=_tie(TIE_BODY.replace("heroes[0]", "heroes[1]"), tail=""), fails_at=3,
             message_contains="positions count from 0"),
        dict(why="a typed start of 9999 (a tie at very high mana catches it)",
             code=_tie('    name = ""\n    low = 9999\n' + TIE_LOOP + "    return name\n"), fails_at=3,
             message_contains="not a typed number"),
        dict(why="every name sorted, the mana ignored", code=_tie(
            '    names = []\n    for hero in heroes:\n        names.append(hero["name"])\n    return sorted(names)[0]\n'),
             fails_at=3, message_contains="Use the alphabet only on a tie"),
        dict(why="a name from the table typed", code=_tie('    return "Bomb Shell"\n'), fails_at=1,
             message_contains='`"Bomb Shell"` typed in it'),
        dict(why="the mana returned, not the name", code=_tie(LOW_START + TIE_LOOP + "    return low\n"), fails_at=1,
             message_contains="not their mana"),
        dict(why="print instead of return", code=_tie(LOW_START + TIE_LOOP + "    print(name)\n"), fails_at=1,
             message_contains="Use `return`, not `print`"),
    ],
    notes=(
        meta(starter_level="S1", path="TRIALS", set="Loops (advanced)", opens="after Unit 6", ceiling="Units 1-6",
             skills="find-lowest,tie-break,compare-text", solo="false", dictates="",
             foreign_names="jars,jar,best,least,size,Acorn,Birch,Oak,Elm",
             par="a tie, the first name already first; a three-way tie; the lowest hero first; a tie at very high "
                 "mana; another roster; a middle value after the lowest; a roster of one hero") + "\n"
        "T-Lo-3a, variant_of lowest-mana-name (same function name, a stricter spec). The roster is Lucky 4, "
        "Oogrish 9, Bomb Shell 4, Gearshift 15: rows 1-2 (slices) have no tie, so the core solution is the partial; "
        "row 3's tie has the alphabet-first name LATER in the roster, so keeping the first fails visibly, while "
        "`<=` passes it by luck and a hidden tie with the first name already first catches it. 'The lowest hero "
        "first' catches the alphabet used for every hero; the three-way tie (alphabet-first in the middle) catches "
        "both first-kept and last-kept. Comparing text with `<` is new use of a taught sign: the Learn pane and "
        "the Example show it (`\"Acorn\" < \"Birch\"`). Names are all capitalised, so case never matters here. A "
        "two-loop answer with `sorted(names)[0]` passes (the 'shorter' angle). 'A middle value after the lowest' "
        "catches the name kept without its mana (no other row has a hero between the first and the lowest), and the "
        "roster of one catches a start at `heroes[1]` (every visible roster has two or more heroes). Show-rung "
        "copy-test: CP lowest's rung (now complete: `mana = hero[\"mana\"]` and the `if` with both updates under it, "
        "then `return name`; it used to end on an empty `if`, a crash) runs: rows 1-2 pass, row 3 fails 'first in "
        "the alphabet wins' (wrong_answers). CP a-tie's rung (the `elif` and the names' `<`, which row 3 decides) "
        "is the solution; CP hidden-tests' rung keeps it. The mana's `<` in CP lowest's rung stays one sign, as "
        "the ruling lists the tie rows: a `<=` passes rows 1-3 (row 3 by luck, the pair talk's point) and the "
        "hidden test 'a tie, the first name already first' catches it."
    ),
)


ITEMS = [
    SPELL_COST, CHEAPEST_SPELL,
    AFFINITY_OF, MEETS,
    RENAME_SPELL, RENAME_SAFELY,
    TOTAL_MANA, AVERAGE_MANA,
    COUNT_BELOW, FIRST_SHRINK_OVER,
    LOWEST_MANA_NAME, LOWEST_WITH_TIES,
]


def _hidden_rows(item):
    """The "+ N hidden tests" line under each Learn-pane table (u08a's form), counted from the checks."""
    hidden = sum(1 for cp in item["checkpoints"] for name, _ in cp["checks"] if name.startswith("hidden: "))
    martu = item["martu"]
    close = martu.index("```", martu.index("```text\n") + 8)
    item["martu"] = martu[:close] + f"+ {hidden} hidden tests\n" + martu[close:]


for _item in ITEMS:
    _hidden_rows(_item)
