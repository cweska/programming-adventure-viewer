"""Unit 7 "Functions II" ("Spells You Can Hand Over"), part a: Mar'tu remembers (6b-remembers) and Lesson 6B
"Recipes That Read Stat Sheets".

Spec: design/curriculum.md, "## Unit 7 · Functions II", item 1 (u07a): 6b-remembers; 6B-01 to 6B-07, 6B-10 and 6B-S,
in that order. Introduces nothing new (concept_map.json: u07a introduces []). Functions come from Unit 3 (u03a/u03b),
lists from Unit 4, dictionaries from Unit 5 (u05a-u05c, in staging). Loops come from Unit 6, which is being written at
the same time and is not in this folder: only its planned concepts are used (u06a: `for` over a list or a list of
dicts), in the warm-up, Lucky's side quest on 6B-01 and the bottom loop of 6B-07. `None` is never written in code
(const:None is u07b's): it only shows up as printed output and in prose.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN `get_mana_bar(caster)`
and `show_mana(caster)` (mana-bars), `add_spell(...)` with `"mana_cost": mana_cost` and `spell_book[spell_name] =
spell` (spell-book), and the guard at the top of `cast_spell` (hold-the-barrier). So every campaign link here is
"you've seen this, now you'll get it". Every student has their own device; pair talk is optional and every checkpoint
is solo.

Terminology (2.9): "function" from here on; Mar'tu still says "recipe" in the Learn pane's first and last lines.
"parameter", "argument", "returns", "variable" (Mar'tu may say "box"), "key". "Matching" means an exact name (6B-03 on).
The quotes sentence stays word for word.

Help ladder as fields (FORMAT.md, the Unit 2 fix pass): hints[0] Where to look (point; "Read Python's last line first"
in a debug step), the middle hints Teach me (a tiny example with other names, listed in foreign_names), the last hint
Show me how: the step's own line in backticks, whose start up to its first `(` or `=` is Start me off (always a
solution line). Then another_way, assemble (More structure, on the make/write exercises) and the solution (Compare).

Check codes (curriculum 2.5), built from the _FX helpers below. `check()` puts in front of each check only the helpers
it uses (and the helpers those use), so the unit JSON stays small. Every check that calls a student function does it
with fresh sheets the task never uses (lint b) and with its prints kept private; nothing a check does shows in the
console, and the student's own sheets are never touched. _capture and _trace use sys.setprofile and always put the
previous hook back (no site code uses a profile or trace hook):
  _need()      the function exists (DEF for a variable made with `=`, NAME for a near miss) with the starter's
               parameters, letter for letter.
  _call()      calls it with stdout captured; _capture() also reads the function's own variables as it returns
               (sys.setprofile), so a spell still being built (6B-03 CP1) and a local box that vanishes (6B-02) are
               seen by behavior, not by reading the text.
  _stubbed()   calls it with a helper swapped for a recorder (CALL: `draw_bar` in 6B-07), only inside the check.
  _trace()     reruns the whole program in a fresh namespace and records every call to the named functions with
               its arguments and its caller (CALL at the top level: 6B-06).
  _keep()      KEEP: an "already finished" helper is unchanged (AST compare with the starter's own copy).
  _outer()     the class's biggest slip, typed test values, in its sheet form: a top-level sheet (`lucky`) read
               inside the function instead of its parameter (`hero`). Typed numbers and typed lines are found by
               two fresh calls giving the same answer (PAR-CONST) or by a constant in the function body.
  _why()       a kind message for an error raised inside a student function while Mar'tu's check called it: a quoted
               parameter used as a key, a near-miss key or parameter (PNM), a key with no quotes, `str()` glue, the
               NoneType glue of a missing `return`, `"▯" * a - b` (precedence), a function glued as text, text read
               like a sheet (wrong order), the wrong number of values, a dict used as a key.
  _gap()       the first difference between a returned line and the wanted line, told in the wanted line's words
               only (Unit 3's _gap), so a student's own text is never repeated back (2.11).
Messages: the fix first, then what happened, then the evidence in brackets, "(Mar'tu's check called `mana_line` with a
sheet for Pell, mana 7 of 12, only inside the check: it should return `Pell: 7/12`.)", as in Units 2-5. The solo's
messages are lean: the kind of slip and the line, never the fix. Invented values only (Pell, Moth, Bellows, Tinplate,
Moon Step, Ash Ward, Sun Ward); the party table's real values for the heroes (Lucky max mana 26, Oogrish 18).

The class's slips for this unit, each proven by a wrong_answers entry (in the exercise named):
  * a function that must return a value returns nothing (`print` inside, no `return`, a bare `return`): 6B-01, 6B-03
    CP2, 6B-10 CP1 (the NoneType TypeError);
  * thinking the caller won't see a change, so the change is returned or kept in a local variable: 6B-02, 6B-S;
    `book = {...}` inside the function: 6B-04;
  * keys that don't exactly match (`"cost"` for `"mana_cost"`, `"affinity"` for `"required_affinity"`): 6B-03;
  * a quoted parameter (`"mana_cost": "mana_cost"`, `book["spell_name"]`, `"spell_name" not in ...`): 6B-03, 6B-04,
    6B-05, 6B-10;
  * typed test values instead of the parameters (a typed line, cost, value, message or sheet): 6B-01, 6B-02, 6B-03,
    6B-04, 6B-05, 6B-07, 6B-10 CP4, 6B-S;
  * the guard after the work, a guard with no `return`, an if/else that falls through, `return` not indented: 6B-05;
  * a helper called with the wrong number or order of values, or edited: 6B-06, 6B-07;
  * a function handed over where its result was wanted (`draw_bar(robot, get_fuel_bar)`, `bar = get_fuel_bar`):
    6B-07 (the reverse slip, `strengthen_magic()`, and `book[name]["effect"]` with no `(hero)` are Lesson 6C, u07b);
  * reading from the wrong sheet: `lucky` for `hero` (6B-01, 6B-02, 6B-05), the hero's sheet for its spell book
    (`spell_name not in hero`, 6B-05).

Deviations from the spec, each small and noted on its exercise:
  * The spec's placeholder test name is never used (teacher ruling): PAR uses invented Tor names.
  * 6B-01's starter keeps `pass` under the signature (Unit 3's rule), so the first Run shows `None` twice.
  * 6B-02's `spend` and 6B-04's `add_to_book` give the `def` line with a numbered comment and `pass` (S2), so the
    bottom calls run on the first Run.
  * 6B-04 CP2 is a program step (a second call, any new name) plus the function-level "a second spell keeps the
    first" check, so it has a slip of its own to catch (the same name twice).
  * 6B-05's bottom calls crash on any guard that lets "Star Glow" through, so those slips fail at 0 with Python's
    KeyError (the explainer's row); the check's own KeyError messages are kept for a changed bottom.
  * 6B-06's two one-click questions have no widget yet: they are the pair-talk prompt and an another_way angle with
    the answers ("Two quick questions"), and the predict asks what a call to the helper shows.
  * 6B-07's numbered comments map one-to-one onto four checkpoints (first 0, second 0, store, pass): the campaign's
    four checks (3 of 5, empty and full, draws once, stored) are all there, regrouped by step.
  * 6B-S: the solo is seat B, `drink_glug(hero, sips)`, because seat A's `rest(hero)` is printed in 6B-02's starter;
    seat A is in its notes (meta).
  * Lucky's side quests never turn a main step red (checked: each bonus solution passes its exercise's checkpoints).
    6B-03's checks allow extra keys for that reason (`"strength"`); a near-miss key is still caught when a required
    key is missing.
  * 6B-05 also gets an Assemble it (it is a write step); 6B-06 (one call) and the debug and solo items do not.

Phone width: every fenced picture, Example, predict and quiz code keeps lines to 36 characters or fewer. Editor code
keeps sheets one key a line; the campaign's own long lines (a `def` with three parameters, the mana-bar `return`, a
comment that carries the code to type) run longer, as in Units 3-5.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u07a
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def fill(template, **values):
    """Check code from a template: each __NAME__ token becomes repr(value)."""
    out = template
    for key, value in values.items():
        out = out.replace("__" + key.upper() + "__", repr(value))
    return out


# ---------------------------------------------------------------------------------------------
# Check helpers, put in front of every check (plain Python, run in the student's namespace)
# ---------------------------------------------------------------------------------------------

_FX = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__
_KEYS = ('name', 'mana', 'max_mana', 'fuel', 'max_fuel', 'mana_cost', 'required_affinity', 'color', 'spell_book',
         'strength')


def _show(_v):
    _t = type(_v).__name__
    if _t == 'str':
        return '"' + _v + '"'
    if _t == 'function':
        return _v.__name__
    return str(_v)


def _ev(_what, _said=''):
    return " (Mar'tu's check " + _what + ', only inside the check' + ((': ' + _said) if _said else '') + '.)'


def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b, _loose=True):
    # NAME / KEY / PNM near miss: case, plural, 1-2 edits; loosely also a shared `_` word or a substring.
    if type(_a).__name__ != 'str' or type(_b).__name__ != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower().replace(' ', '_'), _b.lower().replace(' ', '_')
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    if min(len(_la), len(_lb)) >= 3 and _edits(_la, _lb) <= 2:
        return True
    if not _loose:
        return False
    _wa = set(_w for _w in _la.split('_') if len(_w) >= 4)
    _wb = set(_w for _w in _lb.split('_') if len(_w) >= 4)
    return bool(_wa & _wb) or (len(_la) >= 4 and (_la in _lb or _lb in _la))


def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    if not _q:
        return 'no parameters'
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


def _wrapped(_name):
    return sorted(set(_c.lineno for _c in _calls_in(_top(), 'print') if _calls_in([_c], _name)))


def _blank(_d):
    return any(type(_n).__name__ == 'Return' and _n.value is None for _n in _ast.walk(_d))


def _typed_if(_d):
    # An `if` that asks about one typed test value of a parameter (`if cost == 4:`), so only that call works.
    _ps = [_a.arg for _a in _d.args.args]
    _out = []
    for _n in _ast.walk(_d):
        if type(_n).__name__ != 'If':
            continue
        for _c in _ast.walk(_n.test):
            if type(_c).__name__ != 'Compare':
                continue
            _sides = [_c.left] + list(_c.comparators)
            if (any(type(_s).__name__ == 'Name' and _s.id in _ps for _s in _sides)
                    and any(type(_s).__name__ == 'Constant' for _s in _sides) and _n.lineno not in _out):
                _out.append(_n.lineno)
    return _out


def _only_pass(_d):
    return all(type(_n).__name__ == 'Pass' for _n in _d.body)


def _made(_d):
    # The variables a function makes with `=` (or `+=`, or a `for`), in order.
    _out = []
    for _n in _ast.walk(_d):
        _ts = []
        if type(_n).__name__ == 'Assign':
            _ts = _n.targets
        elif type(_n).__name__ in ('AugAssign', 'For'):
            _ts = [_n.target]
        for _t in _ts:
            if type(_t).__name__ == 'Name' and _t.id not in _out:
                _out.append(_t.id)
    return _out


def _outer(_name):
    # A sheet, book or list made at the top level and read inside the function instead of its parameter.
    _d = _defs().get(_name)
    if _d is None:
        return []
    _ps = [_a.arg for _a in _d.args.args]
    _tops = set(_made(_ast.Module(body=_top(), type_ignores=[])))
    _local = set(_made(_d))
    _out = []
    for _n in _ast.walk(_d):
        if (type(_n).__name__ == 'Name' and _n.id in _tops and _n.id not in _ps and _n.id not in _local
                and _n.id not in _out and type(_g.get(_n.id)).__name__ in ('dict', 'list')):
            _out.append(_n.id)
    return _out


def _find(_name, _kept=True):
    _v = _g.get(_name)
    if type(_v).__name__ == 'function':
        return _v, ''
    if _name in _g:
        return None, ('`' + _name + '` is a variable, made with `=`. A function is made with `def`: a line that starts '
                      '`def ' + _name + '(`, with its steps indented under it.')
    _near = sorted(_k for _k, _x in list(_g.items()) if type(_x).__name__ == 'function' and not _k.startswith('_')
                   and _close(_k, _name, False))
    if _near:
        return None, 'Python matches names letter for letter: you wrote `' + _near[0] + '`, the task needs `' + _name + '`.'
    if _kept:
        return None, 'Keep the function `' + _name + '` from the starter, with its `def` line.'
    return None, 'Make a function named `' + _name + '`: a line that starts `def ' + _name + '(`.'


def _sig_msg(_name, _want, _have, _kept=True):
    _line = '`def ' + _name + '(' + ', '.join(_want) + '):`'
    if len(_have) != len(_want):
        _n = 'one parameter' if len(_want) == 1 else str(len(_want)) + ' parameters'
        return ('`' + _name + '` takes ' + _n + ': ' + _names(_want) + '. ' + ('Keep' if _kept else 'Write')
                + ' its first line as ' + _line + '.')
    return (('Keep the parameter names from the starter: ' if _kept else 'Name the parameters as the task says: ')
            + _line + '. Python matches names letter for letter.')


def _need(_name, _want, _kept=True):
    _f, _m = _find(_name, _kept)
    assert _f, _m
    _ps = _params(_f)
    assert _ps == _want, _sig_msg(_name, _want, _ps, _kept)
    return _f


def _call(_f, _args):
    _buf = _io.StringIO()
    _keep_out = _sys.stdout
    _sys.stdout = _buf
    _val, _err = None, None
    try:
        _val = _f(*_args)
    except Exception as _e:
        _err = _e
    finally:
        _sys.stdout = _keep_out
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _err


def _capture(_f, _args):
    # Like _call, and also the function's own variables as it returns (read from its frame, not from the text).
    _box = {}
    _code = _f.__code__

    def _prof(_fr, _evt, _arg):
        if _evt == 'return' and _fr.f_code is _code:
            _box['l'] = dict(_fr.f_locals)

    _old = _sys.getprofile()
    _sys.setprofile(_prof)
    try:
        _val, _rows, _err = _call(_f, _args)
    finally:
        _sys.setprofile(_old)
    return _box.get('l', {}), _val, _rows, _err


def _stubbed(_f, _args, _name):
    # Call _f with the helper `_name` swapped for a recorder, only inside the check.
    _G = _f.__globals__
    _rec = []
    _real = _G.get(_name)

    def _fake(*_a, **_k):
        # Keyword values (`draw_bar(robot=robot, bar=bar)`) are put in the real helper's own order.
        _ps = _params(_real) if type(_real).__name__ == 'function' else []
        _rec.append(tuple(_a) + tuple(_k[_p] for _p in _ps[len(_a):] if _p in _k)
                    + tuple(_v for _n, _v in _k.items() if _n not in _ps[len(_a):]))

    _G[_name] = _fake
    try:
        _val, _rows, _err = _call(_f, _args)
    finally:
        if _real is None:
            _G.pop(_name, None)
        else:
            _G[_name] = _real
    return _val, _rows, _err, _rec


def _trace(_watch):
    # Run the whole program again in a fresh namespace, recording every call to the named functions.
    _ns = {'__name__': '__main__'}
    _seen = []

    def _prof(_fr, _evt, _arg):
        if _evt == 'call' and _fr.f_code.co_filename == '<again>' and _fr.f_code.co_name in _watch:
            _seen.append((_fr.f_code.co_name, dict(_fr.f_locals), _fr.f_back.f_code.co_name if _fr.f_back else ''))

    _buf = _io.StringIO()
    _keep_out = _sys.stdout
    _old = _sys.getprofile()
    _err = None
    _sys.stdout = _buf
    _sys.setprofile(_prof)
    try:
        exec(compile(_source, '<again>', 'exec'), _ns)
    except Exception as _e:
        _err = _e
    finally:
        _sys.setprofile(_old)
        _sys.stdout = _keep_out
    return _ns, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _seen, _err


def _keep(_name, _orig):
    # KEEP: '' when the function is exactly the starter's (comments aside), else 'gone' or 'changed'.
    _d = _defs().get(_name)
    if _d is None:
        return 'gone'
    _o = [_n for _n in _ast.parse(_orig).body if type(_n).__name__ == 'FunctionDef' and _n.name == _name][0]
    return '' if _ast.dump(_d) == _ast.dump(_o) else 'changed'


def _one(_c):
    return 'space' if _c == ' ' else '`' + _c + '`'


def _gap(_p, _w):
    # The first difference between a returned line `_p` and the wanted line `_w`, told with the wanted line's own
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


def _why(_name, _err, _e='', _foreign=()):
    # A kind message for an error raised inside the student's function while Mar'tu's check called it.
    _f = _g.get(_name)
    _ps = _params(_f) if type(_f).__name__ == 'function' else []
    _k = type(_err).__name__
    _s = str(_err)
    _stop = _ev(_e, 'Python stopped with a ' + _k) if _e else ''
    _ing = ('The parameters of `' + _name + '` are ' + _names(_ps) + '.') if _ps else ''
    if _k == 'KeyError':
        _x = _err.args[0] if _err.args else ''
        if type(_x).__name__ == 'str' and _x in _ps:
            return ('Take the quotes off `"' + _x + '"` to use the parameter `' + _x + '`. With quotes, Python looks '
                    'for a key spelled ' + _x + '. ' + _QUOTES + _stop)
        _near = [_y for _y in _KEYS if _close(_x, _y, False)]
        if _near:
            return ('Use the key `"' + _near[0] + '"`, letter for letter. The sheet has no key `' + _show(_x) + '`.'
                    + _stop)
        return 'Use a key the sheet really has. The dictionary has no key ' + _show(_x) + '.' + _stop
    if _k in ('NameError', 'UnboundLocalError'):
        _x = getattr(_err, 'name', None) or ''
        if not _x:
            _m = _re.search(r"'(\w+)'", _s)
            _x = _m.group(1) if _m else ''
        if _k == 'UnboundLocalError' or 'local variable' in _s:
            return ('Make `' + _x + '` first, then use it. Python runs a function from the top down, and `' + _x
                    + '` was used before the line that makes it.' + _stop)
        if _x in _KEYS and _x not in _ps:
            return 'Put quotes around the key: `["' + _x + '"]`. ' + _QUOTES + _stop
        _fo = [_y for _y in _foreign if _y == _x or (len(_x) >= 3 and _edits(_y, _x) <= 2)]
        if _fo:
            return ('`' + _x + '` ' + ('comes from' if _fo[0] == _x else 'looks like `' + _fo[0] + '` from')
                    + " Mar'tu's example. " + _ing + _stop)
        if [_p for _p in _ps if _close(_x, _p)]:
            return _ing + ' You wrote `' + _x + '`. Python matches names letter for letter.' + _stop
        return 'Inside `' + _name + '`, Python found a name it does not know: `' + _x + '`. ' + _ing + _stop
    if _k == 'TypeError':
        if 'concatenate' in _s and 'NoneType' in _s:
            return ('Make the function it calls `return` its value. A function with no `return` hands back `None`, '
                    "and text can't be glued to `None`." + _stop)
        if 'concatenate' in _s and 'function' in _s:
            return ('Hand over what the function returns, not the function itself: store `get_fuel_bar(robot)` in a '
                    'variable, with `()`, then pass the variable.' + _stop)
        if 'concatenate' in _s:
            return 'Glue a number to text with `str()`, like `str(hero["mana"])`.' + _stop
        if 'string indices' in _s:
            return ('Hand over a sheet where the `def` line has a sheet: the variable, no quotes. Python tried to read '
                    'a key from text.' + _stop)
        if 'unsupported operand' in _s and "'str' and 'int'" in _s:
            return ('Put brackets around the subtraction, so Python works it out first. Python does `*` before `-`, '
                    'so it made the blocks, then tried to take a number away from text.' + _stop)
        if "can't multiply sequence" in _s:
            return 'Multiply the block by a number from the sheet, like `robot["fuel"]`, not by the whole sheet.' + _stop
        if 'unhashable' in _s:
            return ("Put the name in the square brackets and the spell after `=`: `book[spell_name] = spell`. A whole "
                    "dictionary can't be a key." + _stop)
        if 'positional argument' in _s:
            return 'Count the values against the `def` line: a call hands over the wrong number of them.' + _stop
        if 'does not support item assignment' in _s:
            return 'Write into the dictionary that was handed in, not into text.' + _stop
        if 'not subscriptable' in _s:
            return 'Read a key from a sheet. That value is a number or a function, not a sheet.' + _stop
    if _k == 'AttributeError':
        return 'Read a dictionary with square brackets, like `hero["mana"]`, not a dot.' + _stop
    if _k == 'RecursionError':
        return ('Take the spaces off the call inside the function, so it sits at the bottom, outside it. The function '
                'calls itself, again and again.')
    return 'Mend this, then Run again: ' + _k + ': ' + _s + _stop
'''.replace("__QUOTES__", repr(QUOTES_RULE))


def _fx_parts():
    """_FX split into its setup lines (imports, _g, _tree, ...) and its helper functions, each with the helper names
    it uses, so a check can carry only the helpers it needs (the unit JSON stays small)."""
    import ast

    tree = ast.parse(_FX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_FX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_FX_HEAD, _FX_DEFS = _fx_parts()


def check(label, body, foreign=(), **values):
    """(label, code): the _FX setup lines, the helpers this check uses (and the helpers those use), the exercise's
    foreign names (LEFT/RNM), then the filled-in body."""
    import re

    code = f"_FOREIGN = {list(foreign)!r}\n" + fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _FX_DEFS and name not in need:
            need.add(name)
            todo |= _FX_DEFS[name][1]
    helpers = [text for name, (text, _) in _FX_DEFS.items() if name in need]
    return (label, "\n".join(_FX_HEAD) + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + code)


# =============================================================================================
# UNIT (repeated in every part file of spell-recipes; must match u07b and u07c exactly). Copied verbatim
# from u07b's UNIT (written at the same time), as u05a did with u05b, so the parts agree.
# =============================================================================================

UNIT = dict(
    id="spell-recipes",
    order=7,
    title="Functions II",
    subtitle="Spells You Can Hand Over",
    published=True,
    martu_intro=(
        "You know recipes. Now they read stat sheets, write spell books, and guard the door. And one more thing, "
        "the strange one: a recipe can sit in a box, like any value. You can hand it to someone without cooking "
        "it.\n"
        "You have seen all of this in the campaign: `get_mana_bar(caster)`, `add_spell(...)` with "
        "`strengthen_magic` and no `()`, and `cast_spell` holding the barrier. A lot of that code felt like a "
        "wall, yes? This unit takes the wall apart. By the end, it is your code."
    ),
    goals=[
        "Write a function that takes a hero's sheet and returns a value from it",
        "Change a dictionary passed in, know the caller sees the change, and know when a function needs `return`",
        "Build a dictionary from parameters with exact matching names, and store it by key",
        "Guard a function with an early `return`",
        "Read a helper you didn't write, call it correctly, and leave it unchanged",
        "Wire two functions together: build the bar, then pass it on",
        "Use a function as a value: store it, hand it over without `()`, and call it from a dictionary with "
        "`book[name][\"effect\"](hero)`",
    ],
    campaign_links=["friends-in-low-places"],
)

GLOSSARY = [
    dict(
        term="guard",
        aliases=["guards", "guard clause", "early return"],
        plain=(
            "An `if` at the top of a function that checks first. When something is wrong, it says so and stops the "
            "function with `return`. The lines below it run only when the guard lets the call through."
        ),
        example='if spell_name not in book:\n    print("Unknown spell.")\n    return',
    ),
    dict(
        term="helper",
        aliases=["helpers", "helper function", "finished helper"],
        plain=(
            "A finished function someone else wrote for you to call. Read its `def` line to see what to hand it, and "
            "in what order. Leave its steps as they are."
        ),
        example="draw_bar(lucky, bar)",
    ),
    dict(
        term="matching parameter",
        aliases=["matching parameters", "matching"],
        plain=(
            "The parameter with exactly the same name as the key, letter for letter. The key `\"mana_cost\"` gets "
            "the parameter `mana_cost`, with no quotes."
        ),
        example='"mana_cost": mana_cost,',
    ),
    dict(
        term="same sheet",
        aliases=["in place", "changes in place", "change in place"],
        plain=(
            "A function that is handed a dictionary gets that very dictionary, not a copy. A change it makes by key "
            "is a change the caller sees, with no `return` needed."
        ),
        example='def rest(hero):\n    hero["mana"] = hero["max_mana"]',
    ),
]

# The party table (curriculum 1.2): Lucky's max mana is 26 (affinity 13), Oogrish's 18 (affinity 9).

# =============================================================================================
# Mar'tu remembers... (6b-remembers): a Unit 5 nested write and a Unit 6 for-each over the roster
# =============================================================================================

REMEMBERS_6B = dict(
    kind="quiz",
    id="6b-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from earlier units. Nothing is scored.",
    notes=(
        "meta: path=CC; unscored warm-up shown inline before Lesson 6B; recall from Unit 5 (a nested dict write, "
        "4B) and Unit 6 (a for-each over a list of sheets, planned u06a). A miss shows the answer and a one-line "
        "why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="nested-write",
            q="What will this print?",
            code=(
                "lucky = {\n"
                '    "name": "Lucky",\n'
                '    "abilities": {"wisdom": 12},\n'
                "}\n"
                'lucky["abilities"]["wisdom"] = 14\n'
                'print(lucky["abilities"]["wisdom"])\n'
            ),
            choices=["14", "12", "{'wisdom': 14}", "an error"],
            answer="14",
            explain=(
                "Read the brackets left to right. `lucky[\"abilities\"]` is the inner sheet, and `[\"wisdom\"]` is one "
                "key in it. The write puts 14 there, in place of 12, so the read shows 14."
            ),
            notes="12: the write is missed; the inner dict: one bracket read; an error: two brackets feel wrong.",
        ),
        dict(
            type="predict",
            id="every-hero",
            q="What will this print?",
            code=(
                "roster = [\n"
                '    {"name": "Oogrish", "mana": 18},\n'
                '    {"name": "Lucky", "mana": 26},\n'
                "]\n"
                "for hero in roster:\n"
                '    print(hero["name"])\n'
            ),
            choices=["Oogrish\nLucky", "Oogrish", "Lucky", "hero\nhero"],
            answer="Oogrish\nLucky",
            explain=(
                "The loop runs its body once for each sheet in `roster`. The first time, `hero` is Oogrish's sheet; "
                "the second time, Lucky's. Today, `hero` is a parameter that works the same way."
            ),
            notes="One name: the loop runs once (the first or the last); hero/hero: quotes-thinking on a variable.",
        ),
    ],
)

# =============================================================================================
# Lesson 6B "Recipes That Read Stat Sheets"
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# 6B-01 hand-over-a-sheet (S1: the signature only, plus two calls with "should show" comments)
# ---------------------------------------------------------------------------------------------

LUCKY_20 = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 20,\n'
    '    "max_mana": 26,\n'
    "}\n"
)
OOGRISH_18 = (
    "oogrish = {\n"
    '    "name": "Oogrish",\n'
    '    "mana": 18,\n'
    '    "max_mana": 18,\n'
    "}\n"
)
ML_LINE = 'return hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])'


# The another_way angle that points at the clearest None/return twin (u07c's inside-stays-inside), after the
# return steps (6B-01, 6B-02, 6B-10). The same words everywhere it shows.
MORE_PRACTICE = dict(
    angle="more practice",
    label="More practice",
    text="Extra practice, *Inside stays inside*: a box made inside a function vanishes unless the function returns it.",
)


def _ml(body="    " + ML_LINE + "\n", tail=""):
    return ("def mana_line(hero):\n" + body + "\n\n" + LUCKY_20 + OOGRISH_18
            + "print(mana_line(lucky))\n# should show  Lucky: 20/26\n"
            + "print(mana_line(oogrish))\n# should show  Oogrish: 18/18\n" + tail)


ML_STARTER = _ml("    pass\n")
ML_SOLUTION = _ml()
ML_FOREIGN = ["wisdom_line", "sheet", "shell", "w"]

_ML_RET = r'''
_f = _need('mana_line', ['hero'])
_d = _defs()['mana_line']
_e = 'called `mana_line` with a sheet for Pell, mana 7 of 12'
_val, _rows, _err = _call(_f, [{'name': 'Pell', 'mana': 7, 'max_mana': 12}])
assert not _err, _why('mana_line', _err, _e, _FOREIGN)
if _val is None:
    _own = [_x for _x in _made(_d) if _x != 'hero']
    assert not _rows, ('Return the line with `return`. `print` only shows it, so the call gets `None`.'
                       + _ev(_e, 'it printed a line but returned `None`'))
    assert not _blank(_d), ('Put the line after `return`, on the same line. `return` on its own hands back nothing.'
                            + _ev(_e, 'it returned `None`'))
    assert not _own, ('End the function with `return ' + _own[-1] + '`. It builds `' + _own[-1] + '`, but never '
                      'returns it.' + _ev(_e, 'it returned `None`'))
    assert False, 'Replace `pass` with `return` and the glued text, like `Pell: 7/12`.' + _ev(_e, 'it returned `None`')
_t = type(_val).__name__
assert _t != 'dict', ('Return one line of text, glued from `hero["name"]`, `hero["mana"]` and `hero["max_mana"]`. '
                      'That returns the whole sheet.' + _ev(_e, 'it returned a sheet'))
assert _t != 'tuple', ('Glue the pieces with `+`. Commas between them make several values, not one line.'
                       + _ev(_e, 'it returned several values'))
assert _t == 'str', ('Return text: the name, `: `, the mana, `/` and the max mana, glued with `+`.'
                     + _ev(_e, 'it returned a number' if _t in ('int', 'float') else 'it returned something else'))
'''

_ML_PAR = r'''
_f = _need('mana_line', ['hero'])
_cases = [({'name': 'Pell', 'mana': 7, 'max_mana': 12}, 'Pell: 7/12', 'Pell, mana 7 of 12'),
          ({'name': 'Moth', 'mana': 30, 'max_mana': 31}, 'Moth: 30/31', 'Moth, mana 30 of 31')]
_got = []
for _s, _w, _who in _cases:
    _val, _rows, _err = _call(_f, [dict(_s)])
    assert not _err, _why('mana_line', _err, 'called `mana_line` with a sheet for ' + _who, _FOREIGN)
    _got.append(_val)
_out = _outer('mana_line')
for (_s, _w, _who), _val in zip(_cases, _got):
    if _val == _w:
        continue
    _e = 'called `mana_line` with a sheet for ' + _who
    _said = 'it should return `' + _w + '`'
    assert not _out, ('Read from `hero`, not `' + _out[0] + '`. `hero` is whichever sheet the call hands over.'
                      + _ev(_e, _said))
    assert not (type(_got[0]).__name__ == 'str' and _got[0] == _got[1]), (
        'Build the line from `hero`, not typed text, so it fits every sheet.'
        + _ev('called `mana_line` with sheets for Pell and Moth', 'both returned the same line'))
    _n, _m, _x = _s['name'], str(_s['mana']), str(_s['max_mana'])
    assert _val != _n + ': ' + _x + '/' + _m, ('Put the mana first, then the max mana: `hero["mana"]` before the '
                                               '`/`, `hero["max_mana"]` after it.' + _ev(_e, _said))
    assert _val not in (_n + ': ' + _m + '/' + _m, _n + ': ' + _x + '/' + _x), (
        'Read two keys: `"mana"` before the `/`, `"max_mana"` after it.' + _ev(_e, _said))
    if type(_val).__name__ == 'str' and _n in _val and _m in _val and _x in _val:
        assert False, _gap(_val.replace('’', "'"), _w)[0] + _ev(_e, _said)
    # One piece typed in (the class's biggest slip, a piece at a time): the same wrong piece for both sheets.
    _pt = [_re.match(r'^(.*): (.*)/(.*)$', _v) if type(_v).__name__ == 'str' else None for _v in _got]
    if _pt[0] and _pt[1]:
        _wp = [(_c[0]['name'], str(_c[0]['mana']), str(_c[0]['max_mana'])) for _c in _cases]
        for _i, (_lab, _key) in enumerate([('name', 'name'), ('mana', 'mana'), ('max mana', 'max_mana')]):
            _a, _b = _pt[0].group(_i + 1), _pt[1].group(_i + 1)
            assert not (_a == _b and _a != _wp[0][_i]), (
                'Read the ' + _lab + ' from `hero["' + _key + '"]`, not typed in, so the line fits every sheet.'
                + _ev('called `mana_line` with sheets for Pell and Moth', 'both lines had the same ' + _lab))
    assert False, ('Return the name, `: `, the mana, `/`, then the max mana, all read from `hero`.'
                   + _ev(_e, _said))
'''

_ML_ROSTER = r'''
_f = _need('mana_line', ['hero'])
_r = _g.get('roster')
assert type(_r).__name__ == 'list' and len(_r) >= 2, 'Make `roster`, a list of the sheets: `roster = [lucky, oogrish]`.'
_loops = [_n for _n in _tree.body if type(_n).__name__ == 'For' and type(_n.iter).__name__ == 'Name'
          and _n.iter.id == 'roster']
assert _loops, 'Use a `for` loop over `roster`, so every hero gets a line: `for hero in roster:`.'
_v = _loops[0].target.id if type(_loops[0].target).__name__ == 'Name' else ''
_inner = [_c for _c in _calls_in(_loops[0].body, 'mana_line') if _c.args and type(_c.args[0]).__name__ == 'Name'
          and _c.args[0].id == _v]
assert _inner, ('Inside the loop, print `mana_line(' + (_v or 'hero') + ')`, so each pass hands over the next sheet.')
_ls = _lines()
_miss = [_h for _h in _r if type(_h).__name__ == 'dict' and _call(_f, [_h])[0] not in _ls]
assert not _miss, 'Print `mana_line(...)` for every sheet in `roster`, inside the loop.'
'''

HAND_OVER_A_SHEET = dict(
    id="hand-over-a-sheet",
    title="Hand over a sheet",
    martu=(
        "You know recipes. Python calls them [[functions]], and from here on, so do we. Now hand one a whole stat "
        "sheet. The [[parameter]] `hero` (Unit 3's ingredient) holds whichever sheet the call hands over: Lucky's in "
        "one call, Oogrish's in the next.\n"
        "Inside, read the sheet by key, the same as always: `hero[\"mana\"]`. Then `return` the line, so the call "
        "gets it back.\n"
        "Right now the function only says `pass`. Run it first and look, yes?"
    ),
    example=(
        "def wisdom_line(sheet):\n"
        '    w = str(sheet["wisdom"])\n'
        '    return sheet["name"] + ": " + w\n'
        "\n"
        "\n"
        "shell = {\n"
        '    "name": "Bomb Shell",\n'
        '    "wisdom": 8,\n'
        "}\n"
        "print(wisdom_line(shell))\n"
    ),
    example_output="Bomb Shell: 8",
    names=["mana_line", "hero"],
    predict=dict(
        q="Before you press Run: the function only says `pass`. What will this show?",
        code='def mana_line(hero):\n    pass\n\n\nprint(mana_line({"name": "Lucky"}))\n',
        choices=["Lucky", "None", "nothing at all", "ERROR: NameError"],
        answer="None",
        explain=(
            "A function with no `return` hands back `None`, Python's word for nothing. `print` shows that `None`. "
            "Your `return` line gives the call something real."
        ),
    ),
    starter=ML_STARTER,
    checkpoints=[
        dict(
            id="return-the-line",
            text=(
                "Make `mana_line(hero)` return a line like `Lucky: 20/26`, read from `hero`: the name, the mana, then "
                "the max mana."
            ),
            dictated=False,
            hints=[
                "Everything comes from `hero`: `hero[\"name\"]`, `hero[\"mana\"]` and `hero[\"max_mana\"]`. Glue the "
                "pieces with `+`. Numbers need `str()`.",
                "The Example glues `sheet[\"name\"] + \": \" + w` and returns it. Your line has two more pieces: "
                "`\"/\"`, then the max mana.",
                "`return hero[\"name\"] + \": \" + str(...) + \"/\" + str(...)`: put a key read in each `...`. "
                "`return` hands the line back to `print(...)` at the bottom.",
                "Write `" + ML_LINE + "`.",
            ],
            checks=[
                check("mana_line returns a line", _ML_RET, ML_FOREIGN),
                check("the line follows the sheet", _ML_PAR, ML_FOREIGN),
            ],
            pass_line="Mar'tu: One function, any sheet. Lucky's, Oogrish's, a stranger's. That is the point, yes?",
        ),
    ],
    solution=ML_SOLUTION,
    assemble=dict(
        lines=[line for line in ML_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=[
            '    return "Lucky: 20/26"',
            '    print(hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"]))',
            '    return lucky["name"] + ": " + str(lucky["mana"]) + "/" + str(lucky["max_mana"])',
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One function, two sheets",
            text=(
                "```text\nmana_line(lucky)\n  hero = Lucky's sheet\n  -> \"Lucky: 20/26\"\n"
                "mana_line(oogrish)\n  hero = Oogrish's sheet\n  -> \"Oogrish: 18/18\"\n```\n"
                "Same steps. The call decides which sheet `hero` holds."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The call hands over a sheet. `hero` now holds it.\n"
                "2. `hero[\"name\"]` reads the name.\n"
                "3. `str(hero[\"mana\"])` and `str(hero[\"max_mana\"])` turn the numbers into text.\n"
                "4. `+` glues the pieces, with `\": \"` and `\"/\"` between them.\n"
                "5. `return` hands the line back to the call."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "In the mana bars, `get_mana_bar(caster)` took a caster's whole sheet, read `caster[\"mana\"]` and "
                "`caster[\"max_mana\"]`, and returned the bar as text. The game handed in each member's sheet. "
                "`mana_line(hero)` is the same shape."
            ),
        ),
        MORE_PRACTICE,
    ],
    tracer=True,
    bonus=dict(
        by="lucky",
        title="Everyone at once",
        text=(
            "What's in it for me? A whole roster. At the bottom, make `roster = [lucky, oogrish]`. Then use a `for` "
            "loop to print `mana_line(hero)` for every hero in it."
        ),
        hints=[
            "A `for` loop runs its body once for each sheet. Name the loop variable `hero`, then print "
            "`mana_line(hero)` inside the loop.",
            "`for robot in robots:` then, indented, `print(robot[\"name\"])` prints every robot's name.",
            "Write `for hero in roster:`, then `    print(mana_line(hero))` under it.",
        ],
        checks=[check("every hero in roster gets a line", _ML_ROSTER, ML_FOREIGN)],
        solution=ML_SOLUTION + "roster = [lucky, oogrish]\nfor hero in roster:\n    print(mana_line(hero))\n",
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="def get_mana_bar(caster):\n    ...\n    return \"Mana [\" + ...",
        why=(
            "You have seen this. `get_mana_bar(caster)` took a whole sheet as one parameter, read it by key, and "
            "returned text. The game called it for every party member. `mana_line` works the same way."
        ),
    ),
    takeaway="A function can take a whole sheet: `def mana_line(hero):`, read it by key, and `return` what it builds.",
    wrong_answers=[
        dict(why="starter: pass, so the call gets None", code=ML_STARTER, fails_at=1,
             message_contains="Replace `pass` with `return` and the glued text"),
        dict(why="a typed line for Lucky (spec WA; PAR with an invented sheet, Pell)",
             code=_ml('    return "Lucky: 20/26"\n'), fails_at=1, message_contains="Pell"),
        dict(why="one piece typed: Lucky's max mana, 26 (the typed-value slip, a piece at a time)",
             code=_ml('    return hero["name"] + ": " + str(hero["mana"]) + "/26"\n'), fails_at=1,
             message_contains='from `hero["max_mana"]`'),
        dict(why="one piece typed: Lucky's name", code=_ml(
            '    return "Lucky: " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'), fails_at=1,
             message_contains='from `hero["name"]`'),
        dict(why="one piece typed: Lucky's mana, 20", code=_ml('    return hero["name"] + ": 20/" + str(hero["max_mana"])\n'),
             fails_at=1, message_contains='from `hero["mana"]`'),
        dict(why="print instead of return (spec WA: None)",
             code=_ml('    print(hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"]))\n'),
             fails_at=1, message_contains="None"),
        dict(why="reads the caller's sheet lucky instead of the parameter hero (the wrong sheet)",
             code=_ml('    return lucky["name"] + ": " + str(lucky["mana"]) + "/" + str(lucky["max_mana"])\n'),
             fails_at=1, message_contains="not `lucky`"),
        dict(why="the line built in a box but never returned",
             code=_ml('    line = hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'),
             fails_at=1, message_contains="never returns it"),
        dict(why="a bare return under the line", code=_ml(
            '    line = hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n    return\n'),
             fails_at=1, message_contains="on its own"),
        dict(why="returns the whole sheet", code=_ml("    return hero\n"), fails_at=1, message_contains="whole sheet"),
        dict(why="commas instead of + (a tuple)",
             code=_ml('    return hero["name"], hero["mana"], hero["max_mana"]\n'), fails_at=1,
             message_contains="Glue the pieces"),
        dict(why="the mana and the max mana swapped",
             code=_ml('    return hero["name"] + ": " + str(hero["max_mana"]) + "/" + str(hero["mana"])\n'),
             fails_at=1, message_contains="mana first"),
        dict(why="the space after the colon missing",
             code=_ml('    return hero["name"] + ":" + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'),
             fails_at=1, message_contains="space is missing"),
        dict(why="no str() around a number (crashes at the bottom call)",
             code=_ml('    return hero["name"] + ": " + hero["mana"] + "/" + str(hero["max_mana"])\n'),
             fails_at=0, message_contains="can only concatenate"),
        dict(why="a key with no quotes", code=_ml(
            '    return hero[name] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'),
             fails_at=0, message_contains="name 'name' is not defined"),
        dict(why="the parameter in quotes", code=_ml(
            '    return "hero"["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'),
             fails_at=0, message_contains="string indices"),
        dict(why="a near-miss key", code=_ml(
            '    return hero["Name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'),
             fails_at=0, message_contains="KeyError: 'Name'"),
    ],
    notes=(
        meta(starter_level="S1", path="CC", skills="func-takes-dict", solo="false", dictates="",
             foreign_names="wisdom_line,sheet,shell,w,robot,robots",
             par='({"name":"Pell","mana":7,"max_mana":12},),({"name":"Moth","mana":30,"max_mana":31},)') + "\n"
        "M, S1 (the signature plus `pass`, Unit 3's rule, and two calls with 'should show' comments). CP1 [ND]: RET "
        "first (print-instead-of-return, a bare return, a built box never returned, the whole sheet, a tuple), then "
        "PAR with two invented sheets (the spec's placeholder sheet replaced by invented Tor names, teacher ruling), so a typed "
        "line for Lucky (spec WA) fails PAR-CONST ('both returned the same line'), and a read of `lucky` inside "
        "the function (the wrong sheet) is named. A near-miss line gets the first difference in the wanted line's "
        "words (Unit 3's _gap); one piece typed (Lucky's name, 20 or 26) is named by the piece the two fresh lines "
        "share. Slips that crash at the bottom calls (no str(), `hero[name]`, `\"hero\"[...]`, a "
        "near-miss key) fail at 0 with Python's message, the explainer's row. AW: picture, step-by-step, from the "
        "campaign (get_mana_bar, described). BQ (combining function + loop, Unit 6): a for-each over `roster`."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-02 recipes-change-sheets (P -> I -> M; the card "When does a function need `return`?")
# ---------------------------------------------------------------------------------------------

REST_DEF = 'def rest(hero):\n    hero["mana"] = hero["max_mana"]\n'
SPEND_LINE = 'hero["mana"] = hero["mana"] - cost'
LUCKY_9 = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 9,\n'
    '    "max_mana": 26,\n'
    "}\n"
)
SPEND_BOTTOM = "rest(lucky)\nprint(lucky[\"mana\"])\nspend(lucky, 4)\nprint(lucky[\"mana\"])\n"


def _spend(body="    " + SPEND_LINE + "\n", bottom=SPEND_BOTTOM):
    return (REST_DEF + "\n\ndef spend(hero, cost):\n" + body + "\n\n" + LUCKY_9 + bottom)


SPEND_STARTER = _spend("    # 1. Take cost away from hero[\"mana\"].\n    #    No return is needed.\n    pass\n")
SPEND_SOLUTION = _spend()
SPEND_FOREIGN = ["wake", "robot", "bomb", "awake"]

_SPEND = r"""
_f = _need('spend', ['hero', 'cost'])
_d = _defs()['spend']
_cases = [({'name': 'Pell', 'mana': 11, 'max_mana': 16}, 3, 8, 'Pell, mana 11 of 16, and a cost of 3'),
          ({'name': 'Moth', 'mana': 30, 'max_mana': 31}, 7, 23, 'Moth, mana 30 of 31, and a cost of 7')]
