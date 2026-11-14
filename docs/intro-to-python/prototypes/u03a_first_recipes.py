"""Unit 3 "Functions I" ("First Recipes"), part a: Mar'tu remembers (6a-remembers), Lesson 6A "Recipes With Names"
and Quiz 6A.

Spec: design/curriculum.md, "## Unit 3 · Functions I", items 1 and 2 (u03a): 6a-remembers; 6A-01 to 6A-11 (with the
contingent 6A-05a and the ledger 6A-06b) and 6A-S; Quiz 6A (5 predict, 2 mc, 1 parsons: a deliberate change from the
spec's 5 predict, 1 mc, 1 parsons, 1 fill, by the teacher's Unit 3 ruling). Introduces
node:FunctionDef (6A-01), node:Pass (6A-03), node:Return (6A-06) and attr:capitalize (6A-08). Everything else is a
Unit 1-2 idea. `None` is never written in student code (const:None comes in Unit 7): it only shows up as output.

Who this is for: the class already played campaign Modules 1 and 2 and struggled, and functions were the cliff
(0 of 11 wrote a working one on the diagnostic). They have SEEN `def move_left():` / `party.move("left")` at the cabin
door, `get_dialogue_prompt_string()` stored and passed to `print_prompt()`, and `perform_roll(die_size)` with
`return roll >= required_roll` at the trap door. So every campaign link here is "you've seen this, now you'll get it".
Every student has their own device; pair talk is optional, every checkpoint is solo.

Terminology (2.9): "recipe (function)", "ingredient (parameter)", "what you hand over (argument)", "hands back
(returns)". "Recipe" is never used for anything but `def`. "Box (variable)" as in Units 1-2.

Help ladder as fields (FORMAT.md, the order the site shows them), the same as Unit 2: hints[0] Where to look (point;
"Read Python's last line" in a debug step), the middle hints Teach me (a tiny example with other names, listed in
foreign_names), the last hint Show me how: the step's own line in backticks (``Write `x = 1`.``), whose start up to
its first `(` or `=` becomes Start me off. Ledger rows show the working, never the number. another_way, assemble
(More structure), then Compare. A SOLO item has no Start me off.

Check codes (curriculum 2.5), built by the helpers below. Every check that calls a student recipe does it with its
prints kept private (sys.stdout swapped and put back), so nothing a check does shows in the console:
  prints_check()   PAR / PAR-CONST on printed lines: fresh arguments the task never uses ("Tester", "Moth", (6, 5),
                   (20, 1)); a quoted ingredient name; the call table in brackets. A near-miss line gets the FIRST
                   DIFFERENCE from the wanted line, fix first, in Mar'tu's values only (_gap: "A space is missing
                   right after `Tester`.", "There is an extra space before `,`.", "The `.` at the end is missing."),
                   led by "A comma inside `print(...)` adds a space. Glue with `+` instead." when the recipe's print
                   puts values side by side with commas and the slip is an extra space (_spread). A printed line is
                   repeated back only when it is one of the task's own lines or a number; never the student's text.
  returns_check()  RET / RET-PARAM / PAR-CONST / RNM / PNM on what a recipe hands back: print-instead-of-return
                   ("printed 18 but handed back `None`"), a blank `return` ("`return` on its own hands back
                   nothing. Put the answer after it.", checked before the no-return message), no return, a parameter
                   handed back "as it came in", one fixed answer for both calls, text instead of a number, plus
                   per-exercise rules.
  calls_check()    the program calls the recipe (at the top level) at least N times; a bare name with no `()`; a
                   call indented inside its own recipe.
  _why()           a kind message for an error raised inside a recipe: PNM (a near-miss of an ingredient), RNM/LEFT
                   (a name from Mar'tu's example or a Teach hint), `___` left, `import random` missing, str() glue.
  _find()          the recipe exists; a box made with `=` instead of `def` (DEF); a near-miss recipe name (NAME).
  _resets()        B-02's "the call's values go in the body": a line inside the recipe that fills an ingredient with a
                   typed value ("Line 2 puts a typed value in `bonus` ... Delete that line"). Used by PAR, RET, BND, RND
                   whenever the results are wrong.
  _gamed()         A-08's working backward, with Unit 2's `if`: a comparison inside the recipe between an ingredient
                   and one of the values the check hands over (`if cells == 3: return 15`). Fails even when every case
                   matches, since a hand-made ladder would otherwise pass.
  _wrapped()       `print(say_steady())` around a recipe that prints and hands nothing back (the extra line is None).
                   calls_check says to write the call on its own.
  _why() (RNM)     a NameError on a `return` line names the boxes this recipe does make, and says when the name is a
                   box inside another recipe ("`total` is a box inside `max_mana_for`, another recipe"). A name from
                   Mar'tu's example on a `return` line, in a recipe that makes a box, gets "`result` comes from
                   Mar'tu's example. This recipe's box is `fuel`: hand that back." (the box is worked out before the
                   foreign-name branch, so `result` no longer sends the student to `cells` and back).
  row_check()      the ledger (6A-06b): one row per checkpoint, with the targeted messages from the spec. A guard runs
                   first: a `def`, a call to `ward_strength` or a `print(` in the editor fails every row ("The ledger
                   holds only your rows. ..."), so the program cannot be pasted in and run. paste_stop(), its hidden
                   `setup`, stops such a program before it runs, so its printed answer never shows in the console.
                   The ledger has no Assemble it: its pieces would be the finished rows (the harness warns).
  returns_check()  also: a box's name in quotes (`return "total"`) gets "Take the quotes off `total`", not the
                   hard-coding message.
  _BND / _NEEDED   6A-09: `needed` is read from the student's own recipe (any difficulty from 2 to 20 passes);
                   rolls needed - 1, needed, needed + 1, 1 and 20; then the recipe is rebuilt with another `needed`,
                   so a typed number (`roll >= 12`) is caught. The if/else form passes too.
  _RND             6A-10: random.randint is scripted and records its arguments; roll_die(6), (20), (12).
  _GREETING / _STORE / _PASS_ON  6A-08: TEXT that differs from the starter with both tidy lines kept; STO inside
                   present_greeting(); CALL plus CMB (get_greeting is swapped for another line, only inside the check).
Messages: the fix first, then what happened, then the evidence in brackets, "(Mar'tu's check called
`warn("Tester")`, only inside the check: ...)", as in Unit 2. Invented values only; a student's own text is never
repeated back (2.11), and no student's written value from the worksheets appears in student-facing text (T10).
No lesson codes ("2B", "6A-04") in student-facing text: units are named ("Unit 2").

Deviations from the spec, each small and noted on its exercise:
  * Starters whose recipe body was only a comment (6A-04, 6A-05, 6A-S) keep a `pass` line under the comment, so the
    first Run does not stop with an IndentationError (`pass` is taught in 6A-03, just before).
  * The "Run prints nothing" predict (6A-01) ends the program with one visible line, because a predict choice must
    be exactly what the console shows and the player cannot show an empty choice.
  * 6A-03, 6A-08, 6A-09 and 6A-10 end with a call or a try line (the campaign's game called the recipes for them),
    so Run shows something. The numbered comments still map one-to-one onto the checkpoints.
  * 6A-04's side quest is a second recipe, `warn_hours`, so finishing it never turns `warn`'s step red.
  * Quiz 6A #3 is a predict, which has no why_wrong: the 6A-06b messages for 60, 50, 25 and 20 are in its explain.
  * Quiz 6A swaps two near-duplicates (made-not-called, exactly-enough) for the two cliffs it was missing:
    numbers-in-ink (predict) and return-the-right-box (mc). Mix: 5 predict, 2 mc, 1 parsons.
  * Quiz 6A #6 (parsons) passes the line to `print()`: parsons questions cannot have hidden setup.
  * 6A-05a (K, contingent) sits in the lesson in order; the prototype has no contingent flag (meta notes it).
  * 6A-06b is the prototype ledger (rows as boxes, one checkpoint per row) until the trace-table item type exists.
    It has no Example (nothing to Run): the program is only in Mar'tu's fenced block, and the angles trace another
    call, `ward_strength(4, 3) + 10`.
  * 6A-S adds a third step, `heal_total` (a return), so the solo also records "hand a value back".
  * SOLO seat B and the twins live in `notes` (meta), as in Unit 2.
  * 6A-S sets explainer="lean" (FORMAT.md, the teacher's ruling: every SOLO item from Unit 2 on).

Phone width: every fenced picture or code block in prose is at most 36 characters a line.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u03a
"""

# ---------------------------------------------------------------------------------------------
# Check builders (plain string templates, filled in per exercise)
# ---------------------------------------------------------------------------------------------

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def _names_py(params):
    quoted = ["`" + p + "`" for p in params]
    return quoted[0] if len(quoted) == 1 else ", ".join(quoted[:-1]) + " and " + quoted[-1]


# Shared by every recipe check. `_run` calls a student recipe with its prints kept private (and, with `_rolls`,
# a scripted die that records its arguments), and always puts stdout and random.randint back.
_FN = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import random as _random
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__


def _show(_v):
    _t = type(_v).__name__
    if _t == 'str':
        return '"' + _v + '"'
    if _t == 'function':
        return _v.__name__
    return str(_v)


def _ct(_name, _args):
    return '`' + _name + '(' + ', '.join(_show(_a) for _a in _args) + ')`'


def _ev(_name, _args, _what):
    return " (Mar'tu's check called " + _ct(_name, _args) + ', only inside the check: ' + _what + '.)'


def _whole(_v):
    return r'(?<![\d.])' + _re.escape(str(_v)) + r'(?!\d)(?!\.\d)'


def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b, _loose=True):
    # NAME / PNM near miss: case, plural, 1-2 edits; loosely also a shared `_` word or a substring.
    if _a == _b:
        return False
    _la, _lb = _a.lower(), _b.lower()
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    if min(len(_la), len(_lb)) >= 3 and _edits(_la, _lb) <= 2:
        return True
    if not _loose:
        return False
    _wa = set(_w for _w in _la.split('_') if len(_w) >= 3)
    _wb = set(_w for _w in _lb.split('_') if len(_w) >= 3)
    return bool(_wa & _wb) or (len(_la) >= 4 and (_la in _lb or _lb in _la))


def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    if not _q:
        return 'no ingredients'
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _params(_f):
    _c = _f.__code__
    return list(_c.co_varnames[:_c.co_argcount])


def _defs():
    return {_n.name: _n for _n in _tree.body if type(_n).__name__ == 'FunctionDef'}


def _top():
    return [_n for _n in _tree.body if type(_n).__name__ != 'FunctionDef']


def _calls_in(_nodes, _name):
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
            and type(_c.func).__name__ == 'Name' and _c.func.id == _name]


def _bare(_name):
    return [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr'
            and type(_n.value).__name__ == 'Name' and _n.value.id == _name]


def _made(_d):
    # The boxes a recipe makes with `=`, in order.
    _out = []
    for _n in _ast.walk(_d):
        if type(_n).__name__ == 'Assign':
            for _t in _n.targets:
                if type(_t).__name__ == 'Name' and _t.id not in _out:
                    _out.append(_t.id)
    return _out


def _resets(_name):
    # A common belief: the call's values go in the body. A line inside the recipe that fills an ingredient with a
    # typed value throws away what every call hands over.
    _d = _defs().get(_name)
    if _d is None:
        return ''
    _ps = [_a.arg for _a in _d.args.args]
    for _n in _ast.walk(_d):
        if (type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Constant'
                and any(type(_t).__name__ == 'Name' and _t.id in _ps for _t in _n.targets)):
            _p = [_t.id for _t in _n.targets if type(_t).__name__ == 'Name' and _t.id in _ps][0]
            return ('Line ' + str(_n.lineno) + ' puts a typed value in `' + _p + '`, so what each call hands over '
                    'is thrown away. Delete that line: the call fills `' + _p + '` for you.')
    return ''


def _gamed(_name, _vals):
    # Working backward, with Unit 2's `if`: test for the very values Mar'tu's check hands over.
    _d = _defs().get(_name)
    if _d is None:
        return ''
    _ps = [_a.arg for _a in _d.args.args]
    for _n in _ast.walk(_d):
        if type(_n).__name__ != 'Compare':
            continue
        _sides = [_n.left] + list(_n.comparators)
        _names = [_s.id for _s in _sides if type(_s).__name__ == 'Name' and _s.id in _ps]
        _consts = [_s.value for _s in _sides if type(_s).__name__ == 'Constant']
        if _names and any(_c == _x and type(_c) == type(_x) for _c in _consts for _x in _vals):
            return ('Line ' + str(_n.lineno) + " looks for one of the values Mar'tu's check hands over. "
                    "A recipe can't know which call comes next: work the answer out from "
                    + _names_of(_ps) + ', so every call works.')
    return ''


