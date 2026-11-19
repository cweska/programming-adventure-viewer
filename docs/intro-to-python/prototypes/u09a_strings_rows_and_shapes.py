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

Terminology (2.9, and docs/intro-to-python/design/plain-language-guide.md, the plain-language pass): "variable"
(Mar'tu may still say "box"), "function", "parameter", "returns" / "hands back", "method" (new here: a tool you use
with a dot; the dot asks the text to do a job and it hands back a new copy), "position" (never "place") for an index,
"parentheses" / "square brackets" / "curly braces", "period" (never "full stop"), "fix" and "mistake" (debug steps
say "Fix line N": the site reads fix or mend), "changes to match" (never "follows"). Every new idea gets plain words,
an analogy (ruler, quoting a poem, a printed page, quotes inside quotes and the Enter key, a tape diagram, speaking to
someone by name, two function machines in a row, sentence strips, Find and Replace, Mad Libs) and a tiny example in
Mar'tu's first paragraph. The quotes sentence word for word (QUOTES_RULE).

Help ladder as fields (FORMAT.md, the Unit 2 fix pass, as Units 4 to 7): hints[0] Where to look, the middle hints Teach
me (a tiny example with other names, listed in foreign_names), the last hint Show me how: the step's own line in
backticks, whose start up to its first `(` or `=` is Start me off (always a start Mar'tu's version uses; no hint 1 is a
"Start like this"). 3 to 5 hints per checkpoint, then another_way (2 to 4 angles), assemble (More structure) on every
make / write exercise, and the solution (Compare). In debug steps hints[0] is the guide's reading routine (the box's
title in the Console, then Python's last line; for a quiet bug: what the Console shows). Both SOLO items are explainer="lean" with lean check messages (the slip and the
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
  _tried(values) / _called(name, args)  the labelled evidence, last: "Mar'tu tested your code with a test value,
                `sign = "Storeroom, Interior"`." (a test number, a test list; test values, ... and ... for two) /
                "Mar'tu tested your function with a test call, `make_bar(3, 5)`: its blocks should be `▓▓▓░░`."
                (the reconcile pass: u09b's `_ev` and u09c's `_tried` / `_called` say it the same way)
  _why(name, err, foreign, lean)  (as Units 3 and 7) every `_call` error path in every function check (8A-07,
                8B-02, 8B-08 and its bonus, 8B-S): one lead sentence, the teacher's "Inside `tidy_line`, Python
                stopped: `<err>`.", plus one kind sentence (an example's name: "`said` comes from Mar'tu's example:
                the parameter of `tidy_line` is `raw`."; a near-miss: "You wrote `curent`, but the parameters of
                `make_bar` are `current` and `maximum`: Python matches names letter for letter."; a name used before
                the line that makes it: "`said` is used before the line that makes it: Python runs a function from
                the top down, so make `said` first."), then the test call alone (`_crash_ev`: no answer it should
                give, since the run never got that far; guide 4.3.5, three sentences). foreign is the exercise meta's foreign_names; lean (8B-S) names
                the unknown name and the parameter, never the fix.
Messages follow the plain-language guide 4.3: what happened to the student's line first, then the one thing to try,
then the labelled evidence at the end, with no brackets. A method with no `()` reads "`.upper` has no `()`, so the
method never ran: `line` holds the method itself, not text. Add `()` after `.upper`." The first `None` message in
each lesson (8A: make_bar's, 8B: tidy_line's) glosses it: "`None`, Python's word for nothing: no line in it hands
anything back" (the guide's gloss, word for word in u09b and u09c). A rerun
that stops reads "With another sign, your code stopped. Python's last line: `<err>`." SOLO messages name the mistake
and keep the evidence, with no fix. SOLO pass lines start "You did that on your own." (the site swaps it after help)
and promise no skills map. Check data uses invented Tor names only (Pell, Brakka, Moss, Ivo, Glug, Storeroom, Moon Step, Rust Ward); a student's own
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
    _its = ['`' + _k + ' = ' + _q(_v) + '`' for _k, _v in _vals.items()]
    if _len(_its) == 1:
        _v = _list(_vals.values())[0]
        _what = {'int': 'a test number', 'list': 'a test list'}.get(_tn(_v), 'a test value')
        return " Mar'tu tested your code with " + _what + ', ' + _its[0] + '.'
    return " Mar'tu tested your code with test values, " + ' and '.join(_its) + '.'
def _called(_name, _args, _end=''):
    return (" Mar'tu tested your function with a test call, `" + _name + '(' + ', '.join([_q(_a) for _a in _args])
            + ')`' + (': ' + _end if _end else '') + '.')
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
        assert not _near, 'Your function is named `' + _near[0] + '`, but this step needs `' + _name + '`. Python matches names letter for letter.'
        assert False, 'The line `' + _sig + '` is missing or changed. Put it back as it was at the start.'
    assert _B.callable(globals().get(_name)), (
        'A later line put a value in `' + _name + '` with `=`, so it is not a function now. Keep `' + _name + '` a function.')
    _n = _len(_fd.args.args)
    assert _n == _nparams, ('The `def` line of `' + _name + '` has ' + _str(_n) + ' in its parentheses. It needs '
                            + ('one parameter' if _nparams == 1 else _str(_nparams) + ' parameters') + ', like `' + _sig
                            + '`.')
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
    # The parameters as a clause ("the parameters of `make_bar` are `current` and `maximum`"), so a reason and the
    # names stay one sentence.
    _pw = (((('the parameter of `' + _name + '` is ') if _len(_ps) == 1 else ('the parameters of `' + _name + '` are '))
            + _names(_ps)) if _ps else '')
    _then = (': ' + _pw + '.') if _pw else '.'
    _say = ''
    if _k == 'UnboundLocalError' and _x:
        _say = (('`' + _x + '` is used before the line that makes it.') if _lean else
                ('`' + _x + '` is used before the line that makes it: Python runs a function from the top down, so '
                 'make `' + _x + '` first.'))
    elif _k == 'NameError' and _x:
        _fo = [_y for _y in _foreign if _y == _x]
        _near = [_p for _p in _ps if _len(_x) >= 2 and _edits(_p.lower(), _x.lower()) <= 2]
        _fo2 = [_y for _y in _foreign if _len(_x) >= 3 and _edits(_y, _x) <= 2]
        if _fo:
            _say = '`' + _x + '` comes from ' + ('an example' if _lean else "Mar'tu's example") + _then
        elif _near:
            _say = (('`' + _x + '` is not a parameter of `' + _name + '`' + _then) if _lean else
                    ('You wrote `' + _x + '`, but ' + _pw + ': Python matches names letter for letter.'))
        elif _fo2:
            _say = '`' + _x + '` looks like `' + _fo2[0] + '` from ' + ('an example' if _lean else "Mar'tu's example") + _then
        elif _x in _METHODS:
            _say = (('`' + _x + '` is a method, used here like a function.') if _lean else
                    ('`' + _x + '` is a method, so it goes after a dot, like `' + (_ps[0] if _ps else 'text') + '.' + _x
                     + '()`.'))
        else:
            _say = '`' + _x + '` is not a name `' + _name + '` knows' + _then
    elif _lean:
        if 'builtin_function_or_method' in _s:
            _say = 'A method is used with no `()`.'
        elif "'list' object has no attribute 'join'" in _s:
            _say = '`.join` is asked of a list.'
    elif _k == 'TypeError':
        if 'NoneType' in _s:
            _say = ("A function it uses hands back `None`, Python's word for nothing. Give that function a "
                    "`return` line.")
        elif 'concatenate' in _s:
            _say = ('A number is glued straight onto text. Make the number text first with `str()`, like `str('
                    + (_ps[0] if _ps else 'n') + ')`.')
        elif 'unsupported operand' in _s and "'str' and 'int'" in _s:
            _say = ('Python does `*` before `-`, so it made the blocks, then tried to take a number away from text. '
                    'Put parentheses around the subtraction, so Python works it out first, like PEMDAS.')
        elif 'does not support item assignment' in _s:
            _say = "You can't change one letter of a string. Build a new string instead."
        elif 'positional argument' in _s:
            _say = ('A call hands over the wrong number of values. Count the values in its parentheses against the '
                    '`def` line.')
    elif _k == 'AttributeError':
        if 'builtin_function_or_method' in _s:
            _say = ('A method name has no `()` after it, so the method never ran: add `()` after the method name.')
        elif "'list' object has no attribute 'join'" in _s:
            _say = 'A list has no `.join`. Ask the glue instead: `" ".join(words)`.'
        elif "'list' object" in _s:
            _say = 'This is a list: `.split()` hands back a list. Text methods work on text, not on a list.'
        elif "'NoneType'" in _s:
            _say = ("A function it uses hands back `None`, Python's word for nothing. Give that function a "
                    "`return` line.")
        elif "'str' object" in _s and _x:
            _say = 'Text has no method `.' + _x + '`. Check the name after the dot, letter for letter.'
    elif _k == 'IndexError':
        _say = 'It asked for a position past the end. Count positions from 0, like a ruler.'
    elif _k == 'RecursionError':
        _say = ('`' + _name + '` calls itself, again and again, so it never stops: end it with a `return` that does '
                'not call it.')
    return 'Inside `' + _name + '`, Python stopped: `' + _err + '`.' + (' ' + _say if _say else '')
def _crash_ev(_ev):
    # After a crash, the test call alone: never the answer it should give (the run never got that far).
    return _ev.split('`: ', 1)[0] + '`.' if '`: ' in _ev else _ev
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
        "Text in quotes is a [[string]]: letters strung together like beads, in order. Each letter has a position, "
        "counted from 0, the same as the items in a list.\n"
        "In this unit you take text apart and build it again. You cut out a piece, put quote marks inside quotes, "
        "and use tools like `.upper()` that hand back a changed copy.\n"
        "You have seen all of this in the campaign: `.lower().capitalize()` tidying the dialogue options, "
        "`\"█\" * caster[\"mana\"]` in the mana bars, and `+ str(...)` gluing numbers into words. Back then it was "
        "somebody else's code. This time it is yours."
    ),
    goals=[
        "Read one letter of a word by its position, cut out a piece with a [[slice]], and count the letters",
        "Explain why one letter of a word can't be changed, and build a new word instead",
        "Put quote marks and new lines inside text",
        "Use text tools (methods) that hand back a new copy, like all capitals, and keep the copy",
        "Cut a sentence into a list of words, glue a list back into one line, and turn the text `\"48\"` into the "
        "number 48",
        "Fill names and numbers into the blanks of a line, like Mad Libs, in two ways: with an f-string, and with "
        "the campaign's `+` and `str()`",
        "Build a status bar for any numbers, like the campaign's mana bars",
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
            "A tool you use with a dot, like `motto.upper()`. The dot asks the text to do a job, and the text hands "
            "back a new copy. The variable doesn't change, so keep the copy with `=`."
        ),
        example="motto = motto.upper()",
    ),
    dict(
        term="immutable",
        aliases=["can't change in place", "cannot change", "unchangeable"],
        plain=(
            "A programmer's word for *can't change*. You can't swap one letter of a string: `tag[0] = \"R\"` is an "
            "error. Build a new string and put it in the variable instead."
        ),
        example='tag = "R" + tag[1:]',
    ),
    dict(
        term="escape mark",
        aliases=["escape marks", "escape", "escapes", "backslash", "new line"],
        plain=(
            "A backslash inside text, with one mark or letter after it. `\\\"` puts a quote mark in the text. `\\n` starts "
            "a new line, like pressing Enter. The backslash itself never shows."
        ),
        example='print("Gold\\nTeal")',
    ),
    dict(
        term=".upper()",
        aliases=["upper()", "upper"],
        plain="Hands back a copy of the text in capital letters. The text in the variable does not change.",
        example='"teal".upper()   # TEAL',
    ),
    dict(
        term=".title()",
        aliases=["title()"],
        plain="Hands back a copy of the text with a capital at the start of every word, like a book title.",
        example='"moon step".title()   # Moon Step',
    ),
    dict(
        term="chain",
        aliases=["chains", "chained", "chaining", "method chain"],
        plain=(
            "Methods one right after another, like `cry.lower().capitalize()`. Python works left to right. Each "
            "method works on the copy the one before it handed back."
        ),
        example="cry.lower().capitalize()",
    ),
    dict(
        term=".split()",
        aliases=["split()", "split"],
        plain=(
            "Cuts text into a list of pieces. With empty parentheses, it cuts at every space. `.split(\", \")` "
            "cuts at each comma and space."
        ),
        example='"Shield up.".split()   # [\'Shield\', \'up.\']',
    ),
    dict(
        term=".join()",
        aliases=["join()", "join"],
        plain=(
            "Glues a list of texts into one text. Ask the glue, not the list: `\" \".join(bits)` puts a space "
            "between the pieces."
        ),
        example='" ".join(["Shield", "up."])',
    ),
    dict(
        term=".strip()",
        aliases=["strip()", "strip"],
        plain=(
            "Hands back a copy with the spaces cut off both ends, like trimming the edges of a page. Spaces "
            "between the words stay."
        ),
        example='"  hi  ".strip()   # hi',
    ),
    dict(
        term=".replace()",
        aliases=["replace()"],
        plain=(
            "Hands back a copy with every old piece swapped for a new one, like Find and Replace in a document: "
            "`.replace(old, new)`. Capitals must match exactly."
        ),
        example='"Rust Ward".replace("Rust", "Moon")',
    ),
    dict(
        term=".find()",
        aliases=["find()"],
        plain=(
            "Hands back the position where some text starts, counted from 0. When the text is not there, it "
            "hands back -1. Here -1 means *not found*. It is not the last letter."
        ),
        example='"EXIT".find("X")   # 1',
    ),
    dict(
        term="f-string",
        aliases=["f-strings", "f string", "f strings"],
        plain=(
            "Text with an `f` right before the quotes. Each `{name}` inside it is a blank, like in Mad Libs: "
            "Python fills it with what the variable holds. No `+` or `str()` is needed."
        ),
        example='f"{hero} has {coins} coins"',
    ),
]

# The party, the chalk wall, and five invented heroes for the LOOP reruns.
ROSTER = ["Oogrish", "Gearshift", "Bomb Shell", "Lucky"]
OTHER_FIVE = ["Pell", "Brakka", "Moss", "Ivo", "Glug"]
EV_FIVE = " Mar'tu tested your code with a test roster of 5 other heroes."

# =============================================================================================
# Mar'tu remembers… (8a-remembers)
# =============================================================================================

