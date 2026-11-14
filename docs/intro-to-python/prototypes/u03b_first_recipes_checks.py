"""Unit 3 "Functions I", part b: Extra practice 3X "Recipe twins", the optional advanced challenge "Lucky's supply
run", Quick Check Recipes I (forms A and B: five code tasks each as testout items, four questions each as the form's
`<id>-questions` quiz, 3 of 4 needed to pass) and Cheatsheet 3 "Recipes".

Spec: design/curriculum.md, "## Unit 3 · Functions I", items 3, 5 and 6 (u03b): the 3X pool (6A-T1 cheer-on, 6A-T2
double-cost, 6A-T3 glug-left), Quick Check Recipes I (C1-C4 and Q1-Q4, form B with shield_total, step_east,
get_farewell, dodge_check and a d12 for roll_die) and Cheatsheet 3. Item 4, "Before the cabin door" (Route M1
only), is left out: the teacher chose Route M2 for this class (teacher-decisions.md, decision 2).
Teacher ruling on the Unit 3 reviews, applied here:
  * Every message puts the fix first, then what happened, then the evidence in brackets: "(Mar'tu's check called
    `glug_left(12, 5)`, only inside the check: it gave back -7, not 7.)". No message opens with a call the student
    never wrote; most are 35 words or fewer.
  * Quick Check messages name the slip and the evidence, never the fix, the finished line or the recipe body (no
    `def` line, no `>=`, no `randint` line), like Unit 2's QC2: recipe_check(qc=True) and returns_check(lean=True)
    rewrite the shared lesson messages through _leaned() (each rewrite must match, so a reworded lesson message
    cannot leave a fix in the Quick Check), and the Quick-Check-only checks (step, board, store, needed, BND, RND,
    the ledger rows) are lean as written. Every QC exercise is explainer="lean". A gated C5 "Trace the call" (two
    ledger rows, typed, with a paste guard) sits second in both forms, so nobody tests out without tracing; Q3
    became numbers-in-ink. Since Unit 2's play-through the site also gates on the questions: questions_to_pass=3,
    as QC2. 12 minutes. C4's pass line recaps the form's own tasks and offers the stretch.
  * cheer-on's second ingredient is `words` (6A-04's Example is `cheer(name)`); its near-miss messages name the first
    difference with Mar'tu's values only.
  * "Lucky's supply run" (advanced, optional, ~8 min): hand-worked sums turned into `item_cost(count, price)`.
  * The cheatsheet shares no name or number with the Quick Check or the lesson's ledger.
Introduces nothing new: everything here uses Units 1-2 plus u03a's `def`, `pass`, `return` and `.capitalize()`.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN `move_left()`
with `party.move("left")`, `present_dialogue_option()` storing what `get_dialogue_prompt_string()` hands back, and
`perform_roll(die_size)` with `return roll >= required_roll`. Campaign links are "you've seen this, now you'll get
it". 0 of 11 wrote a working function on the worksheet, so the Quick Check is framed as "this shows Mar'tu where to
start", never as a test of what they should know. Every student has their own device; pair talk is optional and
every checkpoint is solo.

Help ladder as fields (FORMAT.md, the order the site shows them), the same as Unit 2: hints[0] Where to look
(point), the middle hints Teach me (a tiny example with other names, which go in foreign_names), the last hint Show
me how: the step's own line in backticks, whose start becomes Start me off. another_way, assemble (More structure),
then Compare. Quick Check exercises are support="none", so none of this shows there.
Terminology (2.9): "recipe (function)", "ingredient (parameter)", "what you hand over (argument)", "hands back
(returns)"; boxes are still "box" in Unit 3, and the campaign-phrased steps say "variable".

Check codes (curriculum 2.5). Each part file is self-contained, so the recipe helpers live here. They CALL the
student's recipe from the check with fresh values (never the task's own), with print captured:
  recipe_check()   NAME + DEF for a recipe: it is made with `def`, has the exact name (near misses, the Example's
                   recipe, a box made with `=` instead), and its ingredients are exactly the task's, in order
                   (the right names in another order get their own message). qc=True: no message shows the `def` line.
  returns_check()  RET / PAR / PAR-CONST / RET-PARAM, plus PNM and RNM when the call stops with a NameError:
                   `print` instead of `return`, no `return` (None), a blank `return`, two fresh calls giving the
                   same answer (typed test values: 7 of 11 did this), an ingredient handed back as it came in, a
                   number handed back as text, and a near-miss ingredient (`base` for `base_armor`) or a name from
                   an example (`result`) or a typo of the recipe's own box. 12.0 for 12 passes (`price * 2.0`).
  prints_check()   PAR / PAR-CONST for a recipe that prints: the quoted ingredient name, the same line for two
                   calls, one line per call, and a near miss named by its first difference ("A space is missing right
                   after `Tester:`.", or "A comma inside `print(...)` adds a space." when the recipe's print has
                   commas). Never repeats the student's own text, only Mar'tu's values.
  more_calls_check()  one more call: a bare name with no `()`, `print(...)` around a recipe that prints (the extra
                   `None`), no calls left, too few calls, and a copy of a starter call (not values of your own).
  stores_check() / print_box_check()  STO at the top level: never called, printed without storing, the recipe
                   itself stored (no `()`), a typed or hand-worked number, the story's numbers handed over (other
                   numbers picked to make the same answer fail, A-08), then the box printed below its line.
  step_check()     CALL: the scout recorder (setup) moves exactly once, in the recipe's direction, and only when the
                   recipe is called (an unindented line is caught; the campaign's `party` / `move_<dir>` and a
                   wrong scout method get plain messages, without the finished line).
  board_check() / sto_check()  CALL + CMB + STO for store-then-pass: the board shows the helper's line once; the
                   check swaps the helper for another line and the board must follow (a typed line fails); the
                   helper's result is stored in a variable inside the recipe and that variable (or a plain copy of
                   it) is passed on; a box made outside the recipe gets its own message.
  needed_check() / bnd_fn_check()  BND inside a recipe: `needed` is read from the student's own `def`, any number
                   from 2 to 20 passes (lint e); rolls needed - 1, needed, needed + 1, 1 and 20; the check then
                   rebuilds the recipe with `needed` moved, so `return roll >= 12` (a typed number) fails. Returns
                   must be True or False: `print`, an `if` with no `else` (None) and text are caught. The if/else form
                   passes (each C3's `assemble` lines use it, and the harness runs them). The sign is never named:
                   "Exactly enough should pass. Which sign means *at least*?"
  rnd_fn_check()   RND: `random.randint` is swapped for a scripted die that records its arguments; roll_die(6) must
                   roll randint(1, 6), roll_die(20) randint(1, 20) (form B: 12 and 6), and hand the roll back.
  row_check() / paste_guard()  C5, the ledger shape (row_check ported from u03a): each row's slips get a message
                   that names the slip without the number; any `def`, call to the recipe or `print(` in the editor
                   fails, so the program cannot be pasted in and run.
  follow_check()   CMB for the supply run: the program is rerun with `item_cost` swapped for a stand-in that hands
                   back other numbers; the cost boxes and `total_cost` must follow (a typed 12 or 36 fails).
Messages use invented values only (Tester, Captain Glug, Hm. Noted.) and never repeat a student's own text (2.11):
numbers are shown, the student's words are not.

Python's messages were verified in CPython 3.13 (the site runs 3.13): `def armor_total = 13` -> "expected '('";
`armor_total(a, b) = a + b` -> "cannot assign to function call here. Maybe you meant '==' instead of '='?";
`double_cost = (price):` -> "invalid syntax"; an empty body -> "expected an indented block after function
definition"; a call with one value too few -> "missing 1 required positional argument";
`cheer_on("Captain Glug", Go now)` -> "invalid syntax. Perhaps you forgot a comma?"; `random.randint(die_size, 1)`
with the shown d20 -> "empty range in randrange(20, 2)"; `random.randint(die_size)` -> "missing 1 required
positional argument: 'b'".

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u03b
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates, filled in per exercise)
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
LESSON = "Recipes With Names"


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def check(label, *lines):
    """A check written as plain lines of code."""
    return (label, "\n".join(lines) + "\n")


def say(message):
    """A Python string literal for a student-facing message, for use inside check code."""
    return repr(message)


def _leaned(code, pairs):
    """Quick Check (a test-out, no hints): the same check with messages that name the slip and the evidence, never
    the fix (the teacher's lean ruling, as for the explainer; Unit 2's QC2 does the same). Each pair must match, so a
    reworded lesson message cannot silently leave a fix in the Quick Check."""
    for old, new in pairs:
        assert old in code, f"lean rewrite does not match: {old[:70]!r}"
        code = code.replace(old, new)
    return code


# Shared by every recipe check: call a recipe with print captured, describe calls and values, find a `def`, and
# explain an error raised inside the recipe (PNM, RNM, the recipe's own box, or Python's own words).
_FN = r'''import ast as _ast
import io as _io
import sys as _sys
import random as _random
_QUOTES = __QUOTES__
def _arg(_v):
    return '"' + _v + '"' if type(_v).__name__ == 'str' else str(_v)
def _c(_name, _args):
    return '`' + _name + '(' + ', '.join(_arg(_a) for _a in _args) + ')`'
def _list(_names):
    _q = ['`' + _n + '`' for _n in _names]
    if not _q:
        return 'nothing'
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]
def _end(_s):
    return '' if str(_s)[-1:] in '.!?' else '.'
def _numlike(_s):
    return _s.lstrip('-').replace('.', '', 1).isdigit()
def _val_text(_v):
    if _v is None:
        return '`None`'
    _k = type(_v).__name__
    if _k == 'bool':
        return '`' + str(_v) + '`'
    if _k == 'str':
        return ('the text `"' + _v + '"`') if (_numlike(_v) or _v in ('True', 'False')) else 'text in quotes'
    if _k == 'function':
        return 'the recipe `' + _v.__name__ + '` itself'
    return str(_v)
def _edits(_a, _b):
    _row = list(range(len(_b) + 1))
    for _i, _ca in enumerate(_a, 1):
        _new = [_i]
        for _j, _cb in enumerate(_b, 1):
            _new.append(min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))
        _row = _new
    return _row[-1]
def _close(_m, _w):
    # NAME: the same name except for capitals, a plural s, underscores, or 1-2 letters
    _a, _b = _m.lower(), _w.lower()
    return _a.rstrip('s') == _b.rstrip('s') or _a.replace('_', '') == _b.replace('_', '') or _edits(_a, _b) <= 2
def _near(_m, _w):
    # PNM: a piece of the name, a shared word, or 1-2 letters off
    _a, _b = _m.lower(), _w.lower()
    if len(_a) >= 3 and (_a in _b or _b in _a):
        return True
    if set(_x for _x in _a.split('_') if len(_x) >= 3) & set(_x for _x in _b.split('_') if len(_x) >= 3):
        return True
    return _edits(_a, _b) <= 2
def _tree():
    return _ast.parse(_source)
def _fdef(_name):
    _found = [_n for _n in _tree().body if type(_n).__name__ == 'FunctionDef' and _n.name == _name]
    return _found[-1] if _found else None
def _boxes_in(_fd):
    _out = []
    for _n in _ast.walk(_fd):
        _ts = _n.targets if type(_n).__name__ == 'Assign' else ([_n.target] if type(_n).__name__ == 'AugAssign' else [])
        for _t in _ts:
            if type(_t).__name__ == 'Name' and _t.id not in _out:
                _out.append(_t.id)
    return _out
def _is_call(_n, _f):
    return type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == _f
def _call(_f, _args):
    if type(_f).__name__ == 'str':
        _f = globals().get(_f)
    _keep = _sys.stdout
    _buf = _io.StringIO()
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _f(*_args)
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _keep
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err
def _ev(_name, _args, _what):
    # The evidence, always last and in brackets: Mar'tu's own call and what came of it.
    return " (Mar'tu's check called " + _c(_name, _args) + ', only inside the check: ' + _what + _end(_what) + ')'
def _ev2(_name, _a1, _a2, _what):
    return (" (Mar'tu's check called " + _c(_name, _a1) + ' and ' + _c(_name, _a2) + ', only inside the check: '
            + _what + _end(_what) + ')')
def _explain(_name, _args, _err, _params, _foreign=(), _special=None):
    _special = _special or {}
    _kind = type(_err).__name__
    _text = str(_err)
    _stop = _ev(_name, _args, 'Python stopped with ' + ('an ' if _kind[:1] in 'AEIOU' else 'a ') + _kind)
    if _kind == 'NameError':
        _miss = getattr(_err, 'name', None) or ''
        if _miss in _special:
            return _special[_miss]
        _fd = _fdef(_name)
        _mine = [_b for _b in (_boxes_in(_fd) if _fd else []) if _b not in _params]
        _src = [_f for _f in _foreign if _f == _miss]
        _src = _src or [_f for _f in _foreign if len(_f) > 3 and _edits(_miss.lower(), _f.lower()) <= 2]
        if _src:
            _head = ('`' + _miss + '` is a name from an example, not from this recipe.' if _src[0] == _miss else
                     '`' + _miss + '` looks like `' + _src[0] + '` from an example, not a name in this recipe.')
            if _mine:
                return "Use this recipe's own box, `" + _mine[0] + '`. ' + _head
            return "Use this recipe's ingredients, " + _list(_params) + '. ' + _head
        _own = [_b for _b in _mine if _close(_miss, _b)]
        if _own:
            return 'Use the box `' + _own[0] + '`, letter for letter: `' + _miss + '` is not a box in this recipe.'
        if [_p for _p in _params if _near(_miss, _p)]:
            return ("Use this recipe's ingredients, " + _list(_params) + ', letter for letter. You wrote `' + _miss
                    + '`.')
        if _params:
            return ('Use the ingredients, ' + _list(_params) + ': no box named `' + _miss + '` is made in the recipe.'
                    + _stop)
        return 'Make `' + _miss + '` on a line above, inside the recipe: no box by that name is made there.' + _stop
    return 'Mend this, then Run again: ' + _kind + ': ' + _text + _stop
'''.replace("__QUOTES__", repr(QUOTES_RULE))

# The Quick Check's _explain: what went wrong inside the recipe, never which name to write instead.
_FN_LEAN = [
    ('''return "Use this recipe's own box, `" + _mine[0] + '`. ' + _head''', "return _head"),
    ('''return "Use this recipe's ingredients, " + _list(_params) + '. ' + _head''', "return _head"),
    ('''return 'Use the box `' + _own[0] + '`, letter for letter: `' + _miss + '` is not a box in this recipe.\'''',
     '''return '`' + _miss + '` is not a box in this recipe, letter for letter.\''''),
    ('''return ("Use this recipe's ingredients, " + _list(_params) + ', letter for letter. You wrote `' + _miss
                    + '`.')''', '''return ('`' + _miss + "` is not one of this recipe's ingredients, letter for letter.")'''),
    ('''return ('Use the ingredients, ' + _list(_params) + ': no box named `' + _miss + '` is made in the recipe.'
                    + _stop)''', '''return ('No box named `' + _miss + '` is made in the recipe.' + _stop)'''),
    ('''return 'Make `' + _miss + '` on a line above, inside the recipe: no box by that name is made there.' + _stop''',
     '''return 'No box named `' + _miss + '` is made inside the recipe.' + _stop'''),
]


def _fill(template, **values):
    code = template
    for key, value in values.items():
        code = code.replace(f"__{key.upper()}__", repr(value))
    return code


_RECIPE = r"""
_name, _want, _foreign, _kept = __NAME__, __PARAMS__, __FOREIGN__, __KEPT__
_t = _tree()
_defs = [_n for _n in _t.body if type(_n).__name__ == 'FunctionDef']
_fd = [_n for _n in _defs if _n.name == _name]
_boxes = [_x.id for _n in _t.body if type(_n).__name__ == 'Assign' for _x in _n.targets if type(_x).__name__ == 'Name']
_sig = ': `def ' + _name + '(' + ', '.join(_want) + '):`'
if not _fd:
    _left = [_n.name for _n in _defs if _n.name in _foreign]
    _miss = [_n.name for _n in _defs if _n.name not in _foreign and _close(_n.name, _name)]
    assert not _miss, ('Name the recipe `' + _name + '`, letter for letter: you wrote `' + (_miss or [''])[0] + '`.')
    assert not _left, ('Name this task' + chr(39) + 's recipe `' + _name + '`: `' + (_left or [''])[0] + '` is the '
                       'Example' + chr(39) + 's recipe.')
    assert _name not in _boxes, ('Make `' + _name + '` with `def`' + _sig + '. It is a box now, made with `=`.')
    assert not _kept, 'Keep the `def` line from the starter' + _sig
    assert False, 'Make a recipe named `' + _name + '`: start a line with `def ' + _name + '(`.'
_got = [_a.arg for _a in _fd[-1].args.args]
if _got != _want:
    assert not _kept, 'Keep the `def` line from the starter' + _sig + '. Its ingredient names are part of the task.'
    assert _want or not _got, 'Keep the brackets of `' + _name + '` empty' + _sig + '. It takes no ingredients.'
    _n = len(_want)
    assert len(_got) == _n, ('Put ' + ('one ingredient' if _n == 1 else str(_n) + ' ingredients') + ' in the '
                             'brackets of `' + _name + '`: ' + _list(_want) + '.')
    assert sorted(_got) != sorted(_want), ('Write `' + _want[0] + '` first' + _sig + '. The right ingredients are in '
                                           'another order, and each call hands its values over in that order.')
    assert False, ('Name the ingredients ' + _list(_want) + ', in that order, letter for letter. You wrote '
                   + _list(_got) + '.')
assert callable(globals().get(_name)), ('Keep only the recipe: a later line put a value in `' + _name + '` with `=`, '
                                         'after `def` made it.')