_out = _outer('spend')
_typed = [_c.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'int']
for _s0, _cost, _want, _who in _cases:
    _s = dict(_s0)
    _locs, _val, _rows, _err = _capture(_f, [_s, _cost])
    _e = 'called `spend` with a sheet for ' + _who
    assert not _err, _why('spend', _err, _e, _FOREIGN)
    _m = _s.get('mana')
    if _m == _want:
        continue
    _start = _s0['mana']
    _said = 'the sheet should hold ' + str(_want) + ' after'
    _held = 'the sheet still held ' + str(_start)
    _ti = _typed_if(_d)
    assert not _ti, ('Take `cost` away on every call, with no `if`. The `if` on line ' + str(_ti[0]) + ' asks about '
                     'one typed value, so other costs are not spent.' + _ev(_e, _said))
    _near = [_k for _k in _s if _k not in _s0 and _close(_k, 'mana', False)]
    assert not _near, ('Write into the key `"mana"`, letter for letter. `spend` made a new key, `' + _show(_near[0])
                       + '`.' + _ev(_e, _said))
    if _m == _start:
        assert not _out, ('Change `hero`, the sheet that was handed in, not `' + _out[0] + '`. `hero` is whichever '
                          'sheet the call hands over.' + _ev(_e, _held))
        assert _locs.get('hero', _s) is _s, ('Write into the sheet that was handed in: `hero["mana"] = hero["mana"] '
                                             '- cost`. `hero = ...` makes a new sheet inside the function, and the '
                                             "caller's sheet never changes." + _ev(_e, _held))
        assert _val != _want, ('Change the sheet itself: `hero["mana"] = hero["mana"] - cost`. No `return` is needed. '
                               '`spend` returns the new mana, but nothing keeps it.' + _ev(_e, _held))
        _box = [_k for _k, _v in _locs.items() if _k not in ('hero', 'cost') and _v == _want]
        assert not _box, ('Store the new mana in the sheet: `hero["mana"] = ...`. Your variable `' + _box[0] + '` '
                          'holds it, but it vanishes when the function ends.' + _ev(_e, _held))
        assert not _rows, ('Write the new mana into the sheet: `hero["mana"] = hero["mana"] - cost`. `spend` only '
                           'shows it.' + _ev(_e, _held))
        _bare = [_n.lineno for _n in _d.body if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
        assert not _bare, ('Put `hero["mana"] = ` in front of line ' + str(_bare[0]) + '. It works out the new mana '
                           'but keeps it nowhere.' + _ev(_e, _held))
        assert not _only_pass(_d), ('Replace `pass` with a line that takes `cost` away from `hero["mana"]`.'
                                    + _ev(_e, _held))
        assert False, ('Write the new mana into the key `"mana"` itself: `hero["mana"] = hero["mana"] - cost`. Right '
                       'now `spend` leaves it as it was.' + _ev(_e, _held))
    _ty = [_t for _t in _typed if _t != _cost and _m == _start - _t]
    assert not _ty, ('Use the parameter `cost`, so every cost works. `spend` takes away a typed ' + str(_ty[0])
                     + '.' + _ev(_e, _said))
    _plain = [_c.value.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Assign'
              and type(_c.value).__name__ == 'Constant']
    assert _m not in _plain, ('Work the new mana out from `hero["mana"]` and `cost`, so every call works. `spend` '
                              'stores a typed number.' + _ev(_e, _said))
    assert not _out, ('Read from `hero`, not `' + _out[0] + '`.' + _ev(_e, _said))
    assert _m != _s0['max_mana'] - _cost, ('Spend from `hero["mana"]`, what the hero has now. That takes the cost '
                                           'away from the max mana.' + _ev(_e, _said))
    assert _m != _cost - _start, ('Start from the old mana: `hero["mana"] - cost`. That takes the mana away from '
                                  'the cost, the wrong way round.' + _ev(_e, _said))
    assert _m != _start + _cost, 'Use `-`: spending takes the cost away. That adds it.' + _ev(_e, _said)
    assert _m != _cost, ('Start the right side from the old mana: `hero["mana"] - cost`. That stores just the cost.'
                         + _ev(_e, _said))
    assert not _typed, ('Work the new mana out from `hero["mana"]` and `cost` only, not a typed ' + str(_typed[0])
                        + ', so every call works.' + _ev(_e, _said + ', not ' + str(_m)))
    assert False, ('Take `cost` away from `hero["mana"]`, once.' + _ev(_e, _said + ', not ' + str(_m)))
"""

_SPEND_OWN = r"""
_l = _g.get('lucky')
assert type(_l).__name__ == 'dict', 'Keep the sheet `lucky` from the starter.'
assert _calls_in(_top(), 'rest') and _calls_in(_top(), 'spend'), (
    'Keep the bottom lines as they are: `rest(lucky)`, then `spend(lucky, 4)`.')
assert _l.get('mana') == _l.get('max_mana', 0) - 4, (
    'Keep the bottom lines as they are: Lucky rests to full, then `spend(lucky, 4)` takes 4 away, so his last line '
    'should show ' + str(_l.get('max_mana', 0) - 4) + '.')
"""

RECIPES_CHANGE_SHEETS = dict(
    id="recipes-change-sheets",
    title="Recipes change sheets",
    martu=(
        "Hand a function a sheet, and it gets [[same sheet|that very sheet]], not a copy. So a change it makes is "
        "a change the "
        "caller sees.\n"
        "Read `rest(hero)` in the starter. It writes into `hero[\"mana\"]` and returns nothing. Yet after "
        "`rest(lucky)`, Lucky's own sheet is full. Run it and see.\n"
        "When does a function need `return`? When the caller needs a value back, like `mana_line`. A function that "
        "only changes a sheet, like `rest`, doesn't. Remember this card, yes?"
    ),
    example=(
        "def wake(robot):\n"
        '    robot["awake"] = True\n'
        "\n"
        "\n"
        'bomb = {"awake": False}\n'
        "wake(bomb)\n"
        'print(bomb["awake"])\n'
    ),
    example_output="True",
    names=["spend", "hero", "cost"],
    predict=dict(
        q="Before you press Run: `rest` returns nothing. What does the last line show?",
        code=(
            "def rest(hero):\n"
            '    hero["mana"] = hero["max_mana"]\n'
            "\n"
            "\n"
            'lucky = {"mana": 9, "max_mana": 26}\n'
            "rest(lucky)\n"
            'print(lucky["mana"])\n'
        ),
        choices=["9", "26", "None", "ERROR: NameError"],
        answer="26",
        explain=(
            "`hero` and `lucky` are two names for one sheet. `rest` wrote 26 into it, so `lucky[\"mana\"]` is 26 now. "
            "No `return` was needed, because nothing had to come back."
        ),
    ),
    starter=SPEND_STARTER,
    pair_talk=(
        "Tell your partner why `lucky` changed, when `rest` only ever wrote into `hero`. Then each of you finishes "
        "`spend` on your own screen."
    ),
    checkpoints=[
        dict(
            id="spend-the-cost",
            text="Finish `spend(hero, cost)` so it takes `cost` away from `hero[\"mana\"]`. No `return` is needed.",
            dictated=False,
            hints=[
                "Copy the shape of `rest`: one line that writes into `hero[\"mana\"]`. The right side reads the old "
                "mana and takes `cost` away.",
                "The Example writes into `robot[\"awake\"]`, and the caller's `bomb` changes. "
                "`robot[\"fuel\"] = robot[\"fuel\"] - 2` would take 2 fuel away the same way.",
                "A new variable inside the function, like `mana = ...`, vanishes when the function ends. Write into "
                "the sheet itself, by key.",
                "Write `" + SPEND_LINE + "` in place of `pass`.",
            ],
            checks=[
                check("spend changes the sheet it is handed", _SPEND, SPEND_FOREIGN),
                check("Lucky's own sheet changes", _SPEND_OWN, SPEND_FOREIGN),
            ],
            pass_line="Gearshift: 26, then 22. Math checks out. Same sheet the whole time.",
        ),
    ],
    solution=SPEND_SOLUTION,
    assemble=dict(
        lines=[line for line in SPEND_SOLUTION.splitlines() if line.strip()],
        distractors=["    mana = hero[\"mana\"] - cost", "    return hero[\"mana\"] - cost",
                     "    hero[\"mana\"] = hero[\"mana\"] - 4"],
    ),
    another_way=[
        dict(
            angle="why",
            label="Why does this work? Same sheet, two labels",
            text=(
                "```text\nlucky --+\n        +--> {\"mana\": 9 ...}\nhero  --+\n```\n"
                "During the call, `lucky` and `hero` point at one sheet. `hero[\"mana\"] = 26` changes that sheet, "
                "so `lucky[\"mana\"]` shows 26 after. Nothing was copied, so nothing has to be returned."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Like handing someone your notebook, not a photo of it. Whatever they write in it is there when you "
                "get it back."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `spend(lucky, 4)`: `hero` is Lucky's sheet, `cost` is 4.\n"
                "2. The right side reads `hero[\"mana\"]`, 26, and takes 4 away: 22.\n"
                "3. The left side writes 22 into `hero[\"mana\"]`, which is Lucky's sheet.\n"
                "4. The function ends. `lucky[\"mana\"]` is 22."
            ),
        ),
        dict(
            angle="shorter",
            text="Need a value back? `return` it. Changing the sheet? Write into it by key. No `return` needed.",
        ),
        MORE_PRACTICE,
    ],
    tracer=True,
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='caster["mana"] = caster["mana"] - spell["mana_cost"]',
        why=(
            "This line sat inside `cast_spell`. It wrote into the caster's own sheet, so the party panel showed the "
            "new mana, with no `return`. Now you know why that worked."
        ),
    ),
    takeaway=(
        "A function gets the caller's own sheet: `hero[\"mana\"] = hero[\"mana\"] - cost` changes it for the caller. "
        "Use `return` only when the caller needs a value back."
    ),
    wrong_answers=[
        dict(why="starter: pass", code=SPEND_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why="returns the new mana instead of changing the sheet (the caller won't see it)",
             code=_spend("    return hero[\"mana\"] - cost\n"), fails_at=1, message_contains="nothing keeps it"),
        dict(why="a local variable holds the new mana (vanishes)", code=_spend("    mana = hero[\"mana\"] - cost\n"),
             fails_at=1, message_contains="vanishes"),
        dict(why="worked out, kept nowhere (BARE)", code=_spend("    hero[\"mana\"] - cost\n"), fails_at=1,
             message_contains="keeps it nowhere"),
        dict(why="printed, not stored", code=_spend("    print(hero[\"mana\"] - cost)\n"), fails_at=1,
             message_contains="only shows it"),
        dict(why="a new sheet made inside the function (hero = {...})",
             code=_spend("    hero = {\"mana\": hero[\"mana\"] - cost}\n"), fails_at=1, message_contains="new sheet"),
        dict(why="the caller's sheet lucky changed instead of hero (the wrong sheet)",
             code=_spend("    lucky[\"mana\"] = lucky[\"mana\"] - cost\n"), fails_at=1, message_contains="not `lucky`"),
        dict(why="a typed 4, the bottom call's cost (PAR)", code=_spend("    hero[\"mana\"] = hero[\"mana\"] - 4\n"),
             fails_at=1, message_contains="typed 4"),
        dict(why="the answer typed: 22", code=_spend("    hero[\"mana\"] = 22\n"), fails_at=1,
             message_contains="typed number"),
        dict(why="an if that only spends for the bottom call's typed cost (if cost == 4)",
             code=_spend("    if cost == 4:\n        hero[\"mana\"] = hero[\"mana\"] - 4\n"), fails_at=1,
             message_contains="one typed value"),
        dict(why="22 worked out from the max mana and a typed 4 (looks right for Lucky only)",
             code=_spend("    hero[\"mana\"] = hero[\"max_mana\"] - 4\n"), fails_at=1, message_contains="not a typed 4"),
        dict(why="a near-miss key written", code=_spend("    hero[\"Mana\"] = hero[\"mana\"] - cost\n"), fails_at=1,
             message_contains='"Mana"'),
        dict(why="spends from the max mana", code=_spend("    hero[\"mana\"] = hero[\"max_mana\"] - cost\n"),
             fails_at=1, message_contains="max mana"),
        dict(why="the wrong way round", code=_spend("    hero[\"mana\"] = cost - hero[\"mana\"]\n"), fails_at=1,
             message_contains="wrong way round"),
        dict(why="adds the cost", code=_spend("    hero[\"mana\"] = hero[\"mana\"] + cost\n"), fails_at=1,
             message_contains="adds it"),
        dict(why="the bottom spend call deleted", code=_spend(bottom="rest(lucky)\nprint(lucky[\"mana\"])\n"),
             fails_at=1, message_contains="Keep the bottom lines"),
        dict(why="the cost in quotes on the bottom call", code=_spend(bottom=SPEND_BOTTOM.replace("4)", '"4")')),
             fails_at=0, message_contains="unsupported operand"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="func-takes-dict", solo="false", dictates="",
             foreign_names="wake,robot,bomb,awake,mana",
             par='({"name":"Pell","mana":11,"max_mana":16},3),({"name":"Moth","mana":30,"max_mana":31},7)') + "\n"
        "P -> I -> M. Predict/Investigate: after `rest(lucky)` the caller's `lucky` is full (26). CP1 [ND]: PAR with "
        "two invented sheets; the check reads the very dict it handed over, so 'the caller's dict changes' is "
        "tested by behavior. The function's own variables are read as it returns (_capture), so a local box "
        "('vanishes'), `hero = {...}` ('a new sheet') and a returned value ('nothing keeps it') each get their own "
        "message: the class's 'the caller won't see the change' belief, in both directions. Typed cost (PAR), typed "
        "answer, the wrong sheet (`lucky`), a near-miss key, the max mana, the sign. A second check keeps the "
        "bottom lines, so the student sees the change in their own run. The card (G3 R25) is the Learn pane's "
        "last paragraph and the 'shorter' angle; paid off by 6B-07 and 6B-10. WT 'Same sheet, two labels' is the "
        "why angle. TR: tracer. `-=` passes too. Pell's max mana is 16, not 15, so `hero[\"max_mana\"] - 4` (a "
        "typed 4) no longer lands on Pell's starting 11 by chance; an `if cost == 4:` guard is named as a typed "
        "value; 'Replace `pass`' is said only while `pass` is still the body."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-03 many-ingredients (S4, campaign phrasing: "Replace each placeholder with the matching parameter")
# ---------------------------------------------------------------------------------------------

MK_DEF = "def make_spell(mana_cost, required_affinity, color):\n"
MK_KEYS = ('"mana_cost"', '"required_affinity"', '"color"')
MK_BOTTOM = 'glow = make_spell(3, 8, "silver")\nprint(glow)\n'


def _mk(values=("mana_cost", "required_affinity", "color"), keys=MK_KEYS, ret="    return spell\n", extra="",
        bottom=MK_BOTTOM):
    return (MK_DEF + "    # 1. Replace each placeholder with the\n    #    matching parameter.\n"
            + "    spell = {\n" + "".join(f"        {k}: {v},\n" for k, v in zip(keys, values)) + extra + "    }\n"
            + "    # 2. Return the spell.\n" + ret + "\n\n" + bottom)


MK_STARTER = _mk(values=("0", "0", '""'), ret="")
MK_SOLUTION = _mk()
MK_FOREIGN = ["make_robot", "robot", "fuel", "cost"]

_MK_CASES = r"""
_want_keys = ['mana_cost', 'required_affinity', 'color']
_cases = [((5, 2, 'teal'), 'make_spell(5, 2, "teal")'), ((9, 7, 'gold'), 'make_spell(9, 7, "gold")')]


def _say(_v):
    # "Typed" only when the value really is typed in the function. A value is named only when it is a number or the
    # task's own text; a student's own text never is.
    _d = _defs().get('make_spell')
    _typed = _d is not None and any(type(_c).__name__ == 'Constant' and _c.value == _v
                                    and type(_c.value) == type(_v) for _c in _ast.walk(_d))
    if type(_v).__name__ in ('int', 'float') or _v in ('', 'silver'):
        return ('a typed ' if _typed else '') + _show(_v)
    if type(_v).__name__ == 'str':
        return 'typed text' if _typed else 'other text'
    return 'something else'
"""

_MK_KEYS_CHECK = _MK_CASES + r"""
_f = _need('make_spell', _want_keys)
for _args, _ct in _cases:
    _locs, _val, _rows, _err = _capture(_f, list(_args))
    _e = 'called `' + _ct + '`'
    assert not _err, _why('make_spell', _err, _e, _FOREIGN)
    _sp = _locs.get('spell')
    if type(_sp).__name__ != 'dict' and type(_val).__name__ == 'dict':
        _sp = _val
    assert type(_sp).__name__ == 'dict', ('Keep the dictionary `spell` from the starter, with its three keys, inside '
                                          'the function.' + _ev(_e, 'no dictionary called `spell` was made'))
    _want = dict(zip(_want_keys, _args))
    _odd = [_k for _k in _sp if type(_k).__name__ != 'str']
    assert not _odd, ('Keep the quotes on the keys: `"mana_cost": mana_cost`. A key with no quotes is looked up as a '
                      'variable, so the value handed in became the key.' + _ev(_e, 'the spell has a key '
                                                                              + _show(_odd[0])))
    _extra = [_k for _k in _sp if _k not in _want]
    _miss = [_k for _k in _want_keys if _k not in _sp]
    for _k in _extra:
        # A near name, or another name holding exactly the missing key's value (`"magic": required_affinity`).
        _n = [_w for _w in _miss if _close(_k, _w) or (_sp[_k] == _want[_w] and type(_sp[_k]) == type(_want[_w]))]
        assert not _n, ('Use the matching name, letter for letter: the key is `"' + _n[0] + '"`. The spell has a key `'
                        + _show(_k) + '` instead, and code that reads the spell asks for `"' + _n[0] + '"`.' + _ev(_e))
    assert not _miss, ('Keep all three keys from the starter: `"mana_cost"`, `"required_affinity"` and `"color"`. '
                       'The key `"' + _miss[0] + '"` is missing.' + _ev(_e))
    for _k in _want_keys:
        _v, _w = _sp[_k], _want[_k]
        if _v == _w and type(_v) == type(_w):
            continue
        _said = '`"' + _k + '"` should hold ' + _show(_w)
        assert not (type(_v).__name__ == 'str' and _v in _want_keys), (
            'Use the parameter without quotes: `"' + _k + '": ' + _k + '`. Right now `"' + _k + '"` holds the text '
            + _show(_v) + '. ' + _QUOTES + _ev(_e))
        _o = [_x for _x in _want_keys if _x != _k and _want[_x] == _v and type(_want[_x]) == type(_v)]
        assert not _o, ('Give each key the parameter with its own name: `"' + _k + '": ' + _k + '`. You swapped '
                        'them: `"' + _k + '"` holds ' + _show(_v) + ', the value handed in as `' + _o[0] + '`.'
                        + _ev(_e))
        assert not (_v == 0 or _v == ''), ('Replace the placeholder with the matching parameter: `"' + _k + '": '
                                          + _k + '`. `"' + _k + '"` still holds ' + _show(_v) + '.' + _ev(_e, _said))
        assert False, ('Use the matching parameter, `"' + _k + '": ' + _k + '`, so every call works. `"' + _k
                       + '"` holds ' + _say(_v) + '.' + _ev(_e, _said))
"""

_MK_RET = _MK_CASES + r"""
_f = _need('make_spell', _want_keys)
_d = _defs()['make_spell']
for _args, _ct in _cases:
    _val, _rows, _err = _call(_f, list(_args))
    _e = 'called `' + _ct + '`'
    assert not _err, _why('make_spell', _err, _e, _FOREIGN)
    if _val is None:
        assert not _rows, ('Return the spell: `return spell`. `print` only shows it, so the call gets `None`.'
                           + _ev(_e, 'it printed the spell but returned `None`'))
        assert not _blank(_d), ('Write the variable after `return`: `return spell`. `return` on its own hands back '
                                'nothing.' + _ev(_e, 'it returned `None`'))
        assert False, ('Under comment 2, write `return spell`, indented inside the function.'
                       + _ev(_e, 'it returned `None`'))
    assert _val != 'spell', ('Take the quotes off: `return spell`. With quotes, the function returns the text `spell`, '
                             'not the dictionary. ' + _QUOTES + _ev(_e))
    assert type(_val).__name__ == 'dict', ('Return the dictionary itself: `return spell`.'
                                           + _ev(_e, 'it returned something else'))
    # Extra keys are fine (Lucky's side quest adds "strength"): the three keys must hold what was handed in.
    assert all(_val.get(_k) == _a for _k, _a in zip(_want_keys, _args)), (
        'Return `spell`, the dictionary the function builds.' + _ev(_e, 'it returned another dictionary'))
"""

_MK_STRENGTH = _MK_CASES + r"""
_f = _need('make_spell', _want_keys)
for (_args, _ct), _st in zip(_cases, (10, 18)):
    _val, _rows, _err = _call(_f, list(_args))
    _e = 'called `' + _ct + '`'
    assert not _err, _why('make_spell', _err, _e, _FOREIGN)
    assert type(_val).__name__ == 'dict', 'Return the spell first: `return spell`.'
    assert 'strength' in _val, 'Add a fourth key, `"strength"`, to the spell, worked out from `mana_cost`.'
    assert _val['strength'] == _st, ('Work `"strength"` out from the parameter: `mana_cost * 2`.'
                                     + _ev(_e, 'it should be ' + str(_st)))
"""

MANY_INGREDIENTS = dict(
    id="many-ingredients",
    title="Many ingredients",
    martu=(
        "A function can take many parameters and build a dictionary from them. The campaign said it like this: "
        "*replace each placeholder with the matching parameter*.\n"
        "[[matching parameter|Matching]] means exactly the same name. The key `\"mana_cost\"` gets the parameter "
        "`mana_cost`, letter "
        "for letter. The key keeps its quotes. The parameter has none, so Python looks inside it.\n"
        "Then `return` the spell, so the caller can keep it."
    ),
    example=(
        "def make_robot(name, fuel):\n"
        "    robot = {\n"
        '        "name": name,\n'
        '        "fuel": fuel,\n'
        "    }\n"
        "    return robot\n"
        "\n"
        "\n"
        'print(make_robot("Bellows", 4))\n'
    ),
    example_output="{'name': 'Bellows', 'fuel': 4}",
    names=["make_spell", "mana_cost", "required_affinity", "color", "spell"],
    predict=dict(
        q="Before you press Run: what will this show?",
        code='cost = 5\nspell = {"mana_cost": "cost"}\nprint(spell["mana_cost"])\n',
        choices=["5", "cost", "mana_cost", "ERROR: KeyError"],
        answer="cost",
        explain=(
            QUOTES_RULE + " `\"cost\"` has quotes, so the spell keeps the four letters c-o-s-t, not the 5. "
            "`\"mana_cost\": cost` would keep the 5."
        ),
    ),
    starter=MK_STARTER,
    pair_talk=(
        "Point at `\"mana_cost\"` and at `mana_cost` in your code. Tell your partner which one is a key and which "
        "one holds the value handed in."
    ),
    checkpoints=[
        dict(
            id="matching-parameters",
            text="Replace each placeholder with the matching parameter. Each key gets the one with its own name.",
            dictated=True,
            hints=[
                "Each key has a parameter with the very same name on the `def` line. That parameter, with no quotes, "
                "goes after the colon, in place of the `0` or the `\"\"`.",
                "The Example writes `\"fuel\": fuel`. The key keeps its quotes; the value has none, so Python looks "
                "inside the parameter.",
                QUOTES_RULE + " `\"mana_cost\": \"mana_cost\"` stores those letters, not the cost.",
                "Write `\"mana_cost\": mana_cost,` in place of `\"mana_cost\": 0,`. Then do the same for the other two "
                "keys.",
            ],
            checks=[check("each key holds its matching parameter", _MK_KEYS_CHECK, MK_FOREIGN)],
            pass_line="Bomb Shell: Three keys. Three matches. Works.",
        ),
        dict(
            id="return-the-spell",
            text="Under comment 2, return `spell`.",
            dictated=True,
            hints=[
                "The spell is built, but the function keeps it. Until it returns something, `glow` at the bottom gets "
                "`None`.",
                "The Example's last line is `return robot`: no quotes, indented inside the function.",
                "`return \"spell\"` returns the text `spell`. `print(spell)` only shows the spell.",
                "Under comment 2, write `return spell`, indented like the lines above it.",
            ],
            checks=[check("make_spell returns the spell", _MK_RET, MK_FOREIGN)],
            pass_line=("Mar'tu: Three, eight, silver on your screen, and my check tried other values too. Whatever is "
                       "handed in, the spell keeps it."),
        ),
    ],
    solution=MK_SOLUTION,
    partials=[_mk(ret="")],
    assemble=dict(
        lines=[line for line in MK_SOLUTION.splitlines() if line.strip() and not line.strip().startswith("#")],
        distractors=['        "mana_cost": "mana_cost",', '        "affinity": required_affinity,', "    print(spell)"],
    ),
    another_way=[
        dict(
            angle="try it",
            label="Same word, two jobs",
            text=(
                "1. Rename the parameter `mana_cost` to `cost`, on the `def` line and after the colon. Run: it "
                "still works.\n"
                "2. Now rename the key `\"mana_cost\"` to `\"cost\"`. Run: the spell changes shape.\n"
                "`\"mana_cost\"` with quotes is a key. `mana_cost` without quotes holds the value handed in. Put "
                "both back when you are done."
            ),
        ),
        dict(
            angle="picture",
            label="Where each value goes",
            text=(
                "```text\nmake_spell(5, 2, \"teal\")\n  mana_cost         = 5\n  required_affinity = 2\n"
                "  color             = \"teal\"\nspell:\n  \"mana_cost\": 5\n  \"required_affinity\": 2\n"
                "  \"color\": \"teal\"\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The call hands over three values, in order.\n"
                "2. They land in the parameters, in the same order as the `def` line.\n"
                "3. Each key gets the parameter with its own name.\n"
                "4. `return spell` hands the finished spell back to the call."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "In the spell book you replaced `\"mana_cost\": 0` with `\"mana_cost\": mana_cost`, the matching "
                "parameter. The game later read exactly `spell[\"mana_cost\"]`, so a near name like `\"cost\"` "
                "would have broken it."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Stronger spells",
        text=(
            "What's in it for me? Stronger spells. Add a fourth key to the spell, `\"strength\"`, that holds "
            "`mana_cost * 2`."
        ),
        hints=[
            "A fourth line inside the curly brackets: the key in quotes, a colon, then the value worked out from "
            "`mana_cost`.",
            "`\"fuel\": fuel * 3` would keep three times the fuel handed in.",
            "Add `\"strength\": mana_cost * 2,` under the `\"color\"` line.",
        ],
        checks=[check("the spell's strength is twice its cost", _MK_STRENGTH, MK_FOREIGN)],
        solution=_mk(extra='        "strength": mana_cost * 2,\n'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet='spell = {\n    "mana_cost": mana_cost,\n    ...\n}',
        why=(
            "You have seen this. Step 1 of the spell book was this very move: replace each placeholder with the "
            "matching parameter. Now you know why the key keeps its quotes and the parameter has none."
        ),
    ),
    takeaway=(
        "Build a dictionary from parameters with matching names: `\"mana_cost\": mana_cost`. The key keeps its "
        "quotes; the parameter has none. Then `return` it."
    ),
    wrong_answers=[
        dict(why="starter: placeholders left, no return", code=MK_STARTER, fails_at=1, message_contains="placeholder"),
        dict(why="a 0 left in place (spec WA: PAR)", code=_mk(values=("0", "required_affinity", "color")), fails_at=1,
             message_contains="still holds 0"),
        dict(why="the parameter in quotes (A-02's quoted-name habit; spec WA: text)",
             code=_mk(values=('"mana_cost"', "required_affinity", "color")), fails_at=1, message_contains="text"),
        dict(why="two parameters swapped (spec WA: swapped)",
             code=_mk(values=("required_affinity", "mana_cost", "color")), fails_at=1, message_contains="swapped"),
        dict(why="the task call's values typed in (A-08: literals for parameters)",
             code=_mk(values=("3", "8", '"silver"')), fails_at=1, message_contains="holds a typed 3"),
        dict(why="a student's own colour typed in", code=_mk(values=("mana_cost", "required_affinity", '"pink"')),
             fails_at=1, message_contains="holds typed text"),
        dict(why="an approximate key name: cost for mana_cost",
             code=_mk(keys=('"cost"', '"required_affinity"', '"color"')), fails_at=1, message_contains='"mana_cost"'),
        dict(why="an approximate key name: affinity for required_affinity",
             code=_mk(keys=('"mana_cost"', '"affinity"', '"color"')), fails_at=1, message_contains="matching name"),
        dict(why='a made-up key name: "magic" for "required_affinity" (the campaign reads the exact name)',
             code=_mk(keys=('"mana_cost"', '"magic"', '"color"')), fails_at=1,
             message_contains='the key is `"required_affinity"`'),
        dict(why="the parameter changed on the way in (mana_cost + 1): not typed, so not called typed",
             code=_mk(values=("mana_cost + 1", "required_affinity", "color")), fails_at=1,
             message_contains='`"mana_cost"` holds 6.'),
        dict(why="a key with a capital: Color", code=_mk(keys=('"mana_cost"', '"required_affinity"', '"Color"')),
             fails_at=1, message_contains='"color"'),
        dict(why="keys with no quotes (the value becomes the key)",
             code=_mk(keys=("mana_cost", "required_affinity", "color")), fails_at=1, message_contains="quotes on the keys"),
        dict(why="print instead of return", code=_mk(ret="    print(spell)\n"), fails_at=2, message_contains="None"),
        dict(why="return with the variable name in quotes", code=_mk(ret='    return "spell"\n'), fails_at=2,
             message_contains="Take the quotes off"),
        dict(why="a bare return", code=_mk(ret="    return\n"), fails_at=2, message_contains="on its own"),
        dict(why="return placed before the dict is built (crashes at the bottom call)",
             code=MK_DEF + "    return spell\n    spell = {\n        \"mana_cost\": mana_cost,\n"
                           "        \"required_affinity\": required_affinity,\n        \"color\": color,\n    }\n\n\n"
                  + MK_BOTTOM, fails_at=0, message_contains="cannot access local variable"),
        dict(why="return not indented (outside the function)", code=_mk(ret="return spell\n"), fails_at=0,
             message_contains="outside function"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="dict-from-params", solo="false", dictates="1,2",
             foreign_names="make_robot,robot,fuel,cost", par='(5,2,"teal"),(9,7,"gold")') + "\n"
        "M, S4, the campaign's phrasing (spell-book step 1). The task's own call is make_spell(3, 8, \"silver\"), so "
        "the spec's fresh sets (5, 2, \"teal\") and (9, 7, \"gold\") never collide with it (lint b). CP1 [D] reads "
        "the spell as the function builds it (its own variable `spell`, by behavior, before CP2's return exists): "
        "PAR, SWAP, the quoted parameter ('text'), a placeholder left, typed values (a student's own text is never "
        "repeated: 'some typed text'), and the exact-name slips: an approximate key (`\"cost\"`, `\"affinity\"`, "
        "`\"Color\"`) is named with the matching key, so is a made-up name holding the missing key's value "
        "(`\"magic\": required_affinity`), and keys with no quotes. 'Typed' is said only for a constant really in "
        "the function (`mana_cost + 1` is told as the value it holds). CP2 [D] RET: print, `\"spell\"`, a "
        "bare return; a return before the build or outside the function crash at 0. Investigate 'same word, two "
        "jobs' (C2 / G4 R6) is the 'try it' angle plus the pair-talk prompt. PA: the solution lines; distractors "
        "are the quoted parameter, an approximate key and `print(spell)`. BQ: `\"strength\": mana_cost * 2`."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-04 store-by-name (S2)
# ---------------------------------------------------------------------------------------------

STORE_LINE = "book[spell_name] = spell"
GLOW_SPELL = 'glow = {\n    "mana_cost": 2,\n    "color": "silver",\n}\n'
WARM_SPELL = 'warm_hands = {\n    "mana_cost": 3,\n    "color": "silver",\n}\n'
SECOND_CALL = 'add_to_book(lucky_book, "Warm Hands", warm_hands)'


def _store(body="    " + STORE_LINE + "\n", second=WARM_SPELL + SECOND_CALL + "\n", head="lucky_book = {}\n"):
    return ("def add_to_book(book, spell_name, spell):\n" + body + "\n\n" + head + GLOW_SPELL
            + 'add_to_book(lucky_book, "Glow", glow)\n'
            + "# 2. Add a second spell to lucky_book\n#    with add_to_book.\n#    Make the spell first, like glow.\n"
            + second + "print(lucky_book)\n")


STORE_STARTER = _store("    # 1. Store spell in book, using\n    #    spell_name as the key.\n    pass\n", second="\n")
STORE_SOLUTION = _store()
STORE_FOREIGN = ["add_tool", "kit", "tool_name", "tool"]

_STORE_KEY = r"""
_f = _need('add_to_book', ['book', 'spell_name', 'spell'])
_b = {}
_sp = {'mana_cost': 4, 'color': 'teal'}
_locs, _val, _rows, _err = _capture(_f, [_b, 'Moon Step', _sp])
_e = 'called `add_to_book` with an empty book, the name "Moon Step" and a spell'
assert not _err, _why('add_to_book', _err, _e, _FOREIGN)
_out = _outer('add_to_book')
if not ('Moon Step' in _b and _b['Moon Step'] == _sp):
    _said = 'the book should hold the spell under "Moon Step"'
    assert 'spell_name' not in _b, ('Take the quotes off: `book[spell_name] = spell`. `book["spell_name"]` uses those '
                                    'exact letters as the key, for every spell. ' + _QUOTES
                                    + _ev(_e, 'the book got a key "spell_name"'))
    if not _b:
        _empty = 'the book stayed empty'
        assert not _out, ('Store into `book`, the book that was handed in, not `' + _out[0] + '`.' + _ev(_e, _empty))
        assert _locs.get('book', _b) is _b, (
            "Store into the book you were handed: `book[spell_name] = spell`. `book = {...}` makes a new book inside "
            "the function, so the book outside didn't change." + _ev(_e, _empty))
        assert type(_val).__name__ != 'dict', (
            "Store into the book you were handed: `book[spell_name] = spell`. `add_to_book` returns a new book, but "
            "nothing keeps it, so the caller's book stays empty." + _ev(_e, _empty))
        assert False, 'Replace `pass` with `book[spell_name] = spell`.' + _ev(_e, _empty)
    _tk = [_k for _k in _b if any(type(_c).__name__ == 'Constant' and _c.value == _k
                                  for _c in _ast.walk(_defs()['add_to_book']))]
    assert 'Moon Step' in _b, ('Use the parameter `spell_name` as the key, as it is, so each spell goes under the name '
                               'handed in.' + _ev(_e, 'the spell went under a typed name' if _tk
                                                  else 'the spell went under another name'))
    _v = _b['Moon Step']
    assert _v != 'spell', ('Take the quotes off: `= spell`. With quotes, the book keeps the text `spell`. ' + _QUOTES
                           + _ev(_e))
    assert not _out, ('Store `spell`, the spell that was handed in, not `' + _out[0] + '`.'
                      + _ev(_e, 'the book got another spell'))
    assert False, 'Store `spell` itself under the name: `book[spell_name] = spell`.' + _ev(_e, 'the book got something else')
"""

_STORE_KEEPS = r"""
_f = _need('add_to_book', ['book', 'spell_name', 'spell'])
_b = {'Glow': {'mana_cost': 2}}
_val, _rows, _err = _call(_f, [_b, 'Moon Step', {'mana_cost': 4}])
_e = 'called `add_to_book` with a book that already held Glow, and the name "Moon Step"'
assert not _err, _why('add_to_book', _err, _e, _FOREIGN)
assert 'Glow' in _b and 'Moon Step' in _b, ('Store the new spell next to the old ones: `book[spell_name] = spell` adds '
                                            'one key and keeps the rest.' + _ev(_e, 'Glow should stay'))
"""

_STORE_SECOND = r"""
_lb = _g.get('lucky_book')
assert type(_lb).__name__ == 'dict', 'Keep `lucky_book` from the starter: a dictionary.'
_made_again = [_x.lineno for _x in _tree.body if type(_x).__name__ == 'Assign'
               and any(getattr(_t, 'id', '') == 'lucky_book' for _t in _x.targets)]
assert 'Glow' in _lb, ('Make `lucky_book` once, at the top, and add each spell with `add_to_book`. Glow is gone from '
                       '`lucky_book`' + (', because line ' + str(_made_again[-1]) + ' makes a new book.'
                                         if len(_made_again) > 1 else '.'))
# By behavior: run the program again and record every call to add_to_book from the bottom, with its book and name.
_ns, _ls, _seen, _err = _trace(['add_to_book'])
_mine = [_c[1] for _c in _seen if _c[2] == '<module>']
_into = [_c for _c in _mine if _c.get('book') is _ns.get('lucky_book')]
_names = []
for _c in _into:
    if _c.get('spell_name') not in _names:
        _names.append(_c.get('spell_name'))
if len(_names) < 2:
    assert len(_lb) < 2, 'Add the second spell with `add_to_book` too, so the function does the storing.'
    assert len(_mine) >= 2, ('Under comment 2, add a second spell with another call: `add_to_book(lucky_book, "...", '
                             '...)`, with a new name and a spell.')
    assert len(_into) >= 2, ('Hand `lucky_book` to the second call too, first: `add_to_book(lucky_book, "...", ...)`. '
                             'One of your calls stores into another book.')
    assert False, ('Give the second spell its own name. Both calls used the same name, so the second spell replaced '
                   'the first: one key holds one value.')
# The screen agrees: the book `print(lucky_book)` shows is the finished book (a second call typed below the print,
# where Start me off lands before a click, would turn green while the screen still shows Glow alone).
_pb = [_c for _c in _calls_in(_top(), 'print') if _c.args and getattr(_c.args[0], 'id', '') == 'lucky_book']
assert _pb and str(_lb) in _lines(), ('Keep `print(lucky_book)` as the last line, under your second call, so the '
                                     'book it shows has both spells.')
"""

STORE_BY_NAME = dict(
    id="store-by-name",
    title="Store by name",
    martu=(
        "A spell book is a dictionary of spells. The key is the spell's name. The value is the spell.\n"
        "`book[spell_name] = spell` stores one. No quotes on `spell_name`: the key is whatever name was handed in.\n"
        "The book a function is handed is the caller's own book, the same sheet idea as before. Store into it, and "
        "the caller sees the new spell. Make a new book with `book = {...}`, and the caller's book never changes."
    ),
    example=(
        "def add_tool(kit, tool_name, tool):\n"
        "    kit[tool_name] = tool\n"
        "\n"
        "\n"
        "kit = {}\n"
        'add_tool(kit, "wrench", 3)\n'
        "print(kit)\n"
    ),
    example_output="{'wrench': 3}",
    names=["add_to_book", "book", "spell_name", "spell", "lucky_book"],
    pick='"Warm Hands"',
    predict=dict(
        q="Before you press Run: `wipe` makes a new book. What does the last line show?",
        code=(
            "def wipe(book):\n"
            "    book = {}\n"
            "\n"
            "\n"
            'spells = {"Glow": 2}\n'
            "wipe(spells)\n"
            "print(spells)\n"
        ),
        choices=["{}", "{'Glow': 2}", "None", "ERROR: NameError"],
        answer="{'Glow': 2}",
        explain=(
            "`book = {}` makes a new, empty book and puts the label `book` on it, inside the function only. The "
            "caller's `spells` was never touched, so it still holds Glow."
        ),
    ),
    starter=STORE_STARTER,
    checkpoints=[
        dict(
            id="store-the-spell",
            text="Finish `add_to_book(book, spell_name, spell)` so it stores `spell` in `book`, with `spell_name` as the key.",
            dictated=False,
            hints=[
                "One line: the book, the key in square brackets, `=`, then the spell. The key is the parameter "
                "`spell_name`, with no quotes.",
                "The Example's `kit[tool_name] = tool` stores 3 under the key `\"wrench\"`, the name that was "
                "handed in.",
                "`book[\"spell_name\"]` uses those exact letters as the key. `book = {...}` makes a new book that the "
                "caller never sees.",
                "Write `" + STORE_LINE + "` in place of `pass`.",
            ],
            checks=[check("add_to_book stores the spell by its name", _STORE_KEY, STORE_FOREIGN)],
            pass_line="Mar'tu: My check handed in Moon Step, and it went under Moon Step. The name in, the key out.",
        ),
        dict(
            id="a-second-spell",
            text=(
                "Under comment 2, add a second spell to `lucky_book` with another call to `add_to_book`. Glow should "
                "stay in the book."
            ),
            dictated=False,
            hints=[
                "Make a second spell, a small dictionary like `glow`, then call `add_to_book` again with a new name, "
                "any name you like, in quotes.",
                "Each name is its own key. Two names make two keys. The same name twice makes one key, and the "
                "second spell replaces the first.",
                "Make the spell first: `warm_hands = {\"mana_cost\": 3, \"color\": \"silver\"}`, like `glow`. Then `"
                + SECOND_CALL + "`.",
            ],
            checks=[
                # The function-level check first: a function that empties the book is named there, not as a remade
                # `lucky_book`.
                check("a second spell keeps the first", _STORE_KEEPS, STORE_FOREIGN),
                check("lucky_book keeps Glow and gains a second spell", _STORE_SECOND, STORE_FOREIGN),
            ],
            pass_line="Lucky: Two spells. Mine. Both of them.",
        ),
    ],
    solution=STORE_SOLUTION,
    partials=[_store(second="\n")],
    assemble=dict(
        lines=[line for line in STORE_SOLUTION.splitlines() if line.strip() and not line.startswith("#")],
        distractors=['    book["spell_name"] = spell', "    book = {spell_name: spell}", '    book[spell_name] = "spell"'],
    ),
    another_way=[
        dict(
            angle="why",
            label="Why does this work? Why `book = {...}` doesn't reach the caller",
            text=(
                "```text\nlucky_book --+\n             +--> {}\nbook       --+\n\nbook = {...}\n"
                "lucky_book ----> {}\nbook       ----> {new}\n```\n"
                "`book[spell_name] = spell` writes into the book both labels point at. `book = {...}` moves the "
                "label `book` to a new book. The caller's label never moved, so its book stays as it was."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "A library shelf with name cards. `book[spell_name] = spell` slides a new spell in behind its own name "
                "card. `book = {...}` builds a whole new shelf in another room, and nobody at the old shelf sees it."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `add_to_book(lucky_book, \"Glow\", glow)`: `book` is Lucky's book, `spell_name` is `\"Glow\"`, "
                "`spell` is the glow spell.\n"
                "2. `book[spell_name] = spell` makes the key `\"Glow\"` and puts the spell under it.\n"
                "3. The function ends. `lucky_book` now holds Glow."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="spell-book",
        snippet="spell_book[spell_name] = spell",
        why=(
            "You have seen this. The last line of `add_spell` stored the spell in each member's own spell book, under "
            "its name. No `return`: the book was the member's own, so the game saw the new spell."
        ),
    ),
    takeaway=(
        "Store by name with `book[spell_name] = spell`: no quotes on the key, and store into the book you were "
        "handed, never a new `book = {...}`."
    ),
    wrong_answers=[
        dict(why="starter: pass", code=STORE_STARTER, fails_at=1, message_contains="Replace `pass`"),
        dict(why='the key in quotes: book["spell_name"] (spec catch)', code=_store('    book["spell_name"] = spell\n'),
             fails_at=1, message_contains='"spell_name"'),
        dict(why="a new book inside the function: book = {spell_name: spell} (spec catch)",
             code=_store("    book = {spell_name: spell}\n"), fails_at=1, message_contains="didn't change"),
        dict(why="returns a new book instead of storing into the caller's",
             code=_store("    return {spell_name: spell}\n"), fails_at=1, message_contains="nothing keeps it"),
        dict(why="stores into the caller's lucky_book, not book (the wrong sheet)",
             code=_store("    lucky_book[spell_name] = spell\n"), fails_at=1, message_contains="not `lucky_book`"),
        dict(why='a typed name: book["Glow"]', code=_store('    book["Glow"] = spell\n'), fails_at=1,
             message_contains="typed name"),
        dict(why="stores the caller's glow, not the parameter spell", code=_store("    book[spell_name] = glow\n"),
             fails_at=1, message_contains="not `glow`"),
        dict(why="the spell in quotes", code=_store('    book[spell_name] = "spell"\n'), fails_at=1,
             message_contains="Take the quotes off"),
        dict(why="the spell used as the key (crashes at the first call)", code=_store("    book[spell] = spell_name\n"),
             fails_at=0, message_contains="unhashable"),
        dict(why="CP2 not done", code=_store(second="\n"), fails_at=2, message_contains="another call"),
        dict(why="the second call written with no warm_hands made first (crashes at the call)",
             code=_store(second=SECOND_CALL + "\n"), fails_at=0, message_contains="name 'warm_hands' is not defined"),
        dict(why="the second call reuses the name Glow (one key holds one value)",
             code=_store(second=WARM_SPELL + 'add_to_book(lucky_book, "Glow", warm_hands)\n'), fails_at=2,
             message_contains="its own name"),
        dict(why="lucky_book made again before the second call (Glow is gone)",
             code=_store(second=WARM_SPELL + "lucky_book = {}\n" + SECOND_CALL + "\n"), fails_at=2,
             message_contains="Glow is gone"),
        dict(why="the second spell written straight into the book, not through add_to_book",
             code=_store(second=WARM_SPELL + 'lucky_book["Warm Hands"] = warm_hands\n'), fails_at=2,
             message_contains="Add the second spell with `add_to_book`"),
        dict(why="a direct write, plus a second add_to_book call for Glow to make up the count (gaming the step)",
             code=_store(second=WARM_SPELL + 'add_to_book(lucky_book, "Glow", glow)\n'
                         'lucky_book["Warm Hands"] = warm_hands\n'), fails_at=2,
             message_contains="Add the second spell with `add_to_book`"),
        dict(why="the second call stores into another book, not lucky_book",
             code=_store(second=WARM_SPELL + 'other_book = {}\nadd_to_book(other_book, "Warm Hands", warm_hands)\n'),
             fails_at=2, message_contains="stores into another book"),
        dict(why="the second spell made and stored below print(lucky_book) (where Start me off lands before a "
                 "click): the screen still shows Glow alone",
             code=_store(second="\n").replace("print(lucky_book)\n", "print(lucky_book)\n" + WARM_SPELL + SECOND_CALL
                                                                      + "\n"),
             fails_at=2, message_contains="so the book it shows has both spells"),
        dict(why="the function empties the book before storing (book.clear()): CMB, a second spell keeps the first",
             code=_store("    book.clear()\n    book[spell_name] = spell\n"), fails_at=2,
             message_contains="keeps the rest"),
        dict(why="the name changed on the way in (spell_name.lower()): not typed, so not called typed",
             code=_store("    book[spell_name.lower()] = spell\n"), fails_at=1, message_contains="another name"),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="store-by-name", solo="false", dictates="",
             foreign_names="add_tool,kit,tool_name,tool,wipe,spells",
             par='({},"Moon Step",{"mana_cost":4,"color":"teal"}),({"Glow":{...}},"Moon Step",{...})') + "\n"
        "M, S2 (the `def` line, a numbered comment and `pass`). CP1 [ND] KEY by behavior: the check hands over its own "
        "empty book and reads it after, so `book[\"spell_name\"]`, `book = {spell_name: spell}` ('the book outside "
        "didn't change', spec) and a returned book are told apart; the function's own variables are read as it "
        "returns. The wrong sheet (`lucky_book`, `glow`), a typed name and a quoted spell are named. CP2 [ND]: a "
        "program step, a second call with any new name (pick: Warm Hands), plus the function-level CMB 'a second "
        "spell keeps the first' (spec). Its own slips: the same name twice (keys are unique), a remade "
        "`lucky_book`, a direct write (also with an extra Glow call to make up the count), a call into another book: "
        "CP2 reruns the program and counts the bottom calls that store into the program's own `lucky_book` "
        "under two names (_trace), then checks that the screen agrees: `print(lucky_book)` shows the finished book "
        "(a second spell below the print, where Start me off lands before a click, fails). The last hint's first code "
        "span is `warm_hands = ...` (Start me off `warm_hands =`); a call with no `warm_hands` made crashes at 0. CMB "
        "runs first, so a function that empties the book is named there. WT 'Why `book = {...}` doesn't reach the "
        "caller' is the why angle and the predict."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-05 guard-at-the-door (P -> I -> M; skill gate pattern:EarlyReturn)
# ---------------------------------------------------------------------------------------------

GUARD_LINES = (
    '    if spell_name not in hero["spell_book"]:\n'
    "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"
    "        return\n"
)
GUARD_COMMENT = (
    "    # 1. Guard: if spell_name is not in\n"
    '    #    hero["spell_book"], show a line\n'
    "    #    and return.\n"
)
CAST_WORK = (
    '    spell = hero["spell_book"][spell_name]\n'
    '    hero["mana"] = hero["mana"] - spell["mana_cost"]\n'
    '    print(hero["name"] + " casts " + spell_name + ".")\n'
)
LUCKY_BOOK = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 26,\n'
    '    "spell_book": {\n'
    '        "Glow": {"mana_cost": 2},\n'
    "    },\n"
    "}\n"
)
CAST_BOTTOM = 'cast_glow(lucky, "Glow")\ncast_glow(lucky, "Star Glow")\nprint(lucky["mana"])\n'


def _guard(guard=GUARD_LINES, work=CAST_WORK, bottom=CAST_BOTTOM):
    return "def cast_glow(hero, spell_name):\n" + GUARD_COMMENT + guard + work + "\n\n" + LUCKY_BOOK + bottom


GUARD_STARTER = _guard(guard="")
GUARD_SOLUTION = _guard()
GUARD_FOREIGN = ["open_door", "name", "guests"]

_GUARD_CASES = r"""
def _pell(_mana=11):
    return {'name': 'Pell', 'mana': _mana, 'spell_book': {'Moon Step': {'mana_cost': 3}}}


def _moth():
    return {'name': 'Moth', 'mana': 20, 'spell_book': {'Glow': {'mana_cost': 2}}}


_cases = [(_pell, 'Ash Ward', 'Pell'), (_moth, 'Sun Ward', 'Moth')]
_f = _need('cast_glow', ['hero', 'spell_name'])
_d = _defs()['cast_glow']
_ifs = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'If']
_reads = [_n.lineno for _n in _ast.walk(_d) if type(_n).__name__ == 'Subscript'
          and type(_n.slice).__name__ == 'Name' and _n.slice.id == 'spell_name']