REMEMBERS_8A = dict(
    kind="quiz",
    id="8a-remembers",
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from earlier units, before you start on text. Nothing is scored.",
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
            explain=(
                "The stamp `\"#\" * 3` is `\"#\" + \"#\" + \"#\"`, so it makes `###`. Then `str(n)` turns the number 3 "
                "into text, so `+` can glue it on: `### 3`."
            ),
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
            explain="Python uses PEMDAS, like math class: `*` goes before `+`. 3 * 4 is 12, then 2 + 12 is 14.",
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
assert _tn(_r) == 'list', 'The list `roster` is missing or changed. Put it back as it was at the start, with its square brackets.'
assert 'initials' in globals(), 'The line `initials = ""` is missing. Put it back above the loop, as it was at the start.'
_v = globals()['initials']
assert _tn(_v) != 'list', ('`initials` holds a list now. A list is a different thing. Keep `initials` as text: start '
                           'it as `""` and glue each letter on with `+`.')
assert _tn(_v) == 'str', '`initials` is not text now. Start it as `""` and glue each letter on with `+`.'
_kept_none = [_n for _l in _ast.walk(_parsed()) if _tn(_l) == 'For' for _n in _ast.walk(_l)
              if _tn(_n) == 'Expr' and _tn(_n.value) == 'BinOp'
              and _any(_tn(_x) == 'Name' and _x.id in ('initials', 'name') for _x in _ast.walk(_n.value))]
assert not (_v == '' and _kept_none), ('Python glued the letter on, then nothing kept it, so `initials` is still '
                                       'empty. Start the line with `initials = `: `initials = initials + ...`.')
assert _v != '', '`initials` is still empty. Glue a letter onto it inside the loop, in place of `pass`.'
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
        'Your glue line is under the loop, not inside it, so it ran once, for the last name. Indent it four '
        'spaces, so it runs for every name.')
    _reset = [_n for _i in _loops for _n in _ast.walk(_body[_i]) if _tn(_n) == 'Assign' and _sets_initials(_n)
              and _tn(_n.value) == 'Constant' and _n.value.value == '']
    assert not (_len(_r) > 1 and _L == _r[-1][0] and _reset), (
        '`initials = ""` is inside the loop too, so it empties `initials` on every pass, and only the last letter '
        'is left. Keep `initials = ""` above the loop only.')
    assert not (_len(_r) > 1 and _L == _r[-1][0]), (
        '`initials` ended with one letter, from the last name: each pass lost the letters from earlier passes. '
        'Glue onto `initials` with `initials + ...`, like a running total.')
    assert _L != _letters(''.join(_r)), '`initials` got whole names. Glue on one letter from each name, not the whole name.'
    assert _L != ''.join([_n[1] for _n in _r if _len(_n) > 1]), (
        '`initials` got the second letter of each name. Position 1 is the second letter, because counting starts '
        'at 0. Use position 0.')
    assert _L != ''.join([_n[-1] for _n in _r]), (
        '`initials` got the last letter of each name: `[-1]` is the last letter. Use position 0 for the first.')
    assert not (_len(_r) > 1 and _L == _r[0][0] * _len(_r)), (
        "Every pass gave the first hero's letter. Read the letter from `name`, this pass's name.")
    assert _L != ''.join([_n[0] for _n in _r])[::-1], (
        'The letters came out backwards. Glue each new letter on the end, `initials + ...`, so they come in '
        'roster order.')
    assert False, '`initials` does not hold the first letter of each name yet. Make it hold one letter for each name in `roster`, in order.'
assert _any(_tn(_n) == 'For' for _n in _ast.walk(_parsed())), 'The `for` loop is gone. Keep it, so every name is reached.'
_ns, _rows, _err, _miss = _rerun({'roster': __FIVE__})
assert not _miss, "Mar'tu can't test your code with other names: the line `roster = [` is missing or changed. Put it back as it was at the start."
assert not _err, "With another roster, your code stopped. Python's last line: `" + _err + "`." + __EV__
assert _ok(_ns.get('initials'), __FIVE__), (
    'With other heroes, `initials` did not change to match. Build `initials` inside the loop, from each `name`.'
    + __EV__)
''',
    FIVE=OTHER_FIVE,
    EV=EV_FIVE,
)

WORD_CHECK = chk(
    "word holds the word before the comma, for another sign too",
    r'''
_s = _first_lit('sign')
assert _tn(_s) == 'str' and ',' in _s, 'The line `sign = "Greenroom, Interior"` is missing or changed. Put it back as it was at the start.'
assert 'word' in globals(), 'The line `word = ...` is missing or changed. Put it back as it was at the start.'
_w = globals()['word']
assert _tn(_w) == 'str', '`word` is not text now. Make it a piece of `sign`: a slice of text is text too.'
assert _w != '', '`word` is still empty. Slice the word out of `sign` and put it in `word`.'
_at = _s.find(',')
if _w != _s[:_at]:
    assert _w != _s[:_at - 1], (
        "Your slice stops one letter early. The end position is left out, so end on the comma's own position.")
    assert _w != _s[:_at + 1], (
        "Your slice takes the comma too. The end position is left out, so end on the comma's own position.")
    assert _w != _s[1:_at], 'Your slice skips the first letter. The first letter is position 0, not 1, so start at 0.'
    assert _len(_w) != 1, '`word` holds one letter. A slice takes a piece, with a colon: `[start:end]`.'
    assert _w.strip() != _s[_at + 1:].strip(), '`word` holds the word after the comma. This step wants the word before it.'
    assert False, '`word` does not hold the word before the comma yet. Make it a slice of `sign`.'
_ns, _rows, _err, _miss = _rerun({'sign': __OTHER__})
assert not _miss, "Mar'tu can't test your code with another sign: the line `sign = ...` is missing or changed. Put it back as it was at the start."
assert not _err, "With another sign, your code stopped. Python's last line: `" + _err + "`." + _tried({'sign': __OTHER__})
assert _ns.get('word') == __OTHER_WORD__, (
    'With another sign, `word` did not change to match. Slice `word` out of `sign` instead of typing it in.'
    + _tried({'sign': __OTHER__}))
''',
    OTHER=OTHER_SIGN,
    OTHER_WORD="Storeroom",
)

LETTERS_HAVE_PLACES = dict(
    id="letters-have-places",
    title="Letters have positions",
    martu=(
        "Text is letters in a row, like the items in a list. Each letter has a position, counted from 0, the way a "
        "ruler starts at 0. `[0]` is the first letter, and `[-1]` is the last:\n"
        "```text\n T  e  l  e  g  u  n\n 0  1  2  3  4  5  6\n-7 -6 -5 -4 -3 -2 -1\n```\n"
        "`len()` counts the letters: `Telegun` has 7.\n"
        "A [[slice]] copies a piece, like quoting a few words of a poem in English class. `[0:4]` takes positions "
        "0, 1, 2 and 3. The end is left out, the same as with lists. You know this from the chalk wall, my wall of "
        "gap numbers (the hours between bursts), yes?"
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
            "`[0]` is the first letter, T. `[-1]` is the last, n. `len()` counts all 7 letters. The last position "
            "is 6, one less than the count, because counting starts at 0."
        ),
    ),
    pair_talk="Before you see the answer, each of you says what `gun[-1]` shows. Compare, then check.",
    starter=PLACES_STARTER,
    checkpoints=[
        dict(
            id="slice-a-word",
            text="On line 4, change `word = \"\"` so `word` holds the word before the comma. Cut it from `sign` "
                 "with a slice.",
            dictated=False,
            hints=[
                "Look at `sign` on line 1. The comma's position is the number of letters before it. How many "
                "letters does `Greenroom` have?",
                "A slice stops right before its end position:\n```python\ncoat = \"Rust, Ward\"\nprint(coat[0:4])\n```\n"
                "That shows `Rust`. The comma is at position 4, so `[0:4]` stops right before it.",
                "Write `word = sign[0:9]` in place of `word = \"\"`.",
            ],
            checks=[WORD_CHECK],
            pass_line="`word` holds Greenroom. Mar'tu: The room where you four landed in Tor. Nobody knows why, yes?",
        ),
        dict(
            id="build-initials",
            text="On line 17, change `pass` so the loop glues the first letter of each name onto `initials`.",
            dictated=False,
            hints=[
                "Look at the loop on line 16. On each pass, `name` holds one hero's name. Which position holds its "
                "first letter?",
                "Glue onto a text variable on each pass, like a running total:\n```python\nmarks = \"\"\n"
                "for jar in [\"salt\", \"oats\"]:\n    marks = marks + jar[-1]\n```\n`marks` ends as `ts`: the "
                "last letter of each word. You want the first.",
                "Write `initials = initials + name[0]` in place of `pass`, with four spaces in front.",
            ],
            checks=[INITIALS_CHECK],
            pass_line="`initials` holds OGBL, one letter for each hero. Mar'tu: Python did the counting, yes?",
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
                "2. Use that position as the end of the slice. The end is left out, so the comma is too.\n"
                "3. In the loop, `name[0]` is this pass's first letter. Glue it on the end of `initials`."
            ),
        ),
        dict(
            angle="English class",
            label="From English class",
            text=(
                "*Seven* is how many, and *seventh* is which one. `Telegun` has seven letters, and its seventh "
                "letter, n, is at position 6. A position counts from 0, so it is always one less."
            ),
        ),
        dict(
            angle="in Tor",
            text=(
                "Mar'tu numbers the chalk wall from 0: gap 0, gap 1, gap 2. A word is a wall of letters. Same "
                "counting, same square brackets."
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
        dict(why="slice starts at 1", code=_places("word = sign[1:9]"), fails_at=1, message_contains="position 0"),
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
             message_contains="not inside it"),
        dict(why='initials = "" repeated inside the loop: emptied on every pass',
             code=_places(WORD_LINE, '    initials = ""\n' + INITIALS_LINE), fails_at=2,
             message_contains="above the loop only"),
        dict(why="off by one: name[1] is the second letter", code=_places(WORD_LINE, "    initials = initials + name[1]"),
             fails_at=2, message_contains="Position 1 is the second"),
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
        dict(why="the glue built, then nothing kept it (a bare expression in the loop)",
             code=_places(WORD_LINE, "    initials + name[0]"), fails_at=2, message_contains="nothing kept it"),
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
assert _tn(_o) == 'str' and _o, 'The line `word = "Plug"` is missing or changed. Put it back as it was at the start.'
_w = globals().get('word')
_want = 'G' + _o[1:]
if _w != _want:
    assert _tn(_w) == 'str', '`word` is not text now. Make it a new string, from `"G"` and the rest of `word`.'
    assert not (_w == _o and _newbox(_want, ('word',))), (
        'Your new variable holds the new string, but `word` still holds ' + _o + '. Put the new string in `word`: '
        'start the line with `word = `.')
    assert not (_w == _o and _want in _lines()), (
        'The print showed the new string, but `word` still holds ' + _o + '. Keep it in `word`: start the line '
        'with `word = `.')
    _lone = [_n for _n in _parsed().body if _tn(_n) == 'Expr' and _tn(_n.value) == 'BinOp']
    assert not (_w == _o and _lone), (
        'Python built the new string, then nothing kept it. Put it in `word`: start the line with `word = `.')
    assert _w != _o, '`word` still holds the old word. Make it hold a new string: `"G"` glued to the rest of the word.'
    assert _w != 'G' + _o[2:], '`word[2:]` skips a letter. The rest of the word starts at position 1.'
    assert _w != 'G' + _o, '`word[0:]` keeps the old first letter too. Start the rest at position 1.'
    assert _w != 'G' + _o[1:2], '`word[1]` is one letter. With a colon, `word[1:]` is the rest of the word.'
    assert False, '`word` does not hold the new word yet. Make it `"G"` glued to the rest of the word, from position 1 on.'
for _o2, _w2 in (('Drum', 'Grum'), ('Brass', 'Grass')):
    _ns, _rows, _err, _miss = _rerun({'word': _o2})
    assert not _miss, "Mar'tu can't test your code with another word: the line `word = \"Plug\"` is missing or changed. Put it back as it was at the start."
    assert not _err, "With another word, your code stopped. Python's last line: `" + _err + "`." + _tried({'word': _o2})
    if _ns.get('word') == _w2:
        continue
    _tree = _parsed()
    _sets = [_n for _n in _tree.body if _tn(_n) == 'Assign'
             and _any(_tn(_t) == 'Name' and _t.id == 'word' for _t in _n.targets) and _tn(_n.value) != 'Constant']
    _reads = [_n for _n in _sets if _any(_tn(_x) == 'Name' and _x.id == 'word' for _x in _ast.walk(_n.value))]
    _from_end = [_n for _n in _ast.walk(_tree) if _tn(_n) == 'Slice' and _n.lower is not None
                 and _tn(_n.lower) == 'UnaryOp']
    _swap = [_n for _n in _ast.walk(_tree) if _tn(_n) == 'Attribute' and _n.attr == 'replace']
    assert not _from_end, (
        'A slice counted from the end only fits a word of one length. With another word, `word` should become '
        + _w2 + ', but it did not. The rest of the word starts at position 1, whatever its length: `word[1:]`.'
        + _tried({'word': _o2}))
    assert not _swap, (
        '`.replace()` swaps the letters you typed, so it only works when the word holds them. With another word, '
        '`word` should become ' + _w2 + ', but it did not. Build it from position 1 on: `word[1:]`.'
        + _tried({'word': _o2}))
    assert not _reads, (
        'Your line only fits Plug. With another word, `word` should become ' + _w2 + ', but it did not. Build it '
        'from position 1 on: `word[1:]`.' + _tried({'word': _o2}))
    assert False, (
        'With another word, `word` should become ' + _w2 + ', but it did not. Build the new word from `word` '
        'itself, instead of typing it in.' + _tried({'word': _o2}))
''',
)

LETTERS_CANT_CHANGE = dict(
    id="letters-cant-change",
    title="Letters can't change",
    martu=(
        "You can't change one letter of a string. Programmers call this [[immutable]]: it can't change. Think of a word printed "
        "in a book: you can't swap one letter on the page, but you can print a new page. So `word[0] = \"G\"` stops "
        "Python with an error. Build a new string instead, like `spell = \"N\" + spell[1:]`.\n"
        "`spell[1:]` is the rest of the word, from position 1 to the end. Glue a new first letter onto it, then "
        "put the new string in the variable with `=`. A new `=` always replaces what a variable holds. A list lets you "
        "swap one item. Text does not.\n"
        "Lucky's canteen (his water bottle) has a label that says `Plug`. It should say `Glug`."
    ),
    example='spell = "Moon Step"\nspell = "N" + spell[1:]\nprint(spell)\n',
    example_output="Noon Step",
    names=["word"],
    starter=PLUG_STARTER,
    checkpoints=[
        dict(
            id="build-a-new-word",
            text="Fix line 4 so `word` holds `Glug`: glue `\"G\"` onto the rest of `word`.",
            dictated=False,
            hints=[
                "Read the title of the box in the Console: it says what went wrong. Then read Python's last line: "
                "`TypeError: 'str' object does not support item assignment`. It means text can't change one letter "
                "at a time.",
                "Make a new string instead, and put it in `word` with `=`. Glue the new letter onto `word[1:]`, the "
                "rest of the word.",
                "With other names:\n```python\ncoat = \"Bust\"\ncoat = \"R\" + coat[1:]\n```\n`coat` now holds "
                "`Rust`. The old text never changed. A new string took its spot.",
                "Write `" + GLUG_LINE + "` in place of `word[0] = \"G\"`.",
            ],
            checks=[GLUG_CHECK],
            pass_line="`word` holds Glug, a brand-new string. Lucky: Better. I'm still keeping the canteen.",
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
                "copy the letters you want, and hang it where the old one was."
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "1. `word[1:]` copies `lug`, the rest of the word.\n2. `\"G\" + ...` glues a G in front: `Glug`.\n"
                "3. `word = ...` puts the new string in the variable. The old `Plug` is gone."
            ),
        ),
        dict(
            angle="why",
            label="Why can't text change?",
            text=(
                "Python keeps each string sealed, so it never changes behind your back. Every change you see is a "
                "new string put in the variable. That is why tools like `.lower()` hand back a copy. You meet them "
                "in the next lesson, Words That Change Shape."
            ),
        ),
    ],
    takeaway="You can't change one letter of a string. Build a new one and keep it: `word = \"G\" + word[1:]`.",
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
             message_contains="The print showed the new string"),
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