"""

# A Quick Check: no message shows the `def` line or says which name to write; only the slip and the task's names.
_RECIPE_LEAN = [
    ("""_sig = ': `def ' + _name + '(' + ', '.join(_want) + '):`'""", "_sig = ''"),
    ("""('Name the recipe `' + _name + '`, letter for letter: you wrote `' + (_miss or [''])[0] + '`.')""",
     """('The recipe is named `' + (_miss or [''])[0] + '`, not `' + _name + '`, letter for letter.')"""),
    ("""('Name this task' + chr(39) + 's recipe `' + _name + '`: `' + (_left or [''])[0] + '` is the '
                       'Example' + chr(39) + 's recipe.')""",
     """('`' + (_left or [''])[0] + '` is the Example' + chr(39) + 's recipe, not this task' + chr(39) + 's.')"""),
    ("""('Make `' + _name + '` with `def`' + _sig + '. It is a box now, made with `=`.')""",
     """('`' + _name + '` is a box, made with `=`, not a recipe.')"""),
    ("""assert not _kept, 'Keep the `def` line from the starter' + _sig\n""",
     """assert not _kept, 'The starter' + chr(39) + 's `def` line is gone, or its name changed.'\n"""),
    ("""'Keep the `def` line from the starter' + _sig + '. Its ingredient names are part of the task.'""",
     """('The `def` line' + chr(39) + 's ingredients changed from the starter' + chr(39) + 's, and its ingredient '
                       'names are part of the task.')"""),
    ("""'Make a recipe named `' + _name + '`: start a line with `def ' + _name + '(`.'""",
     """'No line makes a recipe named `' + _name + '` yet.'"""),
    ("""'Keep the brackets of `' + _name + '` empty' + _sig + '. It takes no ingredients.'""",
     """'`' + _name + '` takes no ingredients, but its brackets hold some.'"""),
    ("""('Put ' + ('one ingredient' if _n == 1 else str(_n) + ' ingredients') + ' in the '
                             'brackets of `' + _name + '`: ' + _list(_want) + '.')""",
     """('The task gives `' + _name + '` ' + ('one ingredient' if _n == 1 else str(_n) + ' ingredients') + ', but '
                             'its brackets hold ' + str(len(_got)) + '.')"""),
    ("""('Write `' + _want[0] + '` first' + _sig + '. The right ingredients are in '
                                           'another order, and each call hands its values over in that order.')""",
     """('The ingredients are in another order than the task' + chr(39) + 's, and each call hands its '
                                           'values over in that order.')"""),
    ("""('Name the ingredients ' + _list(_want) + ', in that order, letter for letter. You wrote '
                   + _list(_got) + '.')""",
     """('The brackets hold ' + _list(_got) + ': not the task' + chr(39) + 's ingredient names, in that '
                   'order, letter for letter.')"""),
    ("""('Keep only the recipe: a later line put a value in `' + _name + '` with `=`, '
                                         'after `def` made it.')""",
     """('A later line put a value in `' + _name + '` with `=`, after `def` made it.')"""),
]


def recipe_check(name, params, foreign=(), kept=False, qc=False):
    """NAME + DEF for a recipe: made with `def`, the exact name, the exact ingredients in order. `kept=True` when the
    starter already has the `def` line (a changed line gets "Keep the def line from the starter"). `qc=True` in a
    Quick Check: the lean messages (_RECIPE_LEAN), and no message shows the `def` line."""
    code = _FN + _fill(_RECIPE, name=name, params=list(params), foreign=list(foreign), kept=bool(kept))
    return (f"{name} is a recipe with the right ingredients", _leaned(code, _FN_LEAN + _RECIPE_LEAN) if qc else code)


_RETURNS = r'''
_name, _params, _foreign, _special = __NAME__, __PARAMS__, __FOREIGN__, __SPECIAL__
_cases, _fix = __CASES__, __FIX__
_seen = []
for _args, _want in _cases:
    _args = tuple(_args)
    _val, _rows, _err = _call(_name, _args)
    assert _err is None, _explain(_name, _args, _err, _params, _foreign, _special)
    _seen.append((_args, _want, _val, _rows))
_fd = _fdef(_name)
_rets = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Return'] if _fd else []
for _args, _want, _val, _rows in _seen:
    if _val is None:
        _num = [_r for _r in _rows if _numlike(_r)]
        assert not _rows, ('Use `return` in place of `print`, so the call gets the answer.'
                           + _ev(_name, _args, 'it printed ' + (_num[0] if _num else 'a line')
                                 + ' but handed back `None`'))
        assert _rets, ('Hand back the answer with `return`: the recipe has no `return` line.'
                       + _ev(_name, _args, 'it handed back `None`'))
        assert not all(_r.value is None for _r in _rets), (
            'Put the answer after `return`: on its own, it hands back nothing.' + _ev(_name, _args, 'it handed back `None`'))
        assert False, _fix + _ev(_name, _args, 'it handed back `None`')
# `return "total"`: a box's name in quotes hands back the word itself (the quoted-name habit), not hard-coding.
_mine = set(_params) | set(_boxes_in(_fd) if _fd else [])
_qw = [(_args, _val) for _args, _want, _val, _rows in _seen if type(_val).__name__ == 'str' and _val in _mine
       and _val != _want]
assert not _qw, ('Take the quotes off `' + str(_qw[0][1]) + '`: with quotes, the recipe hands back the word itself. '
                 'Quotes mean these exact letters.' + _ev(_name, _qw[0][0], 'it handed back the word `'
                                                           + str(_qw[0][1]) + '`'))
(_a1, _w1, _v1, _r1), (_a2, _w2, _v2, _r2) = _seen[0], _seen[1]
assert not (_v1 == _v2 and type(_v1) == type(_v2) and _w1 != _w2), (
    'Use ' + _list(_params) + ': a recipe gets its numbers when it is called.'
    + _ev2(_name, _a1, _a2, 'both gave back ' + _val_text(_v1)))
def _num(_x):
    return type(_x).__name__ in ('int', 'float')
for _args, _want, _val, _rows in _seen:
    if type(_val).__name__ == 'str' and type(_want).__name__ != 'str':
        assert False, 'Hand back a number: no quotes, no `str()`.' + _ev(_name, _args, 'it handed back ' + _val_text(_val))
    # 12.0 for 12 is the right amount (`price * 2.0`): only the type differs, so it passes.
    if _val != _want or (type(_val) != type(_want) and not (_num(_val) and _num(_want))):
        _same = [_p for _p, _a in zip(_params, _args) if _a == _val and type(_a) == type(_val)]
        assert not _same, ('Hand back what the recipe works out, not `' + (_same or [''])[0] + '` as it came in.'
                           + _ev(_name, _args, 'it handed back ' + _val_text(_val)))
        assert False, _fix + _ev(_name, _args, 'it gave back ' + _val_text(_val) + ', not ' + _val_text(_want))
'''


# A Quick Check: the slip and the evidence, never what to write (the QC's own `fix` names the slip too).
_RETURNS_LEAN = [
    ("""('Use `return` in place of `print`, so the call gets the answer.'""",
     """('The recipe prints its answer, but hands nothing back.'"""),
    ("""('Hand back the answer with `return`: the recipe has no `return` line.'""", """('The recipe has no `return` line.'"""),
    ("""'Put the answer after `return`: on its own, it hands back nothing.'""",
     """'`return` stands on its own, so it hands back nothing.'"""),
    ("""'Use ' + _list(_params) + ': a recipe gets its numbers when it is called.'""",
     """'Two calls with different numbers gave back the same answer.'"""),
    ("""'Hand back a number: no quotes, no `str()`.'""", """'The recipe hands back text, not a number.'"""),
    ("""('Take the quotes off `' + str(_qw[0][1]) + '`: with quotes, the recipe hands back the word itself. '
                 'Quotes mean these exact letters.'""",
     """('The recipe hands back a word in quotes, not a box.'"""),
    ("""('Hand back what the recipe works out, not `' + (_same or [''])[0] + '` as it came in.'""",
     """('The recipe hands back `' + (_same or [''])[0] + '` as it came in.'"""),
]


def returns_check(label, name, params, cases, fix, foreign=(), special=None, lean=False):
    """RET / PAR / PAR-CONST / RET-PARAM (+ PNM, RNM). cases = [(args, expected), ...], fresh values only: no case may
    give the same answer as a call written in the task (lint b). `lean`: a Quick Check's messages (_RETURNS_LEAN)."""
    code = _FN + _fill(_RETURNS, name=name, params=list(params), foreign=list(foreign), special=dict(special or {}),
                       cases=[(tuple(a), w) for a, w in cases], fix=fix)
    return (label, _leaned(code, _FN_LEAN + _RETURNS_LEAN) if lean else code)


_PRINTS = r'''
_name, _params, _foreign, _special = __NAME__, __PARAMS__, __FOREIGN__, __SPECIAL__
_cases, _fix = __CASES__, __FIX__
_seen = []
for _args, _want in _cases:
    _args = tuple(_args)
    _val, _rows, _err = _call(_name, _args)
    assert _err is None, _explain(_name, _args, _err, _params, _foreign, _special)
    _seen.append((_args, _want, _val, _rows))
_fd = _fdef(_name)
_only_pass = _fd is not None and [type(_s).__name__ for _s in _fd.body] == ['Pass']
for _args, _want, _val, _rows in _seen:
    if not _rows:
        assert _val is None, ('Show the line with `print(...)` inside the recipe: this recipe shows its line.'
                              + _ev(_name, _args, 'it handed its line back, but printed nothing'))
        assert not _only_pass, 'Replace `pass` with a `print` line that uses ' + _list(_params) + '.'
        assert False, _fix + _ev(_name, _args, 'it printed nothing')
    for _p, _a in zip(_params, _args):
        assert not [_r for _r in _rows if _p in _r and _a not in _r], (
            'Take the quotes off `' + _p + '`: your recipe printed the word `' + _p + '`. ' + _QUOTES)
(_a1, _w1, _v1, _r1), (_a2, _w2, _v2, _r2) = _seen[0], _seen[1]
assert _r1 != _r2, ('Use ' + _list(_params) + ': a recipe gets its ingredients when it is called.'
                    + _ev2(_name, _a1, _a2, 'both printed the same line'))
def _sq(_s):
    return _s.lower().replace(' ', '')
def _first(_r, _w):
    _k = 0
    while _k < len(_r) and _k < len(_w) and _r[_k] == _w[_k]:
        _k += 1
    return _k
# A comma inside print(...) adds a space between the values.
_commas = _fd is not None and any(_is_call(_n, 'print') and len(_n.args) > 1 for _n in _ast.walk(_fd))
for _args, _want, _val, _rows in _seen:
    if _want in _rows:
        continue
    _should = 'the line should be `' + _want + '`'
    _near = [_r for _r in _rows if _sq(_r) == _sq(_want)]
    if _near:
        # The first difference, named with Mar'tu's values only: the student's own line is never shown.
        _r = _near[0]
        _i = _first(_r, _want)
        _at = ('right after `' + _want[:_i].strip() + '`') if _want[:_i].strip() else 'at the start'
        if _want[_i:_i + 1] == ' ' and _r[_i:_i + 1] != ' ':
            assert False, 'A space is missing ' + _at + '.' + _ev(_name, _args, _should)
        if _r[_i:_i + 1] == ' ' and _commas:
            assert False, ('A comma inside `print(...)` adds a space. Glue with `+` instead.'
                           + _ev(_name, _args, 'there was an extra space ' + _at))
        if _r[_i:_i + 1] == ' ':
            assert False, 'Take out the extra space ' + _at + '.' + _ev(_name, _args, _should)
        assert False, 'Match the capitals ' + _at + ': every letter counts.' + _ev(_name, _args, _should)
    assert len(_rows) == 1, ('Print one line, glued together with `+`.'
                             + _ev(_name, _args, 'it printed ' + str(len(_rows)) + ' lines, not one'))
    assert False, _fix + _ev(_name, _args, _should)
'''


def prints_check(label, name, params, cases, fix, foreign=(), special=None):
    """PAR / PAR-CONST for a recipe that prints. cases = [(args, expected_line), ...] with invented values."""
    code = _FN + _fill(_PRINTS, name=name, params=list(params), foreign=list(foreign), special=dict(special or {}),
                       cases=[(tuple(a), w) for a, w in cases], fix=fix)
    return (label, code)


_MORE_CALLS = r'''
_name, _need, _example, _what, _given = __NAME__, __NEED__, __EXAMPLE__, __WHAT__, __GIVEN__
_top = [_n for _n in _tree().body if type(_n).__name__ != 'FunctionDef']
_bare = [_n for _n in _top if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Name' and _n.value.id == _name]
assert not _bare, ('Add brackets with what you hand over, like `' + _example + '`. `' + _name + '` on its own does '
                   'nothing: a recipe runs only when you call it.')
_calls = [_n for _s in _top for _n in _ast.walk(_s) if _is_call(_n, _name)]
_wrapped = [_n for _s in _top for _n in _ast.walk(_s) if _is_call(_n, 'print') and [_a for _a in _n.args if _is_call(_a, _name)]]
assert not _wrapped, ('Call `' + _name + '` on its own line, with no `print(...)` around it. It prints its own line '
                      'and hands back nothing, so the extra `print` shows `None`.')
assert _calls, ('Keep the starter' + chr(39) + 's calls, and add one of your own below them, like `' + _example
                + '`. Nothing calls `' + _name + '` now, so it never runs.')
assert len(_calls) >= _need, ('Add a call of your own below the others, with ' + _what + ', like `' + _example + '`. '
                              'Keep the starter' + chr(39) + 's calls too.')
def _hand(_n):
    return [_ast.dump(_a) for _a in _n.args] + [_ast.dump(_k) for _k in _n.keywords]
_old = [_hand(_ast.parse(_g).body[0].value) for _g in _given]
assert [_n for _n in _calls if _hand(_n) not in _old], ('Make your new call your own, with ' + _what + ', like `'
                                                         + _example + '`. It hands over the same values as a call '
                                                         'above.')
'''


def more_calls_check(label, name, need, example, what, given=()):
    """One more call. `given` = the starter's calls as code: a copy of one of them is not a call of your own (any
    other values pass, lint e)."""
    code = _FN + _fill(_MORE_CALLS, name=name, need=need, example=example, what=what, given=list(given))
    return (label, code)


_STORES = r'''
_box, _fn, _args, _want, _example, _story = __BOX__, __FN__, __ARGS__, __WANT__, __EXAMPLE__, __STORY__
_top = [_n for _n in _tree().body if type(_n).__name__ != 'FunctionDef']
_any = [_n for _s in _top for _n in _ast.walk(_s) if _is_call(_n, _fn)]
_sets = [_n for _n in _top if type(_n).__name__ == 'Assign' and [getattr(_x, 'id', '') for _x in _n.targets] == [_box]]
_printed = [_n for _s in _top for _n in _ast.walk(_s) if _is_call(_n, 'print') and [_a for _a in _n.args if _is_call(_a, _fn)]]
_bare = [_n for _n in _top if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Name' and _n.value.id == _fn]
if _box not in globals():
    _made = [_x.id for _n in _top if type(_n).__name__ == 'Assign' for _x in _n.targets if type(_x).__name__ == 'Name']
    _miss = [_m for _m in _made if _close(_m, _box)]
    assert not _miss, 'Name the box `' + _box + '`, letter for letter: you wrote `' + (_miss or [''])[0] + '`.'
    assert not _bare, ('Call it with brackets, and store what it hands back: `' + _example + '`. `' + _fn + '` on its '
                       'own does nothing.')
    assert not _printed, ('Store it first: `' + _example + '`. Then print `' + _box + '`. A box keeps the answer, so '
                          'later lines can use it.')
    assert _any, ('Call `' + _fn + '`, and store what it hands back: start a line with `' + _box + ' = `. Nothing '
                  'calls it yet, so it never runs.')
    assert False, 'Store what `' + _fn + '` hands back in a box named `' + _box + '`: start a line with `' + _box + ' = `.'
_v = globals()[_box]
assert type(_v).__name__ != 'function', ('Call it: add `' + _example.split(_fn)[-1] + '` after `' + _fn + '`. `'
                                          + _box + '` holds the recipe itself, not its answer.')
assert _sets, 'Make `' + _box + '` with `=`, on its own line: `' + _example + '`.'
_last = _sets[-1].value
if not _is_call(_last, _fn):
    assert type(_last).__name__ != 'Constant', ('Let the recipe work it out: `' + _example + '`. `' + _box + '` holds '
                                                'a number you typed.')
    assert False, 'Let the recipe do it: `' + _example + '`. `' + _box + '` is worked out by hand.'
assert _v is not None, 'Hand back the answer with `return` in `' + _fn + '`: `' + _box + '` holds `None`.'
# What the call hands over, read from the code: a number, a box (its value now), or plain sums. Picking other numbers
# that happen to give the same answer (`25 * 2` "makes 50") skips the story's numbers, so it fails.
_NO = object()
def _value_of(_node):
    if [_x for _x in _ast.walk(_node) if type(_x).__name__ == 'Call']:
        return _NO
    try:
        return eval(compile(_ast.Expression(body=_node), 'check', 'eval'), dict(globals()))
    except Exception:
        return _NO
_fdn = _fdef(_fn)
_pn = [_a.arg for _a in _fdn.args.args] if _fdn else []
_handed = {}
for _i, _a in enumerate(_last.args):
    if _i < len(_pn):
        _handed[_pn[_i]] = _value_of(_a)
for _k in _last.keywords:
    if _k.arg:
        _handed[_k.arg] = _value_of(_k.value)
_got = tuple(_handed.get(_p, _NO) for _p in _pn)
if len(_got) == len(_args) and _NO not in _got and _got != tuple(_args):
    _nums = ' and '.join(str(_x) for _x in _args)
    assert _got != tuple(reversed(_args)), ('Hand over the numbers in the order of the ingredients: `' + _pn[0]
                                            + '` first. `' + _example + '`.')
    assert False, ('Hand over the story' + chr(39) + 's numbers, ' + _nums + ', and let the recipe work out the rest: `'
                   + _example + '`. (' + _story + '.)')
assert _v == _want, ('Hand over the numbers in the order of the ingredients: `' + _example + '`. `' + _box + '` holds '
                     + str(_v) + ', not ' + str(_want) + '.')
'''


def stores_check(label, box, fn, args, want, example, story):
    """STO at the top level: `box = fn(...)` holds `want`, and the call hands over the task's own `args` (as numbers,
    boxes holding them, or keyword values). `story` says where the numbers come from, e.g. "Lucky has 9 sips and
    drinks 4"."""
    code = _FN + _fill(_STORES, box=box, fn=fn, args=tuple(args), want=want, example=example, story=story)
    return (label, code)


_PRINT_BOX = r'''
import re as _re
_box, _want = __BOX__, __WANT__
_t = _tree()
_set_at = max([_n.lineno for _n in _t.body if type(_n).__name__ == 'Assign'
               and [getattr(_x, 'id', '') for _x in _n.targets] == [_box]] or [0])
_prints = [_n for _n in _t.body if type(_n).__name__ == 'Expr' and _is_call(_n.value, 'print')]
def _has(_n, _kind, _val):
    for _x in _n.value.args:
        for _a in _ast.walk(_x):
            if _kind == 'Name' and type(_a).__name__ == 'Name' and _a.id == _val:
                return True
            if _kind == 'Constant' and type(_a).__name__ == 'Constant' and _a.value == _val:
                return True
    return False
_using = [_n for _n in _prints if _has(_n, 'Name', _box)]
_words = [_n for _n in _prints if _has(_n, 'Constant', _box)]
assert _using or not _words, ('Take the quotes off `' + _box + '`: your program printed the word `' + _box + '`. '
                              + _QUOTES)
assert _using, 'Print `' + _box + '` on a line below, so Lucky can see it: `print(' + _box + ')`.'
assert max(_n.lineno for _n in _using) > _set_at, ('Print `' + _box + '` below the line that stores it. Python runs '
                                                  'from the top down.')
_pat = r'(?<![\d.])' + _re.escape(str(_want)) + r'(?![\d])'
assert [_l for _l in _lines() if _re.search(_pat, _l)], 'Print `' + _box + '` itself, so its number shows.'
'''


def print_box_check(label, box, want):
    code = _FN + _fill(_PRINT_BOX, box=box, want=want)
    return (label, code)


_DIRECTIONS = ["north", "south", "east", "west"]

_STEP = r'''
_fn, _dir, _special = __FN__, __DIR__, __SPECIAL__
assert type(globals().get('scout')).__name__ == '_Scout', ('A box of your own is named `scout`, so the scout from the '
                                                          'starter is gone.')
_main = list(scout.steps)
del scout.steps[:]
try:
    _val, _rows, _err = _call(_fn, ())
    _got = list(scout.steps)
finally:
    del scout.steps[:]
    scout.steps.extend(_main)
# A Quick Check (lean): every message names the slip and the evidence, never the finished line or the fix.
if type(_err).__name__ == 'AttributeError' and getattr(_err, 'obj', None) is scout:
    assert False, ('The scout has no `.' + str(getattr(_err, 'name', '') or '') + '`.'
                   + _ev(_fn, (), 'Python stopped with an AttributeError'))
if type(_err).__name__ == 'NameError' and (getattr(_err, 'name', '') or '') not in _special:
    _miss = getattr(_err, 'name', '') or ''
    assert not (_miss == 'party' or _miss.startswith('move_')), (
        '`' + _miss + '` is from the campaign' + chr(39) + 's cabin door, not from this program.')
assert _err is None, _explain(_fn, (), _err, [], [], _special)
_top = [_n for _n in _tree().body if type(_n).__name__ != 'FunctionDef']
_loose = [_n for _s in _top for _n in _ast.walk(_s) if type(_n).__name__ == 'Call'
          and type(_n.func).__name__ == 'Attribute' and _n.func.attr == 'step']
if not _got:
    assert not _loose, 'The scout line ran on its own, not when the recipe was called.'
    assert False, 'Nothing in `' + _fn + '` moves the scout.' + _ev(_fn, (), 'the scout did not move')
assert len(_got) == 1, 'The recipe moves the scout more than once.' + _ev(_fn, (), 'it moved ' + str(len(_got)) + ' times')
_d = _got[0]
_known = __KNOWN__
if _d != _dir:
    assert not (type(_d).__name__ == 'str' and _d.lower() == _dir), (
        'The direction has a capital letter, and every letter counts.'
        + _ev(_fn, (), 'the scout moved with a capital letter'))
    assert False, ('The scout moved another way than the recipe' + chr(39) + 's name says.'
                   + _ev(_fn, (), 'the scout moved ' + (_d if _d in _known else 'another way')))
'''


def step_check(label, fn, direction, special=None):
    """CALL: calling `fn()` moves the scout exactly once, in `direction`, and only when it is called."""
    code = _FN + _fill(_STEP, fn=fn, dir=direction, special=dict(special or {}), known=_DIRECTIONS)
    return (label, code)


_BOARD = r'''
_fn, _helper, _other = __FN__, __HELPER__, __OTHER__
assert type(globals().get('_board')).__name__ == 'list', 'A box of your own is named `_board`, so the ley board is gone.'
_main_board = list(_board)
def _board_after(_fake=None):
    _f = globals().get(_fn)
    _fg = _f.__globals__
    _old = _fg.get(_helper)
    if _fake is not None:
        _fg[_helper] = _fake
    del _board[:]
    try:
        _res = _call(_f, ())
        _got = list(_board)
    finally:
        if _fake is not None:
            _fg[_helper] = _old
        del _board[:]
        _board.extend(_main_board)
    return _got, _res[1], _res[2]
_hv, _hr, _he = _call(_helper, ())
assert _he is None, _explain(_helper, (), _he, [], [], {})
# A Quick Check (lean): every message names the slip and the evidence, never the finished lines or the fix.
assert _hv is not None, ('`' + _helper + '()` was already finished, but now it hands nothing back.'
                         + _ev(_helper, (), 'it handed back `None`'))
_got, _rows, _err = _board_after()
assert _err is None, _explain(_fn, (), _err, [], [], {})
_fd = _fdef(_fn)
_body = [type(_s).__name__ for _s in _fd.body] if _fd else []
if not _got:
    assert _body != ['Pass'], '`' + _fn + '()` still holds only `pass`.'
    assert not _rows, ('The line was printed, not shown on the ley board.'
                       + _ev(_fn, (), 'it printed its line, but the ley board stayed empty'))
    assert False, 'The ley board stayed empty.' + _ev(_fn, (), 'nothing reached the ley board')
assert len(_got) == 1, ('The board got more than one line.'
                        + _ev(_fn, (), 'it put ' + str(len(_got)) + ' lines on the ley board'))
_s = _got[0]
assert type(_s).__name__ != 'function', ('`' + _helper + '` has no `()` after it, so it is never called.'
                                         + _ev(_fn, (), 'the board got the recipe itself, not its line'))
assert _s is not None, ('What reached the board holds `None`, not a line.'
                        + _ev(_fn, (), 'the board got `None`'))
if _s != _hv:
    assert not (type(_s).__name__ == 'str' and _s in _boxes_in(_fd)), (
        'The board showed the word `' + str(_s) + '`, in quotes, not what the box `' + str(_s) + '` holds.')
    assert False, ('The board did not get the line that `' + _helper + '()` hands back.'
                   + _ev(_fn, (), 'the board showed another line, not the one `' + _helper + '()` hands back'))
_got2, _rows2, _err2 = _board_after(lambda: _other)
assert _err2 is None, _explain(_fn, (), _err2, [], [], {})
_tried = (" (Mar'tu's check made `" + _helper + "()` hand back another line, only inside the check: the board did "
          "not change.)")
# A box the recipe passes on but never makes itself was made outside it (stored once, at the top level).
_made = _boxes_in(_fd) if _fd else []
_outside = [_a.id for _n in (_ast.walk(_fd) if _fd else []) if _is_call(_n, 'show_on_ley_board')
            for _a in _n.args if type(_a).__name__ == 'Name' and _a.id not in _made]
assert _got2 == [_other] or not _outside, ('`' + _outside[0] + '` was made outside `' + _fn + '()`, so it does not '
                                           'follow `' + _helper + '()`.' + _tried)
assert _got2 == [_other], 'The board shows a line you typed, not what `' + _helper + '()` hands back.' + _tried
'''


def board_check(label, fn, helper, other="Tester says: shields up."):
    """CALL + CMB: `fn()` puts the helper's line on the ley board once, and follows when the helper changes."""
    code = _FN + _fill(_BOARD, fn=fn, helper=helper, other=other)
    return (label, code)


_STO = r'''
_fn, _helper, _show = __FN__, __HELPER__, __SHOW__
_fd = _fdef(_fn)
_stores = [_s for _s in _ast.walk(_fd) if type(_s).__name__ == 'Assign' and _is_call(_s.value, _helper)
           and len(_s.targets) == 1 and type(_s.targets[0]).__name__ == 'Name']
_names = [_s.targets[0].id for _s in _stores]
# A plain copy into another variable (`line = words`) still passes the stored line on.
_copies = [_s for _s in _ast.walk(_fd) if type(_s).__name__ == 'Assign' and len(_s.targets) == 1
           and type(_s.targets[0]).__name__ == 'Name' and type(_s.value).__name__ == 'Name']
for _round in range(len(_copies)):
    _names += [_s.targets[0].id for _s in _copies if _s.value.id in _names and _s.targets[0].id not in _names]
_passes = [_n for _n in _ast.walk(_fd) if _is_call(_n, _show)
           and [_a for _a in _n.args if type(_a).__name__ == 'Name' and _a.id in _names]]
# A Quick Check (lean): the slip, never the two finished lines.
assert _stores and _passes, ('`' + _show + '()` does not get a variable that holds what `' + _helper + '()` hands '
                             'back. The campaign checks for that stored variable.')
'''


def sto_check(label, fn, helper, show="show_on_ley_board"):
    code = _FN + _fill(_STO, fn=fn, helper=helper, show=show)
    return (label, code)


_NEEDED = r'''
_fn, _box, _lo, _hi = __FN__, __BOX__, __LO__, __HI__
_fd = _fdef(_fn)
_sets = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Assign'
         and [getattr(_x, 'id', '') for _x in _n.targets] == [_box]] if _fd else []
# A Quick Check (lean): the slip and the evidence, never the line to write.
assert _sets, ('`' + _fn + '` has no `' + _box + ' = ` line inside it, and the task asks for one.')
_v = _sets[-1].value
_neg = (type(_v).__name__ == 'UnaryOp' and type(_v.op).__name__ == 'USub' and type(_v.operand).__name__ == 'Constant'
        and type(_v.operand.value).__name__ == 'int')
assert type(_v).__name__ == 'Constant' or _neg, ('`' + _box + '` is worked out, not one typed number, so '
                                                 + "Mar'tu's check cannot change it to try other rolls.")
_n = -_v.operand.value if _neg else _v.value
assert type(_n).__name__ != 'str', '`' + _box + '` holds text, because of the quotes.'
assert type(_n).__name__ == 'int', '`' + _box + '` does not hold a whole number.'
assert _n != 0, ('`' + _box + '` still holds the starter' + chr(39) + 's `0`, and the task asks for a number from '
                 + str(_lo) + ' to ' + str(_hi) + '.')
assert _lo <= _n <= _hi, ('`' + _box + '` holds ' + str(_n) + ', but the task asks for a number from ' + str(_lo)
                          + ' to ' + str(_hi) + ': a d20 roll is 1 to 20.')
'''


def needed_check(label, fn, box="needed", lo=2, hi=20):
    """The recipe's own difficulty box: one whole number from lo to hi, typed (so the BND check can move it)."""
    code = _FN + _fill(_NEEDED, fn=fn, box=box, lo=lo, hi=hi)
    return (label, code)


_BNDF = r'''
_fn, _box, _top, _foreign, _special = __FN__, __BOX__, __TOP__, __FOREIGN__, __SPECIAL__
_fd = _fdef(_fn)
_set = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Assign'
        and [getattr(_x, 'id', '') for _x in _n.targets] == [_box]] if _fd else []
assert _set and type(_set[-1].value).__name__ == 'Constant' and type(_set[-1].value.value).__name__ == 'int', (
    'Step 1 is not done yet: `' + _box + '` holds no typed whole number inside `' + _fn + '`.')
_N = _set[-1].value.value
_rets =[_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Return']
def _with_box(_m):
    _t = _tree()
    _d = [_n for _n in _t.body if type(_n).__name__ == 'FunctionDef' and _n.name == _fn][-1]
    for _n in _ast.walk(_d):
        if type(_n).__name__ == 'Assign' and [getattr(_x, 'id', '') for _x in _n.targets] == [_box]:
            _n.value = _ast.copy_location(_ast.Constant(_m), _n.value)
    _mod = _ast.Module(body=[_d], type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _g = dict(globals())
    exec(compile(_mod, 'main.py', 'exec'), _g)
    return _g[_fn]
def _ask(_r, _f=None):
    _val, _rows, _err = _call(_f or _fn, (_r,))
    assert _err is None, _explain(_fn, (_r,), _err, ['roll'], _foreign, _special)
    # A Quick Check (lean): the messages name the slip and the evidence, never the sign or the finished line.
    if _val is None:
        assert not _rows, ('The recipe prints its answer, but hands nothing back.'
                           + _ev(_fn, (_r,), 'it printed its answer, but handed back `None`'))
        assert _rets, 'The recipe has no `return` line.' + _ev(_fn, (_r,), 'it handed back `None`')
        assert False, ('This roll gets no answer: no `return` line runs for it.'
                       + _ev(_fn, (_r,), 'no `return` ran, so it handed back `None`'))
    assert type(_val).__name__ != 'str', ('The recipe hands back text, not `True` or `False`.'
                                          + _ev(_fn, (_r,), 'it handed back ' + _val_text(_val)))
    assert type(_val).__name__ == 'bool', ('The recipe hands back something that is not `True` or `False`.'
                                           + _ev(_fn, (_r,), 'it handed back ' + _val_text(_val)
                                                 + (', which is `roll` as it came in' if _val == _r else '')))
    return _val
_E = _ask(_N)
assert _E, 'Exactly enough does not pass.' + _ev(_fn, (_N,), 'it handed back `False`, and `' + _box + '` is ' + str(_N))
_B = _ask(_N - 1)
assert not _B, ('A roll one short of `' + _box + '` passes.'
                + _ev(_fn, (_N - 1,), 'it handed back `True`, and ' + str(_N - 1) + ' is one short of `' + _box + '`'))
if _N + 1 <= _top:
    assert _ask(_N + 1), 'A roll above `' + _box + '` fails.' + _ev(_fn, (_N + 1,), 'it handed back `False`')
assert _ask(_top), 'The top roll fails.' + _ev(_fn, (_top,), 'it handed back `False`')
assert not _ask(1), 'A roll of 1 passes.' + _ev(_fn, (1,), 'it handed back `True`')
_M = _N + 3 if _N + 3 <= _top else _N - 3
_f2 = _with_box(_M)
_moved = [(_M, True), (_M - 1, False)] + ([(_M + 1, True)] if _M + 1 <= _top else [])
_ok = {}
for _r, _w in _moved:
    _ok[_r] = _ask(_r, _f2) == _w
_set = " (Mar'tu's check set `" + _box + ' = ' + str(_M) + '`, only inside the check: a roll of '
if _ok[_M] and _ok[_M - 1] and not _ok.get(_M + 1, True):
    assert False, 'A roll above `' + _box + '` fails.' + _set + str(_M + 1) + ' failed.)'
for _r, _w in _moved:
    assert _ok[_r], ('The question does not follow the box `' + _box + '`.' + _set + str(_r)
                     + (' failed.)' if _w else ' passed.)'))
'''


def bnd_fn_check(label, fn, box="needed", top=20, foreign=(), special=None):
    """BND inside a recipe: exactly enough passes, one below fails, a roll above passes, and the comparison follows
    the box (the check rebuilds the recipe with the box moved)."""
    code = _FN + _fill(_BNDF, fn=fn, box=box, top=top, foreign=list(foreign), special=dict(special or {}))
    return (label, code)


_RNDF = r'''
_fn, _cases, _special = __FN__, __CASES__, __SPECIAL__
def _die(_roll, _log):
    def _randint(a, b):
        _log.append((a, b))
        return _roll
    _randint.__name__ = 'randint'
    _randint.__qualname__ = 'randint'
    return _randint
_rfn = globals().get(_fn)
_fg = _rfn.__globals__
_real = _random.randint
for _size, _roll in _cases:
    _log = []
    _fake = _die(_roll, _log)
    _swap = _fg.get('randint') is _real
    _random.randint = _fake
    if _swap:
        _fg['randint'] = _fake
    try:
        _val, _rows, _err = _call(_rfn, (_size,))
    finally:
        _random.randint = _real
        if _swap:
            _fg['randint'] = _real
    assert _err is None, _explain(_fn, (_size,), _err, ['die_size'], [], _special)
    # A Quick Check (lean): the slip and the evidence, never the `randint` line or the fix.
    _fix = 'The recipe does not roll.'
    if not _log:
        assert _val != _size, (_fix + _ev(_fn, (_size,), 'it handed back ' + str(_size) + ', which is `die_size` as it '
                                          'came in'))
        assert _val is not None, _fix + _ev(_fn, (_size,), 'it handed back `None` without rolling')
        assert False, _fix + _ev(_fn, (_size,), 'it handed back ' + _val_text(_val) + ' without rolling')
    _a, _b = _log[0]
    _rolled = 'it rolled `random.randint(' + str(_a) + ', ' + str(_b) + ')`'
    assert _a <= _b, 'The numbers in the roll are in the wrong order.' + _ev(_fn, (_size,), _rolled)
    assert _a <= 1, 'The roll misses the lowest face.' + _ev(_fn, (_size,), _rolled + ', which never gives 1')
    assert _a >= 1, ('The roll can give a face the die does not have.'
                     + _ev(_fn, (_size,), _rolled + ', which can give ' + str(_a)))
    assert _b != _size - 1, ('The roll misses the top face.'
                             + _ev(_fn, (_size,), _rolled + ', which never gives ' + str(_size)))
    assert _b != _size + 1, ('The roll can go past the top face.'
                             + _ev(_fn, (_size,), _rolled + ', which can give ' + str(_b)))
    assert _b == _size, 'The top face does not follow `die_size`.' + _ev(_fn, (_size,), _rolled)
    if _val != _roll:
        assert not (_val is None and _rows), ('The recipe prints its roll, but hands nothing back.'
                                              + _ev(_fn, (_size,), 'it printed its roll, but handed back `None`'))
        assert _val is not None, 'The roll is not handed back.' + _ev(_fn, (_size,), 'it rolled, but handed back `None`')
        assert False, ('The recipe hands back something other than the roll.'
                       + _ev(_fn, (_size,), 'it rolled, but handed back ' + _val_text(_val) + ', not the roll'))
'''


def rnd_fn_check(label, fn, cases, special=None):
    """RND: `fn(size)` rolls random.randint(1, size) and hands the roll back. cases = [(size, scripted_roll), ...]."""
    code = _FN + _fill(_RNDF, fn=fn, cases=[tuple(c) for c in cases], special=dict(special or {}))
    return (label, code)


# Setup recorders (hidden code, run before the student's code): the scout and the ley board.
SCOUT_SETUP = (
    "class _Scout:\n"
    "    def __init__(self):\n"
    "        self.steps = []\n"
    "\n"
    "    def step(self, direction):\n"
    "        self.steps.append(direction)\n"
    "        print(\"The scout steps \" + str(direction) + \".\")\n"
    "\n"
    "\n"
    "scout = _Scout()\n"
    "_board = []\n"
    "\n"
    "\n"
    "def show_on_ley_board(text):\n"
    "    _board.append(text)\n"
    "    print(\"[Ley board] \" + str(text))\n"
)


# =============================================================================================
# UNIT (copied verbatim from u03a: every Unit 3 part file gives the same dict)
# =============================================================================================

UNIT = dict(
    id="first-recipes",
    order=3,
    title="Functions I",
    subtitle="First Recipes",
    published=True,
    martu_intro=(
        "At the Institute we called these recipes. You write the steps once and give them a name. When you need "
        "them, you call the name.\n"
        "Some recipes need ingredients. Some hand something back.\n"
        "You have met recipes already: `def move_left():` at the cabin door, `perform_roll(die_size)` at the trap "
        "door. Recipes were the hardest wall in the campaign, for everyone. Today we take that wall apart, one stone "
        "at a time, yes?"
    ),
    goals=[
        "Tell `=` (a box) from `def` (a recipe), and know that making a recipe does not run it",
        "Call a recipe with `()`, and replace `pass` with a real step, indented under the `def` line",
        "Give a recipe ingredients (parameters), and use their names inside it so every call works",
        "Hand a value back with `return`, catch it in a box, and know why a recipe with no `return` gives `None`",
        "Trace a call: what goes in, what each box holds, and what comes back",
        "Store what one recipe hands back, then pass it on to another, like the dialogue prompt in Module 1",
        "Hand back a comparison with `return roll >= needed`, and roll with `random.randint(1, die_size)`",
    ],
    campaign_links=["leylines-awaken", "friends-in-low-places"],
)

# No new terms here: u03b introduces nothing. Units 1-2 define box, indent, randint, .lower() and the rest; u03a
# defines the recipe terms. This file links to u01b's [[box]] and to u03a's [[ingredients]], [[hands back]], [[None]].
GLOSSARY = []


# =============================================================================================
# Extra practice 3X "Recipe twins" (pool, 9 min): 6A-T1 cheer-on, 6A-T2 double-cost, 6A-T3 glug-left
# =============================================================================================

# ---- 6A-T1 cheer-on: a recipe with two ingredients that prints (PAR) ----

def _cheer(body="    pass", extra=""):
    return (
        "def cheer_on(hero_name, words):\n"
        "    # print the hero, then \": \", then the words\n"
        f"{body}\n"
        "\n"
        "\n"
        "# should show: Lucky: Fine. I'm in.\n"
        "cheer_on(\"Lucky\", \"Fine. I'm in.\")\n"
        "# should show: Oogrish: Steady, now.\n"
        "cheer_on(\"Oogrish\", \"Steady, now.\")\n"
        + extra
    )


CHEER_BODY = "    print(hero_name + \": \" + words)"
CHEER_OWN = "cheer_on(\"Gearshift\", \"On it.\")\n"
CHEER_STARTER = _cheer()
CHEER_DONE = _cheer(CHEER_BODY)
CHEER_SOLUTION = _cheer(CHEER_BODY, CHEER_OWN)
CHEER_FOREIGN = ["label", "item", "owner", "warn", "name", "hero"]
CHEER_PARAMS = ["hero_name", "words"]
CHEER_GIVEN = ["cheer_on(\"Lucky\", \"Fine. I'm in.\")", "cheer_on(\"Oogrish\", \"Steady, now.\")"]

CHEER_ON = dict(
    id="cheer-on",
    title="Twin: cheer them on",
    martu=(
        "A twin of `warn`: the same shape, new names. This recipe has two [[ingredients]], `hero_name` and `words`. "
        "Each call hands over two values, in that order: the first fills `hero_name`, the second fills `words`.\n"
        "Finish the recipe so every call shows its own pair. Then add a call of your own."
    ),
    example=(
        "def label(item, owner):\n"
        "    print(owner + \"'s \" + item)\n"
        "\n"
        "\n"
        "label(\"canteen\", \"Lucky\")\n"
        "label(\"medallion\", \"Oogrish\")\n"
    ),
    example_output="Lucky's canteen\nOogrish's medallion",
    names=["cheer_on", "hero_name", "words"],
    # The two values for the third call, quoted as they go in: typed after `cheer_on(` (a `#` note would go in as a
    # comment line that does nothing until its `#` comes off).
    pick='"Gearshift", "On it."',
    predict=dict(
        q="Before you finish it: in this smaller version, what does the call print?",
        code=(
            "def cheer_on(hero_name, words):\n"
            "    print(words)\n"
            "\n"
            "\n"
            "cheer_on(\"Lucky\", \"Fine. I'm in.\")\n"
        ),
        choices=["Fine. I'm in.", "Lucky", "words", "Lucky: Fine. I'm in."],
        answer=0,
        explain=(
            "The second value goes into the second ingredient, `words`. So `print(words)` shows `Fine. I'm in.` "
            "Order matters: first value, first ingredient."
        ),
    ),
    pair_talk="Tell your partner what `hero_name` holds during the second call, and how you know.",
    starter=CHEER_STARTER,
    checkpoints=[
        dict(
            id="finish-cheer-on",
            text="Finish `cheer_on` so each call shows its own hero and words, like `Lucky: Fine. I'm in.`",
            dictated=False,
            hints=[
                "Look at the `def` line: the ingredients are `hero_name` and `words`. The comment under it shows "
                "the order, with `: ` in between.",
                "Inside a recipe, an ingredient's name holds what the call handed over. The Example glues two of them: "
                "`print(owner + \"'s \" + item)`.",
                "Use the names, never one call's words. `print(\"Lucky: Fine. I'm in.\")` would show Lucky for "
                "every call.",
                "Write `print(hero_name + \": \" + words)` in place of `pass`, four spaces in.",
            ],
            checks=[
                recipe_check("cheer_on", CHEER_PARAMS, CHEER_FOREIGN, kept=True),
                prints_check(
                    "each call shows its own pair", "cheer_on", CHEER_PARAMS,
                    [(("Tester", "Onward."), "Tester: Onward."), (("Captain Glug", "Hm. Noted."), "Captain Glug: Hm. Noted.")],
                    "Print the hero, then `: `, then the words, using `hero_name` and `words`.",
                    foreign=CHEER_FOREIGN,
                ),
            ],
            pass_line="Lucky: Fine. I'm in. Oogrish: Steady, now. Two calls, two lines.",
        ),
        dict(
            id="your-own-cheer",
            text="Add a third call with a hero and words of your own.",
            dictated=False,
            hints=[
                "Copy the shape of the two calls above: the hero first, then the words. Text goes in quotes.",
                "Each call hands over two values, in order: `label(\"map\", \"Mar'tu\")` fills `item`, then `owner`.",
                "Write `cheer_on(\"Gearshift\", \"On it.\")` at the bottom, or a hero and words of your own.",
            ],
            checks=[
                more_calls_check("a third call", "cheer_on", 3, "cheer_on(\"Gearshift\", \"On it.\")",
                                 "any hero and words in quotes", given=CHEER_GIVEN),
            ],
            pass_line="Mar'tu: Three calls, one recipe. You wrote the steps once, yes?",
        ),
    ],
    solution=CHEER_SOLUTION,
    partials=[CHEER_DONE],
    assemble=dict(
        lines=[
            "def cheer_on(hero_name, words):",
            CHEER_BODY,
            "cheer_on(\"Lucky\", \"Fine. I'm in.\")",
            "cheer_on(\"Oogrish\", \"Steady, now.\")",
            "cheer_on(\"Gearshift\", \"On it.\")",
        ],
        distractors=[
            "    print(\"Lucky: Fine. I'm in.\")",
            "    print(\"hero_name: words\")",
            "    print(hero + \": \" + words)",
        ],
    ),
    another_way=[
        dict(angle="picture", label="Who fills what", text=(
            "```text\ncall 1: hero_name = \"Lucky\"\n        words = \"Fine. I'm in.\"\ncall 2: hero_name = \"Oogrish\"\n"
            "        words = \"Steady, now.\"\n```\nEach call fills both boxes fresh. The print line reads them.")),
        dict(angle="everyday", label="A fill-in card", text=(
            "The card says `___: ___`. The first blank is the hero, the second the words. Each call writes new words "
            "in the blanks. The card stays the same.")),
        dict(angle="step-by-step", text=(
            "1. Python reads the `def` and remembers it. 2. The first call puts `\"Lucky\"` in `hero_name` and "
            "`\"Fine. I'm in.\"` in `words`. 3. The print line glues them with `\": \"`. 4. The next call fills both "
            "again.")),
        dict(angle="campaign", label="You've seen this", text=(
            "`party.move(\"left\")` handed one value to a recipe the game wrote. Here you write the recipe, and the "
            "calls hand it two values.")),
    ],
    takeaway="Inside the recipe, use the ingredient names. Each call fills them fresh, in order.",
    wrong_answers=[
        dict(why="the starter (pass)", code=CHEER_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="one call's line typed in (7 of 11 typed the test values)",
             code=_cheer("    print(\"Lucky: Fine. I'm in.\")"), fails_at=1, message_contains="same line"),
        dict(why="the ingredient names in quotes", code=_cheer("    print(\"hero_name: words\")"), fails_at=1,
             message_contains="the word `hero_name`"),
        dict(why="approximate ingredient name (hero for hero_name)", code=_cheer("    print(hero + \": \" + words)"),
             fails_at=0, message_contains="'hero' is not defined"),
        dict(why="the Example's names", code=_cheer("    print(owner + \"'s \" + item)"), fails_at=0,
             message_contains="'owner' is not defined"),
        dict(why="no space after the colon (the first difference, Mar'tu's values only)",
             code=_cheer("    print(hero_name + \":\" + words)"), fails_at=1,
             message_contains="A space is missing right after `Tester:`"),
        dict(why="commas in print (a space before the colon)", code=_cheer("    print(hero_name, \":\", words)"),
             fails_at=1, message_contains="A comma inside `print(...)` adds a space"),
        dict(why="an extra space before the colon, glued with +",
             code=_cheer("    print(hero_name + \" : \" + words)"), fails_at=1,
             message_contains="Take out the extra space right after `Tester`"),
        dict(why="the order swapped", code=_cheer("    print(words + \": \" + hero_name)"), fails_at=1,
             message_contains="should be `Tester: Onward.`"),
        dict(why="two prints (two lines)", code=_cheer("    print(hero_name)\n    print(words)"), fails_at=1,
             message_contains="2 lines"),
        dict(why="return instead of print (the recipe should show its line)",
             code=_cheer("    return hero_name + \": \" + words"), fails_at=1, message_contains="printed nothing"),
        dict(why="the line not indented (empty recipe)", code=_cheer("print(hero_name + \": \" + words)"), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="the def line changed (ingredients renamed)",
             code=CHEER_SOLUTION.replace("def cheer_on(hero_name, words):", "def cheer_on(hero, line):")
             .replace("hero_name + \": \" + words", "hero + \": \" + line"),
             fails_at=1, message_contains="Keep the `def` line"),
        dict(why="no () on the third call", code=_cheer(CHEER_BODY, "cheer_on\n"), fails_at=2,
             message_contains="on its own does nothing"),
        dict(why="wrong number of arguments (one value)", code=_cheer(CHEER_BODY, "cheer_on(\"Bomb Shell\")\n"),
             fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="print around a recipe that prints (shows None)",
             code=_cheer(CHEER_BODY, "print(cheer_on(\"Bomb Shell\", \"Shield up.\"))\n"), fails_at=2,
             message_contains="`None`"),
        dict(why="the third call above the def (called before it is defined)",
             code=CHEER_OWN + CHEER_DONE, fails_at=0, message_contains="'cheer_on' is not defined"),
        dict(why="unquoted hero in the third call", code=_cheer(CHEER_BODY, "cheer_on(Gearshift, \"On it.\")\n"),
             fails_at=0, message_contains="'Gearshift' is not defined"),
        dict(why="a starter call replaced, not added (only two calls)",
             code=CHEER_DONE.replace("cheer_on(\"Oogrish\", \"Steady, now.\")", CHEER_OWN.strip()), fails_at=2,
             message_contains="Keep the starter's calls"),
        dict(why="def used to make a box", code=_cheer("    def line = hero_name + \": \" + words\n    print(line)"),
             fails_at=0, message_contains="expected '('"),
        dict(why="two unquoted words in a call with two values (the explainer's split-on-commas row)",
             code=_cheer(CHEER_BODY, "cheer_on(\"Captain Glug\", Go now)\n"), fails_at=0,
             message_contains="forgot a comma"),
        dict(why="the third call copies a starter call (no hero or cheer of your own)",
             code=_cheer(CHEER_BODY, CHEER_GIVEN[0] + "\n"), fails_at=2, message_contains="same values as a call above"),
        dict(why="defined, but the calls deleted (never called)",
             code="def cheer_on(hero_name, words):\n" + CHEER_BODY + "\n", fails_at=2, message_contains="Nothing calls"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="param-use,def-call", solo="false", dictates="",
             foreign_names=",".join(CHEER_FOREIGN), par='("Tester","Onward."),("Captain Glug","Hm. Noted.")') + "\n"
        "6A-T1 (pool twin of 6A-04 warn). CP1 PAR with two invented calls that never collide with the task's "
        "(Lucky, Oogrish); PAR-CONST catches a typed line (A-06/A-07 test values), the quoted ingredient name gets "
        "its own message (the quotes rule, word for word). The messages never echo the student's words: only "
        "Mar'tu's invented values. With the starter's two calls in place, a near-miss name (`hero`) or the "
        "Example's names crash first: the explainer's rule 2/3 (PNM/RNM) answers there. CP2 is creative (lint e): "
        "any third call with values of the student's own passes; a bare `cheer_on`, a print around the call (the "
        "None line), a replaced starter call, a copy of a starter call and deleted calls are caught. Teacher ruling "
        "on the Unit 3 reviews: the second ingredient is `words`, not `cheer` (6A-04's Example recipe is "
        "`cheer(name)`); a near miss is named by its first difference with Mar'tu's values only ('A space is "
        "missing right after `Tester:`.', and 'A comma inside `print(...)` adds a space.' when the print has "
        "commas); every message puts the fix first, the evidence last. CP2's unquoted two-word value "
        "(`cheer_on(\"Captain Glug\", Go now)`) stops with Python's 'Perhaps you forgot a comma?' (the "
        "explainer's split-on-commas row)."
    ),
)


# ---- 6A-T2 double-cost: a recipe that hands back (RET, PAR-CONST) ----

def _double(body="    pass"):
    return (
        "def double_cost(price):\n"
        "    # hand back twice the price\n"
        f"{body}\n"
        "\n"
        "\n"
        "print(double_cost(4))\n"
        "# should show: 8\n"
        "print(double_cost(15))\n"
        "# should show: 30\n"
    )


DOUBLE_STARTER = _double()
DOUBLE_SOLUTION = _double("    return price * 2")
DOUBLE_FOREIGN = ["add_tip", "coins", "paid", "result", "cheer_on", "hero_name", "words"]

DOUBLE_COST = dict(
    id="double-cost",
    title="Twin: double the cost",
    martu=(
        "This recipe [[hands back]] its answer. `price` is the ingredient: the price of one thing. The recipe hands "
        "back twice that, with `return`.\n"
        "The calls are already written. `print(double_cost(4))` shows what the call hands back. Right now it shows "
        "[[None]]: the recipe hands back nothing yet."
    ),
    example=(
        "def add_tip(coins):\n"
        "    paid = coins + 2\n"
        "    return paid\n"
        "\n"
        "\n"
        "print(add_tip(5))\n"
    ),
    example_output="7",
    names=["double_cost", "price"],
    predict=dict(
        q="Before you press Run: the recipe only says `pass`. What will the two print lines show?",
        choices=["None\nNone", "8\n30", "4\n15"],
        answer=0,
        explain=(
            "`pass` hands nothing back, so each call gives back `None`, and `print` shows it. The comments say what "
            "it *should* show once you finish it."
        ),
    ),
    pair_talk="Ask your partner: why would `return 8` be wrong, even though the first call should show 8?",
    starter=DOUBLE_STARTER,
    checkpoints=[
        dict(
            id="hand-back-double",
            text="Finish `double_cost` so it hands back twice the `price`.",
            dictated=False,
            hints=[
                "What does `price` hold in the first call? What should come back for 4? For 15?",
                "`return` hands an answer back to the call, like the Example's `return paid`. `print` only shows it.",
                "Use the ingredient, never one call's number: `return 4 * 2` hands back 8 for every call.",
                "Write `return price * 2` in place of `pass`, four spaces in.",
            ],
            checks=[
                recipe_check("double_cost", ["price"], DOUBLE_FOREIGN, kept=True),
                returns_check("double_cost hands back twice the price", "double_cost", ["price"],
                              [((6,), 12), ((21,), 42)], "Hand back twice the price: `price` times 2.",
                              foreign=DOUBLE_FOREIGN),
            ],
            pass_line="8, then 30. One recipe, any price.",
        ),
    ],
    solution=DOUBLE_SOLUTION,
    assemble=dict(
        lines=["def double_cost(price):", "    return price * 2", "print(double_cost(4))", "print(double_cost(15))"],
        distractors=["    print(price * 2)", "    return 4 * 2", "    return price"],
    ),
    another_way=[
        dict(angle="picture", label="The note handed back", text=(
            "```text\nprint(double_cost(4))\n      price = 4\n      4 * 2 = 8\n      return 8 --+\n"
            "                 |\nprint(   8   ) <-+\n```")),
        dict(angle="everyday", text=(
            "`print` says the answer out loud to the room. `return` writes it on a note and hands it to whoever "
            "called. Here the caller is `print(...)`, which shows the note.")),
        dict(angle="step-by-step", text=(
            "1. `double_cost(4)` puts 4 in `price`. 2. `price * 2` is 8. 3. `return` hands 8 back to the call. "
            "4. `print` shows 8. The next call puts 15 in `price`.")),
        dict(angle="shorter", text="`return price * 2`. Never a number from one call."),
    ],
    takeaway="`return` hands the answer back to the call. Use the ingredient, never one call's number.",
    wrong_answers=[
        dict(why="the starter (pass: None)", code=DOUBLE_STARTER, fails_at=1, message_contains="no `return`"),
        dict(why="print instead of return", code=_double("    print(price * 2)"), fails_at=1,
             message_contains="printed 12 but handed back `None`"),
        dict(why="no return (worked out, kept, never handed back)", code=_double("    doubled = price * 2"),
             fails_at=1, message_contains="no `return`"),
        dict(why="a blank return (B-02)", code=_double("    doubled = price * 2\n    return"), fails_at=1,
             message_contains="on its own"),
        dict(why="one call's answer typed (A-06 return 50 style)", code=_double("    return 8"), fails_at=1,
             message_contains="both gave back 8"),
        dict(why="one call's numbers typed (4 * 2)", code=_double("    return 4 * 2"), fails_at=1,
             message_contains="both gave back 8"),
        dict(why="unrelated literals (A-02 100 * 5)", code=_double("    return 100 * 5"), fails_at=1,
             message_contains="both gave back 500"),
        dict(why="the ingredient handed back as it came in", code=_double("    return price"), fails_at=1,
             message_contains="as it came in"),
        dict(why="plus instead of times", code=_double("    return price + 2"), fails_at=1, message_contains="not 12"),
        dict(why="handed back as text", code=_double("    return str(price * 2)"), fails_at=1,
             message_contains="no quotes"),
        dict(why="approximate ingredient name", code=_double("    return cost * 2"), fails_at=0,
             message_contains="'cost' is not defined"),
        dict(why="the Example's box name (return paid)", code=_double("    doubled = price * 2\n    return paid"),
             fails_at=0, message_contains="'paid' is not defined"),
        dict(why="def used to make a box", code=_double("    def doubled = price * 2\n    return doubled"),
             fails_at=0, message_contains="expected '('"),
        dict(why="= used to make a recipe (=, then a colon)",
             code=DOUBLE_SOLUTION.replace("def double_cost(price):", "double_cost = (price):"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="= used to make a recipe (a call on the left)",
             code="double_cost(price) = price * 2\n\n\nprint(double_cost(4))\nprint(double_cost(15))\n", fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="the def line changed (another ingredient name)",
             code=_double("    return cost * 2").replace("def double_cost(price):", "def double_cost(cost):"),
             fails_at=1, message_contains="Keep the `def` line"),
        dict(why="the recipe called with no value", code=DOUBLE_SOLUTION + "print(double_cost())\n", fails_at=0,
             message_contains="missing 1 required positional argument"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="return-value,param-use", solo="false", dictates="",
             foreign_names=",".join(DOUBLE_FOREIGN), par="(6,),(21,)") + "\n"
        "6A-T2 (pool twin of 6A-06, `double_cost(price)`). RET + PAR-CONST with fresh prices 6 and 21 (12 and 42, "
        "never 8 or 30, lint b). Catches: print instead of return (B-02 / A-07), no return and a blank return (None), "
        "a typed answer or a typed call (A-06 `return 50`, A-02 `100 * 5`), the ingredient as it came in (A-07), "
        "text. The starter's calls run first, so a NameError in the recipe crashes before the checks: the "
        "explainer's rule 2 (near-miss ingredient) or rule 3 (an example's name) answers. The predict shows `None` "
        "twice: the console's None notice on the first Run. Rung 1 (teacher ruling) names the meaning before the "
        "operation: what `price` holds, and what should come back for 4 and for 15."
    ),
)


# ---- 6A-T3 glug-left: hand back, store it, print it (RET, STO) ----

def _glug(body="    pass", tail=""):
    return (
        "def glug_left(sips_now, sips_drunk):\n"
        "    # hand back the sips left\n"
        f"{body}\n"
        "\n"
        "\n"
        "# Lucky has 9 sips. He drinks 4.\n"
        "# Store the sips left in sips_left.\n"
        "# Then print sips_left.\n"
        + tail
    )


GLUG_BODY = "    return sips_now - sips_drunk"
GLUG_TAIL = "sips_left = glug_left(9, 4)\nprint(sips_left)\n"
GLUG_STARTER = _glug()
GLUG_DONE = _glug(GLUG_BODY)
GLUG_SOLUTION = _glug(GLUG_BODY, GLUG_TAIL)
GLUG_FOREIGN = ["ward_cost", "lanterns", "cost", "tonight", "result", "double_cost", "price"]
GLUG_PARAMS = ["sips_now", "sips_drunk"]
GLUG_CALL = "sips_left = glug_left(9, 4)"

GLUG_LEFT = dict(
    id="glug-left",
    title="Twin: glug left",
    martu=(
        "Lucky's canteen of glug. It heals, and it smells terrible. This recipe takes two ingredients: the sips "
        "Lucky has now, and the sips he drinks. It hands back what is left.\n"
        "Then catch the answer: store it in a [[box]], and print the box. A box keeps the answer, so later lines can "
        "use it."
    ),
    example=(
        "def ward_cost(lanterns):\n"
        "    cost = lanterns * 4\n"
        "    return cost\n"
        "\n"
        "\n"
        "tonight = ward_cost(3)\n"
        "print(tonight)\n"
    ),
    example_output="12",
    names=["glug_left", "sips_now", "sips_drunk", "sips_left"],
    pair_talk="Point at the line where the answer lands in a box. Tell your partner what is in the box after it runs.",
    starter=GLUG_STARTER,
    checkpoints=[
        dict(
            id="hand-back-what-is-left",
            text="Finish `glug_left` so it hands back the sips left.",
            dictated=False,
            hints=[
                "Sips left is the sips Lucky has, take away the sips he drinks. Both are ingredients on the `def` "
                "line.",
                "A recipe hands back its answer with `return`, like the Example's `return cost`. Use the ingredient "
                "names, never one call's numbers.",
                "Write `return sips_now - sips_drunk` in place of `pass`, four spaces in.",
            ],
            checks=[
                recipe_check("glug_left", GLUG_PARAMS, GLUG_FOREIGN, kept=True),
                returns_check("glug_left hands back what is left", "glug_left", GLUG_PARAMS,
                              [((12, 5), 7), ((20, 1), 19)],
                              "Take `sips_drunk` away from `sips_now`: `sips_now` comes first.",
                              foreign=GLUG_FOREIGN),
            ],
        ),
        dict(
            id="store-then-print",
            text="Lucky has 9 sips and drinks 4. Store what `glug_left` hands back in `sips_left`, then print `sips_left`.",
            dictated=False,
            hints=[
                "Call the recipe with Lucky's two numbers, sips now first. Put what it hands back in `sips_left`. "
                "Then print the box.",
                "A box catches what a recipe hands back: `tonight = ward_cost(3)`, then `print(tonight)`.",
                "Write `sips_left = glug_left(9, 4)` at the bottom, then `print(sips_left)`.",
            ],
            checks=[
                stores_check("sips_left catches the answer", "sips_left", "glug_left", (9, 4), 5, GLUG_CALL,
                             "Lucky has 9 sips and drinks 4"),
                print_box_check("sips_left is printed", "sips_left", 5),
            ],
            pass_line="Lucky: Five sips left. Smells terrible. I'm keeping track.",
        ),
    ],
    solution=GLUG_SOLUTION,
    partials=[GLUG_DONE],
    assemble=dict(
        lines=["def glug_left(sips_now, sips_drunk):", GLUG_BODY, GLUG_CALL, "print(sips_left)"],
        distractors=["sips_left = glug_left", "    print(sips_now - sips_drunk)", "    return 9 - 4"],
    ),
    another_way=[
        dict(angle="picture", label="Where the answer lands", text=(
            "```text\nsips_left = glug_left(9, 4)\n            sips_now = 9\n            sips_drunk = 4\n"
            "            return 5\n     <-- 5 lands here\n```")),
        dict(angle="everyday", label="Collect the parcel", text=(
            "The recipe hands you a parcel. If you don't put it somewhere, it is gone. `sips_left = ...` puts it on "
            "the shelf, so a later line can pick it up.")),
        dict(angle="step-by-step", text=(
            "1. `glug_left(9, 4)` fills `sips_now` with 9 and `sips_drunk` with 4. 2. It hands back 5. 3. `sips_left` "
            "catches the 5. 4. `print(sips_left)` shows it.")),
        dict(angle="campaign", label="You've seen this", text=(
            "In Module 1, `present_dialogue_option()` stored what `get_dialogue_prompt_string()` handed back, then "
            "passed it on. Catching the answer in a box first is the same move.")),
    ],
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        why=(
            "You have seen this. `present_dialogue_option()` stored the result of `get_dialogue_prompt_string()` in a "
            "variable, then passed that variable on. Here you store what `glug_left` hands back, then print it."
        ),
    ),
    takeaway="Catch what a recipe hands back in a box: `sips_left = glug_left(9, 4)`. Then use the box.",
    wrong_answers=[
        dict(why="the starter (pass: None)", code=GLUG_STARTER, fails_at=1, message_contains="no `return`"),
        dict(why="the order swapped (negative)", code=_glug("    return sips_drunk - sips_now"), fails_at=1,
             message_contains="`sips_now` comes first"),
        dict(why="one call's numbers typed (A-06 test values)", code=_glug("    return 9 - 4"), fails_at=1,
             message_contains="both gave back 5"),
        dict(why="one call's answer typed", code=_glug("    return 5"), fails_at=1, message_contains="both gave back 5"),
        dict(why="print instead of return", code=_glug("    print(sips_now - sips_drunk)"), fails_at=1,
             message_contains="printed 7 but handed back `None`"),
        dict(why="approximate ingredient names (A-01 attack * bonus)", code=_glug("    return sips - drunk"),
             fails_at=1, message_contains="ingredients, `sips_now` and `sips_drunk`, letter for letter"),
        dict(why="return result after left = ... (A-01 return reslt)",
             code=_glug("    left = sips_now - sips_drunk\n    return result"), fails_at=1,
             message_contains="Use this recipe's own box, `left`"),
        dict(why="a typo of its own box", code=_glug("    left = sips_now - sips_drunk\n    return lft"), fails_at=1,
             message_contains="Use the box `left`, letter for letter"),
        dict(why="the ingredient handed back as it came in", code=_glug("    return sips_now"), fails_at=1,
             message_contains="as it came in"),
        dict(why="defined but never called", code=GLUG_DONE, fails_at=2, message_contains="Nothing calls"),
        dict(why="printed without storing (STO)", code=_glug(GLUG_BODY, "print(glug_left(9, 4))\n"), fails_at=2,
             message_contains="Store it first"),
        dict(why="the recipe stored, not called (no ())", code=_glug(GLUG_BODY, "sips_left = glug_left\nprint(sips_left)\n"),
             fails_at=2, message_contains="recipe itself"),
        dict(why="the answer typed", code=_glug(GLUG_BODY, "sips_left = 5\nprint(sips_left)\n"), fails_at=2,
             message_contains="a number you typed"),
        dict(why="worked out by hand", code=_glug(GLUG_BODY, "sips_left = 9 - 4\nprint(sips_left)\n"), fails_at=2,
             message_contains="by hand"),
        dict(why="the values handed over in the wrong order",
             code=_glug(GLUG_BODY, "sips_left = glug_left(4, 9)\nprint(sips_left)\n"), fails_at=2,
             message_contains="order of the ingredients"),
        dict(why="called but not stored (the answer is lost)",
             code=_glug(GLUG_BODY, "glug_left(9, 4)\nprint(sips_left)\n"), fails_at=0,
             message_contains="'sips_left' is not defined"),
        dict(why="wrong number of arguments", code=_glug(GLUG_BODY, "sips_left = glug_left(9)\nprint(sips_left)\n"),
             fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="called before it is defined", code=GLUG_TAIL + GLUG_DONE, fails_at=0,
             message_contains="'glug_left' is not defined"),
        dict(why="stored, never printed", code=_glug(GLUG_BODY, GLUG_CALL + "\n"), fails_at=2,
             message_contains="Print `sips_left`"),
        dict(why="the box's name printed in quotes", code=_glug(GLUG_BODY, GLUG_CALL + "\nprint(\"sips_left\")\n"),
             fails_at=2, message_contains="the word `sips_left`"),
        dict(why="def used to make a box", code=_glug(GLUG_BODY, "def sips_left = glug_left(9, 4)\nprint(sips_left)\n"),
             fails_at=0, message_contains="expected '('"),
        dict(why="a near-miss box name", code=_glug(GLUG_BODY, "sip_left = glug_left(9, 4)\nprint(sip_left)\n"),
             fails_at=2, message_contains="letter for letter"),
        dict(why="other numbers picked to make 5 (A-08: `25 * 2` makes 50)",
             code=_glug(GLUG_BODY, "sips_left = glug_left(10, 5)\nprint(sips_left)\n"), fails_at=2,
             message_contains="Hand over the story's numbers, 9 and 4"),
        dict(why="other numbers picked to make 5 (5 and 0)",
             code=_glug(GLUG_BODY, "sips_left = glug_left(5, 0)\nprint(sips_left)\n"), fails_at=2,
             message_contains="Hand over the story's numbers, 9 and 4"),
        dict(why="the answer printed, not the box", code=_glug(GLUG_BODY, GLUG_CALL + "\nprint(5)\n"), fails_at=2,
             message_contains="Print `sips_left`"),
    ],
    notes=(
        meta(starter_level="S3", path="pool", skills="return-value,store-then-pass,param-use", solo="false",
             dictates="", foreign_names=",".join(GLUG_FOREIGN), par="(12,5),(20,1)") + "\n"
        "6A-T3 (pool). No call in the starter, so the checks call the recipe themselves and the check-level PNM "
        "(`sips - drunk`, A-01) and RNM (`return result` after `left = ...`, A-01's `return reslt`) messages show. "
        "Fresh calls (12, 5) -> 7 and (20, 1) -> 19 never give 5 (lint b). CP2 is the STO move (A-03/A-04 lost the "
        "returned value): never called, printed without storing, the recipe stored with no `()`, a typed or "
        "hand-worked 5, and the values in the wrong order. The check reads what the call hands over (numbers, boxes "
        "or keywords) and wants the story's 9 and 4: other numbers picked to make 5 (A-08's `25 * 2` makes 50) "
        "fail. `result` is in foreign_names: it is 6A-06's Example name."
    ),
)

EXTRA_3X = dict(
    kind="lesson",
    id="extra-recipe-twins",
    title="Extra practice: Recipe twins",
    optional=True,
    minutes=9,
    summary="Three short recipes in the lesson's shapes: one that prints, one that hands back, and one you catch in a box.",
    notes="3X pool (6A-T1 cheer-on, 6A-T2 double-cost, 6A-T3 glug-left). Optional; every twin is goal-only (ND). "
          "Feeds twins, the spaced queue and early finishers (G1 R19).",
    exercises=[CHEER_ON, DOUBLE_COST, GLUG_LEFT],
)


# =============================================================================================
# Advanced challenge "Lucky's supply run" (optional, ~8 min): hand-worked sums turned into one recipe
# =============================================================================================

# CMB for the supply run: the check reruns the student's program with `item_cost` swapped for Mar'tu's stand-in,
# which hands back other numbers. A box made with a call follows the stand-in; a typed or hand-worked number does not.
# The stand-in (count * price + count + price) depends on both numbers, so other numbers that make the same cost
# (6 and 2 for 3 and 4, A-08) fail too, while the two numbers in either order pass.
_RERUN = r"""
import io as _io
import re as _re
_fn, _rows = __FN__, __ROWS__
def _stand_in(count, price):
    return count * price + count + price
def _rerun():
    _t = _ast.parse(_source)
    _t.body = [_n for _n in _t.body if not (type(_n).__name__ == 'FunctionDef' and _n.name == _fn)]
    _ns = {'__name__': '__main__', '__builtins__': __builtins__, _fn: _stand_in}
    _keep = _sys.stdout
    _buf = _io.StringIO()
    _sys.stdout = _buf
    try:
        exec(compile(_t, 'main.py', 'exec'), _ns)
        _err = None
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _keep
    return _ns, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err
_swap = " (Mar'tu's check swapped in another `" + _fn + "`, only inside the check: "
_ns, _out, _err = _rerun()
assert _err is None, ('Mend this, then Run again: ' + type(_err).__name__ + ': ' + str(_err) + _swap + 'Python stopped '
                      'with ' + ('an ' if type(_err).__name__[:1] in 'AEIOU' else 'a ') + type(_err).__name__ + '.)')
"""

_FOLLOW_BOXES = r"""
for _box, (_a, _b) in _rows:
    assert _box in globals(), 'Keep the box `' + _box + '`, and make it with a call to `' + _fn + '`.'
    _old, _new, _want = globals()[_box], _ns.get(_box), _stand_in(_a, _b)
    if _new == _want:
        continue
    assert type(_new).__name__ != 'function', ('Call `' + _fn + '` with brackets and two numbers.' + _swap + '`'
                                               + _box + '` held the recipe itself, not a cost.)')
    assert _new != _old, ('Make `' + _box + '` with a call to `' + _fn + '`, not a number worked out by hand.' + _swap
                          + '`' + _box + '` did not change.)')
    assert False, ('Hand `' + _fn + '` the two numbers from the old `' + _box + '` line, ' + str(_a) + ' and '
                   + str(_b) + '.' + _swap + '`' + _box + '` came out wrong.)')
"""

_FOLLOW_TOTAL = r"""
assert 'total_cost' in globals(), 'Keep the box `total_cost`, and make it add the three cost boxes.'
_want = sum(_stand_in(_a, _b) for _box, (_a, _b) in _rows)
_new = _ns.get('total_cost')
if _new != _want:
    assert _new != globals()['total_cost'], ('Make `total_cost` add the three cost boxes, not a number worked out by '
                                             'hand.' + _swap + '`total_cost` did not change.)')
    assert False, ('Make `total_cost` add all three cost boxes: ' + _list([_r[0] for _r in _rows]) + '.' + _swap
                   + '`total_cost` came out wrong.)')
_pat = r'(?<![\d.])' + str(_want) + r'(?!\d)'
assert [_l for _l in _out if _re.search(_pat, _l)], ('Print `total_cost` below the line that makes it.' + _swap
                                                    + 'the new total did not print.)')
"""

SUPPLY_ROWS = [("lantern_cost", (3, 4)), ("rope_cost", (2, 7)), ("ration_cost", (5, 2))]


def follow_check(label, part):
    """CMB for the supply run: `part` is _FOLLOW_BOXES (the three cost boxes) or _FOLLOW_TOTAL (total_cost, printed)."""
    code = _FN + _fill(_RERUN, fn="item_cost", rows=[(box, tuple(args)) for box, args in SUPPLY_ROWS]) + part
    return (label, code)


SUPPLY_HEAD = "# Lucky's supply run, worked out\n# by hand, line by line:\n"
SUPPLY_RECIPE = "def item_cost(count, price):\n    return count * price\n\n\n"
SUPPLY_OLD = "lantern_cost = 3 * 4\nrope_cost = 2 * 7\nration_cost = 5 * 2\n"
SUPPLY_CALLS = "lantern_cost = item_cost(3, 4)\nrope_cost = item_cost(2, 7)\nration_cost = item_cost(5, 2)\n"
SUPPLY_TOTAL = "total_cost = lantern_cost + rope_cost + ration_cost\n"
SUPPLY_FOREIGN = ["area", "width", "height", "rug", "mat", "floor", "result"]


def _supply(recipe="", boxes=SUPPLY_OLD, total="total_cost = 36\n", tail="print(total_cost)\n",
            head=SUPPLY_HEAD):
    return head + recipe + boxes + total + tail


SUPPLY_STARTER = _supply()
SUPPLY_SOLUTION = _supply(SUPPLY_RECIPE, SUPPLY_CALLS, SUPPLY_TOTAL,
                          head="# Lucky's supply run, worked out\n# by a recipe, line by line:\n")
assert SUPPLY_STARTER == (
    "# Lucky's supply run, worked out\n"
    "# by hand, line by line:\n"
    "lantern_cost = 3 * 4\n"
    "rope_cost = 2 * 7\n"
    "ration_cost = 5 * 2\n"
    "total_cost = 36\n"
    "print(total_cost)\n"
)

SUPPLY_RUN = dict(
    kind="challenge",
    id="supply-run",
    title="Lucky's Supply Run",
    level="advanced",
    minutes=8,
    summary="Turn Lucky's hand-worked sums into one recipe that every cost line calls.",
    martu=(
        "Lucky worked out his supply run by hand. It works, yes? But if the prices change, three lines and a typed "
        "total all need mending by hand. A recipe does the work once.\n"
        "Write `item_cost`, let each cost line call it, and let `total_cost` add the boxes. Mar'tu's check swaps in "
        "other prices, only inside the check, so your boxes must follow."
    ),
    names=["item_cost", "count", "price", "lantern_cost", "rope_cost", "ration_cost", "total_cost"],
    support="light",
    starter=SUPPLY_STARTER,
    checkpoints=[
        dict(
            id="write-item-cost",
            text="Write `item_cost(count, price)` that hands back the cost of `count` things at `price` each.",
            dictated=False,
            hints=[
                "Each old line multiplies how many by the price of one. Make the recipe at the top, under the "
                "comments, so it exists before any line calls it.",
                "The same shape with other names: `def area(width, height):` then `    return width * height`.",
                "Use the ingredients, never one line's numbers: `return 3 * 4` hands back 12 for every call.",
                "Write `def item_cost(count, price):` under the comments, with `return count * price` under it, "
                "four spaces in.",
            ],
            checks=[
                recipe_check("item_cost", ["count", "price"], SUPPLY_FOREIGN),
                returns_check("item_cost hands back count times price", "item_cost", ["count", "price"],
                              [((6, 3), 18), ((11, 2), 22)], "Hand back the cost: `count` things at `price` each.",
                              foreign=SUPPLY_FOREIGN),
            ],
            pass_line="Mar'tu: One recipe, any count, any price.",
        ),
        dict(
            id="cost-boxes-call-it",
            text="Make the three cost boxes with calls to `item_cost`.",
            dictated=False,
            hints=[
                "Each old line multiplies two numbers. Hand those same two numbers to `item_cost` instead.",
                "A box catches what a call hands back: `rug = area(2, 5)` puts 10 in `rug`.",
                "Write `lantern_cost = item_cost(3, 4)` in place of `lantern_cost = 3 * 4`. Do the same for the "
                "rope and the rations.",
            ],
            checks=[follow_check("the cost boxes follow item_cost", _FOLLOW_BOXES)],
            pass_line="Lucky: The boxes do the sums now? Fine. Less work for me.",
        ),
        dict(
            id="total-adds-the-boxes",
            text="Make `total_cost` add the three boxes, then print it.",
            dictated=False,
            hints=[
                "`total_cost = 36` was added up by hand. Add the three cost boxes instead, and keep "
                "`print(total_cost)` below it.",
                "Boxes add like numbers: `floor = rug + mat` adds what is IN `rug` and `mat`.",
                "Write `total_cost = lantern_cost + rope_cost + ration_cost` in place of `total_cost = 36`.",
            ],
            checks=[follow_check("total_cost follows the boxes", _FOLLOW_TOTAL)],
            pass_line="Mar'tu: Change a price, and every line follows. That is why we write recipes, yes?",
        ),
    ],
    solution=SUPPLY_SOLUTION,
    partials=[_supply(SUPPLY_RECIPE), _supply(SUPPLY_RECIPE, SUPPLY_CALLS)],
    assemble=dict(
        lines=["def item_cost(count, price):", "    return count * price", *SUPPLY_CALLS.splitlines(),
               SUPPLY_TOTAL.strip(), "print(total_cost)"],
        distractors=["    return 3 * 4", "total_cost = 36", "    print(count * price)"],
    ),
    another_way=[
        dict(angle="everyday", label="A price list", text=(
            "Sums scribbled on a receipt go stale when a price changes. A price list on the wall does not: change it "
            "once, and every line that reads it follows. `item_cost` is the price list.")),
        dict(angle="step-by-step", text=(
            "1. Write `item_cost(count, price)` at the top. It hands back the count times the price. 2. Swap each "
            "old sum for a call with the same two numbers. 3. Make `total_cost` add the three boxes. 4. Keep the "
            "print.")),
        dict(angle="campaign", label="You've seen this", text=(
            "`perform_roll(die_size)` did the rolling once, for every check that called it. `item_cost` does the "
            "multiplying once, for every cost line.")),
    ],
    takeaway="Work it out once, in a recipe. Every line that calls it follows when something changes.",
    wrong_answers=[
        dict(why="the starter (no recipe yet)", code=SUPPLY_STARTER, fails_at=1,
             message_contains="Make a recipe named `item_cost`"),
        dict(why="item_cost hands back a typed 3 * 4 (A-06 test values)",
             code=_supply("def item_cost(count, price):\n    return 3 * 4\n\n\n"), fails_at=1,
             message_contains="both gave back 12"),
        dict(why="print instead of return (B-02)",
             code=_supply("def item_cost(count, price):\n    print(count * price)\n\n\n"), fails_at=1,
             message_contains="printed 18 but handed back `None`"),
        dict(why="count + price (the wrong sum)",
             code=_supply("def item_cost(count, price):\n    return count + price\n\n\n"), fails_at=1,
             message_contains="gave back 9, not 18"),
        dict(why="return result after cost = ... (A-01)",
             code=_supply("def item_cost(count, price):\n    cost = count * price\n    return result\n\n\n"),
             fails_at=1, message_contains="Use this recipe's own box, `cost`"),
        dict(why="approximate ingredient name (counts for count)",
             code=_supply("def item_cost(count, price):\n    return counts * price\n\n\n"), fails_at=1,
             message_contains="Use this recipe's ingredients, `count` and `price`"),
        dict(why="the ingredients named differently",
             code=_supply("def item_cost(number, cost):\n    return number * cost\n\n\n"), fails_at=1,
             message_contains="in that order"),
        dict(why="the old lines left as they were (the recipe never called)", code=_supply(SUPPLY_RECIPE), fails_at=2,
             message_contains="`lantern_cost` did not change"),
        dict(why="other numbers that make the same cost (6 and 2 for 3 and 4, A-08)",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS.replace("item_cost(3, 4)", "item_cost(6, 2)")), fails_at=2,
             message_contains="from the old `lantern_cost` line, 3 and 4"),
        dict(why="one box still typed (12)",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS.replace("item_cost(3, 4)", "12")), fails_at=2,
             message_contains="not a number worked out by hand"),
        dict(why="no () on a call (the box holds the recipe)",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS.replace("item_cost(3, 4)", "item_cost")), fails_at=2,
             message_contains="held the recipe itself"),
        dict(why="the total typed (36)", code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS), fails_at=3,
             message_contains="`total_cost` did not change"),
        dict(why="the total worked out by hand (12 + 14 + 10)",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS, "total_cost = 12 + 14 + 10\n"), fails_at=3,
             message_contains="`total_cost` did not change"),
        dict(why="one box left out of the total",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS, "total_cost = lantern_cost + rope_cost\n"), fails_at=3,
             message_contains="all three cost boxes"),
        dict(why="the total made, then the answer printed (print(36))",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS, SUPPLY_TOTAL, "print(36)\n"), fails_at=3,
             message_contains="Print `total_cost`"),
        dict(why="called before it is defined (the def below the calls)",
             code=_supply("", SUPPLY_CALLS, SUPPLY_TOTAL, "print(total_cost)\n\n\n" + SUPPLY_RECIPE.strip() + "\n"),
             fails_at=0, message_contains="'item_cost' is not defined"),
        dict(why="wrong number of arguments (one value)",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS.replace("item_cost(3, 4)", "item_cost(3)"), SUPPLY_TOTAL),
             fails_at=0, message_contains="missing 1 required positional argument: 'price'"),
        dict(why="def used to make a box",
             code=_supply(SUPPLY_RECIPE, SUPPLY_CALLS.replace("lantern_cost = ", "def lantern_cost = ")),
             fails_at=0, message_contains="expected '('"),
    ],
    notes=(
        meta(starter_level="S2", path="challenge", skills="param-use,return-value,store-then-pass", solo="false",
             dictates="", foreign_names=",".join(SUPPLY_FOREIGN), par="(6,3),(11,2)") + "\n"
        "Teacher ruling on the Unit 3 reviews (RTS-9): an optional advanced challenge for the stretch group, offered "
        "by the Quick Check's last pass line. Units 1-3 ideas only (`def`, `return`, boxes, `*`, `+`, `print`). CP1 "
        "is RET + PAR-CONST with fresh values (6, 3) -> 18 and (11, 2) -> 22, never 12, 14 or 10 (lint b). CP2 and "
        "CP3 are CMB: the check reruns the program with `item_cost` swapped for a stand-in (count * price + count + "
        "price), so a typed `12`, the old `3 * 4` lines, a typed 36 and `12 + 14 + 10` all fail ('did not change'), "
        "and other numbers that make the same cost fail too (A-08). The two numbers in either order pass. Evidence "
        "in brackets names Mar'tu's swap, never the student's numbers. All steps goal-only (ND)."
    ),
)


