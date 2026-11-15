"""Unit 9 "Strings" ("Runes and Ribbons"), part a: Mar'tu remembers (8a-remembers), Lesson 8A "Strings Are Rows of
Letters" (8A-01, 8A-03, 8A-06, 8A-07 and the SOLO 8A-S), Mar'tu remembers (8b-remembers), Lesson 8B "Words That
Change Shape" (8B-01, 8B-02, 8B-03, 8B-05, 8B-07, 8B-08, the Broken spell 8B-09 and the SOLO 8B-S) and Quiz 8B.

Spec: design/curriculum.md, "## Unit 9 · Strings", items 1 to 3 (u09a). Introduces exactly what concept_map.json plans
for u09a: const:escape (8A-06), attr:upper and attr:title (8B-01), attr:split and attr:join (8B-03; `int()` is Unit 1's,
call:int, revisited there), attr:strip, attr:replace and attr:find (8B-05), node:FString (8B-07). Everything else comes
from earlier units: `len()`, indexes, `[-1]` and slices (Unit 4), `for` loops (Unit 6), `def` / `return` (Unit 3),
`.lower()` (Unit 2), `.capitalize()` (Unit 3), `str()` and `*` stamps (Unit 1), dictionaries and a function kept in one
(Units 5 and 7, in the 8A warm-up only). No escapes before 8A-06, no `.upper()` / `.title()` before 8B-01, no split /
join before 8B-03, no strip / replace / find before 8B-05 and no f-string before 8B-07, in any code a student sees.
The unit is independent of the Readiness Check (nothing in Unit 10 needs a Strings token): the teacher can run it
before Module 2, alongside it, or after it.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`dialogue_input.lower()` / `.capitalize()` and `option_1.lower().capitalize()` (Module 1, the dialogue parts), and the
mana bar's `"█" * caster["mana"]` with its `+ str(...)` return line (Module 2, mana-bars). Campaign links are "you've
seen this, now you'll get it". Every student has their own device; pair talk is optional and every checkpoint is solo.

Terminology (2.9): "variable" (Mar'tu may still say "box"), "function", "parameter", "argument", "returns" / "hands
back", "method" (new here: an order with a dot). The quotes sentence word for word (QUOTES_RULE).

Help ladder as fields (FORMAT.md, the Unit 2 fix pass, as Units 4 to 7): hints[0] Where to look, the middle hints Teach
me (a tiny example with other names, listed in foreign_names), the last hint Show me how: the step's own line in
backticks, whose start up to its first `(` or `=` is Start me off (always a start Mar'tu's version uses; no hint 1 is a
"Start like this"). 3 to 5 hints per checkpoint, then another_way (2 to 4 angles), assemble (More structure) on every
make / write exercise, and the solution (Compare). In debug steps hints[0] is "Read Python's last line" (for a quiet
bug: what the program printed). Both SOLO items are explainer="lean" with lean check messages (the slip and the
evidence, never the fix). No trace ledger in this part, so no paste_stop guard is needed; no Assemble rung holds a
value a predict asks for (the predicts are one-click choices on their own code).

Check builders (one shared prelude, _PRE, then each check's own body; plain Python run in the student's namespace after
their code, every helper name starting with `_`, builtins taken from `builtins` so a student's `len = 3` cannot break a
check):
  _rerun(values)  CMB / LOOP: the student's program again in a fresh namespace with the FIRST top-level
                `name = <literal>` line of each named variable swapped (another roster, sign, word, report, note...).
                Prints go to a private, capped buffer, and a line budget stops a loop that never ends.
  _call(f, *args) PAR / RET: calls a student function with fresh arguments the task never uses (lint b), prints kept
                private; returns (printed lines, value, error text).
  _first_lit(name) the starter's own value of a variable (read from the code), so a check follows any text the
                student is allowed to change.
  _bare(attr)    a method call standing alone on a line (`line.upper()`): the copy is made, then nothing keeps it.
  _newbox(want)  NEWBOX: another variable holds the right value while the task's variable does not.
  _need_def(name, n)  the function exists, with n parameters (a near-miss name is named).
  _tried(values) / _called(name, args)  the evidence bracket: "(Mar'tu's check tried `sign = "Storeroom, Interior"`,
                only inside the check.)".
  _why(name, err, foreign, lean)  (as Units 3 and 7) every `_call` error path in every function check (8A-07,
                8B-02, 8B-08 and its bonus, 8B-S): "Inside `tidy_line`, Python stopped: <err>." plus one kind
                sentence (an example's name: "`said` comes from Mar'tu's example. The parameter of `tidy_line` is
                `raw`."; a near-miss: "You wrote `curent`. Python matches names letter for letter."; a name used
                before the line that makes it: "Make `said` first, then use it. Python runs a function from the top
                down."), then the evidence bracket. foreign is the exercise meta's foreign_names; lean (8B-S) names
                the unknown name and the parameter, never the fix.
Messages lead with the fix, then say what happened, then the evidence in brackets at the end, about 35 words or fewer
(the teacher's ruling on the Unit 2 reviews). A method with no `()` reads "Add `()` after `.upper`. Without them,
`line` holds the order, not the text. Python runs a method only with `()`." The first `None` message in each lesson
(8A: make_bar's, 8B: tidy_line's) glosses it: "(Python's word for nothing came back)". SOLO messages name the slip
and keep the evidence, with no fix. Check data uses invented Tor names only (Pell, Brakka, Moss, Ivo, Glug, Storeroom, Moon Step, Rust Ward); a student's own
text is never repeated back (8B-08's replies are described, never shown).

The class's slips for this unit, each proven by a wrong_answers entry (in the exercise named):
  * a method called and its result not kept (`line.upper()` alone, then `line` printed unchanged): 8B-01 (bare
    call; `print(line.upper())` with `line` unchanged; a new variable), 8B-02 (two bare steps, then `return raw`),
    8B-05 CP1 (`note.strip()` alone), 8B-08 CP1 (`request.strip()` alone), 8B-09 CP4, 8B-S (the SOLO's bug, in two
    steps: a kept `line = line.strip()`, then `line.lower()` alone, so the student reads which line drops the copy);
    a missing `return` (`None` printed) is Quiz Q8, the def/return item;
  * `lower(line)` as if it were a function: 8B-02 (`capitalize(lower(raw))`), 8B-S (`lower(line)`); `upper(line)`:
    8B-01; `strip(note)`: 8B-05; `split(report)`: 8B-03;
  * a method named with no `()`: 8B-01 (`line = line.upper`), 8B-02 (`return raw.lower`), 8B-09 CP1 (the campaign
    shape `note = note.lower` then `.capitalize()`), 8B-S;
  * changing a letter in place, `word[0] = "G"` (TypeError: 'str' object does not support item assignment): 8A-03
    (the starter), 8A-01 (`initials[0] = ...`), 8A-S (seat B's slip shape);
  * an index off by one, or a slice that misses its end: 8A-01 (`name[1]`, `[0:8]`, `[0:10]`, `[1:9]`, `sign[9]`),
    8A-03 (`word[2:]`, `word[0:]`, `word[1]`), 8B-08 CP2 (`[:2]`, an index past the end of a short split), 8B-09 CP3
    (`parts[3]`, the starter; `parts[1]`), and the 8b-remembers slice distractors;
  * quotes inside quotes without an escape (`"She said "hi""` -> SyntaxError) and a typed newline for `\\n`: 8A-06
    (both, plus `/n` and triple quotes), 8B-08 (`' What's in it for me?'`, an apostrophe inside single quotes);
  * `.split()` hands back a LIST, then treated as text: 8B-03 (`sentences.lower()` on the list, AttributeError;
    `len(report)` for words; `str(words)`), 8B-08 CP2 (a list, or the list written out, handed back);
  * join the wrong way round, `words.join(" ")` (AttributeError): 8B-03 CP4, 8B-08 CP2, 8B-09 CP2, 8B-S (seat B),
    Quiz Q4;
  * `int()` on text that is not digits (`int("48 hrs")`, `int("hours_text")`) -> ValueError, and `"48" + 1`: 8B-03 CP3.
    (Note: `int("7 ")` is NOT a slip: Python's int() ignores spaces at the ends, verified in 3.13. No message calls
    it one.)
  * an f-string without the f (prints `{name}` as it is) or with a brace missing: 8B-07 CP1 (both), CP2 (braces with
    no f);
  * `+` between text and a number without `str()`: 8A-07 (`+ current`), 8B-03 CP3 (`hours_text + 1`), 8B-07 CP2;
  * `.find()` giving -1 read as the last place, and case-sensitive matching: 8B-05 CP3 (`.find("ley")`, `.find` on
    the swapped-out word), CP2 (`.replace("Compass", ...)`); `in` answers True / False, not a place: 8B-05 CP3;
    8B-05's side quest finds the comma with `.find(",")` for any sign (a counted `[0:9]` fails its rerun). The
    case-sensitive `in` ("up" in "SHIELD UP." is False) is 8B-01's side quest (a bonus has no wrong_answers field)
    and u09b's 8A-04 (pool);
  * typing the finished text by hand instead of building it from the values: every CMB / PAR check (8A-01, 8A-03,
    8A-07, 8A-S, 8B-01, 8B-02, 8B-03, 8B-05, 8B-07, 8B-08, 8B-09, 8B-S), each with a typed wrong answer. 8A-07's
    edge bars must be ones `make_bar` handed back (a traced rerun), so a bar glued by hand from pieces fails;
  * the goal skipped by another route, each named kindly ("That prints the right line. This step practices..."):
    8A-06 CP1 with no escape at all (a comma in `print`, the apostrophe glued on, triple quotes), CP2 with one `\\n`
    and a print a gap; 8B-05 CP1 with a counted `[2:-2]` or a `"  "` swap (the other note has 3 spaces in front,
    1 behind); 8B-07 CP2 with `%` or `.format()`; 8B-09 CP1 with line 3 taken out (`.capitalize()` lowers the rest
    anyway), CP2 with `print(*words)` or a loop;
  * the Example's names (NEWBOX): 8A-03 (`spell`), 8B-01 (a new variable), 8B-03 (`items`), 8B-05 (`tag`); and two
    loop slips in 8A-01, the glue line below the loop (not indented) and `initials = ""` repeated inside it.

Phone width: starters, examples, predict code, quiz code and fenced pictures keep to 36 characters a line. One
exception, in editor code only (no fenced prose): 8B-05's solution line `note = note.replace("compass", "Ley Clock")`
(43 characters), kept whole because one call split over two lines reads as two steps to this class. campaign_link
snippets are the campaign's own lines, as in Units 2 to 7.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u09a
"""

import re

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
MODULE_1 = "leylines-awaken"
MODULE_2 = "friends-in-low-places"