QUOTE_COMMENT = "# 1. Print it with the quotes:\n# Mar'tu: \"NOT a compass.\"\n"
WALL_COMMENT = "# 2. Print the chalk wall in ONE\n#    print, one gap a line:\n# 48 48 47 46 44 41 37\n"
QUOTE_LINE = 'print("Mar\'tu: \\"NOT a compass.\\"")'
WALL_PRINT = 'print("48\\n48\\n47\\n46\\n44\\n41\\n37")'


def _escape(quote='print("")', wall='print("")'):
    # Each step has a `print("")` line in the starter to edit (the teacher's ruling).
    return (QUOTE_COMMENT + (quote + "\n" if quote else "") + "\n" + WALL_COMMENT + (wall + "\n" if wall else ""))


ESCAPE_STARTER = _escape()
ESCAPE_SOLUTION = _escape(QUOTE_LINE, WALL_PRINT)

QUOTE_CHECK = chk(
    "Mar'tu's line prints exactly, with its inner quote marks",
    r'''
_want = 'Mar\'tu: "NOT a compass."'
_rows = _lines()
if _want not in _rows:
    def _flat(_l):
        return ' '.join(_l.lower().replace('"', '').replace("'", '').replace('\\', '').split()).rstrip('.')
    _near = [_l for _l in _rows if _flat(_l) == _flat(_want)]
    _slash = [_l for _l in _rows if '/"' in _l and _flat(_l.replace('/', '')) == _flat(_want)]
    assert not _slash, ('A slash showed in the Console: `/"`. Use a backslash, `\\`, not the slash `/`: write each '
                        'inner quote as `\\"`.')
    assert _near, ('No line in the Console matches Mar\'tu\'s line yet. Print it exactly, with its quote marks: '
                   '`Mar\'tu: "NOT a compass."`.')
    _l = _near[0]
    assert '\\' not in _l, (
        'A backslash showed in the Console. Write each inner quote as `\\"`: one backslash, right before the '
        'quote mark.')
    assert "'NOT" not in _l, 'The quote marks around the words are single ones. Use double quote marks, each written `\\"`.'
    assert '"' in _l, 'The quote marks around Mar\'tu\'s words are missing. Inside the text, write each one as `\\"`.'
    assert _l.count('"') == 2, 'The line needs one quote mark before `NOT` and one after the period. Write each one as `\\"`.'
    assert False, ('The line is close, but not exact. Check every letter, space and capital: NOT is in capitals, and '
                   'the period sits inside the quotes.')
_esc_q = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str'
          and ('"' in _n.value or "'" in _n.value) and '\\' in (_ast.get_source_segment(_source, _n) or '')]
assert _esc_q, (
    'That prints the right line, but with no escape mark. This step practices the escape mark: inside ordinary '
    'double quotes, write each inner quote mark as `\\"`.')
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
        '`/n` showed as it is: a slash and an n are two plain letters. Use a backslash, `\\`, not the slash `/`: '
        '`\\n`.')
    assert not _any('\\n' in _l for _l in _rows), (
        '`\\n` showed as two letters. Write it inside ordinary quotes, with one backslash.')
    assert not _any('48 48' in _l or '48, 48' in _l or '4848' in _l for _l in _rows), (
        'The gaps all printed on one line. Put `\\n` between them, so each one starts a new line.')
    assert False, ('The seven gaps did not show in order, one on each line. Print all seven gaps: 48, 48, 47, 46, '
                   '44, 41, 37.')
_strs = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str' and '\n' in _n.value]
_esc = [_n for _n in _strs if '\\n' in (_ast.get_source_segment(_source, _n) or '')]
assert _esc or not _strs, (
    'Triple quotes keep a typed new line, so that works too. But this step practices `\\n`: write the gaps on '
    'one line, with `\\n` between them.')
assert _esc, ('Each gap has a `print` of its own. Use one `print` for all seven gaps: put `\\n` between them, inside '
              'one string.')
_nl = _B.sum([_n.value.count('\n') for _n in _esc])
_glue = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
         and _n.func.attr == 'join' and _tn(_n.func.value) == 'Constant' and _n.func.value.value == '\n']
assert _nl >= 6 or _glue, (
    'Some gaps still have a `print` of their own. Put all seven gaps in one `print`, with `\\n` between each '
    'pair: six of them.')
''',
)

ESCAPE_MARKS = dict(
    id="escape-marks",
    title="Escape marks",
    martu=(
        "Quote marks start and end text. So how do you put a quote mark *inside* text without ending it? Put an "
        "[[escape mark]] in front of it: a backslash, `\\`. `\\\"` means *this quote mark is part of the text*. "
        "So `print(\"Bo: \\\"Run.\\\"\")` shows `Bo: \"Run.\"`. `\\n` is an escape mark too: it starts a new "
        "line, like pressing Enter.\n"
        "In English class, a quote inside a quote uses single marks. I want real double marks, so you need "
        "the backslash.\n"
        "The backslash itself never shows: Python reads it as a signal, not a letter.\n"
        "If you like, after the steps (it's not a step): take one backslash out, press Run, and read the box in "
        "the Console."
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
            "Each `\\\"` shows as a plain quote mark, and the backslash disappears. `\\n` shows nothing you can "
            "see: it starts a new line, so `stuck.` goes on the next one."
        ),
    ),
    starter=ESCAPE_STARTER,
    checkpoints=[
        dict(
            id="quote-inside-quotes",
            text="On line 3, change `print(\"\")` so it shows `Mar'tu: \"NOT a compass.\"` exactly. Write each "
                 "quote mark inside the text as `\\\"`.",
            dictated=True,
            hints=[
                "Look at line 2: Mar'tu's words have their own quote marks. Inside your text, a plain `\"` would end "
                "the text early. What goes right in front of each one?",
                "With other words:\n```python\nprint(\"Gearshift: \\\"Holding.\\\"\")\n```\nThat shows "
                "`Gearshift: \"Holding.\"`. The outer quotes start and end the text. Each `\\\"` is a quote inside it.",
                "The apostrophe in `Mar'tu` is fine inside double quotes. Only the double quote marks need a backslash.",
                "Write `" + QUOTE_LINE + "` in place of the `print(\"\")` under `# 1.`.",
            ],
            checks=[QUOTE_CHECK],
            pass_line="The quote marks show inside the text. Mar'tu: Yes. Once again, it is not a compass.",
        ),
        dict(
            id="wall-on-new-lines",
            text="On line 8, change `print(\"\")` so it shows the seven gaps (hours between bursts) from line 7, one "
                 "on each line. Use "
                 "one `print`, with `\\n` between the gaps.",
            dictated=False,
            hints=[
                "Look at the numbers on line 7. Use one `print` and one string. Where one gap ends and the next "
                "begins, put `\\n`.",
                "```python\nprint(\"gold\\nteal\\nsilver\")\n```\nThat prints three lines: `gold`, `teal`, `silver`. "
                "No spaces around `\\n`, or they print too.",
                "Write `" + WALL_PRINT + "` in place of the `print(\"\")` under `# 2.`.",
            ],
            checks=[WALL_CHECK],
            pass_line="Seven gaps, one `print`. Mar'tu: They shrink down the page, the same as on my wall, yes?",
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
                "A backslash in front, `\\\"`, tells Python: this is not the end, only a quote mark."
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
    takeaway="`\\\"` puts a quote mark inside text, and `\\n` starts a new line. The backslash never shows.",
    wrong_answers=[
        dict(why="the starter prints nothing", code=ESCAPE_STARTER, fails_at=1,
             message_contains="with its quote marks"),
        dict(why="inner quotes with no backslash (SyntaxError)",
             code=_escape('print("Mar\'tu: "NOT a compass."")', WALL_PRINT), fails_at=0,
             message_contains="invalid syntax"),
        # One backslash put in and one missed, as Mar'tu's own text invites ("take one backslash out"), with the
        # starter's `print("")` on line 8 still there: its quote mark is never the end of line 3's text.
        dict(why="one backslash missed: a bare quote mark left inside (SyntaxError)",
             code=_escape('print("Mar\'tu: \\"NOT a compass."")'), fails_at=0,
             message_contains="unterminated string literal"),
        dict(why="the closing quote escaped: the text never closes (SyntaxError)",
             code=_escape('print("Mar\'tu: \\"NOT a compass.\\")'), fails_at=0,
             message_contains="perhaps you escaped the end quote"),
        dict(why="slashes where the backslashes go (SyntaxError)",
             code=_escape('print("Mar\'tu: /"NOT a compass./"")', WALL_PRINT), fails_at=0,
             message_contains="invalid syntax"),
        dict(why="a slash before each escaped quote: the slashes print",
             code=_escape('print("Mar\'tu: /\\"NOT a compass./\\"")', WALL_PRINT), fails_at=1,
             message_contains="not the slash"),
        dict(why="single outer quotes: the apostrophe in Mar'tu ends the text",
             code=_escape("print('Mar'tu: \"NOT a compass.\"')", WALL_PRINT), fails_at=0,
             message_contains="unterminated string literal"),
        dict(why="the inner quotes left out", code=_escape('print("Mar\'tu: NOT a compass.")', WALL_PRINT),
             fails_at=1, message_contains="around Mar'tu's words are missing"),
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
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _crash_ev(_ev)
    assert not (_v is None and _p), (
        "`make_bar` printed the blocks, then handed back `None`, Python's word for nothing. Hand back the blocks "
        "with `return`, not `print`." + _ev)
    assert _v is not None, (
        "`make_bar` handed back `None`, Python's word for nothing: no line in it hands anything back. End it with "
        "`return`, so it hands back the blocks." + _ev)
    assert _tn(_v) == 'str', ('`make_bar` did not hand back text. Hand back the blocks as text: stamp them with `*` '
                              'and glue them with `+`.' + _ev)
    _res.append((_c, _m, _v, _ev))
assert _res[0][2] != _res[1][2], (
    "`make_bar` hands back the same blocks for any numbers. Build them from `current` and `maximum`, so they "
    "change with them. Mar'tu tested your function with two test calls, `make_bar(3, 5)` and `make_bar(6, 9)`: "
    "both handed back the same text.")
for _c, _m, _v, _ev in _res:
    # Only the blocks count here, so a bar that is finished (step 2) still passes step 1.
    if ''.join([_x for _x in _v if _x in '▓░']) == '▓' * _c + '░' * (_m - _c):
        continue
    assert '█' not in _v, 'The bar used `█`. Use `full` and `empty`, the `▓` and `░` already in your code.' + _ev
    _nf, _ne = _v.count('▓'), _v.count('░')
    assert _nf == _c, ('The bar had ' + _str(_nf) + (' full block' if _nf == 1 else ' full blocks') + ', not '
                       + _str(_c) + '. Stamp `full` once for each sip left: `full * current`.' + _ev)
    assert _ne == _m - _c, ('The bar had ' + _str(_ne) + (' empty block' if _ne == 1 else ' empty blocks') + ', not '
                            + _str(_m - _c) + '. Stamp `empty` once for each sip gone: `maximum - current` times.' + _ev)
    assert False, 'The empty blocks came first. Put the full blocks first, then the empty ones, like `▓▓░`.' + _ev
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
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _crash_ev(_ev)
    assert not (_v is None and _p), (
        '`make_bar` printed the bar, then handed back `None`. Hand back the bar with `return`, not `print`.' + _ev)
    assert _v is not None, '`make_bar` handed back `None`. End it with `return`, so it hands back the bar.' + _ev
    assert _tn(_v) == 'str', '`make_bar` did not hand back text. Hand back the bar as text, glued together with `+`.' + _ev
    _res.append((_c, _m, _v, _ev))
for _c, _m, _v, _ev in _res:
    if _v == _want_bar(_c, _m):
        continue
    _fd = _fdef('make_bar')
    _early = _fd is not None and _any(_tn(_n) == 'Return' for _n in _fd.body[:-1])
    assert not (_early and _v == '▓' * _c + '░' * (_m - _c)), (
        'Your first `return bar` hands back the blocks and ends `make_bar`, so the lines under it never run. Take '
        'out that first `return bar`, or move the glue lines above it.' + _ev)
    assert _v != '▓' * _c + '░' * (_m - _c), (
        '`make_bar` handed back only the blocks. Glue `"Glug ["` on the front, then `"] "` and the numbers on the '
        'end, like `Glug [▓▓░] 2/3`.' + _ev)
    assert _v.endswith(_str(_c) + '/' + _str(_m)), (
        'The numbers at the end are missing or out of order. End with the numbers, sips left first, like `2/3`. '
        'Make each one text with `str()`.' + _ev)
    assert _v.startswith('Glug ['), 'The bar does not start with `Glug [`. Start it that way, like `Glug [▓▓░] 2/3`.' + _ev
    assert False, ('The bar is close. Check the square brackets and spaces: one space after `Glug`, one after `]`, '
                   'like `Glug [▓▓░] 2/3`.' + _ev)
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
    assert not _e, _why('make_bar', _e, __FOREIGN__) + _crash_ev(_ev)
    assert _v == _want_bar(_c, _m), ('`make_bar` gives the wrong bar for an empty canteen or a full one. Make it '
                                     'work for those too.' + _ev)
_typed = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str'
          and _re.search(r'\d\s*/\s*\d', _n.value)]
assert not _typed, (
    'A bar is typed in quotes, so it does not come from the function. Print bars that `make_bar` builds, with '
    '`print(make_bar(...))`.')
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
    'A bar is glued together outside the function, so it does not come from it. Print bars that `make_bar` '
    'builds, with `print(make_bar(...))`.')
assert _edge(_from_fn, False), (
    'No bar for an empty canteen shows yet. Under the other prints, call `make_bar` with 0 sips left, and print it.')
assert _edge(_from_fn, True), (
    'No bar for a full canteen shows yet. Print one: call `make_bar` with as many sips left as the canteen holds.')
''',
    FOREIGN=BAR_FOREIGN.split(","),
)

BARS_ONE_MORE_TIME = dict(
    id="bars-one-more-time",
    title="Bars one more time",
    martu=(
        "A bar is a tape diagram, like in math class: the full part plus the empty part make the whole. Make one "
        "for Lucky's canteen of glug (his drink), for any numbers, like this one:\n"
        "```text\nGlug [▓▓░] 2/3\n```\n"
        "In `make_bar(current, maximum)`, `current` is the sips left and `maximum` is how many sips the canteen "
        "holds.\n"
        "Stamp one `▓` for each sip left and one `░` for each sip gone: `\"▓\" * 2` is `\"▓\" + \"▓\"`. Then glue "
        "on the numbers with `+`, made into text with `str()`. You know all three from the campaign's mana bars, "
        "`\"█\" * caster[\"mana\"]`. Now they work together."
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
            text="Replace `pass` on line 7 so `make_bar` hands back only the blocks, for any numbers. For "
                 "`make_bar(2, 3)`, that is `▓▓░`.",
            dictated=False,
            hints=[
                "Look at the `def` line. `current` is the sips left and `maximum` is how many sips the canteen holds. "
                "How many `full` blocks do you need, and how many `empty` ones?",
                "`*` stamps text: `\"#\" * 3` is `###`. Sips gone is `maximum - current`. Like the Example's "
                "`gone = tank - left`, a variable of its own makes Python work that out first.",
                "Glue the two stamps with `+`, full blocks first. Then hand the bar back with `return`, like the "
                "Example's `meter` lines.",
                "Write `used = maximum - current` in place of `pass`. Then `bar = full * current`, then "
                "`bar = bar + empty * used`, then `return bar`.",
            ],
            checks=[BLOCKS_CHECK],
            pass_line="`make_bar(2, 3)` hands back `▓▓░`: two full, one empty. Lucky: Don't look at me like that.",
        ),
        dict(
            id="label-and-numbers",
            text="On your `return` line, glue `\"Glug [\"` in front of the blocks, then `\"] \"` and the numbers "
                 "after them, so `make_bar(2, 3)` hands back `Glug [▓▓░] 2/3`.",
            dictated=False,
            hints=[
                "Look at your `return` line. The blocks are done: which pieces go in front of them, and which go "
                "after?",
                "A number needs `str()` before `+` can glue it to text, like the Example's `str(left)`: "
                "`str(current) + \"/\" + str(maximum)`.",
                "Write `bar = \"Glug [\" + bar + \"] \"`, then `bar = bar + str(current) + \"/\"`, then "
                "`bar = bar + str(maximum)`, then `return bar`, in place of the `return bar` line.",
            ],
            checks=[BAR_CHECK],
            pass_line="`make_bar(2, 3)` hands back `Glug [▓▓░] 2/3`. Lucky: That's my canteen. Don't tell Mar'tu how it smells.",
        ),
        dict(
            id="empty-and-full",
            text="Under the last line, print two more bars from `make_bar`. Make one bar for an empty canteen and "
                 "one for a full one.",
            dictated=False,
            hints=[
                "Look at the two `print` lines at the bottom. An empty canteen has 0 sips left. How many sips does "
                "a full one have left?",
                "Call the function with numbers that show the edges: `fuel_bar(0, 5)` is an empty tank, and "
                "`fuel_bar(5, 5)` is a full one. `\"#\" * 0` is empty text, so nothing breaks.",
                "Write `print(make_bar(0, 3))` and `print(make_bar(3, 3))` at the bottom.",
            ],
            checks=[BAR_EDGE_CHECK],
            pass_line="Empty, full, and everything between. Mar'tu: One function makes them all, yes?",
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
    takeaway="A bar for any numbers: stamp `full * current` and `empty * (maximum - current)`, glue with `+` and `str()`.",
    wrong_answers=[
        dict(why="the starter: pass", code=BAR_STARTER, fails_at=1, message_contains="handed back `None`, Python's word"),
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
             message_contains="You wrote `curent`, but the parameters of `make_bar` are"),
        dict(why="curent with the calls kept: the student's own Run stops (NameError, the explainer's row)",
             code=_bar(BAR_BODY.replace("full * current", "full * curent")), fails_at=0,
             message_contains="name 'curent' is not defined"),
        dict(why="the example's left for current (the calls taken out: _why)",
             code=_bar(BAR_BODY.replace("maximum - current", "maximum - left"), calls=""), fails_at=1,
             message_contains="`left` comes from Mar'tu's example: the parameters of `make_bar` are"),
        dict(why="the example's tank for maximum (the calls taken out: _why)",
             code=_bar(BAR_BODY.replace("used = maximum", "used = tank"), calls=""), fails_at=1,
             message_contains="`tank` comes from Mar'tu's example"),
        dict(why="the blocks done, the label not started (the partial)", code=_bar(BLOCKS_BODY + BAR_RETURN),
             fails_at=2, message_contains="only the blocks"),
        dict(why="the numbers left off", code=_bar(BLOCKS_BODY + '    bar = "Glug [" + bar + "]"\n' + BAR_RETURN),
             fails_at=2, message_contains="End with the numbers"),
        dict(why="the numbers swapped", code=_bar(BAR_BODY.replace("str(current)", "str(MAXX)").replace(
            "str(maximum)", "str(current)").replace("MAXX", "maximum")), fails_at=2, message_contains="sips left first"),
        dict(why="no space before the numbers", code=_bar(BAR_BODY.replace('"] "', '"]"')), fails_at=2,
             message_contains="brackets and spaces"),
        dict(why="no Glug label", code=_bar(BAR_BODY.replace('"Glug [" + bar', '"[" + bar')), fails_at=2,
             message_contains="does not start with"),
        dict(why="the glue lines under the first return bar: they never run",
             code=_bar(BLOCKS_BODY + BAR_RETURN + LABEL_BODY + BAR_RETURN), fails_at=2, message_contains="never run"),
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
    assert not _miss, 'The line `' + _miss[0] + ' = ...` is gone.'
    assert not _err, "With other numbers, your code stopped. Python's last line: `" + _err + "`." + _ev
    _d, _w = _ns.get('days_left'), _ns.get('week')
    _want = 'Velocite [' + '▓' * _d + '░' * (_w - _d) + ']'
    if _want in _rows:
        continue
    _got = [_l for _l in _rows if _l.startswith('Velocite')]
    assert _got, 'No line in the Console shows the Velocite bar.' + _ev
    _nf, _ne = _got[-1].count('▓'), _got[-1].count('░')
    if _vals is not None:
        # The student's own run looked right: name the slip and its line first, then the labelled test.
        _its = ['`' + _k + ' = ' + _str(_x) + '`' for _k, _x in _vals.items()]
        _with = ('With a test number, ' + _its[0] if _len(_its) == 1 else 'With test values, ' + ' and '.join(_its)) + ', '
        _saw = (('the bar held ' + _blk(_nf + _ne) + ', not ' + _str(_w) + '.') if _nf + _ne != _w else
                ('the bar showed ' + _str(_nf) + (' full block' if _nf == 1 else ' full blocks') + ', not '
                 + _str(_d) + '.'))
        _tree = _parsed()
        _typed_bar = [_n for _n in _ast.walk(_tree) if _tn(_n) == 'Constant' and _tn(_n.value) == 'str'
                      and _len(_n.value) > 1 and ('▓' in _n.value or '░' in _n.value)]
        _typed_at = sorted({_n.lineno for _a in _tree.body if _tn(_a) == 'Assign'
                            and _any(_tn(_t) == 'Name' and _t.id == 'bar' for _t in _a.targets)
                            for _n in _ast.walk(_a.value) if _tn(_n) == 'Constant' and _tn(_n.value) == 'int'})
        assert not _typed_bar, ('The bar is typed in the `print` line, so it does not change with `days_left` and '
                                '`week`. ' + _with + _saw)
        assert not _typed_at, ('Line ' + _str(_typed_at[0]) + ' has a number typed in, so the bar does not change '
                               'with `days_left` and `week`. ' + _with + _saw)
    assert _nf == _d, 'The bar shows ' + _blk(_nf) + ' full for ' + _str(_d) + ' days left.' + _ev
    assert _nf + _ne == _w, 'The bar holds ' + _blk(_nf + _ne) + ' in all, for a week of ' + _str(_w) + ' days.' + _ev
    assert False, 'The printed line does not start with `Velocite [` and end with `]`.' + _ev
''',
)