# =============================================================================================
# Quick Check Recipes I (test-out). Forms A and B: four code tasks each, plus four questions each.
# =============================================================================================

_QC_MARTU = ""
_STUCK = f"Stuck? Skip it, or try the lesson {LESSON}. Tasks you pass here stay ticked."


def _qc_meta(skills, dictates, foreign="", form="A", level="S3"):
    return meta(starter_level=level, path="QC-R1", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# ---- C1: write a recipe from its goal (param-use, return-value, return-right-name) ----

def _qc_write(form, name, params, who, call, total, cases, ex):
    """call = the starter's own call args; cases = fresh (args, want) pairs that never give `total`.
    ex = (example_name, example_params, example_code, example_output)."""
    p1, p2 = params
    sig = f"def {name}({p1}, {p2}):"
    ex_name, ex_params, ex_code, ex_out = ex
    foreign = [ex_name, *ex_params, "result", "add", "a", "b"]
    call_line = f"print({name}({call[0]}, {call[1]}))\n"

    def program(body=None, below=False, with_call=True):
        recipe = (sig + "\n" + body + "\n\n\n") if body is not None else ""
        tail = (f"# {who}: base {call[0]}, bonus {call[1]}.\n" + call_line + f"# should show: {total}\n") if with_call else ""
        if below:
            return f"# Write {name} here.\n\n\n" + tail + "\n" + recipe
        return f"# Write {name} here.\n" + recipe + ("\n\n" if body is None else "") + tail

    good = f"    total = {p1} + {p2}\n    return total"
    starter = program()
    solution = program(good)
    short = [p.split("_")[0] for p in params]  # base, bonus: the near-miss names (A-01)
    return dict(
        id="write-a-recipe",
        title="A recipe from its goal",
        martu=_QC_MARTU + (
            f"Write a whole recipe from its goal: `{name}` takes two ingredients and hands back their total. The "
            "Example shows the shape, with its own names.\n" + _STUCK
        ),
        example=ex_code,
        example_output=ex_out,
        names=[name, p1, p2],
        support="none",
        # Teacher ruling: every Quick Check exercise is lean (the crash explainer names the slip and the line).
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id=f"write-{name.replace('_', '-')}",
                text=f"Write `{name}({p1}, {p2})`. It hands back the two added together.",
                dictated=False,
                hints=[
                    f"The `def` line names the recipe and both ingredients, then a colon. Inside, add the ingredients "
                    "and hand the answer back.",
                    "The same shape with other names: `def add(a, b):` / `    return a + b`.",
                    f"Write `{sig}`, then `    total = {p1} + {p2}` and `    return total` under it.",
                ],
                checks=[
                    recipe_check(name, params, foreign, qc=True),
                    returns_check(f"{name} hands back the total", name, params, cases,
                                  "It does not hand back the two ingredients added together.", foreign=foreign,
                                  lean=True),
                ],
                pass_line=f"Mar'tu: {who}'s total, from any two numbers. That is a recipe, yes?",
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[sig, f"    total = {p1} + {p2}", "    return total", call_line.strip()],
            distractors=["    return result", f"    return {short[0]} + {short[1]}", f"    print({p1} + {p2})"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. `def`, the name, the two ingredients in brackets, a colon. 2. Indented: add `{p1}` and `{p2}` "
                "into a box. 3. `return` that box.")),
            dict(angle="shorter", text=f"`{sig}` then `return {p1} + {p2}`, indented."),
        ],
        takeaway="A recipe uses its own ingredient names and hands back its own box.",
        wrong_answers=[
            dict(why="the starter (no recipe yet: the call crashes)", code=starter, fails_at=0,
                 message_contains=f"'{name}' is not defined"),
            dict(why="no recipe yet and the call removed (the qc message names no def line)",
                 code=program(with_call=False), fails_at=1, message_contains="No line makes a recipe named"),
            dict(why="return result (the Example's name), with the call", code=program("    total = " + f"{p1} + {p2}\n    return result"),
                 fails_at=0, message_contains="'result' is not defined"),
            dict(why="return result (the Example's name), no call: RNM",
                 code=program("    total = " + f"{p1} + {p2}\n    return result", with_call=False), fails_at=1,
                 message_contains="is a name from an example"),
            dict(why="approximate ingredient names (A-01), with the call",
                 code=program(f"    return {short[0]} + {short[1]}"), fails_at=0,
                 message_contains=f"'{short[0]}' is not defined"),
            dict(why="approximate ingredient names (A-01), no call: PNM",
                 code=program(f"    return {short[0]} + {short[1]}", with_call=False), fails_at=1,
                 message_contains="not one of this recipe's ingredients"),
            dict(why="the answer typed (A-06 return 50)", code=program(f"    return {total}"), fails_at=1,
                 message_contains=f"both gave back {total}"),
            dict(why="one call's numbers typed (A-07 10 * 5)", code=program(f"    return {call[0]} + {call[1]}"),
                 fails_at=1, message_contains=f"both gave back {total}"),
            dict(why="print instead of return (B-02)", code=program(f"    print({p1} + {p2})"), fails_at=1,
                 message_contains="but handed back `None`"),
            dict(why="no return", code=program(f"    total = {p1} + {p2}"), fails_at=1, message_contains="no `return`"),
            dict(why="the hint's names (a + b), no call: LEFT", code=program("    return a + b", with_call=False),
                 fails_at=1, message_contains="name from an example"),
            dict(why="the first ingredient handed back as it came in", code=program(f"    return {p1}"), fails_at=1,
                 message_contains="as it came in"),
            dict(why="times instead of plus", code=program(f"    return {p1} * {p2}"), fails_at=1,
                 message_contains=f"not {cases[0][1]}"),
            dict(why="the ingredients named differently (short names)",
                 code=program(f"    return {short[0]} + {short[1]}").replace(sig, f"def {name}({short[0]}, {short[1]}):"),
                 fails_at=1, message_contains="in that order"),
            dict(why="no ingredients on the def line", code=program(f"    return {total}").replace(sig, f"def {name}():"),
                 fails_at=0, message_contains="takes 0 positional arguments"),
            dict(why="def used to make a box", code=program(None) .replace(f"# Write {name} here.\n", f"# Write {name} here.\ndef {name} = {total}\n"),
                 fails_at=0, message_contains="expected '('"),
            dict(why="= used to make a recipe (a call on the left)",
                 code=f"{name}({p1}, {p2}) = {p1} + {p2}\n" + call_line, fails_at=0,
                 message_contains="cannot assign to function call"),
            dict(why="= used to make a recipe (a box)", code=f"{name} = {total}\n", fails_at=1,
                 message_contains="is a box, made with `=`"),
            dict(why="called before it is defined (the def below the call)", code=program(good, below=True), fails_at=0,
                 message_contains=f"'{name}' is not defined"),
            dict(why="the Example's recipe name", code=program(good).replace(sig, f"def {ex_name}({p1}, {p2}):"),
                 fails_at=0, message_contains=f"'{name}' is not defined"),
            dict(why="the Example's recipe name, no call",
                 code=program(good, with_call=False).replace(sig, f"def {ex_name}({p1}, {p2}):"), fails_at=1,
                 message_contains="the Example's recipe"),
            dict(why="a capital letter in the recipe's name, no call",
                 code=program(good, with_call=False).replace(sig, f"def {name.capitalize()}({p1}, {p2}):"), fails_at=1,
                 message_contains="letter for letter"),
            dict(why="the colon left off the def", code=program(good).replace(sig, sig[:-1]), fails_at=0,
                 message_contains="expected ':'"),
            dict(why="a typo of its own box", code=program(f"    total = {p1} + {p2}\n    return totl", with_call=False),
                 fails_at=1, message_contains="is not a box in this recipe, letter for letter"),
            dict(why="handed back as text", code=program(f"    return str({p1} + {p2})"), fails_at=1,
                 message_contains="hands back text, not a number"),
            dict(why="lean: the box's name in quotes (`return \"total\"`: a word, not hard-coding)",
                 code=program(f"    total = {p1} + {p2}\n    return \"total\""), fails_at=1,
                 message_contains="hands back a word in quotes, not a box"),
            dict(why="the ingredients in the other order",
                 code=program(f"    return {p1} + {p2}").replace(sig, f"def {name}({p2}, {p1}):"), fails_at=1,
                 message_contains="in another order"),
            dict(why="the Example's minus sign copied", code=program(f"    total = {p1} - {p2}\n    return total"),
                 fails_at=1, message_contains=f"not {cases[0][1]}"),
            dict(why="one ingredient used, the other call's number typed (A-06 test values)",
                 code=program(f"    return {p1} + {call[1]}"), fails_at=1, message_contains=f"not {cases[0][1]}"),
            # Lean: each Quick Check rewrite of a lesson message, proved by its own slip.
            dict(why="lean: a blank return (the slip named, never the answer to put after it)",
                 code=program(f"    total = {p1} + {p2}\n    return"), fails_at=1,
                 message_contains="`return` stands on its own, so it hands back nothing"),
            dict(why="lean: one ingredient on the def line, no call (the count named, never the names)",
                 code=program(f"    return {p1} + {p1}", with_call=False).replace(sig, f"def {name}({p1}):"),
                 fails_at=1, message_contains="2 ingredients, but its brackets hold 1"),
            dict(why="lean: a box name the recipe never makes, no call",
                 code=program("    return power", with_call=False), fails_at=1,
                 message_contains="No box named `power` is made in the recipe"),
            dict(why="lean: a later line puts a value in the recipe's name",
                 code=program(good, with_call=False) + f"{name} = {total}\n", fails_at=1,
                 message_contains="A later line put a value in"),
        ],
        notes=_qc_meta("param-use,return-value,return-right-name", "", ",".join(foreign), form, level="S1") + "\n"
        f"QC-R1 C1, form {form}. Goal only (S1: the task names the signature; the starter has a comment and the call, no def). The Example is on "
        "screen and uses `result` (the class's slip: A-01 `return reslt`, copied from the worksheet example). "
        f"Fresh calls {cases[0][0]} -> {cases[0][1]} and {cases[1][0]} -> {cases[1][1]} never give {total} (lint b). "
        "With the starter's call in place, `return result` and `base + bonus` crash first and the explainer's rules "
        "3 and 2 answer (RNM, PNM); without the call, the check's own RNM/PNM messages answer (both proven). The "
        "ingredient names are required exactly (the task names them). Teacher ruling on the Unit 3 reviews: lean "
        "messages, the slip and the evidence, never the fix. recipe_check(qc=True) never shows the `def` line "
        "('`armor_total` is a box, made with `=`, not a recipe.'; 'No line makes a recipe named ... yet.'), and "
        "returns_check(lean=True) names the slip ('It does not hand back the two ingredients added together.', 'The "
        "recipe has no `return` line.'), never the line. support='none', explainer='lean'.",
    )