"""

_GUARD_STOPS = _GUARD_CASES + r"""
for _make, _bad, _who in _cases:
    _s = _make()
    _val, _rows, _err = _call(_f, [_s, _bad])
    _e = 'called `cast_glow` for ' + _who + ' with "' + _bad + '", a spell ' + _who + ' does not know'
    _ke = 'Python stopped with a KeyError'
    if type(_err).__name__ == 'KeyError' and _err.args and _err.args[0] == _bad:
        _late = _ifs and _reads and min(_i.lineno for _i in _ifs) > min(_reads)
        assert not _late, ('Move the guard to the top of `cast_glow`, above the line that reads the spell. Python '
                           'reached that line first.' + _ev(_e, _ke))
        _shown = any(_who in _r and _bad in _r for _r in _rows)
        assert not _shown, ('Put `return` under the line, indented inside the `if`, so the function stops there. The '
                            'guard showed its line, then carried on to the spell.' + _ev(_e, _ke))
        _typed = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Constant'
                  and type(_c.value).__name__ == 'str' and _c.value not in ('spell_book', 'name')]
        assert not _typed, ('Ask the spell book, `if spell_name not in hero["spell_book"]:`, so every unknown spell is '
                            'stopped. Your guard looks for one typed spell name.' + _ev(_e, _ke))
        assert not _ifs, ('Ask `not in`: `if spell_name not in hero["spell_book"]:`. Your `if` let the unknown spell '
                          'through.' + _ev(_e, _ke))
        assert False, ('Add the guard at the top of `cast_glow`: `if spell_name not in hero["spell_book"]:`, then the '
                       'line, then `return`.' + _ev(_e, _ke))
    assert not _err, _why('cast_glow', _err, _e, _FOREIGN)
    assert _s['mana'] == _make()['mana'] and not any(' casts ' in _r for _r in _rows), (
        'Stop before the spell: `return` right after the line, inside the `if`.' + _ev(_e, 'the spell was cast'))
