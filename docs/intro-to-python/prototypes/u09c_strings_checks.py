"""Unit 9 "Strings" ("Runes and Ribbons"), part c: Quick Check 8 (forms qc8-a and qc8-b, three code tasks each, as
testout items, with their question forms qc8-a-questions and qc8-b-questions as optional quiz items) and the Strings
cheatsheet ("Mar'tu's Chalk Notes: Strings").

Spec: design/curriculum.md, "## Unit 9 · Strings", items 7 and 8 ("### Quick Check 8" and "### Cheatsheet: Strings").
The spec files both under u09b; by assignment they live here, after u09a (Lessons 8A and 8B, Quiz 8B) and u09b
(Extra practice 9X, Projects 8P1 and 8P2). This part introduces no concept (concept_map.json plans none after u09a).
It uses u09a's planned tokens only: `.upper()` / `.title()` (cheatsheet), `.split()` / `.join()`, `.strip()`,
`.replace()`, `.find()` (Q5 and the cheatsheet), escapes (Q4 and the cheatsheet) and f-strings (C3 CP2, Q2 and the
cheatsheet), and from
earlier units `.lower()` (u02a), `.capitalize()` (u03a), `def` / `return` (Unit 3), `str()` / `int()` and `*` stamps
(Unit 1), `len()`, indexes and slices of text and of a list (Unit 4), `in` (u04b, cheatsheet extra) and `for` (u06a,
cheatsheet extra). The unit is independent of the Readiness Check (Unit 10 needs no Strings token).

Who this is for: the class already played campaign Modules 1 and 2 and struggled. They have SEEN
`option_1.lower().capitalize()` (program-dialogue-options) and the mana bar's `+ str(...)` return line (mana-bars).
Campaign links are "you've seen this, now you'll get it". The Quick Check is framed as "it only shows Mar'tu where to
start", never as a test of what they should already know. Every student has their own device; a Quick Check is done
alone (no pair talk).

Titles follow the unit's order, as Units 4 and 6 did: the forms are "Quick Check 9 · Form A / B", and the ids keep the
curriculum's names, qc8-a and qc8-b. The cheatsheet id is "chalk-notes", as in every unit.

The Quick Check is an honest test-out (the teacher's ruling on the four reps' review): no task can be passed by
pasting a lesson's solution with one word changed, writing an f-string is evidenced, and 4 of the 5 questions are
needed.

What the forms hold (the spec table, in order: C1, C2, C3 in each testout form; Q1, Q2 in its question form):
  C1  a tidy function, chained (chain-methods, string-methods). Form A `hush_line(raw)` (the spec's `tidy_line`,
      renamed so it no longer shares 8B-02's name) on Lucky's shouted note
      `"  WHAT'S IN IT FOR ME?  "`, form B `calm_line(raw)` on Mar'tu's line `"  IT IS NOT A COMPASS.  "`: hand back
      `raw` with no spaces on its ends, in small letters, with a capital first letter. The lesson's 8B-02 line
      (`raw.lower().capitalize()`) alone leaves the spaces, so `.strip()` (8B-05, 8B-08) is part of the chain and the
      order matters (capitalize before strip loses the capital). PAR / RET on three fresh lines (spaces on both ends,
      at the end only, at the start only), never the task's own (lint b). Fails on (spec): `.lower` with no `()`
      (PAR: the method itself handed back; in the middle of the chain it is the AttributeError row).
  C2  split, then join (split-join), two checkpoints. Bomb Shell's clipped log: `words` is `said` cut into words,
      then `clipped` is the first three words glued back with spaces (form A "Ore low today so I rest", form B
      "Door shut now and we wait"). A slice of the list between the split and the join, so `.replace()` can't stand
      in for `.join()`. CMB: another line, and a two-word line (a slice never runs past the end; three reads by place
      stop Python with an IndexError). CP1 takes every word, or only the first three (a later `words = words[:3]`,
      or `said.split()[:3]` at once: still `said` cut into words). CP2 must glue with `.join()` (the item is the
      split-join evidence, so a `+` loop that strips its last space is told so) and says "no period this time"
      (8B-08's `clip()` adds one). Fails on (spec): `words[:3].join(" ")` -> AttributeError (crash).
  C3  a bar for any values, with the brackets and `str()` (repeat-string), then the bar in an f-string
      (fstring-read, written), two checkpoints. A new shape and new names (the teacher's ruling: the old C3,
      `make_bar(current, maximum)` -> `Mana [▓▓▓░░] 3/5`, was 8A-07's solution with one word swapped): the numbers
      first, with ` of `, then the blocks in brackets. Form A `shield_bar(hp, top)` -> `Shield 3 of 5 [▓▓▓░░]`
      (the solution keeps the points lost in a variable), form B `ore_gauge(left, week)` -> `Ore 3 of 7 [▮▮▮▯▯▯▯]`
      (the solution writes `rest = empty * (week - left)`): both ways are proven by the harness, and an f-string
      bar and a one-line `return` pass too (verified while authoring). CP1 PAR / RET on four fresh pairs, an
      empty bar and a full one among them; 8A-07's program pasted with its label swapped fails (no `shield_bar`),
      and its body in the task's function fails on the lesson's shape ("The numbers came after the blocks").
      Fails on (spec): no brackets -> `empty * top - hp` stops the student's own Run (TypeError, the explainer's
      row). CP2 [ND]: below the prints, print `Pell: ` and `shield_bar(1, 4)` (form B `Moss: ` and
      `ore_gauge(2, 6)`) in one f-string: a `print` of a JoinedStr that holds a call to the function (straight in
      the brackets, or kept in a variable that is printed), and the printed line is the label plus the bar.
  Q1  an index, a slice and `len()` (predict; off-by-one distractors: counting from 1, a slice that keeps its end,
      `len()` read as the last place). Q2 reading an f-string AND its `+ str()` twin (predict; objective 6: read both,
      the campaign uses the second).
Added beyond the spec's table (say so to the teacher): the question forms carry three more questions, so the form
needs 4 of the 5 (questions_to_pass=4, QC2's shape with one more question) and every objective has evidence: Q3
"letters can't change" (objective 2, mc: `word[0] = "G"` is the TypeError row, `.replace()` not kept, a slice one
off), Q4 "escape marks" (objective 3, mc: which line prints a quote mark and a new line; the distractors are the
class's slips, inner quotes with no backslash, `/n`, and a comma for a new line) and Q5 "find-not-found" (objective
4, predict: `.find()` hands back -1, and `sign[-1]` is the last letter, so Python prints it and never complains; the
distractors are capitals ignored, -1 read as "nothing there", and -1 read as the last place's number). C3's
f-string checkpoint is added too (objective 6's "write"). Objective 5's `int()` is Unit 1's (call:int),
revisited in 8B-03 CP3 and 8P1 task 3; the Quick Check does not test it again (the cheatsheet has it, and its error).

Help ladder (FORMAT.md, the Unit 2 walkthrough conventions): hints[0] Where to look, the middle hints teach with other
names (`cry`, `herbs`, `bits`, `#`, `lamp`, `Oil`, listed in foreign_names), the last hint holds the step's start in
backticks, and
that start is always in the solution (no "Start like this" first hint). Quick Check exercises are support="none" (the
hints are written because the schema needs them) and explainer="lean" (teacher ruling: every QC exercise from Unit 2
on). Every exercise also has 3 or 4 another_way angles and assemble lines (a complete program that passes every
checkpoint). No predict on a code task (Quick Checks hide it) and no trace task, so no paste_stop guard is needed and
no Assemble rung holds a predicted value.

Check builders (u09a's guarded helpers, copied: each part file is plain data; every helper name starts with `_` and
builtins come from `_B`, so a student's `len = 3` can't break a check):
  _call(f, *args)  PAR / RET: a student function on fresh values, prints kept private; (printed lines, value, error).
  _rerun(values)   CMB: the program again in a fresh namespace with the FIRST top-level `said = <literal>` swapped.
                   Prints go to a capped private buffer, and a line budget stops a loop that never ends.
  _first_lit(name) the starter's own text, read from the code, so a check follows the line as it is written.
  _bare(attr)      a method call alone on a line (`raw.strip()`): the copy is made, then nothing keeps it.
  _need_def(...)   the function exists with its parameters; a near-miss name gets the lessons' sentence.
  _lost(name)      a variable that was never made, or its near miss ("you wrote `word`, the task needs `words`").
  _why(name, err)  the lean form of u09a's `_why` (as Units 3 and 7), on every `_call` error path (C1, C3 CP1): an
                   error inside the student's function during the check's own call. It names the unknown name and
                   the function, never the fix, in the same words as the SOLO's lean `_why` (u09a, the reconcile
                   pass): "Inside `hush_line`, Python stopped: `NameError: ...`. `said` is not a name `hush_line`
                   knows." (`said` from 8B-02's example; a typo like `rwa`; 8A-07's `maximum`), or
                   a name used before the line that makes it. Proven with the calls taken out.
Messages are lean (the Unit 2 ruling, as QC2's `_leaned`): each names the slip and the evidence, "Mar'tu tested
your function with a test call, `hush_line("  THE GLUG IS GONE.  ")`.", but never the fix or the line to type. Each
lean message keeps the words of the lesson message for the same slip (the reconcile pass), less the fix. A
student's own text is never repeated back (2.11): what a function hands back is described (spaces on its ends, all
small letters, 7 full blocks), never shown. Invented Tor values only in check data (Pell, Brakka, Moss, Ivo, Glug,
Rust Ward).

The class's slips for this unit, each proven by a wrong_answers entry (in the task named; the rest are u09a's and
u09b's, and the questions carry the ones a code task can't):
  * a method called and its result not kept: C1 (any string method alone on a line inside the function is named:
    three bare calls then `return raw`; `raw.strip()` alone, then the chain; the strip kept, then the whole chain alone;
    `.capitalize()` alone after the strip, which is not misread as "capitalize before strip"), C2 CP1 (`said.split()`
    alone, then `words = said`); Q3's `.replace` distractor;
  * `lower(line)` as if it were a function: C1 (`lower(raw).capitalize()`, `capitalize(lower(strip(raw)))`: NameError),
    C2 (`split(said)`);
  * a method named with no `()`: C1 (`.lower` at the end: the spec's PAR; in the middle: AttributeError; `.strip` with
    no `()`), C2 CP1 (`said.split`);
  * a letter changed in place (`raw[0] = raw[0].upper()` -> TypeError: 'str' object does not support item
    assignment): C1; Q3 (`word[0] = "G"`);
  * an index off by one, or a slice that misses its end: C1 (`raw[2:]` drops a letter), C2 CP2 (`[:2]`, `[:4]`,
    `[1:4]`, letters `said[:3]`, a slice counted for this line), C2's two-word rerun (three reads by place: IndexError);
    Q1 (each distractor), Q3 (`word[2:]`, `rune[:2]`);
  * quotes inside quotes without an escape (SyntaxError) and `\\n` vs a typed new line: Q4 (`"Lucky: "Mine.""`, `/n`,
    a comma for the new line); the code tasks have no text with quotes in it;
  * `.split()` hands back a LIST, then it is treated as text: C2 CP1 (`words.lower()`: AttributeError; `list(said)`,
    letters for words), C2 CP2 (`clipped = words[:3]`, `str(words[:3])`, `" ".join(said[:3])` joining letters);
  * join the wrong way round: C2 CP2 (`words[:3].join(" ")`, the spec's crash; `words.join(" ")`), empty glue, a
    comma for the glue, no `.join()` at all (a `+` loop, stripped);
  * `int("7 ")` / `int("seven")`: not in this Quick Check (see above). NOTE: `int("7 ")` is not an error in Python 3
    (int() ignores spaces at the ends, verified in 3.13); the cheatsheet says so and shows `int("twelve")`;
  * an f-string without the `f` (prints `{bar}` as it is) or with a brace missing (SyntaxError: f-string: expecting
    '}'): C3 CP1 (in the bar) and CP2 (braces in plain quotes; a brace missing in Pell's line); Q2's distractor
    reads the braces as they are; CP2 also names a `+` line ("This line glues with `+`; this step is the f-string"),
    a comma, the call missing (the name with no `(...)`, the call typed with no braces, a variable in the braces);
  * `+` between text and a number without `str()` (TypeError: can only concatenate str (not "int") to str, or
    unsupported operand type(s) for +: 'int' and 'str' when the number comes first): C3, and `str()` round the
    whole sum (TypeError: unsupported operand type(s) for +: 'int' and 'str');
  * `.find()` giving -1 read as the last place: Q5 (capitals count too: no small-w `ward` in `"Ash Ward"`, so -1,
    and `sign[-1]` prints `d`); case-sensitive `in`: not in this Quick Check (8A-04 proves it); the cheatsheet has
    both as rows ("No error, wrong answer: -1 read as a place");
  * typing the finished text by hand instead of building it from the values: C1 (the tidy line typed; the outer
    `heard` read instead of `raw`; `"raw"` in quotes), C2 (a typed list, `said` typed again, a typed `clipped`), C3 (a
    typed bar, a typed count of blocks; CP2 the bar typed in the quotes; C2 CP1 a split typed over by three typed
    words); and a lesson's solution pasted: C3 (8A-07's program with its label swapped, and its body in the task's
    function).
  Also: print for return (C1, C3), the starter's `pass` (C1, C3), `.title()` and `.upper()` for `.capitalize()`,
  `.replace(" ", "")` for `.strip()`, `.capitalize()` then `.lower()` (C1), every word / two / four / the last three
  words, a period or a space left on the end (C2), the wrong blocks, the blocks in the wrong order, the numbers
  swapped, a `/` or `of` with no spaces for ` of `, the label or a space missing, no brackets round the blocks, the
  sign the wrong way round, all empty, all full (C3).

Phone width: starters, question code, question choices, fenced pictures and cheatsheet code keep to 36 characters a
line (checked by script), with one exception: Q5's dictated error choice is Python's own last line, `ERROR:
IndexError: string index out of range` (44; a choice button wraps). Solutions and assemble lines keep to 36 as well,
so C3's numbers take two lines (`nums = str(hp) + " of "`, then `nums = nums + str(top)`) and C1's chain two steps
(`raw = raw.strip()`, then `return raw.lower().capitalize()`). The one-line chain (43 characters, so in no
assemble block), `raw.strip().capitalize()` and a capital built by hand (`raw[0].upper() + raw[1:].lower()` after a
strip) pass too: verified while authoring, with the harness's own runner.

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u09c
"""

import re

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
def _parsed():
    return _ast.parse(_source)
def _q(_v):
    if _tn(_v) == 'str':
        return '"' + _v + '"'
    return _B.str(_v)