# ---- C2: replace pass, then store and pass (replace-pass, def-call, store-then-pass) ----

def _qc_board(form, direction, example_dir, helper, presenter, shout, shown):
    step_fn = f"step_{direction}"

    def program(step="    pass", present="    pass", get_line="    return line", calls=True):
        return (
            f"# 1. Replace pass so the scout\n"
            f"#    steps {direction}. The scout moves\n"
            f"#    like this: scout.step(\"{example_dir}\")\n"
            f"def {step_fn}():\n"
            f"{step}\n"
            "\n"
            "\n"
            "# Already finished. Leave it be.\n"
            f"def {helper}():\n"
            f"    line = \"{shout}\"\n"
            "    line = line.lower()\n"
            "    line = line.capitalize()\n"
            f"{get_line}\n"
            "\n"
            "\n"
            f"# 2. Finish {presenter}():\n"
            "#    store the result of\n"
            f"#    {helper}() in a variable.\n"
            "#    Then pass that variable to\n"
            "#    show_on_ley_board().\n"
            f"def {presenter}():\n"
            f"{present}\n"
            + ("\n\n# Mar'tu's test calls. Leave them.\n" f"{step_fn}()\n" f"{presenter}()\n" if calls else "")
        )

    step_ok = f"    scout.step(\"{direction}\")"
    present_ok = f"    words = {helper}()\n    show_on_ley_board(words)"
    starter = program()
    solution = program(step_ok, present_ok)
    return dict(
        id="step-and-show",
        title="Fill the recipes",
        martu=_QC_MARTU + (
            "Two recipes from the campaign's shapes. First, replace `pass` so the scout steps the right way. Then "
            f"finish `{presenter}()`: store what `{helper}()` hands back, and pass it on to the ley board. Mar'tu's "
            f"check also tries another line from `{helper}()`, so pass on what it hands back.\n" + _STUCK
        ),
        names=[step_fn, presenter, helper, "show_on_ley_board"],
        setup=SCOUT_SETUP,
        support="none",
        # Teacher ruling: every Quick Check exercise is lean (the crash explainer names the slip and the line).
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id=f"replace-pass-{direction}",
                text=f"Replace `pass` in `{step_fn}` so the scout steps {direction}.",
                dictated=False,
                hints=[
                    "The comment shows how the scout moves. Which word in the recipe's name says where to go?",
                    "`pass` is a blank recipe card. Replace it with one indented line: `scout.step(\"up\")` would "
                    "step up.",
                    f"Write `scout.step(\"{direction}\")` in place of `pass`, four spaces in.",
                ],
                checks=[
                    recipe_check(step_fn, [], kept=True, qc=True),
                    step_check(f"{step_fn} steps {direction}", step_fn, direction),
                ],
            ),
            dict(
                id=f"finish-{presenter.replace('_', '-')}",
                text=f"Finish `{presenter}()`: store the result of `{helper}()` in a variable, then pass that "
                     "variable to `show_on_ley_board()`.",
                dictated=False,
                hints=[
                    f"Two lines inside `{presenter}()`: first call the helper and catch what it hands back, then "
                    "hand that box to the board.",
                    "`note = get_note()` catches what `get_note` hands back. Then `show_it(note)` passes it on.",
                    f"Write `words = {helper}()` in place of `pass`, then `show_on_ley_board(words)` under it.",
                ],
                checks=[
                    recipe_check(presenter, [], kept=True, qc=True),
                    board_check("the board shows the helper's line", presenter, helper),
                    sto_check("the line is stored in a variable", presenter, helper),
                ],
                pass_line=f"[Ley board] {shown}",
            ),
        ],
        solution=solution,
        partials=[program(step_ok)],
        assemble=dict(
            lines=[f"def {step_fn}():", step_ok, f"def {helper}():", f"    line = \"{shout}\"", "    line = line.lower()",
                   "    line = line.capitalize()", "    return line", f"def {presenter}():", f"    words = {helper}()",
                   "    show_on_ley_board(words)"],
            distractors=[f"    scout.step({direction})", f"    show_on_ley_board({helper})",
                         f"    scout.step(\"{example_dir}\")"],
        ),
        another_way=[
            dict(angle="step-by-step", text=(
                f"1. In `{step_fn}`, swap `pass` for one `scout.step(...)` line, with the direction in quotes. "
                f"2. In `{presenter}`, call `{helper}()` and store it: `words = ...`. 3. Pass `words` to the board.")),
            dict(angle="campaign", label="You've seen this", text=(
                "`move_left()` with `party.move(\"left\")` at the cabin door, and `present_dialogue_option()` "
                "storing Mar'tu's line, then passing it on. The same two moves.")),
        ],
        campaign_link=dict(
            module="leylines-awaken",
            part="program-movement",
            snippet="def move_left():\n    party.move(\"left\")\n",
            why=(
                "You have seen this. At the cabin door you replaced each `pass` so the party moved, and then stored "
                "Mar'tu's line and passed it to `print_prompt()`. Same moves, now on your own."
            ),
        ),
        takeaway="Replace `pass` with an indented line. Store what a helper hands back, then pass the variable on.",
        wrong_answers=[
            dict(why="the starter (both still pass)", code=starter, fails_at=1, message_contains="did not move"),
            dict(why="the direction unquoted", code=program(f"    scout.step({direction})", present_ok), fails_at=0,
                 message_contains=f"'{direction}' is not defined"),
            dict(why="the Example's direction copied", code=program(f"    scout.step(\"{example_dir}\")", present_ok),
                 fails_at=1, message_contains=f"the scout moved {example_dir}"),
            dict(why="a capital letter in the direction", code=program(f"    scout.step(\"{direction.capitalize()}\")", present_ok),
                 fails_at=1, message_contains="has a capital letter"),
            dict(why="the scout line not indented (pass kept above it)",
                 code=program(f"    pass\nscout.step(\"{direction}\")", present_ok), fails_at=1,
                 message_contains="ran on its own"),
            dict(why="the scout line not indented (pass removed)", code=program(f"scout.step(\"{direction}\")", present_ok),
                 fails_at=0, message_contains="expected an indented block"),
            dict(why="two steps", code=program(step_ok + "\n" + step_ok, present_ok), fails_at=1,
                 message_contains="2 times"),
            dict(why="CP1 done, present still pass", code=program(step_ok), fails_at=2, message_contains="still holds only `pass`"),
            dict(why="the line typed (CMB)", code=program(step_ok, f"    show_on_ley_board(\"{shown}\")"), fails_at=2,
                 message_contains="shows a line you typed"),
            dict(why="no () on the helper", code=program(step_ok, f"    show_on_ley_board({helper})"), fails_at=2,
                 message_contains="has no `()`"),
            dict(why="no () on the helper, stored", code=program(step_ok, f"    words = {helper}\n    show_on_ley_board(words)"),
                 fails_at=2, message_contains="has no `()`"),
            dict(why="passed straight on, not stored (STO)", code=program(step_ok, f"    show_on_ley_board({helper}())"),
                 fails_at=2, message_contains="does not get a variable"),
            dict(why="stored, then printed (not passed to the board)",
                 code=program(step_ok, f"    words = {helper}()\n    print(words)"), fails_at=2,
                 message_contains="stayed empty"),
            dict(why="stored, then handed back (not passed to the board)",
                 code=program(step_ok, f"    words = {helper}()\n    return words"), fails_at=2,
                 message_contains="nothing reached the ley board"),
            dict(why="the variable's name in quotes",
                 code=program(step_ok, f"    words = {helper}()\n    show_on_ley_board(\"words\")"), fails_at=2,
                 message_contains="the word `words`"),
            dict(why="passed a variable that was never stored", code=program(step_ok, "    show_on_ley_board(words)"),
                 fails_at=0, message_contains="'words' is not defined"),
            dict(why="def used to make a box",
                 code=program(step_ok, f"    def words = {helper}()\n    show_on_ley_board(words)"), fails_at=0,
                 message_contains="expected '('"),
            dict(why="the finished helper broken (return removed)", code=program(step_ok, present_ok, get_line=""),
                 fails_at=2, message_contains="was already finished"),
            dict(why="shown twice", code=program(step_ok, present_ok + "\n    show_on_ley_board(words)"), fails_at=2,
                 message_contains="2 lines"),
            dict(why="the test calls removed (the checks still call the recipes)", code=program(calls=False), fails_at=1,
                 message_contains="did not move"),
            dict(why="the scout's line printed, not a real step",
                 code=program(f"    print(\"The scout steps {direction}.\")", present_ok), fails_at=1,
                 message_contains="the scout did not move"),
            dict(why="the campaign's party.move (with the test calls: the run stops)",
                 code=program(f"    party.move(\"{direction}\")", present_ok), fails_at=0,
                 message_contains="'party' is not defined"),
            dict(why="the campaign's party.move, test calls removed",
                 code=program(f"    party.move(\"{direction}\")", present_ok, calls=False), fails_at=1,
                 message_contains="from the campaign's cabin door"),
            dict(why="the campaign's recipe name called (move_...), test calls removed",
                 code=program(f"    move_{direction}()", present_ok, calls=False), fails_at=1,
                 message_contains="from the campaign's cabin door"),
            dict(why="scout.move in place of scout.step, test calls removed",
                 code=program(f"    scout.move(\"{direction}\")", present_ok, calls=False), fails_at=1,
                 message_contains="The scout has no `.move`"),
            dict(why="the helper stored outside the recipe; the recipe passes that outside box",
                 code=program(step_ok, "    show_on_ley_board(words)").replace(
                     "# Mar'tu's test calls. Leave them.\n", f"# Mar'tu's test calls. Leave them.\nwords = {helper}()\n"),
                 fails_at=2, message_contains="was made outside"),
        ],
        notes=_qc_meta("replace-pass,def-call,store-then-pass", "", "note,get_note,show_it", form) + "\n"
        f"QC-R1 C2, form {form}: `{step_fn}` (CALL through the scout recorder in setup) and `{presenter}()` "
        f"(store-then-pass, Module 1's program-dialogue-prompt with `show_on_ley_board`). `{helper}()` is in the "
        "starter (already finished), so the student reads `.lower()` then `.capitalize()` again. CMB: the check "
        f"swaps `{helper}` for a recipe that hands back another line and calls `{presenter}()`: a typed line fails. "
        "STO reads the recipe: a call to the helper assigned to a variable (a plain copy into another variable "
        "still counts), and that variable passed to the board. A helper stored outside the recipe gets its own "
        "message. The starter's test calls show the result on Run; the checks call the recipes themselves (a WA "
        "proves it). The campaign's `party.move(...)` / `move_<dir>()` and a wrong scout method get their own "
        "messages when the test calls are removed (with them, the run stops first and the explainer answers). "
        "Lean messages: no message shows the finished scout line, the stored-and-passed lines or the fix; each "
        "names the slip and the evidence. support='none', explainer='lean'.",
    )