"""

_GUARD_LINE = _GUARD_CASES + r"""
for _make, _bad, _who in _cases:
    _s = _make()
    _val, _rows, _err = _call(_f, [_s, _bad])
    _e = 'called `cast_glow` for ' + _who + ' with "' + _bad + '", a spell ' + _who + ' does not know'
    assert not _err, _why('cast_glow', _err, _e, _FOREIGN)
    _rows = [_r.replace('’', "'") for _r in _rows]
    if len(_rows) == 1 and _who in _rows[0] and _bad in _rows[0]:
        continue
    assert _rows or type(_val).__name__ != 'str', (
        'Show the line with `print(...)`, then `return` on the next line. `return` with text after it hands the text '
        'back, and nothing shows.' + _ev(_e, 'nothing showed'))
    assert _rows, ("Show a line before `return`: `print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")`."
                   + _ev(_e, 'nothing showed'))
    assert len(_rows) == 1, 'Show one line, then `return`.' + _ev(_e, str(len(_rows)) + ' lines showed')
    _l = _rows[0]
    assert not ('Lucky' in _l or 'Star Glow' in _l), (
        'Build the line from `hero["name"]` and `spell_name`, so it fits every hero and every spell.'
        + _ev(_e, 'the line named ' + ('Lucky' if 'Lucky' in _l else 'Star Glow')))
    assert _who in _l, "Put the hero's name in the line: `hero[\"name\"]`." + _ev(_e, 'the line should name ' + _who)
    assert False, ("Put the spell's name in the line: `spell_name`, no quotes."
                   + _ev(_e, 'the line should name ' + _bad))
"""

_GUARD_GOES = _GUARD_CASES + r"""
_s = _pell()
_val, _rows, _err = _call(_f, [_s, 'Moon Step'])
_e = 'called `cast_glow` for Pell with "Moon Step", a spell Pell knows'
assert not _err, _why('cast_glow', _err, _e, _FOREIGN)
if not (_s['mana'] == 8 and 'Pell casts Moon Step.' in _rows):
    _said = 'Pell should cast it and have 8 mana left'
    _cmp = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Compare']
    _quoted = [_c for _c in _cmp if type(_c.left).__name__ == 'Constant' and _c.left.value == 'spell_name']
    assert not _quoted, 'Take the quotes off `spell_name` in your `if`. ' + _QUOTES + _ev(_e, _said)
    _sheet = [_c for _c in _cmp if any(type(_x).__name__ == 'Name' and _x.id == 'hero' for _x in _c.comparators)]
    assert not _sheet, ("Ask the spell book, not the whole sheet: `hero[\"spell_book\"]`. `spell_name not in hero` "
                        "looks at the sheet's own keys, like `\"mana\"`, so every spell is stopped." + _ev(_e, _said))
    _tg = [_i.lineno for _i in _ifs if any(type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'str'
                                           and _c.value not in ('spell_book', 'name', 'mana', 'mana_cost')
                                           for _c in _ast.walk(_i.test))]
    assert not _tg, ('Ask the spell book, `if spell_name not in hero["spell_book"]:`, so the guard fits every hero. '
                     'The `if` on line ' + str(_tg[0]) + ' asks about one typed spell name, so a spell the hero '
                     'knows is stopped too.' + _ev(_e, _said))
    _out = _outer('cast_glow')
    assert not _out, ('Use `hero`, the sheet that was handed in, not `' + _out[0] + '`, in the guard and below it.'
                      + _ev(_e, _said))
    _loose = [_n.lineno for _n in _d.body if type(_n).__name__ == 'Return']
    assert not _loose, ("Indent `return` under the `if`. On line " + str(_loose[0]) + ", at the function's own level, "
                        "it stops every spell, known or not." + _ev(_e, _said))
    _in = [_c for _c in _cmp if any(type(_o).__name__ == 'In' for _o in _c.ops)]
    assert not _in, ('Ask `not in`: the guard stops a spell that is not in the book. `in` stops the spells the hero '
                     'knows.' + _ev(_e, _said))
    assert False, ('Keep the lines below the guard as the starter has them, so a known spell goes ahead.'
                   + _ev(_e, _said))
"""

_GUARD_MANA = _GUARD_CASES + r"""
_mg = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Constant'
       and type(_c.value).__name__ in ('int', 'float')]