def _tried(_vals):
    return (" Mar'tu tested your code with a test line, " + ' and '.join(['`' + _k + ' = ' + _q(_v) + '`' for _k, _v in _vals.items()])
            + '.')
def _called(_name, _args):
    return " Mar'tu tested your function with a test call, `" + _name + '(' + ', '.join([_q(_a) for _a in _args]) + ")`."
def _kind(_v):
    _k = _tn(_v)
    return {'int': 'a number', 'float': 'a number', 'list': 'a list', 'bool': 'True or False', 'tuple': 'a tuple',
            'dict': 'a dictionary', 'NoneType': '`None`'}.get(_k, 'a ' + _k)
def _lit(_v, _at):
    return _ast.copy_location(_ast.parse(_B.repr(_v), mode='eval').body, _at)
def _rerun(_values):
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
    _out, _buf, _err = _sys.stdout, _Cap(), ''
    _sys.stdout = _buf
    try:
        _code = _B.compile(_t, 'main.py', 'exec')
        _guarded(lambda: _B.exec(_code, _ns))
    except _Runaway:
        _err = 'it ran too long'
    except Exception as _e:
        _err = _tn(_e) + ': ' + _B.str(_e)
    finally:
        _sys.stdout = _out
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
def _is_method(_v):
    return _tn(_v) in ('builtin_function_or_method', 'method', 'method-wrapper')
def _bare(_attr):
    # A method call standing alone on a line: `raw.strip()` makes a copy, then nothing keeps it.
    return [_n for _n in _ast.walk(_parsed()) if _tn(_n) == 'Expr' and _tn(_n.value) == 'Call'
            and _tn(_n.value.func) == 'Attribute' and _n.value.func.attr == _attr]
def _fdef(_name):
    _f = [_n for _n in _parsed().body if _tn(_n) == 'FunctionDef' and _n.name == _name]
    return _f[-1] if _f else None
def _attrs_in(_node):
    return [_n.attr for _n in _ast.walk(_node) if _tn(_n) == 'Attribute'] if _node is not None else []
def _edits(_a, _b):
    _row = _B.list(_B.range(_B.len(_b) + 1))
    for _i, _ca in _B.enumerate(_a, 1):
        _new = [_i]
        for _j, _cb in _B.enumerate(_b, 1):
            _new.append(_B.min(_row[_j] + 1, _new[_j - 1] + 1, _row[_j - 1] + (_ca != _cb)))
        _row = _new
    return _row[-1]
def _close(_m, _w):
    _a, _b = _m.lower(), _w.lower()
    return (_a.rstrip('s') == _b.rstrip('s') or _a.replace('_', '') == _b.replace('_', '')
            or (_a[:1] == _b[:1] and _edits(_a, _b) <= 2))
def _made_names():
    _out = []
    for _n in _ast.walk(_parsed()):
        _k = _tn(_n)
        _ts = _n.targets if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'For') else [])
        for _x in _ts:
            if _tn(_x) == 'Name' and _x.id not in _out:
                _out.append(_x.id)
    return _out
def _lost(_w, _skip=()):
    # _skip: the task's other names, never offered as the near miss
    _n = [_m for _m in _made_names() if _m != _w and _m not in _skip and _close(_m, _w)]
    if _n:
        return 'You made `' + _n[0] + '`, but this step needs `' + _w + '`. Python matches names letter for letter.'
    return 'No variable named `' + _w + '` was made.'
def _need_def(_name, _nparams, _sig):
    # Lean: what is missing, never the line to type.
    _fd = _fdef(_name)
    if _fd is None:
        _near = [_n.name for _n in _parsed().body if _tn(_n) == 'FunctionDef' and _close(_n.name, _name)]
        assert not _near, ('Your function is named `' + _near[0] + '`, but this step needs `'
                           + _name + '`. Python matches names letter for letter.')
        assert False, 'There is no function named `' + _name + '`. The line `' + _sig + '` is missing or changed.'
    assert _B.callable(globals().get(_name)), (
        'A later line put a value in `' + _name + '` with `=`, so it is not a function now.')
    _n = _len(_fd.args.args)
    assert _n == _nparams, ('`' + _name + '` has ' + _str(_n) + (' parameter' if _n == 1 else ' parameters')
                            + ", but the `def` line it started with, `" + _sig + '`, has ' + _str(_nparams) + '.')
    return globals()[_name]
def _why(_name, _err):
    # The lean form of u09a's _why (as Units 3 and 7): an error inside a student function while Mar'tu's check
    # called it. Where, and what Python met, never the fix. _err is _call's 'Kind: text'.
    _k, _s = _err.split(': ', 1) if ': ' in _err else (_err, '')
    _m = _re.search(r"'(\w+)'", _s)
    _x = _m.group(1) if _m else ''
    _say = ''
    if _k == 'UnboundLocalError' and _x:
        _say = ' `' + _x + '` is used before the line that makes it.'
    elif _k == 'NameError' and _x in ('lower', 'upper', 'title', 'capitalize', 'strip', 'split', 'join', 'replace',
                                      'find'):
        _say = ' `' + _x + '` is a method, used here like a function.'
    elif _k == 'NameError' and _x:
        _say = ' `' + _x + '` is not a name `' + _name + '` knows.'
    elif 'builtin_function_or_method' in _s:
        _say = ' A method is used with no `()`.'
    elif "'list' object has no attribute 'join'" in _s:
        _say = ' `.join` is asked of a list.'
    return 'Inside `' + _name + '`, Python stopped: `' + _err + '`.' + _say
'''


def chk(label, body, **subs):
    """A check: the shared _PRE, then `body` with each __NAME__ replaced by repr(value)."""
    for key, value in subs.items():
        body = body.replace(f"__{key}__", repr(value))
    left = re.findall(r"__[A-Z][A-Z0-9_]*__", body)
    assert not left, f"unfilled placeholder {left} in {label!r}"
    return (label, _PRE + body)


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

# No new terms: u09a defines this unit's (method, immutable, escape mark, .upper(), .title(), chain, .split(),
# .join(), .strip(), .replace(), .find(), f-string), u09b defines cipher, and Units 1-7 define theirs (string, slice,
# index, len(), list, str(), int(), return, TypeError, AttributeError, ...).
GLOSSARY = []


# =============================================================================================
# Quick Check 8 (test-out), forms A and B: three code tasks each, plus four questions each.
# =============================================================================================

LESSON_8A = "Strings Are Rows of Letters"
LESSON_8B = "Words That Change Shape"


def _stuck(lesson, *exercises):
    """Per skill, never "a whole lesson": the exercises that teach this task, then the lesson they sit in."""
    named = " and ".join(f"*{title}*" for title in exercises)
    return f"Stuck? Skip this task, or go back to {named} in the lesson {lesson}. Tasks you pass here stay ✓ done."


def _qc_meta(skills, form, foreign="", level="S2", dictates=""):
    return meta(starter_level=level, path="QC8", form=form, skills=skills, solo="true", dictates=dictates,
                foreign_names=foreign)


# ---- C1: a tidy function, chained (chain-methods, string-methods) ------------------------------------------------

TIDY_FORMS = {
    "A": dict(
        fn="hush_line", heard="  WHAT'S IN IT FOR ME?  ", tidy="What's in it for me?",
        cases=["  THE GLUG IS GONE.  ", "mOSS IS AT THE DOOR   ", "   pell found the latch"],
        lead=(
            "Lucky shouts his notes, with extra spaces on both ends. Finish `hush_line(raw)` so it hands back `raw` "
            "tidy: no spaces on its ends, small letters, and a capital first letter. "
        ),
        pass_line="`hush_line` tidies any line. Lucky: What's in it for me? Much nicer when it's quiet.",
    ),
    "B": dict(
        fn="calm_line", heard="  IT IS NOT A COMPASS.  ", tidy="It is not a compass.",
        cases=["  BRAKKA SAW THE RED CLOCK.  ", "rUST wARD IS READY   ", "   ivo lost the map"],
        lead=(
            "My lines came out far too loud, with extra spaces on both ends. Finish `calm_line(raw)` so it hands "
            "back `raw` tidy: no spaces on its ends, small letters, and a capital first letter. "
        ),
        pass_line="`calm_line` tidies any line. Mar'tu: It is not a compass. Said calmly, yes?",
    ),
}

_TIDY_BODY = r'''
_fn = __FN__
_f = _need_def(_fn, 1, __SIG__)
_res = []
for _a in __CASES__:
    _p, _v, _e = _call(_f, _a)
    _ev = _called(_fn, (_a,))
    assert not _e, _why(_fn, _e) + _ev
    _res.append((_a, _p, _v, _ev))
_qraw = [_n for _n in _ast.walk(_fdef(_fn) or _parsed()) if _tn(_n) == 'Constant' and _n.value == 'raw']
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2] and _qraw), (
    '`"raw"` is in quotes, so `' + _fn + '` works on the letters r, a, w, not the line it is handed.'
    " Mar'tu tested your function with two test lines: both handed back `" + _str(_res[0][2]) + '`.')
assert not (_tn(_res[0][2]) == 'str' and _res[0][2] == _res[1][2]), (
    '`' + _fn + '` hands back the same text for any line, so what it hands back does not come from `raw`.'
    " Mar'tu tested your function with two test lines: both handed back the same text.")
_fd = _fdef(_fn)
_used = _attrs_in(_fd)
_meths = ('strip', 'lstrip', 'rstrip', 'lower', 'upper', 'capitalize', 'title', 'replace', 'casefold', 'swapcase')
# A method call standing alone on a line inside the function (`raw.lower()`, or a whole chain): its copy is lost.
_lone = [_n.value.func.attr for _n in _ast.walk(_fd) if _tn(_n) == 'Expr' and _tn(_n.value) == 'Call'
         and _tn(_n.value.func) == 'Attribute' and _n.value.func.attr in _meths]
# The methods in the order they run: left to right along a chain, top to bottom down the lines.
_order = [_n.attr for _n in _B.sorted([_n for _n in _ast.walk(_fd) if _tn(_n) == 'Attribute'],
                                      key=lambda _n: (_n.end_lineno, _n.end_col_offset))]
_cap_early = 'capitalize' in _order and _any(
    _x in _order[_order.index('capitalize') + 1:] for _x in ('strip', 'lstrip', 'split', 'replace'))
for _a, _p, _v, _ev in _res:
    _core = _a.strip()
    _want = _core.lower().capitalize()
    if _v == _want:
        continue
    assert not (_v is None and _p), '`' + _fn + '` printed a line, then handed back `None`, Python\'s word for nothing.' + _ev
    assert _v is not None, '`' + _fn + '` handed back `None`, Python\'s word for nothing: no line in it hands anything back.' + _ev
    assert not _is_method(_v), '`' + _fn + '` hands back the method itself, not text: a method with no `()`.' + _ev
    assert _tn(_v) == 'str', '`' + _fn + '` handed back ' + _kind(_v) + ', not text.' + _ev
    assert not _lone, ('`.' + _lone[0] + '()` is on a line of its own: it makes a copy, then nothing keeps it.' + _ev)
    assert _v != _a, ('`' + _fn + '` handed back the line exactly as it came in'
                      + (', not a copy a method made.' if _any(_m in _used for _m in _meths) else '.') + _ev)
    if _v != _v.strip():
        assert False, 'The line came back with spaces still on its ends.' + _ev
    if _v.lower() != _want.lower():
        assert not (_v.lower().replace(' ', '') == _want.lower().replace(' ', '')
                    and _v.count(' ') < _want.count(' ')), (
            'The spaces between the words came out too. Only the spaces on the ends should go.' + _ev)
        assert _len(_v) != _len(_want) - 1, 'The line came back one letter short.' + _ev
        assert False, 'The line came back with different letters from the line handed in.' + _ev
    assert not (_v == _core.lower() and _cap_early), (
        'The line came back all in small letters: with the spaces still on, `.capitalize()` met a space, and '
        'nothing got a capital.' + _ev)
    assert _v != _core.lower(), 'The line came back all in small letters.' + _ev
    assert _v != _core.upper(), 'The line came back all in capitals.' + _ev
    assert _v != _core.title(), 'Every word came back with a capital, not only the first word.' + _ev
    assert _v != _core, 'The line came back with its capitals the same as before.' + _ev
    assert False, 'The line came back with capitals in the wrong places.' + _ev