# Lean, proved: the SOLO's check never names its fix (as Unit 2's _leaned asserts for QC2's rewrites).
assert "(week-days_left)" not in SOLO_A_CHECK[1].replace(" ", ""), "solo-8a's check names its fix"

SOLO_8A = dict(
    id="solo-8a",
    title="Show Mar'tu",
    martu=(
        "One bug, for you alone. Python stops on it. Read the box in the Console: the title first, then Python's "
        "last line, then the line number. Bomb Shell's bar should hold one block for every day of the week, yes?"
    ),
    solo=True,
    explainer="lean",
    names=["bar", "week", "days_left"],
    starter=SOLO_A_STARTER,
    checkpoints=[
        dict(
            id="brackets-first",
            text="Fix line 6 so the bar holds `week` blocks in all: `▓` for each day left, `░` for the rest.",
            dictated=False,
            hints=[
                "Read the title of the box in the Console. Then read Python's last line: "
                "`unsupported operand type(s) for -: 'str' and 'int'`. Python stopped at line 6.",
                "Python uses PEMDAS, so it does `*` before `-`. That makes `\"░\" * week` text first. Then it tries "
                "to take a number away from text.",
                "Parentheses go first, like PEMDAS in math class: `\"#\" * (5 - 2)` stamps 3 marks.",
                "Write `" + SOLO_A_LINE + "` on line 6.",
            ],
            checks=[SOLO_A_CHECK],
            pass_line="Mar'tu: You did that on your own. The empty blocks were worked out first, with parentheses.",
        ),
    ],
    solution=SOLO_A_SOLUTION,
    # No assemble: from Unit 3 on a SOLO has none (its pieces would be the mended line; content.test.ts).
    another_way=[
        dict(angle="shorter", text="`*` goes before `-`. Parentheses go before both, like PEMDAS."),
        dict(
            angle="step-by-step",
            text="1. Work out the days gone: week minus days left.\n2. Stamp `░` that many times.\n3. Glue it on.",
        ),
    ],
    takeaway="Parentheses make Python work out `week - days_left` before it stamps, like PEMDAS.",
    wrong_answers=[
        dict(why="the starter: * before - (TypeError)", code=SOLO_A_STARTER, fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the 3 typed: (week - 3)", code=_solo_a('bar = bar + "░" * (week - 3)'), fails_at=1,
             message_contains="Line 6 has a number typed in"),
        dict(why="the 7 typed: (7 - days_left)", code=_solo_a('bar = bar + "░" * (7 - days_left)'), fails_at=1,
             message_contains="Line 6 has a number typed in"),
        dict(why="the minus taken out: a whole week of empty blocks", code=_solo_a('bar = bar + "░" * week'),
             fails_at=1, message_contains="10 blocks in all"),
        dict(why="the subtraction the wrong way round: no empty blocks", code=_solo_a('bar = bar + "░" * (days_left - week)'),
             fails_at=1, message_contains="3 blocks in all"),
        dict(why="the bar typed in the print", code=_solo_a('bar = bar + "░" * (week - days_left)')
             .replace(SOLO_A_PRINT, 'print("Velocite [▓▓▓░░░░]")\n'), fails_at=1,
             message_contains="typed in the `print` line"),
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
    summary=(
        "Read each letter by its position, cut out pieces, and build new words. Put quote marks and new lines "
        "inside text. Draw a bar for any numbers."
    ),
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
    title="Quick review: 2 questions, not scored",
    optional=True,
    minutes=2,
    summary="Two questions from Strings Are Rows of Letters, before you start. Nothing is scored.",
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
                "`[:5]` takes positions 0, 1, 2, 3 and 4: five letters. The end position, 5, is left out. The "
                "function hands the slice back, and `print` shows it."
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
assert _tn(_o) == 'str', 'The line `line = "shield up."` is missing or changed. Put it back as it was at the start.'
assert 'line' in globals(), 'The variable `line` is missing or changed. Put it back as it was at the start.'
_v = globals()['line']
_want = _o.upper()
if _v != _want:
    assert not _is_method(_v), (
        '`.upper` has no `()`, so the method never ran: `line` holds the method itself, not text. Add `()` after '
        '`.upper`.')
    assert _tn(_v) == 'str', '`line` is not text now. Keep it as text: the capital copy that `.upper()` hands back.'
    assert not (_v == _o and _newbox(_want, ('line',))), (
        'Your new variable holds the capital copy, but `line` still holds small letters. Keep the copy in `line` '
        'itself: start the line with `line = `.')
    assert not (_v == _o and _want in _lines()), (
        'The print showed a capital copy, but `line` itself still holds small letters. Keep the copy in `line`: '
        'start the line with `line = `.')
    assert not (_v == _o and _bare('upper')), (
        '`line.upper()` makes a capital copy, then nothing keeps it. Catch the copy: put it in `line` with '
        '`line = `.')
    assert _v != _o.title(), (
        '`line` got `.title()`: a capital at the start of each word. This step wants every letter in capitals, '
        'with `.upper()`.')
    assert _v != _o.capitalize(), (
        '`line` got `.capitalize()`: only the first letter is a capital. This step wants every letter in capitals, '
        'with `.upper()`.')
    assert False, '`line` does not hold the capital copy yet. Make it hold what `line.upper()` hands back.'
assert _want in _lines(), 'The capital copy does not show in the Console. Print `line` after it changes.'
_ns, _rows, _err, _miss = _rerun({'line': 'latch stuck.'})
assert not _miss, "Mar'tu can't test your code with other text: the line `line = \"shield up.\"` is missing or changed. Put it back as it was at the start."
assert not _err, "With other text, your code stopped. Python's last line: `" + _err + "`." + _tried({'line': 'latch stuck.'})
assert _ns.get('line') == 'LATCH STUCK.', (
    'With other text, `line` did not change to match. Make the copy from `line` with `.upper()`, instead of '
    'typing it in.' + _tried({'line': 'latch stuck.'}))
''',
)

ALARM_CHECK = chk(
    "alarm is True when up is in line, whatever the capitals",
    r'''
assert 'alarm' in globals(), 'There is no variable named `alarm` yet. Make one.'
_a = globals()['alarm']
assert _tn(_a) == 'bool', '`alarm` does not hold True or False. Make it a question with `in`.'
assert _a is True, (
    '`alarm` is False: `in` matches capitals exactly, and `line` now holds UP in capitals. Ask a lower-case copy.')
for _t, _want in (('gear up.', True), ('latch stuck.', False)):
    _ns, _rows, _err, _miss = _rerun({'line': _t})
    assert not _err and _ns.get('alarm') is _want, (
        '`alarm` did not change to match other text. Ask about `line` itself.' + _tried({'line': _t}))
''',
)

LOUD_AND_QUIET = dict(
    id="loud-and-quiet",
    title="Methods hand back a copy",
    martu=(
        "A [[method]] is a tool you use with a dot. The dot asks the text to do a job, the way you speak to someone "
        "by name: `line.upper()` means *line, give me a copy in capitals*. You get a new copy, and the text in "
        "`line` does not change. Catch the copy with `=`, or it is gone: `name = name.title()`.\n"
        "[[.upper()]] hands back a copy in CAPITALS. [[.title()]] hands back A Capital On Each Word, like a book "
        "title. `.lower()` and `.capitalize()`, from earlier units, work the same way.\n"
        "Lucky asks the same thing about everything: \"What's in it for me?\" A string answers every job the same "
        "way: with a new string."
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
            text="Change line 2 so `line` keeps the capital copy. You should see `SHIELD UP.` in the Console.",
            dictated=False,
            hints=[
                "Look at the Console: it shows `shield up.`, still small. Line 2 asks for a capital copy. Where does "
                "that copy go?",
                "A method hands you a new copy. Catch it in the variable with `=`, the way the Example's last two "
                "lines do with `name`.",
                "Write `line = line.upper()` in place of `line.upper()`.",
            ],
            checks=[LOUD_CHECK],
            pass_line="`line` keeps the capital copy: SHIELD UP. Bomb Shell: Loud. Good.",
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
            "Bomb Shell checks his own report. Under the print, make `alarm` hold `True` when the word `up` is in "
            "`line`, in any capitals. `in` matches capitals exactly, so ask a lower-case copy."
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
             message_contains="The print showed a capital copy"),
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
    assert not _e, _why('tidy_line', _e, __FOREIGN__) + _crash_ev(_ev)
    _res.append((_a, _p, _v, _ev))
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    "`tidy_line` hands back the same text for any line. Build the line from `raw`, so it changes with what is "
    "handed in. Mar'tu tested your function with two test lines: both handed back the same text.")
for _a, _p, _v, _ev in _res:
    if _v == _a.lower().capitalize():
        continue
    assert not (_v is None and _p), (
        "`tidy_line` printed the line, then handed back `None`, Python's word for nothing. Hand back the line "
        "with `return`, not `print`." + _ev)
    assert _v is not None, (
        "`tidy_line` handed back `None`, Python's word for nothing: no line in it hands anything back. End it with "
        "`return`, so it hands the tidy line back." + _ev)
    assert not _is_method(_v), (
        '`.' + _v.__name__ + '` has no `()`, so the method never ran: `tidy_line` hands back the method itself, not '
        'text. Add `()` after `.' + _v.__name__ + '`.' + _ev)
    assert _tn(_v) == 'str', '`tidy_line` did not hand back text. Hand back `raw` after its two methods.' + _ev
    assert _v != _a, (
        '`tidy_line` handed back the line as it came in: each method made a copy, and nothing kept it. Keep what '
        'the methods hand back.' + _ev)
    assert _v != _a.lower(), ('The line came back all in small letters. Add `.capitalize()` after `.lower()`, so the '
                              'first letter is a capital.' + _ev)
    assert _v != _a.title(), (
        '`tidy_line` used `.title()`: a capital at the start of every word. `.capitalize()` makes only the first '
        'letter big.' + _ev)
    assert False, ('`tidy_line` does not hand back the tidy line yet. Hand back `raw` in small letters with a capital '
                   'first letter: `.lower()`, then `.capitalize()`.' + _ev)
''',
    CASES=["THE CLOCK IS RED.", "mOON sTEP IS READY."],
    FOREIGN=TIDY_FOREIGN.split(","),
)

CHAIN_THE_SPELLS = dict(
    id="chain-the-spells",
    title="Chain two methods",
    martu=(
        "A [[chain]] is one method right after another, like `said.lower().capitalize()`. Python reads it left to "
        "right. `.lower()` hands back a new string, and `.capitalize()` works on that copy. In math class, it is "
        "like two function machines in a row: what comes out of the first goes into the second.\n"
        "You have done this in two steps before. In the campaign's Module 1, my line went through two tidy "
        "steps:\n"
        "```python\nsaid = said.lower()\nsaid = said.capitalize()\n```\n"
        "A chain does both on one line:\n"
        "```python\nsaid = said.lower().capitalize()\n```"
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
            text="Replace `pass` on line 4 so `tidy_line` hands back `raw.lower().capitalize()`. That gives small "
                 "letters, with a capital first letter.",
            dictated=True,
            hints=[
                "Look at line 4, inside `tidy_line`. There, the text is called `raw`. It needs two methods, in "
                "order: `.lower()`, then `.capitalize()`. Then `return` hands the result back.",
                "Two steps work, each one caught:\n```python\nsaid = said.lower()\nsaid = said.capitalize()\n"
                "return said\n```\nIn `tidy_line`, the text is called `raw`, so write `raw` where this says `said`. "
                "One chain on one line works too.",
                "Write `return raw.lower().capitalize()` in place of `pass`.",
            ],
            checks=[TIDY_CHECK],
            pass_line="`tidy_line` hands back `What is the decay?`, tidy. Mar'tu: Good question. Ask it quietly, yes?",
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
                "\"What is the decay?\"\n```\nEach step down is a new copy. `return` hands back the last one."
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
            label="A shortcut with .capitalize()",
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
             message_contains="`said` comes from Mar'tu's example: the parameter of `tidy_line` is `raw`."),
        dict(why="said with the calls kept: the student's own Run stops (NameError, the explainer's row)",
             code=_tidy("    return said.lower().capitalize()"), fails_at=0, message_contains="name 'said' is not defined"),
        dict(why="Mar'tu's two steps copied, the calls kept: the student's own Run stops (UnboundLocalError, the "
                 "explainer's row)",
             code=_tidy("    said = said.lower()\n    said = said.capitalize()\n    return said"), fails_at=0,
             message_contains="cannot access local variable 'said'"),
        dict(why="Mar'tu's two steps copied as they are: said used before it is made (UnboundLocalError: _why)",
             code=_tidy("    said = said.lower()\n    said = said.capitalize()\n    return said", tail=""), fails_at=1,
             message_contains="used before the line that makes it: Python runs a function from the top down"),
        dict(why="a near-miss of the parameter, rwa (the calls taken out: _why)",
             code=_tidy("    return rwa.lower().capitalize()", tail=""), fails_at=1,
             message_contains="You wrote `rwa`, but the parameter of `tidy_line` is `raw`"),
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
assert _tn(_rep) == 'str', 'The line `report = "Latch stuck. Shield up."` is missing or changed. Put it back as it was at the start.'
assert 'sentences' in globals(), 'The line `sentences = ...` is missing or changed. Put it back as it was at the start.'
_s = globals()['sentences']
if _s != _rep.split('. '):
    assert not _is_method(_s), (
        '`.split` has no `()`, so the method never ran: `sentences` holds the method itself, not the pieces. Add '
        '`()` after `.split`: `.split(". ")`.')
    assert _tn(_s) != 'str', (
        '`sentences` holds text, not a list. Make it hold what `.split(". ")` hands back: a list of pieces.')
    _nb = _newbox(_rep.split('. '), ('sentences',))
    assert not (_s == [] and _nb), (
        '`' + (_nb or [''])[0] + '` holds the pieces, but `sentences` is still the empty list. Put the pieces in '
        '`sentences`, the name this step asks for.')
    assert _s != [], '`sentences` is still the empty list. Make it hold the pieces of `report`, cut with `.split(". ")`.'
    assert _s != _rep.split(), (
        'Empty parentheses cut at every space. Put `". "` in the parentheses, to cut at each period and space.')
    assert _s != _rep.split('.'), (
        'With the period alone, a space stays on the next piece. Put `". "` in the parentheses: a period and a '
        'space.')
    assert False, ('`sentences` does not hold the cut-up report yet. Make it hold `report.split(". ")`: the report '
                   'cut at each period and space.')
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _miss, "Mar'tu can't test your code with another report: the line `report = ...` is missing or changed. Put it back as it was at the start."
assert not _err, "With another report, your code stopped. Python's last line: `" + _err + "`." + _tried({'report': _o})
assert _ns.get('sentences') == _o.split('. '), (
    'With another report, `sentences` did not change to match. Cut `report` itself with `.split`, instead of '
    'typing the list in.' + _tried({'report': _o}))
''',
    OTHER=OTHER_REPORT,
)

COUNT_CHECK = chk(
    "word_count is the number of words in report, for another report too",
    r'''
_rep = globals().get('report')
assert 'word_count' in globals(), 'The line `word_count = ...` is missing or changed. Put it back as it was at the start.'
_c = globals()['word_count']
if not (_c == _len(_rep.split()) and _tn(_c) == 'int'):
    assert _tn(_c) != 'list', '`word_count` holds the list itself. Count its pieces with `len()`.'
    assert _tn(_c) == 'int', '`word_count` is not a number. Make it one: `len()` counts the pieces of a list.'
    assert not (_c == 0 and _first_lit('word_count') == 0 and _len(_assigns('word_count')) == 1), (
        "`word_count` still holds the 0 it started with. Make it hold the number of words in `report`.")
    assert _c != _len(_rep), (
        'That counted every letter and space. Split `report` into words first, then count the pieces.')
    assert _c != _len(_rep.split('. ')), (
        'That counted the sentences. Count the words instead: split with empty parentheses, at the spaces.')
    assert False, '`word_count` does not hold the number of words yet. Make Python count the words in `report` with `len()`.'
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _err, "With another report, your code stopped. Python's last line: `" + _err + "`." + _tried({'report': _o})
assert _ns.get('word_count') == _len(_o.split()), (
    'With another report, it stayed ' + _str(_c) + '. Count with `len()`, so `word_count` changes to match.'
    + _tried({'report': _o}))
''',
    OTHER=OTHER_REPORT,
)

INT_CHECK = chk(
    "next_hours is the number in hours_text plus one, for other text too",
    r'''
_h = globals().get('hours_text')
assert _tn(_h) == 'str' and _h.strip().isdigit(), 'The line `hours_text = "48"` is missing or changed. Put it back as it was at the start.'
assert 'next_hours' in globals(), 'The line `next_hours = ...` is missing or changed. Put it back as it was at the start.'
_n = globals()['next_hours']
if not (_n == _int(_h) + 1 and _tn(_n) == 'int'):
    assert not (_tn(_n) == 'str' and _n == _h + '1'), (
        'Gluing on the text `"1"` gave `' + _h + '1`: text glued to text. Turn `hours_text` into a number with '
        '`int()` first, then add 1.')
    assert _tn(_n) != 'str', ('`next_hours` is text, not a number. `int(hours_text)` turns the text into a number. '
                              'Then add 1.')
    assert not (_n == 0 and _first_lit('next_hours') == 0 and _len(_assigns('next_hours')) == 1), (
        "`next_hours` still holds the 0 it started with. Make it the number in `hours_text`, plus one.")
    assert _n != _int(_h), '`next_hours` holds the number, but not plus one. Add one with `+ 1`.'
    assert False, '`next_hours` does not hold the right number yet. Make it hold `int(hours_text) + 1`.'
_ns, _rows, _err, _miss = _rerun({'hours_text': '37'})
assert not _miss, "Mar'tu can't test your code with other text: the line `hours_text = \"48\"` is missing or changed. Put it back as it was at the start."
assert not _err, "With other text, your code stopped. Python's last line: `" + _err + "`." + _tried({'hours_text': '37'})
assert _ns.get('next_hours') == 38, (
    'With other text, it stayed ' + _str(_n) + '. Use `hours_text` itself, so `next_hours` changes to match.'
    + _tried({'hours_text': '37'}))
''',
)

JOIN_CHECK = chk(
    "joined holds the words glued with a space, for another list too",
    r'''
_wd = globals().get('words')
assert _tn(_wd) == 'list', 'The list `words` is missing or changed. Put it back as it was at the start.'
assert 'joined' in globals(), 'The line `joined = ...` is missing or changed. Put it back as it was at the start.'
_j = globals()['joined']
if _j != ' '.join(_wd):
    assert _tn(_j) == 'str', '`joined` is not text. Make it text: `" ".join(words)` hands back one string.'
    assert _j != '', '`joined` is still empty. Make it hold the words glued together.'
    assert _j != ''.join(_wd), 'The words were glued with no gap. Put a space between the quotes before `.join`.'
    assert _j != _str(_wd), ('`joined` is the list written out, with its square brackets. Glue the words with '
                             '`" ".join(words)`.')
    assert _j != ' '.join('words'), ('`.join` glued the letters of the word *words*. ' + _QUOTES
                                     + ' Take the quotes off `words`.')
    assert False, '`joined` does not hold the glued words yet. Make it hold the words of `words`, with one space between them.'
_o = ['Optic', 'dim.', 'Hold.']
_ns, _rows, _err, _miss = _rerun({'words': _o})
assert not _miss, "Mar'tu can't test your code with another list: the line `words = [...]` is missing or changed. Put it back as it was at the start."
assert not _err, "With another list, your code stopped. Python's last line: `" + _err + "`." + _tried({'words': _o})
assert _ns.get('joined') == 'Optic dim. Hold.', (
    'With three words, `joined` did not change to match. Glue every word in `words` with `.join`.'
    + _tried({'words': _o}))
''',
)

SPLIT_THE_CLIPPED = dict(
    id="split-the-clipped",
    title="Split and join",
    martu=(
        "[[.split()]] cuts text into a [[list]] of pieces, like cutting a sentence strip into word cards in English "
        "class. Empty parentheses cut at every space: `\"Moon Step\".split()` gives `['Moon', 'Step']`. "
        "`.split(\". \")` cuts at each period and space instead. To glue a list back into one text, ask the glue: "
        "`\" \".join(words)`. The text before [[.join()]] goes between the pieces, like the commas in a list of "
        "items.\n"
        "What comes back from `.split()` is a list, not text: count it with `len()`, read it by position. Python "
        "shows each piece with `'` marks. It is the same text.\n"
        "Bomb Shell talks in short, clipped sentences: \"Latch stuck. Shield up.\""
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
            "With empty parentheses, `.split()` cuts at every space: four pieces, in a list. The periods stay on "
            "their words, and the spaces are gone."
        ),
    ),
    starter=CLIP_STARTER,
    checkpoints=[
        dict(
            id="split-the-report",
            text="On line 3, change `sentences = []` so `sentences` holds `report.split(\". \")`: the report cut "
                 "at each period and space.",
            dictated=True,
            hints=[
                "Look at line 3, `sentences = []`. The pieces come from `report`, on line 1.",
                "`\"rope, salt\".split(\", \")` gives `['rope', 'salt']`. What you put in the parentheses is where "
                "the cuts go, and it disappears.",
                "Write `" + SPLIT_LINE + "` in place of `sentences = []`.",
            ],
            checks=[SPLIT_CHECK],
            pass_line="`sentences` holds two pieces. Bomb Shell: Two sentences. Logged.",
        ),
        dict(
            id="count-the-words",
            text="On line 7, change `word_count = 0` so `word_count` holds how many words `report` has. Let "
                 "Python count them.",
            dictated=False,
            hints=[
                "Look at line 7. It takes two steps: split `report` into words, then count the pieces.",
                "`len()` counts the items in a list: `len([\"rope\", \"salt\"])` is 2. Given text, `len()` counts "
                "the letters and spaces instead.",
                "Two lines work too: `pieces = report.split()`, then `word_count = len(pieces)`.",
                "Write `" + COUNT_LINE + "` in place of `word_count = 0`.",
            ],
            checks=[COUNT_CHECK],
            pass_line="`word_count` is 4. Bomb Shell: Four words. Enough.",
        ),
        dict(
            id="digits-to-a-number",
            text="Under `# 3.`, change `next_hours = 0` so `next_hours` is the number in `hours_text`, plus one. "
                 "`int()` turns digits into a number: `int(\"12\")` is 12.",
            dictated=False,
            hints=[
                "Look at the line above it: `hours_text` holds `\"48\"`, in quotes. That is text, and text can't do "
                "math.",
                "`int(\"12\") + 3` is 15. Without `int()`, `\"12\" + 3` is an error, like adding 5 meters to 3 "
                "seconds. `int(\"twelve\")` is an error too: only digits turn into a number.",
                "Write `" + INT_LINE + "` in place of `next_hours = 0`.",
            ],
            checks=[INT_CHECK],
            pass_line="`next_hours` is 49, a number. Mar'tu: Now it can do math, yes?",
        ),
        dict(
            id="join-them-back",
            text="Under `# 4.`, change `joined = \"\"` so `joined` holds the words in `words` glued into one "
                 "text, with a space between them.",
            dictated=False,
            hints=[
                "Look at the `joined = \"\"` line. `.join` is asked of the glue, not of the list. What goes between the "
                "words?",
                "`\"-\".join([\"rope\", \"salt\"])` gives `rope-salt`. Asking the list, `words.join(\" \")`, is an "
                "error: a list has no `.join`.",
                "Write `" + JOIN_LINE + "` in place of `joined = \"\"`.",
            ],
            checks=[JOIN_CHECK],
            pass_line="The two words are one line again. Gearshift: Barrier's holding.",
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
             message_contains="Empty parentheses cut at every space"),
        dict(why="split at the full stop alone", code=_clipped('sentences = report.split(".")'), fails_at=1,
             message_contains="period alone"),
        dict(why="no (): the method itself", code=_clipped("sentences = report.split"), fails_at=1,
             message_contains="Add `()`"),
        dict(why="still the text, not a list", code=_clipped("sentences = report"), fails_at=1,
             message_contains="holds text, not a list"),
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
             fails_at=4, message_contains="with its square brackets"),
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
assert _tn(_o) == 'str', 'The line `note = "  It\'s a compass.  "` is missing or changed. Put it back as it was at the start.'
assert 'note' in globals(), 'The variable `note` is missing or changed. Put it back as it was at the start.'
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
        '`.' + _v.__name__ + '` has no `()`, so the method never ran: `note` holds the method itself, not text. '
        'Add `()` after `.' + _v.__name__ + '`' + (', with the old and new words inside' if _v.__name__ == 'replace'
                                                   else '') + '.')
    assert _tn(_v) == 'str', '`note` is not text now. Keep it as text: the copy that `.strip()` hands back.'
    assert not (_v == _o and _bare('strip')), (
        '`note.strip()` made a copy, and nothing kept it. Catch the stripped copy: put it in `note` with `note = `.')
    _nb = _newbox(_base, ('note',))
    assert not (_v == _o and _nb), (
        '`' + (_nb or [''])[0] + '` holds the stripped copy, but `note` still has its spaces. Put the copy in '
        '`note` itself: start the line with `note = `.')
    assert _v != _o, '`note` still has its spaces. Cut them off and put the copy back in it: `note = note.strip()`.'
    assert _v == _v.strip(), 'Spaces are still on one end. `.strip()` cuts both ends.'
    assert _v.replace('LeyClock', 'compass') != _base.replace(' ', ''), (
        'That took out every space, even between the words. `.strip()` cuts only the spaces at the ends.')
    assert False, ('`note` is not the stripped note yet. Make it hold itself with the spaces cut off both ends: '
                   '`note = note.strip()`.')
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2}, 'note')
assert not _miss, "Mar'tu can't test your code with another note: the line `note = ...` is missing or changed. Put it back as it was at the start."
assert not _err, "With another note, your code stopped. Python's last line: `" + _err + "`." + _tried({'note': _o2})
_nv = _ns.get('note')
assert _o2.strip() in _rerun.hist or _ends_ok(_nv, _o2) or not (_tn(_nv) == 'str' and _nv != _nv.strip()), (
    'With another note, a space was left at one end. Cut the spaces with `.strip()`, so however many there are, '
    'they all go.' + _tried({'note': _o2}))
assert _o2.strip() in _rerun.hist or _ends_ok(_nv, _o2), (
    'With another note, `note` did not change to match. Strip `note` itself, instead of typing the words in.'
    + _tried({'note': _o2}))
''',
    OTHER=OTHER_NOTE,
)

SWAP_CHECK = chk(
    "note says Ley Clock where it said compass, for another note too",
    _NOTE_BASE + r'''
_want = _base.replace('compass', 'Ley Clock')
if _v != _want:
    assert not _is_method(_v), (
        '`.' + _v.__name__ + '` has no `()`, so the method never ran: `note` holds the method itself, not text. '
        'Add `()` after `.' + _v.__name__ + '`' + (', with the old and new words inside' if _v.__name__ == 'replace'
                                                   else '') + '.')
    _args = [[_a.value for _a in _n.args if _tn(_a) == 'Constant'] for _n in _ast.walk(_parsed())
             if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute' and _n.func.attr == 'replace']
    assert not (_v == _base and _any(_a[:1] == ['Compass'] for _a in _args)), (
        '`.replace` found no `Compass`, so nothing changed. Match the capitals exactly: the note says `compass`, '
        'with a small c.')
    assert not (_v == _base and _any(_a[:1] == ['Ley Clock'] for _a in _args)), (
        'The note has no Ley Clock to swap yet, so nothing changed. Put the old words first: `.replace(old, new)`.')
    assert not (_v == _base and _bare('replace')), (
        '`.replace` made a copy, and nothing kept it. Catch the swapped copy: put it in `note` with `note = `.')
    assert _tn(_v) != 'str' or _v.lower() != _want.lower(), "`Ley Clock` needs its two capitals. Write it the way Mar'tu does."
    assert _v != _base, '`note` still says `compass`. Make it say `Ley Clock` there, with `.replace`.'
    assert False, '`note` is not right yet. Make it say `Ley Clock` where it says `compass`. Swap only that word.'
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err, "With another note, your code stopped. Python's last line: `" + _err + "`." + _tried({'note': _o2})
assert _ns.get('note') == _o2.strip().replace('compass', 'Ley Clock'), (
    'With another note, `note` did not change to match. Swap the word inside `note` itself, instead of typing '
    'the words in.' + _tried({'note': _o2}))
''',
    OTHER=OTHER_NOTE,
)

FIND_CHECK = chk(
    "spot is the place where Ley starts in note, for another note too",
    _NOTE_BASE + r'''
assert 'spot' in globals(), 'The line `spot = ...` is missing or changed. Put it back as it was at the start.'
_sp = globals()['spot']
if not (_tn(_sp) == 'int' and _sp == _v.find('Ley')):
    assert _tn(_sp) != 'bool', ('`spot` holds True or False: `in` answers yes or no. This step wants the position, '
                                'a number. Ask with `.find`.')
    assert _tn(_sp) != 'str', '`spot` holds a letter, not a position. `.find` hands back the position, a number.'
    assert _sp != -1, (
        '`spot` is -1, and -1 means not found. It is not the last letter. Look for `"Ley"`, written exactly as the '
        'note writes it.')
    assert not (_sp == 0 and _first_lit('spot') == 0 and _len(_assigns('spot')) == 1), (
        "`spot` still holds the 0 it started with. Make it hold the position where `\"Ley\"` starts.")
    assert False, ('`spot` does not hold the right position yet. Make it hold the position where `"Ley"` starts in '
                   '`note`, found with `.find`.')
_o2 = __OTHER__
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err, "With another note, your code stopped. Python's last line: `" + _err + "`." + _tried({'note': _o2})
assert _ns.get('spot') == _ns.get('note', '').find('Ley'), (
    'With another note, it stayed ' + _str(_sp) + '. Find it with `.find`, so `spot` changes to match.'
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
assert _tn(_s) == 'str' and ',' in _s, 'There is no `sign = "Greenroom, Interior"` line yet. Write it under the last `print`.'
assert 'word' in globals(), 'There is no `word` yet. Under the `sign` line, make `word` the word before the comma.'
_w = globals()['word']
assert _w == _s[:_s.find(',')], (
    "`word` is not the word before the comma. Slice `sign` from the start up to the comma's position.")
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'sign': _o})
assert not _miss, "Mar'tu can't test your code with another sign: the line `sign = ...` needs its text in quotes."
assert not _err, "With another sign, your code stopped. Python's last line: `" + _err + "`." + _tried({'sign': _o})
assert _ns.get('word') == _o[:_o.find(',')], (
    'With another sign, the comma sat at another position, and `word` came out wrong. Find the comma with '
    '`sign.find(",")`, so the slice ends wherever the comma is.' + _tried({'sign': _o}))
''',
    OTHER=OTHER_COMMA_SIGN,
)

STRIP_AND_REPLACE = dict(
    id="strip-and-replace",
    title="Clean-up tools",
    martu=(
        "Three more [[method|methods]], like the tools in a word processor. [[.strip()]] cuts the spaces off both "
        "ends, like trimming the edges of a page. [[.replace()]] swaps old words for new ones, like Find and "
        "Replace: `.replace(old, new)`. [[.find()]] hands back the position where some text starts, like Find "
        "(Ctrl+F), or `-1` when it isn't there.\n"
        "Here `-1` means *not found*. It is not the last letter. All three match capitals exactly. And like every "
        "string method, they hand back something new, so catch it: `tag = tag.strip()`.\n"
        "Lucky left a note on the mantel (the shelf over the fireplace). It has spaces at both ends, and it is "
        "wrong."
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
            "`room` starts at position 5: G is 0. `\"Room\"` with a capital R is not in `Greenroom`, so `.find` "
            "hands back -1, which means not found."
        ),
    ),
    starter=NOTE_STARTER,
    checkpoints=[
        dict(
            id="strip-the-note",
            text="On line 3, change `note = note` to `note = note.strip()`. That cuts the spaces off both ends "
                 "of `note` and keeps the copy.",
            dictated=True,
            hints=[
                "Look at the Console: it shows `[  It's a compass.  ]`. The square brackets show the spaces at both "
                "ends.",
                "`\"  hi  \".strip()` hands back `hi`. Catch it with `=`, or the copy is gone.",
                "Write `" + STRIP_LINE + "` in place of the `note = note` line under `# 1.`.",
            ],
            checks=[STRIP_CHECK],
            pass_line="No spaces at the ends now. Mar'tu: Tidier. Still wrong.",
        ),
        dict(
            id="swap-the-word",
            text="On line 6, change `note = note` so `note` says `Ley Clock` (the clock that counts down to the next "
                 "burst) where it says `compass`.",
            dictated=False,
            hints=[
                "Look at line 6. The swap is a method too. It needs two things in its parentheses: the old words "
                "first, then the new ones.",
                "`\"Rust Ward\".replace(\"Rust\", \"Moon\")` hands back `Moon Ward`. Catch it with `=`, the same as "
                "the strip.",
                "Write `" + SWAP_LINE + "` in place of the `note = note` line under `# 2.`.",
            ],
            checks=[SWAP_CHECK],
            pass_line="The note says Ley Clock now. Mar'tu: Thank you.",
        ),
        dict(
            id="find-a-rune",
            text="On line 9, change `spot = 0` so `spot` holds the position where `\"Ley\"` starts in `note`. "
                 "Find it with `.find`.",
            dictated=False,
            hints=[
                "Look at line 9. `.find` hands back a position, counted from 0. Ask `note` where `\"Ley\"` starts.",
                "`\"Moon Ward\".find(\"Ward\")` is 5. `.find(\"ward\")` is -1: a small w is not there. -1 means not "
                "found.",
                "Write `" + FIND_LINE + "` in place of `spot = 0`.",
            ],
            checks=[FIND_CHECK],
            pass_line="`spot` is 7: Ley starts at position 7. Mar'tu: A word found by its position. Good.",
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
            "The Greenroom sign again. Under the last `print`, write `sign = \"Greenroom, Interior\"`. Then make "
            "`word` the word before the comma, for any sign: let `.find(\",\")` count to the comma for you."
        ),
        hints=[
            "`sign.find(\",\")` hands back the comma's position. A slice `[:n]` stops right before position n, "
            "so it stops right before the comma, wherever it is.",
            "Write `sign = \"Greenroom, Interior\"`, then `word = sign[:sign.find(\",\")]`, below the prints.",
        ],
        checks=[ANY_SIGN_CHECK],
        solution=NOTE_SOLUTION + ANY_SIGN_LINES,
    ),
    takeaway="`.strip()` trims the ends, `.replace(old, new)` swaps, `.find(x)` gives a position or -1 for not found.",
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
             message_contains="`tag` holds the stripped copy"),
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
             fails_at=3, message_contains="a letter, not a position"),
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
assert _tn(_n) == 'str' and _tn(_m) == 'int', 'The lines `name = "Bomb Shell"` and `mana = 24` are missing or changed. Put them back as they were at the start.'
assert 'line' in globals(), 'The variable `line` is missing or changed. Put it back as it was at the start.'
_v = globals()['line']
_as = _assigns('line')
assert not (_tn(_v) == 'str' and '{' in _v and '}' in _v), (
    '`line` shows the curly braces as they are, because there is no `f`. Put an `f` right before the first quote '
    'mark.')