# Two spells with different costs, so a typed cost (`< 3`) is caught.
for _s, _sp, _who in [(_pell(2), 'Moon Step', 'Pell, mana 2, with "Moon Step", which costs 3'),
                      ({'name': 'Moth', 'mana': 4, 'spell_book': {'Sun Ward': {'mana_cost': 5}}}, 'Sun Ward',
                       'Moth, mana 4, with "Sun Ward", which costs 5')]:
    _start = _s['mana']
    _val, _rows, _err = _call(_f, [_s, _sp])
    _e = 'called `cast_glow` for ' + _who
    assert not _err, _why('cast_glow', _err, _e, _FOREIGN)
    if _s['mana'] == _start and not any(' casts ' in _r for _r in _rows):
        assert _rows, 'Show a line before the second `return`, so the hero knows why.' + _ev(_e, 'nothing showed')
        continue
    assert not _mg, ("Compare with the spell's own cost, `spell[\"mana_cost\"]`, not a typed number, so every spell "
                     'is checked.' + _ev(_e, 'the spell should not be cast'))
    assert False, ('Add a second guard below the `spell = ...` line: if `hero["mana"]` is less than '
                   '`spell["mana_cost"]`, show a line and `return`.' + _ev(_e, 'the spell should not be cast'))
_t = _pell(3)
_val, _rows, _err = _call(_f, [_t, 'Moon Step'])
_e = 'called `cast_glow` for Pell, mana 3, with "Moon Step", which costs 3'
assert not _err, _why('cast_glow', _err, _e, _FOREIGN)
assert _t['mana'] == 0, 'Exactly enough mana should still cast: use `<`, not `<=`.' + _ev(_e, 'Pell should cast it')
"""

GUARD_AT_THE_DOOR = dict(
    id="guard-at-the-door",
    title="Guard at the door",
    martu=(
        "A [[guard]] checks first. If something is wrong, it says so and stops the function with `return`. Nothing "
        "below "
        "it runs.\n"
        "Run the starter first. Lucky tries a spell he does not know, and Python stops with a KeyError.\n"
        "A guard at the top of `cast_glow` stops that, politely, before the line that reads the spell. Three lines: "
        "an `if`, the line it shows, then `return`. A good guard does not argue, yes?"
    ),
    example=(
        "def open_door(name, guests):\n"
        "    if name not in guests:\n"
        '        print(name + " waits.")\n'
        "        return\n"
        '    print(name + " comes in.")\n'
        "\n"
        "\n"
        'guests = ["Oogrish", "Lucky"]\n'
        'open_door("Oogrish", guests)\n'
        'open_door("Moth", guests)\n'
    ),
    example_output="Oogrish comes in.\nMoth waits.",
    names=["cast_glow", "hero", "spell_name"],
    predict=dict(
        q=(
            "Before you press Run: Lucky's book has only Glow. Glow goes first, and its line shows. What happens "
            "next, when he tries Star Glow?"
        ),
        choices=["Lucky casts Star Glow.\n22", "24", "ERROR: KeyError: 'Star Glow'"],
        answer=2,
        explain=(
            "`hero[\"spell_book\"][\"Star Glow\"]` asks for a key his book does not have, so Python stops with a "
            "KeyError. The last line never runs. Your guard will ask first, and stop the function kindly."
        ),
    ),
    starter=GUARD_STARTER,
    checkpoints=[
        dict(
            id="guard-stops",
            text=(
                "Add a guard at the top of `cast_glow`. If `spell_name` is not in `hero[\"spell_book\"]`, show a line "
                "like `Lucky doesn't know Star Glow.` and `return`."
            ),
            dictated=False,
            hints=[
                "Still a KeyError on Star Glow? Your guard let it through. Check: `not in`, `return` under the "
                "`print` inside the `if`, and the guard above `spell = ...`. The guard is three lines: `if`, "
                "`print`, `return`. Leave the bottom calls alone: `\"Star Glow\"` is the test.",
                "In the Example, `if name not in guests:` asks first. Under it come the message, then `return`, so "
                "`comes in` never runs for Moth.",
                "Without `return`, the function shows the line and carries on to the spell, and Python stops with a "
                "KeyError. Indent `return` under the `if`.",
                "Write `if spell_name not in hero[\"spell_book\"]:` at the top. Under it, indent "
                "`print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")`, then `return`.",
            ],
            checks=[
                check("an unknown spell stops the function", _GUARD_STOPS, GUARD_FOREIGN),
                check("the guard names the hero and the spell", _GUARD_LINE, GUARD_FOREIGN),
            ],
            pass_line="Oogrish: Steady, now. The door asks first. Good.",
        ),
        dict(
            id="known-spell-goes-ahead",
            text="Make sure a spell the hero knows still goes ahead and spends its mana.",
            dictated=False,
            hints=[
                "Run, and read the first line: Lucky should still cast Glow. If he doesn't, look at what your `if` "
                "asks.",
                "In the Example, `return` sits inside the `if`, indented under it. Lined up with the `if`, it would "
                "stop Oogrish too.",
                "Ask the spell book, `hero[\"spell_book\"]`, about the parameter `spell_name`, with no quotes.",
                "Keep `if spell_name not in hero[\"spell_book\"]:`, with the `print` and the `return` indented under it.",
            ],
            checks=[check("a known spell still goes ahead", _GUARD_GOES, GUARD_FOREIGN)],
            pass_line="Mar'tu: Known spells go in. Strangers wait outside. That is a guard.",
        ),
    ],
    solution=GUARD_SOLUTION,
    assemble=dict(
        lines=[line for line in GUARD_SOLUTION.splitlines() if line.strip() and not line.strip().startswith("#")],
        distractors=['    if spell_name in hero["spell_book"]:', "    return", '    if "spell_name" not in hero["spell_book"]:'],
    ),
    partials=[_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                           "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n    return\n",
                     bottom='cast_glow(lucky, "Star Glow")\nprint(lucky["mana"])\n')],
    another_way=[
        dict(
            angle="everyday",
            text=(
                "A guard checks your name at the door before anything else happens. Not on the list? You hear why, "
                "and that is the end of it. On the list? In you go."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `cast_glow(lucky, \"Star Glow\")`: `spell_name` is `\"Star Glow\"`.\n"
                "2. The guard asks: is `\"Star Glow\"` not in Lucky's book? Yes, it is not.\n"
                "3. It shows `Lucky doesn't know Star Glow.`\n"
                "4. `return` ends the function. The spell line never runs, so no KeyError."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "`cast_spell` in hold-the-barrier opened with this very guard: `if spell_name not in "
                "caster[\"spell_book\"]:`, a message, then `return`. Only after it did the function read the spell."
            ),
        ),
        dict(
            angle="why",
            label="Why does this work? `return` is `break` for a whole function",
            text=(
                "In Unit 6, `break` stopped a loop early. `return` stops a whole function early. Everything after it "
                "is skipped, so the guard needs no `else`."
            ),
        ),
    ],
    bonus=dict(
        by="lucky",
        title="Not enough mana",
        text=(
            "What's in it for me? No embarrassing fizzles. Add a second guard below `spell = ...`: if `hero[\"mana\"]` "
            "is less than `spell[\"mana_cost\"]`, show a line and `return`. Exactly enough mana still casts."
        ),
        hints=[
            "The second guard needs the spell, so it goes after `spell = hero[\"spell_book\"][spell_name]`.",
            "`if fuel < 3:` asks whether the fuel is less than 3. Exactly 3 is not less, so it goes ahead.",
            "Write `if hero[\"mana\"] < spell[\"mana_cost\"]:`, then indent a `print` and `return` under it.",
        ],
        checks=[check("too little mana stops the spell; exactly enough casts", _GUARD_MANA, GUARD_FOREIGN)],
        solution=_guard(work='    spell = hero["spell_book"][spell_name]\n'
                             '    if hero["mana"] < spell["mana_cost"]:\n'
                             '        print(hero["name"] + " needs more mana.")\n'
                             "        return\n"
                             '    hero["mana"] = hero["mana"] - spell["mana_cost"]\n'
                             '    print(hero["name"] + " casts " + spell_name + ".")\n'),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="hold-the-barrier",
        snippet='if spell_name not in caster["spell_book"]:\n    print_prompt(...)\n    return',
        why=(
            "You have seen this. The barrier spell opened with a guard: a caster who did not know the spell heard "
            "why, and `return` stopped the function before it read the spell."
        ),
    ),
    takeaway=(
        "Guard first: `if spell_name not in hero[\"spell_book\"]:`, a message, then `return`, at the top of the "
        "function, before the work."
    ),
    wrong_answers=[
        dict(why="starter: no guard (the predict's KeyError)", code=GUARD_STARTER, fails_at=0,
             message_contains="KeyError: 'Star Glow'"),
        dict(why="a guard with no return: shows the line, then carries on to the spell",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"),
             fails_at=0, message_contains="KeyError"),
        dict(why="an if/else guard that never returns: the work below still runs",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"
                               "    else:\n        print(hero[\"name\"] + \" knows it.\")\n"),
             fails_at=0, message_contains="KeyError"),
        dict(why="the early return placed after the work (the guard comes too late)",
             code=_guard(guard="", work=CAST_WORK.split("\n")[0] + "\n" + GUARD_LINES
                         + "\n".join(CAST_WORK.split("\n")[1:])),
             fails_at=0, message_contains="KeyError"),
        dict(why="`in` for `not in`", code=_guard(guard=GUARD_LINES.replace(" not in ", " in ")), fails_at=0,
             message_contains="KeyError"),
        dict(why="no return, and the bottom test changed to a known spell to stop the crash (the explainer's 'use a "
                 "key that is already there'): the check still calls an unknown spell",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n",
                         bottom=CAST_BOTTOM.replace("Star Glow", "Glow")),
             fails_at=1, message_contains="Put `return` under the line"),
        dict(why="the guard after the read, bottom test changed: the check names the order",
             code=_guard(guard="", work=CAST_WORK.split("\n")[0] + "\n" + GUARD_LINES
                         + "\n".join(CAST_WORK.split("\n")[1:]), bottom=CAST_BOTTOM.replace("Star Glow", "Glow")),
             fails_at=1, message_contains="Move the guard to the top"),
        dict(why="return not indented under the if: it stops every spell",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n    return\n"),
             fails_at=2, message_contains="Indent `return`"),
        dict(why="the parameter in quotes in the if: every spell is stopped",
             code=_guard(guard=GUARD_LINES.replace("if spell_name", 'if "spell_name"')), fails_at=2,
             message_contains="Take the quotes off `spell_name` in your `if`. Quotes mean"),
        dict(why="asks the hero's sheet, not its spell book (the wrong sheet)",
             code=_guard(guard=GUARD_LINES.replace('not in hero["spell_book"]', "not in hero")), fails_at=2,
             message_contains="Ask the spell book"),
        dict(why="asks lucky's book, not hero's (a typed test sheet)",
             code=_guard(guard=GUARD_LINES.replace('not in hero["spell_book"]', 'not in lucky["spell_book"]')),
             fails_at=2, message_contains="not `lucky`"),
        dict(why="the guard looks for the task's one unknown spell (a typed test value): other spells get through",
             code=_guard(guard='    if spell_name == "Star Glow":\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"
                               "        return\n"),
             fails_at=1, message_contains="one typed spell name"),
        dict(why='a guard that asks about one typed spell name (if spell_name != "Glow"): it stops spells the hero knows',
             code=_guard(guard='    if spell_name != "Glow":\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"
                               "        return\n"),
             fails_at=2, message_contains="one typed spell name"),
        dict(why="the work below the guard spends Lucky's mana, not hero's (the wrong sheet)",
             code=_guard(work=CAST_WORK.replace('hero["mana"] = hero["mana"]', 'lucky["mana"] = lucky["mana"]')),
             fails_at=2, message_contains="not `lucky`"),
        dict(why="the message typed for Lucky (PAR)",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(\"Lucky doesn't know Star Glow.\")\n        return\n"),
             fails_at=1, message_contains="Build the line"),
        dict(why="return before the print: nothing shows",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n        return\n'
                               "        print(hero[\"name\"] + \" doesn't know \" + spell_name + \".\")\n"),
             fails_at=1, message_contains="Show a line before `return`"),
        dict(why="the message returned instead of shown",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        return hero[\"name\"] + \" doesn't know \" + spell_name + \".\"\n"),
             fails_at=1, message_contains="nothing shows"),
        dict(why="the spell's name missing from the line",
             code=_guard(guard='    if spell_name not in hero["spell_book"]:\n'
                               "        print(hero[\"name\"] + \" doesn't know that.\")\n        return\n"),
             fails_at=1, message_contains="spell's name"),
    ],
    notes=(
        meta(starter_level="S3", path="CC", skills="early-return", solo="false", dictates="",
             foreign_names="open_door,name,guests,fuel",
             par='(Pell knows Moon Step, "Ash Ward"),(Moth knows Glow, "Sun Ward"),(Pell, "Moon Step")') + "\n"
        "P -> I -> M; skill gate pattern:EarlyReturn. S3: the function's work is the given skeleton, the guard's "
        "place is marked by comment 1. The predict is the starter itself: its right choice is what the console "
        "shows, `Lucky casts Glow.` and then the ERROR line (a KeyError after Lucky casts Glow). "
        "CP1 [ND]: CALL with two invented heroes and unknown spells: one line naming the hero and the spell, built "
        "from the parameters (any wording passes; a typed Lucky line fails PAR), and the mana unchanged. CP2 [ND]: "
        "a known spell still goes ahead (mana spent, the starter's 'casts' line). The bottom calls crash on any "
        "guard that lets Star Glow through (no `return`, an if/else that falls through, the guard after the read, "
        "`in` for `not in`), so those fail at 0 with Python's KeyError and the hint ladder's Teach rung names the "
        "missing `return`; the checks keep their own KeyError messages for a changed bottom. Slips that refuse every "
        "spell pass CP1 and fail CP2 with their own message: `return` at the function's level (the partial), "
        "`\"spell_name\"` in quotes, the wrong sheet (`hero` for its spell book, `lucky` for `hero`). AW: everyday, "
        "step-by-step, from the campaign, and WT ('`return` is `break` for a whole function', Unit 6). BQ (guard + "
        "comparison): a mana guard, BND at exactly enough, with a second spell of another cost so a typed cost "
        "(`< 3`) is caught. A typed spell name in the guard (`if spell_name != \"Glow\":`) is named at CP2."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-06 read-the-helper (I -> R; P19 reading discipline)
# ---------------------------------------------------------------------------------------------

DRAW_HERO = (
    "def draw_bar(hero, bar):\n"
    "    # This function is already finished.\n"
    "    # Leave it as it is.\n"
    "    # It draws bar in this hero's row.\n"
    '    print(hero["name"] + " " + bar)\n'
)
DRAW_CALL = 'draw_bar(lucky, "███░")'


def _helper(call=DRAW_CALL + "\n", draw=DRAW_HERO):
    return (draw + "\n\n" + LUCKY_20 + "# 1. Call draw_bar for Lucky, with any\n#    bar text, in quotes.\n" + call)


HELPER_STARTER = _helper(call="")
HELPER_SOLUTION = _helper()

_KEEP_HERO = r"""
_k = _keep('draw_bar', __ORIG__)
assert _k != 'gone', 'Keep `draw_bar` at the top, as the starter has it. It is already finished.'
assert not _k, ("Leave `draw_bar` as it is: it is already finished. Something inside it changed, so put it back the "
                "way the starter had it, and call it at the bottom instead.")