# ---- C3: a check of your own (return-comparison, boundary) ----

def _qc_check(form, fn, who, what):
    def program(needed="0", body="    return False", calls=True):
        return (
            f"def {fn}(roll):\n"
            f"    # {who} {what}.\n"
            "    # 1. Set needed to how hard this\n"
            "    #    is: a number from 2 to 20.\n"
            f"    needed = {needed}\n"
            "    # 2. Hand back whether roll\n"
            "    #    reaches needed.\n"
            f"{body}\n"
            + (f"\n\nprint({fn}(1))\nprint({fn}(20))\n" if calls else "")
        )

    pick = 12 if form == "A" else 14
    good = "    return roll >= needed"
    if_form = "    if roll >= needed:\n        return True\n    else:\n        return False"
    starter = program()
    solution = program(str(pick), good)
    special = {"required_roll": "`required_roll` is the campaign's name, not a box in this recipe."}
    return dict(
        id="a-check-of-your-own",
        title="A check of your own",
        martu=_QC_MARTU + (
            f"Your own skill check, in a recipe. Pick how hard it is. Then hand back `True` when the roll is high "
            "enough, and `False` when it is not. Exactly enough counts. Mar'tu's check tries every kind of roll.\n"
            + _STUCK
        ),
        names=[fn, "roll", "needed"],
        pick=str(pick),
        support="none",
        # Teacher ruling: every Quick Check exercise is lean (the crash explainer names the slip and the line).
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="pick-needed",
                text="Set `needed` to how hard this is: any number from 2 to 20.",
                dictated=False,
                hints=[
                    "Look at the line `needed = 0` inside the recipe. Numbers have no quotes.",
                    "A box gets a number like this: `target = 7`.",
                    "Write `needed = 12` in place of `needed = 0`, or any number from 2 to 20.",
                ],
                checks=[recipe_check(fn, ["roll"], kept=True, qc=True), needed_check("needed is a fair number", fn)],
            ),
            dict(
                id="hand-back-a-comparison",
                text=f"Make `{fn}` hand back whether `roll` reaches `needed`. Exactly enough counts.",
                dictated=False,
                hints=[
                    "A comparison is already `True` or `False`, so you can hand it back. Which sign means *at least*?",
                    "`return score >= target` hands back `True` or `False`. An `if` with `return True` and `else:` "
                    "`return False` does the same.",
                    "Write `return roll >= needed` in place of `return False`.",
                ],
                checks=[bnd_fn_check("exactly enough passes", fn, special=special)],
                pass_line=f"{who}: It opens. Mar'tu: You picked the number. The recipe did the rest, yes?",
            ),
        ],
        solution=solution,
        partials=[program(str(pick))],
        assemble=dict(
            lines=[f"def {fn}(roll):", f"    needed = {pick}", *if_form.splitlines()],
            distractors=["    return roll > needed", "    return True", "    print(roll >= needed)"],
        ),
        another_way=[
            dict(angle="picture", text="```text\n1 ... needed-1 | needed ... 20\n     False     |    True\n```"),
            dict(angle="step-by-step", text=(
                "1. `needed = ` a number from 2 to 20. 2. `roll >= needed` is `True` or `False`. 3. `return` it. "
                "The long form, `if` / `return True` / `else:` / `return False`, works too.")),
            dict(angle="campaign", label="You've seen this", text=(
                "The trap-door checks: `required_roll = 12`, then `return roll >= required_roll`. Here the box is "
                "`needed`.")),
        ],
        campaign_link=dict(
            module="friends-in-low-places",
            part="skill-checks",
            snippet="required_roll = 12\nreturn roll >= required_roll\n",
            why=(
                "You have seen this at the trap door. Each check set `required_roll`, then handed back "
                "`roll >= required_roll`: `True` from exactly enough up. Now it is your own check."
            ),
        ),
        takeaway="Hand back a comparison: `return roll >= needed`. `>=` lets exactly enough pass.",
        wrong_answers=[
            dict(why="the starter (needed still 0)", code=starter, fails_at=1, message_contains="still holds the starter's `0`"),
            dict(why="return True (always passes)", code=program(str(pick), "    return True"), fails_at=2,
                 message_contains="one short"),
            dict(why="> instead of >= (exactly enough fails)", code=program(str(pick), "    return roll > needed"),
                 fails_at=2, message_contains="Exactly enough"),
            dict(why="== (only exactly passes)", code=program(str(pick), "    return roll == needed"), fails_at=2,
                 message_contains="above"),
            dict(why="== with needed at the top face (no roll can go past it)",
                 code=program("20", "    return roll == needed"), fails_at=2, message_contains="a roll of 18 failed"),
            dict(why="print instead of return", code=program(str(pick), "    print(roll >= needed)"), fails_at=2,
                 message_contains="handed back `None`"),
            dict(why="an if with no else (None for a low roll)",
                 code=program(str(pick), "    if roll >= needed:\n        return True"), fails_at=2,
                 message_contains="gets no answer"),
            dict(why="the if form with >", code=program(str(pick), if_form.replace(">=", ">")), fails_at=2,
                 message_contains="Exactly enough"),
            dict(why="the number typed into the comparison", code=program(str(pick), f"    return roll >= {pick}"),
                 fails_at=2, message_contains="does not follow the box"),
            dict(why="the campaign's box name (required_roll)", code=program(str(pick), "    return roll >= required_roll"),
                 fails_at=0, message_contains="'required_roll' is not defined"),
            dict(why="the campaign's box name, calls removed: RNM",
                 code=program(str(pick), "    return roll >= required_roll", calls=False), fails_at=2,
                 message_contains="campaign's name"),
            dict(why="the comparison turned around", code=program(str(pick), "    return needed >= roll"), fails_at=2,
                 message_contains="one short"),
            dict(why="True in quotes", code=program(str(pick), if_form.replace("True", "\"True\"").replace("False", "\"False\"")),
                 fails_at=2, message_contains="hands back text"),
            dict(why="the roll handed back", code=program(str(pick), "    return roll"), fails_at=2,
                 message_contains="as it came in"),
            dict(why="needed bigger than a d20", code=program("25", good), fails_at=1, message_contains="from 2 to 20"),
            dict(why="needed in quotes", code=program(f"\"{pick}\"", good), fails_at=0, message_contains="not supported"),
            dict(why="needed in quotes, calls removed", code=program(f"\"{pick}\"", good, calls=False), fails_at=1,
                 message_contains="quotes"),
            dict(why="needed rolled at random", code=program("random.randint(2, 20)", good).replace("def ", "import random\n\n\ndef ", 1),
                 fails_at=1, message_contains="not one typed number"),
            dict(why="the else with a condition", code=program(str(pick), if_form.replace("else:", "else roll < needed:")),
                 fails_at=0, message_contains="expected ':'"),
            dict(why="a negative needed", code=program("-5", good), fails_at=1, message_contains="from 2 to 20"),
            dict(why="needed made outside the recipe (a box above the def)",
                 code=f"needed = {pick}\n\n\n" + program(str(pick), good).replace(f"    needed = {pick}\n", ""),
                 fails_at=1, message_contains="inside"),
            dict(why="the number worked out in the comparison", code=program(str(pick), f"    return roll >= {pick - 1} + 1"),
                 fails_at=2, message_contains="does not follow the box"),
            dict(why="the roll ingredient renamed", code=program(str(pick), "    return r >= needed").replace(
                f"def {fn}(roll):", f"def {fn}(r):"), fails_at=1, message_contains="ingredients changed from the starter"),
        ],
        notes=_qc_meta("return-comparison,boundary", "", "score,target,required_roll", form, level="S2") + "\n"
        f"QC-R1 C3, form {form}. `needed` is read from the student's own recipe (any 2-20 passes, lint e). BND calls "
        "the recipe with needed, needed - 1, needed + 1, 20 and 1, then rebuilds the recipe with `needed` moved by 3 "
        "and tries again, so a typed number fails. Returns must be True or False (print, an `if` with no `else`, "
        "text, the roll itself). The if/else form passes: the assemble lines use it and the harness runs them. "
        "`required_roll` (the campaign's name) gets its own message. Lean messages: no message names the sign "
        "or the fix (teacher ruling): 'Exactly enough does not pass.', and an `if` with no `else` gets 'This roll "
        "gets no answer: no `return` line runs for it.' support='none', explainer='lean'.",
    )