'''

TIDY_COMMENT = (
    "    # Hand back raw with no spaces\n"
    "    # on its ends, small letters,\n"
    "    # and a capital first letter.\n"
)
TIDY_STEPS = "    raw = raw.strip()\n    return raw.lower().capitalize()\n"


def _qc_tidy(form):
    f = TIDY_FORMS[form]
    fn, heard = f["fn"], f["heard"]
    sig = f"def {fn}(raw):"

    def program(body="    pass\n", tail=f'heard = "{heard}"\nprint({fn}(heard))\n'):
        return sig + "\n" + TIDY_COMMENT + body + "\n\n" + tail

    starter = program()
    solution = program(TIDY_STEPS)
    return dict(
        id="tidy-the-line",
        title="Tidy the line",
        martu=(
            f["lead"] + "A method hands back a new copy. A [[chain]] runs methods left to right, like two function "
            "machines in a row in math class: `cry.strip().upper()` cuts the spaces, then makes capitals. Or take a "
            "few steps, and keep each copy with `=`. I also test your function with other lines I make up.\n"
            + _stuck(LESSON_8B, "Chain two methods", "Clean-up tools")
        ),
        names=[fn, "raw"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="tidy-raw",
                text=f"Replace `pass` on line 5 so `{fn}(raw)` hands back `raw` with no spaces on its ends, in small "
                     f"letters, with a capital first letter. You should see `{f['tidy']}` in the Console.",
                dictated=False,
                hints=[
                    "Look at `pass` on line 5, inside the function. There the line is called `raw`. Which three jobs "
                    "does the note above `pass` ask for, and in what order?",
                    "A chain with other names:\n```python\ncry = cry.strip().upper()\n```\nEach method works on the "
                    "copy the one before it handed back. Keep the last copy with `=`, or hand it back with `return`.",
                    "Cut the spaces first. On text that starts with a space, `.capitalize()` finds a space, not a "
                    "letter, so nothing gets a capital.",
                    "Write `raw = raw.strip()` in place of `pass`. Under it, hand back `raw` with `.lower()` and "
                    "`.capitalize()` chained on.",
                ],
                checks=[chk(f"{fn} hands back the tidy line, for fresh lines", _TIDY_BODY, FN=fn, SIG=sig,
                            CASES=f["cases"])],
                pass_line=f["pass_line"],
            ),
        ],
        solution=solution,
        assemble=dict(
            lines=[sig, "    raw = raw.strip()", "    return raw.lower().capitalize()", f'heard = "{heard}"',
                   f"print({fn}(heard))"],
            distractors=["    raw.strip()", "    return raw.title()", "    return raw.lower.capitalize()"],
        ),
        another_way=[
            dict(angle="picture", label="One copy at a time", text=(
                "```text\n\"  SHIELD UP.  \"\n   .strip()\n\"SHIELD UP.\"\n   .lower()\n\"shield up.\"\n"
                "   .capitalize()\n\"Shield up.\"\n```\nEach step down is a new copy. `return` hands back the last one.")),
            dict(angle="everyday", text=(
                "A method hands you a new copy, and the text in `raw` stays as it was. Keep each copy with `=`, or "
                "put the next method right onto it. It's like asking Gearshift for a copy of a map: if you don't take "
                "the copy, it falls on the floor.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "In the campaign, the dialogue options used `option_1.lower().capitalize()`: two methods in a chain, "
                "left to right. This line needs one more method at the front of the chain.")),
        ],
        campaign_link=dict(
            module=MODULE_1,
            part="program-dialogue-options",
            snippet="option_1.lower().capitalize()",
            why="You've seen this chain in the campaign's dialogue options: `.lower()` first, then `.capitalize()` "
                "on the copy it handed back.",
        ),
        takeaway="Methods hand back new copies, so chain them in order: `.strip()`, then `.lower()`, then "
                 "`.capitalize()`.",
        wrong_answers=[
            dict(why="the starter: pass", code=starter, fails_at=1, message_contains="handed back `None`"),
            dict(why="print for return", code=program("    print(raw.strip().lower().capitalize())\n"), fails_at=1,
                 message_contains="printed a line, then handed back `None`"),
            dict(why="the tidy line typed by hand", code=program(f'    return "{f["tidy"]}"\n'), fails_at=1,
                 message_contains="same text for any line"),
            dict(why="the outer variable read, not the parameter (typed test value)",
                 code=program("    return heard.strip().lower().capitalize()\n"), fails_at=1,
                 message_contains="does not come from `raw`"),
            dict(why="the parameter in quotes", code=program('    return "raw".strip().lower().capitalize()\n'),
                 fails_at=1, message_contains='`"raw"` is in quotes'),
            dict(why="three bare calls, nothing kept, then return raw (methods hand back NEW strings)",
                 code=program("    raw.strip()\n    raw.lower()\n    raw.capitalize()\n    return raw\n"), fails_at=1,
                 message_contains="`.strip()` is on a line of its own"),
            dict(why="the strip kept, then the chain alone on a line (its copy lost), then return raw",
                 code=program("    raw = raw.strip()\n    raw.lower().capitalize()\n    return raw\n"), fails_at=1,
                 message_contains="`.capitalize()` is on a line of its own"),
            dict(why="strip and lower kept, .capitalize() alone on a line (not misread as capitalize-before-strip)",
                 code=program("    raw = raw.strip().lower()\n    raw.capitalize()\n    return raw\n"), fails_at=1,
                 message_contains="`.capitalize()` is on a line of its own"),
            dict(why="no method at all: return raw", code=program("    return raw\n"), fails_at=1,
                 message_contains="exactly as it came in."),
            dict(why="raw.strip() alone on a line, then the chain", code=program(
                "    raw.strip()\n    return raw.lower().capitalize()\n"), fails_at=1, message_contains="on a line of its own"),
            dict(why=".lower with no () handed back (spec: PAR)", code=program("    raw = raw.strip()\n    return raw.lower\n"),
                 fails_at=1, message_contains="with no `()`"),
            dict(why=".capitalize with no () at the end of the chain",
                 code=program("    raw = raw.strip()\n    return raw.lower().capitalize\n"), fails_at=1,
                 message_contains="with no `()`"),
            dict(why=".lower with no () in the middle of the chain (AttributeError on the student's own Run)",
                 code=program("    raw = raw.strip()\n    return raw.lower.capitalize()\n"), fails_at=0,
                 message_contains="has no attribute 'capitalize'"),
            dict(why=".strip with no () (AttributeError on the student's own Run)",
                 code=program("    raw = raw.strip\n    return raw.lower().capitalize()\n"), fails_at=0,
                 message_contains="has no attribute 'lower'"),
            dict(why="lower(raw) as if it were a function (NameError)",
                 code=program("    raw = raw.strip()\n    return lower(raw).capitalize()\n"), fails_at=0,
                 message_contains="'lower' is not defined"),
            dict(why="8B-02's example name, said, for raw (NameError on the student's own Run)",
                 code=program("    return said.strip().lower().capitalize()\n"), fails_at=0,
                 message_contains="name 'said' is not defined"),
            dict(why="the hint's cry copied, the calls kept: used before it is made (UnboundLocalError on the student's "
                     "own Run)",
                 code=program("    cry = cry.strip()\n    return cry.lower().capitalize()\n"), fails_at=0,
                 message_contains="cannot access local variable 'cry'"),
            dict(why="said for raw, the bottom lines taken out: the check's own call meets it (the lean _why)",
                 code=program("    return said.strip().lower().capitalize()\n", ""), fails_at=1,
                 message_contains=f"`said` is not a name `{fn}` knows."),
            dict(why="a typo in the parameter, rwa, the bottom lines taken out (the lean _why names it)",
                 code=program("    raw = rwa.strip()\n    return raw.lower().capitalize()\n", ""), fails_at=1,
                 message_contains="`rwa` is not a name"),
            dict(why="every method as a function (NameError)", code=program("    return capitalize(lower(strip(raw)))\n"),
                 fails_at=0, message_contains="is not defined"),
            dict(why="a letter changed in place (TypeError)",
                 code=program("    raw = raw.strip().lower()\n    raw[0] = raw[0].upper()\n    return raw\n"),
                 fails_at=0, message_contains="does not support item assignment"),
            dict(why=".replace(\" \", \"\") for .strip(): every space goes, the ones between words too",
                 code=program('    raw = raw.replace(" ", "")\n    return raw.lower().capitalize()\n'), fails_at=1,
                 message_contains="spaces between the words came out too"),
            dict(why="capitalize, then lower: the capital made, then lost (not the spaces' fault)",
                 code=program("    raw = raw.strip()\n    return raw.capitalize().lower()\n"), fails_at=1,
                 message_contains="all in small letters."),
            dict(why="capitalize before strip (the capital meets a space)",
                 code=program("    raw = raw.lower().capitalize()\n    return raw.strip()\n"), fails_at=1,
                 message_contains="with the spaces still on, `.capitalize()` met a space"),
            dict(why="no strip: the lesson's 8B-02 line alone", code=program("    return raw.lower().capitalize()\n"),
                 fails_at=1, message_contains="spaces still on its ends"),
            dict(why="no capital: only strip and lower", code=program("    raw = raw.strip()\n    return raw.lower()\n"),
                 fails_at=1, message_contains="all in small letters."),
            dict(why=".title() for .capitalize()", code=program("    raw = raw.strip()\n    return raw.title()\n"),
                 fails_at=1, message_contains="Every word came back with a capital"),
            dict(why=".upper() for .capitalize()", code=program("    raw = raw.strip()\n    return raw.upper()\n"),
                 fails_at=1, message_contains="all in capitals"),
            dict(why="a slice one off: raw[2:] drops a letter",
                 code=program("    raw = raw.strip().lower()\n    return raw[0].upper() + raw[2:]\n"), fails_at=1,
                 message_contains="one letter short"),
        ],
        notes=_qc_meta("chain-methods,string-methods", form, "cry") + "\n"
        f"QC8 C1, form {form}: `{fn}(raw)` on `\"{heard}\"`, which should come back `{f['tidy']}`. One checkpoint [ND], "
        f"PAR / RET on three fresh lines ({', '.join(repr(c) for c in f['cases'])}: spaces on both ends, at the end "
        "only, at the start only), never the task's own line (lint b). The spec's `tidy_line` chained (form A's is "
        "named `hush_line`, so it no longer shares 8B-02's `tidy_line`; form B's stays `calm_line`), with `.strip()` "
        "in front, so the 8B-02 line alone (`raw.lower().capitalize()`) fails on the spaces, and the order matters "
        "(capitalize before strip loses the capital: named from the AST). `raw.strip().capitalize()` passes "
        "(`.capitalize()` lowers the rest), and so do the one-line chain and a capital built by hand (verified while "
        "authoring; the one-line chain is 43 characters, so the solution and the assemble lines take two steps). "
        "Fails on (spec): `.lower` with no `()` -> PAR (the method itself handed back); "
        "in the middle of the chain it is the AttributeError row. Also: the copy not kept (three bare calls, a bare "
        "strip, the whole chain alone, `.capitalize()` alone after the strip: any string method alone on a line in "
        "the function is named), `lower(raw)` and every method written as a function (NameError), `raw[0] = ...` "
        "(TypeError), `.replace(\" \", \"\")` for `.strip()`, `.capitalize()` then `.lower()`, `.title()`, `.upper()`, a "
        "slice one off, `return raw` with no method, the tidy line typed, the outer `heard` read, `\"raw\"` in quotes, "
        "print for return, the starter's `pass`. An error inside the function during the check's own call gets the "
        "lean `_why` (the unknown name and the function, never the fix): `said` from 8B-02's example, or a typo "
        f"like `rwa`, with the bottom lines taken out: '`said` is not a name `{fn}` knows.' "
        "With the bottom lines in, the same slips stop the student's own Run (NameError). Lean messages; "
        "support='none', explainer='lean'."
    )


# ---- C2: split, then join (split-join) ----------------------------------------------------------------------------

CLIP_FORMS = {
    "A": dict(
        said="Ore low today so I rest",
        other="Moss saw a red clock by the river", short="Hold fast",
        lead=(
            "Bomb Shell keeps his log short: the first three words of every line, and no more. Cut `said` into a "
            "list of words, then glue the first three back into one line. "
        ),
        pass_words="`words` holds a list of words. Bomb Shell: Cut. Good. Next, three of them.",
        pass_clip="`clipped` holds three words, glued with spaces. Bomb Shell: Ore low today.",
    ),
    "B": dict(
        said="Door shut now and we wait",
        other="Pell found the map in the rain", short="Optic dim",
        lead=(
            "Bomb Shell writes the night watch log, and he never uses more than three words a line. Cut `said` into "
            "a list of words, then glue the first three back into one line. "
        ),
        pass_words="`words` holds a list of words. Bomb Shell: Cut. Good. Next, three of them.",
        pass_clip="`clipped` holds three words, glued with spaces. Bomb Shell: Door shut now.",
    ),
}

_WORDS_BODY = r'''
_s0 = _first_lit('said')
assert _tn(_s0) == 'str', 'The line `said = "..."`, there at the start, is gone, so there is no line to cut.'
assert 'words' in globals(), _lost('words', ('said', 'clipped'))
_w = globals()['words']
# Every word, or (a later line kept only those, or the split was sliced at once) the first three: both are `said`
# cut into words, and the first three are what step 2 needs.
_three = _w == _s0.split()[:3] and _w != _s0.split()
if _w != _s0.split() and not _three:
    assert not _is_method(_w), '`words` holds the method itself, not a list: `.split` with no `()` after it.'
    if _tn(_w) == 'str':
        assert not _bare('split'), (
            '`words` holds text, not a list. `.split()` is on a line of its own: it makes a list, then nothing keeps it.')
        assert _w != _s0, '`words` holds the same text as `said`, not a list.'
        assert False, '`words` holds text, not a list.'
    assert _tn(_w) == 'list', '`words` holds ' + _kind(_w) + ', not a list.'
    assert _w != [], '`words` is an empty list.'
    assert _w != [_s0], '`words` holds a list with the whole line as one piece.'
    assert _w != _list(_s0), '`words` holds every letter of `said` as its own item, not its words.'
    assert False, '`words` holds a list, but not the words of `said`.'
_o = __OTHER__
_ns, _rows, _err, _miss = _rerun({'said': _o})
_ev = _tried({'said': _o})
assert not _miss, "The `said = \"...\"` line no longer holds plain text in quotes, so Mar'tu can't test your code with another line."
assert not _err, "With another line in `said`, your code stopped. Python's last line: `" + _err + '`.' + _ev
_got = _ns.get('words')
if _got != (_o.split()[:3] if _three else _o.split()):
    assert _got != _w, 'With another line in `said`, `words` did not change to match, so the list is typed in.' + _ev
    assert False, 'With another line in `said`, `words` did not hold that line\'s words.' + _ev
'''

_CLIP_BODY = r'''
_s0 = _first_lit('said')
assert _tn(_s0) == 'str', 'The line `said = "..."`, there at the start, is gone, so there is no line to cut.'
assert 'clipped' in globals(), _lost('clipped', ('said', 'words'))
_c = globals()['clipped']
_wd = _s0.split()
if _c != ' '.join(_wd[:3]):
    assert not _is_method(_c), '`clipped` holds a method, not text: a method name with no `()` after it.'
    assert _tn(_c) != 'list', '`clipped` holds a list, not text.'
    assert _tn(_c) == 'str', '`clipped` holds ' + _kind(_c) + ', not text.'
    assert not _c.startswith('['), '`clipped` holds a list written out as text, with its square brackets.'
    assert _c != '', '`clipped` is empty text.'
    assert _c != ' '.join(_wd), '`clipped` holds every word of the line, not the first three.'
    assert _c != ' '.join(_wd[:2]), '`clipped` holds the first two words, not three.'
    assert _c != ' '.join(_wd[:4]), '`clipped` holds the first four words, not three.'
    assert _c != ' '.join(_wd[1:4]), '`clipped` starts at the second word, so the first word is missing.'
    assert _c != ''.join(_wd[:3]), 'The three words in `clipped` touch: nothing goes between them.'
    _first3 = ' '.join(_wd[:3])
    assert not (_c.strip() == _first3), (
        '`clipped` holds the three words, plus a space ' + ('on its end.' if _c.endswith(' ') else 'at its start.'))
    assert not (_c.rstrip('.!') == _first3), (
        '`clipped` ends with a `' + _c[-1] + '`, but this step asks for only the three words and the spaces between them.')
    assert _c != ' '.join(_wd[-3:]), '`clipped` holds the last three words, not the first three.'
    _rest, _inorder = _c, True
    for _x in _wd[:3]:
        _at = _rest.find(_x)
        _inorder = _inorder and _at >= 0
        _rest = _rest[_at + _len(_x):] if _at >= 0 else _rest
    assert not (_inorder and _c.startswith(_wd[0]) and _c.endswith(_wd[2])), (
        'The first three words are in `clipped`, but not with one space between each two.')
    assert _c != _s0[:3], '`clipped` holds the first three letters of the line, not three words.'
    assert _c != ' '.join(_s0[:3]), (
        '`clipped` holds three letters with spaces between them: `.join` was handed text, not the list of words.')
    assert False, '`clipped` does not hold the first three words, glued with spaces.'