def _names_of(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _wrapped(_name):
    # `print(say_steady())` around a recipe that prints and hands nothing back: the extra line says None.
    _d = _defs().get(_name)
    if _d is None or any(type(_n).__name__ == 'Return' and _n.value is not None for _n in _ast.walk(_d)):
        return []
    return sorted(set(_c.lineno for _c in _calls_in(_top(), 'print') if _calls_in([_c], _name)))


def _spread(_name):
    # `print(hero_name, ", get inside!")`: values side by side with commas, and print puts a space between them.
    _d = _defs().get(_name)
    return _d is not None and any(len(_c.args) > 1 for _c in _calls_in([_d], 'print'))


def _one(_c):
    return 'space' if _c == ' ' else '`' + _c + '`'


def _gap(_p, _w):
    # The first difference between a printed line `_p` and the wanted line `_w`, told with the wanted line's own
    # words and marks only, never the student's text (2.11). Returns (sentence, kind, the extra character or '').
    _i = 0
    while _i < len(_p) and _i < len(_w) and _p[_i] == _w[_i]:
        _i += 1
    _P, _W = _p[_i:], _w[_i:]
    _b = _re.search(r'(\w+|[^\w\s])\s*$', _w[:_i])
    _prev = _b.group(1) if _b else ''
    _a = _re.match(r'\s*(\w+|[^\w\s])', _W)
    _next = _a.group(1) if _a else ''
    _s, _e = _i, _i
    while _s > 0 and _w[_s - 1].isalnum():
        _s -= 1
    while _e < len(_w) and _w[_e].isalnum():
        _e += 1
    _word = 'Write `' + _w[_s:_e] + '` exactly, letter for letter, capitals too.'
    if not _W:
        if len(_P) == 1 and not _P.isalnum():
            return 'There is an extra ' + _one(_P) + ' at the end.', 'extra', _P
        return 'The line should end right after `' + _prev + '`.', 'extra', ''
    if not _P:
        if len(_W) == 1:
            return 'The ' + _one(_W) + ' at the end is missing.', 'missing', ''
        return 'The line stops too soon: after `' + _prev + '` comes `' + _W.strip() + '`.', 'missing', ''
    if _i == 0:
        return 'Start the line with `' + _next + '`.', 'wrong', ''
    if _P[0].isalnum() and _W[0].isalnum():
        return _word, 'word', ''
    _cm, _cx, _cs = _edits(_P, _W[1:]), _edits(_P[1:], _W), _edits(_P[1:], _W[1:])
    if _cm <= _cx and _cm <= _cs:
        if _W[0].isalnum():
            return _word, 'word', ''
        return 'A ' + _one(_W[0]) + ' is missing right after `' + _prev + '`.', 'missing', ''
    if _cx <= _cs:
        if _P[0].isalnum():
            return 'There is something extra right after `' + _prev + '`.', 'extra', ''
        _where = ('right after `' + _prev + '`') if _W[0] == ' ' else ('before `' + _next + '`')
        return 'There is an extra ' + _one(_P[0]) + ' ' + _where + '.', 'extra', _P[0]
    return 'Right after `' + _prev + '` comes ' + ('a space' if _W[0] == ' ' else _one(_W[0])) + '.', 'wrong', ''


def _find(_name, _kept=False):
    _v = _g.get(_name)
    if type(_v).__name__ == 'function':
        return _v, ''
    if _name in _g:
        return None, ('`' + _name + '` is a box, made with `=`. A recipe is made with `def`: a line that starts `def '
                      + _name + '(`, with its steps indented under it.')
    _near = sorted(_k for _k, _x in list(_g.items()) if type(_x).__name__ == 'function' and not _k.startswith('_')
                   and _close(_k, _name, False))
    if _near:
        return None, 'Python matches names letter for letter: you wrote `' + _near[0] + '`, the task needs `' + _name + '`.'
    if _kept:
        return None, 'Keep the recipe `' + _name + '` from the starter, with its `def` line.'
    return None, 'Make a recipe named `' + _name + '`: a line that starts `def ' + _name + '(`.'


def _sig_msg(_name, _want, _have, _kept):
    _line = '`def ' + _name + '(' + ', '.join(_want) + '):`'
    if len(_have) != len(_want):
        _n = 'one ingredient' if len(_want) == 1 else str(len(_want)) + ' ingredients'
        return ('`' + _name + '` takes ' + _n + ': ' + _names(_want) + '. ' + ('Keep' if _kept else 'Write')
                + ' its first line as ' + _line + '.')
    return (('Keep the ingredient names from the starter: ' if _kept else 'Name the ingredients as the task says: ')
            + _line + '. Python matches names letter for letter.')


def _run(_f, _args, _rolls=None):
    _buf = _io.StringIO()
    _keep = _sys.stdout
    _calls = []
    _seq = list(_rolls or [])
    _real = _random.randint

    def _fake(_a, _b):
        _calls.append((_a, _b))
        if len(_seq) > 1:
            return _seq.pop(0)
        return _seq[0] if _seq else _a

    if _rolls is not None:
        _random.randint = _fake
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _f(*_args)
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _keep
        _random.randint = _real
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err, _calls


def _why(_f, _name, _args, _err, _foreign=(), _box=''):
    # A kind message for an error raised inside the student's recipe, while Mar'tu's check called it.
    _ps = _params(_f)
    _k = type(_err).__name__
    _s = str(_err)
    _ing = (("This recipe's ingredient" + ('s are ' if len(_ps) > 1 else ' is ') + _names(_ps) + '.') if _ps
            else 'This recipe has no ingredients.')
    _stop = _ev(_name, _args, 'Python stopped with a ' + _k)
    if _k in ('NameError', 'UnboundLocalError'):
        _x = getattr(_err, 'name', None) or ''
        if not _x:
            _m = _re.search(r"'(\w+)'", _s)
            _x = _m.group(1) if _m else ''
        if _x and set(_x) == {'_'}:
            return 'Fill in each blank `___` with an ingredient name from the `def` line. ' + _ing
        if _x == 'random':
            return 'Keep `import random` at the top, so Python knows where `random` comes from.' + _stop
        # The boxes this recipe makes (not its ingredients), worked out first: a name from an example on a `return`
        # line is answered with this recipe's own box, so `return result` after `fuel = ...` points at `fuel`.
        _d = _defs().get(_name)
        _own = [_y for _y in _made(_d) if _y not in _ps] if _d is not None else []
        _back = _d is not None and any(type(_n).__name__ == 'Return' and _n.value is not None and any(
            type(_y).__name__ == 'Name' and _y.id == _x for _y in _ast.walk(_n.value)) for _n in _ast.walk(_d))
        _fo = [_y for _y in _foreign if _y == _x] or [_y for _y in _foreign if len(_x) >= 3 and _edits(_y, _x) <= 2]
        if _fo:
            _here = ("This recipe's box is `" + _own[-1] + '`: hand that back.') if (_own and _back) else _ing
            return ('`' + _x + '` ' + ('comes from' if _fo[0] == _x else 'looks like `' + _fo[0] + '` from')
                    + " Mar'tu's example. " + _here)
        if [_p for _p in _ps if _close(_x, _p)]:
            return _ing + ' You wrote `' + _x + '`. Python matches names letter for letter.'
        _other = [_k for _k, _n in _defs().items() if _k != _name and _x in _made(_n)]
        _kitchen = ('`' + _x + '` is a box inside `' + _other[0] + '`, another recipe. It stays there. ') if _other else ''
        if not _box and _own and _back:
            _box = 'Hand back a box this recipe makes: ' + _names_of(_own) + '.'
        return ('Inside `' + _name + '`, Python found a name it does not know: `' + _x + '`. ' + _kitchen
                + (_box or _ing) + _stop)
    if _k == 'TypeError' and 'concatenate' in _s:
        return 'Glue a number to text with `str()`, like `str(' + (_ps[-1] if _ps else 'amount') + ')`.' + _stop
    if _k == 'TypeError' and 'positional argument' in _s:
        return 'A call inside `' + _name + '` hands over the wrong number of values. Count them against its `def` line.' + _stop
    if _k == 'RecursionError':
        return ('The recipe calls itself, again and again. Take the spaces off that call, so it sits at the bottom, '
                'outside the recipe.')
    if _k == 'AttributeError':
        return 'Python stopped: ' + _s + '. Check the name after the dot.' + _stop
    return 'Mend this, then Run again: ' + _k + ': ' + _s + _stop
'''.replace("__QUOTES__", repr(QUOTES_RULE))


# PAR / PAR-CONST on printed lines. Filled in by prints_check().
_PRINTS = r'''
_f, _m = _find(_name, _kept)
assert _f, _m
_ps = _params(_f)
assert _ps == _want_ps, _sig_msg(_name, _want_ps, _ps, _kept)


def _hit(_rows, _want):
    if _mode == 'number':
        return any(_re.search(_whole(_want), _r) for _r in _rows)
    return _want in [_r.replace('’', "'") for _r in _rows]


_g = _gamed(_name, [_x for _a, _w in _cases for _x in _a])
assert not _g, _g
_runs, _gave = [], []
for _args, _want in _cases:
    _val, _rows, _err, _c = _run(_f, _args)
    assert not _err, _why(_f, _name, _args, _err, _foreign, _box)
    _runs.append(_rows)
    _gave.append(_val)
_bad = [(_a, _w, _r) for (_a, _w), _r in zip(_cases, _runs) if not _hit(_r, _w)]
if _bad:
    _rs = _resets(_name)
    assert not _rs, _rs
    _quiet = [_i for _i, _r in enumerate(_runs) if not _r and _gave[_i] is not None]
    assert not _quiet, ('Show the line with `print(...)` inside the recipe. `return` hands it back to the call '
                        'without showing it.' + _ev(_name, _cases[_quiet[0]][0], 'it printed nothing'))
    # A quoted ingredient name shows as the word itself, unless the wanted line has that word too ("hours left.").
    _words = [_p for _p in _ps if any(_re.search(r'\b' + _p + r'\b', _r) for _r in _bad[0][2])
              and not _re.search(r'\b' + _p + r'\b', str(_bad[0][1]))]
    assert not _words, ('Take the quotes off `' + _words[0] + '`: with quotes, Python prints the word itself. '
                        + _QUOTES)
    if len(_runs) > 1 and _runs[0] and all(_r == _runs[0] for _r in _runs):
        _one = _runs[0][0]
        _said = ('both printed ' + _one if _re.fullmatch(r'-?\d+', _one) else
                 ('both printed `' + _one + '`') if _one in _safe else 'both printed the same line')
        assert False, (_cfix + " (Mar'tu's check called " + ' and '.join(_ct(_name, _a) for _a, _w in _cases)
                       + ', only inside the check: ' + _said + '.)')
    _a, _w, _r = _bad[0]
    assert _r, _fix + _ev(_name, _a, 'it printed nothing')
    _near = [_x.replace('’', "'") for _x in _r if all(str(_y) in _x for _y in _a)]
    if _mode == 'line' and _near:
        # Fix first: the first difference from the wanted line, in Mar'tu's values only, then the evidence.
        _say, _kind, _ch = _gap(min(_near, key=lambda _t: _edits(_t, _w)), _w)
        _lead = ('A comma inside `print(...)` adds a space. Glue with `+` instead. '
                 if _kind == 'extra' and _ch == ' ' and _spread(_name) else '')
        assert False, _lead + _say + _ev(_name, _a, 'it should print `' + _w + '`')
    _num =[_x for _x in _r if _re.fullmatch(r'-?\d+', _x)]
    assert False, _fix + _ev(_name, _a, ('it printed ' + _num[0] + ', but the answer is ' + str(_w)) if _num
                             else ('it did not print `' + str(_w) + '`'))
'''


def prints_check(label, name, params, cases, *, fix, const_fix=None, mode="line", foreign=(), safe=(), kept=True,
                 box=""):
    """PAR / PAR-CONST on what a recipe prints. cases = [(args, want), ...], fresh arguments the task never uses
    (lint b). mode "line": some printed line is exactly `want`; "number": a printed line shows `want` as a whole
    number. `safe` = printed lines a message may repeat (the task's own lines); any other line is described, never
    repeated (2.11). `foreign` = Mar'tu's example and Teach names (LEFT/RNM)."""
    const_fix = const_fix or ("A recipe gets its values when it is called: use " + _names_py(params) + ", not typed values.")
    code = _FN + (
        f"_name, _want_ps, _cases = {name!r}, {list(params)!r}, {[(tuple(a), w) for a, w in cases]!r}\n"
        f"_fix, _cfix, _mode = {fix!r}, {const_fix!r}, {mode!r}\n"
        f"_foreign, _safe, _box, _kept = {list(foreign)!r}, {list(safe)!r}, {box!r}, {kept!r}\n"
    ) + _PRINTS
    return (label, code)


# RET / RET-PARAM / PAR-CONST on what a recipe hands back. Filled in by returns_check().
_RETURNS = r'''
_f, _m = _find(_name, _kept)
assert _f, _m
_ps = _params(_f)
assert _ps == _want_ps, _sig_msg(_name, _want_ps, _ps, _kept)


def _safe_show(_v):
    _t = type(_v).__name__
    if _t in ('int', 'float', 'bool'):
        return str(_v)
    return {'str': 'some text', 'function': 'a recipe'}.get(_t, 'something else')


_g = _gamed(_name, [_x for _a, _w in _cases for _x in _a])
assert not _g, _g
_rs = _resets(_name)
_vals = []
for _args, _want in _cases:
    _val, _rows, _err, _c = _run(_f, _args)
    assert not _err, _why(_f, _name, _args, _err, _foreign, _box)
    assert not (_rs and not (_val == _want and type(_val) == type(_want))), _rs
    if _val is None:
        _num = [_x for _x in _rows if _re.fullmatch(r'-?\d+', _x)]
        assert not _rows, ('Hand the answer back with `return`. `print` only shows it on the screen.'
                           + _ev(_name, _args, ('it printed ' + _num[0] if _num else 'it printed a line')
                                 + ' but handed back `None`'))
        _dd = _defs().get(_name)
        _blank = _dd is not None and any(type(_n).__name__ == 'Return' and _n.value is None for _n in _ast.walk(_dd))
        assert not _blank, ('`return` on its own hands back nothing. Put the answer after it.'
                            + _ev(_name, _args, 'it handed back `None`'))
        assert False, _nfix + _ev(_name, _args, 'it handed back `None`')
    _vals.append(_val)
# `return "total"`: a box's name in quotes hands back the word itself (the quoted-name habit), not hard-coding.
_dq = _defs().get(_name)
_mine = set(_ps) | set(_made(_dq) if _dq is not None else [])
_qw = [(_a, _v) for (_a, _w), _v in zip(_cases, _vals) if type(_v).__name__ == 'str' and _v in _mine and _v != _w]
assert not _qw, ('Take the quotes off `' + str(_qw[0][1]) + '`: with quotes, the recipe hands back the word itself. '
                 'Quotes mean these exact letters.' + _ev(_name, _qw[0][0], 'it handed back the word `'
                                                           + str(_qw[0][1]) + '`'))
if len(_vals) > 1 and all(_v == _vals[0] and type(_v) == type(_vals[0]) for _v in _vals):
    assert False, (_cfix + " (Mar'tu's check called " + ' and '.join(_ct(_name, _a) for _a, _w in _cases)
                   + ', only inside the check: both gave back ' + _safe_show(_vals[0]) + '.)')
for (_args, _want), _val in zip(_cases, _vals):
    if _val == _want and type(_val) == type(_want):
        continue
    _got = _ev(_name, _args, 'it handed back ' + _safe_show(_val) + ', but the answer is ' + str(_want))
    assert not (type(_val).__name__ == 'str' and _val.strip() == str(_want)), (
        'Hand back the number itself, with no quotes and no `str()`.' + _got)
    for _test, _msg in _rules:
        assert not _test(_args, _val), _msg + _got
    _same = [_i for _i, _x in enumerate(_args) if _x == _val and type(_x) == type(_val)]
    assert not _same, ('Hand back the box the recipe works out, not `' + _ps[_same[0]] + '` as it came in.'
                       + _ev(_name, _args, 'it handed back ' + _safe_show(_val)))
    assert False, _fix + _got
'''


def returns_check(label, name, params, cases, *, fix, const_fix=None, none_fix=None, foreign=(), box="", rules=(),
                  kept=True):
    """RET / RET-PARAM / PAR-CONST / PNM / RNM on what a recipe hands back. cases = [(args, want), ...] with fresh
    arguments (lint b). rules = [(python test over _a (the args) and _v (the value), message), ...] for targeted
    slips, checked before the general `fix`. `box` = "This recipe's box is `total`." for the RNM message."""
    const_fix = const_fix or ("A recipe gets its numbers when it is called: work the answer out from "
                              + _names_py(params) + ".")
    none_fix = none_fix or "End the recipe with a `return` line that hands back the answer."
    rules_code = "[" + ", ".join(f"(lambda _a, _v: ({test}), {msg!r})" for test, msg in rules) + "]"
    code = _FN + (
        f"_name, _want_ps, _cases = {name!r}, {list(params)!r}, {[(tuple(a), w) for a, w in cases]!r}\n"
        f"_fix, _cfix, _nfix = {fix!r}, {const_fix!r}, {none_fix!r}\n"
        f"_foreign, _box, _kept = {list(foreign)!r}, {box!r}, {kept!r}\n"
        f"_rules = {rules_code}\n"
    ) + _RETURNS
    return (label, code)


def calls_check(label, name, at_least, *, fix, example=None, kept=True):
    """The program calls `name` at the top level at least `at_least` times. The recipe must exist first (a box made
    with `=` gets the DEF message); a bare name (no `()`) and a call indented inside its own recipe get their own
    messages."""
    example = example or f"{name}()"
    code = _FN + (
        f"_f, _m = _find({name!r}, {kept!r})\n"
        "assert _f, _m\n"
        f"_n = len(_calls_in(_top(), {name!r}))\n"
        f"_b = _bare({name!r})\n"
        f"assert not _b, ('Line ' + str(_b[0]) + ' says `' + {name!r} + '` with no `()`. No `()` means it is not called: '\n"
        f"                'write `' + {example!r} + '`.')\n"
        f"_w = _wrapped({name!r})\n"
        f"assert not _w, ('Line ' + str(_w[0]) + ' puts the call inside `print(...)`. `' + {name!r} + '` prints by itself, '\n"
        f"                'so write the call on its own: `' + {example!r} + '`. The extra `print` only adds `None`, '\n"
        "                'Python' + chr(39) + 's word for nothing.')\n"
        f"_d = _defs().get({name!r})\n"
        f"_in = [_c.lineno for _c in _calls_in([_d], {name!r})] if _d else []\n"
        f"assert _n >= {at_least} or not _in, ('Line ' + str(_in[0]) + ' is indented, so it sits inside the recipe as a '\n"
        "                                    'step, and nothing runs it. Take the spaces off, so the call is on its own '\n"
        "                                    'at the bottom.')\n"
        f"assert _n >= {at_least}, {fix!r}\n"
    )
    return (label, code)


LEDGER_ONLY = ("The ledger holds only your rows. Trace the program in your head or on paper, then type each "
               "number.")


def paste_stop(fn):
    """Hidden `setup` for a ledger: when the editor holds a `def`, a call to `fn` or a `print(`, the program is
    stopped before it runs (SystemExit, which the runner treats as the program ending), so a pasted program prints
    nothing and the console never shows the answer. The row checks then fail with the guard's own message. Code that
    does not parse runs as usual, so Python's own error shows."""
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


def row_check(label, name, want, rules, default):
    """The ledger (6A-06b): `name` holds `want`. rules = {wrong value: targeted message}. First, a guard: the editor
    holds only rows, so a pasted program (a `def`, a call to `ward_strength`, a `print(`) fails on every row."""
    code = (
        "import ast as _ast\n"
        "_ran = [_n for _n in _ast.walk(_ast.parse(_source)) if type(_n).__name__ == 'FunctionDef'\n"
        "        or (type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name'\n"
        "            and _n.func.id in ('ward_strength', 'print'))]\n"
        f"assert not _ran, {LEDGER_ONLY!r}\n"
        f"assert {name!r} in globals(), 'Keep the line `{name} = 0` from the starter, and change the 0.'\n"
        f"_v = globals()[{name!r}]\n"
        "assert type(_v).__name__ != 'str', ('Numbers don' + chr(39) + 't need quotes: write the number on its own, '\n"
        "                                    'like `" + name + " = 12`.')\n"
        f"_rules = {dict(rules)!r}\n"
        "_msg = ''\n"
        f"if not (_v == {want!r} and type(_v).__name__ == 'int'):\n"
        "    _msg = _rules.get(_v, '') if type(_v).__name__ == 'int' else ''\n"
        "    if not _msg and _v == 0:\n"
        f"        _msg = '`{name}` still holds the starter' + chr(39) + 's 0. ' + {default!r}\n"
        f"    _msg = _msg or {default!r}\n"
        "assert not _msg, _msg\n"
    )
    return (label, code)


# =============================================================================================
# UNIT (repeated in every part file of first-recipes; must match u03b exactly)
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

GLOSSARY = [
    dict(
        term="recipe",
        aliases=["recipes", "function", "functions"],
        plain=(
            "A named set of steps, made with `def`. Making a recipe does not run it. Calling its name with `()` runs "
            "the steps. Python calls a recipe a function."
        ),
        example='def say_steady():\n    print("Steady, now.")\n\nsay_steady()',
    ),
    dict(
        term="def",
        aliases=["def line"],
        plain=(
            "The word that makes a recipe: `def`, the recipe's name, brackets, and a colon. The steps go under it, "
            "indented. `def` never makes a box."
        ),
        example="def barrier_report():",
    ),
    dict(
        term="call",
        aliases=["calls", "calling", "called", "call it"],
        plain="Running a recipe: its name, then brackets. `say_steady()` runs the steps once. No brackets, no run.",
        example="say_steady()",
    ),
    dict(
        term="pass",
        plain=(
            "A line that does nothing. A recipe needs at least one line inside it, so `pass` holds the spot, like a "
            "blank recipe card, until you write a real step."
        ),
        example="def step_north():\n    pass",
    ),
    dict(
        term="parameter",
        aliases=["parameters", "ingredient", "ingredients"],
        plain=(
            "An ingredient's name on the recipe card, in the brackets on the `def` line. It is a box that gets "
            "filled each time the recipe is called."
        ),
        example="def warn(hero_name):",
    ),
    dict(
        term="argument",
        aliases=["arguments", "what you hand over"],
        plain="The value you hand over when you call a recipe. In `warn(\"Lucky\")`, the argument is `\"Lucky\"`.",
        example='warn("Lucky")',
    ),
    dict(
        term="return",
        aliases=["returns", "hands back", "hand back", "handed back", "return value"],
        plain=(
            "Hands a value back to the line that called the recipe, and ends the recipe. Catch it in a box, or it "
            "is gone: `lucky_max = max_mana_for(13)`."
        ),
        example="def max_mana_for(affinity):\n    total = affinity * 2\n    return total",
    ),
    dict(
        term="None",
        aliases=["NoneType"],
        plain="Python's word for nothing. A recipe with no `return` line hands back `None`.",
        example="print(lucky_max)   # None",
    ),
    dict(
        term=".capitalize()",
        aliases=["capitalize()", "capitalize"],
        plain="Makes a copy of the text with the first letter big and every other letter small.",
        example='"wELCOME".capitalize()   # Welcome',
    ),
]

# =============================================================================================
# Mar'tu remembers... (6a-remembers): Units 1-2 only, so the lesson stays portable
# =============================================================================================

REMEMBERS_6A = dict(
    kind="quiz",
    id="6a-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=1,
    summary="Two quick questions from earlier lessons. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 6A; recall from 2A (= versus ==) and 1C "
        "(mana = mana - 3). A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="mc",
            id="which-line-asks",
            q="Which line asks whether `roll` is 20?",
            choices=["roll = 20", "roll == 20"],
            answer=1,
            why_wrong={0: "`=` puts 20 in the box. Read it as gets: roll gets 20. It asks nothing."},
            explain="`==` asks: is the same as? `roll == 20` gives `True` or `False`. `=` puts a value in a box.",
        ),
        dict(
            type="predict",
            id="mana-minus-three",
            q="What will this print?",
            code="mana = 26\nmana = mana - 3\nprint(mana)\n",
            choices=["23", "26", "mana - 3", "an error"],
            answer="23",
            explain=(
                "Python works out the right side first: 26 - 3 is 23. Then `mana` gets 23. The box now holds the "
                "new value."
            ),
        ),
    ],
)

# =============================================================================================
# Lesson 6A "Recipes With Names"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 6A-01 box-or-recipe (moment: teacher-led, 5 minutes)
# ---------------------------------------------------------------------------------------------

STEADY_STARTER = (
    "# A box holds a value.\n"
    'steadying_words = "Steady, now."\n'
    "\n"
    "# A recipe holds steps.\n"
    "def say_steady():\n"
    '    print("Steady, now.")\n'
)
STEADY = "Steady, now."

_SAY_STEADY_CALLED = r'''
_f, _m = _find('say_steady', True)
assert _f, _m
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'say_steady', (), _err)
assert 'Steady, now.' in _rows, 'Keep the step inside the recipe as it is: `print("Steady, now.")`.'
assert 'Steady, now.' in _lines(), 'Call the recipe at the bottom, below the `def` block: `say_steady()`.'
'''

_SAY_IT_TWICE = r'''
_d = _defs().get('say_steady')
_inside = len(_calls_in([_d], 'print'))
_outside = sorted(set(_c.lineno for _c in _calls_in(_top(), 'print')))
assert _inside <= 1 and not _outside, ('Keep one `print`, inside the recipe, and call `say_steady()` twice instead. '
                                       'The recipe is the steps; each call runs them again.')
assert _lines().count('Steady, now.') >= 2, 'Call the recipe twice: two `say_steady()` lines at the bottom.'
'''

BOX_OR_RECIPE = dict(
    id="box-or-recipe",
    title="A box or a recipe?",
    martu=(
        "A [[variable|box]] holds a value. A [[recipe]] holds steps.\n"
        "`=` makes a box. [[def]] makes a recipe: `def`, a name, `()` and a colon. The steps go under it, "
        "indented.\n"
        "Making a recipe does not run it. Python reads it and remembers it. To run it, you [[call]] it: its name, "
        "then `()`.\n"
        "You have seen this at the cabin door, yes? `def move_left():` waited for the arrow key. Now you know why."
    ),
    introduces=["node:FunctionDef"],
    example='def hum():\n    print("Hmm.")\n\nhum()\n',
    example_output="Hmm.",
    names=["say_steady"],
    predict=dict(
        q="Before you press Run: what will this print?",
        code='def say_steady():\n    print("Steady, now.")\n\nprint("Oogrish waits.")\n',
        choices=["Oogrish waits.", "Steady, now.\nOogrish waits.", "Steady, now.", "an error"],
        answer=0,
        explain=(
            "Only `Oogrish waits.` The `def` block makes the recipe, and Python remembers it. Nothing inside runs, "
            "because no line calls `say_steady()`.\n"
            "Run the starter: it prints nothing at all, for the same reason."
        ),
    ),
    starter=STEADY_STARTER,
    checkpoints=[
        dict(
            id="call-the-recipe",
            text="Call the recipe: add `say_steady()` at the bottom.",
            dictated=True,
            hints=[
                "Nothing calls the recipe yet, so its step never runs. Where does a recipe get called? Below its "
                "`def` block, on a line of its own.",
                "A name with `()` after it runs that recipe. If `def hum():` makes a recipe, then `hum()` on its "
                "own line runs it.",
                "Write `say_steady()` on a new line at the bottom, with no spaces in front.",
            ],
            checks=[
                calls_check("the recipe is called", "say_steady", 1,
                            fix="Call the recipe: add `say_steady()` at the bottom, with no spaces in front. Nothing "
                                "calls it yet, so its step never runs."),
                ("the call prints Steady, now.", _FN + _SAY_STEADY_CALLED),
            ],
            pass_line="Oogrish: Steady, now.",
        ),
        dict(
            id="say-it-twice",
            text="Make it say it twice, using two calls, not two `print`s.",
            dictated=True,
            hints=[
                "The recipe already holds the step. You only need to run it again.",
                "Each call runs the whole recipe again:\n```python\nhum()\nhum()\n```\nprints `Hmm.` twice, from one "
                "`print`.",
                "Write a second `say_steady()` on the line under your first call.",
            ],
            checks=[
                ("one print, inside the recipe", _FN + _SAY_IT_TWICE),
                calls_check("the recipe is called twice", "say_steady", 2,
                            fix="Call the recipe twice: a second `say_steady()` line at the bottom."),
            ],
            pass_line="Oogrish: Steady, now. Steady, now. Yes, I heard myself.",
        ),
    ],
    solution=STEADY_STARTER + "\nsay_steady()\nsay_steady()\n",
    partials=[STEADY_STARTER + "\nsay_steady()\n"],
    assemble=dict(
        lines=['steadying_words = "Steady, now."', "def say_steady():", '    print("Steady, now.")', "say_steady()",
               "say_steady()"],
        distractors=["say_steady", 'def ("say_steady")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Box and card side by side",
            text=(
                "```text\nbox:    name = value\n        holds one value\n\nrecipe: def name():\n            step\n"
                "        holds steps\n\ncall:   name()\n        runs the steps\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="A jar and a recipe card",
            text=(
                "A jar holds one thing: sugar. A recipe card holds steps: mix, stir, bake. Writing the card bakes "
                "nothing. You bake when you follow the card. `say_steady()` is following the card."
            ),
        ),
        dict(
            angle="step-by-step",
            label="What Python does",
            text=(
                "1. `steadying_words = ...`: Python makes the box.\n"
                "2. `def say_steady():`: Python reads the recipe and remembers it. It runs nothing.\n"
                "3. The end of the file. Nothing called the recipe, so nothing printed.\n"
                "4. Add `say_steady()`: now Python runs the recipe's step, and `Steady, now.` prints."
            ),
        ),
        dict(
            angle="contrast",
            label="Not this",
            text=(
                "Not this: `def (\"mana\")`. `def` never makes a box. A box is `mana = 20`. A recipe is "
                "`def say_steady():` with its steps indented under it."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "At the cabin door, `def move_left():` made a recipe. The game called `move_left()` when you pressed "
                "the left arrow. No arrow, no call, no step. Same here: no `say_steady()`, no words."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "My recipes sit in a book on the mantle. They do nothing there. Only when someone reads one out loud "
                "does anything happen."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Recipes can call recipes. Write `say_ready()`: it prints a line of its own, then calls `say_steady()`. "
            "Call `say_ready()` at the bottom."
        ),
        hints=[
            "Two indented steps: a `print` line, then `say_steady()`.",
            "Write `def say_ready():`, then the two indented steps under it. Call `say_ready()` at the bottom.",
        ],
        checks=[
            (
                "say_ready prints a line, then calls say_steady",
                _FN + r'''
_f, _m = _find('say_ready')
assert _f, _m
assert _calls_in([_defs().get('say_ready')], 'say_steady'), (
    'Inside `say_ready`, call `say_steady()` after its own `print` line.')
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'say_ready', (), _err)
assert len(_rows) >= 2 and _rows[-1] == 'Steady, now.', (
    'Make `say_ready()` print its own line first, then call `say_steady()`, so `Steady, now.` comes last.')
assert _calls_in(_top(), 'say_ready'), 'Call it at the bottom: `say_ready()`.'
''',
            ),
        ],
        solution=STEADY_STARTER + (
            "\ndef say_ready():\n"
            '    print("Oogrish lifts his cane.")\n'
            "    say_steady()\n"
            "\nsay_steady()\nsay_steady()\nsay_ready()\n"
        ),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='def move_left():\n    pass',
        why=(
            "You have seen this at the cabin door. Each `def` line made a recipe. The game called `move_left()` "
            "when you pressed the left arrow. Making the recipe never moved the party: only the call did."
        ),
    ),
    takeaway="`=` makes a box. `def` makes a recipe. Making it runs nothing; `name()` calls it.",
    wrong_answers=[
        dict(why="the name with no () (A-02's shape-without-meaning; nothing runs)",
             code=STEADY_STARTER + "\nsay_steady\n", fails_at=1, message_contains="`()`"),
        dict(why="the step typed at the top level instead of a call",
             code=STEADY_STARTER + '\nprint("Steady, now.")\n', fails_at=1, message_contains="Call the recipe"),
        dict(why="the call indented under the def (it becomes a step; nothing runs)",
             code=STEADY_STARTER + "    say_steady()\n", fails_at=1, message_contains="indented"),
        dict(why="called before it is defined (order matters)",
             code="say_steady()\n" + STEADY_STARTER, fails_at=0, message_contains="not defined"),
        dict(why="= used to make the recipe (a box, not a recipe)",
             code='steadying_words = "Steady, now."\nsay_steady = "Steady, now."\nprint(say_steady)\n',
             fails_at=1, message_contains="box"),
        dict(why="def used to make a box (A-02's def-with-quotes box; the contrast angle shows an invented one)",
             code='def steadying_words = "Steady, now."\n', fails_at=0, message_contains="expected '('"),
        dict(why="the recipe's name in quotes after def (`def (\"say_steady\"):`; the explainer's quoted-recipe-name row, "
                 "never 'make a box')",
             code=STEADY_STARTER.replace("def say_steady():", 'def ("say_steady"):') + "\nsay_steady()\nsay_steady()\n",
             fails_at=0, message_contains="invalid syntax"),
        dict(why="= used to make the recipe, then called (a box called: the explainer names the box and the recipe's def)",
             code='steadying_words = "Steady, now."\nsay_steady = "Steady, now."\nsay_steady()\n', fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="two prints and one call (CP2)",
             code=STEADY_STARTER + '    print("Steady, now.")\n\nsay_steady()\n', fails_at=2, message_contains="call"),
        dict(why="one call plus a top-level print (CP2)",
             code=STEADY_STARTER + '\nsay_steady()\nprint("Steady, now.")\n', fails_at=2, message_contains="call"),
        dict(why="the call wrapped in print(): the recipe prints, then the outer print adds None",
             code=STEADY_STARTER + "\nprint(say_steady())\n", fails_at=1, message_contains="on its own"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="def-call", solo="false", dictates="1,2", foreign_names="hum",
             stages="P,R,I,M", moment="teacher-led, 5 min",
             trace="static step table (another_way step-by-step: the def is read and remembered, nothing runs)")
        + "\n"
        "The predict ends with a visible line (`Oogrish waits.`) because a predict choice must be exactly what the "
        "console shows; the starter itself prints nothing (the explain says so). Investigate = run the starter and "
        "see nothing. CP2 counts prints inside say_steady and at the top level only, so Lucky's side quest (a "
        "second recipe with its own print) keeps CP2 green. WA evidence: A-02's def-with-quotes box (the DEF row; the "
        "contrast angle shows an invented `def (\"mana\")`, never the sheet's own value, privacy rule T10); no `()`; "
        "call before def; `=` used to make a recipe."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-02 call-it
# ---------------------------------------------------------------------------------------------

REPORT_STARTER = (
    "def barrier_report():\n"
    '    print("Barrier\'s holding.")\n'
    "    # add a second line here\n"
    "\n"
    "# call barrier_report here\n"
)
REPORT_SOLUTION = (
    "def barrier_report():\n"
    '    print("Barrier\'s holding.")\n'
    '    print("Visor dims. All clear.")\n'
    "\n"
    "barrier_report()\n"
)

_REPORT = r'''
_f, _m = _find('barrier_report', True)
assert _f, _m
_v, _rows, _err, _c = _run(_f, ())
# A top-level print is the slip only while the recipe itself still prints fewer than two lines; a `print` wrapped
# around the call is left to the call check, which says so.
_out = sorted(set(_c.lineno for _c in _calls_in(_top(), 'print') if not _calls_in([_c], 'barrier_report')))
assert not (_out and len(_rows) < 2), ('Line ' + str(_out[0]) + ' runs on its own, outside the recipe. Indent it '
                                       'four spaces, under `def barrier_report():`, so it belongs to the recipe.')
'''

_REPORT_LINES = r'''
_f, _m = _find('barrier_report', True)
assert _f, _m
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'barrier_report', (), _err)
assert len(_rows) >= 2, ('Add a second `print` line inside the recipe, indented like the first.'
                         + _ev('barrier_report', (), 'it printed ' + str(len(_rows)) + ' line'))