# ---- C4: a rolling recipe (randint-param) ----

def _qc_roll(form, shown_size, cases, pass_line):
    """pass_line: the Quick Check's last line, a recap of this form's own tasks plus the stretch offer."""
    def program(body="    return 1", head="import random\n\n\n"):
        return (
            head
            + "def roll_die(die_size):\n"
            "    # Hand back a random whole\n"
            "    # number from 1 to die_size.\n"
            f"{body}\n"
            "\n"
            "\n"
            f"print(roll_die({shown_size}))\n"
        )

    good = "    return random.randint(1, die_size)"
    starter = program()
    solution = program(good)
    other = [s for s, _ in cases if s != shown_size][0]
    special = {
        "randint": "`randint` is used on its own, so Python does not know it.",
        "random": "`import random` is gone from the top, so Python does not know `random`.",
    }
    return dict(
        id="roll-a-die",
        title="A rolling recipe",
        martu=_QC_MARTU + (
            "A die of any size. `die_size` says how many faces. The recipe rolls it and hands the roll back. "
            "Mar'tu's check rolls dice of other sizes, so use the ingredient.\n" + _STUCK
        ),
        names=["roll_die", "die_size"],
        support="none",
        # Teacher ruling: every Quick Check exercise is lean (the crash explainer names the slip and the line).
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="roll-die-size",
                text="Make `roll_die` hand back a random whole number from 1 to `die_size`.",
                dictated=False,
                hints=[
                    "Which ingredient says how many faces? `randint` takes the lowest face, then the highest.",
                    "`random.randint(1, 6)` rolls a d6, both ends included. A recipe uses its ingredient in place of "
                    "the 6.",
                    "Write `return random.randint(1, die_size)` in place of `return 1`.",
                ],
                checks=[recipe_check("roll_die", ["die_size"], kept=True, qc=True),
                        rnd_fn_check("roll_die rolls 1 to die_size", "roll_die", cases, special=special)],
                pass_line=pass_line,
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=["import random", "def roll_die(die_size):", good, f"print(roll_die({shown_size}))"],
            distractors=[f"    return random.randint(1, {shown_size})", "    return random.randint(0, die_size)",
                         "    return die_size"],
        ),
        another_way=[
            dict(angle="picture", text="```text\nroll_die(6)  -> randint(1, 6)\nroll_die(20) -> randint(1, 20)\n```"),
            dict(angle="campaign", label="You've seen this", text=(
                "`perform_roll(die_size)` at the trap door: `return random.randint(1, die_size)`. The same recipe "
                "with another name.")),
        ],
        campaign_link=dict(
            module="friends-in-low-places",
            part="skill-checks",
            snippet="def perform_roll(die_size):\n    return random.randint(1, die_size)\n",
            why=(
                "You have seen this. `perform_roll(die_size)` rolled a die of any size, because it used its "
                "ingredient, not a number from one call."
            ),
        ),
        takeaway="`random.randint(1, die_size)`: the ingredient decides the faces.",
        wrong_answers=[
            dict(why="the starter (return 1)", code=starter, fails_at=1, message_contains="without rolling"),
            dict(why=f"the shown call's size typed (A-06 test values: randint(1, {shown_size}))",
                 code=program(f"    return random.randint(1, {shown_size})"), fails_at=1,
                 message_contains=f"rolled `random.randint(1, {shown_size})`"),
            dict(why="a die that starts at 0", code=program("    return random.randint(0, die_size)"), fails_at=1,
                 message_contains="can give 0"),
            dict(why="the top face left out", code=program("    return random.randint(1, die_size - 1)"), fails_at=1,
                 message_contains="never gives"),
            dict(why="the biggest number first (randint(die_size, 1)): the shown call stops with Python's own words",
                 code=program("    return random.randint(die_size, 1)"), fails_at=0,
                 message_contains=f"empty range in randrange({shown_size}, 2)"),
            dict(why="rolled, not handed back", code=program("    roll = random.randint(1, die_size)"), fails_at=1,
                 message_contains="handed back `None`"),
            dict(why="rolled, then return 1 kept", code=program("    roll = random.randint(1, die_size)\n    return 1"),
                 fails_at=1, message_contains="not the roll"),
            dict(why="print instead of return", code=program("    print(random.randint(1, die_size))"), fails_at=1,
                 message_contains="printed its roll"),
            dict(why="the ingredient handed back", code=program("    return die_size"), fails_at=1,
                 message_contains="as it came in"),
            dict(why="randint with no random. in front", code=program("    return randint(1, die_size)"), fails_at=0,
                 message_contains="'randint' is not defined"),
            dict(why="import random removed", code=program(good, head=""), fails_at=0,
                 message_contains="'random' is not defined"),
            dict(why="one value handed to randint", code=program("    return random.randint(die_size)"), fails_at=0,
                 message_contains="missing 1 required positional argument"),
            dict(why="the other size typed", code=program(f"    return random.randint(1, {other})"), fails_at=1,
                 message_contains="does not follow `die_size`"),
            dict(why="the def line changed (another ingredient)",
                 code=program("    return random.randint(1, sides)").replace("roll_die(die_size)", "roll_die(sides)"),
                 fails_at=1, message_contains="ingredients changed from the starter"),
            dict(why="approximate ingredient name (size for die_size)", code=program("    return random.randint(1, size)"),
                 fails_at=0, message_contains="'size' is not defined"),
            dict(why="the campaign's recipe name (perform_roll)",
                 code=program(good).replace("def roll_die(", "def perform_roll("), fails_at=0,
                 message_contains="'roll_die' is not defined"),
            dict(why="lean: the campaign's recipe name, the call removed (the kept def line is named, never shown)",
                 code=program(good).replace("def roll_die(", "def perform_roll(").replace(
                     f"print(roll_die({shown_size}))\n", ""), fails_at=1,
                 message_contains="`def` line is gone, or its name changed"),
        ],
        notes=_qc_meta("randint-param", "", "", form) + "\n"
        f"QC-R1 C4, form {form}. RND: `random.randint` is swapped for a scripted die that records its arguments "
        f"(and a bare `randint` from `from random import randint` too). The check rolls sizes {[s for s, _ in cases]}; "
        f"the starter's visible call is roll_die({shown_size}), so typing its size (A-06's test values) fails on the "
        "other size. Deterministic: the scripted die returns fixed values. Lean messages: no message shows the "
        "`randint` line or the fix (teacher ruling): the starter's `return 1` gets 'The recipe does not roll.', and "
        "`randint(die_size, 1)` without the call gets 'The numbers in the roll are in the wrong order.' "
        "`random.randint(die_size, 1)` stops on the shown call with Python's 'empty range in randrange(...)'. The "
        "pass line is the Quick Check's last: a recap of this form's own tasks, then the stretch (Lucky's side "
        "quests, the supply-run challenge). support='none', explainer='lean'.",
    )