assert _as and _tn(_as[-1].value) == 'JoinedStr', (
    'The `line =` line is not an f-string yet. Write it with an `f` before the quote marks, and each variable '
    'inside curly braces `{ }`.')
_fparts = _as[-1].value.values
_plain = ''.join([_p.value for _p in _fparts if _tn(_p) == 'Constant' and _tn(_p.value) == 'str'])
_braced = {_x.id for _p in _fparts if _tn(_p) == 'FormattedValue' for _x in _ast.walk(_p.value) if _tn(_x) == 'Name'}
_worded = [_w for _w in ('name', 'mana') if _w not in _braced and _re.search(r'\b' + _w + r'\b', _plain)]
assert _v == _n + ': ' + _str(_m) or not _worded, (
    '`line` shows the word ' + (_worded or [''])[0] + ', because `' + (_worded or [''])[0] + '` has no curly braces '
    'around it. Write it as `{' + (_worded or [''])[0] + '}`.')
assert _v == _n + ': ' + _str(_m), (
    '`line` does not print what it printed before. Keep the same words and spaces around the variables: a colon, '
    'then one space.')
_vals = {'name': 'Pell', 'mana': 9}
_ns, _rows, _err, _miss = _rerun(_vals)
assert not _miss, "Mar'tu can't test your code with other values: the lines `name = ...` and `mana = ...` are missing or changed. Put them back as they were at the start."
assert not _err, "With other values, your code stopped. Python's last line: `" + _err + "`." + _tried(_vals)
assert _ns.get('line') == 'Pell: 9', (
    'With other values, `line` did not change to match. Put each variable inside `{ }`, instead of typing the '
    'words in.' + _tried(_vals))