for _o in __OTHERS__:
    _ns, _rows, _err, _miss = _rerun({'said': _o})
    _ev = _tried({'said': _o})
    _n = _len(_o.split())
    assert not ('IndexError' in _err and _n < 3), (
        'With a line of only ' + _str(_n) + " words, Python stopped at a position past the end of the list. Python's "
        'last line: `' + _err + '`.' + _ev)
    assert not _err, "With another line in `said`, your code stopped. Python's last line: `" + _err + '`.' + _ev
    _got = _ns.get('clipped')
    if _got != ' '.join(_o.split()[:3]):
        assert _got != _c, 'With another line in `said`, `clipped` did not change to match, so it is typed in.' + _ev
        assert False, 'With another line in `said`, `clipped` did not hold its first three words.' + _ev
# The right words every time, but this task is the split-join check: the glue has to be `.join()`.
assert 'join' in _attrs_in(_parsed()), (
    '`clipped` holds the right words, but they were glued without `.join()`, and this step checks `.join()`.')
'''

CLIP_STEP1 = "# 1. Make words: said, cut into a\n#    list of words.\n"
CLIP_STEP2 = (
    "# 2. Make clipped: the first three\n"
    "#    words glued back together, a\n"
    "#    space between them. Print it.\n"
)
WORDS_LINE = "words = said.split()\nprint(words)\n"
CLIP_LINE = 'clipped = " ".join(words[:3])\nprint(clipped)\n'


def _qc_clip(form):
    f = CLIP_FORMS[form]
    said = f["said"]
    head = f'said = "{said}"\n'

    def program(words="", clip=""):
        return head + CLIP_STEP1 + words + CLIP_STEP2 + clip

    starter = program()
    solution = program(WORDS_LINE, CLIP_LINE)
    first3 = " ".join(said.split()[:3])
    typed_list = "[" + ", ".join(f'"{w}"' for w in said.split()) + "]"
    return dict(
        id="clip-the-log",
        title="Clip the log",
        martu=(
            f["lead"] + "[[.split()]] cuts text into a list, like cutting a sentence strip into word cards in "
            "English class. A slice keeps the first few cards. Then ask the glue to join them: "
            "`\"-\".join([\"moss\", \"fern\"])` gives `moss-fern`. A line with only two words keeps both. I also "
            "test your code with other lines I make up, a short one too.\n"
            + _stuck(LESSON_8B, "Split and join", "Two functions of your own")
        ),
        names=["said", "words", "clipped"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="cut-into-words",
                text="Under `# 1.`, make `words` hold `said` cut into a list of words.",
                dictated=False,
                hints=[
                    "Look under `# 1.`. `said` holds the line, on line 1. Which method cuts text into a list of "
                    "words?",
                    "With other names: `\"moss fern\".split()` hands back `['moss', 'fern']`, a list. Empty "
                    "parentheses cut at every space. Keep the list with `=`.",
                    "`.split()` makes a new list and leaves `said` as it was, so the list needs a variable of its "
                    "own.",
                    "Start with `words =` under `# 1.`. Then write `said`, a dot, and the method that cuts at spaces.",
                ],
                checks=[chk("words holds the words of said, for another line too", _WORDS_BODY, OTHER=f["other"])],
                pass_line=f["pass_words"],
            ),
            dict(
                id="glue-three-back",
                text="Under `# 2.`, make `clipped` hold the first three words of `words`, glued with `.join()` "
                     "and one space between each two. Add no period, and when a line has only two words, keep both.",
                dictated=False,
                hints=[
                    "Look under `# 2.`. `words` is a list now. Which slice keeps its first three items, and what "
                    "glues a list back into one text?",
                    "With other names:\n```python\nbits = [\"a\", \"b\", \"c\", \"d\"]\nprint(\"-\".join(bits[:2]))\n```"
                    "\nThis prints `a-b`. The glue comes first, then `.join`, then the list in parentheses.",
                    "A slice never goes past the end: `[:3]` of a two-word list gives both words. One position, like "
                    "`words[2]`, would stop Python.",
                    "Start with `clipped = \" \".join(` under `# 2.`. Then write a slice of `words` that keeps three, "
                    "and a `)`.",
                ],
                checks=[chk("clipped holds the first three words, for other lines too, short ones too", _CLIP_BODY,
                            OTHERS=[f["other"], f["short"]])],
                pass_line=f["pass_clip"],
            ),
        ],
        solution=solution,
        partials=[program(WORDS_LINE)],
        assemble=dict(
            lines=[head.strip(), "words = said.split()", "print(words)", 'clipped = " ".join(words[:3])',
                   "print(clipped)"],
            distractors=['clipped = words[:3].join(" ")', 'clipped = " ".join(words[:2])', "words = said"],
        ),
        another_way=[
            dict(angle="picture", label="Cut, keep three, glue", text=(
                "```text\n\"Pell ran home fast\"\n   .split()\n['Pell', 'ran', 'home', 'fast']\n   [:3]\n"
                "['Pell', 'ran', 'home']\n   \" \".join(...)\n\"Pell ran home\"\n```")),
            dict(angle="everyday", text=(
                "`.split` is scissors: it cuts the line into word cards. A slice keeps the first few cards. `.join` "
                "is glue: you hold up the glue, a space, and it sticks the cards back into one line.")),
            dict(angle="step-by-step", text=(
                "1. `.split()` on `said` hands back a list of words.\n2. A slice, `[:3]`, keeps positions 0, 1 and "
                "2.\n3. The glue, `\" \"`, goes in front of `.join(...)`, and the list goes in its parentheses.")),
        ],
        takeaway="`.split()` hands back a list, a slice keeps the first few items, and `\" \".join(...)` glues "
                 "them back into one text.",
        wrong_answers=[
            dict(why="the starter (comments only)", code=starter, fails_at=1, message_contains="No variable named `words`"),
            dict(why="a near-miss name: word for words", code=program("word = said.split()\n"), fails_at=1,
                 message_contains="You made `word`"),
            dict(why="no split: the text itself", code=program("words = said\n"), fails_at=1,
                 message_contains="same text as `said`"),
            dict(why="said.split() alone on a line, then words = said (the copy not kept)",
                 code=program("said.split()\nwords = said\n"), fails_at=1, message_contains="on a line of its own"),
            dict(why="no (): the method itself", code=program("words = said.split\n"), fails_at=1,
                 message_contains="with no `()`"),
            dict(why="split(said) as if it were a function (NameError)", code=program("words = split(said)\n"),
                 fails_at=0, message_contains="'split' is not defined"),
            dict(why="split at a comma: one piece", code=program('words = said.split(",")\n'), fails_at=1,
                 message_contains="the whole line as one piece"),
            dict(why="a typed list", code=program(f"words = {typed_list}\n"), fails_at=1,
                 message_contains="typed in"),
            dict(why="the line typed again and split, not said", code=program(f'words = "{said}".split()\n'),
                 fails_at=1, message_contains="typed in"),
            dict(why="letters, not words: list(said)", code=program("words = list(said)\n"), fails_at=1,
                 message_contains="every letter of `said`"),
            dict(why="split, then the first three typed over it (typed by hand)",
                 code=program('words = said.split()\nwords = ' + typed_list.split(", ")[0] + ", "
                              + ", ".join(typed_list.split(", ")[1:3]) + ']\n'), fails_at=1,
                 message_contains="the list is typed in"),
            dict(why="the list treated as text: .lower() on a list (AttributeError)",
                 code=program("words = said.split()\nwords = words.lower()\n"), fails_at=0,
                 message_contains="'list' object has no attribute 'lower'"),
            dict(why="step 2 not done (the partial)", code=program(WORDS_LINE), fails_at=2,
                 message_contains="No variable named `clipped`"),
            dict(why="join called the wrong way round, on the slice (spec: crash)",
                 code=program(WORDS_LINE, 'clipped = words[:3].join(" ")\n'), fails_at=0,
                 message_contains="'list' object has no attribute 'join'"),
            dict(why="join called the wrong way round, on the list", code=program(WORDS_LINE, 'clipped = words.join(" ")\n'),
                 fails_at=0, message_contains="'list' object has no attribute 'join'"),
            dict(why="the slice kept as a list", code=program(WORDS_LINE, "clipped = words[:3]\n"), fails_at=2,
                 message_contains="holds a list, not text"),
            dict(why="the list written out with str()", code=program(WORDS_LINE, "clipped = str(words[:3])\n"),
                 fails_at=2, message_contains="with its square brackets"),
            dict(why="every word glued back", code=program(WORDS_LINE, 'clipped = " ".join(words)\n'), fails_at=2,
                 message_contains="every word"),
            dict(why="a slice one short: [:2]", code=program(WORDS_LINE, 'clipped = " ".join(words[:2])\n'), fails_at=2,
                 message_contains="first two words"),
            dict(why="a slice one long: [:4]", code=program(WORDS_LINE, 'clipped = " ".join(words[:4])\n'), fails_at=2,
                 message_contains="first four words"),
            dict(why="counting from 1: [1:4]", code=program(WORDS_LINE, 'clipped = " ".join(words[1:4])\n'), fails_at=2,
                 message_contains="starts at the second word"),
            dict(why="empty glue: the words touch", code=program(WORDS_LINE, 'clipped = "".join(words[:3])\n'),
                 fails_at=2, message_contains="touch"),
            dict(why="three letters, not three words", code=program(WORDS_LINE, "clipped = said[:3]\n"), fails_at=2,
                 message_contains="first three letters"),
            dict(why="the text joined, not the list: letters with spaces",
                 code=program(WORDS_LINE, 'clipped = " ".join(said[:3])\n'), fails_at=2,
                 message_contains="handed text, not the list"),
            dict(why="three reads by place: an index past the end of a short split (IndexError on the rerun)",
                 code=program(WORDS_LINE, 'clipped = words[0] + " " + words[1] + " " + words[2]\n'), fails_at=2,
                 message_contains="only 2 words, Python stopped at a position past the end"),
            dict(why="the lesson's clip(): a period on the end", code=program(WORDS_LINE,
                 'clipped = " ".join(words[:3]) + "."\n'), fails_at=2, message_contains="ends with a `.`"),
            dict(why="built in a loop: a space left on the end", code=program(WORDS_LINE,
                 'clipped = ""\nfor word in words[:3]:\n    clipped = clipped + word + " "\n'), fails_at=2,
                 message_contains="a space on its end"),
            dict(why="the last three words: a slice from the end", code=program(WORDS_LINE,
                 'clipped = " ".join(words[-3:])\n'), fails_at=2, message_contains="last three words"),
            dict(why="built in a loop with +, then stripped: the right words, but no .join()",
                 code=program(WORDS_LINE, 'clipped = ""\nfor word in words[:3]:\n    clipped = clipped + word + " "\n'
                              'clipped = clipped.strip()\n'), fails_at=2, message_contains="this step checks `.join()`"),
            dict(why="a comma for the glue", code=program(WORDS_LINE, 'clipped = ", ".join(words[:3])\n'), fails_at=2,
                 message_contains="not with one space"),
            dict(why="the clipped line typed by hand", code=program(WORDS_LINE, f'clipped = "{first3}"\n'), fails_at=2,
                 message_contains="did not change to match, so it is typed in"),
            dict(why="a slice of letters counted for this line", code=program(WORDS_LINE, f"clipped = said[:{len(first3)}]\n"),
                 fails_at=2, message_contains="did not hold its first three words"),
        ],
        notes=_qc_meta("split-join", form, "herbs,bits") + "\n"
        f"QC8 C2, form {form}: Bomb Shell's clipped log, `said = \"{said}\"` -> `{first3}`. Two checkpoints [ND]. CP1 "
        "`words` is `said` cut into words (any split that gives the words passes, `.split(\" \")` too; every word, or "
        "only the first three, as a later `words = words[:3]` or `said.split()[:3]` leaves it), CMB with "
        f"`\"{f['other']}\"`. CP2 `clipped` is the first three words glued with spaces (spec 'Split, then join'; a "
        "slice of the list sits between the two, so a `.replace()` can't stand in for the `.join()`), CMB with "
        f"`\"{f['other']}\"` and the two-word `\"{f['short']}\"` (the task says a shorter line keeps all its words: "
        "three reads by place stop Python with an IndexError there, the 'index past the end of a split result' "
        "slip). CP2 also needs `.join()` in the code: a `+` loop that strips its last space makes the right text, but "
        "this item is the split-join evidence. Its text says 'no period this time' (8B-08's `clip()` adds one). "
        "Fails on (spec): `words.join(\" \")` -> crash (`words[:3].join(\" \")` and `words.join(\" \")`, the "
        "AttributeError row). Also: the copy not kept, `.split` with no `()`, `split(said)`, the list treated as "
        "text, a typed list, the line typed again, a list kept or written out, every word, `[:2]`, `[:4]`, `[1:4]`, "
        "empty glue, a comma for the glue, a period or a space left on the end, the last three words, no `.join()`, "
        "letters for words (in CP1 and CP2), a typed `clipped`, three words typed over the split, a slice of letters "
        "counted for this line, a near-miss name. One partial (after CP1). Lean messages; support='none', explainer='lean'."
    )


# ---- C3: a bar for any values, then the bar in an f-string (repeat-string, fstring-read) ------------------------

# Lesson 8A-07's solution, copied as it is from u09a's BAR_SOLUTION. With its label swapped it is the paste this task
# must fail: the old C3 (`make_bar(current, maximum)` -> `Mana [▓▓▓░░] 3/5`) passed it with one word changed.
LESSON_BAR = (
    "def make_bar(current, maximum):\n"
    '    full = "▓"\n'
    '    empty = "░"\n'
    "    used = maximum - current\n"
    "    bar = full * current\n"
    "    bar = bar + empty * used\n"
    '    bar = "Glug [" + bar + "] "\n'
    '    bar = bar + str(current) + "/"\n'
    "    bar = bar + str(maximum)\n"
    "    return bar\n"
    "\n\n"
    "print(make_bar(2, 3))\n"
    "print(make_bar(1, 4))\n"
    "print(make_bar(0, 3))\n"
    "print(make_bar(3, 3))\n"
)
# Its body alone (the lines under the two block lines, down to `return bar`).
LESSON_BAR_BODY = LESSON_BAR.split('    empty = "░"\n', 1)[1].split("\n\n\n", 1)[0] + "\n"

BAR_FORMS = {
    "A": dict(
        fn="shield_bar", cur="hp", top="top", label="Shield", full="▓", empty="░",
        calls=[(3, 5), (6, 8)], cases=[(4, 7), (0, 6), (5, 5), (2, 9)], who="Pell", say=(1, 4),
        left_word="`hp`", lost_word="lost", lost_msg="points were lost",
        stamp="    bar = bar + empty * gone\n", no_brackets="    bar = bar + empty * top - hp\n",
        all_empty="    bar = bar + empty * top\n", sign=("top - hp\n", "hp - top\n"),
        order=("    bar = full * hp\n    bar = bar + empty * gone\n",
               "    bar = empty * gone\n    bar = bar + full * hp\n"),
        wrap='    bar = " [" + bar + "]"\n', unwrapped='    bar = " " + bar\n', tight='    bar = "[" + bar + "]"\n',
        distractors=["    gone = hp - top", '    nums = hp + " of "', '    print("Shield " + nums + bar)',
                     'print("Pell: {shield_bar(1, 4)}")'],
        # the points lost kept in a variable of their own
        body=(
            "    gone = top - hp\n"
            "    bar = full * hp\n"
            "    bar = bar + empty * gone\n"
            '    bar = " [" + bar + "]"\n'
            '    nums = str(hp) + " of "\n'
            "    nums = nums + str(top)\n"
            '    return "Shield " + nums + bar\n'
        ),
        lead=(
            "`shield_bar(hp, top)` should hand back a bar like `Shield 3 of 5 [▓▓▓░░]` for any numbers. `hp` is the "
            "points Pell's shield has left, and `top` is the most it holds. The bar has one `▓` for each point left "
            "and one `░` for each point lost. "
        ),
        pass_bar="Your bar works for any numbers. Mar'tu: Even an empty shield, yes? Next: Pell's line, in an f-string.",
        beats=(
            "Your f-string fills in the bar from `shield_bar`. Mar'tu's notes: the Greenroom sign, where you four "
            "arrived in Tor. Lucky's canteen says Glug now. The gaps on the chalk wall still shrink, 48 down to 37. "
            "And it is not a compass. "
        ),
    ),
    "B": dict(
        fn="ore_gauge", cur="left", top="week", label="Ore", full="▮", empty="▯",
        calls=[(3, 7), (5, 6)], cases=[(2, 5), (0, 4), (6, 6), (1, 8)], who="Moss", say=(2, 6),
        left_word="`left`", lost_word="gone", lost_msg="days were gone",
        stamp="    rest = empty * (week - left)\n", no_brackets="    rest = empty * week - left\n",
        all_empty="    rest = empty * week\n", sign=("(week - left)", "(left - week)"),
        order=('" [" + bar + rest + "]"', '" [" + rest + bar + "]"'),
        wrap='    bar = " [" + bar + rest + "]"\n', unwrapped='    bar = " " + bar + rest\n',
        tight='    bar = "[" + bar + rest + "]"\n',
        distractors=["    rest = empty * week - left", '    nums = left + " of "', '    print("Ore " + nums + bar)',
                     'print("Moss: " + ore_gauge(2, 6))'],
        # the brackets right in the stamp
        body=(
            "    bar = full * left\n"
            "    rest = empty * (week - left)\n"
            '    bar = " [" + bar + rest + "]"\n'
            '    nums = str(left) + " of "\n'
            "    nums = nums + str(week)\n"
            '    return "Ore " + nums + bar\n'
        ),
        lead=(
            "`ore_gauge(left, week)` should hand back a gauge like `Ore 3 of 7 [▮▮▮▯▯▯▯]` for any numbers. `left` is "
            "the days of ore left, and `week` is the days in the week. The gauge has one `▮` for "
            "each day left and one `▯` for each day gone. "
        ),
        pass_bar="Your gauge works for any numbers. Bomb Shell: Gauge works. Any week. Next: Moss's line, in an f-string.",
        beats=(
            "Your f-string fills in the gauge from `ore_gauge`. Mar'tu's notes: the Greenroom sign, where you four "
            "arrived in Tor. Lucky's canteen says Glug now, and Bomb Shell's gauge counts the ore. The gaps on the "
            "chalk wall still shrink, 48 down to 37. And it is not a compass. "
        ),
    ),
}

_BAR_FN = r'''
_fn, _full, _empty, _label = __FN__, __FULL__, __EMPTY__, __LABEL__
def _want_bar(_c, _m):
    return _label + ' ' + _str(_c) + ' of ' + _str(_m) + ' [' + _full * _c + _empty * (_m - _c) + ']'