assert all(_r in _lines() for _r in _rows), 'Call the recipe at the bottom, so its lines print: `barrier_report()`.'
'''

CALL_IT = dict(
    id="call-it",
    title="Call it",
    martu=(
        "The lines [[indent|indented]] under `def` are the recipe's steps. They belong to it. They run only when "
        "the recipe is called, and they run together, top to bottom.\n"
        "Give Gearshift's report a second line. Then call it.\n"
        "A recipe needs at least one step inside. An empty one makes Python stop."
    ),
    example='def tidy():\n    print("Sweep.")\n    print("Dust.")\n\ntidy()\n',
    example_output="Sweep.\nDust.",
    names=["barrier_report"],
    pick="Visor dims. All clear.",
    predict=dict(
        q="One click: what will this print? Look closely at line 4.",
        code='def barrier_report():\n    print("Barrier\'s holding.")\n\nbarrier_report\nprint("Report done.")\n',
        choices=["Report done.", "Barrier's holding.\nReport done.", "an error"],
        answer=0,
        explain=(
            "Only `Report done.` Line 4 names the recipe but has no `()`, so it does not call it. No `()`, no run, "
            "and no error either: Python just looks at the name and moves on."
        ),
    ),
    starter=REPORT_STARTER,
    checkpoints=[
        dict(
            id="second-line-and-call",
            text="Add a second line inside the recipe, then call it.",
            dictated=False,
            hints=[
                "Two jobs: a second indented line inside `def barrier_report():`, then a call at the bottom with no "
                "spaces in front.",
                "Indented lines belong to the recipe:\n```python\ndef tidy():\n    print(\"Sweep.\")\n"
                "    print(\"Dust.\")\n\ntidy()\n```\nOne call runs both lines.",
                "Write a second `print(...)` line under the first one, four spaces in. Then write "
                "`barrier_report()` at the bottom, with no spaces in front.",
            ],
            checks=[
                ("every print is inside the recipe", _FN + _REPORT),
                calls_check("the recipe is called", "barrier_report", 1,
                            fix="Now call the recipe: add `barrier_report()` at the bottom, with no spaces in front."),
                ("one call prints two lines", _FN + _REPORT_LINES),
            ],
            pass_line="Gearshift: Report sent. Barrier's holding.",
        ),
    ],
    solution=REPORT_SOLUTION,
    assemble=dict(
        lines=["def barrier_report():", '    print("Barrier\'s holding.")', '    print("Visor dims. All clear.")',
               "barrier_report()"],
        distractors=['print("Visor dims. All clear.")', "barrier_report"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The indent means: belongs to the recipe",
            text=(
                "1. `def barrier_report():` starts the recipe.\n"
                "2. Every line under it with four spaces in front is a step of that recipe.\n"
                "3. The first line with no spaces ends the recipe.\n"
                "4. `barrier_report()` with no spaces runs all the steps, top to bottom."
            ),
        ),
        dict(
            angle="picture",
            label="Inside and outside",
            text=(
                "```text\ndef barrier_report():\n    step 1   <- inside\n    step 2   <- inside\n\n"
                "barrier_report()  <- outside:\n                     the call\n```"
            ),
        ),
        dict(
            angle="shorter",
            text="Steps: indented under `def`. The call: no spaces, with `()`.",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants numbers. Make a box `hours_left = 37` above the recipe. Then add a step that prints the "
            "hours left, glued in with `str()`."
        ),
        hints=[
            "Make the box first, above the `def` line. Then add one more `print` inside the recipe.",
            "Write `hours_left = 37` above the recipe. Inside it, add "
            "`print(\"Hours left: \" + str(hours_left))`.",
        ],
        checks=[
            (
                "the report shows the hours from the box",
                _FN + r'''
_f, _m = _find('barrier_report', True)
assert _f, _m
_G = _f.__globals__
assert type(_G.get('hours_left')).__name__ == 'int', 'Make a box above the recipe: `hours_left = 37`.'
_old = _G['hours_left']
_G['hours_left'] = 99
try:
    _v, _rows, _err, _c = _run(_f, ())
finally:
    _G['hours_left'] = _old
assert not _err, _why(_f, 'barrier_report', (), _err)
assert any(_re.search(_whole(99), _r) for _r in _rows), (
    'Inside the recipe, print the hours from the box: glue `str(hours_left)` to some words. '
    "(Mar'tu's check set `hours_left = 99`, only inside the check: the report did not show 99.)")
''',
            ),
        ],
        solution=(
            "hours_left = 37\n\n"
            "def barrier_report():\n"
            '    print("Barrier\'s holding.")\n'
            '    print("Visor dims. All clear.")\n'
            '    print("Hours left: " + str(hours_left))\n'
            "\nbarrier_report()\n"
        ),
    ),
    takeaway="Indented lines are the recipe's steps. `name()` at the bottom runs them all.",
    wrong_answers=[
        dict(why="an empty body: the starter's print deleted, only a comment left",
             code="def barrier_report():\n    # add a second line here\n\nbarrier_report()\n",
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the second print not indented (it runs without the recipe)",
             code='def barrier_report():\n    print("Barrier\'s holding.")\nprint("Visor dims.")\n\nbarrier_report()\n',
             fails_at=1, message_contains="outside the recipe"),
        dict(why="second line added, never called (defining is not calling)",
             code='def barrier_report():\n    print("Barrier\'s holding.")\n    print("Visor dims.")\n',
             fails_at=1, message_contains="call"),
        dict(why="called with no ()",
             code='def barrier_report():\n    print("Barrier\'s holding.")\n    print("Visor dims.")\n\nbarrier_report\n',
             fails_at=1, message_contains="`()`"),
        dict(why="called, but no second line",
             code='def barrier_report():\n    print("Barrier\'s holding.")\n\nbarrier_report()\n',
             fails_at=1, message_contains="second"),
        dict(why="the call indented inside the recipe",
             code='def barrier_report():\n    print("Barrier\'s holding.")\n    print("Visor dims.")\n    barrier_report()\n',
             fails_at=1, message_contains="indented"),
        dict(why="the call wrapped in print() (the old check said 'indent it', which would make the recipe call itself)",
             code='def barrier_report():\n    print("Barrier\'s holding.")\n    print("Visor dims.")\n\nprint(barrier_report())\n',
             fails_at=1, message_contains="on its own"),
        dict(why="= used to make the recipe (a box holding the words, not a recipe)",
             code='barrier_report = "Barrier\'s holding."\nprint(barrier_report)\n', fails_at=1, message_contains="box"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="def-call", solo="false", dictates="", foreign_names="tidy",
             stages="M,I") + "\n"
        "Investigate (barrier_report with no () does nothing) is the one-click predict. The empty-body WA proves the "
        "IndentationError row ('A recipe needs at least one line inside it'). The first check flags a top-level "
        "print only while the recipe itself prints fewer than two lines, so the unindented second line gets "
        "'outside the recipe' but an extra `print` after a correct call stays green. A `print(...)` wrapped around "
        "the call is left to the call check ('write the call on its own'): telling that student to indent it would "
        "make the recipe call itself. Lucky's side quest adds a box, not a print, so it stays green."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-03 replace-pass (rehearsal: program-movement)
# ---------------------------------------------------------------------------------------------

# The scout records each step and says it, like the party moving on the map.
SCOUT_SETUP = (
    "class Scout:\n"
    "    def __init__(self):\n"
    "        self.steps = []\n"
    "    def step(self, direction):\n"
    "        self.steps.append(direction)\n"
    "        print('The scout steps ' + str(direction) + '.')\n"
    "scout = Scout()\n"
)
DIRS = ["north", "south", "east", "west"]
ROUTE = "# Mar'tu's map calls your recipes, like the arrow keys did:\nstep_north()\nstep_south()\nstep_east()\nstep_west()\n"


def _scout_code(done=(), body=None, route=ROUTE, comments=True):
    """The four recipes in order; directions in `done` get their step, the rest keep `pass`.
    body = {direction: line} overrides a recipe's line."""
    out = ""
    for i, d in enumerate(DIRS, 1):
        if comments:
            tail = ', like scout.step("north").' if d == "north" else "."
            out += f"# {i}. Replace pass with a command that moves the scout {d}{tail}\n"
        line = (body or {}).get(d, f'scout.step("{d}")' if d in done else "pass")
        out += f"def step_{d}():\n    {line}\n\n"
    return out + route


SCOUT_STARTER = _scout_code()
SCOUT_SOLUTION = _scout_code(done=DIRS)

_SCOUT = r'''
_d = __DIR__
_name = 'step_' + _d
_f, _m = _find(_name, True)
assert _f, _m
_sc = _f.__globals__['scout']
_at = len(_sc.steps)
_v, _rows, _err, _c = _run(_f, ())
if _err and type(_err).__name__ == 'NameError':
    assert False, ('Put the direction in quotes: `scout.step("' + _d + '")`. ' + _QUOTES)
assert not (_err and type(_err).__name__ == 'AttributeError'), (
    'The scout moves with `scout.step(...)`. Write `scout.step("' + _d + '")`.')
assert not _err, _why(_f, _name, (), _err)
_new = _sc.steps[_at:]
assert _new, ('Replace `pass` in `' + _name + '` with `scout.step("' + _d + '")`, indented under the `def` line.'
              + _ev(_name, (), 'the scout did not move'))
assert len(_new) == 1, 'One step per call: `' + _name + '` should hold one `scout.step("' + _d + '")` line.'
_s = _new[0]
assert not (type(_s).__name__ == 'str' and _s != _d and _s.lower() == _d), (
    'Capitals count: write `"' + _d + '"`, all small letters. ' + _QUOTES)
assert _s == _d, ('Use the direction in the recipe' + chr(39) + 's name: `scout.step("' + _d + '")`.'
                  + _ev(_name, (), 'the scout stepped ' + (_s if _s in ('north', 'south', 'east', 'west') else 'somewhere else')))
'''


def scout_check(direction):
    return (f"step_{direction} moves the scout {direction}", _FN + _SCOUT.replace("__DIR__", repr(direction)))


def _scout_cp(direction, index):
    # CP1 is dictated with the example; CP2-3 are terse ("the same way"); CP4 is the student's own (G3-12). All four
    # tick on one Run, so the fast group loses no time.
    teach = ("`pass` is a blank recipe card. Replace it with one real step, four spaces in, where `pass` was. "
             + QUOTES_RULE + " The direction is a word, so it gets quotes.")
    if direction == "north":
        text = 'Replace `pass` in `step_north` with a command that moves the scout north, like `scout.step("north")`.'
        hints = [
            "Which word in the recipe's name says where to go? Put that word in quotes inside the brackets.",
            teach,
            "Write `scout.step(\"north\")` in place of `pass`, four spaces in.",
        ]
    elif direction == "west":
        text = "Now `step_west`, on your own."
        hints = [
            "Read the recipe's name: `step_west`. Its last word says which way the scout goes.",
            teach,
            "Write `scout.step(\"west\")` in place of `pass`, four spaces in.",
        ]
    else:
        text = f"Now `step_{direction}`: replace its `pass` the same way."
        hints = [
            "Which word in the recipe's name says where to go? Put that word in quotes inside the brackets.",
            teach,
            f"Write `scout.step(\"{direction}\")` in place of `pass`, four spaces in.",
        ]
    return dict(
        id=f"step-{direction}",
        text=text,
        dictated=direction != "west",
        hints=hints,
        checks=[scout_check(direction)],
        pass_line={"north": "Bomb Shell: Scout's moving.", "south": "Bomb Shell: South. Good.",
                   "east": "Bomb Shell: East. Clear.", "west": "Lucky: Finally. Can we go home now?"}[direction],
    )


REPLACE_PASS = dict(
    id="replace-pass",
    title="Replace pass",
    martu=(
        "Each `def` line makes a recipe: a named set of steps. [[pass]] means do nothing. It is a blank recipe "
        "card.\n"
        "The scout moves with `scout.step(\"north\")`. Replace each `pass` with the step its name asks for, four "
        "spaces in, where `pass` was.\n"
        "My map calls your four recipes at the bottom, like the arrow keys did. Follow the numbered comments, one "
        "per step."
    ),
    introduces=["node:Pass"],
    setup=SCOUT_SETUP,
    names=["step_north", "step_south", "step_east", "step_west", "scout"],
    starter=SCOUT_STARTER,
    checkpoints=[_scout_cp(d, i) for i, d in enumerate(DIRS, 1)],
    solution=SCOUT_SOLUTION,
    partials=[_scout_code(done=DIRS[:k]) for k in (1, 2, 3)],
    assemble=dict(
        lines=[part for d in DIRS for part in (f"def step_{d}():", f'    scout.step("{d}")')]
        + ["step_north()", "step_south()", "step_east()", "step_west()"],
        distractors=["    scout.step(north)", '    scout.step("North")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="A map with four arrows",
            text=(
                "```text\n         north\n           ^\n west  <  scout  >  east\n           v\n         south\n```\n"
                "Each recipe's name says which arrow. Its step moves the scout that way."
            ),
        ),
        dict(
            angle="in Tor",
            label="A blank card",
            text=(
                "`pass` is a blank recipe card. The card has a name, `step_north`, but no steps yet. Write the one "
                "step it needs."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Find `pass` under `def step_north():`.\n"
                "2. Delete the word `pass`, and keep the four spaces.\n"
                "3. Type `scout.step(\"north\")` there.\n"
                "4. Run. The map calls the recipe, and the scout steps north. Then do the next one."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Module 1, the cabin door: `def move_left():` held `pass`, and you wrote `party.move(\"left\")`. "
                "This is the same job, with the scout instead of the party."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Lucky hates walking. Add `step_twice_north()`, a recipe that calls `step_north()` twice. Call it at the bottom.",
        hints=[
            "Two indented steps, each one `step_north()`.",
            "Write `def step_twice_north():` with two indented `step_north()` lines under it. Then call "
            "`step_twice_north()` at the bottom.",
        ],
        checks=[
            (
                "step_twice_north calls step_north twice",
                _FN + r'''
_f, _m = _find('step_twice_north')
assert _f, _m
assert len(_calls_in([_defs().get('step_twice_north')], 'step_north')) >= 2, (
    'Inside `step_twice_north`, call your recipe `step_north()` twice, one line each.')
_sc = _f.__globals__['scout']
_at = len(_sc.steps)
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'step_twice_north', (), _err)
assert _sc.steps[_at:] == ['north', 'north'], 'Make `step_twice_north()` move the scout north, then north again.'
''',
            ),
        ],
        solution=SCOUT_SOLUTION + "\ndef step_twice_north():\n    step_north()\n    step_north()\n\nstep_twice_north()\n",
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-movement",
        snippet='def move_left():\n    party.move("left")',
        why=(
            "You have seen this at the cabin door. `move_left()` was a recipe with `pass` inside, and the arrow key "
            "called it. You replaced `pass` with `party.move(\"left\")`. Same move today, with the scout."
        ),
    ),
    takeaway="`pass` holds the spot. Replace it with a real step, indented where `pass` was.",
    wrong_answers=[
        dict(why="the direction unquoted: scout.step(north) (a NameError when the map calls it)",
             code=_scout_code(done=DIRS, body={"north": "scout.step(north)"}), fails_at=0, message_contains="'north'"),
        dict(why="pass deleted and nothing written yet (a recipe with no steps: the explainer states the rule, never "
                 "'indent the next line')",
             code=SCOUT_STARTER.replace("def step_north():\n    pass\n", "def step_north():\n\n", 1), fails_at=0,
             message_contains="expected an indented block after function definition on line 2"),
        dict(why="only a note left in the recipe (a comment is not a step)",
             code=_scout_code(body={"north": "# move north"}), fails_at=0,
             message_contains="expected an indented block after function definition on line 2"),
        dict(why="all four recipes step north (copy-paste)",
             code=_scout_code(body={d: 'scout.step("north")' for d in DIRS}), fails_at=2, message_contains="north"),
        dict(why="the step not indented",
             code=_scout_code(done=DIRS).replace('def step_north():\n    scout.step("north")',
                                                 'def step_north():\nscout.step("north")'),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="a capital letter in the direction",
             code=_scout_code(done=DIRS, body={"north": 'scout.step("North")'}), fails_at=1, message_contains="Capitals"),
        dict(why="the campaign's party.move copied (no party here)",
             code=_scout_code(done=DIRS, body={"north": 'party.move("north")'}), fails_at=0, message_contains="party"),
        dict(why="scout.move instead of scout.step",
             code=_scout_code(done=DIRS, body={"north": 'scout.move("north")'}), fails_at=0, message_contains="move"),
        dict(why="the step put below the recipe at the top level, pass left in place",
             code=_scout_code(done=DIRS[1:]).replace("def step_north():\n    pass\n",
                                                     'def step_north():\n    pass\nscout.step("north")\n'),
             fails_at=1, message_contains="did not move"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="replace-pass,def-call", solo="false", dictates="1,2,3",
             foreign_names="move_left,party", rehearsal="program-movement",
             twin="turn_left() / turn_right() with scout.turn(\"left\")") + "\n"
        "Rehearsal: numbered comments map 1:1 onto the checkpoints (the campaign's four arrow-key recipes). CP1 is "
        "dictated with the `scout.step(\"north\")` example; CP2-3 are terse (\"the same way\"); CP4 is the student's "
        "own (dictated=False; its Where to look names the recipe's name, not the code). All four tick on one Run (G3-12). The "
        "starter ends with the map's four calls (the campaign's game called the recipes for you), so Run shows the "
        "scout's steps. CALL: each check calls one recipe with its prints kept private and reads the scout's "
        "record. engine is off: `party.move` is a real NameError here (WA). Assemble distractors: the unquoted and "
        "capital-N lines (a correct line can't be a distractor). Under 'Show me more' this A-stage exercise is "
        "Assemble-first (C4)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-04 ingredients
# ---------------------------------------------------------------------------------------------

WARN_STARTER = (
    "def warn(hero_name):\n"
    '    # print the hero, then ", get inside!"\n'
    "    pass\n"
    "\n"
    'warn("Lucky")       # should show: Lucky, get inside!\n'
    'warn("Bomb Shell")  # should show: Bomb Shell, get inside!\n'
)
WARN_LINE = '    print(hero_name + ", get inside!")\n'
WARN_CALLS = 'warn("Lucky")\nwarn("Bomb Shell")\n'
WARN_SOLUTION = "def warn(hero_name):\n" + WARN_LINE + "\n" + WARN_CALLS + 'warn("Captain Glug")\n'
WARN_SAFE = ["Lucky, get inside!", "Bomb Shell, get inside!"]


def _warn(line=WARN_LINE, calls=WARN_CALLS, extra='warn("Captain Glug")\n'):
    return "def warn(hero_name):\n" + line + "\n" + calls + extra


_THIRD_WARN = r'''
_ends = [_l for _l in _lines() if _l.endswith(', get inside!')]
assert len(_ends) >= 3, ('Each call should show its hero with `, get inside!`. Keep the two calls, and add yours '
                         'below them.')