def meta(**fields):
    """The curriculum 2.12 rule 14 `meta:` line (first line of an exercise's notes)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


# ---------------------------------------------------------------------------------------------
# Check helpers, put in front of every check (plain Python, run in the student's namespace)
# ---------------------------------------------------------------------------------------------

_PRE = r'''import ast as _ast
import io as _io
import re as _re
import sys as _sys
import builtins as _B
_len, _str, _int, _any, _all, _list, _dict = _B.len, _B.str, _B.int, _B.any, _B.all, _B.list, _B.dict
_QUOTES = __QUOTES__
_SETUP = __SETUP__
def _tn(_v):
    return _B.type(_v).__name__
class _Runaway(BaseException):
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
def _guarded(_fn, _rec=None):
    # A line budget on the student's own lines (main.py), so a loop that never ends inside a check stops.
    # _rec(frame) is called before each top-level line runs (a watched rerun records a variable's history).
    _left = [20000]
    def _tr(_f, _e, _a):
        if _f.f_code.co_filename != 'main.py':
            return None
        if _e == 'line':
            _left[0] -= 1
            if _left[0] < 0:
                raise _Runaway('ran too long')
            if _rec is not None and _f.f_code.co_name == '<module>':
                _rec(_f)
        return _tr
    _old = _sys.gettrace()
    _sys.settrace(_tr)
    try:
        return _fn()
    finally:
        _sys.settrace(_old)
def _parsed():
    return _ast.parse(_source)
def _q(_v):
    if _tn(_v) == 'str':
        return '"' + _v + '"'
    if _tn(_v) in ('list', 'tuple'):
        return '[' + ', '.join([_q(_x) for _x in _v]) + ']'
    return _B.str(_v)
def _tried(_vals):
    return (" (Mar'tu's check tried " + ' and '.join(['`' + _k + ' = ' + _q(_v) + '`' for _k, _v in _vals.items()])
            + ', only inside the check.)')
def _called(_name, _args, _end=''):
    return (" (Mar'tu's check called `" + _name + '(' + ', '.join([_q(_a) for _a in _args]) + ')`, only inside the '
            'check' + (': ' + _end if _end else '') + '.)')
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _rerun(_values, _watch=None):
    # _watch: a name whose every top-level value is kept, in order, in _rerun.hist.
    _t = _parsed()
    _vals = _dict(_values)
    _seen = []
    for _n in _t.body:
        if (_tn(_n) == 'Assign' and _len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id in _vals and _n.targets[0].id not in _seen
                and _tn(_n.value) in ('List', 'Constant', 'Tuple')):
            _n.value = _lit(_vals[_n.targets[0].id], _n.value)
            _seen.append(_n.targets[0].id)
    _ast.fix_missing_locations(_t)
    _ns = {'__name__': '__main__'}
    _hist = []
    _rerun.hist = _hist
    _rec = (lambda _f: _hist.append(_f.f_globals.get(_watch))) if _watch else None
    _out, _buf, _err = _sys.stdout, _Cap(), ''
    _sys.stdout = _buf
    try:
        if _SETUP:
            _B.exec(_B.compile(_SETUP, '<setup>', 'exec'), _ns)
        _code = _B.compile(_t, 'main.py', 'exec')
        _guarded(lambda: _B.exec(_code, _ns), _rec)
    except _Runaway:
        _err = 'it ran too long'
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
    if _watch:
        _hist.append(_ns.get(_watch))
    _rows = [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()]
    return _ns, _rows, _err, [_k for _k in _vals if _k not in _seen]
def _call(_f, *_args):
    _out, _buf, _got, _err = _sys.stdout, _Cap(), None, ''
    _sys.stdout = _buf
    try:
        _got = _guarded(lambda: _f(*_args))
    except _Runaway:
        _err = 'it ran too long'
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
    return [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _got, _err
def _first_lit(_name):
    for _n in _parsed().body:
        if (_tn(_n) == 'Assign' and _len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name'
                and _n.targets[0].id == _name and _tn(_n.value) == 'Constant'):
            return _n.value.value
    return None
def _assigns(_name):
    return [_n for _n in _parsed().body if _tn(_n) == 'Assign'
            and _any(_tn(_x) == 'Name' and _x.id == _name for _x in _n.targets)]
def _is_method(_v):
    return _tn(_v) in ('builtin_function_or_method', 'method', 'method-wrapper')
def _bare(_attr):
    # A method call standing alone on a line: `line.upper()` makes a copy, then nothing keeps it.
    return [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Expr' and _tn(_n.value) == 'Call'
            and _tn(_n.value.func) == 'Attribute' and _n.value.func.attr == _attr]
def _newbox(_want, _skip):
    return [_k for _k, _x in _list(globals().items()) if not _k.startswith('_') and _k not in _skip
            and _tn(_x) == _tn(_want) and _x == _want]
def _fdef(_name):
    _f = [_n for _n in _parsed().body if _tn(_n) == 'FunctionDef' and _n.name == _name]
    return _f[-1] if _f else None
def _need_def(_name, _nparams, _sig):
    _fd = _fdef(_name)
    if _fd is None:
        _near = [_n.name for _n in _parsed().body if _tn(_n) == 'FunctionDef'
                 and _n.name.lower().replace('_', '') == _name.replace('_', '')]
        assert not _near, 'Name the function `' + _name + '`, letter for letter: you wrote `' + _near[0] + '`.'
        assert False, 'Keep the line `' + _sig + '` from the starter.'
    assert _B.callable(globals().get(_name)), (
        'Keep `' + _name + '` a function: a later line put a value in it with `=`.')
    _n = _len(_fd.args.args)
    assert _n == _nparams, ('Keep ' + ('one parameter' if _nparams == 1 else _str(_nparams) + ' parameters') + ' in `'
                            + _name + '`, like `' + _sig + '`. It has ' + _str(_n) + '.')
    return globals()[_name]
def _edits(_a, _b):
    _prev = _list(_B.range(_len(_b) + 1))
    for _i, _x in _B.enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in _B.enumerate(_b, 1):
            _cur.append(_B.min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]
def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    return _q[0] if _len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]
_METHODS = ('lower', 'upper', 'title', 'capitalize', 'strip', 'split', 'join', 'replace', 'find')
def _why(_name, _err, _foreign=(), _lean=False):
    # A kind message for an error raised inside a student function while Mar'tu's check called it (as Units 3 and
    # 7): an example's name, a near-miss of a parameter, a name used before the line that makes it, a method
    # called like a function, and the unit's TypeError / AttributeError rows. _err is _call's 'Kind: text'.
    # _lean (the SOLO): the name and the parameter, never the fix.
    _f = globals().get(_name)
    _ps = _list(_f.__code__.co_varnames[:_f.__code__.co_argcount]) if _tn(_f) == 'function' else []
    _k, _s = _err.split(': ', 1) if ': ' in _err else (_err, '')
    _m = _re.search(r"'(\w+)'", _s)
    _x = _m.group(1) if _m else ''
    _pw = ((('The parameter of `' + _name + '` is ') if _len(_ps) == 1 else ('The parameters of `' + _name + '` are '))
           + _names(_ps) + '.') if _ps else ''
    _say = ''
    if _k == 'UnboundLocalError' and _x:
        _say = (('`' + _x + '` is used before the line that makes it.') if _lean else
                ('Make `' + _x + '` first, then use it. Python runs a function from the top down.'))
    elif _k == 'NameError' and _x:
        _fo = [_y for _y in _foreign if _y == _x]
        _near = [_p for _p in _ps if _len(_x) >= 2 and _edits(_p.lower(), _x.lower()) <= 2]
        _fo2 = [_y for _y in _foreign if _len(_x) >= 3 and _edits(_y, _x) <= 2]
        if _fo:
            _say = '`' + _x + '` comes from ' + ('an example. ' if _lean else "Mar'tu's example. ") + _pw
        elif _near:
            _say = ((('`' + _x + '` is not a parameter of `' + _name + '`. ') if _lean else
                     ('You wrote `' + _x + '`. Python matches names letter for letter. ')) + _pw)
        elif _fo2:
            _say = '`' + _x + '` looks like `' + _fo2[0] + '` from ' + ('an example. ' if _lean else "Mar'tu's example. ") + _pw
        elif _x in _METHODS:
            _say = (('`' + _x + '` is a method, used here like a function.') if _lean else
                    ('`' + _x + '` is a method: it goes after a dot, like `' + (_ps[0] if _ps else 'text') + '.' + _x
                     + '()`.'))
        else:
            _say = '`' + _x + '` is not a name `' + _name + '` knows. ' + _pw
    elif _lean:
        if 'builtin_function_or_method' in _s:
            _say = 'A method is used with no `()`.'
        elif "'list' object has no attribute 'join'" in _s:
            _say = '`.join` is asked of a list.'
    elif _k == 'TypeError':
        if 'NoneType' in _s:
            _say = ("A function it uses hands back `None` (Python's word for nothing came back): give that function a "
                    "`return`.")
        elif 'concatenate' in _s:
            _say = 'Glue a number to text with `str()`, like `str(' + (_ps[0] if _ps else 'n') + ')`.'
        elif 'unsupported operand' in _s and "'str' and 'int'" in _s:
            _say = ('Put brackets around the subtraction, so Python works it out first. Python does `*` before `-`, so '
                    'it made the blocks, then tried to take a number away from text.')
        elif 'does not support item assignment' in _s:
            _say = "Build a new string instead. Text can't change one letter at a time."
        elif 'positional argument' in _s:
            _say = 'Count the values in the brackets against the `def` line: a call hands over the wrong number.'
    elif _k == 'AttributeError':
        if 'builtin_function_or_method' in _s:
            _say = ('Add `()` after the method name. Without them, Python holds the order, not the text. Python runs '
                    'a method only with `()`.')
        elif "'list' object has no attribute 'join'" in _s:
            _say = 'Ask the glue to join: `" ".join(words)`. A list has no `.join`.'
        elif "'list' object" in _s:
            _say = '`.split()` hands back a list. Text methods work on text, not on a list.'
        elif "'NoneType'" in _s:
            _say = ("A function it uses hands back `None` (Python's word for nothing came back): give that function a "
                    "`return`.")
        elif "'str' object" in _s and _x:
            _say = 'Text has no method `.' + _x + '`. Check the name after the dot, letter for letter.'
    elif _k == 'IndexError':
        _say = 'A place past the end stops Python. Count the places from 0.'
    elif _k == 'RecursionError':
        _say = ('Take the spaces off the call inside the function, so it sits at the bottom, outside it. The function '
                'calls itself, again and again.')
    return 'Inside `' + _name + '`, Python stopped: ' + _err + '.' + (' ' + _say if _say else '')
'''


def chk(label, body, setup="", **subs):
    """A check: the shared _PRE (with this exercise's hidden setup), then `body` with each __NAME__ replaced by
    repr(value)."""
    pre = _PRE.replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    left = re.findall(r"__[A-Z][A-Z0-9_]*__", body)
    assert not left, f"unfilled placeholder {left} in {label!r}"
    return (label, pre + body)


# =============================================================================================
# The unit (the same UNIT dict in every Unit 9 part file)
# =============================================================================================

UNIT = dict(
    id="strings",
    order=9,
    title="Strings",
    subtitle="Runes and Ribbons",
    published=True,
    martu_intro=(
        "Runes are only letters in a row. Python sees words the same way. Today we cut them, stretch them, and make "
        "them behave. Lucky, your notes are next.\n"
        "You have seen all of this in the campaign: `.lower().capitalize()` tidying Mar'tu's lines, "
        "`\"█\" * caster[\"mana\"]` in the mana bars, and `+ str(...)` gluing numbers into words. Back then it was "
        "somebody else's code. This time you take text apart and build it again, yourself."
    ),
    goals=[
        "Read one letter with `[0]` or `[-1]`, cut a piece with a [[slice]], and count letters with `len()`",
        "Explain why `word[0] = \"G\"` fails, and build a new string instead",
        "Put quote marks and new lines inside text with `\\\"` and `\\n`",
        "Call string methods like `.upper()`, `.strip()`, `.replace()` and `.find()`, keep what they hand back "
        "(`line = line.lower()`), and chain them",
        "Cut text into a list with `.split()`, glue a list back with `\" \".join(words)`, and turn digits into a "
        "number with `int()`",
        "Write f-strings, and read `+ str()` lines like the campaign's",
        "Build a status bar for any values",
    ],
    campaign_links=[MODULE_1, MODULE_2],
)

# New terms only. Earlier units define string, quotes, glue, str(), stamp, int(), .lower(), .capitalize(), index,
# slice, len(), list, in, TypeError, AttributeError, ValueError, IndexError, SyntaxError, return...
GLOSSARY = [
    dict(
        term="method",
        aliases=["methods", "string method", "string methods"],
        plain=(
            "An order you give a value with a dot, like `line.upper()`. A string method never changes the text. It "
            "hands back a new string, so catch it with `=`."
        ),
        example="line = line.upper()",
    ),
    dict(
        term="immutable",
        aliases=["can't change in place", "cannot change", "unchangeable"],
        plain=(
            "A string can't change one letter at a time: `word[0] = \"G\"` is a TypeError. Build a new string and "
            "put it in the variable instead."
        ),
        example='word = "G" + word[1:]',
    ),
    dict(
        term="escape mark",
        aliases=["escape marks", "escape", "escapes", "backslash", "new line"],
        plain=(
            "A backslash inside text, with one letter after it. `\\\"` puts a quote mark in the text, and `\\n` "
            "starts a new line. The backslash itself never prints."
        ),
        example='print("Gold\\nTeal")',
    ),
    dict(
        term=".upper()",
        aliases=["upper()", "upper"],
        plain="Hands back a copy of the text in capitals. The text in the variable does not change.",
        example='"teal".upper()   # TEAL',
    ),
    dict(
        term=".title()",
        aliases=["title()"],
        plain="Hands back a copy of the text with a capital at the start of every word.",
        example='"bomb shell".title()   # Bomb Shell',
    ),
    dict(
        term="chain",
        aliases=["chains", "chained", "chaining", "method chain"],
        plain=(
            "One method right after another: `raw.lower().capitalize()`. Python works left to right, and each "
            "method works on what the one before it handed back."
        ),
        example="raw.lower().capitalize()",
    ),
    dict(
        term=".split()",
        aliases=["split()", "split"],
        plain=(
            "Cuts text into a list of pieces. With nothing in the brackets it cuts at the spaces. "
            "`.split(\", \")` cuts at each comma and space."
        ),
        example='"Shield up.".split()   # [\'Shield\', \'up.\']',
    ),
    dict(
        term=".join()",
        aliases=["join()", "join"],
        plain=(
            "Glues a list of texts into one text. Ask the glue, not the list: `\" \".join(words)` puts a space "
            "between the words."
        ),
        example='" ".join(["Shield", "up."])',
    ),
    dict(
        term=".strip()",
        aliases=["strip()", "strip"],
        plain="Hands back a copy with the spaces cut off both ends. Spaces between the words stay.",
        example='"  hi  ".strip()   # hi',
    ),
    dict(
        term=".replace()",
        aliases=["replace()"],
        plain=(
            "Hands back a copy with every old piece swapped for a new one: `.replace(old, new)`. It matches every "
            "letter and capital exactly."
        ),
        example='"Rust Ward".replace("Rust", "Moon")',
    ),
    dict(
        term=".find()",
        aliases=["find()"],
        plain=(
            "Hands back the place where some text starts, counted from 0, or -1 when it is not there. Here -1 "
            "means not found. It is not the last letter."
        ),
        example='"EXIT".find("X")   # 1',
    ),
    dict(
        term="f-string",
        aliases=["f-strings", "f string", "f strings"],
        plain=(
            "Text with an `f` right before the quotes. Inside it, `{name}` shows what the variable holds, so no "
            "`+` or `str()` is needed."
        ),
        example='f"{name}: {mana} mana"',
    ),
]

# The party, the chalk wall, and five invented heroes for the LOOP reruns.
ROSTER = ["Oogrish", "Gearshift", "Bomb Shell", "Lucky"]
OTHER_FIVE = ["Pell", "Brakka", "Moss", "Ivo", "Glug"]
EV_FIVE = " (Mar'tu's check tried a roster of 5 other heroes, only inside the check.)"

# =============================================================================================
# Mar'tu remembers… (8a-remembers)
# =============================================================================================

REMEMBERS_8A = dict(
    kind="quiz",
    id="8a-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from earlier units. Nothing is scored.",
    notes=(
        "meta: path=SC; unscored warm-up shown inline before Lesson 8A. Q1 is still the def/return item every "
        "warm-up carries from Unit 4 on, now a stamp and `str()` (the two pieces 8A-07 needs: the campaign's "
        "mana-bar build). The spec's Unit 7 dictionary-call item (`spells[\"glow\"]` versus `spells[\"glow\"](hero)`) "
        "is dropped, for confidence at the unit's start (the teacher's ruling). Q2 is the spec's 1C / 6B precedence "
        "item, recalled on plain numbers, `2 + 3 * 4`, so it never shows SOLO 8A's fix (`\"░\" * (10 - 3)`); the "
        "SOLO checks 'work it out first' honestly. A miss shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="stamp-and-str",
            q="What will this print?",
            code=(
                "def gauge(n):\n"
                '    return "#" * n + " " + str(n)\n'
                "\n"
                "print(gauge(3))\n"
            ),
            choices=["### n", "### 3", "#3 3", "3 3 3 3"],
            answer="### 3",
            explain="The stamp `\"#\" * 3` makes `###`. Then `str(n)` turns 3 into text, so `+` glues it on: `### 3`.",
            notes="Distractors from the class's slips: `### n` (the name read as its letters), `#3 3` (`*` read as "
                  "glue), `3 3 3 3`.",
        ),
        dict(
            type="predict",
            id="times-before-plus",
            q="What will this print?",
            code="print(2 + 3 * 4)\n",
            choices=["20", "24", "14", "9"],
            answer="14",
            explain="`*` goes before `+`: 3 * 4 is 12, then 2 + 12.",
            notes="20: left to right; 24: every number multiplied; 9: every number added.",
        ),
    ],
)

# =============================================================================================
# Lesson 8A "Strings Are Rows of Letters"
# =============================================================================================

# ---- 8A-01 letters-have-places (absorbs 8A-02 slice-a-word) --------------------------------------------------

ROSTER_CODE = 'roster = [\n    "Oogrish",\n    "Gearshift",\n    "Bomb Shell",\n    "Lucky",\n]\n'
SIGN = "Greenroom, Interior"
OTHER_SIGN = "Storeroom, Interior"   # the same length and the same comma place: a counted slice still fits it


def _places(word='word = ""', body="    pass", roster=ROSTER_CODE, tail=""):
    return (
        f'sign = "{SIGN}"\n'
        "# 1. Slice out the word before\n"
        "#    the comma.\n"
        + word + "\n"
        "print(word)\n"
        "\n"
        + roster
        + "# 2. Glue the first letter of each\n"
        "#    name onto initials.\n"
        'initials = ""\n'
        "for name in roster:\n"
        + body + "\n"
        "print(initials)\n"
        + tail
    )


PLACES_STARTER = _places()
INITIALS_LINE = "    initials = initials + name[0]"
WORD_LINE = "word = sign[0:9]"
PLACES_SOLUTION = _places(WORD_LINE, INITIALS_LINE)

INITIALS_CHECK = chk(
    "initials holds the first letter of every name, for any roster",
    r'''
def _letters(_s):
    return ''.join([_c for _c in _s if _c.isalpha()])
def _ok(_s, _names):
    return (_tn(_s) == 'str' and _letters(_s) == ''.join([_n[0] for _n in _names])
            and _all(_c.isalpha() or _c in ' .-' for _c in _s))
_r = globals().get('roster')
assert _tn(_r) == 'list', 'Keep the list `roster` from the starter, with its square brackets.'
assert 'initials' in globals(), 'Keep the line `initials = ""` from the starter, above the loop.'
_v = globals()['initials']
assert _tn(_v) != 'list', ('Keep `initials` as text: start it as `""` and glue each letter on with `+`. A list is a '
                           'different thing.')
assert _tn(_v) == 'str', 'Keep `initials` as text: start it as `""` and glue each letter on with `+`.'
assert _v != '', 'Glue a letter onto `initials` inside the loop, in place of `pass`. `initials` is still empty.'
if not _ok(_v, _r):
    _L = _letters(_v)
    _body = _parsed().body
    _loops = [_i for _i, _n in _B.enumerate(_body) if _tn(_n) == 'For']
    def _sets_initials(_n):
        _t = _n.targets if _tn(_n) == 'Assign' else ([_n.target] if _tn(_n) == 'AugAssign' else [])
        return _any(_tn(_x) == 'Name' and _x.id == 'initials' for _x in _t)
    _below = [_n for _n in _body[(_loops or [_len(_body)])[0] + 1:] if _sets_initials(_n)
              and _any(_tn(_x) == 'Name' and _x.id == 'name' for _x in _ast.walk(_n.value))]
    assert not (_len(_r) > 1 and _L == _r[-1][0] and _below), (
        'Indent the glue line four spaces, so it sits inside the loop and runs for every name. Below the loop, it '
        'ran once, for the last name.')
    _reset = [_n for _i in _loops for _n in _ast.walk(_body[_i]) if _tn(_n) == 'Assign' and _sets_initials(_n)
              and _tn(_n.value) == 'Constant' and _n.value.value == '']
    assert not (_len(_r) > 1 and _L == _r[-1][0] and _reset), (
        'Keep `initials = ""` above the loop only. Inside the loop, it empties `initials` again on every pass, so '
        'only the last letter is left.')
    assert not (_len(_r) > 1 and _L == _r[-1][0]), (
        'Keep the letters from earlier passes: glue onto `initials` with `initials + ...`. It ended with one letter, '
        'from the last name.')
    assert _L != _letters(''.join(_r)), 'Glue on one letter from each name, not the whole name.'
    assert _L != ''.join([_n[1] for _n in _r if _len(_n) > 1]), (
        'Use place 0 for the first letter. Place 1 is the second letter.')
    assert _L != ''.join([_n[-1] for _n in _r]), 'Use place 0 for the first letter. `[-1]` is the last letter.'
    assert not (_len(_r) > 1 and _L == _r[0][0] * _len(_r)), (
        "Read the letter from `name`, this pass's name. Every pass gave the first hero's letter.")
    assert _L != ''.join([_n[0] for _n in _r])[::-1], (
        'Glue each new letter on the end, `initials + ...`, so the letters come in roster order.')
    assert False, 'Make `initials` hold the first letter of each name in `roster`, in order: one letter a name.'
assert _any(_tn(_n) == 'For' for _n in _ast.walk(_parsed())), 'Keep the `for` loop, so every name is reached.'
_ns, _rows, _err, _miss = _rerun({'roster': __FIVE__})
assert not _miss, "Keep the line `roster = [` from the starter, so Mar'tu's check can try other names."
assert not _err, 'Make it work for another roster too. Python stopped: ' + _err + '.' + __EV__
assert _ok(_ns.get('initials'), __FIVE__), (
    'Build `initials` inside the loop, from each `name`, so it follows the roster. With other heroes, it did not.'
    + __EV__)
''',
    FIVE=OTHER_FIVE,
    EV=EV_FIVE,
)

WORD_CHECK = chk(
    "word holds the word before the comma, for another sign too",
    r'''
_s = _first_lit('sign')
assert _tn(_s) == 'str' and ',' in _s, 'Keep the line `sign = "Greenroom, Interior"` from the starter.'
assert 'word' in globals(), 'Keep the line `word = ...` from the starter.'
_w = globals()['word']
assert _tn(_w) == 'str', 'Make `word` a piece of `sign`. A slice of text is text too.'
assert _w != '', 'Slice the word out of `sign` and put it in `word`. `word` is still empty.'
_at = _s.find(',')
if _w != _s[:_at]:
    assert _w != _s[:_at - 1], (
        "Your slice stops one letter early. The end place is left out, so end on the comma's own place.")
    assert _w != _s[:_at + 1], "Your slice takes the comma too. The end place is left out: end on the comma's place."
    assert _w != _s[1:_at], 'Start the slice at place 0. The first letter is place 0, not 1.'
    assert _len(_w) != 1, 'That is one letter. A slice takes a piece, with a colon: `[start:end]`.'
    assert _w.strip() != _s[_at + 1:].strip(), 'That is the word after the comma. This step wants the word before it.'
    assert False, 'Make `word` hold the word before the comma, sliced from `sign`.'
_ns, _rows, _err, _miss = _rerun({'sign': __OTHER__})
assert not _miss, "Keep the line `sign = ...` from the starter, so Mar'tu's check can try another sign."
assert not _err, 'Make it work for another sign too. Python stopped: ' + _err + '.' + _tried({'sign': __OTHER__})
assert _ns.get('word') == __OTHER_WORD__, (
    'Slice `word` out of `sign`, so it follows the sign. With another sign, `word` did not change with it.'
    + _tried({'sign': __OTHER__}))
''',
    OTHER=OTHER_SIGN,
    OTHER_WORD="Storeroom",
)

LETTERS_HAVE_PLACES = dict(
    id="letters-have-places",
    title="Letters have places",
    martu=(
        "A word is letters in a row, like the gaps on the chalk wall. Each letter has a place (a position, as in "
        "lists), counted from 0.\n"
        "```text\n T  e  l  e  g  u  n\n 0  1  2  3  4  5  6\n-7 -6 -5 -4 -3 -2 -1\n```\n"
        "`[0]` is the first letter. `[-1]` is the last. `len()` counts the letters.\n"
        "A [[slice]] cuts out a piece: `[0:4]` takes places 0, 1, 2 and 3. The end place is left out, the same as "
        "with lists. You know these already, yes? Lists taught you. Text works the same way."
    ),
    example=(
        'spell = "Moon Step"\n'
        "print(spell[0])\n"
        "print(spell[-1])\n"
        "print(len(spell))\n"
        "print(spell[0:4])\n"
    ),
    example_output="M\np\n9\nMoon",
    names=["sign", "word", "roster", "name", "initials"],
    predict=dict(
        q="Before you press Run, look at this smaller program. What will it print?",
        code='gun = "Telegun"\nprint(gun[0])\nprint(gun[-1])\nprint(len(gun))\n',
        choices=["T\nn\n7", "e\nn\n7", "T\nu\n7", "T\nn\n6"],
        answer=0,
        explain=(
            "`[0]` is the first letter, T. `[-1]` is the last, n. `len()` counts all 7 letters. The last place is "
            "6, one less than the count, because counting starts at 0."
        ),
    ),
    pair_talk="Before you look at the answer, each of you says what `gun[-1]` shows. Compare, then check.",
    starter=PLACES_STARTER,
    checkpoints=[
        dict(
            id="slice-a-word",
            text="Make `word` hold the word before the comma, sliced from `sign`.",
            dictated=False,
            hints=[
                "The comma's place is how many letters come before it: `Greenroom` has 9.",
                "A slice stops just before its end place:\n```python\ncoat = \"Rust, Ward\"\nprint(coat[0:4])\n```\n"
                "That shows `Rust`. The comma is at place 4, so `[0:4]` stops right before it.",
                "Write `word = sign[0:9]` in place of `word = \"\"`.",
            ],
            checks=[WORD_CHECK],
            pass_line="Mar'tu: Greenroom. Where you four blinked into Tor. Nobody knows why, yes?",
        ),
        dict(
            id="build-initials",
            text="Build `initials` from the first letter of each name in `roster`, inside the loop.",
            dictated=False,
            hints=[
                "Look inside the loop. On each pass, `name` holds one hero's name. Which place holds its first "
                "letter?",
                "Glue onto a text variable each pass, like a running total:\n```python\nmarks = \"\"\n"
                "for jar in [\"salt\", \"oats\"]:\n    marks = marks + jar[-1]\n```\n`marks` ends as `ts`: the "
                "last letter of each word. You want the first.",
                "Write `initials = initials + name[0]` in place of `pass`, with four spaces in front.",
            ],
            checks=[INITIALS_CHECK],
            pass_line="Mar'tu: OGBL. Four heroes, four letters. Python counted, you did not, yes?",
        ),
    ],
    solution=PLACES_SOLUTION,
    partials=[_places(WORD_LINE)],
    assemble=dict(
        lines=[f'sign = "{SIGN}"', WORD_LINE, "print(word)", "roster = [", '    "Oogrish",', '    "Gearshift",',
               '    "Bomb Shell",', '    "Lucky",', "]", 'initials = ""', "for name in roster:", INITIALS_LINE,
               "print(initials)"],
        distractors=["word = sign[0:10]", "    initials = name[0]", "    initials = initials + name[1]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Letters on tiles",
            text=(
                "Picture each letter on a numbered tile, like the gaps on the chalk wall:\n"
                "```text\nM o o n   S t e p\n0 1 2 3 4 5 6 7 8\n```\n"
                "`[0:4]` takes tiles 0, 1, 2 and 3: `Moon`. The space on tile 4 is left out. The end tile is "
                "never taken."
            ),
        ),
        dict(
            angle="step-by-step",
            label="One step at a time",
            text=(
                "1. For the sign, count to the comma, starting at 0.\n"
                "2. Use that place as the end of the slice. The end is left out, so the comma is too.\n"
                "3. In the loop, `name[0]` is this pass's first letter. Glue it on the end of `initials`."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Mar'tu numbers the chalk wall from 0: gap 0, gap 1, gap 2. A word is a wall of letters. Same "
                "counting, same brackets."
            ),
        ),
    ],
    takeaway="Text is letters in a row: `s[0]` is the first, `s[-1]` the last, `s[0:4]` a slice, `len(s)` the count.",
    wrong_answers=[
        dict(why="the starter: word never changes", code=PLACES_STARTER, fails_at=1, message_contains="still empty"),
        dict(why="slice one short: [0:8]", code=_places("word = sign[0:8]"), fails_at=1,
             message_contains="one letter early"),
        dict(why="slice takes the comma: [0:10]", code=_places("word = sign[0:10]"), fails_at=1,
             message_contains="takes the comma"),
        dict(why="slice starts at 1", code=_places("word = sign[1:9]"), fails_at=1, message_contains="place 0"),
        dict(why="one letter, not a slice: sign[9]", code=_places("word = sign[9]"), fails_at=1,
             message_contains="one letter"),
        dict(why="the word after the comma", code=_places("word = sign[10:]"), fails_at=1,
             message_contains="after the comma"),
        dict(why="typed by hand: Greenroom", code=_places('word = "Greenroom"'), fails_at=1,
             message_contains="With another sign"),
        dict(why="round brackets for a slice (SyntaxError)", code=_places("word = sign(0:9)"), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="a comma for the colon (TypeError)", code=_places("word = sign[0, 9]"), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="the slice done, initials never changes (the partial)", code=_places(WORD_LINE), fails_at=2,
             message_contains="still empty"),
        dict(why="no glue: initials = name[0] keeps only the last letter",
             code=_places(WORD_LINE, "    initials = name[0]"), fails_at=2, message_contains="earlier passes"),
        dict(why="the glue line below the loop, not indented: it runs once, on the last name",
             code=_places(WORD_LINE, "    pass\n" + INITIALS_LINE.strip()), fails_at=2,
             message_contains="Indent the glue line"),
        dict(why='initials = "" repeated inside the loop: emptied on every pass',
             code=_places(WORD_LINE, '    initials = ""\n' + INITIALS_LINE), fails_at=2,
             message_contains="above the loop only"),
        dict(why="off by one: name[1] is the second letter", code=_places(WORD_LINE, "    initials = initials + name[1]"),
             fails_at=2, message_contains="Place 1 is the second"),
        dict(why="the last letter, name[-1]", code=_places(WORD_LINE, "    initials = initials + name[-1]"), fails_at=2,
             message_contains="last letter"),
        dict(why="the whole name glued on", code=_places(WORD_LINE, "    initials = initials + name"), fails_at=2,
             message_contains="not the whole name"),
        dict(why="the first hero's letter every pass", code=_places(WORD_LINE, "    initials = initials + roster[0][0]"),
             fails_at=2, message_contains="this pass's name"),
        dict(why="glued on the front: the letters come backwards",
             code=_places(WORD_LINE, "    initials = name[0] + initials"), fails_at=2, message_contains="roster order"),
        dict(why="typed by hand: OGBL, the loop left with pass",
             code=_places(WORD_LINE, "    pass", tail='initials = "OGBL"\n'), fails_at=2,
             message_contains="With other heroes"),
        dict(why="the loop deleted, four letters read by place (a fifth hero is missed)",
             code=_places(WORD_LINE, "    pass",
                          tail="initials = roster[0][0] + roster[1][0] + roster[2][0] + roster[3][0]\n"),
             fails_at=2, message_contains="With other heroes"),
        dict(why="a letter changed in place: initials[0] = name[0] (TypeError)",
             code=_places(WORD_LINE, '    initials = initials + " "\n    initials[0] = name[0]'), fails_at=0,
             message_contains="does not support item assignment"),
        dict(why="a list method on text: initials.append(name[0])",
             code=_places(WORD_LINE, "    initials.append(name[0])"), fails_at=0,
             message_contains="has no attribute 'append'"),
        dict(why="initials made a list", code=_places(WORD_LINE, "    initials = initials + [name[0]]").replace(
            'initials = ""\n', "initials = []\n"), fails_at=2, message_contains="A list is a different thing"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="string-index-slice", solo="false", dictates="",
             foreign_names="spell,gun,marks,jar,coat", stages="P,R,M") + "\n"
        "8A-01 (absorbs 8A-02 slice-a-word). No new tokens: indexes, `[-1]`, slices and `len()` are Unit 4's, the "
        "loop is Unit 6's. Predict 'Telegun'[0], [-1] and len (T, n, 7) on its own code; the starter is the "
        "task. The teacher's order: the one-line slice first, a quick win (its Greenroom pass line is the unit's "
        "first), then the loop. CP1 [ND] slice-a-word: `word` from `sign` (read from its first `sign =` line, so "
        "`sign = sign[0:9]` then `word = sign` passes too), CMB with another sign whose first word has the same "
        "length (Storeroom), so a counted slice `[0:9]` follows it and a typed Greenroom does not (this fixes the "
        "v1 OUT-only check). Off-by-one slices each get their own message; hint 0 counts the letters before the "
        "comma. CP2 [ND] build-initials: `initials` from the roster's names with a loop. Checks: LOOP (a rerun "
        "with 5 invented heroes must give PBMIG, so a typed OGBL or four reads by place fail) and CMB; a dot or "
        "space between the letters (O.G.B.L.) is accepted. Named slips: no glue, place 1, `[-1]`, the whole name, "
        "`roster[0][0]`, the front, a list, `initials[0] =` (item assignment), `.append` on text, the glue line "
        "left below the loop (not indented) and `initials = \"\"` repeated inside it. Partial: the slice done. AW: "
        "picture (letters on numbered tiles, like the chalk wall), step-by-step, in Tor. Pair talk: "
        "predict-and-compare."
    ),
)

# ---- 8A-03 letters-cant-change --------------------------------------------------------------------------------


def _plug(line='word[0] = "G"', head='word = "Plug"', tail=""):
    return "# Lucky's label says Plug.\n# It holds glug, yes?\n" + head + "\n" + line + "\nprint(word)\n" + tail


PLUG_STARTER = _plug()
GLUG_LINE = 'word = "G" + word[1:]'
PLUG_SOLUTION = _plug(GLUG_LINE)

GLUG_CHECK = chk(
    "word holds a new string: G and the rest of the word, for any word",
    r'''
_o = _first_lit('word')
assert _tn(_o) == 'str' and _o, 'Keep the line `word = "Plug"` from the starter, at the top.'
_w = globals().get('word')
_want = 'G' + _o[1:]
if _w != _want:
    assert _tn(_w) == 'str', 'Keep `word` as text: a new string, made from `"G"` and the rest of `word`.'
    assert not (_w == _o and _newbox(_want, ('word',))), (
        'Put the new string back in `word`: start the line with `word = `. Your new variable holds it, but `word` '
        'still holds ' + _o + '.')
    assert not (_w == _o and _want in _lines()), (
        'Keep the new string in `word`: start the line with `word = `. The print showed it, but `word` still holds '
        + _o + '.')
    _lone = [_n for _n in _parsed().body if _tn(_n) == 'Expr' and _tn(_n.value) == 'BinOp']
    assert not (_w == _o and _lone), (
        'Put the new string back in `word`: start the line with `word = `. Python built it, then nothing kept it.')
    assert _w != _o, 'Make `word` hold a new string: `"G"` glued to the rest of the word.'
    assert _w != 'G' + _o[2:], '`word[2:]` skips a letter. The rest of the word starts at place 1.'
    assert _w != 'G' + _o, '`word[0:]` keeps the old first letter too. Start the rest at place 1.'
    assert _w != 'G' + _o[1:2], '`word[1]` is one letter. With a colon, `word[1:]` is the rest of the word.'
    assert False, 'Make `word` hold `"G"` glued to the rest of the word, from place 1 on.'
for _o2, _w2 in (('Drum', 'Grum'), ('Brass', 'Grass')):
    _ns, _rows, _err, _miss = _rerun({'word': _o2})
    assert not _miss, "Keep the line `word = \"Plug\"` from the starter, so Mar'tu's check can try another word."
    assert not _err, 'Make it work for another word too. Python stopped: ' + _err + '.' + _tried({'word': _o2})
    assert _ns.get('word') == _w2, (
        'Build the new word from `word` itself, so it follows. With another word, it should become ' + _w2 + '.'
        + _tried({'word': _o2}))
''',
)

LETTERS_CANT_CHANGE = dict(
    id="letters-cant-change",
    title="Letters can't change",
    martu=(
        "Lucky labeled his canteen. The label says `Plug`. It should say `Glug`. One letter, yes? Easy.\n"
        "Not in Python. A list lets you swap an item. Text does not. A string is [[immutable]]: it can't change in "
        "place. `word[0] = \"G\"` makes Python stop with a TypeError.\n"
        "So build a new string, and put it in the variable. `word[1:]` is the rest of the word, from place 1 to the "
        "end. Glue a new first letter onto it."
    ),
    example='spell = "Moon Step"\nspell = "N" + spell[1:]\nprint(spell)\n',
    example_output="Noon Step",
    names=["word"],
    starter=PLUG_STARTER,
    checkpoints=[
        dict(
            id="build-a-new-word",
            text="Mend line 4 so `word` holds `Glug`, built from `\"G\"` and the rest of `word`.",
            dictated=False,
            hints=[
                "Read Python's last line: `TypeError: 'str' object does not support item assignment`. Text can't "
                "change one letter at a time.",
                "Make a new string instead, and put it in `word` with `=`: the new letter, glued to `word[1:]`, the "
                "rest of the word.",
                "With other names:\n```python\ncoat = \"Bust\"\ncoat = \"R\" + coat[1:]\n```\n`coat` now holds "
                "`Rust`. The old text was never changed. A new one took its place.",
                "Write `" + GLUG_LINE + "` in place of line 4.",
            ],
            checks=[GLUG_CHECK],
            pass_line="Lucky: Glug. Better. I'm still keeping the canteen.",
        ),
    ],
    solution=PLUG_SOLUTION,
    assemble=dict(
        lines=['word = "Plug"', GLUG_LINE, "print(word)"],
        distractors=['word[0] = "G"', 'word = "G" + word[2:]', 'word = "Glug"'],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="A painted sign",
            text=(
                "A word is like a sign painted on a board. You can't peel off one letter. You paint a new board, "
                "copy the letters you want, and hang it in the old one's place."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `word[1:]` copies `lug`, the rest of the word.\n2. `\"G\" + ...` glues a G in front: `Glug`.\n"
                "3. `word = ...` hangs the new string in the variable. The old `Plug` is simply gone."
            ),
        ),
        dict(
            angle="why",
            label="Why can't text change?",
            text=(
                "Python keeps each string sealed, so it never changes behind your back. Every change you see is a "
                "new string put in the variable. That is why methods like `.lower()` hand back a copy: you meet "
                "them in Lesson 8B."
            ),
        ),
    ],
    takeaway="A string can't change in place. Build a new one: `word = \"G\" + word[1:]`.",
    wrong_answers=[
        dict(why="the starter: a letter changed in place (TypeError)", code=PLUG_STARTER, fails_at=0,
             message_contains="does not support item assignment"),
        dict(why="typed by hand: Glug", code=_plug('word = "Glug"'), fails_at=1, message_contains="should become Grum"),
        dict(why="off by one: word[2:] skips a letter", code=_plug('word = "G" + word[2:]'), fails_at=1,
             message_contains="skips a letter"),
        dict(why="word[0:] keeps the old first letter", code=_plug('word = "G" + word[0:]'), fails_at=1,
             message_contains="old first letter"),
        dict(why="word[1] is one letter, not the rest", code=_plug('word = "G" + word[1]'), fails_at=1,
             message_contains="one letter"),
        dict(why="built, then nothing kept it (a bare expression)", code=_plug('"G" + word[1:]'), fails_at=1,
             message_contains="nothing kept it"),
        dict(why="a new variable holds it, word still Plug", code=_plug('new_word = "G" + word[1:]'), fails_at=1,
             message_contains="new variable"),
        dict(why="printed, never stored", code=_plug('print("G" + word[1:])'), fails_at=1,
             message_contains="The print showed it"),
        dict(why="a counted end that fits four letters only: word[-3:]", code=_plug('word = "G" + word[-3:]'),
             fails_at=1, message_contains="should become Grass"),
        dict(why="a swap that only knows the P", code=_plug('word = word.replace("P", "G")'), fails_at=1,
             message_contains="should become Grum"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="string-immutable", solo="false", dictates="",
             foreign_names="spell,coat", stages="D,M") + "\n"
        "8A-03. No new tokens. The starter is the spec's explainer row: `word[0] = \"G\"` raises "
        "\"TypeError: 'str' object does not support item assignment\" (verified, Python 3.13). The spec's letter C "
        "became G (Plug -> Glug, Lucky's canteen) because an off-by-one slice of a -lock word gives an unsafe word; "
        "the reruns use Drum -> Grum and Brass -> Grass (two lengths, so a counted `[-3:]` fails). CP1 [ND]: build "
        "`\"G\" + word[1:]` (CMB). Named slips: `[2:]`, `[0:]`, `[1]`, built but not kept (a bare expression, a "
        "print, a new variable: NEWBOX), typed Glug. WT: immutability (the 'why' angle and the [[immutable]] "
        "glossary entry)."
    ),
)

# ---- 8A-06 escape-marks -------------------------------------------------------------------------------------------

QUOTE_COMMENT = "# 1. Print it, quotes and all:\n# Mar'tu: \"NOT a compass.\"\n"
WALL_COMMENT = "# 2. Print the chalk wall in ONE\n#    print, one gap a line:\n# 48 48 47 46 44 41 37\n"
QUOTE_LINE = 'print("Mar\'tu: \\"NOT a compass.\\"")'
WALL_PRINT = 'print("48\\n48\\n47\\n46\\n44\\n41\\n37")'


def _escape(quote='print("")', wall='print("")'):
    # Each step has a `print("")` line in the starter to edit (the teacher's ruling).
    return (QUOTE_COMMENT + (quote + "\n" if quote else "") + "\n" + WALL_COMMENT + (wall + "\n" if wall else ""))


ESCAPE_STARTER = _escape()
ESCAPE_SOLUTION = _escape(QUOTE_LINE, WALL_PRINT)

QUOTE_CHECK = chk(
    "Mar'tu's line prints exactly, inner quotes and all",
    r'''
_want = 'Mar\'tu: "NOT a compass."'
_rows = _lines()
if _want not in _rows:
    def _flat(_l):
        return ' '.join(_l.lower().replace('"', '').replace("'", '').replace('\\', '').split()).rstrip('.')
    _near = [_l for _l in _rows if _flat(_l) == _flat(_want)]
    assert _near, 'Print Mar\'tu\'s line exactly: `Mar\'tu: "NOT a compass."`, quotes and all.'
    _l = _near[0]
    assert '\\' not in _l, (
        'Write each inner quote as `\\"`: one backslash, right before the quote mark. A backslash printed as it is.')
    assert "'NOT" not in _l, 'Use double quote marks around the words, each written `\\"`. These are single ones.'
    assert '"' in _l, 'Keep the quote marks around Mar\'tu\'s words. Inside the text, write each one as `\\"`.'
    assert _l.count('"') == 2, 'Put one quote mark before `NOT` and one after the full stop, each written as `\\"`.'
    assert False, 'Check every letter, space and capital: NOT is in capitals, and the full stop sits inside the quotes.'
_esc_q = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str'
          and ('"' in _n.value or "'" in _n.value) and '\\' in (_ast.get_source_segment(_source, _n) or '')]
assert _esc_q, (
    'That prints the right line. This step practices the escape mark: inside ordinary double quotes, write each '
    'inner quote mark as `\\"`.')
''',
)

WALL_CHECK = chk(
    "the seven gaps print one a line, from one string with \\n",
    r'''
_gaps = ['48', '48', '47', '46', '44', '41', '37']
_raw = [_l.strip() for _l in _captured_stdout.split('\n')]
_hit = _any(_raw[_i:_i + 7] == _gaps for _i in _B.range(_len(_raw)))
_rows = _lines()
if not _hit:
    assert not _any('/n' in _l for _l in _rows), (
        'Use a backslash, `\\`, not the slash `/`: `\\n`. `/n` is a slash and an n, two plain letters, so they printed '
        'as they are.')
    assert not _any('\\n' in _l for _l in _rows), (
        'Write `\\n` inside ordinary quotes, with one backslash. It printed as two letters.')
    assert not _any('48 48' in _l or '48, 48' in _l or '4848' in _l for _l in _rows), (
        'Put `\\n` between the gaps, so each one starts a new line. They all printed on one line.')
    assert False, 'Print all seven gaps, in order, one a line: 48, 48, 47, 46, 44, 41, 37.'
_strs = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str' and '\n' in _n.value]
_esc = [_n for _n in _strs if '\\n' in (_ast.get_source_segment(_source, _n) or '')]
assert _esc or not _strs, (
    'Triple quotes keep a typed new line, so that works too. This step practices `\\n`: write the gaps on one line, '
    'with `\\n` between them.')
assert _esc, 'Use one `print` for all seven gaps: put `\\n` between them, inside one string.'
_nl = _B.sum([_n.value.count('\n') for _n in _esc])
_glue = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
         and _n.func.attr == 'join' and _tn(_n.func.value) == 'Constant' and _n.func.value.value == '\n']
assert _nl >= 6 or _glue, (
    'Put all seven gaps in one `print`, with `\\n` between each pair: six of them. Some gaps still have a `print` '
    'of their own.')
''',
)

ESCAPE_MARKS = dict(
    id="escape-marks",
    title="Escape marks",
    martu=(
        "Text starts and ends with a quote mark. So how do you put a quote mark *inside* text, without ending it?\n"
        "With an [[escape mark]]: a backslash, `\\`, and one letter after it.\n"
        "1. `\\\"` means: this quote mark is part of the text.\n"
        "2. `\\n` means: start a new line here.\n"
        "The backslash never prints. Python reads it as an order, not a letter.\n"
        "Try it after the steps: take one backslash away and press Run. Read Python's last line."
    ),
    introduces=["const:escape"],
    example='print("Oogrish: \\"Steady, now.\\"")\nprint("Gold\\nTeal")\n',
    example_output='Oogrish: "Steady, now."\nGold\nTeal',
    predict=dict(
        q="Before you press Run, look at this program. What will it print?",
        code='print("Bomb Shell: \\"Shield up.\\"")\nprint("Latch\\nstuck.")\n',
        choices=[
            'Bomb Shell: "Shield up."\nLatch\nstuck.',
            'Bomb Shell: \\"Shield up.\\"\nLatch\\nstuck.',
            'Bomb Shell: "Shield up."\nLatch stuck.',
            "Bomb Shell: Shield up.\nLatch\nstuck.",
        ],
        answer=0,
        explain=(
            "Each `\\\"` prints as a plain quote mark, and the backslash vanishes. `\\n` prints nothing you can see: "
            "it starts a new line, so `stuck.` goes on the next one."
        ),
    ),
    starter=ESCAPE_STARTER,
    checkpoints=[
        dict(
            id="quote-inside-quotes",
            text="Print `Mar'tu: \"NOT a compass.\"` exactly, using `\\\"` for the quote marks inside.",
            dictated=True,
            hints=[
                "Count the quote marks. The first `\"` inside the text would end it early. Each inner quote needs a "
                "backslash right in front of it.",
                "With other words:\n```python\nprint(\"Gearshift: \\\"Holding.\\\"\")\n```\nThat shows "
                "`Gearshift: \"Holding.\"`. The outer quotes start and end the text. Each `\\\"` is a quote inside it.",
                "The apostrophe in `Mar'tu` is fine inside double quotes. Only the double quote marks need a backslash.",
                "Write `" + QUOTE_LINE + "` in place of the `print(\"\")` under comment 1.",
            ],
            checks=[QUOTE_CHECK],
            pass_line="Mar'tu: Yes. Once again, it is not a compass.",
        ),
        dict(
            id="wall-on-new-lines",
            text="Print the chalk wall's seven gaps, one a line, with one `print` and `\\n` between the gaps.",
            dictated=False,
            hints=[
                "One `print`, one string. Wherever one gap ends and the next begins, put `\\n`.",
                "```python\nprint(\"gold\\nteal\\nsilver\")\n```\nThat prints three lines: `gold`, `teal`, `silver`. "
                "No spaces around `\\n`, or they print too.",
                "Write `" + WALL_PRINT + "` in place of the `print(\"\")` under comment 2.",
            ],
            checks=[WALL_CHECK],
            pass_line="Mar'tu: Seven gaps, one print. The decay reads the same down the page, yes?",
        ),
    ],
    solution=ESCAPE_SOLUTION,
    partials=[_escape(QUOTE_LINE)],
    assemble=dict(
        lines=[QUOTE_LINE, WALL_PRINT],
        distractors=[
            'print("Mar\'tu: "NOT a compass."")',
            'print("48/n48/n47/n46/n44/n41/n37")',
            'print("48 48 47 46 44 41 37")',
        ],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Where the text ends",
            text=(
                "```text\n\"Mar'tu: \"NOT a ...\n^        ^\nstart     Python thinks\n          the text ends\n```\n"
                "A backslash in front, `\\\"`, tells Python: not the end, just a quote mark."
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "In a story, a speaker's words sit inside quote marks. A backslash is like whispering to Python: "
                "\"this one is part of the story, keep reading\"."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Write the outer quotes: `print(\"\")`.\n2. Type the words inside.\n3. Wherever a `\"` belongs "
                "inside, type `\\\"`.\n4. Wherever a new line belongs, type `\\n`."
            ),
        ),
    ],
    takeaway="`\\\"` puts a quote mark inside text, and `\\n` starts a new line. The backslash never prints.",
    wrong_answers=[
        dict(why="the starter prints nothing", code=ESCAPE_STARTER, fails_at=1, message_contains="quotes and all"),
        dict(why="inner quotes with no backslash (SyntaxError)",
             code=_escape('print("Mar\'tu: "NOT a compass."")', WALL_PRINT), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="single outer quotes: the apostrophe in Mar'tu ends the text",
             code=_escape("print('Mar'tu: \"NOT a compass.\"')", WALL_PRINT), fails_at=0,
             message_contains="unterminated string literal"),
        dict(why="the inner quotes left out", code=_escape('print("Mar\'tu: NOT a compass.")', WALL_PRINT),
             fails_at=1, message_contains="Keep the quote marks"),
        dict(why="single quote marks inside", code=_escape('print("Mar\'tu: \'NOT a compass.\'")', WALL_PRINT),
             fails_at=1, message_contains="single ones"),
        dict(why="not in small letters", code=_escape('print("Mar\'tu: \\"not a compass.\\"")', WALL_PRINT),
             fails_at=1, message_contains="capitals"),
        dict(why="the backslash doubled: the quote mark ends the text (SyntaxError)", code=_escape('print("Mar\'tu: \\\\"NOT a compass.\\\\"")'),
             fails_at=0, message_contains="invalid syntax"),
        dict(why="seven prints, no \\n", code=_escape(QUOTE_LINE, "\n".join(f'print("{g}")' for g in
                                                                          [48, 48, 47, 46, 44, 41, 37])),
             fails_at=2, message_contains="one `print`"),
        dict(why="a typed new line inside ordinary quotes (SyntaxError)", code=_escape(QUOTE_LINE, 'print("48\n48")'),
             fails_at=0, message_contains="unterminated string literal"),
        dict(why="/n for \\n: the slash leans the wrong way", code=_escape(QUOTE_LINE, 'print("48/n48/n47/n46/n44/n41/n37")'),
             fails_at=2, message_contains="not the slash"),
        dict(why="spaces, not new lines", code=_escape(QUOTE_LINE, 'print("48 48 47 46 44 41 37")'), fails_at=2,
             message_contains="one line"),
        dict(why="a gap missing", code=_escape(QUOTE_LINE, 'print("48\\n47\\n46\\n44\\n41\\n37")'), fails_at=2,
             message_contains="all seven gaps"),
        dict(why="triple quotes with typed new lines (works, but not the escape mark)",
             code=_escape(QUOTE_LINE, 'print("""48\n48\n47\n46\n44\n41\n37""")'), fails_at=2,
             message_contains="Triple quotes"),
        dict(why="no escape at all: a comma in print puts the quoted words beside the name",
             code=_escape('print("Mar\'tu:", \'"NOT a compass."\')', WALL_PRINT), fails_at=1,
             message_contains="practices the escape mark"),
        dict(why="no escape at all: the apostrophe glued on in its own quotes",
             code=_escape('print(\'Mar\' + "\'" + \'tu: "NOT a compass."\')', WALL_PRINT), fails_at=1,
             message_contains="practices the escape mark"),
        dict(why="triple quotes around the line: no escape needed, so none practiced",
             code=_escape("print('''Mar'tu: \"NOT a compass.\"''')", WALL_PRINT), fails_at=1,
             message_contains="practices the escape mark"),
        dict(why="one \\n, then a print for each other gap",
             code=_escape(QUOTE_LINE, 'print("48\\n48")\n' + "\n".join(f'print("{g}")' for g in [47, 46, 44, 41, 37])),
             fails_at=2, message_contains="six of them"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="escape-chars", solo="false", dictates="1",
             foreign_names="", stages="P,I,M") + "\n"
        "8A-06. Intro const:escape. The spec's line `Mar'tu said, \"It is not a compass.\"` (46 characters in a "
        "print) became `Mar'tu: \"NOT a compass.\"` (35 in its print) for the phone width; the capital NOT is the "
        "brief's own. The starter has a `print(\"\")` under each comment, so each step has a line to edit (it "
        "prints blank lines and fails at CP1; the wall check finds the 7-line window anywhere in the output). CP1 "
        "[D] with `\\\"`: any way that prints the exact line passes (an escaped apostrophe in single quotes too); "
        "near lines are named (no inner quotes, single ones, capitals), and a line printed with no escape at all (a "
        "comma in `print`, the apostrophe glued on in its own quotes, triple quotes) is told kindly that this step "
        "practices `\\\"`. CP2 [ND]: the wall with `\\n` in one string "
        "(the source segment must hold a real `\\n`, six of them for seven gaps, or a `\"\\n\".join`); seven prints, one `\\n` "
        "then a print a gap, triple quotes with typed new lines, `/n`, spaces "
        "and a missing gap each get a message. The investigate step ('take one backslash away and press Run') sits "
        "in the Learn pane. Formatting is off for the course (architecture 4.7), so quotes stay as typed: the editor "
        "never swaps them for curly ones. Python 3.13 messages verified: no backslashes -> 'invalid syntax. Perhaps "
        "you forgot a comma?'; single outer quotes -> 'unterminated string literal'; a typed new line -> "
        "'unterminated string literal'."
    ),
)

# ---- 8A-07 bars-one-more-time ----------------------------------------------------------------------------------

BAR_HEAD = 'def make_bar(current, maximum):\n    full = "▓"\n    empty = "░"\n'
BAR_COMMENT = "    # Hand back a bar like this one,\n    # for any numbers:\n    # Glug [▓▓░] 2/3\n"
# Step 1: the blocks. Step 2: the label and the numbers, glued on in place of the first `return bar`.
BLOCKS_BODY = (
    "    used = maximum - current\n"
    "    bar = full * current\n"
    "    bar = bar + empty * used\n"
)
LABEL_BODY = (
    '    bar = "Glug [" + bar + "] "\n'
    '    bar = bar + str(current) + "/"\n'
    "    bar = bar + str(maximum)\n"
)
BAR_RETURN = "    return bar\n"
BAR_BODY = BLOCKS_BODY + LABEL_BODY + BAR_RETURN
BAR_CALLS = "print(make_bar(2, 3))\nprint(make_bar(1, 4))\n"
BAR_EDGES = "print(make_bar(0, 3))\nprint(make_bar(3, 3))\n"
BAR_FOREIGN = "fuel_bar,left,tank,gone,meter"
FUEL_BAR = (
    "def fuel_bar(left, tank):\n"
    "    gone = tank - left\n"
    '    meter = "#" * left\n'
    '    meter = meter + "." * gone\n'
    '    meter = meter + " " + str(left)\n'
    '    return "Fuel " + meter\n'
    "\n"
)


def _bar(body=BAR_BODY, calls=BAR_CALLS, edges="", comment=True):
    return BAR_HEAD + (BAR_COMMENT if comment else "") + body + "\n\n" + calls + edges


BAR_STARTER = _bar("    pass\n")
BAR_SOLUTION = _bar(BAR_BODY, edges=BAR_EDGES, comment=False)

_BAR_FN = r'''
def _want_bar(_c, _m):
    return 'Glug [' + '▓' * _c + '░' * (_m - _c) + '] ' + _str(_c) + '/' + _str(_m)
'''

BLOCKS_CHECK = chk(
    "make_bar hands back the blocks for fresh numbers: a full one for each sip left, then the empty ones",
    r'''
_f = _need_def('make_bar', 2, 'def make_bar(current, maximum):')
_res = []
for _c, _m in ((3, 5), (6, 9)):
    _p, _v, _e = _call(_f, _c, _m)
    _ev = _called('make_bar', (_c, _m), 'its blocks should be `' + '▓' * _c + '░' * (_m - _c) + '`')
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _ev
    assert not (_v is None and _p), (
        "Hand back the blocks with `return`, not `print`. `make_bar` printed them, then handed back `None` "
        "(Python's word for nothing came back)." + _ev)
    assert _v is not None, (
        "End `make_bar` with `return`, so it hands back the blocks. It handed back `None` (Python's word for "
        "nothing came back)." + _ev)
    assert _tn(_v) == 'str', 'Hand back the blocks as text: stamp them with `*` and glue them with `+`.' + _ev
    _res.append((_c, _m, _v, _ev))
assert _res[0][2] != _res[1][2], (
    'Build the blocks from `current` and `maximum`, so they change with them. (Mar\'tu\'s check called '
    '`make_bar(3, 5)` and `make_bar(6, 9)`, only inside the check: both handed back the same text.)')
for _c, _m, _v, _ev in _res:
    # Only the blocks count here, so a bar that is finished (step 2) still passes step 1.
    if ''.join([_x for _x in _v if _x in '▓░']) == '▓' * _c + '░' * (_m - _c):
        continue
    assert '█' not in _v, 'Use `full` and `empty` from the starter, `▓` and `░`. The bar used `█`.' + _ev
    _nf, _ne = _v.count('▓'), _v.count('░')
    assert _nf == _c, ('Stamp `full` once for each sip left: `full * current`. The bar had ' + _str(_nf)
                       + ' of them, not ' + _str(_c) + '.' + _ev)
    assert _ne == _m - _c, ('Stamp `empty` once for each sip gone, `maximum - current` times. The bar had '
                            + _str(_ne) + ' of them, not ' + _str(_m - _c) + '.' + _ev)
    assert False, 'Put the full blocks first, then the empty ones, like `▓▓░`.' + _ev
''',
    FOREIGN=BAR_FOREIGN.split(","),
)

BAR_CHECK = chk(
    "make_bar hands back the glug bar for fresh numbers",
    _BAR_FN + r'''
_f = _need_def('make_bar', 2, 'def make_bar(current, maximum):')
_res = []
for _c, _m in ((3, 5), (6, 9)):
    _p, _v, _e = _call(_f, _c, _m)
    _ev = _called('make_bar', (_c, _m), 'it should hand back `' + _want_bar(_c, _m) + '`')
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _ev
    assert not (_v is None and _p), (
        'Hand back the bar with `return`, not `print`. `make_bar` printed it, then handed back `None`.' + _ev)
    assert _v is not None, 'End `make_bar` with `return`, so it hands back the bar. It handed back `None`.' + _ev
    assert _tn(_v) == 'str', 'Hand back the bar as text, glued together with `+`.' + _ev
    _res.append((_c, _m, _v, _ev))
for _c, _m, _v, _ev in _res:
    if _v == _want_bar(_c, _m):
        continue
    assert _v != '▓' * _c + '░' * (_m - _c), (
        'Glue `"Glug ["` on the front, then `"] "` and the numbers on the end, like `Glug [▓▓░] 2/3`. `make_bar` '
        'handed back just the blocks.' + _ev)
    assert _v.endswith(_str(_c) + '/' + _str(_m)), (
        'End with the numbers, sips left first, like `2/3`. Make each one text with `str()`.' + _ev)
    assert _v.startswith('Glug ['), 'Start the bar with `Glug [`, like `Glug [▓▓░] 2/3`.' + _ev
    assert False, 'Check the brackets and spaces: one space after `Glug`, one after `]`, like `Glug [▓▓░] 2/3`.' + _ev
''',
    FOREIGN=BAR_FOREIGN.split(","),
)

BAR_EDGE_CHECK = chk(
    "an empty bar and a full bar are printed, made by make_bar",
    _BAR_FN + r'''
import re as _re
_f = globals().get('make_bar')
for _c, _m in ((0, 5), (4, 4)):
    _p, _v, _e = _call(_f, _c, _m)
    _ev = _called('make_bar', (_c, _m), 'it should hand back `' + _want_bar(_c, _m) + '`')
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _ev
    assert _v == _want_bar(_c, _m), 'Make `make_bar` work for an empty canteen and a full one too.' + _ev
_typed = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str'
          and _re.search(r'\d\s*/\s*\d', _n.value)]
assert not _typed, (
    'Print bars that `make_bar` builds, with `print(make_bar(...))`. A bar typed in quotes does not come from the '
    'function.')
# Run the program again, keeping every bar that make_bar hands back, so a bar glued outside it is told apart.
_made, _left = [], [20000]
def _tr2(_fr, _e, _a):
    if _fr.f_code.co_filename != 'main.py':
        return None
    if _e == 'line':
        _left[0] -= 1
        if _left[0] < 0:
            raise _Runaway('ran too long')
    if _e == 'return' and _fr.f_code.co_name == 'make_bar' and _tn(_a) == 'str':
        _made.append(_a.strip())
    return _tr2
_out, _old = _sys.stdout, _sys.gettrace()
_sys.stdout = _Cap()
_sys.settrace(_tr2)
try:
    _B.exec(_B.compile(_parsed(), 'main.py', 'exec'), {'__name__': '__main__'})
except (Exception, _Runaway):
    pass
finally:
    _sys.settrace(_old)
    _sys.stdout = _out
_seen, _from_fn = [], []
for _l in _lines():
    _hit = _re.fullmatch(r'Glug \[[▓░]*\] (\d+)/(\d+)', _l)
    if _hit:
        _seen.append((_int(_hit.group(1)), _int(_hit.group(2))))
        if _l in _made:
            _from_fn.append(_seen[-1])
def _edge(_pairs, _full):
    return _any((_c == _m if _full else _c == 0) and _m > 0 for _c, _m in _pairs)
assert not ((_edge(_seen, False) and not _edge(_from_fn, False)) or (_edge(_seen, True) and not _edge(_from_fn, True))), (
    'Print bars that `make_bar` builds, with `print(make_bar(...))`. A bar glued together outside the function '
    'does not come from it.')
assert _edge(_from_fn, False), (
    'Below the other prints, print the bar for an empty canteen: call `make_bar` with 0 sips left.')
assert _edge(_from_fn, True), (
    'Now print the bar for a full canteen: call `make_bar` with as many sips left as it holds.')
''',
    FOREIGN=BAR_FOREIGN.split(","),
)

BARS_ONE_MORE_TIME = dict(
    id="bars-one-more-time",
    title="Bars one more time",
    martu=(
        "The bars, one more time. In the campaign you filled in `\"█\" * caster[\"mana\"]`. Tonight, Lucky's "
        "canteen. It holds a few sips of glug. Hand back a bar like this one, for any canteen:\n"
        "```text\nGlug [▓▓░] 2/3\n```\n"
        "In `make_bar(current, maximum)`, `current` is the sips left and `maximum` is how many sips the canteen "
        "holds.\n"
        "One `▓` for each sip left, one `░` for each sip gone, then the numbers. Stamp with `*`, glue with `+`, and "
        "turn numbers into text with `str()`. All three you know. Now they work together."
    ),
    example=FUEL_BAR + "print(fuel_bar(2, 5))\n",
    example_output="Fuel ##... 2",
    names=["make_bar", "current", "maximum", "full", "empty"],
    pick="# Mar'tu's picks for step 3: make_bar(0, 3) and make_bar(3, 3)",
    predict=dict(
        q="The tank holds 4 and 1 is left. What will this print?",
        code=FUEL_BAR + "print(fuel_bar(1, 4))\n",
        choices=["Fuel #### 1", "Fuel .### 1", "Fuel #... 1", "Fuel #... 4"],
        answer=2,
        explain=(
            "The first number goes to the first parameter, `left`, so `left` is 1 and `tank` is 4. One `#` for the "
            "fuel left, then `4 - 1` dots, then `str(left)`: `Fuel #... 1`."
        ),
    ),
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="just-the-blocks",
            text="First, make `make_bar` hand back just the blocks: `▓▓░` for `make_bar(2, 3)`, for any numbers.",
            dictated=False,
            hints=[
                "Inside `make_bar`, `current` is the sips left and `maximum` is how many sips the canteen holds. "
                "`full` gets stamped once for each sip left, `empty` once for each sip gone.",
                "`*` stamps text: `\"#\" * 3` is `###`. Sips gone is `maximum - current`. Like the example's "
                "`gone = tank - left`, a variable of its own makes Python work that out first.",
                "Glue the two stamps with `+`, full blocks first, then hand the result back with `return`, like the "
                "example's `meter` lines.",
                "Write `used = maximum - current`, then `bar = full * current`, then `bar = bar + empty * used`, "
                "then `return bar`.",
            ],
            checks=[BLOCKS_CHECK],
            pass_line="Lucky: Two full, one empty. Don't look at me like that.",
        ),
        dict(
            id="label-and-numbers",
            text="Now glue on the label and the numbers, so it hands back `Glug [▓▓░] 2/3`.",
            dictated=False,
            hints=[
                "The blocks are done. Glue the pieces around them with `+`: `\"Glug [\"` in front, then `\"] \"` "
                "and the numbers after.",
                "Like the example's `str(left)` line: `str(current) + \"/\" + str(maximum)`.",
                "Write `bar = \"Glug [\" + bar + \"] \"`, then `bar = bar + str(current) + \"/\"`, then "
                "`bar = bar + str(maximum)`, then `return bar`, in place of your `return bar`.",
            ],
            checks=[BAR_CHECK],
            pass_line="Lucky: That's my canteen. 2 of 3. Don't tell Mar'tu how it smells.",
        ),
        dict(
            id="empty-and-full",
            text="Below the other prints, print two more bars: an empty canteen and a full one.",
            dictated=False,
            hints=[
                "An empty canteen has 0 sips left. A full one has as many sips left as it holds.",
                "Call the function with numbers that show the edges: `fuel_bar(0, 5)` is an empty tank, and "
                "`fuel_bar(5, 5)` is a full one. `\"#\" * 0` is just empty text, so nothing breaks.",
                "Write `print(make_bar(0, 3))` and `print(make_bar(3, 3))` at the bottom.",
            ],
            checks=[BAR_EDGE_CHECK],
            pass_line="Mar'tu: Empty, full, and everything between. The same line does them all, yes?",
        ),
    ],
    solution=BAR_SOLUTION,
    partials=[_bar(BLOCKS_BODY + BAR_RETURN), _bar(BAR_BODY)],
    assemble=dict(
        lines=[line for line in (BAR_HEAD + BAR_BODY + BAR_CALLS + BAR_EDGES).splitlines()],
        distractors=["    bar = full * maximum", '    bar = bar + str(maximum) + "/"', "    print(bar)"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The bar in pieces",
            text=(
                "```text\nGlug [ ▓▓  ░  ]  2 / 3\n      |   |      | |\n      |   |      | maximum\n"
                "      |   |      current\n      |   empty * (3 - 2)\n      full * 2\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `used = maximum - current`: the sips gone.\n2. Stamp `full` `current` times, and `empty` `used` "
                "times: the blocks.\n3. Glue `\"Glug [\"` on the front, then `\"] \"`, `str(current)`, `\"/\"` and "
                "`str(maximum)` on the end.\n4. `return` the whole bar."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "The campaign's mana bar is the same build: `filled = \"█\" * caster[\"mana\"]`, then the empty "
                "blocks, then `str(...)` for the numbers. Your glug bar is that bar, built by you."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE_2,
        part="mana-bars",
        snippet='return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])',
        why=(
            "You have seen this line in the mana bars. It felt long, yes? Now read it piece by piece: blocks "
            "stamped with `*`, glued with `+`, and each number turned into text with `str()`. The same pieces "
            "as your glug bar."
        ),
    ),
    takeaway="A bar for any values: stamp `full * current` and `empty * (maximum - current)`, glue with `+` and `str()`.",
    wrong_answers=[
        dict(why="the starter: pass", code=BAR_STARTER, fails_at=1, message_contains="It handed back `None` (Python's"),
        dict(why="print for return", code=_bar(BAR_BODY.replace(BAR_RETURN, "    print(bar)\n")), fails_at=1,
             message_contains="not `print`"),
        dict(why="typed bar: the first call's answer", code=_bar('    return "Glug [▓▓░] 2/3"\n'), fails_at=1,
             message_contains="both handed back the same text"),
        dict(why="typed blocks: the first call's blocks", code=_bar('    return "▓▓░"\n'), fails_at=1,
             message_contains="both handed back the same text"),
        dict(why="numbers glued with no str() (TypeError on the student's own Run)",
             code=_bar(BAR_BODY.replace("str(current)", "current")), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="no brackets: empty * maximum - current (TypeError on the student's own Run)",
             code=_bar(BAR_BODY.replace("used = maximum - current", "used = 0").replace(
                 "empty * used", "empty * maximum - current")), fails_at=0, message_contains="unsupported operand"),
        dict(why="all empty: empty * maximum", code=_bar(BAR_BODY.replace("empty * used", "empty * maximum")),
             fails_at=1, message_contains="each sip gone"),
        dict(why="all full: full * maximum", code=_bar(BAR_BODY.replace("full * current", "full * maximum")),
             fails_at=1, message_contains="each sip left"),
        dict(why="the empty blocks first",
             code=_bar(BAR_BODY.replace("    bar = full * current\n    bar = bar + empty * used\n",
                                        "    bar = empty * used\n    bar = bar + full * current\n")),
             fails_at=1, message_contains="full blocks first"),
        dict(why="the campaign's block █ for full", code=_bar(BAR_BODY.replace("full * current", '"█" * current')),
             fails_at=1, message_contains="used `█`"),
        dict(why="a near-miss of a parameter, curent (the calls taken out, so the check's own call meets it: _why)",
             code=_bar(BAR_BODY.replace("full * current", "full * curent"), calls=""), fails_at=1,
             message_contains="You wrote `curent`. Python matches names letter for letter."),
        dict(why="curent with the calls kept: the student's own Run stops (NameError, the explainer's row)",
             code=_bar(BAR_BODY.replace("full * current", "full * curent")), fails_at=0,
             message_contains="name 'curent' is not defined"),
        dict(why="the example's left for current (the calls taken out: _why)",
             code=_bar(BAR_BODY.replace("maximum - current", "maximum - left"), calls=""), fails_at=1,
             message_contains="`left` comes from Mar'tu's example. The parameters of `make_bar` are"),
        dict(why="the example's tank for maximum (the calls taken out: _why)",
             code=_bar(BAR_BODY.replace("used = maximum", "used = tank"), calls=""), fails_at=1,
             message_contains="`tank` comes from Mar'tu's example"),
        dict(why="the blocks done, the label not started (the partial)", code=_bar(BLOCKS_BODY + BAR_RETURN),
             fails_at=2, message_contains="just the blocks"),
        dict(why="the numbers left off", code=_bar(BLOCKS_BODY + '    bar = "Glug [" + bar + "]"\n' + BAR_RETURN),
             fails_at=2, message_contains="End with the numbers"),
        dict(why="the numbers swapped", code=_bar(BAR_BODY.replace("str(current)", "str(MAXX)").replace(
            "str(maximum)", "str(current)").replace("MAXX", "maximum")), fails_at=2, message_contains="sips left first"),
        dict(why="no space before the numbers", code=_bar(BAR_BODY.replace('"] "', '"]"')), fails_at=2,
             message_contains="brackets and spaces"),
        dict(why="no Glug label", code=_bar(BAR_BODY.replace('"Glug [" + bar', '"[" + bar')), fails_at=2,
             message_contains="Start the bar with"),
        dict(why="step 3 not done (the partial)", code=_bar(BAR_BODY), fails_at=3, message_contains="empty canteen"),
        dict(why="step 3 with typed bars", code=_bar(BAR_BODY, edges='print("Glug [░░░] 0/3")\nprint("Glug [▓▓▓] 3/3")\n'),
             fails_at=3, message_contains="typed in quotes"),
        dict(why="only the empty bar printed", code=_bar(BAR_BODY, edges="print(make_bar(0, 3))\n"), fails_at=3,
             message_contains="full canteen"),
        dict(why="step 3 typed by hand from pieces, with str() for the numbers (no quoted 0/3 to spot)",
             code=_bar(BAR_BODY, edges='print("Glug [░░░] " + str(0) + "/" + str(3))\n'
                                       'print("Glug [▓▓▓] " + str(3) + "/" + str(3))\n'),
             fails_at=3, message_contains="glued together outside the function"),
        dict(why="step 3: one edge from make_bar, the other glued by hand",
             code=_bar(BAR_BODY, edges='print(make_bar(0, 3))\nprint("Glug [" + "▓" * 3 + "] " + "3" + "/" + "3")\n'),
             fails_at=3, message_contains="glued together outside the function"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="repeat-string", solo="false", dictates="",
             foreign_names=BAR_FOREIGN, par="(3, 5),(6, 9); edges (0, 5),(4, 4)", stages="P,Mk",
             spaced="repeat-string") + "\n"
        "8A-07 (spaced repeat-string). Starter `def make_bar(current, maximum):` with `full = \"▓\"` and "
        "`empty = \"░\"` pre-typed (the symbol tray has both). The teacher's rebuild (the ladder dropped students "
        "here: one blank `pass`, five pieces): Mar'tu says what each number means; the example shows `str(left)` "
        "(`Fuel ##... 2`); a predict on the runnable example, `fuel_bar(1, 4)` -> `Fuel #... 1` (the first number "
        "goes to the first parameter; distractors: the tank size used as fuel left, the blocks backwards, the "
        "wrong number glued on); then three checkpoints, every Show-me the full lines. CP1 [ND] just-the-blocks: "
        "`▓▓░` for (2, 3); PAR with (3, 5) and (6, 9) counts the blocks only (▓ == current, ░ == maximum - current, "
        "full ones first), so a finished CP2 bar still passes it; RET (`None`, glossed as Python's word for nothing "
        "came back: the lesson's first `None` message; print for return). Named slips: typed blocks or a typed bar "
        "(PAR-CONST), all empty, all full, the empty ones first, `█`. CP2 [ND] label-and-numbers: `Glug [▓▓░] 2/3` "
        "(the old bar-for-any-values check, PAR on the same fresh numbers): just the blocks, the numbers missing or "
        "swapped, the spacing and the missing label are named; `+ current` with no `str()` and `empty * maximum - "
        "current` stop the student's own Run (the explainer's rows). CP3 [ND] (spec 'empty and full'): two printed "
        "calls, 0 sips and a full canteen, with a PAR on (0, 5) and (4, 4); bars typed in quotes are named, and a "
        "traced rerun keeps every bar `make_bar` hands back, so an edge bar glued by hand from pieces "
        "(`\"Glug [░░░] \" + str(0) + ...`) fails too. `_why` (Units 3 / 7) explains an error inside `make_bar` "
        "that the check's own call meets: `curent` (a near-miss: 'Python matches names letter for letter'), "
        "`left` / `tank` (the example's names; proven with the bottom calls taken out, since with them the "
        "student's own Run stops first). PAR never uses the task's (2, 3), (1, 4), (0, 3) or (3, 3) (lint b). The "
        "step-by-step solution keeps every line under 36 characters; the one-line campaign form `return \"Glug [\" "
        "+ ... + str(maximum)` passes too. Lucky's box: the mana-bars return line. PA: yes (assemble with three "
        "distractors). `pick` is a note (the step 3 calls), because the checks accept any sizes."
    ),
)

# ---- 8A-S solo-8a -------------------------------------------------------------------------------------------------

SOLO_A_HEAD = "# Bomb Shell's Velocite: a bar\n# with 7 blocks, one per day.\ndays_left = 3\nweek = 7\nbar = \"▓\" * days_left\n"
SOLO_A_PRINT = 'print("Velocite [" + bar + "]")\n'


def _solo_a(line='bar = bar + "░" * week - days_left', tail=""):
    return SOLO_A_HEAD + line + "\n" + SOLO_A_PRINT + tail


SOLO_A_STARTER = _solo_a()
SOLO_A_LINE = 'bar = bar + "░" * (week - days_left)'
SOLO_A_SOLUTION = _solo_a(SOLO_A_LINE)

SOLO_A_CHECK = chk(
    "the Velocite bar has a block for every day of the week, for other numbers too",
    r'''
def _blk(_n):
    return _str(_n) + (' block' if _n == 1 else ' blocks')
for _vals in (None, {'days_left': 5}, {'days_left': 0, 'week': 4}):
    if _vals is None:
        _ns, _rows, _err, _miss, _ev = globals(), _lines(), '', [], ''
    else:
        _ns, _rows, _err, _miss = _rerun(_vals)
        _ev = _tried(_vals)
    assert not _miss, 'The line `' + _miss[0] + ' = ...` from the starter is gone.'
    assert not _err, 'With other numbers, Python stopped: ' + _err + '.' + _ev
    _d, _w = _ns.get('days_left'), _ns.get('week')
    _want = 'Velocite [' + '▓' * _d + '░' * (_w - _d) + ']'
    if _want in _rows:
        continue
    _got = [_l for _l in _rows if _l.startswith('Velocite')]
    assert _got, 'Nothing printed the Velocite bar.' + _ev
    _nf, _ne = _got[-1].count('▓'), _got[-1].count('░')
    assert _nf == _d, 'The bar shows ' + _blk(_nf) + ' full for ' + _str(_d) + ' days left.' + _ev
    assert _nf + _ne == _w, 'The bar holds ' + _blk(_nf + _ne) + ' in all, for a week of ' + _str(_w) + ' days.' + _ev
    assert False, 'The printed line does not start with `Velocite [` and end with `]`.' + _ev
''',
)

SOLO_8A = dict(
    id="solo-8a",
    title="Show Mar'tu",
    martu=(
        "One bug, just for you. Read Python's last line, then the line it names. Bomb Shell's bar should hold a "
        "block for every day of the week, yes?"
    ),
    solo=True,
    explainer="lean",
    names=["bar", "week", "days_left"],
    starter=SOLO_A_STARTER,
    checkpoints=[
        dict(
            id="brackets-first",
            text="Mend line 6 so the bar holds `week` blocks in all: `▓` for each day left, `░` for the rest.",
            dictated=False,
            hints=[
                "Read Python's last line: `unsupported operand type(s) for -: 'str' and 'int'`.",
                "Python does `*` before `-`. So `\"░\" * week` is text first. Then it tries to take a number away "
                "from text.",
                "Brackets go first: `\"#\" * (5 - 2)` stamps 3 marks.",
                "Write `" + SOLO_A_LINE + "` on line 6.",
            ],
            checks=[SOLO_A_CHECK],
            pass_line="Mar'tu: You did that alone. I saw. On your map: ✓ empty blocks, worked out first.",
        ),
    ],
    solution=SOLO_A_SOLUTION,
    assemble=dict(
        lines=["days_left = 3", "week = 7", 'bar = "▓" * days_left', SOLO_A_LINE, SOLO_A_PRINT.strip()],
        distractors=['bar = bar + "░" * week - days_left', 'bar = bar + "░" * (week - 3)', 'bar = bar + "░" * week'],
    ),
    another_way=[
        dict(angle="shorter", text="`*` goes before `-`. Brackets go before both."),
        dict(
            angle="step-by-step",
            text="1. Work out the days gone: week minus days left. 2. Stamp `░` that many times. 3. Glue it on.",
        ),
    ],
    takeaway="On your own: brackets make Python work out `week - days_left` before it stamps.",
    wrong_answers=[
        dict(why="the starter: * before - (TypeError)", code=SOLO_A_STARTER, fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the 3 typed: (week - 3)", code=_solo_a('bar = bar + "░" * (week - 3)'), fails_at=1,
             message_contains="in all"),
        dict(why="the minus taken out: a whole week of empty blocks", code=_solo_a('bar = bar + "░" * week'),
             fails_at=1, message_contains="10 blocks in all"),
        dict(why="the subtraction the wrong way round: no empty blocks", code=_solo_a('bar = bar + "░" * (days_left - week)'),
             fails_at=1, message_contains="3 blocks in all"),
        dict(why="the bar typed in the print", code=_solo_a('bar = bar + "░" * (week - days_left)')
             .replace(SOLO_A_PRINT, 'print("Velocite [▓▓▓░░░░]")\n'), fails_at=1, message_contains="full for 5"),
        dict(why="seat B's slip shape: a letter changed in place (TypeError)", code=_solo_a(SOLO_A_LINE, 'bar[0] = "X"\n'),
             fails_at=0, message_contains="does not support item assignment"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="repeat-string,precedence", solo="true", dictates="",
             foreign_names="", seat_b='word[0] = "X" (TypeError: item assignment; the mend is "X" + word[1:])') + "\n"
        "SOLO, one bug (C6), explainer='lean' (the teacher's ruling from Unit 2 on). Seat A (and anyone solo) gets "
        "the old 8A-08's precedence bug, `\"░\" * week - days_left` (the spec's `\"░\" * 10 - 3` with the task's own "
        "names, so the check can rerun it): \"TypeError: unsupported operand type(s) for -: 'str' and 'int'\". "
        "Checked by CMB on the printed bar: the student's own run, then `days_left = 5`, then `days_left = 0` with "
        "`week = 4`, so a typed 3 or a typed bar fails. Lean messages name the slip and keep the evidence, never "
        "the fix ('The bar holds 9 blocks in all, for a week of 7 days.'). Seat B would get `word[0] = \"X\"` once "
        "pair mode ships; its TypeError is proven here by a wrong answer. Recorded, never blocking, never shown to "
        "a partner. The warm-up's Q2 recalls precedence on plain numbers (`2 + 3 * 4`), so it never shows this fix. "
        "The pass line claims only what the check proves: the empty blocks, worked out first."
    ),
)

LESSON_8A = dict(
    kind="lesson",
    id="strings-are-rows-of-letters",
    title="Strings Are Rows of Letters",
    minutes=22,
    summary="Read letters by their place, cut slices, build new strings, put quotes and new lines inside text, and draw a bar for any values.",
    notes=(
        "Lesson 8A (SC). Preceded by 8a-remembers. Exactly one SOLO (solo-8a, lean). Non-dictated checkpoints: "
        "8A-01 CP1-2, 8A-03, 8A-06 CP2, 8A-07 CP1-3, 8A-S (lint g); dictated: 8A-06 CP1. 8A-01 runs the one-line "
        "slice first (slice-a-word, a quick win whose Greenroom line is the unit's first pass line), then the "
        "initials loop (build-initials). 8A-02 is absorbed into 8A-01 (slice-a-word); 8A-04, 8A-05 and 8A-08 are in "
        "the 9X pool (u09b). 8A-07 is a predict on the runnable fuel_bar and three checkpoints (the blocks, the label "
        "and the numbers, the edges). Campaign callback: mana-bars (8A-07, Lucky's box). 22 minutes: the spec's 20, "
        "plus 2 for 8A-07's bar predict and split (the teacher's ruling)."
    ),
    exercises=[LETTERS_HAVE_PLACES, LETTERS_CANT_CHANGE, ESCAPE_MARKS, BARS_ONE_MORE_TIME, SOLO_8A],
)

# =============================================================================================
# Mar'tu remembers… (8b-remembers)
# =============================================================================================

REMEMBERS_8B = dict(
    kind="quiz",
    id="8b-remembers",
    title="Mar'tu remembers…",
    optional=True,
    minutes=2,
    summary="Two quick questions from Lesson 8A. Nothing is scored.",
    notes=(
        "meta: path=SC; unscored warm-up shown inline before Lesson 8B. It absorbs Quiz 8A's core questions (the "
        "rest of Quiz 8A is in the 9X pool, u09b): Q1 `\"Telegun\"[-1]`, Q2 `\"Greenroom\"[:5]`. Q2 is asked through a "
        "tiny function, so the warm-up still carries the def/return item every warm-up has from Unit 4 on. A miss "
        "shows the answer and a one-line why, with no red X."
    ),
    questions=[
        dict(
            type="predict",
            id="last-letter",
            q="What will this print?",
            code='gun = "Telegun"\nprint(gun[-1])\n',
            choices=["n", "T", "u", "e"],
            answer="n",
            explain="`[-1]` counts from the end: the last letter, n. `[0]` would be T.",
            notes="T: -1 read as the first place; u: one from the end.",
        ),
        dict(
            type="predict",
            id="first-five",
            q="What will this print?",
            code='def first_five(text):\n    return text[:5]\n\nprint(first_five("Greenroom"))\n',
            choices=["Green", "Greenr", "Gree", "reenr"],
            answer="Green",
            explain=(
                "`[:5]` takes places 0, 1, 2, 3 and 4: five letters. The end place, 5, is left out. The function "
                "hands the slice back, and `print` shows it."
            ),
            notes="Greenr: the end place taken too; Gree: one short; reenr: counting from 1.",
        ),
    ],
)

# =============================================================================================
# Lesson 8B "Words That Change Shape"
# =============================================================================================

# ---- 8B-01 loud-and-quiet --------------------------------------------------------------------------------------

LOUD_STARTER = 'line = "shield up."\nline.upper()\nprint(line)\n'


def _loud(line="line = line.upper()", tail=""):
    return 'line = "shield up."\n' + line + "\nprint(line)\n" + tail


LOUD_SOLUTION = _loud()

LOUD_CHECK = chk(
    "line keeps the capital copy, for other text too",
    r'''
_o = _first_lit('line')
assert _tn(_o) == 'str', 'Keep the line `line = "shield up."` from the starter, at the top.'
assert 'line' in globals(), 'Keep the variable `line` from the starter.'
_v = globals()['line']
_want = _o.upper()
if _v != _want:
    assert not _is_method(_v), (
        'Add `()` after `.upper`. Without them, `line` holds the order, not the text. Python runs a method only '
        'with `()`.')
    assert _tn(_v) == 'str', 'Keep `line` as text: the capital copy that `.upper()` hands back.'
    assert not (_v == _o and _newbox(_want, ('line',))), (
        'Keep the capital copy in `line` itself: start the line with `line = `. Your new variable holds it, but '
        '`line` still holds small letters.')
    assert not (_v == _o and _want in _lines()), (
        'Keep the capital copy in `line`: start the line with `line = `. The print showed one, but `line` itself '
        'still holds small letters.')
    assert not (_v == _o and _bare('upper')), (
        'Catch the copy: `line.upper()` makes a capital copy, then nothing keeps it. Put it back in `line` with '
        '`line = `.')
    assert _v != _o.title(), (
        'That is `.title()`: a capital at the start of each word. This step wants every letter in capitals, with '
        '`.upper()`.')
    assert _v != _o.capitalize(), (
        'That is `.capitalize()`: only the first letter. This step wants every letter in capitals, with `.upper()`.')
    assert False, 'Make `line` hold the capital copy that `line.upper()` hands back.'
assert _want in _lines(), 'Print `line` after it changes, so the capital copy shows.'
_ns, _rows, _err, _miss = _rerun({'line': 'latch stuck.'})
assert not _miss, "Keep the line `line = \"shield up.\"` from the starter, so Mar'tu's check can try other text."
assert not _err, 'Make it work for other text too. Python stopped: ' + _err + '.' + _tried({'line': 'latch stuck.'})
assert _ns.get('line') == 'LATCH STUCK.', (
    'Make the copy from `line` with `.upper()`, so it follows the text. With other text, `line` did not.'
    + _tried({'line': 'latch stuck.'}))
''',
)

ALARM_CHECK = chk(
    "alarm is True when up is in line, whatever the capitals",
    r'''
assert 'alarm' in globals(), 'Make a variable named `alarm`.'
_a = globals()['alarm']
assert _tn(_a) == 'bool', 'Make `alarm` hold True or False: a question with `in`.'
assert _a is True, (
    'Ask a lower-case copy: `in` matches capitals exactly, and `line` now holds UP in capitals.')
for _t, _want in (('gear up.', True), ('latch stuck.', False)):
    _ns, _rows, _err, _miss = _rerun({'line': _t})
    assert not _err and _ns.get('alarm') is _want, (
        'Ask about `line` itself, so `alarm` follows the text.' + _tried({'line': _t}))
''',
)

LOUD_AND_QUIET = dict(
    id="loud-and-quiet",
    title="Loud and quiet",
    martu=(
        "Lucky asks the same thing about everything: \"What's in it for me?\" Ask a string to do something, and the "
        "answer is always the same: a new string.\n"
        "That is a [[method]]: an order with a dot. [[.upper()]] hands back a copy in CAPITALS. [[.title()]] hands "
        "back A Capital On Each Word. `.capitalize()`, from the campaign, does only the first letter.\n"
        "The copy is handed to you. The text in the variable does not change. Catch the copy with `=`, or it is "
        "gone."
    ),
    introduces=["attr:upper", "attr:title"],
    example='name = "bomb shell"\nname.title()\nprint(name)\nname = name.title()\nprint(name)\n',
    example_output="bomb shell\nBomb Shell",
    names=["line"],
    predict=dict(
        q="Before you press Run: what will this print?",
        choices=["shield up.", "SHIELD UP.", "Shield up.", "Shield Up."],
        answer="shield up.",
        explain=(
            "`line.upper()` made a copy in capitals and handed it back. Nothing caught it, so it was gone. `line` "
            "still holds the small letters."
        ),
    ),
    pair_talk="Before you press Run, each of you says what prints. Then tell your partner why it surprised you, or didn't.",
    starter=LOUD_STARTER,
    checkpoints=[
        dict(
            id="catch-the-copy",
            text="Change line 2 so `line` keeps the capital copy. Then the last line prints `SHIELD UP.`",
            dictated=False,
            hints=[
                "Read what it printed: `shield up.`, still small. Line 2 asks for a capital copy. Where does the "
                "copy go?",
                "A method hands you a new copy. Catch it in the variable with `=`, the way the example's last two "
                "lines do with `name`.",
                "Write `line = line.upper()` on line 2.",
            ],
            checks=[LOUD_CHECK],
            pass_line="Bomb Shell: SHIELD UP. Loud. Good.",
        ),
    ],
    solution=LOUD_SOLUTION,
    assemble=dict(
        lines=['line = "shield up."', "line = line.upper()", "print(line)"],
        distractors=["line.upper()", "line = line.upper", "upper(line)"],
    ),
    another_way=[
        dict(
            angle="everyday",
            label="Catch the copy",
            text=(
                "A method is like asking Gearshift for a copy of a map. He hands you a new map. If you don't take "
                "it, it falls on the floor. Your old map is still the old map. `line = line.upper()` takes the copy "
                "and keeps it."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `line.upper()` makes `\"SHIELD UP.\"` and hands it back.\n2. `line = ...` puts that copy in "
                "`line`.\n3. `print(line)` shows what `line` holds now."
            ),
        ),
        dict(
            angle="from the campaign",
            text=(
                "Module 1 wrote `dialogue_input = dialogue_input.lower()`. Same shape: the method on the right, the "
                "same name on the left to catch the copy."
            ),
        ),
    ],
    bonus=dict(
        by="bomb-shell",
        title="Is it up?",
        text=(
            "Bomb Shell checks his own report. Make `alarm` hold `True` when the word `up` is in `line`, whatever "
            "its capitals. `in` matches capitals exactly, so ask a lower-case copy."
        ),
        hints=[
            "`\"glow\" in \"Glow\"` is `False`: capitals count. `\"glow\" in \"Glow\".lower()` is `True`.",
            "Write `alarm = \"up\" in line.lower()` below the print.",
        ],
        checks=[ALARM_CHECK],
        solution=LOUD_SOLUTION + 'alarm = "up" in line.lower()\nprint(alarm)\n',
    ),
    takeaway="A method hands back a new string. Catch it: `line = line.upper()`.",
    wrong_answers=[
        dict(why="the starter: the copy is made, then nothing keeps it", code=LOUD_STARTER, fails_at=1,
             message_contains="nothing keeps it"),
        dict(why="printed, never kept: print(line.upper())", code=_loud("print(line.upper())"), fails_at=1,
             message_contains="The print showed one"),
        dict(why="kept in a new variable", code=_loud("shout = line.upper()"), fails_at=1,
             message_contains="new variable"),
        dict(why="no (): line holds the method", code=_loud("line = line.upper"), fails_at=1,
             message_contains="Add `()`"),
        dict(why="upper(line) as if it were a function (NameError)", code=_loud("line = upper(line)"), fails_at=0,
             message_contains="'upper' is not defined"),
        dict(why="a capital U (AttributeError)", code=_loud("line = line.Upper()"), fails_at=0,
             message_contains="has no attribute 'Upper'"),
        dict(why=".title() for .upper()", code=_loud("line = line.title()"), fails_at=1,
             message_contains="`.title()`"),
        dict(why=".capitalize() for .upper()", code=_loud("line = line.capitalize()"), fails_at=1,
             message_contains="only the first letter"),
        dict(why="typed by hand: SHIELD UP.", code=_loud('line = "SHIELD UP."'), fails_at=1,
             message_contains="With other text"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="string-methods", solo="false", dictates="",
             foreign_names="name", stages="P,R,I", twin='line = "latch stuck." then line = line.upper()') + "\n"
        "8B-01. Intro attr:upper and attr:title (`.capitalize()` revisited from Unit 3). Predict on the starter: "
        "`line.upper()` alone, then `print(line)`, shows `shield up.` (the investigate step: the copy is not kept). "
        "CP1 [ND]: `line` holds the capital copy (CMB with `line = \"latch stuck.\"`). The not-kept slip in its three "
        "shapes (a bare call, `print(line.upper())`, a new variable) each gets its own message; no `()`, "
        "`upper(line)`, `.Upper()`, `.title()`, `.capitalize()` and a typed line are named too. AW: everyday "
        "('a method hands you a new copy; catch it'), step-by-step, from the campaign. Side quest (Bomb Shell): "
        "case-sensitive `in`, `\"up\" in line.lower()` (`\"up\" in line` is False once `line` is in capitals)."
    ),
)

# ---- 8B-02 chain-the-spells (revisit of 6A-08) -----------------------------------------------------------------

TIDY_COMMENT = "    # Small letters, then a capital\n    # first letter. Hand it back.\n"
TIDY_TAIL = '\n\nasked = "WHAT IS THE DECAY?"\nprint(tidy_line(asked))\nprint(tidy_line("hOLD THE LINE."))\n'
TIDY_LINE = "    return raw.lower().capitalize()"
TIDY_FOREIGN = "said,cry,shout"   # the meta's foreign_names, read by _why too


def _tidy(body="    pass", comment=True, tail=TIDY_TAIL):
    return "def tidy_line(raw):\n" + (TIDY_COMMENT if comment else "") + body + "\n" + tail


TIDY_STARTER = _tidy()
TIDY_SOLUTION = _tidy(TIDY_LINE, comment=False)

TIDY_CHECK = chk(
    "tidy_line hands back small letters with a capital first letter, for fresh lines",
    r'''
_f = _need_def('tidy_line', 1, 'def tidy_line(raw):')
_res = []
for _a in __CASES__:
    _p, _v, _e = _call(_f, _a)
    _ev = _called('tidy_line', (_a,), 'it should hand back `' + _a.lower().capitalize() + '`')
    assert not _e, _why('tidy_line', _e, __FOREIGN__) + _ev
    _res.append((_a, _p, _v, _ev))
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    'Build the line from `raw`, so it changes with what is handed in. (Mar\'tu\'s check called `tidy_line` with two '
    'other lines, only inside the check: both handed back the same text.)')
for _a, _p, _v, _ev in _res:
    if _v == _a.lower().capitalize():
        continue
    assert not (_v is None and _p), (
        "Hand back the line with `return`, not `print`. `tidy_line` printed it, then handed back `None` (Python's "
        "word for nothing came back)." + _ev)
    assert _v is not None, (
        "End `tidy_line` with `return`, so it hands the tidy line back. It handed back `None` (Python's word for "
        "nothing came back)." + _ev)
    assert not _is_method(_v), (
        'Add `()` after `.' + _v.__name__ + '`. Without them, `tidy_line` hands back the order, not the text. Python '
        'runs a method only with `()`.' + _ev)
    assert _tn(_v) == 'str', 'Hand back text: `raw` after its two methods.' + _ev
    assert _v != _a, (
        'Keep what the methods hand back. `tidy_line` handed back the line as it came in: each method made a copy, '
        'and nothing kept it.' + _ev)
    assert _v != _a.lower(), 'Add `.capitalize()` after `.lower()`, so the first letter is a capital.' + _ev
    assert _v != _a.title(), (
        'That is `.title()`: a capital at the start of every word. `.capitalize()` makes only the first letter '
        'big.' + _ev)
    assert False, 'Hand back `raw` in small letters with a capital first letter: `.lower()`, then `.capitalize()`.' + _ev
''',
    CASES=["THE CLOCK IS RED.", "mOON sTEP IS READY."],
    FOREIGN=TIDY_FOREIGN.split(","),
)

CHAIN_THE_SPELLS = dict(
    id="chain-the-spells",
    title="Chain the spells",
    martu=(
        "You have done this before. In Module 1, Mar'tu's line went through two tidy steps:\n"
        "```python\nsaid = said.lower()\nsaid = said.capitalize()\n```\n"
        "Each method hands back a new string. So you can call the next method on it straight away. That is a "
        "[[chain]]:\n"
        "```python\nsaid = said.lower().capitalize()\n```\n"
        "Python reads a chain left to right: `.lower()` first, then `.capitalize()` on what came back."
    ),
    example='cry = "sHIELD uP"\nprint(cry.lower())\nprint(cry.lower().title())\n',
    example_output="shield up\nShield Up",
    names=["tidy_line", "raw"],
    predict=dict(
        q="Before you press Run, look at this chain. What will it print?",
        code='shout = "SHIELD UP."\nprint(shout.capitalize().lower())\n',
        choices=["shield up.", "Shield up.", "SHIELD UP.", "Shield Up."],
        answer="shield up.",
        explain=(
            "Left to right: `.capitalize()` first gives `Shield up.`. Then `.lower()` makes every letter small "
            "again. In a chain, order matters."
        ),
    ),
    starter=TIDY_STARTER,
    checkpoints=[
        dict(
            id="tidy-line",
            text="Finish `tidy_line(raw)` so it hands back `raw.lower().capitalize()`: small letters, with a "
                 "capital first letter.",
            dictated=True,
            hints=[
                "Inside `tidy_line`, the text is called `raw`. Two methods, in order: `.lower()`, then "
                "`.capitalize()`. Then hand the result back.",
                "Two steps work, each one caught:\n```python\nsaid = said.lower()\nsaid = said.capitalize()\n"
                "return said\n```\nIn `tidy_line`, the text is called `raw`, so write `raw` where this says `said`. "
                "One chain on one line works too.",
                "Write `return raw.lower().capitalize()` in place of `pass`.",
            ],
            checks=[TIDY_CHECK],
            pass_line="Mar'tu: What is the decay? Good question. Ask it quietly, yes?",
        ),
    ],
    solution=TIDY_SOLUTION,
    assemble=dict(
        lines=["def tidy_line(raw):", TIDY_LINE, 'asked = "WHAT IS THE DECAY?"', "print(tidy_line(asked))",
               'print(tidy_line("hOLD THE LINE."))'],
        distractors=["    raw.lower().capitalize()", "    return raw.lower.capitalize()",
                     "    return raw.capitalize().lower()"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="One copy at a time",
            text=(
                "```text\n\"WHAT IS THE DECAY?\"\n   .lower()\n\"what is the decay?\"\n   .capitalize()\n"
                "\"What is the decay?\"\n```\nEach arrow down is a new copy. `return` hands back the last one."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `raw.lower()` hands back a copy in small letters.\n2. `.capitalize()` works on that copy and "
                "hands back a new one with a capital first letter.\n3. `return` hands that last copy back."
            ),
        ),
        dict(
            angle="shorter",
            label="A secret about .capitalize()",
            text=(
                "`.capitalize()` already makes the rest small, so `raw.capitalize()` alone gives the same here. The "
                "campaign chains both to be sure."
            ),
        ),
    ],
    campaign_link=dict(
        module=MODULE_1,
        part="program-dialogue-options",
        snippet=(
            "print_options(\n"
            "    option_1.lower().capitalize(),\n"
            "    option_2.lower().capitalize(),\n"
            "    option_3.lower().capitalize(),\n"
            "    option_4.lower().capitalize(),\n"
            ")"
        ),
        why=(
            "You have seen these four lines in the dialogue options. Each one is a chain: `.lower()` first, then "
            "`.capitalize()` on what came back. The same chain as your `tidy_line`, four times over."
        ),
    ),
    takeaway="Methods chain left to right: `raw.lower().capitalize()`.",
    wrong_answers=[
        dict(why="the starter: pass", code=TIDY_STARTER, fails_at=1, message_contains="handed back `None`"),
        dict(why="print for return", code=_tidy("    print(raw.lower().capitalize())"), fails_at=1,
             message_contains="not `print`"),
        dict(why="two bare steps, nothing kept, then return raw",
             code=_tidy("    raw.lower()\n    raw.capitalize()\n    return raw"), fails_at=1,
             message_contains="nothing kept it"),
        dict(why="no (): the method handed back", code=_tidy("    return raw.lower"), fails_at=1,
             message_contains="Add `()`"),
        dict(why="no () in the middle of the chain (AttributeError on the student's own Run)",
             code=_tidy("    return raw.lower.capitalize()"), fails_at=0,
             message_contains="has no attribute 'capitalize'"),
        dict(why="lower(raw) as if it were a function (NameError)", code=_tidy("    return capitalize(lower(raw))"),
             fails_at=0, message_contains="is not defined"),
        dict(why="only .lower()", code=_tidy("    return raw.lower()"), fails_at=1, message_contains="Add `.capitalize()`"),
        dict(why=".title() for .capitalize()", code=_tidy("    return raw.lower().title()"), fails_at=1,
             message_contains="`.title()`"),
        dict(why="the chain the wrong way round: capitalize, then lower", code=_tidy("    return raw.capitalize().lower()"),
             fails_at=1, message_contains="Add `.capitalize()`"),
        dict(why="typed: the task's own answer", code=_tidy('    return "What is the decay?"'), fails_at=1,
             message_contains="both handed back the same text"),
        dict(why="the example's said for raw (the bottom calls taken out, so the check's own call meets it: _why)",
             code=_tidy("    return said.lower().capitalize()", tail=""), fails_at=1,
             message_contains="`said` comes from Mar'tu's example. The parameter of `tidy_line` is `raw`."),
        dict(why="said with the calls kept: the student's own Run stops (NameError, the explainer's row)",
             code=_tidy("    return said.lower().capitalize()"), fails_at=0, message_contains="name 'said' is not defined"),
        dict(why="Mar'tu's two steps copied as they are: said used before it is made (UnboundLocalError: _why)",
             code=_tidy("    said = said.lower()\n    said = said.capitalize()\n    return said", tail=""), fails_at=1,
             message_contains="Make `said` first, then use it. Python runs a function from the top down."),
        dict(why="a near-miss of the parameter, rwa (the calls taken out: _why)",
             code=_tidy("    return rwa.lower().capitalize()", tail=""), fails_at=1,
             message_contains="You wrote `rwa`. Python matches names letter for letter."),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="chain-methods", solo="false", dictates="1",
             foreign_names=TIDY_FOREIGN, par='("THE CLOCK IS RED.",),("mOON sTEP IS READY.",)', stages="P,I,M")
        + "\n"
        "8B-02 (revisit of 6A-08). No new tokens. Predict: a chain the other way round "
        "(`.capitalize().lower()` -> all small), so order matters before the task. CP1 [D] `tidy_line(raw)` in two "
        "steps or chained as `raw.lower().capitalize()`: both forms pass, and so does `raw.capitalize()` alone (it "
        "lowers the rest; the 'shorter' angle says so honestly). Checks: PAR with two fresh lines, never the task's "
        "`\"WHAT IS THE DECAY?\"` (-> `\"What is the decay?\"`, verified); RET. The not-kept slip is caught in its "
        "two-step shape (`raw.lower()` alone, then `return raw`). The starter calls `tidy_line` twice (the task's "
        "line and `\"hOLD THE LINE.\"`), so a typed answer shows it breaks on the student's own screen; the check's "
        "fresh lines are different (lint b). Hint 1's two-step block uses the Learn pane's `said`, and says to write "
        "`raw` there. `_why` explains an error inside `tidy_line` the check's own call meets: `said` (the example's "
        "name: 'The parameter of `tidy_line` is `raw`'), Mar'tu's two steps copied as they are (`said = "
        "said.lower()`: UnboundLocalError, 'Make `said` first'), `rwa` (a near-miss); each is proven with the bottom "
        "calls taken out, since with them the student's own Run stops first. Its first `None` message is the "
        "lesson's first, glossed. Lucky's box: `option_1.lower().capitalize()` (program-dialogue-options)."
    ),
)

# ---- 8B-03 split-the-clipped (absorbs 8B-04 join-them-back) ------------------------------------------------------

CLIP_REPORT = "Latch stuck. Shield up."
OTHER_REPORT = "Optic dim. Moving out. Hold."
SPLIT_LINE = 'sentences = report.split(". ")'
COUNT_LINE = "word_count = len(report.split())"
INT_LINE = "next_hours = int(hours_text) + 1"
JOIN_LINE = 'joined = " ".join(words)'


def _clipped(s1="sentences = []", s2="word_count = 0", s3="next_hours = 0", s4='joined = ""'):
    return (
        f'report = "{CLIP_REPORT}"\n'
        '# 1. Cut report at each ". "\n'
        + s1 + "\nprint(sentences)\n"
        "\n"
        "# 2. Count the words in report.\n"
        + s2 + "\nprint(word_count)\n"
        "\n"
        '# 3. The text "48" as a number,\n'
        "#    plus one.\n"
        'hours_text = "48"\n'
        + s3 + "\nprint(next_hours)\n"
        "\n"
        "# 4. Glue the words back together,\n"
        "#    a space between them.\n"
        "words = [\"Barrier's\", \"holding.\"]\n"
        + s4 + "\nprint(joined)\n"
    )


CLIP_STARTER = _clipped()
CLIP_SOLUTION = _clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, JOIN_LINE)

SPLIT_CHECK = chk(
    "sentences holds report cut at each full stop and space, for another report too",
    r'''
_rep = globals().get('report')
assert _tn(_rep) == 'str', 'Keep the line `report = "Latch stuck. Shield up."` from the starter.'
assert 'sentences' in globals(), 'Keep the line `sentences = ...` from the starter.'
_s = globals()['sentences']
if _s != _rep.split('. '):
    assert not _is_method(_s), (
        'Add `()` after `.split`: `.split(". ")`. Without them, `sentences` holds the order, not the pieces. Python '
        'runs a method only with `()`.')
    assert _tn(_s) != 'str', (
        'Make `sentences` hold a list: `.split(". ")` hands back a list of pieces. It holds text.')
    _nb = _newbox(_rep.split('. '), ('sentences',))
    assert not (_s == [] and _nb), (
        'Put the pieces in `sentences`, the name this step asks for. `' + (_nb or [''])[0] + '` holds them, but '
        '`sentences` is still the empty list.')
    assert _s != [], 'Make `sentences` hold the pieces of `report`, cut with `.split(". ")`. It is still the empty list.'
    assert _s != _rep.split(), (
        'Put `". "` in the brackets, to cut at each full stop and space. Empty brackets cut at every space.')
    assert _s != _rep.split('.'), (
        'Put `". "` in the brackets: a full stop and a space. With the full stop alone, a space stays on the next '
        'piece.')
    assert False, 'Make `sentences` hold `report.split(". ")`: the report cut at each full stop and space.'
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _miss, "Keep the line `report = ...` from the starter, so Mar'tu's check can try another report."
assert not _err, 'Make it work for another report too. Python stopped: ' + _err + '.' + _tried({'report': _o})
assert _ns.get('sentences') == _o.split('. '), (
    'Cut `report` itself with `.split`, so `sentences` follows it. With another report, it did not.'
    + _tried({'report': _o}))
''',
    OTHER=OTHER_REPORT,
)

COUNT_CHECK = chk(
    "word_count is the number of words in report, for another report too",
    r'''
_rep = globals().get('report')
assert 'word_count' in globals(), 'Keep the line `word_count = ...` from the starter.'
_c = globals()['word_count']
if not (_c == _len(_rep.split()) and _tn(_c) == 'int'):
    assert _tn(_c) != 'list', 'Count the pieces with `len()`. `word_count` holds the list itself.'
    assert _tn(_c) == 'int', 'Make `word_count` a number: `len()` counts the pieces of a list.'
    assert not (_c == 0 and _first_lit('word_count') == 0 and _len(_assigns('word_count')) == 1), (
        "Make `word_count` hold the number of words in `report`. It still holds the starter's 0.")
    assert _c != _len(_rep), (
        'That counted every letter and space. Split `report` into words first, then count the pieces.')
    assert _c != _len(_rep.split('. ')), (
        'That counted the sentences. Count the words: split with empty brackets, at the spaces.')
    assert False, 'Make `word_count` hold the number of words in `report`, counted with `len()`.'
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _err, 'Make it work for another report too. Python stopped: ' + _err + '.' + _tried({'report': _o})
assert _ns.get('word_count') == _len(_o.split()), (
    'Count with `len()`, so `word_count` follows the report. With another report, it stayed ' + _str(_c) + '.'
    + _tried({'report': _o}))
''',
    OTHER=OTHER_REPORT,
)

INT_CHECK = chk(
    "next_hours is the number in hours_text plus one, for other text too",
    r'''
_h = globals().get('hours_text')
assert _tn(_h) == 'str' and _h.strip().isdigit(), 'Keep the line `hours_text = "48"` from the starter.'
assert 'next_hours' in globals(), 'Keep the line `next_hours = ...` from the starter.'
_n = globals()['next_hours']
if not (_n == _int(_h) + 1 and _tn(_n) == 'int'):
    assert not (_tn(_n) == 'str' and _n == _h + '1'), (
        'Turn `hours_text` into a number with `int()` first, then add 1. Gluing on the text `"1"` gave `'
        + _h + '1`.')
    assert _tn(_n) != 'str', 'Make `next_hours` a number: `int(hours_text)` turns the text into one, then `+ 1`.'
    assert not (_n == 0 and _first_lit('next_hours') == 0 and _len(_assigns('next_hours')) == 1), (
        "Make `next_hours` hold the number in `hours_text`, plus one. It still holds the starter's 0.")
    assert _n != _int(_h), 'Add one to the number, with `+ 1`.'
    assert False, 'Make `next_hours` hold `int(hours_text) + 1`.'
_ns, _rows, _err, _miss = _rerun({'hours_text': '37'})
assert not _miss, "Keep the line `hours_text = \"48\"` from the starter, so Mar'tu's check can try other text."
assert not _err, 'Make it work for other text too. Python stopped: ' + _err + '.' + _tried({'hours_text': '37'})
assert _ns.get('next_hours') == 38, (
    'Use `hours_text` itself, so `next_hours` follows it. With other text, it stayed ' + _str(_n) + '.'
    + _tried({'hours_text': '37'}))
''',
)

JOIN_CHECK = chk(
    "joined holds the words glued with a space, for another list too",
    r'''
_wd = globals().get('words')
assert _tn(_wd) == 'list', 'Keep the list `words` from the starter.'
assert 'joined' in globals(), 'Keep the line `joined = ...` from the starter.'
_j = globals()['joined']
if _j != ' '.join(_wd):
    assert _tn(_j) == 'str', 'Make `joined` text: `" ".join(words)` hands back one string.'
    assert _j != '', 'Make `joined` hold the words glued together. It is still empty.'
    assert _j != ''.join(_wd), 'Put a space between the quotes before `.join`. The words were glued with no gap.'
    assert _j != _str(_wd), 'That is the list written out, brackets and all. Glue the words with `" ".join(words)`.'
    assert _j != ' '.join('words'), _QUOTES + ' Take the quotes off `words`: `.join` glued its letters.'
    assert False, 'Make `joined` hold the words of `words`, glued with one space between them.'
_o = ['Optic', 'dim.', 'Hold.']
_ns, _rows, _err, _miss = _rerun({'words': _o})
assert not _miss, "Keep the line `words = [...]` from the starter, so Mar'tu's check can try another list."
assert not _err, 'Make it work for another list too. Python stopped: ' + _err + '.' + _tried({'words': _o})
assert _ns.get('joined') == 'Optic dim. Hold.', (
    'Glue every word in `words` with `.join`, so `joined` follows the list. With three words, it did not.'
    + _tried({'words': _o}))
''',
)

SPLIT_THE_CLIPPED = dict(
    id="split-the-clipped",
    title="Split and join",
    martu=(
        "Bomb Shell talks in short, clipped sentences: \"Latch stuck. Shield up.\"\n"
        "[[.split()]] cuts text into pieces. Empty brackets cut at every space. `.split(\". \")` cuts at each full "
        "stop and space. What comes back is a [[list]], not text: count it with `len()`, read it by place. Python "
        "shows a list's text with `'` marks. It is the same text.\n"
        "To glue a list back into one text, ask the glue: `\" \".join(words)`. The text before [[.join()]] goes "
        "between the pieces."
    ),
    introduces=["attr:split", "attr:join", "call:int"],
    example=(
        'cargo = "rope, salt, oats"\n'
        'items = cargo.split(", ")\n'
        "print(items)\n"
        "print(len(items))\n"
        'print("-".join(items))\n'
        'print(int("12") + 3)\n'
    ),
    example_output="['rope', 'salt', 'oats']\n3\nrope-salt-oats\n15",
    names=["report", "sentences", "word_count", "hours_text", "next_hours", "words", "joined"],
    predict=dict(
        q="Before you press Run, look at this smaller program. What will it print?",
        code=f'report = "{CLIP_REPORT}"\nprint(report.split())\n',
        choices=[
            "['Latch', 'stuck.', 'Shield', 'up.']",
            "['Latch stuck', 'Shield up.']",
            "Latch stuck. Shield up.",
            "['Latch stuck.', 'Shield up.']",
        ],
        answer=0,
        explain=(
            "With empty brackets, `.split()` cuts at every space: four pieces, in a list. The full stops stay on "
            "their words, and the spaces are gone."
        ),
    ),
    starter=CLIP_STARTER,
    checkpoints=[
        dict(
            id="split-the-report",
            text="Make `sentences` hold `report.split(\". \")`: the report cut at each full stop and space.",
            dictated=True,
            hints=[
                "Look at the `sentences = []` line. The pieces come from `report`.",
                "`\"rope, salt\".split(\", \")` gives `['rope', 'salt']`. What you put in the brackets is where the "
                "cuts go, and it vanishes.",
                "Write `" + SPLIT_LINE + "` in place of `sentences = []`.",
            ],
            checks=[SPLIT_CHECK],
            pass_line="Bomb Shell: Two sentences. Logged.",
        ),
        dict(
            id="count-the-words",
            text="Make `word_count` hold how many words `report` has, counted by Python.",
            dictated=False,
            hints=[
                "Two steps: split `report` into words, then count the pieces.",
                "`len()` counts the items in a list: `len([\"rope\", \"salt\"])` is 2. Given text, `len()` counts "
                "the letters and spaces instead.",
                "Two lines work too: `pieces = report.split()`, then `word_count = len(pieces)`.",
                "Write `" + COUNT_LINE + "` in place of `word_count = 0`.",
            ],
            checks=[COUNT_CHECK],
            pass_line="Bomb Shell: Four words. Enough.",
        ),
        dict(
            id="digits-to-a-number",
            text="`int()` turns digits into a number: `int(\"12\")` is 12. Make `next_hours` the number in "
                 "`hours_text`, plus one.",
            dictated=False,
            hints=[
                "`hours_text` holds `\"48\"`, in quotes. That is text, and text can't do math.",
                "`int(\"12\") + 3` is 15. Without `int()`, `\"12\" + 3` is a TypeError. And `int(\"twelve\")` is a "
                "ValueError: only digits turn into a number.",
                "Write `" + INT_LINE + "` in place of `next_hours = 0`.",
            ],
            checks=[INT_CHECK],
            pass_line="Mar'tu: 49. A number now, so it can do math, yes?",
        ),
        dict(
            id="join-them-back",
            text="Make `joined` hold `words` glued into one text, one space between each two.",
            dictated=False,
            hints=[
                "`.join` is asked of the glue, not of the list. What goes between the words?",
                "`\"-\".join([\"rope\", \"salt\"])` gives `rope-salt`. Asking the list, `words.join(\" \")`, is an "
                "AttributeError: a list has no `.join`.",
                "Write `" + JOIN_LINE + "` in place of `joined = \"\"`.",
            ],
            checks=[JOIN_CHECK],
            pass_line="Gearshift: Barrier's holding.",
        ),
    ],
    solution=CLIP_SOLUTION,
    partials=[
        _clipped(SPLIT_LINE),
        _clipped(SPLIT_LINE, COUNT_LINE),
        _clipped(SPLIT_LINE, COUNT_LINE, INT_LINE),
    ],
    assemble=dict(
        lines=[f'report = "{CLIP_REPORT}"', SPLIT_LINE, "print(sentences)", COUNT_LINE, "print(word_count)",
               'hours_text = "48"', INT_LINE, "print(next_hours)", "words = [\"Barrier's\", \"holding.\"]", JOIN_LINE,
               "print(joined)"],
        distractors=['joined = words.join(" ")', "word_count = len(report)", "next_hours = hours_text + 1"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Cut, then glue",
            text=(
                "```text\n\"Latch stuck. Shield up.\"\n   .split(\". \")\n['Latch stuck', 'Shield up.']\n\n"
                "[\"Barrier's\", \"holding.\"]\n   \" \".join(...)\n\"Barrier's holding.\"\n```"
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "`.split` is scissors: you say where to cut. `.join` is glue: you hold up the glue and say what to "
                "stick together. You never ask the paper to glue itself."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `report.split(\". \")`: a list of sentences.\n2. `len(report.split())`: split at spaces, then "
                "count.\n3. `int(hours_text) + 1`: text to number, then math.\n4. `\" \".join(words)`: the glue first, "
                "then the list."
            ),
        ),
        dict(
            angle="why",
            label="Why the glue does the joining",
            text=(
                "The glue is the one piece of text that goes between each two items. So you ask the glue to do the "
                "joining, and hand it the list: `\" \".join(words)`. The list only hands over its items."
            ),
        ),
    ],
    takeaway="`.split()` hands back a list; `\" \".join(words)` glues one back; `int(\"48\")` turns digits into a number.",
    wrong_answers=[
        dict(why="the starter", code=CLIP_STARTER, fails_at=1, message_contains="still the empty list"),
        dict(why="split at every space", code=_clipped("sentences = report.split()"), fails_at=1,
             message_contains="Empty brackets cut at every space"),
        dict(why="split at the full stop alone", code=_clipped('sentences = report.split(".")'), fails_at=1,
             message_contains="full stop alone"),
        dict(why="no (): the method itself", code=_clipped("sentences = report.split"), fails_at=1,
             message_contains="Add `()`"),
        dict(why="still the text, not a list", code=_clipped("sentences = report"), fails_at=1,
             message_contains="It holds text"),
        dict(why="split(report) as if it were a function (NameError)", code=_clipped('sentences = split(report, ". ")'),
             fails_at=0, message_contains="'split' is not defined"),
        dict(why="typed list", code=_clipped("sentences = ['Latch stuck', 'Shield up.']"), fails_at=1,
             message_contains="With another report"),
        dict(why="the Example's name: items holds the pieces, sentences is left empty",
             code=_clipped('items = report.split(". ")\nsentences = []'), fails_at=1,
             message_contains="the name this step asks for"),
        dict(why="the list treated as text: .lower() on a list (AttributeError)",
             code=_clipped(SPLIT_LINE + "\nsentences = sentences.lower()"), fails_at=0,
             message_contains="'list' object has no attribute 'lower'"),
        dict(why="len(report) counts letters", code=_clipped(SPLIT_LINE, "word_count = len(report)"), fails_at=2,
             message_contains="every letter and space"),
        dict(why="counted the sentences", code=_clipped(SPLIT_LINE, "word_count = len(sentences)"), fails_at=2,
             message_contains="counted the sentences"),
        dict(why="the list, not its count", code=_clipped(SPLIT_LINE, "word_count = report.split()"), fails_at=2,
             message_contains="holds the list itself"),
        dict(why="typed 4", code=_clipped(SPLIT_LINE, "word_count = 4"), fails_at=2, message_contains="it stayed 4"),
        dict(why="text plus a number, no int() (TypeError)", code=_clipped(SPLIT_LINE, COUNT_LINE,
                                                                            "next_hours = hours_text + 1"),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="the text 1 glued on: 481", code=_clipped(SPLIT_LINE, COUNT_LINE, 'next_hours = hours_text + "1"'),
             fails_at=3, message_contains="gave `481`"),
        dict(why="int() of the name in quotes (ValueError)",
             code=_clipped(SPLIT_LINE, COUNT_LINE, 'next_hours = int("hours_text") + 1'), fails_at=0,
             message_contains="invalid literal for int()"),
        dict(why="int() on text with letters in it: 48 hrs (ValueError)",
             code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE).replace('hours_text = "48"', 'hours_text = "48 hrs"'),
             fails_at=0, message_contains="invalid literal for int()"),
        dict(why="int() of the number word: seven (ValueError)",
             code=_clipped(SPLIT_LINE, COUNT_LINE, 'next_hours = int("seven") + 1'), fails_at=0,
             message_contains="invalid literal for int()"),
        dict(why="typed 49", code=_clipped(SPLIT_LINE, COUNT_LINE, "next_hours = 49"), fails_at=3,
             message_contains="it stayed 49"),
        dict(why="join called the wrong way round (AttributeError)",
             code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, 'joined = words.join(" ")'), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
        dict(why="empty glue: no space", code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, 'joined = "".join(words)'),
             fails_at=4, message_contains="no gap"),
        dict(why="the list written out with str()", code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, "joined = str(words)"),
             fails_at=4, message_contains="brackets and all"),
        dict(why="the list's name in quotes", code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, 'joined = " ".join("words")'),
             fails_at=4, message_contains="Take the quotes off"),
        dict(why="two words glued by place: a third is missed",
             code=_clipped(SPLIT_LINE, COUNT_LINE, INT_LINE, 'joined = words[0] + " " + words[1]'), fails_at=4,
             message_contains="With three words"),
    ],
    notes=(
        meta(starter_level="S3", path="SC", skills="split-join", solo="false", dictates="1",
             foreign_names="cargo,items", stages="P,M") + "\n"
        "8B-03 (absorbs 8B-04 join-them-back). Intro attr:split and attr:join (call:int is Unit 1's, listed again "
        "here as the spec does; the gate already allows it). Predict: `.split()` with empty brackets. The Learn pane "
        "says a list shows its text with `'` marks (the same text); its `int()` lines moved to CP3's own text. CP1 [D] "
        "split "
        "Bomb Shell's report on `\". \"` (CMB with another report; the Example's `items` holding the pieces is named). CP2 [ND] `len(report.split())` (CMB; this fixes "
        "the v1 OUT-only check): `len(report)` (letters) and the sentence count are named; a middle hint shows the two-"
        "line form (`pieces = report.split()`, then `len(pieces)`), which passes every checkpoint. CP3 [ND] (the "
        "teacher's ruling: the text says what `int()` does, not the line) `int(\"48\")` plus "
        "one: `\"48\" + 1` (TypeError), `\"48\" + \"1\"`, `int(\"hours_text\")`, `int(\"48 hrs\")` and `int(\"seven\")` "
        "(ValueError) are proven. `int(\"7 \")` is not a slip (Python strips the ends, verified in 3.13), so no "
        "message calls it one. CP4 [ND] join-them-back (the goal only; Mar'tu's text and the example model "
        "`\" \".join`, and a 'why' angle says why the glue does the joining): `words.join(\" \")` is the "
        "AttributeError row; empty glue, `str(words)`, a quoted name and two words glued by place (a rerun with "
        "three words) are named. Partials after CP1, CP2 and CP3."
    ),
)

# ---- 8B-05 strip-and-replace (absorbs 8B-06 find-a-rune) ---------------------------------------------------------

NOTE_TEXT = "  It's a compass.  "
OTHER_NOTE = "   A compass? No. "   # 3 spaces in front, 1 behind: a counted [2:-2] or a "  " swap leaves one
STRIP_LINE = "note = note.strip()"
SWAP_LINE = 'note = note.replace("compass", "Ley Clock")'
FIND_LINE = 'spot = note.find("Ley")'


def _note(s1="note = note", s2="note = note", s3="spot = 0", head=f'note = "{NOTE_TEXT}"', tail=""):
    return (
        head + "\n"
        "# 1. Strip the spaces off note.\n"
        + s1 + "\n"
        '# 2. Swap "compass" for\n'
        '#    "Ley Clock".\n'
        + s2 + "\n"
        'print("[" + note + "]")\n'
        '# 3. Where does "Ley" start?\n'
        + s3 + "\n"
        "print(spot)\n"
        + tail
    )


NOTE_STARTER = _note()
NOTE_SOLUTION = _note(STRIP_LINE, SWAP_LINE, FIND_LINE)

_NOTE_BASE = r'''
_o = _first_lit('note')
assert _tn(_o) == 'str', 'Keep the line `note = "  It\'s a compass.  "` from the starter, at the top.'
assert 'note' in globals(), 'Keep the variable `note` from the starter.'
_v = globals()['note']
_base = _o.strip()
def _ends_ok(_x, _start):
    # _x is _start with its end spaces cut off, and maybe its compass swapped for any words (step 2)
    _b = _start.strip()
    if _tn(_x) != 'str' or _x != _x.strip():
        return False
    if 'compass' not in _b:
        return _x == _b
    _pre, _suf = _b.split('compass', 1)
    return _x.startswith(_pre) and _x.endswith(_suf) and _len(_x) >= _len(_pre) + _len(_suf)
'''

STRIP_CHECK = chk(
    "note has no spaces at either end, for another note too",
    _NOTE_BASE + r'''
_later = False
if _is_method(_v) and _v.__name__ != 'strip':
    # Step 1 done and kept, then a later step left a method in `note`: that is step 2's slip, told there.
    _rerun({}, 'note')
    _later = _base in _rerun.hist
if not (_ends_ok(_v, _o) or _later):
    assert not _is_method(_v), (
        'Add `()` after `.' + _v.__name__ + '`' + (', with the old and new words inside' if _v.__name__ == 'replace'
                                                   else '') + '. Without them, `note` holds the order, not the text. '
        'Python runs a method only with `()`.')
    assert _tn(_v) == 'str', 'Keep `note` as text: the copy that `.strip()` hands back.'
    assert not (_v == _o and _bare('strip')), (
        'Catch the stripped copy: put it back in `note` with `note = `. `note.strip()` made a copy, and nothing kept '
        'it.')
    _nb = _newbox(_base, ('note',))
    assert not (_v == _o and _nb), (
        'Put the stripped copy back in `note` itself: start the line with `note = `. `' + (_nb or [''])[0]
        + '` holds it, but `note` still has its spaces.')
    assert _v != _o, 'Cut the spaces off `note` and put the copy back in it: `note = note.strip()`.'
    assert _v == _v.strip(), 'Spaces are still on one end. `.strip()` cuts both ends.'
    assert _v.replace('LeyClock', 'compass') != _base.replace(' ', ''), (
        'That took out every space, even between the words. `.strip()` cuts only the spaces at the ends.')
    assert False, 'Make `note` hold itself with the spaces cut off both ends: `note = note.strip()`.'
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2}, 'note')
assert not _miss, "Keep the line `note = ...` from the starter, so Mar'tu's check can try another note."
assert not _err, 'Make it work for another note too. Python stopped: ' + _err + '.' + _tried({'note': _o2})
_nv = _ns.get('note')
assert _o2.strip() in _rerun.hist or _ends_ok(_nv, _o2) or not (_tn(_nv) == 'str' and _nv != _nv.strip()), (
    'Cut the spaces with `.strip()`, so however many there are, they all go. With another note, a space was left '
    'at one end.' + _tried({'note': _o2}))
assert _o2.strip() in _rerun.hist or _ends_ok(_nv, _o2), (
    'Strip `note` itself, so it follows the note. With another note, it did not.' + _tried({'note': _o2}))
''',
    OTHER=OTHER_NOTE,
)

SWAP_CHECK = chk(
    "note says Ley Clock where it said compass, for another note too",
    _NOTE_BASE + r'''
_want = _base.replace('compass', 'Ley Clock')
if _v != _want:
    assert not _is_method(_v), (
        'Add `()` after `.' + _v.__name__ + '`' + (', with the old and new words inside' if _v.__name__ == 'replace'
                                                   else '') + '. Without them, `note` holds the order, not the text. '
        'Python runs a method only with `()`.')
    _args = [[_a.value for _a in _n.args if _tn(_a) == 'Constant'] for _n in _ast.walk(_parsed())
             if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute' and _n.func.attr == 'replace']
    assert not (_v == _base and _any(_a[:1] == ['Compass'] for _a in _args)), (
        'Match the capitals exactly: the note says `compass`, with a small c. `.replace` found no `Compass`, so '
        'nothing changed.')
    assert not (_v == _base and _any(_a[:1] == ['Ley Clock'] for _a in _args)), (
        'Put the old words first: `.replace(old, new)`. The note has no Ley Clock to swap yet.')
    assert not (_v == _base and _bare('replace')), (
        'Catch the swapped copy: put it back in `note` with `note = `. `.replace` made a copy, and nothing kept it.')
    assert _tn(_v) != 'str' or _v.lower() != _want.lower(), "Write `Ley Clock` with its two capitals, like Mar'tu does."
    assert _v != _base, 'Make `note` say `Ley Clock` where it says `compass`, with `.replace`.'
    assert False, 'Make `note` say `Ley Clock` where it says `compass`. Swap only that word.'
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err, 'Make it work for another note too. Python stopped: ' + _err + '.' + _tried({'note': _o2})
assert _ns.get('note') == _o2.strip().replace('compass', 'Ley Clock'), (
    'Swap the word inside `note` itself, so it follows the note. With another note, it did not.'
    + _tried({'note': _o2}))
''',
    OTHER=OTHER_NOTE,
)

FIND_CHECK = chk(
    "spot is the place where Ley starts in note, for another note too",
    _NOTE_BASE + r'''
assert 'spot' in globals(), 'Keep the line `spot = ...` from the starter.'
_sp = globals()['spot']
if not (_tn(_sp) == 'int' and _sp == _v.find('Ley')):
    assert _tn(_sp) != 'bool', '`in` answers True or False. This step wants the place, a number: ask with `.find`.'
    assert _tn(_sp) != 'str', 'That is a letter, not a place. `.find` hands back the place, a number.'
    assert _sp != -1, (
        '-1 means not found, not the last letter. Look for `"Ley"`, written exactly as the note writes it.')
    assert not (_sp == 0 and _first_lit('spot') == 0 and _len(_assigns('spot')) == 1), (
        "Make `spot` hold the place where `\"Ley\"` starts. It still holds the starter's 0.")
    assert False, 'Make `spot` hold the place where `"Ley"` starts in `note`, found with `.find`.'
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err, 'Make it work for another note too. Python stopped: ' + _err + '.' + _tried({'note': _o2})
assert _ns.get('spot') == _ns.get('note', '').find('Ley'), (
    'Find it with `.find`, so `spot` follows the note. With another note, it stayed ' + _str(_sp) + '.'
    + _tried({'note': _o2}))
''',
    OTHER=OTHER_NOTE,
)

ANY_SIGN_LINES = 'sign = "Greenroom, Interior"\nword = sign[:sign.find(",")]\nprint(word)\n'
OTHER_COMMA_SIGN = "Pantry, Interior"   # the comma at place 6, not 9 as on the greenroom sign: a counted [0:9] misses

ANY_SIGN_CHECK = chk(
    "word is the word before the comma, found with .find, for a sign with its comma in another place",
    r'''
_s = _first_lit('sign')
assert _tn(_s) == 'str' and ',' in _s, 'Below the prints, make `sign = "Greenroom, Interior"`.'
assert 'word' in globals(), 'Below the `sign` line, make `word` the word before the comma.'
_w = globals()['word']
assert _w == _s[:_s.find(',')], (
    "Make `word` hold the word before the comma: slice `sign` from the start up to the comma's place.")
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'sign': _o})
assert not _miss, "Keep the line `sign = ...` with its text in quotes, so Mar'tu's check can try another sign."
assert not _err, 'Make it work for another sign too. Python stopped: ' + _err + '.' + _tried({'sign': _o})
assert _ns.get('word') == _o[:_o.find(',')], (
    'Find the comma with `sign.find(",")`, so the slice ends wherever the comma is. With another sign, the comma '
    'sat in another place.' + _tried({'sign': _o}))
''',
    OTHER=OTHER_COMMA_SIGN,
)

STRIP_AND_REPLACE = dict(
    id="strip-and-replace",
    title="Clean-up tools",
    martu=(
        "Lucky left a note on the mantle. It has spaces at both ends, and it is wrong.\n"
        "Three more [[method|methods]]:\n"
        "1. [[.strip()]] hands back a copy with the spaces cut off both ends.\n"
        "2. [[.replace()]] hands back a copy with every old piece swapped: `.replace(old, new)`.\n"
        "3. [[.find()]] hands back the place where some text starts, or `-1` when it isn't there. Here `-1` means "
        "*not found*. It is not the last letter.\n"
        "All three match capitals exactly. And like every string method, they hand back something new. Catch it."
    ),
    introduces=["attr:strip", "attr:replace", "attr:find"],
    example=(
        'tag = "  Rust Ward  "\n'
        "tag = tag.strip()\n"
        'tag = tag.replace("Rust", "Moon")\n'
        "print(tag)\n"
        'print(tag.find("Ward"))\n'
        'print(tag.find("ward"))\n'
    ),
    example_output="Moon Ward\n5\n-1",
    names=["note", "spot"],
    predict=dict(
        q="Before you press Run, look at this smaller program. What will it print?",
        code='room = "Greenroom"\nprint(room.find("room"))\nprint(room.find("Room"))\n',
        choices=["5\n-1", "5\n5", "6\n-1", "5\nm"],
        answer=0,
        explain=(
            "`room` starts at place 5: G is 0. `\"Room\"` with a capital R is not in `Greenroom`, so `.find` hands "
            "back -1, which means not found."
        ),
    ),
    starter=NOTE_STARTER,
    checkpoints=[
        dict(
            id="strip-the-note",
            text="Cut the spaces off both ends of `note`, and keep the copy in `note`: change the `note = note` "
                 "line under comment 1 to `note = note.strip()`.",
            dictated=True,
            hints=[
                "Read what it printed: `[  It's a compass.  ]`. The brackets show spaces at both ends.",
                "`\"  hi  \".strip()` hands back `hi`. Catch it with `=`, or the copy is gone.",
                "Write `" + STRIP_LINE + "` in place of the `note = note` line under comment 1.",
            ],
            checks=[STRIP_CHECK],
            pass_line="Mar'tu: Tidier. Still wrong.",
        ),
        dict(
            id="swap-the-word",
            text="Make `note` say `Ley Clock` where it says `compass`.",
            dictated=False,
            hints=[
                "The swap is a method too. It needs two things in its brackets: the old words first, then the new "
                "ones.",
                "`\"Rust Ward\".replace(\"Rust\", \"Moon\")` hands back `Moon Ward`. Catch it with `=`, the same as "
                "the strip.",
                "Write `" + SWAP_LINE + "` in place of the `note = note` line under comment 2.",
            ],
            checks=[SWAP_CHECK],
            pass_line="Mar'tu: Thank you.",
        ),
        dict(
            id="find-a-rune",
            text="Make `spot` hold the place where `\"Ley\"` starts in `note`, found with `.find`.",
            dictated=False,
            hints=[
                "`.find` hands back a place, counted from 0. Ask `note` where `\"Ley\"` starts.",
                "`\"Moon Ward\".find(\"Ward\")` is 5. `.find(\"ward\")` is -1: a small w is not there. -1 means not "
                "found.",
                "Write `" + FIND_LINE + "` in place of `spot = 0`.",
            ],
            checks=[FIND_CHECK],
            pass_line="Mar'tu: Place 7. A rune found by its place. Good.",
        ),
    ],
    solution=NOTE_SOLUTION,
    partials=[_note(STRIP_LINE), _note(STRIP_LINE, SWAP_LINE)],
    assemble=dict(
        lines=[f'note = "{NOTE_TEXT}"', STRIP_LINE, SWAP_LINE, 'print("[" + note + "]")', FIND_LINE, "print(spot)"],
        distractors=["note.strip()", 'note = note.replace("Compass", "Ley Clock")', 'spot = note.find("ley")'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Three tools",
            text=(
                "```text\n\"  It's a compass.  \"\n  .strip()\n\"It's a compass.\"\n  .replace(...)\n"
                "\"It's a Ley Clock.\"\n  .find(\"Ley\")\n7\n```"
            ),
        ),
        dict(
            angle="everyday",
            text=(
                "Strip is trimming the ragged edges off a page. Replace is crossing out a word and writing a new "
                "one. Find is running your finger along the line until you reach the word, and counting the steps."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `note = note.strip()`.\n2. `note = note.replace(old, new)`, old words first.\n3. "
                "`note.find(\"Ley\")` counts from 0. Not there? -1."
            ),
        ),
    ],
    bonus=dict(
        by="mar-tu",
        title="Any sign",
        text=(
            "The greenroom sign again. Below the prints, write `sign = \"Greenroom, Interior\"`. Then make `word` "
            "the word before the comma, for any sign: let `.find(\",\")` count to the comma for you."
        ),
        hints=[
            "`sign.find(\",\")` hands back the comma's place. A slice `[:n]` stops just before place n, so it "
            "stops right before the comma, wherever it is.",
            "Write `sign = \"Greenroom, Interior\"`, then `word = sign[:sign.find(\",\")]`, below the prints.",
        ],
        checks=[ANY_SIGN_CHECK],
        solution=NOTE_SOLUTION + ANY_SIGN_LINES,
    ),
    takeaway="`.strip()` trims the ends, `.replace(old, new)` swaps, `.find(x)` gives a place or -1 for not found.",
    wrong_answers=[
        dict(why="the starter", code=NOTE_STARTER, fails_at=1, message_contains="note = note.strip()"),
        dict(why="stripped, then nothing kept it", code=_note("note.strip()"), fails_at=1,
             message_contains="nothing kept it"),
        dict(why="no (): the method itself, then glued into the print (TypeError)", code=_note("note = note.strip"),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="no () (with step 2 not started yet)", code=_note("note = note.strip").replace(
            'print("[" + note + "]")\n', "").replace("print(spot)\n", ""), fails_at=1, message_contains="Add `()`"),
        dict(why="strip(note) as if it were a function (NameError)", code=_note("note = strip(note)"), fails_at=0,
             message_contains="'strip' is not defined"),
        dict(why="every space taken out", code=_note('note = note.replace(" ", "")'), fails_at=1,
             message_contains="every space"),
        dict(why="typed by hand", code=_note('note = "It\'s a compass."'), fails_at=1,
             message_contains="With another note"),
        dict(why="a counted slice, [2:-2]: fits two spaces a side only", code=_note("note = note[2:-2]"), fails_at=1,
             message_contains="a space was left"),
        dict(why="double spaces swapped out: an odd space is left", code=_note('note = note.replace("  ", "")'),
             fails_at=1, message_contains="a space was left"),
        dict(why="the Example's name: tag holds the stripped copy", code=_note("tag = note.strip()"), fails_at=1,
             message_contains="`tag` holds it"),
        dict(why="replace with no (), the print taken out: step 1 kept, then note holds the order (step 2's slip)",
             code=_note(STRIP_LINE, "note = note.replace").replace('print("[" + note + "]")\n', ""), fails_at=2,
             message_contains="Add `()` after `.replace`, with the old and new words inside"),
        dict(why="replace with no (), the print kept: glued into the print (TypeError on the student's own Run)",
             code=_note(STRIP_LINE, "note = note.replace"), fails_at=0, message_contains="can only concatenate str"),
        dict(why="replace with a capital C: nothing matches", code=_note(STRIP_LINE,
                                                                       'note = note.replace("Compass", "Ley Clock")'),
             fails_at=2, message_contains="small c"),
        dict(why="replace with the words the wrong way round", code=_note(STRIP_LINE,
                                                                          'note = note.replace("Ley Clock", "compass")'),
             fails_at=2, message_contains="old words first"),
        dict(why="swapped, then nothing kept it", code=_note(STRIP_LINE, 'note.replace("compass", "Ley Clock")'),
             fails_at=2, message_contains="nothing kept it"),
        dict(why="ley clock in small letters", code=_note(STRIP_LINE, 'note = note.replace("compass", "ley clock")'),
             fails_at=2, message_contains="two capitals"),
        dict(why="typed: It's a Ley Clock.", code=_note(STRIP_LINE, 'note = "It\'s a Ley Clock."'), fails_at=2,
             message_contains="With another note"),
        dict(why="find with a small l: -1, not found", code=_note(STRIP_LINE, SWAP_LINE, 'spot = note.find("ley")'),
             fails_at=3, message_contains="-1 means not found"),
        dict(why="find the swapped-out word: -1, not found", code=_note(STRIP_LINE, SWAP_LINE,
                                                                        'spot = note.find("compass")'),
             fails_at=3, message_contains="not the last letter"),
        dict(why="in for find: True or False", code=_note(STRIP_LINE, SWAP_LINE, 'spot = "Ley" in note'), fails_at=3,
             message_contains="True or False"),
        dict(why="the letter at the place, not the place", code=_note(STRIP_LINE, SWAP_LINE, "spot = note[7]"),
             fails_at=3, message_contains="a letter, not a place"),
        dict(why="typed 7", code=_note(STRIP_LINE, SWAP_LINE, "spot = 7"), fails_at=3, message_contains="it stayed 7"),
    ],
    notes=(
        meta(starter_level="S2", path="SC", skills="string-methods", solo="false", dictates="1",
             foreign_names="tag,room", stages="P,M") + "\n"
        "8B-05 (absorbs 8B-06 find-a-rune). Intro attr:strip, attr:replace, attr:find. Predict: `.find` on "
        "Greenroom, a hit (5) and a capital miss (-1). CP1 [D] strip Lucky's note `\"  It's a compass.  \"` (CMB with "
        "`\"   A compass? No. \"`, 3 spaces in front and 1 behind, so a counted `[2:-2]` or a `\"  \"` swap leaves a space; "
        "the Example's `tag` holding the copy is named). "
        "CP2 [ND] replace compass with Ley Clock (CMB with the same other note); Mar'tu: 'Thank you.' The "
        "capital C (case-sensitive), the words the wrong way round and the copy not kept each get a message. "
        "CP3 [ND] find-a-rune: `.find` gives an index (7), or -1 when the text is not there; -1 read as a place is "
        "named ('not the last letter'), and so are `in` (a True / False) and `note[7]` (a letter). Every check "
        "stays true as later steps finish (CP1 undoes the swap before it compares). The starter has a placeholder "
        "`note = note` under comments 1 and 2 (like `spot = 0` for step 3), so each step has a line to change. A "
        "`.replace` with no `()` is named at step 2 (step 1 is read from the watched history, so it stays green). "
        "Side quest (Mar'tu, 'Any sign', the find-the-comma bonus): `word = sign[:sign.find(\",\")]` on the greenroom "
        "sign, rerun on `\"Pantry, Interior\"` (the comma at place 6, not 9), so a counted `[0:9]` fails. Phone "
        "width: the solution's replace line is 43 characters (editor code only; see the file header)."
    ),
)

# ---- 8B-07 f-strings ---------------------------------------------------------------------------------------------

LINE_PLUS = 'line = name + ": " + str(mana)'
LINE_F = 'line = f"{name}: {mana}"'
FUEL_F = 'fuel = f"Ore: {days} days"'
FUEL_PLUS = 'fuel = "Ore: " + str(days) + " days"'


def _fstr(s1=LINE_PLUS, s2=FUEL_F):
    return (
        'name = "Bomb Shell"\n'
        "mana = 24\n"
        "# 1. Rewrite as an f-string:\n"
        + s1 + "\nprint(line)\n"
        "\n"
        "days = 7\n"
        "# 2. Rewrite with + and str():\n"
        + s2 + "\nprint(fuel)\n"
    )


FSTR_STARTER = _fstr()
FSTR_SOLUTION = _fstr(LINE_F, FUEL_PLUS)

FSTR_CHECK = chk(
    "line is an f-string that prints the same, for other values too",
    r'''
_n, _m = globals().get('name'), globals().get('mana')
assert _tn(_n) == 'str' and _tn(_m) == 'int', 'Keep the lines `name = "Bomb Shell"` and `mana = 24` from the starter.'
assert 'line' in globals(), 'Keep the variable `line` from the starter.'
_v = globals()['line']
_as = _assigns('line')
assert not (_tn(_v) == 'str' and '{' in _v and '}' in _v), (
    'Put an `f` right before the first quote mark. Without it, the braces print as they are.')
assert _as and _tn(_as[-1].value) == 'JoinedStr', (
    'Write the `line =` line as an f-string: an `f` before the quote marks, and each variable inside `{ }`.')
assert _v == _n + ': ' + _str(_m), (
    'Keep the same words and spaces around the variables, so it prints what it printed before: a colon, then one '
    'space.')
_vals = {'name': 'Pell', 'mana': 9}
_ns, _rows, _err, _miss = _rerun(_vals)
assert not _miss, "Keep the lines `name = ...` and `mana = ...` from the starter, so Mar'tu's check can try others."
assert not _err, 'Make it work for other values too. Python stopped: ' + _err + '.' + _tried(_vals)
assert _ns.get('line') == 'Pell: 9', (
    'Put each variable inside `{ }`, so the line follows them. With other values, it did not.' + _tried(_vals))
''',
)

PLUS_CHECK = chk(
    "fuel is glued with + and str(), and prints the same, for another number too",
    r'''
_d = globals().get('days')
assert _tn(_d) == 'int', 'Keep the line `days = 7` from the starter.'
assert 'fuel' in globals(), 'Keep the variable `fuel` from the starter.'
_v = globals()['fuel']
_as = _assigns('fuel')
assert not (_as and _tn(_as[-1].value) == 'JoinedStr'), (
    'Write `fuel` with `+` and `str()` this time: no `f`, and no `{ }`.')
_noadd = bool(_as and _tn(_as[-1].value) != 'Constant'
              and not _any(_tn(_x) == 'BinOp' and _tn(_x.op) == 'Add' for _x in _ast.walk(_as[-1].value)))
assert not (_noadd and _v == 'Ore: ' + _str(_d) + ' days'), (
    'Glue the pieces with `+` and `str(days)` this time, the way the campaign does. That works, but this step '
    'practices `+` and `str(days)`.')
assert not _noadd, 'Glue the pieces with `+` and `str(days)` this time, the way the campaign does.'
assert not (_tn(_v) == 'str' and '{' in _v), (
    'Glue `days` in with `+` and `str(days)`. Without an `f`, the braces print as they are.')
assert not (_tn(_v) == 'str' and 'days days' in _v), _QUOTES + ' Glue in `str(days)`, with no quotes round `days`.'
assert _v == 'Ore: ' + _str(_d) + ' days', (
    'Keep the same words and spaces, so it prints what it printed before, like `Ore: 7 days`.')
_ns, _rows, _err, _miss = _rerun({'days': 3})
assert not _miss, "Keep the line `days = 7` from the starter, so Mar'tu's check can try another number."
assert not _err, 'Make it work for another number too. Python stopped: ' + _err + '.' + _tried({'days': 3})
assert _ns.get('fuel') == 'Ore: 3 days', (
    'Glue in `days` itself with `str(days)`, so the line follows it. With another number, it did not.'
    + _tried({'days': 3}))
''',
)

F_STRINGS = dict(
    id="f-strings",
    title="f-strings",
    martu=(
        "Two ways to build the same line. The campaign glues with `+` and `str()`:\n"
        "```python\nname + \": \" + str(mana) + \" mana\"\n```\n"
        "An [[f-string]] puts an `f` right before the quotes, and each variable inside `{ }`:\n"
        "```python\nf\"{name}: {mana} mana\"\n```\n"
        "With Lucky's sheet, both give `Lucky: 26 mana`. Inside `{ }`, Python looks in the variable, and no "
        "`str()` is needed.\n"
        "The campaign uses `+` and `str()`, so read both. Write whichever you like. Then put your own hero in "
        "`name`, any name in quotes."
    ),
    introduces=["node:FString"],
    example='cart = "Oats"\nbags = 3\nprint(cart + " x" + str(bags))\nprint(f"{cart} x{bags}")\n',
    example_output="Oats x3\nOats x3",
    names=["line", "name", "mana", "fuel", "days"],
    predict=dict(
        q="Before you press Run, look at this smaller program. What will it print?",
        code='name = "Lucky"\nmana = 26\nprint("{name}: {mana}")\nprint(f"{name}: {mana}")\n',
        choices=[
            "{name}: {mana}\nLucky: 26",
            "Lucky: 26\nLucky: 26",
            "{name}: {mana}\n{name}: {mana}",
            "Lucky: 26\n{name}: {mana}",
        ],
        answer=0,
        explain=(
            "Without the `f`, the braces are just more letters, so Python prints them as they are. With the `f`, "
            "Python looks inside each variable."
        ),
    ),
    pair_talk="Tell your partner why `mana` needs `str()` in the `+` line, but not inside the f-string.",
    starter=FSTR_STARTER,
    checkpoints=[
        dict(
            id="plus-to-f-string",
            text="Rewrite the `line =` line as an f-string. It must print exactly what it printed before.",
            dictated=False,
            hints=[
                "Start with `f\"`. Every piece goes inside one pair of quotes, and each variable goes inside `{ }`.",
                "From the example: `cart + \" x\" + str(bags)` became `f\"{cart} x{bags}\"`. The text between the "
                "variables stays as it is.",
                "Write `" + LINE_F + "` in place of the `line =` line.",
            ],
            checks=[FSTR_CHECK],
            pass_line="Bomb Shell: Same line. Fewer pieces.",
        ),
        dict(
            id="f-string-to-plus",
            text="Rewrite the `fuel =` line with `+` and `str()`, with no f-string. It must print the same.",
            dictated=False,
            hints=[
                "Glue three pieces with `+`: the text before `{days}`, the number made into text, and the text "
                "after it.",
                "`f\"{cart} x{bags}\"` became `cart + \" x\" + str(bags)`. A number needs `str()` before `+` can "
                "glue it to text.",
                "Write `" + FUEL_PLUS + "` in place of the `fuel =` line.",
            ],
            checks=[PLUS_CHECK],
            pass_line="Mar'tu: Now you read the campaign's way and your own. Both say the same thing, yes?",
        ),
    ],
    solution=FSTR_SOLUTION,
    partials=[_fstr(LINE_F)],
    assemble=dict(
        lines=['name = "Bomb Shell"', "mana = 24", LINE_F, "print(line)", "days = 7", FUEL_PLUS, "print(fuel)"],
        distractors=['line = "{name}: {mana}"', 'fuel = "Ore: " + days + " days"', 'line = f"{name}:{mana}"'],
    ),
    another_way=[
        dict(
            angle="picture",
            label="The same line, twice",
            text=(
                "```text\nname + \": \" + str(mana)\n  |      |       |\n  v      v       v\n"
                "f\"{name}: {mana}\"\n```\nEach glued piece moves inside one pair of quotes."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. Write `f\"` and the closing `\"`.\n2. Copy the text pieces in, in order.\n3. Where a variable "
                "was glued in, write its name inside `{ }`. Drop every `+` and `str()`."
            ),
        ),
        dict(
            angle="from the campaign",
            label="Why read both?",
            text=(
                "The campaign's `cast_spell` says `caster[\"character_name\"] + \" doesn't have enough mana to cast \" "
                "+ spell_name + \".\"`. Read it like a sentence: text, a value, text, a value. An f-string says the "
                "same thing in one pair of quotes."
            ),
        ),
    ],
    takeaway="`f\"{name}: {mana}\"` and `name + \": \" + str(mana)` give the same text. Read both, write either.",
    wrong_answers=[
        dict(why="the starter: still glued with +", code=FSTR_STARTER, fails_at=1, message_contains="as an f-string"),
        dict(why="an f-string without the f: the braces print", code=_fstr('line = "{name}: {mana}"'), fails_at=1,
             message_contains="Put an `f`"),
        dict(why="a closing brace missing (SyntaxError)", code=_fstr('line = f"{name}: {mana"'), fails_at=0,
             message_contains="expecting '}'"),
        dict(why="a brace too many (SyntaxError)", code=_fstr('line = f"{name}}: {mana}"'), fails_at=0,
             message_contains="single '}' is not allowed"),
        dict(why="the space after the colon lost", code=_fstr('line = f"{name}:{mana}"'), fails_at=1,
             message_contains="same words and spaces"),
        dict(why="typed in an f-string: no variables", code=_fstr('line = f"Bomb Shell: 24"'), fails_at=1,
             message_contains="With other values"),
        dict(why="still an f-string in step 2", code=_fstr(LINE_F, 'fuel = f"Ore: {days} days"'), fails_at=2,
             message_contains="this time"),
        dict(why="+ with a number and no str() (TypeError)", code=_fstr(LINE_F, 'fuel = "Ore: " + days + " days"'),
             fails_at=0, message_contains="can only concatenate str"),
        dict(why="braces with no f", code=_fstr(LINE_F, 'fuel = "Ore: {days} days"'), fails_at=2,
             message_contains="braces print"),
        dict(why="the variable's name in quotes", code=_fstr(LINE_F, 'fuel = "Ore: " + str("days") + " days"'),
             fails_at=2, message_contains="no quotes round"),
        dict(why="the spaces lost", code=_fstr(LINE_F, 'fuel = "Ore:" + str(days) + "days"'), fails_at=2,
             message_contains="same words and spaces"),
        dict(why="typed by hand: Ore: 7 days", code=_fstr(LINE_F, 'fuel = "Ore: 7 days"'), fails_at=2,
             message_contains="With another number"),
        dict(why="% formatting: the same text, but no + and str() to read", code=_fstr(LINE_F, 'fuel = "Ore: %d days" % days'),
             fails_at=2, message_contains="the way the campaign does"),
        dict(why=".format(): the same text, but no + and str() to read",
             code=_fstr(LINE_F, 'fuel = "Ore: {} days".format(days)'), fails_at=2,
             message_contains="the way the campaign does"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="fstring-read", solo="false", dictates="",
             foreign_names="cart,bags", stages="P,I,M") + "\n"
        "8B-07. Intro node:FString. The Learn pane shows both of the spec's forms, `name + \": \" + str(mana) + \" "
        "mana\"` and `f\"{name}: {mana} mana\"` (33 and 22 characters in the fences); the starter's line drops "
        "` mana` to stay under 36. Predict: a missing f prints `{name}` as it is. CP1 [ND] rewrite a `+ str()` line "
        "as an f-string (the last `line =` must be a JoinedStr, `_uses('node:FString')` in spirit) with identical "
        "output; CMB with `name = \"Pell\"`, `mana = 9` stops a typed f-string. CP2 [ND] translate an f-string back "
        "to `+ str()`: no `str()` is the TypeError row, and the last `fuel =` must glue with `+` (`%` and `.format()` "
        "give the same text and are told 'That works, but this step practices `+` and `str(days)`'). Mar'tu invites "
        "the student's own hero in `name` (any name passes: the check reads the student's own `name` and reruns with "
        "Pell). WT: 'The campaign uses `+` and `str()`, so read both' (Q12: "
        "read both, write either), as the 'from the campaign' angle with `cast_spell`'s prompt line. Python 3.13 "
        "messages verified: `f\"{name: {mana\"`-style -> \"f-string: expecting '}'\", an extra brace -> "
        "\"f-string: single '}' is not allowed\"."
    ),
)

# ---- 8B-08 whats-in-it-for-me (echo) ---------------------------------------------------------------------------

REPLY_BODY = (
    "    tidy = request.strip()\n"
    "    tidy = tidy.capitalize()\n"
    "    ask = \" What's in it for me?\"\n"
    "    return tidy + ask\n"
)
CLIP_BODY = (
    "    words = sentence.split()\n"
    '    short = " ".join(words[:3])\n'
    '    return short + "."\n'
)
REPLY_FOREIGN = "shout,order,bits"   # the meta's foreign_names, read by _why too
REPLY_CALLS = ('# Ask Lucky anything:\nprint(lucky_reply("  carry this  "))\nprint(clip("Latch is stuck again"))\n'
               'print(lucky_reply(" open it"))\nprint(clip("Optic dim"))\n')


def _reply(reply="    pass\n", clip="    pass\n", calls=REPLY_CALLS, tail=""):
    return "def lucky_reply(request):\n" + reply + "\n\ndef clip(sentence):\n" + clip + "\n\n" + calls + tail


REPLY_STARTER = _reply()
REPLY_SOLUTION = _reply(REPLY_BODY, CLIP_BODY)
MARTU_REPLY = (
    "\n\ndef martu_reply(sentence):\n"
    "    short = clip(sentence)\n"
    '    return short[:-1] + ", yes?"\n'
    "\n\n"
    'said = "Hold the line now"\n'
    "print(martu_reply(said))\n"
)

REPLY_CHECK = chk(
    "lucky_reply hands back the tidy request, then Lucky's question, for fresh requests",
    r'''
_f = _need_def('lucky_reply', 1, 'def lucky_reply(request):')
_ASK = " What's in it for me?"
_res = []
for _a in __CASES__:
    _p, _v, _e = _call(_f, _a)
    _ev = _called('lucky_reply', (_a,), 'it should hand back `' + _a.strip().capitalize() + _ASK + '`')
    assert not _e, _why('lucky_reply', _e, __FOREIGN__) + _ev
    _res.append((_a, _p, _v, _ev))
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    'Build the reply from `request`, so it changes with what is asked. (Mar\'tu\'s check called `lucky_reply` with '
    'two other requests, only inside the check: both replies were the same.)')
for _a, _p, _v, _ev in _res:
    if _v == _a.strip().capitalize() + _ASK:
        continue
    assert not (_v is None and _p), (
        'Hand back the reply with `return`, not `print`. `lucky_reply` printed it, then handed back `None`.' + _ev)
    assert _v is not None, 'End `lucky_reply` with `return`, so it hands the reply back. It handed back `None`.' + _ev
    assert not _is_method(_v), (
        'Add `()` after `.' + _v.__name__ + '`. Without them, `lucky_reply` hands back the order, not the text. Python '
        'runs a method only with `()`.' + _ev)
    assert _tn(_v) == 'str', 'Hand back text: the tidy request, then the question.' + _ev
    assert "what's in it for me?" in _v.lower(), (
        "Glue Lucky's question on the end: ` What's in it for me?`, with a space in front." + _ev)
    assert _v.endswith("What's in it for me?"), (
        "Write Lucky's question exactly, at the very end: ` What's in it for me?`, with a capital W." + _ev)
    assert _v.endswith(_ASK), "Put one space before `What's`, so the question doesn't touch the request." + _ev
    _head, _core = _v[:-_len(_ASK)], _a.strip()
    _used = [_n.attr for _n in _ast.walk(_fdef('lucky_reply')) if _tn(_n) == 'Attribute']
    assert not (_head != _head.strip() and _bare('strip')), (
        'Catch the stripped copy with `=`: `request.strip()` on its own line makes a copy, then nothing keeps it.'
        + _ev)
    assert _head == _head.strip(), 'Strip the spaces off both ends of `request` first, with `.strip()`.' + _ev
    assert not (_head == _core.lower() and 'capitalize' not in _used), (
        'Give the request a capital first letter with `.capitalize()`, after `.strip()`.' + _ev)
    assert _head != _core.lower(), (
        'Strip first, then capitalize. With the spaces still on, `.capitalize()` meets a space, and nothing gets a '
        'capital.' + _ev)
    assert _head != _core, 'Capitalize the request: `.capitalize()` makes the first letter big and the rest small.' + _ev
    assert _head != _core.title(), (
        'That is `.title()`: a capital on every word. `.capitalize()` makes only the first letter big.' + _ev)
    assert False, "Hand back the request, stripped and capitalized, then ` What's in it for me?`." + _ev
''',
    CASES=["  bring the rope  ", "FETCH THE GLUG"],
    FOREIGN=REPLY_FOREIGN.split(","),
)

CLIP_CHECK = chk(
    "clip hands back the first three words and a period, for fresh sentences, short ones too",
    r'''
_f = _need_def('clip', 1, 'def clip(sentence):')
_res = []
for _a in __CASES__:
    _p, _v, _e = _call(_f, _a)
    _want = ' '.join(_a.split()[:3]) + '.'
    _ev = _called('clip', (_a,), 'it should hand back `' + _want + '`')
    assert not ('IndexError' in _e and _len(_a.split()) < 3), (
        'Inside `clip`, Python stopped: ' + _e + '. Make `clip` work for short sentences too: a slice like `[:3]` '
        'takes what is there, but a place past the end stops Python.' + _ev)
    assert not _e, _why('clip', _e, __FOREIGN__) + _ev
    _res.append((_a, _p, _v, _ev, _want))
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    'Build the short version from `sentence`, so it changes with what is handed in. (Mar\'tu\'s check called `clip` '
    'with two other sentences, only inside the check: both gave the same text.)')
for _a, _p, _v, _ev, _want in _res:
    if _v == _want:
        continue
    assert not (_v is None and _p), (
        'Hand back the short version with `return`, not `print`. `clip` printed it, then handed back `None`.' + _ev)
    assert _v is not None, 'End `clip` with `return`, so it hands the short version back. It handed back `None`.' + _ev
    assert _tn(_v) != 'list', 'Join the words back into text with `" ".join(...)`, then glue on the period.' + _ev
    assert _tn(_v) == 'str', 'Hand back text: three words and a period.' + _ev
    assert not _v.startswith('['), (
        'That is the list written out, brackets and all. Join the words with `" ".join(...)`.' + _ev)
    assert _v.endswith('.'), 'Glue a period on the end, with `+ "."`.' + _ev
    _body, _w = _v[:-1], _a.split()
    assert not (_len(_w) > 2 and _body == ' '.join(_w[:2])), (
        'That is two words. A slice leaves its end out, so `[:3]` takes three: places 0, 1 and 2.' + _ev)
    assert not (_len(_w) > 3 and _body == ' '.join(_w[:4])), 'That is four words. `[:3]` takes three: places 0, 1 and 2.' + _ev
    assert _body != ''.join(_w[:3]), 'Put a space between the quotes before `.join`. The words touch.' + _ev
    assert _body != _a[:3], 'That is three letters. Split `sentence` into words first, then take three of them.' + _ev
    assert _body != ' '.join(_w[1:4]), 'Start at place 0: the first word is place 0.' + _ev
    assert False, 'Hand back the first three words of `sentence`, joined with spaces, then a period.' + _ev
''',
    CASES=["Moving out before the burst", "Optic is dim again tonight", "Shield up"],
    FOREIGN=REPLY_FOREIGN.split(","),
)

MARTU_REPLY_CHECK = chk(
    "martu_reply clips the sentence and ends with , yes?",
    r'''
_f = globals().get('martu_reply')
assert _B.callable(_f), 'Write a function named `martu_reply`, with one parameter, `sentence`.'
for _a in ('Optic is dim again tonight', 'Moving out before the burst'):
    _p, _v, _e = _call(_f, _a)
    _want = ' '.join(_a.split()[:3]) + ', yes?'
    _ev = _called('martu_reply', (_a,), 'it should hand back `' + _want + '`')
    assert not _e, _why('martu_reply', _e, __FOREIGN__) + _ev
    assert _v == _want, 'Hand back the clipped sentence with its period cut off, then `, yes?`.' + _ev
_fd = _fdef('martu_reply')
assert _any(_tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'clip' for _n in _ast.walk(_fd)), (
    'Call `clip` inside `martu_reply`, so the clipping is done in one place.')
''',
    FOREIGN=REPLY_FOREIGN.split(","),
)

WHATS_IN_IT_FOR_ME = dict(
    id="whats-in-it-for-me",
    title="What's in it for me?",
    martu=(
        "Make two of your own. Lucky answers every request the same way. Bomb Shell answers in three words, then "
        "stops.\n"
        "1. `lucky_reply(request)` hands back the request, stripped and capitalized, then ` What's in it for me?`.\n"
        "2. `clip(sentence)` hands back the first three words of `sentence`, joined with spaces, then a period.\n"
        "You know every piece already. Ask Lucky anything you like in the last lines."
    ),
    example=(
        "def shout(order):\n"
        "    order = order.strip()\n"
        "    order = order.upper()\n"
        '    return order + "!"\n'
        "\n"
        'print(shout("  run  "))\n'
    ),
    example_output="RUN!",
    names=["lucky_reply", "request", "clip", "sentence"],
    pick='"  guard the door  "',
    starter=REPLY_STARTER,
    checkpoints=[
        dict(
            id="lucky-reply",
            text="Finish `lucky_reply(request)`: hand back `request` stripped and capitalized, then "
                 "` What's in it for me?`.",
            dictated=False,
            hints=[
                "Two methods on `request`, in order: strip first, then capitalize. Then glue the question on the "
                "end with `+`, space and all.",
                "Same shape as the Example's `shout`: strip, then a method, then `return order + \"!\"`. Here the "
                "method is `.capitalize()`, and the end is Lucky's question.",
                "Strip first, or `.capitalize()` meets a space. Keep Lucky's question in double quotes: it has an "
                "apostrophe.",
                "Write `tidy = request.strip()`, then `tidy = tidy.capitalize()`, then hand back "
                "`tidy + \" What's in it for me?\"`.",
            ],
            checks=[REPLY_CHECK],
            pass_line="Mar'tu: What's in it for you, Lucky? Existing.",
        ),
        dict(
            id="clip",
            text="Finish `clip(sentence)`: hand back its first three words, joined with spaces, then a period. A "
                 "shorter sentence keeps all its words.",
            dictated=False,
            hints=[
                "Split `sentence` into words, take the first three with a slice, join them back, then glue on "
                "`\".\"`.",
                "`[\"a\", \"b\", \"c\", \"d\"][:3]` is `['a', 'b', 'c']`. A short list never breaks it: "
                "`[\"a\", \"b\"][:3]` is `['a', 'b']`.",
                "```python\nbits = [\"a\", \"b\", \"c\", \"d\"]\nprint(\"-\".join(bits[:2]))\n``` shows `a-b`: slice "
                "first, then join.",
                "Write `words = sentence.split()`, then `short = \" \".join(words[:3])`, then "
                "`return short + \".\"`.",
            ],
            checks=[CLIP_CHECK],
            pass_line="Bomb Shell: Three words. Done.",
        ),
    ],
    solution=REPLY_SOLUTION,
    partials=[_reply(REPLY_BODY)],
    assemble=dict(
        lines=["def lucky_reply(request):"] + REPLY_BODY.rstrip("\n").split("\n") + ["def clip(sentence):"]
        + CLIP_BODY.rstrip("\n").split("\n") + ['print(lucky_reply("  carry this  "))', 'print(clip("Latch is stuck again"))',
                                                  'print(lucky_reply(" open it"))', 'print(clip("Optic dim"))'],
        distractors=["    tidy = request.capitalize().strip()", '    short = words.join(" ")', "    return words[:3]"],
    ),
    another_way=[
        dict(
            angle="picture",
            label="Two pipelines",
            text=(
                "```text\n\"  carry this  \"\n  .strip()\n\"carry this\"\n  .capitalize()\n\"Carry this\"\n"
                "  + ask\n\"Carry this What's ...\"\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`clip`:\n1. `sentence.split()`: a list of words.\n2. `[:3]`: the first three, or fewer.\n"
                "3. `\" \".join(...)`: back to text.\n4. `+ \".\"`: Bomb Shell's full stop."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Lucky never says yes without asking his question. Bomb Shell never says a fourth word. Each function "
                "is one hero's habit, written once and used for any line."
            ),
        ),
    ],
    bonus=dict(
        by="mar-tu",
        title="Mar'tu's turn",
        text=(
            "Write `martu_reply(sentence)`: call `clip`, cut its period off with `[:-1]`, and glue on `, yes?`. "
            "`martu_reply(\"Optic is dim again tonight\")` should hand back `Optic is dim, yes?`."
        ),
        hints=[
            "`[:-1]` is every letter but the last: `\"Glug.\"[:-1]` is `Glug`.",
            "Write `short = clip(sentence)`, then `return short[:-1] + \", yes?\"`.",
        ],
        checks=[MARTU_REPLY_CHECK],
        solution=REPLY_SOLUTION + MARTU_REPLY,
    ),
    takeaway="Strip, capitalize, glue; split, slice, join: two string functions that work on any text.",
    wrong_answers=[
        dict(why="the starter: pass", code=REPLY_STARTER, fails_at=1, message_contains="handed back `None`"),
        dict(why="print for return", code=_reply(REPLY_BODY.replace("    return tidy + ask", "    print(tidy + ask)")),
             fails_at=1, message_contains="not `print`"),
        dict(why="no strip", code=_reply("    tidy = request.capitalize()\n    return tidy + \" What's in it for me?\"\n"),
             fails_at=1, message_contains="Strip the spaces"),
        dict(why="the strip made, then nothing kept it",
             code=_reply("    request.strip()\n    tidy = request.capitalize()\n"
                         "    return tidy + \" What's in it for me?\"\n"), fails_at=1, message_contains="nothing keeps it"),
        dict(why="capitalize before strip: it meets a space first",
             code=_reply("    tidy = request.capitalize().strip()\n    return tidy + \" What's in it for me?\"\n"),
             fails_at=1, message_contains="Strip first, then capitalize"),
        dict(why="no capitalize", code=_reply("    tidy = request.strip()\n    return tidy + \" What's in it for me?\"\n"),
             fails_at=1, message_contains="after `.strip()`"),
        dict(why=".title() for .capitalize()",
             code=_reply("    tidy = request.strip().title()\n    return tidy + \" What's in it for me?\"\n"), fails_at=1,
             message_contains="`.title()`"),
        dict(why="no space before What's", code=_reply(REPLY_BODY.replace('" What', '"What')), fails_at=1,
             message_contains="one space before"),
        dict(why="the question in small letters", code=_reply(REPLY_BODY.replace("What's", "what's")), fails_at=1,
             message_contains="capital W"),
        dict(why="the question left off", code=_reply("    return request.strip().capitalize()\n"), fails_at=1,
             message_contains="Glue Lucky's question"),
        dict(why="an apostrophe inside single quotes (SyntaxError)",
             code=_reply(REPLY_BODY.replace("\" What's in it for me?\"", "' What's in it for me?'")), fails_at=0,
             message_contains="unterminated string literal"),
        dict(why="typed: the starter call's own answer", code=_reply("    return \"Carry this What's in it for me?\"\n"),
             fails_at=1, message_contains="both replies were the same"),
        dict(why="clip not started (the partial)", code=_reply(REPLY_BODY), fails_at=2, message_contains="handed back `None`"),
        dict(why="clip: a slice one short, [:2]", code=_reply(REPLY_BODY, CLIP_BODY.replace("[:3]", "[:2]")), fails_at=2,
             message_contains="two words"),
        dict(why="clip: three words read by place: the bottom call clip(\"Optic dim\") stops the student's own Run",
             code=_reply(REPLY_BODY, "    words = sentence.split()\n"
                                     '    short = words[0] + " " + words[1] + " " + words[2]\n'
                                     '    return short + "."\n'), fails_at=0, message_contains="list index out of range"),
        dict(why="clip: three words read by place, the short bottom call taken out: the check's short sentence meets it",
             code=_reply(REPLY_BODY, "    words = sentence.split()\n"
                                     '    short = words[0] + " " + words[1] + " " + words[2]\n'
                                     '    return short + "."\n',
                         calls=REPLY_CALLS.replace('print(clip("Optic dim"))\n', "")), fails_at=2,
             message_contains="short sentences"),
        dict(why="clip: the example's order for sentence (the calls taken out: _why)",
             code=_reply(REPLY_BODY, CLIP_BODY.replace("sentence.split()", "order.split()"), calls=""), fails_at=2,
             message_contains="`order` comes from Mar'tu's example. The parameter of `clip` is `sentence`."),
        dict(why="lucky_reply: a near-miss of the parameter, reqest (the calls taken out: _why)",
             code=_reply(REPLY_BODY.replace("request.strip()", "reqest.strip()"), CLIP_BODY, calls=""), fails_at=1,
             message_contains="You wrote `reqest`. Python matches names letter for letter."),
        dict(why="clip: join called the wrong way round (AttributeError)",
             code=_reply(REPLY_BODY, CLIP_BODY.replace('" ".join(words[:3])', 'words[:3].join(" ")')), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
        dict(why="clip: the list handed back, not text", code=_reply(REPLY_BODY, "    return sentence.split()[:3]\n"),
             fails_at=2, message_contains="Join the words back"),
        dict(why="clip: the list written out with str()",
             code=_reply(REPLY_BODY, "    words = sentence.split()\n    return str(words[:3]) + \".\"\n"), fails_at=2,
             message_contains="brackets and all"),
        dict(why="clip: three letters, not three words", code=_reply(REPLY_BODY, '    return sentence[:3] + "."\n'),
             fails_at=2, message_contains="three letters"),
        dict(why="clip: no period", code=_reply(REPLY_BODY, CLIP_BODY.replace('short + "."', "short")), fails_at=2,
             message_contains="Glue a period"),
        dict(why="clip: empty glue", code=_reply(REPLY_BODY, CLIP_BODY.replace('" ".join', '"".join')), fails_at=2,
             message_contains="The words touch"),
        dict(why="clip: typed", code=_reply(REPLY_BODY, '    return "Latch is stuck."\n'), fails_at=2,
             message_contains="both gave the same text"),
    ],
    notes=(
        meta(starter_level="S1", path="SC", skills="string-methods,split-join,func-make", solo="false", dictates="",
             foreign_names=REPLY_FOREIGN, par='("  bring the rope  ",),("FETCH THE GLUG",); clip: two fresh '
             'sentences and the short "Shield up"', echo="the printed lucky_reply line (pass_line is the static "
             "fallback)", df="pick") + "\n"
        "8B-08 (Mk, S1 signature only). CP1 [ND] `lucky_reply(request)`: the stripped, capitalized request plus "
        "`\" What's in it for me?\"`. CP2 [ND] `clip(sentence)`: Bomb Shell's version, the first three words then a "
        "period. Checks: PAR (two fresh requests; three fresh sentences, one of them only two words long, so an "
        "index past the end of the split is caught kindly); RET. The bottom calls: the student's 'Ask Lucky anything' "
        "pair first (the echo reads the printed reply), then `lucky_reply(\" open it\")` and `clip(\"Optic dim\")`, so a "
        "typed answer shows it breaks and a short sentence runs on the student's own screen (three words read by "
        "place stops there with an IndexError; with that call taken out, the check's own short sentence names it). "
        "`_why` explains an error inside either function or the bonus (`order` from the example, `reqest`). Hints: "
        "lucky-reply's middle rungs show the Example's `shout` shape, then 'strip first' with the apostrophe note; "
        "clip's show a normal `[:3]` before the short-list case, then `\"-\".join(bits[:2])` (slice first, then join). "
        "Any request text passes in the bottom calls (lint e): no check reads them. Messages describe a reply and never show it (2.11). Echo spot (2.11): the site "
        "reads the printed reply aloud, deadpan, through the blocklist with the class switch; the schema has no echo "
        "field yet, so the pass line is the privacy-safe static fallback. DF: Mar'tu's pick for the request. BQ "
        "(combining two functions): `martu_reply` adds `, yes?` to a clipped sentence, cutting the period with "
        "`[:-1]`."
    ),
)

# ---- 8B-09 broken-spell-8b ---------------------------------------------------------------------------------------

B_NOTE_BAD = "note = note.lower"
B_NOTE_GOOD = "note = note.lower()"
B_JOIN_BAD = 'print(words.join(" "))'
B_JOIN_GOOD = 'print(" ".join(words))'
B_LAST_BAD = "print(parts[3])"
B_LAST_GOOD = "print(parts[-1])"
B_CALM_BAD = "calm.lower()"
B_CALM_GOOD = "calm = calm.lower()"


def _broken(note=B_NOTE_BAD, join=B_JOIN_BAD, last=B_LAST_BAD, calm=B_CALM_BAD):
    return (
        "# 1. Shows: The clock is red.\n"
        'note = "THE CLOCK IS RED."\n'
        + note + "\n"
        "note = note.capitalize()\n"
        "print(note)\n"
        "\n"
        "# 2. Shows: Barrier's holding.\n"
        "words = [\"Barrier's\", \"holding.\"]\n"
        + join + "\n"
        "\n"
        "# 3. Shows the last word: now\n"
        'report = "Shield up now"\n'
        "parts = report.split()\n"
        + last + "\n"
        "\n"
        "# 4. Shows: steady, now.\n"
        'calm = "STEADY, NOW."\n'
        + calm + "\n"
        "print(calm)\n"
    )


BROKEN_STARTER = _broken()
BROKEN_SOLUTION = _broken(B_NOTE_GOOD, B_JOIN_GOOD, B_LAST_GOOD, B_CALM_GOOD)
_ALL_GOOD = dict(note=B_NOTE_GOOD, join=B_JOIN_GOOD, last=B_LAST_GOOD, calm=B_CALM_GOOD)


def _mend(**changes):
    return _broken(**{**_ALL_GOOD, **changes})


B_NOTE_CHECK = chk(
    "note is the tidy copy, for another note too",
    r'''
_o = _first_lit('note')
assert _tn(_o) == 'str', 'Keep the line `note = "THE CLOCK IS RED."` from the starter.'
assert globals().get('note') == _o.lower().capitalize(), (
    'Mend line 3 so `note` holds a lower-case copy: call `.lower` with `()`.')
_o2 = 'SHIELD UP NOW.'
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err and _ns.get('note') == 'Shield up now.', (
    'Make the copy from `note` itself, so it follows. With another note, it did not.' + _tried({'note': _o2}))
_low = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
        and _n.func.attr == 'lower' and _tn(_n.func.value) == 'Name' and _n.func.value.id == 'note']
assert _low, (
    'Mend line 3 rather than taking `.lower` out: give it its `()`. The note still prints right, because '
    '`.capitalize()` lowers the rest, but this step practices the `()`.')
''',
)

B_JOIN_CHECK = chk(
    "the words print glued with a space, for another list too",
    r'''
_wd = globals().get('words')
assert _tn(_wd) == 'list', 'Keep the list `words` from the starter.'
assert ' '.join(_wd) in _lines(), (
    'Mend line 9 so it prints the words with a space between: ask the glue, `" "`, to `.join` them.')
_o = ['Optic', 'dim', 'tonight.']
_ns, _rows, _err, _miss = _rerun({'words': _o})
assert not _err and 'Optic dim tonight.' in _rows, (
    'Glue the words of `words` with `.join`, so the line follows the list. With three words, it did not.'
    + _tried({'words': _o}))
_glue = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
         and _n.func.attr == 'join' and not (_tn(_n.func.value) == 'Name' and _n.func.value.id == 'words')]
assert _glue, (
    'Mend the join on line 9 rather than printing another way: ask the glue, `" "`, to `.join(words)`. This step '
    'practices which way round `.join` goes.')
''',
)

B_LAST_CHECK = chk(
    "the report's last word prints, for another report too",
    r'''
_rep = globals().get('report')
assert _tn(_rep) == 'str' and _rep.split(), 'Keep the line `report = "Shield up now"` from the starter.'
assert _rep.split()[-1] in _lines(), (
    'Mend line 14 so it prints the last word. The list has 3 words, at places 0, 1 and 2.')
_o = 'Optic dims fast'
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _err and 'fast' in _rows, (
    'Print a word from `parts`, so the line follows the report. With another report, it did not.'
    + _tried({'report': _o}))
''',
)

B_CALM_CHECK = chk(
    "calm keeps its lower-case copy, for other text too",
    r'''
_o = _first_lit('calm')
assert _tn(_o) == 'str', 'Keep the line `calm = "STEADY, NOW."` from the starter.'
_c = globals().get('calm')
if _c != _o.lower():
    assert not (_c == _o and _o.lower() in _lines()), (
        'Keep the copy in `calm`: start line 18 with `calm = `. The print showed it, but `calm` still holds capitals.')
    assert False, ('Mend line 18: `calm.lower()` makes a copy, then nothing keeps it. Put it back in `calm` with '
                   '`calm = `.')
assert _o.lower() in _lines(), 'Print `calm` after it changes, so the quiet copy shows.'
_o2 = 'HOLD THE LINE.'
_ns, _rows, _err, _miss = _rerun({'calm': _o2})
assert not _err and _ns.get('calm') == 'hold the line.', (
    'Make the copy from `calm` itself, so it follows. With other text, it did not.' + _tried({'calm': _o2}))
''',
)

BROKEN_SPELL_8B = dict(
    id="broken-spell-8b",
    title="Broken spell",
    martu=(
        "Four lines, four bugs. Three are loud: Python stops and names a line. One is quiet: the program runs, and "
        "prints the wrong thing.\n"
        "Read the last line of Python's message first. Sometimes the slip is one line above the line it names. "
        "When Python stops complaining, compare what it printed with the comment above each part."
    ),
    names=["note", "words", "parts", "calm"],
    pair_talk=(
        "You may hunt these bugs together. One of you reads Python's last line out loud; the other "
        "points at the line it names. Each of you mends it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-the-method",
            text="Mend line 3 so `note` holds a lower-case copy of the note.",
            dictated=False,
            hints=[
                "Read Python's last line: `'builtin_function_or_method' object has no attribute 'capitalize'`. It "
                "names line 4.",
                "On line 4, `note` holds the order, not the text. Line 3 put it there: `.lower` with nothing after "
                "it is an order that never ran.",
                "A method runs only with `()`: `cry.lower` is the method, `cry.lower()` is the copy it makes.",
                "Write `" + B_NOTE_GOOD + "` on line 3.",
            ],
            checks=[B_NOTE_CHECK],
            pass_line="Mar'tu: One loud bug down. Python got further, yes?",
        ),
        dict(
            id="mend-the-join",
            text="Mend line 9 so it prints `Barrier's holding.`",
            dictated=False,
            hints=[
                "Read Python's last line: `'list' object has no attribute 'join'`.",
                "A list can't join itself. `.join` belongs to the glue, the text that goes between the words.",
                "`\"-\".join([\"rope\", \"salt\"])` gives `rope-salt`: the glue first, then the list in the brackets.",
                "Write `" + B_JOIN_GOOD + "` on line 9.",
            ],
            checks=[B_JOIN_CHECK],
            pass_line="Gearshift: Barrier's holding.",
        ),
        dict(
            id="mend-the-index",
            text="Mend line 14 so it prints the last word, `now`.",
            dictated=False,
            hints=[
                "Read Python's last line: `IndexError: list index out of range`.",
                "`report.split()` hands back 3 words, at places 0, 1 and 2. Place 3 is past the end.",
                "`[-1]` is always the last item, however long the list is.",
                "Write `" + B_LAST_GOOD + "` on line 14.",
            ],
            checks=[B_LAST_CHECK],
            pass_line="Mar'tu: Three loud bugs down. Now the quiet one. Read what it printed.",
        ),
        dict(
            id="mend-the-copy",
            text="Mend line 18 so `calm` keeps its lower-case copy.",
            dictated=False,
            hints=[
                "Read what it printed at the bottom: `STEADY, NOW.`, still loud. The comment says it should be quiet.",
                "Line 18 makes a lower-case copy. Nothing catches it, so `calm` never changes.",
                "Catch a method's copy with `=`: `cry = cry.lower()`.",
                "Write `" + B_CALM_GOOD + "` on line 18.",
            ],
            checks=[B_CALM_CHECK],
            pass_line="Oogrish: steady, now. Four bugs, four mends. You read the output, not just the errors.",
        ),
    ],
    solution=BROKEN_SOLUTION,
    assemble=dict(
        lines=[line for line in BROKEN_SOLUTION.split("\n") if line and not line.startswith("#")],
        distractors=[B_NOTE_BAD, B_JOIN_BAD, B_CALM_BAD],
    ),
    another_way=[
        dict(
            angle="step-by-step",
            label="Which bug first?",
            text=(
                "1. Run. Line 4 stops it, but the slip is on line 3. Mend it.\n2. Run again. A new message is good "
                "news: Python got further. Line 9 stops it next.\n3. Then line 14.\n4. Now nothing stops. Read the "
                "output against each comment: the last part is still loud."
            ),
        ),
        dict(
            angle="picture",
            label="Four bugs, four clues",
            text=(
                "```text\nline 3   .lower      -> line 4\n                        stops\nline 9   words.join  -> stops\n"
                "line 14  parts[3]    -> stops\nline 18  not kept    -> loud\n```"
            ),
        ),
        dict(angle="shorter", text="Call methods with `()`. Ask the glue to `.join`. Count from 0. Catch every copy."),
    ],
    takeaway="Call a method with `()`, ask the glue to join, count places from 0, and catch every copy with `=`.",
    wrong_answers=[
        dict(why="the starter: .lower with no () (AttributeError on line 4)", code=BROKEN_STARTER, fails_at=0,
             message_contains="has no attribute 'capitalize'"),
        dict(why="bug 1 mended, the join still the wrong way round", code=_broken(B_NOTE_GOOD), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
        dict(why="bugs 1-2 mended, the index still past the end", code=_broken(B_NOTE_GOOD, B_JOIN_GOOD), fails_at=0,
             message_contains="list index out of range"),
        dict(why="the three loud bugs mended, the quiet copy not kept", code=_broken(B_NOTE_GOOD, B_JOIN_GOOD,
                                                                                     B_LAST_GOOD),
             fails_at=4, message_contains="nothing keeps it"),
        dict(why="bug 1 typed in", code=_mend(note='note = "the clock is red."'), fails_at=1,
             message_contains="With another note"),
        dict(why="bug 1 hidden, not mended: line 3 taken out (capitalize lowers the rest anyway)",
             code=BROKEN_SOLUTION.replace(B_NOTE_GOOD + "\n", ""), fails_at=1, message_contains="practices the `()`"),
        dict(why="bug 1 hidden, not mended: line 3 made note = note", code=_mend(note="note = note"), fails_at=1,
             message_contains="practices the `()`"),
        dict(why="bug 2 hidden, not mended: print(*words) prints them with spaces, no join",
             code=_mend(join="print(*words)"), fails_at=2, message_contains="which way round"),
        dict(why="bug 2: empty glue", code=_mend(join='print("".join(words))'), fails_at=2,
             message_contains="space between"),
        dict(why="bug 2 typed in", code=_mend(join='print("Barrier\'s holding.")'), fails_at=2,
             message_contains="With three words"),
        dict(why="bug 2: two words glued by place", code=_mend(join='print(words[0] + " " + words[1])'), fails_at=2,
             message_contains="With three words"),
        dict(why="bug 3: one place too far again", code=_mend(last="print(parts[4])"), fails_at=0,
             message_contains="list index out of range"),
        dict(why="bug 3: off by one the other way, parts[1]", code=_mend(last="print(parts[1])"), fails_at=3,
             message_contains="places 0, 1 and 2"),
        dict(why="bug 3 typed in", code=_mend(last='print("now")'), fails_at=3, message_contains="With another report"),
        dict(why="bug 4: printed, never kept", code=_mend(calm="print(calm.lower())"), fails_at=4,
             message_contains="The print showed it"),
        dict(why="bug 4 typed in", code=_mend(calm='calm = "steady, now."'), fails_at=4,
             message_contains="With other text"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="string-methods,split-join,read-traceback", solo="false",
             dictates="", foreign_names="cry") + "\n"
        "8B-09. The spec's four bugs, one checkpoint each, in the order Python's messages arrive (verified, Python "
        "3.13): `note.lower` with no `()` (the campaign shape: the next line's `.capitalize()` fails with "
        "\"'builtin_function_or_method' object has no attribute 'capitalize'\", so the slip is one line above the "
        "line Python names), `words.join(\" \")` (the AttributeError row), an index past the end of a split result "
        "(`parts[3]` on three words: IndexError), then the quiet one, `calm.lower()` never stored. A crash fails "
        "every checkpoint, so the three loud bugs fail at 0 and there are no partials (as Units 4 and 6's broken "
        "spells). Every checkpoint reruns with other values, so a typed mend is caught; a bug hidden rather than mended is named "
        "(line 3 taken out or made `note = note`, which still prints right because `.capitalize()` lowers the rest; "
        "`print(*words)` or a loop for the join); `parts[2]` and `parts[-1]` "
        "both pass (the rerun report has three words too). Rung 0 is 'Read Python's last line' for the loud bugs and "
        "'Read what it printed' for the quiet one. Pairs allowed; each student mends on their own screen."
    ),
)

# ---- 8B-S solo-8b --------------------------------------------------------------------------------------------------

SOLO_B_CALL = 'print(whisper("  HUSH. LISTEN.  "))'
SOLO_B_TAIL = "\n\n# This should show: hush. listen.\n" + SOLO_B_CALL + "\n"
SOLO_B_STRIP = "    line = line.strip()"
SOLO_B_BAD = "    line.lower()"
SOLO_B_GOOD = "    line = line.lower()"
SOLO_B_FOREIGN = "cry"   # the meta's foreign_names, read by the lean _why too


def _solo_b(body=SOLO_B_STRIP + "\n" + SOLO_B_BAD + "\n    return line", tail=SOLO_B_TAIL):
    return "def whisper(line):\n" + body + "\n" + tail


SOLO_B_STARTER = _solo_b()
SOLO_B_SOLUTION = _solo_b(SOLO_B_STRIP + "\n" + SOLO_B_GOOD + "\n    return line")

SOLO_B_CHECK = chk(
    "whisper hands back the line stripped and in small letters, for fresh lines",
    r'''
_f = _need_def('whisper', 1, 'def whisper(line):')
_res = []
for _a in __CASES__:
    _p, _v, _e = _call(_f, _a)
    _ev = _called('whisper', (_a,))
    assert not _e, _why('whisper', _e, __FOREIGN__, True) + _ev
    _res.append((_a, _p, _v, _ev))
for _a, _p, _v, _ev in _res:
    _want = _a.strip().lower()
    if _v == _want:
        continue
    assert not (_v is None and _p), '`whisper` prints, but hands back `None`.' + _ev
    assert _v is not None, '`whisper` hands back `None`.' + _ev
    assert not _is_method(_v), '`whisper` hands back the order, not text: a method with no `()`.' + _ev
    assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
        '`whisper` hands back the same text for every line.' + _ev)
    assert _v != _a, (
        'The copies are made, then nothing keeps them: `whisper` hands back the line as it came in.' + _ev)
    assert not (_v == _a.strip() and _bare('lower')), (
        'The lower-case copy is made, then nothing keeps it: `whisper` hands back the line with its spaces cut, '
        'still in capitals.' + _ev)
    assert _v != _a.strip(), '`whisper` hands back the line with its spaces cut, still in capitals.' + _ev
    assert not (_tn(_v) == 'str' and _v != _want and _v.strip() == _want), (
        '`whisper` hands back small letters, but the spaces at the ends are still on.' + _ev)
    assert not (_tn(_v) == 'str' and _v.strip() == _a.strip().upper()), (
        '`whisper` hands back capitals, not small letters.' + _ev)
    assert False, '`whisper` does not hand back the line stripped and in small letters.' + _ev
''',
    CASES=["  Moon Step ", "RUST WARD, LIT.   "],
    FOREIGN=SOLO_B_FOREIGN.split(","),
)

SOLO_8B = dict(
    id="solo-8b",
    title="Show Mar'tu",
    martu=(
        "One quiet bug, just for you. Python won't stop, so read what it prints. `whisper` should hand back any line "
        "with the spaces cut off its ends, in small letters, yes?"
    ),
    solo=True,
    explainer="lean",
    names=["whisper", "line"],
    starter=SOLO_B_STARTER,
    checkpoints=[
        dict(
            id="keep-the-copy",
            text="Make `whisper(line)` hand back `line` stripped and in small letters, for any line.",
            dictated=False,
            hints=[
                "Read what it printed: the spaces are gone, but it is still in capitals. The comment says it should "
                "be small.",
                "Two lines make a copy of `line`. Which copy is kept?",
                "A method hands back a new string: `cry = cry.lower()` keeps it.",
                "Write `line = line.lower()` on line 3.",
            ],
            checks=[SOLO_B_CHECK],
            pass_line="Mar'tu: You did that alone. I saw. On your map: ✓ a method's copy, caught.",
        ),
    ],
    solution=SOLO_B_SOLUTION,
    assemble=dict(
        lines=["def whisper(line):", SOLO_B_STRIP, SOLO_B_GOOD, "    return line", SOLO_B_CALL],
        distractors=[SOLO_B_BAD, "    line.strip()", "    line = lower(line)"],
    ),
    another_way=[
        dict(angle="shorter", text="A method's copy is lost unless something catches it with `=` or hands it back."),
        dict(
            angle="step-by-step",
            text=(
                "1. `line = line.strip()` makes a copy with no end spaces, and keeps it. 2. `line.lower()` makes a "
                "quiet copy. 3. Nothing keeps that one. 4. `return line` hands back the stripped, loud line."
            ),
        ),
    ],
    takeaway="On your own: a method hands back a new string, so keep it: `line = line.lower()`.",
    wrong_answers=[
        dict(why="the starter: the lower-case copy is made, then nothing keeps it", code=SOLO_B_STARTER, fails_at=1,
             message_contains="nothing keeps it: `whisper` hands back the line with its spaces cut"),
        dict(why="both steps bare: nothing keeps either copy",
             code=_solo_b("    line.strip()\n" + SOLO_B_BAD + "\n    return line"), fails_at=1,
             message_contains="hands back the line as it came in"),
        dict(why="strip only: line 3 taken out", code=_solo_b(SOLO_B_STRIP + "\n    return line"), fails_at=1,
             message_contains="still in capitals"),
        dict(why="line 2 made bare while mending line 3: the spaces are left",
             code=_solo_b("    line.strip()\n" + SOLO_B_GOOD + "\n    return line"), fails_at=1,
             message_contains="spaces at the ends are still on"),
        dict(why="line 2 taken out: the spaces are left", code=_solo_b(SOLO_B_GOOD + "\n    return line"), fails_at=1,
             message_contains="spaces at the ends are still on"),
        dict(why="typed: the call's own answer", code=_solo_b('    return "hush. listen."'), fails_at=1,
             message_contains="same text for every line"),
        dict(why="printed, not handed back", code=_solo_b(SOLO_B_STRIP + "\n    print(line.lower())"), fails_at=1,
             message_contains="prints, but hands back"),
        dict(why="printed the copy, handed back the stripped line",
             code=_solo_b(SOLO_B_STRIP + "\n    print(line.lower())\n    return line"), fails_at=1,
             message_contains="still in capitals"),
        dict(why="no (): the method handed back", code=_solo_b(SOLO_B_STRIP + "\n    return line.lower"), fails_at=1,
             message_contains="a method with no `()`"),
        dict(why="lower(line) as if it were a function (NameError on the student's own Run)",
             code=_solo_b(SOLO_B_STRIP + "\n    line = lower(line)\n    return line"), fails_at=0,
             message_contains="'lower' is not defined"),
        dict(why="lower(line), the call taken out: the check's own call meets it (the lean _why)",
             code=_solo_b(SOLO_B_STRIP + "\n    line = lower(line)\n    return line", tail=""), fails_at=1,
             message_contains="`lower` is a method, used here like a function."),
        dict(why=".upper() for .lower()", code=_solo_b(SOLO_B_STRIP + "\n    line = line.upper()\n    return line"),
             fails_at=1, message_contains="capitals, not small letters"),
        dict(why="seat B's slip shape: join called the wrong way round (AttributeError)",
             code=_solo_b('    words = line.lower().split()\n    return words.join(" ")'), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
    ],
    notes=(
        meta(starter_level="S4", path="SC", skills="string-methods", solo="true", dictates="",
             foreign_names=SOLO_B_FOREIGN, par='("  Moon Step ",),("RUST WARD, LIT.   ",)', seat_b='words.join(" ") (AttributeError; the mend is '
             '" ".join(words))') + "\n"
        "SOLO, one bug (C6), explainer='lean'. Seat A (and anyone solo) gets the quiet slip in two steps, so the "
        "student must read which line drops the copy: `line = line.strip()` is kept, then `line.lower()` is never "
        "stored, and `return line` hands back the stripped line still in capitals. Python never stops; the call "
        "prints `HUSH. LISTEN.` where its comment says `hush. listen.` (rung 0: 'Read what it printed'; rung 1 asks "
        "which of the two copies is kept). The mend is line 3, `line = line.lower()`; `return line.lower()` passes "
        "too. PAR with two fresh lines with end spaces, so a typed answer, both steps bare, strip only, the spaces "
        "left (line 2 made bare or taken out), print for return, no `()`, `lower(line)` and `.upper()` each fail "
        "with their own lean message. Lean messages name the slip and keep the evidence bracket, with no fix; an "
        "error inside `whisper` gets the lean `_why` (the unknown name and the parameter, no fix). Seat B would get "
        "`words.join(\" \")` once pair mode ships; its AttributeError is proven here by a wrong answer. Recorded, "
        "never blocking, never shown to a partner."
    ),
)

LESSON_8B = dict(
    kind="lesson",
    id="words-that-change-shape",
    title="Words That Change Shape",
    minutes=32,
    summary=(
        "String methods that hand back new text: capitals, chains, split and join, strip, replace and find, and "
        "f-strings. Then two functions of your own."
    ),
    notes=(
        "Lesson 8B (SC). Preceded by 8b-remembers. Exactly one SOLO (solo-8b, lean). Non-dictated checkpoints: "
        "8B-01, 8B-03 CP2-4, 8B-05 CP2-3, 8B-07 CP1-2, 8B-08 CP1-2, 8B-09 (all four mends), 8B-S (lint g); "
        "dictated: 8B-02, 8B-03 CP1, 8B-05 CP1. 8B-04 is absorbed into 8B-03 (join-them-back) and 8B-06 "
        "into 8B-05 (find-a-rune). Campaign callbacks: program-dialogue-options (8B-02, Lucky's box), "
        "program-dialogue-prompt (8B-01's 'from the campaign' angle), hold-the-barrier (8B-07's angle). Echo spot: "
        "8B-08. 32 minutes, as the spec."
    ),
    exercises=[LOUD_AND_QUIET, CHAIN_THE_SPELLS, SPLIT_THE_CLIPPED, STRIP_AND_REPLACE, F_STRINGS, WHATS_IN_IT_FOR_ME,
               BROKEN_SPELL_8B, SOLO_8B],
)

# =============================================================================================
# Quiz 8B
# =============================================================================================

QUIZ_8B = dict(
    kind="quiz",
    id="words-quiz",
    title="Quiz: Words That Change Shape",
    minutes=8,
    summary=(
        "Eight questions on string methods, split and join, find, f-strings and a function. Retake as often as "
        "you like."
    ),
    notes=(
        "Quiz 8B (SC): 4 predict, 2 bug, 1 mc and 1 fill, in the spec's order (Q1 predict, Q2 predict, Q3 predict, "
        "Q4 bug, Q5 mc, Q6 predict, Q7 fill, Q8 bug). Q7 is a fill on `.title()` (it no longer repeats Q1's "
        "`.lower().capitalize()` line). Q8 is the def/return item (every unit quiz has one from Unit 4 on), now a "
        "missing `return` (`None` printed), unlike solo-8b's copy that is never kept. Code keeps to 36 characters a "
        "line (Q1 is split over three lines for that). Review order: right "
        "answers first (G1 R26). The right choice sits in varied places (the site shuffles too)."
    ),
    questions=[
        dict(
            type="predict",
            id="tidy-chain",
            q="What will this print?",
            code='line = "WHAT IS THE DECAY?"\nline = line.lower().capitalize()\nprint(line)\n',
            choices=["what is the decay?", "What is the decay?", "What Is The Decay?", "WHAT IS THE DECAY?"],
            answer="What is the decay?",
            explain=(
                "Left to right: `.lower()` makes every letter small, then `.capitalize()` makes the first one big. "
                "The line keeps the copy, so it prints `What is the decay?`."
            ),
            notes="Distractors: only .lower(), .title(), the copy not kept.",
        ),
        dict(
            type="predict",
            id="join-and-split",
            q="What will this print?",
            code='print(" ".join(["Shield", "up."]))\nprint("gold,teal".split(","))\n',
            choices=[
                "Shield up.\n['gold', 'teal']",
                "Shieldup.\n['gold', 'teal']",
                "Shield up.\ngold teal",
                "['Shield', 'up.']\n['gold,teal']",
            ],
            answer="Shield up.\n['gold', 'teal']",
            explain=(
                "`\" \".join(...)` glues the list into one text with a space between. `.split(\",\")` cuts at the "
                "comma and hands back a list, so `print` shows its brackets and quotes."
            ),
            notes="Distractors: the glue forgotten, the list read as text, each call the other way round.",
        ),
        dict(
            type="predict",
            id="find-not-there",
            q="What will this print?",
            code='print("EXIT".find("Z"))\n',
            choices=["3", "-1", "T", "ERROR: ValueError"],
            answer="-1",
            explain="There is no Z in EXIT, so `.find` hands back -1: not found. It is not the last place, which is 3.",
            notes="3 and T: -1 read as the last place or the last letter; an error: .index's habit.",
        ),
        dict(
            type="bug",
            id="join-the-glue",
            q="This should print `Latch stuck.` It stops with an AttributeError. Mend it.",
            code='words = ["Latch", "stuck."]\nprint(words.join(" "))\n',
            fix='words = ["Latch", "stuck."]\nprint(" ".join(words))\n',
            expected_output="Latch stuck.",
            explain="A list has no `.join`. Ask the glue instead: `\" \".join(words)` puts a space between the words.",
            notes="The AttributeError row (8B-03 CP4, 8B-09 CP2).",
        ),
        dict(
            type="mc",
            id="fstring-twin",
            q="Which line prints the same as the last line here?",
            code='name = "Lucky"\nmana = 26\nprint(f"{name}: {mana}")\n',
            choices=[
                'print(name + ": " + str(mana))',
                'print("{name}: {mana}")',
                'print(name + ": " + mana)',
                'print("name: " + str(mana))',
            ],
            answer=0,
            why_wrong={
                1: "With no `f`, the braces print as they are: `{name}: {mana}`.",
                2: "Text plus a number is a TypeError: `mana` needs `str()` before `+` can glue it.",
                3: "In quotes, `name` is just the letters n, a, m, e. No quotes means look inside the variable.",
            },
            explain="Both give `Lucky: 26`. The f-string looks inside `{name}` and `{mana}`; the `+` line glues them, with `str()` for the number.",
        ),
        dict(
            type="predict",
            id="strip-and-swap",
            q="What will this print?",
            code='sign = "  EXIT  "\nsign = sign.strip()\nsign = sign.replace("X", "D")\nprint("[" + sign + "]")\n',
            choices=["[EDIT]", "[  EDIT  ]", "[EXIT]", "[  EXIT  ]"],
            answer="[EDIT]",
            explain=(
                "`.strip()` cuts the spaces off both ends, and `.replace(\"X\", \"D\")` swaps the X. Each copy is "
                "caught in `sign`, so the brackets show `EDIT` with no spaces."
            ),
            notes="Distractors: the strip missed, the replace missed, both missed.",
        ),
        dict(
            type="fill",
            id="fill-title",
            q="Fill the blank so this prints `Bomb Shell`.",
            code='print("bomb shell".___())\n',
            answer="title",
            expected_output="Bomb Shell",
            explain="`.title()` gives every word a capital; `.capitalize()` would give `Bomb shell`.",
            notes="A fill on `.title()`, so it no longer repeats Q1's `.lower().capitalize()` line.",
        ),
        dict(
            type="bug",
            id="hand-it-back",
            q="This should print `SHIELD UP.` It prints `None`. Mend it.",
            code='def shout(line):\n    line = line.upper()\n\nprint(shout("shield up."))\n',
            fix='def shout(line):\n    line = line.upper()\n    return line\n\nprint(shout("shield up."))\n',
            expected_output="SHIELD UP.",
            explain=(
                "No `return`, so `shout` hands back `None`: Python's word for nothing came back. End it with "
                "`return line`."
            ),
            notes=(
                "The def/return item: the missing `return` shape (spec Q8 asked for a forgotten reassignment; that "
                "shape is now solo-8b's, so the quiz asks a different decision)."
            ),
        ),
    ],
)

ITEMS = [REMEMBERS_8A, LESSON_8A, REMEMBERS_8B, LESSON_8B, QUIZ_8B]