"""

_CALL_HERO = r"""
_b = _bare('draw_bar')
assert not _b, ('Write `()` after the name, with the two values inside: `draw_bar(lucky, "███░")`. Line ' + str(_b[0])
                + ' says `draw_bar` with no `()`, so it is not called.')
_ns, _ls, _seen, _err = _trace(['draw_bar'])
_mine = [_c[1] for _c in _seen if _c[2] == '<module>']
assert _mine, ("At the bottom, call `draw_bar` with Lucky's sheet first and your bar text second: "
               '`draw_bar(lucky, "███░")`.')
_lk = _ns.get('lucky')
_ok = [_c for _c in _mine if _c.get('hero') is _lk and type(_c.get('bar')).__name__ == 'str']
if not _ok:
    assert _mine[0].get('hero') is _lk, "Hand over Lucky's sheet first: the variable `lucky`, with no quotes."
    assert False, 'Hand over the bar text second, in quotes.'
assert any(_c['bar'].strip() for _c in _ok), 'Put some bar text inside the quotes, like `"███░"`.'
_w = _wrapped('draw_bar')
assert not _w, ('Write the call on its own line: `draw_bar(lucky, "███░")`. `draw_bar` shows the line itself. Line '
                + str(_w[0]) + ' puts the call inside `print(...)`, which adds a line that says `None`.')
"""

READ_THE_HELPER = dict(
    id="read-the-helper",
    title="Read the helper",
    martu=(
        "Not every function is yours to write. Some are finished [[helpers]]. Your job is to *read* one and call it "
        "right.\n"
        "Read the `def` line first. Its brackets say what to hand over, and in what order. The comments say what it "
        "does.\n"
        "Then leave its steps alone. In the campaign, `print_mana(caster, mana_bar)` was a helper like this one."
    ),
    names=["draw_bar", "lucky"],
    pick='"███░"',
    predict=dict(
        q="Before you press Run: what does this call show?",
        code=(
            "def draw_bar(hero, bar):\n"
            '    print(hero["name"] + " " + bar)\n'
            "\n"
            "\n"
            'oogrish = {"name": "Oogrish"}\n'
            'draw_bar(oogrish, "███░")\n'
        ),
        choices=["Oogrish ███░", "hero bar", "███░ Oogrish", "ERROR: TypeError"],
        answer="Oogrish ███░",
        explain=(
            "The values land in the `def` line's order: `hero` gets Oogrish's sheet, `bar` gets the text. Then the "
            "helper shows the name, a space and the bar."
        ),
    ),
    pair_talk=(
        "Before you type, ask your partner two things. Which lines of `draw_bar` should you change? What two things "
        "does it need? Then each of you calls it on your own screen."
    ),
    starter=HELPER_STARTER,
    checkpoints=[
        dict(
            id="call-the-helper",
            text="Call `draw_bar` for Lucky, with any bar text you like.",
            dictated=True,
            hints=[
                "Read the `def` line: `draw_bar(hero, bar)`. First a hero's sheet, then the bar text. Lucky's sheet "
                "is the variable `lucky`.",
                "The predict's `draw_bar(oogrish, \"███░\")` handed over a sheet first and text second, in the `def` "
                "line's order.",
                "Leave `draw_bar` as it is. Your line goes at the bottom, at the left edge, outside the function.",
                "At the bottom, write `" + DRAW_CALL + "`.",
            ],
            checks=[
                check("draw_bar is unchanged", _KEEP_HERO, orig=DRAW_HERO),
                check("draw_bar is called for Lucky with bar text", _CALL_HERO),
            ],
            pass_line="Mar'tu: You read it, you called it, you left it alone. That is most of programming, yes?",
        ),
    ],
    solution=HELPER_SOLUTION,
    another_way=[
        dict(
            angle="check",
            label="Two quick questions",
            text=(
                "Which lines of `draw_bar` should you change? None: it is finished.\n"
                "What two things does it need? A hero's sheet, then the bar text, in that order."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Read the `def` line: `hero`, then `bar`.\n"
                "2. Match each one to something you have: `lucky` for `hero`, your text for `bar`.\n"
                "3. Write the call in that order, at the bottom: `draw_bar(lucky, \"███░\")`.\n"
                "4. Run. The helper does the rest."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Like a vending machine: you don't open it up. You read the label, put in what it asks for, in the "
                "order it asks, and press the button."
            ),
        ),
    ],
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="def print_mana(caster, mana_bar):\n    # This function is already finished.",
        why=(
            "You have seen this. `print_mana` said it was finished, so you left it alone and only called it: the "
            "caster first, then the bar. Same reading, same order, here."
        ),
    ),
    takeaway=(
        "A finished helper: read its `def` line for what to hand over and in what order, call it, and leave its "
        "steps alone."
    ),
    wrong_answers=[
        dict(why="starter: not called yet", code=HELPER_STARTER, fails_at=1, message_contains="At the bottom, call"),
        dict(why="the helper edited (its print changed)",
             code=_helper(draw=DRAW_HERO.replace('" " + bar', '": " + bar')), fails_at=1,
             message_contains="already finished"),
        dict(why="the helper's parameters renamed to fit the call",
             code=_helper(draw=DRAW_HERO.replace("(hero, bar)", "(lucky, bar)").replace('hero["name"]', 'lucky["name"]')),
             fails_at=1, message_contains="already finished"),
        dict(why="the call indented inside the helper (it becomes a step of draw_bar)",
             code=_helper(call="", draw=DRAW_HERO + '    draw_bar(lucky, "███░")\n'), fails_at=1,
             message_contains="already finished"),
        dict(why="the values in the wrong order", code=_helper('draw_bar("███░", lucky)\n'), fails_at=0,
             message_contains="string indices"),
        dict(why="one value only", code=_helper("draw_bar(lucky)\n"), fails_at=0,
             message_contains="missing 1 required positional argument"),
        dict(why="three values", code=_helper('draw_bar(lucky, "███", "░")\n'), fails_at=0,
             message_contains="takes 2 positional arguments"),
        dict(why="Lucky's name typed where his sheet goes", code=_helper('draw_bar("Lucky", "███░")\n'), fails_at=0,
             message_contains="string indices"),
        dict(why="a number where the bar text goes", code=_helper("draw_bar(lucky, 20)\n"), fails_at=0,
             message_contains="can only concatenate"),
        dict(why="the call wrapped in print (an extra None line)", code=_helper('print(draw_bar(lucky, "███░"))\n'),
             fails_at=1, message_contains="None"),
        dict(why="the name with no ()", code=_helper("draw_bar\n"), fails_at=1, message_contains="no `()`"),
        dict(why="the line printed by hand, no call", code=_helper('print("Lucky ███░")\n'), fails_at=1,
             message_contains="At the bottom, call"),
        dict(why="empty bar text", code=_helper('draw_bar(lucky, "")\n'), fails_at=1, message_contains="some bar text"),
        dict(why="another sheet handed over", code=_helper('draw_bar({"name": "Lucky"}, "███░")\n'), fails_at=1,
             message_contains="Lucky's sheet first"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="read-helper", solo="false", dictates="1", foreign_names="oogrish") + "\n"
        "I -> R, S4 (the helper is given whole; one call to write). CP1 [D]: KEEP (AST compare with the starter's "
        "own `draw_bar`, comments aside), then CALL by behavior: the whole program is run again in a fresh "
        "namespace with every call to `draw_bar` recorded (_trace), and one call from the bottom must hand over "
        "the program's own `lucky` first and non-empty text second (any text: pick ███░). The spec's one-click "
        "questions ('Which lines should you change?', 'What two things does it need?') have no widget yet: they "
        "are the pair-talk prompt and the 'Two quick questions' angle (site request: a one-click question). Wrong "
        "order or number of values crash at 0 with Python's own line (TypeError rows). An edited helper, renamed "
        "parameters and a call indented into the helper fail KEEP. Lucky's box is `print_mana(caster, mana_bar)` "
        "(P19 practice)."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-07 bar-then-draw (Mk, rehearsal of mana-bars: Gearshift's starlode gauge)
# ---------------------------------------------------------------------------------------------

DRAW_ROBOT = (
    "def draw_bar(robot, bar):\n"
    "    # This function is already finished.\n"
    "    # Leave it as it is.\n"
    "    # It draws bar in this robot's row.\n"
    '    print(robot["name"] + " " + bar)\n'
)
FULL_LINE = 'full = "▮" * robot["fuel"]'
EMPTY_LINE = 'empty = "▯" * (robot["max_fuel"] - robot["fuel"])'
STORE_BAR = "fuel_bar = get_fuel_bar(robot)"
PASS_BAR = "draw_bar(robot, fuel_bar)"
FUEL_RETURN = '    return "Fuel [" + full + empty + "] " + str(robot["fuel"]) + "/" + str(robot["max_fuel"])\n'
ROBOTS = (
    "gearshift = {\n"
    '    "name": "Gearshift",\n'
    '    "fuel": 4,\n'
    '    "max_fuel": 6,\n'
    "}\n"
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "fuel": 2,\n'
    '    "max_fuel": 7,\n'
    "}\n"
    "robots = [gearshift, bomb_shell]\n"
    "for robot in robots:\n"
    "    show_fuel(robot)\n"
)


START_PRINT = "print(get_fuel_bar(robot))"


def _fuel(full='full = "▮" * 0', empty='empty = "▯" * 0', show="    " + START_PRINT + "\n", draw=DRAW_ROBOT):
    return (draw + "\n\n"
            "def get_fuel_bar(robot):\n"
            '    # 1. Change this 0 to robot["fuel"].\n'
            "    " + full + "\n"
            "    # 2. Change this 0 to the fuel used:\n"
            '    #    robot["max_fuel"] - robot["fuel"]\n'
            "    " + empty + "\n" + FUEL_RETURN + "\n\n"
            "def show_fuel(robot):\n"
            "    # 3. Replace this print line:\n"
            "    #    store the result of\n"
            "    #    get_fuel_bar(robot)\n"
            "    #    in a variable.\n"
            "    # 4. Pass the robot and that\n"
            "    #    variable to draw_bar().\n" + show + "\n\n" + ROBOTS)


FUEL_STARTER = _fuel()
FUEL_SOLUTION = _fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    " + PASS_BAR + "\n")
FUEL_PARTIALS = [
    _fuel(FULL_LINE),                                       # the starter's print line still shows both bars
    _fuel(FULL_LINE, EMPTY_LINE),
    _fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n"),  # comment 3: the store line replaces the print line
]
FUEL_FOREIGN = ["greeting", "get_greeting", "dialogue"]

_FUEL_HEAD = r"""
def _want(_r):
    return ('Fuel [' + '▮' * _r['fuel'] + '▯' * (_r['max_fuel'] - _r['fuel']) + '] ' + str(_r['fuel']) + '/'
            + str(_r['max_fuel']))


def _robot(_name, _fuel, _top):
    return {'name': _name, 'fuel': _fuel, 'max_fuel': _top}


_f = _need('get_fuel_bar', ['robot'])
_d = _defs()['get_fuel_bar']
_out = _outer('get_fuel_bar')
"""

_FUEL_FULL = _FUEL_HEAD + r"""
for _r, _who in [(_robot('Bellows', 3, 5), 'Bellows, fuel 3 of 5'), (_robot('Tinplate', 1, 4), 'Tinplate, fuel 1 of 4')]:
    _locs, _val, _rows, _err = _capture(_f, [_r])
    _e = 'called `get_fuel_bar` for ' + _who
    # Step 1 is the full blocks only: a slip on the light-blocks line (step 2) is told at step 2.
    _full = _locs.get('full')
    _later = _err is not None and type(_full).__name__ == 'str' and type(_err).__name__ == 'TypeError'
    assert not _err or _later, _why('get_fuel_bar', _err, _e, _FOREIGN)
    if not _later:
        assert type(_val).__name__ == 'str', ('Keep the `return` line at the end of `get_fuel_bar`, as the starter '
                                              'has it.' + _ev(_e, 'it returned no bar'))
    _n = (_full if _later else _val).count('▮')
    if _n == _r['fuel']:
        continue
    _said = 'the bar should have ' + str(_r['fuel']) + ' full blocks'
    assert _n != 0, ('Replace the first 0 with `robot["fuel"]`: one full block for each point of fuel.'
                     + _ev(_e, 'the bar had no full blocks'))
    assert _n != _r['max_fuel'], ('Use `robot["fuel"]`, the fuel left. That reads `"max_fuel"`.'
                                  + _ev(_e, _said + ', not ' + str(_n)))
    assert not _out, ('Read from `robot`, the parameter, not `' + _out[0] + '`. `robot` is whichever robot the call '
                      'hands over.' + _ev(_e, _said + ', not ' + str(_n)))
    assert False, ('Use `robot["fuel"]`, not a typed number, so the bar follows the robot.'
                   + _ev(_e, _said + ', not ' + str(_n)))
"""

_FUEL_BAR = _FUEL_HEAD + r"""
_em = [_n.value for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign'
       and any(getattr(_t, 'id', '') == 'empty' for _t in _n.targets)]
_zero = bool(_em) and type(_em[0]).__name__ == 'BinOp' and type(_em[0].right).__name__ == 'Constant' and _em[0].right.value == 0
for _r, _who in __CASES__:
    _r = _robot(*_r)
    _val, _rows, _err = _call(_f, [_r])
    _e = 'called `get_fuel_bar` for ' + _who
    assert not _err, _why('get_fuel_bar', _err, _e, _FOREIGN)
    _w = _want(_r)
    if _val == _w:
        continue
    assert type(_val).__name__ == 'str', ('Keep the `return` line at the end of `get_fuel_bar`, as the starter has it.'
                                          + _ev(_e, 'it returned no bar'))
    _said = 'it should return `' + _w + '`'
    _m, _used = _val.count('▯'), _r['max_fuel'] - _r['fuel']
    assert not (_zero and _used), ('Replace the second 0 with `robot["max_fuel"] - robot["fuel"]`, in brackets: the '
                                   'fuel used.' + _ev(_e, _said))
    # A typed number (`"▯" * 2`, `(6 - robot["fuel"])`) and the wrong sheet first: by value they can look like
    # another slip.
    _tn = [_c.value for _x in _em for _c in _ast.walk(_x) if type(_c).__name__ == 'Constant'
           and type(_c.value).__name__ == 'int']
    assert not _tn, ('Work the light blocks out from `robot`: `robot["max_fuel"] - robot["fuel"]`, not a typed '
                     + str(_tn[0]) + ', so every gauge fits.' + _ev(_e, _said))
    assert not _out, 'Read from `robot`, the parameter, not `' + _out[0] + '`.' + _ev(_e, _said)
    assert _m != _r['max_fuel'] or not _used, ('Make the light blocks the fuel used: `robot["max_fuel"] - '
                                               'robot["fuel"]`, not the max fuel alone.' + _ev(_e, _said))
    assert _m != _r['fuel'] or _r['fuel'] == _used, ('Make the light blocks the fuel used: `robot["max_fuel"] - '
                                                     'robot["fuel"]`, not the fuel left.' + _ev(_e, _said))
    assert not (_m == 0 and _used), ('Start from the max fuel: `robot["max_fuel"] - robot["fuel"]`. The other way '
                                     'round is less than 0, so no light blocks show.' + _ev(_e, _said))
    assert not _out, 'Read from `robot`, the parameter, not `' + _out[0] + '`.' + _ev(_e, _said)
    assert False, 'Make the light blocks `"▯" * (robot["max_fuel"] - robot["fuel"])`.' + _ev(_e, _said)
"""

_FUEL_STORE = r"""
_f = _need('show_fuel', ['robot'])
_d = _defs()['show_fuel']
_asg = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
        and type(_n.targets[0]).__name__ == 'Name']
_st = [_n for _n in _asg if type(_n.value).__name__ == 'Call' and getattr(_n.value.func, 'id', '') == 'get_fuel_bar']
if not _st:
    _fn = [_n for _n in _asg if type(_n.value).__name__ == 'Name' and _n.value.id == 'get_fuel_bar']
    assert not _fn, ('Call it, with `()`: `' + (_fn[0].targets[0].id if _fn else 'fuel_bar') + ' = get_fuel_bar(robot)`. '
                     'With no `()`, the variable holds the function itself, not a bar.')
    _q = [_n for _n in _asg if type(_n.value).__name__ == 'Constant' and 'get_fuel_bar' in str(_n.value.value)]
    assert not _q, ('Take the quotes off: `fuel_bar = get_fuel_bar(robot)`. With quotes, the variable holds those '
                    'letters, not a bar. ' + _QUOTES)
    _top_st = [_n.lineno for _t in _top() for _n in _ast.walk(_t) if type(_n).__name__ == 'Assign'
               and _calls_in([_n.value], 'get_fuel_bar')]
    assert not _top_st, ('Put the store line inside `show_fuel`, indented, where the print line was. Line '
                         + str(_top_st[0]) + ' is outside it.')
    assert not _calls_in([_d], 'get_fuel_bar'), ('Store the bar first, with `=`: `fuel_bar = get_fuel_bar(robot)`. '
                                                 'Right now the bar is made, then lost.')
    assert False, ('In `show_fuel`, store the bar: `fuel_bar = get_fuel_bar(robot)`, the call on the right, a '
                   'variable on the left.')
_a = list(_st[0].value.args) + [_k.value for _k in _st[0].value.keywords]  # `get_fuel_bar(robot=robot)` is fine
assert len(_a) == 1 and type(_a[0]).__name__ == 'Name' and _a[0].id == 'robot', (
    'Hand over `robot`, the parameter of `show_fuel`: `get_fuel_bar(robot)`, so each robot gets its own bar.')
_val, _rows, _err, _rec = _stubbed(_f, [{'name': 'Bellows', 'fuel': 3, 'max_fuel': 5}], 'draw_bar')
assert not _err, _why('show_fuel', _err, 'called `show_fuel` for Bellows, fuel 3 of 5', _FOREIGN)
"""

_KEEP_ROBOT = r"""
_k = _keep('draw_bar', __ORIG__)
assert _k != 'gone', 'Keep `draw_bar` at the top, as the starter has it. It is already finished.'
assert not _k, ("Leave `draw_bar` as it is: it is already finished. Something inside it changed, so put it back the "
                "way the starter had it.")
"""

_FUEL_DRAW = r"""
_f = _need('show_fuel', ['robot'])
_d = _defs()['show_fuel']
_r = {'name': 'Bellows', 'fuel': 3, 'max_fuel': 5}
_w = 'Fuel [▮▮▮▯▯] 3/5'
_val, _rows, _err, _rec = _stubbed(_f, [_r], 'draw_bar')
_e = 'called `show_fuel` for Bellows, fuel 3 of 5'
assert not _err, _why('show_fuel', _err, _e, _FOREIGN)
_stored = [_n.targets[0].id for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and len(_n.targets) == 1
           and type(_n.targets[0]).__name__ == 'Name' and _calls_in([_n.value], 'get_fuel_bar')]
_v = _stored[0] if _stored else 'fuel_bar'
assert _rec, ('Pass the robot and that variable to `draw_bar()`: `draw_bar(robot, ' + _v + ')`, under the line that '
              'stores it.' + _ev(_e, '`draw_bar` was not called'))
assert len(_rec) == 1, 'Call `draw_bar` once in `show_fuel`.' + _ev(_e, '`draw_bar` was called ' + str(len(_rec)) + ' times')
_a = _rec[0]
assert len(_a) == 2, ('Hand `draw_bar` two things, as its `def` line says: the robot, then the bar.'
                      + _ev(_e, '`draw_bar` got ' + str(len(_a))))
_x, _y = _a
assert not (type(_x).__name__ == 'str' and type(_y).__name__ == 'dict'), (
    "Hand them over in the `def` line's order, the robot first: `draw_bar(robot, " + _v + ")`."
    + _ev(_e, 'the bar came first'))
assert type(_y).__name__ != 'function', ('Pass the variable you stored, not the function. `get_fuel_bar` with no `()` '
                                         'is the function itself, not a bar.' + _ev(_e, '`draw_bar` got a function'))
assert _x is _r, ('Hand over `robot`, the parameter of `show_fuel`, so every robot gets its own row.'
                  + _ev(_e, '`draw_bar` got another robot'))
assert not (type(_y).__name__ == 'str' and _y in _stored), (
    'Take the quotes off: `draw_bar(robot, ' + _v + ')`. With quotes, the helper gets the letters, not the bar. '
    + _QUOTES + _ev(_e))
assert _y == _w, ('Pass the bar that `get_fuel_bar(robot)` returned: the variable you stored.'
                  + _ev(_e, '`draw_bar` should get `' + _w + '`'))
_dc = _calls_in([_d], 'draw_bar')
_bar = None
if _dc:
    _kw = [_k.value for _k in _dc[0].keywords if _k.arg == 'bar']
    _bar = _dc[0].args[1] if len(_dc[0].args) >= 2 else (_kw[0] if _kw else None)
assert type(_bar).__name__ != 'Constant', ('Pass the variable you stored, `' + _v + '`, not typed text: store, then '
                                           'pass, so every robot gets its own bar.')
assert type(_bar).__name__ == 'Name' and _bar.id in _stored, (
    'Pass the variable you stored, `' + _v + '`, not a second call: store, then pass.')
# The starter's `print(get_fuel_bar(robot))` left in: the console shows each bar twice.
_pr = [_c for _c in _calls_in([_d], 'print') if _calls_in(list(_c.args), 'get_fuel_bar')]
assert not _pr, "Take out the starter's print line: `draw_bar` shows the row now."
"""

_GLUG_BAR = r"""
_f = _need('get_glug_bar', ['hero'], False)
for _h, _who in [({'name': 'Pell', 'glug': 2, 'max_glug': 5}, 'Pell, 2 sips of 5'),
                 ({'name': 'Moth', 'glug': 4, 'max_glug': 4}, 'Moth, 4 sips of 4')]:
    _val, _rows, _err = _call(_f, [_h])
    _e = 'called `get_glug_bar` for ' + _who
    assert not _err, _why('get_glug_bar', _err, _e, _FOREIGN)
    _w = '▓' * _h['glug'] + '░' * (_h['max_glug'] - _h['glug'])
    assert type(_val).__name__ == 'str' and _w in _val, (
        'Return `"▓"` for each sip left, then `"░"` for each sip drunk: `hero["max_glug"] - hero["glug"]`, in brackets.'
        + _ev(_e, 'the bar should hold `' + _w + '`'))
# By behavior: run the program again and record the calls to draw_bar from the bottom (store, then pass).
_ns, _ls, _seen, _err = _trace(['draw_bar'])
_lk = _ns.get('lucky')
_mine = [_c[1] for _c in _seen if _c[2] == '<module>' and _c[1].get('robot') is _lk
         and type(_c[1].get('bar')).__name__ == 'str' and '▓' in _c[1].get('bar')]