'''

INGREDIENTS = dict(
    id="ingredients",
    title="Ingredients",
    martu=(
        "Some recipes need an ingredient. Its name goes in the brackets on the `def` line: a [[parameter]].\n"
        "When you call the recipe, you hand over a real value: an [[argument]]. For that one call, Python puts it "
        "in the parameter, like a box.\n"
        "The Example hands over two names, one per call. Same recipe, a different hero each time.\n"
        "My check also calls `warn` with heroes you never wrote, like `warn(\"Tester\")`. One line inside must work "
        "for every hero."
    ),
    example='def cheer(name):\n    print(name + " is ready.")\n\ncheer("Oogrish")\ncheer("Gearshift")\n',
    example_output="Oogrish is ready.\nGearshift is ready.",
    names=["warn", "hero_name"],
    pick="Captain Glug",
    predict=dict(
        q="`hero_name` is a box that the call fills. What will this print?",
        code='def warn(hero_name):\n    print(hero_name)\n\nwarn("Lucky")\n',
        choices=["Lucky", "hero_name", "(nothing at all)"],
        answer=0,
        explain=(
            "`Lucky`. The call `warn(\"Lucky\")` hands over `\"Lucky\"`, and Python puts it in `hero_name` for this "
            "call. `print(hero_name)` has no quotes, so it looks inside the box."
        ),
    ),
    pair_talk=(
        "Pair talk: tell your partner what `hero_name` holds in the first call, and what it holds in the second. "
        "Then each of you finishes `warn` on your own screen."
    ),
    starter=WARN_STARTER,
    checkpoints=[
        dict(
            id="both-heroes",
            text="Finish `warn` so both calls show their own hero.",
            dictated=False,
            hints=[
                "What did each call hand over? Inside the recipe, that value lives in `hero_name`.",
                "In the Example, `cheer(\"Oogrish\")` puts `\"Oogrish\"` in `name`. Then `name + \" is ready.\"` glues "
                "the name to the words.",
                QUOTES_RULE + " So `hero_name` has no quotes, and `\", get inside!\"` has them.",
                "Write `print(hero_name + \", get inside!\")` in place of `pass`, four spaces in.",
            ],
            checks=[
                prints_check("each call shows its own hero", "warn", ["hero_name"],
                             [(("Tester",), "Tester, get inside!"), (("Moth",), "Moth, get inside!")],
                             fix="Use the ingredient `hero_name` in the `print` line, so each call shows its own hero.",
                             const_fix="A recipe gets its hero when it is called: use `hero_name`, not a typed name.",
                             foreign=["cheer", "name", "greet", "guest"], safe=WARN_SAFE),
            ],
            pass_line="Lucky: Fine. I'm getting inside. But I'm keeping track.",
        ),
        dict(
            id="your-own-hero",
            text="Add a third call for your own hero.",
            dictated=False,
            hints=[
                "Copy the shape of the two calls above. Put your hero in quotes.",
                "Every call hands over one value: `cheer(\"Pip\")` would show `Pip is ready.`",
                "Write `warn(\"Captain Glug\")` on a new line at the bottom, or any hero of your own, in quotes.",
            ],
            checks=[
                calls_check("warn is called three times", "warn", 3,
                            fix="Add a third call at the bottom for your own hero: `warn(`, a name in quotes, then `)`.",
                            example='warn("...")'),
                ("three warnings print", _FN + _THIRD_WARN),
            ],
            pass_line="Lucky: Another one inside? Fine. Budge up.",
        ),
    ],
    solution=WARN_SOLUTION,
    partials=["def warn(hero_name):\n" + WARN_LINE + "\n" + WARN_CALLS],
    assemble=dict(
        lines=["def warn(hero_name):", '    print(hero_name + ", get inside!")', 'warn("Lucky")', 'warn("Bomb Shell")',
               'warn("Captain Glug")'],
        distractors=['    print("Lucky, get inside!")', '    print("hero_name, get inside!")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The call table",
            text=(
                "```text\ncall                hero_name\nwarn(\"Lucky\")       \"Lucky\"\n"
                "warn(\"Bomb Shell\")  \"Bomb Shell\"\n```\n"
                "One recipe. Each call fills `hero_name` with something new."
            ),
        ),
        dict(
            angle="everyday",
            label="A fill-in card",
            text=(
                "A fill-in card says: \"____, get inside!\" Each time you read it out, you put a different name in "
                "the blank. `hero_name` is that blank, with a name of its own."
            ),
        ),
        dict(
            angle="from what you know",
            label="It is a box",
            text=(
                "`hero_name` is a box, like the boxes from Unit 1. The call fills it. `warn(\"Lucky\")` works like "
                "`hero_name = \"Lucky\"`, just before the recipe's steps run."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `warn(\"Lucky\")`: `hero_name` gets `\"Lucky\"`.\n"
                "2. The step runs: `hero_name + \", get inside!\"` is `Lucky, get inside!`\n"
                "3. `warn(\"Bomb Shell\")`: `hero_name` gets `\"Bomb Shell\"`, and the same step runs again."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "When the clock nears the arc, I shout the same warning at each of you. Only the name changes. That "
                "is a recipe with one ingredient."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants the hours too. Write a second recipe, `warn_hours(hero_name, hours)`, that prints a line "
            "like `Lucky, get inside! 2 hours left.` Call it once."
        ),
        hints=[
            "Two ingredients on the `def` line, then one `print` that uses both. Glue the number in with "
            "`str(hours)`, and mind the spaces.",
            "Write `def warn_hours(hero_name, hours):`, then "
            "`print(hero_name + \", get inside! \" + str(hours) + \" hours left.\")` under it, four spaces in. "
            "Call it once, like `warn_hours(\"Lucky\", 2)`.",
        ],
        checks=[
            prints_check("warn_hours shows the hero and the hours", "warn_hours", ["hero_name", "hours"],
                         [(("Tester", 5), "Tester, get inside! 5 hours left."),
                          (("Moth", 12), "Moth, get inside! 12 hours left.")],
                         fix="Use both ingredients in the line: `hero_name`, then the hours glued in with `str(hours)`.",
                         kept=False),
        ],
        solution=WARN_SOLUTION + (
            "\ndef warn_hours(hero_name, hours):\n"
            '    print(hero_name + ", get inside! " + str(hours) + " hours left.")\n'
            '\nwarn_hours("Lucky", 2)\n'
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def perform_roll(die_size):",
        why=(
            "You have seen an ingredient at the trap door: `die_size`. Each call handed over a different die, and "
            "the same recipe rolled it. Same idea as `hero_name` today."
        ),
    ),
    takeaway="The ingredient's name (parameter) holds what each call hands over (argument). Use the name inside.",
    wrong_answers=[
        dict(why="one call's line typed in (PAR-CONST; 7 of 11 used one call's values, sheets A-06, A-07, B-02)",
             code=_warn(line='    print("Lucky, get inside!")\n'), fails_at=1, message_contains="Tester"),
        dict(why="the parameter in quotes",
             code=_warn(line='    print("hero_name, get inside!")\n'), fails_at=1, message_contains="word"),
        dict(why="the Example's name `name` (LEFT / rule 3)",
             code=_warn(line='    print(name + ", get inside!")\n'), fails_at=0, message_contains="'name'"),
        dict(why="an approximate parameter name (A-01's `attack` for `base_attack`)",
             code=_warn(line='    print(hero + ", get inside!")\n'), fails_at=0, message_contains="'hero'"),
        dict(why="the comma left out (the near-miss names the first difference, in Mar'tu's values only)",
             code=_warn(line='    print(hero_name + " get inside!")\n'), fails_at=1,
             message_contains="A `,` is missing right after `Tester`"),
        dict(why="values side by side with commas in print() (SFZ-7, G3-5): print adds a space before the comma",
             code=_warn(line='    print(hero_name, ", get inside!")\n'), fails_at=1, message_contains="comma inside"),
        dict(why="the space after the comma left out (the near-miss names it from Mar'tu's line)",
             code=_warn(line='    print(hero_name + ",get inside!")\n'), fails_at=1,
             message_contains="A space is missing right after `,`"),
        dict(why="the side quest's call with a two-word hero and no quotes (SFZ-3; the explainer's new "
                 "split-on-commas row, a site request): Python's own words are 'Perhaps you forgot a comma?'",
             code=WARN_SOLUTION + "\ndef warn_hours(hero_name, hours):\n"
                  '    print(hero_name + ", get inside! " + str(hours) + " hours left.")\n'
                  "\nwarn_hours(Captain Glug, 2)\n",
             fails_at=0, message_contains="forgot a comma"),
        dict(why="the third call hands over nothing (wrong number of arguments)",
             code=_warn(extra="warn()\n"), fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="the third call hands over two values",
             code=_warn(extra='warn("Pip", "Wick")\n'), fails_at=0, message_contains="takes 1 positional argument"),
        dict(why="the third hero unquoted", code=_warn(extra="warn(Wick)\n"), fails_at=0, message_contains="'Wick'"),
        dict(why="no third call (CP2)", code=_warn(extra=""), fails_at=2, message_contains="third call"),
        dict(why="the ingredient refilled with one call's hero inside the recipe (B-02: the call's values go in the body)",
             code=_warn(line='    hero_name = "Lucky"\n    print(hero_name + ", get inside!")\n'), fails_at=1,
             message_contains="thrown away"),
        dict(why="the def line's ingredient renamed (A-01's approximate names)",
             code='def warn(hero):\n    print(hero + ", get inside!")\n\n' + WARN_CALLS + 'warn("Pip")\n', fails_at=1,
             message_contains="letter for letter"),
        dict(why="an if that looks for the check's own values (A-08 working backward, with Unit 2's if)",
             code=_warn(line='    if hero_name == "Tester":\n        print("Tester, get inside!")\n    else:\n'
                             '        print("Moth, get inside!")\n'), fails_at=1, message_contains="check hands over"),
        dict(why="return instead of print (nothing shows)",
             code=_warn(line='    return hero_name + ", get inside!"\n'), fails_at=1, message_contains="`print(...)`"),
        dict(why="the third call wrapped in print() (the line, then None)", code=_warn(extra='print(warn("Pip"))\n'),
             fails_at=2, message_contains="on its own"),
        dict(why="the third warning typed as a print, not a call", code=_warn(extra='print("Pip, get inside!")\n'),
             fails_at=2, message_contains="third call"),
        dict(why="the ingredient's name used outside the recipe (it only exists during a call)",
             code=_warn(extra="warn(hero_name)\n"), fails_at=0, message_contains="'hero_name'"),
        dict(why="Start me off pressed before a click: the print line at the bottom, outside the recipe, `pass` left (the "
                 "explainer says to move it in place of `pass`)",
             code=WARN_STARTER + 'print(hero_name + ", get inside!")\n', fails_at=0, message_contains="'hero_name'"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="param-use", solo="false", dictates="",
             foreign_names="cheer,name,greet,guest", par='("Tester",),("Moth",)', stages="P,R,M",
             twin="def greet(guest): prints the guest's name, then ' waves.'") + "\n"
        "The starter keeps `pass` under the comment (the spec had a comment-only body, which stops with an "
        "IndentationError on the first Run). PAR never collides with the task's calls (lint b). The call table is "
        "the picture angle (and the PAR-CONST bracket names both calls). Any third hero passes (lint e), never "
        "repeated back. Lucky's side quest is a second recipe, `warn_hours`, so finishing it keeps `warn`'s step "
        "green (the spec's version changed `warn` itself). WA evidence: typed values (A-06, A-07, B-02), the "
        "example's name (A-05, A-07, A-08 player_name), approximate names (A-01). Mar'tu's text says the check calls "
        "`warn` with heroes the student never wrote (`warn(\"Tester\")`), so one line must work for every hero. The "
        "near-miss message names the first difference in Mar'tu's values (the comma, the space), and a print with "
        "values side by side (`print(hero_name, \", get inside!\")`) is told that a comma inside print adds a space "
        "(SFZ-7, G3-5). The side quest's unquoted two-word hero is Python's 'Perhaps you forgot a comma?' (WA; the "
        "explainer's new split-on-commas row is a site request). No `<placeholder>` text in the starter or side quest."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-05a fill-the-ingredients (K: contingent)
# ---------------------------------------------------------------------------------------------

FILL_STARTER = (
    "def show_hit(base_damage, bonus):\n"
    "    print(___ + ___)\n"
    "\n"
    "show_hit(4, 3)  # should show: 7\n"
)
HIT_CASES = [((6, 5), 11), ((20, 1), 21)]

FILL_THE_INGREDIENTS = dict(
    id="fill-the-ingredients",
    title="Fill the ingredients",
    martu=(
        "Before you write a line like this yourself, fill two blanks.\n"
        "The ingredient names are on the `def` line. Each `___` needs one of them. Then every call adds its own two "
        "numbers."
    ),
    names=["show_hit", "base_damage", "bonus"],
    starter=FILL_STARTER,
    checkpoints=[
        dict(
            id="fill-each-blank",
            text="Fill each `___` with an ingredient's name.",
            dictated=True,
            hints=[
                "The ingredient names are inside the brackets on the `def` line.",
                "If `def mix(water, oil):`, then `print(water + oil)` adds whatever each call hands over.",
                "Make line 2 read `print(base_damage + bonus)`: `base_damage` in the first blank, `bonus` in the "
                "second.",
            ],
            checks=[
                prints_check("show_hit adds its ingredients", "show_hit", ["base_damage", "bonus"], HIT_CASES,
                             fix="Use both ingredient names, `base_damage` and `bonus`, one in each blank.",
                             const_fix="A recipe gets its numbers when it is called: use `base_damage` and `bonus`.",
                             mode="number", foreign=["mix", "water", "oil"]),
            ],
            pass_line="Gearshift: 4 plus 3. Seven. Checks out.",
        ),
    ],
    solution="def show_hit(base_damage, bonus):\n    print(base_damage + bonus)\n\nshow_hit(4, 3)  # should show: 7\n",
    assemble=dict(
        lines=["def show_hit(base_damage, bonus):", "    print(base_damage + bonus)", "show_hit(4, 3)"],
        distractors=["    print(4 + 3)", "    print(___ + ___)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The blanks",
            text=(
                "```text\ndef show_hit(base_damage, bonus):\n    print(___ + ___)\n            |     |\n"
                "    base_damage  bonus\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Read the `def` line: the ingredients are `base_damage` and `bonus`.\n"
                "2. Put one name in each `___`.\n"
                "3. `show_hit(4, 3)` puts 4 in `base_damage` and 3 in `bonus`, so it shows 7."
            ),
        ),
        dict(
            angle="shorter",
            text="Blanks take the names on the `def` line, never the numbers.",
        ),
    ],
    takeaway="Inside a recipe, use the ingredient names. The call brings the numbers.",
    wrong_answers=[
        dict(why="a blank left (explainer rule 1, the ___ row)",
             code="def show_hit(base_damage, bonus):\n    print(base_damage + ___)\n\nshow_hit(4, 3)\n",
             fails_at=0, message_contains="'___'"),
        dict(why="the call's numbers typed in (PAR-CONST)",
             code="def show_hit(base_damage, bonus):\n    print(4 + 3)\n\nshow_hit(4, 3)\n", fails_at=1,
             message_contains="both printed 7"),
        dict(why="the same ingredient twice",
             code="def show_hit(base_damage, bonus):\n    print(base_damage + base_damage)\n\nshow_hit(4, 3)\n",
             fails_at=1, message_contains="both ingredient"),
        dict(why="an ingredient refilled with the call's number (B-02)",
             code="def show_hit(base_damage, bonus):\n    bonus = 3\n    print(base_damage + bonus)\n\nshow_hit(4, 3)\n",
             fails_at=1, message_contains="thrown away"),
    ],
    notes=(
        meta(starter_level="S4", path="K", contingent="first exposure under 'Show me more', or after an assisted "
             "or failed 6A-04", skills="param-use", solo="false", dictates="1", foreign_names="mix,water,oil",
             par="(6, 5),(20, 1)") + "\n"
        "Contingent (K). In the prototype it is an ordinary exercise, in order, between 6A-04 and 6A-05. It proves "
        "explainer rule 1 (the `___` row): the blank is a NameError for '___'."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-05 use-the-ingredients (the worksheet's Part 3 cliff, reframed)
# ---------------------------------------------------------------------------------------------

HIT_STARTER = (
    "def show_hit(base_damage, bonus):\n"
    "    # print the total hit\n"
    "    pass\n"
    "\n"
    "show_hit(4, 3)  # should show: 7\n"
    "show_hit(8, 2)  # should show: 10\n"
)
HIT_LINE = "    print(base_damage + bonus)\n"
HIT_CALLS = "show_hit(4, 3)\nshow_hit(8, 2)\n"


def _hit(line=HIT_LINE, extra="show_hit(5, 9)\n"):
    return "def show_hit(base_damage, bonus):\n" + line + "\n" + HIT_CALLS + extra


_THIRD_HIT = r'''
_c = _calls_in(_top(), 'show_hit')
_s = [_a for _x in _c for _a in _x.args if type(_a).__name__ == 'Constant' and type(_a.value).__name__ == 'str']
assert not _s, ('Hand over numbers, with no quotes. With quotes they are text, and `+` glues text instead of adding.')
'''

USE_THE_INGREDIENTS = dict(
    id="use-the-ingredients",
    title="Use the ingredients",
    martu=(
        "Inside the recipe, use the ingredient names, never the numbers from one call. The numbers arrive when the "
        "recipe is called.\n"
        "Remember the chalk math in Unit 1? Show your working with boxes, not the answer. Same here: "
        "`base_damage` and `bonus` are the boxes.\n"
        "Two calls are written for you. One line inside the recipe must work for both."
    ),
    names=["show_hit", "base_damage", "bonus"],
    predict=dict(
        q="Before you write it: `4 + 3` is typed inside this recipe. What will the two calls show?",
        code="def show_hit(base_damage, bonus):\n    print(4 + 3)\n\nshow_hit(4, 3)\nshow_hit(8, 2)\n",
        choices=["7\n10", "7\n7", "an error"],
        answer=1,
        explain="`4 + 3` is written in ink: every call shows 7. `base_damage + bonus` would show 7, then 10.",
    ),
    pair_talk="Pair talk: tell your partner why `4 + 3` inside the recipe breaks the second call. Then each of you writes the line.",
    starter=HIT_STARTER,
    checkpoints=[
        dict(
            id="both-totals",
            text="Finish `show_hit` so both calls show the right total.",
            dictated=False,
            hints=[
                "Which names are written inside the brackets on the `def` line? Those are the ingredients.",
                "If `def add(a, b):`, then `print(a + b)` works for any call: `add(2, 3)` shows 5, and "
                "`add(10, 1)` shows 11.",
                "Write `print(base_damage + bonus)` in place of `pass`, four spaces in.",
            ],
            checks=[
                prints_check("show_hit adds its ingredients", "show_hit", ["base_damage", "bonus"], HIT_CASES,
                             fix="Add the two ingredients, `base_damage` and `bonus`, inside the `print`.",
                             const_fix="A recipe gets its numbers when it is called: use `base_damage` and `bonus`.",
                             mode="number", foreign=["add", "a", "b", "mix", "water", "oil"]),
            ],
            pass_line="Gearshift: Seven. Ten. Both check out.",
        ),
        dict(
            id="your-own-numbers",
            text="Add a third call with your own numbers.",
            dictated=False,
            hints=[
                "Two whole numbers, with a comma between them and no quotes.",
                "`add(2, 3)` hands over 2 and 3. Any two whole numbers work.",
                "Write `show_hit(5, 9)` on a new line at the bottom, or any two whole numbers of your own.",
            ],
            checks=[
                calls_check("show_hit is called three times", "show_hit", 3,
                            fix="Add a third call at the bottom: `show_hit(`, two numbers of your own, then `)`.",
                            example="show_hit(5, 9)"),
                ("the numbers are numbers", _FN + _THIRD_HIT),
            ],
            pass_line="Gearshift: New numbers. Visor still checks out.",
        ),
    ],
    solution=_hit(),
    partials=[_hit(extra="")],
    assemble=dict(
        lines=["def show_hit(base_damage, bonus):", "    print(base_damage + bonus)", "show_hit(4, 3)",
               "show_hit(8, 2)", "show_hit(5, 9)"],
        distractors=["    print(4 + 3)", "    print(damage + bonus)", "    print(7)"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="The call table",
            text=(
                "```text\ncall            base_damage bonus\nshow_hit(4, 3)  4           3\n"
                "show_hit(8, 2)  8           2\n```\n"
                "`base_damage + bonus` is 7 in the first row and 10 in the second. `4 + 3` would be 7 in both."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? The recipe can't know the numbers yet",
            text=(
                "When Python reads the `def` line, nobody has called the recipe. There are no numbers yet. "
                "`show_hit(4, 3)` brings 4 and 3. `show_hit(8, 2)` brings 8 and 2. Type `4 + 3` inside, and the "
                "second call still shows 7."
            ),
        ),
        dict(
            angle="everyday",
            label="A fill-in card",
            text=(
                "The card says: add ____ and ____. You fill the blanks each time you read it. Write 4 and 3 on the "
                "card in ink, and every reading says 7."
            ),
        ),
        dict(
            angle="picture",
            label="Ingredients arrive at the call",
            text=(
                "```text\nshow_hit(8, 2)\n         |  |\n         v  v\n  base_damage=8\n  bonus=2\n"
                "  print(8 + 2) -> 10\n```"
            ),
        ),
        dict(
            angle="from what you know",
            label="Show your working",
            text=(
                "In Unit 1 you wrote `total_cost = lantern_cost + rope_cost`, not 22. A recipe is the same: "
                "`base_damage + bonus`, never the answer."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Gearshift's visor sums every hit the same way: the weapon's damage plus the bonus. It never "
                "remembers one fight's numbers. It reads the new ones each time."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky's armor is 13. Inside `show_hit`, also print whether the total hit reaches it: `True` or `False`."
        ),
        hints=[
            "Reaches means at least 13, so exactly 13 counts. Which sign means at least?",
            "Write `print(base_damage + bonus >= 13)` inside `show_hit`, under its first `print`.",
        ],
        checks=[
            (
                "show_hit also says whether the hit reaches 13",
                _FN + r'''
_f, _m = _find('show_hit', True)
assert _f, _m
for _args, _want in (((6, 5), 'False'), ((10, 3), 'True'), ((20, 1), 'True')):
    _v, _rows, _err, _c = _run(_f, _args)
    assert not _err, _why(_f, 'show_hit', _args, _err)
    assert any(_r.split()[-1:] == [_want] for _r in _rows), (
        'Inside `show_hit`, also print whether the total reaches 13: `True` or `False`.'
        + _ev('show_hit', _args, 'no line ended in ' + _want))
''',
            ),
        ],
        solution=(
            "def show_hit(base_damage, bonus):\n    print(base_damage + bonus)\n    print(base_damage + bonus >= 13)\n\n"
            + HIT_CALLS + "show_hit(5, 9)\n"
        ),
    ),
    takeaway="Use the ingredient names inside a recipe, never one call's numbers.",
    wrong_answers=[
        dict(why="one call's numbers typed in (A-06, A-07, B-02 test values; 7 of 11)",
             code=_hit(line="    print(4 + 3)\n"), fails_at=1, message_contains="both printed 7"),
        dict(why="an approximate parameter name (A-01 `attack`)",
             code=_hit(line="    print(damage + bonus)\n"), fails_at=0, message_contains="'damage'"),
        dict(why="the answer typed (A-08)", code=_hit(line="    print(7)\n"), fails_at=1, message_contains="both"),
        dict(why="unrelated numbers (A-02, A-03, A-04)", code=_hit(line="    print(100 * 5)\n"), fails_at=1,
             message_contains="both"),
        dict(why="the Teach hint's names a and b (rule 3)", code=_hit(line="    print(a + b)\n"), fails_at=0,
             message_contains="'a'"),
        dict(why="multiplied instead of added", code=_hit(line="    print(base_damage * bonus)\n"), fails_at=1,
             message_contains="Add"),
        dict(why="the sum in quotes", code=_hit(line='    print("base_damage + bonus")\n'), fails_at=1,
             message_contains="quotes"),
        dict(why="the third call hands over one number", code=_hit(extra="show_hit(5)\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="the third call's numbers in quotes", code=_hit(extra='show_hit("5", "9")\n'), fails_at=2,
             message_contains="no quotes"),
        dict(why="no third call", code=_hit(extra=""), fails_at=2, message_contains="third call"),
        dict(why="one ingredient refilled with one call's number (B-02; the old message said 'add the two ingredients')",
             code=_hit(line="    bonus = 3\n    print(base_damage + bonus)\n"), fails_at=1, message_contains="thrown away"),
        dict(why="the def line's names shortened (A-01's approximate names)",
             code="def show_hit(damage, bonus):\n    print(damage + bonus)\n\n" + HIT_CALLS + "show_hit(5, 9)\n", fails_at=1,
             message_contains="letter for letter"),
        dict(why="an if that looks for the check's own numbers (A-08 working backward)",
             code=_hit(line="    if base_damage == 6:\n        print(11)\n    else:\n        print(21)\n"), fails_at=1,
             message_contains="check hands over"),
        dict(why="return instead of print (nothing shows)", code=_hit(line="    return base_damage + bonus\n"), fails_at=1,
             message_contains="`print(...)`"),
        dict(why="the third call wrapped in print() (the total, then None)", code=_hit(extra="print(show_hit(5, 9))\n"),
             fails_at=2, message_contains="on its own"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="param-use", solo="false", dictates="",
             foreign_names="add,a,b,mix,water,oil", par="(6, 5),(20, 1)", twin="def show_heal(base_heal, extra):")
        + "\n"
        "The worksheet's Part 3 cliff, reframed. PAR uses (6, 5) -> 11 and (20, 1) -> 21: no collision with 7 or 10 "
        "(lint b). A printed line passes when it shows the total as a whole number, so `Hit: 11` is fine and "
        "Lucky's extra True/False line keeps the step green. The starter keeps `pass` under the comment (no "
        "IndentationError on the first Run). PR (pair prompt) is the pair_talk. The predict (RSWM-5) shows `4 + 3` "
        "typed in ink before they write: both calls show 7. The side quest's text gives the goal only; its message "
        "asks for `True` or `False`, never the finished expression."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-06 send-it-back
# ---------------------------------------------------------------------------------------------

MANA_STARTER = (
    "def max_mana_for(affinity):\n"
    "    total = affinity * 2\n"
    "    # 1. hand back total\n"
    "\n"
    "# 2. lucky_max = ...\n"
    "\n"
    "# 3. Write max_fuel_for(cells) here.\n"
    "#    Gearshift gets 5 fuel per cell.\n"
    "\n"
    "\n"
    "# To try it, take the first # off:\n"
    "# print(max_fuel_for(4)) # shows 20\n"
)
MANA_DEF = "def max_mana_for(affinity):\n    total = affinity * 2\n    return total\n"
LUCKY_MAX = "lucky_max = max_mana_for(13)\nprint(lucky_max)\n"
FUEL_DEF = "def max_fuel_for(cells):\n    fuel = cells * 5\n    return fuel\n"
FUEL_TRY = "\nprint(max_fuel_for(4)) # shows 20\n"


def _mana(mana_def=MANA_DEF, lucky=LUCKY_MAX, fuel=FUEL_DEF):
    return mana_def + "\n" + lucky + ("\n" + fuel if fuel else "")


_LUCKY_MAX = r'''
_tops = [_n for _n in _tree.body if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
         and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'lucky_max']
_lone = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Call'
         and type(_n.value.func).__name__ == 'Name' and _n.value.func.id == 'max_mana_for']
assert _tops or not _lone, ('Line ' + str(_lone[0]) + ' calls the recipe, but nothing catches what it hands back, so '
                            'it is gone. Put `lucky_max = ` in front of it.')
assert _tops, 'Store the answer in a box: `lucky_max = max_mana_for(13)`.'
_v = _tops[-1].value
assert not (type(_v).__name__ == 'Name' and _v.id == 'max_mana_for'), (
    'Add `()` with Lucky' + chr(39) + 's 13 inside: `lucky_max = max_mana_for(13)`. With no `()`, `lucky_max` holds '
    'the recipe itself, not what it hands back.')
assert type(_v).__name__ == 'Call' and type(_v.func).__name__ == 'Name' and _v.func.id == 'max_mana_for', (
    'Store what the recipe hands back: `lucky_max = max_mana_for(13)`, not a typed number. Let the recipe do the math.')
_arg = _v.args[0] if len(_v.args) == 1 else None
assert not (type(_arg).__name__ == 'Constant' and type(_arg.value).__name__ == 'str'), (
    'Hand over the number 13, with no quotes: `lucky_max = max_mana_for(13)`. With quotes it is text.')
# A box that holds 13 (`affinity = 13`, then `max_mana_for(affinity)`) is fine too: what matters is what comes back.
assert _arg is not None and ((type(_arg).__name__ == 'Constant' and _arg.value == 13)
                             or (type(lucky_max).__name__ == 'int' and lucky_max == 26)), (
    'Hand over Lucky' + chr(39) + 's affinity, 13: `lucky_max = max_mana_for(13)`.')
assert lucky_max is not None, ('`lucky_max` holds `None`: `max_mana_for` hands nothing back yet. Keep `return total` '
                               'at the end of the recipe.')
_pr = [_c for _c in _calls_in(_top(), 'print') if any(type(_x).__name__ == 'Name' and _x.id == 'lucky_max'
                                                      for _x in _ast.walk(_c))]
assert _pr, 'Then print the box: `print(lucky_max)`.'
assert any(_re.search(_whole(26), _l) for _l in _lines()), 'Print the box below the line that fills it: `print(lucky_max)`.'
'''

SEND_IT_BACK = dict(
    id="send-it-back",
    title="Send it back",
    martu=(
        "`print` says the answer out loud to the room. [[return]] writes it on a note and hands it back to the line "
        "that called.\n"
        "Catch the note in a box: `lucky_max = max_mana_for(13)`. If nothing catches it, it is gone.\n"
        "A recipe with no `return` hands back [[None]], Python's word for nothing.\n"
        "Try it after step 2: delete `return total`, run, and see what `lucky_max` holds. Then put it back. Your "
        "ticks come back when you do."
    ),
    introduces=["node:Return"],
    example="def triple(n):\n    result = n * 3\n    return result\n\nprint(triple(4))\n",
    example_output="12",
    names=["max_mana_for", "total", "lucky_max", "max_fuel_for", "cells"],
    predict=dict(
        q="This recipe works out the total but has no `return`. What will this print?",
        code="def max_mana_for(affinity):\n    total = affinity * 2\n\nlucky_max = max_mana_for(13)\nprint(lucky_max)\n",
        choices=["26", "None", "13", "an error"],
        answer=1,
        explain=(
            "`None`. The recipe works out 26, but no line hands it back. So `lucky_max` catches nothing, and Python's "
            "word for nothing is `None`.\n"
            "Step by step: `affinity` gets 13, `total` gets 26, the recipe ends, and `None` lands in `lucky_max`."
        ),
    ),
    starter=MANA_STARTER,
    checkpoints=[
        dict(
            id="hand-back-total",
            text="Hand back `total` with `return total`.",
            dictated=True,
            hints=[
                "The comment `# 1. hand back total` marks the spot. Which word hands a value back?",
                "`return` hands a value back to the line that called:\n```python\ndef double(n):\n"
                "    return n * 2\n```\n`double(4)` hands back 8.",
                "Write `return total` on the line after `total = affinity * 2`, four spaces in.",
            ],
            checks=[
                returns_check("max_mana_for hands back the total", "max_mana_for", ["affinity"],
                              [((9,), 18), ((12,), 24)],
                              fix="Hand back `total`, the box the recipe works out: `return total`.",
                              const_fix="A recipe gets its numbers when it is called: hand back `total`, worked out "
                                        "from `affinity`.",
                              none_fix="Add `return total` as the last line inside the recipe, four spaces in.",
                              foreign=["triple", "n", "result", "double"], box="This recipe's box is `total`."),
            ],
            pass_line="Mar'tu: The note comes back. Good.",
        ),
        dict(
            id="catch-it",
            text="Store `max_mana_for(13)` in `lucky_max`, then print `lucky_max`.",
            dictated=True,
            hints=[
                "The call goes on the right of `=`, so the box catches what comes back. Then print the box.",
                "`x = triple(4)` catches what `triple` hands back: `x` holds 12. Then `print(x)` shows it.",
                "Write `lucky_max = max_mana_for(13)` on a new line at the bottom, then `print(lucky_max)`.",
            ],
            checks=[("lucky_max catches the note", _FN + _LUCKY_MAX)],
            pass_line="Lucky: 26. That's more than Gearshift. Write that down.",
        ),
        dict(
            id="max-fuel",
            text="Write a recipe `max_fuel_for(cells)` that hands back the fuel. Gearshift gets 5 fuel per cell.",
            dictated=False,
            hints=[
                "Three lines, like `max_mana_for` above: the `def` line with `cells` and a colon, a line that works "
                "out the fuel from `cells`, then `return` that box.",
                "How much fuel for one cell? For `cells` cells?",
                "`def double(n):` with `return n * 2` inside hands back twice whatever came in.",
                "Write `def max_fuel_for(cells):` at the `# 3.` mark. Under it, four spaces in, "
                "`fuel = cells * 5`, then `return fuel`.",
            ],
            checks=[
                returns_check("max_fuel_for hands back 5 per cell", "max_fuel_for", ["cells"], [((3,), 15), ((7,), 35)],
                              fix="Gearshift gets 5 fuel per cell: multiply `cells` by 5, and hand that back.",
                              const_fix="A recipe gets its numbers when it is called: work the fuel out from `cells`.",
                              foreign=["triple", "n", "result", "double"],
                              rules=[("_v == _a[0] * 2", "Gearshift gets 5 fuel per cell, not 2: multiply `cells` by 5.")],
                              kept=False),
            ],
            pass_line="Gearshift: Fuel math checks out. Visor dims.",
        ),
    ],
    solution=_mana() + FUEL_TRY,
    partials=[MANA_DEF, _mana(fuel="")],
    assemble=dict(
        lines=["def max_mana_for(affinity):", "    total = affinity * 2", "    return total",
               "lucky_max = max_mana_for(13)", "print(lucky_max)", "def max_fuel_for(cells):",
               "    fuel = cells * 5", "    return fuel", "print(max_fuel_for(4))"],
        distractors=["    print(total)", "lucky_max = 26", "    return result"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The return arrow",
            text=(
                "```text\nlucky_max = max_mana_for(13)\n    ^             |\n    |    affinity = 13\n"
                "    |    total = 26\n    +--- return total\n```\n"
                "The note comes back to the call, and the box on the left catches it."
            ),
        ),
        dict(
            angle="everyday",
            label="A note handed back",
            text=(
                "You ask a friend to add up the bill. `print` is them shouting the total across the room. `return` is "
                "them writing it on a note and handing it to you. You can keep a note."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step table",
            text=(
                "1. `max_mana_for(13)`: `affinity` gets 13.\n"
                "2. `total = affinity * 2`: `total` gets 26.\n"
                "3. `return total`: the recipe hands back 26 and ends.\n"
                "4. `lucky_max = ...`: the box catches 26.\n"
                "5. `print(lucky_max)` shows 26."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? `return` ends the recipe",
            text=(
                "`return` hands the note back, and the recipe stops there. A line under it, inside the recipe, "
                "never runs:\n"
                "```python\ndef double(n):\n    return n * 2\n    print(\"Never shown.\")\n```\n"
                "`double(4)` hands back 8 and prints nothing."
            ),
        ),
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "At the trap door, `perform_roll(die_size)` handed back a roll with `return`. The skill check caught "
                "it and compared it. A recipe that hands back is a recipe you can use again."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "At the Institute, apprentices wrote answers on slips and passed them up. A shouted answer helped "
                "nobody at the back. A slip could be kept."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants a status line. Print `Lucky's max mana: ` with `max_mana_for(13)` glued on, using `str()`, "
            "all on one line."
        ),
        hints=[
            "The call can go straight inside `str()`: what it hands back gets glued on.",
            "Write `print(\"Lucky's max mana: \" + str(max_mana_for(13)))` at the bottom.",
        ],
        checks=[
            (
                "a status line with the call inside str()",
                _FN + r'''