''',
)

PLUS_CHECK = chk(
    "fuel is glued with + and str(), and prints the same, for another number too",
    r'''
_d = globals().get('days')
assert _tn(_d) == 'int', 'The line `days = 7` is missing or changed. Put it back as it was at the start.'
assert 'fuel' in globals(), 'The variable `fuel` is missing or changed. Put it back as it was at the start.'
_v = globals()['fuel']
_as = _assigns('fuel')
assert not (_as and _tn(_as[-1].value) == 'JoinedStr'), (
    '`fuel` is still an f-string. Write it with `+` and `str()` this time: no `f`, and no `{ }`.')
_noadd = bool(_as and _tn(_as[-1].value) != 'Constant'
              and not _any(_tn(_x) == 'BinOp' and _tn(_x.op) == 'Add' for _x in _ast.walk(_as[-1].value)))
assert not (_noadd and _v == 'Ore: ' + _str(_d) + ' days'), (
    'That works, but this step practices `+` and `str(days)`. Glue the pieces with `+` and `str(days)` this time, '
    'the way the campaign does.')
assert not _noadd, '`fuel` is not glued with `+`. Glue the pieces with `+` and `str(days)` this time, the way the campaign does.'
assert not (_tn(_v) == 'str' and '{' in _v), (
    'Without an `f`, the braces print as they are. Glue `days` in with `+` and `str(days)`.')
assert not (_tn(_v) == 'str' and 'days days' in _v), ('`fuel` shows the word days twice. ' + _QUOTES
                                                      + ' Glue in `str(days)`, with no quotes around `days`.')
assert _v == 'Ore: ' + _str(_d) + ' days', (
    '`fuel` does not print what it printed before. Keep the same words and spaces, like `Ore: 7 days`.')