# ---- C5: trace the call (trace-call): two ledger rows, typed, with the slips named ----

def row_check(label, name, want, rules, default):
    """The ledger shape (ported from u03a's row_check): `name` holds `want`. rules = {wrong value: targeted message}.
    A Quick Check (lean): the messages name the slip, never the number or the fix."""
    code = (
        f"assert {name!r} in globals(), 'The line `{name} = 0` from the starter is gone.'\n"
        f"_v = globals()[{name!r}]\n"
        f"assert type(_v).__name__ != 'str', '`{name}` holds text, because of the quotes.'\n"
        f"_rules = {dict(rules)!r}\n"
        "_msg = ''\n"
        f"if not (_v == {want!r} and type(_v).__name__ == 'int'):\n"
        "    _msg = _rules.get(_v, '') if type(_v).__name__ == 'int' else ''\n"
        "    if not _msg and _v == 0:\n"
        f"        _msg = {default!r} + ' `{name}` still holds the starter' + chr(39) + 's 0.'\n"
        f"    _msg = _msg or {default!r}\n"
        "assert not _msg, _msg\n"
    )
    return (label, code)


def paste_guard(fn):
    """The ledger's guard: the program may not be pasted in and run. No `def`, no call to the recipe, no `print(`."""
    code = (
        "import ast as _ast\n"
        "_bad = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef' or "
        "(type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id in "
        f"({fn!r}, 'print'))]\n"
        "assert not _bad, ('The editor holds more than the two row lines: a `def`, a call to the recipe or a '\n"
        "                  '`print`. This task is traced by reading, yes?')\n"
    )
    return ("the program is traced, not run", code)


def paste_stop(fn):
    """Hidden `setup` (as u03a's ledger): when the editor holds a `def`, a call to `fn` or a `print(`, the program is
    stopped before it runs (SystemExit ends it quietly), so a pasted program prints nothing and the console never
    shows the answer. The paste guard check then names the slip. Code that does not parse runs as usual."""
    return (
        "def _paste_stop():\n"
        "    import ast\n"
        "    try:\n"
        "        _tree = ast.parse(_source)\n"
        "    except SyntaxError:\n"
        "        return\n"
        "    for _n in ast.walk(_tree):\n"
        "        if type(_n).__name__ == 'FunctionDef' or (type(_n).__name__ == 'Call' and type(_n.func).__name__ == "
        f"'Name' and _n.func.id in ({fn!r}, 'print')):\n"
        "            raise SystemExit\n"
        "\n"
        "\n"
        "_paste_stop()\n"
    )


# A Quick Check (lean): each slip is named with its evidence, never the number or the fix.
_CONST = "That adds the numbers written in the recipe, not what is IN each box when `return` runs."
_RAW = "That adds the values handed over, not what the recipe worked out."


def _qc_trace(form, fn, params, mults, boxes, box, call):
    """The ledger shape with new numbers: what the call hands back, then what the last line prints.
    params/mults/boxes: `boxes[i] = params[i] * mults[i]`; `box = fn(*call) + 10`."""
    (p1, p2), (m1, m2), (b1, b2), (a1, a2) = params, mults, boxes, call
    back = a1 * m1 + a2 * m2
    shown = back + 10
    const, raw = m1 + m2, a1 + a2
    one_box = [a1 * m1, a2 * m2]
    # Each row's slips must differ from each other and from the row's answer, so every slip gets its own message.
    for want, keys in ((back, [const, raw, shown, *one_box]), (shown, [back, const + 10, raw + 10, const, raw])):
        assert len(set(keys)) == len(keys) and want not in keys, (want, keys)
    slips = [back, shown, const, raw, const + 10, raw + 10, *one_box]
    program = (
        f"def {fn}({p1}, {p2}):\n"
        f"    {b1} = {p1} * {m1}\n"
        f"    {b2} = {p2} * {m2}\n"
        f"    return {b1} + {b2}\n"
        "\n"
        f"{box} = {fn}({a1}, {a2}) + 10\n"
        f"print({box})\n"
    )
    assert max(len(line) for line in program.splitlines()) <= 36

    def rows(back_row=0, printed_row=0, quote=False):
        q = '"' if quote else ""
        return (f"# The ledger for {fn}({a1}, {a2})\n"
                f"handed_back_row = {q}{back_row}{q}\n"
                f"printed_row = {printed_row}\n")

    starter = rows()
    solution = rows(back, shown)
    added = "That adds the 10 from the last line too."
    one = "That is what one box holds, not what `return` hands back."
    forgot = "That leaves out the 10 the last line adds."
    back_rules = {const: _CONST, raw: _RAW, shown: added, one_box[0]: one, one_box[1]: one}
    shown_rules = {
        back: forgot,
        const + 10: "That adds the numbers written in the recipe, then 10.",
        raw + 10: "That adds the values handed over, then 10.",
        const: _CONST,
        raw: _RAW,
    }
    # Another way traces another call, so no angle hands over this task's rows.
    o1, o2 = (5, 4) if form == "A" else (3, 5)
    o_back = o1 * m1 + o2 * m2
    assert o_back not in slips and o_back + 10 not in slips
    guard = paste_guard(fn)
    return dict(
        id="trace-the-call",
        title="Trace the call",
        martu=_QC_MARTU + (
            "Trace it like the ledger: what does the call hand back, and what does the last line print?\n"
            "```python\n" + program + "```\n" + _STUCK
        ),
        names=["handed_back_row", "printed_row"],
        support="none",
        # Teacher ruling: every Quick Check exercise is lean (the crash explainer names the slip and the line).
        explainer="lean",
        # A pasted program is stopped before it runs, so its printed number never shows (U3 review).
        setup=paste_stop(fn),
        starter=starter,
        checkpoints=[
            dict(
                id="handed-back-row",
                text=f"Set `handed_back_row` to the number `{fn}({a1}, {a2})` hands back.",
                dictated=False,
                hints=[
                    f"Look at the `return` line. What is in `{b1}` and `{b2}` when it runs?",
                    "Work out a line from what is IN the boxes: if `cups` holds 2, then `cups * 10` is 20.",
                    f"Write `handed_back_row = ` and then what `{b1}` and `{b2}` hold, added together.",
                ],
                checks=[guard, row_check(f"handed_back_row is {back}", "handed_back_row", back, back_rules,
                                         f"That is not what `{fn}({a1}, {a2})` hands back.")],
            ),
            dict(
                id="printed-row",
                text="Set `printed_row` to the number the last line prints.",
                dictated=False,
                hints=[
                    f"The `{box}` line: the call becomes what it handed back. Then the `+ 10`.",
                    "If a recipe hands back 8, then `x = recipe() + 1` puts 9 in `x`.",
                    "Write `printed_row = ` and then your `handed_back_row` number plus 10.",
                ],
                checks=[guard, row_check(f"printed_row is {shown}", "printed_row", shown, shown_rules,
                                         "That is not what the last line prints.")],
                pass_line="Mar'tu: Traced, not guessed. That is the ledger, yes?",
            ),
        ],
        solution=solution,
        partials=[rows(back)],
        another_way=[
            dict(angle="picture", label="Another call", text=(
                f"```text\n{fn}({o1}, {o2})\n  {p1} = {o1}\n  {p2} = {o2}\n  {b1} = {o1 * m1}\n  {b2} = {o2 * m2}\n"
                f"  return {o_back} ----+\n                |\n{box} = {o_back} + 10\n```")),
            dict(angle="step-by-step", text=(
                f"1. The call fills `{p1}` and `{p2}`, in order. 2. Work out `{b1}` and `{b2}` from what is IN them. "
                f"3. `return` hands back `{b1} + {b2}`. 4. The last line adds 10, and `print` shows `{box}`.")),
        ],
        takeaway="Trace a call with what is IN the boxes. What comes back lands where the call was.",
        wrong_answers=[
            dict(why="the starter (the 0 left)", code=starter, fails_at=1, message_contains="still holds the starter's 0"),
            dict(why=f"handed back = {const}: the numbers written in the recipe (the 15-type answer, A-03/A-04)",
                 code=rows(const), fails_at=1, message_contains="numbers written in the recipe"),
            dict(why=f"handed back = {raw}: the values handed over (the 7-type answer, A-07)", code=rows(raw),
                 fails_at=1, message_contains="values handed over"),
            dict(why=f"handed back = {shown}: the + 10 from the last line added in", code=rows(shown), fails_at=1,
                 message_contains="10 from the last line"),
            dict(why=f"handed back = {one_box[1]}: one box only", code=rows(one_box[1]), fails_at=1,
                 message_contains="one box holds"),
            dict(why="handed back in quotes", code=rows(back, quote=True), fails_at=1, message_contains="because of the quotes"),
            dict(why="the program pasted in and run (the paste guard)", code=program + "\n" + solution, fails_at=1,
                 message_contains="more than the two row lines"),
            dict(why=f"printed = {back}: the + 10 dropped", code=rows(back, back), fails_at=2,
                 message_contains="leaves out the 10"),
            dict(why=f"printed = {const + 10}: the numbers in the recipe, then 10", code=rows(back, const + 10),
                 fails_at=2, message_contains="numbers written in the recipe, then 10"),
            dict(why=f"printed = {raw + 10}: the values handed over, then 10", code=rows(back, raw + 10), fails_at=2,
                 message_contains="values handed over, then 10"),
            dict(why="printed row: the 0 left", code=rows(back), fails_at=2, message_contains="still holds the starter's 0"),
            dict(why="a print added to check the rows (the guard: no print in the editor)",
                 code=solution + "print(handed_back_row)\n", fails_at=1, message_contains="more than the two row lines"),
        ],
        notes=_qc_meta("trace-call", "", "cups,recipe,x", form, level="S2") + "\n"
        f"QC-R1 C5, form {form} (teacher ruling on the Unit 3 reviews: the code tasks alone gate the test-out, so "
        "tracing gets a gated task, as Unit 2's C3 did; typed rows, checked, no question scoring needed). The "
        f"ledger shape with new numbers: {fn}({a1}, {a2}) hands back {back}, the last line prints {shown}. Placed "
        "second, so C4 stays last. No Example (it would print the answer); the program sits in Mar'tu's fenced "
        "block, and the paste guard fails any `def`, call to the recipe or `print(` in the editor; the hidden setup "
        "(paste_stop) stops such a program before it runs, so the console never shows its number. No assemble (its "
        "pieces would be the rows). Every slip gets "
        f"a message that names it without the number: {const} (the constants, A-03/A-04), {raw} (the raw inputs, "
        f"A-07), {shown} in the first row (the + 10 added early), {one_box[0]}/{one_box[1]} (one box), then "
        f"{back} printed (the + 10 dropped), {const + 10} and {raw + 10} (the same slips, then 10). Another way "
        f"traces {fn}({o1}, {o2}), never this call. support='none', explainer='lean'.",
    )