'''

_BAR_BODY = _BAR_FN + r'''
_f = _need_def(_fn, 2, __SIG__)
_res = []
for _c, _m in __CASES__:
    _p, _v, _e = _call(_f, _c, _m)
    _ev = _called(_fn, (_c, _m))
    assert not _e, _why(_fn, _e) + _ev
    _res.append((_c, _m, _p, _v, _ev))
assert not (_tn(_res[0][3]) == 'str' and _res[0][3] == _res[1][3]), (
    '`' + _fn + '` hands back the same bar for any numbers, so the bar does not come from the numbers handed in.'
    " Mar'tu tested your function with two test calls, `" + _fn + '(' + _str(_res[0][0]) + ', ' + _str(_res[0][1])
    + ')` and `' + _fn + '(' + _str(_res[1][0]) + ', ' + _str(_res[1][1]) + ')`: both handed back the same text.')
for _c, _m, _p, _v, _ev in _res:
    if _v == _want_bar(_c, _m):
        continue
    assert not (_v is None and _p), '`' + _fn + '` printed the bar, then handed back `None`, Python\'s word for nothing.' + _ev
    assert _v is not None, '`' + _fn + '` handed back `None`, Python\'s word for nothing: no line in it hands anything back.' + _ev
    assert _tn(_v) == 'str', '`' + _fn + '` handed back ' + _kind(_v) + ', not text.' + _ev
    assert not ('{' in _v or '}' in _v), (
        'The bar came back with the curly braces `{` and `}` in it: an f-string with no `f` in front.' + _ev)
    _odd = [_b for _b in '█▓░▮▯' if _b in _v and _b not in (_full, _empty)]
    assert not _odd, "The bar used `" + _odd[0] + "`, not the blocks in `full` and `empty`." + _ev
    _nf, _ne = _v.count(_full), _v.count(_empty)
    _with = " With a test call, `" + _fn + '(' + _str(_c) + ', ' + _str(_m) + ')`, the bar had '
    _blocks = lambda _n, _w: _str(_n) + ' ' + _w + (' block' if _n == 1 else ' blocks')  # noqa: E731
    assert _nf == _c, ('The full blocks do not come from ' + __LEFT__ + '.' + _with + _blocks(_nf, 'full') + ', but '
                       + __LEFT__ + ' was ' + _str(_c) + '.')
    assert _ne == _m - _c, ('The empty blocks do not come from the ' + __LOST__.split(' ')[0] + ' '
                            + __LOST__.split(' ', 2)[2] + '.' + _with + _blocks(_ne, 'empty') + ', but only '
                            + _str(_m - _c) + ' ' + __LOST__ + '.')
    _bl = _full * _c + _empty * (_m - _c)
    assert _bl in _v, 'The bar has the right blocks in the wrong order: the empty blocks came first.' + _ev
    _at = _v.find(_bl)
    # 8A-07's shape, `Glug [▓▓░] 2/3`: the numbers after the blocks (the labels hold no digits).
    assert not (_str(_m) in _v[_at + _len(_bl):] and _str(_m) not in _v[:_at]), (
        'The numbers came after the blocks, at the end of the bar.' + _ev)
    _nums = _str(_c) + ' of ' + _str(_m)
    assert _nums in _v, 'The numbers in the bar do not read `' + _nums + '`.' + _ev
    assert _v.startswith(_label + ' '), 'The bar does not start with the word `' + _label + '` and a space.' + _ev
    assert _v.endswith('[' + _bl + ']'), 'The bar does not end with its blocks inside square brackets, `[` and `]`.' + _ev
    assert False, ('The square brackets or the spaces in the bar are not right: it came back as `' + _v + '`.'
                   + _ev[:-1] + ': it should hand back `' + _want_bar(_c, _m) + '`.')
'''

# Checkpoint 2: one print of an f-string that holds a call to the function (straight in `print(...)`, or kept in a
# variable that is printed), and the line it prints is the label and the bar.
_SAY_BODY = _BAR_FN + r'''
_who, _a, _b = __WHO__, __A__, __B__
_want = _who + ': ' + _want_bar(_a, _b)
_t = _parsed()
_kept = {}
for _n in _t.body:
    if _tn(_n) == 'Assign' and _len(_n.targets) == 1 and _tn(_n.targets[0]) == 'Name':
        _kept[_n.targets[0].id] = _n.value
def _what(_p):
    # what a one-value print shows: the value itself, or the line that made the variable it names
    _x = _p.args[0]
    return _kept.get(_x.id, _x) if _tn(_x) == 'Name' else _x
def _calls_fn(_node, _args=None):
    return _any(_tn(_x) == 'Call' and _tn(_x.func) == 'Name' and _x.func.id == _fn
                and (_args is None or [_tn(_y) == 'Constant' and _y.value for _y in _x.args] == _list(_args))
                for _x in _ast.walk(_node))
def _says_who(_node):
    return _any(_tn(_x) == 'Constant' and _tn(_x.value) == 'str' and _who in _x.value for _x in _ast.walk(_node))
_prints = [_n for _n in _ast.walk(_t) if _tn(_n) == 'Call' and _tn(_n.func) == 'Name' and _n.func.id == 'print'
           and _n.args]
_fs = [_p for _p in _prints if _len(_p.args) == 1 and _tn(_what(_p)) == 'JoinedStr' and _calls_fn(_what(_p))]
if _fs:
    assert _want in _lines(), (
        'Your f-string line does not show `' + _who + ': ` and then the bar from `' + _fn + '(' + _str(_a) + ', '
        + _str(_b) + ')`.')
else:
    _mine = [_p for _p in _prints if _any(_says_who(_x) or _calls_fn(_x, (_a, _b)) for _x in _p.args)
             or (_len(_p.args) == 1 and _says_who(_what(_p)))]
    assert _mine, 'There is no line that prints `' + _who + ': ` and the bar.'
    _p = _mine[-1]
    assert _len(_p.args) == 1, 'Your new `print` line uses a comma, but this step checks an f-string.'
    _x = _what(_p)
    assert _tn(_x) != 'BinOp', 'Your new `print` line glues with `+`, but this step checks an f-string.'
    _txt = ''.join([_y.value for _y in _ast.walk(_x) if _tn(_y) == 'Constant' and _tn(_y.value) == 'str'])
    assert not (_tn(_x) == 'Constant' and '{' in _txt), (
        'The curly braces are in plain quotes, with no `f` in front, so they print as they are.')
    assert not (_full in _txt or _empty in _txt), (
        'The bar is typed inside the quotes, so it does not come from `' + _fn + '`.')
    assert _tn(_x) != 'JoinedStr', 'The f-string has no call to `' + _fn + '` inside its curly braces.'
    assert False, 'The line that prints `' + _who + ': ` is not an f-string, and this step checks an f-string.'