_ns, _rows, _err, _miss = _rerun({'days': 3})
assert not _miss, "Mar'tu can't test your code with another number: the line `days = 7` is missing or changed. Put it back as it was at the start."
assert not _err, "With another number, your code stopped. Python's last line: `" + _err + "`." + _tried({'days': 3})
assert _ns.get('fuel') == 'Ore: 3 days', (
    'With another number, `fuel` did not change to match. Glue in `days` itself with `str(days)`.'
    + _tried({'days': 3}))
''',
)

F_STRINGS = dict(
    id="f-strings",
    title="f-strings",
    martu=(
        "An [[f-string]] is text with blanks, like Mad Libs in English class. Put an `f` right before the quotes, "
        "and write each variable inside curly braces `{ }`. Python fills each blank with what the variable holds. "
        "When `name` holds Lucky and `mana` holds 26, `f\"{name}: {mana} mana\"` gives `Lucky: 26 mana`. Inside "
        "`{ }`, no `str()` is needed.\n"
        "The campaign builds the same line another way, gluing with `+` and `str()`:\n"
        "```python\nname + \": \" + str(mana) + \" mana\"\n```\n"
        "Read both. Write whichever you like. If you want, put your own hero in `name`: any name in quotes."
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
            "Without the `f`, the braces are plain letters, so Python prints them as they are. With the `f`, "
            "Python fills each blank from its variable."
        ),
    ),
    pair_talk="Tell your partner why `mana` needs `str()` in the `+` line, but not inside the f-string.",
    starter=FSTR_STARTER,
    checkpoints=[
        dict(
            id="plus-to-f-string",
            text="On line 4, rewrite the `line =` line as an f-string. It must print exactly what it printed "
                 "before.",
            dictated=False,
            hints=[
                "Look at line 4. An f-string starts with `f\"`. Every piece goes inside one pair of quotes, and each "
                "variable goes inside `{ }`.",
                "From the Example: `cart + \" x\" + str(bags)` became `f\"{cart} x{bags}\"`. The text between the "
                "variables stays as it is.",
                "Write `" + LINE_F + "` in place of `" + LINE_PLUS + "`.",
            ],
            checks=[FSTR_CHECK],
            pass_line="Same line, now an f-string. Bomb Shell: Fewer pieces.",
        ),
        dict(
            id="f-string-to-plus",
            text="On line 9, rewrite the `fuel =` line with `+` and `str()`, with no f-string. It must print the "
                 "same.",
            dictated=False,
            hints=[
                "Look at line 9. Glue three pieces with `+`: the text before `{days}`, the number made into text, "
                "and the text after it.",
                "`f\"{cart} x{bags}\"` became `cart + \" x\" + str(bags)`. A number needs `str()` before `+` can "
                "glue it to text.",
                "Write `" + FUEL_PLUS + "` in place of `" + FUEL_F + "`.",
            ],
            checks=[PLUS_CHECK],
            pass_line="Same line, glued the campaign's way. Mar'tu: Two ways to say the same thing, yes?",
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
        dict(why="the starter: still glued with +", code=FSTR_STARTER, fails_at=1, message_contains="not an f-string yet"),
        dict(why="an f-string without the f: the braces print", code=_fstr('line = "{name}: {mana}"'), fails_at=1,
             message_contains="Put an `f`"),
        dict(why="a variable's name typed as a word: no curly braces around name", code=_fstr('line = f"name: {mana}"'),
             fails_at=1, message_contains="no curly braces"),
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
             fails_at=2, message_contains="no quotes around"),
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
    assert not _e, _why('lucky_reply', _e, __FOREIGN__) + _crash_ev(_ev)
    _res.append((_a, _p, _v, _ev))
assert not (_tn(_res[0][2]) == 'str' and '{' in _res[0][2] and '}' in _res[0][2]), (
    '`lucky_reply` hands back the curly braces as they are, because there is no `f`. Put an `f` right before the '
    'first quote mark, or glue the pieces with `+`.' + _res[0][3])
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    "`lucky_reply` gives the same reply to everything. Build the reply from `request`, so it changes with what is "
    "asked. Mar'tu tested your function with two test requests: both replies were the same.")
for _a, _p, _v, _ev in _res:
    if _v == _a.strip().capitalize() + _ASK:
        continue
    assert not (_v is None and _p), (
        '`lucky_reply` printed the reply, then handed back `None`. Hand back the reply with `return`, not `print`.' + _ev)
    assert _v is not None, '`lucky_reply` handed back `None`. End it with `return`, so it hands the reply back.' + _ev
    assert not _is_method(_v), (
        '`.' + _v.__name__ + '` has no `()`, so the method never ran: `lucky_reply` hands back the method itself, not '
        'text. Add `()` after `.' + _v.__name__ + '`.' + _ev)
    assert _tn(_v) == 'str', '`lucky_reply` did not hand back text. Hand back the tidy request, then the question.' + _ev
    assert "what's in it for me?" in _v.lower(), (
        "Lucky's question is missing. Glue it on the end: ` What's in it for me?`, with a space in front." + _ev)
    assert _v.endswith("What's in it for me?"), (
        "Lucky's question is not exact. Write it at the very end: ` What's in it for me?`, with a capital W." + _ev)
    assert _v.endswith(_ASK), "The question touches the request. Put one space before `What's`." + _ev
    _head, _core = _v[:-_len(_ASK)], _a.strip()
    _used = [_n.attr for _n in _ast.walk(_fdef('lucky_reply')) if _tn(_n) == 'Attribute']
    assert not (_head != _head.strip() and _bare('strip')), (
        '`request.strip()` on its own line makes a copy, then nothing keeps it. Catch the stripped copy with `=`.'
        + _ev)
    assert _head == _head.strip(), ('The reply still has spaces at the ends of the request. Strip them off '
                                    '`request` first, with `.strip()`.' + _ev)
    assert not (_head == _core.lower() and 'capitalize' not in _used), (
        'The request has no capital first letter. Give it one with `.capitalize()`, after `.strip()`.' + _ev)
    assert _head != _core.lower(), (
        'With the spaces still on, `.capitalize()` met a space, and nothing got a capital. Strip first, then '
        'capitalize.' + _ev)
    assert _head != _core, ('The request kept its old capitals. Capitalize it: `.capitalize()` makes the first letter '
                            'big and the rest small.' + _ev)
    assert _head != _core.title(), (
        '`lucky_reply` used `.title()`: a capital on every word. `.capitalize()` makes only the first letter big.' + _ev)
    assert False, ("The reply is not right yet. Hand back the request, stripped and capitalized, then "
                   "` What's in it for me?`." + _ev)
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
        "Python stopped inside `clip` on a short sentence. Python's last line: `" + _e + "`. A position past the end "
        "stops Python, but a slice like `[:3]` takes what is there. Make `clip` work for short sentences too." + _ev)
    assert not _e, _why('clip', _e, __FOREIGN__) + _crash_ev(_ev)
    _res.append((_a, _p, _v, _ev, _want))
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    "`clip` gives the same text for any sentence. Build the short version from `sentence`, so it changes with what "
    "is handed in. Mar'tu tested your function with two test sentences: both gave the same text.")
for _a, _p, _v, _ev, _want in _res:
    if _v == _want:
        continue
    assert not (_v is None and _p), (
        '`clip` printed the short version, then handed back `None`. Hand it back with `return`, not `print`.' + _ev)
    assert _v is not None, '`clip` handed back `None`. End it with `return`, so it hands the short version back.' + _ev
    assert _tn(_v) != 'list', ('`clip` handed back a list, not text. Join the words back into text with '
                               '`" ".join(...)`, then glue on the period.' + _ev)
    assert _tn(_v) == 'str', '`clip` did not hand back text. Hand back three words and a period.' + _ev
    assert not _v.startswith('['), (
        '`clip` handed back the list written out, with its square brackets. Join the words with `" ".join(...)`.' + _ev)
    assert _v.endswith('.'), 'The period is missing. Glue it on the end, with `+ "."`.' + _ev
    _body, _w = _v[:-1], _a.split()
    assert not (_len(_w) > 2 and _body == ' '.join(_w[:2])), (
        '`clip` handed back two words. A slice leaves its end out, so `[:3]` takes three: positions 0, 1 and 2.' + _ev)
    assert not (_len(_w) > 3 and _body == ' '.join(_w[:4])), (
        '`clip` handed back four words. `[:3]` takes three: positions 0, 1 and 2.' + _ev)
    assert _body != ''.join(_w[:3]), 'The words touch. Put a space between the quotes before `.join`.' + _ev
    assert _body != _a[:3], ('`clip` handed back three letters. Split `sentence` into words first, then take three '
                             'of them.' + _ev)
    assert _body != ' '.join(_w[1:4]), '`clip` skipped the first word. Start at position 0: the first word is position 0.' + _ev
    assert False, ('The short version is not right yet. Hand back the first three words of `sentence`, joined with '
                   'spaces, then a period.' + _ev)
''',
    CASES=["Moving out before the burst", "Optic is dim again tonight", "Shield up"],
    FOREIGN=REPLY_FOREIGN.split(","),
)

MARTU_REPLY_CHECK = chk(
    "martu_reply clips the sentence and ends with , yes?",
    r'''
_f = globals().get('martu_reply')
assert _B.callable(_f), 'There is no function named `martu_reply` yet. Write one, with one parameter, `sentence`.'
for _a in ('Optic is dim again tonight', 'Moving out before the burst'):
    _p, _v, _e = _call(_f, _a)
    _want = ' '.join(_a.split()[:3]) + ', yes?'
    _ev = _called('martu_reply', (_a,), 'it should hand back `' + _want + '`')
    assert not _e, _why('martu_reply', _e, __FOREIGN__) + _crash_ev(_ev)
    assert _v == _want, ('`martu_reply` does not hand back the right line yet. Hand back the clipped sentence with '
                         'its period cut off, then `, yes?`.' + _ev)
_fd = _fdef('martu_reply')
assert _any(_tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'clip' for _n in _ast.walk(_fd)), (
    '`martu_reply` does not call `clip`. Call `clip` inside it, so the clipping is done in one spot.')
''',
    FOREIGN=REPLY_FOREIGN.split(","),
)

WHATS_IN_IT_FOR_ME = dict(
    id="whats-in-it-for-me",
    title="Two functions of your own",
    martu=(
        "Now write two functions of your own, built from tools you know. A function is a recipe with a name, as in "
        "Unit 3: the same steps, for any line you hand it. Lucky answers every request the same way. Bomb Shell answers in three "
        "words, then stops.\n"
        "1. `lucky_reply(request)` hands back the request, stripped and capitalized, then ` What's in it for me?`.\n"
        "2. `clip(sentence)` hands back the first three words of `sentence`, joined with spaces, then a period.\n"
        "You know every piece already: `.strip()`, `.capitalize()`, `.split()`, a slice and `.join()`. In the last "
        "lines, ask Lucky anything you like."
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
            text="Replace `pass` on line 2. Make `lucky_reply` hand back `request`, stripped and capitalized, then "
                 "` What's in it for me?`.",
            dictated=False,
            hints=[
                "Look at line 2, inside `lucky_reply`. Which two methods tidy `request`, and which one goes first? "
                "Then glue the question on the end with `+`. It starts with a space.",
                "The Example's `shout` takes three moves: strip, then a method, then `return order + \"!\"`. Here "
                "the method is `.capitalize()`, and the end is Lucky's question.",
                "Strip first, or `.capitalize()` meets a space. Keep Lucky's question in double quotes: it has an "
                "apostrophe.",
                "Write `tidy = request.strip()` in place of `pass`. Under it, `tidy = tidy.capitalize()`, then "
                "`return tidy + \" What's in it for me?\"`.",
            ],
            checks=[REPLY_CHECK],
            pass_line="`lucky_reply` tidies any request. Mar'tu: What's in it for you, Lucky? Existing.",
        ),
        dict(
            id="clip",
            text="Replace `pass` inside `clip` so it hands back the first three words of `sentence`, joined with "
                 "spaces, then a period. A shorter sentence keeps all its words.",
            dictated=False,
            hints=[
                "Look at `pass` inside `clip`. `sentence` is one text: which method cuts it into a list of words, so "
                "a slice can keep three?",
                "`[\"a\", \"b\", \"c\", \"d\"][:3]` is `['a', 'b', 'c']`. A short list never breaks it: "
                "`[\"a\", \"b\"][:3]` is `['a', 'b']`.",
                "```python\nbits = [\"a\", \"b\", \"c\", \"d\"]\nprint(\"-\".join(bits[:2]))\n```\nThat shows `a-b`: "
                "slice first, then join.",
                "Write `words = sentence.split()` in place of the `pass` inside `clip`. Then "
                "`short = \" \".join(words[:3])`, then `return short + \".\"`.",
            ],
            checks=[CLIP_CHECK],
            pass_line="`clip` keeps three words. Bomb Shell: Three words. Done.",
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
            label="Copy after copy",
            text=(
                "```text\n\"  carry this  \"\n  .strip()\n\"carry this\"\n  .capitalize()\n\"Carry this\"\n"
                "  + ask\n\"Carry this What's ...\"\n```"
            ),
        ),
        dict(
            angle="step-by-step",
            text=(
                "`clip`:\n1. `sentence.split()`: a list of words.\n2. `[:3]`: the first three, or fewer.\n"
                "3. `\" \".join(...)`: back to text.\n4. `+ \".\"`: Bomb Shell's period."
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
            "At the bottom of your code, write a new function, `martu_reply(sentence)`. It calls `clip`, cuts the "
            "period off with `[:-1]`, and glues on `, yes?`. So `martu_reply(\"Optic is dim again tonight\")` should hand back "
            "`Optic is dim, yes?`."
        ),
        hints=[
            "`[:-1]` is every letter but the last: `\"Glug.\"[:-1]` is `Glug`.",
            "Start with `def martu_reply(sentence):`. Under it, four spaces in, write `short = clip(sentence)`, then "
            "`return short[:-1] + \", yes?\"`.",
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
             fails_at=1, message_contains="still has spaces at the ends"),
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
             message_contains="Lucky's question is missing"),
        dict(why="an apostrophe inside single quotes (SyntaxError)",
             code=_reply(REPLY_BODY.replace("\" What's in it for me?\"", "' What's in it for me?'")), fails_at=0,
             message_contains="unterminated string literal"),
        dict(why="typed: the starter call's own answer", code=_reply("    return \"Carry this What's in it for me?\"\n"),
             fails_at=1, message_contains="both replies were the same"),
        dict(why="clip not started (the partial)", code=_reply(REPLY_BODY), fails_at=2, message_contains="handed back `None`"),
        dict(why="clip: a slice one short, [:2]", code=_reply(REPLY_BODY, CLIP_BODY.replace("[:3]", "[:2]")), fails_at=2,
             message_contains="two words"),
        dict(why="clip: the sliced list glued to text with + (TypeError on the student's own Run)",
             code=_reply(REPLY_BODY, "    words = sentence.split()\n    return words[:3] + \".\"\n"), fails_at=0,
             message_contains="can only concatenate list"),
        dict(why="lucky_reply: an f-string with no f, the braces shown as they are",
             code=_reply("    tidy = request.strip().capitalize()\n    return \"{tidy} What's in it for me?\"\n", CLIP_BODY),
             fails_at=1, message_contains="there is no `f`"),
        dict(why="lucky_reply: the Example's order copied, the calls kept (UnboundLocalError on the student's own Run)",
             code=_reply("    order = order.strip()\n    order = order.capitalize()\n"
                         "    return order + \" What's in it for me?\"\n", CLIP_BODY), fails_at=0,
             message_contains="cannot access local variable 'order'"),
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
             message_contains="`order` comes from Mar'tu's example: the parameter of `clip` is `sentence`."),
        dict(why="lucky_reply: a near-miss of the parameter, reqest (the calls taken out: _why)",
             code=_reply(REPLY_BODY.replace("request.strip()", "reqest.strip()"), CLIP_BODY, calls=""), fails_at=1,
             message_contains="You wrote `reqest`, but the parameter of `lucky_reply` is `request`"),
        dict(why="clip: join called the wrong way round (AttributeError)",
             code=_reply(REPLY_BODY, CLIP_BODY.replace('" ".join(words[:3])', 'words[:3].join(" ")')), fails_at=0,
             message_contains="'list' object has no attribute 'join'"),
        dict(why="clip: the list handed back, not text", code=_reply(REPLY_BODY, "    return sentence.split()[:3]\n"),
             fails_at=2, message_contains="Join the words back"),
        dict(why="clip: the list written out with str()",
             code=_reply(REPLY_BODY, "    words = sentence.split()\n    return str(words[:3]) + \".\"\n"), fails_at=2,
             message_contains="with its square brackets"),
        dict(why="clip: three letters, not three words", code=_reply(REPLY_BODY, '    return sentence[:3] + "."\n'),
             fails_at=2, message_contains="three letters"),
        dict(why="clip: no period", code=_reply(REPLY_BODY, CLIP_BODY.replace('short + "."', "short")), fails_at=2,
             message_contains="The period is missing"),
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
assert _tn(_o) == 'str', 'The line `note = "THE CLOCK IS RED."` is missing or changed. Put it back as it was at the start.'
assert globals().get('note') == _o.lower().capitalize(), (
    '`note` is not the tidy copy yet. Fix line 3: call `.lower` with `()`.')
