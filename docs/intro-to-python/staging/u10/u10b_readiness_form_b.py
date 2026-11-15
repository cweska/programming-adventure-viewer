"""Unit 10 "Campaign Readiness Check" ("Before We Continue"), part b: Part 1 form B (the same 13 skills as form A, with
new names, numbers and situations: the quiz rc-part1-b-questions with the 12 questions of the 9 predict / mc / explain
items, first, then the testout rc-part1-b with its 9 code tasks), mini-boss B "Hold the Glow Ward" (rc-miniboss-b,
campaign mode for everyone, 5.4), and the optional advanced trial "Hold the Ember Ward from its goals"
(rc-trial-ember-ward, a challenge for ready-to-stretch students).

Spec: design/curriculum.md "## Unit 10" and "# 5. Campaign Readiness Check" (5.1 to 5.5): "Forms B and C reuse the
skills with new names and data. Form B: `step_east`, `get_farewell`, `dodge_check` (needed 14), `option 3`, a d8,
`shield_cost(...)`, and so on." Mini-boss B: "`use_ward(caster, ward)` with other heroes and costs." With the teacher's
decisions (design/teacher-decisions.md) and the teacher's review of Unit 10 (form B directives 1-10: questions
first, the retake summary, the Stuck line, `ward_name` in mini-boss B, the trial). Introduces nothing (concept_map.json
plans nothing for u10b). Independent of
Strings (T1): no code a student sees uses a Unit 9 token (const:escape, attr:upper, attr:title, attr:split,
attr:join, attr:strip, attr:replace, attr:find, node:FString), and no optional-only token either (tuples, zip,
comprehensions, .items(), defaults, keyword arguments, lambda, map, match, assert, input, int, **, %, //). The READY
path is proved by running the harness with the planned concept map moved aside (in a copy of the staging folder), so
the gate is built only from the real files u01-u07: no u08 or u09 token is open to u10b there.

Who this is for: the class already played campaign Modules 1 and 2 and struggled. Form B is the parallel form: a
retake, or the "parallel item from another form" after a review cycle (5.5), so it repeats no item of form A. Its
summary says so: open it when Mar'tu's notes send you here, for the one task they name. Questions come first, as in
form A, so the first win is a prediction; every task's Learn text ends with form A's Stuck line ("Stuck? Skip it, and
come back. A task you pass here stays ticked."). Mini-boss B is the follow-up for students who needed Mar'tu's version
on mini-boss A, so it stays dictated; the trial is the goal-only stretch for students who finished early. Every
student has their own device and does every item alone: no pair talk here (the evidence must be each student's own).

Item for item with form A (curriculum 5.3; each item's notes give `rc_item`, its skill tags, what this part checks and
the campaign part it prepares):
   1  predict      concat-str                         Q1  `"Shield: " + str(mana)`, then `+ "/" + str(max_mana)`
   2  code         replace-pass                       C1  step_east (the scout)
   3  predict+code chain-methods, store-then-pass     Q2  get_farewell tidies "SAFE ROADS, LUCKY."; C2 present_farewell
   4  predict x2   boundary, return-comparison,       Q3  dodge_check, needed = 14, at 13 / 14 / 15; Q4 the ledger shape
                   trace-call                             (armor_score(4, 5) + 3), typed, no choices
   5  predict+code elif-chain, quote-text             Q5  trace on "option 3"; C3 mend `elif choice == option 2:`
   6  code+predict dict-read, dict-nested, dict-write, C4  Bomb Shell's sheet, `book[ward_name] = ward`; Q6 `in` on keys
                   dict-in, dict-key-from-variable
   7  predict+code repeat-string                      Q7  `"█" * 4 + "░" * 3`; C5 mend `"░" * max_mana - mana`
   8  mc+code      randint, randint-param             Q8  a d8; C6 throw_die(die_size)
   9  explain+pred func-as-value, call-stored-func    Q9  `charms["spark"]` vs `charms["spark"](gearshift)`; Q10 predict
  10  trace+explain list-of-dicts, for-each           Q11 how many calls, with what; Q12 what `member` holds
  11  code (3 CPs) read-traceback                     C7  KeyError 'Mana', TypeError (str + int), NameError 'totl'
  12  code         dict-write, reassign,              C8  spend `cost` from `oogrish["mana"]`
                   combine-values
  13  code         param-use, return-right-name,      C9  shield_cost(plates, price_per_plate), Example `double(n)`
                   exact-names

How the two parts are represented with the schema's existing fields (as form A does; no new fields):
  * Part 1 is unaided: the testout's exercises are support="none" (no hints, Another way, Assemble it, tracer,
    predict or Compare) and explainer="lean". The glossary and read-aloud stay on. Their hints exist only because the
    schema needs two; they never hold a finished line. No assemble, no another_way. Every typed task is behavior-checked
    with other values (CMB, PAR, CALL, RND, KEY, STO), never OUT alone. Check messages are lean: the slip and the
    evidence, never the fix (as QC2, QC-R1 and QC-R2).
  * The 12 questions are the quiz rc-part1-b-questions (listed first in ITEMS); questions_to_pass=10 on the testout
    approximates "Part 1 >= 11/13" (every code task is required by the testout; two question misses allowed). The
    trace item (Q4, the ledger shape) is typed, with no choices, so the answer is in no visible text, as form A's now
    is; the explanation traces another call (armor_score(2, 1), kept because the same question can be retaken) and
    names the two slip values (11: the numbers written in the function; 12: the numbers handed in). A quiz has no
    Run, so nothing there can be pasted and run (the trace guard paste_stop belongs to a ledger's own editor; there
    is none here).
  * Part 2, the mini-boss, is a project with support="light", solo=True (every student alone; solo also turns off
    Start me off and the Learn-pane Another way) and explainer="lean". No assemble, no tracer, no predict. Hints are
    capped at rung 2 by writing: Where to look plus two Teach rungs; the last rung (which the site labels "Show me
    how") is written at teach level, with no finished line and no code span that gives a Start me off. Compare with
    Mar'tu's version is the site's own (the intro promises 5 minutes; the course setting also opens it after 4 counted
    failed runs). It has the same shape as form A's mini-boss, so a retake asks for the same help: the six numbered
    comments and checkpoints in the campaign's check order (the comments and the intro say the numbers are the
    checks' order: the code tests the caster first), the same rung-2 ladder (CP1 says early that the cast moves
    under `else:`, CP2 pays with `jar["honey"] - spoon["size"]`, CP3's third rung is the jar / spoon picture), and
    the same campaign-like messages (what the check expects and what happened, with the evidence in short sentences
    and no brackets inside brackets, never the finished line). Only the names and data differ.
  * The trial is a challenge (level="advanced", optional, ~15 min) with support="light", solo=True and
    explainer="lean": the same campaign part from its goals only (every checkpoint dictated=False), with the guard
    and one comment given ("# Get it, compare, act."). It reuses mini-boss B's six checks and its two-messages
    check (one set of check bodies, filled with each function's names through `_C`), with a third set of names:
    `raise_ward(mage, ward_name)`, Oogrish's sheet and the Ember Ward, and Briar Ring as the check ward. Ladders are
    Where to look plus two teach rungs, with no finished line and no Start me off. Not counted for Ready.

Check codes (curriculum 2.5), built from one helper prelude (_BX). check() puts in front of each check only the
helpers it uses (as u07a / u07c / u10a do). Every call a check makes uses fresh values the task never uses (lint b),
with prints kept private; nothing a check does shows in the console:
  NAME/DEF  _find / _params: a function made with `def`, its exact name (near misses, a variable made with `=`), its
           exact parameters in order. Lean wording, never the `def` line.
  CALL     C1: the scout recorder (setup) moves once, east, only when `step_east()` is called. C2: the ley board
           recorder gets the helper's line once. C7: each traceback's function is called with fresh values.
  CMB      _rerun() runs the program again in a fresh namespace (setup first, prints private) with a line slipped in
           right after the statement that makes a name: another `choice`, another sheet in `bomb_shell` / `oogrish`,
           another `ward_name` and `ward`, other mana numbers, another cost. A typed value cannot follow; its message
           takes form A's words ("`mana_now` holds a typed 17. Mar'tu's check put another sheet in `bomb_shell`, and
           `mana_now` still said 17."). C2 also swaps `get_farewell` for one that returns another line.
  STO      C2: inside present_farewell, the helper's result is stored in a variable, and that variable is passed on.
           When the board does show the line, the message says so first, in form A's words ("Your line runs, and
           the board shows the line. But ...").
  KEEP     the finished helpers (`get_farewell`, the mini-boss's `show_mana`) are unchanged (AST compare). The
           mini-boss's given guard is behavior-checked in CP1, as form A's is (a ward the caster doesn't know is
           still turned away). C1, C2, C6, C9 and the mini-boss also name a given call at the bottom left without
           brackets (`step_east`, `print(throw_die)`), so the student's own run is never green and empty.
  KEY      C4: the page is stored under the name in `ward_name` (a quoted variable name, a typed key, a rebuilt book
           that loses its first page, a page that is not `ward`); C8: the new mana under another key.
  STREXACT C3: a compared text that differs from an option only in capitals or spaces.
  RND      C6: `random.randint` swapped for a scripted die that records its arguments; sizes 12 and 4.
  PAR / PAR-CONST / RET / RET-PARAM / PNM / RNM  C9: shield_cost called with (5, 7) and (6, 9) (the task's own call
           is (3, 4): 12, so no fresh set collides); print for return, no return and a blank return (each says
           `None` is "Python's word for nothing"), the same answer twice (the numbers are typed in the function), a
           typed multiplier (`plates * 2`), a parameter returned as it came in, a near-miss parameter, the
           Example's `answer`.
  BND      the mini-boss (and the trial) casts for a fresh hero (Ivo, mana 14 of 20; every other turned-away case is
           Moss, so a name copied from a message is a typed name) with a fresh ward (Ember Wall; the trial's Briar
           Ring): affinity below, at and above the need (the visible ward's own need as the typed-number trap), mana
           below, at and above the cost (its cost as the trap, and a need below the cost so a test on the wrong key
           shows), both too low at once, costs 2 and 9 from mana 14 and 17 (a typed cost, a typed result, a typed 4
           from the message or a typed start of 14 each fail). CP4 also asks for two messages, not the same words for
           both reasons.
Messages use invented Tor names only in check data (Brakka, Pell, Ivo, Moss, Ember Wall, Briar Ring, Ash Veil, Star
Shard, "A grumpy moth") and the party's real values; a student's own text is never repeated back (text shows as "some
text").

The class's slips, each proven by a wrong_answers entry (in the task named):
  * typed values instead of reading or handing over (CMB): C2 (a typed board line, a typed store), C3 (the chain
    replaced by one print), C4 (17, 6, `book["Teal Wall"]`, a typed copy of the page), C5 (`"░" * 5`, `"░░░░░"`,
    `"░" * (9 - 4)`), C6 (`randint(1, 8)`), C7 (`return 4`, a typed ore line, `return 10`), C8
    (`oogrish["mana"] = 13`, a typed cost, a typed start `18 - cost`), C9 (`return 12`, `plates = 3` inside,
    `plates * 4`, `3 * price_per_plate`), the mini-boss and the trial (a typed cost, a typed result, a typed 4 from a
    check message, a typed start of 14, typed numbers in the tests, a typed hero name, the check's own hero name
    copied, a typed ward name, the effect's words printed);
  * print instead of return: C6 (print the roll), C7 (print the total), C9, and its mirror in C2 (stored, then
    returned: "The function returns the line, so it goes back to the caller and never reaches the ley board.");
    = vs ==: C3 (`elif choice = ...`), C8
    (`==` for `=`); > vs >= at the boundary: Q3, the mini-boss CP3 / CP5 (`<=`); unquoted text: C1 (`east`), C3
    (`option 2`, the starter); quoted names (KEY): C4 (`book["ward_name"]`); a missing colon: C1, C3, C9, the
    mini-boss; a missing indent: C1 (the scout line at the left edge, an unindented body), C2 (the pass-on line at
    the left edge), the mini-boss (cast lines not under `else:`); def vs =: C1 (`def step_east = ...`), C9 (`def
    shield_cost = ...`); calling vs handing over (): C2 (no `()` on the helper, `farewell()` called), the mini-boss
    (the effect read, never called; form A's habit `ward["effect"]`; `ward_name["effect"]`, the name read as a
    page), Q9 / Q10; skipping a nesting level: C4 (`bomb_shell["dexterity"]`), the mini-boss
    (`caster["magical_affinity"]`); str() before +: C7 CP2 (and the call mended instead of the line); parentheses in
    "░" * (max_mana - mana): C5; resetting a total inside a loop: C7 CP3 (`total = 0` moved into the loop);
    approximate parameter names: C9 (`price`, `def shield_cost(plate, price):`); editing a helper you were told to
    leave alone: C2 (`get_farewell`), the mini-boss (`show_mana`, and the given guard's `return` or the whole guard).
    Also: calling vs naming at the bottom (C1 `step_east`, C2 `present_farewell`, C6 `print(throw_die)`, C9
    `print(shield_cost)`, the mini-boss `use_ward`, `show_mana` with no `()`, `print()` around the effect); `=` for
    `def` (C9 `shield_cost = 12`); an extra indent (C7 `return` inside the loop); the wrong key on a page (the
    mini-boss: affinity against the cost, mana against the need); one test merged with `or` (the mini-boss CP4).

Deviations from the spec, each small and noted on its item:
  * C3 mends `option 2` and Q5 traces `option 3` (form B's "option 3"); form A traces option 2 and mends option 3, so
    no line repeats across the forms.
  * Q2 (item 3a) tidies other words than C2's helper ("SAFE ROADS, LUCKY." against "WATCH THE ARC, FRIENDS."), so a
    student who runs C2 first does not see the answer to 3a on the board.
  * C7 (item 11) puts each slip in its own small function with the calls at the bottom, so each traceback is a live
    one, and the checks call each function with fresh values. No partials: Python stops at the first slip, so a
    program with one slip mended still crashes at the next, and no check can run on it.
  * C2 (item 3b) has two checkpoints, store then pass on (form A's task has one): the same work, and the store gets
    its own STO message and a partial.
  * Q4 (item 4b, the ledger shape) is typed, with no choices, where form A's 4b offers four: the honest-tracing rule
    (no answer in any visible text). Worth aligning one way or the other, so the forms ask the same.
  * The mini-boss renames the spec's `use_ward(caster, ward)` to `use_ward(caster, ward_name)`, so `ward` never means
    the name (as in form A, and in this file's own read-and-write task, where `ward` is the page). The page stays
    `page`: the given line is `page = caster["wards"][ward_name]`. The student writes `page["effect"](caster)`.
  * The trial is new (the teacher's directive 10): not in 5.4, optional, advanced, and not counted for Ready.
  * Q4's explanation names the two slip values (11 and 12) after the other call's trace.

What the site does not yet support (listed for the handback; no field was invented):
  * Readiness scoring: the 5.5 heuristic (Part 1 >= 11/13 items, item 6 at >= 3 of 4 parts, item 13 passed; the
    mini-boss's 6 checks without Compare; Ready / Ready with a review list / Review first). A testout passes only
    when every code task passes, and an item that spans a task and a question (3, 5, 6, 7, 8) is not scored as one.
  * Skill-tag routing: each item's skills and campaign part live in `notes` only (meta lines), so the per-missed-skill
    review routing, the per-part Band A / B view and "Mar'tu's notes" need site work.
  * Campaign mode on a project or challenge: a hint cap at rung 2 (here written into the ladder), Compare by time
    only (5 minutes, as the intro promises; the course setting also opens it after 4 failed runs), and a record of
    whether Compare was opened, which the Ready rule needs (a pass after Compare should point the student to
    mini-boss B). Form choice: nothing yet draws form B for a retake or a review cycle, and a quiz retake does not
    draw another form's questions.
  * The trial: nothing marks a challenge "not counted for Ready" (its meta line says counts_for_ready=false), and no
    route offers it only to students who finished Part 2 early.
  * The testout wiring (the teacher's site request): a testout leaves the item list and its pass marks the whole
    unit tested out. Form B is optional=True, so the site's "required testout is a core item" fix keys on form A's
    rc-part1-a only; form B's pass must not mark the mini-boss, rc-explain or the trial tested out.

Correct-but-different answers that pass (checked by script): other variable names (in the trial, any name for the
page, or no page variable at all), the trial's tests written positive-first or with early returns, single quotes, a keyword
argument (`scout.step(direction="east")`, `random.randint(a=1, b=die_size)`), `from random import randint`, a copy
of the stored variable (`message = farewell`), `-=`, a two-step read or bar, `.get()`, `print("Ore left:", ore)`,
`sum(costs)`, reversed comparisons, the tests written positive-first, a re-read page, messages in any words, and a
changed starting number in C5 / C8 (judged by the student's own numbers; the reruns still pin the behavior).

Phone width: starters, question code and fenced pictures keep to 36 characters, except the campaign's own shapes in the
mini-boss and the trial: the given guard (`if ward_name not in caster["wards"]:`, 40, and its print line, 41; the
trial's `mage` guard, 38 and 41) and the given page line `page = caster["wards"][ward_name]` (37), as form A's guard
is; and in Mar'tu's versions the nested affinity test and the subtraction, as Units 5 and 7 did. Checked by script.

Python's messages were checked in CPython 3.13 (the site runs 3.13): `elif choice == option 2:` -> "invalid syntax";
`elif choice = "option 2":` -> "invalid syntax. Maybe you meant '==' or ':=' instead of '='?"; a missing colon ->
"expected ':'"; `def step_east = ...` -> "expected '('"; an unindented body -> "expected an indented block after
function definition"; `"░" * max_mana - mana` -> "unsupported operand type(s) for -: 'str' and 'int'"; `ward["Mana"]`
-> KeyError: 'Mana'; `"Ore left: " + ore` -> "can only concatenate str (not "int") to str"; `return totl` -> "name
'totl' is not defined"; `get_farewell() = farewell` -> "cannot assign to function call"; `book[ward] = ward_name` ->
"unhashable type: 'dict'"; `random.randint(die_size)` -> "missing 1 required positional argument: 'b'".

Verify:
    PROTOTYPE_DIR=<staging dir> python3 docs/intro-to-python/prototypes/harness.py u10b
"""

QUOTES_RULE = "Quotes mean these exact letters. No quotes means look inside the box with this label."
M1 = "leylines-awaken"
M2 = "friends-in-low-places"


def meta(**fields):
    """The 2.12 rule 14 `meta:` line (first line of an exercise's notes until the schema has these fields)."""
    return "meta: " + "; ".join(f"{key}={value}" for key, value in fields.items())


def fill(template, **values):
    """Check code from a template: each __NAME__ token becomes repr(value) (a message, a number, a list)."""
    out = template
    for key, value in values.items():
        out = out.replace("__" + key.upper() + "__", repr(value))
    return out


# ---------------------------------------------------------------------------------------------
# Check helpers (plain Python, run in the student's namespace after their code). check() puts in front of each
# check only the helpers it uses, and the helpers those use, so the unit JSON stays small (as u07a / u10a do).
# ---------------------------------------------------------------------------------------------

_BX = r'''import ast as _ast
import io as _io
import random as _random
import sys as _sys
_g = globals()
_tree = _ast.parse(_source)
_QUOTES = __QUOTES__
_SETUP = __SETUP__


def _show(_v):
    # A value in a message: numbers and code names only, never a student's own words (2.11).
    if _v is None:
        return '`None`'
    _t = type(_v).__name__
    if _t == 'function':
        return 'the function `' + _v.__name__ + '`'
    if _t in ('int', 'float', 'bool'):
        return '`' + str(_v) + '`'
    if _t == 'str':
        return 'some text'
    return {'dict': 'a dictionary', 'list': 'a list'}.get(_t, 'a ' + _t)


def _ev(_what, _said=''):
    return " (Mar'tu's check " + _what + ', only inside the check' + ((': ' + _said) if _said else '') + '.)'


def _err(_e):
    return type(_e).__name__ + (': ' + str(_e) if str(_e) else '')


def _edits(_a, _b):
    _prev = list(range(len(_b) + 1))
    for _i, _x in enumerate(_a, 1):
        _cur = [_i]
        for _j, _y in enumerate(_b, 1):
            _cur.append(min(_prev[_j] + 1, _cur[_j - 1] + 1, _prev[_j - 1] + (_x != _y)))
        _prev = _cur
    return _prev[-1]


def _close(_a, _b):
    # A near miss for a name: case, a plural, 1-2 edits, a shared word, or one inside the other.
    if type(_a).__name__ != 'str' or type(_b).__name__ != 'str' or _a == _b:
        return False
    _la, _lb = _a.lower(), _b.lower()
    if _la == _lb or _la + 's' == _lb or _lb + 's' == _la:
        return True
    if min(len(_la), len(_lb)) >= 3 and _edits(_la, _lb) <= 2:
        return True
    _wa = set(_w for _w in _la.split('_') if len(_w) >= 4)
    _wb = set(_w for _w in _lb.split('_') if len(_w) >= 4)
    return bool(_wa & _wb) or (len(_la) >= 4 and (_la in _lb or _lb in _la))


def _names(_ps):
    _q = ['`' + _p + '`' for _p in _ps]
    if not _q:
        return 'nothing'
    return _q[0] if len(_q) == 1 else ', '.join(_q[:-1]) + ' and ' + _q[-1]


def _params(_f):
    _c = getattr(_f, '__code__', None)
    return list(_c.co_varnames[:_c.co_argcount]) if _c is not None else []


def _defs():
    return {_n.name: _n for _n in _tree.body if type(_n).__name__ == 'FunctionDef'}


def _top():
    return [_n for _n in _tree.body if type(_n).__name__ != 'FunctionDef']


def _is_call(_n, _name):
    return type(_n).__name__ == 'Call' and type(_n.func).__name__ == 'Name' and _n.func.id == _name


def _calls_in(_nodes, _name):
    return [_c for _n in _nodes if _n is not None for _c in _ast.walk(_n) if _is_call(_c, _name)]


def _made_by(_n):
    # The names a statement makes with `=`, `+=` or `def`.
    _k = type(_n).__name__
    if _k in ('FunctionDef', 'ClassDef'):
        return [_n.name]
    _ts = list(_n.targets) if _k == 'Assign' else ([_n.target] if _k in ('AugAssign', 'AnnAssign') else [])
    return [_t.id for _t in _ts if type(_t).__name__ == 'Name']


def _from_call(_node, _name):
    # The variables inside _node that are given the result of a call to _name.
    return [_x for _n in _ast.walk(_node) if type(_n).__name__ == 'Assign' and _is_call(_n.value, _name)
            for _x in _made_by(_n)]


def _find(_name):
    # The student's function `_name`, or the lean message that says why it is not there.
    _v = _g.get(_name)
    if callable(_v) and type(_v).__name__ == 'function':
        return _v, ''
    if _name in _g:
        return None, '`' + _name + '` is not a function: a line with `=` put a value in it.'
    _near = sorted(_k for _k, _x in list(_g.items()) if type(_x).__name__ == 'function' and not _k.startswith('_')
                   and _close(_k, _name))
    if _near:
        return None, ('Python matches names letter for letter: the code has `' + _near[0] + '`, and the task names `'
                      + _name + '`.')
    return None, 'No function called `' + _name + '` was made.'


def _call(_f, _args=()):
    # Call _f with its prints kept private. Returns (value, printed lines, error or None).
    _buf = _io.StringIO()
    _keep_out = _sys.stdout
    _sys.stdout = _buf
    _val, _e = None, None
    try:
        _val = _f(*_args)
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    return _val, [_l.strip() for _l in _buf.getvalue().splitlines() if _l.strip()], _e


def _keep(_name, _orig):
    # KEEP: '' when the function is exactly the starter's (comments aside), else 'gone' or 'changed'.
    _d = _defs().get(_name)
    if _d is None:
        return 'gone'
    _o = [_n for _n in _ast.parse(_orig).body if type(_n).__name__ == 'FunctionDef' and _n.name == _name][0]
    return '' if _ast.dump(_d) == _ast.dump(_o) else 'changed'


def _die(_log):
    # A scripted randint: records what it was asked, and rolls one below the top face (a d12 rolls 11). Its
    # parameters are named a and b, like the real one, so `random.randint(a=1, b=die_size)` works too.
    def randint(a, b):
        _log.append((a, b))
        if type(a).__name__ == 'int' and type(b).__name__ == 'int' and b > a:
            return b - 1
        return a
    return randint


def _rolled(_f, _args=()):
    # The pretend die stands in for `random.randint`, and for a `randint` the code brought in by name
    # (`from random import randint`), only during this one call.
    _log = []
    _real = _random.randint
    _fake = _die(_log)
    _fg = getattr(_f, '__globals__', _g)
    _own = [_k for _k, _v in list(_fg.items()) if _v is _real]
    _random.randint = _fake
    for _k in _own:
        _fg[_k] = _fake
    try:
        _val, _rows, _e = _call(_f, _args)
    finally:
        _random.randint = _real
        for _k in _own:
            _fg[_k] = _real
    return _val, _rows, _e, _log


def _uncalled():
    # A top-level line that names one of the code's own functions with no brackets after it, so it never runs
    # (or prints the function itself). '' when there is none.
    _fns = set(_defs())
    for _n in _top():
        if type(_n).__name__ != 'Expr':
            continue
        _v = _n.value
        if type(_v).__name__ == 'Name' and _v.id in _fns:
            return 'Line ' + str(_n.lineno) + ' names `' + _v.id + '` with no brackets after it, so it never runs.'
        if _is_call(_v, 'print'):
            for _a in _v.args:
                if type(_a).__name__ == 'Name' and _a.id in _fns:
                    return 'Line ' + str(_n.lineno) + ' prints the function `' + _a.id + '` itself: nothing calls it.'
    return ''


def _rerun(_changes=()):
    # The program again in a fresh namespace: setup, then the student's code, prints kept private. Each change's
    # line runs right after the first top-level statement of the student's code that makes its name.
    _body, _found = [], []
    for _code, _mine in ((_SETUP, False), (_source, True)):
        for _n in (_ast.parse(_code).body if _code.strip() else []):
            _body.append(_n)
            if _mine:
                for _anchor, _line in _changes:
                    if _anchor not in _found and _anchor in _made_by(_n):
                        _found.append(_anchor)
                        _body.extend(_ast.parse(_line).body)
    _mod = _ast.Module(body=_body, type_ignores=[])
    _ast.fix_missing_locations(_mod)
    _ns = {'__name__': '__main__'}
    _out, _keep_out, _e = _io.StringIO(), _sys.stdout, None
    _sys.stdout = _out
    try:
        exec(compile(_mod, 'main.py', 'exec'), _ns)
    except SystemExit:
        pass
    except Exception as _x:
        _e = _x
    finally:
        _sys.stdout = _keep_out
    _ls = [_l.strip() for _l in _out.getvalue().splitlines() if _l.strip()]
    return _ns, _ls, _e, [_a for _a, _l in _changes if _a not in _found]


def _gone(_miss):
    return 'The line `' + _miss + " = ...` is gone from the code, so Mar'tu's check could not try other values."


def _stopped(_fn, _ps, _e, _foreign=()):
    # Lean: what stopped a call inside the student's function, never the name to write instead.
    if type(_e).__name__ == 'NameError':
        _m = getattr(_e, 'name', '') or ''
        if _m in _foreign or [_x for _x in _foreign if len(_x) > 3 and _edits(_m.lower(), _x.lower()) <= 2]:
            return ' `' + _m + '` is a name from the Example, not from this function.'
        if [_p for _p in _ps if _close(_m, _p)]:
            return ' `' + _m + "` is not one of this function's parameters, letter for letter."
        return ' No variable named `' + _m + '` is made inside `' + _fn + '`.'
    return ''
'''