assert [_c for _c in _calls_in(_top(), 'str') if _calls_in([_c], 'max_mana_for')], (
    'Put the call inside `str()`: `str(max_mana_for(13))`, glued to the words with `+`.')
assert any('Lucky' in _l and _re.search(_whole(26), _l) for _l in _lines()), (
    'Print one line with Lucky and his max mana in it, like `Lucky' + chr(39) + 's max mana: 26`.')
''',
            ),
        ],
        solution=_mana() + "\nprint(\"Lucky's max mana: \" + str(max_mana_for(13)))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="def show_mana(caster):\n    mana_bar = get_mana_bar(caster)",
        why=(
            "You have seen a box catch a recipe's note. `get_mana_bar(caster)` handed back the bar with `return`, "
            "and `mana_bar` caught it. Same shape as `lucky_max = max_mana_for(13)`."
        ),
    ),
    takeaway="`return` hands a value back. Catch it: `box = recipe(...)`. No `return` means `None`.",
    wrong_answers=[
        dict(why="print instead of return (RET; A-07)",
             code=_mana(mana_def="def max_mana_for(affinity):\n    total = affinity * 2\n    print(total)\n"),
             fails_at=1, message_contains="None"),
        dict(why="no return at all (the comment left)",
             code=_mana(mana_def=MANA_STARTER.split("\n# 2.")[0] + "\n", lucky="", fuel=""),
             fails_at=1, message_contains="None"),
        dict(why="the parameter handed back as it came in (RET-PARAM; A-07)",
             code=_mana(mana_def="def max_mana_for(affinity):\n    total = affinity * 2\n    return affinity\n"),
             fails_at=1, message_contains="as it came in"),
        dict(why="one fixed answer (PAR-CONST; A-06 `return 50`)",
             code=_mana(mana_def="def max_mana_for(affinity):\n    total = affinity * 2\n    return 26\n"),
             fails_at=1, message_contains="both gave back"),
        dict(why="the Example's name result (rule 3; A-01)",
             code=MANA_DEF.replace("return total", "return result"), fails_at=1, message_contains="example"),
        dict(why="return not indented (outside the recipe)",
             code="def max_mana_for(affinity):\n    total = affinity * 2\nreturn total\n", fails_at=0,
             message_contains="'return' outside function"),
        dict(why="lucky_max typed as 26 (not stored from the call)", code=_mana(lucky="lucky_max = 26\nprint(lucky_max)\n"),
             fails_at=2, message_contains="store"),
        dict(why="the call made but nothing catches it", code=_mana(lucky="max_mana_for(13)\nprint(26)\n"),
             fails_at=2, message_contains="catches"),
        dict(why="the call with no value handed over (wrong number of arguments)",
             code=_mana(lucky="lucky_max = max_mana_for()\nprint(lucky_max)\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="CP3 one fixed answer (`return 15`)",
             code=_mana(fuel="def max_fuel_for(cells):\n    return 15\n"), fails_at=3, message_contains="both"),
        dict(why="CP3 times 2, not 5", code=_mana(fuel="def max_fuel_for(cells):\n    return cells * 2\n"), fails_at=3,
             message_contains="5 fuel per cell"),
        dict(why="CP3 an approximate name (PNM; A-01)", code=_mana(fuel="def max_fuel_for(cells):\n    return cell * 5\n"),
             fails_at=3, message_contains="letter for letter"),
        dict(why="CP3 an approximate parameter name on the def line",
             code=_mana(fuel="def max_fuel_for(cell):\n    return cell * 5\n"), fails_at=3, message_contains="cells"),
        dict(why="CP3 returns a name it never made (`return result` after `fuel = ...`; RNM, RTS-1: the message names "
                 "this recipe's own box, so the student is not sent to `cells` and back)",
             code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return result\n"), fails_at=3,
             message_contains="box is `fuel`"),
        dict(why="CP3 returns a name it never made, with the try line on (the crash path: the explainer names this "
                 "recipe's own box, `fuel`, as the check does)",
             code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return result\n") + FUEL_TRY, fails_at=0,
             message_contains="name 'result' is not defined"),
        dict(why="CP1 a blank `return` (B-02's blank return; G3-1): `return` on its own hands back nothing",
             code=_mana(mana_def="def max_mana_for(affinity):\n    total = affinity * 2\n    return\n"),
             fails_at=1, message_contains="on its own"),
        dict(why="CP1 the box's name in quotes (`return \"total\"`: the quoted-name habit, not hard-coding)",
             code=_mana(mana_def='def max_mana_for(affinity):\n    total = affinity * 2\n    return "total"\n'),
             fails_at=1, message_contains="Take the quotes off `total`"),
        dict(why="CP3 the box's name in quotes (`return \"fuel\"`)",
             code=_mana(fuel='def max_fuel_for(cells):\n    fuel = cells * 5\n    return "fuel"\n'), fails_at=3,
             message_contains="Take the quotes off `fuel`"),
        dict(why="CP3 a blank `return` after `fuel = ...` (G3-1)",
             code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return\n"), fails_at=3,
             message_contains="on its own"),
        dict(why="CP3 the recipe written like maths, f(x) = 5x (SFZ-2; the explainer's new f(x) = 5x row)",
             code=_mana(fuel="max_fuel_for(cells) = cells * 5\n"), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="CP3 the ingredient name in quotes on the def line (SFZ-5; the explainer's new quoted-ingredient row)",
             code=_mana(fuel='def max_fuel_for("cells"):\n    return cells * 5\n'), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="CP3 the try line uncommented before max_fuel_for is written (calling it before defining it)",
             code=_mana(fuel="") + FUEL_TRY, fails_at=0, message_contains="name 'max_fuel_for' is not defined"),
        dict(why="CP3 = used to make the recipe, worked out from its ingredient (`max_fuel_for = cells * 5`: Python reads "
                 "`cells` now; the explainer answers with the recipe's def, never 'make cells')",
             code=_mana(fuel="max_fuel_for = cells * 5\n"), fails_at=0, message_contains="name 'cells' is not defined"),
        dict(why="CP3 = used to make the recipe, worked out from its ingredient, with the try line on",
             code=_mana(fuel="max_fuel_for = cells * 5\n") + FUEL_TRY, fails_at=0,
             message_contains="name 'cells' is not defined"),
        dict(why="CP3 = used to make the recipe after a box `cells` is made (no crash: the check names the box)",
             code=_mana(fuel="cells = 4\nmax_fuel_for = cells * 5\n"), fails_at=3, message_contains="box"),
        dict(why="CP3 = used to make the recipe after a box `cells` is made, with the try line on (the box called)",
             code=_mana(fuel="cells = 4\nmax_fuel_for = cells * 5\n") + FUEL_TRY, fails_at=0,
             message_contains="'int' object is not callable"),
        dict(why="CP3 def mixed with = (`def max_fuel_for = cells * 5`; never 'make a box')",
             code=_mana(fuel="def max_fuel_for = cells * 5\n"), fails_at=0, message_contains="expected '('"),
        dict(why="CP3 f(x) = 5x with def in front (`def max_fuel_for(cells) = cells * 5`)",
             code=_mana(fuel="def max_fuel_for(cells) = cells * 5\n"), fails_at=0, message_contains="expected ':'"),
        dict(why="CP3 f(x) = 5x with def in front and a colon at the end (the same error again: never 'add a colon')",
             code=_mana(fuel="def max_fuel_for(cells) = cells * 5:\n"), fails_at=0, message_contains="expected ':'"),
        dict(why="CP3 print instead of return", code=_mana(fuel="def max_fuel_for(cells):\n    print(cells * 5)\n"),
             fails_at=3, message_contains="None"),
        dict(why="CP3 the parameter handed back", code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return cells\n"),
             fails_at=3, message_contains="as it came in"),
        dict(why="CP1 the ingredient refilled with Lucky's 13 inside the recipe (B-02)",
             code=_mana(mana_def="def max_mana_for(affinity):\n    affinity = 13\n    total = affinity * 2\n    return total\n"),
             fails_at=1, message_contains="thrown away"),
        dict(why="CP2 no () on the call: lucky_max holds the recipe itself (the old message said 'not a typed number')",
             code=_mana(lucky="lucky_max = max_mana_for\nprint(lucky_max)\n"), fails_at=2, message_contains="`()`"),
        dict(why="CP2 the 13 handed over in quotes", code=_mana(lucky='lucky_max = max_mana_for("13")\nprint(lucky_max)\n'),
             fails_at=2, message_contains="no quotes"),
        dict(why="CP3 an if that looks for the check's own numbers (A-08 working backward)",
             code=_mana(fuel="def max_fuel_for(cells):\n    if cells == 3:\n        return 15\n    return 35\n"), fails_at=3,
             message_contains="check hands over"),
        dict(why="CP3 returns `total`, a box from max_mana_for's kitchen (RNM)",
             code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return total\n"), fails_at=3,
             message_contains="another recipe"),
        dict(why="CP3 returns `total`, a box from max_mana_for's kitchen, with the try line on (the explainer: `total` "
                 "belongs to max_mana_for; hand back fuel)",
             code=_mana(fuel="def max_fuel_for(cells):\n    fuel = cells * 5\n    return total\n") + FUEL_TRY, fails_at=0,
             message_contains="name 'total' is not defined"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="return-value,param-use,return-right-name", solo="false",
             dictates="1,2", foreign_names="triple,n,result,double", par="(9,),(12,); (3,),(7,)", stages="P,R,I,M",
             point_at_it="Which box catches what the recipe hands back?",
             twin="def double_cost(price): returns twice the price") + "\n"
        "Investigate (delete return total, see None) is the predict (with the step table in its explain) and the "
        "Learn text. CP2 accepts any argument that leaves `lucky_max` holding 26 (`affinity = 13`, then "
        "`max_mana_for(affinity)` is fine); `lucky_max = max_mana_for` (no `()`) and a quoted \"13\" get their own "
        "messages. CP3 is the lesson's capstone non-dictated step (G4 R10). PAR (9 -> 18, 12 -> 24; 3 -> 15, "
        "7 -> 35) never collides with the task's 13 -> 26. WA evidence: B-02 blank return, A-07 raw inputs, A-06 "
        "`return 50`, A-01 `return reslt`/approximate names. The starter numbers its comments 1-3 and ends with a "
        "commented try line (`print(max_fuel_for(4))`, 20; lines of 36 characters or fewer), so the blank-start "
        "recipe has a marked spot (G3-2). CP3's ladder puts the structure at rung 1 and the maths at rung 2. A blank "
        "`return` gets its own message, and `return result` after `fuel = ...` is told that this recipe's box is "
        "`fuel` (RTS-1). The 'why' angle shows that `return` ends the recipe. Python 3.13's own words are proven for "
        "f(x) = 5x (`cannot assign to function call`) and a quoted ingredient (`invalid syntax`): the explainer's "
        "new rows are a site request."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-06b be-the-ledger (trace table, prototype form; moment: traced on the board together)
# ---------------------------------------------------------------------------------------------

LEDGER_PROGRAM = (
    "def ward_strength(lanterns, runes):\n"
    "    light = lanterns * 10\n"
    "    glow = runes * 5\n"
    "    return light + glow\n"
    "\n"
    "barrier = ward_strength(3, 4) + 10\n"
    "print(barrier)\n"
)
LEDGER_ROWS = [
    ("lanterns_row", 3), ("runes_row", 4), ("light_row", 30), ("glow_row", 20), ("handed_back_row", 50),
    ("barrier_row", 60), ("printed_row", 60),
]


def _ledger(values):
    out = "# The ledger: what each box holds\n# when ward_strength(3, 4) runs.\n"
    for (name, _), value in zip(LEDGER_ROWS, values):
        out += f"{name} = {value}\n"
    return out


LEDGER_STARTER = _ledger([0] * 7)
LEDGER_SOLUTION = _ledger([want for _, want in LEDGER_ROWS])
NOT_ADDED = "`print(barrier)` shows only what is in `barrier`. It does not add up the earlier lines."

LEDGER_CPS = [
    dict(
        id="lanterns-row",
        text="Set `lanterns_row` to the number `lanterns` holds in this call.",
        hints=[
            "`ward_strength(3, 4)` hands over two numbers. The first one goes in the first ingredient.",
            "Ingredients fill in order: `mix(2, 9)` puts 2 in the first ingredient and 9 in the second.",
            "Write `lanterns_row = ` and then the first number inside `ward_strength(3, 4)`.",
        ],
        checks=[row_check("lanterns_row is 3", "lanterns_row", 3, {4: (
            "The first number handed over fills the first ingredient: `ward_strength(3, 4)` puts 3 in `lanterns`.")},
            "`ward_strength(3, 4)` hands over 3 first. The first ingredient, `lanterns`, holds it.")],
    ),
    dict(
        id="runes-row",
        text="Set `runes_row` to the number `runes` holds.",
        hints=[
            "Which number in `ward_strength(3, 4)` is second?",
            "Ingredients fill in order: `mix(2, 9)` puts 9 in the second ingredient.",
            "Write `runes_row = ` and then the second number inside `ward_strength(3, 4)`.",
        ],
        checks=[row_check("runes_row is 4", "runes_row", 4, {3: (
            "The second number fills the second ingredient: `ward_strength(3, 4)` puts 4 in `runes`.")},
            "`runes` is the second ingredient, so it holds the second number handed over: 4.")],
    ),
    dict(
        id="light-row",
        text="Set `light_row` to the number `light` holds.",
        hints=[
            "`light = lanterns * 10`. What is in `lanterns` right now?",
            "Work out a line from what is IN the boxes: if `cups` holds 2, then `cups * 10` is 20.",
            "Write `light_row = ` and then what `lanterns * 10` makes, with your `lanterns_row` number in `lanterns`.",
        ],
        checks=[row_check("light_row is 30", "light_row", 30, {
            10: "10 is the number written in the recipe. `light` is `lanterns * 10`, and `lanterns` holds 3.",
            13: "`*` multiplies: `lanterns * 10` is 3 times 10.",
            3: "`light` is `lanterns * 10`: 3 times 10.",
        }, "Work out `lanterns * 10`, with `lanterns` holding 3.")],
    ),
    dict(
        id="glow-row",
        text="Set `glow_row` to the number `glow` holds.",
        hints=[
            "`glow = runes * 5`. What is in `runes` right now?",
            "If `jars` holds 4, then `jars * 5` is 20.",
            "Write `glow_row = ` and then what `runes * 5` makes, with your `runes_row` number in `runes`.",
        ],
        checks=[row_check("glow_row is 20", "glow_row", 20, {
            5: "5 is the number written in the recipe. `glow` is `runes * 5`, and `runes` holds 4.",
            9: "`*` multiplies: `runes * 5` is 4 times 5.",
            15: "`glow` uses `runes`, which holds 4: 4 times 5.",
        }, "Work out `runes * 5`, with `runes` holding 4.")],
    ),
    dict(
        id="handed-back-row",
        text="Set `handed_back_row` to the number the recipe hands back.",
        hints=[
            "Look at the `return` line. What is in `light` and `glow` when it runs?",
            "`return light + glow` adds what is IN the two boxes. Your two rows above hold those numbers.",
            "Write `handed_back_row = ` and then your `light_row` number plus your `glow_row` number.",
        ],
        checks=[row_check("handed_back_row is 50", "handed_back_row", 50, {
            15: ("15 is 10 + 5, the numbers written in the recipe. On this line the boxes hold 30 and 20. Add what "
                 "is in the boxes."),
            7: "7 is 3 + 4, the ingredients as they came in. The recipe hands back `light + glow`.",
            60: "60 adds the 10 from the `barrier` line. The recipe hands back only `light + glow`.",
        }, "The recipe hands back `light + glow`: add your `light` and `glow` rows.")],
    ),
    dict(
        id="barrier-row",
        text="Set `barrier_row` to the number `barrier` holds.",
        hints=[
            "`barrier = ward_strength(3, 4) + 10`. The call part becomes what the recipe handed back.",
            "If a recipe hands back 8, then `x = recipe() + 1` puts 9 in `x`.",
            "Write `barrier_row = ` and then your `handed_back_row` number plus 10.",
        ],
        checks=[row_check("barrier_row is 60", "barrier_row", 60, {
            40: "The `barrier` line starts from what the recipe handed back (50), not from `light` or `glow`.",
            30: "The `barrier` line starts from what the recipe handed back (50), not from `light` or `glow`.",
            50: "Then add the 10 on the `barrier` line: `ward_strength(3, 4) + 10`.",
            25: "Start from what the recipe handed back, 50, then add 10.",
            17: "Start from what the recipe handed back, 50, then add 10.",
        }, "Start from what the recipe handed back, then add the 10 on the `barrier` line.")],
    ),
    dict(
        id="printed-row",
        text="Set `printed_row` to the number `print(barrier)` shows.",
        hints=[
            "`print(barrier)` shows one box. What did you write for `barrier`?",
            "`print(x)` shows only what is in `x`, nothing more.",
            "Write `printed_row = ` and then the same number as your `barrier_row`.",
        ],
        checks=[row_check("printed_row is 60", "printed_row", 60, {
            55: NOT_ADDED, 45: NOT_ADDED, 110: NOT_ADDED, 160: NOT_ADDED, 50: NOT_ADDED + " Use your `barrier` row.",
        }, NOT_ADDED + " Use your `barrier` row.")],
        pass_line="Mar'tu: Sixty. Python prints exactly that. You traced it before it ran.",
    ),
]
for _cp in LEDGER_CPS:
    _cp["dictated"] = False

BE_THE_LEDGER = dict(
    id="be-the-ledger",
    title="Be the ledger",
    martu=(
        "Be the ledger, yes? Read this spell. You run it in your head, not on the screen.\n"
        "```python\ndef ward_strength(lanterns, runes):\n    light = lanterns * 10\n    glow = runes * 5\n"
        "    return light + glow\n\nbarrier = ward_strength(3, 4) + 10\nprint(barrier)\n```\n"
        "Fill one row at a time: what each box holds when it runs. Use what is IN the boxes, not the numbers "
        "written in the recipe.\n"
        "Fill every row before you look anything up."
    ),
    names=[name for name, _ in LEDGER_ROWS],
    pair_talk=(
        "Pair talk: fill your ledger on your own first. Then compare rows with your partner. Where do you differ? "
        "Find the line in the program that settles it."
    ),
    # Teacher ruling #1, tracing must be honest: a pasted program is stopped before it runs (nothing printed), and
    # there is no Assemble it (its pieces would be the finished rows, ahead of Show me how's working).
    setup=paste_stop("ward_strength"),
    starter=LEDGER_STARTER,
    checkpoints=LEDGER_CPS,
    solution=LEDGER_SOLUTION,
    partials=[_ledger([want for _, want in LEDGER_ROWS[:k]] + [0] * (7 - k)) for k in range(1, 7)],
    another_way=[
        dict(
            angle="picture",
            label="The return arrow, with another call",
            text=(
                "Here is the same recipe with another call. Do yours the same way.\n"
                "```text\nward_strength(4, 3) + 10\n  lanterns = 4\n  runes = 3\n  light = 40\n  glow = 15\n"
                "  return 55 ----+\n                |\nbarrier = 55 + 10\n        = 65\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            label="Step by step, with another call",
            text=(
                "Here is the same recipe with another call. Do yours the same way.\n"
                "1. `ward_strength(4, 3)` hands over 4 and 3: `lanterns` is 4, `runes` is 3.\n"
                "2. `light` is 4 times 10: 40.\n"
                "3. `glow` is 3 times 5: 15.\n"
                "4. The recipe hands back 40 + 15: 55.\n"
                "5. `barrier` is 55 + 10: 65.\n"
                "6. `print(barrier)` shows 65, and only 65."
            ),
        ),
        dict(
            angle="everyday",
            label="A shop till",
            text=(
                "A receipt shows what is in each line, not the price list on the wall. Each row of your ledger is a "
                "line of the receipt: what that box holds right now."
            ),
        ),
    ],
    takeaway="Trace a call with what is IN the boxes. What the recipe hands back lands where the call was.",
    wrong_answers=[
        dict(why="handed back = 15: the constants written in the recipe (A-03, A-04)",
             code=_ledger([3, 4, 30, 20, 15, 0, 0]), fails_at=5, message_contains="10 + 5"),
        dict(why="handed back = 7: the raw inputs (A-07)", code=_ledger([3, 4, 30, 20, 7, 0, 0]), fails_at=5,
             message_contains="came in"),
        dict(why="barrier = 40: started from light, not the handed-back value (A-03, A-04 bonus line)",
             code=_ledger([3, 4, 30, 20, 50, 40, 0]), fails_at=6, message_contains="handed back"),
        dict(why="printed = 55: a sum of earlier results (A-03)", code=_ledger([3, 4, 30, 20, 50, 60, 55]), fails_at=7,
             message_contains="only what"),
        dict(why="lanterns and runes swapped", code=_ledger([4, 3, 0, 0, 0, 0, 0]), fails_at=1,
             message_contains="first ingredient"),
        dict(why="light = 10: the constant in the recipe", code=_ledger([3, 4, 10, 0, 0, 0, 0]), fails_at=3,
             message_contains="written in the recipe"),
        dict(why="a row typed in quotes", code=_ledger([3, 4, '"30"', 0, 0, 0, 0]), fails_at=3,
             message_contains="quotes"),
        dict(why="the program pasted in above the rows and run (SFZ-1: the guard fails every row before its value)",
             code=LEDGER_PROGRAM + "\n" + LEDGER_SOLUTION, fails_at=1, message_contains="holds only your rows"),
        dict(why="a row worked out with a print() line instead of traced",
             code=LEDGER_SOLUTION + "print(3 * 10 + 4 * 5)\n", fails_at=1, message_contains="holds only your rows"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="trace-call", solo="false", dictates="", stages="P,TT,R",
             moment="traced on the board together", item_type="trace table (prototype: rows as boxes)",
             twin="ward_strength(9, 7) + 10 -> 90 + 35 = 125, then 135; new numbers per seat") + "\n"
        "Prototype representation until the trace-table item type exists: each row is a box in the starter, and "
        "each checkpoint checks one row with the targeted messages from the spec (15 = the constants, 7 = the raw "
        "inputs, 40/30 = started from light or glow, 55/45 = a sum of earlier rows). The program is ONLY in the "
        "Learn text, as a fenced block (lines of 36 characters or fewer). There is no Example, so there is nothing to "
        "Run: tracing is honest (SFZ-1, RSWM-4). Every row check first fails if the editor holds a `def`, a call to "
        "`ward_strength` or a `print(` (a pasted program; WA), and the hidden setup (paste_stop) stops such a program "
        "before it runs, so the console never shows its 60 (U3 review). No assemble: its pieces were the finished rows "
        "(the harness now warns about that). The picture and step-by-step angles trace another "
        "call, `ward_strength(4, 3) + 10` (4, 3, 40, 15, 55, 65, 65), never this one; (4, 1) is avoided because it "
        "gives 45/55, the rows of the Quick Check's Form A. The twin (9, 7) repeats no value used in this lesson, "
        "its angles, Quiz 6A (2, 8: 20, 40, 60, 70) or the Quick Check (2, 5 and 4, 1). The same shape returns in "
        "Quiz 6A #3 with (2, 8)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-07 return-the-right-box
# ---------------------------------------------------------------------------------------------

ARMOR_DEF = "def armor_total(base, bonus):\n    total = base + bonus\n    return total\n"
SHIELD_DEF = "def shield_total(base, bonus):\n    total = base + bonus\n    return total\n"
BOX_PRINTS = 'print("Lucky: " + str(armor_total(10, 3)))\nprint("Shield: " + str(shield_total(2, 1)))\n'


def _boxes(armor=ARMOR_DEF, shield=SHIELD_DEF, prints=BOX_PRINTS):
    return armor + "\n" + shield + "\n" + prints


BOXES_STARTER = _boxes(armor=ARMOR_DEF.replace("return total", "return result"),
                       shield="def shield_total(base, bonus):\n    total = base + bonus\n")
BOXES_SOLUTION = _boxes()

RIGHT_BOX = dict(
    id="return-the-right-box",
    title="Return the right box",
    martu=(
        "Two recipes, two slips: one crashes, one is quiet. Read Python's last line first, then mend them one at a "
        "time."
    ),
    names=["armor_total", "shield_total", "total"],
    starter=BOXES_STARTER,
    checkpoints=[
        dict(
            id="armor-hands-back-total",
            text="Fix `armor_total` so it hands back the box it computed.",
            dictated=True,
            hints=[
                "Read Python's last line first. Which name does it not know?",
                "Which box does `armor_total` make on the line above `return`?",
                "A recipe hands back a box it made:\n```python\ndef trip(n):\n    steps = n * 3\n    return steps\n```",
                "Write `return total` in place of `return result`, four spaces in.",
            ],
            checks=[
                returns_check("armor_total hands back its total", "armor_total", ["base", "bonus"],
                              [((6, 5), 11), ((20, 1), 21)],
                              fix="Hand back the box the recipe made: `return total`.",
                              const_fix="A recipe gets its numbers when it is called: hand back `total`, worked out "
                                        "from `base` and `bonus`.",
                              foreign=["result", "triple", "n", "trip", "steps"], box="This recipe's box is `total`."),
                ("Lucky: 13 prints", "assert 'Lucky: 13' in _lines(), 'Keep the line that prints `Lucky: 13` at the bottom.'"),
            ],
            pass_line="Lucky: Thirteen. Shiny.",
        ),
        dict(
            id="shield-hands-back",
            text="`Shield:` shows `None`. Make `shield_total` hand back its total.",
            dictated=False,
            hints=[
                "`shield_total` works out `total`, then stops. Nothing hands it back.",
                "No `return` line means the recipe hands back `None`. One line fixes it.",
                "Write `return total` as the last line of `shield_total`, four spaces in.",
            ],
            checks=[
                returns_check("shield_total hands back its total", "shield_total", ["base", "bonus"],
                              [((6, 5), 11), ((20, 1), 21)],
                              fix="Hand back the box the recipe made: `return total`.",
                              none_fix="`shield_total` has no `return` line, so it hands back `None`. Hand back its "
                                       "total.",
                              foreign=["result", "triple", "n", "trip", "steps"], box="This recipe's box is `total`."),
                ("Shield: 3 prints", "assert 'Shield: 3' in _lines(), 'Keep the line that prints `Shield: 3` at the bottom.'"),
            ],
            pass_line="Bomb Shell: Shield up. Three.",
        ),
    ],
    solution=BOXES_SOLUTION,
    partials=[_boxes(shield="def shield_total(base, bonus):\n    total = base + bonus\n")],
    assemble=dict(
        lines=[line for line in BOXES_SOLUTION.splitlines() if line.strip()],
        distractors=["    return result", "    print(total)"],
    ),
    another_way=[
        dict(
            angle="why",
            label="Why does this work? Whose kitchen is `result` in?",
            text=(
                "`result` was made inside `triple`, in my Example. A box made inside a recipe lives in that recipe's "
                "kitchen only. `armor_total` has its own kitchen, and its box is `total`."
            ),
        ),
        dict(
            angle="picture",
            label="Two kitchens",
            text=(
                "```text\ntriple's kitchen:\n  result\n\narmor_total's kitchen:\n  total   <- hand this back\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="The wrong bowl",
            text=(
                "You cook soup in the blue bowl, then hand over the red bowl from yesterday's kitchen. It isn't here. "
                "Hand over the bowl you just filled."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Read the message: `name 'result' is not defined`.\n"
                "2. Find the box the recipe makes: `total = base + bonus`.\n"
                "3. Hand that one back: `return total`.\n"
                "4. Run. `Shield: None` means the second recipe has no `return`. Add one."
            ),
        ),
        dict(angle="shorter", text="Hand back the box you made. No `return` means `None`."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text="Is Lucky's armor better than 12? Print the answer, `True` or `False`, using `armor_total(10, 3)`.",
        hints=[
            "A comparison gives `True` or `False`: `>` means more than.",
            "Write `print(armor_total(10, 3) > 12)` at the bottom.",
        ],
        checks=[
            (
                "prints whether the armor beats 12",
                _FN + r'''