_o2 = 'SHIELD UP NOW.'
_ns, _rows, _err, _miss = _rerun({'note': _o2})
assert not _err and _ns.get('note') == 'Shield up now.', (
    'With another note, `note` did not change to match. Make the copy from `note` itself, instead of typing it in.'
    + _tried({'note': _o2}))
_low = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
        and _n.func.attr == 'lower' and _tn(_n.func.value) == 'Name' and _n.func.value.id == 'note']
assert _low, (
    'The note still prints right, because `.capitalize()` lowers the rest. But this step practices the `()`: fix '
    'line 3 by giving `.lower` its `()`, instead of taking it out.')
''',
)

B_JOIN_CHECK = chk(
    "the words print glued with a space, for another list too",
    r'''
_wd = globals().get('words')
assert _tn(_wd) == 'list', 'The list `words` is missing or changed. Put it back as it was at the start.'
assert ' '.join(_wd) in _lines(), (
    'The words do not show with a space between them yet. Fix line 9: ask the glue, `" "`, to `.join` them.')
_o = ['Optic', 'dim', 'tonight.']
_ns, _rows, _err, _miss = _rerun({'words': _o})
assert not _err and 'Optic dim tonight.' in _rows, (
    'With three words, the line did not change to match. Glue the words of `words` with `.join`.'
    + _tried({'words': _o}))
_glue = [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Call' and _tn(_n.func) == 'Attribute'
         and _n.func.attr == 'join' and not (_tn(_n.func.value) == 'Name' and _n.func.value.id == 'words')]
assert _glue, (
    'That shows the words another way. This step practices which way round `.join` goes: fix line 9 so the glue, '
    '`" "`, joins them with `.join(words)`.')
''',
)

B_LAST_CHECK = chk(
    "the report's last word prints, for another report too",
    r'''
_rep = globals().get('report')
assert _tn(_rep) == 'str' and _rep.split(), 'The line `report = "Shield up now"` is missing or changed. Put it back as it was at the start.'
assert _rep.split()[-1] in _lines(), (
    'Line 14 does not print the last word. The list has 3 words, at positions 0, 1 and 2. Fix line 14 so it '
    'prints the last one.')
_o = 'Optic dims fast'
_ns, _rows, _err, _miss = _rerun({'report': _o})
assert not _err and 'fast' in _rows, (
    'With another report, the line did not change to match. Print a word from `parts`, instead of typing it in.'
    + _tried({'report': _o}))
''',
)

B_CALM_CHECK = chk(
    "calm keeps its lower-case copy, for other text too",
    r'''
_o = _first_lit('calm')
assert _tn(_o) == 'str', 'The line `calm = "STEADY, NOW."` is missing or changed. Put it back as it was at the start.'
_c = globals().get('calm')
if _c != _o.lower():
    assert not (_c == _o and _o.lower() in _lines()), (
        'The print showed the lower-case copy, but `calm` still holds capitals. Keep the copy in `calm`: start line 18 '
        'with `calm = `.')
    assert False, ('Line 18, `calm.lower()`, makes a copy, then nothing keeps it. Fix line 18: put the copy in '
                   '`calm` with `calm = `.')
assert _o.lower() in _lines(), 'The lower-case copy does not show in the Console. Print `calm` after it changes.'
_o2 = 'HOLD THE LINE.'
_ns, _rows, _err, _miss = _rerun({'calm': _o2})
assert not _err and _ns.get('calm') == 'hold the line.', (
    'With other text, `calm` did not change to match. Make the copy from `calm` itself, instead of typing it in.'
    + _tried({'calm': _o2}))
''',
)

BROKEN_SPELL_8B = dict(
    id="broken-spell-8b",
    title="Broken spell",
    martu=(
        "This code has four bugs. A *bug* is a mistake in code. Three are loud: Python stops with an error. One is "
        "quiet: the code runs, but shows the wrong thing, like a wrong word that spell-check can't catch.\n"
        "For a loud bug, read the box in the Console: the title first, then Python's last line, then the line "
        "number. Sometimes the mistake is on the line above the one where Python stopped.\n"
        "When no more errors appear, compare what shows in the Console with the comment above each part."
    ),
    names=["note", "words", "parts", "calm"],
    pair_talk=(
        "You may hunt these bugs together. One of you reads the box in the Console out loud. The other points at "
        "the line where Python stopped. Each of you fixes it on your own screen."
    ),
    starter=BROKEN_STARTER,
    checkpoints=[
        dict(
            id="mend-the-method",
            text="Fix line 3 so `note` holds a lower-case copy of the note.",
            dictated=False,
            hints=[
                "Read the title of the box in the Console. Then read Python's last line: "
                "`'builtin_function_or_method' object has no attribute 'capitalize'`. Python stopped at line 4, but "
                "the mistake is one line above.",
                "On line 4, `note` holds the method itself, not text. Line 3 put it there: `.lower` with no `()` is "
                "a method that never ran.",
                "A method runs only with `()`. In math class, f is the rule and f(3) is the answer. Here, "
                "`cry.lower` is the method, and `cry.lower()` is the copy it makes.",
                "Write `" + B_NOTE_GOOD + "` in place of `" + B_NOTE_BAD + "`.",
            ],
            checks=[B_NOTE_CHECK],
            pass_line="One loud bug fixed. Mar'tu: Python got further, yes?",
        ),
        dict(
            id="mend-the-join",
            text="Fix line 9 so it shows `Barrier's holding.`",
            dictated=False,
            hints=[
                "Read the title of the box in the Console. Then read Python's last line: "
                "`'list' object has no attribute 'join'`.",
                "A list can't join itself. `.join` belongs to the glue, the text that goes between the words.",
                "`\"-\".join([\"rope\", \"salt\"])` gives `rope-salt`: the glue first, then the list in the "
                "parentheses.",
                "Write `" + B_JOIN_GOOD + "` in place of `" + B_JOIN_BAD + "`.",
            ],
            checks=[B_JOIN_CHECK],
            pass_line="Two loud bugs fixed. Gearshift: Barrier's holding.",
        ),
        dict(
            id="mend-the-index",
            text="Fix line 14 so it shows the last word, `now`.",
            dictated=False,
            hints=[
                "Read the title of the box in the Console. Then read Python's last line: "
                "`IndexError: list index out of range`. It means a position past the end of the list.",
                "`report.split()` hands back 3 words, at positions 0, 1 and 2. Position 3 is past the end.",
                "`[-1]` is always the last item, however long the list is.",
                "Write `" + B_LAST_GOOD + "` in place of `" + B_LAST_BAD + "`.",
            ],
            checks=[B_LAST_CHECK],
            pass_line="Three loud bugs fixed. Mar'tu: Now the quiet one. Read what shows in the Console.",
        ),
        dict(
            id="mend-the-copy",
            text="Fix line 18 so `calm` keeps its lower-case copy.",
            dictated=False,
            hints=[
                "Look at the last line in the Console: `STEADY, NOW.`, still in capitals. The comment on line 16 says "
                "it should show `steady, now.`, in small letters.",
                "Line 18 makes a lower-case copy. Nothing catches it, so `calm` never changes.",
                "Catch a method's copy with `=`: `cry = cry.lower()`.",
                "Write `" + B_CALM_GOOD + "` in place of `" + B_CALM_BAD + "`.",
            ],
            checks=[B_CALM_CHECK],
            pass_line="Four bugs fixed, three loud and one quiet. Oogrish: Steady, now. You read the Console, not only the errors.",
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
                "1. Press Run. Line 4 stops it, but the mistake is on line 3. Fix it.\n2. Press Run again. A new "
                "error is good news: Python got further. Line 9 stops it next.\n3. Then line 14.\n4. Now nothing "
                "stops. Compare the Console with each comment: the last part is still in capitals."
            ),
        ),
        dict(
            angle="picture",
            label="Four bugs, four clues",
            text=(
                "```text\nline 3   .lower      -> line 4\n                        stops\nline 9   words.join  -> stops\n"
                "line 14  parts[3]    -> stops\nline 18  not kept    -> CAPS\n```"
            ),
        ),
        dict(angle="shorter", text="Call methods with `()`. Ask the glue to `.join`. Count from 0. Catch every copy."),
    ],
    takeaway="Call a method with `()`, ask the glue to join, count positions from 0, and catch every copy with `=`.",
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
             message_contains="positions 0, 1 and 2"),
        dict(why="bug 3 typed in", code=_mend(last='print("now")'), fails_at=3, message_contains="With another report"),
        dict(why="bug 4: printed, never kept", code=_mend(calm="print(calm.lower())"), fails_at=4,
             message_contains="The print showed the lower-case copy"),
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
    assert not _e, _why('whisper', _e, __FOREIGN__, True) + _crash_ev(_ev)
    _res.append((_a, _p, _v, _ev))
for _a, _p, _v, _ev in _res:
    _want = _a.strip().lower()
    if _v == _want:
        continue
    assert not (_v is None and _p), '`whisper` printed the line, then handed back `None`.' + _ev
    assert _v is not None, '`whisper` hands back `None`.' + _ev
    assert not _is_method(_v), '`whisper` hands back the method itself, not text: a method with no `()`.' + _ev
    assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
        '`whisper` hands back the same text for any line.' + _ev)
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

# Lean, proved: the SOLO's check never names its fix (as Unit 2's _leaned asserts for QC2's rewrites).
assert SOLO_B_GOOD.replace(" ", "") not in SOLO_B_CHECK[1].replace(" ", ""), "solo-8b's check names its fix"

SOLO_8B = dict(
    id="solo-8b",
    title="Show Mar'tu",
    martu=(
        "One quiet bug, for you alone. Python won't stop, so read what shows in the Console. `whisper` should hand "
        "back any line with the spaces cut off its ends, in small letters, yes?"
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
                "Look at the Console: the spaces are gone, but the line is still in capitals. The comment above the "
                "`print` line says it should be small.",
                "Two lines make a copy of `line`. Which copy is kept?",
                "A method hands back a new string: `cry = cry.lower()` keeps it.",
                "Write `line = line.lower()` on line 3.",
            ],
            checks=[SOLO_B_CHECK],
            pass_line="Mar'tu: You did that on your own. You caught a method's copy and kept it.",
        ),
    ],
    solution=SOLO_B_SOLUTION,
    # No assemble: from Unit 3 on a SOLO has none (its pieces would be the mended line; content.test.ts).
    another_way=[
        dict(angle="shorter", text="A method's copy is lost unless you keep it with `=` or hand it back."),
        dict(
            angle="step-by-step",
            text=(
                "1. `line = line.strip()` makes a copy with no end spaces, and keeps it.\n2. `line.lower()` makes a "
                "lower-case copy.\n3. Nothing keeps that one.\n4. `return line` hands back the stripped line, still in "
                "capitals."
            ),
        ),
    ],
    takeaway="A method hands back a new string, so keep it: `line = line.lower()`.",
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
             message_contains="same text for any line"),
        dict(why="printed, not handed back", code=_solo_b(SOLO_B_STRIP + "\n    print(line.lower())"), fails_at=1,
             message_contains="printed the line, then handed back"),
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
        "Text tools (methods) that hand back a changed copy: capitals, chains, split and join, strip, replace and "
        "find. Then f-strings, and two functions of your own."
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
        "8 questions on text tools, split and join, find, f-strings and a function. Retake it as often as you "
        "like."
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
                "comma and hands back a list, so `print` shows its square brackets and quotes."
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
            explain="There is no Z in EXIT, so `.find` hands back -1: not found. It is not the last position, which is 3.",
            notes="3 and T: -1 read as the last place or the last letter; an error: .index's habit.",
        ),
        dict(
            type="bug",
            id="join-the-glue",
            q="This should print `Latch stuck.`, but it stops with an error. Fix it.",
            code='words = ["Latch", "stuck."]\nprint(words.join(" "))\n',
            fix='words = ["Latch", "stuck."]\nprint(" ".join(words))\n',
            expected_output="Latch stuck.",
            explain="A list has no `.join`. Ask the glue instead: `\" \".join(words)` puts a space between the words.",
            notes="The AttributeError row (8B-03 CP4, 8B-09 CP2).",
        ),
        dict(
            type="mc",
            id="fstring-twin",
            q="Which line prints the same as the last line of this code?",
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
                2: "Text plus a number is an error: `mana` needs `str()` before `+` can glue it.",
                3: "In quotes, `name` is only the letters n, a, m, e. No quotes means look inside the variable.",
            },
            explain=(
                "Both give `Lucky: 26`. The f-string fills the blanks `{name}` and `{mana}`. The `+` line glues the "
                "same pieces, with `str()` for the number."
            ),
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
                "caught in `sign`, so the square brackets show `EDIT` with no spaces."
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
            explain="`.title()` gives every word a capital, like a book title. `.capitalize()` would give `Bomb shell`.",
            notes="A fill on `.title()`, so it no longer repeats Q1's `.lower().capitalize()` line.",
        ),
        dict(
            type="bug",
            id="hand-it-back",
            q="This should print `SHIELD UP.`, but it prints `None`. Fix it.",
            code='def shout(line):\n    line = line.upper()\n\nprint(shout("shield up."))\n',
            fix='def shout(line):\n    line = line.upper()\n    return line\n\nprint(shout("shield up."))\n',
            expected_output="SHIELD UP.",
            explain=(
                "No `return`, so `shout` hands back `None`, Python's word for nothing. End it with "
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