assert _mine, ("Draw Lucky's gauge with the helper, at the bottom: store `get_glug_bar(lucky)` in a variable, then "
               'pass it on: `draw_bar(lucky, ...)`.')
_dc = [_c for _c in _calls_in(_top(), 'draw_bar') if len(_c.args) >= 2 and type(_c.args[1]).__name__ == 'Name']
assert _dc, ('Store, then pass: keep `get_glug_bar(lucky)` in a variable first, then hand that variable to '
             '`draw_bar`.')
"""

BAR_THEN_DRAW = dict(
    id="bar-then-draw",
    title="Build the bar, then draw it",
    martu=(
        "Gearshift runs on starlode, and his gauge works like the mana bars. One function builds the bar. Another "
        "passes it to a finished helper that draws it.\n"
        "*Store, then pass*: keep what `get_fuel_bar(robot)` returns in a variable, then hand that variable to "
        "`draw_bar()`.\n"
        "The numbered comments match the steps, one each. The blocks `▮` and `▯` are already typed. When Gearshift's "
        "visor dims, he is doing this math, yes?"
    ),
    example=(
        'print("▮" * 3 + "▯" * (5 - 3))\n'
        "\n"
        "\n"
        "def get_greeting():\n"
        '    return "Barrier holding."\n'
        "\n"
        "\n"
        "greeting = get_greeting()\n"
        "print(greeting)\n"
    ),
    example_output="▮▮▮▯▯\nBarrier holding.",
    names=["get_fuel_bar", "show_fuel", "draw_bar", "robot"],
    predict=dict(
        q="Before you press Run: what does this line do?",
        code='print("▯" * 5 - 3)\n',
        choices=["▯▯", "▯▯▯▯▯", "ERROR: TypeError: unsupported operand type(s) for -: 'str' and 'int'"],
        answer=2,
        explain=(
            "Python does `*` before `-`. It makes `▯▯▯▯▯` first, then tries to take 3 away from text, and stops. "
            "Brackets go first: `\"▯\" * (5 - 3)` makes `▯▯`."
        ),
    ),
    starter=FUEL_STARTER,
    checkpoints=[
        dict(
            id="first-zero",
            text="Replace the first 0 with `robot[\"fuel\"]`.",
            dictated=True,
            hints=[
                "Look at comment 1, in `get_fuel_bar`. The number after `*` is how many full blocks to make.",
                "`\"▮\" * 3` makes `▮▮▮`. A key read gives a number too, so `\"▮\" * robot[\"fuel\"]` makes one block "
                "for each point of fuel.",
                "Change the line to `" + FULL_LINE + "`.",
            ],
            checks=[check("a test robot, 3 of 5: three full blocks", _FUEL_FULL, FUEL_FOREIGN)],
            pass_line="Gearshift: Four blocks for four fuel. Math checks out.",
        ),
        dict(
            id="second-zero",
            text="Replace the second 0 with `robot[\"max_fuel\"] - robot[\"fuel\"]`.",
            dictated=True,
            hints=[
                "Comment 2. The light blocks are the fuel used: the max fuel minus the fuel left. A TypeError about "
                "`-`? The subtraction needs brackets.",
                "Python does `*` before `-`. `\"▯\" * 5 - 3` tries to take 3 away from text. The Example puts the "
                "subtraction in brackets: `\"▯\" * (5 - 3)`.",
                "Change the line to `" + EMPTY_LINE + "`.",
            ],
            checks=[
                check("a test robot, 3 of 5: Fuel [▮▮▮▯▯] 3/5", _FUEL_BAR, FUEL_FOREIGN,
                      cases=[(("Bellows", 3, 5), "Bellows, fuel 3 of 5")]),
                check("empty and full gauges", _FUEL_BAR, FUEL_FOREIGN,
                      cases=[(("Tinplate", 0, 4), "Tinplate, fuel 0 of 4"), (("Tinplate", 4, 4), "Tinplate, fuel 4 of 4")]),
            ],
            pass_line="Gearshift: Empty reads empty. Full reads full. Gauge is honest.",
        ),
        dict(
            id="store-the-bar",
            text="In `show_fuel(robot)`, store the result of `get_fuel_bar(robot)` in a variable.",
            dictated=True,
            hints=[
                "Comment 3, in `show_fuel`. The print line shows the bar, then loses it. Keep what "
                "`get_fuel_bar(robot)` returns, with `=`.",
                "The Example stores first: `greeting = get_greeting()`, the call on the right, a variable on the left. "
                "In Module 1, `present_dialogue_option()` did the same.",
                "Write `" + STORE_BAR + "` in place of `" + START_PRINT + "`.",
            ],
            checks=[check("the bar is stored in a variable", _FUEL_STORE, FUEL_FOREIGN)],
        ),
        dict(
            id="pass-the-bar",
            text="Pass the robot and that variable to `draw_bar()`.",
            dictated=True,
            hints=[
                "Comment 4. `draw_bar` takes two things, as its `def` line says: the robot first, then the bar.",
                "Hand over the variable, not the function: `get_fuel_bar` with no `()` is the function itself, not a "
                "bar.",
                "Under the store line, write `" + PASS_BAR + "`.",
            ],
            checks=[
                check("draw_bar is unchanged", _KEEP_ROBOT, FUEL_FOREIGN, orig=DRAW_ROBOT),
                check("show_fuel draws the bar once", _FUEL_DRAW, FUEL_FOREIGN),
            ],
            pass_line="Bomb Shell: Two rows. Two gauges. Works.",
        ),
    ],
    solution=FUEL_SOLUTION,
    partials=FUEL_PARTIALS,
    assemble=dict(
        lines=[line for line in FUEL_SOLUTION.splitlines() if line.strip() and not line.strip().startswith("#")],
        distractors=['    empty = "▯" * robot["max_fuel"] - robot["fuel"]', "    draw_bar(robot, get_fuel_bar)",
                     "    draw_bar(fuel_bar, robot)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Who hands what to whom",
            text=(
                "```text\nshow_fuel(gearshift)\n  fuel_bar = get_fuel_bar(robot)\n      -> \"Fuel [▮▮▮▮▯▯] 4/6\"\n"
                "  draw_bar(robot, fuel_bar)\n      -> the row on screen\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. The loop at the bottom hands each robot to `show_fuel`.\n"
                "2. `show_fuel` calls `get_fuel_bar(robot)` and stores the bar.\n"
                "3. `get_fuel_bar` makes the full blocks, then the light ones, and returns the bar as text.\n"
                "4. `show_fuel` passes the robot and the stored bar to `draw_bar`, which draws the row."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Like a baker and a shop window. The baker makes the cake and hands it over. You carry it, then set it "
                "in the window. You never put the baker in the window."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "This is the mana bars, with fuel for mana. `get_mana_bar(caster)` built `\"█\" * caster[\"mana\"]` "
                "and `\"░\" * (caster[\"max_mana\"] - caster[\"mana\"])`. `show_mana` stored it and passed it to "
                "`print_mana`."
            ),
        ),
    ],
    tracer=True,
    bonus=dict(
        by="lucky",
        title="A glug gauge",
        text=(
            "What's in it for me? My canteen. At the bottom, make `lucky = {\"name\": \"Lucky\", \"glug\": 4, "
            "\"max_glug\": 6}`. Write `get_glug_bar(hero)`, which returns `\"▓\"` for each sip left and `\"░\"` for "
            "each sip drunk. Then store Lucky's bar and pass it to `draw_bar`."
        ),
        hints=[
            "`get_glug_bar` is a twin of `get_fuel_bar`: `\"▓\"` times the sips left, then `\"░\"` times the sips "
            "drunk, in brackets.",
            "`\"▓\" * 2 + \"░\" * (5 - 2)` makes `▓▓░░░`.",
            "Write `return \"▓\" * hero[\"glug\"] + \"░\" * (hero[\"max_glug\"] - hero[\"glug\"])` as its last line.",
        ],
        checks=[check("Lucky's glug gauge is drawn", _GLUG_BAR, FUEL_FOREIGN)],
        solution=FUEL_SOLUTION + (
            "\n\ndef get_glug_bar(hero):\n"
            '    return "▓" * hero["glug"] + "░" * (hero["max_glug"] - hero["glug"])\n'
            "\n\n"
            'lucky = {"name": "Lucky", "glug": 4, "max_glug": 6}\n'
            "glug_bar = get_glug_bar(lucky)\n"
            "draw_bar(lucky, glug_bar)\n"
        ),
    ),
    campaign_link=dict(
        module="friends-in-low-places",
        part="mana-bars",
        snippet="def show_mana(caster):\n    mana_bar = get_mana_bar(caster)\n    print_mana(caster, mana_bar)",
        why=(
            "You have seen this. The mana bars had the same four steps: two 0s, then store the bar, then pass it on. "
            "Now you know why each step sits where it does."
        ),
    ),
    takeaway=(
        "Build, store, pass: `fuel_bar = get_fuel_bar(robot)`, then `draw_bar(robot, fuel_bar)`. Brackets around "
        "the subtraction: `\"▯\" * (robot[\"max_fuel\"] - robot[\"fuel\"])`."
    ),
    wrong_answers=[
        dict(why="starter: both 0s left", code=FUEL_STARTER, fails_at=1, message_contains="first 0"),
        dict(why="a typed 4 (Gearshift's fuel) for the first 0",
             code=_fuel('full = "▮" * 4'), fails_at=1, message_contains="not a typed number"),
        dict(why="the max fuel for the full blocks", code=_fuel('full = "▮" * robot["max_fuel"]'), fails_at=1,
             message_contains='reads `"max_fuel"`'),
        dict(why="Gearshift's sheet read instead of the parameter (the wrong sheet)",
             code=_fuel('full = "▮" * gearshift["fuel"]'), fails_at=1, message_contains="not `gearshift`"),
        dict(why="the block times the whole sheet (the starter's print line runs it: crashes in the bottom loop)",
             code=_fuel('full = "▮" * robot'), fails_at=0, message_contains="can't multiply sequence by non-int"),
        dict(why="the block times the whole sheet, with the print line taken out: the check names it",
             code=_fuel('full = "▮" * robot', show="    pass\n"), fails_at=1, message_contains="not by the whole sheet"),
        dict(why="no brackets: \"▯\" * a - b (spec catch: precedence; the starter's print line runs it: crashes in "
                 "the bottom loop, as the predict shows)",
             code=_fuel(FULL_LINE, 'empty = "▯" * robot["max_fuel"] - robot["fuel"]'), fails_at=0,
             message_contains="unsupported operand type(s) for -: 'str' and 'int'"),
        dict(why="no brackets, with the print line taken out: the check names the brackets",
             code=_fuel(FULL_LINE, 'empty = "▯" * robot["max_fuel"] - robot["fuel"]', show="    pass\n"), fails_at=2,
             message_contains="Put brackets around the subtraction"),
        dict(why="the second 0 left", code=_fuel(FULL_LINE), fails_at=2, message_contains="second 0"),
        dict(why="a typed 2 for the light blocks (right for 3 of 5 only)", code=_fuel(FULL_LINE, 'empty = "▯" * 2'),
             fails_at=2, message_contains="not a typed 2"),
        dict(why="Gearshift's max fuel typed in: (6 - robot[\"fuel\"])",
             code=_fuel(FULL_LINE, 'empty = "▯" * (6 - robot["fuel"])'), fails_at=2, message_contains="not a typed 6"),
        dict(why="Gearshift's sheet read for the max fuel (the wrong sheet)",
             code=_fuel(FULL_LINE, 'empty = "▯" * (gearshift["max_fuel"] - robot["fuel"])'), fails_at=2,
             message_contains="not `gearshift`"),
        dict(why="the fuel left for the light blocks", code=_fuel(FULL_LINE, 'empty = "▯" * robot["fuel"]'), fails_at=2,
             message_contains="not the fuel left"),
        dict(why="the max fuel alone for the light blocks", code=_fuel(FULL_LINE, 'empty = "▯" * robot["max_fuel"]'),
             fails_at=2, message_contains="not the max fuel alone"),
        dict(why="the subtraction the wrong way round",
             code=_fuel(FULL_LINE, 'empty = "▯" * (robot["fuel"] - robot["max_fuel"])'), fails_at=2,
             message_contains="Start from the max fuel"),
        dict(why="the bar made but lost (not stored)", code=_fuel(FULL_LINE, EMPTY_LINE, "    get_fuel_bar(robot)\n"),
             fails_at=3, message_contains="made, then lost"),
        dict(why="the function stored, not its result: no ()",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    fuel_bar = get_fuel_bar\n"), fails_at=3,
             message_contains="holds the function itself"),
        dict(why="the call in quotes", code=_fuel(FULL_LINE, EMPTY_LINE, '    fuel_bar = "get_fuel_bar(robot)"\n'),
             fails_at=3, message_contains="Take the quotes off"),
        dict(why="Gearshift handed over instead of robot",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    fuel_bar = get_fuel_bar(gearshift)\n"), fails_at=3,
             message_contains="Hand over `robot`"),
        dict(why="the starter's print line left as it is (printed straight away, never stored)",
             code=_fuel(FULL_LINE, EMPTY_LINE), fails_at=3, message_contains="Store the bar first"),
        dict(why="CP4 not done: stored, never passed", code=FUEL_PARTIALS[2], fails_at=4,
             message_contains="`draw_bar` was not called"),
        dict(why="the store line added under the starter's print line, not in its place (CP3 passes), never passed",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + START_PRINT + "\n    " + STORE_BAR + "\n"), fails_at=4,
             message_contains="`draw_bar` was not called"),
        dict(why="store and pass done, the starter's print line left in (each bar shows twice)",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + START_PRINT + "\n    " + STORE_BAR + "\n    " + PASS_BAR
                        + "\n"), fails_at=4, message_contains="Take out the starter's print line"),
        dict(why="the function handed to draw_bar, not the bar (spec catch; crashes in the bottom loop)",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    draw_bar(robot, get_fuel_bar)\n"),
             fails_at=0, message_contains='(not "function")'),
        dict(why="the values swapped (crashes in the helper)",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    draw_bar(fuel_bar, robot)\n"),
             fails_at=0, message_contains="string indices"),
        dict(why="one value only", code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    draw_bar(robot)\n"),
             fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="the variable's name in quotes",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + '\n    draw_bar(robot, "fuel_bar")\n'),
             fails_at=4, message_contains="Take the quotes off"),
        dict(why="stored, then a typed bar passed instead of the variable",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + '\n    draw_bar(robot, "Fuel [▮▮▮▯▯] 3/5")\n'),
             fails_at=4, message_contains="not typed text"),
        dict(why="stored, then a second call passed instead of the variable",
             code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    draw_bar(robot, get_fuel_bar(robot))\n"),
             fails_at=4, message_contains="not a second call"),
        dict(why="drawn twice", code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR + "\n    " + PASS_BAR + "\n    "
                                            + PASS_BAR + "\n"), fails_at=4, message_contains="once"),
        dict(why="Gearshift drawn every time", code=_fuel(FULL_LINE, EMPTY_LINE, "    " + STORE_BAR
                                                          + "\n    draw_bar(gearshift, fuel_bar)\n"),
             fails_at=4, message_contains="another robot"),
        dict(why="the helper edited to print the bar differently",
             code=FUEL_SOLUTION.replace('robot["name"] + " " + bar', 'robot["name"] + ": " + bar', 1), fails_at=4,
             message_contains="already finished"),
    ],
    notes=(
        meta(starter_level="S4", path="CC", skills="repeat-string,store-then-pass,read-helper", solo="false",
             dictates="1,2,3,4", foreign_names="greeting,get_greeting,dialogue",
             par='Bellows 3/5, Tinplate 1/4, Tinplate 0/4 and 4/4') + "\n"
        "Mk, rehearsal of mana-bars (not campaign mode: 2.10 lists 6C-04, 6C-05, 6P only). Gearshift's starlode gauge. "
        "The numbered comments map one-to-one onto the four checkpoints (rule 13), in the campaign's phrasing: the "
        "first 0, the second 0, store the result, pass it on. The campaign's four checks are all there: CP1 '3 of "
        "5' (full blocks), CP2 '3 of 5' and 'empty and full gauges', CP3 'stored in a variable' (STO), CP4 'draws "
        "once' (CALL, with `draw_bar` swapped for a recorder inside the check) plus KEEP and store-then-pass (the "
        "argument is the stored variable). The robots in the task are 4/6 and 2/7, so the fresh 3/5, 1/4, 0/4 and "
        "4/4 never collide (lint b). Catches (spec): `\"▯\" * a - b` (precedence; the predict and the Example show "
        "it); `draw_bar(robot, get_fuel_bar)` (crashes in the bottom loop: fails at 0 with Python's 'not "
        "\"function\"', the explainer's row; hint 2 names it), plus `fuel_bar = get_fuel_bar` (no `()`), the wrong "
        "sheet, swapped or missing values. PA: per function (the whole program's lines; distractors: the "
        "precedence slip, the function handed over, the swap). TR: tracer. BQ (combining): Lucky's glug gauge with "
        "`▓`, through the same helper (by behavior: a bottom call to `draw_bar` with Lucky's sheet and a stored "
        "bar; a `print` of the bar does not count). The recorder takes keyword values too "
        "(`draw_bar(robot=robot, bar=fuel_bar)` passes). A typed light-block count and the wrong sheet are named "
        "before the value-based messages, which they can look like. Teacher ruling: the starter's `show_fuel` body is "
        "`print(get_fuel_bar(robot))` (comment 3 starts 'Replace this print line:'), so both robots' bars show from "
        "the first Run, never a blank console; the last hint of CP3 says `in place of` that line, so Start me off "
        "replaces it. That print runs `get_fuel_bar` in the bottom loop, so the precedence slip and `\"▮\" * robot` "
        "crash at 0 with Python's TypeError (the predict shows that very error; CP2's first hint names it); the checks "
        "keep their own messages for a `show_fuel` without the print (WAs). CP4 fails while the starter's print line "
        "is still in `show_fuel` (each bar would show twice), after the `draw_bar` checks."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-10 broken-spell-6b (D, SC): four slips, one checkpoint each, in the order Python reports them
# ---------------------------------------------------------------------------------------------

BROKEN_LINE = '    line = hero["name"] + ": " + str(hero["mana"]) + "/" + str(hero["max_mana"])\n'


def _broken6(ret="", store='book["spell_name"] = spell', empty='empty = "░" * hero["max_mana"] - hero["mana"]',
             spend='hero["mana"] = hero["mana"] - 4', status='print("Status: " + mana_line(lucky))',
             read='print(lucky_book["Glow"])'):
    return (
        "def mana_line(hero):\n" + BROKEN_LINE + ret + "\n\n"
        "def add_to_book(book, spell_name, spell):\n    " + store + "\n\n\n"
        "def get_bar(hero):\n"
        '    full = "█" * hero["mana"]\n'
        "    " + empty + "\n"
        "    return full + empty\n\n\n"
        "def spend(hero, cost):\n    " + spend + "\n\n\n"
        + LUCKY_20 + "lucky_book = {}\n"
        + 'glow = {"mana_cost": 2}\n'
        + status + "\n"
        + 'add_to_book(lucky_book, "Glow", glow)\n'
        + read + "\n"
        + "print(get_bar(lucky))\n"
        + "spend(lucky, 4)\n"
        + 'print("Status: " + mana_line(lucky))\n'
    )


FIX_RET = "    return line\n"
FIX_STORE = "book[spell_name] = spell"
FIX_EMPTY = 'empty = "░" * (hero["max_mana"] - hero["mana"])'
FIX_SPEND = 'hero["mana"] = hero["mana"] - cost'
BROKEN6_STARTER = _broken6()
BROKEN6_SOLUTION = _broken6(FIX_RET, FIX_STORE, FIX_EMPTY, FIX_SPEND)

_B6_RET = r"""
_f = _need('mana_line', ['hero'])
_d = _defs()['mana_line']
_e = 'called `mana_line` with a sheet for Pell, mana 7 of 12'
_val, _rows, _err = _call(_f, [{'name': 'Pell', 'mana': 7, 'max_mana': 12}])
assert not _err, _why('mana_line', _err, _e, _FOREIGN)
if _val is None:
    assert not _rows, ('Return the line: `return line`. `print` only shows it, so the call still gets `None`.'
                       + _ev(_e, 'it printed a line but returned `None`'))
    assert False, ('Add `return line` as the last line of `mana_line`. With no `return`, it hands back `None`.'
                   + _ev(_e, 'it returned `None`'))
assert _val == 'Pell: 7/12', ('Return `line`, the line `mana_line` builds, as it is.'
                              + _ev(_e, 'it should return `Pell: 7/12`'))
"""

_B6_STATUS = r"""
assert any(_l.startswith('Status: ') and 'Lucky' in _l for _l in _lines()) and _calls_in(_top(), 'mana_line'), (
    'Keep the Status lines at the bottom: `print("Status: " + mana_line(lucky))`. Mend the function, not the line '
    'that uses it.')
"""

_B6_STORE = r"""
_f = _need('add_to_book', ['book', 'spell_name', 'spell'])
_b = {}
_sp = {'mana_cost': 4}
_val, _rows, _err = _call(_f, [_b, 'Moon Step', _sp])
_e = 'called `add_to_book` with an empty book and the name "Moon Step"'
assert not _err, _why('add_to_book', _err, _e, _FOREIGN)
assert 'spell_name' not in _b, ('Take the quotes off: `book[spell_name] = spell`. With quotes, every spell goes under '
                                'the key "spell_name". ' + _QUOTES + _ev(_e, 'the book got a key "spell_name"'))
assert 'Moon Step' in _b and _b['Moon Step'] == _sp, ('Store the spell under the name handed in: '
                                                      '`book[spell_name] = spell`.' + _ev(_e, 'the book got no '
                                                                                         '"Moon Step"'))
"""

_B6_BAR = r"""
_f = _need('get_bar', ['hero'])
for _s, _who in [({'name': 'Pell', 'mana': 3, 'max_mana': 5}, 'Pell, mana 3 of 5'),
                 ({'name': 'Moth', 'mana': 0, 'max_mana': 2}, 'Moth, mana 0 of 2')]:
    _val, _rows, _err = _call(_f, [_s])
    _e = 'called `get_bar` with a sheet for ' + _who
    assert not _err, _why('get_bar', _err, _e, _FOREIGN)
    _w = '█' * _s['mana'] + '░' * (_s['max_mana'] - _s['mana'])
    if _val == _w:
        continue
    assert type(_val).__name__ == 'str', 'Keep `return full + empty` at the end of `get_bar`.' + _ev(_e)
    assert '░' in _val, ('Keep the light blocks: `empty = "░" * (hero["max_mana"] - hero["mana"])`, and return '
                         '`full + empty`.' + _ev(_e, 'it should return `' + _w + '`'))
    _out = _outer('get_bar')
    assert not _out, ('Read from `hero`, the sheet handed in, not `' + _out[0] + '`, so the bar fits every sheet.'
                      + _ev(_e, 'it should return `' + _w + '`'))
    _tn = [_c.value for _c in _ast.walk(_defs()['get_bar']) if type(_c).__name__ == 'Constant'
           and type(_c.value).__name__ == 'int']
    assert not _tn, ('Work the light blocks out from `hero`: `hero["max_mana"] - hero["mana"]`, in brackets, not a '
                     'typed ' + str(_tn[0]) + '. A typed number only looks right for Lucky.'
                     + _ev(_e, 'it should return `' + _w + '`'))
    assert False, ('Put brackets around the subtraction: `"░" * (hero["max_mana"] - hero["mana"])`.'
                   + _ev(_e, 'it should return `' + _w + '`'))