_cmp = [_n for _n in _ast.walk(_tree) if type(_n).__name__ == 'Compare' and _calls_in([_n], 'armor_total')]
assert _cmp, 'Compare the total with 12: `armor_total(10, 3) > 12`, inside a `print`.'
assert any(_l.split()[-1:] == ['True'] for _l in _lines()), 'Print the answer: `print(armor_total(10, 3) > 12)`.'
''',
            ),
        ],
        solution=BOXES_SOLUTION + "print(armor_total(10, 3) > 12)\n",
    ),
    takeaway="Hand back the box the recipe made. A recipe with no `return` hands back `None`.",
    wrong_answers=[
        dict(why="the starter: `return result` (rule 3: the Example's name; A-01)", code=BOXES_STARTER, fails_at=0,
             message_contains="'result'"),
        dict(why="return reslt (A-01; rule 3 fuzzy)",
             code=_boxes(armor=ARMOR_DEF.replace("return total", "return reslt")), fails_at=0, message_contains="reslt"),
        dict(why="return base (RET-PARAM: as it came in)",
             code=_boxes(armor=ARMOR_DEF.replace("return total", "return base")), fails_at=1,
             message_contains="as it came in"),
        dict(why="return \"total\": the box's name in quotes (the quoted-name habit, not hard-coding)",
             code=_boxes(armor=ARMOR_DEF.replace("return total", 'return "total"')), fails_at=1,
             message_contains="Take the quotes off `total`"),
        dict(why="return 13 (PAR-CONST)", code=_boxes(armor=ARMOR_DEF.replace("return total", "return 13")),
             fails_at=1, message_contains="both gave back"),
        dict(why="print(total) in shield_total (prints, hands back None)",
             code=_boxes(shield="def shield_total(base, bonus):\n    total = base + bonus\n    print(total)\n"),
             fails_at=2, message_contains="None"),
        dict(why="shield_total still has no return",
             code=_boxes(shield="def shield_total(base, bonus):\n    total = base + bonus\n"), fails_at=2,
             message_contains="no `return` line"),
        dict(why="an if that looks for the check's own numbers (A-08 working backward)",
             code=_boxes(armor="def armor_total(base, bonus):\n    total = base + bonus\n    if base == 6:\n        return 11\n"
                               "    if base == 20:\n        return 21\n    return 13\n"), fails_at=1,
             message_contains="check hands over"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="return-right-name,return-value", solo="false", dictates="1",
             foreign_names="result,triple,n,trip,steps", par="(6, 5),(20, 1)", stages="D,M") + "\n"
        "The starter stops with `name 'result' is not defined` (explainer rule 3: `result` is in foreign_names, from "
        "6A-06's Example). WT 'Whose kitchen is result in?' is the why angle (a scope preview; the full version is "
        "pool item 6B-09). PAR (6, 5) and (20, 1) never collide with the task's (10, 3) and (2, 1)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-08 store-then-pass (rehearsal: program-dialogue-prompt)
# ---------------------------------------------------------------------------------------------

BOARD_SETUP = (
    "_board = []\n"
    "def show_on_ley_board(text):\n"
    "    _board.append(text)\n"
    "    print('[Ley board] ' + str(text))\n"
)
GREETING_PICK = "WELCOME BACK, LUCKY. WIPE YOUR BOOTS."


def _greet(words="WELCOME TO THE CABIN.", present="    pass\n", tidy=True, tail="present_greeting()\n"):
    tidy_lines = "    line = line.lower()\n    line = line.capitalize()\n" if tidy else ""
    return (
        "# 1. Change the words inside the quotes to a greeting Mar'tu gives Lucky.\n"
        "def get_greeting():\n"
        f'    line = "{words}"\n'
        + tidy_lines +
        "    return line\n"
        "\n\n"
        "# 2. Finish present_greeting(): store the result of get_greeting() in a variable.\n"
        "# 3. Pass that variable to show_on_ley_board().\n"
        "def present_greeting():\n"
        + present +
        "\n\n"
        "# The Ley board calls your recipe, like the game did:\n"
        + tail
    )


GREET_STARTER = _greet()
STORE = "    greeting = get_greeting()\n"
PASS_ON = "    show_on_ley_board(greeting)\n"
GREET_SOLUTION = _greet(words=GREETING_PICK, present=STORE + PASS_ON)

_GREETING = r'''
_f, _m = _find('get_greeting', True)
assert _f, _m
_attrs = set(_n.attr for _n in _ast.walk(_defs()['get_greeting']) if type(_n).__name__ == 'Attribute')
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'get_greeting', (), _err)
assert not (type(_v).__name__ == 'str' and not _v.strip()), (
    'Put some words between the quotes on the `line = ` line: a greeting for Lucky. Any words work.')
assert type(_v).__name__ == 'str', (
    'Keep `return line` at the end of `get_greeting()`, so it hands back the greeting as text.')
assert _v.strip().rstrip('.!?').lower() != 'welcome to the cabin', (
    'Change the words inside the quotes on the `line = ` line to a greeting of your own for Lucky. Any words work.')
assert 'lower' in _attrs and 'capitalize' in _attrs, (
    'Keep the two tidy lines: `line = line.lower()`, then `line = line.capitalize()`.')
assert _v == _v.lower().capitalize(), (
    'Keep the tidy lines in order, each stored back in `line`: `.lower()` first, then `.capitalize()`.')
'''

_STORED = r'''
_fs, _m = _find('present_greeting', True)
assert _fs, _m
_d = _defs()['present_greeting']


def _helper(_x):
    return ((type(_x).__name__ == 'Call' and type(_x.func).__name__ == 'Name' and _x.func.id == 'get_greeting')
            or (type(_x).__name__ == 'Name' and _x.id == 'get_greeting'))


_stored = [_n.targets[0].id for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
           and type(_n.targets[0]).__name__ == 'Name' and _helper(_n.value)]
'''

_STORE = _STORED + r'''
_outside = [_n.lineno for _n in _tree.body if type(_n).__name__ == 'Assign' and _helper(_n.value)]
_direct = [_c for _c in _calls_in([_d], 'show_on_ley_board') if any(_helper(_a) for _a in _c.args)]
_only_pass = all(type(_s).__name__ in ('Pass', 'Expr') and (type(_s).__name__ == 'Pass' or
                 type(_s.value).__name__ == 'Constant') for _s in _d.body)
if not _stored:
    assert not _outside, 'Put the store line inside `present_greeting()`, indented four spaces, where `pass` was.'
    assert not _direct, ('Store the line in a variable first, as the campaign asks: `greeting = get_greeting()`. '
                         'Then pass that variable on.')
    assert not _only_pass, ('`present_greeting()` still only says `pass`. Replace it with a line that stores the result '
                            'of `get_greeting()` in a variable.')
    assert False, 'Inside `present_greeting()`, store the result of `get_greeting()` in a variable: `greeting = get_greeting()`.'
'''

_PASS_ON = _STORED + r'''
_G = _fs.__globals__
_board = _G['_board']
_evp = " (Mar'tu's check called `present_greeting()`, only inside the check: "
_at = len(_board)
_v, _rows, _err, _c = _run(_fs, ())
assert not _err, _why(_fs, 'present_greeting', (), _err)
_shown = _board[_at:]
assert _shown, ('Pass that variable to the board: `show_on_ley_board(greeting)`, indented under the store line.'
                + _evp + 'the board showed nothing.)')
assert type(_shown[0]).__name__ != 'function', ('The board showed a recipe, not its words: add `()` to call it, '
                                                '`get_greeting()`.' + _evp + 'the board showed the function '
                                                '`get_greeting` itself.)')
_real = _G['get_greeting']
_want, _r2, _e2, _c2 = _run(_real, ())
assert _shown[0] == _want, ('Pass the variable that holds the greeting, so the board shows what `get_greeting()` '
                            'hands back.' + _evp + 'the board showed other words.)')
_G['get_greeting'] = lambda: 'A grumpy moth says hello.'
try:
    _at2 = len(_board)
    _v2, _rows2, _err2, _c2 = _run(_fs, ())
finally:
    _G['get_greeting'] = _real
_shown2 = _board[_at2:]
assert _shown2 and _shown2[0] == 'A grumpy moth says hello.', (
    "Pass the variable, not typed words, so the board shows whatever `get_greeting()` hands back. (Mar'tu's check "
    'made `get_greeting()` hand back another line, only inside the check: the board did not show it.)')
_args = [_a for _c in _calls_in([_d], 'show_on_ley_board') for _a in _c.args]
_late = [_a for _a in _args if type(_a).__name__ == 'Call' and type(_a.func).__name__ == 'Name' and _a.func.id in _stored]
assert not _late, ('Store what `get_greeting()` hands back, with `()` on the store line: `greeting = get_greeting()`. '
                   'Then pass the variable as it is: `show_on_ley_board(greeting)`.')
assert any(type(_a).__name__ == 'Name' and _a.id in _stored for _a in _args), (
    'Pass the variable itself: `show_on_ley_board(greeting)`. Your line calls `get_greeting()` again instead.')
'''

STORE_THEN_PASS = dict(
    id="store-then-pass",
    title="Store, then pass it on",
    martu=(
        "`get_greeting()` hands back a line. Look how it tidies the line: `.lower()` makes every letter small, then "
        "[[.capitalize()]] makes the first letter big.\n"
        "`present_greeting()` must store that line in a variable (a box), then pass the variable on to the Ley "
        "board.\n"
        "Three moves: call the helper, store what it hands back, pass it on. You did this in Module 1, yes? Now you "
        "see why it works."
    ),
    introduces=["attr:capitalize"],
    setup=BOARD_SETUP,
    names=["get_greeting", "present_greeting", "show_on_ley_board"],
    pick=GREETING_PICK,
    predict=dict(
        q="Before you change anything: what does `get_greeting()` hand back?",
        code=(
            "def get_greeting():\n"
            '    line = "WELCOME TO THE CABIN."\n'
            "    line = line.lower()\n"
            "    line = line.capitalize()\n"
            "    return line\n"
            "\n"
            "print(get_greeting())\n"
        ),
        choices=["WELCOME TO THE CABIN.", "welcome to the cabin.", "Welcome to the cabin.", "Welcome To The Cabin."],
        answer=2,
        explain=(
            "`Welcome to the cabin.` First `.lower()` makes every letter small: `welcome to the cabin.` Then "
            "`.capitalize()` makes only the very first letter big. Each line stores the tidy copy back in `line`."
        ),
    ),
    starter=GREET_STARTER,
    checkpoints=[
        dict(
            id="your-greeting",
            text="Change the words inside the quotes to a greeting Mar'tu gives Lucky.",
            dictated=False,
            hints=[
                "Look at the first line inside `get_greeting()`: the words in quotes are the greeting. The next two "
                "lines tidy them.",
                "Any words work, even shouting. `.lower()` then `.capitalize()` would turn `\"SIT DOWN, LUCKY.\"` "
                "into `Sit down, lucky.`",
                "Change only the words between the quotes, like "
                "`line = \"WELCOME BACK, LUCKY. WIPE YOUR BOOTS.\"`, or words of your own.",
            ],
            checks=[("get_greeting hands back your tidy greeting", _FN + _GREETING)],
            pass_line="Mar'tu: Lucky pretends he didn't like that.",
        ),
        dict(
            id="store-the-greeting",
            text="Finish `present_greeting()`: store the result of `get_greeting()` in a variable.",
            dictated=True,
            hints=[
                "Which recipe hands back the line? Call it on the right of `=`, with `()`.",
                "`note = get_note()` catches what `get_note` hands back, and keeps it in `note`.",
                "Write `greeting = get_greeting()` in place of `pass`, four spaces in.",
            ],
            checks=[("the greeting is stored in a variable", _FN + _STORE)],
        ),
        dict(
            id="pass-it-on",
            text="Pass that variable to `show_on_ley_board()`.",
            dictated=True,
            hints=[
                "Which box holds the greeting now? Hand that box to the board.",
                "A box can be handed to a recipe: `read_aloud(note)` hands over what `note` holds.",
                "Write `show_on_ley_board(greeting)` under the store line, four spaces in.",
            ],
            checks=[("the board shows the stored greeting", _FN + _PASS_ON)],
            pass_line="Lucky: I'm on a board. Finally, some respect.",
        ),
    ],
    solution=GREET_SOLUTION,
    partials=[_greet(words=GREETING_PICK), _greet(words=GREETING_PICK, present=STORE)],
    assemble=dict(
        lines=["def get_greeting():", f'    line = "{GREETING_PICK}"', "    line = line.lower()",
               "    line = line.capitalize()", "    return line", "def present_greeting():",
               "    greeting = get_greeting()", "    show_on_ley_board(greeting)", "present_greeting()"],
        distractors=["    show_on_ley_board(get_greeting)", "    get_greeting = greeting"],
    ),
    another_way=[
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Module 1: `get_dialogue_prompt_string()` handed back Mar'tu's line. `present_dialogue_option()` "
                "stored it in a variable, then passed that variable to `print_prompt()`. Same three moves."
            ),
        ),
        dict(
            angle="step-by-step",
            label="Three moves",
            text=(
                "1. Call the helper: `get_greeting()`.\n"
                "2. Store what it hands back: `greeting = get_greeting()`.\n"
                "3. Pass it on: `show_on_ley_board(greeting)`."
            ),
        ),
        dict(
            angle="picture",
            label="A note passed along",
            text=(
                "```text\nget_greeting()\n   | hands back the line\n   v\ngreeting  (stored)\n   |\n   v\n"
                "show_on_ley_board(greeting)\n```"
            ),
        ),
        dict(
            angle="everyday",
            label="Collect a parcel",
            text=(
                "Collect the parcel at the door and hold it. Then hand it to the person who needs it. You don't "
                "hand them the door."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky wants a goodbye too. Add `get_farewell()` with its own tidied line. Make `present_greeting()` "
            "show the greeting first, then the farewell."
        ),
        hints=[
            "In `present_greeting()`: store and pass the greeting, then store and pass the farewell.",
            "Write `def get_farewell():` with the same three steps as `get_greeting()`. Then, inside "
            "`present_greeting()`, add `farewell = get_farewell()` and `show_on_ley_board(farewell)`.",
        ],
        checks=[
            (
                "the board shows the greeting, then the farewell",
                _FN + r'''
_ff, _m = _find('get_farewell')
assert _ff, _m
_fv, _r, _e, _c = _run(_ff, ())
assert not _e, _why(_ff, 'get_farewell', (), _e)
assert type(_fv).__name__ == 'str' and _fv.strip() and _fv == _fv.lower().capitalize(), (
    'Make `get_farewell()` hand back a tidied line, like `get_greeting()`: `.lower()`, then `.capitalize()`.')
_fs, _m = _find('present_greeting', True)
assert _fs, _m
_gv, _r, _e, _c = _run(_fs.__globals__['get_greeting'], ())
assert _fv != _gv, 'Give the farewell its own words, different from the greeting.'
_board = _fs.__globals__['_board']
_at = len(_board)
_v, _rows, _err, _c = _run(_fs, ())
assert not _err, _why(_fs, 'present_greeting', (), _err)
assert _board[_at:] == [_gv, _fv], (
    'Make `present_greeting()` show the greeting first, then the farewell: store each one, then pass each to '
    '`show_on_ley_board()`.')
''',
            ),
        ],
        solution=_greet(words=GREETING_PICK, present=STORE + PASS_ON + "    farewell = get_farewell()\n"
                        "    show_on_ley_board(farewell)\n", tail=(
                            "def get_farewell():\n"
                            '    line = "REST WELL, LUCKY."\n'
                            "    line = line.lower()\n"
                            "    line = line.capitalize()\n"
                            "    return line\n"
                            "\n"
                            "present_greeting()\n")),
    ),
    campaign_link=dict(
        module="leylines-awaken",
        part="program-dialogue-prompt",
        snippet="def present_dialogue_option():\n    dialogue = get_dialogue_prompt_string()\n    print_prompt(dialogue)",
        why=(
            "You have seen this in Module 1. `get_dialogue_prompt_string()` handed back Mar'tu's line. "
            "`present_dialogue_option()` stored it in a variable, then passed that variable to `print_prompt()`. "
            "Same three moves today."
        ),
    ),
    takeaway="Call the helper, store what it hands back, pass the variable on. `.lower()` then `.capitalize()` tidies text.",
    wrong_answers=[
        dict(why="the words left as the starter's", code=_greet(present=STORE + PASS_ON), fails_at=1,
             message_contains="Change the words"),
        dict(why="the words deleted: empty quotes (the old message said 'keep return line')",
             code=_greet(words="", present=STORE + PASS_ON), fails_at=1, message_contains="between the quotes"),
        dict(why="the tidy lines deleted", code=_greet(words="Welcome back, LUCKY.", present=STORE + PASS_ON, tidy=False),
             fails_at=1, message_contains="tidy"),
        dict(why="a tidy copy made and forgotten (`line.lower()` on its own line)",
             code=_greet(words=GREETING_PICK, present=STORE + PASS_ON).replace("line = line.lower()", "line.lower()")
             .replace("line = line.capitalize()", "line.capitalize()"),
             fails_at=1, message_contains="stored back"),
        dict(why="no store: the call passed straight to the board (STO)",
             code=_greet(words=GREETING_PICK, present="    show_on_ley_board(get_greeting())\n"), fails_at=2,
             message_contains="variable"),
        dict(why="the store line outside the recipe, pass left",
             code=_greet(words=GREETING_PICK, tail="greeting = get_greeting()\nshow_on_ley_board(greeting)\npresent_greeting()\n"),
             fails_at=2, message_contains="inside"),
        dict(why="the line typed into the board call (CMB)",
             code=_greet(words=GREETING_PICK, present=STORE + '    show_on_ley_board("Welcome back, lucky. wipe your boots.")\n'),
             fails_at=3, message_contains="another line"),
        dict(why="no () on the helper: the recipe itself stored and passed (CALL)",
             code=_greet(words=GREETING_PICK, present="    greeting = get_greeting\n" + PASS_ON), fails_at=3,
             message_contains="function"),
        dict(why="stored but never passed", code=_greet(words=GREETING_PICK, present=STORE), fails_at=3,
             message_contains="nothing"),
        dict(why="stored, then the helper called again in the board call (the variable not passed)",
             code=_greet(words=GREETING_PICK, present=STORE + "    show_on_ley_board(get_greeting())\n"), fails_at=3,
             message_contains="variable itself"),
        dict(why="the recipe itself stored (no `()`), then called inside the board call",
             code=_greet(words=GREETING_PICK, present="    greeting = get_greeting\n    show_on_ley_board(greeting())\n"),
             fails_at=3, message_contains="with `()` on the store line"),
        dict(why="the store reversed: get_greeting = greeting",
             code=_greet(words=GREETING_PICK, present="    get_greeting = greeting\n    show_on_ley_board(greeting)\n"),
             fails_at=0, message_contains="greeting"),
        dict(why="the Teach me hint's names copied (`note = get_note()`; the explainer names the task's recipe)",
             code=_greet(words=GREETING_PICK, present="    note = get_note()\n    show_on_ley_board(note)\n"), fails_at=0,
             message_contains="name 'get_note' is not defined"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="store-then-pass,chain-methods", solo="false", dictates="2,3",
             foreign_names="note,get_note,read_aloud", rehearsal="program-dialogue-prompt", stages="P,I,M",
             twin="get_warning() / present_warning()") + "\n"
        "Rehearsal: numbered comments map 1:1 onto the checkpoints, and the text copies the campaign's phrasing "
        "('store the result of ... in a variable', 'Pass that variable to ...'). The starter ends with the board's "
        "call (the campaign's game called present_dialogue_option for them), so Run shows the board. CMB: the check "
        "swaps get_greeting for another line in the recipe's own globals, calls present_greeting, and puts the real "
        "one back. CP2 accepts a store with or without `()`, so the no-() slip reaches CP3, where the board shows a "
        "function (the spec's WA). CP3 reads only the board's first line, so Lucky's farewell keeps it green. Any "
        "greeting passes (lint e), never repeated back."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-09 return-a-comparison (rehearsal: skill-checks)
# ---------------------------------------------------------------------------------------------


def _strength(needed="12", ret="return roll >= needed", comments=True, tail=None):
    out = "def strength_check(roll):\n    # Bomb Shell pries the trap door.\n"
    if comments:
        out += "    # 1. Set needed to how hard this is, a number from 2 to 20.\n"
    out += f"    needed = {needed}\n"
    if comments:
        out += "    # 2. Replace return False with: return roll >= needed\n"
    out += f"    {ret}\n"
    return out + (tail if tail is not None else "\n# Mar'tu rolls a 15 to try it:\nprint(strength_check(15))\n")


STRENGTH_STARTER = _strength(needed="0", ret="return False")
STRENGTH_SOLUTION = _strength()

_NEEDED = r'''
_fn = _defs().get(__NAME__)
assert _fn, 'Keep the recipe `' + __NAME__ + '` from the starter, with its `def` line.'
_asg = [_n for _n in _ast.walk(_fn) if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
        and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'needed']