'''

_STRETCH = "Want a stretch? Try the projects The Water-Stained Log and The Institute Cipher."


def _qc_bar(form):
    f = BAR_FORMS[form]
    fn, cur, top, label, full, empty = f["fn"], f["cur"], f["top"], f["label"], f["full"], f["empty"]
    who, (sa, sb) = f["who"], f["say"]
    sig = f"def {fn}({cur}, {top}):"
    (c1, m1), (c2, m2) = f["calls"]
    shape = f"{label} {c1} of {m1} [{full * c1}{empty * (m1 - c1)}]"
    said = f"{who}: {label} {sa} of {sb} [{full * sa}{empty * (sb - sa)}]"
    head = sig + "\n" + f'    full = "{full}"\n    empty = "{empty}"\n'
    comment = "    # Hand back a bar like this one,\n    # for any numbers:\n" + f"    # {shape}\n"
    calls = f"print({fn}({c1}, {m1}))\nprint({fn}({c2}, {m2}))\n"
    call = f"{fn}({sa}, {sb})"
    say = f'print(f"{who}: {{{call}}}")\n'
    body, ret, full_line = f["body"], f["body"].splitlines(True)[-1], f"    bar = full * {cur}\n"
    nums = f'    nums = str({cur}) + " of "\n    nums = nums + str({top})\n'
    assert nums in body and ret.startswith("    return ")

    def program(b=body, tail=calls + say):
        return head + comment + b + "\n\n" + tail

    def swap(old, new):
        assert old in body, old
        return program(body.replace(old, new))

    def says(line):
        return program(tail=calls + line + "\n")

    starter = program("    pass\n", calls)
    solution = program()
    pasted = LESSON_BAR_BODY.replace("current", cur).replace("maximum", top).replace("Glug", label)
    check = chk(f"{fn} hands back the bar for fresh numbers, empty and full too", _BAR_BODY, FN=fn, FULL=full,
                EMPTY=empty, LABEL=label, SIG=sig, CASES=f["cases"], LEFT=f["left_word"], LOST=f["lost_msg"],
                SHAPE=shape)
    say_check = chk(f"one f-string prints {who}'s line, with a call to {fn} in its braces", _SAY_BODY, FN=fn,
                    FULL=full, EMPTY=empty, LABEL=label, WHO=who, A=sa, B=sb)
    wrong = [
        dict(why="the starter: pass", code=starter, fails_at=1, message_contains="handed back `None`"),
        dict(why="print for return", code=swap(ret, ret.replace("return ", "print(")[:-1] + ")\n"),
             fails_at=1, message_contains="printed the bar, then handed back `None`"),
        dict(why="the bar typed by hand: the first call's answer", code=program(f'    return "{shape}"\n'), fails_at=1,
             message_contains="same bar for any numbers"),
        dict(why="+ with a number, no str() round the second number (TypeError on the student's own Run)",
             code=swap(f"str({top})", top), fails_at=0, message_contains="can only concatenate str"),
        dict(why="+ with a number, no str() round the first number (TypeError on the student's own Run)",
             code=swap(f"str({cur})", cur), fails_at=0, message_contains="unsupported operand type(s) for +"),
        dict(why="str() round the whole sum (TypeError on the student's own Run)",
             code=swap(nums, f'    nums = str({cur} + " of " + {top})\n'), fails_at=0,
             message_contains="unsupported operand type(s) for +"),
        dict(why="no brackets: empty * top - cur (spec: crash, the TypeError row)",
             code=swap(f["stamp"], f["no_brackets"]), fails_at=0, message_contains="unsupported operand type(s) for -"),
        dict(why="all empty: empty * top", code=swap(f["stamp"], f["all_empty"]), fails_at=1,
             message_contains="empty blocks"),
        dict(why="the sign the wrong way round (no empty blocks)", code=swap(*f["sign"]), fails_at=1,
             message_contains="empty blocks"),
        dict(why="all full: full * top", code=swap(full_line, f"    bar = full * {top}\n"), fails_at=1,
             message_contains="full blocks"),
        dict(why="a count of blocks typed inside the function", code=swap(full_line, "    bar = full * 3\n"),
             fails_at=1, message_contains="full blocks"),
        dict(why="the numbers swapped",
             code=swap(nums, f'    nums = str({top}) + " of "\n    nums = nums + str({cur})\n'),
             fails_at=1, message_contains="do not read"),
        dict(why="a slash for ' of ' (the lesson's 3/5 shape)", code=swap('" of "', '"/"'), fails_at=1,
             message_contains="do not read"),
        dict(why="'of' with no spaces round it", code=swap('" of "', '"of"'), fails_at=1,
             message_contains="do not read"),
        dict(why="the empty blocks first, then the full ones", code=swap(*f["order"]), fails_at=1,
             message_contains="wrong order"),
        dict(why="the campaign's block for full", code=swap(full_line, f'    bar = "█" * {cur}\n'),
             fails_at=1, message_contains="used `█`"),
        dict(why="no label", code=swap(ret, "    return nums + bar\n"), fails_at=1,
             message_contains="does not start with the word"),
        dict(why="the label with no space after it", code=swap(f'"{label} "', f'"{label}"'), fails_at=1,
             message_contains="does not start with the word"),
        dict(why="the lesson's 8A-07 make_bar pasted with the label swapped", code=LESSON_BAR.replace("Glug", label),
             fails_at=1, message_contains=f"There is no function named `{fn}`"),
        dict(why="8A-07's body pasted into the task's function, its names and label swapped: the lesson's shape",
             code=program(pasted), fails_at=1, message_contains="The numbers came after the blocks"),
        dict(why="8A-07's body pasted as it is (NameError on the student's own Run)", code=program(LESSON_BAR_BODY),
             fails_at=0, message_contains="name 'maximum' is not defined"),
        dict(why="8A-07's body pasted as it is, the calls taken out: the check's own call meets it (the lean _why)",
             code=program(LESSON_BAR_BODY, ""), fails_at=1,
             message_contains=f"`maximum` is not a name `{fn}` knows."),
        dict(why="no brackets round the blocks", code=swap(f["wrap"], f["unwrapped"]), fails_at=1,
             message_contains="does not end with its blocks inside"),
        dict(why="no space before [", code=swap(f["wrap"], f["tight"]), fails_at=1,
             message_contains="square brackets or the spaces"),
        dict(why="an f-string with no f (the braces print as they are)",
             code=swap(nums, f'    nums = "{{{cur}}} of {{{top}}}"\n'), fails_at=1, message_contains="`{` and `}`"),
        dict(why="an f-string with a brace missing (SyntaxError)",
             code=swap(nums, f'    nums = f"{{{cur}}} of {{{top}"\n'), fails_at=0, message_contains="expecting '}'"),
        # checkpoint 2: the bar in an f-string
        dict(why="step 2 not done (the partial)", code=program(tail=calls), fails_at=2,
             message_contains=f"There is no line that prints `{who}: `"),
        dict(why="glued with +, not an f-string", code=says(f'print("{who}: " + {call})'), fails_at=2,
             message_contains="glues with `+`, but this step checks an f-string."),
        dict(why="glued with +, the label in a variable", code=says(f'who = "{who}: "\nprint(who + {call})'),
             fails_at=2, message_contains="glues with `+`"),
        dict(why="a + line kept in a variable, then printed",
             code=says(f'line = "{who}: " + {call}\nprint(line)'), fails_at=2,
             message_contains="glues with `+`"),
        dict(why="printed with a comma, not an f-string", code=says(f'print("{who}:", {call})'), fails_at=2,
             message_contains="uses a comma, but this step checks an f-string"),
        dict(why="braces with no f (they print as they are)", code=says(f'print("{who}: {{{call}}}")'), fails_at=2,
             message_contains="with no `f` in front"),
        dict(why="the call missing: the function's name with no (...) in the braces",
             code=says(f'print(f"{who}: {{{fn}}}")'), fails_at=2, message_contains=f"no call to `{fn}`"),
        dict(why="the call missing: typed in the f-string with no braces", code=says(f'print(f"{who}: {call}")'),
             fails_at=2, message_contains=f"no call to `{fn}`"),
        dict(why="the call missing: a variable in the braces, the call on another line",
             code=says(f'got = {call}\nprint(f"{who}: {{got}}")'), fails_at=2, message_contains=f"no call to `{fn}`"),
        dict(why="the bar typed in the f-string's quotes", code=says(f'print(f"{said}")'), fails_at=2,
             message_contains="typed inside the quotes"),
        dict(why="the whole line typed in plain quotes", code=says(f'print("{said}")'), fails_at=2,
             message_contains="typed inside the quotes"),
        dict(why="the numbers swapped in the call", code=says(f'print(f"{who}: {{{fn}({sb}, {sa})}}")'), fails_at=2,
             message_contains="Your f-string line does not show"),
        dict(why="no colon after the name", code=says(f'print(f"{who} {{{call}}}")'), fails_at=2,
             message_contains="Your f-string line does not show"),
        dict(why="a brace missing in the f-string (SyntaxError)", code=says(f'print(f"{who}: {{{call}")'), fails_at=0,
             message_contains="expecting '}'"),
    ]
    lines = (head + body).splitlines() + calls.strip().splitlines() + [say.strip()]
    return dict(
        id="a-bar-for-any-values",
        title="A bar for any values",
        martu=(
            f["lead"] + "Bars like this are tape diagrams, like in math class: the full part plus the empty part make "
            f"the whole. Then print {who}'s line with an f-string, text with blanks like Mad Libs. I test `{fn}` with "
            "other numbers I make up, an empty bar and a full one too.\n"
            + _stuck(LESSON_8A, "Bars one more time")
        ),
        names=[fn, cur, top, "full", "empty"],
        support="none",
        explainer="lean",
        starter=starter,
        checkpoints=[
            dict(
                id="bar-for-any-values",
                text=f"Replace `pass` on line 7 so `{fn}({cur}, {top})` hands back a bar like `{shape}` for any "
                     f"numbers. You should see `{shape}` on the first line in the Console.",
                dictated=False,
                hints=[
                    f"Look at `pass` on line 7, inside `{fn}`. `{cur}` and `{top}` hold the numbers. How many "
                    "`full` blocks does the bar need, and how many `empty` blocks?",
                    "`*` repeats text, like a stamp: `\"#\" * 3` is `###`. For the empty blocks, put "
                    f"`{top} - {cur}` in parentheses, so Python works it out before the `*`, like PEMDAS.",
                    f"Glue the pieces in order with `+`: `\"{label} \"`, the numbers with `\" of \"` between them, "
                    "then the blocks inside `\" [\"` and `\"]\"`. A number needs `str()` before `+` can glue it to "
                    "text.",
                    f"Start with `bar = full * {cur}` in place of `pass`. Then glue on the empty blocks and the "
                    "square brackets, put the numbers in front, and hand back the bar with `return`.",
                ],
                checks=[check],
                pass_line=f["pass_bar"],
            ),
            dict(
                id="bar-in-an-f-string",
                text=f"Under `print({fn}({c2}, {m2}))`, add a line that prints `{who}: ` and then the bar from "
                     f"`{call}`, in one f-string. You should see `{said}`.",
                dictated=False,
                hints=[
                    f"Look under `print({fn}({c2}, {m2}))`, the last line. What goes right before the quotes to "
                    "make an f-string, and what goes inside its curly braces?",
                    "An f-string is text with blanks, like Mad Libs. With other names:\n```python\n"
                    "print(f\"Oil: {lamp(2, 6)}\")\n```\nThe `f` goes right before the quotes. Python calls `lamp` "
                    "and fills the blank with the text it hands back.",
                    "No `+` and no `str()` this time: the f-string fills in the bar for you. Without the `f`, the "
                    "curly braces print as they are.",
                    f"Start with `print(f\"{who}: {{` under `print({fn}({c2}, {m2}))`. Then write the call, then "
                    "`}\")`.",
                ],
                checks=[say_check],
                pass_line=f["beats"] + _STRETCH,
            ),
        ],
        solution=solution,
        partials=[program(tail=calls)],
        assemble=dict(
            lines=lines,
            distractors=f["distractors"],
        ),
        another_way=[
            dict(angle="picture", label="The bar in pieces", text=(
                "```text\nFuel 2 of 5 [##...]\n     |    |  |  |\n     |    |  |  \".\" * (5 - 2)\n"
                "     |    |  \"#\" * 2\n     |    tank\n     left\n```\nEach line under the bar points down to "
                "the code that makes that piece. `left` and `tank` are the two numbers.")),
            dict(angle="step-by-step", text=(
                f"1. Stamp `full` `{cur}` times. Then stamp `empty` `({top} - {cur})` times: the parentheses make "
                f"Python work out the minus first.\n2. Put the blocks inside `\" [\"` and `\"]\"`.\n3. In front go "
                f"`\"{label} \"`, `str({cur})`, `\" of \"` and `str({top})`.\n4. Hand back the whole bar with "
                "`return`.")),
            dict(angle="from the campaign", label="You've seen this", text=(
                "The campaign's mana bar was built the same way: blocks stamped with `*`, glued "
                "with `+`, and each number turned into text with `str()`. Only the order of the pieces is new.")),
            dict(angle="side by side", label="Two ways, one line", text=(
                "```python\nprint(\"Oil: \" + lamp(2, 6))\nprint(f\"Oil: {lamp(2, 6)}\")\n```\nBoth print the same "
                "line. The first glues with `+`. The second puts the call in curly braces, and Python fills it in.")),
        ],
        campaign_link=dict(
            module=MODULE_2,
            part="mana-bars",
            snippet='return "Mana [" + filled + empty + "] " + str(caster["mana"]) + "/" + str(caster["max_mana"])',
            why="You've seen this line in the campaign's mana bars: blocks stamped with `*`, glued with `+`, and "
                "`str()` for each number. Your bar is built the same way, with its pieces in a new order.",
        ),
        takeaway=f"A bar for any numbers: stamp `full * {cur}` and `empty * ({top} - {cur})`, then glue the "
                 "pieces with `+` and `str()`. An f-string can hold the call in its curly braces.",
        wrong_answers=wrong,
        notes=_qc_meta("repeat-string,fstring-read", form, "#,.,Fuel,left,tank,lamp,Oil") + "\n"
        f"QC8 C3, form {form}: `{fn}({cur}, {top})` -> `{shape}`, with `full = \"{full}\"` and `empty = \"{empty}\"` "
        "pre-typed (the symbol tray has both). A new shape and new names (the teacher's ruling): the numbers first, "
        "with ` of `, then the blocks in brackets, so lesson 8A-07's solution with one word changed no longer "
        "passes (the old C3 was `make_bar(current, maximum)` -> `Mana [▓▓▓░░] 3/5`). Two checkpoints [ND]. CP1, "
        f"PAR / RET on four fresh pairs, {f['cases']} (an empty bar and a full one among them), never the task's "
        f"{f['calls']} or CP2's ({sa}, {sb}) (lint b). Form A's solution keeps the points lost in a variable "
        "(`gone = top - hp`), form B's writes the brackets in the stamp (`rest = empty * (week - left)`): both "
        "pass, and both are the harness's proof. An f-string bar (`return f\"...\"`) and a one-line `return` pass "
        "too (verified while authoring). Fails on (spec): no brackets -> "
        f"`empty * {top} - {cur}` stops the student's own Run (TypeError: unsupported operand type(s) for -: 'str' "
        "and 'int', the explainer's row). Also: `+` with no `str()` (either number) and `str()` round the whole sum "
        "(TypeErrors on the student's own Run), an f-string with no `f` (braces in the bar) or a brace missing "
        "(SyntaxError), a typed bar, a typed count, all empty, all full, the blocks in the wrong order, the sign the "
        "wrong way round, the numbers swapped, a `/` or `of` with no spaces, `█`, the label or a space missing, no "
        "brackets round the blocks, print for return, the starter's `pass`. 8A-07 pasted: the whole program with "
        "its label swapped fails on the missing function; its body in the task's function, names and label "
        "swapped, fails on the lesson's shape ('The numbers came after the blocks'); its body as it is stops the "
        "student's own Run (NameError), and with the calls taken out the lean `_why` names the unknown name: "
        f"'`maximum` is not a name `{fn}` knows.' CP2 [ND] (writing an f-string, "
        f"evidenced): `{say.strip()}`. The check needs a `print` of one f-string (JoinedStr) that holds a call to "
        f"`{fn}` (straight in the brackets, or kept in a variable that is printed: both are an f-string written), "
        f"and the printed line `{said}`. Lean messages: a `+` line ('This line glues with `+`; this step is the "
        "f-string', the label in a variable or the line kept in one too), a comma, braces with no `f`, the call "
        "missing (the name with no `(...)`, the call typed with no braces, a variable in the braces), a bar typed "
        "in the quotes, the wrong numbers or no colon. CP2 hints use `lamp(2, 6)` and `Oil` (the cheatsheet's "
        "lamp), listed in foreign_names. One partial (after CP1). Lean messages; support='none', explainer='lean'."
    )


_QC_SUMMARY = (
    "Optional: three short code tasks, then five questions, with no hints. You don't need to know all of this yet: it "
    "shows Mar'tu where you should start. Pass all three tasks and get 4 of the 5 questions right, and Unit 9 counts "
    "as done. Tasks you pass here stay ✓ done."
)

QC8_A = dict(
    kind="testout",
    id="qc8-a",
    title="Quick Check 9 · Form A",
    optional=True,
    minutes=16,
    summary=_QC_SUMMARY,
    questions_to_pass=4,
    exercises=[
        _qc_tidy("A"),
        _qc_clip("A"),
        _qc_bar("A"),
    ],
    notes=(
        "Quick Check 8, form A (code tasks C1, C2, C3, in the spec's order; the spec's Q1 and Q2 live in "
        "qc8-a-questions, with three added questions). An honest test-out (the teacher's ruling): pass = every code "
        "task plus 4 of the 5 questions (questions_to_pass=4, QC2's shape with one more question); a retake draws "
        "form B. Coverage (lint d): chain-methods, string-methods -> C1 `hush_line` (renamed from the spec's "
        "`tidy_line`, so it no longer shares 8B-02's name; WA `.lower` with no `()` handed back, the spec's PAR; in "
        "the middle of the chain, the AttributeError row; the copy not kept; `lower(raw)`; `.title()`; `.upper()`; "
        "capitalize before strip; no strip; a letter changed in place); split-join -> C2 (WA `words[:3].join(\" \")` "
        "and `words.join(\" \")`, the spec's crash; `said.split()` not kept; `.split` with no `()`; `split(said)`; "
        "the list treated as text; every word, `[:2]`, `[:4]`, `[1:4]`, empty glue, three reads by place on a "
        "two-word line); repeat-string -> C3 CP1 `shield_bar(hp, top)` -> `Shield 3 of 5 [▓▓▓░░]` (a new shape, so "
        "8A-07's solution pasted with its label swapped fails; WA no brackets, the spec's crash; `+` with no "
        "`str()`; an f-string with no `f` or a brace missing; all empty, all full, a typed bar); fstring-read, "
        "written -> C3 CP2 (Pell's line in one f-string that holds the call; a `+` line, a comma, no `f`, the call missing, a "
        "typed bar); string-index-slice -> Q1 (counting from 1, a slice that keeps its end, `len()` read as the "
        "last place), with C1's `raw[2:]` and C2's slices in code; fstring-read -> Q2 (an f-string and its "
        "`+ str()` twin, read side by side: the braces read as they are, the math in the braces not done, a name "
        "read as its letters); string-immutable -> Q3 (objective 2, added) and C1's `raw[0] = ...`; escape-chars "
        "-> Q4 (objective 3, added: inner quotes with no backslash, `/n`, a comma for a new line); string-methods "
        "-> Q5 (added: `.find()` and its -1, the class's 'last letter' slip). Check messages are lean (the Unit 2 "
        "ruling): the slip and the evidence, never the fix; an error inside a function during the check's own call "
        "gets the lean `_why` (the unknown name and the function). Framing (G4 R25): it only shows Mar'tu where to "
        "start; each task's Stuck? line names the exercises that teach that one skill. The last pass line (C3 "
        "CP2, which shows only once C3 is done) keeps to the core lessons' story beats (8A-01's Greenroom sign, "
        "8A-07's Glug canteen, 8A-06's chalk wall, 8B-05's compass) for students who test out, then offers the two "
        "projects as the stretch; it no longer recaps the optional 8P1 or gives away its answer, and it no longer "
        "opens with 'A line tidied, a log clipped' (shown even when C1 or C2 failed). support='none' and "
        "explainer='lean' everywhere: no hints, tracer or compare; glossary and read-aloud stay on. 16 minutes "
        "(the spec's ~10, plus C2's second checkpoint, C3's f-string checkpoint and the three added questions)."
    ),
)

QC8_B = dict(
    kind="testout",
    id="qc8-b",
    title="Quick Check 9 · Form B",
    optional=True,
    minutes=16,
    summary=_QC_SUMMARY,
    questions_to_pass=4,
    exercises=[
        _qc_tidy("B"),
        _qc_clip("B"),
        _qc_bar("B"),
    ],
    notes=(
        "Quick Check 8, form B: `calm_line(raw)` on Mar'tu's `\"  IT IS NOT A COMPASS.  \"` (C1), Bomb Shell's "
        "watch log `\"Door shut now and we wait\"` -> `Door shut now` (C2), Bomb Shell's Velocite gauge "
        "`ore_gauge(left, week)` -> `Ore 3 of 7 [▮▮▮▯▯▯▯]` (C3 CP1, the brackets right in the stamp) and Moss's line "
        "`print(f\"Moss: {ore_gauge(2, 6)}\")` (C3 CP2). The last pass line has form A's core beats, with Bomb "
        "Shell's gauge swapped in beside the canteen. Same coverage, rules and minutes as form A (16). Questions live "
        "in qc8-b-questions; questions_to_pass=4 (4 of the 5)."
    ),
)


# Lean, proved (as Unit 2's _leaned asserts its rewrites and Units 4-6's _lean_guard their forms): no check names the
# fix. The strings unit adds its own verbs (Strip, Split, Join, Slice, Return, Chain) to the words a fix opens with.
_FIX_WORDS = {"Put", "Make", "Add", "Use", "Copy", "Read", "Store", "Take", "Print", "Change", "Replace", "Spend",
              "Fill", "Check", "Write", "Ask", "Indent", "Give", "Build", "Warn", "Swap", "Compare", "Set", "Spell",
              "Move", "Delete", "Remove", "Type", "Try", "Mend", "Fix", "Keep", "Count", "Hand", "Loop", "Walk",
              "Call", "Start", "Stop", "Break", "Glue", "Unindent", "Strip", "Split", "Join", "Slice", "Return",
              "Chain", "Cut", "Wrap"}


def _lean_guard(form):
    """Quick Check messages are lean (Unit 2 ruling): the slip and the evidence, never the fix. Proved at import, two
    ways, as u05c and u06c do. (1) No check of a form's tasks holds a line of Mar'tu's version that the starter does
    not show, or that line's working part (the chain, the split, the join, the stamp, the f-string); a bare name
    (`clipped`, printed) is the task's own name, not a fix. (2) No text in a check opens a sentence with a fix
    ("Strip the spaces ...", "Glue the words ..."): every text that opens a sentence is the slip or the evidence."""
    import ast as _ast_guard
    squash = lambda text: "".join(text.split())  # noqa: E731
    for ex in form["exercises"]:
        shown = {squash(line) for line in ex["starter"].split("\n")}
        pieces = set()
        for line in ex["solution"].split("\n"):
            code = squash(line.split("  #")[0])
            if not code or code.startswith("#") or code in shown:
                continue
            pieces.add(code)
            right = code.split("=", 1)[1] if "=" in code and "==" not in code else code
            for head in ("print(", "return", "if", "for"):
                if right.startswith(head):
                    right = right[len(head):].rstrip(":)")
            if right.strip("[]0123456789,-+") and len(right) >= 6 and not right.isidentifier():
                pieces.add(right)
        for cp in ex["checkpoints"]:
            for name, check_code in cp["checks"]:
                for node in _ast_guard.walk(_ast_guard.parse(check_code)):
                    if isinstance(node, _ast_guard.Constant) and isinstance(node.value, str):
                        # Text a student reads (it has `code` marks or ends a sentence) never shows a line of the fix.
                        shown_text = "`" in node.value or node.value.rstrip().endswith(".")
                        named = [piece for piece in pieces if shown_text and len(piece) >= 6 and piece in squash(node.value)]
                        assert not named, f"{form['id']}/{ex['id']}: the check {name!r} shows the fix {named[0]!r}"
                        words = node.value.strip().split(" ")
                        first = words[0] if len(words) > 1 else ""
                        assert first not in _FIX_WORDS, (f"{form['id']}/{ex['id']}: the check {name!r} opens a message "
                                                         f"with the fix: {node.value[:60]!r}")
    return form


_lean_guard(QC8_A)
_lean_guard(QC8_B)


# =============================================================================================
# Quick Check 8 · question forms (scored with their form: 4 of the 5 right, questions_to_pass=4)
# =============================================================================================

def _qc_questions(form, index_slice, fstring, cant_change, escapes, not_found):
    """index_slice / fstring / not_found = (code, answer, choices, explain, notes); cant_change / escapes = (q, code,
    choices, answer, why_wrong, explain, notes)."""
    def predict(qid, parts):
        code, answer, choices, explain, notes = parts
        return dict(type="predict", id=qid, q="What will this print?", code=code, answer=answer, choices=choices,
                    explain=explain, notes=notes)

    def mc(qid, parts):
        q, code, choices, answer, why_wrong, explain, notes = parts
        out = dict(type="mc", id=qid, q=q, choices=choices, answer=answer, why_wrong=why_wrong, explain=explain,
                   notes=notes)
        if code:
            out["code"] = code
        return out

    return dict(
        kind="quiz",
        id=f"qc8-{form.lower()}-questions",
        title=f"Quick Check 9 · Form {form} questions",
        optional=True,
        minutes=5,
        summary="Five questions that go with Quick Check 9. To pass the Quick Check, get 4 of the 5 right.",
        questions=[
            predict("index-and-slice", index_slice),
            predict("read-an-f-string", fstring),
            mc("letters-cant-change", cant_change),
            mc("escape-marks", escapes),
            predict("find-not-found", not_found),
        ],
        notes=(
            f"Quick Check 8, form {form} questions, scored with qc8-{form.lower()}: every code task plus 4 of the 5 "
            "questions (questions_to_pass=4 on the form: QC2's shape with one more question, so the test-out is "
            "honest). Q1 and Q2 are the spec's; Q3 (objective 2, letters can't change), Q4 (objective 3, escape "
            "marks) and Q5 (objective 4, `.find()` and its -1, the class's 'last letter' slip) are added, so every "
            "objective has evidence. The best score counts, so a retake can lift it. No hints; "
            "read-aloud and glossary stay on. The site shuffles the choices; the right one is also authored in a "
            "different place in each question."
        ),
    )


QC8_A_QUESTIONS = _qc_questions(
    "A",
    (
        'sign = "EXIT"\nprint(sign[1])\nprint(sign[1:3])\nprint(len(sign))\n',
        "X\nXI\n4",
        ["E\nEX\n4", "X\nXIT\n4", "X\nXI\n4", "X\nXI\n3"],
        (
            "Positions start at 0, like a ruler, so `sign[1]` is the second letter, X. A slice stops before its end "
            "number, like the open dot on a number line: `[1:3]` takes positions 1 and 2, `XI`. `len()` counts the "
            "letters: 4."
        ),
        "Q1, string-index-slice (spec: off-by-one). Distractors: counting from 1 (E, EX), a slice that keeps its end "
        "(XIT), `len()` read as the last place (3). The greenroom sign. The right one is authored third.",
    ),
    (
        'hero = "Bomb Shell"\ndays = 7\nprint(f"{hero}: {days - 2} days")\nprint(hero + " has " + str(days))\n',
        "Bomb Shell: 5 days\nBomb Shell has 7",
        [
            "{hero}: {days - 2} days\nBomb Shell has 7",
            "Bomb Shell: 5 days\nBomb Shell has 7",
            "Bomb Shell: 7 - 2 days\nBomb Shell has 7",
            "Bomb Shell: 5 days\nhero has 7",
        ],
        (
            "An f-string is text with blanks, like Mad Libs. Python fills in each `{ }`: `{hero}` is `Bomb Shell`, "
            "and `{days - 2}` works out to 5. The `+` line glues the same kind of text: `hero` has no quotes, so "
            "Python looks inside the variable, the words in quotes show as they are, and `str(days)` is 7."
        ),
        "Q2, fstring-read, plus objective 6's `+ str()` reading (the campaign uses it). Distractors: the braces read "
        "as they are (as if there were no `f`), the math inside the braces not done, a name read as its letters. The "
        "right one is authored second.",
    ),
    (
        "`word` holds `\"Flow\"`. Which line, put in place of `# the line goes here`, makes the code print `Glow`?",
        'word = "Flow"\n# the line goes here\nprint(word)\n',
        ['word[0] = "G"', 'word.replace("F", "G")', 'word = "G" + word[1:]', 'word = "G" + word[2:]'],
        2,
        {
            0: "You can't swap one letter of a string, the way you can't swap one letter on a printed page. Python "
               "stops: *TypeError: 'str' object does not support item assignment*.",
            1: "`.replace()` hands back a new copy, and no `=` keeps it, so `word` still holds `Flow`.",
            3: "`word[2:]` starts at position 2, `ow`, so the `l` is lost: `Gow`.",
        },
        (
            "`word[1:]` is everything from position 1 on: `low`. Glue a `G` in front, and put the new string back "
            "in `word`. You can't change one letter of a string, like a printed page, so you build a new one."
        ),
        "Q3 (added), objective 2, letters can't change. Distractors: the in-place change (the TypeError row), the "
        "`.replace` copy not kept (the class's biggest slip), a slice one off. The right one is authored third.",
    ),
    (
        "Which line shows these two lines in the Console?\n```text\nLucky: \"Mine.\"\nNo.\n```",
        None,
        [
            'print("Lucky: "Mine."\\nNo.")',
            'print("Lucky: \\"Mine.\\"/nNo.")',
            'print("Lucky: \\"Mine.\\"", "No.")',
            'print("Lucky: \\"Mine.\\"\\nNo.")',
        ],
        3,
        {
            0: ("The quote mark before `Mine.` ends the text early, so Python stops with a SyntaxError. Python's last "
                "line guesses you forgot a comma, but that guess is wrong here."),
            1: ("`/n` uses the slash `/`, not the backslash `\\`. So `/n` is two plain marks: it shows as it is, "
                "and everything stays on one line."),
            2: "A comma in `print` shows one space, not a new line: `Lucky: \"Mine.\" No.`, all on one line.",
        },
        (
            "`\\\"` puts a quote mark inside the text, like quotation marks inside a quotation in English class. "
            "`\\n` starts a new line, like pressing Enter. The backslashes never show."
        ),
        "Q4 (added), objective 3, escape-chars. Distractors from the class's slips: quotes inside quotes with no "
        "backslash (SyntaxError), `/n` for `\\n`, a comma for a new line. Verified in 3.13. The right one is "
        "authored last.",
    ),
    (
        'sign = "Ash Ward"\nspot = sign.find("ward")\nprint(spot)\nprint(sign[spot])\n',
        "-1\nd",
        ["-1\nd", "4\nW", "-1\nERROR: IndexError: string index out of range", "7\nd"],
        (
            "`.find()` works like Find (Ctrl+F), and capitals count: `\"Ash Ward\"` has no small-w `ward`. So "
            "`.find()` hands back -1, which means not found. But `sign[-1]` is a real position, the last letter, so "
            "Python shows `d` with no error. That's a quiet bug: check for -1 before you use it."
        ),
        "Q5 (added), objective 4, string-methods: `.find()` and its -1, the class's 'last letter' slip (case counts "
        "too). Distractors: capitals ignored (4, W), -1 read as 'nothing there' (an IndexError), -1 read as the last "
        "place's number (7, d). The quiet bug of the cheatsheet's last row, on new text. The right one is authored "
        "first.",
    ),
)

QC8_B_QUESTIONS = _qc_questions(
    "B",
    (
        'door = "Interior"\nprint(door[2])\nprint(door[2:5])\nprint(len(door))\n',
        "t\nter\n8",
        ["t\nter\n8", "n\nnte\n8", "t\nteri\n8", "t\nter\n7"],
        (
            "Positions start at 0, like a ruler, so `door[2]` is the third letter, t. A slice stops before its end "
            "number, like the open dot on a number line: `[2:5]` takes positions 2, 3 and 4, `ter`. `len()` counts "
            "the letters: 8."
        ),
        "Form B of index-and-slice (the greenroom door, \"Interior\"). Distractors: counting from 1, a slice that "
        "keeps its end, `len()` read as the last place. The right one is authored first.",
    ),
    (
        'name = "Lucky"\nsips = 3\nprint(f"{name} drinks {sips - 1}")\nprint(name + " had " + str(sips))\n',
        "Lucky drinks 2\nLucky had 3",
        [
            "Lucky drinks 3 - 1\nLucky had 3",
            "Lucky drinks 2\nname had 3",
            "{name} drinks {sips - 1}\nLucky had 3",
            "Lucky drinks 2\nLucky had 3",
        ],
        (
            "An f-string is text with blanks, like Mad Libs. Python fills in each `{ }`: `{name}` is `Lucky`, and "
            "`{sips - 1}` works out to 2. The `+` line glues the same kind of text: `name` has no quotes, so Python "
            "looks inside the variable, the words in quotes show as they are, and `str(sips)` is 3."
        ),
        "Form B of read-an-f-string (Lucky's glug). Same distractors. The right one is authored last.",
    ),
    (
        "`rune` holds `\"Glum\"`. Which line, put in place of `# the line goes here`, makes the code print `Glug`?",
        'rune = "Glum"\n# the line goes here\nprint(rune)\n',
        ['rune = rune[:3] + "g"', 'rune[3] = "g"', 'rune = rune[:2] + "g"', 'rune.replace("m", "g")'],
        0,
        {
            1: "You can't swap one letter of a string, the way you can't swap one letter on a printed page. Python "
               "stops: *TypeError: 'str' object does not support item assignment*.",
            2: "`rune[:2]` stops before position 2, so it is only `Gl`: `Glg`.",
            3: "`.replace()` hands back a new copy, and no `=` keeps it, so `rune` still holds `Glum`.",
        },
        (
            "`rune[:3]` is positions 0, 1 and 2: `Glu`. Glue a `g` on the end, and put the new string back in "
            "`rune`. You can't change one letter of a string, like a printed page, so you build a new one."
        ),
        "Form B of letters-cant-change (Lucky's glug, the last letter this time). The right one is authored first.",
    ),
    (
        "Which line shows these two lines in the Console?\n```text\nSign: \"EXIT\"\nBye.\n```",
        None,
        [
            'print("Sign: \\"EXIT\\"", "Bye.")',
            'print("Sign: \\"EXIT\\"\\nBye.")',
            'print("Sign: "EXIT"\\nBye.")',
            'print("Sign: \\"EXIT\\"/nBye.")',
        ],
        1,
        {
            0: "A comma in `print` shows one space, not a new line: `Sign: \"EXIT\" Bye.`, all on one line.",
            2: ("The quote mark before `EXIT` ends the text early, so Python stops with a SyntaxError. Python's last "
                "line guesses you forgot a comma, but that guess is wrong here."),
            3: ("`/n` uses the slash `/`, not the backslash `\\`. So `/n` is two plain marks: it shows as it is, "
                "and everything stays on one line."),
        },
        (
            "`\\\"` puts a quote mark inside the text, like quotation marks inside a quotation in English class. "
            "`\\n` starts a new line, like pressing Enter. The backslashes never show."
        ),
        "Form B of escape-marks (the greenroom sign). The right one is authored second.",
    ),
    (
        'door = "Moon Step"\nspot = door.find("step")\nprint(spot)\nprint(door[spot])\n',
        "-1\np",
        ["5\nS", "-1\nERROR: IndexError: string index out of range", "-1\np", "8\np"],
        (
            "`.find()` works like Find (Ctrl+F), and capitals count: `\"Moon Step\"` has no small-s `step`. So "
            "`.find()` hands back -1, which means not found. But `door[-1]` is a real position, the last letter, so "
            "Python shows `p` with no error. That's a quiet bug: check for -1 before you use it."
        ),
        "Form B of find-not-found (the Moon Step door). The same distractor shapes: capitals ignored (5, S), -1 read "
        "as 'nothing there' (an IndexError), -1 read as the last place's number (8, p). The right one is authored "
        "third.",
    ),
)


# =============================================================================================
# Cheatsheet "Mar'tu's Chalk Notes: Strings"
# =============================================================================================

CHALK_NOTES_9 = dict(
    kind="cheatsheet",
    id="chalk-notes",
    title="Mar'tu's Chalk Notes: Strings",
    summary="Every idea from Unit 9 on one page, with a short example of each. You can print it.",
    entries=[
        dict(concept="One letter: `s[0]` and `s[-1]`. How many: `len(s)`",
             code='rune = "Lantern"\nprint(rune[0])\nprint(rune[-1])\nprint(len(rune))\n',
             output="L\nn\n7",
             note="Positions start at 0, like a ruler. `[-1]` is the last letter. `len()` counts every letter and "
                  "space. (Lesson: Strings Are Rows of Letters)"),
        dict(concept="A slice: `s[2:5]`",
             code='rune = "Lantern"\nprint(rune[2:5])\nprint(rune[:4])\n',
             output="nte\nLant",
             note="From position 2 up to position 5, but not position 5 itself, like the open dot on a number line. "
                  "Leave out the start, and it begins at 0."),
        dict(concept="You can't change one letter",
             code='word = "Tusk"\nword = "D" + word[1:]\nprint(word)\n',
             output="Dusk",
             note="Like a word on a printed page, a string can't have one letter swapped: `word[0] = \"D\"` is a "
                  "TypeError. Build a new string, and put it back in the variable."),
        dict(concept="Escape marks: `\\\"` and `\\n`",
             code='print("Pell: \\"Fire!\\"\\nMoss: Why?")\n',
             output="Pell: \"Fire!\"\nMoss: Why?",
             note="`\\\"` puts a quote mark inside the quotes. `\\n` starts a new line, like pressing Enter. The "
                  "backslash never shows."),
        dict(concept="Methods hand back a new string",
             code='cry = "teal optic"\ncry.upper()\nprint(cry)\ncry = cry.upper()\nprint(cry)\n',
             output="teal optic\nTEAL OPTIC",
             note="A method is a tool you use with a dot, and it hands back a new copy. Alone on a line, the copy is "
                  "lost. Keep it with `=`: `cry = cry.upper()`. (Lesson: Words That Change Shape)"),
        dict(concept="`.upper()`, `.title()`, `.capitalize()`",
             code='said = "the FIRE is warm."\nprint(said.upper())\nprint(said.title())\n'
                  "print(said.capitalize())\n",
             output="THE FIRE IS WARM.\nThe Fire Is Warm.\nThe fire is warm.",
             note="`.upper()` makes every letter big, and `.lower()` makes every letter small. `.title()` makes the "
                  "first letter of each word big, like a book title. `.capitalize()` makes only the first letter big, "
                  "and the rest small."),
        dict(concept="Chain them: `.lower().capitalize()`",
             code='note = "MOSS IS ASLEEP."\nprint(note.lower().capitalize())\n',
             output="Moss is asleep.",
             note="Left to right, like two function machines in a row: each method works on the copy the one before "
                  "it handed back. You've seen this: `option_1.lower().capitalize()`."),
        dict(concept="`.split()` hands back a list",
             code='herbs = "moss fern reed"\nprint(herbs.split())\nprint("ash,elm".split(","))\n',
             output="['moss', 'fern', 'reed']\n['ash', 'elm']",
             note="Like cutting a sentence strip into word cards. Empty parentheses cut at every space. Text in the "
                  "parentheses says where to cut. The result is a list: count it with `len()`, and read it by "
                  "position."),
        dict(concept="`\" \".join(list)`: ask the glue",
             code='herbs = ["moss", "fern"]\nprint(" and ".join(herbs))\n',
             output="moss and fern",
             note="The glue goes first, then `.join`, then the list in parentheses. The glue goes between each two "
                  "pieces."),
        dict(concept="`.strip()` and `.replace(old, new)`",
             code='tag = "  Old Gate  "\ntag = tag.strip()\ntag = tag.replace("Old", "New")\nprint("[" + tag + "]")\n',
             output="[New Gate]",
             note="`.strip()` cuts the spaces off both ends, like trimming the edges of a page. `.replace(old, new)` "
                  "swaps every match, like Find and Replace. Capitals must match exactly."),
        dict(concept="`.find()` and -1",
             code='sign = "LANTERN"\nprint(sign.find("T"))\nprint(sign.find("Z"))\n',
             output="3\n-1",
             note="`.find()` works like Find (Ctrl+F). It hands back the position where the text starts, or -1 when "
                  "the text is not there. Here -1 means *not found*. It is not the last position."),
        dict(concept="`int(\"12\")`: digits to a number",
             code='print(int("12") + 1)\nprint(int(" 12 ") + 1)\n',
             output="13\n13",
             note="`int` is short for integer, a whole number. Only digits turn into a number. Spaces at the ends "
                  "are fine, but letters are not."),
        dict(concept="An f-string, and its `+ str()` twin",
             code='hero = "Oogrish"\ngold = 12\nprint(f"{hero}: {gold}")\nprint(hero + ": " + str(gold))\n',
             output="Oogrish: 12\nOogrish: 12",
             note="The same line, two ways. An f-string is text with blanks, like Mad Libs: Python fills each `{ }` "
                  "with what the variable holds. The campaign uses `+` and `str()`, so learn to read both. (Lesson: "
                  "Words That Change Shape)"),
        dict(concept="A bar for any numbers",
             code='def lamp(oil, most):\n    lit = "▓" * oil\n    off = "░" * (most - oil)\n'
                  '    return "Oil [" + lit + off + "]"\n\n\nprint(lamp(2, 6))\n',
             output="Oil [▓▓░░░░]",
             note="Stamp blocks with `*`. The parentheses make Python work out `most - oil` first, like PEMDAS. "
                  "You've seen this in the campaign's mana bars. (Lesson: Strings Are Rows of Letters)"),
        dict(concept="(extra) `in`: is it in there?",
             code='report = "The clock is red."\nprint("red" in report)\nprint("Red" in report)\n',
             output="True\nFalse",
             note="`in` asks a yes-or-no question: is this text somewhere inside? Capitals count. To ignore them, "
                  "ask `report.lower()` instead. (Extra practice: Letter by Letter)"),
        dict(concept="(extra) Letter by letter",
             code='for letter in "ash":\n    print(letter)\n',
             output="a\ns\nh",
             note="A `for` loop over text takes one letter at a time. (Extra practice: Letter by Letter)"),
        dict(concept="Error: changing a letter", code='word = "Tusk"\nword[0] = "D"\n',
             note="TypeError: 'str' object does not support item assignment. In plain words: you can't change one "
                  "letter of text (`str`). Build a new string: `\"D\" + word[1:]`."),
        dict(concept="Error: quotes inside quotes", code='print("Pell: "Fire!"")\n',
             note="SyntaxError: invalid syntax. Perhaps you forgot a comma? The quote mark before `Fire!` ends the "
                  "text early. Python's last line guesses a comma, but that guess is wrong here. Put a backslash in "
                  "front of each quote mark inside: `\\\"`."),
        dict(concept="Error: `.join` on the list", code='herbs = ["moss", "fern"]\nprint(herbs.join(" "))\n',
             note="AttributeError: 'list' object has no attribute 'join'. In plain words: a list has no `.join` "
                  "tool. Ask the glue instead: `\" \".join(herbs)`."),
        dict(concept="Error: text plus a number", code='gold = 12\nprint("Gold: " + gold)\n',
             note="TypeError: can only concatenate str (not \"int\") to str. In plain words: `+` glues text (`str`) "
                  "only to text, and `gold` is a whole number (`int`). Use `str(gold)`, or an f-string."),
        dict(concept="Error: not digits", code='print(int("twelve"))\n',
             note="ValueError: invalid literal for int() with base 10: 'twelve'. In plain words: `int()` can't read "
                  "the word twelve. Only digits turn into a number."),
        dict(concept="Error: past the end", code='rune = "Ash"\nprint(rune[3])\n',
             note="IndexError: string index out of range. In plain words: there is no letter at that position. The "
                  "last position is `len(rune) - 1`, which is 2. A slice never goes past the end: `rune[:9]` is only "
                  "`Ash`."),
        dict(concept="Error: a brace missing", code='gold = 12\nprint(f"Gold: {gold")\n',
             note="SyntaxError: f-string: expecting '}'. In plain words: a curly brace is missing. Every `{` needs "
                  "its `}`."),
        dict(concept="No error, wrong answer: no `f`",
             code='hero = "Moss"\nprint("{hero} waits.")\n',
             output="{hero} waits.",
             note="A quiet bug: the code runs, but shows the wrong thing. Without the `f`, the curly braces print as "
                  "they are. Put an `f` right before the quotes."),
        dict(concept="No error, wrong answer: -1 read as a position",
             code='sign = "LANTERN"\nspot = sign.find("Z")\nprint(sign[spot])\n',
             output="N",
             note="Another quiet bug. `.find()` gave -1, *not found*, but `sign[-1]` reads the last letter, so Python "
                  "shows `N` with no error. Check for -1 before you use the position."),
    ],
    notes=(
        "Cheatsheet 9 (the spec's list in order: `s[0]`, `s[-1]`, `s[2:5]`, `len(s)`; `\"C\" + s[1:]`; `\\\"` and "
        "`\\n`; methods return a new string; `.lower().capitalize()`; `.split()` / `\" \".join(list)`; `.strip()`, "
        "`.replace(a, b)`, `.find(x)` -> -1; `int(...)`; an f-string and its `+ str()` twin), then the bar "
        "(objective 7), the pool extras (`in`, a loop over letters), and the error rows and quiet bugs this unit "
        "catches. Entries with `output` are run and checked by the harness; the error rows have none. As Unit 3's "
        "ruling asks, no entry shares a name or number with the Quick Check (hush_line / calm_line, said / words / "
        "clipped, shield_bar / ore_gauge, Pell, Moss, EXIT, Interior, Flow, Glum, Ash Ward, Moon Step: the "
        "`.strip()` entry's text was Moon Step until form B's Q5 took it, and is Old Gate now) or with the "
        "lessons' tasks, so the page never "
        "hands over an answer: the spec's `int(\"48\")` is written `int(\"12\")` (48 + 1 is 8B-03's answer), and "
        "the f-string uses Oogrish's gold, not a task's mana. Code lines keep to 36 characters (checked by script)."
    ),
)


ITEMS = [
    QC8_A,
    QC8_A_QUESTIONS,
    QC8_B,
    QC8_B_QUESTIONS,
    CHALK_NOTES_9,
]