"""

_B6_SPEND = r"""
_f = _need('spend', ['hero', 'cost'])
_d = _defs()['spend']
_typed = [_c.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'int']
for _s0, _cost, _want, _who in [({'name': 'Pell', 'mana': 11, 'max_mana': 16}, 3, 8, 'Pell, mana 11, and a cost of 3'),
                                ({'name': 'Moth', 'mana': 30, 'max_mana': 31}, 7, 23, 'Moth, mana 30, and a cost of 7')]:
    _s = dict(_s0)
    _val, _rows, _err = _call(_f, [_s, _cost])
    _e = 'called `spend` with a sheet for ' + _who
    assert not _err, _why('spend', _err, _e, _FOREIGN)
    if _s['mana'] == _want:
        continue
    _said = 'the sheet should hold ' + str(_want) + ' after'
    _ty = [_t for _t in _typed if _s['mana'] == _s0['mana'] - _t]
    assert not _ty, ('Use the parameter `cost`, so it works for any cost. `spend` takes away a typed ' + str(_ty[0])
                     + ', which only looks right for `spend(lucky, ' + str(_ty[0]) + ')`.' + _ev(_e, _said))
    _out = _outer('spend')
    assert not _out, ('Change `hero`, the sheet handed in, not `' + _out[0] + '`, so it works for every sheet.'
                      + _ev(_e, _said))
    assert _val != _want, ('Write the new mana into `hero["mana"]`: no `return` is needed. `spend` returns it, and '
                           "the caller's sheet stays as it was." + _ev(_e, 'the sheet did not change'))
    assert _s['mana'] != _s0['mana'], ('Keep the line that writes the new mana into `hero["mana"]`.'
                                       + _ev(_e, 'the sheet did not change'))
    _plain = [_c.value.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Assign'
              and type(_c.value).__name__ == 'Constant']
    assert _s['mana'] not in _plain, ('Work the new mana out from `hero["mana"]` and `cost`, not a typed number.'
                                      + _ev(_e, _said))
    assert False, 'Take `cost` away from `hero["mana"]`: `hero["mana"] = hero["mana"] - cost`.' + _ev(_e, _said)
"""

BROKEN_SPELL_6B = dict(
    id="broken-spell-6b",
    title="Broken spell",
    martu=(
        "Four small functions, four slips. Python reports the loud ones one at a time. Read the last line of each "
        "message first, then go to the line it names. Mend one, run again, and Python shows you the next.\n"
        "The last slip is quiet. No error, and the output even looks right. My checks find it, yes?"
    ),
    names=["mana_line", "add_to_book", "get_bar", "spend", "cost", "spell_name"],
    pair_talk=(
        "Compare which line each message names, and what it says went wrong. Each of you mends your own screen."
    ),
    starter=BROKEN6_STARTER,
    checkpoints=[
        dict(
            id="return-the-line",
            text="Mend `mana_line` so the Status line works.",
            dictated=False,
            hints=[
                "Read Python's last line first. It names `NoneType`: something handed back `None`.",
                "`mana_line` builds `line`, but never returns it. A function with no `return` gives `None`, and text "
                "can't be glued to `None`.",
                "The card: a function needs `return` when the caller needs a value back. "
                "`\"Status: \" + mana_line(lucky)` needs one.",
                "Add `return line` as the last line of `mana_line`, indented.",
            ],
            checks=[
                check("mana_line returns the line", _B6_RET),
                check("the Status line shows", _B6_STATUS),
            ],
        ),
        dict(
            id="store-by-its-name",
            text="Mend `add_to_book` so the spell is stored under its own name.",
            dictated=False,
            hints=[
                "Read Python's last line first. Which key could it not find?",
                "Look at `add_to_book`. Which key does it store the spell under, every time?",
                QUOTES_RULE + " `book[\"spell_name\"]` uses those letters as the key, whatever name is handed in.",
                "Change the line to `" + FIX_STORE + "`.",
            ],
            checks=[check("add_to_book stores the spell under its name", _B6_STORE)],
        ),
        dict(
            id="brackets-first",
            text="Mend the line in `get_bar` that Python names.",
            dictated=False,
            hints=[
                "Read Python's last line first: it tried to take a number away from text.",
                "Python does `*` before `-`, so it makes the light blocks first, then tries to take a number away "
                "from them.",
                "Brackets go first: `\"░\" * (10 - 4)` makes 6 light blocks.",
                "Change the line to `" + FIX_EMPTY + "`.",
            ],
            checks=[check("get_bar returns the bar", _B6_BAR)],
        ),
        dict(
            id="use-the-cost",
            text="Mend `spend` so it works for any cost, not only 4.",
            dictated=False,
            hints=[
                "No error this time, and the output even looks right. Read `spend`: which number does it take away?",
                "`spend(lucky, 4)` hands over 4, so a typed 4 looks right. My checks hand over other costs.",
                "Use the parameter: `cost` holds whatever the call hands over.",
                "Change the line to `" + FIX_SPEND + "`.",
            ],
            checks=[check("spend takes away the cost it is handed", _B6_SPEND)],
            pass_line="Bomb Shell: Four slips. Four mends. That latch hates me. Not this one.",
        ),
    ],
    solution=BROKEN6_SOLUTION,
    another_way=[
        dict(
            angle="step-by-step",
            label="One slip at a time",
            text=(
                "1. Run. Read the last line of the message.\n"
                "2. Go to the line it names. If that line calls a function, the slip may be inside the function.\n"
                "3. Mend it and Run again. A new message? Good: that is the next slip.\n"
                "4. No message? The checks tell you what is left."
            ),
        ),
        dict(
            angle="picture",
            label="Where each slip is",
            text=(
                "```text\nmana_line   no return\nadd_to_book \"spell_name\"\nget_bar     * before -\n"
                "spend       a typed 4\n```\nThe first three are loud. The last one is quiet."
            ),
        ),
        dict(
            angle="shorter",
            text="Return what the caller needs. No quotes on a parameter. Brackets around a subtraction. Use the parameter.",
        ),
        dict(
            angle="try it",
            label="Try another cost",
            text=(
                "Change the bottom call to `spend(lucky, 7)`. Predict the Status line, then Run. Did 7 come off?"
            ),
        ),
        MORE_PRACTICE,
    ],
    takeaway=(
        "Loud slips stop Python; quiet slips only look right. Read the last line, mend one slip, run again, and let "
        "the checks find the quiet one."
    ),
    wrong_answers=[
        dict(why="starter: the missing return (spec: the NoneType TypeError)", code=BROKEN6_STARTER, fails_at=0,
             message_contains='(not "NoneType")'),
        dict(why="return mended; the quoted key shows as a KeyError on the read", code=_broken6(FIX_RET), fails_at=0,
             message_contains="KeyError: 'Glow'"),
        dict(why="two mended; the precedence slip", code=_broken6(FIX_RET, FIX_STORE), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="three mended; the typed 4 is quiet (PAR finds it)", code=_broken6(FIX_RET, FIX_STORE, FIX_EMPTY),
             fails_at=4, message_contains="typed 4"),
        dict(why="the crash 'mended' by dropping \"Status: \" + (None printed, mana_line still returns nothing)",
             code=_broken6(store=FIX_STORE, empty=FIX_EMPTY, spend=FIX_SPEND, status="print(mana_line(lucky))")
             .replace('print("Status: " + mana_line(lucky))', "print(mana_line(lucky))"),
             fails_at=1, message_contains="Add `return line`"),
        dict(why="print(line) inside mana_line, the Status line wrapped in str()",
             code=_broken6("    print(line)\n", FIX_STORE, FIX_EMPTY, FIX_SPEND,
                           status='print("Status: " + str(mana_line(lucky)))')
             .replace('print("Status: " + mana_line(lucky))', 'print("Status: " + str(mana_line(lucky)))'),
             fails_at=1, message_contains="`print` only shows it"),
        dict(why="the KeyError 'mended' by reading the wrong key instead of storing right",
             code=_broken6(FIX_RET, empty=FIX_EMPTY, spend=FIX_SPEND, read='print(lucky_book["spell_name"])'),
             fails_at=2, message_contains='"spell_name"'),
        dict(why="the precedence slip 'mended' by dropping the light blocks",
             code=_broken6(FIX_RET, FIX_STORE, 'empty = ""', FIX_SPEND), fails_at=3, message_contains="light blocks"),
        dict(why="brackets in the wrong place: still text minus a number",
             code=_broken6(FIX_RET, FIX_STORE, 'empty = ("░" * hero["max_mana"]) - hero["mana"]', FIX_SPEND),
             fails_at=0, message_contains="unsupported operand"),
        dict(why="the quiet slip 'mended' by typing the answer", code=_broken6(FIX_RET, FIX_STORE, FIX_EMPTY,
                                                                              'hero["mana"] = 16'),
             fails_at=4, message_contains="not a typed number"),
        dict(why="the precedence slip 'mended' with a typed count of light blocks (right for Lucky only)",
             code=_broken6(FIX_RET, FIX_STORE, 'empty = "░" * 6', FIX_SPEND), fails_at=3, message_contains="typed 6"),
        dict(why="the light blocks read from Lucky's sheet, not hero's (the wrong sheet)",
             code=_broken6(FIX_RET, FIX_STORE, 'empty = "░" * (lucky["max_mana"] - lucky["mana"])', FIX_SPEND),
             fails_at=3, message_contains="not `lucky`"),
        dict(why="spend 'mended' to change lucky, not hero (the wrong sheet)",
             code=_broken6(FIX_RET, FIX_STORE, FIX_EMPTY, 'lucky["mana"] = lucky["mana"] - cost'), fails_at=4,
             message_contains="not `lucky`"),
        dict(why="spend 'mended' to return the new mana (the caller won't see a change it never makes)",
             code=_broken6(FIX_RET, FIX_STORE, FIX_EMPTY, 'return hero["mana"] - cost'), fails_at=4,
             message_contains="no `return` is needed"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="func-takes-dict,none-return,store-by-name,repeat-string,"
             "read-traceback", solo="false", dictates="") + "\n"
        "Broken spell, the spec's four bugs, one checkpoint each, in the order Python reports them: the missing "
        "`return` in `mana_line` (`\"Status: \" + mana_line(lucky)` raises 'can only concatenate str (not "
        "\"NoneType\") to str', the card's payoff), `book[\"spell_name\"]` (seen as `KeyError: 'Glow'` on the read "
        "below it, so the hint sends the student into the function), `\"░\" * a - b` (unsupported operand), and a "
        "literal instead of a parameter: `spend` takes away a typed 4, exactly the bottom call's cost, so the "
        "output looks right and only PAR finds it (the class's biggest slip, made visible). Each mend is checked by "
        "calling the function with invented sheets, so mending the line that uses a function instead of the "
        "function fails (dropping `\"Status: \" +`, reading `lucky_book[\"spell_name\"]`, deleting the light blocks, "
        "typing 16, a typed count of light blocks, Lucky's sheet read for `hero`, a `return` in `spend`). Pell's "
        "max mana is 16 so a typed 4 never lands on 11 by chance. No partials: a crash fails every checkpoint on the site. No Assemble it (debugging)."
    ),
)


# ---------------------------------------------------------------------------------------------
# 6B-S solo-6b (SOLO make-twin, S2, done alone; lean)
# ---------------------------------------------------------------------------------------------

GLUG_LINE = 'hero["mana"] = hero["mana"] + sips'
LUCKY_12 = (
    "lucky = {\n"
    '    "name": "Lucky",\n'
    '    "mana": 12,\n'
    '    "max_mana": 26,\n'
    "}\n"
)


def _solo6(body="    " + GLUG_LINE + "\n"):
    return ("def drink_glug(hero, sips):\n    # Add sips to hero[\"mana\"].\n" + body + "\n\n" + LUCKY_12
            + "drink_glug(lucky, 5)\nprint(lucky[\"mana\"])\n")


SOLO6_STARTER = _solo6("    pass\n")
SOLO6_SOLUTION = _solo6()

# Lean (FORMAT.md, from Unit 2 on): the kind of slip and the line, never the fix.
_SOLO6 = r"""
_f = _need('drink_glug', ['hero', 'sips'])
_d = _defs()['drink_glug']
_out = _outer('drink_glug')
_writes = [_n.lineno for _n in _ast.walk(_d) if type(_n).__name__ in ('Assign', 'AugAssign', 'Return', 'Expr')
           and not (type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Constant')]
_wl = 'Line ' + str(_writes[0] if _writes else 3)
_typed = [_c.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Constant' and type(_c.value).__name__ == 'int']
for _s0, _sips, _want, _who in [({'name': 'Pell', 'mana': 7, 'max_mana': 18}, 3, 10, 'Pell, mana 7, and 3 sips'),
                                ({'name': 'Moth', 'mana': 20, 'max_mana': 33}, 6, 26, 'Moth, mana 20, and 6 sips')]:
    _s = dict(_s0)
    _locs, _val, _rows, _err = _capture(_f, [_s, _sips])
    _e = 'called `drink_glug` with a sheet for ' + _who
    assert not _err, 'Python stopped with a ' + type(_err).__name__ + ' inside `drink_glug`.' + _ev(_e)
    _m = _s.get('mana')
    if _m == _want:
        continue
    _start = _s0['mana']
    _held = 'the sheet that was handed in still held ' + str(_start)
    _near = [_k for _k in _s if _k not in _s0]
    assert not _near, _wl + ' writes a new key, `' + _show(_near[0]) + '`.' + _ev(_e)
    _ti = _typed_if(_d)
    assert not _ti, 'The `if` on line ' + str(_ti[0]) + ' lets only one typed number of sips through.' + _ev(_e)
    _other = [_k for _k in _s if _k != 'mana' and _s[_k] != _s0.get(_k)]
    assert not _other, _wl + ' changes `"' + _other[0] + '"`, not `"mana"`.' + _ev(_e)
    if _m == _start:
        assert not _out, _wl + ' changes `' + _out[0] + '`, not the sheet handed in as `hero`.' + _ev(_e, _held)
        assert _locs.get('hero', _s) is _s, _wl + ' makes a new sheet inside the function.' + _ev(_e, _held)
        assert _val != _want, _wl + ' returns the new mana, and nothing keeps it.' + _ev(_e, _held)
        _box = [_k for _k, _v in _locs.items() if _k not in ('hero', 'sips') and _v == _want]
        assert not _box, (_wl + ' keeps the new mana in a new variable, `' + _box[0] + '`, inside the function.'
                          + _ev(_e, _held))
        assert not _rows, _wl + ' only shows the new mana.' + _ev(_e, _held)
        assert False, 'The sheet that was handed in does not change yet.' + _ev(_e, _held)
    _ty = [_t for _t in _typed if _t != _sips and _m == _start + _t]
    assert not _ty, _wl + ' adds a typed ' + str(_ty[0]) + ', not `sips`.' + _ev(_e)
    _plain = [_c.value.value for _c in _ast.walk(_d) if type(_c).__name__ == 'Assign'
              and type(_c.value).__name__ == 'Constant']
    assert _m not in _plain, _wl + ' stores a typed number.' + _ev(_e)
    assert not _out, _wl + ' reads `' + _out[0] + '`, not `hero`.' + _ev(_e)
    assert _m != _start - _sips, _wl + ' takes the sips away.' + _ev(_e)
    assert _m != _s0['max_mana'] + _sips, _wl + ' starts from the max mana.' + _ev(_e)
    assert _m != _sips, _wl + ' stores just the sips.' + _ev(_e)
    assert not _typed, _wl + ' uses a typed ' + str(_typed[0]) + '.' + _ev(_e)
    assert False, 'The sheet holds ' + str(_m) + ' after. It should hold ' + str(_want) + '.' + _ev(_e)
"""

SOLO_6B = dict(
    id="solo-6b",
    title="Show Mar'tu",
    martu=(
        "A short one, just for you. Lucky's canteen of glug smells terrible and brings mana back. Finish "
        "`drink_glug` so it adds `sips` to the sheet it is handed."
    ),
    solo=True,
    # Teacher ruling (FORMAT.md, from Unit 2 on): every SOLO item is lean.
    explainer="lean",
    names=["drink_glug", "hero", "sips"],
    starter=SOLO6_STARTER,
    checkpoints=[
        dict(
            id="drink-glug",
            text="Finish `drink_glug(hero, sips)` so it adds `sips` to `hero[\"mana\"]`.",
            dictated=False,
            hints=[
                "One line, like `spend`: write into `hero[\"mana\"]`, reading the old mana on the right.",
                "`robot[\"fuel\"] = robot[\"fuel\"] + 2` adds 2 to the sheet the function was handed.",
                "Write `" + GLUG_LINE + "` in place of `pass`.",
            ],
            checks=[check("drink_glug changes the sheet it is handed", _SOLO6)],
            pass_line=(
                "Mar'tu: You did that alone. I saw. On your map: ✓ a function that changes the sheet it is handed."
            ),
        ),
    ],
    solution=SOLO6_SOLUTION,
    another_way=[
        dict(angle="shorter", text="Same sheet in, same sheet changed. Write into it by key; no `return` needed."),
        dict(
            angle="step-by-step",
            text="1. Read `hero[\"mana\"]`. 2. Add `sips`. 3. Write the answer back into `hero[\"mana\"]`.",
        ),
    ],
    takeaway="On your own: a function changes the sheet it is handed, by key: `hero[\"mana\"] = hero[\"mana\"] + sips`.",
    wrong_answers=[
        dict(why="starter: pass", code=SOLO6_STARTER, fails_at=1, message_contains="does not change yet"),
        dict(why="returns the new mana (the caller won't see it)", code=_solo6("    return hero[\"mana\"] + sips\n"),
             fails_at=1, message_contains="nothing keeps it"),
        dict(why="a local variable", code=_solo6("    mana = hero[\"mana\"] + sips\n"), fails_at=1,
             message_contains="new variable, `mana`"),
        dict(why="the bottom call's 5 typed (PAR)", code=_solo6("    hero[\"mana\"] = hero[\"mana\"] + 5\n"),
             fails_at=1, message_contains="typed 5"),
        dict(why="the answer typed: 17", code=_solo6("    hero[\"mana\"] = 17\n"), fails_at=1,
             message_contains="typed number"),
        dict(why="lucky changed instead of hero (the wrong sheet)", code=_solo6("    lucky[\"mana\"] = lucky[\"mana\"] + sips\n"),
             fails_at=1, message_contains="not the sheet handed in"),
        dict(why="takes the sips away", code=_solo6("    hero[\"mana\"] = hero[\"mana\"] - sips\n"), fails_at=1,
             message_contains="takes the sips away"),
        dict(why="a near-miss key", code=_solo6("    hero[\"Mana\"] = hero[\"mana\"] + sips\n"), fails_at=1,
             message_contains='"Mana"'),
        dict(why="a new sheet inside the function", code=_solo6("    hero = {\"mana\": hero[\"mana\"] + sips}\n"),
             fails_at=1, message_contains="new sheet"),
        dict(why="printed, not stored", code=_solo6("    print(hero[\"mana\"] + sips)\n"), fails_at=1,
             message_contains="only shows"),
        dict(why="sips in quotes on the bottom call", code=_solo6().replace("drink_glug(lucky, 5)", 'drink_glug(lucky, "5")'),
             fails_at=0, message_contains="unsupported operand"),
        dict(why="the max mana minus a typed 5 (the old test sheets both gave 10 and 26 this way; fresh sheets now)",
             code=_solo6("    hero[\"mana\"] = hero[\"max_mana\"] - 5\n"), fails_at=1, message_contains="typed 5"),
        dict(why="an if that only adds for the bottom call's typed 5 (if sips == 5)",
             code=_solo6("    if sips == 5:\n        hero[\"mana\"] = hero[\"mana\"] + 5\n"), fails_at=1,
             message_contains="one typed number"),
        dict(why="writes the max mana, not the mana", code=_solo6("    hero[\"max_mana\"] = hero[\"mana\"] + sips\n"),
             fails_at=1, message_contains='changes `"max_mana"`'),
    ],
    notes=(
        meta(starter_level="S2", path="CC", skills="func-takes-dict", solo="true", dictates="",
             foreign_names="robot",
             par='({"name":"Pell","mana":7},3),({"name":"Moth","mana":20},6)') + "\n"
        "SOLO make-twin of 6B-02's `spend`, about 2 minutes, recorded and never blocking. Seat B's `drink_glug(hero, "
        "sips)` (adds the sips) is the exercise, because seat A's `rest(hero)` (mana to max) is printed in 6B-02's "
        "starter and would only show copying. Seat A for a teacher who wants it: "
        "`def rest(hero):` / `hero[\"mana\"] = hero[\"max_mana\"]`, the same check with the max mana as the "
        "answer. CP1 [ND]: PAR with two invented sheets, the caller's dict changing (read from the dict the check "
        "handed over). Lean messages (teacher ruling, FORMAT.md): the kind of slip and the line, never the fix "
        "('Line 3 adds a typed 5, not `sips`.'); explainer='lean'. The class's slips: returned or local "
        "(the caller won't see it), typed values (also an `if sips == 5:`), the wrong sheet, a near-miss key, "
        "another key changed, the sign. The fresh sheets (7 of 18, 20 of 33) leave a different gap to the max "
        "mana, so no single typed number fits both (the old pair let `hero[\"max_mana\"] - 5` pass)."
    ),
)


# =============================================================================================
# Lesson 6B and ITEMS
# =============================================================================================

LESSON_6B = dict(
    kind="lesson",
    id="recipes-read-sheets",
    title="Recipes That Read Stat Sheets",
    minutes=40,
    summary=(
        "Functions that read a hero's sheet, change it, build spells from parameters, guard the door, and call "
        "helpers you didn't write."
    ),
    notes=(
        "Lesson 6B (CC; 6B-10 SC). Preceded by 6b-remembers. Exactly one SOLO (solo-6b, lean). Non-dictated "
        "checkpoints: 6B-01, 6B-02, 6B-04 CP1-2, 6B-05 CP1-2, 6B-10 (all four mends), 6B-S (lint g). Rehearsal: "
        "6B-07 (mana-bars; normal help, not campaign mode). Campaign callbacks: mana-bars (6B-01 get_mana_bar, "
        "6B-06 print_mana, 6B-07 show_mana), spell-book (6B-03 the matching parameters, 6B-04 "
        "spell_book[spell_name] = spell), hold-the-barrier (6B-02 the mana line inside cast_spell, 6B-05 the "
        "opening guard). The card 'When does a function need `return`?' is taught in 6B-02 and paid off in 6B-07 "
        "(get_fuel_bar returns, show_fuel doesn't) and 6B-10 CP1. Minutes: 40 (spec), about 4 per exercise plus "
        "the warm-up; 6B-07 takes about 8."
    ),
    exercises=[HAND_OVER_A_SHEET, RECIPES_CHANGE_SHEETS, MANY_INGREDIENTS, STORE_BY_NAME, GUARD_AT_THE_DOOR,
               READ_THE_HELPER, BAR_THEN_DRAW, BROKEN_SPELL_6B, SOLO_6B],
)

ITEMS = [REMEMBERS_6B, LESSON_6B]