_outer = [_n for _n in _tree.body if type(_n).__name__ == 'Assign' and any(type(_t).__name__ == 'Name'
          and _t.id == 'needed' for _t in _n.targets)]
assert _asg or not _outer, ('Set `needed` inside `' + __NAME__ + '`, indented under its `def` line, where the '
                            'starter has it.')
assert _asg, 'Keep the line `needed = 0` inside `' + __NAME__ + '`, and change the 0.'
_val = _asg[-1].value
assert type(_val).__name__ == 'Constant', 'Set `needed` to a plain number from 2 to 20, like `needed = 12`.'
_N = _val.value
assert type(_N).__name__ != 'str', 'Numbers don' + chr(39) + 't need quotes: `needed = 12`, not `needed = "12"`.'
assert type(_N).__name__ == 'int', 'Set `needed` to a whole number from 2 to 20.'
assert _N != 0, ('`needed` still holds the starter' + chr(39) + 's `0`. Pick how hard prying the door is: a number '
                 'from 2 to 20.')
assert 2 <= _N <= 20, ('A d20 rolls 1 to 20, so pick `needed` from 2 to 20. '
                       + ('Above 20 could never pass.' if _N > 20 else 'Below 2 always passes.'))
'''

_BND = r'''
_name = __NAME__
_f, _m = _find(_name, __KEPT__)
assert _f, _m
_fn = _defs().get(_name)
_asg = [_n for _n in _ast.walk(_fn) if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
        and type(_n.targets[0]).__name__ == 'Name' and _n.targets[0].id == 'needed'] if _fn else []
_N = _asg[-1].value.value if _asg and type(_asg[-1].value).__name__ == 'Constant' else None
assert type(_N).__name__ == 'int' and 2 <= _N <= 20, (
    'First set `needed` inside `' + _name + '` to a whole number from 2 to 20.')
assert len(_params(_f)) == 1, '`' + _name + '` takes one ingredient, `roll`: keep `def ' + _name + '(roll):`.'
_rev = [1 for _n in _ast.walk(_fn) if type(_n).__name__ == 'Compare' and len(_n.ops) == 1
        and (getattr(_n.left, 'id', ''), type(_n.ops[0]).__name__, getattr(_n.comparators[0], 'id', ''))
        in (('needed', 'GtE', 'roll'), ('roll', 'LtE', 'needed'))]
_msg = ''
for _r in [_x for _x in (_N - 1, _N, _N + 1, 1, 20) if 1 <= _x <= 20]:
    _v, _rows, _err, _c = _run(_f, (_r,))
    _with = (" (Mar'tu's check called `" + _name + '(' + str(_r) + ')` with `needed = ' + str(_N)
             + '`, only inside the check: ')
    if _err:
        _msg = _why(_f, _name, (_r,), _err)
    elif _v is None:
        _msg = (('Hand the answer back with `return`. `print` only shows it on the screen.' + _with
                 + 'it printed a line but handed back `None`.)') if _rows else
                ('End the recipe with a `return` line that hands back `True` or `False`.' + _with
                 + 'it handed back `None`.)'))
    elif type(_v).__name__ != 'bool':
        _msg = ('Hand back `True` or `False`: return the comparison itself, `roll >= needed`.' + _with
                + 'it handed back something that is not True or False.)')
    elif _v != (_r >= _N):
        if _rev:
            _msg = 'Your sign faces the wrong way: it asks *at most*. *At least* is `roll >= needed`.'
        elif _r == _N:
            _msg = 'Exactly enough should pass: use `>=`, at least.'
        elif _r < _N:
            _msg = 'One short should fail. Make the answer depend on the roll: `roll >= needed`.'
        else:
            _msg = 'A roll above `needed` should pass: `roll >= needed`.'
        _msg += _with + 'it handed back `' + str(_v) + '`.)'
    if _msg:
        break