# The page says the pass rule under it, counted (LessonPlayer's Quick Check intro), so the summary does not repeat it.
_QC_SUMMARY = (
    "Five short tasks, then four questions. Nobody has to know this yet: it only shows Mar'tu where to start. Tasks "
    "you pass here stay ticked."
)
_STRETCH = "Want more? Lucky's side quests in Recipes With Names, or the challenge Lucky's Supply Run."


QC_R1_A = dict(
    kind="testout",
    id="qc-r1-a",
    title="Quick Check Recipes I · Form A",
    optional=True,
    minutes=12,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_write("A", "armor_total", ["base_armor", "bonus_armor"], "Lucky", (10, 3), 13,
                  [((7, 5), 12), ((20, 4), 24)],
                  ("coins_left", ["coins", "spent"],
                   "def coins_left(coins, spent):\n    result = coins - spent\n    return result\n\n\nprint(coins_left(20, 6))\n",
                   "14")),
        _qc_trace("A", "ward_strength", ("lanterns", "runes"), (10, 5), ("light", "glow"), "barrier", (2, 5)),
        _qc_board("A", "west", "north", "get_warning", "present_warning", "GET INSIDE, NOW!", "Get inside, now!"),
        _qc_check("A", "latch_check", "Bomb Shell", "picks the latch"),
        _qc_roll("A", 20, [(6, 5), (20, 17), (4, 3)],
                 "Mar'tu: The scout stepped west, the warning reached the board, the latch opened, and the die is "
                 "yours. " + _STRETCH),
    ],
    notes=(
        "Quick Check Recipes I, form A (code tasks, in order C1, C5, C2, C3, C4: C5 sits second so C4 stays last). "
        "Pass = every code task plus 3 of the 4 questions in qc-r1-a-questions; a retake draws form B. The site "
        "gates on both (questions_to_pass=3, as Unit 2's QC2). The code tasks still cover the unit on their own "
        "(teacher ruling on the Unit 3 reviews: C5 added, so nobody tests out without tracing). Framing (G4 R25): it "
        "shows Mar'tu where to start. Messages are lean, like the explainer: the slip and the evidence in brackets, "
        "never the fix, the finished line or the recipe body (u03b `_leaned`; no `def` line, no `>=`, no `randint` "
        "line), so a task can't be passed by following them. "
        "Coverage (lint d): param-use -> C1 (WA `base + bonus` PNM, `return 13` PAR-CONST, typed `10 + 3`) and Q3 "
        "(numbers in ink); return-value -> C1 (WA print, no return), C3 (WA print, if with no else), C4 (WA rolled "
        "not returned), Q2 (None); return-right-name -> C1 (WA return result, a typo of its own box); trace-call -> "
        "C5 (WA the 15-type constants, the 7-type raw inputs, the dropped + 10); replace-pass -> C2 CP1 (WA "
        "unquoted, the Example's direction, unindented); def-call -> C2 (WA no `()` on the helper), C1 (WA def below "
        "the call, def used for a box) and Q1; store-then-pass -> C2 CP2 (WA no store, typed line, printed or "
        "returned instead of passed); return-comparison, boundary -> C3 (WA `>`, `return True`, `==`, a typed "
        "number); randint-param -> C4 (WA randint(1, 20), from 0, top left out, biggest first); chain-methods -> Q4 "
        "and C2's finished helper. C4's pass line recaps this form's own tasks and offers the stretch. "
        "support='none' and explainer='lean' everywhere: no hints, tracer or compare; glossary and read-aloud stay "
        "on. 12 minutes (was 9)."
    ),
)

QC_R1_B = dict(
    kind="testout",
    id="qc-r1-b",
    title="Quick Check Recipes I · Form B",
    optional=True,
    minutes=12,
    summary=_QC_SUMMARY,
    questions_to_pass=3,
    exercises=[
        _qc_write("B", "shield_total", ["base_shield", "bonus_shield"], "Bomb Shell", (6, 4), 10,
                  [((9, 2), 11), ((15, 4), 19)],
                  ("hours_left", ["hours", "gone"],
                   "def hours_left(hours, gone):\n    result = hours - gone\n    return result\n\n\nprint(hours_left(37, 5))\n",
                   "32")),
        _qc_trace("B", "glow_total", ("candles", "runes"), (4, 3), ("light", "shine"), "room", (5, 3)),
        _qc_board("B", "east", "south", "get_farewell", "present_farewell", "SAFE TRAVELS, FRIENDS.",
                  "Safe travels, friends."),
        _qc_check("B", "dodge_check", "Lucky", "dodges a falling beam"),
        _qc_roll("B", 6, [(12, 9), (6, 4), (8, 7)],
                 "Mar'tu: The scout stepped east, the farewell reached the board, Lucky dodged the beam, and the die "
                 "is yours. " + _STRETCH),
    ],
    notes=(
        "Quick Check Recipes I, form B: shield_total(base_shield, bonus_shield) for Bomb Shell (6 + 4) with an "
        "Example `hours_left` that uses `result`; C5 traces glow_total(5, 3) + 10 (hands back 29, prints 39); "
        "step_east and get_farewell / present_farewell; dodge_check for Lucky; roll_die's d12 test (sizes 12, 6 and "
        "8; the starter shows roll_die(6)). Same coverage, order and rules as form A, 12 minutes. Questions live in "
        "qc-r1-b-questions: pass = every code task plus 3 of the 4 (questions_to_pass=3). Lean check messages."
    ),
)


def _qc_questions(form, box_line, no_return, ink, shout):
    """no_return / ink / shout = (code, answer, choices, explain, notes)."""
    def predict(qid, parts):
        code, answer, choices, explain, notes = parts
        return dict(type="predict", id=qid, q="What will this print?", code=code, answer=answer, choices=choices,
                    explain=explain, notes=notes)

    name, value = box_line
    return dict(
        kind="quiz",
        id=f"qc-r1-{form.lower()}-questions",
        title=f"Quick Check Recipes I · Form {form} questions",
        optional=True,
        minutes=3,
        summary="Four questions that go with Quick Check Recipes I. To pass the Quick Check, get 3 of the 4 right.",
        questions=[
            dict(
                type="mc",
                id="box-or-recipe",
                q="Which line makes a box?",
                choices=[f"def {name} = {value}", f"{name} = {value}", f"def {name}():"],
                answer=1,
                why_wrong={
                    0: "`def` never makes a box. Python stops at once: it expects `(` after the name.",
                    2: "`def` makes a recipe, not a box. It needs indented steps under it, and holds no value.",
                },
                explain=f"A box is a name, `=`, and a value: `{name} = {value}`. `def` makes a recipe.",
                notes="Skill def-call (`=` versus `def`). Evidence: A-02 `def (\"character\")`, def used to make a box.",
            ),
            predict("no-return", no_return),
            predict("numbers-in-ink", ink),
            predict("lower-then-capitalize", shout),
        ],
        notes=(
            f"Quick Check Recipes I, form {form} questions (scored with qc-r1-{form.lower()}: every code task plus 3 "
            "of the 4 questions, questions_to_pass=3 on the form, as Unit 2's QC2). The best score counts, so a retake "
            "can lift it. Q3 was follow-the-call; it moved into C5 and numbers-in-ink took its place. No hints; "
            "read-aloud and glossary stay on."
        ),
    )


QC_R1_A_QUESTIONS = _qc_questions(
    "A",
    ("hero", "\"Lucky\""),
    (
        "def shield_for(affinity):\n    shield = affinity + 4\n\n\nlucky_shield = shield_for(13)\nprint(lucky_shield)\n",
        "None",
        ["17", "None", "13", "shield"],
        (
            "The recipe works out 17 and keeps it in `shield`, but it has no `return`. So the call hands back "
            "`None`, and `lucky_shield` holds `None`."
        ),
        "Skill return-value (Q2): no return -> None. Distractors: the worked-out value (the 26-type answer), the "
        "argument, the box's name.",
    ),
    (
        "def show_cost(count, price):\n    print(3 * 5)\n\nshow_cost(2, 9)\n",
        "15",
        ["15", "18", "an error"],
        (
            "Numbers typed inside the recipe are written in ink: every call shows 15, whatever it hands over. To use "
            "the 2 and the 9, the recipe needs its ingredients, `count * price`."
        ),
        "Skill param-use (Q3, numbers in ink: A-06/A-07, typed test values, 7 of 11). Distractors: 18 (the belief "
        "that the call's values flow in anyway, 2 * 9), an error (the ingredients are never used). It replaces "
        "follow-the-call, which moved into the gated C5.",
    ),
    (
        "def get_question():\n    line = \"WHO GOES THERE?\"\n    line = line.lower()\n    line = line.capitalize()\n"
        "    return line\n\n\nprint(get_question())\n",
        "Who goes there?",
        ["WHO GOES THERE?", "who goes there?", "Who goes there?", "Who Goes There?"],
        "`.lower()` makes every letter small. Then `.capitalize()` makes only the first letter big.",
        "Skill chain-methods (Q4). Distractors: no change, only .lower(), every word capitalized.",
    ),
)

QC_R1_B_QUESTIONS = _qc_questions(
    "B",
    ("spell", "\"Fireball\""),
    (
        "def fuel_for(cells):\n    fuel = cells * 5\n\n\ntank = fuel_for(3)\nprint(tank)\n",
        "None",
        ["15", "None", "3", "fuel"],
        (
            "The recipe works out 15 and keeps it in `fuel`, but it has no `return`. So the call hands back `None`, "
            "and `tank` holds `None`."
        ),
        "Form B of no-return.",
    ),
    (
        "def show_heal(base, bonus):\n    print(6 + 2)\n\nshow_heal(4, 5)\n",
        "8",
        ["8", "9", "an error"],
        (
            "Numbers typed inside the recipe are written in ink: every call shows 8, whatever it hands over. To use "
            "the 4 and the 5, the recipe needs its ingredients, `base + bonus`."
        ),
        "Form B of numbers-in-ink. Distractors: 9 (the call's values, 4 + 5), an error.",
    ),
    (
        "def get_order():\n    line = \"STAY BEHIND THE WARD.\"\n    line = line.lower()\n    line = line.capitalize()\n"
        "    return line\n\n\nprint(get_order())\n",
        "Stay behind the ward.",
        ["STAY BEHIND THE WARD.", "stay behind the ward.", "Stay behind the ward.", "Stay Behind The Ward."],
        "`.lower()` makes every letter small. Then `.capitalize()` makes only the first letter big.",
        "Form B of lower-then-capitalize.",
    ),
)


# =============================================================================================
# Cheatsheet 3 "Mar'tu's Chalk Notes: Recipes"
# =============================================================================================

CHALK_NOTES_3 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Recipes",
    summary="Everything from Unit 3 on one page. Printable.",
    entries=[
        dict(concept="A recipe: `def`, then call it",
             code="def say_steady():\n    print(\"Steady, now.\")\n\n\nprint(\"First line.\")\nsay_steady()\n",
             output="First line.\nSteady, now.",
             note="`def` makes a recipe (a function): a named set of steps, indented under it. Making it runs "
                  "nothing. Its name with `()` calls it. (Lesson: Recipes With Names)"),
        dict(concept="`=` makes a box, `def` makes a recipe",
             code="steady = \"Steady, now.\"\nprint(steady)\n", output="Steady, now.",
             note="A box holds a value. A recipe holds steps. `def` never makes a box."),
        dict(concept="`pass`: a blank recipe card",
             code="def step_north():\n    pass\n\n\nstep_north()\nprint(\"Nothing moved.\")\n", output="Nothing moved.",
             note="`pass` means do nothing. Replace it with real steps, indented. You've seen this: `move_left()` "
                  "with `party.move(\"left\")`."),
        dict(concept="Ingredients and what you hand over",
             code="def warn(hero_name):\n    print(hero_name + \", get inside!\")\n\n\nwarn(\"Lucky\")\n"
                  "warn(\"Bomb Shell\")\n",
             output="Lucky, get inside!\nBomb Shell, get inside!",
             note="`hero_name` is the ingredient (parameter) on the card. `\"Lucky\"` is what you hand over (argument). "
                  "Each call fills the ingredient fresh."),
        dict(concept="Use the ingredients, never one call's numbers",
             code="def show_hit(base_damage, bonus):\n    print(base_damage + bonus)\n\n\nshow_hit(4, 3)\n"
                  "show_hit(8, 2)\n",
             output="7\n10",
             note="`print(4 + 3)` inside would show 7 for every call. The numbers arrive when the recipe is called."),
        dict(concept="Hand it back: `return`",
             code="def max_mana_for(affinity):\n    total = affinity * 2\n    return total\n\n\n"
                  "lucky_max = max_mana_for(13)\nprint(lucky_max)\n",
             output="26",
             note="`return` hands the answer back to the call. `lucky_max = ...` catches it in a box."),
        dict(concept="No `return`: `None`",
             code="def max_mana_for(affinity):\n    print(affinity * 2)\n\n\nlucky_max = max_mana_for(13)\n"
                  "print(lucky_max)\n",
             output="26\nNone",
             note="`print` only shows the answer. With no `return`, the call hands back `None`."),
        dict(concept="Hand back the right box",
             code="def crate_count(rows, per_row):\n    total = rows * per_row\n    return total\n\n\n"
                  "print(crate_count(4, 3))\n",
             output="12",
             note="Hand back the box this recipe made, `total`. A name from an example, like `result`, is not here."),
        dict(concept="Follow a call",
             code="def lamp_oil(lamps, nights):\n    oil = lamps * 2\n    spare = nights * 3\n"
                  "    return oil + spare\n\n\nstock = lamp_oil(4, 2) + 1\nprint(stock)\n",
             output="15",
             note="Write each box's value: lamps 4, nights 2, oil 8, spare 6. The call hands back 14, so `stock` is "
                  "15. Use what is IN the boxes. (Lesson: Recipes With Names, Be the ledger)"),
        dict(concept="Store, then pass it on",
             code="def get_line():\n    return \"Barrier's holding.\"\n\n\ndef present_line():\n"
                  "    words = get_line()\n    print(words)\n\n\npresent_line()\n",
             output="Barrier's holding.",
             note="Call the helper, store what it hands back in a variable, then pass that variable on. You've seen "
                  "this: `present_dialogue_option()`."),
        dict(concept="`.lower()` then `.capitalize()`",
             code="line = \"WHO GOES THERE?\"\nline = line.lower()\nline = line.capitalize()\nprint(line)\n",
             output="Who goes there?",
             note="`.lower()` makes every letter small. `.capitalize()` makes only the first letter big."),
        dict(concept="Hand back a comparison",
             code="def gate_check(roll):\n    needed = 9\n    return roll >= needed\n\n\nprint(gate_check(8))\n"
                  "print(gate_check(9))\n",
             output="False\nTrue",
             note="`roll >= needed` is already `True` or `False`, so hand it back. An `if` with `return True` and "
                  "`else:` `return False` does the same. You've seen this: `return roll >= required_roll`."),
        dict(concept="A rolling recipe",
             code="import random\n\n\ndef roll_die(die_size):\n    return random.randint(1, die_size)\n\n\n"
                  "print(roll_die(20))\n",
             note="The ingredient decides the faces: `roll_die(6)` is a d6. You've seen this: `perform_roll(die_size)`."),
        dict(concept="Error: `def` to make a box", code="def max_mana = 18\n",
             note="SyntaxError: expected '('. `def` makes recipes. A box is `max_mana = 18`."),
        dict(concept="Error: a missing colon", code="def say_ready()\n    print(\"Ready.\")\n",
             note="SyntaxError: expected ':'. A `def` line ends with `:`."),
        dict(concept="Error: an empty recipe", code="def say_ready():\n\nsay_ready()\n",
             note="IndentationError: expected an indented block after function definition. Put at least one indented "
                  "line inside, even `pass`."),
        dict(concept="Error: a call before its `def`", code="say_ready()\n\n\ndef say_ready():\n    print(\"Ready.\")\n",
             note="NameError: name 'say_ready' is not defined. Python reads from the top: put the `def` above the call."),
        dict(concept="Error: a value too few",
             code="def show_hit(base_damage, bonus):\n    print(base_damage + bonus)\n\n\nshow_hit(4)\n",
             note="TypeError: show_hit() missing 1 required positional argument: 'bonus'. Hand over one value for "
                  "each ingredient."),
        dict(concept="Error: a name from an example",
             code="def crate_count(rows, per_row):\n    total = rows * per_row\n    return result\n\n\n"
                  "print(crate_count(4, 3))\n",
             note="NameError: name 'result' is not defined. Hand back this recipe's own box: `return total`."),
        dict(concept="No `()`: no call", code="def say_ready():\n    print(\"Ready.\")\n\n\nsay_ready\n",
             note="No error, and nothing runs. A recipe's name alone is not a call: add `()`. Printing it shows "
                  "`<function say_ready ...>`."),
    ],
    notes="Cheatsheet 3 (spec items in order, then the errors this unit catches). Entries with `output` are run and "
          "checked by the harness; the random roll and the errors have none. Teacher ruling on the Unit 3 reviews: "
          "no entry shares a name or number with the Quick Check (`gate_check` with `needed = 9`, not form A's "
          "`latch_check`; `crate_count`, not form A's `armor_total(10, 3)`) or with the lesson's ledger "
          "(`lamp_oil(4, 2) + 1`, not `ward_strength(3, 4) + 10`), so the page never hands over an answer.",
)


ITEMS = [EXTRA_3X, SUPPLY_RUN, QC_R1_A, QC_R1_A_QUESTIONS, QC_R1_B, QC_R1_B_QUESTIONS, CHALK_NOTES_3]