def _bx_parts():
    """_BX split into its setup lines and its helper functions, each with the helper names it uses."""
    import ast

    tree = ast.parse(_BX)
    head, defs = [], {}
    for node in tree.body:
        text = ast.get_source_segment(_BX, node)
        if isinstance(node, ast.FunctionDef):
            defs[node.name] = (text, {n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        else:
            head.append(text)
    return head, defs


_BX_HEAD, _BX_DEFS = _bx_parts()


def check(label, body, setup="", **values):
    """(label, code): the _BX setup lines, the helpers this check uses (and the helpers those use), then the body."""
    import re

    code = fill(body, **values)
    need, todo = set(), set(re.findall(r"\b_\w+", code))
    while todo:
        name = todo.pop()
        if name in _BX_DEFS and name not in need:
            need.add(name)
            todo |= _BX_DEFS[name][1]
    head = "\n".join(_BX_HEAD).replace("__QUOTES__", repr(QUOTES_RULE)).replace("__SETUP__", repr(setup))
    helpers = [text for name, (text, _) in _BX_DEFS.items() if name in need]
    return (label, head + "\n\n\n" + "\n\n\n".join(helpers) + "\n\n\n" + code.strip("\n") + "\n")


# =============================================================================================
# UNIT (copied verbatim from u10a: the exporter requires every field two parts give to match)
# =============================================================================================

UNIT = dict(
    id="readiness-check",
    order=10,
    title="Campaign Readiness Check",
    subtitle="Before We Continue",
    published=True,
    martu_intro=(
        "You have learned enough to help, yes? Show me without the hints. Then we continue.\n"
        "This is practice, never a grade. It shows me what you can do alone now, and what we look at once more.\n"
        "Part 1 has short tasks and questions, with no hints. Part 2 is a whole campaign part, with only the help "
        "the campaign gives. Then one click: explain a line you wrote.\n"
        "Once, this code was a wall. Now you take it apart yourself."
    ),
    goals=[
        "Read every line of a campaign part's starter code, and say what it does",
        "Make the campaign's one-line edits with no hints: replace `pass`, store then pass, read and write a "
        "sheet, roll a die",
        "Read a traceback and mend the line it names",
        "Finish a whole campaign part with only the campaign's help: hold the ward with `if`, `elif` and `else`",
        "Explain a line you wrote, in plain words",
    ],
    campaign_links=[M1, M2],
)

# No new terms: every [[link]] in this file is defined in an earlier unit or in u10a ("campaign mode").
GLOSSARY = []


def _rc(item, part, skills, checks, prepares, **more):
    """The meta line every Part 1 item carries (5.3): its item number, its skill tags (the same as form A's, item for
    item), the tags this part checks, and the campaign part it prepares."""
    return meta(rc_item=item, form="B", part=part, skills=skills, checks=checks, prepares=prepares, solo="true", **more)


_P1_NOTE = ("Part 1 is unaided: support='none' (no hints, Another way, Assemble it, tracer or Compare) and "
            "explainer='lean'; glossary and read-aloud stay on. The hints exist because the schema needs two; they "
            "never hold a finished line. Check messages are lean: the slip and the evidence, never the fix.")
# The last line of every Part 1 task's Learn text, as form A's.
_STUCK = "Stuck? Skip it, and come back. A task you pass here stays ticked."


# =============================================================================================
# Part 1 form B, code tasks (testout rc-part1-b)
# =============================================================================================

# ---------------------------------------------------------------------------------------------
# C1 (item 2) step east: replace-pass. CALL on the scout recorder.
# ---------------------------------------------------------------------------------------------

SCOUT_SETUP = (
    "class Scout:\n"
    "    def __init__(self):\n"
    "        self.steps = []\n"
    "    def step(self, direction):\n"
    "        self.steps.append(direction)\n"
    "        print('The scout steps ' + str(direction) + '.')\n"
    "scout = Scout()\n"
)
STEP_HEAD = "# Replace pass with a command\n# that moves the scout east.\ndef step_east():\n"
STEP_TAIL = "\n\n# Mar'tu's map calls it:\nstep_east()\n"


def _step(body="    pass\n", head=STEP_HEAD, tail=STEP_TAIL):
    return head + body + tail


STEP_STARTER = _step()
STEP_SOLUTION = _step('    scout.step("east")\n')

_STEP = r'''
_f, _m = _find('step_east')
assert _f, _m
_sc = _f.__globals__.get('scout')
assert type(_sc).__name__ == 'Scout', 'A variable of your own is named `scout`, so the scout from the starter is gone.'
_at = len(_sc.steps)
_what = 'called `step_east()`'
_v, _rows, _e = _call(_f)
assert _e is None, 'Calling `step_east()` stopped Python: ' + _err(_e) + '.' + _ev(_what)
_new = _sc.steps[_at:]
if not _new:
    _out = [_c for _n in _top() for _c in _ast.walk(_n) if type(_c).__name__ == 'Call'
            and type(_c.func).__name__ == 'Attribute' and _c.func.attr == 'step']
    assert not _out, ('`step_east()` did not move the scout: the `scout.step` line sits outside the function, at the '
                      'left edge.' + _ev(_what))
    assert False, '`step_east()` did not move the scout.' + _ev(_what)
assert len(_new) == 1, '`step_east()` moved the scout ' + str(len(_new)) + ' times.' + _ev(_what)
_s = _new[0]
assert not (type(_s).__name__ == 'str' and _s != 'east' and _s.strip().lower() == 'east'), (
    '`step_east()` stepped with other letters than `"east"`: capitals and spaces count.' + _ev(_what))
assert _s == 'east', ('`step_east()` moved the scout ' + (_s if _s in ('north', 'south', 'west') else 'somewhere else')
                      + '.' + _ev(_what))
_u = _uncalled()
assert not _u, _u
'''

STEP_EAST = dict(
    id="step-east",
    title="Step east",
    martu=(
        "Campaign style, yes? The `def` line is written, and `pass` holds its place.\n"
        "The scout moves with a command like `scout.step(\"north\")`. My check calls your function, only inside the "
        "check.\n" + _STUCK
    ),
    setup=SCOUT_SETUP,
    names=["step_east"],
    support="none",
    explainer="lean",
    starter=STEP_STARTER,
    checkpoints=[
        dict(
            id="scout-steps-east",
            text="Replace `pass` with a command that moves the scout east.",
            dictated=False,
            hints=[
                "Look at the function's name: it says which way to go.",
                "A command that takes a word needs that word in quotes, inside the brackets.",
                "The direction goes in small letters, exactly as the name spells it.",
            ],
            checks=[check("step_east moves the scout east", _STEP)],
            pass_line="Mar'tu: East, and only when it is called. Good.",
        ),
    ],
    solution=STEP_SOLUTION,
    wrong_answers=[
        dict(why="the starter (pass)", code=STEP_STARTER, fails_at=1, message_contains="did not move the scout"),
        dict(why="unquoted text: scout.step(east) (NameError)", code=_step("    scout.step(east)\n"), fails_at=0,
             message_contains="name 'east' is not defined"),
        dict(why="the wrong direction (copy-paste from the example)", code=_step('    scout.step("north")\n'),
             fails_at=1, message_contains="moved the scout north"),
        dict(why="the opposite direction", code=_step('    scout.step("west")\n'), fails_at=1,
             message_contains="moved the scout west"),
        dict(why="a capital letter in the text", code=_step('    scout.step("East")\n'), fails_at=1,
             message_contains="capitals"),
        dict(why="the campaign's engine name copied (party is not here)", code=_step('    party.move("east")\n'),
             fails_at=0, message_contains="name 'party' is not defined"),
        dict(why="the step at the left edge, under pass (a missing indent: it runs at once, not when called)",
             code=_step("    pass\nscout.step(\"east\")\n"), fails_at=1, message_contains="outside the function"),
        dict(why="print instead of a command", code=_step('    print("east")\n'), fails_at=1,
             message_contains="did not move"),
        dict(why="a missing colon on the def line", code=_step('    scout.step("east")\n',
                                                               head=STEP_HEAD.replace("():", "()")),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the body not indented (IndentationError)", code=_step('scout.step("east")\n'), fails_at=0,
             message_contains="expected an indented block"),
        dict(why="def used like = (def vs =)", code=(
            "# Replace pass with a command\n# that moves the scout east.\ndef step_east = scout.step(\"east\")\n"
            + STEP_TAIL), fails_at=0, message_contains="expected '('"),
        dict(why="two steps in one call", code=_step('    scout.step("east")\n    scout.step("east")\n'), fails_at=1,
             message_contains="2 times"),
        dict(why="the map's call left without () (calling vs naming): nothing moves in the student's own run",
             code=_step('    scout.step("east")\n', tail="\n\n# Mar'tu's map calls it:\nstep_east\n"), fails_at=1,
             message_contains="no brackets after it"),
    ],
    notes=_rc(2, "code", "replace-pass", "replace-pass", "program-movement", starter_level="S4", path="READY",
              dictates="", foreign_names="north") + "\n"
    "C1, item 2 (form A: step_west). Campaign-style starter (G3 R18): the `def` line and `pass`. CALL: the check calls "
    "`step_east()` itself and reads the scout recorder (setup): one step, `\"east\"`, and only when called (a step at "
    "the left edge runs at load and is named). Fails on (spec): `scout.step(east)` -> crash (the explainer's NameError "
    "row); `\"west\"` -> CALL. The Learn text shows `scout.step(\"north\")`, the campaign's own kind of example, so "
    "`\"north\"` is also a wrong answer. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C2 (item 3b) present farewell: store-then-pass (3a, chain-methods, is quiz Q2). STO, CALL, CMB, KEEP.
# ---------------------------------------------------------------------------------------------

BOARD_SETUP = (
    "_board = []\n"
    "\n\n"
    "def show_on_ley_board(text):\n"
    "    _board.append(text)\n"
    "    print('[Ley board] ' + str(text))\n"
)
FAREWELL_DEF = (
    "def get_farewell():\n"
    '    line = "WATCH THE ARC, FRIENDS."\n'
    "    line = line.lower()\n"
    "    line = line.capitalize()\n"
    "    return line\n"
)


def _farewell(present="    pass\n", helper=FAREWELL_DEF, tail="\n\npresent_farewell()\n"):
    return (
        "# get_farewell() is finished.\n"
        "# Leave it as it is.\n"
        + helper +
        "\n\n"
        "# Finish present_farewell():\n"
        "# 1. Store the result of\n"
        "#    get_farewell() in a variable.\n"
        "# 2. Pass that variable to\n"
        "#    show_on_ley_board().\n"
        "def present_farewell():\n"
        + present + tail
    )


FW_STORE = "    farewell = get_farewell()\n"
FW_PASS = "    show_on_ley_board(farewell)\n"
FAREWELL_STARTER = _farewell()
FAREWELL_SOLUTION = _farewell(FW_STORE + FW_PASS)

_FW_STORE = r'''
_k = _keep('get_farewell', __ORIG__)
assert _k != 'gone', 'The finished `get_farewell()` is gone from the code.'
assert not _k, '`get_farewell()` is not the same as in the starter, and it was marked finished.'
_fs, _m = _find('present_farewell')
assert _fs, _m
_d = _defs()['present_farewell']
if not _from_call(_d, 'get_farewell'):
    _bare = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Name'
             and _n.value.id == 'get_farewell']
    assert not _bare, '`present_farewell()` stores the function `get_farewell` itself: nothing calls it.'
    _outside = [_n for _n in _top() if type(_n).__name__ == 'Assign' and _is_call(_n.value, 'get_farewell')]
    assert not _outside, 'The result of `get_farewell()` is stored outside `present_farewell()`, at the left edge.'
    _direct = [_c for _c in _calls_in([_d], 'show_on_ley_board') if [_a for _a in _c.args if _is_call(_a, 'get_farewell')]]
    if _direct:
        # Run it once, privately: when the board does show the line, say so first (as form A's STO message).
        _bd = _fs.__globals__.get('_board')
        _at = len(_bd) if type(_bd).__name__ == 'list' else 0
        _v, _rows, _e = _call(_fs)
        _shown = _bd[_at:] if type(_bd).__name__ == 'list' else []
        _line = _call(_fs.__globals__.get('get_farewell'))[0]
        assert not (_e is None and _shown == [_line]), (
            'Your line runs, and the board shows the line. But `show_on_ley_board()` does not get a variable that '
            'holds what `get_farewell()` returns. The campaign checks for that stored variable.')
        assert False, ('`present_farewell()` hands `get_farewell()` straight to the board: no variable holds the '
                       'result first.')
    _typed = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Constant']
    assert not _typed, '`present_farewell()` stores typed words, not the result of `get_farewell()`.'
    _only = all(type(_s).__name__ == 'Pass' or (type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Constant')
                for _s in _d.body)
    assert not _only, '`present_farewell()` still holds only `pass`.'
    assert False, 'No variable inside `present_farewell()` holds the result of `get_farewell()`.'
'''

_FW_PASS = r'''
_fs, _m = _find('present_farewell')
assert _fs, _m
_G = _fs.__globals__
_board = _G['_board']
_what = 'called `present_farewell()`'
_at = len(_board)
_v, _rows, _e = _call(_fs)
assert _e is None, 'Calling `present_farewell()` stopped Python: ' + _err(_e) + '.' + _ev(_what)
_shown = _board[_at:]
if not _shown:
    assert not _rows, '`present_farewell()` printed a line, but nothing reached the board.' + _ev(_what)
    assert not (_v is not None and _v == _call(_G.get('get_farewell'))[0]), (
        'The function returns the line, so it goes back to the caller and never reaches the ley board.' + _ev(_what))
    assert False, '`present_farewell()` put nothing on the board.' + _ev(_what)
assert len(_shown) == 1, '`present_farewell()` put ' + str(len(_shown)) + ' things on the board.' + _ev(_what)
assert type(_shown[0]).__name__ != 'function', ('The board was handed the function `' + _shown[0].__name__
                                                + '` itself, not its words.' + _ev(_what))
_real = _G.get('get_farewell')
_want = _call(_real)[0]
assert _shown[0] == _want, 'The board showed other words than `get_farewell()` returns.' + _ev(_what)
_said = 'made `get_farewell()` return other words'
_G['get_farewell'] = lambda: 'A grumpy moth says goodbye.'
try:
    _at = len(_board)
    _v, _rows, _e = _call(_fs)
finally:
    _G['get_farewell'] = _real
assert _e is None, 'With other words from `get_farewell()`, Python stopped: ' + _err(_e) + '.' + _ev(_said)
_shown = _board[_at:]
assert _shown and _shown[0] == 'A grumpy moth says goodbye.', (
    'When `get_farewell()` returned other words, the board still showed the old ones.' + _ev(_said))
_d = _defs()['present_farewell']
_stored = _from_call(_d, 'get_farewell')
_more = True
while _more:
    # a variable copied from the stored one (`message = farewell`) holds the result too
    _more = False
    for _n in _ast.walk(_d):
        if type(_n).__name__ == 'Assign' and type(_n.value).__name__ == 'Name' and _n.value.id in _stored:
            for _x in _made_by(_n):
                if _x not in _stored:
                    _stored.append(_x)
                    _more = True
_args = [_a for _c in _calls_in([_d], 'show_on_ley_board') for _a in list(_c.args) + [_k.value for _k in _c.keywords]]
if not [_x for _a in _args for _x in _ast.walk(_a) if type(_x).__name__ == 'Name' and _x.id in _stored]:
    # The board did show the line (both runs above), so the STO message says so first, as form A's does.
    assert not [_a for _a in _args if _is_call(_a, 'get_farewell')], (
        'Your line runs, and the board shows the line. But the board was handed a new call of `get_farewell()`, '
        'not the variable that holds the result.')
    assert False, ('Your line runs, and the board shows the line. But `show_on_ley_board()` does not get a variable '
                   'that holds what `get_farewell()` returns. The campaign checks for that stored variable.')
_u = _uncalled()
assert not _u, _u
'''

PRESENT_FAREWELL = dict(
    id="present-farewell",
    title="Store, then pass it on",
    martu=(
        "`get_farewell()` hands back a tidy line. `present_farewell()` must put that line on the Ley board.\n"
        "Campaign style again: the numbered comments say what to do. My check calls `present_farewell()` with other "
        "words, only inside the check.\n" + _STUCK
    ),
    setup=BOARD_SETUP,
    names=["get_farewell", "present_farewell", "show_on_ley_board"],
    support="none",
    explainer="lean",
    starter=FAREWELL_STARTER,
    checkpoints=[
        dict(
            id="store-the-farewell",
            text="Finish `present_farewell()`: store the result of `get_farewell()` in a variable.",
            dictated=False,
            hints=[
                "Look at comment 1, inside `present_farewell()`, where `pass` is.",
                "A variable can hold what a function hands back, if the function is called.",
                "Any variable name works. The call needs its brackets.",
            ],
            checks=[check("the farewell is stored in a variable", _FW_STORE, orig=FAREWELL_DEF)],
        ),
        dict(
            id="pass-it-to-the-board",
            text="Pass that variable to `show_on_ley_board()`.",
            dictated=False,
            hints=[
                "Look at comment 2: the next line, inside the function too.",
                "Whatever is inside a call's brackets is handed to it.",
                "Hand over the variable itself, not a new call and not typed words.",
            ],
            checks=[check("present_farewell shows the line on the board", _FW_PASS)],
            pass_line="Mar'tu: Stored, then passed on. The board says it.",
        ),
    ],
    solution=FAREWELL_SOLUTION,
    partials=[_farewell(FW_STORE)],
    wrong_answers=[
        dict(why="the starter (pass)", code=FAREWELL_STARTER, fails_at=1, message_contains="only `pass`"),
        dict(why="no store: the call passed straight on (STO: the board shows the line, so that is said first)",
             code=_farewell("    show_on_ley_board(get_farewell())\n"), fails_at=1,
             message_contains="Your line runs, and the board shows the line. But `show_on_ley_board()` does not get"),
        dict(why="no store, and the line handed straight on twice (the board does not show it once)",
             code=_farewell("    show_on_ley_board(get_farewell())\n    show_on_ley_board(get_farewell())\n"),
             fails_at=1, message_contains="straight to the board"),
        dict(why="no () on the helper: the function stored, not its line",
             code=_farewell("    farewell = get_farewell\n" + FW_PASS), fails_at=1, message_contains="nothing calls it"),
        dict(why="a typed line stored instead of the result (CMB)",
             code=_farewell('    farewell = "Watch the arc, friends."\n' + FW_PASS), fails_at=1,
             message_contains="typed words"),
        dict(why="stored, then typed words passed to the board (CMB: the swap shows it)",
             code=_farewell(FW_STORE + '    show_on_ley_board("Watch the arc, friends.")\n'), fails_at=2,
             message_contains="still showed the old ones"),
        dict(why="print instead of handing it to the board", code=_farewell(FW_STORE + "    print(farewell)\n"),
             fails_at=2, message_contains="nothing reached the board"),
        dict(why="stored, then returned instead of passed on", code=_farewell(FW_STORE + "    return farewell\n"),
             fails_at=2, message_contains="goes back to the caller and never reaches the ley board"),
        dict(why="stored, then nothing done with it", code=_farewell(FW_STORE), fails_at=2,
             message_contains="put nothing on the board"),
        dict(why="stored at the left edge, outside the function",
             code=_farewell("    pass\n", tail="\n\nfarewell = get_farewell()\nshow_on_ley_board(farewell)\n"
                                                "present_farewell()\n"),
             fails_at=1, message_contains="outside `present_farewell()`"),
        dict(why="the store line reversed (cannot assign to a call)",
             code=_farewell("    get_farewell() = farewell\n" + FW_PASS), fails_at=0,
             message_contains="cannot assign to function call"),
        dict(why="the finished helper edited (a helper you were told to leave alone)",
             code=_farewell(FW_STORE + FW_PASS, helper=FAREWELL_DEF.replace("    line = line.lower()\n", "")),
             fails_at=1, message_contains="marked finished"),
        dict(why="the variable called like a function: farewell()",
             code=_farewell(FW_STORE + "    show_on_ley_board(farewell())\n"), fails_at=0,
             message_contains="'str' object is not callable"),
        dict(why="the pass-on line at the left edge (a missing indent: farewell is not defined there)",
             code=_farewell(FW_STORE, tail="show_on_ley_board(farewell)\n\n\npresent_farewell()\n"), fails_at=0,
             message_contains="name 'farewell' is not defined"),
        dict(why="stored, then a second call handed over instead of the variable",
             code=_farewell(FW_STORE + "    show_on_ley_board(get_farewell())\n"), fails_at=2,
             message_contains="Your line runs, and the board shows the line. But the board was handed a new call"),
        dict(why="stored, then a variable made at the left edge handed over (CMB: the swap shows it)",
             code=_farewell(FW_STORE + "    show_on_ley_board(line)\n",
                            tail="\n\nline = get_farewell()\npresent_farewell()\n"), fails_at=2,
             message_contains="still showed the old ones"),
        dict(why="the last line left without () (calling vs naming): the board stays empty in the student's own run",
             code=_farewell(FW_STORE + FW_PASS, tail="\n\npresent_farewell\n"), fails_at=2,
             message_contains="no brackets after it"),
    ],
    notes=_rc(3, "b", "chain-methods,store-then-pass", "store-then-pass", "program-dialogue-prompt,mana-bars",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C2, item 3b (form A: get_warning / present_warning). Item 3a (chain-methods) is quiz Q2, with other words, so "
    "running this task first gives nothing away there. CP1 STO + KEEP: the finished `get_farewell` is unchanged (AST "
    "compare), and a variable inside `present_farewell` holds the result of a call to it (no store, no `()`, a typed "
    "line, the store at the left edge and `pass` left are each named). A copy of the stored variable (`message = "
    "farewell`) counts as the stored variable, and so does the variable inside a call (`str(farewell)`). CP2 CALL + CMB: the check calls "
    "`present_farewell()` and reads the board recorder (setup), then swaps `get_farewell` for one that returns 'A "
    "grumpy moth says goodbye.': the board must follow, and the call must hand over the stored variable. The STO "
    "messages use form A's wording when the board does show the line ('Your line runs, and the board shows the "
    "line. But ...'; CP1 runs the function once, privately, to know). Stored then returned has its own message "
    "('The function returns the line, so it goes back to the caller and never reaches the ley board.'), apart "
    "from 'put nothing on the board'. Fails on (spec): a typed line -> CMB; no store -> STO; no `()` -> CALL. "
    + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C3 (item 5b) mend the reply: quote-text in an elif chain (5a, the trace, is quiz Q5). CMB over every option.
# ---------------------------------------------------------------------------------------------

REPLIES = [
    ("option 1", "Oogrish: Steady, now."),
    ("option 2", "Gearshift: Visor dims."),
    ("option 3", "Bomb Shell: Shield up."),
    ("option 4", "Lucky: Fine. I'm in."),
]


def _replies(line5="elif choice == option 2:", line3='if choice == "option 1":', line7='elif choice == "option 3":',
             body5='    print("Gearshift: Visor dims.")'):
    return (
        'choice = "option 2"\n'
        "\n"
        f"{line3}\n"
        '    print("Oogrish: Steady, now.")\n'
        f"{line5}\n"
        f"{body5}\n"
        f"{line7}\n"
        '    print("Bomb Shell: Shield up.")\n'
        "else:\n"
        "    print(\"Lucky: Fine. I'm in.\")\n"
    )


REPLY_STARTER = _replies()
REPLY_SOLUTION = _replies('elif choice == "option 2":')

_REPLY = r'''
_RUNS = __RUNS__
_LINES = [_l for _o, _l in _RUNS]
_OPTS = [_o for _o, _l in _RUNS]
_near = []
for _n in _ast.walk(_tree):
    if type(_n).__name__ == 'Compare':
        for _x in [_n.left] + list(_n.comparators):
            if (type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'str' and _x.value not in _OPTS
                    and _x.value.lower().replace(' ', '') in [_o.replace(' ', '') for _o in _OPTS]):
                _near.append(_n.lineno)


def _who(_l):
    return _l.split(':')[0]


for _c, _want in [_RUNS[1], _RUNS[0], _RUNS[2], _RUNS[3]]:
    _ns, _ls, _e, _miss = _rerun([('choice', 'choice = ' + repr(_c))])
    assert not _miss, _gone('choice')
    _said = 'set `choice = "' + _c + '"`'
    _with = 'With `choice = "' + _c + '"`, '
    assert _e is None, _with + 'Python stopped: ' + _err(_e) + '.' + _ev(_said)
    _got = [_l for _l in _ls if _l in _LINES]
    if _got == [_want]:
        continue
    assert not _near, ('Line ' + str(_near[0]) + ' compares `choice` with a text that differs from an option only in '
                       'its capitals or spaces.' + _ev(_said, _who(_want) + "'s reply did not print"))
    assert _got, _with + 'none of the four replies printed.' + _ev(_said)
    assert len(_got) == 1, _with + str(len(_got)) + ' replies printed.' + _ev(_said)
    assert False, _with + _who(_got[0]) + "'s reply printed, not " + _who(_want) + "'s." + _ev(_said)
'''

MEND_THE_REPLY = dict(
    id="mend-the-reply",
    title="Mend the reply",
    martu=(
        "Four options, four replies, like the campaign's dialogue boxes. Python stops before anyone speaks.\n"
        "My check tries every option, only inside the check.\n" + _STUCK
    ),
    names=["choice"],
    support="none",
    explainer="lean",
    starter=REPLY_STARTER,
    checkpoints=[
        dict(
            id="mend-line-5",
            text="Mend line 5, so each option gets its own reply.",
            dictated=False,
            hints=[
                "Run it, and read the last line of what Python says. It names line 5.",
                "Compare line 5 with the lines above and below it, mark by mark.",
                "Line 5 compares `choice` with something. What kind of value is `choice`?",
            ],
            checks=[check("each option gets its own reply", _REPLY, runs=REPLIES)],
            pass_line="Gearshift: Visor dims. Option 2 heard.",
        ),
    ],
    solution=REPLY_SOLUTION,
    wrong_answers=[
        dict(why="the starter: unquoted text after == (SyntaxError)", code=REPLY_STARTER, fails_at=0,
             message_contains="invalid syntax"),
        dict(why="= for == on line 5", code=_replies('elif choice = "option 2":'), fails_at=0,
             message_contains="Maybe you meant '=='"),
        dict(why="a capital letter in the text (STREXACT)", code=_replies('elif choice == "Option 2":'), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="the space left out (STREXACT)", code=_replies('elif choice == "option2":'), fails_at=1,
             message_contains="capitals or spaces"),
        dict(why="a missing colon", code=_replies('elif choice == "option 2"'), fails_at=0,
             message_contains="expected ':'"),
        dict(why="the test is only the text (always True)", code=_replies('elif "option 2":'), fails_at=1,
             message_contains="Gearshift's reply printed, not Bomb Shell's"),
        dict(why="a name for the text: option_2 (NameError)", code=_replies("elif choice == option_2:"), fails_at=0,
             message_contains="name 'option_2' is not defined"),
        dict(why="if for elif on line 5 (two replies for option 1)", code=_replies('if choice == "option 2":'),
             fails_at=1, message_contains="2 replies printed"),
        dict(why="the chain replaced by one typed print (CMB)", code='choice = "option 2"\n\nprint("Gearshift: Visor dims.")\n',
             fails_at=1, message_contains="Gearshift's reply printed, not Oogrish's"),
        dict(why="the reply under line 5 not indented", code=_replies('elif choice == "option 2":',
                                                                     body5='print("Gearshift: Visor dims.")'),
             fails_at=0, message_contains="expected an indented block"),
    ],
    notes=_rc(5, "b", "elif-chain,quote-text", "quote-text,elif-chain", "program-dialogue-options",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C3, item 5b (form A mends `option 3`; form B mends `option 2`, and Q5 traces `option 3`, so no line repeats). "
    "The starter is the campaign's four-option shape with one bare text. CMB: the check reruns the program with "
    "`choice` set to each option (option 2 first), and exactly that option's reply must print, alone. STREXACT: a "
    "compared text that differs from an option only in capitals or spaces is named. Fails on (spec): left unquoted -> "
    "crash (the explainer's 'two bare words after ==' row). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C4 (items 6a-6c) read and write the sheets: dict-read, dict-nested, dict-write, dict-key-from-variable.
# Item 6d (dict-in) is quiz Q6. CMB and KEY.
# ---------------------------------------------------------------------------------------------

SHEET = (
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "mana": 17,\n'
    '    "max_mana": 24,\n'
    '    "abilities": {\n'
    '        "dexterity": 6,\n'
    '        "wisdom": 8,\n'
    "    },\n"
    "}\n"
)


def _sheets(mana="mana_now = 0", dex="dex_now = 0", store="", book='book = {"Glimmer": {"mana_cost": 2}}'):
    return (
        SHEET + "\n"
        "# 1. Make mana_now hold Bomb Shell's\n"
        "#    mana, read from the sheet.\n"
        + mana + "\n"
        "\n"
        "# 2. Make dex_now hold Bomb Shell's\n"
        "#    dexterity, read from the sheet.\n"
        + dex + "\n"
        "\n"
        + book + "\n"
        'ward_name = "Teal Wall"\n'
        'ward = {"mana_cost": 4}\n'
        "# 3. Store ward in book, using\n"
        "#    ward_name as the key.\n"
        + store + "\n"
        "\n"
        "print(mana_now, dex_now)\n"
        "print(book)\n"
    )


MANA_READ = 'mana_now = bomb_shell["mana"]'
DEX_READ = 'dex_now = bomb_shell["abilities"]["dexterity"]'
BOOK_WRITE = "book[ward_name] = ward"
SHEETS_STARTER = _sheets()
SHEETS_SOLUTION = _sheets(MANA_READ, DEX_READ, BOOK_WRITE)
BRAKKA_SHEET = {"name": "Brakka", "mana": 11, "max_mana": 20, "abilities": {"dexterity": 9, "wisdom": 5}}
_OTHER_SHEET = [("bomb_shell", "bomb_shell = " + repr(BRAKKA_SHEET))]
_SHEET_SAID = "another sheet in `bomb_shell` (Brakka: 11 of 20 mana, dexterity 9)"
_SHEET_WHAT = "put another sheet in `bomb_shell`"

_FOLLOW = r'''
_T, _WANT, _PLACE = __TARGET__, __WANT__, __PLACE__
assert _T in _g, 'No variable called `' + _T + '` is left in the code.'
_v = _g[_T]
if not (type(_v).__name__ == type(_WANT).__name__ and _v == _WANT):
    _t = type(_v).__name__
    assert _t != 'str', '`' + _T + '` holds text, not a number.'
    assert _t != 'dict', '`' + _T + '` holds a whole dictionary, not a number.'
    _start = [_n for _n in _top() if type(_n).__name__ == 'Assign' and _T in _made_by(_n)
              and type(_n.value).__name__ == 'Constant' and _n.value.value == _PLACE]
    assert not (_v == _PLACE and _start), '`' + _T + '` still holds the starter' + chr(39) + 's ' + str(_PLACE) + '.'
    for _k, _msg in __RULES__:
        assert _v != _k, _msg
    assert False, '`' + _T + '` holds ' + _show(_v) + ', not ' + _show(_WANT) + '.'
for _changes, _want, _said, _what in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _got = _ns.get(_T)
    if _got != _want:
        # CMB, in form A's words: the value was typed, and the other sheet did not change it.
        assert _got != _WANT, ('`' + _T + '` holds a typed ' + str(_WANT) + ". Mar'tu's check " + _what + ', and `'
                               + _T + '` still said ' + str(_got) + '.')
        assert False, 'With ' + _said + ', `' + _T + '` held ' + _show(_got) + ', not ' + _show(_want) + '.' + _ev(_what)
'''

_BOOK = r'''
_b = _g.get('book')
assert type(_b).__name__ == 'dict', '`book` is not a dictionary any more.'
assert 'Glimmer' in _b, '`book` lost its Glimmer page.'
_wn = _g.get('ward_name')
assert not ('ward_name' in _b and _wn != 'ward_name'), (
    '`book` got a page under the key `"ward_name"`: those exact letters, not the name the variable holds.')
assert type(_wn).__name__ == 'str' and _wn in _b, '`book` has no page under the name that `ward_name` holds.'
_p = _b[_wn]
assert type(_p).__name__ == 'dict', 'The new page holds ' + _show(_p) + ', not the `ward` dictionary.'
for _changes, _cost, _said, _what in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _nb = _ns.get('book')
    assert type(_nb).__name__ == 'dict' and 'Ember Wall' in _nb, (
        'With ' + _said + ', `book` got no Ember Wall page: the key does not follow `ward_name`.' + _ev(_what))
    _np = _nb['Ember Wall']
    assert type(_np).__name__ == 'dict' and _np.get('mana_cost') == _cost, (
        'With ' + _said + ', the Ember Wall page did not hold the new `ward`.' + _ev(_what))
'''

_BOOK_RERUNS = [([("ward_name", 'ward_name = "Ember Wall"'), ("ward", 'ward = {"mana_cost": 9}')], 9,
                 '`ward_name = "Ember Wall"` and `ward = {"mana_cost": 9}`',
                 "set `ward_name` and `ward` to other values")]

READ_AND_WRITE = dict(
    id="read-and-write-the-sheets",
    title="Read and write the sheets",
    martu=(
        "Bomb Shell's stat sheet is a [[dictionary]], with a [[nested dictionary]] inside it. Read two values from "
        "it, then write one page into a book of wards.\n"
        "My check puts other sheets and other pages in, only inside the check.\n" + _STUCK
    ),
    names=["mana_now", "dex_now", "book", "ward_name", "ward"],
    support="none",
    explainer="lean",
    starter=SHEETS_STARTER,
    checkpoints=[
        dict(
            id="read-the-mana",
            text="Make `mana_now` hold Bomb Shell's mana, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 1, and at the sheet's keys.",
                "Square brackets after a dictionary's name read the value under one key.",
                "The key is text, so it keeps its quotes.",
            ],
            checks=[check(
                "mana_now reads the mana from the sheet", _FOLLOW, target="mana_now", want=17, place=0,
                rules=[(24, "`mana_now` holds 24, the sheet's `\"max_mana\"`."),
                       (6, "`mana_now` holds 6, Bomb Shell's dexterity.")],
                reruns=[(_OTHER_SHEET, 11, _SHEET_SAID, _SHEET_WHAT)],
            )],
        ),
        dict(
            id="read-the-dexterity",
            text="Make `dex_now` hold Bomb Shell's dexterity, read from the sheet.",
            dictated=False,
            hints=[
                "Look at comment 2. Where on the sheet is `\"dexterity\"`?",
                "A dictionary inside a dictionary is read one key at a time, outer key first.",
                "Two pairs of square brackets in a row.",
            ],
            checks=[check(
                "dex_now reads the dexterity from inside the abilities", _FOLLOW, target="dex_now", want=6, place=0,
                rules=[(8, "`dex_now` holds 8, Bomb Shell's wisdom."),
                       (17, "`dex_now` holds 17, Bomb Shell's mana.")],
                reruns=[(_OTHER_SHEET, 9, _SHEET_SAID, _SHEET_WHAT)],
            )],
        ),
        dict(
            id="store-the-ward",
            text="Store `ward` in `book`, using `ward_name` as the key.",
            dictated=False,
            hints=[
                "Look at comment 3, under the three lines about the book.",
                "Square brackets on the left of `=` write a page into a dictionary.",
                QUOTES_RULE,
            ],
            checks=[check("the ward is stored under the name in ward_name", _BOOK, reruns=_BOOK_RERUNS)],
            pass_line="Bomb Shell: Teal Wall. Logged. Shield up.",
        ),
    ],
    solution=SHEETS_SOLUTION,
    partials=[_sheets(MANA_READ), _sheets(MANA_READ, DEX_READ)],
    wrong_answers=[
        dict(why="the starter (0 placeholders)", code=SHEETS_STARTER, fails_at=1, message_contains="still holds"),
        dict(why="CP1 a typed 17 (CMB)", code=_sheets("mana_now = 17"), fails_at=1,
             message_contains="`mana_now` holds a typed 17. Mar'tu's check put another sheet in `bomb_shell`, and "
                              "`mana_now` still said 17."),
        dict(why="CP1 max_mana read instead of mana", code=_sheets('mana_now = bomb_shell["max_mana"]'), fails_at=1,
             message_contains="max_mana"),
        dict(why="CP1 the key with a capital (KeyError)", code=_sheets('mana_now = bomb_shell["Mana"]'), fails_at=0,
             message_contains="KeyError: 'Mana'"),
        dict(why="CP1 the key without quotes (NameError)", code=_sheets("mana_now = bomb_shell[mana]"), fails_at=0,
             message_contains="name 'mana' is not defined"),
        dict(why="CP1 a dot for brackets (AttributeError)", code=_sheets("mana_now = bomb_shell.mana"), fails_at=0,
             message_contains="has no attribute 'mana'"),
        dict(why="CP1 the read in quotes (text)", code=_sheets("mana_now = 'bomb_shell[\"mana\"]'"), fails_at=1,
             message_contains="holds text"),
        dict(why="CP2 a skipped nesting level (KeyError)", code=_sheets(MANA_READ, 'dex_now = bomb_shell["dexterity"]'),
             fails_at=0, message_contains="KeyError: 'dexterity'"),
        dict(why="CP2 only the outer key: the whole abilities dictionary",
             code=_sheets(MANA_READ, 'dex_now = bomb_shell["abilities"]'), fails_at=2,
             message_contains="whole dictionary"),
        dict(why="CP2 a typed 6 (CMB)", code=_sheets(MANA_READ, "dex_now = 6"), fails_at=2,
             message_contains="`dex_now` holds a typed 6. Mar'tu's check put another sheet in `bomb_shell`"),
        dict(why="CP2 the wrong inner key", code=_sheets(MANA_READ, 'dex_now = bomb_shell["abilities"]["wisdom"]'),
             fails_at=2, message_contains="wisdom"),
        dict(why="CP3 the variable's name quoted as the key (KEY)", code=_sheets(MANA_READ, DEX_READ,
                                                                              'book["ward_name"] = ward'),
             fails_at=3, message_contains='"ward_name"'),
        dict(why="CP3 a typed key (CMB: the rerun's name is not there)",
             code=_sheets(MANA_READ, DEX_READ, 'book["Teal Wall"] = ward'), fails_at=3,
             message_contains="does not follow `ward_name`"),
        dict(why="CP3 the book rebuilt: the first page lost", code=_sheets(MANA_READ, DEX_READ,
                                                                        "book = {ward_name: ward}"),
             fails_at=3, message_contains="lost its Glimmer page"),
        dict(why="CP3 key and value swapped (TypeError: a dict as a key)",
             code=_sheets(MANA_READ, DEX_READ, "book[ward] = ward_name"), fails_at=0,
             message_contains="unhashable type: 'dict'"),
        dict(why="CP3 == for = (the comparison reads a page that is not there: the explainer's KeyError row)",
             code=_sheets(MANA_READ, DEX_READ, "book[ward_name] == ward"), fails_at=0,
             message_contains="KeyError: 'Teal Wall'"),
        dict(why="CP3 the variable's name in quotes as the value", code=_sheets(MANA_READ, DEX_READ,
                                                                             'book[ward_name] = "ward"'),
             fails_at=3, message_contains="not the `ward` dictionary"),
        dict(why="CP3 a typed copy of the page (CMB: the rerun's page is not there)",
             code=_sheets(MANA_READ, DEX_READ, 'book[ward_name] = {"mana_cost": 4}'), fails_at=3,
             message_contains="did not hold the new `ward`"),
        dict(why="CP3 .append on a dictionary (AttributeError)", code=_sheets(MANA_READ, DEX_READ, "book.append(ward)"),
             fails_at=0, message_contains="has no attribute 'append'"),
    ],
    notes=_rc(6, "a-c", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable",
              "dict-read,dict-nested,dict-write,dict-key-from-variable", "spell-book,hold-the-barrier",
              starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C4, items 6a-6c (form A: `hero[\"mana\"]`, `hero[\"abilities\"][\"wisdom\"]`, `book[spell_name] = spell`). Item 6d "
    "(dict-in) is quiz Q6. Bomb Shell's real values (dexterity 6, wisdom 8, max mana 24), with 17 mana left so "
    "`\"max_mana\"` read for the mana shows in the student's own run. CP1 and CP2 CMB: the program reruns with Brakka's "
    "sheet slipped in after the student's `bomb_shell` line (11 of 20 mana, dexterity 9): a typed number cannot follow. "
    "CP3 KEY + CMB: the page must be under the name `ward_name` holds, the Glimmer page must stay, and a rerun with "
    "`ward_name = \"Ember Wall\"` and another `ward` must store that page (a book of wards: `ward` is the page and "
    "`ward_name` its name, the same meaning as in the mini-boss). A typed read takes form A's CMB wording ('`mana_now` "
    "holds a typed 17. Mar'tu's check put another sheet in `bomb_shell`, and `mana_now` still said 17.'). Fails on "
    "(spec): `bomb_shell[\"dexterity\"]` "
    "(the skipped level, KeyError); `book[\"ward_name\"]`. The Ready rule's 'item 6 at >= 3 of 4 parts' counts CP1-CP3 "
    "here and Q6 (site scoring work). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C5 (item 7b) mend the bar: repeat-string, the parentheses (7a is quiz Q7). CMB with other mana.
# ---------------------------------------------------------------------------------------------


def _bar(empty='empty = "░" * max_mana - mana', full='full = "█" * mana'):
    return (
        "mana = 4\n"
        "max_mana = 9\n"
        "\n"
        f"{full}\n"
        f"{empty}\n"
        'print("[" + full + empty + "]")\n'
    )


BAR_STARTER = _bar()
BAR_SOLUTION = _bar('empty = "░" * (max_mana - mana)')

_BAR = r'''
for _changes, _m, _mx, _said, _what in __RUNS__:
    if _changes:
        _ns, _ls, _e, _miss = _rerun(_changes)
        assert not _miss, _gone(_miss[0])
        assert _e is None, _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
        _lead, _tail = _said + ', ', _ev(_what)
    else:
        _ns, _ls, _lead, _tail = _g, _lines(), '', ''
        if type(_g.get('mana')).__name__ == 'int' and type(_g.get('max_mana')).__name__ == 'int':
            _m, _mx = _g['mana'], _g['max_mana']
    _em, _fu = _ns.get('empty'), _ns.get('full')
    assert type(_em).__name__ == 'str', _lead + '`empty` holds ' + _show(_em) + ', not blocks.' + _tail
    assert _em == '░' * len(_em), _lead + '`empty` holds other marks, not only `░` blocks.' + _tail
    assert len(_em) == max(0, _mx - _m), (_lead + '`empty` held ' + str(len(_em)) + ' blocks, not '
                                          + str(max(0, _mx - _m)) + '.' + _tail)
    assert type(_fu).__name__ == 'str' and _fu == '█' * _m, (
        _lead + '`full` did not hold ' + str(_m) + ' `█` blocks.' + _tail)
    assert [_l for _l in _ls if _fu + _em in _l], ((_lead + 'the' if _lead else 'The')
                                                   + ' bar line did not show `full`, then `empty`.' + _tail)
'''

_BAR_RUNS = [
    ((), 4, 9, "", ""),
    ([("mana", "mana = 6"), ("max_mana", "max_mana = 8")], 6, 8, "With `mana = 6` and `max_mana = 8`",
     "tried `mana = 6` and `max_mana = 8`"),
    ([("mana", "mana = 1"), ("max_mana", "max_mana = 4")], 1, 4, "With `mana = 1` and `max_mana = 4`",
     "tried `mana = 1` and `max_mana = 4`"),
]

MEND_THE_BAR = dict(
    id="mend-the-bar",
    title="Mend the bar",
    martu=(
        "A mana bar: a `█` for each point of mana left, a `░` for each point used. The blocks are typed for you.\n"
        "Python stops on line 5. My check tries other mana, only inside the check.\n" + _STUCK
    ),
    names=["empty", "full", "mana", "max_mana"],
    support="none",
    explainer="lean",
    starter=BAR_STARTER,
    checkpoints=[
        dict(
            id="mend-line-5",
            text="Mend line 5, so `empty` holds one `░` for each point of mana used.",
            dictated=False,
            hints=[
                "Run it, and read the last line of what Python says.",
                "Python does `*` before `-`, so it works out the blocks first.",
                "Which part of line 5 should be worked out first?",
            ],
            checks=[check("empty holds a block for each point used", _BAR, runs=_BAR_RUNS)],
            pass_line="Mar'tu: Four left, five used. The bar tells the truth.",
        ),
    ],
    solution=BAR_SOLUTION,
    wrong_answers=[
        dict(why="the starter: no parentheses (TypeError)", code=BAR_STARTER, fails_at=0,
             message_contains="unsupported operand type(s) for -: 'str' and 'int'"),
        dict(why="a typed count (CMB)", code=_bar('empty = "░" * 5'), fails_at=1, message_contains="held 5 blocks"),
        dict(why="typed blocks (CMB)", code=_bar('empty = "░░░░░"'), fails_at=1, message_contains="held 5 blocks"),
        dict(why="the parentheses right, the numbers typed inside them (CMB: the rerun shows it)",
             code=_bar('empty = "░" * (9 - 4)'), fails_at=1, message_contains="held 5 blocks, not 2"),
        dict(why="only the max: the subtraction dropped", code=_bar('empty = "░" * max_mana'), fails_at=1,
             message_contains="held 9 blocks"),
        dict(why="the subtraction reversed (no blocks)", code=_bar('empty = "░" * (mana - max_mana)'), fails_at=1,
             message_contains="held 0 blocks"),
        dict(why="blocks minus blocks (TypeError)", code=_bar('empty = "░" * max_mana - "░" * mana'), fails_at=0,
             message_contains="for -: 'str' and 'str'"),
        dict(why="brackets around the wrong part", code=_bar('empty = ("░" * max_mana) - mana'), fails_at=0,
             message_contains="unsupported operand"),
        dict(why="the sum in quotes (TypeError: text times text)", code=_bar('empty = "░" * "max_mana - mana"'),
             fails_at=0, message_contains="can't multiply sequence"),
        dict(why="full typed as well (CMB)", code=_bar('empty = "░" * (max_mana - mana)', full='full = "████"'),
             fails_at=1, message_contains="`full` did not hold 6"),
    ],
    notes=_rc(7, "b", "repeat-string", "repeat-string", "mana-bars", starter_level="S4", path="READY", dictates="",
              foreign_names="") + "\n"
    "C5, item 7b (form A mends `\"░\" * 10 - 3`). Form B uses the mana-bars variables, so the task can be rerun with "
    "other values: CMB with mana 6 of 8 and 1 of 4, and `full` and the printed bar must follow. The first run "
    "follows the student's own `mana` and `max_mana`, so a changed number is not marked wrong; `(9 - 4)` fails the "
    "reruns. Fails on (spec): no "
    "parentheses -> the TypeError row ('Put the subtraction in parentheses' is the full explainer's; lean names the "
    "line). Typed counts and typed blocks fail the reruns. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C6 (item 8b) throw the die: randint-param (8a, randint, is quiz Q8). RND.
# ---------------------------------------------------------------------------------------------


def _die_code(body="    return 1\n", tail="\n\nprint(throw_die(8))\n"):
    return "import random\n\n\ndef throw_die(die_size):\n" + body + tail


DIE_STARTER = _die_code()
DIE_SOLUTION = _die_code("    return random.randint(1, die_size)\n")

_ROLL = r'''
_f, _m = _find('throw_die')
assert _f, _m
_ps = _params(_f)
assert _ps == ['die_size'], 'The `def` line of `throw_die` has ' + _names(_ps) + ', and the starter has `die_size`.'
_d = _defs()['throw_die']
_inner = [_n for _n in _ast.walk(_d) if _n is not _d and 'die_size' in _made_by(_n)]
_typed = [_c for _c in _ast.walk(_d) if type(_c).__name__ == 'Call' and type(_c.func).__name__ == 'Attribute'
          and _c.func.attr == 'randint' and len(_c.args) == 2 and type(_c.args[1]).__name__ == 'Constant']
for _size in (12, 4):
    _c = '`throw_die(' + str(_size) + ')`'
    _what = 'called ' + _c + ' with a pretend die that rolls one below its top face'
    _val, _rows, _e, _log = _rolled(_f, (_size,))
    assert _e is None, _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    assert _log, _c + ' returned ' + _show(_val) + ' and rolled no die.' + _ev(_what)
    assert len(_log) == 1, _c + ' rolled ' + str(len(_log)) + ' times.' + _ev(_what)
    _a, _b = _log[0]
    if (_a, _b) != (1, _size):
        _span = _c + ' rolled from ' + str(_a) + ' to ' + str(_b)
        assert not _inner, _span + ': a line inside the function sets `die_size`.' + _ev(_what)
        assert not _typed, _span + ': the top face is a typed number.' + _ev(_what)
        assert _a != 0, _span + ': a die has no 0 face.' + _ev(_what)
        assert _b != _size + 1, _span + ': one face too many.' + _ev(_what)
        assert False, _span + '.' + _ev(_what)
    if _val != _b - 1:
        assert not (_val is None and _rows), (_c + ' printed the roll and returned `None`, Python' + chr(39)
                                              + 's word for nothing.' + _ev(_what))
        assert _val is not None, _c + ' rolled, then returned `None`, Python' + chr(39) + 's word for nothing.' + _ev(_what)
        assert False, _c + ' rolled ' + str(_b - 1) + ' but returned ' + _show(_val) + '.' + _ev(_what)
_u = _uncalled()
assert not _u, _u
'''

THROW_DIE = dict(
    id="throw-the-die",
    title="Roll the die",
    martu=(
        "Campaign style: `throw_die(die_size)` must roll a die with `die_size` faces. Right now it always says 1.\n"
        "My check rolls other dice with a pretend die, only inside the check.\n" + _STUCK
    ),
    names=["throw_die", "die_size"],
    support="none",
    explainer="lean",
    starter=DIE_STARTER,
    checkpoints=[
        dict(
            id="roll-from-1-to-die-size",
            text="Replace `return 1` with a random whole number from 1 to `die_size`.",
            dictated=False,
            hints=[
                "Look at the `import` line at the top: it brings in the tools for random numbers.",
                "[[randint]] takes the lowest and the highest number, and both can come up.",
                "The highest face is whatever was handed in, so it is the parameter, not a number.",
            ],
            checks=[check("throw_die rolls from 1 to die_size", _ROLL)],
            pass_line="Lucky: Any size die. I'll take the d20, thanks.",
        ),
    ],
    solution=DIE_SOLUTION,
    wrong_answers=[
        dict(why="the starter (return 1)", code=DIE_STARTER, fails_at=1, message_contains="rolled no die"),
        dict(why="a typed d8 (RND: the literal size)", code=_die_code("    return random.randint(1, 8)\n"), fails_at=1,
             message_contains="typed number"),
        dict(why="a typed d6", code=_die_code("    return random.randint(1, 6)\n"), fails_at=1,
             message_contains="typed number"),
        dict(why="the exclusive-range belief: die_size + 1", code=_die_code("    return random.randint(1, die_size + 1)\n"),
             fails_at=1, message_contains="one face too many"),
        dict(why="from 0", code=_die_code("    return random.randint(0, die_size)\n"), fails_at=1,
             message_contains="no 0 face"),
        dict(why="print instead of return", code=_die_code("    print(random.randint(1, die_size))\n"), fails_at=1,
             message_contains="printed the roll and returned `None`"),
        dict(why="rolled, but no return", code=_die_code("    random.randint(1, die_size)\n"), fails_at=1,
             message_contains="returned `None`"),
        dict(why="die_size set inside (the parameter thrown away)",
             code=_die_code("    die_size = 8\n    return random.randint(1, die_size)\n"), fails_at=1,
             message_contains="sets `die_size`"),
        dict(why="the size returned with no roll", code=_die_code("    return die_size\n"), fails_at=1,
             message_contains="rolled no die"),
        dict(why="randint with one value (TypeError)", code=_die_code("    return random.randint(die_size)\n"),
             fails_at=0, message_contains="missing 1 required positional argument"),
        dict(why="randint without random. (NameError)", code=_die_code("    return randint(1, die_size)\n"), fails_at=0,
             message_contains="name 'randint' is not defined"),
        dict(why="the parameter in quotes", code=_die_code('    return random.randint(1, "die_size")\n'), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="the function printed, not called (handing over vs calling: no (8))",
             code=_die_code("    return random.randint(1, die_size)\n", tail="\n\nprint(throw_die)\n"), fails_at=1,
             message_contains="prints the function `throw_die` itself"),
    ],
    notes=_rc(8, "b", "randint,randint-param", "randint-param", "skill-checks", starter_level="S4", path="READY",
              dictates="", foreign_names="") + "\n"
    "C6, item 8b (form A: `roll_die(die_size)`). Item 8a (randint, a d8) is quiz Q8. Campaign-style starter "
    "(`perform_roll`'s `return 1`). RND: the check swaps `random.randint` for a scripted die that records its "
    "arguments and rolls one below the top face, then calls `throw_die(12)` and `throw_die(4)`: one roll, from 1 to "
    "the size handed in, and that roll returned. The pretend die also stands in for a `randint` brought in with "
    "`from random import randint`, and takes `a=` / `b=`, so those right answers pass. The visible call is "
    "`throw_die(8)`, so 12 and 4 are fresh. Fails on "
    "(spec): `randint(1, 6)` -> RND; also the typed 8, `die_size + 1` (the exclusive-range belief), 0, print for "
    "return, and a line that sets `die_size` inside. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C7 (item 11) three tracebacks: read-traceback. Each slip in its own function; CALL + CMB with fresh values.
# ---------------------------------------------------------------------------------------------

TB_WARD_BAD = 'def ward_mana(ward):\n    return ward["Mana"]\n'
TB_WARD_GOOD = 'def ward_mana(ward):\n    return ward["mana"]\n'
TB_ORE_BAD = 'def ore_report(ore):\n    print("Ore left: " + ore)\n'
TB_ORE_GOOD = 'def ore_report(ore):\n    print("Ore left: " + str(ore))\n'
TB_TOTAL_HEAD = "def total_cost(costs):\n    total = 0\n    for cost in costs:\n        total = total + cost\n"
TB_TOTAL_BAD = TB_TOTAL_HEAD + "    return totl\n"
TB_TOTAL_GOOD = TB_TOTAL_HEAD + "    return total\n"
TB_CALLS = (
    'teal = {"name": "Teal", "mana": 4}\n'
    "print(ward_mana(teal))\n"
    "ore_report(12)\n"
    "print(total_cost([3, 5, 2]))\n"
)


def _tb(ward=TB_WARD_BAD, ore=TB_ORE_BAD, total=TB_TOTAL_BAD, calls=TB_CALLS):
    return ward + "\n\n" + ore + "\n\n" + total + "\n\n" + calls


TB_STARTER = _tb()
TB_SOLUTION = _tb(TB_WARD_GOOD, TB_ORE_GOOD, TB_TOTAL_GOOD)

_TB_WARD = r'''
_f, _m = _find('ward_mana')
assert _f, _m
for _w in ({'name': 'Ivo Ward', 'mana': 9}, {'name': 'Moss Ward', 'mana': 2}):
    _c = '`ward_mana` on a ward with ' + str(_w['mana']) + ' mana'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (_w,))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    assert _val == _w['mana'], ('`ward_mana` returned ' + _show(_val) + ' for a ward with ' + str(_w['mana'])
                                + ' mana.' + _ev(_what))
'''

_TB_ORE = r'''
_f, _m = _find('ore_report')
assert _f, _m
for _ore in (30, 7):
    _c = '`ore_report(' + str(_ore) + ')`'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (_ore,))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    assert ('Ore left: ' + str(_ore)) in _rows, _c + ' did not print `Ore left: ' + str(_ore) + '`.' + _ev(_what)
'''

_TB_TOTAL = r'''
_f, _m = _find('total_cost')
assert _f, _m
for _costs, _want in (([6, 1, 4, 2], 13), ([9], 9)):
    _c = '`total_cost(' + str(_costs) + ')`'
    _what = 'called ' + _c
    _val, _rows, _e = _call(_f, (list(_costs),))
    assert _e is None, 'Calling ' + _c + ' stopped Python: ' + _err(_e) + '.' + _ev(_what)
    if _val != _want:
        assert not (_val is None and _rows), (_c + ' printed a number and returned `None`, Python' + chr(39)
                                              + 's word for nothing.' + _ev(_what))
        assert not (len(_costs) > 1 and _val == _costs[-1]), (
            _c + ' returned ' + _show(_val) + ', only the last cost: the total starts again on every pass.' + _ev(_what))
        assert not (len(_costs) > 1 and _val == _costs[0]), (
            _c + ' returned ' + _show(_val) + ', only the first cost: the `return` runs on the first pass of the loop.'
            + _ev(_what))
        assert False, _c + ' returned ' + _show(_val) + ', not `' + str(_want) + '`.' + _ev(_what)
'''

THREE_TRACEBACKS = dict(
    id="three-tracebacks",
    title="Three tracebacks",
    martu=(
        "Three slips, one in each function. Python stops at the first one it meets, every time.\n"
        "Read the [[traceback]]'s last line first, then the line it names. Mend one, then Run again. My check calls "
        "each function with other values, only inside the check.\n" + _STUCK
    ),
    names=["ward_mana", "ore_report", "total_cost"],
    support="none",
    explainer="lean",
    starter=TB_STARTER,
    checkpoints=[
        dict(
            id="first-traceback",
            text="Run it, then mend the line Python names, so `ward_mana` returns a ward's mana.",
            dictated=False,
            hints=[
                "Read the last line of the message first: the kind of error, then what it says.",
                "Then find the line it names, inside one of the functions.",
                "Mend that one line, not the data or the call below it.",
            ],
            checks=[check("ward_mana returns the ward's mana", _TB_WARD)],
            pass_line="Mar'tu: One mended. Python got further, yes?",
        ),
        dict(
            id="second-traceback",
            text="Run again, then mend the next line Python names, so `ore_report` prints the ore, like `Ore left: 12`.",
            dictated=False,
            hints=[
                "Read the new last line. It is a different kind of error now.",
                "It names a line inside another function.",
                "Mend the line itself, so any number handed in works.",
            ],
            checks=[check("ore_report prints the ore left", _TB_ORE)],
        ),
        dict(
            id="third-traceback",
            text="Run again, then mend the last line Python names, so `total_cost` returns the total of every cost.",
            dictated=False,
            hints=[
                "Read the last line once more. Python may suggest a name.",
                "Python matches names letter for letter.",
                "Mend that line so the function hands back its total.",
            ],
            checks=[check("total_cost returns the total of every cost", _TB_TOTAL)],
            pass_line="Mar'tu: Three tracebacks, three mends, and no hints. You read them yourself.",
        ),
    ],
    solution=TB_SOLUTION,
    wrong_answers=[
        dict(why="the starter: the first traceback (KeyError)", code=TB_STARTER, fails_at=0,
             message_contains="KeyError: 'Mana'"),
        dict(why="only the first slip mended: the second traceback (TypeError)", code=_tb(TB_WARD_GOOD), fails_at=0,
             message_contains="can only concatenate str"),
        dict(why="two slips mended: the third traceback (NameError)", code=_tb(TB_WARD_GOOD, TB_ORE_GOOD), fails_at=0,
             message_contains="name 'totl' is not defined"),
        dict(why="CP1 the data mended, not the line (the key renamed in teal)",
             code=_tb(TB_WARD_BAD, TB_ORE_GOOD, TB_TOTAL_GOOD, TB_CALLS.replace('"mana": 4', '"Mana": 4')), fails_at=1,
             message_contains="KeyError: 'Mana'"),
        dict(why="CP1 a typed 4 (CMB)", code=_tb('def ward_mana(ward):\n    return 4\n', TB_ORE_GOOD, TB_TOTAL_GOOD),
             fails_at=1, message_contains="returned `4`"),
        dict(why="CP2 the call mended, not the line: the ore handed over as text",
             code=_tb(TB_WARD_GOOD, TB_ORE_BAD, TB_TOTAL_GOOD, TB_CALLS.replace("ore_report(12)", 'ore_report("12")')),
             fails_at=2, message_contains="can only concatenate str"),
        dict(why="CP2 a typed ore line (CMB)", code=_tb(TB_WARD_GOOD, 'def ore_report(ore):\n    print("Ore left: 12")\n',
                                                        TB_TOTAL_GOOD), fails_at=2, message_contains="did not print"),
        dict(why="CP2 str() around a typed number", code=_tb(TB_WARD_GOOD,
                                                             'def ore_report(ore):\n    print("Ore left: " + str(12))\n',
                                                             TB_TOTAL_GOOD), fails_at=2, message_contains="did not print"),
        dict(why="CP3 the total reset inside the loop", code=_tb(TB_WARD_GOOD, TB_ORE_GOOD, (
            "def total_cost(costs):\n    for cost in costs:\n        total = 0\n        total = total + cost\n"
            "    return total\n")), fails_at=3, message_contains="starts again on every pass"),
        dict(why="CP3 the return indented into the loop (an extra indent: it hands back on the first pass)",
             code=_tb(TB_WARD_GOOD, TB_ORE_GOOD, TB_TOTAL_HEAD + "        return total\n"), fails_at=3,
             message_contains="first pass of the loop"),
        dict(why="CP3 a typed 10 (CMB)", code=_tb(TB_WARD_GOOD, TB_ORE_GOOD, TB_TOTAL_HEAD + "    return 10\n"),
             fails_at=3, message_contains="returned `10`"),
        dict(why="CP3 print instead of return", code=_tb(TB_WARD_GOOD, TB_ORE_GOOD, TB_TOTAL_HEAD + "    print(total)\n"),
             fails_at=3, message_contains="printed a number and returned `None`"),
        dict(why="the calls deleted to stop the tracebacks (the slips are still there)",
             code=_tb(calls=""), fails_at=1, message_contains="KeyError: 'Mana'"),
    ],
    notes=_rc(11, "code", "read-traceback", "read-traceback", "every part", starter_level="S4", path="READY",
              dictates="", foreign_names="") + "\n"
    "C7, item 11 (form A: KeyError 'dexterity', the str + int TypeError, NameError 'mana_cots'). Form B: KeyError "
    "'Mana' (a capital), the same TypeError in another line, and NameError 'totl' (a dropped letter). Each slip sits "
    "in its own small function with the calls at the bottom, so every traceback is live, in order, and each "
    "checkpoint calls its function with fresh values (CALL + CMB): a typed 4, a typed ore line, a typed 10, the data "
    "or the call mended instead of the line, and the calls deleted each fail. CP3's loop also catches the reset slip "
    "(`total = 0` moved into the loop). No partials: Python stops at the first slip left, so a program with one slip "
    "mended still crashes at the next, before any check can run. " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C8 (item 12) spend the mana: dict-write, reassign, combine-values. CMB with another cost and start.
# ---------------------------------------------------------------------------------------------

SPEND_HEAD = (
    "oogrish = {\n"
    '    "name": "Oogrish",\n'
    '    "mana": 18,\n'
    "}\n"
    "cost = 5\n"
    "\n"
    '# Spend cost from oogrish["mana"].\n'
)


def _spend(line=""):
    return SPEND_HEAD + line + "\n\nprint(oogrish[\"mana\"])\n"


SPEND_STARTER = _spend()
SPEND_SOLUTION = _spend('oogrish["mana"] = oogrish["mana"] - cost\n')

_SPEND = r'''
_o = _g.get('oogrish')
assert type(_o).__name__ == 'dict', '`oogrish` is not a dictionary any more.'
_m = _o.get('mana')
# The start and the cost as the code gives them (18 and 5 in the starter; a changed number is judged by its own).
_m0, _c0 = 18, _g.get('cost')
for _n in _top():
    if type(_n).__name__ == 'Assign' and 'oogrish' in _made_by(_n) and type(_n.value).__name__ == 'Dict':
        _m0 = dict((_k.value, _v.value) for _k, _v in zip(_n.value.keys, _n.value.values)
                   if type(_k).__name__ == 'Constant' and type(_v).__name__ == 'Constant').get('mana', 18)
        break
_ok = type(_m0).__name__ == 'int' and type(_c0).__name__ == 'int'
_w0 = _m0 - _c0 if _ok else 13
_s0 = str(_m0)
if _m != _w0:
    if _m == _m0:
        assert not [_k for _k in _o if _k not in ('name', 'mana')], (
            '`oogrish["mana"]` is still ' + _s0 + ': the new value went under another key.')
        _cmp = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Compare']
        assert not _cmp, '`oogrish["mana"]` is still ' + _s0 + ': the line with `==` compares, and stores nothing.'
        _bare = [_n for _n in _top() if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp']
        assert not _bare, '`oogrish["mana"]` is still ' + _s0 + ': the subtraction is worked out, then forgotten.'
        _shown = [_c for _c in _calls_in(_top(), 'print') if [_a for _a in _c.args if type(_a).__name__ == 'BinOp']]
        assert not _shown, '`oogrish["mana"]` is still ' + _s0 + ': the new mana is printed, not stored.'
        _box = [_x for _n in _top() if type(_n).__name__ in ('Assign', 'AugAssign')
                and type(_n.value).__name__ == 'BinOp' for _x in _made_by(_n)]
        assert not _box, '`oogrish["mana"]` is still ' + _s0 + ': the new mana went into `' + _box[0] + '`.'
        assert False, '`oogrish["mana"]` is still ' + _s0 + '.'
    assert False, '`oogrish["mana"]` is ' + _show(_m) + ', not `' + str(_w0) + '`.'
for _changes, _want, _said, _what in __RERUNS__:
    _ns, _ls, _e, _miss = _rerun(_changes)
    assert not _miss, _gone(_miss[0])
    assert _e is None, 'With ' + _said + ', Python stopped: ' + _err(_e) + '.' + _ev(_what)
    _no = _ns.get('oogrish')
    _got = _no.get('mana') if type(_no).__name__ == 'dict' else None
    if _got != _want:
        # CMB, in form A's words: the value was typed, and the other sheet and cost did not change it.
        assert _got != _w0, ('`oogrish["mana"]` holds a typed ' + str(_w0) + ". Mar'tu's check " + _what
                             + ', and `oogrish["mana"]` still said ' + str(_got) + '.')
        assert False, ('With ' + _said + ', `oogrish["mana"]` ended at ' + _show(_got) + ', not `' + str(_want) + '`.'
                       + _ev(_what))
'''

_SPEND_RERUNS = [
    ([("oogrish", 'oogrish = {"name": "Pell", "mana": 11}'), ("cost", "cost = 3")], 8,
     "Pell's sheet (11 mana) and `cost = 3`", "put Pell's sheet in `oogrish` and tried `cost = 3`"),
    ([("oogrish", 'oogrish = {"name": "Ivo", "mana": 20}'), ("cost", "cost = 6")], 14,
     "Ivo's sheet (20 mana) and `cost = 6`", "put Ivo's sheet in `oogrish` and tried `cost = 6`"),
]

SPEND_THE_MANA = dict(
    id="spend-the-mana",
    title="Spend the mana",
    martu=(
        "Oogrish casts. The spell costs `cost`, and it comes out of his sheet.\n"
        "My check tries another sheet and another cost, only inside the check.\n" + _STUCK
    ),
    names=["oogrish", "cost"],
    support="none",
    explainer="lean",
    starter=SPEND_STARTER,
    checkpoints=[
        dict(
            id="spend-the-cost",
            text="Spend `cost` from `oogrish[\"mana\"]`.",
            dictated=False,
            hints=[
                "Look at the comment: one line goes under it.",
                "The new mana is worked out from the old mana and the cost, then stored back.",
                "Read the old value on the right of `=`, and store the new one on the left.",
            ],
            checks=[check("oogrish's mana goes down by cost", _SPEND, reruns=_SPEND_RERUNS)],
            pass_line="Oogrish: Thirteen left. Steady, now.",
        ),
    ],
    solution=SPEND_SOLUTION,
    wrong_answers=[
        dict(why="the starter (nothing spent)", code=SPEND_STARTER, fails_at=1, message_contains="still 18"),
        dict(why="a typed 13 (CMB)", code=_spend('oogrish["mana"] = 13\n'), fails_at=1,
             message_contains="`oogrish[\"mana\"]` holds a typed 13. Mar'tu's check put Pell's sheet in `oogrish`"),
        dict(why="the subtraction with no store", code=_spend('oogrish["mana"] - cost\n'), fails_at=1,
             message_contains="worked out, then forgotten"),
        dict(why="a typed cost (CMB)", code=_spend('oogrish["mana"] = oogrish["mana"] - 5\n'), fails_at=1,
             message_contains="ended at `6`, not `8`"),
        dict(why="a typed start: 18 copied from the sheet (CMB)", code=_spend('oogrish["mana"] = 18 - cost\n'),
             fails_at=1, message_contains="ended at `15`, not `8`"),
        dict(why="the sheet's 18 edited to 13, nothing spent (the start is read from the student's own sheet)",
             code=_spend().replace('"mana": 18', '"mana": 13'), fails_at=1, message_contains="is still 13"),
        dict(why="the new mana in a new variable (NEWBOX)", code=_spend('mana = oogrish["mana"] - cost\n'), fails_at=1,
             message_contains="went into `mana`"),
        dict(why="the subtraction reversed", code=_spend('oogrish["mana"] = cost - oogrish["mana"]\n'), fails_at=1,
             message_contains="`-13`"),
        dict(why="== for = (a comparison, nothing stored)", code=_spend('oogrish["mana"] == oogrish["mana"] - cost\n'),
             fails_at=1, message_contains="compares"),
        dict(why="printed, not stored", code=_spend('print(oogrish["mana"] - cost)\n'), fails_at=1,
             message_contains="printed, not stored"),
        dict(why="a capital key: the new value under another key (KEY)",
             code=_spend('oogrish["Mana"] = oogrish["mana"] - cost\n'), fails_at=1, message_contains="another key"),
        dict(why="the cost overwritten", code=_spend('cost = oogrish["mana"] - cost\n'), fails_at=1,
             message_contains="went into `cost`"),
        dict(why="the sheet replaced by a number (TypeError at the print)",
             code=_spend('oogrish = oogrish["mana"] - cost\n'), fails_at=0, message_contains="not subscriptable"),
    ],
    notes=_rc(12, "code", "dict-write,reassign,combine-values", "dict-write,reassign,combine-values",
              "hold-the-barrier", starter_level="S4", path="READY", dictates="", foreign_names="") + "\n"
    "C8, item 12 (form A: `hero[\"mana\"]` and `cost`). Typed (G2 R17). CMB: the program reruns with Pell's sheet (11 "
    "mana, cost 3: 8) and Ivo's (20 mana, cost 6: 14) slipped in after the student's own lines, so the typed 13 and a "
    "typed cost fail. Fails on (spec): `oogrish[\"mana\"] = 13` -> CMB; the subtraction with no store. Also the new "
    "mana in a new variable (NEWBOX), `==` for `=`, printed not stored, a capital key, and the subtraction reversed. "
    "`oogrish[\"mana\"] -= cost` passes too. The first check reads the start and the cost from the student's own "
    "code, so a changed `cost` is judged by its own numbers (the reruns still catch a typed 13, a typed cost and a "
    "typed 18). " + _P1_NOTE,
)


# ---------------------------------------------------------------------------------------------
# C9 (item 13) shield cost: param-use, return-right-name, exact-names. PAR, PAR-CONST, RET, PNM, RNM.
# ---------------------------------------------------------------------------------------------

SHIELD_HEAD = (
    "# 1. Make shield_cost, with the\n"
    "#    parameters plates and\n"
    "#    price_per_plate.\n"
    "# 2. Return the total cost.\n"
)
SHIELD_CALL = "\n\nprint(shield_cost(3, 4))\n"


def _shield(body=""):
    return SHIELD_HEAD + body + SHIELD_CALL


SHIELD_DEF = "def shield_cost(plates, price_per_plate):\n"
SHIELD_STARTER = _shield()
SHIELD_SOLUTION = _shield(SHIELD_DEF + "    total = plates * price_per_plate\n    return total\n")
DOUBLE_EXAMPLE = "def double(n):\n    answer = n * 2\n    return answer\n\n\nprint(double(7))\n"

_SHIELD = r'''
_f, _m = _find('shield_cost')
assert _f, _m
_ps = _params(_f)
assert _ps == ['plates', 'price_per_plate'], ('The `def` line of `shield_cost` has ' + _names(_ps) + ', and the task '
                                             'names `plates` and `price_per_plate`.')
_d = _defs().get('shield_cost')
_rets = [_n for _n in _ast.walk(_d) if type(_n).__name__ == 'Return'] if _d is not None else []
# Whole numbers typed into a multiplication inside the function (`plates * 2`): the typed-multiplier slip.
_typed_k = [_x.value for _n in (_ast.walk(_d) if _d is not None else []) if type(_n).__name__ == 'BinOp'
            and type(_n.op).__name__ == 'Mult' for _x in (_n.left, _n.right)
            if type(_x).__name__ == 'Constant' and type(_x.value).__name__ == 'int' and _x.value not in (0, 1)]
_res = []
for _args, _want in (((5, 7), 35), ((6, 9), 54)):
    _c = '`shield_cost(' + str(_args[0]) + ', ' + str(_args[1]) + ')`'
    _val, _rows, _e = _call(_f, _args)
    assert _e is None, (_c + ' stopped Python: ' + _err(_e) + '.' + _stopped('shield_cost', _ps, _e, __FOREIGN__)
                        + _ev('called ' + _c))
    _res.append((_c, _val, _rows, _want, _args))
_what = 'called `shield_cost(5, 7)` and `shield_cost(6, 9)`'
_word = ', Python' + chr(39) + 's word for nothing.'
_none = ', so the call gets back `None`' + _word
for _c, _val, _rows, _want, _args in _res:
    if _val is None:
        assert not _rows, '`shield_cost` prints its answer, but the call gets back `None`' + _word + _ev(_what)
        assert _rets, '`shield_cost` has no `return` line' + _none + _ev(_what)
        assert [_x for _x in _rets if _x.value is not None], '`return` stands on its own' + _none + _ev(_what)
        assert False, 'No `return` line ran for ' + _c + _none + _ev(_what)
(_c1, _v1), (_c2, _v2) = [(_r[0], _r[1]) for _r in _res]
assert not (_v1 == _v2 and _v1 != 35), (_c1 + ' and ' + _c2 + ' both returned ' + _show(_v1) + ': the numbers are '
                                        'typed in the function, so the answer does not follow `plates` and '
                                        '`price_per_plate`.' + _ev(_what))
for _c, _val, _rows, _want, _args in _res:
    if _val != _want:
        assert _val not in _args, _c + ' returned ' + _show(_val) + ': a parameter, just as it came in.' + _ev(_what)
        _k = [_x for _x in _typed_k if _val == _args[0] * _x]
        assert not _k, (_c + ' returned ' + _show(_val) + ': it multiplies by a typed ' + str(_k[0]) + ', not by '
                        '`price_per_plate`, so the answer does not follow the price.' + _ev(_what))
        _k = [_x for _x in _typed_k if _val == _args[1] * _x]
        assert not _k, (_c + ' returned ' + _show(_val) + ': it multiplies by a typed ' + str(_k[0]) + ', not by '
                        '`plates`, so the answer does not follow the plates.' + _ev(_what))
        assert False, _c + ' returned ' + _show(_val) + ', not `' + str(_want) + '`.' + _ev(_what)
_u = _uncalled()
assert not _u, _u
'''

SHIELD_COST = dict(
    id="shield-cost",
    title="Shield cost",
    martu=(
        "A shield needs `plates`, and each plate has a price. Write the whole function, yes? The Example shows the "
        "shape, with other names.\n"
        "My check calls your function with other numbers, only inside the check.\n" + _STUCK
    ),
    example=DOUBLE_EXAMPLE,
    example_output="14",
    names=["shield_cost", "plates", "price_per_plate"],
    support="none",
    explainer="lean",
    starter=SHIELD_STARTER,
    checkpoints=[
        dict(
            id="write-shield-cost",
            text="Write `shield_cost(plates, price_per_plate)`, which returns the total cost.",
            dictated=False,
            hints=[
                "Look at the Example: a `def` line, the work, and a `return` line.",
                "A function gets its numbers when it is called, through its parameters.",
                "Use this task's names, letter for letter, not the Example's.",
            ],
            checks=[check("shield_cost returns plates times the price of one", _SHIELD,
                          foreign=["double", "n", "answer"])],
            pass_line="Gearshift: Twelve for three plates at four. Math checks out.",
        ),
    ],
    solution=SHIELD_SOLUTION,
    wrong_answers=[
        dict(why="the starter (no function)", code=SHIELD_STARTER, fails_at=0,
             message_contains="name 'shield_cost' is not defined"),
        dict(why="the Example's name returned (RNM)", code=_shield(SHIELD_DEF + "    total = plates * price_per_plate\n"
                                                                              "    return answer\n"),
             fails_at=0, message_contains="name 'answer' is not defined"),
        dict(why="a near-miss parameter (PNM): price", code=_shield(SHIELD_DEF + "    return price * plates\n"), fails_at=0,
             message_contains="name 'price' is not defined"),
        dict(why="the Example's 2 kept (PAR: a typed multiplier)", code=_shield(SHIELD_DEF + "    return plates * 2\n"),
             fails_at=1, message_contains="returned `10`: it multiplies by a typed 2, not by `price_per_plate`"),
        dict(why="a literal (PAR-CONST)", code=_shield(SHIELD_DEF + "    return 12\n"), fails_at=1,
             message_contains="both returned `12`: the numbers are typed in the function, so the answer does not "
                              "follow `plates` and `price_per_plate`."),
        dict(why="print instead of return (RET)", code=_shield(SHIELD_DEF + "    print(plates * price_per_plate)\n"),
             fails_at=1, message_contains="prints its answer, but the call gets back `None`, Python's word for nothing"),
        dict(why="no return at all", code=_shield(SHIELD_DEF + "    total = plates * price_per_plate\n"), fails_at=1,
             message_contains="`shield_cost` has no `return` line, so the call gets back `None`, Python's word for "
                              "nothing."),
        dict(why="a blank return", code=_shield(SHIELD_DEF + "    total = plates * price_per_plate\n    return\n"),
             fails_at=1, message_contains="`return` stands on its own, so the call gets back `None`"),
        dict(why="approximate parameter names", code=_shield("def shield_cost(plate, price):\n    return plate * price\n"),
             fails_at=1, message_contains="the task names"),
        dict(why="def used like = (def vs =)", code=_shield("def shield_cost = plates * price_per_plate\n"), fails_at=0,
             message_contains="expected '('"),
        dict(why="a missing colon", code=_shield(SHIELD_DEF.replace("):", ")") + "    return plates * price_per_plate\n"),
             fails_at=0, message_contains="expected ':'"),
        dict(why="the task's price typed in (PAR: a typed multiplier instead of the parameter)",
             code=_shield(SHIELD_DEF + "    return plates * 4\n"), fails_at=1,
             message_contains="returned `20`: it multiplies by a typed 4, not by `price_per_plate`"),
        dict(why="the task's plates typed in (PAR: a typed multiplier instead of the other parameter)",
             code=_shield(SHIELD_DEF + "    return 3 * price_per_plate\n"), fails_at=1,
             message_contains="multiplies by a typed 3, not by `plates`"),
        dict(why="= used like def (def vs =): a number, not a function (TypeError at the visible call)",
             code=_shield("shield_cost = 12\n"), fails_at=0, message_contains="'int' object is not callable"),
        dict(why="the function printed, not called (handing over vs calling: no (3, 4))",
             code=_shield(SHIELD_DEF + "    return plates * price_per_plate\n").replace(SHIELD_CALL, "\n\nprint(shield_cost)\n"),
             fails_at=1, message_contains="prints the function `shield_cost` itself"),
        dict(why="+ for * (PAR)", code=_shield(SHIELD_DEF + "    return plates + price_per_plate\n"), fails_at=1,
             message_contains="returned `12`, not `35`"),
        dict(why="the task's numbers typed inside (PAR-CONST)",
             code=_shield(SHIELD_DEF + "    plates = 3\n    price_per_plate = 4\n    return plates * price_per_plate\n"),
             fails_at=1, message_contains="both returned `12`"),
        dict(why="a parameter handed back as it came in (RET-PARAM)", code=_shield(SHIELD_DEF + "    return plates\n"),
             fails_at=1, message_contains="a parameter, just as it came in"),
        dict(why="numbers on the def line (SyntaxError)", code=_shield("def shield_cost(3, 4):\n    return 12\n"),
             fails_at=0, message_contains="invalid syntax"),
    ],
    notes=_rc(13, "code", "param-use,return-right-name,exact-names", "param-use,return-right-name,exact-names",
              "every part with parameters", starter_level="S1", path="READY", dictates="",
              foreign_names="double,n,answer", par="(5, 7),(6, 9)") + "\n"
    "C9, item 13 (form A: `glug_cost(sips, price_per_sip)` with the Example `triple`). Directive 4.6: the goal plus "
    "an Example (`double(n)`, its box `answer`), on screen with Run. The starter has numbered comments (1. make "
    "shield_cost with its parameters; 2. return the total cost), as forms A and C. The None branches are form A's "
    "(no `return` line, print and None, a blank return), each naming `None` as Python's word for nothing; the "
    "same answer twice says the numbers are typed in the function; a typed multiplier (`plates * 2`, `plates * "
    "4`, `3 * price_per_plate`) is named before the plain 'not 35'. NAME: the exact name and the exact parameters, "
    "in order. PAR with (5, 7) -> 35 and (6, 9) -> 54; the task's own call is (3, 4) -> 12, and neither fresh set "
    "gives 12 (lint b). Fails on (spec): the Example's box -> RNM; `plates * 2` -> PAR; `price * plates` -> PNM; a "
    "literal -> PAR-CONST. RNM and PNM crash at the visible call first, so they reach the student as the explainer's "
    "NameError rows 2 and 3; the check names them too when the visible call is gone. " + _P1_NOTE,
)


_P1_SUMMARY = (
    "A retake form. Open it when Mar'tu's notes send you here, for the one task they name. Twelve questions, then "
    "nine short tasks. The glossary, read-aloud and the error explainer stay on; hints are off."
)

RC_PART1_B = dict(
    kind="testout",
    id="rc-part1-b",
    title="Readiness Check · Part 1 · Form B",
    optional=True,
    minutes=20,
    summary=_P1_SUMMARY,
    questions_to_pass=10,
    exercises=[STEP_EAST, PRESENT_FAREWELL, MEND_THE_REPLY, READ_AND_WRITE, MEND_THE_BAR, THROW_DIE, THREE_TRACEBACKS,
               SPEND_THE_MANA, SHIELD_COST],
    notes=(
        "Readiness Check Part 1, form B (curriculum 5.2 / 5.3): the 9 code tasks of items 2, 3b, 5b, 6a-c, 7b, 8b, 11, "
        "12 and 13, in item order. The 12 questions (items 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, 10a, 10b) live in "
        "rc-part1-b-questions, listed first (ITEMS), as form A, so the first win is a prediction; "
        "questions_to_pass=10 approximates 'Part 1 >= 11/13', as form A. The parallel form for a retake or a review "
        "cycle: the same skills as form A, item for item, with new names, numbers and situations (5.2). The "
        "summary (shared with the questions) says it is a retake form, opened from Mar'tu's notes for the one task "
        "they name, and that hints are off. Every task's Learn text ends with form A's Stuck line. Optional: form A "
        "is the one the class takes first, and only form A's rc-part1-a is a required testout (the site's "
        "'required testout = core item' fix keys on it). 20 minutes here plus 8 for the questions = the spec's ~28. "
        "support='none' and explainer='lean' on every task: no hints, tracer, Another way, "
        "Assemble it or Compare; glossary and read-aloud stay on. Every typed task is behavior-checked (CMB, PAR, "
        "CALL, RND, STO, KEY), never OUT alone. Site work: the 5.5 scoring (11/13 items, item 6 at 3 of 4, item 13 "
        "required), skill-tag routing from the notes' meta lines, drawing form B for a retake (and another form's "
        "questions for a quiz retake), opening one named task from Mar'tu's notes, and a pass here that does not "
        "mark the rest of the unit tested out."
    ),
)


# =============================================================================================
# Part 1 form B, questions (quiz rc-part1-b-questions: 10 of the 12 right, questions_to_pass=10)
# =============================================================================================

SHIELD_LINE = (
    "mana = 5\n"
    "max_mana = 12\n"
    'text = "Shield: " + str(mana)\n'
    'print(text + "/" + str(max_mana))\n'
)
FAREWELL_PREDICT = (
    "def get_farewell():\n"
    '    line = "SAFE ROADS, LUCKY."\n'
    "    line = line.lower()\n"
    "    line = line.capitalize()\n"
    "    return line\n"
    "\n\n"
    "print(get_farewell())\n"
)
DODGE_PREDICT = (
    "def dodge_check(roll):\n"
    "    needed = 14\n"
    "    return roll >= needed\n"
    "\n\n"
    "print(dodge_check(13))\n"
    "print(dodge_check(14))\n"
    "print(dodge_check(15))\n"
)
LEDGER_PREDICT = (
    "def armor_score(plates, studs):\n"
    "    heavy = plates * 6\n"
    "    light = studs * 2\n"
    "    return heavy + light\n"
    "\n\n"
    "armor = armor_score(4, 5) + 3\n"
    "print(armor)\n"
)
OPTION_PREDICT = (
    'choice = "option 3"\n'
    "\n"
    'if choice == "option 1":\n'
    '    print("Oogrish: Steady, now.")\n'
    'elif choice == "option 3":\n'
    '    print("Bomb Shell: Shield up.")\n'
    "else:\n"
    "    print(\"Lucky: Fine. I'm in.\")\n"
    'print("The fire crackles.")\n'
)
IN_PREDICT = (
    'book = {"Glimmer": 2, "Mist": 4}\n'
    'print("Glimmer" in book)\n'
    "print(4 in book)\n"
)
CHARMS_LINES = 'charms["spark"]\ncharms["spark"](gearshift)\n'
CHARMS_PREDICT = (
    "def spark(hero):\n"
    '    print(hero["name"] + " sparks.")\n'
    "\n\n"
    'charms = {"spark": spark}\n'
    'gearshift = {"name": "Gearshift"}\n'
    'print("Ready.")\n'
    + CHARMS_LINES
)
ROSTER_CODE = (
    "def check_in(member):\n"
    '    print(member["name"], "is in.")\n'
    "\n\n"
    "roster = [\n"
    '    {"name": "Oogrish", "die": 6},\n'
    '    {"name": "Lucky", "die": 6},\n'
    '    {"name": "Gearshift", "die": 8},\n'
    "]\n"
    "for member in roster:\n"
    "    check_in(member)\n"
)

RC_PART1_B_QUESTIONS = dict(
    kind="quiz",
    id="rc-part1-b-questions",
    title="Readiness Check · Part 1 · Form B questions",
    optional=True,
    minutes=8,
    summary=_P1_SUMMARY,
    questions=[
        dict(
            type="predict",
            id="glue-the-shield-line",
            q="What will the last line print?",
            code=SHIELD_LINE,
            choices=["Shield:5/12", "Shield: 5 / 12", "Shield: 5/12", "Shield: str(mana)/str(max_mana)"],
            answer="Shield: 5/12",
            explain=(
                "`+` glues text exactly as it is, and adds no spaces. The only space is the one inside "
                "`\"Shield: \"`. `str(mana)` is the text `5`, so the brackets and `str` are not printed."
            ),
            notes=_rc(1, "predict", "concat-str", "concat-str", "mana-bars") + "\n"
            "Q1, item 1 (form A: `\"Mana: \" + str(7) + \"/\" + str(10)`). The glue is split over two lines with "
            "variables, the mana-bars shape, so every line fits a phone (36 characters). Fails on (spec): "
            "`Shield:5/12`, `Shield: 5 / 12`. The last distractor is the 'str() is printed' belief.",
        ),
        dict(
            type="predict",
            id="tidy-the-farewell",
            q="`get_farewell()` tidies its line, then the last line prints it. What will it print?",
            code=FAREWELL_PREDICT,
            choices=["SAFE ROADS, LUCKY.", "Safe roads, Lucky.", "safe roads, lucky.", "Safe roads, lucky."],
            answer="Safe roads, lucky.",
            explain=(
                "`.lower()` makes every letter small. Then `.capitalize()` makes only the very first letter big, so "
                "`lucky` stays small. Each line stores its result back in `line`."
            ),
            notes=_rc(3, "a", "chain-methods,store-then-pass", "chain-methods", "program-dialogue-prompt") + "\n"
            "Q2, item 3a (form A: `get_warning()`). Other words than C2's helper, so running C2 gives nothing away. "
            "Distractors: no tidy at all, `.capitalize()` read as capitalizing every name, `.lower()` only.",
        ),
        dict(
            type="predict",
            id="exactly-enough-roll",
            q="`dodge_check` needs 14. What will these three lines print?",
            code=DODGE_PREDICT,
            choices=["False\nFalse\nTrue", "False\nTrue\nTrue", "True\nTrue\nTrue", "False\nTrue\nFalse"],
            answer="False\nTrue\nTrue",
            explain=(
                "`>=` means *at least*. 13 is below 14, so `False`. 14 is exactly enough, so `True`. 15 is more, so "
                "`True`. The function returns the comparison's answer."
            ),
            notes=_rc(4, "a", "boundary,return-comparison,trace-call", "boundary,return-comparison",
                      "skill-checks") + "\n"
            "Q3, item 4a (form A: `latch_check`, needed 11). Fails on (spec): the exact roll -> False (`>` read for "
            "`>=`). Also every roll passes, and `==` read for `>=`.",
        ),
        dict(
            type="predict",
            id="be-the-ledger",
            q="Trace it in your head, then type the number this program prints.",
            code=LEDGER_PREDICT,
            answer="37",
            explain=(
                "Trace with what is IN the boxes. With another call, `armor_score(2, 1) + 3`: `plates` is 2 and "
                "`studs` is 1, so `heavy` is 12 and `light` is 2. The function returns 14, and the line adds 3: 17. "
                "If you typed 11, you added the numbers written in the function; 12, the numbers handed in."
            ),
            notes=_rc(4, "b", "boundary,return-comparison,trace-call", "trace-call", "skill-checks") + "\n"
            "Q4, item 4b, the ledger shape (`ward_strength`-style) with new numbers (form A has its own). Typed, with no "
            "choices: honest tracing, the answer is in no visible text, and the explanation traces another call. Fails "
            "on (spec): the 15-type value (the constants in the function: 6 + 2, then 11 with the + 3) and the 7-type "
            "value (the numbers handed in: 4 + 5, then 12). A quiz has no Run, so nothing here can be pasted and run.",
        ),
        dict(
            type="predict",
            id="which-branch-runs",
            q="What will this program print?",
            code=OPTION_PREDICT,
            choices=["Oogrish: Steady, now.\nThe fire crackles.", "Bomb Shell: Shield up.",
                     "Bomb Shell: Shield up.\nThe fire crackles.",
                     "Bomb Shell: Shield up.\nLucky: Fine. I'm in.\nThe fire crackles."],
            answer="Bomb Shell: Shield up.\nThe fire crackles.",
            explain=(
                "Python asks each test in order, and runs only the first branch whose test is `True`: the `elif`. It "
                "skips `else`. The last `print` is not indented, so it is outside the chain and always runs."
            ),
            notes=_rc(5, "a", "elif-chain,quote-text", "elif-chain", "program-dialogue-options") + "\n"
            "Q5, item 5a (form A traces `option 2`). Fails on (spec): the first branch. Also the `else` run as well, "
            "and the unindented last line taken as part of the chain.",
        ),
        dict(
            type="predict",
            id="in-looks-at-keys",
            q="What will these two lines print?",
            code=IN_PREDICT,
            choices=["True\nTrue", "False\nTrue", "True\nFalse", "False\nFalse"],
            answer="True\nFalse",
            explain=(
                "`in` on a dictionary looks at its keys only. `\"Glimmer\"` is a key, so `True`. 4 is a value, not a "
                "key, so `False`."
            ),
            notes=_rc(6, "d", "dict-read,dict-nested,dict-write,dict-in,dict-key-from-variable", "dict-in",
                      "spell-book,hold-the-barrier") + "\n"
            "Q6, item 6d (form A: `\"Glow\" in book`). Fails on (spec): a value -> True (`in` read as looking at "
            "values).",
        ),
        dict(
            type="predict",
            id="stamp-the-bar",
            q="What will this line print?",
            code='print("█" * 4 + "░" * 3)\n',
            choices=["█4░3", "███████", "████ ░░░", "████░░░"],
            answer="████░░░",
            explain="`*` with text stamps it that many times: four `█`, then three `░`. `+` glues them, with no space.",
            notes=_rc(7, "a", "repeat-string", "repeat-string", "mana-bars") + "\n"
            "Q7, item 7a (form A: `\"█\" * 3 + \"░\" * 2`). Fails on (spec): `█4░3`. Also every block the same, and a "
            "space added by `+`.",
        ),
        dict(
            type="mc",
            id="faces-of-a-d8",
            q="A d8 roll is `random.randint(1, 8)`. Which numbers can it give?",
            choices=["Any whole number from 0 to 8", "Any whole number from 1 to 7", "Any whole number from 1 to 8",
                     "Only the two ends, 1 or 8"],
            answer=2,
            why_wrong={
                0: "A die has no 0 face: the first number, 1, is the lowest it can give.",
                1: "[[randint]] includes its last number, so 8 can come up, like the top face of a real d8.",
                3: "It gives any whole number from the first to the last, not only the two ends.",
            },
            explain="`random.randint(1, 8)` gives a whole number from 1 to 8, and both ends can come up, like a real d8.",
            notes=_rc(8, "a", "randint,randint-param", "randint", "skill-checks") + "\n"
            "Q8, item 8a (form A: `random.randint(1, 6)`). Fails on (spec): 1-7, the exclusive-range belief. Also 0 to "
            "8 and the two ends only. The four choices share one shape, so the right one is not the longest.",
        ),
        dict(
            type="mc",
            id="read-or-call",
            q="`charms` holds a function under the key `\"spark\"`. What is the difference between these two lines?",
            code=CHARMS_LINES,
            choices=[
                "Both lines call the spell, so it runs twice.",
                "The first only reads the function. The second calls it.",
                "The first calls the spell. The second only reads it.",
                "The first reads the text `\"spark\"`. The second calls it.",
            ],
            answer=1,
            why_wrong={
                0: "Only the brackets on the end call a function. Without them, the line only reads what is stored.",
                2: "It is the other way round: the line with `(gearshift)` on the end is the one that calls.",
                3: "`charms[\"spark\"]` is what is stored under the key: the function `spark` itself, not text.",
            },
            explain=(
                "`charms[\"spark\"]` reads the value under the key: the [[function as a value|function]] itself. Adding "
                "`(gearshift)` calls it and hands it `gearshift`, like `spark(gearshift)`."
            ),
            notes=_rc(9, "a", "func-as-value,call-stored-func", "func-as-value", "spell-book,hold-the-barrier") + "\n"
            "Q9, item 9 explain (form A: `spells[\"glow\"]` and `spells[\"glow\"](hero)`). Fails on (spec): 'both run "
            "the spell'. Distractors: the reverse, and the stored value taken for its key's text. The four choices "
            "share one length and shape, so the right one is not the longest.",
        ),
        dict(
            type="predict",
            id="what-the-charm-does",
            q="What will this program print?",
            code=CHARMS_PREDICT,
            choices=["Ready.\nGearshift sparks.", "Ready.\nGearshift sparks.\nGearshift sparks.", "Ready.",
                     "Ready.\nspark\nGearshift sparks."],
            answer="Ready.\nGearshift sparks.",
            explain=(
                "The line `charms[\"spark\"]` on its own reads the function and does nothing with it, so nothing "
                "prints. Only `charms[\"spark\"](gearshift)` calls it: one line."
            ),
            notes=_rc(9, "b", "func-as-value,call-stored-func", "call-stored-func", "spell-book,hold-the-barrier")
            + "\n"
            "Q10, item 9 predict. Fails on (spec): 'both run the spell' (two lines). Also the call missed, and a bare "
            "read taken to print the key.",
        ),
        dict(
            type="mc",
            id="how-many-calls",
            q="How many times does `check_in` run, and what is it handed each time?",
            code=ROSTER_CODE,
            choices=[
                "Once, with the whole roster.",
                "3 times, with one hero's sheet each time.",
                "3 times, with the whole roster each time.",
                "Once, with Oogrish's sheet only.",
            ],
            answer=1,
            why_wrong={
                0: "The call is inside the [[for loop]], so it runs once on every pass, and `member` is one hero each "
                   "time.",
                2: "`check_in(member)` hands over `member`, one sheet from the roster, not the whole list.",
                3: "The loop goes through every sheet in `roster`, not only the first.",
            },
            explain=(
                "The loop runs once for each sheet in `roster`: 3 passes. On each pass `member` holds one hero's "
                "sheet, and `check_in(member)` hands that one sheet over."
            ),
            notes=_rc(10, "a", "list-of-dicts,for-each", "list-of-dicts,for-each", "spell-book,mana-bars") + "\n"
            "Q11, item 10 trace (form A: `show_status(hero)`). Fails on (spec): 'one call with the whole roster'. Also "
            "the whole roster each time, and the first sheet only.",
        ),
        dict(
            type="mc",
            id="what-member-holds",
            q="Same program. While the loop runs, what does `member` hold?",
            code=ROSTER_CODE,
            choices=[
                "The text `\"member\"`, on every pass.",
                "A count of the passes: 1, then 2, then 3.",
                "One hero's sheet on each pass, in order.",
                "The whole roster, on every pass.",
            ],
            answer=2,
            why_wrong={
                0: "`member` has no quotes: it is a variable, the [[loop variable]].",
                1: "The loop does not count the passes. It hands over each item of `roster`, in order.",
                3: "The roster is `roster`. `member` holds one item of it on each pass.",
            },
            explain=(
                "`for member in roster:` puts each item of `roster` in `member`, one pass at a time, in order. Each "
                "item is a hero's sheet, a [[dictionary]]."
            ),
            notes=_rc(10, "b", "list-of-dicts,for-each", "for-each", "spell-book,mana-bars") + "\n"
            "Q12, item 10 explain (one click). Distractors: the name taken as text, the loop variable taken for a "
            "counter (the range-loop belief), the whole list. The four choices share one length.",
        ),
    ],
    notes=(
        "Readiness Check Part 1, form B questions, scored with rc-part1-b: every code task plus 10 of these 12 "
        "(questions_to_pass=10 on the form, as form A). Item order: 1, 3a, 4a, 4b, 5a, 6d, 7a, 8a, 9a, 9b, 10a, 10b; "
        "each question's notes give its item, skill tags and the campaign part it prepares (5.3). No hints; "
        "read-aloud and glossary stay on. Q4, the trace, is typed with no choices (honest tracing), as form A's "
        "ledger question now is; its explanation traces armor_score(2, 1) (kept: the same question can be retaken) "
        "and names the slip values 11 and 12. Right answers sit at varied positions (the site also shuffles). "
        "Listed before rc-part1-b, as form A, and it shares rc-part1-b's summary."
    ),
)


# =============================================================================================
# Part 2: mini-boss B "Hold the Glow Ward" (project, campaign mode for everyone, 5.4), and the optional trial "Hold
# the Ember Ward from its goals" (challenge, advanced). Mini-boss B has the same shape as form A's "Hold the Lantern
# Ward" (rc-miniboss-a), so the two forms ask for the same help: the six comments and checkpoints in the campaign's
# check order, the same rung-2 ladder, the same lean, campaign-like messages. Other names (`use_ward(caster,
# ward_name)`, the page in `page`), another hero (Bomb Shell), another ward and other check data (Ivo, Ember Wall).
# The trial reuses the same six checks, and the two-messages check, with a third set of names (`raise_ward(mage,
# ward_name)`, Oogrish, the Ember Ward) and goals only.
# =============================================================================================

HERO_NAMES = ["Bomb Shell", "Oogrish", "Gearshift", "Lucky"]


def _show_mana(who):
    """The finished `show_mana` helper, for the parameter name `who` (KEEP-checked in CP2)."""
    return (
        f"def show_mana({who}):\n"
        f'    mana = {who}["mana"]\n'
        f'    used = {who}["max_mana"] - mana\n'
        '    bar = "█" * mana + "░" * used\n'
        f'    print({who}["name"], bar)\n'
    )


def _flat(lines):
    """Cast lines moved one step out (straight in the function, not under a branch)."""
    return "".join(line[4:] if line.startswith("        ") else line for line in lines)


# Hidden setup: Bomb Shell's sheet (the party table: affinity 12, max mana 24) with the Glow Ward in his wards, and
# the ward's effect, which records who it was cast on (an engine-like helper, 2.12 rule 3).
MB_SETUP = (
    "_effects = []\n"
    "\n\n"
    "def glow_ward(caster):\n"
    "    _effects.append(caster)\n"
    '    print(caster["name"] + "\'s glow ward shines.")\n'
    "\n\n"
    "bomb_shell = {\n"
    '    "name": "Bomb Shell",\n'
    '    "mana": 24,\n'
    '    "max_mana": 24,\n'
    '    "abilities": {"magical_affinity": 12},\n'
    '    "wards": {\n'
    '        "Glow Ward": {\n'
    '            "mana_cost": 7,\n'
    '            "required_affinity": 10,\n'
    '            "effect": glow_ward,\n'
    "        },\n"
    "    },\n"
    "}\n"
)
SHOW_MANA = _show_mana("caster")
MB_HEAD = (
    "# Already finished. Leave it as\n"
    "# it is.\n"
    + SHOW_MANA
    + "\n\n"
    "def use_ward(caster, ward_name):\n"
    '    if ward_name not in caster["wards"]:\n'
    '        print("Unknown ward:", ward_name)\n'
    "        return\n"
    '    page = caster["wards"][ward_name]\n'
    "\n"
    "    # An if, an elif and an else.\n"
    "    # The numbers follow the order\n"
    "    # of the checks. In the code,\n"
    "    # the caster is tested first.\n"
    "    # 1. A skilled caster with\n"
    "    #    enough mana casts the\n"
    "    #    page's effect.\n"
    "    # 2. Then the mana goes down by\n"
    "    #    the page's cost, and the\n"
    "    #    bar is drawn again.\n"
    "    # 3. Too little affinity: print\n"
    "    #    why, and no cast.\n"
    "    # 4. Otherwise, too little mana:\n"
    "    #    print why, and no cast.\n"
    "    # 5. Exactly enough mana casts.\n"
    "    # 6. Use the page's own cost.\n"
)
MB_CALL = '\n\nuse_ward(bomb_shell, "Glow Ward")\n'
AFF = 'caster["abilities"]["magical_affinity"] < page["required_affinity"]'
MANA = 'caster["mana"] < page["mana_cost"]'
EFFECT = 'page["effect"](caster)'
PAY = '        caster["mana"] = caster["mana"] - page["mana_cost"]\n'
TYPED_PAY = '        caster["mana"] = caster["mana"] - 7\n'
SKILL_MSG = '        print(caster["name"], "isn\'t skilled enough.")\n'
MANA_MSG = '        print(caster["name"], "needs more mana.")\n'
SHOW = "        show_mana(caster)\n"
GUARD_RET = '        print("Unknown ward:", ward_name)\n        return\n'

# What the shared mini-boss checks need to know about this function (filled into each check as `_C`).
MB_CFG = dict(
    fn="use_ward", who="caster", name="ward_name", page="page", sheet="bomb_shell", sheet_hero="Bomb Shell",
    own_fx="glow_ward", own_ward="Glow Ward", own_cost=7, words=["shines", "rises"],
    cw="Ember Wall", cw_line="Ember Wall rises.", foreign=["hero", "spell", "spell_name", "ward"],
    names_line="This one's names are `caster`, `ward_name` and `page`.",
)


def _mb_body(aff=AFF, mana=MANA, effect=EFFECT, pay=PAY, show=SHOW, skill_msg=SKILL_MSG, mana_msg=MANA_MSG):
    return (f"    if {aff}:\n" + skill_msg + f"    elif {mana}:\n" + mana_msg + "    else:\n"
            f"        {effect}\n" + pay + show)


def _mb(body="    pass\n", head=MB_HEAD, call=MB_CALL):
    return head + body + call


MB_STARTER = _mb()
MB_SOLUTION = _mb(_mb_body())
MB_P1 = _mb(f"    {EFFECT}\n")
MB_P2 = _mb(_flat([f"        {EFFECT}\n", TYPED_PAY, SHOW]))
MB_P3 = _mb(f"    if {AFF}:\n" + SKILL_MSG + "    else:\n" + f"        {EFFECT}\n" + TYPED_PAY + SHOW)
MB_P4 = _mb(_mb_body(mana=MANA.replace("<", "<="), pay=TYPED_PAY))
MB_P5 = _mb(_mb_body(pay=TYPED_PAY))

# The shared mini-boss prelude. The check data is fresh, never the visible hero's: Ivo casts Ember Wall (or the
# trial's Briar Ring), with mana 14 of 20 unless a case says otherwise. Evidence is a few short sentences in one pair
# of brackets, with no brackets inside it.
_MB_PRE = r'''
_C = __MB__
_FN, _WHO, _NM, _PG, _SHEET = _C['fn'], _C['who'], _C['name'], _C['page'], _C['sheet']
_fd = _defs().get(_FN)
assert _fd is not None and callable(_g.get(_FN)), 'Keep `' + _FN + '` from the starter, made with `def`.'
assert [_a.arg for _a in _fd.args.args] == [_WHO, _NM], (
    'Keep the `def` line from the starter: `def ' + _FN + '(' + _WHO + ', ' + _NM + '):`.')
_wrong_sheet = bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Name' and _n.id == _SHEET])
_guard_ifs = [_n for _n in _fd.body if type(_n).__name__ == 'If' and type(_n.test).__name__ == 'Compare'
              and type(_n.test.ops[0]).__name__ == 'NotIn']
_ifs = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'If' and _n not in _guard_ifs]
_typed_cmp = [_c for _i in _ifs for _c in _ast.walk(_i.test) if type(_c).__name__ == 'Compare'
              and [_x for _x in [_c.left] + list(_c.comparators) if type(_x).__name__ == 'Constant'
                   and type(_x.value).__name__ == 'int']]
_max_read = bool([_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Subscript'
                  and type(_n.slice).__name__ == 'Constant' and _n.slice.value == 'max_mana'])
_into_page = [_n for _n in _ast.walk(_fd) if type(_n).__name__ in ('Assign', 'AugAssign')
              and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
                   if type(_t).__name__ == 'Subscript' and type(_t.value).__name__ == 'Name' and _t.value.id == _PG]]


def _why(_m, _r):
    if _wrong_sheet:
        return ('`' + _FN + '` uses `' + _SHEET + '` by name, so ' + _r['who'] + "'s cast used " + _C['sheet_hero']
                + "'s sheet.")
    if _max_read:
        return '`' + _FN + '` reads `"max_mana"`, the most a ' + _WHO + ' can hold, not the mana they have now.'
    return _m


def _say(_r, _also=''):
    return (" (Mar'tu's check cast " + _r['cw'] + ' for ' + _r['who'] + ', only inside the check. ' + _r['cw']
            + ' costs ' + str(_r['cost']) + ' and needs affinity ' + str(_r['need']) + '. ' + _r['who']
            + ' has affinity ' + str(_r['aff']) + ' and ' + str(_r['mana']) + ' mana.'
            + ((' ' + _also) if _also else '') + ')')


def _cast(_aff, _mana, _cost, _need, _who='Ivo'):
    _fx = []
    _cw = _C['cw']

    def _effect(_target):
        _fx.append(_target)
        print(_C['cw_line'])

    _hero = {'name': _who, 'mana': _mana, 'max_mana': 20, 'abilities': {'magical_affinity': _aff},
             'wards': {_cw: {'mana_cost': _cost, 'required_affinity': _need, 'effect': _effect}}}
    _bars = []

    def _drawn(_target):
        _bars.append((_target, _target.get('mana') if type(_target).__name__ == 'dict' else None))

    _real = _g.get('show_mana')
    _w0 = len(_g.get('_effects', []))
    _g['show_mana'] = _drawn
    try:
        _val, _ls, _x = _call(_g[_FN], (_hero, _cw))
    finally:
        _g['show_mana'] = _real
    return dict(fx=_fx, msgs=[_l for _l in _ls if _l != _C['cw_line']], left=_hero['mana'], bars=_bars,
                wards=_g.get('_effects', [])[_w0:], err=_x, hero=_hero, who=_who, cw=_cw, cost=_cost, need=_need,
                aff=_aff, mana=_mana)


def _crash(_r):
    _e = _r['err']
    _n = (getattr(_e, 'name', '') or '') if type(_e).__name__ == 'NameError' else ''
    if _n in _C['foreign']:
        return '`' + _n + '` is a name from another function. ' + _C['names_line'] + _say(_r)
    if _n == 'print_prompt':
        return "`print_prompt` is the campaign's helper, and it is not here." + _say(_r)
    if type(_e).__name__ == 'KeyError' and _e.args and _e.args[0] == _C['own_ward']:
        return ('`' + _FN + '` reads the ward `"' + _C['own_ward'] + '"` by a typed name, not the one `' + _NM
                + '` names. Python stopped with ' + _err(_e) + '.' + _say(_r))
    _text_read = [_s for _s in _ast.walk(_fd) if type(_s).__name__ == 'Subscript'
                  and type(_s.value).__name__ == 'Name' and _s.value.id == _NM]
    if type(_e).__name__ == 'TypeError' and 'string indices' in str(_e) and _text_read:
        return ('`' + _NM + "` holds the ward's name, some text, not its page. Python stopped with " + _err(_e) + '.'
                + _say(_r))
    return 'Inside `' + _FN + '`, Python stopped with ' + _err(_e) + '.' + _say(_r)
'''

_MB_CASTS = r'''
_r = _cast(11, 14, 4, 8)
assert _r['err'] is None, _crash(_r)
_never = _r['cw'] + ' never ran.'
_instead = 'The ' + _C['own_ward'] + ' ran instead.'
if not _r['fx']:
    _bare = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Subscript']
    assert not _bare, 'The ' + _PG + "'s effect is read, but nothing calls it." + _say(_r, _never)
    _by_name = [_c for _c in _ast.walk(_fd) if _is_call(_c, _C['own_fx'])]
    assert not (_r['wards'] and _by_name), ('`' + _C['own_fx'] + '` is called by its own name, so every ward would '
                                            'cast the ' + _C['own_ward'] + '.' + _say(_r, _instead))
    assert not _r['wards'], (_why('The ' + _C['own_ward'] + ' ran, not the ward that `' + _NM + '` names.', _r)
                             + _say(_r, _instead))
    _said_fx = [_l for _l in _r['msgs'] if [_w for _w in _C['words'] if _w in _l.lower()]]
    assert not _said_fx, "The effect's words were printed, but the " + _PG + "'s effect never ran." + _say(_r, _never)
    assert not _r['msgs'], _why('A skilled ' + _WHO + ' with enough mana was turned away.', _r) + _say(_r)
    assert False, 'A skilled ' + _WHO + ' with enough mana did not cast: the ' + _PG + "'s effect never ran." + _say(_r)
assert len(_r['fx']) == 1, 'The ' + _PG + "'s effect ran more than once in one cast." + _say(_r)
assert _r['fx'][0] is _r['hero'], (_why('The ' + _PG + "'s effect was handed another sheet, not the " + _WHO + '.', _r)
                                   + _say(_r))
assert 'None' not in _r['msgs'], ('A `print(...)` around a call showed `None`, Python' + chr(39) + 's word for '
                                  'nothing.' + _say(_r))
_u = _uncalled()
assert not _u, _u
'''

# The starter's guard still turns away a ward the caster doesn't know (it is given; a check keeps it honest, as
# form A's does).
_MB_GUARD = r'''
_fx = []


def _veil(_target):
    _fx.append(_target)


_hero = {'name': 'Brakka', 'mana': 15, 'max_mana': 20, 'abilities': {'magical_affinity': 12},
         'wards': {'Ash Veil': {'mana_cost': 5, 'required_affinity': 7, 'effect': _veil}}}
_real = _g.get('show_mana')
_w0 = len(_g.get('_effects', []))
_g['show_mana'] = lambda _target: None
try:
    _val, _ls, _e = _call(_g[_FN], (_hero, 'Star Shard'))
finally:
    _g['show_mana'] = _real
_said = " (Mar'tu's check cast Star Shard for Brakka, only inside the check. Brakka knows only Ash Veil."
_away = "The starter's guard no longer turns away a ward the " + _WHO + " doesn't know."
assert _e is None, _away + ' Python stopped with ' + _err(_e) + '.' + _said + ')'
assert not _fx and len(_g.get('_effects', [])) == _w0 and _hero['mana'] == 15, _away + _said + ' A ward was cast.)'
assert _ls, ("The starter's guard no longer says so when the " + _WHO + " doesn't know the ward." + _said
             + ' Nothing was printed.)')
'''

_MB_BAR = r'''
_r = _cast(11, 14, 4, 8)
assert _r['err'] is None, _crash(_r)
_still = _r['who'] + ' still had 14 mana.'
if _r['left'] == 14:
    _sub = [_n for _n in _ast.walk(_fd) if (type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'BinOp')
            or (type(_n).__name__ == 'Assign' and type(_n.targets[0]).__name__ == 'Name'
                and type(_n.value).__name__ == 'BinOp')]
    assert not _sub, 'The new mana is worked out, but `' + _WHO + '["mana"]` never changes.' + _say(_r, _still)
    assert not _into_page, "The new mana went into the ward's page, not the " + _WHO + "'s sheet." + _say(_r, _still)
    assert False, _why('After the cast, the ' + _WHO + "'s mana did not go down.", _r) + _say(_r, _still)
assert _r['left'] < 14, (_why('After the cast, the ' + _WHO + "'s mana went up.", _r)
                         + _say(_r, _r['who'] + "'s mana went up to " + str(_r['left']) + '.'))
_bare_show = [_n for _n in _ast.walk(_fd) if type(_n).__name__ == 'Expr' and type(_n.value).__name__ == 'Name'
              and _n.value.id == 'show_mana']
assert _r['bars'] or not _bare_show, ('`show_mana` has no `()` after it, so it is never called.'
                                      + _say(_r, 'The bar was not drawn again.'))
assert _r['bars'], 'After the cast, `show_mana` was not called, so the bar was not drawn again.' + _say(_r)
_hb, _mb = _r['bars'][-1]
assert _hb is _r['hero'], _why('`show_mana` was handed another sheet, not the ' + _WHO + '.', _r) + _say(_r)
assert _mb == _r['left'], ('The bar was drawn before the mana went down, so it shows the old mana.'
                           + _say(_r, 'The bar showed ' + str(_mb) + ' mana. The mana ended at ' + str(_r['left'])
                                  + '.'))
'''

_MB_KEEP = r'''
_fn0 = __FN__
_k = _keep('show_mana', __ORIG__)
assert _k != 'gone', 'The finished `show_mana` is gone from the code, and `' + _fn0 + '` calls it.'
assert not _k, '`show_mana` was already finished, and it changed.'
'''

_MB_TURNS_AWAY = r'''
def _effect_line(_s):
    return (type(_s).__name__ == 'Expr' and type(_s.value).__name__ == 'Call'
            and type(_s.value.func).__name__ == 'Subscript')


def _open_chain(_s):
    # an if (or an if / elif chain) with no last `else`
    while len(_s.orelse) == 1 and type(_s.orelse[0]).__name__ == 'If':
        _s = _s.orelse[0]
    return not _s.orelse


# An `if` with no `else` straight in the function, and the cast still at function level below it: the caster is
# told why, then casts anyway (the cast lines were never moved under `else:`). Two `if` tests: the first one's
# message shows, then the second one's `else` casts anyway.
_top_ifs = [_s for _s in _fd.body if type(_s).__name__ == 'If' and _s not in _guard_ifs]
_open_if = [_i for _i, _s in enumerate(_fd.body) if _s in _top_ifs and _open_chain(_s)]
_no_else = bool(_open_if) and bool([_i for _i, _s in enumerate(_fd.body) if _effect_line(_s) and _i > _open_if[0]])
for _i, (_aff, _mana, _cost, _need, _kind) in enumerate(__CASES__):
    _who = 'Moss' if _i % 2 else 'Ivo'
    _r = _cast(_aff, _mana, _cost, _need, _who)
    assert _r['err'] is None, _crash(_r)
    if _kind == 'low':
        if _r['fx']:
            _also = 'The message showed, then the ward was cast.' if _r['msgs'] else 'The ward was cast anyway.'
            assert not (_r['msgs'] and _no_else), ('The ' + _WHO + ' is told why, then casts anyway: the cast lines '
                                                   'are not inside the last branch, `else`.' + _say(_r, _also))
            assert not (_r['msgs'] and len(_top_ifs) >= 2), (
                'With two `if` tests, a ' + _WHO + ' turned away by the first one still reached `else` and cast.'
                + _say(_r, _also))
            assert not _typed_cmp, __TYPED__ + _say(_r, _also)
            assert False, _why(__TURN_AWAY__, _r) + _say(_r, _also)
        assert _r['left'] == _mana, 'Nothing was cast, but the mana still went down.' + _say(_r)
        assert _r['msgs'], 'The ' + _WHO + ' was turned away, but nothing was printed to say why.' + _say(_r)
        assert len(_r['msgs']) == 1, 'One cast printed ' + str(len(_r['msgs'])) + ' messages.' + _say(_r)
        _named = [_n for _n in __HEROES__ + ['Ivo', 'Moss'] if _n in _r['msgs'][0] and _n != _who]
        assert not _named, ('A message names ' + (_named or [''])[0] + ', a typed name, not the ' + _WHO + '.'
                            + _say(_r))
    else:
        assert _r['fx'], __EXACT__ + _say(_r, _who + ' was turned away.')
'''

# Too little affinity and too little mana are two reasons: one message for each, not the same words for both.
_MB_TWO_REASONS = r'''
_a = _cast(5, 14, 4, 8)
_b = _cast(11, 3, 4, 8)
assert _a['err'] is None, _crash(_a)
assert _b['err'] is None, _crash(_b)
assert not (_a['msgs'] and _a['msgs'] == _b['msgs']), (
    "Too little mana printed the same message as too little affinity. (Mar'tu's check cast " + _a['cw']
    + ' for Ivo twice, only inside the check. Once Ivo had affinity 5, and ' + _a['cw'] + ' needs 8. Once Ivo had '
    '3 mana, and ' + _a['cw'] + ' costs 4.)')
'''

# Two casts with other mana and other costs, so a typed cost, a typed result and a typed start each show.
_MB_OWN_COST = r'''
_res = []
for _mana, _cost in ((14, 2), (17, 9)):
    _r = _cast(11, _mana, _cost, 8)
    assert _r['err'] is None, _crash(_r)
    _res.append((_mana, _cost, _mana - _cost, _r))
_pays = [_n for _n in _ast.walk(_fd) if type(_n).__name__ in ('Assign', 'AugAssign')
         and [_t for _t in (_n.targets if type(_n).__name__ == 'Assign' else [_n.target])
              if type(_t).__name__ == 'Subscript' and type(_t.slice).__name__ == 'Constant' and _t.slice.value == 'mana']]
_typed_pay = [_c for _p in _pays for _c in _ast.walk(_p.value) if type(_c).__name__ == 'Constant'
              and type(_c.value).__name__ == 'int']
_own = _C['own_cost']
_same = _res[0][3]['left'] == _res[1][3]['left']
for _mana, _cost, _want, _r in _res:
    if _r['left'] != _want:
        _end = _r['who'] + "'s mana ended at " + str(_r['left']) + ', not ' + str(_want) + '.'
        assert _r['left'] != _mana - _own, ('The mana went down by a typed ' + str(_own) + ", not by the ward's own "
                                            'cost.' + _say(_r, _end))
        assert _r['left'] != _cost - _mana, 'The subtraction runs the wrong way: the cost minus the mana.' + _say(_r, _end)
        assert _r['left'] != 14 - _cost, ('The new mana starts from a typed 14, not from the ' + _WHO + "'s mana."
                                          + _say(_r, _end))
        assert not _same, ('The mana ends at ' + str(_r['left']) + ' whatever the mana and the cost: the number was '
                           'typed.' + _say(_r, _end))
        assert not _typed_pay, "The mana goes down by a typed number, not by the ward's own cost." + _say(_r, _end)
        assert False, _why("The mana did not go down by the ward's own cost.", _r) + _say(_r, _end)
'''


def mb_check(label, body, cfg=MB_CFG, setup=MB_SETUP, **values):
    """A mini-boss check: the shared _MB_PRE, then the body. Both are filled with the same values."""
    return check(label, _MB_PRE + body, setup=setup, mb=cfg, **values)


def _six_checks(cfg, setup, show_mana, who):
    """The six checkpoints' checks, in the campaign's order (form B's mini-boss and the trial share them)."""
    say = dict(cfg=cfg, setup=setup)
    return [
        [mb_check(f"a skilled {who} with enough mana casts", _MB_CASTS, **say),
         mb_check(f"the starter's guard still turns away a ward the {who} doesn't know", _MB_GUARD, **say)],
        [check("show_mana is unchanged", _MB_KEEP, orig=show_mana, fn=cfg["fn"]),
         mb_check("the mana bar updates after a cast", _MB_BAR, **say)],
        [mb_check("too little affinity does not cast", _MB_TURNS_AWAY, **say,
                  cases=[(5, 14, 4, 8, "low"), (10, 14, 4, 11, "low"), (8, 14, 4, 8, "exact")],
                  typed=f"A test compares with a typed number, not the {cfg['page']}'s own `\"required_affinity\"`.",
                  turn_away=f"A {who} with too little affinity still cast.",
                  exact=f"A {who} with exactly enough affinity was turned away.", heroes=HERO_NAMES)],
        [mb_check("too little mana does not cast", _MB_TURNS_AWAY, **say,
                  cases=[(11, 3, 4, 8, "low"), (11, 7, 8, 5, "low"), (5, 3, 4, 8, "low")],
                  typed=f"A test compares with a typed number, not the {cfg['page']}'s own `\"mana_cost\"`.",
                  turn_away=f"A {who} with too little mana still cast.", exact="", heroes=HERO_NAMES),
         mb_check("too little mana and too little affinity print different messages", _MB_TWO_REASONS, **say)],
        [mb_check("exactly enough mana still casts", _MB_TURNS_AWAY, **say,
                  cases=[(11, 4, 4, 8, "exact"), (11, 9, 9, 8, "exact")], typed="", turn_away="",
                  exact=f"A {who} with exactly enough mana was turned away.", heroes=HERO_NAMES)],
        [mb_check("the ward's own cost is used", _MB_OWN_COST, **say)],
    ]


_MB_CHECKS = _six_checks(MB_CFG, MB_SETUP, SHOW_MANA, "caster")

# The jar and spoon: the picture with other names that CP2 and CP3 (and the trial) teach with.
JAR_PICTURE = (
    "```python\n"
    'if jar["honey"] < spoon["size"]:\n'
    '    print("Not enough honey.")\n'
    "else:\n"
    "    pour(jar, spoon)\n"
    "```"
)
JAR_PAY = ('`jar["honey"] = jar["honey"] - spoon["size"]` reads the old value on the right, takes away a value read '
           'from the other dictionary, and stores the new one on the left.')

RC_MINIBOSS_B = dict(
    kind="project",
    id="rc-miniboss-b",
    title="Mini-boss B: Hold the Glow Ward",
    optional=True,
    minutes=15,
    summary=(
        "A second mini-boss with other names: for after Mar'tu's version helped you through the first one, or for "
        "more practice. Write `use_ward` and pass its six checks, on your own."
    ),
    intro=(
        "Write the rest of `use_ward(caster, ward_name)` where the comments are, using an `if`, an `elif` and an "
        "`else`. The comments are numbered in the order of the six checks, not of the lines: in the code, the caster "
        "is tested first. This is [[campaign mode]]: the numbered comments, the check messages, the error explainer, "
        "and Mar'tu's version after 5 minutes. No Assemble it, and Help stops before the answer, as in the campaign.\n"
        "The campaign's error messages are shorter than Mar'tu's. Read the last line first, the same way."
    ),
    martu=(
        "The barrier part, with other names again. The guard is done: a ward the caster doesn't know is turned away. "
        "`ward_name` holds the ward's name, and `page` holds its page. Bomb Shell's sheet is already made:\n"
        "```python\nbomb_shell = {\n    \"name\": \"Bomb Shell\",\n    \"mana\": 24,\n    \"max_mana\": 24,\n"
        "    \"abilities\": {\n        \"magical_affinity\": 12,\n    },\n    \"wards\": {\n"
        "        \"Glow Ward\": {\n            \"mana_cost\": 7,\n            \"required_affinity\": 10,\n"
        "            \"effect\": glow_ward,\n        },\n    },\n}\n```\n"
        "`show_mana(caster)` is finished. My check casts for other heroes, with other wards, only inside the check. "
        "Exactly enough is enough, yes?"
    ),
    setup=MB_SETUP,
    names=["use_ward", "caster", "ward_name", "page", "show_mana"],
    support="light",
    solo=True,
    explainer="lean",
    starter=MB_STARTER,
    checkpoints=[
        dict(
            id="skilled-caster-casts",
            text="A caster who is skilled enough and has enough mana casts: call `page[\"effect\"](caster)`.",
            dictated=True,
            hints=[
                "Look at comment 1. For now the cast can sit right under the `page` line. When the tests come, it "
                "moves one step deeper, under `else:`.",
                "A function stored in a dictionary runs when brackets with a value follow it: `pack[\"tool\"](sheet)` "
                "runs the tool on that sheet.",
                "Read the effect from `page`, then hand it the caster, `caster`, in the brackets.",
            ],
            checks=_MB_CHECKS[0],
            pass_line="Bomb Shell: Glow Ward up. Shield up.",
        ),
        dict(
            id="bar-updates",
            text="The mana bar updates: subtract `page[\"mana_cost\"]` from `caster[\"mana\"]`, then call "
                 "`show_mana(caster)`.",
            dictated=True,
            hints=[
                "Look at comment 2. Two more lines go under the cast, in the same branch.",
                JAR_PAY,
                "The cost is on the ward's page, `page[\"mana_cost\"]`. The finished helper draws the bar.",
            ],
            checks=_MB_CHECKS[1],
            pass_line="Gearshift: Mana down, bar redrawn. Math checks out.",
        ),
        dict(
            id="low-affinity-no-cast",
            text="If `caster[\"abilities\"][\"magical_affinity\"]` is lower than `page[\"required_affinity\"]`, "
                 "print that the caster isn't skilled enough, and don't cast.",
            dictated=True,
            hints=[
                "Look at comment 3. This test goes first, at the top of the chain, above the cast.",
                "Two keys in a row read inside a sheet, the outer key first: the affinity sits inside "
                "`\"abilities\"`. `<` means *lower than*.",
                "Only one branch runs. The lines that must wait for the test move one step deeper, under `else:`. "
                "With other names:\n" + JAR_PICTURE,
            ],
            checks=_MB_CHECKS[2],
            pass_line="Oogrish: Not skilled enough is a fair answer. Steady, now.",
        ),
        dict(
            id="low-mana-no-cast",
            text="Otherwise, if `caster[\"mana\"]` is lower than `page[\"mana_cost\"]`, print that the caster needs "
                 "more mana, and don't cast.",
            dictated=True,
            hints=[
                "Look at comment 4. `elif` sits between the first test and `else:`, at the same indent as the `if`.",
                "`elif` asks only when the test above it was false, so one cast prints one message at most.",
                "Compare `caster[\"mana\"]` with the page's own `\"mana_cost\"`, and give this reason its own words.",
            ],
            checks=_MB_CHECKS[3],
            pass_line="Lucky: No mana, no ward. I'll allow it.",
        ),
        dict(
            id="exactly-enough-mana",
            text="Exactly enough mana still casts. Use `<` and not `<=`.",
            dictated=True,
            hints=[
                "Look at comment 5, then at the sign in the mana test.",
                "`<` means *lower than*. `<=` means *lower than or the same*, so it turns away exactly enough.",
                "A caster with 4 mana and a ward that costs 4 has exactly enough: the test must let them through.",
            ],
            checks=_MB_CHECKS[4],
            pass_line="Mar'tu: Exactly enough is enough. The ward holds.",
        ),
        dict(
            id="own-cost",
            text="The ward's own cost is used, whatever the ward.",
            dictated=False,
            hints=[
                "Look at comment 6, then at the subtraction. Each ward has its own cost, on its own page.",
                "Read a value from the page you have, like `shelf[\"price\"]`, not a number typed in.",
                "The page is `page`. Its cost is under the key `\"mana_cost\"`.",
            ],
            checks=_MB_CHECKS[5],
            pass_line="Mar'tu: Get it, compare, act. Six checks. You did that on your own.",
        ),
    ],
    solution=MB_SOLUTION,
    partials=[MB_P1, MB_P2, MB_P3, MB_P4, MB_P5],
    another_way=[
        dict(angle="picture", label="Get it, compare, act", text=(
            "```text\nGet it:  page = the ward's page\nCompare: affinity < need?\n           -> not skilled\n"
            "         mana < cost?\n           -> not enough\nAct:     cast, pay, draw\n```")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "This is `cast_spell` from hold-the-barrier, with other names: `ward_name` for `spell_name`, `page` for "
            "`spell`, `\"wards\"` for `\"spell_book\"`, `\"effect\"` for `\"spell_function\"`, and `print` for "
            "`print_prompt`. The same six checks, in the same order.")),
    ],
    campaign_link=dict(
        module=M2,
        part="hold-the-barrier",
        why=(
            "You have played this part: `cast_spell` with its guard, the nested affinity read, `<` and not `<=`, "
            "`spell[\"spell_function\"](caster)`, the cost, and `show_mana`. Pass these six checks alone, and "
            "the campaign's six are the same ones."
        ),
    ),
    takeaway="Get it, compare, act: `if` / `elif` with `<`, then `page[\"effect\"](caster)`, pay, `show_mana(caster)`.",
    wrong_answers=[
        dict(why="the starter (pass)", code=MB_STARTER, fails_at=1, message_contains="did not cast"),
        dict(why="the effect read, never called (calling vs handing over: no (caster))",
             code=_mb(_mb_body(effect='page["effect"]')), fails_at=1, message_contains="nothing calls it"),
        dict(why="glow_ward called by its own name", code=_mb(_mb_body(effect="glow_ward(caster)")), fails_at=1,
             message_contains="by its own name"),
        dict(why="the effect handed the wrong sheet (bomb_shell, not caster)",
             code=_mb(_mb_body(effect='page["effect"](bomb_shell)')), fails_at=1,
             message_contains="`use_ward` uses `bomb_shell` by name, so Ivo's cast used Bomb Shell's sheet."),
        dict(why="the affinity sign backwards", code=_mb(_mb_body(aff=AFF.replace("<", ">"))), fails_at=1,
             message_contains="was turned away"),
        dict(why="a nesting level skipped: caster[\"magical_affinity\"] (KeyError)",
             code=_mb(_mb_body(aff='caster["magical_affinity"] < page["required_affinity"]')), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="form A's name hero copied (NameError at the student's own run)",
             code=_mb(_mb_body(aff=AFF.replace("caster", "hero"))), fails_at=0,
             message_contains="name 'hero' is not defined"),
        dict(why="the campaign's spell copied for page (NameError)", code=_mb(_mb_body(aff=AFF.replace("page", "spell"))),
             fails_at=0, message_contains="name 'spell' is not defined"),
        dict(why="the campaign's print_prompt copied, in a branch the own run never reaches (engine off)",
             code=_mb(_mb_body(skill_msg='        print_prompt(caster["name"] + " can\'t.")\n')), fails_at=3,
             message_contains="`print_prompt` is the campaign's helper"),
        dict(why="form A's habit: the effect read from `ward`, form A's page (NameError at the student's own run)",
             code=_mb(_mb_body(effect='ward["effect"](caster)')), fails_at=0,
             message_contains="name 'ward' is not defined"),
        dict(why="form A's habit `ward[\"effect\"](caster)`, the given call removed (the check names it)",
             code=_mb(_mb_body(effect='ward["effect"](caster)'), call="\n"), fails_at=1,
             message_contains="`ward` is a name from another function. This one's names are `caster`, `ward_name` "
                              "and `page`."),
        dict(why="the effect read from the name, not the page: ward_name[\"effect\"] (TypeError)",
             code=_mb(_mb_body(effect='ward_name["effect"](caster)')), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="ward_name[\"effect\"], the given call removed (the check names it)",
             code=_mb(_mb_body(effect='ward_name["effect"](caster)'), call="\n"), fails_at=1,
             message_contains="`ward_name` holds the ward's name, some text, not its page."),
        dict(why="CP1 the given guard's return removed (a given line edited: an unknown ward crashes)",
             code=_mb(_mb_body(), head=MB_HEAD.replace(GUARD_RET, '        print("Unknown ward:", ward_name)\n')),
             fails_at=1, message_contains="starter's guard"),
        dict(why="CP1 the given guard deleted",
             code=_mb(_mb_body(), head=MB_HEAD.replace('    if ward_name not in caster["wards"]:\n' + GUARD_RET, "")),
             fails_at=1, message_contains="starter's guard"),
        dict(why="CP1 the page read by a typed ward name (CMB: a literal instead of the parameter `ward_name`)",
             code=_mb(_mb_body(), head=MB_HEAD.replace('caster["wards"][ward_name]', 'caster["wards"]["Glow Ward"]')),
             fails_at=1, message_contains="by a typed name, not the one `ward_name` names"),
        dict(why="CP1 the effect read through a typed ward name",
             code=_mb(_mb_body(effect='caster["wards"]["Glow Ward"]["effect"](caster)')), fails_at=1,
             message_contains="by a typed name"),
        dict(why="CP1 Bomb Shell's own Glow Ward effect, read from bomb_shell",
             code=_mb(_mb_body(effect='bomb_shell["wards"]["Glow Ward"]["effect"](caster)')), fails_at=1,
             message_contains="uses `bomb_shell` by name"),
        dict(why="CP1 the effect's words printed instead of calling it (a typed line)",
             code=_mb(_mb_body(effect='print(caster["name"] + "\'s glow ward shines.")')), fails_at=1,
             message_contains="words were printed"),
        dict(why="CP1 print() around the effect call (it returns None)",
             code=_mb(_mb_body(effect='print(page["effect"](caster))')), fails_at=1,
             message_contains="showed `None`, Python's word for nothing"),
        dict(why="CP1 the given call at the bottom left without () (calling vs naming)",
             code=_mb(_mb_body(), call="\n\nuse_ward\n"), fails_at=1, message_contains="no brackets after it"),
        dict(why="CP2 show_mana with no () (calling vs naming)", code=_mb(_mb_body(show="        show_mana\n")),
             fails_at=2, message_contains="has no `()`"),
        dict(why="CP2 the subtraction never stored",
             code=_mb(_mb_body(pay='        caster["mana"] - page["mana_cost"]\n')), fails_at=2,
             message_contains="never changes"),
        dict(why="CP2 the new mana kept in a new variable",
             code=_mb(_mb_body(pay='        mana = caster["mana"] - page["mana_cost"]\n')), fails_at=2,
             message_contains="never changes"),
        dict(why="CP2 show_mana not called", code=_mb(_mb_body(show="")), fails_at=2, message_contains="was not called"),
        dict(why="CP2 show_mana before the subtraction", code=_mb(_mb_body(pay=SHOW + PAY, show="")), fails_at=2,
             message_contains="old mana"),
        dict(why="CP2 show_mana handed the wrong sheet", code=_mb(_mb_body(show="        show_mana(bomb_shell)\n")),
             fails_at=2, message_contains="uses `bomb_shell` by name"),
        dict(why="CP2 the finished helper edited (told to leave it as it is)",
             code=_mb(_mb_body(), head=MB_HEAD.replace('print(caster["name"], bar)', "print(bar)")), fails_at=2,
             message_contains="was already finished, and it changed"),
        dict(why="CP2 the new mana stored in the ward's page (the wrong sheet)",
             code=_mb(_mb_body(pay='        page["mana_cost"] = caster["mana"] - page["mana_cost"]\n')),
             fails_at=2, message_contains="ward's page"),
        dict(why="CP2 subtracted from max_mana (the wrong key)",
             code=_mb(_mb_body(pay='        caster["mana"] = caster["max_mana"] - page["mana_cost"]\n')),
             fails_at=2, message_contains="`\"max_mana\"`"),
        dict(why="CP3 <= on the affinity (exactly enough turned away)", code=_mb(_mb_body(aff=AFF.replace("<", "<="))),
             fails_at=3, message_contains="exactly enough affinity"),
        dict(why="CP3 a typed number for the required affinity (the Glow Ward's 10)",
             code=_mb(_mb_body(aff='caster["abilities"]["magical_affinity"] < 10')), fails_at=3,
             message_contains="typed number"),
        dict(why="CP3 two ifs, not if / elif (the second if's else still casts)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    if {MANA}:\n" + MANA_MSG + "    else:\n"
                      f"        {EFFECT}\n" + PAY + SHOW), fails_at=3, message_contains="two `if` tests"),
        dict(why="CP3 the affinity compared with the cost (the wrong key on the page)",
             code=_mb(_mb_body(aff='caster["abilities"]["magical_affinity"] < page["mana_cost"]')), fails_at=3,
             message_contains="too little affinity still cast"),
        dict(why="CP3 the check's hero name copied from a message into the print (a typed name)",
             code=_mb(_mb_body(skill_msg='        print("Ivo isn\'t skilled enough.")\n')), fails_at=3,
             message_contains="names Ivo"),
        dict(why="CP3 no message when turned away", code=_mb(_mb_body(skill_msg="        return\n")), fails_at=3,
             message_contains="nothing was printed"),
        dict(why="CP3 the if added above the cast, no else (the cast lines never moved under else:)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + _flat([f"        {EFFECT}\n", PAY, SHOW])), fails_at=3,
             message_contains="casts anyway"),
        dict(why="the elif added too, still no else (caught at CP3)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    elif {MANA}:\n" + MANA_MSG
                      + _flat([f"        {EFFECT}\n", PAY, SHOW])), fails_at=3, message_contains="casts anyway"),
        dict(why="else: written, the cast lines not indented under it (a missing indent)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + "    else:\n" + _flat([f"        {EFFECT}\n", PAY, SHOW])),
             fails_at=0, message_contains="expected an indented block"),
        dict(why="the colon left off elif", code=_mb(_mb_body().replace(f"    elif {MANA}:", f"    elif {MANA}")),
             fails_at=0, message_contains="expected ':'"),
        dict(why="elif after else (SyntaxError)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + "    else:\n" + f"        {EFFECT}\n" + PAY + SHOW
                      + f"    elif {MANA}:\n" + MANA_MSG), fails_at=0, message_contains="invalid syntax"),
        dict(why="CP3 a typed hero name in the message (a literal instead of the parameter)",
             code=_mb(_mb_body(skill_msg='        print("Bomb Shell isn\'t skilled enough.")\n')), fails_at=3,
             message_contains="a typed name"),
        dict(why="CP4 a typed number for the cost in the test (the Glow Ward's 7)",
             code=_mb(_mb_body(mana='caster["mana"] < 7')), fails_at=4, message_contains="typed number"),
        dict(why="CP4 max_mana read in the mana test (the wrong key)",
             code=_mb(_mb_body(mana='caster["max_mana"] < page["mana_cost"]')), fails_at=4,
             message_contains="`\"max_mana\"`"),
        dict(why="CP4 the mana test as a second if (two messages)",
             code=_mb(f"    if {AFF}:\n" + SKILL_MSG + f"    if {MANA}:\n" + MANA_MSG
                      + f"    if not {MANA} and not {AFF}:\n" f"        {EFFECT}\n" + PAY + SHOW),
             fails_at=4, message_contains="2 messages"),
        dict(why="CP4 the mana compared with the required affinity (the wrong key on the page)",
             code=_mb(_mb_body(mana='caster["mana"] < page["required_affinity"]')), fails_at=4,
             message_contains="too little mana still cast"),
        dict(why="CP4 both tests merged into the first with or (the mana case told it isn't skilled)",
             code=_mb(_mb_body(aff=AFF + " or " + MANA)), fails_at=4, message_contains="same message"),
        dict(why="CP4 the same words for both reasons",
             code=_mb(_mb_body(mana_msg=SKILL_MSG)), fails_at=4, message_contains="same message"),
        dict(why="CP4 a typed hero name in the mana message",
             code=_mb(_mb_body(mana_msg='        print("Bomb Shell needs more mana.")\n')), fails_at=4,
             message_contains="a typed name"),
        dict(why="CP5 <= on the mana (> vs >= at the exact boundary; the campaign's own warning)",
             code=MB_P4.replace(TYPED_PAY, PAY), fails_at=5, message_contains="exactly enough mana"),
        dict(why="CP6 a typed cost in the subtraction", code=MB_P5, fails_at=6, message_contains="a typed 7"),
        dict(why="CP6 a typed result (the new mana typed, not worked out)",
             code=_mb(_mb_body(pay='        caster["mana"] = 10\n')), fails_at=6,
             message_contains="whatever the mana and the cost"),
        dict(why="CP6 a typed 4 copied from the check message (Ember Wall's cost)",
             code=_mb(_mb_body(pay='        caster["mana"] = caster["mana"] - 4\n')), fails_at=6,
             message_contains="goes down by a typed number"),
        dict(why="CP6 the starting mana typed from the check message (Ivo's 14)",
             code=_mb(_mb_body(pay='        caster["mana"] = 14 - page["mana_cost"]\n')), fails_at=6,
             message_contains="starts from a typed 14"),
        dict(why="CP6 the subtraction the wrong way round",
             code=_mb(_mb_body(pay='        caster["mana"] = page["mana_cost"] - caster["mana"]\n')), fails_at=6,
             message_contains="the wrong way"),
    ],
    notes=(
        meta(starter_level="S2", path="READY", form="B", part=2,
             skills="dict-nested,elif-chain,boundary,call-stored-func,dict-write,read-helper",
             prepares="hold-the-barrier", solo="true", dictates="1,2,3,4,5", camp="true", hint_cap=2,
             foreign_names="pack,tool,sheet,jar,honey,spoon,size,pour,shelf,price") + "\n"
        "Mini-boss B, 'Hold the Glow Ward' (5.4): the near transfer of hold-the-barrier, form B of two, the same "
        "shape as form A (rc-miniboss-a) so a retake asks for the same help. The follow-up for students who needed "
        "Mar'tu's version on mini-boss A (5.5: 'the mini-boss passed only after Compare, and its immediate twin'), "
        "so it stays dictated. `use_ward(caster, ward_name)`: the spec's `use_ward(caster, ward)` renamed so `ward` "
        "never means the name, as in form A and in this file's own read-and-write task; the page stays `page`. "
        "Given: the guard, `page = caster[\"wards\"][ward_name]`, the finished `show_mana(caster)` (KEEP-checked) "
        "and six numbered comments, one for each checkpoint, in the campaign's check order (2.12 rule 13); the "
        "comments and the intro say the numbers are the checks' order, not the lines' (the code tests the caster "
        "first). The student writes the if / elif / else: the nested affinity test, the `<` mana test, "
        "`page[\"effect\"](caster)`, the subtraction and the redraw. CP1-CP6 are the campaign's six checks, in "
        "order; each casts Ember Wall (a recorder effect) for a fresh hero, Ivo (mana 14 of 20), so the student's "
        "own run of Bomb Shell never has to show a branch; show_mana is swapped for a recorder only during the "
        "check's call. CP1 also checks that the given guard still turns away a ward the caster doesn't know "
        "(Brakka, who knows only Ash Veil, asked for Star Shard), as form A's does, and names form A's habit "
        "`ward[\"effect\"]` (NameError 'ward') and `ward_name[\"effect\"]` (string indices). Turned-away cases "
        "alternate between Ivo and Moss, so a check hero's name copied into a message is caught. CP4 adds a check "
        "that the two reasons print different messages (one test merged with `or`, or the same words twice). BND: "
        "need - 1, need + 1 (with the Glow Ward's own 10 as the typed-number trap), exactly enough affinity (CP3); "
        "cost above the mana (with the Glow Ward's 7 as the trap), both too low at once (CP4: one message, so "
        "`elif`); exactly enough mana at 4 and 9 (CP5); costs 2 and 9 from mana 14 and 17 (CP6), so a typed 7, a "
        "typed result, a typed 4 from the check message, a typed start of 14 and a reversed subtraction each fail. "
        "Partials p2-p5 pay a typed 7, so CP6 turns green last, as in the campaign. Ladders: CP1's Where to look "
        "says early that the cast moves under `else:`; CP2 teaches the pay with `jar[\"honey\"] - spoon[\"size\"]` "
        "(a value read from the other dictionary, never a typed number); CP3's third rung is the jar / spoon "
        "picture of the move under `else:`. Evidence in check messages is short sentences in one pair of "
        "brackets, with none inside.\n"
        "Campaign mode for everyone (2.10, T4), as form A: support='light', solo=True (alone; no Start me off, no "
        "Learn-pane Another way), explainer='lean', no assemble, no tracer, no predict. Hints capped at rung 2 by "
        "writing: Where to look plus two teach rungs, the last never the finished line, and its first code span "
        "gives no Start me off. Compare unlocks by the course setting (the intro promises 5 minutes; the course "
        "setting also opens it after 4 counted failed runs). Site work still needed (as form A): a real hint cap, "
        "Compare by time only, the Readiness result and its 'Compare used' flag (a pass after Compare is recorded "
        "and points the student here), drawing form B for a retake. Messages are campaign-like: what the check "
        "expects and what happened, with the evidence, never the finished line. Optional: form A is the one the "
        "class takes first."
    ),
)


# =============================================================================================
# The trial (challenge, advanced, optional): the same campaign part from its goals only, for ready-to-stretch
# students. A third set of names in form A's pattern: `raise_ward(mage, ward_name)`, the page in its own variable.
# =============================================================================================

TRIAL_SETUP = (
    "_effects = []\n"
    "\n\n"
    "def ember_ward(mage):\n"
    "    _effects.append(mage)\n"
    '    print(mage["name"] + "\'s ember ward flares.")\n'
    "\n\n"
    "oogrish = {\n"
    '    "name": "Oogrish",\n'
    '    "mana": 18,\n'
    '    "max_mana": 18,\n'
    '    "abilities": {"magical_affinity": 9},\n'
    '    "wards": {\n'
    '        "Ember Ward": {\n'
    '            "mana_cost": 6,\n'
    '            "required_affinity": 9,\n'
    '            "effect": ember_ward,\n'
    "        },\n"
    "    },\n"
    "}\n"
)
TRIAL_SHOW_MANA = _show_mana("mage")
TRIAL_HEAD = (
    "# Already finished. Leave it as\n"
    "# it is.\n"
    + TRIAL_SHOW_MANA
    + "\n\n"
    "def raise_ward(mage, ward_name):\n"
    '    if ward_name not in mage["wards"]:\n'
    '        print("Unknown ward:", ward_name)\n'
    "        return\n"
    "    # Get it, compare, act.\n"
)
TRIAL_CALL = '\n\nraise_ward(oogrish, "Ember Ward")\n'
T_GET = '    ward = mage["wards"][ward_name]\n'
T_AFF = 'mage["abilities"]["magical_affinity"] < ward["required_affinity"]'
T_MANA = 'mage["mana"] < ward["mana_cost"]'
T_EFFECT = 'ward["effect"](mage)'
T_PAY = '        mage["mana"] = mage["mana"] - ward["mana_cost"]\n'
T_TYPED_PAY = '        mage["mana"] = mage["mana"] - 6\n'
T_SKILL_MSG = '        print(mage["name"], "isn\'t skilled enough.")\n'
T_MANA_MSG = '        print(mage["name"], "needs more mana.")\n'
T_SHOW = "        show_mana(mage)\n"
T_GUARD_RET = '        print("Unknown ward:", ward_name)\n        return\n'

TRIAL_CFG = dict(
    fn="raise_ward", who="mage", name="ward_name", page="ward", sheet="oogrish", sheet_hero="Oogrish",
    own_fx="ember_ward", own_ward="Ember Ward", own_cost=6, words=["flares", "grows"],
    cw="Briar Ring", cw_line="Briar Ring grows.", foreign=["hero", "caster", "spell", "spell_name"],
    names_line="This one's parameters are `mage` and `ward_name`.",
)


def _tr_body(get=T_GET, aff=T_AFF, mana=T_MANA, effect=T_EFFECT, pay=T_PAY, show=T_SHOW, skill_msg=T_SKILL_MSG,
             mana_msg=T_MANA_MSG):
    return (get + f"    if {aff}:\n" + skill_msg + f"    elif {mana}:\n" + mana_msg + "    else:\n"
            f"        {effect}\n" + pay + show)


def _tr(body="", head=TRIAL_HEAD, call=TRIAL_CALL):
    return head + body + call


TRIAL_STARTER = _tr()
TRIAL_SOLUTION = _tr(_tr_body())
T_P1 = _tr(T_GET + f"    {T_EFFECT}\n")
T_P2 = _tr(T_GET + _flat([f"        {T_EFFECT}\n", T_TYPED_PAY, T_SHOW]))
T_P3 = _tr(T_GET + f"    if {T_AFF}:\n" + T_SKILL_MSG + "    else:\n" + f"        {T_EFFECT}\n" + T_TYPED_PAY + T_SHOW)
T_P4 = _tr(_tr_body(mana=T_MANA.replace("<", "<="), pay=T_TYPED_PAY))
T_P5 = _tr(_tr_body(pay=T_TYPED_PAY))
_TRIAL_CHECKS = _six_checks(TRIAL_CFG, TRIAL_SETUP, TRIAL_SHOW_MANA, "mage")

RC_TRIAL = dict(
    kind="challenge",
    id="rc-trial-ember-ward",
    title="Trial: Hold the Ember Ward from its goals",
    level="advanced",
    optional=True,
    minutes=15,
    summary="Finished early? The same campaign part with goals only: you choose every line.",
    martu=(
        "Finished early, yes? Here is the barrier part with only its goals. The guard is written. The rest is yours, "
        "every line and every name inside: get the ward's page, compare, act.\n"
        "Oogrish's sheet is already made:\n"
        "```python\noogrish = {\n    \"name\": \"Oogrish\",\n    \"mana\": 18,\n    \"max_mana\": 18,\n"
        "    \"abilities\": {\n        \"magical_affinity\": 9,\n    },\n    \"wards\": {\n"
        "        \"Ember Ward\": {\n            \"mana_cost\": 6,\n            \"required_affinity\": 9,\n"
        "            \"effect\": ember_ward,\n        },\n    },\n}\n```\n"
        "`show_mana(mage)` is finished. My check casts for other heroes, with other wards, only inside the check."
    ),
    setup=TRIAL_SETUP,
    names=["raise_ward", "mage", "ward_name", "show_mana"],
    support="light",
    solo=True,
    explainer="lean",
    starter=TRIAL_STARTER,
    checkpoints=[
        dict(
            id="skilled-mage-casts",
            text="A skilled mage with enough mana casts the ward.",
            dictated=False,
            hints=[
                "Look at Oogrish's sheet: each ward's page sits inside `\"wards\"`, under its name, and holds its "
                "`\"effect\"`.",
                "Get it first: a page read from the sheet can go in a variable of its own, so the next lines can "
                "read from it.",
                "A function stored on a page runs when brackets with a value follow it, like `pack[\"tool\"](sheet)`. "
                "Hand it the mage who casts.",
            ],
            checks=_TRIAL_CHECKS[0],
            pass_line="Oogrish: Ember Ward up. Steady, now.",
        ),
        dict(
            id="bar-updates",
            text="The mana bar shows what the cast cost.",
            dictated=False,
            hints=[
                "Look at the ward's page: its `\"mana_cost\"` is what a cast takes from the mage.",
                JAR_PAY,
                "The finished helper draws the bar. Call it after the mana changes, for the mage who cast.",
            ],
            checks=_TRIAL_CHECKS[1],
            pass_line="Bomb Shell: Mana down. Bar drawn. Good.",
        ),
        dict(
            id="low-affinity-no-cast",
            text="Too little affinity: say why, and no cast.",
            dictated=False,
            hints=[
                "Look at the mage's `\"abilities\"`, and at the page's `\"required_affinity\"`.",
                "Two keys in a row read inside a sheet, the outer key first. *Lower than* is `<`.",
                "Only one branch runs. The lines that must wait for the test move one step deeper, under `else:`. "
                "With other names:\n" + JAR_PICTURE,
            ],
            checks=_TRIAL_CHECKS[2],
            pass_line="Lucky: Not skilled enough? Happens to the best of us.",
        ),
        dict(
            id="low-mana-no-cast",
            text="Otherwise, too little mana: say why, and no cast.",
            dictated=False,
            hints=[
                "Look at the chain: this test sits between the first test and the cast.",
                "`elif` asks only when the test above it was false, so one cast prints one message at most.",
                "Each reason gets its own words, so the mage knows which one it was.",
            ],
            checks=_TRIAL_CHECKS[3],
            pass_line="Gearshift: No mana, no cast. Visor dims.",
        ),
        dict(
            id="exactly-enough-mana",
            text="Exactly enough mana still casts.",
            dictated=False,
            hints=[
                "Look at the sign in the mana test.",
                "`<` means *lower than*. `<=` means *lower than or the same*, so it turns away exactly enough.",
                "A mage with 4 mana and a ward that costs 4 has exactly enough: the test must let them through.",
            ],
            checks=_TRIAL_CHECKS[4],
            pass_line="Mar'tu: Exactly enough is enough. The ward holds.",
        ),
        dict(
            id="own-cost",
            text="Each ward's own cost is used.",
            dictated=False,
            hints=[
                "Look at the subtraction. Each ward has its own cost, on its own page.",
                "Read a value from the page you have, like `shelf[\"price\"]`, not a number typed in.",
                "Oogrish's 6 is only the Ember Ward's cost. My check casts wards with other costs.",
            ],
            checks=_TRIAL_CHECKS[5],
            pass_line="Mar'tu: Every line yours, from its goal. Six checks. You held the ward alone.",
        ),
    ],
    solution=TRIAL_SOLUTION,
    partials=[T_P1, T_P2, T_P3, T_P4, T_P5],
    another_way=[
        dict(angle="picture", label="Get it, compare, act", text=(
            "```text\nGet it:  the ward's page\nCompare: affinity < need?\n           -> not skilled\n"
            "         mana < cost?\n           -> not enough\nAct:     cast, pay, draw\n```")),
        dict(angle="from the campaign", label="You've seen this", text=(
            "This is `cast_spell` from hold-the-barrier, with other names: `mage` for `caster`, `ward_name` for "
            "`spell_name`, `\"wards\"` for `\"spell_book\"` and `\"effect\"` for `\"spell_function\"`. The same six "
            "checks, in the same order.")),
    ],
    campaign_link=dict(
        module=M2,
        part="hold-the-barrier",
        why=(
            "You have played this part: `cast_spell` holding the barrier, with most of its lines given. Here you "
            "wrote every line from its goal. The campaign's six checks are these six."
        ),
    ),
    takeaway="Get it, compare, act: read the page, test with `if` / `elif` and `<`, then cast, pay and draw.",
    wrong_answers=[
        dict(why="the starter (the guard only)", code=TRIAL_STARTER, fails_at=1, message_contains="did not cast"),
        dict(why="the page read by a typed ward name (CMB)",
             code=_tr(_tr_body(get='    ward = mage["wards"]["Ember Ward"]\n')), fails_at=1,
             message_contains="reads the ward `\"Ember Ward\"` by a typed name, not the one `ward_name` names"),
        dict(why="Get it skipped: no page variable made (NameError at the student's own run)",
             code=_tr(_tr_body(get="")), fails_at=0, message_contains="name 'ward' is not defined"),
        dict(why="Get it skipped, the given call removed (the check names the error)",
             code=_tr(_tr_body(get=""), call="\n"), fails_at=1,
             message_contains="Inside `raise_ward`, Python stopped with NameError"),
        dict(why="form B's page name copied: page[\"effect\"] (NameError at the student's own run)",
             code=_tr(_tr_body(effect='page["effect"](mage)')), fails_at=0,
             message_contains="name 'page' is not defined"),
        dict(why="the campaign's caster copied, the given call removed (the check names it)",
             code=_tr(_tr_body(aff=T_AFF.replace("mage", "caster", 1)), call="\n"), fails_at=1,
             message_contains="`caster` is a name from another function. This one's parameters are `mage` and "
                              "`ward_name`."),
        dict(why="the effect read, never called (calling vs handing over)",
             code=_tr(_tr_body(effect='ward["effect"]')), fails_at=1, message_contains="nothing calls it"),
        dict(why="ember_ward called by its own name", code=_tr(_tr_body(effect="ember_ward(mage)")), fails_at=1,
             message_contains="by its own name"),
        dict(why="the effect handed the visible hero's sheet (oogrish, not mage)",
             code=_tr(_tr_body(effect='ward["effect"](oogrish)')), fails_at=1,
             message_contains="`raise_ward` uses `oogrish` by name, so Ivo's cast used Oogrish's sheet."),
        dict(why="the effect read from the name, not the page (TypeError)",
             code=_tr(_tr_body(effect='ward_name["effect"](mage)')), fails_at=0,
             message_contains="string indices must be integers"),
        dict(why="a nesting level skipped (KeyError)",
             code=_tr(_tr_body(aff='mage["magical_affinity"] < ward["required_affinity"]')), fails_at=0,
             message_contains="KeyError: 'magical_affinity'"),
        dict(why="the effect's words printed instead of calling it",
             code=_tr(_tr_body(effect='print(mage["name"] + "\'s ember ward flares.")')), fails_at=1,
             message_contains="words were printed"),
        dict(why="print() around the effect call", code=_tr(_tr_body(effect='print(ward["effect"](mage))')),
             fails_at=1, message_contains="showed `None`"),
        dict(why="the given guard's return removed (a given line edited)",
             code=_tr(_tr_body(), head=TRIAL_HEAD.replace(T_GUARD_RET, '        print("Unknown ward:", ward_name)\n')),
             fails_at=1, message_contains="starter's guard"),
        dict(why="CP2 show_mana with no ()", code=_tr(_tr_body(show="        show_mana\n")), fails_at=2,
             message_contains="has no `()`"),
        dict(why="CP2 the subtraction never stored", code=_tr(_tr_body(pay='        mage["mana"] - ward["mana_cost"]\n')),
             fails_at=2, message_contains="never changes"),
        dict(why="CP2 show_mana before the subtraction", code=_tr(_tr_body(pay=T_SHOW + T_PAY, show="")),
             fails_at=2, message_contains="old mana"),
        dict(why="CP2 the finished helper edited",
             code=_tr(_tr_body(), head=TRIAL_HEAD.replace('print(mage["name"], bar)', "print(bar)")), fails_at=2,
             message_contains="was already finished, and it changed"),
        dict(why="CP2 subtracted from max_mana",
             code=_tr(_tr_body(pay='        mage["mana"] = mage["max_mana"] - ward["mana_cost"]\n')), fails_at=2,
             message_contains="`\"max_mana\"`"),
        dict(why="CP3 <= on the affinity", code=_tr(_tr_body(aff=T_AFF.replace("<", "<="))), fails_at=3,
             message_contains="exactly enough affinity"),
        dict(why="CP3 a typed number for the required affinity (the Ember Ward's 9)",
             code=_tr(_tr_body(aff='mage["abilities"]["magical_affinity"] < 9')), fails_at=3,
             message_contains="typed number"),
        dict(why="CP3 the if added above the cast, no else",
             code=_tr(T_GET + f"    if {T_AFF}:\n" + T_SKILL_MSG + _flat([f"        {T_EFFECT}\n", T_PAY, T_SHOW])),
             fails_at=3, message_contains="casts anyway"),
        dict(why="CP3 two ifs, not if / elif",
             code=_tr(T_GET + f"    if {T_AFF}:\n" + T_SKILL_MSG + f"    if {T_MANA}:\n" + T_MANA_MSG + "    else:\n"
                      f"        {T_EFFECT}\n" + T_PAY + T_SHOW), fails_at=3, message_contains="two `if` tests"),
        dict(why="CP3 a typed hero name in the message",
             code=_tr(_tr_body(skill_msg='        print("Oogrish isn\'t skilled enough.")\n')), fails_at=3,
             message_contains="a typed name"),
        dict(why="CP4 a typed number for the cost in the test (the Ember Ward's 6)",
             code=_tr(_tr_body(mana='mage["mana"] < 6')), fails_at=4, message_contains="typed number"),
        dict(why="CP4 the same words for both reasons", code=_tr(_tr_body(mana_msg=T_SKILL_MSG)), fails_at=4,
             message_contains="same message"),
        dict(why="CP4 both tests merged with or", code=_tr(_tr_body(aff=T_AFF + " or " + T_MANA)), fails_at=4,
             message_contains="same message"),
        dict(why="CP5 <= on the mana", code=T_P4.replace(T_TYPED_PAY, T_PAY), fails_at=5,
             message_contains="exactly enough mana"),
        dict(why="CP6 a typed cost in the subtraction", code=T_P5, fails_at=6, message_contains="a typed 6"),
        dict(why="CP6 a typed result", code=_tr(_tr_body(pay='        mage["mana"] = 12\n')), fails_at=6,
             message_contains="whatever the mana and the cost"),
        dict(why="CP6 the starting mana typed from the check message",
             code=_tr(_tr_body(pay='        mage["mana"] = 14 - ward["mana_cost"]\n')), fails_at=6,
             message_contains="starts from a typed 14"),
        dict(why="CP6 the subtraction the wrong way round",
             code=_tr(_tr_body(pay='        mage["mana"] = ward["mana_cost"] - mage["mana"]\n')), fails_at=6,
             message_contains="the wrong way"),
    ],
    notes=(
        meta(starter_level="S1", path="READY", form="trial", part=2,
             skills="dict-nested,elif-chain,boundary,call-stored-func,dict-write,read-helper",
             prepares="hold-the-barrier", solo="true", dictates="", camp="true", hint_cap=2, counts_for_ready="false",
             foreign_names="pack,tool,sheet,jar,honey,spoon,size,pour,shelf,price") + "\n"
        "The trial (optional, advanced, ~15 min): for ready-to-stretch students who finished early. The same "
        "campaign part as the mini-boss, from its goals only: every checkpoint is dictated=False, and the starter "
        "keeps only the guard and one comment, '# Get it, compare, act.', so the student writes every line, the "
        "page read too. A third set of names in form A's pattern: `raise_ward(mage, ward_name)`, the name in "
        "`ward_name`, the page in a variable of the student's own choosing (`ward` in Mar'tu's version). Oogrish's "
        "real values (affinity 9, max mana 18), with the Ember Ward (cost 6, needs 9: exactly enough for him). "
        "Reuses mini-boss B's six checks and its two-messages check (one shared set of check bodies, filled with "
        "this function's names), with Briar Ring as the check ward so no check name looks like the Ember Ward. "
        "Mini-boss B stays dictated: it is the follow-up for students who needed Mar'tu's version. Ladders are "
        "Where to look plus two teach rungs, with no finished line and no Start me off (solo). Not counted for "
        "Ready (5.5): the Ready rule reads mini-boss A, or B after Compare. Site work: nothing marks a challenge as "
        "'not counted for Ready' (the meta line says so), and no route offers it only to students who finished "
        "Part 2 early."
    ),
)


ITEMS = [RC_PART1_B_QUESTIONS, RC_PART1_B, RC_MINIBOSS_B, RC_TRIAL]