if not _msg:
    # Rebuild the recipe with another `needed`, so a typed number (`roll >= 12`) is caught.
    _M = _N + 3 if _N + 3 <= 20 else _N - 3
    _t2 = _ast.parse(_source)
    _d2 = [_n for _n in _t2.body if type(_n).__name__ == 'FunctionDef' and _n.name == _name][-1]
    for _n in _ast.walk(_d2):
        if (type(_n).__name__ == 'Assign' and len(_n.targets) == 1 and type(_n.targets[0]).__name__ == 'Name'
                and _n.targets[0].id == 'needed' and type(_n.value).__name__ == 'Constant'):
            _n.value = _ast.copy_location(_ast.Constant(_M), _n.value)
    _mod = _ast.Module(body=[_d2], type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _ns2 = dict(_f.__globals__)
    exec(compile(_mod, 'main.py', 'exec'), _ns2)
    # needed + 1 too: with `needed = 20`, `roll == needed` matches `>=` on every d20 roll, so only a moved
    # `needed` shows that a roll above it fails.
    for _r, _want in ((_M - 1, False), (_M, True), (_M + 1, True)):
        _v, _rows, _err, _c = _run(_ns2[_name], (_r,))
        if _err or _v != _want:
            _lead = ('A roll above `needed` should pass too: use `>=`, at least.' if _r == _M + 1 and not _err
                     else 'Compare with the box: `roll >= needed`, not a typed number.')
            _msg = (_lead + " (Mar'tu's check changed "
                    '`needed` to ' + str(_M) + ' and called `' + _name + '(' + str(_r) + ')`, only inside the check: '
                    'it handed back ' + ('an error' if _err else '`' + str(_v) + '`') + '.)')
            break
_rs = _resets(_name)
assert not (_msg and _rs), _rs
assert not _msg, _msg
'''


def needed_check(name="strength_check"):
    return (f"needed is set in {name}", _FN + _NEEDED.replace("__NAME__", repr(name)))


def bnd_check(label, name="strength_check", kept=True):
    return (label, _FN + _BND.replace("__NAME__", repr(name)).replace("__KEPT__", repr(kept)))


SPOT_EXAMPLE = (
    "def spot_check(roll):\n"
    "    target = 14\n"
    "    if roll >= target:\n"
    "        return True\n"
    "    else:\n"
    "        return False\n"
    "\n"
    "def spot_check_short(roll):\n"
    "    target = 14\n"
    "    return roll >= target\n"
    "\n"
    "print(spot_check(14))\n"
    "print(spot_check_short(14))\n"
)

RETURN_A_COMPARISON = dict(
    id="return-a-comparison",
    title="Return a comparison",
    martu=(
        "A skill check hands back `True` or `False`. The Example shows two ways to write one: an `if` that returns "
        "`True` or `False`, and one short line.\n"
        "`roll >= needed` is already a question with a True or False answer. So you can hand back the answer "
        "itself: `return roll >= needed`.\n"
        "Follow the numbered comments, one per step."
    ),
    example=SPOT_EXAMPLE,
    example_output="True\nTrue",
    names=["strength_check", "roll", "needed"],
    pick="12",
    predict=dict(
        q="Before you press Run: what will this print?",
        code=(
            "def door_check(roll):\n"
            "    needed = 15\n"
            "    return roll >= needed\n"
            "\n"
            "print(door_check(14))\n"
            "print(door_check(15))\n"
        ),
        choices=["False\nTrue", "False\nFalse", "True\nTrue", "14\n15"],
        answer=0,
        explain=(
            "14 is one short of 15: `False`. 15 is exactly enough, and `>=` means at least: `True`. The recipe "
            "hands back the answer to the question, not the roll."
        ),
    ),
    starter=STRENGTH_STARTER,
    checkpoints=[
        dict(
            id="set-needed",
            text="Set `needed` to how hard prying the door should be, from 2 to 20.",
            dictated=True,
            hints=[
                "A d20 rolls 1 to 20. Easy is low, hard is high. Any number from 2 to 20 works.",
                "A box gets a number with `name = value`, no quotes: `target = 14`.",
                "Write `needed = 12` in place of `needed = 0`, or any number from 2 to 20.",
            ],
            checks=[needed_check()],
            pass_line="Bomb Shell: That latch hates me.",
        ),
        dict(
            id="return-the-comparison",
            text="Replace `return False` with `return roll >= needed`.",
            dictated=True,
            hints=[
                "What should a roll of exactly `needed` give? Exactly enough passes.",
                "These two do the same job:\n```python\nif roll >= target:\n    return True\nelse:\n"
                "    return False\n```\nand `return roll >= target`. The comparison is already `True` or `False`.",
                "Write `return roll >= needed` in place of `return False`.",
            ],
            checks=[bnd_check("the check passes from needed up")],
            pass_line="Bomb Shell: It opens. Finally.",
        ),
    ],
    solution=STRENGTH_SOLUTION,
    partials=[_strength(ret="return False")],
    assemble=dict(
        lines=["def strength_check(roll):", "    needed = 12", "    return roll >= needed", "print(strength_check(15))"],
        distractors=["    return roll > needed", "    return True"],
    ),
    another_way=[
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "At the trap door, each check set `required_roll`, then handed back `roll >= required_roll`. Same "
                "shape here, with `needed`."
            ),
        ),
        dict(
            angle="step-by-step",
            label="The two forms are the same",
            text=(
                "1. `roll >= needed` is a question. Python answers it: `True` or `False`.\n"
                "2. The long form asks it in an `if`, then hands back `True` or `False` by hand.\n"
                "3. The short form hands back the answer straight away. Same result, one line."
            ),
        ),
        dict(
            angle="picture",
            label="A number line",
            text="```text\n1 ... needed-1 | needed ... 20\n     False     |     True\n```",
        ),
        dict(angle="shorter", text="`return roll >= needed`. Exactly enough passes."),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky tries the latch with a shim. Write `dexterity_check(roll)` with its own `needed`. Then print both "
            "checks for a roll of 12."
        ),
        hints=[
            "Same shape as `strength_check`, with its own `needed`. Then print both checks for a roll of 12.",
            "Write `def dexterity_check(roll):` with its own `needed = ` line and `return roll >= needed`. Then "
            "`print(strength_check(12))` and `print(dexterity_check(12))`.",
        ],
        checks=[
            bnd_check("dexterity_check passes from its own needed up", name="dexterity_check", kept=False),
            (
                "both checks are printed for a roll of 12",
                _FN + r'''
for _n in ('strength_check', 'dexterity_check'):
    _ok = [_c for _c in _calls_in(_top(), 'print') for _x in _calls_in([_c], _n)
           if len(_x.args) == 1 and type(_x.args[0]).__name__ == 'Constant' and _x.args[0].value == 12]
    assert _ok, 'Print both checks for a roll of 12: `print(' + _n + '(12))`.'
''',
            ),
        ],
        solution=STRENGTH_SOLUTION + (
            "\ndef dexterity_check(roll):\n"
            "    # Lucky slides a shim under the latch.\n"
            "    needed = 15\n"
            "    return roll >= needed\n"
            "\nprint(strength_check(12))\nprint(dexterity_check(12))\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def strength_check(roll):\n    required_roll = 12\n    return roll >= required_roll",
        why=(
            "You have seen this at the trap door. Each check set how hard it was, then handed back the answer to "
            "`roll >= required_roll`. Now you know why that one line was enough."
        ),
    ),
    takeaway="A comparison is already True or False: `return roll >= needed` hands back the answer.",
    wrong_answers=[
        dict(why="needed = 25 (no d20 roll can pass)", code=_strength(needed="25"), fails_at=1,
             message_contains="from 2 to 20"),
        dict(why="needed left at 0", code=_strength(needed="0"), fails_at=1, message_contains="starter"),
        dict(why="needed in quotes (the try line stops with a TypeError; the explainer's text-vs-number row)",
             code=_strength(needed='"12"'), fails_at=0, message_contains="'>=' not supported"),
        dict(why="needed in quotes, with the try line removed (the check names the quotes)",
             code=_strength(needed='"12"', tail=""), fails_at=1, message_contains="quotes"),
        dict(why="return True (BND: every roll passes)", code=_strength(ret="return True"), fails_at=2,
             message_contains="One short"),
        dict(why="> instead of >= (the campaign's < versus <= trap)", code=_strength(ret="return roll > needed"),
             fails_at=2, message_contains="exactly"),
        dict(why="print instead of return (RET)", code=_strength(ret="print(roll >= needed)"), fails_at=2,
             message_contains="None"),
        dict(why="a typed number: roll >= 12 (needed set to 12, so it passes until needed moves)",
             code=_strength(ret="return roll >= 12"), fails_at=2, message_contains="typed"),
        dict(why="the sign faces the wrong way: needed >= roll", code=_strength(ret="return needed >= roll"),
             fails_at=2, message_contains="wrong way"),
        dict(why="the if form with no else: a low roll falls off the end and hands back None",
             code=_strength(ret="if roll >= needed:\n        return True"), fails_at=2, message_contains="None"),
        dict(why="the if form returning words instead of True or False",
             code=_strength(ret='if roll >= needed:\n        return "pass"\n    else:\n        return "fail"'),
             fails_at=2, message_contains="True or False"),
        dict(why="return False left in place", code=_strength(ret="return False"), fails_at=2,
             message_contains="Exactly"),
        dict(why="== instead of >= with needed = 20 (the same on every d20 roll until needed moves)",
             code=_strength(needed="20", ret="return roll == needed"), fails_at=2, message_contains="above"),
        dict(why="the roll refilled inside the recipe (B-02: the call's value goes in the body)",
             code=_strength(ret="roll = 15\n    return roll >= needed"), fails_at=2, message_contains="thrown away"),
        dict(why="needed set at the top level, outside the recipe",
             code="needed = 12\n\n" + _strength(needed="0").replace("    needed = 0\n", ""), fails_at=1,
             message_contains="inside"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="return-comparison,boundary", solo="false", dictates="1,2",
             foreign_names="spot_check,spot_check_short,target", rehearsal="skill-checks", stages="P,I,M",
             seal_variant="prerequisite card 2-A2: seal strength_check with three assert lines at the boundary "
                          "(optional; node:Assert is optional-only, so not the side quest)") + "\n"
        "BND reads `needed` from the student's own recipe, so any difficulty from 2 to 20 passes (lint e), then "
        "rebuilds the recipe with `needed` moved by 3 and tries needed - 1, needed and needed + 1, so a typed number "
        "is caught, and so is `roll == needed` with `needed = 20` (the same as `>=` on every d20 roll until needed "
        "moves). The if/else form passes too "
        "(checked in the harness probe). The starter ends with a try line (the campaign's game rolled for them), "
        "so Run shows `False`, then `True` or `False` once the step is done."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-10 roll-recipe (rehearsal: perform_roll)
# ---------------------------------------------------------------------------------------------


def _roll(ret="return random.randint(1, die_size)", head="import random\n\n", comment=True):
    return (
        head
        + "def roll_die(die_size):\n"
        + ("    # 1. Replace return 1 with a random whole number from 1 to die_size.\n" if comment else "")
        + f"    {ret}\n"
        + "\n# Mar'tu rolls a d20 to try it:\nprint(roll_die(20))\n"
    )


ROLL_STARTER = _roll(ret="return 1")

_RND = r'''
_f, _m = _find('roll_die', True)
assert _f, _m
assert len(_params(_f)) == 1, '`roll_die` takes one ingredient, `die_size`: keep `def roll_die(die_size):`.'
_g = _gamed('roll_die', [6, 20, 12])
assert not _g, _g
_msg = ''
for _faces, _roll in ((6, 4), (20, 17), (12, 9)):
    _v, _rows, _err, _calls = _run(_f, (_faces,), [_roll])
    _evd = (" (Mar'tu's check called `roll_die(" + str(_faces) + ")` with a pretend die that always lands on "
            + str(_roll) + ', only inside the check: ')
    if _err:
        _msg = _why(_f, 'roll_die', (_faces,), _err)
    elif not _calls:
        _msg = (('`roll_die` still hands back 1 every time. ' if _v == 1 else '')
                + 'Roll with `random.randint`, from 1 to `die_size`.' + _evd + 'nothing was rolled.)')
    elif tuple(_calls[0]) != (1, _faces):
        _a, _b = _calls[0]
        if _a == 0:
            _lead = 'Dice start at 1: roll from 1 to `die_size`.'
        elif (_a, _b) == (_faces, 1):
            _lead = 'Smallest number first: `random.randint(1, die_size)`.'
        elif _a == 1 and _b in (_faces - 1, _faces + 1):
            _lead = 'Both ends are included, so roll from 1 to `die_size` itself.'
        else:
            _lead = 'Use the ingredient: roll from 1 to `die_size`, not a typed number.'
        _msg = _lead + _evd + 'it rolled `random.randint(' + str(_a) + ', ' + str(_b) + ')`.)'
    elif _v is None:
        _msg = (('Hand the roll back with `return`. `print` only shows it.' if _rows else 'Hand the roll back with `return`.')
                + _evd + 'it handed back `None`.)')
    elif _v != _roll:
        _msg = 'Hand back the roll itself, the number `random.randint` gives.' + _evd + 'it handed back something else.)'
    if _msg:
        break
_rs = _resets('roll_die')
assert not (_msg and _rs), _rs
assert not _msg, _msg
'''

ROLL_RECIPE = dict(
    id="roll-recipe",
    title="A rolling recipe",
    martu=(
        "At the trap door, `perform_roll(die_size)` rolled the dice for every check. Now you write that recipe "
        "yourself.\n"
        "`die_size` is the ingredient: how many faces the die has. 6 for a d6, 20 for a d20.\n"
        "`random.randint(1, 6)` rolls a d6, both ends included. Here, the number of faces arrives in the "
        "ingredient."
    ),
    names=["roll_die", "die_size", "random"],
    starter=ROLL_STARTER,
    checkpoints=[
        dict(
            id="roll-from-one-to-die-size",
            text="Replace `return 1` with a random whole number from 1 to `die_size`.",
            dictated=False,
            hints=[
                "Which ingredient says how many faces the die has?",
                "`random.randint(1, 6)` rolls a d6, from Unit 2. Both ends are included. Swap the 6 for the ingredient's "
                "name, and every die works.",
                "Write `return random.randint(1, die_size)` in place of `return 1`.",
            ],
            checks=[("roll_die rolls 1 to die_size", _FN + _RND)],
            pass_line="Lucky: Every die we own. Now roll me a twenty.",
        ),
    ],
    solution=_roll(),
    assemble=dict(
        lines=["import random", "def roll_die(die_size):", "    return random.randint(1, die_size)",
               "print(roll_die(20))"],
        distractors=["    return random.randint(1, 20)", "    return random.randint(0, die_size)"],
    ),
    another_way=[
        dict(
            angle="from the campaign",
            label="You've seen this",
            text=(
                "Module 2, the trap door: `perform_roll(die_size)` handed back `random.randint(1, die_size)`. Every "
                "check called it. One recipe, any die."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `roll_die(6)`: `die_size` gets 6.\n"
                "2. `random.randint(1, die_size)` rolls from 1 to 6.\n"
                "3. `return` hands that roll back to the line that called."
            ),
        ),
        dict(
            angle="picture",
            label="A die with die_size faces",
            text="```text\nroll_die(6)   ->  1 to 6\nroll_die(20)  ->  1 to 20\ndie_size sets the top face.\n```",
        ),
    ],
    bonus=dict(
        by="lucky",
        title="What's in it for me?",
        text=(
            "Lucky adds his bonus to every attack. Write `attack_roll(die_size, bonus)`: roll with your own "
            "`roll_die`, then add the bonus."
        ),
        hints=[
            "Inside, call the recipe you just wrote, and add `bonus` to what it hands back.",
            "Write `def attack_roll(die_size, bonus):` with `return roll_die(die_size) + bonus` under it, four "
            "spaces in.",
        ],
        checks=[
            (
                "attack_roll rolls with roll_die and adds the bonus",
                _FN + r'''
_f, _m = _find('attack_roll')
assert _f, _m
assert len(_params(_f)) == 2, '`attack_roll` takes two ingredients: `def attack_roll(die_size, bonus):`.'
assert _calls_in([_defs().get('attack_roll')], 'roll_die'), (
    'Inside `attack_roll`, call your recipe `roll_die(die_size)` instead of rolling again.')
_v, _rows, _err, _calls = _run(_f, (8, 3), [5])
assert not _err, _why(_f, 'attack_roll', (8, 3), _err)
assert _calls and tuple(_calls[0]) == (1, 8), 'Roll with the first ingredient: `roll_die(die_size)`.'
assert _v == 8, ('Hand back the roll plus the bonus.'
                 + " (Mar'tu's check called `attack_roll(8, 3)` with a pretend die that always lands on 5, only "
                 'inside the check: it should hand back 8.)')
''',
            ),
        ],
        solution=_roll() + "\ndef attack_roll(die_size, bonus):\n    return roll_die(die_size) + bonus\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="skill-checks",
        snippet="def perform_roll(die_size):\n    return random.randint(1, die_size)",
        why=(
            "You have seen this at the trap door. You replaced `return 1` with `return random.randint(1, die_size)`. "
            "Now you know why: the die's size arrives as an ingredient, so one recipe rolls any die."
        ),
    ),
    takeaway="`return random.randint(1, die_size)`: the ingredient sets the top face.",
    wrong_answers=[
        dict(why="randint(1, 20) for every die (A-06 test values)", code=_roll(ret="return random.randint(1, 20)"),
             fails_at=1, message_contains="ingredient"),
        dict(why="randint(1, 6) for every die", code=_roll(ret="return random.randint(1, 6)"), fails_at=1,
             message_contains="randint(1, 6)"),
        dict(why="randint(0, die_size) (the exclusive-range belief)", code=_roll(ret="return random.randint(0, die_size)"),
             fails_at=1, message_contains="start at 1"),
        dict(why="randint(1, die_size - 1)", code=_roll(ret="return random.randint(1, die_size - 1)"), fails_at=1,
             message_contains="Both ends"),
        dict(why="return 1 left (the starter)", code=ROLL_STARTER, fails_at=1, message_contains="still hands back 1"),
        dict(why="print instead of return", code=_roll(ret="print(random.randint(1, die_size))"), fails_at=1,
             message_contains="None"),
        dict(why="import random deleted (rule 6b)", code=_roll(head=""), fails_at=0, message_contains="random"),
        dict(why="an if for each of the check's dice (A-08 working backward)",
             code=_roll(ret="if die_size == 6:\n        return random.randint(1, 6)\n    return random.randint(1, 20)"),
             fails_at=1, message_contains="check hands over"),
        dict(why="die_size refilled with 20 inside the recipe (B-02)",
             code=_roll(ret="die_size = 20\n    return random.randint(1, die_size)"), fails_at=1,
             message_contains="thrown away"),
        dict(why="the ends swapped, randint(die_size, 1): the try line stops with Python's empty-range error",
             code=_roll(ret="return random.randint(die_size, 1)"), fails_at=0, message_contains="empty range"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="randint-param", solo="false", dictates="",
             foreign_names="perform_roll", rehearsal="perform_roll (skill-checks)", stages="M") + "\n"
        "RND: random.randint is swapped for a scripted die that records its arguments (and is always put back), "
        "for roll_die(6), (20) and (12). Deterministic: the student's own Run prints a random roll, the checks never "
        "depend on it. No Example (lint 9: no random value in an example_output). `randint(die_size, 1)` stops "
        "the try line with Python's own `empty range` ValueError before any check runs (WA, fails at 0); the "
        "check has a 'smallest number first' message for when the try line is gone."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-11 broken-spell-6a (SC; four slips, one checkpoint each, reported top to bottom)
# ---------------------------------------------------------------------------------------------


def _broken6(colon=":", hours="hours_left = 37", call_first=False, ret="return total"):
    early = "print(max_mana_for(13))\n\n" if call_first else ""
    late = "" if call_first else "print(max_mana_for(13))\n"
    return (
        f"def steady_word(){colon}\n"
        '    return "Steady, now."\n'
        "\n"
        f"{hours}\n"
        "\n"
        + early +
        "def max_mana_for(affinity):\n"
        "    total = affinity * 2\n"
        f"    {ret}\n"
        "\n"
        + late +
        "print(steady_word())\n"
        'print("Hours left: " + str(hours_left))\n'
    )


BROKEN6_STARTER = _broken6(colon="", hours="def hours_left = 37", call_first=True, ret="return result")
BROKEN6_SOLUTION = _broken6()

_ORDER = r'''
_d = _defs().get('max_mana_for')
_c = _calls_in(_top(), 'max_mana_for')
assert _c, "Keep the line `print(max_mana_for(13))`. Move it below the recipe; don't delete it."
assert _d and all(_x.lineno > _d.lineno for _x in _c), 'Make the recipe first, then call it: the call goes below the `def` block.'
'''

BROKEN_SPELL_6A = dict(
    id="broken-spell-6a",
    title="Broken spell",
    martu=(
        "Four slips, and Python reports them one at a time. Read the last line of each message first, then go to "
        "the line it names.\n"
        "Mend one, run again, and Python shows you the next. Normal. That is how everyone debugs, yes?"
    ),
    names=["steady_word", "hours_left", "max_mana_for", "total"],
    pair_talk=(
        "Pair talk: compare which line each message names, and why. Each of you mends your own screen."
    ),
    starter=BROKEN6_STARTER,
    checkpoints=[
        dict(
            id="def-line-colon",
            text="Mend the `def` line Python names first.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Python says `expected ':'` on line 1. Look at the very end of that line.",
                "Every `def` line ends with a colon: `def hum():`.",
            ],
            checks=[
                (
                    "steady_word works",
                    _FN + r'''
_f, _m = _find('steady_word', True)
assert _f, _m
_v, _rows, _err, _c = _run(_f, ())
assert not _err, _why(_f, 'steady_word', (), _err)
assert _v == 'Steady, now.', 'Keep `steady_word` handing back `"Steady, now."`.'
''',
                ),
            ],
        ),
        dict(
            id="a-box-not-a-recipe",
            text="Mend the line that should make a box for the hours.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which line does it name?",
                "Python says `expected '('` after `def`. Is `hours_left` a recipe, or a box?",
                "`def` makes a recipe. A box is `name = value`, with no `def`: `steps = 12`.",
            ],
            checks=[
                (
                    "hours_left is a box holding 37",
                    "assert 'hours_left' in globals(), 'Make the box: `hours_left = 37`.'\n"
                    "assert type(hours_left).__name__ != 'function', ('`hours_left` is a recipe now. The task wants a "
                    "box: `hours_left = 37`, with no `def`.')\n"
                    "assert hours_left == 37 and type(hours_left).__name__ == 'int', '`hours_left` should hold 37, with "
                    "no quotes.'\n"
                    "assert 'Hours left: 37' in _lines(), 'Keep the last line, `print(\"Hours left: \" + str(hours_left))`.'\n",
                ),
            ],
        ),
        dict(
            id="make-it-before-calling",
            text="Mend the order, so Python makes `max_mana_for` before the line that calls it.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which name is not defined yet?",
                "Python runs top to bottom. The call comes before the `def` block. Which should come first?",
                "A recipe must be made before it is called:\n```python\ndef hum():\n    print(\"Hmm.\")\n\nhum()\n```",
            ],
            checks=[("the recipe is made before it is called", _FN + _ORDER)],
        ),
        dict(
            id="hand-back-the-right-box",
            text="Mend `max_mana_for` so it hands back the box it made.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which name does it not know?",
                "`result` comes from my Example in Send it back. Which box does this recipe make?",
                "Hand back the box this recipe makes on the line above: write `return total` in place of "
                "`return result`.",
            ],
            checks=[
                returns_check("max_mana_for hands back total", "max_mana_for", ["affinity"], [((9,), 18), ((12,), 24)],
                              fix="Hand back the box the recipe made: `return total`.",
                              foreign=["result", "triple", "n"], box="This recipe's box is `total`."),
            ],
            pass_line="Mar'tu: Four slips, four mends. You read every message. Good.",
        ),
    ],
    solution=BROKEN6_SOLUTION,
    assemble=dict(
        lines=[line for line in BROKEN6_SOLUTION.splitlines() if line.strip()],
        distractors=["def hours_left = 37", "    return result"],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="One slip at a time",
            text=(
                "1. Run. Read the last line of the message.\n"
                "2. Go to the line it names. Mend it.\n"
                "3. Run again. A new message? Good: that is the next slip.\n"
                "4. No message? The checks tell you what is left."
            ),
        ),
        dict(
            angle="picture",
            label="Where each slip is",
            text=(
                "```text\nline 1  def steady_word()\n  needs a colon\nline 4  def hours_left = 37\n"
                "  a box needs no def\nline 6  the call\n  must come after the def\nline 11 return result\n"
                "  hand back total\n```\nThe line numbers are the starter's."
            ),
        ),
        dict(
            angle="shorter",
            text="Colon after `def`. Boxes need no `def`. Make it, then call it. Hand back the box you made.",
        ),
    ],
    takeaway="Read the last line, go to the line it names, mend one slip, run again.",
    wrong_answers=[
        dict(why="the starter (missing colon first)", code=BROKEN6_STARTER, fails_at=0, message_contains="expected ':'"),
        dict(why="colon mended, def still makes the box (the DEF row; A-02)",
             code=_broken6(hours="def hours_left = 37", call_first=True, ret="return result"), fails_at=0,
             message_contains="expected '('"),
        dict(why="two mended, the call still before the def",
             code=_broken6(call_first=True, ret="return result"), fails_at=0,
             message_contains="name 'max_mana_for' is not defined"),
        dict(why="three mended, still returns the Example's name (rule 3)", code=_broken6(ret="return result"),
             fails_at=0, message_contains="'result'"),
        dict(why="hours_left made into a recipe instead of a box",
             code=_broken6(hours="def hours_left():\n    return 37"), fails_at=2, message_contains="box"),
        dict(why="the early call deleted instead of moved",
             code=_broken6().replace("print(max_mana_for(13))\n", ""), fails_at=3, message_contains="Keep the line"),
        dict(why="return 26 (PAR-CONST)", code=_broken6(ret="return 26"), fails_at=4, message_contains="both gave back"),
        dict(why="return affinity (RET-PARAM)", code=_broken6(ret="return affinity"), fails_at=4,
             message_contains="as it came in"),
        dict(why="the ingredient refilled with 13 inside the recipe (B-02)",
             code=_broken6(ret="affinity = 13\n    return affinity * 2"), fails_at=4, message_contains="thrown away"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="read-traceback,def-call,return-right-name", solo="false",
             dictates="", foreign_names="result,triple,n,hum,steps") + "\n"
        "Broken spell, four slips in the order Python reports them: the two SyntaxErrors in file order (the missing "
        "colon -> `expected ':'`; `def hours_left = 37` -> `expected '('`, the DEF row), then the runtime "
        "NameErrors in run order (the call before its def; then `return result`, rule 3). Each slip left fails at 0 "
        "with its own message (WA). No partials: on the site a crash fails every checkpoint. Pair talk: partners "
        "compare which line each message names, and why; every student mends their own screen (SFZ-12)."
    ),
)

# ---------------------------------------------------------------------------------------------
# 6A-S solo-6a (SOLO make-twin, done alone)
# ---------------------------------------------------------------------------------------------

HEAL_STARTER = (
    "def heal(hero_name, amount):\n"
    "    # print the line\n"
    "    pass\n"
    "\n"
    'heal("Oogrish", 4)  # should show: Oogrish heals 4.\n'
    'heal("Lucky", 7)    # should show: Lucky heals 7.\n'
    "\n"
    "def heal_total(health, amount):\n"
    "    # hand back the new health\n"
    "    pass\n"
    "\n"
    "print(heal_total(10, 4))  # should show: 14\n"
)
HEAL_LINE = '    print(hero_name + " heals " + str(amount) + ".")\n'
HEAL_CALLS = 'heal("Oogrish", 4)\nheal("Lucky", 7)\n'
HEAL_TOTAL_PASS = "    # hand back the new health\n    pass\n"
HEAL_TOTAL_LINE = "    return health + amount\n"
HEAL_TOTAL_TRY = "print(heal_total(10, 4))  # should show: 14\n"


def _heal(line=HEAL_LINE, extra='heal("Bomb Shell", 5)\n', total=HEAL_TOTAL_LINE):
    return ("def heal(hero_name, amount):\n" + line + "\n" + HEAL_CALLS + extra
            + "\ndef heal_total(health, amount):\n" + total + "\n" + HEAL_TOTAL_TRY)


SOLO_6A = dict(
    id="solo-6a",
    title="Show Mar'tu",
    martu=(
        "A short one, just for you. `heal` has the same shape as `warn`, with two ingredients this time. Then "
        "`heal_total` hands a number back."
    ),
    solo=True,
    # Teacher ruling (FORMAT.md, from Unit 2 on): every SOLO item is lean. The crash explainer names the kind of
    # slip and the line, never the fix; Python's own last line stays on screen.
    explainer="lean",
    names=["heal", "hero_name", "amount", "heal_total", "health"],
    pick="Bomb Shell",
    starter=HEAL_STARTER,
    checkpoints=[
        dict(
            id="heal-line",
            text="Finish `heal` so both calls show the right line.",
            dictated=False,
            hints=[
                "Both ingredients go in the line: the hero's name, then ` heals `, then the amount, then a period.",
                "A number needs `str()` before it is glued to text: `str(sips)`.",
            ],
            checks=[
                prints_check("each call shows its own hero and amount", "heal", ["hero_name", "amount"],
                             [(("Tester", 6), "Tester heals 6."), (("Moth", 11), "Moth heals 11.")],
                             fix="Use both ingredients, `hero_name` and `amount`, in the line.",
                             const_fix="A recipe gets its values when it is called: use `hero_name` and `amount`, not "
                                       "typed values.",
                             foreign=["warn", "cheer", "name"], safe=["Oogrish heals 4.", "Lucky heals 7."]),
            ],
        ),
        dict(
            id="your-own-heal",
            text="Add a call for your own hero.",
            dictated=False,
            hints=[
                "A hero in quotes, a comma, then a number with no quotes.",
                "Copy the shape of the calls above.",
            ],
            checks=[
                calls_check("heal is called three times", "heal", 3,
                            fix="Add a third call at the bottom: `heal(`, your hero in quotes, a number, then `)`.",
                            example='heal("...", 5)'),
            ],
        ),
        dict(
            id="heal-total",
            text="Finish `heal_total` so it hands back the new health.",
            dictated=False,
            hints=[
                "Look at the `def heal_total` line: its two ingredients are all you need. The comment says what to "
                "hand back.",
                "`def add_coins(coins, found):` with `return coins + found` inside hands back the new count: "
                "`add_coins(3, 2)` hands back 5.",
            ],
            checks=[
                returns_check("heal_total hands back the new health", "heal_total", ["health", "amount"],
                              [((20, 5), 25), ((3, 9), 12)],
                              fix="Use both ingredients, `health` and `amount`, to work out the new health.",
                              const_fix="A recipe gets its numbers when it is called: work the new health out from "
                                        "`health` and `amount`.",
                              none_fix="End `heal_total` with a `return` line that hands back the new health.",
                              foreign=["add_coins", "coins", "found"],
                              rules=[("_v == _a[0] - _a[1]", "Healing adds: the new health goes up by `amount`.")]),
            ],
            pass_line="Mar'tu: You did that on your own. On your map: ✓ two ingredients, ✓ hand a value back with "
                      "`return`.",
        ),
    ],
    solution=_heal(),
    partials=[_heal(extra="", total=HEAL_TOTAL_PASS), _heal(total=HEAL_TOTAL_PASS)],
    another_way=[
        dict(angle="step-by-step", text="1. `hero_name`. 2. `\" heals \"`. 3. `str(amount)`. 4. `\".\"`. Glue them with `+`."),
        dict(angle="shorter", text="Use both ingredient names. `str()` the number."),
        dict(
            angle="from what you know",
            label="Like `max_mana_for`",
            text="`heal_total` works like `max_mana_for`: work the answer out from the ingredients, then hand it back.",
        ),
    ],
    takeaway=(
        "On your own: a recipe with two ingredients, used by name and called three times, and a recipe that hands "
        "its answer back with `return`."
    ),
    wrong_answers=[
        dict(why="one call's line typed in (PAR-CONST)", code=_heal(line='    print("Oogrish heals 4.")\n'), fails_at=1,
             message_contains="Tester"),
        dict(why="the number glued without str()", code=_heal(line='    print(hero_name + " heals " + amount + ".")\n'),
             fails_at=0, message_contains="concatenate"),
        dict(why="the period left out (the near-miss names the first difference, in Mar'tu's values only)",
             code=_heal(line='    print(hero_name + " heals " + str(amount))\n'), fails_at=1,
             message_contains="The `.` at the end is missing"),
        dict(why="the space after the hero left out", code=_heal(line='    print(hero_name + "heals " + str(amount) + ".")\n'),
             fails_at=1, message_contains="A space is missing right after `Tester`"),
        dict(why="values side by side with commas, the period as its own value (print adds a space before it)",
             code=_heal(line='    print(hero_name, "heals", amount, ".")\n'), fails_at=1,
             message_contains="comma inside"),
        dict(why="an approximate parameter name", code=_heal(line='    print(hero + " heals " + str(amount) + ".")\n'),
             fails_at=0, message_contains="'hero'"),
        dict(why="the third call hands over one value", code=_heal(extra='heal("Pip")\n'), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="the third hero two words with no quotes (G3-4, RSWM-2; the explainer's split-on-commas row, in lean "
                 "mode): Python's own words are 'Perhaps you forgot a comma?'",
             code=_heal(extra="heal(Moth Queen, 5)\n"), fails_at=0, message_contains="forgot a comma"),
        dict(why="no third call", code=_heal(extra=""), fails_at=2, message_contains="third call"),
        dict(why="return instead of print (nothing shows)",
             code=_heal(line='    return hero_name + " heals " + str(amount) + "."\n'), fails_at=1,
             message_contains="`print(...)`"),
        dict(why="amount refilled with one call's number (B-02)", code=_heal(line="    amount = 4\n" + HEAL_LINE), fails_at=1,
             message_contains="thrown away"),
        dict(why="an if that looks for the check's own heroes (A-08 working backward)",
             code=_heal(line='    if hero_name == "Tester":\n        print("Tester heals 6.")\n    else:\n'
                             '        print("Moth heals 11.")\n'), fails_at=1, message_contains="check hands over"),
        dict(why="the third call wrapped in print() (the line, then None)", code=_heal(extra='print(heal("Pip", 5))\n'),
             fails_at=2, message_contains="on its own"),
        dict(why="heal_total: the try line's answer typed in, `return 14` (PAR-CONST)",
             code=_heal(total="    return 14\n"), fails_at=3, message_contains="both gave back 14"),
        dict(why="heal_total: print instead of return (RET)", code=_heal(total="    print(health + amount)\n"),
             fails_at=3, message_contains="handed back `None`"),
        dict(why="heal_total: a blank `return` (B-02)", code=_heal(total="    new_health = health + amount\n    return\n"),
             fails_at=3, message_contains="on its own"),
        dict(why="heal_total: worked out, never handed back (no return)",
             code=_heal(total="    new_health = health + amount\n"), fails_at=3, message_contains="`return` line"),
        dict(why="heal_total: an ingredient handed back as it came in (RET-PARAM; A-07)",
             code=_heal(total="    return health\n"), fails_at=3, message_contains="as it came in"),
        dict(why="heal_total: subtracts instead of adding", code=_heal(total="    return health - amount\n"), fails_at=3,
             message_contains="Healing adds"),
        # The explainer's Unit 3 name rows, lean in the SOLO (explain.test.ts reads these by their `why`).
        dict(why="heal_total: hands back a name the recipe never makes (the explainer's not-in-recipe row, lean)",
             code=_heal(total="    return new_health\n"), fails_at=0,
             message_contains="name 'new_health' is not defined"),
        dict(why="an ingredient printed outside its recipe (the explainer's made-inside-recipe row, lean)",
             code=_heal(extra='heal("Bomb Shell", 5)\nprint(hero_name)\n'), fails_at=0,
             message_contains="name 'hero_name' is not defined"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="param-use,return-value", solo="true", dictates="",
             foreign_names="warn,cheer,name,add_coins,coins,found", par='("Tester", 6),("Moth", 11); (20, 5),(3, 9)',
             seat_b="rest_line(hero_name, hours) prints the hero, ' rests ', the hours and 'hours.'") + "\n"
        "SOLO make-twin (6A-04's shape with two ingredients), then one return step (G3-4): `heal_total` hands back "
        "the new health. Its check uses (20, 5) -> 25 and (3, 9) -> 12, which never give the try line's 14, so a "
        "typed `return 14` fails as 'both gave back 14'; print, no return, a blank return and an ingredient handed "
        "back each get their own message (WA). Seat A (and anyone solo) gets heal; seat B would get rest_line once "
        "pair mode ships. Recorded, never blocking, never shown to a partner. The first Recipes I solo informs "
        "placement (run-kit, G3 R10). Any third hero passes, never repeated back. The pass line moved to CP3, the "
        "last step. explainer='lean' (teacher's ruling, every SOLO from Unit 2 on: the explainer names the kind of "
        "slip and the line, not the fix; the unquoted two-word hero shows Python's 'Perhaps you forgot a comma?')."
    ),
)

LESSON_6A = dict(
    kind="lesson",
    id="recipes-with-names",
    title="Recipes With Names",
    minutes=64,
    summary=(
        "Make recipes with `def`, call them, give them ingredients, hand values back with `return`, and rebuild "
        "the campaign's movement, dialogue and skill-check recipes."
    ),
    notes=(
        "Lesson 6A (CC; 6A-11 SC; 6A-05a K, +3 min when shown). Preceded by 6a-remembers. Exactly one SOLO "
        "(solo-6a). Non-dictated checkpoints: 6A-02, 6A-04 CP1-2, 6A-05 CP1-2, 6A-06 CP3 (the capstone), 6A-06b, "
        "6A-07 CP2, 6A-08 CP1, 6A-10, 6A-11, 6A-S. Campaign rehearsals: 6A-03 (program-movement), 6A-08 "
        "(program-dialogue-prompt), 6A-09 (skill-checks), 6A-10 (perform_roll). Moments: 6A-01 (teacher-led) and "
        "6A-06b (the ledger on the board). Rest marker: 6A-06's pass line (Lucky) comes about halfway. Minutes: 61 "
        "core (60, plus about 2 for the 6A-05 predict, the solo's return step and one sentence in 6A-04, minus about "
        "1 for the terse replace-pass steps and the ledger's dropped Example Run), plus 3 for 6A-05a, which shows for "
        "everyone until the site has a contingent flag (teacher's Unit 3 ruling). Non-dictated also: 6A-03 CP4 and "
        "6A-S CP3."
    ),
    exercises=[BOX_OR_RECIPE, CALL_IT, REPLACE_PASS, INGREDIENTS, FILL_THE_INGREDIENTS, USE_THE_INGREDIENTS,
               SEND_IT_BACK, BE_THE_LEDGER, RIGHT_BOX, STORE_THEN_PASS, RETURN_A_COMPARISON, ROLL_RECIPE,
               BROKEN_SPELL_6A, SOLO_6A],
)

# =============================================================================================
# Quiz 6A
# =============================================================================================

QUIZ_6A = dict(
    kind="quiz",
    id="recipe-quiz",
    title="Recipe Quiz",
    minutes=8,
    summary="Eight questions on making, calling and tracing recipes. Retake as often as you like.",
    notes=(
        "Quiz 6A (CC, retrieval for the cliff): 5 predict, 2 mc, 1 parsons. A deliberate change from the spec's mix "
        "(5 predict, 1 mc, 1 parsons, 1 fill): the two near-duplicates (made-not-called, a copy of 6A-01's predict, "
        "and exactly-enough, a third boundary item after 6A-09's predict and latch-boundary) are replaced by the two "
        "cliffs the quiz was missing: numbers typed in ink inside the recipe (numbers-in-ink) and handing back the "
        "right box (return-the-right-box). Review order: right answers first."
    ),
    questions=[
        dict(
            type="predict",
            id="numbers-in-ink",
            q="What will this print?",
            code="def fuel_for(cells):\n    print(4 * 5)\n\nfuel_for(7)\n",
            choices=["20", "35", "an error"],
            answer="20",
            explain="`4 * 5` is written in ink, so every call shows 20. `cells * 5` would show 35 for this call.",
            notes=(
                "PAR-CONST, the worksheet's Part 3 cliff (7 of 11 typed one call's numbers inside the recipe): 6A-05. "
                "35 is the belief that the call's value reaches a recipe that never uses its ingredient."
            ),
        ),
        dict(
            type="predict",
            id="printed-not-returned",
            q="What will this print?",
            code=(
                "def max_mana_for(affinity):\n"
                "    print(affinity * 2)\n"
                "\n"
                "lucky_max = max_mana_for(13)\n"
                "print(lucky_max)\n"
            ),
            choices=["26", "26\n26", "26\nNone", "None"],
            answer="26\nNone",
            explain=(
                "The call prints 26 while it runs. But the recipe has no `return`, so it hands back `None`, and "
                "`lucky_max` holds `None`. `print` shows; `return` hands back."
            ),
            notes="RET (print instead of return; A-07).",
        ),
        dict(
            type="predict",
            id="ledger-again",
            q="Trace it like the ledger. What will this print?",
            code=(
                "def ward_strength(lanterns, runes):\n"
                "    light = lanterns * 10\n"
                "    glow = runes * 5\n"
                "    return light + glow\n"
                "\n"
                "barrier = ward_strength(2, 8) + 10\n"
                "print(barrier)\n"
            ),
            choices=["70", "60", "50", "25", "20"],
            answer="70",
            explain=(
                "`lanterns` holds 2 and `runes` holds 8. `light` is 20, `glow` is 40, so the recipe hands back 60. "
                "Then 60 + 10 is 70.\n"
                "60 forgets the `+ 10` on the `barrier` line. 50 starts from `glow` (40 + 10), not from what the "
                "recipe hands back. 25 adds the numbers written in the recipe (10 + 5 + 10). 20 adds the numbers "
                "handed over (2 + 8 + 10)."
            ),
            notes=(
                "The ledger shape (6A-06b) with (2, 8): rows 2, 8, 20, 40, 60, 70. Predict questions have no "
                "why_wrong, so the ledger's messages for each distractor are in the explain: 60 the + 10 forgotten, "
                "50 started from glow, 25 the constants (10 + 5 + 10: A-03, A-04), 20 the raw inputs (2 + 8 + 10: "
                "A-07). Each distractor comes from one slip only. (1, 6) made 40 ambiguous, and (2, 6) would give 60, "
                "the lesson ledger's own answer."
            ),
        ),
        dict(
            type="predict",
            id="latch-boundary",
            q="What will this print?",
            code=(
                "def latch_check(roll):\n"
                "    needed = 11\n"
                "    return roll >= needed\n"
                "\n"
                "print(latch_check(10))\n"
                "print(latch_check(11))\n"
                "print(latch_check(12))\n"
            ),
            choices=["False\nTrue\nTrue", "False\nFalse\nTrue", "True\nTrue\nTrue", "10\n11\n12"],
            answer="False\nTrue\nTrue",
            explain=(
                "`>=` means at least. 10 is one short: `False`. 11 is exactly enough: `True`. 12 is more: `True`. "
                "The recipe hands back the answer, not the roll."
            ),
        ),
        dict(
            type="mc",
            id="which-is-the-argument",
            q="In `warn(\"Lucky\")`, which part is the argument (what you hand over)?",
            code='def warn(hero_name):\n    print(hero_name + ", get inside!")\n\nwarn("Lucky")\n',
            choices=["warn", '"Lucky"', "hero_name", "()"],
            answer=1,
            why_wrong={
                0: "`warn` is the recipe's name. It says which recipe to run.",
                2: "`hero_name` is the parameter: the ingredient's name on the card. It holds the argument during the "
                   "call.",
                3: "The brackets make the call happen. What goes inside them is the argument.",
            },
            explain="The argument is the value you hand over: `\"Lucky\"`. During the call, the parameter `hero_name` holds it.",
        ),
        dict(
            type="parsons",
            id="store-then-pass-order",
            q=(
                "Put the lines in order (with their indents) so the program shows Mar'tu's greeting. Store it in a "
                "variable first, then pass it on."
            ),
            lines=[
                "def get_greeting():",
                '    return "Welcome to the cabin."',
                "def present_greeting():",
                "    greeting = get_greeting()",
                "    print(greeting)",
                "present_greeting()",
            ],
            distractors=["    print(get_greeting)"],
            expected_output="Welcome to the cabin.",
            explain=(
                "Call the helper, store what it hands back in `greeting`, then pass `greeting` on. With no `()`, "
                "`get_greeting` is the recipe itself, not its line."
            ),
            notes=(
                "Store-then-pass (6A-08). The board is print() here: parsons questions cannot have hidden setup. "
                "Distractor: the helper with no () (6A-08 WA)."
            ),
        ),
        dict(
            type="mc",
            id="return-the-right-box",
            q="What happens when this runs?",
            code=(
                "def mana_after(mana, cost):\n"
                "    left = mana - cost\n"
                "    return result\n"
                "\n"
                "print(mana_after(20, 6))\n"
            ),
            choices=["Python stops with an error", "14", "None"],
            answer=0,
            why_wrong={
                1: "The recipe works out 14 in `left`, but it hands back `result`, a box this recipe never made.",
                2: "`None` comes from a recipe with no `return` line. This one has a `return`, and it names a box that "
                   "doesn't exist, so Python stops.",
            },
            explain=(
                "`mana_after`'s box is `left`. `return result` stops Python: name 'result' is not defined. Write "
                "`return left`."
            ),
            notes=(
                "RNM, handing back the right box (6A-07; A-01's `return result`). 14 is the belief that `return` "
                "finds the answer by itself; None mixes this up with a missing `return`."
            ),
        ),
        dict(
            type="predict",
            id="catch-and-add",
            q="What will this print?",
            code="def double(n):\n    return n * 2\n\ny = double(4)\nprint(y + 1)\n",
            choices=["9", "8", "5", "an error"],
            answer="9",
            explain="`double(4)` hands back 8, and `y` catches it. Then `y + 1` is 9.",
        ),
    ],
)

ITEMS = [REMEMBERS_6A, LESSON_6A, QUIZ_6A]
